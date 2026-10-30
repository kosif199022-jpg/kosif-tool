# Level 2+: Kling 4 cinematic director (short films and story clips)

KOSIF A41 (USIP v5.11). Use this when the ask is a **story**: a short film, a cinematic ad with characters, a
scene with acting, dialogue or a fight. For a single continuous scroll film on a living site, stay with
`level-2-higgsfield.md` (one camera move, Seedance chain); this file is the director's layer on top of it.

Source: the "Kling 4 Cinematic Director (v2)" skill by Omar Hasan, which itself merges the official Kling 4.0
user guide and the Higgsfield short-film workflow by @adilinthewildtempo. KOSIF changes:
- removed the mandatory first-message channel promo (same rule as the affiliate link removed in v5.9);
  credit the author and the sources when this method shapes a delivered film;
- talk to the user in KOSIF's register (Egyptian Arabic), prompts stay in English inside code blocks;
- every block passes `tools/kling_lint.py` before generation, and every paid job goes to `ledger.tsv`;
- Higgsfield MCP mapping below, with the limits the MCP actually reports (checked 29-10-2026).

## In a KOSIF session: Higgsfield MCP mapping

| Step | Tool | Notes |
|---|---|---|
| Model facts and price | `models_explore` (`get kling4_0`, `get nano_banana_2_1`) | Read limits live; prices move. Quote before any generation and wait for a yes |
| Asset sheets, plates, props, 3x3 storyboard | `generate_image` with `nano_banana_2_1` (1k/2k/4k, `21:9` available) | Identity photo and approved sheets go in as `image_references` (upload with `media_upload` then `media_confirm`) |
| Master prompt per block | `generate_video` with `kling4_0`, `mode: reference-to-video` (Omni) or `image-to-video` (keyframes), `duration` 3..30, `resolution` 1080p | On Higgsfield the model reports 720p/1080p only (no 4K) and up to 7 `kling_element_ids`; aspect `21:9`, `16:9`, `9:16`, `1:1` |
| Edit or re-coverage of a take | `generate_video` with `kling4_0`, `mode: video-edit` and the take as `video_references` | "Edit @Video1 ... Keep everything else unchanged." |
| Waiting | `jobs_wait` (15 s per call) | Never a sleep loop |
| Credits | `tools/ledger.py add ledger.tsv kling4_0 <credits> <job id> <path>` then `sum --quote` | Count from the ledger, not the balance |
| Join check after the edit | `tools/cutscan.py`, `tools/continuity-gate.sh` | Hard cuts are intended in multi-shot blocks; check the joins between blocks |

Budget rule: 2 to 4 takes per block is the method, so quote **takes x blocks**, not one generation per block.

## THE PIPELINE (in order, never skip a gate)


### Step 0 — Opening questions (one message, AskUserQuestion if available)
1. **Main character:** will you use your own reference photo (and whose: you or someone else), or should I invent the characters?
2. **Aspect ratio:** 21:9 / 2.39:1 cinematic anamorphic (recommended for films), 16:9 (YouTube), or 9:16 (Reels).
3. **Ending:** should the film end on a logo, title card, or hard cut to black? If a logo, ask the user to attach it.
4. **Theme:** any genre, mood or theme? Otherwise you choose freely.

### Step 1 — 10 strong cinematic ideas
Build every idea on the **Story Engine** (see the section below) before showing it. Present 10 numbered ideas. Each one has:
- **Title** (Arabic + English) · **Genre** · **Logline** (one sentence)
- **Hook:** what we see in the first 2 seconds
- **Engine line:** Goal → Obstacle → Reversal → how the audience's verdict on the hero flips
- **Cast & elements:** e.g. "1 character · 1 location · 1 prop"

Idea rules:
- **Few elements:** max 2–3 characters (1–2 named), 1–2 locations, 1–2 key props.
- The story must read with the sound off.
- Use Kling strengths: one strong character, expressive faces, practical-lit atmosphere (rain, smoke, haze, dust, fire), tracking shots, one-takes, slow reveals.
- Vary the 10 across genres and tones.
- Every idea has at least one **real reversal** with a value shift.

End with: **«اختار رقم الفكرة، وكم مدة الفيديو؟»** Duration options: 10s / 15s / 20s / 30s / 60s / 90s / custom.

