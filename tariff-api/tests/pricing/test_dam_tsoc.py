r"""Fetching DAM prices from TSOC (dam_tsoc.py): page parsing, the strict
cancel rules, and the dataset built from the prices. No network: TSOC is
replaced by saved sample pages (tests/fixtures/tsoc/) or generated pages.

Run from tariff-api/:  .venv\Scripts\python.exe -m pytest tests/pricing
"""

import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pytest
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import dam_data  # noqa: E402
import dam_tsoc  # noqa: E402
from tsoc_stub import day_rows, page  # noqa: E402

SAMPLES = Path(__file__).resolve().parents[1] / "fixtures" / "tsoc"


def sample(name: str) -> str:
    return (SAMPLES / name).read_text(encoding="utf-8")


class Resp:
    def __init__(self, status_code=200, text="", headers=None):
        self.status_code, self.text, self.headers = status_code, text, headers or {}

    encoding = "utf-8"

    def iter_content(self, chunk_size=65536):
        data = self.text.encode("utf-8")
        for i in range(0, len(data), chunk_size):
            yield data[i:i + chunk_size]

    def close(self):
        pass


class Session:
    """Answers by startdt; any other day is an unpublished (empty) page."""

    def __init__(self, by_startdt=None):
        self.headers, self.urls = {}, []
        self.by_startdt = by_startdt or {}

    def get(self, url, timeout=None, stream=False):
        self.urls.append(url)
        startdt = re.search(r"startdt=([\d-]+)", url).group(1)
        resp = self.by_startdt.get(startdt, Resp(200, sample("tsoc_empty_unpublished.html")))
        if isinstance(resp, list):
            resp = resp.pop(0)
        if isinstance(resp, Exception):
            raise resp
        return resp


def stored(*days: str, price=0.1):
    """damDailyData holding full days (€/kWh)."""
    return dam_data.build_dam_payload({
        f"{d} {s // 2:02d}:{30 * (s % 2):02d}": price for d in days for s in range(48)
    })["damDailyData"]


def gen(*days: date, skip_first=0):
    rows = []
    for i, d in enumerate(days):
        rows += day_rows(d, skip=skip_first if i == 0 else 0)
    return Resp(200, page(rows))


def preview(stored_daily, session, now):
    return dam_tsoc.fetch_preview(stored_daily, now=now, session=session, sleep=lambda s: None)


# Cyprus time 2026-10-01 10:00 -> today 10-01, tomorrow 10-02 (not yet published).
NOW_OCT1 = datetime(2026, 10, 1, 10, 0)


# ── page parsing ──────────────────────────────────────────────────────────────

def test_sample_page_parses_48_rows():
    rows, problems = dam_tsoc.parse_tsoc_html(sample("tsoc_2026-10-01_1days.html"))
    assert problems == [] and len(rows) == 48
    assert rows[0].key == "2026-10-01 00:00" and rows[-1].key == "2026-10-01 23:30"


def test_page_scripts_are_only_text():
    # The empty sample contains <script>alert(...)</script>; it is never run or kept.
    rows, problems = dam_tsoc.parse_tsoc_html(sample("tsoc_empty_unpublished.html"))
    assert rows == [] and problems == []


def test_missing_table_means_layout_changed():
    with pytest.raises(dam_tsoc.DamError, match="layout may have changed"):
        dam_tsoc.parse_tsoc_html("<html><body><table id='other'></table></body></html>")


def test_bad_rows_are_reported():
    html = page([("2026-10-01 00:00:00", "abc"), ("yesterday", "10")])
    rows, problems = dam_tsoc.parse_tsoc_html(html)
    assert rows == [] and len(problems) == 2


def test_normal_page_with_cloudflare_script_is_not_a_challenge():
    assert not dam_tsoc.is_challenge_page(sample("tsoc_2026-10-01_1days.html"))
    assert dam_tsoc.is_challenge_page(sample("cloudflare_challenge.html"))


def test_plan_requests_uses_only_allowed_lengths():
    d = date(2026, 1, 1)
    days = [d + timedelta(days=i) for i in range(10)] + [date(2026, 2, 1), date(2026, 2, 2)]
    assert dam_tsoc.plan_requests(days) == [(date(2026, 1, 1), 7), (date(2026, 1, 8), 3), (date(2026, 2, 1), 3)]


