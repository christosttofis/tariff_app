"""
Supplier API router — supplier portal (supplier.html) only.

Auth rules
----------
  Every route here requires the supplier role, enforced once by the
  router-level require_supplier dependency below. Admins use /api/admin/...
  and get 403 here.

Scoping
-------
  Every query is limited to the caller's own supplier (user.supplier_name /
  user.supplier_id). The supplier name in a request body is never trusted:
  it must match the caller's own supplier or the request is rejected.
  Tariffs a supplier creates or edits always go (back) to "pending" review.

Deletion
--------
  A tariff that has EVER been public (Tariff.everPublished, including one
  since edited back to pending) is archived, not removed: hidden from
  customers, kept read-only in the supplier's list and the admin panel, and
  logged. Tariffs that were never public are deleted outright, also logged. Only an admin can
  permanently delete or restore an archived tariff.
"""

import email_utils

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

import models
from auth import CurrentUser, require_supplier
from database import get_db
from routers.shared import (
    _add_changelog, _apply_tariff_body, _assert_profile_exists, _diff_fields, _document_dicts, _document_response,
    _message_targets, _new_tariff, _now, _save_pdf_upload,
)
from schemas import TariffIn
from serializers import message_to_dict, profile_to_summary_dict, tariff_to_dict

router = APIRouter(prefix="/api/supplier", tags=["supplier"], dependencies=[Depends(require_supplier)])


def _own_tariff(db: Session, tariff_id: str, user: CurrentUser) -> models.Tariff:
    """Load a tariff owned by the caller's supplier. Another supplier's tariff
    gets the same 404 as a missing one, so IDs can't be probed."""
    t = db.get(models.Tariff, tariff_id)
    if not t or t.supplier != user.supplier_name:
        raise HTTPException(404, "Tariff not found")
    return t


def _assert_not_archived(t: models.Tariff) -> None:
    if t.status == "archived":
        raise HTTPException(409, "This tariff is archived and can no longer be changed")


def _assert_own_supplier_name(body: TariffIn, user: CurrentUser) -> None:
    if body.supplier != user.supplier_name:
        raise HTTPException(403, f"You can only submit tariffs for '{user.supplier_name}'")


# ── Tariffs ───────────────────────────────────────────────────────────────────

@router.get("/tariffs", summary="List own tariffs")
def list_tariffs(db: Session = Depends(get_db), user: CurrentUser = Depends(require_supplier)):
    q = db.query(models.Tariff).filter(models.Tariff.supplier == user.supplier_name)
    return [tariff_to_dict(t) for t in q.all()]


@router.post("/tariffs", status_code=201, summary="Submit a new tariff for review")
def create_tariff(body: TariffIn, db: Session = Depends(get_db), user: CurrentUser = Depends(require_supplier)):
    _assert_own_supplier_name(body, user)
    _assert_profile_exists(db, body)
    # A client-chosen id must not collide with (and silently overwrite-fail on)
    # an existing tariff, including another supplier's.
    if body.id and db.get(models.Tariff, body.id):
        raise HTTPException(409, "A tariff with this id already exists")
    t = _new_tariff(body, status="pending")
    db.add(t)
    _add_changelog(db, action="created", tariff_id=t.id,
                   tariff_name=body.name, supplier=body.supplier, changes=[], actor=user)
    db.commit()
    db.refresh(t)
    email_utils.notify_admin_new_tariff(body.name, body.supplier)
    return tariff_to_dict(t)


@router.put("/tariffs/{tariff_id}", summary="Edit own tariff (goes back to pending review)")
def update_tariff(tariff_id: str, body: TariffIn, db: Session = Depends(get_db),
                  user: CurrentUser = Depends(require_supplier)):
    t = _own_tariff(db, tariff_id, user)
    _assert_not_archived(t)
    # Without this, a supplier could reassign its own tariff to another supplier's name.
    _assert_own_supplier_name(body, user)
    _assert_profile_exists(db, body)
    changes = _diff_fields(db, t, body)   # capture diff before modifying t
    _apply_tariff_body(t, body)
    t.status = "pending"
    _add_changelog(db, action="updated", tariff_id=tariff_id,
                   tariff_name=body.name, supplier=body.supplier, changes=changes, actor=user)
    db.commit()
    db.refresh(t)
    email_utils.notify_admin_resubmit(body.name, body.supplier)
    return tariff_to_dict(t)


@router.delete("/tariffs/{tariff_id}", status_code=204,
               summary="Delete own tariff (archived instead if it has ever been public)")
