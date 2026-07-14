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


def supplier_to_dict(s: models.Supplier) -> dict:
    return {
        "name": s.name,
        "licence": s.licence or "",
        "address": s.address or "",
        "website": s.website or "",
        "email": s.email or "",
        "tel": s.tel or "",
    }
