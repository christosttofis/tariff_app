# Tariff Calculation Reference

This document is the source of truth for **how each tariff type's cost is calculated** on the customer page (`customer.html`), for both Annual and Monthly input modes, plus the charges common to all tariff types (regulated costs, FPA, discounts).

> **Maintenance rule:** every time the calculation logic changes in `customer.html` (or is added for a new tariff type), this file must be updated in the same change. If a change and this doc ever disagree, the code is not "done" until the doc is fixed too.

Current live calculation logic lives in `customer.html`, primarily in:
- `monthlyBreakdown(t, dc)` — the actual per-month cost engine used everywhere (both modes, all 4 pricing types)
- `annualCostForTariff(t, dc)` — sums `monthlyBreakdown`'s 12 months into one annual/period total
- Helpers: `computeAnnualHHFF`, `getSlotKwh`, `getDiscountFactors`, `getTariffFpa`, `regulatedAnnual` / `regulatedBreakdown`, `applyTiers`, `getCyprusHolidays`, `getDayCounts`

All tariffs share a load **profile** (`profileId` → `cfg.profiles`), which defines a half-hourly (48 slots/day, 30-min each) consumption shape (HHFF — half-hour flow factor) per calendar month, split into a **Working Day (W)** shape and a **Non-Working Day (NW)** shape. Non-working days = Saturdays, Sundays, and Cyprus public holidays (computed via `getCyprusHolidays`, including Orthodox Easter-relative dates). Calculations run against a fixed reference year, `CALC_YEAR = 2026`, used only to get correct day-of-week/holiday counts per month.

---

## Annual mode calculations

In Annual mode the customer enters one **annual kWh** figure. Each tariff's profile is used to distribute that annual figure across the 12 calendar months, and — where the tariff needs intra-day granularity (ToU, Dynamic) — further across the 48 half-hourly slots of each day, weighted by working/non-working day shape and actual day counts for `CALC_YEAR`.

### Fixed tariffs
- Monthly kWh (`mKwhForMonth`) = annual kWh distributed across the month in proportion to that month's share of the profile's annual HHFF total (`computeAnnualHHFF`), i.e. months with a "heavier" profile shape get proportionally more kWh, not a flat 1/12 split.
- Energy cost for the month = monthly kWh × tariff's flat `rate`.
- No time-of-day pricing is applied — the profile only affects the *monthly* split, not intra-day.

### ToU (Time of Use) tariffs
- Uses `getSlotKwh` to distribute the month's HHFF-weighted kWh across all 48 half-hourly slots (via `computeAnnualHHFF` normalisation), using the correct working/non-working shape per slot.
- Each tariff month is tagged "high season" or "low season" (`hiStart`/`hiEnd` months vs the rest), each with its own peak window (`hiPeakStart/End` or `loPeakStart/End`) and peak/off-peak rates.
- For each slot: if the slot's start hour falls inside the season's peak window → peak rate; else → off-peak rate. Energy cost = Σ(slot kWh × applicable rate).
- If the tariff has no profile assigned, falls back to a simple day-fraction split: `peak_fraction = (peak hours)/24`, `energy = kWh×peak_fraction×peakRate + kWh×(1-peak_fraction)×offRate`.

### Dynamic tariffs
- Requires a profile — no profile means the tariff is excluded (`return null`).
- For every **actual day** of the month (`dims[m]` days, leap-year aware for February), and every one of the 48 half-hourly slots that day:
  - Slot kWh = annual kWh × (that slot's HHFF value for the day's working/non-working shape) ÷ annual HHFF total (`annualHHFF`) — i.e. full-year normalisation, same as ToU.
  - Slot's DAM price is looked up with this fallback order: **exact date + slot actual price** (`damDailyData`, current `CALC_YEAR`) → **the same date+slot one year earlier** (`CALC_YEAR-1`, same `damDailyData` bucket — daily data is bucketed by calendar month only, not year, so prior-year dates live in the same array) → **that month's half-hourly slot average** (`damBySlot`) → **that month's flat DAM average** (`damMonthly`). If none exist for that month, the tariff is excluded for the whole calculation (`return null`).
  - Effective price = `max(damPrice, damFloor) × mult + adder` (tariff-specific floor/multiplier/adder from `t.rates`).
  - Energy cost += slot kWh × effective price, summed across every slot of every day in the month.

