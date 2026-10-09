"""11. The admin panel still works under the strict Content-Security-Policy.

Like test_10, but for admin.html (the largest page): every sidebar section and
the main actions in each are clicked through in headless Chromium, and the
browser must block nothing and report no script errors.
"""
import pytest

from conftest import ACME, ADMIN, DELTA, PASSWORD, VOLT
from test_10_pages_work import NEW, _WATCH_CSP, _clean, browser  # noqa: F401  (browser is a fixture)

PANES = ["dashboard", "suppliers", "profiles", "tariffs", "users", "login-activity", "messages", "dam",
         "regulated", "audit", "notices", "changelog", "reports"]


@pytest.fixture
def page(browser):
    ctx = browser.new_context(accept_downloads=True)
    ctx.add_init_script(_WATCH_CSP)
    pg = ctx.new_page()
    pg.errors = []
    pg.on("pageerror", lambda e: pg.errors.append(str(e)))
    pg.on("console", lambda m: pg.errors.append(m.text) if m.type == "error" else None)
    # confirm() → OK; prompt() → the text a test queued in pg.prompt_answer
    pg.prompt_answer = ""
    pg.on("dialog", lambda d: d.accept(pg.prompt_answer) if d.type == "prompt" else d.accept())
    yield pg
    ctx.close()


def _until(page, check, what, tries=100):
    for _ in range(tries):
        if check():
            return
        page.wait_for_timeout(100)
    raise AssertionError(f"timed out waiting for: {what}")


def _sign_in(page, app, email=ADMIN, password=PASSWORD, english=True):
    page.goto(f"{app.url}/admin.html", wait_until="networkidle")
    page.fill("#login-email", email)
    page.fill("#login-password", password)
    page.press("#login-password", "Enter")
    page.wait_for_selector("#login-overlay", state="hidden", timeout=15000)
    if english:
        page.click("[data-action=setLang][data-arg=en]")


def _dam_csv(days, start_day=1):
    """Half-hourly DAM prices (€/MWh) for January, in the format the upload box reads."""
    return "\n".join(f"2026-01-{d:02d} {s // 2:02d}:{30 * (s % 2):02d},{80 + s}"
                     for d in range(start_day, start_day + days) for s in range(48))


def _pane(page, name):
    page.click(f".nav-item[data-arg='{name}']")
    page.wait_for_selector(f"#pane-{name}.active", timeout=5000)
    assert "active" in page.get_attribute(f".nav-item[data-arg='{name}']", "class")   # sidebar highlight


def test_admin_sign_in_every_section_and_sign_out(make_app, page):
    app = make_app()
    page.goto(f"{app.url}/admin.html", wait_until="networkidle")
    page.click("#login-overlay a[data-action=showForgotForm]")
    page.wait_for_selector("#forgot-panel", state="visible")
    page.click("#forgot-panel a[data-action=hideForgotForm]")
    _sign_in(page, app)
    for p in PANES:
        _pane(page, p)
    page.click("[data-action=setLang][data-arg=el]")
    page.click("[data-action=setLang][data-arg=en]")
    page.click("[data-action=doLogout]")
    page.wait_for_selector("#login-overlay", state="visible")
    _clean(page)


def test_admin_tariff_review_and_status(make_app, page):
    app = make_app()
    _sign_in(page, app)
    _pane(page, "tariffs")
    for g in ("supplier", "pricing", "contract", "none"):
        page.click(f"[data-action=setTariffGroup][data-arg={g}]")
    page.select_option("#tf-pricing", "Fixed")                       # filter (change event)
    page.click("[data-action=clearTariffFilters]")
    assert page.input_value("#tf-pricing") == ""
    pending = app.sql("SELECT id FROM tariffs WHERE status = 'pending'")[0][0]
    page.click(f"[data-action=openReview][data-arg='{pending}']")
    page.wait_for_selector("#review-overlay", state="visible")
    page.click("#review-reject-btn")                                 # reject panel, custom reason, cancel
    page.wait_for_selector("#reject-reason-panel", state="visible")
    page.check("input[name=reject-preset][value=__custom__]")
    assert page.is_visible("#reject-custom-text")
    page.click("[data-action=cancelReject]")
    page.click("#review-approve-btn")
    _until(page, lambda: app.sql("SELECT status FROM tariffs WHERE id = ?", (pending,)) == [("approved",)], "approval")
    page.wait_for_timeout(500)
    page.click(f"[data-action=suspendTariff][data-arg='{pending}']")
    _until(page, lambda: app.sql("SELECT status FROM tariffs WHERE id = ?", (pending,)) == [("suspended",)], "suspend")
    page.wait_for_timeout(500)
    page.click(f"[data-action=setTariffStatus][data-arg='{pending}']")
    _until(page, lambda: app.sql("SELECT status FROM tariffs WHERE id = ?", (pending,)) == [("approved",)], "restore")
    _clean(page)


