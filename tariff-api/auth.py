"""
JWT authentication utilities and FastAPI dependencies.

Secret key
----------
Read from config.py (TARIFF_SECRET_KEY env var). The fallback there is for
local development only — any token signed with the dev key would be
accepted by any other dev install, so never deploy it.

Token lifetime: sliding — each authenticated request extends the session by
TOKEN_EXPIRE_HOURS, capped at ABSOLUTE_SESSION_HOURS from the original login
regardless of activity (bounds how long a stolen/replayed token stays useful).

Roles
-----
  admin    — CERA staff; can see/edit everything and approve tariffs
  supplier — licensed supplier; can only manage their own tariffs
"""

import re
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

import email_utils
import models
from config import TARIFF_SECRET_KEY
from database import get_db

# Endpoints reachable even while a user's password has expired (must_change_password=True) —
# just enough to let them set a new password and sign out, nothing else.
_PASSWORD_EXPIRED_ALLOWLIST = {
    "/api/auth/password",
}

PASSWORD_EXPIRY_DAYS = 180        # 6 months
PASSWORD_REUSE_HISTORY = 5        # block reuse of the last N passwords

# ── Secret & algorithm ────────────────────────────────────────────────────────

SECRET_KEY = TARIFF_SECRET_KEY
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 1      # sliding window — renewed on each authenticated request
ABSOLUTE_SESSION_HOURS = 12  # hard cap from login, regardless of activity
OTP_EXPIRE_MINUTES = 10

# The session JWT lives in an httpOnly cookie so it's never exposed to JS (and
# therefore can't be exfiltrated by an XSS payload) — no Max-Age is set, so
# it's a browser-session cookie (dies when the browser closes). The token
# itself is reissued with a fresh expiry on every authenticated request (see
# get_current_user), so an active user is never logged out mid-work; the
# ABSOLUTE_SESSION_HOURS cap is the real backstop against a stolen/replayed
# token being kept alive indefinitely.
ACCESS_COOKIE_NAME = "cera_access_token"

# ── Password hashing ──────────────────────────────────────────────────────────

def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


_SYMBOL_RE = re.compile(r"[^A-Za-z0-9]")


def validate_password_strength(pw: str) -> None:
    """Raises HTTPException(400) if pw doesn't meet the minimum policy:
    8+ chars, at least one letter, one digit, one symbol."""
    if len(pw) < 8:
        raise HTTPException(400, "Password must be at least 8 characters.")
    if not re.search(r"[A-Za-z]", pw):
        raise HTTPException(400, "Password must include at least one letter.")
    if not re.search(r"[0-9]", pw):
        raise HTTPException(400, "Password must include at least one number.")
    if not _SYMBOL_RE.search(pw):
        raise HTTPException(400, "Password must include at least one symbol.")


def check_password_reuse(db: Session, user: "models.User", new_plain: str) -> None:
    """Raises HTTPException(400) if new_plain matches the current password or
    any of the user's last PASSWORD_REUSE_HISTORY passwords."""
    if verify_password(new_plain, user.password_hash):
        raise HTTPException(400, "New password must be different from your current password.")
    history = (
        db.query(models.PasswordHistory)
        .filter(models.PasswordHistory.user_id == user.id)
        .order_by(models.PasswordHistory.id.desc())
        .limit(PASSWORD_REUSE_HISTORY)
        .all()
    )
    for rec in history:
        if verify_password(new_plain, rec.password_hash):
            raise HTTPException(400, f"You cannot reuse one of your last {PASSWORD_REUSE_HISTORY} passwords.")


def record_password_change(db: Session, user: "models.User", new_plain: str) -> None:
    """Archives the current hash, sets the new one, and clears the expiry flags."""
    now = datetime.now(timezone.utc).isoformat()
    db.add(models.PasswordHistory(user_id=user.id, password_hash=user.password_hash, changed_at=now))
    db.flush()  # SessionLocal has autoflush=False — make the just-added row visible to the query below
    old_ids = [
        row.id for row in
        db.query(models.PasswordHistory.id)
        .filter(models.PasswordHistory.user_id == user.id)
        .order_by(models.PasswordHistory.id.desc())
        .offset(PASSWORD_REUSE_HISTORY)
        .all()
    ]
    if old_ids:
        db.query(models.PasswordHistory).filter(models.PasswordHistory.id.in_(old_ids)).delete(synchronize_session=False)

    user.password_hash = hash_password(new_plain)
    user.password_changed_at = now
    user.must_change_password = False
    user.password_expiry_notified_at = None
    db.commit()


# ── Token creation ────────────────────────────────────────────────────────────

def create_token(user: models.User, session_start: datetime | None = None) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "role": user.role,
        "supplier_id": user.supplier_id,
        "iat": now,
        # Preserved across sliding renewals so ABSOLUTE_SESSION_HOURS can be enforced
        # from the original login, not from whichever renewal issued this token.
        # PyJWT only auto-converts the registered iat/exp/nbf claims from datetime —
        # this is a custom claim, so it must be encoded as a timestamp explicitly.
        "session_start": (session_start or now).timestamp(),
        "exp": now + timedelta(hours=TOKEN_EXPIRE_HOURS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def set_auth_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=ACCESS_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=True,
        samesite="strict",
        path="/",
    )


