"""12. DAM prices: versions (backup/rollback), change log, checks on saved data,
freshness, and the admin page's DAM tools. (Fetching from TSOC: test_13.)
"""
import json
import os
import subprocess
import sys
from datetime import timedelta
from pathlib import Path

import pytest

from conftest import ADMIN, API_DIR, _BASE_ENV, _NO_DOTENV
from test_10_pages_work import _WATCH_CSP, _clean, browser  # noqa: F401  (browser is a fixture)
from test_11_admin_page import _pane, _sign_in, _until

sys.path.insert(0, str(API_DIR))
import dam_data  # noqa: E402

TODAY = dam_data.cyprus_now().date()


def _payload(*days, price=0.1, year=2026):
    p = dam_data.build_dam_payload({f"{d} {s // 2:02d}:{30 * (s % 2):02d}": price for d in days for s in range(48)})
    return {**p, "damYear": year}


def _days_back(first, last):
    """Full days from `first` to `last` days before today (Cyprus)."""
    return [(TODAY - timedelta(days=n)).isoformat() for n in range(first, last - 1, -1)]


def _stored(app):
    return json.loads(app.sql("SELECT damDailyData FROM dam_data")[0][0])


@pytest.fixture
def page(browser):
    ctx = browser.new_context(accept_downloads=True)
    ctx.add_init_script(_WATCH_CSP)
    pg = ctx.new_page()
    pg.errors = []
    pg.on("pageerror", lambda e: pg.errors.append(str(e)))
    pg.on("console", lambda m: pg.errors.append(m.text) if m.type == "error" else None)
    pg.on("dialog", lambda d: d.accept())
    yield pg
    ctx.close()


# ── versions, change log, restore ─────────────────────────────────────────────

def test_save_keeps_a_backup_and_logs_it(app, admin):
    before = _stored(app)
    r = admin.put("/api/admin/dam", json={**_payload(*_days_back(5, 3)), "source": "upload"})
    assert r.status_code == 200, r.text
    versions = admin.get("/api/admin/dam/versions").json()
    # The data stored before versioning existed is backed up first, then the new data.
    assert [v["source"] for v in versions] == ["upload", "initial"]
    assert versions[0]["id"] == r.json()["versionId"]
    assert versions[0]["dayCount"] == 3 and versions[0]["createdBy"] == ADMIN
    assert json.loads(app.sql("SELECT payload FROM dam_versions WHERE source = 'initial'")[0][0])["damDailyData"] == before
    log = admin.get("/api/admin/dam/log").json()
    assert log[0]["action"] == "saved_upload" and log[0]["actor"] == ADMIN
    assert log[0]["details"]["daysAdded"] == 3 and log[0]["versionId"] == versions[0]["id"]


def test_later_save_adds_days_and_updates_status(admin):
    assert admin.put("/api/admin/dam", json=_payload(*_days_back(5, 0))).status_code == 200
    status = admin.get("/api/admin/dam/status").json()
    assert status["lastDate"] == TODAY.isoformat() and status["stale"] is False and status["dayCount"] == 6
    assert status["lastVersion"]["source"] == "upload"
    log = admin.get("/api/admin/dam/log").json()[0]
    assert log["details"]["daysAdded"] == 3 and log["details"]["daysRemoved"] == 0


def test_restore_brings_back_an_earlier_version(app, admin):
    versions = admin.get("/api/admin/dam/versions").json()
    target = [v for v in versions if v["source"] == "upload"][-1]           # the 3-day one
    r = admin.post(f"/api/admin/dam/versions/{target['id']}/restore")
    assert r.status_code == 200, r.text
    old = admin.get(f"/api/admin/dam/versions/{target['id']}").json()["payload"]
    assert _stored(app) == old["damDailyData"]
    after = admin.get("/api/admin/dam/versions").json()
    assert len(after) == len(versions) + 1, "restoring must not delete anything"
    assert after[0]["source"] == "rollback" and after[0]["restoredFrom"] == target["id"]
    log = admin.get("/api/admin/dam/log").json()[0]
    assert log["action"] == "rollback" and log["details"]["daysRemoved"] == 3


