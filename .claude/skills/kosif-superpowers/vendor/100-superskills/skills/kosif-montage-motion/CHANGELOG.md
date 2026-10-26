# KOSIF Montage & Motion — changelog

## v6.2 — 2026-10-09 — review page (Motion OS), AI-video prompts recovered, the night-boat film

Input: https://github.com/jasonlee-breadcrumb/motion-os (MIT). The site is Claude's helper, not a replacement.

### New
- **Review page** `/review/NAME/` on KOSIF Motion Web: the Motion OS player (commit 6dbf5da, Arabic/RTL, vertical) vendored
  in `scripts/web/static/review/` with its LICENSE and checker; patched to name this skill, save every send for Claude
  (`POST feedback`) and send the edits with Export. Routes `/api/reviews`, `/review/NAME/{feedback,export,…}` behind
  the cross-origin guard; a «المراجعة» view in the site; 4 MCP tools.
- **`scripts/review.py` → `kmotion review init|apply|export|feedback|bump|list`**: reel.json from an HTML composition
  (`kosif-reel` + `kosif-props` blocks, `:root` colours), a timeline spec (clips → scenes, text/lower-third overlays →
  elements bound to the spec: text, colour, size, timing, position) or any video (scenes by cut detection). `apply`
  writes bound edits exactly and returns what is left for Claude.
- **`scripts/aiprompts.py` → `kmotion aiprompts`** — recovered capability: per-shot 7-layer prompts for Veo, Sora, Kling,
  Runway and a keyframe, with locks, negatives, platform limits, warnings and a strong/weak-word score.
- **Installer restored** (dropped since KOSIF-Motion.zip): `install.bat`, `requirements.txt`, `KOSIF Motion.bat`.
- **`projects/night_boat`** and `outputs/KOSIF-v6.2-night-boat-5s.mp4` (+ its AI prompts JSON).

