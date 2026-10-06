"""4. Guessing passwords and sign-in codes; flooding the server.

Lockouts last 3 hours, so every test here gets its own fresh server.
"""
import pytest

from conftest import ACME, PASSWORD, VOLT, Client

LOCKED = 429


def _login(app, email, password):
    return app.anon().post("/api/auth/login", json={"email": email, "password": password})


def test_three_wrong_passwords_lock_the_account(make_app):
    app = make_app()
    codes = [_login(app, ACME, f"Wrong-guess{i}!").status_code for i in range(3)]
    assert codes == [401, 401, LOCKED]
    r = _login(app, ACME, PASSWORD)
    assert r.status_code == LOCKED and not r.cookies.get("cera_access_token"), "right password accepted while locked"


def test_lockout_is_cleared_only_by_an_admin_or_time(make_app):
    app = make_app()
    for i in range(3):
        _login(app, ACME, f"Wrong-guess{i}!")
    admin = app.login("admin1@demo.local")
    assert admin.post(f"/api/admin/users/{app.user_id(ACME)}/unlock").status_code == 200
    app.login(ACME)


@pytest.fixture
def otp_app(make_app):
    """A server where Volt Co's user must enter an emailed 6-digit code after the password."""
    app = make_app()
    admin = app.login("admin1@demo.local")
    assert admin.patch(f"/api/admin/users/{app.user_id(VOLT)}/otp", json={"otp_enabled": True}).status_code == 200
    return app


def _start_otp_login(app) -> str:
    r = _login(app, VOLT, PASSWORD)
    assert r.status_code == 200 and r.json()["status"] == "otp_required"
    return r.json()["pending_token"]


def _code(app) -> str:
    # Email is off in tests, so read the code the app stored.
    return app.sql("SELECT code FROM otp_codes WHERE email = ? ORDER BY id DESC", (VOLT,))[0][0]


def test_correct_code_completes_sign_in(otp_app):
    pending = _start_otp_login(otp_app)
    c = Client(otp_app)
    r = c.post("/api/auth/verify-otp", json={"pending_token": pending, "code": _code(otp_app)})
    assert r.status_code == 200 and c.token
    assert c.get("/api/supplier/tariffs").status_code == 200


def test_three_wrong_codes_lock_the_account(otp_app):
    pending = _start_otp_login(otp_app)
    real = _code(otp_app)
    wrong = [c for c in ("000000", "111111", "222222", "333333") if c != real][:3]
    codes = [otp_app.anon().post("/api/auth/verify-otp", json={"pending_token": pending, "code": w}).status_code
             for w in wrong]
    assert codes == [401, 401, LOCKED]
    r = otp_app.anon().post("/api/auth/verify-otp", json={"pending_token": pending, "code": real})
    assert r.status_code == LOCKED and not r.cookies.get("cera_access_token"), "right code accepted while locked"


def test_code_cannot_be_used_twice(otp_app):
    pending = _start_otp_login(otp_app)
    code = _code(otp_app)
    assert otp_app.anon().post("/api/auth/verify-otp", json={"pending_token": pending, "code": code}).status_code == 200
    assert otp_app.anon().post("/api/auth/verify-otp", json={"pending_token": pending, "code": code}).status_code == 401


def test_new_code_cannot_be_requested_again_within_two_minutes(otp_app):
    pending = _start_otp_login(otp_app)
    r = otp_app.anon().post("/api/auth/resend-otp", json={"pending_token": pending})
    assert r.status_code == 429


def test_tampered_half_finished_login_is_refused(otp_app):
    # The pending token names the account; editing it must not let a code be tried on another account.
    pending = _start_otp_login(otp_app)
    h, p, s = pending.split(".")
    r = otp_app.anon().post("/api/auth/verify-otp", json={"pending_token": f"{h}.{p}.{s[:-2]}AA", "code": _code(otp_app)})
    assert r.status_code == 401


def test_request_flood_is_rate_limited(make_app):
    app = make_app(rate_limit=60)          # the production value: 60 requests per minute per address
    anon = app.anon()
    codes = [anon.get("/api/public/config").status_code for _ in range(61)]
    # (the server's start-up check already used one request of this minute)
    assert codes.count(200) >= 55 and codes[-1] == 429
    # Sign-in attempts count too, so password guessing is slowed down as well.
    assert _login(app, ACME, PASSWORD).status_code == 429
