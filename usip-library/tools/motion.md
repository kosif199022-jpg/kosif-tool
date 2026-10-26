# أدوات المجال `motion` (25 أداة)

> مولّد من `data/tools.json`. [الفهرس الرئيسي](../README.md) · `python3 scripts/hub.py tool <id>` للبطاقة الحية.

### `aspects` — محلّل نِسَب أبعاد الفيديو / Flexible aspect ratio resolver

| الحقل | القيمة |
|---|---|
| المسار | `scripts/aspects.py` (جذر: skill) |
| المجال | `motion` |
| الدليل | `tested-here` |
| العائلات | `formats-platforms` |

**ما تفعله:** وحدة بايثون لا تعتمد إلا على المكتبة القياسية، تحوّل أي صيغة لنسبة الأبعاد (نسبة W:H، أو أبعاد WxH بالبكسل، أو اسم منصة بالإنجليزية أو العربية مثل reel أو سينما أو مربع) إلى تسمية وأبعاد بكسل زوجية، مع دوال لحساب النسبة ونص الدقة والتحقق من الصحة.

**What it does:** Standard-library Python module that turns any aspect spec (W:H ratio, WxH pixels, or an English/Arabic platform name such as reel, cinema or مربع) into a label and even pixel dimensions, plus ratio, resolution-string and validity helpers.

#### متى تُستدعى

- «What pixel size should a 2.35:1 cinema video be?»
- «Resolve 'reel' or '21:9' to an even H.264-safe resolution»
- «كم أبعاد فيديو مقاس سينمائي أو مربع؟»
- «ابي أعرف الدقة المناسبة لمقاس تيك توك»
- «Validate the aspect the user typed before scaffolding»

#### الأوامر

- **import**: Imports the module from the skill root; prints ('2.35:1', 1920, 818).
  - `python3 -c "import sys; sys.path.insert(0,'scripts'); import aspects; print(aspects.resolve('2.35:1'))"`
- **resolve**: Returns (label, width, height) with even dimensions; here ('9:16', 1080, 1920). Raises ValueError for unreadable specs or W:H ratios outside 1:5–5:1 (explicit WxH sizes are not range-checked).
  - `python3 -c "import sys; sys.path.insert(0,'scripts'); from aspects import resolve; print(resolve('ريلز'))"`
- **ratio_of**: Returns width/height as a float for any accepted spec (2.3529… here).
  - `python3 -c "import sys; sys.path.insert(0,'scripts'); from aspects import ratio_of; print(ratio_of('1920x816'))"`
- **resolution**: Returns a 'WxH' string; cinema -> 1920x804.
  - `python3 -c "import sys; sys.path.insert(0,'scripts'); from aspects import resolution; print(resolution('cinema'))"`
- **is_valid**: Returns True/False instead of raising (False here).
  - `python3 -c "import sys; sys.path.insert(0,'scripts'); from aspects import is_valid; print(is_valid('foo'))"`

#### المتطلبات والأمان

- الأمان: read-only
- الموافقة: —
- الحدود: Only maps aspect specs to even pixel sizes (1080 px short side for ratios between 9:16 and 16:9, otherwise a 1920 px long side; W:H limited to 1:5–5:1); it does not resize, crop or reframe media.

#### الاختبارات والأدلة

- `tests/test_aspects.py`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/motion.md`
- مرجع: `.claude/skills/kosif-superpowers/references/executable-creative-motion.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:aspects --evidence <ملف>`.

### `atlas-render` — رندر أفلام الشرح: ستوريبورد وفحص حتمية وMP4 حقيقي بصوت مُركّب / Atlas explainer renderer: storyboard, determinism check and real MP4 with synthesized score

| الحقل | القيمة |
|---|---|
| المسار | `scripts/atlas_render.py` (جذر: skill) |
| المجال | `motion` |
| الدليل | `tested-here` |
| العائلات | `hand-drawn-draw-on`, `story-direction-ideas` |

**ما تفعله:** يشغّل صفحة شرح A15 في متصفح بلا واجهة: لوحة ستوريبورد، لقطات، فحص حتمية وسرعة، رندر MP4 إطارًا بإطار مع صوت مُركّب متزامن، وحزمة HTML واحدة.

**What it does:** Drives an A15 explainer page (window.seek/DURATION/scoreSound) in headless Chromium: storyboard grid PNG, single stills, a determinism and speed check, frame-by-frame H.264 render with the KSound score rendered offline and muxed as AAC, and a single-file HTML bundle.

#### متى تُستدعى

- «رندر فيلم الشرح إلى MP4»
- «اعرض لي الستوريبورد قبل الفيلم»
- «Render the explainer page to video»
- «Check the explainer is deterministic»

#### الأوامر

- **check**: Same t -> same pixels at 4 probes, ms per frame, beats, scoreSound present.
  - `python3 scripts/atlas_render.py check`
- **storyboard**: PNG of the ?storyboard=1 grid.
  - `python3 scripts/atlas_render.py storyboard --out out/atlas/storyboard.png`
- **render**: H.264 frames + offline-rendered AAC score.
  - `python3 scripts/atlas_render.py render --fps 30 --out out/atlas/film.mp4`
- **bundle**: Inlines scripts and the font into one HTML file.
  - `python3 scripts/atlas_render.py bundle --out out/atlas/single.html`

#### المتطلبات والأمان

- binaries: ffmpeg
- python: playwright
- الأمان: writes-files
- الموافقة: Writes only the --out path; refuses to overwrite without --force; no network.
- الحدود: Needs Playwright with Chromium and ffmpeg; frame capture is ~4-6 fps of wall time at 1280x720; audio is the page's synthesized score (no voice-over mixing yet).

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_atlas_render.py`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A15-futurepedia-style-atlas.md`
- مرجع: `.claude/skills/kosif-superpowers/proofs/style-atlas-86/README.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:atlas-render --evidence <ملف>`.

### `creative-reasoning-bridge` — جسر الصوت إلى لوحة القصة / Audio-to-Storyboard Bridge

| الحقل | القيمة |
|---|---|
| المسار | `scripts/creative_reasoning_bridge.py` (جذر: skill) |
| المجال | `motion` |
| الدليل | `tested-here` |
| العائلات | `audio-sync-captions`, `story-direction-ideas`, `hand-drawn-draw-on` |

**ما تفعله:** يحوّل ملف JSON بصيغة kosif.audio-cues.v1 (بدايات الأصوات المقيسة والكلمات المحاذاة الناتجة عن audio_cue_mapper.py) إلى لوحة قصة قابلة للتحرير بصيغة motion_director، فيها نص موقوت ومسار يُرسم تدريجيًا وشخصية وتقريب للكاميرا، مع تقرير قرار يقيّم أساليب doodle وkinetic وcinematic.

**What it does:** Turns a kosif.audio-cues.v1 JSON (measured onsets plus aligned words from audio_cue_mapper.py) into an editable motion_director storyboard with timed text, a draw-on path, a character and a camera zoom, plus a decision report that scores the doodle, kinetic and cinematic styles.

#### متى تُستدعى

- «حوّل التعليق الصوتي وتوقيت الكلمات لستوري بورد موشن جرافيك»
- «اعمل لي مشاهد متزامنة مع الصوت من ملف cues.json»
- «أبغى لوحة قصة رأسية للريلز مبنية على توقيت كلماتي»
- «turn my audio cues and word timings into an editable motion storyboard»
- «pick a doodle, kinetic or cinematic style for this voiceover and build scenes»
- «generate a 9:16 scene plan synced to the narration»

#### الأوامر

- **plan (auto style)**: Validates the cues, scores the three styles with a declared heuristic, cuts the audio into scenes (target 6 s, inside a 2-9 s window) at pauses or word ends, and writes a new 1080x1920 30 fps storyboard JSON and a decision/evidence report. It prints a one-line JSON summary (rendered: false).
  - `python3 scripts/creative_reasoning_bridge.py ./cues.json --style auto --out ./out/scene.json --report ./out/decision.json`
- **plan (forced style, landscape)**: Uses the chosen style (doodle, kinetic or cinematic) and a 1920x1080 frame.
  - `python3 scripts/creative_reasoning_bridge.py ./cues.json --style kinetic --landscape --out ./out/scene.json --report ./out/decision.json`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: —
- الحدود: Builds an unrendered storyboard from a hand-written style heuristic and amplitude onsets; it does not understand lyrics or emotion, verify beats or render video.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_creative_intelligence.py`
- مرجع: `.claude/skills/kosif-superpowers/references/creative-intelligence-execution.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/motion.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/audio.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:creative-reasoning-bridge --evidence <ملف>`.

### `export-profile` — معيار التصدير: إعدادات التسليم المعتمدة لكل فيديو / Export profile: the owner-approved delivery settings for every video

| الحقل | القيمة |
|---|---|
| المسار | `scripts/export_profile.py` (جذر: skill) |
| المجال | `motion` |
| الدليل | `tested-here` |
| العائلات | `formats-platforms`, `engines-render-pipeline` |

**ما تفعله:** مصدر واحد لمعيار التصدير المعتمد: 1080×1920، 30 فريم، H.264 High بجودة CRF 17 وpreset slow، ألوان BT.709، الصوت الأصلي منسوخ بالبايت لما الـMP4 يقدر يشيله (وإلا AAC 320k)، MP4 مع faststart، ومن غير 4K إلا لو اتطلب. السكريبتات بتستورد video_args وaudio_args بدل ما تكتب إعداداتها.

**What it does:** One source for the delivery export standard the owner approved: 1080x1920, 30 fps, H.264 High CRF 17 preset slow, BT.709, the user's audio stream-copied byte for byte when MP4 can carry it (AAC 320k 48 kHz otherwise), MP4 +faststart, no 4K unless asked. Scripts import video_args(), audio_args(src) and FASTSTART instead of writing their own ffmpeg flags; running it prints the profile as JSON.

#### متى تُستدعى

- «صدّر الفيديو بنفس إعدادات داري يا قلبي»
- «What ffmpeg settings should a delivery MP4 use?»
- «عايز التصدير يبقى بأعلى جودة من غير 4K»

#### الأوامر

- **print**: Print the export profile as JSON.
  - `python3 scripts/export_profile.py`

#### المتطلبات والأمان

- binaries: ffprobe
- الأمان: read-only
- الموافقة: Reads only; writes nothing.
- الحدود: Sets encoder flags only; matching the colour grade to the source is a per-job measurement described in playbooks/export-standard.md.

#### الاختبارات والأدلة

- `tests/test_export_profile.py`
- مرجع: `playbooks/export-standard.md`
- مرجع: `playbooks/render-pipeline.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:export-profile --evidence <ملف>`.

### `infinite-matrices` — محرك المصفوفات اللانهائية للأساليب السببية / KOSIF Infinite Matrices causal style engine

| الحقل | القيمة |
|---|---|
| المسار | `.claude/skills/kosif-infinite-matrices/scripts/kmx.py` (جذر: repo) |
| المجال | `motion` |
| الدليل | `tested-here` |
| العائلات | `creativity-engine`, `particles-fluids-physics`, `light-glow-bloom`, `engines-render-pipeline` |

