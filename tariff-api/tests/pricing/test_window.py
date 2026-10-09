r"""The 12-month calculation window: estimates cover the customer's first year
after switching (starting next month), not January-December.

Run from tariff-api/:  .venv\Scripts\python.exe -m pytest tests/pricing
"""

import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from pricing.daycounts import calc_window, get_window_day_counts  # noqa: E402
from pricing.engine import monthly_breakdown, offer_summary  # noqa: E402
from pricing.invoice import get_sample_invoice_period  # noqa: E402

WINDOW = calc_window(date(2026, 10, 9))   # Nov 2026 - Oct 2027
PROFILE = [{"W": [1.0] * 36 + [3.0] * 12, "NW": [1.0] * 48} for _ in range(12)]


def _run(tariff, window=WINDOW, **kw):
    args = dict(
        is_monthly=False, monthly_kwh_flat=0, annual_kwh=5000, profile_months=PROFILE,
        regulated_rates={"fpaLV": 0, "fpaMV": 0, "fpaHV": 0}, discount_overrides=None, offers_enabled=True,
    )
    args.update(kw)
    return monthly_breakdown(tariff, window, **args)


@pytest.mark.parametrize("today,first,last", [
    (date(2026, 10, 9), (2026, 10), (2027, 9)),    # Oct -> Nov 2026 .. Oct 2027
    (date(2026, 12, 31), (2027, 0), (2027, 11)),   # Dec -> Jan .. Dec of next year
    (date(2027, 1, 1), (2027, 1), (2028, 0)),      # Jan -> Feb 2027 .. Jan 2028
])
def test_window_starts_next_month(today, first, last):
    w = calc_window(today)
    assert len(w) == 12 and w[0] == first and w[-1] == last


def test_window_day_counts_cover_every_day_including_leap_february():
    w = calc_window(date(2027, 6, 15))   # Jul 2027 - Jun 2028, includes 29 Feb 2028
    dc = get_window_day_counts(w)
    assert sum(m["working"] + m["nonWorking"] for m in dc) == 366


def test_time_limited_discount_starts_with_first_month_after_switching():
    t = {"id": "t", "pricing": "Fixed", "rates": {"rate": 0.2}, "fpaSource": "none",
         "discounts": [{"type": "energy", "percentage": 50, "durationMonths": 3}]}
    bd = _run(t)
    discounted = [i for i, m in enumerate(bd) if m["energyDisc"] > 0]
    assert discounted == [0, 1, 2]   # Nov, Dec, Jan — not Jan, Feb, Mar


def test_tou_high_season_follows_the_calendar_month_not_the_position():
    t = {"id": "t", "pricing": "ToU", "fpaSource": "none", "rates": {
        "hiStart": 6, "hiEnd": 9, "hiPeakStart": 0, "hiPeakEnd": 24, "loPeakStart": 0, "loPeakEnd": 24,
        "hiPeakRate": 2, "hiOffRate": 2, "loPeakRate": 1, "loOffRate": 1}}
    bd = _run(t)
    high = [WINDOW[i][1] + 1 for i, m in enumerate(bd) if m["peakRate"] == 2]
    assert high == [6, 7, 8, 9]


def _dyn():
    return {"id": "t", "pricing": "Dynamic", "rates": {"mult": 1, "adder": 0, "damFloor": None}, "fpaSource": "none"}


def test_dynamic_prices_exactly_the_entered_kwh_across_the_year_boundary():
    bd = _run(_dyn(), dam_monthly=[1.0] * 12)
    assert sum(m["energyFull"] for m in bd) == pytest.approx(5000)


def test_dynamic_uses_same_date_up_to_two_years_back_before_averages():
    # Only a 2025 price exists for 15 Jan; the window's January is 2027.
    daily = [[] for _ in range(12)]
    daily[0] = [{"dateStr": "2025-01-15", "slots": [10.0] * 48}]
    with_day = _run(_dyn(), dam_monthly=[1.0] * 12, dam_daily_data=daily)
    without = _run(_dyn(), dam_monthly=[1.0] * 12)
    jan = next(i for i, (_, mi) in enumerate(WINDOW) if mi == 0)
    assert with_day[jan]["energyFull"] > without[jan]["energyFull"]
    assert with_day[jan - 1]["energyFull"] == pytest.approx(without[jan - 1]["energyFull"])


def test_offer_summary_shows_cost_after_the_offer_ends():
    t = {"id": "t", "pricing": "Fixed", "rates": {"rate": 0.2}, "fpaSource": "none", "standing": 0,
         "discounts": [{"type": "energy", "percentage": 50, "durationMonths": 3},
                       {"type": "standing", "percentage": 10, "durationMonths": None}]}
    bd = _run(t)
    s = offer_summary(t, bd, None, True)
    assert s["months"] == 3
    assert s["afterMonthlyAvg"] == pytest.approx(sum(m["total"] for m in bd[3:]) / 9)
    # Offer switched off by the customer, or offers hidden -> nothing to warn about.
    assert offer_summary(t, bd, {"t": {"t_disc_0": False}}, True) is None
    assert offer_summary(t, bd, None, False) is None


def test_offer_summary_ignores_permanent_and_full_year_discounts():
    t = {"id": "t", "discounts": [{"type": "energy", "percentage": 5, "durationMonths": None},
                                  {"type": "energy", "percentage": 5, "durationMonths": 12}]}
    assert offer_summary(t, [{"total": 1}] * 12, None, True) is None


