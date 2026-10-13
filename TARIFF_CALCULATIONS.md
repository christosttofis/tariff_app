# Tariff Calculation Reference

This document is the source of truth for **how each tariff type's cost is calculated** for the public customer calculator (customer page), for both Annual and Monthly input modes, plus the charges common to all tariff types (regulated costs, FPA, discounts).

> **Maintenance rule:** every time the calculation logic changes (or is added for a new tariff type), this file must be updated in the same change. If a change and this doc ever disagree, the code is not "done" until the doc is fixed too.

**All calculation runs server-side** (since 2026-09-03, as part of the customer-data-exposure fix — see `SECURITY_REMEDIATION_PLAN_customer_data_exposure.md`). The customer page (`customer.js`) only sends the customer's inputs to `POST /api/public/calculate` / `POST /api/public/sample-invoice` and renders what comes back; it contains no pricing formulas. The engine was originally a direct, numerically-verified port of the earlier client-side JS. Function and variable names below are the Python ones in `tariff-api/pricing/`:
- `pricing/engine.py: monthly_breakdown(...)` — the per-month cost engine used everywhere (both modes, all 4 pricing types); inner helper `m_kwh_for_month(i)` gives each month's kWh
- `pricing/engine.py: annual_cost_for_tariff(...)` — sums `monthly_breakdown`'s 12 months into one annual total; `annual_cost_no_discount(...)` does the same with every discount switched off; `offer_summary(...)` — the "after the offer ends" figure (see Discounts)
- `pricing/engine.py: monthly_kwh_display(...)` — the per-month kWh figures shown to the customer (same split as `m_kwh_for_month`)
- Helpers: `pricing/profiles.py` (`compute_annual_hhff`, `get_slot_kwh`), `pricing/discounts.py` (`get_discount_factors`), `pricing/regulated.py` (`get_regulated_rates`, `get_tariff_fpa`, `mdm_for_tariff`, `regulated_breakdown`), `pricing/tiers.py` (`apply_tiers`), `pricing/daycounts.py` (`calc_window`, `get_window_day_counts`, `is_non_working`, `easter_date`, `get_cyprus_holidays`), `pricing/invoice.py` (`build_sample_invoice_data`)
- Orchestration (loading tariffs/profiles/regulated rates/DAM data from the DB and calling the above): `tariff-api/routers/public_calc.py`
- Tests: `tariff-api/tests/pricing/`
- **Admin audit calculator** (`admin.js`: `runAudit`, `runAuditVariable` and the `audit*` helpers): a deliberately *independent* JavaScript re-implementation of the same rules, showing every half-hour slot of one window month (or every billing period for Variable). It must be kept in step with the engine: after each run it calls `POST /api/public/calculate` (Annual mode, all offers on) and shows whether the customer page gives the same figure (`auditCrossCheck`, tolerance €0.005). Checked 2026-10-09 on the demo data: 41 of 41 cases matched.

All tariffs share a load **profile** (a `Profile` DB row, referenced by `profileId`), which defines a half-hourly (48 slots/day, 30-min each) consumption shape (HHFF — half-hour flow factor) per calendar month, split into a **Working Day (W)** shape and a **Non-Working Day (NW)** shape. Non-working days = Saturdays, Sundays, and Cyprus public holidays (`get_cyprus_holidays`): 10 fixed dates (1 Jan, 6 Jan, 25 Mar, 1 Apr, 1 May, 15 Aug, 1 Oct, 28 Oct, 25 Dec, 26 Dec) plus 4 dates relative to **Orthodox** Easter (`easter_date`): Green Monday (−48 days), Good Friday (−2), Easter Monday (+1) and Kataklysmos/Whit Monday (+50).

### The 12-month window (since 2026-10-09)

Every estimate covers **the customer's first 12 months after switching**: the 12 calendar months starting with the month after today (Cyprus time, `Europe/Nicosia`), e.g. a calculation on 9 Oct 2026 covers Nov 2026 – Oct 2027. `calc_window(today)` returns these as 12 `(year, month index 0–11)` pairs; `public_calc.py` builds it per request and returns it to the page as `window: [{year, month 1–12}, …]`.