**ما تفعله:** يبني نظامًا بصريًا جديدًا من لبنات سببية (حالة، عملية، قانون، زمن، ذاكرة، تغذية راجعة) مستخرجة من أساليب الأطلس الـ86، ويثبت قانونه بمقارنة مضادة أ/ب/ج عبر بذور متعددة ومنحنى جرعة، ويرندر مشهدًا قابلًا للتقليب ولقطات وفيديو MP4 بأدوات الأطلس، ويحفظ النتائج والأفكار والتقييمات والمصادر في سجل متسلسل بالهاش.

**What it does:** Builds a new visual system from causal bricks (state, operation, law, time, memory, feedback) mined from the 86 atlas styles, proves its law with an A/B/C counterfactual over seeds and a dose sweep, renders a scrubbable scene, stills and MP4 with the atlas harness and sound kit, and saves verdicts, ideas, ratings and sources in a hash-chained ledger.

#### متى تُستدعى

- «اعمل أسلوب جديد بقانون سببي وقارن مع وبدون ذاكرة الضوء»
- «طوّر فكرة الزجاج اللي بيتذكر الضوء ورندرها فيديو»
- «Invent a new motion style from causal bricks and prove the effect with a counterfactual»
- «Which of the 86 atlas styles really use a field to steer motion?»
- «سجّل المصدر الجديد ده وابني على نتايج التجارب اللي فاتت»

#### الأوامر

- **doctor**: Reports python, node+Playwright, ffmpeg, the atlas assets, the 86-card index, the 283 hypothesis statuses, the ledger hash chain and the number of registered sources; exits 1 if the ledger chain is broken.
  - `python3 .claude/skills/kosif-infinite-matrices/scripts/kmx.py doctor`
- **recipe validate**: Checks schema, all six bricks, three parents in the order structure/dynamics/finish from three families, operators tagged on each parent in the 86-card index, overrides that point at real fields, and no shared code lineage between parents (REA fingerprints). Prints the recipe hash.
  - `python3 .claude/skills/kosif-infinite-matrices/scripts/kmx.py recipe validate .claude/skills/kosif-infinite-matrices/recipes/glass-remembers-light.json`
- **experiment**: Simulates every condition from identical inputs, replicates over the recipe's seeds, sweeps the coupling gain, and returns CONFIRMED_IN_MODEL only when all checks pass (exit 3 otherwise). Writes report.json, report.md and scene.html; --render adds JPEG stills and a pixel A/B/C difference; --mp4 renders 1280x720 video with the offline atlas score; --record appends to the ledger (refuses a recipe hash already recorded unless --replication).
  - `python3 .claude/skills/kosif-infinite-matrices/scripts/kmx.py experiment --recipe .claude/skills/kosif-infinite-matrices/recipes/glass-remembers-light.json --out out/kmx/glass --render --mp4`
- **scene**: Writes only the self-contained scene page (atlas contract: seek, DURATION, scoreSound, __ready, __kosif; views grid / one condition / storyboard).
  - `python3 .claude/skills/kosif-infinite-matrices/scripts/kmx.py scene --recipe .claude/skills/kosif-infinite-matrices/recipes/glass-remembers-light.json --out out/kmx/glass.html`
- **ledger**: stats: events by type, chain check, the 283 hypothesis statuses, experiments and Beta operator scores; list: one line per event; verify: hash-chain check (exit 1 when broken).
  - `python3 .claude/skills/kosif-infinite-matrices/scripts/kmx.py ledger stats`
- **rate**: Appends a human rating (0..5) for an experiment that exists in the ledger; ratings feed the operator scores used by ideate.
  - `python3 .claude/skills/kosif-infinite-matrices/scripts/kmx.py rate --experiment EXP-0001 --score 4 --by "reviewer"`
- **ideate**: Proposes parent/role triples from three families, skipping any signature already in the 283 seeds or the ledger and any pair of parents that share code (REA), ranked by ledger feedback; --record saves them as PROPOSED ideas.
  - `python3 .claude/skills/kosif-infinite-matrices/scripts/kmx.py ideate --count 10`
- **hypotheses**: stats / show ID / mark ID --status S --evidence FILE: the 283 seeds stay UNTESTED_UNRENDERED until marked with an evidence file whose sha256 is stored.
  - `python3 .claude/skills/kosif-infinite-matrices/scripts/kmx.py hypotheses stats`
- **sources**: list / verify --file F / add --file F --title T --relevance core\|method\|context\|not_relevant --rights R --used-for "a;b": the registry of every source by sha256; the same bytes under a new name become an alias.
  - `python3 .claude/skills/kosif-infinite-matrices/scripts/kmx.py sources list`
- **bricks**: summary or show ID from data/86_style_code_bricks.json: six bricks per style inferred from its code, REA function/call/relation counts and code-lineage neighbours.
  - `python3 .claude/skills/kosif-infinite-matrices/scripts/kmx.py bricks show flow-field`
- **laws**: list / run RECIPE [--render DIR] / verify REPORT / atoms [--axis A]: four typed causal laws from the owner's v0.2 causal studio (trajectory, material and elastic memory, self-imprinting), each an A/B run with one edge switched off plus a gain dose sweep; --render writes A/B SVG frames with a sha256 receipt; atoms lists the 197 conceptual mechanism atoms.
  - `python3 .claude/skills/kosif-infinite-matrices/scripts/kmx.py laws run .claude/skills/kosif-infinite-matrices/recipes/laws/self-imprinting.json`

#### المتطلبات والأمان

- binaries: python3
- optional: node, playwright, ffmpeg
- الأمان: writes-files
- الموافقة: --record, rate, ideate --record, hypotheses mark and sources add append to tracked files (memory/ledger.jsonl, sources/registry.json) that are meant to be committed as shared research memory; run them only for results the user wants kept.
- الحدود: v1 has one stimulus, one structure and one dynamics law (plus the four small v0.2 particle laws under `laws`); its causal claims hold inside the numerical model only, the 283 seeds are untested, code-brick labels are static inferences, and nothing is production-ready without a human rating.

#### الاختبارات والأدلة

- `.claude/skills/kosif-infinite-matrices/tests/test_kmx_engine.py`
- `.claude/skills/kosif-infinite-matrices/tests/test_infinite_matrices.py`
- مرجع: `.claude/skills/kosif-infinite-matrices/SKILL.md`
- مرجع: `.claude/skills/kosif-infinite-matrices/references/engine.md`
- مرجع: `.claude/skills/kosif-infinite-matrices/references/limits.md`
- مرجع: `.claude/skills/kosif-infinite-matrices/references/examples.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:infinite-matrices --evidence <ملف>`.

### `motion-director` — مُصرِّف حركة SVG المتزامنة مع الصوت / Audio-timed SVG motion compiler

| الحقل | القيمة |
|---|---|
| المسار | `scripts/motion_director.py` (جذر: skill) |
| المجال | `motion` |
| الدليل | `tested-here` |
| العائلات | `hand-drawn-draw-on`, `audio-sync-captions`, `engines-render-pipeline`, `shapes-morph-geometry` |

**ما تفعله:** يتحقق من ملف مشاهد بصيغة JSON مُوقَّت على مستوى الكلمات (مسارات ودوائر ونصوص وشخصيات وممثلون بمفاصل وتحوّلات أشكال وحركة كاميرا)، ثم يحوّله إلى رسم متحرك SVG/HTML مستقل يمكن الانتقال فيه إلى أي لحظة، مع تصيير اختياري إلى MP4 عبر render_html.cjs.

**What it does:** Validates a word-timed JSON scene spec (paths, circles, text, characters, rigged actors, morphs, camera) and compiles it into a self-contained seekable SVG/HTML animation, with an optional MP4 render through render_html.cjs.

#### متى تُستدعى

- «Compile this word-timed scene JSON into a seekable SVG explainer»
- «Render this compiled motion HTML to MP4 with my voice track»
- «اعمل لي موشن جرافيك عربي متزامن مع الكلمات من ملف JSON»
- «حوّل السكربت ده لأنيميشن رسم خطوط يتحرك مع الصوت»
- «ابي فيديو رسم بالكود مقاس ريلز ٩:١٦ مع التعليق الصوتي»

#### الأوامر

- **doctor**: Probes for the motion engine asset, render_html.cjs, node, ffmpeg and ffprobe; renders nothing.
  - `python3 scripts/motion_director.py doctor`
- **sample**: Writes a valid 9-second, 3-scene 1080x1920 Arabic demo spec (refuses an existing path).
  - `python3 scripts/motion_director.py sample --out ./scene.json`
- **compile**: Validates the spec and writes a new self-contained HTML/SVG animation exposing window.__kosif.seek(t); status html_compiled_not_rendered.
  - `python3 scripts/motion_director.py compile ./scene.json --out ./out/scene.html`
- **render**: Runs node render_html.cjs --mode seek --offline (Playwright Chromium + ffmpeg, 20-minute timeout) to write a new MP4, optionally muxing the user's audio; result is marked verified:false.
  - `python3 scripts/motion_director.py render ./out/scene.html --out ./out/scene.mp4 --audio ./voice.wav`

#### المتطلبات والأمان

- optional: bin:chromium, bin:ffmpeg, bin:ffprobe, bin:node, npm:playwright
- الأمان: runs-external-programs
- الموافقة: render launches node + headless Playwright Chromium + ffmpeg (timeout up to 20 min) and writes an MP4 muxed with the user's audio: confirm before rendering. sample/compile only create new files and never overwrite.
- الحدود: Compiles only its own validated vector primitives (≤80 elements, ≤120 s); it does not read words.json directly, transcribe or align audio, or verify the rendered MP4.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_motion_director.py`
- `.claude/skills/kosif-superpowers/evals/test_creative_intelligence.py`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/motion.md`
- مرجع: `.claude/skills/kosif-superpowers/references/executable-creative-motion.md`
- مرجع: `.claude/skills/kosif-superpowers/references/creative-intelligence-execution.md`
- مرجع: `.claude/skills/kosif-superpowers/references/code-drawing-master.md`
- مرجع: `.claude/skills/kosif-superpowers/references/capability-operating-manual.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:motion-director --evidence <ملف>`.

### `motion-engine-js` — محرك حركة SVG / SVG motion engine runtime

| الحقل | القيمة |
|---|---|
| المسار | `assets/motion_engine.js` (جذر: skill) |
| المجال | `motion` |
| الدليل | `tested-here` |
| العائلات | `hand-drawn-draw-on`, `characters-rigs`, `audio-sync-captions`, `shapes-morph-geometry` |

**ما تفعله:** سكربت يعمل في المتصفح يدمجه الأمر motion_director.py compile، يقرأ بيانات المشاهد بصيغة JSON من الوسم <script id=kosif-data> ويحرّك فيلم SVG بشكل حتمي: يرسم الخطوط تدريجيًا، ويُظهر النصوص بالتلاشي، ويحوّل المضلعات من شكل إلى آخر، ويحرّك شخصية خطية وممثلين بمفاصل محورية (مشي، جري، تلويح، إشارة، جلوس) مع رأس قلم متحرك، ويكبّر الكاميرا ويحرّكها لكل مشهد، ويعرض ترجمة عربية من اليمين إلى اليسار موقّتة بالكلمات، وكل ذلك عبر الدالة window.__kosif.seek(t) لرندر دقيق إطارًا بإطار.

**What it does:** A browser-side script (IIFE), inlined by motion_director.py compile, that reads scene JSON from <script id=kosif-data> and animates an SVG film deterministically: stroke draw-on, text fades, polygon morphs, a stick character, pivot-rigged actors (walk/run/wave/point/sit) with a moving pen tip, per-scene camera zoom/pan and word-timed RTL captions, all through window.__kosif.seek(t) for frame-exact rendering.

