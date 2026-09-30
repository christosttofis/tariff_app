"""
Centralized environment/secrets configuration.

Every environment variable the app depends on is read here, once, instead
of scattered os.getenv() calls across auth.py/database.py/email_utils.py/
main.py/routers/*.py (TARIFF_BASE_URL alone used to be read independently
in 4 different places, each with its own copy of the same fallback and
.rstrip("/") call). One file to audit = one place to see exactly what
configuration exists and which fallbacks are silently in play.

This does NOT change *how* secrets are supplied. python-dotenv's
load_dotenv() only fills in variables not already set in the process
environment, so a real deployment target that injects secrets as actual
environment variables (Azure App Service Application Settings, an Azure
Key Vault reference resolved to an app setting, a container's env block,
etc.) works identically to a local .env file — this module doesn't care
which one supplied the value, only that os.environ has it by the time this
runs.
"""

import ipaddress
import logging
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# ── JWT signing secret ───────────────────────────────────────────────────────
# No silent fallback: a well-known key baked into source would let anyone who's
# read this file forge admin session tokens. Local dev must opt in explicitly
# via TARIFF_ALLOW_DEV_SECRET=1 rather than getting the insecure key by default.
_DEV_SECRET_KEY_FALLBACK = "dev-only-do-not-deploy-cera-tariff-2026-xK9mP3qR7sN1wL5"
TARIFF_SECRET_KEY = os.getenv("TARIFF_SECRET_KEY")
if not TARIFF_SECRET_KEY:
    if os.getenv("TARIFF_ALLOW_DEV_SECRET") == "1":
        TARIFF_SECRET_KEY = _DEV_SECRET_KEY_FALLBACK
        logger.warning(
            "TARIFF_SECRET_KEY is not set - using the well-known dev-only "
            "signing key because TARIFF_ALLOW_DEV_SECRET=1. Never do this "
            "outside local dev; anyone who reads this source file can forge "
            "session tokens with this key."
        )
    else:
        raise RuntimeError(
            "TARIFF_SECRET_KEY is not set. Refusing to start with a "
            "well-known fallback signing key. Set TARIFF_SECRET_KEY to a "
            "real random value, or set TARIFF_ALLOW_DEV_SECRET=1 to opt "
            "into the insecure dev-only key for local development."
        )

# ── Database ──────────────────────────────────────────────────────────────────
_SQLITE_FALLBACK_PATH = Path(__file__).parent / "tariff.db"
_SQLITE_FALLBACK_URL = f"sqlite:///{_SQLITE_FALLBACK_PATH}"
DATABASE_URL = os.getenv("DATABASE_URL", _SQLITE_FALLBACK_URL)
if DATABASE_URL == _SQLITE_FALLBACK_URL:
    logger.warning(
        "DATABASE_URL is not set - falling back to a local SQLite file (%s). "
        "Expected for local dev/demo use; if this is meant to be a shared or "
        "production environment, it is silently running against the wrong "
        "database.", _SQLITE_FALLBACK_PATH,
    )

# ── Azure AD / Microsoft Graph (outgoing email) ──────────────────────────────
AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID", "")
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID", "")
AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET", "")
TARIFF_EMAIL_FROM = os.getenv("TARIFF_EMAIL_FROM", "")
TARIFF_ADMIN_EMAIL = os.getenv("TARIFF_ADMIN_EMAIL", "")
if not (AZURE_TENANT_ID and AZURE_CLIENT_ID and AZURE_CLIENT_SECRET and TARIFF_EMAIL_FROM):
    logger.warning(
        "Azure email configuration is incomplete - outgoing email (OTP codes, "
        "password resets, notifications) will silently fail to send rather "
        "than raise an error (by design, so a slow/failing Graph call never "
        "blocks the request that triggered it). Expected for local dev/demo "
        "without real Azure credentials."
    )

# ── Public base URL (CORS origin, email links, OTP/reset links) ─────────────
TARIFF_BASE_URL = os.getenv("TARIFF_BASE_URL", "http://localhost:8000").rstrip("/")

# ── API docs (/docs, /redoc, /openapi.json) ──────────────────────────────────
# On by default for local dev convenience. Set TARIFF_ENABLE_DOCS=0 in
# production - these otherwise expose the full route/schema surface
# (including every admin endpoint's shape) to anyone, unauthenticated.
TARIFF_ENABLE_DOCS = os.getenv("TARIFF_ENABLE_DOCS", "1") == "1"

# ── Tariff input sanity limits ───────────────────────────────────────────────
# Upper bounds enforced on every tariff saved (supplier portal, admin
# editor). They exist to reject typos and malformed data before it can
# reach the public calculator, not to police pricing - set them well above any
# real tariff. Adjust via Application Settings / .env; no code change needed.
# See ADMIN_MANUAL.md "Tariff input limits".
TARIFF_MAX_ENERGY_RATE = float(os.getenv("TARIFF_MAX_ENERGY_RATE", "5"))           # €/kWh
TARIFF_MAX_MONTHLY_CHARGE = float(os.getenv("TARIFF_MAX_MONTHLY_CHARGE", "1000"))   # €/month

# ── Admin network restriction ────────────────────────────────────────────────
# Admin accounts (and admin.html) only work from these networks - the CERA
# office and VPN egress addresses. Comma-separated IPs/CIDRs, e.g.
# "203.0.113.10/32,198.51.100.0/28". Empty = restriction OFF (local dev, the
# reviewer demo). See client_ip.py and ADMIN_MANUAL.md "Network restriction".
def _parse_networks(raw: str) -> list[ipaddress.IPv4Network | ipaddress.IPv6Network]:
    networks = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            networks.append(ipaddress.ip_network(part, strict=False))
        except ValueError as e:
            # Fail loudly: a typo must not silently lock admins out, or silently
            # leave the restriction wider than intended.
            raise RuntimeError(f"TARIFF_ADMIN_ALLOWED_NETWORKS: invalid entry {part!r} ({e})") from None
    return networks


TARIFF_ADMIN_ALLOWED_NETWORKS = _parse_networks(os.getenv("TARIFF_ADMIN_ALLOWED_NETWORKS", ""))
if not TARIFF_ADMIN_ALLOWED_NETWORKS:
    logger.warning(
        "TARIFF_ADMIN_ALLOWED_NETWORKS is not set - admin accounts can be used "
        "from any network. Expected for local dev/demo; in production set it to "
        "the CERA office and VPN egress addresses."
    )

# How many reverse proxies in front of the app append to X-Forwarded-For.
# 0 = use the TCP peer address (local dev, direct connections).
# 1 = Azure App Service (its front end appends the real client IP).
# Never trust X-Forwarded-For entries beyond this count: a client can put
# anything it likes at the start of that header.
TARIFF_TRUSTED_PROXY_HOPS = int(os.getenv("TARIFF_TRUSTED_PROXY_HOPS", "0"))
if TARIFF_TRUSTED_PROXY_HOPS < 0:
    raise RuntimeError("TARIFF_TRUSTED_PROXY_HOPS must be 0 or more")