- **Every per-month list is in window order**, not January–December: input arrays stored per calendar month (profile months, `damBySlot`, `damMonthly`, `damDailyData`) are reordered into window order first, and every per-month output (`months`, `moKwh`) has index 0 = first month after switching. The customer page labels months from `window` (e.g. "Nov '26").
- **Day counts come from the window itself** (`get_window_day_counts(window)`, computed inside the engine — callers pass only the window), so each month uses its own year's weekends, holidays and February length, and the Dynamic day loop always uses the same days as the HHFF normalisation.
- **Why:** time-limited offers are applied from the first month after switching (see Discounts), and seasonal prices are covered for the year the customer would actually be on the tariff. Before this change every estimate was January–December, so a "50% off for 3 months" offer was always valued on Jan–Mar whatever the date. On the 2026 demo data the same 3-month 50% offer on the Dynamic tariff is worth between €89 (Sep–Nov) and €144 (May–Jul), so its placement can change the ranking.

> **Fixed 2026-10-09:** (1) `easter_date` used the Western (Gregorian) Easter algorithm, so Green Monday, Good Friday and Easter Monday were a week early in 2026 (5 weeks early in 2027), and Kataklysmos was set to Easter + 49 (Pentecost Sunday, already a weekend day) instead of + 50, so it was never counted as a holiday. (2) `dc` was built from the real current year while the Dynamic loop used a fixed `CALC_YEAR = 2026`; from 1 Jan 2027 a 5,000 kWh input would have been priced as ~5,006 kWh (`CALC_YEAR` was then replaced by the 12-month window above). (3) ToU peak windows starting/ending on a half hour (e.g. 16.5) were rounded to whole hours in Annual mode. Measured effect on the 2026 demo data: under €0.15/year per tariff (< 0.02%).

---

## Annual mode calculations

In Annual mode the customer enters one **annual kWh** figure. Each tariff's profile is used to distribute that annual figure across the 12 months of the window, and — where the tariff needs intra-day granularity (ToU, Dynamic) — further across the 48 half-hourly slots of each day, weighted by working/non-working day shape and actual day counts of each window month.

### Fixed tariffs
- Monthly kWh (`m_kwh_for_month`) = annual kWh × (that month's HHFF total ÷ the profile's annual HHFF total, `compute_annual_hhff`). A month's HHFF total = Σ over 48 slots of (W value × working days + NW value × non-working days), using that profile month (by calendar month) and that window month's day counts. `annual_hhff` is the sum over the 12 window months. So months with a "heavier" profile shape get proportionally more kWh, not a flat 1/12 split. Without a profile (or an all-zero one) it falls back to annual kWh ÷ 12.
- Energy cost for the month = monthly kWh × tariff's flat `rate`.
- No time-of-day pricing is applied — the profile only affects the *monthly* split, not intra-day.

### ToU (Time of Use) tariffs
- Uses `get_slot_kwh` to distribute the month's HHFF-weighted kWh across the 48 half-hourly slots: slot kWh = annual kWh × (W value × working days + NW value × non-working days) ÷ `annual_hhff`. Working and non-working days are combined per slot, and the same peak window applies to both.
- Each month is tagged "high season" or "low season" by its **calendar** month (`hiStart`…`hiEnd` inclusive vs the rest), each with its own peak window (`hiPeakStart/End` or `loPeakStart/End`, in hours, end exclusive) and peak/off-peak rates.
- For each slot: if the slot's start time in hours (0, 0.5, … 23.5) is ≥ peak start and < peak end → peak rate; else → off-peak rate. Energy cost = Σ(slot kWh × applicable rate).
- Both may **wrap around** (since 2026-10-09; `_in_season`, `_in_peak`): a high season with start > end runs over the new year (11 → 2 = Nov, Dec, Jan, Feb), and a peak window with start > end runs over midnight (22 → 6 = 22:00–06:00; 22 → 0 = 22:00–midnight). `0/0` means no high season, and an end month of 0 also means no high season. Equal peak start and end means no peak hours. Before this, a wrapping season or peak silently gave no high season / no peak at all.
- If the tariff has no profile assigned, falls back to a simple day-fraction split: `peak_fraction = (peak hours)/24` (peak hours of a wrapping window = 24 − start + end, `_peak_hours`), `energy = kWh×peak_fraction×peakRate + kWh×(1-peak_fraction)×offRate`.

