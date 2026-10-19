"""
Sign-in lockout rules, shared by the sign-in endpoints, the admin panel's
unlock/activate buttons and unlock_user.py.

Wrong passwords are counted from the login_activity log (no extra table), per
account AND per address, so a stranger who knows a supplier's email can no
longer lock the real person out:

  - IP_MAX_FAILURES wrong passwords for one email from one address within
    IP_WINDOW: that address may not try that email again until the oldest of
    them is older than IP_WINDOW. The owner, signing in from elsewhere, is
    unaffected. Unknown emails are treated the same (no account discovery).
  - ACCOUNT_MAX_FAILURES wrong passwords for one email from all addresses
    within ACCOUNT_WINDOW: the whole account is locked for LOCK_MINUTES and its
    owner is emailed. One address can make at most 20 attempts an hour, so
    this needs several addresses guessing at once.
  - OTP_MAX_FAILURES wrong 6-digit sign-in codes in a row (only reachable with
    the right password, so a sign the password is known): the account is
    locked for LOCK_MINUTES and its owner is emailed. A correct password does
    not reset this count; only a completed sign-in or an unlock does, so the
    codes can't be guessed a few at a time across repeated sign-ins.

What resets the counts:
  - a completed sign-in: the wrong-code count, and the wrong-password count of
    the address it came from only (the owner signing in must not give an
    attacker's address fresh tries; the account-wide count isn't reset either,
    since no real user gets near it);
  - an admin unlock or reactivation (or unlock_user.py): everything, by setting
    User.lockout_reset_at.
"""

from datetime import datetime, timedelta

from sqlalchemy import func

import models

IP_MAX_FAILURES = 5
IP_WINDOW = timedelta(minutes=15)
ACCOUNT_MAX_FAILURES = 30
ACCOUNT_WINDOW = timedelta(minutes=60)
OTP_MAX_FAILURES = 3
LOCK_MINUTES = 30

# login_activity reasons that count as a wrong password (blocked attempts don't count).
PASSWORD_FAILURES = ("bad_password", "unknown_email")

# One message for every kind of block, so it doesn't reveal which one applied
# (an account lock would otherwise confirm that the account exists).
LOCKED_MESSAGE = ("Too many failed sign-in attempts. "
                  "Please try again later or contact your CERA administrator.")


def _failures(db, email: str, user: "models.User | None", since: str):
    # ISO-8601 UTC strings, all written by datetime.now(timezone.utc).isoformat(), compare in time order.
    if user is not None and user.lockout_reset_at and user.lockout_reset_at > since:
        since = user.lockout_reset_at
    return db.query(models.LoginActivity).filter(
        models.LoginActivity.email == email,
        models.LoginActivity.reason.in_(PASSWORD_FAILURES),
        models.LoginActivity.ts > since,
    )


def address_blocked(db, email: str, user, ip: str | None, now: datetime) -> bool:
    """Has this address used up its wrong-password attempts for this email?"""
    since = (now - IP_WINDOW).isoformat()
    last_ok = db.query(func.max(models.LoginActivity.ts)).filter(
        models.LoginActivity.email == email, models.LoginActivity.ip_address == ip,
        models.LoginActivity.success == True,  # noqa: E712
    ).scalar()
    q = _failures(db, email, user, max(since, last_ok or since)).filter(models.LoginActivity.ip_address == ip)
    return q.count() >= IP_MAX_FAILURES


def account_failures(db, email: str, user, now: datetime) -> int:
    return _failures(db, email, user, (now - ACCOUNT_WINDOW).isoformat()).count()


def is_locked(user: "models.User", now: datetime) -> bool:
    return bool(user.locked_until and now < datetime.fromisoformat(user.locked_until))


def lock(user: "models.User", now: datetime) -> None:
    user.locked_until = (now + timedelta(minutes=LOCK_MINUTES)).isoformat()


def signed_in(user: "models.User") -> None:
    """Completed sign-in. (Its success row in login_activity resets that address's count.)"""
    user.failed_attempts = 0
    user.locked_until = None


def clear(user: "models.User", now: datetime) -> None:
    """Admin unlock or reactivation: every count starts again, for every address."""
    signed_in(user)
    user.lockout_reset_at = now.isoformat()
