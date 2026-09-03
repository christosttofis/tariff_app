"""Public tariff-calculation API.

Replaces the client-side calculation previously done entirely in
customer.html JS against the full raw dataset returned by
GET /api/public/config. See SECURITY_REMEDIATION_PLAN_customer_data_exposure.md
for the full rationale and phased rollout plan.

Route handlers here are orchestration only — all pricing math lives in the
pricing/ package as pure, independently-testable functions.
"""

import json
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
from database import get_db
from pricing.daycounts import get_day_counts
from pricing.display import format_tier_summary
from pricing.engine import annual_cost_for_tariff, annual_cost_no_discount, monthly_breakdown, monthly_kwh_display
from pricing.filters import filter_matching_tariffs
from pricing.invoice import build_sample_invoice_data
from pricing.regulated import get_regulated_rates, get_tariff_fpa, mdm_for_tariff, regulated_breakdown
from schemas import PublicCalculateIn, PublicSampleInvoiceIn
from serializers import tariff_to_dict

router = APIRouter(prefix="/api/public", tags=["public-calculate"])


def _load_context(db: Session):
    tariffs = [
        tariff_to_dict(t)
        for t in db.query(models.Tariff).filter(models.Tariff.status == "approved").all()
    ]
    profiles_by_id = {}
    for p in db.query(models.Profile).all():
        profiles_by_id[p.id] = json.loads(p.months) if p.months else []
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
    return tariffs, profiles_by_id, suppliers_regulated, regulated_rates, dam_monthly, dam_by_slot, dam_daily_data


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


@router.post("/calculate", summary="Compute ranked tariff comparison for the customer calculator")
def calculate(body: PublicCalculateIn, db: Session = Depends(get_db)):
    tariffs, profiles_by_id, suppliers_regulated, regulated_rates, dam_monthly, dam_by_slot, dam_daily_data = _load_context(db)

    if body.customerType == "domestic":
        voltage, contracts, load_entitlement = "LV", ["Domestic"], None
    else:
        voltage = body.voltage
        contracts = ["Commercial", "Industrial"]
        load_entitlement = None if voltage == "HV" else body.loadEntitlement

    is_monthly = body.inputMode == "monthly"
    monthly_kwh_flat = body.monthlyKwh / body.billingPeriod if body.billingPeriod else 0
    annual_kwh = (monthly_kwh_flat * 12) if is_monthly else body.annualKwh

    if annual_kwh <= 0:
        return {"results": [], "noDamTariffs": []}

    dc = get_day_counts(datetime.now(timezone.utc).year)

    matched = filter_matching_tariffs(tariffs, voltage, contracts, body.pricingFilter, load_entitlement, body.vulnerableEligible)

    results = []
    no_dam = []
    for t in matched:
        kwargs = _calc_kwargs(
            t, profiles_by_id, regulated_rates,
            is_monthly=is_monthly, monthly_kwh_flat=monthly_kwh_flat, annual_kwh=annual_kwh,
            discount_overrides=body.discountOverrides, offers_enabled=body.offersEnabled,
            dam_monthly=dam_monthly, dam_by_slot=dam_by_slot, dam_daily_data=dam_daily_data,
        )
        base = annual_cost_for_tariff(t, dc, **kwargs)
        if base is None:
            if t.get("pricing") == "Dynamic":
                no_dam.append({"id": t["id"], "name": t["name"], "supplier": t["supplier"]})
            continue

        supplier_regulated = suppliers_regulated.get(t["supplier"], False)
        mdm = mdm_for_tariff(t, supplier_regulated, regulated_rates)
        reg_bd = regulated_breakdown(t["voltage"], annual_kwh, mdm, t.get("mdmInvoiceMonths"), supplier_regulated, regulated_rates)

        has_discounts = bool(t.get("discounts"))
        full_base = annual_cost_no_discount(t, dc, **kwargs) if has_discounts else None

        months = monthly_breakdown(t, dc, **kwargs)
        mo_kwh = monthly_kwh_display(
            t, dc, is_monthly=is_monthly, monthly_kwh_flat=monthly_kwh_flat, annual_kwh=annual_kwh,
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
        }
        if t.get("pricing") == "Variable":
            entry["tierSummary"] = format_tier_summary(t)
            entry["resetMonths"] = (t.get("rates") or {}).get("resetMonths") or 1
        if t.get("pricing") == "Dynamic":
            entry["damFloor"] = (t.get("rates") or {}).get("damFloor")

        results.append(entry)

    results.sort(key=lambda r: r["base"])
    return {"results": results, "noDamTariffs": no_dam}


@router.post("/sample-invoice", summary="Compute the on-demand sample-invoice modal data for one tariff")
def sample_invoice(body: PublicSampleInvoiceIn, db: Session = Depends(get_db)):
    tariffs, profiles_by_id, suppliers_regulated, regulated_rates, dam_monthly, dam_by_slot, dam_daily_data = _load_context(db)
    t = next((x for x in tariffs if x["id"] == body.tariffId), None)
    if not t:
        raise HTTPException(404, "Tariff not found")

    is_monthly = body.inputMode == "monthly"
    monthly_kwh_flat = body.monthlyKwh / body.billingPeriod if body.billingPeriod else 0
    annual_kwh = (monthly_kwh_flat * 12) if is_monthly else body.annualKwh
    if annual_kwh <= 0:
        return None

    dc = get_day_counts(datetime.now(timezone.utc).year)
    kwargs = _calc_kwargs(
        t, profiles_by_id, regulated_rates,
        is_monthly=is_monthly, monthly_kwh_flat=monthly_kwh_flat, annual_kwh=annual_kwh,
        discount_overrides=body.discountOverrides, offers_enabled=body.offersEnabled,
        dam_monthly=dam_monthly, dam_by_slot=dam_by_slot, dam_daily_data=dam_daily_data,
    )
    months = monthly_breakdown(t, dc, **kwargs)
    mo_kwh = monthly_kwh_display(
        t, dc, is_monthly=is_monthly, monthly_kwh_flat=monthly_kwh_flat, annual_kwh=annual_kwh,
        profile_months=kwargs["profile_months"],
    )
    supplier_regulated = suppliers_regulated.get(t["supplier"], False)
    return build_sample_invoice_data(
        t, months, mo_kwh, annual_kwh, regulated_rates, supplier_regulated, body.inputMode, body.billingPeriod,
    )
