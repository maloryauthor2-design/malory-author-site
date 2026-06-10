# Handoff — Malory's IG/TikTok Reel System (v2)
**Author:** Malory (also **Jake Malory** for Psyker Marine + Arcane Galaxy)
**Updated:** June 2026
**Format thesis:** a single-format vertical Reel whose first frame does NOT look like book marketing — it reads as a native artifact (a text thread, a Spotify-style Wrapped card, a receipt, a case file). Hold it, let it pay off, end on a brand title card. Built as static PNGs concatenated with ffmpeg (no keyframe animation), drop the MP4 into IG/TikTok, add audio in-app, post.

---

## The work in one paragraph
Malory writes indie LitRPG / progression-fantasy / military-sci-fi across six+ series. Goal: reach + follower growth on IG (and TikTok crossposts). We build 10–17s vertical Reels that stop the scroll by borrowing a non-book visual category, anchored in **real manuscript/vault canon** (never the website blurb). The current generation uses **progressive reveal** (messages/stats pop in one at a time) and, for long threads, a **scrolling** chat that clips older messages off the top. Each reel ships with a production brief (copy, canon notes, trial posting spec, captions, hashtags). Everything durable lives in this website repo so nothing is lost between sessions.

---

## Track record (READ THE CAVEAT)
| # | Series | Format | Result | Audience type |
|---|---|---|---|---|
| 1 | Arcane Galaxy / Rivers | Tesco receipt | 1,000 | follower-inclusive |
| 2 | Morgan & Merlin / Morgan | Reddit AITA | 800 | follower-inclusive |
| 3 | Soar / Lowe | case file | 600 | follower-inclusive |
| 4 | M&M / Morgan & Merlin | iMessage (1:1, naming scene) | **600** | **Trial (cold only)** |
| 5 | M&M / Morgan | "537 AD Wrapped" stat card | **400** | **Trial (cold only)** |
| 6 | Arcane Galaxy / Rivers crew | group chat (prison break + boom) | pending | (built, not yet trialled) |

**The caveat that governs everything:** Trial Reels are shown to **non-followers only**, so 4 and 5 (600 → 400) are the only two cleanly comparable numbers. The older 1,000 / 800 / 600 *included existing followers*, so the AG receipt's "1,000" is NOT a fair benchmark for a Trial — AG/Rivers likely has the biggest home crowd, which inflated it. When reading any new Trial, compare **watch-through %, follows-per-view, and shares/saves** against the iMessage (600) and Wrapped (400), not raw views.

---

## What's built this session (all in `brand/reels/`)
- `morgan-merlin-imessage/` — Merlin texts Morgan; she names herself Morgan le Fay. 1:1 thread, progressive reveal. **600 trial.**
- `morgan-merlin-wrapped/` — "537 AD Wrapped": Top Artist Merlin, "my dear ×103", aura "Anxious & Flammable". Spotify-Wrapped homage (no logo). **400 trial.**
- `arcane-galaxy-imessage/` — "The Gazelle" crew group chat: Rivers/Bluey/Henrik break Henrik out of space prison; he'd rather stay; ends on a literal explosion. Scrolling thread + boom. **Ready to trial.**

Each folder has: `*_reel.mp4`, a cover/final frame PNG, `PRODUCTION_BRIEF.md` (the source of truth for that reel — copy, canon, captions, tags, posting spec).

---

## Where everything lives
**Brand source of truth:** `brand/BRAND_FOUNDATION.md` (palette, fonts, title-card spec, per-series anchor colours). Read before designing.
- Pen names: **Malory** default; **Jake Malory** ONLY for Psyker Marine + Arcane Galaxy. AG co-author **Troy Osgood** — credit him.
- Series anchors: Psyker red `#D04848`, Bounty brass `#C9A85A`, Punish console-green `#3DA672`, **Arcane Galaxy electric blue `#3D7FB8`**, Soar steel `#7A8B99`, **Morgan & Merlin violet `#5B3A7A`**, Boys' Own brass-bright `#E0C478`.
- Fonts that actually work in `brand/fonts/`: `Fraunces-VF.ttf` (variable; axes order [opsz, wght, soft, wonk] → set `[144, 600, 0, 1]` for the wordmark), `Inter-Medium-static.ttf`, `Inter-SemiBold-static.ttf`. Poppins (Bold/Medium) is available system-wide for Wrapped-style cards. JetBrains/DejaVu mono for system-message bubbles.

**Renderers (durable):** `brand/scripts/`
- `render_imessage_mm.py` — M&M 1:1 thread, progressive reveal.
- `render_titlecard_mm.py` — M&M title card (Malory wordmark, violet anchor, welcome-cover.jpg).
- `render_wrapped_mm.py` — Wrapped stat card, progressive reveal.
- `render_imessage_group_ag.py` — **reusable group-chat engine**: bottom-anchored scrolling, sender names + coloured avatars, swap the `THREAD` list for any crew/series. Phone-owner = blue/right.
- `render_titlecard_ag.py` — Jake Malory lockup (Jake 400 over Malory 600), Troy Osgood credit, electric-blue anchor, arcane-1.jpg.
- `render_boom.py` — explosion finish (white flash + fireball with radial rays, smoke, debris incl. message-bubble shards, dry payoff caption).

**Covers:** `welcome-cover.jpg` (M&M), `arcane-1.jpg` (AG), plus murder/tower/cuckoo/curator/psyker/pts/boys covers in the repo root.

