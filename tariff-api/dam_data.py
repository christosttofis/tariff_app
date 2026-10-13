"""
DAM (Day-Ahead Market) dataset helpers shared by the DAM endpoints: the dataset
shape the pricing engine reads, its dates, and how old it is.

build_dam_payload() matches admin.js parseDAM() exactly (same shape, same
arithmetic), so prices entered either way give the same stored data. Change
both together; tests/security/test_12_dam_data.py checks they agree.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

SLOTS_PER_DAY = 48


# ── time ──────────────────────────────────────────────────────────────────────

def _last_sunday(year: int, month: int) -> date:
    d = date(year, month + 1, 1) - timedelta(days=1) if month < 12 else date(year, 12, 31)
    return d - timedelta(days=(d.weekday() + 1) % 7)


def is_dst_change_day(d: date) -> bool:
    """EU clock-change days (last Sunday of March and of October)."""
    return d.month in (3, 10) and d == _last_sunday(d.year, d.month)


def cyprus_now(utc_now: datetime | None = None) -> datetime:
    """Current Cyprus wall-clock time (EET/EEST, EU DST rules), without tzdata."""
    utc_now = utc_now or datetime.now(timezone.utc)
    y = utc_now.year
    dst_start = datetime.combine(_last_sunday(y, 3), datetime.min.time(), timezone.utc) + timedelta(hours=1)
    dst_end = datetime.combine(_last_sunday(y, 10), datetime.min.time(), timezone.utc) + timedelta(hours=1)
    offset = 3 if dst_start <= utc_now < dst_end else 2
    return (utc_now + timedelta(hours=offset)).replace(tzinfo=None)


# ── dataset (same shape and arithmetic as admin.js parseDAM) ─────────────────

def stored_slots(dam_daily_data: list | None) -> dict[str, float]:
    """Flatten stored damDailyData (€/kWh) into {"YYYY-MM-DD HH:MM": price}."""
    out: dict[str, float] = {}
    for month in dam_daily_data or []:
        for day in month or []:
            ds = day.get("dateStr") if isinstance(day, dict) else None
            slots = day.get("slots") if isinstance(day, dict) else None
            if not isinstance(ds, str) or not isinstance(slots, list):
                continue
            for s, price in enumerate(slots[:SLOTS_PER_DAY]):
                if isinstance(price, (int, float)) and not isinstance(price, bool):
                    out[f"{ds} {s // 2:02d}:{30 * (s % 2):02d}"] = float(price)
    return out


def _mean(values: list[float]) -> float | None:
    if not values:
        return None
    total = 0.0
    for v in values:       # plain left-to-right sum, as JS reduce() does
        total += v
    return total / len(values)


def build_dam_payload(slots: dict[str, float]) -> dict:
    """damMonthly / damBySlot / damDailyData / damRowCount from €/kWh slots,
    computed exactly like parseDAM() (rows in date+time order)."""
    month_buckets: list[list[float]] = [[] for _ in range(12)]
    slot_buckets: list[list[list[float]]] = [[[] for _ in range(48)] for _ in range(12)]
    days: dict[str, dict] = {}
    for key in sorted(slots):
        price = slots[key]
        ds = key[:10]
        mi = int(key[5:7]) - 1
        s = int(key[11:13]) * 2 + (1 if int(key[14:16]) >= 30 else 0)
        month_buckets[mi].append(price)
        slot_buckets[mi][s].append(price)
        if ds not in days:
            # JS getDay(): Sunday = 0 … Saturday = 6
            days[ds] = {"dateStr": ds, "month": mi, "dow": (date.fromisoformat(ds).weekday() + 1) % 7,
                        "slots": [None] * SLOTS_PER_DAY}
        days[ds]["slots"][s] = price
    daily: list[list[dict]] = [[] for _ in range(12)]
    for ds in sorted(days):
        daily[days[ds]["month"]].append(days[ds])
    return {
        "damMonthly": [_mean(b) for b in month_buckets],
        "damBySlot": [[_mean(s) for s in month] for month in slot_buckets],
        "damDailyData": daily,
        "damRowCount": len(slots),
    }


def dataset_dates(dam_daily_data: list | None) -> list[str]:
    """Sorted dates that have at least one price."""
    return sorted({
        d["dateStr"] for month in (dam_daily_data or []) for d in (month or [])
        if isinstance(d, dict) and isinstance(d.get("dateStr"), str)
        and any(v is not None for v in (d.get("slots") or []))
    })


# ── status ────────────────────────────────────────────────────────────────────

STALE_AFTER_DAYS = 15


def freshness(dam_daily_data: list | None, now: datetime | None = None) -> dict:
    dates = dataset_dates(dam_daily_data)
    today = (now or cyprus_now()).date()
    if not dates:
        return {"firstDate": None, "lastDate": None, "dayCount": 0, "ageDays": None, "stale": True}
    last = date.fromisoformat(dates[-1])
    age = max((today - last).days, 0)   # data can reach tomorrow
    return {"firstDate": dates[0], "lastDate": dates[-1], "dayCount": len(dates),
            "ageDays": age, "stale": age > STALE_AFTER_DAYS}
