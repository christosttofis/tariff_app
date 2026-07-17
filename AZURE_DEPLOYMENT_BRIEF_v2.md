# CERA Electricity Tariff Comparison Tool — Azure Deployment Brief (Revised)

**Prepared by:** Regulatory Affairs / CERA  
**Date:** July 2026  
**Purpose:** Recommendation for hosting the CERA Tariff Comparison Tool on Microsoft Azure  
**Revision note:** This version addresses questions raised on the June 2026 draft.

> **📝 PK (2026-07-17):** Removed the "SQLite pilot, upgrade to PostgreSQL later" plan that appeared throughout earlier drafts of this document — the application has since been migrated to PostgreSQL during development and no longer supports a SQLite pilot phase. Deploying straight to Azure Database for PostgreSQL Flexible Server avoids a redundant migration and gets automated backups in place from day one. Section 8 (formerly the SQLite→PostgreSQL migration guide) has been replaced with a Backup & Disaster Recovery section.

---

## 1. Background

The CERA Electricity Tariff Comparison Tool is a web application developed and currently running locally on a CERA workstation. It is ready for deployment. This document describes the recommended hosting approach — Microsoft Azure App Service — and the rationale for choosing it over an on-premises server deployment.

> **💬 EP (IT):** Through MS 365?

The application uses CERA's existing Microsoft 365 / Azure tenant for sending email notifications (OTP login codes, tariff approval/rejection notices, supplier invitations). All email is sent via the Microsoft Graph API (Mail.Send) using an App Registration already created within CERA's tenant. No separate email provider is introduced — the tool operates entirely within the Microsoft ecosystem already in use at CERA.

> **📝 PK:** It uses my personal CERA email for now with a Key — this needs to be switched to a shared/service mailbox before go-live.

A separate document covers the full technical overview of the application. This document focuses on Azure deployment architecture, security, and the actions required from IT.

---

## 2. Why Azure and not a CERA server

Both options are technically viable. Azure is recommended for the following reasons:

**Security maintenance is handled by Microsoft, not CERA IT**
Operating system security patches, platform vulnerability fixes, and infrastructure hardening are applied automatically by Microsoft. On Azure App Service, the underlying OS and Python runtime are maintained by Microsoft — CERA IT does not need to manually apply OS patches or monitor for platform vulnerabilities.

> **💬 EP (IT):** Who will update Python version, PostgreSQL etc?

*Regarding Python and runtime version updates:* Azure App Service allows the Python runtime version to be changed in a single configuration step in the Azure Portal (Settings → Configuration → General settings → Python version). Microsoft notifies customers when a runtime version approaches end-of-life. Updating is a one-click change and a redeploy — it does not require touching any application code. PostgreSQL (if adopted at full production) is similarly managed: Azure Database for PostgreSQL Flexible Server handles minor version patches automatically and provides an in-portal upgrade path for major versions.

**SSL/TLS certificates are managed automatically**
HTTPS certificates on Azure App Service are issued and renewed by Microsoft without any manual intervention. There is no risk of a missed renewal causing the site to become inaccessible.

**Encryption — data at rest and in transit**
- *In transit:* All traffic between users and the application is encrypted via TLS 1.2/1.3, enforced by Azure App Service. Communication between the application and Azure Key Vault, and between the application and the Microsoft Graph mail service, also takes place over TLS.
- *At rest:* Azure App Service storage and Azure Database for PostgreSQL both encrypt data at rest using AES-256 by default, with no additional configuration required.

**Secrets are stored securely in Azure Key Vault**
The application requires several sensitive credentials — a JWT signing key, and the Azure client secret used for email. On a self-managed server these would be stored in a plain text configuration file on disk. Azure Key Vault stores them encrypted, with access logging and no file on disk. The App Service accesses Key Vault using a Managed Identity — no credential is needed to retrieve a credential, eliminating a class of secret-exposure risk entirely.

**CERA is already in the Azure ecosystem**
The application already uses CERA's Azure tenant for email (Microsoft Graph Mail.Send, with admin consent already granted). Hosting on Azure App Service keeps everything within the same administrative boundary — same tenant, same IT governance, same Microsoft relationship.

