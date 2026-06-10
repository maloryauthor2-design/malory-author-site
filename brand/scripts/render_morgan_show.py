#!/usr/bin/env python3
"""THE MORGAN SHOW — episodic reel renderer (M&M, weekly series).

Episode 1: "Don't move." — ch1 recruitment, all lines verbatim (post-beta docx).
Same proven iMessage skin as the 600-view trial, plus the series wrapper:
a violet episode badge on every frame and a next-episode tease composited
onto the title card. Swap EPISODE for next week's gag and re-render.
Static stills only, concat-demuxer MP4 workflow unchanged.
"""
from PIL import Image, ImageDraw, ImageFont
import random

W, H = 1080, 1920
REPO = "/sessions/youthful-epic-lovelace/mnt/malory-author-website"
FONTS = f"{REPO}/brand/fonts"
OUT = "/sessions/youthful-epic-lovelace/mnt/outputs"

INTER_MED = f"{FONTS}/Inter-Medium-static.ttf"
INTER_SEMI = f"{FONTS}/Inter-SemiBold-static.ttf"

IOS_BG = (0, 0, 0)
BUBBLE_GRAY = (38, 38, 42)
BUBBLE_BLUE = (10, 132, 255)
TXT_WHITE = (255, 255, 255)
TXT_GRAY = (142, 142, 147)
CANVAS = (5, 5, 7)
MM_VIOLET = (91, 58, 122)

EPISODE = {
    "num": 1,
    "badge": "537 AD · ep 1",
    "contact": "Unknown",
    "avatar": "?",
    "caption1": "she woke up dead on a battlefield in 537 AD.",
    "caption2": "the legend of Morgan le Fay starts here.",
    # ('m' = contact gray-left, 'o' = Morgan blue-right)
    "thread": [
        ("m", "Don't move."),
        ("m", "If you move, they will see you still live, and then they will kill you."),
        ("o", "Who are you, and what do you want with my dead arse?"),
        ("m", "There is absolutely nothing about your arse that interests me. My name is Merlin, and I am going to need you to help me save the world."),
    ],
    # (n_visible, typing, caption2, hold seconds)
    "sequence": [
        (0, True,  False, 0.6),
        (1, False, False, 1.1),
        (1, True,  False, 0.4),
        (2, False, False, 1.9),
        (3, False, False, 1.8),
        (3, True,  False, 0.4),
        (4, False, False, 2.5),
        (4, False, True,  2.0),
    ],
    "tease": "next episode: morgan tells a joke. merlin pretends not to get it.",
    "prefix": "ms_ep01",
}

def F(p, s): return ImageFont.truetype(p, s)

f_bub = F(INTER_MED, 38)
f_name = F(INTER_MED, 31)
f_date_b = F(INTER_SEMI, 28)
f_date = F(INTER_MED, 28)
f_small = F(INTER_MED, 27)
f_cap = F(INTER_SEMI, 44)
f_av = F(INTER_SEMI, 50)
f_badge = F(INTER_SEMI, 30)
f_tease = F(INTER_MED, 30)
LH = 50
MAXW = 560
CARD_W = 920
CARD_X = (W - CARD_W) // 2

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
BUBBLES = []
for side, text in EPISODE["thread"]:
    lines = wrap(probe, text, f_bub, MAXW)
    bh = int(len(lines) * LH + 44 - (LH - f_bub.size) * 0.4)
    BUBBLES.append({"side": side, "lines": lines, "h": bh, "font": f_bub})

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
        x0 = CARD_X + CARD_W - 36 - bw; x1 = CARD_X + CARD_W - 36
    else:
        x0 = CARD_X + 36; x1 = x0 + bw
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

def draw_badge(d):
    s = EPISODE["badge"]
    tw = d.textlength(s, font=f_badge)
    bw, bh = tw + 56, 56
    x0 = (W - bw) / 2; y0 = 58
    d.rounded_rectangle((x0, y0, x0 + bw, y0 + bh), radius=28, fill=MM_VIOLET)
    d.text((x0 + 28, y0 + 11), s, font=f_badge, fill=(245, 240, 250))

