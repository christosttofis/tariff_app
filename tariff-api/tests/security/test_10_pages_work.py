"""10. The converted pages still work, under the strict Content-Security-Policy.

Plan B moves each page's code out of the page and stops the browser from running
any code written inside a page. These tests click through each converted page in
headless Chromium and check that every button and form still does its job, and
that the browser blocked nothing (no CSP violations, no script errors).
"""
import pytest
from playwright.sync_api import sync_playwright

from conftest import ACME, PASSWORD

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
    assert not page.errors, f"browser errors: {page.errors}"


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
