"""Public tariff-calculation API.

Replaces the client-side calculation previously done entirely in
customer.html JS against the full raw dataset returned by
GET /api/public/config. See SECURITY_REMEDIATION_PLAN_customer_data_exposure.md
for the full rationale and phased rollout plan.

Route handlers here are orchestration only — all pricing math lives in the
pricing/ package as pure, independently-testable functions.
"""

import json
import logging
import math
from datetime import date, datetime
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
from database import get_db
from pricing.daycounts import calc_window
from pricing.display import format_tier_summary
from pricing.engine import annual_cost_for_tariff, annual_cost_no_discount, monthly_breakdown, monthly_kwh_display, offer_summary
from pricing.filters import filter_matching_tariffs
from pricing.invoice import build_sample_invoice_data
from pricing.regulated import get_regulated_rates, get_tariff_fpa, mdm_for_tariff, regulated_breakdown
from schemas import PublicCalculateIn, PublicSampleInvoiceIn
from serializers import tariff_to_dict

router = APIRouter(prefix="/api/public", tags=["public-calculate"])

logger = logging.getLogger(__name__)

CYPRUS_TZ = ZoneInfo("Europe/Nicosia")


def _today_in_cyprus() -> date:
    return datetime.now(CYPRUS_TZ).date()


def _window_json(window: list[tuple[int, int]]) -> list[dict]:
    return [{"year": y, "month": mi + 1} for y, mi in window]


def _load_context(db: Session):
    tariffs = [
        tariff_to_dict(t)
        for t in db.query(models.Tariff).filter(models.Tariff.status == "approved").all()
    ]
    profiles_by_id = {}
    profile_names = {}
    for p in db.query(models.Profile).all():
        profiles_by_id[p.id] = json.loads(p.months) if p.months else []
        profile_names[p.id] = p.name
    suppliers_regulated = {s.name: bool(s.regulated) for s in db.query(models.Supplier).all()}
    reg_row = db.query(models.Regulated).first()
    regulated_rates = get_regulated_rates({
        "lv": reg_row.lv if reg_row else 0, "mv": reg_row.mv if reg_row else 0, "hv": reg_row.hv if reg_row else 0,
        "fpaLV": reg_row.fpaLV if reg_row else 0, "fpaMV": reg_row.fpaMV if reg_row else 0, "fpaHV": reg_row.fpaHV if reg_row else 0,
        "pso": reg_row.pso if reg_row else 0, "res": reg_row.res if reg_row else 0, "mdm": reg_row.mdm if reg_row else 0,
    })
    dam = db.query(models.DamData).first()
    dam_monthly = json.loads(dam.damMonthly) if dam and dam.damMonthly else [None] * 12
    dam_by_slot = json.loads(dam.damBySlot) if dam and dam.damBySlot else []
    dam_daily_data = json.loads(dam.damDailyData) if dam and dam.damDailyData else [[] for _ in range(12)]
    return tariffs, profiles_by_id, profile_names, suppliers_regulated, regulated_rates, dam_monthly, dam_by_slot, dam_daily_data


def _calc_kwargs(t: dict, profiles_by_id: dict, regulated_rates: dict, *, is_monthly, monthly_kwh_flat, annual_kwh, discount_overrides, offers_enabled, dam_monthly, dam_by_slot, dam_daily_data) -> dict:
    return {
        "is_monthly": is_monthly,
        "monthly_kwh_flat": monthly_kwh_flat,
        "annual_kwh": annual_kwh,
        "profile_months": profiles_by_id.get(t.get("profileId")) if t.get("profileId") else None,
        "regulated_rates": regulated_rates,
        "discount_overrides": discount_overrides,
        "offers_enabled": offers_enabled,
        "dam_monthly": dam_monthly,
        "dam_by_slot": dam_by_slot,
        "dam_daily_data": dam_daily_data,
    }


def _tariff_result(t: dict, window, profiles_by_id: dict, profile_names: dict, suppliers_regulated: dict, regulated_rates: dict, *,
                   body: PublicCalculateIn, is_monthly, monthly_kwh_flat, annual_kwh, dam_monthly, dam_by_slot, dam_daily_data) -> dict | None:
    """One tariff's comparison entry, or None if it can't be priced (e.g. a Dynamic tariff with no DAM data)."""
    kwargs = _calc_kwargs(
        t, profiles_by_id, regulated_rates,
        is_monthly=is_monthly, monthly_kwh_flat=monthly_kwh_flat, annual_kwh=annual_kwh,
        discount_overrides=body.discountOverrides, offers_enabled=body.offersEnabled,
        dam_monthly=dam_monthly, dam_by_slot=dam_by_slot, dam_daily_data=dam_daily_data,
    )
    base = annual_cost_for_tariff(t, window, **kwargs)
    if base is None:
        return None
    if not math.isfinite(base):
        raise ValueError(f"non-finite annual cost {base!r}")

    supplier_regulated = suppliers_regulated.get(t["supplier"], False)
    mdm = mdm_for_tariff(t, supplier_regulated, regulated_rates)
    reg_bd = regulated_breakdown(t["voltage"], annual_kwh, mdm, t.get("mdmInvoiceMonths"), supplier_regulated, regulated_rates)

    # Full (undiscounted) price only when offers are shown and the tariff has any.
    has_discounts = bool(t.get("discounts")) and body.offersEnabled
    full_base = annual_cost_no_discount(t, window, **kwargs) if has_discounts else None

    months = monthly_breakdown(t, window, **kwargs)
    mo_kwh = monthly_kwh_display(
        t, window, is_monthly=is_monthly, monthly_kwh_flat=monthly_kwh_flat, annual_kwh=annual_kwh,
        profile_months=kwargs["profile_months"],
    )

    entry = {
        "id": t["id"],
        "base": base,
        "reg": reg_bd["total"],
        "fullBase": full_base,
        "months": months,
        "moKwh": mo_kwh,
        "regBd": {k: v for k, v in reg_bd.items() if k != "total"},
        "fpaRate": get_tariff_fpa(t, regulated_rates),
        # Already shown to the customer today (renderDiscountToggles) —
        # not new exposure, just relocated alongside the rest of the
        # per-tariff pricing result.
        "discounts": t.get("discounts") or [],
        "profileName": profile_names.get(t.get("profileId")),
        "offer": offer_summary(t, months, body.discountOverrides, body.offersEnabled),
    }
    if t.get("pricing") == "Variable":
        entry["tierSummary"] = format_tier_summary(t)
        entry["resetMonths"] = (t.get("rates") or {}).get("resetMonths") or 1
    if t.get("pricing") == "Dynamic":
        entry["damFloor"] = (t.get("rates") or {}).get("damFloor")

    return entry


