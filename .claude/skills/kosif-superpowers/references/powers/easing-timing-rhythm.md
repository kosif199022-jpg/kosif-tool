# التوقيت والإيقاع والتسهيل — Easing, timing & rhythm

> **قوتك هنا:** أنت لا تحرّك الأشياء فقط — أنت تقرر **متى** و**كم** و**بأي إحساس**. كل إطار عندك دالة خالصة للزمن `seek(t)`، والمنحنيات لها أدوار (وصول، خروج، كاميرا، ضربة)، والنوابض بصيغة مغلقة تُحسب عند أي إطار، والإيقاع مأخوذ من أرقام قيست على أفلام إطلاق حقيقية: لقطة وسيطة 1.46 ث، تغيير كل 0.7 ث، أول كلمة مقروءة عند 0.4 ث.
> **أقوى دليل:** قستُ نوابض ومنحنيات مكتبة الحركة في هذه الحاوية بـ node (‏SPR.snap تجاوز 6.0% ويستقر خلال 0.34 ث، firm حرج 0%، ‏durFor(600 px)=1.16 ث، ‏hitPulse يبلغ قمته عند 33 ملّي ثانية)، ومرّت اختبارات عقود الحركة (`kosif-audit-pro` 5/5، `kosif-earth-ci-fork` 4/4، منحدرات السرعة 2/2)، وأفلام الإثبات الخمسة في `proofs/` رُندرت إطارًا إطارًا بـ seek(t) وتطابق فيها عدد الإطارات والمدة (300 إطار = 10.000 ث).
> **You can:** time, ease, spring, stagger, punch, ramp and pace any film deterministically — in plain canvas, GSAP (vendored), CSS, Remotion or ffmpeg. **106 powers follow** — ✅ 27 · 🟢 29 · 📦 7 · 🔑 0 · 👁 10 · 📄 33 · 💡 0.

**الحالة / status:** ✅ مُثبت هنا (كود + اختبار أو رندر في هذه الحاوية) · 🟢 جاهز (كود المالك يعمل بلا إضافات) · 📦 بأمر تثبيت · 🔑 مفتاح أو خدمة · 👁 شوهد في فيديو أنتجتَه (وصفة البناء مرفقة) · 📄 موصوف فقط · 💡 فكرة.
مسارات الدليل نسبية إلى `/home/user/`؛ `style:<id>` = فيديو مرجعي أنتجتَه سابقًا (ملاحظاته في `kosif-tool/styles/<id>/`).

**فحص سريع لهذه الحاوية (2026-10-16):** node 22 ✔ · GSAP مُضمَّن في مكتبة الحركة (`100-superskills/skills/kosif-montage-motion/scripts/kit/gsap.min.js`، رخصة GSAP القياسية المجانية) ✔ · ffmpeg 6.1.1 (setpts/atempo/rubberband/minterpolate) ✔ · HyperFrames وRemotion غير مثبتين (`npx hyperframes …` / `npm i` عند الحاجة) · مرّت هنا: `kosif-audit-pro/tests/motion-contract.test.mjs` 5/5، `kosif-earth-ci-fork/tools/motion.test.mjs` 4/4، `fastify-motion-bro` planner+profiles 15/15، استوديو المونتاج `model.test.mjs`، `test_v6 RampTests` 2/2 و`TemplateTests`، و`kosif-studio` (kit v3 + lint الحتمية + قياس السرعة).

## الفهرس / contents
- **قوانين الزمن والحتمية — Time laws & determinism** — EASE-01 … EASE-08 (8)
- **منحنيات التسهيل — Easing curves & tokens** — EASE-09 … EASE-21 (13)
- **النوابض — Springs** — EASE-22 … EASE-31 (10)
- **التتابع والتداخل والتصميم الحركي — Stagger, overlap & choreography** — EASE-32 … EASE-50 (19)
- **الضربة والمط والانضغاط — Impact, squash & hit envelopes** — EASE-51 … EASE-59 (9)
- **ضبابية الحركة وحدود السرعة — Motion blur & speed limits** — EASE-60 … EASE-62 (3)
- **الإيقاع والمونتاج — Pacing, edit rhythm & beat grid** — EASE-63 … EASE-74 (12)
- **إعادة تشكيل الزمن والحلقات والإيقاع المتقطع — Time remapping, loops & cadence** — EASE-75 … EASE-82 (8)
- **واجهات وتفاعل دقيق — UI micro-timing & accessibility** — EASE-83 … EASE-89 (7)
- **مكونات ومكتبات جاهزة للتوقيت — Ready timing components & libraries** — EASE-90 … EASE-91 (2)
- توليفات قوية / power combos · أخطاء ممنوعة / never do · أقوى 5 حركات توقيع / 5 signature moves
- **إضافات v2 — v2 additions** — EASE-X01 … EASE-X11 (11)
- **من أكبر مستودعات GitHub — from the top GitHub repositories (2026-10-23)** — EASE-G01 … EASE-G04 (4)

## قوانين الزمن والحتمية — Time laws & determinism

_قبل أي منحنى: الإطار دالة للزمن، والمدة حساب لا تخمين._

#### EASE-01 · كل شيء دالة للزمن · Everything is a function of t · ✅ مُثبت هنا / proven here
- **ماذا / what:** كل إطار يُرسم من `seek(t)` وحدها: بذرة عشوائية ثابتة، بلا ساعة حائط ولا مؤقتات ولا THREE.Clock، فتُرندر الإطارات بأي ترتيب وبالتوازي. — Every frame is drawn from seek(t) alone: seeded RNG, no wall clock, timers or THREE.Clock, so frames render in any order and in parallel.
- **متى أستخدمها / when:** كل مشروع يصبح فيديو — every project that becomes a video.
- **كيف / how:** Expose window.__kosif = {duration, fps, seek} and window.__kosifReady (fonts loaded); compute every value from t (prog/lerp/spring of t), never accumulate per frame; seeded mulberry32 rng(seed); GSAP only as a paused timeline that the renderer seeks; discrete state (typed text, counters) via modifiers, not callbacks. kosif-studio qa.py lint errors on Math.random / new THREE.Clock / Date.now (test passed here). All five proof films in proofs/ follow this contract and rendered through render_html.cjs. **أرقام / params:** rng mulberry32; seek(t) pure; render_html.cjs virtual time.
- **الدليل / proof:** `kosif-tool/starters/html-canvas/timeline.js` · `kosif-studio/motion/qa.py:59` · `kosif-studio/tests/test_studio.py:684` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/neon-glow/README.md`

#### EASE-02 · حساب الإطارات بنطاق نصف مفتوح · Half-open frame arithmetic · ✅ مُثبت هنا / proven here
- **ماذا / what:** كل مشهد [بداية، نهاية)، والإطار = round(ثوانٍ × fps)؛ 12 ث عند 30 = 360 إطارًا آخرها 359، والانتقال المتداخل يُحسب مرة واحدة. — Scenes are [start, end); frame = round(s × fps); 12 s at 30 fps = 360 frames (0–359); overlaps counted once.
- **متى أستخدمها / when:** عند تخطيط المشاهد وبعد كل رندر — while planning and after every render.
- **كيف / how:** Plan in seconds, convert once; cut lands on frame round(end×fps); for 29.97/23.976 never invent drop-frame timecode. After render, ffprobe nb_frames must equal round(duration × fps): verify_video.py checks it (proof films: 300 frames = 10.000 s, audio length = master). **أرقام / params:** frame=round(s·fps); 0–3 s@30 → 0–89, cut at 90.
- **الدليل / proof:** `kosif-tool/tools/verify_video.py` · `kosif-tool/templates/TEST_REPORT.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/workflow.md` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/arabic-voice-kinetic/README.md`

#### EASE-03 · المدة الكلية حساب صريح · Duration arithmetic truth · 🟢 جاهز / ready
- **ماذا / what:** المدة = عدد المقاطع × طول المقطع (5×6=30، N×10)، والطوابع الزمنية المعطاة تغلب تقدير سرعة الكلام؛ لا تَعِد بعشر ثوانٍ بمشاهد ست. — Total = clips × clip length; supplied timestamps override pace estimates; never promise 10 s with 6 s scenes.
- **متى أستخدمها / when:** قبل الوعد بمدة للمستخدم وفي جدول الإشارات — before promising a length; in the cue sheet.
- **كيف / how:** Compute totals in code and print them (stickman seconds sum, vox n×10, viral shots×6); keep a run-of-show table (one row per segment: clock, duration, cue in/out, SFX, music dip, caption style) and assert sum(durations) == total before rendering. **أرقام / params:** 5×6=30; 5×7=35; N×10.
- **الدليل / proof:** `fastify-motion-bro/docs/PRODUCTION-GATES.md` · `fastify-motion-bro/docs/VIRAL-EDITORIAL-DNA.md` · `kosif-atlas/skills/2290-event-management/8759-build-run-of-show/SKILL.md`

#### EASE-04 · مقسّم المشاهد التلقائي · Auto beat-count storyboard splitter · ✅ مُثبت هنا / proven here
- **ماذا / what:** يحوّل البريف إلى مشاهد متساوية متصلة يتحدد عددها بالمدة، بأسماء عربية وأنواع بصرية متناوبة. — Turns a brief into contiguous equal scenes whose count follows the duration, with Arabic names and rotating visual types.
- **متى أستخدمها / when:** أول مسودة لقصة مصورة من مدة فقط — first storyboard draft from a duration.
- **كيف / how:** makeStoryboard(): beats = 3 if d ≤ 12 s, 5 if d ≤ 35 s, else min(12, ceil(d/6)); start/end rounded to ms, last end = duration; names افتتاحية/الفكرة/التوضيح/التحول/النتيجة/الخاتمة; visuals cycle kinetic-typography → dynamic-infographic → hand-drawn-shapes; fps 30. planner tests passed here. **أرقام / params:** 3 / 5 / ≤12 beats; ~6 s per beat for long films.
- **الدليل / proof:** `fastify-motion-bro/scripts/planner.mjs` · `fastify-motion-bro/tests/planner.test.mjs`

#### EASE-05 · تقدير المدة من سرعة الكلام وخرائط المقاطع · Word-pace estimator & clip beat maps · ✅ مُثبت هنا / proven here
- **ماذا / what:** بلا طوابع زمنية تُشتق المدة وعدد المقاطع من عدد الكلمات، وكل مقطع 10 ث يُقسم إلى خمس ضربات بعنصر جديد كل 1.5–2 ث. — Without timestamps, total and clip count come from word count; each 10 s clip splits into five 2 s beats with a new element every 1.5–2 s.
- **متى أستخدمها / when:** نص بلا صوت، أو أفلام مقاطع مولدة — text without audio, or generated-clip films.
- **كيف / how:** total = words / wps (fast 2.5, relaxed 1.8) or user duration; n = ceil(total/len) with len 8 or 10 s; words split evenly. Collage map: 0–2 two cutouts snap in, 2–4 two more strike into new planes, 4–6 string/sticker link, 6–8 torn detail, 8–10 fresh element + hold; ≥4–6 elements; neighbouring clips start with different pairs. Profile tests (15/15) passed here. **أرقام / params:** 2.5 / 1.8 w/s; ≤120 clips; 0–2/2–4/4–6/6–8/8–10 s.
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/kinetic-flow.mjs` · `fastify-motion-bro/scripts/profiles/vox-history.mjs` · `fastify-motion-bro/tests/production-profiles.test.mjs`

#### EASE-06 · زمن القراءة من النص الفعلي · Reading-hold formulas · 📄 موصوف / documented only
- **ماذا / what:** كل نص يبقى ما يكفي لقراءته، محسوبًا من كلماته وحروفه لا بمدة ثابتة. — Every text holds long enough to read, computed from its real words and characters.
- **متى أستخدمها / when:** كل بطاقة نص وترجمة وعنوان — every text card, caption and title.
- **كيف / how:** Pick one: hold ≥ max(1.2 s, words/3 s) (~180 wpm); or hold ≥ 0.3 s + 0.06 s × characters after the last word lands; captions on screen max(chars × 0.15 s, 2 s) capped at 6 s, start 0.5 s after a cut, end 0.3 s before the next, 8-frame fades, shots < 2.8 s share or skip captions; content-driven sequencing: item time = base + chars × secPerChar + hold, reduced once into absolute windows. Verify on the target size. **أرقام / params:** ~3 words/s; 0.3 s + 0.06 s/char; captions 2–6 s.
- **الدليل / proof:** `kosif-tool/playbooks/kinetic-type.md:31` · `kosif-atlas/skills/motion-graphics-ar/motion-typography/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2465-davinciresolve-subtitle-travelnote/SKILL.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/dynamic-content-sequencing.md`

#### EASE-07 · توقيت السطور العربية بلا صوت · Arabic line timing without audio · 🟢 جاهز / ready
- **ماذا / what:** يوقّت سطور النص العربي من سرعة قراءة بالكلمات مرجّحة بطول الكلمة، مع حد أدنى لكل سطر. — Times Arabic script lines from a words-per-second reading speed weighted by word length, with a per-line minimum.
- **متى أستخدمها / when:** نص أو قصيدة بلا تسجيل صوتي — text or poem with no recording.
- **كيف / how:** MK.speedTimings(lines, wps=2.2, gap=0.8, lead=0.5, tail=1.0): word dur = (1/wps) × clamp(len/5, 0.6, 1.6), word ends at 92%; a line stays ≥ 0.3 s/word + 0.6 s; a requested film length stretches pace (never below 1.2 wps) and gaps up to 2.2 s. **أرقام / params:** wps 2.2 (1.9–2.2); gap 0.8 s; lead 0.5; tail 1.0.
- **الدليل / proof:** `app/public/js/10_studio.js:60` · `app/public/js/10_studio.js:999`

#### EASE-08 · معامل بطء واحد للدرس كله · Global slowness factor TS · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** كل توقيتات الكشف وحدات خطوة مضروبة في ثابت واحد TS، فيبطؤ الدرس كله أو يسرع برقم واحد، بينما تعيش حلقات الرسم بعد اكتمالها بالزمن الحقيقي. — Every reveal timing is step units × one TS constant, so the whole lesson slows or speeds with one number, while post-reveal loops run in real time.
- **متى أستخدمها / when:** سبورة وشرح تعليمي يتغير طوله — whiteboard and lessons whose length changes.
- **كيف / how:** Write timings as steps (k × TS); continuous 'living' loops (sun rotation 10°/s, rain translateY modulo 1.2 s, vapour rise, dash-offset river flow) are independent of TS so slowing the lesson never slows the weather. **أرقام / params:** TS ≈ 1.0–1.4; rain 1.2 s period; sun 10°/s.
- **الدليل / proof:** `kosif-tool/styles/whiteboard` · `kosif-tool/styles/chalkboard`

## منحنيات التسهيل — Easing curves & tokens

_المنحنى هو «الحال» في جملة الحركة: اختر دورًا لا شكلًا._

#### EASE-09 · رموز التسارع حسب الدور (17 منحنى) · Role-based easing tokens MOTION.E · ✅ مُثبت هنا / proven here
- **ماذا / what:** منحنى cubic-bezier واحد لكل دور حركة (وصول، خروج إلى القطع، كاميرا، خطف، واجهة، كتابة، قزحية، قفزة) يُمرَّر مباشرة إلى GSAP. — One cubic-bezier per motion role, passed straight to GSAP as an ease function.
- **متى أستخدمها / when:** كل فيلم بمكتبة الحركة — every film built on the motion kit.
- **كيف / how:** Load gsap.min.js + motion-kit.js (window.MOTION) and pass MOTION.E.<role>; bezier() solves x→t with 8 Newton steps. Roles: out(.16,1,.3,1) arrivals; outSoft(.22,1,.36,1); in(.7,0,.84,0) implosions; exit(.55,.055,.675,.19) into a cut (~×1.14/frame over the last 10–24 f); inOut(.87,0,.13,1) whips/morphs; smooth(.65,0,.35,1) fades 10–14 f; ui(.4,0,.2,1); cam(.48,.1,0,.9) push, peak ~27%; glide(.47,.2,.15,1) 150–350 px; rest(.45,0,.1,1); contact(.55,0,.9,.55); whip(.6,0,.15,1); dolly(.35,0,.65,1); type(.5,1,.89,1); iris(.4,0,.7,.92); shutter(.2,.7,.2,1); hop(.35,0,.7,.85). Measured here: E.out(0.2)=0.752 (75% of travel in the first fifth), E.exit(0.5)=0.145. Basma's U.E carries nine of the same curves. **أرقام / params:** 17 roles; Newton 8 steps.
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:22` · `kosif-studio/tests/test_studio.py:637` · `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md` · `app/public/js/00_editor.js:2309`