def clear_auth_cookie(response: Response) -> None:
    response.delete_cookie(key=ACCESS_COOKIE_NAME, path="/")


def create_pending_token(email: str) -> str:
    """Short-lived token issued after password check, before OTP verification.
    Carries purpose='otp' so get_current_user rejects it for normal API calls."""
    payload = {
        "sub": email,
        "purpose": "otp",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=OTP_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_pending_token(token: str) -> str:
    """Decode a pending OTP token and return the email, or raise HTTPException."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "OTP session expired — please log in again")
    except jwt.InvalidTokenError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid session token")
    if payload.get("purpose") != "otp":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid session token")
    return payload["sub"]


# ── Current-user dependency ───────────────────────────────────────────────────

def resolve_supplier_name(db: Session, user: models.User) -> str | None:
    """Look up a user's supplier name live via supplier_id, so a supplier
    rename is reflected immediately everywhere without needing to cascade
    an update to any User row."""
    if user.supplier_id is None:
        return None
    supplier = db.get(models.Supplier, user.supplier_id)
    return supplier.name if supplier else None


class CurrentUser:
    def __init__(self, id: int, email: str, role: str, supplier_name: str | None, supplier_id: int | None = None):
        self.id = id
        self.email = email
        self.role = role
        self.supplier_name = supplier_name
        self.supplier_id = supplier_id

    @property
    def is_admin(self) -> bool:
        return self.role == "admin"

    @property
    def is_supplier(self) -> bool:
        return self.role == "supplier"


def get_current_user(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
) -> CurrentUser:
    token = request.cookies.get(ACCESS_COOKIE_NAME)
    if not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not authenticated")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token expired — please log in again")
    except jwt.InvalidTokenError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")

    if payload.get("purpose") == "otp":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "2FA not yet completed")

    session_start_ts = payload.get("session_start")
    session_start = datetime.fromtimestamp(session_start_ts, tz=timezone.utc) if session_start_ts else None
    if session_start and datetime.now(timezone.utc) - session_start > timedelta(hours=ABSOLUTE_SESSION_HOURS):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Session expired — please log in again")

    user = db.get(models.User, int(payload["sub"]))
    if not user or not user.is_active:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User not found or deactivated")

    # Invalidate tokens issued before the most recent password change — closes the
    # window where an old (stolen or superseded) token stays valid after a reset.
    iat = payload.get("iat")
    if iat and user.password_changed_at:
        token_issued = datetime.fromtimestamp(iat, tz=timezone.utc)
        changed_at = datetime.fromisoformat(user.password_changed_at)
        if changed_at.tzinfo is None:
            changed_at = changed_at.replace(tzinfo=timezone.utc)
        if token_issued < changed_at:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Session invalidated — please log in again")

    if user.must_change_password and request.url.path not in _PASSWORD_EXPIRED_ALLOWLIST:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "password_expired")

    # Sliding renewal — every authenticated request extends the session by
    # TOKEN_EXPIRE_HOURS, still capped at ABSOLUTE_SESSION_HOURS from session_start.
    set_auth_cookie(response, create_token(user, session_start=session_start))

    return CurrentUser(
        id=user.id,
        email=user.email,
        role=user.role,
        supplier_name=resolve_supplier_name(db, user),
        supplier_id=user.supplier_id,
    )


def require_admin(user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    """Dependency: allows only admin-role users through."""
    if not user.is_admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Admin access required")
    return user


# ── Password expiry background check ──────────────────────────────────────────

_PASSWORD_REMINDER_LEAD_DAYS = 14  # send the reminder this many days before expiry


def run_password_expiry_check(db: Session) -> None:
    """Flags overdue passwords and emails a one-time reminder before expiry.
    Called once a day from main.py's background scheduler loop — not an HTTP endpoint."""
    now = datetime.now(timezone.utc)
    users = db.query(models.User).filter(
        models.User.is_active == True,  # noqa: E712
        models.User.password_changed_at.isnot(None),
    ).all()

    for user in users:
        changed_at = datetime.fromisoformat(user.password_changed_at)
        if changed_at.tzinfo is None:
            changed_at = changed_at.replace(tzinfo=timezone.utc)
        age_days = (now - changed_at).days
        days_left = PASSWORD_EXPIRY_DAYS - age_days

        if days_left <= 0:
            if not user.must_change_password:
                user.must_change_password = True
                db.commit()
        elif days_left <= _PASSWORD_REMINDER_LEAD_DAYS and not user.password_expiry_notified_at:
            email_utils.notify_password_expiring(user.email, days_left, user.role)
            user.password_expiry_notified_at = now.isoformat()
            db.commit()
