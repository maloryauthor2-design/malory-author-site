"""Generate every 1080x1920 PNG card needed for the PH Shorts video.

Brand-strict: Fraunces (display), JetBrains Mono (system blocks),
Inter (UI / captions). Palette per BRAND_FOUNDATION.md §3. Saves to
the vault `_video/cards-01-ph/` and the workspace Reviews folder.

Drop each PNG onto its beat in CapCut. Apply Fade In, Typewriter,
or Slide Up animation as preferred. The 9:16 cover (book reveal)
is already in `_assets/` and is the 6th beat.
"""
import os
import io
import numpy as np
import cairosvg
from PIL import Image, ImageDraw, ImageFont

# --- Paths -------------------------------------------------------------
BRAND_DIR    = "/sessions/blissful-practical-hopper/mnt/malory-author-website/brand"
BRAND_FONTS  = os.path.join(BRAND_DIR, "fonts")
CANVAS_FONTS = "/sessions/blissful-practical-hopper/mnt/.claude/skills/canvas-design/canvas-fonts"
VAULT_OUT    = "/sessions/blissful-practical-hopper/mnt/PhD/08_Reviews/_video/cards-01-ph"
WS_OUT       = "/sessions/blissful-practical-hopper/mnt/Reviews/cards-01-ph"

os.makedirs(VAULT_OUT, exist_ok=True)
os.makedirs(WS_OUT, exist_ok=True)

# --- Palette -----------------------------------------------------------
MIDNIGHT     = (13, 16, 21)
SURFACE_2    = (34, 39, 47)
BRASS        = (201, 168, 90)
BRASS_BRIGHT = (224, 196, 120)
BRASS_DEEP   = (146, 120, 56)
SIGNAL_RED   = (208, 72, 72)
CREAM        = (232, 224, 204)
MUTED        = (154, 160, 168)


def F(path, size):
    return ImageFont.truetype(path, size)


def fraunces(size):
    return F(os.path.join(BRAND_FONTS, "Fraunces-VF.ttf"), size)


def inter_med(size):
    return F(os.path.join(BRAND_FONTS, "Inter-Medium-static.ttf"), size)


def jbmono(size, bold=False):
    name = "JetBrainsMono-Bold.ttf" if bold else "JetBrainsMono-Regular.ttf"
    return F(os.path.join(CANVAS_FONTS, name), size)


def crimson_italic(size):
    return F(os.path.join(CANVAS_FONTS, "CrimsonPro-Italic.ttf"), size)


# --- Background --------------------------------------------------------
def make_ground(w, h, seed=11):
    arr = np.zeros((h, w, 3), dtype=np.float32)
    arr[:] = np.array(MIDNIGHT, dtype=np.float32)
    y, x = np.mgrid[0:h, 0:w]
    cx_b, cy_b = w * 0.5, h * 0.08
    d_b = np.sqrt((x - cx_b) ** 2 + (y - cy_b) ** 2)
    max_d = np.sqrt(w ** 2 + h ** 2)
    glow = np.clip(1.0 - (d_b / (max_d * 0.45)), 0, 1) ** 2 * 0.16
    for c in range(3):
        arr[:, :, c] += (BRASS_DEEP[c] - MIDNIGHT[c]) * glow
    cx_v, cy_v = w * 0.1, h * 0.95
    d_v = np.sqrt((x - cx_v) ** 2 + (y - cy_v) ** 2)
    vign = np.clip(1.0 - (d_v / (max_d * 0.55)), 0, 1) ** 2 * 0.30
    for c in range(3):
        arr[:, :, c] -= MIDNIGHT[c] * vign * 0.4
    np.random.seed(seed)
    grain = np.random.normal(0, 3.0, (h, w, 3))
    arr += grain
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)


# --- Utilities ---------------------------------------------------------
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


def center_x(text, fnt, w, ls=0):
    return (w - text_w(text, fnt, ls)) // 2


def hairline(d, x1, y1, x2, y2, color=BRASS_DEEP, width=1):
    d.line([(x1, y1), (x2, y2)], fill=color, width=width)


def render_svg(svg_path, width=None, height=None):
    kwargs = {}
    if width:
        kwargs["output_width"] = width
    if height:
        kwargs["output_height"] = height
    png_bytes = cairosvg.svg2png(url=svg_path, **kwargs)
    return Image.open(io.BytesIO(png_bytes)).convert("RGBA")


