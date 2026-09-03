"""Cyprus public holidays and working/non-working day counts.

Direct port of easterDate/getCyprusHolidays/getDayCounts in customer.html
(~lines 1303-1328).
"""

from datetime import date, timedelta

DAYS_IN_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def easter_date(year: int) -> date:
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)


def get_cyprus_holidays(year: int) -> set[str]:
    fixed = [(1, 1), (1, 6), (3, 25), (4, 1), (5, 1), (8, 15), (10, 1), (10, 28), (12, 25), (12, 26)]
    holidays = {f"{year}{mo:02d}{d:02d}" for mo, d in fixed}
    e = easter_date(year)
    for offset in (-48, -2, 1, 49):
        dt = e + timedelta(days=offset)
        holidays.add(f"{dt.year}{dt.month:02d}{dt.day:02d}")
    return holidays


def _js_day_of_week(d: date) -> int:
    """JS Date.getDay(): Sunday=0 .. Saturday=6, vs Python's Monday=0..Sunday=6."""
    return (d.weekday() + 1) % 7


def get_day_counts(year: int) -> list[dict]:
    holidays = get_cyprus_holidays(year)
    is_leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    result = []
    for mi in range(12):
        dim = 29 if (mi == 1 and is_leap) else DAYS_IN_MONTH[mi]
        working = non_working = 0
        for d in range(1, dim + 1):
            dow = _js_day_of_week(date(year, mi + 1, d))
            key = f"{year}{mi + 1:02d}{d:02d}"
            if dow == 0 or dow == 6 or key in holidays:
                non_working += 1
            else:
                working += 1
        result.append({"working": working, "nonWorking": non_working})
    return result
