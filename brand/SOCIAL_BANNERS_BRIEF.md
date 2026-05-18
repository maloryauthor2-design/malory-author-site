# Social Banners — Task Brief & Handoff

A previous Claude session (call it "Session B") attempted this task and got the brand wrong on every axis. This document is the clean spec for **a future session to pick it up correctly**, with the few things from Session B's attempt that are actually worth preserving (the layout math, the dimensions, the dynamic-sizing trick).

The author asked for social-media banners for **Facebook, Reddit, and Twitter/X**. They'd like the work picked up by a session that already knows the canonical Malory brand.

---

## What to build

Three branded banners showcasing the catalog and award credential, sized for each platform's spec:

| File | Dimensions | Aspect | For |
|---|---|---|---|
| `fb-cover.jpg` | 1640 × 624 | 2.63:1 | Facebook cover photo |
| `reddit-banner.jpg` | 1280 × 384 | 3.33:1 | Reddit profile banner |
| `twitter-header.jpg` | 1500 × 500 | 3:1 | Twitter / X header |

Output as JPEG, quality ≥ 92, progressive, optimized. Save to `brand/banners/`.

---

## Brand requirements — read these first

**`brand/BRAND_FOUNDATION.md` is the source of truth.** Don't deviate from it. Specifically, banners must:

- Use **Fraunces** for the "Malory" wordmark (weight 600, mixed case, +0.04em tracking)
- Use **brass `#C9A85A`** as the primary accent — NOT casino gold `#d4af37`, NOT amber, NOT yellow
- Use **primary-deep `#0D1015`** as the background base
- Use the **canonical `malory-mark.svg`** as the logo glyph (clean M in brass on primary-deep, thin brass ring) — NOT the legacy gothic-flourish JPG
- Use **Inter** or **JetBrains Mono** for any kicker/tagline copy (Inter for promotional, Mono for data/credentials register)
- Reference the **series anchor colours** from BRAND_FOUNDATION.md §6 if any series-specific accent is needed
- Respect the Jake Malory sub-identity rule (§5c) — if a banner specifically features Psyker Marine or Arcane Galaxy: Chaos Protocols and would carry an author byline, use the **Jake Malory** secondary lockup, not the umbrella Malory wordmark

If you need to add anything outside the existing palette/type stack, propose the addition in BRAND_FOUNDATION.md first and have the author confirm before generating.

---

## Layout pattern that worked compositionally

(Session B's brand choices were wrong, but the structural composition was sound. Use this pattern.)

**Three-zone horizontal layout:**

- **Left zone (~26% width)** — brand anchor block, vertically stacked: wordmark on top, thin brass rule, logo monogram, then a short tagline. Centred vertically within the available banner height.
- **Right zone (~70% width)** — cover cascade. Five to seven covers arranged left-to-right with alternating gentle tilts (±2–3°), cream-border + drop shadow on each, slight horizontal overlap so the leftmost peeks behind and the rightmost (most recent) sits on top.
- **Small reserved margin (right edge)** to prevent the rightmost cover from kissing the canvas edge.

Background: primary-deep with a soft radial brass glow in the upper-right corner (low intensity — atmospheric, not loud) and a darker vignette in the lower-left for depth behind the anchor block.

A small handful of brass "ember" specks across the upper portion add texture without competing with the covers. Optional.

---

## Dynamic logo sizing (don't skip this)

The Reddit banner is 384px tall — much shorter than FB (624) and Twitter (500). A logo sized as a % of canvas width will overflow vertically on Reddit.

**Compute logo dimensions based on vertical budget**, not width:

```
vertical_budget = H − (top/bottom safety margin)
available_for_logo = vertical_budget − wordmark_h − rule − tagline_h − gaps
logo_w  = min(W × logo_w_pct, available_for_logo / logo_aspect)
logo_h  = logo_w × logo_aspect
```

This guarantees the wordmark + logo + tagline anchor always fits whatever banner height it's given. Without this you get a clipped wordmark on Reddit.

---

## Cover cascade math

For *n* covers in a width *cover_area_w* with cover height *cover_h* and tilt ±max_tilt°:

```
cover_w_approx     = cover_h / 1.6          # standard book aspect
tilt_expansion     = cover_h × sin(max_tilt)
effective_cover_w  = cover_w_approx + tilt_expansion
max_last_left      = cover_area_right − effective_cover_w
step               = (max_last_left − cover_area_left) / (n − 1)
step               = max(step, cover_w_approx × 0.45)   # min 45% non-overlap
```

`tilt_expansion` matters because rotating a cover makes its bounding box wider — without it the last cover's bottom corner clips the canvas.

The 45% floor prevents collapse into an unreadable stack when *n* is large.

---

## Cover selection

By default include all books to advertise the catalog breadth. The author currently has **30+ books across 7 series** so you'll need to be selective — possible curations:

- **Latest from each series** (one book per series, 7 covers) — best for "look at the catalog" framing
- **Featured + supporting** — the highlighted release at front-right, with the rest cascading behind in series-anchor-colour order

Make this configurable via a CLI flag or config file so the author can override per banner.

---

## What from Session B's attempt to discard

- **`brand/scripts/gen_banners.py`** (Session B's version) — wrong fonts, wrong palette, wrong logo, missing Jake Malory variant, missing four of the seven series. Replace, don't refactor.
- **`brand/scripts/enhance_logo.py`** — Session B built this to clean up the legacy gothic-flourish JPG. The canonical `malory-mark.svg` is already vector + correctly coloured, so this enhancer is redundant.
- **`brand/logo/malory-mark-gold-*.png`** — rasterised versions of the wrong logo. Delete.
- **`brand/fonts/`** — Orbitron and Rajdhani TTFs. Deprecated per §4 of the foundation. Delete; Fraunces/Newsreader/Inter/JetBrains Mono are the canon now.
- **`favicon-{16,32,64,180}.png`** and the new `favicon.ico` at the site root — generated from the wrong logo. Delete or regenerate from `malory-mark.svg`.

If any of Session B's `brand/` files don't appear in your working tree, they were correctly never pushed and stayed only in the (now-discarded) `design-v2-by-claude` branch.

---

## Jake Malory variant — when needed

If the author wants a banner that specifically features *Psyker Marine* or *Arcane Galaxy: Chaos Protocols* as the headline book (e.g., for an Audible launch push), the wordmark in the anchor block becomes the Jake Malory lockup (`brand/jake-malory-wordmark.svg`) instead of the umbrella `malory-wordmark.svg`. Everything else stays the same. Worth offering a `--variant jake` flag.

---

## Distribution

Once generated:

- **Facebook**: Page → Edit → Cover photo → upload `fb-cover.jpg`
- **Reddit**: Profile → Settings → Banner image → upload `reddit-banner.jpg`
- **Twitter / X**: Profile → Edit profile → Header → upload `twitter-header.jpg`

All three previews ought to show the wordmark and at least the first 3 covers without crop loss.

---

## One-line summary

> Build three branded banners (FB 1640×624, Reddit 1280×384, X 1500×500), using the canonical Malory brand (Fraunces wordmark, brass #C9A85A accent, `malory-mark.svg` logo, primary-deep background), with a horizontal layout that anchors the left side with the brand block and cascades the catalog covers across the right. Use the dynamic logo-sizing trick so Reddit doesn't clip the wordmark.
