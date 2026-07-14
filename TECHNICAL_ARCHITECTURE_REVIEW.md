# CERA Tariff Comparison Tool — Technical Architecture & Security Review

**Document purpose:** technical reference for an expert/external reviewer (functional + security assessment) prior to production go-live. Reflects the codebase as of 2026-07-14.

**Scope:** full-stack review of `tariff-api/` (FastAPI backend) and the three static frontend applications (`admin.html`, `supplier.html`, `customer.html`) plus supporting scripts.

---

## 1. System overview

A tariff comparison and regulatory-approval tool for the Cyprus Energy Regulatory Authority (CERA). Three audiences, three portals, one backend:

| Portal | File | Auth | Purpose |
|---|---|---|---|
| Customer calculator | `customer.html` | None (public) | Compare electricity tariffs from approved suppliers |
| Supplier portal | `supplier.html` | JWT + OTP 2FA | Suppliers submit/edit their own tariffs, upload supporting documents, read CERA broadcast messages |
| Admin panel | `admin.html` | JWT + OTP 2FA | CERA staff approve/reject tariffs, manage suppliers/users/regulated charges/DAM data, send broadcast messages |

**Stack**

- Backend: Python 3.14, FastAPI, SQLAlchemy 2.0 (sync ORM), served by `uvicorn`
- Database: PostgreSQL 17 (migrated from SQLite on 2026-07-10; SQLite remains as a fallback if `DATABASE_URL` is unset — used by the IT-review test package)
- Auth: PyJWT (HS256), `bcrypt` for password hashing (direct `bcrypt` library, not `passlib`)
- Email: Microsoft Graph API via `msal` (OAuth2 client-credentials flow), no SMTP/passwords
- Frontend: no build step, no framework — three self-contained static HTML files with inline CSS and vanilla JS, served by FastAPI's `StaticFiles` mount
- Process model: single uvicorn process; an `asyncio` background task inside the same process handles scheduled notifications and password-expiry checks (no separate worker/queue)

**Repository layout (relevant files)**

```
tariff-api/
  main.py            FastAPI app, CORS, static mount, startup schema migrations, background scheduler
  auth.py            JWT issuance/verification, password hashing/policy, lockout-aware get_current_user
  database.py        SQLAlchemy engine/session (Postgres via DATABASE_URL, SQLite fallback)
  models.py          ORM models (16 tables)
  schemas.py         Pydantic request schemas
  serializers.py      ORM → dict serializers shared by public/admin endpoints
  importer.py        Bulk config import (legacy "Publish" flow)
  email_utils.py     Graph API email templates and sending
  routers/auth.py    /api/auth/* — login, OTP, password reset/change
  routers/admin.py   /api/admin/* — all authenticated CRUD + messaging + scheduling
  create_user.py     CLI: create/update/deactivate a user account
  unlock_user.py     CLI: clear an account lockout
  seed.py            CLI: bulk-load a legacy JSON config into the DB
  uploads/           Uploaded PDF documents (server-side, uuid-named)
  .env               Local secrets (see §5 — currently plaintext, not committed to any VCS since there is no git repo)
admin.html / supplier.html / customer.html / reset-password.html   Static frontend pages
start.bat            Dev launcher: creates venv, installs deps, runs uvicorn
```

There is **no version control** in this project directory (`git status` shows "not a git repository") — this itself is worth flagging to the external reviewer as a process gap: no commit history, no code review trail, no rollback mechanism.

---

## 2. Request flow

1. Browser loads `admin.html` / `supplier.html` / `customer.html` directly from FastAPI's static mount (same origin as the API — no separate frontend server).
2. `customer.html` calls only `GET /api/public/config` (unauthenticated) and renders everything client-side from that single JSON blob (suppliers, profiles, approved tariffs, regulated charges, DAM price data, notices, changelog).
3. `admin.html` / `supplier.html` show a login overlay first. Successful login issues either a full JWT or a short-lived "pending" OTP token (see §4). Once authenticated, the token is held in `sessionStorage` and sent as `Authorization: Bearer <token>` on every subsequent `/api/admin/*` or `/api/auth/*` call.
4. All API routers are registered **before** the catch-all static mount in `main.py`, so `/api/...` paths always take priority over static file serving.

---

## 3. Data model

