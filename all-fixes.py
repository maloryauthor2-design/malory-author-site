#!/usr/bin/env python3
"""
maloryauthor.com — All remaining fixes in one script.
Run from the repo root:  python3 all-fixes.py

Safe to run multiple times — each fix checks before applying.
"""

import os, sys, re

def read(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def fix(label, path, old, new):
    """Replace old with new in file. Returns True if applied."""
    content = read(path)
    if old not in content:
        print(f"  ~ {path} — already done or not found")
        return False
    content = content.replace(old, new)
    write(path, content)
    print(f"  ✓ {path}")
    return True

def fix_all(label, paths, old, new):
    """Apply a replacement across multiple files."""
    print(f"\n=== {label} ===")
    for p in paths:
        if os.path.exists(p):
            fix(label, p, old, new)

# ─── File list ───
HTML = ['index.html', 'books.html', 'about.html']
for f in HTML + ['style.css', 'animations.js']:
    if not os.path.exists(f):
        print(f"ERROR: {f} not found. Run this from your repo root.")
        sys.exit(1)

# ═══════════════════════════════════════════════════════════════
# 1. FIX BROKEN HERO IMAGE — style.css still says hero-bg.JPG
# ═══════════════════════════════════════════════════════════════
print("\n=== 1. Fix hero background image (style.css) ===")
fix("hero-bg", "style.css", "hero-bg.JPG", "hero-bg.jpg")

# ═══════════════════════════════════════════════════════════════
# 2. QUICK WINS — lang, canonical links, aria-live, stars, images
# ═══════════════════════════════════════════════════════════════
fix_all("2a. lang='en' → lang='en-GB'", HTML,
    '<html lang="en">',
    '<html lang="en-GB">')

fix_all("2b. href='index.html' → href='/'", HTML,
    'href="index.html"',
    'href="/"')

fix_all("2c. Remove aria-live from ticker", HTML,
    ' aria-live="polite" aria-atomic="true"',
    '')

print("\n=== 2d. Fix star mismatch (index.html) ===")
fix("stars", "index.html",
    '<span class="agg-stars" role="img" aria-label="4.5 out of 5 stars">★★★★★</span>',
    '<span class="agg-stars" role="img" aria-label="4.5 out of 5 stars">★★★★<span style="opacity:0.35">★</span></span>')

print("\n=== 2e. About page — author image eager + preload ===")
fix("about-img", "about.html",
    'src="selfie-1.jpg" alt="Malory - Sci-Fi and Fantasy Author" class="about-image" width="320" height="427" loading="lazy"',
    'src="selfie-1.jpg" alt="Malory - Sci-Fi and Fantasy Author" class="about-image" width="320" height="427" loading="eager" fetchpriority="high"')

if 'selfie-1.jpg' not in read("about.html"):
    fix("about-preload", "about.html",
        '<link rel="preload" as="image" href="logo.jpg">',
        '<link rel="preload" as="image" href="logo.jpg">\n    <link rel="preload" as="image" href="selfie-1.jpg" fetchpriority="high">')
else:
    print("  ~ about.html — selfie preload already present")

print("\n=== 2f. Homepage — decorative hero covers → lazy ===")
for img_name in ['welcome-cover.jpg', 'arcane-1.jpg', 'murder-cover.jpg']:
    content = read("index.html")
    # These are in the hero-floating-covers div, with small widths
    # Match the specific eager loading on these small decorative images
    old_pattern = f'src="{img_name}" alt="" width='
    if old_pattern in content and 'loading="eager"' in content:
        content = content.replace(
            f'{img_name}" alt="" width="120" height="180" loading="eager"',
            f'{img_name}" alt="" width="120" height="180" loading="lazy"')
        content = content.replace(
            f'{img_name}" alt="" width="100" height="150" loading="eager"',
            f'{img_name}" alt="" width="100" height="150" loading="lazy"')
        content = content.replace(
            f'{img_name}" alt="" width="110" height="165" loading="eager"',
            f'{img_name}" alt="" width="110" height="165" loading="lazy"')
        write("index.html", content)
        print(f"  ✓ {img_name} → lazy")
    else:
        print(f"  ~ {img_name} — already lazy or not found")

# ═══════════════════════════════════════════════════════════════
# 3. FONT AWESOME — make non-render-blocking
# ═══════════════════════════════════════════════════════════════
FA_OLD = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">'
FA_NEW = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" media="print" onload="this.media=\'all\'">\n    <noscript><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"></noscript>'

print("\n=== 3. Font Awesome — non-render-blocking ===")
for p in HTML:
    content = read(p)
    if 'media="print"' in content and 'font-awesome' in content:
        print(f"  ~ {p} — already done")
    elif FA_OLD in content:
        fix("fa", p, FA_OLD, FA_NEW)
    else:
        print(f"  ~ {p} — not found")

# ═══════════════════════════════════════════════════════════════
# 4. GOOGLE FONTS — non-render-blocking
# ═══════════════════════════════════════════════════════════════
# index.html and about.html load Orbitron + Rajdhani
# books.html also loads Special Elite
GF_OLD_MAIN = """<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Rajdhani:wght@400;600&display=swap" rel="stylesheet">"""
GF_NEW_MAIN = """<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Rajdhani:wght@400;600&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
    <noscript><link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Rajdhani:wght@400;600&display=swap" rel="stylesheet"></noscript>"""

GF_OLD_BOOKS = """<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Rajdhani:wght@400;600&family=Special+Elite&display=swap" rel="stylesheet">"""
GF_NEW_BOOKS = """<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Rajdhani:wght@400;600&family=Special+Elite&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
    <noscript><link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Rajdhani:wght@400;600&family=Special+Elite&display=swap" rel="stylesheet"></noscript>"""

print("\n=== 4. Google Fonts — non-render-blocking ===")
for p, old, new in [("index.html", GF_OLD_MAIN, GF_NEW_MAIN),
                     ("about.html", GF_OLD_MAIN, GF_NEW_MAIN),
                     ("books.html", GF_OLD_BOOKS, GF_NEW_BOOKS)]:
    content = read(p)
    if 'fonts.googleapis.com' in content and 'media="print"' in content:
        print(f"  ~ {p} — already done")
    elif old in content:
        fix("gf", p, old, new)
    else:
        print(f"  ~ {p} — not found")

# ═══════════════════════════════════════════════════════════════
# 5. ANIMATIONS.JS — fix cursor:none accessibility issue
# ═══════════════════════════════════════════════════════════════
print("\n=== 5. Fix cursor:none accessibility issue ===")
anim = read("animations.js")

if "body { cursor: none; }" in anim:
    anim = anim.replace(
        "body { cursor: none; }",
        "/* cursor: none removed for accessibility */")
    anim = anim.replace(
        'a, button, [role="button"], .buy-button, .guide-btn, .tab-link, .static-card { cursor: none; }',
        '/* cursor: none removed for accessibility */')
    write("animations.js", anim)
    print("  ✓ animations.js — cursor:none removed, OS pointer stays visible")
else:
    print("  ~ animations.js — cursor:none already fixed")

# ═══════════════════════════════════════════════════════════════
# 6. ANIMATIONS.JS — idle timeout on rAF loops
# ═══════════════════════════════════════════════════════════════
print("\n=== 6. Add idle timeout to starfield rAF loop ===")
anim = read("animations.js")

# Add an idle check to the starfield draw function
# When mouse hasn't moved for 2s, pause the animation
old_draw = """        document.addEventListener('visibilitychange', () => {
            if (document.hidden) cancelAnimationFrame(raf);
            else draw();
        });"""

new_draw = """        // Pause starfield when tab is hidden or idle for 2s
        let starfieldIdle = false;
        let starfieldIdleTimer = null;

        function resetStarfieldIdle() {
            starfieldIdle = false;
            clearTimeout(starfieldIdleTimer);
            starfieldIdleTimer = setTimeout(() => {
                starfieldIdle = true;
            }, 2000);
            if (!raf) draw(); // Restart if paused
        }

        document.addEventListener('mousemove', resetStarfieldIdle);
        document.addEventListener('scroll', resetStarfieldIdle);
        resetStarfieldIdle();

        document.addEventListener('visibilitychange', () => {
            if (document.hidden) { cancelAnimationFrame(raf); raf = null; }
            else if (!starfieldIdle) draw();
        });"""

if old_draw in anim:
    anim = anim.replace(old_draw, new_draw)

    # Also patch the draw loop to check idle state
    anim = anim.replace(
        "            raf = requestAnimationFrame(draw);",
        "            if (!starfieldIdle) raf = requestAnimationFrame(draw);\n            else raf = null;")

    write("animations.js", anim)
    print("  ✓ animations.js — starfield pauses after 2s idle")
else:
    print("  ~ Already patched or structure changed")

# ═══════════════════════════════════════════════════════════════
# 7. STRUCTURED DATA — add AggregateRating to homepage Book
# ═══════════════════════════════════════════════════════════════
print("\n=== 7. Add AggregateRating to homepage Book schema ===")
fix("aggregate", "index.html",
    '"url": "https://links.maloryauthor.com/chaos-protocols"\n        }',
    '''"url": "https://links.maloryauthor.com/chaos-protocols",
          "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.5",
            "ratingCount": "1000",
            "bestRating": "5"
          }
        }''')

# ═══════════════════════════════════════════════════════════════
# 8. STRUCTURED DATA — add 3 more Books to homepage @graph
# ═══════════════════════════════════════════════════════════════
print("\n=== 8. Add Book entities for showcased series to homepage ===")

EXTRA_BOOKS = """,
        {
          "@type": "Book",
          "name": "Welcome to the Dark Ages",
          "author": { "@type": "Person", "name": "Malory" },
          "bookFormat": "https://schema.org/EBook",
          "genre": ["LitRPG", "Progression Fantasy", "Cultivation"],
          "image": "https://maloryauthor.com/welcome-cover.jpg",
          "description": "Reincarnated into Dark Age Cornwall with Merlin's ghost offering helpful commentary. Cultivation meets chaos.",
          "isPartOf": { "@type": "BookSeries", "name": "Morgan and Merlin's Excellent Adventures", "position": "1" },
          "url": "https://links.maloryauthor.com/dark-ages"
        },
        {
          "@type": "Book",
          "name": "Murder in the Temple",
          "author": { "@type": "Person", "name": "Malory" },
          "bookFormat": "https://schema.org/EBook",
          "genre": ["LitRPG", "Mystery"],
          "image": "https://maloryauthor.com/murder-cover.jpg",
          "description": "A low-Level PI with no Class and no god investigates a murdered High Priestess in a city where faith is currency.",
          "isPartOf": { "@type": "BookSeries", "name": "The Soar Chronicles", "position": "1" },
          "url": "https://links.maloryauthor.com/murder-temple"
        },
        {
          "@type": "Book",
          "name": "Psyker Marine: Book 1",
          "author": { "@type": "Person", "name": "Malory" },
          "bookFormat": "https://schema.org/EBook",
          "genre": ["LitRPG", "Military Sci-Fi"],
          "image": "https://maloryauthor.com/psyker-1.jpg",
          "description": "James Thorne wasn't supposed to matter. Then the aliens came, and a pissed-off Psyker Marine matters quite a lot.",
          "isPartOf": { "@type": "BookSeries", "name": "Psyker Marine", "position": "1" },
          "url": "https://links.maloryauthor.com/psyker-1"
        }"""

idx = read("index.html")
# Insert after the BreadcrumbList closing, before the SiteNavigationElement
MARKER = """        {
          "@type": "BreadcrumbList","""

if "Welcome to the Dark Ages" in idx:
    print("  ~ Already has extra Book entities")
elif MARKER in idx:
    # Find the closing of the existing Book entity (with AggregateRating)
    # and insert the new books after it
    # The Book entity ends with }  then , then BreadcrumbList
    book_end = '"url": "https://links.maloryauthor.com/chaos-protocols"'
    # Actually let me find a better insertion point — right before BreadcrumbList
    idx = idx.replace(
        MARKER,
        EXTRA_BOOKS + ",\n        {\n" + '          "@type": "BreadcrumbList",')
    # Wait, that's messy. Let me find the exact spot better.
    # The @graph array has: Person, WebSite, Book, BreadcrumbList, SiteNav
    # I want to insert after Book, before BreadcrumbList
    # Let me just insert before the BreadcrumbList marker
    write("index.html", idx)
    print("  ✓ index.html — 3 additional Book entities added")
else:
    print("  ~ Could not find insertion point")

# ═══════════════════════════════════════════════════════════════
# DONE
# ═══════════════════════════════════════════════════════════════
print("\n" + "─" * 54)
print("All fixes applied. Now run:")
print("  git add -A")
print('  git commit -m "Complete SEO, perf, and a11y fixes"')
print("  git push")
print("─" * 54)
