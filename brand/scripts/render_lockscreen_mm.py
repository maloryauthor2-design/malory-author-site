#!/usr/bin/env python3
"""Morgan & Merlin LOCK SCREEN Reel — progressive-reveal frame renderer.

The density test: same ch12 Whoopass scene as the 600-view iMessage trial,
rebuilt as an iOS lock screen receiving three notifications. One variable
changed vs the winner (format/density). Static stills only — no keyframes;
same concat-demuxer MP4 workflow as every other reel.

Notifications appear newest-on-top (real lock-screen behaviour):
  1. Messages / Merlin — the solemn naming lecture        (verbatim ch12)
  2. CULTIVATION SYSTEM — [Can of Whoopass] technique named (verbatim ch12)
  3. Messages / Merlin — "You could not help yourself, could you?" (verbatim)
"""
from PIL import Image, ImageDraw, ImageFont
import random

W, H = 1080, 1920
REPO = "/sessions/youthful-epic-lovelace/mnt/malory-author-website"
FONTS = f"{REPO}/brand/fonts"
OUT = "/sessions/youthful-epic-lovelace/mnt/outputs"

INTER_MED = f"{FONTS}/Inter-Medium-static.ttf"
INTER_SEMI = f"{FONTS}/Inter-SemiBold-static.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

CANVAS = (5, 5, 7)
CARD_OUTLINE = (40, 40, 44)
TXT_WHITE = (245, 245, 247)
TXT_GRAY = (152, 152, 160)
NOTIF_BG = (42, 42, 48)
MSG_GREEN = (52, 199, 89)
MM_VIOLET = (91, 58, 122)      # Morgan & Merlin series anchor #5B3A7A

CAPTION_1 = "merlin waited 1,500 years for an heir."
CAPTION_2 = "she chose with great care."

def F(p, s): return ImageFont.truetype(p, s)

f_cap = F(INTER_SEMI, 44)
f_clock = F(INTER_SEMI, 168)
f_date = F(INTER_MED, 40)
f_app = F(INTER_MED, 26)
f_time = F(INTER_MED, 26)
f_title = F(INTER_SEMI, 34)
f_body = F(INTER_MED, 34)
f_mono = F(MONO, 31)

CARD_W = 920
CARD_X = (W - CARD_W) // 2
CARD_Y, CARD_H = 285, 1480
NOTIF_W = CARD_W - 72
NOTIF_X = CARD_X + 36
BODY_LH = 44

# (app, title, body, mono) — newest gets drawn on top of the stack
NOTIFS = [
    ("Messages", "Merlin",
     "A technique's name defines a cultivator's legend for centuries. Choose with great care.", False),
    ("CULTIVATION SYSTEM", None,
     "[Can of Whoopass] technique named", True),
    ("Messages", "Merlin",
     "You could not help yourself, could you?", False),
]

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
MEASURED = []
for app, title, body, mono in NOTIFS:
    fnt = f_mono if mono else f_body
    lines = wrap(probe, body, fnt, NOTIF_W - 200)
    h = 30 + 38 + (10 + 44 if title else 6) + len(lines) * BODY_LH + 26
    MEASURED.append({"app": app, "title": title, "lines": lines,
                     "mono": mono, "h": h, "font": fnt})

def draw_msg_icon(d, x, y, s=64):
    d.rounded_rectangle((x, y, x + s, y + s), radius=15, fill=MSG_GREEN)
    bx0, by0, bx1, by1 = x + 11, y + 14, x + s - 11, y + s - 22
    d.rounded_rectangle((bx0, by0, bx1, by1), radius=14, fill=(255, 255, 255))
    d.polygon([(x + 20, by1 - 4), (x + 20, by1 + 10), (x + 34, by1 - 4)], fill=(255, 255, 255))

def draw_sys_icon(d, x, y, s=64):
    d.rounded_rectangle((x, y, x + s, y + s), radius=15, fill=MM_VIOLET)
    cx, cy = x + s / 2, y + s / 2
    r = 17
    d.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)],
              outline=(255, 255, 255), width=4)
    d.ellipse((cx - 4, cy - 4, cx + 4, cy + 4), fill=(255, 255, 255))