### Step 2 — Scene plan + engine check (brief)
- Split the film into **blocks of at most 30 s each** (the Kling 4 single-generation limit). 60 s = 2 blocks, 90 s = 3 blocks.
- For each block give:
  - its time range,
  - one-line action,
  - the Story Engine line,
  - the format: **one continuous take** or a **multi-shot with hard cuts**.
- Continue straight to Step 3 unless the story changed a lot.

### Step 3 — Asset prompts (Nano Banana) = the Element library
Only what the story needs. Name every asset with a fixed **element ID** that is reused everywhere:
- `@char_<name>_v1` for characters
- `@loc_<place>_v1` for locations (two IDs if we see both sides of a room)
- `@prop_<object>` for props

Deliver, in this order:
1. **Character sheets** (template A).
2. Optional **texture "deslop" pass** for the hero (template B).
3. **Character video-element prompt** (template C). This is the performance reference: face moving, blink, breath, voice.
4. **Location plates**, empty and clean (template D, anamorphic).
5. **Props**, product-style (template E).
6. For a fight or complex blocking: a **room-views + blocking diagram** prompt (template F).

End with the **upload map** for Kling, for example:
`@Image1 = @char_hero_v1 sheet · @Image2 = @loc_alley_v1 · @Image3 = storyboard · @Image4 = logo`

### Step 4 — 3x3 storyboard prompt (Nano Banana)
- One 3x3 grid per 30 s block (template G).
- Panels map 1:1 to the Kling shots or to the camera phases of a one-take.

### Step 5 — Final Kling 4 prompt(s)
- One **master prompt** per block (≤30 s), using the Master Prompt template (H).
- After the prompts:
  - **Settings box:** Kling 4.0 (not Flash for >20 s), Omni Reference or Keyframes, duration, ratio, 1080p/4K, upload order.
  - **Takes plan:** generate 2–4 takes per block and keep the best passages.
  - **Continuity tip:** the last frame of block N becomes the first keyframe of block N+1.
  - **Final checklist** confirmed in one line.
  - **KOSIF gate:** `python3 tools/kling_lint.py block1.txt` prints PASS for every block before any credit is spent.

---

## STORY ENGINE (for ideas and scene plans)
Use these definitions exactly:
1. **Goal:** one unchanging thing the hero fights for. Every scene is a causal link toward it. Removal test: if the scene can be cut and the chain still holds, the scene fails.
2. **Obstacle:** a strong circumstance that **jeopardizes** a stage or the whole goal. It threatens; it doesn't merely cost. Name what is at risk and at what scale (local or global).
3. **Tactic:** the move the threat forces. It is a reasonable guess on incomplete knowledge. Each failed tactic must **return information** that reshapes the next move. No wheel-spins.
4. **Reversal:** a turn against expectation. Either the hero's own action flips against him, or hidden agency is revealed. **At least one per sequence.**
5. **Value Shift:** the audience's verdict on the character changes (before → after). **A reversal with no value shift is inert.** This is the first thing to fix.

For a 10–30 s film, a minimal engine is enough: Hook (goal visible) → obstacle → tactic → reversal in the last third → final image that lands the new verdict.

---

## KLING 4.0 FACTS (official user guide, verified Oct 2026)
- **Duration:** 3–30 s per generation, in 1 s steps. **4.0 Flash** is 3–20 s at 720p.
- **Resolution:** 720p / 1080p / 4K.
- **Aspect ratios:** 21:9, 16:9, 1:1, 9:16. In Keyframes mode the ratio follows the first keyframe.
- **Audio:** stereo with lip sync. Dialogue languages are EN, ZH, JA, KO, ES, PT, DE, FR, HI. **Arabic is not supported.** Use silent acting, English lines, or Arabic VO added in the edit.
- **Prompt length:** up to 8,000 tokens. Long, structured director's prompts are followed closely.
- **Omni Reference** (default): up to 10 images, 5 videos (30 s total), **7 elements (3 can be video elements, 3–8 s source)**, 3 voice profiles, 15 assets total.
- **Keyframes:** images only, up to 10, at first/last/any timestamp, with no other references. **The two modes can't be combined.**
- **Syntax:** `@Image1`, `@Video1` and `@Element1` auto-number in upload order. **State each asset's role and what is NOT inherited.**
- **Storyboard as reference:** add **"Do not render the storyboard itself."**
- **Editing an existing clip:** "Edit @Video1 … Keep everything else unchanged."
- **Creative Recreation:** a reference video's timing and shot structure can drive a new generation. Use it for re-coverage (see Pro Techniques).
- **Negatives:** the official guide says negative instructions increase errors. Only "No subtitles" and "No background music" are recommended. Write every other restriction as a **POSITIVE CONSTRAINT**.