- **Launch videos — the /brag method** (https://github.com/latent-spaces/brag, MIT): `scripts/launch.py` →
  `kmotion brag init|deliver`, `kmotion readable`, `kmotion sfx`; `scripts/poster.py` → `kmotion poster` (best settled
  frame, baked as frame 0, frames/duration verified); timeline `audio.sfx`; 20 CC0 effects in `scripts/kit/sfx`
  (Kenney + unicae_games, with /brag's analysis); `references/launch-video.md`. Colours from CSS incl. oklch/rgb/hsl.
- **v5.1 recovered from kosif-studio's uncommitted work**: verse symbols by meaning + counters (CONCEPTS, concept_of,
  line.motif, icons in templates/verse.html), `motion.html_text` / `motion.json_for_script` (direct, verse), the empty
  fix key ignored in `direct.apply_fixes`, audio2motion labels from the cue (no invented "68°F"), a clear message when
  studio.py is missing, the 2D/3D truss wording in proplan.
- **Fixed**: verse's payoff sweep cloned the words mid-entry (a ghost word); a symbol now yields before a counter starts.
- `outputs/KOSIF-v6.2-najah-verse-5s.mp4` («النجاح رحلة / 3 خطوات كل يوم», from the v5.1 voice): trophy + counter, −14.2 LUFS.
  Both v6.2 films have their poster baked as frame 0.

- **Reference-video breakdown**: `scripts/analyze.py` → `kmotion analyze VIDEO | --batch FOLDER` (beats from hard cuts,
  dissolves by colour-histogram jumps and element entrances above a codec-noise floor; per-beat palette/background hex,
  motion energy, pan, entry type; LUFS/BPM/SFX sync; 3 stills per beat, overview and timeline sheets; brief.json to fill)
  and `scripts/omniprompt.py` → `kmotion omniprompt` (one Google Omni Flash block, ≥ 1080, compressed to 10 s; overrides
  for brand/palette/text/duration/aspect/tone/style/add/remove, a removed main subject stops the build; `--markdown`
  writes the shot-by-shot document). Method: `references/video-breakdown.md`.
- **Quality-first delivery**: `kmotion final` (PNG capture, slow/CRF 16, short side ≥ 1080, poster, gate) and the draft
  loop; `scripts/shard.py` (frame-range render farm) + `references/render-farm.md` with the measured times.

- **Fetch + Audio Lab** (the user's Cinema C V32 method): `scripts/fetch.py` → `kmotion fetch` (yt-dlp: Pinterest pins,
  boards, image pins via og:image originals, plus TikTok/Instagram/Facebook/YouTube; simple-format retry; edit-safe copy
  with the sound kept; fetch-credits.json; duplicates skipped) and `scripts/audiolab.py` → `kmotion audiolab` (voice /
  music / both / novoice / nomusic; mono refused for music).

- **Pinterest → montage**: image pins fetched at their original size (yt-dlp `ignore_no_formats_error`); `kmotion montage`
  takes folders and photos (slow push in/out), prefers `.edit.mp4` copies, shows landscape media whole over a blurred
  copy in a vertical frame (no more cut-off text), and writes `FILM.credits.txt` from fetch-credits.json. Tested live:
  Pinterest search in the browser pane (the user signed in) → 4 video pins + 3 image pins → a 16 s 9:16 reel on an
  original score (`outputs/KOSIF-v6.2-pinterest-night-sea-16s.mp4`, gate ok).
- **One command**: `references/operating-manual.md` (how every tool is chosen) + `/kosif-video` for Claude Code.

### Verified
- `python -m unittest discover -s tests`: 95 OK (+ test_launch ×7, test_analyze ×5, test_fetch_lab ×4); audio2motion 8 OK (new: test_review ×3, test_web review route).
- Night boat: `inspect` ok — 1920×1080, 30 fps, H.264 yuv420p, 5.0 s, −13.7 LUFS, true peak −1.1 dBTP, no black/frozen.
- Review loop in the built-in browser: page loads in Arabic, edit title → send → feedback on disk → `review apply`
  changed the source (then restored). The Motion OS checker passes on the generated reel.json.

### Not verified
- The review page's Export button end to end (route and job path are unit-tested; a full re-render from it was not run).

## v6.1 — 2026-10-09 — KOSIF Studio 6.0 joins the kit; frame-accurate browser export; KOSIF Studio Cloud

Input: `KOSIF-Motion-Workbench-complete-source-v4.zip` (site v4 / Studio 6.0: a browser montage editor in
`site/public/studio`, the MIDNIGHT 2.5D scene in `cinematic-cat/`, 21 Studio tests). Requested in Full Pro mode.

### New
- **KOSIF Studio 6.0 served by the local site** (`/studio/`, linked from the site's nav; `/examples/` carries the v4
  cat and MIDNIGHT pages). Its 21 original tests run from `tests/studio/` against the served copy.
- **Offline, frame-accurate MP4 export in the Studio** (`static/studio/offline.mjs`, button «تصدير MP4 دقيق»): every
  frame drawn by the Studio's own `draw()` after the media are sought to that time, H.264 via WebCodecs, sound mixed
  once with an OfflineAudioContext and encoded AAC (Opus fallback), muxed by mp4-muxer 5.2.1 (MIT, vendored in
  `static/studio/vendor/`). Needs no animation frames, no real time and no visible tab. The real-time MediaRecorder
  path stays as «تسجيل مباشر».
- **Loudness in the browser:** BS.1770-4 meter (K-weighting, 400 ms blocks, −70/−10 gates) and normalisation to
  −14 LUFS under a −1.5 dBFS sample-peak ceiling, applied to the offline export.
- **KOSIF Studio Cloud** (claude.ai artifact, built by `scripts/web/build_studio_cloud.py`): the whole editor as one
  page; saves go through the artifact's `downloads` capability. KOSIF Motion Cloud links to it.
- **`kmotion studio-import`** (`scripts/studio_import.py`, recipe and `POST /api/studio/import`, a button in the
  site's timeline tab): a Studio project JSON → a timeline spec (video/image clips with trims and fits, demo presets as
  colour cards, text overlays with position/size/opacity/animation, soundtrack gain) → the full-quality FFmpeg render.
  Shapes and soundtrack trim are reported, not silently dropped.
- **MIDNIGHT as an engine project** (`scripts/projects/midnight_cat`): the v4 scene wrapped as a composition
  (`window.render(t)`), lint-clean, its own 289-sample and player tests passing from the new layout.

### Fixed / hardened
- **Cross-origin guard:** state-changing requests to `/api/*` and `/mcp` from another website's page (`Origin` not
  loopback, or `Sec-Fetch-Site: cross-site|same-site`) are refused with 403. The site binds to 127.0.0.1, but any page
  open in the user's browser could otherwise post to it. Scripts and curl (no Origin) and the site's own pages pass.
