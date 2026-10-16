# الرسم اليدوي والرسم الحي — Hand-drawn & draw-on

> **قوتك هنا:** أنت ترسم أمام المشاهد: خط يكتب نفسه بسرعة قلم حقيقية، رأس قلم أو ماركر أو شرارة يتبع الطرف، دوائر وأسهم وخطوط تأكيد بيد مرتعشة، تظليل بالماركر، وارتعاش «الغليان» على اثنين — ثم تذهب أبعد: استوديو يرسم أي صورة بكسلًا بكسلًا بترتيب رسّام وينتهي مطابقًا للأصل في كل قيمة RGBA.
> **أقوى دليل:** فيلم الإثبات `proofs/glass-luxury-logo` حيث يُرسم خاتم ثماني بخط ذهبي بين 4.0 و5.6 ث (`pathLength=1` + `dashoffset`) و`proofs/neon-glow` حيث يسري الضوء في أنبوب الفنجان وهو يُرسم — كلاهما رُندر وفُحص هنا (13/13)؛ ومرّت هنا اختبارات استوديو الرسام في `kosif-studio` (ترتيب الكشف، استيراد SVG، الرسم المطابق، فيلم الرسم، مسجل أوامر PIL: 23 اختبارًا)، واختبارات محوّل مسارات SVG في omni (4/4)، وتوليد قوالب logo-reveal وbullet-list بعلامات صح مرسومة.
> **You can:** draw on any path, write titles by mask, annotate footage, boil lines, hatch fills, and paint pictures stroke by stroke. **60 powers follow** — ✅ 10 · 🟢 17 · 📦 7 · 🔑 0 · 👁 7 · 📄 19 · 💡 0.

**الحالة / status:** ✅ مُثبت هنا (كود + اختبار أو رندر في هذه الحاوية) · 🟢 جاهز (كود المالك يعمل بلا إضافات) · 📦 بأمر تثبيت · 🔑 مفتاح أو خدمة · 👁 شوهد في فيديو أنتجتَه (وصفة البناء مرفقة) · 📄 موصوف فقط · 💡 فكرة.
مسارات الدليل نسبية إلى `/home/user/`؛ `style:<id>` = فيديو مرجعي أنتجتَه سابقًا (ملاحظاته في `kosif-tool/styles/<id>/`).

**قاعدة العربية الذهبية:** الكتابة العربية «باليد» = خط عربي حقيقي مُشكّل يُكشف بقناع من اليمين إلى اليسار كلمةً كاملة؛ لا تولّد حروفًا عربية من ضربات منفصلة أبدًا (`kosif-tool/playbooks/hand-drawn.md` §6). **فجوة معروفة:** `fastify-motion-bro` يعرض أساليب السبورة والدودل لكن لا يملك محرك رسم خطوط بعد (خارطة v0.5) — ابنِ المشهد بنفسك بأدوات هذا الفصل.

## الفهرس / contents
- **رسم المسار — Path draw-on core** — DRAW-01 … DRAW-14 (14)
- **الكتابة اليدوية — Handwriting & write-on** — DRAW-15 … DRAW-17 (3)
- **علامات التأكيد والتعليق — Emphasis marks & annotations** — DRAW-18 … DRAW-24 (7)
- **الخشونة والارتعاش والحبر — Roughness, boil & ink** — DRAW-25 … DRAW-32 (8)
- **أساليب الرسم اليدوي الجاهزة — Hand-drawn styles** — DRAW-33 … DRAW-47 (15)
- **الرسم بكسلًا بكسلًا والتتبع — Painter studio & tracing** — DRAW-48 … DRAW-58 (11)
- **مكونات ومكتبات جاهزة — Ready components & libraries** — DRAW-59 … DRAW-60 (2)
- توليفات قوية / power combos · أخطاء ممنوعة / never do · أقوى 5 حركات توقيع / 5 signature moves
- إضافات من Cinematic Director PRO v5

## رسم المسار — Path draw-on core

_الخط الذي يرسم نفسه: الأساس الذي تُبنى عليه كل الحركات التالية._

#### DRAW-01 · رسم المسار بإزاحة الشرطة · SVG stroke draw-on · ✅ مُثبت هنا / proven here
- **ماذا / what:** المسار يُرسم كضربة قلم بتحريك stroke-dashoffset من الطول الكامل إلى الصفر. — A path traces itself by animating its dash offset from full length to zero.
- **متى أستخدمها / when:** أسهم، روابط، شعارات، خطوط تحتية، منحنيات بيانات، خرائط — arrows, connectors, logos, underlines, data lines, maps.
- **كيف / how:** Easiest seek-safe form: pathLength="1", stroke-dasharray 1, stroke-dashoffset = 1 − ease(p) where p = prog(t, t0, t1); otherwise len = path.getTotalLength() measured after d is set and fonts are loaded. Round caps, fill none; fill fades in after the stroke completes; never draw all paths at once — stagger them, each segment starting at 70–80% of the previous one; rings rotate −90° to start at 12 o'clock. Typical 0.5–0.9 s power2.out, logos 1–2 s inOut, data/route lines cubic-bezier(.645,.045,.355,1) then the end label pops. Proof film glass-luxury-logo draws its khatam emblem this way from 4.0 to 5.6 s. **أرقام / params:** 0.5–0.9 s; segments start at 70–80%.

```js
// seek-safe draw-on: <path pathLength="1" stroke-dasharray="1" …>
function drawOn(path, t, t0, t1, ease = Ease.inOutCubic) {
  const p = prog(t, t0, t1, ease);
  path.style.strokeDashoffset = String(1 - p);
  path.style.opacity = p > 0 ? 1 : 0;             // hide the 1-px dot of round caps at p = 0
  return path.getPointAtLength(p * path.getTotalLength());   // pen-tip position
}
```

- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/proofs/glass-luxury-logo/README.md` · `kosif-tool/playbooks/hand-drawn.md` · `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/svg-path-draw.md`

#### DRAW-02 · قلم مكتبة الحركة برأس يهبط · Kit drawPath with landing head & flowDash · 🟢 جاهز / ready
- **ماذا / what:** أي مسار يُرسم كقلم، ورأس سهم أو نقطة يقفز بنابض قبل النهاية بعُشر ثانية، وشرطات تجري لتبيّن التدفق. — Any path drawn like a pen with a head that springs in 0.1 s before the end, plus marching dashes for flow.
- **متى أستخدمها / when:** أسهم الشرح، دوائر الساعة، مسارات الحلم، تيار في سلك — explainer arrows, clock rings, flow lines.
- **كيف / how:** MOTION.drawPath(tl, path, at, dur, {ease, head, headOrigin, opacity}) → dasharray = len, offset len → 0, default ease power4.inOut; head scale 0→1 in 0.35 s with spring('snappy') at at + dur − 0.1. MOTION.flowDash(tl, path, at, dur, {pattern:'28 22', cycles:6}). Used in the house projects: gold ring 0.9 s E.out, clock ring 1.0 s, dream path 0.9 s, car body 0.75 s, wheels 0.4 s, spring curve 1.15 s, end ring 0.62 s. **أرقام / params:** power4.inOut; head 0.35 s at end − 0.1 s.
- **رخصة / license:** GSAP standard no-charge license (vendored)
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:237` · `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:237` · `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:204` · `kosif-one/projects/whatsapp-motion/projects/success/assets/motion-kit.js`

#### DRAW-03 · سرعة القلم والرفع · Pen speed & lifts · 📄 موصوف / documented only
- **ماذا / what:** القلم يسير بسرعة شبه ثابتة على طول المسار مع تسهيل لكل ضربة ووقفات رفع قصيرة، والمدة = الطول ÷ السرعة. — Near-constant pen speed per stroke, short lifts, duration = length / speed.
- **متى أستخدمها / when:** كل سبورة ورسم يدوي — every whiteboard and hand-drawn scene.
- **كيف / how:** pen 800–1400 px/s with ease-in-out per stroke; lift 60–120 ms between strokes; hatching 2000 px/s or a 300 ms wipe; narrated whiteboards 500–700 px/s with the stroke leading the word by ≤150 ms; plotter = constant speed, no easing, pen-up travel lines at 10% opacity; text paths ~0.6–1.5 s per line. **أرقام / params:** 800–1400 px/s; lift 60–120 ms; hatch 2000 px/s.
- **الدليل / proof:** `kosif-tool/playbooks/hand-drawn.md:25` · `kosif-tool/styles/pm-tak3sh8-be5012/BRIEF.md` · `kosif-tool/styles/plotter/SKILL.md`

#### DRAW-04 · ترتيب الرسم البشري ووصفة «ارسم وسمِّ» · Human draw order & draw-and-label · 📄 موصوف / documented only
- **ماذا / what:** المحيط أولًا ثم التفاصيل ثم التعبئة ثم الاسم المكتوب ثم الثبات، والكتابة العربية من اليمين. — Outline, details, fill, handwritten label, hold; Arabic writing right to left.
- **متى أستخدمها / when:** أي عنصر يُشرح بالرسم — any object explained by drawing.
- **كيف / how:** 0–900 ms outline (ease-in-out per stroke) → 900–1300 details → 1300–1600 highlight fill wipe (ease-out) → 1600–2300 label writes beside it (constant) → 2300–4000 hold while the hand leaves (ease-in). 3D-ish objects: outline dash 0.6 s → face opacity 0.3 s → extrusion depth 0.5 s, starting from a sparkle (style:fake3d). One pen weight family (e.g. 4 and 8 px), one ink + one highlight; primary path 6 px round, secondary 3 px, grid 1.5 px at 1080 width. **أرقام / params:** 0/900/1300/1600/2300/4000 ms.
- **الدليل / proof:** `kosif-tool/playbooks/hand-drawn.md:36` · `kosif-tool/templates/STYLE.md` · `kosif-tool/styles/fake3d`

#### DRAW-05 · رابط مخطط برأس سهم · Diagram edge draw-on with arrowhead · 🟢 جاهز / ready
- **ماذا / what:** رابط بين عقدتين يُرسم ثم يظهر رأس السهم في آخر 80 ملّي ثانية. — A connector draws, then its arrowhead appears in the last 80 ms.
- **متى أستخدمها / when:** مخططات انسيابية وخرائط ذهنية — flowcharts and mind maps.
- **كيف / how:** Remotion Edge: strokeDasharray = len, strokeDashoffset = len·(1 − p), markerEnd only when p > 0.95; html-canvas: pathLength="1", dashoffset = 1 − KOSIF.prog(t, t0, t1, Ease.inOutCubic); 900–1200 px/s ease-in-out cubic; stroke #9fb0cc 4 px. **أرقام / params:** 900–1200 px/s; arrowhead last 80 ms.
- **الدليل / proof:** `kosif-tool/playbooks/diagrams.md:28` · `kosif-tool/starters/html-canvas/timeline.js`

