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

_Section pending — see repos.md for the tools._

<a id="draw"></a>

## draw — الرسم

*2D creative coding, SVG/Canvas drawing, hand-drawn and sketchy looks, draw-on strokes* — 8 repositories listed under *draw* in [repos.md](repos.md).

_Section pending — see repos.md for the tools._

<a id="data"></a>

## data — البيانات

*charts, maps, diagrams and data-driven motion* — 8 repositories listed under *data* in [repos.md](repos.md).

_Section pending — see repos.md for the tools._

<a id="voice"></a>

## voice — الصوت

*speech-to-text with word timestamps, forced alignment, TTS, music/beat analysis, loudness* — 10 repositories listed under *voice* in [repos.md](repos.md).

_Section pending — see repos.md for the tools._

<a id="arabic"></a>

## arabic — النص العربي

*Arabic/RTL shaping, bidi, fonts, diacritics and Arabic NLP for captions and kinetic type* — 7 repositories listed under *arabic* in [repos.md](repos.md).

_Section pending — see repos.md for the tools._

<a id="captions"></a>

## captions — الترجمات

*subtitle/caption formats, word-timing conversion, karaoke-style captions* — 5 repositories listed under *captions* in [repos.md](repos.md).

_Section pending — see repos.md for the tools._

<a id="generate"></a>

## generate — التوليد

*AI-generated images, video, 3D, talking heads and voices used as original assets within their licenses* — 7 repositories listed under *generate* in [repos.md](repos.md).

_Section pending — see repos.md for the tools._

<a id="orchestrate"></a>

## orchestrate — التنسيق

*Claude Code skills, agent workflows, MCP servers and browser automation for inspection and QA* — 8 repositories listed under *orchestrate* in [repos.md](repos.md).

_Section pending — see repos.md for the tools._

<a id="design"></a>

## design — التصميم

*UI motion patterns, icon sets, design tokens, scroll and parallax libraries* — 6 repositories listed under *design* in [repos.md](repos.md).

_Section pending — see repos.md for the tools._

## Credits — الحقوق

Every tool named above belongs to its authors under the license recorded in [repos.md](repos.md). KOSIF describes how to use them in its own words and never redistributes their code, prompts, media or weights.

**بالعربية:** كل أداة أعلاه ملك لأصحابها بترخيصها المسجّل في repos.md؛ يصف KOSIF طريقة استخدامها بكلماته ولا يعيد توزيع كودها أو وسائطها أو أوزانها.
