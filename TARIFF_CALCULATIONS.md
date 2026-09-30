# Tariff Calculation Reference

This document is the source of truth for **how each tariff type's cost is calculated** for the public customer calculator (`customer.html`), for both Annual and Monthly input modes, plus the charges common to all tariff types (regulated costs, FPA, discounts).

> **Maintenance rule:** every time the calculation logic changes (or is added for a new tariff type), this file must be updated in the same change. If a change and this doc ever disagree, the code is not "done" until the doc is fixed too.

**As of the customer-data-exposure fix (see `SECURITY_REMEDIATION_PLAN_customer_data_exposure.md`), calculation runs server-side**, not in `customer.html` JS — `customer.html` sends the customer's inputs to `POST /api/public/calculate` / `POST /api/public/sample-invoice` and renders whatever comes back. This was a direct, numerically-verified port (see that plan's Phase 1); the formulas described below are unchanged, only their location moved. Current live calculation logic lives in `tariff-api/pricing/`, primarily in:
- `pricing/engine.py: monthly_breakdown(...)` — the actual per-month cost engine used everywhere (both modes, all 4 pricing types)
- `pricing/engine.py: annual_cost_for_tariff(...)` — sums `monthly_breakdown`'s 12 months into one annual/period total
- Helpers: `pricing/profiles.py` (`compute_annual_hhff`, `get_slot_kwh`), `pricing/discounts.py` (`get_discount_factors`), `pricing/regulated.py` (`get_tariff_fpa`, `regulated_breakdown`), `pricing/tiers.py` (`apply_tiers`), `pricing/daycounts.py` (`get_cyprus_holidays`, `get_day_counts`)
- Orchestration (loading tariffs/profiles/regulated rates/DAM data from the DB and calling the above): `tariff-api/routers/public_calc.py`

All tariffs share a load **profile** (a `Profile` DB row, referenced by `profileId`), which defines a half-hourly (48 slots/day, 30-min each) consumption shape (HHFF — half-hour flow factor) per calendar month, split into a **Working Day (W)** shape and a **Non-Working Day (NW)** shape. Non-working days = Saturdays, Sundays, and Cyprus public holidays (computed via `get_cyprus_holidays`, including Orthodox Easter-relative dates). The Dynamic-pricing day-loop runs against a fixed reference year, `CALC_YEAR = 2026` (`pricing/engine.py`), used only to get correct day-of-week/holiday counts per month.

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
- Source is per-tariff (`t.fpaSource`): `'none'` → €0; `'custom'` → tariff's own `fpaCustom` rate; `'global'` (default) → the regulated global rate matching the tariff's voltage level (`fpaLV`/`fpaMV`/`fpaHV` from the Regulated DB row (loaded via `pricing/regulated.py: get_regulated_rates`)).
- Applied as `monthly/period kWh × fpaRate`, subject to the same energy discount factor as the tariff's own energy cost.
- In the UI, FPA is shown as a clickable label ("FPA"/"ΑΤΚ" where space is tight, e.g. the per-tariff monthly table header; full text "Fuel price adjustment"/"Αναπροσαρμογή τιμής καυσίμου" where space allows, e.g. the per-bill breakdown) with an "ℹ" icon that opens the same info-popup mechanism used for regulated charges (`openRegInfo('FPA_FULL','FPA_DESC')`), rather than a hover-only tooltip. The label also shows that tariff's actual FPA rate in parentheses (e.g. "FPA (€0.0350/kWh)") instead of a "(custom)"/"(προσαρμοσμένο)" marker — the rate itself tells the customer whether it differs from the regulated default.

### Discounts
- `getDiscountFactors(t, monthIdx1)` returns an `energyFactor` and `standingFactor` (1.0 = no discount) for a given calendar month (1-indexed).
- Each tariff can have multiple discounts (`t.discounts[]`), each with a `type` (`'energy'` or `'standing'`), a `percentage`, and an optional `durationMonths` (discount only applies to the first N months of the tariff, from month index 1).
- Customers can toggle individual discounts off in the UI (`window._discountState`); toggled-off discounts are excluded from the factor calculation for that tariff.
- Multiple active discounts of the same type stack additively (percentages summed, then floored at 0% remaining — i.e. cannot go negative).
- `annualCostNoDiscount(t, dc)` recomputes the full breakdown with all discounts forced off, to show the "full price" (strikethrough) alongside the discounted price.
- Discount data format (enforced server-side since 2026-09-30, `schemas.DiscountIn`): `{type: 'energy'|'standing', percentage: >0–100, durationMonths: 1–120 | null, conditions: string}`. Both the admin editor and the supplier portal save this shape. The supplier portal previously saved `{label, pct, euro}`, which the engine ignored.

