# Admin access restricted to CERA network (VPN + office)

> **Status:** implemented 2026-09-30. See `SECURITY_REMEDIATION_CHECKLIST.md` Round 14 for what was built and verified, and `ADMIN_MANUAL.md` §14.9 for operation. Still to do on Azure: the two settings, with addresses from CERA IT.

## Context
Admin accounts can currently sign in and use the admin panel from anywhere on the internet. The API role split (commit `1a14f0b`) put every admin endpoint behind one router-level guard (`require_admin`), so a network restriction can be enforced in one place. The existing pre-go-live item "Restrict `admin.html` to CERA IPs" (`SECURITY_REMEDIATION_CHECKLIST.md`) relied on Azure App Service access restrictions. Those apply to the whole site, not to one page, and wouldn't have protected the API anyway. This plan replaces that item with an in-app check.

**User decisions:**
- **Allowed networks:** the CERA office public IP(s) plus the VPN's outgoing IP(s).
- **Anything admin from outside the network:** only a plain "Website unavailable". That covers the admin page, admin sign-in and any admin action. There is no sign-in error message and no mention of the network.

Suppliers and the public calculator are unaffected.

## Approach

### 1. Trusted client IP: one helper, safe behind Azure (`tariff-api/client_ip.py`, new)
The restriction is only as strong as the client-IP check. Behind Azure App Service, the client IP arrives in `X-Forwarded-For`, which a client can pre-fill with a fake VPN address.
- `client_ip(request) -> ipaddress.IPv4Address | IPv6Address | None`
  - `TARIFF_TRUSTED_PROXY_HOPS = 0` (default, local dev): use the socket peer (`request.client.host`).
  - `= 1` (Azure App Service): use the **rightmost** `X-Forwarded-For` entry. The Azure front end appends it, so the client can't forge it; anything further left is client-supplied and ignored. `= 2` would cover a future Front Door or App Gateway in front.
  - Strip a port (`1.2.3.4:5678`, `[::1]:443`), since Azure includes one. If the value can't be parsed, return `None`, which is treated as "not allowed".
- Also switch the per-IP rate limiter (`main.py`, `rate_limit_middleware`, uses `request.client.host`) to this helper. That closes the open `X-Forwarded-For` item from Round 9 with the same code.

### 2. Configuration (`tariff-api/config.py`)
- `TARIFF_ADMIN_ALLOWED_NETWORKS`: comma-separated IPs/CIDRs (e.g. `203.0.113.10/32,198.51.100.0/28`), parsed once with `ipaddress.ip_network`. An invalid entry stops startup with a clear error.
- **Empty = restriction off.** Local dev and the reviewer demo keep working, but a startup warning is logged, like the existing Azure-email warning in `config.py`.
- `TARIFF_TRUSTED_PROXY_HOPS` (above).
- Helper `admin_network_allowed(request) -> bool`: returns True if the list is empty or the client IP is in any listed network.

### 3. Enforcement points
| Where | File | Behaviour outside the network |
|---|---|---|
| Every authenticated request by an admin (all `/api/admin/*`, plus `/api/auth/me`, `/email`, `/password`) | `auth.py` `get_current_user`: add the check for `user.role == "admin"`, next to the existing `is_active` check | 404 `Not Found`. Covers a stolen admin cookie and a VPN that drops mid-session. |
| Login | `routers/auth.py` `login`: after loading the user, **before** the lockout and password checks, if the user is an admin and off-network → log `LoginActivity(reason="network_blocked")` and return 404 "Website unavailable" | "Website unavailable", as decided. In practice this is only reachable by a script or via the supplier login page, since the admin page itself is already unavailable off-network. The password is never checked, so there's no way to test whether a password is right, and failed-attempt counting and lockout aren't touched: internet attackers can't lock admins out. Trade-off (accepted): a different response than the supplier-login "Invalid email or password" reveals that an email is an admin account. |
| OTP verify / resend | `routers/auth.py` `verify_otp`, `resend_otp` | Same check. Blocks finishing a login started on-network and completed off-network. |
| `admin.html` | `main.py`: small middleware before the static mount; path `/admin.html` (and `/admin.html?…`) | 404 with a minimal "Website unavailable" HTML page. No CERA branding and no mention of the network. |
| Password reset (`/forgot-password`, `/reset-password`) | unchanged | Allowed. A reset alone gives no access, since signing in still needs the network. |

Reuse the existing `_log_login` in `routers/auth.py` for the new `network_blocked` reason, so it shows up in the admin **Login activity** page with the IP.

