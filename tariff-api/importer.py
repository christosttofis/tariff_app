"""
Shared logic for importing the full localStorage cfg JSON into the database.
Used by both seed.py (CLI) and the admin "Publish" endpoint (PUT /api/admin/config).

The cfg JSON shape is produced by admin.html's saveAll() function:
  {version, suppliers, profiles, tariffs, regulated, notices,
   damMonthly, damBySlot, damDailyData, damRowCount, damYear, savedAt}

Note: the changelog (audit trail) is deliberately NOT part of this import — it's
written directly to the database by the individual create/update/delete endpoints
and must survive a bulk publish untouched, regardless of what the client sends.
"""

import json
from typing import Any

from sqlalchemy.orm import Session

import models


def import_cfg(cfg: dict[str, Any], db: Session) -> dict:
    """
    Replace all database content with the data from a cfg JSON snapshot.
    Returns a summary dict.

    Deletion order respects logical dependencies even though SQLite does not
    enforce foreign keys by default.
    """
    # Clear existing data (order matters conceptually even without FK enforcement)
    # NOTE: models.Changelog is intentionally NOT cleared/reimported here — it's an
    # append-only audit trail written directly by the individual create/update/delete
    # endpoints (_add_changelog in routers/admin.py), and must survive a bulk publish
    # regardless of what the client's in-memory snapshot happens to contain.
    db.query(models.Tariff).delete()
    db.query(models.Profile).delete()
    db.query(models.Supplier).delete()

    # ── Suppliers ──────────────────────────────────────────────────────────
    for s in cfg.get("suppliers", []):
        # Old format stored suppliers as plain strings; new format is objects
        if isinstance(s, str):
            s = {"name": s}
        db.add(models.Supplier(
            name=s.get("name", ""),
            licence=s.get("licence", ""),
            address=s.get("address", ""),
            website=s.get("website", ""),
            email=s.get("email", ""),
            tel=s.get("tel", ""),
        ))

    # ── Profiles ───────────────────────────────────────────────────────────
    for p in cfg.get("profiles", []):
        db.add(models.Profile(
            id=p["id"],
            name=p.get("name", ""),
            desc=p.get("desc", ""),
            months=json.dumps(p.get("months", [])),
            covW=p.get("covW", 0),
            covNW=p.get("covNW", 0),
            rows=p.get("rows", 0),
            colCount=p.get("colCount", 0),
        ))

    # ── Tariffs ────────────────────────────────────────────────────────────
    for t in cfg.get("tariffs", []):
        db.add(models.Tariff(
            id=t["id"],
            name=t.get("name", ""),
            supplier=t.get("supplier", ""),
            contract=t.get("contract", "Domestic"),
            voltage=t.get("voltage", "LV"),
            pricing=t.get("pricing", "Fixed"),
            standing=float(t.get("standing", 0)),
            mdm=float(t.get("mdm", 0)),
            rates=json.dumps(t.get("rates", {})),
            profileId=t.get("profileId"),
            fpaSource=t.get("fpaSource", "global"),
            fpaCustom=float(t.get("fpaCustom", 0)),
            durationMonths=t.get("durationMonths"),
            loadEntitlement=t.get("loadEntitlement"),
            discounts=json.dumps(t.get("discounts", [])),
            vulnerable=bool(t.get("vulnerable", False)),
            # localStorage cfg has no status field → default to 'approved'
            status=t.get("status", "approved"),
            createdAt=t.get("createdAt"),
            updatedAt=t.get("updatedAt"),
        ))

    # ── Regulated (single row, always id=1) ────────────────────────────────
    r = cfg.get("regulated", {})
    # Backwards compat: old cfg had a single 'fpa' field instead of fpaLV/fpaMV/fpaHV
    fpa_fallback = float(r.get("fpa", 0))
    db.merge(models.Regulated(
        id=1,
        lv=float(r.get("lv", 0)),
        mv=float(r.get("mv", 0)),
        hv=float(r.get("hv", 0)),
        fpaLV=float(r.get("fpaLV", fpa_fallback)),
        fpaMV=float(r.get("fpaMV", fpa_fallback)),
        fpaHV=float(r.get("fpaHV", fpa_fallback)),
        pso=float(r.get("pso", 0)),
        res=float(r.get("res", 0)),
        mdm=float(r.get("mdm", 0)),
    ))

    # ── DAM data (single row, always id=1) ─────────────────────────────────
    db.merge(models.DamData(
        id=1,
        damMonthly=json.dumps(cfg.get("damMonthly", [None] * 12)),
        damBySlot=json.dumps(cfg.get("damBySlot", [])),
        damDailyData=json.dumps(cfg.get("damDailyData", [[] for _ in range(12)])),
        damRowCount=int(cfg.get("damRowCount", 0)),
        damYear=int(cfg.get("damYear", 2026)),
    ))

    # ── Notices (single row, always id=1) ──────────────────────────────────
    n = cfg.get("notices", {})
    db.merge(models.Notices(
        id=1,
        # Backwards compat: old cfg used 'assumptions' / 'legal' (no lang suffix)
        assumptions_en=n.get("assumptions_en", n.get("assumptions", "")),
        assumptions_el=n.get("assumptions_el", ""),
        legal_en=n.get("legal_en", n.get("legal", "")),
        legal_el=n.get("legal_el", ""),
        vulnerable_en=n.get("vulnerable_en", ""),
        vulnerable_el=n.get("vulnerable_el", ""),
    ))

    db.commit()

    approved = db.query(models.Tariff).filter(models.Tariff.status == "approved").count()
    return {
        "status": "ok",
        "suppliers": db.query(models.Supplier).count(),
        "profiles": db.query(models.Profile).count(),
        "tariffs": db.query(models.Tariff).count(),
        "approved_tariffs": approved,
        "changelog_entries": db.query(models.Changelog).count(),
    }
