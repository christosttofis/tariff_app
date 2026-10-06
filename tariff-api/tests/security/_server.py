"""Throwaway app instance for the attacker tests (never used by the real app).

Started by conftest.py as a subprocess, against a copy of a fake demo database.
Everything it needs comes from the environment conftest.py sets up:
DATABASE_URL (a temp SQLite file), a random TARIFF_SECRET_KEY, empty email/Azure
settings, and the network-restriction settings a test asks for.

In-memory test overrides, so the tests measure the app rather than their own setup:
  - tariff-api/.env is never read (load_dotenv is disabled before config imports it),
    so local credentials and the real database can't leak into a test run;
  - uploaded PDFs go to a temp folder (TEST_UPLOAD_DIR), not tariff-api/uploads;
  - the per-IP rate limit is raised (TEST_RATE_LIMIT), since every test request
    comes from 127.0.0.1. The rate-limit test starts a server with the real value.

Usage: python _server.py <port>
"""
import os
import sys
from pathlib import Path

API_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(API_DIR))
os.chdir(API_DIR)

import dotenv  # noqa: E402

dotenv.load_dotenv = lambda *a, **k: False

import main  # noqa: E402
from routers import shared  # noqa: E402

shared._UPLOAD_DIR = Path(os.environ["TEST_UPLOAD_DIR"])
main._RATE_LIMIT_MAX_REQUESTS = int(os.environ.get("TEST_RATE_LIMIT", str(10 ** 9)))

import uvicorn  # noqa: E402

uvicorn.run(main.app, host="127.0.0.1", port=int(sys.argv[1]), log_level="warning")
