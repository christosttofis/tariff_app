"""7. Planting harmful text (stored XSS), checked in a real browser.

Text that looks like code is saved everywhere a supplier, an admin or a member
of the public can type, then every page that shows it is opened in headless
Chromium. The text must appear as plain text; it must never become page
markup and its code must never run. (The CSP still allows inline code for now,
so the escaping is what's being tested here.)
"""
import pytest
from playwright.sync_api import sync_playwright

from conftest import ACME, ADMIN, COOKIE

# Each payload sets window.__xss if it ever runs, in three different ways.
MARK = "XSSPROBE"
PAYLOAD = (f'{MARK}<img src=x onerror="window.__xss=1"><svg onload="window.__xss=1">'
           f'"\'><script>window.__xss=1</script>')
INJECTED = 'img[src="x"], [onerror*="__xss"], [onload*="__xss"]'
EVIL_ID = "x');window.__xss=1;('"


@pytest.fixture(scope="module")
def planted(app, admin, acme):
    """Put the payload into every free-text field that some page displays."""
    own = acme.get("/api/supplier/tariffs").json()[0]
    body = {k: v for k, v in own.items() if k not in ("id", "status", "createdAt", "updatedAt", "rejection_reason",
                                                       "hasDocs", "everPublished")}
    # Discount conditions are free text shown in the public tariff card's offers box.
    discount = {"type": "energy", "percentage": 5, "durationMonths": None, "conditions": PAYLOAD}
    r = acme.post("/api/supplier/tariffs", json={**body, "name": PAYLOAD[:200], "discounts": [discount]})
    assert r.status_code == 201, r.text
    tid = r.json()["id"]
    r = acme.post(f"/api/supplier/tariffs/{tid}/documents",
                  files={"file": (f"{PAYLOAD[:150]}.pdf", b"%PDF-1.4\n%%EOF\n", "application/pdf")})
    assert r.status_code == 201, r.text
    assert admin.patch(f"/api/admin/tariffs/{tid}/status", json={"status": "approved"}).status_code == 200

    supplier = next(s for s in admin.get("/api/admin/suppliers").json() if s["name"] == "Acme Energy")
    r = admin.put("/api/admin/suppliers/Acme Energy", json={**supplier, "address": PAYLOAD, "licence": PAYLOAD[:100]})
    assert r.status_code == 200, r.text

    r = admin.post("/api/admin/messages", json={"subject": PAYLOAD[:200], "body": PAYLOAD,
                                                "audience": "all", "target_suppliers": []})
    assert r.status_code == 201, r.text

    prof = admin.get("/api/admin/profiles").json()[0]
    r = admin.post("/api/admin/profiles", json={**{k: v for k, v in prof.items() if k != "id"},
                                                "name": PAYLOAD[:200], "desc": PAYLOAD})
    assert r.status_code == 201, r.text
    assert admin.post("/api/admin/profiles", json={**prof, "id": EVIL_ID}).status_code == 422
    r = app.anon().post("/api/public/report-tariff", json={"tariff_id": EVIL_ID, "category": "other", "note": "x",
                                                          "reporter_email": "visitor@example.com"})
    assert r.status_code == 422

    # A supplier may choose its tariff's ID. One that breaks out of a JavaScript string in a
    # click handler would run code for every visitor who opens the card.
    # Layer 1: the API refuses such IDs. Layer 2: the pages stay safe even with one already
    # stored (e.g. from before the rule), so plant it directly in the throwaway database.
    assert acme.post("/api/supplier/tariffs", json={**body, "id": EVIL_ID}).status_code == 422
    assert admin.post("/api/admin/tariffs", json={**body, "id": EVIL_ID}).status_code == 422
    r = acme.post("/api/supplier/tariffs", json={**body, "name": f"{MARK} id test"})
    assert r.status_code == 201
    assert admin.patch(f"/api/admin/tariffs/{r.json()['id']}/status", json={"status": "approved"}).status_code == 200
    app.sql("UPDATE tariffs SET id = ? WHERE id = ?", (EVIL_ID, r.json()["id"]))

    # Public visitor: a tariff report; anyone: a sign-in attempt (shown in Login activity).
    r = app.anon().post("/api/public/report-tariff", json={"tariff_id": tid, "category": "other",
                                                          "note": PAYLOAD, "reporter_email": "visitor@example.com"})
    assert r.status_code in (200, 201), r.text
    app.anon().post("/api/auth/login", json={"email": PAYLOAD, "password": "x"})
    return tid


@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        b = p.chromium.launch()
        yield b
        b.close()


def _open(browser, app, page_name, session=None):
    ctx = browser.new_context()
    if session is not None:
        ctx.add_cookies([{"name": COOKIE, "value": session.token, "url": app.url, "httpOnly": True}])
    page = ctx.new_page()
    page.dialogs = []
    page.on("dialog", lambda d: (page.dialogs.append(d.message), d.dismiss()))
    page.goto(f"{app.url}/{page_name}", wait_until="networkidle")
    return page


def _assert_safe(page, where):
    page.wait_for_timeout(500)
    ran = page.evaluate("window.__xss")
    injected = page.locator(INJECTED).count()
    assert not ran and not injected and not page.dialogs, \
        f"{where}: code ran={ran!r}, injected elements={injected}, dialogs={page.dialogs}"


def test_public_calculator_shows_planted_text_safely(app, planted, browser):
    page = _open(browser, app, "customer.html")
    page.fill("#annual-kwh", "5000")
    page.wait_for_selector(".rank-card", timeout=15000)
    assert MARK in page.inner_text("body"), "planted tariff not displayed - test would prove nothing"
    _assert_safe(page, "customer results")
    for header in page.locator(".rank-header").all():       # open every tariff card
        header.click()
        _assert_safe(page, "customer tariff details")
    assert page.locator(".rank-detail.open :text('XSSPROBE')").count(), \
        "planted discount conditions not displayed - test would prove nothing"


def test_supplier_portal_shows_planted_text_safely(app, planted, browser):
    acme = app.login(ACME)
    page = _open(browser, app, "supplier.html", acme)
    # (polled: Playwright's wait_for_function evaluates text as code, which the strict CSP refuses)
    for _ in range(150):
        if MARK in page.inner_text("body"):
            break
        page.wait_for_timeout(100)
    assert MARK in page.inner_text("body"), "planted tariff not displayed - test would prove nothing"
    _assert_safe(page, "supplier tariff list")
    for step, js in (("messages", "openMessagesModal()"),
                     ("documents", f"openDocsModal('{planted}')"),
                     ("tariff form", f"openForm('{planted}')")):
        page.evaluate(js)
        _assert_safe(page, f"supplier {step}")


def test_admin_panel_shows_planted_text_safely(app, planted, browser):
    admin = app.login(ADMIN)
    page = _open(browser, app, "admin.html", admin)
    page.wait_for_selector(".nav-item", state="visible", timeout=15000)
    seen = False
    for item in page.locator(".nav-item").all():
        label = item.inner_text().strip()
        item.click()
        _assert_safe(page, f"admin '{label}'")
        seen = seen or MARK in page.inner_text("body")
    assert seen, "planted text never displayed in the admin panel - test would prove nothing"
    page.evaluate(f"typeof openDocsModal === 'function' && openDocsModal('{planted}')")
    _assert_safe(page, "admin documents")
