"""9. Files that must never be served, and the browser-protection headers.

Only the four pages and the logo are public. Source code, settings (.env),
the database, uploaded documents and git history must never be downloadable,
however the path is written.
"""
import pytest

PUBLIC = {"/customer.html": "text/html", "/supplier.html": "text/html", "/admin.html": "text/html",
          "/reset-password.html": "text/html", "/Logo_Transparent.png": "image/png"}

BLOCKED = [
    "/tariff-api/.env", "/.env", "/tariff-api/config.py", "/tariff-api/main.py", "/main.py",
    "/tariff-api/tariff.db", "/tariff-api/alembic.ini", "/tariff-api/requirements.txt",
    "/.git/config", "/.git/HEAD", "/start.bat", "/README.md", "/SECURITY_REMEDIATION_CHECKLIST.md",
    "/tariff-api/.venv/pyvenv.cfg", "/tariff-api/", "/tariff-api/uploads/",
    "/ADMIN.HTML", "/Customer.html", "/./admin.html/..", "/",
    "/%2e%2e/%2e%2e/Windows/win.ini", "/..%2f..%2fetc%2fpasswd", "/tariff-api/%2e%65nv",
    "/static/../tariff-api/.env", "/customer.html%00.env",
]


@pytest.mark.parametrize("path", PUBLIC)
def test_public_pages_are_served(app, path):
    r = app.anon().get(path)
    assert r.status_code == 200 and r.headers["content-type"].startswith(PUBLIC[path])


@pytest.mark.parametrize("path", BLOCKED)
def test_private_files_are_never_served(app, path):
    r = app.anon().get(path)
    assert r.status_code in (400, 404, 405), f"{path} -> {r.status_code}"


def test_uploaded_documents_are_not_public(app, acme):
    t = acme.get("/api/supplier/tariffs").json()[-1]
    acme.post(f"/api/supplier/tariffs/{t['id']}/documents", files={"file": ("a.pdf", b"%PDF-1.4\n", "application/pdf")})
    stored = next(app.upload_dir.iterdir()).name
    for path in (f"/uploads/{stored}", f"/tariff-api/uploads/{stored}", f"/{stored}"):
        assert app.anon().get(path).status_code == 404


@pytest.mark.parametrize("path", ["/customer.html", "/admin.html", "/api/public/config"])
def test_browser_protection_headers_are_sent(app, path):
    h = app.anon().get(path).headers
    csp = h.get("Content-Security-Policy", "")
    for rule in ("default-src 'self'", "object-src 'none'", "frame-ancestors 'self'", "base-uri 'self'",
                 "form-action 'self'"):
        assert rule in csp, f"CSP missing {rule!r}"
    assert h.get("X-Content-Type-Options") == "nosniff"
    assert h.get("Referrer-Policy") == "strict-origin-when-cross-origin"


def test_session_cookie_is_protected(app):
    r = app.anon().post("/api/auth/login", json={"email": "acme.energy@demo.local", "password": "Demo123!"})
    cookie = r.headers["set-cookie"].lower()
    for flag in ("httponly", "secure", "samesite=strict"):
        assert flag in cookie, f"session cookie missing {flag}"
