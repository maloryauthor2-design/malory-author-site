#!/usr/bin/env python3
"""THE MORGAN SHOW — movie-poster cover ("Dark Age Playbill").
One-sheet grammar played straight: hero art (full-res WTTDA cover, cropped
above the baked title lettering), star pull-quotes from canon, kicker, big
Fraunces title, tagline in tracked caps, condensed billing block, Malory
lockup, violet anchor strip. 1080x1920 + 1080x1080.
"""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import random

REPO = "/sessions/youthful-epic-lovelace/mnt/malory-author-website"
FONTS = f"{REPO}/brand/fonts"
OUT = "/sessions/youthful-epic-lovelace/mnt/outputs"
COVER = "/sessions/youthful-epic-lovelace/mnt/Downloads/book-links-app/public/welcome-cover.JPG"

DEEP = (13, 16, 21)
CREAM = (232, 224, 204)
BRASS = (201, 168, 90)
MUTED = (154, 160, 168)
TEXT = (230, 230, 234)
VIOLET = (91, 58, 122)
VIOLET_LT = (139, 102, 173)

def F(p, s, var=None):
    f = ImageFont.truetype(p, s)
    if var: f.set_variation_by_axes(var)
    return f

fraunces = lambda s: F(f"{FONTS}/Fraunces-VF.ttf", s, [144, 600, 0, 1])
inter_m = lambda s: F(f"{FONTS}/Inter-Medium-static.ttf", s)
inter_sb = lambda s: F(f"{FONTS}/Inter-SemiBold-static.ttf", s)
dejavu = lambda s: F("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", s)

QUOTES = [
    ("★★★★★", "“a f***ing liberty.”", "— Vortigern’s Dragon"),
    ("★★★★★", "“That was a joke.”", "— Merlin"),
]
KICKER = "A COMEDY FROM THE DARK AGES"
TITLE = "The Morgan Show"
TAGLINE = "SHE IS BECOMING MORGAN LE FAY.  ONE TEXT AT A TIME."
BILLING = [
    "MALORY PRESENTS A DARK AGES PRODUCTION “THE MORGAN SHOW”",
    "STARRING MORGAN LE FAY AND THE DISEMBODIED VOICE OF MERLIN",
    "BASED ON THE NOVEL “WELCOME TO THE DARK AGES” · NEW EPISODES MON WED FRI · INSTAGRAM & TIKTOK",
]

def tracked(d, cx, y, s, font, fill, tracking=7):
    w = sum(d.textlength(ch, font=font) for ch in s) + tracking * (len(s) - 1)
    x = cx - w / 2
    for ch in s:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + tracking
    return w

def condensed_line(s, font_size, squeeze=0.66, fill=MUTED):
    f = inter_sb(font_size)
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    w = int(probe.textlength(s, font=f)) + 8
    h = font_size + 12
    tmp = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    td.text((4, 2), s, font=f, fill=fill + (255,))
    return tmp.resize((int(w * squeeze), h), Image.LANCZOS)

def hero(W, H, art_bottom):
    """Crop the cover art (above its baked lettering) to fill W x art_bottom+overlap."""
    src = Image.open(COVER).convert("RGB")          # 1600x2560
    crop = src.crop((180, 270, 1600, 1340))         # dragons + Morgan, no lettering
    target_h = art_bottom + 260                     # extra for the gradient melt
    ratio = W / target_h
    cw, ch = crop.size
    if cw / ch > ratio:
        nw = int(ch * ratio)
        x0 = int(cw * 0.56) - nw // 2               # bias toward Morgan (right of centre)
        x0 = max(0, min(cw - nw, x0))
        crop = crop.crop((x0, 0, x0 + nw, ch))
    else:
        nh = int(cw / ratio)
        crop = crop.crop((0, 0, cw, nh))
    img = crop.resize((W, target_h), Image.LANCZOS)
    img = ImageEnhance.Color(img).enhance(0.92)
    img = ImageEnhance.Brightness(img).enhance(0.96)
    return img

