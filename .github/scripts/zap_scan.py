"""ZAP scan driven by realistic traffic (CI only; runs on GitHub's throwaway machine).

1. Use the throwaway app THROUGH ZAP's proxy the way real people would: a visitor
   (calculator, report form, sign-in/reset forms), a supplier (tariffs, documents,
   messages) and an admin (every admin page, approve, create/edit/delete), with
   real IDs and real sessions. ZAP records every request.
2. Import the OpenAPI description and spider the public page for anything missed.
3. Passive scan, then active scan of everything recorded (sign-out / change
   password / change email excluded so it doesn't end its own sessions).
4. Check the recorded sessions still worked at the end, then write the reports.

Coverage guard: if too few signed-in supplier/admin requests succeeded, the run
fails, so a "pass" can't come from a scan that never got past the login page.

Usage: zap_scan.py <app_url> <zap_url> <api_key> <out_dir>
"""
import json
import os
import sys
import time
from collections import Counter

import requests

APP, ZAP, KEY, OUT = sys.argv[1].rstrip("/"), sys.argv[2].rstrip("/"), sys.argv[3], sys.argv[4]
DRY_RUN = os.getenv("ZAP_DRY_RUN") == "1"   # exercise the app only: no ZAP, no proxy, no attack
PROXIES = {} if DRY_RUN else {"http": ZAP, "https": ZAP}
MAX_SCAN_MIN = int(os.getenv("ZAP_MAX_SCAN_MIN", "35"))
PW = "Demo123!"

zapi = requests.Session()
zapi.trust_env = False
web = requests.Session()
web.trust_env = False
web.proxies.update(PROXIES)

ok = Counter()      # role -> 2xx count
calls = Counter()   # role -> total


def z(path, **params):
    # Under heavy active-scan load ZAP's API can drop a single connection while
    # ZAP itself carries on; retry for ~2.5 min before treating it as a crash.
    for attempt in range(10):
        try:
            r = zapi.get(ZAP + path, params={"apikey": KEY, **params}, timeout=300)
            r.raise_for_status()
            return r.json() if "/JSON/" in path else r.text
        except (requests.ConnectionError, requests.Timeout) as e:
            if attempt == 9:
                raise
            print(f"  (ZAP API not responding: {type(e).__name__}; retrying in 15s)", flush=True)
            time.sleep(15)


def call(role, method, path, cookie=None, **kw):
    headers = kw.pop("headers", {})
    if cookie:
        headers["Cookie"] = f"cera_access_token={cookie}"
    try:
        r = web.request(method, APP + path, headers=headers, timeout=60, **kw)
    except requests.RequestException as e:
        print(f"  {role:8} {method:6} {path} -> ERROR {e}")
        calls[role] += 1
        return None
    calls[role] += 1
    if 200 <= r.status_code < 300:
        ok[role] += 1
    print(f"  {role:8} {method:6} {path} -> {r.status_code}")
    return r


def js(r, default=None):
    try:
        return r.json()
    except Exception:
        return default


def login(email):
    r = web.post(APP + "/api/auth/login", json={"email": email, "password": PW}, timeout=30)
    r.raise_for_status()
    return r.cookies["cera_access_token"]


def first(items, key="id"):
    return items[0][key] if isinstance(items, list) and items and key in items[0] else None


# ── wait for ZAP ──
if not DRY_RUN:
    for _ in range(180):
        try:
            print("ZAP version", z("/JSON/core/view/version/")["version"]); break
        except Exception:
            time.sleep(2)
    else:
        sys.exit("ZAP did not start")
    z("/JSON/core/action/newSession/", overwrite="true")

# ── 1. visitor ──
print("== visitor")
for p in ("/customer.html", "/supplier.html", "/admin.html", "/reset-password.html", "/Logo_Transparent.png"):
    call("visitor", "GET", p)
pub = js(call("visitor", "GET", "/api/public/config"), {})
tid_pub = first(pub.get("tariffs", []))
call("visitor", "POST", "/api/public/calculate", json={"customerType": "domestic", "inputMode": "annual", "annualKwh": 4000})
call("visitor", "POST", "/api/public/calculate", json={"customerType": "ci", "voltage": "LV", "loadEntitlement": "lt70",
                                                       "inputMode": "monthly", "monthlyKwh": 900, "billingPeriod": 2})
