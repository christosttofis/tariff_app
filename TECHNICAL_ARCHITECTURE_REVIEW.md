# CERA Tariff Comparison Tool — Technical Architecture & Security Review

**Document purpose:** technical reference for an expert/external reviewer (functional + security assessment) prior to production go-live. Originally written 2026-07-14; updated 2026-07-15 to reflect the `SECURITY_REMEDIATION_CHECKLIST.md` hardening pass, a follow-on security review covering SQL injection, buffer overflow, broken access control, email injection, OTP brute-force, dependency CVEs, and JWT storage (see §11 and §12), and a later same-day pass covering accidental-overload protection, sliding session expiry, and two cross-portal access-control gaps found during manual testing (see §13). Updated again 2026-07-23 (see §14) to reflect five days of subsequent functional/data-integrity work: a supplier↔user foreign key replacing string matching, a scheduled local database backup, and an append-only-changelog bug fix. Updated again same day to close the Alembic-migrations and audit-trail-gap risk items, centralize secrets handling (§5), and add a **proposed production deployment architecture on Azure** (§19) — not yet built, included here specifically for the external reviewer's comment before we commit to it. **Updated 2026-09-25** to reflect three later work streams and re-number the sections chronologically: moving all tariff calculation server-side and trimming the public config to close a customer-data-exposure finding (§15), a penetration test of the resulting public endpoints (§16), and a black-box security test with its fixes (§17). The core "how it works" sections (§2, §3, §8) were corrected in the same pass — before this update they still described the superseded client-side-calculation design. **Updated 2026-09-30:** the API was split into admin-only `/api/admin/*` and supplier-only `/api/supplier/*`, each guarded router-wide (§4 Authorization model).

**Scope:** full-stack review of `tariff-api/` (FastAPI backend) and the three static frontend applications (`admin.html`, `supplier.html`, `customer.html`) plus supporting scripts.

---

## 1. System overview

