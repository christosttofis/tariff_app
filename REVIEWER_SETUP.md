# Setup for external review

This repo contains no real data or secrets — `.env` and the production database
were never committed (see `.gitignore`). Follow these steps to run the app
locally against a synthetic demo dataset.

**Start here:** `TECHNICAL_ARCHITECTURE_REVIEW.pdf` — the technical/security
architecture reference this walkthrough is meant to accompany.

## 1. Prerequisites

- Python 3.11+ installed and on PATH
- Windows (the provided `start.bat` is Windows-specific; on macOS/Linux see
  the manual steps at the bottom of this file)

## 2. One-time setup

```
git clone <this repo>
cd tariff_app\tariff-api
```

Create a file named `.env` in `tariff-api\` with this content:

```
DATABASE_URL=sqlite:///./demo.db
TARIFF_SECRET_KEY=any-random-string-for-local-testing-only
```

(`DATABASE_URL` points the app at the demo SQLite file created in the next
step, instead of falling back to an empty local database. `TARIFF_SECRET_KEY`
signs login sessions — any string works for a local test run.)

Generate the demo database:

```
python seed_demo_data.py
```

This creates `tariff-api\demo.db` with fake suppliers, tariffs, and accounts —
no real CERA data. It prints the login accounts again at the end, also listed
below.

## 3. Run the app

From the repo root, double-click `start.bat` (or run it from a terminal). It
creates a virtual environment, installs dependencies, and starts the server —
watch for `.env` being picked up automatically.

```
Customer (public, no login): http://localhost:8000/customer.html
Admin panel:                 http://localhost:8000/admin.html
Supplier portal:             http://localhost:8000/supplier.html
API docs (Swagger):          http://localhost:8000/docs
```

## 4. Demo accounts

All passwords: `Demo123!` — 2FA/OTP is disabled on these accounts for
convenience (email sending isn't configured in this environment anyway, since
no real Azure credentials are included).

| Email | Role | Notes |
|---|---|---|
| `admin1@demo.local` | admin | full CERA staff access |
| `admin2@demo.local` | admin | second admin account, for cross-account testing |
| `acme.energy@demo.local` | supplier | scoped to "Acme Energy" |
| `delta.power@demo.local` | supplier | scoped to "Delta Power" |
| `volt.co@demo.local` | supplier | scoped to "Volt Co" |

Demo tariffs are seeded across every status (draft/pending/approved/rejected)
and pricing type (Fixed/ToU/Dynamic/Variable) to exercise most of the app's
functionality without needing to create data manually.

## 5. Known limitations of this demo environment

- **No email sending** — OTP codes, password resets, and notifications won't
  actually be delivered (no real Azure/Graph credentials are included). The
  demo accounts have OTP disabled specifically so login still works without
  email. If you want to test the OTP/email flow itself, that requires real
  Azure AD app credentials, which aren't provided in this environment.
- **SQLite, not the real PostgreSQL** — functionally equivalent for review
  purposes (same ORM code path), but not representative of the production
  database engine.
- **Re-running `seed_demo_data.py`** refuses to overwrite an existing
  `demo.db` — delete it first if you want a fresh copy.

## Manual run (macOS/Linux, or if you'd rather not use start.bat)

```
cd tariff-api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python seed_demo_data.py
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Do **not** add `--reload` — it causes HTTP 500 errors on POST requests with
this Python/uvicorn combination (a known, documented issue, not something to
debug).