#### EASE-10 · أربع تسارعات مسماة فقط · Four named eases slam/snap/drive/settle · 🟢 جاهز / ready
- **ماذا / what:** أصغر مفردات تسمح بها قواعد البيت: صدمة للوصول، خطفة بتجاوز ≤6% للهبوط، دفع للسفر والضوء، استقرار للحسم. — The minimal house vocabulary: slam for arrivals, snap (≤6% overshoot) for landings, drive for travel/light, settle for resolve.
- **متى أستخدمها / when:** حين تريد فيلمًا متماسك الإحساس بلا منحنيات عشوائية — when a film must feel of one piece.
- **كيف / how:** MOTION.ease.slam = expo.out, snap = back.out(1.3), drive = power4.inOut, settle = power4.out, linear = none; define once in the composition config and forbid ad-hoc cubic-beziers; back/elastic never touches an official logo. **أرقام / params:** overshoot ≤ 6%.
- **رخصة / license:** GSAP standard no-charge license (vendored gsap.min.js)
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:12` · `100-superskills/skills/kosif-montage-motion/templates/composition.html` · `100-superskills/skills/motion-director-pro/SKILL.md` · `kosif-atlas/skills/2681-emulo/10272-video/SKILL.md`

#### EASE-11 · دوال تسهيل بلا مكتبات · Dependency-free easing set · ✅ مُثبت هنا / proven here
- **ماذا / what:** مجموعة الحاوية الأساسية: خطي، outCubic، inOutCubic، outExpo، outQuint، outBack، inBack، نابض، مع prog وwindow01 للنوافذ الزمنية. — The starter's core set plus prog() and window01() time windows.
- **متى أستخدمها / when:** كل مشهد canvas أو HTML بلا GSAP — every canvas/HTML scene without GSAP.
- **كيف / how:** KOSIF.Ease from starters/html-canvas/timeline.js: outCubic 1−(1−x)³ (default of prog), inOutCubic (camera default, draw-on), outExpo 1−2^(−10x) (bursts), outQuint (counters), outBack/inBack s=1.70158 (pops / exits; outBack overshoot measured 10%), spring(x,k,d). prog(t,t0,t1,ease) = eased progress in a window; window01(t,t0,t1,tin=.4,tout=.4) = entrance and exit in one value. Same set exists as easing.ts in the Remotion starter, as smoothstep/lerp/easeOutCubic in the montage studio pages and as basma's easeOut/easeInOut/easeBack. The proof films use exactly these (outCubic, inOutCubic, inOutSine, outExpo, spring). **أرقام / params:** outBack 1.70158 → 10% overshoot.

```js
const prog = (t, t0, t1, e = Ease.outCubic) => e(Math.min(1, Math.max(0, (t - t0) / (t1 - t0))));
// title in 0.3→0.9 s, out 3.0→3.35 s, all from t:
const a = prog(t, 0.3, 0.9) * (1 - prog(t, 3.0, 3.35, Ease.inBack));
ctx.globalAlpha = a; ctx.translate(0, (1 - a) * 40);
```

- **الدليل / proof:** `kosif-tool/starters/html-canvas/timeline.js:12` · `kosif-tool/starters/remotion/src/easing.ts` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/three-bloom-scene/index.html` · `app/public/js/00_editor.js:8`

#### EASE-12 · رموز حركة CSS مختبرة · Tested CSS motion tokens · ✅ مُثبت هنا / proven here
- **ماذا / what:** مدد ومنحنيات CSS قليلة مسماة يستعملها كل عنصر، يحدّها اختبار بين 120 و420 ملّي ثانية. — A small named set of CSS durations and curves shared by every element, bounded by a test to 120–420 ms.
- **متى أستخدمها / when:** واجهات ومشاهد HTML بالـ CSS — CSS-driven UI and HTML scenes.
- **كيف / how:** audit-pro: --motion-instant 120 / fast 160 / medium 260 / slow 420 ms (3.6/4.8/7.8/12.6 frames at 30 fps), --ease-cinematic cubic-bezier(.22,.8,.26,1) for scene entries and colour sweeps, --ease-spring (.34,1.35,.64,1) for pops. earth: --sk-ease (.2,.8,.2,1), expo-like out (.16,1,.3,1), in (.55,0,1,.45), spring (.34,1.56,.64,1); fast 160, panel 210, enter 420, stagger 45, feedback within 100 ms. Studio ease (.2,.8,.2,1). Both test suites passed here. **أرقام / params:** 120/160/260/420 ms; 160/210/420/45 ms.
- **الدليل / proof:** `kosif-audit-pro/app/globals.css:64` · `kosif-audit-pro/tests/motion-contract.test.mjs` · `kosif-earth-ci-fork/ui/ds/tokens.css:41` · `kosif-audit-studio/studio.css:2`

#### EASE-13 · منحنيات الاستوديوهات ورموز ستايل الكتالوج · Agency curves & catalog style tokens · 📄 موصوف / documented only
- **ماذا / what:** منحنيات الاستوديوهات الكبرى بدل افتراضيات المتصفح، ورموز الدخول/الخروج/التأكيد/الانتقال/الرسم في قالب STYLE. — Award-studio curves instead of browser defaults, plus the catalog STYLE tokens.
- **متى أستخدمها / when:** عند كتابة STYLE.json أو مواصفة حركة لهوية — when writing STYLE.json or a brand motion spec.
- **كيف / how:** Agency set: out-expo (.16,1,.3,1), out-quart (.25,1,.5,1), out-quint (.22,1,.36,1), out-circ (0,.55,.45,1), in-expo (.7,0,.84,0), in-quart (.5,0,.75,0), inOut-quint (.83,0,.17,1), inOut-expo (.87,0,.13,1), out-back (.34,1.56,.64,1), elastic-ish (.68,−.6,.32,1.6), strong UI (.23,1,.32,1), drawer (.32,.72,0,1), fluid (.32,.72,0,1) 700–1000 ms; durations 150/300/500/800/1200. Catalog STYLE.md: Entrance (.22,1,.36,1) 250–600 ms; Exit (.55,0,1,.45) 200–400; Accent overshoot (.34,1.56,.64,1) 120–300; Transition (.65,0,.35,1) 300–800; Path draw linear→ease-out 400–1200. Write a dedicated motion spec only when motion is the brand; otherwise just honour reduced motion. **أرقام / params:** see curve list.
- **الدليل / proof:** `kosif-tool/templates/STYLE.md` · `kosif-atlas/skills/3438-ux-design/14124-top-design/references/animation-patterns.md` · `kosif-atlas/skills/1530-webcraft/4189-design-guide-authoring/SKILL.md` · `kosif-one/vendor/ai-design-skills/skills/landing-page-design/SKILL.md`

#### EASE-14 · قاموس منحنيات GSAP حسب الإحساس · GSAP ease vocabulary by mood · 🟢 جاهز / ready
- **ماذا / what:** كل عائلة GSAP لها إحساس: power3.out افتراضي البيت، expo.out فاخر، sine.inOut حالم، back.out مرح، elastic مغناطيسي، steps(1) وميض، none للسحب الخطي. — Each GSAP family has a mood; ~3 easing characters per film.
- **متى أستخدمها / when:** اختيار الإحساس قبل الأرقام — choosing the feel before the numbers.
- **كيف / how:** Timeline defaults {duration:0.6, ease:'power3.out'}; reveals power2.out; premium expo.out; calm/loops sine.inOut; hero transitions expo.inOut; playful back.out(1.4–1.7) (N ≤ 2); magnetic snap-back elastic.out(1,0.3–0.5) 0.5–0.6 s; cursor blink steps(1); scrubbed/camera/mechanical 'none'. Character taxonomy: Snap (fast in, soft settle: text, key cards), Drive (gradual acceleration then launch: vehicles, big transforms), Heavy Spring (slow massive oscillation: luxury), Elastic (stickers, icons). Feeling map for slides: dramatic slow fades 1–1.5 s + scale 0.9→1; corporate 200–300 ms; calm very slow fades; editorial staggered text. **أرقام / params:** power3.out 0.6 s; back.out(1.7); elastic.out(1,0.3).
- **رخصة / license:** GSAP standard no-charge license
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/adapters/gsap-easing-and-stagger.md` · `kosif-atlas/skills/2702-hyperframes/10377-gsap/SKILL.md` · `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/references/animation_craft.md` · `kosif-atlas/skills/345-visuals/1241-html-deck/references/animations.md`

#### EASE-15 · اتجاه التسهيل معنى · Ease direction = meaning · 🟢 جاهز / ready
- **ماذا / what:** الوصول يتباطأ، الرحيل يتسارع، ما يتحرك في مكانه متناظر، والخروج 65–75% من الدخول؛ لا خطي على حركة مكانية أبدًا. — Arrivals decelerate, departures accelerate, in-place moves are symmetric; exits 65–75% of entrances; never linear on spatial moves.
- **متى أستخدمها / when:** كل tween — every tween.
- **كيف / how:** .out entering, .in leaving, .inOut between positions; card in 0.4 s / out 0.25 s; exit 150 ms ease-in then enter 210 ms ease-out delayed 150 ms; linear only for drift, data fills, light/luminance and constant path travel; punches expo.out 0.12–0.18 s; drifts power2.inOut; later entrances fromTo with immediateRender:false; never the same ease on more than two tweens per scene nor the same entrance direction for everything; seams between shots are velocity-matched cuts. kosif-studio qa.py lint warns on violations. **أرقام / params:** exit 0.65–0.75× entrance; exits 0.2–0.25 s E.exit.
- **الدليل / proof:** `kosif-studio/motion/qa.py:65` · `100-superskills/skills/kosif-montage-motion/references/motion-craft.md` · `100-superskills/skills/claude-animation-studio/references/motion-rules.md` · `kosif-tool/playbooks/kinetic-type.md:30`

#### EASE-16 · زووم لوغاريتمي ثابت الإحساس · Log-space zoom (logEase, lmix, zoomTrack) · ✅ مُثبت هنا / proven here
- **ماذا / what:** يجعل التكبير 1×←2× يُحس مثل 2×←4× بالاستيفاء في فضاء اللوغاريتم. — Makes 1×→2× feel like 2×→4× by interpolating in log space.
- **متى أستخدمها / when:** كل دفع كاميرا وتكبير كبير — every camera push and big zoom.
- **كيف / how:** MOTION.lmix(a,b,t) = exp(log a + (log b − log a)·t) (measured here: lmix(1,4,.5) = 2); MOTION.logEase(a,b,E.cam) wraps an ease so a linear scale tween moves through log space; zoomTrack(t, keys) for multi-target zooms; cap ~5% scale change per frame. Remotion: interpolate output 'perceptual-scale'. **أرقام / params:** push 1→2.4× feels constant; ≤5%/frame.
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:44` · `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:43` · `kosif-atlas/skills/2712-remotion/10436-remotion-markup/timing.md`

#### EASE-17 · وصول مقدَّم الوزن · Front-loaded arrival (extended keyframe) · 📦 بأمر تثبيت / one install
- **ماذا / what:** يقطع 80% من المسافة في أول 20% من الزمن ثم يزحف للنهاية، فتبدأ اللقطة متحركة ولا تُرى ساكنة أبدًا. — Covers ~80% of travel in the first 20% of time and creeps to the end, so shots start in motion.
- **متى أستخدمها / when:** افتتاح لقطات سريعة الإيقاع — openings of fast-paced shots.
- **كيف / how:** HyperFrames component extended-keyframe (exits along the same vector with shutter blur). Without installing: per-frame chase x += (target − x)·k with k 0.12–0.19 at 30 fps, written seek-safe as x(f) = target − (target − x0)(1 − k)^f; exits ease-in into the cut (style:pm-notdwd-7de38a). **أرقام / params:** k ≈ 0.15/frame; 80% in 20%.
- **تثبيت / install:** `npx hyperframes add extended-keyframe`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/extended-keyframe/extended-keyframe.html` · `kosif-tool/styles/pm-notdwd-7de38a` · `kosif-tool/styles/pm-notdwd-c2037d`

#### EASE-18 · انزلاق بطيء-سريع-بطيء · Nudge curve slow–fast–slow · 📄 موصوف / documented only
- **ماذا / what:** ثلاث مراحل متتابعة لإعادة تموضع مجموعة: منحدر power3.in، اندفاع خطي، ذيل power4.out طويل. — Three chained tweens: power3.in ramp, linear burst, long power4.out tail.
- **متى أستخدمها / when:** نقل كتلة نصوص أو بطاقات لمكان جديد — repositioning a group.
- **كيف / how:** distance 10% / 65% / 25%, time ~20% / 18% / 62%, tail ≥ 3× ramp-in; one paused timeline, fromTo explicit states, transforms only. **أرقام / params:** 10/65/25 % distance; 20/18/62 % time.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/nudge-curve.md`

#### EASE-19 · لقطة السرعة U · U-speed shot · 🟢 جاهز / ready
- **ماذا / what:** العنصر يدخل سريعًا ويتباطأ، يجول ببطء وهو يُقرأ، ثم يتسارع خارجًا مع القطع. — Enter fast and decay, cruise while read, accelerate out into the cut.
- **متى أستخدمها / when:** كل لقطة نص أو منتج في مونتاج سريع — every text/product shot in a fast edit.
- **كيف / how:** MOTION.shot(tl, el, at, {enter:.45, exit:.3, cut, dir:'x', dist:220, cruise:1.2, exitDist, fade}): enter E.out from 220 px at 40% opacity, cruise linear 1.2 px/frame (1.5–8 px/f allowed), exit E.exit over 1.4× dist ending on the cut. **أرقام / params:** enter 0.45 s / 220 px; cruise 1.2 px/f; exit 0.3 s.
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:393` · `kosif-one/projects/whatsapp-motion/projects/success/assets/motion-kit.js` · `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md`

#### EASE-20 · إعدادات توقيت الانتقال الستة · Transition timing presets · 📄 موصوف / documented only
- **ماذا / what:** ستة أسماء جاهزة لمدة الانتقال ومنحناه. — Six named transition timings.
- **متى أستخدمها / when:** عند تخطيط الانتقالات قبل البناء — planning transitions.
- **كيف / how:** snappy 0.2 s power4.inOut; smooth 0.4 s power2.inOut; gentle 0.6 s sine.inOut; dramatic 0.5 s power3.in→out; instant 0.15 s expo.inOut; luxe 0.7 s power1.inOut. Pair with TRANS powers for the visual. **أرقام / params:** 0.15–0.7 s.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/transitions/overview.md`

