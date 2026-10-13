"""
Cyprus Day-Ahead Market (DAM) prices: fetch from TSOC and build the dataset
the pricing engine reads.

TSOC publishes the half-hourly prices on a public page (not an API):
    https://tsoc.org.cy/competitive-electricity-market/dam-volume-prices-graph/
with the data server-rendered in <table id="marketdam_graph_data">. Use agreed
with TSOC (2026-10-12). Ported from the standalone "TSOC DAM Fetcher" tool.

Page quirks this module handles:
  - only +1/+3/+7 day ranges are accepted (enddt=%2BNdays);
  - an invalid or out-of-range date silently returns TODAY's data instead, so
    every returned row is checked against the requested range;
  - Cloudflare answers default library user-agents with a challenge page; an
    honest self-identifying user-agent is let through. A block is reported,
    never worked around;
  - DST change days can come back with 46 rows.

Strict rules: fetch_preview() cancels on any error or missing data rather than
producing a partly filled dataset. Nothing here writes to the database; the
admin reviews the preview and saves it through the normal PUT /api/admin/dam.

Removable on its own: nothing outside the fetch endpoint uses this module
(shared DAM helpers live in dam_data.py). It can also be switched off with
TARIFF_TSOC_FETCH=off.
"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from html.parser import HTMLParser
from typing import Callable, Iterable

import requests

from dam_data import SLOTS_PER_DAY, build_dam_payload, cyprus_now, is_dst_change_day, stored_slots

TSOC_URL = "https://tsoc.org.cy/competitive-electricity-market/dam-volume-prices-graph/"
USER_AGENT = "Mozilla/5.0 (compatible; TariffComparisonBot/1.0)"
TABLE_ID = "marketdam_graph_data"
HISTORY_START = date(2025, 10, 1)       # earliest day TSOC has
ENDDT_CHOICES = (1, 3, 7)               # the only range lengths TSOC accepts
MAX_DAYS_PER_REQUEST = 7
MAX_FETCH_DAYS = 31                     # per fetch; larger gaps go through the CSV upload
# Cyprus DAM prices cannot be negative (TARIFF_CALCULATIONS.md, Dynamic tariffs); 0 is common at solar noon.
MIN_PRICE_MWH, MAX_PRICE_MWH = 0.0, 4000.0
MAX_RESPONSE_BYTES = 5 * 1024 * 1024    # a 7-day page is ~30 KB; reading stops past this
FETCH_TIME_LIMIT = 90                   # seconds for a whole fetch, retries and pauses included

TS_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}) (\d{2}):(\d{2})(?::\d{2})?$")
PRICE_RE = re.compile(r"^-?\d+(?:\.\d+)?$")
CHALLENGE_TITLE_RE = re.compile(r"<title>\s*(just a moment|attention required)", re.IGNORECASE)

# Replaced in tests (and the CI scan server) by a fake that serves sample pages.
session_factory: Callable[[], requests.Session] = requests.Session


class DamError(Exception):
    """A fetch problem: the fetch is cancelled and the admin is told why."""


class CloudflareBlocked(DamError):
    pass


# ── time ──────────────────────────────────────────────────────────────────────

def slot_key(day: str, hour: str, minute: str) -> str:
    """Key rounded down to the half-hour: ``YYYY-MM-DD HH:MM``."""
    return f"{day} {hour}:{'30' if int(minute) >= 30 else '00'}"


def key_date(key: str) -> date:
    return date.fromisoformat(key[:10])


# ── TSOC page ─────────────────────────────────────────────────────────────────

@dataclass
class FetchedRow:
    key: str
    price: str      # €/MWh text exactly as TSOC sent it


def is_challenge_page(text: str, headers=None) -> bool:
    """Cloudflare interstitial? (Normal pages also load 'challenge-platform' scripts, so not that.)"""
    if headers is not None and str(headers.get("cf-mitigated", "")).lower() == "challenge":
        return True
    head = text[:20000]
    return bool(CHALLENGE_TITLE_RE.search(head)) or "cf-chl" in head.lower()


class _TableCells(HTMLParser):
    """Collects the <td> texts of each <tr> inside <table id=TABLE_ID>.
    Only reads text; nothing on the page is ever run."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.found = False
        self.rows: list[list[str]] = []
        self._depth = 0          # table nesting depth inside the data table
        self._row: list[str] | None = None
        self._cell: list[str] | None = None

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            if self._depth:
                self._depth += 1
            elif dict(attrs).get("id") == TABLE_ID:
                self.found = True
                self._depth = 1
        elif self._depth == 1 and tag == "tr":
            self._row = []
        elif self._depth == 1 and tag == "td" and self._row is not None:
            self._cell = []

    def handle_endtag(self, tag):
        if tag == "table" and self._depth:
            self._depth -= 1
        elif self._depth == 1 and tag == "td" and self._cell is not None:
            self._row.append("".join(self._cell).strip())
            self._cell = None
        elif self._depth == 1 and tag == "tr" and self._row is not None:
            self.rows.append(self._row)
            self._row = None

    def handle_data(self, data):
        if self._cell is not None:
            self._cell.append(data)