- **Arabic file names from curl on Windows:** cp1256 bytes read as Latin-1 (and UTF-8 read as Latin-1) are repaired
  on upload; a guess is accepted only when it yields Arabic letters.

### Cloud edition: works inside claude.ai with no computer
- `kmotion setup` (`scripts/cloud_setup.py`): a writable home (`~/kosif-motion`), ffmpeg from imageio-ffmpeg when the
  sandbox has none (`--install`), an ffprobe stand-in (`scripts/ffprobe_shim.py`, built on ffmpeg; matches ffprobe on
  every field the kit reads, frame counts exact, durations to 1/100 s), the examples copied, and `~/.kosif-motion.json`
  which `kmotion.py` applies on every call (no shell state needed between commands).
- `kmotion workbench "task" --aspect 9:16 --titles "…|…" --out film.mp4`: a 2D film with Arabic titles and no browser
  (the Workbench planner + the Pillow frame + FFmpeg, verified with ffprobe).
- `timeline` renders picture and sound as two passes joined losslessly: one graph carrying both stalled on FFmpeg 7.1
  (the build imageio-ffmpeg ships) — the AAC encoder got no samples unless verbose logging slowed the scheduler.
  Sound is now measured and normalised linearly (two-pass loudnorm): a 7.9 s film went from −15.9 to within the gate.
- `audio2motion` resolves ffmpeg/ffprobe paths (it called them by bare name) and normalises the voice to −14 LUFS
  (`--keep-level` to skip); a −31.3 LUFS voice now passes the gate.
- `inspect` fails fast on a missing file instead of hanging.
- SKILL.md: description cut to 866 characters (the skill format allows 1,024; claude.ai checks it), a first section on
  working in claude.ai, LF line endings. `build_package.py --claude-ai` refuses > 200 files or a long description.
- Verified in a simulated sandbox (no ffmpeg/ffprobe on PATH, a throwaway home, only imageio-ffmpeg 0.6 / FFmpeg 7.1):
  setup; workbench 9:16 6 s (180 frames, Arabic titles shaped); timeline with circleopen/slideup, a speed ramp, Arabic
  overlays, TikTok captions and ducked music (gate ok, −13.1 LUFS); scenes (2 shots found); grade + Hormozi captions;
  Voice2Motion 29.4 s / 706 frames in 10 s (gate ok, −14.0 LUFS). tests/test_cloud.py repeats the core of this (4 tests).
- Not verified on claude.ai itself: whether its sandbox lets pip fetch imageio-ffmpeg, and whether Chromium can be installed.

### Packaging (claude.ai upload)
- `scripts/build_package.py` builds the full zip and, with `--claude-ai`, the skill upload (claude.ai accepts at most
  200 files; the full package has 217). The upload leaves out the test suites, the example videos/GIF and the kit
  copies inside example projects: 179 files, 3.3 MB.
