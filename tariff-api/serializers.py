"""
Shared serializer functions that turn ORM rows into the JSON dicts
both the public and admin endpoints return.
"""

import json

import models


def tariff_to_dict(t: models.Tariff) -> dict:
    return {
        "id": t.id,
        "name": t.name,
        "supplier": t.supplier,
        "contract": t.contract,
        "voltage": t.voltage,
        "pricing": t.pricing,
        "standing": t.standing,
        "mdm": t.mdm or 0.0,
        "mdmSource": t.mdmSource or "custom",
        "mdmInvoiceMonths": t.mdmInvoiceMonths or 2,
        "rates": json.loads(t.rates) if t.rates else {},
        "profileId": t.profileId,
        "fpaSource": t.fpaSource,
        "fpaCustom": t.fpaCustom,
        "durationMonths": t.durationMonths,
        "loadEntitlement": t.loadEntitlement,
        "discounts": json.loads(t.discounts) if t.discounts else [],
        "vulnerable": t.vulnerable,
        "status": t.status,
        "rejectionReason": t.rejection_reason,
        "createdAt": t.createdAt,
        "updatedAt": t.updatedAt,
    }


def tariff_to_public_summary_dict(t: models.Tariff) -> dict:
    """Display/filter-only fields for the public customer calculator — no
    rate/discount/profile/FPA-source data (see
    SECURITY_REMEDIATION_PLAN_customer_data_exposure.md). Pricing is computed
    server-side via POST /api/public/calculate instead."""
    return {
        "id": t.id,
        "name": t.name,
        "supplier": t.supplier,
        "contract": t.contract,
        "voltage": t.voltage,
        "pricing": t.pricing,
        "standing": t.standing,
        "vulnerable": t.vulnerable,
        "durationMonths": t.durationMonths,
        "loadEntitlement": t.loadEntitlement,
        "updatedAt": t.updatedAt,
    }


def profile_to_dict(p: models.Profile) -> dict:
    return {
        "id": p.id,
        "name": p.name,
        "desc": p.desc,
        "months": json.loads(p.months) if p.months else [],
        "covW": p.covW,
        "covNW": p.covNW,
        "rows": p.rows,
        "colCount": p.colCount,
    }


def profile_to_summary_dict(p: models.Profile) -> dict:
    """Display-only fields for the profile-picker dropdown (supplier.html) —
    no raw half-hourly shape data. Suppliers only ever render id/name/desc;
    the full months array is needed only by admin.html's profile management
    UI (coverage tables, per-month shape preview), which uses profile_to_dict
    instead."""
    return {"id": p.id, "name": p.name, "desc": p.desc}


def message_to_dict(m: models.Message) -> dict:
    return {
        "id": m.id,
        "subject": m.subject,
        "body": m.body,
        "audience": m.audience,
        "targetSuppliers": json.loads(m.target_suppliers) if m.target_suppliers else [],
        "createdBy": m.created_by,
        "createdAt": m.created_at,
        "archived": bool(m.archived),
    }


def scheduled_notification_to_dict(s: models.ScheduledNotification) -> dict:
    return {
        "id": s.id,
        "subject": s.subject,
        "body": s.body,
        "audience": s.audience,
        "targetSuppliers": json.loads(s.target_suppliers) if s.target_suppliers else [],
        "intervalMonths": s.interval_months,
        "nextSendAt": s.next_send_at,
        "enabled": bool(s.enabled),
        "createdBy": s.created_by,
        "createdAt": s.created_at,
        "lastSentAt": s.last_sent_at,
    }


def tariff_report_to_dict(r: models.TariffReport) -> dict:
    return {
        "id": r.id,
        "tariffId": r.tariffId,
        "tariffName": r.tariffName,
        "supplier": r.supplier,
        "note": r.note,
        "status": r.status,
        "adminNote": r.adminNote,
        "createdAt": r.createdAt,
        "resolvedAt": r.resolvedAt,
        "resolvedBy": r.resolvedBy,
        # ipAddress intentionally omitted — internal-only, never sent to any frontend
    }


def supplier_to_dict(s: models.Supplier) -> dict:
    return {
        "name": s.name,
        "licence": s.licence or "",
        "address": s.address or "",
        "website": s.website or "",
        "email": s.email or "",
        "tel": s.tel or "",
        "regulated": bool(s.regulated),
    }