#### متى تُستدعى

- «ارسم لي مشهد سبورة بيضاء يتحرك بالقلم ومتزامن مع الكلام»
- «أبي شخصية مرسومة تمشي وتلوّح بعد ما تنرسم»
- «اعمل فيلم SVG فيه ترجمة عربية كلمة بكلمة على توقيت الصوت»
- «Animate my SVG scene with draw-on strokes, a walking character and word-timed captions»
- «Build a seekable whiteboard animation I can render to MP4»

#### الأوامر

- **embed**: Validates the scene spec, escapes it into <script id=kosif-data> and inlines this engine into a new self-contained HTML film. It refuses an existing output and needs the folder to exist. For a demo spec, run `python3 scripts/motion_director.py sample --out ./out/scene.json`.
  - `python3 scripts/motion_director.py compile ./scene.json --out ./out/film.html`
- **seek**: Draws the exact frame for time t (clamped to 0..duration) and returns the active scene id and caption word. render_html.cjs calls it for every frame in seek mode.
  - `window.__kosif.seek(2.5) // in the compiled page: draws t=2.5 s, returns {time, scene, word}`
- **check**: Syntax-checks the engine source, as documented in references/executable-creative-motion.md.
  - `node --check assets/motion_engine.js`

#### المتطلبات والأمان

- optional: bin:chromium, bin:ffmpeg, bin:ffprobe, bin:node, bin:python3, npm:playwright
- الأمان: writes-files
- الموافقة: —
- الحدود: Draws simple SVG strokes, polygon morphs and stick-figure rigs only and shows one caption word at a time. It needs a host page and a separate renderer (render_html.cjs) to become MP4, and it is not a general animation editor.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_motion_engine.mjs`
- `.claude/skills/kosif-superpowers/evals/test_code_drawing_engine.mjs`
- `.claude/skills/kosif-superpowers/evals/test_motion_director.py`
- مرجع: `.claude/skills/kosif-superpowers/references/executable-creative-motion.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/motion.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:motion-engine-js --evidence <ملف>`.

### `motion-kit-bridge` — جسر توقيتات Motion Starter Kit / Motion Starter Kit timing bridge

| الحقل | القيمة |
|---|---|
| المسار | `scripts/motion_kit_bridge.py` (جذر: skill) |
| المجال | `motion` |
| الدليل | `tested-here` |
| العائلات | `audio-sync-captions`, `hand-drawn-draw-on`, `app-feature-transfer` |

**ما تفعله:** يحوّل ملف توقيت الكلمات بصيغة motion-starter-kit (lines[].words[]) إلى لوحة قصة أصلية لـ KOSIF Motion Director بعد التحقق منها، مع معاينة HTML اختيارية يمكن الانتقال فيها إلى أي لحظة، بأنماط plotter وdoodle وwhiteboard وinfographic.

**What it does:** Converts motalim-ai/motion-starter-kit word-timing JSON (lines[].words[]) into a validated native KOSIF Motion Director storyboard, plus optional seekable HTML, for the plotter, doodle, whiteboard or infographic styles.

#### متى تُستدعى

- «Build a doodle storyboard from my motion-starter-kit words.json»
- «Convert these line/word timings into a seekable SVG preview»
- «حوّل ملف توقيت الكلمات من motion starter kit لموشن وايت بورد»
- «ابي ستوري بورد رسم يدوي من توقيتات الكلمات»
- «إيه الأساليب المدعومة من motion starter kit؟»

#### الأوامر

- **styles**: Lists the 10 upstream styles and which 4 are native_svg executable versus upstream_reference.
  - `python3 scripts/motion_kit_bridge.py styles`
- **demo**: Builds a storyboard (and optional HTML) from built-in synthetic Arabic timings; timing_provenance estimated_no_audio.
  - `python3 scripts/motion_kit_bridge.py demo --style doodle --out ./out/demo-story.json --html ./out/demo-story.html`
- **build**: Validates upstream timings (duration ≤120 s, 1–24 lines, 1–240 monotonic words per line, audio field present) and writes a Motion Director spec with one scene per line, plus optional seekable HTML.
  - `python3 scripts/motion_kit_bridge.py build --timings ./words.json --style plotter --out ./out/story.json --html ./out/story.html --fps 30`
- **build (estimated)**: Accepts timings with no audio field only when --allow-estimated is given.
  - `python3 scripts/motion_kit_bridge.py build --timings ./reading-estimates.json --allow-estimated --style whiteboard --out ./out/estimated-story.json`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: —
- الحدود: Executes only 4 of 10 upstream styles as native SVG approximations, does not render MP4, transcribe or align audio, and rejects KOSIF's flat words.json (top-level words[]).

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_motion_kit_bridge.py`
- مرجع: `.claude/skills/kosif-superpowers/references/motion-starter-kit-bridge.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/motion.md`
- مرجع: `.claude/skills/kosif-superpowers/references/repository-capability-transfer.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:motion-kit-bridge --evidence <ملف>`.

### `motion-physics` — فيزياء الحركة / Motion Physics

| الحقل | القيمة |
|---|---|
| المسار | `scripts/motion_physics.py` (جذر: skill) |
| المجال | `motion` |
| الدليل | `tested-here` |
| العائلات | `easing-timing-rhythm` |

**ما تفعله:** يحسب أرقام الحركة بدل تخمينها: نابض من الصلابة والتخميد والكتلة (القيمة في كل إطار ونسبة التخميد وزمن الاستقرار والتجاوز، أو إطارات CSS)، وأي منحنى cubic-bezier أو تسهيل CSS مسمى بنفس حساب المتصفح، وتأخيرات التتابع من نقطة أصل (الأول أو الأخير أو المنتصف أو الأطراف أو عنصر بعينه) في صف أو شبكة، وعينات خط مفاتيح لكل إطار بتسهيل. مكتبة بايثون القياسية فقط؛ يطبع JSON أو CSS ولا يكتب ملفات.

**What it does:** Computes motion numbers instead of guessing them: a spring from stiffness, damping and mass (value per frame, damping ratio, settle time, overshoot, or CSS @keyframes), any CSS cubic-bezier or named easing sampled exactly as a browser does, stagger delays from an origin (first, last, center, edges or an index) on a row or a grid, and a keyframe track sampled per frame with an easing. Pure standard library; prints JSON or CSS and writes no files.

#### متى تُستدعى

- «عايز ارتداد نابض طبيعي للعنوان، اطلعلي القيم لكل فريم»
- «حوّل cubic-bezier ده لقيم لكل فريم»
- «give me stagger delays from the center of a 4x3 grid»
- «spring keyframes with stiffness 180 and damping 12 as CSS»

#### الأوامر

- **spring**: Values per frame, damping ratio, regime, settle time and overshoot; --css NAME prints @keyframes
  - `python3 scripts/motion_physics.py spring --from 0 --to 1 --stiffness 170 --damping 26 --fps 30`
- **bezier**: A CSS cubic-bezier sampled at --frames + 1 evenly spaced points
  - `python3 scripts/motion_physics.py bezier 0.25 0.1 0.25 1 --frames 30`
- **stagger**: Delay in seconds for each element from an origin on a row or a grid
  - `python3 scripts/motion_physics.py stagger --count 12 --each 0.06 --from center --grid 4x3 --ease out`
- **keyframes**: A time:value track sampled per frame with an easing
  - `python3 scripts/motion_physics.py keyframes --track 0:0,0.5:120,1.2:100 --ease out --fps 30`
- **--self-test**: Checks spring regimes, the CSS 'ease' value at 0.5, stagger origins and track sampling
  - `python3 scripts/motion_physics.py --self-test`

#### المتطلبات والأمان

- binaries: python3
- الأمان: read-only
- الموافقة: —
- الحدود: The spring is integrated numerically (16 sub-steps per frame), so values match an analytic spring to about 1e-3, not exactly; one dimension at a time; settle uses a 0.1 % rest threshold; easing names cover the CSS keywords plus a few common curves, not every library's presets.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_motion_physics.py`
- مرجع: `.claude/skills/kosif-superpowers/references/powers/easing-timing-rhythm.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/motion.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:motion-physics --evidence <ملف>`.

### `motion-runtime` — إنشاء فيلم سبورة مرسوم وتصييره / Doodle film runtime and renderer

| الحقل | القيمة |
|---|---|
| المسار | `scripts/motion_runtime.py` (جذر: skill) |
| المجال | `motion` |
| الدليل | `tested-here` |
| العائلات | `hand-drawn-draw-on`, `engines-render-pipeline`, `typography-arabic` |

**ما تفعله:** ينشئ فيلم رسم يدوي عربي على سبورة بيضاء بصيغة SVG قابلًا للتعديل (film.html وmotion.json وREADME) مع آلية انتقال زمني حتمية، ويعرض 25 بطاقة توجيه لمحركات الحركة، ولا يصيّره إلى صورة معاينة PNG أو فيديو MP4 بمقاس 1080x1920 عبر render_html.cjs إلا عند تمرير ‎--run صراحةً.

**What it does:** Scaffolds an editable Arabic whiteboard-doodle SVG film (film.html + motion.json + README) with a deterministic seek contract, lists 25 motion-engine route cards, and only with explicit --run renders it to a 1080x1920 PNG preview or MP4 through render_html.cjs.

#### متى تُستدعى

- «Make me an editable whiteboard doodle film I can render to MP4»
- «Render a preview PNG of this film.html at 1080x1920»
- «اعمل فيلم رسم يدوي عربي على سبورة بيضاء بالكود»
- «ابي معاينة صورة للفيلم قبل الرندر النهائي»
- «Which motion engines fit a whiteboard explainer?»

#### الأوامر

- **doctor**: Probes python3/node/ffmpeg/ffprobe on PATH, the template and the renderer; all *_verified flags stay false.
  - `python3 scripts/motion_runtime.py doctor`
- **engines**: Prints route cards from data/motion_engines.json (families: 2d, 3d, character, creative, effects, explain, export, timeline, vector, whiteboard); knowledge only.
  - `python3 scripts/motion_runtime.py engines --family whiteboard`
- **scaffold**: Creates a new project folder with film.html, motion.json and README.md from the doodle-film template.
  - `python3 scripts/motion_runtime.py scaffold --out ./out/film --title "قصيف يرسم" --subtitle "الحركة تُولد بالكود" --duration 8 --fps 30`
- **render (dry)**: Without --run returns status approval_required and executes nothing.
  - `python3 scripts/motion_runtime.py render --in ./out/film/film.html --out ./out/film/film.mp4`
- **render (preview PNG)**: A .png output path makes the tool pass --preview to render_html.cjs and write one preview image (there is no --preview flag on this CLI).
  - `python3 scripts/motion_runtime.py render --in ./out/film/film.html --out ./out/film/preview.png --run`
- **render**: Runs node render_html.cjs --offline --mode seek at 1080x1920 to a new MP4; --audio is allowed only with MP4.
  - `python3 scripts/motion_runtime.py render --in ./out/film/film.html --out ./out/film/film.mp4 --fps 30 --audio ./voice.wav --run`

#### المتطلبات والأمان

