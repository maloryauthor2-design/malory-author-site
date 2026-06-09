#!/usr/bin/env python3
"""Morgan & Merlin iMessage Reel — progressive-reveal frame renderer.
Generates one PNG per conversation state; ffmpeg concatenates them with
timed holds so the thread plays out like live messaging. Still static
frames only — no keyframe motion, drop-in MP4 workflow unchanged.
"""
from PIL import Image, ImageDraw, ImageFont
import random

W, H = 1080, 1920
FONTS = "/sessions/determined-focused-wright/mnt/malory-author-website/brand/fonts"
INTER_MED = f"{FONTS}/Inter-Medium-static.ttf"
INTER_SEMI = f"{FONTS}/Inter-SemiBold-static.ttf"
OUT = "/sessions/determined-focused-wright/mnt/outputs"

IOS_BG = (0, 0, 0)
BUBBLE_GRAY = (38, 38, 42)
BUBBLE_BLUE = (10, 132, 255)
TXT_WHITE = (255, 255, 255)
TXT_GRAY = (142, 142, 147)
CANVAS = (5, 5, 7)

CAPTION_1 = "merlin waited 1,500 years for an heir."
CAPTION_2 = "he got morgan."

# (sender, text, mono) — 'm' = Merlin gray-left, 'o' = Morgan blue-right
THREAD = [
    ("m", "A technique's name defines a cultivator's legend for centuries. Choose with great care."),
    ("o", "[Can of Whoopass] technique named", "mono"),
    ("m", "You could not help yourself, could you?"),
    ("o", "and that's the bottom line. because Morgan said so"),
]

def F(path, size):
    return ImageFont.truetype(path, size)