16 tables, all in `models.py`. Key groupings:

- **Reference data**: `suppliers`, `profiles` (half-hourly load-shape curves parsed from EAC CSV exports)
- **Core business object**: `tariffs` — one row per tariff, `rates`/`discounts` stored as JSON text columns (frontend calculation logic consumes them as plain JSON; no need to normalize further at this scale). Lifecycle status: `draft → pending → approved/rejected`, plus `suspended` (admin can pull a live tariff without deleting it).
- **Regulated charges**: `regulated` (current values, single row) + `regulated_history` (append-only snapshot on every change, for trend history)
- **Market data**: `dam_data` — single-row table holding Day-Ahead Market price data as JSON arrays (monthly, half-hourly-by-slot, and raw daily)
- **Content**: `notices` (bilingual EN/EL rich text shown in the calculator)
- **Audit**: `changelog` (field-level diffs on every tariff/regulated-charge change, records actor role+email), `login_activity` (every login attempt, success or failure, with IP/user-agent)
- **Auth/accounts**: `users`, `password_history` (last 5 hashes, reuse prevention), `password_resets` (1-hour single-use tokens, also reused for the supplier invite-link flow), `otp_codes` (10-minute single-use 6-digit codes)
- **Documents**: `tariff_documents` — uploaded PDF metadata; the file itself lives in `uploads/<uuid>.pdf`, decoupled from the user-supplied filename
- **Messaging**: `messages`, `message_reads` (read + acknowledge tracking per supplier), `scheduled_notifications` (recurring broadcast rules, e.g. "remind suppliers every 6 months")

Schema evolution is handled by a hand-rolled migration block at the top of `main.py` (`ALTER TABLE ... ADD COLUMN` wrapped in try/except with per-statement rollback for Postgres) rather than Alembic. This works but has no down-migration path and no version tracking — acceptable for the current single-developer/single-environment stage, but worth automating (Alembic) before the schema needs to move across multiple environments (dev/staging/prod) in lockstep.

---

## 4. Authentication & authorization

### Login flow
1. `POST /api/auth/login` — email+password checked against `bcrypt` hash.
2. **Account lockout**: 3 failed attempts locks the account for 180 minutes; lockout and unlock are both logged to `login_activity`, and a lockout triggers an email alert to the account owner (`notify_account_locked`). Unknown emails and known-but-wrong-password both return generic 401s, but only known accounts increment `failed_attempts` (avoids leaking which emails exist while still supporting lockout).
3. On success, if the user has `otp_enabled` (default true), the server does **not** issue a real JWT — it emails a 6-digit OTP (10-minute expiry, one active code per email, 2-minute resend cooldown) and returns a short-lived "pending" token (`purpose: "otp"` claim) that `get_current_user` explicitly rejects for any real API call.
4. `POST /api/auth/verify-otp` exchanges the pending token + code for a real 8-hour JWT.
5. `otp_enabled` can be toggled off per-user by an admin (documented as intended for testing) — this is a legitimate operational escape hatch but is also a control an external reviewer will want to see is restricted to admins and audited (it is admin-only via `require_admin`, but toggling it is **not** currently written to `changelog` or any audit trail — only `login_activity.reason` would show `password_only` afterwards).

### Token design
- HS256 JWT, 8-hour expiry, claims: `sub` (user id), `email`, `role`, `supplier`, `iat`, `exp`.
- **Session invalidation on password change**: `get_current_user` compares the token's `iat` against `user.password_changed_at` and rejects tokens issued before the most recent password change — closes the window where a stolen/old token stays valid after a reset.
- **Password-expiry gate**: once `must_change_password` is set (see below), every endpoint except `PUT /api/auth/password` returns 403 `password_expired` until the user sets a new password.

### Password policy
- Minimum 8 chars, must include a letter, a digit, and a symbol (`validate_password_strength`).
- Reuse prevention: cannot reuse the current password or any of the last 5 (`password_history`, checked via `bcrypt.checkpw` against each stored hash — correctly avoids a plaintext comparison table).
- **180-day expiry**: a daily background check (`run_password_expiry_check`, driven by the in-process scheduler in `main.py`) flags overdue passwords and emails a one-time reminder 14 days before expiry.

