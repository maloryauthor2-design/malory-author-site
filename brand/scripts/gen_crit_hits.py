"""Crit Hits review covers — brand-aligned per Malory BRAND_FOUNDATION.md.

Field-manual register, disciplined-publisher aesthetic. Uses canonical
brand assets (palette, fonts, malory-mark.svg, malory-wordmark.svg).
Generates: Substack 1456x816, X 1200x675, Square 1080x1080.
"""
import os
import io
import math
import numpy as np
import cairosvg
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# --- Paths --------------------------------------------------------------
BRAND_DIR  = "/sessions/awesome-relaxed-brahmagupta/mnt/malory-author-website/brand"
BRAND_FONTS = os.path.join(BRAND_DIR, "fonts")
CANVAS_FONTS = "/sessions/awesome-relaxed-brahmagupta/mnt/.claude/skills/canvas-design/canvas-fonts"
OUT_DIR    = "/sessions/awesome-relaxed-brahmagupta/mnt/outputs"
COVERS_DIR = OUT_DIR

# --- Brand palette (exact, from BRAND_FOUNDATION.md §3) ----------------
MIDNIGHT     = (13, 16, 21)      # #0D1015 primary-deep — canvas
PRIMARY_MID  = (26, 30, 36)      # #1A1E24
SURFACE_2    = (34, 39, 47)      # #22272F
LINE         = (51, 58, 68)      # #333A44
BRASS        = (201, 168, 90)    # #C9A85A — primary accent
BRASS_BRIGHT = (224, 196, 120)   # #E0C478
BRASS_DEEP   = (146, 120, 56)    # #927838
SIGNAL_RED   = (208, 72, 72)     # #D04848 — sparingly
CREAM        = (232, 224, 204)   # #E8E0CC
MUTED        = (154, 160, 168)   # #9AA0A8


def F(path, size):
    return ImageFont.truetype(path, size)


# Convenience font loaders
EXTRA_FONTS = "/sessions/awesome-relaxed-brahmagupta/mnt/outputs/fonts"


def fraunces(size):
    # Variable font, used at the size we set
    return F(os.path.join(BRAND_FONTS, "Fraunces-VF.ttf"), size)


def fraunces_sb(size):
    # Brand SemiBold file is empty in brand/fonts; the VF covers all weights
    return F(os.path.join(BRAND_FONTS, "Fraunces-VF.ttf"), size)


def inter_sb(size):
    return F(os.path.join(EXTRA_FONTS, "Inter-SemiBold.ttf"), size)


def inter_med(size):
    return F(os.path.join(EXTRA_FONTS, "Inter-Medium-static.ttf"), size)


def jbmono(size, bold=False):
    name = "JetBrainsMono-Bold.ttf" if bold else "JetBrainsMono-Regular.ttf"
    return F(os.path.join(CANVAS_FONTS, name), size)


# --- SVG rasterisers ---------------------------------------------------
def render_svg(svg_path, width=None, height=None):
    """Render an SVG to a PIL RGBA Image at the requested pixel size."""
    kwargs = {}
    if width: kwargs["output_width"] = width
    if height: kwargs["output_height"] = height
    png_bytes = cairosvg.svg2png(url=svg_path, **kwargs)
    return Image.open(io.BytesIO(png_bytes)).convert("RGBA")


# --- Background --------------------------------------------------------
def make_ground(w, h):
    """Primary-deep canvas with subtle brass radial upper-right and dark
    vignette lower-left. Per BRAND_FOUNDATION pattern."""
    arr = np.zeros((h, w, 3), dtype=np.float32)
    arr[:] = np.array(MIDNIGHT, dtype=np.float32)

    # Brass radial — upper-right
    y, x = np.mgrid[0:h, 0:w]
    cx_b, cy_b = w * 0.88, h * 0.15
    d_b = np.sqrt((x - cx_b) ** 2 + (y - cy_b) ** 2)
    max_d = np.sqrt(w ** 2 + h ** 2)
    glow = np.clip(1.0 - (d_b / (max_d * 0.55)), 0, 1) ** 2 * 0.22
    for c in range(3):
        arr[:, :, c] += (BRASS_DEEP[c] - MIDNIGHT[c]) * glow

    # Vignette — lower-left corner darker
    cx_v, cy_v = w * 0.1, h * 0.95
    d_v = np.sqrt((x - cx_v) ** 2 + (y - cy_v) ** 2)
    vign = np.clip(1.0 - (d_v / (max_d * 0.55)), 0, 1) ** 2 * 0.35
    for c in range(3):
        arr[:, :, c] -= MIDNIGHT[c] * vign * 0.4  # darken below midnight

    # Subtle film grain
    grain = np.random.normal(0, 3.5, (h, w, 3))
    arr += grain
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)


