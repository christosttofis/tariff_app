"""Pydantic request/response schemas for admin API endpoints."""

from __future__ import annotations

import math
import re
from datetime import date
from typing import Annotated, Any, Literal

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

# Client-chosen record IDs (tariffs, profiles): letters, digits, '-' and '_' only.
# The pages put IDs into links, attributes and (on pages not yet converted to the
# strict CSP) click handlers; a quote or bracket in a supplier-chosen ID broke out
# of the customer page's handler and ran code (SECURITY_REMEDIATION_CHECKLIST.md, Round 18).
_ID_PATTERN = r"^[A-Za-z0-9_-]+$"


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


# ── Consumption (load) profiles ──────────────────────────────────────────────
# Profiles drive every tariff's cost in the public calculator, so one bad value
# (text, NaN, a nested object) silently empties the customer's results. Shape
# matches what admin.html builds from the EAC CSV: 12 months x 48 half-hourly
# working-day (W) and non-working-day (NW) values. Real profiles hold small
# non-negative factors (~0.03-0.3); the cap only rejects absurd values.
# strict=True: numbers must be JSON numbers, not numeric-looking strings.
_HH_VALUE = Field(ge=0, le=1_000_000, allow_inf_nan=False, strict=True)


class ProfileMonthIn(BaseModel):
    model_config = ConfigDict(extra="ignore")

    W: list[Annotated[float, _HH_VALUE]] = Field(..., min_length=48, max_length=48)
    NW: list[Annotated[float, _HH_VALUE]] = Field(..., min_length=48, max_length=48)
    hasW: bool
    hasNW: bool


class ProfileIn(BaseModel):
    id: str | None = Field(None, max_length=100, pattern=_ID_PATTERN)
    name: str = Field(..., max_length=200)
    desc: str = Field("", max_length=2000)
    months: list[ProfileMonthIn] = Field(..., min_length=12, max_length=12)
    covW: int = Field(0, ge=0, le=12)
    covNW: int = Field(0, ge=0, le=12)
    rows: int = Field(0, ge=0, le=1_000_000)
    colCount: int = Field(0, ge=0, le=10_000)


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
    id: str | None = Field(None, max_length=100, pattern=_ID_PATTERN)
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
    # These feed every tariff's cost in the public calculator. Without limits, a
    # negative or huge value showed absurd totals, NaN was silently dropped, and
    # Infinity was stored and then crashed both the calculator and this admin
    # page (SECURITY_REMEDIATION_CHECKLIST.md, Round 19).
    lv: float = _energy()       # network charges, €/kWh
    mv: float = _energy()
    hv: float = _energy()
    fpaLV: float = _energy(lo=-TARIFF_MAX_ENERGY_RATE)   # fuel adjustment can be negative
    fpaMV: float = _energy(lo=-TARIFF_MAX_ENERGY_RATE)
    fpaHV: float = _energy(lo=-TARIFF_MAX_ENERGY_RATE)
    pso: float = _energy()
    res: float = _energy()
    mdm: float = _monthly()     # €/month

    # Grid usage always falls with voltage (LV > MV > HV); a value out of that
    # order is a typing mistake. FPA is not checked here: when it goes negative
    # the order flips, so the admin page only asks for confirmation.
    @field_validator("mv", "hv")
    @classmethod
    def _grid_falls_with_voltage(cls, v, info):
        higher = {"mv": "lv", "hv": "mv"}[info.field_name]
        above = info.data.get(higher)
        if above is not None and not v < above:
            raise ValueError(f"{info.field_name.upper()} grid usage must be lower than {higher.upper()}")
        return v


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
    tariff_id: str | None = Field(None, max_length=100, pattern=_ID_PATTERN)
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


# DAM prices are stored in €/kWh. Anything above 10 €/kWh (10,000 €/MWh) or
# below -1 €/kWh is not a market price - most likely a file uploaded with the
# wrong unit selected. 7,400 days is 20 years of history.
DAM_PRICE_MIN, DAM_PRICE_MAX = -1.0, 10.0
DAM_MAX_DAYS = 7400
_DAM_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_DAM_DAY_KEYS = {"dateStr", "month", "dow", "slots"}