### 4. Frontend (`admin.html`)
Extend the existing fetch interceptor (~line 5262, which already handles 403 `password_expired` and `X-User-Role`): on a 404 from `/api/admin/*`, `/api/auth/me` or `/api/auth/login` (e.g. the VPN drops mid-session), replace the whole page with the same "Website unavailable" text. No other UI changes.

### 5. Break-glass and operations (docs)
- **`ADMIN_MANUAL.md`:**
  - New §14.9 "Network restriction": what it does, how to change `TARIFF_ADMIN_ALLOWED_NETWORKS` (Azure → App Service → Environment variables → Apply; locally `.env` + restart), and how to switch it off in an emergency (clear the value).
  - Troubleshooting entry: "Admin can't sign in / 'Website unavailable'": check the VPN is connected; check Login activity for `network_blocked`.
- **`AZURE_DEPLOYMENT_CHECKLIST.md`:**
  - Replace the "admin.html access restriction" procedure (~line 350), which describes App Service route rules that don't exist, with the new settings.
  - Update Step 6a: set `TARIFF_TRUSTED_PROXY_HOPS=1`, do not set `FORWARDED_ALLOW_IPS=*`, Cloudflare stays "DNS only" (proxying would add a hop).
- **Items for CERA IT:**
  1. Office egress IP(s).
  2. VPN egress IP(s).
  3. Confirm the VPN is full-tunnel, or add `tariffs.cera.org.cy` to the tunnelled routes. With split-tunnel, the traffic wouldn't come from the VPN IP.
- **`SECURITY_REMEDIATION_CHECKLIST.md`:** new round, and close the "Restrict admin.html" and XFF open items.
- **`TECHNICAL_ARCHITECTURE_REVIEW.md`:** §4 note.

## Local development and testing (no impact by default)
- **Off unless configured.** With `TARIFF_ADMIN_ALLOWED_NETWORKS` unset (the local `.env` won't set it), nothing changes: admin panel, logins, tests and the reviewer demo behave exactly as today. Only a one-line startup warning says the restriction is off.
- **`TARIFF_TRUSTED_PROXY_HOPS` defaults to 0** = the socket peer, which is what the app and the rate limiter use today, so the local behaviour is identical.
- **To try it locally:** add `TARIFF_ADMIN_ALLOWED_NETWORKS=127.0.0.1/32` to `tariff-api\.env` and restart. This PC is then "inside". Anyone opening the app through this PC's LAN address is "outside" (sees "Website unavailable") unless their IP or range is added. Remove the line to switch it off.
- Automated tests pass the settings to a throwaway server directly. They never edit `.env` or touch the real database.
- The restriction only takes effect in production, where Azure App Service settings hold the office and VPN ranges supplied by CERA IT.

## Verification
All on a throwaway SQLite DB with email disabled, server on 127.0.0.1 (never the real DB):
1. **Restriction on, localhost not allowed** (`TARIFF_ADMIN_ALLOWED_NETWORKS=10.99.0.0/16`):
   - Admin login via the API with the **correct** password → 404 "Website unavailable"; `network_blocked` logged; `failed_attempts` unchanged. 10 attempts → no lockout.
   - A supplier signs in normally, and all supplier flows work.
   - An admin cookie obtained earlier → every `/api/admin/*` route (enumerated from OpenAPI) → 404; `/api/auth/me` → 404.
   - `/admin.html` → 404 "Website unavailable"; `/customer.html`, `/supplier.html` → 200; the public calculator works.
2. **Restriction on, localhost allowed** (`127.0.0.1/32`): full admin login, OTP disabled on demo accounts, admin panel works. Rerun the existing role-separation and validation test scripts.
3. **Spoofing** with `TARIFF_TRUSTED_PROXY_HOPS=1`:
   - A request with `X-Forwarded-For: <allowed-ip>, <real-ip>` → blocked, because the rightmost value is used.
   - `X-Forwarded-For: <allowed-ip>` as the only/rightmost entry → allowed. This simulates the Azure front end appending the real IP.
   - Port forms `1.2.3.4:5678` and `[::1]:443` are parsed. Garbage values → blocked.
4. **Restriction off** (empty setting): startup warning logged; everything behaves as today.
5. **Browser (Playwright/Edge):** off-network, admin.html shows "Website unavailable"; switching the setting mid-session → the next admin action shows "Website unavailable". No JS errors.
6. **Before go-live, on Azure itself:** from inside the VPN, and from a phone on mobile data, confirm the IP the app sees (temporary log line or Login activity entry) matches expectations. This is the one step that can't be simulated locally.