# --- Drawing utilities -------------------------------------------------
def hairline(draw, x1, y1, x2, y2, color=LINE, width=1):
    draw.line([(x1, y1), (x2, y2)], fill=color, width=width)


def text_w(text, fnt, ls=0):
    if not text:
        return 0
    w = 0
    for ch in text:
        b = fnt.getbbox(ch)
        w += (b[2] - b[0]) + ls
    return w - ls


def draw_tracked(draw, text, x, y, fnt, color, ls=0):
    cx = x
    for ch in text:
        draw.text((cx, y), ch, font=fnt, fill=color)
        b = fnt.getbbox(ch)
        cx += (b[2] - b[0]) + ls
    return cx - ls


# --- Book placement with brass hairline frame --------------------------
def place_book(canvas, cover_img, x, y, w, h):
    cover = cover_img.resize((w, h), Image.LANCZOS)
    # Soft drop shadow
    pad = 80
    sh = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    sd.rectangle([(pad + 6, pad + 14), (pad + w + 6, pad + h + 14)],
                 fill=(0, 0, 0, 170))
    sh = sh.filter(ImageFilter.GaussianBlur(radius=26))
    canvas.paste(sh, (x - pad, y - pad), sh)
    canvas.paste(cover, (x, y))
    d = ImageDraw.Draw(canvas)
    # Thin brass hugging rule
    d.rectangle([(x - 2, y - 2), (x + w + 1, y + h + 1)], outline=BRASS, width=2)
    # Subtle outer line
    d.rectangle([(x - 12, y - 12), (x + w + 11, y + h + 11)], outline=BRASS_DEEP, width=1)


# --- Verdict credential badge (brass, disciplined — NOT pulp red stamp) -
def verdict_badge(canvas, x, y, w, h, label="HARD RECOMMEND", sub="THE VERDICT",
                  code="CH·02·HWFWM·MMXXVI"):
    d = ImageDraw.Draw(canvas)
    # Outer brass border
    d.rectangle([(x, y), (x + w, y + h)], outline=BRASS, width=2)
    # Inner hairline
    d.rectangle([(x + 6, y + 6), (x + w - 6, y + h - 6)], outline=BRASS_DEEP, width=1)

    # Top sub-label "THE VERDICT" in mono small
    sub_f = jbmono(int(h * 0.12), bold=True)
    sw = text_w(sub, sub_f, 3)
    draw_tracked(d, sub, x + (w - sw) // 2, y + int(h * 0.13),
                 sub_f, BRASS_DEEP, ls=3)

    # Main label — dynamically size to fit within badge width with margin
    available = w - 24
    target_size = int(h * 0.40)
    label_f = fraunces(target_size)
    lw = text_w(label, label_f, 1)
    while lw > available and target_size > 14:
        target_size -= 1
        label_f = fraunces(target_size)
        lw = text_w(label, label_f, 1)
    label_y = y + int(h * 0.32)
    draw_tracked(d, label, x + (w - lw) // 2, label_y,
                 label_f, BRASS_BRIGHT, ls=1)

    # Tiny brass divider line under label
    dx1 = x + w // 4
    dx2 = x + w - w // 4
    line_y = y + h - int(h * 0.22)
    hairline(d, dx1, line_y, dx2, line_y, BRASS_DEEP, 1)

    # Bottom code line — also auto-fit
    code_size = max(8, int(h * 0.11))
    code_f = jbmono(code_size, bold=False)
    cw = text_w(code, code_f, 2)
    while cw > available and code_size > 7:
        code_size -= 1
        code_f = jbmono(code_size, bold=False)
        cw = text_w(code, code_f, 2)
    draw_tracked(d, code, x + (w - cw) // 2, y + h - int(h * 0.18),
                 code_f, MUTED, ls=2)


