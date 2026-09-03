"""Half-hourly load-profile (HHFF) math.

Direct port of computeAnnualHHFF/getSlotKwh in customer.html (~lines
1569-1597). `profile_months` is the 12-entry list from a Profile row's
`months` JSON (each entry {W:[48], NW:[48]} or None).
"""


def _slot(arr: list | None, s: int) -> float:
    if not arr or s >= len(arr) or arr[s] is None:
        return 0
    return arr[s]


def compute_annual_hhff(profile_months: list, day_counts: list[dict]) -> float:
    total = 0.0
    for m in range(12):
        pm = profile_months[m] if m < len(profile_months) else None
        if not pm:
            continue
        wd = day_counts[m]["working"]
        nwd = day_counts[m]["nonWorking"]
        w = pm.get("W")
        nw = pm.get("NW")
        for s in range(48):
            total += _slot(w, s) * wd + _slot(nw, s) * nwd
    return total


def get_slot_kwh(profile_months: list, month_idx: int, annual_kwh: float, day_counts: list[dict], annual_hhff: float) -> list[float] | None:
    if not annual_hhff:
        return None
    pm = profile_months[month_idx] if month_idx < len(profile_months) else None
    if not pm:
        return None
    wd = day_counts[month_idx]["working"]
    nwd = day_counts[month_idx]["nonWorking"]
    w = pm.get("W")
    nw = pm.get("NW")
    return [annual_kwh * (_slot(w, s) * wd + _slot(nw, s) * nwd) / annual_hhff for s in range(48)]
