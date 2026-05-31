#!/usr/bin/env python3
"""
Bake the latest 3 Substack posts into index.html so the homepage "From the
Substack" grid is always current — reliably, server-side, visible to crawlers.

Runs in GitHub Actions on a schedule. Replaces the contents of
<div class="essay-pull-grid" id="essay-pull-grid"> ... </div> with freshly
rendered cards. Idempotent: if the posts haven't changed, the file is byte-for-
byte identical and the workflow's `git diff` finds nothing to commit.

Stdlib only — no pip installs in CI.

Usage:
    python3 .github/scripts/update_substack.py            # fetch + write
    python3 .github/scripts/update_substack.py --selftest # verify the HTML
                                                          # surgery with sample
                                                          # data, write nothing
"""
import sys
import re
import html
import pathlib
import urllib.request
from email.utils import parsedate_to_datetime
from xml.etree import ElementTree as ET

FEED_URL = "https://maloryauthor.substack.com/feed"
ROOT = pathlib.Path(__file__).resolve().parents[2]   # .github/scripts/ -> repo root
INDEX = ROOT / "index.html"
N_POSTS = 3

# On-site mirrors — if a Substack post has a local essay page, link to that.
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


def fetch_feed(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (maloryauthor.com site updater)"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def parse_items(xml_text: str, limit: int = N_POSTS) -> list[dict]:
    root = ET.fromstring(xml_text)
    items = []
    for item in root.iterfind(".//item"):
        def t(tag):
            el = item.find(tag)
            return (el.text or "").strip() if el is not None else ""
        items.append({
            "title": t("title"),
            "link": t("link"),
            "pubDate": t("pubDate"),
            "description": t("description"),
        })
        if len(items) >= limit:
            break
    return items


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
        raise SystemExit("ERROR: could not find <div id=\"essay-pull-grid\"> in index.html")
    replacement = r"\1" + "\n" + cards_html.replace("\\", "\\\\") + "\n            " + r"\2\3"
    return GRID_RE.sub(replacement, source, count=1)


SAMPLE = [
    {"title": "Wednesday Deconstruction: A Sample Post", "link": "https://maloryauthor.substack.com/p/a-sample-post",
     "pubDate": "Wed, 28 May 2026 09:00:00 GMT", "description": "<p>This is <b>sample</b> body text used only to verify the HTML surgery works correctly.</p>"},
    {"title": "What You Told Me About Something", "link": "https://maloryauthor.substack.com/p/what-you-told-me-about-boys-and-books",
     "pubDate": "Tue, 27 May 2026 09:00:00 GMT", "description": "A second sample item."},
    {"title": "Another Recent Post", "link": "https://maloryauthor.substack.com/p/another-recent-post",
     "pubDate": "Mon, 26 May 2026 09:00:00 GMT", "description": "A third sample item, slightly longer so the truncation path is exercised end to end here."},
]


def main():
    selftest = "--selftest" in sys.argv
    items = SAMPLE if selftest else parse_items(fetch_feed(FEED_URL))
    if not items:
        raise SystemExit("ERROR: no items parsed from feed")

    src = INDEX.read_text(encoding="utf-8")
    out = update_html(src, render_cards(items))

    if selftest:
        m = GRID_RE.search(out)
        grid_region = out[m.start():m.end()]   # excludes the <script> body below
        assert grid_region.count('class="essay-pull-card"') == 3, "expected exactly 3 cards in grid"
        assert "A Sample Post" in out and "Another Recent Post" in out
        assert "Tutorial Phase" not in out, "old fallback card was not replaced"
        print("SELFTEST PASS — grid replaced with 3 cards; old fallback gone; structure intact.")
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