def test_admin_tariff_editor_and_documents(make_app, page):
    app = make_app()
    acme = app.login(ACME)
    tid = acme.get("/api/supplier/tariffs").json()[0]["id"]
    acme.post(f"/api/supplier/tariffs/{tid}/documents", files={"file": ("acme-terms.pdf", b"%PDF-1.4\n%%EOF\n", "application/pdf")})
    _sign_in(page, app)
    _pane(page, "tariffs")
    # View → edit → save
    page.click(f"[data-action=openViewer][data-arg='{tid}']")
    page.wait_for_selector("#editor-overlay", state="visible")
    page.click("[data-action=editorStartEdit]")
    page.fill("#edit-name", "Renamed by admin")
    page.click("[data-action=saveTariff]")
    _until(page, lambda: app.sql("SELECT name FROM tariffs WHERE id = ?", (tid,)) == [("Renamed by admin",)], "save")
    page.wait_for_selector("#editor-overlay", state="hidden")
    # New tariff: every dropdown, discounts and tiers, then cancel via the backdrop
    page.click("[data-action=openEditorNew]")
    page.wait_for_selector("#editor-overlay", state="visible")
    page.select_option("#edit-contract", "Commercial")
    page.select_option("#edit-voltage", "MV")
    page.select_option("#edit-duration-type", "fixed")
    assert page.is_visible("#duration-months-field")
    page.select_option("#edit-fpa-source", "custom")
    assert page.is_visible("#fpa-custom-field")
    page.click("[data-action=addDiscount][data-arg=standing]")
    page.click("[data-action=addDiscount][data-arg=energy]")
    n = page.locator("[data-action=removeDiscountRow]").count()
    assert n == 2
    page.locator("[data-action=removeDiscountRow]").first.click()
    assert page.locator("[data-action=removeDiscountRow]").count() == 1
    page.select_option("#edit-pricing", "Variable")
    t = page.locator("#tier-rows [data-action=removeTierRow]").count()
    page.click("[data-action=addTierRow]")
    assert page.locator("#tier-rows [data-action=removeTierRow]").count() == t + 1
    page.locator("#tier-rows [data-action=removeTierRow]").last.click()
    page.click("#editor-overlay", position={"x": 5, "y": 5})         # backdrop; unsaved → confirm → OK
    page.wait_for_selector("#editor-overlay", state="hidden")
    # Documents
    page.click(f"[data-action=openAdminDocs][data-arg='{tid}']")
    page.wait_for_selector("#adocs-overlay", state="visible")
    with page.expect_download() as dl:
        page.locator("#adocs-list [data-action=downloadDoc]").first.click()
    assert dl.value.suggested_filename == "acme-terms.pdf"
    page.click("#adocs-overlay", position={"x": 5, "y": 5})
    page.wait_for_selector("#adocs-overlay", state="hidden")
    _clean(page)


def _field_msg(page, sel):
    el = page.locator(sel).first
    assert "field-invalid" in (el.get_attribute("class") or ""), f"{sel} not highlighted"
    return el.evaluate("e => e._errMsg ? e._errMsg.textContent : ''")


def _typed(page, sel, text):
    page.locator(sel).first.fill("")
    page.locator(sel).first.type(text)
    return page.locator(sel).first.input_value()


