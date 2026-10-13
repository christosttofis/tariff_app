"""
Admin API router — CERA admin only.

Auth rules
----------
  Every route here requires the admin role, enforced once by the router-level
  require_admin dependency below. A route added later is therefore admin-only
  by default, even if it forgets its own guard.

  Supplier-portal endpoints live in routers/supplier.py (/api/supplier/...),
  never here. Shared tariff/document/message logic is in routers/shared.py.
"""

import calendar
import json
import secrets
from datetime import datetime, timedelta, timezone

import dam_data
import email_utils

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy.orm import Session

import models
from auth import CurrentUser, hash_password, require_admin, resolve_supplier_name
from config import TARIFF_BASE_URL
from database import get_db
from schemas import (
    CreateUserIn, DamIn, MessageArchiveIn, MessageIn, NoticesIn, ProfileIn, RegulatedIn,
    SampleInvoiceConfigIn, ScheduledNotificationEnabledIn, ScheduledNotificationIn, SupplierIn, TariffIn,
    TariffReportStatusIn, TariffStatusIn, UserOtpToggleIn, UserStatusIn,
)
from serializers import (
    message_to_dict, profile_to_dict, scheduled_notification_to_dict,
    supplier_to_dict, tariff_report_to_dict, tariff_to_dict,
)

from routers.shared import (
    _add_changelog, _apply_tariff_body, _assert_profile_exists, _diff_fields, _document_dicts, _document_response,
    _message_targets, _new_tariff, _now, _save_pdf_upload, _uid,
)

router = APIRouter(prefix="/api/admin", tags=["admin"], dependencies=[Depends(require_admin)])

_VALID_STATUSES = {"draft", "pending", "approved", "rejected", "suspended", "archived"}


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


# ── Bulk config ───────────────────────────────────────────────────────────────

@router.get("/config", summary="Full config for admin — all tariff statuses")
def get_admin_config(
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_admin),
):
    suppliers = db.query(models.Supplier).all()
    profiles  = db.query(models.Profile).all()
    tariffs   = db.query(models.Tariff).all()
    regulated = db.query(models.Regulated).first()
    dam       = db.query(models.DamData).first()
    notices   = db.query(models.Notices).first()
    sample_invoice_cfg = db.query(models.SampleInvoiceConfig).first()
    changelog = db.query(models.Changelog).order_by(models.Changelog.ts.desc()).all()
    reports   = db.query(models.TariffReport).order_by(models.TariffReport.createdAt.desc()).all()

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
        "sampleInvoiceEnabled": bool(sample_invoice_cfg.enabled) if sample_invoice_cfg else False,
        **_dam_to_dict(dam),
        "changelog": [
            {"id": c.id, "tariffId": c.tariffId, "tariffName": c.tariffName,
             "supplier": c.supplier, "action": c.action,
             "changes": json.loads(c.changes) if c.changes else [], "ts": c.ts,
             "actorRole": c.actorRole, "actorEmail": c.actorEmail}
            for c in changelog
        ],
        "docTariffIds": doc_tariff_ids,
        "reports": [tariff_report_to_dict(r) for r in reports],
        "savedAt": _now(),
    }


# ── Tariffs ───────────────────────────────────────────────────────────────────

@router.get("/tariffs", summary="List tariffs")
def list_tariffs(
    status: str | None = None,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_admin),
):
    q = db.query(models.Tariff)
    if status:
        if status not in _VALID_STATUSES:
            raise HTTPException(400, f"status must be one of {_VALID_STATUSES}")
        q = q.filter(models.Tariff.status == status)
    return [tariff_to_dict(t) for t in q.all()]


@router.post("/tariffs", status_code=201, summary="Create a tariff")
def create_tariff(
    body: TariffIn,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_admin),
):
    _assert_profile_exists(db, body)
    t = _new_tariff(body, status="approved")
    db.add(t)
    _add_changelog(db, action="created", tariff_id=t.id,
                   tariff_name=body.name, supplier=body.supplier, changes=[], actor=user)
    db.commit()
    db.refresh(t)
    return tariff_to_dict(t)


