# Security Remediation Checklist

Complete record of security work on the CERA Tariff Comparison Tool, newest round last within each section. Originally a forward-looking action list from the 2026-07-14 architecture/security review (`TECHNICAL_ARCHITECTURE_REVIEW.md`) and the XSS deep-dive; expanded 2026-09-25 to be the single log of **every** security task handled and how it was solved, so it can be handed to the external certifier as-is.

Legend: **[x]** done & verified · **[~]** partially done / follow-up noted · **[ ]** open (pre-production).

Every "verified live" note below means the fix was exercised against a running instance backed by a **disposable** database with real attack payloads — the production/dev database was never used for testing.

---

## Round 1 — Stored XSS deep-dive (2026-07-14)

- [x] **Exhaustive review of all 116 `innerHTML`/`outerHTML`/`insertAdjacentHTML` sinks** across all four frontend files (76 in admin.html, 20 in customer.html, 19 in supplier.html, 1 in reset-password.html). The portals are vanilla-JS with no templating layer, so every dynamic render is a hand-built HTML string — any DB-sourced value (tariff/supplier/profile name, email, filename, changelog value, user-agent) dropped in without escaping was a stored-XSS sink.
  - **Fix:** added an `esc()` HTML-escaping helper and applied it at every sink across all three portals.
  - **Sneakier variant also fixed:** a value inside an inline `onclick="fn('${x}')"` handler is unsafe *even when HTML-escaped*, because the browser decodes the attribute before running it as JS. Those were rebuilt to use `data-*` attributes + `this.dataset` (or an id-keyed cache), so the untrusted value never sits inside a JS string.
  - Verified live with `onerror`/quote-breakout payloads in every affected field — 0 fires.

---

## Round 2 — Post-XSS hardening, 4 planned items (2026-07-14)

