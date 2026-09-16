#!/usr/bin/env python3
"""Keep Article dates and hasPart Book authors honest in the JSON-LD.

Two things Google asks for that the pages were missing:

  * datePublished on the reader-guide Articles. Taken from the file's first
    commit rather than invented, and dateModified from its last, so the dates
    are true and stay true. Needs full history (the workflow checks out with
    fetch-depth: 0); if history is shallow the page is left alone rather than
    given a made-up date.
  * author on each Book inside a BookSeries hasPart list. The series pages named
    the series author but not the author of the individual books.
"""
import glob
import json
import pathlib
import re
import subprocess

root = pathlib.Path(__file__).resolve().parents[2]


def git_date(path, first):
    args = ["git", "log", "--format=%cs"] + (["--diff-filter=A"] if first else ["-1"]) + ["--", path]
    out = subprocess.run(args, cwd=root, capture_output=True, text=True).stdout.strip().splitlines()
    return (out[-1] if first else out[0]) if out else None


def collect_author(obj, found):
    """The hasPart Books sit on the CollectionPage, while the author is declared on
    the BookSeries beside it, so the author has to be found before the walk rather
    than carried down the tree."""
    if isinstance(obj, list):
        for x in obj:
            collect_author(x, found)
    elif isinstance(obj, dict):
        if obj.get("@type") in ("BookSeries", "Book", "Article") and obj.get("author"):
            found.append(obj["author"])
        for v in obj.values():
            if isinstance(v, (dict, list)):
                collect_author(v, found)


def fix(obj, author, dates, touched):
    if isinstance(obj, list):
        for x in obj:
            fix(x, author, dates, touched)
        return
    if not isinstance(obj, dict):
        return
    if "@graph" in obj:
        fix(obj["@graph"], author, dates, touched)
        return

    t = obj.get("@type")
    if t == "Article" and "datePublished" not in obj and dates[0]:
        obj["datePublished"] = dates[0]
        obj.setdefault("dateModified", dates[1] or dates[0])
        touched.append("datePublished")
    if t == "Book" and "author" not in obj and author:
        obj["author"] = author
        touched.append("Book author")
    for v in obj.values():
        if isinstance(v, (dict, list)):
            fix(v, author, dates, touched)


pages = sorted(glob.glob("*.html", root_dir=root) + glob.glob("series/*.html", root_dir=root))
changed = []
for name in pages:
    path = root / name
    s = path.read_text(encoding="utf-8")
    if "application/ld+json" not in s:
        continue
    dates = (git_date(name, True), git_date(name, False))
    out, pos, touched = [], 0, []
    for m in re.finditer(r'(<script type="application/ld\+json">)(.*?)(</script>)', s, re.S):
        try:
            data = json.loads(m.group(2))
        except Exception:
            continue
        before = json.dumps(data, sort_keys=True)
        found = []
        collect_author(data, found)
        fix(data, found[0] if found else None, dates, touched)
        if json.dumps(data, sort_keys=True) == before:
            continue
        out.append(s[pos:m.start()])
        out.append(m.group(1) + "\n" + json.dumps(data, indent=2, ensure_ascii=False) + "\n    " + m.group(3))
        pos = m.end()
    if pos:
        out.append(s[pos:])
        path.write_text("".join(out), encoding="utf-8")
        changed.append("%s (%s)" % (name, ", ".join(sorted(set(touched)))))

print("schema updated on %d pages" % len(changed))
for c in changed:
    print("   ", c)
