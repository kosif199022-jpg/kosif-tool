# Capability map — خريطة القوى

One section per superpower: what it adds to a KOSIF film, a decision table (need → tool → how → license note), recipes anchored to the production steps (observe / plan / build / sync audio / render / verify / deliver), pitfalls and the playbooks it strengthens. Tools are named and linked, never copied; install each from its own repository and respect its license (legend in [repos.md](repos.md)). The KOSIF cloud machine ships Node 22, Python 3.13, ffmpeg and Playwright with Chromium; everything else is *install first* or *run elsewhere and import the result* — check with `python3 .claude/skills/kosif-superpowers/scripts/superpowers.py doctor`.

**بالعربية:** قسم لكل قوة: ما تضيفه للفيلم، جدول اختيار (الحاجة → الأداة → الطريقة → ملاحظة الترخيص)، وصفات مرتبطة بخطوات الإنتاج، مزالق، والدلائل التي تعززها. الأدوات تُسمّى وتُربط ولا تُنسخ؛ ثبّت كل أداة من مستودعها واحترم ترخيصها. جهاز KOSIF السحابي يحوي Node 22 وPython 3.13 وffmpeg وPlaywright؛ وما عداها «ثبّت أولًا» أو «شغّله في مكان آخر واستورد النتيجة».

