"""Derived, curated display data — no JS analogue (customer.html builds this
text inline via the client-side T() translator). This module stops short of
producing translated strings; it returns the same *numbers* customer.html's
calcNote() already displays for Variable tariffs (tier ranges/rates/fixed
charges — already shown to every visitor today, see calcNote() ~line 2120)
so the client can keep formatting them with its own i18n dictionary.
"""


def format_tier_summary(tariff: dict) -> list[dict]:
    r = tariff.get("rates") or {}
    tiers = r.get("tiers") or []
    result = []
    prev = 0
    for tier in tiers:
        up_to = tier.get("upTo")
        result.append({
            "from": prev,
            "upTo": up_to,
            "rate": tier.get("rate") or 0,
            "fixedCharge": tier.get("fixedCharge") or 0,
        })
        prev = up_to if up_to is not None else prev
    return result
