# CERA Tariff Comparison Tool — Administrator Manual

**Version:** 1.4  
**Date:** July 2026 (updated 2026-07-17: Suppliers, Load Profiles, Notices, and DAM Data now save immediately when you click their own Save button — see Section 12; the old Publish page was removed 2026-09-30)  
**Prepared by:** Cyprus Energy Regulatory Authority  

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Accessing the Admin Panel](#2-accessing-the-admin-panel)
3. [Navigation](#3-navigation)
4. [User Management](#4-user-management)
5. [Supplier Management](#5-supplier-management)
6. [Tariff Workflow](#6-tariff-workflow)
7. [Regulated Charges](#7-regulated-charges)
8. [Load Profiles](#8-load-profiles)
9. [Day-Ahead Market (DAM) Data](#9-day-ahead-market-dam-data)
10. [Notices & Disclaimers](#10-notices--disclaimers)
11. [Audit Log](#11-audit-log)
12. [Saving changes](#12-saving-changes)
13. [Email Notifications](#13-email-notifications)
14. [Security & Account Lockout](#14-security--account-lockout)
15. [Server Operations](#15-server-operations)
16. [Troubleshooting](#16-troubleshooting)

---

## 1. System Overview

The CERA Tariff Comparison Tool is a web application that enables electricity consumers in Cyprus to compare tariffs offered by licensed suppliers. It consists of three separate portals:

| Portal | URL | Audience |
|---|---|---|
| **Customer Calculator** | `/customer.html` | General public — read-only, no login required |
| **Admin Panel** | `/admin.html` | CERA staff — full management access |
| **Supplier Portal** | `/supplier.html` | Licensed suppliers — submit and manage their own tariffs |

### How it works

1. CERA admin creates supplier accounts and invites them by email
2. Suppliers log in, submit their tariffs, and upload supporting documents
3. Submitted tariffs appear as **pending** — they are not yet visible to the public
4. CERA admin reviews and either **approves** or **rejects** each tariff
5. Approved tariffs become immediately visible on the public customer calculator
6. CERA admin manages regulated charges, load profiles, and DAM data centrally

---

## 2. Accessing the Admin Panel

Open a browser and navigate to:
```
http://<server-address>/admin.html
```

You will be presented with a login overlay. Enter your CERA email address and password.

**Verification code (2FA):** After a correct password, most accounts are prompted for a 6-digit verification code sent to your registered email address. Enter the code to complete sign-in. The code is valid for 10 minutes; if you don't receive it, you can request a new one after 2 minutes using the resend link. **Entering the wrong code 3 times locks your account for 30 minutes** — see [Section 14.1](#141-lockout-policy).

**Session duration:** Your session stays active while you're actively using the panel — it automatically renews itself in the background, so you will not be logged out mid-task purely because time has passed. As a safety limit, a session always ends after **12 hours** even if continuously active, and you'll need to sign in again at that point regardless.

**Signing in with a different role in another browser tab:** The browser can only hold one active sign-in at a time — the same limitation as most sites (e.g. you can't be logged into two different Gmail accounts in two regular browser tabs at once). If you're signed into the Admin Panel and then sign into the Supplier Portal in another tab of the *same* browser (or vice versa), the tab you were using first will detect this and sign you out, asking you to sign in again. This is expected and protects against the two sessions interfering with each other. If you genuinely need both an admin and a supplier session open at the same time, use a private/incognito window (or a separate browser) for one of them.

**Automatic sign-out on inactivity:** If no activity (clicking, typing, or scrolling) is detected for 15 minutes, you will see a "Still there?" warning with a 60-second countdown. If you don't click **Stay signed in** before the countdown ends, you are automatically signed out and returned to the login screen. This applies to both the Admin Panel and the Supplier Portal, and protects the panel if a screen is left unattended. Any activity while the warning is showing does not extend the session on its own — only clicking **Stay signed in** does.

**Forgot your password?** Click the *Forgot password* link on the login screen. A reset link will be sent to your registered email address. The link is valid for 1 hour.

> **Note:** If you have been locked out after too many failed attempts and cannot access the login screen, see [Section 14](#14-security--account-lockout) for the emergency unlock procedure.

---

## 3. Navigation

The admin panel is divided into sections accessible from the left-hand navigation menu:

| Section | Icon | Purpose |
|---|---|---|
| **Tariffs** | 📋 | View, approve, reject, suspend all supplier tariffs |
| **Suppliers** | 🏢 | Manage licensed supplier records |
| **Users** | 👥 | Manage admin and supplier portal accounts |
| **Regulated** | ⚖️ | Set network, PSO and metering charges |
| **Profiles** | 📊 | Manage DSO load profiles used for calculations |
| **DAM Data** | 📈 | Day-ahead market prices: fetch from TSOC or upload, check, back up, restore |
| **Notices** | 📝 | Edit the notices and disclaimers shown on the calculator |
| **Audit Log** | 🕵️ | View full history of all tariff changes |

A **badge** on the Tariffs navigation item shows the number of tariffs currently awaiting review.

---

## 4. User Management

Navigate to **Users** in the left menu.

### 4.1 Inviting a supplier user

1. Click **+ Invite user**
2. Enter the supplier's email address
3. Select the supplier company they represent from the dropdown
4. Click **Send invitation**

The supplier receives an email with a secure link to set their password. The link is valid for **7 days**. If it expires, use the **Resend invitation** button.

> Only one user account per supplier is currently supported. Contact the development team if a supplier requires multiple logins.

### 4.2 Account status badges

Each user in the list displays one or more status badges:

| Badge | Meaning |
|---|---|
| 🟢 **Active** | Account is active — user can log in |
| 🔴 **Inactive** | Account has been deactivated — user cannot log in |
| 🟡 **🔒 Locked** | Account is temporarily locked due to failed login attempts |

### 4.3 Activating and deactivating accounts

- Click **Deactivate** to prevent a supplier from logging in (e.g. if their licence is suspended). Their tariffs remain in the system but they cannot make changes.
- Click **Activate** to restore access. This also clears any active lockout.

> Admin accounts cannot be deactivated through the panel. Contact the system administrator to deactivate an admin account.

### 4.4 Unlocking a locked supplier account

If a supplier's account shows the 🔒 **Locked** badge:

1. Click the **🔓 Unlock** button next to their name
2. Confirm the action in the prompt
3. The supplier can immediately attempt to log in again

> **Locked admin accounts** cannot be unlocked through the panel — see [Section 14.5](#145-unlocking-a-locked-admin-account) for the procedure.

### 4.5 Resending an invitation

If a supplier did not receive or has lost their invitation email, click **Resend invitation**. A new secure link is sent immediately. Previous links are invalidated.

### 4.6 Deleting a user

Click the red **Delete** button next to a supplier account to permanently remove it. This action cannot be undone. The supplier's tariffs remain in the system.

> Admin accounts cannot be deleted through the panel.

---

## 5. Supplier Management

Navigate to **Suppliers** in the left menu.

This section manages the registered details of each licensed supplier — name, licence number, address, contact email, telephone, and website. These details are displayed on the public calculator when a consumer expands a tariff card.

Every action in this section (add, edit, remove) saves straight to the server the moment you click its button — there is no separate publish step (see [Section 12](#12-saving-changes)).

### Adding a supplier

1. Type the new supplier's name into the field at the bottom of the supplier list
2. Click **+ Add**

This creates the supplier record immediately (name only). To fill in licence number, address, contact details, etc., use **Edit details** afterwards.

> A supplier record must exist before a user account can be created for that supplier, and before any tariffs can be submitted under that supplier's name.

### Editing a supplier

Click **✏ Edit details** next to any supplier to open the detail form, update the fields, and click **Save details**. Changes (including renaming the supplier) are saved immediately and are reflected right away on the public calculator — renaming a supplier also automatically updates every tariff currently assigned to them.

### Deleting a supplier

Click **Remove** next to a supplier. A supplier can only be deleted if they have no tariffs in the system — remove all their tariffs first, then delete the supplier record. Deletion takes effect immediately.

### Regulated supplier flag

A supplier can be marked **Regulated supplier** in the detail form. This changes how the Meter Data Management (MDM) charge is calculated for every tariff under that supplier — see [Section 7](#7-regulated-charges) for what the flag actually does to the calculation.

Because toggling it affects every tariff belonging to that supplier, changing the checkbox requires two separate confirmations: a pop-out box when you click the checkbox, and a second confirmation when you click **Save details**. Both must be confirmed for the change to take effect. Every confirmed change is recorded in the changelog (with a "Regulated supplier" entry, old/new value, who made the change, and when).

---

## 6. Tariff Workflow

Navigate to **Tariffs** in the left menu.

### 6.1 Tariff status values

| Status | Meaning | Visible to public? |
|---|---|---|
| **Pending** | Submitted by supplier, awaiting CERA review | No |
| **Approved** | Reviewed and approved by CERA | Yes |
| **Rejected** | Reviewed and not approved | No |
| **Suspended** | Previously approved, temporarily withdrawn | No |
| **Archived** | Was live at some point, then deleted by the supplier (see 6.9) | No |

### 6.2 Reviewing a pending tariff

Tariffs awaiting review are shown with an amber left border and a **🔍 Review** button.

1. Click **🔍 Review** to open the review modal
2. The modal shows the full tariff details
3. If the tariff was previously approved and has been edited, changed fields are highlighted showing the old and new values side by side
4. Supporting documents uploaded by the supplier can be downloaded from within the modal
5. Click **✓ Approve** to publish the tariff, or **✕ Reject** to decline it

When rejecting, you will be asked to provide a reason. The reason is sent to the supplier by email and recorded in the audit log.

### 6.3 Viewing an approved or rejected tariff

Click the **View** button next to any tariff to see its full details in a read-only modal. The Edit and Delete buttons are also available from within this modal.

### 6.4 Suspending a tariff

If an approved tariff needs to be temporarily removed from the public calculator (e.g. a supplier has requested a temporary withdrawal, or there is a compliance issue):

1. Find the tariff in the list
2. Click **Suspend**
3. Confirm the action

The tariff is immediately hidden from the public calculator. The supplier is not automatically notified — contact them separately if required.

### 6.5 Restoring a suspended tariff

Click **Restore** next to a suspended tariff to make it live again immediately.

### 6.6 Editing a tariff (admin)

Admins can edit any tariff directly without going through the supplier submission workflow. Click **View** then **Edit** inside the modal. Admin edits do not change the tariff status.

### 6.7 Deleting a tariff

Click **View** then **Delete** inside the modal. A confirmation prompt is shown. The tariff is deleted from the server immediately and the deletion is recorded in the Changelog. This action cannot be undone. (Before 2026-09-30 this button only removed the tariff from the page, and it reappeared on reload.)

### 6.8 Tariff documents

Suppliers upload supporting documents (PDF, Word) when submitting or resubmitting a tariff. A 📎 button appears on tariffs that have documents attached. Click it to open the documents list where each file can be downloaded individually.

### 6.9 Archived tariffs (deleted by a supplier)

Suppliers can delete their own tariffs at any time, without CERA approval. What happens depends on whether the tariff was **ever** public, not just its current status:

- **Any tariff that has ever been approved** is **archived**, not removed. This includes one that is currently pending or rejected because the supplier edited it after it went live. They are hidden from the public calculator immediately, but stay in the supplier's list and in the admin Tariffs list with a grey **▣ Archived by supplier** badge. The supplier can no longer edit it, delete it again, or upload documents to it.
- **Tariffs that were never approved** (a new submission still pending, a draft, or one rejected on first review) are removed entirely.

Both cases are recorded in the **Changelog** with the supplier's email. An archive shows as a status change to `archived`, and a removal shows as `Deleted`.

To put an archived tariff back online, click **▶ Restore** next to it (the same button used for suspended tariffs). To remove it permanently, use **View → Delete** as in 6.7.

### 6.10 Tariff input checks and limits

Every tariff is checked by the server before it is saved, whether it comes from a supplier or the admin editor. A tariff that fails a check is rejected with a message explaining which field is wrong. Nothing is stored.

These checks protect the public calculator. Before they existed, a single tariff containing malformed data (for example, a price entered as text) could stop the comparison working for **every** customer once approved.

| What | Allowed values |
|---|---|
| Energy prices: fixed rate, ToU peak/off-peak rates, Variable tier rates, Dynamic price floor | 0 to **€5/kWh** (adjustable, see below) |
| Dynamic adder, custom FPA | −€5 to +€5/kWh (same setting; these can legitimately be negative) |
| Standing charge, MDM, Variable tier fixed charge | 0 to **€1,000/month** (adjustable, see below) |
| Dynamic multiplier | above 0, up to 10 |
| ToU high-season months | 1–12 (0 = no high season) |
| ToU peak hours | 0–24 |
| Variable tiers | 1–20 tiers; each tier's limit higher than the previous; only the last tier may be open-ended |
| Discounts | at most 20 per tariff; energy or standing; above 0% and up to 100%; duration 1–120 months or blank (permanent); conditions up to 500 characters |
| Load profile | must be an existing profile |

Values must be real numbers: text, "NaN" and "Infinity" are refused.

**Adjusting the two limits.** The €5/kWh and €1,000/month limits are settings, not code. If a genuine tariff is ever refused because it exceeds them, raise them:

| Setting | Default | Meaning |
|---|---|---|
| `TARIFF_MAX_ENERGY_RATE` | `5` | Maximum €/kWh for any energy price (also the ± range for adder and custom FPA) |
| `TARIFF_MAX_MONTHLY_CHARGE` | `1000` | Maximum €/month for standing charge, MDM and tier fixed charges |

- **On the local server:** add or change the line in `tariff-api\.env`, e.g. `TARIFF_MAX_ENERGY_RATE=8`, then restart the server (15.3).
- **On Azure App Service:** App Service → **Settings → Environment variables** (Application settings) → add or edit the setting → **Apply**. The app restarts automatically.

Set them comfortably above any real tariff. They exist to catch typos and malformed data, not to regulate prices. The other limits in the table above are fixed in `tariff-api/schemas.py` and would need a code change.

---

## 7. Regulated Charges

Navigate to **Regulated** in the left menu.

Regulated charges are set by CERA and applied uniformly to all tariffs on the calculator. They are not set by suppliers.

| Field | Description |
|---|---|
| **Network charge — LV** | Distribution/transmission charge for low-voltage connections (€/kWh) |
| **Network charge — MV** | Distribution/transmission charge for medium-voltage connections (€/kWh) |
| **Network charge — HV** | Distribution/transmission charge for high-voltage connections (€/kWh) |
| **PSO** | Public Service Obligation levy (€/kWh) — not subject to VAT |
| **FPA — LV/MV/HV** | Fuel Price Adjustment per voltage level (€/kWh) |
| **MDM** | Meter Data Management charge (€ per invoice) |

Click **Save** after making any changes. Changes are reflected immediately on the public calculator.

> **MDM is the one exception to "not set by suppliers."** Whether a tariff uses this regulated rate depends entirely on whether its supplier is flagged **Regulated** (Suppliers page):
>
> - **Regulated supplier** (e.g. EAC) — every one of their tariffs always uses this global rate. There is no per-tariff override; the tariff editor's MDM field is locked and shows this value.
> - **Non-regulated supplier** — this global rate is never used. Each of their tariffs has its own freely-editable MDM value, and there is no option to opt into the regulated rate instead.
>
> MDM is charged **once per invoice, not once a month** — each tariff also has its own **Invoicing frequency** (Monthly or Bimonthly, set in the tariff editor), which determines how many times a year the charge is actually applied (12 for monthly, 6 for bimonthly). Two tariffs with the same MDM value but different invoicing frequency will show different annual totals.

### Checks before saving

To catch typing mistakes (e.g. 0.4735 entered instead of 0.04735):

- **Grid usage must fall with voltage: LV > MV > HV.** If it doesn't, Save is refused and the out-of-order field is highlighted. The server enforces the same rule.
- **Every changed value is compared with the previous one.** Before saving, a window lists each change, e.g. "The LV grid usage value is now 12.5% higher than the previous one (0.0393 → 0.0442).", and asks **Is this correct?** **Confirm** saves; **Cancel** saves nothing and keeps your entries on the form so you can correct them.
- **FPA rates out of the usual LV > MV > HV order** are also listed in that window. This is a warning only, not a refusal, because a negative FPA reverses the order.

---

## 8. Load Profiles

Navigate to **Profiles** in the left menu.

Load profiles define how a consumer's annual electricity consumption is distributed across months, working days, and non-working days. They are used by the calculator to produce accurate cost estimates for Time-of-Use and Dynamic tariffs.

Profiles are imported from EAC CSV exports. Each profile contains 12 months of half-hourly load shapes for working days and non-working days.

Every action in this section (add/overwrite, rename, delete) saves straight to the server the moment you click its button — there is no separate publish step.

### Uploading a profile

1. Enter a **Profile name** (and optional description)
2. Paste the DSO CSV export into the text box — see the expected format shown above the form
3. Click **⚡ Parse & save profile**

Parsing and saving happen in one step: the file is validated and, if valid, saved immediately. The status message underneath confirms how many time slots and months were covered. If you reuse the name of an existing profile, you'll be asked to confirm overwriting it — the existing profile's underlying record is updated in place, so tariffs already assigned to it stay correctly assigned.

#### Checks before saving

Profiles drive every tariff's price in the public calculator, and a single bad value would stop the calculator showing any results to customers. So the whole CSV is checked before anything is saved.

**Refused:** the profile is not saved. Every problem is listed with its line number, column and time, up to 10 and then "…and N more". For example:

> Profile not saved: 3 problems found:
> • Line 31, Mar_WD at 14:30: "abc" is not a number
> • Line 31, Mar_NWD at 14:30: empty cell
> • Line 32, Jul_WD at 15:00: negative value -0.2

The problems that cause a refusal are:
- a cell that is empty, not a number, or negative;
- a time row that appears twice ("Time 09:00 appears twice (lines 20 and 51)");
- a missing time row ("Missing time rows: 14:30");
- a time that isn't on the half hour (e.g. `14:15`);
- two columns for the same month and day type.

Rows without a time, such as a "Total" line, are skipped as before. `24:00` is accepted as `00:00`.

**Warned:** you're asked "Save anyway?", and **Cancel** saves nothing:
- a month or day type with no column or no usage at all ("No data for: March non-working days"). If saved, it shows as partial coverage;
- values over **10× the profile's typical value**, which usually means a typo or a different unit ("July working days at 12:00: 4.2").

The server repeats the essential checks as a safety net: exactly 12 months, 48 working-day and 48 non-working-day values per month, all real non-negative numbers. If it refuses, the message names the month, day type and time (e.g. "March, working days, 03:00: Input should be a valid number"). The previously saved version of a profile is never changed by a refused save.

### Renaming a profile

Click **✏ Rename** next to a profile in the **Saved profiles** list, enter the new name, and confirm. Saved immediately.

### Deleting a profile

Click **Delete** next to a profile. A profile can only be deleted if no tariffs are currently assigned to it — reassign affected tariffs to a different profile first. Deletion takes effect immediately.

---

## 9. Day-Ahead Market (DAM) Data

Navigate to **DAM Data** in the left menu.

DAM data is required to calculate costs for **Dynamic (market-linked)** tariffs. It provides day-ahead electricity market prices used to estimate what a consumer would pay under a dynamic pricing contract.

Two levels of data are derived from the half-hourly prices:

| Type | Granularity | Used for |
|---|---|---|
| **Monthly averages** | One average price per month (€/kWh) | Annual cost estimate for dynamic tariffs |
| **Half-hourly slot data** | 48 slots × 12 months | More accurate profile-weighted calculation |

Both are computed automatically from the half-hourly prices. There is no separate manual entry for monthly averages.

**Keep the whole history.** The calculator prices each future half-hour using the same date one or two years earlier, so older prices are still used. The stored history starts on 1 October 2025, the first day TSOC publishes. Never replace it with a file that holds only recent months (see 9.3).

### 9.1 Keeping the prices up to date

There are two ways to add prices:

- **🌐 Fetch from TSOC** (normal way): adds the missing days automatically. See 9.2.
- **CSV upload**: for days TSOC cannot provide, corrections, or long gaps. See 9.3.

TSOC publishes the next day's prices in the afternoon, Cyprus time (normally after about 14:00). Fetching once a week, or whenever the dashboard shows a warning (9.8), is enough.

### 9.2 Fetch from TSOC

1. Click **🌐 Fetch from TSOC**. It can take up to a minute.
2. The tool asks TSOC for every day after the last stored day, up to tomorrow. If tomorrow is not published yet, it is simply left out.
3. You get a **preview**. The status line says how many half-hours were fetched for which days, and the report below lists each day. Click a day in the report to see its 48 prices (see 9.4). New days have a blue outline in the calendar.
4. Check the new days, then click **💾 Save DAM data**. Nothing reaches the calculator until you save.

If the data on screen has unsaved changes, Fetch asks first, because it starts again from the saved data.

**If the fetch is cancelled.** Any error or missing data cancels the whole fetch. A red panel lists the reasons, and nothing is changed. What to do:

| Reason shown | What to do |
|---|---|
| TSOC/Cloudflare refused the request, TSOC did not answer, or TSOC is too slow | Try again later. If it keeps happening, upload a CSV instead. |
| A day has fewer than 48 half-hours (e.g. "46 of 48", often the clock-change day, the last Sunday of March) | Fill that day by CSV: **⬇ Download CSV**, add the missing half-hours, upload it (9.3). The next fetch continues after it. |
| More than 31 days are missing | Fill the gap by CSV first, then fetch. |
| No prices from TSOC for a day before tomorrow | TSOC has not published it. Try again later. |
| Wrong day returned, conflicting prices, unreadable row, or a price outside 0–4000 €/MWh | Try again later. If it persists, check the prices on TSOC's website and enter them by CSV. |
| The page layout may have changed | TSOC changed its website. Use CSV upload and report it, as the fetch needs updating. |

Every fetch, including cancelled ones, is recorded in the change log (9.7).

### 9.3 Uploading a CSV

Format: one price per line, `date time,price` (comma or semicolon), half-hourly or hourly, Cyprus local time, for example:

```
2026-05-22 00:00,237.5
2026-05-22 00:30,237.5
```

1. Set the **Data year** and **Price unit** (€/MWh or €/kWh)
2. Drag & drop one or more CSV files onto the drop zone (or click it to browse)
3. Check the preview (9.4), then click **💾 Save DAM data**

Dropping a file only builds a preview in your browser. Nothing is saved to the server until you click **💾 Save DAM data**. Click **Clear** to discard it.

**An upload replaces all stored prices**, so the file must contain the whole history, not just the new days. The safe way to correct or add prices:

1. Click **⬇ Download CSV (re-uploadable)**. It gives everything currently stored, in €/MWh.
2. Correct or add lines in a spreadsheet or text editor and save it as CSV.
3. Upload it with **Price unit: €/MWh** and save.

Safeguards:

- If the file would **remove days** that are already stored, Save asks you to confirm and shows which dates would go. Click **Cancel** unless that is really intended.
- The server checks the data before saving: 12 months, 48 half-hours per day, real dates, and prices between −1 and 10 €/kWh. A €/MWh file uploaded with **€/kWh** selected gives prices around 100 €/kWh and is refused with "was the right price unit selected?". Select €/MWh and try again.
- If a wrong file was saved anyway, restore the previous version (9.6).

> The **Data year** is recorded and displayed to consumers on the calculator.

### 9.4 Checking the prices

- **Data coverage** calendar: each month is green (complete), amber (partly filled) or grey (no data). Click a month to see its days, then click a day to see its **48 half-hourly prices** in €/MWh, with the day's minimum, maximum and average. Missing half-hours are shown in red.
- Days and months with a **blue outline are new and not saved yet**, e.g. after a fetch or a file upload. Check them before saving.
- **Price explorer**: choose a month with the tabs and step through it week by week on the chart (blue = working day, purple = weekend or holiday). A month tab holds that month for every year stored (October has both 2025 and 2026); to look at one particular day, use the calendar.
- **Monthly averages** card: the average price per month.

### 9.5 Downloading the prices

- **⬇ Download CSV (re-uploadable)**: every price currently on screen, in €/MWh, in the upload format. If you have fetched or loaded something but not saved it, the download includes it.
- The buttons on the **Monthly averages** card (daily prices, slot averages, monthly averages) are for analysis in a spreadsheet. They are in €/kWh and cannot be uploaded again.
- An older saved version can be downloaded from the versions list (9.6).

### 9.6 Saved versions (backups) and restoring

Every save is kept as a **version**: the latest is marked **live**, older ones are backups. The list shows when each was saved, by whom, how (CSV upload, TSOC fetch, Restored), the date range and the number of half-hours.

- **⬇ CSV**: downloads that version in the upload format.
- **↩ Restore**: makes that version live again, after a confirmation. The current data is kept as a version too, so a restore can itself be undone.

Versions are never deleted.

### 9.7 Change log

Below the versions, the **Change log** lists every DAM event with the time and the person:

- Saved (CSV upload) / Saved (TSOC fetch), with the days added and removed
- Restored version
- Fetched (not saved yet), and **Fetch cancelled** with every reason (in red)
- Reminder emailed (see 9.8)

### 9.8 Dashboard warning and email reminder

The **Dashboard** has a **DAM prices** card showing the last date with prices, how many days ago that was, the last change (when, by whom, how) and the number of days stored.

When the newest price is **more than 15 days old**:

- the card shows it in red, a line appears under "needs attention" with a button to open the DAM page, and the **DAM Data** menu item gets a red **!**;
- the admin email address (`TARIFF_ADMIN_EMAIL`) receives a reminder, repeated weekly while the prices stay old.

Saving newer prices clears the warning.

### 9.9 Switching off or removing "Fetch from TSOC"

If fetching DAM prices from TSOC stops working (for example, TSOC blocks the server) or is no longer wanted, manual CSV upload keeps working either way.

- **To switch it off** (no code change): set `TARIFF_TSOC_FETCH=off` in `tariff-api/.env` (or in the Azure app settings) and restart the server. The **🌐 Fetch from TSOC** button disappears. Set it back to `on` to restore it.
- **To remove the fetch for good**, run `git revert 6c041bc`. This removes only the TSOC fetch; backups and restore, the change log, the data checks, the dashboard card and the 15-day reminder stay.

---

## 10. Notices & Disclaimers

Navigate to **Notices** in the left menu.

This section allows you to edit the text shown in the **Notices & Disclaimers** popup on the public calculator. Content is maintained in both English and Greek.

| Tab | Purpose |
|---|---|
| **Notices / Assumptions** | Explains how costs are calculated, what assumptions are made |
| **Disclaimers** | Legal disclaimer — the calculator provides indicative estimates only |
| **Vulnerable consumer** | Explains who qualifies for a social/vulnerable consumer tariff |

Content is entered as HTML, allowing basic formatting (headings, paragraphs, bullet lists).

Click **💾 Save notices** at the bottom of the page after making any changes — this saves and publishes all the notices content in one step; nothing is written to the server until you click it.

### Sample invoice toggle

At the top of the Notices page is a **"Sample invoice"** switch: **Enable sample invoice on customer calculator**. When on, customers see a "📄 Sample invoice" button on each tariff card that opens a bill-styled cost breakdown (based on the customer's own inputs) with explanations for each charge. This switch saves immediately when clicked — no separate Save button. It defaults to **off**. If the feature ever looks wrong or confusing for a particular tariff type, turn it off here — this disables it site-wide immediately, no code changes needed.

---

## 11. Audit Log

Navigate to **Audit Log** in the left menu.

The audit log records every create, edit, and delete action performed on tariffs, showing:

- The action taken (created / updated / deleted)
- The tariff name and supplier
- The date and time
- For edits: every field that changed, showing the old value and the new value side by side

The log is read-only and cannot be modified or deleted. Use it to track the history of any tariff and to investigate disputes with suppliers.

Changes to DAM prices are recorded separately, in the **Change log** on the DAM Data page (see 9.7).

---

## 12. Saving changes

There is no Publish step. Every section of the admin panel saves itself when you click its own button, and the change is live on the customer calculator straight away:

| Section | Button that saves it |
|---|---|
| Suppliers | **+ Add**, **Save details**, **Remove** |
| Load profiles | **⚡ Parse & save profile** (add or overwrite), **✏ Rename**, **Delete** |
| Tariffs | **Save** in the tariff editor, **Approve** / **Reject** / **Suspend** / **Restore**, **View → Delete** |
| Regulated charges | **💾 Save regulated charges** |
| DAM price data | **💾 Save DAM data** (also after **🌐 Fetch from TSOC**, which is only a preview), **↩ Restore** |
| Notices | **💾 Save notices** |
| Sample invoice | its on/off checkbox (saves as soon as you tick or untick it) |

A green "Saved ✓" (or the updated list) confirms the change reached the server. If you see "Save failed", nothing was changed. Fix the problem shown and save again.

**Mistakes in the tariff editor are highlighted field by field.** If a value is missing or out of range, Save doesn't send anything. Each problem field gets a red outline and a message underneath, e.g. "Please provide the tariff name." or "This cannot be more than 1000.". The status line says how many fields need correcting. Typing in a field clears its highlight. The supplier portal's tariff form works the same way. Number boxes accept only plain numbers: `e`, `+` and `-` are ignored, except in the boxes where a negative value is valid (custom FPA, the Dynamic adder, the regulated FPA rates).

**Unsaved-changes warnings.** If you edit a form and haven't clicked its Save button yet:

- Its menu item shows a yellow **●**. Your edits stay in the form, but they are **not live** until you save.
- Leaving that page asks first. **Cancel** takes you back to finish and save. **OK** moves on and keeps the edits in the form, still marked ●.
- Closing the tariff editor or the supplier-details window asks before throwing away your edits.
- **Sign out** asks first. Automatic sign-outs (idle timeout, expired session) can't wait for an answer, so save before stepping away.
- Reloading or closing the browser tab shows the browser's own "Leave site?" prompt.

The supplier portal has the same protection for its tariff form.

> **History:** the admin panel used to have a **Publish** page with a **💾 Save & publish** button. It dated from the early version of the tool, when all data lived in the browser and had to be pushed out in one go for the customer tab to see it. After every section gained its own save, the button became redundant and dangerous: it replaced all suppliers, profiles and tariffs with the browser's copy, and set every tariff to Approved. It was removed on 2026-09-30.

---

## 13. Email Notifications

The system automatically sends email notifications for the following events:

| Event | Recipient |
|---|---|
| New tariff submitted by supplier | CERA admin |
| Tariff resubmitted after editing | CERA admin |
| Tariff approved | Supplier |
| Tariff rejected (with reason) | Supplier |
| New user invitation | Supplier (invite link, valid 7 days) |
| Password reset requested | Requester (reset link, valid 1 hour) |
| Account locked after failed logins | Affected user |
| DAM prices more than 15 days old (weekly while they stay old) | CERA admin |

Emails are sent via Microsoft Azure (Mail.Send) using CERA's existing Azure tenant. They are sent from the address configured in the server's `.env` file (`TARIFF_EMAIL_FROM`).

> Emails are sent in the background and do not affect the response time of the panel. If email delivery fails, an error is recorded in the server log but the action (approval, rejection, etc.) still completes.

---

## 14. Security & Account Lockout

### 14.1 Lockout policy

Wrong passwords are counted per account **and** per network address, so someone who only knows a user's email can't lock the real person out:

- **5 wrong passwords from one address:** that address can't try that account again for **15 minutes**. The real user, signing in from their own office or home, is not affected. Signing in successfully from that address clears its count.
- **30 wrong passwords from all addresses within an hour** (many computers guessing at once): the whole account is locked for **30 minutes**.
- **3 wrong 6-digit verification codes** at the 2FA step (see [Section 2](#2-accessing-the-admin-panel)): the account is locked for **30 minutes**. Only someone with the right password reaches this step, so it's a sign the password is known. Signing in again with the password doesn't reset the count; only a completed sign-in or an unlock does.

The sign-in page shows the same message for all three ("Too many failed sign-in attempts…"), so it doesn't reveal which applied or whether an account exists.

When the whole account is locked:
- The affected user receives an email notification immediately
- The email advises them to try again later or contact their CERA administrator
- A 🔒 Locked badge appears next to the account in the Users panel

An admin **Unlock** (or **Activate**) clears all of these at once, including blocked addresses. In the Login Activity log, blocked attempts appear as `address_blocked` (one address) or `locked` (whole account).

### 14.2 Idle session timeout

Both the Admin Panel and Supplier Portal automatically sign a user out after **15 minutes of inactivity** (no clicks, key presses, or scrolling). A warning is shown 1 minute before sign-out, with a **Stay signed in** button to continue the session. This reduces the risk of an unattended, logged-in screen being used by someone else — e.g. an admin stepping away from their desk without locking their computer.

### 14.3 Protection against accidental overload

The server automatically limits how many requests it will accept from a single computer in a short period (60 per minute). This is not meant to stop a person — it protects the system if a browser tab gets stuck retrying a failed action in a loop, or if a script is accidentally run that hammers the server with requests. If this limit is ever hit, the affected action will briefly show an error; simply wait a few seconds and try again. Repeated hits on the sign-in page specifically are also recorded in the Login Activity log (see [Section 11](#11-audit-log)) so they can be distinguished from genuine failed sign-in attempts.

### 14.4 Unlocking a locked supplier account

See [Section 4.4](#44-unlocking-a-locked-supplier-account).

### 14.5 Unlocking a locked admin account

Because a locked admin cannot access the admin panel, the unlock must be performed directly on the server.

**Steps:**

1. Log onto the server via RDP (Windows) or SSH (Linux)
2. Open a terminal / command prompt
3. Navigate to the `tariff-api` folder:
```
cd C:\path\to\tariff-backend\tariff-api
```
4. Run:
```
python unlock_user.py --email yourname@cera.org.cy
```
5. You should see:
```
[OK] Account 'yourname@cera.org.cy' has been unlocked.
```
6. Return to the browser and log in normally

### 14.6 If you have forgotten your password

Use the **Forgot password** link on the admin login screen. A reset link will be sent to your registered CERA email address. The link is valid for 1 hour.

If you cannot receive the reset email, ask IT to reset your password using the command line tool:
```
python create_user.py --email yourname@cera.org.cy --role admin
```
This will prompt for a new password.

### 14.7 Creating a new admin account

Admin accounts cannot be created through the admin panel. They must be created on the server by IT.

**Steps:**

1. Open a terminal (Command Prompt or PowerShell) on the server
2. Navigate to the `tariff-api` folder:
   ```
   cd "C:\path\to\Tariff backend\tariff-api"
   ```
3. Run the following command, replacing the email with the new admin's address:
   ```
   python create_user.py --email newadmin@cera.org.cy --role admin
   ```
4. When prompted, type a password for the new account (minimum 8 characters — it will not be visible as you type)
5. Press **Enter** — you should see:
   ```
   Created: newadmin@cera.org.cy (admin)
   ```
6. The new admin can now log in immediately at `/admin.html` using the email and password you just set

> The new admin will be asked to change their password via the **My Account** menu after first login, or they can use the **Forgot password** link on the login screen to set their own password.

### 14.8 Removing an admin account

Admin accounts cannot be removed through the admin panel. This must be done on the server by IT.

**Option A — Deactivate (recommended)**

Deactivation prevents the admin from logging in but keeps their account in the system. It can be reversed if needed.

1. Open a terminal on the server and navigate to the `tariff-api` folder:
   ```
   cd "C:\path\to\Tariff backend\tariff-api"
   ```
2. Run:
   ```
   python create_user.py --email admin@cera.org.cy --deactivate
   ```
3. You should see:
   ```
   User admin@cera.org.cy deactivated.
   ```
4. The account is now blocked immediately — no restart required

To **re-activate** the account later, run the create command again for the same email and confirm when prompted to update the existing account.

**Option B — Permanent deletion**

If you need to fully remove the account from the database:

1. Open a terminal on the server and navigate to the `tariff-api` folder
2. Run:
   ```
   python -c "from database import SessionLocal; import models; db=SessionLocal(); u=db.query(models.User).filter(models.User.email=='admin@cera.org.cy').first(); db.delete(u); db.commit(); print('Deleted.')"
   ```
3. Replace `admin@cera.org.cy` with the actual email address

> **Note:** Permanent deletion cannot be undone. Deactivation (Option A) is the safer choice in most cases.

---

## 15. Server Operations

### 14.9 Network restriction (admin access only from the CERA office / VPN)

On the live site, admin accounts only work from the CERA office network and the CERA VPN. From anywhere else, the admin page, admin sign-in and every admin action show only **"Website unavailable"**. The page doesn't say why, on purpose. Customers and suppliers are not affected.

- **Working from home:** connect to the CERA VPN first, then open the admin page.
- **If the VPN drops while you're working**, your next click shows "Website unavailable". Unsaved edits are lost. Reconnect and sign in again.
- **Every blocked attempt** appears in **Login activity** with the reason `network_blocked` and the address it came from.

**Changing the allowed addresses.** The list is the setting `TARIFF_ADMIN_ALLOWED_NETWORKS`: comma-separated addresses or ranges, e.g. `203.0.113.10/32,198.51.100.0/28`. CERA IT provides the office and VPN addresses and should tell you if they change.
- **On Azure:** App Service → **Settings → Environment variables** → edit `TARIFF_ADMIN_ALLOWED_NETWORKS` → **Apply**. The app restarts automatically. A typo in the list stops the app from starting; check **Log stream** and correct it.
- **Emergency (e.g. the VPN is down and an admin task can't wait):** clear the value and Apply. The restriction is then off (anyone with an admin password and 2FA code can sign in from anywhere). Put the value back as soon as possible.
- **Locally:** the setting is normally not set, so there is no restriction on a development PC. To try it, add `TARIFF_ADMIN_ALLOWED_NETWORKS=127.0.0.1/32` to `tariff-api\.env` and restart (15.3). That PC is then "inside"; anyone opening the app through its network address is "outside".

### 15.1 Starting the server

Double-click **`start.bat`** in the project root folder. This will:
- Check that Python is installed
- Create a virtual environment if one does not exist
- Install or update all required dependencies
- Start the web server on port 8000

The server window must remain open while the application is in use. Closing the window stops the server.

> On a production server, the application runs as a background service managed by IT and starts automatically. The `start.bat` file is for local use only.

### 15.2 Stopping the server

Press **Ctrl+C** in the server window, or simply close the window.

### 15.3 After making code changes

The server does **not** reload automatically. After any code changes:

1. Press Ctrl+C to stop the server
2. Double-click `start.bat` to restart it

### 15.4 Checking the server is running

Open a browser and navigate to:
```
http://localhost:8000/customer.html
```
If the page loads, the server is running. If not, start it using `start.bat`.

### 15.5 Restoring the database from a backup

**Local development environment**

Daily backups are taken automatically (see Section 16, "The database is unreachable or data appears to be missing") and stored in:
```
C:\Users\<you>\OneDrive - Cyprus Energy Regulatory Authority\Tariff-App-DB-Backups\
```
with `daily\` (last 14 days) and `weekly\` (last 8 weeks) subfolders, each containing timestamped `.dump` files, plus a `backup.log` showing the history of each run.

To restore one:

1. **Stop the server first** ([Section 15.2](#152-stopping-the-server)) so nothing is writing to the database mid-restore.
2. Open PowerShell and find the backup you want, e.g.:
   ```powershell
   dir "C:\Users\<you>\OneDrive - Cyprus Energy Regulatory Authority\Tariff-App-DB-Backups\daily"
   ```
3. **Take a fresh backup of the current state first**, even if it's the thing you're trying to fix — this is your undo button if you pick the wrong backup file:
   ```powershell
   powershell -ExecutionPolicy Bypass -File "C:\Projects\Tariff app\tariff-api\scripts\backup_db.ps1"
   ```
4. **Restore over the live database:**
   ```powershell
   & "C:\Program Files\PostgreSQL\17\bin\pg_restore.exe" -h 127.0.0.1 -p 5433 -U postgres -d tariff_app --clean --if-exists "<path to the .dump file you chose>"
   ```
   `--clean --if-exists` drops and recreates each table before restoring it, so this fully replaces the current contents of `tariff_app` with the backup's contents. (Credentials are read automatically from `%APPDATA%\postgresql\pgpass.conf` — no password prompt.)
5. **Restart the server** ([Section 15.1](#151-starting-the-server)) and confirm the data looks correct — check the Tariffs list, Suppliers list, and Changelog page in the admin panel.

**To inspect a backup without touching the live database at all** (e.g. to compare it against current data before deciding to restore):
```powershell
& "C:\Program Files\PostgreSQL\17\bin\createdb.exe" -h 127.0.0.1 -p 5433 -U postgres tariff_app_test
& "C:\Program Files\PostgreSQL\17\bin\pg_restore.exe" -h 127.0.0.1 -p 5433 -U postgres -d tariff_app_test "<path to the .dump file>"
```
This restores into a separate, throwaway database (`tariff_app_test`) rather than `tariff_app`. Point a temporary `DATABASE_URL` at it to browse the data, or query it directly with `psql`. Drop it when done:
```powershell
& "C:\Program Files\PostgreSQL\17\bin\dropdb.exe" -h 127.0.0.1 -p 5433 -U postgres tariff_app_test
```

**On Azure (production)** — once the application has been migrated to Azure Database for PostgreSQL Flexible Server (`AZURE_DEPLOYMENT_BRIEF_v2.md`), restores are done through the Azure Portal — **PostgreSQL Flexible Server → Backup and restore → Restore** — rather than the command-line steps above, and always restore to a **new** server rather than overwriting the live one. See the Backup & Disaster Recovery section (Section 8) of that document.

---

## 16. Troubleshooting

### The login page shows but login fails
- Check your email and password are correct
- Check your account has not been locked (see Section 14)
- Check your account is active — ask another admin to verify in the Users panel
- **A CERA admin account cannot sign into the Supplier Portal, and a supplier account cannot sign into the Admin Panel.** Attempting either shows the same generic "Invalid email or password" message as any other failed sign-in (by design, so the message doesn't reveal anything about the account) — this doesn't mean your credentials are wrong, just that you're on the wrong page. Go to the correct portal for your account type.
- If you were previously signed in and suddenly find yourself back at the login screen with the message "Your session was terminated", see the note on signing in with a different role in another tab, in [Section 2](#2-accessing-the-admin-panel).

### A supplier says they did not receive their invitation email
- Go to Users → find the supplier → click **Resend invitation**
- Ask the supplier to check their spam/junk folder
- Verify the email address is correct

### A tariff I approved is not showing on the calculator
- Check the tariff status is **Approved** (not Suspended)
- Check the tariff's voltage and contract type match what the customer is filtering for
- Check the tariff has a valid profile assigned

### The server window shows errors on startup
- Check that Python 3.12 or higher is installed
- If first-time dependency installation fails with an SSL/certificate error (possible on a corporate network that inspects HTTPS traffic), contact IT. `start.bat` no longer skips certificate checks (`--trusted-host` was removed on 2026-10-09; installation from this PC worked without it).
- `start.bat` starts the server for this PC only (`127.0.0.1`); other computers on the network cannot open it.
- Check that the `.env` file exists inside the `tariff-api/` folder and contains the required values

### An admin sees "Website unavailable"

The admin is outside the allowed networks (14.9). Check that the VPN is connected; with split-tunnel VPNs, CERA IT must route the site's address through the VPN. In **Login activity**, look for `network_blocked` entries: the IP shown is the address the site saw. If it's a genuine CERA address that's missing from the list, ask IT to confirm it and add it to `TARIFF_ADMIN_ALLOWED_NETWORKS`.

### Emails are not being sent
- Check the Azure client secret in the `.env` file has not expired (secrets are set to expire after 12 months)
- Check the server log for email error messages
- Verify that the `TARIFF_EMAIL_FROM` address has the Mail.Send permission in the Azure portal

### The database is unreachable or data appears to be missing
- The application stores its data in a PostgreSQL database, configured via the `DATABASE_URL` value in `tariff-api/.env` — not in a local file. If the panel fails to load data at all, first confirm the PostgreSQL service is running and reachable at the configured host/port.
- If specific data (e.g. tariffs, suppliers, or the audit log) appears to have disappeared while the server itself is running fine, this points to a database-level change, not a missing file — do not assume it will reappear on its own.
- **Automated backups (local dev environment):** a scheduled Windows Task (`TariffApp-DB-Backup`, runs daily at 10:00) takes a `pg_dump` of `tariff_app` and writes it to `OneDrive - Cyprus Energy Regulatory Authority\Tariff-App-DB-Backups\` (14 days of daily backups, 8 weeks of weekly backups, pruned automatically). This is temporary insurance for the current local development environment only — it is superseded once the application moves to Azure Database for PostgreSQL Flexible Server, which provides automated backups natively (see `AZURE_DEPLOYMENT_BRIEF_v2.md`, Section 8). The task can be inspected or run manually via Task Scheduler, or by running `tariff-api\scripts\backup_db.ps1` directly. Check `Tariff-App-DB-Backups\backup.log` if a backup appears to be missing.

---

*This document covers version 1.4 of the CERA Tariff Comparison Tool. For technical support or to report issues, contact the system administrator.*
