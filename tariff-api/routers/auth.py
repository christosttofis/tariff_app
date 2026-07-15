"""Auth router — login, forgot-password, reset-password endpoints."""

import os
import secrets
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

import email_utils
import models
from auth import (
    CurrentUser, check_password_reuse, create_pending_token, create_token, decode_pending_token,
    get_current_user, record_password_change, validate_password_strength, verify_password,
)
from database import get_db

router = APIRouter(prefix="/api/auth", tags=["auth"])

_BASE_URL = os.getenv("TARIFF_BASE_URL", "http://localhost:8000").rstrip("/")

_MAX_ATTEMPTS = 3       # failed logins before lockout
_LOCKOUT_MINUTES = 180  # how long the lockout lasts


def _log_login(db: Session, request: Request, *, email: str, user_id: int | None, success: bool, reason: str) -> None:
    db.add(models.LoginActivity(
        email=email,
        user_id=user_id,
        success=success,
        reason=reason,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        ts=datetime.now(timezone.utc).isoformat(),
    ))
    db.commit()


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


class UpdatePasswordIn(BaseModel):
    current_password: str
    new_password: str


@router.post("/login", summary="Exchange email + password for a JWT bearer token")
def login(body: LoginIn, request: Request, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == body.email).first()
    now = datetime.now(timezone.utc)

    # Check lockout before verifying password
    if user and user.locked_until:
        locked_until = datetime.fromisoformat(user.locked_until)
        if now < locked_until:
            _log_login(db, request, email=body.email, user_id=user.id, success=False, reason="locked")
            raise HTTPException(
                429,
                "Account locked due to too many failed attempts. "
                "Please try again later or contact your CERA administrator."
            )
        # Lockout period has expired — reset automatically
        user.failed_attempts = 0
        user.locked_until = None
        db.commit()

    if not user or not verify_password(body.password, user.password_hash):
        # Record failed attempt (only for existing accounts to avoid email enumeration)
        if user:
            user.failed_attempts = (user.failed_attempts or 0) + 1
            if user.failed_attempts >= _MAX_ATTEMPTS:
                # Lock the account and notify the user — only on the attempt that triggers it
                user.locked_until = (now + timedelta(minutes=_LOCKOUT_MINUTES)).isoformat()
                db.commit()
                email_utils.notify_account_locked(user.email, _LOCKOUT_MINUTES, user.role)
                _log_login(db, request, email=body.email, user_id=user.id, success=False, reason="locked_out")
                raise HTTPException(
                    429,
                    "Account locked due to too many failed attempts. "
                    "Please try again later or contact your CERA administrator."
                )
            else:
                remaining = _MAX_ATTEMPTS - user.failed_attempts
                db.commit()
                _log_login(db, request, email=body.email, user_id=user.id, success=False, reason="bad_password")
                raise HTTPException(
                    401,
                    f"Invalid email or password. "
                    f"{remaining} attempt(s) remaining before your account is locked."
                )
        _log_login(db, request, email=body.email, user_id=None, success=False, reason="unknown_email")
        raise HTTPException(401, "Invalid email or password")

    if not user.is_active:
        _log_login(db, request, email=body.email, user_id=user.id, success=False, reason="inactive")
        raise HTTPException(403, "Account is inactive — contact your CERA administrator")

    # Successful password check — clear any previous failed attempts
    user.failed_attempts = 0
    user.locked_until = None

    # Skip OTP entirely if disabled for this user (e.g. during testing)
    if not (user.otp_enabled if user.otp_enabled is not None else True):
        _log_login(db, request, email=user.email, user_id=user.id, success=True, reason="password_only")
        return {
            "access_token": create_token(user),
            "token_type": "bearer",
            "role": user.role,
            "supplier": user.supplier_name,
            "email": user.email,
        }

    # Generate 6-digit OTP, delete any existing codes for this email, store new one
    code = str(secrets.randbelow(900000) + 100000)
    db.query(models.OtpCode).filter(models.OtpCode.email == user.email).delete()
    expires = (now + timedelta(minutes=10)).isoformat()
    db.add(models.OtpCode(email=user.email, code=code, expires_at=expires, created_at=now.isoformat()))
    db.commit()

    email_utils.send_otp_code(user.email, code)

    return {
        "status": "otp_required",
        "pending_token": create_pending_token(user.email),
    }