- optional: bin:chromium, bin:ffmpeg, bin:ffprobe, bin:node, npm:playwright
- الأمان: runs-external-programs
- الموافقة: render --run launches node + headless Playwright Chromium + ffmpeg (240 s timeout) and writes a new PNG/MP4 with the user's audio muxed; without --run it only returns approval_required.
- الحدود: The template is a fixed 8-second 1080x1920 whiteboard doodle performance (longer durations need hand-extended keyframes), and the render is not self-verified.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_motion_runtime.py`
- مرجع: `.claude/skills/kosif-superpowers/references/motion-runtime.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/motion.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:motion-runtime --evidence <ملف>`.

### `motion-stack` — مولّد مشاريع بداية لمحركات الحركة / Third-party motion engine scaffolder

| الحقل | القيمة |
|---|---|
| المسار | `scripts/motion_stack.py` (جذر: skill) |
| المجال | `motion` |
| الدليل | `tested-here` |
| العائلات | `engines-render-pipeline`, `code-engineering`, `3d-spatial` |

**ما تفعله:** يعرض 25 تقنية حركة مسجّلة في الكتالوج، وينشئ مشاريع بداية أصلية دون تثبيت لكل من GSAP (مع Rough.js وVivus) وRemotion وManim وThree.js وPixiJS وp5.js، وتتيح مشاريع GSAP وThree.js وPixiJS وp5 الانتقال إلى أي لحظة عبر window.__kosif.

**What it does:** Lists 25 catalogued motion technologies and writes original, uninstalled starter projects for GSAP (+Rough.js/Vivus), Remotion, Manim, Three.js, PixiJS or p5.js; the GSAP, Three.js, PixiJS and p5 starters expose a seekable window.__kosif contract.

#### متى تُستدعى

- «Scaffold a Remotion project for a 9:16 explainer»
- «Give me a GSAP timeline starter with a hand-drawn stroke reveal»
- «عايز مشروع بداية Three.js أو p5 للموشن»
- «أعطني هيكل مشروع Manim لشرح فكرة بالرسوم»
- «وش محركات الأنيميشن اللي تقدر تشتغل عليها؟»

#### الأوامر

- **list**: Validates data/motion_sources.json and prints the 25 motion sources (name, repo, role, npm, license hint); runtime_status not_probed.
  - `python3 scripts/motion_stack.py list`
- **doctor**: Reports whether node, npm, ffmpeg, ffprobe and the manim CLI are on PATH (presence only, nothing run).
  - `python3 scripts/motion_stack.py doctor`
- **scaffold**: Creates a new folder with package.json/index.html/src files (or main.py for manim) for backend gsap\|remotion\|manim\|three\|pixi\|p5; nothing is installed or run.
  - `python3 scripts/motion_stack.py scaffold gsap --out ./out/kosif-gsap`

#### المتطلبات والأمان

- optional: npm:@remotion/cli, npm:gsap, npm:p5, npm:pixi.js, npm:react, npm:react-dom, npm:remotion, npm:roughjs, npm:three, npm:vite, npm:vivus, pip:manim
- الأمان: writes-files
- الموافقة: Installing the scaffold's dependencies (npm install for gsap/roughjs/vivus/vite/remotion/react/three/pixi.js/p5, pip install manim) and accepting Remotion's company license are separate steps that need user approval; the tool itself only writes a new folder.
- الحدود: Writes starter source only; it does not install packages, check that any engine runs, or render a video.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_motion_stack.py`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/motion.md`
- مرجع: `.claude/skills/kosif-superpowers/references/executable-creative-motion.md`
- مرجع: `.claude/skills/kosif-superpowers/references/capability-operating-manual.md`
- مرجع: `.claude/skills/kosif-superpowers/references/repository-capability-transfer.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:motion-stack --evidence <ملف>`.

### `motion-toolkit` — مكتبة رياضيات الحركة / Motion math toolkit

| الحقل | القيمة |
|---|---|
| المسار | `resources/motion-runtime/motion_toolkit.mjs` (جذر: skill) |
| المجال | `motion` |
| الدليل | `tested-here` |
| العائلات | `easing-timing-rhythm`, `camera-composition-layout`, `hand-drawn-draw-on`, `characters-rigs` |

**ما تفعله:** وحدة ES بلا اعتماديات تصدّر 12 دالة حركة حتمية يمكن الانتقال بها إلى أي لحظة: حصر القيم ضمن مدى، ومنحنيات التسهيل، والاستيفاء بين الإطارات المفتاحية وخطوط الزمن، وكشف خطوط SVG تدريجيًا، وتحريك الكاميرا وتكبيرها، وزوايا مفاصل دورة المشي، واختلاف المنظر (البارالاكس)، واهتزاز الخط اليدوي ببذرة ثابتة، والرمز الزمني بصيغة HH:MM:SS:FF، وحالة الترجمة على مستوى الكلمة الكاملة، والتحقق من عقد الإطارات قبل الرندر.

**What it does:** A dependency-free ES module that exports 12 deterministic, seekable animation primitives: clamp, easing, keyframe interpolation and timelines, SVG stroke reveal, camera pan/zoom, walk-cycle joint angles, parallax, seeded hand-drawn line jitter, HH:MM:SS:FF timecode, whole-word caption cue state and a render frame-contract check.

#### متى تُستدعى

- «أبي دوال جاهزة للـ easing والكي فريم في الأنيميشن بتاعي»
- «اعمل لي خط مرسوم باليد بشكل ثابت يتكرر بنفس الشكل»
- «احسب لي عدد الإطارات والتايم كود لفيديو 8 ثواني 30 فريم»
- «Give me deterministic easing/keyframe helpers for a seekable SVG animation»
- «I need walk-cycle and camera zoom math for my HTML film»

#### الأوامر

- **import**: Loads the module from the skill root and prints '0.5 00:00:02:15'. All 12 names (clamp, ease, interpolate, timeline, strokeReveal, camera, walkRig, parallax, seededSketchLine, timeCode, wordCueState, assertFrameContract) can be imported the same way in Node.js or an ES-module browser page; no npm packages are needed.
  - `node --input-type=module -e "import {ease, timeCode} from './resources/motion-runtime/motion_toolkit.mjs'; console.log(ease(0.5,'cubic'), timeCode(2.5,30))"`
- **ease**: Clamps u to 0..1 and applies the named easing curve (default smooth). Throws on an unknown kind.
  - `ease(0.5, "cubic") // 0.5; kinds: linear \| smooth \| in \| out \| cubic`
- **interpolate**: Eases from `from` to `to` between times a and b. Throws if b<=a or any value is non-finite.
  - `interpolate(2, 1, 3, 4, 8) // 6`
- **timeline**: A multi-keyframe track with held endpoints. Keyframe times must strictly increase.
  - `timeline(2, [{time:0,value:0},{time:1,value:10},{time:3,value:20}]) // 15`
- **strokeReveal**: Returns dasharray/dashoffset values that draw an SVG path of the given length like a pen between start and end.
  - `strokeReveal(0.5, 0, 1, 300) // {strokeDasharray:300, strokeDashoffset:150}`
- **camera**: Returns {zoom, x, y} for an eased zoom about the centre plus a pan.
  - `camera(4, {end:8, zoomEnd:1.1, panX:20, centerX:540, centerY:960}) // {zoom:1.05, x:-17, y:-48}`
- **walkRig**: Returns leg and arm angles in degrees plus an `active` value that eases in over 0.5 s after onset.
  - `walkRig(4, {onset:3.3, frequency:6, stride:14, armSwing:12})`
- **parallax**: Scales the camera offset by a layer depth from 0 to 1.
  - `parallax(10, 20, 0.5) // {x:5, y:10}`
- **seededSketchLine**: Returns steps+1 jittered points that look hand-drawn. The jitter fades to zero at both ends, so the endpoints stay on the line within floating-point error, and the same seed always gives the same line.
  - `seededSketchLine(0, 0, 100, 0, {seed:7, roughness:1.5, steps:20})`
- **timeCode**: Formats seconds as HH:MM:SS:FF (non-drop-frame) at an integer fps from 1 to 240.
  - `timeCode(2.5, 30) // "00:00:02:15"`
- **wordCueState**: Returns per-word active/progress state for caption timing without splitting Arabic words.
  - `wordCueState(0.5, [{word:"قصيف", start:0, end:1}]) // [{word, active:true, progress:0.5}]`
- **assertFrameContract**: Checks the duration (0–3600 s), the integer fps (1–120) and an even width/height of at least 64 px before rendering, and returns the total frame count.
  - `assertFrameContract(8, 30, 1080, 1920) // {..., totalFrames:240, aspect:0.5625}`
- **clamp**: Clamps a number into [min, max], 0..1 by default.
  - `clamp(2) // 1`

#### المتطلبات والأمان

