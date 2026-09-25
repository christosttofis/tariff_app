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
- **False positives ruled out during this round** (recorded so they aren't re-investigated): supplier tariff list "leaking Volt" was an automated-check artifact matching the substring in `"voltage"` (scoping is correct); `regulated` "leaking" in public/config was a match inside changelog text (no raw pricing is exposed).
- **Confirmed still solid:** anon → all admin routes 401; supplier → admin-only reads/writes 403; cross-supplier tariff GET/PUT/PATCH/DELETE denied; supplier self-approve denied; doc-download 404-uniform (Round 8 fix holds); input validation (NaN/Infinity/oversized) all 422 (Round 8 fix holds); no login/forgot-password enumeration; session cookie carries HttpOnly + SameSite + Secure.

---

## Open items — must be handled before go-live

These are deployment/production tasks, tracked in full in `AZURE_DEPLOYMENT_CHECKLIST.md` and project memory.

- [ ] **HTTPS** — load-bearing, not just good practice: the `Secure` session cookie means login silently fails over plain HTTP on a real domain.
- [ ] **Production secrets** — set a real random `TARIFF_SECRET_KEY` (never the dev fallback) and real Azure/Graph credentials in Key Vault.
- [ ] **`X-Forwarded-For` / `FORWARDED_ALLOW_IPS` trust** configured correctly at the proxy (Round 9 above; checklist Step 6a).
- [ ] **Disable API docs in production** — set `TARIFF_ENABLE_DOCS=0` so `/docs`, `/redoc`, `/openapi.json` don't expose the full route surface.
- [ ] **Restrict `admin.html`** to CERA IPs (checklist has the procedure).
- [ ] **Rate limiter is in-memory/single-process** — needs a shared store (e.g. Redis) only if ever scaled to multiple workers/instances.
- [ ] **External IT certification** — this document is the security summary to hand over.
- [~] **Round 6 follow-up** — live UI walkthrough confirming `ConfigImportIn` accepts every real "Publish" payload.

---

*Historical detail beyond this summary lives in `TECHNICAL_ARCHITECTURE_REVIEW.md`, `SECURITY_REMEDIATION_PLAN_customer_data_exposure.md`, and project memory. Compliance (Article 121) work is tracked separately and is not a security-hardening concern.*
