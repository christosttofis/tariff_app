"""
Emergency unlock for a locked-out user account (intended for admin accounts
that cannot be unlocked through the admin panel).

Usage:
    python unlock_user.py --email yourname@cera.org.cy
"""

import argparse
import sys
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from database import engine
import lockout
import models


def unlock(email: str) -> None:
    with Session(engine) as db:
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            print(f"[ERROR] No account found for: {email}")
            sys.exit(1)

        # Always applied (not only when locked_until is set): it also lifts
        # per-address blocks, which leave no mark on the user row.
        lockout.clear(user, datetime.now(timezone.utc))
        db.commit()
        print(f"[OK] Account '{email}' has been unlocked.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Unlock a locked CERA Tariff Tool account.")
    parser.add_argument("--email", required=True, help="Email address of the account to unlock")
    args = parser.parse_args()
    unlock(args.email.strip().lower())
