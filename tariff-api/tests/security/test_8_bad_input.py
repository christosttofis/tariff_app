"""8. Bad files and absurd values.

Uploads must be real PDFs within the size limit and can't choose where they
are stored. Prices, consumption and profiles must be sensible numbers. And no
input, however malformed, may crash the server (HTTP 500).
"""
import copy
import json
import re

import pytest

PDF = b"%PDF-1.4\n%%EOF\n"
CALC = {"customerType": "domestic", "inputMode": "annual", "annualKwh": 4000}


@pytest.fixture(scope="module")
def tariff_body(acme):
    t = acme.get("/api/supplier/tariffs").json()[0]
    return {k: v for k, v in t.items() if k not in ("id", "status", "createdAt", "updatedAt",
                                                    "rejection_reason", "hasDocs", "everPublished")}


@pytest.fixture(scope="module")
def own_tariff(acme, tariff_body):
    # A separate pending tariff: an upload to a live one rightly sends it back for review.
    r = acme.post("/api/supplier/tariffs", json={**tariff_body, "name": "upload target"})
    assert r.status_code == 201
    return r.json()


# ── Uploads ──────────────────────────────────────────────────────────────────
@pytest.mark.parametrize("name, content", [
    ("terms.pdf", b"MZ\x90\x00 this is a Windows program"),
    ("terms.pdf", b"<html><script>alert(1)</script></html>"),
    ("terms.exe", PDF),
    ("terms.pdf.html", PDF),
    ("terms.pdf", b""),
    ("terms.pdf", b"%PDF" + b"0" * (10 * 1024 * 1024)),        # just over 10 MB
], ids=["exe-renamed", "html-renamed", "exe-name", "double-extension", "empty", "over-10MB"])
def test_only_real_pdfs_within_the_limit_are_accepted(app, acme, own_tariff, name, content):
    before = set(app.upload_dir.iterdir())
    r = acme.post(f"/api/supplier/tariffs/{own_tariff['id']}/documents",
                  files={"file": (name, content, "application/pdf")})
    assert r.status_code == 400
    assert set(app.upload_dir.iterdir()) == before, "a refused file was still written to disk"


@pytest.mark.parametrize("name", ["../../evil.pdf", "..\\..\\evil.pdf", "/etc/evil.pdf", "C:\\Windows\\evil.pdf"])
def test_uploaded_file_name_cannot_choose_where_it_is_stored(app, acme, own_tariff, name):
    before = set(app.upload_dir.iterdir())
    r = acme.post(f"/api/supplier/tariffs/{own_tariff['id']}/documents",
                  files={"file": (name, PDF, "application/pdf")})
    assert r.status_code in (201, 400)
    new = set(app.upload_dir.iterdir()) - before
    assert all(re.fullmatch(r"[0-9a-f]{32}\.pdf", p.name) for p in new), f"unexpected stored names: {new}"
    assert not list(app.upload_dir.parent.parent.rglob("evil.pdf")), "file escaped the uploads folder"


# ── Tariff prices ────────────────────────────────────────────────────────────
BAD_TARIFF = {
    "negative rate": {"rates": {"rate": -5}},
    "rate above 5 €/kWh": {"rates": {"rate": 5.01}},
    "rate 1e300": {"rates": {"rate": 1e300}},
    "rate as text": {"rates": {"rate": "cheap"}},
    "rate as object": {"rates": {"rate": {"x": 1}}},
    "standing above 1000 €/month": {"standing": 1000.01},
    "negative standing": {"standing": -1},
    "discount 150%": {"discounts": [{"type": "energy", "percentage": 150}]},
    "discount -300%": {"discounts": [{"type": "energy", "percentage": -300}]},
    "21 discounts": {"discounts": [{"type": "energy", "percentage": 1}] * 21},
    "ToU hour 25": {"pricing": "ToU", "rates": {"hiPeakStart": 25}},
    "Variable tiers out of order": {"pricing": "Variable", "rates": {"tiers": [
        {"upTo": 2000, "rate": 0.1}, {"upTo": 1000, "rate": 0.2}, {"upTo": None, "rate": 0.3}]}},
    "unknown contract type": {"contract": "Free"},
    "name 10,000 characters": {"name": "x" * 10_000},
    "unknown profile": {"profileId": "no-such-profile"},
}


@pytest.mark.parametrize("label", BAD_TARIFF)
def test_absurd_tariff_values_are_refused(acme, admin, tariff_body, label):
    body = {**tariff_body, **BAD_TARIFF[label]}
    assert acme.post("/api/supplier/tariffs", json=body).status_code == 422
    assert admin.post("/api/admin/tariffs", json=body).status_code == 422


@pytest.mark.parametrize("token", ["NaN", "Infinity", "-Infinity"])
def test_not_a_number_prices_are_refused(acme, tariff_body, token):
    raw = json.dumps({**tariff_body, "standing": 1.2345}).replace("1.2345", token)
    r = acme.post("/api/supplier/tariffs", data=raw, headers={"Content-Type": "application/json"})
    assert r.status_code == 422


# ── Public calculator ────────────────────────────────────────────────────────
@pytest.mark.parametrize("change", [
    {"annualKwh": -1}, {"annualKwh": 5_000_001}, {"annualKwh": "lots"}, {"annualKwh": 1e308},
    {"customerType": "hacker"}, {"inputMode": None}, {"billingPeriod": 99},
], ids=lambda c: next(iter(c)) + "=" + str(next(iter(c.values()))))
def test_absurd_consumption_is_refused(app, change):
    assert app.anon().post("/api/public/calculate", json={**CALC, **change}).status_code == 422