@router.post("/verify-otp", summary="Verify OTP code and exchange for a full JWT")
def verify_otp(body: VerifyOtpIn, request: Request, db: Session = Depends(get_db)):
    email = decode_pending_token(body.pending_token)
    now_dt = datetime.now(timezone.utc)
    now = now_dt.isoformat()

    user = db.query(models.User).filter(models.User.email == email, models.User.is_active == True).first()
    if not user:
        _log_login(db, request, email=email, user_id=None, success=False, reason="user_not_found")
        raise HTTPException(401, "User not found or deactivated.")

    # Reuse the same failed_attempts/locked_until fields as password login — a
    # correct password already resets them to 0 before OTP starts, so guessing
    # the 6-digit code is bounded by the same lockout, not left uncapped.
    if user.locked_until:
        locked_until = datetime.fromisoformat(user.locked_until)
        if now_dt < locked_until:
            _log_login(db, request, email=email, user_id=user.id, success=False, reason="locked")
            raise HTTPException(
                429,
                "Account locked due to too many failed attempts. "
                "Please try again later or contact your CERA administrator."
            )
        user.failed_attempts = 0
        user.locked_until = None
        db.commit()

    rec = (
        db.query(models.OtpCode)
        .filter(models.OtpCode.email == email, models.OtpCode.used == False)
        .order_by(models.OtpCode.id.desc())
        .first()
    )
    if not rec or rec.expires_at < now or rec.code != body.code.strip():
        user.failed_attempts = (user.failed_attempts or 0) + 1
        if user.failed_attempts >= _MAX_ATTEMPTS:
            user.locked_until = (now_dt + timedelta(minutes=_LOCKOUT_MINUTES)).isoformat()
            db.commit()
            email_utils.notify_account_locked(user.email, _LOCKOUT_MINUTES, user.role)
            _log_login(db, request, email=email, user_id=user.id, success=False, reason="locked_out")
            raise HTTPException(
                429,
                "Account locked due to too many failed attempts. "
                "Please try again later or contact your CERA administrator."
            )
        remaining = _MAX_ATTEMPTS - user.failed_attempts
        db.commit()
        _log_login(db, request, email=email, user_id=user.id, success=False, reason="bad_otp")
        raise HTTPException(
            401,
            f"Invalid or expired verification code. "
            f"{remaining} attempt(s) remaining before your account is locked."
        )

    rec.used = True
    user.failed_attempts = 0
    user.locked_until = None
    db.commit()

    _log_login(db, request, email=user.email, user_id=user.id, success=True, reason="otp_verified")

    return {
        "access_token": create_token(user),
        "token_type": "bearer",
        "role": user.role,
        "supplier": user.supplier_name,
        "email": user.email,
    }


_OTP_RESEND_COOLDOWN_SECONDS = 120  # 2 minutes


@router.post("/resend-otp", summary="Resend OTP code (minimum 2 minutes between sends)")
def resend_otp(body: ResendOtpIn, db: Session = Depends(get_db)):
    email = decode_pending_token(body.pending_token)
    now = datetime.now(timezone.utc)

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

    code = str(secrets.randbelow(900000) + 100000)
    db.query(models.OtpCode).filter(models.OtpCode.email == email).delete()
    expires = (now + timedelta(minutes=10)).isoformat()
    db.add(models.OtpCode(email=email, code=code, expires_at=expires, created_at=now.isoformat()))
    db.commit()

    email_utils.send_otp_code(email, code)

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
        db.add(models.PasswordReset(token=token, email=body.email, expires_at=expires))
        db.commit()
        portal = "supplier" if user.role == "supplier" else "admin"
        reset_url = f"{_BASE_URL}/reset-password.html?token={token}&portal={portal}"
        email_utils.notify_password_reset(body.email, reset_url)
    # Always return the same message — don't reveal whether the email exists
    return {"message": "If this email is registered, a reset link has been sent."}


@router.post("/reset-password", summary="Set a new password using a reset token")
def reset_password(body: ResetPasswordIn, db: Session = Depends(get_db)):
    rec = db.get(models.PasswordReset, body.token)
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
    new_email = body.new_email.strip()
    if not new_email:
        raise HTTPException(400, "Email cannot be empty.")
    if db.query(models.User).filter(models.User.email == new_email).first():
        raise HTTPException(409, "This email is already registered.")
    user = db.get(models.User, current.id)
    user.email = new_email
    db.commit()
    return {"message": "Email updated."}


@router.put("/password", summary="Update the current user's password")
def update_password(
    body: UpdatePasswordIn,
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
    return {"message": "Password updated.", "access_token": create_token(user)}
