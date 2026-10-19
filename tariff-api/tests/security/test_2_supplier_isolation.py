"""2. Nosy supplier: Acme Energy tries to reach or change Delta Power's data."""
import pytest

from conftest import DELTA

PDF = b"%PDF-1.4\n% attacker-test document\n%%EOF\n"
_READ_ONLY = ("id", "status", "createdAt", "updatedAt", "rejection_reason", "hasDocs", "everPublished")


def _body(tariff: dict, **changes) -> dict:
    b = {k: v for k, v in tariff.items() if k not in _READ_ONLY}
    return {**b, **changes}


@pytest.fixture(scope="module")
def deltas_tariff(app, delta):
    t = delta.get("/api/supplier/tariffs").json()[0]
    assert t["supplier"] == "Delta Power"
    return t


@pytest.fixture(scope="module")
def deltas_document(delta, deltas_tariff):
    r = delta.post(f"/api/supplier/tariffs/{deltas_tariff['id']}/documents",
                   files={"file": ("delta-terms.pdf", PDF, "application/pdf")})
    assert r.status_code == 201, r.text
    return r.json()["id"]


def _admin_view(admin, tariff_id):
    return next(t for t in admin.get("/api/admin/tariffs").json() if t["id"] == tariff_id)


def test_supplier_sees_only_its_own_tariffs(acme):
    tariffs = acme.get("/api/supplier/tariffs").json()
    assert tariffs and {t["supplier"] for t in tariffs} == {"Acme Energy"}


def test_cannot_touch_another_suppliers_tariff(acme, admin, deltas_tariff, deltas_document):
    tid = deltas_tariff["id"]
    before = _admin_view(admin, tid)
    attempts = {
        "edit": acme.put(f"/api/supplier/tariffs/{tid}", json=_body(deltas_tariff, supplier="Acme Energy", name="hijacked")),
        "delete": acme.delete(f"/api/supplier/tariffs/{tid}"),
        "list documents": acme.get(f"/api/supplier/tariffs/{tid}/documents"),
        "upload document": acme.post(f"/api/supplier/tariffs/{tid}/documents",
                                     files={"file": ("x.pdf", PDF, "application/pdf")}),
        "download document": acme.get(f"/api/supplier/documents/{deltas_document}/download"),
    }
    # 404, the same as for an item that doesn't exist, so IDs can't be probed.
    assert {k: r.status_code for k, r in attempts.items()} == {k: 404 for k in attempts}
    after = _admin_view(admin, tid)
    assert after == before, "Delta's tariff changed"


def test_cannot_submit_or_move_a_tariff_under_another_supplier(acme, deltas_tariff):
    own = acme.get("/api/supplier/tariffs").json()[0]
    r = acme.post("/api/supplier/tariffs", json=_body(own, supplier="Delta Power", name="posing as Delta"))
    assert r.status_code == 403
    r = acme.put(f"/api/supplier/tariffs/{own['id']}", json=_body(own, supplier="Delta Power"))
    assert r.status_code == 403
    # Reusing another supplier's tariff ID must not overwrite it.
    r = acme.post("/api/supplier/tariffs", json={**_body(own), "id": deltas_tariff["id"]})
    assert r.status_code == 409


def test_cannot_approve_own_tariff_by_adding_fields(acme, admin):
    own = acme.get("/api/supplier/tariffs").json()[0]
    sneaky = {**_body(own, name="self-approved?"), "status": "approved", "everPublished": True,
              "rejection_reason": None, "createdAt": "2000-01-01", "supplier_id": 999}
    r = acme.post("/api/supplier/tariffs", json=sneaky)
    assert r.status_code == 201
    new = r.json()
    assert new["status"] == "pending" and new["supplier"] == "Acme Energy" and not new["everPublished"]
    r = acme.put(f"/api/supplier/tariffs/{new['id']}", json=sneaky)
    assert r.status_code == 200 and r.json()["status"] == "pending"
    assert _admin_view(admin, new["id"])["status"] == "pending"
    public = admin.post("/api/public/calculate", json={"customerType": "domestic", "inputMode": "annual",
                                                       "annualKwh": 4000}).json()
    assert all(x["id"] != new["id"] for x in public["results"]), "unapproved tariff is public"


def test_public_config_shows_no_audit_log_accounts_or_unpublished_tariffs(app, admin, delta, deltas_tariff):
    # Delta submits a tariff that is not approved yet, and an admin changes a sign-in
    # setting: both go into the audit log, which once came with the public config.
    r = delta.post("/api/supplier/tariffs", json=_body(deltas_tariff, name="Delta unpublished offer"))
    assert r.status_code == 201
    user = next(u for u in admin.get("/api/admin/users").json() if u["email"] == DELTA)
    for value in (not user["otp_enabled"], user["otp_enabled"]):
        assert admin.patch(f"/api/admin/users/{user['id']}/otp", json={"otp_enabled": value}).status_code == 200
    logged = str(admin.get("/api/admin/changelog").json())
    assert "Delta unpublished offer" in logged and DELTA in logged, "nothing logged - test would prove nothing"

    public = app.anon().get("/api/public/config")
    assert public.status_code == 200 and "changelog" not in public.json()
    # Sign-in accounts are @demo.local; the suppliers' public contact addresses are not.
    for private in ("Delta unpublished offer", "@demo.local", "otp_enabled"):
        assert private not in public.text, f"public config shows {private!r}"


def test_supplier_gets_only_profile_names_not_data(acme):
    profiles = acme.get("/api/supplier/profiles").json()
    assert profiles and all(set(p) <= {"id", "name", "desc"} for p in profiles)


def test_cannot_read_messages_sent_to_another_supplier(acme, delta, admin):
    r = admin.post("/api/admin/messages", json={"subject": "For Delta only", "body": "private",
                                                "audience": "selected", "target_suppliers": ["Delta Power"]})
    assert r.status_code == 201
    mid = r.json()["id"]
    assert any(m["id"] == mid for m in delta.get("/api/supplier/messages").json())
    assert all(m["id"] != mid for m in acme.get("/api/supplier/messages").json())
    assert acme.post(f"/api/supplier/messages/{mid}/read").status_code == 404
    assert acme.post(f"/api/supplier/messages/{mid}/ack").status_code == 404