### Input validation and failure isolation
- Every tariff's `rates`, `discounts` and charges are validated on save against a per-pricing-type schema (`schemas.py`: `FixedRatesIn`, `TouRatesIn`, `DynamicRatesIn`, `VariableRatesIn`, `DiscountIn`). The engine can therefore assume numeric, finite, in-range values. Limits are listed in `ADMIN_MANUAL.md` §6.10.
- As a safety net, `/api/public/calculate` prices each tariff independently: if the engine raises for one tariff, or returns a non-finite total, that tariff is skipped and logged, and the rest of the comparison is still returned.

### Regulated charges (network/PSO/RES) & MDM
- Not part of the supplier ranking/comparison — always shown as a separate line item, added on top of the supplier's own cost. Labelled to the customer as **"additional charges"**, not "regulated charges" — MDM (below) is not always actually CERA-regulated, so the old wording overclaimed.
- `regulatedAnnual(voltage, annualKwh, mdm, mdmInvoiceMonths, mdmRegulated)` returns `regulatedBreakdown(...).total`: `annualKwh × (gridRate + psoRate + resRate) + mdm × (12/mdmInvoiceMonths)`.
  - `gridRate` = network charge, selected by voltage level (`lv`/`mv`/`hv` from the Regulated DB row (loaded via `pricing/regulated.py: get_regulated_rates`)).
  - `pso` = Public Service Obligation levy (per kWh, flat across voltage levels).
  - `res` = RES & Energy Conservation Fund levy (per kWh, flat across voltage levels).
  - `mdm` = Meter Data Management, a charge **per invoice** (not per kWh, and not always monthly) — see below.
- `regulated_breakdown(...)` is the single source of truth for these figures — it computes the same total plus individually labelled rows (Grid / PSO / RES / MDM) for the itemised bill view; (there is no separate wrapper function server-side — the route handler reads `regulated_breakdown(...)["total"]` directly). Each row also carries a `regulated: true/false` flag (Grid/PSO/RES are always `true`; MDM depends on sourcing below) used purely for display.