Contents / المحتويات: [observe](#observe) · [animate](#animate) · [render](#render) · [space](#space) · [draw](#draw) · [data](#data) · [voice](#voice) · [arabic](#arabic) · [captions](#captions) · [generate](#generate) · [orchestrate](#orchestrate) · [design](#design)

<a id="observe"></a>

## observe — رصد المرجع

*reference acquisition and inspection: fetching permitted media, sampling frames, palette extraction, scene-cut detection, motion/optical-flow analysis* — 12 repositories listed under *observe* in [repos.md](repos.md).

### What it adds / ما تضيفه

The observe superpower turns a permitted reference into numbers before anything is scaffolded: cut timestamps, a measured palette, type sizes read from frames, motion magnitude and subject positions. It extends the repository's own `scripts/fetch_reference.py` pass (contact sheet, `cuts.json`, `palette.json`) with finer tools, and every result lands in the *Observed* half of STYLE.md so PLAN.md rests on evidence. The same tools return at verify to check the render against those numbers.

**بالعربية:** قوة الرصد تحوّل المرجع المسموح به إلى أرقام قبل البناء: زمن القطعات، الألوان المقاسة، أحجام النص، شدة الحركة ومواقع الشخص. تكمّل سكربت الجلب وffmpeg بأدوات أدق، وتصبّ النتائج في قسم «ما لوحظ» في STYLE.md، ثم تعود عند التحقق لمقارنة الرندر بما قسته.

### Decision table / جدول الاختيار

| need | tool | how | license note |
|---|---|---|---|
| decode frames, histograms, optical flow, frame diff at verify | [OpenCV](https://github.com/opencv/opencv) | `pip install opencv-python-headless`, then `cv2.VideoCapture` and `cv2.calcOpticalFlowFarneback` | Apache-2.0, permissive; ~60 MB wheel |
| exact cut list and shot-length statistics | [PySceneDetect](https://github.com/Breakthrough/PySceneDetect) | `pip install scenedetect[opencv]`; `scenedetect -i reference.mp4 detect-adaptive list-scenes` | BSD-3-Clause, permissive |
| contact sheets, colour counts, pixel diffs | [ImageMagick](https://github.com/ImageMagick/ImageMagick) | `apt install imagemagick`; `magick montage`, `magick compare -metric AE` | ImageMagick licence (Apache-style), permissive; v6 packages use `convert` |
| fetch a permitted clip with subtitles and metadata | [yt-dlp](https://github.com/yt-dlp/yt-dlp) | `pip install -U "yt-dlp[default]"`; `yt-dlp --dump-json URL`, then download with `--write-subs` | Unlicense; some bundled binaries GPLv3 — external CLI only |
| dominant colours as hex for STYLE.md | [Color Thief](https://github.com/lokesh/color-thief) | `npm install colorthief`; `ColorThief.getPalette('frame.png', 6)` in Node | MIT, permissive; needs sharp |
| read on-screen Arabic titles and their boxes | [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) | `pip install paddlepaddle paddleocr`; `PaddleOCR(lang="ar").predict("frame.png")` | Apache-2.0, permissive; heavy install, install first |
| MP4 box tree, timescale, track timing | [GPAC / MP4Box](https://github.com/gpac/gpac) | `apt install gpac`; `MP4Box -info -std file.mp4` | LGPL-2.1, weak copyleft — fine as external CLI |
| transparent cutouts of logos, products, portraits | [rembg](https://github.com/danielgatis/rembg) | `pip install "rembg[cpu]"`; `rembg i in.png out.png -m u2net` | MIT code; default BRIA weights need a paid licence for commercial work — use u2net |
| face, hand and pose landmarks per frame | [MediaPipe](https://github.com/google-ai-edge/mediapipe) | `pip install mediapipe`; PoseLandmarker / FaceLandmarker in VIDEO mode over OpenCV frames, export JSON | Apache-2.0, permissive; heavy wheel plus model downloads |
| depth map for 2.5D slicing | [Depth Anything V2](https://github.com/DepthAnything/Depth-Anything-V2) | clone, `pip install -r requirements.txt`, run with the Small encoder | Code and Small model Apache-2.0; Base/Large/Giant CC-BY-NC-4.0 — non-commercial |
| upscale small logos and frames before zooms | [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) | `pip install realesrgan basicsr`, or the portable ncnn-Vulkan binary | BSD-3-Clause, permissive; GPU for speed |
| tracked subject mattes through a clip | [SAM 2](https://github.com/facebookresearch/sam2) | clone, `pip install -e .`, `build_sam2_video_predictor()` in Python | Apache-2.0, permissive; CUDA GPU required — run elsewhere, import masks |

### Recipes / وصفات

1. **Cut rhythm → scene grid** (step: observe → plan; PySceneDetect, ffmpeg). Fetch the reference with `scripts/fetch_reference.py` into `.kosif-cache/`; install PySceneDetect and run the adaptive detector with scene listing on `reference.mp4`; compute average shot length and where pacing changes; write them to STYLE.md *Observed* and draft PLAN.md boundaries, which `words.json` overrides once audio exists. Artefact: scene list CSV in the cache, STYLE.md cut-rhythm row, PLAN.md draft.
   **بالعربية:** اكتشف القطعات بدقة واحسب طول اللقطة وحوّلها إلى حدود مشاهد أولية يتقدّم عليها ملف الكلمات.

2. **Observed palette table** (step: observe; ffmpeg, Color Thief or ImageMagick). Extract 8 evenly spaced frames with ffmpeg; run Color Thief with six colours per frame, or ImageMagick's six-colour histogram; merge, drop near-duplicates, keep the frame timestamp beside each hex; name survivors as tokens (`--ink`, `--paper`, `--accent`) and mark averaged tints *estimated*. Artefact: STYLE.md palette table and `palette.json`.
   **بالعربية:** عينات إطارات ثم ست ألوان لكل إطار، تُدمج وتُسمّى كرموز تصميم مع تمييز الألوان المقدَّرة.

3. **Arabic title metrics** (step: observe; PaddleOCR, ffmpeg). Extract full-resolution frames at the title moments; run PaddleOCR with the Arabic model (install first, or run elsewhere and import the JSON); turn each box into text height and line gap as a share of frame height, then canvas px; check against `playbooks/arabic-typography.md` minimums. Artefact: `titles.json` and STYLE.md type-scale rows (text *Observed*, font identity *Assumed*).
   **بالعربية:** قراءة العناوين العربية وصناديقها لاستخراج الأحجام والمسافات ومنطقة الأمان قبل التخطيط.

4. **Camera drift and motion density** (step: observe → build; OpenCV). Read 24 consecutive frames around one camera move; compute dense optical flow between neighbours; the median vector gives drift direction and speed in %/s, the mean magnitude per second a motion-density curve; record both in STYLE.md and reuse the curve when choosing easing. Artefact: `motion.json` and STYLE.md camera row.
   **بالعربية:** التدفق البصري يقيس انجراف الكاميرا وكثافة الحركة لكل ثانية بدل التخمين.

5. **Render against measurement** (step: verify; PySceneDetect, ImageMagick, MP4Box). After `python3 tools/verify_video.py` passes, run the same scene detector on `out/film.mp4` and compare cut density with the reference row; pixel-compare approved `preview.png` frames with final frames at the same timestamps; dump the box tree to confirm fps, timescale and untouched audio. Artefact: three rows in TEST_REPORT.md.
   **بالعربية:** بعد البوابة قارن كثافة القطعات والإطارات المعتمدة وجدول الصناديق بما قسته ودوّن الفروق.

### Pitfalls / مزالق

- Determinism: PySceneDetect, OpenCV, ImageMagick and MP4Box repeat exactly on CPU; Real-ESRGAN, SAM 2 and Depth Anything vary across hardware, so run them once, store the output as an input asset, never inside the render loop.
- Arabic shaping: OpenCV and ImageMagick drawing APIs do not shape Arabic, OCR is weaker on connected display fonts, and super-resolution can invent letterforms — treat transcriptions as drafts.
- Fonts before frame 0: a measured type scale is worthless if the render falls back to another font; load the family through `window.__kosifReady`, then re-measure cap height on the contact sheet against the OCR boxes.
- Licensing: rembg's default weights and Depth Anything's larger checkpoints are non-commercial; yt-dlp fetches only what the user may analyse; LGPL/GPL tools stay external CLIs, never vendored.
- Weight and GPU: PaddlePaddle, PyTorch and MediaPipe wheels run to gigabytes; the KOSIF cloud machine ships Node 22, Python 3.13, ffmpeg and Playwright with Chromium under `/opt/pw-browsers` — no Whisper, no GPU models — so recipes say "install first" or "run elsewhere and import the result".
- Never rehost: fetched clips, frames, cutouts and mattes stay in `.kosif-cache/`, never under `styles/` or `catalog/`, never inside the deliverable; cutouts of third-party frames are study material only.
- Never imply integrations that are not installed: run `python3 .claude/skills/kosif-superpowers/scripts/superpowers.py doctor` and name only tools it marks installed.

### Playbooks extended / الدلائل المعززة

- `playbooks/render-pipeline.md` — pixel diffs on the contact sheet; box-tree check of fps, timescale and audio pass-through at the gate.
- `playbooks/arabic-typography.md` — OCR boxes supply observed Arabic sizes, line gaps and safe areas.
- `playbooks/kinetic-type.md`, `playbooks/music.md` — cut lists and shot-length statistics expose per-word pacing and the beat grid.
- `playbooks/ads.md` — measured hook length and cut density; product shots become clean cutouts.
- `playbooks/photos.md`, `playbooks/3d.md` — depth maps, mattes, upscaling and palettes prepare 2.5D parallax plates.
- `playbooks/phone.md`, `playbooks/characters.md` — face, hand and pose landmarks anchor callouts, follow-cam moves and rig poses.
- `playbooks/shapes.md`, `playbooks/product-ui.md` — palettes and frame diffs check a shape system or rebuilt UI against the reference.
- `playbooks/audio-sync.md` — subtitle and chapter metadata hint at timing before `words.json`; MP4Box proves the audio was untouched.

<a id="animate"></a>

## animate — التحريك

*motion engines, timelines, easing, path/shape morphing, physics, particles* — 14 repositories listed under *animate* in [repos.md](repos.md).

### What it adds / ما تضيفه

The animate superpower sits between PLAN.md and pixels: one master timeline that `window.__kosif.seek(t)` or a Remotion frame can scrub, plus the easing, morph, physics and noise helpers that land each beat where the playbook says it should. The starters already ship a base (`KOSIF.Ease`, `rng`, `Timeline`; `easing.ts` with Remotion's `spring`); these libraries extend it for stagger choreography, SVG morphs, falling words or GPU particles. One rule everywhere: build paused, compute from `t`, draw once per frame.

**بالعربية:** قوة التحريك هي الطبقة بين PLAN.md والبكسل: خط زمني رئيسي يمرّره `seek(t)` أو إطار Remotion، مع أدوات التسهيل والتحوّل والفيزياء والضوضاء التي تجعل كل ضربة تقع حيث يحددها الدليل. المشاريع البادئة تملك الأساس، وهذه المكتبات تمدّه عند الحاجة إلى تدرّج معقد أو تحوّل مسارات أو كلمات تسقط. القاعدة واحدة: ابنِ متوقفًا، احسب من الزمن، ارسم مرة لكل إطار.

### Decision table / جدول الاختيار

| need | tool | how (entry point) | license note |
|---|---|---|---|
| master timeline with labels on `words.json`, text reveals, motion paths | [GSAP](https://github.com/greensock/GSAP) | `npm install gsap` → `gsap.timeline({paused:true})`, drive with `tl.seek(frame/fps)` | custom no-charge licence (free since 2025): read it, credit it, never rebuild as a competing tool |
| light MIT timeline for scaffolded HTML films: word staggers, counters, SVG draw-on | [Anime.js](https://github.com/juliangarnier/anime) | `npm i animejs` → `createTimeline({autoplay:false})`, then `tl.seek(ms)` | MIT |
| the exact cubic-bezier curve a playbook names, inside any loop | [bezier-easing](https://github.com/gre/bezier-easing) | `npm install bezier-easing` → `BezierEasing(0.22, 1, 0.36, 1)(p)` | MIT |
| React/Remotion springs, layout and shared-element transitions | [Motion](https://github.com/motiondivision/motion) | `npm i motion` → `import { motion, animate } from "motion/react"` | MIT |
| morph between two SVG paths with different point counts | [Flubber](https://github.com/veltman/flubber) | `npm install flubber` → `interpolate(pathA, pathB)(p)` | MIT; sparse maintenance |
| seeded organic drift, handheld shake, logo wobble, grain | [simplex-noise.js](https://github.com/jwagner/simplex-noise.js) | `npm i simplex-noise alea` → `createNoise2D(alea(seed))` | MIT |
| perceptual colour tweens, palette ramps, caption contrast | [chroma.js](https://github.com/gka/chroma.js) | `npm install chroma-js` → `chroma.scale([a, b]).mode('lch')(p)` | BSD-3-Clause |
| hand-drawn stroke reveal of outlined Arabic logos and diagram lines | [Vivus](https://github.com/maxwellito/vivus) | `npm i vivus` → `new Vivus(id, {start:'manual'})`, then `.setFrameProgress(p)` | MIT; low activity, stable |
| After Effects icon loops and rigged characters as JSON layers | [Lottie Web](https://github.com/airbnb/lottie-web) | `npm install lottie-web` → `loadAnimation({autoplay:false})`, then `goToAndStop(frame, true)` | MIT; each JSON asset carries its author's licence |
| GPU particle fields, shader filters, sprite-sheet effects | [PixiJS](https://github.com/pixijs/pixijs) | `npm i pixi.js` → stop the ticker, call `ticker.update(t)` and `app.render()` per frame | MIT; needs WebGL in headless Chromium |
| words, logos or shapes that fall, pile up and swing | [Matter.js](https://github.com/liabru/matter-js) | `npm install matter-js` → `Engine.update(engine, 1000/fps)` per frame | MIT |
| fake-3D camera maths emitted as CSS `matrix3d` | [gl-matrix](https://github.com/toji/gl-matrix) | `npm i gl-matrix` → `mat4.perspective`, `mat4.lookAt`, `quat.slerp` | MIT; pin the npm version |
| hero shots keyframed by hand and saved as JSON | [Theatre.js](https://github.com/theatre-js/theatre) | `npm i @theatre/core @theatre/studio` → `sheet.sequence.position = t` | Apache-2.0 core; studio is AGPL, dev-time only |
| code-first alternative to Remotion with built-in voice markers | [Motion Canvas](https://github.com/motion-canvas/motion-canvas) | `npm init @motion-canvas@latest` → `yield* waitUntil('marker')` | MIT; MP4 export needs its ffmpeg plugin |

### Recipes / وصفات

1. **Word-synced master timeline — build + sync audio (GSAP or Anime.js, bezier-easing).** Load `words.js`; create one paused timeline; add a label per word at `start − 0.06 s`; place each word's rise (300–450 ms, the kinetic-type curve via bezier-easing) at its label; expose `window.__kosif = { duration, fps, seek: t => tl.seek(t) }`. Artefact: `film.html` driven by `render_html.cjs` in seek mode; label times go into PLAN.md.
   **بالعربية:** خط زمني واحد متوقف، علامة لكل كلمة قبل بدايتها بـ 60 مللي ثانية، و`seek(t)` يمرّره إطارًا بإطار.

2. **Bars-to-donut morph — build (Flubber, chroma.js).** Export both chart states as single closed paths; feed them to a flubber interpolator; drive it over 800–1000 ms with the shapes playbook's `cubic-bezier(0.65, 0, 0.35, 1)`; tween the fill in Lch with chroma so it never greys out midway; hold 1.5 s. Artefacts: the chart scene in `film.html` or `Film.tsx`, plus the STYLE.md palette table with chroma ramps and contrast ratios.
   **بالعربية:** مساران مغلقان يتحوّلان خلال 800–1000 مللي ثانية ولون يُسهَّل في فضاء Lch، ثم ثبات 1.5 ثانية.

3. **Falling Arabic words — build (Matter.js, simplex-noise.js).** Outline each whole word into a polygon (never letters); build bodies with `fromVertices`; step the engine with a fixed `1000/fps` delta from a reset world, replaying frames 0…n inside `seek(t)` or baking positions once per frame; add seeded noise wobble to the camera. Artefacts: the fall scene and a `preview.png` rendered twice to prove identical frames.
   **بالعربية:** كلمات كاملة كأجسام صلبة، خطوة ثابتة لكل إطار من حالة البداية، وضوضاء مزروعة للكاميرا.

4. **Draw-on logo with Lottie accents — build + render (Vivus, Lottie Web).** Convert the Arabic logo to outlined strokes; reveal it with Vivus in manual mode at the hand-drawn playbook's pen speed; add Lottie icon layers with autoplay off; inside `seek(t)` call `setFrameProgress` and `goToAndStop` from `t`; cut the 2–4 s half-resolution motion check. Artefacts: `film.html` and `out/check.mp4` for approval.
   **بالعربية:** الشعار بخطوط محدّدة يُرسم يدويًا، وطبقات Lottie تُثبَّت على الإطار المحسوب من الزمن.

### Pitfalls / مزالق

- **Determinism.** Never let an engine autoplay: Motion's wall-clock springs, GSAP's default clock, the PixiJS ticker and Lottie playback all drift between runs. Seek, step or scrub from `t`, pass `--seed` to `render_html.cjs`, and draw randomness from `KOSIF.rng` or alea.
- **Physics is history.** A Matter.js body depends on every earlier step: replay from frame 0 inside `seek(t)` or bake positions once; never step on `requestAnimationFrame`.
- **Arabic shaping.** SplitText, character staggers and PixiJS text work on characters or LTR runs; split Arabic into whole words, keep shaping in HTML/CSS, and outline words before Vivus, Flubber or Matter.js touch them.
- **Licensing.** GSAP is free under a custom licence: read it and credit it in TEST_REPORT.md's stack line. Theatre.js studio is AGPL: dev machine only, ship `@theatre/core`. Lottie JSON and reference media stay with their owners, never rehosted here.
- **Weight.** PixiJS needs WebGL in headless Chromium, slow without a GPU: test a 2 s clip first. Motion Canvas is a second toolchain, not a drop-in; the rest are small pure-JS installs.
- **Fonts before frame 0.** Resolve `window.__kosifReady` (`document.fonts.ready`) before building any timeline that measures text, or word widths and text-derived paths shift mid-render.
- **Never imply integrations that are not installed.** None of these packages exist on the KOSIF cloud machine until `npm install` runs in the film directory. Node 22, Python 3.13, ffmpeg and Playwright with Chromium under `/opt/pw-browsers` are present; Whisper and GPU models are not, so plans say "install first" or "run elsewhere and import the result".
- **Playbook numbers win.** Springs on bars, letter-spacing on Arabic and overshoot on data stay wrong even when a library offers them.

### Playbooks extended / الدلائل المعززة

- `playbooks/kinetic-type.md` — word staggers and emphasis pops on GSAP/Anime.js labels tied to `words.json`.
- `playbooks/arabic-typography.md` — whole-word reveals, outlined glyphs for Vivus and Matter.js, no letter splitting.
- `playbooks/shapes.md` — Flubber morphs, bezier-easing curves, squash-and-stretch springs through Motion.
- `playbooks/charts.md` — one eased scalar for bar and counter, chroma Lch ramps, bars-to-donut morphs.
- `playbooks/particles.md` — seeded PixiJS fields and simplex-noise flow.
- `playbooks/hand-drawn.md`, `playbooks/diagrams.md` — Vivus stroke reveals at the playbook's pen speed.
- `playbooks/characters.md`, `playbooks/product-ui.md` — Lottie layers and Motion layout transitions.
- `playbooks/3d.md`, `playbooks/photos.md` — gl-matrix cameras and Theatre.js keyframed paths.
- `playbooks/audio-sync.md` — timeline labels and Motion Canvas markers from word timings.
- `playbooks/render-pipeline.md` — every engine paused and driven by `seek(t)` so `render_html.cjs` and Remotion stay frame-exact.

<a id="render"></a>

## render — الرندر

*deterministic frame rendering, encoding, programmatic video, previews and delivery gates* — 8 repositories listed under *render* in [repos.md](repos.md).

### What it adds / ما تضيفه

Render turns a KOSIF film from code into a file that passes the delivery gate. It offers two deterministic frame sources (Chromium via Playwright behind `tools/render_html.cjs`, or React via Remotion), one encoder (native FFmpeg) that makes yuv420p H.264 from frames and muxes the voice untouched, and helpers (Manim, sharp, MoviePy, ffmpeg-python, ffmpeg.wasm) for scripted scenes, post-processing, stitching and browser fallbacks. Every recipe ends at `python3 tools/verify_video.py` and a filled TEST_REPORT.md.

**بالعربية:** قوة الرندر تحوّل كود الفيلم إلى ملف يمرّ من بوابة التسليم: مصدران حتميان للإطارات (Playwright أو Remotion)، ومُرمّز واحد هو ffmpeg الذي يدمج الصوت دون تعديل، وأدوات مساعدة للتجميع والمعاينة. كل وصفة تنتهي بـ `verify_video.py` وTEST_REPORT.md.

### Decision table / جدول الاختيار

| need | tool | how | license note |
|---|---|---|---|
| Encode PNG frames to MP4, mux untouched audio, probe for TEST_REPORT | [FFmpeg](https://github.com/FFmpeg/FFmpeg) | `ffmpeg -framerate 30 -i frames/frame_%06d.png -i voice.mp3 -c:v libx264 -pix_fmt yuv420p out.mp4`; `ffprobe -show_streams out.mp4` | LGPL/GPL (libx264 builds are GPL): call as a subprocess, never vendor or link |
| Deterministic frames from an HTML/Canvas/SVG film | [Playwright](https://github.com/microsoft/playwright) | already wrapped by `node tools/render_html.cjs` (seek or virtual mode); on the cloud machine Chromium lives under `/opt/pw-browsers`, never run `playwright install` | Apache-2.0 |
| React composition with editable props and Studio preview | [Remotion](https://github.com/remotion-dev/remotion) | `starters/remotion`; `npx remotion studio`; `npx remotion render KosifFilm out/film.mp4 --props=props.json` | Custom licence: free for individuals and small teams, paid above a company-size threshold; read before use |
| Normalise stills, stamp safe-area or logo overlays, thumbnails | [sharp](https://github.com/lovell/sharp) | `npm install sharp`, then chain resize / composite / toFile per image | Apache-2.0; install first (native libvips binary) |
| Stitch scene files, crossfades, bumpers, attach the voice | [MoviePy](https://github.com/Zulko/moviepy) | `pip install moviepy`; concatenate clips, `with_audio`, `write_videofile(fps=30)` | MIT; needs the ffmpeg binary; v2 API differs from v1 |
| Readable filter graphs (loudnorm, scale, overlay, concat) from Python | [ffmpeg-python](https://github.com/kkroening/ffmpeg-python) | `pip install ffmpeg-python`; `import ffmpeg` then input → filter → output → run; `.compile()` prints the command | Apache-2.0 wrapper; the ffmpeg it drives stays LGPL/GPL |
| Equation reveals, graph morphs, chart transitions as Python scenes | [Manim Community](https://github.com/ManimCommunity/manim) | `pip install manim`; `manim -qh --fps 30 scene.py SceneName` (`--format png` for frame sequences) | MIT; heavy install (Cairo, pango, ffmpeg, optional LaTeX) |
| Probe, trim or preview inside a browser-only sandbox | [ffmpeg.wasm](https://github.com/ffmpegwasm/ffmpeg.wasm) | `npm i @ffmpeg/ffmpeg @ffmpeg/util`; load, writeFile, exec, readFile | MIT; experimental and slow; final deliveries use native ffmpeg |

### Recipes / وصفات

1. **Render → verify: standard HTML delivery.** Playwright (via `tools/render_html.cjs`), FFmpeg, `tools/verify_video.py`.
   - Preview with `node tools/render_html.cjs --in film.html --out out/preview.png --preview`; check sizes, clipping, Arabic shaping.
   - Render a 2–4 s half-resolution motion check of the hardest moment; show both to the user.
   - Render the final with `--fps 30 --audio voice.mp3`, plus `--seed` for randomness and `--offline` when fonts are local.
   - Gate with `python3 tools/verify_video.py out/film.mp4 --aspect 9:16 --fps 30 --duration <s> --audio voice.mp3`; copy values into TEST_REPORT.md.
   Artefacts: out/preview.png, out/check.mp4, out/film.mp4, TEST_REPORT.md.
   **بالعربية:** لوحة إطارات، مقطع فحص، رندر نهائي مع الصوت، ثم بوابة `verify_video.py` والتقرير.

2. **Render: frames needing post-processing.** Playwright, sharp, FFmpeg.
   - Render with `--frames-dir out/frames --keep-frames` to keep the PNG sequence.
   - Composite the approved logo or safe-area guide onto every frame with sharp at fixed coordinates, no resizing.
   - Encode with the manual ffmpeg line in render-pipeline.md (libx264, yuv420p, CRF 18, faststart, `-shortest`).
   - Gate as in recipe 1.
   Artefacts: stamped out/frames/*.png, out/film.mp4.
   **بالعربية:** احتفظ بالإطارات، اطبع الشعار بـ sharp، رمّز بـ ffmpeg وتحقق.

3. **Build → render: scripted maths or chart scene.** Manim Community, FFmpeg.
   - Install first (`pip install manim` plus Cairo and pango); if that fails here, run elsewhere and import the frames.
   - Write the scene class with timings from PLAN.md scene boundaries, rounded to frames.
   - Render at the film's fps as a PNG sequence or silent MP4.
   - Mux the untouched voice with ffmpeg; gate with verify_video.py.
   Artefacts: scene.py, frame sequence, out/film.mp4.
   **بالعربية:** ثبّت Manim أولًا، ارندر المشهد بلا صوت بتوقيتات PLAN.md، ثم ادمج الصوت وتحقق.

4. **Deliver: stitch scenes, export per platform.** MoviePy or ffmpeg-python, FFmpeg.
   - Render each scene (recipes 1–3) at the master aspect.
   - Concatenate in Python (MoviePy for crossfades and bumpers, ffmpeg-python for loudnorm, scale and overlay graphs); attach the voice once at frame 0.
   - Re-compose per platform (never crop blindly) per the spec table in render-pipeline.md.
   - Run verify_video.py on every export; one TEST_REPORT.md block each.
   Artefacts: out/film_9x16.mp4, out/film_16x9.mp4, TEST_REPORT.md.
   **بالعربية:** اجمع المشاهد في Python، أعد التكوين لكل منصة، وأجرِ البوابة على كل ملف.

5. **Verify: browser-only fallback.** ffmpeg.wasm.
   - Without native ffmpeg (a reviewer's browser), load ffmpeg.wasm, write the MP4 into its virtual file system, probe or trim it.
   - Export a low-res GIF for the review thread.
   - Mark TEST_REPORT.md "preliminary: wasm probe"; repeat the gate with native ffmpeg before delivery.
   Artefacts: preview.gif, preliminary probe notes.
   **بالعربية:** فحص أولي في المتصفح، يُعاد بـ ffmpeg الأصلي قبل التسليم.

### Pitfalls / مزالق

- Determinism: frame = f(t); seed randomness (`--seed`), fix viewport and device scale, never screen-record, render one frame twice before trusting a pipeline.
- Fonts before frame 0: resolve `window.__kosifReady` after local fonts load, or Arabic shaping and widths shift mid-render; prefer `--offline`.
- Arabic shaping: Playwright and Remotion shape correctly with installed fonts and `dir="rtl"`; sharp, MoviePy text and Manim's default text path do not guarantee it, so render Arabic in the browser and composite it as images.
- Licensing: FFmpeg is LGPL/GPL (libx264 GPL), subprocess only; Remotion's licence depends on company size; credit and link every tool, copy nothing.
- Installation weight: Playwright browsers are hundreds of MB (use `/opt/pw-browsers`, never reinstall); Manim needs Cairo, pango, optional LaTeX; sharp's native libvips binary can fail on odd CI images; CPU-only, no GPU.
- Never imply integrations that are not installed: the cloud machine has Node 22, Python 3.13, ffmpeg and Playwright with Chromium; Manim, MoviePy, sharp, ffmpeg-python and ffmpeg.wasm are "install first"; Whisper and GPU models: "run elsewhere and import the result".
- Encoding hygiene: stream-copy or one AAC encode from the source plus `-shortest`, never resample or stretch; yuv420p and even dimensions; audio length within 50 ms.
- Never rehost third-party media: license and download assets before render time, keep them out of the repository, cite the source in TEST_REPORT.md.

### Playbooks extended / الدلائل المعززة

- playbooks/render-pipeline.md — adds post-processing, stitching and browser-fallback paths to its renderer table.
- playbooks/audio-sync.md — its ffprobe duration and untouched-mux rules anchor every recipe.
- playbooks/kinetic-type.md — deterministic word-by-word frames from Playwright or Remotion, shaping checked on the contact sheet.
- playbooks/charts.md, playbooks/diagrams.md, playbooks/shapes.md — Manim as a scripted route for equation reveals and graph or geometry morphs through the same ffmpeg gate.
- playbooks/product-ui.md — `--scale 2` focus-zoom renders and sharp-stamped safe-area guides.
- playbooks/photos.md, playbooks/ads.md — sharp normalises stills to frame size, overlays logos, makes thumbnails.
- playbooks/music.md — MoviePy and ffmpeg-python for bumpers, crossfades and loudnorm at delivery.

<a id="space"></a>

## space — الفضاء ثلاثي الأبعاد

*3D/WebGL scenes, cameras, 3D text, model loading, fake-3D parallax from depth maps* — 7 repositories listed under *space* in [repos.md](repos.md).

### What it adds / ما تضيفه

Space gives a KOSIF film a camera that can travel: product orbits, fly-throughs between narration terms, extruded logos and depth pulled out of a flat photo. It extends the Three.js snippet in `playbooks/3d.md` with shaped Arabic text inside the scene, cinematic post-processing, a Remotion route and an external Blender route. Every scene keeps the seek contract: transforms come from `t`, one draw per `seek(t)`.

**بالعربية:** قوة الفضاء تمنح الفيلم كاميرا تتحرك فعلًا: دوران حول منتج، تحليق، شعارات مجسمة، وعمق من صورة مسطحة. تكمّل دليل 3D بنص عربي مشكّل داخل المشهد ومعالجة سينمائية ومسارَي Remotion وBlender، مع التزام كل مشهد بعقد `seek(t)`.

### Decision table / جدول الاختيار

| need | tool | how | license note |
|---|---|---|---|
| Real 3D scene, camera path, glTF model, seekable under Playwright | [three.js](https://github.com/mrdoob/three.js) | `npm i three`; build the scene, call `renderer.render(scene, camera)` inside `window.__kosif.seek(t)` with `preserveDrawingBuffer: true` | MIT, permissive |
| Arabic title or caption as a crisp object inside the scene, RTL and joined | [Troika (troika-three-text)](https://github.com/protectwise/troika) | `npm i three troika-three-text`; `new Text()` with a local TTF/OTF, `direction = 'rtl'`, then `sync()` and wait for its callback | MIT, permissive; no WOFF2 |
| Bloom on titles, shallow focus, grain, SMAA per frame | [postprocessing](https://github.com/pmndrs/postprocessing) | `npm i three postprocessing`; replace the render call in `seek(t)` with `composer.render()` | Zlib, permissive; three peer version coupling |
| 3D scene inside the Remotion starter, props from the frame | [React Three Fiber](https://github.com/pmndrs/react-three-fiber) | `npm i three @react-three/fiber @remotion/three`; `<ThreeCanvas>` with props from `useCurrentFrame()` | MIT, permissive; v8 ↔ React 18, v9 ↔ React 19 |
| Studio lighting, contact shadows, environment, helpers in R3F | [drei](https://github.com/pmndrs/drei) | `npm i @react-three/drei`; `Environment` with a local HDR file, `ContactShadows` | MIT, permissive; heavy tree, download environment maps first |
| Keyframed animation groups, inspector, alternative engine | [Babylon.js](https://github.com/BabylonJS/Babylon.js) | `npm i @babylonjs/core @babylonjs/loaders`; step `animationGroup.goToFrame(n)` then `scene.render()` per frame | Apache-2.0, permissive; several-MB bundle |
| Extruded logos, modelling, GLB export, offline PNG sequences | [Blender](https://github.com/blender/blender) | install from blender.org (not on the cloud machine); run headless with a `bpy` script, export GLB or PNG frames | GPL-3.0, copyleft: external tool only, never vendor |

### Recipes / وصفات

1. **Build → render: seekable Three.js hero shot** (three.js, postprocessing, `tools/render_html.cjs`).
   - Scaffold with `starters/html-canvas`; keep its `window.__kosif` and `__kosifReady`.
   - Light and frame per `playbooks/3d.md`; compute every transform from `t` inside `seek(t)`, no `requestAnimationFrame`.
   - Wrap the renderer in an `EffectComposer` (one bloom pass, SMAA); call `composer.render()` once per seek.
   - Preview with `--preview`, run a short motion check, then the final render with `--audio`.
   Artefacts: film.html, out/preview.png, out/film.mp4.
   **بالعربية:** مشهد Three.js يحسب كل شيء من الزمن داخل `seek(t)`، مع توهج، ثم معاينة ورندر.

2. **Build: Arabic title inside the scene** (troika-three-text, `playbooks/arabic-typography.md`).
   - Copy the licensed TTF/OTF into the project; troika reads no WOFF2 and must not fetch fallbacks while rendering.
   - One `Text` per whole word or line with `direction = 'rtl'`; never one mesh per letter.
   - Call `sync()` and resolve `window.__kosifReady` only after its callback, so frame 0 has shaped glyphs.
   - Compare the contact sheet with the phrase as an HTML overlay; joins and diacritics must match.
   Artefacts: shaped title object, out/preview.png, TEST_REPORT.md row 9.
   **بالعربية:** نص عربي بخط محلي واتجاه RTL، كلمات كاملة لا حروف، وانتظار `sync()` قبل الإطار الأول.

3. **Build → render: Remotion 3D composition** (React Three Fiber, drei, Remotion).
   - Install first: `cd starters/remotion && npm install`, then add three, the fiber, `@remotion/three` and drei (fiber major = React major).
   - Mount `<ThreeCanvas>` in `Film.tsx`; derive camera, mesh and title props from `useCurrentFrame()` and `words.json`; no `useFrame`.
   - Light with drei's `Environment` from a downloaded, licensed HDR plus `ContactShadows`.
   - Check a still with `npx remotion still`, render, gate with `python3 tools/verify_video.py`.
   Artefacts: src/Scene3D.tsx, out/still.png, out/film.mp4.
   **بالعربية:** مشهد 3D داخل Remotion، خصائصه من `useCurrentFrame()` والكلمات، إضاءة من HDR محلي مرخّص، ثم البوابة.

4. **Observe → build: depth-map parallax from one photo** (three.js, Depth Anything V2 via observe).
   - Record the photo's licence in ASSETS.md; produce the depth map elsewhere and import it (no GPU here).
   - Map the photo onto a subdivided plane with the depth map as displacement; raise until edges tear, then back off.
   - Move the camera within `playbooks/photos.md` limits, eased, over 2–4 s; if it still tears, use the three-layer rig of `playbooks/3d.md`.
   Artefacts: depth.png, ASSETS.md row, out/preview.png.
   **بالعربية:** خريطة عمق تُنتَج خارجيًا وتُستورد كإزاحة على مستوى مقسّم، وحركة كاميرا صغيرة ضمن حدود دليل الصور.

### Pitfalls / مزالق

- Determinism: no `requestAnimationFrame`, `Clock` or `useFrame` time; disable the R3F loop (`frameloop="demand"` or `ThreeCanvas`), step Babylon with a fixed delta, seed noise, keep `preserveDrawingBuffer: true`, render one frame twice before trusting the pipeline.
- Arabic shaping: `TextGeometry`, drei's `Text3D`, Babylon and Blender text objects neither shape nor reorder Arabic; use troika, an HTML/SVG overlay or an RTL canvas texture, never letters as separate meshes; Blender extrusions start from browser-shaped SVG outlines.
- Fonts before frame 0: troika shapes asynchronously in a worker, so resolve `window.__kosifReady` after `sync()`; local fonts only, render with `--offline`.
- GPU and installation weight: the cloud machine has no GPU, so headless Chromium draws WebGL in software; expect seconds per frame at 1080×1920, keep one bloom pass, lower `--scale` for checks; Babylon weighs several MB, Blender hundreds.
- Never imply integrations that are not installed: present are Node 22, Python 3.13, ffmpeg and Playwright with Chromium under `/opt/pw-browsers`; three, troika, R3F, drei, Remotion are "install first"; Blender, Depth Anything, GPU models: "run elsewhere and import the result".
- Licensing: all permissive except Blender (GPL, external tool only); models, HDRs and textures carry their own licences: record and credit them in ASSETS.md and TEST_REPORT.md.
- Never rehost third-party media: no reference frames as textures, no CDN models or HDRIs at render time, nothing from `.kosif-cache/` in the deliverable.

### Playbooks extended / الدلائل المعززة

- playbooks/3d.md — adds shaped Arabic text, post-processing, Remotion and Blender routes to its snippet.
- playbooks/photos.md — its parallax numbers drive a depth-displaced plane under the same camera limits.
- playbooks/arabic-typography.md — troika carries its no-split, local-font, RTL rules into WebGL.
- playbooks/kinetic-type.md — SDF or extruded titles timed to word onsets under a moving camera.
- playbooks/render-pipeline.md — fills its "Three.js" renderer row with seek-mode and `@remotion/three` recipes.

<a id="draw"></a>

## draw — الرسم

*2D creative coding, SVG/Canvas drawing, hand-drawn and sketchy looks, draw-on strokes* — 8 repositories listed under *draw* in [repos.md](repos.md).

### What it adds / ما تضيفه

The draw superpower serves films that must look drawn, not typeset: wobbly whiteboard boxes, strokes revealing a diagram as the narrator speaks, traced logos, sketch textures. It adds two layers: geometry generators ([Rough.js](https://github.com/rough-stuff/rough), [Excalidraw](https://github.com/excalidraw/excalidraw), [D3.js](https://github.com/d3/d3) shape helpers, [opentype.js](https://github.com/opentypejs/opentype.js) outlines) emitting path data once, and renderers ([Paper.js](https://github.com/paperjs/paper.js), [Fabric.js](https://github.com/fabricjs/fabric.js), [p5.js](https://github.com/processing/p5.js), [node-canvas](https://github.com/Automattic/node-canvas)) painting it for a given `t`. Every route ends in `window.__kosif.seek(t)` or numbered PNGs, so `render_html.cjs`, ffmpeg and `verify_video.py` stay the gate.

**بالعربية:** قوة الرسم للأفلام التي يجب أن تبدو مرسومة لا مطبوعة: صناديق سبورة مرتجفة، خطوط تكشف المخطط مع الراوي، شعار يُرسم، وخامات توليدية. تولّد المسارات مرة واحدة ببذرة ثابتة ثم ترسمها دالةً في الزمن عبر `seek(t)` أو تسلسل PNG، فتبقى أدوات KOSIF هي البوابة.

### Decision table / جدول الاختيار

| need | tool | how | license note |
|---|---|---|---|
| hand-sketched rectangles, circles, arrows and hatch fills for whiteboard and doodle styles | [Rough.js](https://github.com/rough-stuff/rough) | `npm install roughjs`; call `rough.svg(svgEl)` with a fixed `seed`, store the generated paths | MIT, permissive |
| scales, arcs, line generators and interpolators evaluated from `frame/fps` | [D3.js](https://github.com/d3/d3) | `npm install d3`; import `scaleLinear`, `line`, `arc`, `interpolate` — skip d3-transition | ISC, permissive |
| import an SVG, measure path lengths, place a pen tip at `getPointAt`, headless Node frames | [Paper.js](https://github.com/paperjs/paper.js) | `npm install paper-jsdom-canvas`; `paper.setup` then `project.importSVG` | MIT; Node build needs Cairo — install first |
| headline glyph outlines as path data for stroke draw-on or morphs | [opentype.js](https://github.com/opentypejs/opentype.js) | `npm i opentype.js`; `font.getPath(text, x, y, size).toPathData()` on shaped text | MIT; no Arabic shaping inside |
| seeded generative strokes, particle fields and sketch textures in the browser | [p5.js](https://github.com/processing/p5.js) | `npm install p5` or a local script copy; `noLoop()`, seed, `redraw()` per frame | LGPL-2.1, weak copyleft — link unmodified, credit |
| PNG frames of strokes or chart layers without Chromium, Arabic fonts registered | [node-canvas](https://github.com/Automattic/node-canvas) | `npm install canvas`; `registerFont` then `canvas.toBuffer('image/png')` per frame | MIT; native Cairo/Pango deps — install first |
| a whole sketchy diagram authored as JSON and exported to SVG | [Excalidraw](https://github.com/excalidraw/excalidraw) | `npm i @excalidraw/excalidraw`; `exportToSvg({elements, appState, files})` | MIT; heavy React bundle and bundled fonts |
| lower-thirds and title cards as scene objects re-exported as editable SVG at deliver | [Fabric.js](https://github.com/fabricjs/fabric.js) | `npm install fabric`; `StaticCanvas`, set props per frame, `canvas.toSVG()` | MIT; headless needs node-canvas |

### Recipes / وصفات

1. **Sketchy diagram with causal draw-on** (step: build; Rough.js, D3.js). After scaffolding, generate every node and edge once through Rough.js with one `seed` and save the paths to `sketch-paths.json`; in `film.html` reveal each path via `pathLength`/`strokeDashoffset` at the 900–1200 px/s of `playbooks/diagrams.md`, nodes before edges; position with D3 scales so RTL flips one range. Artefact: `sketch-paths.json`, the diagram scene, PLAN.md edge timings.
   **بالعربية:** مسارات مرتجفة ببذرة ثابتة تُرسم بترتيب سببي وبسرعة قلم الدليل.

2. **Logo traced to spoken words** (step: build + sync audio; Paper.js, `words.json`). Import the client's SVG with Paper.js, read each path's length; give each stroke the start and end of its word in `words.json`, so the outline completes as the word is spoken (`playbooks/hand-drawn.md` §7); inside `seek(t)` derive the covered length and `getPointAt` for the pen tip. Artefact: PLAN.md stroke table (path, word, start, end), the logo scene.
   **بالعربية:** كل خط يُسنَد إلى كلمة فيكتمل عند نطقها، ورأس القلم يُحسب من الطول المقطوع.

3. **Arabic headline as outlines** (step: build; opentype.js, a shaper). Shape the headline first — install a HarfBuzz WebAssembly build, or shape elsewhere and import the SVG; extract outlines with opentype.js from shaped glyphs, never raw code points; reveal the whole word with a right-to-left mask per `playbooks/arabic-typography.md`; compare width and diacritics with the browser-rendered word on the contact sheet. Artefact: `headline.svg`, a STYLE.md type-scale row.
   **بالعربية:** تشكيل أولًا ثم استخراج المخططات، وكشف الكلمة كاملة من اليمين.

4. **Headless frame sequence** (step: render + verify; node-canvas, ffmpeg). Install node-canvas first if the doctor marks it absent; `registerFont` every Arabic family before the first frame; draw each frame purely from `t` with a seeded generator like `KOSIF.rng`; write `frames/frame_%06d.png`; encode with the manual ffmpeg recipe in `playbooks/render-pipeline.md`, voice untouched; gate with `python3 tools/verify_video.py`. Artefact: `frames/`, `out/film.mp4`, TEST_REPORT.md duration, fps, audio rows.
   **بالعربية:** إطارات PNG حتمية بلا Chromium، خطوط عربية مسجّلة قبل الإطار الأول، ثم ffmpeg والبوابة.

5. **Deterministic p5 texture layer** (step: build + verify; p5.js). Load an unmodified local p5 copy; call `noLoop()`, seed random and noise in `setup`; inside `seek(t)` set the frame counter from `t × fps` and `redraw()`; run `node tools/render_html.cjs --preview` twice and pixel-compare. Artefact: two identical `preview.png` files, the determinism line in TEST_REPORT.md.
   **بالعربية:** حلقة p5 متوقفة، بذور ثابتة، إعادة رسم من الزمن، ومعاينتان متطابقتان.

### Pitfalls / مزالق

- Determinism: Rough.js and Excalidraw re-roll their wobble unless seeded; p5 follows the wall clock unless stopped and stepped; D3 transitions, Fabric's `animate()` and Paper's `onFrame` are time-based — drive everything from `t` or bake paths first.
- Arabic shaping: none of these libraries shapes Arabic; opentype.js needs a shaper upstream, node-canvas relies on Pango (check joining and digit order on frame 0), Fabric and p5 text lean on the browser. Prefer browser-shaped whole words or pre-outlined SVG, never per-letter strokes.
- Licensing: p5.js is LGPL-2.1 — load an unmodified copy, never fork it into `tools/`, credit it. Excalidraw's bundled fonts carry their own terms; check before embedding them in delivered SVG. The rest are MIT or ISC.
- Installation weight: node-canvas and `paper-jsdom-canvas` compile against Cairo; Excalidraw pulls React and megabytes of assets. None is installed by default — run `superpowers.py doctor` before promising a headless path; fall back to Playwright seek mode if a native build fails.
- Fonts before frame 0: `registerFont` before the first `toBuffer`, `window.__kosifReady` before the first `seek`; fallback fonts shift Arabic widths.
- Never rehost third-party media: imported logos, reference sketches and borrowed Excalidraw scenes stay in `.kosif-cache/`, never under `styles/` or `catalog/`, never in the deliverable unlicensed.
- Never imply integrations that are not installed: the KOSIF cloud machine has Node 22, Python 3.13, ffmpeg and Playwright with Chromium under `/opt/pw-browsers`; Whisper and GPU models are absent, so recipes say "install first" or "run elsewhere and import the result".

### Playbooks extended / الدلائل المعززة

- `playbooks/hand-drawn.md` — Rough.js wobble, Paper.js pen-tip pinning, word-timed strokes.
- `playbooks/diagrams.md` — seeded sketchy nodes and edges with causal draw-on.
- `playbooks/shapes.md` — D3 interpolators and Paper.js booleans for morphs.
- `playbooks/charts.md` — D3 scales and arcs per frame; node-canvas renders chart layers headlessly.
- `playbooks/kinetic-type.md` — opentype.js outlines make headlines strokable and morphable.
- `playbooks/arabic-typography.md` — shaper-first outlines and Pango checks keep joined forms intact.
- `playbooks/particles.md` — seeded p5 fields drawn from `t` for sketch textures.
- `playbooks/render-pipeline.md` — a Chromium-free PNG route into the same ffmpeg encode and gate.

<a id="data"></a>

## data — البيانات

*charts, maps, diagrams and data-driven motion* — 8 repositories listed under *data* in [repos.md](repos.md).

### What it adds / ما تضيفه

The data superpower turns numbers, networks and places into KOSIF scenes without hand-placing shapes: text becomes a laid-out diagram, a JSON option becomes a chart with real axes, a tile style becomes a camera path over terrain. The libraries handle layout and projection; KOSIF owns timing, so every reveal is computed from `t` through `window.__kosif.seek(t)` or `useCurrentFrame()`, and the charts playbook's one-scalar rule still governs whatever the library draws. The insight sentence in `PLAN.md` comes first, the tool second.

**بالعربية:** قوة البيانات تحوّل الأرقام والشبكات والأماكن إلى مشاهد KOSIF دون رسم يدوي: النص يصبح مخططًا، وJSON رسمًا بمحاور حقيقية، ونمط الخريطة مسار كاميرا. المكتبات تتولى التخطيط وKOSIF يملك التوقيت: كل ظهور يُحسب من الزمن عبر `seek(t)` أو إطار Remotion، وقاعدة القيمة الواحدة للعمود والعدّاد تبقى سارية. جملة الخلاصة في `PLAN.md` أولًا.

### Decision table / جدول الاختيار

| need | tool | how (entry point) | license note |
|---|---|---|---|
| animated bars, lines, pies, bar races, RTL dashboards from one option object | [Apache ECharts](https://github.com/apache/echarts) | `npm i echarts` → `echarts.init(el, null, {renderer:'svg'})` then `setOption` per frame | Apache-2.0 |
| process, architecture, sequence or timeline diagram written as text | [Mermaid](https://github.com/mermaid-js/mermaid) | `npm i -g @mermaid-js/mermaid-cli` → `mmdc -i flow.mmd -o flow.svg` | MIT; CLI installs Chromium (heavy) |
| deterministic chart frames exported headlessly from a JSON grammar | [Vega](https://github.com/vega/vega) | `npm i -g vega vega-cli canvas` → `vg2svg spec.json out.svg` | BSD-3-Clause; PNG needs node-canvas |
| org charts, knowledge graphs, relationship maps with many layout algorithms | [Cytoscape.js](https://github.com/cytoscape/cytoscape.js) | `npm i cytoscape` → `cytoscape({container, elements, layout:{name:'cose', animate:false}})` | MIT |
| node-and-edge diagram as real React components inside Remotion | [React Flow](https://github.com/xyflow/xyflow) | `npm i @xyflow/react` → `<ReactFlow nodes={..} edges={..} />` with interaction disabled | MIT |
| map fly-throughs, route reveals, 3D terrain with Arabic place names | [MapLibre GL JS](https://github.com/maplibre/maplibre-gl-js) | `npm i maplibre-gl` → `map.jumpTo(cameraAt(t))` per frame, RTL plugin loaded | BSD-3-Clause; tiles carry their own terms |
| 3D surfaces, choropleths, scientific or statistical plots | [plotly.js](https://github.com/plotly/plotly.js) | `npm i plotly.js-dist-min` → `Plotly.react(div, dataAt(t), layout)` per frame | MIT; 3–4 MB bundle |
| arcs, hex bins, trips or point clouds over a basemap at GPU scale | [deck.gl](https://github.com/visgl/deck.gl) | `npm install deck.gl maplibre-gl` → `new Deck({layers:[...]})`, `setProps` per frame | MIT; needs WebGL2 |

### Recipes / وصفات

1. **Text diagram with word-synced draw-on — plan + build + sync audio (Mermaid).** Write the flow as a `.mmd` file beside `PLAN.md`, one node per spoken concept; export SVG with mermaid-cli and inline it in `film.html`; give each node group and edge path `pathLength="1"` and reveal them in causal order with `KOSIF.prog` from the `words.json` start of the naming word; mirror the layout for Arabic films. Artefacts: `flow.svg`, node-to-word table in `PLAN.md`, diagram scene.
   **بالعربية:** مخطط نصي يُصدَّر SVG ثم تُرسم عقده وروابطه بترتيب السبب على توقيت الكلمات.

2. **Frame-stepped ECharts race or dashboard — build + render (Apache ECharts).** Init with the SVG renderer and `animation:false`; compute the dataset for time `t` yourself (linear values, eased ranks, per the charts playbook) and call `setOption` inside `seek(t)`; set `dir="rtl"` on the container with right-anchored axis labels; preview with `node tools/render_html.cjs --preview` and inspect a rank swap. Artefacts: chart scene, `out/preview.png`, `STYLE.md` axis-direction line.
   **بالعربية:** أوقف حركة ECharts الداخلية واحسب البيانات لكل إطار بنفسك، ثم مرّر `setOption` من `seek(t)`.

3. **Spec-per-state chart frames — build + verify (Vega).** Write one Vega spec per chart state; export SVG headlessly in Node; interpolate marks between states in the timeline (or morph the exported paths with the animate superpower's Flubber); render one frame twice and diff the PNGs. Artefacts: `states/*.svg`, identical-frame proof in `TEST_REPORT.md`.
   **بالعربية:** مواصفة Vega لكل حالة، تصدير SVG حتمي، ثم تداخل بين الحالات والتحقق بإطارين متطابقين.

4. **Map fly-through with Arabic labels — build + render (MapLibre GL JS).** Download and license a style and tiles for offline use; load the RTL text plugin before `window.__kosifReady` resolves; define the camera as `f(t)` (centre, zoom, bearing, pitch) and call `jumpTo` per frame; wait for the map's idle event before each capture; cut a 2–4 s half-resolution motion check. Artefacts: route scene, `out/check.mp4` for approval.
   **بالعربية:** خريطة بمسار كاميرا دالة في الزمن، وإضافة RTL محمّلة قبل الإطار الأول، وانتظار استقرار البلاطات قبل كل لقطة.

### Pitfalls / مزالق

- **Determinism.** Every library here animates on wall-clock time by default: disable built-in animation and transitions (ECharts, Cytoscape, plotly, deck.gl, MapLibre `easeTo`) and set state from `t`. Cytoscape and dagre force layouts are randomized: run them once, save `positions.json`, animate from the file. Tiles load asynchronously: wait for idle before each frame.
- **Arabic shaping.** Canvas text in ECharts, Cytoscape and plotly needs an explicit Arabic font; MapLibre shapes Arabic only with the RTL plugin; Mermaid and React Flow labels need `dir="rtl"`. Prefer SVG renderers so the browser does the shaping.
- **Fonts before frame 0.** Resolve `window.__kosifReady` only after fonts and the RTL plugin load; a fallback font shifts label widths and axis layout mid-render.
- **Licensing.** All eight libraries are permissive; map styles, tiles, basemap fonts and datasets are not automatically. Print the data source in the frame, list the stack in `TEST_REPORT.md`; never rehost third-party media, tiles or reference videos here.
- **Installation weight and GPU.** mermaid-cli pulls its own Chromium, plotly weighs several megabytes, deck.gl and MapLibre need WebGL2 and crawl without a GPU: test a 2 s clip first. Vega PNG export needs native node-canvas; export SVG instead.
- **Never imply integrations that are not installed.** The KOSIF cloud machine has Node 22, Python 3.13, ffmpeg and Playwright with Chromium under `/opt/pw-browsers`; none of these packages exist until `npm install` runs in the film directory, and Whisper and GPU models are absent, so plans say "install first" or "run elsewhere and import the result".

### Playbooks extended / الدلائل المعززة

- `playbooks/charts.md` — ECharts, Vega and plotly supply axes, scales and chart families while the playbook's one-scalar timing drives them.
- `playbooks/diagrams.md` — Mermaid, Cytoscape.js and React Flow lay out nodes and edges for causal draw-on and camera chapters.
- `playbooks/arabic-typography.md` — RTL plugin for maps, `dir="rtl"` nodes and explicit Arabic fonts on canvas labels.
- `playbooks/audio-sync.md` — node pops, counters and race periods placed on `words.json` starts.
- `playbooks/3d.md` — MapLibre terrain and plotly 3D surfaces as spatial scenes with camera as `f(t)`.
- `playbooks/particles.md` — deck.gl point clouds and trips as data-bearing particle fields.
- `playbooks/code.md`, `playbooks/product-ui.md` — seeded data, saved layouts and React Flow panels inside product screens.
- `playbooks/render-pipeline.md` — SVG renderers, idle waits and `seek(t)` stepping so captures stay frame-exact.

<a id="voice"></a>

## voice — الصوت

*speech-to-text with word timestamps, forced alignment, TTS, music/beat analysis, loudness* — 10 repositories listed under *voice* in [repos.md](repos.md).

### What it adds / ما تضيفه

The voice superpower makes the soundtrack the measurable master clock that `playbooks/audio-sync.md` demands. It turns narration into `words.json` by transcription or, better, by snapping the known script onto the audio; it produces draft Arabic narration before the final voice-over arrives; and it reads the music bed for beats, onsets and a loudness envelope. Every output is JSON or WAV that `tools/words_convert.py`, the starters and `tools/render_html.cjs --audio` already accept.

**بالعربية:** قوة الصوت تجعل المسار الصوتي ساعةً قابلة للقياس: تحوّل تعليق العميل إلى `words.json` بالتفريغ أو بمحاذاة النص المعروف، وتولّد تعليقًا عربيًا مؤقتًا قبل وصول الصوت النهائي، وتستخرج من الموسيقى الضربات والجهارة لتقع القطعات عليها. كل ما تنتجه ملفات JSON أو WAV تفهمها أدوات KOSIF الحالية دون تغيير خطوات الرندر والتحقق.

### Decision table / جدول الاختيار

| need | tool | how | license note |
|---|---|---|---|
| word timings from the user's voice track, CPU only | [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | `pip install faster-whisper`; `WhisperModel(...).transcribe(path, word_timestamps=True)` and read `segment.words` | MIT, permissive; weights download on first run — install first |
| exact word timings when the Arabic script already exists | [CTC Forced Aligner](https://github.com/MahmoudAshraf97/ctc-forced-aligner) | `pip install git+https://github.com/MahmoudAshraf97/ctc-forced-aligner.git`; CLI with audio, text, language `ara` and romanize | BSD-2-Clause code; default MMS weights CC-BY-NC — swap in an Arabic wav2vec2 model for commercial films |
| exact audio length, trim leading silence, clean WAV | [pydub](https://github.com/jiaaro/pydub) | `pip install pydub`; `AudioSegment.from_file(p).duration_seconds` | MIT, permissive; needs ffmpeg (present on the KOSIF machine) |
| beats, onsets, RMS envelope from the music bed | [librosa](https://github.com/librosa/librosa) | `pip install librosa`; `librosa.beat.beat_track(y=y, sr=sr)` | ISC, permissive; CPU, deterministic, ~100 MB of NumPy/SciPy/numba |
| transcription plus wav2vec2 re-alignment and speaker labels | [WhisperX](https://github.com/m-bain/whisperX) | `pip install whisperx`; CLI on `narration.wav` with language `ar` and JSON output | BSD-2-Clause; diarization needs a Hugging Face token and gated pyannote weights — GPU recommended |
| speech/silence map for cuts, holds and trims | [Silero VAD](https://github.com/snakers4/silero-vad) | `pip install silero-vad[audio]`; `get_speech_timestamps(read_audio(p), model, return_seconds=True)` | MIT in LICENSE; a README badge says CC BY-NC — read the LICENSE file before commercial use |
| draft Arabic narration with word boundaries, no GPU | [edge-tts](https://github.com/rany2/edge-tts) | `pip install edge-tts`; CLI with an `ar-*` voice writing media and subtitles | LGPL-3.0, weak copyleft — external CLI only; unofficial online endpoint, check Microsoft terms before final use |
| word timings without any Python stack | [whisper.cpp](https://github.com/ggml-org/whisper.cpp) | build with CMake; `whisper-cli` with Arabic language, max-length 1 and JSON output on 16-bit WAV | MIT, permissive; ggml models are GBs; word timestamps experimental |
| vocal stem for clean STT, drum stem for beat cuts | [Demucs](https://github.com/facebookresearch/demucs) | `pip install -U demucs`; `demucs --two-stems=vocals track.mp3` | MIT, permissive; archived Jan 2025 (fork at adefossez/demucs); PyTorch, GPU recommended |
| cloned or expressive Arabic narration locally | [Chatterbox TTS](https://github.com/resemble-ai/chatterbox) | `pip install chatterbox-tts`; `ChatterboxMultilingualTTS.from_pretrained(...).generate(text, language_id="ar", ...)` | MIT; heavy PyTorch, GPU; output watermarked and non-deterministic — run elsewhere, import the WAV |

### Recipes / وصفات

1. **Narration → words.json** (step: sync audio; pydub, Silero VAD, faster-whisper or whisper.cpp). Measure the file with pydub and set the film duration to it; map speech with Silero VAD, marking pauses over 600 ms as scene-change candidates; transcribe with word timestamps (install faster-whisper first, or run whisper.cpp elsewhere and import its JSON); convert with `python3 tools/words_convert.py voice.json words.json` and hand-correct names and numbers, keeping the timings. Artefact: `words.json` (or `words.js`), `speech.json`, PLAN.md scene bounds.
   **بالعربية:** قِس المدة، ارسم مناطق الكلام والصمت، فرّغ بطوابع الكلمات، ثم حوّل وصحّح النص دون لمس التوقيت.

2. **Script-first alignment** (step: sync audio; CTC Forced Aligner or WhisperX). When the user supplies the exact Arabic script, align instead of transcribing: one phrase per line, aligner with language `ara` and romanization, spans converted to `words.json`, three words per scene spot-checked on the waveform. Artefact: `words.json` carrying the user's exact text, including Qur'anic or branded wording.
   **بالعربية:** عند توفر النص الدقيق تُحاذيه على الصوت بدل تفريغه، فتحصل على توقيت كل كلمة بنص المستخدم نفسه.

3. **Scratch voice before the real one** (step: plan → sync audio; edge-tts, later Chatterbox). Generate a draft with an Arabic edge-tts voice writing media plus subtitles; convert the word boundaries (100-ns ticks → seconds) or the SRT with `tools/words_convert.py`; build and preview against it; when the final voice-over lands, swap the audio, re-run recipe 1 or 2 and re-time only scenes whose bounds moved. Artefact: `scratch.mp3`, `words.json` marked *draft* in PLAN.md.
   **بالعربية:** صوت مؤقت بتوقيت كلمات يسمح ببناء الحركة مبكرًا، ثم يُستبدل بالصوت النهائي وتُعاد المحاذاة.

4. **Beat grid and envelope** (step: build; librosa, optionally Demucs). Separate the drum stem when the mix is dense; run beat tracking and onset detection, rounding each time to the nearest frame; compute RMS every 1/fps s, smooth over 100–200 ms, clamp; export both as JSON the starters read by frame index. Artefact: `beats.json`, `envelope.json`, BPM row in STYLE.md.
   **بالعربية:** استخرج الضربات والبدايات وغلاف الجهارة من الموسيقى وصدّرها كمفاتيح زمنية حتمية تقرأها المشاهد.

5. **Ducked mix and loudness gate** (step: render → verify; pydub, ffmpeg). Keep the voice untouched; duck music 8–12 dB under speech with ffmpeg sidechain compression; normalize to −14 LUFS / −1 dBTP per `playbooks/audio-sync.md` section 7; render with `--audio`, run `python3 tools/verify_video.py ... --audio voice.mp3 --lufs -14` and copy the measured values into TEST_REPORT.md. Artefact: `mix.wav`, passing gate, TEST_REPORT.md loudness rows.
   **بالعربية:** اخفض الموسيقى تحت الصوت، طبّع الجهارة، ارندر مع الصوت الأصلي ثم اجتز البوابة ودوّن القياسات.

### Pitfalls / مزالق

- Determinism: Whisper variants, WhisperX and Chatterbox can differ across runs or hardware; librosa, pydub and the aligners repeat on CPU. Run speech tools once and commit the JSON as an input, never inside the render loop.
- Arabic text: transcribers split clitics, glue punctuation and drop diacritics; merge entries into whole displayable words and keep the user's script for sacred or branded text.
- Licensing: default CTC aligner weights and possibly Silero are non-commercial — verify before client films; edge-tts and Chatterbox voices need a terms check; LGPL tools stay external CLIs, never vendored.
- Weight and GPU: PyTorch, pyannote, Demucs and large Whisper models run to gigabytes and want CUDA; the KOSIF cloud machine has Node 22, Python 3.13, ffmpeg and Playwright with Chromium under `/opt/pw-browsers` — no Whisper, no GPU — so every recipe says "install first" or "run elsewhere and import the result".
- Never imply integrations that are not installed: run `python3 .claude/skills/kosif-superpowers/scripts/superpowers.py doctor` and name only what it marks installed; otherwise ask the user for `words.json` or an SRT.
- Fonts before frame 0: word-accurate timing is wasted if the first caption uses a fallback font; gate on `window.__kosifReady`.
- Never rehost: narration, TTS drafts, stems and songs stay in `.kosif-cache/` or the user's project, never under `styles/` or `catalog/`; third-party stems are analysis material only.

### Playbooks extended / الدلائل المعززة

- `playbooks/audio-sync.md` — transcription, alignment and VAD tools behind pipeline steps 2–3, plus a measured ducking and loudness mix.
- `playbooks/kinetic-type.md` — per-word `start` values drive anticipation and karaoke highlights.
- `playbooks/arabic-typography.md` — aligned words keep the user's exact Arabic text and diacritics.
- `playbooks/music.md` — measured BPM, beat list and RMS envelope replace guessed grids.
- `playbooks/charts.md` — spoken-number timings let counters settle on the word within ±100 ms.
- `playbooks/particles.md` — onset and envelope JSON drive audio-reactive emission.
- `playbooks/ads.md` — scratch narration and beat grids time hook, beats and logo hit before final assets exist.
- `playbooks/render-pipeline.md` — exact audio length sizes the timeline; gate loudness values fill TEST_REPORT.md.

<a id="arabic"></a>

## arabic — النص العربي

*Arabic/RTL shaping, bidi, fonts, diacritics and Arabic NLP for captions and kinetic type* — 7 repositories listed under *arabic* in [repos.md](repos.md).

### What it adds / ما تضيفه

The arabic superpower makes Arabic text in a KOSIF film shape, order and load identically on every machine. It puts licensed fonts on disk so `window.__kosifReady` resolves against local files, trims them to the glyphs a script needs, and supplies a reference shaper for when the contact sheet shows broken joins or drifting harakat. For captions it adds normalization and tokenization so transcript tokens match the user's script, plus shaping and bidi for Pillow, Matplotlib and subtitle writers, which lack both.

**بالعربية:** قوة النص العربي تثبّت التشكيل والاتجاه والخطوط على كل جهاز: خطوط مرخّصة محلية بدل الشبكة، تقليصها إلى ما يحتاجه السيناريو، ومُشكِّل مرجعي يُستشار عند انقطاع الحروف أو انحراف التشكيل. وللترجمات تضيف توحيد الكتابة وتقطيع الكلمات لمطابقة الصوت، مع التشكيل والاتجاه للأدوات التي لا تجيدهما.

### Decision table / جدول الاختيار

| need | tool | how | license note |
|---|---|---|---|
| licensed Arabic faces on disk for every render | [Google Fonts](https://github.com/google/fonts) | sparse clone of `ofl/cairo`, `ofl/tajawal`, `ofl/almarai`…; then `@font-face { src: url('assets/fonts/Cairo.ttf') }` | OFL-1.1 per family (some Apache-2.0 / UFL-1.0), permissive; keep each family's licence file |
| small WOFF2 subsets holding only the script's glyphs | [fontTools](https://github.com/fonttools/fonttools) | `pip install "fonttools[woff]"`; `pyftsubset` with the script as text file, all layout features kept, WOFF2 flavour | MIT, permissive; the font's own licence still governs the subset |
| explain broken joins or misplaced harakat seen on the contact sheet | [HarfBuzz](https://github.com/harfbuzz/harfbuzz) | `apt install harfbuzz-tools`; `hb-shape assets/fonts/Cairo.ttf "النص"` | MIT (Old MIT), permissive; external CLI |
| per-glyph kinetic type on canvas or WebGL without breaking joins | [harfbuzzjs](https://github.com/harfbuzz/harfbuzzjs) | `npm install harfbuzzjs`; shape the whole word, animate the returned glyph paths | MIT, permissive; wasm loads asynchronously, no bidi |
| connected letters in Pillow or Matplotlib QA images | [python-arabic-reshaper](https://github.com/mpcabd/python-arabic-reshaper) | `pip install arabic-reshaper`; `reshape(text)` with `delete_harakat` set to False | MIT, permissive |
| correct visual order in those images and in generated SRT/ASS | [python-bidi](https://github.com/MeirKriheli/python-bidi) | `pip install python-bidi`; `get_display(reshaped, base_dir="R")` | LGPL-3.0, weak copyleft; fine as an unmodified dependency, never vendored |
| normalize and tokenize Arabic so captions match `words.json` | [CAMeL Tools](https://github.com/CAMeL-Lab/camel_tools) | `pip install camel-tools && camel_data -i light` | MIT, permissive; heavy install (Rust, CMake), models downloaded separately |

### Recipes / وصفات

1. **Local font bundle** (step: build; Google Fonts, fontTools). Sparse-clone only the needed `ofl/<family>` folders into `.kosif-cache/`; copy each TTF with its OFL file into `assets/fonts/`; subset to the script's characters, keeping every layout feature so joining forms and mark positioning survive, writing WOFF2; replace the starter's Google Fonts `<link>` with `@font-face` rules on those files so `window.__kosifReady` waits on local fonts. Artefact: `assets/fonts/*.woff2` plus licence files; STYLE.md font row marked *local*.
   **بالعربية:** خطوط مرخّصة محلية ومقلّصة مع إبقاء كل ميزات التشكيل، تحل محل رابط الشبكة في القالب.

2. **Shaping audit** (step: verify; HarfBuzz). When `node tools/render_html.cjs --preview` shows disconnected letters, reversed digits or clipped marks, run `hb-shape` on the same font file and string; if HarfBuzz joins the glyphs but the render does not, the page splits the word, letter-spaces it or fell back to another font; if HarfBuzz is also wrong, swap the font. Artefact: TEST_REPORT.md Arabic row naming string, font and outcome.
   **بالعربية:** قارن ما يُنتجه المُشكِّل المرجعي بما رُندر لتحديد هل الخطأ في الصفحة أم في الخط.

3. **Shaped glyph paths for kinetic type** (step: build; harfbuzzjs). Load the wasm and the same local TTF; shape each whole word; read glyph ids, advances and offsets; turn each glyph into a `Path2D`; animate those paths (draw-on, scale, mask) while keeping their shaped positions. The whole-word rule of `playbooks/arabic-typography.md` holds because shaping finished before motion began; mixed-direction lines stay with the browser. Artefact: `glyphs.json` or a canvas module per title, plus `preview.png`.
   **بالعربية:** شكّل الكلمة كاملة أولًا ثم حرّك مسارات حروفها الناتجة، فتبقى الوصلات والتشكيل سليمة.

4. **Caption-token alignment** (step: sync audio; CAMeL Tools, python-bidi). Install CAMeL Tools first, or run it elsewhere and import the JSON; normalize alef, hamza, ya and tatweel in the user's script and the transcript tokens; tokenize both; match by normalized form, then copy the script's display text with diacritics into `words.json`, keeping the transcript's timings; merge clitics the transcriber split. For burned-in SRT/ASS aimed at players without bidi, pass each line through reshaper then `get_display`; browser and Remotion captions keep logical text. Artefact: corrected `words.json`, optional `captions.srt`.
   **بالعربية:** وحّد الكتابة وقطّع النصين، طابق بالصورة الموحّدة، واحتفظ بنص المستخدم وتوقيت التفريغ.

### Pitfalls / مزالق

- Determinism: a CDN font can fail or change version mid-render and alter widths and shaping; every family lives in `assets/fonts/` and `window.__kosifReady` resolves after `document.fonts.ready`.
- Fonts before frame 0: a subset that drops `init`, `medi`, `fina`, `liga`, `mark` or `mkmk` loads on time but renders disconnected; re-check the first contact-sheet frame after every subset.
- Arabic shaping: browsers and Remotion shape and reorder natively, so reshaper and bidi serve Pillow, Matplotlib and subtitle files only; applying them to text a browser will render yields doubly reversed, pre-shaped junk.
- Per-glyph motion: only shaped glyph output (harfbuzzjs) may be animated glyph by glyph; a `<span>` per letter breaks joins, and no shaper can repair a font lacking ligatures or kashida glyphs.
- Licensing: keep each family's OFL/Apache/UFL file beside the font, subsets included; python-bidi is LGPL and stays a pip dependency, never copied into `tools/`; CAMeL models carry their own terms.
- Installation weight: CAMeL Tools needs a Rust compiler, CMake and hundreds of MB of models; HarfBuzz is a system package; the KOSIF cloud machine ships Node 22, Python 3.13, ffmpeg and Playwright with Chromium under `/opt/pw-browsers` — Whisper and GPU models are absent — so recipes say "install first" or "run elsewhere and import the result".
- Never rehost: fonts are copied under their licence only; reference clips, frames and third-party caption files stay in `.kosif-cache/`, never in `styles/` or the deliverable.
- Never imply integrations that are not installed: run `python3 .claude/skills/kosif-superpowers/scripts/superpowers.py doctor` and name only what it reports present.

### Playbooks extended / الدلائل المعززة

- `playbooks/arabic-typography.md` — local licensed fonts, a reference shaper for its quality checklist, and a sanctioned path to per-glyph motion.
- `playbooks/kinetic-type.md` — shaped glyph paths let draw-on, masks and springs act on Arabic words without disconnecting letters.
- `playbooks/audio-sync.md` — normalization and tokenization reconcile transcript tokens with the user's script and merge split clitics in `words.json`; reshaper and bidi make burned-in SRT/ASS readable in players lacking bidi.
- `playbooks/render-pipeline.md` — WOFF2 subsets and local `@font-face` satisfy the fonts-before-frame-0 rule and make the contact-sheet shaping check conclusive.

<a id="captions"></a>

## captions — الترجمات

*subtitle/caption formats, word-timing conversion, karaoke-style captions* — 5 repositories listed under *captions* in [repos.md](repos.md).

### What it adds / ما تضيفه

KOSIF already turns Whisper JSON, SRT, VTT or CSV into `words.json` with `tools/words_convert.py`; this superpower covers the edges around that converter. It re-times a client's subtitle file to the final mix, aligns an exact Arabic script instead of trusting transcription, and exports the timeline as SRT, VTT or styled ASS, so one `words.json` drives both the kinetic type and the caption file. Burn-in through libass adds a hard-subtitled variant beside the editable film.

**بالعربية:** تضيف هذه القوة ما يحيط بمحوّل `words.json`: إعادة توقيت ترجمة قديمة على المزيج النهائي، ومحاذاة النص العربي الدقيق، وتصدير التوقيت إلى SRT وVTT وASS، ثم حرق الكاريوكي داخل MP4 عند الحاجة.

### Decision table / جدول الاختيار

| need | tool | how | license note |
|---|---|---|---|
| Convert `words.json` or Whisper output to SRT/VTT/ASS, shift cues after a trim, build karaoke ASS | [pysubs2](https://github.com/tkarabela/pysubs2) | `pip install pysubs2` then `pysubs2 --shift 0.3s --to srt in.ass` or `pysubs2.load(path)` | MIT, permissive; credit in TEST_REPORT.md |
| Burn right-to-left Arabic or `\k` karaoke captions into the MP4 | [libass](https://github.com/libass/libass) via ffmpeg | `ffmpeg -i in.mp4 -vf "subtitles=captions.ass:fontsdir=fonts" out.mp4` | ISC, permissive; ships inside ffmpeg builds |
| Re-time a client SRT that was cut against an older edit | [ffsubsync](https://github.com/smacke/ffsubsync) | `ffs final.mp4 -i client.srt -o synced.srt` | MIT, permissive; fused VAD extra pulls in PyTorch |
| Phrase timings from an exact Arabic script without ASR | [aeneas](https://github.com/readbeyond/aeneas) | `python -m aeneas.tools.execute_task audio.mp3 script.txt "task_language=ara\|is_text_type=plain\|os_task_file_format=json" out.json` | AGPL-3.0, copyleft; call the CLI, never vendor or import its code |
| Word and phoneme timestamps for progressive reveals or lip-sync | [Montreal Forced Aligner](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner) | `mfa align corpus/ dict acoustic out/` after the conda install and `mfa model download acoustic <lang>` | MIT, permissive; heavy Kaldi/conda install |

### Recipes / وصفات

1. **Re-time a client SRT — sync audio — ffsubsync + `tools/words_convert.py`.** Install ffsubsync first, then run `ffs` against the final MP4 with the client SRT as input. Spot-check three cues; for a mid-film re-cut, split the SRT there and sync each half. Convert the synced SRT to `words.json` and hand-correct key words to the 100 ms tolerance. Artefact: `words.json`.
   **بالعربية:** أعد توقيت SRT القديم على المزيج النهائي، حوّله إلى `words.json`، وصحّح الكلمات المفتاحية.

2. **Exact Arabic script to phrase timings — sync audio — aeneas.** Write the script one phrase per line (a pause > 400 ms ends a phrase). Run aeneas elsewhere, or in a separate older-Python environment with eSpeak, asking for JSON output. Spread each fragment into `word,start,end` CSV rows, then `python3 tools/words_convert.py fragments.csv words.json`. Fragment ends become PLAN.md scene boundaries. Artefact: `words.json`, PLAN.md timings.
   **بالعربية:** حاذِ نصّ العميل سطرًا لكل عبارة، ثم حوّل التوقيت إلى `words.json` وحدود المشاهد.

3. **Phoneme-level timing — build — Montreal Forced Aligner.** Run MFA outside the cloud machine on audio plus matching transcripts with a downloaded Arabic model and dictionary. Convert the TextGrid word tier to CSV, then to `words.json`; keep the phoneme tier as `phonemes.csv` for mouth shapes. Artefact: `words.json`, `phonemes.csv`.
   **بالعربية:** شغّل المحاذاة القسرية خارج الجهاز السحابي، وحوّل الكلمات إلى `words.json` واحتفظ بالفونيمات لأشكال الفم.

4. **Sidecar captions from the film's timeline — deliver — pysubs2.** Load `words.json`, group words into phrases on pauses > 400 ms within the 14–22 character portrait line rule. Save one cue per phrase as SRT and VTT and check boundaries against the preview contact sheet. Artefact: `captions.srt`, `captions.vtt` beside the MP4.
   **بالعربية:** جمّع كلمات `words.json` في عبارات عند الوقفات وصدّر SRT وVTT مرافقين.

5. **Burned-in Arabic karaoke — render — pysubs2 + libass.** From `words.json`, write one ASS line per phrase with a `\k` duration (centiseconds) per word, styled with a bundled open-licence Arabic font. After `render_html.cjs` produces `film.mp4`, run ffmpeg's `subtitles` filter with `fontsdir` on that folder, copying the audio unchanged. Re-run `python3 tools/verify_video.py` and compare one frame against the contact sheet. Artefact: `film_captioned.mp4` and the ASS source.
   **بالعربية:** أنشئ ASS بوسوم كاريوكي لكل كلمة، واحرقه بخط عربي مرفق دون تغيير الصوت، ثم أعد التحقق.

### Pitfalls / مزالق

- Determinism: libass repeats exactly only with the same font files, so always pass `fontsdir` with the bundled font; a fontconfig fallback changes Arabic widths.
- Arabic shaping: pysubs2 only edits text and times; joining and bidi happen in libass, which needs HarfBuzz and FriBidi in the ffmpeg build. Check `ffmpeg -version` for `--enable-libass`; disjoint or reversed glyphs mean fall back to DOM captions. Apply `\k` per Arabic word, never per letter.
- Licensing: aeneas is AGPL, so call its CLI from a subprocess and keep none of its code in the repo; credit all five tools in TEST_REPORT.md; client SRTs and reference videos are never rehosted.
- Installation weight: MFA needs conda and Kaldi, aeneas a C extension, eSpeak and a 2017-era Python, ffsubsync's fused VAD pulls PyTorch. None of them, nor Whisper or any GPU model, is on the KOSIF cloud machine (Node 22, Python 3.13, ffmpeg, Playwright with Chromium under `/opt/pw-browsers`). Run the superpowers `doctor`, then say "install first" or "run elsewhere and import the result"; never imply integrations that are not installed.
- Fonts before frame 0: DOM captions wait for `document.fonts.ready` and `window.__kosifReady`; burned captions find their font in `fontsdir`, never on the network.
- Burn-in is a second encode: copy the audio, keep the CRF from `playbooks/render-pipeline.md` §5, re-gate.
- SRT and aeneas give phrase timing, not word onsets; names and numbers still need the manual pass in `playbooks/audio-sync.md`.

### Playbooks extended / الدلائل المعززة

- `playbooks/audio-sync.md` — step 2 gains script alignment (aeneas, MFA), step 3 gains SRT re-timing before `words_convert.py`.
- `playbooks/kinetic-type.md` — recipe B (karaoke caption) gets a burned-in ASS twin with identical word timings.
- `playbooks/arabic-typography.md` — shaping and bundled-font checks extend to libass burn-in via `fontsdir`.
- `playbooks/render-pipeline.md` — an optional burn-in stage between final render and the `verify_video.py` gate, audio untouched.
- `playbooks/characters.md` — MFA's phoneme tier supplies mouth-shape timing for lip-sync.

<a id="generate"></a>

## generate — التوليد

*AI-generated images, video, 3D, talking heads and voices used as original assets within their licenses* — 7 repositories listed under *generate* in [repos.md](repos.md).

### What it adds / ما تضيفه

The generate superpower supplies original assets a film lacks: style-matched backgrounds and textures, short motion plates, a mesh for a 3D camera, or a presenter speaking the user's own narration. Each output is produced once, seeded where the tool allows, saved under the film's `assets/` folder with an `ASSETS.md` row, and declared in STYLE.md as generated; the render loop only loads files. None of these tools exist on the KOSIF cloud machine: install first on a GPU host, or run elsewhere and import the result.

**بالعربية:** قوة التوليد تنتج أصولًا أصلية ينقصها الفيلم: خلفيات وملمسات على طراز الاستايل، لقطات حركة قصيرة، شبكة ثلاثية الأبعاد لكاميرا حقيقية، أو مقدِّم ينطق تعليق المستخدم نفسه. يُولَّد كل أصل مرة واحدة ببذرة ثابتة، يُحفظ في `assets/` مع صف في `ASSETS.md`، ويُصرَّح به في STYLE.md؛ أما حلقة الرندر فتحمّل ملفات فقط. لا شيء من هذه الأدوات مثبّت على جهاز KOSIF السحابي، فكل وصفة إما «ثبّت أولًا» على جهاز بمعالج رسومي أو «شغّله في مكان آخر واستورد النتيجة».

### Decision table / جدول الاختيار

| need | tool | how | license note |
|---|---|---|---|
| scripted, seeded stills: backgrounds, textures, loop frames | [Diffusers](https://github.com/huggingface/diffusers) | `pip install diffusers[torch]`, then a pipeline call with a manual-seed generator | Apache-2.0 code; each checkpoint has its own terms, some non-commercial |
| a saved node graph re-run for every revision of a film | [ComfyUI](https://github.com/Comfy-Org/ComfyUI) | `pip install comfy-cli && comfy install`; POST the API-format workflow JSON to the local `/prompt` endpoint | GPL-3.0, copyleft: external tool only, never vendored; weights separate |
| props and plates that land on the Arabic type grid | [ControlNet](https://github.com/lllyasviel/ControlNet) | depth, canny or scribble map from the storyboard; prefer the 1.1 models through Diffusers | Apache-2.0 code; SD weights under CreativeML terms, check commercial use |
| still → short motion plate, two designed frames → transition | [LTX-Video](https://github.com/Lightricks/LTX-Video) | `pip install -e .[inference]`, then the inference script with conditioning images and a pipeline config | Apache-2.0 code; weights OpenRAIL-M; successor lives in the LTX-2 repo |
| B-roll loops on a small GPU, first-to-last-frame bridges | [Wan2.1](https://github.com/Wan-Video/Wan2.1) | `python generate.py --task t2v-1.3B` with the 480p size and model offload | Apache-2.0, permissive; 14B and FLF2V modes need large GPUs |
| one product still or icon → textured mesh | [TripoSR](https://github.com/VAST-AI-Research/TripoSR) | `python run.py input.png --output-dir out/ --bake-texture`, then OBJ → glTF in Blender | MIT, permissive; weights fetched from Hugging Face |
| portrait + untouched narration → lip-synced presenter clip | [SadTalker](https://github.com/OpenTalker/SadTalker) | `python inference.py --driven_audio voice.wav --source_image face.png` | Apache-2.0 code; weight licensing unstated; portrait needs a model release |

### Recipes / وصفات

1. **Seeded background plates** (step: build; Diffusers or ComfyUI). Describe STYLE.md's palette and texture rows in your own prompt; run Diffusers on a GPU host, or a ComfyUI workflow, with one fixed seed per scene; generate at the master aspect plus 12% bleed for camera drift; save as `assets/bg_<scene>.png`, add `ASSETS.md` rows (seed, model, license) and mark the plates *generated* in STYLE.md. Artefact: `assets/bg_*.png`, `ASSETS.md` rows, STYLE.md disclosure line.
   **بالعربية:** خلفيات ببذرة ثابتة لكل مشهد، مُوسَّعة قليلًا للانجراف، مسجّلة بترخيصها ومصرَّح بها.

2. **Props that respect the type grid** (step: plan → build; ControlNet via Diffusers). Export the PLAN.md layout as a scribble or depth map with the Arabic text area empty; run a ControlNet 1.1 model on it so props stay out of the safe area; cut the result with rembg (see observe) and place it as `assets/subject.png` at depth 1.0 in the photos rig. Artefact: control map in `.kosif-cache/`, `assets/subject.png`, PLAN.md asset row.
   **بالعربية:** خريطة تحكم من التخطيط تُبقي المولَّد خارج منطقة النص العربي.

3. **Keyframe bridge** (step: build → render; LTX-Video or Wan2.1). Save scene A's last frame and scene B's first as stills; run first-to-last-frame generation elsewhere, 2–3 s, at the master size; import as `assets/bridge_<n>.mp4`, draw it under the typography layer with `seek(t)` setting the video time, and check the contact sheet for halos. Artefact: `assets/bridge_*.mp4`, PLAN.md transition row, preview.png.
   **بالعربية:** جسر عضوي بين إطارَين مصمَّمَين، يُركَّب تحت طبقة النص ويُفحص في لوحة الإطارات.

4. **Icon to mesh** (step: build; TripoSR, Blender). Clean the product still to a flat background; run TripoSR with texture baking on a GPU host; convert OBJ to glTF in Blender, retouching guessed back faces; load `assets/product.glb` in the Three.js seek scene from `playbooks/3d.md`. Artefact: `assets/product.glb`, `ASSETS.md` row.
   **بالعربية:** من صورة واحدة إلى شبكة glTF تدور أمام كاميرا حقيقية.

5. **Presenter from the user's voice** (step: build → sync audio; SadTalker). Convert the narration to WAV untrimmed; run SadTalker with the released portrait; keep the clip's video only as `assets/presenter.mp4`; composite it, mux the original `voice.mp3` at render and confirm with `verify_video.py --audio`. Artefact: `assets/presenter.mp4`, TEST_REPORT.md audio row.
   **بالعربية:** المقدِّم يتحرك على صوت المستخدم، والصوت الأصلي يُدمج دون تغيير عند الرندر.

### Pitfalls / مزالق

- **Determinism:** Diffusers and ComfyUI repeat a seed on identical hardware and versions; Wan2.1, LTX-Video and SadTalker drift between runs — generate once, store the file, record seed and model in `ASSETS.md`, never inside `seek(t)`.
- **Arabic shaping:** no diffusion model renders Arabic letters correctly; keep every word in the HTML or Remotion text layer and mask glyph-like scribbles out of generated plates.
- **Licensing:** code is permissive except ComfyUI (GPL, external tool), but weights carry their own terms (CreativeML, OpenRAIL-M, unstated for SadTalker); check commercial use per checkpoint, keep a portrait release, declare generated imagery and never present it as documentary evidence (`playbooks/photos.md`).
- **GPU and weight:** every tool needs PyTorch, multi-gigabyte checkpoints and usually CUDA; budget minutes per clip.
- **Fonts before frame 0:** plates load as images, but type still waits on `window.__kosifReady`; a late font shifts Arabic widths over a finished plate.
- **Never rehost:** reference frames are never conditioning inputs; control maps come from your own storyboard, and nothing derived from third-party media enters `styles/` or `catalog/`.
- **Never imply integrations that are not installed:** the KOSIF cloud machine has Node 22, Python 3.13, ffmpeg and Playwright with Chromium under `/opt/pw-browsers`; Whisper and GPU models are absent, so run the doctor and write "install first" or "run elsewhere and import the result".

### Playbooks extended / الدلائل المعززة

- `playbooks/photos.md` — generated plates and cutouts join the parallax rig under the same `ASSETS.md` discipline.
- `playbooks/ads.md` — product plates and short B-roll behind the hook without stock footage.
- `playbooks/particles.md` — seeded textures replace per-frame randomness.
- `playbooks/characters.md` — a talking presenter among rigged characters.
- `playbooks/hand-drawn.md` — storyboard scribbles become control maps for props the hand draws over.
- `playbooks/3d.md` — TripoSR meshes give the camera real geometry.
- `playbooks/product-ui.md` — device meshes for hero shots around rebuilt UI.
- `playbooks/audio-sync.md` — the avatar follows the untouched narration; the original track is muxed at render.
- `playbooks/render-pipeline.md` — assets are files loaded before frame 0, checked on the contact sheet, gated unchanged.

<a id="orchestrate"></a>

## orchestrate — التنسيق

*Claude Code skills, agent workflows, MCP servers and browser automation for inspection and QA* — 8 repositories listed under *orchestrate* in [repos.md](repos.md).

### What it adds / ما تضيفه

Orchestrate gives the film-maker eyes and discipline, not pixels: a real browser that opens the HTML film at any `window.__kosif.seek(t)` checkpoint, a network panel that reveals the media URL behind a `blob:` player, version-pinned library docs before a timeline is written, and MCP wrappers that expose `tools/kosif.py` and `tools/verify_video.py` to any agent. The workflow repositories supply the process: brainstorm, plan, build, verify before claiming done. Nothing here renders a frame.

**بالعربية:** قوة التنسيق عينٌ وانضباط لا بكسلات: متصفح حقيقي يفتح الفيلم عند أي لحظة، لوحة شبكة تكشف رابط الوسائط المخفي، وثائق مكتبات بإصدار محدد، وأغلفة MCP لأدوات المستودع، وعملية: فكّر، خطّط، ابنِ مشهدًا مشهدًا، وتحقق قبل «تم».

### Decision table / جدول الاختيار

| need | tool | how | license note |
|---|---|---|---|
| open the preview at checkpoint times, read DOM order of Arabic runs, screenshot before the final render | [Playwright MCP](https://github.com/microsoft/playwright-mcp) | `claude mcp add playwright npx @playwright/mcp@latest` with headless Chromium; add the vision capability for pixel clicks | Apache-2.0, permissive; wants its own Chromium (~150 MB) — point it at `/opt/pw-browsers` via `PLAYWRIGHT_BROWSERS_PATH` |
| find the real media URL behind a `blob:` player; console errors and frame-time traces of heavy canvas/WebGL scenes | [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp) | `claude mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest`; tools for network requests, performance trace, screenshot | Apache-2.0, permissive; needs a current stable Chrome (install first); usage statistics on by default |
| exact GSAP, anime.js, Three.js, Remotion and ffmpeg signatures while writing timelines or render scripts | [Context7](https://github.com/upstash/context7) | `npx ctx7 setup --claude`, then name the library in the prompt | MIT, permissive; hosted service, network and API key required |
| the brainstorm → plan → execute → verify discipline the runbook follows | [Superpowers](https://github.com/obra/superpowers) | `/plugin install superpowers@claude-plugins-official`; skills trigger by name | MIT, permissive; English-only methodology, no renderer |
| canonical SKILL.md frontmatter, folder layout and an eval loop for this skill's triggering | [Anthropic Agent Skills](https://github.com/anthropics/skills) | `git clone https://github.com/anthropics/skills`; copy the template folder, run skill-creator evals | Apache-2.0 for spec and template; document skills source-available — read before reuse |
| expose `kosif.py` search/scaffold/validate and ffprobe checks as MCP tools | [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) | `pip install "mcp[cli]"`; decorate functions as tools, serve over stdio, register in `.mcp.json` | MIT, permissive; Python 3.11+; v2 API names differ from older tutorials |
| drive the whole pipeline headless with a hook that blocks delivery when the gate fails | [Claude Agent SDK (Python)](https://github.com/anthropics/claude-agent-sdk-python) | `pip install claude-agent-sdk`; `query()` plus a PreToolUse hook | MIT, permissive; bundles the Claude Code CLI, needs an Anthropic account; runs are non-deterministic |
| package styles, playbooks and scripts as one installable plugin | [Claude Plugins Official](https://github.com/anthropics/claude-plugins-official) | copy the example plugin and marketplace manifest as the layout model | Apache-2.0 for the directory; each plugin has its own license — review before installing |

### Recipes / وصفات

1. **Checkpoint walk** (step: verify; Playwright MCP). Open `film.html` headless; at each PLAN.md scene start call `window.__kosif.seek(t)` via page-evaluate; snapshot the DOM for right-to-left order and unmirrored numbers; screenshot at 1080 and 360 px; fill TEST_REPORT.md rows 8, 9, 12. Artefact: `out/checkpoints/*.png`.
   **بالعربية:** اقفز إلى بداية كل مشهد في متصفح حقيقي، افحص الاتجاه واللقطات، ودوّن النتائج.

2. **Media behind a blob player** (step: observe; Chrome DevTools MCP). Open the permitted reference page; list media and manifest requests as the player starts; pass the direct URL to `scripts/fetch_reference.py` (encrypted streams still refused); note it in STYLE.md section 1. Artefact: `.kosif-cache/reference/<slug>/REPORT.md`.
   **بالعربية:** استخرج رابط الوسائط من لوحة الشبكة ومرّره لسكربت الجلب، للمواد المسموح بتحليلها فقط.

3. **Signatures before the timeline** (step: build; Context7). Before writing `draw(t)` or a Remotion sequence, request docs for the library version pinned in `package.json`; keep only the needed signature as a comment; repeat for ffmpeg flags before editing a render script. Artefact: PLAN.md stack row with pinned versions.
   **بالعربية:** اطلب توقيعات الدوال للإصدار المثبّت قبل كتابة الخط الزمني.

4. **KOSIF as MCP tools with a delivery hook** (step: plan → deliver; MCP Python SDK, Claude Agent SDK). Wrap `kosif.py search`, `scaffold`, `validate.py` and `verify_video.py --json` as tools in a stdio server registered in `.mcp.json`; in a headless Agent SDK run, a PreToolUse hook reads the verify JSON and refuses to copy or upload the MP4 while any check is FAIL. Artefact: `kosif_mcp.py`, `out/verify.json`.
   **بالعربية:** غلّف أدوات المستودع كأدوات MCP، وخطاف يمنع التسليم ما دامت البوابة فاشلة.

### Pitfalls / مزالق

- Determinism: MCP browsers look, never capture; delivery frames come only from `tools/render_html.cjs` or Remotion; Agent SDK runs vary.
- Arabic shaping: accessibility snapshots give logical order and hide canvas/WebGL text; judge joining and diacritics on a phone-scale screenshot.
- Fonts before frame 0: await `window.__kosifReady` before any checkpoint screenshot; a late font masks a renderer fallback.
- Installation weight: both browser MCPs pull a browser; reuse Chromium under `/opt/pw-browsers`, never run a browser install; Chrome is *install first*.
- Never imply integrations that are not installed: the machine ships Node 22, Python 3.13, ffmpeg and Playwright with Chromium; MCP servers, Context7, the SDKs, Whisper and GPU models are absent until the doctor says otherwise — write "install first" or "run elsewhere and import the result".
- Never rehost third-party media: a network-panel URL serves analysis of permitted material only; nothing from it is committed or embedded.
- Licensing and privacy: all eight are permissive, but directory plugins carry their own licenses; DevTools and Context7 send page contents or queries to remote services, telemetry on by default; process plugins know no Arabic — the playbooks win.

### Playbooks extended / الدلائل المعززة

- `playbooks/render-pipeline.md` — checkpoint pass before the gate; a hook enforcing it at delivery.
- `playbooks/arabic-typography.md` — DOM direction checks and phone-scale screenshots for shaping and digits.
- `playbooks/product-ui.md` — real-browser inspection of rebuilt screens and pointer paths.
- `playbooks/particles.md`, `playbooks/3d.md` — performance traces of heavy canvas/WebGL scenes against the 50 ms budget.
- `playbooks/kinetic-type.md`, `playbooks/code.md` — exact easing and API signatures before keying words to `words.json`.
- `playbooks/audio-sync.md` — verify tools over MCP so every agent checks the audio-duration match.

#### Process superpowers / قوى العملية

1. Run the doctor; plan only with installed tools.
2. Brainstorm before code: concept, audience, aspect, duration, source material, unknowns; one batch of questions; pick the style ID.
3. Observe the reference, or state in STYLE.md that you could not.
4. Write STYLE.md (observed versus assumed) and PLAN.md scene by scene, timestamps from `words.json` or `cuts.json`.
5. Execute scene by scene, one commit each; parallel scenes go to one subagent each in its own git worktree, returning a preview frame and the files changed; merge, preview the whole film.
6. Sync to the voice as master clock; never alter the audio.
7. Verify before claiming completion: contact sheet, 2–4 s motion clip, approval, final render, `python3 tools/verify_video.py` gate, TEST_REPORT.md with measured values.
8. Request review against the guardrails (observed/assumed, credits, no rehosted media, determinism, Arabic shaping, timing); apply it.
9. Finish the branch: editable sources beside the MP4; commit, push, PR only when asked.

**بالعربية:** افحص الأدوات، فكّر قبل الكود، ارصد المرجع، اكتب STYLE.md وPLAN.md بالأزمنة، ابنِ المشاهد في التزامات منفصلة أو عبر وكلاء في worktrees، زامن مع الصوت، تحقق بالبوابة والتقرير، راجع، ثم أنهِ الفرع.

<a id="design"></a>

## design — التصميم

*UI motion patterns, icon sets, design tokens, scroll and parallax libraries* — 6 repositories listed under *design* in [repos.md](repos.md).

### What it adds / ما تضيفه

The design superpower gives a KOSIF film one visual vocabulary: a token source read by both `starters/html-canvas` and `starters/remotion`, a uniform stroke-icon set for draw-on and UI mock-ups, real components for dashboards, exact editor colours for code and a scroll engine driven from the timeline. All of it lives at the build step, so the contact sheet shows what STYLE.md promised.

**بالعربية:** مفردات بصرية واحدة للفيلم: رموز تصميم مشتركة، أيقونات خطية متجانسة، مكوّنات حقيقية، ألوان محرر دقيقة، وتمرير يُقاد من الخط الزمني.

### Decision table / جدول الاختيار

| need | tool | how | license note |
|---|---|---|---|
| uniform stroke icons for UI, diagrams and draw-on | [Lucide Icons](https://github.com/lucide-icons/lucide) | `npm i lucide-react lucide-static`; read raw SVG from lucide-static for Canvas | ISC; credit in the stack line |
| one token source for CSS variables and TS constants | [Style Dictionary](https://github.com/style-dictionary/style-dictionary) | `npm i -D style-dictionary`; build with the css/variables and javascript/es6 formats | Apache-2.0; v4+ is ESM-only |
| eased, frame-exact scroll inside a mock screen | [Lenis](https://github.com/darkroomengineering/lenis) | `npm i lenis`; construct with `autoRaf: false`, position it from `seek(t)` | MIT |
| animatable cards, tables, dialogs in Remotion | [shadcn/ui](https://github.com/shadcn-ui/ui) | `npx shadcn@latest add card button table` after Tailwind is wired into the Remotion project | MIT; components become your source |
| VS Code-accurate code colours as drawable tokens | [Shiki](https://github.com/shikijs/shiki) | `npm i shiki`; `codeToTokens(src, { lang, theme })` then draw each token | MIT; grammars and themes carry their own notices |
| an icon Lucide lacks (Material, Phosphor, Tabler…) | [Iconify](https://github.com/iconify/iconify) | `npm i @iconify/utils @iconify-json/mdi`; `iconToSVG` from the local JSON set | MIT framework; each icon set keeps its own licence |

### Recipes / وصفات

1. **Token table → both renderers** (step: plan → build; Style Dictionary). Fill STYLE.md section 4 (`STYLE.json` is catalog metadata, not tokens); copy each row into `tokens.json` in the tool's nesting; build once to `tokens.css` and `tokens.ts`; load the CSS into `index.html`'s `:root`, import the constants in `Film.tsx`. Artefact: `tokens.css`, `tokens.ts`, STYLE.md token table.
   **بالعربية:** رموز STYLE.md تُبنى مرة واحدة إلى CSS وTypeScript فيتفق المساران.

2. **Draw-on icon vocabulary** (step: build; Lucide, Iconify as fallback). Pick icons at one stroke width; inline SVG paths from lucide-static, or missing ones from a locally installed Iconify JSON set; set `pathLength="1"` and move `strokeDashoffset` with `KOSIF.prog(t, …)` as `playbooks/diagrams.md` does; mirror only directional glyphs for RTL. Artefact: `icons/` of inline SVG, the icon scene, attribution in TEST_REPORT.md.
   **بالعربية:** أيقونات بوزن واحد تُرسم تدريجيًا، ولا يُعكس منها إلا ما له اتجاه.

3. **Frame-exact scroll beat** (step: build → render; Lenis). Build the feed as real DOM inside the clipped screen; create Lenis with `autoRaf` off; in `seek(t)` compute the eased target from PLAN.md's beats (450 ms moves, 600 ms holds per `playbooks/phone.md`) and call `scrollTo` with `immediate`, or feed `raf` fixed frame times under `--mode virtual`. Artefact: scroll scene, `out/check.mp4`, `preview.png` rendered twice identically.
   **بالعربية:** موضع التمرير يُحسب من الزمن لا من ساعة المتصفح.

4. **Animatable dashboard** (step: build; shadcn/ui). Install Tailwind into `starters/remotion` first (absent by default); initialise shadcn, add card, table, button; set `dir="rtl"` and a local Arabic family; drive values and staggers from `useCurrentFrame()` with `playbooks/product-ui.md` timings; check via `npx remotion still`. Artefact: `Screen.tsx` from `components/ui`, `out/still.png`.
   **بالعربية:** لوحة تحكم من مكوّنات قابلة للتعديل، لا لقطة ملصوقة.

5. **Code scene in exact theme colours** (step: build; Shiki). Preload one language and theme from the fine-grained bundle before `window.__kosifReady` resolves; call `codeToTokens`, cache it as `code-tokens.json`; draw each line's tokens on Canvas with the typed index and highlight band from `playbooks/code.md`. Artefact: `code-tokens.json`, the code scene.
   **بالعربية:** ألوان المحرر تصير رموزًا تُرسم على الكانفاس.

### Pitfalls / مزالق

- **Determinism.** Lenis with `autoRaf` on, shadcn's CSS transitions and Shiki's async loading drift between runs: position scroll from `t`, pause DOM animations inside `seek` or use `--mode virtual`, highlight before frame 0.
- **Arabic shaping.** No icon set ships Arabic glyphs, so labels stay text; code stays LTR via `unicode-bidi: isolate`; shadcn needs `dir="rtl"`, logical utilities and a manually added Arabic font.
- **Licensing.** All six are permissive, but Iconify sets are licensed individually (some require attribution) and Shiki themes carry notices; record what shipped in TEST_REPORT.md and keep third-party files out of `styles/` and `catalog/`.
- **Weight.** Shiki's WASM engine plus grammars reaches several MB (use the fine-grained bundle); shadcn pulls Tailwind and Radix into Remotion. None needs a GPU.
- **Fonts before frame 0.** Tokens and components name font families; load them locally and resolve `window.__kosifReady` first, or text metrics shift on the contact sheet.
- **Never rehost.** Iconify's web component fetches icons over the network at render time: install JSON sets locally and inline the SVG; reference screenshots stay in `.kosif-cache/`, never in the deliverable.
- **Never imply integrations that are not installed.** None of these packages exists on the KOSIF cloud machine (Node 22, Python 3.13, ffmpeg, Playwright with Chromium under `/opt/pw-browsers`; no Whisper, no GPU models) until `npm install` runs in the film directory; run the doctor and write "install first" in PLAN.md.
- **Playbook numbers win.** Library defaults yield to the playbooks' millisecond tables.

### Playbooks extended / الدلائل المعززة

- `playbooks/product-ui.md`: components, icons and tokens make layered screens retimable.
- `playbooks/phone.md`: Lenis gives one-card-per-beat scroll a deterministic position.
- `playbooks/charts.md`: shadcn cards and tables frame KPI tiles that agree with the chart.
- `playbooks/code.md`: Shiki supplies per-token colours for typing and highlight bands.
- `playbooks/diagrams.md`, `playbooks/shapes.md`: stroke icons share the draw-on grammar.
- `playbooks/kinetic-type.md`: type-scale and easing tokens travel with the palette.
- `playbooks/arabic-typography.md`: its mirroring rules decide which icons flip.
- `playbooks/render-pipeline.md`: offline icon sets and one token build keep renders network-free.

## Credits — الحقوق

Every tool named above belongs to its authors under the license recorded in [repos.md](repos.md). KOSIF describes how to use them in its own words and never redistributes their code, prompts, media or weights.

**بالعربية:** كل أداة أعلاه ملك لأصحابها بترخيصها المسجّل في repos.md؛ يصف KOSIF طريقة استخدامها بكلماته ولا يعيد توزيع كودها أو وسائطها أو أوزانها.
