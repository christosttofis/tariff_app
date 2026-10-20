"""Auth router — login, forgot-password, reset-password endpoints."""

import secrets
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.orm import Session

import email_utils
import lockout
import models
from client_ip import UNAVAILABLE_DETAIL, admin_network_allowed, client_ip_str
from auth import (
    OTP_EXPIRE_MINUTES, CurrentUser, check_password_reuse, clear_auth_cookie, create_pending_token, create_token,
    decode_pending_token, get_current_user, hash_password, otp_digest, otp_matches, record_password_change,
    reset_token_digest, resolve_supplier_name, set_auth_cookie, validate_password_strength, verify_password,
)
from config import TARIFF_BASE_URL
from database import get_db
from schemas import _check_email

router = APIRouter(prefix="/api/auth", tags=["auth"])

_BASE_URL = TARIFF_BASE_URL

# Checked against for unknown emails, so a sign-in takes the same time whether or not
# the account exists (otherwise the reply time reveals which emails are registered).
_DUMMY_HASH = hash_password(secrets.token_urlsafe(16))


def _log_login(db: Session, request: Request, *, email: str, user_id: int | None, success: bool, reason: str) -> None:
    db.add(models.LoginActivity(
        email=email,
        user_id=user_id,
        success=success,
        reason=reason,
        ip_address=client_ip_str(request),
        user_agent=request.headers.get("user-agent"),
        ts=datetime.now(timezone.utc).isoformat(),
    ))
    db.commit()


def _send_new_otp(db: Session, email: str, now: datetime) -> None:
    """Replace any earlier sign-in code for this email with a new 6-digit one,
    stored only as a keyed hash, and email it. (Sign-in and "resend code".)"""
    code = str(secrets.randbelow(900000) + 100000)
    db.query(models.OtpCode).filter(models.OtpCode.email == email).delete()
    expires = (now + timedelta(minutes=OTP_EXPIRE_MINUTES)).isoformat()
    db.add(models.OtpCode(email=email, code=otp_digest(email, code), expires_at=expires, created_at=now.isoformat()))
    db.commit()
    email_utils.send_otp_code(email, code)


class LoginIn(BaseModel):
    email: str
    password: str


class ForgotPasswordIn(BaseModel):
    email: str


class ResetPasswordIn(BaseModel):
    token: str
    password: str


class VerifyOtpIn(BaseModel):
    pending_token: str
    code: str


class ResendOtpIn(BaseModel):
    pending_token: str


class UpdateEmailIn(BaseModel):
    new_email: str
    # Re-authentication: without it, anyone holding a stolen session cookie
    # could change the email and then take the account over via
    # forgot-password.
    current_password: str = Field(..., max_length=200)

    _validate_new_email = field_validator("new_email")(_check_email)


class UpdatePasswordIn(BaseModel):
    current_password: str
    new_password: str


@router.post("/login", summary="Exchange email + password for a session cookie")
def login(body: LoginIn, request: Request, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == body.email).first()
    now = datetime.now(timezone.utc)

    # Admin accounts only work from the CERA office/VPN networks. Checked
    # before the password on purpose: the password is never tested from
    # outside (no way to confirm a guess), and failed attempts from the
    # internet can't lock an admin out. Response is the generic
    # "Website unavailable" (the admin page itself is unavailable outside too).
    if user and user.role == "admin" and not admin_network_allowed(request):
        _log_login(db, request, email=body.email, user_id=user.id, success=False, reason="network_blocked")
        raise HTTPException(404, UNAVAILABLE_DETAIL)

    # Lockouts (see lockout.py) are checked before the password, so a blocked
    # caller learns nothing from guessing. Blocked attempts are logged but not
    # counted as wrong passwords.
    user_id = user.id if user else None
    if user and user.locked_until:
        if lockout.is_locked(user, now):
            _log_login(db, request, email=body.email, user_id=user_id, success=False, reason="locked")
            raise HTTPException(429, lockout.LOCKED_MESSAGE)
        user.failed_attempts = 0        # lock has expired
        user.locked_until = None
        db.commit()
    if lockout.address_blocked(db, body.email, user, client_ip_str(request), now):
        _log_login(db, request, email=body.email, user_id=user_id, success=False, reason="address_blocked")
        raise HTTPException(429, lockout.LOCKED_MESSAGE)

    if not verify_password(body.password, user.password_hash if user else _DUMMY_HASH) or not user:
        # Same reply for a wrong password and an unknown email, and no attempts-remaining
        # count, so the reply doesn't reveal which emails are registered.
        _log_login(db, request, email=body.email, user_id=user_id, success=False,
                   reason="bad_password" if user else "unknown_email")
        if user and lockout.account_failures(db, body.email, user, now) >= lockout.ACCOUNT_MAX_FAILURES:
            # Many addresses guessing at once: lock the whole account, tell the owner.
            lockout.lock(user, now)
            db.commit()
            email_utils.notify_account_locked(user.email, lockout.LOCK_MINUTES, user.role)
            _log_login(db, request, email=body.email, user_id=user_id, success=False, reason="locked_out")
            raise HTTPException(429, lockout.LOCKED_MESSAGE)
        raise HTTPException(401, "Invalid email or password")

    if not user.is_active:
        _log_login(db, request, email=body.email, user_id=user.id, success=False, reason="inactive")
        raise HTTPException(403, "Account is inactive — contact your CERA administrator")

    # Skip OTP entirely if disabled for this user (e.g. during testing)
    if not (user.otp_enabled if user.otp_enabled is not None else True):
        lockout.signed_in(user)
        db.commit()
        _log_login(db, request, email=user.email, user_id=user.id, success=True, reason="password_only")
        set_auth_cookie(response, create_token(user))
        return {
            "role": user.role,
            "supplier": resolve_supplier_name(db, user),
            "email": user.email,
        }

    _send_new_otp(db, user.email, now)
    return {
        "status": "otp_required",
        "pending_token": create_pending_token(user.email),
    }