- `kmotion sync` now also restores the kit fonts a page names (`assets/fonts/*.woff2`), so examples need no copies.
- `kmotion lint` no longer scans the kit files sync copies in (`three-kit.bundle.js`, `shape-kit.js`, `lab-kit.js`).
- Checked by extracting the upload zip into an empty folder, syncing the examples and running every suite there.

### Verified on this PC (2026-10-09)
- Python: test_web 13/13 · test_v6 13/13 · core + render client 44/44 · bridge 30/31 (1 skipped: symlink privilege) ·
  audio2motion 7/7. Node: Studio 28/28 (21 original + 7 offline/loudness) · MIDNIGHT 289 samples + player lifecycle.
- MIDNIGHT through the engine: 1280×720, 24 fps, 288 frames, 12.000 s, 53 s with 4 browsers; against the shipped
  librsvg reference SSIM 0.983, PSNR 33.4 dB (different rasterisers, same frames).
- Studio in the desktop app's browser pane (window hidden, 0 animation frames/s, so «تسجيل مباشر» could not advance):
  offline demo export 240 frames in 2.0 s; a project with a VP9/Opus clip + a WAV soundtrack → 360 frames, H.264 High
  + AAC LC 48 kHz stereo, 12.0 s, music alone at 3 s (220 Hz) and the clip's sound at 10 s (440 Hz), loudness
  −22.0 → −14.0 LUFS, `kmotion inspect` ok (−14.0 LUFS, −7.7 dBTP). The JS meter read −22.00 where FFmpeg's ebur128
  read −22.0, and −3.01 on the standard's calibration sine.
- The single-page Studio Cloud bundle exported the demo the same way when served locally.

### Not verified / limits
- The pane's embedded Chromium refused AAC and MP3 sources (it decoded H.264 video); tests used VP9/Opus and WAV.
  Chrome and Edge decode AAC/MP3; that path was not exercised here.
- KOSIF Studio Cloud is private to the owner and was not opened signed-in from this session; its bundle was checked
  locally. `downloads` saves need the viewer's confirmation.
- The Full Pro council run (KOSIF Think `kmm-v6-fullpro-20261009-dev`) completed 500/500 experts and every stage but
  ended `blocked_gate` (C500_TEXT_GATE_BLOCK) with an off-topic frozen answer; it is not used as evidence here.
- Studio projects still cap at 60 s / 24 scenes; transitions between Studio clips remain hard cuts.

## v6.0 — 2026-10-09 — KOSIF Motion Web (the local studio site) + the timeline engine

Built on v5.2 from the v5.3-python drop, the v5.1 Voice2Motion drop (already inside v5.2), the KOSIF Motion Workbench
complete-source-v3 package, the ultra-motion-montage skill, kosif-audit-pro's motion rules and the Atlas video skills
(`references/atlas-v6-sources.md`).

### New — the site (`scripts/web/`, `kmotion web`, «KOSIF Motion Web.bat», http://127.0.0.1:8766/)
- Starlette + uvicorn, 127.0.0.1 only, Arabic RTL UI without a build step: media library (uploads, probe), recipe forms
  for every kmotion command (argv built from declared fields, options → `--` → positionals, never a shell), projects
  (create 2D/3D/lab/canvas/template/manifest, iframe preview, in-place editing with `.bak`, frames/draft/render/lint as
  jobs), timeline editor with a computed strip, jobs with SSE logs and inline players, the Workbench flow
  (plan → validate → compile → canvas → local MP4 → project), a Claude tab and an environment tab.
- The Workbench v3 contract ported to Python (`web/wbcompat.py`): the planner, validator, compiler, `drawFrame`
  (`manifest-player.js`), the strict manifest model and the Pillow frame; the render-service API with job tokens and
  ffprobe verification; the 4 MCP tools — plus 14 studio MCP tools (`/mcp`).
