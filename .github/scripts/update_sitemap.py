#!/usr/bin/env python3
"""Regenerate sitemap.xml from the HTML files actually in the repo.

lastmod comes from each file's last git commit date (requires full history —
the workflow checks out with fetch-depth: 0). Run from anywhere in the repo.
"""
import glob
import pathlib
import subprocess

root = pathlib.Path(__file__).resolve().parents[2]
BASE = "https://maloryauthor.com/"

PRIORITY = {"": "1.00", "books.html": "0.90"}
CHANGEFREQ = {"": "daily", "books.html": "weekly"}


def url_for(path):
    if path == "index.html":
        return ""
    if path.endswith("/index.html"):
        return path[: -len("index.html")]
    return path


def lastmod(path):
    out = subprocess.run(
        ["git", "log", "-1", "--format=%cs", "--", path],
        cwd=root, capture_output=True, text=True,
    ).stdout.strip()
    return out or None


files = sorted(
    f for f in (
        glob.glob("*.html", root_dir=root)
        + glob.glob("series/*.html", root_dir=root)
        + glob.glob("essays/*.html", root_dir=root)
    )
    if f != "404.html"
)

entries = []
for f in files:
    loc = url_for(f)
    date = lastmod(f)
    prio = PRIORITY.get(loc, "0.80" if loc.startswith("series/") or "/" not in loc else "0.60")
    freq = CHANGEFREQ.get(loc, "monthly")
    e = [f"    <loc>{BASE}{loc}</loc>"]
    if date:
        e.append(f"    <lastmod>{date}</lastmod>")
    e.append(f"    <changefreq>{freq}</changefreq>")
    e.append(f"    <priority>{prio}</priority>")
    entries.append("  <url>\n" + "\n".join(e) + "\n  </url>")

xml = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "\n".join(entries)
    + "\n</urlset>\n"
)

out = root / "sitemap.xml"
if out.read_text(encoding="utf-8") != xml:
    out.write_text(xml, encoding="utf-8")
    print(f"sitemap.xml regenerated ({len(files)} URLs).")
else:
    print("sitemap.xml unchanged.")
