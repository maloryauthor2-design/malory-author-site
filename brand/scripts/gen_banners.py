#!/usr/bin/env python3
"""
Malory — Social Banners Generator
=================================

Produces FB / Reddit / Twitter-X banners that match BRAND_FOUNDATION.md.

Design pattern (per SOCIAL_BANNERS_BRIEF.md):
  - Left zone (~26%): brand anchor — wordmark / brass rule / M monogram / kicker
  - Right zone (~70%): cover cascade with subtle tilt + drop shadow
  - Soft brass radial in upper-right, dark vignette lower-left
  - Brass embers scattered across upper portion

The same script lives in both /malory-author-site and /Desktop/malory-author-website
brand folders. It writes outputs to the Desktop folder where the canonical
brand assets live (per the brief).
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Resolve paths regardless of which clone the script is run from.
HERE = os.path.dirname(os.path.abspath(__file__))            # …/brand/scripts
BRAND = os.path.dirname(HERE)                                # …/brand
ROOT  = os.path.dirname(BRAND)                               # …/(site root)
OUT   = os.path.join(BRAND, "banners")
FONTS = os.path.join(BRAND, "fonts")
os.makedirs(OUT, exist_ok=True)

# Brand palette — from BRAND_FOUNDATION.md
MIDNIGHT     = (13, 16, 21)        # #0D1015 primary-deep
PRIMARY_MID  = (26, 30, 36)        # #1A1E24
SURFACE      = (34, 39, 47)        # #22272F
BRASS        = (201, 168, 90)      # #C9A85A
BRASS_BRIGHT = (224, 196, 120)     # #E0C478
BRASS_DEEP   = (146, 120, 56)      # #927838
CREAM        = (232, 224, 204)     # #E8E0CC
MUTED        = (154, 160, 168)     # #9AA0A8

# Fonts
FRAUNCES_BOLD = os.path.join(FONTS, "Fraunces-VF.ttf")           # variable; size only
FRAUNCES_SB   = os.path.join(FONTS, "Fraunces-SemiBold.ttf")
INTER_SB      = os.path.join(FONTS, "Inter-SemiBold.ttf")
INTER_MED     = os.path.join(FONTS, "Inter-Medium.ttf")

def font(path, size):
    """Load a font, fall back to DejaVu if missing."""
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", size)

# Cover roster — one per series. Order matters: this is the L→R cascade order.
# Last item sits on top (most prominent), earlier items peek behind.
COVERS = [
    ("welcome-cover.jpg",   "Morgan & Merlin · Welcome to the Dark Ages"),
    ("psyker-5.jpg",        "Psyker Marine 5"),
    ("cuckoo-cover.jpg",    "The Soar Chronicles · Cuckoo's Last Call"),
    ("boys-2.jpg",          "Boy's Own Adventures · Mr Glimm's Skull"),
    ("pts-cover.jpg",       "Punish the System"),
    ("arcane-1.jpg",        "Arcane Galaxy: Chaos Protocols  (Jim Baen Award)"),
]

# ─────────────────────────────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────────────────────────────

def background(W, H):
    """
    Primary-deep canvas with soft brass radial upper-right and dark
    vignette lower-left. Tasteful, not loud.
    """
    img = Image.new("RGB", (W, H), MIDNIGHT)

    # Build atmospheric layers on a separate canvas, then blur + blend.
    glow = Image.new("RGB", (W, H), MIDNIGHT)
    gd = ImageDraw.Draw(glow)

    # Brass radial, upper-right
    cx, cy = int(W * 0.82), int(H * 0.18)
    max_r = int(min(W, H) * 0.95)
    for r in range(max_r, 0, -max(8, max_r // 60)):
        a = int(70 * (r / max_r))  # 0..70
        col = (
            min(MIDNIGHT[0] + a // 4, 60),
            min(MIDNIGHT[1] + a // 5, 48),
            min(MIDNIGHT[2] + a // 8, 38),
        )
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)

    # Dark vignette, lower-left (darker than midnight to create depth)
    for r in range(int(min(W, H) * 0.7), 0, -10):
        col = (
            max(MIDNIGHT[0] - 6, 4),
            max(MIDNIGHT[1] - 6, 6),
            max(MIDNIGHT[2] - 6, 10),
        )
        gd.ellipse([-int(W * 0.1) - r, int(H * 1.05) - r,
                    -int(W * 0.1) + r, int(H * 1.05) + r], fill=col)

    glow = glow.filter(ImageFilter.GaussianBlur(80))
    img = Image.blend(img, glow, 0.65)

    # Brass embers — a small handful across the upper portion
    d = ImageDraw.Draw(img)
    random.seed(42)  # deterministic
    n_embers = max(8, W // 110)
    for _ in range(n_embers):
        ex = random.randint(int(W * 0.30), int(W * 0.96))
        ey = random.randint(8, int(H * 0.45))
        r = random.choice([1, 1, 2, 2, 3])
        alpha = random.randint(40, 110)
        ember_layer = Image.new("RGBA", (r * 6, r * 6), (0, 0, 0, 0))
        ed = ImageDraw.Draw(ember_layer)
        ed.ellipse([r * 2, r * 2, r * 4, r * 4],
                   fill=BRASS_BRIGHT + (alpha,))
        ember_layer = ember_layer.filter(ImageFilter.GaussianBlur(1.2))
        img.paste(ember_layer, (ex - r * 3, ey - r * 3), ember_layer)

    return img


def render_anchor(W, H, jake=False, max_w=None):
    """
    Render the brand anchor block (transparent layer) at native resolution,
    sized to fit BOTH the banner's vertical budget AND the horizontal width
    of its target zone. Composed of:
      - Wordmark (Malory or Jake Malory)
      - Brass rule
      - M monogram
      - Kicker line
    Returns: PIL Image (RGBA, transparent background), and the rendered (w, h).
    """
    # Vertical budget
    safety = max(36, int(H * 0.10))
    avail_h = H - 2 * safety
    # Horizontal budget — allow caller override; default to a generous slice of W.
    avail_w = max_w if max_w is not None else int(W * 0.24)

    # Decide sizes from the vertical budget, not from width.
    # Reserve proportional space:
    #   wordmark: 28% of avail_h  (or 22% if "Jake Malory" two-line)
    #   gap     : 5%
    #   rule    : 1px (negligible)
    #   gap     : 6%
    #   mono    : 40%
    #   gap     : 6%
    #   kicker  : 9%
    if jake:
        # Two-line wordmark: "JAKE" (small) + "Malory" (large)
        word_h    = int(avail_h * 0.30)
        kicker_h  = int(avail_h * 0.07)
        mono_h    = int(avail_h * 0.38)
        gap_a     = int(avail_h * 0.03)
        gap_b     = int(avail_h * 0.05)
    else:
        word_h    = int(avail_h * 0.26)
        kicker_h  = int(avail_h * 0.08)
        mono_h    = int(avail_h * 0.42)
        gap_a     = int(avail_h * 0.04)
        gap_b     = int(avail_h * 0.06)

    # Word font sizing — start from the vertical budget…
    word_font_size   = max(28, int(word_h * 0.95))
    kicker_font_size = max(11, int(kicker_h * 0.95))
    if jake:
        jake_font_size = max(18, int(word_h * 0.42))

    word_font   = font(FRAUNCES_SB, word_font_size)
    kicker_font = font(INTER_MED,   kicker_font_size)

    test = Image.new("RGBA", (10, 10))
    tdraw = ImageDraw.Draw(test)

    # …then shrink it until "Malory" fits the horizontal budget with room to breathe.
    # Target: wordmark must fit within ~88% of avail_w (leaves visual margin).
    word_target_w = int(avail_w * 0.88)
    while word_font_size > 22:
        w = tdraw.textlength("Malory", font=word_font)
        if w <= word_target_w:
            break
        word_font_size = int(word_font_size * 0.92)
        word_font = font(FRAUNCES_SB, word_font_size)

    # Same constraint for kicker text — narrower it fits, shrink until it does.
    kicker_text = "SCI-FI · LITRPG · PROGRESSION" if not jake else "PSYKER MARINE · ARCANE GALAXY"
    while kicker_font_size > 9:
        kw = tdraw.textlength(kicker_text, font=kicker_font)
        if kw <= int(avail_w * 0.96):
            break
        kicker_font_size = int(kicker_font_size * 0.92)
        kicker_font = font(INTER_MED, kicker_font_size)

    if jake:
        jake_font = font(FRAUNCES_SB, jake_font_size)
        word_w_main = tdraw.textlength("Malory", font=word_font)
        word_w_jake = tdraw.textlength("JAKE",   font=jake_font)
        word_w = max(word_w_main, word_w_jake)
    else:
        word_w = tdraw.textlength("Malory", font=word_font)

    # The kicker is often wider than the wordmark — measure it and use the larger
    # so the rendered layer encloses both without clipping.
    kicker_w = tdraw.textlength(kicker_text, font=kicker_font)
    widest = max(word_w, kicker_w)

    # Logo monogram size
    rule_w = int(word_w * 0.6)
    mono_size = mono_h   # square mark

    # Anchor block width is driven by whichever line is widest (wordmark OR kicker)
    # plus a tiny bit of breathing room. Without this the kicker gets clipped on
    # banners where the kicker is wider than "Malory".
    block_w = int(widest * 1.10)
    # Make sure it's at least as wide as the monogram + small margin
    block_w = max(block_w, mono_size + 16)

    # Total block height
    if jake:
        block_h = (int(jake_font_size * 1.1) + word_h + 6
                   + 2 + gap_a + mono_size + gap_b + kicker_h)
    else:
        block_h = word_h + 6 + 2 + gap_a + mono_size + gap_b + kicker_h

    # Cap to avail_h
    if block_h > avail_h:
        scale = avail_h / block_h
        # Rescale by recursively shrinking — simplest is to size everything down
        word_font   = font(FRAUNCES_SB, max(20, int(word_font_size * scale)))
        kicker_font = font(INTER_MED,   max(10, int(kicker_font_size * scale)))
        if jake:
            jake_font = font(FRAUNCES_SB, max(14, int(jake_font_size * scale)))
        mono_size = int(mono_size * scale)
        word_w = tdraw.textlength("Malory", font=word_font)
        rule_w = int(word_w * 0.6)
        block_w = max(int(word_w * 1.15), mono_size + 16)
        # Recompute block_h
        if jake:
            block_h = (int(jake_font.size * 1.1) + int(word_font.size * 1.05) + 6
                       + 2 + gap_a + mono_size + gap_b + int(kicker_font.size * 1.1))
        else:
            block_h = int(word_font.size * 1.05) + 6 + 2 + gap_a + mono_size + gap_b + int(kicker_font.size * 1.1)

    layer = Image.new("RGBA", (block_w, block_h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    y = 0
    cx = block_w // 2

    # Optional JAKE line
    if jake:
        bbox = d.textbbox((0, 0), "JAKE", font=jake_font)
        text_w = bbox[2] - bbox[0]
        d.text((cx - text_w // 2, y), "JAKE", font=jake_font, fill=MUTED)
        y += int(jake_font.size * 1.1) + 2

    # Wordmark — "Malory"
    bbox = d.textbbox((0, 0), "Malory", font=word_font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    d.text((cx - text_w // 2, y - bbox[1]), "Malory", font=word_font, fill=CREAM)
    y += int(word_font.size * 1.05)

    # Brass rule
    y += 6
    rule_x0 = cx - rule_w // 2
    rule_x1 = cx + rule_w // 2
    d.line([(rule_x0, y), (rule_x1, y)], fill=BRASS, width=2)
    y += 2 + gap_a

    # Monogram — draw the SVG-style mark by hand (avoids depending on cairosvg).
    # Circle base, brass ring, brass M, bottom rule.
    mx0 = cx - mono_size // 2
    my0 = y
    mx1 = mx0 + mono_size
    my1 = my0 + mono_size
    # Base
    d.ellipse([mx0, my0, mx1, my1], fill=MIDNIGHT)
    # Brass ring
    ring_inset = max(2, mono_size // 60)
    d.ellipse([mx0 + ring_inset, my0 + ring_inset,
               mx1 - ring_inset, my1 - ring_inset],
              outline=BRASS, width=max(1, mono_size // 90))
    # M glyph
    m_font_size = int(mono_size * 0.66)
    m_font = font(FRAUNCES_VF if os.path.exists(FRAUNCES_VF := os.path.join(FONTS, "Fraunces-VF.ttf"))
                  else FRAUNCES_SB,
                  m_font_size)
    # Re-baseline so the M sits optically centred
    bbox = d.textbbox((0, 0), "M", font=m_font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    # Place
    mx = cx - text_w // 2 - bbox[0]
    my = my0 + (mono_size - text_h) // 2 - bbox[1]
    d.text((mx, my), "M", font=m_font, fill=BRASS)
    # Bottom rule inside the circle
    rule_y = my0 + int(mono_size * 0.78)
    rule_half = int(mono_size * 0.18)
    d.line([(cx - rule_half, rule_y), (cx + rule_half, rule_y)],
           fill=BRASS, width=max(1, mono_size // 110))
    y = my1 + gap_b

    # Kicker
    kicker = "SCI-FI · LITRPG · PROGRESSION" if not jake else "PSYKER MARINE · ARCANE GALAXY"
    bbox = d.textbbox((0, 0), kicker, font=kicker_font)
    text_w = bbox[2] - bbox[0]
    d.text((cx - text_w // 2, y - bbox[1]), kicker, font=kicker_font, fill=BRASS)

    return layer, block_w, block_h


def render_cover(cover_path, target_h, tilt_deg):
    """
    Load a cover, resize to target_h, add a cream-thin border and drop shadow,
    rotate by tilt_deg. Returns an RGBA image with transparent background.
    """
    cov = Image.open(cover_path).convert("RGB")
    ratio = target_h / cov.height
    new_w = max(1, int(cov.width * ratio))
    cov = cov.resize((new_w, target_h), Image.LANCZOS)

    # Cream hairline border
    border_w = max(1, target_h // 220)
    bordered = Image.new("RGB", (cov.width + 2 * border_w, cov.height + 2 * border_w), CREAM)
    bordered.paste(cov, (border_w, border_w))

    # Drop shadow
    shadow_pad = max(20, target_h // 18)
    canvas_w = bordered.width + 2 * shadow_pad
    canvas_h = bordered.height + 2 * shadow_pad
    shadow_layer = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow_layer)
    sd.rectangle(
        [shadow_pad + 4, shadow_pad + 8,
         shadow_pad + bordered.width + 4, shadow_pad + bordered.height + 8],
        fill=(0, 0, 0, 200),
    )
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(shadow_pad // 2))

    composite = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    composite.paste(shadow_layer, (0, 0), shadow_layer)
    composite.paste(bordered, (shadow_pad, shadow_pad))

    # Rotate
    if abs(tilt_deg) > 0.01:
        composite = composite.rotate(tilt_deg, resample=Image.BICUBIC, expand=True)

    return composite


def cascade_covers(canvas, covers, area_left, area_right, area_top, area_bottom,
                   max_tilt=3.0):
    """
    Lay out n covers across the area, with subtle alternating tilt and overlap.
    Last cover ends up on top (frontmost). Uses the brief's cascade math.
    """
    n = len(covers)
    area_h = area_bottom - area_top
    area_w = area_right - area_left

    # Cover height: about 92% of the area height (small margins top/bottom)
    cover_h = int(area_h * 0.92)
    cover_w_approx = cover_h / 1.6
    tilt_expansion = cover_h * math.sin(math.radians(max_tilt))
    effective_w = cover_w_approx + tilt_expansion

    max_last_left = area_right - effective_w
    if n > 1:
        step = (max_last_left - area_left) / (n - 1)
        step = max(step, cover_w_approx * 0.45)
    else:
        step = 0

    cy = area_top + area_h // 2

    for i, (fname, _alt) in enumerate(covers):
        path = os.path.join(ROOT, fname)
        if not os.path.exists(path):
            print(f"  ! missing cover: {fname}")
            continue
        tilt = max_tilt if (i % 2 == 0) else -max_tilt
        # Front cover (last) sits flat — most legible
        if i == n - 1:
            tilt = 0
        img = render_cover(path, cover_h, tilt)
        x = int(area_left + i * step) - img.width // 2 + int(effective_w / 2)
        y = cy - img.height // 2
        canvas.paste(img, (x, y), img)


def build_banner(W, H, out_name, jake=False):
    """Produce one banner: composite background + anchor + cover cascade."""
    img = background(W, H)

    # Anchor zone — left ~26% of width, with 30px outer padding either side
    pad = 30
    anchor_zone_w = int(W * 0.26)
    anchor_inner_w = anchor_zone_w - 2 * pad

    # Build the anchor constrained to that inner width so nothing overflows
    anchor, ablock_w, ablock_h = render_anchor(W, H, jake=jake, max_w=anchor_inner_w)
    anchor_x = max(pad, pad + (anchor_inner_w - ablock_w) // 2)
    anchor_y = max(20, (H - ablock_h) // 2)
    img.paste(anchor, (anchor_x, anchor_y), anchor)

    # Cover cascade on the right — starts after the anchor zone with a small gutter
    cascade_left   = anchor_zone_w + int(W * 0.01)
    cascade_right  = W - 18
    cascade_top    = int(H * 0.06)
    cascade_bottom = int(H * 0.94)
    cascade_covers(img, COVERS, cascade_left, cascade_right, cascade_top, cascade_bottom)

    out = os.path.join(OUT, out_name)
    img.save(out, "JPEG", quality=93, optimize=True, progressive=True)
    sz = os.path.getsize(out)
    print(f"  ✓ {out_name}  ({W}×{H}, {sz:,} bytes)")
    return  # explicit early return — code below is the old shared save


def build_youtube_banner(out_name, jake=False):
    """
    YouTube channel banner — 2048 × 1152.

    YouTube crops aggressively across devices:
      - TV view:      shows the full 2048 × 1152
      - Desktop view: shows ~2048 × 423 (centred horizontally + vertically)
      - Mobile view:  shows ~1546 × 423 (centred)
      - SAFE ZONE:    1235 × 338, centred — guaranteed visible everywhere

    So the brand block must live INSIDE the safe zone, and the cover cascade
    spreads into the side bleed wings (visible on desktop/TV but cropped on
    mobile — that's fine, they're decorative).
    """
    W, H = 2048, 1152
    SAFE_W, SAFE_H = 1235, 338
    safe_left   = (W - SAFE_W) // 2     # 406
    safe_right  = safe_left + SAFE_W    # 1641
    safe_top    = (H - SAFE_H) // 2     # 407
    safe_bottom = safe_top + SAFE_H     # 745

    img = background(W, H)

    # Brand block — pass a virtual height much larger than the safe zone so
    # the anchor renders at a visually appropriate size for the 2048×1152
    # canvas. Then constrain horizontal width to the safe zone so nothing
    # spills outside what's guaranteed visible.
    anchor_inner_w = SAFE_W - 120
    virtual_h = int(H * 0.62)   # gives the wordmark room to be properly large
    anchor, ablock_w, ablock_h = render_anchor(W, virtual_h, jake=jake,
                                                max_w=anchor_inner_w)
    anchor_x = (W - ablock_w) // 2
    anchor_y = (H - ablock_h) // 2
    img.paste(anchor, (anchor_x, anchor_y), anchor)

    # Cover cascades in the two bleed wings.
    # YouTube's bleed wings are narrow (~400px each side of the safe zone),
    # so use only 2 covers per wing — over-stuffing crams them. The flagship
    # (last COVER in the roster) goes to the right wing front.
    n = len(COVERS)
    # Use the 4 most prominent covers; flagship sits in right wing front.
    selected = COVERS[-4:]   # last four (flagship is last)
    left_pair  = selected[:2]
    right_pair = selected[2:]

    # Vertical band for covers — narrower so cover_w fits the wing width.
    cov_top    = (H - 420) // 2
    cov_bottom = cov_top + 420

    # Left wing — covers tilt slightly outward
    cascade_covers(img, left_pair,
                   area_left=int(W * 0.04),
                   area_right=safe_left - 40,
                   area_top=cov_top,
                   area_bottom=cov_bottom,
                   max_tilt=2.5)

    # Right wing — flagship sits frontmost on the right.
    cascade_covers(img, right_pair,
                   area_left=safe_right + 40,
                   area_right=W - int(W * 0.04),
                   area_top=cov_top,
                   area_bottom=cov_bottom,
                   max_tilt=2.5)

    out = os.path.join(OUT, out_name)
    img.save(out, "JPEG", quality=93, optimize=True, progressive=True)
    sz = os.path.getsize(out)
    print(f"  ✓ {out_name}  ({W}×{H}, {sz:,} bytes)")


def main():
    print("Building social banners → " + OUT)
    build_banner(1640, 624, "fb-cover.jpg")
    build_banner(1280, 384, "reddit-banner.jpg")
    build_banner(1500, 500, "twitter-header.jpg")
    build_youtube_banner("youtube-banner.jpg")

    # Optional Jake Malory variants for Psyker / Arcane Galaxy launches
    # Build them so they exist; the author can use them when the moment calls.
    # We swap the leftmost roster to put a Jake series cover at the front.
    global COVERS
    original = COVERS[:]
    COVERS = [c for c in COVERS if c[0] not in ("arcane-1.jpg", "psyker-5.jpg")] + \
             [("psyker-5.jpg", "Psyker Marine 5"),
              ("arcane-1.jpg", "Arcane Galaxy: Chaos Protocols")]
    print()
    print("Jake Malory variants (psyker/arcane front):")
    build_banner(1640, 624, "fb-cover-jake.jpg",      jake=True)
    build_banner(1280, 384, "reddit-banner-jake.jpg", jake=True)
    build_banner(1500, 500, "twitter-header-jake.jpg", jake=True)
    build_youtube_banner("youtube-banner-jake.jpg", jake=True)
    COVERS = original


if __name__ == "__main__":
    main()
