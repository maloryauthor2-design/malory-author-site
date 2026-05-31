#!/usr/bin/env python3
"""
Bake the latest 3 Substack posts into index.html so the homepage "From the
Substack" grid is always current — reliably, server-side, visible to crawlers.

Runs in GitHub Actions on a schedule. Replaces the contents of
<div class="essay-pull-grid" id="essay-pull-grid"> ... </div> with freshly
rendered cards. Idempotent: if the posts haven't changed, the file is byte-for-
byte identical and the workflow's `git diff` finds nothing to commit.

Resilient fetch: tries the Substack RSS feed directly (with browser headers),
and if that's blocked — GitHub's datacenter IPs are often 403'd by Cloudflare —
falls back to the rss2json proxy, which fetches the feed server-side. Stdlib
only; no pip installs in CI.

Usage:
    python3 .github/scripts/update_substack.py            # fetch + write
    python3 .github/scripts/update_substack.py --selftest # verify HTML surgery
    python3 .github/scripts/update_substack.py --proxytest # force the proxy path
"""
import sys
import re
import html
import json
import pathlib
import urllib.request
import urllib.parse
from email.utils import parsedate_to_datetime
from xml.etree import ElementTree as ET

FEED_URL = "https://maloryauthor.substack.com/feed"
PROXY_URL = ("https://api.rss2json.com/v1/api.json?rss_url="
             + urllib.parse.quote(FEED_URL, safe=""))
ROOT = pathlib.Path(__file__).resolve().parents[2]   # .github/scripts/ -> repo root
INDEX = ROOT / "index.html"
N_POSTS = 3

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
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def _parse_rss(xml_text: str, limit: int) -> list[dict]:
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


def get_items(limit: int = N_POSTS, force_proxy: bool = False) -> list[dict]:
    # 1) direct RSS (unless we're explicitly testing the proxy path)
    if not force_proxy:
        try:
            items = _parse_rss(_get(FEED_URL), limit)
            if items:
                print(f"Fetched {len(items)} posts via direct Substack RSS.")
                return items
            print("Direct RSS returned no items; trying proxy.")
        except Exception as ex:                       # noqa: BLE001
            print(f"Direct RSS failed ({type(ex).__name__}: {ex}); trying proxy.")

    # 2) rss2json proxy (fetches the feed server-side; not blocked on runner IPs)
    try:
        data = json.loads(_get(PROXY_URL))
        if data.get("status") == "ok" and data.get("items"):
            items = [{"title": i.get("title", ""), "link": i.get("link", ""),
                      "pubDate": i.get("pubDate", ""), "description": i.get("description", "")}
                     for i in data["items"][:limit]]
            print(f"Fetched {len(items)} posts via rss2json proxy.")
            return items
        raise RuntimeError(f"proxy status={data.get('status')!r}")
    except Exception as ex:                            # noqa: BLE001
        raise SystemExit(f"ERROR: could not fetch feed (direct + proxy both failed): {ex}")


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


def render_cards(items: list[dict]) -> str:
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
        raise SystemExit("ERROR: no items to render")

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
              "would change file:" , out != src)
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