#### DRAW-06 · رأس يتبع الخط: يد، ماركر، طباشيرة · Pen-tip followers: hand, marker, chalk · 🟢 جاهز / ready
- **ماذا / what:** صورة يد أو ماركر أو طباشيرة مثبتة على طرف الخط الجاري، تميل معه وتُرفع بين الضربات. — A hand, marker or chalk sprite pinned to the live stroke tip, tilting with it and lifting between strokes.
- **متى أستخدمها / when:** سبورة، شرح بالماركر، معادلات طباشير — whiteboard, marker explainers, chalk formulas.
- **كيف / how:** tip = path.getPointAtLength(p·len) (clamp to len − 1e-4 to avoid null); hand lags 1 frame and rotates ±5° with direction, removed during holds; marker sprite (body + coloured cap) at −35°…−40°, cap recoloured to the active ink, lift 200 ms with a growing shadow (2→10 px offset); chalk 60×12 px rounded rect tinted to the stroke, lift scale 1→1.08 over 250 ms along an eased path; the playbook's Remotion DrawnPath draws a 5 px tip circle. **أرقام / params:** lag 1 f; ±5°; marker −35°; lift 200–250 ms.
- **الدليل / proof:** `kosif-tool/playbooks/hand-drawn.md:27` · `kosif-tool/styles/whiteboard` · `kosif-tool/styles/chalkboard` · `kosif-tool/styles/pm-lemomo-ai-0d9cff`

