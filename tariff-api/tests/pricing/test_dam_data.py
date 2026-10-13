r"""DAM dataset helpers (dam_data.py): Cyprus time, the dataset built from
half-hourly prices (same as admin.js parseDAM), and how old the data is.

Run from tariff-api/:  .venv\Scripts\python.exe -m pytest tests/pricing
"""

import sys
from datetime import date, datetime, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import dam_data  # noqa: E402


def stored(*days: str, price=0.1):
    return dam_data.build_dam_payload({
        f"{d} {s // 2:02d}:{30 * (s % 2):02d}": price for d in days for s in range(48)
    })["damDailyData"]


def test_cyprus_time_follows_eu_dst():
    assert dam_data.cyprus_now(datetime(2026, 1, 15, 22, 30, tzinfo=timezone.utc)) == datetime(2026, 1, 16, 0, 30)
    assert dam_data.cyprus_now(datetime(2026, 7, 15, 21, 30, tzinfo=timezone.utc)) == datetime(2026, 7, 16, 0, 30)
    assert dam_data.is_dst_change_day(date(2026, 3, 29)) and dam_data.is_dst_change_day(date(2025, 10, 26))
    assert not dam_data.is_dst_change_day(date(2026, 3, 22))


def test_dataset_shape_and_averages():
    slots = {"2026-01-04 00:00": 0.10, "2026-01-04 00:30": 0.20, "2026-01-05 00:00": 0.30,
             "2026-02-01 13:30": 0.40}
    p = dam_data.build_dam_payload(slots)
    assert p["damRowCount"] == 4
    assert p["damMonthly"][0] == pytest.approx(0.2) and p["damMonthly"][1] == pytest.approx(0.4)
    assert p["damMonthly"][2] is None
    assert p["damBySlot"][0][0] == pytest.approx(0.2) and p["damBySlot"][0][1] == pytest.approx(0.2)
    assert p["damBySlot"][1][27] == pytest.approx(0.4)
    jan4 = p["damDailyData"][0][0]
    assert jan4["dateStr"] == "2026-01-04" and jan4["month"] == 0
    assert jan4["dow"] == 0                       # 4 Jan 2026 is a Sunday: JS getDay() = 0
    assert jan4["slots"][:3] == [0.10, 0.20, None]


def test_stored_slots_round_trip():
    p = dam_data.build_dam_payload({"2026-03-01 23:30": 0.5, "2026-03-02 00:00": 0.25})
    assert dam_data.stored_slots(p["damDailyData"]) == {"2026-03-01 23:30": 0.5, "2026-03-02 00:00": 0.25}


def test_freshness():
    daily = stored("2026-09-14", "2026-09-15")
    assert dam_data.freshness(daily, datetime(2026, 9, 30, 12))["stale"] is False    # 15 days
    s = dam_data.freshness(daily, datetime(2026, 10, 1, 12))
    assert s == {"firstDate": "2026-09-14", "lastDate": "2026-09-15", "dayCount": 2, "ageDays": 16, "stale": True}
    assert dam_data.freshness([], datetime(2026, 10, 1))["stale"] is True
