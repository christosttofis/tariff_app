"""10. The converted pages still work, under the strict Content-Security-Policy.

Plan B moves each page's code out of the page and stops the browser from running
any code written inside a page. These tests click through each converted page in
headless Chromium and check that every button and form still does its job, and
that the browser blocked nothing (no CSP violations, no script errors).
"""
import pytest
from playwright.sync_api import sync_playwright

from conftest import ACME, DELTA, PASSWORD, VOLT

NEW = "Fresh-Passw0rd!"

# Records anything the browser refuses under the CSP, before any page script runs.
_WATCH_CSP = """
window.__csp = [];
document.addEventListener('securitypolicyviolation',
  e => window.__csp.push(e.violatedDirective + ' ' + (e.blockedURI || 'inline') + ' ' + (e.sourceFile || '') + ':' + e.lineNumber));
"""


@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        b = p.chromium.launch()
        yield b
        b.close()


@pytest.fixture
def page(browser):
    ctx = browser.new_context()
    ctx.add_init_script(_WATCH_CSP)
    pg = ctx.new_page()
    pg.errors = []
    pg.on("pageerror", lambda e: pg.errors.append(str(e)))
    pg.on("console", lambda m: pg.errors.append(m.text) if m.type == "error" else None)
    yield pg
    ctx.close()


def _clean(page):
    """Nothing blocked, nothing crashed."""
    violations = page.evaluate("window.__csp")
    assert not violations, f"blocked by CSP: {violations}"
    # The browser also logs every HTTP error status as a console error (e.g. the 401 from
    # "am I signed in?" before signing in). Those are the server's normal answers; only
    # script errors and other console errors count here.
    errors = [e for e in page.errors if not e.startswith("Failed to load resource: the server responded with a status of")]
    assert not errors, f"browser errors: {errors}"


# ── customer.html (public calculator) ────────────────────────────────────────
OVERLAYS = ["est-overlay", "meth-modal-overlay", "report-overlay", "notices-overlay", "reg-info-overlay",
            "sample-invoice-overlay", "sup-contact-overlay", "vulnerable-overlay"]


@pytest.fixture(scope="module")
def calc_app(app, admin):
    # Show the sample-invoice button on every card, so its handler is exercised too.
    assert admin.put("/api/admin/sample-invoice", json={"enabled": True}).status_code == 200
    return app


def _open_customer(page, app):
    page.goto(f"{app.url}/customer.html", wait_until="networkidle")
    page.wait_for_selector("#app", state="visible")


def _results(page, kwh="5000"):
    page.fill("#annual-kwh", kwh)
    page.wait_for_selector(".rank-card", timeout=15000)


def _shown(page, overlay):
    page.wait_for_selector(f"#{overlay}", state="visible", timeout=5000)


def _hidden(page, overlay):
    page.wait_for_selector(f"#{overlay}", state="hidden", timeout=5000)


def test_customer_settings_and_results(calc_app, page):
    _open_customer(page, calc_app)
    page.click("#lang-btn-en")
    assert "active" in page.get_attribute("#lang-btn-en", "class")
    _results(page)
    first = page.inner_text(".rank-card")
    page.click("#tab-ci")                                   # commercial customer
    assert "active" in page.get_attribute("#tab-ci", "class")
    page.wait_for_timeout(800)
    page.click("#tab-domestic")
    page.wait_for_timeout(800)
    page.select_option("#sel-pricing", "Fixed")             # pricing filter (change event)
    page.wait_for_timeout(800)
    assert all("Fixed" in c or "Σταθερ" in c for c in page.locator(".rank-card").all_inner_texts())
    page.select_option("#sel-pricing", "All")
    page.click("#tab-ci")
    page.select_option("#sel-voltage", "MV")                # voltage (change event)
    page.click("#le-gt") if page.is_visible("#le-gt") else None
    page.click("#tab-domestic")
    page.click("#offers-check")                             # checkbox (change event)
    page.click("#offers-check")
    page.click("#btn-monthly")                              # monthly mode + billing period
    assert page.is_visible("#monthly-kwh")
    page.fill("#monthly-kwh", "400")
    page.click("#bp-btn-2")
    assert "active" in page.get_attribute("#bp-btn-2", "class")
    page.click("#bp-btn-1")
    page.click("#btn-annual")
    _results(page, "6000")
    assert page.inner_text(".rank-card") != "" and first
    # Typing in the consumption box collapses the connection card (focus event)...
    assert page.get_attribute("#cc-head", "aria-expanded") == "false"
    page.click("#cc-head")                                  # ...a click opens it again...
    assert page.get_attribute("#cc-head", "aria-expanded") == "true"
    page.focus("#cc-head")
    page.keyboard.press("Enter")                            # ...and the keyboard works too
    assert page.get_attribute("#cc-head", "aria-expanded") == "false"
    page.click("#lang-btn-el")
    assert "active" in page.get_attribute("#lang-btn-el", "class")
    _clean(page)