- Claude as the brain (`web/claude_bridge.py`): MCP (Claude Code drives the site), the Claude Code CLI when present,
  an optional local API key, and copy/paste of the same prompt package; replies are plans applied only on تطبيق.
- Tests: `tests/test_web.py` (9): contract (the 13 domain cases), render jobs end to end (a 320×180, 2 s, 48-frame
  MP4 verified by ffprobe), jobs + SSE, media round trip, project containment, timeline summaries, Claude package/apply, MCP.

### New — the engine
- `timeline.py` (`kmotion timeline`, `transitions`): the declarative edit → one FFmpeg graph (xfade + acrossfade,
  exact speed ramps, zooms, grades, Pillow Arabic overlays, lower thirds, images, progress bar, captions, ducking, LUFS).
- `scenes.py` (`kmotion scenes`): scdet shot detection, sheet, split, timeline spec.
- `faces.py` + `privacy.py` (`kmotion privacy`): YuNet / Haar / skin detectors, tracked masks, regions.
- `mtemplates.py` + `templates/motion/*.html` (`kmotion template`): 8 Arabic-first motion templates.
- `montage.py`: caption styles `tiktok`, `hormozi`, `boxed`, `minimal` (STYLES are dicts now; `ass()` takes the style's max_words).
- `platforms.py` (`kmotion platforms`): per-platform deliveries with limit checks.
- `render_client.py` (`kmotion remote`) and the public `site_bridge.py` from v5.3 with their tests (the symlink test skips on Windows).
- `env_check`: face detector, xfade count, Tk, and the v6 capabilities.
- Tests: `tests/test_v6.py` (11): ramps, transitions, a full timeline film with gate, validation, text PNGs, scene
  detection on a 3-shot synthetic clip, privacy masks + fallback detector, every template generated and lint-clean,
  caption styles, platform table, the registry.

### Verified on this PC (2026-10-09, route A: FFmpeg 9, Edge, faster-whisper, 8 cores, Intel Iris Xe)
- Test suites, all offline: test_web 9/9 · test_v6 11/11 · core + render client 44/44 · bridge 30/31 (1 skipped:
  symlink privilege) · audio2motion 7/7.
- In the desktop app's browser pane at 1280×900: media cards with players; recipe `transitions` → job → live SSE log
  → done (exit 0); project `ui_card` created from `title-card` with Arabic parameters, previewed in the iframe, then
  rendered by the site's render job (`render --engine studio`, 1080×1920, 5 s, 150 frames) → `scripts/out/ui_card.mp4`,
  gate ok (no audio by design); Workbench plan → manifest → canvas → local render: 1920×1080, 30 fps, 12 s, 360 frames,
  605 KB MP4 verified by ffprobe inside the server; a demo timeline (two clips, a speed ramp, circleopen/slideup/
  fadeblack, Arabic title box, lower third with an arrow glyph from the fallback font, progress bar, tiktok captions,
  music ducked under the clips) → `out/demo_v6.mp4` 1080×1920 · 7.67 s · 231 frames · gate ok · −14.6 LUFS · −9.8 dBTP.
- Frames of three motion templates (title-card, countdown, bullet-list) captured through the engine and looked at.

### Not done / limits
- No YuNet model is shipped or downloaded; without it the skin heuristic protects more than faces.
- The hosted Workbench site, Render hosting and the private repository are untouched; this is a local site.
- `KOSIF Motion Desk` (a Tk window) was dropped in favour of the site.

## v5.2 — 2026-10-08 — Voice2Motion + Workbench bridge + audit fixes

Built from five supplied archives (v5 baseline, Pro 1.3, v4, KOSIF-Motion standalone, v5.1 Voice2Motion, v5.1 site build).

### New
- **`audio2motion` (KOSIF Voice2Motion):** an uploaded voice → motion-graphic scenes chosen by the *meaning* of each cue
  (weather / traffic / support / refund / generic), reacting to the measured speech envelope, with the cue sheet as the
  editable source. v5.2 finds a real font on Windows/Linux/macOS (NotoKufiArabic → Amiri → Segoe UI → Tahoma → DejaVu;
  `KOSIF_FONT`) and shapes Arabic captions (arabic_reshaper + bidi) — the v5.1 drop hard-coded a Linux DejaVu path.
  Registered in `kmotion` (menu + CLI); `scripts/test_audio2motion.py`; example cue sheet in `examples/voice2motion`.
- **`site_bridge.py` + `kmotion bridge`:** the optional private Workbench planner client (plan/validate/compile/project),
  exact-origin, consent-gated (`--allow-remote`), token only via `KOSIF_SITE_TOKEN`; mocked tests in `tests/bridge`.
  Documented in `references/site-bridge.md`; the planning audit in `references/audit-v5.1.md`.
- SKILL.md §10–12: Voice2Motion workflow, the bridge boundary, and the 5-second film recipe.

### Fixed (from the v5.1 static audit)
1. `motion.new`, `direct`, `verse`: project names pass `motion.safe_name()` — last path part, word chars/Arabic/-/_ only,
   never empty or `..`; sizes/seconds/fps range-checked.
2. Template titles are HTML-escaped before substitution.
3. `direct.apply_fixes` skips an empty source phrase instead of looping without progress.
4. `film.Encoder.close` raises when FFmpeg exits non-zero (a half-written MP4 is no longer reported as success).

### Not merged (on purpose)
- The v5.1 site build's short SKILL.md (it removed the local workflow); its content survives as `LEGACY_WORKFLOWS.md`.
- `KOSIF-Motion.zip` (v3.4 standalone): already inside v4/v5; its BAT launcher pattern is noted in README.


## v5.0 — 2026-10-08 — one skill: v4 + Pro 1.3 + direct + verse

Two branches had grown from v3.4/v1.1 side by side; v5 joins them and adds two automatic directors.

### Merged
- **Rendering:** v4's parallel studio renderer (frame ranges on N browsers, lossless concat, CDP `optimizeForSpeed`,
  drafts, fingerprint cache, GPU process off for DOM pages) with Pro's worker policy (≥ 20 frames per page, ≤ 6 pages,
  one page per 2 cores on software WebGL, `KOSIF_WORKERS`) and Pro's undecoded PNG pipe to FFmpeg.
