"""Pydantic request/response schemas for admin API endpoints."""

from __future__ import annotations

import re
from typing import Any, Literal

from email_validator import EmailNotValidError, validate_email
from pydantic import BaseModel, Field, field_validator

_URL_RE = re.compile(r"^https?://", re.IGNORECASE)


def _check_email(v: str) -> str:
    """Allows an empty string (field not filled in); validates format otherwise."""
    if not v:
        return v
    try:
        validate_email(v, check_deliverability=False)
    except EmailNotValidError as e:
        raise ValueError(f"invalid email address: {e}") from e
    return v


def _check_url(v: str) -> str:
    """Allows an empty string; otherwise requires an http(s) scheme (blocks
    javascript:/data: injection at the source, not just at render time)."""
    if v and not _URL_RE.match(v):
        raise ValueError("website must start with http:// or https://")
    return v


class SupplierIn(BaseModel):
    name: str = Field(..., max_length=200)
    licence: str = Field("", max_length=100)
    address: str = Field("", max_length=500)
    website: str = Field("", max_length=500)
    email: str = Field("", max_length=254)
    tel: str = Field("", max_length=50)

    _validate_email = field_validator("email")(_check_email)
    _validate_website = field_validator("website")(_check_url)


class ProfileIn(BaseModel):
    id: str | None = Field(None, max_length=100)
    name: str = Field(..., max_length=200)
    desc: str = Field("", max_length=2000)
    months: list[Any] = []         # 12 × {W:[48 floats], NW:[48 floats], hasW, hasNW}
    covW: int = 0
    covNW: int = 0
    rows: int = 0
    colCount: int = 0


class TariffIn(BaseModel):
    id: str | None = Field(None, max_length=100)
    name: str = Field(..., max_length=200)
    supplier: str = Field(..., max_length=200)
    contract: Literal["Domestic", "Commercial", "Industrial"]
    voltage: Literal["LV", "MV", "HV"]
    pricing: Literal["Fixed", "ToU", "Dynamic", "Variable"]
    standing: float = 0.0
    mdm: float = 0.0
    rates: dict[str, Any] = {}
    profileId: str | None = Field(None, max_length=100)
    fpaSource: Literal["global", "custom", "none"] = "global"
    fpaCustom: float = 0.0
    durationMonths: int | None = Field(None, ge=1, le=120)
    loadEntitlement: Literal["any", "lt70", "gt70"] | None = None
    discounts: list[Any] = []
    vulnerable: bool = False
    createdAt: str | None = None
    updatedAt: str | None = None


class TariffStatusIn(BaseModel):
    status: Literal["draft", "pending", "approved", "rejected", "suspended"]
    reason: str | None = Field(None, max_length=1000)  # rejection reason (only used when status=rejected)


class CreateUserIn(BaseModel):
    email: str = Field(..., max_length=254)
    supplier_name: str = Field(..., max_length=200)

    _validate_email = field_validator("email")(_check_email)


class UserStatusIn(BaseModel):
    is_active: bool


class UserOtpToggleIn(BaseModel):
    otp_enabled: bool


class RegulatedIn(BaseModel):
    lv: float = 0.0
    mv: float = 0.0
    hv: float = 0.0
    fpaLV: float = 0.0
    fpaMV: float = 0.0
    fpaHV: float = 0.0
    pso: float = 0.0
    res: float = 0.0
    mdm: float = 0.0


class NoticesIn(BaseModel):
    assumptions_en: str = Field("", max_length=50000)
    assumptions_el: str = Field("", max_length=50000)
    legal_en: str = Field("", max_length=50000)
    legal_el: str = Field("", max_length=50000)
    vulnerable_en: str = Field("", max_length=50000)
    vulnerable_el: str = Field("", max_length=50000)


class MessageIn(BaseModel):
    subject: str = Field(..., max_length=200)
    body: str = Field(..., max_length=20000)
    audience: Literal["all", "selected"]
    target_suppliers: list[str] = []


class MessageArchiveIn(BaseModel):
    archived: bool


class ScheduledNotificationIn(BaseModel):
    subject: str = Field(..., max_length=200)
    body: str = Field(..., max_length=20000)
    audience: Literal["all", "selected"]
    target_suppliers: list[str] = []
    interval_months: int = Field(..., ge=1, le=60)
    start_date: str | None = None   # YYYY-MM-DD; defaults to today


class ScheduledNotificationEnabledIn(BaseModel):
    enabled: bool


class DamIn(BaseModel):
    damMonthly: list[Any]          # [null|float × 12]
    damBySlot: list[Any] = []      # [[float × 48] × 12]
    damDailyData: list[Any] = []   # [[{dateStr,dow,slots}...] × 12]
    damRowCount: int = 0
    damYear: int = 2026