@pytest.mark.parametrize("box, mode", [("#annual-kwh", "annual"), ("#monthly-kwh", "monthly")])
def test_customer_consumption_box_takes_plain_amounts_only(calc_app, page, box, mode):
    _open_customer(page, calc_app)
    page.click(f"#btn-{mode}")
    for typed, expected in (("-500", "500"), ("+5e3", "53"), ("1.5", "1.5"), ("5000", "5000")):
        page.fill(box, "")
        page.type(box, typed)                         # "-", "+" and "e" keys are ignored
        assert page.input_value(box) == expected, f"typed {typed!r}"
    for pasted, expected in (("-500", ""), ("1e9", "5000000"), ("5e3", "5000")):
        page.fill(box, pasted)                        # pasted values are cleaned up
        assert page.input_value(box) == expected, f"pasted {pasted!r}"
    page.fill(box, "4000")
    page.wait_for_selector(".rank-card", timeout=15000)
    _clean(page)


def test_customer_tariff_card_and_its_buttons(calc_app, page):
    _open_customer(page, calc_app)
    _results(page)
    page.click(".rank-header")                              # open the first card
    page.wait_for_selector(".rank-detail.open .mo-table")
    assert page.locator(".rank-detail.open canvas").count() >= 1
    box = page.locator(".rank-detail.open input[type=checkbox][data-change=toggleDiscount]")
    if box.count():
        box.first.click()                                   # discount toggle (change event)
        page.wait_for_timeout(600)
        assert page.locator(".rank-detail.open .mo-table").count()
    page.click(".rank-detail.open [data-action=openSampleInvoice]")
    _shown(page, "sample-invoice-overlay")
    assert "€" in page.inner_text("#sample-invoice-body")
    page.click("#sample-invoice-overlay [data-action=closeSampleInvoice]")
    _hidden(page, "sample-invoice-overlay")
    page.click(".rank-detail.open button[data-action=openSupContact]")
    _shown(page, "sup-contact-overlay")
    page.click("#sup-contact-overlay", position={"x": 5, "y": 5})   # click on the dimmed backdrop
    _hidden(page, "sup-contact-overlay")
    page.click(".rank-card .rank-sup-pill")                 # supplier pill inside the header...
    _shown(page, "sup-contact-overlay")
    page.click("#sup-contact-overlay [data-action=closeSupContact]")
    assert page.locator(".rank-detail.open").count() == 1   # ...didn't also toggle the card
    trigger = page.locator(".rank-detail.open .reg-info-trigger")
    if trigger.count():
        trigger.first.click()
        _shown(page, "reg-info-overlay")
        page.click("#reg-info-overlay [data-action=closeRegInfo]")
        _hidden(page, "reg-info-overlay")
    page.focus(".rank-header")
    page.keyboard.press("Enter")                            # keyboard closes the card again
    page.wait_for_timeout(300)
    assert page.locator(".rank-detail.open").count() == 0
    _clean(page)


