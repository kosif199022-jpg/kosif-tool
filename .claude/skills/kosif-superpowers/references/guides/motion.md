# الموشن والرندر — Motion graphics and rendering

إنشاء موشن جرافيك قابل للتعديل (SVG/HTML/Canvas) ورندره إلى MP4 مع الصوت، والمكتبات الحقيقية (GSAP وRemotion وManim وThree وPixi وp5) وجسر Motion Starter Kit.

Authoring editable motion graphics (SVG/HTML/Canvas), rendering them to MP4 with audio, scaffolding real-library projects and the Motion Starter Kit bridge.

Commands below are typed from the skill folder (`.claude/skills/kosif-superpowers/`) unless they say otherwise; `$SKILL_DIR` means that folder.

<!-- hub:area:motion:start -->

**الأدوات / tools (23)** — `python3 scripts/hub.py tool <id>` for every command, requirement and limit:

| tool | what it does | start with | evidence |
|---|---|---|---|
| `aspects` | Standard-library Python module that turns any aspect spec (W:H ratio, WxH pixels, or an English/Arabic platform name such as reel, cinema or مربع) into a label and even pixel dimensions, plus ratio, resolution-string and validity helpers. | `python3 -c "import sys; sys.path.insert(0,'scripts'); import aspects; print(aspects.resolve('2.35:1'))"` | tested-here |
| `creative-reasoning-bridge` | Turns a kosif.audio-cues.v1 JSON (measured onsets plus aligned words from audio_cue_mapper.py) into an editable motion_director storyboard with timed text, a draw-on path, a character and a camera zoom, plus a decision report that scores the doodle, kinetic and cinematic styles. | `python3 scripts/creative_reasoning_bridge.py ./cues.json --style auto --out ./out/scene.json --report ./out/decision.json` | tested-here |
| `motion-director` | Validates a word-timed JSON scene spec (paths, circles, text, characters, rigged actors, morphs, camera) and compiles it into a self-contained seekable SVG/HTML animation, with an optional MP4 render through render_html.cjs. | `python3 scripts/motion_director.py doctor` | tested-here |
| `motion-engine-js` | A browser-side script (IIFE), inlined by motion_director.py compile, that reads scene JSON from <script id=kosif-data> and animates an SVG film deterministically: stroke draw-on, text fades, polygon morphs, a stick character, pivot-rigged actors (walk/run/wave/point/sit) with a moving pen tip, per-scene camera zoom/pan and word-timed RTL captions, all through window.__kosif.seek(t) for frame-exact rendering. | `python3 scripts/motion_director.py compile ./scene.json --out ./out/film.html` | tested-here |
| `motion-kit-bridge` | Converts motalim-ai/motion-starter-kit word-timing JSON (lines[].words[]) into a validated native KOSIF Motion Director storyboard, plus optional seekable HTML, for the plotter, doodle, whiteboard or infographic styles. | `python3 scripts/motion_kit_bridge.py styles` | tested-here |
| `motion-runtime` | Scaffolds an editable Arabic whiteboard-doodle SVG film (film.html + motion.json + README) with a deterministic seek contract, lists 25 motion-engine route cards, and only with explicit --run renders it to a 1080x1920 PNG preview or MP4 through render_html.cjs. | `python3 scripts/motion_runtime.py doctor` | tested-here |
| `motion-stack` | Lists 25 catalogued motion technologies and writes original, uninstalled starter projects for GSAP (+Rough.js/Vivus), Remotion, Manim, Three.js, PixiJS or p5.js; the GSAP, Three.js, PixiJS and p5 starters expose a seekable window.__kosif contract. | `python3 scripts/motion_stack.py list` | tested-here |
| `motion-toolkit` | A dependency-free ES module that exports 12 deterministic, seekable animation primitives: clamp, easing, keyframe interpolation and timelines, SVG stroke reveal, camera pan/zoom, walk-cycle joint angles, parallax, seeded hand-drawn line jitter, HH:MM:SS:FF timecode, whole-word caption cue state and a render frame-contract check. | `node --input-type=module -e "import {ease, timeCode} from './resources/motion-runtime/motion_toolkit.mjs'; console.log(ease(0.5,'cubic'), timeCode(2.5,30))"` | tested-here |
| `render-html` | The skill's bundled copy of KOSIF's deterministic HTML-to-MP4 renderer: it captures a local or http HTML film frame by frame in headless Chromium (through window.__kosif.seek(t) or Chromium virtual time), encodes H.264 with ffmpeg, optionally muxes untouched audio and checks fps, frames, duration, size and audio with ffprobe, or with --preview makes an 8-frame contact sheet instead. | `node resources/motion-runtime/render_html.cjs --in ./film.html --out ./out/film.mp4 --fps 30 --audio ./voice.wav` | tested-elsewhere |
| `verify-video` | Checks a rendered video with ffprobe/ffmpeg against the request (H.264/yuv420p, even size, aspect, fps, duration and frame count, AAC audio at ≥44.1 kHz, EBU R128 loudness and true peak, master-audio length) and prints PASS/FAIL lines with an optional JSON report. | `python3 scripts/verify_video.py ./in.mp4 --aspect 9:16 --fps 30 --duration 15 --json ./out/report.json` | tested-here |
| `repo-aspects` (repo root) | A standard-library-only Python module, shared by kosif.py, verify_video.py and import_briefs.py, that turns any aspect spec (a W:H ratio, WxH pixels or an English or Arabic platform name such as reel, cinema or مربع) into a label and an even pixel size, with helpers for the numeric ratio, a 'WxH' string and validity. | `python3 -c "import sys; sys.path.insert(0,'tools'); from aspects import resolve; print(resolve('2.35:1'))"` | tested-here |
| `repo-render-html` (repo root) | Renders a local or http HTML film frame by frame in headless Chromium (Playwright), driving the page through window.__kosif.seek(t) or, for any CSS/WAAPI/rAF/GSAP page, through paused Chromium virtual time. It encodes H.264 yuv420p with ffmpeg, can mux a supplied audio track re-encoded as AAC 192k without resampling or retiming it, and checks fps, frame count, duration, size and audio presence with ffprobe. With --preview it writes an 8-frame contact-sheet PNG instead of a video. | `node tools/render_html.cjs --in starters/html-canvas/index.html --out ./out/film.mp4 --fps 30 --audio ./voice.mp3` | tested-elsewhere |
| `repo-verify-video` (repo root) | Probes a rendered video with ffprobe and ffmpeg and checks it against the request: H.264, yuv420p, even dimensions, aspect, fps, duration and frame count, AAC audio at 44.1 kHz or more, EBU R128 integrated loudness (default -14 LUFS ±1.5), true peak ≤ -1 dBFS and master-audio length (±50 ms). It prints PASS/FAIL lines and can write a JSON report. | `python3 tools/verify_video.py ./out/film.mp4 --aspect 9:16 --fps 30 --duration 12 --audio ./voice.mp3 --json ./out/report.json` | tested-here |
| `repo-job-wait` (repo root) | Starts a long render, encode, download or install detached (log, pid and exit code in a job folder) and waits on it without `sleep N; check`, which Claude Code blocks: `wait` prints a throttled PROGRESS line (render_html.cjs `frame i/n`, ffmpeg `frame=`, percentages) then DONE or FAILED with the log tail and exits with the job's code, for the Monitor tool or Bash run_in_background; `status` peeks without waiting; `stop` ends it. | `python3 tools/job.py start --dir out/20261024-film/render -- node tools/render_html.cjs --in film.html --out out/film.mp4` | tested-here |
| `starter-html-canvas` (repo root) | A 9:16 sample film (HTML + Canvas + SVG, 1080x1920, 30 fps, 12 s, no JS libraries) whose every frame is a pure function of time. It exposes window.__kosif.seek(t) so tools/render_html.cjs can render it deterministically to MP4, and shows a scene timeline, easing, a keyframed camera, SVG draw-on, seeded particles and word-synced Arabic captions. | `python3 tools/kosif.py scaffold kinetic-arabic ./my-film --starter html-canvas` | tested-elsewhere |
| `starter-remotion` (repo root) | A minimal Remotion v4 project with one composition, KosifFilm (1080x1920, 30 fps, 12 s): a staggered title, an animated SVG line chart and a closing logo card inside a CameraRig, plus word-level captions from public/words.json, driven by title, words, accent and lang props. | `python3 tools/kosif.py scaffold product ./my-film --starter remotion` | tested-elsewhere |
| `unified-cinematic` | Compose photo effects, layered animated strokes and shapes, WAV onset candidates, camera push/pan transitions and source-timed AAC audio into H.264 MP4. | `python3 scripts/unified_cinematic.py doctor` | tested-here |
| `style-atlas-bridge` | Searches the 86 paraphrased Futurepedia AI Style Atlas methods in 14 families (look, motion, explainer grammar, fonts, palette, techniques, sounds), fuses up to two (85/15), writes a storyboard-first production brief, scaffolds an explainer project on the original KOSIF engine, and draws static SVG studies. | `python3 scripts/style_atlas_bridge.py families` | tested-here |
| `atlas-render` | Drives an A15 explainer page (window.seek/DURATION/scoreSound) in headless Chromium: storyboard grid PNG, single stills, a determinism and speed check, frame-by-frame H.264 render with the KSound score rendered offline and muxed as AAC, and a single-file HTML bundle. | `python3 scripts/atlas_render.py check` | tested-here |
| `particles` | Computes every particle of a seeded burst at any time t from a closed-form drag+gravity solution and a stateless lowbias32 hash RNG (so frames render identically in any order), checks a particle spec against the family's budget rules (sizes, colours, per-engine counts, burst size, seeding, layering), and writes one frame as SVG for visual review. | `python3 scripts/particles.py burst --seed 7 --count 40 --t 0.5 --visible-only` | tested-here |
| `ui-beat` | Computes one cursor keyframe per frame along a bowed quadratic Bezier timed by a CSS cubic-bezier easing (solved by bisection), with press, release, UI-response (60-120 ms) and ripple timings; mirrors a UI layout for RTL (x' = W - x - w, left/right alignment flips, directional icon flip list); and checks that a loop's first and last states match, listing differing keys. | `python3 scripts/ui_beat.py cursor --from 900,1700 --to 540,960 --dur 0.8 --fps 30 --ease ease-in-out --arc 0.12` | tested-here |
| `motion-physics` | Computes motion numbers instead of guessing them: a spring from stiffness, damping and mass (value per frame, damping ratio, settle time, overshoot, or CSS @keyframes), any CSS cubic-bezier or named easing sampled exactly as a browser does, stagger delays from an origin (first, last, center, edges or an index) on a row or a grid, and a keyframe track sampled per frame with an easing. Pure standard library; prints JSON or CSS and writes no files. | `python3 scripts/motion_physics.py spring --from 0 --to 1 --stiffness 170 --damping 26 --fps 30` | tested-here |
| `infinite-matrices` (repo root) | Builds a new visual system from causal bricks (state, operation, law, time, memory, feedback) mined from the 86 atlas styles, proves its law with an A/B/C counterfactual over seeds and a dose sweep, renders a scrubbable scene, stills and MP4 with the atlas harness and sound kit, and saves verdicts, ideas, ratings and sources in a hash-chained ledger. | `python3 .claude/skills/kosif-infinite-matrices/scripts/kmx.py doctor` | tested-here |

<!-- hub:area:motion:end -->

## الفهرس / contents

1. [القدرة التنفيذية الجديدة — KOSIF Creative Motion Lab](#القدرة-التنفيذية-الجديدة--kosif-creative-motion-lab)
2. [Motion runtime bridge / جسر الرندر التنفيذي](#motion-runtime-bridge--جسر-الرندر-التنفيذي)

## القدرة التنفيذية الجديدة — KOSIF Creative Motion Lab

**جسر Motion Starter Kit التنفيذي:** لو المستخدم أرسل [motalim-ai/motion-starter-kit](https://github.com/motalim-ai/motion-starter-kit)، لا تكتفِ بفتح مرجع خارجي. اقرأ [جسر Motion Starter Kit التنفيذي](../motion-starter-kit-bridge.md)، واستدعِ `scripts/motion_kit_bridge.py` لتحويل `lines[].words[].w/start/end` إلى Storyboard وHTML KOSIF. أوامر: `styles`، و`demo --style doodle --out demo.json --html demo.html`، و`build --style plotter --timings words.json --out plotter.json --html plotter.html`. أربع طرق SVG قابلة للتنفيذ (doodle, plotter, whiteboard, infographic) وستة أنماط للمراجعة فقط؛ لا تعتبر عرض الستايل إثبات تطابق فيديو مرجعي. لا تخمّن توقيت كلام حقيقي، ولا تعلن عن MP4 قبل رندره وفحصه. هذا الجسر تكامل أصلي مع KOSIF وليس نسخًا للمستودع.

**لا تكتفِ بترشيح المستودعات.** إذا طلب المستخدم موشن أو رسمًا بالكود أو فيديو، افتح [Executable Creative Motion Lab](../executable-creative-motion.md)، ثم **استخدم الأدوات الأصلية داخل المهارة** لإنشاء المصدر الفعلي، وفحص الناتج، وتصدير MP4 عند توفر محرك الرندر. مصدر القدرة هنا هو كود أصلي قابل للتنفيذ؛ المكتبات الخارجية خيارات مستقلة بشروطها.

من داخل جذر المستودع أو مسار المهارة المثبتة:

    python3 $SKILL_DIR/scripts/motion_director.py doctor
    python3 $SKILL_DIR/scripts/motion_director.py sample --out ./storyboard.json
    python3 $SKILL_DIR/scripts/motion_director.py compile ./storyboard.json --out ./motion.html

الملف HTML المولد يحتوي فعلًا على **رسم خطوط SVG تدريجيًا، تحريك جسم شخصية مرسومة بعد ظهورها، حركة كاميرا وتوقيت كلمات صوتية مُعطى**؛ لا تقل إن لديك نص الصوت أو توقيتاته الدقيقة دون فحص ملف المستخدم. للحصول على أدلة فيديو مرجعي مصرح به:

    python3 $SKILL_DIR/scripts/motion_reference_probe.py ./reference.mp4 --cuts --out ./reference-cuts.json

لإنشاء مشاريع قابلة للتعديل تستدعي المكتبات الحقيقية (دون تنزيل تلقائي):

    python3 $SKILL_DIR/scripts/motion_stack.py list
    python3 $SKILL_DIR/scripts/motion_stack.py scaffold gsap --out ./gsap-project
    python3 $SKILL_DIR/scripts/motion_stack.py scaffold remotion --out ./remotion-project
    python3 $SKILL_DIR/scripts/motion_stack.py scaffold manim --out ./manim-project
    python3 $SKILL_DIR/scripts/motion_stack.py scaffold three --out ./three-project
    python3 $SKILL_DIR/scripts/motion_stack.py scaffold pixi --out ./pixi-project
    python3 $SKILL_DIR/scripts/motion_stack.py scaffold p5 --out ./p5-project

محرك الاستوديو الأصلي للمهارة مستقل عن JS packages؛ تشغيل GSAP/Rough/Vivus/Remotion/Manim/Three.js/PixiJS/p5.js الحقيقي يحتاج تثبيتها قانونيًا داخل بيئة المستخدم واختبارها. يعرض ملف [25 creative technologies](../../data/motion_sources.json) ما يمكن تعلمه من كل محرك والأدوار والتراخيص، وليس 25 محركًا مثبتًا. Remotion وGSAP لهما شروط استخدام خاصة تستلزم مراجعة قبل توزيع منتج تجاري. لإنتاج MP4 من HTML مع الصوت، يوجد الآن **محرك KOSIF المضمّن داخل حزمة المهارة** في resources/motion-runtime/render_html.cjs، ومعه scripts/verify_video.py و scripts/aspects.py. يمكن تشغيله دون نسخ المستودع الكامل بشرط توفر Node.js وPlaywright/Chromium وFFmpeg/ffprobe وفحص الناتج:

    python3 $SKILL_DIR/scripts/motion_director.py render ./motion.html --out ./motion.mp4 --audio ./voice.wav
    python3 $SKILL_DIR/scripts/verify_video.py ./motion.mp4 --aspect 9:16 --fps 30 --duration 9 --audio ./voice.wav

**مكتبة حركة إضافية مجربة:** resources/motion-runtime/motion_toolkit.mjs (12 دالة لخط الزمن، الكَي فريم، Easing، التوقيت العربي، وتحريك الشخصية والكاميرا والرسم اليدوي)، ومعها نموذج SVG مستقل resources/motion-runtime/doodle-film.template.html؛ انظر [بروتوكول الإنتاج والاختبار](../executable-creative-motion.md). إنشاء حزمة رفع Claude: python3 $SKILL_DIR/scripts/package_skill.py --lite. **لا تُسمِّ الأدوات مثبتة إلا بعد probe وتشغيلها.**

**حقيقة القدرات:** إنشاء HTML ناجح ≠ إنتاج MP4، واستنباط قطع الفيديو ≠ محاكاة الحركة، ووجود المكتبات في GitHub ≠ تشغيلها. ابحث عن الدليل الفعلي في ناتج الأوامر واختبار الإطارات والصوت قبل وسم القدرة مثبتة. لا تُدخل التقنيات الـ25 في عداد 4,223 تلقائيًا.

## Motion runtime bridge / جسر الرندر التنفيذي

- Use `scripts/motion_runtime.py` for deterministic motion runtime tasks, with `data/motion_engines.json` and `references/motion-runtime.md`; run `evals/test_motion_runtime.py` to validate this added engine before production use.
- Keep existing `scripts/motion_director.py` and `resources/motion-runtime/` workflows as separate, compatible paths; don't replace either runtime. Verify rendered video and audio before delivery.

## Causal style synthesis (KOSIF Infinite Matrices)

When the request is a *new* look or motion system rather than an existing style, use the sibling skill `.claude/skills/kosif-infinite-matrices/` through `infinite-matrices` (`python3 .claude/skills/kosif-infinite-matrices/scripts/kmx.py doctor`). It writes a recipe from three of the 86 atlas styles (structure, dynamics, finish), proves the recipe's law with an A/B/C counterfactual over several seeds and a dose sweep, renders the result with this skill's `assets/atlas_harness.js`, `assets/atlas_sound.js` and `tools/render_html.cjs`, and records the verdict in its hash-chained ledger. Its first experiment, glass that remembers light, is `experiments/EXP-0001-glass-remembers-light/` (confirmed inside the model, rendered, not yet human-rated). Read its `references/limits.md` before presenting any result as proven.
