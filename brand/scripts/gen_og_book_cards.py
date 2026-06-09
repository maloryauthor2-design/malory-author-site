#!/usr/bin/env python3
"""
Malory - OG share cards for book pages (1200x630).

Matches the existing og-*.png card system (dark field, brass rule + kicker,
big title, muted subline, footer bar) and adds the book cover on the right
with a soft shadow. Series anchor colors per BRAND_FOUNDATION.md.

Outputs og-book-<slug>.png to the site root.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
BRAND = os.path.dirname(HERE)
ROOT = os.path.dirname(BRAND)
FONTS = os.path.join(BRAND, "fonts")

W, H = 1200, 630
MIDNIGHT = (13, 16, 21)
DEEP = (10, 13, 18)
BRASS = (201, 168, 90)
CREAM = (232, 224, 204)
WHITE = (240, 240, 244)
MUTED = (154, 160, 168)

ANCHORS = {
    "psyker": (208, 72, 72),     # signal red
    "pts":    (61, 166, 114),    # console green
    "arcane": (61, 127, 184),    # electric blue
    "soar":   (122, 139, 153),   # steel
    "merlin": (91, 58, 122),     # deep violet
    "boys":   (224, 196, 120),   # brass bright
}

def F(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)

BOOKS = [
    # slug, cover, series-key, kicker, title, subline
    ("welcome-to-the-dark-ages", "welcome-cover.jpg", "merlin", "MORGAN & MERLIN · BOOK 1", "Welcome to the\nDark Ages", "Reincarnated into Dark Age Cornwall. Merlin's ghost is “helping.”"),
    ("journey-to-the-dark-tower", "tower-cover.jpg", "merlin", "MORGAN & MERLIN · BOOK 2", "Journey to the\nDark Tower", "The cultivation gets harder. The commentary doesn't improve."),
    ("quest-for-the-dark-blade", "blade-cover.jpg", "merlin", "MORGAN & MERLIN · BOOK 3", "Quest for the\nDark Blade", "Higher realms, sharper enemies, a sword with opinions."),
    ("murder-in-the-temple", "murder-cover.jpg", "soar", "THE SOAR CHRONICLES · BOOK 1", "Murder in\nthe Temple", "No Class. No god. A very punchable face."),
    ("death-of-a-curator", "curator-cover.jpg", "soar", "THE SOAR CHRONICLES · BOOK 2", "Death of\na Curator", "A second body. A different god. Still owed money."),
    ("the-cuckoos-last-call", "cuckoo-cover.jpg", "soar", "THE SOAR CHRONICLES · BOOK 3", "The Cuckoo's\nLast Call", "The third case. Everyone's patience is thinner."),
    ("psyker-marine-1", "psyker-1.jpg", "psyker", "PSYKER MARINE · BOOK 1 · JAKE MALORY", "Psyker Marine\nBook 1", "Thorne wasn't supposed to matter. Then the aliens came."),
    ("psyker-marine-2", "psyker-2.jpg", "psyker", "PSYKER MARINE · BOOK 2 · JAKE MALORY", "Psyker Marine\nBook 2", "The war escalates. The squad takes ground. The cost rises."),
    ("psyker-marine-3", "psyker-3.jpg", "psyker", "PSYKER MARINE · BOOK 3 · JAKE MALORY", "Psyker Marine\nBook 3", "The mid-war turn. More rules. More cracks."),
    ("psyker-marine-4", "psyker-4.jpg", "psyker", "PSYKER MARINE · BOOK 4 · JAKE MALORY", "Psyker Marine\nBook 4", "Larger engagements, hostile politics, a System not to be trusted."),
    ("psyker-marine-5", "psyker-5.jpg", "psyker", "PSYKER MARINE · BOOK 5 · JAKE MALORY", "Psyker Marine\nBook 5", "The war finds its shape. The alliances find their cost."),
    ("psyker-marine-6", "psyker-6.jpg", "psyker", "PSYKER MARINE · BOOK 6 · JAKE MALORY", "Psyker Marine\nBook 6", "The finale. Everything the war has been pointing at."),
    ("chaos-protocols", "arcane-1.jpg", "arcane", "ARCANE GALAXY · BOOK 1 · JAKE MALORY", "Chaos\nProtocols", "An SAS operator, an elf pilot, and a broken ship vs the System."),
    ("swashbuckler", "arcane-2.jpg", "arcane", "ARCANE GALAXY · BOOK 2 · JAKE MALORY", "Swashbuckler", "Further into the System. Further into trouble."),
    ("punish-the-system", "pts-cover.jpg", "pts", "PUNISH THE SYSTEM · BOOK 1", "Punish\nthe System", "Connor Keene died saving the world. The world hates him for it."),
    ("mr-glimms-skull", "boys-1.jpg", "boys", "BOY'S OWN ADVENTURES · BOOK 1", "The Weird Map in\nMr Glimm's Skull", "Part Hardy Boys, part Cold War thriller, a touch of horror."),
    ("terror-from-the-deep", "boys-2.jpg", "boys", "BOY'S OWN ADVENTURES · BOOK 2 · JUNE 2026", "Terror from\nthe Deep", "A war for ancient technology on the ocean floor. Pre-order now."),
    ("punish-the-system-2", "pts-2-cover.jpg", "pts", "PUNISH THE SYSTEM · BOOK 2 · AUG 31, 2026", "Punish the System\nBook 2", "Connor Keene is the ultimate bug remover. Pre-order now."),
]

f_kick = F("Inter-SemiBold-static.ttf", 30)
f_title = F("Fraunces-VF.ttf", 76)
try:
    f_title.set_variation_by_axes([76, 600, 0, 0])  # opsz, wght
except Exception:
    pass
f_sub = F("Inter-Medium-static.ttf", 30)
f_foot = F("Inter-SemiBold-static.ttf", 26)

for slug, cover, key, kicker, title, sub in BOOKS:
    anchor = ANCHORS[key]
    img = Image.new("RGB", (W, H), MIDNIGHT)
    d = ImageDraw.Draw(img)
    # top band + footer band slightly darker
    d.rectangle([0, 0, W, 122], fill=DEEP)
    d.rectangle([0, H - 86, W, H], fill=DEEP)

    # cover on the right, rotated shadow card
    cov = Image.open(os.path.join(ROOT, cover)).convert("RGB")
    ch = 430
    cw = int(cov.width * ch / cov.height)
    cov = cov.resize((cw, ch), Image.LANCZOS)
    cx, cy = W - cw - 84, 122 + (H - 122 - 86 - ch) // 2
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rectangle([cx + 10, cy + 16, cx + cw + 10, cy + ch + 16], fill=(0, 0, 0, 160))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    img.paste(shadow, (0, 0), shadow)
    img.paste(cov, (cx, cy))
    d.rectangle([cx, cy, cx + cw, cy + ch], outline=anchor, width=2)

    text_right = cx - 50

    # brass rule + kicker (top band)
    d.line([(62, 62), (182, 62)], fill=anchor, width=5)
    d.text((62, 80), kicker, font=f_kick, fill=anchor)

    # title
    y = 168
    for line in title.split("\n"):
        d.text((62, y), line, font=f_title, fill=WHITE)
        y += 92

    # subline, wrapped to text zone
    words, lines, cur = sub.split(), [], ""
    for w_ in words:
        test = (cur + " " + w_).strip()
        if d.textlength(test, font=f_sub) > text_right - 62 and cur:
            lines.append(cur); cur = w_
        else:
            cur = test
    lines.append(cur)
    y = max(y + 26, 408)
    for line in lines[:3]:
        d.text((62, y), line, font=f_sub, fill=MUTED)
        y += 42

    # footer
    d.text((62, H - 62), "MALORYAUTHOR.COM", font=f_foot, fill=BRASS)
    right = "2026 JIM BAEN AWARD WINNER"
    d.text((W - 62 - d.textlength(right, font=f_foot), H - 62), right, font=f_foot, fill=MUTED)

    img.save(os.path.join(ROOT, f"og-book-{slug}.png"), optimize=True)
    print("og-book-%s.png" % slug)