def delete_tariff(tariff_id: str, db: Session = Depends(get_db), user: CurrentUser = Depends(require_supplier)):
    t = _own_tariff(db, tariff_id, user)
    _assert_not_archived(t)
    if t.everPublished or t.status in ("approved", "suspended"):
        _add_changelog(db, action="updated", tariff_id=tariff_id, tariff_name=t.name, supplier=t.supplier,
                       changes=[{"field": "status", "from": t.status, "to": "archived"}], actor=user)
        t.status = "archived"
        t.updatedAt = _now()
    else:
        _add_changelog(db, action="deleted", tariff_id=tariff_id,
                       tariff_name=t.name, supplier=t.supplier, changes=[], actor=user)
        db.delete(t)
    db.commit()


# ── Tariff documents ──────────────────────────────────────────────────────────

@router.post("/tariffs/{tariff_id}/documents", status_code=201, summary="Upload a supporting document for own tariff")
async def upload_document(
    tariff_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(require_supplier),
):
    t = _own_tariff(db, tariff_id, user)
    _assert_not_archived(t)
    doc = await _save_pdf_upload(db, tariff_id, file, user)
    # A new doc on a live/rejected tariff sends it back to pending review
    resubmitted = False
    if t.status in ("approved", "rejected"):
        old_status = t.status
        t.status = "pending"
        t.rejection_reason = None
        resubmitted = True
        _add_changelog(
            db, action="updated", tariff_id=tariff_id, tariff_name=t.name, supplier=t.supplier,
            changes=[{"field": "status", "from": old_status, "to": "pending"},
                     {"field": "documents", "from": "", "to": f"uploaded {doc.original_name}"}],
            actor=user,
        )
    db.commit()
    db.refresh(doc)
    return {"id": doc.id, "original_name": doc.original_name, "uploaded_at": doc.uploaded_at,
            "uploaded_by": user.email, "resubmitted": resubmitted, "new_status": t.status}


@router.get("/tariffs/{tariff_id}/documents", summary="List documents for own tariff")
def list_documents(tariff_id: str, db: Session = Depends(get_db), user: CurrentUser = Depends(require_supplier)):
    _own_tariff(db, tariff_id, user)
    return _document_dicts(db, tariff_id)


@router.get("/documents/{doc_id}/download", summary="Download a document of own tariff")
def download_document(doc_id: int, db: Session = Depends(get_db), user: CurrentUser = Depends(require_supplier)):
    doc = db.get(models.TariffDocument, doc_id)
    # Same 404 for "doesn't exist" and "exists but isn't yours" — a distinct
    # 403 here would let a supplier enumerate which document IDs exist.
    t = db.get(models.Tariff, doc.tariff_id) if doc else None
    if not doc or not t or t.supplier != user.supplier_name:
        raise HTTPException(404, "Document not found.")
    return _document_response(doc)


# ── Messages ──────────────────────────────────────────────────────────────────

def _own_message(db: Session, message_id: str, user: CurrentUser) -> models.Message:
    """Load a non-archived message addressed to the caller's supplier."""
    msg = db.get(models.Message, message_id)
    if not msg or msg.archived or user.supplier_name not in _message_targets(db, msg):
        raise HTTPException(404, "Message not found.")
    return msg


@router.get("/messages", summary="List messages addressed to own supplier")
def list_messages(db: Session = Depends(get_db), user: CurrentUser = Depends(require_supplier)):
    messages = db.query(models.Message).order_by(models.Message.created_at.desc()).all()
    out = []
    for m in messages:
        if m.archived or user.supplier_name not in _message_targets(db, m):
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


@router.post("/messages/{message_id}/read", summary="Mark a message as read")
def mark_message_read(message_id: str, db: Session = Depends(get_db), user: CurrentUser = Depends(require_supplier)):
    _own_message(db, message_id, user)
    existing = db.query(models.MessageRead).filter(
        models.MessageRead.message_id == message_id,
        models.MessageRead.supplier_id == user.supplier_id,
    ).first()
    if not existing:
        db.add(models.MessageRead(message_id=message_id, supplier_id=user.supplier_id, read_at=_now()))
        db.commit()
    return {"ok": True}


@router.post("/messages/{message_id}/ack", summary="Acknowledge a message")
def acknowledge_message(message_id: str, db: Session = Depends(get_db), user: CurrentUser = Depends(require_supplier)):
    _own_message(db, message_id, user)
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


# ── Profiles ──────────────────────────────────────────────────────────────────

@router.get("/profiles", summary="List profiles (id/name/desc only, for the tariff form's picker)")
def list_profiles(db: Session = Depends(get_db), user: CurrentUser = Depends(require_supplier)):
    # The full half-hourly shape data is admin-only; suppliers only need the picker fields.
    return [profile_to_summary_dict(p) for p in db.query(models.Profile).all()]