- **Kits:** v4 `motion-kit` (shake, parallax, glitch, stagger, lowerThird, the self-playing preview) · v4 `lab-kit`
  (`new --lab`) · Pro `shape-kit` (`window.K3S`, SDF characters) copied into every 3D project · Pro `three-kit` with
  `K3.POST`, bundle rebuilt (`kmotion kit-bundle`) · Cairo / Space Grotesk / JetBrains Mono (OFL) in `kit/fonts`.
- **Tools:** v4 `tools.py` (silence, aspect, export, thumb, trim, concat, loop, stabilize, probe, batch, fonts) ·
  Structural Twin v0.2 (2D + 3D) · `proplan` · `twinview` · two-pass loudness in the mux · Playwright-cache and
  `KOSIF_BROWSER` discovery · esbuild's native Linux binary.
- `kmotion sync` restores every kit a page names (examples ship without kit copies).
- `frames` retries a stalled grab (seek again, back off) instead of failing a long review.

### New: `direct` — the auto-directed edit of a talking clip
Subject per shot → camera pushes and punches on it; face → keyword → caption stack (type never on the mouth); one
keyword per sentence by end-focus + stress + theme words (fillers and refrains never); a number → a clock ring on its
repetition; a cut → the word at the cut becomes the transition plane; the payoff by rhetoric (the first full sentence
after a refrain's last repetition); the clip's own music bed kept when the quiet floor shows one. Everything in
`edit.json`; `--fix` corrects the transcript and keeps the timing.

### New: `verse` — a film of words from sound alone
Song, poem, dua or voice-over → aligned true text (diacritics/hamza/ASR misspellings) or Whisper times or an honest
*estimated* timing; lines by dynamic programming over phrase breaks; sections at pauses or by time; keywords that earn
it; the refrain's last return (or the closing argument) as the payoff; light driven by the track (kicks, onsets,
loudness); optional pictures with the type kept off faces. Measured on a 24.8 s dua: 743 frames, 6 browsers, 308 s,
gate ok at −14.0 LUFS / −1.0 dBTP.

