"""Build crit-hits-NN-slug-shorts-1080x1920.png from the existing
1080x1080 square covers. Adds disciplined-publisher brass margins
top and bottom carrying the masthead and archival code.

This is a bridge build — it composes from already-rendered square
assets. When the book cover JPEGs are re-uploaded, the proper
make_shorts() function in gen_crit_hits.py renders from source.
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# --- Paths (current cowork session mounts) -----------------------------
ASSETS_VAULT = "/sessions/blissful-practical-hopper/mnt/PhD/08_Reviews/_assets"
ASSETS_WS    = "/sessions/blissful-practical-hopper/mnt/Reviews"
CANVAS_FONTS = "/sessions/blissful-practical-hopper/mnt/.claude/skills/canvas-design/canvas-fonts"
BRAND_FONTS  = "/sessions/blissful-practical-hopper/mnt/malory-author-website/brand/fonts"

# Try Inter from outputs (downloaded previously) or fall back
INTER_PATHS = [
    "/sessions/blissful-practical-hopper/mnt/outputs/fonts/Inter-Medium-static.ttf",
    "/sessions/blissful-practical-hopper/mnt/outputs/fonts/Inter-SemiBold.ttf",
    os.path.join(CANVAS_FONTS, "Inter-Medium.ttf"),
]

# --- Brand palette (exact, BRAND_FOUNDATION.md §3) ---------------------
MIDNIGHT     = (13, 16, 21)
BRASS        = (201, 168, 90)
BRASS_BRIGHT = (224, 196, 120)
BRASS_DEEP   = (146, 120, 56)
CREAM        = (232, 224, 204)
MUTED        = (154, 160, 168)


def find_font(candidates, size):
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    # Last-ditch fallback
    return ImageFont.load_default()


def fraunces(size):
    return find_font([os.path.join(BRAND_FONTS, "Fraunces-VF.ttf")], size)


def inter_med(size):
    return find_font(INTER_PATHS, size)


def jbmono(size, bold=False):
    name = "JetBrainsMono-Bold.ttf" if bold else "JetBrainsMono-Regular.ttf"
    return find_font([os.path.join(CANVAS_FONTS, name)], size)


def text_w(text, fnt, ls=0):
    if not text:
        return 0
    w = 0
    for ch in text:
        b = fnt.getbbox(ch)
        w += (b[2] - b[0]) + ls
    return w - ls


def draw_tracked(draw, text, x, y, fnt, color, ls=0):
    cx = x
    for ch in text:
        draw.text((cx, y), ch, font=fnt, fill=color)
        b = fnt.getbbox(ch)
        cx += (b[2] - b[0]) + ls
    return cx - ls


def hairline(draw, x1, y1, x2, y2, color=BRASS_DEEP, width=1):
    draw.line([(x1, y1), (x2, y2)], fill=color, width=width)


def make_ground(w, h):
    arr = np.zeros((h, w, 3), dtype=np.float32)
    arr[:] = np.array(MIDNIGHT, dtype=np.float32)
    # Subtle brass radial top
    y, x = np.mgrid[0:h, 0:w]
    cx_b, cy_b = w * 0.5, h * 0.08
    d_b = np.sqrt((x - cx_b) ** 2 + (y - cy_b) ** 2)
    max_d = np.sqrt(w ** 2 + h ** 2)
    glow = np.clip(1.0 - (d_b / (max_d * 0.45)), 0, 1) ** 2 * 0.18
    for c in range(3):
        arr[:, :, c] += (BRASS_DEEP[c] - MIDNIGHT[c]) * glow
    # Film grain
    np.random.seed(11)
    grain = np.random.normal(0, 3.0, (h, w, 3))
    arr += grain
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)


# --- Issue config (matches gen_crit_hits.py) ---------------------------
ISSUES = {
    "ph": {
        "number": "01",
        "code": "CH·01·PH·MMXXVI",
        "title": "THE PRIMAL HUNTER",
        "author": "ZOGARTH",
        "pub":   "AETHON BOOKS  ·  2022",
    },
    "hwfwm": {
        "number": "02",
        "code": "CH·02·HWFWM·MMXXVI",
        "title": "HE WHO FIGHTS WITH MONSTERS",
        "author": "SHIRTALOON",
        "pub":   "AETHON / PODIUM  ·  2021",
    },
}


def make_shorts(slug):
    """Build 1080x1920 vertical title card from the existing 1080x1080 square."""
    issue = ISSUES[slug]
    W, H = 1080, 1920
    canvas = make_ground(W, H)
    d = ImageDraw.Draw(canvas)

    # Load the existing 1080x1080 square cover
    sq_path = os.path.join(ASSETS_VAULT, f"crit-hits-{issue['number']}-{slug}-square-1080x1080.png")
    if not os.path.exists(sq_path):
        print(f"  ERROR: missing source square at {sq_path}")
        return None
    square = Image.open(sq_path).convert("RGB")

    # Vertical layout zones:
    #   0-340      top margin (masthead + Crit Hits Nº NN)
    #   340-1420   square body (1080x1080 centred)
    #   1420-1920  bottom margin (verdict reinforcement + URL + archival code)
    top_margin_h = 340
    bottom_margin_y = top_margin_h + 1080  # 1420

    # Paste the square in the middle
    canvas.paste(square, (0, top_margin_h))

    # === TOP MARGIN ====================================================
    M = 48

    # Top hairline accent (just inside the top edge)
    hairline(d, M, 28, W - M, 28, BRASS, 2)
    hairline(d, M, 36, W // 2 - 30, 36, BRASS_DEEP, 1)
    hairline(d, W // 2 + 30, 36, W - M, 36, BRASS_DEEP, 1)

    # Eyebrow: "CRIT HITS · THE REVIEW COLUMN"
    eyebrow_f = jbmono(20, bold=True)
    eyebrow = "CRIT HITS  ·  THE REVIEW COLUMN"
    ew = text_w(eyebrow, eyebrow_f, 5)
    draw_tracked(d, eyebrow, (W - ew) // 2, 70, eyebrow_f, BRASS, ls=5)

    # Issue number — large Fraunces
    issue_f = fraunces(120)
    issue_text = "Nº " + issue["number"]
    iw = text_w(issue_text, issue_f)
    d.text(((W - iw) // 2, 110), issue_text, font=issue_f, fill=CREAM)

    # Bottom of top margin — hairline rule before the square body begins
    hairline(d, M, top_margin_h - 14, W - M, top_margin_h - 14, BRASS_DEEP, 1)

    # === BOTTOM MARGIN =================================================
    by = bottom_margin_y
    # Hairline rule just below the square
    hairline(d, M, by + 14, W - M, by + 14, BRASS_DEEP, 1)

    # Book title (large Fraunces brass), centred
    title = issue["title"]
    target = 80
    title_f = fraunces(target)
    available = W - 2 * M
    # Try one-line, then wrap to two if needed
    if text_w(title, title_f) > available:
        # Wrap on word boundaries
        words = title.split()
        lines = []
        cur = ""
        for w in words:
            test = (cur + " " + w).strip()
            if text_w(test, title_f) <= available:
                cur = test
            else:
                if cur: lines.append(cur)
                cur = w
        if cur: lines.append(cur)
    else:
        lines = [title]

    # Shrink to fit if even wrapping fails
    while any(text_w(line, title_f) > available for line in lines) and target > 36:
        target -= 4
        title_f = fraunces(target)

    title_y = by + 60
    line_h = int(target * 1.06)
    for i, line in enumerate(lines):
        lw = text_w(line, title_f)
        d.text(((W - lw) // 2, title_y + i * line_h), line, font=title_f, fill=BRASS_BRIGHT)

    # Author + publisher in mono
    by_offset = title_y + len(lines) * line_h + 28
    auth_f = jbmono(20, bold=True)
    auth_text = "BY " + issue["author"]
    aw = text_w(auth_text, auth_f, 4)
    draw_tracked(d, auth_text, (W - aw) // 2, by_offset, auth_f, BRASS, ls=4)
    pub_f = jbmono(16)
    pw = text_w(issue["pub"], pub_f, 3)
    draw_tracked(d, issue["pub"], (W - pw) // 2, by_offset + 30, pub_f, MUTED, ls=3)

    # Decorative central dot ornament with brass rules
    orn_y = by_offset + 80
    hairline(d, M + 60, orn_y, W // 2 - 24, orn_y, BRASS, 1)
    hairline(d, W // 2 + 24, orn_y, W - M - 60, orn_y, BRASS, 1)
    cx = W // 2
    for off in [-18, 0, 18]:
        r = 3 if off == 0 else 2
        d.ellipse([(cx + off - r, orn_y - r), (cx + off + r, orn_y + r)], fill=BRASS)

    # URL + archival code at very bottom
    url_f = jbmono(18, bold=True)
    url = "MALORYAUTHOR.SUBSTACK.COM"
    uw = text_w(url, url_f, 4)
    draw_tracked(d, url, (W - uw) // 2, H - 100, url_f, CREAM, ls=4)
    code_f = jbmono(14)
    cw = text_w(issue["code"], code_f, 3)
    draw_tracked(d, issue["code"], (W - cw) // 2, H - 64, code_f, MUTED, ls=3)

    # Bottom edge hairline accents matching top
    hairline(d, M, H - 36, W // 2 - 30, H - 36, BRASS_DEEP, 1)
    hairline(d, W // 2 + 30, H - 36, W - M, H - 36, BRASS_DEEP, 1)
    hairline(d, M, H - 28, W - M, H - 28, BRASS, 2)

    return canvas


def main():
    out_paths = [ASSETS_VAULT, ASSETS_WS]
    for slug in ["ph", "hwfwm"]:
        img = make_shorts(slug)
        if img is None:
            continue
        num = ISSUES[slug]["number"]
        fname = f"crit-hits-{num}-{slug}-shorts-1080x1920.png"
        for dest_dir in out_paths:
            os.makedirs(dest_dir, exist_ok=True)
            outp = os.path.join(dest_dir, fname)
            img.save(outp, "PNG", optimize=True)
            print(f"  saved {outp}")


if __name__ == "__main__":
    print("Crit Hits 9:16 shorts covers")
    print("=" * 50)
    main()