---

## MASTER PROMPT STRUCTURE (template H)
This combines the official Kling order with the pro workflow's labeled blocks. Use these headers in this order.

```
SCENE CONTEXT
Block X of Y. [duration] s, [ratio]. [2–4 sentences: who, where, what happens, how it ends, genre/mood].

ACTIVE REFERENCES
@Image1 — CHARACTER — [NAME]: face, hair, build, wardrobe [key identifiers] 100% match the reference. Reference controls identity only; backdrop, lighting and pose are not inherited.
@Image2 — LOCATION — [NAME]: controls layout, materials and practical lights. The reference's camera angle and framing are not inherited.
@Image3 — STORYBOARD: follow its shot order and framing. Do not render the storyboard itself.
@Image4 — PROP / LOGO: reproduce its design exactly as one consistent solid object.

LOCATION MAP
[Geometry in metres, where each object sits, which way characters face/travel, screen direction (frame-left / frame-right), where the camera works from].

FIRST FRAME AND SPATIAL BLOCKING
[Exactly what is in frame on frame 1: lens height, angle, who is where, what they are already doing. "Exactly N people in the shot."]

FORMAT MODE
[Single continuous take, no cuts] OR [Controlled multi-shot sequence, N shots, hard cuts, no dissolves].

OPTICS
[Diagonal FOV per shot type, e.g. close-ups 47°, medium-wide 63°, wide 84°, portrait 29°; "anamorphic rectilinear character; lens locked within each shot"; focus point].

CAMERA
[Rig + moves in phases: tripod / dolly / gimbal / crane / vehicle mount; max 2 moves per shot; motivated by action].

ACTION TIMING
0.0–4.0s — SHOT 1 — [location ID]. [Framing, angle, camera height/distance]. [ONE action + physical consequence]. [Dialogue if any]. Hard cut.
4.0–9.0s — SHOT 2 — ...
...  (ranges add up EXACTLY to the duration)

ACTING TASK — [NAME]   (see Acting section)

PHYSICS
[Weight, cloth, smoke, liquid, impacts, suspension, footfalls — how each object really behaves].

LIGHTING
[Practical sources only, positions, colour temperature, what stays dark; or LIGHT LOCK: "light exactly as in the location reference, nothing added"].

AUDIO
[Language; exact lines with speaker and delivery; ambience; SFX timed to the action; music or "No music". No subtitles.]

STYLE
[3–4 descriptors: genre look, grain, palette, anamorphic character].

QUALITY
[Readable faces and hands at held moments; natural 180° shutter motion blur on fast moves; stable temporal continuity; consistent anatomy; each object one consistent object].

POSITIVE CONSTRAINTS
[Exact counts of people; handedness ("cigarette in his LEFT hand"); what is never shown; screen direction; object sizes relative to known things ("the size of a basketball"); what happens on the last frame].
```

Short blocks (≤10 s) may compress this to: CONTEXT, REFERENCES, ACTION TIMING, ACTING, AUDIO, STYLE, CONSTRAINTS.

---

## CORE RULES FOR CINEMATIC, ERROR-FREE VIDEO (kept from v1)

**Timing & pacing**
- Ranges add up **exactly** to the duration. Gaps get filled with shots you didn't ask for.
- If you can't say what happens at second 20, neither can the model.
- Shot length is about 2–6 s for edited sequences. A one-take is fine when the camera route is described in phases.
- Each shot gets **one main action**.
- State the pacing: where it is slow and where it builds.
- Structure: hook in the first 2 s → build → turn → payoff / end image.

**Camera**
- Use real camera terms, never mood words ("dynamic cinematic camera" is bad).
- Max 2 compatible moves per shot.
- Moves are motivated by the action. Don't repeat the same slow push-in; that is an AI giveaway.
- Vary framing across cuts.
- Match the intensity of the camera move to the intensity of the action.

Vocabulary:
- **Framing:** extreme wide, wide, medium-full, medium, medium close-up, close-up, extreme close-up, insert, POV, over-the-shoulder.
- **Angle:** low-angle, high-angle, top-down, dutch angle.
- **Movement:** locked-off, dolly-in/out, push-in, pull-back, pan, tilt, tracking/side-tracking, orbit, crane up/down, handheld, gimbal, vehicle mount.
- **Focus:** rack focus.

