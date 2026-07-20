"""
Admin API router.

Auth rules
----------
  get_current_user  — any logged-in user (admin or supplier)
  require_admin     — CERA admin only

Tariff ownership
----------------
  Suppliers may only create / update / delete their own tariffs.
  Status changes (approve / reject) are admin-only.
  Admins can touch any tariff.
"""

import calendar
import json
import os
import random
import secrets
import string
import time
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import email_utils

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

import models
from auth import CurrentUser, get_current_user, hash_password, require_admin, resolve_supplier_name
from database import get_db
from importer import import_cfg
from schemas import (
    CreateUserIn, DamIn, MessageArchiveIn, MessageIn, NoticesIn, ProfileIn, RegulatedIn,
    ScheduledNotificationEnabledIn, ScheduledNotificationIn, SupplierIn, TariffIn, TariffStatusIn,
    UserOtpToggleIn, UserStatusIn,
)
from serializers import message_to_dict, profile_to_dict, scheduled_notification_to_dict, supplier_to_dict, tariff_to_dict

router = APIRouter(prefix="/api/admin", tags=["admin"])

_VALID_STATUSES = {"draft", "pending", "approved", "rejected", "suspended"}


def _uid() -> str:
    ts = int(time.time() * 1000)
    rand = "".join(random.choices(string.ascii_lowercase + string.digits, k=4))
    return f"{ts:x}{rand}"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _add_changelog(db, *, action, tariff_id, tariff_name, supplier, changes, actor: CurrentUser | None = None):
    db.add(models.Changelog(
        id=_uid(), tariffId=tariff_id, tariffName=tariff_name,
        supplier=supplier, action=action,
        changes=json.dumps(changes), ts=_now(),
        actorRole=actor.role if actor else None,
        actorEmail=actor.email if actor else None,
    ))


def _dam_to_dict(d: models.DamData | None) -> dict:
    if not d:
        return {"damMonthly": [None]*12, "damBySlot": [], "damDailyData": [[] for _ in range(12)], "damRowCount": 0, "damYear": 2026}
    return {
        "damMonthly":   json.loads(d.damMonthly)   if d.damMonthly   else [None]*12,
        "damBySlot":    json.loads(d.damBySlot)    if d.damBySlot    else [],
        "damDailyData": json.loads(d.damDailyData) if d.damDailyData else [[] for _ in range(12)],
        "damRowCount":  d.damRowCount,
        "damYear":      d.damYear,
    }


def _notices_to_dict(n: models.Notices | None) -> dict:
    empty = {"assumptions_en": "", "assumptions_el": "", "legal_en": "", "legal_el": "", "vulnerable_en": "", "vulnerable_el": ""}
    if not n:
        return empty
    return {k: (getattr(n, k) or "") for k in empty}


def _regulated_to_dict(r: models.Regulated | None) -> dict:
    if not r:
        return {"lv": 0, "mv": 0, "hv": 0, "fpaLV": 0, "fpaMV": 0, "fpaHV": 0, "pso": 0, "res": 0, "mdm": 0,
                "updated_at": None, "fpa_updated_at": None, "grid_updated_at": None, "universal_updated_at": None}
    return {"lv": r.lv, "mv": r.mv, "hv": r.hv, "fpaLV": r.fpaLV, "fpaMV": r.fpaMV, "fpaHV": r.fpaHV, "pso": r.pso, "res": r.res, "mdm": r.mdm,
            "updated_at": r.updated_at, "fpa_updated_at": r.fpa_updated_at,
            "grid_updated_at": r.grid_updated_at, "universal_updated_at": r.universal_updated_at}


_REGULATED_LABELS = {
    "lv":    "Network — LV (€/kWh)",
    "mv":    "Network — MV (€/kWh)",
    "hv":    "Network — HV (€/kWh)",
    "fpaLV": "FPA — LV (€/kWh)",
    "fpaMV": "FPA — MV (€/kWh)",
    "fpaHV": "FPA — HV (€/kWh)",
    "pso":   "PSO (€/kWh)",
    "res":   "RES & Energy Conservation Fund (€/kWh)",
    "mdm":   "MDM (€/month)",
}


def _fmt_rate(v: float) -> str:
    """Format a rate value, stripping unnecessary trailing zeros."""
    return f"{v:.6f}".rstrip("0").rstrip(".") if v else "0"


def _supplier_emails(db, supplier_name: str) -> list[str]:
    """Return email addresses of all active users for a given supplier (looked
    up by name, e.g. from Tariff.supplier, then matched to users via supplier_id)."""
    supplier = db.query(models.Supplier).filter(models.Supplier.name == supplier_name).first()
    if not supplier:
        return []
    users = db.query(models.User).filter(
        models.User.supplier_id == supplier.id,
        models.User.is_active == True,
    ).all()
    return [u.email for u in users if u.email]


def _assert_tariff_owner(t: models.Tariff, user: CurrentUser) -> None:
    """Raise 403 if a supplier tries to touch another supplier's tariff."""
    if not user.is_admin and t.supplier != user.supplier_name:
        raise HTTPException(403, "You can only modify your own tariffs")


# ── Bulk config ───────────────────────────────────────────────────────────────

