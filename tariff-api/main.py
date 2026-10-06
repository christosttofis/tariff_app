"""
CERA Tariff Comparison Tool — FastAPI backend (Phase 3, local dev)

Run from inside tariff-api/:
    python -m uvicorn main:app

Then open:
    http://localhost:8000/customer.html   ← customer calculator
    http://localhost:8000/admin.html      ← admin panel
    http://localhost:8000/docs            ← auto-generated API docs
"""

import asyncio
import json
import logging
import math
import time
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()  # loads tariff-api/.env if present

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

import jwt

import email_utils
import models
from auth import ACCESS_COOKIE_NAME, ALGORITHM, SECRET_KEY, run_password_expiry_check
from client_ip import UNAVAILABLE_HTML, admin_network_allowed, client_ip_str
from config import TARIFF_BASE_URL, TARIFF_ENABLE_DOCS
from database import SessionLocal, get_db
from routers import admin as admin_router
from routers import auth as auth_router
from routers import public_calc as public_calc_router
from routers import supplier as supplier_router
from routers.admin import run_due_scheduled_notifications
from routers.shared import _uid
from schemas import TariffReportIn
from serializers import supplier_to_dict, tariff_to_public_summary_dict

logger = logging.getLogger(__name__)

# Schema is managed by Alembic (tariff-api/migrations/) rather than
# metadata.create_all() + hand-rolled ALTER TABLE statements — see
# migrations/README_MIGRATIONS.md for why and how to add a new migration.
# Running "upgrade head" here on every startup keeps the previous
# no-manual-step workflow (start.bat just works) while gaining versioning,
# ordering, and a rollback path that the old approach didn't have.
from alembic import command as _alembic_command
from alembic.config import Config as _AlembicConfig

_alembic_cfg = _AlembicConfig(str(Path(__file__).parent / "alembic.ini"))
_alembic_cfg.set_main_option("script_location", str(Path(__file__).parent / "migrations"))
_alembic_command.upgrade(_alembic_cfg, "head")

# Ensure uploads directory exists
(Path(__file__).parent / "uploads").mkdir(exist_ok=True)

app = FastAPI(
    title="CERA Tariff API",
    version="0.3.0",
    description="Backend for the Cyprus electricity tariff comparison tool.",
    docs_url="/docs" if TARIFF_ENABLE_DOCS else None,
    redoc_url="/redoc" if TARIFF_ENABLE_DOCS else None,
    openapi_url="/openapi.json" if TARIFF_ENABLE_DOCS else None,
)

# ── Per-IP rate limiting ────────────────────────────────────────────────────
# Guards against accidental overload (a stuck retry loop, a mis-run script)
# rather than sophisticated abuse. Self-contained sliding-window counter per
# client IP, applied to every route — deliberately not using a routing-library
# based limiter (e.g. slowapi) because its route-handler lookup doesn't
# recognize routes registered via app.include_router() on this FastAPI/
# Starlette version, so it silently rate-limited nothing under /api/auth or
# /api/admin. In-memory only: correct for the single-process deployment this
# app assumes (see the scheduled-notifications loop below); would need a
# shared store (e.g. Redis) if ever scaled to multiple instances/workers.
_RATE_LIMIT_WINDOW_SECONDS = 60
_RATE_LIMIT_MAX_REQUESTS = 60
_rate_limit_buckets: dict[str, list[float]] = {}


def _is_rate_limited(client_ip: str) -> bool:
    now = time.monotonic()
    cutoff = now - _RATE_LIMIT_WINDOW_SECONDS
    bucket = _rate_limit_buckets.setdefault(client_ip, [])
    while bucket and bucket[0] < cutoff:
        bucket.pop(0)
    if len(bucket) >= _RATE_LIMIT_MAX_REQUESTS:
        return True
    bucket.append(now)
    return False