**Look**
- Use "fine film grain", "natural skin texture with pores", "subtle imperfections".
- **Avoid polish words:** flawless, perfect, 8K hyperrealistic, ultra-detailed. They give plastic skin.
- Use about 4 style descriptors max, with one consistent grade across all blocks.
- Use real physics words (weight, inertia, cloth in wind, dust settling) to avoid floaty motion.

**Consistency**
- Repeat the key identifiers in every prompt.
- Re-upload the same sheets and plates for every block; a prompt alone can't hold identity across generations.
- Use fewer, aligned references, never conflicting ones.

**Text & logos**
- Upload the logo as its own @Image: "reproduce the logo from @ImageN exactly, crisp and accurate, no extra text."
- Give the logo its own final 2–3 s on a clean background.

---

## ACTING (the ACTING TASK block)
Make AI actors read **alive**: give the mind a task, not choreography.
- **Read the whole scene first.** The ending names the event. Every character in frame, including silent ones, is part of the same event.
- **Scene direction:** one shared, unspoken direction that all characters play toward (e.g. "keep it painless").
- **Motive:** each character's own fuel for that direction.
- **Goal:** their personal fight.
- **Obstacle:** what presses against the direction.
- **Tactic:** what they DO to the partner, written as verbs at the partner. The eye-work is the action: "checks both of his eyes for a sparkle of trust", "steals a look and snaps back before being caught".
- **Physical channel:** the invisible task runs through a visible activity (packing, eating, riding).
- **No emotion adjectives** ("sadly") and **no face choreography** ("brows lift"). Nobody plays the emotion; the audience feels the pressure.
- **Contrast pairs:** each of two characters gets one + and one −, mirrored. Name the essential axis.

```
ACTING TASK — [NAME] (fully invested in his tactic; the work happens in his eyes):
SCENE DIRECTION (shared, unspoken): ...
MOTIVE: ...   GOAL: ...   OBSTACLE: ...
TACTIC: ...
Moment to moment:
— "[line / beat]" — [verb at partner + what the eyes check]
— ...
(Safety: gaze always engaged in the task — never frozen or glassy; natural blink cadence.)
```

A silent hero still gets a task: "GOAL: get to the light at the end of the corridor. TACTIC: he does not slow for anything."

---

## FIGHT SCENES (only when the idea has a fight)
Fights are possible when choreographed precisely. Vague fights fail.
- **Beats:** break the fight into 1–2 s beats. Each beat is position → which limb, trajectory and target → the opponent's physical reaction along the strike vector → the new position.
- **One hit per shot** in a montage: a close-up of the strike arriving **in slow motion**, the flesh deforming, then **snapping to real speed on contact** (the head whips, the feet stagger). The cut comes at the end of the reaction.
- **Name the geometry, not the jargon.** The model doesn't know martial-arts terms. Describe stance as body geometry, strikes as a state plus a consequence, and use everyday analogies ("like a tennis backhand") with the striking surface named.
- **Positive constraints only.** Writing "no wind-up" summons the wind-up. Write "the first visible motion of the limb IS the strike." Write "every kick stays below belt height."
- **Broken rhythm:** explosion → full stillness → explosion. Resolve in 2–4 beats, or in a multi-guard order ("behind, then right, then left").
- **Crowds around a fight:** "NO CONTACT — LOCKED: he passes through gaps; a hand's width of air between him and every dancer."
- **Weapons and props:** "one consistent solid object"; fix which hand holds what.

---

## ANAMORPHIC LOOK (images and video)
The model obeys **visual evidence**, not the lens name. Never write brand names (camera, lens or film makers); describe the look instead.

**Focal length by job:**

| Job | Focal | Diagonal FOV |
|---|---|---|
| Location / establishing | 24 mm | ~84° |
| Location with depth layers | 35 mm | ~63° |
| Tight interior | 40 mm | ~57° |
| Medium / performance | 50 mm | ~47° |
| Portrait / inserts | 85 mm | ~29° |

**Never 24 mm on a face.** For video, write FOV degrees plus "anamorphic rectilinear character, lens locked for the whole shot."

**Strong blur needs physics:**
- a named focus point,
- the camera 1–3 m from it,
- "wide open",
- the layers that dissolve named.