def test_admin_number_boxes_take_plain_numbers(make_app, page):
    app = make_app()
    _sign_in(page, app)
    _pane(page, "regulated")
    assert _typed(page, "#reg-lv", "-0.02") == "0.02"                 # network charge can't be negative
    assert _typed(page, "#reg-fpa-lv", "-0.02") == "-0.02"            # a negative fuel adjustment is valid
    assert _typed(page, "#reg-pso", "1e3") == "13"
    _pane(page, "tariffs")
    page.click("[data-action=openEditorNew]")
    page.click("[data-action=addDiscount][data-arg=energy]")
    pct = "#energy-discounts .discount-row input >> nth=1"
    months = "#energy-discounts .discount-row input >> nth=2"
    assert _typed(page, pct, "1e5") == "15"
    assert _typed(page, months, "-12") == "12"
    page.select_option("#edit-pricing", "Dynamic")
    assert _typed(page, "#var-adder", "-0.01") == "-0.01"
    page.locator(pct).fill("5e1")                                     # pasted: cleaned up
    assert page.locator(pct).input_value() == "50"
    _clean(page)


def test_admin_editor_highlights_each_wrong_field(make_app, page):
    app = make_app()
    _sign_in(page, app)
    _pane(page, "tariffs")
    page.click("[data-action=openEditorNew]")
    page.wait_for_selector("#editor-overlay", state="visible")
    page.fill("#edit-name", "")
    page.fill("#edit-mdm", "")
    page.fill("#edit-standing", "1500")
    page.click("[data-action=addDiscount][data-arg=standing]")
    page.locator("#standing-discounts .discount-row input >> nth=1").fill("")
    before = app.sql("SELECT COUNT(*) FROM tariffs")[0][0]
    page.click("[data-action=saveTariff]")
    assert _field_msg(page, "#edit-name") == "Please provide the tariff name."
    assert _field_msg(page, "#edit-mdm") == "Please enter a value."
    assert _field_msg(page, "#edit-standing") == "This cannot be more than 1000."
    assert "remove this discount" in _field_msg(page, "#standing-discounts .discount-row input >> nth=1")
    assert "highlighted fields (4)" in page.inner_text("#editor-status")
    assert app.sql("SELECT COUNT(*) FROM tariffs")[0][0] == before, "saved despite errors"
    page.type("#edit-name", "Fixed later")
    assert "field-invalid" not in (page.get_attribute("#edit-name", "class") or "")
    page.locator("[data-action=removeDiscountRow]").click()
    # Tiers: a missing limit before the last tier, limits out of order
    page.select_option("#edit-pricing", "Variable")
    page.click("[data-action=addTierRow]")
    page.click("[data-action=addTierRow]")
    rows = page.locator("#tier-rows .tier-row")
    for i, (up, rate) in enumerate((("1000", "0.2"), ("", "0.2"), ("", "0.25"))):
        rows.nth(i).locator(".tier-upto").fill(up)
        rows.nth(i).locator(".tier-rate").fill(rate)
    page.fill("#edit-mdm", "0")
    page.fill("#edit-standing", "5")
    page.click("[data-action=saveTariff]")
    assert "Only the last tier" in _field_msg(page, "#tier-rows .tier-row >> nth=1 >> .tier-upto")
    rows.nth(1).locator(".tier-upto").fill("500")
    page.click("[data-action=saveTariff]")
    assert "higher than the one before" in _field_msg(page, "#tier-rows .tier-row >> nth=1 >> .tier-upto")
    # In Greek
    page.click("[data-action=setLang][data-arg=el]")
    page.fill("#edit-name", "")
    page.click("[data-action=saveTariff]")
    assert _field_msg(page, "#edit-name") == "Παρακαλώ δώστε το όνομα της διατίμησης."
    _clean(page)


def test_admin_editor_places_server_errors_on_the_field(make_app, page):
    app = make_app({"TARIFF_MAX_ENERGY_RATE": "1"})
    _sign_in(page, app)
    _pane(page, "tariffs")
    page.click("[data-action=openEditorNew]")
    page.fill("#edit-name", "Server check")
    page.fill("#fix-rate", "2")
    page.click("[data-action=saveTariff]")
    page.wait_for_selector("#fix-rate.field-invalid", timeout=10000)
    assert _field_msg(page, "#fix-rate") == "This cannot be more than 1."
    page.fill("#fix-rate", "0.5")
    page.click("[data-action=saveTariff]")
    page.wait_for_selector("#editor-overlay", state="hidden", timeout=10000)
    assert app.sql("SELECT 1 FROM tariffs WHERE name = 'Server check'")
    _clean(page)


