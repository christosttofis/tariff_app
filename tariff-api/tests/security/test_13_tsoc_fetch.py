"""13. Fetching DAM prices from TSOC through the admin API and page.

The test server's "TSOC" is a fake (tests/tsoc_stub.py, chosen by
TEST_TSOC_MODE); nothing here contacts the real TSOC website.
"""
import json
from datetime import timedelta

import pytest

from conftest import ADMIN
from test_10_pages_work import _clean, browser  # noqa: F401  (browser is a fixture)
from test_11_admin_page import _sign_in, _until
from test_12_dam_data import TODAY, _days_back, _payload, _stored, page  # noqa: F401  (page is a fixture)

import dam_data  # noqa: E402  (path set up by test_12_dam_data)


def test_fetch_is_only_a_preview(app, admin):
    admin.put("/api/admin/dam", json=_payload(*_days_back(5, 3)))
    stored_before = _stored(app)
    r = admin.post("/api/admin/dam/fetch-tsoc")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["ok"] is True, body
    assert set(body["report"]["addedByDay"]) == set(_days_back(2, 0))
    assert body["report"]["notYetPublished"] == [(TODAY + timedelta(days=1)).isoformat()]
    assert dam_data.dataset_dates(body["payload"]["damDailyData"])[-1] == TODAY.isoformat()
    assert _stored(app) == stored_before, "a fetch must not change the live data"
    assert admin.get("/api/admin/dam/log").json()[0]["action"] == "fetch_ok"

    # Saving the preview makes it live, as a "tsoc" version.
    r = admin.put("/api/admin/dam", json={**body["payload"], "damYear": 2026, "source": "tsoc"})
    assert r.status_code == 200, r.text
    status = admin.get("/api/admin/dam/status").json()
    assert status["lastDate"] == TODAY.isoformat() and status["lastVersion"]["source"] == "tsoc"
    assert admin.get("/api/admin/dam/log").json()[0]["action"] == "saved_tsoc"
    again = admin.post("/api/admin/dam/fetch-tsoc").json()
    assert again["ok"] is True and again["payload"] is None


def test_fetch_is_admin_only(app, acme):
    assert app.anon().post("/api/admin/dam/fetch-tsoc").status_code == 401
    assert acme.post("/api/admin/dam/fetch-tsoc").status_code == 403


def test_fetch_takes_no_url_or_dates_from_the_caller(app):
    op = app.anon().get("/openapi.json").json()["paths"]["/api/admin/dam/fetch-tsoc"]["post"]
    assert not op.get("parameters") and "requestBody" not in op


@pytest.mark.parametrize("mode, reason", [("short", "46 of 48"), ("blocked", "Cloudflare")])
def test_cancelled_fetch_changes_nothing(make_app, mode, reason):
    app = make_app({"TEST_TSOC_MODE": mode})
    admin = app.login(ADMIN)
    admin.put("/api/admin/dam", json=_payload(*_days_back(4, 2)))
    before = _stored(app)
    body = admin.post("/api/admin/dam/fetch-tsoc").json()
    assert body["ok"] is False and reason in "\n".join(body["reasons"]), body
    assert "payload" not in body
    assert _stored(app) == before
    log = admin.get("/api/admin/dam/log").json()[0]
    assert log["action"] == "fetch_cancelled" and reason in "\n".join(log["details"]["reasons"])


def test_big_gap_is_cancelled_without_contacting_tsoc(make_app):
    app = make_app()
    admin = app.login(ADMIN)
    admin.put("/api/admin/dam", json=_payload(*_days_back(60, 59)))
    body = admin.post("/api/admin/dam/fetch-tsoc").json()
    assert body["ok"] is False and "at most 31" in body["reasons"][0]
    assert body["report"]["requests"] == []


def test_switched_off_hides_the_button_and_refuses_the_endpoint(make_app, browser):
    app = make_app({"TARIFF_TSOC_FETCH": "off"})
    admin = app.login(ADMIN)
    assert admin.get("/api/admin/config").json()["tsocFetchEnabled"] is False
    r = admin.post("/api/admin/dam/fetch-tsoc")
    assert r.status_code == 404 and "switched off" in r.text
    assert app.sql("SELECT COUNT(*) FROM dam_change_log WHERE action LIKE 'fetch%'") == [(0,)]
    pg = browser.new_page()
    _sign_in(pg, app)
    pg.click(".nav-item[data-arg='dam']")
    pg.wait_for_selector("#pane-dam.active")
    assert not pg.is_visible("#dam-fetch-btn")
    assert pg.is_visible("[data-action=downloadDamCsv]")       # the rest of the DAM page still works
    pg.close()


def test_admin_page_fetch_check_and_save(make_app, page):
    app = make_app()
    assert app.login(ADMIN).get("/api/admin/config").json()["tsocFetchEnabled"] is True
    app.login(ADMIN).put("/api/admin/dam", json=_payload(*_days_back(5, 3)))
    _sign_in(page, app)
    page.click(".nav-item[data-arg='dam']")
    page.wait_for_selector("#pane-dam.active")
    page.click("[data-action=fetchDamFromTsoc]")
    _until(page, lambda: "Review, then Save" in page.inner_text("#dam-status"), "fetch preview")
    assert "+48" in page.inner_text("#dam-fetch-report")
    assert app.sql("SELECT COUNT(*) FROM dam_versions") == [(2,)], "preview must not save"
    # Click a fetched day in the report → its 48 prices, marked as new.
    page.click(f"#dam-fetch-report li[data-arg='{TODAY}']")
    page.wait_for_selector("#dam-day-detail", state="visible")
    assert page.locator("#dam-day-detail .dam-day-slot").count() == 48
    assert "100.50" in page.inner_text("#dam-day-detail")            # fake TSOC: 100.5 €/MWh at 00:00
    assert "not saved" in page.inner_text("#dam-day-detail")
    page.click("[data-action=saveDamData]")
    _until(page, lambda: app.sql("SELECT source FROM dam_versions ORDER BY id DESC LIMIT 1") == [("tsoc",)], "saved")
    page.wait_for_selector("#dam-log-tbody")
    _until(page, lambda: "Saved (TSOC fetch)" in page.inner_text("#dam-log-tbody"), "log shows the TSOC save")
    assert json.loads(app.sql("SELECT damDailyData FROM dam_data")[0][0])
    _clean(page)
