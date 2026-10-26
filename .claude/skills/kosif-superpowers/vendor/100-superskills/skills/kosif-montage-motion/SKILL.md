---
name: kosif-montage-motion
description: "KOSIF Montage & Motion v6.3 — Arabic-first motion graphics and video editing from one request, on a PC or claude.ai (scripts/cloud_setup.py). Motion films (2D/3D, kinetic Arabic type), mimic (a reel rebuilt shot for shot with new Pinterest footage), a JSON timeline → film (transitions, speed ramps, Arabic titles, ducked music, -14 LUFS), auto-edited reels of talking clips, lyric/poem/dua films from sound, Voice2Motion, beat-cut montage, colour grades, karaoke captions, silence cuts, smart 9:16, per-platform export, scene detection, face privacy, Arabic motion templates, a browser editor, a scene-by-scene review page, per-shot AI-video prompts, launch videos, reference-video breakdowns into generation prompts, and a delivery gate. Use for: animation, motion graphics, montage, mimic, reel, TikTok, captions, subtitles, color grade, transcribe, beat sync, thumbnail, explainer. Arabic: محاكاة، انميشن، موشن، مونتاج، فيديو، ريلز، ترجمة، سبتايتل، تلوين، تفريغ، قص الصمت، غلاف، شرح متحرك."
---

> **Start here for any video request:** read `references/operating-manual.md` — it says which tool to use when (material from files, Pinterest and links; montage, timeline, reel, verse, motion/3D, launch video, analysis and prompts; review; quality-first delivery).

# KOSIF Montage & Motion — استوديو المونتاج والموشن

One skill for every moving-picture job: films made from code (2D, 3D, canvas), edits of real footage, sound, and the
quality gate. Everything is deterministic (each frame is a function of time), measured (beats, loudness, speed,
exposure) and rendered locally. Built from KOSIF Motion v3.4, the Ultra Motion & Montage skill and KOSIF Omni's
cinema, video, audio, lighting and vision skills; v5 joins the v4 branch (fast parallel renders, drafts, everyday
edits, lab kit), the Pro v1.3 branch (shape kit, 3D structural twin) and the auto-directed edit (`direct`) and the sound-only typographic film (`verse`); v5.2 adds Voice2Motion (`audio2motion`), the optional private Workbench planner (`site_bridge`) and the hardening from the v5.1 static audit.

## 0. Where am I? A PC, or claude.ai with no computer
If `/mnt/user-data` or `/mnt/skills` exists (claude.ai), or the skill folder is read-only, there is **no user PC**:
never send the user to localhost, `.bat` files, Edge, Windows voices or the local site. Work in the sandbox:
```bash
python <skill>/scripts/cloud_setup.py --install      # once per sandbox: writable home ~/kosif-motion, ffmpeg (imageio-ffmpeg)
                                                     # + an ffprobe stand-in in ~/kosif-motion/bin, the examples copied
python <skill>/scripts/kmotion.py <command> …        # always through kmotion: it applies that home and bin by itself
```
- Inputs the user uploads: `/mnt/user-data/uploads`. Deliver every file to `/mnt/user-data/outputs` and say where it is.
- **Renders with no browser** (verified in a sandbox with only the imageio-ffmpeg binary and the ffprobe stand-in):
  `workbench` (a task → plan → 2D film with Arabic titles, Pillow + FFmpeg), `timeline` (clips, xfade transitions,
  speed ramps, Arabic overlays, captions, ducked music, two-pass −14 LUFS), `audio2motion` (voice → motion scenes, voice
  normalised to −14 LUFS), `montage`, `grade`, `captions`, `silence`, `aspect`, `trim`, `concat`, `loop`, `export`,
  `platforms`, `thumb`, `scenes`, `privacy`, `studio-import`, `score`, `ambience`, `structural`, `inspect`, `sheet`.
