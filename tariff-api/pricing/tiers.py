"""Tiered/block-rate application. Direct port of applyTiers in customer.html
(~line 1339)."""

import math


def apply_tiers(tiers: list[dict], kwh: float) -> float:
    if not tiers or math.isnan(kwh) or kwh <= 0:
        return 0
    cost = 0.0
    prev = 0.0
    for tier in tiers:
        up_to = tier.get("upTo")
        cap = up_to if up_to is not None else math.inf
        band = min(kwh - prev, cap - prev)
        if band <= 0:
            break
        cost += band * (tier.get("rate") or 0)
        prev = cap
        if up_to is None or kwh <= cap:
            break
    return cost
