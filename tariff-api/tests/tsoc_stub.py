"""Stand-in for the TSOC website, so tests and the CI scan never contact TSOC.

install(mode) replaces dam_tsoc.session_factory. The fake answers each request
with a page shaped like TSOC's, built for the requested days:
  "ok"      - 48 half-hours per day up to today (Cyprus time); tomorrow is
              "not published yet" (empty table), as before ~14:00 in Cyprus
  "short"   - like "ok", but the first requested day has only 46 rows
  "blocked" - Cloudflare challenge page with HTTP 403
"""
import re
from datetime import date, timedelta

import dam_data
import dam_tsoc


class _Resp:
    def __init__(self, status_code, text, headers=None):
        self.status_code, self.text, self.headers = status_code, text, headers or {}

    encoding = "utf-8"

    def iter_content(self, chunk_size=65536):
        data = self.text.encode("utf-8")
        for i in range(0, len(data), chunk_size):
            yield data[i:i + chunk_size]

    def close(self):
        pass


def page(rows: list[tuple[str, str]]) -> str:
    body = "".join(f"<tr><td>{ts}</td><td>{p}</td><td>100.0</td></tr>" for ts, p in rows)
    return ('<html><head><title>DAM</title></head><body><table id="marketdam_graph_data"><thead>'
            "<tr><th>Timestamp</th><th>Price</th><th>Volume</th></tr></thead>"
            f"<tbody>{body}</tbody></table></body></html>")


def day_rows(d: date, skip: int = 0) -> list[tuple[str, str]]:
    return [(f"{d} {s // 2:02d}:{30 * (s % 2):02d}:00", f"{100 + s}.5") for s in range(48 - skip)]


class FakeTsoc:
    def __init__(self, mode: str = "ok"):
        self.mode, self.headers, self.urls = mode, {}, []

    def get(self, url, timeout=None, stream=False):
        self.urls.append(url)
        if self.mode == "blocked":
            return _Resp(403, "<html><head><title>Just a moment...</title></head></html>")
        m = re.search(r"startdt=(\d{2})-(\d{2})-(\d{4})&enddt=%2B(\d)days", url)
        start = date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        today = dam_data.cyprus_now().date()
        rows = []
        for i in range(int(m.group(4))):
            d = start + timedelta(days=i)
            if d <= today:
                rows += day_rows(d, skip=2 if self.mode == "short" and i == 0 else 0)
        return _Resp(200, page(rows))


def install(mode: str = "ok") -> None:
    dam_tsoc.session_factory = lambda: FakeTsoc(mode)