def test_calculator_still_works_after_all_that(app):
    r = app.anon().post("/api/public/calculate", json=CALC)
    assert r.status_code == 200 and r.json()["results"]


# ── Consumption profiles (admin) ─────────────────────────────────────────────
def _set(v):
    return lambda p: p["months"][2]["W"].__setitem__(5, v)


BAD_PROFILE = {
    "text value": _set("1.0 AND 1=1"),
    "negative value": _set(-0.5),
    "absurd value": _set(1e300),
    "missing value": _set(None),
    "47 half-hours": lambda p: p["months"][0]["W"].pop(),
    "11 months": lambda p: p["months"].pop(),
    "13 months": lambda p: p["months"].append(copy.deepcopy(p["months"][0])),
    "months as text": lambda p: p.__setitem__("months", ["junk"] * 12),
}


@pytest.mark.parametrize("label", BAD_PROFILE)
def test_broken_profiles_are_refused_and_change_nothing(app, admin, label):
    calc_before = app.anon().post("/api/public/calculate", json=CALC).json()
    prof = admin.get("/api/admin/profiles").json()[0]
    bad = copy.deepcopy(prof)
    BAD_PROFILE[label](bad)
    assert admin.put(f"/api/admin/profiles/{prof['id']}", json=bad).status_code == 422
    assert admin.get("/api/admin/profiles").json()[0] == prof
    assert app.anon().post("/api/public/calculate", json=CALC).json() == calc_before


# ── Regulated charges (admin) ────────────────────────────────────────────────
# These feed every tariff's cost; Infinity once stored crashed the calculator.
@pytest.mark.parametrize("field, value", [
    ("lv", -5), ("mv", 5.01), ("hv", 1e300), ("pso", -0.001), ("res", 6), ("mdm", -1), ("mdm", 1000.01),
    ("fpaLV", -5.01), ("fpaHV", 99), ("lv", "abc"), ("lv", "NaN"), ("pso", "Infinity"), ("mdm", "-Infinity"),
], ids=lambda v: str(v))
def test_absurd_regulated_charges_are_refused_and_change_nothing(app, admin, field, value):
    before = admin.get("/api/admin/regulated").json()
    calc_before = app.anon().post("/api/public/calculate", json=CALC).json()
    body = {k: before[k] for k in ("lv", "mv", "hv", "fpaLV", "fpaMV", "fpaHV", "pso", "res", "mdm")}
    raw = json.dumps({**body, field: 1.2345}).replace("1.2345", value if value in ("NaN", "Infinity", "-Infinity")
                                                       else json.dumps(value))
    r = admin.put("/api/admin/regulated", data=raw, headers={"Content-Type": "application/json"})
    assert r.status_code == 422
    assert admin.get("/api/admin/regulated").json() == before
    calc = app.anon().post("/api/public/calculate", json=CALC)
    assert calc.status_code == 200 and calc.json() == calc_before


@pytest.mark.parametrize("change", [{"mv": 0.05}, {"hv": 0.038}, {"lv": 0.03}], ids=str)
def test_grid_usage_out_of_voltage_order_is_refused(admin, change):
    # Seed: LV 0.045 > MV 0.038 > HV 0.030. Grid usage must fall with voltage.
    before = admin.get("/api/admin/regulated").json()
    body = {k: before[k] for k in ("lv", "mv", "hv", "fpaLV", "fpaMV", "fpaHV", "pso", "res", "mdm")}
    r = admin.put("/api/admin/regulated", json={**body, **change})
    assert r.status_code == 422 and "grid usage must be lower" in r.text
    assert admin.get("/api/admin/regulated").json() == before


def test_valid_regulated_charges_are_accepted(admin):
    before = admin.get("/api/admin/regulated").json()
    body = {k: before[k] for k in ("lv", "mv", "hv", "fpaLV", "fpaMV", "fpaHV", "pso", "res", "mdm")}
    for change in ({"fpaLV": -0.05}, {"lv": 5, "mdm": 1000}, {"pso": 0}):     # negative FPA and the limits are fine
        assert admin.put("/api/admin/regulated", json={**body, **change}).status_code == 200
    assert admin.put("/api/admin/regulated", json=body).status_code == 200


# ── Nothing crashes the server ───────────────────────────────────────────────
GARBAGE = ["", "{", "null", "[]", '"text"', "12345", '{"a":' * 200 + "1" + "}" * 200, "\x00\xff"]


def test_malformed_requests_never_crash_the_server(app, admin, acme):
    paths = app.anon().get("/openapi.json").json()["paths"]
    targets = [(m.upper(), re.sub(r"\{[^}]+\}", "999999", p)) for p, ops in paths.items() for m in ops
               if m in ("post", "put", "patch") and "/logout" not in p]
    crashes = []
    for method, path in targets:
        who = admin if path.startswith("/api/admin") else acme if path.startswith("/api/supplier") else app.anon()
        for g in GARBAGE:
            r = who.req(method, path, data=g.encode("utf-8", "surrogatepass"),
                        headers={"Content-Type": "application/json"})
            if r.status_code >= 500:
                crashes.append((method, path, g[:20], r.status_code))
    assert not crashes, f"server errors: {crashes}"
