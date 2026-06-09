# Reel 4 — Morgan & Merlin iMessage · Production Brief

**File:** `mm_imessage_reel.mp4` — 11.3s, 1080×1920, 30fps. Messages pop in live (7 timed stills — no keyframes, same drop-in workflow). Opens on typing dots; dots precede every Merlin reply; Morgan's `[Can of Whoopass]` system line pops back instantly — the reply speed is the punchline. Final frame: Merlin typing forever while "he got morgan." lands. 1.5s title card. Silent audio baked in; add trending audio in the IG/TikTok editor, volume low.

## The test
Low density + paced reveal vs the AITA's static ~12-paragraph dump, same series, same account. The pacing means each beat is a retention hook, so watch completion especially. Benchmarks: AITA did 800. **≥800 = thread format wins** → scale across series (push-notification format is the next rung down the density ladder). **≤500 = density wasn't the problem** → next test is format-fatigue (motion).

First card tuned for follower growth: CTA reads "follow for more from the dark ages" (brass-bright), "available now · link in bio" demoted to muted. Want your @handle baked in instead? Say so and I re-render in one pass.

**Watch:** completion % (10s runtime, 5s read — should beat the case file), profile visits and follows per 1k reach vs the AITA, saves/shares as the tiebreaker.

## Post
Thursday 6pm ET / 11pm UK. TikTok crosspost same evening, 1–2h after IG. Comment-pin: "she explains the name choice in chapter 5."

## Trial Reel posting spec (researched June 2026)

**Eligibility first:** trials need a public professional account with 1,000+ followers. If the Trial toggle doesn't appear on the share screen, you're under the bar or not rolled out — post normally with the same spec below.

**Field by field:**
1. **Upload** `mm_imessage_reel.mp4`. No edits needed in-app except audio.
2. **Audio:** pick a quiet trending sound from IG's library, volume low so the text leads. Avoid the actual Stone Cold glass-shatter (WWE copyright) and avoid any sound marked unavailable for professional accounts. IG's 2026 originality scoring favours sounds you haven't all-out copied a trend with — our visual is original, so any ambient trending audio is fine. Note: followers can stumble on the trial via the audio page; harmless.
3. **Caption:** use variant 1 below. Captions are now IG's main discovery signal (keyword SEO — IG and Google index them); hashtags are capped at 5 and demoted to categorisation.
4. **Tags (max 5):** #litrpg #progressionfantasy #isekai #booktok #fantasybooks
5. **Topics (if offered on share screen):** Books & Literature · Comedy · Sci-fi & Fantasy — this drives cold-audience categorisation, which is exactly how trials distribute.
6. **Toggle Trial ON** (final share screen).
7. **Auto-share:** turn ON "share with everyone automatically" — it only fires if the trial performs well on views in the first 72h, which is pure upside for the follower-growth goal. You can flip it off any time.
8. **Cover:** upload `mm_imessage_final_frame.png` from this folder — only matters once it goes public/on-grid, but set it now.
9. **Timing:** trials distribute to cold audiences over 24–72h so the slot matters less than usual; Thu 6pm ET still fine. Trials can be scheduled since Feb 2026 if you'd rather batch.

**Reading the results (24h insights):** views, likes, comments, shares, plus IG's comparison vs your previous trials. Caveat for our ladder: trial views are non-followers only, so don't compare raw views against the receipt/AITA/case-file numbers — those included followers. Compare watch-through, shares, and follows-per-view instead. This trial becomes the baseline for every future format test, which is cleaner than what we had.

**Don't:** delete and repost mid-trial, edit the caption mid-trial, or crosspost the TikTok version with any watermark (we're clean — built from source).

## Captions (pick one — keyword-SEO weighted)
1. her first original technique needed a name worthy of legend. she consulted the sacred texts of 1998. WELCOME TO THE DARK AGES — a LitRPG isekai comedy where a modern woman is reincarnated into Arthurian Britain as Merlin's last hope. book one out now. follow for more from the dark ages.
2. stone cold meets sixth-century cultivation. merlin is not coping. a progression fantasy comedy for readers who grew up on the attitude era. book one in bio. follow for the dark ages with attitude.
3. a modern woman dies, wakes up in dark age Britain, and starts her cultivation legend the only way she knows how. Morgan & Merlin book one — LitRPG comedy meets Arthurian legend. follow for more.

**TikTok tags (unchanged, no 5-cap there):** #booktok #litrpg #isekai #arthuriana #fantasybooktok #attitudeera

## The thread (final copy)
Caption (persistent): *merlin waited 1,500 years for an heir.* Final-frame add: *he got morgan.*

> **Merlin:** A technique's name defines a cultivator's legend for centuries. Choose with great care.
> **Morgan:** `[Can of Whoopass] technique named` *(mono system-message bubble, instant reply)*
> **Merlin:** You could not help yourself, could you?
> **Morgan:** and that's the bottom line. because Morgan said so
> **Merlin:** *(typing…)*

## Canon anchors (manuscript-checked, post-beta docx)
All chapter 12. The Stunner on Tosser ("his chin... shattered with a very satisfying crunching noise"), `[Can of Whoopass] technique named` verbatim, "You could not help yourself, could you?" verbatim, "And that's the bottom line. Because Morgan said so." verbatim. Merlin's lecture compresses his "Techniques are hugely influential in the way cultivators are viewed" speech. Comment-pin: "chapter 12. she kicked him somewhere unsporting first."

## Reel 5, ready to build (same template)
Qi-graffiti thread from ch11: "I leave you alone for one hour." / "i invented a new qi technique" / "Show me." / "it's a giant glowing purple c*ck and balls. in the field" / "future historians will think it's religious" / (typing…). Caption: "merlin recruited her to save the world. this is day three." One command to render.

## Files
Assets: this folder. Renderers: `brand/scripts/render_imessage_mm.py`, `render_titlecard_mm.py` (fonts/cover paths point at this repo; ffmpeg pattern unchanged from the handoff — static concat, no motion).

## Format roadmap (taxonomy folded in)
| Category | Tested | Next best | Theory it tests |
|---|---|---|---|
| 1 Fake-organic native | AITA 800 · iMessage (this) | lock-screen push alert (lowest density), group chat, Google autocomplete | density |
| 2 Receipts/documents | Receipt 1000 · case file 600 | **Bounty receipt — still the pending format-vs-series test** | series effect |
| 3 Data/proof | — | "the math" card or giant-number stat in JetBrains Mono (Punish the System, console green) | new-niche pull |
| 4 Typographic | — | dictionary definition (cheapest build), Craigslist ad (M&M comedy) | hook isolation |
| 5 Analog/handmade | — | handwritten journal page (Soar, noir register) | format fatigue |
| 6 UI/product | — | LitRPG system-message app screen | format fatigue |
