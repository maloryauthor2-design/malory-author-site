#!/usr/bin/env python3
"""Morgan & Merlin — '537 AD Wrapped' stat card, progressive reveal.
Year-in-review music-stats format (Spotify Wrapped homage, no logo/trademark).
Full-bleed violet duotone, stats pop in one block at a time. Native-artifact
frame breaks brand palette on purpose (like the receipt/AITA/iOS frames);
the on-brand title card closes the reel.
"""
from PIL import Image, ImageDraw, ImageFont
import random

W, H = 1080, 1920
GF = "/usr/share/fonts/truetype/google-fonts"
OUT = "/sessions/determined-focused-wright/mnt/outputs"

# vivid Wrapped duotone, anchored to the M&M violet (#5B3A7A brightened)
VIOLET     = (107, 63, 160)    # 6B3FA0 full-bleed base
VIOLET_DK  = (74, 41, 112)     # 4A2970 recessed blocks
GOLD       = (240, 200, 110)   # bright warm accent (big numbers, #1 marks)
CORAL      = (255, 122, 102)   # secondary pop (top song)
CREAM      = (244, 238, 222)   # body text
CREAM_DIM  = (206, 192, 220)   # muted labels (violet-tinted)

def P(weight, size):
    return ImageFont.truetype(f"{GF}/Poppins-{weight}.ttf", size)

f_kick   = P("Medium", 34)
f_wrap   = P("Bold", 132)
f_label  = P("Bold", 38)
f_num    = P("Bold", 168)
f_value  = P("Bold", 92)
f_genre  = P("Bold", 60)
f_rank   = P("Bold", 60)
f_song   = P("Bold", 66)
f_snark  = P("MediumItalic", 37)
f_foot   = P("Medium", 42)
f_aura   = P("Bold", 64)

def tlen(d, t, f):
    return d.textlength(t, font=f)

def tracked(d, xy, text, font, fill, trk):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + trk
    return x - trk

# ---- block painters: each returns the new y cursor ----
def block_minutes(d, x, y):
    d.text((x, y), "MINUTES LISTENED", font=f_label, fill=CREAM_DIM)
    y += 48
    d.text((x, y), "12,043", font=f_num, fill=GOLD)
    y += 184
    d.text((x, y), "you couldn't skip one. he's in your skull.", font=f_snark, fill=CREAM)
    return y + 66

def block_artist(d, x, y):
    d.text((x, y), "TOP ARTIST", font=f_label, fill=CREAM_DIM)
    y += 48
    d.text((x, y), "Merlin", font=f_value, fill=CREAM)
    y += 104
    d.text((x, y), "called you 'my dear' 103 times", font=f_snark, fill=CREAM)
    return y + 70

def block_genres(d, x, y):
    d.text((x, y), "TOP GENRES", font=f_label, fill=CREAM_DIM)
    y += 56
    rows = ["Cultivation", "Mansplaining (Ancient)", "Impending Doom"]
    for i, g in enumerate(rows, 1):
        d.text((x, y), str(i), font=f_rank, fill=GOLD)
        d.text((x + 64, y), g, font=f_genre, fill=CREAM)
        y += 74
    return y + 24

def block_song(d, x, y):
    d.text((x, y), "TOP SONG", font=f_label, fill=CREAM_DIM)
    y += 50
    d.text((x, y), "Fireball", font=f_song, fill=CORAL)
    y += 72
    d.text((x, y), "(feat. one crow)", font=f_song, fill=CORAL)
    return y + 78

BLOCKS = [block_minutes, block_artist, block_genres, block_song]

def render_state(n_blocks, show_foot, fname):
    img = Image.new("RGB", (W, H), VIOLET)
    d = ImageDraw.Draw(img)

    # subtle top-to-bottom deepening for depth
    for yy in range(H):
        t = yy / H
        r = int(VIOLET[0] * (1 - 0.18 * t) + VIOLET_DK[0] * 0.18 * t)
        g = int(VIOLET[1] * (1 - 0.18 * t) + VIOLET_DK[1] * 0.18 * t)
        b = int(VIOLET[2] * (1 - 0.18 * t) + VIOLET_DK[2] * 0.18 * t)
        d.line([(0, yy), (W, yy)], fill=(r, g, b))

    MX = 96  # left margin
    # ---- header ----
    d.text((MX, 118), "@morgan_lefay", font=f_kick, fill=CREAM)
    d.text((MX, 176), "537 AD", font=f_wrap, fill=GOLD)
    d.text((MX, 312), "WRAPPED", font=f_wrap, fill=CREAM)

    # gold rule under header
    d.rectangle((MX, 478, MX + 360, 484), fill=GOLD)

    y = 540
    for i in range(n_blocks):
        y = BLOCKS[i](d, MX, y)

    if show_foot:
        fy = 1606
        d.rectangle((MX, fy - 34, W - MX, fy - 30), fill=GOLD)
        d.text((MX, fy), "YOUR AURA", font=f_label, fill=CREAM_DIM)
        d.text((MX, fy + 50), "Anxious & Flammable", font=f_aura, fill=CORAL)

    # faint grain so it reads as a screen-grab, not vector art
    random.seed(537)
    px = img.load()
    for _ in range(11000):
        rx, ry = random.randint(0, W - 1), random.randint(0, H - 1)
        r_, g_, b_ = px[rx, ry]
        n = random.randint(-4, 4)
        px[rx, ry] = (max(0, min(255, r_ + n)), max(0, min(255, g_ + n)), max(0, min(255, b_ + n)))

    img.save(f"{OUT}/{fname}")
    return fname

# (n_blocks visible, show_foot, hold seconds)
SEQUENCE = [
    (0, False, 0.9),   # header only
    (1, False, 1.4),   # minutes
    (2, False, 1.4),   # top artist
    (3, False, 1.6),   # genres
    (4, False, 1.5),   # top song
    (4, True,  2.4),   # + footer (full card)
]

with open(f"{OUT}/wrapped_frames.txt", "w") as fl:
    for i, (n, foot, hold) in enumerate(SEQUENCE):
        fn = render_state(n, foot, f"mm_wrap_{i:02d}.png")
        fl.write(f"file '{OUT}/{fn}'\nduration {hold}\n")
    fl.write(f"file '{OUT}/mm_wrap_{len(SEQUENCE)-1:02d}.png'\n")

print(f"rendered {len(SEQUENCE)} frames, main {sum(s[2] for s in SEQUENCE):.1f}s")