def parse_tsoc_html(html: str) -> tuple[list[FetchedRow], list[str]]:
    """Parse the data table. Returns (rows, problems)."""
    if is_challenge_page(html):
        raise CloudflareBlocked("TSOC returned a Cloudflare challenge page instead of data.")
    parser = _TableCells()
    parser.feed(html)
    parser.close()
    if not parser.found:
        raise DamError(f'No <table id="{TABLE_ID}"> on the TSOC page; the page layout may have changed.')
    rows: list[FetchedRow] = []
    problems: list[str] = []
    for cells in parser.rows:
        if not cells:
            continue  # header row (<th> only)
        if len(cells) < 2:
            problems.append(f"row with too few cells: {cells!r}")
            continue
        m = TS_RE.match(cells[0])
        if not m:
            problems.append(f"row with unreadable timestamp: {cells[0][:40]!r}")
            continue
        if not PRICE_RE.match(cells[1]):
            problems.append(f"{cells[0]}: price is not a number: {cells[1][:40]!r}")
            continue
        rows.append(FetchedRow(slot_key(*m.groups()), cells[1]))
    return rows, problems


def tsoc_url(start: date, ndays: int) -> str:
    return f"{TSOC_URL}?startdt={start:%d-%m-%Y}&enddt=%2B{ndays}days"


class Fetcher:
    """One request at a time, a pause between requests, retries with backoff.
    The whole fetch (all requests, retries and pauses) must finish within
    time_limit seconds, and no page may be larger than MAX_RESPONSE_BYTES."""

    def __init__(self, delay: float = 1.5, retries: int = 3, timeout: float = 20,
                 time_limit: float = FETCH_TIME_LIMIT, session=None,
                 sleep: Callable[[float], None] = time.sleep, clock: Callable[[], float] = time.monotonic):
        self.session = session or session_factory()
        self.session.headers.update({"User-Agent": USER_AGENT})
        self.delay = delay
        self.retries = retries
        self.timeout = timeout
        self.sleep = sleep
        self.clock = clock
        self.time_limit = time_limit
        self.deadline = clock() + time_limit
        self._requested_once = False

    def _remaining(self) -> float:
        left = self.deadline - self.clock()
        if left <= 0:
            raise DamError(f"TSOC is too slow: the fetch was stopped after {self.time_limit:g} seconds.")
        return left

    def _read(self, resp) -> str:
        """Read the body in chunks, stopping as soon as it is too large or too slow."""
        body = bytearray()
        for chunk in resp.iter_content(chunk_size=65536):
            body += chunk
            if len(body) > MAX_RESPONSE_BYTES:
                raise DamError(f"TSOC sent an unexpectedly large page (over {MAX_RESPONSE_BYTES // 1048576} MB).")
            self._remaining()
        return body.decode(resp.encoding or "utf-8", errors="replace")

    def get(self, url: str) -> str:
        last_problem = ""
        for attempt in range(1, self.retries + 1):
            if self._requested_once:
                pause = self.delay if attempt == 1 else self.delay * 2 ** (attempt - 1)
                if pause >= self._remaining():
                    raise DamError(f"TSOC is too slow: the fetch was stopped after {self.time_limit:g} seconds"
                                   + (f" ({last_problem})." if last_problem else "."))
                self.sleep(pause)
            self._requested_once = True
            try:
                resp = self.session.get(url, timeout=min(self.timeout, self._remaining()), stream=True)
            except (requests.Timeout, requests.ConnectionError) as exc:
                last_problem = type(exc).__name__
                continue
            try:
                text = self._read(resp)
            except (requests.Timeout, requests.ConnectionError) as exc:
                last_problem = type(exc).__name__
                continue
            finally:
                resp.close()
            challenge = is_challenge_page(text, getattr(resp, "headers", None))
            if resp.status_code == 403 or challenge:
                raise CloudflareBlocked(
                    f"TSOC/Cloudflare refused the request (HTTP {resp.status_code}"
                    f"{', challenge page' if challenge else ''}). Try later, or upload a CSV instead."
                )
            if resp.status_code >= 500:
                last_problem = f"HTTP {resp.status_code}"
                continue
            if resp.status_code != 200:
                raise DamError(f"TSOC returned HTTP {resp.status_code}.")
            return text
        raise DamError(f"TSOC did not answer after {self.retries} attempts ({last_problem}).")


