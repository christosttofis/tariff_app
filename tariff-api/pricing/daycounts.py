"""Cyprus public holidays, working/non-working day counts, and the
12-month calculation window.

Originally a port of easterDate/getCyprusHolidays/getDayCounts in the old
client-side customer.html code.
"""

import calendar
from datetime import date, timedelta
from functools import lru_cache



def easter_date(year: int) -> date:
    """Orthodox Easter Sunday (Meeus' Julian algorithm, converted to the
    Gregorian calendar; the +13-day offset is valid for 1900-2099).

    The original JS port used the Western (Gregorian) algorithm, which gives
    the wrong date in most years (e.g. 2026-04-05 instead of 2026-04-12)."""
    a = year % 4
    b = year % 7
    c = year % 19
    d = (19 * c + 15) % 30
    e = (2 * a + 4 * b - d + 34) % 7
    month = (d + e + 114) // 31
    day = ((d + e + 114) % 31) + 1
    return date(year, month, day) + timedelta(days=13)


@lru_cache(maxsize=16)
def get_cyprus_holidays(year: int) -> frozenset[str]:
    fixed = [(1, 1), (1, 6), (3, 25), (4, 1), (5, 1), (8, 15), (10, 1), (10, 28), (12, 25), (12, 26)]
    holidays = {f"{year}{mo:02d}{d:02d}" for mo, d in fixed}
    e = easter_date(year)
    # Green Monday, Good Friday, Easter Monday, Kataklysmos (Whit Monday,
    # Easter + 50 — Easter + 49 is Pentecost Sunday, already a weekend day).
    for offset in (-48, -2, 1, 50):
        dt = e + timedelta(days=offset)
        holidays.add(f"{dt.year}{dt.month:02d}{dt.day:02d}")
    return frozenset(holidays)


def calc_window(today: date) -> list[tuple[int, int]]:
    """The 12 months every cost estimate covers: (year, month index 0-11)
    pairs, starting with the month after `today` — i.e. the customer's first
    year after switching, so time-limited offers land on the right months."""
    start = today.year * 12 + today.month   # today.month is 1-based -> next month
    return [(k // 12, k % 12) for k in range(start, start + 12)]


def is_non_working(d: date) -> bool:
    return d.weekday() >= 5 or d.strftime("%Y%m%d") in get_cyprus_holidays(d.year)


def get_window_day_counts(window: list[tuple[int, int]]) -> list[dict]:
    """Working/non-working day counts for each (year, month index) of a window."""
    result = []
    for year, mi in window:
        dim = calendar.monthrange(year, mi + 1)[1]
        non_working = sum(is_non_working(date(year, mi + 1, d)) for d in range(1, dim + 1))
        result.append({"working": dim - non_working, "nonWorking": non_working})
    return result
