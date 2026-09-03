"""Core monthly/annual cost engine — direct port of monthlyBreakdown /
annualCostForTariff / annualCostNoDiscount / monthlyKwhDisplay in
customer.html (~lines 1610-1852).

All functions are pure: every value the JS read from `window`/`document`
(inputMode, _billingPeriod, window._discountState, the two kWh input
fields) is now an explicit parameter.
"""

from datetime import date

from .daycounts import get_cyprus_holidays
from .discounts import get_discount_factors
from .profiles import compute_annual_hhff, get_slot_kwh
from .regulated import get_tariff_fpa
from .tiers import apply_tiers

# Hardcoded to match the JS CALC_YEAR constant exactly (customer.html:1334) —
# used only for weekday/holiday lookups inside the Dynamic-mode day loop, to
# stay aligned with the DAM dataset's own date keys. Not derived from the
# real current year (that's `dc`'s year, passed in separately for HHFF
# normalisation, per the original JS's own — deliberate — inconsistency).
CALC_YEAR = 2026


def _slot(arr: list | None, s: int) -> float:
    if not arr or s >= len(arr) or arr[s] is None:
        return 0
    return arr[s]


def _js_day_of_week(d: date) -> int:
    return (d.weekday() + 1) % 7


def _month_hhff(pm: dict, wd: int, nwd: int) -> float:
    w, nw = pm.get("W"), pm.get("NW")
    return sum(_slot(w, s) * wd + _slot(nw, s) * nwd for s in range(48))


def monthly_kwh_display(
    tariff: dict,
    dc: list[dict],
    *,
    is_monthly: bool,
    monthly_kwh_flat: float,
    annual_kwh: float,
    profile_months: list | None,
) -> list[float]:
    if is_monthly:
        return [monthly_kwh_flat] * 12
    prof = profile_months
    if not prof or annual_kwh <= 0:
        return [annual_kwh / 12] * 12
    annual_hhff = compute_annual_hhff(prof, dc)
    result = []
    for m in range(12):
        pm = prof[m] if m < len(prof) else None
        m_hhff = _month_hhff(pm, dc[m]["working"], dc[m]["nonWorking"]) if pm else 0
        result.append(annual_kwh * (m_hhff / annual_hhff) if annual_hhff > 0 else annual_kwh / 12)
    return result


