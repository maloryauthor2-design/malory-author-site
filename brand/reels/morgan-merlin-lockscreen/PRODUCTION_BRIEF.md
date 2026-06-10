# Reel 7 — Morgan & Merlin lock screen · Production Brief

**File:** `mm_lockscreen_reel.mp4` — 11.1s, 1080×1920, 30fps. iOS lock screen ("Thursday, 537 AD", clock 5:37) receiving three notifications, newest on top. All static stills, no keyframes; 1.6s Malory title card (reused from the iMessage reel). Silent audio baked in — add a quiet trending library sound in-app, volume low.

## The test
**The cleanest A/B we have run.** Same series, same account, same ch12 scene, same verified canon lines as the 600-view iMessage trial — only the format changed, to the lowest rung on the density ladder (3 notifications vs 5 bubbles, 11.1s vs 11.3s). Trial pools are non-followers only, so reusing the scene is safe.

**Why now:** AG group chat trialled at **200 with 4 likes, 0 saves, 0 shares** — zero share signal, so no second distribution wave. Cold trend is monotone in density: iMessage (5 msgs) 600 → Wrapped (stat card) 400 → group chat (13 msgs, scrolling) 200.

**Decision rule:**
- **≥600** → density confirmed as the lever. Scale low-density formats across series; Rivers receipt next (series test).
- **400–600** → format-neutral; M&M itself is the asset. Build more M&M, any low-density format.
- **≤300** → density wasn't it; the whole text-artifact category may be fading on this account. Next test = format-fatigue (motion, Veo/Grok) or profile-funnel fixes before more trials.

**Watch (not raw views):** completion % (11s runtime, light read), saves/shares (the wave trigger — AG's failure mode), follows per 1k cold reach. Screenshot insights at 24h.

## The screen (final copy — newest on top)
Persistent caption: *merlin waited 1,500 years for an heir.* Final-frame add: *she chose with great care.*

> **MESSAGES · Merlin:** A technique's name defines a cultivator's legend for centuries. Choose with great care.
> **CULTIVATION SYSTEM** (violet icon, mono): `[Can of Whoopass] technique named` — pops instantly, the reply speed is the punchline
> **MESSAGES · Merlin:** You could not help yourself, could you?

## Canon anchors (manuscript-checked, ch12 — identical set to the iMessage reel)
All three lines verbatim from chapter 12 (verified for Reel 4). The closing caption echoes Merlin's own "Choose with great care." Comment-pin: "chapter 12. she kicked him somewhere unsporting first."

## Trial posting spec
Same as `../morgan-merlin-imessage/PRODUCTION_BRIEF.md`: public pro account 1,000+, Trial ON, auto-share ON, cover = `mm_lockscreen_final_frame.png`, topics Books & Literature / Comedy / Sci-fi & Fantasy. **Space it 24h+ from any other trial** — trials posted close together cannibalise the same non-follower pool. Audio: quiet trending library sound, low.

## Captions (keyword-SEO, no emojis; max 5 IG tags)
**Recommended:**
> merlin spent 1,500 years preparing to train the next great cultivator. her first original technique is named after a stone cold stunner.
>
> WELCOME TO THE DARK AGES — a LitRPG isekai comedy where a modern woman is reincarnated into Arthurian Britain as Merlin's last hope. book one out now. follow for more from the dark ages.

**Alt:**
> she chose with great care. WELCOME TO THE DARK AGES — Arthurian isekai comedy meets progression fantasy. book one in bio. follow for the dark ages with attitude.

**IG tags:** #litrpg #progressionfantasy #isekai #booktok #fantasybooks
**TikTok tags:** #booktok #litrpg #isekai #arthuriana #fantasybooktok #attitudeera

## Files
Renderer: `brand/scripts/render_lockscreen_mm.py` (swap NOTIFS for any series — Messages + one custom app icon per notification). Title card reused: `../morgan-merlin-imessage/mm_titlecard.png`. ffmpeg pattern unchanged.