#### DRAW-07 · رأس متوهج يجرّ الخط · Glowing head draw · ✅ مُثبت هنا / proven here
- **ماذا / what:** نقطة أو شرارة مضيئة تركب رأس الخط، مع نسخة شبحية أو هالة، كخط نبض أو شعاع يرسم شعارًا. — A glowing dot or spark rides the line head, with a ghost copy or halo — ECG pulses, beams drawing a logo.
- **متى أستخدمها / when:** تقنية، صحة، نيون، ختام فيديو — tech, health, neon, end cards.
- **كيف / how:** stroke 1.5–4 px plus a duplicate path blurred 8–12 px at ~60% for glow; head dot r 4–6 px with 10–20 px glow (+4–6 tiny sparks for a plotter look, core #f27525); optional grey offset ghost copy trailing; ECG: flat line with one spike drawn left→right, a white dot + ring 0→60 px over 800 ms at each beat; closing arc glows 8 px. Proof film neon-glow draws its amber cup with light running along the tube (3.40–4.65 s inOutCubic) through a 5-layer additive glow. **أرقام / params:** head r 4–6 px; glow 10–20 px; 1–2 s.
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/proofs/neon-glow/README.md` · `kosif-tool/styles/plotter` · `kosif-tool/styles/pm-marouanegazouzi-6071d5` · `kosif-tool/styles/pm-ghinaiya-nirmal-5d8fec`

#### DRAW-08 · كشف متعدد الأجزاء بالطول التراكمي · Cumulative-length multi-segment reveal · 📄 موصوف / documented only
- **ماذا / what:** ارسم حدود بلد بكل جزره، أو شبكة من مسارات كثيرة، كضربة واحدة موقوتة بالطول التراكمي دون اختراع وصلات. — Draw many rings/segments as one timed stroke by cumulative length, never inventing joins.
- **متى أستخدمها / when:** حدود دول، شبكات، مسارات متعددة M — borders, grids, multi-M paths.
- **كيف / how:** Store each segment, its length and cumulative start; for a reveal window slice every overlapping segment (emit a MultiLineString); skip slivers < 0.0008 km; never clip the border to the viewport. For freehand renderers split a path with several M commands into separate strokes and distribute progress proportional to length so the brush never bridges them with a scribble. **أرقام / params:** sliver 0.0008 km; length-weighted progress.
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10435-remotion-maps/techniques/maptiler/references/map-explainer-architecture.md` · `kosif-tool/styles/chalkboard`

#### DRAW-09 · سلامة رسم المسارات · SVG draw-on safety · 📦 بأمر تثبيت / one install
- **ماذا / what:** قِس المسار بعد ضبط d، ولا تجعل dasharray في CSS يتصارع مع التحريك. — Measure the path after d is set; never fight CSS dasharray.
- **متى أستخدمها / when:** قبل رندر أي مسار يُرسم — before rendering any draw-on.
- **كيف / how:** HyperFrames lint rules svg_measure_before_path_d and svg_drawon_css_dasharray_conflict catch both bugs; in your own pages measure inside the font/asset ready gate, set dasharray from JS only, and check a still at p = 0 (no stray dot) and p = 1 (no gap).
- **تثبيت / install:** `npx hyperframes lint`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/lint/src/rules/gsap.ts`

#### DRAW-10 · نهر يمتلئ ثم يجري · River fill then flow · 🟢 جاهز / ready
- **ماذا / what:** مجرى يمتلئ من الجبل إلى البحر ثم تجري عليه شرطات ضوء، وفي 3D شريط يتقدم بنطاق الرسم. — A river fills mountain→sea then light dashes run along it; in 3D a ribbon advances by draw range.
- **متى أستخدمها / when:** دورة المياه، أنهار، خطوط أنابيب — water cycle, rivers, pipelines.
- **كيف / how:** same path three times: dry bed #CDE7F7 20 px; water #2B8CE6 pathLength=1 dasharray '1 1' dashoffset 1→0 (7.3–8.7 s); flow #A9DBFF 6 px dasharray '0.04 0.07' dashoffset −0.35·t, fading in at 8.4 s. three-kit: makeRibbon(curve, {segments:220, radius:11, radial:10}) revealed with geometry.setDrawRange. **أرقام / params:** dashes .04/.07; −0.35·t.
- **الدليل / proof:** `kosif-one/projects/water-cycle-animation/index.html` · `kosif-studio/motion/kit/three-kit.js`

#### DRAW-11 · المحراب بقلم ذهبي · Gold-pen arch draw-on · 🟢 جاهز / ready
- **ماذا / what:** قوس المحراب وقوس داخلي يُرسمان كقلم ذهبي في البداية، ثم يثخن الخط عند «آمين». — The mihrab arch draws like a gold pen and thickens on the final 'آمين'.
- **متى أستخدمها / when:** أدعية، مناسبات دينية، بطاقات إسلامية — duas and Islamic occasions.
- **كيف / how:** stroke url(#gold) linear gradient #fff0b3 / #e8b04a / #fff0b3, width 7 round caps; drawPath(tl, path, 0, 1.7, {ease:E.out}); inner arch #f3c766 opacity .55 width 3 at 0.25 s; at the amen word stroke-width 7 → 9; arch d = 'M150,1760 L150,1010 C150,770 370,610 540,520 C710,610 930,770 930,1010 L930,1760' (1080×1920). **أرقام / params:** 1.7 s E.out; 7 → 9 px.
- **الدليل / proof:** `kosif-one/projects/thursday-dua-animation/source/index.html`

#### DRAW-12 · رسوم خطية صغيرة فوق الفيديو · Line micro-graphics over footage · 🟢 جاهز / ready
- **ماذا / what:** رسوم عاجية رفيعة توضح كل مثال منطوق لنحو 1.2 ث: ساعة 24 علامة، مسار حلم، مسطرة قياس، سيارة بخط واحد، شريط وقت ينضب. — Thin ivory line drawings illustrating each spoken example for ~1.2 s.
- **متى أستخدمها / when:** مونتاج متكلم فاخر — premium talking-head edits.
- **كيف / how:** stroke 2–3 px #F5F0E6 with #E7B65A accents; car body stroke 2.6 round joins + wheels r 19, road = 6 gold dashes sliding −70 px; clock ring r 150 with 24 ticks (every 6th longer, 3 px) and a hand rotating 360° in 1 s; ticks appear right after the ring: opacity .9, 0.08 s each, stagger .035 s; rail 460 px with 18 ticks sliding x −24→0. **أرقام / params:** ~1.2 s per example; ticks stagger 35 ms.
- **الدليل / proof:** `kosif-studio/motion/projects/premium_edit/index.html:56` · `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:198` · `kosif-studio/out/FINAL_EDIT/EDIT_NOTES.txt`

#### DRAW-13 · أيقونات المعنى المرسومة · Meaning icons drawn on · 🟢 جاهز / ready
- **ماذا / what:** أيقونة خطية تُختار من معنى السطر وتُرسم فوقه ثم تتنفس مع الإيقاع، والأرقام تعدّ بدلًا منها. — A stroke icon picked from the line's meaning, drawn on and breathing on the beat.
- **متى أستخدمها / when:** قصائد، أغانٍ، دروس بنص عربي — poems, songs, Arabic text lessons.
- **كيف / how:** verse.html: 12 icons (sun, moon, heart, clock, money, trophy, road, question, check, home, rain, light) in a 200×200 box, stroke 5 round, accent colour; drawPath per stroke 0.7 s, stagger 0.06 s; breathe 1 + .06·beat + .04·rms; kind 'count' with a value counts up (150 px). Basma: 16 stroke motifs (sun, cloud, wave, drop, bulb, heart, star, check, chart, target, clock, mountain, phone, people, doc, arrow) with fill outlines for hatching and an Arabic keyword matcher MK.motifFor (شمس/سحاب/بحر/فكر/قلب/نمو/هدف/وقت/جبل…) else 8 defaults. **أرقام / params:** 0.7 s, stagger .06 s; 200×200, stroke 5.
- **الدليل / proof:** `kosif-studio/motion/templates/verse.html` · `100-superskills/skills/kosif-montage-motion/templates/verse.html:258` · `app/public/js/10_studio.js:245`

#### DRAW-14 · قوالب موشن بالقلم · Pen-drawn motion templates · ✅ مُثبت هنا / proven here
- **ماذا / what:** قالبان جاهزان: كشف الشعار بالقلم (رسم ← تعبئة ← اسم وشعار نصي) وقائمة نقاط بعلامات صح مرسومة. — Two ready templates: pen logo reveal and a bullet list with drawn ticks.
- **متى أستخدمها / when:** شعار بسيط أو خطوات قصيرة في دقائق — a quick logo sting or short steps.
- **كيف / how:** python scripts/mtemplates.py new NAME --template logo-reveal --set name=… tagline=… (6 s; default hexagon path viewBox 120×136, accent #E7B65A, bg #0f1a2b→#06101c, tagline 'حركة لها معنى') or --template bullet-list (8 s; ≤6 items each with a drawn check; 'ثلاث خطوات' / 'خطّط|نفّذ|راجع'; accent #5BD1A5). Also from the web studio Projects tab or MCP kosif_project_create. Every template generated and linted here (TemplateTests). **أرقام / params:** 6 s / 8 s; ≤6 items.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/mtemplates.py:48` · `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:14` · `100-superskills/skills/kosif-montage-motion/tests/test_v6.py`

## الكتابة اليدوية — Handwriting & write-on

_العنوان يُكتب أمام العين — بالقناع للعربية، وبترتيب الضربات للاتينية._

#### DRAW-15 · كتابة بقناع فرشاة من اليمين · Brush-mask write-on (RTL) · 📄 موصوف / documented only
- **ماذا / what:** ضربة فرشاة سميكة تكشف عبارة عربية مكتملة من اليمين إلى اليسار — كشف لنص مُشكّل لا توليد حروف. — A thick brush stroke reveals a finished Arabic phrase right to left — a reveal of shaped text, not generated glyphs.
- **متى أستخدمها / when:** افتتاحيات دافئة، عناوين بخط يدوي، شعار نصي — warm openings, handwritten titles.
- **كيف / how:** Typeset the phrase in a real Arabic face (Aref Ruqaa, Marhey, Amiri), then animate a thick SVG stroke (dashoffset) or a soft-edged rect used as a mask: 0–0.5 s stroke starts, 0.5–2.5 s reveal, 2.5–4 s read; script headlines: mask wipe ~800 ms with gold gradient #f5c542→#d8a664 and soft shadow; sticky-note handwriting: one line per 500 ms; Latin goes left→right. See ARAB-22 for the soft-mask + pen-tip version. **أرقام / params:** 4 s MG-015; wipe 500–800 ms per line.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-typography.md` · `kosif-tool/playbooks/hand-drawn.md` · `kosif-tool/styles/pm-deebeeeff-50fcd0`

#### DRAW-16 · كتابة حقيقية بترتيب الضربات (لاتيني) · True glyph write-on with stroke order (Latin) · 📦 بأمر تثبيت / one install
- **ماذا / what:** حروف Caveat معبأة تُكشف بخطوط مركزية مخبوزة لكل حرف بترتيب الكتابة الحقيقي وسرعة قلم تتكيف مع الانحناء ورفع القلم. — Filled Caveat letters revealed by baked per-glyph centrelines in real stroke order.
- **متى أستخدمها / when:** عناوين إنجليزية بخط اليد — handwritten English titles.
- **كيف / how:** HyperFrames block hw-write-title (Caveat 700, 1920×1080, 6 s, GSAP paused timeline); single-stroke alternative: HersheyScript1 / HersheyScriptMed SVG stroke fonts through gen-stroke-path.py to write apex words (neon, chalk, graffiti); seen equivalents: handwriting paths ~40–120 ms per glyph with a marker following. Latin only — Arabic uses the mask (DRAW-15). **أرقام / params:** ~40–120 ms/glyph.
- **تثبيت / install:** `npx hyperframes add hw-write-title`
- **رخصة / license:** Apache-2.0; Hershey fonts carry a public-domain-style notice (unverified)
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/hw-write-title/hw-write-title.html` · `kosif-one/vendor/hyperframes/skills/embedded-captions/assets/strokefonts/HersheyScript1.svg` · `kosif-one/vendor/hyperframes/skills/embedded-captions/scripts/gen-stroke-path.py`

#### DRAW-17 · ترجمة بخط اليد تُكتب · Handwritten typewriter caption · 📄 موصوف / documented only
- **ماذا / what:** جملة بخط يدوي تُكشف تدريجيًا بعد تثبيت تخطيطها كاملًا فلا يعاد توسيطها أثناء الكتابة، مع خط تحتي أو دائرة. — A handwritten-style sentence revealed progressively after its full layout is fixed.
- **متى أستخدمها / when:** ملاحظات فوق فيديو سفر أو فلوج — notes over travel/vlog footage.
- **كيف / how:** lay out the whole sentence first, then reveal over 65% of the clip (delay + duration ≤ 1); place 8–12% inside frame edges on empty area; glyph height 4–5% of H; Latin per character 25–30 ms (Kalam/Caveat 600); Arabic per word or by RTL mask; optional circle via a draw-on ellipse. **أرقام / params:** reveal 0.65 of clip; glyph 4–5% H.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2431-akbun-davinciresolve-caption-template/SKILL.md` · `kosif-tool/styles/pm-himanshutwtxs-5f4b43`

## علامات التأكيد والتعليق — Emphasis marks & annotations

_دائرة، سهم، خط تحتي، تظليل — يد المعلم فوق الكلمة أو الصورة._

#### DRAW-18 · أنماط قلم التحديد · Marker emphasis modes · 📄 موصوف / documented only
- **ماذا / what:** خمسة أنماط حتمية على كلمة: مسح تظليل، دائرة يدوية، خطوط انفجار، خط متموج، شطب تخطيطي. — Five deterministic emphasis styles on a word.
- **متى أستخدمها / when:** الكلمة المفتاحية في عنوان أو جملة — the key word in a title or sentence.
- **كيف / how:** highlight: span inset 0 −6px, radius 3 px, scaleX 0→1 in 0.5 s power2.out at ~0.6 s, multiply blend, colour rgba(255,236,79,.62); multi-line stagger 0.3 s; Arabic starts the swipe from the RIGHT (transform-origin right) and checks contrast; circle: 3 px ellipse border-radius 50% with slight rotation, back.out(1.7) 0.6 s; burst: 12 lines at 30° steps, 40–80 px, stagger 0.03 s; scribble: wavy path 3 px round caps drawn by dashoffset; sketch-out: rough rectangle. Underlines: ::after scaleX 0→1 swapping transform-origin (enter from one side, leave from the other) 0.4 s expo-out, or background-size 0%→100% 1px; thick 4 px rule 400 ms ease-out under the last line. **أرقام / params:** 0.5 s sweep; 12 burst lines; underline 0.3–0.5 s.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/css-marker-patterns.md` · `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/references/css-patterns.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-collage-textures.md`

#### DRAW-19 · دائرة يدوية مرتعشة · Hand-drawn circle emphasis · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** إهليلج غير منتظم بحلقتين يتجاوز بدايته يُرسم حول خطأ أو رابط أو معادلة، مع علامات انفجار أو ✗. — An irregular, overshooting double-loop ellipse drawn around a target.
- **متى أستخدمها / when:** إبراز خطأ، رابط الدعوة، وجه في صورة مصغرة — errors, CTAs, faces in thumbnails.
- **كيف / how:** jittered ellipse path (start and end overlap ~15%), stroke 2–3 px, draw 300–700 ms by dashoffset after the content lands; extras: burst ticks around a label, a short underline and a red ✗; clickbait variant: red ring around the head (300 ms) + curved red arrow sliding in (250 ms) + yellow Impact caption with black stroke. **أرقام / params:** 300–700 ms; 2–3 px.
- **الدليل / proof:** `kosif-tool/styles/pm-0xnfrith-5be616` · `kosif-tool/styles/pm-ik-builds-b8bdcf` · `kosif-tool/styles/pm-tak3sh8-be5012` · `kosif-tool/styles/pm-sab8a-364a5a`

#### DRAW-20 · خربشة توضيحية فوق الصورة · Doodle annotations on footage · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** سهم ودائرة وخط تحتي تُرسم فوق الشيء المقصود، وملاحظات بخط اليد بالأزرق للصحيح والأحمر للخطأ. — Arrows, circles and underlines drawn over the referenced object; handwritten notes, blue right / red wrong.
- **متى أستخدمها / when:** شرح لقطات شاشة، تصحيح أخطاء، دروس — screenshot explainers, corrections, lessons.
- **كيف / how:** MG-105 timing: 0–1 s shot, 1–4 s marks, 4–6 s read; each mark explains one point and never covers the subject (track it if the shot moves); curved arrow drawn first (250–300 ms) then the note types (25–30 ms/char Latin, by word in Arabic); a strike line drawn over the wrong statement; blue #2f7bf5, red #ef3b55. **أرقام / params:** arrow 250–300 ms; 6 s beat.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md` · `kosif-tool/styles/pm-chatgptastra-0d95c7` · `kosif-tool/styles/pm-himanshutwtxs-5f4b43`

#### DRAW-21 · شطب بخربشة ثم إعادة كتابة · Scribble strike-through rewrite · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** خربشة ملتفة تُرسم فوق الكلمات القديمة فتخفت إلى النصف، ثم يصعد السطر الجديد تحتها. — A looping scribble crosses out the old words, then the new line slides up.
- **متى أستخدمها / when:** «لا… بل…»، تصحيح مفهوم — 'not this, but that' moments.
- **كيف / how:** magenta looping scribble path drawn by dashoffset in 300 ms, old words fade to 50%, new line 250 ms easeOutBack from below. **أرقام / params:** 300 ms; 250 ms.
- **الدليل / proof:** `kosif-tool/styles/pm-paulo-kombucha-96431c`

#### DRAW-22 · ملاحظة يدوية داخل إطار · Boxed handwritten callout · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** مستطيل مدوّر مرتعش يُرسم أولًا بلون التأكيد ثم تظهر الكلمات بداخله. — A jittered rounded rectangle draws first, then the handwritten words appear inside.
- **متى أستخدمها / when:** نصيحة جانبية، تعريف مصطلح — side tips, term definitions.
- **كيف / how:** rough rounded-rect path 400 ms in #d17c55, then text 600 ms; HyperFrames hw-box-label also drops the box in with a volume-preserving squash and spring. **أرقام / params:** 400 + 600 ms.
- **الدليل / proof:** `kosif-tool/styles/pm-lemomo-ai-0d9cff` · `kosif-one/vendor/hyperframes/registry/components/hw-box-label/hw-box-label.html`

#### DRAW-23 · علامات rough-notation · Rough-notation marks · 📦 بأمر تثبيت / one install
- **ماذا / what:** تظليل ودائرة وخط تحتي وشطب وإطار وقوس بخطوط خشنة حول الكلمات مع قيمة تقدّم. — Sketchy highlight/circle/underline/strike/box/bracket around words driven by a progress value.
- **متى أستخدمها / when:** Remotion أو صفحة HTML تحتاج علامات جاهزة — Remotion or HTML pages needing ready marks.
- **كيف / how:** Remotion @remotion/rough-notation <Highlight/Circle/Underline/StrikeThrough/CrossedOff/Box/Bracket progress={interpolate(frame,[15,40],[0,1],{extrapolateRight:'clamp'})}>; highlight rgba(255,236,79,0.62); plain HTML: rough-notation npm driven by seek(t), never its own timers. **أرقام / params:** draw window ~25 frames.
- **تثبيت / install:** `npm i rough-notation`
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10436-remotion-markup/text-highlights.md`

#### DRAW-24 · خط الرحلة من اليمين · Journey line draw-on (RTL) · 🟢 جاهز / ready
- **ماذا / what:** خط تقدم 2 بكسل ينمو من الحافة اليمنى، ألوانه تعني الحالة: رمادي قادم، بنفسجي حالي، أخضر مزرق منجز. — A 2 px progress line grows from the right edge; colour stops encode state.
- **متى أستخدمها / when:** مراحل رحلة أو برنامج بالعربية — Arabic step journeys.
- **كيف / how:** ::before line, transform-origin right center, keyframe scaleX 0→1 with opacity .2→1 over 680 ms ease-cinematic (.22,.8,.26,1), delay 160 ms; gradient to left: border 0–38%, primary 38–64%, teal 64–100%; inset 10%. **أرقام / params:** 680 ms; delay 160 ms.
- **الدليل / proof:** `kosif-audit-pro/app/globals.css:981` · `kosif-audit-pro/app/globals.css:1082`

## الخشونة والارتعاش والحبر — Roughness, boil & ink

_النقص المقصود هو ما يجعل الرسم «يدويًا»._

#### DRAW-25 · عدم الكمال المقصود · Deliberate imperfection · 📄 موصوف / documented only
- **ماذا / what:** ارتعاش 1–2 بكسل، أطراف مدورة، تجاوز عند الزوايا، وأجسام من 5–30 ضربة فقط. — 1–2 px wobble, round caps, corner overshoot, objects from 5–30 strokes.
- **متى أستخدمها / when:** كل رسم يدوي — every hand-drawn look.
- **كيف / how:** offset path vertices with seeded noise ±0.5–2 px (Catmull-Rom smoothed), width variation ±10–20%, stroke 2–6 px warm dark ink (#1a1a18, #2a2a2a, #3a2a1e); flat fills that slightly miss the outline; paper/board texture 5–10%, static unless the style boils; keep the seed fixed per stroke so frames do not jitter by accident. **أرقام / params:** wobble 1–2 px; 5–30 strokes; texture 5–10%.
- **الدليل / proof:** `kosif-tool/playbooks/hand-drawn.md:16` · `kosif-tool/styles/map-journey` · `kosif-tool/styles/pm-hbcoop-de365c`

#### DRAW-26 · غليان الخط · Line boil · 📄 موصوف / documented only
- **ماذا / what:** الخطوط تعيد ارتعاشها كل إطارين أو ثلاثة فيبدو الرسم حيًا مرسومًا باليد. — Lines re-wobble every 2–3 frames so the drawing feels hand-animated.
- **متى أستخدمها / when:** دودل، رسوم أطفال، رصاص — doodles, kids' stories, pencil looks.
- **كيف / how:** seed = floor(t·12) (on twos at 24 fps) or floor(t·8) (on threes); amplitude 0.5–1.5 px at 1080p (graphite ±1.2 px, roughness 1.5); or cycle 3 pre-made stroke variants; boil only the drawing, never Arabic text outlines; HyperFrames hw-boil provides the same seeded, seek-safe jitter (off/calm/lively). **أرقام / params:** 8–12 fps; 0.5–1.5 px; 3 variants.
- **الدليل / proof:** `kosif-tool/playbooks/hand-drawn.md:28` · `kosif-atlas/skills/2414-animation/9355-learn-style` · `kosif-tool/styles/pm-nikolajankovic-ce4ff4` · `kosif-one/vendor/hyperframes/registry/components/hw-boil/hw-boil.html`

#### DRAW-27 · رسم خشن بأسلوب Rough.js · Rough.js / Excalidraw sketch rendering · 📦 بأمر تثبيت / one install
- **ماذا / what:** أشكال SVG/Canvas بارتعاش متحكم وتعبئة بخطوط مائلة أو متقاطعة. — Sketchy SVG/Canvas shapes with controllable wobble and hachure/cross-hatch fills.
- **متى أستخدمها / when:** مخططات بإحساس يدوي، سبورة ذهنية — hand-feel diagrams, mind boards.
- **كيف / how:** rough.svg(svg).rectangle(x,y,w,h,{roughness:0–2, fill, fillStyle:'hachure'|'cross-hatch'|'solid', hachureGap, seed}) — fixed seed per element (no accidental boil) or seed = floor(t·12) for deliberate boil; Excalidraw JSON elements carry the same fields (roughness 0/1/2, strokeStyle solid|dashed|dotted). Reveal drawn elements with DRAW-01. **أرقام / params:** roughness 0–2; fixed seed.
- **تثبيت / install:** `npm i roughjs`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog.md` · `kosif-atlas/skills/2790-work/11181-draw-excalidraw`

#### DRAW-28 · خطوط بضغط perfect-freehand · Pressure strokes (perfect-freehand) · 📦 بأمر تثبيت / one install
- **ماذا / what:** النقاط على المسار تتحول إلى مضلع خط بعرض متغير كالحبر أو الماركر أو الطباشير، ويُرسم تدريجيًا بتمرير جزء من النقاط. — Path points become a variable-width ink/marker/chalk polygon, drawn progressively by passing a prefix of the points.
- **متى أستخدمها / when:** سبورة ودودل وطباشير بجودة يدوية — premium whiteboard, doodle and chalk.
- **كيف / how:** sample with getPointAtLength (clamp to L − 1e-4); getStroke(points.slice(0, n·ease(p)), {size, thinning, simulatePressure}) → fill the outline polygon; marker size 8–10 thinning .6; chalk size 6–8 thinning .5 drawn twice (halo ×2.2 at ~0.12 opacity, then the stroke); doodle 3–6 px at 720 w ink #2f2820 with pressure from sin over arc length; cache static shapes. **أرقام / params:** marker 8–10/.6; chalk 6–8/.5; halo ×2.2.
- **تثبيت / install:** `npm i perfect-freehand`
- **الدليل / proof:** `kosif-tool/styles/whiteboard` · `kosif-tool/styles/chalkboard` · `kosif-tool/styles/doodle`

#### DRAW-29 · حبر بصمة بضغط وتظليل · Basma INK pressure strokes & hatching · 🟢 جاهز / ready
- **ماذا / what:** خط يُرسم تدريجيًا بطول القوس بأطراف مدببة وضغط متغير ويعيد رأس القلم، وتعبئة شكل مغلق بتظليل مائل تدريجي كالماركر. — Progressive tapered pressure strokes returning the pen head, plus progressive diagonal hatching.
- **متى أستخدمها / when:** محرر بصمة وأفلام السبورة فيه — the Basma editor and its board films.
- **كيف / how:** INK.stroke(c, pts, k, w, col, seed, {plain, alpha}): cumulative length; taper = min(1, .35 + 5u, .35 + 5(1 − u)); pressure .74 + .26·sin(0.9i + 3.7·seed); INK.strokes runs a list sequentially sharing progress by length; INK.at returns the point at fraction k. INK.hatch(c, outline, k, col, gap, w, alpha=.5) clips to the outline and draws diagonal lines up to k of the span. **أرقام / params:** taper .35 + 5u; pressure .74 ± .26.
- **الدليل / proof:** `app/public/js/10_studio.js:208` · `app/public/js/10_studio.js:232`

#### DRAW-30 · محرك فرشاة الحبر الحتمي · Deterministic ink-brush engine · 📄 موصوف / documented only
- **ماذا / what:** المسارات تُرسم بكبسولات فرشاة مع ضبابية JS قابلة للفصل وطبقات نغمية وحبيبات ورق، فيعطي المدخل نفسه نفس البكسلات. — Paths rendered through capsule dabs, separable JS blur, tone layers and paper grain — identical pixels every time.
- **متى أستخدمها / when:** أسلوب حبر وفرشاة جافة فاخر — premium ink and dry-brush looks.
- **كيف / how:** capsule dabs of width 2·bias along contours; implement blur in JS because Chromium ctx.filter blur silently no-ops below ~0.8 px (source blur σ ≈ 0.85 px); tone layers at several greys for dry-brush; paperGrain opacity (off for a faithful copy); expose window.renderFrame(t) for frame capture. **أرقام / params:** blur floor 0.8 px; σ 0.85.
- **الدليل / proof:** `kosif-atlas/skills/2414-animation/9357-rotoscope/SKILL.md` · `kosif-atlas/skills/2414-animation/9357-rotoscope/reference/method.md`

#### DRAW-31 · ملمس الرصاص والطباشير بالمرشحات · Pencil & chalk texture filters · 📄 موصوف / documented only
- **ماذا / what:** ملمس رصاص من feTurbulence + feDisplacementMap، وغبار طباشير صغير ينفث عند اكتمال كل حد في المعادلة. — Pencil texture via SVG turbulence + displacement, and a chalk-dust puff on each completed term.
- **متى أستخدمها / when:** مشهد رصاص هادئ، معادلات طباشير — quiet pencil scenes, chalk formulas.
- **كيف / how:** <filter><feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="2" seed="7"/><feDisplacementMap in="SourceGraphic" scale="1.5–3"/></filter> on strokes, static seed; chalk: dusty stroke texture + 6–10 small particles that puff out and fade over ~300 ms at each term's completion. **أرقام / params:** displacement 1.5–3; puff ~300 ms.
- **الدليل / proof:** `kosif-atlas/skills/1094-akbun-draw/2419-akbun-draw-quiet-pencil/SKILL.md` · `kosif-tool/playbooks/hand-drawn.md:50`

#### DRAW-32 · خطوط ماء موازية للساحل · Triple coastline water lines · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** يُخطّ حد البحر ثلاث مرات بعروض متناقصة بالتناوب بين الحبر ولون البحر داخل مضلع البحر، فتظهر ثلاث تموجات موازية. — The sea boundary stroked three times inside the sea polygon for three parallel ripples.
- **متى أستخدمها / when:** خرائط مرسومة وقصص رحلات — hand-drawn maps and journeys.
- **كيف / how:** clip to the sea polygon; stroke widths ~18 / 12 / 6 px alternating ink #5d5140 then sea #bfcdbe on top. **أرقام / params:** 18/12/6 px.
- **الدليل / proof:** `kosif-tool/styles/map-journey`

## أساليب الرسم اليدوي الجاهزة — Hand-drawn styles

_أساليب كاملة في الكتالوج ومحرر بصمة — اختر واحدًا وابنِ عليه._

#### DRAW-33 · سبورة بيضاء · Whiteboard · 🟢 جاهز / ready
- **ماذا / what:** رسم بالماركر على سبورة خطوة بخطوة بيد أو بلا يد، متزامن مع الصوت، ثم انتقال إلى مساحة نظيفة. — Marker drawing step by step with or without a hand, synced to the voice, then a pan to clean space.
- **متى أستخدمها / when:** دروس وشروحات بتعليق صوتي — narrated lessons.
- **كيف / how:** python3 tools/kosif.py scaffold whiteboard <dir> (playbook hand-drawn); hold 1.5–2 s at sentence end, then pan one board-width in 800 ms ease-in-out; each sentence triggers its element's draw-on (start = sentence onset). Basma STY.whiteboard: 16:9, calm, 2.0 wps, font Marhey, bg #F4F4F1, ink #23272E, accent #E0412E, colours #1E63D6 / #E0412E / #F28C12 / #2E9B4F; sfx write=pen, line=click, end=shimmer; lines revealed right→left behind the pen. style:whiteboard wrote an Arabic title with a soft mask and marker tip. **أرقام / params:** hold 1.5–2 s; pan 800 ms; 2.0 wps.
- **الدليل / proof:** `kosif-tool/styles/whiteboard/SKILL.md` · `kosif-tool/playbooks/hand-drawn.md:29` · `app/public/js/10_studio.js:342`

#### DRAW-34 · سبورة سينمائية · Whiteboard cinematic · 🟢 جاهز / ready
- **ماذا / what:** شرح السبورة مع دفع كاميرا وعمق وتأطير درامي بين الرسومات. — Whiteboard explainer upgraded with camera dolly, depth and dramatic framing.
- **متى أستخدمها / when:** شرح أطول يحتاج طاقة — longer explainers that need energy.
- **كيف / how:** python3 tools/kosif.py scaffold whiteboard-cinematic <dir>; draw-on 800–1400 px/s with a hand pinned to the tip; after a 1.5–2 s hold the camera pushes/pans to clean board space; pen 4/8 px; texture 5–10%. **أرقام / params:** pen 4/8 px; texture 5–10%.
- **الدليل / proof:** `kosif-tool/styles/whiteboard-cinematic/SKILL.md` · `kosif-tool/styles/whiteboard-cinematic/STYLE.json`

#### DRAW-35 · سبورة الطباشير · Chalkboard · 🟢 جاهز / ready
- **ماذا / what:** رسم بالطباشير على سبورة خضراء أو سوداء بحبر معكوس، لدروس الرياضيات والعلوم. — Chalk on a green/black board with inverted ink.
- **متى أستخدمها / when:** رياضيات، علوم، معادلات — maths, science, formulas.
- **كيف / how:** python3 tools/kosif.py scaffold chalkboard <dir>; draw-on 800–1400 px/s, chalk-textured strokes, board texture 5–10%. Basma STY.chalkboard: 16:9, calm, 1.9 wps, font Aref Ruqaa, bg #264A3E, ink #F3F1E7, accent #F6E07A, colours #F6E07A / #F4A9BC / #9AD3F0 / #A9E6A2; sfx write=chalk, line=tick, end=shimmer. All timings × one slowness factor TS (EASE-08). **أرقام / params:** 1.9 wps; #264A3E / #F3F1E7.
- **الدليل / proof:** `kosif-tool/styles/chalkboard/SKILL.md` · `app/public/js/10_studio.js:471`

#### DRAW-36 · قصص الدودل · Doodle stories · 🟢 جاهز / ready
- **ماذا / what:** عالم مرسوم بالحبر في لقطة واحدة مستمرة، شخصية تمشي، وكلام كلمة بكلمة مع كلمة متوهجة. — An ink world in one continuous take with a walking character and word-by-word speech.
- **متى أستخدمها / when:** حكايات وقصص أطفال وأمثال — tales, kids' stories, proverbs.
- **كيف / how:** python3 tools/kosif.py scaffold doodle <dir>; boil 3 stroke variants every 2–3 frames; continuous camera through the world; every sentence spawns one prop (sign, question bubble, heart card) popping 0→1.08→1. Basma STY.doodle: 9:16, calm, 1.9 wps, Tajawal; sky #AFDCF0→#EAF6F4, sand #F1D9AE, grass #BCDB92, water #6FB3C8, ink #3A2A1E, text #1E2B45, emphasis #F07F2E, glow #FFD0A0, robe #F6F0E4, turban #2F4E86, skin #C98B5B; sfx pop/shimmer/swish/swell. **أرقام / params:** 9:16; 1.9 wps.
- **الدليل / proof:** `kosif-tool/styles/doodle/SKILL.md` · `app/public/js/10_studio.js:854`

#### DRAW-37 · قلم البلوتر · Plotter pen · 🟢 جاهز / ready
- **ماذا / what:** قلم بلوتر ميكانيكي يرسم منحنى بسرعة ثابتة على ورق شبكي داكن بشرارة برتقالية وتعليقات أحادية العرض. — A mechanical pen plotter traces a curve at constant speed with an orange spark and mono annotations.
- **متى أستخدمها / when:** شرح تقني وبرمجي — tech explainers.
- **كيف / how:** python3 tools/kosif.py scaffold plotter <dir>; constant pen speed, no easing, optional pen-up travel lines at 10%. Basma STY.plotter: 16:9, tech, 2.2 wps, Readex Pro + IBM Plex Mono, bg #0B0B0C, ink #F4F4F2, dim #3A3A3E, accent #FF5A1F, grid rgba(255,255,255,.055) at 6.2% drifting 3 px/s, 180-point seeded curve, timeline ruler and STEP counters, vignette 0.5 + grain 0.08; style:plotter spark: line 1.5 px bone-white, core 6 px #f27525, glow 10 px, 1–2 s per stroke. **أرقام / params:** 2.2 wps; spark 6 px; grid drift 3 px/s.
- **الدليل / proof:** `kosif-tool/styles/plotter/SKILL.md` · `app/public/js/10_studio.js:292` · `kosif-tool/styles/plotter`

#### DRAW-38 · إطار بإطار على اثنين · Frame-by-frame on twos · 🟢 جاهز / ready
- **ماذا / what:** إحساس الرسوم التقليدية المرسومة لكل إطار: رسمة جديدة كل إطارين وغليان بثلاث نسخ. — Traditional per-frame drawn feel: a new drawing every 2 frames, boil with 3 variants.
- **متى أستخدمها / when:** لحظات عاطفية أو فنية — emotional or artistic moments.
- **كيف / how:** python3 tools/kosif.py scaffold frame-by-frame <dir>; swap drawings every 2 frames (12 drawings/s at 24 fps); boil with 3 stroke variants every 2–3 frames; camera moves stay on ones (EASE-77). **أرقام / params:** 12 dps.
- **الدليل / proof:** `kosif-tool/styles/frame-by-frame/SKILL.md` · `kosif-tool/styles/frame-by-frame/STYLE.json`

#### DRAW-39 · رسومات الماركر للقصص · Marker-doodle story illustrations · 📄 موصوف / documented only
- **ماذا / what:** مظهر التسجيل البصري: ورق كريمي، حدود كحلية مرتعشة، تظليل ماركر يتجاوز الخطوط، 3–5 ألوان زاهية، حشود بيضاء بلا وجوه، وأسهم تأكيد حمراء. — The graphic-recording look.
- **متى أستخدمها / when:** قصة من 2–5 مشاهد: مقدمة ← مشكلة ← حل — 2–5 scene stories.
- **كيف / how:** Procedural here: SVG jittered strokes + hatch patterns + draw-on; or one generated plate per beat with a fixed CHARACTER sentence reused verbatim (models have no memory), English prompt slots only, 1–2 short labels max, then reveal the plate with a draw-on mask or wipe — set any Arabic as real type on top (ARAB-09). **أرقام / params:** 3–5 colours; 2–5 scenes.
- **الدليل / proof:** `kosif-atlas/skills/1094-akbun-draw/2421-akbun-draw-storytellingimage/SKILL.md`

#### DRAW-40 · مشهد الرصاص الهادئ بلون واحد · Quiet pencil one-accent scene · 📄 موصوف / documented only
- **ماذا / what:** مشهد رصاص رمادي على ورق كريمي، ثلثاه الأعليان فارغان، 1–3 أشخاص صغار على خط أرض منخفض، وشيء واحد فقط بلون أزرق مخضر حيث يقع المعنى. — Graphite scene on cream paper, top two-thirds empty, one teal object where the meaning lands.
- **متى أستخدمها / when:** سرد تأملي، بطاقات نهاية — reflective narration B-roll, end cards.
- **كيف / how:** paper #F4ECDC, 4:3, graphite #4A4A4A–#9A9A9A hatching only, figure seen from behind, ONE flat teal #2E7D8C prop; pencil texture (DRAW-31) with slow draw-on; in motion animate only the coloured object or use it as the transition anchor; the subject changes, the style never does. **أرقام / params:** #F4ECDC; #2E7D8C; top 2/3 empty.
- **الدليل / proof:** `kosif-atlas/skills/1094-akbun-draw/2419-akbun-draw-quiet-pencil/SKILL.md`

#### DRAW-41 · إطارات ستوري بورد بالرصاص · Pencil storyboard frames · 📄 موصوف / documented only
- **ماذا / what:** إطارات 16:9 بالرصاص الرمادي بلا لون إلا خطوط حمراء رفيعة لمحور الكاميرا وخط النظر، وكاميرا مرسومة على حامل بسهم اتجاه. — Grey-pencil 16:9 storyboard frames with red camera-axis lines.
- **متى أستخدمها / when:** تخطيط لقطات قبل التصوير أو التوليد — planning shots before filming or generating.
- **كيف / how:** per shot fill props, camera position, person view, action, frame cut line; render procedurally (jittered SVG strokes, dashed frame rectangle, handwritten dimension notes) or via an image model (external). **أرقام / params:** 16:9; grey pencil + red axis.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2449-akbun-vlog-storyboard/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2448-akbun-vlog-shotsketch/SKILL.md`

#### DRAW-42 · خريطة رحلة مرسومة باليد · Hand-drawn route sketch map · 📄 موصوف / documented only
- **ماذا / what:** رسم مسطح بملمس الطباشير الملون لمسار رحلة: محطات مرقمة على ورق كريمي وخطوط ملونة بلا طرق مخترعة. — Crayon-textured trip map with numbered stops and no invented roads.
- **متى أستخدمها / when:** قصص سفر ومدونات — travel stories.
- **كيف / how:** paper #FBF6E9, confirmed path #B9AEA6, routes #8CC63F / #8E6BB0 / #F2A03D, greenery #DDE8B5 #7FB241 #3F6B2A, water #A9CDE8, ink #2B2B2B, panel #F7F1DC; 3:4; numbers only as text; without direction info stops flow top→bottom; draw with a rough stroke filter and animate route draw-on (DRAW-01). **أرقام / params:** 3:4; 3 route colours.
- **الدليل / proof:** `kosif-atlas/skills/1094-akbun-draw/2422-akbun-draw-travel-blog/SKILL.md`

#### DRAW-43 · مخططات تجادل لا تعرض · Diagrams that argue (sketch patterns) · 📄 موصوف / documented only
- **ماذا / what:** الشكل يحمل المعنى: تفرّع، تقارب، شجرة، دورة، سحابة، خط إنتاج، مقارنة، فجوة — ولو حذفت النص يبقى المعنى. — Shape carries the argument; remove the text and it still communicates.
- **متى أستخدمها / when:** شرح فكرة معقدة بالرسم — explaining an idea by drawing.
- **كيف / how:** timelines as a line with 10–20 px dots and free labels; trees as trunk + branch lines; assembly line chaos → process → order; Excalidraw-style roughness 0 smooth / 1 default / 2 rough; reveal strokes in argument order. See EXPL for full diagram powers. **أرقام / params:** dots 10–20 px; roughness 0–2.
- **الدليل / proof:** `kosif-atlas/skills/2790-work/11181-draw-excalidraw/references/visual-patterns.md` · `kosif-atlas/skills/2790-work/11181-draw-excalidraw/SKILL.md`

#### DRAW-44 · رسوم خطية استعارية تتحرك · Line-art metaphor motions · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** رسم خطي بسيط يتحرك ليقول الفكرة: ناسخة تُخرج نسخًا وبقعة حمراء تنتشر، حديقة تنمو من جذورها، أقواس تحريك حول كوب، يدان تطلقان شيئًا يكمل وحده. — Simple line art that moves to state the idea.
- **متى أستخدمها / when:** استعارات في الشرح والإعلان — metaphors in explainers and ads.
- **كيف / how:** copier: 2 px charcoal outline, pages slide out 600 ms, a red blot spreads to show the error copied everywhere; garden: flowers scaleY from the root (transform-origin bottom) 500–700 ms easeOut, stagger 80 ms, insects on Lissajous paths with wing flap scaleX at 8 Hz; stirring: two thin elliptical arcs rotating ~1 turn/s; hands release: 900 ms cubic-bezier(.33,1,.68,1), 120 ms hold, then linear drift; hang strings: 1 px gold lines draw down, then the word drops on a spring. **أرقام / params:** 600 ms; 8 Hz flap; 900 ms release.
- **الدليل / proof:** `kosif-tool/styles/pm-henkvaness-0e06af` · `kosif-tool/styles/pm-abderrahmen-g-9e8ed0` · `kosif-tool/styles/pm-sarut0bisasuke-cefa43` · `kosif-tool/styles/pm-robvjourney-ce3e1a/BRIEF.md`

#### DRAW-45 · قص الرسومات من صفحة الكراسة · Sketch cut-out lift & eraser wipe · 📄 موصوف / documented only
- **ماذا / what:** رسومات ممسوحة تُرفع عن صفحة كراسة مصورة بأقنعة شفافية وتتحرك كقصاصات، والمسح بشكل ممحاة. — Scanned drawings lifted off a sketchbook page via alpha masks; eraser-shaped wipes.
- **متى أستخدمها / when:** كولاج يدوي من رسومات المستخدم — handmade collage from the user's own drawings.
- **كيف / how:** PNG alpha cut-outs moved only by translate, rotate ≤ ±12° and uniform scale — never recolour or trace the user's art; line boil by cycling 2–3 scan variants or 2 px jitter held on threes (8 fps); eraser wipe: a 400 ms mask following an eraser sprite's path. **أرقام / params:** rotate ≤ ±12°; boil 8 fps 2 px; wipe 400 ms.
- **الدليل / proof:** `kosif-tool/styles/pm-abderrahmen-g-9e8ed0/BRIEF.md` · `kosif-tool/styles/pm-tak3sh8-be5012/BRIEF.md`

#### DRAW-46 · شريط مخطط يُرسم · Striped ribbon draw-on · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** ثلاثة خطوط متوازية بالأحمر والأبيض والأزرق تُرسم معًا على منحنى. — Three parallel offset strokes draw together along a curve.
- **متى أستخدمها / when:** رياضة، أعلام، مناسبات — sports, flags, occasions.
- **كيف / how:** one curve, three strokes at offsets (width ~30 px total) drawn by dashoffset over 1.5 s; for Arab flags swap to their real colours. **أرقام / params:** 1.5 s; ~30 px.
- **الدليل / proof:** `kosif-tool/styles/pm-mrtanviir-132457` · `kosif-tool/styles/pm-umangratani-57f86a`

#### DRAW-47 · من مخطط سلكي إلى مجسم · Wireframe draw → solid formation · 🟢 جاهز / ready
- **ماذا / what:** حواف شبكة سلكية تُرسم متتابعة، وشريط مسح يصعد على المجسم بحافة لامعة، ثم يتشكل المجسم النهائي من المخطط. — Mesh edges draw on, a scan band sweeps up the model, and the finished object forms from the schematic.
- **متى أستخدمها / when:** «رقمنة» منتج أو شخصية، تقنية — digitising a product/character.
- **كيف / how:** SVG edges dashoffset staggered (~1.5 s total); three.js: wireframe ShaderMaterial on the same geometry, band = smoothstep(.09, 0, scan − y)·step(y, scan + .004), edge = smoothstep(.012, 0, |y − scan|), colour (.62,1,.72)→(.95,1,.8), scanY lerp(−.02, .4) over .78 s, ground ring 0xd0ff6a scale 1.15→0.6; schematic(obj).set(form = 1 − ease(ramp(t, .4, 2.8))), explode(.35·pulse), joints glow (three-kit bundle in the kit folder). **أرقام / params:** scan .78 s; form ramp .4–2.8 s.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:59` · `100-superskills/skills/kosif-montage-motion/scripts/projects/lab_rabbit_lion/src/main.js:19` · `kosif-tool/styles/pm-tdinh-me-815acb`

## الرسم بكسلًا بكسلًا والتتبع — Painter studio & tracing

_الصورة تتكون أمام العين بترتيب رسام، وتنتهي مطابقة للأصل._

#### DRAW-48 · ترتيب الرسام في الكشف · Painter reveal orders · ✅ مُثبت هنا / proven here
- **ماذا / what:** بكسلات كل خطوة تُرتب كما يضعها الرسام: فرشاة ذهابًا وإيابًا، نمو من نقطة، صعود من القدمين، نزول، يمين، يسار، أو تناثر للتفاصيل. — Each step's changed pixels laid down in painter order.
- **متى أستخدمها / when:** فيلم «الصورة تُرسم» — 'picture being painted' films.
- **كيف / how:** Step(name, ops, order='sweep'|'grow'|'rise'|'down'|'left'|'right'|'sparkle', origin=(x,y), weight); reveal_order(idx, W, step, scale, seed) returns a permutation; sweep bands round(7·scale) px boustrophedon with jitter 26·scale; grow = distance to origin + jitter 9·scale; rise/down/left/right jitter 7·scale; sparkle random. Permutation test passed here. **أرقام / params:** band 7·scale px; jitter 7–26·scale.
- **الدليل / proof:** `kosif-studio/render.py:846` · `kosif-studio/tests/test_studio.py:93` · `100-superskills/skills/pixel-studio-painter/references/drawing-guide.md`

#### DRAW-49 · فيلم الرسم · Drawing film (picture forming as MP4) · ✅ مُثبت هنا / proven here
- **ماذا / what:** يسجّل أي مشهد أو ملف كود أو صورة وهو يُرسم بكسلًا بكسلًا إلى فيديو H.264 ويثبت الإطار الأخير. — Records any scene, code file or image being painted into H.264, holding the final frame.
- **متى أستخدمها / when:** تايم لابس رسم، «كيف رُسمت هذه» — painting timelapses.
- **كيف / how:** python film.py drawing <scene|code|image> --out x.mp4 [--fps 30 --speed slow|normal|fast]; python film.py animate page.html|scene.py --out x.mp4 --seconds 6; dur per step = SPEEDS[speed]·weight·√(n/area) (EASE-82); images wrapped as image code; native canvases fit into 1280×720 on #1b1b1b; libx264 preset medium crf 18 yuv420p, GOP 2·fps, +faststart; hold 1.5 s. Encode test passed here. **أرقام / params:** 30 fps; crf 18; hold 1.5 s.
- **الدليل / proof:** `kosif-studio/film.py:59` · `kosif-studio/tests/test_studio.py:305` · `100-superskills/skills/pixel-studio-painter/scripts/film.py:229`

#### DRAW-50 · الرسم بترتيب الكود نفسه · PIL command recorder · ✅ مُثبت هنا / proven here
- **ماذا / what:** يلتقط كل أمر مستطيل/إهليلج/مضلع/خط/قوس/نص في Pillow فتتكون الصورة بالترتيب الذي رسمها به الكود. — Every Pillow draw call is snapshotted so the picture forms in the code's own order.
- **متى أستخدمها / when:** «اكتب كود يرسم… وأرني وهو يرسم» — showing code-drawn art being drawn.
- **كيف / how:** Recorder.install() wraps ImageDraw methods, Image.paste/alpha_composite and save/show; consecutive calls of one kind are grouped (RUN = 20 commands per stroke: 360 sky lines → 18 strokes); stream thinned above 300 snapshots; labels are Arabic call names with counts; final job 'اللمسات الأخيرة'; image code is read as data, never executed. Runner tests passed here. **أرقام / params:** 20 commands/stroke; ≤300 snapshots.
- **الدليل / proof:** `kosif-studio/runner.py:247` · `kosif-studio/runner.py:39` · `kosif-studio/tests/test_studio.py:331`

#### DRAW-51 · الرسم المطابق تمامًا · Exact-match painting · ✅ مُثبت هنا / proven here
- **ماذا / what:** يعيد رسم أي صورة من ورقة شفافة على مراحل رسام وينتهي مطابقًا للأصل في كل قيمة RGBA: كتل لونية ثم تدقيق نغمي ثم تصحيح كل بكسل متبقٍ. — Repaints any image in painter stages and ends identical in every RGBA value.
- **متى أستخدمها / when:** إعادة رسم شعار أو صورة كفيلم «يدوي» قابل للإثبات — a provable hand-made recreation.
- **كيف / how:** exact.plan(rgba, block_k, fine_k): block-in uses the logo's own palette or Lab k-means on a bilateral-filtered copy (+median 5) with jobs 'grow' weight .9; refine splits changed pixels into luminance tertiles (shadows, mid-tones, lights) as 'sparkle' weight .7 (change threshold Σ|diff| > 12); final touches go from visible to invisible; asserts array_equal; photos try 4 plans (6/10/16/24 block colours) in ~3 s. Exact and JevPlan tests passed here. **أرقام / params:** bilateral 9/40/9; k-means ≤60000 samples, 40 iters.
- **الدليل / proof:** `kosif-studio/exact.py:1` · `kosif-studio/exact.py:151` · `kosif-studio/tests/test_studio.py:157` · `100-superskills/skills/pixel-studio-painter/scripts/exact.py`

#### DRAW-52 · صورة إلى برنامج بايثون · Image to standalone Pillow program · ✅ مُثبت هنا / proven here
- **ماذا / what:** يكتب برنامج Pillow فقط يرسم مضلعات ثم يكمل البكسلات من الأصل المضمّن ويتحقق من نفسه. — Writes a Pillow-only program that draws polygons, completes pixels from the embedded original and self-verifies.
- **متى أستخدمها / when:** «حوّل الصورة إلى كود» — 'turn this image into code'.
- **كيف / how:** python3 to_python.py <image> (or studio.py --image-code); --data-only form; the program reproduces the image with plain Python (ImageToPython test passed here).
- **الدليل / proof:** `kosif-studio/tests/test_studio.py:185` · `100-superskills/skills/pixel-studio-painter/scripts/to_python.py`

#### DRAW-53 · استيراد SVG والتحويل إلى متجهات · SVG import & vectorize to draw steps · ✅ مُثبت هنا / proven here
- **ماذا / what:** كل عنصر SVG يصبح خطوة رسم بالترتيب، والشعار المسطح يتحول إلى متجهات بألوانه وثقوبه. — Every SVG element becomes a drawing step; flat logos vectorize keeping colours and holes.
- **متى أستخدمها / when:** رسم شعار المستخدم أمام العين — drawing the user's logo on screen.
- **كيف / how:** svg_import.py honours shapes, styles, transforms (rect, circle, ellipse, polygon, path arcs/smooth curves, gradients, text); vectorize keeps a flat logo's palette and its holes and treats noise as a photo; holes and even-odd compounds render correctly. Svg, Vectorize and Renderer tests passed here.
- **الدليل / proof:** `kosif-studio/svg_import.py:369` · `kosif-studio/tests/test_studio.py:105` · `100-superskills/skills/pixel-studio-painter/scripts/svg_import.py`

#### DRAW-54 · محوّل مسارات SVG إلى نقاط · SVG path sampler · ✅ مُثبت هنا / proven here
- **ماذا / what:** تحويل بيانات مسار SVG (مطلق/نسبي، منحنيات مكعبة وتربيعية) إلى نقاط بايثون خالصة لإعادة استخدامها في رسم تدريجي. — Pure-Python sampling of SVG path data into polylines for draw-on.
- **متى أستخدمها / when:** رسم مسار في Pillow أو أي محرك بلا متصفح — draw-on outside the browser.
- **كيف / how:** desktop._svg_paths(d) → list of point lists (M/L/H/V/C/Q/T/Z, curves sampled not chorded, closed paths return to start); _shape_paths(shapes); _fit_tf(paths, box, margin=0.08, viewbox); reveal points up to t in a render(t). Drawing tests 4/4 passed here. **أرقام / params:** margin 0.08; arcs every 6° (≥12 points).
- **الدليل / proof:** `kosif-one/tools/kosif-omni/mcp-server/kosif_mcp/desktop.py:1032` · `kosif-one/tools/kosif-omni/mcp-server/tests/test_desktop.py:259`

#### DRAW-55 · الرسم بالفأرة في برنامج الرسام · Drawing by mouse in Windows Paint · 📄 موصوف / documented only
- **ماذا / what:** يرسم مسارات SVG أو أشكالًا ضربة بضربة في برنامج Paint بقلم صناعي، أو يعيد رسم صورة بكسلًا بكسلًا ويتحقق حتى التطابق. — Draws SVG paths stroke by stroke into Paint, or redraws an image pixel by pixel until identical.
- **متى أستخدمها / when:** على جهاز ويندوز للمستخدم فقط — only on the user's Windows desktop.
- **كيف / how:** kosif_mouse_act window=Paint actions=[{do:'draw', target:'canvas', viewbox:[0,0,100,100], svg:'M…'}]; closed shapes run on 30% past start to seal bucket fills; hatch gap 2 px; kosif_paint_copy image=<png> [zoom 4] [colors 64]: ~0.6–0.68 s per colour, ~1,030 px/s, 85×98 logo with 2,650 colours = 100% in ~25 min, 64 colours ~1.3 min mean ΔE 2.4. Not runnable in this Linux container. **أرقام / params:** limit 200,000 px; 64 colours ≈1.3 min.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-mouse/SKILL.md` · `kosif-one/tools/kosif-omni/mcp-server/kosif_mcp/replicate.py:1003`

#### DRAW-56 · رسم فوق لقطات مولدة · Draw-over film on generated bases · 📄 موصوف / documented only
- **ماذا / what:** المقاطع المولدة تعطي الحركة، وطبقة رسم بالكود هي الصورة الفعلية: حبران على ورق، نقاط هافتون، خطوط تغلي 12 مرة/ث، وكتابة كلمات حركية. — Generated clips give motion; a coded drawing layer is the actual picture.
- **متى أستخدمها / when:** كليب أغنية بطابع مطبوع/مرسوم — a printed/drawn-look music video.
- **كيف / how:** extract base frames with ffmpeg; renderAt(t) draws two inks on paper, halftone, line work, boil 12×/s, fixed paper tooth; shots.json {at, dur, base, baseStart, focus 0..1, type big|quiet|none, side}; render frame-exact in headless Chromium; mux the original audio; contact-sheet every cell; 16:9 and 1080×1920 from the same film. **أرقام / params:** boil 12 fps.
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3903-video/SKILL.md` · `kosif-atlas/skills/1511-homie/3903-video/references/METHOD.md`

#### DRAW-57 · دراسة أسلوب مرسوم بالتتبع · Rotoscope style study & style pack · 📄 موصوف / documented only
- **ماذا / what:** فك رسوم مرجعية إلى رسمات مميزة، تتبعها إلى متجهات، إعادة رسمها وقياسها، ثم حفظ إحصاءات الأسلوب فقط (لوحة، خشونة، سماكة، غليان، ثبات). — Decode, trace, re-render and measure a reference, keeping only style statistics.
- **متى أستخدمها / when:** «اعمل بنفس أسلوب الرسم هذا» دون نسخ الرسوم — 'match this drawn style' without copying it.
- **كيف / how:** dedup drawings by large-grey-step pixel count; threshold at the ink/paper grey midpoint; supersample 4× (8× adds nothing) after an unsharp mask; findContours + approxPolyDP; measure XOR vs codec floor (~0.22%) and SSIM; store p10/p50/p90 bands in style.json and check new scenes against them. Study only — never ship traced third-party geometry or store source frames. **أرقام / params:** S = 4; XOR ~0.22%.
- **رخصة / license:** study tool — do not redistribute traced third-party art
- **الدليل / proof:** `kosif-atlas/skills/2414-animation/9357-rotoscope/reference/method.md` · `kosif-atlas/skills/2414-animation/9355-learn-style/SKILL.md`

#### DRAW-58 · إعادة رسم مخرجات مولدة كمتجهات · Generated raster → hand vector recreation · 🟢 جاهز / ready
- **ماذا / what:** حين لا يمكن تنزيل الصورة المولدة أو يجب أن تبقى حادة بأي حجم، تُعاد يدويًا كـ SVG صغير وتُقيَّم مقابل الأصل. — Recreate a generated raster as a compact SVG and score it against the render.
- **متى أستخدمها / when:** خلفيات وشعارات تحتاج حدة وحركة طبقات — backgrounds and emblems needing sharpness and layers.
- **كيف / how:** valley-dusk.svg: three dune paths with gradients (sky #8f8ae0 → #c9c3f5 → #f1e9fb), palms #4e46a8, flock ellipses, crescent and stars, 1200×600 xMinYMax slice — each dune is a parallax layer; scoring: Canva render 3.84/4 vs vector 3.79/4 for the emblem. **أرقام / params:** sky 2.6 KB SVG.
- **الدليل / proof:** `kosif-earth-ci-fork/ui/art/valley-dusk.svg` · `kosif-earth-ci-fork/docs/design/KOSIF-LUXE.md`

## مكونات ومكتبات جاهزة — Ready components & libraries

_ما يُستدعى بأمر واحد._

#### DRAW-59 · مكونات HyperFrames للرسم اليدوي · HyperFrames hand-drawn components · 📦 بأمر تثبيت / one install
- **ماذا / what:** مكتبة مكونات وكتل يدوية جاهزة تُضاف بأمر واحد، كلها بمحرك GSAP متوقف وقابلة للبحث. — A ready library of hand-drawn components and blocks.
- **متى أستخدمها / when:** تركيبات HyperFrames تحتاج علامات يدوية سريعة — HyperFrames compositions.
- **كيف / how:** npx hyperframes add <name>, mount on a class="clip" div (data-composition-src, data-start/duration/track-index, JSON in data-variable-values). Components: hw-arrow (straight/gentle/swoop, plain/soft/sharp/spray, stretch pulse on arrival), hw-boil (seeded jitter off/calm/lively, wobbly ellipse, curvature-adaptive pen ease), hw-box-label, hw-callout-circle (scribble fill + curved connector), hw-underline (squiggle, double strike, bracket), cursor-annotate (pen draws loop/underline/arrow, #f43f5e, target in %), marker-highlight (highlight|circle|underline|scribble at 0.9 s), vox-annotate (marker + connector to a mono label in one beat), whiteboard-ink (bulb|flow|rocket, pen nib), marker-checklist-card, yt-circle-pointer, svg-stroke-trace (stroke 12), svg-line-draw-loader, stitched-text-draw (fine|coarse needle). Blocks: hw-frame (8 s), hw-path-text (6 s), hw-pipeline (flowchart 7 s), hw-scribble-transition (2.2 s), hw-text-cloud (speech bubble), hw-title, hw-write-title. Latin fonts bundled (Caveat, Permanent Marker, Courier Prime) — swap to an Arabic face and RTL masks for Arabic. **أرقام / params:** 21 items.
- **تثبيت / install:** `npx hyperframes add hw-callout-circle`
- **رخصة / license:** Apache-2.0 (GSAP standard no-charge license inside)
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components` · `kosif-one/vendor/hyperframes/registry/blocks` · `kosif-one/vendor/hyperframes/registry/components/cursor-annotate/cursor-annotate.html` · `kosif-one/vendor/hyperframes/registry/blocks/hw-scribble-transition/hw-scribble-transition.html`

#### DRAW-60 · مكتبات الرسم التدريجي · Draw-on libraries · 📦 بأمر تثبيت / one install
- **ماذا / what:** مكتبات بديلة للرسم التدريجي والخشونة حين لا تكفي dashoffset المكتوبة يدويًا. — Alternative draw-on and roughness libraries.
- **متى أستخدمها / when:** مشاريع npm أو Remotion — npm/Remotion projects.
- **كيف / how:** vivus 0.4 (path draw-on scenarios), roughjs 4.6, rough-notation 0.5, perfect-freehand, @remotion/paths (getLength, evolvePath for draw-on in Remotion), @excalidraw/excalidraw (scene JSON → SVG). Wire every one to seek(t) (set progress directly), never their own requestAnimationFrame timers.
- **تثبيت / install:** `npm i vivus roughjs rough-notation perfect-freehand @remotion/paths`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog.md`

## توليفات قوية / power combos

- **سبورة تعليمية عربية / Arabic whiteboard lesson:** DRAW-33 + DRAW-03 + DRAW-06 + DRAW-04 + ARAB-22 + EASE-08 + VOICE — العنوان يُكتب بقناع من اليمين برأس ماركر، كل جملة ترسم عنصرها بسرعة 800–1400 بكسل/ث، ثبات 1.5–2 ث ثم انتقال لمساحة نظيفة.
- **شرح بيانات مرسوم / sketched data story:** DRAW-01 + DRAW-07 + DRAW-18 + DATA + EXPL — خط البيانات يُرسم برأس متوهج، والرقم المهم يُحاط بدائرة يدوية ويُظلل.
- **فيلم «الصورة تُرسم» / painting film:** DRAW-53 + DRAW-48 + DRAW-49 + DRAW-51 + BRAND — شعار المستخدم يُستورد ويُرسم بترتيب رسام وينتهي مطابقًا للأصل بكسلًا بكسلًا.
- **دعاء أو مناسبة / dua or occasion:** DRAW-11 + DRAW-13 + GLOW + ARAB-66 — محراب بقلم ذهبي، أيقونة المعنى ترسم فوق السطر وتتنفس مع الصوت.
- **ريل تعليق على لقطة شاشة / annotated screen reel:** DRAW-20 + DRAW-19 + DRAW-21 + UI + CAM — سهم ثم ملاحظة، دائرة حول الخطأ، شطب وإعادة كتابة، والكاميرا تقترب لكل علامة.
- **حكاية دودل / doodle tale:** DRAW-36 + DRAW-26 + DRAW-28 + CHAR + EASE-77 — عالم حبر متصل، شخصية تمشي، خطوط تغلي على اثنين.
- **رحلة على خريطة مرسومة / sketched map journey:** DRAW-42 + DRAW-32 + DRAW-08 + MAP — ساحل بثلاث تموجات، مسار يرسم نفسه، محطات مرقمة.
- **شعار تقني / tech logo sting:** DRAW-47 + DRAW-07 + 3D + GLOW — حواف سلكية ترسم، شريط مسح، ثم المجسم يكتمل.

## أخطاء ممنوعة / never do

1. **لا تولد حروفًا عربية من ضربات منفصلة ولا ترسم العربية حرفًا حرفًا** — تتفكك الحروف؛ اكشف خطًا عربيًا حقيقيًا بقناع من اليمين (DRAW-15، ARAB-01).
2. **لا تقس المسار قبل ضبط d وتحميل الخطوط** — طول خاطئ وفجوة في النهاية؛ قِس داخل بوابة الجاهزية (DRAW-09).
3. **لا ترسم كل المسارات معًا** — يفقد الرسم معناه؛ ابدأ كل مقطع عند 70–80% من سابقه (DRAW-01).
4. **لا غليان غير مقصود** — بذرة عشوائية متغيرة لكل إطار تجعل الرسم يرتجف؛ ثبّت البذرة لكل خط، والغليان فقط بـ floor(t·12) (DRAW-25/26).
5. **لا تترك اليد أو الماركر على الشاشة أثناء الثبات** — يحجب الرسم ويشتت؛ ارفعه بين الضربات وأزله عند الثبات (DRAW-06).
6. **لا تغطِّ الشيء الذي تشرحه بالعلامة** — الدائرة حوله والسهم إليه، لا فوقه (DRAW-20).
7. **لا تعتمد على ctx.filter blur تحت 0.8 بكسل في Chromium** — يُتجاهل بصمت؛ اكتب الضبابية بـ JS (DRAW-30).
8. **لا تنسخ أو تشحن رسومًا متتبعة من فيديو طرف ثالث** — التتبع للدراسة فقط وتُحفظ الإحصاءات لا الرسوم (DRAW-57).
9. **لا تترك مكتبة رسم تعمل بمؤقتاتها الخاصة** — vivus وrough-notation يجب أن تُقاد بـ seek(t) وإلا يختلف الرندر (DRAW-60).
10. **لا تَعِد بأداة «hand-drawn» في fastify-motion-bro كأنها جاهزة** — لا يوجد محرك خطوط هناك بعد؛ ابنِ المشهد بأدوات هذا الفصل.
11. **لا تبدأ مسح قلم التحديد من اليسار على جملة عربية** — يعاكس اتجاه القراءة؛ ابدأ من اليمين (DRAW-18).

## أقوى 5 حركات توقيع / 5 signature moves

1. **DRAW-01 — رسم المسار بـ pathLength=1:** أبسط وأضمن رسم حي، مُثبت في فيلم الخاتم الذهبي.
2. **DRAW-06 — رأس يتبع الخط:** يد أو ماركر أو طباشيرة على طرف الخط تحوّل أي مسار إلى «شخص يرسم».
3. **DRAW-19 — الدائرة اليدوية المرتعشة:** 300–700 ملّي ثانية حول الكلمة أو الرقم المهم — أقوى تأكيد في الشرح.
4. **DRAW-48 + DRAW-49 — فيلم الرسام:** أي صورة أو شعار يُرسم بترتيب رسام إلى MP4، مختبر هنا.
5. **DRAW-33 — السبورة المتزامنة مع الصوت:** كل جملة ترسم عنصرها، ثبات، ثم انتقال — قالب الشرح الأول.

## إضافات من Cinematic Director PRO v5

_مستخلصة من حزمة المالك KOSIF Claude Cinematic Director PRO v5 (انظر [cinematic-director-pro.md](../cinematic-director-pro.md)). مسارات الدليل `owner-upload:` تشير إلى ملفات داخل أرشيف المالك، لا إلى هذا المستودع._

#### DRAW-P01 · قصة الخط الواحد المستمر حتى الشعار · Continuous-line logo story (one stroke → three beats → wordmark loop) · ✅ مُثبت هنا / proven here
- **ماذا / what:** خط واحد لا ينقطع يمر بثلاث محطات مرقّمة ثم يلتف حول الشعار، مع صوت مولّد بالكود. / One unbroken line travels through three numbered beats and closes into a loop around the wordmark, with code-synthesised sound.
- **كيف / how:** 13 waypoints interpolated 18 steps each; drawn length = smoothstep(t/4.1); beat dots grow with smoothstep((t−(0.9+0.85k))/0.55) and their labels (01 CAPTURE, 02 CONNECT, 03 RESURFACE) appear at the same instants; from 4.25 s an ellipse (rx 100, ry 42) draws over 1.1 s around the wordmark. Editorial palette: paper (246,241,230), ink (31,36,34), one accent (213,70,48), 6 px stroke, pen-tip dot. Audio generated in NumPy (see BEAT-P01). Re-ran here: 6.000 s, 360×640, 24 fps, H.264 + AAC 96k. **أرقام / params:** 360×640 · 24 fps · 6 s · draw 4.1 s · beats at 0.9/1.75/2.6 s · loop 4.25–5.35 s
- **الرخصة / license:** owner package (own work)
- **الدليل / proof:** `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/tools/render_continuous_line.py` · `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/examples/Continuous_Line_Logo_Story.mp4` · `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/integrations/kosif-see/INTEGRATION_REPORT.json`
