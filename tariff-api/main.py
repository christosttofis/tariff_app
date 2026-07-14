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
import os
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()  # loads tariff-api/.env if present

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

import models
from auth import run_password_expiry_check
from database import SessionLocal, engine, get_db
from routers import admin as admin_router
from routers import auth as auth_router
from routers.admin import run_due_scheduled_notifications
from serializers import profile_to_dict, supplier_to_dict, tariff_to_dict

logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)

# Ensure uploads directory exists
(Path(__file__).parent / "uploads").mkdir(exist_ok=True)

# Add columns introduced after initial schema creation
from sqlalchemy import text as _text
with engine.connect() as _c:
    for _col in [
        "ALTER TABLE tariffs ADD COLUMN rejection_reason TEXT",
        "ALTER TABLE tariffs ADD COLUMN mdm REAL DEFAULT 0.0",
        "ALTER TABLE regulated ADD COLUMN res REAL DEFAULT 0.0",
        "ALTER TABLE regulated ADD COLUMN updated_at TEXT",
        "ALTER TABLE regulated ADD COLUMN fpa_updated_at TEXT",
        "ALTER TABLE regulated ADD COLUMN grid_updated_at TEXT",
        "ALTER TABLE regulated ADD COLUMN universal_updated_at TEXT",
        "ALTER TABLE changelog ADD COLUMN \"actorRole\" TEXT",
        "ALTER TABLE changelog ADD COLUMN \"actorEmail\" TEXT",
        "ALTER TABLE otp_codes ADD COLUMN created_at TEXT",
        "ALTER TABLE users ADD COLUMN otp_enabled INTEGER DEFAULT 1",
        "ALTER TABLE users ADD COLUMN password_changed_at TEXT",
        "ALTER TABLE users ADD COLUMN must_change_password INTEGER DEFAULT 0",
        "ALTER TABLE users ADD COLUMN password_expiry_notified_at TEXT",
    ]:
        try:
            _c.execute(_text(_col)); _c.commit()
        except Exception:
            # Postgres aborts the whole transaction on error (unlike SQLite,
            # which tolerates it per-statement) — roll back so the next
            # statement in the loop can still run.
            _c.rollback()

    # One-time backfill: existing users get password_changed_at = now so nobody
    # is instantly flagged as expired by the new rotation policy.
    _c.execute(_text(
        "UPDATE users SET password_changed_at = :now WHERE password_changed_at IS NULL"
    ), {"now": datetime.now(timezone.utc).isoformat()})
    _c.commit()

app = FastAPI(
    title="CERA Tariff API",
    version="0.3.0",
    description="Backend for the Cyprus electricity tariff comparison tool.",
)

# Frontend is normally served same-origin by this app (relative fetch calls), so this
# only matters for cross-origin access — restrict to the actual deployment URL rather
# than "*". Set TARIFF_BASE_URL per-environment; it's already used for email links.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("TARIFF_BASE_URL", "http://localhost:8000")],
    allow_methods=["*"],
    allow_headers=["*"],
)

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


# ── Static file serving ───────────────────────────────────────────────────────
# Serves admin.html and customer.html from the parent directory.
# Declared last so /api/... routes above are matched first.
_STATIC_ROOT = Path(__file__).parent.parent
app.mount("/", StaticFiles(directory=str(_STATIC_ROOT), html=False), name="static")