# --- Pull quote rendering ----------------------------------------------
def draw_pull_quote(draw, text, x, y, max_w, fnt, color):
    """Wrap and draw a pull quote as italic Fraunces. Returns final y."""
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        if text_w(test, fnt) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    line_h = int(fnt.size * 1.22)
    for i, line in enumerate(lines):
        draw.text((x, y + i * line_h), line, font=fnt, fill=color)
    return y + len(lines) * line_h


# --- Malory mark and wordmark helpers ----------------------------------
def malory_mark(target_w):
    return render_svg(os.path.join(BRAND_DIR, "malory-mark.svg"),
                      width=target_w, height=target_w)


def malory_wordmark(target_w):
    # SVG viewBox is 800x280 so aspect 800/280
    h = int(target_w * 280 / 800)
    return render_svg(os.path.join(BRAND_DIR, "malory-wordmark.svg"),
                      width=target_w, height=h)


def draw_malory_lockup(canvas, x, y, name_size=44, with_kicker=True, color=CREAM):
    """Draw the Malory wordmark inline using Fraunces + brass rule + kicker.
    More legible at masthead sizes than rendering the SVG small.
    Returns (final_width, final_height)."""
    d = ImageDraw.Draw(canvas)
    name_f = fraunces(name_size)
    name = "Malory"
    name_w = text_w(name, name_f)
    d.text((x, y), name, font=name_f, fill=color)
    # Brass rule beneath, 60% of name width, centred on the name
    rule_y = y + int(name_size * 0.92) + 2
    rw = int(name_w * 0.6)
    rx = x + (name_w - rw) // 2
    d.line([(rx, rule_y), (rx + rw, rule_y)],
           fill=BRASS, width=max(1, int(name_size / 28)))
    if with_kicker:
        kick_size = max(8, int(name_size * 0.16))
        kick_f = inter_med(kick_size)
        kick = "SCI-FI  ·  LITRPG  ·  PROGRESSION"
        ls = max(2, int(name_size * 0.06))
        kw = text_w(kick, kick_f, ls)
        kx = x + (name_w - kw) // 2
        draw_tracked(d, kick, kx, rule_y + int(name_size * 0.22),
                     kick_f, MUTED, ls=ls)
        return name_w, rule_y + int(name_size * 0.22) + kick_size - y
    return name_w, rule_y + 4 - y


# ========================================================================
# ISSUE CONFIG
# ========================================================================
ISSUES = {
    "hwfwm": {
        "number": "02",
        "code": "CH·02·HWFWM·MMXXVI",
        "title_lines": ("He Who Fights", "with Monsters"),
        "title_full": "He Who Fights with Monsters",
        "subtitle": "Book One",
        "author": "Shirtaloon  ·  Travis Deverell",
        "publisher_line": "AETHON / PODIUM  ·  2021",
        "pull": "By every measure the world is using, he's monster-shaped. The book's case is that he isn't one.",
        "cover_file": "cover.jpeg",   # extracted from epub earlier
    },
    "ph": {
        "number": "01",
        "code": "CH·01·PH·MMXXVI",
        "title_lines": ("The Primal", "Hunter"),
        "title_full": "The Primal Hunter",
        "subtitle": "Book One",
        "author": "Zogarth",
        "publisher_line": "AETHON BOOKS  ·  2022",
        "pull": "A quiet book about a man having a genuinely nice time.",
        "cover_file": "ph-cover.jpeg",  # awaiting Malory upload
    },
}