@router.post("/calculate", summary="Compute ranked tariff comparison for the customer calculator")
def calculate(body: PublicCalculateIn, db: Session = Depends(get_db)):
    tariffs, profiles_by_id, profile_names, suppliers_regulated, regulated_rates, dam_monthly, dam_by_slot, dam_daily_data = _load_context(db)
    has_slot_dam = any(v is not None for month in (dam_by_slot or []) for v in (month or []))

    if body.customerType == "domestic":
        voltage, contracts, load_entitlement = "LV", ["Domestic"], None
    else:
        voltage = body.voltage
        contracts = ["Commercial", "Industrial"]
        load_entitlement = None if voltage == "HV" else body.loadEntitlement

    is_monthly = body.inputMode == "monthly"
    monthly_kwh_flat = body.monthlyKwh / body.billingPeriod if body.billingPeriod else 0
    annual_kwh = (monthly_kwh_flat * 12) if is_monthly else body.annualKwh

    window = calc_window(_today_in_cyprus())
    if annual_kwh <= 0:
        return {"results": [], "noDamTariffs": [], "window": _window_json(window)}

    matched = filter_matching_tariffs(tariffs, voltage, contracts, body.pricingFilter, load_entitlement, body.vulnerableEligible)

    results = []
    no_dam = []
    for t in matched:
        # One tariff with data the engine can't handle must not take the whole
        # comparison down for every customer: skip it and log it instead.
        # (Input validation in schemas.TariffIn is the primary defence; this
        # is the safety net for anything already stored or missed there.)
        try:
            entry = _tariff_result(
                t, window, profiles_by_id, profile_names, suppliers_regulated, regulated_rates,
                body=body, is_monthly=is_monthly, monthly_kwh_flat=monthly_kwh_flat, annual_kwh=annual_kwh,
                dam_monthly=dam_monthly, dam_by_slot=dam_by_slot, dam_daily_data=dam_daily_data,
            )
        except Exception:
            logger.exception("Skipping tariff %s (%s) in public calculation: pricing engine failed", t.get("id"), t.get("name"))
            continue
        if entry is None:
            if t.get("pricing") == "Dynamic":
                no_dam.append({"id": t["id"], "name": t["name"], "supplier": t["supplier"]})
            continue
        results.append(entry)

    results.sort(key=lambda r: r["base"])
    return {"results": results, "noDamTariffs": no_dam, "hasSlotDam": has_slot_dam, "window": _window_json(window)}


@router.post("/sample-invoice", summary="Compute the on-demand sample-invoice modal data for one tariff")
def sample_invoice(body: PublicSampleInvoiceIn, db: Session = Depends(get_db)):
    tariffs, profiles_by_id, profile_names, suppliers_regulated, regulated_rates, dam_monthly, dam_by_slot, dam_daily_data = _load_context(db)
    t = next((x for x in tariffs if x["id"] == body.tariffId), None)
    if not t:
        raise HTTPException(404, "Tariff not found")

    is_monthly = body.inputMode == "monthly"
    monthly_kwh_flat = body.monthlyKwh / body.billingPeriod if body.billingPeriod else 0
    annual_kwh = (monthly_kwh_flat * 12) if is_monthly else body.annualKwh
    if annual_kwh <= 0:
        return None

    window = calc_window(_today_in_cyprus())
    kwargs = _calc_kwargs(
        t, profiles_by_id, regulated_rates,
        is_monthly=is_monthly, monthly_kwh_flat=monthly_kwh_flat, annual_kwh=annual_kwh,
        discount_overrides=body.discountOverrides, offers_enabled=body.offersEnabled,
        dam_monthly=dam_monthly, dam_by_slot=dam_by_slot, dam_daily_data=dam_daily_data,
    )
    months = monthly_breakdown(t, window, **kwargs)
    mo_kwh = monthly_kwh_display(
        t, window, is_monthly=is_monthly, monthly_kwh_flat=monthly_kwh_flat, annual_kwh=annual_kwh,
        profile_months=kwargs["profile_months"],
    )
    supplier_regulated = suppliers_regulated.get(t["supplier"], False)
    return build_sample_invoice_data(
        t, months, mo_kwh, annual_kwh, regulated_rates, supplier_regulated, body.inputMode, body.billingPeriod, window,
    )