def test_unknown_or_malformed_version_ids(admin):
    assert admin.get("/api/admin/dam/versions/999999").status_code == 404
    assert admin.post("/api/admin/dam/versions/999999/restore").status_code == 404
    assert admin.get("/api/admin/dam/versions/1%20OR%201=1").status_code == 422
    assert admin.post("/api/admin/dam/versions/abc/restore").status_code == 422


def test_dam_endpoints_are_admin_only(app, acme):
    anon = app.anon()
    for m, p in [("GET", "/api/admin/dam/status"), ("GET", "/api/admin/dam/log"),
                 ("GET", "/api/admin/dam/versions"), ("GET", "/api/admin/dam/versions/1"),
                 ("POST", "/api/admin/dam/versions/1/restore")]:
        assert anon.req(m, p).status_code == 401, p
        assert acme.req(m, p).status_code == 403, p


# ── the server checks the data before saving it ──────────────────────────────

def test_unknown_source_is_refused(admin):
    r = admin.put("/api/admin/dam", json={**_payload(*_days_back(2, 1)), "source": "<script>"})
    assert r.status_code == 422


def _broken(change):
    p = _payload("2026-01-01", "2026-01-02", price=0.09)
    change(p)
    return p


@pytest.mark.parametrize("change, message", [
    (lambda p: p["damDailyData"][0][0]["slots"].__setitem__(5, 90.5), "right price unit"),   # €/MWh sent as €/kWh
    (lambda p: p["damMonthly"].__setitem__(0, 120), "right price unit"),
    (lambda p: p["damDailyData"][0][0]["slots"].pop(), "48 half-hours"),
    (lambda p: p["damDailyData"][0].append(dict(p["damDailyData"][0][0])), "appears twice"),
    (lambda p: p["damDailyData"][1].append(p["damDailyData"][0].pop()), "wrong month"),
    (lambda p: p["damDailyData"][0][0].__setitem__("dateStr", "2026-02-30"), "not a date"),
    (lambda p: p["damDailyData"][0][0].__setitem__("note", "<img src=x onerror=alert(1)>"), "dateStr and slots only"),
    (lambda p: p["damDailyData"][0][0].__setitem__("slots", "x" * 48), "48 half-hours"),
    (lambda p: p.__setitem__("damBySlot", [[0.1] * 48] * 3), "12 months"),
    (lambda p: p.__setitem__("damMonthly", [None] * 11), "12 months"),
])
def test_malformed_dam_data_is_refused(app, admin, change, message):
    before = app.sql("SELECT COUNT(*) FROM dam_versions")
    r = admin.put("/api/admin/dam", json=_broken(change))
    assert r.status_code == 422 and message in r.text, r.text[:500]
    assert app.sql("SELECT COUNT(*) FROM dam_versions") == before, "refused data must not be versioned"


def test_non_finite_prices_are_refused(admin):
    body = json.dumps(_payload("2026-01-01")).replace("0.1,", "NaN,", 1)
    r = admin.put("/api/admin/dam", data=body, headers={"Content-Type": "application/json"})
    assert r.status_code == 422


def test_oversized_dam_body_is_refused_before_reading(app, admin):
    import http.client
    conn = http.client.HTTPConnection("127.0.0.1", app.port, timeout=10)
    conn.putrequest("PUT", "/api/admin/dam")
    conn.putheader("Cookie", f"cera_access_token={admin.token}")
    conn.putheader("Content-Type", "application/json")
    conn.putheader("Content-Length", str(200 * 1024 * 1024))
    conn.endheaders()                      # no body sent at all
    assert conn.getresponse().status == 413
    conn.close()


# ── 15-day freshness: status and the reminder email ──────────────────────────