# ========================================================================
# SUBSTACK HEADER  (1456 x 816)
# ========================================================================
def make_substack(issue):
    W, H = 1456, 816
    canvas = make_ground(W, H)
    d = ImageDraw.Draw(canvas)
    M = 56

    # === Top masthead bar =================================================
    draw_malory_lockup(canvas, M, M - 8, name_size=46, with_kicker=True, color=CREAM)
    # Masthead hairline pushed down to give the kicker proper breathing room
    masthead_rule_y = M + 100
    hairline(d, M, masthead_rule_y, W - M, masthead_rule_y, BRASS_DEEP, 1)
    # Centred masthead line — date now integrated, no right-aligned text to clash with monogram
    mast_f = inter_sb(13)
    centre_text = ("CRIT HITS   ·   THE REVIEW COLUMN   ·   ISSUE Nº "
                   + issue["number"] + "   ·   MAY 2026")
    cw = text_w(centre_text, mast_f, 3)
    draw_tracked(d, centre_text, (W - cw) // 2, M + 42, mast_f, BRASS, ls=3)

    # === Footer (computed early so layout knows the bound) ===============
    foot_y = H - M - 32
    hairline(d, M, foot_y, W - M, foot_y, BRASS_DEEP, 1)
    foot_f = jbmono(11, bold=True)
    foot_text = "MALORY  ·  CRIT HITS  ·  " + issue["code"] + "  ·  MALORYAUTHOR.SUBSTACK.COM"
    draw_tracked(d, foot_text, M, foot_y + 11, foot_f, MUTED, ls=3)

    # Main content area pushed down to match new masthead, with badge clearance from footer
    main_top = masthead_rule_y + 18
    main_bot = foot_y - 36

    # === Book hero (left) ================================================
    cover = Image.open(os.path.join(COVERS_DIR, issue["cover_file"])).convert("RGB")
    book_h = main_bot - main_top - 12
    book_w = int(book_h * (cover.width / cover.height))
    book_x = M + 36
    book_y = main_top + 6
    place_book(canvas, cover, book_x, book_y, book_w, book_h)

    # === Verdict badge anchored bottom-right of main area ================
    badge_w = 320
    badge_h = 110
    badge_x = W - M - badge_w
    badge_y = main_bot - badge_h
    verdict_badge(canvas, badge_x, badge_y, badge_w, badge_h,
                  label="HARD RECOMMEND", sub="THE VERDICT",
                  code=issue["code"])

    # === Monogram seal top-right corner — sits cleanly, no date to clash with ===
    mono = malory_mark(64)
    canvas.paste(mono, (W - M - 64, M + 8), mono)

    # === Right column ====================================================
    rx = book_x + book_w + 80
    column_w = (W - M) - rx
    below_badge_left_limit = badge_x - 32

    # Eyebrow + brass mark
    eyebrow_f = jbmono(14, bold=True)
    draw_tracked(d, "REVIEW  ·  Nº " + issue["number"], rx, main_top + 4,
                 eyebrow_f, BRASS, ls=4)
    hairline(d, rx, main_top + 32, rx + 70, main_top + 32, BRASS, 2)

    # CRIT HITS — single line, auto-sized to fill the full right column
    crit_text = "CRIT HITS"
    target = 240
    crit_f = fraunces(target)
    while text_w(crit_text, crit_f) > column_w and target > 80:
        target -= 4
        crit_f = fraunces(target)
    # Grow if there's headroom (until we're 96% of column width)
    while text_w(crit_text, crit_f) < column_w * 0.96 and target < 280:
        target += 2
        crit_f = fraunces(target)
        if text_w(crit_text, crit_f) > column_w:
            target -= 2
            crit_f = fraunces(target)
            break
    crit_y = main_top + 56
    d.text((rx, crit_y), crit_text, font=crit_f, fill=CREAM)
    # Actual rendered glyph bottom via PIL metrics (much more reliable than estimate)
    bbox = d.textbbox((rx, crit_y), crit_text, font=crit_f)
    crit_bottom = bbox[3]

    # Tagline below the wordmark, with clear breathing room
    tag_f = inter_med(21)
    tag_y = crit_bottom + 22
    d.text((rx, tag_y), "LitRPG  ·  reviewed from inside the game.",
           font=tag_f, fill=MUTED)

    # Hairline rule
    rule_y = tag_y + 36
    hairline(d, rx, rule_y, rx + 260, rule_y, BRASS, 1)
    hairline(d, rx, rule_y + 4, rx + 100, rule_y + 4, BRASS_DEEP, 1)

    # Pull quote — larger now, full column width, wraps cleanly
    pull_f = F(os.path.join(CANVAS_FONTS, "CrimsonPro-Italic.ttf"), 30)
    pull_y = rule_y + 22
    pull_max_w = below_badge_left_limit - rx
    final_y = draw_pull_quote(d, "“" + issue["pull"] + "”",
                              rx, pull_y, pull_max_w, pull_f, CREAM)

    # Bottom row: byline + meta left, verdict badge right (already drawn)
    by_f = inter_sb(14)
    meta_f = jbmono(13)
    # Anchor byline to the badge's vertical centre area
    bot_block_y = badge_y + 10
    draw_tracked(d, "BY " + issue["author"].upper(),
                 rx, bot_block_y, by_f, BRASS_BRIGHT, ls=3)
    draw_tracked(d, issue["publisher_line"],
                 rx, bot_block_y + 28, meta_f, MUTED, ls=3)

    return canvas


# ========================================================================
# X / SOCIAL CARD  (1200 x 675)
# ========================================================================
def make_x_card(issue):
    W, H = 1200, 675
    canvas = make_ground(W, H)
    d = ImageDraw.Draw(canvas)
    M = 44

    # Top masthead
    draw_malory_lockup(canvas, M, M - 6, name_size=38, with_kicker=True, color=CREAM)
    masthead_rule_y = M + 82
    hairline(d, M, masthead_rule_y, W - M, masthead_rule_y, BRASS_DEEP, 1)
    mast_f = inter_sb(11)
    centre_text = "CRIT HITS   ·   ISSUE Nº " + issue["number"] + "   ·   MAY 2026"
    cw = text_w(centre_text, mast_f, 3)
    draw_tracked(d, centre_text, (W - cw) // 2, M + 34, mast_f, BRASS, ls=3)

    # Footer first
    foot_y = H - M - 24
    hairline(d, M, foot_y, W - M, foot_y, BRASS_DEEP, 1)
    foot_f = jbmono(10, bold=True)
    foot_text = "MALORY  ·  CRIT HITS  ·  " + issue["code"] + "  ·  MALORYAUTHOR.SUBSTACK.COM"
    draw_tracked(d, foot_text, M, foot_y + 8, foot_f, MUTED, ls=3)

    main_top = masthead_rule_y + 14
    main_bot = foot_y - 28

    # Book hero
    cover = Image.open(os.path.join(COVERS_DIR, issue["cover_file"])).convert("RGB")
    book_h = main_bot - main_top - 8
    book_w = int(book_h * (cover.width / cover.height))
    book_x = M + 28
    book_y = main_top + 4
    place_book(canvas, cover, book_x, book_y, book_w, book_h)

    # Verdict badge bottom-right anchor
    badge_w = 280
    badge_h = 100
    badge_x = W - M - badge_w
    badge_y = main_bot - badge_h
    verdict_badge(canvas, badge_x, badge_y, badge_w, badge_h,
                  label="HARD RECOMMEND", sub="THE VERDICT",
                  code=issue["code"])

    # Monogram top-right — clean space, date moved to centre line
    mono = malory_mark(54)
    canvas.paste(mono, (W - M - 54, M + 6), mono)

    # Right column
    rx = book_x + book_w + 64
    column_w = (W - M) - rx
    below_badge_left_limit = badge_x - 24

    eyebrow_f = jbmono(12, bold=True)
    draw_tracked(d, "REVIEW  ·  Nº " + issue["number"], rx, main_top + 2,
                 eyebrow_f, BRASS, ls=4)
    hairline(d, rx, main_top + 28, rx + 60, main_top + 28, BRASS, 2)

    # CRIT HITS auto-fit to column width
    crit_text = "CRIT HITS"
    target = 200
    crit_f = fraunces(target)
    while text_w(crit_text, crit_f) > column_w and target > 70:
        target -= 4
        crit_f = fraunces(target)
    while text_w(crit_text, crit_f) < column_w * 0.96 and target < 240:
        target += 2
        crit_f = fraunces(target)
        if text_w(crit_text, crit_f) > column_w:
            target -= 2
            crit_f = fraunces(target)
            break
    crit_y = main_top + 44
    d.text((rx, crit_y), crit_text, font=crit_f, fill=CREAM)
    bbox = d.textbbox((rx, crit_y), crit_text, font=crit_f)
    crit_bottom = bbox[3]

    tag_f = inter_med(17)
    tag_y = crit_bottom + 18
    d.text((rx, tag_y), "LitRPG  ·  reviewed from inside the game.",
           font=tag_f, fill=MUTED)
    rule_y = tag_y + 28
    hairline(d, rx, rule_y, rx + 220, rule_y, BRASS, 1)
    hairline(d, rx, rule_y + 4, rx + 84, rule_y + 4, BRASS_DEEP, 1)

    pull_f = F(os.path.join(CANVAS_FONTS, "CrimsonPro-Italic.ttf"), 24)
    pull_y = rule_y + 18
    pull_max_w = below_badge_left_limit - rx
    final_y = draw_pull_quote(d, "“" + issue["pull"] + "”",
                              rx, pull_y, pull_max_w, pull_f, CREAM)
    by_f = inter_sb(13)
    bot_block_y = badge_y + 8
    draw_tracked(d, "BY " + issue["author"].upper(),
                 rx, bot_block_y, by_f, BRASS_BRIGHT, ls=3)
    meta_f = jbmono(12)
    draw_tracked(d, issue["publisher_line"],
                 rx, bot_block_y + 24, meta_f, MUTED, ls=3)

    return canvas


# ========================================================================
# X ARTICLE COVER  (1500 x 600)  — 2.5:1 aspect, matches X Article crop
# The X Article editor's crop box is roughly 2.5:1 (narrower than the
# 3:1 banner standard). This aspect fits the crop without clipping the
# wordmark on the left or HITS on the right.
# ========================================================================
def make_x_article(issue):
    W, H = 1500, 600
    canvas = make_ground(W, H)
    d = ImageDraw.Draw(canvas)
    M = 28

    # Top masthead: Malory wordmark (with kicker) left, masthead text right
    draw_malory_lockup(canvas, M, M - 6, name_size=34, with_kicker=True, color=CREAM)
    mast_f = inter_sb(12)
    centre_text = "CRIT HITS  ·  ISSUE Nº " + issue["number"] + "  ·  MAY 2026"
    cw = text_w(centre_text, mast_f, 3)
    draw_tracked(d, centre_text, W - M - 60 - cw - 20, M + 12,
                 mast_f, BRASS, ls=3)
    mono = malory_mark(52)
    canvas.paste(mono, (W - M - 52, M - 4), mono)

    # Hairline rules
    top_rule_y = M + 72
    hairline(d, M, top_rule_y, W - M, top_rule_y, BRASS_DEEP, 1)
    foot_y = H - M - 4
    foot_rule_y = foot_y - 20
    hairline(d, M, foot_rule_y, W - M, foot_rule_y, BRASS_DEEP, 1)
    foot_f = jbmono(10, bold=True)
    foot_text = "MALORY  ·  CRIT HITS  ·  " + issue["code"] + "  ·  MALORYAUTHOR.SUBSTACK.COM"
    draw_tracked(d, foot_text, M, foot_y - 14, foot_f, MUTED, ls=3)

    main_top = top_rule_y + 16
    main_bot = foot_rule_y - 18

    # Book cover left, full main height
    cover = Image.open(os.path.join(COVERS_DIR, issue["cover_file"])).convert("RGB")
    book_h = main_bot - main_top
    book_w = int(book_h * (cover.width / cover.height))
    book_x = M + 18
    book_y = main_top
    place_book(canvas, cover, book_x, book_y, book_w, book_h)

    # Verdict badge anchored bottom-right of main area
    badge_w = 300
    badge_h = 104
    badge_x = W - M - badge_w
    badge_y = main_bot - badge_h
    verdict_badge(canvas, badge_x, badge_y, badge_w, badge_h,
                  label="HARD RECOMMEND", sub="THE VERDICT",
                  code=issue["code"])

    # Right column
    rx = book_x + book_w + 60
    column_w = (W - M) - rx
    below_badge_left_limit = badge_x - 28

    eyebrow_f = jbmono(13, bold=True)
    draw_tracked(d, "REVIEW  ·  Nº " + issue["number"], rx, main_top + 4,
                 eyebrow_f, BRASS, ls=4)
    hairline(d, rx, main_top + 28, rx + 60, main_top + 28, BRASS, 2)

    # CRIT HITS — single line, auto-fit
    crit_text = "CRIT HITS"
    target = 160
    crit_f = fraunces(target)
    while text_w(crit_text, crit_f) > column_w and target > 80:
        target -= 4
        crit_f = fraunces(target)
    while text_w(crit_text, crit_f) < column_w * 0.96 and target < 200:
        target += 2
        crit_f = fraunces(target)
        if text_w(crit_text, crit_f) > column_w:
            target -= 2
            crit_f = fraunces(target)
            break
    crit_y = main_top + 42
    d.text((rx, crit_y), crit_text, font=crit_f, fill=CREAM)
    bbox = d.textbbox((rx, crit_y), crit_text, font=crit_f)
    crit_bottom = bbox[3]

    tag_f = inter_med(17)
    tag_y = crit_bottom + 14
    d.text((rx, tag_y), "LitRPG  ·  reviewed from inside the game.",
           font=tag_f, fill=MUTED)
    rule_y = tag_y + 28
    hairline(d, rx, rule_y, rx + 220, rule_y, BRASS, 1)
    hairline(d, rx, rule_y + 4, rx + 84, rule_y + 4, BRASS_DEEP, 1)

    pull_f = F(os.path.join(CANVAS_FONTS, "CrimsonPro-Italic.ttf"), 24)
    pull_y = rule_y + 16
    pull_max_w = below_badge_left_limit - rx
    final_y = draw_pull_quote(d, "“" + issue["pull"] + "”",
                              rx, pull_y, pull_max_w, pull_f, CREAM)
    by_f = inter_sb(13)
    bot_block_y = badge_y + 8
    draw_tracked(d, "BY " + issue["author"].upper(),
                 rx, bot_block_y, by_f, BRASS_BRIGHT, ls=3)
    meta_f = jbmono(12)
    draw_tracked(d, issue["publisher_line"],
                 rx, bot_block_y + 24, meta_f, MUTED, ls=3)

    return canvas


# ========================================================================
# SQUARE  (1080 x 1080)  — stacked composition
# ========================================================================
def make_square(issue):
    W, H = 1080, 1080
    canvas = make_ground(W, H)
    d = ImageDraw.Draw(canvas)
    M = 56

    # Top masthead — centred Malory lockup
    name_f = fraunces(54)
    name_w = text_w("Malory", name_f)
    lockup_x = (W - name_w) // 2
    draw_malory_lockup(canvas, lockup_x, M - 6, name_size=54, with_kicker=True, color=CREAM)
    mast_f = inter_sb(12)
    centre_text = "CRIT HITS  ·  THE REVIEW COLUMN  ·  ISSUE Nº " + issue["number"] + "  ·  MAY 2026"
    cw = text_w(centre_text, mast_f, 3)
    draw_tracked(d, centre_text, (W - cw) // 2, M + 96, mast_f, BRASS, ls=3)
    # Mini hairline under it
    sub_rule_y = M + 124
    hairline(d, M + 80, sub_rule_y, W - M - 80, sub_rule_y, BRASS_DEEP, 1)

    # === Hero: large CRIT HITS column display ============================
    # Auto-fit to canvas width with safe margins
    available = W - 2 * (M + 60)
    target = 220
    crit_f = fraunces(target)
    space_w_approx = int(target * 0.14)
    while text_w("CRIT", crit_f) + space_w_approx + text_w("HITS", crit_f) > available and target > 80:
        target -= 4
        crit_f = fraunces(target)
        space_w_approx = int(target * 0.14)
    crit_y = sub_rule_y + 18
    crit_w = text_w("CRIT", crit_f, 0)
    hits_w = text_w("HITS", crit_f, 0)
    space = space_w_approx
    total_w = crit_w + space + hits_w
    sx = (W - total_w) // 2
    d.text((sx, crit_y), "CRIT", font=crit_f, fill=CREAM)
    d.text((sx + crit_w + space, crit_y), "HITS", font=crit_f, fill=CREAM)
    # True glyph bottom via bbox for safe tagline placement
    bbox = d.textbbox((sx, crit_y), "CRIT HITS", font=crit_f)
    crit_bottom = bbox[3]

    # Tagline below
    tag_f = inter_med(22)
    tag_text = "LitRPG  ·  reviewed from inside the game."
    tw = text_w(tag_text, tag_f, 0)
    d.text(((W - tw) // 2, crit_bottom + 22), tag_text, font=tag_f, fill=MUTED)

    # Decorative central rule with brass dot ornament — positioned via tagline metrics
    tag_bbox = d.textbbox(((W - tw) // 2, crit_bottom + 22), tag_text, font=tag_f)
    rule_y = tag_bbox[3] + 32
    hairline(d, M + 80, rule_y, W // 2 - 60, rule_y, BRASS, 1)
    hairline(d, W // 2 + 60, rule_y, W - M - 80, rule_y, BRASS, 1)
    cx_dot = W // 2
    for off in [-22, 0, 22]:
        r = 3 if off == 0 else 2
        d.ellipse([(cx_dot + off - r, rule_y - r), (cx_dot + off + r, rule_y + r)],
                  fill=BRASS)

    # === Book cover + pull quote panel below =============================
    cover = Image.open(os.path.join(COVERS_DIR, issue["cover_file"])).convert("RGB")
    book_h = 470
    book_w = int(book_h * (cover.width / cover.height))
    book_x = M + 30
    book_y = rule_y + 36
    place_book(canvas, cover, book_x, book_y, book_w, book_h)

    # Right of book — text column
    rx = book_x + book_w + 56
    rw = W - M - rx - 6

    eyebrow_f = jbmono(13, bold=True)
    draw_tracked(d, "REVIEW  ·  Nº " + issue["number"], rx, book_y + 4,
                 eyebrow_f, BRASS, ls=4)
    hairline(d, rx, book_y + 28, rx + 60, book_y + 28, BRASS, 2)

    # Pull quote first — the load-bearing line, larger
    pull_f = F(os.path.join(CANVAS_FONTS, "CrimsonPro-Italic.ttf"), 26)
    pull_y = book_y + 50
    final_y = draw_pull_quote(d, "“" + issue["pull"] + "”",
                              rx, pull_y, rw, pull_f, CREAM)

    # Hairline divider
    div_y = final_y + 16
    hairline(d, rx, div_y, rx + 160, div_y, BRASS, 1)

    # Byline + metadata block in mono
    by_f = inter_sb(13)
    by_y = div_y + 18
    draw_tracked(d, "BY " + issue["author"].upper(),
                 rx, by_y, by_f, BRASS_BRIGHT, ls=3)
    meta_f = jbmono(12)
    draw_tracked(d, issue["publisher_line"],
                 rx, by_y + 26, meta_f, MUTED, ls=3)

    # Verdict badge anchored at the bottom of the text column
    badge_w = min(rw, 320)
    badge_h = 100
    badge_x = rx
    badge_y = book_y + book_h - badge_h
    verdict_badge(canvas, badge_x, badge_y, badge_w, badge_h,
                  label="HARD RECOMMEND", sub="THE VERDICT",
                  code=issue["code"])

    # Footer
    foot_y = H - M - 28
    hairline(d, M, foot_y, W - M, foot_y, BRASS_DEEP, 1)
    foot_f = jbmono(10, bold=True)
    foot_text = "MALORY  ·  " + issue["code"] + "  ·  MALORYAUTHOR.SUBSTACK.COM"
    fw = text_w(foot_text, foot_f, 3)
    draw_tracked(d, foot_text, (W - fw) // 2, foot_y + 10, foot_f, MUTED, ls=3)

    return canvas


# ========================================================================
# main
# ========================================================================
def render_issue(slug, only=None):
    issue = ISSUES[slug]
    cover_path = os.path.join(COVERS_DIR, issue["cover_file"])
    if not os.path.exists(cover_path):
        print(f"SKIP {slug}: cover file not found at {cover_path}")
        return

    targets = {
        "substack":  (make_substack,  "substack-1456x816"),
        "x":         (make_x_card,    "x-1200x675"),
        "x-article": (make_x_article, "x-article-1500x600"),
        "square":    (make_square,    "square-1080x1080"),
    }
    if only:
        targets = {k: v for k, v in targets.items() if k in only}

    for fmt, (fn, dim_label) in targets.items():
        np.random.seed(11)  # deterministic background grain per format
        img = fn(issue)
        out = os.path.join(OUT_DIR, f"crit-hits-{issue['number']}-{slug}-{dim_label}.png")
        img.save(out, "PNG", optimize=True)
        print(f"  saved {os.path.basename(out)}")


if __name__ == "__main__":
    print("HWFWM (Nº 02):")
    render_issue("hwfwm")
    print()
    print("Primal Hunter (Nº 01):")
    render_issue("ph")