**Data remains under CERA's control**
The application and its database are hosted in CERA's own Azure subscription, in an EU datacentre (West Europe — Netherlands, or North Europe — Ireland). Microsoft has no access to the data. This is fully compliant with GDPR and consistent with NIS2 requirements applicable to regulatory authorities.

**Compliance certifications are inherited**
Azure holds ISO/IEC 27001, SOC 2 Type II, and GDPR-ready certifications. A self-managed server would require CERA to independently certify and maintain its own infrastructure security posture.

**Reduced IT burden long-term**
There is no server to maintain, no OS to patch, no hardware to replace, and no process manager to configure. If traffic grows or the application is extended in future, scaling is a configuration change rather than a hardware procurement.

> **💬 EP (IT):** Encryption for data at rest or in transit?

*Addressed above under the "Encryption" heading in Section 2.*

---

## 3. Proposed architecture

The following Azure services are required:

| Service | Purpose | Estimated cost |
|---|---|---|
| Azure App Service — Basic B1 | Hosts and runs the Python web application | ~€13/month |
| Azure Key Vault | Secure storage for application secrets and credentials | ~€2/month |
| Azure Database for PostgreSQL Flexible Server | Production-grade database, including automated daily backups | ~€25/month |
| *(Azure App Registration)* | Already exists — used for email sending, no changes needed | No cost |

**Estimated total: ~€40/month, from the pilot onward.**

*Regarding PostgreSQL from day one:* the application already runs on PostgreSQL in development (it is no longer built against SQLite), so the pilot deploys directly to Azure Database for PostgreSQL Flexible Server rather than starting on a temporary SQLite database and migrating later. This avoids a redundant data migration and means the pilot gets Azure's automated backup and point-in-time restore coverage (see Section 8) from the first day it's live, rather than only after a later upgrade.

---

## 4. How the architecture works

### Architecture diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        END USERS                                │
│                                                                 │
│  👤 General Public    👤 CERA Admin     👤 Licensed Suppliers   │
│  customer.html        admin.html        supplier.html           │
│  Read-only, no login  Login required    Login required          │
└───────────────────────┬─────────────────────────────────────────┘
                        │ HTTPS request
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                        INTERNET                                 │
│                                                                 │
│  tariffs.cera.org.cy  ──(CNAME)──►  appname.azurewebsites.net  │
│                                                                 │
│  (DNS hosted on Cloudflare — see Section 4a)                    │
└───────────────────────┬─────────────────────────────────────────┘
                        │ Encrypted HTTPS
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│         MICROSOFT AZURE — CERA TENANT (EU Datacentre)           │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Azure App Service — Basic B1                            │   │
│  │                                                          │   │
│  │  SSL/TLS Certificate  ◄── Managed & auto-renewed         │   │
│  │         │                                                │   │
│  │         ▼                                                │   │
│  │  Uvicorn + FastAPI (Python)                              │   │
│  │  Business logic · REST API · JWT authentication          │   │
│  │  Auto-restart & always-on — built-in                     │   │
│  └────────┬───────────────┬──────────────────┬─────────────┘   │
│           │               │                  │                  │
│           ▼               ▼                  ▼                  │
│  ┌──────────────┐ ┌──────────────┐  ┌──────────────────────┐   │
│  │   STORAGE    │ │  KEY VAULT   │  │  AZURE ACTIVE DIR.   │   │
│  │              │ │              │  │  (CERA Tenant)       │   │
│  │ PostgreSQL   │ │ JWT key      │  │                      │   │
│  │ Flexible     │ │ Client secret│  │ App Registration     │   │
│  │ Server       │ │ Tenant ID    │  │ Mail.Send permission │   │
│  │ (auto backup)│ │ Client ID    │  │ (already granted)    │   │
│  │              │ │ DB creds     │  │        │             │   │
│  └──────────────┘ └──────────────┘  │   Azure Mail ────────┼──►│
│                                     └──────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                                    │ Email
                                                    ▼
                                    📧 Supplier inboxes
                                    📧 CERA admin inbox
