"""3. Stolen, forged or old logins."""
import time
from datetime import datetime, timedelta, timezone

import jwt
import pytest

from conftest import ACME, DELTA, PASSWORD, VOLT, Client


def _sign(app, **claims) -> str:
    """A token signed with the test server's real key, i.e. as the app itself would issue it."""
    now = datetime.now(timezone.utc)
    payload = {"iat": now, "session_start": now.timestamp(), "exp": now + timedelta(hours=1), **claims}
    return jwt.encode(payload, app.secret, algorithm="HS256")


@pytest.mark.parametrize("who, path", [(ACME, "/api/supplier/tariffs"), ("admin1@demo.local", "/api/admin/config")],
                         ids=["supplier", "admin"])
def test_tampered_or_forged_tokens_are_refused(app, who, path):
    real = app.login(who).token
    assert Client(app, real).get(path).status_code == 200
    h, p, s = real.split(".")
    forged = {
        "signature altered": f"{h}.{p}.{s[:-2]}AA",
        "junk appended": f"{h}.{p}.{s}!!!!",
        "payload swapped, old signature": f"{h}.{jwt.encode({'sub': '1', 'role': 'admin'}, 'x' * 32).split('.')[1]}.{s}",
        "unsigned (alg none)": jwt.encode({"sub": "1", "role": "admin"}, None, algorithm="none"),
        "signed with a guessed key": jwt.encode({"sub": "1", "role": "admin", "exp": 9999999999}, "x" * 32),
        "garbage": "not-a-token",
        "empty": "",
    }
    wrong = {label: code for label, t in forged.items() if (code := Client(app, t).get(path).status_code) != 401}
    assert not wrong, f"accepted or errored on forged tokens: {wrong}"


def test_expired_token_is_refused(app):
    uid = app.user_id(ACME)
    old = datetime.now(timezone.utc) - timedelta(hours=2)
    t = _sign(app, sub=str(uid), role="supplier", iat=old, exp=old + timedelta(hours=1))
    assert Client(app, t).get("/api/supplier/tariffs").status_code == 401


def test_session_older_than_12_hours_is_refused_even_if_renewed(app):
    uid = app.user_id(ACME)
    t = _sign(app, sub=str(uid), role="supplier",
              session_start=(datetime.now(timezone.utc) - timedelta(hours=13)).timestamp())
    assert Client(app, t).get("/api/supplier/tariffs").status_code == 401


def test_role_comes_from_the_database_not_the_token(app):
    # Even a validly signed token that claims "admin" gets supplier rights only.
    t = _sign(app, sub=str(app.user_id(ACME)), role="admin")
    assert Client(app, t).get("/api/admin/config").status_code == 403


def test_half_finished_login_is_not_a_session(app, admin):
    uid = app.user_id(VOLT)
    assert admin.patch(f"/api/admin/users/{uid}/otp", json={"otp_enabled": True}).status_code == 200
    r = app.anon().post("/api/auth/login", json={"email": VOLT, "password": PASSWORD})
    assert r.status_code == 200 and r.json().get("status") == "otp_required"
    assert not r.cookies.get("cera_access_token"), "session cookie issued before the code was entered"
    pending = r.json()["pending_token"]
    assert Client(app, pending).get("/api/supplier/tariffs").status_code == 401


def test_deactivated_account_loses_its_session_immediately(app, admin):
    delta = app.login(DELTA)
    uid = app.user_id(DELTA)
    assert admin.patch(f"/api/admin/users/{uid}/status", json={"is_active": False}).status_code == 200
    try:
        assert delta.get("/api/supplier/tariffs").status_code == 401
        r = app.anon().post("/api/auth/login", json={"email": DELTA, "password": PASSWORD})
        assert r.status_code == 403 and not r.cookies.get("cera_access_token")
    finally:
        admin.patch(f"/api/admin/users/{uid}/status", json={"is_active": True})


def test_password_change_ends_other_sessions_but_keeps_this_one(make_app):
    app = make_app()
    stolen = app.login(ACME)          # e.g. a copy of the cookie on another machine
    time.sleep(1.1)                    # token times are in whole seconds
    me = app.login(ACME)
    r = me.put("/api/auth/password", json={"current_password": PASSWORD, "new_password": "N3w-Passw0rd!"})
    assert r.status_code == 200, r.text
    assert stolen.get("/api/supplier/tariffs").status_code == 401, "old session still works after password change"
    assert me.get("/api/supplier/tariffs").status_code == 200, "user was signed out by their own password change"