#### MDM sourcing — regulated vs. supplier-set
- Suppliers can be flagged `regulated` (`cfg.suppliers[].regulated`, e.g. EAC) — orthogonal to a tariff's Domestic/Commercial/Industrial contract type.
- `mdm_for_tariff(tariff, supplier_regulated, regulated_rates)` decides the €/invoice value: **regulated supplier** → always the CERA-set global rate (the Regulated DB row's `mdm` field), ignoring the tariff's own `mdm` field entirely; **non-regulated supplier** → the tariff's own `t.mdm` (admin/supplier-entered, freely editable). There is deliberately no way for a non-regulated supplier to opt into the regulated rate.
- This also drives display: a regulated MDM row is coloured/labelled like Grid/PSO/RES (blue, "Meter Data Management (MDM)", `REG_MDM_DESC` info text). A non-regulated MDM row uses the supplier-charge colour (`var(--text2)`, same as Energy/Standing), the `MDM_SUPPLIER` label and `MDM_SUPPLIER_DESC` info text, explicitly stating it's a competitive charge, not a regulated one. The Standing row/header carries the same "competitive charge" info text (`STANDING_DESC`) for the same reason — it is always supplier-set, never regulated.

#### MDM invoicing frequency
- MDM is charged **once per invoice**, not once per calendar month. `t.mdmInvoiceMonths` (`1` = monthly, `2` = bimonthly; set per tariff by the admin/supplier, defaults to `2`) gives invoices/year = `12 / mdmInvoiceMonths`, and `annual MDM = mdm × invoices/year` — **not** a flat `× 12`. E.g. a €0.94 bimonthly charge totals €5.64/year, not €11.28/year as a naive ×12 would give.
- Displayed rate text is deliberately short — `€{N} / λογαριασμό` / `€{N} / invoice` (`LBL_FIXED_ROW_MDM`), no frequency inline, to avoid widening the breakdown table's columns. The actual frequency is only in the `title` hover tooltip (`MDM_BILLED_MONTHLY` / `MDM_BILLED_BIMONTHLY`).

- Regulated/additional charges are **not** discounted — the discount system only applies to the supplier's own energy/standing charges.
- Each row's label is clickable (`openRegInfo`, same info-popup mechanism as FPA) — €/kWh for Grid/PSO/RES, a flat €/invoice figure for MDM. This applies in both the annual ranked-list breakdown and the monthly single-bill breakdown.

### Standing charge
- Flat, tariff-specific monthly fee (`t.standing`), added once per month regardless of consumption. Always supplier-set/competitive, never regulated — its label carries an info tooltip (`STANDING_DESC`) saying so, same treatment as a non-regulated MDM row.
- Subject to the tariff's `standingFactor` discount (if any `type: 'standing'` discount is active and in-period).
- For Variable tariffs, any reached tier's `fixedCharge` is folded into "standing" (for discount-eligibility purposes) rather than kept separate.
- The annual/ranked-list breakdown table always derives its displayed "Standing" total by summing each month's already-discounted `monthlyBreakdown(...).standing` (`moBd.reduce(...)`) — never `t.standing×12` — so the row's Energy+FPA+Standing always foots to the same total shown in the Total column, even when a standing discount is active. (Prior to 2026-07-17 the annual table used `t.standing×12` for all non-Variable pricing types, which silently ignored standing discounts in the displayed breakdown while the ranked total itself was already correct — a display-only bug, now fixed.)

---

## Sample invoice (admin-togglable customer feature)

An optional "Sample invoice" view (`openSampleInvoice` in customer.html, which fetches `pricing/invoice.py: build_sample_invoice_data` via POST /api/public/sample-invoice) lets a customer see a bill-styled breakdown for a tariff, explained line by line. It is admin-controlled — `cfg.sampleInvoiceEnabled` (from a single-row `sample_invoice_config` DB table, defaults to off) gates whether the button/modal render at all — and introduces no new pricing logic: it only re-presents numbers already produced by `monthlyBreakdown`/`regulated_breakdown`, plus two additions specific to this illustrative view:

- **Which period is shown:** not a 12-month average. Monthly input mode shows the customer's own chosen billing cycle — `_billingPeriod` (the Monthly/Bi-monthly toggle next to the "consumption per bill" field, 1 or 2 months), since that's literally what the entered kWh figure represents. Annual input mode shows the tariff's own invoicing cadence (`t.mdmInvoiceMonths`, default 2) instead, since there's no billing-cycle input to read in that mode. Either way, the period is counted back from today's real-world month — e.g. a bimonthly period shows the last two calendar months summed from `monthly_breakdown`'s per-month `energy`/`fpa`/`standing` (not divided evenly), so it reflects that period's actual HHFF-weighted consumption. Grid/PSO/RES/MDM are taken from `regulated_breakdown`'s annual figures scaled by `periodMonths/12`, the same "annual ÷ 12 × period" convention already used for the existing monthly-mode bill breakdown table — not a new calculation path.
- **VAT:** the tool is otherwise entirely ex-VAT everywhere else (see "Regulated charges" above). The sample invoice is the one place VAT is shown, purely for realism, mirroring the EAC bill example: Cyprus standard 19% is applied to (energy + FPA + standing + grid + PSO + MDM); RES & ES Fund is added afterwards, untaxed — same ordering as the real EAC bill's "Total subject to VAT" → "+ RES & ES Fund" → "+ VAT" flow. This is purely a display computation local to `build_sample_invoice_data`; it does not feed back into the comparison ranking or any other total shown elsewhere.

If a tariff has no cost data for the chosen period (e.g. a Dynamic tariff missing DAM data), `build_sample_invoice_data` returns `null` and the button is simply omitted for that tariff — no error state, no fallback calculation.

The view is laid out like a real bill (customer/account/meter info block, itemised charges, highlighted amount due) to make the numbers easier to relate to an actual EAC bill. Everything identifying a "customer" is a fixed placeholder (`SAMPLE_INV_EX_NAME`/`SAMPLE_INV_EX_ADDRESS`/`SAMPLE_INV_EX_ACCOUNT`/`SAMPLE_INV_EX_METER` translation keys) — never real data, since the tool has no customer accounts. (An earlier version also showed a fabricated "same period last year" comparison with a small chart; this was removed since the tool holds no real metering history to compare against.)

Each charge row also shows its "qty × rate" calculation underneath the label (`.invoice-calc`, e.g. `1,633 kWh × €0.1035/kWh`), matching the EAC bill's `{1.633 kWh x €0,1035}` notation, computed in `build_sample_invoice_data`:
- **Energy**: for **Fixed** tariffs, one row (`energyRate = energyFull / periodKwh`, equal to the tariff's own configured rate). For **ToU** tariffs, split into two rows — **Peak** and **Off-Peak** — each with its own real `kWh × rate` line: `monthly_breakdown` (engine.py) now tags every 30-min slot (or, in monthly-flat input mode, the peak-hours fraction of the month) as peak or off-peak using that month's `hi`/`loPeakStart`/`End` window, accumulating `peakKwh`/`offPeakKwh` and `peakEnergy`/`offPeakEnergy` (discounted) plus `...Full` (undiscounted) alongside the existing blended `energy` total; `build_sample_invoice_data` sums these across the invoice period and derives `peakRate`/`offPeakRate` as `energyFull / kwh` per bucket. Dynamic/Variable tariffs still charge a different rate per time slot/tier with no fixed per-bucket rate to show, so the formula line is omitted for those (the energy total itself is still shown, just without a "qty × rate" underneath).
- **FPA/Grid/PSO/RES**: straightforward `periodKwh × rate`, using each charge's real fixed per-kWh rate.
- **Standing**: `t.standing/mo × monthsCount` (the tariff's base monthly fee).
- **MDM**: `mdmRate € × mdmInvoices`, where `mdmInvoices = monthsCount / (t.mdmInvoiceMonths||2)` — equals exactly 1 whenever the period was sized to the tariff's own invoicing cadence (always true in Annual mode by construction); can be fractional in Monthly mode if the tariff's real cadence differs from the single-month sample period.

**Discounted rows show both figures.** Energy/FPA/Standing formulas above are all built from the *pre-discount* rate/qty, so they reconcile to `energyFull`/`fpaFull`/`standingFull` (summed from `monthly_breakdown`'s `*Full` fields) — not to the actual (post-discount) `energy`/`fpa`/`standing` totals when a discount is active on that tariff. Rather than show a formula whose arithmetic doesn't match the printed total (e.g. "€4.00/mo × 2" next to €7.60 instead of €8.00 — the bug this note replaced), the row displays both: the pre-discount amount struck through, then the actual amount due, the same convention already used in the ranked comparison list elsewhere on this page. Grid/PSO/RES/MDM are never discounted (see "Regulated charges" above), so their formulas always reconcile exactly as-is.

**Competitive vs. regulated grouping.** Rows are split into two sections, matching the distinction used everywhere else in this tool (see "Regulated charges" above): a **Competitive charges** section (Energy, FPA, Standing) and a **Regulated charges** section (Grid, PSO). MDM is placed into whichever section actually reflects who set the rate — `mdmRegulated` (from `mdmForTariff()`/`supplier.regulated`) decides: a regulated supplier (e.g. EAC) uses the CERA-set MDM rate, so it belongs with the regulated section; otherwise it's the supplier's own competitive metering charge. Each section has its own subtotal (`competitiveTotal`, `regulatedTotal`); their sum is `vatBase`, shown as "Total subject to VAT" — unchanged from the underlying calculation, just relabelled/regrouped for display.

**RES & ES Fund is shown on its own, after both sections**, since — unlike every other regulated charge — it is *not* subject to VAT (`res` is added to `vatBase` only after the VAT rate is applied, per the VAT rule above). This also fixed a pre-existing wording bug in the regulated-charge info popups: `REG_PSO_DESC` previously claimed PSO was not subject to VAT (wrong — PSO *is* taxed, it's part of `vatBase`) while `REG_RES_DESC` didn't mention VAT at all (it should have, since RES is the one that's actually exempt). Both descriptions now state the correct VAT treatment.

---

## Adding a new tariff type or changing a calculation

When adding a new pricing type or changing how an existing one works:
1. Update `monthly_breakdown(tariff, dc, ...)` (and, if the Annual/Monthly split differs meaningfully, keep the `isMonthly` branch logic consistent with the pattern above).
2. Add a new chapter to both the **Annual mode** and **Monthly mode** sections above, following the same structure (source of monthly kWh → intra-day/slot logic → price lookup/formula).
3. If the change affects FPA, discounts, or regulated-charge treatment, update the **Common calculations** section too.
3a. Add or update the matching rates schema in `tariff-api/schemas.py` (`_RATES_MODEL`). Otherwise the new fields are rejected or silently dropped on save.
4. Consider whether the change should also be surfaced to customers — e.g. via a notice (`cfg.notices` / `assumptions_en` shown on the customer page) or a per-supplier explanatory field on the supplier admin page — so the assumptions are visible to end users, not just documented here internally.