def test_admin_regulated_refusal_is_shown_on_the_field(make_app, page):
    app = make_app()
    before = app.sql("SELECT lv, mdm FROM regulated")
    _sign_in(page, app)
    _pane(page, "regulated")
    page.fill("#reg-lv", "9")
    page.fill("#reg-mdm", "1500")
    page.click("[data-action=saveRegulated]")
    page.click("#reg-change-overlay [data-action=confirmRegChange]")
    page.wait_for_selector("#reg-lv.field-invalid", timeout=10000)
    assert _field_msg(page, "#reg-lv") == "This cannot be more than 5."
    assert _field_msg(page, "#reg-mdm") == "This cannot be more than 1000."
    assert "highlighted fields (2)" in page.inner_text("#reg-save-status")
    assert app.sql("SELECT lv, mdm FROM regulated") == before, "refused values were stored"
    page.fill("#reg-lv", "0.04")
    page.fill("#reg-mdm", "0.9")
    page.click("[data-action=saveRegulated]")
    page.click("#reg-change-overlay [data-action=confirmRegChange]")
    _until(page, lambda: app.sql("SELECT lv, mdm FROM regulated") == [(0.04, 0.9)], "valid values saved")
    assert page.locator("#pane-regulated .field-invalid").count() == 0
    _clean(page)


def test_admin_regulated_changes_are_checked_before_saving(make_app, page):
    # Seed: grid LV 0.045 > MV 0.038 > HV 0.030; FPA 0.06 / 0.055 / 0.05; PSO 0.005.
    app = make_app()
    before = app.sql("SELECT lv, mv, hv, fpaLV, fpaMV, fpaHV, pso FROM regulated")
    _sign_in(page, app)
    _pane(page, "regulated")
    # Grid usage out of voltage order is refused on the page, no window
    page.fill("#reg-mv", "0.05")
    page.click("[data-action=saveRegulated]")
    page.wait_for_selector("#reg-mv.field-invalid", timeout=5000)
    assert _field_msg(page, "#reg-mv") == "Grid usage must fall with voltage: LV > MV > HV."
    assert not page.is_visible("#reg-change-overlay")
    # A changed value asks first, with the % change; Cancel saves nothing
    page.fill("#reg-mv", "0.0399")
    page.fill("#reg-pso", "0.004")
    page.click("[data-action=saveRegulated]")
    page.wait_for_selector("#reg-change-overlay", state="visible")
    text = page.inner_text("#reg-change-list")
    assert "The MV grid usage value is now 5.0% higher than the previous one (0.038 → 0.0399)." in text
    assert "The PSO value is now 20.0% lower than the previous one (0.005 → 0.004)." in text
    assert "Is this correct?" in page.inner_text("#reg-change-overlay")
    page.click("#reg-change-overlay [data-action=cancelRegChange]")
    page.wait_for_selector("#reg-change-overlay", state="hidden")
    assert page.inner_text("#reg-save-status") == "Not saved."
    assert app.sql("SELECT lv, mv, hv, fpaLV, fpaMV, fpaHV, pso FROM regulated") == before
    # Confirm saves; the new values become the "previous" ones
    page.click("[data-action=saveRegulated]")
    page.click("#reg-change-overlay [data-action=confirmRegChange]")
    _until(page, lambda: app.sql("SELECT mv, pso FROM regulated") == [(0.0399, 0.004)], "confirmed values saved")
    # The 0.4735-for-0.04735 typo: flagged both as a big jump and as out of order
    page.fill("#reg-fpa-mv", "0.55")
    page.click("[data-action=saveRegulated]")
    page.wait_for_selector("#reg-change-overlay", state="visible")
    text = page.inner_text("#reg-change-list")
    assert "The MV FPA value is now 900.0% higher than the previous one (0.055 → 0.55)." in text
    assert "not in the usual order LV > MV > HV" in text
    page.click("#reg-change-overlay [data-action=cancelRegChange]")
    assert app.sql("SELECT fpaMV FROM regulated") == [(0.055,)]
    # Unchanged values save without asking
    page.fill("#reg-fpa-mv", "0.055")
    page.click("[data-action=saveRegulated]")
    _until(page, lambda: page.inner_text("#reg-save-status") == "Saved ✓", "saved without asking")
    assert not page.is_visible("#reg-change-overlay")
    _clean(page)