def monthly_breakdown(
    tariff: dict,
    dc: list[dict],
    *,
    is_monthly: bool,
    monthly_kwh_flat: float,
    annual_kwh: float,
    profile_months: list | None,
    regulated_rates: dict,
    discount_overrides: dict | None,
    offers_enabled: bool,
    dam_monthly: list | None = None,
    dam_by_slot: list | None = None,
    dam_daily_data: list | None = None,
) -> list[dict | None]:
    if annual_kwh <= 0:
        return [None] * 12

    prof = profile_months
    fpa_rate = get_tariff_fpa(tariff, regulated_rates)
    standing = tariff.get("standing") or 0
    annual_hhff = compute_annual_hhff(prof, dc) if prof else 0

    def m_kwh_for_month(m: int) -> float:
        if is_monthly:
            return monthly_kwh_flat
        if prof:
            pm = prof[m] if m < len(prof) else None
            m_hhff = _month_hhff(pm, dc[m]["working"], dc[m]["nonWorking"]) if pm else 0
            return annual_kwh * (m_hhff / annual_hhff) if annual_hhff > 0 else annual_kwh / 12
        return annual_kwh / 12

    def get_df(month_idx1: int) -> dict:
        return get_discount_factors(
            tariff["id"],
            tariff.get("discounts") or [],
            month_idx1,
            (discount_overrides or {}).get(tariff["id"]),
            offers_enabled,
        )

    pricing = tariff.get("pricing")

    if pricing == "Fixed":
        rate = (tariff.get("rates") or {}).get("rate") or 0
        result = []
        for m in range(12):
            m_kwh = m_kwh_for_month(m)
            df = get_df(m + 1)
            base_energy = m_kwh * rate
            base_fpa = m_kwh * fpa_rate
            result.append({
                "energy": base_energy * df["energyFactor"],
                "fpa": base_fpa * df["energyFactor"],
                "standing": standing * df["standingFactor"],
                "total": base_energy * df["energyFactor"] + base_fpa * df["energyFactor"] + standing * df["standingFactor"],
                "energyFull": base_energy, "fpaFull": base_fpa, "standingFull": standing,
                "energyDisc": base_energy * (1 - df["energyFactor"]),
                "standingDisc": standing * (1 - df["standingFactor"]),
            })
        return result

    if pricing == "ToU":
        r = tariff.get("rates") or {}
        result = []
        for m in range(12):
            is_high = (m + 1) >= (r.get("hiStart") or 0) and (m + 1) <= (r.get("hiEnd") or 0)
            ps = r.get("hiPeakStart") if is_high else r.get("loPeakStart")
            pe = r.get("hiPeakEnd") if is_high else r.get("loPeakEnd")
            pr = r.get("hiPeakRate") if is_high else r.get("loPeakRate")
            orr = r.get("hiOffRate") if is_high else r.get("loOffRate")
            slots = get_slot_kwh(prof, m, annual_kwh, dc, annual_hhff) if (not is_monthly and prof) else None
            df = get_df(m + 1)
            if slots:
                energy = 0.0
                fpa_total = 0.0
                for s in range(48):
                    h = (s * 30) // 60
                    energy += slots[s] * (pr if (ps <= h < pe) else orr)
                    fpa_total += slots[s] * fpa_rate
            else:
                m_kwh = m_kwh_for_month(m)
                pf = max(0, min(24, pe - ps)) / 24
                energy = m_kwh * pf * pr + m_kwh * (1 - pf) * orr
                fpa_total = m_kwh * fpa_rate
            result.append({
                "energy": energy * df["energyFactor"], "fpa": fpa_total * df["energyFactor"],
                "standing": standing * df["standingFactor"],
                "total": energy * df["energyFactor"] + fpa_total * df["energyFactor"] + standing * df["standingFactor"],
                "energyFull": energy, "fpaFull": fpa_total, "standingFull": standing,
                "energyDisc": energy * (1 - df["energyFactor"]), "standingDisc": standing * (1 - df["standingFactor"]),
            })
        return result

    if pricing == "Dynamic":
        r = tariff.get("rates") or {}
        if not prof:
            return [None] * 12
        is_leap = CALC_YEAR % 4 == 0 and (CALC_YEAR % 100 != 0 or CALC_YEAR % 400 == 0)
        dims = [31, 29 if is_leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        holidays = get_cyprus_holidays(CALC_YEAR)
        result = []
        for m in range(12):
            pm = prof[m] if m < len(prof) else None
            if not pm:
                result.append(None)
                continue
            wd, nwd = dc[m]["working"], dc[m]["nonWorking"]
            dam_slot_avg = dam_by_slot[m] if dam_by_slot and m < len(dam_by_slot) and dam_by_slot[m] else [None] * 48
            dam_avg = dam_monthly[m] if dam_monthly and m < len(dam_monthly) else None
            daily_data = dam_daily_data[m] if dam_daily_data and m < len(dam_daily_data) and dam_daily_data[m] else []

            m_kwh = m_kwh_for_month(m)
            m_hhff = _month_hhff(pm, wd, nwd)

            energy = 0.0
            fpa_total = 0.0
            failed = False
            for d in range(1, dims[m] + 1):
                date_str = f"{CALC_YEAR}-{m + 1:02d}-{d:02d}"
                date_key = date_str.replace("-", "")
                dow = _js_day_of_week(date(CALC_YEAR, m + 1, d))
                is_non_work = dow == 0 or dow == 6 or date_key in holidays
                hhff_arr = pm.get("NW") if is_non_work else pm.get("W")
                day_dam = next((x for x in daily_data if x.get("dateStr") == date_str), None)
                date_str_ly = f"{CALC_YEAR - 1}-{m + 1:02d}-{d:02d}"
                day_dam_ly = next((x for x in daily_data if x.get("dateStr") == date_str_ly), None)

                for s in range(48):
                    hhff = _slot(hhff_arr, s)
                    if is_monthly:
                        kwh_slot = m_kwh * (hhff) / m_hhff if m_hhff > 0 else m_kwh / (dims[m] * 48)
                    else:
                        kwh_slot = annual_kwh * (hhff) / annual_hhff

                    dam_raw = None
                    day_slots = day_dam.get("slots") if day_dam else None
                    day_slots_ly = day_dam_ly.get("slots") if day_dam_ly else None
                    if day_slots and s < len(day_slots) and day_slots[s] is not None:
                        dam_raw = day_slots[s]
                    elif day_slots_ly and s < len(day_slots_ly) and day_slots_ly[s] is not None:
                        dam_raw = day_slots_ly[s]
                    elif dam_slot_avg[s] is not None:
                        dam_raw = dam_slot_avg[s]
                    elif dam_avg is not None:
                        dam_raw = dam_avg

                    if dam_raw is None:
                        failed = True
                        break
                    eff_price = max(dam_raw, r.get("damFloor") or 0)
                    mult = r.get("mult") or 1
                    adder = r.get("adder") or 0
                    energy += kwh_slot * (eff_price * mult + adder)
                    fpa_total += kwh_slot * fpa_rate
                if failed:
                    break
            if failed:
                result.append(None)
                continue
            df = get_df(m + 1)
            result.append({
                "energy": energy * df["energyFactor"], "fpa": fpa_total * df["energyFactor"],
                "standing": standing * df["standingFactor"],
                "total": energy * df["energyFactor"] + fpa_total * df["energyFactor"] + standing * df["standingFactor"],
                "energyFull": energy, "fpaFull": fpa_total, "standingFull": standing,
                "energyDisc": energy * (1 - df["energyFactor"]), "standingDisc": standing * (1 - df["standingFactor"]),
            })
        return result

    if pricing == "Variable":
        r = tariff.get("rates") or {}
        tiers = r.get("tiers") or []
        reset = r.get("resetMonths") or 1
        result: list[dict | None] = [None] * 12
        period_start = 0
        while period_start < 12:
            period_end = min(period_start + reset, 12)
            period_len = period_end - period_start
            month_kwhs = [m_kwh_for_month(m) for m in range(period_start, period_end)]
            period_kwh = sum(month_kwhs)
            period_energy_cost = apply_tiers(tiers, period_kwh)
            period_fpa_cost = period_kwh * fpa_rate
            period_fixed_cost = 0.0
            prev = 0.0
            for tier in tiers:
                up_to = tier.get("upTo")
                cap = up_to if up_to is not None else float("inf")
                if period_kwh > prev:
                    period_fixed_cost += tier.get("fixedCharge") or 0
                prev = cap
                if up_to is None or period_kwh <= cap:
                    break
            month_energy = period_energy_cost / period_len
            month_fpa = period_fpa_cost / period_len
            month_tier_fixed = period_fixed_cost / period_len
            for mi in range(period_start, period_end):
                df = get_df(mi + 1)
                month_standing = (standing + month_tier_fixed) * df["standingFactor"]
                month_standing_full = standing + month_tier_fixed
                result[mi] = {
                    "energy": month_energy * df["energyFactor"], "fpa": month_fpa * df["energyFactor"],
                    "standing": month_standing,
                    "total": month_energy * df["energyFactor"] + month_fpa * df["energyFactor"] + month_standing,
                    "energyFull": month_energy, "fpaFull": month_fpa, "standingFull": month_standing_full,
                    "energyDisc": month_energy * (1 - df["energyFactor"]),
                    "standingDisc": month_standing_full * (1 - df["standingFactor"]),
                }
            period_start += reset
        return result

    return [None] * 12


def annual_cost_for_tariff(tariff: dict, dc: list[dict], **kwargs) -> float | None:
    bd = monthly_breakdown(tariff, dc, **kwargs)
    if not bd or all(v is None for v in bd):
        return None
    total = 0.0
    for v in bd:
        if v is None:
            return None
        total += v["total"]
    return total


def annual_cost_no_discount(tariff: dict, dc: list[dict], **kwargs) -> float | None:
    discounts = tariff.get("discounts") or []
    override = {f"{tariff['id']}_disc_{i}": False for i in range(len(discounts))}
    kwargs = dict(kwargs)
    kwargs["discount_overrides"] = {tariff["id"]: override}
    kwargs["offers_enabled"] = True
    bd = monthly_breakdown(tariff, dc, **kwargs)
    if not bd or all(v is None for v in bd):
        return None
    return sum(v["total"] for v in bd)