- [x] **1. DOMPurify for the notices rich-text path.** The admin notices editor (assumptions/legal/vulnerable text, EN/EL) intentionally renders raw HTML on customer.html — a WYSIWYG feature, but a stored-XSS path if an admin account is compromised or the editor misbehaves. **Fix:** vendored DOMPurify 3.1.6 and sanitized at all 4 sinks — customer.html `switchNoticesTab()` and `openVulnerableModal()` (the public exposure points), and admin.html `setNotices()`/`getNotices()` so a payload can't round-trip through the editor and what's saved server-side is already clean. Verified live via Playwright: 0 fires, safe markup preserved, dangerous attributes stripped.
- [x] **2. Content-Security-Policy header.** **Fix:** added a CSP response header (`add_csp_header` middleware in `main.py`) on every response. Scripts/styles allow `'unsafe-inline'` plus only the two CDNs actually used (cdnjs for Chart.js/DOMPurify, Google Fonts); everything else locked down (`object-src 'none'`, `base-uri 'self'`, `form-action 'self'`, `frame-ancestors 'self'`, `connect-src 'self'`, `img-src 'self' data:`). `'unsafe-inline'` was kept deliberately (the app is hundreds of inline handlers/scripts; a strict policy needs a full refactor first), so this guards against *external* malicious scripts and locks down framing/forms/plugins/cross-origin — it does not by itself stop inline-injection (that's what Rounds 1-2 items 1,3,4 cover). Verified live across all 3 portals: 0 errors, CDNs and fonts still load.
- [x] **3. Server-side input validation on tariff/supplier submissions (`schemas.py`).** **Fix:** rewrote schemas — enum-like fields (`contract`/`voltage`/`pricing`/`fpaSource`/`loadEntitlement`, status, audience) are now `Literal[...]` types, so a raw API call with a valid token can't set arbitrary values; `max_length` bounds on every free-text field and numeric `ge`/`le` bounds; emails go through the `email-validator` library; supplier `website` must be `http(s)://` — the **root-cause fix** for the `javascript:` URL bug (can no longer be *submitted*, not just neutralized at render). `rates`/`discounts` left as loose JSON (shape varies by pricing type; follow-up if per-type schemas ever wanted). Verified live: valid submissions still 201; `javascript:` website + bad email rejected 422; bad `contract` rejected 422.
- [x] **4. Rebuild the 3 highest-risk `innerHTML` sinks as real DOM nodes** so untrusted data can only ever be text, not markup. **Fix:** admin.html `renderLoginActivity()`, `buildDashboard()`'s pending-review widget, and `openReview()` modal now built with `document.createElement` + `.textContent` and `addEventListener` (no inline `onclick` with embedded ids). Verified live with 8 payload flags: 0 fires. *Scope note:* targeted rewrite of the 3 worst sinks; the rest still rely on `esc()`, applied everywhere and verified in Round 1.
- [x] **Bonus: CSV formula injection** in the changelog export neutralized, plus a related quoting bug (embedded double-quotes weren't doubled).

---

## Round 3 — Broader vulnerability-class review (2026-07-15)

- [x] **SQL injection — checked, clean.** All queries go through the SQLAlchemy ORM (parameterized). Only raw SQL is the startup migration block with hardcoded literals and one bound param; no user input reaches it.
- [x] **Buffer overflow — not applicable.** Pure Python/JS, no native buffer handling. The one raw-bytes path (PDF upload) uses a size-capped read, magic-byte check, and UUID storage filenames (no path traversal).
- [x] **`Content-Disposition` header injection — fixed.** Document downloads built the filename via an unescaped f-string; a `"` in an uploaded filename could inject header parameters. **Fix:** removed the manual header and rely on Starlette's `FileResponse(filename=...)`, which quotes/encodes correctly.
- [x] **Broken access control / IDOR — fixed, live-verified.** `GET /api/admin/config` and `/changelog` returned the *entire* changelog (other suppliers' names/diffs/admin emails) to any supplier; `GET /api/admin/suppliers` returned every supplier's full contact record to any logged-in user. **Fix:** changelog filtered to the caller's own supplier; `/suppliers` switched to admin-only. Verified with two seeded supplier accounts: each sees only its own data; supplier gets 403 on `/suppliers`; admin still sees all.
- [x] **Email HTML injection — fixed.** Tariff names / rejection reasons were interpolated unescaped into HTML emails (letting a supplier inject phishing/tracking content into CERA-branded mail). **Fix:** added `html.escape` at all 5 email-body call sites. Verified with `<img>/<script>` payloads → escaped entities in the sent JSON.
- [x] **OTP brute-force — fixed, live-verified.** OTP verification had no attempt limit — 1,000,000 codes guessable within the 10-minute window. **Fix:** reused the existing account lockout (3 attempts → 180-minute lock, lockout email, activity log). Verified: 3 wrong codes → locked; a *correct* code is rejected while locked; unlock restores normal login.
- [x] **Dependency CVE scan — clean.** `pip-audit` against `.venv` (the authoritative environment): no known vulnerabilities. *Operational note:* always run via `tariff-api\.venv\Scripts\python.exe`, not bare `python` (bare resolves to a global install with unrelated packages).
- [x] **JWT storage moved sessionStorage → httpOnly cookie — live-verified.** The token was JS-readable, so any future XSS could exfiltrate it. **Fix:** session now lives in an `HttpOnly`, `Secure`, `SameSite=Strict` cookie; added `POST /api/auth/logout` (JS can't clear an httpOnly cookie); frontend no longer stores or attaches the token. Verified in a real browser (19 checks): token never in `document.cookie`, persists across reload, logout clears it. **Deployment implication:** `Secure` means real deployments **require HTTPS** or login silently fails (see pre-production section).

---

## Round 4 — Rate limiting, sessions, cross-portal access control (2026-07-15)

- [x] **Per-IP rate limiting.** Custom in-process sliding-window limiter (60 req/min per IP) in `main.py` to protect against accidental overload. `slowapi` was tried first but silently no-ops on routes registered via `include_router()` on this FastAPI/Starlette version, so it's hand-rolled. Auth-endpoint hits are logged to the "Login activity" table. *This is best-effort overload protection, not anti-abuse — see Round 9 / pre-production for the X-Forwarded-For caveat.*
- [x] **Sliding session expiry.** Tokens now renew on each request (1h idle) capped at a 12h absolute lifetime, replacing a flat expiry — active users aren't logged out mid-work, a stolen token can't be replayed indefinitely.
- [x] **Cross-portal access control.** supplier.html accepted admin logins, and admin.html treated any 200 from `/config` as proof of admin. **Fix:** each portal verifies role explicitly and treats a mismatch as "not logged in"; added `X-User-Role` header + `GET /api/auth/me` to catch a cookie swapped by a different-role login in another tab. Server-side authorization was already intact — this closed a UI-exposure gap. All wrong-role/expired messages are now generic (no role/account leak).

---

## Round 5 — Infrastructure & audit hardening (2026-07-20 → 07-23)

- [x] **Real foreign key** replaces string-matched supplier↔user linkage.
- [x] **Secrets/config centralized** into `config.py` (one place to audit; no scattered `os.getenv` fallbacks).
- [x] **Alembic migrations** replace hand-rolled `ALTER TABLE` statements; startup crash on a `%` in `DATABASE_URL` fixed.
- [x] **Scheduled local `pg_dump` backup** added and documented in the admin manual (restore procedure included).
- [x] **Audit-trail gaps closed** — OTP-toggle and document-upload-triggered resubmissions now logged to the changelog.

---

## Round 6 — Point-in-time penetration test (2026-08-13)

Full manual audit of `tariff-api/` and the 3 portals (auth/session, IDOR, injection, XSS, CORS, secrets, client-side token handling). No SQLi, RCE, exploitable XSS, CORS misconfig, or IDOR found; session confirmed httpOnly-cookie-only. Four issues found and fixed same day:

- [x] **Login enumeration** — wrong-password responses included "N attempts remaining" (only shown for real accounts). Now returns the same generic "Invalid email or password" as the unknown-email branch.
- [x] **Hardcoded JWT fallback secret** — if `TARIFF_SECRET_KEY` were unset, the app silently signed tokens with a fixed in-source string (anyone with repo access could forge admin tokens). Now a hard startup failure unless `TARIFF_ALLOW_DEV_SECRET=1` is set for local dev only.
- [x] **`PUT /api/admin/config` had no schema validation** — took a raw dict and wholesale-replaced the catalog with untyped data. Added `ConfigImportIn` (composed from the existing per-entity schemas) so a bulk publish can't write data the individual endpoints would reject.
- [x] **`UpdateEmailIn.new_email` had no format check** — a user could set their own email to a non-email string, breaking OTP/reset delivery. Added the shared email validator.
- [~] **Follow-up:** live UI walkthrough of login / password-reset / "Publish" / email-change to confirm `ConfigImportIn` accepts every real payload shape. Schema was unit-verified against `persistConfig()`'s structure but not yet exercised through the live UI.

---

## Round 7 — Customer-data-exposure remediation (2026-09-03 → 09-04)

A reviewing security specialist flagged that customer.html shipped the entire pricing engine **and** the full raw dataset to any anonymous visitor (`GET /api/public/config` dumped every tariff's rates/discounts/standing charges, full half-hourly load-shape profiles, all regulated rates, and 2 years of Day-Ahead-Market prices). Full plan in `SECURITY_REMEDIATION_PLAN_customer_data_exposure.md`.

- [x] **Pricing moved server-side.** New pure-function `tariff-api/pricing/` package + `POST /api/public/calculate` and `POST /api/public/sample-invoice`. customer.html now sends inputs and renders returned results; ~520 lines of client-side calc deleted. Numeric parity verified against the old engine.
- [x] **`GET /api/public/config` trimmed** to display/filter metadata only — `profiles`, `regulated`, and all DAM series removed, and per-tariff `rates`/`discounts`/`mdmSource`/`fpaSource`/`profileId` removed. (Re-confirmed clean in Round 9's black-box test.)
- [x] **Stopped shipping full load-profile shapes to supplier accounts** — `GET /api/admin/profiles` now returns id/name/desc to suppliers (all supplier.html uses), full shape data to admins only.

---

## Round 8 — Penetration test of the new public endpoints (2026-09-14)

- [x] **NaN/Infinity crash → fixed.** `annualKwh`/`monthlyKwh` accepted non-standard JSON `NaN`/`Infinity`, crashing the pricing engine with a 500 — and the 422 meant to reject them itself 500'd during JSON encoding. **Fix:** `allow_inf_nan=False` + an upper bound (5,000,000) on the inputs, plus a `RequestValidationError` handler that sanitizes non-finite floats before encoding. Verified: NaN/Infinity/1e20/negative all return clean 422s; normal requests 200.
- [x] **Document-ID enumeration → fixed.** `GET /api/admin/documents/{id}/download` returned 403 for another supplier's document vs 404 for a non-existent one, letting a supplier enumerate which IDs exist. Both now return 404.
- [x] **Division-by-zero in Dynamic annual-mode calc → fixed.** A Dynamic tariff with an all-zero profile crashed every customer's comparison in annual mode. Mirrored the existing monthly-mode zero-guard (spread evenly instead of dividing by zero). Found by an independent second-opinion code review.

---

## Round 9 — Black-box security test (2026-09-25)

Outside-attacker testing over HTTP against an isolated instance on a throwaway database, across anonymous / supplier / admin roles. *Fixes committed on branch `security/blackbox-findings-2026-09-25` — not yet merged.*

- [x] **MED — supplier could read admin-only reference data → fixed, verified.** `GET /api/admin/dam`, `/api/admin/regulated`, and `/api/admin/regulated/history` used `get_current_user`, so any authenticated supplier could read the full DAM price series and the regulated-charge table/history — while sibling admin GETs correctly required admin. Impact is limited (shared regulator/market reference data, not another supplier's private data or PII), but inconsistent with the endpoints' gating. **Fix:** switched all three to `require_admin`. Verified: supplier → 403, admin → 200, no supplier-portal regression (supplier.html never called these), public calculator still computes.
- [x] **Reviewer/demo setup was broken → fixed.** Migration `83ce50ff9ed3` used `ALTER COLUMN ... DROP NOT NULL`, which SQLite rejects, so `seed_demo_data.py` (the documented path for the external reviewer to stand up the app) crashed. **Fix:** wrapped in `batch_alter_table` — works on SQLite and PostgreSQL alike (identical DDL on Postgres).
- [~] **MED — rate-limit trust of `X-Forwarded-For` → documented (deployment fix, not code).** The per-IP limiter keys on `request.client.host`, which behind a proxy comes from `X-Forwarded-For` via uvicorn's proxy-header handling. Rotating that header created unlimited buckets **when the caller is a trusted proxy IP** (as in loopback testing); a remote attacker against a directly-exposed instance can't do this today. A code change to parse XFF would *introduce* the spoof, so the correct fix is deployment config: documented in `AZURE_DEPLOYMENT_CHECKLIST.md` Step 6a — never set `FORWARDED_ALLOW_IPS=*`, ensure the front end overwrites client XFF, and note the per-account lockout (not the IP limiter) is the real brute-force defense.
- **False positives ruled out during this round** (recorded so they aren't re-investigated): supplier tariff list "leaking Volt" was an automated-check artifact matching the substring in `"voltage"` (scoping is correct); `regulated` "leaking" in public/config was a match inside changelog text (no raw pricing is exposed). **Correction 2026-10-19:** that changelog text was itself a leak (audit log with staff emails and unapproved tariffs' prices); see Round 20.
- **Confirmed still solid:** anon → all admin routes 401; supplier → admin-only reads/writes 403; cross-supplier tariff GET/PUT/PATCH/DELETE denied; supplier self-approve denied; doc-download 404-uniform (Round 8 fix holds); input validation (NaN/Infinity/oversized) all 422 (Round 8 fix holds); no login/forgot-password enumeration; session cookie carries HttpOnly + SameSite + Secure.

---

## Round 10 — API split by role, deny-by-default (2026-09-30)

- [x] **Admin and supplier portals shared `/api/admin/*` → split, verified.** Suppliers previously called `/api/admin/*` routes, whose handlers branched on role internally. That was allow-by-default: any handler guarded with `get_current_user` instead of `require_admin` was open to suppliers. This is how the Round 3 changelog/supplier-contact leaks and the Round 9 DAM/regulated leak happened. **Fix:** `/api/admin/*` is now guarded router-wide by `require_admin`. A new `/api/supplier/*` router is guarded router-wide by a new `require_supplier` and scoped to the caller's own supplier. Shared logic lives in `routers/shared.py`, and `supplier.html` was moved to the new routes. Another supplier's tariff/document/message returns 404, the same as a missing one.
- [x] **Supplier could reassign its own tariff to another supplier → fixed, verified.** `PUT` on a tariff only checked the tariff's *current* owner, then copied `body.supplier` onto it. A supplier could therefore move its own tariff under a competitor's name. The supplier route now rejects any `body.supplier` other than the caller's own (403).
- [x] **Supplier could mark/ack messages not addressed to it → fixed.** Minor: this only created a read record for itself. Read/ack now 404 unless the message targets the caller's supplier and isn't archived.
- **Verified live** (disposable SQLite DB, email disabled): every route in the OpenAPI schema was enumerated. Anon → 401 on all admin and supplier routes. Supplier → 403 on **every** `/api/admin/*` route. Admin → 403 on every `/api/supplier/*` route. Full supplier flow worked end to end: list, create (→ pending), edit, delete, upload/list/download doc, read/ack message, profile picker receives id/name/desc only. Cross-supplier create/edit/reassign/delete/upload/list/download/read were all blocked. Admin flow was unchanged (config, CRUD, approve, docs, messages with ack status, users, notices, DAM, regulated). The public calculator was unaffected. 162 requests, 0 failures.

---

## Round 11 — Supplier-submitted data validation (2026-09-30)

Reviewed every field a supplier can send. Ownership checks were already complete after Round 10; the gaps were in the tariff **content**.

- [x] **HIGH — one malformed tariff could take the public calculator down → fixed, verified.** `rates` (`dict[str, Any]`) and `discounts` (`list[Any]`) were stored unvalidated and fed straight into the pricing engine. A price or discount sent as text, a nested object, or a non-object discount was accepted. Once approved, it made `/api/public/calculate` return 500 **for every customer**. Admin approval didn't catch it, because the admin view renders `"0.15"` the same as `0.15`. **Fix:** a strict per-pricing-type schema (`FixedRatesIn`/`TouRatesIn`/`DynamicRatesIn`/`VariableRatesIn`/`DiscountIn` in `schemas.py`). It enforces numbers only, finite values and sane bounds; unknown keys are dropped rather than stored. It applies to supplier, admin editor and Publish alike.
- [x] **MED — absurd or negative values accepted → fixed.** Negative prices (shown to customers as a −€19,718/yr bill and ranked #1), 1e300, NaN standing charges, −300% "discounts", nonexistent profile IDs, and multi-MB junk in `rates` were all accepted. Now: energy prices 0–`TARIFF_MAX_ENERGY_RATE` (default €5/kWh), monthly charges 0–`TARIFF_MAX_MONTHLY_CHARGE` (default €1,000), discounts above 0 and up to 100%, and the profile must exist. Limits are adjustable without code (`config.py`, `ADMIN_MANUAL.md` §6.10). `Infinity` previously caused a 500 on save; it is now a clean 422.
- [x] **Defense in depth — calculator failure isolation.** `/api/public/calculate` now prices each tariff independently. A tariff the engine can't handle, such as a legacy row stored before validation existed, is skipped and logged instead of failing the whole response. Verified with a malformed row inserted directly into the database: the comparison still returns 200 with all other tariffs intact.
- [x] **MED — email change without re-authentication → fixed.** `PUT /api/auth/email` did not ask for the current password, so a stolen session could change the email and then take the account over via forgot-password. It now requires `current_password` (both portals updated).
- [x] **Functional — supplier discounts never worked → fixed.** `supplier.html` saved discounts as `{label, pct, euro}`; the engine, customer page and admin form use `{type, percentage, durationMonths, conditions}`. Supplier-entered discounts were silently ignored in prices and would have shown "undefined%". The supplier form now uses the shared format (the unsupported "€ off" type was dropped). The admin review panel had the mirror-image bug and showed admin-format discounts as "undefined"; this is also fixed.
- [x] **Supplier deletion of live tariffs → archive + audit.** Any tariff that has **ever** been approved becomes `archived` when a supplier deletes it: hidden from customers, read-only in the supplier's list, visible to admins, restorable by an admin, logged. This is tracked by a new `tariffs.everPublished` flag (migration `5c1e7a9d2f40`, backfilled from current status plus changelog approval history). The flag is set automatically on any transition to `approved`, so a live tariff edited back to pending, or later rejected, is still archived rather than erased. Tariffs never approved are deleted outright, also logged.
- **Verified live** (disposable SQLite DB, email disabled): 24 malformed inputs → all 422. 10 valid edge cases (limits, negative FPA/adder, every pricing type, admin-format discounts) → 201. Every seeded tariff re-saves unchanged, and all 11 tariffs in the dev database pass the new schema unchanged (read-only check). Archive, restore and audit flow all passed. Email re-auth: missing/wrong/right password → 422/400/200. Browser run in Edge (Playwright) of both portals: discount entry round-trips in the new format, validation errors are readable, archived badge and read-only row shown, email form asks for the password, admin review shows the discount correctly. No JS exceptions on supplier, admin or customer pages.

---

## Round 12 — "Save & publish" removed (2026-09-30)

- [x] **HIGH — "Save & publish" replaced all data from a browser snapshot → removed, verified.** `PUT /api/admin/config` deleted every supplier, profile and tariff and re-created them from the admin's in-browser copy. Because `TariffIn` has no `status`, every tariff came back **approved**: pending, draft, rejected, suspended and archived tariffs went live, and `rejection_reason`/`mdmSource`/`mdmInvoiceMonths` were lost. Suppliers came back with new IDs and without their `regulated` flag. Verified on a throwaway SQLite DB (the reviewer-demo setup), where one click made a pending, a draft and a rejected tariff public. On PostgreSQL the supplier delete violates the `users`/`message_reads` foreign keys, so the call failed and rolled back; the dev DB has 2 supplier logins and 4 read records, so it was likely never damaged. The feature dated from the browser-storage era and had been redundant since every section gained its own save (§16.3 of the architecture review). **Fix:** removed the Publish page, button, menu item and endpoint (`PUT /api/admin/config`, `ConfigImportIn`). `GET /api/admin/config` stays, as the admin panel's data load. Confirmed every admin section saves through its own endpoint.
- [x] **Admin "View → Delete" never reached the server → fixed, verified.** `editorDeleteFromViewer()` only removed the tariff from the page and relied on Publish to persist it. The API-backed `deleteTariff()` existed but was never called. The tariff reappeared on reload and stayed on the customer calculator. It now calls the server first and updates the page only on success. Verified: the tariff is gone server-side, stays gone after reload, and the deletion is logged.
- [x] **`seed.py` could wipe a live database.** It shares `import_cfg()`, which replaces all data. It now refuses to run against a database that already has suppliers or tariffs unless `--force` is given. Verified against a populated demo DB: refused, nothing changed.

---

## Round 13 — Whole project folder was publicly downloadable (2026-09-30)

- [x] **CRITICAL — server exposed secrets, source code, git history and internal documents → fixed, verified.** The static files were served by a `StaticFiles` mount of the entire project folder, so anyone who could reach the server could download `tariff-api/.env` (JWT signing secret, Azure client secret, database credentials), all source code, `.git/` (the full repository history), internal documents (`handover.docx`, security/architecture reviews, deployment plans), the SQLite fallback DB file and uploaded tariff PDFs (bypassing the authenticated download endpoint). `start.bat` binds `0.0.0.0:8000`, so on the CERA workstation that meant anyone on the same network. Found while planning the admin network restriction; verified by requesting each path from a throwaway instance (status codes only, contents never read). **Fix:** the mount is replaced by explicit routes for exactly five files (`customer.html`, `supplier.html`, `admin.html`, `reset-password.html`, `Logo_Transparent.png`). Everything else is 404, including case variants and encoded paths. Verified: 20 sensitive/trick paths all 404; the 5 public files and the API unaffected.
- [ ] **Follow-up (manual): rotate the secrets that were exposed**: `TARIFF_SECRET_KEY` (signs sessions; rotating it signs everyone out), the Azure app client secret, and the PostgreSQL password. This matters if the local server was ever reachable by other machines (Windows Firewall / network setup). The external repo history is unaffected; `.env` was never committed.

## Round 14 — Admin access restricted to the CERA office / VPN networks (2026-09-30)

- [x] **Admin accounts usable from anywhere on the internet → restricted, verified.** New setting `TARIFF_ADMIN_ALLOWED_NETWORKS` (CIDR list; empty = off with a startup warning). Outside those networks, the only response is a generic "Website unavailable" (404) for all of the following:
  - `admin.html`;
  - admin sign-in, checked *before* the password, so no password oracle and no lockout DoS from the internet;
  - OTP verify/resend;
  - every authenticated admin request, enforced in `get_current_user` for the admin role, so a stolen cookie or a dropped VPN mid-session gets nothing.

  Blocked sign-ins are logged as `network_blocked`. Suppliers and customers are unaffected.
- [x] **Trusted client IP (`client_ip.py`), which closes the Round 9 `X-Forwarded-For` item.** With `TARIFF_TRUSTED_PROXY_HOPS=1` (Azure), only the rightmost `X-Forwarded-For` entry, the one appended by the Azure front end, is trusted. Client-supplied entries further left are ignored, ports are stripped, and unparseable values are treated as "not allowed". The rate limiter and all IP logging (login activity, tariff reports) now use the same helper, so rotating `X-Forwarded-For` no longer escapes the rate limit.
- **Verified live** on throwaway servers, for four configurations: restriction on with this machine allowed; on with it outside; behind-proxy mode; off.
  - Admin sign-in with the correct password from outside → 404, `network_blocked` logged, and 6 wrong passwords caused no failed-attempt count or lockout.
  - OTP started inside and finished outside → 404.
  - All 46 admin API routes with a valid admin cookie → 404 "Website unavailable".
  - `admin.html` → plain page with no branding; the public pages, supplier sign-in and flows, and the calculator all work.
  - Spoofed `X-Forwarded-For` (allowed IP first, real IP appended) → blocked; no header → blocked; a rotating header can't dodge the rate limit.
  - Browser (Edge): admin working inside, VPN drops, next click shows only "Website unavailable", no "Leave site?" prompt.
  - Earlier suites rerun unchanged: role separation 160/160 and unsaved-changes 28/28.
- [ ] **On Azure before go-live:** set both settings (see `AZURE_DEPLOYMENT_CHECKLIST.md` Step 6a) with the office and VPN addresses from CERA IT, then confirm from the VPN and from mobile data that the IP the app sees is right. This can't be simulated locally.

## Round 15 — Automated scanners (2026-10-02)

The first run of off-the-shelf scanners, so findings no longer depend on manual review alone.

- [x] **pip-audit (third-party libraries): 13 advisories in PyJWT 2.13.0 → upgraded to 2.15.1, verified.** The app only uses HS256 with one fixed secret and a single-algorithm allow-list (no JWK/JWKS, no public-key algorithms), so most advisories didn't apply; the upgrade clears them all. Verified on a throwaway server: admin and supplier sign-in and OTP work; tampered, malformed, `alg=none` and wrong-key tokens all get a clean 401 (never a 500). Re-run: no known vulnerabilities.
- [x] **bandit (Python code): 11 low-severity results, 0 real problems.** The 2 non-cryptographic random-ID results were hardened anyway: `_uid()` (tariff, report, message and changelog IDs) used `random.choices` with 4 characters. It now uses `secrets` with 8 characters, and the duplicate copy in `main.py` is replaced by the shared one. This wasn't exploitable, since every access is ownership-checked, but IDs are no longer guessable from the creation time. Verified: role suite 160/160, public report works, new IDs in the new format. The 9 accepted results:
  - `config.py:36`: the labelled dev-only key, used only with an explicit `TARIFF_ALLOW_DEV_SECRET=1`, with a warning;
  - `main.py:121`: deliberately ignores an unreadable login body when logging a rate-limit hit;
  - `seed_demo_data.py`: the fake demo password;
  - `scripts/verify_customer_calc.py`: `assert` statements in a verification script.
- [x] **gitleaks (secrets): clean.** All 62 commits scanned, including the extracted text of every Word/PDF ever committed; the two image-only PDFs were checked by eye (architecture diagrams, no values). The only secrets on disk are in `tariff-api/.env`, which is git-ignored and was never committed (see Open items: production secrets in Key Vault).
- [x] **semgrep (code patterns):** can't run on the development PC (no Windows build, and WSL needs admin rights). Moved to GitHub Actions (Round 16).
- [x] **OWASP ZAP (attack test against a running throwaway copy):** a 2-minute rehearsal ran locally; the full scan moved to GitHub Actions (Round 16). The development PC's managed ESET network protection treats ZAP's probes as real attacks: it blocked 27 of them ("PHP/CVE-2024-4577"), which also distorts results. ZAP is therefore not run on CERA workstations.

## Round 16 — Automated scans on GitHub Actions; rehearsal findings (2026-10-02)

- [x] **Two workflows, on GitHub's throwaway Linux machines.** They use no repository secrets and never read `.env`. Permissions are read-only, and every third-party step is pinned (actions by commit SHA, images by version, gitleaks by version plus SHA-256). Details are in `REVIEWER_SETUP.md` → "Automated security checks".
  - `security-checks.yml`: pip-audit, bandit, semgrep and gitleaks, on every push and every Monday. The Monday run catches newly published library vulnerabilities even when the code hasn't changed.
  - `zap-scan.yml`: ZAP as visitor, demo supplier and demo admin, against a copy with fake demo data, every Monday and on demand.
  - **Policy:** a run fails (❌ + email) on any library vulnerability, any secret, high-severity bandit, ERROR-severity semgrep, or a High-risk ZAP alert. Everything else is reported in the run's artifacts, which are kept 30 days, and reviewed in batches here.
- [x] **Accepted bandit results** (low severity; they don't fail the run):
  - `config.py`: the labelled dev-only key (B105);
  - `main.py`: the deliberate try/except/pass in rate-limit logging (B110);
  - `seed_demo_data.py`: the demo password (B105);
  - `scripts/verify_customer_calc.py`: `assert` statements (B101).
- [x] **First full ZAP scan in CI (run 37010580557, 2026-10-02).** It was signed in as visitor, supplier and admin: 57/57 admin and 13/13 supplier actions, about 270,000 attack requests, sessions valid to the end.
  - Two earlier attempts had to be fixed first. The first only reached public pages: the spider failed on the 404 site root, and the OpenAPI-only requests carried made-up IDs. That led to `zap_scan.py`, which drives realistic traffic and has a coverage guard.
  - **1 High alert, "SQL Injection" on `PUT /api/admin/profiles/{id}` → false positive.** Profile values are `json.dumps`-ed and stored through SQLAlchemy's parameter binding; the only raw SQL in the app is the `SELECT 1` health check. ZAP was misled because the endpoint echoes back what it stored, so its `…1=1` / `…1=2` payloads came back as two different responses.
  - **But it exposed a real gap, now fixed:** profile `months` was `list[Any]`, so an admin could store text, nested objects, negative or absurd values. Verified on a throwaway copy: **one text value made the public calculator return no tariffs at all**, silently. (Admin-only, office/VPN-restricted; the risk is a mistake, a UI bug or a compromised admin account.)
    - **Fix:** new `ProfileMonthIn` schema: exactly 12 months, exactly 48 + 48 strict, finite numbers each, 0 to 1,000,000, with bounded counts. The admin page shows the readable error (`apiErrorText`), and `ADMIN_MANUAL.md` §8 is updated.
    - **Verified:** 27 checks (6 valid paths including rename, 19 malformed variants → 422, stored profile and calculator unchanged). The 3 real dev-DB profiles pass, checked read-only (values 0.03–0.29). Role suite 160/160; scan-script dry run 57/57 + 13/13.
  - The active scan reached only ~30% of its rules in the 35-minute cap. The cap is now 110 minutes, about 520 of the 2,000 free minutes a month.
- [x] **Getting ZAP to finish a full scan (2026-10-05).** Three runs stopped partway, each for a scan-setup reason, not because of the app:
  - DOM-XSS rule: its headless browser exhausted Docker's 64 MB shared memory. Now `--shm-size=2g`.
  - A dropped connection to ZAP's API under load. ZAP API calls now retry.
  - ZAP's Java memory reached 99% at 91% of the scan, and ZAP shut itself down. Now `-Xmx4g`. The informational "User Agent Fuzzer" rule is disabled: it alone sent 1,775 requests and raised 666 notes.
- [x] **First complete full ZAP scan, run 37285323887 (2026-10-05): passed, 0 High.** About 88 minutes, ~858,000 attack requests; admin 57/57 and supplier 13/13 actions.
  - **No SQL injection.** The SQLi alert from the earlier, interrupted runs didn't recur once profile validation was in place.
  - **Medium, Subresource Integrity missing on the cdnjs scripts → fixed.** Chart.js 4.4.1 and DOMPurify 3.1.6 in `customer.html` and `admin.html` now carry `integrity="sha512-…"` and `crossorigin="anonymous"`. The hashes were computed from the files and match cdnjs's published values; cdnjs sends `Access-Control-Allow-Origin: *`. If cdnjs ever served a modified file, the browser would refuse to run it.
  - **Medium, SRI missing on the Google Fonts stylesheet → accepted.** SRI isn't possible there: Google generates that CSS per browser. A stylesheet can't run scripts, and `font-src`/`style-src` in the CSP limit it to Google's domains. Self-hosting the font would remove it, if wanted.
  - **Medium, CSP allows `'unsafe-inline'` for scripts and styles → open, planned as a separate task** (see the open items below). Inline scripts are currently mitigated by output escaping, DOMPurify and the DOM-node rendering from the July XSS fixes.
  - **Low, "XSS weakness (persistent in JSON response)" ×14 → accepted by design.** ZAP stored `<script>` text and the JSON API returned it exactly as stored. Text is stored as entered and made safe when the page displays it (escaping and DOMPurify, from the July fixes). ZAP raised it with low confidence, since the response is `application/json`, not HTML. To be confirmed in a real browser by the planned attacker test suite.
  - **Low, cross-domain JavaScript inclusion → accepted.** These are the same two cdnjs scripts, now SRI-pinned.
  - **Info, comments in HTML/JS → accepted.** Developer explanations only (e.g. "minutes from midnight"); no credentials, internal hosts or hidden endpoints.
- [x] **Accepted false positive: "SQL Injection" (ZAP rule 40018) on `PUT /api/admin/profiles/{id}`.** The first scheduled scan (run 37330744487, 2026-10-05) failed on it, this time on the `desc` field. Investigated and confirmed not a vulnerability; recorded as an accepted exception in the scan's pass/fail step.
  - **What ZAP did:** it saved the description once ending `… AND 1=1 -- ` and once ending `… OR 1=1 -- `. It saw two different replies and concluded the database had obeyed the injected condition.
  - **Why it's false:**
    1. **No SQL is built from text.** The profile is saved by assigning attributes on an SQLAlchemy ORM object (`routers/admin.py`, `update_profile`), which sends values as bound parameters; the text is stored as data, never executed. A search of the app found one hand-written SQL statement, the constant `SELECT 1` health check (`main.py`).
    2. **The two replies differed for an unrelated reason.** The endpoint returns the whole saved profile: name, description and 12 months × 96 values. ZAP runs 4 attack threads at once, and other threads were rewriting the same profile's other fields between the two probes. ZAP only discounts the field it attacked, so the rest of the reply had changed.
    3. **Not reproducible.** Same endpoint in runs 37010580557 and 37330744487; absent from the complete run 37285323887, which sent the same probes. A real injection would be found every time.
    4. **Input validation.** Since `a9c09c7` every field of a profile is validated (`ProfileIn`/`ProfileMonthIn`): text lengths are capped, and month values must be finite numbers. Text fields are still accepted as entered, which is correct for a description.
  - **Options considered:**
    - Change the endpoint to stop echoing the saved profile. That would remove the trigger, but it changes working code for a scanner's sake, makes this endpoint inconsistent with every other save endpoint, and would not stop the same effect elsewhere.
    - Scan one request at a time. That would avoid the parallel changes, but the weekly scan would take several hours.

    Both were rejected in favour of a documented exception (decision of the tool owner, 2026-10-06).
  - **How the exception is limited:**
    - It's defined in `.github/scripts/zap_gate.py` (`ACCEPTED`) and matches only rule 40018, method `PUT`, path `/api/admin/profiles/{id}`, parameters `name`/`desc`.
    - SQL injection on any other endpoint, method or parameter (including `months`), or any other High alert, still fails the run. This was verified against the real report and five altered copies (other parameter, endpoint, method, rule, and an extra instance elsewhere): all five failed as intended.
    - It isn't hidden: every run's summary lists it as "High (accepted)" with this justification, and the full ZAP report still contains it.
  - **Review:** re-assess if the profile endpoint changes or if raw SQL is ever introduced. Any new accepted exception needs its own entry here.
- [x] **Windows-only: the local dev server can be knocked offline. Recorded, not fixed.** The cause is uvicorn on Windows with the default Proactor event loop: after one abruptly reset connection fails in `accept()` (WinError 64), it permanently stops accepting connections.
  - Reproduced during the ZAP rehearsal, where ESET's resets triggered it. A Selector-loop server survived 300 deliberately reset connections.
  - Affects only `start.bat` local development, which isn't reachable from the network.
  - Production on Azure App Service runs Linux, where this code path doesn't exist.
- Design note for the inspection: sign-out clears the browser cookie, but tokens are stateless JWTs. A copied token stays valid until it expires (1 hour sliding, 12-hour absolute cap). This is standard for JWT sessions; server-side revocation would need a token blocklist or version counter.

## Round 17 — Attacker (abuse-case) test suite (2026-10-06)

Generic scanners can't know this app's rules (e.g. "Acme must not touch Delta's tariffs"). So the earlier one-off attack scripts were turned into a permanent suite, and the missing scenarios were added: `tariff-api/tests/security/`, 128 pytest tests, about 2.5 minutes.

- [x] **The suite.** Each test attempts one specific misuse over real HTTP against a throwaway server and checks that it is refused.
  - **Setup:** fake demo data, a random signing key, email off; `.env` is not read (disabled in `_server.py`). Uploads go to a temp folder.
  - **The 9 groups:**
    1. role separation on every admin/supplier route (taken from the app's route list, so new routes are covered automatically), plus the office/VPN restriction, including a spoofed `X-Forwarded-For`;
    2. supplier-to-supplier isolation, including extra fields in saves (mass assignment);
    3. forged, altered, `alg: none`, expired, over-12-hour, half-finished (OTP pending) and deactivated sessions, and a claimed admin role in a validly signed supplier token;
    4. password and OTP guessing, lockout, code reuse, resend cooldown, the request limit;
    5. account discovery by reply content and timing;
    6. reset links (reuse, guessing, expiry, superseded, deactivated account, weak and reused passwords);
    7. stored XSS: payloads saved in every displayed free-text field (tariff name, document name, supplier details, messages, profiles, public reports, the login-activity email), then the customer, supplier and admin pages opened in headless Chromium. No markup is injected and no code runs. This closes ZAP's "XSS in JSON" Low.
    8. fake or oversized PDFs and path tricks in file names; absurd prices, consumption and profiles; garbage bodies to every POST/PUT/PATCH route (no HTTP 500);
    9. private files never served; CSP and hardening headers; cookie `HttpOnly`/`Secure`/`SameSite=Strict`.
- [x] **CI.** A new `attacker-tests` job in `security-checks.yml` runs the suite on every push/PR and every Monday; any failure fails the run. pytest 9.1.1 is pinned in `requirements-dev.txt`, which pip-audit already checks. semgrep now excludes `tariff-api/tests`, because the tests deliberately forge tokens (`alg: none`, guessed keys) that would rightly be flagged in app code.
- [x] **Finding 1 (bug, not a vulnerability): changing your own password signed you out, about 4 times in 5.**
  - **Cause:** PyJWT stores `iat` in whole seconds, while `password_changed_at` has microseconds. The fresh token issued by the password change looked older than the change itself (same second) and was refused.
  - **Fix:** tokens carry a precise `iat_precise`, used for that comparison (`auth.py`). Older tokens fall back to `iat`.
  - **Verified:** other sessions are still ended by a password change, with no window; the test passed 5/5 repeats.
- [x] **Finding 2 (Low): sign-in reply time revealed which emails are registered.**
  - **Cause:** the bcrypt check ran only for existing accounts, so replies took about 0.33 s for a real email and 0.03 s for a made-up one. That allowed building a list of real supplier/admin emails to target; the 3-try lockout still protected the passwords.
  - **Fix:** unknown emails are checked against a dummy bcrypt hash, so both take the same time (`routers/auth.py`).
  - **Verified:** the timing test passed 5/5 repeats (threshold 80 ms).
  - **Remaining by design:** admin emails used from outside the office/VPN get "unavailable" (404) instead of "invalid" (401). That is the Round 14 network restriction, which deliberately never checks admin passwords from outside. It does reveal that an address is an admin account, accepted in exchange for admins never being lockable from the internet.
- [x] **Everything else passed on the existing code (126 of 128 tests before the two fixes).**
- [x] **Proven to catch regressions.** On a throwaway branch with the supplier ownership check deliberately removed, CI failed the supplier-isolation tests: Acme's edit of Delta's tariff succeeded (run 37430128284). The branch was deleted unmerged. On `master` all five jobs pass (run 37430104947, about 1.5 minutes for the suite on GitHub).

## Round 18 — Stored XSS through a supplier-chosen tariff ID (2026-10-06)

- [x] **Finding (Medium–High), found while converting `customer.html` (Plan B).**
  - **Cause:** suppliers may choose their own tariff ID when submitting (`TariffIn.id`, previously any text up to 100 characters). The public page built each card's click handler as `onclick="toggleCard('${t.id}')"`, with the ID unescaped inside a JavaScript string.
  - **Impact:** an ID such as `x');…;('` breaks out of the string. Once an admin approved the tariff, which shows the ID only incidentally, the code would run in the browser of every visitor who opened that card.
  - **Requires:** a supplier account (or a stolen one) plus an admin approval.
  - **Why it was missed:** the July XSS review and Round 17's planted-text tests covered names, descriptions and other text fields, not IDs, because IDs were assumed to be app-generated.
  - **Proven:** with a new attacker test, the planted code ran on the unconverted page.
- [x] **Fixed in two independent layers:**
  1. **Server:** client-chosen IDs (`TariffIn.id`, `ProfileIn.id`, and the public report's `tariff_id`) must match `^[A-Za-z0-9_-]+$` (`schemas._ID_PATTERN`). A read-only check of the real database found all IDs already compliant: 11 tariffs, 3 profiles, 2 messages.
  2. **Page:** `customer.html` no longer puts any value into code. The ID goes into an escaped `data-arg` attribute, and the strict CSP would refuse such code anyway.
- [x] **Tests:** `test_7` checks that the API refuses such IDs (supplier, admin, profile, public report). It also plants one directly in the database, as if it predated the rule, and confirms that the customer, supplier and admin pages run nothing.
- [x] **Follow-up, closed 2026-10-07:** `admin.html` (profiles, messages, schedules, reports, tariffs) and `supplier.html` (message acknowledge) used to put IDs into handlers. Both conversions removed the pattern: IDs are now escaped `data-arg` attributes, and no page contains inline code (`test_9`).

## Round 19 — Regulated charges had no limits (2026-10-09)

- [x] **Finding (Medium; admin-only, office/VPN), found while adding the admin number-box rule.**
  - **Cause:** `PUT /api/admin/regulated` (`RegulatedIn`) accepted any number for the network, FPA, PSO, RES and MDM charges, which feed every tariff's cost in the public calculator. Tariffs and profiles already had limits.
  - **Proven on a throwaway copy:**
    - LV network charge `-5` → the public calculator showed regulated charges of **-€19,950**;
    - `1e300` → an absurd total;
    - `NaN` → that charge silently left out;
    - PSO `Infinity` → **stored, after which the public calculator and the admin's own Regulated page both returned HTTP 500**, recoverable only by editing the database.
  - **Reach:** NaN/Infinity need a direct API call by a signed-in admin from the office or VPN, and the admin form could send negative or huge values. So the realistic causes are a typo, a page bug, or a compromised admin account taking the public calculator down.
- [x] **Fix:** `RegulatedIn` uses the same limits as tariffs (`schemas._energy`/`_monthly`, which also refuse NaN/Infinity):
  - network, PSO and RES: 0 to 5 €/kWh;
  - FPA: -5 to 5 €/kWh (fuel adjustment can be negative);
  - MDM: 0 to 1,000 €/month.

  A read-only check of the real database found the current values well within these limits (e.g. LV 0.0393, MDM 0.94).
- [x] **Admin page:** a refused save outlines each wrong box with its message (e.g. "This cannot be more than 5."). It used to show the raw reply ("[object Object]").
- [x] **Tests:**
  - `test_8`: 13 refused cases (negative, too large, text, NaN, ±Infinity, per field), each leaving the stored values and the public calculator unchanged; also valid edge values, including a negative FPA.
  - `test_11`: the page shows a refusal on its fields and stores nothing.
  - Full suite: 188 passed.

## Round 20 — Whole-app review with Anthropic's security-review method (2026-10-19)

The prompt and false-positive rules of `anthropics/claude-code-security-review` were applied to the whole codebase, not just a diff. Two findings; everything else (SQL injection, access control, login/OTP/reset, CSRF/CORS, uploads, email escaping, TSOC fetch, CI workflows) was clean.

- [x] **Finding 1 (High): the public config carried the whole audit log.**
  - **Cause:** `GET /api/public/config` (no sign-in) returned every changelog entry, although `customer.html` never used it.
  - **Exposed:** before/after rates and discounts of tariffs still pending, rejected or never approved (a competitor could read another supplier's prices before CERA approves them); supplier staff emails (`actorEmail`); and which accounts have 2FA switched off (OTP changes are logged under the user's email).
  - **Why it was missed:** Round 9's black-box test looked at that text for raw pricing only and recorded it as a false positive (corrected there).
  - **Fix:** the public config no longer includes the changelog. Admins still get it from `/api/admin/config` and `/api/admin/changelog`.
- [x] **Finding 2 (Medium): supplier text became markup on the public results page.**
  - **Cause:** a discount's `conditions` (supplier free text, up to 500 characters) was the one value in `customer.js` `renderDiscountToggles` not passed through `esc()`.
  - **Impact:** once an admin approved the tariff (the review shows the text plainly, so markup is easy to miss), it became page markup for every visitor who opened the card. The strict CSP stops scripts from running, but inline styles are allowed, so a supplier could hide competitors' results or add a misleading link.
  - **Fix:** `esc(d.conditions)`.
- [x] **Tests:**
  - `test_2`: Delta submits an unapproved tariff and an admin toggles a user's 2FA. The public config must show neither, no sign-in account email, and no changelog. The test checks first that both did reach the admin's log.
  - `test_7`: the planted text now also goes into a discount condition, and the test checks that it is displayed on the public card as plain text.
  - Both new checks failed on the old code (the leak was visible; 2 injected elements on the customer page) and pass after the fix. Full suite: 224 passed.
  - `zap_scan.py`: the supplier's tariff gets a discount with conditions, and after the admin approves it a visitor loads the results, so ZAP scans that field on the public page. The script's dry run completed against a throwaway copy.

## Open items — must be handled before go-live

These are deployment/production tasks, tracked in full in `AZURE_DEPLOYMENT_CHECKLIST.md` and project memory.

- [ ] **HTTPS** — load-bearing, not just good practice: the `Secure` session cookie means login silently fails over plain HTTP on a real domain.
- [ ] **Production secrets** — set a real random `TARIFF_SECRET_KEY` (never the dev fallback) and real Azure/Graph credentials in Key Vault.
- [ ] **Admin network restriction settings on Azure** (`TARIFF_ADMIN_ALLOWED_NETWORKS`, `TARIFF_TRUSTED_PROXY_HOPS=1`) with addresses from CERA IT, and a VPN full-tunnel confirmation (Round 14; checklist Step 6a). This replaces the earlier `X-Forwarded-For` trust item, now handled in code.
- [ ] **Disable API docs in production** — set `TARIFF_ENABLE_DOCS=0` so `/docs`, `/redoc`, `/openapi.json` don't expose the full route surface.
- [x] ~~Restrict `admin.html` to CERA IPs~~: done in-app (Round 14); covers the admin API too, not just the page.
- [ ] **Rotate secrets exposed by the static-file issue** (Round 13).
- [x] **Removed `'unsafe-inline'` from the CSP `script-src`** (ZAP Medium, Round 16), page by page; done 2026-10-07. One strict policy now applies to every page and response.
  - **How:** each page's code moves to its own `.js` file, and inline handlers are replaced by listeners. The page then gets the strict `script-src 'self' https://cdnjs.cloudflare.com`; while converting, pages not yet done kept the old policy through a temporary `_CSP_LEGACY_PAGES` set in `main.py`, now deleted.
  - **Enforced by the attacker suite:**
    - `test_9`: converted pages contain no inline code and are served with the strict policy;
    - `test_10`: every converted page is clicked through in headless Chromium, with zero CSP violations or script errors allowed.
  - **Done:**
    - `reset-password.html` (2026-10-06). Verified in the browser: code planted into the page is refused, with a CSP violation recorded, while on a not-yet-converted page the same code ran.
    - `customer.html` → `customer.js` (2026-10-06).
      - All ~70 handlers, including those generated for cards, discounts and estimator options, now use `data-action` and a fixed action table. Hover colours moved to CSS.
      - 5 click-through tests cover every control and modal. `verify_customer_calc.py` passes, and the full suite passes (144 tests).
      - This also removed the Round 18 code path.
    - `supplier.html` → `supplier.js` (2026-10-06).
      - Both script blocks are merged into `supplier.js`, and all ~47 handlers are replaced, including the message-acknowledge button, which put an ID into code.
      - 7 click-through tests cover:
        - sign-in, forgot-password, sign-in with an emailed code, sign-out;
        - tariff form (all selects, discounts, tiers, submit, edit, delete);
        - documents (upload, download) and messages (acknowledge);
        - account password change, idle warning, expired-password gate.
      - Full suite passes (155 tests).
    - `admin.html` → `admin.js` (2026-10-07).
      - Both script blocks are merged, and all 196 handlers are replaced (162 click, 23 change, 6 input, 2 Enter-key, 3 drag-and-drop).
      - Two places that found buttons by their `onclick` text were updated: the sidebar highlight, and the tariff editor's unsaved-changes check.
      - IDs no longer go into code (this closes the Round 18 follow-up).
      - `admin.js` is served only inside the office/VPN, like `admin.html` (tested from outside, with a spoofed header, and with no proxy header).
      - 9 click-through tests (`test_11`) cover every one of the 13 sections and their main actions:
        - review, approve, suspend, restore; editor with discounts and tiers; documents;
        - suppliers, including the regulated toggle; users (invite, unlock, OTP, deactivate, reinvite, delete);
        - profiles; messages and schedules;
        - DAM upload by picker and by drag-and-drop; regulated charges and history; audit; notices formatting; reports; changelog export;
        - account, idle warning, expired-password gate, sign-in with a code.
      - Full suite passes (170 tests).
      - Two existing admin bugs were found by these tests and fixed:
        1. **"Regulated supplier" could never be changed:** confirming the change did nothing, because the code read the checkbox after the browser had already flipped it (since `b2e9d3b`).
        2. Some refusals (e.g. an invalid email when inviting a user) showed **"[object Object]"** instead of the reason. Now they're readable (`apiErrorText`).
  - **Confirmed by ZAP (run 37889993604, 2026-10-09; full scan, about 623,000 attack requests):**
    - the "CSP: script-src unsafe-inline" Medium is gone, and so is the "cross-domain JavaScript" Low;
    - 0 High;
    - remaining: style-src (below), SRI on Google Fonts (accepted, Round 16), XSS-in-JSON Low (accepted, now also proven safe in the browser by `test_7`), and Info notes.
  - **Not done (decision pending):** `style-src 'unsafe-inline'`. Inline styles can't run code, so ZAP's style-src item is Medium only by rule; removing it would mean moving ~770 `style="…"` attributes into CSS classes.
- [ ] **Rate limiter is in-memory/single-process** — needs a shared store (e.g. Redis) only if ever scaled to multiple workers/instances.
- [ ] **External IT certification** — this document is the security summary to hand over.
- [~] **Round 6 follow-up** — live UI walkthrough confirming `ConfigImportIn` accepts every real "Publish" payload.

---

*Historical detail beyond this summary lives in `TECHNICAL_ARCHITECTURE_REVIEW.md`, `SECURITY_REMEDIATION_PLAN_customer_data_exposure.md`, and project memory. Compliance (Article 121) work is tracked separately and is not a security-hardening concern.*
