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
