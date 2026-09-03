"""Tariff matching filters — direct port of the filter block inside
applyFilters() in customer.html (~lines 2239-2251)."""


def filter_matching_tariffs(
    tariffs: list[dict],
    voltage: str,
    contracts: list[str],
    pricing_filter: str,
    load_entitlement: str | None,
    vulnerable_eligible: bool,
) -> list[dict]:
    matched = []
    for t in tariffs:
        if t.get("voltage") != voltage:
            continue
        if t.get("contract") not in contracts:
            continue
        if pricing_filter != "All" and t.get("pricing") != pricing_filter:
            continue
        if load_entitlement is not None:
            tle = t.get("loadEntitlement") or "any"
            if tle != "any" and tle != load_entitlement:
                continue
        if t.get("vulnerable") and not vulnerable_eligible:
            continue
        matched.append(t)
    return matched
