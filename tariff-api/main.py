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
import random
import string
import time
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()  # loads tariff-api/.env if present

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

import jwt

import email_utils
import models
from auth import ACCESS_COOKIE_NAME, ALGORITHM, SECRET_KEY, run_password_expiry_check
from config import TARIFF_BASE_URL
from database import SessionLocal, get_db
from routers import admin as admin_router
from routers import auth as auth_router
from routers.admin import run_due_scheduled_notifications
from schemas import TariffReportIn
from serializers import profile_to_dict, supplier_to_dict, tariff_to_dict

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
    client_ip = request.client.host if request.client else "unknown"
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

# Content-Security-Policy — permissive on script/style ('unsafe-inline') because the
# frontend is ~hundreds of inline onclick="..." handlers plus inline <script> blocks;
# blocking those without 'unsafe-inline' would require refactoring every handler to
# addEventListener first (tracked separately). Still meaningfully restricts everything
# else: no plugins/objects, no framing by other sites, no cross-origin form posts or
# fetch/XHR, and scripts/styles/fonts only from this origin + the two CDN hosts actually
# used (cdnjs for Chart.js/DOMPurify, fonts.googleapis.com/fonts.gstatic.com for Roboto).
_CSP_POLICY = (
    "default-src 'self'; "
    "script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; "
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
    "font-src 'self' https://fonts.gstatic.com; "
    "img-src 'self' data:; "
    "connect-src 'self'; "
    "object-src 'none'; "
    "base-uri 'self'; "
    "form-action 'self'; "
    "frame-ancestors 'self'"
)


@app.middleware("http")
async def add_csp_header(request, call_next):
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = _CSP_POLICY
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

# Admin router — all /api/admin/... routes (protected)
app.include_router(admin_router.router)


# ── Public endpoint ───────────────────────────────────────────────────────────

@app.get("/api/public/config", summary="Config consumed by customer calculator")
def get_public_config(db: Session = Depends(get_db)):
    """
    Returns a JSON object in exactly the same shape as the localStorage
    'elec-config-v5' key, but only includes tariffs with status='approved'.
    """
    suppliers = db.query(models.Supplier).all()
    profiles  = db.query(models.Profile).all()
    tariffs   = db.query(models.Tariff).filter(models.Tariff.status == "approved").all()
    regulated = db.query(models.Regulated).first()
    dam       = db.query(models.DamData).first()
    notices   = db.query(models.Notices).first()
    changelog = db.query(models.Changelog).order_by(models.Changelog.ts.desc()).all()

    reg = regulated
    return {
        "version": 5,
        "suppliers": [supplier_to_dict(s) for s in suppliers],
        "profiles":  [profile_to_dict(p)  for p in profiles],
        "tariffs":   [tariff_to_dict(t)   for t in tariffs],
        "regulated": {
            "lv":    reg.lv    if reg else 0,
            "mv":    reg.mv    if reg else 0,
            "hv":    reg.hv    if reg else 0,
            "fpaLV": reg.fpaLV if reg else 0,
            "fpaMV": reg.fpaMV if reg else 0,
            "fpaHV": reg.fpaHV if reg else 0,
            "pso":   reg.pso   if reg else 0,
            "res":   reg.res   if reg else 0,
            "mdm":   reg.mdm   if reg else 0,
            "updated_at":         reg.updated_at         if reg else None,
            "fpa_updated_at":     reg.fpa_updated_at     if reg else None,
            "grid_updated_at":    reg.grid_updated_at    if reg else None,
            "universal_updated_at": reg.universal_updated_at if reg else None,
        },
        "notices": {
            "assumptions_en": notices.assumptions_en or "" if notices else "",
            "assumptions_el": notices.assumptions_el or "" if notices else "",
            "legal_en":       notices.legal_en       or "" if notices else "",
            "legal_el":       notices.legal_el       or "" if notices else "",
            "vulnerable_en":  notices.vulnerable_en  or "" if notices else "",
            "vulnerable_el":  notices.vulnerable_el  or "" if notices else "",
        },
        "damMonthly":   json.loads(dam.damMonthly)   if dam and dam.damMonthly   else [None] * 12,
        "damBySlot":    json.loads(dam.damBySlot)    if dam and dam.damBySlot    else [],
        "damDailyData": json.loads(dam.damDailyData) if dam and dam.damDailyData else [[] for _ in range(12)],
        "damRowCount":  dam.damRowCount if dam else 0,
        "damYear":      dam.damYear     if dam else 2026,
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


def _uid() -> str:
    ts = int(time.time() * 1000)
    rand = "".join(random.choices(string.ascii_lowercase + string.digits, k=4))
    return f"{ts:x}{rand}"


@app.post("/api/public/report-tariff", summary="Report an issue with a published tariff")
def report_tariff(body: TariffReportIn, request: Request, db: Session = Depends(get_db)):
    """Article 121(ζ) — customer-facing "report erroneous offer info" process.
    No login required (customer.html has no auth); tariff_name/supplier are
    looked up server-side rather than trusted from the client."""
    t = db.query(models.Tariff).filter(
        models.Tariff.id == body.tariff_id, models.Tariff.status == "approved"
    ).first()
    if not t:
        raise HTTPException(404, "Tariff not found")
    r = models.TariffReport(
        id=_uid(),
        tariffId=t.id,
        tariffName=t.name,
        supplier=t.supplier,
        note=body.note,
        status="open",
        createdAt=datetime.now(timezone.utc).isoformat(),
        ipAddress=request.client.host if request.client else None,
    )
    db.add(r)
    db.commit()
    email_utils.notify_admin_tariff_report(t.name, t.supplier, body.note)
    return {"ok": True}


# ── Static file serving ───────────────────────────────────────────────────────
# Serves admin.html and customer.html from the parent directory.
# Declared last so /api/... routes above are matched first.
_STATIC_ROOT = Path(__file__).parent.parent
app.mount("/", StaticFiles(directory=str(_STATIC_ROOT), html=False), name="static")