@app.middleware("http")
async def rate_limit_middleware(request, call_next):
    # Same trusted-IP rule as the admin network check (client_ip.py): behind
    # Azure this is the address the front end saw, not a client-supplied
    # X-Forwarded-For value that could be rotated to get unlimited buckets.
    client_ip = client_ip_str(request) or "unknown"
    if not _is_rate_limited(client_ip):
        return await call_next(request)

    # Auth endpoints already have a "Login activity" audit trail (models.LoginActivity)
    # shown in the admin panel — record rate-limit hits there too so an admin sees a
    # retry storm alongside lockouts/bad-password attempts, instead of only in server logs.
    if request.url.path.startswith("/api/auth/"):
        email = "(unknown)"
        try:
            body = await request.json()
            email = body.get("email") or email
        except Exception:
            pass
        db = SessionLocal()
        try:
            db.add(models.LoginActivity(
                email=email,
                user_id=None,
                success=False,
                reason="rate_limited",
                ip_address=client_ip,
                user_agent=request.headers.get("user-agent"),
                ts=datetime.now(timezone.utc).isoformat(),
            ))
            db.commit()
        except Exception:
            logger.exception("Failed to record rate-limited login activity")
        finally:
            db.close()

    return JSONResponse(
        {"error": f"Rate limit exceeded: {_RATE_LIMIT_MAX_REQUESTS} per {_RATE_LIMIT_WINDOW_SECONDS} seconds"},
        status_code=429,
    )

# Frontend is normally served same-origin by this app (relative fetch calls), so this
# only matters for cross-origin access — restrict to the actual deployment URL rather
# than "*". Set TARIFF_BASE_URL per-environment; it's already used for email links.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[TARIFF_BASE_URL],
    allow_methods=["*"],
    allow_headers=["*"],
)

# customer.html/admin.html are hundreds of KB of uncompressed HTML+inline JS
# served on every page load; gzip cuts that transfer size substantially with
# no code changes on the frontend side.
app.add_middleware(GZipMiddleware, minimum_size=500)

# Content-Security-Policy. Scripts may only come from this origin's own files and
# cdnjs (Chart.js/DOMPurify): no inline <script> blocks or onclick="..." handlers, so
# code an attacker manages to plant into a page is refused by the browser even if
# escaping ever missed it. Also: no plugins/objects, no framing by other sites, no
# cross-origin form posts or fetch/XHR, styles/fonts only from this origin + Google
# Fonts. style-src still allows inline styles (style="..."), which can't run code.
_CSP_POLICY = (
    "default-src 'self'; "
    "script-src 'self' https://cdnjs.cloudflare.com; "
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
    "font-src 'self' https://fonts.gstatic.com; "
    "img-src 'self' data:; "
    "connect-src 'self'; "
    "object-src 'none'; "
    "base-uri 'self'; "
    "form-action 'self'; "
    "frame-ancestors 'self'"
)
# TEMPORARY, while the remaining pages are converted page by page (see
# SECURITY_REMEDIATION_CHECKLIST.md, open items): these still contain inline
# scripts/handlers, so they get the old policy that allows them. Delete this
# (and _CSP_LEGACY) once the set is empty.
_CSP_LEGACY_PAGES = {"/supplier.html", "/admin.html"}
_CSP_LEGACY = _CSP_POLICY.replace("script-src 'self'", "script-src 'self' 'unsafe-inline'")


@app.middleware("http")
async def add_csp_header(request, call_next):
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = (
        _CSP_LEGACY if request.url.path in _CSP_LEGACY_PAGES else _CSP_POLICY)
    # Standard hardening headers alongside CSP: block MIME-sniffing away from
    # the declared Content-Type, avoid leaking the full referrer URL to other
    # origins, and disable browser features this app never uses.
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    if request.url.scheme == "https":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


# admin.html and supplier.html each verify their required role once, at page
# load — but the session lives in a browser-wide cookie, not a per-tab one.
# If a user logs into the other role in a second tab, that overwrites the
# cookie for every tab, including one that's already sitting on the "wrong"
# portal — and subsequent API calls from that tab silently start acting under
# the new identity instead of failing (a supplier tab that inherits an admin
# cookie gets full unfiltered data back with no error at all). This header
# lets each page's fetch interceptor notice the swap and force a fresh login,
# regardless of which specific endpoint happened to be called.
@app.middleware("http")
async def add_role_header(request, call_next):
    response = await call_next(request)
    token = request.cookies.get(ACCESS_COOKIE_NAME)
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if payload.get("purpose") != "otp":
                response.headers["X-User-Role"] = payload.get("role", "")
        except jwt.InvalidTokenError:
            pass
    return response