def _run_staleness_check(app, times=1, shift_days=0):
    """Runs the daily check in a separate process against the test database, with
    the email replaced by a print. Returns how many emails it would have sent."""
    code = _NO_DOTENV + (
        "import sys, datetime as dt; sys.path.insert(0, '.'); "
        "import email_utils; sent = []; email_utils.notify_dam_stale = lambda *a: sent.append(a) or True; "
        "from database import SessionLocal; from routers import admin as A; import models; "
        f"db = SessionLocal()\n"
        f"for i in range({times}):\n"
        f"    A.run_dam_staleness_check(db)\n"
        f"    d = db.query(models.DamData).first()\n"
        f"    if d.stale_notified_at:\n"
        f"        t = dt.datetime.fromisoformat(d.stale_notified_at) - dt.timedelta(days={shift_days}); "
        f"d.stale_notified_at = t.isoformat(); db.commit()\n"
        "print(len(sent))"
    )
    env = {**os.environ, **_BASE_ENV, "TARIFF_SECRET_KEY": "x" * 64, "DATABASE_URL": "sqlite:///" + app.db_path.as_posix()}
    r = subprocess.run([sys.executable, "-c", code], cwd=API_DIR, env=env, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return int(r.stdout.strip().splitlines()[-1])


def test_old_data_is_flagged_and_emailed_once_a_week(make_app):
    app = make_app()
    admin = app.login(ADMIN)
    admin.put("/api/admin/dam", json=_payload(*_days_back(20, 16)))
    s = admin.get("/api/admin/dam/status").json()
    assert s["stale"] is True and s["ageDays"] == 16 and s["staleAfterDays"] == 15
    assert _run_staleness_check(app, times=3) == 1                      # not again the same week
    assert _run_staleness_check(app, times=1, shift_days=8) == 0        # marker moved back below...
    assert _run_staleness_check(app, times=1) == 1                      # ...so a week later: again
    assert admin.get("/api/admin/dam/log").json()[0]["action"] == "stale_alert_sent"
    admin.put("/api/admin/dam", json=_payload(*_days_back(3, 0)))       # fresh data resets it
    assert app.sql("SELECT stale_notified_at FROM dam_data") == [(None,)]
    assert _run_staleness_check(app) == 0
    assert admin.get("/api/admin/dam/status").json()["stale"] is False


# ── admin page ────────────────────────────────────────────────────────────────

def _csv(days, price="100.5"):
    return "\n".join(f"{d} {s // 2:02d}:{30 * (s % 2):02d},{price}" for d in days for s in range(48))


def test_upload_gives_the_same_dataset_as_the_python_builder(make_app, page):
    # Uneven prices, two months; the file is in time order, as TSOC data and exported files are.
    rows = {f"2026-01-{d:02d} {s // 2:02d}:{30 * (s % 2):02d}": round(80.123 + d * 1.7 + s * 0.31, 3)
            for d in (3, 4, 5) for s in range(48)}
    rows.update({f"2026-02-01 {s // 2:02d}:{30 * (s % 2):02d}": -1.25 + s for s in range(48)})
    csv = "\n".join(f"{k}:00,{v}" for k, v in sorted(rows.items()))
    app = make_app()
    _sign_in(page, app)
    _pane(page, "dam")
    page.select_option("#dam-unit", "mwh")
    page.set_input_files("#dam-file-input", files=[{"name": "p.csv", "mimeType": "text/csv", "buffer": csv.encode()}])
    _until(page, lambda: "Parsed 192 rows" in page.inner_text("#dam-status"), "upload parsed")
    page.click("[data-action=saveDamData]")
    _until(page, lambda: app.sql("SELECT damRowCount FROM dam_data") == [(192,)], "saved")
    js = {k: json.loads(v) for k, v in zip(("damMonthly", "damBySlot", "damDailyData"),
                                            app.sql("SELECT damMonthly, damBySlot, damDailyData FROM dam_data")[0])}
    py = dam_data.build_dam_payload({k: float(str(v)) / 1000 for k, v in rows.items()})
    assert js["damDailyData"] == py["damDailyData"]
    assert js["damMonthly"] == py["damMonthly"]
    assert js["damBySlot"] == py["damBySlot"]
    _clean(page)


def test_admin_page_check_days_download_save_restore_and_dashboard(make_app, page):
    app = make_app()
    admin = app.login(ADMIN)
    admin.put("/api/admin/dam", json=_payload(*_days_back(22, 18)))   # 18 days old: stale
    _sign_in(page, app)
    page.wait_for_selector("#dash-dam-attention", state="visible")
    assert "18" in page.inner_text("#dash-dam-until")
    assert page.is_visible("#nav-dam-bubble")
    page.click("#dash-dam-attention [data-action=showPane]")
    page.wait_for_selector("#pane-dam.active")

    # Load a file that adds the missing days (not saved yet).
    page.select_option("#dam-unit", "mwh")
    page.set_input_files("#dam-file-input", files=[{"name": "d.csv", "mimeType": "text/csv",
                                                    "buffer": _csv(_days_back(22, 0)).encode()}])
    _until(page, lambda: f"Parsed {23 * 48} rows" in page.inner_text("#dam-status"), "parsed")
    # Check a day before saving: its 48 prices, marked as new.
    page.click(f"[data-action=damOpenMonth][data-arg='{TODAY.month - 1}'][data-arg2='{TODAY.year}']")
    page.click(f"#dam-cal-day-grid [data-arg='{TODAY}']")
    page.wait_for_selector("#dam-day-detail", state="visible")
    assert page.locator("#dam-day-detail .dam-day-slot").count() == 48
    assert page.locator("#dam-day-detail .dam-day-slot.missing").count() == 0
    assert "100.50" in page.inner_text("#dam-day-detail") and "not saved" in page.inner_text("#dam-day-detail")
    assert "dcal-new" in page.get_attribute(f"#dam-cal-day-grid [data-arg='{TODAY}']", "class")
    # Price explorer month tabs respond to clicks (they used inline onclick, which the CSP blocks).
    tabs = page.locator("#dam-month-tabs [data-action=selectDamMonth]")
    assert tabs.count() >= 1
    tabs.first.click()
    assert "active" in tabs.first.get_attribute("class")
    with page.expect_download() as dl:
        page.click("[data-action=downloadDamCsv]")
    text = Path(dl.value.path()).read_text(encoding="utf-8")
    assert text.startswith("timestamp,price_eur_mwh\n") and f"{TODAY} 23:30,100.5\n" in text

    page.click("[data-action=saveDamData]")
    _until(page, lambda: app.sql("SELECT COUNT(*) FROM dam_versions") == [(3,)], "saved")
    _until(page, lambda: not page.is_visible("#nav-dam-bubble"), "stale marker cleared after saving fresh data")
    assert page.eval_on_selector("#dash-dam-attention", "e => e.style.display") == "none"
    page.wait_for_selector("#dam-versions-tbody [data-action=damRestoreVersion]")
    assert "Saved" in page.inner_text("#dam-log-tbody")

    # Download an old version, then restore it.
    old_id = app.sql("SELECT id FROM dam_versions WHERE day_count = 5 AND source = 'upload'")[0][0]
    with page.expect_download():
        page.click(f"[data-action=damDownloadVersion][data-arg='{old_id}']")
    page.click(f"[data-action=damRestoreVersion][data-arg='{old_id}']")
    _until(page, lambda: app.sql("SELECT source, restored_from FROM dam_versions ORDER BY id DESC LIMIT 1")
           == [("rollback", old_id)], "restored")
    _until(page, lambda: "restored" in page.inner_text("#dam-status"), "restore message")
    _clean(page)


def test_saving_a_partial_file_asks_first(make_app, browser):
    app = make_app()
    admin = app.login(ADMIN)
    admin.put("/api/admin/dam", json=_payload("2026-01-01", "2026-01-02", "2026-01-03"))
    ctx = browser.new_context()
    pg = ctx.new_page()
    seen = []
    pg.on("dialog", lambda d: (seen.append(d.message), d.dismiss()))
    _sign_in(pg, app)
    _pane(pg, "dam")
    pg.select_option("#dam-unit", "mwh")
    pg.set_input_files("#dam-file-input", files=[{"name": "d.csv", "mimeType": "text/csv",
                                                  "buffer": _csv(["2026-01-01"], "90").encode()}])
    _until(pg, lambda: "Parsed 48 rows" in pg.inner_text("#dam-status"), "parsed")
    pg.click("[data-action=saveDamData]")
    _until(pg, lambda: bool(seen), "confirm dialog")
    assert "2 day(s)" in seen[0] and "2026-01-02 to 2026-01-03" in seen[0]
    pg.wait_for_timeout(300)
    assert app.sql("SELECT COUNT(*) FROM dam_versions") == [(2,)], "dismissed: nothing saved"
    ctx.close()
