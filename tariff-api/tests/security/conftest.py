"""Shared setup for the attacker (abuse-case) tests.

Every test talks to a throwaway copy of the app over real HTTP, started by
_server.py on 127.0.0.1 with:
  - a copy of a fake demo database (seed_demo_data.py; demo users, password Demo123!);
  - a random signing key, generated per run;
  - email/Azure settings empty, so nothing is ever sent; emails are written to a
    file instead, and read back with `app.otp_code()` / `app.reset_token()`;
  - tariff-api/.env never read, and the real database never touched.

Each test module gets its own fresh server and database (`app` fixture), so
tests in different files can't affect each other. Tests that need special
settings (admin network restriction, the real rate limit) or that lock
accounts start their own short-lived server with `make_app`.
"""
import json
import os
import re
import secrets
import shutil
import socket
import sqlite3
import subprocess
import sys
import time
from pathlib import Path

import pytest
import requests

API_DIR = Path(__file__).resolve().parents[2]
SERVER = Path(__file__).with_name("_server.py")
PASSWORD = "Demo123!"
ADMIN = "admin1@demo.local"
ACME = "acme.energy@demo.local"
DELTA = "delta.power@demo.local"
VOLT = "volt.co@demo.local"
COOKIE = "cera_access_token"

# Never inherit these from the developer's environment; .env is not read at all.
_BASE_ENV = {
    "TARIFF_ENABLE_DOCS": "1",                 # the role tests read the route list from /openapi.json
    "TARIFF_ADMIN_ALLOWED_NETWORKS": "",
    "TARIFF_TRUSTED_PROXY_HOPS": "0",
    "AZURE_TENANT_ID": "", "AZURE_CLIENT_ID": "", "AZURE_CLIENT_SECRET": "",
    "TARIFF_EMAIL_FROM": "", "TARIFF_ADMIN_EMAIL": "",
    "TARIFF_BASE_URL": "http://127.0.0.1",
    "PYTHONIOENCODING": "utf-8",
}
_NO_DOTENV = "import dotenv; dotenv.load_dotenv = lambda *a, **k: False; "


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class Client:
    """One browser-like session. The cookie is sent as a raw header because it is
    marked Secure and the test server runs on plain http."""

    def __init__(self, app: "App", token: str | None = None):
        self.app, self.token = app, token

    def req(self, method: str, path: str, **kw) -> requests.Response:
        headers = dict(kw.pop("headers", {}) or {})
        if self.token is not None:
            headers["Cookie"] = f"{COOKIE}={self.token}"
        r = requests.request(method, self.app.url + path, headers=headers, allow_redirects=False, timeout=30, **kw)
        if r.cookies.get(COOKIE):            # sliding renewal: keep the newest token
            self.token = r.cookies[COOKIE]
        return r

    def get(self, path, **kw): return self.req("GET", path, **kw)
    def post(self, path, **kw): return self.req("POST", path, **kw)
    def put(self, path, **kw): return self.req("PUT", path, **kw)
    def patch(self, path, **kw): return self.req("PATCH", path, **kw)
    def delete(self, path, **kw): return self.req("DELETE", path, **kw)


