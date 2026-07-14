# CERA Tariff Comparison Tool — Administrator Manual

**Version:** 1.1  
**Date:** July 2026  
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
12. [Publishing](#12-publishing)
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

**Session duration:** Sessions expire after 8 hours. You will be asked to log in again after this time.

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
| **DAM Data** | 📈 | Upload day-ahead market price data |
| **Notices** | 📝 | Edit the notices and disclaimers shown on the calculator |
| **Audit Log** | 🕵️ | View full history of all tariff changes |
| **Publish** | 🚀 | Manually publish the current configuration |

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

> **Locked admin accounts** cannot be unlocked through the panel — see [Section 14.4](#144-unlocking-a-locked-admin-account) for the procedure.

### 4.5 Resending an invitation

If a supplier did not receive or has lost their invitation email, click **Resend invitation**. A new secure link is sent immediately. Previous links are invalidated.

### 4.6 Deleting a user

Click the red **Delete** button next to a supplier account to permanently remove it. This action cannot be undone. The supplier's tariffs remain in the system.

> Admin accounts cannot be deleted through the panel.

---

## 5. Supplier Management

Navigate to **Suppliers** in the left menu.

This section manages the registered details of each licensed supplier — name, licence number, address, contact email, telephone, and website. These details are displayed on the public calculator when a consumer expands a tariff card.

### Adding a supplier

1. Click **+ Add supplier**
2. Fill in the supplier details
3. Click **Save**

> A supplier record must exist before a user account can be created for that supplier, and before any tariffs can be submitted under that supplier's name.

### Editing a supplier

Click the **Edit** button next to any supplier to update their details. Changes are reflected immediately on the public calculator.

### Deleting a supplier

A supplier can only be deleted if they have no tariffs in the system. Remove all their tariffs first, then delete the supplier record.

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

Click **View** then **Delete** inside the modal. A confirmation prompt is shown. This action cannot be undone.

### 6.8 Tariff documents

Suppliers upload supporting documents (PDF, Word) when submitting or resubmitting a tariff. A 📎 button appears on tariffs that have documents attached. Click it to open the documents list where each file can be downloaded individually.

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
| **MDM** | Meter Data Management charge (€/month) — global default |

Click **Save** after making any changes. Changes are reflected immediately on the public calculator.

> The MDM charge can also be set on a per-tariff basis by the supplier. The per-tariff value takes precedence over the global default.

---

## 8. Load Profiles

Navigate to **Profiles** in the left menu.

Load profiles define how a consumer's annual electricity consumption is distributed across months, working days, and non-working days. They are used by the calculator to produce accurate cost estimates for Time-of-Use and Dynamic tariffs.

Profiles are imported from EAC CSV exports. Each profile contains 12 months of half-hourly load shapes for working days and non-working days.

### Uploading a profile

1. Click **+ Upload profile**
2. Select the CSV file exported from the DSO system
3. The system parses the file and shows a preview of coverage (months with working-day and non-working-day data)
4. Click **Save** to confirm

### Deleting a profile

A profile can only be deleted if no tariffs are currently assigned to it. Reassign affected tariffs to a different profile first.

---

## 9. Day-Ahead Market (DAM) Data

Navigate to **DAM Data** in the left menu.

DAM data is required to calculate costs for **Dynamic (market-linked)** tariffs. It provides day-ahead electricity market prices used to estimate what a consumer would pay under a dynamic pricing contract.

Two levels of data can be stored:

| Type | Granularity | Used for |
|---|---|---|
| **Monthly averages** | One average price per month (€/kWh) | Annual cost estimate for dynamic tariffs |
| **Half-hourly slot data** | 48 slots × 12 months | More accurate profile-weighted calculation |

### Updating DAM data

1. Enter or paste the monthly average prices for each month of the reference year
2. Optionally upload the half-hourly slot data file
3. Click **Save**

> DAM data represents historical or forecast prices and should be updated periodically to reflect current market conditions. The year of the data is recorded and displayed to consumers on the calculator.

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

Click **Save** after making any changes.

---

## 11. Audit Log

Navigate to **Audit Log** in the left menu.

The audit log records every create, edit, and delete action performed on tariffs, showing:

- The action taken (created / updated / deleted)
- The tariff name and supplier
- The date and time
- For edits: every field that changed, showing the old value and the new value side by side

The log is read-only and cannot be modified or deleted. Use it to track the history of any tariff and to investigate disputes with suppliers.

---

## 12. Publishing

Most changes (approvals, regulated charge updates, notices) take effect immediately on the public calculator without any manual publish step.

The **Publish** section is used to perform a **full configuration replacement** — uploading a complete configuration file (suppliers, tariffs, profiles, regulated charges, DAM data) in one operation. This is used for bulk initial setup or major migrations, not for routine day-to-day changes.

> Use Publish with caution. It replaces the entire configuration. All existing data is overwritten.

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

Emails are sent via Microsoft Azure (Mail.Send) using CERA's existing Azure tenant. They are sent from the address configured in the server's `.env` file (`TARIFF_EMAIL_FROM`).

> Emails are sent in the background and do not affect the response time of the panel. If email delivery fails, an error is recorded in the server log but the action (approval, rejection, etc.) still completes.

---

## 14. Security & Account Lockout

### 14.1 Lockout policy

To protect against unauthorised access, accounts are automatically locked after **3 consecutive failed login attempts**. The lockout lasts **3 hours**.

When an account is locked:
- The affected user receives an email notification immediately
- The email advises them to try again later or contact their CERA administrator
- A 🔒 Locked badge appears next to the account in the Users panel

### 14.2 Idle session timeout

Both the Admin Panel and Supplier Portal automatically sign a user out after **15 minutes of inactivity** (no clicks, key presses, or scrolling). A warning is shown 1 minute before sign-out, with a **Stay signed in** button to continue the session. This reduces the risk of an unattended, logged-in screen being used by someone else — e.g. an admin stepping away from their desk without locking their computer.

### 14.3 Unlocking a locked supplier account

See [Section 4.4](#44-unlocking-a-locked-supplier-account).

### 14.4 Unlocking a locked admin account

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

### 14.5 If you have forgotten your password

Use the **Forgot password** link on the admin login screen. A reset link will be sent to your registered CERA email address. The link is valid for 1 hour.

If you cannot receive the reset email, ask IT to reset your password using the command line tool:
```
python create_user.py --email yourname@cera.org.cy --role admin
```
This will prompt for a new password.

### 14.6 Creating a new admin account

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

### 14.7 Removing an admin account

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

---

## 16. Troubleshooting

### The login page shows but login fails
- Check your email and password are correct
- Check your account has not been locked (see Section 14)
- Check your account is active — ask another admin to verify in the Users panel

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
- On CERA's corporate network, dependency installation may fail — the `start.bat` script includes the necessary trusted-host flags, but if issues persist contact IT
- Check that the `.env` file exists inside the `tariff-api/` folder and contains the required values

### Emails are not being sent
- Check the Azure client secret in the `.env` file has not expired (secrets are set to expire after 12 months)
- Check the server log for email error messages
- Verify that the `TARIFF_EMAIL_FROM` address has the Mail.Send permission in the Azure portal

### The database file is missing
- The database file (`tariff-api/tariff.db`) is created automatically the first time the server starts
- If it has been accidentally deleted, all data is lost — restore from the most recent backup
- Contact IT to verify that automated backups are in place

---

*This document covers version 1.1 of the CERA Tariff Comparison Tool. For technical support or to report issues, contact the system administrator.*