def test_admin_suppliers_and_users(make_app, page):
    app = make_app()
    app.sql("UPDATE users SET failed_attempts = 3, locked_until = '2999-01-01T00:00:00+00:00' WHERE email = ?", (VOLT,))
    _sign_in(page, app)
    _pane(page, "suppliers")
    page.fill("#sup-name", "Browser Test Energy")
    page.press("#sup-name", "Enter")                                  # Enter adds
    _until(page, lambda: app.sql("SELECT 1 FROM suppliers WHERE name = 'Browser Test Energy'"), "supplier added")
    page.locator("[data-action=openSupModal][data-sup='Browser Test Energy']").click()
    page.wait_for_selector("#sup-modal-overlay", state="visible")
    page.fill("#sup-tel", "+357 22 123456")
    page.click("#sup-regulated")                                      # asks for confirmation first
    page.wait_for_selector("#regulated-confirm-overlay", state="visible")
    assert not page.is_checked("#sup-regulated"), "checkbox changed before confirming"
    page.click("[data-action=confirmRegulatedToggle]")
    assert page.is_checked("#sup-regulated")
    page.click("#sup-regulated")                                      # untick, but cancel: stays ticked
    page.click("[data-action=closeRegulatedConfirm] >> nth=0")
    assert page.is_checked("#sup-regulated")
    page.click("[data-action=saveSupplierDetails]")
    _until(page, lambda: app.sql("SELECT tel, regulated FROM suppliers WHERE name = 'Browser Test Energy'") == [("+357 22 123456", 1)], "supplier saved")
    page.wait_for_selector("#sup-modal-overlay", state="hidden")
    page.locator("[data-action=openSupModal][data-sup='Browser Test Energy']").click()   # untick and confirm
    page.click("#sup-regulated")
    page.click("[data-action=confirmRegulatedToggle]")
    assert not page.is_checked("#sup-regulated")
    page.click("[data-action=saveSupplierDetails]")
    _until(page, lambda: app.sql("SELECT regulated FROM suppliers WHERE name = 'Browser Test Energy'") == [(0,)], "regulated off")
    page.wait_for_selector("#sup-modal-overlay", state="hidden")
    page.wait_for_timeout(300)
    page.locator("[data-action=removeSupplier][data-sup='Browser Test Energy']").click()
    _until(page, lambda: not app.sql("SELECT 1 FROM suppliers WHERE name = 'Browser Test Energy'"), "supplier removed")
    # Users
    _pane(page, "users")
    page.click("[data-action=usersToggleForm]")
    page.fill("#inv-email", "not-an-email")                          # refused: a readable reason, not [object Object]
    page.select_option("#inv-supplier", "Acme Energy")
    page.click("[data-action=usersInvite]")
    _until(page, lambda: page.inner_text("#users-form-msg") != "", "invite refusal")
    assert "object" not in page.inner_text("#users-form-msg").lower()
    page.fill("#inv-email", "new.user@example.com")
    page.select_option("#inv-supplier", "Acme Energy")
    page.click("[data-action=usersInvite]")
    _until(page, lambda: app.sql("SELECT 1 FROM users WHERE email = 'new.user@example.com'"), "user invited")
    uid = app.user_id(VOLT)
    page.click(f"[data-action=usersUnlock][data-arg='{uid}']")
    _until(page, lambda: app.sql("SELECT locked_until FROM users WHERE id = ?", (uid,)) == [(None,)], "unlock")
    page.wait_for_timeout(300)
    page.click(f"[data-action=usersToggleOtp][data-arg='{uid}']")
    _until(page, lambda: app.sql("SELECT otp_enabled FROM users WHERE id = ?", (uid,)) == [(1,)], "otp on")
    page.wait_for_timeout(300)
    page.click(f"[data-action=usersSetStatus][data-arg='{uid}'][data-arg2=false]")
    _until(page, lambda: app.sql("SELECT is_active FROM users WHERE id = ?", (uid,)) == [(0,)], "deactivate")
    page.wait_for_timeout(300)
    page.click(f"[data-action=usersSetStatus][data-arg='{uid}'][data-arg2=true]")
    _until(page, lambda: app.sql("SELECT is_active FROM users WHERE id = ?", (uid,)) == [(1,)], "activate")
    page.wait_for_timeout(300)
    page.click(f"[data-action=usersReinvite][data-arg='{uid}']")
    new_uid = app.user_id("new.user@example.com")
    page.wait_for_timeout(300)
    page.click(f"[data-action=usersDelete][data-arg='{new_uid}']")
    _until(page, lambda: not app.sql("SELECT 1 FROM users WHERE id = ?", (new_uid,)), "user deleted")
    # Login activity
    _pane(page, "login-activity")
    page.click("[data-action=loginActivityLoad]")
    page.fill("#la-filter-email", "acme")
    page.select_option("#la-filter-result", index=1)
    _clean(page)