class App:
    """A running throwaway server with its own copy of the demo database."""

    def __init__(self, workdir: Path, template_db: Path, env: dict | None = None, rate_limit: int | None = None):
        workdir.mkdir(parents=True, exist_ok=True)
        self.db_path = workdir / "app.db"
        shutil.copy(template_db, self.db_path)
        self.upload_dir = workdir / "uploads"
        self.upload_dir.mkdir()
        self.mail_file = workdir / "mail.jsonl"
        self.secret = secrets.token_hex(32)
        self.port = _free_port()
        self.url = f"http://127.0.0.1:{self.port}"
        full_env = {**os.environ, **_BASE_ENV, **(env or {}),
                    "DATABASE_URL": "sqlite:///" + self.db_path.as_posix(),
                    "TARIFF_SECRET_KEY": self.secret,
                    "TEST_UPLOAD_DIR": str(self.upload_dir),
                    "TEST_MAIL_FILE": str(self.mail_file)}
        if rate_limit is not None:
            full_env["TEST_RATE_LIMIT"] = str(rate_limit)
        full_env = {k: v for k, v in full_env.items() if v is not None}   # None = setting left out
        self.log_path = workdir / "server.log"
        self._log = open(self.log_path, "w", encoding="utf-8")
        self.proc = subprocess.Popen([sys.executable, str(SERVER), str(self.port)], cwd=API_DIR,
                                     env=full_env, stdout=self._log, stderr=subprocess.STDOUT)
        for _ in range(120):
            if self.proc.poll() is not None:
                break
            try:
                requests.get(self.url + "/customer.html", timeout=1)
                return
            except requests.RequestException:
                time.sleep(0.25)
        self.stop()
        raise RuntimeError("test server did not start:\n" + self.log_path.read_text(encoding="utf-8")[-3000:])

    def stop(self):
        if self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(10)
            except subprocess.TimeoutExpired:
                self.proc.kill()
        self._log.close()

    # ── helpers ──
    def anon(self) -> Client:
        return Client(self)

    def login(self, email: str, password: str = PASSWORD, headers: dict | None = None) -> Client:
        c = Client(self)
        r = c.post("/api/auth/login", json={"email": email, "password": password}, headers=headers)
        assert r.status_code == 200, f"login {email}: {r.status_code} {r.text[:200]}"
        assert c.token, f"login {email}: no session cookie"
        return c

    def mails(self, to: str) -> list[dict]:
        """Emails the server "sent" to this address, oldest first (_server.py writes
        them to a file instead of sending them)."""
        if not self.mail_file.exists():
            return []
        lines = self.mail_file.read_text(encoding="utf-8").splitlines()
        return [m for m in map(json.loads, lines) if to in m["to"]]

    def otp_code(self, email: str) -> str:
        """The 6-digit code from the newest sign-in-code email (the database holds only a hash)."""
        html = [m for m in self.mails(email) if "verification code" in m["subject"]][-1]["html"]
        return re.search(r">(\d{6})</span>", html).group(1)

    def reset_token(self, email: str) -> str:
        """The token from the newest reset or invite link emailed (the database holds only a hash)."""
        html = [m for m in self.mails(email) if "reset-password.html?token=" in m["html"]][-1]["html"]
        return re.search(r"reset-password\.html\?token=([A-Za-z0-9_-]+)", html).group(1)

    def sql(self, query: str, params: tuple = ()) -> list:
        """Read or adjust the throwaway database directly. Never used against a real database."""
        con = sqlite3.connect(self.db_path)
        try:
            rows = con.execute(query, params).fetchall()
            con.commit()
            return rows
        finally:
            con.close()

    def user_id(self, email: str) -> int:
        return self.sql("SELECT id FROM users WHERE email = ?", (email,))[0][0]


@pytest.fixture(scope="session")
def template_db(tmp_path_factory) -> Path:
    """The demo database, built once per test run and copied for each server."""
    path = tmp_path_factory.mktemp("template") / "demo.db"
    env = {**os.environ, **_BASE_ENV, "TARIFF_SECRET_KEY": secrets.token_hex(32),
           "DATABASE_URL": "sqlite:///" + path.as_posix()}
    code = _NO_DOTENV + "import runpy, sys; sys.argv = ['seed_demo_data.py', sys.argv[1]]; " \
                        "runpy.run_path('seed_demo_data.py', run_name='__main__')"
    r = subprocess.run([sys.executable, "-c", code, str(path)], cwd=API_DIR, env=env, capture_output=True, text=True)
    assert r.returncode == 0 and path.exists(), f"seeding failed:\n{r.stdout}\n{r.stderr}"
    return path


@pytest.fixture(scope="module")
def app(template_db, tmp_path_factory):
    a = App(tmp_path_factory.mktemp("app"), template_db)
    yield a
    a.stop()


@pytest.fixture
def make_app(template_db, tmp_path):
    """Start an extra server with special settings; stopped after the test."""
    started = []

    def _make(env: dict | None = None, rate_limit: int | None = None) -> App:
        a = App(tmp_path / f"app{len(started)}", template_db, env, rate_limit)
        started.append(a)
        return a

    yield _make
    for a in started:
        a.stop()


@pytest.fixture(scope="module")
def admin(app): return app.login(ADMIN)


@pytest.fixture(scope="module")
def acme(app): return app.login(ACME)


@pytest.fixture(scope="module")
def delta(app): return app.login(DELTA)