def test_customer_report_an_issue(calc_app, page):
    before = calc_app.sql("SELECT COUNT(*) FROM tariff_reports")[0][0]
    _open_customer(page, calc_app)
    _results(page)
    page.click(".rank-header")
    page.click(".rank-detail.open [data-action=reportTariff]")
    _shown(page, "report-overlay")
    assert page.inner_text("#report-tariff-name")
    page.fill("#report-note", "The price shown is out of date.")
    page.fill("#report-email", "visitor@example.com")
    page.click("#report-submit-btn")
    page.wait_for_selector("#report-success", state="visible")
    assert calc_app.sql("SELECT COUNT(*) FROM tariff_reports")[0][0] == before + 1
    page.click("#report-overlay [data-action=closeReportIssue]")
    _hidden(page, "report-overlay")
    page.click("#footer-report-issue-btn")                  # general (not tariff-specific) report
    _shown(page, "report-overlay")
    page.click("#report-btn-cancel")
    _hidden(page, "report-overlay")
    _clean(page)


def test_customer_estimator(calc_app, page):
    _open_customer(page, calc_app)
    page.click("#est-trigger-btn")
    _shown(page, "est-overlay")
    page.locator("#est-ac-group .est-radio").last.click()   # generated radio options
    assert "active" in page.locator("#est-ac-group .est-radio").last.get_attribute("class")
    page.click("#est-calc-btn")
    page.wait_for_selector("#est-result-wrap", state="visible")
    page.click("#est-meth-link")
    _shown(page, "meth-modal-overlay")
    page.click("#meth-modal-overlay [data-action=closeEstMeth]")
    _hidden(page, "meth-modal-overlay")
    page.click("#est-use-btn")
    _hidden(page, "est-overlay")
    assert page.input_value("#annual-kwh") not in ("", "0")
    page.wait_for_selector(".rank-card", timeout=15000)
    page.click("#est-trigger-btn")
    page.click("#est-overlay", position={"x": 5, "y": 5})   # backdrop closes it
    _hidden(page, "est-overlay")
    _clean(page)


def test_customer_notices_vulnerable_and_footer(calc_app, page):
    _open_customer(page, calc_app)
    page.click("#notices-open-btn")
    _shown(page, "notices-overlay")
    for tab in ("about", "legal", "assumptions"):
        page.click(f"#ntab-{tab}")
        assert "active" in page.get_attribute(f"#ntab-{tab}", "class")
    page.click("#notices-overlay [data-action=closeNotices]")
    _hidden(page, "notices-overlay")
    # The row only shows when a vulnerable-customer tariff exists (none in the demo data).
    page.evaluate("document.getElementById('vulnerable-row').style.display='block'")
    page.click("#vulnerable-info-btn")
    _shown(page, "vulnerable-overlay")
    page.click("#vulnerable-overlay [data-action=closeVulnerableModal]")
    _hidden(page, "vulnerable-overlay")
    page.click("#a11y-toggle")
    assert page.evaluate("document.documentElement.classList.contains('a11y-mode')")
    page.click("#a11y-toggle")
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_selector("#back-to-top", state="visible")
    page.click("#back-to-top")
    # (Playwright's wait_for_function evaluates text as code, which the strict CSP rightly refuses.)
    for _ in range(50):
        if page.evaluate("window.scrollY") < 50:
            break
        page.wait_for_timeout(100)
    assert page.evaluate("window.scrollY") < 50, "back-to-top didn't scroll up"
    assert not any(page.is_visible(f"#{o}") for o in OVERLAYS)
    _clean(page)


# ── supplier.html (supplier portal) ──────────────────────────────────────────
def _visible(page, sel):
    return page.is_visible(sel)


def _sign_in(page, app, email=ACME, password=PASSWORD):
    page.goto(f"{app.url}/supplier.html", wait_until="networkidle")
    page.wait_for_selector("#login-overlay", state="visible")
    page.fill("#login-email", email)
    page.fill("#login-password", password)
    page.press("#login-password", "Enter")                  # Enter submits
    page.wait_for_selector("#app", state="visible", timeout=15000)


