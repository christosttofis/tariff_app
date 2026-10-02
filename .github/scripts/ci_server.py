"""Throwaway app instance for the ZAP workflow (CI only, never used by the real app).

Runs the normal application code against a fake demo database, with two
in-memory test overrides so the scan measures the app rather than its limits:
  - per-IP rate limit raised (ZAP sends thousands of requests from one IP)
  - session tokens last 4h, so the recorded sign-ins stay valid for the scan

All configuration (DATABASE_URL, a random TARIFF_SECRET_KEY, empty email
settings) comes from the workflow's environment. No real credentials exist here.
"""
import os
import sys
from pathlib import Path

API_DIR = Path(__file__).resolve().parents[2] / "tariff-api"
sys.path.insert(0, str(API_DIR))
os.chdir(API_DIR)

import auth  # noqa: E402

auth.TOKEN_EXPIRE_HOURS = 4

import main  # noqa: E402

main._RATE_LIMIT_MAX_REQUESTS = 10 ** 9

import uvicorn  # noqa: E402

uvicorn.run(main.app, host="127.0.0.1", port=8002, log_level="warning")
