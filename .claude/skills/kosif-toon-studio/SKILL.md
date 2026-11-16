---
name: kosif-toon-studio
description: Mahmoud Elkosif's cartoon studio for the series «أبو كاب وأبو نضارة» (Cap and Specs). Makes 20-second vertical reels of the two characters in two tested ways (A, drawn in Python code, free; B, painted with an image generator, about 2.5 credits), with English captions, sound effects, a watermark, a credit line and copy-ready descriptions and hashtags. Use when the owner asks for a video, an idea or a series with the characters (أبو كاب، أبو نضارة، الشخصيتين، كرتون، فيديو علمي، أفكار هوك، اينشتاين), or sends this skill in a new chat.
---

# KOSIF Toon Studio: «أبو كاب وأبو نضارة»

Everything agreed with the owner, in one place, so a new chat does not start from scratch.

## 0. The owner and how to reply

- **Who he is:** Mahmoud Elkosif, an Egyptian video editor who makes 9:16 reels and reads on his phone.
- **Language:** Egyptian Arabic, short, result first.
- **Every delivery:** the first line is the full output path. Then send the file. Then one code block with the description and hashtags (§7).
- **Options:** when you offer choices, use numbered or lettered options and mark the recommended one with ⭐. Then execute when he says «نفذ».
- **Background jobs:** while long work runs, give one line of status. Never claim to have watched or heard something you did not open.

## 1. Rules agreed with the owner (never break them)

1. **Money and publishing.** Quoted as he said it: «ممنوع تصرف فلوس أو تنشر أو تمسح حاجة من غير موافقتي الصريحة.»
   - Before any paid generation, show the exact price from the tool (`get_cost` preflight) and wait for a yes.
   - Never publish anywhere (TikTok included).
   - Never git push without an explicit yes.
2. **Uploads.** Quoted as he said it: «ممنوع ترفع توكنات أو settings.json أو BlackDragon.rar أو خطوط. لو مش معاك صلاحية رفع، سلّمني zip وقولّي.»
3. **Faces.** Never draw a real person's face (Einstein's included; his name may appear in captions only). Never copy another creator's characters, video or art. An idea taken from a reference reel is retold with our characters and our own drawing.
4. **Watermark and credit.**
   - The «© Mahmoud Elkosif» watermark stays in the bottom-right for the whole film.
   - In the last 1.5–2 s, over a dark gradient, show two lines: «مونتاج وإخراج Mahmoud Elkosif» and «تابعني على فيسبوك» (gold).
   - When remaking a reel, replace the original creator's handle with ours.
5. **Export standard.**
   - 1080×1920, 30 fps, H.264 High, CRF 17, preset slow, yuv420p, BT.709, `+faststart`.
   - Exactly as long as planned: 20.0 s means 600 frames.
   - No dark first or last frame.
   - If the owner supplied audio, stream-copy it.
6. **One heavy render at a time.** Never wait with `sleep` loops: run it in the background and get a notification.
7. **On-screen text.**
   - Captions are short, correct English: 2–8 words, at least 1.2 s on screen, never over a face or the key action.
   - Never guess an unclear word from a source reel.
8. **Disk.** The owner allowed «لو مفيش مساحة امسح أي حاجة قديمة واشتغل كامل». Delete only old intermediate files (frames, previews), never final videos.

## 2. The characters (the identity of the series)

| | Cap («أبو كاب») | Specs («أبو نضارة») |
|---|---|---|
| Look | white round bean head, **red cap**, **red t-shirt**, dark trousers, red sneakers | white round bean head, **round black glasses**, spiky dark hair, **blue t-shirt**, grey trousers |
| Personality | hasty, mocks, laughs a lot, does the "obvious" thing and fails | calm, clever, knows the science; his strange method works |
| Arc | laughs → is shocked → learns and ends up amazed or sharing | quiet smile → proof → shares the result |

- Reference image: `refs/charsheet.jpg`. In the code, `tk.fig(g, "cap"|"specs", ...)`.
- A warm ending is required: they share the result and laugh together. No humiliation.

## 3. Idea and hook formula (what the owner liked)