# ── Scheduled notifications background loop ────────────────────────────────────
# Single in-process loop — assumes one running app instance (true for the
# current Basic B1 App Service / local dev setup). Scaling to multiple
# instances later would need a lock to avoid double-sending a schedule.
_SCHEDULER_INTERVAL_SECONDS = 3600
_last_password_check_date: str | None = None


async def _scheduled_notifications_loop():
    global _last_password_check_date
    while True:
        try:
            db = SessionLocal()
            try:
                run_due_scheduled_notifications(db)

                # Password expiry only needs checking once per day.
                today = datetime.now(timezone.utc).date().isoformat()
                if today != _last_password_check_date:
                    run_password_expiry_check(db)
                    _last_password_check_date = today
            finally:
                db.close()
        except Exception:
            logger.exception("Scheduled notifications loop failed")
        await asyncio.sleep(_SCHEDULER_INTERVAL_SECONDS)


@app.on_event("startup")
async def _start_scheduled_notifications_loop():
    asyncio.create_task(_scheduled_notifications_loop())


# Auth router — /api/auth/login (public, no token required)
app.include_router(auth_router.router)

# Admin router — all /api/admin/... routes (admin role only, enforced router-wide)
app.include_router(admin_router.router)

# Supplier router — all /api/supplier/... routes (supplier role only, enforced
# router-wide; every query scoped to the caller's own supplier)
app.include_router(supplier_router.router)

# Public calculation router — /api/public/calculate, /api/public/sample-invoice
# (Phase 1 of the customer-data-exposure fix: engine built and reachable, but
# customer.html doesn't call it yet and /api/public/config is unchanged — see
# SECURITY_REMEDIATION_PLAN_customer_data_exposure.md)
app.include_router(public_calc_router.router)


# Unhandled exceptions otherwise fall through to Starlette's default
# ServerErrorMiddleware, which returns a plain-text "Internal Server Error"
# body rather than JSON - every other error path in this app (HTTPException,
# the rate-limit 429) returns JSON with a "detail"/"error" key, and the
# frontend's error handling (e.g. admin.html:1886, `e.detail||resp.status`)
# expects JSON it can parse. This keeps a 500 in that same shape and ensures
# it's always logged server-side.
@app.exception_handler(Exception)
async def _unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception on %s %s", request.method, request.url.path)
    return JSONResponse({"detail": "Internal server error"}, status_code=500)


def _sanitize_non_finite(obj):
    """Replace NaN/Infinity floats with their str() form so the result is
    always strict-JSON-serializable."""
    if isinstance(obj, float) and not math.isfinite(obj):
        return str(obj)
    if isinstance(obj, dict):
        return {k: _sanitize_non_finite(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sanitize_non_finite(v) for v in obj]
    return obj


# A request that fails validation because a numeric field is NaN/Infinity
# (rejected via allow_inf_nan=False on the public calculate/sample-invoice
# schemas) has that same NaN/Infinity value echoed back in the error detail's
# "input" field by FastAPI's default handler - and Starlette's JSONResponse
# uses strict JSON encoding (allow_nan=False), so *serializing that 422*
# raises and becomes an unhandled 500 instead. Same shape as FastAPI's
# default handler, just with non-finite floats in the payload made safe first.
@app.exception_handler(RequestValidationError)
async def _validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        {"detail": _sanitize_non_finite(jsonable_encoder(exc.errors()))},
        status_code=422,
    )


@app.get("/health", summary="Liveness/readiness check for uptime monitoring and load balancers")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok"}


# ── Public endpoint ───────────────────────────────────────────────────────────