@router.get("/tariffs/{tariff_id}", summary="Get a single tariff")
def get_tariff(
    tariff_id: str,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_admin),
):
    t = db.get(models.Tariff, tariff_id)
    if not t:
        raise HTTPException(404, "Tariff not found")
    return tariff_to_dict(t)


@router.put("/tariffs/{tariff_id}", summary="Replace a tariff")
def update_tariff(
    tariff_id: str,
    body: TariffIn,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_admin),
):
    t = db.get(models.Tariff, tariff_id)
    if not t:
        raise HTTPException(404, "Tariff not found")
    _assert_profile_exists(db, body)
    changes = _diff_fields(db, t, body)   # capture diff before modifying t
    _apply_tariff_body(t, body)
    _add_changelog(db, action="updated", tariff_id=tariff_id,
                   tariff_name=body.name, supplier=body.supplier, changes=changes, actor=user)
    db.commit()
    db.refresh(t)
    return tariff_to_dict(t)


@router.delete("/tariffs/{tariff_id}", status_code=204, summary="Delete a tariff")
def delete_tariff(
    tariff_id: str,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_admin),
):
    t = db.get(models.Tariff, tariff_id)
    if not t:
        raise HTTPException(404, "Tariff not found")
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
    if bool(s.regulated) != bool(body.regulated):
        # Flipping this flag changes how MDM is calculated for every tariff under
        # this supplier (see onEditSupplierChange in admin.html), so it's worth its
        # own audit trail entry distinct from the rest of the supplier's fields —
        # separate from the two confirmation steps the admin UI already requires.
        _add_changelog(
            db, action="updated", tariff_id=None, tariff_name="Supplier settings",
            supplier=body.name,
            changes=[{"field": "regulated", "from": "yes" if s.regulated else "no",
                      "to": "yes" if body.regulated else "no"}],
            actor=user,
        )
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
    # users.supplier_id is a real FK — deleting the supplier while a login is
    # still attached to it violates the constraint and surfaces as a raw 500,
    # so check (and give a clear reason) up front instead.
    if db.query(models.User).filter(models.User.supplier_id == s.id).count():
        raise HTTPException(400, "Remove all user accounts for this supplier first")
    db.delete(s)
    db.commit()


# ── Tariff documents ──────────────────────────────────────────────────────────

@router.post("/tariffs/{tariff_id}/documents", status_code=201, summary="Upload a supporting document for a tariff")
async def upload_document(
    tariff_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_admin),
):
    t = db.query(models.Tariff).filter(models.Tariff.id == tariff_id).first()
    if not t:
        raise HTTPException(404, "Tariff not found.")
    doc = await _save_pdf_upload(db, tariff_id, file, user)
    db.commit()
    db.refresh(doc)
    return {"id": doc.id, "original_name": doc.original_name, "uploaded_at": doc.uploaded_at, "uploaded_by": user.email, "resubmitted": False, "new_status": t.status}


@router.get("/tariffs/{tariff_id}/documents", summary="List documents for a tariff")
def list_documents(
    tariff_id: str,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_admin),
):
    t = db.query(models.Tariff).filter(models.Tariff.id == tariff_id).first()
    if not t:
        raise HTTPException(404, "Tariff not found.")
    return _document_dicts(db, tariff_id)


@router.get("/documents/{doc_id}/download", summary="Download a tariff document")
def download_document(
    doc_id: int,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_admin),
):
    doc = db.get(models.TariffDocument, doc_id)
    if not doc:
        raise HTTPException(404, "Document not found.")
    return _document_response(doc)


# ── User management (admin only) ──────────────────────────────────────────────