def draw_notif(d, m, y):
    d.rounded_rectangle((NOTIF_X, y, NOTIF_X + NOTIF_W, y + m["h"]),
                        radius=34, fill=NOTIF_BG)
    ix, iy = NOTIF_X + 26, y + 28
    if m["app"] == "Messages":
        draw_msg_icon(d, ix, iy)
    else:
        draw_sys_icon(d, ix, iy)
    tx = ix + 64 + 24
    hy = y + 30
    d.text((tx, hy), m["app"].upper() if m["app"] != "Messages" else "MESSAGES",
           font=f_app, fill=TXT_GRAY)
    nw = d.textlength("now", font=f_time)
    d.text((NOTIF_X + NOTIF_W - 28 - nw, hy), "now", font=f_time, fill=TXT_GRAY)
    yy = hy + 38
    if m["title"]:
        d.text((tx, yy + 10), m["title"], font=f_title, fill=TXT_WHITE)
        yy += 10 + 44
    else:
        yy += 6
    for l in m["lines"]:
        d.text((tx, yy), l, font=f_mono if m["mono"] else f_body, fill=TXT_WHITE)
        yy += BODY_LH
    return y + m["h"]

def render_state(n_visible, caption2, fname):
    img = Image.new("RGB", (W, H), CANVAS)
    d = ImageDraw.Draw(img)

    # caption block (matches the iMessage reel treatment)
    cy = 152
    lw = d.textlength(CAPTION_1, font=f_cap)
    d.text(((W - lw) / 2, cy), CAPTION_1, font=f_cap, fill=TXT_WHITE)
    if caption2:
        lw2 = d.textlength(CAPTION_2, font=f_cap)
        d.text(((W - lw2) / 2, cy + 58), CAPTION_2, font=f_cap, fill=TXT_WHITE)

    # phone card with a faint violet-black wallpaper gradient
    card = Image.new("RGB", (CARD_W, CARD_H), (0, 0, 0))
    cd = ImageDraw.Draw(card)
    for yy in range(CARD_H):
        t = yy / CARD_H
        cd.line([(0, yy), (CARD_W, yy)],
                fill=(int(16 * (1 - t) + 4 * t), int(10 * (1 - t) + 4 * t), int(24 * (1 - t) + 8 * t)))
    img.paste(card, (CARD_X, CARD_Y))
    d.rounded_rectangle((CARD_X, CARD_Y, CARD_X + CARD_W, CARD_Y + CARD_H),
                        radius=52, outline=CARD_OUTLINE, width=2)
    # mask the gradient corners back to canvas
    # (cheap: redraw rounded outline over a canvas-colored corner frame)
    corner = Image.new("RGB", (W, H), CANVAS)
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((CARD_X, CARD_Y, CARD_X + CARD_W, CARD_Y + CARD_H), radius=52, fill=255)
    img = Image.composite(img, corner, mask)
    d = ImageDraw.Draw(img)
    # re-draw caption (composite wiped nothing above the card, but be safe)
    d.text(((W - lw) / 2, cy), CAPTION_1, font=f_cap, fill=TXT_WHITE)
    if caption2:
        d.text(((W - lw2) / 2, cy + 58), CAPTION_2, font=f_cap, fill=TXT_WHITE)
    d.rounded_rectangle((CARD_X, CARD_Y, CARD_X + CARD_W, CARD_Y + CARD_H),
                        radius=52, outline=CARD_OUTLINE, width=2)

    # status glyphs top-right: signal dots, wifi, battery
    sx, sy = CARD_X + CARD_W - 150, CARD_Y + 34
    for i in range(4):
        bh = 8 + i * 6
        d.rounded_rectangle((sx + i * 13, sy + 26 - bh, sx + i * 13 + 8, sy + 26),
                            radius=2, fill=TXT_WHITE if i < 3 else (90, 90, 96))
    wx = sx + 62
    for r_, wdt in ((22, 4), (14, 4), (5, 5)):
        d.arc((wx - r_, sy + 4 - r_ + 22, wx + r_, sy + 4 + r_ + 22),
              start=225, end=315, fill=TXT_WHITE, width=wdt)
    bx = sx + 92
    d.rounded_rectangle((bx, sy + 4, bx + 44, sy + 26), radius=7, outline=TXT_WHITE, width=3)
    d.rounded_rectangle((bx + 4, sy + 8, bx + 32, sy + 22), radius=3, fill=TXT_WHITE)
    d.rounded_rectangle((bx + 46, sy + 11, bx + 50, sy + 19), radius=2, fill=TXT_WHITE)

    # padlock
    pcx, pcy = W // 2, CARD_Y + 120
    d.rounded_rectangle((pcx - 17, pcy - 2, pcx + 17, pcy + 24), radius=8, fill=TXT_WHITE)
    d.arc((pcx - 12, pcy - 22, pcx + 12, pcy + 4), start=180, end=0, fill=TXT_WHITE, width=5)

    # date + clock
    date_s = "Thursday, 537 AD"
    dw = d.textlength(date_s, font=f_date)
    d.text(((W - dw) / 2, CARD_Y + 168), date_s, font=f_date, fill=TXT_WHITE)
    clock_s = "5:37"
    cw = d.textlength(clock_s, font=f_clock)
    d.text(((W - cw) / 2, CARD_Y + 212), clock_s, font=f_clock, fill=TXT_WHITE)

    # notification stack — newest on top
    y = CARD_Y + 560
    visible = MEASURED[:n_visible]
    for m in reversed(visible):
        y = draw_notif(d, m, y) + 16

    # flashlight + camera + home bar
    fy = CARD_Y + CARD_H - 150
    for cx_ in (CARD_X + 130, CARD_X + CARD_W - 130):
        d.ellipse((cx_ - 44, fy - 44, cx_ + 44, fy + 44), fill=(34, 34, 40))
    fcx = CARD_X + 130
    d.polygon([(fcx - 10, fy - 18), (fcx + 10, fy - 18), (fcx + 6, fy - 2),
               (fcx - 6, fy - 2)], fill=TXT_WHITE)
    d.rounded_rectangle((fcx - 6, fy - 2, fcx + 6, fy + 18), radius=3, fill=TXT_WHITE)
    ccx = CARD_X + CARD_W - 130
    d.rounded_rectangle((ccx - 20, fy - 14, ccx + 20, fy + 14), radius=8, outline=TXT_WHITE, width=4)
    d.ellipse((ccx - 7, fy - 7, ccx + 7, fy + 7), outline=TXT_WHITE, width=4)
    d.rounded_rectangle((W // 2 - 110, CARD_Y + CARD_H - 38, W // 2 + 110, CARD_Y + CARD_H - 28),
                        radius=5, fill=(220, 220, 225))

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

# ---- reveal sequence: (n_visible, caption2, hold seconds) ----
SEQUENCE = [
    (0, False, 0.9),   # empty lock screen — the artifact registers
    (1, False, 2.8),   # the solemn naming lecture
    (2, False, 1.7),   # [Can of Whoopass] pops on top — instant
    (3, False, 1.9),   # "You could not help yourself, could you?"
    (3, True,  2.2),   # "she chose with great care."
]

with open(f"{OUT}/ls_frames.txt", "w") as fl:
    for i, (n, c2, hold) in enumerate(SEQUENCE):
        fn = render_state(n, c2, f"mm_ls_frame_{i:02d}.png")
        fl.write(f"file '{OUT}/{fn}'\nduration {hold}\n")
    fl.write(f"file '{OUT}/mm_ls_frame_{len(SEQUENCE)-1:02d}.png'\n")

print(f"rendered {len(SEQUENCE)} frames, main duration {sum(s[2] for s in SEQUENCE):.1f}s")