if tid_pub:
    call("visitor", "POST", "/api/public/sample-invoice", json={"tariffId": tid_pub, "inputMode": "annual", "annualKwh": 4000})
    call("visitor", "POST", "/api/public/report-tariff", json={"tariff_id": tid_pub, "category": "other",
                                                             "note": "zap scan", "reporter_email": "zap@example.com"})
call("visitor", "POST", "/api/auth/login", json={"email": "nobody@example.com", "password": "wrong-password"})
call("visitor", "POST", "/api/auth/forgot-password", json={"email": "acme.energy@demo.local"})
call("visitor", "POST", "/api/auth/reset-password", json={"token": "x" * 40, "new_password": "NewPassw0rd!xyz"})
call("visitor", "POST", "/api/auth/verify-otp", json={"pending_token": "x" * 40, "code": "123456"})

sup = login("acme.energy@demo.local")
adm = login("admin1@demo.local")

# ── 2. admin (first, so there is a message for the supplier to read) ──
print("== admin")
A = lambda m, p, **kw: call("admin", m, p, adm, **kw)  # noqa: E731
A("GET", "/api/auth/me")
cfg = js(A("GET", "/api/admin/config"), {})
tariffs = js(A("GET", "/api/admin/tariffs"), [])
for p in ("/api/admin/suppliers", "/api/admin/users", "/api/admin/login-activity", "/api/admin/messages",
          "/api/admin/scheduled-notifications", "/api/admin/profiles", "/api/admin/regulated",
          "/api/admin/regulated/history", "/api/admin/notices", "/api/admin/sample-invoice", "/api/admin/dam"):
    A("GET", p)
tid = first(tariffs)
if tid:
    A("GET", f"/api/admin/tariffs/{tid}")
    A("GET", f"/api/admin/tariffs/{tid}/documents")
# settings round-trips (GET then PUT the same values back)
for p in ("/api/admin/regulated", "/api/admin/notices", "/api/admin/sample-invoice", "/api/admin/dam"):
    body = js(A("GET", p))
    if isinstance(body, dict):
        A("PUT", p, json=body)
# DAM prices: fetch preview (fake TSOC on the CI server), status, change log,
# versions (the PUT round-trip above created them), download one, restore one.
A("POST", "/api/admin/dam/fetch-tsoc")
A("GET", "/api/admin/dam/status")
A("GET", "/api/admin/dam/log?limit=50")
dam_versions = js(A("GET", "/api/admin/dam/versions"), [])
dvid = first(dam_versions)
if dvid:
    A("GET", f"/api/admin/dam/versions/{dvid}")
    A("POST", f"/api/admin/dam/versions/{dvid}/restore")
profiles = js(A("GET", "/api/admin/profiles"), [])
if profiles:
    A("PUT", f"/api/admin/profiles/{profiles[0]['id']}", json=profiles[0])
if profiles:   # a valid new profile = a copy of an existing one (12 x 48+48 values)
    A("POST", "/api/admin/profiles", json={**{k: v for k, v in profiles[0].items() if k != "id"},
                                           "name": "ZAP profile", "desc": "scan"})
suppliers = js(A("GET", "/api/admin/suppliers"), [])
A("POST", "/api/admin/suppliers", json={"name": "ZAP Test Energy", "licence": "Z-1", "email": "zap@example.com"})
A("PUT", "/api/admin/suppliers/ZAP Test Energy", json={"name": "ZAP Test Energy", "licence": "Z-2"})
nu = js(A("POST", "/api/admin/users", json={"email": "zap.user@example.com", "supplier_name": "ZAP Test Energy"}), {})
nuid = nu.get("id") if isinstance(nu, dict) else None
if nuid:
    A("PATCH", f"/api/admin/users/{nuid}/otp", json={"otp_enabled": True})
    A("PATCH", f"/api/admin/users/{nuid}/status", json={"is_active": False})
    A("POST", f"/api/admin/users/{nuid}/unlock")
    A("POST", f"/api/admin/users/{nuid}/reinvite")
msg = js(A("POST", "/api/admin/messages", json={"subject": "ZAP scan", "body": "<p>hello</p>",
                                               "audience": "selected", "target_suppliers": ["Acme Energy"]}), {})
