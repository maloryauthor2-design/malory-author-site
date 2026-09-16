#!/usr/bin/env python3
"""Put an Offer on the Book in each book page's JSON-LD.

Prices live in book-prices.json rather than in eighteen separate pages, so
correcting one is a one-line edit and the next workflow run rewrites the lot.
They are Amazon UK prices in GBP: the site is en-GB and the Associates tag is a
European one, so that is the store a search result should quote.

The offer url points at the links.maloryauthor.com slug, not at a fixed Amazon
domain, because that redirect now sends each reader to their own store.

A page whose price is missing from the file is left alone. A wrong price is
worse than no price, so this never guesses.
"""
import json
import pathlib
import re

root = pathlib.Path(__file__).resolve().parents[2]
config = json.loads((root / "book-prices.json").read_text(encoding="utf-8"))
currency = config.get("_currency", "GBP")
BOOKS = config["books"]


def offer_for(entry):
    return {
        "@type": "Offer",
        "price": entry["price"],
        "priceCurrency": currency,
        "availability": "https://schema.org/InStock",
        "url": "https://links.maloryauthor.com/" + entry["slug"],
        "seller": {"@type": "Organization", "name": "Amazon"},
    }


def apply(obj, entry, touched):
    """Add the offer to the first Book that has no offers of its own."""
    if isinstance(obj, list):
        for x in obj:
            apply(x, entry, touched)
        return
    if not isinstance(obj, dict):
        return
    if "@graph" in obj:
        apply(obj["@graph"], entry, touched)
        return
    if obj.get("@type") == "Book":
        want = offer_for(entry)
        if obj.get("offers") != want:
            obj["offers"] = want
            touched.append("offers")
        if entry.get("format") and "bookFormat" not in obj:
            obj["bookFormat"] = "https://schema.org/" + entry["format"]
            touched.append("bookFormat")
    for v in obj.values():
        if isinstance(v, (dict, list)):
            apply(v, entry, touched)


changed, skipped = [], []
for name, entry in sorted(BOOKS.items()):
    path = root / name
    if not path.exists():
        skipped.append(name + " (no such page)")
        continue
    html = path.read_text(encoding="utf-8")
    out, pos, touched = [], 0, []
    for m in re.finditer(r'(<script type="application/ld\+json">)(.*?)(</script>)', html, re.S):
        try:
            data = json.loads(m.group(2))
        except Exception:
            continue
        before = json.dumps(data, sort_keys=True)
        apply(data, entry, touched)
        if json.dumps(data, sort_keys=True) == before:
            continue
        out.append(html[pos:m.start()])
        out.append(m.group(1) + "\n" + json.dumps(data, indent=2, ensure_ascii=False) + "\n    " + m.group(3))
        pos = m.end()
    if pos:
        out.append(html[pos:])
        path.write_text("".join(out), encoding="utf-8")
        changed.append("%s (%s)" % (name, ", ".join(sorted(set(touched)))))

print("book offers written to %d pages" % len(changed))
for c in changed:
    print("   ", c)
for s in skipped:
    print("    skipped:", s)