def grade(img, W, H, art_bottom):
    """Melt the art into DEEP from melt_start to art_bottom; subtle top grade."""
    ov = Image.new("L", (W, img.height), 0)
    od = ImageDraw.Draw(ov)
    melt_start = art_bottom - 330
    for y in range(melt_start, img.height):
        t = min(1.0, (y - melt_start) / 330)
        od.line([(0, y), (W, y)], fill=int(255 * (t ** 1.4)))
    for y in range(0, 420):
        t = (420 - y) / 420
        od.line([(0, y), (W, y)], fill=int(215 * t ** 1.35))
    deep = Image.new("RGB", img.size, DEEP)
    return Image.composite(deep, img, ov)

def render(W, H, fname, sq=False):
    art_bottom = int(H * (0.60 if not sq else 0.52))
    canvas = Image.new("RGB", (W, H), DEEP)
    art = grade(hero(W, H, art_bottom), W, H, art_bottom)
    canvas.paste(art.crop((0, 0, W, min(art.height, H))), (0, 0))
    d = ImageDraw.Draw(canvas)
    cx = W // 2

    # star pull-quotes over the sky
    qy = int(H * 0.028)
    f_star = dejavu(30 if not sq else 26)
    f_q = inter_sb(33 if not sq else 29)
    f_attr = inter_m(26 if not sq else 23)
    for stars, quote, attr in QUOTES:
        sw = d.textlength(stars, font=f_star)
        d.text((cx - sw / 2, qy), stars, font=f_star, fill=BRASS)
        qw = d.textlength(quote, font=f_q)
        d.text((cx - qw / 2, qy + 40), quote, font=f_q, fill=CREAM)
        aw = d.textlength(attr, font=f_attr)
        d.text((cx - aw / 2, qy + 86), attr, font=f_attr, fill=(202, 202, 208))
        qy += 138 if not sq else 124

    # kicker
    ky = art_bottom - 36
    tracked(d, cx, ky, KICKER, inter_sb(27 if not sq else 25), MUTED)

    # title
    f_t = fraunces(124 if not sq else 96)
    tw = d.textlength(TITLE, font=f_t)
    ty = ky + 44
    d.text((cx - tw / 2, ty), TITLE, font=f_t, fill=CREAM)

    # violet rule
    ry = ty + (172 if not sq else 136)
    d.rectangle((cx - W * 0.16, ry, cx + W * 0.16, ry + 4), fill=VIOLET_LT)

    # tagline
    tgy = ry + (44 if not sq else 36)
    tracked(d, cx, tgy, TAGLINE, inter_sb(27 if not sq else 23), TEXT, tracking=3)

    # billing block
    by = tgy + (110 if not sq else 84)
    for line in BILLING:
        bl = condensed_line(line, 29 if not sq else 25, squeeze=0.6)
        canvas.paste(bl, (cx - bl.width // 2, by), bl)
        by += (46 if not sq else 40)
    d = ImageDraw.Draw(canvas)

    # Malory lockup
    f_a = fraunces(62 if not sq else 50)
    aw = d.textlength("Malory", font=f_a)
    ay = int(H * (0.905 if not sq else 0.885))
    d.text((cx - aw / 2, ay), "Malory", font=f_a, fill=CREAM)
    rw = aw * 0.6
    d.rectangle((cx - rw / 2, ay + (84 if not sq else 68), cx + rw / 2, ay + (85 if not sq else 69)), fill=BRASS)

    # anchor strip + grain
    d.rectangle((0, H - 14, W, H), fill=VIOLET)
    random.seed(537)
    px = canvas.load()
    for _ in range(16000):
        x_, y_ = random.randint(0, W - 1), random.randint(0, H - 1)
        r_, g_, b_ = px[x_, y_]
        n = random.randint(-4, 4)
        px[x_, y_] = (max(0, min(255, r_ + n)), max(0, min(255, g_ + n)), max(0, min(255, b_ + n)))

    canvas.save(f"{OUT}/{fname}")

render(1080, 1920, "morgan_show_poster_1080x1920.png")
render(1080, 1080, "morgan_show_poster_1080x1080.png", sq=True)
print("done")