@router.post("/verify-otp", summary="Verify OTP code and exchange for a session cookie")
def verify_otp(body: VerifyOtpIn, request: Request, response: Response, db: Session = Depends(get_db)):
    email = decode_pending_token(body.pending_token)
    now_dt = datetime.now(timezone.utc)
    now = now_dt.isoformat()

    user = db.query(models.User).filter(models.User.email == email, models.User.is_active == True).first()
    if not user:
        _log_login(db, request, email=email, user_id=None, success=False, reason="user_not_found")
        raise HTTPException(401, "User not found or deactivated.")
    # A login started inside the network must also be finished inside it.
    if user.role == "admin" and not admin_network_allowed(request):
        _log_login(db, request, email=email, user_id=user.id, success=False, reason="network_blocked")
        raise HTTPException(404, UNAVAILABLE_DETAIL)

    # Wrong codes count in user.failed_attempts (lockout.py). Only a completed
    # sign-in or an unlock resets it, not a correct password, so the 6-digit code
    # can't be guessed a few tries at a time across repeated sign-ins.
    if user.locked_until:
        if lockout.is_locked(user, now_dt):
            _log_login(db, request, email=email, user_id=user.id, success=False, reason="locked")
            raise HTTPException(429, lockout.LOCKED_MESSAGE)
        user.failed_attempts = 0        # lock has expired
        user.locked_until = None
        db.commit()

    rec = (
        db.query(models.OtpCode)
        .filter(models.OtpCode.email == email, models.OtpCode.used == False)
        .order_by(models.OtpCode.id.desc())
        .first()
    )
    if not rec or rec.expires_at < now or not otp_matches(rec.code, email, body.code.strip()):
        user.failed_attempts = (user.failed_attempts or 0) + 1
        if user.failed_attempts >= lockout.OTP_MAX_FAILURES:
            lockout.lock(user, now_dt)
            db.commit()
            email_utils.notify_account_locked(user.email, lockout.LOCK_MINUTES, user.role)
            _log_login(db, request, email=email, user_id=user.id, success=False, reason="locked_out")
            raise HTTPException(429, lockout.LOCKED_MESSAGE)
        remaining = lockout.OTP_MAX_FAILURES - user.failed_attempts
        db.commit()
        _log_login(db, request, email=email, user_id=user.id, success=False, reason="bad_otp")
        raise HTTPException(
            401,
            f"Invalid or expired verification code. "
            f"{remaining} attempt(s) remaining before your account is locked."
        )

    rec.used = True
    lockout.signed_in(user)
    db.commit()

    _log_login(db, request, email=user.email, user_id=user.id, success=True, reason="otp_verified")

    set_auth_cookie(response, create_token(user))
    return {
        "role": user.role,
        "supplier": resolve_supplier_name(db, user),
        "email": user.email,
    }


@router.post("/logout", summary="Clear the session cookie")
def logout(response: Response):
    clear_auth_cookie(response)
    return {"message": "Signed out."}