_BASE_URL = TARIFF_BASE_URL


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
    old_value = target.otp_enabled if target.otp_enabled is not None else True
    target.otp_enabled = body.otp_enabled
    if old_value != body.otp_enabled:
        _add_changelog(
            db, action="updated", tariff_id=f"user:{target.id}", tariff_name=target.email,
            supplier=resolve_supplier_name(db, target) or "CERA",
            changes=[{"field": "otp_enabled", "from": old_value, "to": body.otp_enabled}],
            actor=user,
        )
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
    # login_activity.user_id / password_history.user_id are real FKs to users.id
    # with no cascade, so deleting the user while either still points at it
    # raises an IntegrityError (surfaces as a raw 500). Login activity is an
    # audit trail — keep the rows (email/ip/timestamp still identify them) and
    # just detach the FK; password history has no purpose once the account is
    # gone, so it's fine to drop.
    db.query(models.LoginActivity).filter(models.LoginActivity.user_id == target.id).update({"user_id": None})
    db.query(models.PasswordHistory).filter(models.PasswordHistory.user_id == target.id).delete()
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

@router.get("/messages", summary="List messages — full history with per-supplier read/ack status")
def list_messages(db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    messages = db.query(models.Message).order_by(models.Message.created_at.desc()).all()
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

@router.get("/profiles", summary="List all profiles, with full half-hourly shape data")
def list_profiles(db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    return [profile_to_dict(p) for p in db.query(models.Profile).all()]


def _profile_months_json(body: ProfileIn) -> str:
    # Same stored shape as before ({W, NW, hasW, hasNW} x 12), now validated by ProfileMonthIn.
    return json.dumps([m.model_dump() for m in body.months])


@router.post("/profiles", status_code=201, summary="Create a profile (admin only)")
def create_profile(body: ProfileIn, db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    pid = body.id or _uid()
    p = models.Profile(id=pid, name=body.name, desc=body.desc,
                       months=_profile_months_json(body),
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
    p.months = _profile_months_json(body)
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

@router.get("/regulated", summary="Get regulated charge settings (admin only)")
def get_regulated(db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    return _regulated_to_dict(db.query(models.Regulated).first())


_GRID_FIELDS = {"lv", "mv", "hv"}
_FPA_FIELDS = {"fpaLV", "fpaMV", "fpaHV"}
_UNIVERSAL_FIELDS = {"pso", "res", "mdm"}  # MDM applies to all voltage levels, like PSO/RES


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


@router.get("/regulated/history", summary="Full history of regulated-charges snapshots, newest first (admin only)")
def get_regulated_history(db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
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
def get_notices(db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    return _notices_to_dict(db.query(models.Notices).first())


@router.put("/notices", summary="Update notices (admin only)")
def update_notices(body: NoticesIn, db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    db.merge(models.Notices(id=1, **body.model_dump()))
    db.commit()
    return body.model_dump()


# ── Sample invoice toggle (admin only) ────────────────────────────────────────

@router.get("/sample-invoice", summary="Get sample invoice feature toggle")
def get_sample_invoice_config(db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    row = db.query(models.SampleInvoiceConfig).first()
    return {"enabled": bool(row.enabled) if row else False}


@router.put("/sample-invoice", summary="Update sample invoice feature toggle (admin only)")
def update_sample_invoice_config(body: SampleInvoiceConfigIn, db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    db.merge(models.SampleInvoiceConfig(id=1, enabled=body.enabled))
    db.commit()
    return {"enabled": body.enabled}


# ── DAM data (admin only) ─────────────────────────────────────────────────────

@router.get("/dam", summary="Get stored DAM price data (admin only)")
def get_dam(db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    return _dam_to_dict(db.query(models.DamData).first())


@router.put("/dam", summary="Replace DAM price data (admin only)")
def update_dam(body: DamIn, db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    payload = {"damMonthly": body.damMonthly, "damBySlot": body.damBySlot, "damDailyData": body.damDailyData,
               "damRowCount": body.damRowCount, "damYear": body.damYear}
    version = _replace_dam(db, payload, source=body.source, actor=user.email,
                           action="saved_tsoc" if body.source == "tsoc" else "saved_upload")
    db.commit()
    return {"ok": True, "damYear": body.damYear, "damRowCount": body.damRowCount, "versionId": version.id}


# Data changes (save, rollback) all go through _replace_dam: the previous dataset
# stays in dam_versions and every change is written to dam_change_log.

def _version_meta(v: models.DamVersion) -> dict:
    return {"id": v.id, "createdAt": v.created_at, "createdBy": v.created_by, "source": v.source,
            "restoredFrom": v.restored_from, "firstDate": v.first_date, "lastDate": v.last_date,
            "dayCount": v.day_count, "rowCount": v.row_count}


def _new_version(db: Session, payload: dict, *, source: str, actor: str | None,
                 restored_from: int | None = None) -> models.DamVersion:
    fresh = dam_data.freshness(payload.get("damDailyData"))
    v = models.DamVersion(created_at=_now(), created_by=actor, source=source, restored_from=restored_from,
                          first_date=fresh["firstDate"], last_date=fresh["lastDate"],
                          day_count=fresh["dayCount"], row_count=payload.get("damRowCount") or 0,
                          payload=json.dumps(payload))
    db.add(v)
    db.flush()
    return v


def _ensure_initial_version(db: Session, current: models.DamData | None) -> None:
    """Back up the dataset stored before versioning existed, once, before it is first replaced."""
    if db.query(models.DamVersion.id).first() is None and current is not None:
        _new_version(db, _dam_to_dict(current), source="initial", actor=None)


def _log_dam(db: Session, action: str, actor: str | None, summary: str, details: dict | None = None,
             version_id: int | None = None) -> None:
    db.add(models.DamChangeLog(ts=_now(), actor=actor, action=action, version_id=version_id,
                               summary=summary, details=json.dumps(details or {})))


def _replace_dam(db: Session, payload: dict, *, source: str, actor: str, action: str,
                 restored_from: int | None = None) -> models.DamVersion:
    current = db.query(models.DamData).first()
    _ensure_initial_version(db, current)
    before = set(dam_data.dataset_dates(_dam_to_dict(current)["damDailyData"]))
    after = set(dam_data.dataset_dates(payload["damDailyData"]))
    db.merge(models.DamData(id=1,
        damMonthly=json.dumps(payload["damMonthly"]), damBySlot=json.dumps(payload["damBySlot"]),
        damDailyData=json.dumps(payload["damDailyData"]),
        damRowCount=payload["damRowCount"], damYear=payload["damYear"], stale_notified_at=None))
    version = _new_version(db, payload, source=source, actor=actor, restored_from=restored_from)
    added, removed = sorted(after - before), sorted(before - after)
    rng = lambda ds: f"{ds[0]} to {ds[-1]}" if ds else "none"  # noqa: E731
    summary = (f"Version {version.id}: {len(after)} days ({rng(sorted(after))}); "
               f"{len(added)} day(s) added, {len(removed)} removed")
    if restored_from:
        summary = f"Rolled back to version {restored_from}. " + summary
    _log_dam(db, action, actor, summary, {
        "daysAdded": len(added), "addedRange": rng(added), "daysRemoved": len(removed),
        "removedRange": rng(removed), "before": rng(sorted(before)), "after": rng(sorted(after)),
        "rowCount": payload["damRowCount"],
    }, version_id=version.id)
    return version


@router.get("/dam/status", summary="DAM data freshness and last change (admin only)")
def get_dam_status(db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    status = dam_data.freshness(_dam_to_dict(db.query(models.DamData).first())["damDailyData"])
    last = db.query(models.DamVersion).order_by(models.DamVersion.id.desc()).first()
    return {**status, "staleAfterDays": dam_data.STALE_AFTER_DAYS,
            "lastVersion": _version_meta(last) if last else None}


@router.get("/dam/log", summary="DAM change log, newest first (admin only)")
def get_dam_log(limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db),
                user: CurrentUser = Depends(require_admin)):
    rows = db.query(models.DamChangeLog).order_by(models.DamChangeLog.id.desc()).limit(limit).all()
    return [{"id": r.id, "ts": r.ts, "actor": r.actor, "action": r.action, "versionId": r.version_id,
             "summary": r.summary, "details": json.loads(r.details or "{}")} for r in rows]


@router.get("/dam/versions", summary="Saved DAM datasets, newest first (admin only)")
def list_dam_versions(db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    rows = db.query(models.DamVersion).order_by(models.DamVersion.id.desc()).all()
    return [_version_meta(v) for v in rows]


@router.get("/dam/versions/{version_id}", summary="One saved DAM dataset with its data (admin only)")
def get_dam_version(version_id: int, db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    v = db.get(models.DamVersion, version_id)
    if not v:
        raise HTTPException(404, "Version not found.")
    return {**_version_meta(v), "payload": json.loads(v.payload)}


@router.post("/dam/versions/{version_id}/restore", summary="Make an earlier DAM dataset live again (admin only)")
def restore_dam_version(version_id: int, db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    v = db.get(models.DamVersion, version_id)
    if not v:
        raise HTTPException(404, "Version not found.")
    new = _replace_dam(db, json.loads(v.payload), source="rollback", actor=user.email,
                       action="rollback", restored_from=v.id)
    db.commit()
    return {"ok": True, "versionId": new.id, "restoredFrom": v.id}


_DAM_STALE_REMIND_DAYS = 7


def run_dam_staleness_check(db: Session) -> None:
    """Emails the admin when the newest DAM price is more than 15 days old;
    repeats weekly while it stays old. Called daily from main.py's background loop."""
    dam = db.query(models.DamData).first()
    status = dam_data.freshness(_dam_to_dict(dam)["damDailyData"])
    if not status["stale"] or dam is None:
        return
    now = datetime.now(timezone.utc)
    if dam.stale_notified_at:
        last = datetime.fromisoformat(dam.stale_notified_at)
        if now - last < timedelta(days=_DAM_STALE_REMIND_DAYS):
            return
    if not email_utils.notify_dam_stale(status["lastDate"], status["ageDays"]):
        return   # no admin email address configured; the dashboard still shows it
    dam.stale_notified_at = now.isoformat()
    age = f"{status['ageDays']} days old" if status["lastDate"] else "no data"
    _log_dam(db, "stale_alert_sent", None, f"Reminder emailed: newest DAM price {status['lastDate'] or '—'} ({age}).")
    db.commit()



# ── Changelog ─────────────────────────────────────────────────────────────────

@router.get("/changelog", summary="Full changelog")
def get_changelog(db: Session = Depends(get_db), user: CurrentUser = Depends(require_admin)):
    q = db.query(models.Changelog)
    return [
        {"id": c.id, "tariffId": c.tariffId, "tariffName": c.tariffName,
         "supplier": c.supplier, "action": c.action,
         "changes": json.loads(c.changes) if c.changes else [], "ts": c.ts,
         "actorRole": c.actorRole, "actorEmail": c.actorEmail}
        for c in q.order_by(models.Changelog.ts.desc()).all()
    ]


# ── Tariff reports (Article 121(ζ) — customer-reported issues) ─────────────────

@router.patch("/reports/{report_id}", summary="Update a tariff report's status (admin only)")
def update_report_status(
    report_id: str,
    body: TariffReportStatusIn,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_admin),
):
    r = db.get(models.TariffReport, report_id)
    if not r:
        raise HTTPException(404, "Report not found")
    r.status = body.status
    # Only overwrite when a note was actually sent — status-only updates (e.g.
    # a plain Reopen) must not wipe out a note left on an earlier transition.
    if body.admin_note is not None:
        r.adminNote = body.admin_note
    r.resolvedAt = _now()
    r.resolvedBy = user.email
    db.commit()
    db.refresh(r)
    return tariff_report_to_dict(r)