def test_supplier_sign_in_forgot_and_sign_out(make_app, page):
    app = make_app()
    page.goto(f"{app.url}/supplier.html", wait_until="networkidle")
    page.click("#login-overlay a[data-action=showForgotForm]")
    page.wait_for_selector("#forgot-panel", state="visible")
    page.fill("#forgot-email", ACME)
    page.click("#forgot-btn")
    for _ in range(50):
        if app.sql("SELECT COUNT(*) FROM password_resets WHERE email = ?", (ACME,))[0][0]:
            break
        page.wait_for_timeout(100)
    assert app.sql("SELECT COUNT(*) FROM password_resets WHERE email = ?", (ACME,))[0][0] == 1
    page.click("#forgot-panel a[data-action=hideForgotForm]")
    page.wait_for_selector("#login-email", state="visible")
    assert page.evaluate("location.hash") == "", "href='#' link jumped"
    page.fill("#login-email", ACME)
    page.fill("#login-password", PASSWORD)
    page.click("#login-btn")
    page.wait_for_selector("#app", state="visible", timeout=15000)
    page.click("[data-action=setLang][data-arg=en]:visible")
    page.click("[data-action=doLogout]")
    page.wait_for_selector("#login-overlay", state="visible")
    _clean(page)


def test_supplier_sign_in_with_a_code(make_app, page):
    app = make_app()
    admin = app.login("admin1@demo.local")
    admin.patch(f"/api/admin/users/{app.user_id(VOLT)}/otp", json={"otp_enabled": True})
    page.goto(f"{app.url}/supplier.html", wait_until="networkidle")
    page.fill("#login-email", VOLT)
    page.fill("#login-password", PASSWORD)
    page.click("#login-btn")
    page.wait_for_selector("#otp-panel", state="visible")
    code = app.sql("SELECT code FROM otp_codes WHERE email = ? ORDER BY id DESC", (VOLT,))[0][0]
    page.type("#otp-code", code[:3] + "ab" + code[3:])      # letters are stripped as you type
    assert page.input_value("#otp-code") == code
    page.press("#otp-code", "Enter")                         # Enter verifies
    page.wait_for_selector("#app", state="visible", timeout=15000)
    _clean(page)


def test_supplier_tariff_form(make_app, page):
    app = make_app()
    page.on("dialog", lambda d: d.accept())
    _sign_in(page, app)
    rows_before = page.locator("#tariff-tbody tr").count()
    page.click("[data-action=openForm]")
    page.wait_for_selector("#form-overlay", state="visible")
    page.fill("#edit-name", "Browser-test tariff")
    page.select_option("#edit-contract", "Commercial")       # change events
    page.select_option("#edit-voltage", "MV")
    page.select_option("#edit-duration-type", "fixed")
    assert _visible(page, "#duration-months-field")
    page.select_option("#edit-duration-type", "indefinite")
    page.select_option("#edit-fpa-source", "custom")
    assert _visible(page, "#fpa-custom-field")
    page.select_option("#edit-fpa-source", "global")
    page.click("[data-action=addDiscount][data-arg=standing]")
    page.click("[data-action=addDiscount][data-arg=energy]")
    assert page.locator(".discount-row").count() == 2
    page.locator("[data-action=removeDiscountRow]").first.click()
    assert page.locator(".discount-row").count() == 1
    page.locator("[data-action=removeDiscountRow]").first.click()
    page.select_option("#edit-pricing", "Variable")
    assert _visible(page, "#fields-variable")
    n = page.locator("#tier-rows [data-action=removeTierRow]").count()
    page.click("[data-action=addTierRow]")
    assert page.locator("#tier-rows [data-action=removeTierRow]").count() == n + 1
    page.locator("#tier-rows [data-action=removeTierRow]").last.click()
    assert page.locator("#tier-rows [data-action=removeTierRow]").count() == n
    page.select_option("#edit-pricing", "Fixed")
    page.fill("#fix-rate", "0.17")
    page.fill("#edit-standing", "3")
    page.click("#submit-btn")
    page.wait_for_selector("#form-overlay", state="hidden", timeout=15000)
    assert app.sql("SELECT status FROM tariffs WHERE name = 'Browser-test tariff'") == [("pending",)]
    page.wait_for_timeout(500)
    assert page.locator("#tariff-tbody tr").count() == rows_before + 1
    # Edit, then cancel; then delete (a never-published tariff is removed).
    row = page.locator("#tariff-tbody tr", has_text="Browser-test tariff")
    row.locator("[data-action=editTariff]").click()
    page.wait_for_selector("#form-overlay", state="visible")
    assert page.input_value("#edit-name") == "Browser-test tariff"
    page.locator("#form-overlay [data-action=closeForm]").first.click()
    page.wait_for_selector("#form-overlay", state="hidden")
    row.locator("[data-action=deleteTariff]").click()
    for _ in range(50):
        if not app.sql("SELECT 1 FROM tariffs WHERE name = 'Browser-test tariff'"):
            break
        page.wait_for_timeout(100)
    assert not app.sql("SELECT 1 FROM tariffs WHERE name = 'Browser-test tariff'")
    _clean(page)