def test_identifies_itself_honestly():
    session = Session({"01-10-2026": Resp(200, sample("tsoc_2026-10-01_1days.html"))})
    preview(stored("2026-09-30"), session, NOW_OCT1)
    assert session.headers["User-Agent"] == dam_tsoc.USER_AGENT
    assert "Chrome" not in dam_tsoc.USER_AGENT and "Bot" in dam_tsoc.USER_AGENT


# ── successful preview ────────────────────────────────────────────────────────

def test_adds_missing_days_and_leaves_tomorrow_when_unpublished():
    session = Session({"01-10-2026": Resp(200, sample("tsoc_2026-10-01_1days.html"))})
    r = preview(stored("2026-09-30"), session, NOW_OCT1)
    assert r["ok"], r
    assert r["report"]["addedByDay"] == {"2026-10-01": 48}
    assert r["report"]["notYetPublished"] == ["2026-10-02"]
    assert session.urls == [dam_tsoc.tsoc_url(date(2026, 10, 1), 3)]   # today + tomorrow in one request
    p = r["payload"]
    assert dam_data.dataset_dates(p["damDailyData"]) == ["2026-09-30", "2026-10-01"]
    oct1 = p["damDailyData"][9][0]
    assert oct1["slots"][0] == pytest.approx(275 / 1000)                  # €/MWh -> €/kWh
    assert p["damRowCount"] == 96


def test_stored_prices_are_kept_exactly():
    old = stored("2026-09-30", price=0.123456789)
    session = Session({"01-10-2026": Resp(200, sample("tsoc_2026-10-01_1days.html"))})
    p = preview(old, session, NOW_OCT1)["payload"]
    assert p["damDailyData"][8][-1]["slots"] == [0.123456789] * 48


def test_already_up_to_date_makes_no_request():
    session = Session()
    r = preview(stored("2026-10-01", "2026-10-02"), session, NOW_OCT1)
    assert r["ok"] and r["payload"] is None and "up to date" in r["message"]
    assert session.urls == []


def test_tomorrow_not_published_and_nothing_else_missing():
    session = Session()
    r = preview(stored("2026-10-01"), session, NOW_OCT1)
    assert r["ok"] and r["payload"] is None
    assert r["report"]["notYetPublished"] == ["2026-10-02"]


# ── strict rules: any error or missing data cancels ──────────────────────────

def _cancelled(r, *needles):
    assert r["ok"] is False, r
    text = "\n".join(r["reasons"])
    for n in needles:
        assert n in text, text
    assert "payload" not in r


def test_dst_day_with_46_rows_cancels():
    session = Session({"29-03-2026": Resp(200, sample("tsoc_2026-03-29_dst_46rows.html"))})
    r = preview(stored("2026-03-28"), session, datetime(2026, 3, 29, 9, 0))
    _cancelled(r, "2026-03-29 (clock-change day): 46 of 48", "05:00", "05:30")


def test_partial_day_cancels():
    session = Session({"30-09-2026": gen(date(2026, 9, 30), date(2026, 10, 1), skip_first=1)})
    r = preview(stored("2026-09-29"), session, NOW_OCT1)
    _cancelled(r, "2026-09-30: 47 of 48", "23:30")


def test_missing_day_before_tomorrow_cancels():
    # TSOC has nothing for today: that is missing data, not "not yet published".
    session = Session({"01-10-2026": Resp(200, sample("tsoc_empty_unpublished.html"))})
    _cancelled(preview(stored("2026-09-30"), session, NOW_OCT1), "2026-10-01: no prices")


def test_partly_published_tomorrow_cancels():
    rows = day_rows(date(2026, 10, 1)) + day_rows(date(2026, 10, 2), skip=20)
    session = Session({"01-10-2026": Resp(200, page(rows))})
    _cancelled(preview(stored("2026-09-30"), session, NOW_OCT1), "2026-10-02: 28 of 48")


def test_fallback_to_today_cancels():
    # Tomorrow (10-10) is asked for; TSOC silently sends today's (10-09) prices instead.
    session = Session({"10-10-2026": Resp(200, sample("tsoc_fallback_today_2026-10-09.html"))})
    r = preview(stored("2026-10-09"), session, datetime(2026, 10, 9, 15, 0))
    _cancelled(r, "Wrong day returned", "dated 2026-10-09")


