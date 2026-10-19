"""6. Password-reset links: guessing, reusing or replaying them."""
import pytest

from conftest import ACME, DELTA, PASSWORD

NEW = "Fresh-Passw0rd!"


def _request_link(app, email) -> str:
    assert app.anon().post("/api/auth/forgot-password", json={"email": email}).status_code == 200
    return app.reset_token(email)          # from the emailed link


def _reset(app, token, password=NEW):
    return app.anon().post("/api/auth/reset-password", json={"token": token, "password": password})


@pytest.fixture
def fresh(make_app):
    return make_app()


def test_link_works_once_only(fresh):
    token = _request_link(fresh, ACME)
    assert _reset(fresh, token).status_code == 200
    fresh.login(ACME, NEW)
    assert _reset(fresh, token, "Another-Passw0rd!").status_code == 400, "reset link worked twice"
    fresh.login(ACME, NEW)


def test_made_up_or_altered_links_are_refused(fresh):
    token = _request_link(fresh, ACME)
    for fake in ("", "x", "0" * 43, token[:-1] + ("A" if token[-1] != "A" else "B"), token + "x"):
        assert _reset(fresh, fake).status_code in (400, 422), f"accepted {fake!r}"
    fresh.login(ACME, PASSWORD)          # password unchanged


def test_expired_link_is_refused(fresh):
    token = _request_link(fresh, ACME)
    fresh.sql("UPDATE password_resets SET expires_at = '2000-01-01T00:00:00+00:00' WHERE email = ?", (ACME,))
    assert _reset(fresh, token).status_code == 400
    fresh.login(ACME, PASSWORD)


def test_new_link_cancels_the_previous_one(fresh):
    first = _request_link(fresh, ACME)
    _request_link(fresh, ACME)
    assert _reset(fresh, first).status_code == 400


def test_link_of_a_deactivated_account_is_refused(fresh):
    token = _request_link(fresh, DELTA)
    admin = fresh.login("admin1@demo.local")
    admin.patch(f"/api/admin/users/{fresh.user_id(DELTA)}/status", json={"is_active": False})
    assert _reset(fresh, token).status_code == 400


def test_database_copy_holds_no_usable_link(fresh):
    # Someone with a copy of the database (a backup, an export) finds only a
    # fingerprint of the token, which doesn't work as a link.
    token = _request_link(fresh, ACME)
    stored = fresh.sql("SELECT token FROM password_resets WHERE email = ?", (ACME,))[0][0]
    assert stored != token and token not in stored
    assert _reset(fresh, stored).status_code == 400
    assert _reset(fresh, token).status_code == 200


def test_invite_links_work_and_are_stored_hashed(fresh):
    admin = fresh.login("admin1@demo.local")
    r = admin.post("/api/admin/users", json={"email": "new.user@example.com", "supplier_name": "Acme Energy"})
    assert r.status_code == 201
    token = fresh.reset_token("new.user@example.com")
    assert token in r.json()["invite_url"]
    assert fresh.sql("SELECT token FROM password_resets WHERE email = ?", ("new.user@example.com",))[0][0] != token
    assert _reset(fresh, token).status_code == 200
    r = fresh.anon().post("/api/auth/login", json={"email": "new.user@example.com", "password": NEW})
    assert r.status_code == 200 and r.json()["status"] == "otp_required"     # new accounts use 2FA


@pytest.mark.parametrize("weak", ["short1!", "nodigits!!", "n0symbols1", "12345678!"], ids=lambda p: p)
def test_weak_passwords_are_refused(fresh, weak):
    assert _reset(fresh, _request_link(fresh, ACME), weak).status_code == 400


def test_current_or_recent_password_cannot_be_reused(fresh):
    assert _reset(fresh, _request_link(fresh, ACME), PASSWORD).status_code == 400
    assert _reset(fresh, _request_link(fresh, ACME), NEW).status_code == 200
    assert _reset(fresh, _request_link(fresh, ACME), PASSWORD).status_code == 400, "old password reused"
