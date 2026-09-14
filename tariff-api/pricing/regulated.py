"""CERA-regulated charges: grid usage, PSO, RES, MDM, and FPA.

Direct port of getRegulated/mdmForTariff/getTariffFpa/regulatedBreakdown in
customer.html (~lines 1361-1467).
"""


def get_regulated_rates(reg: dict | None) -> dict:
    r = reg or {}
    return {
        "lv": r.get("lv") or 0,
        "mv": r.get("mv") or 0,
        "hv": r.get("hv") or 0,
        "fpaLV": r.get("fpaLV") or r.get("fpa") or 0,
        "fpaMV": r.get("fpaMV") or r.get("fpa") or 0,
        "fpaHV": r.get("fpaHV") or r.get("fpa") or 0,
        "pso": r.get("pso") or 0,
        "res": r.get("res") or 0,
        "mdm": r.get("mdm") or 0,
    }


def mdm_for_tariff(tariff: dict, supplier_regulated: bool, regulated_rates: dict) -> float:
    if supplier_regulated:
        return regulated_rates.get("mdm") or 0
    return tariff.get("mdm") or 0


def get_tariff_fpa(tariff: dict, regulated_rates: dict) -> float:
    src = tariff.get("fpaSource") or "global"
    if src == "none":
        return 0
    if src == "custom":
        return tariff.get("fpaCustom") or 0
    voltage = tariff.get("voltage") or "LV"
    if voltage == "LV":
        return regulated_rates["fpaLV"]
    if voltage == "MV":
        return regulated_rates["fpaMV"]
    return regulated_rates["fpaHV"]


def regulated_breakdown(
    voltage: str,
    annual_kwh: float,
    mdm: float,
    mdm_invoice_months: int | None,
    mdm_regulated: bool,
    regulated_rates: dict,
) -> dict:
    grid_rate = regulated_rates["lv"] if voltage == "LV" else (regulated_rates["mv"] if voltage == "MV" else regulated_rates["hv"])
    mdm_val = mdm or 0
    invoices_per_year = 12 / (mdm_invoice_months or 2)
    pso = regulated_rates["pso"]
    res = regulated_rates["res"]
    return {
        "grid": {"label": "REGULATED_GRID", "annual": annual_kwh * grid_rate, "rate": grid_rate, "perKwh": True, "regulated": True},
        "pso": {"label": "REGULATED_PSO", "annual": annual_kwh * pso, "rate": pso, "perKwh": True, "regulated": True},
        "res": {"label": "REGULATED_RES", "annual": annual_kwh * res, "rate": res, "perKwh": True, "regulated": True},
        "mdm": {
            "label": "REGULATED_MDM" if mdm_regulated else "MDM_SUPPLIER",
            "annual": mdm_val * invoices_per_year,
            "rate": mdm_val,
            "perKwh": False,
            "invoiceMonths": mdm_invoice_months or 2,
            "regulated": bool(mdm_regulated),
        },
        "total": annual_kwh * (grid_rate + pso + res) + mdm_val * invoices_per_year,
    }