- binaries: node
- الأمان: read-only
- الموافقة: —
- الحدود: Supplies math primitives only: it draws, renders and edits nothing, and has just five easing curves and a single sine-based walk cycle.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_motion_toolkit.mjs`
- مرجع: `.claude/skills/kosif-superpowers/references/motion-runtime.md`
- مرجع: `.claude/skills/kosif-superpowers/references/executable-creative-motion.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/motion.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:motion-toolkit --evidence <ملف>`.

### `particles` — جسيمات قابلة للقفز: انفجار بصيغة مغلقة وفحص الميزانية وإطار SVG / Seekable particles: closed-form bursts, budget check and SVG frame

| الحقل | القيمة |
|---|---|
| المسار | `scripts/particles.py` (جذر: skill) |
| المجال | `motion` |
| الدليل | `tested-here` |
| العائلات | `particles-fluids-physics` |

**ما تفعله:** يحسب موقع وشفافية كل جسيم في انفجار ببذرة عند أي زمن t بصيغة مغلقة للسحب والجاذبية ومولد عشوائي بالهاش بلا حالة (فيطابق كل إطار في أي ترتيب رندر)، ويفحص مواصفة الجسيمات مقابل قواعد الميزانية، ويرسم إطارًا واحدًا SVG للمراجعة.

**What it does:** Computes every particle of a seeded burst at any time t from a closed-form drag+gravity solution and a stateless lowbias32 hash RNG (so frames render identically in any order), checks a particle spec against the family's budget rules (sizes, colours, per-engine counts, burst size, seeding, layering), and writes one frame as SVG for visual review.

#### متى تُستدعى

- «اعمل انفجار جسيمات ثابت في كل رندر»
- «هل عدد الجسيمات ده كتير على Canvas؟»
- «Make a deterministic particle burst I can seek to any frame»
- «Check my particle budget before rendering»

#### الأوامر

- **burst**: Position, opacity, size and colour of every particle at time t.
  - `python3 scripts/particles.py burst --seed 7 --count 40 --t 0.5 --visible-only`
- **budget**: Budget violations and warnings with the source power card of each rule.
  - `echo '{"engine":"canvas2d","kind":"ambient","count":900,"sizes":[4,8,14],"colors":["#fff","#fc0"],"seeded":true,"behind_text":true}' \| python3 scripts/particles.py budget -`
- **svg**: One frame as SVG on stdout (or --out FILE).
  - `python3 scripts/particles.py svg --seed 7 --count 160 --t 0.4`
- **self-test**: Offline self-check.
  - `python3 scripts/particles.py --self-test`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: Writes only the --out SVG path the user passes; otherwise stdout.
- الحدود: Radial bursts with linear drag and constant gravity only (no collisions, fluids or forces between particles); the SVG/DOM count limit of 300 is a tool heuristic, the Canvas/WebGL limits come from PART-04.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_particles.py`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:particles --evidence <ملف>`.

### `render-html` — محوّل HTML إلى فيديو MP4 / HTML to MP4 renderer

| الحقل | القيمة |
|---|---|
| المسار | `resources/motion-runtime/render_html.cjs` (جذر: skill) |
| المجال | `motion` |
| الدليل | `tested-elsewhere` |
| العائلات | `engines-render-pipeline`, `qa-verification`, `formats-platforms` |

**ما تفعله:** نسخة مضمّنة في المهارة من عارض KOSIF الحتمي لتحويل HTML إلى MP4: يلتقط فيلم HTML محليًا أو عبر رابط http إطارًا بإطار في Chromium بلا واجهة (عبر window.__kosif.seek(t) أو الزمن الافتراضي في Chromium)، ويرمّزه بصيغة H.264 عبر ffmpeg، ويدمج الصوت اختياريًا دون تعديله، ثم يتحقق بـ ffprobe من معدل الإطارات وعددها والمدة والأبعاد والصوت، أو يصنع بالخيار ‎--preview لوحة معاينة من 8 إطارات بدل الفيديو.

**What it does:** The skill's bundled copy of KOSIF's deterministic HTML-to-MP4 renderer: it captures a local or http HTML film frame by frame in headless Chromium (through window.__kosif.seek(t) or Chromium virtual time), encodes H.264 with ffmpeg, optionally muxes untouched audio and checks fps, frames, duration, size and audio with ffprobe, or with --preview makes an 8-frame contact sheet instead.

#### متى تُستدعى

- «حوّل ملف film.html لفيديو MP4 مع التعليق الصوتي»
- «اعمل لي معاينة سريعة للأنيميشن قبل الرندر النهائي»
- «أبي أصدّر الموشن جرافيك بمقاس ريلز 9:16»
- «Render this HTML animation to a 1080x1920 MP4 at 30 fps with my voiceover»
- «Make a contact-sheet preview of my HTML film before the final render»

#### الأوامر

- **render**: Renders every frame (seek mode if window.__kosif exists, otherwise it relaunches in virtual mode), encodes libx264 CRF 18 yuv420p, muxes the audio as AAC 192k padded to the video length, then prints a 'VERIFY OK\|FAIL' line from ffprobe. Exits 3 on a mismatch.
  - `node resources/motion-runtime/render_html.cjs --in ./film.html --out ./out/film.mp4 --fps 30 --audio ./voice.wav`
- **preview**: Captures 8 evenly spaced frames and tiles them into a 4x2 contact sheet at ./out/film_preview.png. It always appends '_preview.png' to the --out stem. Tiles are labelled when ffmpeg has drawtext. Audio is ignored.
  - `node resources/motion-runtime/render_html.cjs --in ./film.html --out ./out/film.mp4 --preview`
- **virtual**: Renders any CSS/WAAPI/rAF/GSAP page under the paused Chromium virtual clock in exact 1000/fps steps. --offline aborts every http(s) request and --seed replaces Math.random with a seeded PRNG, for reproducible output.
  - `node resources/motion-runtime/render_html.cjs --in ./page.html --out ./out/clip.mp4 --mode virtual --duration 6 --aspect 16:9 --offline --seed 7`
- **help**: Prints every option (--aspect, --width, --height, --fps, --duration, --start, --audio, --mode, --preview, --frames-dir, --keep-frames, --crf, --scale, --seed, --offline, --timeout, --settle) and the exit codes.
  - `node resources/motion-runtime/render_html.cjs --help`

#### المتطلبات والأمان

- binaries: chromium, ffmpeg, ffprobe, node
- network: true
- node: playwright
- الأمان: network
- الموافقة: An http(s) --in URL, or a page that loads remote assets, contacts the network (use --offline to block it). It runs the page's own scripts in headless Chromium, so render only pages the user trusts. It overwrites --out, and --frames-dir deletes existing frame_######.png, preview_raw_NN.png and preview_tile_NN.png files in that folder.
- الحدود: Verifies only container metrics (fps, frame count, duration, size, audio presence), not visual or creative correctness, and it installs nothing, so Playwright Chromium and ffmpeg/ffprobe must already be present.

#### الاختبارات والأدلة

- لا اختبار مسجل: الشارة لا تتجاوز 📄 حتى يُختبر هنا.
- مرجع: `.claude/skills/kosif-superpowers/references/motion-runtime.md`
- مرجع: `.claude/skills/kosif-superpowers/references/executable-creative-motion.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/motion.md`
- مرجع: `tools/render_html.md`
- مرجع: `playbooks/render-pipeline.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:render-html --evidence <ملف>`.

### `repo-aspects` — محلّل نسب العرض المرن / Flexible aspect ratio resolver

| الحقل | القيمة |
|---|---|
| المسار | `tools/aspects.py` (جذر: repo) |
| المجال | `motion` |
| الدليل | `tested-here` |
| العائلات | `formats-platforms` |

**ما تفعله:** وحدة بايثون لا تعتمد إلا على المكتبة القياسية، تستخدمها kosif.py وverify_video.py وimport_briefs.py، وتحوّل أي صيغة لنسبة العرض إلى تسمية وأبعاد زوجية بالبكسل. تقبل نسبة W:H أو أبعادًا بصيغة WxH أو اسم منصة أو شكل بالإنجليزية أو العربية مثل reel وcinema ومربع، وتوفّر دوال لحساب النسبة العددية وإرجاع نص الأبعاد WxH والتحقق من صلاحية الصيغة.

**What it does:** A standard-library-only Python module, shared by kosif.py, verify_video.py and import_briefs.py, that turns any aspect spec (a W:H ratio, WxH pixels or an English or Arabic platform name such as reel, cinema or مربع) into a label and an even pixel size, with helpers for the numeric ratio, a 'WxH' string and validity.

#### متى تُستدعى

- «كم أبعاد فيديو سينمائي 2.35:1 بالبكسل؟»
- «حوّل ريلز أو مربع إلى عرض وارتفاع»
- «what pixel size should a 21:9 render use?»
- «check whether '1920x816' is a valid aspect spec»
- «resolve 'cinema' to width and height in Python»

#### الأوامر

- **resolve**: Returns (label, width, height) with even dimensions; here ('2.35:1', 1920, 818). Raises ValueError for unreadable specs.
  - `python3 -c "import sys; sys.path.insert(0,'tools'); from aspects import resolve; print(resolve('2.35:1'))"`
- **ratio_of**: Returns width/height as a float for any accepted spec (cinema gives 2.388…).
  - `python3 -c "import sys; sys.path.insert(0,'tools'); from aspects import ratio_of; print(ratio_of('cinema'))"`
- **resolution**: Returns a 'WxH' string (ريلز gives 1080x1920).
  - `python3 -c "import sys; sys.path.insert(0,'tools'); from aspects import resolution; print(resolution('ريلز'))"`
- **is_valid**: Returns True or False instead of raising (prints False True).
  - `python3 -c "import sys; sys.path.insert(0,'tools'); from aspects import is_valid; print(is_valid('10:1'), is_valid('1920x816'))"`
- **import**: Shows the four classic pixel presets and the 35 English and Arabic platform and shape names.
  - `python3 -c "import sys; sys.path.insert(0,'tools'); from aspects import PRESETS, NAMES; print(PRESETS); print(sorted(NAMES))"`

#### المتطلبات والأمان

- binaries: python3
- الأمان: read-only
- الموافقة: —
- الحدود: It only maps aspect specs to even pixel sizes; it does not resize, crop or reframe media, and it has no CLI.

#### الاختبارات والأدلة

- `tests/test_aspects.py`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/motion.md`
- مرجع: `.claude/skills/kosif-superpowers/references/executable-creative-motion.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:repo-aspects --evidence <ملف>`.

### `repo-check-frame-cover` — فحص تغطية الصورة للإطار / Photo frame-cover check

| الحقل | القيمة |
|---|---|
| المسار | `tools/check_frame_cover.cjs` (جذر: repo) |
| المجال | `motion` |
| الدليل | `tested-here` |
| العائلات | `qa-verification`, `engines-render-pipeline` |

**ما تفعله:** يرندر فريمات عينة من فيلم صور HTML لكل ستايل (مثل ?style=1..5) ويفشل لو أي فريم ظهرت فيه حافة فاضية. بيسجّل كل رسم صورة بالتحويل والشفافية والبلور ويتأكد إن صورة معتمة بتغطي أركان الإطار الأربعة، فالصور الغامقة أو الأبيض والأسود ما بتعملش إنذار كاذب، وفجوة بكسل واحد بتفشل. يُستخدم مع tools/photo_cover.js، الكاميرا المشتركة اللي بتخلي الصورة مغطية الإطار في كل زوم وبان واهتزاز ودوران وبلور لأي مقاس صورة.

**What it does:** Renders sample frames of an HTML photo film (window.__kosif.seek) for every variant such as ?style=1..5 and fails when any frame shows an empty edge. It records every drawImage with its transform, alpha, blend mode and blur and checks that an opaque photo covers all four canvas corners, so dark or black-and-white photos never raise false alarms and a one-pixel gap still fails. Pair it with tools/photo_cover.js, the shared camera that keeps a photo covering the frame through zoom, pan, shake, rotation and blur for any photo aspect ratio.

#### متى تُستدعى

- «The photo doesn't fill the top of the frame in some styles»
- «Check that no empty edge shows in any of the five lyric video styles»
- «الصورة مش مالية الفريم من فوق في بعض الستايلات»
- «افحص إن الصورة مغطية الشاشة كلها في كل حركات الكاميرا»

#### الأوامر

- **check styles**: Renders 24 evenly spaced frames per variant and prints ok/FAIL per variant; exit 0 when every frame is covered, 3 when any frame shows an empty edge.
  - `node tools/check_frame_cover.cjs --in tests/fixtures/photo-cover/index.html --variants "style=1;style=2;style=3;style=4;style=5" --samples 24`
- **check exact times with evidence**: Checks the given times, saves a PNG of each failing frame and writes a JSON report with the uncovered photo quads.
  - `node tools/check_frame_cover.cjs --in projects/egypt-saudi-salute/index.html --times 0,26.46,66.16 --frames-dir ./out/gaps --json ./out/cover.json`

#### المتطلبات والأمان

- binaries: chromium, node
- node: playwright
- الأمان: runs-external-programs
- الموافقة: —
- الحدود: Checks canvas drawImage geometry only: photos drawn as DOM/CSS images or through WebGL are not measured, and a photo composited through an offscreen canvas counts only when that canvas itself received a covering opaque photo.

#### الاختبارات والأدلة

- `tests/test_photo_cover.mjs`
- مرجع: `playbooks/render-pipeline.md`
- مرجع: `starters/html-canvas/README.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:repo-check-frame-cover --evidence <ملف>`.

### `repo-job-wait` — تشغيل المهام الطويلة في الخلفية وانتظارها بلا sleep / Background job runner and waiter (no sleep waits)

| الحقل | القيمة |
|---|---|
| المسار | `tools/job.py` (جذر: repo) |
| المجال | `motion` |
| الدليل | `tested-here` |
| العائلات | `qa-verification`, `engines-render-pipeline` |

