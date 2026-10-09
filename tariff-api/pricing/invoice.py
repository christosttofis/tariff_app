"""Sample-invoice generation. Originally a port of the old client-side
getSampleInvoicePeriod/buildSampleInvoiceData JS.

Reuses an already-computed monthly_breakdown()/monthly_kwh_display() result —
this module does not run its own cost calculation.
"""

import calendar
from datetime import date

from .regulated import get_tariff_fpa, mdm_for_tariff, regulated_breakdown


def get_sample_invoice_period(tariff: dict, input_mode: str, billing_period: int, window: list[tuple[int, int]]) -> dict:
    """The customer's first bill after switching: the first 1 or 2 months of
    the calculation window (the customer's own billing cycle in Monthly mode,
    the tariff's invoicing cadence in Annual mode)."""
    n = billing_period if input_mode == "monthly" else (tariff.get("mdmInvoiceMonths") or 2)
    first_y, first_mi = window[0]
    last_y, last_mi = window[n - 1]
    start_date = date(first_y, first_mi + 1, 1)
    end_date = date(last_y, last_mi + 1, calendar.monthrange(last_y, last_mi + 1)[1])
    return {"monthIndices": list(range(n)), "startDate": start_date.isoformat(), "endDate": end_date.isoformat()}


def build_sample_invoice_data(
    tariff: dict,
    mo_bd: list[dict | None],
    mo_kwh: list[float],
    annual_kwh: float,
    regulated_rates: dict,
    supplier_regulated: bool,
    input_mode: str,
    billing_period: int,
    window: list[tuple[int, int]],
) -> dict | None:
    if not mo_bd or all(v is None for v in mo_bd):
        return None
    period = get_sample_invoice_period(tariff, input_mode, billing_period, window)
    month_indices = period["monthIndices"]
    if any(mo_bd[mi] is None for mi in month_indices):
        return None

    energy = sum(mo_bd[mi]["energy"] for mi in month_indices)
    fpa = sum(mo_bd[mi]["fpa"] for mi in month_indices)
    standing = sum(mo_bd[mi]["standing"] for mi in month_indices)
    energy_full = sum(mo_bd[mi].get("energyFull", mo_bd[mi]["energy"]) for mi in month_indices)
    fpa_full = sum(mo_bd[mi].get("fpaFull", mo_bd[mi]["fpa"]) for mi in month_indices)
    standing_full = sum(mo_bd[mi].get("standingFull", mo_bd[mi]["standing"]) for mi in month_indices)

    period_kwh = sum(mo_kwh[mi] or 0 for mi in month_indices)

    mdm = mdm_for_tariff(tariff, supplier_regulated, regulated_rates)
    reg_bd = regulated_breakdown(
        tariff.get("voltage"), annual_kwh, mdm, tariff.get("mdmInvoiceMonths"), supplier_regulated, regulated_rates
    )
    frac = len(month_indices) / 12
    grid = reg_bd["grid"]["annual"] * frac
    pso = reg_bd["pso"]["annual"] * frac
    res = reg_bd["res"]["annual"] * frac
    mdm_amt = reg_bd["mdm"]["annual"] * frac

    supplier_total = energy + fpa + standing
    vat_base = supplier_total + grid + pso + mdm_amt
    vat = vat_base * 0.19
    total_before_vat = vat_base + res
    amount_due = total_before_vat + vat

    energy_rate = energy_full / period_kwh if period_kwh > 0 else 0
    mdm_invoices = len(month_indices) / (tariff.get("mdmInvoiceMonths") or 2)

    is_tou = tariff.get("pricing") == "ToU"
    peak_kwh = sum(mo_bd[mi].get("peakKwh", 0) for mi in month_indices) if is_tou else 0
    off_peak_kwh = sum(mo_bd[mi].get("offPeakKwh", 0) for mi in month_indices) if is_tou else 0
    peak_energy = sum(mo_bd[mi].get("peakEnergy", 0) for mi in month_indices) if is_tou else 0
    off_peak_energy = sum(mo_bd[mi].get("offPeakEnergy", 0) for mi in month_indices) if is_tou else 0
    peak_energy_full = sum(mo_bd[mi].get("peakEnergyFull", 0) for mi in month_indices) if is_tou else 0
    off_peak_energy_full = sum(mo_bd[mi].get("offPeakEnergyFull", 0) for mi in month_indices) if is_tou else 0
    peak_rate = peak_energy_full / peak_kwh if peak_kwh > 0 else 0
    off_peak_rate = off_peak_energy_full / off_peak_kwh if off_peak_kwh > 0 else 0

    return {
        "startDate": period["startDate"], "endDate": period["endDate"], "monthsCount": len(month_indices),
        "periodKwh": period_kwh,
        "fpaRate": get_tariff_fpa(tariff, regulated_rates),
        "energy": energy, "fpa": fpa, "standing": standing,
        "energyFull": energy_full, "fpaFull": fpa_full, "standingFull": standing_full,
        "supplierTotal": supplier_total,
        "grid": grid, "pso": pso, "res": res, "mdm": mdm_amt, "mdmRegulated": bool(reg_bd["mdm"]["regulated"]),
        "energyRate": energy_rate, "gridRate": reg_bd["grid"]["rate"], "psoRate": reg_bd["pso"]["rate"],
        "resRate": reg_bd["res"]["rate"], "mdmRate": reg_bd["mdm"]["rate"], "mdmInvoices": mdm_invoices,
        "vatBase": vat_base, "vat": vat, "totalBeforeVat": total_before_vat, "amountDue": amount_due,
        "isToU": is_tou,
        "peakKwh": peak_kwh, "offPeakKwh": off_peak_kwh,
        "peakEnergy": peak_energy, "offPeakEnergy": off_peak_energy,
        "peakEnergyFull": peak_energy_full, "offPeakEnergyFull": off_peak_energy_full,
        "peakRate": peak_rate, "offPeakRate": off_peak_rate,
    }
