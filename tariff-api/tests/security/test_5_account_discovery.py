"""5. Finding out who has an account (account enumeration).

The sign-in and "forgot password" forms must answer a registered email and a
made-up one the same way, in content and in time.
"""
import statistics
import time

from conftest import ACME, DELTA, VOLT

UNKNOWN = ["nobody1@demo.local", "nobody2@demo.local", "nobody3@demo.local"]
KNOWN = [ACME, DELTA, VOLT]          # one wrong guess each, so nobody gets locked


def test_sign_in_gives_the_same_answer_for_real_and_made_up_emails(app):
    real = app.anon().post("/api/auth/login", json={"email": "admin2@demo.local", "password": "Wrong-guess1!"})
    fake = app.anon().post("/api/auth/login", json={"email": "ghost@demo.local", "password": "Wrong-guess1!"})
    assert (real.status_code, real.json()) == (fake.status_code, fake.json())


def test_forgot_password_gives_the_same_answer_for_real_and_made_up_emails(app):
    real = app.anon().post("/api/auth/forgot-password", json={"email": ACME})
    fake = app.anon().post("/api/auth/forgot-password", json={"email": "ghost@demo.local"})
    assert (real.status_code, real.json()) == (fake.status_code, fake.json())


def _timed_login(app, email):
    t = time.perf_counter()
    app.anon().post("/api/auth/login", json={"email": email, "password": "Wrong-guess2!"})
    return time.perf_counter() - t


def test_sign_in_takes_the_same_time_for_real_and_made_up_emails(app):
    _timed_login(app, "warmup@demo.local")
    known = statistics.median(_timed_login(app, e) for e in KNOWN)
    unknown = statistics.median(_timed_login(app, e) for e in UNKNOWN)
    # A password check costs ~0.1-0.3 s by design; skipping it for unknown emails
    # would let anyone test which emails are registered by timing the reply.
    assert abs(known - unknown) < 0.08, f"registered {known:.3f}s vs made-up {unknown:.3f}s"