**The ffmpeg pattern (static stills → MP4):** concat demuxer of timed frames, then concat the title card, silent stereo track for IG compatibility:
```bash
ffmpeg -y -f concat -safe 0 -i frames.txt \
  -f lavfi -t <total> -i anullsrc=channel_layout=stereo:sample_rate=44100 \
  -loop 1 -t 1.6 -i title.png \
  -filter_complex "[0:v]fps=30,setsar=1[v0];[2:v]fps=30,setsar=1[v1];[v0][v1]concat=n=2:v=1:a=0[vout]" \
  -map "[vout]" -map 1:a -c:v libx264 -pix_fmt yuv420p -preset medium -crf 20 \
  -c:a aac -b:a 96k -shortest -movflags +faststart out.mp4
```
`frames.txt` lines: `file '<png>'` then `duration <secs>`, last frame repeated once with no duration. Progressive reveal = one PNG per conversation state; scrolling = bottom-anchor the stack and clip the viewport band.

---

## Canon sourcing — the rules we've burned ourselves on
1. **Never trust the website blurb over the manuscript/vault.** Always anchor lines in real canon.
2. **Check publication state.** Only **Chaos Protocols (AG Book 1)** is out. In the AG vault, every character page has `book:` frontmatter — Leni, Trevor, Gargle, Alvechurch are **Book 2+** and must stay OUT of a Book 1 promo. Book 1 AG crew = **Rivers, Bluey, Henrik**.
3. **Fiction series vaults live under `~/Documents/Claude/Projects/<Series>/`**, NOT the `~/Documents/Obsidian` mount. The AG vault is at `~/Documents/Claude/Projects/Arcane Galaxy/Arcane Galaxy/` (`02 - Characters`, `01 - Canon/Voice Exemplars`, `07 - Writing Reference/Recurring Jokes and Callbacks`). Mount the relevant Project folder instead of asking for the manuscript. (M&M's *Welcome to the Dark Ages* was uploaded as a docx per-session — re-upload if needed, ~120k words.)

---

## Trial Reels — posting spec (researched June 2026)
- Needs a **public professional account with 1,000+ followers**; the **Trial** toggle appears on the final share screen. Trials go to **non-followers**, ~24h of insights, **auto-share** to followers if it performs in the first 72h. Schedulable since Feb 2026.
- **Captions now drive discovery** (keyword SEO — IG and Google index them); write natural long-tail (e.g. "space-western LitRPG", "Arthurian isekai comedy"). **Hashtags capped at 5 on IG**; TikTok uncapped.
- **Audio:** a quiet trending **library** sound, volume low so text leads. **Trademark-safe:** never a Spotify/"Wrapped" branded sound or any branded audio. For the AG reel, add a **boom SFX at ~14.3s** (the flash) — the one place a sting earns its keep.
- Turn auto-share ON (pure upside for follower growth). Set the cover to the reel's `*_final_frame.png`. Topics (if offered): Books & Literature / Comedy / Sci-fi & Fantasy.

---

## House rules — do NOT
1. No motion/zoom/pan/Ken Burns/keyframes. Everything is concatenated static stills (progressive reveal, scroll, and boom are all stills).
2. No CapCut workflow.
3. No emojis in caption/overlay copy (general user pref). No fancy dialogue tags, no "kind of X that Y", no "Not X. Not Y. Z." stacked negation, no intensifiers.
4. Native-artifact frame breaks the brand palette on purpose (Reddit blue, iOS dark, Spotify duotone, fireball orange). ONLY the closing **title card** uses the brand palette.
5. Correct pen name (Jake Malory for AG/Psyker) + co-author credit (Troy Osgood for AG).
6. Keep production briefs short and operational.

---

## Open questions / ranked next tests
1. **Rivers receipt (highest information, still open).** Same series, the proven receipt format, given a *clean cold-audience Trial* for the first time. Isolates "is the receipt the franchise, or was it always the follower base?" The group chat changed both series and format, so it did NOT answer this.
2. **Lock-screen push notification** — the next rung down the density ladder after the iMessage; tests the "density is hurting watch-time" theory directly.
3. **Motion format (Veo 3 / Grok)** — tests algorithm format-fatigue (motion vs static, same hook).
4. **AG Book 2 group chat** — the Leni/Trevor/Gargle "vaporised-the-client-before-payday" thread is written and funny; **hold for the Swashbuckler (Book 2) launch.** Regenerate via the group-chat engine.
5. **More Morgan formats, same vibe** (offered, not built): real **chapter-titles card** (shows her actual prose voice — likely highest book-conversion), **Wikipedia stub**, **Google autocomplete**.

Per-reel, watch: completion %, profile-visits & follows per 1k cold reach, saves/shares as tiebreaker.

---

## How to pick up in a new chat
> "Continuing Malory's IG/TikTok Reel system (indie LitRPG author, Jake Malory pen name for AG/Psyker). Read `brand/reels/HANDOFF.md` and `brand/BRAND_FOUNDATION.md`, plus the `PRODUCTION_BRIEF.md` in whichever reel folder we're touching. Trial results so far: M&M iMessage 600, M&M Wrapped 400 (both cold-audience). AG prison-break group chat is built and ready to trial. I want to test [X] next."

Renderers are in `brand/scripts/`, assets and briefs in `brand/reels/<reel>/`. Swap a `THREAD`/stat list and re-render in one command. The group-chat engine and the boom renderer are reusable across series.
