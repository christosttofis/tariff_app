"""Browser-driven smoke test of the public customer.html calculator.

Dev-only tool (see requirements-dev.txt) — not run automatically, not part
of the app. Exercises the flow end-to-end against a live server: annual
mode, card expand, discount toggle, sample invoice, monthly mode. Also
guards against server-returned i18n translation *keys* leaking into the
page unrendered (see the "REGULATED_GRID" label bug fixed 2026-09-03).

Usage:
  1. Start the app: .venv/Scripts/python.exe -m uvicorn main:app --port 8000
     (from inside tariff-api/; do NOT use --reload)
  2. .venv/Scripts/python.exe -m pip install -r requirements-dev.txt
     .venv/Scripts/python.exe -m playwright install chromium   (first time only)
  3. .venv/Scripts/python.exe scripts/verify_customer_calc.py [base_url]
     (base_url defaults to http://127.0.0.1:8000)

Exits non-zero and prints details on any browser console error or failed
assertion. Saves a full-page screenshot next to this script.
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"
SCREENSHOT_PATH = Path(__file__).parent / "customer_calc_verify.png"
console_errors = []


def log(msg):
    print(f"[verify] {msg}", flush=True)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda exc: console_errors.append(str(exc)))

        log(f"loading {BASE}/customer.html")
        page.goto(f"{BASE}/customer.html", wait_until="networkidle")
        page.wait_for_selector("#app", state="visible", timeout=10000)

        log("entering annual kWh = 5000 (domestic, default)")
        page.fill("#annual-kwh", "5000")
        page.wait_for_timeout(600)  # debounce window

        page.wait_for_selector(".rank-card", timeout=10000)
        cards = page.query_selector_all(".rank-card")
        log(f"rank cards rendered: {len(cards)}")
        assert len(cards) > 0, "no rank cards rendered"

        first_cost = page.query_selector(".rank-annual-val").inner_text()
        log(f"first tariff's displayed cost: {first_cost!r}")

        # Server returns translation *keys* for some fields (e.g. regulated-
        # charge row labels) that the client must run through T() — catch
        # regressions where a raw key leaks into the rendered page.
        body_text = page.inner_text("body")
        for bad_key in ["REGULATED_GRID", "REGULATED_PSO", "REGULATED_RES", "MDM_SUPPLIER", "REGULATED_MDM"]:
            assert bad_key not in body_text, f"raw translation key {bad_key} leaked into rendered page"
        log("no raw translation keys found in page text")

        log("expanding first card")
        page.click(".rank-header")
        page.wait_for_timeout(400)
        mo_table = page.query_selector(".rank-detail.open .mo-table")
        assert mo_table is not None, "monthly breakdown table did not render on expand"
        log("monthly breakdown table rendered")

        canvas = page.query_selector(".rank-detail.open canvas")
        log(f"chart canvas present: {canvas is not None}")

        disc_checkbox = page.query_selector(".rank-detail.open input[type=checkbox][data-tariff]")
        if disc_checkbox:
            before = page.query_selector(".rank-detail.open .mo-table tbody tr:last-child td:last-child").inner_text()
            log(f"discount checkbox found, total before toggle: {before!r}")
            disc_checkbox.click()
            page.wait_for_timeout(500)
            after_table = page.query_selector(".rank-detail.open .mo-table")
            assert after_table is not None, "table disappeared after discount toggle"
            log("discount toggle re-rendered without error")
        else:
            log("no discount toggle on first expanded card (skipping)")

        buttons = page.query_selector_all(".rank-detail.open button")
        sample_btn = next((b for b in buttons if "\U0001F4C4" in (b.inner_text() or "")), None)
        if sample_btn:
            log("sample invoice button found, clicking")
            sample_btn.click()
            page.wait_for_timeout(600)
            overlay = page.query_selector("#sample-invoice-overlay")
            visible = overlay.is_visible() if overlay else False
            log(f"sample invoice overlay visible: {visible}")
            if visible:
                body = page.inner_text("#sample-invoice-body")
                assert "€" in body, "sample invoice body has no currency figures"
                log(f"sample invoice body length: {len(body)} chars, contains currency values")
                page.evaluate("closeSampleInvoice()")
                page.wait_for_timeout(200)
                log("sample invoice closed")
        else:
            log("sample invoice not enabled/no button on this tariff (skipping)")

        log("switching to monthly mode")
        page.click("#btn-monthly")
        page.fill("#monthly-kwh", "400")
        page.wait_for_timeout(600)
        cards_monthly = page.query_selector_all(".rank-card")
        log(f"rank cards in monthly mode: {len(cards_monthly)}")
        assert len(cards_monthly) > 0, "no rank cards in monthly mode"

        page.screenshot(path=str(SCREENSHOT_PATH), full_page=True)
        log(f"screenshot saved to {SCREENSHOT_PATH}")

        browser.close()

    if console_errors:
        log(f"CONSOLE ERRORS ({len(console_errors)}):")
        for e in console_errors:
            log(f"  - {e}")
        sys.exit(1)
    else:
        log("NO console errors. ALL CHECKS PASSED.")


if __name__ == "__main__":
    main()
