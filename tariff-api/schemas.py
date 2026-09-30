"""Pydantic request/response schemas for admin API endpoints."""

from __future__ import annotations

import re
from typing import Any, Literal

from email_validator import EmailNotValidError, validate_email
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator

from config import TARIFF_MAX_ENERGY_RATE, TARIFF_MAX_MONTHLY_CHARGE

_URL_RE = re.compile(r"^https?://", re.IGNORECASE)

# Shared constraint for customer-supplied consumption figures (annualKwh/
# monthlyKwh on the public calculate/sample-invoice endpoints): reject NaN/
# Infinity (valid JSON per the spec's producers, but not real floats — Pydantic
# doesn't reject them by default and they crash the pricing engine downstream)
# and cap at a generous but sane upper bound so a bogus huge value can't
# produce absurd output instead of a clean validation error.
_KWH_FIELD = Field(default=0, ge=0, le=5_000_000, allow_inf_nan=False)


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
    regulated: bool = False

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


# ── Tariff pricing data ──────────────────────────────────────────────────────
# `rates` and `discounts` are fed straight into the public calculator
# (pricing/engine.py), so they are validated as strictly as the fixed fields:
# numbers only (no text, NaN or Infinity), within sane bounds. A single
# malformed approved tariff would otherwise break /api/public/calculate for
# every customer. Limits come from config.py (TARIFF_MAX_*), adjustable
# without a code change. Unknown keys are dropped rather than stored.

def _energy(default: float | None = 0.0, *, lo: float = 0.0):
    """A €/kWh value."""
    return Field(default, ge=lo, le=TARIFF_MAX_ENERGY_RATE, allow_inf_nan=False)


def _monthly(default: float | None = 0.0):
    """A €/month (or €/period) charge."""
    return Field(default, ge=0, le=TARIFF_MAX_MONTHLY_CHARGE, allow_inf_nan=False)


class _RatesBase(BaseModel):
    model_config = ConfigDict(extra="ignore")


class FixedRatesIn(_RatesBase):
    rate: float = _energy()


class TouRatesIn(_RatesBase):
    # High-season months (1–12, inclusive); 0/0 means no high season.
    hiStart: int = Field(0, ge=0, le=12)
    hiEnd: int = Field(0, ge=0, le=12)
    # Peak windows as hours of the day, [start, end).
    hiPeakStart: float = Field(0, ge=0, le=24, allow_inf_nan=False)
    hiPeakEnd: float = Field(0, ge=0, le=24, allow_inf_nan=False)
    loPeakStart: float = Field(0, ge=0, le=24, allow_inf_nan=False)
    loPeakEnd: float = Field(0, ge=0, le=24, allow_inf_nan=False)
    hiPeakRate: float = _energy()
    hiOffRate: float = _energy()
    loPeakRate: float = _energy()
    loOffRate: float = _energy()


class DynamicRatesIn(_RatesBase):
    # Effective price = max(DAM, damFloor) × mult + adder
    mult: float = Field(1.0, gt=0, le=10, allow_inf_nan=False)
    adder: float = _energy(lo=-TARIFF_MAX_ENERGY_RATE)
    damFloor: float | None = _energy(None)


class TierIn(_RatesBase):
    upTo: float | None = Field(None, gt=0, le=10_000_000, allow_inf_nan=False)   # kWh; null = no upper bound
    rate: float = _energy()
    fixedCharge: float | None = _monthly(None)


class VariableRatesIn(_RatesBase):
    resetMonths: int = Field(2, ge=1, le=12)
    tiers: list[TierIn] = Field(..., min_length=1, max_length=20)

    @model_validator(mode="after")
    def _tiers_ascending(self):
        caps = [t.upTo for t in self.tiers]
        if any(c is None for c in caps[:-1]):
            raise ValueError("only the last tier may have no upper limit")
        bounded = [c for c in caps if c is not None]
        if any(b <= a for a, b in zip(bounded, bounded[1:])):
            raise ValueError("tier limits must be strictly increasing")
        return self


_RATES_MODEL = {"Fixed": FixedRatesIn, "ToU": TouRatesIn, "Dynamic": DynamicRatesIn, "Variable": VariableRatesIn}


class DiscountIn(BaseModel):
    model_config = ConfigDict(extra="ignore")

    type: Literal["energy", "standing"]
    percentage: float = Field(..., gt=0, le=100, allow_inf_nan=False)
    durationMonths: int | None = Field(None, ge=1, le=120)   # null = permanent
    conditions: str = Field("", max_length=500)