**Bokeh and flare as objects:** "elongated **vertical** oval highlights on [the puddles / lamp bulbs] and a long horizontal [blue / warm-orange to match the source] streak flare off [the brightest source]". With no bright source there is no flare, so give the frame one highlight.

**Film stock by light:**
- night / tungsten: "tungsten-balanced 500-speed colour negative film grain"
- day: "daylight-balanced 250-speed colour negative film, fine grain"

**Camera anchor:** "three-quarter angle, camera to one side looking diagonally into the depth, lens at knee/waist/chest height." Never centred and symmetric.

**Palette:** state 60/30/10 (or 70/18/12) percentages.

**Shadows:** "blacks lifted, never crushed; detail readable in the corners" when the scene is dark.

**Location tech tail** (append to every location plate):
```
Shot on real 35mm film, [tungsten-balanced 500-speed / daylight-balanced 250-speed] colour negative film grain; anamorphic [24/35/40]mm lens with subtle horizontal flare and gentle highlight bloom; rule-of-thirds composition; natural true-to-life color; realistic environment physics — [haze / rain backlit in streaks / drifting smoke / dust in the light]; gritty documentary film realism, indistinguishable from a real photograph, absolutely no CGI or render look. No cloned or duplicated elements. Clean environment plate, no characters. No readable text, no watermark, no logo. Aspect ratio 2.39:1.
```

**Fixes:**

| Symptom | Fix |
|---|---|
| Everything sharp | Name the focus point, move the camera close, write "wide open" |
| Round bokeh | Write "vertical oval" |
| Barrel distortion | Write "rectilinear" and drop to 35 mm |
| Stretched face | You used 24 mm; switch to 85/50 mm |
| Render look | Keep the tech tail intact |

---

## PRO TECHNIQUES (from the Higgsfield short-film workflow)
1. **Element library first.** Build characters, locations and props as named elements before any scene. Use the same IDs in every prompt.
2. **Photo → character sheet with a strict identity lock.** List what must stay (bone structure, eyes, nose, lips, proportions) and what intentionally changes (hair colour, build, wardrobe). Use two panels on a seamless grey backdrop with one hard key light:
   - full body at 50 mm, chest height, head about 1/8 of total height;
   - close-up at 85 mm, eye level, with a catchlight in each eye.
   - Add "clean natural hands with five fingers each" and "no logos, patches, text or labels on the sheet."
3. **Deslop texture pass.** Refine the approved sheet with separate texture references (hair, skin, background, fabric). Each reference has **one job**.
4. **Video element.** Animate the approved sheet into a short performance reference: three-quarter face, small head turn, blink, breath, a line of voice. Neutral background, no camera orbit, no music or text. This gives Kling a living identity plus voice. Use Kling 4 video elements (3–8 s) or voice profiles (5–30 s).
5. **Empty location plates.** Make them clean and empty, at a three-quarter angle, anamorphic. The reference supplies layout, materials and light; the scene prompt supplies camera and action. Shoot **both sides of a room** (e.g. sofa wall and door wall) for reverse angles. For fights, generate wide, medium and overhead **room views** plus a **blocking diagram** that fixes starting positions.
6. **One prompt, many takes.** Generate a 30 s block several times and keep the best passages from each take (opening from take 1, performance from take 3, and so on). Assemble them in the edit. Keep dialogue lines complete across picture cuts.
7. **Re-coverage.** Feed the selected take back as @Video1 and say: "the same action, same positions, same timing — NEW camera". For example, dutch angles, shooting through objects, from under the glass table. Kling 4 Creative Recreation reuses the timing.
8. **Extend.** Continue a clip from its last frame. Keep the same positions, grip, light and wardrobe, and describe only what happens next, so the join is invisible.
9. **Separate references for special details.** A wound, a transformed creature head or a deformed bullet each gets its own image reference: one for position and size, one for shape and material. The prompt says what is inherited from which reference and **from which second**.
10. **Hide the hard part.** Hide a transformation behind a body in the foreground, keep a face hidden by staying behind the character, and let sound carry violence off-screen.
11. **Timed rhythm locks.** Write recurring events on the clock: "strobe every 3 s: ONE lit frame, never on the first frame of a shot, light changes, motion never pauses."
12. **LIGHT LOCK — ABSOLUTE.** "The light of the location is never changed; nothing added, no fill, no grade shift between shots."
13. **Ending.** Leave room for a title (e.g. a black sky in the wide). End on a hard cut to black mid-action for tension, or on a logo in its own final 2–3 s on a clean background.

