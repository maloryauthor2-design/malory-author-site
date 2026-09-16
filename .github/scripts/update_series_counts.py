#!/usr/bin/env python3
"""Fill in the 'N books, Kindle Unlimited' lines under the Where-to-Start fans.

Every page carrying a Where-to-Start grid has one
<p class="series-count" data-series="..."> per guide card. Rather than typing the
numbers in and letting them rot after the next release, count the real book cards
in the matching series section of books.html, which is the page that already has
to be right.

This walks EVERY html file that contains a series-count, not just the homepage:
the same grid lives on index.html and start-here.html, and the two drifting apart
is exactly the bug this is here to prevent.

'Coming soon' placeholder cards are not books and are not counted, and the Kindle
Unlimited half of the line is only claimed when that series' own KU badge on
books.html claims it.
"""
import glob
import pathlib
import re

root = pathlib.Path(__file__).resolve().parents[2]
books = (root / "books.html").read_text(encoding="utf-8")

# anthologies are counted, but they are not "books 1..n of a series"
NOUN = {"raconteur": ("anthology", "anthologies")}


def sections(html):
    marks = [(m.start(), m.group(1)) for m in
             re.finditer(r'<section class="series-group[^"]*" id="([^"]+)"', html)]
    for i, (start, sid) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(html)
        yield sid, html[start:end]


def summarise(seg):
    cards = seg.count('class="series-book-card"')
    placeholders = seg.count("placeholder-cover")
    badge = re.search(r'class="ku-badge"[^>]*>(.*?)</p>', seg, re.S)
    text = re.sub("<[^>]+>", "", badge.group(1)) if badge else ""
    return cards - placeholders, "kindle unlimited" in text.lower()


data = {sid: summarise(seg) for sid, seg in sections(books)}
missing = set()


def line_for(sid):
    if sid not in data or data[sid][0] < 1:
        missing.add(sid)
        return None
    n, ku = data[sid]
    singular, plural = NOUN.get(sid, ("book", "books"))
    out = "%d %s" % (n, singular if n == 1 else plural)
    if ku:
        out += " &middot; Kindle Unlimited"
    return out


pages = sorted(p for p in glob.glob("*.html", root_dir=root)
               if 'class="series-count"' in (root / p).read_text(encoding="utf-8"))
if not pages:
    raise SystemExit("no page carries a series-count line - has the markup changed?")

touched = []
for name in pages:
    path = root / name
    html = path.read_text(encoding="utf-8")
    changed = [0]

    def replace(m):
        new = line_for(m.group(1))
        if new is None:
            return m.group(0)
        if m.group(2) != new:
            changed[0] += 1
        return '<p class="series-count" data-series="%s">%s</p>' % (m.group(1), new)

    out = re.sub(r'<p class="series-count" data-series="([^"]+)">(.*?)</p>',
                 replace, html, flags=re.S)
    if changed[0]:
        path.write_text(out, encoding="utf-8")
        touched.append("%s (%d)" % (name, changed[0]))

if missing:
    raise SystemExit("no book data on books.html for: %s" % ", ".join(sorted(missing)))

print("series counts updated: " + ", ".join(touched) if touched
      else "series counts already current on: " + ", ".join(pages))
