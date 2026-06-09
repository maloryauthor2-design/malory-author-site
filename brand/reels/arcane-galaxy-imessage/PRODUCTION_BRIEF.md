# Reel — Arcane Galaxy "The Gazelle" crew group chat · Production Brief

**Pen name: Jake Malory** (AG + Psyker only). Co-authored with **Troy Osgood** — credit both. Series anchor: electric blue `#3D7FB8`.

**File:** `ag_imessage_reel.mp4` — 16.7s, 1080×1920, 30fps. iOS **group chat** ("The Gazelle"); bubbles pop in and the thread **scrolls** like a real long chat, builds to "WHICH wall," then a white flash → **literal explosion** (the answer to his question) with the dry button *"he'd rather stay in."*, then the 1.6s Jake Malory title card. All static stills, no keyframes — same drop-in workflow. Silent audio baked in. **Add a boom/explosion SFX in-app timed to ~14.3s** (the flash) — that's the one place a sound sting really pays off; keep a quiet trending bed under the rest.

## ⚠️ Book 1 cast only
**Only Chaos Protocols (Book 1) is published.** Leni, Trevor, Gargle, and Alvechurch are **Book 2+** — keeping them out of a Book 1 promo. The Book 1 crew is **Rivers, Bluey, Henrik**. This reel uses only those three and a Book 1 plot beat (the Chaos Protocol).

## The test
First AG Trial, and the first **ensemble/group-chat** format. Tests whether AG's banter-heavy crew chemistry — the series' headline selling point — carries on a cold audience. Compare against the two clean cold-audience baselines: iMessage 600, Wrapped 400. **Honest caveat:** this does NOT settle the handoff's #1 question (is the *receipt* format the franchise?), because it changes both series and format vs the receipt. If a Rivers receipt is still wanted, that test stays open.

## The thread (final copy)
Caption (persistent): *breaking him out of space prison* · Final-frame add: *he'd rather stay in.*
Group: **The Gazelle** — Henrik live-texting from death row while Rivers & Bluey run the break-in (Ch17–22).
> **Rivers:** Henrik. sit tight, we're breaking you out
> **Henrik:** who is this
> **Rivers:** cell B-24601. that's you?
> **Henrik:** ...yes. how do you have my cell number
> **Bluey:** i'm on the watchtower cannon when you're ready
> **Henrik:** the watchtower has a cannon??
> **Bluey:** not for much longer
> **Rivers:** it's a rescue, Henrik. try to look rescued
> **Henrik:** mate i'm on death row for genocide. better life expectancy in here
> **Henrik:** fewer explosions. more regular meals
> **Rivers:** about that
> **Bluey:** Henrik. move away from the east wall
> **Henrik:** WHICH wall
> **[ explosion ]** — over the fireball: *he'd rather stay in.*

The finish: Henrik complains there are too many explosions; one beat later the wall he's behind becomes one. The blast answers "WHICH wall." Renderer: `render_boom.py` (flash + fireball stills). Cover/poster = `ag_imessage_final_frame.png` (the "WHICH wall" frame, most legible); `ag_boom_frame.png` is the blast.

## Canon anchors (AG vault, Book 1 — every line)
Rivers & Bluey storm the **Camaroke Detention Centre** to rescue Henrik (Ch17–22). Henrik is **Prisoner 24601** (Ch16) → "cell B-24601." Bluey uses the **stolen watchtower cannon** (Ch17–22) → "i'm on the watchtower cannon" / "not for much longer." Henrik's ingratitude is near-verbatim canon: *"thanks for the dramatic rescue, but I think I had a longer life expectancy when I was on death row"* (Voice Bank) → "better life expectancy in here." The closer *"fewer explosions. less shouting. more regular meals"* is his canon line for why death row beat crew life. He's on death row for **genocide** (a hyperfusion cascade that killed a planet + sentient caterpillars, Ch22). Rivers = dry ex-SAS captain; "try to look rescued" is his deadpan register.

## Why this beat
Reluctant-rescue is a universally legible cold-audience hook (everyone gets "the guy doesn't want to be saved"), and it sells the book's actual tone — competent chaos, banter as the engine — better than a plan-planning scene. Bluey's cannon two-beat and Henrik's death-row button are the share-bait lines.

## Voice routing
Rivers = blue/right (his phone). Crew = grey/left with names + avatars: Bluey (teal), Henrik (amber). Both Book 1 crew.

## Trial posting spec
Same as the iMessage brief (`../morgan-merlin-imessage/PRODUCTION_BRIEF.md`): public pro account 1,000+ followers, Trial ON, auto-share ON, cover = `ag_imessage_final_frame.png`, topics Books & Literature / Comedy / Sci-fi & Fantasy. Audio: quiet trending **library** sound, low. Captions carry discovery; 5 hashtags max on IG.

## Captions (keyword-SEO weighted, no emojis; hook on line 1 for the feed cut-off)
**Recommended:**
> breaking the engineer out of space prison is going great. one problem: he'd rather stay on death row.
>
> CHAOS PROTOCOLS is a space-western LitRPG — an ex-SAS operator, an elf pilot, and a crew who can't run a rescue without blowing up a wall. Firefly meets a System that wants them dead. book one by Jake Malory & Troy Osgood, out now.
>
> follow for more from the Gazelle.

**Alt A (POV, good for TikTok):**
> POV: your rescue squad is bickering about a cannon while you're still on death row for genocide. CHAOS PROTOCOLS — a Firefly-flavoured progression-fantasy LitRPG. book one in bio, follow for more from the Gazelle.

**Alt B (explosion button):**
> he said there were too many explosions. so they made another one. CHAOS PROTOCOLS, book one of Arcane Galaxy — space-western LitRPG by Jake Malory & Troy Osgood. follow for more.

**IG tags (max 5, paste at end of caption):** #litrpg #spacewestern #progressionfantasy #scifibooks #booktok
**TikTok tags (no cap):** #booktok #litrpg #scifi #spaceopera #progressionfantasy #firefly #theexpanse

## Files
Assets: this folder. Renderers: `brand/scripts/render_imessage_group_ag.py` (reusable group-chat engine — swap THREAD), `render_titlecard_ag.py`. Swap any bubble and re-render in one command.

## Book 2 version (hold for later)
The vaporised-client / Leni-Trevor-Gargle group chat is written and funny — save it for when Book 2 (Swashbuckler) launches. It's archived at the bottom of `brand/scripts/render_imessage_group_ag.py` history / ask me to regenerate.