class TariffIn(BaseModel):
    id: str | None = Field(None, max_length=100)
    name: str = Field(..., max_length=200)
    supplier: str = Field(..., max_length=200)
    contract: Literal["Domestic", "Commercial", "Industrial"]
    voltage: Literal["LV", "MV", "HV"]
    pricing: Literal["Fixed", "ToU", "Dynamic", "Variable"]
    standing: float = _monthly()
    mdm: float = _monthly()
    mdmSource: Literal["global", "custom"] = "custom"
    mdmInvoiceMonths: Literal[1, 2] = 2
    rates: dict[str, Any] = {}
    profileId: str | None = Field(None, max_length=100)
    fpaSource: Literal["global", "custom", "none"] = "global"
    # Fuel adjustment can legitimately be negative.
    fpaCustom: float = _energy(lo=-TARIFF_MAX_ENERGY_RATE)
    durationMonths: int | None = Field(None, ge=1, le=120)
    loadEntitlement: Literal["any", "lt70", "gt70"] | None = None
    discounts: list[DiscountIn] = Field([], max_length=20)
    vulnerable: bool = False
    createdAt: str | None = None
    updatedAt: str | None = None

    @model_validator(mode="after")
    def _validate_rates(self):
        """Validate `rates` against the model for this tariff's pricing type and
        replace it with the cleaned (typed, unknown-keys-dropped) version."""
        try:
            parsed = _RATES_MODEL[self.pricing].model_validate(self.rates)
        except ValidationError as e:
            problems = "; ".join(
                f"{'.'.join(str(p) for p in err['loc']) or 'rates'}: {err['msg']}" for err in e.errors()
            )
            raise ValueError(f"invalid {self.pricing} rates — {problems}") from None
        self.rates = parsed.model_dump()
        return self


class TariffStatusIn(BaseModel):
    status: Literal["draft", "pending", "approved", "rejected", "suspended", "archived"]
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


class SampleInvoiceConfigIn(BaseModel):
    enabled: bool


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


_REPORT_CATEGORIES = ("incorrect_price", "terms_mismatch", "broken_link", "other")


def _check_email_required(v: str) -> str:
    if not v or not v.strip():
        raise ValueError("email is required")
    try:
        validate_email(v, check_deliverability=False)
    except EmailNotValidError as e:
        raise ValueError(f"invalid email address: {e}") from e
    return v


def _check_note_required(v: str) -> str:
    if not v or not v.strip():
        raise ValueError("note is required")
    return v


class TariffReportIn(BaseModel):
    # None = a general site issue, not tied to any one tariff (customer.html's
    # footer "Report a general issue" link) — tariff/supplier are looked up
    # server-side below only when this is set.
    tariff_id: str | None = Field(None, max_length=100)
    category: Literal[_REPORT_CATEGORIES] = "other"
    note: str = Field(..., max_length=2000)
    reporter_email: str = Field(..., max_length=254)

    _validate_reporter_email = field_validator("reporter_email")(_check_email_required)
    _validate_note = field_validator("note")(_check_note_required)


class TariffReportStatusIn(BaseModel):
    status: Literal["open", "reviewed", "resolved", "dismissed"]
    admin_note: str | None = Field(None, max_length=2000)


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


class PublicCalculateIn(BaseModel):
    """Inputs for POST /api/public/calculate — mirrors exactly what
    customer.html's applyFilters() derives from the DOM/window state before
    running its (now server-side) cost engine. See
    SECURITY_REMEDIATION_PLAN_customer_data_exposure.md."""
    customerType: Literal["domestic", "ci"]
    voltage: Literal["LV", "MV", "HV"] = "LV"
    loadEntitlement: Literal["lt70", "gt70"] | None = None
    pricingFilter: Literal["All", "Fixed", "ToU", "Variable", "Dynamic"] = "All"
    vulnerableEligible: bool = False
    offersEnabled: bool = True
    inputMode: Literal["annual", "monthly"]
    annualKwh: float = _KWH_FIELD
    monthlyKwh: float = _KWH_FIELD
    billingPeriod: Literal[1, 2] = 1
    # {tariffId: {"<tariffId>_disc_<index>": bool}} — same shape as the
    # client's existing window._discountState.
    discountOverrides: dict[str, dict[str, bool]] = {}


class PublicSampleInvoiceIn(BaseModel):
    tariffId: str = Field(..., max_length=100)
    inputMode: Literal["annual", "monthly"]
    annualKwh: float = _KWH_FIELD
    monthlyKwh: float = _KWH_FIELD
    billingPeriod: Literal[1, 2] = 1
    offersEnabled: bool = True
    discountOverrides: dict[str, dict[str, bool]] = {}
