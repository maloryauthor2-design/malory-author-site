#!/usr/bin/env python3
"""Arcane Galaxy — 'The Gazelle' crew GROUP iMessage, scrolling progressive reveal.
Fixed phone-screen card; bubbles bottom-anchor and older ones clip off the top
like a real long thread. Incoming bubbles get a sender name + coloured avatar on
the first of a run; Rivers (phone owner) is blue/right. On-brand AG title card
closes the reel. Book 1 cast only (Rivers, Bluey, Henrik).
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
NAME_GRAY = (150, 150, 156)
CANVAS = (5, 5, 7)

AV = {
    "Bluey":  (58, 150, 168),
    "Henrik": (206, 128, 70),
}

CAPTION_1 = "breaking him out of space prison"
CAPTION_2 = "he'd rather stay in."

# (sender, text) — 'Rivers' = outgoing blue-right; others incoming gray-left. Book 1 canon.
THREAD = [
    ("Rivers", "Henrik. sit tight, we're breaking you out"),
    ("Henrik", "who is this"),
    ("Rivers", "cell B-24601. that's you?"),
    ("Henrik", "...yes. how do you have my cell number"),
    ("Bluey",  "i'm on the watchtower cannon when you're ready"),
    ("Henrik", "the watchtower has a cannon??"),
    ("Bluey",  "not for much longer"),
    ("Rivers", "it's a rescue, Henrik. try to look rescued"),
    ("Henrik", "mate i'm on death row for genocide. better life expectancy in here"),
    ("Henrik", "fewer explosions. more regular meals"),
    ("Rivers", "about that"),
    ("Bluey",  "Henrik. move away from the east wall"),
    ("Henrik", "WHICH wall"),
]

def F(path, size):
    return ImageFont.truetype(path, size)

f_bub   = F(INTER_MED, 39)
f_name  = F(INTER_MED, 27)
f_hdr   = F(INTER_MED, 31)
f_date_b= F(INTER_SEMI, 28)
f_date  = F(INTER_MED, 28)
f_small = F(INTER_MED, 27)
f_cap   = F(INTER_SEMI, 44)
f_av    = F(INTER_SEMI, 38)
f_avhdr = F(INTER_SEMI, 30)
LH = 50
MAXW = 600
CARD_W = 936
CARD_X = (W - CARD_W) // 2
AV_R = 33

# fixed phone-screen card geometry
CARD_Y = 206
CARD_H = 1486
CARD_BOTTOM = CARD_Y + CARD_H            # 1692
HEADER_H = 198
VIEW_TOP = CARD_Y + HEADER_H             # 404
VIEW_BOTTOM = CARD_BOTTOM - 24           # 1668
DATE_BLOCK = 64
GAP, NAME_H, TYPING_H = 16, 30, 88

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w_
    if cur:
        lines.append(cur)
    return lines

probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
BUB = []
for i, (sender, text) in enumerate(THREAD):
    lines = wrap(probe, text, f_bub, MAXW)
    bh = int(len(lines) * LH + 36)
    run_start = (sender != "Rivers") and (i == 0 or THREAD[i-1][0] != sender)
    BUB.append({"sender": sender, "lines": lines, "h": bh,
                "incoming": sender != "Rivers", "run_start": run_start})

def content_height(n, typing):
    h = DATE_BLOCK
    for i in range(n):
        if BUB[i]["run_start"]:
            h += NAME_H
        h += BUB[i]["h"] + GAP
    if typing:
        h += TYPING_H
    return h

def draw_avatar(d, cx, cy, r, fill, initial, font):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill)
    iw = d.textlength(initial, font=font)
    d.text((cx - iw / 2, cy - font.size * 0.62), initial, font=font, fill=(245, 245, 245))

def draw_bubble(d, b, y):
    incoming = b["incoming"]
    color = BUBBLE_GRAY if incoming else BUBBLE_BLUE
    tw = max(d.textlength(l, font=f_bub) for l in b["lines"])
    bw = int(tw + 60)
    if incoming:
        x0 = CARD_X + 36 + AV_R * 2 + 16
        x1 = x0 + bw
    else:
        x1 = CARD_X + CARD_W - 46
        x0 = x1 - bw
    d.rounded_rectangle((x0, y, x0 + bw, y + b["h"]), radius=38, fill=color)
    bot = y + b["h"]
    if incoming:
        d.ellipse((x0 - 16, bot - 28, x0 + 16, bot + 4), fill=color)
        d.ellipse((x0 - 42, bot - 34, x0 - 2, bot + 6), fill=IOS_BG)
    else:
        d.ellipse((x1 - 16, bot - 28, x1 + 16, bot + 4), fill=color)
        d.ellipse((x1 + 2, bot - 34, x1 + 42, bot + 6), fill=IOS_BG)
    yy = y + 19
    for l in b["lines"]:
        d.text((x0 + 30, yy), l, font=f_bub, fill=TXT_WHITE)
        yy += LH
    return bot

def draw_typing(d, y):
    tb_w, tb_h = 156, 84
    tx0 = CARD_X + 36 + AV_R * 2 + 16
    d.rounded_rectangle((tx0, y, tx0 + tb_w, y + tb_h), radius=40, fill=BUBBLE_GRAY)
    tbot = y + tb_h
    d.ellipse((tx0 - 16, tbot - 26, tx0 + 14, tbot + 4), fill=BUBBLE_GRAY)
    d.ellipse((tx0 - 40, tbot - 32, tx0 - 2, tbot + 6), fill=IOS_BG)
    dot_y = y + tb_h // 2
    for i, dx in enumerate((42, 78, 114)):
        shade = (150, 150, 156) if i == 1 else (118, 118, 124)
        d.ellipse((tx0 + dx - 10, dot_y - 10, tx0 + dx + 10, dot_y + 10), fill=shade)

def render_state(n, typing, caption2, fname):
    img = Image.new("RGB", (W, H), CANVAS)
    d = ImageDraw.Draw(img)

    # caption
    lw = d.textlength(CAPTION_1, font=f_cap)
    d.text(((W - lw) / 2, 82), CAPTION_1, font=f_cap, fill=(245, 245, 245))
    if caption2:
        lw2 = d.textlength(CAPTION_2, font=f_cap)
        d.text(((W - lw2) / 2, 140), CAPTION_2, font=f_cap, fill=(245, 245, 245))

    # card (fixed phone screen)
    d.rounded_rectangle((CARD_X, CARD_Y, CARD_X + CARD_W, CARD_BOTTOM),
                        radius=52, fill=IOS_BG, outline=(40, 40, 44), width=2)

    # ---- scroll content on its own layer, then composite only the viewport band ----
    ch = content_height(n, typing)
    view_h = VIEW_BOTTOM - VIEW_TOP
    y = (VIEW_TOP + 8) if ch <= view_h else (VIEW_BOTTOM - ch)

    scroll = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scroll)

    wb = sd.textlength("Today", font=f_date_b)
    wr = sd.textlength("  9:41 AM", font=f_date)
    sx = CARD_X + (CARD_W - wb - wr) / 2
    sd.text((sx, y), "Today", font=f_date_b, fill=TXT_GRAY)
    sd.text((sx + wb, y), "  9:41 AM", font=f_date, fill=TXT_GRAY)
    y += DATE_BLOCK

    last_bottom, last_incoming = None, True
    for i in range(n):
        b = BUB[i]
        if b["run_start"]:
            nx = CARD_X + 36 + AV_R * 2 + 16 + 12
            sd.text((nx, y), b["sender"], font=f_name, fill=NAME_GRAY)
            y += NAME_H
        yb = draw_bubble(sd, b, y)
        if b["run_start"]:
            draw_avatar(sd, CARD_X + 36 + AV_R, yb - AV_R, AV_R,
                        AV[b["sender"]], b["sender"][0], f_av)
        last_bottom, last_incoming = yb, b["incoming"]
        y = yb + GAP

    if last_bottom is not None and not last_incoming and not typing:
        dw = sd.textlength("Delivered", font=f_small)
        sd.text((CARD_X + CARD_W - 40 - dw, last_bottom + 6), "Delivered", font=f_small, fill=TXT_GRAY)

    if typing:
        draw_typing(sd, y)

    # clip to the viewport band (top + bottom) and paste onto the card
    band = scroll.crop((0, VIEW_TOP, W, VIEW_BOTTOM))
    img.paste(band, (0, VIEW_TOP), band)
    d = ImageDraw.Draw(img)

    # ---- header nav drawn on top of the (already solid) card header band ----
    hx, hy = CARD_X + 42, CARD_Y + 92
    d.line([(hx + 20, hy - 24), (hx, hy), (hx + 20, hy + 24)], fill=BUBBLE_BLUE, width=6, joint="curve")
    gcx, gcy = CARD_X + CARD_W // 2, CARD_Y + 82
    d.ellipse((gcx - 6, gcy - 46, gcx + 78, gcy + 38), fill=(150, 150, 156))
    d.ellipse((gcx - 78, gcy - 38, gcx + 6, gcy + 46), fill=(96, 102, 116))
    d.text((gcx - 78 + 28, gcy - 16), "G", font=f_avhdr, fill=(235, 235, 240))
    nm = "The Gazelle"
    nw = d.textlength(nm, font=f_hdr)
    d.text((gcx - nw / 2 - 9, gcy + 56), nm, font=f_hdr, fill=TXT_WHITE)
    cx2 = gcx + nw / 2 + 6
    cy2 = gcy + 56 + 16
    d.line([(cx2, cy2 - 8), (cx2 + 8, cy2), (cx2, cy2 + 8)], fill=TXT_GRAY, width=3)
    # thin divider under header
    d.line([(CARD_X + 3, VIEW_TOP), (CARD_X + CARD_W - 3, VIEW_TOP)], fill=(28, 28, 32), width=2)

    random.seed(52)
    px = img.load()
    for _ in range(13000):
        rx, ry = random.randint(0, W - 1), random.randint(0, H - 1)
        r_, g_, b_ = px[rx, ry]
        nz = random.randint(-4, 4)
        px[rx, ry] = (max(0, min(255, r_ + nz)), max(0, min(255, g_ + nz)), max(0, min(255, b_ + nz)))

    img.save(f"{OUT}/{fname}")
    return fname

# (n_visible, typing, caption2, hold)
SEQ = [
    (1,  False, False, 0.7),   # R: sit tight, breaking you out
    (2,  False, False, 0.8),   # H: who is this
    (3,  False, False, 1.0),   # R: cell B-24601
    (4,  False, False, 1.2),   # H: how do you have my cell number
    (5,  False, False, 1.2),   # Bluey: watchtower cannon
    (6,  False, False, 0.9),   # H: the watchtower has a cannon??
    (7,  False, False, 1.0),   # Bluey: not for much longer
    (8,  False, False, 1.2),   # R: try to look rescued
    (9,  False, False, 1.4),   # H: death row / better life expectancy
    (10, False, False, 1.2),   # H: fewer explosions. more regular meals
    (11, False, False, 0.9),   # R: about that
    (12, False, False, 1.1),   # Bluey: move away from the east wall
    (12, True,  False, 0.5),   # Henrik typing (panic)
    (13, False, False, 0.9),   # H: WHICH wall  -> then BOOM
]

with open(f"{OUT}/ag_frames.txt", "w") as fl:
    for i, (n, t, c2, hold) in enumerate(SEQ):
        fn = render_state(n, t, c2, f"ag_frame_{i:02d}.png")
        fl.write(f"file '{OUT}/{fn}'\nduration {hold}\n")
    fl.write(f"file '{OUT}/boom_flash.png'\nduration 0.12\n")
    fl.write(f"file '{OUT}/boom_fire.png'\nduration 0.9\n")
    fl.write(f"file '{OUT}/boom_fire.png'\n")

print(f"rendered {len(SEQ)} frames, main {sum(s[3] for s in SEQ):.1f}s, "
      f"final content_h {content_height(10, False)} vs view {VIEW_BOTTOM-VIEW_TOP}")