mid = msg.get("id") if isinstance(msg, dict) else None
sch = js(A("POST", "/api/admin/scheduled-notifications", json={"subject": "ZAP reminder", "body": "<p>x</p>",
                                                               "audience": "all", "interval_months": 6}), {})
sid = sch.get("id") if isinstance(sch, dict) else None
if sid:
    A("PUT", f"/api/admin/scheduled-notifications/{sid}", json={"subject": "ZAP reminder 2", "body": "<p>y</p>",
                                                               "audience": "all", "interval_months": 12})
    A("PATCH", f"/api/admin/scheduled-notifications/{sid}/enabled", json={"enabled": False})
reports = cfg.get("reports") or cfg.get("tariffReports") or []
rid = first(reports)
if rid:
    A("PATCH", f"/api/admin/reports/{rid}", json={"status": "reviewed", "admin_note": "zap"})

# ── 3. supplier ──
print("== supplier")
S = lambda m, p, **kw: call("supplier", m, p, sup, **kw)  # noqa: E731
S("GET", "/api/auth/me")
own = js(S("GET", "/api/supplier/tariffs"), [])
S("GET", "/api/supplier/profiles")
msgs = js(S("GET", "/api/supplier/messages"), [])
smid = mid or first(msgs)
if smid:
    S("POST", f"/api/supplier/messages/{smid}/read")
    S("POST", f"/api/supplier/messages/{smid}/ack")
new_tid = doc_id = None
if own:
    base = {k: v for k, v in own[0].items()
            if k not in ("id", "status", "createdAt", "updatedAt", "rejection_reason", "hasDocs", "everPublished")}
    new = js(S("POST", "/api/supplier/tariffs", json={**base, "name": base.get("name", "T") + " (ZAP)"}), {})
    new_tid = new.get("id") if isinstance(new, dict) else None
    if new_tid:
        # A discount with free-text conditions: shown on the public results page once approved.
        S("PUT", f"/api/supplier/tariffs/{new_tid}", json={**base, "id": new_tid, "name": base.get("name", "T") + " (ZAP v2)",
                                                          "discounts": [{"type": "energy", "percentage": 5, "durationMonths": 12,
                                                                         "conditions": "Direct debit (ZAP)"}]})
        d = js(S("POST", f"/api/supplier/tariffs/{new_tid}/documents",
                 files={"file": ("zap.pdf", b"%PDF-1.4\n% zap scan\n", "application/pdf")}), {})
        doc_id = d.get("id") if isinstance(d, dict) else None
        S("GET", f"/api/supplier/tariffs/{new_tid}/documents")
        if doc_id:
            S("GET", f"/api/supplier/documents/{doc_id}/download")
    tmp = js(S("POST", "/api/supplier/tariffs", json={**base, "name": "ZAP to delete"}), {})
    if isinstance(tmp, dict) and tmp.get("id"):
        S("DELETE", f"/api/supplier/tariffs/{tmp['id']}")

# ── 4. admin actions on the supplier's new items, then clean-up deletes ──
print("== admin (review + deletes)")
if new_tid:
    A("GET", f"/api/admin/tariffs/{new_tid}/documents")
    if doc_id:
        A("GET", f"/api/admin/documents/{doc_id}/download")
        A("POST", f"/api/admin/tariffs/{new_tid}/documents",
          files={"file": ("admin.pdf", b"%PDF-1.4\n% admin\n", "application/pdf")})
    A("PATCH", f"/api/admin/tariffs/{new_tid}/status", json={"status": "approved"})
    # Visitor again, now that the supplier's discount conditions are public.
    call("visitor", "GET", "/api/public/config")
    call("visitor", "POST", "/api/public/calculate", json={"customerType": "domestic", "inputMode": "annual", "annualKwh": 4000})
    t = js(A("GET", f"/api/admin/tariffs/{new_tid}"), {})
    if isinstance(t, dict) and t:
        A("PUT", f"/api/admin/tariffs/{new_tid}", json=t)
if own:
    at = js(A("POST", "/api/admin/tariffs", json={**base, "name": "ZAP admin tariff"}), {})
    if isinstance(at, dict) and at.get("id"):
        A("DELETE", f"/api/admin/tariffs/{at['id']}")
if mid:
    A("PATCH", f"/api/admin/messages/{mid}/archive", json={"archived": True})