def test_supplier_number_boxes_take_plain_numbers(make_app, page):
    app = make_app()
    _sign_in(page, app)
    page.click("[data-action=openForm]")
    page.wait_for_selector("#form-overlay", state="visible")
    page.click("[data-action=addDiscount][data-arg=energy]")
    pct, months = ".discount-row .disc-pct", ".discount-row .disc-months"

    def typed(sel, text):
        page.fill(sel, "")
        page.type(sel, text)
        return page.input_value(sel)

    assert typed(pct, "1e5") == "15"                  # "e" ignored (discount %)
    assert typed(months, "-12") == "12"               # "-" ignored (months can't be negative)
    assert typed(months, "+6") == "6"
    page.select_option("#edit-duration-type", "fixed")
    assert typed("#edit-duration-months", "2e4") == "24"
    page.select_option("#edit-fpa-source", "custom")
    assert typed("#edit-fpa-custom", "-0.02") == "-0.02"   # a negative fuel adjustment is valid
    page.select_option("#edit-pricing", "Dynamic")
    assert typed("#var-adder", "-0.01") == "-0.01"         # so is a negative Dynamic adder
    page.fill(pct, "5e1")                             # pasted: cleaned up
    assert page.input_value(pct) == "50"
    page.fill(months, "-3")
    assert page.input_value(months) == ""
    _clean(page)


def _field_msg(page, sel):
    """The error shown for a field: it must be outlined, with its message right next to it."""
    el = page.locator(sel).first
    assert "field-invalid" in (el.get_attribute("class") or ""), f"{sel} not highlighted"
    return el.evaluate("e => e._errMsg ? e._errMsg.textContent : ''")


def test_supplier_form_highlights_each_wrong_field(make_app, page):
    app = make_app()
    _sign_in(page, app)
    page.click("[data-action=setLang][data-arg=en]:visible")
    page.click("[data-action=openForm]")
    page.wait_for_selector("#form-overlay", state="visible")
    page.fill("#edit-name", "")
    page.fill("#edit-mdm", "")
    page.fill("#edit-standing", "1500")
    page.click("[data-action=addDiscount][data-arg=energy]")       # a discount with no percentage
    before = app.sql("SELECT COUNT(*) FROM tariffs")[0][0]
    page.click("#submit-btn")
    assert _field_msg(page, "#edit-name") == "Please provide the tariff name."
    assert _field_msg(page, "#edit-mdm") == "Please enter a value."
    assert _field_msg(page, "#edit-standing") == "This cannot be more than 1000."
    assert "remove this discount" in _field_msg(page, ".discount-row .disc-pct")
    assert "highlighted fields (4)" in page.inner_text("#form-status")
    assert app.sql("SELECT COUNT(*) FROM tariffs")[0][0] == before, "submitted despite errors"
    page.type("#edit-name", "Fixed later")                          # typing clears that field's error
    assert "field-invalid" not in (page.get_attribute("#edit-name", "class") or "")
    assert page.locator("#edit-name ~ .field-err-msg").count() == 0
    # Tiers: an open limit before the last tier, and limits out of order.
    page.select_option("#edit-pricing", "Variable")
    page.locator("[data-action=removeDiscountRow]").click()
    page.click("[data-action=addTierRow]")
    page.click("[data-action=addTierRow]")
    rows = page.locator("#tier-rows .tier-row")
    rows.nth(0).locator(".tier-upto").fill("")
    rows.nth(0).locator(".tier-rate").fill("0.2")
    rows.nth(1).locator(".tier-upto").fill("500")
    rows.nth(1).locator(".tier-rate").fill("0.2")
    rows.nth(2).locator(".tier-upto").fill("")
    rows.nth(2).locator(".tier-rate").fill("")
    page.click("#submit-btn")
    assert "Only the last tier" in _field_msg(page, "#tier-rows .tier-row >> nth=0 >> .tier-upto")
    assert _field_msg(page, "#tier-rows .tier-row >> nth=2 >> .tier-rate") == "Please enter a value."
    rows.nth(0).locator(".tier-upto").fill("1000")
    rows.nth(2).locator(".tier-rate").fill("0.25")
    page.click("#submit-btn")
    assert "higher than the one before" in _field_msg(page, "#tier-rows .tier-row >> nth=1 >> .tier-upto")
    _clean(page)


