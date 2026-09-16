#!/usr/bin/env python3
"""Fill in the 'N books, Kindle Unlimited' lines under the Where-to-Start fans.

The homepage carries one <p class="series-count" data-series="..."> per guide
card. Rather than typing the numbers in and letting them rot after the next
release, count the real book cards in the matching series section of
books.html, which is the page that already has to be right.

'Coming soon' placeholder cards are not books and are not counted, and the
Kindle Unlimited half of the line is only claimed when that series' own KU
badge on books.html claims it.
"""
import pathlib
import re

root = pathlib.Path(__file__).resolve().parents[2]
books = (root / "books.html").read_text(encoding="utf-8")
index_path = root / "index.html"
index = index_path.read_text(encoding="utf-8")

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

changed = 0
missing = []


def line_for(sid):
    if sid not in data:
        missing.append(sid)
        return None
    n, ku = data[sid]
    if n < 1:
        missing.append(sid)
        return None
    singular, plural = NOUN.get(sid, ("book", "books"))
    out = "%d %s" % (n, singular if n == 1 else plural)
    if ku:
        out += " &middot; Kindle Unlimited"
    return out


def replace(m):
    global changed
    sid = m.group(1)
    new = line_for(sid)
    if new is None:
        return m.group(0)
    if m.group(2) != new:
        changed += 1
    return '<p class="series-count" data-series="%s">%s</p>' % (sid, new)


index = re.sub(r'<p class="series-count" data-series="([^"]+)">(.*?)</p>',
               replace, index, flags=re.S)

if missing:
    raise SystemExit("no book data on books.html for: %s" % ", ".join(sorted(set(missing))))

if changed:
    index_path.write_text(index, encoding="utf-8")
    print("series counts updated (%d changed)" % changed)
else:
    print("series counts already current")
