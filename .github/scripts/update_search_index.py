#!/usr/bin/env python3
"""Regenerate search-index.json from page titles and meta descriptions."""
import glob
import html
import json
import pathlib
import re

root = pathlib.Path(__file__).resolve().parents[2]
SKIP = {"404.html", "search.html", "essays/first-person-narrative-voice.html", "essays/bait-and-switch-chapter-end.html"}


def page_type(path):
    if path.startswith("essays/"):
        return "Essay"
    if path.startswith("series/"):
        return "Series"
    if path in ("index.html", "about.html", "press.html", "books.html", "start-here.html"):
        return "Page"
    if "litrpg" in path or "books-like" in path or "cultivation" in path:
        return "Reader guide"
    return "Book"


entries = []
for f in sorted(glob.glob("*.html", root_dir=root) + glob.glob("series/*.html", root_dir=root) + glob.glob("essays/*.html", root_dir=root)):
    if f in SKIP:
        continue
    s = (root / f).read_text(encoding="utf-8", errors="replace")
    t = re.search(r"<title>(.*?)</title>", s, re.S)
    d = re.search(r'<meta name="description" content="(.*?)"', s)
    if not t:
        continue
    title = html.unescape(t.group(1)).split("|")[0].strip()
    url = "" if f == "index.html" else (f[:-len("index.html")] if f.endswith("/index.html") else f)
    entries.append({
        "title": title,
        "desc": html.unescape(d.group(1)) if d else "",
        "url": url or "./",
        "type": page_type(f),
    })

out = root / "search-index.json"
new = json.dumps(entries, ensure_ascii=False, indent=1) + "\n"
if not out.exists() or out.read_text(encoding="utf-8") != new:
    out.write_text(new, encoding="utf-8")
    print(f"search-index.json regenerated ({len(entries)} pages).")
else:
    print("search-index.json unchanged.")
