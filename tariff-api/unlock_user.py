"""
Emergency unlock for a locked-out user account (intended for admin accounts
that cannot be unlocked through the admin panel).

Usage:
    python unlock_user.py --email yourname@cera.org.cy
"""

import argparse
import sys

from sqlalchemy.orm import Session

from database import engine
import models


def unlock(email: str) -> None:
    with Session(engine) as db:
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            print(f"[ERROR] No account found for: {email}")
            sys.exit(1)

        if not user.locked_until and not user.failed_attempts:
            print(f"[INFO] Account '{email}' is not locked — nothing to do.")
            return

        user.failed_attempts = 0
        user.locked_until = None
        db.commit()
        print(f"[OK] Account '{email}' has been unlocked.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Unlock a locked CERA Tariff Tool account.")
    parser.add_argument("--email", required=True, help="Email address of the account to unlock")
    args = parser.parse_args()
    unlock(args.email.strip().lower())
