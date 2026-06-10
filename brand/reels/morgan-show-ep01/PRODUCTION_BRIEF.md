# THE MORGAN SHOW — Episode 1 · Production Brief

**File:** `ms_ep01_reel.mp4` — 12.6s, 1080×1920, 30fps. iMessage thread from contact "Unknown" (the reveal that it's Merlin IS the punchline), violet "537 AD · ep 1" badge on every frame, series title card with next-episode tease. Static stills, silent audio baked in — add a quiet trending library sound in-app, low.

## The show premise (what's new vs every previous reel)
This is episode one of a weekly series, not a one-off. The follow logic: badge signals a catalog, the title card promises a specific next episode, fresh canon every week means auto-share never confuses followers. Spine for cold viewers: she is becoming THE Morgan le Fay.

## The thread (final copy)
Caption (persistent): *she woke up dead on a battlefield in 537 AD.* Final-frame add: *the legend of Morgan le Fay starts here.*

> **Unknown:** Don't move.
> **Unknown:** If you move, they will see you still live, and then they will kill you.
> **Morgan:** Who are you, and what do you want with my dead arse?
> **Unknown:** There is absolutely nothing about your arse that interests me. My name is Merlin, and I am going to need you to help me save the world.

Title card: "the morgan show · episode one" + tease *"next episode: morgan tells a joke. merlin pretends not to get it."* (cadence-neutral on purpose — the schedule lives in the caption/bio, not baked into assets).

## Canon anchors (post-beta docx, ch1 — checked this session)
All four bubbles verbatim from the chapter 1 recruitment exchange, with two compressions: Morgan's line drops her crow preamble ("oh voice with the skill to cremate crows..."), and Merlin's closer drops its opening clause ("I am more than happy to enlighten you, my dear. But, to reassure you, ..."). The chapter ends on that line — it is the book's actual hook. Comment-pin: "chapter one. the wizard had just flash-fried a crow that was about to eat her eye."

## Trial posting spec
Standard (see `../morgan-merlin-imessage/PRODUCTION_BRIEF.md`): public pro account, Trial ON, **auto-share ON — and if it has not auto-shared by 72h, share to everyone manually.** Followers must not miss episodes of a show. Cover = `ms_ep01_final_frame.png`. Topics: Books & Literature / Comedy / Sci-fi & Fantasy. 24h+ from any other trial. **Cadence: 3 episodes a week — Mon/Wed/Fri** (2026 data: daily lifts reach ~40% but 3–5/week is the small-account sweet spot; quality and early engagement beat volume, and daily would burn the 15-gag season in two weeks). Reassess at ep 6 with follows-per-1k data; go daily only if gag quality holds and Books 2–3 are mined.

## Captions (keyword-SEO, no emojis)
**Recommended:**
> a wizard texts "don't move" to a woman who just woke up dead on a battlefield. episode one of the morgan show.
>
> WELCOME TO THE DARK AGES — a LitRPG isekai comedy where a modern woman is reincarnated into Arthurian Britain as Merlin's last hope, on her way to becoming THE Morgan le Fay. book one out now.
>
> new episodes monday, wednesday, friday. follow for episode 2: morgan tells a joke, merlin pretends not to get it.

**Alt:**
> day one of being dead in 537 AD and the legendary wizard is already setting boundaries. the morgan show, episode one. WELCOME TO THE DARK AGES, book one out now. follow for episode 2.

**IG tags (max 5):** #litrpg #isekai #progressionfantasy #booktok #fantasybooks
**TikTok tags:** #booktok #litrpg #isekai #arthuriana #fantasybooktok #morganlefay
TikTok: add episode to a "the morgan show" playlist. IG: if the Series tab (Meta test, June 2026) appears on the account, create the series and add this as episode 1; pin eps 1–3 to the grid as they ship; put "the morgan show — new episodes mon/wed/fri" in the bio. Show art in `../morgan-show-brand/`: movie-poster covers `morgan_show_poster_1080x1920.png` / `_1080x1080.png` (primary — Series hub, playlist, pinned anchor; built by `render_show_poster.py` from the full-res cover in `~/Downloads/book-links-app/public/`), plus the typographic bubble cards `morgan_show_cover_*` as alternates.

## Reading results
Follows per 1k cold reach is THE metric, then profile visits, saves/shares (wave trigger), completion. Compare against iMessage 600 / Wrapped 400 / group chat 200 (4 likes, 0 saves, 0 shares). Screenshot 24h insights.

## Files
This folder: reel, final frame (cover), series title card. Renderer: `brand/scripts/render_morgan_show.py` — swap the EPISODE dict for ep 2 (slate + verbatim lines in `../SEASON_ONE.md`) and re-render in one command.
