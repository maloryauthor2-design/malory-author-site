#!/usr/bin/env python3
"""
Bake the latest 3 Substack posts into index.html so the homepage "From the
Substack" grid is always current — reliably, server-side, visible to crawlers.

Runs in GitHub Actions on a schedule. Replaces the contents of
<div class="essay-pull-grid" id="essay-pull-grid"> ... </div> with freshly
rendered cards. Idempotent: if the posts haven't changed, the file is byte-for-
byte identical and the workflow's `git diff` finds nothing to commit.

Resilient fetch, three independent sources, each retried with backoff:
  1) Substack RSS directly (browser headers) — often 403'd on datacenter IPs
  2) rss2json proxy (fetches the feed server-side)
  3) allorigins proxy (raw RSS, different infra to rss2json)
If ALL sources are down (rare simultaneous outage), the script leaves
index.html untouched and exits 0 — the previously baked posts stay in place and
the client-side live-pull is a second safety net, so a transient blip does NOT
fail the workflow (no false-alarm red X / failure email). Stdlib only.

Usage:
    python3 .github/scripts/update_substack.py            # fetch + write
    python3 .github/scripts/update_substack.py --selftest # verify HTML surgery
    python3 .github/scripts/update_substack.py --proxytest # force the proxy path
"""
import sys
import re
import html
import json
import time
import pathlib
import urllib.request
import urllib.parse
from email.utils import parsedate_to_datetime
from xml.etree import ElementTree as ET

FEED_URL = "https://maloryauthor.substack.com/feed"
PROXY_RSS2JSON = ("https://api.rss2json.com/v1/api.json?rss_url="
                  + urllib.parse.quote(FEED_URL, safe=""))
PROXY_ALLORIGINS = ("https://api.allorigins.win/raw?url="
                    + urllib.parse.quote(FEED_URL, safe=""))
ROOT = pathlib.Path(__file__).resolve().parents[2]   # .github/scripts/ -> repo root
INDEX = ROOT / "index.html"
N_POSTS = 3
RETRIES = 3
BACKOFF = 2  # seconds, multiplied by attempt number

HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/124.0.0.0 Safari/537.36"),
    "Accept": "application/rss+xml, application/xml, text/xml, application/json, */*",
    "Accept-Language": "en-US,en;q=0.9",
}

MIRRORS = {
    "wednesday-deconstruction-using-first": "essays/first-person-narrative-voice.html",
    "what-you-told-me-about-boys-and-books": "essays/what-you-told-me-about-boys-and-books.html",
    "wednesday-deconstruction-the-art": "essays/bait-and-switch-chapter-end.html",
}

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

GRID_RE = re.compile(
    r'(<div class="essay-pull-grid" id="essay-pull-grid">).*?(</div>)(\s*<script)',
    re.S,
)


def _get(url: str) -> str:
    """GET with retries + backoff. Raises the last exception if all attempts fail."""
    last = None
    for attempt in range(1, RETRIES + 1):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as ex:                       # noqa: BLE001
            last = ex
            if attempt < RETRIES:
                time.sleep(BACKOFF * attempt)
    raise last


def _parse_rss(xml_text: str, limit: int) -> list:
    root = ET.fromstring(xml_text)
    out = []
    for item in root.iterfind(".//item"):
        def t(tag):
            el = item.find(tag)
            return (el.text or "").strip() if el is not None else ""
        out.append({"title": t("title"), "link": t("link"),
                    "pubDate": t("pubDate"), "description": t("description")})
        if len(out) >= limit:
            break
    return out


def _from_rss2json(limit: int) -> list:
    data = json.loads(_get(PROXY_RSS2JSON))
    if data.get("status") == "ok" and data.get("items"):
        return [{"title": i.get("title", ""), "link": i.get("link", ""),
                 "pubDate": i.get("pubDate", ""), "description": i.get("description", "")}
                for i in data["items"][:limit]]
    raise RuntimeError(f"rss2json status={data.get('status')!r}")


def get_items(limit: int = N_POSTS, force_proxy: bool = False) -> list:
    """Try each source in turn; return [] only if every source fails."""
    sources = []
    if not force_proxy:
        sources.append(("direct Substack RSS", lambda: _parse_rss(_get(FEED_URL), limit)))
    sources.append(("rss2json proxy", lambda: _from_rss2json(limit)))
    sources.append(("allorigins proxy", lambda: _parse_rss(_get(PROXY_ALLORIGINS), limit)))

    for name, fn in sources:
        try:
            items = fn()
            if items:
                print(f"Fetched {len(items)} posts via {name}.")
                return items
            print(f"{name} returned no items; trying next source.")
        except Exception as ex:                       # noqa: BLE001
            print(f"{name} failed ({type(ex).__name__}: {ex}); trying next source.")

    print("WARNING: all sources failed (Substack + both proxies). "
          "Leaving index.html unchanged; existing posts and the client-side "
          "live-pull cover the gap. Not failing the workflow.")
    return []