### Authorization model
Two roles only: `admin` (CERA staff) and `supplier` (scoped to one `supplier_name`). Enforcement pattern is consistent throughout `routers/admin.py`:
- `get_current_user` — any authenticated user (used for GET endpoints and supplier-writable resources)
- `require_admin` — admin-only (all supplier/regulated/notices/DAM/user-management/messaging writes)
- `_assert_tariff_owner` — explicit ownership check on every tariff mutation so a supplier token can never touch another supplier's tariff, even by guessing a tariff ID
- Tariff-document endpoints repeat the same ownership check independently (upload/list/download) rather than sharing a single dependency — functionally correct today but a maintenance risk if a new document endpoint is added without copying the check.

No CSRF protection is implemented, but this is **appropriate** for the current design: there are no cookie-based sessions (bearer token only, sent explicitly via JS, never auto-attached by the browser), so classic CSRF does not apply. CORS is restricted to `TARIFF_BASE_URL` (see §6), which is the correct control for this architecture.

---

## 5. Secrets & configuration

All configuration is environment-variable driven (`tariff-api/.env`, loaded via `python-dotenv`). Current variables:

- `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET` — Azure AD app registration for Graph API email sending
- `TARIFF_EMAIL_FROM`, `TARIFF_ADMIN_EMAIL` — mailbox identities
- `TARIFF_BASE_URL` — public base URL (used for CORS origin, email links, and OTP/reset links)
- `TARIFF_SECRET_KEY` — JWT signing secret
- `DATABASE_URL` — Postgres connection string (includes DB password)

**⚠️ Open finding (already tracked internally, not yet remediated):** `.env` holds all of the above in plaintext on disk. This is the single most obvious finding an external reviewer will surface. It must be replaced with a proper secret store (Azure Key Vault, or environment variables injected by the hosting platform at deploy time) before production deployment or external inspection. The project folder was already moved off OneDrive (2026-07-10) to remove cloud-sync exposure, but the file itself is still not access-controlled beyond OS file permissions.

**⚠️ Related finding:** the Azure app registration's `Mail.Send` permission is an **application permission** ("send mail as any user" — confirmed against Microsoft's own permission description in the Azure Portal), not delegated. The app is correctly restricted to "My organization only" (rules out cross-tenant abuse), but nothing yet scopes *which* mailboxes within the tenant it can impersonate — that requires an Exchange Online **Application Access Policy**, which needs a Global/Exchange admin to apply (the operating account does not have the required role). This should be raised as a distinct action item from the `.env` plaintext issue, not folded into it.

`auth.py` has a hardcoded fallback JWT secret (`dev-only-do-not-deploy-...`) used only if `TARIFF_SECRET_KEY` is unset — clearly labeled as dev-only in an adjacent comment, and superseded by a real generated value in the current `.env`. Confirm before go-live that the environment used for external inspection/production actually has `TARIFF_SECRET_KEY` set (the fallback exists precisely so an operator can't accidentally deploy with no secret configured, but it can't stop them deploying with the *same known* fallback if the env var is missing).

---

## 6. Network/transport controls