- **Needs a browser** (Chromium via Playwright): `new/frames/preview/render` of HTML, 3D and lab compositions, `direct`,
  `verse`, rendering `template` projects. Try `cloud_setup.py --install --browser`; if the report still shows no browser,
  deliver the composition's `index.html` (it plays itself) and, for a montage the user wants to cut by hand, point to
  KOSIF Studio Cloud (the owner's claude.ai artifact; frame-accurate MP4 in their browser). Say plainly what was not rendered.
- `transcribe` needs faster-whisper and a model download; when that is blocked, ask for a transcript or timed cues.
- Uploading this skill to claude.ai: build the ≤ 200-file package with `scripts/build_package.py --claude-ai`.

## 0b. What can this machine do?
```bash
python scripts/env_check.py
```
- **Route A** (browser + FFmpeg): render MP4 films, edit footage, everything below.
- **Route B** (FFmpeg, no browser): edit footage (montage, grade, captions, decaption, reel); films are delivered as a
  self-playing HTML composition.
- **Route C** (no FFmpeg — e.g. a locked-down sandbox): write the composition HTML (it plays itself with a play bar,
  audio in sync), synthesise the music WAV, and give the exact commands to render on a full machine.
- The skill folder may be read-only (claude.ai): `export KOSIF_MOTION_HOME=$PWD` (or a writable folder) before creating
  projects; put deliverables where the environment lets the user download them (on claude.ai: `/mnt/user-data/outputs`).
- Never claim a render you did not run. If a step is unavailable, say which and deliver the strongest artifact possible.

All tools sit behind one entry: `python scripts/kmotion.py help` (or run with no arguments for the Arabic menu).

**Speed rules (v4).** Look before you render, render small before you render big, never render twice:
1. `kmotion frames PROJECT --times …` (seconds) → 2. `kmotion preview PROJECT` (a half-size 15 fps draft, ≈ 10× faster
than the master; the same page and the same t give the same composition) → 3. `kmotion render PROJECT --engine studio`
(parallel browsers — auto: ≥ 20 frames per page, at most 6, one per 2 cores on software WebGL; `--workers N` or
`KOSIF_WORKERS` to set). A master whose sources and parameters are unchanged is
served from its fingerprint cache (`--force` to redo). DOM/CSS compositions capture with the GPU process off (2×
faster, automatic; 3D pages keep WebGL). A page that throws fails in seconds with the error, not after the budget.
Several independent jobs → `kmotion batch jobs.json --parallel N`.

## 1. Classify the request
| The user wants | Do |
|---|---|
| An animation / motion piece / explainer / showreel from an idea | §2 Film from code |
| A talking clip turned into a directed edit (keywords, camera, symbols, payoff) | `direct` (§3) |
| A song, poem, dua or voice-over (sound only) turned into a film of its words | `verse` (§3) |
| Their own video edited ("مونتاج", "ريلز", captions, colour) | §3 Footage |
| Burned-in subtitles removed / a transcript / an SRT | `decaption` / `transcribe` (§3) |
| Music, ambience, narration | §4 Sound |
| Pauses cut out of a talking clip ("قص الصمت", jump-cut) | `silence` (§3b) |
| A vertical / square version, a cover with a title, GIF, a loop, steadier footage | `aspect` · `export` · `thumb` · `loop` · `stabilize` (§3b) |
| A "product lab" / schematic piece: a plush character, orbiting lens, callouts, HUD | `kmotion new NAME --lab` (§2, Lab kit) |
| A cute / sculpted 3D character or object (plush, glossy eyes, smooth shapes) | `new NAME --3d` + shape kit (`references/shape-kit.md`) |
| A real 2D or 3D truss analysed (SHAPE/JOINT/LOAD/BREAK/SWAP/RANK numbers) | `structural` · `twinview` (§8, `references/STRUCTURAL_TWIN.md`) |
| Prompts for Veo / Sora / Kling / Runway | `references/ai_video_models.md` + `references/seven-layer-anatomy.md` (write prompts; generate only if asked and a tool exists) |

## 2. Film from code
**Direction before effects** (`references/motion-craft.md`, `craft-numbers.md`): audience, feeling, duration, aspect →
2–3 genuinely different directions → pick one → a shot list with times (4–7 beats, one carried device, named camera
moves) → a motion score (what moves, from where, how long, which ease). Story arc for short pieces: hook (frame 0
composed and moving) → development → pressure → lift → payoff → deliberate end.

```bash
python scripts/kmotion.py new NAME --seconds 10                 # flat: HTML + GSAP + motion-kit
python scripts/kmotion.py new NAME --3d --seconds 10            # 3D: src/main.js on the three-kit (runs on window.K3 without npm)
python scripts/kmotion.py new NAME --canvas --seconds 10        # canvas: one page, window.seek(t)
python scripts/kmotion.py new NAME --lab --seconds 20 --fps 24 --size 960x540   # product lab: plush 3D + HUD + orbit walk
python scripts/kmotion.py frames projects/NAME --times 1,4,7    # the 8-second gate: look at keyframes before rendering
python scripts/kmotion.py preview projects/NAME                   # draft cut, seconds (NAME.draft.mp4)
python scripts/kmotion.py render projects/NAME --engine studio --blur 4   # master; --workers N, --force, --capture png|jpeg
python scripts/kmotion.py inspect out/NAME.mp4                  # delivery gate
python scripts/kmotion.py kit-bundle                            # after editing kit/three-kit.js: rebuild window.K3 (esbuild)
python scripts/kmotion.py export out/NAME.mp4 --out deliver --title "العنوان" --gif   # 9:16 · 1:1 · 16:9 + poster + GIF
```
- **Flat kit** (`scripts/kit/motion-kit.js`, `window.MOTION` v4): eases `E`, physical springs `SPR`/`track`, Arabic word
  masks `revealWords`/`riseWords`/`maskRise` (whole words move, letters stay joined), `typeOn`, `counter`, `drawPath`,
  `morphPath`, camera `push`/`rackFocus`, v4: `shake` (decaying seeded camera hit), `parallax` (layers by depth),
  `glitch` (≤ 0.4 s digital stutter), `stagger` (lists arriving one by one), `lowerThird` (Arabic-safe name/role card),
  `shim(root, seconds)`; footage via `<video data-start>`; audio via `<audio id data-start data-volume
  data-role="voice|music">` (voice ducks music in the mux, master −14 LUFS). After editing the kit: `kmotion sync PROJECT`.
- **Shape kit** (`scripts/kit/shape-kit.js`, `window.K3S`, v1.3): sculpt 3D shapes and characters from signed distance
  fields — sphere/ellipsoid/round-cone/box/torus with smooth union, carve, intersect and colour paint → a watertight
  mesh (coarse-to-fine surface nets); `plushMaterial` (felt sheen + fuzz), glossy `eye()`, `tube()`, `stageDisc`,
  `makeLitePost` (fast post), `trussOverlay` (structural twin in 3D), and a rigged cute `bunny()`. Read
  `references/shape-kit.md` (API + the "cute recipe") before making a character.
- **3D kit** (`scripts/kit/three-kit.js`; global `window.K3` from `three-kit.bundle.js`; `K3.POST` = the post classes;
  rebuild with `kmotion kit-bundle` after editing): renderer (tone `aces|agx|neutral`),
  sky, terrain, forest, sea, shallow water + caustics, koi, petals, pebbles, clouds, flocks, post (bloom, rays, DOF,
  grade, grain, NaN guard), GPU motion blur, `shot()`/`shotFromWords()`/`sequence()` (Veo shot vocabulary as cameras),
  `lightPreset()` (Rembrandt, clamshell, edge…), `aerialPerspective()`, `makeLookPass()` (gamut, night, split tone),
  `makeSpectrumGround()`/`makeGlitchPass()`/`MOTION.channels()` (the sound drives the picture), `makeParticleBody()`
  (real motion from `mocap`), long exposure `render --shutter 30 --stack lighten`.
- **Lab kit** (`scripts/kit/lab-kit.js`, loads after the bundle and extends `window.K3`; `kmotion new NAME --lab`): the
  2026 "3D schematic" look — one plush hero on a cream studio sweep, a lens that walks the whole circle and stops at
  parts, extreme close-ups with dashed callouts + measurement cards, an instrument-panel HUD (title strip, timeline,
  charts). Blocks: `makeFur` (shell fur), `makeEye` (sclera/iris/pupil/cornea), `makeRabbit` / `makeLion` (named joints
  `userData.joints`), `schematic` (`set(k)` wire ↔ plush, `explode(k)`, `joints(k)` dashed pivots), `orbitWalk(camera,
  stops)` (walks around what it looks at, holds at each stop), `studio` (sweep, 3-light rig, contact shadow, grid),
  `hud(root, W, H)` + `addCallout({anchor, label, title, text, measure})` projected from 3D every frame, `labPost`
  (bloom/rays/DOF off: fast on software GL), `idle` (breath, blink, ear and tail life). Script the six beats SHAPE →
  JOINT → LOAD → BREAK → SWAP → RANK (`references/STRUCTURAL_TWIN.md`): an animation illustrates; it is not physics proof.
  Example: `scripts/projects/lab_rabbit_lion` (20 s, 960×540, 24 fps: ≈ 2 s/frame on software GL, ≈ 8 min with 2 workers).
- Contract and traps: `references/hyperframes-authoring.md` (no `dir=rtl` on `<html>`, literal
  `window.__timelines["root"] = tl`, `<audio>` needs an id, fonts need @font-face, seeded randomness only).
- Any composition opened in a normal browser **plays itself** (play/pause, scrub, audio in sync, fitted to the window) —
  the preview deliverable for Route C; renderers never see the player.

## 3. Footage (real video)
**Edit the meaning, not just the words.** Transcribe first; for every sentence find its meaning, emphasis and the
1–4 key words, then choose: nothing · caption · keyword typography · camera move · symbol · transition · sound accent.
The speaker stays the hero; every graphic has a reason (`references/montage_grammar.md`, `animation_craft.md`).

```bash
python scripts/kmotion.py direct CLIP.mp4 --name NAME --credit "insta: handle"   # a DIRECTED edit, planned automatically, editable (recommended for talking clips)
python scripts/kmotion.py render projects/NAME --engine studio                  # then: kmotion inspect out/NAME.mp4 · kmotion sheet out/NAME.mp4
python scripts/kmotion.py verse SONG.mp3 --name NAME --text lyrics.txt --title "…" --mood night   # sound only → a typographic film (song, poem, dua, voice-over)
python scripts/kmotion.py reel CLIP.mp4 --out FINAL.mp4                     # automatic: words → decaption → restore 1080×1920 → voice → music only if none → karaoke → −14 LUFS → gate
python scripts/kmotion.py transcribe CLIP.mp4 --model large-v3              # words.json, .srt, captions.json (word times drive animation)
python scripts/kmotion.py decaption CLIP.mp4 --out CLEAN.mp4                # erase burned-in captions + a fixed credit line
python scripts/kmotion.py montage a.mp4 b.mp4 --music track.wav --out M.mp4 # beat-planned cuts, punches, grade, ducking
python scripts/kmotion.py grade CLIP.mp4 --preset restore                   # restore · teal_orange · golden_hour · blue_hour · sodium_night · cyberpunk · vintage_film …
python scripts/kmotion.py captions CLIP.mp4 --spec captions.json            # Arabic karaoke (one ASS event per word)
```
**`direct` — how it decides** (every decision lands in `projects/NAME/edit.json` / `edit.js`; change it and re-render):
- the subject of each shot (skin region, else the moving region) → the camera pushes on it; the stack is face →
  keyword → caption, so text never covers the mouth; motifs go on the free side at eye level;
- one keyword per sentence by **end-focus** (Arabic sentences land on their last content word) + loudness + theme
  words the speaker repeats; fillers (ممكن، اللي، ده…) and refrains never; the unit after a number belongs to the ring;
- a number → a clock ring on its repetition; a cut → the word at the cut becomes the transition plane;
- the payoff by **rhetoric**: a repeated short line builds ("كافح… كافح… كافح") and the first full sentence after its
  last repetition resolves it; otherwise the most stressed sentence in the last 40 %; then a deliberate dip to black;
- music: the clip's own bed is kept when the quiet floor shows one; else an original underscore.
**Review loop (always):** read `projects/NAME/transcript.srt` — fix ASR spelling with
`--fix "ما حدش=محدش;بتعودش ضايع=متقعدش تضيّع"` (timings kept) — look at `kmotion frames projects/NAME --times …` —
adjust `edit.json` (a keyword, a y, the payoff lines, a ring) — render — `inspect` + `sheet` — fix what a reviewer
would call P0/P1.

**`verse` — a film of words from sound alone** (`projects/NAME/verse.json` holds every decision; edit and re-render):
- timing: Whisper's word times; `--text` aligns the true words (lyrics, poem, dua — diacritics, hamza and ASR
  misspellings matched) onto them; no Whisper + `--text` → laid over the voiced spans and reported as *estimated*;
  `--words NAME.words.json` for exact times from elsewhere;
