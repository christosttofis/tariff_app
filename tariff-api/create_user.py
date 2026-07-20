"""
CLI script to create admin panel user accounts.

Usage
-----
  # CERA admin account
  python create_user.py --email admin@cera.gov.cy --role admin

  # Supplier account (supplier_name must match a name in the suppliers table)
  python create_user.py --email info@volterra.com --role supplier --supplier "Volterra"

The script will prompt for the password interactively (not visible in shell history).

To deactivate a user (without deleting), use --deactivate:
  python create_user.py --email info@volterra.com --deactivate
"""

import argparse
import getpass
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import models
from auth import hash_password
from database import SessionLocal, engine


def pick_supplier(db) -> str:
    """Interactive prompt to choose a supplier from the DB by number or free text."""
    suppliers = [s.name for s in db.query(models.Supplier).order_by(models.Supplier.name).all()]
    if suppliers:
        print("\nExisting suppliers:")
        for i, name in enumerate(suppliers, 1):
            print(f"  {i}. {name}")
        print()
    else:
        print("\n(No suppliers in the database yet — you can still enter a name manually.)\n")

    while True:
        raw = input("Supplier [number or exact name]: ").strip()
        if not raw:
            print("Supplier name is required.")
            continue
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(suppliers):
                chosen = suppliers[idx]
                print(f'→ Using "{chosen}"')
                return chosen
            print(f"  Please enter a number between 1 and {len(suppliers)}.")
        else:
            if suppliers and raw not in suppliers:
                confirm = input(f'  "{raw}" is not in the supplier list. Use it anyway? [y/N] ')
                if confirm.lower() != "y":
                    continue
            return raw


def main():
    parser = argparse.ArgumentParser(description="Create or manage tariff admin users")
    parser.add_argument("--email", required=True, help="User email address")
    parser.add_argument("--role", choices=["admin", "supplier"], help="User role")
    parser.add_argument("--supplier", help="Supplier name (required for supplier role)")
    parser.add_argument("--deactivate", action="store_true", help="Deactivate this user")
    args = parser.parse_args()

    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        existing = db.query(models.User).filter(models.User.email == args.email).first()

        if args.deactivate:
            if not existing:
                print(f"User {args.email} not found.")
                sys.exit(1)
            existing.is_active = False
            db.commit()
            print(f"User {args.email} deactivated.")
            return

        if not args.role:
            parser.error("--role is required when creating a user")

        if args.role == "supplier" and not args.supplier:
            args.supplier = pick_supplier(db)

        supplier_id = None
        if args.role == "supplier":
            supplier = db.query(models.Supplier).filter(models.Supplier.name == args.supplier).first()
            if not supplier:
                print(f'Supplier "{args.supplier}" does not exist in the suppliers table — create it first.')
                sys.exit(1)
            supplier_id = supplier.id

        password = getpass.getpass(f"Password for {args.email}: ")
        if len(password) < 8:
            print("Password must be at least 8 characters.")
            sys.exit(1)

        now = datetime.now(timezone.utc).isoformat()

        if existing:
            confirm = input(f"User {args.email} already exists. Update password and role? [y/N] ")
            if confirm.lower() != "y":
                print("Aborted.")
                return
            existing.password_hash = hash_password(password)
            existing.role = args.role
            existing.supplier_id = supplier_id
            existing.is_active = True
            existing.password_changed_at = now
            existing.must_change_password = False
            existing.password_expiry_notified_at = None
            db.commit()
            print(f"Updated: {args.email} ({args.role})")
        else:
            db.add(models.User(
                email=args.email,
                password_hash=hash_password(password),
                role=args.role,
                supplier_id=supplier_id,
                is_active=True,
                created_at=now,
                password_changed_at=now,
            ))
            db.commit()
            print(f"Created: {args.email} ({args.role})")

    finally:
        db.close()


if __name__ == "__main__":
    main()