- **CORS**: `allow_origins=[TARIFF_BASE_URL]` (was previously `"*"`, tightened 2026-07-10). Verified live: unlisted origins receive no CORS header; the configured origin does. `allow_methods`/`allow_headers` remain `"*"`, which is fine given the origin restriction.
- **HTTPS/TLS**: not handled by the app itself — `uvicorn` is run directly on port 8000 with no TLS. This is acceptable for local dev but **must** sit behind a reverse proxy (nginx/Caddy/Azure App Service's built-in TLS termination) with HTTPS before any external exposure. Currently there is no reverse proxy in front of it.
- **`--reload` must never be used** in this environment: with Python 3.14 / uvicorn 0.49, `--reload` causes HTTP 500 on all POST endpoints. `start.bat` and all documented run instructions correctly omit it.

---

## 7. File uploads

`POST /api/admin/tariffs/{id}/documents` accepts supplier-uploaded supporting PDFs:
- Extension check (`.pdf`) **and** magic-byte check (`content.startswith(b"%PDF")`) — resistant to simple extension-renaming bypass.
- 10 MB size cap enforced after reading the full body into memory (acceptable at this file-size ceiling; would need streaming for much larger limits).
- Stored server-side under a `uuid4().hex + ".pdf"` filename — the original filename is preserved only as metadata (`original_name`) and never used to construct a filesystem path, which avoids path-traversal via crafted filenames.
- Download endpoint re-checks tariff ownership for supplier tokens before serving the file (`GET /api/admin/documents/{doc_id}/download`).
- Uploading a new document on an approved/rejected tariff automatically reverts it to `pending` — correct business logic (an admin approval covers a specific document set; a new document should trigger re-review), and is itself changelog-worthy — currently this state transition is **not** written to `changelog` (only status changes made via the explicit status-patch endpoint are). Minor audit-trail gap.

No antivirus/content scanning of uploaded PDFs — acceptable given admin-approval gates every tariff, but worth noting for the external reviewer's threat model if these PDFs are later served to end customers rather than just CERA staff.

---

## 8. Frontend architecture & client-side findings

All three portal pages are single-file monoliths (no bundler, no framework) — `admin.html` (~5,360 lines / ~166 functions), `supplier.html` (~1,890 lines / ~74 functions), `customer.html` (~2,560 lines / ~77 functions), plus a small standalone `reset-password.html` (~150 lines).

**Auth handling (admin/supplier):** token stored only in `sessionStorage` (never `localStorage`), sent explicitly via `Authorization: Bearer`, cleared on logout, and every portal consistently redirects to the login overlay on any 401. This is a sound pattern — no auto-attached cookies means no CSRF surface, and `sessionStorage` limits token lifetime to the tab's life.

**customer.html** is confirmed public/read-only: the entire file makes exactly one network call, `fetch('/api/public/config')` (GET, unauthenticated), and uses no `localStorage`/`sessionStorage` at all.

### ✅ XSS findings — exhaustively reviewed and fixed 2026-07-14

An initial sampled review found one instance in `customer.html`. Live exploit testing then kept turning up more instances the sample had missed, so the review was escalated to a full manual audit of **every single one of the 116 `innerHTML`/`outerHTML`/`insertAdjacentHTML` call sites** across all four frontend files (76 in `admin.html`, 19 in `supplier.html`, 20 in `customer.html`, 1 in `reset-password.html`) — not a sample. All findings below have been remediated and re-verified; kept here as the record and as the model to follow for any new render code.

**Root cause:** all three portals are vanilla-JS monoliths (no framework, no templating layer), so every dynamic render is a hand-built string assigned to `.innerHTML`. Any database-sourced string interpolated into one of these without an escaping helper is a stored-XSS sink. A second, sneakier variant recurred repeatedly: embedding such a string inside an inline `onclick="fn('${x}')"` handler is unsafe **even when HTML-escaped**, because the browser HTML-decodes the attribute value before parsing it as JS — an escaped `'` (`&#39;`) decodes back to a literal `'` and still breaks the JS string. The only real fix is to stop embedding the value in the handler at all (`data-*` attribute + `this.dataset`, or an id-keyed lookup cache).

**Findings, roughly in order of severity:**

1. **Unauthenticated stored XSS via the login-activity audit table** (`admin.html`) — the single worst finding. `POST /api/auth/login` logs the submitted `email` and the request's `User-Agent` header verbatim into `login_activity`, with **no authentication and no account required** — anyone can hit the public login endpoint with an arbitrary string in either field. Both were rendered unescaped in the admin-only login-activity table. This is a stored-XSS path that needs zero valid credentials of any kind and lands directly in an admin's authenticated session.
2. **Dashboard pending-review widget** (`admin.html`, `buildDashboard()`) — renders every pending tariff's name/supplier and fires **automatically the instant an admin logs in**, no click required.
3. **Tariff review modal** (`admin.html`, `openReview()`) — where an admin inspects a supplier's pending submission before approving it: `t.supplier`, `t.name`, `t.contract`/`voltage`/`pricing`, `prof.name`, discount labels, and changelog diff values (`ch.from`/`ch.to`) were all unescaped. A malicious submission could execute script directly in the admin's session during approval review.
4. **Public customer.html** — the original finding: `tariff.name`/`tariff.supplier` (one case inside an inline `onclick`), profile names, and supplier contact-card fields (address/phone/email/website/notes) unescaped on the fully public, unauthenticated calculator page.
5. **`supplier.html`'s `openDocsModal(id, name)`** — embedded the tariff name inside an inline-`onclick` JS string; worse than the admin.html equivalents because `supplier.html`'s own pre-existing `esc()` didn't escape single quotes at all, so a bare `'` in a tariff name broke it immediately, no entity-decoding subtlety required.
6. **Document-download `onclick` in both `admin.html` and `supplier.html`** — built as `onclick="downloadDoc(id,'${original_name.replace(/'/g,"\\'")}')"`; escaping only the JS single quote does not protect this context, so a `"` or `<` in an uploaded PDF's filename could still break attribute/JS context.
7. **Changelog table + its supplier filter dropdown, a second supplier-filter dropdown on the tariff-management tab, the "group by supplier" header, the supplier-management list, the profiles list (`name`/`desc`), the edit-tariff and invite-user supplier dropdowns, the audit-calculator panel, and tier-rate `value=` input attributes in both `admin.html` and `supplier.html`** — same unescaped-interpolation pattern, lower individual severity but same fix.
8. **`admin.html`'s user-management table** — `user.email`/`user.supplier_name` unescaped in the table and inside several inline `onclick` handlers. Lower severity since these are admin-set at account creation.

**Fix applied uniformly:** a consistent `esc()` HTML-escaping helper (escaping `& < > " '`) was added to `admin.html` and `customer.html`, and the pre-existing `esc()` in `supplier.html` was upgraded to also escape `'`. Every finding above now routes through it. Every inline-`onclick`-embedding case was additionally restructured to pass only an id and resolve the associated string from a small lookup (`_docsCache`, `_usersCache`, `tariffs.find(...)`, or a `data-*` attribute) rather than ever embedding a database-sourced string inside event-handler JS source.

