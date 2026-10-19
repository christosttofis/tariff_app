# CERA Tariff Comparison Tool — Azure Deployment Checklist

**Prepared for:** IT Department  
**Date:** July 2026  
**Application:** CERA Electricity Tariff Comparison Tool  
**Technology:** Python / FastAPI web application

---

## What this document covers

Step-by-step instructions to deploy the CERA Tariff Comparison Tool to Microsoft Azure App Service, running on Azure Database for PostgreSQL Flexible Server from day one (with its automated backups), with secrets stored in Azure Key Vault (not in plain configuration) and a custom domain (`tariffs.cera.org.cy`) added via Cloudflare DNS. This is the companion document referenced in `AZURE_DEPLOYMENT_BRIEF_v2.md`.

---

## Prerequisites

Before starting, confirm the following:

- [ ] You have access to the CERA Azure portal (`portal.azure.com`) with permission to create App Service, Azure Database for PostgreSQL, Key Vault, and DNS-related resources
- [ ] You have the application folder (`Tariff backend/`) — copy from the CERA desktop or shared drive
- [ ] You have the Azure Zip Deploy tool or VS Code with the Azure App Service extension installed (see Step 7)
- [ ] You have access to the Cloudflare dashboard for the `cera.org.cy` zone (Step 10)

---

## Step 1 — Prepare the application folder for upload

The application folder structure must look like this before uploading:

```
Tariff backend/           ← this entire folder gets zipped and uploaded
├── customer.html
├── admin.html
├── supplier.html
├── reset-password.html
├── Logo_Transparent.png
└── tariff-api/
    ├── main.py
    ├── config.py
    ├── requirements.txt
    ├── models.py
    ├── schemas.py
    ├── serializers.py
    ├── database.py
    ├── auth.py
    ├── email_utils.py
    ├── importer.py
    ├── create_user.py
    ├── unlock_user.py
    ├── alembic.ini
    ├── migrations/            ← required — main.py runs "alembic upgrade
    │   ├── env.py                head" on every startup; the app will not
    │   ├── script.py.mako        start without this folder
    │   └── versions/
    ├── routers/
    │   ├── admin.py
    │   └── auth.py
    └── (do NOT include .env — settings are entered in Azure, not uploaded)
```

> **Important:** Do NOT include the `.env` file in the zip. Secrets are stored in Azure Key Vault (Step 4) and referenced from App Service settings (Step 5).
> Do NOT include the `tariff.db` database file if you are starting fresh.
> Do NOT include the `venv/` or `.venv/` virtual environment folder — Azure creates its own.

**To create the zip:**
1. Open the `Tariff backend` folder in File Explorer
2. Select all contents (Ctrl+A)
3. Right-click → Send to → Compressed (zipped) folder
4. Name it `tariff-app.zip`

---

## Step 2 — Create the Azure App Service