```

### Step-by-step request flow

1. A user opens a browser and navigates to `tariffs.cera.org.cy`
2. DNS resolves the domain to the Azure App Service via a CNAME record

> **💬 EP (IT):** Domain hosting on Cloudflare — is it ok? How can it be deployed?
(see Section 4a for Cloudflare-specific steps)
3. Azure App Service handles the HTTPS connection using its automatically managed SSL certificate
4. The Python application processes the request — serving pages, handling logins, reading and writing tariff data
5. Secrets (credentials, signing keys) are read from Azure Key Vault — nothing sensitive is stored in configuration files
6. For email events (tariff submitted, approved, rejected, supplier invited) the application calls Azure Mail.Send using the existing CERA app registration
7. The encrypted response is returned to the user's browser

### 4a. DNS configuration when the domain is hosted on Cloudflare

If `cera.org.cy` DNS is managed via Cloudflare, the steps are slightly different from a standard DNS provider:

1. Log in to the Cloudflare dashboard and select the `cera.org.cy` zone
2. Add a **CNAME** record:
   - **Name:** `tariffs`
   - **Target:** `cera-tariff-tool.azurewebsites.net` (the Azure App Service default hostname)
   - **Proxy status:** set to **DNS only** (grey cloud, not orange) — Azure manages its own SSL certificate; Cloudflare proxying would interfere with Azure's certificate issuance
3. In the Azure Portal, open the App Service → **Custom domains** → **Add custom domain**
4. Enter `tariffs.cera.org.cy` and follow the domain verification steps (Azure will ask for a TXT record to be added in Cloudflare to confirm ownership)
5. Once the custom domain is verified, enable the **Managed certificate** — Azure will issue and auto-renew the HTTPS certificate for `tariffs.cera.org.cy`

This is a standard process. Azure has a built-in guide that shows the exact DNS records needed at each step.

---

## 5. Three user roles, three pages

| Role | Page | Access |
|---|---|---|
| General public | customer.html | No login required. Read-only. Compares tariffs and estimates consumption. |
| CERA admin staff | admin.html | Login required. Manages suppliers, approves or rejects tariff submissions, manages regulated charges. |

> **💬 EP (IT):** This page will be visible to the public?
>
> **📝 PK:** See note below.
| Licensed suppliers | supplier.html | Login required. Submits and edits their own tariffs. Receives email notifications on approval or rejection. |

**Regarding admin.html visibility:** The admin page is publicly reachable at its URL (like any web page), but it displays only a login form. Without valid credentials it shows nothing — no data, no controls, no information about the system. This is standard practice for web admin panels. If CERA prefers to restrict the URL entirely (so that only CERA office IP addresses can reach admin.html), this can be done via Azure App Service access restrictions at no additional cost.
> **📝 PK:** We should enable the IP restriction for admin.html before go-live.

User accounts are created by CERA admin staff through the admin panel. Suppliers receive an email invitation with a link to set their own password.

---

## 6. Security — questions answered

### Password recovery process
A "Forgot password" link is available on both the admin and supplier login screens. Clicking it sends a time-limited reset link (valid 1 hour) to the user's registered email address. The link is single-use — it cannot be reused after the password has been changed. There is no ability to recover or view an existing password; only a reset is possible.

### MFA / 2FA
The application implements two-factor authentication for all logins. After entering a correct email and password, the user receives a six-digit one-time code by email. The code expires after 10 minutes and is single-use. There is an option in the admin panel to temporarily disable OTP for specific accounts (e.g. during initial testing) — this can be re-enabled at any time.

> **📝 PK:** I can enable/disable 2FA per user for testing purposes from the admin panel.

### Automatic sign-out on inactivity
Both the admin panel and the supplier portal automatically sign a user out after 15 minutes with no activity (no clicks, key presses, or scrolling). A warning is shown 60 seconds before sign-out, with a "Stay signed in" option to continue the session; incidental activity while that warning is showing does not extend the session on its own. This limits the exposure window if a user leaves an authenticated session unattended, independent of the underlying 8-hour login token.

### What if credentials are stolen / invalid data is submitted
- **Stolen credentials:** Without the OTP code delivered to the registered email address, stolen credentials alone are not sufficient to log in. Account lockout applies after 3 consecutive failed attempts (locked for 3 hours). The account holder is notified by email when a lockout occurs.
- **Invalid or malicious data submissions:** All inputs are validated server-side. Supplier tariff submissions are held in a pending state and must be reviewed and explicitly approved by a CERA admin before they become visible to the public. No supplier-submitted data is published automatically.

### How user credentials are generated and what policy rules apply
- Accounts are created by CERA admin staff only — suppliers cannot self-register
- When an account is created, the supplier receives an email with a link to set their own password
- Passwords must be at least 8 characters (enforced server-side)
- Password policy for stronger requirements (length, complexity) can be tightened in the application configuration if CERA requires it

> **📝 PK:** To be added prior to deployment.

### How passwords are stored
Passwords are never stored in plain text. When a password is set or changed, it is processed through **bcrypt**, a one-way hashing algorithm specifically designed for password storage. bcrypt incorporates a random salt (preventing rainbow table attacks) and a work factor (making brute-force attacks computationally expensive). Even if the database file were obtained, passwords cannot be recovered from the stored hashes.

### Can users change their passwords
Yes. Both admin and supplier users can change their own password from within the application after logging in (Profile / Account settings area). There is currently no enforced periodic password change. If CERA's security policy requires periodic rotation, a password expiry mechanism can be added.

> **📝 PK:** To be added prior to deployment.

---

## 7. What IT needs to do

### One-time setup tasks

1. **Create an Azure App Service** (Basic B1 tier) within CERA's existing Azure subscription, with Python 3.12 runtime selected
2. **Create an Azure Key Vault** and grant the App Service access to it using a Managed Identity (no credentials required — Azure handles this internally)
3. **Store the following secrets in Key Vault:** JWT signing key (a random 64-character string), Azure Tenant ID, Azure Client ID, Azure Client Secret, sender email address, admin notification email address, application base URL
4. **Generate a new Azure client secret** for the existing app registration (the one used for tariff-tool email sending) in Azure Portal → App registrations → Certificates & secrets. Set expiry to 12 months. Store the new secret in Key Vault. The previous secret used for local development should be deleted.
5. **Add a DNS CNAME record** pointing `tariffs.cera.org.cy` to the App Service hostname — follow the Cloudflare-specific steps in Section 4a above
6. **Add the custom domain** in App Service settings and enable the managed SSL certificate
7. **Deploy the application** by uploading a ZIP file of the project folder via the Azure Portal or Azure CLI (full instructions are in the companion AZURE_DEPLOYMENT_CHECKLIST.md)
8. **Enable Always On** in App Service configuration to prevent the app from sleeping between requests
9. **Create the first admin account** via the Azure SSH console (instructions in AZURE_DEPLOYMENT_CHECKLIST.md Section 8)

### Ongoing (minimal)

- **Rotate the Azure client secret once per year** — a calendar reminder should be set. The process: generate a new secret in the App Registration, update the value in Key Vault, delete the old secret. The application picks up the new value automatically on next restart. Estimated time: 15 minutes.
- **Bug detection and fixing:** Application errors are logged in Azure App Service → Monitoring → Log stream. For the pilot period, the Regulatory Affairs team (who owns the application) should be the first point of contact for reported issues. IT's involvement would be limited to infrastructure-level problems (App Service unavailability, certificate issues, Key Vault access problems). Application-level bugs are handled by the development team.
- **Review Azure Security Centre recommendations** periodically (monthly or quarterly)
- **Database backup:** Azure Database for PostgreSQL Flexible Server provides automated daily backups with point-in-time restore for up to 35 days by default — no action required to enable it. IT should confirm the retention window is sufficient for CERA's audit requirements at setup time, and perform one test restore before go-live (see Section 8).

### Source code administration
The application source code is currently held on the CERA workstation where it was developed. For production, it is recommended that the source code be transferred to a CERA-controlled repository — either an Azure DevOps repository (already available within CERA's Microsoft tenant at no extra cost) or a private GitHub repository. This ensures that code changes are tracked, deployments are repeatable, and the application is not dependent on a single workstation. The Regulatory Affairs team and the development team should agree on ownership. IT can create the Azure DevOps repository if preferred.

---

## 8. Backup & disaster recovery

The application runs on Azure Database for PostgreSQL Flexible Server from day one (see Section 3), so backup coverage is in place from the pilot's first day live rather than only after a later database migration.

### What's automatic

- **Automated daily backups**, retained for **35 days** by default, with **point-in-time restore** to any moment within that window. This is a built-in feature of the Flexible Server tier — no configuration, script, or ongoing action is required to enable it.
- Backups are stored encrypted (AES-256) and, by default, in the same region as the database. **Geo-redundant backup storage** can be enabled at server creation time for an additional cost if cross-region disaster recovery is required — worth considering given CERA's regulatory role; confirm with IT/Regulatory Affairs whether this is needed before the server is provisioned, since it cannot be changed after the fact without recreating the server.

### What IT should still do

1. **At server creation:** decide on the 35-day default vs. a longer retention period, and whether geo-redundant backup storage is needed. Both are one-time choices made when the PostgreSQL Flexible Server is provisioned.
2. **Before go-live:** perform one test restore (Azure Portal → PostgreSQL Flexible Server → Backup and restore → Restore) into a temporary server, and confirm the application connects to it and the data looks correct. This is the only way to be confident the backup actually works, rather than assuming it does — see the note below.
3. **Ongoing:** no scheduled task is needed for the database itself. Azure Security Centre recommendations (already reviewed periodically per Section 7) will flag any backup-related configuration issues.

### Why the test restore matters

During development, a bug in the application's own "bulk publish" feature caused one specific table (the audit/changelog log) to be silently wiped — not a database failure, but the application itself overwriting its own data via a since-fixed code path. No backup existed for that environment at the time, so the history was not recoverable. The bug is fixed, but the incident is the reason a **verified, tested restore path** is called out explicitly here rather than just noting that "Azure handles backups automatically." Automatic backups only protect you if a restore has actually been proven to work.

### What's not covered by database backups

Azure's PostgreSQL backups protect the database only. They do **not** cover:
- Application source code — see the "Source code administration" recommendation in Section 7 (a version-controlled repository, not the database, is the source of truth for code)
- Uploaded tariff documents, if stored on the App Service filesystem rather than in the database — confirm with the development team where these live and whether they need separate backup coverage
- Azure Key Vault secrets — Key Vault has its own soft-delete/purge-protection settings, which are separate from database backups and should be enabled independently

---

## 9. Summary

| Requirement | How it is met |
|---|---|
| Public access over HTTPS | Azure App Service with managed SSL certificate |
| Secure credential storage | Azure Key Vault with Managed Identity access |
| Email notifications | Existing CERA Azure app registration (Mail.Send already granted) |
| Data sovereignty | CERA Azure tenant, EU datacentre |
| GDPR compliance | Azure EU hosting, inherited Microsoft certifications |
| Encryption at rest | AES-256 on PostgreSQL storage and Azure Files |
| Encryption in transit | TLS 1.2/1.3 enforced on all connections |
| Two-factor authentication | Email OTP on every login |
| Password security | bcrypt hashing — passwords never stored in plain text |
| Account protection | Lockout after 3 failed attempts, email notification |
| Unattended session protection | Auto sign-out after 15 min inactivity, with a 60s warning |
| Automatic security patching | Managed by Microsoft on App Service platform |
| Python/runtime updates | One-click version change in Azure Portal |
| High availability (pilot) | App Service Basic B1 (99.95% SLA) |
| Cloudflare DNS compatibility | CNAME + DNS-only mode — full instructions in Section 4a |
| Source code administration | Recommended: Azure DevOps repository within CERA tenant |
| Database backup | Automated daily, 35-day point-in-time restore — see Section 8 |
| Cost | ~€40/month, from the pilot onward |

---

## 10. Contact

For questions about the application code, configuration values, or deployment steps, contact the Regulatory Affairs / CERA project lead.

*Document version 2.2 — July 2026. v2.0 addressed IT review comments on v1.0; v2.1 added the idle-session auto sign-out security feature; v2.2 removes the SQLite pilot phase (the application now runs on PostgreSQL from day one) and replaces the SQLite→PostgreSQL migration guide with a Backup & Disaster Recovery section.*