**Verification — three escalating rounds, the last two genuine live exploit tests against the real app:**
1. Static check: started the dev server, loaded both main pages via Playwright, confirmed zero console/page errors, confirmed `esc()` neutralizes representative payloads in isolation.
2. Live end-to-end test: seeded a **disposable SQLite database** (the real Postgres dev DB was never touched — `DATABASE_URL` overridden per-process to a scratchpad temp file, Azure email credentials blanked so no real email could send) with a malicious supplier and tariff record, ran the real FastAPI app against it on a spare port, and drove real Chromium via Playwright through the actual public-calculator and admin-review-modal flows. This caught the dashboard widget and a filter dropdown that the first fix pass had missed.
3. After escalating to the full 116-sink manual review (which surfaced the login-activity, profiles-list, and `supplier.html` `openDocsModal` findings above): re-seeded the test database with payloads targeting every newly-fixed site — a malicious profile name/description, a tariff renamed to a bare single-quote payload, an **unauthenticated** login POST with a malicious email, and a malicious `User-Agent` header — and re-ran the full live test across both an admin session and a supplier session. **Final result: 0 script executions across 7 distinct payload markers, 0 dialogs, 0 page errors.**

**Separate, also-fixed finding — `javascript:`/`data:` URL scheme injection:** HTML-escaping (`esc()`) does not protect against a malicious URL *scheme*, since a payload like `javascript:alert(1)` contains none of the characters escaping touches. `customer.html`'s two supplier-contact-card renderers built `href="${esc(s.website)}"` from the supplier's self-entered website field — a malicious/compromised supplier could have set their "website" to a `javascript:` URL that executes when any customer clicks the contact link on the public page. **Fix:** added a `safeUrl()` helper that only allows `http://`/`https://` through (anything else, including bare domains with no scheme, becomes `#`); verified live that `javascript:`, mixed-case `JaVaScRiPt:`, and `data:` payloads are all neutralized while a real `https://` URL passes through unchanged. `admin.html`/`supplier.html` don't render `website` as a clickable link (admin.html shows it as plain text), so no equivalent gap existed there. `tel:`/`mailto:` links elsewhere are safe by construction — the scheme prefix is a hardcoded template literal, not user-controlled.

No hardcoded secrets or API keys were found in any frontend file. No `Content-Security-Policy` (or other security headers) is set via `<meta>` tag in any of the four HTML files — if a CSP is desired, it would need to be added as a response header from FastAPI (e.g. via middleware), which is not currently present. Adding one would be good defense-in-depth on top of the output-escaping fix above, though not a substitute for it.

