"""
Trusted client IP and the admin network check.

Every place that needs "who is calling" (admin network restriction, per-IP
rate limiting, login-activity / report logging) goes through client_ip(), so
there is exactly one rule for which address to believe.

Behind a reverse proxy (Azure App Service's front end) the TCP peer is the
proxy, and the real client is in X-Forwarded-For. That header is a list the
client can pre-fill ("X-Forwarded-For: <any address I like>"); each proxy
appends the address it saw. So only the last TARIFF_TRUSTED_PROXY_HOPS
entries, counted from the right, were written by our own infrastructure, and
the client IP is the rightmost of those. Anything further left is ignored.
"""

import ipaddress

from fastapi import Request

from config import TARIFF_ADMIN_ALLOWED_NETWORKS, TARIFF_TRUSTED_PROXY_HOPS

IPAddress = ipaddress.IPv4Address | ipaddress.IPv6Address


def _parse_ip(value: str) -> IPAddress | None:
    """Parse "1.2.3.4", "1.2.3.4:5678", "::1", "[::1]" or "[::1]:443" (Azure includes a port)."""
    value = value.strip()
    if value.startswith("["):                       # [IPv6] or [IPv6]:port
        value = value[1:value.find("]")] if "]" in value else ""
    elif value.count(":") == 1:                     # IPv4:port
        value = value.split(":")[0]
    try:
        ip = ipaddress.ip_address(value)
    except ValueError:
        return None
    # An IPv4 client reaching an IPv6 socket shows up as ::ffff:a.b.c.d
    if isinstance(ip, ipaddress.IPv6Address) and ip.ipv4_mapped:
        return ip.ipv4_mapped
    return ip


def client_ip(request: Request) -> IPAddress | None:
    """The caller's IP, or None if it can't be determined (treated as not allowed)."""
    if TARIFF_TRUSTED_PROXY_HOPS == 0:
        return _parse_ip(request.client.host) if request.client else None
    entries = [e for e in ",".join(request.headers.getlist("x-forwarded-for")).split(",") if e.strip()]
    if len(entries) < TARIFF_TRUSTED_PROXY_HOPS:
        return None                                 # didn't come through the expected proxy
    return _parse_ip(entries[-TARIFF_TRUSTED_PROXY_HOPS])


def client_ip_str(request: Request) -> str | None:
    ip = client_ip(request)
    return str(ip) if ip else None


def admin_network_allowed(request: Request) -> bool:
    """True if admin access is allowed for this request: restriction off, or the
    caller's IP is inside one of TARIFF_ADMIN_ALLOWED_NETWORKS."""
    if not TARIFF_ADMIN_ALLOWED_NETWORKS:
        return True
    ip = client_ip(request)
    return ip is not None and any(ip.version == n.version and ip in n for n in TARIFF_ADMIN_ALLOWED_NETWORKS)


# Body of every "outside the network" response. Deliberately generic: no CERA
# branding, no mention of admins, VPN or networks.
UNAVAILABLE_DETAIL = "Website unavailable"
UNAVAILABLE_HTML = (
    "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
    "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
    "<title>Website unavailable</title></head>"
    "<body style=\"font-family:system-ui,sans-serif;color:#444;display:flex;align-items:center;"
    "justify-content:center;min-height:90vh;margin:0\"><p>Website unavailable</p></body></html>"
)
