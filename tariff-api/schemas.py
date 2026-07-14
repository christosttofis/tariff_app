"""Pydantic request/response schemas for admin API endpoints."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class SupplierIn(BaseModel):
    name: str
    licence: str = ""
    address: str = ""
    website: str = ""
    email: str = ""
    tel: str = ""


class ProfileIn(BaseModel):
    id: str | None = None          # if omitted the server generates one
    name: str
    desc: str = ""
    months: list[Any] = []         # 12 × {W:[48 floats], NW:[48 floats], hasW, hasNW}
    covW: int = 0
    covNW: int = 0
    rows: int = 0
    colCount: int = 0


class TariffIn(BaseModel):
    id: str | None = None          # if omitted the server generates one
    name: str
    supplier: str
    contract: str                  # Domestic | Commercial | Industrial
    voltage: str                   # LV | MV | HV
    pricing: str                   # Fixed | ToU | Dynamic | Variable
    standing: float = 0.0
    mdm: float = 0.0
    rates: dict[str, Any] = {}
    profileId: str | None = None
    fpaSource: str = "global"      # global | custom | none
    fpaCustom: float = 0.0
    durationMonths: int | None = None
    loadEntitlement: str | None = None
    discounts: list[Any] = []
    vulnerable: bool = False
    createdAt: str | None = None
    updatedAt: str | None = None


class TariffStatusIn(BaseModel):
    status: str                    # draft | pending | approved | rejected
    reason: str | None = None      # rejection reason (only used when status=rejected)


class CreateUserIn(BaseModel):
    email: str
    supplier_name: str


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
    assumptions_en: str = ""
    assumptions_el: str = ""
    legal_en: str = ""
    legal_el: str = ""
    vulnerable_en: str = ""
    vulnerable_el: str = ""


class MessageIn(BaseModel):
    subject: str
    body: str
    audience: str                  # all | selected
    target_suppliers: list[str] = []


class MessageArchiveIn(BaseModel):
    archived: bool


class ScheduledNotificationIn(BaseModel):
    subject: str
    body: str
    audience: str                   # all | selected
    target_suppliers: list[str] = []
    interval_months: int
    start_date: str | None = None   # YYYY-MM-DD; defaults to today


class ScheduledNotificationEnabledIn(BaseModel):
    enabled: bool


class DamIn(BaseModel):
    damMonthly: list[Any]          # [null|float × 12]
    damBySlot: list[Any] = []      # [[float × 48] × 12]
    damDailyData: list[Any] = []   # [[{dateStr,dow,slots}...] × 12]
    damRowCount: int = 0
    damYear: int = 2026