@app.get("/api/public/config", summary="Display/filter metadata consumed by customer calculator")
def get_public_config(db: Session = Depends(get_db)):
    """
    Display-only metadata for the public customer calculator — supplier
    contact info, per-tariff filter/display fields (no rates, discounts,
    load profiles, regulated rates, or DAM price data). Pricing is computed
    server-side via POST /api/public/calculate and POST /api/public/sample-invoice
    instead — see SECURITY_REMEDIATION_PLAN_customer_data_exposure.md
    (Phase 3: this is the endpoint the data-exposure fix actually lands on).
    Only includes tariffs with status='approved'.
    """
    suppliers = db.query(models.Supplier).all()
    tariffs   = db.query(models.Tariff).filter(models.Tariff.status == "approved").all()
    notices   = db.query(models.Notices).first()
    sample_invoice_cfg = db.query(models.SampleInvoiceConfig).first()
    changelog = db.query(models.Changelog).order_by(models.Changelog.ts.desc()).all()

    return {
        "version": 5,
        "suppliers": [supplier_to_dict(s) for s in suppliers],
        "tariffs":   [tariff_to_public_summary_dict(t) for t in tariffs],
        "notices": {
            "assumptions_en": notices.assumptions_en or "" if notices else "",
            "assumptions_el": notices.assumptions_el or "" if notices else "",
            "legal_en":       notices.legal_en       or "" if notices else "",
            "legal_el":       notices.legal_el       or "" if notices else "",
            "vulnerable_en":  notices.vulnerable_en  or "" if notices else "",
            "vulnerable_el":  notices.vulnerable_el  or "" if notices else "",
        },
        "sampleInvoiceEnabled": bool(sample_invoice_cfg.enabled) if sample_invoice_cfg else False,
        "changelog": [
            {
                "id": c.id, "tariffId": c.tariffId, "tariffName": c.tariffName,
                "supplier": c.supplier, "action": c.action,
                "changes": json.loads(c.changes) if c.changes else [],
                "ts": c.ts, "actorRole": c.actorRole, "actorEmail": c.actorEmail,
            }
            for c in changelog
        ],
        "savedAt": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/api/public/report-tariff", summary="Report an issue with a published tariff, or a general site issue")
def report_tariff(body: TariffReportIn, request: Request, db: Session = Depends(get_db)):
    """Article 121(ζ) — customer-facing "report erroneous offer info" process.
    No login required (customer.html has no auth); tariff_name/supplier are
    looked up server-side rather than trusted from the client. body.tariff_id
    is None for a general issue submitted via the page footer, not tied to
    any one tariff."""
    tariff_name = supplier = None
    if body.tariff_id:
        t = db.query(models.Tariff).filter(
            models.Tariff.id == body.tariff_id, models.Tariff.status == "approved"
        ).first()
        if not t:
            raise HTTPException(404, "Tariff not found")
        tariff_name, supplier = t.name, t.supplier
    r = models.TariffReport(
        id=_uid(),
        tariffId=body.tariff_id,
        tariffName=tariff_name,
        supplier=supplier,
        category=body.category,
        note=body.note,
        reporterEmail=body.reporter_email,
        status="open",
        createdAt=datetime.now(timezone.utc).isoformat(),
        ipAddress=client_ip_str(request),
    )
    db.add(r)
    db.commit()
    email_utils.notify_admin_tariff_report(tariff_name, supplier, body.category, body.note, body.reporter_email)
    return {"ok": True}


# ── Static file serving ───────────────────────────────────────────────────────
# Only these files are served. This used to be a StaticFiles mount of the whole
# project folder, which also exposed tariff-api/.env (secrets), the source code,
# .git, internal documents and uploaded tariff PDFs to anyone who could reach
# the server. An explicit allowlist means a new file in the folder is never
# public by accident.
_STATIC_ROOT = Path(__file__).parent.parent
_PUBLIC_FILES = {
    "customer.html": "text/html; charset=utf-8",
    "customer.js": "text/javascript; charset=utf-8",
    "supplier.html": "text/html; charset=utf-8",
    "admin.html": "text/html; charset=utf-8",
    "reset-password.html": "text/html; charset=utf-8",   # linked from invite/reset emails
    "reset-password.js": "text/javascript; charset=utf-8",
    "Logo_Transparent.png": "image/png",
}


def _static_route(name: str, media_type: str):
    path = _STATIC_ROOT / name

    def serve(request: Request):
        # The admin panel is only served inside the CERA office/VPN networks;
        # outside, a plain "Website unavailable" (same as the admin API).
        if name == "admin.html" and not admin_network_allowed(request):
            return HTMLResponse(UNAVAILABLE_HTML, status_code=404)
        return FileResponse(path, media_type=media_type)
    serve.__name__ = "static_" + name.replace(".", "_").replace("-", "_")
    return serve


for _name, _media_type in _PUBLIC_FILES.items():
    app.add_api_route("/" + _name, _static_route(_name, _media_type), methods=["GET", "HEAD"], include_in_schema=False)