f_bub = F(INTER_MED, 38)
f_mono = F("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 35)
f_name = F(INTER_MED, 31)
f_date_b = F(INTER_SEMI, 28)
f_date = F(INTER_MED, 28)
f_small = F(INTER_MED, 27)
f_cap = F(INTER_SEMI, 44)
f_av = F(INTER_SEMI, 50)
LH = 50
MAXW = 560
CARD_W = 920
CARD_X = (W - CARD_W) // 2

def wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

# ---- pre-measure all bubbles against final layout ----
probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
BUBBLES = []
for entry in THREAD:
    side, text = entry[0], entry[1]
    font = f_mono if len(entry) > 2 and entry[2] == "mono" else f_bub
    lines = wrap(probe, text, font, MAXW)
    bh = int(len(lines) * LH + 44 - (LH - font.size) * 0.4)
    BUBBLES.append({"side": side, "lines": lines, "h": bh, "font": font})

HEADER_H, DATE_H, GAP = 208, 58, 18
DELIVERED_H, TYPING_H = 40, 104

def card_height(n_visible, typing):
    h = HEADER_H + DATE_H + sum(b["h"] for b in BUBBLES[:n_visible]) + GAP * n_visible
    if n_visible and BUBBLES[n_visible - 1]["side"] == "o":
        h += DELIVERED_H + 14
    if typing:
        h += TYPING_H
    return h + 32

def draw_bubble(d, b, y):
    color = BUBBLE_BLUE if b["side"] == "o" else BUBBLE_GRAY
    fnt = b["font"]
    tw = max(d.textlength(l, font=fnt) for l in b["lines"])
    bw = int(tw + 64)
    if b["side"] == "o":
        x0 = CARD_X + CARD_W - 36 - bw
        x1 = CARD_X + CARD_W - 36
    else:
        x0 = CARD_X + 36
        x1 = x0 + bw
    d.rounded_rectangle((x0, y, x0 + bw, y + b["h"]), radius=40, fill=color)
    bot = y + b["h"]
    if b["side"] == "o":
        d.ellipse((x1 - 16, bot - 28, x1 + 16, bot + 4), fill=color)
        d.ellipse((x1 + 2, bot - 34, x1 + 42, bot + 6), fill=IOS_BG)
    else:
        d.ellipse((x0 - 16, bot - 28, x0 + 16, bot + 4), fill=color)
        d.ellipse((x0 - 42, bot - 34, x0 - 2, bot + 6), fill=IOS_BG)
    yy = y + 19
    for l in b["lines"]:
        d.text((x0 + 34, yy), l, font=fnt, fill=TXT_WHITE)
        yy += LH
    return bot

def draw_typing(d, y):
    tb_w, tb_h = 168, 92
    tx0 = CARD_X + 36
    d.rounded_rectangle((tx0, y, tx0 + tb_w, y + tb_h), radius=44, fill=BUBBLE_GRAY)
    tbot = y + tb_h
    d.ellipse((tx0 - 16, tbot - 28, tx0 + 16, tbot + 4), fill=BUBBLE_GRAY)
    d.ellipse((tx0 - 42, tbot - 34, tx0 - 2, tbot + 6), fill=IOS_BG)
    dot_y = y + tb_h // 2
    for i, dx in enumerate((46, 84, 122)):
        shade = (150, 150, 156) if i == 1 else (120, 120, 126)
        d.ellipse((tx0 + dx - 11, dot_y - 11, tx0 + dx + 11, dot_y + 11), fill=shade)

def render_state(n_visible, typing, caption2, fname):
    """n_visible bubbles shown; typing dots after them if typing=True."""
    img = Image.new("RGB", (W, H), CANVAS)
    d = ImageDraw.Draw(img)

    # caption — line 1 fixed in place, line 2 appears under it on the punchline frame
    cy = 152
    lw = d.textlength(CAPTION_1, font=f_cap)
    d.text(((W - lw) / 2, cy), CAPTION_1, font=f_cap, fill=(245, 245, 245))
    if caption2:
        lw2 = d.textlength(CAPTION_2, font=f_cap)
        d.text(((W - lw2) / 2, cy + 58), CAPTION_2, font=f_cap, fill=(245, 245, 245))

    card_y = 285
    ch = card_height(n_visible, typing)
    d.rounded_rectangle((CARD_X, card_y, CARD_X + CARD_W, card_y + ch),
                        radius=52, fill=IOS_BG, outline=(40, 40, 44), width=2)

    # header
    hx = CARD_X + 44
    hy = card_y + 82
    d.line([(hx + 22, hy - 26), (hx, hy), (hx + 22, hy + 26)],
           fill=BUBBLE_BLUE, width=6, joint="curve")
    av_cx, av_cy, av_r = CARD_X + CARD_W // 2, card_y + 86, 54
    d.ellipse((av_cx - av_r, av_cy - av_r, av_cx + av_r, av_cy + av_r), fill=(108, 114, 128))
    aw = d.textlength("M", font=f_av)
    d.text((av_cx - aw / 2, av_cy - 33), "M", font=f_av, fill=(235, 235, 240))
    nw = d.textlength("Merlin", font=f_name)
    d.text((av_cx - nw / 2 - 10, av_cy + av_r + 14), "Merlin", font=f_name, fill=TXT_WHITE)
    chx, chy = av_cx + nw / 2 + 4, av_cy + av_r + 31
    d.line([(chx, chy - 9), (chx + 9, chy), (chx, chy + 9)], fill=TXT_GRAY, width=3)
    vx, vy = CARD_X + CARD_W - 110, card_y + 68
    d.rounded_rectangle((vx, vy + 6, vx + 44, vy + 36), radius=10, outline=BUBBLE_BLUE, width=5)
    d.polygon([(vx + 48, vy + 21), (vx + 66, vy + 6), (vx + 66, vy + 36)], outline=BUBBLE_BLUE)

    # date
    dy = card_y + HEADER_H
    wb = d.textlength("537 AD", font=f_date_b)
    wr = d.textlength("  9:41 AM", font=f_date)
    sx = CARD_X + (CARD_W - wb - wr) / 2
    d.text((sx, dy), "537 AD", font=f_date_b, fill=TXT_GRAY)
    d.text((sx + wb, dy), "  9:41 AM", font=f_date, fill=TXT_GRAY)

    # bubbles in fixed positions
    y = dy + DATE_H
    last_o_bottom = None
    for i, b in enumerate(BUBBLES):
        if i >= n_visible:
            break
        yb = draw_bubble(d, b, y)
        if b["side"] == "o":
            last_o_bottom = yb
        y = yb + GAP

    # Delivered under Morgan's most recent visible text
    if last_o_bottom and BUBBLES[n_visible - 1]["side"] == "o":
        dw = d.textlength("Delivered", font=f_small)
        d.text((CARD_X + CARD_W - 36 - dw - 6, last_o_bottom + 8),
               "Delivered", font=f_small, fill=TXT_GRAY)
        y = last_o_bottom + DELIVERED_H + 14

    if typing:
        draw_typing(d, y)

    # grain
    random.seed(537)
    px = img.load()
    for _ in range(14000):
        x_, y_ = random.randint(0, W - 1), random.randint(0, H - 1)
        r_, g_, b_ = px[x_, y_]
        n = random.randint(-4, 4)
        px[x_, y_] = (max(0, min(255, r_ + n)), max(0, min(255, g_ + n)), max(0, min(255, b_ + n)))

    img.save(f"{OUT}/{fname}")
    return fname

# ---- the reveal sequence: (n_visible, typing, caption2, hold seconds) ----
# dots before every Merlin message; Morgan's system line pops back instantly —
# the reply speed is the punchline
SEQUENCE = [
    (0, True,  False, 0.7),   # opening: Merlin typing into the void
    (1, False, False, 1.7),   # the solemn naming lecture
    (2, False, False, 1.6),   # [Can of Whoopass] — instant, no hesitation
    (2, True,  False, 0.5),   # dots…
    (3, False, False, 1.4),   # "You could not help yourself, could you?"
    (4, False, False, 1.7),   # bottom line + Delivered
    (4, True,  True,  2.1),   # dots forever + "he got morgan."
]

with open(f"{OUT}/frames.txt", "w") as fl:
    for i, (n, t, c2, hold) in enumerate(SEQUENCE):
        fn = render_state(n, t, c2, f"mm_frame_{i:02d}.png")
        fl.write(f"file '{OUT}/{fn}'\nduration {hold}\n")
    # concat demuxer needs the last file repeated, no duration
    fl.write(f"file '{OUT}/mm_frame_{len(SEQUENCE)-1:02d}.png'\n")

total = sum(s[3] for s in SEQUENCE)
print(f"rendered {len(SEQUENCE)} frames, main duration {total:.1f}s, final card_bottom {285 + card_height(len(BUBBLES), True)}")