@router.get("/me", summary="Current session's identity — lets the frontend re-hydrate the user badge after a reload/new tab")
def me(user: CurrentUser = Depends(get_current_user)):
    return {"role": user.role, "supplier": user.supplier_name, "email": user.email}


_OTP_RESEND_COOLDOWN_SECONDS = 120  # 2 minutes


@router.post("/resend-otp", summary="Resend OTP code (minimum 2 minutes between sends)")
def resend_otp(body: ResendOtpIn, request: Request, db: Session = Depends(get_db)):
    email = decode_pending_token(body.pending_token)
    now = datetime.now(timezone.utc)

    user = db.query(models.User).filter(models.User.email == email).first()
    if user and user.role == "admin" and not admin_network_allowed(request):
        raise HTTPException(404, UNAVAILABLE_DETAIL)

    rec = (
        db.query(models.OtpCode)
        .filter(models.OtpCode.email == email, models.OtpCode.used == False)
        .order_by(models.OtpCode.id.desc())
        .first()
    )

    if rec and rec.created_at:
        created = datetime.fromisoformat(rec.created_at)
        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)
        elapsed = (now - created).total_seconds()
        if elapsed < _OTP_RESEND_COOLDOWN_SECONDS:
            wait = int(_OTP_RESEND_COOLDOWN_SECONDS - elapsed)
            raise HTTPException(429, f"Please wait {wait} seconds before requesting a new code.")

    _send_new_otp(db, email, now)
    return {"message": "A new verification code has been sent to your email."}


@router.post("/forgot-password", summary="Request a password reset link by email")
def forgot_password(body: ForgotPasswordIn, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == body.email,
        models.User.is_active == True,
    ).first()
    if user:
        # Remove any existing unused tokens for this email
        db.query(models.PasswordReset).filter(
            models.PasswordReset.email == body.email
        ).delete()
        token = secrets.token_urlsafe(32)
        expires = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
        db.add(models.PasswordReset(token=reset_token_digest(token), email=body.email, expires_at=expires))
        db.commit()
        portal = "supplier" if user.role == "supplier" else "admin"
        reset_url = f"{_BASE_URL}/reset-password.html?token={token}&portal={portal}"
        email_utils.notify_password_reset(body.email, reset_url)
    # Always return the same message — don't reveal whether the email exists
    return {"message": "If this email is registered, a reset link has been sent."}


@router.post("/reset-password", summary="Set a new password using a reset token")
def reset_password(body: ResetPasswordIn, db: Session = Depends(get_db)):
    rec = db.get(models.PasswordReset, reset_token_digest(body.token))
    now = datetime.now(timezone.utc).isoformat()
    if not rec or rec.used or rec.expires_at < now:
        raise HTTPException(400, "This reset link is invalid or has expired.")
    validate_password_strength(body.password)
    user = db.query(models.User).filter(
        models.User.email == rec.email,
        models.User.is_active == True,
    ).first()
    if not user:
        raise HTTPException(400, "This reset link is invalid or has expired.")
    check_password_reuse(db, user, body.password)
    record_password_change(db, user, body.password)
    rec.used = True
    db.commit()
    return {"message": "Password updated. You can now sign in."}


@router.put("/email", summary="Update the current user's email")
def update_email(
    body: UpdateEmailIn,
    db: Session = Depends(get_db),
    current: CurrentUser = Depends(get_current_user),
):
    user = db.get(models.User, current.id)
    if not verify_password(body.current_password, user.password_hash):
        raise HTTPException(400, "Current password is incorrect.")
    new_email = body.new_email.strip()
    if not new_email:
        raise HTTPException(400, "Email cannot be empty.")
    if db.query(models.User).filter(models.User.email == new_email).first():
        raise HTTPException(409, "This email is already registered.")
    user.email = new_email
    db.commit()
    return {"message": "Email updated."}


@router.put("/password", summary="Update the current user's password")
def update_password(
    body: UpdatePasswordIn,
    response: Response,
    db: Session = Depends(get_db),
    current: CurrentUser = Depends(get_current_user),
):
    user = db.get(models.User, current.id)
    if not verify_password(body.current_password, user.password_hash):
        raise HTTPException(400, "Current password is incorrect.")
    validate_password_strength(body.new_password)
    check_password_reuse(db, user, body.new_password)
    record_password_change(db, user, body.new_password)
    # Changing the password invalidates old tokens (see auth.get_current_user's
    # iat check) — issue a fresh one so the current session isn't kicked out.
    set_auth_cookie(response, create_token(user))
    return {"message": "Password updated."}
