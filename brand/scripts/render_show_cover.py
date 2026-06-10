#!/usr/bin/env python3
"""THE MORGAN SHOW — show cover / series identity card.
Brand surface (NOT a reel artifact frame), so it uses the brand palette per
BRAND_FOUNDATION.md: primary-deep canvas, Fraunces display, cream display text,
M&M violet series anchor, brass for the author lockup. Bubble motif signals the
format. Outputs: 1080x1920 (reel/series cover; critical content in the centre
crop zone) and 1080x1080 (grid/playlist).
"""
from PIL import Image, ImageDraw, ImageFont
import random

REPO = "/sessions/youthful-epic-lovelace/mnt/malory-author-website"
FONTS = f"{REPO}/brand/fonts"
OUT = "/sessions/youthful-epic-lovelace/mnt/outputs"

DEEP = (13, 16, 21)        # 0D1015
CREAM = (232, 224, 204)    # E8E0CC
BRASS = (201, 168, 90)     # C9A85A
MUTED = (154, 160, 168)    # 9AA0A8
TEXT = (230, 230, 234)     # E6E6EA
VIOLET = (91, 58, 122)     # 5B3A7A
VIOLET_LT = (139, 102, 173)
BUBBLE_GRAY = (38, 38, 42)
BUBBLE_BLUE = (10, 132, 255)

def F(p, s, var=None):
    f = ImageFont.truetype(p, s)
    if var:
        f.set_variation_by_axes(var)
    return f

fraunces = lambda s: F(f"{FONTS}/Fraunces-VF.ttf", s, [144, 600, 0, 1])
inter_m = lambda s: F(f"{FONTS}/Inter-Medium-static.ttf", s)
inter_sb = lambda s: F(f"{FONTS}/Inter-SemiBold-static.ttf", s)

def kicker_text(d, x, y, s, font, fill, tracking=8):
    cx = x
    for ch in s:
        d.text((cx, y), ch, font=font, fill=fill)
        cx += d.textlength(ch, font=font) + tracking
    return cx - tracking - x

def kicker_width(d, s, font, tracking=8):
    return sum(d.textlength(ch, font=font) for ch in s) + tracking * (len(s) - 1)

def bubble(d, text, font, x, y, side, W):
    tw = d.textlength(text, font=font)
    bw, bh = int(tw + 60), int(font.size + 42)
    if side == "r":
        x0 = x - bw
        color = BUBBLE_BLUE
    else:
        x0 = x
        color = BUBBLE_GRAY
    d.rounded_rectangle((x0, y, x0 + bw, y + bh), radius=int(bh / 2), fill=color)
    d.text((x0 + 30, y + 19), text, font=font, fill=(255, 255, 255))
    return y + bh

def render(W, H, fname):
    img = Image.new("RGB", (W, H), DEEP)
    d = ImageDraw.Draw(img)
    cx = W // 2
    sq = H == W
    top = int(H * (0.10 if sq else 0.285))

    # kicker
    f_k = inter_sb(26 if sq else 28)
    ks = "A COMEDY FROM THE DARK AGES"
    kw = kicker_width(d, ks, f_k)
    kicker_text(d, cx - kw / 2, top, ks, f_k, MUTED)

    # title
    f_t = fraunces(96 if sq else 108)
    ts = "The Morgan Show"
    tw = d.textlength(ts, font=f_t)
    ty = top + 56
    d.text((cx - tw / 2, ty), ts, font=f_t, fill=CREAM)

    # violet rule
    ry = ty + (140 if sq else 156)
    d.rectangle((cx - W * 0.18, ry, cx + W * 0.18, ry + 4), fill=VIOLET_LT)

    # bubble motif
    f_b = inter_m(34 if sq else 36)
    bx_l = int(W * 0.14)
    bx_r = int(W * 0.86)
    by = ry + (50 if sq else 70)
    by = bubble(d, "Don't move.", f_b, bx_l, by, "l", W) + 22
    by = bubble(d, "what do you want with my dead arse?", f_b, bx_r, by, "r", W) + 22
    by = bubble(d, "My name is Merlin.", f_b, bx_l, by, "l", W)

    # tagline
    f_tag = inter_m(36 if sq else 40)
    tag = "she is becoming Morgan le Fay. one text at a time."
    tgw = d.textlength(tag, font=f_tag)
    tgy = by + (54 if sq else 70)
    d.text((cx - tgw / 2, tgy), tag, font=f_tag, fill=TEXT)

    # book line
    f_bk = inter_m(27 if sq else 29)
    bk = "from WELCOME TO THE DARK AGES · book one out now"
    bkw = d.textlength(bk, font=f_bk)
    d.text((cx - bkw / 2, tgy + (58 if sq else 66)), bk, font=f_bk, fill=MUTED)

    # author lockup bottom: Malory in Fraunces cream + brass rule
    f_a = fraunces(56 if sq else 64)
    aw = d.textlength("Malory", font=f_a)
    ay = int(H * (0.86 if sq else 0.875))
    d.text((cx - aw / 2, ay), "Malory", font=f_a, fill=CREAM)
    rw = aw * 0.6
    d.rectangle((cx - rw / 2, ay + (76 if sq else 86), cx + rw / 2, ay + (77 if sq else 87)), fill=BRASS)

    # series anchor strip
    d.rectangle((0, H - 14, W, H), fill=VIOLET)

    # grain
    random.seed(537)
    px = img.load()
    for _ in range(10000):
        x_, y_ = random.randint(0, W - 1), random.randint(0, H - 1)
        r_, g_, b_ = px[x_, y_]
        n = random.randint(-3, 3)
        px[x_, y_] = (max(0, min(255, r_ + n)), max(0, min(255, g_ + n)), max(0, min(255, b_ + n)))

    img.save(f"{OUT}/{fname}")

render(1080, 1920, "morgan_show_cover_1080x1920.png")
render(1080, 1080, "morgan_show_cover_1080x1080.png")
print("done")