- **The owner wants "smart":** a REAL, surprising science fact with a visible mechanism. Not silly slapstick: he rejected «ده هبل».
- **Hook:** the first 1.5 s already shows the strange image (an upside-down umbrella, a man in a cage under lightning), zoomed in, then the camera pulls back.
- **Structure:** hook → Cap's obvious way + laughter → Specs's strange way → visible proof (cut-away, arrows, a zoom inset) → ✗ on Cap's way and ✓ on Specs's way → warm ending.
- **Correct physics:**
  - If an effect is tiny, say so, e.g. «×1,000,000,000» or "tiny".
  - Exaggeration must stay physically right (for twins aging, use a near-light-speed trip, not a car).
- **When asked for ideas:** give a numbered list (5 or 10). For each idea give:
  - a title;
  - the hook image;
  - the fact;
  - the twist.

  Then wait for a number.
- **Seasons done so far (don't repeat them):**
  - 01–25 science and survival;
  - 26–30 animals;
  - 31–40 Einstein;
  - 41 zombies;
  - 42 the upside-down umbrella.

  The titles are in `briefs/` and in the session's HASHTAGS file.

## 4. Way A: drawn in code (free, the main engine)

Engine: `engine/toonkit.py`, with `captions.py`, `toonx.py` and `toonb.py` beside it.

**Setup, once:** `bash scripts/setup.sh`.
- It downloads the Archivo Black and Cairo fonts (OFL, from Google Fonts).
- It checks numpy, opencv, Pillow with raqm (Arabic shaping) and ffmpeg.
- Sound effects are not included; see `sfx/README.md`. Without them the film renders silent.
- Or point `TOON_SFX=<folder>` at an existing sfx folder.

**How to write a film:** copy `examples/f42_umbrella.py` (the latest, with captions and studio-style directing) or `examples/f01_cage.py` (the simplest). Every film has `audio()`, `bg()`, `draw(g, t, n)`, `cam(t)` and `__main__` → `tk.run(...)`.
- **Surface:** `G` is a 1080×1920 world. Colours are BGR. Draw order is z-order.
- **Characters:** `tk.fig(g, who, x, gy, d, t, eyes=, mouth=, brows=, blush=, sweat=, walk=, sit=, crouch=, lh=, rh=, soot=, k=)`.
  - `d = +1` faces right.
  - `lh`/`rh` are hand targets.
  - Laughing: `eyes="squeeze", mouth="laugh"` + `tk.laugh_marks`.
  - Shocked: `eyes="wide", mouth="o"`.
- **Motion:**
  - `tk.key` keyframes and `cam(t)` returning `(cx, cy, zoom 1.0–1.5)`;
  - `tk.shake` on impacts;
  - `tk.out_back` / `out_bounce` for overshoot;
  - effects: `rain`, `splash`, `stream`, `fire`, `bolt`, `bulb`, `arrow`, `badge`, `sparkles`, `glow`, `stars`.
- **Directing at "studio level"** (from the stickman-video-director study):
  - a new shot or camera move every 1–3 s;
  - a punch-in zoom on every cut;
  - a whip blur plus a short white flash between shots;
  - captions in Archivo Black, white with a thick dark outline, popping in (see `f42_umbrella.py`).
- **Sound:** `tk.Mix(D)`.
  - Real effects: `m.sfx(name, t, gain, dur=, loop=)`.
  - Synth: `thump`, `clang`, `boing`, `ding`, `tada`, `rise`, `slide_down`, `steps`, `chirps`, and `tune(t0, t1)` for the light background music.
  - Every visible action has a sound at the same moment.
  - `m.save()` normalises loudness to −14 LUFS.

**Workflow:**
1. Preview: `python3 film.py prev --stills 0.5,2,4,...,19.5` writes `prev_sheet.jpg`. Open it and look.
2. Fix what reads badly: something off-frame, a caption over a face, an unclear action, an empty lower third.
3. Render: `python3 film.py done/NN_name.mp4`.

## 5. Way B: painted with an image generator (higher quality, about 2.5 credits per 20 s)

- **When:** the owner wants a painted "studio" look (the B6 Dynamic Meme style).
- **Cost:** Higgsfield `gpt_image_2_6` at default quality is 0.25 per image. Quality "high" is 1.5 per image, so don't use it. Show the price and get a yes first.
- **Steps:**
  1. Character sheet (once): see `refs/painted_prompts.md`. Keep its job_id and reuse it as `image_references` in every shot.
  2. 8–9 shots in one `generate_image_batch` call, plus one empty background for a time jump. Wait with `jobs_wait`, then download them as `shots/s0.png`…`s8.png`.
  3. Edit the `SHOTS`, `CAPS` and `audio()` tables in `examples/painted_build.py`. `SHOTS` holds the image, start, end, camera from/to as (zoom, cx, cy) and the effect: `rain`, `rain_laugh`, `heat`, `heat_shake` or `warm`. Then run it from the job folder:
     `cd <job> && JOB=$PWD python3 <skill>/examples/painted_build.py x --stills` → `stills.jpg`. Look at it, then:
     `JOB=$PWD python3 <skill>/examples/painted_build.py final.mp4`.
- **The build adds:**
  - Ken Burns camera moves with a punch-in;
  - a laugh bounce;
  - a shake;
  - drawn rain;
  - heat shimmer;
  - a whip blur and flash;
  - captions;
  - the credit and watermark;
  - sound.
- **Known weaknesses:** the images are stills (the movement is camera and effects, not acting), and a prop's colour can change between shots. Name the colour in every prompt.

### The honest comparison (umbrella film, 16 Nov 2026)

| Way | What the owner gets |
|---|---|
| B (painted) | Much prettier and stronger in the first 2 seconds of a reel. |
| A (code) | Free; the characters really move; colours and characters stay the same; but the drawing is simpler. |

Recommendation:
- Use B for the series' showcase films.
- Use A for long series with lots of motion.

## 6. Way C: 3D world (experimental)

The owner sent the `cartoon-audio-short` skill. It puts flat cards inside a three.js world with ink, rendered by Chromium on the CPU at about 3–10 s per frame.

- It is designed around a voiceover, with music and effects at 50% of the voice level.
- Without a voiceover, use music, effects and captions.
- First test: `out/20261116-s83`. Read that test's result before relying on it.

## 7. Delivery (fixed format)

1. The full path on the first line.
2. Send the file.
3. Verify before sending:
   `ffprobe -v error -count_frames -show_entries stream=width,height,r_frame_rate,nb_read_frames:format=duration -of compact final.mp4`
   It must show 1080×1920, 30/1, 600 frames for 20 s.
4. Then one code block, ready to copy, per video. **Hashtags in English.**

   ```
   <short Arabic title + emoji>
   <one or two Arabic lines explaining the idea, in Egyptian>
   <the same in English>

   #science #physics ... #stickman #animation #mindblown #fyp
   ```

   **When the video is a remake of a reel the owner sent:** use exactly the original's hashtags, minus the creator's handle, and add none of our own.
5. Report the credits spent, if any. End with one honest line on the weakest point, then the next step as options.

## 8. Lessons learned (mistakes we will not repeat)

- **Frame count.** `-shortest` in ffmpeg cut the video to 598 frames because the audio was a little shorter. Don't use it. Rely on `-frames:v N` and verify the frame count.
- **Image cost.** The 9:16 "high" quality preflight showed 1.5 credits per image. Default quality is enough.
- **Large repos.** A full clone of a big repo filled the disk. Use `--depth 1 --filter=blob:none --sparse`, and fetch single files from raw.githubusercontent.
- **Fact-check every number.** In the coffee film I corrected an E=mc² figure I had given the owner wrong. Check every number before putting it on screen.
- **Rate limits.** When the 5-hour usage limit stops a background agent, resume it after the reset instead of starting from zero.
- **Random ranges.** In random ranges (`rng.integers(low, high)`), make sure high > low.
- **Dark starts.** If the first shot is dark, swap the order so it isn't, or brighten it.

## 9. Files in this skill

- `engine/`: the code-drawing engine and helpers.
- `examples/`:
  - `f01_cage.py`: simple.
  - `f42_umbrella.py`: studio directing.
  - `painted_build.py`: way B.
- `briefs/`:
  - `BRIEF.md`: series rules for anyone making a film.
  - `BRIEF_EINSTEIN.md`: changes for the Einstein season.
- `refs/`:
  - `charsheet.jpg`;
  - `painted_prompts.md`;
  - `painted_shots.jpg` and `code_shots.jpg`: the two ways compared.
- `scripts/setup.sh`: fonts and checks.
- `fonts/` and `sfx/`: filled by setup or by you. Not shipped in the zip.