@router.get("/config", summary="Full config for admin — all tariff statuses")
def get_admin_config(
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    suppliers = db.query(models.Supplier).all()
    profiles  = db.query(models.Profile).all()
    # Suppliers see only their own tariffs; admins see all
    tq = db.query(models.Tariff)
    if user.is_supplier:
        tq = tq.filter(models.Tariff.supplier == user.supplier_name)
    tariffs   = tq.all()
    regulated = db.query(models.Regulated).first()
    dam       = db.query(models.DamData).first()
    notices   = db.query(models.Notices).first()
    cq = db.query(models.Changelog)
    if user.is_supplier:
        cq = cq.filter(models.Changelog.supplier == user.supplier_name)
    changelog = cq.order_by(models.Changelog.ts.desc()).all()

    tariff_ids = [t.id for t in tariffs]
    doc_tariff_ids = [
        row[0] for row in
        db.query(models.TariffDocument.tariff_id).filter(
            models.TariffDocument.tariff_id.in_(tariff_ids)
        ).distinct().all()
    ] if tariff_ids else []

    return {
        "version": 5,
        "suppliers":  [supplier_to_dict(s) for s in suppliers],
        "profiles":   [profile_to_dict(p)  for p in profiles],
        "tariffs":    [tariff_to_dict(t)   for t in tariffs],
        "regulated":  _regulated_to_dict(regulated),
        "notices":    _notices_to_dict(notices),
        **_dam_to_dict(dam),
        "changelog": [
            {"id": c.id, "tariffId": c.tariffId, "tariffName": c.tariffName,
             "supplier": c.supplier, "action": c.action,
             "changes": json.loads(c.changes) if c.changes else [], "ts": c.ts,
             "actorRole": c.actorRole, "actorEmail": c.actorEmail}
            for c in changelog
        ],
        "docTariffIds": doc_tariff_ids,
        "savedAt": _now(),
    }


@router.put("/config", summary="Replace all config from admin Publish (admin only)")
def put_admin_config(
    payload: dict[str, Any],
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_admin),
):
    try:
        return import_cfg(payload, db)
    except Exception as exc:
        raise HTTPException(400, str(exc))


# ── Tariffs ───────────────────────────────────────────────────────────────────