- lines: dynamic programming over the cuts — ~1.1–3.6 s and ≤ 7 words per line, broken at pauses, punctuation and
  phrase openers (و/ف-clauses, اللهم، يا، إلا, a dua's imperatives); never after a particle, never between a number
  and its unit, never inside «يا حي يا قيوم»;
- structure: a 3 s pause opens a section (palette step, light rule, next `--images` picture with a hard cut and a
  slow push); 4.5 s is an interlude (an eight-point rosette breathing on the beat); without pauses, sections by time
  (one per picture, else ~12 s); a long intro holds the title card, else the title is a quiet header;
- emphasis: a keyword only when it earns it (above-average weight, ≥ 2 s apart, each word once, never a filler);
  the payoff is the refrain's last return, else the closing line naming the theme or a number — larger, a light
  passes through it, the sky flares;
- the light is the sound: kicks swell the halo and send rings, onsets lift the motes, loudness breathes the glow;
  `--mood night|dawn|gold|sea|ink`; over pictures the type moves off any face (lower or upper third);
- music: nothing added by default (a song has its own; keep a recitation unaccompanied); `--music auto` adds an
  underscore only when the track has no bed. Review loop as for `direct` (`transcript.srt`, `--fix`, `frames`).

### 3b. Everyday edits (`scripts/tools.py`, one FFmpeg pass each, sources never touched)
```bash
python scripts/kmotion.py silence CLIP.mp4 --out cut.mp4 [--threshold -35 --min 0.45 --pad 0.08]   # jump-cut the pauses, picture+sound together
python scripts/kmotion.py aspect CLIP.mp4 --to 9:16 --mode smart --out v.mp4   # smart = around the faces (motion centroid when no face); crop; blur = blurred pad
python scripts/kmotion.py export FILM.mp4 --out deliver --aspects 9:16,1:1,16:9 --title "عنوان" --gif --webp   # every variant + poster in parallel
python scripts/kmotion.py thumb FILM.mp4 --at 2.0 --text "عنوان عربي" --sub "KOSIF" --size 1080x1920 --out cover.jpg   # shaped + ordered Arabic
python scripts/kmotion.py trim CLIP.mp4 --from 3.2 --to 9.8 --out part.mp4 · concat a.mp4 b.mp4 --out all.mp4 · loop CLIP.mp4 --seconds 30 --out loop.mp4
python scripts/kmotion.py stabilize CLIP.mp4 --out steady.mp4           # vidstab 2-pass when built in, else deshake
python scripts/kmotion.py probe FILE · fonts                            # streams/duration · which Arabic fonts exist here
```
`reel` (v4) accepts `--transcript NAME.words.json` (a reel without Whisper), runs transcription and decaption side by side, encodes the picture once (captions + credit in one pass)
and uses `--model auto` (the best whisper model already cached; batched decoding when faster-whisper ≥ 1.1 is
present, openai-whisper as a fallback).

**Directed premium edit by hand** (when a piece needs custom graphics per idea; example `scripts/projects/premium_edit/index.html`):
1. Transcribe (large-v3) and cross-check against any burned captions (OCR) — the audio is the source of truth.
2. `decaption` → restore/upscale the plate (`grade restore`, Lanczos to 1080×1920) → an all-intra plate
   (`kmotion footage`) the composition seeks frame-exactly.
3. A composition over the plate: camera (push 100→108 %, punches on stressed words, a pull-back before the payoff),
   three text levels (speech caption · phrase · keyword), micro-graphics ≤ 1.5 s for examples, the cut treated as a
   chapter, the payoff alone on screen, a deliberate end (hold → dip to black).
4. Sound: clean the voice; if the clip already has a music bed keep it and add only accents; else an original
   underscore; SFX on stressed words, always under the voice.
5. Render, then the gate and a contact sheet; review with two reviewers (P0/P1/P2), fix, re-render.

## 4. Sound
`kmotion score out.wav --spec score.json` (original music on the beat grid; tape stops; risers; booms; designed SFX
from cues) · `kmotion ambience` (rain, sea, birds, brook, chords, whoosh) · `kmotion voice out.wav --text "…"`
(Arabic narration offline — Windows voices only) · `kmotion beats` / `channels` (any track → beat grid / per-frame
channels: kick, bass, onsets, silence, tape-stop). Analysis: `scripts/omni/audio_analyze.py` (LUFS, peaks, BPM).

## 5. Gates (all must pass before delivery)
1. `kmotion inspect FILM` → ok (yuv420p H.264, no unintended black/frozen stretches, −14 ± 1.5 LUFS, true peak ≤ −1,
   no blown/crushed frames); intended holds listed with `--allow a-b`.
2. Keyframes / contact sheet looked at (`kmotion sheet FILM`) — including the phone-width view; a review written.
3. Arabic: correct spelling, joined letters, RTL on text elements, words in the right order (ASS `Encoding -1`),
   descender dots visible (`background-clip:text` needs padding), max 2 lines, inside mobile safe areas
   (9:16: keep text between ~15 % and ~80 % of the height, off the right-edge UI), never over eyes or mouth.
4. Motion: no linear eases on spatial moves, no crossfades, a visible change every ~0.7–2.5 s, nothing faster than
   ~80 px/frame (`kmotion speed`), the strongest moment near the end.
5. Sound: the voice is always on top; SFX below dialogue; 48 kHz AAC.
6. Honesty: report what was measured and what was not; credit the source of footage you did not make (re-set the
   creator's handle in your typography if a watermark was removed); never fabricate or replace a real person's face.

## 6. References
`references/craft-numbers.md` (measured motion norms) · `motion-craft.md` · `motion-director.md` ·
`hyperframes-authoring.md` (contract, kit, lessons v1→v3.4) · `book-lessons.md` (Gurney colour, Grimes lighting, night
photography, Veo shot language) · `montage_grammar.md` · `animation_craft.md` · `ai_video_models.md` ·
`seven-layer-anatomy.md` + `continuity-protocols.md` (cinema prompts) · `story-conflict.md` (+ `scripts/omni/story_lint.py`)
· `lighting-presets.md` (+ `scripts/omni/light_calc.py`) · `x-trend-2026.md` (what made the Opus 5.5 motion wave work).
Examples (sources only; renders are rebuilt): `scripts/projects/` — koi_pond, sound_ground, blue_hour, showreel,
premium_edit, water_cycle_3d, lab_rabbit_lion, bunny_twin (`kmotion sync projects/NAME` restores the kit copies).
`references/shape-kit.md` (SDF characters) · `STRUCTURAL_TWIN.md` · `KOSIF_SEE_INTEGRATION.md`. What changed: `CHANGELOG.md`.

## 7. KOSIF SEE integration — safe Pro media extension (2026-10-08)
The canonical KOSIF SEE front door stays the owner of request intake and capability truth.
When the user asks to **edit footage, create motion graphics/3D animation, generate a reel,
transcribe, create kinetic Arabic titles, repair sound, or measure delivery quality**, route
through `kosif-media-motion` and this specialized `kosif-montage-motion` implementation.
This adds an executable local *media package*, **not** a parallel general-purpose reasoning
system or automatic replacement for KOSIF Think's request-bound Full Pro runtime.

Preflight before irreversible/expensive work:
```bash
python scripts/kmotion.py proplan --task 'مونتاج ريلز عربي وترجمة وموسيقى' --mode pro --out plan.json
python scripts/env_check.py
python -m unittest discover -s tests -v
```
`proplan` is deterministic and read-only; it chooses a bounded relevant subset of
Atlas method skills. It does **not** preload ~15K skills or claim their executors ran.
When Full Pro is mandatory use `--require-full-pro`; the CLI deliberately fails closed
(exit code 3) because it cannot independently validate ChatGPT host execution receipts.
Actual external Full Pro must be invoked separately through KOSIF Think and must produce
runtime, executor, authorization and QA receipts before it can be described as complete.

### ASR fallback for an existing timecoded transcript
When Whisper isn't installed, do **not** invent word timestamps. Supply a real
`*.words.json` created by transcription in another environment or manually timed:
```bash
python scripts/kmotion.py reel source.mp4 --out reel.mp4 \
  --transcript source.words.json --no-decaption --credit '@original_creator'
```
The input is validated for monotonic timing, word text and video duration.
The credit overlay uses a UTF-8 text file instead of unsafe FFmpeg text interpolation;
it works without a Windows-only font path. By default preserve the original footage
attribution; never impersonate a speaker, strip ownership without replacing credit,
or declare a QA gate passed when its result reports failure.

Detailed integration contract: `references/KOSIF_SEE_INTEGRATION.md`.

## 8. KOSIF Structural Twin (2026-10-08, 3D since v1.3) — SHAPE / JOINT / LOAD / BREAK / SWAP / RANK
Activate when the user requests constrained joints, physical load stress checks, conceptual break paths,
part-replacement experiments, force-based failure ranking or technical 3D schematics. Do **not** hijack
ordinary 3D animation, product image prompts, or a request for a purely visual render.

This feature provides a real **limited pin-jointed truss calculation — 2D plane trusses and, since v1.3, 3D space
trusses** (`[x, y, z]` nodes, `x/y/z` supports, `fz_n` loads; NumPy solve with a singularity gate) — and an offline
interactive HUD, not a general continuum/FEA simulation or engineering certification. The six-phase cinematic storyboard can be
rendered in an ordinary animation, but the force values must come from a validated calculation,
not generated from a photo/video. User-supplied screenshots and social posts are concepts to evaluate,
not evidence that a named vendor has released the alleged engineering system.

```bash
python scripts/kmotion.py structural --sample --swap AB --area 0.0002 --fracture-scale 3.2 --out twin.json
python scripts/kmotion.py twinview twin.json --out twin.html
python scripts/kmotion.py proplan --task 'هيكل مفصلي مجسم: اختبر الوصلات والأحمال والانهيار' --seconds 18
```
Read **`references/STRUCTURAL_TWIN.md`** for schema, supported physics, source attribution,
failure/ill-conditioning behavior, and strict limitations. Never claim verified 3D FEA, validated
fracture, actual-object dimensions or Full Pro completion from this package.

## 9. v1.3 — faster renders, 3D shapes, 3D twin (2026-10-08)
- **Speed:** `render --engine studio` splits the film into contiguous chunks rendered by parallel browser pages
  (`--workers`, default auto = cores, ≥ 20 frames each); each page encodes its own H.264 segment and the segments
  are joined losslessly. Capture uses CDP `optimizeForSpeed`; PNG frames go to FFmpeg undecoded when no sub-frame blur is
  needed (`--capture jpeg` grabs ≈ 2× faster). Measured on a 4-core sandbox with software WebGL (60 frames of the 1080×1920 bunny film): v1.2 151 s →
  v1.3 112 s with 1 page, 99 s with 2 pages (1.5×). Software GL already uses every core, so auto picks cores/2
  there; with a real GPU the browser frame is cheap and the parallel pages pay off more.
- **Lite post:** `K3S.makeLitePost` (bloom + grade) instead of `makePost` when you do not need rays/DOF/grain passes.
- **Browser discovery:** Playwright caches (`PLAYWRIGHT_BROWSERS_PATH`, `/opt/pw-browsers`, `~/.cache/ms-playwright`)
  and `KOSIF_BROWSER` are found, so cloud sandboxes reach route A instead of preview-only route C.
- **Loudness:** the mux measures, then normalises linearly (two-pass loudnorm): short films land on −14 LUFS.
- **Frames render in any order:** anything a page derives from the camera (HUD callouts) must call
  `camera.updateMatrixWorld()` first — never rely on the previous frame's state.
- Example: `scripts/projects/bunny_twin` — `python projects/bunny_twin/twin/build_truss.py` (solve) then
  `kmotion render projects/bunny_twin --engine studio --blur 2`.

## 10. v5.2 Voice2Motion — uploaded voice → semantic motion graphics (`audio2motion`)

Trigger: the user uploads `wav/mp3/m4a` and asks for graphics that follow the *spoken words* — «اعمل موشن جرافيك للصوت»,
«حوّل التعليق الصوتي لفيديو». Route here (not to `verse`, which is typographic, and not to beat matching) when the
**meaning** of each sentence must choose the picture.

1. Probe the real audio (duration, pauses). Never invent a transcript or word times: a transcript comes from the user,
   from `transcribe` (Whisper, if installed) or from an existing timecoded file.
2. Cue sheet `cues.json`: `{"cues":[{"start","end","text","kind"}], "timing_quality": "..."}` sorted, non-overlapping,
   inside the duration. `kind` ∈ weather · traffic · support · refund · generic (extend `audio2motion.py` for a new motif;
   `classify()` already reads Arabic keywords). `--transcript file.txt` without times gives *estimated* cues labelled
   `estimated_from_text_length_NOT_ASR` — say so in the delivery.
3. Every scene animates and reacts to the measured speech energy (the bars at the bottom are the real RMS envelope).
   Captions are shaped Arabic (arabic_reshaper + bidi) in the first Arabic-capable font found (NotoKufiArabic, Amiri,
   Segoe UI, Tahoma; override with `KOSIF_FONT` / `KOSIF_FONT_BOLD`).
4. Render → `inspect` the MP4 (video + audio streams, −14 LUFS) and sample one frame per cue (`frames`/`sheet`).
5. Deliver the MP4 **and** `cues.json` (the editable source).

```
python scripts/kmotion.py audio2motion voice.wav --cues cues.json --out out/voice.mp4 --fps 30 --size 1080x1920
python scripts/audio2motion.py voice.wav --transcript voice.txt --plan-only          # cue sheet to review first
python -m unittest scripts/test_audio2motion.py -v
```

## 11. Optional: the private KOSIF Motion Workbench planner (`site_bridge.py`, `kmotion bridge`)

A stdlib-only client for a *remote planning* service (plan → validate → compile → 2D `project_html`). It never
renders, never runs FFmpeg and never certifies quality; it is a second opinion on shot lists. Rules, from
[references/site-bridge.md](references/site-bridge.md): exact origin only; the credential arrives as the
environment variable `KOSIF_SITE_TOKEN` through an authorized setup (never searched for, printed or pasted);
every POST needs `--allow-remote`, which is the user's explicit permission to send **that task text** off the machine.
Without a token or permission: skip it and plan locally with `proplan`. Tests: `python -m unittest discover -s tests/bridge -v`.
[references/audit-v5.1.md](references/audit-v5.1.md) (full package only) lists the legacy limitations found by the static audit; v5.2 fixed
items 1–4 (name containment, escaped titles, empty fix keys, encoder exit code); 5–10 still hold.

## 12. The 5-second film, start to finish (the default quick deliverable)

```
python scripts/kmotion.py new five --seconds 5 --fps 30 --size 1080x1920 --title "العنوان"   # 2D composition in projects/five
# edit projects/five/index.html: scene list (≤ 3 beats in 5 s), one carrier object, one camera move, ≤ 8 words
python scripts/kmotion.py frames projects/five --times 0.5,2.5,4.5                           # the keyframe gate, by eye
python scripts/kmotion.py lint projects/five && python scripts/kmotion.py render projects/five --engine studio --blur 2
python scripts/kmotion.py inspect out/five.mp4                                               # duration 5.0 s, fps, black/freeze, loudness
```
Five seconds is one idea: entrance (0–1.2 s), hold with a slow camera (1.2–3.8 s), exit or payoff (3.8–5 s).

## 13. v6.0 — KOSIF Motion Web: the local studio site, with Claude as the brain (2026-10-09)

```
python scripts/kmotion.py web                 # http://127.0.0.1:8766/  (or «KOSIF Motion Web.bat»)
python -m unittest tests.test_web -v          # the site's 9 offline tests
```
The site is the hands, Claude is the brain. Tabs: الوسائط (uploads stay in `workbench/media`) · الوصفات (every kmotion
command as a form, the command line shown first) · المشاريع (create 2D/3D/lab/canvas or a motion template; self-playing
preview; edit index.html / edit.json / verse.json with a `.bak`; frames · draft · render · lint) · التايملاين (JSON +
a computed strip; validate · save · render) · المهام (live log, outputs, player) · Workbench (the hosted site's
plan → validate → compile → canvas preview, plus a local MP4 render and a project from the manifest) · Claude · البيئة.

Contract kept from the KOSIF Motion Workbench v3 source: `/api/health|templates|plan|validate|compile`, `/api/render/*`
(job tokens, ffprobe verification), `/mcp` (`motion_plan|validate|compile|templates`) — ported to Python; the 13
`domain.cjs` cases pass. Studio tools on `/mcp`: `kosif_env|recipes|run|job|jobs|media|projects|project_read|
project_write|project_create|timeline_check|timeline_save|transitions|render_manifest`. Register once in Claude Code:
`claude mcp add --transport http kosif-web http://127.0.0.1:8766/mcp` — then Claude writes compositions into projects,
runs recipes and polls jobs. Without MCP or the CLI, the Claude tab copies the same prompt package to paste into any
Claude chat and applies the pasted reply (nothing runs before تطبيق). Details: `references/web-studio.md`.

## 14. v6.0 — timeline, scenes, privacy, templates, styles, platforms

```
python scripts/kmotion.py timeline edit.json --out film.mp4 --inspect     # kmotion timeline --example edit.json · kmotion transitions
python scripts/kmotion.py scenes CLIP.mp4 --sheet shots.png --timeline edit.json [--transition fade]
python scripts/kmotion.py privacy CLIP.mp4 --out safe.mp4 [--mode pixelate|blur|box] [--region x,y,w,h[,from,to]]
python scripts/kmotion.py template list · template new NAME --template title-card --set title="…" sub="…" accent=#E7B65A
python scripts/kmotion.py captions CLIP.mp4 --spec caps.json --style tiktok|hormozi|boxed|minimal|reels|cinema|punchy
python scripts/kmotion.py platforms FILM.mp4 --out deliver --platforms tiktok,shorts,whatsapp --title "عنوان"
```
- **timeline** (`references/timeline-schema.md`): clips with in/out, constant speed (pitch-kept audio) or exact speed
  ramps, Ken-Burns zoom, grades, fit cover/contain/blur, images and colour cards; 57 `xfade` transitions with matching
  audio cross-fades; Pillow-drawn Arabic text/lower-third/image overlays with entrances; a progress bar; karaoke captions;
  music ducked under the voice or under the footage's own speech; −14 LUFS. Intermediates render in parallel; the
  final pass is one graph. `--dry-run` shows the graph; `film.timeline.json` records every decision.
- **scenes**: shot boundaries by `scdet` (fallback `select=scene`), a thumbnail sheet, `--split`, and a timeline spec
  with one clip per shot (cuts by default, as a city-montage cut rhythm advises).
- **privacy**: faces pixelated/blurred/boxed with tracking, a margin and a hold through misses; manual regions with
  time windows; sound untouched. Detector = YuNet (drop `face_detection_yunet_2023mar.onnx` into `scripts/kit/models/`
  — not downloaded automatically), Haar when the build has it, else the skin heuristic (over-protects; the report says which).
- **templates** (`templates/motion/`): title-card · lower-third · stat-counter · quote-card · logo-reveal · countdown ·
  end-card · bullet-list — Arabic-first, Cairo embedded, deterministic, lint-clean; parameters kept in `template.json`.
- **caption styles**: `tiktok` (≤ 4 words, thick outline), `hormozi` (one word at a time), `boxed` (opaque box),
  `minimal` (no pop), with the v5 `reels`, `cinema`, `punchy`.
- **platforms**: one checked file per platform (ratio, size, bitrate ceiling, duration/size limits reported, never trimmed).
- **remote**: `render_client.py` (v5.3, consent-gated external 2D render) and the public `site_bridge.py` with their tests.
Honesty: `faces.which()` is in every privacy report; platform limits are "as commonly published — verify at use"; a
timeline's measured durations may differ from the plan by up to a frame per clip.

## 15. v6.1 — KOSIF Studio 6.0 in the kit, frame-accurate browser export, Studio Cloud (2026-10-09)

- `/studio/` on the local site is the browser montage editor from the Workbench v4 source (import media, order and
  trim clips, text/shape layers, soundtrack, project JSON). «تصدير MP4 دقيق» renders frame by frame (WebCodecs H.264 +
  AAC, mp4-muxer) at −14 LUFS without real time; «تسجيل مباشر» is the original MediaRecorder capture.
- KOSIF Studio Cloud (claude.ai artifact) is the same editor as one page, rebuilt with
  `python scripts/web/build_studio_cloud.py --out studio-cloud.html --home-url URL_OF_KOSIF_MOTION_CLOUD`.
- `kmotion studio-import PROJECT.kosif.json --out edit.json --media DIR [--render film.mp4]` turns a Studio project into
  a timeline for the full FFmpeg pipeline; the site's timeline tab has «استيراد مشروع Studio».
- `projects/midnight_cat` renders the v4 MIDNIGHT scene through the engine (`kmotion render projects/midnight_cat`).
- The local API refuses state-changing requests from other websites (Origin / Sec-Fetch-Site guard).
- Tests: `node --test tests/studio/*.test.mjs` (28) besides the Python suites.
- Packages: `python scripts/build_package.py --out ../KOSIF-Montage-Motion-v6.1.zip` (full) and
  `--claude-ai --out ../KOSIF-Montage-Motion-v6.1-claude-ai.zip` (the ≤ 200-file claude.ai upload). After installing
  from the upload, run `kmotion sync projects/NAME` before rendering an example (it restores kit scripts and fonts).

## 16. v6.2 — the review page (Motion OS, MIT), AI-video prompts, the night-boat film (2026-10-09)

The site helps Claude; it does not replace it. After a render, open the film for review and let the user mark it up:
- `kmotion review init PROJECT|SPEC.json|VIDEO [--video film.mp4]` writes `reel.json` (scenes + editable elements) and
  serves it at `http://127.0.0.1:8766/review/NAME/` — the Motion OS player by Jason Lee (MIT, commit 6dbf5da: Arabic/RTL
  UI, 9:16), patched so «أرسل إلى Claude» also saves the feedback to `NAME/review/feedback-v*.json`.
- `kmotion review feedback NAME` prints what the user sent; `kmotion review apply NAME` writes every **bound** edit into the
  source exactly (timeline spec fields; an HTML page's `<script id="kosif-props">` JSON and `:root` colours) and lists
  what is left for you (notes, motion requests, unbound edits) and the approved scenes not to touch. Then render,
  `sheet` + `inspect`, and `kmotion review bump NAME --video NEW.mp4` (the open page reloads as the next version).
- HTML compositions declare their review data in `<script type="application/json" id="kosif-reel">` (scenes → els with
  `props.*.bind` keys of `kosif-props`, optional `boxBind`/`timeBind`); see `scripts/projects/night_boat/index.html`.
  Check with `node scripts/web/static/review/check.mjs PROJECT` (the Motion OS checker).
- MCP: `kosif_reviews`, `kosif_review_init`, `kosif_review_feedback`, `kosif_review_apply`.
- `kmotion aiprompts SHOTS.json|reel.json|PROJECT` — per-shot 7-layer prompts for Veo, Sora, Kling, Runway and a
  keyframe (recovered from ultra-motion-montage / Egypt-2120); style locks carry across shots; lighting without
  direction + Kelvin is flagged. Text only: nothing is sent anywhere.
- One-click install restored from the old KOSIF-Motion package: `install.bat`, `requirements.txt`, `KOSIF Motion.bat`.
- `projects/night_boat`: 5 s, 1920×1080, three-kit sea (planar reflection, moon glitter path), a parametric felucca hull,
  a 1900K flickering lantern, a fisherman, a fish splash at 2.8 s with a synced plink, Arabic title from `kosif-props`.
- **v5.1 recovered** (from kosif-studio's uncommitted work): verse draws a symbol by meaning above a line (sun, moon,
  heart, clock, money, trophy, road, question, check, home, rain, light) and counts up a number that is said; titles
  are escaped (`motion.html_text`), script JSON is `</`-safe (`motion.json_for_script`); audio2motion labels come from
  the cue's own words (never the demo's "68°F"); `film.py` explains a missing studio.py.

## 17. v6.2 — launch videos, the poster, readability, sound effects (the /brag method, MIT)

Read `references/launch-video.md`. `kmotion brag init DIR|URL` gathers the material and writes `brag-plan.md`
(rubric, shape, tones, laws); you write the angle and storyboard, build with the engine, then
`kmotion brag deliver OUT --film film.mp4`. Use the pieces in any film:
- `kmotion poster FILM [--at T] --bake` — the strongest settled frame becomes frame 0 (thumbnails everywhere use it);
  frame count, duration and sound unchanged (checked). Do it for every delivery that opens on a fade.
- `kmotion readable FILE` — reel.json / verse.json / a timeline spec: lines too short to read, and whether the hook
  lands in the first 2 s.
- `kmotion sfx` + timeline `"audio": {"sfx": [{"src": "kit:reveal-1", "at": 0.4, "gain": -10}]}` — 20 CC0 cues
  (full package; the claude.ai upload leaves the sound files out to stay under 200 files).

## 18. v6.2 — reference-video breakdown, Omni Flash prompts, quality-first final, render farm

**The user sends someone's reel and wants the SAME film with new footage (المحاكاة / التقليد: same cuts, transitions, words, lettering, sound; Pinterest clips of the same mood) — read `references/mimic.md` and run `kmotion mimic` (study → fill texts/style → layer/fonts → fetch a pool from Pinterest → match → build; the gate in compare.json must pass).**

**When the user sends a video to copy, study or rebuild — read `references/video-breakdown.md` and follow it.**
- `kmotion analyze VIDEO --out NAME.breakdown [--transcribe]` measures the WHOLE film (beats from hard cuts, dissolves and
  element entrances; per-beat palette/background hex, motion energy, pan, entry type; LUFS, BPM, SFX sync) and
  extracts 3 stills per beat + overview/timeline sheets. LOOK at every beat, then fill `brief.json` (all fields).
- `kmotion omniprompt NAME.breakdown/brief.json [--overrides changes.json] [--markdown breakdown.md]` → one copy-paste
  Google Omni Flash block (≥ 1080, compressed to 10 s with the factor stated) + the readable shot-by-shot document.
  Overrides: brand, palette, text, duration, aspect, tone, style, add, remove (a removed main subject = rewrite the beats).
- `kmotion analyze --batch FOLDER` → `library.json/csv`: the measured style of many references at once.
- Example: `outputs/analysis-example-launch-video/` (breakdown, prompt, the same with a brand/palette/9:16 override).

**Render time without losing quality** (measured on this PC, the 5 s 3D boat at 1080p): preview/draft 28 s for every
review round; `kmotion final PROJECT [--blur N]` once at the end — PNG capture (lossless), libx264 slow / CRF 16, short
side never under 1080, poster baked, gate run (173 s with 4× motion blur). Close Chrome and plug the charger in.
`scripts/shard.py` splits a render across machines (frame ranges joined losslessly); a GitHub Actions workflow lives in
the private repo kosif-render-lab (see `references/render-farm.md`).

## 19. v6.2 — fetching media (Pinterest and more) and the Audio Lab (from the user's Cinema C V32)

- `kmotion fetch URL… [--max 30] [--only video|image] [--list]` — a Pinterest pin, board or section (and TikTok,
  Instagram, Facebook, YouTube, X… — anything yt-dlp reads) into the studio media library (`workbench/media`): videos
  with an edit-safe copy `NAME.edit.mp4` (H.264 yuv420p, the source's constant frame rate ≤ 60, AAC 48 kHz, faststart;
  the original kept), image pins as the original-size image (WebP → PNG). `fetch-credits.json` records the source,
  title and creator of every file. `--list` reads a pin/board without downloading. Never type the user's password:
  public pins need no login; private boards take a cookies.txt the user exported (`--cookies`). When the user browses
  Pinterest in the browser pane with you, collect the pin links from the page (read_page) and pass them to `fetch`.
  Pins are their creators' work: references, or published only with rights — say so when a pin goes into a film.
- `kmotion audiolab FILE --mode voice|music|both|novoice|nomusic [--strong]` — speech isolated by RNNoise (`lq` model,
  fetched once) + FFT denoise; music by centre cancellation (real stereo only — mono is refused, not faked); the video
  with music only (under a new voice-over) or voice only. Measured on Arabic speech over a stereo bed: speech-to-pause
  contrast 11.2 → 40.9 dB.