def test_admin_profiles(make_app, page):
    app = make_app()
    admin = app.login(ADMIN)
    prof = admin.get("/api/admin/profiles").json()[0]
    r = admin.post("/api/admin/profiles", json={**{k: v for k, v in prof.items() if k != "id"}, "name": "Spare profile"})
    spare = r.json()["id"]
    _sign_in(page, app)
    _pane(page, "profiles")
    page.locator(f"[data-action=selectProfileMonth][data-arg='{prof['id']}']").nth(3).click()
    page.prompt_answer = "Renamed profile"
    page.click(f"[data-action=editProfileName][data-arg='{spare}']")
    _until(page, lambda: app.sql("SELECT name FROM profiles WHERE id = ?", (spare,)) == [("Renamed profile",)], "rename")
    page.wait_for_timeout(300)
    page.click(f"[data-action=deleteProfile][data-arg='{spare}']")
    _until(page, lambda: not app.sql("SELECT 1 FROM profiles WHERE id = ?", (spare,)), "profile deleted")
    page.click("[data-action=parseAndAddProfile]")                    # empty input → a message, not a crash
    _clean(page)


def test_admin_messages_and_schedules(make_app, page):
    app = make_app()
    _sign_in(page, app)
    _pane(page, "messages")
    page.check("input[name=msg-audience][value=selected]")
    page.check("input[name=msg-audience][value=all]")
    page.fill("#msg-subject", "Browser test notice")
    page.fill("#msg-body", "Hello suppliers")
    page.click("[data-action=sendMessage]")
    _until(page, lambda: app.sql("SELECT id FROM messages WHERE subject = 'Browser test notice'"), "message sent")
    mid = app.sql("SELECT id FROM messages WHERE subject = 'Browser test notice'")[0][0]
    page.wait_for_selector(f"[data-action=openMsgStatusModal][data-arg='{mid}']")
    page.locator(f"[data-action=openMsgStatusModal][data-arg='{mid}']").first.click()
    page.wait_for_selector("#msg-status-overlay", state="visible")
    page.click("#msg-status-overlay", position={"x": 5, "y": 5})
    page.wait_for_selector("#msg-status-overlay", state="hidden")
    page.click(f"[data-action=archiveMessage][data-arg='{mid}'][data-arg2=true]")
    _until(page, lambda: app.sql("SELECT archived FROM messages WHERE id = ?", (mid,)) == [(1,)], "archive")
    page.wait_for_timeout(300)
    page.click(f"[data-action=archiveMessage][data-arg='{mid}'][data-arg2=false]")
    _until(page, lambda: app.sql("SELECT archived FROM messages WHERE id = ?", (mid,)) == [(0,)], "restore")
    page.wait_for_timeout(300)
    page.click(f"[data-action=deleteMessageEntry][data-arg='{mid}']")
    _until(page, lambda: not app.sql("SELECT 1 FROM messages WHERE id = ?", (mid,)), "message deleted")
    # Scheduled notifications
    page.locator("[data-action=schedToggleForm]").first.click()
    page.wait_for_selector("#sched-form", state="visible")
    page.fill("#sched-subject", "Monthly reminder")
    page.fill("#sched-body", "Please check your tariffs.")
    page.check("input[name=sched-audience][value=selected]")
    page.check("input[name=sched-audience][value=all]")
    page.click("#sched-save-btn")
    _until(page, lambda: app.sql("SELECT id FROM scheduled_notifications"), "schedule saved")
    sid = app.sql("SELECT id FROM scheduled_notifications")[0][0]
    page.wait_for_selector(f"[data-action=toggleScheduleEnabled][data-arg='{sid}']")
    page.click(f"[data-action=toggleScheduleEnabled][data-arg='{sid}'][data-arg2=false]")
    _until(page, lambda: app.sql("SELECT enabled FROM scheduled_notifications WHERE id = ?", (sid,)) == [(0,)], "pause")
    page.wait_for_timeout(300)
    page.click(f"[data-action=editSchedule][data-arg='{sid}']")
    page.wait_for_selector("#sched-form", state="visible")
    assert page.input_value("#sched-subject") == "Monthly reminder"
    page.locator("#sched-form [data-action=schedToggleForm]").click()
    page.click(f"[data-action=deleteSchedule][data-arg='{sid}']")
    _until(page, lambda: not app.sql("SELECT 1 FROM scheduled_notifications WHERE id = ?", (sid,)), "schedule deleted")
    _clean(page)


