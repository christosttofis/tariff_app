# Setting Up a Test Environment — IT Review

This guide sets up a fully working copy of the Tariff Comparison Tool on your own PC, using synthetic test data only — no real CERA data, credentials, or secrets are included in this package.

## Prerequisites

- Python 3.11 or newer installed, with "Add Python to PATH" ticked during install
- Internet access (needed once, to download dependencies)

## 1. Start the app

Run `start.bat` in the project root. On first run it will:
- Create a Python virtual environment (`.venv`)
- Install all required dependencies
- Start the server at `http://localhost:8000`

No database setup is required — the app automatically creates a fresh, empty local SQLite database file (`tariff-api/tariff.db`) on first run, since no production `DATABASE_URL` is configured in this package.

If it worked, you should be able to open `http://localhost:8000/customer.html` in a browser and see the (currently empty) tariff comparison calculator.

## 2. Create a test admin account

Open a **new** terminal window, then:

```
cd tariff-api
.venv\Scripts\activate
python create_user.py --email testadmin@example.com --role admin
```

It will prompt for a password (minimum 8 characters) — anything is fine, e.g. `TestAdmin123`.

## 3. Log in as admin

Go to `http://localhost:8000/admin.html` and log in with the account you just created.

From there, use the admin panel to:
- Add a test supplier (e.g. "Test Energy Ltd")
- Either invite a supplier account through the panel itself (tests the real invite flow), **or** create one directly for speed:

```
python create_user.py --email testsupplier@example.com --role supplier --supplier "Test Energy Ltd"
```

## 4. Submit and approve a test tariff

- Log in as the supplier account at the supplier portal and submit one or two test tariffs with made-up numbers.
- Log back in as admin and approve them.

## 5. Verify the public-facing side

Open `http://localhost:8000/customer.html` (no login required) and confirm the approved test tariff appears correctly in the comparison calculator.

---

**Note on scope**: this package intentionally omits the real production database and any live credentials (Azure email secret, production database password). If testing the email-notification flow specifically is needed, let us know and we'll provide separate, disposable test credentials for that rather than the live ones.