**Explicitly out of scope for this pass (flagged, not fixed) — for the external reviewer's awareness:**
- **CSV formula injection**: `admin.html`'s changelog CSV export interpolates tariff/supplier names into CSV cells unescaped; a name starting with `=`, `+`, `-`, or `@` could be interpreted as a formula by Excel/Sheets on open. A different bug class (client-side spreadsheet risk, not in-browser script execution) and not remediated here.
- **DOM-based XSS via `location.hash`/`location.search`/`postMessage`**: not searched for in this pass; the only URL-parameter consumer checked was `reset-password.html`'s `token`/`portal` params, confirmed rendered safely (not via `innerHTML`).
- **The admin notices rich-text editor intentionally renders raw HTML** (a WYSIWYG feature, by design) — meaning a compromised *admin* account, not just a compromised supplier account, has a direct stored-XSS path to the public page. This is an accepted design tradeoff given the trust model (admins are the most-trusted role), not a bug, but should be named explicitly to an external reviewer rather than left implicit.

---

## 9. Email / notification subsystem

`email_utils.py` sends all mail via Microsoft Graph (`POST /v1.0/users/{from}/sendMail`), authenticated with `msal.ConfidentialClientApplication` client-credentials flow — no SMTP credentials anywhere. All sends are fire-and-forget on a daemon thread (`_send_bg`) so a slow/failing Graph call never blocks the request that triggered it; failures are logged, never raised to the caller. Templates are table-based HTML with inline styles for Outlook/Gmail compatibility. Notification triggers: new tariff submission, resubmission, approval, rejection, password reset, account lockout, OTP code, password-expiry warning, supplier invite, and broadcast messages (manual and scheduled). Bilingual (EN/EL) templates are used for the password-expiry and broadcast-message notifications; the rest are English-only.

---

## 10. Background scheduler

A single `asyncio` task started on FastAPI startup (`_scheduled_notifications_loop`, `main.py`) runs every hour in-process: fires any due recurring `scheduled_notifications`, and once per day also runs the password-expiry check. This is explicitly a **single-instance design** — the code comment notes that scaling to multiple app instances would double-send without adding a lock. Fine for the current Basic B1 App Service / single-process deployment target; must be revisited if the app is ever scaled horizontally.

---

## 11. Known outstanding risks (pre-production checklist)

These are tracked items, not yet remediated, in priority order for an external certification review:

1. **Secrets in plaintext `.env`** (§5) — highest priority, easiest finding for any reviewer.
2. **Azure `Mail.Send` application permission not yet scoped** via Exchange Application Access Policy (§5) — requires a Global/Exchange admin.
3. **Stored XSS on the public customer page** via unescaped tariff/supplier names (§8) — code fix, no infra dependency, should be quick to remediate.
4. **No HTTPS/reverse proxy** in the current setup — must sit behind TLS termination before external exposure.
5. **Dev-only PostgreSQL instance** — user-owned, non-service process, no managed backup/TLS/HA. Needs a real managed Postgres (e.g. Azure Database for PostgreSQL) before production.
6. **No version control** — no git repository exists for this project; no commit history, diff review, or rollback capability.
7. **No Alembic migrations** — schema changes are hand-rolled `ALTER TABLE` statements at startup; works but has no rollback path.
8. **Minor audit-trail gaps**: OTP-toggle-per-user and document-upload-triggered-resubmission are not written to `changelog` (only explicit status-patch actions are).
9. Document-upload feature has no malware/content scanning (acceptable today given admin-gated approval, worth reassessing if exposure changes).

An external IT company is expected to perform a combined functional/UAT walkthrough and OWASP-style security assessment before go-live; the items above are the ones most likely to surface in that assessment and should be prioritized accordingly.

---

## 12. Summary assessment

The backend shows a consistent, deliberate security design for its size: bearer-token-only auth (no CSRF surface), server-side ownership checks on every mutating endpoint, account lockout with audit logging, password history/expiry/reuse enforcement, session invalidation on password change, and OTP 2FA with proper short-lived "pending" tokens that are explicitly rejected by the main auth dependency. The main gaps are operational/infrastructure (secrets storage, TLS, managed DB, version control) rather than architectural, plus one concrete code-level finding (inconsistent output escaping, most seriously on the public customer page) that should be fixed before any external security assessment.
