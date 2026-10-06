"""1. Wrong person, wrong area.

Every admin and supplier endpoint is read from the app's own route list, so an
endpoint added later is covered automatically. Path IDs are dummies: the
access check must refuse before the app even looks the item up.
"""
import re

import pytest

from conftest import ACME, ADMIN, PASSWORD


def _routes(app, prefix):
    paths = app.anon().get("/openapi.json").json()["paths"]
    found = [(m.upper(), p) for p, ops in paths.items() for m in ops if p.startswith(prefix)]
    assert found, f"no {prefix} routes found - route list unreadable?"
    return found


def _fill(path):
    return re.sub(r"\{[^}]+\}", "999999", path)


def test_route_lists_are_complete(app):
    # Guards the tests below against silently checking nothing.
    assert len(_routes(app, "/api/admin/")) >= 40
    assert len(_routes(app, "/api/supplier/")) >= 10


def test_signed_out_visitor_is_refused_everywhere(app):
    anon = app.anon()
    wrong = [(m, p, r.status_code) for m, p in _routes(app, "/api/admin/") + _routes(app, "/api/supplier/")
             if (r := anon.req(m, _fill(p), json={})).status_code != 401]
    for m, p in (("GET", "/api/auth/me"), ("PUT", "/api/auth/email"), ("PUT", "/api/auth/password")):
        if (r := anon.req(m, p, json={})).status_code != 401:
            wrong.append((m, p, r.status_code))
    assert not wrong, f"reachable without signing in: {wrong}"


def test_supplier_is_refused_on_every_admin_endpoint(app, acme):
    wrong = [(m, p, r.status_code) for m, p in _routes(app, "/api/admin/")
             if (r := acme.req(m, _fill(p), json={})).status_code != 403]
    assert not wrong, f"supplier reached admin endpoints: {wrong}"


def test_admin_is_refused_on_every_supplier_endpoint(app, admin):
    wrong = [(m, p, r.status_code) for m, p in _routes(app, "/api/supplier/")
             if (r := admin.req(m, _fill(p), json={})).status_code != 403]
    assert not wrong, f"admin reached supplier-only endpoints: {wrong}"


# ── Admin only from the CERA office/VPN ──────────────────────────────────────
# The server is told it sits behind one proxy (as on Azure) that writes the
# caller's address as the last X-Forwarded-For entry. 10.0.0.0/8 plays "CERA".
INSIDE = {"X-Forwarded-For": "10.20.30.40"}
OUTSIDE = {"X-Forwarded-For": "203.0.113.7"}
SPOOFED = {"X-Forwarded-For": "10.20.30.40, 203.0.113.7"}   # attacker pre-fills a CERA address


@pytest.fixture
def office_app(make_app):
    return make_app({"TARIFF_ADMIN_ALLOWED_NETWORKS": "10.0.0.0/8", "TARIFF_TRUSTED_PROXY_HOPS": "1"})


def test_admin_works_inside_the_office_network(office_app):
    admin = office_app.login(ADMIN, headers=INSIDE)
    assert admin.get("/api/admin/config", headers=INSIDE).status_code == 200
    assert office_app.anon().get("/admin.html", headers=INSIDE).status_code == 200


@pytest.mark.parametrize("where", [OUTSIDE, SPOOFED, {}], ids=["outside", "spoofed-header", "no-proxy-header"])
def test_admin_is_unavailable_outside_the_office_network(office_app, where):
    anon = office_app.anon()
    assert anon.get("/admin.html", headers=where).status_code == 404
    r = anon.post("/api/auth/login", json={"email": ADMIN, "password": PASSWORD}, headers=where)
    assert r.status_code == 404, "admin password must not even be checked from outside"
    # A session started inside stops working as soon as it is used from outside.
    admin = office_app.login(ADMIN, headers=INSIDE)
    assert admin.get("/api/admin/config", headers=where).status_code == 404


def test_outside_attempts_cannot_lock_out_an_admin(office_app):
    anon = office_app.anon()
    for _ in range(5):
        anon.post("/api/auth/login", json={"email": ADMIN, "password": "wrong-Pass1!"}, headers=OUTSIDE)
    office_app.login(ADMIN, headers=INSIDE)   # still able to sign in from the office


def test_suppliers_are_not_restricted_by_network(office_app):
    acme = office_app.login(ACME, headers=OUTSIDE)
    assert acme.get("/api/supplier/tariffs", headers=OUTSIDE).status_code == 200
