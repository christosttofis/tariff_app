"""
Helpers shared by the admin and supplier routers.

The two routers are split by role (see routers/admin.py and routers/supplier.py)
so each can enforce its role once at the router level. The underlying tariff,
document and message logic lives here so it isn't duplicated between them.
"""

import json
import secrets
import string
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastapi import HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

import models
from auth import CurrentUser
from schemas import TariffIn


def _uid() -> str:
    # Timestamp keeps IDs roughly sortable; the random part comes from the OS
    # CSPRNG (secrets) so IDs aren't predictable from the time of creation.
    ts = int(time.time() * 1000)
    alphabet = string.ascii_lowercase + string.digits
    rand = "".join(secrets.choice(alphabet) for _ in range(8))
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


# ── Tariffs ───────────────────────────────────────────────────────────────────

def _discounts(body: TariffIn) -> list[dict]:
    return [d.model_dump() for d in body.discounts]


def _new_tariff(body: TariffIn, *, status: str) -> models.Tariff:
    now = _now()
    return models.Tariff(
        id=body.id or _uid(), name=body.name, supplier=body.supplier,
        contract=body.contract, voltage=body.voltage, pricing=body.pricing,
        standing=body.standing, mdm=body.mdm, mdmSource=body.mdmSource,
        mdmInvoiceMonths=body.mdmInvoiceMonths, rates=json.dumps(body.rates),
        profileId=body.profileId, fpaSource=body.fpaSource, fpaCustom=body.fpaCustom,
        durationMonths=body.durationMonths, loadEntitlement=body.loadEntitlement,
        discounts=json.dumps(_discounts(body)), vulnerable=body.vulnerable,
        status=status,
        createdAt=now, updatedAt=now,
    )


def _apply_tariff_body(t: models.Tariff, body: TariffIn) -> None:
    t.name = body.name; t.supplier = body.supplier
    t.contract = body.contract; t.voltage = body.voltage; t.pricing = body.pricing
    t.standing = body.standing; t.mdm = body.mdm; t.mdmSource = body.mdmSource
    t.mdmInvoiceMonths = body.mdmInvoiceMonths; t.rates = json.dumps(body.rates)
    t.profileId = body.profileId; t.fpaSource = body.fpaSource; t.fpaCustom = body.fpaCustom
    t.durationMonths = body.durationMonths; t.loadEntitlement = body.loadEntitlement
    t.discounts = json.dumps(_discounts(body)); t.vulnerable = body.vulnerable
    t.updatedAt = _now()


def _assert_profile_exists(db: Session, body: TariffIn) -> None:
    if body.profileId and not db.get(models.Profile, body.profileId):
        raise HTTPException(422, f"Unknown profile '{body.profileId}'")


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
        ("mdm",             old.mdm,             body.mdm),
        ("mdmSource",       old.mdmSource,       body.mdmSource),
        ("mdmInvoiceMonths", old.mdmInvoiceMonths, body.mdmInvoiceMonths),
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
    if old_disc != _discounts(body):
        changes.append({"field": "discounts",
                        "from": json.dumps(old_disc),
                        "to":   json.dumps(_discounts(body))})
    return changes


# ── Tariff documents ──────────────────────────────────────────────────────────

_UPLOAD_DIR = Path(__file__).parent.parent / "uploads"
_MAX_FILE_BYTES = 10 * 1024 * 1024  # 10 MB


async def _save_pdf_upload(db: Session, tariff_id: str, file: UploadFile, user: CurrentUser) -> models.TariffDocument:
    """Validate and store an uploaded PDF and add its TariffDocument row (not yet committed)."""
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
    doc = models.TariffDocument(
        tariff_id=tariff_id,
        original_name=original,
        stored_name=stored,
        uploaded_at=_now(),
        uploaded_by=user.email,
    )
    db.add(doc)
    return doc


def _document_dicts(db: Session, tariff_id: str) -> list[dict]:
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


def _document_response(doc: models.TariffDocument) -> FileResponse:
    file_path = _UPLOAD_DIR / doc.stored_name
    if not file_path.exists():
        raise HTTPException(404, "File not found on server.")
    return FileResponse(
        path=str(file_path),
        filename=doc.original_name,
        media_type="application/pdf",
    )


# ── Messages ──────────────────────────────────────────────────────────────────

def _message_targets(db: Session, msg: models.Message) -> list[str]:
    """Resolve which supplier names a message applies to."""
    if msg.audience == "all":
        return [s.name for s in db.query(models.Supplier).all()]
    return json.loads(msg.target_suppliers) if msg.target_suppliers else []