def plan_requests(days: Iterable[date]) -> list[tuple[date, int]]:
    """Group days into contiguous runs and split into (start, +Ndays) requests."""
    days = sorted(set(days))
    runs: list[list[date]] = []
    for d in days:
        if runs and d - runs[-1][-1] == timedelta(days=1):
            runs[-1].append(d)
        else:
            runs.append([d])
    plan = []
    for run in runs:
        for i in range(0, len(run), MAX_DAYS_PER_REQUEST):
            chunk = run[i: i + MAX_DAYS_PER_REQUEST]
            ndays = next(n for n in ENDDT_CHOICES if n >= len(chunk))
            plan.append((chunk[0], ndays))
    return plan


@dataclass
class FetchResult:
    rows: dict[str, str] = field(default_factory=dict)         # key -> €/MWh text
    per_day: dict[date, int] = field(default_factory=dict)
    dropped: list[str] = field(default_factory=list)            # "fallback to today" rows
    problems: list[str] = field(default_factory=list)
    conflicts: list[str] = field(default_factory=list)          # same slot twice, different prices
    requests: list[str] = field(default_factory=list)


def fetch_days(fetcher: Fetcher, days: Iterable[date]) -> FetchResult:
    result = FetchResult()
    seen: dict[str, list[str]] = {}
    for start, ndays in plan_requests(days):
        end = start + timedelta(days=ndays - 1)
        url = tsoc_url(start, ndays)
        result.requests.append(url)
        rows, problems = parse_tsoc_html(fetcher.get(url))
        result.problems += [f"[{start} +{ndays} days] {p}" for p in problems]
        dropped_here: dict[str, int] = {}
        for row in rows:
            d = key_date(row.key)
            if not (start <= d <= end):
                dropped_here[d.isoformat()] = dropped_here.get(d.isoformat(), 0) + 1
                continue
            result.per_day[d] = result.per_day.get(d, 0) + 1
            seen.setdefault(row.key, []).append(row.price)
        for ds, n in sorted(dropped_here.items()):
            result.dropped.append(
                f"asked for {start}..{end} but TSOC sent {n} row(s) dated {ds} "
                "(TSOC answers with today's prices when a day is not available)"
            )
    for key, prices in sorted(seen.items()):
        distinct = list(dict.fromkeys(prices))
        if len(distinct) == 1:
            result.rows[key] = distinct[0]
        else:
            result.conflicts.append(f"{key}: TSOC sent different prices ({', '.join(prices)})")
    return result