**ما تفعله:** يشغّل رندر أو ترميز أو تحميل أو تثبيت طويل في الخلفية (اللوج ورقم العملية وكود الخروج في مجلد المهمة) وينتظره بدون `sleep N; check` الذي يمنعه Claude Code: الأمر `wait` يطبع سطر تقدّم كل فترة (فريم كذا من كذا، أو frame= من ffmpeg، أو نسبة مئوية) ثم DONE أو FAILED مع آخر سطور اللوج، ويخرج بكود المهمة، ليعمل داخل أداة Monitor أو مع run_in_background؛ و`status` نظرة بلا انتظار، و`stop` يوقفها.

**What it does:** Starts a long render, encode, download or install detached (log, pid and exit code in a job folder) and waits on it without `sleep N; check`, which Claude Code blocks: `wait` prints a throttled PROGRESS line (render_html.cjs `frame i/n`, ffmpeg `frame=`, percentages) then DONE or FAILED with the log tail and exits with the job's code, for the Monitor tool or Bash run_in_background; `status` peeks without waiting; `stop` ends it.

#### متى تُستدعى

- «Render the full video in the background and tell me the progress»
- «Wait for the ffmpeg encode to finish without sleep»
- «رندر الفيديو كامل في الخلفية وقولي وصل لفين»
- «استنى التحميل لحد ما يخلص من غير sleep»

#### الأوامر

- **start**: Launches the command detached, writes job.log/job.pid/job.exit into --dir and returns at once.
  - `python3 tools/job.py start --dir out/20261024-film/render -- node tools/render_html.cjs --in film.html --out out/film.mp4`
- **wait**: Blocks until the job ends: a PROGRESS line at most every 20 s (--every), WARN on new error lines, then DONE exit=0 or FAILED exit=N with the last 5 log lines; --quiet prints only the final line; --timeout N exits 124. Run it under the Monitor tool or Bash run_in_background.
  - `python3 tools/job.py wait --dir out/20261024-film/render`
- **status**: Prints RUNNING with the last progress line, DONE or FAILED, and returns immediately.
  - `python3 tools/job.py status --dir out/20261024-film/render`
- **stop**: Sends SIGTERM to the job's process group.
  - `python3 tools/job.py stop --dir out/20261024-film/render`

#### المتطلبات والأمان

- الأمان: runs-external-programs
- الموافقة: —
- الحدود: Progress is parsed from the job's own log lines, so a command that prints nothing shows no PROGRESS until it ends; POSIX only (process groups, /proc for zombie detection).

#### الاختبارات والأدلة

- `tests/test_job_wait.py`
- مرجع: `playbooks/render-pipeline.md`
- مرجع: `CLAUDE.md`
- مرجع: `AGENTS.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:repo-job-wait --evidence <ملف>`.

### `repo-render-html` — محوّل حتمي من HTML إلى فيديو MP4 / Deterministic HTML-to-MP4 renderer

| الحقل | القيمة |
|---|---|
| المسار | `tools/render_html.cjs` (جذر: repo) |
| المجال | `motion` |
| الدليل | `tested-elsewhere` |
| العائلات | `engines-render-pipeline`, `qa-verification`, `formats-platforms` |

**ما تفعله:** يحوّل فيلم HTML محليًا أو عبر رابط http إلى فيديو إطارًا بإطار داخل متصفح Chromium بلا واجهة (Playwright)، إما بالدالة window.__kosif.seek(t) في الصفحة، وإما بإيقاف الزمن الافتراضي للمتصفح وتقديمه خطوة خطوة لأي صفحة تعتمد CSS أو WAAPI أو requestAnimationFrame أو GSAP. ثم يرمّز الإطارات بصيغة H.264 ‏yuv420p عبر ffmpeg، ويدمج الصوت المرفق بعد ترميزه AAC بمعدل 192k دون إعادة أخذ العينات أو تغيير توقيته، ويتحقق عبر ffprobe من معدل الإطارات وعددها والمدة والأبعاد ووجود الصوت. ومع ‎--preview يُخرج لوحة PNG من ثمانية إطارات بدلًا من الفيديو.

**What it does:** Renders a local or http HTML film frame by frame in headless Chromium (Playwright), driving the page through window.__kosif.seek(t) or, for any CSS/WAAPI/rAF/GSAP page, through paused Chromium virtual time. It encodes H.264 yuv420p with ffmpeg, can mux a supplied audio track re-encoded as AAC 192k without resampling or retiming it, and checks fps, frame count, duration, size and audio presence with ffprobe. With --preview it writes an 8-frame contact-sheet PNG instead of a video.

#### متى تُستدعى

- «حوّل صفحة الأنيميشن HTML لفيديو MP4 مع الصوت الأصلي»
- «اعمل لي معاينة إطارات قبل الرندر النهائي»
- «رندر الستارتر html-canvas بمقاس ريلز 9:16 و30 فريم»
- «render this GSAP/CSS animation page to a 30 fps MP4»
- «make a contact-sheet preview of my HTML film before the final render»
- «render only seconds 4 to 7 at half size for a motion check»

#### الأوامر

- **render**: Full render: seek mode when window.__kosif exists, otherwise it relaunches in virtual mode. Muxes the audio as AAC 192k (apad + -shortest, no retiming) and prints an ffprobe 'VERIFY OK/FAIL' line; exit 3 means the output disagrees with the request.
  - `node tools/render_html.cjs --in starters/html-canvas/index.html --out ./out/film.mp4 --fps 30 --audio ./voice.mp3`
- **preview**: Captures 8 evenly spaced frames into a 4x2 contact sheet written as <out-basename>_preview.png next to --out (here ./out/film_preview.png). No video is produced and --audio is ignored.
  - `node tools/render_html.cjs --in starters/html-canvas/index.html --out ./out/film.mp4 --preview`
- **virtual**: Forces the virtual-time driver for a page without a seek hook; here --aspect sets 1920x1080, --offline aborts every http(s) request and --seed replaces Math.random with a seeded PRNG for a reproducible render.
  - `node tools/render_html.cjs --in ./page.html --out ./out/clip.mp4 --mode virtual --duration 6 --aspect 16:9 --offline --seed 7`
- **segment**: Renders only part of the film (from film time --start for --duration seconds) at a custom viewport size, as a quick motion check.
  - `node tools/render_html.cjs --in starters/html-canvas/index.html --out ./out/check.mp4 --start 4 --duration 3 --width 540 --height 960`
- **frames-dir**: Writes and keeps the PNG frames (frame_000000.png …) in the given folder after deleting older frame_NNNNNN.png and preview_raw/tile_NN.png files there; --keep-frames instead keeps the temporary folder.
  - `node tools/render_html.cjs --in starters/html-canvas/index.html --out ./out/film.mp4 --frames-dir ./out/frames`
- **help**: Prints the options and exit codes (0 ok, 1 usage, 2 render or encode failure, 3 ffprobe disagrees). Note: `-h` is not recognised and exits 1 with a usage error.
  - `node tools/render_html.cjs --help`

#### المتطلبات والأمان

- binaries: chromium, ffmpeg, ffprobe, node
- network: true
- node: playwright
- optional: bin:ffmpeg built with the drawtext filter (time labels on preview tiles)
- الأمان: network
- الموافقة: An http(s) --in URL, or a page that loads remote assets, contacts the network (the html-canvas starter loads Google Fonts); --offline blocks this. It runs the page's own scripts in headless Chromium with HTTPS errors ignored, so render only pages the user trusts. It overwrites --out, and --frames-dir deletes existing frame_NNNNNN.png and preview_raw/tile_NN.png files in that folder.
- الحدود: It verifies only container metrics (fps, frame count, duration, size, audio presence), not whether the visuals are right, and it installs nothing: Playwright, its Chromium and ffmpeg/ffprobe must already be present.

#### الاختبارات والأدلة

- لا اختبار مسجل: الشارة لا تتجاوز 📄 حتى يُختبر هنا.
- مرجع: `tools/render_html.md`
- مرجع: `playbooks/render-pipeline.md`
- مرجع: `starters/html-canvas/README.md`
- مرجع: `playbooks/audio-sync.md`
- مرجع: `README.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/motion.md`
- مرجع: `.claude/skills/kosif-superpowers/references/capabilities.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:repo-render-html --evidence <ملف>`.

### `repo-verify-video` — بوابة فحص تسليم الفيديو / Video delivery gate

| الحقل | القيمة |
|---|---|
| المسار | `tools/verify_video.py` (جذر: repo) |
| المجال | `motion` |
| الدليل | `tested-here` |
| العائلات | `qa-verification`, `verification-evals`, `media-image-audio`, `formats-platforms` |

**ما تفعله:** يفحص الفيديو المُصدَّر عبر ffprobe وffmpeg ويقارنه بالمطلوب: ترميز H.264 وصيغة yuv420p والأبعاد الزوجية ونسبة العرض ومعدل الإطارات والمدة وعدد الإطارات، وصوت AAC بتردد لا يقل عن 44.1 كيلوهرتز. ويقيس كذلك الجهارة المتكاملة وفق EBU R128 (الهدف الافتراضي ‎-14 LUFS بسماحية ±1.5) والذروة الحقيقية التي يجب ألا تتجاوز ‎-1 dBFS، ويتحقق من تطابق طول الصوت مع الملف الأصلي (±50 ملّي ثانية). ثم يطبع سطور نجاح أو فشل، ويكتب تقرير JSON عند الطلب.

**What it does:** Probes a rendered video with ffprobe and ffmpeg and checks it against the request: H.264, yuv420p, even dimensions, aspect, fps, duration and frame count, AAC audio at 44.1 kHz or more, EBU R128 integrated loudness (default -14 LUFS ±1.5), true peak ≤ -1 dBFS and master-audio length (±50 ms). It prints PASS/FAIL lines and can write a JSON report.

#### متى تُستدعى

- «افحص الفيديو النهائي قبل التسليم: المقاس والمدة والصوت»
- «تأكد إن الريل 9:16 و30 فريم ومدته 15 ثانية بالضبط»
- «هل جهارة الصوت في الفيلم -14 LUFS؟»
- «verify my render matches 9:16, 30 fps, 12 s and the voice track»
- «check loudness and true peak of film.mp4»
- «fill the TEST_REPORT numbers for the delivered MP4»

#### الأوامر

- **verify**: Runs every check (13 when all options are given), including that the delivered audio length matches the master file; prints PASS/FAIL lines and 'N/M checks passed' and writes the JSON report.
  - `python3 tools/verify_video.py ./out/film.mp4 --aspect 9:16 --fps 30 --duration 12 --audio ./voice.mp3 --json ./out/report.json`
- **verify source-preserved audio**: Requires the first audio stream's packet MD5 (ADTS-normalised for AAC) to equal the source's and no other audio stream; when both hold, loudness, true peak, a sample rate under 44.1 kHz and an MP3 codec are [INFO] 'source preserved … (not normalised by design)' instead of failures; JSON gains source_audio and a status on every check.
  - `python3 tools/verify_video.py ./out/reel.mp4 --aspect 9:16 --fps 30 --duration 15 --source-audio ./voice.m4a --json ./out/report.json`
- **silent**: Checks an intentionally silent deliverable: requires that there is no audio stream and skips the audio checks.
  - `python3 tools/verify_video.py ./out/film.mp4 --aspect 16:9 --fps 30 --duration 6 --no-audio`
- **loudness-target**: Runs the codec, size and audio checks with a different integrated-loudness target (±1.5 LU).
  - `python3 tools/verify_video.py ./out/film.mp4 --lufs -16`
- **help**: Shows usage and the list of checks.
  - `python3 tools/verify_video.py --help`