# --- Brand-bookend overlays (used on cold-open and end-card only) ------
def draw_top_brass(d, w, h):
    M = 48
    hairline(d, M, 28, w - M, 28, BRASS, 2)
    hairline(d, M, 36, w // 2 - 30, 36, BRASS_DEEP, 1)
    hairline(d, w // 2 + 30, 36, w - M, 36, BRASS_DEEP, 1)


def draw_bottom_brass(d, w, h):
    M = 48
    hairline(d, M, h - 36, w // 2 - 30, h - 36, BRASS_DEEP, 1)
    hairline(d, w // 2 + 30, h - 36, w - M, h - 36, BRASS_DEEP, 1)
    hairline(d, M, h - 28, w - M, h - 28, BRASS, 2)


# ========================================================================
# CARD 01 — COLD OPEN
# ========================================================================
def card_01_cold_open():
    W, H = 1080, 1920
    canvas = make_ground(W, H, seed=11)
    d = ImageDraw.Draw(canvas)
    draw_top_brass(d, W, H)
    draw_bottom_brass(d, W, H)

    eb_f = jbmono(20, bold=True)
    eb = "CRIT HITS  ·  THE REVIEW COLUMN"
    draw_tracked(d, eb, center_x(eb, eb_f, W, 5), 70, eb_f, BRASS, ls=5)

    cy, cx = H // 2, W // 2
    for off in [-44, 0, 44]:
        r = 5 if off == 0 else 4
        d.ellipse([(cx + off - r, cy - r), (cx + off + r, cy + r)], fill=BRASS)

    code_f = jbmono(22)
    code = "CH·01·PH·MMXXVI"
    draw_tracked(d, code, center_x(code, code_f, W, 4), H - 100, code_f, MUTED, ls=4)
    return canvas


# ========================================================================
# CARD 02-03 — IN A WORLD
# ========================================================================
def card_02_in_a_world_1():
    W, H = 1080, 1920
    canvas = make_ground(W, H, seed=12)
    d = ImageDraw.Draw(canvas)
    lines = ["In a world where every man", "is told he should be happy..."]
    fnt = fraunces(74)
    total_h = len(lines) * int(fnt.size * 1.25)
    y = (H - total_h) // 2
    for line in lines:
        d.text((center_x(line, fnt, W), y), line, font=fnt, fill=BRASS_BRIGHT)
        y += int(fnt.size * 1.25)
    return canvas


def card_03_in_a_world_2():
    W, H = 1080, 1920
    canvas = make_ground(W, H, seed=13)
    d = ImageDraw.Draw(canvas)
    lines = ["...comes the genre",
             "publishing won't admit",
             "it reads."]
    fnt = fraunces(74)
    total_h = len(lines) * int(fnt.size * 1.25)
    y = (H - total_h) // 2
    for line in lines:
        d.text((center_x(line, fnt, W), y), line, font=fnt, fill=BRASS_BRIGHT)
        y += int(fnt.size * 1.25)
    return canvas


# ========================================================================
# CARD 04 — LITRPG GENRE FRAME
# ========================================================================
def card_04_litrpg_frame():
    W, H = 1080, 1920
    canvas = make_ground(W, H, seed=14)
    d = ImageDraw.Draw(canvas)

    eb_f = jbmono(22, bold=True)
    eb = "GENRE DEFINITION"
    draw_tracked(d, eb, center_x(eb, eb_f, W, 5), 200, eb_f, BRASS, ls=5)
    hairline(d, W // 2 - 80, 240, W // 2 + 80, 240, BRASS, 2)

    mono_f = jbmono(44, bold=True)
    lines = [
        ("> SYSTEM_DEFINE: LITRPG",        CREAM),
        ("",                                CREAM),
        ("> THE BIGGEST POPULAR",           CREAM),
        ("  FICTION NOBODY'S",              CREAM),
        ("  HEARD OF.",                     CREAM),
        ("",                                CREAM),
        ("> WHERE EVERY NOVEL",             CREAM),
        ("  IS ALSO A SPREADSHEET_",        BRASS_BRIGHT),
    ]
    max_w = max(text_w(t, mono_f) for t, _ in lines)
    x = (W - max_w) // 2
    y = 420
    line_h = int(mono_f.size * 1.30)
    for text, color in lines:
        d.text((x, y), text, font=mono_f, fill=color)
        y += line_h
    return canvas


# ========================================================================
# CARD 05 — A SPREADSHEET
# ========================================================================
def card_05_spreadsheet():
    W, H = 1080, 1920
    canvas = make_ground(W, H, seed=15)
    d = ImageDraw.Draw(canvas)

    grid_top = H // 2 - 280
    grid_bot = H // 2 + 280
    grid_left = 120
    grid_right = W - 120
    for i in range(9):
        y = grid_top + i * (grid_bot - grid_top) // 8
        d.line([(grid_left, y), (grid_right, y)], fill=SURFACE_2, width=1)
    for i in range(6):
        x = grid_left + i * (grid_right - grid_left) // 5
        d.line([(x, grid_top), (x, grid_bot)], fill=SURFACE_2, width=1)

    line1_f = fraunces(160)
    line1 = "a spreadsheet."
    while text_w(line1, line1_f) > W - 80:
        line1_f = fraunces(line1_f.size - 4)
    line1_w = text_w(line1, line1_f)
    d.text(((W - line1_w) // 2, (H - line1_f.size) // 2 - 20),
           line1, font=line1_f, fill=BRASS_BRIGHT)
    return canvas


# ========================================================================
# CARD 07 — STARRING
# ========================================================================
def card_07_starring():
    W, H = 1080, 1920
    canvas = make_ground(W, H, seed=17)
    d = ImageDraw.Draw(canvas)

    title_f = fraunces(220)
    title = "STARRING"
    tw = text_w(title, title_f, 8)
    while tw > W - 80:
        title_f = fraunces(title_f.size - 4)
        tw = text_w(title, title_f, 8)
    draw_tracked(d, title, (W - tw) // 2, (H - title_f.size) // 2 - 40,
                 title_f, BRASS_BRIGHT, ls=8)

    rule_y = (H - title_f.size) // 2 + title_f.size + 20
    rw = int(tw * 0.5)
    rx = (W - rw) // 2
    d.line([(rx, rule_y), (rx + rw, rule_y)], fill=BRASS, width=4)
    return canvas


# ========================================================================
# CARDS 08-10 — CHARACTER STAT BLOCKS
# ========================================================================
def _character_card(name, charclass, spec, tag, seed=18):
    W, H = 1080, 1920
    canvas = make_ground(W, H, seed=seed)
    d = ImageDraw.Draw(canvas)

    eb_f = jbmono(22, bold=True)
    eb = "STARRING  ·  REVIEW Nº 01"
    draw_tracked(d, eb, center_x(eb, eb_f, W, 5), 220, eb_f, BRASS, ls=5)
    hairline(d, W // 2 - 80, 260, W // 2 + 80, 260, BRASS, 2)

    cur_f = jbmono(54, bold=True)
    rows = [
        ("NAME:  ",  name,        CREAM),
        ("CLASS: ",  charclass,   CREAM),
        ("SPEC:  ",  spec,        CREAM),
        ("TAG:   ",  tag,         BRASS_BRIGHT),
    ]
    longest = max(text_w(k + v, cur_f) for k, v, _ in rows)
    target_w = W - 160
    while longest > target_w and cur_f.size > 24:
        cur_f = jbmono(cur_f.size - 2, bold=True)
        longest = max(text_w(k + v, cur_f) for k, v, _ in rows)

    line_h = int(cur_f.size * 1.65)
    block_h = len(rows) * line_h
    start_y = (H - block_h) // 2 + 60
    x = (W - longest) // 2

    for label, value, value_color in rows:
        d.text((x, start_y), label, font=cur_f, fill=BRASS_DEEP)
        label_w = text_w(label, cur_f)
        d.text((x + label_w, start_y), value, font=cur_f, fill=value_color)
        start_y += line_h

    code_f = jbmono(18)
    code = "CH·01·PH·MMXXVI"
    draw_tracked(d, code, center_x(code, code_f, W, 3), H - 100,
                 code_f, MUTED, ls=3)
    return canvas


def card_08_jake():
    return _character_card("JAKE THAYNE", "ARCHER", "FINANCIAL ANALYST",
                            "BLINDFOLDED-ARROW-CATCHING ENJOYER", seed=18)


def card_09_joanna():
    return _character_card("JOANNA", "ACCOUNTS", "COFFEE-MACHINE AMBUSHER",
                            "UNABRIDGED-WEEKEND PROVIDER", seed=19)


def card_10_villy():
    return _character_card("VILLY", "GOD", "POISONS",
                            "MUSHROOM PROFESSOR", seed=20)


# ========================================================================
# CARD 11 — SYSTEM EATS EARTH
# ========================================================================
def card_11_system_eats_earth():
    W, H = 1080, 1920
    canvas = make_ground(W, H, seed=21)
    d = ImageDraw.Draw(canvas)

    hdr_f = jbmono(46, bold=True)
    hdr = "[SYSTEM ANNOUNCEMENT]"
    draw_tracked(d, hdr, center_x(hdr, hdr_f, W, 4), 380,
                 hdr_f, SIGNAL_RED, ls=4)
    hairline(d, W // 2 - 200, 440, W // 2 + 200, 440, SIGNAL_RED, 2)

    body_f = jbmono(50, bold=True)
    lines = [
        "> EARTH: TERMINATED",
        "> PAGE: 8",
        "> BADGER COUNT: 4",
        "> JAKE: DROPPED INTO",
        "  FOREST.",
    ]
    max_w = max(text_w(t, body_f) for t in lines)
    x = (W - max_w) // 2
    y = 540
    for t in lines:
        d.text((x, y), t, font=body_f, fill=SIGNAL_RED)
        y += int(body_f.size * 1.45)
    return canvas


# ========================================================================
# CARD 12 — PIVOT
# ========================================================================
def card_12_pivot():
    W, H = 1080, 1920
    canvas = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(canvas)

    lines = ["And, for the first", "time in his life..."]
    fnt = crimson_italic(82)
    line_h = int(fnt.size * 1.30)
    total_h = len(lines) * line_h
    y = (H - total_h) // 2
    for line in lines:
        d.text((center_x(line, fnt, W), y), line, font=fnt, fill=CREAM)
        y += line_h
    return canvas


# ========================================================================
# CARD 13 — PULL QUOTE
# ========================================================================
def card_13_pull_quote():
    W, H = 1080, 1920
    canvas = make_ground(W, H, seed=23)
    d = ImageDraw.Draw(canvas)

    pad = 80
    card_top, card_bot = 480, H - 480
    d.rectangle([(pad, card_top), (W - pad, card_bot)], outline=BRASS, width=3)
    d.rectangle([(pad + 14, card_top + 14), (W - pad - 14, card_bot - 14)],
                outline=BRASS_DEEP, width=1)

    eb_f = jbmono(20, bold=True)
    eb = "PULL QUOTE"
    draw_tracked(d, eb, center_x(eb, eb_f, W, 5), card_top + 60,
                 eb_f, BRASS, ls=5)
    hairline(d, W // 2 - 60, card_top + 100, W // 2 + 60, card_top + 100, BRASS, 1)

    quote = "“A quiet book about a man having a genuinely nice time.”"
    q_f = crimson_italic(56)
    inner_w = W - 2 * (pad + 80)
    words = quote.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if text_w(test, q_f) <= inner_w:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    line_h = int(q_f.size * 1.30)
    total_h = len(lines) * line_h
    y = card_top + (card_bot - card_top - total_h) // 2
    for line in lines:
        d.text((center_x(line, q_f, W), y), line, font=q_f, fill=CREAM)
        y += line_h

    attr_f = inter_med(22)
    attr = "CRIT HITS  Nº 01  ·  THE PRIMAL HUNTER"
    draw_tracked(d, attr, center_x(attr, attr_f, W, 3), card_bot - 80,
                 attr_f, MUTED, ls=3)
    return canvas


# ========================================================================
# CARD 14 — HONEST TITLE
# ========================================================================
def card_14_honest_title():
    W, H = 1080, 1920
    canvas = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(canvas)

    eb_f = jbmono(28, bold=True)
    eb = "AN HONEST TITLE"
    draw_tracked(d, eb, center_x(eb, eb_f, W, 6), 380, eb_f, BRASS, ls=6)
    hairline(d, W // 2 - 100, 430, W // 2 + 100, 430, BRASS, 2)

    lines = [
        "PORTAL FANTASY",
        "FOR INTROVERTS",
        "WHO WERE NEVER GOING",
        "TO MAKE PARTNER",
    ]
    title_f = fraunces(108)
    while max(text_w(l, title_f) for l in lines) > W - 60:
        title_f = fraunces(title_f.size - 4)
    line_h = int(title_f.size * 1.12)
    total_h = len(lines) * line_h
    # Centre vertically (with eyebrow already at y=380, give it room above)
    y = (H - total_h) // 2
    for line in lines:
        d.text((center_x(line, title_f, W), y), line, font=title_f, fill=BRASS_BRIGHT)
        y += line_h
    return canvas


# ========================================================================
# CARD 15 — END CARD
# ========================================================================
def card_15_end_card():
    W, H = 1080, 1920
    canvas = make_ground(W, H, seed=25)
    d = ImageDraw.Draw(canvas)
    draw_top_brass(d, W, H)
    draw_bottom_brass(d, W, H)

    eb_f = jbmono(22, bold=True)
    eb = "CRIT HITS  ·  THE REVIEW COLUMN"
    draw_tracked(d, eb, center_x(eb, eb_f, W, 5), 70, eb_f, BRASS, ls=5)

    mark_path = os.path.join(BRAND_DIR, "malory-mark.svg")
    mark_size = 320
    mark = render_svg(mark_path, width=mark_size, height=mark_size)
    canvas.paste(mark, ((W - mark_size) // 2, 480), mark)

    title_f = fraunces(96)
    title = "CRIT HITS  Nº 01"
    tw = text_w(title, title_f, 4)
    draw_tracked(d, title, (W - tw) // 2, 880, title_f, BRASS_BRIGHT, ls=4)

    tag_f = inter_med(32)
    tag = "LitRPG  ·  reviewed from inside the game."
    draw_tracked(d, tag, center_x(tag, tag_f, W, 2), 1000, tag_f, MUTED, ls=2)

    rule_y = 1100
    hairline(d, 200, rule_y, W // 2 - 30, rule_y, BRASS, 1)
    hairline(d, W // 2 + 30, rule_y, W - 200, rule_y, BRASS, 1)
    cx = W // 2
    for off in [-18, 0, 18]:
        r = 3 if off == 0 else 2
        d.ellipse([(cx + off - r, rule_y - r), (cx + off + r, rule_y + r)],
                  fill=BRASS)

    url_f = jbmono(32, bold=True)
    url = "MALORYAUTHOR.SUBSTACK.COM"
    draw_tracked(d, url, center_x(url, url_f, W, 5), 1240, url_f, CREAM, ls=5)

    sub_f = inter_med(22)
    sub = "FULL REVIEW"
    draw_tracked(d, sub, center_x(sub, sub_f, W, 5), 1310, sub_f, BRASS, ls=5)

    code_f = jbmono(22)
    code = "CH·01·PH·MMXXVI"
    draw_tracked(d, code, center_x(code, code_f, W, 4), H - 100,
                 code_f, MUTED, ls=4)
    return canvas


# ========================================================================
# main
# ========================================================================
def main():
    cards = [
        ("01-cold-open",          card_01_cold_open),
        ("02-in-a-world-1",       card_02_in_a_world_1),
        ("03-in-a-world-2",       card_03_in_a_world_2),
        ("04-litrpg-frame",       card_04_litrpg_frame),
        ("05-spreadsheet",        card_05_spreadsheet),
        # 06 = the existing 9:16 cover (book reveal), already in _assets/
        ("07-starring",           card_07_starring),
        ("08-jake",               card_08_jake),
        ("09-joanna",             card_09_joanna),
        ("10-villy",              card_10_villy),
        ("11-system-eats-earth",  card_11_system_eats_earth),
        ("12-pivot",              card_12_pivot),
        ("13-pull-quote",         card_13_pull_quote),
        ("14-honest-title",       card_14_honest_title),
        ("15-end-card",           card_15_end_card),
    ]
    for slug, fn in cards:
        img = fn()
        for dest in [VAULT_OUT, WS_OUT]:
            outp = os.path.join(dest, f"{slug}.png")
            img.save(outp, "PNG", optimize=True)
        print(f"  saved {slug}.png")
    print(f"\nTotal: {len(cards)} cards saved to:")
    print(f"  {VAULT_OUT}")
    print(f"  {WS_OUT}")


if __name__ == "__main__":
    print("Building PH Shorts cards (1080x1920)")
    print("=" * 50)
    main()
