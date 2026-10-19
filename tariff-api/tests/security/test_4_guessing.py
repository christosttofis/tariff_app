"""4. Guessing passwords and sign-in codes; flooding the server.

Lockout rules (lockout.py): 5 wrong passwords block that address for that email;
30 from all addresses within an hour lock the whole account; 3 wrong sign-in codes
lock the account. Locks outlast a test, so every test here gets its own fresh
server. The password tests run behind one trusted proxy hop, so each request can
come from a chosen address (X-Forwarded-For), as it would on Azure.
"""
import pytest

from conftest import ACME, PASSWORD, VOLT, Client

LOCKED = 429
COOKIE = "cera_access_token"
ATTACKER, OWNER = "203.0.113.66", "198.51.100.7"
PROXIED = {"TARIFF_TRUSTED_PROXY_HOPS": "1"}


def _login(app, email, password, ip=None):
    headers = {"X-Forwarded-For": ip} if ip else None
    return app.anon().post("/api/auth/login", json={"email": email, "password": password}, headers=headers)


def _admin(app):
    return app.login("admin1@demo.local", headers={"X-Forwarded-For": "192.0.2.1"})


def test_wrong_passwords_block_only_the_guessing_address(make_app):
    app = make_app(PROXIED)
    codes = [_login(app, ACME, f"Wrong-guess{i}!", ATTACKER).status_code for i in range(6)]
    assert codes == [401] * 5 + [LOCKED]
    r = _login(app, ACME, PASSWORD, ATTACKER)
    assert r.status_code == LOCKED and not r.cookies.get(COOKIE), "right password accepted from a blocked address"
    # The real supplier, elsewhere, is not locked out (the old rule locked them for 3 hours).
    app.login(ACME, headers={"X-Forwarded-For": OWNER})
    # ...and the owner signing in gives the guessing address no fresh tries.
    assert _login(app, ACME, "Wrong-guess9!", ATTACKER).status_code == LOCKED


def test_blocked_address_gets_the_same_reply_for_made_up_emails(make_app):
    app = make_app(PROXIED)
    real = [_login(app, ACME, f"Wrong-guess{i}!", ATTACKER) for i in range(6)]
    fake = [_login(app, "ghost@demo.local", f"Wrong-guess{i}!", ATTACKER) for i in range(6)]
    assert [(r.status_code, r.json()) for r in real] == [(r.status_code, r.json()) for r in fake]


def test_own_typos_are_forgiven_after_signing_in(make_app):
    app = make_app(PROXIED)
    for i in range(4):
        assert _login(app, ACME, f"Typo{i}!", OWNER).status_code == 401
    app.login(ACME, headers={"X-Forwarded-For": OWNER})
    assert [_login(app, ACME, f"Typo{i}!", OWNER).status_code for i in range(5)] == [401] * 5


def test_guessing_from_many_addresses_locks_the_account(make_app):
    app = make_app(PROXIED)
    codes = [_login(app, ACME, f"Wrong-guess{i}!", f"203.0.113.{i // 5 + 1}").status_code for i in range(30)]
    assert codes == [401] * 29 + [LOCKED]                   # 6 addresses x 5 guesses
    r = _login(app, ACME, PASSWORD, OWNER)
    assert r.status_code == LOCKED and not r.cookies.get(COOKIE), "right password accepted while locked"
    assert any("locked" in m["subject"] for m in app.mails(ACME)), "owner not emailed"


def test_admin_unlock_clears_account_and_address_blocks(make_app):
    app = make_app(PROXIED)
    for i in range(30):
        _login(app, ACME, f"Wrong-guess{i}!", f"203.0.113.{i // 5 + 1}")
    assert _admin(app).post(f"/api/admin/users/{app.user_id(ACME)}/unlock").status_code == 200
    app.login(ACME, headers={"X-Forwarded-For": "203.0.113.1"})       # a previously blocked address too


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
    return app.otp_code(VOLT)              # from the emailed code; the database holds only a hash


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


def test_signing_in_again_does_not_reset_wrong_codes(otp_app):
    # A correct password used to reset the count, so someone with the password
    # could guess codes two at a time forever, signing in again in between.
    wrong = lambda p: otp_app.anon().post("/api/auth/verify-otp", json={"pending_token": p, "code": "000000"})  # noqa: E731
    for _ in range(2):
        pending = _start_otp_login(otp_app)
        if _code(otp_app) == "000000":
            pytest.skip("the random code happened to be 000000")
        assert wrong(pending).status_code == 401
    r = _login(otp_app, VOLT, PASSWORD)
    pending = r.json()["pending_token"]
    assert wrong(pending).status_code == LOCKED


def test_database_copy_holds_no_usable_code(otp_app):
    _start_otp_login(otp_app)
    stored = otp_app.sql("SELECT code FROM otp_codes WHERE email = ?", (VOLT,))[0][0]
    assert _code(otp_app) not in stored and len(stored) == 64


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