def slug_of(link: str) -> str:
    m = re.search(r"/p/([a-z0-9-]+)", link or "")
    return m.group(1) if m else ""


def category_for(title: str) -> str:
    t = (title or "").lower()
    if t.startswith("wednesday deconstruction") or "art of" in t:
        return "Craft"
    if "what you told" in t or "manufacture" in t or "research" in t:
        return "Research"
    return "Essay"


def clean_title(title: str) -> str:
    return re.sub(r"^Wednesday Deconstruction:\s*", "", title or "", flags=re.I)


def format_date(pub: str) -> str:
    try:
        d = parsedate_to_datetime(pub)
        return f"{d.day} {MONTHS[d.month - 1]} {d.year}"
    except Exception:
        return ""


def short_desc(desc_html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", desc_html or "")
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return (text[:97] + "...") if len(text) > 100 else text


def e(s: str) -> str:
    return html.escape(s or "", quote=True)


def render_cards(items: list) -> str:
    cards = []
    for p in items:
        slug = slug_of(p["link"])
        href = MIRRORS.get(slug, p["link"])
        external = slug not in MIRRORS
        attrs = f'href="{e(href)}"'
        if external:
            attrs += ' target="_blank" rel="noopener noreferrer"'
        cards.append(
            f'                <a {attrs} class="essay-pull-card">\n'
            f'                    <div class="essay-pull-meta"><span class="cat">{e(category_for(p["title"]))}</span>'
            f'<span class="sep">&middot;</span>'
            f'<span class="date">{e(format_date(p["pubDate"]))}</span></div>\n'
            f'                    <h3>{e(clean_title(p["title"]))}</h3>\n'
            f'                    <p>{e(short_desc(p["description"]))}</p>\n'
            f'                    <span class="essay-pull-cta">Read the essay '
            f'<i class="fas fa-arrow-right" aria-hidden="true"></i></span>\n'
            f'                </a>'
        )
    return "\n".join(cards)


def update_html(source: str, cards_html: str) -> str:
    if not GRID_RE.search(source):
        raise SystemExit('ERROR: could not find <div id="essay-pull-grid"> in index.html')
    replacement = r"\1" + "\n" + cards_html.replace("\\", "\\\\") + "\n            " + r"\2\3"
    return GRID_RE.sub(replacement, source, count=1)


def main():
    selftest = "--selftest" in sys.argv
    proxytest = "--proxytest" in sys.argv

    if selftest:
        items = [
            {"title": "Wednesday Deconstruction: A Sample Post",
             "link": "https://maloryauthor.substack.com/p/a-sample-post",
             "pubDate": "Wed, 28 May 2026 09:00:00 GMT",
             "description": "<p>Sample <b>body</b> text to verify the HTML surgery.</p>"},
            {"title": "What You Told Me About Something",
             "link": "https://maloryauthor.substack.com/p/what-you-told-me-about-boys-and-books",
             "pubDate": "Tue, 27 May 2026 09:00:00 GMT", "description": "Second sample."},
            {"title": "Another Recent Post",
             "link": "https://maloryauthor.substack.com/p/another-recent-post",
             "pubDate": "Mon, 26 May 2026 09:00:00 GMT",
             "description": "Third sample, a little longer so truncation runs."},
        ]
    else:
        items = get_items(force_proxy=proxytest)

    if not items:
        # No fetch succeeded — leave the file as-is and exit cleanly (see get_items).
        print("No items fetched — homepage left unchanged.")
        return

    src = INDEX.read_text(encoding="utf-8")
    out = update_html(src, render_cards(items))

    if selftest:
        m = GRID_RE.search(out)
        assert out[m.start():m.end()].count('class="essay-pull-card"') == 3
        assert "A Sample Post" in out and "Tutorial Phase" not in out
        print("SELFTEST PASS — grid replaced with 3 cards; old fallback gone.")
        return
    if proxytest:
        print("PROXYTEST: fetched via proxy and rendered;",
              "would change file:", out != src)
        return

    if out != src:
        INDEX.write_text(out, encoding="utf-8")
        print(f"Updated index.html with {len(items)} latest posts:")
        for p in items:
            print(f"  - {format_date(p['pubDate'])}  {clean_title(p['title'])}")
    else:
        print("No change — homepage already shows the latest posts.")


if __name__ == "__main__":
    main()