### Dynamic tariffs
- Requires a profile — no profile means `monthly_breakdown` returns `None` for every month and the tariff is left out of the comparison.
- For every **actual date** of each window month (its real year, so leap-year February is included when the window contains it), and every one of the 48 half-hourly slots that day:
  - The day is non-working if it is a Saturday, Sunday or holiday in that year (`is_non_working`); its W or NW shape is used accordingly.
  - Slot kWh = annual kWh × (that slot's HHFF value for the day's shape) ÷ `annual_hhff` — full-year normalisation, so all slots of the window add up to exactly the annual kWh. If `annual_hhff` is 0 (all-zero profile), annual kWh is spread evenly over every slot of the window.
  - Slot's DAM price is looked up with this fallback order (DB table `DamData`, fields `damDailyData` / `damBySlot` / `damMonthly`): **exact date + slot actual price** → **the same date + slot 1, then 2 years earlier** (`DAM_LOOKBACK_YEARS = 2`; the window reaches up to a year ahead and the DAM data covers roughly the past year, so most window dates find a real price 1 or 2 years back. Daily data is grouped by calendar month only, so prior-year dates sit in the same month list. A 29 Feb has no earlier-year match and falls through to the averages) → **that month's half-hourly slot average** (`damBySlot`) → **that month's flat DAM average** (`damMonthly`). If none exists, that month returns `None`, `annual_cost_for_tariff` returns `None`, and the tariff is listed under "no DAM data" (`noDamTariffs`) instead of being ranked.
  - Effective price = `max(DAM price, damFloor) × mult + adder` (tariff's `rates`). If `damFloor` is not set, it is treated as 0. This is intended: negative prices are not currently allowed in the Cyprus DAM, so the DAM data never contains them (confirmed by the user 2026-10-09). Revisit if the market rules change.
  - Energy cost += slot kWh × effective price, summed across every slot of every day in the month.
- DAM timestamps are taken as Cyprus local time, as written in the uploaded file (admin page DAM parser in `admin.js: parseDAM`, one price per half-hour slot). Checked 2026-10-09: zero-price slots cluster around 12:00–12:30, i.e. local solar noon, so prices line up with the profile's local-time slots.
- **DAM data handling (since 2026-10-12).** Stored the same way however it comes in:
  - *CSV upload* (admin page → DAM price data): `admin.js: parseDAM` builds `damMonthly` / `damBySlot` / `damDailyData` in the browser. `tariff-api/dam_data.py: build_dam_payload` builds the same three fields with the same arithmetic on the server (checked by `tests/security/test_12_dam_data.py::test_upload_gives_the_same_dataset_as_the_python_builder`). **Change both together.**
  - The server checks the data before saving (`schemas.py: DamIn`): 12 months, 48 half-hours per day, real dates each under its own month and only once, prices from −1 to 10 €/kWh (a file read with the wrong unit gives ~100 and is refused).
  - Every save and rollback is kept in `dam_versions` (restorable) and every change is written to `dam_change_log`. The admin dashboard flags the data when the newest price is more than 15 days old, and the admin is emailed (then weekly while it stays old).

### Variable tariffs
- Rates are **tiered/block** (`rates.tiers`: `{upTo, rate, fixedCharge}` bands) and reset every `resetMonths` (e.g. every 1, 2, 3… months — a "period"). Periods start with the first month after switching (e.g. Nov–Dec, Jan–Feb, … for `resetMonths = 2` and a November start), not with the supplier's own billing calendar, which the tool does not hold. If `resetMonths` does not divide 12, the last period is shorter.
- For each period: total period kWh = sum of that period's months' HHFF-distributed kWh (`m_kwh_for_month`), tiered cost computed via `apply_tiers` (cumulative block pricing, not a flat rate on the whole tier).
- Any tier's fixed charge (`fixedCharge`) is included once per period if that tier was reached, then split evenly across the months in the period and added to standing charge.
- Energy/FPA/fixed-charge totals for the period are split evenly across the months in that period (not weighted by month).

---

## Monthly mode calculations

In Monthly mode the customer enters a flat **per-bill kWh** figure; the server uses `monthly_kwh_flat = monthlyKwh ÷ billingPeriod` (request fields; billing can be monthly or bi-monthly) and `annual_kwh = monthly_kwh_flat × 12` (used for regulated charges). Unlike Annual mode, **every month uses the exact same flat kWh** — there is no annual-total redistribution across months. The ranking/total shown still sums all 12 months of the window, each priced with that month's real profile shape and DAM data, so the *total* reflects 12 months of "what if every bill were this many kWh," not a single month's bill.

Because of this simplification, once the customer enters a value the UI shows a note (`#monthly-calc-note`, `MONTHLY_CALC_NOTE` translation key, populated in `updateMonthlyCalcNote()`) reading roughly "This calculation is based on your consumption for the current month of `<Month>`. For more accurate results, please use the annual calculator." — steering users with seasonal usage patterns toward the Annual mode.

### Fixed tariffs
- Monthly kWh = the flat input value, used as-is for all 12 months (`m_kwh_for_month` returns `monthly_kwh_flat` directly — no profile-based redistribution across months).
- Energy cost = monthly kWh × tariff's flat `rate`. Profile is not used at all for Fixed.

### ToU tariffs
- Every month uses the same flat kWh (no redistribution across months), but the profile **is** used for the split across the day (since 2026-10-09): the month's flat kWh is spread over the 48 half-hour slots by that month's profile shape (W × working days + NW × non-working days per slot), normalised within the month (`_monthly_slot_kwh`), so the slots add up exactly to the flat kWh — the same within-month normalisation Dynamic uses. Each slot is then priced peak/off-peak exactly as in Annual mode.
- Without a profile (or an all-zero month) it falls back to the day-fraction split (`peak_fraction = peak hours / 24`).
- Before 2026-10-09 Monthly-mode ToU always used the day-fraction split, which assumes even use across the day and so under-counted evening/daytime peak use. Effect on the demo data at 400 kWh/month: MV commercial ToU €1,197.90 → €1,238.68/year (peak share 62.5% → 72.3%); domestic ToU +€0.32 (its peak and off-peak rates are almost equal).

### Dynamic tariffs
- Requires a profile — no profile means the tariff is excluded.
- For every actual day of the month, every one of the 48 half-hourly slots:
  - Slot kWh = flat monthly kWh × (slot's HHFF value for that day's working/non-working shape) ÷ **that month's own HHFF total** (`m_hhff`, not the annual total) — i.e. normalised within-month, so the sum of all slots in the month equals the flat monthly kWh exactly.
  - DAM price lookup and floor/mult/adder application are identical to Annual mode (exact date + slot → same date + slot one year earlier → month slot average → month flat average → exclude if none).
- Net effect: same "break the bill into ~1,344–1,488 half-hour periods (28–31 days × 48 slots) and price each against that period's real DAM price" approach the annual mode uses, just with a fixed flat kWh per month instead of an HHFF-weighted annual split.

### Variable tariffs
- Same tiered logic as Annual mode, except every month's kWh input into the period total is the flat monthly kWh (via `m_kwh_for_month`) instead of an HHFF-weighted annual split.

---

## Common calculations (applied to all tariff types)

### FPA (Fuel & Purchased-power Adjustment)
- `get_tariff_fpa(tariff, regulated_rates)`: per-kWh charge added to every unit of energy, on top of the tariff's own rate (Dynamic tariffs included).
- Source is per-tariff (`fpaSource`): `'none'` → €0; `'custom'` → tariff's own `fpaCustom` rate; `'global'` (default) → the regulated global rate matching the tariff's voltage level (`fpaLV`/`fpaMV`/`fpaHV` from the Regulated DB row, loaded via `get_regulated_rates`).
- Applied as `monthly/period kWh × fpaRate`, subject to the same energy discount factor as the tariff's own energy cost.
- In the UI, FPA is shown as a clickable label ("FPA"/"ΑΤΚ" where space is tight, e.g. the per-tariff monthly table header; full text "Fuel price adjustment"/"Αναπροσαρμογή τιμής καυσίμου" where space allows, e.g. the per-bill breakdown) with an "ℹ" icon that opens the same info-popup mechanism used for regulated charges (`openRegInfo('FPA_FULL','FPA_DESC')`), rather than a hover-only tooltip. The label also shows that tariff's actual FPA rate in parentheses (e.g. "FPA (€0.0350/kWh)") instead of a "(custom)"/"(προσαρμοσμένο)" marker — the rate itself tells the customer whether it differs from the regulated default.

### Discounts
- `get_discount_factors(tariff_id, discounts, month_idx1, active_overrides, offers_enabled)` returns an `energyFactor` and `standingFactor` (1.0 = no discount) for a given month of the window (`month_idx1`: 1 = first month after switching).
- Each tariff can have multiple discounts (`discounts[]`), each with a `type` (`'energy'` or `'standing'`), a `percentage`, and an optional `durationMonths`. The duration counts **from the first month after switching** (window month 1): calculated in October, a 3-month discount applies to Nov–Jan. (Before 2026-10-09 it always applied to Jan–Mar.)
- Customers can toggle individual discounts off in the UI (`window._discountState` in `customer.js`); the page sends that state as `discountOverrides` (keys `"{tariffId}_disc_{index}"`), and toggled-off discounts are excluded from the factor calculation. `offersEnabled: false` switches all discounts off.
- **After the offer ends** (`offer_summary`, sent per tariff as `offer`): if any active discount has a `durationMonths` under 12, the result carries `{months: N, afterMonthlyAvg: X}` — N = the longest such duration, X = the average monthly supplier cost (`months[N:]` totals, i.e. energy + FPA + standing with only the permanent discounts still applied) for the rest of the window. The customer page shows it under the price: "⚠ Includes a N-month offer. After it ends: about €X / month (supplier charges)." `None` when offers are hidden, the customer has switched those discounts off, or every discount is permanent / ≥ 12 months. Purpose: an attractive introductory offer cannot hide what the rest of the year costs — e.g. a cheap-season Dynamic discount followed by expensive summer DAM prices.
- Multiple active discounts of the same type stack additively (percentages summed, then floored at 0% remaining — i.e. cannot go negative).
- `annual_cost_no_discount(...)` recomputes the full breakdown with all discounts forced off, to show the "full price" (strikethrough) alongside the discounted price. It is only computed for tariffs that have discounts while offers are shown (`fullBase` in the response; `null` when offers are switched off). It uses the same summation as the discounted total, so with no discount active the two are exactly equal; the page only shows a struck-through price when `fullBase − base ≥ €0.005` (fixed 2026-10-09: with offers switched off, floating-point noise between two differently-summed totals showed e.g. ~~€1486~~ €1486).
- Discount data format (enforced server-side since 2026-09-30, `schemas.DiscountIn`): `{type: 'energy'|'standing', percentage: >0–100, durationMonths: 1–120 | null, conditions: string}`. Both the admin editor and the supplier portal save this shape. The supplier portal previously saved `{label, pct, euro}`, which the engine ignored.

### Input validation and failure isolation
- Every tariff's `rates`, `discounts` and charges are validated on save against a per-pricing-type schema (`schemas.py`: `FixedRatesIn`, `TouRatesIn`, `DynamicRatesIn`, `VariableRatesIn`, `DiscountIn`). The engine can therefore assume numeric, finite, in-range values. Limits are listed in `ADMIN_MANUAL.md` §6.10.
- As a safety net, `/api/public/calculate` prices each tariff independently: if the engine raises for one tariff, or returns a non-finite total, that tariff is skipped and logged, and the rest of the comparison is still returned.

### Regulated charges (network/PSO/RES) & MDM
- Not part of the supplier ranking/comparison — always shown as a separate line item, added on top of the supplier's own cost. Labelled to the customer as **"additional charges"**, not "regulated charges" — MDM (below) is not always actually CERA-regulated, so the old wording overclaimed.
- `regulated_breakdown(voltage, annual_kwh, mdm, mdm_invoice_months, mdm_regulated, regulated_rates)["total"]` = `annual_kwh × (grid_rate + pso + res) + mdm × (12 / mdm_invoice_months)` (sent to the page as `reg`).
  - `grid_rate` = network charge, selected by voltage level (`lv`/`mv`/`hv` from the Regulated DB row, loaded via `get_regulated_rates`).
  - `pso` = Public Service Obligation levy (per kWh, flat across voltage levels).
  - `res` = RES & Energy Conservation Fund levy (per kWh, flat across voltage levels).
  - `mdm` = Meter Data Management, a charge **per invoice** (not per kWh, and not always monthly) — see below.
- `regulated_breakdown(...)` is the single source of truth for these figures — it computes the total plus individually labelled rows (Grid / PSO / RES / MDM, sent as `regBd`) for the itemised bill view. Each row also carries a `regulated: true/false` flag (Grid/PSO/RES are always `true`; MDM depends on sourcing below) used purely for display.

#### MDM sourcing — regulated vs. supplier-set
- Suppliers can be flagged `regulated` (`Supplier.regulated` DB column, e.g. EAC) — orthogonal to a tariff's Domestic/Commercial/Industrial contract type.
- `mdm_for_tariff(tariff, supplier_regulated, regulated_rates)` decides the €/invoice value: **regulated supplier** → always the CERA-set global rate (the Regulated DB row's `mdm` field), ignoring the tariff's own `mdm` field entirely; **non-regulated supplier** → the tariff's own `mdm` (admin/supplier-entered, freely editable). There is deliberately no way for a non-regulated supplier to opt into the regulated rate.
- This also drives display: a regulated MDM row is coloured/labelled like Grid/PSO/RES (blue, "Meter Data Management (MDM)", `REG_MDM_DESC` info text). A non-regulated MDM row uses the supplier-charge colour (`var(--text2)`, same as Energy/Standing), the `MDM_SUPPLIER` label and `MDM_SUPPLIER_DESC` info text, explicitly stating it's a competitive charge, not a regulated one. The Standing row/header carries the same "competitive charge" info text (`STANDING_DESC`) for the same reason — it is always supplier-set, never regulated.

#### MDM invoicing frequency
- MDM is charged **once per invoice**, not once per calendar month. `mdmInvoiceMonths` (`1` = monthly, `2` = bimonthly; set per tariff by the admin/supplier, defaults to `2`) gives invoices/year = `12 / mdmInvoiceMonths`, and `annual MDM = mdm × invoices/year` — **not** a flat `× 12`. E.g. a €0.94 bimonthly charge totals €5.64/year, not €11.28/year as a naive ×12 would give.
- Displayed rate text is deliberately short — `€{N} / λογαριασμό` / `€{N} / invoice` (`LBL_FIXED_ROW_MDM`), no frequency inline, to avoid widening the breakdown table's columns. The actual frequency is only in the `title` hover tooltip (`MDM_BILLED_MONTHLY` / `MDM_BILLED_BIMONTHLY`).

- Regulated/additional charges are **not** discounted — the discount system only applies to the supplier's own energy/standing charges.
- Each row's label is clickable (`openRegInfo`, same info-popup mechanism as FPA) — €/kWh for Grid/PSO/RES, a flat €/invoice figure for MDM. This applies in both the annual ranked-list breakdown and the monthly single-bill breakdown.

### Standing charge
- Flat, tariff-specific monthly fee (`standing`), added once per month regardless of consumption. Always supplier-set/competitive, never regulated — its label carries an info tooltip (`STANDING_DESC`) saying so, same treatment as a non-regulated MDM row.
- Subject to the tariff's `standingFactor` discount (if any `type: 'standing'` discount is active and in-period).
- For Variable tariffs, any reached tier's `fixedCharge` is folded into "standing" (for discount-eligibility purposes) rather than kept separate.
- The annual/ranked-list breakdown table (`customer.js`) always derives its displayed "Standing" total by summing each month's already-discounted `standing` from the server's `months` array (`moBd.reduce(...)`) — never `standing × 12` — so the row's Energy+FPA+Standing always foots to the same total shown in the Total column, even when a standing discount is active. (Prior to 2026-07-17 the annual table used `t.standing×12` for all non-Variable pricing types, which silently ignored standing discounts in the displayed breakdown while the ranked total itself was already correct — a display-only bug, now fixed.)

---

## Sample invoice (admin-togglable customer feature)

An optional "Sample invoice" view (`openSampleInvoice` in `customer.js`, which fetches `pricing/invoice.py: build_sample_invoice_data` via POST /api/public/sample-invoice) lets a customer see a bill-styled breakdown for a tariff, explained line by line. It is admin-controlled — `cfg.sampleInvoiceEnabled` (from a single-row `sample_invoice_config` DB table, defaults to off) gates whether the button/modal render at all — and introduces no new pricing logic: it only re-presents numbers already produced by `monthly_breakdown`/`regulated_breakdown`, plus two additions specific to this illustrative view:

- **Which period is shown:** not a 12-month average. Monthly input mode shows the customer's own chosen billing cycle — `_billingPeriod` (the Monthly/Bi-monthly toggle next to the "consumption per bill" field, 1 or 2 months), since that's literally what the entered kWh figure represents. Annual input mode shows the tariff's own invoicing cadence (`mdmInvoiceMonths`, default 2) instead, since there's no billing-cycle input to read in that mode. Either way, the period is **the customer's first bill after switching**: the first 1 or 2 months of the window (`get_sample_invoice_period(..., window)`; e.g. calculated in October, a bimonthly invoice covers 1 Nov – 31 Dec). Before 2026-10-09 it was the last 1–2 months before today. The months are summed from `monthly_breakdown`'s per-month `energy`/`fpa`/`standing` (not divided evenly), so it reflects that period's actual HHFF-weighted consumption. Grid/PSO/RES/MDM are taken from `regulated_breakdown`'s annual figures scaled by `monthsCount / 12`, the same "annual ÷ 12 × period" convention already used for the existing monthly-mode bill breakdown table — not a new calculation path.
- **VAT:** the tool is otherwise entirely ex-VAT everywhere else (see "Regulated charges" above). The sample invoice is the one place VAT is shown, purely for realism, mirroring the EAC bill example: Cyprus standard 19% is applied to (energy + FPA + standing + grid + PSO + MDM); RES & ES Fund is added afterwards, untaxed — same ordering as the real EAC bill's "Total subject to VAT" → "+ RES & ES Fund" → "+ VAT" flow. This is purely a display computation local to `build_sample_invoice_data`; it does not feed back into the comparison ranking or any other total shown elsewhere.

If a tariff has no cost data for the chosen period (e.g. a Dynamic tariff missing DAM data), `build_sample_invoice_data` returns `None` (JSON `null`) and the button is simply omitted for that tariff — no error state, no fallback calculation.

The view is laid out like a real bill (customer/account/meter info block, itemised charges, highlighted amount due) to make the numbers easier to relate to an actual EAC bill. Everything identifying a "customer" is a fixed placeholder (`SAMPLE_INV_EX_NAME`/`SAMPLE_INV_EX_ADDRESS`/`SAMPLE_INV_EX_ACCOUNT`/`SAMPLE_INV_EX_METER` translation keys) — never real data, since the tool has no customer accounts. (An earlier version also showed a fabricated "same period last year" comparison with a small chart; this was removed since the tool holds no real metering history to compare against.)

Each charge row also shows its "qty × rate" calculation underneath the label (`.invoice-calc`, e.g. `1,633 kWh × €0.1035/kWh`), matching the EAC bill's `{1.633 kWh x €0,1035}` notation, computed in `build_sample_invoice_data`:
- **Energy**: for **Fixed** tariffs, one row (`energyRate = energyFull / periodKwh`, equal to the tariff's own configured rate). For **ToU** tariffs, split into two rows — **Peak** and **Off-Peak** — each with its own real `kWh × rate` line: `monthly_breakdown` (engine.py) now tags every 30-min slot (or, in monthly-flat input mode, the peak-hours fraction of the month) as peak or off-peak using that month's `hi`/`loPeakStart`/`End` window, accumulating `peakKwh`/`offPeakKwh` and `peakEnergy`/`offPeakEnergy` (discounted) plus `...Full` (undiscounted) alongside the existing blended `energy` total; `build_sample_invoice_data` sums these across the invoice period and derives `peakRate`/`offPeakRate` as `energyFull / kwh` per bucket. Dynamic/Variable tariffs still charge a different rate per time slot/tier with no fixed per-bucket rate to show, so the formula line is omitted for those (the energy total itself is still shown, just without a "qty × rate" underneath).
- **FPA/Grid/PSO/RES**: straightforward `periodKwh × rate`, using each charge's real fixed per-kWh rate.
- **Standing**: `standing/mo × monthsCount` (the tariff's base monthly fee).
- **MDM**: `mdmRate € × mdmInvoices`, where `mdmInvoices = monthsCount / (mdmInvoiceMonths or 2)` — equals exactly 1 whenever the period was sized to the tariff's own invoicing cadence (always true in Annual mode by construction); can be fractional in Monthly mode if the tariff's real cadence differs from the single-month sample period.

**Discounted rows show both figures.** Energy/FPA/Standing formulas above are all built from the *pre-discount* rate/qty, so they reconcile to `energyFull`/`fpaFull`/`standingFull` (summed from `monthly_breakdown`'s `*Full` fields) — not to the actual (post-discount) `energy`/`fpa`/`standing` totals when a discount is active on that tariff. Rather than show a formula whose arithmetic doesn't match the printed total (e.g. "€4.00/mo × 2" next to €7.60 instead of €8.00 — the bug this note replaced), the row displays both: the pre-discount amount struck through, then the actual amount due, the same convention already used in the ranked comparison list elsewhere on this page. Grid/PSO/RES/MDM are never discounted (see "Regulated charges" above), so their formulas always reconcile exactly as-is.

**Competitive vs. regulated grouping.** Rows are split into two sections, matching the distinction used everywhere else in this tool (see "Regulated charges" above): a **Competitive charges** section (Energy, FPA, Standing) and a **Regulated charges** section (Grid, PSO). MDM is placed into whichever section actually reflects who set the rate — `mdmRegulated` (from `mdm_for_tariff()` / `Supplier.regulated`) decides: a regulated supplier (e.g. EAC) uses the CERA-set MDM rate, so it belongs with the regulated section; otherwise it's the supplier's own competitive metering charge. Each section has its own subtotal (`competitiveTotal`, `regulatedTotal`, computed for display in `customer.js`); their sum is `vatBase`, shown as "Total subject to VAT" — unchanged from the underlying calculation, just relabelled/regrouped for display.

**RES & ES Fund is shown on its own, after both sections**, since — unlike every other regulated charge — it is *not* subject to VAT (`res` is added to `vatBase` only after the VAT rate is applied, per the VAT rule above). This also fixed a pre-existing wording bug in the regulated-charge info popups: `REG_PSO_DESC` previously claimed PSO was not subject to VAT (wrong — PSO *is* taxed, it's part of `vatBase`) while `REG_RES_DESC` didn't mention VAT at all (it should have, since RES is the one that's actually exempt). Both descriptions now state the correct VAT treatment.

---

## Adding a new tariff type or changing a calculation

When adding a new pricing type or changing how an existing one works:
1. Update `monthly_breakdown(tariff, dc, ...)` (and, if the Annual/Monthly split differs meaningfully, keep the `is_monthly` branch logic consistent with the pattern above).
2. Add a new chapter to both the **Annual mode** and **Monthly mode** sections above, following the same structure (source of monthly kWh → intra-day/slot logic → price lookup/formula).
3. If the change affects FPA, discounts, or regulated-charge treatment, update the **Common calculations** section too.
3a. Add or update the matching rates schema in `tariff-api/schemas.py` (`_RATES_MODEL`). Otherwise the new fields are rejected or silently dropped on save.
4. Consider whether the change should also be surfaced to customers — e.g. via a notice (`cfg.notices` / `assumptions_en` shown on the customer page) or a per-supplier explanatory field on the supplier admin page — so the assumptions are visible to end users, not just documented here internally.