### Fixed in the merge
- `reel.has_music_bed`: pauses that are digitally silent mean *no bed* (the merged floor fallback had ignored them
  and heard a bed in a dry voice).
- Filler list (`direct.STOP`) extended with colloquial Egyptian fillers (بالنسبة، عبارة، حوالي، قال لي، حاجة …).

## v4.0 (2026-10-08) — faster, wider

Measured on a 2-core Linux sandbox, the flat demo composition, 1280×720, 6 s (180 frames):

| render | v3.4 | v4.0 |
|---|---|---|
| master, 1 browser | 96 s | 34 s (CDP `optimizeForSpeed` capture, OpenCV decode, GPU process off for DOM pages) |
| master, 2 browsers | — | 22 s (`--workers`, frame ranges rendered side by side, lossless concat) |
| draft (`preview`) | — | 11 s (half size, 15 fps, ultrafast, JPEG grab) |
| unchanged re-render | 96 s | 0.05 s (fingerprint cache; `--force` to redo) |

Frames of the 1- and 2-worker masters differ by < 0.3/255 mean (codec noise): parallel rendering is deterministic.

### Rendering
- `film.film_animate`: `workers` (0 = one per core, ≤ 4), `capture` png|jpeg, `preset`, `crf`; segments concatenated with `-c copy`.
- Screenshots through Chrome DevTools `Page.captureScreenshot` with `optimizeForSpeed` (lossless PNG at ~half the time).
- `html_render.page_flags`: `--disable-gpu` for pages that never mention WebGL/three (2× faster capture); `KOSIF_GPU=0|1` overrides.
- `motion.render`: `--draft`, `--workers`, `--force`, `--capture`, `--preset`, `--crf`; `motion.preview`.
- A page that throws before `window.__ready` fails in seconds with the error instead of waiting out the 600 s budget.
- `project_dir` accepts a path, `projects/NAME` or a bare name wherever projects live.
- `measure` streams frames (no temp PNGs).

### New tools (`scripts/tools.py`, all behind `kmotion`)
`silence` (jump-cut pauses, picture+sound in one pass) · `aspect` (smart face/motion-centred crop, centre crop, blurred pad) ·
`trim` · `concat` (sizes/rates unified, silent clips padded) · `loop` (tail dissolves into head) · `stabilize` (vidstab or deshake) ·
`export` (all aspects + poster + GIF/WebP, in parallel) · `thumb` (poster with shaped, ordered Arabic title) · `probe` · `batch` · `fonts`.

### Footage pipeline
- `reel`: transcription and decaption run concurrently; the intermediate plate is fast/near-lossless; captions and the credit line
  burn in a single encode (one generation fewer, minutes faster); cross-platform credit font.
- `transcribe`: `--model auto` (best cached model), batched decoding on faster-whisper ≥ 1.1 (3-4× on CPU), `cpu_threads` = cores,
  VAD filter, openai-whisper fallback.

### Motion kit v4 (`scripts/kit/motion-kit.js`)
`shake`, `parallax`, `glitch`, `stagger`, `lowerThird` — seeded, deterministic, Arabic-safe. Run `kmotion sync PROJECT` on old projects.