#### المتطلبات والأمان

- binaries: ffmpeg, ffprobe, python3
- الأمان: runs-external-programs
- الموافقة: --json overwrites the named report file; otherwise it only reads the video and master audio with local ffprobe/ffmpeg.
- الحدود: Checks technical delivery specs only; it does not judge visual content, caption correctness or word-level audio sync. --source-audio compares the first audio stream only (an extra stream fails the separate one-stream check).

#### الاختبارات والأدلة

- `tests/test_tools_extra.py`
- `tests/test_verify_source_audio.py`
- مرجع: `playbooks/render-pipeline.md`
- مرجع: `playbooks/audio-sync.md`
- مرجع: `playbooks/music.md`
- مرجع: `.claude/skills/kosif-superpowers/references/verification.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/motion.md`
- مرجع: `tools/render_html.md`
- مرجع: `starters/html-canvas/README.md`
- مرجع: `README.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:repo-verify-video --evidence <ملف>`.

### `starter-html-canvas` — قالب فيلم HTML Canvas / HTML Canvas film starter

| الحقل | القيمة |
|---|---|
| المسار | `starters/html-canvas/` (جذر: repo) |
| المجال | `motion` |
| الدليل | `tested-elsewhere` |
| العائلات | `engines-render-pipeline`, `easing-timing-rhythm`, `audio-sync-captions`, `typography-arabic` |

**ما تفعله:** فيلم تجريبي عمودي بنسبة 9:16 (‏1080×1920، و30 إطارًا في الثانية، و12 ثانية) مبني بـ HTML وCanvas وSVG دون مكتبات JavaScript، ويُحسب كل إطار فيه من الزمن وحده. يوفّر الدالة window.__kosif.seek(t) ليحوّله tools/render_html.cjs إلى ملف MP4 بنتيجة متطابقة في كل مرة، ويضم خطًا زمنيًا للمشاهد، ودوال تسهيل، وكاميرا بإطارات مفتاحية، ورسمًا تدريجيًا لمسارات SVG، وجسيمات ببذرة عشوائية ثابتة، وترجمة عربية متزامنة على مستوى الكلمة.

**What it does:** A 9:16 sample film (HTML + Canvas + SVG, 1080x1920, 30 fps, 12 s, no JS libraries) whose every frame is a pure function of time. It exposes window.__kosif.seek(t) so tools/render_html.cjs can render it deterministically to MP4, and shows a scene timeline, easing, a keyframed camera, SVG draw-on, seeded particles and word-synced Arabic captions.

#### متى تُستدعى

- «ابدأ مشروع موشن HTML Canvas بترجمة عربية متزامنة»
- «عايز قالب فيلم 9:16 أعدّله وأرندره MP4»
- «أبي قالب جاهز فيه كاميرا ورسم مسار وجسيمات»
- «Start a deterministic canvas motion graphic with word-synced Arabic captions»
- «Give me a starter page that render_html can seek frame by frame»

#### الأوامر

- **scaffold**: Creates a project folder (STYLE.md, PLAN.md, TEST_REPORT.md, words.json, REQUEST.md) and copies this starter to ./my-film/html-canvas/ without node_modules. It refuses a non-empty folder unless --force is given.
  - `python3 tools/kosif.py scaffold kinetic-arabic ./my-film --starter html-canvas`
- **live-preview**: Opens the page with play, scrub and safe-area controls. Space toggles play, ?t=3.2 jumps to a time and ?autoplay=1 starts playback. The controls hide under the renderer (navigator.webdriver).
  - `python3 -m webbrowser "file://$PWD/starters/html-canvas/index.html"`
- **words**: Regenerates words.js (window.KOSIF_WORDS) from SRT, VTT, Whisper JSON, CSV/TSV or words.json. The page reads words.js, so it also works from file://.
  - `python3 tools/words_convert.py ./captions.srt ./my-film/html-canvas/words.js`
- **contact-sheet**: Renders 8 evenly spaced, labelled frames into ./out/film_preview.png for approval before the final render. --offline blocks the Google Fonts request, so a system font is used.
  - `node tools/render_html.cjs --in starters/html-canvas/index.html --out ./out/film.mp4 --preview --offline`
- **render**: Seek-mode render of all 360 frames with headless Chromium, encoded with libx264 by ffmpeg. The user's audio is re-encoded to AAC 192k with its timing untouched, then padded or cut to the film's 12 s.
  - `node tools/render_html.cjs --in starters/html-canvas/index.html --out ./out/film.mp4 --fps 30 --audio ./voice.mp3`
- **verify**: Delivery gate that checks codecs, size, fps, frame count, audio and loudness against the request. --audio also requires the delivered audio to match the master's length (±50 ms).
  - `python3 tools/verify_video.py ./out/film.mp4 --aspect 9:16 --fps 30 --duration 12 --audio ./voice.mp3`
- **KOSIF.Timeline**: The in-page API from timeline.js. It also exports Ease (linear, outCubic, inOutCubic, outExpo, outQuint, outBack, inBack, spring), prog, window01, lerp, clamp01, rng(seed), cameraAt/applyCamera, activeWord and phrases.
  - `const tl = new KOSIF.Timeline({ duration: 12, fps: 30, scenes: [{ id: 'title', t0: 0, t1: 3, draw: (t, p, local) => {} }] }); window.__kosif = { duration: 12, fps: 30, seek: (t) => tl.seek(t) };`

#### المتطلبات والأمان

- binaries: chromium, ffmpeg, ffprobe, node, python3
- network: true
- node: playwright
- الأمان: network
- الموافقة: Unless --offline is passed, the page fetches the Cairo webfont from fonts.googleapis.com, and opening it in a browser does too. Any --audio file must be one the user has rights to (it is re-encoded to AAC with its timing untouched).
- الحدود: It is one hand-coded 12 s sample film to copy and edit, with no visual editor, and it does not render itself (render_html.cjs with Playwright Chromium and ffmpeg does).

#### الاختبارات والأدلة

- لا اختبار مسجل: الشارة لا تتجاوز 📄 حتى يُختبر هنا.
- مرجع: `starters/html-canvas/README.md`
- مرجع: `tools/render_html.md`
- مرجع: `playbooks/render-pipeline.md`
- مرجع: `AGENTS.md`
- مرجع: `README.md`
- مرجع: `.claude/skills/kosif-superpowers/references/capabilities.md`
- مرجع: `.claude/skills/kosif-superpowers/references/powers/engines-render-pipeline.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/motion.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:starter-html-canvas --evidence <ملف>`.

### `starter-remotion` — قالب فيلم Remotion / Remotion film starter

| الحقل | القيمة |
|---|---|
| المسار | `starters/remotion/` (جذر: repo) |
| المجال | `motion` |
| الدليل | `tested-elsewhere` |
| العائلات | `engines-render-pipeline`, `audio-sync-captions`, `charts-data-infographic`, `typography-arabic` |

**ما تفعله:** مشروع Remotion v4 مصغّر فيه تركيبة واحدة اسمها KosifFilm (‏1080×1920، و30 إطارًا في الثانية، و12 ثانية): عنوان تظهر كلماته تباعًا، ورسم بياني خطي متحرك بـ SVG، وبطاقة شعار ختامية، وكلها داخل حامل كاميرا متحرك (CameraRig)، مع ترجمة على مستوى الكلمة من public/words.json. وتتحكم فيها الخصائص title وwords وaccent وlang.

**What it does:** A minimal Remotion v4 project with one composition, KosifFilm (1080x1920, 30 fps, 12 s): a staggered title, an animated SVG line chart and a closing logo card inside a CameraRig, plus word-level captions from public/words.json, driven by title, words, accent and lang props.

#### متى تُستدعى

- «ابدأ مشروع Remotion لفيديو عمودي بترجمة عربية»
- «عايز أعمل فيديو React فيه عنوان ورسم بياني وشعار»
- «أبي أعدّل الخصائص في Remotion Studio وأصدّر MP4»
- «Set up a Remotion starter with word-level captions from words.json»
- «Render KosifFilm with custom props to MP4»

#### الأوامر

- **scaffold**: Creates the project documents and copies this starter to ./my-film/remotion/ without node_modules, which keeps installs out of the repo.
  - `python3 tools/kosif.py scaffold product ./my-film --starter remotion`
- **install**: Installs the pinned remotion@4.0.535, @remotion/cli, react@19.3.1, react-dom, TypeScript and the @types packages from the npm registry. npm ci installs exactly from the committed package-lock.json.
  - `cd ./my-film/remotion && npm install`
- **preview**: Starts Remotion Studio, a long-lived server at http://localhost:3000, with a timeline and live prop editing.
  - `cd ./my-film/remotion && npm run preview`
- **still**: Renders frame 60 to out/still.png.
  - `cd ./my-film/remotion && npm run still`
- **render**: Renders KosifFilm with the default props to out/film.mp4.
  - `cd ./my-film/remotion && npm run render`
- **render-props**: Renders with custom title, words, accent and lang props. Adding --frames=0-30 renders the first second as a quick smoke test.
  - `cd ./my-film/remotion && npx remotion render KosifFilm out/film.mp4 --props=./props.example.json`
- **typecheck**: Runs tsc --noEmit.
  - `cd ./my-film/remotion && npm run typecheck`
- **verify**: Runs the delivery gate on the render. Once AUDIO_FILE is set in src/Film.tsx, drop --no-audio and pass --audio instead.
  - `python3 tools/verify_video.py ./my-film/remotion/out/film.mp4 --aspect 9:16 --fps 30 --duration 12 --no-audio`

#### المتطلبات والأمان

- binaries: node, npm, npx, python3
- network: true
- node: @remotion/cli, react, react-dom, remotion, typescript
- optional: bin:chromium_headless_shell, bin:ffmpeg, bin:ffprobe, npm:@remotion/media-utils@4.0.535
- الأمان: network
- الموافقة: npm install (or npm ci) downloads packages from the npm registry. Remotion's licence is free for individuals and companies of up to 3 people, and larger companies need a paid company licence, so confirm before commercial use. npm run preview starts a long-lived local server. If no local Chromium is found, Remotion may download a headless browser.
- الحدود: It was neither installed nor rendered here (no node_modules), and it is one fixed 12 s composition whose length does not follow the audio unless you add calculateMetadata.

#### الاختبارات والأدلة

- لا اختبار مسجل: الشارة لا تتجاوز 📄 حتى يُختبر هنا.
- مرجع: `starters/remotion/README.md`
- مرجع: `playbooks/render-pipeline.md`
- مرجع: `AGENTS.md`
- مرجع: `README.md`
- مرجع: `KOSIF_SUPERPOWERS_ENVIRONMENT_REPORT.md`
- مرجع: `.claude/skills/kosif-superpowers/references/capabilities.md`
- مرجع: `.claude/skills/kosif-superpowers/references/powers/engines-render-pipeline.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/motion.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:starter-remotion --evidence <ملف>`.

### `style-atlas-bridge` — أطلس الأساليب الكامل (86 طريقة): بحث وتوليف وموجز إنتاج وهيكل مشروع شرح / Futurepedia AI Style Atlas — all 86 methods: search, fusion, storyboard-first briefs and engine scaffolds

| الحقل | القيمة |
|---|---|
| المسار | `scripts/style_atlas_bridge.py` (جذر: skill) |
| المجال | `motion` |
| الدليل | `tested-here` |
| العائلات | `hand-drawn-draw-on`, `story-direction-ideas` |