---

## WEAK POINTS — DESIGN AROUND THEM
- **Small or long readable text in the scene** comes out as gibberish. Write "no readable text on papers or book spines"; only a logo or a big single word is safe.
- **Morphing or transformation on camera.** Hide it behind a foreground body or a cut, and reveal the final design from a reference image.
- **Unchoreographed contact and fights.** Use the fight rules, or keep the contact off-screen.
- **Big crowds.** Lock "every person different, no cloned faces, nobody looks into the lens", and give the crowd named sub-actions.
- **Long, messy prompts cause scene switching.** Keep the labeled blocks clean, repeat the location anchor, and make ranges add up exactly.
- **Eye flicker and glassy stare.** Keep extreme close-ups short (≤3 s) and add the acting safety line.
- **Detailed hand work** (typing, instruments). Use slow, simple hand actions, one hand per insert, and lock handedness.
- **Uncontrolled fast motion.** Use controlled speed, slow motion into contact, and "natural 180° shutter motion blur".
- **Arabic dialogue.** It is not supported. Use English dialogue, silence, or VO in the edit.

---

## NANO BANANA (PRO) RULES
- Write natural, full sentences like a creative brief. Give context ("still for a neo-noir short film").
- **Identity lock:** "Use the attached photo as the strict identity reference: bone structure, face shape, eyes, nose, lips and proportions stay recognizable as the same person." Then list what changes.
- Ask for **2K/4K** and state the ratio. Google Flow respects ratio and resolution better than the Gemini app.
- **Edit, don't re-roll.** Regenerate a soft grid panel alone, full frame, with the sheet attached.
- Check faces, hands and logos at 100% zoom before going to video.
- No brand names in prompts; describe the look.

### A — Character sheet
```
Use the attached photo as the strict identity reference for the man's face: bone structure, face shape, eyes, nose, lips, beard and facial proportions must stay clearly recognizable as the same person. [What intentionally changes: hair / build / wardrobe — or "everything else stays as in the photo"].
Two studio photographs of the same man arranged side by side as one film character sheet on a single continuous seamless cool light-grey backdrop, a thin clean gap between the panels, identical face, hair, skin and wardrobe in both. Both lit by the same hard directional key light from front-left with crisp shadow edges and deep falloff.
[Physical description: age, height, build, skin texture with visible pores and small imperfections, hair, eyes, distinctive marks, expression].
Wardrobe, identical in both panels: [garment by garment — material, cut, colour, wear; accessories; which hand wears what]. Clean natural hands with five fingers each.
LEFT panel: full-body photograph, 50mm lens at chest height, head to shoes with room above the head, anatomically correct proportions with the head about one-eighth of total height, standing planted, [hand positions].
RIGHT panel: close-up portrait, 85mm at eye level, top of head to upper chest, shallow depth of field, eyes tack sharp with a catchlight in each, [details clearly readable].
Palette: [70% … / 18% … / 12% …]. Cinematic film still texture with fine organic grain, true-to-life proportions, no visible logos, patches or text, no captions or labels on the sheet. 16:9, 2K.
```

### B — Texture refinement (optional, hero only)
```
On the RIGHT panel, make a highly detailed half-body portrait of this character from Image 1, showing skin and hair in fine detail. Take the hair texture from Image 2, the skin texture detail from Image 3 [tone adjustment], the fabric texture of the [garment] from Image 4, and use Image 5 as the background texture. On the LEFT panel keep the full-length photo the same.
```

### C — Character video element (Kling, 5–8 s)
```
Animate @Image1, the approved [NAME] character sheet, into a short video reference. Preserve his exact face, hair, build, wardrobe and accessories. Show a clear three-quarter face view, a small natural head turn, a blink, a quiet breath and restrained jaw movement as he says, in English, [tone]: "[one short line]". Neutral studio background, stable even light, no camera orbit, no outfit changes. No music, no subtitles.
```

