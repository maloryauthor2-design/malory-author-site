#!/usr/bin/env python3
"""Morgan & Merlin title card — brand spec from BRAND_FOUNDATION.md.
Kicker + Malory wordmark (Fraunces 600) + brass rule, cover hero with
brass hairline + shadow, deep-violet series strip, follower-growth CTA.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
SITE = "/sessions/determined-focused-wright/mnt/malory-author-website"
FONTS = f"{SITE}/brand/fonts"

PRIMARY_DEEP = (13, 16, 21)      # 0D1015
CREAM = (232, 224, 204)          # E8E0CC
BRASS = (201, 168, 90)           # C9A85A
BRASS_BRIGHT = (224, 196, 120)   # E0C478
MUTED = (154, 160, 168)          # 9AA0A8
VIOLET = (91, 58, 122)           # 5B3A7A — Morgan & Merlin anchor

def fraunces(size, wght=600):
    f = ImageFont.truetype(f"{FONTS}/Fraunces-VF.ttf", size)
    # axes: [Optical Size 9-144, Weight 100-900, Softness 0-100, Wonky 0-1]
    f.set_variation_by_axes([144, wght, 0, 1])
    return f

def inter(size, semi=False):
    p = f"{FONTS}/Inter-SemiBold-static.ttf" if semi else f"{FONTS}/Inter-Medium-static.ttf"
    return ImageFont.truetype(p, size)

def tracked(draw, xy, text, font, fill, tracking):
    """draw text with manual letter-spacing; returns total width"""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking
    return x - xy[0] - tracking

def tracked_width(draw, text, font, tracking):
    return sum(draw.textlength(c, font=font) for c in text) + tracking * (len(text) - 1)

img = Image.new("RGB", (W, H), PRIMARY_DEEP)
d = ImageDraw.Draw(img)

# ---- top band: kicker + wordmark + brass rule ----
f_kick = inter(33, semi=True)
kick = "MORGAN & MERLIN  ·  BOOK ONE"
ktrk = 6
kw = tracked_width(d, kick, f_kick, ktrk)
tracked(d, ((W - kw) / 2, 128), kick, f_kick, MUTED, ktrk)

f_word = fraunces(104, 600)
word = "Malory"
wtrk = int(104 * 0.04)
ww = tracked_width(d, word, f_word, wtrk)
tracked(d, ((W - ww) / 2, 196), word, f_word, CREAM, wtrk)

rule_w = int(ww * 0.6)
ry = 348
d.rectangle(((W - rule_w) / 2, ry, (W + rule_w) / 2, ry + 3), fill=BRASS)

# ---- cover hero with shadow + brass hairline ----
cover = Image.open(f"{SITE}/welcome-cover.jpg").convert("RGB")
CW = 640
CH = int(CW * cover.height / cover.width)  # 640x1024
cover = cover.resize((CW, CH), Image.LANCZOS)
cx, cy = (W - CW) // 2, 420

shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.rectangle((cx - 10, cy + 18, cx + CW + 10, cy + CH + 38), fill=(0, 0, 0, 170))
shadow = shadow.filter(ImageFilter.GaussianBlur(28))
img = Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB")
img.paste(cover, (cx, cy))
d = ImageDraw.Draw(img)
d.rectangle((cx - 2, cy - 2, cx + CW + 1, cy + CH + 1), outline=BRASS, width=2)

# ---- series anchor strip ----
sy = cy + CH + 44
d.rectangle((cx, sy, cx + CW, sy + 10), fill=VIOLET)

# ---- CTA block ----
f_cta = inter(42, semi=True)
cta = "follow for more from the dark ages"
cw_ = d.textlength(cta, font=f_cta)
d.text(((W - cw_) / 2, sy + 54), cta, font=f_cta, fill=BRASS_BRIGHT)

f_sub = inter(30)
sub = "available now  ·  link in bio"
sw = d.textlength(sub, font=f_sub)
d.text(((W - sw) / 2, sy + 130), sub, font=f_sub, fill=MUTED)

img.save("/sessions/determined-focused-wright/mnt/outputs/mm_titlecard.png")
print("saved mm_titlecard.png", img.size, "cover", CW, CH, "strip_y", sy)
