#!/usr/bin/env python3
"""Explosion finish for the AG prison-break reel.
Two stills: a white impact flash, then a fireball with smoke, debris (incl.
message-bubble shards as a wink to the format), shockwave ring, and the dry
payoff caption. Concatenated after the chat, before the title card.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random, math

W, H = 1080, 1920
FONTS = "/sessions/determined-focused-wright/mnt/malory-author-website/brand/fonts"
OUT = "/sessions/determined-focused-wright/mnt/outputs"
f_cap = ImageFont.truetype(f"{FONTS}/Inter-SemiBold-static.ttf", 44)

CX, CY = 540, 900   # blast centre
CREAM = (245, 245, 245)

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

# fireball colour stops, t=0 core (white-hot) -> t=1 edge (near black)
STOPS = [
    (0.00, (255, 255, 248)),
    (0.12, (255, 244, 196)),
    (0.26, (255, 196, 92)),
    (0.44, (240, 122, 44)),
    (0.64, (150, 50, 26)),
    (0.84, (60, 24, 18)),
    (1.00, (12, 9, 11)),
]
def stop_color(t):
    for i in range(len(STOPS) - 1):
        t0, c0 = STOPS[i]; t1, c1 = STOPS[i + 1]
        if t0 <= t <= t1:
            return lerp(c0, c1, (t - t0) / (t1 - t0))
    return STOPS[-1][1]

def grain(img, n=16000, amp=5):
    random.seed(7)
    px = img.load()
    for _ in range(n):
        x, y = random.randint(0, W - 1), random.randint(0, H - 1)
        r, g, b = px[x, y][:3]
        d = random.randint(-amp, amp)
        px[x, y] = (max(0, min(255, r + d)), max(0, min(255, g + d)), max(0, min(255, b + d)))

# ---------- FLASH ----------
def render_flash():
    img = Image.new("RGB", (W, H), (255, 252, 240))
    d = ImageDraw.Draw(img)
    # faint hot core + quick falloff so it's a blinding blink, not flat white
    for t in [x / 40 for x in range(40, 0, -1)]:
        r = int(820 * t)
        col = lerp((255, 255, 255), (255, 230, 180), t)
        d.ellipse((CX - r, CY - r, CX + r, CY + r), fill=col)
    grain(img, n=8000, amp=4)
    img.save(f"{OUT}/boom_flash.png")

# ---------- FIREBALL ----------
def render_fire():
    img = Image.new("RGB", (W, H), (10, 8, 10))
    # warm dark vignette base
    base = img.load()
    for y in range(0, H, 2):
        for x in range(0, W, 2):
            dx, dy = (x - CX) / W, (y - CY) / H
            v = max(0, 1 - (dx * dx + dy * dy) * 2.2)
            c = lerp((10, 8, 10), (40, 20, 14), v)
            base[x, y] = c
            if x + 1 < W: base[x + 1, y] = c
            if y + 1 < H: base[x, y + 1] = c
    # smoke layer (blurred dark billows above the blast)
    smoke = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(smoke)
    random.seed(11)
    for _ in range(26):
        bx = CX + random.randint(-460, 460)
        by = CY - random.randint(-120, 520)
        br = random.randint(120, 300)
        shade = random.randint(28, 70)
        sd.ellipse((bx - br, by - br, bx + br, by + br),
                   fill=(shade, int(shade * 0.7), int(shade * 0.55), 120))
    smoke = smoke.filter(ImageFilter.GaussianBlur(40))
    img = Image.alpha_composite(img.convert("RGBA"), smoke).convert("RGB")
    d = ImageDraw.Draw(img)

    # fireball: large->small concentric, dark edge first then white core on top
    R = 600
    steps = 150
    for i in range(steps):
        t = 1 - i / steps          # 1 (edge) -> ~0 (core)
        rr = int(R * t)
        if rr <= 0:
            continue
        aj = abs(int(18 * math.sin(i * 1.7)))
        d.ellipse((CX - rr - aj, CY - rr, CX + rr + aj, CY + rr), fill=stop_color(t))

    # radial flame rays bursting outward (jagged, not bokeh)
    rays = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ryd = ImageDraw.Draw(rays)
    random.seed(21)
    for _ in range(46):
        ang = random.uniform(0, 2 * math.pi)
        r0 = R * random.uniform(0.25, 0.55)
        r1 = R * random.uniform(0.92, 1.28)
        wob = random.uniform(0.018, 0.05)
        col = stop_color(random.uniform(0.18, 0.46)) + (random.randint(120, 200),)
        p_in1 = (CX + math.cos(ang - wob) * r0, CY + math.sin(ang - wob) * r0)
        p_in2 = (CX + math.cos(ang + wob) * r0, CY + math.sin(ang + wob) * r0)
        p_out = (CX + math.cos(ang) * r1, CY + math.sin(ang) * r1)
        ryd.polygon([p_in1, p_out, p_in2], fill=col)
    rays = rays.filter(ImageFilter.GaussianBlur(5))
    img = Image.alpha_composite(img.convert("RGBA"), rays).convert("RGB")
    d = ImageDraw.Draw(img)

    # a few merged flame masses near the rim (irregular, overlapping — not dots)
    random.seed(5)
    for _ in range(14):
        ang = random.uniform(0, 2 * math.pi)
        rad = R * random.uniform(0.82, 1.0)
        fx, fy = CX + math.cos(ang) * rad, CY + math.sin(ang) * rad
        fr = random.randint(60, 120)
        d.ellipse((fx - fr, fy - fr * 0.7, fx + fr, fy + fr * 0.7),
                  fill=stop_color(random.uniform(0.28, 0.5)))

    # shockwave ring
    for k, a in ((1.10, 70), (1.02, 130)):
        rr = int(R * k)
        ring = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        rd = ImageDraw.Draw(ring)
        rd.ellipse((CX - rr, CY - rr, CX + rr, CY + rr), outline=(255, 226, 180, a), width=6)
        img = Image.alpha_composite(img.convert("RGBA"), ring.filter(ImageFilter.GaussianBlur(3))).convert("RGB")
    d = ImageDraw.Draw(img)

    # debris — dark shards with motion streaks, flung radially
    random.seed(99)
    for _ in range(34):
        ang = random.uniform(0, 2 * math.pi)
        rad = R * random.uniform(1.0, 1.7)
        x, y = CX + math.cos(ang) * rad, CY + math.sin(ang) * rad
        sz = random.randint(6, 20)
        sx, sy = math.cos(ang) * sz * 2.5, math.sin(ang) * sz * 2.5
        d.line([(x, y), (x + sx, y + sy)], fill=(20, 16, 16), width=max(2, sz // 4))
        d.polygon([(x, y), (x + sz, y + sz // 2), (x + sz // 2, y + sz)], fill=(28, 22, 20))

    # a few message-bubble shards (wink to the format) flying out of the blast
    random.seed(3)
    for _ in range(5):
        ang = random.uniform(-math.pi, 0)        # mostly upward
        rad = R * random.uniform(0.9, 1.5)
        x, y = CX + math.cos(ang) * rad, CY + math.sin(ang) * rad
        bw, bh = random.randint(70, 120), random.randint(40, 58)
        col = random.choice([(38, 38, 42), (10, 132, 255)])
        shard = Image.new("RGBA", (bw + 20, bh + 20), (0, 0, 0, 0))
        ImageDraw.Draw(shard).rounded_rectangle((4, 4, bw, bh), radius=18, fill=col + (235,))
        shard = shard.rotate(random.uniform(-40, 40), expand=True, resample=Image.BICUBIC)
        img.paste(shard, (int(x), int(y)), shard)

    d = ImageDraw.Draw(img)
    grain(img, n=15000, amp=6)

    # captions: continuity line on top, dry payoff button low
    lw = d.textlength("breaking him out of space prison", font=f_cap)
    d.text(((W - lw) / 2, 82), "breaking him out of space prison", font=f_cap, fill=CREAM)
    pay = "he'd rather stay in."
    pw = d.textlength(pay, font=f_cap)
    # subtle dark plate behind the payoff so it reads over the fire
    d.rectangle(((W - pw) / 2 - 26, 1604, (W + pw) / 2 + 26, 1672), fill=(8, 6, 8))
    d.text(((W - pw) / 2, 1612), pay, font=f_cap, fill=CREAM)

    img.save(f"{OUT}/boom_fire.png")

render_flash()
render_fire()
print("saved boom_flash.png, boom_fire.png")