def test_conflicting_prices_cancel():
    rows = day_rows(date(2026, 10, 1)) + [("2026-10-01 00:00:00", "999")]
    session = Session({"01-10-2026": Resp(200, page(rows))})
    _cancelled(preview(stored("2026-09-30"), session, NOW_OCT1), "Conflicting prices", "2026-10-01 00:00")


def test_unreadable_row_cancels():
    rows = day_rows(date(2026, 10, 1)) + [("2026-10-01 00:00:00", "n/a")]
    session = Session({"01-10-2026": Resp(200, page(rows))})
    _cancelled(preview(stored("2026-09-30"), session, NOW_OCT1), "Unreadable row")


@pytest.mark.parametrize("price", ["4000.01", "-0.5"])
def test_price_out_of_range_cancels(price):
    rows = [(ts, price if i == 5 else p) for i, (ts, p) in enumerate(day_rows(date(2026, 10, 1)))]
    session = Session({"01-10-2026": Resp(200, page(rows))})
    _cancelled(preview(stored("2026-09-30"), session, NOW_OCT1), f"price {price}")


@pytest.mark.parametrize("response", [
    Resp(403, sample("cloudflare_challenge.html")),
    Resp(403, "Forbidden"),
    Resp(200, sample("cloudflare_challenge.html")),
    Resp(200, "<html></html>", {"cf-mitigated": "challenge"}),
])
def test_cloudflare_block_cancels_without_retrying(response):
    session = Session({"01-10-2026": response})
    _cancelled(preview(stored("2026-09-30"), session, NOW_OCT1), "Cloudflare")
    assert len(session.urls) == 1


def test_retries_server_errors_then_succeeds():
    seq = [Resp(503, "busy"), requests.Timeout("slow"), Resp(200, sample("tsoc_2026-10-01_1days.html"))]
    sleeps = []
    r = dam_tsoc.fetch_preview(stored("2026-09-30"), now=NOW_OCT1, session=Session({"01-10-2026": seq}),
                               sleep=sleeps.append)
    assert r["ok"], r
    assert sleeps == [3.0, 6.0]


def test_network_failure_cancels():
    seq = [requests.ConnectionError("down")] * 3
    _cancelled(preview(stored("2026-09-30"), Session({"01-10-2026": seq}), NOW_OCT1), "did not answer")


def test_oversized_page_cancels_without_reading_it_all():
    big = Resp(200, "<html>" + "x" * (dam_tsoc.MAX_RESPONSE_BYTES + 1) + "</html>")
    read = []
    original = big.iter_content
    big.iter_content = lambda chunk_size=65536: (read.append(len(c)) or c for c in original(chunk_size))
    _cancelled(preview(stored("2026-09-30"), Session({"01-10-2026": big}), NOW_OCT1), "unexpectedly large")
    assert sum(read) <= dam_tsoc.MAX_RESPONSE_BYTES + 65536


def test_slow_tsoc_is_stopped_at_the_time_limit():
    # TSOC answers every request, but each takes 50 seconds: the second request
    # pushes the fetch past the 90-second limit and it is cancelled there.
    now = [0.0]

    class SlowSession(Session):
        def get(self, url, timeout=None, stream=False):
            self.urls.append(url)
            assert timeout <= 20
            now[0] += 50
            start = re.search(r"startdt=(\d+)-(\d+)-(\d+)", url).groups()
            d = date(int(start[2]), int(start[1]), int(start[0]))
            return gen(*[d + timedelta(days=i) for i in range(7)])

    session = SlowSession()
    r = dam_tsoc.fetch_preview(stored("2026-09-20"), now=NOW_OCT1, session=session,
                               sleep=lambda s: now.__setitem__(0, now[0] + s), clock=lambda: now[0])
    _cancelled(r, "too slow", "90 seconds")
    assert len(session.urls) == 2


def test_layout_change_cancels():
    session = Session({"01-10-2026": Resp(200, "<html><body>new site</body></html>")})
    _cancelled(preview(stored("2026-09-30"), session, NOW_OCT1), "layout may have changed")


def test_gap_over_31_days_cancels_without_requests():
    session = Session()
    _cancelled(preview(stored("2026-08-01"), session, NOW_OCT1), "at most 31", "CSV upload")
    assert session.urls == []


def test_no_stored_data_cancels_as_a_large_gap():
    _cancelled(preview([], Session(), NOW_OCT1), "at most 31")