**ما تفعله:** يبحث في 86 طريقة من أطلس Futurepedia في 14 عائلة (الشكل، الحركة، قواعد الشرح، الخطوط، الألوان، التقنيات، الأصوات)، ويدمج طريقتين 85/15، ويكتب موجز إنتاج بستوريبورد أولًا، ويُنشئ مشروع شرح جاهزًا على محرك KOSIF الأصلي.

**What it does:** Searches the 86 paraphrased Futurepedia AI Style Atlas methods in 14 families (look, motion, explainer grammar, fonts, palette, techniques, sounds), fuses up to two (85/15), writes a storyboard-first production brief, scaffolds an explainer project on the original KOSIF engine, and draws static SVG studies.

#### متى تُستدعى

- «ادمج أساليب Futurepedia في الرسم»
- «اعمل فيلم شرح بأسلوب الطباشير»
- «Find Futurepedia AI Style Atlas methods»
- «Make an animated explainer in a retro CRT style»

#### الأوامر

- **families**: Lists the 14 families and their 86 methods.
  - `python3 scripts/style_atlas_bridge.py families`
- **search**: Ranks methods by Arabic/English words over name, look, motion, grammar, fonts and hints.
  - `python3 scripts/style_atlas_bridge.py search "سبورة"`
- **show**: Prints one full method card.
  - `python3 scripts/style_atlas_bridge.py show FA-45`
- **brief**: Writes a storyboard-first production brief (style card, contract, steps, acceptance).
  - `python3 scripts/style_atlas_bridge.py brief --topic "كيف تعمل البطارية" --style FA-45 --accent FA-16 --out out/atlas/brief.md`
- **scaffold**: Copies the original engine, font and style card into a new explainer project.
  - `python3 scripts/style_atlas_bridge.py scaffold --style FA-45 --out out/atlas/battery`
- **plan**: Writes a typed 85/15 fusion recipe with the production contract.
  - `python3 scripts/style_atlas_bridge.py plan --topic "كيف يتعلم الذكاء" --style FA-04 --accent FA-06 --out out/fusion.json`
- **study-svg**: Draws a static original SVG study for any of the 86 methods.
  - `python3 scripts/style_atlas_bridge.py study-svg --style FA-15 --topic "original" --out out/study.svg`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: Writes new output files in explicitly selected locations only; refuses overwrite; no network, paid tools or private downloads.
- الحدود: Method cards are paraphrases; a scaffold starts from the FA-23 chalkboard demo, so each other method's medium must still be drawn per project before rendering. Nothing is rendered until atlas_render.py runs.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_style_atlas_bridge.py`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A14-drawing-cinematic-academy.md`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A15-futurepedia-style-atlas.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:style-atlas-bridge --evidence <ملف>`.

### `ui-beat` — إيقاع الواجهات: مسار مؤشر بتسهيل وعكس تخطيط للعربية وفحص الحلقة المتصلة / UI beat: eased cursor keyframes, RTL layout mirror and seamless-loop check

| الحقل | القيمة |
|---|---|
| المسار | `scripts/ui_beat.py` (جذر: skill) |
| المجال | `motion` |
| الدليل | `tested-here` |
| العائلات | `ui-product-device` |

**ما تفعله:** يحسب إطارات حركة المؤشر على منحنى بيزييه بتسهيل CSS مع توقيت النقر والتموج، ويعكس تخطيط الواجهة للعربية مع قائمة الأيقونات التي تنقلب، ويتأكد أن بداية الحلقة تساوي نهايتها.

**What it does:** Computes one cursor keyframe per frame along a bowed quadratic Bezier timed by a CSS cubic-bezier easing (solved by bisection), with press, release, UI-response (60-120 ms) and ripple timings; mirrors a UI layout for RTL (x' = W - x - w, left/right alignment flips, directional icon flip list); and checks that a loop's first and last states match, listing differing keys.

#### متى تُستدعى

- «اعمل حركة ماوس طبيعية من الزر للقائمة مع نقرة»
- «اعكس تصميم الشاشة ده للعربي»
- «اتأكد إن اللوب بيرجع لنفس البداية»
- «Generate cursor keyframes with a click ripple for a UI demo»
- «Mirror this layout for RTL»
- «Check that my UI animation loops seamlessly»

#### الأوامر

- **cursor**: Per-frame x/y/progress/angle keyframes plus click, response and ripple timings.
  - `python3 scripts/ui_beat.py cursor --from 900,1700 --to 540,960 --dur 0.8 --fps 30 --ease ease-in-out --arc 0.12`
- **rtl-mirror**: Mirrored elements, alignment flips, icons to flip vs keep, warnings for out-of-bounds elements.
  - `python3 scripts/ui_beat.py rtl-mirror /tmp/layout.json --width 1080`
- **loop-check**: seamless true/false with every differing, missing or retyped key; warns outside 3-6 s.
  - `python3 scripts/ui_beat.py loop-check /tmp/states.json --tol 0.000001`
- **self-test**: Offline self-check.
  - `python3 scripts/ui_beat.py --self-test`

#### المتطلبات والأمان

- الأمان: read-only
- الموافقة: —
- الحدود: Computes numbers only (no rendering): one Bezier leg per call, icon flipping is a name-based rule list, and loop-check compares declared states, not rendered frames.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_ui_beat.py`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:ui-beat --evidence <ملف>`.

### `unified-cinematic` — السينما الموحدة: مونتاج الفيديو مع الصوت وحركة الكاميرا / Unified Cinematic: sound-clocked animation and video

| الحقل | القيمة |
|---|---|
| المسار | `scripts/unified_cinematic.py` (جذر: skill) |
| المجال | `motion` |
| الدليل | `tested-here` |
| العائلات | `audio-sync-captions`, `camera-composition-layout`, `photo-video-footage`, `easing-timing-rhythm` |

**ما تفعله:** تجميع معالجة الصور والرسم والموشن والموسيقى في فيديو بصوت متزامن، وحركة كاميرا وتأثيرات دخول وخروج.

**What it does:** Compose photo effects, layered animated strokes and shapes, WAV onset candidates, camera push/pan transitions and source-timed AAC audio into H.264 MP4.

#### متى تُستدعى

- «Combine a local WAV audio master with a drawn scene and render cinematic MP4»
- «Animate a drawing using measured audio transients and camera movement»
- «إضافة الصوت والحركة والمؤثرات السينمائية إلى فيديو الرسم»

#### الأوامر

- **doctor**: Display source audio formats, selected camera moves, codec support.
  - `python3 scripts/unified_cinematic.py doctor`
- **render**: Build source-audio-clocked composited H.264/AAC MP4 with camera movement, fades, and measured transient-driven drawing pulses.
  - `python3 scripts/unified_cinematic.py render --photo templates/unified-media-demo-photo.png --scene templates/unified-draw-motion-demo.json --audio ./source.wav --output ./cinematic.mp4 --fps 12 --camera push-in --fade-frames 2 --pulse-element 3`
- **tests**: Run eight integration regression tests, including real H264/AAC output and source WAV immutability.
  - `python3 scripts/test_unified_cinematic.py`

#### المتطلبات والأمان

- binaries: ffmpeg, ffprobe
- python: Pillow, numpy, opencv-python
- الأمان: writes-files
- الموافقة: —
- الحدود: Maximum 300 video frames; 2D camera not real 3D; WAV source untouched but exported MP4 AAC is re-encoded; no verified BPM/beats, lyrics or phoneme word alignment; no claim all skills fused.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/scripts/test_unified_cinematic.py`
- مرجع: `.claude/skills/kosif-superpowers/references/unified-cinematic-integration.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:unified-cinematic --evidence <ملف>`.

### `verify-video` — بوابة فحص تسليم الفيديو / Video delivery gate

| الحقل | القيمة |
|---|---|
| المسار | `scripts/verify_video.py` (جذر: skill) |
| المجال | `motion` |
| الدليل | `tested-here` |
| العائلات | `qa-verification`, `formats-platforms`, `media-image-audio` |

**ما تفعله:** يفحص الفيديو المُصدَّر باستخدام ffprobe وffmpeg مقابل المطلوب (ترميز H.264 وyuv420p، والأبعاد الزوجية، ونسبة الأبعاد، ومعدل الإطارات، والمدة وعدد الإطارات، وصوت AAC بتردد 44.1 كيلوهرتز فأكثر، وجهارة الصوت وفق EBU R128 والذروة الحقيقية، وتطابق طوله مع الصوت الأصلي)، ثم يطبع نتيجة كل فحص بالنجاح أو الفشل مع تقرير JSON اختياري.

**What it does:** Checks a rendered video with ffprobe/ffmpeg against the request (H.264/yuv420p, even size, aspect, fps, duration and frame count, AAC audio at ≥44.1 kHz, EBU R128 loudness and true peak, master-audio length) and prints PASS/FAIL lines with an optional JSON report.

#### متى تُستدعى

- «Verify this MP4 is 9:16, 30 fps and 15 seconds before delivery»
- «Check the loudness and that the audio length matches my voice file»
- «اتأكد إن الفيديو مقاس ريلز وإن الصوت مضبوط قبل ما أسلمه»
- «افحص الفيديو النهائي: المدة والفريمات والصوت»
- «Is my rendered film ready to upload?»

#### الأوامر

- **verify**: Runs the codec/size/aspect/fps/duration/frame-count/audio/loudness checks and writes a JSON report; exit 0 if all pass, 1 if any fail.
  - `python3 scripts/verify_video.py ./in.mp4 --aspect 9:16 --fps 30 --duration 15 --json ./out/report.json`
- **verify source-preserved audio**: Requires the first audio stream's packet MD5 (ADTS-normalised for AAC) to equal the source's and no other audio stream; when both hold, loudness, true peak, a sample rate under 44.1 kHz and an MP3 codec are [INFO] 'source preserved … (not normalised by design)' instead of failures; JSON gains source_audio and a status on every check.
  - `python3 scripts/verify_video.py ./out/reel.mp4 --aspect 9:16 --fps 30 --duration 15 --source-audio ./voice.m4a --json ./out/report.json`
- **verify with master audio**: Adds a check that the delivered audio length matches the master audio within 50 ms.
  - `python3 scripts/verify_video.py ./in.mp4 --aspect reel --fps 30 --duration 15 --audio ./voice.wav --lufs -14`
- **verify silent**: Requires that the deliverable has no audio stream and skips the audio and loudness checks.
  - `python3 scripts/verify_video.py ./in.mp4 --aspect 16:9 --no-audio`

#### المتطلبات والأمان

- binaries: ffmpeg, ffprobe
- الأمان: runs-external-programs
- الموافقة: —
- الحدود: Checks technical delivery specs only; it does not judge visual content, caption correctness or word-level audio sync. --source-audio compares the first audio stream only (an extra stream fails the separate one-stream check).

#### الاختبارات والأدلة

- `tests/test_tools_extra.py`
- `tests/test_verify_source_audio.py`
- مرجع: `.claude/skills/kosif-superpowers/references/verification.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/motion.md`
- مرجع: `.claude/skills/kosif-superpowers/references/executable-creative-motion.md`
- مرجع: `.claude/skills/kosif-superpowers/references/motion-runtime.md`
- مرجع: `playbooks/render-pipeline.md`
- مرجع: `playbooks/audio-sync.md`
- مرجع: `README.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:verify-video --evidence <ملف>`.