1. Go to [portal.azure.com](https://portal.azure.com)
2. Click **Create a resource** → search for **Web App** → click **Create**
3. Fill in the form:

| Field | Value |
|---|---|
| **Subscription** | CERA's Azure subscription |
| **Resource Group** | Create new: `rg-tariff-tool` |
| **Name** | `cera-tariff-tool` (or similar — this becomes part of the URL) |
| **Publish** | Code |
| **Runtime stack** | Python 3.12 |
| **Operating System** | Linux |
| **Region** | West Europe (Netherlands) — closest EU region |
| **Pricing plan** | B1 Basic (~€13/month) |

4. Click **Review + create** → **Create**
5. Wait for deployment to complete (~2 minutes)

After creation, the app will be reachable at:
```
https://cera-tariff-tool.azurewebsites.net
```

6. **Enable Managed Identity** — this lets the App Service read Key Vault secrets without storing any credential:
   - Open the App Service → **Settings → Identity**
   - Under **System assigned**, set **Status** to **On** → **Save**
   - Note the **Object (principal) ID** shown — needed in Step 4

---

## Step 3 — Create the Azure Database for PostgreSQL Flexible Server

The application runs on PostgreSQL (not SQLite) from day one — this gets Azure's automated daily backups in place immediately, with no later migration required. See `AZURE_DEPLOYMENT_BRIEF_v2.md`, Section 8 for backup/restore details.

1. In the Azure portal, click **Create a resource** → search for **Azure Database for PostgreSQL** → **Create** → choose **Flexible server**
2. Fill in the form:

| Field | Value |
|---|---|
| **Subscription** | CERA's Azure subscription |
| **Resource Group** | `rg-tariff-tool` (same as the App Service) |
| **Server name** | `cera-tariff-db` (or similar — must be globally unique) |
| **Region** | West Europe (same as the App Service) |
| **PostgreSQL version** | 16 (or latest available) |
| **Workload type** | Development (Burstable tier, B1ms — ~€25/month) |
| **Authentication method** | PostgreSQL authentication |
| **Admin username** | `tariffadmin` (or similar — avoid `postgres`/`admin`) |
| **Password** | Generate a strong password and record it securely — needed below |

3. Under **Networking**: choose **Public access**, then add a firewall rule **Allow public access from any Azure service within Azure** (this permits the App Service to connect without needing a VNet). If CERA's security policy requires it, a private VNet-integrated setup is also possible but is more involved — discuss with IT before choosing this.
4. Click **Review + create** → **Create**. Provisioning takes a few minutes.
5. Once created, open the server → **Databases** → **+ Add** → create a database named `tariffdb`
6. Note the **server hostname** (shown on the server's Overview page, e.g. `cera-tariff-db.postgres.database.azure.com`) — needed for the `DATABASE-URL` secret in Step 4
7. **Confirm automated backups are enabled** (they are by default) — server → **Backup and restore** — note the retention period (35 days by default) and confirm with Regulatory Affairs whether that's sufficient, or whether it should be extended

> **Backup retention and geo-redundancy** are set at server creation and are harder to change afterward. Decide before this step whether CERA needs geo-redundant backup storage (protects against a full regional outage, at extra cost) — see the Backup & Disaster Recovery section of `AZURE_DEPLOYMENT_BRIEF_v2.md`.

---

## Step 4 — Create the Key Vault and store secrets

Secrets are never stored in a configuration file. They live in Key Vault; the App Service reads them at startup via its Managed Identity.

1. In the Azure portal, click **Create a resource** → search for **Key Vault** → **Create**
2. Fill in the form:

| Field | Value |
|---|---|
| **Subscription** | CERA's Azure subscription |
| **Resource Group** | `rg-tariff-tool` (same as the App Service) |
| **Key vault name** | `kv-tariff-tool` (or similar — must be globally unique) |
| **Region** | West Europe (same as the App Service) |
| **Pricing tier** | Standard |

3. Click **Review + create** → **Create**
4. Open the new Key Vault → **Access control (IAM)** → **Add role assignment**
   - Role: **Key Vault Secrets User**
   - Assign access to: **Managed identity** → select the `cera-tariff-tool` App Service identity (from Step 2.6)
   - Click **Review + assign**
5. Open **Objects → Secrets** → **+ Generate/Import**, and create one secret per row below:

| Secret name | Value |
|---|---|
| `AZURE-TENANT-ID` | *(copy from the `.env` file)* |
| `AZURE-CLIENT-ID` | *(copy from the `.env` file)* |
| `AZURE-CLIENT-SECRET` | *(the newly generated app-registration secret — see note below)* |
| `TARIFF-EMAIL-FROM` | Shared/service mailbox address (e.g. `tariffs@cera.org.cy`) — do not use a personal mailbox in production |
| `TARIFF-ADMIN-EMAIL` | Real CERA admin distribution address |
| `TARIFF-SECRET-KEY` | *(generate a new random string — see note below)* |
| `DATABASE-URL` | `postgresql+psycopg://tariffadmin:<password>@cera-tariff-db.postgres.database.azure.com/tariffdb?sslmode=require` *(use the actual admin username, password, and server hostname from Step 3)* |

> **Key Vault secret names cannot contain underscores** — use hyphens (`AZURE-TENANT-ID`, not `AZURE_TENANT_ID`). The reference syntax in Step 5 maps these back to the underscore-named environment variables the application expects.

> **Generate a new Azure client secret** (do not reuse the one from local development): Azure Portal → **App registrations** → the CERA app registration used for tariff-tool email sending → **Certificates & secrets** → **New client secret** → expiry **12 months**. Copy the value immediately (shown once) into the `AZURE-CLIENT-SECRET` Key Vault entry above. Delete the old development secret from the app registration once the new one is confirmed working.

> **Generating TARIFF-SECRET-KEY:** Open PowerShell and run:
> ```powershell
> -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 48 | ForEach-Object {[char]$_})
> ```
> Paste the output as the secret value. This key signs all login tokens — keep it secret and do not reuse the local-development value in production.

---

## Step 5 — Configure App Service settings to reference Key Vault

Instead of pasting secret values directly, App Service settings point at the Key Vault entries created in Step 4. Azure resolves them at runtime using the Managed Identity — no secret ever touches a config file or the deployment package.

1. Open the App Service (`cera-tariff-tool`) → **Settings → Environment variables**
2. Add each setting below using **+ Add**. The value is a Key Vault reference, not the secret itself:

| Name | Value |
|---|---|
| `AZURE_TENANT_ID` | `@Microsoft.KeyVault(SecretUri=https://kv-tariff-tool.vault.azure.net/secrets/AZURE-TENANT-ID/)` |
| `AZURE_CLIENT_ID` | `@Microsoft.KeyVault(SecretUri=https://kv-tariff-tool.vault.azure.net/secrets/AZURE-CLIENT-ID/)` |
| `AZURE_CLIENT_SECRET` | `@Microsoft.KeyVault(SecretUri=https://kv-tariff-tool.vault.azure.net/secrets/AZURE-CLIENT-SECRET/)` |
| `TARIFF_EMAIL_FROM` | `@Microsoft.KeyVault(SecretUri=https://kv-tariff-tool.vault.azure.net/secrets/TARIFF-EMAIL-FROM/)` |
| `TARIFF_ADMIN_EMAIL` | `@Microsoft.KeyVault(SecretUri=https://kv-tariff-tool.vault.azure.net/secrets/TARIFF-ADMIN-EMAIL/)` |
| `TARIFF_SECRET_KEY` | `@Microsoft.KeyVault(SecretUri=https://kv-tariff-tool.vault.azure.net/secrets/TARIFF-SECRET-KEY/)` |
| `DATABASE_URL` | `@Microsoft.KeyVault(SecretUri=https://kv-tariff-tool.vault.azure.net/secrets/DATABASE-URL/)` |
| `TARIFF_BASE_URL` | `https://tariffs.cera.org.cy` *(plain value — not a secret; update once the custom domain in Step 10 is live, or use the `azurewebsites.net` URL until then)* |
| `SCM_DO_BUILD_DURING_DEPLOYMENT` | `true` *(plain value)* |

3. Click **Apply** → **Confirm**
4. After saving, refresh the page and confirm each Key Vault–referenced setting shows a green checkmark (resolved) rather than a warning icon — a warning means the Managed Identity role assignment (Step 4.4) has not propagated yet or the secret name doesn't match exactly.

---

## Step 6 — Set the startup command

In the Azure portal:

1. Open the App Service → **Settings → Configuration**
2. Click the **General settings** tab
3. In the **Startup Command** field, enter exactly:
```
cd tariff-api && python -m uvicorn main:app --host 0.0.0.0 --port 8000
```
4. Confirm **Always On** is set to **On** (same page) — this prevents the app from sleeping between requests
5. Click **Save**

### Step 6a — Client IP and admin network restriction (required)

The app works out who is calling from the client IP. That drives the **admin network restriction** (admin accounts and `admin.html` only work from the CERA office and VPN) and the per-IP rate limiter. Behind Azure App Service, the real client IP is in the `X-Forwarded-For` header. A client can put any address it likes at the *start* of that header, but it can't change the entry the Azure front end appends at the *end*. The app therefore trusts only that last entry (`tariff-api/client_ip.py`).

Add these **Application settings** (App Service → Settings → Environment variables):

| Setting | Value | Why |
|---|---|---|
| `TARIFF_TRUSTED_PROXY_HOPS` | `1` | One proxy (the App Service front end) in front of the app. Use `2` only if Azure Front Door or Application Gateway is added in front later. |
| `TARIFF_ADMIN_ALLOWED_NETWORKS` | e.g. `203.0.113.10/32,198.51.100.0/28` | CERA office egress IP(s) + VPN egress IP(s), comma-separated. **Get these from CERA IT.** Empty = restriction off (a warning is logged at startup). An invalid entry stops the app from starting, so check the log stream after saving. |

Also:
- **Do NOT set `FORWARDED_ALLOW_IPS=*`.** The app doesn't need it (it reads the header itself). With it, uvicorn would trust client-supplied addresses elsewhere.
- **Keep Cloudflare on "DNS only" (grey cloud)** (Step 10). Proxying through Cloudflare would add a second proxy hop and change which entry is the real client.
- **Ask CERA IT to confirm the VPN is full-tunnel**, or to add `tariffs.cera.org.cy` to the routes sent through the VPN. With split-tunnel, an admin's traffic to the site wouldn't come from the VPN address and would be blocked.
- **Verify once after deployment** (Step 8): sign in as an admin from the office or VPN. Then open `https://<site>/admin.html` from a phone on mobile data: it must show only "Website unavailable". Admin → **Login activity** shows the IP the app saw for each attempt. Attempts from outside are logged as `network_blocked`.
- The sign-in lockout (`lockout.py`: 5 wrong passwords block that address for 15 minutes; 30 from all addresses within an hour, or 3 wrong sign-in codes, lock the account for 30 minutes) remains the main defence against password guessing. Its per-address rule needs the real client IP, so `TARIFF_TRUSTED_PROXY_HOPS=1` must be set on Azure (Step 6a); otherwise every caller looks like the same address. Sign-ins to admin accounts from outside the allowed networks are refused before the password is even checked, so they can't lock an admin out.

---

## Step 7 — Deploy the application

**Option A — Azure CLI (recommended for IT)**

If the Azure CLI is installed, open PowerShell and run:

```powershell
az login
az webapp deploy --resource-group rg-tariff-tool --name cera-tariff-tool --src-path "C:\path\to\tariff-app.zip" --type zip
```

**Option B — VS Code extension**

1. Install the **Azure App Service** extension in VS Code
2. Sign in to Azure
3. Right-click the App Service → **Deploy to Web App**
4. Select the `Tariff backend` folder

**Option C — Azure portal drag-and-drop**

1. In the App Service, go to **Development Tools → Advanced Tools (Kudu)** → **Go**
2. In the Kudu interface, go to **Tools → Zip Push Deploy**
3. Drag and drop `tariff-app.zip` onto the page

---

## Step 8 — Verify the deployment

After deployment completes (allow 2–3 minutes for the first start):

1. Open a browser and navigate to:
   ```
   https://cera-tariff-tool.azurewebsites.net/customer.html
   ```
   The customer calculator should load.

2. Navigate to:
   ```
   https://cera-tariff-tool.azurewebsites.net/admin.html
   ```
   The admin login screen should appear.

3. Log in with the admin account credentials (create one first — see Step 9).

If pages do not load, check the application logs (Step 8a).

### Step 8a — Checking logs if something goes wrong

In the Azure portal:

1. Open the App Service → **Monitoring → Log stream**
2. This shows live output from the application, including any startup errors

Common issues:

| Symptom | Likely cause | Fix |
|---|---|---|
| Page shows "Application Error" | Startup command wrong, or missing dependency | Check Log stream for Python error |
| Login fails with server error | `TARIFF_SECRET_KEY` not resolving | Check the Key Vault reference shows a green checkmark (Step 5.4) |
| Settings show a warning icon instead of resolving | Managed Identity role assignment missing or secret name mismatch | Re-check Step 4.4 (role assignment) and that secret names match exactly |
| Emails not sent | `AZURE_CLIENT_SECRET` missing, expired, or wrong mailbox configured | Verify the Key Vault secret value and that `TARIFF_EMAIL_FROM` is a mailbox the app registration can send as |
| Page shows "Application Error" and logs mention a database connection failure | `DATABASE_URL` malformed, wrong password, or the PostgreSQL server's firewall doesn't allow the App Service | Confirm the `DATABASE-URL` Key Vault secret matches Step 4's format exactly, and that Step 3's firewall rule (allow Azure services) is in place |

---

## Step 9 — Create the first admin account

On first deployment, there are no admin accounts in the database. Create one from the Azure console:

1. In the App Service → **Development Tools → SSH** → **Go**
2. In the SSH terminal, run:
```bash
cd /home/site/wwwroot/tariff-api
python create_user.py --email yourname@cera.org.cy --role admin
```
3. Enter a password when prompted
4. Log in to the admin panel

---

## Step 10 — Add the custom domain (`tariffs.cera.org.cy`) via Cloudflare

The `cera.org.cy` DNS zone is hosted on Cloudflare. Follow these steps rather than a generic DNS provider's flow:

1. Log in to the Cloudflare dashboard and select the `cera.org.cy` zone
2. Go to **DNS** → **Add record**:
   - **Type:** CNAME
   - **Name:** `tariffs`
   - **Target:** `cera-tariff-tool.azurewebsites.net`
   - **Proxy status:** **DNS only** (grey cloud) — do **not** enable the orange-cloud proxy; Azure needs to issue and validate its own certificate directly against the App Service, and Cloudflare's proxy would break that
3. In the Azure portal, open the App Service → **Settings → Custom domains** → **+ Add custom domain**
4. Enter `tariffs.cera.org.cy` and click **Validate**
5. Azure will show a **TXT record** to add for domain ownership verification — add it in Cloudflare DNS under the same zone, then click **Validate** again in Azure
6. Once validated, click **Add**
7. Back in the custom domain list, click **Add binding** next to `tariffs.cera.org.cy` → choose **App Service Managed Certificate** → **Create App Service Managed Certificate**, then bind it
   - Certificate issuance can take a few minutes; refresh the page to check status
8. Once bound, update the `TARIFF_BASE_URL` setting from Step 5 to `https://tariffs.cera.org.cy` if it wasn't already set to that value

After this, both `https://cera-tariff-tool.azurewebsites.net` and `https://tariffs.cera.org.cy` will serve the application; only the custom domain should be shared with users.

---

## Restricting access to `admin.html` and the admin API

This is handled **inside the application**, not with App Service access restrictions: those apply to the whole site (customers and suppliers too) and can't target one page or the API. Setting `TARIFF_ADMIN_ALLOWED_NETWORKS` in Step 6a is all that's needed. Outside those networks:
- `admin.html` returns a plain "Website unavailable" page;
- admin sign-in returns "Website unavailable" (the password is never checked);
- every admin API request, even with a valid session, returns "Website unavailable".

Customers and suppliers are unaffected. To change the allowed addresses later, or to switch the restriction off in an emergency, edit or clear the setting and click **Apply**. The app restarts automatically (see `ADMIN_MANUAL.md` §14.9).

---

## Ongoing maintenance

- **Rotate the Azure client secret once per year** (before its 12-month expiry set in Step 4). Generate a new secret in the app registration, update the `AZURE-CLIENT-SECRET` value in Key Vault (same secret name — Azure picks up the new version automatically), then delete the old secret from the app registration. No redeploy needed. Set a calendar reminder ~11 months from creation.
- **Monitor Log stream / Azure Security Centre** periodically (monthly or quarterly) for application errors and platform recommendations.
- **Database backup:** handled automatically by Azure Database for PostgreSQL Flexible Server (daily backups, 35-day point-in-time restore by default) — no manual download or ongoing task required. See the Backup & Disaster Recovery section of `AZURE_DEPLOYMENT_BRIEF_v2.md` (Section 8), and do the one-time test restore recommended there before go-live.
- **Bug reports:** the Regulatory Affairs team is first point of contact for application-level issues; IT's involvement is limited to infrastructure problems (App Service down, certificate errors, Key Vault access failures).

---

## Stopping / pausing the App Service

To stop the app (e.g. at end of tryout period) without deleting anything:

1. App Service → **Overview** → click **Stop**

To delete everything when the tryout is complete:

1. Delete the Resource Group `rg-tariff-tool` — this removes the App Service, Key Vault, and all associated resources

---

## Cost summary

| Resource | Plan | Estimated monthly cost |
|---|---|---|
| App Service | B1 Basic, West Europe | ~€13/month |
| Key Vault | Standard tier | ~€2/month |
| Azure Database for PostgreSQL Flexible Server | Burstable B1ms, includes automated backups | ~€25/month |
| Storage (persistent `/home`) | Included in B1 | €0 |
| Custom domain + managed certificate | Included, no extra cost | €0 |
| Outbound data transfer | First 5 GB/month free | ~€0 for tryout |
| **Total** | | **~€40/month** |

The App Service can be stopped when not in use to reduce compute costs — a stopped App Service is not billed for compute. The PostgreSQL Flexible Server can also be stopped (for up to 7 days at a time) to save its compute cost during an extended pause; Key Vault's small monthly cost applies regardless.

---

## Contact

For questions about the application code, configuration values, or environment variables, contact the CERA Tariff Tool project lead.

*Document version 2.2 — July 2026. v2.0 added Key Vault-based secret storage, Cloudflare custom-domain steps, and admin.html-specific access restriction, per IT review of v1.0. v2.1 replaces the deferred-SQLite pilot with PostgreSQL from day one (new Step 3), updates the cost summary and all subsequent step numbers accordingly, and points backup guidance at the Backup & Disaster Recovery section of `AZURE_DEPLOYMENT_BRIEF_v2.md`. v2.2 corrects Step 1's file list, which had fallen out of sync with the codebase — adds `config.py`, `schemas.py`, `serializers.py`, `importer.py`, `create_user.py`, `Logo_Transparent.png`, and (critically) `alembic.ini`/`migrations/`, since the app has run schema migrations via Alembic on every startup since 2026-07-23 and will not start without them.*