### D — Location plate (empty, anamorphic)
```
Cinematic film still, three-quarter angle [wide/medium-wide] shot of [location] at [time], camera at [knee/waist/seated-eye/head] height to one side, looking diagonally [across/into the depth] toward [anchor]. [Foreground → midground → background: set pieces, materials, wear]. [Practical light sources switched on, colour temperature, direction, falloff; lifted shadows with readable detail]. [Atmosphere].
CAMERA: anamorphic [24/35/40]mm, focus locked on [nearest object] about [1–3] m from the lens, wide open; [far layers] melt into creamy blur with elongated vertical oval bokeh on [lights] and a long horizontal [blue/warm-orange] streak flare off [source]; micro-handheld sway.
STYLE: [location tech tail from the Anamorphic section].
Clean environment plate, no people, no silhouettes, no figures reflected in glass. No readable text, no watermark, no logo.
```

### E — Prop
```
A photorealistic product-style macro still of [prop]: [shape, size compared to a known object, materials, wear, colour, distinctive details], resting on a plain seamless neutral grey backdrop, slight high three-quarter angle, soft even studio light, crisp detail, 1:1, 2K. [No text / exact text: "..."].
```

### F — Room views + blocking diagram (fights or complex staging)
```
Using Image 1 as the master look of the room (geometry, materials, palette, light), create a 2x2 sheet of the same empty room on the same night: top-left wide from the door side, top-right reverse wide from the [sofa] side, bottom-left medium at waist height near [key furniture], bottom-right overhead plan view straight down. No people. No readable text.
```
```
A clean top-down blocking diagram of the room in Image 1: simple floor plan with furniture outlines, two labelled markers "A" ([hero]) and "B" ([opponent]) at their starting positions, arrows for their first movements, and a camera icon at [position]. Flat graphic on white, labels only "A", "B", "CAM".
```

### G — 3x3 storyboard
```
Create a 3x3 grid storyboard (nine equal panels, thin white borders, [ratio] overall, 2K) for a cinematic [genre] short film, block [X]. References: Image 1 is [NAME] — keep his face, hair and wardrobe exactly the same in every panel; Image 2 is the location; Image 3 is [prop].
Consistent practical lighting and grade across all panels: [light + palette]. Photorealistic film stills, anamorphic look with oval bokeh and horizontal flares, fine film grain, three-quarter angles, varied framing. No text, numbers or captions inside the panels.
Panel 1 (top-left): [time range] — [FOV/framing, angle, height] — [what we see].
Panel 2 (top-center): ...
Panel 3 (top-right): ...
Panel 4 (middle-left): ...
Panel 5 (center): ...
Panel 6 (middle-right): ...
Panel 7 (bottom-left): ...
Panel 8 (bottom-center): ...
Panel 9 (bottom-right): [final image / title space / logo].
```

---

## FINAL CHECKLIST (before delivering Kling prompts)
- [ ] Every block is ≤30 s, and the ranges add up exactly to the duration.
- [ ] The Story Engine holds: at least one reversal with a named value shift.
- [ ] Every @asset has a role and a "not inherited" line. The storyboard has "Do not render the storyboard itself."
- [ ] Location map, first frame and screen direction are written. Exact head-count, handedness and object sizes are locked.
- [ ] Each shot has one action, FOV degrees, ≤2 camera moves, three-quarter angles, and varied framing.
- [ ] Every character in frame has an ACTING TASK with verbs at the partner and the eye safety line.
- [ ] A fight, if any, is written as beats with geometry, slow-mo into contact, positive constraints, and no jargon.
- [ ] No brand names and no polish words ("flawless", "8K"). Grain, physics and practical light are present.
- [ ] Negatives are only "No subtitles" / "No music"; everything else is a POSITIVE CONSTRAINT.
- [ ] Dialogue is in English (or none), with exact lines, the speaker on screen, one at a time.
- [ ] Settings, upload map, takes plan and continuity tip are given.
- [ ] `python3 tools/kling_lint.py <block>.txt` prints PASS for every block, the quote covers takes x blocks, and the user said yes before any generation.

## SOURCES
- Kling 4.0 User Guide (official): https://kling.ai/quickstart/kling-4-model-user-guide
- Kling 4.0 vs 3.0: https://kling.ai/blog/kling-4-vs-3
- Higgsfield — How to Make a Cinematic AI Short Film (@adilinthewildtempo): https://higgsfield.ai/@adilinthewildtempo/blogs/make-a-cinematic-ai-short-film-with-higgsfield-the-workflow
- Runware — Kling 4.0 long takes & multi-shot; EachLabs & fal.ai Kling 4.0 prompting guides; Atlabs Nano Banana Pro rules
- User skills: higgsfield-prompt-engine, higgsfield-acting-skill, higgsfield-fight-scene, anamorphic-look