@router.get("/tariffs", summary="List tariffs")
def list_tariffs(
    status: str | None = None,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    q = db.query(models.Tariff)
    if user.is_supplier:
        q = q.filter(models.Tariff.supplier == user.supplier_name)
    if status:
        if status not in _VALID_STATUSES:
            raise HTTPException(400, f"status must be one of {_VALID_STATUSES}")
        q = q.filter(models.Tariff.status == status)
    return [tariff_to_dict(t) for t in q.all()]


@router.post("/tariffs", status_code=201, summary="Create a tariff")
def create_tariff(
    body: TariffIn,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    # Suppliers can only create tariffs under their own supplier name
    if user.is_supplier and body.supplier != user.supplier_name:
        raise HTTPException(403, f"You can only create tariffs for '{user.supplier_name}'")
    tariff_id = body.id or _uid()
    now = _now()
    t = models.Tariff(
        id=tariff_id, name=body.name, supplier=body.supplier,
        contract=body.contract, voltage=body.voltage, pricing=body.pricing,
        standing=body.standing, mdm=body.mdm, rates=json.dumps(body.rates),
        profileId=body.profileId, fpaSource=body.fpaSource, fpaCustom=body.fpaCustom,
        durationMonths=body.durationMonths, loadEntitlement=body.loadEntitlement,
        discounts=json.dumps(body.discounts), vulnerable=body.vulnerable,
        status="pending" if user.is_supplier else "approved",
        createdAt=now, updatedAt=now,
    )
    db.add(t)
    _add_changelog(db, action="created", tariff_id=tariff_id,
                   tariff_name=body.name, supplier=body.supplier, changes=[], actor=user)
    db.commit()
    db.refresh(t)
    if user.is_supplier:
        email_utils.notify_admin_new_tariff(body.name, body.supplier)
    return tariff_to_dict(t)


@router.get("/tariffs/{tariff_id}", summary="Get a single tariff")
def get_tariff(
    tariff_id: str,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    t = db.get(models.Tariff, tariff_id)
    if not t:
        raise HTTPException(404, "Tariff not found")
    _assert_tariff_owner(t, user)
    return tariff_to_dict(t)


def _profile_label(db: Session, profile_id) -> str:
    """Render a profile id as 'Name' for changelog display, falling back to the raw id."""
    if not profile_id:
        return ""
    p = db.get(models.Profile, profile_id)
    return p.name if p else str(profile_id)


def _diff_fields(db: Session, old: models.Tariff, body: TariffIn) -> list[dict]:
    """Compare old DB record against incoming body; return list of {field, from, to}."""
    changes = []
    for field, ov, nv in [
        ("name",            old.name,            body.name),
        ("contract",        old.contract,        body.contract),
        ("voltage",         old.voltage,         body.voltage),
        ("pricing",         old.pricing,         body.pricing),
        ("standing",        old.standing,        body.standing),
        ("fpaSource",       old.fpaSource,       body.fpaSource),
        ("fpaCustom",       old.fpaCustom,       body.fpaCustom),
        ("durationMonths",  old.durationMonths,  body.durationMonths),
        ("loadEntitlement", old.loadEntitlement, body.loadEntitlement),
        ("vulnerable",      old.vulnerable,      body.vulnerable),
        ("profileId",       old.profileId,       body.profileId),
    ]:
        if str(ov if ov is not None else "") != str(nv if nv is not None else ""):
            if field == "profileId":
                changes.append({"field": field,
                                "from": _profile_label(db, ov),
                                "to":   _profile_label(db, nv)})
            else:
                changes.append({"field": field,
                                "from": "" if ov is None else str(ov),
                                "to":   "" if nv is None else str(nv)})
    old_rates = json.loads(old.rates) if old.rates else {}
    if old_rates != body.rates:
        changes.append({"field": "rates", "from": json.dumps(old_rates), "to": json.dumps(body.rates)})
    old_disc = json.loads(old.discounts) if old.discounts else []
    if old_disc != body.discounts:
        changes.append({"field": "discounts",
                        "from": json.dumps(old_disc),
                        "to":   json.dumps(body.discounts)})
    return changes


@router.put("/tariffs/{tariff_id}", summary="Replace a tariff")
def update_tariff(
    tariff_id: str,
    body: TariffIn,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    t = db.get(models.Tariff, tariff_id)
    if not t:
        raise HTTPException(404, "Tariff not found")
    _assert_tariff_owner(t, user)
    changes = _diff_fields(db, t, body)   # capture diff before modifying t
    t.name = body.name; t.supplier = body.supplier
    t.contract = body.contract; t.voltage = body.voltage; t.pricing = body.pricing
    t.standing = body.standing; t.mdm = body.mdm; t.rates = json.dumps(body.rates)
    t.profileId = body.profileId; t.fpaSource = body.fpaSource; t.fpaCustom = body.fpaCustom
    t.durationMonths = body.durationMonths; t.loadEntitlement = body.loadEntitlement
    t.discounts = json.dumps(body.discounts); t.vulnerable = body.vulnerable
    t.updatedAt = _now()
    if user.is_supplier:
        t.status = "pending"
    _add_changelog(db, action="updated", tariff_id=tariff_id,
                   tariff_name=body.name, supplier=body.supplier, changes=changes, actor=user)
    db.commit()
    db.refresh(t)
    if user.is_supplier:
        email_utils.notify_admin_resubmit(body.name, body.supplier)
    return tariff_to_dict(t)


@router.delete("/tariffs/{tariff_id}", status_code=204, summary="Delete a tariff")
def delete_tariff(
    tariff_id: str,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    t = db.get(models.Tariff, tariff_id)
    if not t:
        raise HTTPException(404, "Tariff not found")
    _assert_tariff_owner(t, user)
    _add_changelog(db, action="deleted", tariff_id=tariff_id,
                   tariff_name=t.name, supplier=t.supplier, changes=[], actor=user)
    db.delete(t)
    db.commit()


@router.patch("/tariffs/{tariff_id}/status", summary="Change approval status (admin only)")
def update_tariff_status(
    tariff_id: str,
    body: TariffStatusIn,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_admin),
):
    if body.status not in _VALID_STATUSES:
        raise HTTPException(400, f"status must be one of {_VALID_STATUSES}")
    t = db.get(models.Tariff, tariff_id)
    if not t:
        raise HTTPException(404, "Tariff not found")
    old = t.status
    tariff_name = t.name
    supplier    = t.supplier
    t.status = body.status
    t.rejection_reason = body.reason if body.status == "rejected" else None
    t.updatedAt = _now()
    _add_changelog(db, action="updated", tariff_id=tariff_id,
                   tariff_name=tariff_name, supplier=supplier,
                   changes=[{"field": "status", "from": old, "to": body.status}], actor=user)
    db.commit()
    emails = _supplier_emails(db, supplier)
    if body.status == "approved":
        email_utils.notify_supplier_approved(emails, tariff_name, supplier)
    elif body.status == "rejected":
        email_utils.notify_supplier_rejected(emails, tariff_name, supplier, body.reason or "")
    return {"id": tariff_id, "status": t.status}


# ── Suppliers (admin only) ────────────────────────────────────────────────────

@router.get("/suppliers", summary="List all suppliers (admin only)")
def list_suppliers(db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    return [supplier_to_dict(s) for s in db.query(models.Supplier).all()]


@router.post("/suppliers", status_code=201, summary="Create a supplier (admin only)")
def create_supplier(body: SupplierIn, db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    if db.query(models.Supplier).filter(models.Supplier.name == body.name).first():
        raise HTTPException(409, f"Supplier '{body.name}' already exists")
    db.add(models.Supplier(**body.model_dump()))
    db.commit()
    return body.model_dump()


@router.put("/suppliers/{name}", summary="Update a supplier (admin only)")
def update_supplier(name: str, body: SupplierIn, db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    s = db.query(models.Supplier).filter(models.Supplier.name == name).first()
    if not s:
        raise HTTPException(404, "Supplier not found")
    if body.name != name:
        # Tariff.supplier and Message.target_suppliers are still plain strings
        # (no FK — see migrate_supplier_fk.sql for why User/MessageRead don't
        # need this treatment anymore), so a rename must still cascade to them
        # or those records silently stop resolving to this supplier.
        db.query(models.Tariff).filter(models.Tariff.supplier == name).update({"supplier": body.name})
        for msg in db.query(models.Message).filter(models.Message.audience == "selected").all():
            targets = json.loads(msg.target_suppliers or "[]")
            if name in targets:
                msg.target_suppliers = json.dumps([body.name if t == name else t for t in targets])
        for sched in db.query(models.ScheduledNotification).filter(models.ScheduledNotification.audience == "selected").all():
            targets = json.loads(sched.target_suppliers or "[]")
            if name in targets:
                sched.target_suppliers = json.dumps([body.name if t == name else t for t in targets])
        # models.Changelog.supplier is intentionally left untouched — it's an append-only
        # audit trail and should keep recording the supplier name as it was at the time
        # of each historical entry, not be rewritten to match the current name.
    for k, v in body.model_dump().items():
        setattr(s, k, v)
    db.commit()
    return body.model_dump()


@router.delete("/suppliers/{name}", status_code=204, summary="Delete a supplier (admin only)")
def delete_supplier(name: str, db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    if db.query(models.Tariff).filter(models.Tariff.supplier == name).count():
        raise HTTPException(400, "Remove all tariffs for this supplier first")
    s = db.query(models.Supplier).filter(models.Supplier.name == name).first()
    if not s:
        raise HTTPException(404, "Supplier not found")
    db.delete(s)
    db.commit()


# ── Tariff documents ──────────────────────────────────────────────────────────

_UPLOAD_DIR = Path(__file__).parent.parent / "uploads"
_MAX_FILE_BYTES = 10 * 1024 * 1024  # 10 MB


@router.post("/tariffs/{tariff_id}/documents", status_code=201, summary="Upload a supporting document for a tariff")
async def upload_document(
    tariff_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    t = db.query(models.Tariff).filter(models.Tariff.id == tariff_id).first()
    if not t:
        raise HTTPException(404, "Tariff not found.")
    if user.role == "supplier" and t.supplier != user.supplier_name:
        raise HTTPException(403, "You can only upload documents for your own tariffs.")
    original = (file.filename or "document").strip()
    if not original.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are accepted.")
    content = await file.read()
    if len(content) > _MAX_FILE_BYTES:
        raise HTTPException(400, "File exceeds the 10 MB limit.")
    if not content.startswith(b"%PDF"):
        raise HTTPException(400, "File does not appear to be a valid PDF.")
    stored = uuid.uuid4().hex + ".pdf"
    (_UPLOAD_DIR / stored).write_bytes(content)
    now = datetime.now(timezone.utc).isoformat()
    doc = models.TariffDocument(
        tariff_id=tariff_id,
        original_name=original,
        stored_name=stored,
        uploaded_at=now,
        uploaded_by=user.email,
    )
    db.add(doc)
    # Supplier uploading a new doc on a live/rejected tariff → back to pending review
    resubmitted = False
    if user.role == "supplier" and t.status in ("approved", "rejected"):
        t.status = "pending"
        t.rejection_reason = None
        resubmitted = True
    db.commit()
    db.refresh(doc)
    return {"id": doc.id, "original_name": original, "uploaded_at": now, "uploaded_by": user.email, "resubmitted": resubmitted, "new_status": t.status}


@router.get("/tariffs/{tariff_id}/documents", summary="List documents for a tariff")
def list_documents(
    tariff_id: str,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    t = db.query(models.Tariff).filter(models.Tariff.id == tariff_id).first()
    if not t:
        raise HTTPException(404, "Tariff not found.")
    if user.role == "supplier" and t.supplier != user.supplier_name:
        raise HTTPException(403, "Access denied.")
    docs = (
        db.query(models.TariffDocument)
        .filter(models.TariffDocument.tariff_id == tariff_id)
        .order_by(models.TariffDocument.uploaded_at.desc())
        .all()
    )
    return [
        {"id": d.id, "original_name": d.original_name, "uploaded_at": d.uploaded_at, "uploaded_by": d.uploaded_by}
        for d in docs
    ]


@router.get("/documents/{doc_id}/download", summary="Download a tariff document")
def download_document(
    doc_id: int,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    doc = db.get(models.TariffDocument, doc_id)
    if not doc:
        raise HTTPException(404, "Document not found.")
    if user.role == "supplier":
        t = db.query(models.Tariff).filter(models.Tariff.id == doc.tariff_id).first()
        if not t or t.supplier != user.supplier_name:
            raise HTTPException(403, "Access denied.")
    file_path = _UPLOAD_DIR / doc.stored_name
    if not file_path.exists():
        raise HTTPException(404, "File not found on server.")
    return FileResponse(
        path=str(file_path),
        filename=doc.original_name,
        media_type="application/pdf",
    )


# ── User management (admin only) ──────────────────────────────────────────────

_BASE_URL = os.getenv("TARIFF_BASE_URL", "http://localhost:8000").rstrip("/")


@router.get("/users", summary="List all portal users")
def list_users(db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc)
    return [
        {
            "id": u.id,
            "email": u.email,
            "role": u.role,
            "supplier_name": resolve_supplier_name(db, u),
            "is_active": u.is_active,
            "is_locked": bool(u.locked_until and datetime.fromisoformat(u.locked_until) > now),
            "otp_enabled": u.otp_enabled if u.otp_enabled is not None else True,
        }
        for u in db.query(models.User).order_by(models.User.id).all()
    ]


@router.post("/users", status_code=201, summary="Create supplier user and send invite email")
def create_user(body: CreateUserIn, db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    email = body.email.strip().lower()
    if not email:
        raise HTTPException(400, "Email is required.")
    if db.query(models.User).filter(models.User.email == email).first():
        raise HTTPException(409, f"A user with email '{email}' already exists.")
    supplier = db.query(models.Supplier).filter(models.Supplier.name == body.supplier_name).first()
    if not supplier:
        raise HTTPException(404, f"Supplier '{body.supplier_name}' not found.")
    new_user = models.User(
        email=email,
        password_hash=hash_password(secrets.token_urlsafe(32)),
        role="supplier",
        supplier_id=supplier.id,
        is_active=True,
    )
    db.add(new_user)
    db.flush()
    token = secrets.token_urlsafe(32)
    expires = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()
    db.query(models.PasswordReset).filter(models.PasswordReset.email == email).delete()
    db.add(models.PasswordReset(token=token, email=email, expires_at=expires))
    db.commit()
    invite_url = f"{_BASE_URL}/reset-password.html?token={token}&portal=supplier&setup=1"
    email_utils.notify_supplier_invite(email, body.supplier_name, invite_url)
    return {"id": new_user.id, "email": email, "supplier_name": body.supplier_name, "invite_url": invite_url}


@router.patch("/users/{user_id}/status", summary="Activate or deactivate a portal user")
def set_user_status(user_id: int, body: UserStatusIn, db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    target = db.get(models.User, user_id)
    if not target:
        raise HTTPException(404, "User not found.")
    if target.id == user.id:
        raise HTTPException(400, "You cannot deactivate your own account.")
    target.is_active = body.is_active
    # Reactivating an account also clears any lockout so the user can log in immediately
    if body.is_active:
        target.failed_attempts = 0
        target.locked_until = None
    db.commit()
    return {"id": target.id, "is_active": target.is_active}


@router.patch("/users/{user_id}/otp", summary="Enable or disable OTP 2FA for a user")
def set_user_otp(user_id: int, body: UserOtpToggleIn, db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    target = db.get(models.User, user_id)
    if not target:
        raise HTTPException(404, "User not found.")
    target.otp_enabled = body.otp_enabled
    db.commit()
    return {"id": target.id, "otp_enabled": target.otp_enabled}


@router.post("/users/{user_id}/unlock", summary="Clear account lockout immediately")
def unlock_user(user_id: int, db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    target = db.get(models.User, user_id)
    if not target:
        raise HTTPException(404, "User not found.")
    target.failed_attempts = 0
    target.locked_until = None
    db.commit()
    return {"id": target.id, "unlocked": True}


@router.post("/users/{user_id}/reinvite", summary="Resend invite link to a supplier user")
def reinvite_user(user_id: int, db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    target = db.get(models.User, user_id)
    if not target:
        raise HTTPException(404, "User not found.")
    if target.role != "supplier":
        raise HTTPException(400, "Invites can only be sent to supplier accounts.")
    token = secrets.token_urlsafe(32)
    expires = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()
    db.query(models.PasswordReset).filter(models.PasswordReset.email == target.email).delete()
    db.add(models.PasswordReset(token=token, email=target.email, expires_at=expires))
    db.commit()
    invite_url = f"{_BASE_URL}/reset-password.html?token={token}&portal=supplier&setup=1"
    email_utils.notify_supplier_invite(target.email, resolve_supplier_name(db, target) or "", invite_url)
    return {"ok": True, "invite_url": invite_url}


@router.delete("/users/{user_id}", status_code=204, summary="Delete a supplier user account")
def delete_user(user_id: int, db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    target = db.get(models.User, user_id)
    if not target:
        raise HTTPException(404, "User not found.")
    if target.role == "admin":
        raise HTTPException(400, "Admin accounts cannot be deleted.")
    if target.id == user.id:
        raise HTTPException(400, "You cannot delete your own account.")
    db.query(models.PasswordReset).filter(models.PasswordReset.email == target.email).delete()
    db.delete(target)
    db.commit()


@router.get("/login-activity", summary="List recent login attempts (successful and failed)")
def list_login_activity(
    limit: int = 200,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_admin),
):
    limit = max(1, min(limit, 1000))
    rows = (
        db.query(models.LoginActivity)
        .order_by(models.LoginActivity.id.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "id": r.id,
            "email": r.email,
            "user_id": r.user_id,
            "success": r.success,
            "reason": r.reason,
            "ip_address": r.ip_address,
            "user_agent": r.user_agent,
            "ts": r.ts,
        }
        for r in rows
    ]


# ── Messages (broadcast communications to suppliers) ──────────────────────────

def _message_targets(db: Session, msg: models.Message) -> list[str]:
    """Resolve which supplier names a message applies to."""
    if msg.audience == "all":
        return [s.name for s in db.query(models.Supplier).all()]
    return json.loads(msg.target_suppliers) if msg.target_suppliers else []


@router.get("/messages", summary="List messages — full history for admins, own messages for suppliers")
def list_messages(db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    messages = db.query(models.Message).order_by(models.Message.created_at.desc()).all()

    if user.is_admin:
        sid_to_name = {s.id: s.name for s in db.query(models.Supplier).all()}
        out = []
        for m in messages:
            targets = _message_targets(db, m)
            reads = db.query(models.MessageRead).filter(models.MessageRead.message_id == m.id).all()
            # Keyed by the supplier's *current* name (resolved live via supplier_id)
            # so a rename doesn't orphan read/ack tracking for historical messages.
            reads_by_supplier = {sid_to_name[r.supplier_id]: r for r in reads if r.supplier_id in sid_to_name}
            read_by = list(reads_by_supplier.keys())
            acked_by = [s for s, r in reads_by_supplier.items() if r.acknowledged_at]
            d = message_to_dict(m)
            d["totalTargets"] = len(targets)
            d["readCount"] = len([s for s in targets if s in read_by])
            d["readBy"] = [s for s in targets if s in read_by]
            d["unreadBy"] = [s for s in targets if s not in read_by]
            d["ackCount"] = len([s for s in targets if s in acked_by])
            d["ackBy"] = [s for s in targets if s in acked_by]
            d["recipients"] = [
                {
                    "supplier": s,
                    "read": s in reads_by_supplier,
                    "readAt": reads_by_supplier[s].read_at if s in reads_by_supplier else None,
                    "acknowledged": bool(reads_by_supplier.get(s) and reads_by_supplier[s].acknowledged_at),
                    "ackAt": reads_by_supplier[s].acknowledged_at if s in reads_by_supplier else None,
                }
                for s in sorted(targets)
            ]
            out.append(d)
        return out

    # Supplier: only non-archived messages that target them, with their own read/ack flags
    supplier_name = user.supplier_name
    out = []
    for m in messages:
        if m.archived:
            continue
        targets = _message_targets(db, m)
        if supplier_name not in targets:
            continue
        rec = db.query(models.MessageRead).filter(
            models.MessageRead.message_id == m.id,
            models.MessageRead.supplier_id == user.supplier_id,
        ).first()
        d = message_to_dict(m)
        d["read"] = rec is not None
        d["acknowledged"] = bool(rec and rec.acknowledged_at)
        out.append(d)
    return out


def _validate_message_fields(subject: str, body_text: str, audience: str, target_suppliers: list[str]) -> None:
    if audience not in ("all", "selected"):
        raise HTTPException(400, "audience must be 'all' or 'selected'.")
    if not subject.strip():
        raise HTTPException(400, "Subject is required.")
    if not body_text.strip():
        raise HTTPException(400, "Message body is required.")
    if audience == "selected" and not target_suppliers:
        raise HTTPException(400, "Select at least one supplier.")


def _send_message(db: Session, *, subject: str, body_text: str, audience: str,
                   target_suppliers: list[str], created_by: str) -> models.Message:
    """Create a Message row, resolve its recipients, and email them. Shared by
    the manual compose endpoint and the recurring-schedule background loop."""
    msg = models.Message(
        id=_uid(),
        subject=subject.strip(),
        body=body_text,
        audience=audience,
        target_suppliers=json.dumps(target_suppliers if audience == "selected" else []),
        created_by=created_by,
        created_at=_now(),
    )
    db.add(msg)
    db.commit()

    targets = _message_targets(db, msg)
    target_ids = [s.id for s in db.query(models.Supplier).filter(models.Supplier.name.in_(targets)).all()]
    emails = [
        u.email for u in db.query(models.User).filter(
            models.User.role == "supplier",
            models.User.supplier_id.in_(target_ids),
            models.User.is_active == True,  # noqa: E712
        ).all()
    ]
    email_utils.notify_new_message(emails, msg.subject)
    return msg


@router.post("/messages", status_code=201, summary="Compose and send a message to suppliers (admin only)")
def create_message(body: MessageIn, db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    _validate_message_fields(body.subject, body.body, body.audience, body.target_suppliers)
    msg = _send_message(
        db, subject=body.subject, body_text=body.body, audience=body.audience,
        target_suppliers=body.target_suppliers, created_by=user.email,
    )

    return message_to_dict(msg)


@router.post("/messages/{message_id}/read", summary="Mark a message as read (supplier only)")
def mark_message_read(message_id: str, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    if not user.is_supplier:
        raise HTTPException(400, "Only supplier accounts can mark messages as read.")
    msg = db.get(models.Message, message_id)
    if not msg:
        raise HTTPException(404, "Message not found.")
    existing = db.query(models.MessageRead).filter(
        models.MessageRead.message_id == message_id,
        models.MessageRead.supplier_id == user.supplier_id,
    ).first()
    if not existing:
        db.add(models.MessageRead(message_id=message_id, supplier_id=user.supplier_id, read_at=_now()))
        db.commit()
    return {"ok": True}


@router.post("/messages/{message_id}/ack", summary="Acknowledge a message (supplier only)")
def acknowledge_message(message_id: str, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    if not user.is_supplier:
        raise HTTPException(400, "Only supplier accounts can acknowledge messages.")
    msg = db.get(models.Message, message_id)
    if not msg:
        raise HTTPException(404, "Message not found.")
    rec = db.query(models.MessageRead).filter(
        models.MessageRead.message_id == message_id,
        models.MessageRead.supplier_id == user.supplier_id,
    ).first()
    if not rec:
        rec = models.MessageRead(message_id=message_id, supplier_id=user.supplier_id, read_at=_now())
        db.add(rec)
    if not rec.acknowledged_at:
        rec.acknowledged_at = _now()
        db.commit()
    return {"ok": True}


@router.patch("/messages/{message_id}/archive", summary="Archive or restore a message (admin only)")
def archive_message(message_id: str, body: MessageArchiveIn, db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    msg = db.get(models.Message, message_id)
    if not msg:
        raise HTTPException(404, "Message not found.")
    msg.archived = body.archived
    db.commit()
    return {"id": msg.id, "archived": msg.archived}


@router.delete("/messages/{message_id}", status_code=204, summary="Retract a message (admin only)")
def delete_message(message_id: str, db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    msg = db.get(models.Message, message_id)
    if not msg:
        raise HTTPException(404, "Message not found.")
    db.query(models.MessageRead).filter(models.MessageRead.message_id == message_id).delete()
    db.delete(msg)
    db.commit()


# ── Scheduled (recurring) notifications ────────────────────────────────────────

def _add_months(date_str: str, months: int) -> str:
    """Add N months to an ISO date/datetime string, clamping the day for short months.
    Always returns a plain YYYY-MM-DD string so next_send_at stays lexicographically
    comparable to _now()[:10] regardless of how many times it's been advanced."""
    d = datetime.fromisoformat(date_str)
    total = d.month - 1 + months
    year = d.year + total // 12
    month = total % 12 + 1
    day = min(d.day, calendar.monthrange(year, month)[1])
    return d.replace(year=year, month=month, day=day).date().isoformat()


@router.get("/scheduled-notifications", summary="List recurring notification schedules (admin only)")
def list_scheduled_notifications(db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    rows = db.query(models.ScheduledNotification).order_by(models.ScheduledNotification.created_at.desc()).all()
    return [scheduled_notification_to_dict(r) for r in rows]


@router.post("/scheduled-notifications", status_code=201, summary="Create a recurring notification schedule (admin only)")
def create_scheduled_notification(body: ScheduledNotificationIn, db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    _validate_message_fields(body.subject, body.body, body.audience, body.target_suppliers)
    if body.interval_months < 1:
        raise HTTPException(400, "Interval must be at least 1 month.")
    start_date = body.start_date or _now()[:10]
    try:
        datetime.fromisoformat(start_date)
    except ValueError:
        raise HTTPException(400, "start_date must be an ISO date (YYYY-MM-DD).")

    sched = models.ScheduledNotification(
        id=_uid(),
        subject=body.subject.strip(),
        body=body.body,
        audience=body.audience,
        target_suppliers=json.dumps(body.target_suppliers if body.audience == "selected" else []),
        interval_months=body.interval_months,
        next_send_at=start_date,
        enabled=True,
        created_by=user.email,
        created_at=_now(),
    )
    db.add(sched)
    db.commit()
    return scheduled_notification_to_dict(sched)


@router.put("/scheduled-notifications/{schedule_id}", summary="Edit a recurring notification schedule (admin only)")
def update_scheduled_notification(schedule_id: str, body: ScheduledNotificationIn, db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    sched = db.get(models.ScheduledNotification, schedule_id)
    if not sched:
        raise HTTPException(404, "Schedule not found.")
    _validate_message_fields(body.subject, body.body, body.audience, body.target_suppliers)
    if body.interval_months < 1:
        raise HTTPException(400, "Interval must be at least 1 month.")
    sched.subject = body.subject.strip()
    sched.body = body.body
    sched.audience = body.audience
    sched.target_suppliers = json.dumps(body.target_suppliers if body.audience == "selected" else [])
    sched.interval_months = body.interval_months
    db.commit()
    return scheduled_notification_to_dict(sched)


@router.patch("/scheduled-notifications/{schedule_id}/enabled", summary="Pause or resume a schedule (admin only)")
def set_scheduled_notification_enabled(schedule_id: str, body: ScheduledNotificationEnabledIn, db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    sched = db.get(models.ScheduledNotification, schedule_id)
    if not sched:
        raise HTTPException(404, "Schedule not found.")
    sched.enabled = body.enabled
    db.commit()
    return {"id": sched.id, "enabled": sched.enabled}


@router.delete("/scheduled-notifications/{schedule_id}", status_code=204, summary="Delete a recurring notification schedule (admin only)")
def delete_scheduled_notification(schedule_id: str, db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    sched = db.get(models.ScheduledNotification, schedule_id)
    if not sched:
        raise HTTPException(404, "Schedule not found.")
    db.delete(sched)
    db.commit()


def run_due_scheduled_notifications(db: Session) -> None:
    """Fire every enabled schedule whose next_send_at has passed. Called periodically
    from main.py's background task — not an HTTP endpoint."""
    today = _now()[:10]
    due = db.query(models.ScheduledNotification).filter(
        models.ScheduledNotification.enabled == True,  # noqa: E712
        models.ScheduledNotification.next_send_at <= today,
    ).all()
    for sched in due:
        _send_message(
            db, subject=sched.subject, body_text=sched.body, audience=sched.audience,
            target_suppliers=json.loads(sched.target_suppliers) if sched.target_suppliers else [],
            created_by=sched.created_by,
        )
        sched.last_sent_at = _now()
        # Advance past today even if the server was down for multiple cycles —
        # sends once on catch-up rather than firing repeatedly in a burst.
        next_at = sched.next_send_at
        while next_at <= today:
            next_at = _add_months(next_at, sched.interval_months)
        sched.next_send_at = next_at
        db.commit()


# ── Profiles (admin only) ─────────────────────────────────────────────────────

@router.get("/profiles", summary="List all profiles")
def list_profiles(db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    return [profile_to_dict(p) for p in db.query(models.Profile).all()]


@router.post("/profiles", status_code=201, summary="Create a profile (admin only)")
def create_profile(body: ProfileIn, db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    pid = body.id or _uid()
    p = models.Profile(id=pid, name=body.name, desc=body.desc,
                       months=json.dumps(body.months),
                       covW=body.covW, covNW=body.covNW, rows=body.rows, colCount=body.colCount)
    db.add(p)
    db.commit()
    db.refresh(p)
    return profile_to_dict(p)


@router.put("/profiles/{profile_id}", summary="Replace a profile in place (admin only)")
def update_profile(profile_id: str, body: ProfileIn, db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    p = db.get(models.Profile, profile_id)
    if not p:
        raise HTTPException(404, "Profile not found")
    p.name = body.name
    p.desc = body.desc
    p.months = json.dumps(body.months)
    p.covW = body.covW
    p.covNW = body.covNW
    p.rows = body.rows
    p.colCount = body.colCount
    db.commit()
    db.refresh(p)
    return profile_to_dict(p)


@router.delete("/profiles/{profile_id}", status_code=204, summary="Delete a profile (admin only)")
def delete_profile(profile_id: str, db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    if db.query(models.Tariff).filter(models.Tariff.profileId == profile_id).count():
        raise HTTPException(400, "Unassign this profile from all tariffs first")
    p = db.get(models.Profile, profile_id)
    if not p:
        raise HTTPException(404, "Profile not found")
    db.delete(p)
    db.commit()


# ── Regulated (admin only) ────────────────────────────────────────────────────

@router.get("/regulated", summary="Get regulated charge settings")
def get_regulated(db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    return _regulated_to_dict(db.query(models.Regulated).first())


_GRID_FIELDS = {"lv", "mv", "hv"}
_FPA_FIELDS = {"fpaLV", "fpaMV", "fpaHV"}
_UNIVERSAL_FIELDS = {"pso", "res"}


@router.put("/regulated", summary="Update regulated charges (admin only)")
def update_regulated(body: RegulatedIn, db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    old = db.query(models.Regulated).first()
    new_vals = body.model_dump()

    changes = []
    grid_changed = fpa_changed = universal_changed = False
    for field, label in _REGULATED_LABELS.items():
        old_val = float(getattr(old, field) or 0) if old else 0.0
        new_val = float(new_vals.get(field) or 0)
        if round(old_val, 8) != round(new_val, 8):
            changes.append({"field": label, "from": _fmt_rate(old_val), "to": _fmt_rate(new_val)})
            if field in _GRID_FIELDS:
                grid_changed = True
            elif field in _FPA_FIELDS:
                fpa_changed = True
            elif field in _UNIVERSAL_FIELDS:
                universal_changed = True

    # One combined form/button saves everything, but each charge type only
    # actually changes when an admin edits it — so only touch the timestamp
    # for the group(s) whose values actually changed, not every group just
    # because the form was submitted (a same-value resave should be a no-op).
    now_iso = datetime.now(timezone.utc).isoformat()
    grid_updated_at = now_iso if grid_changed else (old.grid_updated_at if old else None)
    fpa_updated_at = now_iso if fpa_changed else (old.fpa_updated_at if old else None)
    universal_updated_at = now_iso if universal_changed else (old.universal_updated_at if old else None)
    updated_at = max(t for t in (grid_updated_at, universal_updated_at) if t) if (grid_updated_at or universal_updated_at) else None

    db.merge(models.Regulated(
        id=1, **new_vals,
        updated_at=updated_at, fpa_updated_at=fpa_updated_at,
        grid_updated_at=grid_updated_at, universal_updated_at=universal_updated_at,
    ))
    if changes:
        db.add(models.RegulatedHistory(recorded_at=now_iso, **new_vals))
    db.commit()

    if changes:
        _add_changelog(db, action="updated", tariff_id="regulated",
                       tariff_name="Regulated Charges", supplier="CERA", changes=changes, actor=user)
        db.commit()

    return _regulated_to_dict(db.query(models.Regulated).first())


@router.get("/regulated/history", summary="Full history of regulated-charges snapshots, newest first")
def get_regulated_history(db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    rows = db.query(models.RegulatedHistory).order_by(models.RegulatedHistory.recorded_at.desc()).all()
    return [
        {
            "id": r.id, "recordedAt": r.recorded_at,
            "lv": r.lv, "mv": r.mv, "hv": r.hv,
            "fpaLV": r.fpaLV, "fpaMV": r.fpaMV, "fpaHV": r.fpaHV,
            "pso": r.pso, "res": r.res, "mdm": r.mdm,
        }
        for r in rows
    ]


# ── Notices (admin only) ──────────────────────────────────────────────────────

@router.get("/notices", summary="Get notices / assumptions HTML")
def get_notices(db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    return _notices_to_dict(db.query(models.Notices).first())


@router.put("/notices", summary="Update notices (admin only)")
def update_notices(body: NoticesIn, db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    db.merge(models.Notices(id=1, **body.model_dump()))
    db.commit()
    return body.model_dump()


# ── DAM data (admin only) ─────────────────────────────────────────────────────

@router.get("/dam", summary="Get stored DAM price data")
def get_dam(db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    return _dam_to_dict(db.query(models.DamData).first())


@router.put("/dam", summary="Replace DAM price data (admin only)")
def update_dam(body: DamIn, db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    db.merge(models.DamData(id=1,
        damMonthly=json.dumps(body.damMonthly), damBySlot=json.dumps(body.damBySlot),
        damDailyData=json.dumps(body.damDailyData),
        damRowCount=body.damRowCount, damYear=body.damYear))
    db.commit()
    return {"ok": True, "damYear": body.damYear, "damRowCount": body.damRowCount}


# ── Changelog ─────────────────────────────────────────────────────────────────

@router.get("/changelog", summary="Full changelog for admins, own-supplier changelog for suppliers")
def get_changelog(db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    q = db.query(models.Changelog)
    if user.is_supplier:
        q = q.filter(models.Changelog.supplier == user.supplier_name)
    return [
        {"id": c.id, "tariffId": c.tariffId, "tariffName": c.tariffName,
         "supplier": c.supplier, "action": c.action,
         "changes": json.loads(c.changes) if c.changes else [], "ts": c.ts,
         "actorRole": c.actorRole, "actorEmail": c.actorEmail}
        for c in q.order_by(models.Changelog.ts.desc()).all()
    ]