def _dam_price_ok(v) -> bool:
    return v is None or (isinstance(v, (int, float)) and not isinstance(v, bool)
                         and math.isfinite(v) and DAM_PRICE_MIN <= v <= DAM_PRICE_MAX)


def _dam_problems(m: "DamIn") -> list[str]:
    """Every way the dataset differs from what the admin page / TSOC fetch build
    (admin.js parseDAM, dam_tsoc.build_dam_payload). Stops early on a flood."""
    out: list[str] = []
    bad_price = (f"must be numbers from {DAM_PRICE_MIN:g} to {DAM_PRICE_MAX:g} €/kWh "
                 "(was the right price unit selected?)")

    if len(m.damMonthly) != 12:
        out.append("damMonthly must have 12 months.")
    elif not all(_dam_price_ok(v) for v in m.damMonthly):
        out.append("damMonthly: monthly averages " + bad_price)

    if len(m.damBySlot) not in (0, 12):
        out.append("damBySlot must have 12 months.")
    else:
        for mi, month in enumerate(m.damBySlot):
            if not isinstance(month, list) or len(month) != 48:
                out.append(f"damBySlot month {mi + 1} must have 48 half-hours.")
            elif not all(_dam_price_ok(v) for v in month):
                out.append(f"damBySlot month {mi + 1}: half-hour averages " + bad_price)

    if len(m.damDailyData) not in (0, 12):
        out.append("damDailyData must have 12 months.")
        return out
    seen: set[str] = set()
    for mi, month in enumerate(m.damDailyData):
        if not isinstance(month, list):
            out.append(f"damDailyData month {mi + 1} must be a list of days.")
            continue
        for day in month:
            if len(out) >= 10:
                return out
            if not isinstance(day, dict) or not set(day) <= _DAM_DAY_KEYS or not {"dateStr", "slots"} <= set(day):
                out.append(f"damDailyData month {mi + 1}: each day needs dateStr and slots only.")
                continue
            ds = day["dateStr"]
            try:
                d = date.fromisoformat(ds) if isinstance(ds, str) and _DAM_DATE_RE.match(ds) else None
            except ValueError:
                d = None
            if d is None:
                out.append(f"damDailyData month {mi + 1}: {str(ds)[:20]!r} is not a date.")
                continue
            if d.month != mi + 1 or day.get("month", mi) != mi:
                out.append(f"{ds} is filed under the wrong month.")
            if ds in seen:
                out.append(f"{ds} appears twice.")
            seen.add(ds)
            dow = day.get("dow", 0)
            if not isinstance(dow, int) or isinstance(dow, bool) or not 0 <= dow <= 6:
                out.append(f"{ds}: dow must be 0-6.")
            slots = day["slots"]
            if not isinstance(slots, list) or len(slots) != 48:
                out.append(f"{ds}: must have 48 half-hours.")
            elif not all(_dam_price_ok(v) for v in slots):
                out.append(f"{ds}: prices " + bad_price)
    if len(seen) > DAM_MAX_DAYS:
        out.append(f"Too many days ({len(seen)}); at most {DAM_MAX_DAYS}.")
    return out


class DamIn(BaseModel):
    damMonthly: list[Any]          # [null|float × 12]
    damBySlot: list[Any] = []      # [[float × 48] × 12]
    damDailyData: list[Any] = []   # [[{dateStr,month,dow,slots}...] × 12]
    damRowCount: int = Field(0, ge=0, le=DAM_MAX_DAYS * 48 * 4)   # uploads may repeat rows
    damYear: int = Field(2026, ge=2000, le=2100)
    source: Literal["upload", "tsoc"] = "upload"   # recorded in the DAM change log

    @model_validator(mode="after")
    def _check_dataset(self):
        problems = _dam_problems(self)
        if problems:
            raise ValueError(" ".join(problems))
        return self


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