def test_supplier_form_places_server_errors_on_the_field(make_app, page):
    # The server's limit can be set lower than the page's built-in one; its refusal
    # must still land on the right field.
    app = make_app({"TARIFF_MAX_ENERGY_RATE": "1"})
    _sign_in(page, app)
    page.click("[data-action=setLang][data-arg=en]:visible")
    page.click("[data-action=openForm]")
    page.fill("#edit-name", "Server check")
    page.fill("#fix-rate", "2")
    page.click("#submit-btn")
    page.wait_for_selector("#fix-rate.field-invalid", timeout=10000)
    assert _field_msg(page, "#fix-rate") == "This cannot be more than 1."
    assert "highlighted fields (1)" in page.inner_text("#form-status")
    page.fill("#fix-rate", "0.5")
    page.click("#submit-btn")
    page.wait_for_selector("#form-overlay", state="hidden", timeout=10000)
    _clean(page)


def test_supplier_documents_and_messages(make_app, page, tmp_path):
    app = make_app()
    admin = app.login("admin1@demo.local")
    admin.post("/api/admin/messages", json={"subject": "Browser test", "body": "Please acknowledge.",
                                           "audience": "all", "target_suppliers": []})
    _sign_in(page, app)
    # Documents: open, upload, download, close.
    page.locator("[data-action=openDocsModal]").first.click()
    page.wait_for_selector("#docs-modal-overlay", state="visible")
    pdf = tmp_path / "terms.pdf"
    pdf.write_bytes(b"%PDF-1.4\n% browser test\n%%EOF\n")
    page.set_input_files("#docs-modal-file", str(pdf))
    page.click("[data-action=uploadDocModal]")
    page.wait_for_selector("#docs-modal-list [data-action=downloadDoc]", timeout=10000)
    with page.expect_download() as dl:
        page.locator("#docs-modal-list [data-action=downloadDoc]").first.click()
    assert dl.value.suggested_filename == "terms.pdf"
    page.click("#docs-modal-overlay", position={"x": 5, "y": 5})   # backdrop closes it
    page.wait_for_selector("#docs-modal-overlay", state="hidden")
    # Messages: open, acknowledge, show acknowledged, close.
    page.click("#messages-btn")
    page.wait_for_selector("#messages-overlay", state="visible")
    page.locator("#messages-list [data-action=ackMessage]").first.click()
    for _ in range(50):
        if app.sql("SELECT acknowledged_at FROM message_reads")[0:1] and app.sql("SELECT acknowledged_at FROM message_reads")[0][0]:
            break
        page.wait_for_timeout(100)
    assert app.sql("SELECT acknowledged_at FROM message_reads")[0][0]
    page.locator("#messages-list [data-action=toggleAckedSection]").click()
    assert _visible(page, "#acked-messages")
    page.locator("#messages-overlay [data-action=closeMessagesModal]").click()
    page.wait_for_selector("#messages-overlay", state="hidden")
    _clean(page)