### Variable tariffs
- Rates are **tiered/block** (`rates.tiers`: `{upTo, rate, fixedCharge}` bands) and reset every `resetMonths` (e.g. every 1, 2, 3… months — a "period").
- For each period: total period kWh = sum of that period's months' HHFF-distributed kWh (`mKwhForMonth`), tiered cost computed via `applyTiers` (cumulative block pricing, not a flat rate on the whole tier).
- Any tier's fixed charge (`fixedCharge`) is included once per period if that tier was reached, then split evenly across the months in the period and added to standing charge.
- Energy/FPA/fixed-charge totals for the period are split evenly across the months in that period (not weighted by month).

---

## Monthly mode calculations

In Monthly mode the customer enters a flat **per-bill kWh** figure (`monthly-kwh` ÷ `_billingPeriod`, since billing can be monthly or bi-monthly). Unlike Annual mode, **every month uses the exact same flat kWh** — there is no annual-total redistribution across months. The ranking/total shown still sums all 12 months of `CALC_YEAR`, each priced with that month's real profile shape and DAM data, so the *total* reflects 12 months of "what if every bill were this many kWh," not a single month's bill.

Because of this simplification, once the customer enters a value the UI shows a note (`#monthly-calc-note`, `MONTHLY_CALC_NOTE` translation key, populated in `updateMonthlyCalcNote()`) reading roughly "This calculation is based on your consumption for the current month of `<Month>`. For more accurate results, please use the annual calculator." — steering users with seasonal usage patterns toward the Annual mode.

### Fixed tariffs
- Monthly kWh = the flat input value, used as-is for all 12 months (`mKwhForMonth` returns `monthlyKwhFlat` directly — no profile-based redistribution across months).
- Energy cost = monthly kWh × tariff's flat `rate`. Profile is not used at all for Fixed.

### ToU tariffs
- Profile is **not** used to redistribute across months (every month = same flat kWh), but *is* used for intra-day split only if annual mode; in monthly mode ToU actually falls back to the simple day-fraction split (`peak_fraction = peakHours/24`) rather than half-hourly slots, since the `slots` branch is only taken `!isMonthly && prof`. So Monthly-mode ToU is always the fraction-based peak/off-peak split, regardless of whether a profile is assigned.

### Dynamic tariffs
- Requires a profile — no profile means the tariff is excluded.
- For every actual day of the month, every one of the 48 half-hourly slots:
  - Slot kWh = flat monthly kWh × (slot's HHFF value for that day's working/non-working shape) ÷ **that month's own HHFF total** (`mHHFF`, not the annual total) — i.e. normalised within-month, so the sum of all slots in the month equals the flat monthly kWh exactly.
  - DAM price lookup and floor/mult/adder application are identical to Annual mode (exact date+slot → month slot average → month flat average → exclude if none).
- Net effect: same "break the bill into ~1,344–1,488 half-hour periods (28–31 days × 48 slots) and price each against that period's real DAM price" approach the annual mode uses, just with a fixed flat kWh per month instead of an HHFF-weighted annual split.

### Variable tariffs
- Same tiered logic as Annual mode, except every month's kWh input into the period total is the flat monthly kWh (via `mKwhForMonth`) instead of an HHFF-weighted annual split.

---

## Common calculations (applied to all tariff types)

### FPA (Fuel & Purchased-power Adjustment)
- `getTariffFpa(t)`: per-kWh charge added to every unit of energy, on top of the tariff's own rate.
- Source is per-tariff (`t.fpaSource`): `'none'` → €0; `'custom'` → tariff's own `fpaCustom` rate; `'global'` (default) → the regulated global rate matching the tariff's voltage level (`fpaLV`/`fpaMV`/`fpaHV` from `cfg.regulated`).
- Applied as `monthly/period kWh × fpaRate`, subject to the same energy discount factor as the tariff's own energy cost.
- In the UI, FPA is shown as a clickable label ("FPA"/"ΑΤΚ" where space is tight, e.g. the per-tariff monthly table header; full text "Fuel price adjustment"/"Αναπροσαρμογή τιμής καυσίμου" where space allows, e.g. the per-bill breakdown) with an "ℹ" icon that opens the same info-popup mechanism used for regulated charges (`openRegInfo('FPA_FULL','FPA_DESC')`), rather than a hover-only tooltip. The label also shows that tariff's actual FPA rate in parentheses (e.g. "FPA (€0.0350/kWh)") instead of a "(custom)"/"(προσαρμοσμένο)" marker — the rate itself tells the customer whether it differs from the regulated default.