def test_admin_dam_regulated_audit_notices_reports_changelog(make_app, page):
    app = make_app()
    acme = app.login(ACME)
    tid = acme.get("/api/supplier/tariffs").json()[0]["id"]
    app.anon().post("/api/public/report-tariff", json={"tariff_id": tid, "category": "other", "note": "Price out of date",
                                                      "reporter_email": "visitor@example.com"})
    _sign_in(page, app)
    # DAM prices: load a file via the picker and another by drag-and-drop, then
    # calendar → month → days, back; week navigation; save; export
    _pane(page, "dam")
    page.select_option("#dam-unit", "mwh")
    page.set_input_files("#dam-file-input", files=[{"name": "jan-a.csv", "mimeType": "text/csv",
                                                    "buffer": _dam_csv(7).encode()}])
    _until(page, lambda: "Parsed 336 rows" in page.inner_text("#dam-status"), "file picker upload")
    page.evaluate("""csv => { const dt = new DataTransfer();
        dt.items.add(new File([csv], 'jan-b.csv', {type: 'text/csv'}));
        document.getElementById('dam-dropzone').dispatchEvent(new DragEvent('drop', {dataTransfer: dt, bubbles: true, cancelable: true})); }""",
                  _dam_csv(7, start_day=8))
    _until(page, lambda: "Parsed 672 rows" in page.inner_text("#dam-status"), "drag-and-drop upload")
    page.click("[data-action=saveDamData]")
    _until(page, lambda: app.sql("SELECT damRowCount FROM dam_data") == [(672,)], "DAM saved")
    page.locator("#dam-cal-mon-grid [data-action=damOpenMonth]").first.click()
    page.wait_for_selector("#dam-cal-day-view", state="visible")
    page.click("[data-action=damBackToMonths]")
    page.wait_for_selector("#dam-cal-month-view", state="visible")
    if page.is_visible("#dam-next-week"):
        page.click("#dam-next-week")
        page.click("#dam-prev-week")
    with page.expect_download():
        page.click("[data-action=exportDAM][data-arg=monthly]")
    # Regulated charges: live preview, save, history chart
    _pane(page, "regulated")
    page.fill("#reg-preview-kwh", "4000")
    page.fill("#reg-lv", "0.0451")
    page.click("[data-action=saveRegulated]")
    page.click("#reg-change-overlay [data-action=confirmRegChange]")
    _until(page, lambda: page.inner_text("#reg-save-status") != "", "regulated saved")
    page.click("[data-action=openRegHistory][data-arg=grid]")
    page.wait_for_selector("#reg-history-overlay", state="visible")
    page.click("[data-action=closeRegHistory]")
    page.wait_for_selector("#reg-history-overlay", state="hidden")
    # Audit calculator
    _pane(page, "audit")
    page.select_option("#audit-tariff-sel", index=1)
    page.fill("#audit-kwh", "4000")
    page.click("[data-action=runAudit]")
    page.wait_for_selector("#audit-results", state="visible", timeout=10000)
    # Notices: formatting buttons, save; sample-invoice toggle
    _pane(page, "notices")
    page.click("#assumptions-en")
    page.keyboard.type("Test")
    page.keyboard.press("Control+A")
    page.click("[data-action=fmtDoc][data-arg=assumptions-en][data-arg2=bold]")
    assert "<b>" in page.inner_html("#assumptions-en") or "<strong>" in page.inner_html("#assumptions-en")
    page.click("[data-action=saveNotices]")
    _until(page, lambda: page.inner_text("#notices-status") != "", "notices saved")
    page.click("#sample-invoice-enabled")
    _until(page, lambda: page.inner_text("#sample-invoice-status") != "", "sample invoice toggled")
    # Reported issues
    _pane(page, "reports")
    rid = app.sql("SELECT id FROM tariff_reports")[0][0]
    page.select_option("#rp-filter-status", index=0)
    page.click(f"[data-action=setReportStatus][data-arg='{rid}'][data-arg2=reviewed]")
    _until(page, lambda: app.sql("SELECT status FROM tariff_reports WHERE id = ?", (rid,)) == [("reviewed",)], "report status")
    # Changelog
    _pane(page, "changelog")
    page.select_option("#cl-filter-action", index=1)
    with page.expect_download():
        page.click("[data-action=exportChangelog]")
    _clean(page)