def test_supplier_account_idle_and_expired_password(make_app, page):
    app = make_app()
    _sign_in(page, app)
    page.click("[data-action=openAccountModal]")
    page.wait_for_selector("#acct-overlay", state="visible")
    page.fill("#acct-cur-pw", PASSWORD)
    page.fill("#acct-new-pw", NEW)
    page.fill("#acct-confirm-pw", NEW)
    page.click("[data-action=doUpdatePassword]")
    for _ in range(50):
        if page.inner_text("#acct-pw-msg"):
            break
        page.wait_for_timeout(100)
    app.login(ACME, NEW)
    page.click("#acct-overlay", position={"x": 5, "y": 5})
    page.wait_for_selector("#acct-overlay", state="hidden")
    page.reload(wait_until="networkidle")
    page.wait_for_selector("#app", state="visible", timeout=15000)   # still signed in after own change
    page.evaluate("_showIdleWarning()")                     # the idle warning's button
    page.wait_for_selector("#idle-warning-overlay", state="visible")
    page.click("[data-action=dismissIdleWarning]")
    page.wait_for_selector("#idle-warning-overlay", state="hidden")
    _clean(page)


def test_supplier_expired_password_must_be_changed_first(make_app, page):
    app = make_app()
    app.sql("UPDATE users SET must_change_password = 1 WHERE email = ?", (DELTA,))
    page.goto(f"{app.url}/supplier.html", wait_until="networkidle")
    page.fill("#login-email", DELTA)
    page.fill("#login-password", PASSWORD)
    page.click("#login-btn")
    page.wait_for_selector("#pw-expired-overlay", state="visible", timeout=15000)
    page.fill("#pwx-cur-pw", PASSWORD)
    page.fill("#pwx-new-pw", NEW)
    page.fill("#pwx-confirm-pw", NEW)
    page.click("[data-action=doUpdatePasswordExpired]")
    page.wait_for_selector("#pw-expired-overlay", state="hidden", timeout=15000)
    assert app.sql("SELECT must_change_password FROM users WHERE email = ?", (DELTA,)) == [(0,)]
    _clean(page)


# ── reset-password.html ──────────────────────────────────────────────────────
def _reset_link(app, email=ACME):
    assert app.anon().post("/api/auth/forgot-password", json={"email": email}).status_code == 200
    token = app.sql("SELECT token FROM password_resets WHERE email = ?", (email,))[0][0]
    return f"{app.url}/reset-password.html?token={token}&portal=supplier"


@pytest.fixture
def fresh(make_app):
    return make_app()


def test_reset_password_sets_the_new_password(fresh, page):
    page.goto(_reset_link(fresh), wait_until="networkidle")
    assert page.inner_text(".back-link") == "← Back to Supplier sign in"
    page.fill("#pw1", NEW)
    page.fill("#pw2", NEW)
    page.click("#submit-btn")
    page.wait_for_selector("text=Password updated")
    _clean(page)
    fresh.login(ACME, NEW)


def test_reset_password_enter_key_submits(fresh, page):
    page.goto(_reset_link(fresh), wait_until="networkidle")
    page.fill("#pw1", NEW)
    page.fill("#pw2", NEW)
    page.press("#pw2", "Enter")
    page.wait_for_selector("text=Password updated")
    _clean(page)


def test_reset_password_shows_its_errors(fresh, page):
    page.goto(_reset_link(fresh), wait_until="networkidle")
    page.fill("#pw1", NEW)
    page.fill("#pw2", NEW + "x")
    page.click("#submit-btn")
    assert "do not match" in page.inner_text("#msg")
    page.fill("#pw1", "weak")
    page.fill("#pw2", "weak")
    page.click("#submit-btn")
    assert "at least 8 characters" in page.inner_text("#msg")
    _clean(page)
    fresh.login(ACME, PASSWORD)          # unchanged


def test_reset_password_rejects_a_bad_link(fresh, page):
    page.goto(f"{fresh.url}/reset-password.html?token=made-up", wait_until="networkidle")
    page.fill("#pw1", NEW)
    page.fill("#pw2", NEW)
    page.click("#submit-btn")
    page.wait_for_selector("#expired-msg", state="visible")
    page.goto(f"{fresh.url}/reset-password.html?setup=1", wait_until="networkidle")
    assert page.is_visible("#expired-msg") and "Invitation expired" in page.inner_text("#expired-title")
    # The browser's console reports the refused API call (HTTP 400) as an error; that's expected here.
    page.errors = [e for e in page.errors if "400" not in e]
    _clean(page)
