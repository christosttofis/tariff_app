"""Per-tariff customer-togglable discounts. Direct port of getDiscountFactors
in customer.html (~line 1415).

The discount-toggle key convention (f"{tariff_id}_disc_{index}") matches the
existing client-side `window._discountState` shape exactly so no change is
needed on the customer.html side of the discount-toggle UI.
"""


def get_discount_factors(
    tariff_id: str,
    discounts: list[dict],
    month_idx1: int,
    active_overrides: dict | None,
    offers_enabled: bool,
) -> dict:
    if not discounts:
        return {"energyFactor": 1, "standingFactor": 1}
    if not offers_enabled:
        return {"energyFactor": 1, "standingFactor": 1}
    state = active_overrides or {}
    energy_disc = 0.0
    standing_disc = 0.0
    for i, d in enumerate(discounts):
        key = f"{tariff_id}_disc_{i}"
        active = state.get(key) is not False
        if not active:
            continue
        duration = d.get("durationMonths")
        in_period = not duration or month_idx1 <= duration
        if not in_period:
            continue
        if d.get("type") == "energy":
            energy_disc += d.get("percentage") or 0
        elif d.get("type") == "standing":
            standing_disc += d.get("percentage") or 0
    return {
        "energyFactor": max(0, 1 - energy_disc / 100),
        "standingFactor": max(0, 1 - standing_disc / 100),
    }
