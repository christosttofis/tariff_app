"""Core monthly/annual cost engine. Originally a direct port of the old
client-side monthlyBreakdown / annualCostForTariff / annualCostNoDiscount /
monthlyKwhDisplay JS.

Every estimate covers a 12-month `window` — (year, month index 0-11) pairs
from daycounts.calc_window(), starting the month after today — so results
describe the customer's first year after switching. All per-month lists
(input day counts, output breakdowns) are in window order: index 0 is the
first month after switching, which is also "month 1" for discount durations.

All functions are pure: every input is an explicit parameter.
"""

import calendar
from datetime import date

from .daycounts import get_window_day_counts, is_non_working
from .discounts import get_discount_factors
from .profiles import compute_annual_hhff, get_slot_kwh
from .regulated import get_tariff_fpa
from .tiers import apply_tiers

# How many years back the Dynamic DAM lookup may go for the same date+slot
# (the DAM dataset covers roughly the past year; a window reaches up to a
# year ahead).
DAM_LOOKBACK_YEARS = 2


def _slot(arr: list | None, s: int) -> float:
    if not arr or s >= len(arr) or arr[s] is None:
        return 0
    return arr[s]


def _month_hhff(pm: dict, wd: int, nwd: int) -> float:
    w, nw = pm.get("W"), pm.get("NW")
    return sum(_slot(w, s) * wd + _slot(nw, s) * nwd for s in range(48))


def _monthly_slot_kwh(pm: dict | None, dcm: dict, m_kwh: float) -> list[float] | None:
    """Monthly mode: spread one month's flat kWh over the 48 half-hour slots
    by the profile's daily shape for that month (working and non-working days
    combined), normalised within the month so the slots add up to m_kwh."""
    if not pm:
        return None
    m_hhff = _month_hhff(pm, dcm["working"], dcm["nonWorking"])
    if m_hhff <= 0:
        return None
    w, nw = pm.get("W"), pm.get("NW")
    return [m_kwh * (_slot(w, s) * dcm["working"] + _slot(nw, s) * dcm["nonWorking"]) / m_hhff for s in range(48)]


def _in_season(month: int, start: int, end: int) -> bool:
    """ToU high season, months 1-12 inclusive. start > end wraps over the new
    year (11 -> 2 = Nov, Dec, Jan, Feb). 0 means unset: 0/0 = no high season."""
    if start <= end:
        return start <= month <= end
    if end == 0:
        return False
    return month >= start or month <= end


def _in_peak(hour: float, start: float, end: float) -> bool:
    """ToU peak window in hours, [start, end). start > end wraps over midnight
    (22 -> 6 = 22:00-06:00); start == end = no peak hours."""
    if start <= end:
        return start <= hour < end
    return hour >= start or hour < end


def _peak_hours(start: float, end: float) -> float:
    return min(24, end - start) if start <= end else 24 - start + end


def _in_window_order(per_month: list | None, window: list[tuple[int, int]]) -> list:
    """Reorder a calendar-month-indexed list (Jan..Dec) into window order."""
    per_month = per_month or []
    return [per_month[mi] if mi < len(per_month) else None for _, mi in window]


def monthly_kwh_display(
    tariff: dict,
    window: list[tuple[int, int]],
    *,
    is_monthly: bool,
    monthly_kwh_flat: float,
    annual_kwh: float,
    profile_months: list | None,
) -> list[float]:
    if is_monthly:
        return [monthly_kwh_flat] * 12
    if not profile_months or annual_kwh <= 0:
        return [annual_kwh / 12] * 12
    prof = _in_window_order(profile_months, window)
    dc = get_window_day_counts(window)
    annual_hhff = compute_annual_hhff(prof, dc)
    result = []
    for i in range(12):
        pm = prof[i]
        m_hhff = _month_hhff(pm, dc[i]["working"], dc[i]["nonWorking"]) if pm else 0
        result.append(annual_kwh * (m_hhff / annual_hhff) if annual_hhff > 0 else annual_kwh / 12)
    return result