### Lab kit (`scripts/kit/lab-kit.js`, `kmotion new NAME --lab`, template `templates/lab/`)
Shell fur, glossy eyes, procedural rabbit and lion with named joints, schematic modes (wire ↔ plush, exploded, joint
rings), `orbitWalk` with holds, a cream studio with a three-light rig and contact shadow, an instrument-panel HUD with
callouts projected from 3D and t-driven charts, `labPost`, `idle`. Drafts: `window.__draftScale` shrinks the GL buffers.
Example film: `scripts/projects/lab_rabbit_lion` (أرنب وأسد, 20 s).

### Merged from the v1.2 Structural edition
`structural_twin.py` (2D pin-jointed truss: SHAPE/JOINT/LOAD/BREAK/SWAP/RANK), `twin_dashboard.py`, `proplan.py`,
`references/STRUCTURAL_TWIN.md`, `references/KOSIF_SEE_INTEGRATION.md`, `examples/`, `tests/` (18 offline tests),
`reel --transcript` (a reel from a pre-timed words.json without Whisper), the credit line via a text file.

### Drafts
`render --draft` / `preview` now keep the composition's own layout (CSS zoom) and shrink the GL buffers; frames are
the composition at half the pixels, never a crop.

### Environment
`env_check` reports CPU count, parallel workers, vidstab, the Arabic font found, openai-whisper and reshaper/bidi availability.

---
## The Pro branch (merged into v5)

### 1.3.0 — 2026-10-08 — faster, 3D shapes, 3D structural twin
- Parallel studio renderer: contiguous chunks on N browser pages → per-chunk H.264 segments → lossless concat;
  CDP optimizeForSpeed capture piped to FFmpeg without decoding; `--workers`, `--capture`, `--preset`.
- New `kit/shape-kit.js` (window.K3S): SDF sculpting (smooth union / carve / intersect / paint), coarse-to-fine
  surface-nets mesher with surface projection, plush/gloss materials, eyes, tubes, stage disc, lite post stack,
  3D truss overlay, rigged `bunny()`. `references/shape-kit.md` documents the API and the cute-character recipe.
- `three-kit` exports `POST` (EffectComposer and passes); `kmotion kit-bundle` rebuilds the bundle; esbuild's
  native Linux binary is now run directly (bundling failed on Linux before).
- Structural Twin v0.2: 3D space trusses (x/y/z), NumPy solve with eigenvalue singularity gate, 400 nodes / 1600
  members; 2D behaviour and all earlier tests unchanged.
- Fixes: browser discovery in Playwright caches (route C → A on cloud sandboxes); two-pass loudness in the mux
  (−12.1 → −14.5 LUFS on a 5 s film); `kmotion` now prints a command's error message instead of exiting silently.
- Fonts: Cairo (Arabic), Space Grotesk, JetBrains Mono (OFL) in `kit/fonts/` for offline Arabic HUDs.
- Example film `projects/bunny_twin` (5 s, 1080×1920) and tests: space truss (5), shape kit (4), fast render (2).

### 1.1.0 — 2026-10-08
- Added ProPlan preflight, deterministic 5-shot beat timeline, Arabic typography and mobile-safe-area gates.
- Added honest/locked Full Pro transport boundary and bounded nine-pack Atlas method selection.
- Added `reel --transcript` timing-validated fallback independent of Whisper installation.
- Fixed credit-overlay Windows font-only path and unsafe FFmpeg inline user text.
- Added unit regression tests, environment capability extension and integration documentation.
- Preserved the source scripts, kits, examples and original project layout.

### Structural Twin v0.1 (2026-10-08)
- Inspired by user-provided schematic-motion clip (concept; vendor attribution not validated).
- Implemented deterministic 2D linear elastic pin-jointed truss solver, reactions, axial stress and utilization ranking.
- Added hypothetical break/removal sequence, swap-and-recompute, strict JSON validation and offline HUD viewer.
- Added physics-specific six-beat shotplan routing without replacing general animation or image prompts.
- Added regression tests for equilibrium, hand calculation, singularity, NaN, parameter allowlist, swapping, browser behavior and output contract.
