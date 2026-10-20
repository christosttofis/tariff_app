"""Pricing-engine checks for the calendar (holidays, day counts) and the
half-hourly slot split. Pure functions only — no server or database needed.

Run from tariff-api/:  .venv\\Scripts\\python.exe -m pytest tests/pricing
"""

import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from pricing.daycounts import calc_window, easter_date, get_cyprus_holidays, get_window_day_counts  # noqa: E402
from pricing.engine import monthly_breakdown  # noqa: E402

WINDOW = calc_window(date(2026, 10, 9))   # Nov 2026 - Oct 2027


@pytest.mark.parametrize("year,expected", [
    (2024, date(2024, 5, 5)),
    (2025, date(2025, 4, 20)),
    (2026, date(2026, 4, 12)),
    (2027, date(2027, 5, 2)),
    (2028, date(2028, 4, 16)),
])
def test_orthodox_easter(year, expected):
    assert easter_date(year) == expected


def test_cyprus_holidays_2026_movable_dates():
    h = get_cyprus_holidays(2026)
    # Green Monday, Good Friday, Easter Monday, Kataklysmos (Whit Monday)
    for d in ("20260223", "20260410", "20260413", "20260601"):
        assert d in h
    # Western-Easter dates the old algorithm produced
    for d in ("20260216", "20260403", "20260406"):
        assert d not in h


def test_day_counts_cover_every_day():
    for year in (2026, 2027, 2028):
        dc = get_window_day_counts([(year, mi) for mi in range(12)])
        total = sum(m["working"] + m["nonWorking"] for m in dc)
        assert total == (366 if year == 2028 else 365)


def _flat_profile(w=1.0, nw=1.0):
    return [{"W": [w] * 48, "NW": [nw] * 48} for _ in range(12)]


def _peaky_profile():
    # Working days use more in the evening; non-working days are flat.
    w = [1.0] * 36 + [3.0] * 12
    return [{"W": list(w), "NW": [1.0] * 48} for _ in range(12)]


def _run(tariff, profile, **kw):
    args = dict(
        is_monthly=False, monthly_kwh_flat=0, annual_kwh=5000, profile_months=profile,
        regulated_rates={"fpaLV": 0, "fpaMV": 0, "fpaHV": 0}, discount_overrides=None, offers_enabled=True,
    )
    args.update(kw)
    return monthly_breakdown(tariff, WINDOW, **args)


def test_dynamic_annual_mode_prices_exactly_the_entered_kwh():
    # With a DAM price of 1 €/kWh everywhere, energy cost == kWh priced.
    t = {"id": "t", "pricing": "Dynamic", "rates": {"mult": 1, "adder": 0, "damFloor": None}, "fpaSource": "none"}
    bd = _run(t, _peaky_profile(), dam_monthly=[1.0] * 12)
    assert sum(m["energyFull"] for m in bd) == pytest.approx(5000)


def test_dynamic_monthly_mode_prices_the_flat_kwh_each_month():
    t = {"id": "t", "pricing": "Dynamic", "rates": {"mult": 1, "adder": 0, "damFloor": None}, "fpaSource": "none"}
    bd = _run(t, _peaky_profile(), is_monthly=True, monthly_kwh_flat=400, annual_kwh=4800, dam_monthly=[1.0] * 12)
    for m in bd:
        assert m["energyFull"] == pytest.approx(400)


def test_profile_split_sums_to_annual_kwh():
    t = {"id": "t", "pricing": "Fixed", "rates": {"rate": 1.0}, "fpaSource": "none"}
    bd = _run(t, _peaky_profile())
    assert sum(m["energyFull"] for m in bd) == pytest.approx(5000)


def test_tou_half_hour_peak_boundary():
    # Peak 16:30-17:00 only: exactly one of 48 equal slots is peak.
    t = {"id": "t", "pricing": "ToU", "fpaSource": "none", "rates": {
        "hiStart": 0, "hiEnd": 0, "hiPeakStart": 0, "hiPeakEnd": 0,
        "loPeakStart": 16.5, "loPeakEnd": 17, "hiPeakRate": 0, "hiOffRate": 0, "loPeakRate": 1, "loOffRate": 0,
    }}
    bd = _run(t, _flat_profile())
    total_kwh = sum(m["peakKwh"] + m["offPeakKwh"] for m in bd)
    assert total_kwh == pytest.approx(5000)
    assert sum(m["peakKwh"] for m in bd) == pytest.approx(5000 / 48)