### Discounts
- `getDiscountFactors(t, monthIdx1)` returns an `energyFactor` and `standingFactor` (1.0 = no discount) for a given calendar month (1-indexed).
- Each tariff can have multiple discounts (`t.discounts[]`), each with a `type` (`'energy'` or `'standing'`), a `percentage`, and an optional `durationMonths` (discount only applies to the first N months of the tariff, from month index 1).
- Customers can toggle individual discounts off in the UI (`window._discountState`); toggled-off discounts are excluded from the factor calculation for that tariff.
- Multiple active discounts of the same type stack additively (percentages summed, then floored at 0% remaining — i.e. cannot go negative).
- `annualCostNoDiscount(t, dc)` recomputes the full breakdown with all discounts forced off, to show the "full price" (strikethrough) alongside the discounted price.

### Regulated charges (network/PSO/RES/MDM)
- Not part of the supplier ranking/comparison — always shown as a separate line item, added on top of the supplier's own cost.
- `regulatedAnnual(voltage, annualKwh, mdm)` returns `regulatedBreakdown(...).total`: `annualKwh × (gridRate + psoRate + resRate) + mdm × 12`.
  - `gridRate` = network charge, selected by voltage level (`lv`/`mv`/`hv` from `cfg.regulated`).
  - `pso` = Public Service Obligation levy (per kWh, flat across voltage levels).
  - `res` = RES & Energy Conservation Fund levy (per kWh, flat across voltage levels).
  - `mdm` = Meter Data Management, a **fixed monthly** charge (not per-kWh) that is tariff-specific (`t.mdm`), annualised ×12.
- `regulatedBreakdown(...)` is the single source of truth for these figures — it computes the same total plus individually labelled rows (Grid / PSO / RES / MDM) for the itemised bill view; `regulatedAnnual` is a thin wrapper so the two never drift apart.
- Regulated charges are **not** discounted — the discount system only applies to the supplier's own energy/standing charges.
- Each regulated row's label is clickable (`openRegInfo`, same info-popup mechanism as FPA) and shows its rate in parentheses next to the label — €/kWh for Grid/PSO/RES, a flat €/month figure (via `LBL_FIXED_ROW`) for MDM. This applies in both the annual ranked-list breakdown and the monthly single-bill breakdown.

### Standing charge
- Flat, tariff-specific monthly fee (`t.standing`), added once per month regardless of consumption.
- Subject to the tariff's `standingFactor` discount (if any `type: 'standing'` discount is active and in-period).
- For Variable tariffs, any reached tier's `fixedCharge` is folded into "standing" (for discount-eligibility purposes) rather than kept separate.
- The annual/ranked-list breakdown table always derives its displayed "Standing" total by summing each month's already-discounted `monthlyBreakdown(...).standing` (`moBd.reduce(...)`) — never `t.standing×12` — so the row's Energy+FPA+Standing always foots to the same total shown in the Total column, even when a standing discount is active. (Prior to 2026-07-17 the annual table used `t.standing×12` for all non-Variable pricing types, which silently ignored standing discounts in the displayed breakdown while the ranked total itself was already correct — a display-only bug, now fixed.)

---

## Adding a new tariff type or changing a calculation

When adding a new pricing type or changing how an existing one works:
1. Update `monthlyBreakdown(t, dc)` (and, if the Annual/Monthly split differs meaningfully, keep the `isMonthly` branch logic consistent with the pattern above).
2. Add a new chapter to both the **Annual mode** and **Monthly mode** sections above, following the same structure (source of monthly kWh → intra-day/slot logic → price lookup/formula).
3. If the change affects FPA, discounts, or regulated-charge treatment, update the **Common calculations** section too.
4. Consider whether the change should also be surfaced to customers — e.g. via a notice (`cfg.notices` / `assumptions_en` shown on the customer page) or a per-supplier explanatory field on the supplier admin page — so the assumptions are visible to end users, not just documented here internally.
