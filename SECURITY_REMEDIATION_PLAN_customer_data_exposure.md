# Move Tariff Calculation Server-Side (Reduce Public Data Exposure)

## Context

A security specialist reviewing the app flagged that on the customer tab, "the whole application is loaded onto the browser." Investigation confirmed this is accurate and substantive, not just a comment about readable source code:

- `customer.html` (2,963 lines) is served as a raw static file with no build/minify step ([tariff-api/main.py:333-334](tariff-api/main.py#L333-L334)), with no authentication by design.
- It contains ~500 lines of unminified JavaScript ([customer.html:1290-1834](customer.html#L1290-L1834)) implementing the entire tariff-pricing engine: 4 pricing modes (Fixed, Time-of-Use, Dynamic/DAM-indexed, Variable/tiered), regulated-charge calculation, discount logic, and a sample-invoice/VAT generator.
- The backend endpoint the page calls, `GET /api/public/config` ([main.py:235-295](tariff-api/main.py#L235-L295)), does no calculation — it dumps the **full raw pricing dataset** to any anonymous visitor: every approved tariff's rate tiers/FPA/discounts/standing charges, full 48-slot × 12-month half-hourly load-shape profiles, all CERA-regulated rates, and 2 years of full Day-Ahead-Market price time series.
- Net effect: anyone can view-source or inspect network responses and walk away with the complete current rate book and pricing algorithm for every supplier — not just UI code.

For comparison, `admin.html`/`supplier.html` are served the same way, but their privileged *actions* are gated server-side by JWT/role checks (`require_admin` in [routers/admin.py](tariff-api/routers/admin.py)). `customer.html` has no equivalent held-back layer — the thing of value (calc logic + full pricing data) has nothing protecting it.

**Decision:** move calculation server-side so the client requests computed results rather than raw rate structures. This is the full-scope fix (not a partial mitigation) — chosen so this plan can be handed to the specialist as the complete remediation approach.

No server-side calculation logic exists anywhere today (confirmed: no PDF/report generator does pricing math; `serializers.py` is pure ORM-to-dict flattening) — this is a full port, not wiring up existing logic.

## What the page actually does (for context on the design)

`customer.html` renders a **ranked comparison table**: the customer enters their consumption (kWh) and filter criteria, and `applyFilters()` ([customer.html:2215-2532](customer.html#L2215-L2532)) scores every matching approved tariff and renders one expandable card per tariff, cheapest first, with a 12-month breakdown table and charts. All recalculation triggers are discrete (dropdown/checkbox changes, or keystrokes in two number fields) — no continuous slider dragging — so a network round trip per recalculation is workable with debouncing on the two number inputs.

Important nuance: several numbers computed by the pricing engine are also displayed literally for transparency (FPA rate, standing charge, discount %/duration, tier ranges for Variable tariffs, Dynamic floor price). The fix must return curated **derived display fields** (e.g. "effective FPA rate for this tariff", a pre-formatted discount summary, a tier-summary string) rather than simply deleting all numeric fields — otherwise the UI breaks.

## Design

### 1. New endpoints
- `POST /api/public/calculate` — accepts the same inputs `applyFilters()` currently derives from the DOM (consumption, billing mode/period, customerType, voltage, contract, loadEntitlement, pricing-type filter, offers/vulnerable toggles, per-tariff discount-toggle state, calendar year) and returns, per matching approved tariff: ranked annual/period cost, 12-month breakdown, regulated-charge breakdown, and a `display` block of pre-formatted values (FPA rate string, standing charge, discount summary, tier/calc-note text, Dynamic floor) — never raw tier tables, full profile arrays, or full DAM series.
- `POST /api/public/sample-invoice` — separate, on-demand endpoint (called only when a customer opens the sample-invoice modal) returning the same shape `buildSampleInvoiceData()` produces today.

### 2. `GET /api/public/config` trimmed
Keeps: supplier contact info, a new trimmed per-tariff summary (id/name/supplier/contract/voltage/pricing-type/vulnerable/durationMonths/loadEntitlement/standing charge — display/filter metadata only, no rates/discounts/mdm/fpa source), notices, `sampleInvoiceEnabled`.
Drops entirely: `profiles` (full half-hourly arrays), `regulated` (raw CERA rate table), `damMonthly`/`damBySlot`/`damDailyData` (raw DAM price series). Verify nothing else in the UI reads these before removing (e.g. a "last updated" timestamp) and preserve just the timestamp/metadata if so.

### 3. Python calculation engine — new package `tariff-api/pricing/`
Pure functions, one module per concern, each a direct port of its JS counterpart with all global/DOM-state coupling removed (the JS versions read `window`/`document` directly — the ports take everything as explicit parameters):
- `daycounts.py` — `easter_date`, `get_cyprus_holidays`, `get_day_counts` (port of [customer.html:1303-1328](customer.html#L1303-L1328))
- `profiles.py` — `compute_annual_hhff`, `get_slot_kwh` (port of 1569, 1587)
- `regulated.py` — `get_regulated_rates`, `mdm_for_tariff`, `get_tariff_fpa`, `regulated_breakdown` (port of 1361-1479)
- `discounts.py` — `get_discount_factors` (port of 1415)
- `tiers.py` — `apply_tiers` (port of 1339)
- `engine.py` — `monthly_breakdown` (port of the 1623 workhorse, split into `_fixed`/`_tou`/`_dynamic`/`_variable` per mode), `annual_cost_for_tariff`, `annual_cost_no_discount`
- `invoice.py` — `get_sample_invoice_period`, `seeded_variance` (must replicate the JS PRNG's exact 32-bit-overflow hash arithmetic byte-for-byte), `build_sample_invoice_data` (port of 1478-1519)
- `display.py` — new (no JS analogue): `format_fpa_rate`, `format_discount_summary`, `format_calc_note` — builds the derived display strings so raw rate tables never need to leave the server
- `filters.py` — `filter_matching_tariffs` (port of the filter block in `applyFilters()`, 2233-2246)

Route handler in new `tariff-api/routers/public_calc.py` (registered in `main.py` alongside existing routers) is orchestration only — loads data, calls the pure functions, assembles the response. New Pydantic request/response models go in `tariff-api/schemas.py`. New trimmed tariff serializer goes in `tariff-api/serializers.py`.

### 4. `customer.html` changes
- `applyFilters()` becomes `async`, replacing its local scoring loop with a `fetch('/api/public/calculate', ...)` call; rendering code (DOM building, Chart.js) stays intact, consuming the response instead of locally computed values.
- Card expand / chart redraw reuses the cached last-fetched response for that tariff (no extra round trip on expand, matching current UX).
- `toggleDiscount()` re-fetches with updated discount overrides instead of recomputing locally.
- The two consumption `oninput` handlers get debounced (~300-350ms) with request-cancellation (AbortController or a request-id guard) so a fast keystroke doesn't render a stale, slower response.
- `openSampleInvoice()` fetches `/api/public/sample-invoice` on demand instead of using a precomputed-for-all-cards object.
- All now-dead client calc functions (`monthlyBreakdown`, `annualCostForTariff`, `regulatedBreakdown`, `getDiscountFactors`, `computeAnnualHHFF`, `getSlotKwh`, `applyTiers`, `getTariffFpa`, `mdmForTariff`, `getRegulated`, `calcNote`'s raw-rate logic, `buildSampleInvoiceData`, `getSampleInvoicePeriod`, `_seededVariance`, `getDayCounts`/`getCyprusHolidays`/`easterDate`) get deleted once cutover is verified.

### 5. Verification (numeric parity is critical — must not shift customer-visible prices)
Build a temporary diff-testing harness (`tariff-api/scripts/diff_test_pricing.py`, not shipped) that runs a matrix of every approved tariff × a spread of consumption values × both billing modes × discount on/off × offers on/off through both the new Python engine and the existing JS (via a headless Node/Playwright runner against the real page, to also catch DOM-coupling quirks), asserting numeric equality within tolerance (e.g. 1e-6, or a EUR-cent tolerance) on every leaf field before rounding/display formatting. Include edge cases explicitly: Dynamic tariffs with partial DAM coverage, Variable tariffs with reset periods not dividing evenly into 12, discounts shorter than the billing period, leap years, both `mdmSource` values, regulated vs non-regulated suppliers.

### 6. Phasing (each phase independently shippable, exposure only actually drops in Phase 3)
1. **Build + verify the engine** — add `pricing/` package and the two new endpoints; `/api/public/config` and `customer.html` untouched, so zero user-facing risk. Exit when the diff-testing matrix passes 100%.
2. **Cut `customer.html` over** — parallel-run in a dev/staging deploy first (compute both paths, render only the old one, log mismatches) for a manual QA soak period; then switch rendering to the server response, add debounce/cancellation, delete dead client calc code. `/api/public/config` still returns full data at this point, so nothing breaks. Exit when grep confirms no remaining references to raw `rates`/`discounts`/`profiles`/`regulated`/`dam*` fields in `customer.html`.
3. **Strip the raw fields from `/api/public/config`** — swap in the trimmed tariff serializer, drop `profiles`/`regulated`/`dam*` arrays. This is the actual security fix. Verify via a full click-through and a Network-tab check that the response no longer contains any rate/tier/FPA/profile data.

## Critical files
- [tariff-api/main.py](tariff-api/main.py) — `/api/public/config` route to trim (~235-295), router registration, static mount (~333-334)
- [customer.html](customer.html) — calc engine to port/delete (~1290-1834), `applyFilters()` to rewire (~2215-2532), `openSampleInvoice` (~1963), `calcNote` (~2124)
- `tariff-api/serializers.py` — add trimmed `tariff_to_public_summary_dict`
- `tariff-api/models.py` — `Tariff`/`Profile`/`Regulated`/`DamData` field shapes the port must match
- `tariff-api/routers/admin.py` — reference pattern for structuring the new `routers/public_calc.py`
- `tariff-api/schemas.py` — new Pydantic request/response models
- New: `tariff-api/pricing/*.py`, `tariff-api/routers/public_calc.py`, `tariff-api/scripts/diff_test_pricing.py` (temporary)

## Verification
1. Run the diff-testing harness after Phase 1 — must pass 100% across the full input matrix before proceeding.
2. Manual browser QA in Phase 2's parallel-run mode (staging) across all filter/pricing-mode/discount/sample-invoice combinations, watching for logged mismatches.
3. After Phase 3, inspect `/api/public/config`'s actual network response in devtools to confirm no rate/tier/FPA/profile/DAM data remains, and click through the full customer flow (all 4 pricing modes, discounts, sample invoice) to confirm no regressions.
4. Update [TARIFF_CALCULATIONS.md](TARIFF_CALCULATIONS.md) to reflect that calculation now happens server-side, per the existing project convention that this doc must stay in sync with calc logic changes.