def monthly_breakdown(
    tariff: dict,
    window: list[tuple[int, int]],
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

    # Everything below is indexed by window position i (0 = first month).
    dc = get_window_day_counts(window)
    prof = _in_window_order(profile_months, window) if profile_months else None
    fpa_rate = get_tariff_fpa(tariff, regulated_rates)
    standing = tariff.get("standing") or 0
    annual_hhff = compute_annual_hhff(prof, dc) if prof else 0

    def m_kwh_for_month(i: int) -> float:
        if is_monthly:
            return monthly_kwh_flat
        if prof:
            pm = prof[i]
            m_hhff = _month_hhff(pm, dc[i]["working"], dc[i]["nonWorking"]) if pm else 0
            return annual_kwh * (m_hhff / annual_hhff) if annual_hhff > 0 else annual_kwh / 12
        return annual_kwh / 12

    def get_df(month_no: int) -> dict:
        # month_no: 1 = first month after switching
        return get_discount_factors(
            tariff["id"],
            tariff.get("discounts") or [],
            month_no,
            (discount_overrides or {}).get(tariff["id"]),
            offers_enabled,
        )

    pricing = tariff.get("pricing")

    if pricing == "Fixed":
        rate = (tariff.get("rates") or {}).get("rate") or 0
        result = []
        for i in range(12):
            m_kwh = m_kwh_for_month(i)
            df = get_df(i + 1)
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
        for i, (_, mi) in enumerate(window):
            is_high = _in_season(mi + 1, r.get("hiStart") or 0, r.get("hiEnd") or 0)
            ps = r.get("hiPeakStart") if is_high else r.get("loPeakStart")
            pe = r.get("hiPeakEnd") if is_high else r.get("loPeakEnd")
            pr = r.get("hiPeakRate") if is_high else r.get("loPeakRate")
            orr = r.get("hiOffRate") if is_high else r.get("loOffRate")
            if not prof:
                slots = None
            elif is_monthly:
                slots = _monthly_slot_kwh(prof[i], dc[i], m_kwh_for_month(i))
            else:
                slots = get_slot_kwh(prof, i, annual_kwh, dc, annual_hhff)
            df = get_df(i + 1)
            if slots:
                peak_kwh = 0.0
                offpeak_kwh = 0.0
                peak_energy = 0.0
                offpeak_energy = 0.0
                fpa_total = 0.0
                for s in range(48):
                    # Slot start in hours (0, 0.5, ... 23.5), so half-hour
                    # peak boundaries such as 16.5 are honoured.
                    if _in_peak(s / 2, ps, pe):
                        peak_kwh += slots[s]
                        peak_energy += slots[s] * pr
                    else:
                        offpeak_kwh += slots[s]
                        offpeak_energy += slots[s] * orr
                    fpa_total += slots[s] * fpa_rate
            else:
                m_kwh = m_kwh_for_month(i)
                pf = _peak_hours(ps, pe) / 24
                peak_kwh = m_kwh * pf
                offpeak_kwh = m_kwh * (1 - pf)
                peak_energy = peak_kwh * pr
                offpeak_energy = offpeak_kwh * orr
                fpa_total = m_kwh * fpa_rate
            energy = peak_energy + offpeak_energy
            result.append({
                "energy": energy * df["energyFactor"], "fpa": fpa_total * df["energyFactor"],
                "standing": standing * df["standingFactor"],
                "total": energy * df["energyFactor"] + fpa_total * df["energyFactor"] + standing * df["standingFactor"],
                "energyFull": energy, "fpaFull": fpa_total, "standingFull": standing,
                "energyDisc": energy * (1 - df["energyFactor"]), "standingDisc": standing * (1 - df["standingFactor"]),
                "peakKwh": peak_kwh, "offPeakKwh": offpeak_kwh,
                "peakEnergy": peak_energy * df["energyFactor"], "offPeakEnergy": offpeak_energy * df["energyFactor"],
                "peakEnergyFull": peak_energy, "offPeakEnergyFull": offpeak_energy,
                "peakRate": pr, "offPeakRate": orr,
            })
        return result

    if pricing == "Dynamic":
        r = tariff.get("rates") or {}
        if not prof:
            return [None] * 12
        dims = [calendar.monthrange(y, mi + 1)[1] for y, mi in window]
        dam_slot_avgs = _in_window_order(dam_by_slot, window)
        dam_avgs = _in_window_order(dam_monthly, window)
        daily_by_month = _in_window_order(dam_daily_data, window)
        floor = r.get("damFloor") or 0
        mult = r.get("mult") or 1
        adder = r.get("adder") or 0
        result = []
        for i, (year, mi) in enumerate(window):
            pm = prof[i]
            if not pm:
                result.append(None)
                continue
            dam_slot_avg = dam_slot_avgs[i] or [None] * 48
            dam_avg = dam_avgs[i]
            day_slots_by_date = {x.get("dateStr"): x.get("slots") for x in (daily_by_month[i] or [])}

            m_kwh = m_kwh_for_month(i)
            m_hhff = _month_hhff(pm, dc[i]["working"], dc[i]["nonWorking"])

            energy = 0.0
            fpa_total = 0.0
            failed = False
            for d in range(1, dims[i] + 1):
                hhff_arr = pm.get("NW") if is_non_working(date(year, mi + 1, d)) else pm.get("W")
                # Actual prices for this date, then the same date 1, 2 … years earlier.
                candidates = [
                    day_slots_by_date.get(f"{year - back}-{mi + 1:02d}-{d:02d}")
                    for back in range(DAM_LOOKBACK_YEARS + 1)
                ]

                for s in range(48):
                    hhff = _slot(hhff_arr, s)
                    if is_monthly:
                        kwh_slot = m_kwh * (hhff) / m_hhff if m_hhff > 0 else m_kwh / (dims[i] * 48)
                    else:
                        # annual_hhff can be 0 for a profile with no shape data
                        # at all (e.g. all-zero W/NW arrays) - spread evenly
                        # across the window instead of dividing by zero.
                        kwh_slot = annual_kwh * (hhff) / annual_hhff if annual_hhff > 0 else annual_kwh / (sum(dims) * 48)

                    dam_raw = next((c[s] for c in candidates if c and s < len(c) and c[s] is not None), None)
                    if dam_raw is None:
                        dam_raw = dam_slot_avg[s] if s < len(dam_slot_avg) and dam_slot_avg[s] is not None else dam_avg

                    if dam_raw is None:
                        failed = True
                        break
                    energy += kwh_slot * (max(dam_raw, floor) * mult + adder)
                    fpa_total += kwh_slot * fpa_rate
                if failed:
                    break
            if failed:
                result.append(None)
                continue
            df = get_df(i + 1)
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
        # Billing periods start with the first month after switching.
        period_start = 0
        while period_start < 12:
            period_end = min(period_start + reset, 12)
            period_len = period_end - period_start
            month_kwhs = [m_kwh_for_month(i) for i in range(period_start, period_end)]
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
            for i in range(period_start, period_end):
                df = get_df(i + 1)
                month_standing = (standing + month_tier_fixed) * df["standingFactor"]
                month_standing_full = standing + month_tier_fixed
                result[i] = {
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


def annual_cost_for_tariff(tariff: dict, window: list[tuple[int, int]], **kwargs) -> float | None:
    bd = monthly_breakdown(tariff, window, **kwargs)
    if not bd or all(v is None for v in bd):
        return None
    total = 0.0
    for v in bd:
        if v is None:
            return None
        total += v["total"]
    return total


def annual_cost_no_discount(tariff: dict, window: list[tuple[int, int]], **kwargs) -> float | None:
    discounts = tariff.get("discounts") or []
    override = {f"{tariff['id']}_disc_{i}": False for i in range(len(discounts))}
    kwargs = dict(kwargs)
    kwargs["discount_overrides"] = {tariff["id"]: override}
    kwargs["offers_enabled"] = True
    bd = monthly_breakdown(tariff, window, **kwargs)
    if not bd or all(v is None for v in bd):
        return None
    return sum(v["total"] for v in bd)


def offer_summary(tariff: dict, months: list[dict | None], discount_overrides: dict | None, offers_enabled: bool) -> dict | None:
    """For a tariff whose active discounts run out inside the 12-month window:
    how many months the (longest) time-limited offer lasts, and the average
    monthly supplier cost once it has ended. None if nothing runs out.

    Shown to the customer so an attractive introductory offer can't hide what
    the rest of the year costs."""
    if not offers_enabled or not months or any(v is None for v in months):
        return None
    state = (discount_overrides or {}).get(tariff["id"]) or {}
    ending = [
        d.get("durationMonths")
        for i, d in enumerate(tariff.get("discounts") or [])
        if state.get(f"{tariff['id']}_disc_{i}") is not False and d.get("durationMonths") and d["durationMonths"] < 12
    ]
    if not ending:
        return None
    n = max(ending)
    after = months[n:]
    return {"months": n, "afterMonthlyAvg": sum(v["total"] for v in after) / len(after)}