def test_sample_invoice_is_the_first_bill_after_switching():
    p = get_sample_invoice_period({"mdmInvoiceMonths": 2}, "annual", 1, calc_window(date(2026, 11, 20)))
    assert p == {"monthIndices": [0, 1], "startDate": "2026-12-01", "endDate": "2027-01-31"}
    p = get_sample_invoice_period({}, "monthly", 1, WINDOW)
    assert p == {"monthIndices": [0], "startDate": "2026-11-01", "endDate": "2026-11-30"}


def _tou(peak_start, peak_end):
    return {"id": "t", "pricing": "ToU", "fpaSource": "none", "rates": {
        "hiStart": 0, "hiEnd": 0, "hiPeakStart": 0, "hiPeakEnd": 0, "loPeakStart": peak_start, "loPeakEnd": peak_end,
        "hiPeakRate": 0, "hiOffRate": 0, "loPeakRate": 1, "loOffRate": 0}}


def test_tou_monthly_mode_uses_the_profile_daily_shape():
    # PROFILE: working days use 3x more from 18:00; non-working days are flat.
    bd = _run(_tou(18, 24), is_monthly=True, monthly_kwh_flat=400, annual_kwh=4800)
    dc = get_window_day_counts(WINDOW)
    for m, d in zip(bd, dc):
        wd, nwd = d["working"], d["nonWorking"]
        expected_peak = 400 * (12 * 3 * wd + 12 * nwd) / (36 * wd + 12 * 3 * wd + 48 * nwd)
        assert m["peakKwh"] + m["offPeakKwh"] == pytest.approx(400)
        assert m["peakKwh"] == pytest.approx(expected_peak)
        assert m["peakKwh"] > 400 * 6 / 24   # more than the old flat hours/24 share


def test_tou_monthly_mode_without_profile_keeps_flat_split():
    bd = _run(_tou(18, 24), is_monthly=True, monthly_kwh_flat=400, annual_kwh=4800, profile_months=None)
    assert all(m["peakKwh"] == pytest.approx(100) for m in bd)


def _tou_rates(**rates):
    base = {"hiStart": 0, "hiEnd": 0, "hiPeakStart": 0, "hiPeakEnd": 0, "loPeakStart": 0, "loPeakEnd": 0,
            "hiPeakRate": 2, "hiOffRate": 2, "loPeakRate": 1, "loOffRate": 1}
    base.update(rates)
    return {"id": "t", "pricing": "ToU", "fpaSource": "none", "rates": base}


@pytest.mark.parametrize("start,end,months", [
    (6, 9, [6, 7, 8, 9]),          # normal summer season
    (11, 2, [11, 12, 1, 2]),       # winter season wrapping over the new year
    (0, 0, []),                    # no high season
    (5, 0, []),                    # end unset -> no high season (as before)
])
def test_tou_high_season_may_wrap_over_new_year(start, end, months):
    bd = _run(_tou_rates(hiStart=start, hiEnd=end))
    high = sorted(WINDOW[i][1] + 1 for i, m in enumerate(bd) if m["peakRate"] == 2)
    assert high == sorted(months)


def test_tou_peak_window_may_wrap_over_midnight():
    # Night peak 22:00-06:00 = 8 hours = 16 of 48 equal half-hour slots.
    t = _tou_rates(loPeakStart=22, loPeakEnd=6, loPeakRate=1, loOffRate=0)
    flat = [{"W": [1.0] * 48, "NW": [1.0] * 48} for _ in range(12)]
    annual = _run(t, profile_months=flat)
    assert sum(m["peakKwh"] for m in annual) == pytest.approx(5000 * 16 / 48)
    # Monthly mode without a profile: peak share = 8 / 24 hours.
    monthly = _run(t, is_monthly=True, monthly_kwh_flat=300, annual_kwh=3600, profile_months=None)
    assert all(m["peakKwh"] == pytest.approx(100) for m in monthly)
    # 22:00 to midnight (end 0) = 2 hours.
    late = _run(_tou_rates(loPeakStart=22, loPeakEnd=0, loPeakRate=1, loOffRate=0), profile_months=flat)
    assert sum(m["peakKwh"] for m in late) == pytest.approx(5000 * 4 / 48)


def test_no_discount_total_is_exactly_the_same_when_no_discount_applies():
    # With offers switched off, the "full price" must equal the shown price
    # exactly, or the page shows a struck-through price equal to the real one.
    from pricing.engine import annual_cost_for_tariff, annual_cost_no_discount
    t = dict(_dyn(), discounts=[{"type": "energy", "percentage": 50, "durationMonths": 3}])
    daily = [[{"dateStr": f"2026-{m + 1:02d}-01", "slots": [0.1 + 0.0137 * s for s in range(48)]}] for m in range(12)]
    kw = dict(is_monthly=False, monthly_kwh_flat=0, annual_kwh=7777, profile_months=PROFILE,
              regulated_rates={"fpaLV": 0.0351, "fpaMV": 0, "fpaHV": 0}, discount_overrides=None,
              dam_monthly=[0.17] * 12, dam_daily_data=daily)
    t["fpaSource"] = "global"; t["voltage"] = "LV"; t["standing"] = 4.37
    assert annual_cost_for_tariff(t, WINDOW, offers_enabled=False, **kw) == annual_cost_no_discount(t, WINDOW, offers_enabled=True, **kw)