def test_admin_account_idle_and_expired_password(make_app, page):
    app = make_app()
    _sign_in(page, app)
    page.click("[data-action=openAccountModal]")
    page.wait_for_selector("#acct-overlay", state="visible")
    page.fill("#acct-cur-pw", PASSWORD)
    page.fill("#acct-new-pw", NEW)
    page.fill("#acct-confirm-pw", NEW)
    page.click("[data-action=doUpdatePassword]")
    _until(page, lambda: page.inner_text("#acct-pw-msg") != "", "password message")
    app.login(ADMIN, NEW)
    page.click("#acct-overlay", position={"x": 5, "y": 5})
    page.wait_for_selector("#acct-overlay", state="hidden")
    page.evaluate("_showIdleWarning()")
    page.wait_for_selector("#idle-warning-overlay", state="visible")
    page.click("[data-action=dismissIdleWarning]")
    page.wait_for_selector("#idle-warning-overlay", state="hidden")
    _clean(page)


def test_admin_expired_password_and_code_sign_in(make_app, page):
    app = make_app()
    app.sql("UPDATE users SET must_change_password = 1 WHERE email = 'admin2@demo.local'")
    _sign_in(page, app, "admin2@demo.local", english=False)
    page.wait_for_selector("#pw-expired-overlay", state="visible", timeout=15000)
    page.fill("#pwx-cur-pw", PASSWORD)
    page.fill("#pwx-new-pw", NEW)
    page.fill("#pwx-confirm-pw", NEW)
    page.click("[data-action=doUpdatePasswordExpired]")
    page.wait_for_selector("#pw-expired-overlay", state="hidden", timeout=15000)
    page.click("[data-action=doLogout]")
    # Sign-in with an emailed code
    admin = app.login(ADMIN)
    admin.patch(f"/api/admin/users/{app.user_id(ADMIN)}/otp", json={"otp_enabled": True})
    page.wait_for_selector("#login-overlay", state="visible")
    page.fill("#login-email", ADMIN)
    page.fill("#login-password", PASSWORD)
    page.click("#login-btn")
    page.wait_for_selector("#otp-panel", state="visible")
    code = app.sql("SELECT code FROM otp_codes WHERE email = ? ORDER BY id DESC", (ADMIN,))[0][0]
    page.type("#otp-code", code[:3] + "x" + code[3:])
    assert page.input_value("#otp-code") == code
    page.press("#otp-code", "Enter")
    page.wait_for_selector("#login-overlay", state="hidden", timeout=15000)
    _clean(page)