# ── preview ───────────────────────────────────────────────────────────────────

def fetch_preview(stored_daily: list | None, *, now: datetime | None = None, session=None,
                  sleep: Callable[[float], None] = time.sleep,
                  clock: Callable[[], float] = time.monotonic) -> dict:
    """Fetch the days after the last stored day, up to tomorrow (Cyprus time).

    Returns {"ok": True, "payload": {...} | None, "report": {...}} or
    {"ok": False, "reasons": [...], "report": {...}}. Never writes anything."""
    existing = stored_slots(stored_daily)
    cy_now = now or cyprus_now()
    today = cy_now.date()
    tomorrow = today + timedelta(days=1)
    last = key_date(max(existing)) if existing else None
    start = max(last + timedelta(days=1) if last else HISTORY_START, HISTORY_START)
    target = [start + timedelta(days=i) for i in range((tomorrow - start).days + 1)]
    report = {"lastStoredDate": last.isoformat() if last else None, "today": today.isoformat(),
              "requested": [d.isoformat() for d in target], "requests": [], "addedByDay": {},
              "notYetPublished": []}

    def cancel(reasons: list[str]) -> dict:
        return {"ok": False, "reasons": reasons, "report": report}

    if not target:
        return {"ok": True, "payload": None, "report": report,
                "message": f"Already up to date to {last.isoformat()}."}
    if len(target) > MAX_FETCH_DAYS:
        return cancel([
            f"{len(target)} days are missing (from {start} to {tomorrow}); one fetch covers at most "
            f"{MAX_FETCH_DAYS}. Fill the gap with a CSV upload first, then fetch."
        ])

    try:
        fetch = fetch_days(Fetcher(session=session, sleep=sleep, clock=clock), target)
    except DamError as exc:
        return cancel([str(exc)])
    report["requests"] = fetch.requests

    reasons: list[str] = []
    reasons += [f"Unreadable row: {p}" for p in fetch.problems]
    reasons += [f"Wrong day returned: {x}" for x in fetch.dropped]
    reasons += [f"Conflicting prices: {x}" for x in fetch.conflicts]
    for d in target:
        n = fetch.per_day.get(d, 0)
        if d == tomorrow and n == 0:
            report["notYetPublished"].append(d.isoformat())
            continue
        if n != SLOTS_PER_DAY:
            have = {k for k in fetch.rows if key_date(k) == d}
            missing = [f"{s // 2:02d}:{30 * (s % 2):02d}" for s in range(SLOTS_PER_DAY)
                       if f"{d.isoformat()} {s // 2:02d}:{30 * (s % 2):02d}" not in have]
            note = " (clock-change day)" if is_dst_change_day(d) else ""
            if n == 0:
                reasons.append(f"{d}{note}: no prices from TSOC.")
            else:
                reasons.append(f"{d}{note}: {n} of {SLOTS_PER_DAY} half-hours"
                               + (f"; missing {', '.join(missing)}" if missing else "") + ".")
    for key, price in fetch.rows.items():
        p = float(price)
        if not (MIN_PRICE_MWH <= p <= MAX_PRICE_MWH):
            reasons.append(f"{key}: price {price} €/MWh is outside {MIN_PRICE_MWH:g}..{MAX_PRICE_MWH:g}.")
    if reasons:
        return cancel(reasons)

    new = {k: float(v) / 1000 for k, v in fetch.rows.items() if k not in existing}
    for k in new:
        d = k[:10]
        report["addedByDay"][d] = report["addedByDay"].get(d, 0) + 1
    if not new:
        return {"ok": True, "payload": None, "report": report,
                "message": f"Already up to date to {last.isoformat() if last else '—'}; "
                           "tomorrow's prices are not published yet."}
    payload = build_dam_payload({**existing, **new})
    return {"ok": True, "payload": payload, "report": report,
            "message": f"Fetched {len(new)} half-hours for {len(report['addedByDay'])} day(s), "
                       f"{min(report['addedByDay'])} to {max(report['addedByDay'])}. Review, then Save."}