def render_state(n_visible, typing, caption2, fname):
    img = Image.new("RGB", (W, H), CANVAS)
    d = ImageDraw.Draw(img)

    draw_badge(d)

    cy = 158
    lw = d.textlength(EPISODE["caption1"], font=f_cap)
    d.text(((W - lw) / 2, cy), EPISODE["caption1"], font=f_cap, fill=(245, 245, 245))
    if caption2:
        lw2 = d.textlength(EPISODE["caption2"], font=f_cap)
        d.text(((W - lw2) / 2, cy + 58), EPISODE["caption2"], font=f_cap, fill=(245, 245, 245))

    card_y = 300
    ch = card_height(n_visible, typing)
    d.rounded_rectangle((CARD_X, card_y, CARD_X + CARD_W, card_y + ch),
                        radius=52, fill=IOS_BG, outline=(40, 40, 44), width=2)

    # header — contact is "Unknown" with a "?" avatar; the reveal is the last bubble
    hx = CARD_X + 44
    hy = card_y + 82
    d.line([(hx + 22, hy - 26), (hx, hy), (hx + 22, hy + 26)],
           fill=BUBBLE_BLUE, width=6, joint="curve")
    av_cx, av_cy, av_r = CARD_X + CARD_W // 2, card_y + 86, 54
    d.ellipse((av_cx - av_r, av_cy - av_r, av_cx + av_r, av_cy + av_r), fill=(108, 114, 128))
    aw = d.textlength(EPISODE["avatar"], font=f_av)
    d.text((av_cx - aw / 2, av_cy - 33), EPISODE["avatar"], font=f_av, fill=(235, 235, 240))
    nw = d.textlength(EPISODE["contact"], font=f_name)
    d.text((av_cx - nw / 2 - 10, av_cy + av_r + 14), EPISODE["contact"], font=f_name, fill=TXT_WHITE)
    chx, chy = av_cx + nw / 2 + 4, av_cy + av_r + 31
    d.line([(chx, chy - 9), (chx + 9, chy), (chx, chy + 9)], fill=TXT_GRAY, width=3)
    vx, vy = CARD_X + CARD_W - 110, card_y + 68
    d.rounded_rectangle((vx, vy + 6, vx + 44, vy + 36), radius=10, outline=BUBBLE_BLUE, width=5)
    d.polygon([(vx + 48, vy + 21), (vx + 66, vy + 6), (vx + 66, vy + 36)], outline=BUBBLE_BLUE)

    dy = card_y + HEADER_H
    wb = d.textlength("537 AD", font=f_date_b)
    wr = d.textlength("  9:41 AM", font=f_date)
    sx = CARD_X + (CARD_W - wb - wr) / 2
    d.text((sx, dy), "537 AD", font=f_date_b, fill=TXT_GRAY)
    d.text((sx + wb, dy), "  9:41 AM", font=f_date, fill=TXT_GRAY)

    y = dy + DATE_H
    last_o_bottom = None
    for i, b in enumerate(BUBBLES):
        if i >= n_visible: break
        yb = draw_bubble(d, b, y)
        if b["side"] == "o": last_o_bottom = yb
        y = yb + GAP

    if last_o_bottom and n_visible and BUBBLES[n_visible - 1]["side"] == "o":
        dw = d.textlength("Delivered", font=f_small)
        d.text((CARD_X + CARD_W - 36 - dw - 6, last_o_bottom + 8),
               "Delivered", font=f_small, fill=TXT_GRAY)
        y = last_o_bottom + DELIVERED_H + 14

    if typing:
        draw_typing(d, y)

    random.seed(537)
    px = img.load()
    for _ in range(14000):
        x_, y_ = random.randint(0, W - 1), random.randint(0, H - 1)
        r_, g_, b_ = px[x_, y_]
        n = random.randint(-4, 4)
        px[x_, y_] = (max(0, min(255, r_ + n)), max(0, min(255, g_ + n)), max(0, min(255, b_ + n)))

    img.save(f"{OUT}/{fname}")
    return fname

# ---- series title card: existing card + episode line + next-episode tease ----
def render_titlecard():
    base = Image.open(f"{REPO}/brand/reels/morgan-merlin-imessage/mm_titlecard.png").convert("RGB")
    bw, bh = base.size
    sc = bw / 1080.0
    d = ImageDraw.Draw(base)
    f_ep = F(INTER_SEMI, int(34 * sc))
    f_tz = F(INTER_MED, int(30 * sc))
    ep_s = "the morgan show · episode one"
    tw = d.textlength(ep_s, font=f_ep)
    ey = int(bh * 0.905)
    d.text(((bw - tw) / 2, ey), ep_s, font=f_ep, fill=(200, 180, 220))
    lines = wrap(d, EPISODE["tease"], f_tz, int(bw * 0.84))
    ty = ey + int(48 * sc)
    for l in lines:
        lw = d.textlength(l, font=f_tz)
        d.text(((bw - lw) / 2, ty), l, font=f_tz, fill=(150, 150, 158))
        ty += int(40 * sc)
    p = f"{OUT}/{EPISODE['prefix']}_titlecard.png"
    base.save(p)
    return p

with open(f"{OUT}/{EPISODE['prefix']}_frames.txt", "w") as fl:
    for i, (n, t, c2, hold) in enumerate(EPISODE["sequence"]):
        fn = render_state(n, t, c2, f"{EPISODE['prefix']}_frame_{i:02d}.png")
        fl.write(f"file '{OUT}/{fn}'\nduration {hold}\n")
    fl.write(f"file '{OUT}/{EPISODE['prefix']}_frame_{len(EPISODE['sequence'])-1:02d}.png'\n")

tc = render_titlecard()
total = sum(s[3] for s in EPISODE["sequence"])
print(f"rendered {len(EPISODE['sequence'])} frames + titlecard {tc}, main {total:.1f}s")
