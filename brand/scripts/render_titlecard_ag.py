#!/usr/bin/env python3
"""Arcane Galaxy title card — brand spec, Jake Malory sub-identity.
Jake (Fraunces 400) over Malory (Fraunces 600), Troy Osgood co-author credit,
electric-blue series anchor (#3D7FB8), arcane-1.jpg hero with brass hairline.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
SITE = "/sessions/determined-focused-wright/mnt/malory-author-website"
FONTS = f"{SITE}/brand/fonts"

PRIMARY_DEEP = (13, 16, 21)
CREAM = (232, 224, 204)
BRASS = (201, 168, 90)
BRASS_BRIGHT = (224, 196, 120)
MUTED = (154, 160, 168)
ELECTRIC = (61, 127, 184)     # 3D7FB8 — Arcane Galaxy anchor

def fraunces(size, wght=600):
    f = ImageFont.truetype(f"{FONTS}/Fraunces-VF.ttf", size)
    f.set_variation_by_axes([144, wght, 0, 1])  # opsz, wght, soft, wonk
    return f

def inter(size, semi=False):
    p = f"{FONTS}/Inter-SemiBold-static.ttf" if semi else f"{FONTS}/Inter-Medium-static.ttf"
    return ImageFont.truetype(p, size)

def tw(d, t, f, trk):
    return sum(d.textlength(c, font=f) for c in t) + trk * (len(t) - 1)

def tracked(d, xy, text, font, fill, trk):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + trk

img = Image.new("RGB", (W, H), PRIMARY_DEEP)
d = ImageDraw.Draw(img)

# kicker
f_kick = inter(33, semi=True)
kick = "ARCANE GALAXY  ·  BOOK ONE"
ktrk = 6
d_w = tw(d, kick, f_kick, ktrk)
tracked(d, ((W - d_w) / 2, 120), kick, f_kick, MUTED, ktrk)

# Jake Malory stacked lockup
f_jake = fraunces(58, 400)
jw = d.textlength("Jake", font=f_jake)
d.text(((W - jw) / 2, 172), "Jake", font=f_jake, fill=CREAM)
f_word = fraunces(100, 600)
mtrk = int(100 * 0.04)
mw = tw(d, "Malory", f_word, mtrk)
tracked(d, ((W - mw) / 2, 230), "Malory", f_word, CREAM, mtrk)

# co-author credit
f_co = inter(29)
co = "with Troy Osgood"
cw = d.textlength(co, font=f_co)
d.text(((W - cw) / 2, 356), co, font=f_co, fill=MUTED)

# brass rule
rule_w = int(mw * 0.6)
d.rectangle(((W - rule_w) / 2, 408, (W + rule_w) / 2, 411), fill=BRASS)

# cover hero with shadow + brass hairline
cover = Image.open(f"{SITE}/arcane-1.jpg").convert("RGB")
CW = 624
CH = int(CW * cover.height / cover.width)   # ~939
cover = cover.resize((CW, CH), Image.LANCZOS)
cx, cy = (W - CW) // 2, 452

shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.rectangle((cx - 10, cy + 18, cx + CW + 10, cy + CH + 38), fill=(0, 0, 0, 170))
shadow = shadow.filter(ImageFilter.GaussianBlur(28))
img = Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB")
img.paste(cover, (cx, cy))
d = ImageDraw.Draw(img)
d.rectangle((cx - 2, cy - 2, cx + CW + 1, cy + CH + 1), outline=BRASS, width=2)

# electric-blue series anchor strip
sy = cy + CH + 40
d.rectangle((cx, sy, cx + CW, sy + 10), fill=ELECTRIC)

# CTA
f_cta = inter(42, semi=True)
cta = "follow for more from the Gazelle"
cw2 = d.textlength(cta, font=f_cta)
d.text(((W - cw2) / 2, sy + 50), cta, font=f_cta, fill=BRASS_BRIGHT)

f_sub = inter(30)
sub = "book one out now  ·  link in bio"
sw = d.textlength(sub, font=f_sub)
d.text(((W - sw) / 2, sy + 124), sub, font=f_sub, fill=MUTED)

img.save("/sessions/determined-focused-wright/mnt/outputs/ag_titlecard.png")
print("saved ag_titlecard.png", img.size, "cover", CW, CH, "strip_y", sy)