A tariff comparison and regulatory-monitoring tool for the Cyprus Energy Regulatory Authority (CERA). Three audiences, three portals, one backend:

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
  client_ip.py       Trusted client IP (X-Forwarded-For hop rule) + admin network check
  main.py            FastAPI app, CORS/CSP, rate-limit middleware, 5-file static allowlist, Alembic upgrade at startup, background scheduler
  pricing/           Server-side tariff-pricing engine (pure functions, one module per concern) — see §15
  routers/public_calc.py  /api/public/calculate + /api/public/sample-invoice — orchestrates the pricing engine
  auth.py            JWT issuance/verification, password hashing/policy, lockout-aware get_current_user
  database.py        SQLAlchemy engine/session (Postgres via DATABASE_URL, SQLite fallback)
  models.py          ORM models (16 tables)
  schemas.py         Pydantic request schemas
  serializers.py      ORM → dict serializers shared by public/admin endpoints
  importer.py        One-off legacy JSON import for seed.py (the admin "Publish" flow that also used it was removed 2026-09-30)
  email_utils.py     Graph API email templates and sending
  routers/auth.py    /api/auth/* — login, OTP, password reset/change
  routers/admin.py   /api/admin/* — admin-only (router-wide require_admin): CRUD, user mgmt, messaging, scheduling
  routers/supplier.py /api/supplier/* — supplier-only (router-wide require_supplier), scoped to the caller's own supplier
  routers/shared.py  Tariff/document/message helpers used by both role routers (no logic duplicated between them)
  create_user.py     CLI: create/update/deactivate a user account
  unlock_user.py     CLI: clear an account lockout
  seed.py            CLI: first-time load of a legacy JSON config into an empty DB (refuses a populated DB without --force)
  scripts/           One-off migration SQL (supplier FK backfill/cleanup) + backup_db.ps1 (§14.2)
  uploads/           Uploaded PDF documents (server-side, uuid-named)
  .env               Local secrets (see §5 — currently plaintext; excluded from version control via .gitignore)
admin.html / supplier.html / customer.html / reset-password.html   Static frontend pages
start.bat            Dev launcher: creates venv, installs deps, runs uvicorn
```

**Version control**: a local git repository was initialized 2026-07-14 (previously there was none — flagged as a process gap in the original version of this document). `.gitignore` excludes `.env`, `tariff-api/.venv/`, `tariff-api/uploads/*` (except a `.gitkeep`), and `*.db` files. There is no remote configured — history exists locally only, which is adequate for a single-developer project but worth noting if collaboration or off-machine backup of history becomes a requirement.

---

## 2. Request flow

1. Browser loads `admin.html` / `supplier.html` / `customer.html` directly from FastAPI's static mount (same origin as the API — no separate frontend server).
2. `customer.html` (unauthenticated) calls three public endpoints: `GET /api/public/config` for **display/filter metadata only** (supplier contact info, a trimmed per-tariff summary, notices, `sampleInvoiceEnabled`), then `POST /api/public/calculate` (debounced on input) and, on demand, `POST /api/public/sample-invoice` for computed results. **As of 2026-09 (§15)** all tariff pricing is computed **server-side** — the page sends the customer's inputs and renders the returned per-tariff costs; it no longer holds any pricing engine or raw rate data. The public config deliberately no longer includes `profiles`, `regulated`, or DAM series, nor per-tariff `rates`/`discounts`/`mdmSource`/`fpaSource`/`profileId` (this was the customer-data-exposure remediation — see §15). The page also has a footer "report an issue" link that `POST`s to `/api/public/report-tariff`.
3. `admin.html` / `supplier.html` show a login overlay first. Successful login issues either a full JWT or a short-lived "pending" OTP token (see §4). **As of 2026-07-15**, the full JWT is delivered via an `httpOnly`/`Secure`/`SameSite=Strict` session cookie set by the server (`Set-Cookie`), not returned in the JSON response body — the browser attaches it automatically to same-origin requests, and JavaScript cannot read it at all (see §12.7). Because the client can no longer synchronously know whether it's authenticated (the cookie isn't JS-readable), each portal's page-load logic optimistically calls its first authenticated data endpoint and lets a 401 response (rather than a locally-stored flag) trigger the login overlay.
4. All API routers are registered **before** the catch-all static mount in `main.py`, so `/api/...` paths always take priority over static file serving.

---

## 3. Data model

16 tables, all in `models.py`. Key groupings:

- **Reference data**: `suppliers`, `profiles` (half-hourly load-shape curves parsed from EAC CSV exports)
- **Core business object**: `tariffs` — one row per tariff, `rates`/`discounts` stored as JSON text columns (the **server-side** pricing engine in `pricing/` consumes them as plain JSON — see §15; these are never sent to the public page anymore). Lifecycle status: `draft → pending → approved/rejected`, plus `suspended` (admin can pull a live tariff without deleting it).
- **Regulated charges**: `regulated` (current values, single row) + `regulated_history` (append-only snapshot on every change, for trend history)
- **Market data**: `dam_data` — single-row table holding Day-Ahead Market price data as JSON arrays (monthly, half-hourly-by-slot, and raw daily)
- **Content**: `notices` (bilingual EN/EL rich text shown in the calculator)
- **Audit**: `changelog` (field-level diffs on every tariff/regulated-charge change, records actor role+email), `login_activity` (every login attempt, success or failure, with IP/user-agent)
- **Auth/accounts**: `users`, `password_history` (last 5 hashes, reuse prevention), `password_resets` (1-hour single-use tokens, also reused for the supplier invite-link flow), `otp_codes` (10-minute single-use 6-digit codes). **Updated 2026-07-20 (§14.1)**: `User.supplier_id` is now a real FK to `suppliers.id` (was a plain `supplier_name` string that had to exactly match `Supplier.name`, with no enforced relationship); `MessageRead` got the same FK treatment. `Tariff.supplier` and `Message`/`ScheduledNotification.target_suppliers` remain plain strings.
- **Documents**: `tariff_documents` — uploaded PDF metadata; the file itself lives in `uploads/<uuid>.pdf`, decoupled from the user-supplied filename
- **Messaging**: `messages`, `message_reads` (read + acknowledge tracking per supplier), `scheduled_notifications` (recurring broadcast rules, e.g. "remind suppliers every 6 months")

Schema evolution is handled by **Alembic** (`tariff-api/migrations/`); `main.py` runs `alembic upgrade head` at startup, giving version history and a rollback path. (This replaced an earlier hand-rolled `ALTER TABLE` block on 2026-07-23 — see §18 item 5.)

---

## 4. Authentication & authorization

### Login flow
1. `POST /api/auth/login` — email+password checked against `bcrypt` hash.
2. **Account lockout**: 3 failed attempts locks the account for 180 minutes; lockout and unlock are both logged to `login_activity`, and a lockout triggers an email alert to the account owner (`notify_account_locked`). Unknown emails and known-but-wrong-password both return generic 401s, but only known accounts increment `failed_attempts` (avoids leaking which emails exist while still supporting lockout).
3. On success, if the user has `otp_enabled` (default true), the server does **not** issue a real JWT — it emails a 6-digit OTP (10-minute expiry, one active code per email, 2-minute resend cooldown) and returns a short-lived "pending" token (`purpose: "otp"` claim) that `get_current_user` explicitly rejects for any real API call.
4. `POST /api/auth/verify-otp` exchanges the pending token + code for a real JWT (sliding expiry — see Token design below).
5. `otp_enabled` can be toggled off per-user by an admin (documented as intended for testing) — this is a legitimate operational escape hatch but is also a control an external reviewer will want to see is restricted to admins and audited (it is admin-only via `require_admin`, but toggling it is **not** currently written to `changelog` or any audit trail — only `login_activity.reason` would show `password_only` afterwards).

### Token design
- HS256 JWT, claims: `sub` (user id), `email`, `role`, `supplier`, `iat`, `exp`, `session_start`.
- **Expiry, updated 2026-07-15 (§13.2): sliding, not flat.** Originally a flat 8-hour expiry from login. Now `TOKEN_EXPIRE_HOURS = 1` is a *sliding* window — `get_current_user` reissues the cookie with a fresh 1-hour expiry on every successful authenticated request — capped by `ABSOLUTE_SESSION_HOURS = 12` measured from the original login via the `session_start` claim, which is preserved unchanged across renewals (only `iat`/`exp` advance). This means an active user is never logged out mid-work purely because a fixed clock ran out, while a stolen/replayed token still can't be kept alive indefinitely.
- **Delivery, updated 2026-07-15**: the JWT is set via `Set-Cookie` (httpOnly/Secure/SameSite=Strict, no `Max-Age` — a browser-session cookie, so it doesn't outlive the browser session regardless of the server-side expiry) rather than returned in the JSON body. `get_current_user` reads it from `request.cookies`. A `POST /api/auth/logout` endpoint clears the cookie server-side (`Set-Cookie` with an expired date) — necessary because JavaScript cannot clear an httpOnly cookie itself.
- **Identity re-hydration, added 2026-07-15 (§13.3)**: `GET /api/auth/me` returns `{role, supplier, email}` for the current session. Added because the frontend previously only knew the logged-in user's identity from the login response itself, cached in `sessionStorage` — a valid cookie in a *new* tab or after a reload had no way to repopulate the user badge / Sign-out control. Both portals now call this endpoint to re-hydrate identity whenever `sessionStorage` is empty but the session cookie is still valid.
- **Session invalidation on password change**: `get_current_user` compares the token's `iat` against `user.password_changed_at` and rejects tokens issued before the most recent password change — closes the window where a stolen/old token stays valid after a reset.
- **Password-expiry gate**: once `must_change_password` is set (see below), every endpoint except `PUT /api/auth/password` returns 403 `password_expired` until the user sets a new password.

### Password policy
- Minimum 8 chars, must include a letter, a digit, and a symbol (`validate_password_strength`).
- Reuse prevention: cannot reuse the current password or any of the last 5 (`password_history`, checked via `bcrypt.checkpw` against each stored hash — correctly avoids a plaintext comparison table).
- **180-day expiry**: a daily background check (`run_password_expiry_check`, driven by the in-process scheduler in `main.py`) flags overdue passwords and emails a one-time reminder 14 days before expiry.

### Authorization model
Two roles only: `admin` (CERA staff) and `supplier` (scoped to one `supplier_name`). **Updated 2026-09-30: the API is split by role, and each role is enforced once at the router level:**
- `/api/admin/*` (`routers/admin.py`) — `APIRouter(..., dependencies=[Depends(require_admin)])`. Every route, including any added later, is admin-only by default. Before this change, admin and supplier portals shared these routes and each handler branched on `user.is_supplier`. That was allow-by-default: a handler written with `get_current_user` instead of `require_admin` was silently open to suppliers, which is exactly what §12.3 and §17.1 found.
- `/api/supplier/*` (`routers/supplier.py`) — `dependencies=[Depends(require_supplier)]` (supplier role **and** linked to a supplier). Admins get 403 here. Every handler scopes to `user.supplier_name`/`supplier_id`: another supplier's tariff, document or message returns the same 404 as a missing one (no ID probing). A body's `supplier` field must equal the caller's own supplier on create **and** update. Before the split, update only checked the tariff's existing owner, so a supplier could reassign its own tariff to a competitor's name; this was found and closed during the split. Supplier creates/edits always go to `pending`.
- `/api/auth/*` stays shared (login is role-agnostic). `/api/public/*` stays anonymous.
- The underlying tariff/document/message logic lives in `routers/shared.py`, so the two routers differ only in guards and scoping, not in duplicated business logic.
- This layout also means perimeter controls (e.g. restricting admin access to the CERA VPN) can target a path prefix or a single router dependency.

**Admin network restriction (2026-09-30).** Admin accounts only work from the networks in `TARIFF_ADMIN_ALLOWED_NETWORKS` (CERA office + VPN). This is enforced in `get_current_user` for the admin role (every request), at sign-in before the password check, at OTP verify/resend, and on `admin.html`. The only response outside is a generic 404 "Website unavailable". The client IP comes from `client_ip.py`: behind Azure (`TARIFF_TRUSTED_PROXY_HOPS=1`) only the rightmost `X-Forwarded-For` entry is trusted. The same helper feeds the rate limiter and IP logging. Static files are served from an explicit five-file allowlist: the earlier whole-folder mount exposed `.env`, source and `.git`. See `SECURITY_REMEDIATION_CHECKLIST.md` Rounds 13–14.

**Tariff input validation (2026-09-30).** Tariff content is validated as strictly as the fixed fields: `rates` against a per-pricing-type schema and `discounts` against `DiscountIn` (numbers only, finite, bounded by `TARIFF_MAX_ENERGY_RATE`/`TARIFF_MAX_MONTHLY_CHARGE` from `config.py`), and the profile must exist. Previously a single malformed approved tariff could make `/api/public/calculate` fail for every customer. The calculator now also isolates per-tariff failures. Email change requires the current password. Details: `SECURITY_REMEDIATION_CHECKLIST.md` Round 11.

**CSRF, updated 2026-07-15**: the session now lives in a cookie (see §2, §12.7), which does auto-attach to requests — the control that makes classic CSRF not apply is `SameSite=Strict` on that cookie, not "bearer-token-only" as in the original design. `SameSite=Strict` means the browser never sends the cookie on a request originating from another site, including top-level navigations, so a malicious third-party page cannot ride the victim's session even to a same-origin endpoint. Combined with the app having no cross-origin form actions anywhere and CSP's `form-action 'self'` (see §8), this is considered sufficient without a separate CSRF-token scheme for this app's architecture (single origin, no third-party embedding, no public cross-site API consumers). CORS is restricted to `TARIFF_BASE_URL` (see §6), which is the correct control for cross-origin fetch/XHR attempts specifically.

---

## 5. Secrets & configuration

All configuration is environment-variable driven, read from one centralized module as of 2026-07-23 (`tariff-api/config.py`, replacing what used to be 8 separate `os.getenv()` call sites scattered across `auth.py`/`database.py`/`email_utils.py`/`main.py`/both routers — `TARIFF_BASE_URL` alone was previously read independently in 4 places). `config.py` calls `python-dotenv`'s `load_dotenv()`, which fills in variables not already set in the process environment — so a real deployment target that injects secrets as actual environment variables (Azure App Service Application Settings, a Key Vault reference resolved to an app setting, etc.) works identically to a local `.env` file; this file doesn't care which one supplied the value; it only centralizes where it's read from. Current variables:

- `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET` — Azure AD app registration for Graph API email sending
- `TARIFF_EMAIL_FROM`, `TARIFF_ADMIN_EMAIL` — mailbox identities
- `TARIFF_BASE_URL` — public base URL (used for CORS origin, email links, and OTP/reset links)
- `TARIFF_SECRET_KEY` — JWT signing secret
- `DATABASE_URL` — Postgres connection string (includes DB password)

**Added 2026-07-23**: `config.py` now logs a startup warning (previously silent) for each of the three fallback conditions worth knowing about immediately rather than discovering later — `TARIFF_SECRET_KEY` falling back to the well-known dev key, `DATABASE_URL` falling back to a local SQLite file, and incomplete Azure email credentials. Verified these fire correctly in an isolated test with no `.env` present.

**⚠️ Open finding (already tracked internally, not yet remediated):** `.env` holds all of the above in plaintext on disk. This is the single most obvious finding an external reviewer will surface. It must be replaced with a proper secret store before production deployment or external inspection. The project folder was already moved off OneDrive (2026-07-10) to remove cloud-sync exposure, but the file itself is still not access-controlled beyond OS file permissions. The centralization above is prep work for this move (whichever secret store is chosen, only `config.py` needs to know how to reach it), not the fix itself — actually provisioning a secret store is still outstanding. **Proposed fix: see §19** — Azure App Service Application Settings (or Key Vault, for a more mature setup) once the target hosting environment is confirmed.

**⚠️ Related finding:** the Azure app registration's `Mail.Send` permission is an **application permission** ("send mail as any user" — confirmed against Microsoft's own permission description in the Azure Portal), not delegated. The app is correctly restricted to "My organization only" (rules out cross-tenant abuse), but nothing yet scopes *which* mailboxes within the tenant it can impersonate — that requires an Exchange Online **Application Access Policy**, which needs a Global/Exchange admin to apply (the operating account does not have the required role). This should be raised as a distinct action item from the `.env` plaintext issue, not folded into it.

`config.py` has a hardcoded fallback JWT secret (`dev-only-do-not-deploy-...`) used only if `TARIFF_SECRET_KEY` is unset — clearly labeled as dev-only in an adjacent comment and now backed by a loud startup warning, superseded by a real generated value in the current `.env`. Confirm before go-live that the environment used for external inspection/production actually has `TARIFF_SECRET_KEY` set (the fallback exists precisely so an operator can't accidentally deploy with no secret configured, but it can't stop them deploying with the *same known* fallback if the env var is missing — the new warning at least makes that condition visible in the startup log instead of silent).

---

## 6. Network/transport controls

- **CORS**: `allow_origins=[TARIFF_BASE_URL]` (was previously `"*"`, tightened 2026-07-10). Verified live: unlisted origins receive no CORS header; the configured origin does. `allow_methods`/`allow_headers` remain `"*"`, which is fine given the origin restriction.
- **HTTPS/TLS**: not handled by the app itself — `uvicorn` is run directly on port 8000 with no TLS. This is acceptable for local dev but **must** sit behind a reverse proxy or platform-level TLS termination before any external exposure. Currently there is no reverse proxy in front of it. **Proposed fix: see §19** — Azure App Service's built-in TLS termination.
- **`--reload` must never be used** in this environment: with Python 3.14 / uvicorn 0.49, `--reload` causes HTTP 500 on all POST endpoints. `start.bat` and all documented run instructions correctly omit it.
- **Rate limiting, added 2026-07-15 (§13.1)**: a per-IP sliding-window limiter (60 requests/minute) guards against *accidental* overload — a stuck frontend retry loop or a mis-run script — rather than sophisticated abuse. Self-contained middleware in `main.py`, not a third-party library; see §13.1 for why.

---

## 7. File uploads

`POST /api/supplier/tariffs/{id}/documents` (and the admin equivalent under `/api/admin/`) accepts supporting PDFs; validation is shared in `routers/shared.py::_save_pdf_upload`:
- Extension check (`.pdf`) **and** magic-byte check (`content.startswith(b"%PDF")`) — resistant to simple extension-renaming bypass.
- 10 MB size cap enforced after reading the full body into memory (acceptable at this file-size ceiling; would need streaming for much larger limits).
- Stored server-side under a `uuid4().hex + ".pdf"` filename — the original filename is preserved only as metadata (`original_name`) and never used to construct a filesystem path, which avoids path-traversal via crafted filenames.
- The supplier download endpoint (`GET /api/supplier/documents/{doc_id}/download`) re-checks tariff ownership before serving the file; the admin one is under `/api/admin/`.
- **Fixed 2026-07-15**: the download endpoint used to build its `Content-Disposition` header via an unescaped f-string embedding the uploaded file's original filename — a `"` in that filename could inject extra header directives. Fixed by removing the manual header override and relying on Starlette's built-in `FileResponse(filename=...)` handling, which runs the name through `urllib.parse.quote()` and automatically switches to RFC 5987 `filename*=utf-8''...` encoding whenever the quoted form would differ.
- Uploading a new document on an approved/rejected tariff automatically reverts it to `pending` — correct business logic (an admin approval covers a specific document set; a new document should trigger re-review). **Fixed 2026-07-23**: this state transition is now written to `changelog` alongside the status change (previously only explicit status-patch actions were logged — see §14.3's sibling fix, the audit-trail gap item).

**No antivirus/content scanning of uploaded PDFs today** — acceptable given admin-approval gates every tariff, but worth noting for the external reviewer's threat model if these PDFs are later served to end customers rather than just CERA staff. **Proposed fix: see §19.4** — moving uploads to Azure Blob Storage with Defender for Storage's Malware Scanning add-on as part of the proposed production deployment.

---

## 8. Frontend architecture & client-side findings

All three portal pages are single-file monoliths (no bundler, no framework) — `admin.html` (~5,360 lines / ~166 functions), `supplier.html` (~1,890 lines / ~74 functions), `customer.html` (~2,560 lines / ~77 functions), plus a small standalone `reset-password.html` (~150 lines). Since 2026-10 the pages are being moved to separate script files (`customer.js`, `supplier.js`, `admin.js`, `reset-password.js`; all four pages done 2026-10-07) with no inline event handlers, so they can run under a strict CSP (§8); elements declare their action with `data-action`/`data-change`/… and a small dispatcher at the end of each `.js` file maps those names to functions.

**Auth handling (admin/supplier), updated 2026-07-15:** the session token was originally stored in `sessionStorage` and sent explicitly via `Authorization: Bearer`. It has since been migrated to an httpOnly cookie (see §4, §12.7) specifically because `sessionStorage` is JS-readable — any successful XSS (present or future) could exfiltrate it with `sessionStorage.getItem(...)`. An httpOnly cookie cannot be read by JavaScript at all, closing that theft vector even if a new XSS bug is found later. Every portal still consistently redirects to the login overlay on any 401, now driven by the first authenticated data call's response rather than a locally-stored flag (see §2).

**customer.html** is confirmed public/read-only and uses no `localStorage`/`sessionStorage` at all. It makes four unauthenticated calls: `GET /api/public/config` (display/filter metadata), `POST /api/public/calculate`, `POST /api/public/sample-invoice`, and `POST /api/public/report-tariff` (see §2). **As of 2026-09 it holds no pricing logic or raw rate data** — all calculation is server-side (§15).

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

No hardcoded secrets or API keys were found in any frontend file.

**Content-Security-Policy, added 2026-07-14** (was previously absent — see §11.2): a `Content-Security-Policy` response header is now set via FastAPI middleware on every response (not via `<meta>` tag). `script-src`/`style-src` retain `'unsafe-inline'` (the frontend's ~hundreds of inline `onclick` handlers and inline `<script>` blocks would need a full refactor to `addEventListener` to remove it, not currently scheduled) plus the two CDN hosts actually used (cdnjs for Chart.js/DOMPurify, Google Fonts). Everything else is locked down: `object-src 'none'`, `base-uri 'self'`, `form-action 'self'`, `frame-ancestors 'self'`, `connect-src 'self'`, `img-src 'self' data:`. **Update 2026-10:** `script-src` is now strict (`'self'` + cdnjs, no `'unsafe-inline'`) for every converted page for every page and all API responses (the temporary `_CSP_LEGACY_PAGES` used during the page-by-page conversion is gone; `admin.js`, like `admin.html`, is only served inside the office/VPN). On every page the CSP now does block injected inline code. Originally: because of the `'unsafe-inline'` allowance, this CSP did **not** block the class of bug the escaping/DOMPurify fixes address — it guards against loading external malicious scripts/styles and locks down framing, forms, plugins, and cross-origin connections, as defense-in-depth on top of (not instead of) output escaping.

**Three follow-up items from this pass, all closed 2026-07-14 (see §11.1, §11.4):**

- ~~The admin notices rich-text editor intentionally renders raw HTML (a WYSIWYG feature, by design) — meaning a compromised admin account has a direct stored-XSS path to the public page.~~ **Closed** via `SECURITY_REMEDIATION_CHECKLIST.md` item 1: DOMPurify 3.1.6 now sanitizes at all 4 sinks touching this content (`customer.html`'s tab renderer and vulnerable-customer modal; `admin.html`'s editor display and save-back path), so a compromised admin account can no longer inject executable script via the notices editor.
- **CSV formula injection**: `admin.html`'s changelog CSV export interpolated tariff/supplier names into CSV cells unescaped; a name starting with `=`, `+`, `-`, or `@` could be interpreted as a formula by Excel/Sheets on open. Fixed with a `csvCell()` helper that prefixes a leading `'` on any such value and correctly doubles embedded `"` per RFC4180 (a pre-existing quoting bug found alongside the injection fix).
- **DOM-based XSS via `location.hash`/`location.search`/`postMessage`**: grepped all 4 frontend files for this pass — the only hit was `reset-password.html`'s `token`/`portal` query-string parsing, confirmed safe (never rendered via `innerHTML`, only compared as a string or forwarded as opaque data). No `postMessage` listeners exist anywhere in the app.

---

## 9. Email / notification subsystem

`email_utils.py` sends all mail via Microsoft Graph (`POST /v1.0/users/{from}/sendMail`), authenticated with `msal.ConfidentialClientApplication` client-credentials flow — no SMTP credentials anywhere. All sends are fire-and-forget on a daemon thread (`_send_bg`) so a slow/failing Graph call never blocks the request that triggered it; failures are logged, never raised to the caller. Templates are table-based HTML with inline styles for Outlook/Gmail compatibility. Notification triggers: new tariff submission, resubmission, approval, rejection, password reset, account lockout, OTP code, password-expiry warning, supplier invite, and broadcast messages (manual and scheduled). Bilingual (EN/EL) templates are used for the password-expiry and broadcast-message notifications; the rest are English-only.

---

## 10. Background scheduler

A single `asyncio` task started on FastAPI startup (`_scheduled_notifications_loop`, `main.py`) runs every hour in-process: fires any due recurring `scheduled_notifications`, and once per day also runs the password-expiry check. This is explicitly a **single-instance design** — the code comment notes that scaling to multiple app instances would double-send without adding a lock. Fine for the current Basic B1 App Service / single-process deployment target; must be revisited if the app is ever scaled horizontally.

---

## 11. Post-checklist hardening (2026-07-14) — `SECURITY_REMEDIATION_CHECKLIST.md`

Four forward-looking hardening items identified during the original review, all closed 2026-07-14 (full detail lives in `SECURITY_REMEDIATION_CHECKLIST.md`; summarized here for the reviewer):

**13.1 DOMPurify for the notices rich-text path.** The admin notices editor (assumptions/legal/vulnerable-customer text, EN/EL) intentionally renders raw HTML — a WYSIWYG feature, not a bug, but it meant a compromised admin account had a direct stored-XSS path to the public page (see §8). DOMPurify 3.1.6 (vendored via cdnjs, the same CDN already used for Chart.js) now sanitizes at all 4 sinks: `customer.html`'s `switchNoticesTab()`/`openVulnerableModal()` and `admin.html`'s `setNotices()`/`getNotices()`, so a payload can't round-trip through the admin's own editor either.

**13.2 Content-Security-Policy header.** See §8 for the policy detail and the `'unsafe-inline'` tradeoff.

**13.3 Server-side input validation (`tariff-api/schemas.py`).** Rewrote the Pydantic schemas: `Literal[...]` types for every enum-like field (`contract`, `voltage`, `pricing`, `fpaSource`, `loadEntitlement`, tariff `status`, message/notification `audience`) matching the exact value sets the frontend's `<select>` elements use — a raw API call with a valid JWT can no longer set an arbitrary string in these fields. Added `max_length` bounds to every free-text field and `ge`/`le` bounds on numeric duration fields. `SupplierIn.email`/`CreateUserIn.email` now validate through the `email-validator` library; `SupplierIn.website` now requires an `http://`/`https://` scheme — this is the root-cause fix for the `javascript:`-URL finding in §8 (a supplier can no longer *submit* such a URL, not just have it neutralized at render time by `safeUrl()`). `rates`/`discounts` remain loosely-typed JSON since their shape varies by pricing type.

**13.4 Reduced `innerHTML` reliance at the 3 highest-risk sinks.** Rewrote `admin.html`'s `renderLoginActivity()`, `buildDashboard()`'s pending-review widget, and the tariff review modal (`openReview()`) to build real DOM nodes (`document.createElement`/`.textContent`) instead of HTML template-literal strings — untrusted data can only ever render as text at these 3 sinks now, independent of whether `esc()` is called correctly. This was a targeted rewrite of the most severe sinks, not all ~116 `innerHTML` sites; the remainder still rely on the `esc()` escaping pattern documented in §8, which was verified live in the original XSS pass.

Also closed alongside this pass: the CSV formula-injection fix and the DOM-based-XSS (`location`/`postMessage`) grep documented in §8.

---

## 12. Post-XSS security review (2026-07-15)

A further pass covering vulnerability classes not addressed by the original review or the checklist above: SQL injection, buffer overflow, broken access control, email injection, OTP brute-force, dependency CVEs, and JWT storage. All 7 items closed; each was verified live against a disposable SQLite database (the real Postgres dev database was never touched) using the project's actual `.venv` Python environment.

**14.1 SQL injection — checked, clean.** Every data query in `tariff-api/` goes through SQLAlchemy's ORM (`db.query(Model).filter(Model.col == value)`), which parameterizes automatically. The only raw SQL in the codebase is `main.py`'s startup migration block (hardcoded `ALTER TABLE` literals, one bound `:now` parameter) — no user input reaches it.

**14.2 Buffer overflow — not an applicable vulnerability class.** Pure Python/JS stack, no `ctypes`/`struct`/native extensions handling raw buffers. The PDF-upload path (the only raw-bytes handling in the app) uses Starlette's dynamically-sized `UploadFile.read()` with the size cap, magic-byte check, and UUID storage filename already described in §7.

**Bonus finding, fixed alongside this item:** the document-download `Content-Disposition` header injection described in §7.

**14.3 Broken access control / IDOR — found and fixed.** Three routes in `routers/admin.py` did not enforce the ownership checks used consistently elsewhere (§4):

- `GET /api/admin/config` and `GET /api/admin/changelog` returned the **entire changelog unfiltered** to any authenticated supplier — other suppliers' tariff names, diffs, and admin actor emails, even though the tariffs list itself was correctly scoped. Fixed by filtering `Changelog.supplier == user.supplier_name` for supplier-role users.
- `GET /api/admin/suppliers` returned every supplier's full contact record (address/email/tel/website/licence) to any logged-in supplier, despite the file's own docstring already saying "admin only". Fixed by switching its dependency to `require_admin` — confirmed via grep that no frontend page needed the unfiltered version (`admin.html` gets suppliers through the already-scoped `/config` bulk endpoint).

Verified live with two distinct supplier accounts, each with their own tariff and changelog entry — confirmed one supplier's token can no longer see the other's data, while an admin token still sees everything. 8/8 checks passed.

**14.4 Email HTML injection — found and fixed.** `email_utils.py` sends via Microsoft Graph's structured JSON `sendMail` call (not raw SMTP), so classic CRLF/header injection does not apply. However, `tariff_name`/`supplier`/rejection `reason` were interpolated **unescaped** into the HTML email bodies sent to admin and supplier inboxes on tariff submit/resubmit/approve/reject — all attacker-reachable via the tariff-submission form (schemas.py bounds `name`'s length but doesn't escape its content). This is the same bug class as the §8 stored-XSS findings, just landing in a mail client instead of a browser — a supplier could inject phishing links or tracking pixels into a legitimate CERA-branded email. Fixed with an `_esc()` (`html.escape`) helper applied at all 5 call sites touching an HTML body. Verified by mocking the Graph API call and injecting `<img src=x onerror=...>`/`<script>` payloads — captured payload showed properly escaped entities.

**14.5 OTP brute-force — found and fixed.** `verify_otp()` in `routers/auth.py` had no attempt limit independent of the password-login lockout (§4) — once past the password step, an attacker holding a `pending_token` could guess the 6-digit OTP (1,000,000 possibilities) unlimited times within its 10-minute validity. Fixed by reusing the existing `User.failed_attempts`/`locked_until` fields the password lockout already uses (no schema change needed, since a correct password already resets both to 0 immediately before OTP verification starts). Verified live: 2 wrong guesses → 401, a 3rd → 429 locked, and — critically — the actual correct code was also rejected while locked, proving the lockout blocks even an eventual correct guess, not just further wrong ones.

**14.6 Dependency CVE scan — checked, clean.** `pip-audit` against both `requirements.txt` and the actually-installed `tariff-api/.venv` environment found no known vulnerabilities in any resolved package (FastAPI, Starlette, SQLAlchemy, psycopg, PyJWT, bcrypt, msal, requests, Pydantic, email-validator, and transitive dependencies). Note: this surfaced that ad-hoc terminal commands (this review and presumably earlier work) had been invoking the machine's global Python rather than the project's `.venv` — the venv itself was correctly set up and is now the one actually used for running/testing this app.

**14.7 JWT storage — migrated from `sessionStorage` to an httpOnly cookie.** See §2, §4, and §8 for the full description of the before/after design and the CSRF implication (`SameSite=Strict`). In short: `sessionStorage` was JS-readable, so any successful XSS could exfiltrate the live session token; an httpOnly cookie cannot be read by JavaScript, closing that theft vector even against XSS bugs not yet found. Verified live with a real Chromium browser via Playwright (not just an HTTP client — Python's `requests`/`http.cookiejar` doesn't implement the browser-specific "localhost counts as a secure context" exception needed to resend a `Secure` cookie over plain `http://`, so only a real browser test is authoritative here): cookie carries `HttpOnly`/`Secure`/`SameSite=Strict` with no `Max-Age`; `document.cookie` never exposes the token; session persists across reload; logout clears the cookie server-side (a new `POST /api/auth/logout` endpoint, since JS cannot clear an httpOnly cookie itself) and does not silently re-authenticate; the two FormData document-upload paths that used to attach the token manually now work with zero explicit client-side auth code. 19 checks across both portals, zero console errors.

**Deployment implication:** the cookie's `Secure` flag means login requires HTTPS in a real deployment — this doesn't add a new requirement (HTTPS was already tracked below) but makes it load-bearing rather than just good practice; worth calling out explicitly to whoever handles the external deployment.

**Known accepted limitation:** opening the HTML files directly via `file://` instead of through the server no longer supports login (a cookie set by `http://localhost:8000` cannot be read back by a `file://`-origin page). Confirmed this doesn't affect the documented workflow — `start.bat` already serves everything same-origin via uvicorn.

---

## 13. Session hardening, accidental-overload protection & cross-portal access control (2026-07-15, later pass)

Prompted by a direct question — "are we protected against a buggy frontend retrying in a loop, or someone running a script that hammers the server by mistake?" — which led to fixing that gap and then, during live testing of the fix, surfaced two real access-control gaps between the admin and supplier portals. All items below were verified against the running app, not just read in code.

**15.1 Per-IP rate limiting.** No rate limiting of any kind existed previously. `slowapi` was tried first and found broken on this stack: FastAPI 0.139.0 / Starlette 1.3.1 wraps routers registered via `app.include_router()` in an internal `_IncludedRouter` object that slowapi's route-handler lookup doesn't recognize, so its limiter silently applied only to the one route declared directly on `app` (`/api/public/config`) and did nothing for `/api/auth/*` or `/api/admin/*` — confirmed empirically (a 3/min test limit tripped correctly on `/api/public/config` but never on `/api/auth/login` after 6+ requests). Replaced with a small self-contained sliding-window counter (`main.py`, keyed by client IP, no routing-library dependency, no third-party package) — 60 requests/minute per IP, returns `429` past that. In-memory only, correct for the current single-process deployment; would need a shared store (Redis) if ever scaled to multiple workers/instances. Rate-limit hits on `/api/auth/*` are also written into the existing `login_activity` table (`reason: "rate_limited"`) so they're visible in the admin panel's Login Activity tab alongside lockouts, not just in server logs. Verified live: 65 rapid requests to `/api/auth/login` → first 60 succeed, remainder return `429`, each logged with email/IP.

**15.2 Sliding session expiry with an absolute cap.** See §4 (Token design) for the mechanism. Motivated by a direct question about whether shortening the flat token expiry (originally 8 hours) risked logging an active user out mid-work — it did, since no renewal mechanism existed at all. Fixed by making expiry slide on activity (1 hour, renewed every authenticated request) while capping total session lifetime at 12 hours from the original login (`session_start` claim, immune to renewal). Caught and fixed a real bug during testing: PyJWT only auto-converts the *registered* `iat`/`exp`/`nbf` claims from `datetime` — the custom `session_start` claim needed an explicit `.timestamp()` conversion or every request crashed. Verified live: chained requests show `session_start` unchanged while `iat`/`exp` advance; a hand-crafted 13-hour-old session was correctly rejected with `401` even though its own `exp` was still valid.

**15.3 Identity re-hydration (`GET /api/auth/me`).** See §4. Fixed a UX bug (not a security issue) where a valid session cookie in a fresh tab or after a reload never repopulated the frontend's cached identity (email/role in `sessionStorage`), so the Sign-out button and user badge silently never appeared even though the user was correctly authenticated.

**15.4 Cross-portal role enforcement — found and fixed.** Two frontend gaps let the wrong role load the wrong portal's UI:
- `supplier.html` explicitly accepted `role === 'admin'` logins.
- `admin.html` treated any `200` from `GET /api/admin/config` as proof of being an admin — but that endpoint just scopes tariffs down for supplier accounts rather than rejecting them (see §12.3), so a supplier's cookie on a fresh `admin.html` tab sailed straight through.

Both portals now explicitly verify the caller's role (via cached identity or `/api/auth/me`) before rendering their dashboard, and treat a mismatch exactly like "not authenticated" — showing the normal login screen — rather than auto-redirecting to the other portal (an earlier iteration of the fix did redirect; changed at the user's request so a wrong-role session doesn't get any information about where it *should* go). Wrong-role login/OTP attempts and any forced sign-out now show the same generic messages used for any other auth failure (`"Invalid email or password."` / `"Your session was terminated — please sign in again."`) — no mention of roles, portals, or account existence, to avoid giving an attacker probing the login form any information beyond "that didn't work."

**Verified this was a UI exposure, not an authorization bypass**, by attacking the API directly with a real supplier token, bypassing the frontend entirely: approving a tariff (`403 Admin access required`), deleting/creating/reading another supplier's tariff (`403 You can only modify your own tariffs` / `"You can only create tariffs for '<name>'"`), listing all portal users (`403`), and deleting a supplier (`403`) were all correctly rejected server-side — while the same account's own tariff remained fully accessible (`200`). Every mutating endpoint in `routers/admin.py` was also read end-to-end and confirmed to use `require_admin` or the `_assert_tariff_owner`/`is_supplier` ownership checks already documented in §4 and §12.3. The actual authorization boundary was correct throughout; what was broken was only which page's UI a given session was allowed to render.

**15.5 Cross-tab session collision (`X-User-Role` header) — found and fixed.** The session cookie is shared across every tab in a browser, not per-tab. Logging into a different role in a second tab silently overwrites the cookie everywhere, including an already-open tab on the other portal. In one direction (an admin tab whose cookie becomes a supplier's) this surfaces as `403`s on admin-only calls; in the other direction (a supplier tab whose cookie becomes an admin's) there is **no error at all** — admin sessions are allowed everywhere — so status-code-based detection can't catch it, and the supplier tab would silently start receiving full unfiltered cross-supplier data.

Fixed with a new response header rather than reactive error handling: `main.py` middleware decodes whatever cookie is actually attached to each request and sets `X-User-Role` on every response. Both portals' existing global `fetch` interceptor (already used for the password-expiry gate) compares that header against the role the tab expects (`sessionStorage`) on every single response and forces a fresh login — same generic "session terminated" message as §13.4 — the moment they diverge, regardless of which endpoint triggered it. Verified live: a real admin token yields `X-User-Role: admin`, a real supplier token yields `X-User-Role: supplier`, an unauthenticated request has no such header (doesn't interfere with existing `401` handling).

**Known accepted limitation**, confirmed with the user rather than assumed: this does not allow simultaneous admin + supplier sessions in the same browser — that's a hard limit of any cookie-based session design (identical to why one browser can't hold two different Gmail accounts in two regular tabs), not something app code can fix without reintroducing the JS-readable-token XSS risk that §12.7 deliberately closed. The practical workaround for testing both roles at once is a separate browser profile or a private/incognito window.

---

## 14. Functional/data-integrity work, 2026-07-17 to 2026-07-20 (not a security review pass)

Five days of ordinary feature and bugfix work followed §13, none of it prompted by a security review, but three items are relevant to this document and are recorded here so the doc stays an accurate description of the running system.

**16.1 Supplier↔user linkage replaced with a real foreign key.** Previously `User.supplier_name` (and `MessageRead.supplier_name`) were plain strings that had to exactly match `Supplier.name`, with no FK enforcing the relationship — renaming a supplier in the admin panel silently orphaned any user row still holding the old name, with no error. This wasn't a hypothetical: renaming "EAC Supply" cut off a real supplier user (`cera.progress@gmail.com`) from all 6 of their tariffs. Fixed by adding a real `supplier_id` FK (`ForeignKey("suppliers.id")`) to both tables, backfilled via `scripts/migrate_supplier_fk.sql` (verified zero NULLs before the old string columns were dropped via `scripts/drop_supplier_name_columns.sql`). `CurrentUser.supplier_name` is now resolved live on every request via `auth.resolve_supplier_name()` (a `db.get(Supplier, user.supplier_id)` lookup) rather than read from a stored column, so a rename is reflected instantly everywhere with nothing left to cascade. `Tariff.supplier` and `Message`/`ScheduledNotification.target_suppliers` were deliberately left as plain strings (a bigger normalization effort, and not where the actual bug lived); `update_supplier()`'s existing rename-cascade logic now also covers `ScheduledNotification.target_suppliers`, which the original cascade had missed.

**16.2 Scheduled local database backup.** §18 previously listed "no managed backup" as an open risk with zero mitigation in place. There is now a **daily local `pg_dump`** (`tariff-api/scripts/backup_db.ps1`, Windows Scheduled Task, 10:00 daily) producing a custom-format (`-Fc`) archive with 14-day daily + 8-week weekly rolling retention and automatic pruning, written to a OneDrive-synced folder (giving it off-machine redundancy without a manual step). Credentials are read from `%APPDATA%\postgresql\pgpass.conf`, not embedded in the script. Verified end-to-end: both a manual run and an actual Scheduled Task trigger produced an archive that `pg_restore -l` confirmed contains all 101 database objects. The restore procedure (overwrite-in-place vs. restore-to-a-throwaway-database-to-inspect-first) is documented in `ADMIN_MANUAL.md` §13.5. This is explicitly **temporary insurance for the current dev-only Postgres instance**, not a replacement for real managed backups once migrated to Azure Database for PostgreSQL (Flexible Server's built-in automated backups supersede this local script at that point) — §18 item 4 below is updated to reflect partial mitigation, not closure.

**16.3 Changelog data-loss bug found and fixed — worth the external reviewer's attention.** The `changelog` table is meant to be an append-only audit trail (§3), but the legacy bulk "Save & publish" flow (`importer.py`'s `import_cfg()`) was deleting and rebuilding it from whatever snapshot the browser happened to hold in memory at the time — **this had already silently wiped the production changelog table before the bug was found**, with no backup in place at the time to recover it (predates §14.2). Fixed by making every admin section (suppliers, load profiles, notices, DAM data — tariffs and regulated charges already worked this way) save itself immediately via its own REST endpoint instead of staging changes for a bulk publish step, and by removing `import_cfg()`'s changelog-clearing behavior entirely; "Save & publish" is now an optional manual full-resync checkpoint rather than the only way changes reached the database. A related orphaning bug was fixed alongside it: "overwrite profile by name" previously generated a fresh random id every time, silently breaking any tariff's `profileId` reference to the old row — it now reuses the existing profile's id. Also: the changelog UI now resolves `profileId` changes to the profile's current name and maps raw camelCase field keys to human-readable labels, and a "Clear log" button was removed (no longer appropriate for an append-only audit trail). `ADMIN_MANUAL.md` (now v1.4) documents the new per-section save behavior. **Update 2026-09-30:** "Save & publish" has since been removed entirely (it still replaced all data and reset every tariff to approved); see `SECURITY_REMEDIATION_CHECKLIST.md` Round 12.

**Why this belongs in a security-facing document:** an append-only audit trail silently losing data on a routine admin action, with no backup to recover it, is exactly the kind of integrity gap an external assessment would flag — worth disclosing proactively rather than letting it surface as a "finding." It is now fixed and the backup in §14.2 provides a recovery path if a similar bug recurs.

---

## 15. Customer-data-exposure remediation — calculation moved server-side (2026-09-03 → 09-04)

A reviewing security specialist observed that "on the customer tab, the whole application is loaded onto the browser." Investigation confirmed this was substantive, not just a comment about readable source: `customer.html` shipped ~500 lines implementing the entire tariff-pricing engine (four pricing modes, regulated charges, discounts, tiers, sample-invoice/VAT generation), and `GET /api/public/config` dumped the **full raw pricing dataset** to any anonymous visitor — every approved tariff's rate tiers/FPA/discounts/standing charges, full 48-slot × 12-month half-hourly load-shape profiles, all CERA-regulated rates, and two years of Day-Ahead-Market price series. Anyone could view-source or inspect the network response and walk away with the complete current rate book and pricing algorithm for every supplier. Unlike the admin/supplier portals — whose *actions* are gated server-side (§4) — the customer page had nothing held back: the thing of value (calc logic + full pricing data) had no protecting layer. Full rationale and phased plan in `SECURITY_REMEDIATION_PLAN_customer_data_exposure.md`.

**15.1 Server-side pricing engine.** The entire client-side engine was ported to a pure-function Python package, `tariff-api/pricing/` (one module per concern: day-counts/holidays, HHFF profile math, regulated charges, discounts, tiers, the four-mode `monthly_breakdown` engine, sample-invoice generation, and a `display` module that builds curated derived display strings so raw rate tables never need to leave the server). It is exposed via two new endpoints in `routers/public_calc.py`: `POST /api/public/calculate` (ranked per-tariff costs + 12-month breakdown + a `display` block) and `POST /api/public/sample-invoice` (on demand when a customer opens the sample-invoice modal). Numeric parity with the old JS was verified across a matrix of tariffs × consumption values × billing modes × discount/offers states before cutover.

**15.2 `customer.html` cut over.** `applyFilters()` is now async and POSTs the customer's inputs to `/api/public/calculate` (debounced on the two consumption fields, with a request-id guard against out-of-order responses) and renders the returned results; ~520 net lines of dead client-side calc were deleted. See §2 and §8 for the updated request flow.

**15.3 `GET /api/public/config` trimmed.** Now returns display/filter metadata only — `profiles`, `regulated`, and all DAM series are gone entirely, and each tariff no longer carries `rates`/`discounts`/`mdmSource`/`fpaSource`/`profileId`. Verified via curl that the trimmed config produces byte-identical `/api/public/calculate` results to before, and that `customer.html` has no remaining reference to the removed fields.

**15.4 Related data-minimization fix.** `GET /api/admin/profiles` (used by `supplier.html` to populate a picker) returned the full half-hourly shape arrays for every profile, but the supplier page only renders id/name/desc. The endpoint is now role-gated: suppliers get id/name/desc only, admins still get the full data. Not itself a vulnerability (profile shapes aren't proprietary and the endpoint requires a supplier session), but the same "don't ship data the browser doesn't use" principle.

---

## 16. Penetration test of the new public endpoints (2026-09-14)

An authorized live pen test against the new public `calculate`/`sample-invoice` endpoints found and fixed:

**16.1 Non-finite / extreme numeric inputs → 500 (fixed).** `annualKwh`/`monthlyKwh` accepted the non-standard JSON literals `NaN`/`Infinity` (Pydantic's `float` doesn't reject them by default), which crashed the pricing engine with an unhandled 500. Worse, the 422 meant to reject them itself 500'd, because Pydantic echoed the offending non-finite value into the error payload and Starlette's default JSON encoder (strict `allow_nan=False`) then raised while serializing that very error. **Fix:** `allow_inf_nan=False` plus a sane upper bound (5,000,000) on both fields in `schemas.py`, and a `RequestValidationError` handler in `main.py` that sanitizes non-finite floats in the error payload before encoding. Verified: NaN/Infinity/1e20/negative all return clean 422s; normal requests still 200.

**16.2 Document-ID enumeration (fixed).** `GET /api/admin/documents/{id}/download` returned 403 for another supplier's document versus 404 for one that doesn't exist, letting an authenticated supplier enumerate which document IDs exist system-wide. Both cases now return 404.

**16.3 Division-by-zero in the Dynamic annual-mode calc (fixed).** Found by an independent second-opinion code review of the remediation diff: the annual-mode branch of `monthly_breakdown()`'s Dynamic-pricing slot calculation divided by `annual_hhff` with no zero-guard (the adjacent monthly branch already had one). A Dynamic tariff whose assigned profile had all-zero shape data would crash every customer's comparison request in annual mode — where the original JS silently produced `NaN` and never crashed. Mirrored the existing zero-guard (spread evenly instead of dividing). Reproduced pre-fix, confirmed fixed, and confirmed a real Dynamic tariff's cost was unchanged.

---

## 17. Black-box security test (2026-09-25)

Outside-attacker testing over HTTP against an **isolated instance** on a throwaway database (real dev/prod DB never opened), exercising the anonymous, supplier, and admin roles. Fixes live on branch `security/blackbox-findings-2026-09-25` (not yet merged at time of writing). Full itemized record in `SECURITY_REMEDIATION_CHECKLIST.md` Round 9.

**17.1 Supplier could read admin-only reference data (fixed).** `GET /api/admin/dam`, `/api/admin/regulated`, and `/api/admin/regulated/history` used `get_current_user`, so any authenticated supplier could read the full DAM price series and the regulated-charge table/history — while sibling admin GETs (users/suppliers/login-activity/scheduled-notifications) already required admin. Impact is limited (shared regulator/market reference data, not another supplier's private data or PII), but inconsistent with the endpoints' gating and with the §15 effort to keep this data off the public surface. **Fix:** all three switched to `require_admin`. Verified: supplier → 403, admin → 200, no supplier-portal regression (`supplier.html` never called these), and `/api/public/calculate` still computes (it reads the data internally, not via the gated route).

**17.2 Reviewer/demo setup was broken (fixed).** Migration `83ce50ff9ed3` used `ALTER COLUMN ... DROP NOT NULL`, which SQLite rejects, so `seed_demo_data.py` (the documented path for the external reviewer to stand up the app) crashed. **Fix:** wrapped in `batch_alter_table` — works on SQLite and PostgreSQL alike (identical DDL on Postgres).

**17.3 Rate-limit trust of `X-Forwarded-For` (deployment hardening, documented — not a code change).** The per-IP limiter (§13.1) keys on `request.client.host`, which behind a proxy is derived from `X-Forwarded-For` via uvicorn's `ProxyHeadersMiddleware` (default `forwarded_allow_ips="127.0.0.1"`). Rotating that header created unlimited rate-limit buckets **when the caller is a trusted proxy IP** (as in loopback testing); a remote attacker against a directly-exposed instance is not on the trusted list, so the limiter holds today. A code change to parse XFF ourselves would *introduce* the spoof, so the correct fix is deployment config — documented in `AZURE_DEPLOYMENT_CHECKLIST.md` Step 6a: never set `FORWARDED_ALLOW_IPS=*`, ensure the front end overwrites client-supplied XFF, and note that the per-account lockout (§4), which keys on the account rather than the IP, is the real brute-force defense.

**Confirmed still solid** (recorded so they aren't re-tested from scratch): anon → all admin routes 401; supplier → admin-only reads/writes 403; cross-supplier tariff GET/PUT/PATCH/DELETE denied; supplier self-approve denied; document-download 404-uniform (§16.2 holds); input validation on `calculate` all 422 (§16.1 holds); no login/forgot-password user enumeration; session cookie carries `HttpOnly` + `SameSite` + `Secure`; trimmed public config carries no raw pricing (§15.3 holds). Two automated-scan false positives were ruled out (a "Volt" tariff-leak that matched the substring in `"voltage"`, and a "regulated" match inside changelog text) — scoping and the public config are both correct.

---

## 18. Known outstanding risks (pre-production checklist)

These are tracked items, not yet remediated, in priority order for an external certification review:

1. **Secrets in plaintext `.env`** (§5) — highest priority, easiest finding for any reviewer. **Proposed fix: §19.2** (Azure Key Vault / App Service Application Settings).
2. **Azure `Mail.Send` application permission not yet scoped** via Exchange Application Access Policy (§5) — requires a Global/Exchange admin. **Not resolved by the Azure hosting proposal in §19** — this is an Exchange Online mail-administration action independent of where the app itself runs; it stays blocked on someone at CERA with the right admin role regardless of hosting decisions.
3. **No HTTPS/reverse proxy** in the current setup — must sit behind TLS termination before external exposure. Now load-bearing, not just best practice: the session cookie's `Secure` flag (§12.7) means login will silently fail without it. **Proposed fix: §19.1** (Azure App Service's built-in TLS termination).
4. **Dev-only PostgreSQL instance** — user-owned, non-service process, no TLS/HA. **Partially mitigated 2026-07-17 (§14.2)**: a daily local `pg_dump` with rolling retention now exists, so the data is no longer unrecoverable — but this is temporary insurance, not a substitute for a real managed Postgres with proper TLS/HA before production. **Proposed fix: §19.3** (Azure Database for PostgreSQL Flexible Server).
5. ~~No Alembic migrations~~ **Closed 2026-07-23.** Schema is now managed by Alembic (`tariff-api/migrations/`) instead of hand-rolled `ALTER TABLE` statements. `main.py` runs `alembic upgrade head` at every startup (no manual step added to the existing workflow), giving a real version history and a rollback path (`alembic downgrade`) that the old approach didn't have. A baseline migration captures the schema as it stood at introduction; the real dev Postgres instance needs a one-time `alembic stamp head` (bookkeeping only, no schema/data change) rather than having that baseline re-run against tables that already exist — see `tariff-api/migrations/README.md`.
6. ~~Minor audit-trail gaps~~ **Closed 2026-07-23.** OTP-toggle-per-user and document-upload-triggered-resubmission now write to `changelog`, using the same helper already used for tariff/regulated-charge changes, scoped to the affected supplier. Verified live against a disposable database.
7. Document-upload feature has no malware/content scanning (acceptable today given admin-gated approval, worth reassessing if exposure changes). **Proposed fix: §19.4** (Azure Blob Storage + Defender for Storage Malware Scanning).
8. **Local git history only, no remote** — **Closed 2026-07-23.** Repository is now hosted on a private GitHub remote (`github.com/koussip/tariff_app`) shared with the external specialist for this review; full history was scanned for secrets before pushing (clean).

Two items from the original version of this list are now closed and removed from tracking: stored XSS on the public customer page (§8, fixed 2026-07-14) and the absence of version control (§1, a local repository now exists). A later item is also closed: **public exposure of the full pricing dataset and calculation logic** on the customer page (fixed 2026-09 by moving calculation server-side and trimming the public config — §15).

An external IT company is expected to perform a combined functional/UAT walkthrough and OWASP-style security assessment before go-live; the items above are the ones most likely to surface in that assessment and should be prioritized accordingly. **§19 below sketches our proposed hosting architecture for items #1, #3, #4, and #7 — feedback and objections from the reviewer are explicitly welcome before we commit to it.**

---

## 19. Proposed production deployment architecture (Azure)

**Status: proposed, not yet built.** This section sketches the intended production hosting architecture, addressing outstanding risks #1, #3, #4, and #7 in §18 together as one deployment decision rather than four separate ones. **Nothing below has been provisioned yet** — this is presented for the external reviewer's comment before we commit to it. If the reviewer proposes a different approach, we want to hear it before infrastructure exists to unwind.

### Why Azure, and why an isolated deployment

Three reasons drove this direction, worth stating explicitly for the reviewer's assessment:

1. **Existing organizational relationship.** CERA already holds a Microsoft account for Microsoft 365 and other software, so Azure isn't a new vendor relationship or a new procurement/legal process — it extends an existing one.
2. **EU data residency.** Azure has EU regions (e.g. West Europe, North Europe) that keep all data — the database, uploaded documents, secrets — within the EU under EU law, which matters for a regulator's own data.
3. **Deliberate isolation from CERA's existing infrastructure.** The proposal is to run this app in its **own dedicated Azure resource group** (or its own subscription, if the reviewer prefers stronger isolation), with no shared services, no shared VNet, and no shared Active Directory trust with anything else CERA runs — including anything already hosted on-prem or elsewhere in Azure. This is a considered choice, not a limitation: it means a compromise or misconfiguration in this app cannot cascade into any other CERA system, and a problem elsewhere in CERA's infrastructure cannot affect this app. This is also the direct answer to "why not host on a local CERA server" — an isolated cloud deployment has a smaller, better-defined blast radius than adding another service to shared on-prem infrastructure that other systems also depend on.

### 19.1 Compute — Azure App Service

The app is a stock FastAPI/uvicorn application with no unusual runtime requirements — App Service's native Linux/Python runtime should run it directly from `requirements.txt`, the same way `start.bat` does locally, with no code changes required. Containerizing it (a Dockerfile, deployed to App Service's container support) is a secondary option worth the reviewer's opinion on — it adds a small amount of build complexity but guarantees the exact same environment in every stage (dev/staging/prod), which the current `.venv`-based workflow doesn't strictly guarantee.

**One hard constraint carried over from §10**: the in-process background scheduler (`main.py`'s `_scheduled_notifications_loop`) is explicitly single-instance — running two copies would double-send scheduled notifications, since there's no distributed lock. App Service must be pinned to a **single instance with autoscale disabled** unless that scheduler is redesigned first. At this application's expected load, a single instance should be more than sufficient — this is a configuration constraint to remember during setup, not a capacity concern.

### 19.2 Secrets — Azure Key Vault / App Service Application Settings

`config.py` (§5) already reads every secret via `os.getenv()` with no assumption about where the value comes from — this was built specifically so this step requires no code changes. Two options, in order of how much initial setup they need:

- **App Service Application Settings** — the simplest path: every current `.env` variable becomes an Application Setting in the Azure Portal, encrypted at rest by Azure, injected as real environment variables at runtime. This alone already closes risk #1 (plaintext `.env` on disk).
- **Azure Key Vault**, referenced from App Service via Key Vault references — a more mature setup: centralized secret rotation, access policies/RBAC on who can read which secret, and an audit log of every access. Worth it if CERA wants a formal secret-rotation policy (tying back to the manual `AZURE_CLIENT_SECRET` rotation done earlier this review) rather than ad hoc rotation.

Recommendation: start with Application Settings for the initial deployment (fast, zero new infrastructure to learn), graduate to Key Vault once the deployment is stable — the migration between the two is a config change, not a code change.

### 19.3 Database — Azure Database for PostgreSQL Flexible Server

Replaces the current dev-only, user-owned Postgres process (§18 item #4) with a managed instance: automated backups, TLS by default, and uptime that doesn't depend on a laptop staying on. Same region as the App Service instance, for latency. `DATABASE_URL` (already the single point of database configuration — see `config.py`, §5) is the only thing that changes in the app itself.

**Networking**: the reviewer's input is wanted here specifically — whether Flexible Server should sit behind a **private endpoint** reachable only from the App Service's VNet integration (stronger isolation, requires an App Service plan tier that supports VNet integration — Standard or above), versus a simpler public-endpoint-with-firewall-rules setup restricted to the App Service's outbound IPs (less setup, slightly larger attack surface). Given the isolation principle above, the private-endpoint approach is our default preference, but we want to confirm the added complexity is justified at this app's scale before committing to it.

**Migration mechanics**: the same `pg_dump`/`pg_restore` process already used for the local backup script (§14.2) applies — dump the current dev database, restore into the new Flexible Server instance, verify row counts match (the same verification approach used for the original SQLite→Postgres migration on 2026-07-10), then cut `DATABASE_URL` over.

### 19.4 File storage — Azure Blob Storage + Defender for Storage Malware Scanning

Currently uploaded PDFs (`tariff_documents`, §7) live on local disk (`tariff-api/uploads/`), addressed by a fixed path (`_UPLOAD_DIR`) outside `DATABASE_URL`'s reach. This needs to move regardless of the malware-scanning question: App Service's local filesystem isn't reliable persistent storage for user-uploaded content (it can reset across restarts/scaling), so Blob Storage is needed for correctness, not just security.

Once files are in Blob Storage, turning on the **Microsoft Defender for Storage → Malware Scanning** add-on for that storage account gets automatic on-upload scanning "for free" — every blob is scanned using Microsoft Defender's engine as it's written, and the result is attached as blob metadata (clean/malicious), which the app checks before serving a download. This directly closes risk #7 (no malware scanning) as a side effect of the storage migration, rather than a separate subsystem to build.

**Code changes required** (unlike §19.1–18.3, this one isn't config-only): `routers/admin.py`'s upload/list/download endpoints (§7) currently read/write local disk directly and would need to use the `azure-storage-blob` SDK instead — `TariffDocument.stored_name` can keep serving as the blob name with no schema change, and the download endpoint gains one new check (reject the download, or warn, if the malware-scan metadata tag isn't "clean" yet or came back positive).

### 19.5 Rollout sequence (once the reviewer's feedback is incorporated)

1. Provision resources: resource group, App Service plan + app (single instance, autoscale off), Key Vault or Application Settings, Flexible Server, Storage account with Defender for Storage enabled — all in the chosen EU region.
2. Migrate data: `pg_dump`/`pg_restore` into Flexible Server; one-time copy of existing `uploads/` files into Blob Storage.
3. Code change: swap the local-disk upload/download logic for Blob Storage (§19.4) — the only non-config code change in this whole plan.
4. Configure secrets in Application Settings/Key Vault; set `DATABASE_URL` to the Flexible Server connection string.
5. Deploy the app to App Service; confirm `alembic upgrade head` runs cleanly against the fresh Flexible Server instance (it will run the full baseline migration from scratch, same as any new database — see `tariff-api/migrations/README.md`).
6. Update `TARIFF_BASE_URL`/CORS origin to the real production URL (custom domain or `*.azurewebsites.net`), cut DNS over if using a custom domain.
7. Keep the local dev environment (local Postgres, local `.venv`) as-is for ongoing development — production and dev remain separate environments, this migration only affects where the live/production instance runs.

### 19.6 Open questions for the external reviewer

Explicitly flagging these rather than deciding unilaterally:

- Dedicated **resource group** within an existing subscription, or a fully separate **subscription**, for the isolation goal in the intro above?
- Private-endpoint VNet integration for the database (§19.3), or is public-endpoint-with-firewall-rules an acceptable tradeoff at this scale?
- Application Settings vs. Key Vault for secrets (§19.2) — start simple and graduate later, or go straight to Key Vault?
- Native Python runtime vs. containerized deployment for App Service (§19.1)?
- Any objection to the EU region choice, or a preference between specific EU regions (e.g. West Europe vs. North Europe) for latency/compliance reasons we haven't considered?

---

## 20. Summary assessment

The backend shows a consistent, deliberate security design for its size, strengthened further by the 2026-07-14/15 hardening passes: cookie-based session auth with `httpOnly`/`Secure`/`SameSite=Strict` (immune to both XSS-based token theft and CSRF), sliding expiry with an absolute session cap (§13.2), server-side ownership checks on every mutating endpoint (including the changelog/supplier-list gaps closed in §12.3, and re-verified end-to-end during the §13.4 cross-portal review), account lockout with audit logging extended to cover OTP guessing as well as password attempts (§12.5), password history/expiry/reuse enforcement, session invalidation on password change, Pydantic-enforced input validation matching the frontend's actual value sets (§11.3), a Content-Security-Policy header, DOMPurify sanitization on the one deliberate raw-HTML rendering path, consistent output escaping across all 116 audited `innerHTML` sinks, per-IP rate limiting against accidental overload (§13.1), versioned schema migrations (§14, closing what was previously a hand-rolled `ALTER TABLE` approach), and centralized secrets/config handling (§5) as prep work for a real secret store. SQL injection and dependency CVEs were checked and found clean; buffer overflow is not an applicable risk for this stack. The two cross-portal UI gaps found in §13.4/§13.5 were UX/access-routing issues, not authorization bypasses — the underlying permission checks held throughout, confirmed by direct API attack attempts, not just code reading. The remaining gaps are entirely operational/infrastructure (secrets storage, TLS, managed DB, malware scanning) rather than architectural — none of the previously-open code-level findings remain outstanding, and §19 proposes a single Azure-based deployment addressing all four remaining infrastructure gaps together, pending the external reviewer's feedback.

The September 2026 work extends this posture: the largest change was **moving all tariff calculation server-side** and trimming the public config (§15), which closed the one place the customer surface exposed something of value — the full rate book and pricing algorithm — that had no protecting layer. A penetration test of the resulting public endpoints (§16) and a black-box test across all three roles (§17) each found a small number of issues, all fixed or (for the deployment-only `X-Forwarded-For` item) documented, with the core access-control, input-validation, and session controls confirmed intact. The security posture is best understood as a series of dated review passes (§§11–17) rather than a single point-in-time audit; `SECURITY_REMEDIATION_CHECKLIST.md` is the consolidated cross-referenced index of every round.
