"""
Generate a fresh SQLite database with entirely fake data, for the external
reviewer/specialist to run the app against without needing access to the
real PostgreSQL dev database or any real supplier/customer data.

Usage:
    cd tariff-api
    python seed_demo_data.py [output_path]      # default: ./demo.db

Then run the app against it:
    Windows (PowerShell):
        $env:DATABASE_URL = "sqlite:///./demo.db"
        .venv\\Scripts\\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000
    macOS/Linux:
        DATABASE_URL=sqlite:///./demo.db .venv/bin/python -m uvicorn main:app --host 127.0.0.1 --port 8000

Then open http://127.0.0.1:8000/customer.html (no login) or
http://127.0.0.1:8000/admin.html / supplier.html and sign in with one of
the accounts printed at the end of this script.

Every name, email, address, and password below is fake/placeholder data
invented for this script — none of it corresponds to a real CERA supplier,
customer, or account.
"""

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models

DEMO_PASSWORD = "Demo123!"


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def main():
    out_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "demo.db"
    if out_path.exists():
        print(f"Refusing to overwrite existing file: {out_path}")
        print("Delete it first or pass a different output path.")
        sys.exit(1)

    # Build the schema the same way the app itself does — via Alembic
    # migrations — rather than a separate create_all() path, so this demo
    # database is structurally identical to what start.bat/main.py produce.
    from alembic import command as alembic_command
    from alembic.config import Config as AlembicConfig

    db_url = f"sqlite:///{out_path}"
    alembic_cfg = AlembicConfig(str(Path(__file__).parent / "alembic.ini"))
    alembic_cfg.set_main_option("script_location", str(Path(__file__).parent / "migrations"))
    alembic_cfg.attributes["sqlalchemy.url"] = db_url
    alembic_command.upgrade(alembic_cfg, "head")

    engine = create_engine(db_url, connect_args={"check_same_thread": False})
    db = sessionmaker(bind=engine)()

    # ---- Suppliers ----
    suppliers = [
        models.Supplier(
            name="Acme Energy", licence="LIC-DEMO-001",
            address="12 Demo Street, Nicosia", website="https://acme-energy.example",
            email="contact@acme-energy.example", tel="+357 22 000001",
        ),
        models.Supplier(
            name="Delta Power", licence="LIC-DEMO-002",
            address="45 Sample Ave, Limassol", website="https://delta-power.example",
            email="contact@delta-power.example", tel="+357 25 000002",
        ),
        models.Supplier(
            name="Volt Co", licence="LIC-DEMO-003",
            address="7 Placeholder Rd, Larnaca", website="https://volt-co.example",
            email="contact@volt-co.example", tel="+357 24 000003",
        ),
    ]
    db.add_all(suppliers)
    db.commit()
    for s in suppliers:
        db.refresh(s)
    supplier_names = [s.name for s in suppliers]
    supplier_ids = [s.id for s in suppliers]

    # ---- Users: 2 admins, 1 user per supplier ----
    users = [
        models.User(email="admin1@demo.local", password_hash=hash_password(DEMO_PASSWORD),
                    role="admin", is_active=True, created_at=now_iso(),
                    otp_enabled=False, password_changed_at=now_iso()),
        models.User(email="admin2@demo.local", password_hash=hash_password(DEMO_PASSWORD),
                    role="admin", is_active=True, created_at=now_iso(),
                    otp_enabled=False, password_changed_at=now_iso()),
    ]
    for name, sid in zip(supplier_names, supplier_ids):
        users.append(models.User(
            email=f"{name.lower().replace(' ', '.')}@demo.local",
            password_hash=hash_password(DEMO_PASSWORD),
            role="supplier", supplier_id=sid, is_active=True, created_at=now_iso(),
            otp_enabled=False, password_changed_at=now_iso(),
        ))
    db.add_all(users)
    db.commit()

    # ---- Load profile ----
    flat_day = [1.0] * 48
    profile = models.Profile(
        id="demo-profile-flat",
        name="Flat Demo Profile",
        desc="Synthetic flat half-hourly load shape for demo purposes",
        months=json.dumps([{"W": flat_day, "NW": flat_day, "hasW": True, "hasNW": True} for _ in range(12)]),
        covW=12, covNW=12, rows=365, colCount=48,
    )
    db.add(profile)
    db.commit()

    # ---- Tariffs: mix of statuses across suppliers ----
    tariff_specs = [
        ("Acme Fixed Domestic", supplier_names[0], "Domestic", "LV", "Fixed", "approved", {"rate": 0.19}),
        ("Acme ToU Commercial", supplier_names[0], "Commercial", "MV", "ToU", "approved", {
            "hiStart": 4, "hiEnd": 10, "hiPeakStart": 8, "hiPeakEnd": 22,
            "loPeakStart": 17, "loPeakEnd": 20, "hiPeakRate": 0.22, "hiOffRate": 0.15,
            "loPeakRate": 0.20, "loOffRate": 0.13,
        }),
        ("Delta Dynamic Industrial", supplier_names[1], "Industrial", "HV", "Dynamic", "pending",
         {"mult": 1.05, "adder": 0.01, "damFloor": 0.05}),
        ("Delta Variable Domestic", supplier_names[1], "Domestic", "LV", "Variable", "draft", {
            "resetMonths": 12,
            "tiers": [{"upTo": 200, "rate": 0.17, "fixedCharge": 0}, {"upTo": None, "rate": 0.21, "fixedCharge": 0}],
        }),
        ("Volt Fixed Commercial", supplier_names[2], "Commercial", "LV", "Fixed", "approved", {"rate": 0.185}),
        ("Volt Fixed Domestic (rejected demo)", supplier_names[2], "Domestic", "LV", "Fixed", "rejected", {"rate": 0.30}),
    ]
    for i, (name, supplier, contract, voltage, pricing, status, rates) in enumerate(tariff_specs):
        db.add(models.Tariff(
            id=f"demo-tariff-{i+1}",
            name=name, supplier=supplier, contract=contract, voltage=voltage, pricing=pricing,
            standing=2.5, mdm=0.30, rates=json.dumps(rates), profileId=profile.id,
            fpaSource="global", fpaCustom=0.0, discounts="[]", vulnerable=False,
            status=status,
            rejection_reason="Demo rejection reason — pricing exceeds regulated cap." if status == "rejected" else None,
            createdAt=now_iso(), updatedAt=now_iso(),
        ))
    db.commit()

    # ---- Regulated charges (single row) ----
    db.add(models.Regulated(
        id=1, lv=0.045, mv=0.038, hv=0.030,
        fpaLV=0.06, fpaMV=0.055, fpaHV=0.05,
        pso=0.005, res=0.007, mdm=0.30,
        updated_at=now_iso(), fpa_updated_at=now_iso(), grid_updated_at=now_iso(), universal_updated_at=now_iso(),
    ))

    # ---- DAM data (single row, minimal placeholder) ----
    db.add(models.DamData(
        id=1,
        damMonthly=json.dumps([0.08] * 12),
        damBySlot=json.dumps([[0.08] * 48 for _ in range(12)]),
        damDailyData="[]",
        damRowCount=0, damYear=datetime.now().year,
    ))

    # ---- Notices ----
    db.add(models.Notices(
        id=1,
        assumptions_en="<p>Demo assumptions text (EN).</p>",
        assumptions_el="<p>Δοκιμαστικό κείμενο παραδοχών (EL).</p>",
        legal_en="<p>Demo legal notice (EN).</p>", legal_el="<p>Δοκιμαστικό νομικό σημείωμα (EL).</p>",
        vulnerable_en="<p>Demo vulnerable-customer notice (EN).</p>",
        vulnerable_el="<p>Δοκιμαστική ειδοποίηση ευάλωτων πελατών (EL).</p>",
    ))
    db.commit()

    # ---- A little changelog history, so the Changelog tab isn't empty ----
    for i, (name, supplier, *_rest) in enumerate(tariff_specs[:3]):
        db.add(models.Changelog(
            id=f"demo-changelog-{i+1}",
            tariffId=f"demo-tariff-{i+1}", tariffName=name, supplier=supplier,
            action="created", changes="[]",
            ts=(datetime.now(timezone.utc) - timedelta(days=i + 1)).isoformat(),
            actorRole="supplier", actorEmail=f"{supplier.lower().replace(' ', '.')}@demo.local",
        ))
    db.commit()
    db.close()

    print(f"Wrote demo database to {out_path}\n")
    print("Demo accounts (all use password: " + DEMO_PASSWORD + ", OTP disabled for convenience):")
    print("  admin1@demo.local        (admin)")
    print("  admin2@demo.local        (admin)")
    for name in supplier_names:
        print(f"  {name.lower().replace(' ', '.')}@demo.local   (supplier — {name})")
    print("\nAll data above is synthetic placeholder data — no real CERA suppliers,")
    print("customers, or accounts are represented.")


if __name__ == "__main__":
    main()