m2 = js(A("POST", "/api/admin/messages", json={"subject": "ZAP delete me", "body": "x", "audience": "all"}), {})
if isinstance(m2, dict) and m2.get("id"):
    A("DELETE", f"/api/admin/messages/{m2['id']}")
if sid:
    A("DELETE", f"/api/admin/scheduled-notifications/{sid}")
zp = [p for p in js(A("GET", "/api/admin/profiles"), []) if p.get("name") == "ZAP profile"]
if zp:
    A("DELETE", f"/api/admin/profiles/{zp[0]['id']}")
if nuid:
    A("DELETE", f"/api/admin/users/{nuid}")
A("DELETE", "/api/admin/suppliers/ZAP Test Energy")

print("successful requests per role:", dict(ok), "of", dict(calls))
if DRY_RUN:
    sys.exit(0)

# ── 5. OpenAPI + spider (fill gaps) ──
try:
    z("/JSON/openapi/action/importUrl/", url=APP + "/openapi.json")
except Exception as e:
    print("OpenAPI import failed:", e)
sp = z("/JSON/spider/action/scan/", url=APP + "/customer.html", recurse="true")["scan"]
while int(z("/JSON/spider/view/status/", scanId=sp)["status"]) < 100:
    time.sleep(2)
while int(z("/JSON/pscan/view/recordsToScan/")["recordsToScan"]) > 0:
    time.sleep(2)
print("requests recorded by ZAP:", z("/JSON/core/view/numberOfMessages/", baseurl=APP)["numberOfMessages"])

# ── 6. active scan ──
for rx in (r".*/api/auth/logout.*", r".*/api/auth/password.*", r".*/api/auth/email.*"):
    z("/JSON/ascan/action/excludeFromScan/", regex=rx)
z("/JSON/ascan/action/setOptionMaxScanDurationInMins/", Integer=str(MAX_SCAN_MIN))
z("/JSON/ascan/action/setOptionMaxRuleDurationInMins/", Integer="10")   # 5 cut SQLi + path traversal short
z("/JSON/ascan/action/setOptionThreadPerHost/", Integer="4")
# User Agent Fuzzer (10104) is informational only; in run 37274911928 it sent 1,775
# requests and raised 666 notes, filling ZAP's memory until ZAP shut itself down.
z("/JSON/ascan/action/disableScanners/", ids="10104")
aid = z("/JSON/ascan/action/scan/", url=APP, recurse="true", inScopeOnly="false")["scan"]
last = -1
zap_crashed = False
try:
    while (st := int(z("/JSON/ascan/view/status/", scanId=aid)["status"])) < 100:
        if st // 10 != last // 10:
            print(f"active scan {st}%  alerts so far: {z('/JSON/core/view/numberOfAlerts/', baseurl=APP)['numberOfAlerts']}", flush=True)
            last = st
        time.sleep(20)
    print("active scan done; requests sent:", z("/JSON/core/view/numberOfMessages/", baseurl=APP)["numberOfMessages"])
except requests.RequestException as e:
    zap_crashed = True
    print(f"::error::ZAP stopped responding during the active scan ({type(e).__name__}). "
          "This is a scan-setup problem, not a finding; see the 'ZAP log' step.")

# sessions still valid at the end? (if not, later parts of the scan weren't signed in)
for role, ck in (("supplier", sup), ("admin", adm)):
    r = requests.get(APP + "/api/auth/me", headers={"Cookie": f"cera_access_token={ck}"}, timeout=30)
    print(f"after scan, {role} session still valid: {r.status_code == 200} ({r.status_code})")

# ── 7. reports ──
os.makedirs(OUT, exist_ok=True)
json.dump({"ok": ok, "calls": calls}, open(os.path.join(OUT, "coverage.json"), "w"))
if zap_crashed:
    sys.exit("No report: ZAP crashed before the scan finished.")
open(os.path.join(OUT, "zap-all.json"), "w", encoding="utf-8").write(z("/OTHER/core/other/jsonreport/"))
open(os.path.join(OUT, "zap-all.html"), "w", encoding="utf-8").write(z("/OTHER/core/other/htmlreport/"))

# coverage guard
if ok["supplier"] < 8 or ok["admin"] < 30:
    sys.exit(f"Coverage too low - signed-in areas were not exercised: {dict(ok)}")