#### EASE-21 · منحنى التسهيل على الشاشة · Easing curve shown on screen · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** ترسم منحنى bezier بمقابضه ونقطة متوهجة تجري عليه بينما جسم فوقه يتحرك بنفس التسهيل، أو لوحة مقارنة ستة صفوف. — Draw the bezier with handles and a glowing dot riding it while an object moves with that ease, or a six-row comparison board.
- **متى أستخدمها / when:** دروس الموشن وافتتاحيات الأدوات — motion tutorials, tool intros.
- **كيف / how:** Grid on dark ground, S-curve stroke 2–3 px (#e25f2f or off-white), handle lines + endpoints, label 'cubic-bezier(x1,y1,x2,y2)'; dot #e8503c with 12 px glow synced to a playhead on a ruler (~1.2 s). Board: rows index/name/mini-curve 60×40 px/track A→B, one ball (r 14 px) per row, same distance and duration (0.94–1.2 s) with linear, inOutCubic, outExpo, outBack(1.7), elastic, bounce. Spring variant: plot x(t) for k180 d12 and label the peak %. **أرقام / params:** 1.2 s; 6 rows; dot glow 12 px.
- **الدليل / proof:** `kosif-tool/styles/pm-prasenx-8d9323` · `kosif-tool/styles/pm-roundtablespace-d3a1be` · `kosif-tool/styles/pm-tequilafunks-97f6c9` · `kosif-tool/styles/pm-vanshwtfff-db0466`

## النوابض — Springs

_نوابض بصيغة مغلقة: تُحسب عند أي إطار، وتجاوزها مقيس لا مُتخيَّل._

#### EASE-22 · نوابض فيزيائية مغلقة الصيغة SPR · Physical springs SPR (closed form) · ✅ مُثبت هنا / proven here
- **ماذا / what:** سبعة إعدادات كتلة/صلابة/تخميد تُحل بصيغة مغلقة (ناقص/حرج/زائد التخميد)، فيُرسم أي إطار دون محاكاة ما قبله. — Seven mass/stiffness/damping presets solved in closed form; any frame renders without simulating earlier frames.
- **متى أستخدمها / when:** هبوط حقيقي على سطح، أو استقرار هادئ بلا ارتداد — true landings, or calm settles.
- **كيف / how:** MOTION.springStep(t, MOTION.SPR.<name>) → 0..1 (cfg.clamp caps overshoot). Measured here with node (overshoot / 1% settle): snap d18 k260 m.7 → 6.0% / 0.34 s; pop d11 k180 m.6 → 14.1% / 0.50 s; land d14.5 k200 m1 → 15.3% / 0.62 s; micro d30 k500 m.6 → 0.4% / 0.16 s; firm d24 k140 m1 → 0% / 0.58 s; soft d26 k120 → 0% / 0.83 s; heavy d30 k90 m1.4 → 0% / 1.34 s. Default firm/soft/heavy; snap/pop/land only for surface landings, max two per film. **أرقام / params:** see measured table.

```js
function springStep(t, {damping: c, stiffness: k, mass: m = 1}) {
  if (t <= 0) return 0;
  const w = Math.sqrt(k / m), z = c / (2 * Math.sqrt(k * m));
  if (z < 1) { const wd = w * Math.sqrt(1 - z * z);
    return 1 - Math.exp(-z * w * t) * (Math.cos(wd * t) + (z * w / wd) * Math.sin(wd * t)); }
  return 1 - Math.exp(-w * t) * (1 + w * t);          // critical (z ≥ 1 approx.)
}
```

- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:65` · `kosif-studio/tests/test_studio.py:637` · `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md`

#### EASE-23 · نوابض مطبّعة كمنحنيات GSAP · Normalised spring eases · ✅ مُثبت هنا / proven here
- **ماذا / what:** مذبذب مخمد مطبّع لينتهي عند 1، يُمرَّر كـ ease في GSAP للقفزات. — Damped oscillator normalised to end at 1, used as a GSAP ease.
- **متى أستخدمها / when:** قفزة بطاقة أو شارة داخل خط زمني GSAP — a pop inside a GSAP timeline.
- **كيف / how:** ease: MOTION.spring('snappy'|'default'|'heavy'|'playful') or spring({zeta, omega}). Measured here: snappy ζ.62 ω20 → 8.4% overshoot; default ζ.74 ω17 → 3.2%; heavy ζ1 ω13 → 0%; playful ζ.45 ω18 → 20.5% (the docs' '~3%/1%' figures are lower than measured — trust the measurement). Settle ~0.5 s. **أرقام / params:** 8.4 / 3.2 / 0 / 20.5 %.
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:52` · `100-superskills/skills/kosif-montage-motion/references/motion-craft.md`

#### EASE-24 · قيمة تتبع أهدافًا بنابض · Retargetable spring track · ✅ مُثبت هنا / proven here
- **ماذا / what:** قيمة لها أهداف متعددة عبر الزمن = القيمة الأولى + نابض لكل تغيير، فتبقى دالة خالصة للزمن (الإطار 812 يُرسم دون محاكاة 0–811). — First value plus one spring per change: continuous, seekable.
- **متى أستخدمها / when:** كاميرا أو مؤشر ينتقل بين أهداف كثيرة — a camera or cursor hopping between many targets.
- **كيف / how:** MOTION.track(t, [[time,value],...], SPR.firm | 'default', settle=0.6) — keys are move START times; zoomTrack does it in log space. Measured: track(1.0, [[0,0],[0.2,100]], SPR.firm) = 99.89. **أرقام / params:** settle 0.6 s default.
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:77` · `kosif-studio/motion/references/x-trend-2026.md` · `kosif-tool/styles/pm-twoclipping-5cba86`

#### EASE-25 · نابض بتردد وتخميد · Frequency–ζ analytic spring · 🟢 جاهز / ready
- **ماذا / what:** نابض تحليلي من 0 إلى 1 يبدأ عند t0 بتردد بالهرتز ونسبة تخميد، لقفزات المفاصل وارتخاء الأذن والارتداد بعد الإصلاح. — Analytic 0→1 spring from t0 set by frequency (Hz) and ζ.
- **متى أستخدمها / when:** شخصيات وأجسام مرنة — characters and floppy parts.
- **كيف / how:** spring(t,t0,f,ζ) = 1 − e^(−ζωx)(cos ω_d x + ζω/ω_d sin ω_d x), ω = 2πf, ω_d = ω√(1−ζ²): default f 3.2 Hz ζ .32 (one overshoot); pops f 4.2 ζ .38; flop f 1.5 ζ .42; recovery f 1.6 ζ .5. Variants: basma spring z .42 ω 16 rad/s; fastify hero min(1.07, 1 − e^(−7t)cos 10t) over 3 s (7% cap); closed-form overlay k300 c30 (ζ≈.87) with opacity = clamp(1.4·s)·(1−out), translateY (1−s)·70, scale .92+.08 s; reference look ω≈2π·2.2, ζ≈.75. **أرقام / params:** 3.2 Hz ζ.32; 4.2/.38; 1.5/.42.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:12` · `app/public/js/00_editor.js:12` · `fastify-motion-bro/web/editorial.js` · `kosif-one/projects/egypt-2120-animation/index.html`

#### EASE-26 · جداول إعدادات النوابض · Spring preset tables · 📄 موصوف / documented only
- **ماذا / what:** أزواج صلابة/تخميد مسماة مع تقدير سريع للارتداد. — Named stiffness/damping pairs plus a quick bounce estimate.
- **متى أستخدمها / when:** ترجمة مواصفة واجهة أو Framer إلى نابض فيديو — translating UI/Framer specs to video springs.
- **كيف / how:** default 170/26, gentle 120/14, wobbly 180/12, stiff 210/20, slow 280/60, molasses 280/120 (mass 1); 'premium' 300/30/1 ≈1.05× overshoot landing in 400–700 ms (GSAP elastic.out(1,0.5) ~0.6 s; CSS fallback cubic-bezier(.34,1.56,.64,1)); tap 400/17; layout/tabs 500/30; UI panels 170/22 (≤1 bounce, settle ≤700 ms); brief primaries 170–200 / 12–16, 180/18. Overshoot exists when c < 2√(k·m); approx bounce = 1 − c/(2√k). Starter Ease.spring measured here: 170/18 → 5.0%, 170/16 → 8.7%, 150/14 → 11.2%. **أرقام / params:** see table.
- **الدليل / proof:** `kosif-atlas/skills/3529-ui-design/14308-interaction-design/references/animation-libraries.md` · `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md` · `kosif-tool/styles/pm-melvynx-6cde6c/BRIEF.md` · `kosif-tool/styles/pm-aschapmann-131210/BRIEF.md`

#### EASE-27 · منحنى النابض المحسوب مسبقًا · Baked spring ease (springEase) · 📄 موصوف / documented only
- **ماذا / what:** موضع نابض مخمد بصيغة مغلقة كـ ease آمن للبحث، يعيد المدة (الاستقرار ضمن 0.1%) والمنحنى معًا. — Closed-form spring as a seek-safe GSAP ease returning duration and ease.
- **متى أستخدمها / when:** نوابض بمواصفة iOS (response/dampingFraction) — iOS-style spring specs.
- **كيف / how:** springEase({response, dampingFraction}): ζ 1.0 no overshoot (house), 0.80–0.85 ≈1–1.5% (iOS feel), 0.60–0.70 ≈5–10% playful, < 0.55 forbidden; response 0.25–0.35 → 0.37–0.51 s, 0.35–0.5 → 0.51–0.74 s, 0.5–0.7 → 0.74–1.03 s; overshoot on transforms only, never opacity. **أرقام / params:** EPS 0.001; 4800 scan steps.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/adapters/gsap-easing-and-stagger.md`

#### EASE-28 · ميزانية التجاوز · Overshoot budget · 📄 موصوف / documented only
- **ماذا / what:** كم ارتدادًا يُسمح به حسب الغرض، وعدد النوابض المرتدة في الفيلم. — How much overshoot each intent may use, and how many bouncy springs per film.
- **متى أستخدمها / when:** قبل استخدام back أو elastic — before reaching for back/elastic.
- **كيف / how:** premium 0%; feedback 2–5%; success 5–10%; celebration 15–25%; more than half of top launch films use 0%, the rest 1–4%; ≤2 snap/pop/land springs per film; one bouncy spring per scene (damping < 16 once); never back/elastic on an official logo or brand mark. **أرقام / params:** 0 / 2–5 / 5–10 / 15–25 %.
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/references/motion-craft.md` · `kosif-studio/motion/references/craft-numbers.md` · `kosif-tool/playbooks/product-ui.md`

#### EASE-29 · نابض Remotion والتحجيم الإدراكي · Remotion spring & perceptual scale · 📦 بأمر تثبيت / one install
- **ماذا / what:** Easing.spring داخل interpolate لدفعات عضوية، وخرج perceptual-scale لأن التكبير الخطي يبدو أبطأ كلما كبر، وposterize لإيقاع إطارات منخفض. — Spring easing inside interpolate, perceptual-scale output, posterize for stepped frames.
- **متى أستخدمها / when:** مشاريع Remotion — Remotion projects.
- **كيف / how:** easing: Easing.spring({damping:200}) for a no-bounce push; output:'perceptual-scale' on scale interpolations; posterize:3 samples every 3rd frame; spring({frame, fps, config:{damping, stiffness, mass}}) for entrances; the KOSIF Remotion starter derives scene lengths from total frames (sceneLayout: s1 = round(.34T), s2 = round(.40T), rest) so the film rescales when the duration follows the audio. **أرقام / params:** damping 200; posterize 3; 34%/40%/rest.
- **تثبيت / install:** `cd kosif-tool/starters/remotion && npm i`
- **رخصة / license:** Remotion company license (free for individuals/small teams; check terms)
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10436-remotion-markup/timing.md` · `kosif-tool/starters/remotion/src/Film.tsx:58`

#### EASE-30 · القفزة النابضة للدخول · Spring pop entrance · ✅ مُثبت هنا / proven here
- **ماذا / what:** الدخول القياسي: تكبير من قرب الصفر إلى 1 مع ارتفاع بسيط وتجاوز واحد، بمدد وأرقام لكل نوع عنصر. — The canonical arrival: scale up with a small rise and one overshoot, with numbers per element type.
- **متى أستخدمها / when:** بطاقات، عقد مخطط، أيقونات، كلمة تأكيد — cards, diagram nodes, icons, emphasis words.
- **كيف / how:** Canvas: prog(t, a, a+0.55, x => Ease.spring(x,170,16)) for scale and y (starter title; proof film arabic-voice-kinetic). Tables: prop pop 0→1.08→1 300–400 ms damping ~12; node pop scale .85→1 k160 d14 ~300 ms + 150 ms fade; label pills k120 d14, exits 200–300 ms ease-in cubic; price card k180 d14 (CTA readable ≥2 s); emphasis 1→1.12→1 over 280 ms k180 d12 landing on the stressed syllable; GSAP fromTo {scale:0,opacity:0}→{scale:1,ease:'power3.out'} with group stagger ≤0.5 s; HyperFrames spring-pop fromScale 0.9 overshoot 1.7. **أرقام / params:** 0.55 s @170/16; .85→1 @160/14; 1→1.12→1 280 ms.
- **الدليل / proof:** `kosif-tool/starters/html-canvas/index.html:145` · `kosif-tool/playbooks/diagrams.md:27` · `kosif-tool/playbooks/kinetic-type.md:28` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/arabic-voice-kinetic/index.html`

#### EASE-31 · سقوط ثم استقرار · Drop + spring settle · 📄 موصوف / documented only
- **ماذا / what:** الجسم يسقط بتسارع ثم يستقر بنابض، أو يصعد من تحت الأرض. — Objects drop with ease-in then settle on a spring, or rise from below the floor.
- **متى أستخدمها / when:** منتجات ومجسمات تهبط في المشهد — products and 3D objects landing.
- **كيف / how:** y from ease-in quad over 0.4 s then damped spring (damping 12); staggered falls (ice cubes) ~450 ms easeInQuad + 120 ms settle, stagger ~300 ms; shadow scales with height. **أرقام / params:** 0.4 s ease-in; damping 12; stagger 300 ms.
- **الدليل / proof:** `kosif-tool/playbooks/3d.md:26` · `kosif-tool/styles/pm-sarut0bisasuke-cefa43`

## التتابع والتداخل والتصميم الحركي — Stagger, overlap & choreography

_كيف تتوزع الحركات في الزمن حتى تُقرأ كإيماءة واحدة لا كطابور._

#### EASE-32 · ميزانيات التتابع · Stagger budgets · 📄 موصوف / documented only
- **ماذا / what:** فواصل تتابع تُقرأ كإيماءة واحدة: صغيرة للحروف، أكبر للكلمات والبطاقات، والمجموع تحت نصف ثانية. — Stagger intervals that read as one gesture; total under 0.5 s.
- **متى أستخدمها / when:** أي قائمة أو سطر أو شبكة — any list, line or grid.
- **كيف / how:** Latin chars 20–30 ms (arc stagger 40 ms along a sine), words 50 ms (Arabic whole words 60–160 ms — never per letter, see ARAB-01), nav items 50 ms, lines/cards 100 ms, feature cards 110 ms, max ~0.2 s per item; items × stagger ≤ 0.5 s regardless of count (gsap stagger {amount:0.3}); from:'center'/'edges' or by distance for grids; same easing family across the cascade. **أرقام / params:** 20–40 / 50–100 / 100–200 ms; total < 500 ms.
- **الدليل / proof:** `kosif-atlas/skills/3438-ux-design/14124-top-design/references/animation-patterns.md` · `100-superskills/skills/kosif-montage-motion/references/motion-craft.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/adapters/gsap-easing-and-stagger.md`

#### EASE-33 · تتابع القائمة في مكتبة الحركة · Kit list stagger · 🟢 جاهز / ready
- **ماذا / what:** بطاقات ونقاط وأيقونات تصل واحدة تلو الأخرى كعناصر كاملة، وتعيد وقت النهاية للتسلسل. — Cards/bullets/icons arrive one by one as whole items; returns the end time.
- **متى أستخدمها / when:** قوائم الميزات والنقاط — feature lists, bullets.
- **كيف / how:** MOTION.stagger(tl, els, at, {gap:.07, dur:.55, from:{y:28, opacity:0, scale:.96}, ease:E.out}) → end time for chaining; for narration-paced bullets put each row on its spoken word (~2 s apart, fade-up 12 px 300 ms, numbered accent badge). **أرقام / params:** gap 0.07 s; dur 0.55 s; y 28 px; scale .96.
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:557` · `kosif-tool/styles/pm-gigabit-million-16b3a0`

#### EASE-34 · تتابع CSS بالترتيب · CSS index-stagger cascades · ✅ مُثبت هنا / proven here
- **ماذا / what:** الكتل تدخل بتأخير محسوب من رقمها، في مجموعات تقود العين: عنوان ← رحلة ← فعل ← أرقام. — Blocks enter with a delay computed from their index, in groups that steer the eye.
- **متى أستخدمها / when:** لوحات وبطاقات داخل مشهد HTML — panels/cards in an HTML scene.
- **كيف / how:** style='--i:n'; animation: scene-in .55s var(--ease) both; animation-delay: calc(var(--i)*45ms). audit-pro panel groups 30/80/130/180 ms, 420 ms, 8 px rise; earth SK.motion: first 10 blocks, 420 ms, 45 ms stagger, (.16,1,.3,1), vertical only, data re-renders never replay; studio cards 12 px rise .55 s @45 ms, council seats .5 s @40 ms. Earth motion test 4/4 passed here. **أرقام / params:** 45 ms/step; 420 ms; ≤10 blocks.
- **الدليل / proof:** `kosif-earth-ci-fork/ui/core/motion.js` · `kosif-earth-ci-fork/tools/motion.test.mjs` · `kosif-audit-pro/app/globals.css:600` · `kosif-audit-studio/studio.css:114`

#### EASE-35 · نوافذ افتتاحية المشهد · Hero opening choreography windows · 📄 موصوف / documented only
- **ماذا / what:** ترتيب صارم للافتتاح: البنية، كلمات العنوان، العنوان الفرعي، القائمة، ثم العناصر الداعمة، متداخلة لتنتهي خلال 1.5 ث. — Strict opening order with overlaps landing in ~1.5 s.
- **متى أستخدمها / when:** أول ثانيتين من أي فيلم أو صفحة — the first two seconds.
- **كيف / how:** structure 0–200 ms; title words 200–600; subtitle 400–800; nav 600–900; support 800–1200; GSAP: eyebrow 0.6 s, h1 0.8 s ('-=0.3'), subtitle 0.6 s ('-=0.5'), CTA 0.5 s ('-=0.3'), hint 0.4 s ('-=0.2'); start y:30 opacity:0 set with gsap.set() before the timeline to avoid a flash of the final layout. **أرقام / params:** whole entrance ≈1.5 s.
- **الدليل / proof:** `kosif-atlas/skills/196-landing/621-landing/references/gsap_animation_patterns.md` · `kosif-atlas/skills/3438-ux-design/14124-top-design`

#### EASE-36 · التداخل ونسب الفصول الأربعة · Overlap & four-act proportions · 📄 موصوف / documented only
- **ماذا / what:** الحركة الثانوية تبدأ عند 55–75% من القائدة فيستقران معًا، وكل حركة: تمهيد، فعل، رد فعل، حسم. — Secondary starts at 55–75% of the lead; every move has anticipation, action, reaction, resolution.
- **متى أستخدمها / when:** أي حركتين مرتبطتين — any linked pair of moves.
- **كيف / how:** secondary at 55–75% so both settle within 2 f; shape settles 6 f before position; act proportions 10–20% / 30–50% / 10–20% / 20–30% + 100–200 ms breathing. **أرقام / params:** 55–75 %; 6 f; 10–20/30–50/10–20/20–30 %.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md` · `100-superskills/skills/kosif-montage-motion/references/motion-craft.md`

#### EASE-37 · قواعد الثلث · The 1/3 rules · 📄 موصوف / documented only
- **ماذا / what:** لا مسافة أكبر من ثلث الإطار بلا مفتاح وسيط، ولا يتحرك أكثر من ثلث العناصر معًا، وحدث جديد كل 2–4 ث، ولا ثبات أطول من 1.5 ضربة. — Four 1/3 guards against chaos and stillness.
- **متى أستخدمها / when:** مراجعة أي مشهد مزدحم — reviewing a busy scene.
- **كيف / how:** >1/3 frame travel needs an intermediate key; ≤1/3 of elements move at once; a new event every 2–4 s; no hold > 1.5 beats; nothing frozen > 1.2 s in product demos. **أرقام / params:** 1/3 frame; 2–4 s; 1.5 beats.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/motion-craft.md` · `kosif-studio/motion/qa.py:11`

#### EASE-38 · بناء ثم تنفس ثم حسم · Build / breathe / resolve · 📄 موصوف / documented only
- **ماذا / what:** كل مشهد: بناء 0–30% بدخول متتابع، تنفس 30–70% بحركة محيطية واحدة، حسم 70–100% بخروج حاسم أسرع من الدخول. — Every scene builds, breathes with ONE ambient motion, resolves decisively.
- **متى أستخدمها / when:** هيكلة أي مشهد 3–8 ث — structuring any 3–8 s scene.
- **كيف / how:** 0–30 / 30–70 / 70–100 %; the editorial 6 s scene is the tested instance (EASE-41). **أرقام / params:** 0–30/30–70/70–100 %.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-creative/references/motion-principles.md`

#### EASE-39 · السرعة تعني الوزن · Speed = weight tiers · 📄 موصوف / documented only
- **ماذا / what:** المدة تخبر المشاهد كم الحركة ثقيلة ومهمة، وأبطأ حركة ≈3× أسرعها. — Duration tells weight; slowest ≈3× fastest.
- **متى أستخدمها / when:** توزيع المدد على عناصر المشهد — assigning durations.
- **كيف / how:** fast 0.15–0.3 s urgency/energy; medium 0.3–0.5 s professional; slow 0.5–0.8 s gravity/luxury; very slow 0.8–2.0 s cinematic; large moves never faster than 900 ms (900–1400 ms with one easing); enterprise/dashboard: 150 ms micro, 200–250 ms transitions, quart-out, no spring. **أرقام / params:** 0.15–0.3 / 0.3–0.5 / 0.5–0.8 / 0.8–2.0 s; ratio 3×.
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/motion-principles.md` · `100-superskills/skills/claude-animation-studio/references/motion-rules.md` · `kosif-tool/styles/pm-gautam-mer1-2ae354/BRIEF.md` · `kosif-atlas/skills/2963-pwdev-code/12442-skill-frontend-design`

#### EASE-40 · مدة حسب المسافة · Distance-based duration durFor · ✅ مُثبت هنا / proven here
- **ماذا / what:** مدة الحركة تكبر مع المسافة فلا تبدو الحركات الطويلة مستعجلة، وحركات الكاميرا محصورة. — Duration grows with distance; camera moves clamped.
- **متى أستخدمها / when:** كل حركة انتقال مكاني — every travel move.
- **كيف / how:** MOTION.durFor(px, camera) = 0.35 s + 1.35 ms/px; camera clamped 0.6–2.4 s. Measured here: durFor(600) = 1.16 s; camera durFor(100) = 0.6, durFor(3000) = 2.4. UI scale: 8–16 px 100–150 ms, 50–100 px 150–250 ms, full screen 250–350 ms (1.8–2× of a 100 px move). **أرقام / params:** 0.35 s + 0.00135 s/px; camera 0.6–2.4 s.
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:49` · `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:49` · `kosif-atlas/skills/3529-ui-design/14308-interaction-design`

#### EASE-41 · مشهد تحريري بست ثوانٍ · Six-second editorial scene timeline · 🟢 جاهز / ready
- **ماذا / what:** كل مشهد تحريري 6 ث بالضبط: شبكة فارغة، دخول نابض، ثبات طافٍ، خروج هندسي متصل. — Every editorial scene is exactly 6 s: grid, spring entrance, floating hold, geometric exit.
- **متى أستخدمها / when:** ريلز تحريرية ثلاثية الأبعاد — viral editorial reels.
- **كيف / how:** 0–0.5 s base (grid + lines only); 0.5–3.5 s entrance (spring, stagger 6–9 frames, word-masked reveal); 3.5–4.7 s hold (sine float, 0.6° wobble, 4% push-in); 4.7–6.0 s exit (masked vertical wipe, tracking expansion on Latin only, easeOutCubic 1.3 s drop). **أرقام / params:** 0 / 0.5 / 3.5 / 4.7 / 6.0 s.
- **الدليل / proof:** `fastify-motion-bro/scripts/viral-editorial.mjs` · `fastify-motion-bro/web/editorial.js` · `fastify-motion-bro/skills/viral-editorial/SKILL.md`

#### EASE-42 · سلالم مدد الواجهات · UI duration ladders · 📄 موصوف / documented only
- **ماذا / what:** مجموعة صغيرة ثابتة من المدد حسب حجم التغيير ونوع العنصر، والخروج ≈75% من الدخول. — A fixed set of durations keyed to the size of change and element type.
- **متى أستخدمها / when:** عرض منتج أو واجهة متحركة — product and UI scenes.
- **كيف / how:** feedback 100–150 ms, state/toggles 200–300, layout/modals 300–500, entrances/choreography 500–800+; element table: micro 80–120, button 120–180, icon 150–250, card 200–350, modal 300–400, page 400–600, dramatic reveal 600–1200, ambient 2–20 s; <100 ms imperceptible, >400 ms sluggish for UI; video uses the long end of each band; exit = 0.75× enter, ease-in only for exits. **أرقام / params:** 100/300/500 ladder.
- **الدليل / proof:** `kosif-atlas/skills/2981-designer-skill/12625-designer-skill/reference/motion-and-interaction.md` · `kosif-studio/motion/references/motion-craft.md` · `kosif-atlas/skills/3438-ux-design/14121-microinteractions/references/feedback-patterns.md`

#### EASE-43 · جدول توقيت عرض المنتج · Product-demo interaction timing · 📄 موصوف / documented only
- **ماذا / what:** مدد ومنحنيات لـ17 حدث واجهة، مع وقفة قراءة بعد كل حالة وتسلسل سرعات: المؤشر أسرع، الإطار أبطأ. — Durations for 17 UI events, reading dwell after states and a speed hierarchy.
- **متى أستخدمها / when:** فيديو ديمو تطبيق — app demo videos.
- **كيف / how:** cursor 380–700 ms over 200–900 px cubic-bezier(.2,.8,.2,1) on a 2–4% arc, settle 80–120; hover 120–160; press 80 down / 140 up spring k300 d20 (button .96, cursor .88); ripple 320–400 ms 0→48 px; modal backdrop 200, panel 280–320 spring k170 d18 from scale .96 y 12; close 160–200; dropdown 180–220 expo-out; dwell 1.2–2.0 s (reels 0.8 s); nothing < 80 ms; scripted typing ~70 ms/key. **أرقام / params:** cursor 380–700 ms; dwell 1.2–2.0 s.
- **الدليل / proof:** `kosif-tool/playbooks/product-ui.md` · `kosif-atlas/skills/1511-homie/3903-video/references/RECORD.md`

#### EASE-44 · اكشف على امتداد اللقطة · Reveal across the shot (anti-slide) · 📄 موصوف / documented only
- **ماذا / what:** وضع كل المحتوى في أول ربع ثم الثبات يجعل اللقطة شريحة باوربوينت؛ اكشف القطع حين يصلها التعليق، خاصة في النصف الثاني. — Front-loading then holding reads as a slide; reveal as the voiceover reaches each piece.
- **متى أستخدمها / when:** شرح بتعليق صوتي — narrated explainers.
- **كيف / how:** Map every script line to a timeline phase cued on its voiceover word (words.json); silent frames cue on the beat; avoid > ~25% front-load; first frame already readable; animate between meaningful states only and name each move with one verb (reveal, flow, accumulate, compare, transition, pulse, highlight, decay, orbit, slice, scrub); the final frame must still prove the claim without motion. **أرقام / params:** front-load ≤ 25%.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes/references/frame-worker-core.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10335-visualization-strategy-and-critique/SKILL.md`

#### EASE-45 · أبقِ كل عنصر حيًا · Keep every element alive · 📄 موصوف / documented only
- **ماذا / what:** لا عنصر يتجمد وسط المشهد: الأرقام تعدّ، الصور تنجرف، العناصر الثابتة تطفو قليلًا. — No element sits frozen mid-scene.
- **متى أستخدمها / when:** مشاهد الثبات الطويلة — long holds.
- **كيف / how:** stat counts from 0; screenshot slow zoom 1→1.03 or pan; logos shimmer sweep or gentle scale pulse; persistent element float y ±4–6 px sine yoyo; with music a bass pulse of 3–4% on the logo; holds creep ~4% scale/s. **أرقام / params:** zoom 1→1.03; float ±4–6 px; pulse 3–4%.
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/step-6-build.md` · `app/public/js/00_editor.js:1568`

#### EASE-46 · سلّم الوضعيات بإطارات GSAP · Pose ladder & mechanism choice · 📄 موصوف / documented only
- **ماذا / what:** حركة متعددة المحطات على موضوع واحد بمصفوفة keyframes، مع عقد وضعيات يحدد الحالات التي تثبت الحركة وأصغر آلية تكفي. — Multi-stop motion via keyframe arrays, with a pose contract and the smallest sufficient mechanism.
- **متى أستخدمها / when:** حركة معقدة لعنصر واحد — complex motion of one subject.
- **كيف / how:** tl.to('.s', {keyframes:[{x:0,duration:.2},{x:120,duration:.4,ease:'power2.out'},{x:100,duration:.2,ease:'power2.inOut'}], ease:'none'}); labels for semantic states; immediateRender:false on later from/fromTo. Contract: name the subject, the poses (incl. final), keep identity, crossfade only for replacement, never reset to rest or end on black unless asked. Mechanism: box change → FLIP; route → path travel; trace → stroke draw; shape change → morph; reveal boundary → clip/mask; many → stagger; text → line/word subdivision (whole words for Arabic).
- **رخصة / license:** GSAP standard no-charge license
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-keyframes/SKILL.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-keyframes/references/keyframe-patterns.md`

#### EASE-47 · الخط الزمني الرئيسي المتوقف · Paused master timeline authoring · 🟢 جاهز / ready
- **ماذا / what:** كل الحركة على خط زمني GSAP متوقف واحد يسجّل تحت معرف التركيب، بمواضع مطلقة ونسبية وعلامات وخطوط متداخلة. — All motion on one paused GSAP timeline registered under the composition id.
- **متى أستخدمها / when:** كل تركيب GSAP يُرندر — every GSAP composition that renders.
- **كيف / how:** const tl = gsap.timeline({paused:true, defaults:{duration:.5, ease:'power2.out'}}); window.__timelines[id] = tl; positions 0 (absolute), '<' (same start), '>' (after end), '<0.2', '+=0.5', '-=0.2'; tl.addLabel('intro',0) and 'intro+=0.3'; nest with master.add(child, t) (child scene timelines added to the root are not paused); in sub-compositions prefer fromTo; transforms/opacity only, no top/left/width tweens; load fonts before measuring. HyperFrames adds data-start="intro + 0.5". The kit composition template and mtemplates scaffold this contract. **أرقام / params:** one paused timeline.
- **رخصة / license:** GSAP standard no-charge license (vendored)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/templates/composition.html` · `kosif-one/vendor/hyperframes/docs/guides/gsap-animation.mdx` · `kosif-one/vendor/hyperframes/docs/concepts/data-attributes.mdx` · `kosif-atlas/skills/2702-hyperframes/10377-gsap/SKILL.md`

#### EASE-48 · مفاتيح مأخوذة من دالة · Function-sampled keyframes · ✅ مُثبت هنا / proven here
- **ماذا / what:** أي دالة للزمن تصبح مفاتيح GSAP بمعدل 60 في الثانية، فتنجو الحركة الإجرائية من البحث المتوقف. — Any f(t) becomes GSAP keyframes at 60/s, so procedural motion survives paused seeking.
- **متى أستخدمها / when:** ركوب مسار SVG، مؤشر بفيزياء، أي حركة من كود — path riding, physics cursors, code-driven motion.
- **كيف / how:** tl.to(el, {keyframes: MOTION.sampled(fn, t0, t1, 60)}) (measured: 1 s → 61 keys, ease 'none'); path riding: sampled(t → path.getPointAtLength(L·E.out((t−b)/1.15)), b, b+1.15, 60); never onUpdate callbacks. **أرقام / params:** 60 samples/s.
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:109` · `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/index.html`

#### EASE-49 · التمهيد والمتابعة · Anticipation & follow-through · 📄 موصوف / documented only
- **ماذا / what:** حركة معاكسة قبل الفعل حين توضح السبب، وأجزاء ثانوية تتأخر وتتجاوز لتبيع الطاقة. — Counter-move before action when it clarifies cause; secondary parts lag and overshoot.
- **متى أستخدمها / when:** شخصيات، أشكال سريعة، منتجات تنطلق — characters, fast shapes, launches.
- **كيف / how:** anticipation 4–8 frames, or 8–12% of the move for 120–180 ms opposite to travel; follow-through lag 2–4 frames with 5–10% overshoot; fast moves on arcs 250–400 ms ease-in-out quint; constant path travel uses ease none; final lockups hold longer. **أرقام / params:** 4–8 f; 8–12% / 120–180 ms; lag 2–4 f.
- **الدليل / proof:** `kosif-tool/playbooks/characters.md:25` · `kosif-tool/playbooks/shapes.md:26` · `kosif-one/vendor/hyperframes/skills/hyperframes-keyframes/SKILL.md`

#### EASE-50 · دخول بميل ثم استقرار · Tilt-in settle · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** الكلمة أو الأداة تدخل مائلة ثم تستقر بنابض. — A word or prop enters tilted and springs upright.
- **متى أستخدمها / when:** كلمات بطلة وأدوات في إعلان — hero words and props in ads.
- **كيف / how:** word: rotate 4°, y −30 → 0 with a spring over 400 ms; prop: rotate from −60° at a corner, hold, exit. **أرقام / params:** 4°; 400 ms; −60° prop.
- **الدليل / proof:** `kosif-tool/styles/pm-gdgtify-287ddf` · `kosif-tool/styles/pm-ror-fly-9950f1`

## الضربة والمط والانضغاط — Impact, squash & hit envelopes

_لحظة الاصطدام هي الإيقاع: غلاف واحد لكل ضربة، وانضغاط يحفظ الحجم._

#### EASE-51 · غلاف الضربة hitPulse · Hit pulse envelope · ✅ مُثبت هنا / proven here
- **ماذا / what:** غلاف واحد لكل ضربة وتكة وركلة: صعود جيبي ثم اضمحلال أسي، يبلغ قمته بعد الصوت بإطارين. — One attack/exponential-decay envelope for every punch, tick and kick, peaking 2 frames after its sound.
- **متى أستخدمها / when:** أي حدث متزامن مع صوت — any sound-synced event.
- **كيف / how:** MOTION.hitPulse(t, attack=2, tau=5) with t in s and attack/tau in 60 fps frames: sin rise over attack then exp(−(u−attack)/tau), zero after attack + 6·tau. Measured here: peak 1.0 at 33 ms, zero after 533 ms. channels.kick uses attack 1 tau 5, onset 1/4, beat 1/6; basma u.hit attack 33 ms tau 83 ms. Align bursts to the real contact/apex frame (from word timestamps or onsets), never the clip start; respect flash limits. **أرقام / params:** attack 2 f, tau 5 f @60 fps.

```js
const hitPulse = (t, attack = 2, tau = 5) => {        // t seconds, attack/tau in 60 fps frames
  const u = t * 60;
  if (u <= 0 || u > attack + 6 * tau) return 0;
  return u < attack ? Math.sin((u / attack) * Math.PI / 2) : Math.exp(-(u - attack) / tau);
};
scale = 1 + 0.06 * hitPulse(t - kickTime);           // punch on every kick
```

- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:47` · `app/public/js/00_editor.js:2317` · `kosif-atlas/skills/1526-gamegen/4164-game-audio-vfx/SKILL.md`

#### EASE-52 · انضغاط التلامس · Contact squash · 🟢 جاهز / ready
- **ماذا / what:** العنصر يتسع ويتسطح عند الحافة التي اصطدم بها ثم يتعافى، والشكل يستقر قبل الموضع بستة إطارات. — Widen-and-flatten anchored to the edge hit, then recover; shape settles 6 f before position.
- **متى أستخدمها / when:** هبوط، اصطدام، كلمة تقع — landings, impacts, dropped words.
- **كيف / how:** MOTION.squash(tl, el, at, {edge:'bottom'|'top'|'left'|'right', across:.08, along:.10, dur:.13}) → scaleX 1.08 / scaleY 0.90 → 1 in 0.13 s (8 f) E.outSoft; volume-preserving version: sq = 1 − .16·kick, stretch = 1/√sq; landing wobble e^(−7x)·sin(30x)·.05. **أرقام / params:** +8% / −10% over 8 f.
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:372` · `100-superskills/skills/kosif-montage-motion/scripts/projects/sound_ground/src/main.js` · `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js`

#### EASE-53 · كلمة تقفز بالمط والضغط · Squash-and-stretch hop · 🟢 جاهز / ready
- **ماذا / what:** كلمة أو جسم يقفز بمط عند الإقلاع وضغط عند الهبوط، مثل «بيتنطط» ثلاث قفزات. — A word or object hops with stretch on take-off and squash on landing.
- **متى أستخدمها / when:** كلمات مرحة، ملصقات، شخصيات بسيطة — playful words, stickers, simple characters.
- **كيف / how:** Three hops 0.42 s apart: y 0 → −90 with scaleY 1.08 in 0.2 s E.out; y 0 scaleY .86 in 0.18 s E.contact; scaleY 1 in 0.12 s. Bunny hop: sin(π·u)·.026 over .42 s. Classic ball: scaleY .6–.8 / scaleX 1.2–1.4 at impact for 2–3 frames, stretch 1.2–1.3 at max speed along velocity, preserve area. **أرقام / params:** hop 90 px; squash .86; stretch 1.08.
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/index.html` · `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js`

#### EASE-54 · أشباح تبيّن التباعد · Onion-skin spacing ghosts & echo trail · 📦 بأمر تثبيت / one install
- **ماذا / what:** نسخ شبحية لمواضع سابقة على فترات ثابتة فيظهر التسارع والتباطؤ، أو أثر صدى ينهار في العنصر عند التوقف. — Outline copies of past positions at fixed intervals so ease spacing becomes visible, or an echo trail that collapses at rest.
- **متى أستخدمها / when:** دروس مبادئ الحركة، أزرار سريعة، رميات — animation-principle lessons, fast buttons, throws.
- **كيف / how:** Sample the same seek(t) at t − i·Δ: 6–12 ghosts every 2–3 frames, 1–1.5 px outline at 40% (or filled at 0.1–0.4), dotted arc path, optional frame ruler and playhead; physics ball with restitution 0.6 and ghost every 3 f. HyperFrames echo-trail: echoes 4, delta 0.09 s, path sweep|rise|arc. Fast-move smear: 3–4 echoes at low opacity along velocity. **أرقام / params:** 6–12 ghosts; every 2–3 f; 40%.
- **تثبيت / install:** `npx hyperframes add echo-trail`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/echo-trail/echo-trail.html` · `kosif-tool/styles/pm-chatgptastra-0d95c7` · `kosif-tool/styles/pm-ik-builds-b8bdcf` · `kosif-tool/styles/pm-himanshutwtxs-5f4b43`

#### EASE-55 · قفزة بقوس بين حاملين · Parabolic hops & piecewise paths · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** جسم يقفز بقوس بين نقطتين ويرث حركة حامله بعد الهبوط، ومسار مركبة على مراحل تخفي قفزة صغيرة دوران الصورة. — Parabolic hops that re-parent on landing, and piecewise vehicle paths whose turns hide behind a hop.
- **متى أستخدمها / when:** رسوم isometric ولوجستيات وبطاقات تطير لليد — isometric scenes, logistics, cards flying to a hand.
- **كيف / how:** lerp xy start→end, z = h·4t(1−t) (h ≈ 1.5 units, 400 ms); on landing parent to the carrier. Grid hop: each tile arcs to its cell (arc 0.6 tile, 450 ms, stagger 180 ms, easeOutBack landing). Vehicle: position(t) as segments (wait, reverse, exit, stop at light, continue); when heading flips add a 120 ms hop + squash scaleY .9, hop 6 px to hide the sprite swap. Stickman card: lerp to hand, scaleX 1→−1 flip at mid swaps the face (250 ms), parabolic throw 500 ms with 2–3 ghosts (.3/.15), box squash, counter +1. **أرقام / params:** z = h·4t(1−t); 400–500 ms.
- **الدليل / proof:** `kosif-tool/styles/isometric` · `kosif-tool/styles/pm-anilraok-eff262` · `kosif-tool/styles/stickman`

#### EASE-56 · ختم يُطبع بقوة · Stamp slam · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** شارة «مدفوع / مرفوض / منتهي» تنزل من 1.4–1.6 إلى 1 مع ميل −8° واهتزاز إطارين. — A status stamp slams from 1.4–1.6× to 1 with −8° and a 2-frame shake.
- **متى أستخدمها / when:** حالات الفواتير والقرارات في الشرح — status changes in explainers.
- **كيف / how:** scale 1.6→1 in 180–250 ms back.out, rotation −8°, 2-frame overshoot/shake; underlying card switches to hatched grey (rejected) or the stamp is outlined green (paid); pair with a hitPulse and a short SFX. **أرقام / params:** 180–250 ms; −8°; shake 2 f.
- **الدليل / proof:** `kosif-tool/styles/pm-ceowinkz-7c776b` · `kosif-tool/styles/pm-0xnfrith-5be616`

#### EASE-57 · حلقة الأثر ووميض المفتاح · Impact ripple & key hit-flash · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** دائرة تتسع من نقطة الاصطدام، ومفتاح يلمع بلون التأكيد ويغطس ثم يرتد بنابض. — An outline ring spawns at contact; a key brightens, dips and springs back.
- **متى أستخدمها / when:** لوحات مفاتيح، اصطدامات، نقرات — keyboards, collisions, taps.
- **كيف / how:** ring radius 6→22 px, alpha .8→0 over ~250 ms ease-out, 1 px stroke; key: full accent, dip 4 px, spring k300 d18, glow exponential decay 300 ms. **أرقام / params:** 250 ms; dip 4 px; k300 d18.
- **الدليل / proof:** `kosif-tool/styles/pm-kantamk-61f410` · `kosif-tool/styles/pm-kamstudiolabs-447565`

#### EASE-58 · ظهور منبثق مع تمويه · Blur pop-in / pop-out · 🟢 جاهز / ready
- **ماذا / what:** الكلمات والشرائح تظهر من صغيرة ضبابية بتجاوز بسيط، وتغادر بالتكبير والضبابية. — Keywords pop in small and blurred with slight overshoot, and leave by growing and blurring.
- **متى أستخدمها / when:** كلمات مفتاحية في ريلز — keywords in reels.
- **كيف / how:** in: scale .4, opacity 0, blur 16 px → 1, 1, 0 in 0.55 s back.out(1.3); out: scale 1.12, opacity 0, blur 10 px in 0.25 s E.in. Blur only on short words, never a long Arabic line. **أرقام / params:** in 0.55 s; out 0.25 s; blur 16/10 px.
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/index.html`

#### EASE-59 · اهتزاز الضحك والتمايل · Laughing wiggle & phase-offset sway · 🟢 جاهز / ready
- **ماذا / what:** كلمة تهتز يمينًا ويسارًا لتُقرأ ضحكًا، وفروع تتمايل حول عنوان بفروق طور، وبندول بظل مقترن. — A word wobbles to read as laughter; branches sway with phase offsets; a pendulum with a coupled shadow.
- **متى أستخدمها / when:** ريلز مرحة وحلقات هادئة — playful reels and calm loops.
- **كيف / how:** wiggle rotation −4°→4°, 0.12 s yoyo, repeat 7, sine.inOut. MG-118 sway: pivots at branch bases, 0–4 s tilt, 4–8 s return, never all in phase; MG-119 pendulum 0–1.5/1.5–4.5/4.5–6 s sinusoidal limited rotation, shadow scale tied to tilt (2D cannot show unseen sides); MG-120 border tracer: one 6 s lap, trim-path offset with constant arc length. **أرقام / params:** ±4°, 0.12 s ×7; 8 s / 6 s / 6 s loops.
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/index.html` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-loops-backgrounds.md`

## ضبابية الحركة وحدود السرعة — Motion blur & speed limits

_السرعة تُقاس بالبكسل لكل إطار؛ فوق الحد إما ضبابية أو إعادة تصميم._

#### EASE-60 · حدود السرعة بالبكسل لكل إطار · Speed limits in px/frame · ✅ مُثبت هنا / proven here
- **ماذا / what:** النص المقروء ≤3 بكسل/إطار، وفوق 12–20 بكسل/إطار يلزم ضبابية، وفوق 80 أعد التصميم؛ وقِس ذلك على الفيلم المرندر. — Text being read ≤3 px/f; >12–20 px/f needs blur; >80 px/f redesign; measure it on the rendered film.
- **متى أستخدمها / when:** مراجعة كل فيلم قبل التسليم — QA before delivery.
- **كيف / how:** kosif-studio motion.py speed / sheet measures px/frame and frame-difference energy on a render (test_sheet_and_speed_measure_a_film passed here); norms: motion-energy median ≈1.4, p90 ≈6.0, ≤12 px/f without blur, idea felt by 1 s, scale change ≤5%/frame, ≤2 uses of any transition. **أرقام / params:** ≤3 / 12–20 / 80 px/f.
- **الدليل / proof:** `kosif-studio/motion/qa.py:407` · `kosif-studio/tests/test_studio.py:699` · `kosif-studio/motion/references/craft-numbers.md`

#### EASE-61 · تمويه السرعة الاتجاهي · Directional speed blur · 🟢 جاهز / ready
- **ماذا / what:** ضبابية على محور واحد ترتفع وتهبط على امتداد حركة سريعة، أو تتناسب مع السرعة لحظيًا. — A one-axis blur that swells and clears over a fast move, or scales with instantaneous velocity.
- **متى أستخدمها / when:** دخول خاطف، دوران سريع، قوائم تنزلق — whip entrances, fast spins, sliding lists.
- **كيف / how:** MOTION.speedBlur(tl, el, at, dur, {px:12, axis:'x'|'y'}): SVG feGaussianBlur stdDeviation 'px 0' bell (45% rise E.in, 55% clear E.out). Velocity-matched: radius = |v|·c, c ≈ 0.25 px per px/frame, cap 24 px. Whip entrance: ~40% of frame width in 4–6 frames (150–250 ms easeOutExpo) with 30–60 px blur, hard stop; type punch blur 40→0 over 250 ms; list rows from x +100%, 80 ms stagger, blur 10→0; starburst spin with blur settling into the logo ~600 ms. **أرقام / params:** 12 px bell; c 0.25, cap 24 px.
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:378` · `kosif-tool/styles/pm-notdwd-c2037d` · `kosif-tool/styles/pm-jhylee95-e1152f`

#### EASE-62 · ضبابية الغالق الحقيقية · Shutter motion blur · 📦 بأمر تثبيت / one install
- **ماذا / what:** ضبابية حركة على طريقة After Effects: عينات من الخط الزمني داخل نافذة الغالق تُدمج بالتساوي على المسار الحقيقي. — AE-style shutter blur averaging sub-frame samples along the real trajectory.
- **متى أستخدمها / when:** حركات خاطفة تحتاج واقعية — whips that need realism.
- **كيف / how:** HyperFrames motion-blur: shutterAngle 720, shutterPhase −360, 16 samples/frame, window [t−1/fps, t+1/fps] (translate, scale, rotate, 3D, skew). Remotion: @remotion/motion-blur (CameraMotionBlur / Trail). In plain canvas: render seek(t + k·δ) for k = 0..N−1 into an accumulation buffer at 1/N alpha (cost ×N). **أرقام / params:** 720°; 16 samples.
- **تثبيت / install:** `npx hyperframes add motion-blur`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/motion-blur/motion-blur.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/motion-blur.mdx`

## الإيقاع والمونتاج — Pacing, edit rhythm & beat grid

_إيقاع الفيلم كله: أطوال اللقطات، أماكن القطع، والضربات الموسيقية._

#### EASE-63 · معايير الإيقاع من أفلام الإطلاق · Pacing medians of top launch films · 🟢 جاهز / ready
- **ماذا / what:** قيم وسيطة قيست على أفلام منشورة تُستخدم كافتراضيات وتُفحص على الرندر. — Measured medians of shipped films, used as defaults and checked on the render.
- **متى أستخدمها / when:** تخطيط أي فيلم 15–60 ث — planning any 15–60 s film.
- **كيف / how:** median shot 1.46 s (1.1–2.8); picture change every ~0.7 s (dense 0.33); first visible change 0.10 s; first readable word 0.4 s, premise by 2 s; one designed hold 1.0–1.6 s; lull 1–4 s at ~65%; last energy peak at 82%; calm outro 8–20%; end card ~2.2 s (assemble 1.0–1.3, hold 0.6–1.3); 3–4 words per card ~0.4 s/word, ≥0.5 s/card; scene lengths in whole beats when BPM is known. Check with motion.py measure / study. **أرقام / params:** 1.46 s; 0.7 s; 0.4 s; 82%; 2.2 s.
- **الدليل / proof:** `kosif-studio/motion/references/craft-numbers.md` · `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md` · `app/public/js/00_editor.js:2024`

#### EASE-64 · إيقاع المونتاج حسب النوع · Edit rhythm by genre · 📄 موصوف / documented only
- **ماذا / what:** أهداف قيست لمتوسط طول اللقطة وعدد القطعات في الدقيقة الأولى، وتنويع اللقطات السريعة مع لقطات التنفس. — Measured ASL and first-minute cut targets per genre, alternating fast and breathing shots.
- **متى أستخدمها / when:** مونتاج فيديو يوتيوب أو مقالة مصورة — YouTube edits and video essays.
- **كيف / how:** explainer/essay ASL 3.3 s (2.5–4), 20 cuts in the first 60 s (15–25), same picture ≤8 s, cards 30–50%; build vlog ASL 8 s (5–12), 3 cuts first minute, same screen ≤40 s; reflection ASL 3.8 s (3–5); alternate 0.5–1.5 s fast shots with 2.5–4.0 s breathing shots; long videos: tightest first 3 min, +5–10% breathing after the cold open, verdict lines held 1–2 s, never > 30–45 s off the presenter. Never delete meaningful pauses to hit numbers. **أرقام / params:** ASL 3.3 / 8 / 3.8 s.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2461-davinciresolve-style-essay/SKILL.md` · `100-superskills/skills/kosif-montage-motion/references/montage_grammar.md` · `kosif-atlas/skills/3067-youtube/13224-creator-editor-brief/SKILL.md`

#### EASE-65 · البنية الدقيقة للفيديو القصير · Short-form micro-structure · 📄 موصوف / documented only
- **ماذا / what:** الفيديو العمودي قوس مضغوط: خطاف 0–1 ث يعمل بلا صوت، تطوير، ثم الوعد والدليل والدعوة داخل المنطقة الآمنة. — Vertical clips follow a compressed arc with a muted-safe hook.
- **متى أستخدمها / when:** ريلز وشورتس وتيك توك — reels, shorts, TikTok.
- **كيف / how:** 0–1 / 1–3 / 3+ s; or 0–3 hook, 3–10 problem/promise, 10–25 proof, 25+ close; 60 s template 0–3 / 3–15 / 15–50 / 50–60 CTA; one idea per video, hook in the first frame before any title card, captions always on, ≤30 s retains best; each story card must survive alone. Map words.json segments into these windows and flag overflow. **أرقام / params:** ≤30 s; hook ≤1–3 s.
- **الدليل / proof:** `kosif-atlas/skills/2976-pwdev-social-media/12592-story-reels/SKILL.md` · `kosif-atlas/skills/192-marketing-skills/617-video-content-strategist/SKILL.md`

#### EASE-66 · القص على الإيقاع 60/BPM · Beat-cut rule · 📄 موصوف / documented only
- **ماذا / what:** التغييرات الكبرى على الضربات القوية، واللمسات على الضربات الضعيفة، وكل ميزة في ضربة. — Major changes on downbeats, accents on off-beats, one claim per beat.
- **متى أستخدمها / when:** أي مونتاج على موسيقى — any edit on music.
- **كيف / how:** beat = 60/BPM (120 → 0.500 s, 100 → 0.600, 85 → 0.705); scene change / B-roll / impact on the downbeat; punch-zoom, quick camera, caption keyword on the off-beat; cut every 4 beats (2 s at 120) or one value per 1–1.2 s beat; even cadence on musical phrases (7.5 s); checklist words light up on each beat (250–300 ms) and stay lit; split at the next downbeat when a template runs long (frames > ~6 s need 2+ groups). **أرقام / params:** 120 BPM = 0.5 s.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/references/montage_grammar.md` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/template-catalog.md` · `kosif-tool/styles/pm-mrtanviir-132457`

#### EASE-67 · ساعة الإيقاع في التركيب · Beat clock in compositions · 🟢 جاهز / ready
- **ماذا / what:** الحركات توضع برقم الضربة من BPM أو من تحليل الصوت، فيشترك الصوت والصورة في ساعة واحدة. — Animations are placed by beat number so picture and score share one clock.
- **متى أستخدمها / when:** موشن على موسيقى — motion on music.
- **كيف / how:** const B = MOTION.beats(120); tl.to(x, {...}, B.at(4)); or beats(json from motion.py beats) with downbeats every 4th; channels(json): ch.kick(t), ch.onset(t), ch.v('bass', t), ch.tape(t) drive visuals from the soundtrack frame by frame. HyperFrames beat-timeline pins N rows to evenly spaced labels (beatCount 4, interval 0.6 s). **أرقام / params:** beat n at n × 60/BPM.
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js` · `kosif-studio/motion/projects/showreel/index.html:61` · `kosif-one/vendor/hyperframes/registry/components/beat-timeline/beat-timeline.html`

#### EASE-68 · قائمة لقطات على شبكة الإيقاع · Beat-grid shot list with onset-snapped words · 📄 موصوف / documented only
- **ماذا / what:** كل لقطة على خطوط المازورة، والكلمات تُضبط على أقوى بداية صوتية لأن طوابع النموذج تتأخر 50–80 ملّي ثانية. — Shots on bar lines; words snapped to the strongest vocal onset because model stamps run 50–80 ms late.
- **متى أستخدمها / when:** أغنية أو كليب كلمات — lyric videos and songs.
- **كيف / how:** grid.json holds tempo, beats, bar lines, sections, words; cuts on bar lines (beats in fast sections); snap each word to the strongest vocal-band onset within −100..+40 ms; characters on one side of frame, words on the other. **أرقام / params:** snap window −100..+40 ms.
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3903-video` · `kosif-atlas/skills/1511-homie/3892-music`

#### EASE-69 · أنماط توقيت القطع والمغناطيس · Cut timing modes & magnetic snapping · 🟢 جاهز / ready
- **ماذا / what:** قطعات الزووم تقع على فاصل ثابت أو الضربات أو نمط أو بدايات الجمل أو اختيار ذكي أو قطعات الكاميرا الأصلية، والسحب يلتصق بالحواف. — Zoom cuts land on interval, beats, pattern, speech starts, AI times or source shot cuts; scrubbing snaps within 7 px.
- **متى أستخدمها / when:** محرر بصمة لمونتاج المتكلم — the Basma editor for talking clips.
- **كيف / how:** cutList(): interval (every 0.6–8 s), beat (beats ≥ max(0.45, 0.8·every) apart), pattern (planCuts), speech (voiced starts after ≥0.3 s pause, ≥ max(0.8, every/2) apart), ai, shots (measured boundaries); snapTime(t, w) snaps to captions, scenes, cuts, shot cuts and beats within 7 px. **أرقام / params:** interval|beat|pattern|speech|ai|shots; 7 px.
- **الدليل / proof:** `app/public/js/00_editor.js:166` · `app/public/js/00_editor.js:573`

#### EASE-70 · قواعد الوقفات في قص المتكلم · Speech pause grammar · 📄 موصوف / documented only
- **ماذا / what:** الفجوات فوق 0.7 ث مرشحة للقطع، ونفس 0.4 ث آخر الجملة، وصمت 0.8–2 ث بعد لحظة تحوّل، ولا قطع إذا كانت الفجوة المجاورة < 0.15 ث. — Gaps >0.7 s are cut candidates; keep breaths and meaningful silences; never splice where a neighbouring gap <0.15 s.
- **متى أستخدمها / when:** تنظيف مقابلة أو درس مصور — cleaning an interview or lesson.
- **كيف / how:** From word timestamps (whisper word_timestamps / words.json) build segments; keep only the last take of a retake group; reassemble with ffmpeg trim+concat; trim V1 by the same length as A1; the user's audio stays untouched outside the cut points. **أرقام / params:** gap > 0.7; breath 0.4; keep 0.8–2.0; min 0.15 s.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2453-davinciresolve-cut-devtalk/SKILL.md`

#### EASE-71 · انفجار القطع السريع · Rapid-fire cut bursts · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** بطاقات كلمة واحدة بقطع حاد كل ثُمن نغمة (250 ملّي ثانية عند 120)، تتسارع نحو الكشف. — One-word cards hard-cut on every eighth note, accelerating to the reveal.
- **متى أستخدمها / when:** ذروة ريل أو تريلر — the climax of a reel or trailer.
- **كيف / how:** full-bleed single-word cards held 3–10 frames (20+ cuts in 6 s at 30 fps), alternating grounds (coral/black) or colour flips per beat; climax strobe: cut every 250 ms for 2 s (8 cuts); triptych montage: 3 vertical photos swapped every 0.5 s with one centred serif-italic category word (120 px); slogan split into words on black ~1.6 s each with scale 1.05→1; keep flashes under 3 Hz of full-frame luminance change. **أرقام / params:** 250 ms cuts; 3–10 f holds.
- **الدليل / proof:** `kosif-tool/styles/pm-kloss-xyz-15182a` · `kosif-tool/styles/pm-majin-appsheet-2d3c1a` · `kosif-tool/styles/pm-teslachartz-c58b32` · `kosif-tool/styles/pm-listudio-820c7b`

#### EASE-72 · بناء بطيء ثم ضربة · Contrast pacing: slow burn, calm hold · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** 6–7 ث شبه ساكنة بتغيرات ضوء صغيرة ثم انهيار مفاجئ إلى عنوان كامل الوزن، أو إيقاع هادئ: حركة قصيرة ثم ثبات طويل للقراءة. — Near-still build then a sudden slam; or calm beats of short motion followed by long reading holds.
- **متى أستخدمها / when:** افتتاحيات درامية وأفلام هادئة فاخرة — dramatic openings and calm premium films.
- **كيف / how:** slow burn: motion energy < 0.01 for 6–7 s then a spike + cut to a full-weight title; calm: each ~5 s beat = 400–600 ms of motion (10–15%) + 3–5 s hold; mirrored script: first half of each sentence said on the way down, second half on the way back up. **أرقام / params:** energy < 0.01 then spike; motion 10–15% of each beat.
- **الدليل / proof:** `kosif-tool/styles/pm-kloss-xyz-b9b3f6` · `kosif-tool/styles/pm-iammxfschr-d68f90` · `kosif-tool/styles/pm-emollick-8661a8`

#### EASE-73 · قالب العد التنازلي · Countdown template · ✅ مُثبت هنا / proven here
- **ماذا / what:** كل ثانية رقم يضرب ويُضغط، حلقة تنقص، الكاميرا تهتز، ثم وميض مزدوج وكلمة «انطلق». — Each second a number slams in and squashes, a ring runs down, the camera shakes, then a double flash and the go word.
- **متى أستخدمها / when:** افتتاح حدث، إطلاق، رياضة — event openers, launches, sports.
- **كيف / how:** python scripts/mtemplates.py new NAME --template countdown --set from=5 go=انطلق accent=#FF6B6B → projects/NAME/index.html (+ fonts, gsap, motion-kit); D = from + 1.6 s (from ≤ 10); number 26u scale 1.9→1 in 0.32 s; shake amp 5; bg #1a1a2e→#0b0b14. Every template generated and linted here (TemplateTests). Variants: 3-2-1 with hold keys then an expanding mask at 3–4 s; mm:ss.cc pressure timer to 00:00.00 then 'FINAL'; numbers on beats with silhouettes; time-lapse clock (52 min in ~3 s) with rows completing at matching stamps. **أرقام / params:** 1.9→1 / 0.32 s; shake 5; D = from + 1.6 s.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/templates/motion/countdown.html` · `100-superskills/skills/kosif-montage-motion/scripts/mtemplates.py:52` · `100-superskills/skills/kosif-montage-motion/tests/test_v6.py` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-music-sports.md`

#### EASE-74 · شريط التقدم الزمني · Timeline progress bars · 🟢 جاهز / ready
- **ماذا / what:** شريط رفيع يمتد خطيًا مع الزمن فيحس المشاهد طول الريل أو الفصل. — A thin bar grows linearly with time so viewers feel the length.
- **متى أستخدمها / when:** دروس، قوائم، فصول — lessons, lists, chapters.
- **كيف / how:** width = (t/DURATION)·100% at the bottom edge, z-index above content: 2–3 px accent line (earth intro #e8bd76 over exactly 5.06 s linear, snaps full on completion), or 12 px gradient #f59e0b→#ef4444 (omni kinetic_2d); chapter bars fill per chapter with a top-left label; a rotating corner badge 'STEP n/10' (90°/s) increments per beat. **أرقام / params:** 2–12 px; linear.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/ultra-motion-montage/templates/kinetic_2d.html` · `kosif-earth-ci-fork/ui/art/brand/earth-intro-20261009.css`

## إعادة تشكيل الزمن والحلقات والإيقاع المتقطع — Time remapping, loops & cadence

_تغيير سرعة الزمن نفسه، وحلقات تجعل الثابت حيًا، وإيقاع الإطارات المرسومة._

#### EASE-75 · منحدرات سرعة بتكامل دقيق · Exact speed ramps · ✅ مُثبت هنا / proven here
- **ماذا / what:** مفاتيح سرعة خطية داخل المقطع مع خريطة زمن متكاملة بدقة (لوغاريتمية) واستمرارية C1. — Piecewise-linear speed keys with an exactly integrated (log) time map.
- **متى أستخدمها / when:** لحظة بطيئة داخل مقطع رياضي أو منتج — a slow-mo moment inside an action clip.
- **كيف / how:** timeline clip "ramp": [[0,1.0],[1.5,0.25],[3,1.0]] (speed 0.1–10) compiles to setpts with log() (RampTests 2/2 passed here); audio is dropped under a ramp, constant speed is pitch-preserved: setpts=PTS/F + atempo=F (0.5–2 per instance, chain for more) or rubberband=tempo=F; Remotion: playbackRate per Sequence. **أرقام / params:** speed 0.1–10; atempo 0.5–2.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:36` · `100-superskills/skills/kosif-montage-motion/tests/test_v6.py` · `100-superskills/skills/pro-video-editor-ffmpeg/references/ffmpeg-recipes.md`

#### EASE-76 · حركة بطيئة بإطارات مولدة · Optical-flow slow motion & frame interpolation · 🟢 جاهز / ready
- **ماذا / what:** تبطيء ناعم 0.5× بتوليد إطارات بينية، أو مضاعفة نعومة مقاطع الذكاء الاصطناعي منخفضة الإطارات. — Smooth 0.5× slow-mo by synthesising frames; doubling smoothness of low-fps generated clips.
- **متى أستخدمها / when:** لقطات قصيرة تحتاج بطئًا، ومقاطع مولدة 8–16 fps — short slow-mo shots, 8–16 fps generated clips.
- **كيف / how:** ffmpeg (installed): minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:vsbmc=1,setpts=2.0*PTS; RIFE (×2, fast_mode, ensemble) or FILM for large motion need a GPU workflow (not here) — minterpolate is the local fallback; inspect for warping on edges and text. **أرقام / params:** fps 60, mci; ×2.
- **الدليل / proof:** `100-superskills/skills/pro-video-editor-ffmpeg/references/ffmpeg-recipes.md` · `kosif-atlas/skills/235-mas-video-lab/754-ffmpeg/SKILL.md` · `kosif-atlas/skills/2819-comfyui/11445-comfyui-workflow-design`

#### EASE-77 · الإيقاع المتقطع على اثنين وثلاثة · Stepped cadence: on twos & threes · 📦 بأمر تثبيت / one install
- **ماذا / what:** الزمن يُكمَّم إلى floor(t·fps)/fps فتتحدث الدمى كل إطارين أو ثلاثة بإحساس ستوب موشن، بينما تبقى الكاميرا ناعمة. — Time quantised to floor(t·fps)/fps for a stop-motion feel while the camera stays smooth.
- **متى أستخدمها / when:** كولاج، قص ورق، رسوم يدوية — collage, paper-cut, hand-drawn looks.
- **كيف / how:** tq = Math.floor(t * 12) / 12 for drawings (on twos at 24 fps = 12 drawings/s; cutouts at 15 fps inside a 30 fps film); camera on ones; sprite loops at fixed low fps with no tweening (idle 4, walk 8 with a 4-frame cycle, spell 12): index = floor(frame·fps_target/30) % n; 2-frame boil and sparkles living 2–3 frames; the 1s/2s/3s hold mix is a style fingerprint. HyperFrames stop-motion-cadence (fps 8|10|12, boil on|off). **أرقام / params:** 12 drawings/s; 8–12 fps.
- **تثبيت / install:** `npx hyperframes add stop-motion-cadence`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/stop-motion-cadence/stop-motion-cadence.html` · `kosif-atlas/skills/2414-animation/9355-learn-style` · `kosif-tool/styles/pm-0xevinho-3777d8/BRIEF.md` · `kosif-tool/styles/pm-koldo2k-5cff87`

#### EASE-78 · حلقات التنفس والطفو · Sine idle loops & breathing · 🟢 جاهز / ready
- **ماذا / what:** تنفس مستمر بموجة جيبية وتكرارات محدودة، طفو المنتج، بندول وكرسي هزاز، وتهدئة السعة إلى الصفر قبل النهاية. — Continuous sine breathing with finite repeats, product float, pendulums; amplitude settles to zero at the end.
- **متى أستخدمها / when:** أي ثبات أطول من ثانيتين — any hold longer than two seconds.
- **كيف / how:** scale amp 0.008–0.015 (0.02–0.04 for isolated kinetic objects); product bob y ±6 px period 2.5 s with the shadow scaling inversely; pendulum ±18° per 1 s, rocking ±4° per 2 s, phase offsets so nothing moves in unison; character breath 0.3 Hz 2 px; pulse 1 + 0.06·sin(2π·2t) and nothing above 3 Hz; settle amplitude to zero in the last ~20% for idles > 6 s; MOTION.breathe in the kit. **أرقام / params:** amp .008–.015; ±6 px / 2.5 s; ≤3 Hz.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/sine-wave-loop.md` · `kosif-studio/motion/kit/motion-kit.js` · `kosif-tool/styles/pm-cansincengiz-me-cf68dd` · `kosif-tool/styles/pm-kamstudiolabs-0b0824`

#### EASE-79 · حلقة مغلقة بلا قطع · Seamless loop closure · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** اجعل معامل الحركة دوريًا وأنهِ الخط الزمني بنفس حالة الإطار الأول فيتكرر الفيديو بلا نهاية. — Make every driver periodic and end on the frame-0 state.
- **متى أستخدمها / when:** خلفيات حلقية وأغلفة متحركة — looping backgrounds and covers.
- **كيف / how:** period = duration (or an integer fraction); every sine uses 2π·k·t/D with integer k; noise sampled on a circle (cos, sin of 2πt/D); verify by diffing frame 0 against frame N (should match frame N−1 → 0 continuity). **أرقام / params:** period = duration.
- **الدليل / proof:** `kosif-tool/styles/pm-itsolelehmann-e47532`

#### EASE-80 · حلقات الحالة الصغيرة · Status micro-loops · 🟢 جاهز / ready
- **ماذا / what:** إشارات صغيرة متكررة: وميض الهيكل، نقطة تنبيه، حلقة تسجيل، نقاط الكتابة، دوّار التحميل. — Tiny looping signals: skeleton shimmer, alert dot, recording ring, typing dots, spinner.
- **متى أستخدمها / when:** مشاهد واجهات ومساعدات ذكية — UI and assistant scenes.
- **كيف / how:** shimmer linear-gradient(90deg, s2, s3, s2) at 200% size, background-position → −200% in 1.2 s linear infinite, bars 14 px radius 7; alert pulse opacity 1→.35→1 1.6 s ease-in-out; recording ring box-shadow 0 0 0 6px at 50% over 1 s; typing dots opacity .25 translateY(−3 px) at 50%, 1 s, delays 0/.15/.3 s; spinner 34 px ring, border 4 px, one side transparent, .8 s linear; calm enter opacity .65→1, y 4 px, 180 ms. In a render use finite repeats tied to t. **أرقام / params:** 1.2 s / 1.6 s / 1 s / .8 s.
- **الدليل / proof:** `kosif-earth-ci-fork/ui/ds/shell.css:217` · `kosif-earth-ci-fork/ui/ds/components.css:38` · `kosif-earth-ci-fork/ui/features/assistant.css:20`

#### EASE-81 · سرعات الكتابة الآلية · Typewriter speed table · 🟢 جاهز / ready
- **ماذا / what:** حروف في الثانية لكل إحساس، ومؤشر وميض بخطوات حادة. — Characters per second per mood, with a hard-stepped caret.
- **متى أستخدمها / when:** أوامر طرفية، كود، عناوين تُكتب — terminal commands, code, typed titles.
- **كيف / how:** 3–5 cps dramatic, 8–12 natural, 15–20 tech/code, 30+ bulk fill; caret opacity yoyo with steps(1), block 11×22 px; kit MOTION.typeOn drives the count through a modifier (seek-safe) with E.type (.5,1,.89,1) for an eased count; Arabic text types by whole words or a mask wipe, not characters (ARAB-01). **أرقام / params:** 3–5 / 8–12 / 15–20 / 30+ cps.
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js` · `kosif-atlas/skills/2702-hyperframes/10377-gsap/references/effects.md` · `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md`

#### EASE-82 · زمن الرسم حسب حجم الخطوة · Drawing-time model · 🟢 جاهز / ready
- **ماذا / what:** مدة رسم كل خطوة تتناسب مع الجذر التربيعي لحصتها من البكسلات المتغيرة مضروبة في وزنها، فالتفاصيل سريعة والسماء بطيئة. — Each painting step lasts ∝ √(changed-pixel share) × weight.
- **متى أستخدمها / when:** مشاهد تُرسم أمام المشاهد في استوديو الرسم — scenes painted on screen.
- **كيف / how:** dur = SPEEDS[speed] · step.weight · √(n/area); pixels revealed linearly in time; speeds slow 5.0, normal 1.8, fast 0.55, instant 0 (seconds per full-sheet step); the film renderer uses the same formula per frame. **أرقام / params:** 5.0 / 1.8 / 0.55 / 0 s.
- **الدليل / proof:** `kosif-studio/studio.py:46` · `kosif-studio/film.py:28`

## واجهات وتفاعل دقيق — UI micro-timing & accessibility

_توقيت الأزرار والنوافذ والحالات — وحق المشاهد في حركة هادئة._

#### EASE-83 · تفاعلات الضغط والمرور والنوافذ · Press, hover & dialog entrances · 🟢 جاهز / ready
- **ماذا / what:** الأزرار تغطس عند الضغط، البطاقات ترد بظل أعمق، النوافذ تستقر بتجاوز بسيط بلا تحجيم، والتنبيهات تنزلق للأعلى. — Buttons dip, cards deepen their shadow, dialogs settle with slight overshoot (rise only), toasts slide up.
- **متى أستخدمها / when:** ديمو واجهات ولقطات تطبيقات — UI demos.
- **كيف / how:** .btn:active scale(.985) 180 ms ease-out; card hover box-shadow 220 ms (no movement); gate lift −2 px .18 s; dialog translateY(8 px) 300 ms spring (no scale so 44 px targets stay full size); menu 220 ms ease-out; toast translateY(12 px) scale(.96) 340 ms spring; dropdown y −4 px scale .98 .2 s; popover .14 s; toggle knob translateX + colour swap 250 ms spring; comment bubble 0.9→1 200 ms easeOutBack, hold ~1.5 s; theme cross-fade on bg/colour/border/shadow 220 ms (.2,.8,.2,1). **أرقام / params:** 180 / 220 / 300 / 340 ms.
- **الدليل / proof:** `kosif-earth-ci-fork/ui/ds/luxe.css:373` · `kosif-earth-ci-fork/ui/ds/luxe.css:367` · `kosif-earth-ci-fork/ui/ds/tokens.css:99`

#### EASE-84 · التحويل والشفافية فقط · Transform/opacity-only contract · ✅ مُثبت هنا / proven here
- **ماذا / what:** الأسطح التفاعلية لا تستخدم transition-all، والحركة محصورة في transform وopacity (وتلاشي الألوان)، والقيم المالية لا تتحرك أبدًا. — No transition-all; animate transform/opacity only; money values never animate.
- **متى أستخدمها / when:** كل واجهة ومشهد HTML — every UI and HTML scene.
- **كيف / how:** explicit property lists in transitions; GPU-friendly transforms; numbers that carry legal/financial meaning appear final, never counted; the motion-contract test asserts it for buttons, progress and tabs (5/5 passed here).
- **الدليل / proof:** `kosif-audit-pro/tests/motion-contract.test.mjs` · `kosif-audit-pro/README.md`

#### EASE-85 · زر تهدئة الحركة وتقليلها · Quiet-motion toggle & reduced motion · 🟢 جاهز / ready
- **ماذا / what:** بجانب إعداد النظام، زر يضع data-motion=quiet فيقتل كل حركة وانتقال، ورموز الحركة تتحول إلى فورية. — Besides the OS setting, a toggle sets data-motion=quiet and kills animation; tokens swap to instant/linear.
- **متى أستخدمها / when:** صفحات المعاينة والمشغّلات التفاعلية — preview pages and interactive players.
- **كيف / how:** documentElement.dataset.motion = 'quiet'|'full'; :root[data-motion=quiet] * {animation:none; transition:none}; waveform level fixed at .08; @media (prefers-reduced-motion: reduce) overrides tokens (instant 0, fast 100, normal 200, slow 300, slower 500 ms); the rendered video itself is unaffected. **أرقام / params:** wave level .08 when quiet.
- **الدليل / proof:** `kosif-audit-studio/studio.js:23` · `kosif-audit-studio/studio.css:140` · `kosif-atlas/skills/1567-tonone/4430-form-tokens`

#### EASE-86 · حركات طبقات الاستوديو · Studio layer entrances & opacity envelope · ✅ مُثبت هنا / proven here
- **ماذا / what:** كل طبقة نص أو شكل في استوديو المونتاج تختار: ظهور، صعود، تكبير، أو ثابت، فوق غلاف شفافية شبه منحرف. — Each studio text/shape layer picks fade, rise, zoom or none over a trapezoid opacity envelope.
- **متى أستخدمها / when:** إضافة نص فوق فيديو في محرر المتصفح — adding text over footage in the browser editor.
- **كيف / how:** animationProgress(o,t) = min(1, (t−start)/min(0.6, d/3), (end−t)/min(0.4, d/3)), 0 outside; ease = 1 − (1 − clamp((t−start)/0.65))³; rise y offset (1−ease)·0.07·h; zoom scale 0.65 + 0.35·ease; none = full opacity. model.test.mjs passed here. **أرقام / params:** in 0.6 s, out 0.4 s, each ≤ d/3; 0.65 s ease.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/model.mjs:12` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:75` · `100-superskills/skills/kosif-montage-motion/tests/studio/model.test.mjs`

#### EASE-87 · تبديل الحالات بانسيابية · State swaps: FLIP reflow & headline crossfade · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** الصناديق تنتقل من مواضعها القديمة إلى الجديدة، والعنوان الخارج يصعد ويتلاشى بينما الداخل يأتي من الأسفل بتداخل 200 ملّي ثانية. — FLIP boxes to new layout; outgoing headline up and out while the new one rises, 200 ms overlap.
- **متى أستخدمها / when:** إعادة ترتيب واجهة، تبديل عناوين — layout changes, headline swaps.
- **كيف / how:** FLIP: measure first/last rects, animate the inverse to identity over 600 ms cubic-bezier(.65,0,.35,1); collapse a detail list into one chip row. Headline: out y −12 px + fade, in from +12 px, 500 ms easeInOut, overlap 200 ms. **أرقام / params:** 600 ms (.65,0,.35,1); ±12 px, 200 ms overlap.
- **الدليل / proof:** `kosif-tool/styles/pm-moguzbulbul-6311b6` · `kosif-tool/styles/pm-ai-baymax-0ef9dd`

#### EASE-88 · تنعيم أثر المؤشر بالمسافة · Distance-sampled pointer trail · 📄 موصوف / documented only
- **ماذا / what:** رأس يقترب من الهدف كل إطار ونقاط الأثر توضع حسب المسافة لا الزمن، فلا يتمزق الأثر في الضربات السريعة. — A head eased toward the target each frame, trail points laid by distance travelled.
- **متى أستخدمها / when:** إصبع أو مؤشر مرسوم بأثر — scripted finger/cursor trails.
- **كيف / how:** head += (target − head)·0.3 per frame; push a point when distance > 0.01 field units; drop points older than 1.6 s; 24 points; for a seek-safe render compute the head from a sampled path (EASE-48) rather than accumulating. **أرقام / params:** follow 0.3/f; spacing 0.01; life 1.6 s; 24 pts.
- **الدليل / proof:** `kosif-atlas/skills/100-ui-motion/211-thermal-finger-trail`

#### EASE-89 · توقيتات الصور وضربات الميزات · Photo & feature-beat timings · 📄 موصوف / documented only
- **ماذا / what:** أرقام قياسية لدخول الصور وخروجها وتتابعها وثباتها، ولضربات الميزات في الإعلانات. — Standard photo entrance/exit/stagger/holds and ad feature beats.
- **متى أستخدمها / when:** ألبومات صور، إعلانات منتج — photo stories, product ads.
- **كيف / how:** photo in 400 ms opacity + scale 1.04→1 (.22,1,.36,1); out 250–300 ms (.55,0,1,.45); next starts 2 frames early; stagger 80–120 ms (60 for ≥6); ≤6 photos at once; holds 2.5–5 s with narration, 1.2–2 s montage, ≥8 frames. Feature beat: enter 300–450 ms ease-out quint, hold until read, exit 200 ms, cut on music. Word entrance 300–450 ms, rise 40–70 px, opacity in the first 60%; word stagger 70–120 ms (or word start − 60 ms with audio); decaying slide 80/60/50/25/12 px per successive word. **أرقام / params:** 400 / 250–300 ms; holds 2.5–5 s.
- **الدليل / proof:** `kosif-tool/playbooks/photos.md:40` · `kosif-tool/playbooks/ads.md:26` · `kosif-tool/playbooks/kinetic-type.md:26` · `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md`

## مكونات ومكتبات جاهزة للتوقيت — Ready timing components & libraries

_ما يمكن استدعاؤه بأمر واحد بدل بنائه._

#### EASE-90 · مكونات HyperFrames للتوقيت · HyperFrames timing components · 📦 بأمر تثبيت / one install
- **ماذا / what:** مكونات مسجلة تُضاف بأمر واحد وتُركّب على div بالـ data attributes، والمدة الزائدة تصبح ثباتًا لا تمديدًا. — Registry components added with one command and mounted via data attributes.
- **متى أستخدمها / when:** تركيبات HyperFrames — HyperFrames compositions.
- **كيف / how:** npx hyperframes add <name> copies compositions/components/<name>.html; mount on a class="clip" div with data-composition-src + data-start/data-duration/data-track-index and JSON overrides in data-variable-values; colours/fonts from the 18 theme tokens; preview/render with npx hyperframes preview|render. Timing set: arc-motion-path (MotionPath autoRotate); beat-timeline (beatCount 4, 0.6 s); echo-trail (4 echoes, 0.09 s); extended-keyframe; keyframe-scrub-stack; motion-blur (720°, 16 samples); offset-path-traveler (SVG path, tangent rotation); shutter-slam (one word through six single-property beats under shutter blur); slit-scan-reveal (rows|cols, spread .45, resolve 2.2 s); spring-pop (fromScale .9, overshoot 1.7); stagger-cascade (6 items, 60 ms); stagger-lattice; stop-motion-cadence (8|10|12 fps); velocity-throw-snap (5-shot rail, hero index 2); talking-head recut cards with 13 data-anim kinds quantised to 1/fps. **أرقام / params:** 15 components.
- **تثبيت / install:** `npx hyperframes add spring-pop`
- **رخصة / license:** Apache-2.0 (components use GSAP: standard no-charge license)
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/shutter-slam/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/velocity-throw-snap/velocity-throw-snap.html` · `kosif-one/vendor/hyperframes/registry/components/slit-scan-reveal/slit-scan-reveal.html` · `kosif-one/vendor/hyperframes/skills/talking-head-recut/SKILL.md`

#### EASE-91 · مكتبات توقيت إضافية · Extra timing libraries · 📦 بأمر تثبيت / one install
- **ماذا / what:** محركات توقيت بديلة حين يلزم: anime.js، Motion، Theatre.js، Lottie، وMotion Canvas. — Alternative timing engines when needed.
- **متى أستخدمها / when:** حين يطلب المستخدم محركًا بعينه أو تسلسلًا مرئيًا للمفاتيح — when a specific engine or a visual keyframe editor is wanted.
- **كيف / how:** animejs 4.5 (stagger utilities, MIT), motion 14 (springs, MIT), @theatre/core 0.7 (keyframe sequencing; studio is AGPL — keep it out of shipped bundles), lottie-web 5.13 (play AE exports, seek by frame), @motion-canvas/core 3.17 (generator timelines). Render any of them through render_html.cjs only after wiring seek(t) to the library's own seek/goToAndStop — never real time. **أرقام / params:** seek-wired only.
- **تثبيت / install:** `npm i animejs motion @theatre/core lottie-web`
- **رخصة / license:** Theatre.js studio AGPL-3.0; others MIT/Apache
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`

## توليفات قوية / power combos

- **ريل كلام على ساعة الكلمات / talking reel on the word clock:** EASE-01 + EASE-06 + EASE-51 + ARAB-62 + SYNC (words.json) — كل كلمة تدخل عند موعد نطقها (أقصى فرق 33 ملّي ثانية في فيلم الإثبات)، وضربة hitPulse على الكلمة المنبورة، والصوت الأصلي لا يُمس.
- **مونتاج على البيت / beat montage:** EASE-66 + EASE-67 + EASE-71 + BEAT (BPM والضربات) + TRANS — القطع الكبير على الضربة القوية، الزووم على الضعيفة، وذروة بطاقات كل ثُمن نغمة.
- **إطلاق منتج فاخر / premium launch:** EASE-63 + EASE-09 (out/exit/cam) + EASE-16 + EASE-28 (تجاوز 0%) + CAM + GLOW — لقطة وسيطة 1.46 ث، دفع كاميرا لوغاريتمي، ولا ارتداد على الشعار.
- **درس مبادئ الحركة / animation-principles lesson:** EASE-21 + EASE-54 + EASE-53 + EASE-49 + DRAW — منحنى التسهيل يُرسم على الشاشة، كرة بانضغاط وأشباح تبيّن التباعد.
- **ديمو تطبيق / app demo:** EASE-43 + EASE-83 + EASE-42 + EASE-81 + UI — مؤشر بقوس 2–4%، ضغط 80/140 ملّي ثانية، وقفة قراءة 1.2–2 ث، وكتابة 15–20 حرفًا/ث.
- **سبورة تعليمية / whiteboard lesson:** EASE-08 + EASE-82 + EASE-44 + DRAW + ARAB-22 — معامل بطء واحد، رسم بسرعة تتناسب مع حجم الخطوة، وكشف على امتداد التعليق.
- **ستوب موشن كولاج / stop-motion collage:** EASE-77 + EASE-05 + EASE-56 + TEX (ورق) — رسوم على اثنين، خمس ضربات لكل 10 ث، وأختام تضرب.
- **قصة بيانات / data story:** EASE-44 (فعل حركة لكل مشهد) + EASE-30 + EASE-45 + DATA — عقد تقفز بنابض k160 d14 والأرقام تعدّ ولا عنصر يتجمد.
- **فيديو حلقي للغلاف / looping cover:** EASE-79 + EASE-78 + PART — كل موجة بتكرار صحيح داخل المدة، وتنفس بسعة 1%.

## أخطاء ممنوعة / never do

1. **لا ساعة حائط ولا Math.random ولا مؤقتات في مشهد يُرندر** — الإطارات تختلف بين رندر وآخر ولا يمكن الرندر بالتوازي؛ كل شيء من seek(t) وبذرة ثابتة (EASE-01).
2. **لا تراكم القيم إطارًا بعد إطار (x += …) في الرندر** — البحث إلى إطار بعيد يعطي نتيجة خاطئة؛ استخدم صيغة مغلقة أو MOTION.sampled (EASE-17/48).
3. **لا تحرك موقعًا مكانيًا بمنحنى خطي** — يبدو آليًا؛ الخطي للانجراف والبيانات والضوء فقط (EASE-15).
4. **لا back/elastic على شعار رسمي ولا أكثر من نابضين مرتدين في الفيلم** — يرخص الهوية ويُتعب العين؛ الافتراضي تجاوز 0% (EASE-28).
5. **لا تتابع حرفًا حرفًا على العربية** — يكسر الوصل؛ تتابع الكلمات 60–160 ملّي ثانية أو قناع (EASE-32، ARAB-01).
6. **لا تملأ أول ربع اللقطة ثم تجمّد** — تصبح شريحة؛ اكشف مع التعليق (EASE-44).
7. **لا تتجاوز 3 بكسل/إطار لنص يُقرأ ولا 80 بكسل/إطار لأي شيء** — لا يُقرأ ويتقطع؛ قِس بـ motion.py speed (EASE-60).
8. **لا تثق بنسب التجاوز المكتوبة في الوثائق دون قياس** — قستُ هنا: spring('snappy') يتجاوز 8.4% لا 3% (EASE-23).
9. **لا وميض كامل الإطار أسرع من 3 هرتز** — خطر على المصابين بالصرع ويُرفض في المنصات (EASE-71/78).
10. **لا تحذف وقفة ذات معنى لتصل إلى رقم ASL** — الأرقام إرشاد لا هدف؛ والقطع حيث الفجوة < 0.15 ث يُسمع (EASE-64/70).
11. **لا تعِد بمدة لا يحتملها الحساب** — 5 مشاهد × 6 ث = 30 ث وليس 25 (EASE-03).
12. **لا CSS transitions ولا تكرار لا نهائي في صفحة تُرندر** — لا تُبحث بالزمن الافتراضي؛ تكرارات محدودة مربوطة بـ t (EASE-80).

## أقوى 5 حركات توقيع / 5 signature moves

1. **EASE-09 — منحنيات الأدوار:** ‏E.out للوصول، E.exit إلى القطع، E.cam للكاميرا — أول ما تختاره لأي فيلم؛ مقيسة هنا.
2. **EASE-22 — نوابض SPR المغلقة:** ‏firm للاستقرار الهادئ (0%، 0.58 ث)، وsnap لهبوط حقيقي (6%، 0.34 ث) — أي إطار يُحسب مباشرة.
3. **EASE-51 — غلاف الضربة:** قمة بعد الصوت بإطارين واضمحلال أسي — يجعل كل ركلة وكلمة منبورة «تضرب».
4. **EASE-19 — لقطة السرعة U:** دخول سريع، تجوال 1.2 بكسل/إطار، تسارع إلى القطع — توقيع المونتاج السريع الأنيق.
5. **EASE-63 — أرقام الإيقاع:** لقطة 1.46 ث، أول كلمة 0.4 ث، ذروة عند 82%، بطاقة نهاية 2.2 ث — ابدأ كل تخطيط منها.

## إضافات v2 — v2 additions

_قدرات أُضيفت في الإصدار الثاني من حزم المالك (higgsfield-motion-saas وhiggsfield-motion-claude ومهارة المونتاج التحريرية وفيلم الأغنية وKOSIF SEE) ومن مهارات ECC (رخصة MIT)، مكتوبة بكلماتنا. ✅ هنا = شُغّلت في جلسة 2026-10-16 وسجلها في [external-skills.md](../external-skills.md)؛ مسارات `owner-upload:` تشير إلى أرشيفات المالك لا إلى هذا المستودع. — v2 additions from the owner's packages and ECC skills (MIT), in our own words; ✅ = run in this session, log in external-skills.md; `owner-upload:` paths point into the owner's archives, not this repo._

#### EASE-X01 · نموذج شكل السرعة · Speed-shape model (r = speed ÷ mean speed) · ✅ مُثبت هنا / proven here
- **ماذا / what:** صِف كل حركة بنسبة سرعتها إلى متوسطها r بدل البكسل في الثانية، فتصلح الوصفة لأي حجم وأي fps؛ وأربعة أشكال تكفي: Easy Ease والإبرة والنتوء والتتابع. — Describe every move by r = speed / mean speed instead of px/s so a recipe survives any size or fps; four target shapes cover cuts and joints: Easy Ease, needle, cusp and relay.
- **متى أستخدمها / when:** عند تصميم أي حركة تعبر قطعًا أو تتصل بحركة أخرى — whenever a move crosses a cut or hands over to another move.
- **كيف / how:** Model an After Effects temporal ease as a cubic Bézier in (time, value): P0=(t1,v1), P1=(t1+i1·D, v1+s1·i1·D), P2=(t2−i2·D, v2−s2·i2·D), P3=(t2,v2) with influence i and key speed s. With zero key speeds and the same influence a on both keys the peak is r = 1/(1−a): Easy Ease 33.33 is exactly smoothstep (peak 1.5×, speed 0 at the keys, the amateur mistake on an event); 90 → 10×; 95 → 20× (the needle). Cusp for a UI-morph joint: outer keys (0, a), joint key (r·mean, b); no overshoot while 1/(1−a) ≤ r ≤ 1/b. Relay: start the next bell ≈0.45 into the current one so the summed speed never reaches 0 (EASE-X04). Ran here (external-skills.md V1): a numeric Bézier gives 1.500 / 10.00 / 20.00, matching 1/(1−a). **أرقام / params:** r_peak = 1/(1−a); a 33.33 → 1.5×, 90 → 10×, 95 → 20×; relay start 0.45.
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/ease-math.md`
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/references/external-skills.md` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/motion-v2/README.md` · `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/ease-math.md`

#### EASE-X02 · إبرة السرعة على القطع · Needle ease: the speed peak lands on the cut · ✅ مُثبت هنا / proven here
- **ماذا / what:** اجعل أسرع لحظة في الحركة هي لحظة القطع: منحنى 95/95 يبلغ 20 ضعف المتوسط في لحظة، فيختفي القطع داخل الحركة. — Hide the cut inside the fastest instant of the move: a 95/95 ease peaks at 20× mean speed, so the edit disappears into the motion.
- **متى أستخدمها / when:** زوم أو سوط ينتهي بقطع، أو جسم مستمر يعبر القطع — a zoom or whip that ends on a cut, or a persistent object crossing it.
- **كيف / how:** Keys at cut − 0.2 s and cut + 0.2 s − 1 frame, both influence 95 (CSS ≈ cubic-bezier(.95,0,.05,1)); put the curve midpoint at cut − ½ frame so ONE peak frame-step ends on the cut. Print the per-frame speed list and read it: a list that touches 0 mid-move means a pause; a peak one frame off means move the keys, not the influence. Ran here (V1): 100 → 135 in 0.4 s @60 with 95/95 gives steps … 46 64 95 161 581 581 161 95 64 … units/s: the midpoint sat on a frame boundary, so the peak split into two equal steps; shift the keys half a frame to get one. Frame-averaged peak ≈ 6.6× mean even though the instantaneous peak is 20×. **أرقام / params:** influence 95/95; keys cut−0.2 s / cut+0.2 s−1 f; midpoint cut−½ f.
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/ease-math.md`
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/references/external-skills.md` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/motion-v2/README.md` · `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/ease-math.md`

#### EASE-X03 · سرعة نسبية متطابقة عبر القطع · Match relative speed across a cut (rho) · ✅ مُثبت هنا / proven here
- **ماذا / what:** عند القطع بين طبقتين مختلفتي الحجم طابِق السرعة النسبية (تغير الحجم ÷ الحجم) لا البكسل في الثانية، وإلا قفزت الحركة. — When cutting between two layers of different size, match relative speed rho = (dH/dt)/H, not px/s, or the move jumps.
- **متى أستخدمها / when:** انتقال تكبير يسلّم إلى طبقة أصغر أو أكبر في اللقطة التالية — a growth/zoom move handed to a differently sized layer after the cut.
- **كيف / how:** r2 = r1 · p/(1+p) · (1−q)/q · D2/D1, where p and q are the fractional size changes on each side and D the durations; then the incoming end influence = min(86, 100·(1−1/r2)). Worked example (ran here, V1): r1 = 9, p = q = 0.18, equal durations → r2 = 6.254, influence 84. The source's own self-test gave rho 3.74/s vs 3.80/s (ratio 1.017). Pair with EASE-X05 so the slopes also match. **أرقام / params:** r2 = r1·p/(1+p)·(1−q)/q·D2/D1; influence = min(86, 100(1−1/r2)).
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/ease-math.md`
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/references/external-skills.md` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/motion-v2/README.md` · `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/ease-math.md`

#### EASE-X04 · تتابع متداخل بلا توقف · Relay overlap: start the next move at 0.45 · ✅ مُثبت هنا / proven here
- **ماذا / what:** ابدأ الحركة التالية قبل انتهاء الحالية (عند نحو 0.45) على أب واحد فتُجمع السرعات ولا تصل إلى الصفر عند المنعطف. — Start the next move about 0.45 into the current one on a parent null so speeds add and never hit zero at the corner.
- **متى أستخدمها / when:** مسار A ← B ← C لكاميرا أو جسم أو مؤشر — any A→B→C path for a camera, object or cursor.
- **كيف / how:** Acceptance: closest approach to B ≥ 5 % of |AB| and minimum speed clearly above 0; sequential Easy Eases give 0 % and a full stop; the source rejected a hybrid at 3.9–4.3 %. Ran here (V1) on a 90° turn with equal legs and Easy Ease on both moves: sequential → 0 % / 0 % of peak speed; next starts at 0.5 D → 22.1 % / 60 %; at 0.45 D → 26.2 % / 57 %. Stack the two moves as summed deltas on one parent instead of keying one layer twice. **أرقام / params:** overlap 0.45; closest approach ≥ 5 % |AB|; min speed > 0.
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/ease-math.md`
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/references/external-skills.md` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/motion-v2/README.md` · `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/ease-math.md`

#### EASE-X05 · زوج منحنيين بميل متساوٍ عند القطع · Equal-slope curve pair across a cut · ✅ مُثبت هنا / proven here
- **ماذا / what:** منحنى الخروج قبل القطع ومنحنى الدخول بعده لهما الميل نفسه عند القطع، فتبقى السرعة واحدة على الجانبين. — The ease into the cut and the ease out of it share the same slope at the cut, so speed is continuous across it.
- **متى أستخدمها / when:** سوط معكوس أو زوم يكمل في اللقطة التالية — a mirrored whip or a zoom that continues in the next shot.
- **كيف / how:** expoIn cubic-bezier(.7,0,.84,0) ends with slope 6.25 and expoOut (.16,1,.3,1) starts with slope 6.25 (ran here, V1: 6.250 / 6.250). In code films in(k) = p^k ends with slope k and out(k) starts with slope k, so speed at the cut = k·Δ/T: a mirrored whip −700 px in(2) 0.45 s then +700 px out(2) 0.45 s has identical speed on both sides. **أرقام / params:** expoIn (.7,0,.84,0) ↔ expoOut (.16,1,.3,1): slope 6.25; speed = k·Δ/T.
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/ease-math.md`
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/references/external-skills.md` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/motion-v2/README.md` · `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/ease-math.md` · `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/transitions.md`

#### EASE-X06 · جداول منحنيات بالاسم والنية · Named curves: AE ↔ CSS table and intent eases · 📄 موصوف / documented only
- **ماذا / what:** قائمة جاهزة تربط كل نية حركة بمنحنى CSS محدد، وتترجم إعدادات After Effects إلى cubic-bezier. — A ready list that maps each motion intent to a concrete CSS curve and translates After Effects settings to cubic-bezier.
- **متى أستخدمها / when:** عند اختيار منحنى لكاميرا أو تحوّل واجهة أو دخول — choosing a curve for a camera, UI morph or entrance.
- **كيف / how:** AE → CSS: needle 95/95 ≈ (.95,0,.05,1); scroll-into ≈ (.5,0,.85,.625); settle after a cut ≈ (.2,.7,.05,1); UI morph out/in ≈ (.66,0,.9,.1) / (.07,.44,.16,1); entrance width ≈ (.75,0,.25,1); Easy Ease (.333,0,.667,1). By intent: camera push/pull (.76,0,.24,1); follow (.55,0,.25,1); soft drift (.37,0,.63,1); snap pull-back (.25,.1,0,1); whip (.83,0,.17,1); suck into a landing (.62,0,.92,.42). Never tween a fill between distant hues through RGB (magenta → lime passes salmon and mustard); interpolate in a perceptual space. **أرقام / params:** push (.76,0,.24,1) · follow (.55,0,.25,1) · drift (.37,0,.63,1) · whip (.83,0,.17,1).
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-skill-claude/higgsfield-motion-claude/references/production-lessons.md`
- **الدليل / proof:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/ease-math.md` · `owner-upload:motion-skill-claude/higgsfield-motion-claude/references/production-lessons.md`

#### EASE-X07 · أرقام نعومة قبلها العميل · Client-approved smoothness numbers · 📄 موصوف / documented only
- **ماذا / what:** أرقام دخول وتتابع ونص ومؤشر مرّت عند عميل حقيقي في أفلام إطلاق، تصلح نقطة بداية لأي فيلم واجهات. — Entrance, stagger, text and cursor numbers that passed a real client on launch films; a starting point for any UI film.
- **متى أستخدمها / when:** أفلام المنتجات والواجهات وكل دخول داخل مشهد — product/UI films and every in-scene entrance.
- **كيف / how:** Entrances 0.45–0.7 s on (.16,1,.3,1), scale from ≥ 0.9, travel ≤ 40–70 px, overshoot ≤ 2–4 %; staggers 50–80 ms (letters 30–60 ms); text = opacity ×1.8 speed + rise 24 px + blur 12 → 0 px (optional chromatic text-shadow 14–18 px → 0); cursor 0.6–0.9 s per move on a 5–15 % arc, click squash 0.92 in 0.12 s, release 0.2 s; typing ≤ 50–60 chars/s; anything that must be read stays ≥ 0.8 s; nothing appears in < 0.2 s outside a blurred transition. Strong in(3)/out(3) curves belong to transitions only. **أرقام / params:** entrance 0.45–0.7 s; overshoot ≤ 2–4 %; stagger 50–80 ms; read ≥ 0.8 s.
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/client-taste.md`
- **الدليل / proof:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/client-taste.md` · `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/launch-film.md`

#### EASE-X08 · قراءات مسموحة وميزانية السكون · Listed reads and the still-time budget · 📄 موصوف / documented only
- **ماذا / what:** السكون مسموح فقط لقراءة مسمّاة وبقدر ما تحتاجه؛ غير ذلك يجب أن يتغير شيء كل نصف ثانية تقريبًا. — Stillness is allowed only as a listed read and only as long as the read needs; otherwise something must change about every half second.
- **متى أستخدمها / when:** ضبط إيقاع فيلم واجهات أو إعلان قصير — pacing a UI film or short ad.
- **كيف / how:** Allowed stills: status line 1.0 s · name + ✓ 0.6–0.7 s · three numbers 1.2 s · one list item 0.8 s · end lockup 2 s; anything else longer than ≈ 0.5–0.6 s needs a trigger, a camera follow or a cut. Read time for a line = max(1.0 s, 0.35 s × words + 0.5 s) × k (count characters for CJK/Thai). Measure the result with the dead-air meter (QA-X02) instead of guessing. **أرقام / params:** reads 1.0 / 0.65 / 1.2 / 0.8 / 2.0 s; readTime = max(1, 0.35·w + 0.5).
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-skill-claude/higgsfield-motion-claude/SKILL.md`
- **الدليل / proof:** `owner-upload:motion-skill-claude/higgsfield-motion-claude/SKILL.md` · `owner-upload:motion-skill-claude/higgsfield-motion-claude/scripts/activity.mjs`

#### EASE-X09 · نابض بارتداد واحد ومفاتيح بمنحنى الوصول · One-overshoot spring and arriving-key ease tracks · ✅ مُثبت هنا / proven here
- **ماذا / what:** نابض مغلق الصيغة يرتد مرة واحدة وينتهي عند 1 تمامًا، ومسارات مفاتيح يحدد فيها منحنى المفتاح شكل المقطع الواصل إليه، والخروج يبدأ من الحالة الراهنة. — A closed-form spring with a single overshoot that lands exactly on 1, plus key tracks where a key's ease shapes the segment arriving at it and exits start from the current state.
- **متى أستخدمها / when:** محرك حركة صغير مكتوب يدويًا لفيلم مونتاج أو ريل — a small hand-written motion engine for an edit or reel.
- **كيف / how:** spring(k) = 1 − e^(−6k)·cos(7.5k)·(1−k). Measured: max 1.0736 at k ≈ 0.315 (≈ 7.4 % overshoot) and exactly 1.0000 at k = 1 (re-run here in Python, V1; the session distillation also ran the original JS). Tracks are [[t, value, ease]] where the ease on a key shapes the segment ARRIVING at it: sample([[0,0],[1,10,'expoOut'],[2,[1,2]]], 0.5) → 9.6875. An exit shorthand starts from whatever the property is doing at out.t, not from the rest value, so an interrupted entrance never snaps. **أرقام / params:** spring peak 1.0736 @ k 0.315; settles at k = 1.
- **الرخصة / license:** unknown (reference only)
- **المصدر / source:** `owner-upload:Claude_edit_skill_1/Claude edit skill/implementation/browser-reference/engine.js`
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/references/external-skills.md` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/motion-v2/README.md` · `session-2026-10-16:motion-leftovers#3.2` · `owner-upload:Claude_edit_skill_1/Claude edit skill/implementation/browser-reference/engine.js`

#### EASE-X10 · بوسترة طبقة واحدة · Per-layer posterize (stepped time on one layer) · 📄 موصوف / documented only
- **ماذا / what:** حرّك طبقة واحدة بخطوات إيقاف حركة (مثل 8 أو 12 إطارًا في الثانية) بينما تبقى الصورة والحبيبات على معدل الفيلم الكامل. — Step one layer's animation at a stop-motion rate (e.g. 8 or 12 fps) while the picture and grain stay at the film's full rate.
- **متى أستخدمها / when:** نص أو رسم يدوي يحتاج إحساسًا مصنوعًا يدويًا داخل لقطة ناعمة — type or hand-drawn marks that need a handmade feel inside a smooth shot.
- **كيف / how:** t_layer = floor(t·fps_step)/fps_step for that layer only; never quantise the grain or the camera with it (they reveal the trick). Keep discrete events (a stamp, a click) on the quantised clock so they land on a stepped frame. **أرقام / params:** step fps 8–12 on one layer; film stays 24–30 fps.
- **الرخصة / license:** unknown (reference only)
- **المصدر / source:** `owner-upload:Claude_edit_skill_1/Claude edit skill/implementation/browser-reference/typeLayers.js`
- **الدليل / proof:** `owner-upload:Claude_edit_skill_1/Claude edit skill/implementation/browser-reference/typeLayers.js`

#### EASE-X11 · تصميم الضربة الرئيسية · Main-hit micro-choreography · 📄 موصوف / documented only
- **ماذا / what:** الضربة الكبرى في الفيلم تُبنى: تراجع تمهيدي ثم دفع متسارع ثم تركيز ثم ارتطام، مع اهتزاز بتردد عالٍ قصير العمر. — Build the film's main hit: anticipation dip, accelerating push, rack focus, snap, with a short high-frequency shake.
- **متى أستخدمها / when:** لحظة الكشف أو الشعار أو ذروة الإعلان — the reveal, logo or ad climax.
- **كيف / how:** 0.4 s anticipation dip → accelerating push + rack focus → snap; shake at ~11/17 Hz with decay tau ≈ 0.13 s (2 Hz reads as sway, not impact); a flash blooms from the action point, at most one big flash per second; text edits remove words in 0.2–0.3 s and relay the survivors with a 2-frame stagger in non-crossing order; finish fading masked text before an iris starts. Accessibility: ≤ 3 flashes/s, a full white flash ≤ 2 frames. **أرقام / params:** dip 0.4 s; shake 11/17 Hz, tau 0.13 s; ≤ 1 big flash/s.
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-skill-claude/higgsfield-motion-claude/references/production-lessons.md`
- **الدليل / proof:** `owner-upload:motion-skill-claude/higgsfield-motion-claude/references/production-lessons.md`

## من أكبر مستودعات GitHub — from the top GitHub repositories (2026-10-23)

_قدرات من أشهر مستودعات GitHub ذات الترخيص المفتوح (MIT)، مكتوبة بكلماتنا لا منسوخة، وسجل كل مستودع في [github-top-1000.md](../github-top-1000.md). 🟢 = الكود هنا في `scripts/motion_physics.py` واختباره `evals/test_motion_physics.py`. — Powers from the most-starred open-licence (MIT) GitHub repositories, restated in our own words; per-repo record in github-top-1000.md; 🟢 = code here in scripts/motion_physics.py with its test._

#### EASE-G01 · نابض بالفيزياء يطبع كل إطار · Spring solved frame by frame · 🟢 جاهز / ready
- **ماذا / what:** احسب النابض من الكتلة والصلابة والتخميد لا من مدة، واطبع قيمته في كل إطار وزمن استقراره ونسبة تجاوزه، أو كإطارات CSS. — Solve the spring from mass, stiffness and damping instead of a duration, and print its value every frame, its settle time and overshoot, or CSS @keyframes.
- **متى أستخدمها / when:** حركة دخول أو ارتداد طبيعية في HTML أو Remotion أو After Effects / a natural entrance or bounce in HTML, Remotion or After Effects
- **كيف / how:** `python3 scripts/motion_physics.py spring --from 0 --to 1 --stiffness 170 --damping 26 --fps 30` → JSON with damping_ratio, regime, settled, seconds, overshoot_pct and values per frame; `--css pop` prints @keyframes. Damping ratio ζ = damping / (2√(stiffness·mass)): ζ<1 bounces, ζ≈1 settles fastest without overshoot. Measured here: 170/26 settles in 0.73 s with 0 % overshoot (ζ≈1.0); 180/8 overshoots 37 % and settles in 1.6 s. Paste the values array instead of hand-keying a bounce. **أرقام / params:** stiffness 170 · damping 26 · mass 1 (react-spring defaults); sub-step 1/16 frame.
- **الرخصة / license:** MIT
- **المصدر / source:** https://github.com/pmndrs/react-spring (MIT; tension/friction model) — our own solver in scripts/motion_physics.py
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/scripts/motion_physics.py` · `kosif-tool/.claude/skills/kosif-superpowers/evals/test_motion_physics.py`

#### EASE-G02 · منحنى CSS محسوب كما يحسبه المتصفح · Browser-exact cubic-bezier sampling · 🟢 جاهز / ready
- **ماذا / what:** حوّل أي cubic-bezier أو اسم تسهيل CSS إلى قيم لكل إطار بنفس حل المتصفح، لتطابق الحركة في الفيديو ما يظهر في الصفحة. — Turn any cubic-bezier or named CSS easing into per-frame values with the browser's solution, so the rendered film matches the page.
- **متى أستخدمها / when:** نقل حركة من CSS إلى Manim أو After Effects أو العكس / moving an animation between CSS and Manim or After Effects
- **كيف / how:** `python3 scripts/motion_physics.py bezier 0.25 0.1 0.25 1 --frames 30`; named easings for `--ease` in stagger and keyframes: linear, ease, ease-in, ease-out, ease-in-out, out-expo, out-back, in-out-cubic, plus steps(n). Solver: Newton on x(t) with bisection fallback, then y(t). Check: CSS 'ease' at x=0.5 gives 0.8024. **أرقام / params:** x1, x2 ∈ [0,1]; y may overshoot (out-back).
- **الرخصة / license:** MIT
- **المصدر / source:** CSS Easing Functions definition (W3C) — our own solver in scripts/motion_physics.py
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/scripts/motion_physics.py` · `kosif-tool/.claude/skills/kosif-superpowers/evals/test_motion_physics.py`

#### EASE-G03 · تتابع من نقطة أصل على شبكة · Stagger from an origin on a grid · 🟢 جاهز / ready
- **ماذا / what:** وزّع التأخير على العناصر حسب بعدها عن نقطة أصل (الأول، الأخير، المنتصف، الأطراف، عنصر بعينه) في صف أو شبكة، مع منحنى للتأخير نفسه. — Spread delays by each element's distance from an origin (first, last, center, edges, a given index) in a row or grid, with an easing on the delays themselves.
- **متى أستخدمها / when:** ظهور حروف أو أيقونات أو بلاطات شبكة / revealing letters, icons or grid tiles
- **كيف / how:** `python3 scripts/motion_physics.py stagger --count 12 --each 0.06 --from center --grid 4x3 --ease out` → delays in seconds per element (2-D distance on a grid). Center-out reads as an explosion, edges-in as gathering; ease-out on delays bunches the first ones and spreads the tail. Keep the total stagger ≤ 40 % of the move so the group still reads as one gesture. **أرقام / params:** each 0.03-0.08 s for letters; total ≤ 40 % of the move.
- **الرخصة / license:** MIT
- **المصدر / source:** https://github.com/juliangarnier/anime (MIT; stagger options) — semantics restated, our own code in scripts/motion_physics.py
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/scripts/motion_physics.py` · `kosif-tool/.claude/skills/kosif-superpowers/evals/test_motion_physics.py`

#### EASE-G04 · خط زمني بإزاحات نسبية وعلامات · Timeline with relative offsets and labels · 📄 موصوف / documented only
- **ماذا / what:** ابنِ المشهد كخط زمني واحد تُوضع فيه كل حركة بإزاحة نسبية من السابقة أو عند علامة مسماة، فيتغير التوقيت كله بتعديل رقم واحد. — Build the scene as one timeline where each move is placed by a relative offset from the previous one or at a named label, so retiming means editing one number.
- **متى أستخدمها / when:** مشهد فيه أكثر من خمس حركات متتالية / a scene with more than five chained moves
- **كيف / how:** Place: '+=0.2' (gap after the previous end), '-=0.15' (overlap), '<' (same start as previous), 'label+0.3'. Labels for beats ('title', 'logo', 'cta') come from the audio grid (words.json or beats). Never hard-code absolute times in many places; compute them from the label table and export the table with the film for review.
- **الرخصة / license:** MIT
- **المصدر / source:** https://github.com/juliangarnier/anime (MIT; timeline offsets) — restated; GSAP's position parameter is the same idea (GSAP licence: link only)
