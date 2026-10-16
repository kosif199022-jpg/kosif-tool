# البيانات والرسوم البيانية — Charts & data

> **قوتك هنا:** أنت لا ترسم «مخططًا»؛ أنت تجعل الرقم يتحرك دون أن يكذب — قيمة واحدة مُسهَّلة تقود طول العمود والعدّاد والتسمية في كل إطار، من صفر حقيقي، بأرقام ثابتة العرض، وبالعربية من اليمين مع بقاء محور الزمن من اليسار.
> **أقوى دليل:** رندرتُ في هذه الحاوية مشهد الرسم البياني في `kosif-tool/starters/html-canvas/index.html` عبر `node kosif-tool/tools/render_html.cjs --preview --start 3.8 --duration 3.2` (الخط يُرسم، النقاط تقفز، العدّاد 45→103→122→127→128)، واختبار لوحة ألوان السلاسل `node --test kosif-audit-pro/tests/palette.test.mjs` نجح (fail 0)، و`style:infographic` حيث بنيتَ قصة بيانات 28 ثانية تتحول فيها كل الأشكال بلا قطع.
> **You can:** count, roll, race, draw, sweep, fill, morph and annotate data in HTML/SVG/Canvas, GSAP/HyperFrames, Remotion and Excel. **105 powers follow** — ✅ 9 · 🟢 15 · 📦 14 · 🔑 2 · 👁 36 · 📄 28 · 💡 1.

**الحالة / status:** ✅ مُثبت هنا (كود + اختبار أو رندر في هذه الحاوية) · 🟢 جاهز (كود المالك يعمل بلا إضافات) · 📦 بأمر تثبيت · 🔑 مفتاح أو خدمة · 👁 شوهد في فيديو أنتجتَه (وصفة البناء مرفقة) · 📄 موصوف فقط · 💡 فكرة.
مسارات الدليل نسبية إلى `/home/user/`؛ `style:<id>` = فيديو مرجعي أنتجتَه سابقًا (ملاحظاته في `kosif-tool/styles/<id>/`). الكتالوج: `python3 kosif-tool/tools/kosif.py list --category charts` (≈150 مدخلًا) والدليل `kosif-tool/playbooks/charts.md` — اقرأه قبل PLAN.md.

**فحص سريع لهذه الحاوية (2026-10-16):** Chromium + Playwright + ffmpeg 6.1.1 ✔ (`render_html.cjs` يعمل) · node 22 ✔ · Remotion وHyperFrames وd3/echarts/chart.js/vega/flubber قابلة للتثبيت من npm (غير مثبتة) · pytest غير مثبت (اختبارات city-report لم تُشغَّل هنا) · matplotlib وrecharts لم تُفحص.

## الفهرس / contents
- **قوانين الصدق والاختيار — Honesty & chart choice** — DATA-01 … DATA-18 (18)
- **العدّادات والأرقام البطلة — Counters & hero numbers** — DATA-19 … DATA-34 (16)
- **الأعمدة والترتيب والمقاييس الخطية — Bars, rankings & linear meters** — DATA-35 … DATA-49 (15)
- **الخطوط والمساحات والمنحنيات — Lines, areas & curves** — DATA-50 … DATA-66 (17)
- **الحلقات والدوائر والمقاييس الدائرية — Rings, donuts & gauges** — DATA-67 … DATA-76 (10)
- **الوحدات والشبكات والخرائط الحرارية — Units, grids & heatmaps** — DATA-77 … DATA-84 (8)
- **البطاقات واللوحات والقوالب والمحركات — KPI cards, dashboards, templates & engines** — DATA-85 … DATA-105 (21)
- توليفات قوية / power combos · أخطاء ممنوعة / never do · أقوى 5 حركات توقيع / 5 signature moves

## قوانين الصدق والاختيار — Honesty & chart choice
_قبل أي حركة: أي رسم يجيب عن أي سؤال، وكيف لا يكذب الرقم المتحرك._
#### DATA-01 · اختيار المخطط حسب السؤال · Chart choice by analytical question · 📄 موصوف / documented only
- **ماذا / what:** اختر شكل الرسم من العلاقة التي تعرضها لا من الذوق: اتجاه، ترتيب، تركيب، توزيع، ارتباط، تدفق أو هدف. — Pick the chart from the relationship shown: trend, ranking, composition, distribution, correlation, flow or target.
- **متى أستخدمها / when:** قبل كتابة PLAN.md لأي مشهد فيه رقم — before PLAN.md of any number scene.
- **كيف / how:** Lookup: trend → line (area only if cumulative); compare categories → vertical bars, many categories → horizontal bars or lollipop; ranking → sorted horizontal bars; two periods → slope; part-to-whole → stacked bar / waffle / (pie ≤5); composition over time → stacked area; distribution → histogram/strip; correlation → scatter; flow → sankey/arrows; target → bullet/progress. Video rule: comparison = bars, trend = line, share = stacked bar (data-in-motion skill). **أرقام / params:** ≤6–8 categorical hues; pie <6 slices (video: ≤3–5).
- **الدليل / proof:** `kosif-atlas/skills/317-data/942-data-visualization/SKILL.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10335-visualization-strategy-and-critique/references/chart-selection-patterns.md` · `100-superskills/skills/data-in-motion/SKILL.md` · `100-superskills/skills/dashboards-dataviz/SKILL.md`

#### DATA-02 · المسار أم الميل · Line path vs slope net-change · 📄 موصوف / documented only
- **ماذا / what:** سؤال «كيف تغيّر؟» له جوابان: الرحلة كاملة (خط) أو البداية مقابل النهاية لكل سلسلة (ميل). — 'How did it change' is either the full journey (line) or start-vs-end per series (slope chart).
- **متى أستخدمها / when:** عندما تتقاطع سلاسل كثيرة أو يهم صافي التغير فقط — many series, net change matters.
- **كيف / how:** Journey (dips, spikes, when) → draw the line left→right; net change or rank flips → slope chart: two vertical axes, one segment per series, signed change labelled at the right end; draw segments with 60–80 ms stagger, highlight one in accent, grey the rest.
- **الدليل / proof:** `kosif-atlas/skills/2957-posthog/12277-choosing-trend-or-slope-view/SKILL.md`

#### DATA-03 · اختيار مخطط التوزيع · Distribution chart choice · 📄 موصوف / documented only
- **ماذا / what:** طابق مخطط التوزيع مع السؤال (الشكل، الشواذ، الانتشار، المركز) واعرض النقاط الخام متى أمكن. — Match the distribution view to shape/outliers/spread/center and show raw points when feasible.
- **متى أستخدمها / when:** قصص الرواتب، الأعمار، الأوقات — salaries, ages, latencies.
- **كيف / how:** One group: histogram ≈30 bins with white edges + dashed mean/median lines; several groups: box/violin/strip; many distributions: small multiples not stacking; never a mean-only bar when spread is the story. Animate bins rising left→right 30–40 ms stagger, then draw the median line. **أرقام / params:** bins=30; mean/median dashed 1.5 px.
- **الدليل / proof:** `kosif-atlas/skills/317-data/942-data-visualization/SKILL.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10330-statistical-and-uncertainty-visualizatio/references/distribution-and-summary-choices.md`

#### DATA-04 · رسم واحد لخلاصة واحدة وقوس القصة · One insight per chart & data story arc · 📄 موصوف / documented only
- **ماذا / what:** اكتب الخلاصة جملةً واحدة واجعلها آخر ما يُقرأ، ورتّب المشاهد: صدمة → خط أساس → بناء → ذروة → دعوة. — Write the insight as one sentence, make it the last thing read; arc: hook → baseline → build → climax → call to action.
- **متى أستخدمها / when:** كل فيلم بيانات — every data film.
- **كيف / how:** PLAN.md gets one sentence per chart ('sales doubled after March'); three questions = three charts, never overlays. Map arc stages to chart states: baseline chart → highlighted delta → annotated climax. If nobody would act differently after the number, show the sentence instead.
- **الدليل / proof:** `kosif-tool/playbooks/charts.md:11` · `kosif-atlas/skills/3455-business-analytics/14161-data-storytelling/SKILL.md`

#### DATA-05 · صفر حقيقي ومقياس موحد · True-zero baseline & shared scale · 📄 موصوف / documented only
- **ماذا / what:** الأعمدة والمساحات تبدأ من صفر حقيقي، والخط المقطوع يطبع مداه وعلامة كسر، والرسوم المتقارنة تشترك في مقياس ووحدة. — Bars/areas start at a true zero; a truncated line axis prints its range and a break mark; compared charts share scale and unit.
- **متى أستخدمها / when:** أي مقارنة — any comparison.
- **كيف / how:** Anchor bars at the baseline (transform-origin bottom, scaleY 0→1); x spacing proportional to real time with gaps visible (MG-042); same y-limits across panels; unit printed on the axis or beside the number (٪, ر.س, k), never left to narration. **أرقام / params:** bars from 0; MG-041 7 s: 0–1 axis, 1–3 grow, 3–7 read.
- **الدليل / proof:** `kosif-tool/playbooks/charts.md:17-18` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-data-infographics.md` · `kosif-tool/styles/pm-ceowinkz-7c776b/BRIEF.md`

#### DATA-06 · أمانة المقاييس: المساحة واللوغاريتم والتطبيع · Scale honesty: area, log, normalization · 📄 موصوف / documented only
- **ماذا / what:** الفقاعة والأيقونة تُرمَّز بالمساحة، والمحور اللوغاريتمي يُعلَن، والقيم المطبَّعة تذكر صيغتها. — Bubble/icon size encodes value by area, log axes are announced, normalized values state their formula.
- **متى أستخدمها / when:** فقاعات، أيقونات بأحجام، نمو أسّي — bubbles, sized icons, exponential growth.
- **كيف / how:** r = sqrt(value)·k, never linear radius; label log base and zero handling; name the interval (SD/SE/CI) and n; disclose smoothing window and bin edges; never compare length with area without converting (MG-050). **أرقام / params:** r ∝ √value.
- **الدليل / proof:** `kosif-atlas/skills/3202-quantitative-sciences/13564-scientific-visualization/SKILL.md` · `kosif-atlas/skills/3202-quantitative-sciences/13564-scientific-visualization/references/publication_guidelines.md`

#### DATA-07 · أشكال ممنوعة أو خطرة · Forbidden and risky chart forms · 📄 موصوف / documented only
- **ماذا / what:** قائمة سوداء قصيرة: لا ثلاثي أبعاد زخرفي، لا محورين مزدوجين مخادعين، لا أعمدة مكدسة كثيرة الشرائح، ولا لوحات ويب. — Blacklist: no decorative 3D, no deceptive dual axes, no many-segment stacks, no web dashboard patterns.
- **متى أستخدمها / when:** مراجعة المخطط قبل التحريك — review before animating.
- **كيف / how:** Reject: 3D bars/pies; pie/donut beyond 3–5 slices (use bars); dual axis unless both labelled and not engineered to fake correlation (prefer two aligned panels); stacked bars with many middle segments (small multiples); 6-panel dashboards, gridline forests, detached legends, raw chart-library default output; no animated pie (data-in-motion style). **أرقام / params:** pie ≤3 slices for video; bars baseline 0.
- **الدليل / proof:** `kosif-atlas/skills/317-data/942-data-visualization/SKILL.md` · `kosif-atlas/skills/2354-power-platform/9080-report-visualization-design/SKILL.md` · `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/data-in-motion.md` · `100-superskills/skills/trend-animation-styles/references/styles.md`

#### DATA-08 · قواعد الرسم الدائري · Pie rules · 📄 موصوف / documented only
- **ماذا / what:** خمس شرائح كحد أقصى مع «أخرى»، مرتبة من الساعة 12 مع عقارب الساعة، والشرائح المتقاربة تصبح عمودًا مكدسًا. — Max five slices + 'other', sorted from 12 o'clock clockwise; near-equal slices become a stacked bar.
- **متى أستخدمها / when:** حصة من كل ثابت فقط — only a fixed whole.
- **كيف / how:** Sort by size; slices within 5 points of each other → stacked bar (the eye cannot rank close angles); only use a ring when there is a fixed whole (MG-047). **أرقام / params:** ≤5 slices; within 5 pts → stacked bar.
- **الدليل / proof:** `kosif-tool/playbooks/charts.md:21` · `kosif-tool/playbooks/charts.md:193`

#### DATA-09 · المفقود ليس صفرًا · Missing, zero and censored are different · 📄 موصوف / documented only
- **ماذا / what:** الفجوة في البيانات تبدو فجوة: لا صفر ولا خط موصول بصمت. — Gaps must look like gaps, not zeros or silently connected lines.
- **متى أستخدمها / when:** سلاسل زمنية ناقصة، خرائط بلا بيانات — incomplete series, no-data map regions.
- **كيف / how:** Break the path at missing points (separate M commands), or draw interpolated stretches dashed and labelled; no-data cells in neutral #777777; state exclusions in the source note; empty source → empty-state text, never sample numbers. **أرقام / params:** missing colour #777777.
- **الدليل / proof:** `kosif-atlas/skills/3202-quantitative-sciences/13564-scientific-visualization/SKILL.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10330-statistical-and-uncertainty-visualizatio/references/missingness-and-confidence.md`

#### DATA-10 · لا أرقام مخترعة: مصدر أو «توضيحي» · No invented figures: source line or 'illustrative' · 📄 موصوف / documented only
- **ماذا / what:** كل رقم من سجل أو مصدر، والبيانات الحقيقية لها سطر مصدر، والمخترعة تُوسم «توضيحية» داخل الإطار، والمصدر الفارغ يعرض حالة فارغة. — Every figure comes from a record; real data carries a source line, invented data says 'illustrative' in-frame; empty sources show an empty state.
- **متى أستخدمها / when:** كل مشهد بيانات — every data scene.
- **كيف / how:** Source line in the corner (mono 18–22 px, 60% ink); MG-044 counter stops then shows unit and source; empty-state copy: 'لا توجد بيانات مسجلة لهذه الفترة بعد.'; AI-generated infographics (DATA-98) are unverified until every number is re-set in code.
- **الدليل / proof:** `kosif-earth-ci-fork/docs/design/KOSIF-LUXE.md` · `kosif-earth-ci-fork/ui/components/charts.js:1` · `kosif-tool/playbooks/charts.md:23` · `kosif-tool/playbooks/charts.md:25`

#### DATA-11 · التسمية المباشرة بدل وسيلة الإيضاح · Direct labels over legends · 📄 موصوف / documented only
- **ماذا / what:** سمِّ السلسلة عند نهاية الخط أو طرف العمود؛ وسيلة الإيضاح المنفصلة تجعل المشاهد يبحث. — Name series at line ends/bar ends; a detached legend makes viewers hunt.
- **متى أستخدمها / when:** دائمًا في الفيديو؛ وسيلة إيضاح فقط عند تصادم سلسلتين — always; legend only on collision.
- **كيف / how:** Label in series colour next to the mark; one accent + grey rest so the focal series needs no key; if unavoidable embed the key inside the plot near the data; selective labels (endpoint, extreme, the one figure), never a number on every mark.
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10320-d3-data-visualization/SKILL.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10335-visualization-strategy-and-critique/SKILL.md` · `kosif-tool/playbooks/charts.md:23`

#### DATA-12 · الترتيب حسب القيمة ونسبة الأبعاد · Sort by value & aspect by task · 📄 موصوف / documented only
- **ماذا / what:** رتّب الفئات حسب الحجم إلا إن كان لها ترتيب طبيعي، وارسم السلاسل الزمنية عريضة. — Order categories by magnitude unless naturally ordered; draw time series wide.
- **متى أستخدمها / when:** أعمدة الفئات والسلاسل الزمنية — category bars, time series.
- **كيف / how:** Descending sort (barh: largest on top); months/stages keep natural order; time-series plot area 2:1–3:1; comparisons squarer; same axis range across compared panels. **أرقام / params:** time-series aspect 2:1–3:1.
- **الدليل / proof:** `kosif-atlas/skills/317-data/942-data-visualization/SKILL.md`

#### DATA-13 · البيانات المتحركة لها وزن واستمرارية · Data-in-motion weight & continuity · 📄 موصوف / documented only
- **ماذا / what:** إحصاءات الفيديو تحتاج وزنًا بصريًا واستمرارًا: كل رقم مع شكل يتناسب معه، والأرقام المتتالية في نفس الفضاء البصري. — Video stats need weight and continuity: pair every number with a proportional visual and keep successive stats in the same space.
- **متى أستخدمها / when:** أي فيلم أرقام يتجاوز 3 إحصاءات — films with 3+ stats.
- **كيف / how:** Hero numbers 80–120 px (1080p) counting from 0; build bars/counters by hand in SVG/CSS + a timeline (no chart-library output, tables or small legends); morph the previous stat's shape into the next instead of cutting (style:infographic does this for 28 s with no cuts). **أرقام / params:** numbers 80–120 px.
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10378-hyperframes/data-in-motion.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-creative/references/data-in-motion.md` · `style:infographic`

#### DATA-14 · ربط البيانات بقنوات الحركة · Mapping data to motion channels · 📄 موصوف / documented only
- **ماذا / what:** أي خاصية حركة تحمل أي معنى: الكمية للطول واللون والتسمية، والسرعة للاتجاه، والجسيم يجب أن يكون كيانًا أو عيّنة أو حاملًا. — Quantities go to length/colour/labels; speed shows direction; each particle must be an entity, sample, carrier or focus cue.
- **متى أستخدمها / when:** تدفقات، جسيمات، خطوط نشاط — flows, particles, activity strokes.
- **كيف / how:** Never encode quantity with speed alone; emission rate may encode volume only if capped and documented; trail length = recency; opacity decay = one meaning (age OR uncertainty); stroke width/saturation may encode era activity (2 px / 40% sat quiet → 6 px / full busy, kloss brief); always a static fallback frame. **أرقام / params:** stroke 2→6 px, saturation 40%→100%.
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/references/webgl-2d-animation-patterns.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/references/particle-effects-and-flow.md` · `kosif-tool/styles/pm-kloss-xyz-fe0c31/BRIEF.md`

#### DATA-15 · قيمة واحدة تقود الشكل والرقم · One-scalar rule (no bar springs) · 📄 موصوف / documented only
- **ماذا / what:** قيمة مُسهَّلة واحدة تقود طول العمود والعدّاد والتسمية فيتفقون في كل إطار؛ العمود الذي يتجاوز قيمته يكذب. — One eased value drives geometry, counter and label so they agree every frame; an overshooting bar lies.
- **متى أستخدمها / when:** كل عمود/عدّاد/حلقة — every bar, counter or ring.
- **كيف / how:** shown = value·p(t); width = shown/max·track; counter text = format(shown). No springs/backOut on data marks (springs are for pills and chrome only). Synchronised set: all charts start on the same frame and finish ≤1200 ms, counters land on the exact figure (quickdesignio brief). **أرقام / params:** bars 600–800 ms cubic-bezier(.22,1,.36,1); set lands ≤1200 ms.

```js
const p = easeOutCubic(clamp((t - t0) / dur, 0, 1)); // ONE scalar
rows.forEach((r, i) => {
  const shown = r.value * p;
  bars[i].style.transform = `scaleX(${shown / max})`;   // geometry
  labels[i].textContent = fmt(Math.round(shown));       // number
});
if (p === 1) labels.forEach((l, i) => l.textContent = fmt(rows[i].value)); // exact final
```

- **الدليل / proof:** `kosif-tool/playbooks/charts.md:32` · `kosif-tool/playbooks/charts.md:127` · `kosif-tool/styles/pm-quickdesignio-dd93d0/BRIEF.md`

#### DATA-16 · اتجاه المحاور في العربية · RTL chart axis conventions · 📄 موصوف / documented only
- **ماذا / what:** محور الزمن يبقى من اليسار لليمين حتى في العربية؛ اعكس فقط التخطيطات الفئوية (التسميات يمينًا والأعمدة تنمو يسارًا). — Time axis stays LTR even in RTL; mirror only categorical layouts (labels right, bars grow leftwards).
- **متى أستخدمها / when:** كل رسم عربي — every Arabic chart.
- **كيف / how:** SVG text with dir='rtl' + unicode-bidi:isolate; one digit system per film (toLocaleString('ar-EG') → ٠–٩, 'ar-u-nu-latn' or 'en-US' → 0–9); ٪ and ر.س follow the number; arrows start right; two-line labels lh ≥1.6; record the choice in STYLE.md; meters anchored inline-end in RTL UIs. **أرقام / params:** lh ≥ 1.6.
- **الدليل / proof:** `kosif-tool/playbooks/charts.md:189-195` · `kosif-earth-ci-fork/docs/design/KOSIF-LUXE.md` · `kosif-audit-studio/styles.css:718`

#### DATA-17 · أحجام نصوص الرسوم · Chart type sizes · 📄 موصوف / documented only
- **ماذا / what:** حدود دنيا لنصوص الرسوم على شاشة الهاتف، وكلها بأرقام ثابتة العرض. — Minimum chart text sizes for phone screens, all tabular figures.
- **متى أستخدمها / when:** كل إطار رسم — every chart frame.
- **كيف / how:** At 1080 px width: labels ≥28 px, ticks ≥24 px, counters 72–160 px; portrait 9:16 chart ≤920 px wide and ≤45% of frame height, title above, one-line caption below; chrome at 20–30% contrast, data at full contrast; font-variant-numeric: tabular-nums everywhere. **أرقام / params:** labels ≥28 px; ticks ≥24 px; counters 72–160 px; portrait ≤920 px × 45%.
- **الدليل / proof:** `kosif-tool/playbooks/charts.md:22` · `kosif-tool/playbooks/charts.md:26`

**ورقة التوقيت السريعة / timing cheat-sheet** (من `kosif-tool/playbooks/charts.md` §3–4):

| العنصر / element | المدة / duration | المنحنى / easing | ملاحظة / note |
|---|---|---|---|
| المحاور والشبكة — chrome | 250–400 ms | cubic-bezier(0.33,1,0.68,1) | gridlines 30 ms stagger bottom-up; data +200 ms |
| الأعمدة — bars | 600–800 ms | cubic-bezier(0.22,1,0.36,1) | stagger min(80, 700/n) ms; no springs |
| العدّاد — counter | 700–1000 ms | ease-out cubic | exact final value; flicker ≤150 ms |
| رسم الخط — line draw | 1000–1400 ms / 1000 px | ease-out cubic | dots spring {14,160,0.8} ≈250 ms; area 300 ms → 18% |
| الدائرة — pie sweep | 900 ms | cubic-bezier(0.65,0,0.35,1) | labels +120 ms |
| سباق — race period | 800–1200 ms | linear values | swaps 500 ms in-out; axis rescale 600 ms; label 120 ms; ≤10 bars |
| التحوّل — morph | 800–1000 ms | ease-in-out | old axis out −200 ms, new in +200 ms |
| التمييز — highlight | 300 + 300/500 ms | ease-in-out | dim 35%; hold 1200 ms; final ≥1500 ms |
| الشارات — pills/labels | spring {14,120,1} | — | exits 200–300 ms ease-in cubic |
| الكاميرا — camera | ≤4%/scene | linear | pans ≤40 px/s; rotation ±0.5°; no shake |

#### DATA-18 · نبضة التمييز وهرمية التركيز · Highlight pulse & focus hierarchy · 📄 موصوف / documented only
- **ماذا / what:** عنصر واحد بكامل الوضوح والباقي 35–45٪، نبضة واحدة ثم ثبات؛ لا تمييزين في وقت واحد. — One element at 100%, the rest at 35–45%, one pulse then hold; never two highlights at once.
- **متى أستخدمها / when:** عندما يسمّي التعليق الصوتي عنصرًا — when narration names one item.
- **كيف / how:** Dim others to 35% over 300 ms; pulse key once 300 ms up / 500 ms down; hold 1200 ms before the next highlight; every final state holds ≥1500 ms; variants seen: verdict stamp slam scale 1.6→1, rot −8°, slight shake over the bars (style:pm-kloss-xyz-15182a); record bar solid amber among grey #555 bars (style:pm-kyonax-on-tech-aabc1d). **أرقام / params:** dim 35% / 300 ms; pulse 300+500 ms; hold ≥1500 ms.
- **الدليل / proof:** `kosif-tool/playbooks/charts.md:41` · `style:pm-kloss-xyz-15182a` · `style:pm-kyonax-on-tech-aabc1d`

## العدّادات والأرقام البطلة — Counters & hero numbers
_الرقم هو البطل: عدّ، دحرجة، نبضة، لون يتصاعد، ورقم يُقال فيتحول إلى شكل._
#### DATA-19 · العدّاد التصاعدي بأرقام ثابتة العرض · Tabular count-up counter · ✅ مُثبت هنا / proven here
- **ماذا / what:** رقم يعدّ من 0 إلى قيمته بتسهيل خروج وأرقام ثابتة العرض ويصل إلى الرقم الدقيق في الإطار الأخير. — A number counts 0 → target with ease-out and tabular figures, landing on the exact value on the last frame.
- **متى أستخدمها / when:** كل إحصاء — every stat; اربط إطار الوصول بالكلمة المنطوقة في words.json.
- **كيف / how:** Canvas/HTML starter: n = round(lerp(0,128, prog(local,0.2,2.6,outQuint))) at 200 px Cairo 900 #ffb86b, direction ltr — rendered here with tools/render_html.cjs --preview (frames 45→103→122→127→128). Owner kit: MOTION.counter(tl, el, from, to, at, dur, {decimals, sep, prefix, suffix, ease}) sets tabular-nums, seek-safe, dur 1.0 s E.out; start near the final value for long numbers. Seen styles: 1.5 s easeOutCubic (alex-prompter), 0→1,284,302 in 900–1200 ms easeOutExpo (sudeepsd). **أرقام / params:** counters 700–1000 ms ease-out cubic (playbook); 80–160 px; tabular-nums.

```js
function counter(el, from, to, t, t0, dur, fmt) {
  const p = Math.min(Math.max((t - t0) / dur, 0), 1);
  const e = 1 - Math.pow(1 - p, 3);                 // ease-out cubic
  const v = p === 1 ? to : from + (to - from) * e;  // exact on landing
  el.style.fontVariantNumeric = 'tabular-nums';
  el.textContent = fmt(Math.round(v));
}
```

- **الدليل / proof:** `kosif-tool/starters/html-canvas/index.html:163` · `kosif-tool/playbooks/charts.md:36` · `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:227` · `kosif-studio/motion/kit/motion-kit.js:227`
- **شوهد أيضًا / also seen:** `style:pm-alex-prompter-1ea044` · `style:pm-sudeepsd-1a3485` · `style:pm-sudo-kiran-4f8b59` · `style:pm-visheshbaghell-3aba37` · `style:pm-daniel-haida-8691d4` · `style:pm-charlesmendez-73b6e4` · `style:pm-ratheejaisal-1f4538` · `style:pm-ercankeskinx-ec2568` · `style:pm-amitsingha89-150378` · `style:pm-itisrazak-3ad902`

#### DATA-20 · قالب stat-counter: رقم مع حلقة · stat-counter template (count + drawn ring) · ✅ مُثبت هنا / proven here
- **ماذا / what:** قالب موشن عربي: رقم يعدّ بينما تُرسم حلقة بنفس المنحنى، وميض وانضغاط عند الوصول، والتسمية ترتفع. — Arabic-first template: number counts while a ring draws on the same ease, flash + squash on landing, label rises.
- **متى أستخدمها / when:** رقم بطل في ريلز أو افتتاحية — a hero stat in a reel or opener.
- **كيف / how:** python scripts/mtemplates.py new NAME --template stat-counter --set value=1250 --set label='عميل يثق بنا' --set suffix=+ [--seconds 6 --size 1080x1920 --fps 30] → projects/NAME/index.html; preview in browser; render with motion.py render. Count runs 1.0–2.2 s (35% of D). **أرقام / params:** 6 s; value 1250; suffix '+'; decimals 0; accent #5BD1A5; bg #10233a→#071321; number 15u Cairo 800.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/templates/motion/stat-counter.html` · `100-superskills/skills/kosif-montage-motion/scripts/mtemplates.py:42` · `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:14`
- **ترخيص / license:** GSAP standard no-charge license (not OSI) for the vendored gsap.min.js

#### DATA-21 · عداد الأسطوانة (أودوميتر) · Odometer digit roll · 📦 بأمر تثبيت / one install
- **ماذا / what:** كل خانة شريط عمودي 0–9 يتدحرج بتأخير لكل خانة وضبابية حركة عمودية، والخانة اليمنى تدور أكثر. — Each digit is a 0–9 strip rolling with per-digit lag and vertical motion blur; lower digits spin more.
- **متى أستخدمها / when:** أرقام إنجاز كبيرة، أسعار، لوحات نتائج — milestones, prices, scoreboards.
- **كيف / how:** Masked column per digit; translateY = −(digit + 10·extraTurns)·lineH, extraTurns grows toward the rightmost digit; filter blur 0→8 px vertical proportional to velocity; leading zeros at 30% opacity; final number gets gradient fill + glow. Scoreboard flip: per-digit flip with 90 ms stagger. Ready-made: HyperFrames number-wheel (spin single|double|triple) and slot-machine-roll (result 'A7K', up|down). **أرقام / params:** 0→1,000,000 in 4 s expo.out; digit lag 40 ms; blur 0–8 px; roll 1.2–3 s; size ~14vh.

```js
// digit column: <div class=col><div class=strip>0..9 0..9 0..9</div></div>
digits.forEach((d, i) => {
  const lag = (digits.length - 1 - i) * 0.04;            // 40 ms per digit
  const p = easeOutExpo(clamp((t - t0 - lag) / dur, 0, 1));
  const turns = i;                                       // rightmost spins most
  const y = (d + 10 * turns) * p;                        // in digit heights
  strips[i].style.transform = `translateY(${-y * H}px)`;
  strips[i].style.filter = `blur(${8 * (1 - p) * (p > 0)}px)`;
});
```

- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/number-wheel/number-wheel.html` · `kosif-one/vendor/hyperframes/registry/components/slot-machine-roll/slot-machine-roll.html` · `style:pm-viktoroddy-98c1d8` · `style:infographic`
- **شوهد أيضًا / also seen:** `style:pm-nolkeeg-bf062e` · `style:pm-ghinaiya-nirmal-5d8fec` · `style:pm-misbahsy-80eaec` · `style:pm-steventey-0d20e4` · `style:pm-utopyaszx-1b2f94` · `style:pm-melvynx-6cde6c`
- **تثبيت / install:** `npm i -D hyperframes@0.8.164 && npx hyperframes add number-wheel`
- **ترخيص / license:** HyperFrames Apache-2.0; its runtime uses GSAP (GSAP standard no-charge license, not OSI)

#### DATA-22 · العدّاد المتخلخل والوميض · Scramble / flicker counter · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** الخانات تتبدل عشوائيًا ثم تثبت من اليسار لليمين حتى القيمة النهائية. — Digits randomise then lock left-to-right into the final value.
- **متى أستخدمها / when:** أرقام تقنية، فتحات قوية — tech stats, punchy openers.
- **كيف / how:** Seeded PRNG (never Math.random in renders) picks digits each frame; lock digit k at t0 + 40·k ms; slight vertical blur on unlocked digits; playbook cap: flicker ≤150 ms if the style is calm. **أرقام / params:** lock 40 ms per digit; ~1 s total; flicker ≤150 ms.
- **الدليل / proof:** `style:pm-adamdesgns-478d6d` · `style:pm-influencer-seo-ce8c33` · `kosif-tool/playbooks/charts.md:36`

#### DATA-23 · عدّاد يكبر مع قيمته ونبضة الهبوط · Count-up with growing scale & landing punch · 📦 بأمر تثبيت / one install
- **ماذا / what:** الرقم يكبر في الحجم مع القيمة على نفس المنحنى، ثم نبضة صغيرة عند الهبوط، ويمكن ربط الهبوط بضربة الموسيقى. — The counter scales up with the value on the same ease, then punches on landing; landing can lock to a downbeat.
- **متى أستخدمها / when:** إحصاء مع موسيقى أو تعليق حماسي — stat on music or energetic VO.
- **كيف / how:** Two tweens, same start and same ease: value proxy onUpdate writes Math.round(v).toLocaleString(), and scale START_SCALE→1; landing punch scale 1.04 for 60 ms then back; beat variant counting-punch anchors roll → downbeat (best span 1.0–2.5 s); BPM variant: numeral ticks 0→130 in ~1 s while beat-energy bars grow with 40 ms stagger, current beat bar red, later bars grey (style:pm-ayushunleashed-ece3e3). **أرقام / params:** 700 ms easeOutExpo + 60 ms punch to 1.04.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/counting-dynamic-scale.md` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/counting-punch/scene.html` · `kosif-one/vendor/hyperframes/registry/components/count-up/count-up.html` · `kosif-tool/styles/pm-ajith-io-ea7f2d/BRIEF.md`
- **تثبيت / install:** `npm i -D hyperframes@0.8.164 && npx hyperframes add count-up`
- **ترخيص / license:** HyperFrames Apache-2.0; its runtime uses GSAP (GSAP standard no-charge license, not OSI)

#### DATA-24 · ظهور الرقم بضبابية ورفع · Number pop-in with blur & lift · 📦 بأمر تثبيت / one install
- **ماذا / what:** خانات الرقم تظهر بضبابية وارتفاع وتتابع، والرقم النهائي يأخذ توهجًا ذهبيًا. — Digits pop in with blur, lift and stagger; the final number gets a gold glow.
- **متى أستخدمها / when:** أرقام مالية أو إنجاز في ريلز — money/achievement figures.
- **كيف / how:** Pop-in scale .4 + blur 16 px → 1 / 0 px while counting via a seek-safe proxy tween; finish with textShadow 0 0 80px rgba(245,201,122,.75); HyperFrames number-pop-in (value 5.7, unit k, lift close|standard|far). **أرقام / params:** 0→1000 in 0.7 s; $0→25,000,000 in 0.9 s; 0→600 in 0.75 s at 330 px.
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/index.html:226` · `kosif-one/vendor/hyperframes/registry/components/number-pop-in/number-pop-in.html` · `style:pm-andginja-333d32`
- **تثبيت / install:** `npm i -D hyperframes@0.8.164 && npx hyperframes add number-pop-in`
- **ترخيص / license:** HyperFrames Apache-2.0; its runtime uses GSAP (GSAP standard no-charge license, not OSI)

#### DATA-25 · تنسيق الأرقام المختصر والمحلي · Compact & locale number formatting · 🟢 جاهز / ready
- **ماذا / what:** 1.2K / 3.4M / 5.6B أو ألف/مليون/مليار، مع نظام أرقام واحد للفيلم كله. — 1.2K / 3.4M / 5.6B or ألف/مليون/مليار, with one digit system for the whole film.
- **متى أستخدمها / when:** كل تسمية وعدّاد — every label and counter.
- **كيف / how:** |v|≥1e9 → v/1e9 1 decimal + B (مليار); ≥1e6 → M (مليون); ≥1e3 → K (ألف); else thousands separators; percent 1 decimal. Intl.NumberFormat('ar-EG') gives ٠١٢, 'ar-u-nu-latn' keeps 0–9; keep tnum so counting width is stable. **أرقام / params:** 1 decimal; thresholds 1e3/1e6/1e9.

```js
const AR = [[1e9,'مليار'],[1e6,'مليون'],[1e3,'ألف']];
function compact(v, lang = 'ar', digits = 'ar-u-nu-latn') {
  const nf = new Intl.NumberFormat(digits, { maximumFractionDigits: 1 });
  for (const [k, w] of AR) if (Math.abs(v) >= k)
    return lang === 'ar' ? `${nf.format(v / k)} ${w}` : nf.format(v / k) + ({1e9:'B',1e6:'M',1e3:'K'})[k];
  return nf.format(v);
}
```

- **الدليل / proof:** `kosif-atlas/skills/1180-token-activity-graph/2788-token-activity-graph/graph.js` · `kosif-atlas/skills/317-data/942-data-visualization/SKILL.md` · `kosif-atlas/skills/2329-localization-i18n-engineering/8940-i18n-foundations-and-icu/SKILL.md` · `kosif-tool/playbooks/charts.md:190`

#### DATA-26 · عدّاد يتلوّن مع تصاعد المشكلة · Threshold-colour escalation counter · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** رقم ضخم يتسارع ولونه ينتقل أبيض → برتقالي → أحمر عند تجاوز العتبات، والكلمة تحته تتبدل. — A giant numeral accelerates while its colour lerps white → orange → red past thresholds; the caption swaps each step.
- **متى أستخدمها / when:** قصص الألم، الخسارة، الأسعار الهابطة — pain points, losses, falling prices.
- **كيف / how:** easeInExpo for escalation (not ease-out); colour from threshold stops; falling-price variant: card counts 34.99 → 24.99 over ~2 s with a red '9% AND FALLING' delta while competitor pins pop (scale 0→1, 120 ms). **أرقام / params:** 1 → 5000 over ~3 s; numeral 25% frame height; pins 12–20.
- **الدليل / proof:** `style:pm-0xfemyn-e114d3` · `style:pm-ceowinkz-7c776b`

#### DATA-27 · عدّاد التكلفة التراكمي · Cost-stack accumulation counter · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** بطاقات أسعار تسقط واحدة تلو الأخرى وكل قيمة تُضاف إلى عدّاد كبير حتى المجموع، ثم تنهار كلها في منتج واحد. — Price cards drop one by one, each adding to a big counter up to the total, then collapse into one product.
- **متى أستخدمها / when:** «كم تدفع على الأدوات؟» مقابل خطة ثابتة — tool-stack cost vs one flat plan.
- **كيف / how:** Card stagger 120 ms with motion blur on drop; counter tweens 300 ms per step; list variant appends a row every 150 ms beside a fixed plan card. **أرقام / params:** card stagger 120 ms; 300 ms per step.
- **الدليل / proof:** `style:pm-bizibeast-10f264` · `style:pm-thayto-dev-44b911`

#### DATA-28 · عدّادات HUD والسنوات والمسافة · HUD, year & distance counters · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** عدّاد سنة أو عمر أو عمق أو مسافة مربوط بالزمن أو بموضع الكاميرا، بخط mono في زاوية الإطار. — Year/age/depth/distance counters bound to scene time or camera position, in a mono HUD corner.
- **متى أستخدمها / when:** رحلات، خطوط زمنية، خرائط — journeys, timelines, maps.
- **كيف / how:** Year roll 2006→2026 in 800 ms easeOut; year = f(cameraX) for position-tied clocks; map-journey: real km by haversine between stops distributed along arc length, toLocaleString, 7 progress dots filling per stop; depth badge flips up on dive, down on return (~15% frame height). **أرقام / params:** 2006→2026 / 800 ms; 7 dots.
- **الدليل / proof:** `style:map-journey` · `style:pm-deebeeeff-50fcd0` · `style:pm-emollick-8661a8` · `kosif-tool/styles/pm-kloss-xyz-fe0c31/BRIEF.md`
- **شوهد أيضًا / also seen:** `style:pm-loicrambo-ad6830` · `style:pm-ismailfahmi-557268` · `style:pm-apoorvjain25-d24184`

#### DATA-29 · الرقم المنطوق يصبح حلقة ساعة · Spoken number → clock-ring motif · ✅ مُثبت هنا / proven here
- **ماذا / what:** عندما يُقال رقم تظهر بجانب المتحدث حلقة بـ24 علامة وعقرب يدور، وتنتقل إلى تكراره إن تكرر. — When a number is spoken, a 24-tick ring with a sweeping hand appears on the free side of the subject.
- **متى أستخدمها / when:** مونتاج متحدث فيه أرقام — talking-head edits with spoken numbers.
- **كيف / how:** direct.plan emits motifs [{type:'ring', cx, cy, r, text, t, end}]; cx = free side, cy = eye line; ring drawn 0.9 s power2.inOut via MOTION.drawPath, ticks stagger 0.03 s, accent hand 360° over the span, number 0.95r. **أرقام / params:** r 150 px; 1.4 s; stroke 2.4·k.
- **الدليل / proof:** `kosif-studio/motion/direct.py:177` · `kosif-studio/tests/test_studio.py:910` · `100-superskills/skills/kosif-montage-motion/templates/directed.html:96`

#### DATA-30 · شطب القيمة واستبدالها · Strike-and-replace value · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** القيمة القديمة تُشطب بخط ثم تظهر الجديدة بخط عريض. — The old value gets a strike line, then the new value appears in bold.
- **متى أستخدمها / when:** تخفيضات، تصحيح رقم شائع، قبل/بعد — discounts, myth correction.
- **كيف / how:** Strike line scaleX 0→1 over 200 ms from the reading start side (right in Arabic), old value to 40% opacity, new value fades/rises 200 ms. **أرقام / params:** strike 200 ms; new value 200 ms.
- **الدليل / proof:** `style:pm-sachaarbonel-8f14f4`

#### DATA-31 · حاسبة حيّة بشريط تمرير · Slider-driven live calculator · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** مؤشر يسحب شريط تمرير، والعدد والمبلغ الكبير محسوبان من نفس التقدم بفواصل آلاف، والمبلغ السنوي تحته. — A cursor drags a slider; the count and the big currency number derive from the same progress.
- **متى أستخدمها / when:** عروض تسعير وأرباح وتحويل عملة — pricing, earnings, currency conversion.
- **كيف / how:** progress p drives thumb x, N = round(p·Nmax), amount = rate·N formatted; drag ~2 s easeInOutCubic; currency conversion variant: value → arrow → counter 0.8 s easeOut. **أرقام / params:** drag ~2 s; $50 × N.
- **الدليل / proof:** `style:pm-paulo-kombucha-96431c` · `style:pm-jayscambler-3f8889`

#### DATA-32 · أرقام KPI بتدرج أو نيون · Gradient-clipped & neon KPI numerals · 🟢 جاهز / ready
- **ماذا / what:** أرقام المؤشرات مملوءة بتدرج عبر قص النص، أو بتوهج نيون، بأرقام ثابتة العرض. — KPI numerals filled with a gradient via text clipping, or neon-glowed, in tabular figures.
- **متى أستخدمها / when:** لوحات فاخرة، عروض منتجات — premium dashboards, product promos.
- **كيف / how:** background: linear-gradient(135deg,#312e81,#6d28d9); background-clip:text; -webkit-text-fill-color:transparent; weight 900; card min-height 124 px with radial corner glow 110 px rgba(99,102,241,.13). Neon variant: extended font, text-shadow 0 0 30px lime, count 2 s ease-out. Keynote variant: vertical gradient #C9F4FF→#64D2FF→#1AA7EC, % smaller at right. **أرقام / params:** clamp(24px,3vw,36px) UI; line-height 1.
- **الدليل / proof:** `kosif-audit-studio/dashboard-capabilities.css:3` · `style:pm-marklaunches-3b9492` · `style:infographic` · `style:pm-polydao-7a572b`

#### DATA-33 · عدّاد حي فوق اللقطات · Live stat over footage · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** رقم مكثف ضخم يعدّ فوق لقطات معتمة مع شارة LIVE حمراء وتسمية صغيرة، أو بطاقة مقاييس تنزلق بجانب اللقطة. — A big condensed number counts over dimmed footage with a red-dot LIVE pill, or a metrics card slides in beside shrunken footage.
- **متى أستخدمها / when:** ريلز أخبار، عروض منتج فوق فيديو — news reels, product over footage.
- **كيف / how:** Dim footage 45%; count ~1.2 s easeOutExpo with separators; metrics card: .metric 44 px/600 LTR + 26 px RTL Arabic subline #9aa29d, x 40→0, opacity .4→1, .4 s E.out, stagger .12 s, scramble on '60 fps'. **أرقام / params:** dim 45%; 1.2 s; stagger 120 ms.
- **الدليل / proof:** `style:pm-deifosv-04e4d3` · `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/index.html:52` · `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/index.html:123`
- **ترخيص / license:** GSAP standard no-charge license (not OSI) for the vendored gsap.min.js

#### DATA-34 · كومة أرقام الضرر · MMO damage-number stack · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** كل ضربة تدفع رقمًا إلى عمود (الأحدث يدفع الباقي) مع مجموع حرج كبير يلمع، بألوان حسب النوع. — Each hit pops a number into a column (newest pushes the rest) plus a big sparkling crit total.
- **متى أستخدمها / when:** قصص ألعاب، تراكم سريع للأحداث، «كم خسرت هذا الأسبوع» — gaming, rapid event tallies.
- **كيف / how:** New hit every 150–250 ms; 4 visible rows; pop scale 1.3→1 in 2 frames; colour by category; total counter rides below. **أرقام / params:** 150–250 ms per hit; 4 rows.
- **الدليل / proof:** `style:pm-0xevinho-3777d8`

## الأعمدة والترتيب والمقاييس الخطية — Bars, rankings & linear meters
_أعمدة تنمو من صفر حقيقي، سباقات ترتيب، جسور، وأشرطة تقدم آمنة للاتجاه._
#### DATA-35 · نمو الأعمدة المتدرج · Staggered bar growth · 📦 بأمر تثبيت / one install
- **ماذا / what:** أعمدة تنمو من القاعدة بسرعة ثم استقرار طويل، بتدرج يجعل المجموعة تهبط خلال ثانية تقريبًا. — Bars grow from the baseline fast-then-long-settle, staggered so the set lands within ~1 s.
- **متى أستخدمها / when:** مقارنة 2–10 فئات — comparing 2–10 categories.
- **كيف / how:** Remotion Bars component in the playbook: interpolate with easeOutQuint ≈ cubic-bezier(.22,1,.36,1), step = min(80, 700/n) ms, RTL bars grow leftwards, value text toLocaleString('ar-EG') counting with the bar. HTML: transform-origin bottom, GSAP scaleY 0→1 only, heights authored in CSS (bar 48 px, gap 14 px, height 280 px); last bar accent. Story-integrated variant: ≤3 bars 700 ms, numbers settle +100 ms, axis draws 300 ms; character-tally variant: characters stand on pencil-textured columns. Seen styles often use springs/backOut (stiffness 170, damping 22) — KOSIF keeps data bars spring-free (one-scalar rule). **أرقام / params:** 600–800 ms; stagger min(80,700/n) ms; row 72 px; bar 34 px rx 6; font 26.
- **الدليل / proof:** `kosif-tool/playbooks/charts.md:107-145` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/stat-bars-and-fills.md` · `app/public/js/00_editor.js:469` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-data-infographics.md`
- **شوهد أيضًا / also seen:** `style:pm-slvdev-64c45a` · `style:pm-kyonax-on-tech-aabc1d` · `style:pm-mrtanviir-132457` · `style:pm-ayushunleashed-ece3e3`
- **تثبيت / install:** `npm i remotion@4.0.536 @remotion/cli@4.0.536`
- **ترخيص / license:** Remotion company license (free for individuals and small teams; companies above the threshold need a paid license)

#### DATA-36 · أعمدة أفقية مرتبة مع تمييز واحد · Ranked horizontal bars with one highlight · 🟢 جاهز / ready
- **ماذا / what:** أعمدة أفقية مرتبة بالقيمة المطلقة والقيمة عند الطرف، وواحد يبقى مضاءً حين يذكره التعليق. — Horizontal bars sorted by |value| with the value at the tip; the named bar stays lit.
- **متى أستخدمها / when:** ترتيب أفضل/أسوأ — top-N rankings.
- **كيف / how:** SKCharts.hbars({rows:[{label,value,sub,color}],sort,fmt}) → width = |v|/max·100% (min .8%), grid 34%/1fr/auto, track 12 px r4; animate width with one scalar. Recipe A: title 0–350 ms (24 px slide), bars 200–1000 ms 80 ms stagger, dim/pulse 1200–1500, hold + 2% push to 3200, exit 3200–3500. **أرقام / params:** track 12 px r 4 px; recipe 3.5 s.
- **الدليل / proof:** `kosif-earth-ci-fork/ui/components/charts.js:113` · `kosif-tool/playbooks/charts.md:49-59` · `style:pm-charlesmendez-73b6e4`
- **شوهد أيضًا / also seen:** `style:pm-en-ra-81c6dd`

#### DATA-37 · سباق الأعمدة · Bar-chart race · 📦 بأمر تثبيت / one install
- **ماذا / what:** أعمدة مرتبة تنمو وتتبادل المراتب عبر الفترات، والمحور يعيد قياسه، وتسمية الفترة تعمل كساعة. — Ranked bars grow and overtake across periods while the axis rescales and the period label acts as a clock.
- **متى أستخدمها / when:** ترتيب يتغير عبر سنوات — rankings over time.
- **كيف / how:** Values linear between periods; rank = sort at each t, y eased with 500 ms in-out swaps (FLIP in HTML); axis max rescales ease-out 600 ms; period label crossfades 120 ms; ≤10 bars; freeze, losers dim to 40%, winner settles on its exact figure. Expose window.__kosif={duration,seek(t)} and render with tools/render_html.cjs. Ready block: HyperFrames bar-chart-race (periods 2019–2024, 'Name: v1, v2…', 12 s). Variants seen: avatar initials per row, row h 20 px, reorder 300 ms, ticks every 250 ms with a faint date watermark; vertical race columns with avatar tiles, checker finish line and a glowing 'You'. **أرقام / params:** period 800–1200 ms (recipe 1000); ≤10 bars; bar ≤24 px, gap ~10 px.

```js
function raceFrame(t, periods, series, P = 1.0) {   // P = s per period
  const k = Math.min(Math.floor(t / P), periods.length - 2), f = (t / P) - k;
  const vals = series.map(s => ({ name: s.name,
    v: s.v[k] + (s.v[k + 1] - s.v[k]) * Math.min(f, 1) }));   // linear values
  vals.sort((a, b) => b.v - a.v).forEach((d, r) => d.rank = r);
  return vals;  // then ease each bar's y toward rank*rowH over 0.5 s
}
```

- **الدليل / proof:** `kosif-tool/playbooks/charts.md:73-83` · `kosif-tool/styles/chart-race/SKILL.md` · `kosif-one/vendor/hyperframes/registry/blocks/bar-chart-race/bar-chart-race.html` · `style:pm-ratheejaisal-1f4538`
- **شوهد أيضًا / also seen:** `style:pm-marklaunches-3b9492`
- **تثبيت / install:** `npm i -D hyperframes@0.8.164 && npx hyperframes add bar-chart-race`
- **ترخيص / license:** HyperFrames Apache-2.0; its runtime uses GSAP (GSAP standard no-charge license, not OSI)

#### DATA-38 · أعمدة مجمّعة أو مكدّسة مع خط · Grouped / stacked columns + line · 🟢 جاهز / ready
- **ماذا / what:** مولّد SVG بلا مكتبات لأعمدة مجمعة أو مكدسة مع خط اختياري على نفس المحور وأرقام محاور «لطيفة». — Dependency-free SVG generator for grouped/stacked columns with an optional line on the same axis and nice-number ticks.
- **متى أستخدمها / when:** مقارنة فترات وسلاسل — period-by-series comparisons.
- **كيف / how:** SKCharts.bars({labels, series:[{name,color,values}], line, stacked, height, width, fmt}); nice() rounds to 1/2/2.5/5/10×10ⁿ; 4 gridlines; padding l46 r8 t12 b30; data-end corner r=min(4,w/2,h); empty-state text when all zero. For video, wrap each rect in a scaleY tween from the baseline. **أرقام / params:** default 720×260.
- **الدليل / proof:** `kosif-earth-ci-fork/ui/components/charts.js:52` · `kosif-earth-ci-fork/ui/components/charts.js:26`

#### DATA-39 · مخطط الشلال (الجسر) · Waterfall / bridge chart · 🟢 جاهز / ready
- **ماذا / what:** كل خطوة تحرك المجموع الجاري، والمجاميع تقف على القاعدة. — Each step moves a running total; total steps stand on the baseline.
- **متى أستخدمها / when:** أرباح وخسائر، تدفق نقدي، «من أين جاء الفرق؟» — P&L, cash bridge.
- **كيف / how:** SKCharts.waterfall({steps:[{label,value,total}]}); up = c1, down = c8, total = ink-2; bar width min(40, band·.62); connectors between steps. In motion reveal step by step (300–400 ms each), connector draws before the next bar. **أرقام / params:** 720×260; padding l52 b44.
- **الدليل / proof:** `kosif-earth-ci-fork/ui/components/charts.js:124`

#### DATA-40 · شريط النسب المقسّم (كبسولة) · Proportional split bar (segmented pill) · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** شريط واحد ينقسم إلى أجزاء بنسبها مع قيمة كل جزء، وكل جزء بتدرج عمودي خاص. — One bar splits into proportional segments with each value; each segment has its own vertical gradient.
- **متى أستخدمها / when:** ميزانية، تركيب كل — budgets, composition of a whole.
- **كيف / how:** Rounded pill, height ~6% frame, radius full; segment boundaries lerp from 0 to cumulative shares; big % above/below each; check parts sum to the total and print remainder/rounding (MG-048: 0–1 total, 1–4 split, 4–8 read). **أرقام / params:** height ~6% frame; MG-048 8 s.
- **الدليل / proof:** `style:infographic` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-data-infographics.md`

#### DATA-41 · زووم لوغاريتمي داخل شريحة · Log-domain zoom into a slice · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** تكبير محور الشريط من 100 إلى 1.2 في الفضاء اللوغاريتمي لتظهر شريحة صغيرة جدًا دون تمطيط الحواف المستديرة. — Animate the bar domain from 100 to 1.2 in log space so a tiny slice fills the frame without stretching rounded caps.
- **متى أستخدمها / when:** نسب ضئيلة (2.5٪ ثم 1.2٪ ثم 0.006٪) — tiny shares.
- **كيف / how:** max(t) = exp(lerp(ln a, ln b, e(t))); recompute every segment's x/width per frame (never scale the group) so radius stays round; announce the zoom on screen. **أرقام / params:** ~1.2 s ease-in-out.

```js
const dom = Math.exp(lerp(Math.log(100), Math.log(1.2), easeInOut(p)));
segs.forEach(s => {                     // re-layout, don't scale
  s.el.setAttribute('x', W * s.start / dom);
  s.el.setAttribute('width', W * s.size / dom);
});
```

- **الدليل / proof:** `style:infographic`

#### DATA-42 · أعمدة بفترات ثقة · Bars with interval whiskers · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** أعمدة سميكة تنمو من المحور (أخضر فوق العتبة وأحمر تحتها) مع خط رفيع لفترة 95٪ وقيمة «n من N» عند الطرف. — Thick bars grow from the axis (green above threshold, red below) with a thin 95% interval whisker and 'n of N' at the tip.
- **متى أستخدمها / when:** استطلاعات، تقييم نماذج، قصص صحفية — surveys, model evals.
- **كيف / how:** Serif labels left; grow 800 ms easeOutCubic, stagger 200 ms; whisker draws after the bar; italic annotation; palette paper #eee8dc, ink #2b2622, red #c9463d, green #1f7a4f. **أرقام / params:** 800 ms; stagger 200 ms.
- **الدليل / proof:** `style:pm-henkvaness-0e06af`

#### DATA-43 · مقاييس وأشرطة تقدم بلون الحكم · Verdict-coloured meters & RTL-safe progress · 🟢 جاهز / ready
- **ماذا / what:** صفوف أعمدة متدرجة حسب الخطورة، ومقياس يتغير لونه حسب الحكم، وشريط تقدم ينمو من جهة البداية بالتحويل فقط. — Severity gradient bar rows, a meter whose colour follows the verdict, and a progress bar that grows from the start side via transform.
- **متى أستخدمها / when:** مخاطر، تدقيق، تقدم مهام — risk, audit, task progress.
- **كيف / how:** Rows: grid minmax(80px,1fr) 2.5fr 42px, fill = round(n/max·100)%; track 9 px #f1f5f9; fills 90deg critical #f43f5e→#ef4444, high #f59e0b→#f97316, medium #06b6d4→#6366f1, low #10b981→#14b8a6. Meter: width transition .5s ease, data-verdict approaching → warning, material → danger, anchored inline-end. Progress: translateX(-(100-value)%) height 8 px, 500 ms ease-out, aria-valuetext. **أرقام / params:** 500 ms ease; track 9 px.
- **الدليل / proof:** `kosif-audit-studio/v5/continuous-dashboard.js:31` · `kosif-audit-studio/styles.css:718` · `kosif-audit-pro/components/ui/progress.tsx` · `kosif-audit-pro/tests/ui-components.test.mjs`

#### DATA-44 · أشرطة مقسّمة إلى خانات · Segmented / dotted meters · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** صف مربعات أو نقاط يضيء واحدًا تلو الآخر حتى المستوى مع عدّاد مربوط، أو دلو بخانات يفرغ ويمتلئ. — A row of squares/dots lights up cell by cell to a level with a bound counter, or a slotted bucket drains and refills.
- **متى أستخدمها / when:** مهارات، حصص، تحميل، مهلة — skills, quotas, loading, leases.
- **كيف / how:** Cells light left→right (right→left in Arabic) 30–50 ms each, rows stagger 120 ms, end tag 'MAX' or '[x] Ready'; bucket: 10 rounded slots, blue #5aa8ff, partial top slot as thin bar, stroke red #f85149 at zero; lease bars drain linearly over 10 s, refill on check-in, 'EXPIRED' sticker at 0; trading-card variant: 3 labelled bars 600 ms ease-out stagger 150 ms. **أرقام / params:** 16–20 cells; 30–50 ms per cell; 0→98% in 1 s.
- **الدليل / proof:** `style:pm-anthonyriera-9b1b2a` · `style:pm-ibrahimwasim240-809370` · `style:pm-parkerrex-1a54fe` · `style:pm-gigabit-million-16b3a0`
- **شوهد أيضًا / also seen:** `style:pm-manuelogomigo-f33ca9` · `style:pm-0xnfrith-5be616` · `style:pm-sab8a-364a5a` · `style:pm-johnsavage-ai-b091c0`

#### DATA-45 · سباق المقارنة والسرعة · Speed / latency comparison race · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** شريطان أو أكثر يتسابقان: واحد يمتلئ فورًا أو يتجاوز حافة الإطار، والمنافسون يزحفون، وعدّاد الزمن ينزل. — Two+ bars race: one fills instantly or overshoots the frame edge, competitors crawl, a ms readout counts down.
- **متى أستخدمها / when:** «أسرع بعشر مرات»، قبل/بعد — speed claims, before/after.
- **كيف / how:** ease-in-expo on the brand bar to ≤120% width (breaking the frame is the joke), others ≤60%; timer counters per bar; before/after: two segmented timelines, the 'after' shorter in green. **أرقام / params:** 1–1.2 s; brand ≤120% width; others ≤60%.
- **الدليل / proof:** `kosif-tool/styles/pm-influencer-seo-ce8c33/BRIEF.md` · `style:pm-heyiammallik-e72d17` · `style:pm-polydao-7a572b` · `style:pm-prasad-pilla-2c0cba`

#### DATA-46 · لوحة احتمالات الكلمة التالية · Next-token probability panel · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** 4 كلمات مرشحة بأشرطة تنمو إلى احتمالاتها، والمختارة بشريط برتقالي وسهم، ثم تُكتب في سطر الأمر. — Four candidate tokens with bars growing to their probabilities; the chosen one turns orange with an arrow, then types into the prompt.
- **متى أستخدمها / when:** شرح الذكاء الاصطناعي والاحتمالات — explaining LLMs and probability.
- **كيف / how:** Bars grow 400 ms staggered 80 ms; values like 0.55/0.21/0.11/0.01; chosen bar accent + arrow; then typewriter with cursor; same pattern for prediction-market probability bars (600 ms easeOut, values count). **أرقام / params:** 400 ms; stagger 80 ms.
- **الدليل / proof:** `style:plotter` · `style:pm-polydao-7a572b`

#### DATA-47 · ترتيب يتغير والقوائم المرتبة · Rank swap & ranked lists · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** بطاقات مرتبة تنتقل إلى ترتيب جديد مع تحديث أرقامها، أو بطاقات أرقام تتحول إلى قائمة «الأضعف أولًا». — Ranked cards move to a new order while numbers update, or stat tiles cross-fade into a weakest-first list.
- **متى أستخدمها / when:** ترتيب بين فترتين، نتائج، لوحات صدارة — two-period ranks, leaderboards.
- **كيف / how:** MG-049: 0–2 s period one, 2–5 s reorder, 5–8 s period two; fixed slot positions per rank, paths that cross least, identity colour kept (FLIP). Tiles→list: opacity/translateY 30→0 then rows translateX 40→0 stagger .08 s; ranked rows 80–120 ms stagger with right-aligned scores and status pills (bg #fbe3e3, text #a8484a). **أرقام / params:** MG-049 8 s; rows 80–120 ms.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-data-infographics.md` · `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/index.html:102` · `style:pm-palashbagchi11-0a4b6b` · `style:pm-twoclipping-6dd14e`

#### DATA-48 · مخطط أعمدة دائري / شعاعي · Radial / clockwise bar chart · 💡 فكرة / idea
- **ماذا / what:** أعمدة تمتد من المركز للخارج أو قطاعات تنمو مع عقارب الساعة واحدًا تلو الآخر مع تسميات متأخرة. — Bars extend outward from the centre, or segments grow clockwise one at a time with delayed labels.
- **متى أستخدمها / when:** دورات زمنية، 12 شهرًا، ساعات اليوم — cyclic data.
- **كيف / how:** SVG arcs from −90°; each 300–500 ms cubic-bezier(0.33,1,0.68,1), 60 ms stagger, label +100–150 ms; length from the inner radius (area grows faster than value — say so or use constant-width wedges). **أرقام / params:** 300–500 ms/segment; stagger 60 ms.
- **الدليل / proof:** `kosif-tool/styles/pm-marouanegazouzi-6071d5/BRIEF.md` · `kosif-tool/styles/pm-monokern-ade5b6/BRIEF.md`

#### DATA-49 · المضاعفات الصغيرة · Small multiples · 📄 موصوف / documented only
- **ماذا / what:** كرّر نفس المخطط الصغير لكل فئة بمحاور مشتركة بدل تحميل مخطط واحد. — Repeat the same mini-chart per category with shared axes instead of overloading one chart.
- **متى أستخدمها / when:** 4–9 سلاسل لا يجب تكديسها — 4–9 series that must not be stacked.
- **كيف / how:** Grid columns = min(3, n), shared x and y, empty cells hidden; one neutral hue + accent; reveal panels in reading order (right-to-left rows in Arabic) with 60–100 ms stagger. **أرقام / params:** cols=min(3,n); stagger 60–100 ms.
- **الدليل / proof:** `kosif-atlas/skills/317-data/942-data-visualization/SKILL.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10330-statistical-and-uncertainty-visualizatio/references/distribution-and-summary-choices.md`

## الخطوط والمساحات والمنحنيات — Lines, areas & curves
_خط يُرسم بقلم يحمل الرقم، مساحات، شموع، تحوّلات، وعدم يقين._
#### DATA-50 · خط يُرسم مع مساحة ونقاط تقفز · Line draw-on with area fade & dot pops · ✅ مُثبت هنا / proven here
- **ماذا / what:** سلسلة 12 نقطة تُرسم بـ pathLength=1 والمساحة المتدرجة تظهر وكل نقطة تقفز حين يمر القلم. — A 12-point series draws via pathLength=1 dashoffset, a gradient area fades in, each dot pops as the pen passes.
- **متى أستخدمها / when:** اتجاه زمني واحد — one trend over time.
- **كيف / how:** series → path d; line.strokeDashoffset = 1 − prog(local,0.2,2.4,inOutCubic); dot r = 12·prog(draw, i/(n−1), +0.08, outBack); area gradient #7ee8d2 .35→0. Rendered here (preview frames 3.8–7.0 s: line, dots and counter 45→128). Honest note: in the starter the area gradient leads the pen slightly — reveal the area with a clip that follows the pen if that matters. **أرقام / params:** viewBox 900×620; stroke #7ee8d2 14 px round; dots #ffb86b r12; 2.2 s draw.
- **الدليل / proof:** `kosif-tool/starters/html-canvas/index.html:88` · `kosif-tool/starters/html-canvas/index.html:157` · `kosif-tool/playbooks/charts.md:37`
- **شوهد أيضًا / also seen:** `style:pm-rammanq-f5a90f` · `style:pm-charlesmendez-73b6e4` · `style:pm-daniel-haida-8691d4` · `style:pm-demonugc-4c5753` · `style:pm-miskinho-443898` · `style:pm-quickdesignio-dd93d0`

#### DATA-51 · خط يرسمه رأس قلم يحمل العدّاد · Pen-tip counter line · 🟢 جاهز / ready
- **ماذا / what:** الخط يُرسم والعدّاد يقرأ قيمة رأس القلم المستوفاة، والنقاط تقفز عند المرور، والمساحة تُملأ بعده. — The line draws while a counter reads the interpolated pen value; dots pop as it passes; area fills after.
- **متى أستخدمها / when:** قصة نمو يكون فيها آخر رقم هو الخلاصة — growth stories ending on the key number.
- **كيف / how:** Canvas drawFrame(t): axes alpha 0.2–0.6 s; head = ease((t−0.6)/1.2)·(n−1); tip value = lerp between neighbours; counter Noto Kufi Arabic 600 72 px; stroke #19c37d 6 px; axis #5a5a5a. Recipe B: axes 0–400, draw 400–1700, area to 18% 1700–2000, caption 2000–2400, hold to 4000 ms. Leading dot rides the tip, glow 6 px; tooltip pops at the max. **أرقام / params:** 1000–1400 ms per 1000 px ease-out cubic; dots spring {14,160,0.8} ≈250 ms; area 300 ms → 18%.
- **الدليل / proof:** `kosif-tool/playbooks/charts.md:151-181` · `kosif-tool/playbooks/charts.md:61-71` · `style:pm-sudeepsd-1a3485` · `style:pm-viktoroddy-98c1d8`
- **شوهد أيضًا / also seen:** `style:pm-astrodevil-3f2054`

#### DATA-52 · منحنى ناعم في Remotion · Remotion smooth cubic line · 📦 بأمر تثبيت / one install
- **ماذا / what:** 9 نقاط ببذرة ثابتة بمنحنى تكعيبي، تُرسم خطيًا مع كشف المساحة بقص، وشبكة منقطة تنمو، ونقاط بنابض، وعدّاد عربي. — Nine seeded points joined by a cubic path, drawn linearly with a clip-path area reveal, dashed grid growing, spring dots, Arabic counter.
- **متى أستخدمها / when:** عندما يكون المشروع Remotion — Remotion projects.
- **كيف / how:** makeSeries('kosif-chart') via remotion random(); smoothPath() with handles at 1/3; DRAW_START 12, DRAW_LENGTH 66 frames; dot spring damping 10 stiffness 180; counter 124 px 800 easeOutExpo Intl.NumberFormat('ar-EG'). **أرقام / params:** 920×620 viewBox; pad 60/40/50/70; stroke 10; grid 0/.25/.5/.75/1 dash '6 10'.
- **الدليل / proof:** `kosif-tool/starters/remotion/src/Film.tsx:253` · `kosif-tool/starters/remotion/src/Film.tsx:266` · `kosif-tool/starters/remotion/src/Film.tsx:281`
- **تثبيت / install:** `npm i remotion@4.0.536 @remotion/cli@4.0.536`
- **ترخيص / license:** Remotion company license (free for individuals and small teams; companies above the threshold need a paid license)

#### DATA-53 · مؤشر قراءة متحرك على المخطط · Chart scrub readout (playhead) · 📦 بأمر تثبيت / one install
- **ماذا / what:** خط تتبع وعلامة يتحركان على المنحنى وتلميح تاريخ/قيمة يتنقل عبر البيانات ويتوقف عند القمة. — A tracking line + marker moves along the baked polyline while a date/value tooltip steps through the data and stops on the peak.
- **متى أستخدمها / when:** شرح لحظة بعينها في سلسلة — explaining a specific moment in a series.
- **كيف / how:** Scrub 1.5–3 s, ≥0.8 s hold after; peak stop power3.out; series B lights up 0.25 s power2.out when crossed; tooltip pill snaps to the nearest point. Step-chart variant: state history as a step line up to t, vertical playhead, event ticks below coloured by outcome, dashed max line. **أرقام / params:** SCRUB_DUR 1.5–3 s; hold ≥0.8 s.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/chart-scrub-readout.md` · `style:pm-steventey-0d20e4` · `style:pm-twoclipping-5cba86` · `style:pm-parkerrex-1a54fe`
- **تثبيت / install:** `npm i -D hyperframes@0.8.164 && npx hyperframes add mk-line-graph`
- **ترخيص / license:** HyperFrames Apache-2.0; its runtime uses GSAP (GSAP standard no-charge license, not OSI)

#### DATA-54 · خط/مساحة مع مؤشر تقاطع · SKCharts line/area with crosshair · 🟢 جاهز / ready
- **ماذا / what:** مخطط خطي SVG بمساحة 10٪ ونقاط نهاية وتسميات نهاية وتخفيف للتسميات ومؤشر تقاطع. — SVG line chart with optional 10% area, end dots and end labels, label thinning and a crosshair tooltip.
- **متى أستخدمها / when:** تقارير ولوحات تُلتقط إطاراتها — reports and dashboards captured to frames.
- **كيف / how:** SKCharts.line({labels, series, area, endLabels, height, width}); label step = ceil(n / max(3, floor(iw/56))); end labels when ≤4 series (pr 70); point r 4; line 2 px. **أرقام / params:** 720×240.
- **الدليل / proof:** `kosif-earth-ci-fork/ui/components/charts.js:89`

#### DATA-55 · الخطوط المصغرة · Sparklines & micro-charts · ✅ مُثبت هنا / proven here
- **ماذا / what:** خطوط بحجم الكلمة بجانب الرقم الذي تشرحه، بعلامة آخر قيمة وحلقة ورقية. — Word-sized trend lines beside the number they explain, end marker with a paper ring.
- **متى أستخدمها / when:** بطاقات المؤشرات وصفوف الجداول — stat cards, table rows.
- **كيف / how:** PRESS primitives (Python → SVG string): sparkline 300×68, 2 px round-cap line, end dot r≥4 with 2 px paper ring, hairline grid; dual_sparkline for two series; SKCharts.spark(values,{w,h,color,accent}) 90×28 stroke 1.8 end r 3; trendSvg: x(i)=p+i(w−2p)/(n−1), evidence #6366f1 vs issues #ec4899 3 px. Animate by revealing the path then pulsing the end dot. **أرقام / params:** 300×68 px; end r≥4 + 2 px ring; draw 800 ms; area α .15.
- **الدليل / proof:** `kosif-atlas/skills/2622-city-report/9999-city-report/scripts/charts.py` · `kosif-earth-ci-fork/ui/components/charts.js:242` · `kosif-audit-studio/v5/continuous-dashboard.js:34` · `kosif-atlas/skills/2690-build-web-data-visualization/10319-canvas2d-data-visualization/references/sparklines-and-microcharts.md`
- **شوهد أيضًا / also seen:** `style:pm-ratheejaisal-1f4538`

#### DATA-56 · صعود ثم انهيار · Rise-then-crash line metaphor · 📦 بأمر تثبيت / one install
- **ماذا / what:** خط يصعد كالسهم أثناء ذكر الهدف، ثم مقطع أحمر سميك يهوي عند ذكر الفشل، والخلفية تُعتم مع الهبوط. — A line climbs while the goal is mentioned, then a thick red segment plunges on the failure line; background darkens with the decline.
- **متى أستخدمها / when:** قصص المخاطرة والخسارة والتحذير — risk, loss, warnings.
- **كيف / how:** drawPath(chartUp, 15.5 s, 2.8 s) stroke #7fd0ff 7 px; chartDown #ff5a5a 9 px drawn in 0.45 s at 19.64 s (on the spoken word); both fade at 23.6 s. HyperFrames decline-chart counts 82 → 34 while drawing down. Pixel variant: 12 green candles every 80–120 ms then 6 red ones and a falling line (style:pm-0xevinho-3777d8); crash comparison end labels −20% vs −28%. **أرقام / params:** up 2.8 s; crash 0.45 s.
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/index.html:234-237` · `kosif-one/vendor/hyperframes/registry/components/decline-chart/decline-chart.html` · `style:pm-0xevinho-3777d8` · `style:pm-rammanq-f5a90f`
- **تثبيت / install:** `npm i -D hyperframes@0.8.164 && npx hyperframes add decline-chart`
- **ترخيص / license:** HyperFrames Apache-2.0; its runtime uses GSAP (GSAP standard no-charge license, not OSI)

#### DATA-57 · الشموع وشريط الأسعار · Candlesticks & price ticker · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** شموع تظهر يسارًا ليمين بألوان صعود/هبوط، وحبة سعر حي تتبع آخر نقطة، وشريط رموز يمر. — Candles appear left→right in up/down colours, a live price pill tracks the last point, a ticker strip scrolls.
- **متى أستخدمها / when:** محتوى مالي وتداول — finance and trading.
- **كيف / how:** Candles 20 ms stagger, green #2ee6a6 / red #e5486b; price pill ticks every 100 ms with tabular nums; ticker tape rotated strip with mono symbols at 200 px/s; price-target scale: axis from→target with a green glowing marker; payoff curve: trapezoid green above zero, pink below. **أرقام / params:** 20 ms/candle; ticker 200 px/s.
- **الدليل / proof:** `style:pm-dale-vaz-cc612a` · `style:pm-aistocksavvy-3fb9f5` · `kosif-tool/styles/pm-0xevinho-3777d8/BRIEF.md`

#### DATA-58 · طبقة التعليقات والإبراز · Annotation & highlight layer · 🟢 جاهز / ready
- **ماذا / what:** تعليقات مربوطة بنقاط البيانات، فترات مظللة، وخطوط هدف متقطعة تشرح نقاط التحول. — Callouts tied to data points, shaded spans and dashed target lines that explain turning points.
- **متى أستخدمها / when:** عند كل نقطة تحول يذكرها التعليق — every turning point the narration names.
- **كيف / how:** Separate layer above marks: arrow callout label → point; shaded span ~20% alpha for a period (era bands); dashed grey target line with value label; short straight or gently elbowed leaders 0.75–1.25 px; label halo 2–3 px background stroke (paint-order stroke). Draw annotations after the data lands (+200 ms). **أرقام / params:** span α ~0.2; halo 2–3 px; leader 0.75–1.25 px.
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10320-d3-data-visualization/SKILL.md` · `kosif-atlas/skills/3455-business-analytics/14161-data-storytelling/references/details.md` · `style:pm-kloss-xyz-fe0c31`

#### DATA-59 · تحوّل المخططات · Chart morph (bars → donut / line / scatter) · 📦 بأمر تثبيت / one install
- **ماذا / what:** نفس البيانات تتحول من عرض إلى آخر: أعمدة تنثني إلى أقواس، أو أعمدة تصير خطًا، أو منحنى يتحول من شكل لآخر. — The same dataset morphs between views: bars bend into arcs, bars become a line, a curve changes generator.
- **متى أستخدمها / when:** من «الحجم» إلى «الحصة» في لقطة واحدة بلا قطع — size → share without a cut.
- **كيف / how:** Recipe D: axes fade 1600–1800 ms, labels detach 12 px; bend 1800–2700 cubic-bezier(.65,0,.35,1) keeping colour+label; centre total counts 2700–3000. Resample both paths to equal point counts (flubber or own resampler) then lerp; waveform morph between flat/sine/gaussian/square in 800 ms easeInOutCubic; ceiling → logistic S-curve 800 ms after a 250 ms strike scribble. Morph only between views of the same data. **أرقام / params:** 800–1000 ms in-out; old axis out 200 ms before, new in 200 ms after.
- **الدليل / proof:** `kosif-tool/playbooks/charts.md:85-95` · `kosif-tool/styles/morph-charts/SKILL.md` · `style:pm-rneayan-ea6129` · `style:pm-ik-builds-b8bdcf`
- **شوهد أيضًا / also seen:** `style:infographic`
- **تثبيت / install:** `npm i flubber@0.4.2`

#### DATA-60 · رسم بياني بخط اليد · Hand-drawn axis plot · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** محاور بأسهم وتسميات بخط اليد ثم منحنى ناعم أو مهتز يُرسم من اليسار لليمين بحبر لوني. — Axes with arrowheads and handwritten labels, then a smooth or noisy curve traced left→right in accent ink.
- **متى أستخدمها / when:** شروحات سبورة وأفكار — whiteboard explainers.
- **كيف / how:** Axes draw 300 ms each; curve 1.5–2.5 s; wobble jitter 1 px per frame for sketch feel (seeded); 'now $X' label updates with the pen; can use roughjs for the sketchy stroke. **أرقام / params:** curve 1.5–2.5 s; jitter 1 px.
- **الدليل / proof:** `style:pm-tak3sh8-be5012` · `style:pm-nikolajankovic-ce4ff4` · `style:pm-ik-builds-b8bdcf`

#### DATA-61 · مروحة مونت كارلو وعدم اليقين · Monte Carlo fan & uncertainty · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** ألف مسار عشوائي رفيع بشفافية 0.1 مع خط الوسيط وشارات المئينات. — 1000 thin random-walk paths at alpha 0.1 with a median line and percentile pills.
- **متى أستخدمها / when:** توقعات، استثمار، مخاطر — forecasts, investing, risk.
- **كيف / how:** Seeded random walks on Canvas (lighter alpha 0.1), draw over 1.5 s; median bold; shade the 5th–95th band; label the interval and n (scale honesty). **أرقام / params:** 1000 paths; α 0.1; 1.5 s.
- **الدليل / proof:** `style:pm-rammanq-f5a90f` · `kosif-atlas/skills/2690-build-web-data-visualization/10330-statistical-and-uncertainty-visualizatio/references/missingness-and-confidence.md`

#### DATA-62 · هيستوغرام نقاط يصير منحنى جرس · Dot histogram resolving to a bell curve · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** كل محاكاة تُسقط نقطة في عمودها والعدّاد يصل إلى N، ثم يُرسم منحنى طبيعي فوق الأكوام ويُظلل نطاق 5–95٪. — Each simulated result drops a dot into its bin while a counter ticks to N; then a normal curve draws over the stacks with the 5–95% band shaded.
- **متى أستخدمها / when:** شرح الاحتمالات والتوزيع — probability and distribution explainers.
- **كيف / how:** N=500, dot 4 px, 20–40 ms stagger, mono counter; curve draw 600 ms; bright marker rises 400 ms ease-out; stacked-dot variant sorted descending with long tail in black (dot 6 px, 1.2 s); particle histogram with labelled spike. **أرقام / params:** N=500; dot 4 px; curve 600 ms.
- **الدليل / proof:** `style:pm-marouanegazouzi-6071d5` · `style:pm-palashbagchi11-0a4b6b` · `style:pm-ismailfahmi-557268`

#### DATA-63 · رسم الدوال والمشتقة حيًّا · Live function & derivative tracer · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** محوران: الأيسر للدالة مع مماس ونقطة تتبع x، والأيمن يرسم المشتقة أثرًا، وتسمية الميل تتحدث حيًّا. — Left axes show f with a tangent + dot following x(t); right axes trace f'(x); slope label updates live.
- **متى أستخدمها / when:** شرح رياضيات، منحنيات التسهيل — math lessons, easing curves.
- **كيف / how:** x from −2 to 2 over 8–10 s linear; tangent ~1.2 units; slope label 2 decimals; progressive value table rows fade in with shift up; easing-graph variant: position vs time axes, cubic-bezier(.65,0,.35,1) with handles, playhead sweeping 1.5 s while a box moves with the same easing. manim is installable for this genre (pip install manim). **أرقام / params:** 8–10 s sweep; 2-decimal slope.
- **الدليل / proof:** `style:pm-linearuncle-5d2bae` · `style:pm-chatgptastra-0d95c7`

#### DATA-64 · راكب على خط المخطط · Glyph riding the chart path · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** أيقونة أو نقطة تُأخذ إحداثياتها من الخط أثناء رسمه (طائرة، كرة، نقطة تحويل من أ إلى ب). — A glyph or dot sampled from the drawing line (plane, ball, transfer dot A→B).
- **متى أستخدمها / when:** رحلات، تحويلات، «أين نحن الآن» — journeys, transfers, progress.
- **كيف / how:** pos = path.getPointAtLength(p·L); angle from a second sample 1 px ahead; 1800 ms ease-in-out; chips spring 180/14/1 ≤600 ms; ring pulse at arrival; journey bar: dot on a line between labelled endpoints. **أرقام / params:** 1800 ms; spring 180/14/1.
- **الدليل / proof:** `kosif-tool/styles/pm-utopyaszx-1b2f94/BRIEF.md` · `style:pm-davidmarcus-a28a60` · `style:pm-apoorvjain25-d24184`

#### DATA-65 · حقل خطوط الجبال · Ridge-line wave field · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** 30–40 خطًا أفقيًا متراكبًا يزيحها ضجيج مع نتوء مركزي، والخطوط السفلى محجوبة، والتدرج من السماوي للأحمر. — 30–40 stacked horizontal lines displaced by noise with a central bump, lower lines occluded, cyan→red by row.
- **متى أستخدمها / when:** خلفية بيانات أو صوت، توزيعات متعددة (ridgeline) — data/audio backdrops, ridgeline plots.
- **كيف / how:** Each row: fill below the polyline with the background to occlude rows beneath; noise amplitude × gaussian centre bump; animate noise time 0.5; colour by row index. **أرقام / params:** amp centre 60 px; speed 0.5; 30–40 rows.
- **الدليل / proof:** `style:pm-shinskinakamoto-20190b` · `style:pm-eyishazyer-af035b`

#### DATA-66 · مبعثر الحد الفعّال · Scatter with frontier curve · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** نقاط تقفز بتتابع ثم يُرسم المنحنى الحدّي وتُبرز أفضل نقطة. — Dots pop in sequence, then the frontier curve draws and the best point is highlighted.
- **متى أستخدمها / when:** علاقة بين متغيرين، مقايضات — two-variable trade-offs.
- **كيف / how:** Dots scale 0→1 with 10 ms stagger (order by x for reading flow); curve stroke-dashoffset after the last dot; best point ring pulse + label. **أرقام / params:** stagger 10 ms.
- **الدليل / proof:** `style:pm-rammanq-f5a90f`

## الحلقات والدوائر والمقاييس الدائرية — Rings, donuts & gauges
_نسبة من كل ثابت: حلقة، دونات، سائل يمتلئ، رادار، نجوم._
#### DATA-67 · حلقة التقدم المخروطية · Conic-gradient progress ring · 🟢 جاهز / ready
- **ماذا / what:** حلقة نسبة مرسومة بتدرج مخروطي زاويته متغير CSS مع قرص داخلي ورقم كبير في الوسط. — A percentage ring drawn with a conic gradient whose sweep is a CSS variable, inner disc and big centred numeral.
- **متى أستخدمها / when:** جاهزية، اكتمال، درجة جودة — readiness, completion, quality score.
- **كيف / how:** el.style.setProperty('--progress', pct·3.6+'deg'); background: conic-gradient(colour var(--progress), track 0); ::after inner disc inset 13 px (v4: 4 px). Variants: quality dial conic-gradient(#6366f1 calc(var(--score)*1%), #e0e7ff 0) 110 px value 30 px #4338ca; SKCharts.ring 56 px (48 px phones) with ok/warn/bad classes. Animate the variable from one scalar (register it with @property for smooth CSS interpolation). **أرقام / params:** legacy 190 px #72dbc4 / inner #351848 / 38 px; KOSIF4 210 px #d9f3c7 / 43 px weight 500.
- **الدليل / proof:** `kosif-audit-studio/styles.css:177` · `kosif-audit-studio/app.js:514` · `kosif-audit-studio/dashboard-capabilities.css` · `kosif-earth-ci-fork/ui/components/charts.js:218`

#### DATA-68 · دونات بخدعة المحيط 100 · Donut via r = 15.915 dasharray · 🟢 جاهز / ready
- **ماذا / what:** دائرة نصف قطرها 15.915 محيطها 100 فيصبح طول الشرطة هو النسبة مباشرة، مع دخول القطاعات بدوران وتتابع. — A circle with r = 15.915 has circumference 100, so each dash length is the percentage; segments spin in staggered.
- **متى أستخدمها / when:** حصص قليلة (≤5) — few shares.
- **كيف / how:** SKCharts.donut(segs,{center,sub}): viewBox 42, stroke-width 6, dasharray (p−.6) (100−p+.6), dashoffset −cumulative; centre total + caption; entrance .dn-seg 0.75 s from opacity 0 scale(.84) rotate(−12°), delay i·50 ms; hover dims others to .26. **أرقام / params:** gap .6; 0.75 s; 50 ms stagger.

```html
<svg viewBox="0 0 42 42"><!-- C = 2π·15.915 ≈ 100 -->
  <circle r="15.915" cx="21" cy="21" fill="none" stroke="#e5e7eb" stroke-width="6"/>
  <circle r="15.915" cx="21" cy="21" fill="none" stroke="#2a78d6" stroke-width="6"
          stroke-dasharray="39.4 60.6" stroke-dashoffset="25"/>   <!-- 40%, starts 12 o'clock -->
</svg>
```

- **الدليل / proof:** `kosif-earth-ci-fork/ui/components/charts.js:223` · `kosif-earth-ci-fork/ui/ds/components.css:322`

#### DATA-69 · مسح الدائرة بزاوية واحدة · Pie sweep (one eased angle) · 📄 موصوف / documented only
- **ماذا / what:** زاوية مُسهَّلة واحدة تدور حول الدائرة والشرائح تُقطع منها فتبقى النسب صحيحة في كل إطار. — One eased angle sweeps the circle; slices are cut from it so proportions are true every frame.
- **متى أستخدمها / when:** دائرة صادقة بأقل من 5 شرائح — an honest pie, ≤5 slices.
- **كيف / how:** A(t) = 360·e(t); slice k visible arc = clamp(A − start_k, 0, size_k); labels appear 120 ms after their slice completes; sorted from 12 o'clock clockwise. **أرقام / params:** 900 ms cubic-bezier(.65,0,.35,1); labels +120 ms.
- **الدليل / proof:** `kosif-tool/playbooks/charts.md:38`

#### DATA-70 · دونات متوهجة مع قائمة · Glowing donut with legend · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** قطاعات بشرطات تراكمية، والمميزة لها نسخة أعرض شفافة خلفها كتوهج، وقائمة صفوف بنقطة وتسمية وقيمة. — Segments as cumulative dashes; highlighted ones get a wider translucent duplicate behind for glow; legend rows with dot, label, value.
- **متى أستخدمها / when:** تركيب من 8 فئات في عرض بأسلوب أبل — 8-category composition, keynote look.
- **كيف / how:** strokeDasharray=[len, C] with cumulative offset; glow copy width ×2 opacity 0.3; highlighted legend rows white, others #86868b; bg #000 with navy radial glow #0d2944; bar bends into this ring with no cut. **أرقام / params:** 8 categories; glow ×2 / 0.3.
- **الدليل / proof:** `style:infographic`

#### DATA-71 · حلقة قياس مع عدّاد متزامن · Arc gauge with synced counter · 📦 بأمر تثبيت / one install
- **ماذا / what:** قوس رفيع يُرسم بينما تعدّ النسبة من نفس الاستدعاء، مع تلوين حسب الحالة وتجاوز 100٪ بالأحمر. — A thin arc draws while its percentage counts from the same call; colour by status, red past 100%.
- **متى أستخدمها / when:** درجات، استخدام، أهداف — scores, usage, goals.
- **كيف / how:** Basma ring: easeInOut over max(0.7, 0.55·d) s, arc from −90°, line width 0.2R, round caps, Rubik 900 %, label after 0.3 s, spring scale 0.7→1. Score ring 65→92 in 600 ms; amber→green when full (1.2 s); overage gauge: 60 outer ticks, stroke 10 px, colour lerps to red after 100%; stopwatch: arc + mm:ss counter 1.2 s; gauge arc cubic-bezier(0.22,1,0.36,1) 900 ms with the numeral on the same curve; at 100% swap to a check and burst 30 confetti pieces. **أرقام / params:** 600–1200 ms; stroke 10–14 px.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/mk-usage-arc/mk-usage-arc.html` · `app/public/js/00_editor.js:508` · `style:pm-sudeepsd-1a3485` · `style:pm-gabrielbuzziv-4ff0c6`
- **شوهد أيضًا / also seen:** `style:pm-en-ra-81c6dd` · `style:pm-daniel-haida-8691d4` · `style:pm-sudo-kiran-4f8b59` · `style:pm-sudo-kiran-6609ed` · `style:pm-blushpetal795-0c85c2`
- **تثبيت / install:** `npm i -D hyperframes@0.8.164 && npx hyperframes add mk-usage-arc`
- **ترخيص / license:** HyperFrames Apache-2.0; its runtime uses GSAP (GSAP standard no-charge license, not OSI)

#### DATA-72 · مقاييس HUD الدائرية · HUD radial gauges · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** قوس خارجي للتقدم وحلقة علامات داخلية تدور و16 معينًا يمتلئ بالتتابع، أو حلقة بأربعة أقواس ملونة وخانة أخيرة تتدحرج. — Outer progress arc, rotating inner tick ring and 16 diamonds filling in sequence; or a 4-colour segmented ring with a rolling last digit.
- **متى أستخدمها / when:** واجهات تقنية، خيال علمي، تحميل — tech/sci-fi HUDs, loading.
- **كيف / how:** Arc 2 px white, ring 60 ticks; diamonds fill blue in sequence; centre dot; % counter below. Segmented ring: stroke 14 px, ticks every 30°, marker dot rides the ring, last digit rolls 300 ms easeInOut. **أرقام / params:** 60 ticks; stroke 2–14 px.
- **الدليل / proof:** `style:pm-himanshutwtxs-5f4b43` · `style:pm-leonkohli-6dc01b`

#### DATA-73 · مقياس السائل والمنسوب · Liquid-fill & level gauges · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** دائرة أو أنبوب يمتلئ بسائل بسطح متموج وفقاعات، والرقم مربوط بنفس التقدم (حتى بكسور ¼ ½ ¾). — A circle or tube fills with wavy liquid and bubbles; the number is bound to the same progress (even ¼ ½ ¾ fractions).
- **متى أستخدمها / when:** وصفات ومقادير، حرارة، بطارية، مخاطرة — recipes, temperature, battery, risk.
- **كيف / how:** Liquid: fill 1.2 s, wave amplitude 6 px, lime; pour 1.5–2.5 s easeInOutSine with a ruler arrow following the surface y and ticks appearing as the level passes; thermometer: hatched 45° 6 px fill, user threshold blue line, red dashed danger line with handwritten labels (range 100–260%); battery fill with % count ~600 ms; gradient bar green→red with threshold ticks. **أرقام / params:** fill 1.2 s; wave 6 px; pour 1.5–2.5 s.
- **الدليل / proof:** `style:pm-leadnotifi-e83f94` · `style:pm-sarut0bisasuke-cefa43` · `style:pm-nikolajankovic-ce4ff4` · `style:pm-cansincengiz-me-cf68dd`
- **شوهد أيضًا / also seen:** `style:pm-ror-fly-9950f1`

#### DATA-74 · تعبئة النجوم والتقييم · Star-rating fill · 📦 بأمر تثبيت / one install
- **ماذا / what:** طبقة لون تمسح صف النجوم حتى التقييم مع الحفاظ على النجمة الكسرية الأخيرة، والقيمة تعدّ معها. — A colour layer sweeps the star row to the rating, keeping the fractional last star, value counting in sync.
- **متى أستخدمها / when:** مراجعات، إثبات اجتماعي — reviews, social proof.
- **كيف / how:** Clip a filled star row to width = rating/count·100%; 600 ms; proof tiles flip in rotateX 90→0 400 ms with 120 ms stagger (star meter, % ring, count). **أرقام / params:** rating 4.8 / 5; star fill 600 ms.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/star-rating-fill/star-rating-fill.html` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/stat-bars-and-fills.md` · `kosif-tool/styles/pm-ceowinkz-7c776b/BRIEF.md`
- **تثبيت / install:** `npm i -D hyperframes@0.8.164 && npx hyperframes add star-rating-fill`
- **ترخيص / license:** HyperFrames Apache-2.0; its runtime uses GSAP (GSAP standard no-charge license, not OSI)

#### DATA-75 · رادار المسح · Radar sweep with pings · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** حلقات متحدة المركز ووتد مخروطي يدور، والنقاط تضيء حين يمر المسح مع شارات تسمية. — Concentric rings with a rotating conic wedge; dots light up as the sweep passes, label chips fade in.
- **متى أستخدمها / when:** رصد، تتبع منافسين، اكتشاف فرص — monitoring, tracking, discovery.
- **كيف / how:** 4 rings 1 px; conic-gradient wedge 6–8 s/rev (or 1 rev/2 s for urgency); dot pulse 300 ms when |angle − sweep| < 3°; orbital variant: ellipse ry = 0.4 rx with tags (STEADY/RISING) and a growing green line chart beside it. **أرقام / params:** 6–8 s/rev; pulse 300 ms.
- **الدليل / proof:** `style:pm-xelandre-363f00` · `style:pm-blueoctopusai-dd17bd` · `style:pm-marouanegazouzi-6071d5`

#### DATA-76 · نصف دائرة البرلمان وحلقة النقاط · Parliament hemicycle & dot ring · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** نقاط على أقواس متحدة المركز ملونة حسب الحزب مع العدد في الوسط، أو آلاف النقاط على حلقة ملونة حسب حصة الفئة. — Dots on concentric arcs coloured by party with the centre count, or thousands of dots on an annulus coloured by share.
- **متى أستخدمها / when:** انتخابات، تمثيل، تركيب سكاني — elections, representation, demographics.
- **كيف / how:** Place seats row by row on arcs (outer rows more seats), sort by party angle; fill in order with 5–10 ms stagger; dot ring: 4500 dots scattered in an annulus, category by cumulative angle. **أرقام / params:** 4500 dots.
- **الدليل / proof:** `style:pm-triglyceee-bd5b08` · `style:pm-jesscaroline7-1ff7cb`

## الوحدات والشبكات والخرائط الحرارية — Units, grids & heatmaps
_نقطة لكل وحدة، تقويم، مصفوفات حرارة، وجداول تتكشف._
#### DATA-77 · مخطط الوافل: 100 نقطة · Waffle — 100 dots with synced percent · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** شبكة 10×10 والعدد المطابق للنسبة يتلون بالتتابع بينما عدّاد النسبة يصل معه في نفس الإطار. — A 10×10 grid where the matching count takes colour in sequence while a percent counter lands with it.
- **متى أستخدمها / when:** نسب يفهمها الجميع على الهاتف — shares that read instantly on phones.
- **كيف / how:** MG-043: 0–1 s grid, 1–3 s colouring with computed delay, 3–6 s explanation; state the unit ('كل نقطة = 1٪'); explain rounding; fill order right-to-left rows for Arabic (or random seeded order); 172-dot variant: dot 14 px gap 8 px, fill 1.5 s, salmon #e07b78 on grey #d9d9d9, outliers black; pictogram variant: 10×10 people icons, 10 ms stagger; isometric variant: 100 iso tiles, chosen ones extrude 50 ms stagger. **أرقام / params:** 10×10 = 100 cells; colouring 1.5–2 s.

```js
// k of 100 cells, Arabic reading order: rows top→bottom, cells right→left
const order = [...Array(100).keys()].map(i => ({ r: Math.floor(i / 10), c: 9 - (i % 10) }));
order.slice(0, k).forEach((cell, i) => {
  const p = clamp((t - t0 - i * (fillDur / k)) / 0.15, 0, 1);  // 150 ms per dot
  dot(cell).style.fill = mix(GREY, ACCENT, p);
});
pct.textContent = Math.round(k * clamp((t - t0) / fillDur, 0, 1)) + '٪';
```

- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-data-infographics.md` · `style:pm-palashbagchi11-0a4b6b` · `style:infographic` · `style:pm-blushpetal795-0c85c2`
- **شوهد أيضًا / also seen:** `style:pm-melvynx-6cde6c` · `style:pm-sudiyasa-f48ac9`

#### DATA-78 · مصفوفة الوحدات: نقطة لكل عنصر · Unit dot matrix (one dot per item) · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** نقطة لكل عنصر حقيقي (مثلًا 40×30) وتمييز مجموعة فرعية بلون التمييز. — One dot per real item (e.g. 40×30) with a subset highlighted in accent.
- **متى أستخدمها / when:** أعداد كبيرة يُراد الإحساس بحجمها — large counts that must feel big.
- **كيف / how:** Canvas for >500 dots; state the unit; highlight subset with a 5–10 ms stagger or a sweep; can later become particles that fly into a bar (DATA-14 rules: particle = entity). **أرقام / params:** 40×30 = 1200 dots.
- **الدليل / proof:** `style:pm-jesscaroline7-1ff7cb` · `kosif-atlas/skills/2690-build-web-data-visualization/10332-threejs-data-visualization/references/particle-effects-and-flow.md`
- **شوهد أيضًا / also seen:** `style:pm-itisrazak-3ad902`

#### DATA-79 · مقياس إلى شيء مألوف · Scale to a familiar object · 📄 موصوف / documented only
- **ماذا / what:** قيمة موثقة تتحول إلى صف وحدات بصرية مع مثال مقارنة واضح. — A documented value becomes a row of visual units with a clear comparison example.
- **متى أستخدمها / when:** أرقام مجردة ضخمة (لترات، أطنان، كيلومترات) — abstract huge numbers.
- **كيف / how:** MG-050: 0–1 s value, 1–4 s units form, 4–7 s comparison; write 'تقريبًا' when rounding; never compare length with area without converting; icon size by area if sized (DATA-06). **أرقام / params:** 7 s.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-data-infographics.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### DATA-80 · خريطة حرارية تقويمية · Calendar heatmap grid · 🟢 جاهز / ready
- **ماذا / what:** شبكة أيام على طريقة GitHub (الأسابيع أعمدة والأيام صفوف) ملونة بمقياس يومي. — A GitHub-style grid of days (weeks as columns, weekdays as rows) coloured by a daily metric.
- **متى أستخدمها / when:** عادات، نشاط، رمضان/التقويم الهجري — habits, activity, Ramadan/Hijri stories.
- **كيف / how:** Build week arrays from the first date; row = (weekday+6)%7 (Monday first); squares 10 px with 2 px gaps, left gutter 24 px, top 14 px for months; sequential ramp; animate fill by week column or random seeded order 40 ms stagger; Arabic month labels; serif-counter variant: 12×8 grid fill accelerating easeInExpo ~1.8 s with a big numeral in sync. **أرقام / params:** CELL 10, GAP 2, LEFT 24, TOP 14.
- **الدليل / proof:** `kosif-atlas/skills/1180-token-activity-graph/2788-token-activity-graph/graph.js` · `style:pm-astrodevil-3f2054` · `style:pm-fionntobin-97b7af`
- **شوهد أيضًا / also seen:** `style:pm-macrohou-33959d` · `style:pm-utopyaszx-1b2f94`

#### DATA-81 · خريطة المخاطر 3×3 بأربع درجات · 3×3 risk heatmap with 4-step scale · 🟢 جاهز / ready
- **ماذا / what:** مصفوفة احتمال × أثر يتحدد لون خليتها من الدرجة، بتدرج أخضر → أحمر بأربع درجات للفاتح والداكن. — A likelihood × impact matrix whose cell colour comes from the score, 4-step green → red in light and dark.
- **متى أستخدمها / when:** تقارير المخاطر والتدقيق — risk and audit reports.
- **كيف / how:** SKCharts.heatmap(grid,{sel}): score ≥6 h4, ≥4 h3, ≥3 h2 else h1; cells ≥52 px, 700 16 px Latin digits; labels منخفض/متوسط/مرتفع, axes الأثر/الاحتمالية; hover scale 1.04; for video light cells in score order 60 ms stagger. **أرقام / params:** light #cfe8d6 #f3e2a6 #f1b98a #e98a86; dark #1f5a3b #6b5a17 #7a4219 #7f2626.
- **الدليل / proof:** `kosif-earth-ci-fork/ui/components/charts.js:232` · `kosif-earth-ci-fork/ui/ds/tokens.css:48` · `kosif-earth-ci-fork/ui/ds/luxe.css:168`

#### DATA-82 · جدول حرارة الصفوف × الأعمدة · Matrix intensity table · 🟢 جاهز / ready
- **ماذا / what:** جدول صفوف × أعمدة شفافية لون كل خلية تعبّر عن قيمتها (مثل البنود × الأشهر). — Rows × columns table where each cell's brand-colour alpha encodes its value (items × months).
- **متى أستخدمها / when:** موسمية، مقارنة بنود عبر الزمن — seasonality, items over time.
- **كيف / how:** SKCharts.matrix({rows, cols, values, fmt}); --a = max(.08, v/max); class hi (white text) when a > .55; reveal column by column. **أرقام / params:** min α .08; highlight > .55.
- **الدليل / proof:** `kosif-earth-ci-fork/ui/components/charts.js:260`

#### DATA-83 · مخطط بنفورد للرقم الأول · Benford first-digit chart · ✅ مُثبت هنا / proven here
- **ماذا / what:** أعمدة SVG لتكرارات الرقم الأول المرصودة مقابل خط توقع بنفورد، مع تعليم الأرقام التي تنحرف بأكثر من 3 نقاط. — SVG bars of observed first-digit frequencies against the Benford expectation, flagging digits off by >3 points.
- **متى أستخدمها / when:** قصص كشف الاحتيال والتدقيق — fraud/audit stories.
- **كيف / how:** benfordAnalysis(amounts) → template-string SVG: per digit a rect bar, a short expected line, an axis text; classes .bar/.hot/.expected/.axis. Animate bars rising, then expected ticks draw, then hot digits pulse. **أرقام / params:** viewBox 420×186; bar 26 / pitch 44 / rx 5; expected 30.1/17.6/12.5/9.7/7.9/6.7/5.8/5.1/4.6%.
- **الدليل / proof:** `kosif-audit-studio/analytics.js:160` · `kosif-audit-studio/app.js:1290` · `kosif-audit-studio/styles.css:688`

#### DATA-84 · جدول يتكشف صفًّا صفًّا · Progressive table & status pills · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** جدول بعمودين وترويسة يُضاف صف مع كل خطوة، أو جدول مرتب برؤوس mono وشارات حالة حمراء. — A two-column table appends a row each step, or a ranked table with mono headers and red status pills.
- **متى أستخدمها / when:** عندما تكون الأرقام نفسها هي القصة (تقارب، أسوأ النتائج) — when the numbers themselves are the story.
- **كيف / how:** Row height ~6% H; each row fades in with shift up 12–20 px; header coloured like its series; ranked variant: rows slide up 120 ms stagger, right-aligned values, dead row tinted pink, pills #fbe3e3/#a8484a; end with an arrow note. Keep ≤6 rows on screen (no web tables). **أرقام / params:** row stagger 120 ms; ≤6 rows.
- **الدليل / proof:** `style:pm-linearuncle-5d2bae` · `style:pm-palashbagchi11-0a4b6b`

## البطاقات واللوحات والقوالب والمحركات — KPI cards, dashboards, templates & engines
_قوالب جاهزة ولوحات كاملة وملفات إكسل ومكتبات رسوم تتحول إلى إطارات._
#### DATA-85 · تشريح بطاقة المؤشر · KPI card anatomy · 📄 موصوف / documented only
- **ماذا / what:** الرقم يستحق الشاشة فقط إن قال أيضًا: جيد أم سيئ (الفجوة عن الهدف) وأفضل أم أسوأ (الاتجاه). — A headline number earns screen time only with good/bad (gap to target) and better/worse (trend).
- **متى أستخدمها / when:** كل بطاقة KPI — every KPI tile.
- **كيف / how:** Three layers: Number (right units, minimal decimals) · Meaning (target or prior period + signed gap with arrow) · Context (sparkline or tiny breakdown, only if useful). Neutral colour on target, deep red only when off. Tile = value + unit + delta + period + source. ≤3 tiles per frame, spring 14-120 pop, counters offset 600 ms, one highlighted at the end. **أرقام / params:** ≤3–4 tiles/frame; counters offset 600 ms.
- **الدليل / proof:** `kosif-atlas/skills/3455-business-analytics/14162-kpi-dashboard-design/SKILL.md` · `kosif-one/tools/kosif-omni/skills/kosif-web-design/references/web-playbook.md` · `kosif-tool/playbooks/charts.md:97`

#### DATA-86 · ثلاثية بطاقات الأرقام والإثبات · Stat-tile trio & proof cards · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** ثلاث بطاقات ملونة تعدّ إلى قيمها بينما خط يُرسم تحتها، أو عمود أرقام بجانب بطاقة أعمدة وخط وشارة «+301٪». — Three coloured tiles count up while a line draws beneath, or a column of numbers beside a bars+line card with a '+301%' chip.
- **متى أستخدمها / when:** إثبات نتائج، ملخص ربع سنوي — results proof, quarter recap.
- **كيف / how:** Count 800 ms easeOutExpo, line dashoffset 1.2 s; stats row: 3 columns split by 1 px rules drawing downward, count 600–800 ms, mono source tag; stacked cards slide 400 ms ease-out stagger 250 ms, number counts 600 ms as it lands; analytics card: header 'Views last 30 days', big number, green delta chip, line 700 ms, endpoint pops; card radius 16 px, stagger 120 ms; inspector panel slides x 100%→0 400 ms with +35%→+50% metric; analytics drawer slides up while the line draws 900 ms ease-out and counters tick 800 ms easeOutQuart. **أرقام / params:** 800 ms count; 1.2 s line; stagger 120–250 ms.
- **الدليل / proof:** `style:pm-bizibeast-10f264` · `style:pm-jasonzhou1993-8595e0` · `style:pm-samuel-yostt-891f87` · `style:pm-motiondsgnr-9dcfa6`
- **شوهد أيضًا / also seen:** `style:pm-arjunsh1607-93005d` · `style:pm-mehul4795-4a7007` · `style:pm-vanshwtfff-db0466` · `style:pm-eyishazyer-af035b` · `style:pm-kikelopezdesign-7cc9e8` · `style:pm-gigabit-million-16b3a0` · `style:pm-kmasiff-cc72cb` · `style:pm-thilina-a-891c09` · `style:pm-tankazunori0914-0fc886` · `style:pm-jazzen-chen-4542ae` · `style:pm-danilowm-d3720d`

#### DATA-87 · افتتاحية الرقم البطل · Hero-number opener card · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** رقم ضخم في الوسط أو اليسار مع سطرين تحته وشارات مصدر تقفز، أو رقم رفيع بخط serif. — A huge number centred or left with a two-line caption and source pills popping in, or a thin serif numeral.
- **متى أستخدمها / when:** أول 2 ثانية من فيلم بيانات — the first 2 s of a data film.
- **كيف / how:** Number 18–25% of frame height; tracked caption below; source pills pop (spring); italic byline; counter 600 ms easeOut; supporting graphic on the other side; metric-pair variant: two big numbers in columns beside a screenshot. **أرقام / params:** number 18–25% H; count 600 ms.
- **الدليل / proof:** `style:pm-henkvaness-0e06af` · `style:pm-blushpetal795-0c85c2` · `style:pm-madebyjmayala-b9204d`
- **شوهد أيضًا / also seen:** `style:pm-ajith-io-c52e09` · `style:pm-wani-shola-16ca7a` · `style:pm-reflex-cloud-72ffe5`

#### DATA-88 · سجل HyperFrames للبيانات · HyperFrames data registry (components & blocks) · 📦 بأمر تثبيت / one install
- **ماذا / what:** مكوّنات وكتل جاهزة للبيانات في نسخة HyperFrames المحلية: عدّادات، حلقات، أعمدة، خطوط، سباقات، وجدران شعارات. — Ready data components/blocks in the local HyperFrames copy: counters, rings, bars, lines, races, logo walls.
- **متى أستخدمها / when:** عندما تريد مشهد بيانات خلال دقائق على خط زمني GSAP — a data scene in minutes on a GSAP timeline.
- **كيف / how:** npx hyperframes add <name> copies into compositions/; mount on a class="clip" div with data-composition-src + data-start/data-duration/data-track-index; overrides as JSON in data-variable-values; one paused GSAP timeline, fromTo explicit states, transforms/opacity only. See the table below for every item and its variables. Chip-grid variant (5×N rounded chips coloured by category, 40 ms stagger) fits the same mount pattern.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/chart-story/chart-story.html` · `kosif-one/vendor/hyperframes/registry/blocks/data-chart/data-chart.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/count-up.mdx` · `kosif-one/vendor/hyperframes/registry/examples/nyt-graph/index.html`
- **تثبيت / install:** `npm i -D hyperframes@0.8.164 && npx hyperframes add chart-story`
- **ترخيص / license:** HyperFrames Apache-2.0; its runtime uses GSAP (GSAP standard no-charge license, not OSI)

| الاسم / name | النوع / kind | ماذا يفعل / does | متغيرات / variables |
|---|---|---|---|
| `animated-bar-chart` | component | بطاقة أعمدة تنمو بحتمية مع تسميات قيم | — |
| `chart-story` | component | bars | line | donut | progress بترتيب القراءة وتمييز واحد | type, data "12, 28, 45, 64", labels Q1..Q4, emphasize, unit % |
| `count-up` | component | عدّاد يصل للرقم الصحيح بنبضة واحدة | start 0, end 100, prefix/suffix, accent green|blue|violet, glow |
| `number-pop-in` | component | خانات تظهر بضبابية ورفع | value 5.7, unit k, lift close|standard|far, tone |
| `number-wheel` | component | عداد خانات دوّارة | spin single|double|triple, spacing, tone |
| `slot-machine-roll` | component | بكرة حروف/أرقام إلى نتيجة | result A7K, direction up|down, size |
| `conic-progress-ring` | component | حلقة مخروطية مع رقم مركزي | progress 0..100, thickness 4..30, label |
| `mk-usage-arc` | component | قوس رفيع يُرسم مع عدّ النسبة | — |
| `decline-chart` | component | خط يهبط والقيمة تنزل والخلفية تُعتم | label Retention, start_value 82, end_value 34 |
| `star-rating-fill` | component | مسح النجوم مع النجمة الكسرية | rating 4.8, starCount 1..10, showValue |
| `avatar-cloud` | component | صور رمزية حول عنوان مجتمع بخطوط | avatarCount 6..16, showLinks, label "50k builders" |
| `logo-wall` | component | جدار شعارات «يثق بنا» بتتابع | rows 2..4, cols 3..6, stagger 20..75 ms |
| `apple-money-count` | block | عداد مال $0→$10,000 بوميض أخضر وانفجار أيقونات (ملف الصوت غير موجود محليًا) | 5 s, 1920×1080 |
| `bar-chart-race` | block | سباق أعمدة مع إعادة قياس المحور والقائد مميز | periods 2019–2024, series lines, 12 s |
| `data-chart` | block | أعمدة + خط بأسلوب الصحافة | 15 s, Libre Baskerville + Libre Franklin |
| `mk-line-graph` | block | سلسلتان تُرسمان مع نقاط وتسميات على جبهة الرسم | 7 s |
| `mk-progress-stat` | block | رقم كبير يعدّ مع شريط تقدم إلى value/max | 7 s, light/dark |
| `mk-specs-list` | block | قائمة مواصفات بتتابع وخط تمييز | 8 s |
| `week-in-merges` | block | لوحة صدارة تتحرك فيها الصورة بسرعة تتناسب مع القيمة | 1080×1350, 16 s |
| `nyt-graph (example)` | example | مخطط تحريري على ورق #faf9f6 (ينقصه ملف فرعي محليًا) | 15 s; `npx hyperframes init --example nyt-graph` |

المصدر المحلي: `kosif-one/vendor/hyperframes/registry/{components|blocks|examples}/<name>/` والوثائق في `kosif-one/vendor/hyperframes/docs/catalog/`.

#### DATA-89 · مخططات مشاهد البيانات في HyperFrames · HyperFrames data blueprints & categories · 📄 موصوف / documented only
- **ماذا / what:** وصفات متعددة المراحل: عدّ تصاعدي مع كاميرا تخترق شبكة إحصاءات، محور نجوم، فئة «رقم إحصائي»، فئة «رسوم»، و«الأصل يصبح الرسم». — Multi-phase recipes: count-up with a camera pushing through a tilted stat grid, constellation hub, 'stat hit', 'charts', and 'asset fusion' (the object becomes the chart).
- **متى أستخدمها / when:** تخطيط اللقطات في shot-plan.json — shot planning.
- **كيف / how:** Pick by role from blueprints-index.md and cite the blueprint id per beat: dataviz-countup (4–12 s: ring/number → trend chart → tilted stat grid → land on hero metric); constellation-hub (5–8 s, end card ~2.5 s); category stat (~4–6 s hero count + ring); charts (one chart one message); asset-fusion (~5–8 s: straw → gauge, liquid → pie). **أرقام / params:** 4–12 s per blueprint.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/dataviz-countup.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/constellation-hub.md` · `kosif-one/vendor/hyperframes/skills/motion-graphics/categories/asset-fusion/module.md` · `kosif-one/vendor/hyperframes/skills/motion-graphics/categories/stat/module.md`

#### DATA-90 · ستايل الإنفوجرافيك بأسلوب أبل · Keynote infographic style · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** قصة بيانات على أسود بتوهج أزرق: كل شكل يتحول إلى التالي بلا قطع، أرقام تتدحرج كعداد المسافات، وتمييز واحد بكامل الوضوح. — A data story on black with blue glow: every shape morphs into the next with no cuts, odometer numbers, one highlight at 100%.
- **متى أستخدمها / when:** شرح نسب ومقادير بفخامة — premium ratio/quantity explainers.
- **كيف / how:** Palette #000000 bg, glow #0d2944/#021422, accents #4b89d1 #1239a0 #5b5be0, highlight #64d2ff, text #f5f5f7 / grey #86868b; IBM Plex Sans Arabic 300/500/700 (eyebrow grey ~2.5% H over bold white headline ~5%, hero number ~12–15% H with vertical cyan→blue gradient); lines rise from a mask translateY 70%→0 with blur clearing; counters 700–1000 ms ease-out cubic; one highlight 100%, others 35–45%; sfx whoosh/tick/drop; 16:9 ~28 s; scaffold python3 tools/kosif.py scaffold infographic <dir>. **أرقام / params:** 28 s; 30 fps; 2.0 wps.
- **الدليل / proof:** `style:infographic` · `kosif-tool/styles/infographic/SKILL.md` · `app/public/js/10_studio.js:701`

#### DATA-91 · ستايل البيانات المتحركة الداكن · Data-in-Motion dark style · 📄 موصوف / documented only
- **ماذا / what:** لوح داكن بلوحة فئات آمنة لعمى الألوان، أعمدة تنمو بتسهيل خروج، أرقام تعد، ومحور ثابت. — Dark board with a CVD-safe categorical palette, ease-out bars, counting numbers, fixed axis.
- **متى أستخدمها / when:** تقارير وفيديوهات تحليلية جادة — serious analytical films.
- **كيف / how:** bg #0D1B2A; series #3B82F6 #F59E0B #10B981 #EF4444 #A855F7; stagger 60 ms; tabular-nums; IBM Plex Sans Arabic 700; no animated pie, no 3D; values computed in code from clean CSV; source in the corner. **أرقام / params:** stagger 60 ms.
- **الدليل / proof:** `100-superskills/skills/trend-animation-styles/references/styles.md` · `100-superskills/skills/data-in-motion/SKILL.md`

#### DATA-92 · لوحات ألوان الرسوم · Chart palettes (categorical, sequential, semantic) · ✅ مُثبت هنا / proven here
- **ماذا / what:** لوحات فئات بترتيب ثابت للهوية لا للترتيب، مختبرة لعمى الألوان، مع تدرجات حرارة ومخاطر وإجهاد. — Fixed-order categorical palettes (identity, never rank), CVD-checked, plus heat, risk and utilisation ramps.
- **متى أستخدمها / when:** قبل أول لون في أي رسم — before the first chart colour.
- **كيف / how:** See the palette table below. Series colours bound to semantic anchors with a uniqueness test (passed in this container: node --test kosif-audit-pro/tests/palette.test.mjs → fail 0). 8-slot set worst adjacent ΔE 9.1 light / 8.4 dark; slots in identity order; kosif looks override c1/c2 with brand colours. Theme-aware series: shadcn ChartContainer injects per-series CSS vars with separate light/dark values (Recharts; recharts itself was not probed in this container). **أرقام / params:** ≤4 hues per chart (playbook); ≤6–8 total.
- **الدليل / proof:** `kosif-audit-pro/tests/palette.test.mjs` · `kosif-audit-pro/app/globals.css:40` · `kosif-earth-ci-fork/ui/ds/tokens.css:111` · `kosif-audit-pro/components/ui/chart.tsx`

| اللوحة / palette | القيم / values | ملاحظة / note | الدليل / proof |
|---|---|---|---|
| 8 فئات فاتح — categorical light | #2a78d6 #eb6834 #1baf7a #eda100 #e87ba4 #008300 #4a3aa7 #e34948 | worst adjacent ΔE 9.1 | `kosif-earth-ci-fork/ui/ds/tokens.css:111` |
| 8 فئات داكن — categorical dark | #3987e5 #d95926 #199e70 #c98500 #d55181 #008300 #9085e9 #e66767 | worst adjacent ΔE 8.4 | `kosif-earth-ci-fork/ui/ds/tokens.css:111` |
| سلاسل مربوطة بالهوية — anchored series (tested) | #5b2acb #087f86 #ad6700 #c93343 #39536f | uniqueness test passes here | `kosif-audit-pro/app/globals.css:40` |
| البيانات المتحركة الداكن — Data-in-Motion | bg #0D1B2A · #3B82F6 #F59E0B #10B981 #EF4444 #A855F7 | CVD-safe set | `100-superskills/skills/trend-animation-styles/references/styles.md` |
| مخاطر 4 درجات — risk heat light | #cfe8d6 #f3e2a6 #f1b98a #e98a86 | dark #1f5a3b #6b5a17 #7a4219 #7f2626 | `kosif-earth-ci-fork/ui/ds/tokens.css:48` |
| خطورة متدرجة — severity gradients | critical #f43f5e→#ef4444 · high #f59e0b→#f97316 · medium #06b6d4→#6366f1 · low #10b981→#14b8a6 | default #6366f1→#a855f7 | `kosif-audit-studio/v5/continuous-dashboard.js:31` |
| نسبة الإجهاد — utilisation ramp | <.35 #8cffc0 · <.72 #b4ed88 · <1 #ffe083 · ≥1 #ff907a | dashed 12/9 at failure | `kosif-studio/motion/twin_dashboard.py:1` |
| كينوت أزرق — keynote infographic | #000000 · glow #0d2944 · #4b89d1 #1239a0 #64d2ff · text #f5f5f7 / #86868b | one highlight, rest 35–45% | `style:infographic` |
| ورق تحريري — editorial paper | #eee8dc · ink #2b2622 · red #c9463d · green #1f7a4f | serif numerals | `style:pm-henkvaness-0e06af` |
| وافل سلمون — waffle salmon | #e07b78 on #d9d9d9 · pills #fbe3e3/#a8484a | outliers #111111 | `style:pm-palashbagchi11-0a4b6b` |
| الشموع — candles | up #2ee6a6 · down #e5486b |  | `style:pm-dale-vaz-cc612a` |
| مفقود — missing data | #777777 | never a zero colour | `kosif-atlas/skills/3202-quantitative-sciences/13564-scientific-visualization/SKILL.md` |

#### DATA-93 · رموز بطاقات البيانات التقنية · Tech-doc data-card tokens · 📄 موصوف / documented only
- **ماذا / what:** مظهر توثيق فاتح ثابت: IBM Plex Sans للنص وIBM Plex Mono بأرقام ثابتة للأرقام، وصفحة رمادية زرقاء ولوحة بيضاء. — A consistent light documentation look: IBM Plex Sans body, Plex Mono tabular numbers, blue-grey page and white panel.
- **متى أستخدمها / when:** رسوم تقنية/علمية هادئة — calm technical/scientific figures.
- **كيف / how:** CSS custom properties; Arabic pairs with IBM Plex Sans Arabic; page #e8ecf2, panel border #cdd5e1, ink #1d2632, muted #5d6a7a / #98a3b3, accents #1f6fe5 #e2640f #15a05a #2f6fe0 #dc2b3e. **أرقام / params:** #e8ecf2 #cdd5e1 #1d2632 ….
- **الدليل / proof:** `kosif-atlas/skills/3186-create-figure/13532-create-figure/SKILL.md`

#### DATA-94 · لوحة التوأم الإنشائي · Structural-twin dashboard & utilisation ramp · ✅ مُثبت هنا / proven here
- **ماذا / what:** صفحة HTML مستقلة: مخطط جملون ملون حسب نسبة الإجهاد، شريط حمل، تبويبات قبل/بعد، ترتيب الانهيار، وبطاقات أرقام تتحول إلى قائمة. — Self-contained HTML lab: truss coloured by utilisation, load slider, baseline/swap tabs, failure ranking, stat tiles turning into a list.
- **متى أستخدمها / when:** مشاريع هندسية ومحاكاة — engineering and simulation stories.
- **كيف / how:** python twin_dashboard.py report.json --out lab.html; embedded JSON; SVG 660×400 projected from node bounds; load .10–4.00× step .05; colour(u): u≥1 #ff907a (dashed 12/9), ≥.72 #ffe083, ≥.35 #b4ed88, else #8cffc0; HUD peak text same thresholds; grid 1.85fr/1fr collapses under 850 px; prefers-reduced-motion respected; bg #081213, lime #D0FF6A, mint #9DFFB4. **أرقام / params:** thresholds .35/.72/1.0.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/examples/structural-twin-demo.html:1` · `kosif-studio/motion/twin_dashboard.py:1` · `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/index.html:107`

#### DATA-95 · ملف إكسل برسوم أصلية · Excel workbook with native charts · ✅ مُثبت هنا / proven here
- **ماذا / what:** ملف .xlsx كامل في استدعاء واحد: جداول إكسل حقيقية، ترتيب، تنسيقات، مجاميع SUM حية، أوراق RTL، ورسم أعمدة/خط/دائري. — A finished .xlsx in one call: real Excel tables, sorting, formats, live SUM totals, RTL sheets and a bar/column/line/pie chart.
- **متى أستخدمها / when:** عندما يحتاج العميل البيانات نفسها بجانب الفيديو — when the client needs the data file beside the film.
- **كيف / how:** kosif_sheet_build sheets=[{name, headers, rows, sort, formats{money|percent|date|integer|code}, totals, chart{type:bar|column|line|pie, labels, values[], title}, rtl:true}] (openpyxl); kosif_db exports a SELECT to xlsx/csv with chart. Live Excel automation (kosif_excel, COM) works only on Windows with Excel open — not here. **أرقام / params:** chart 18×9 cm beside the table; TableStyleMedium2.
- **الدليل / proof:** `kosif-one/tools/kosif-omni/mcp-server/kosif_mcp/office.py:226` · `kosif-one/tools/kosif-omni/mcp-server/tests/test_office.py:56` · `kosif-one/tools/kosif-omni/mcp-server/kosif_mcp/office_live.py`

#### DATA-96 · مكتبات الرسوم كإطارات فيديو · Chart libraries as video frames · 📦 بأمر تثبيت / one install
- **ماذا / what:** D3 أو ECharts أو Chart.js أو Vega-Lite داخل صفحة تُرندر إطارًا إطارًا، بشرط تعطيل حركتها الداخلية وقيادتها بالزمن. — D3, ECharts, Chart.js or Vega-Lite inside a page rendered frame by frame, with their own animation disabled and driven by time.
- **متى أستخدمها / when:** خرائط معقدة، sankey، treemap، شبكات — complex forms you should not hand-build.
- **كيف / how:** Set animation:false (Chart.js/ECharts) and redraw from data(t) inside window.__kosif.seek(t); D3: compute layouts (d3-hierarchy treemap, d3-sankey, d3-geo) and interpolate attributes yourself; never ship default library styling (restyle: no legends, direct labels, palette DATA-92); render with node tools/render_html.cjs.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10320-d3-data-visualization/SKILL.md` · `kosif-tool/tools/render_html.cjs`
- **تثبيت / install:** `npm i d3@7.9.0   # or: echarts@6.1.0 | chart.js@4.5.1 | vega@6.4.0 vega-lite@6.5.0`
- **ترخيص / license:** d3 ISC; echarts Apache-2.0; chart.js MIT; vega/vega-lite BSD-3-Clause

#### DATA-97 · مشاهد بسمة للبيانات وقوالب أفلامها · Basma chart scenes & data-film templates · 🔑 مفتاح أو خدمة / needs key or paid service
- **ماذا / what:** مشاهد جاهزة في محرر بسمة (عدّاد، أعمدة، حلقة، قائمة) وفئة «أفلام البيانات» بخمسة قوالب يكتب Claude مشاهدها. — Ready scenes in the Basma editor (counter, bars, ring, list) and a 'charts' film category with five templates whose scenes Claude codes.
- **متى أستخدمها / when:** عند العمل داخل تطبيق بسمة — when working inside the Basma app.
- **كيف / how:** TEMPLATES.counter (lerp easeOut over max(0.6, 0.6d) s, Rubik 900 at 20% of min side), TEMPLATES.bars (2–5 bars, spring z .6 w 12, stagger 0.12 s from 0.25 s, IBM Plex Sans Arabic 700 labels), TEMPLATES.ring, TEMPLATES.list (0.32 s stagger, drawn tick). Film templates: data-story 12 s, bar-race 12 s, report-card (tiles + ring + sparkline), price-move (candle/line follow cam), survey (100-dot grid wave), plus milestone, dashboard-reveal, compare, math; rule: never invent figures. Coded film scenes call the Anthropic API (needs a key); the app itself needs its npm install.
- **الدليل / proof:** `app/public/js/00_editor.js:458` · `app/public/js/00_editor.js:469` · `app/public/js/00_editor.js:2007` · `app/public/js/00_editor.js:1777`
- **ترخيص / license:** owner code; scenes generated via the Anthropic API

#### DATA-98 · إنفوجرافيك مولَّد مستند إلى بحث · Search-grounded infographic generation · 🔑 مفتاح أو خدمة / needs key or paid service
- **ماذا / what:** نماذج صور Gemini تبحث عن حقائق حالية وترسمها إنفوجرافيك في طلب واحد. — Gemini image models look up current facts and render them as an infographic in one request.
- **متى أستخدمها / when:** مسودة بصرية سريعة أو مرجع شكل — a quick visual draft or look reference.
- **كيف / how:** Prompt in three parts: what to search, what to extract/analyse, how to render (chart type, theme). Treat every number as unverified: re-set exact figures in code (DATA-10) before publishing; never ship the raster as the chart.
- **الدليل / proof:** `kosif-atlas/skills/881-codex-seo/1954-seo-image-gen`
- **ترخيص / license:** needs a Google Gemini API key (paid service)

#### DATA-99 · مشاهد السرد بالتمرير كبيانات · Scrollytelling scenes as data · 📄 موصوف / documented only
- **ماذا / what:** قصص بيانات يتغير فيها المشهد مع التقدم: كل مشهد يعلن نصه وحالته البصرية وطبقة بياناته ومدى تقدمه. — Author-led data stories where state changes with progress: each scene declares text, visual state, data layer and progress range.
- **متى أستخدمها / when:** تحويل قصة ويب تفاعلية إلى فيديو أو العكس — web story ↔ video.
- **كيف / how:** Techniques: graphic sequence, animated transition, pan-and-zoom, sticky side-by-side, parallax depth. For video replace scroll progress with timeline time: progress = (t − scene.start)/scene.dur; keep a reduced-motion/static fallback frame per scene.
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10329-scrollytelling-and-parallax-data-visuali/SKILL.md`

#### DATA-100 · تخطيطات إنفوجرافيك العمليات · Process infographic layouts · 📄 موصوف / documented only
- **ماذا / what:** إنفوجرافيك خطوات مرقمة: خط زمني عمودي، مراحل أفقية أو شبكة بطاقات، يُرندر HTML إلى صورة. — Numbered-step infographics as vertical timeline, horizontal phases or a card grid, HTML rendered to PNG.
- **متى أستخدمها / when:** منشورات ثابتة أو بطاقات خطوات داخل فيلم — static posts or step cards inside a film.
- **كيف / how:** Step = 2–5 word title + <15-word description; 3–4 steps grid, 5–6 vertical timeline, 7–9 vertical with phases, 10+ compact; height 630 + 135 per step above 4 (cap 1500) at 1200 px; numbered circle markers 36 px on a 2 px rail. Rebuild from these ideas — do not copy the source code. **أرقام / params:** 1200 × (630…1500); marker 36 px; rail 2 px.
- **الدليل / proof:** `kosif-atlas/skills/x4919-visual-gen/x20319-process-infographic/SKILL.md`
- **ترخيص / license:** source package declared copyleft/WTFPL-like (x4919): use the ideas only, write your own code

#### DATA-101 · الخطوط الزمنية المتحركة · Animated timelines & Gantt traces · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** خط زمني تُرسم موصلاته المتوهجة مع دخول البطاقات، أو نقطة حمراء تنتقل إلى سنة كل فصل، أو أشرطة جانت تنمو بالتتابع. — Timelines whose glowing connectors draw as cards spring in, a red dot hopping to each chapter year, or Gantt bars growing in sequence.
- **متى أستخدمها / when:** تاريخ، مراحل مشروع، سجل تنفيذ — history, project phases, execution logs.
- **كيف / how:** Gantt only when the data has real start/end dates (task grid left, time right, milestones distinct from spans, restrained dependencies, today/deadline line only when it answers a question), else a milestone timeline; MG-042: 0–1 axes, 1–5 draw, 5–8 milestone, x proportional to real time; connectors stroke-dashoffset 600 ms with a 30% blurred duplicate glow; scrubber: 1 px line with ticks, red dot ease inOut 0.8 s, year label bottom-left; execution trace bars grow 200 ms stagger 120 ms, retry in amber; commit timeline: line 900 ms, nodes scale 0→1 150 ms; Arabic timeline with coloured year tags (time axis stays LTR). **أرقام / params:** connector 600 ms; dot hop 0.8 s; bars 200 ms.
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10323-gantt-chart-visualization/references/gantt-chart-design-and-use-cases.md` · `style:pm-aschapmann-131210` · `style:pm-buildfastwithai-53234e` · `style:pm-sachaarbonel-8f14f4`
- **شوهد أيضًا / also seen:** `style:pm-triglyceee-bd5b08`

#### DATA-102 · الشبكات والمحاور والأقواس · Networks, hubs & brackets · 📦 بأمر تثبيت / one install
- **ماذا / what:** صور رمزية على حلقة بيضاوية بخطوط منقطة إلى محور مركزي، عناقيد شبكية متوهجة، وشجرة مسابقات تسري فيها نبضات ضوء نحو المركز. — Avatars on an elliptical ring with dashed lines to a hub, glowing network clusters, and tournament brackets with light pulses travelling to the centre.
- **متى أستخدمها / when:** مجتمعات، إثبات اجتماعي، منافسات، توزيع من مصدر واحد — communities, social proof, tournaments, fan-outs.
- **كيف / how:** Hub scale 0.8→1 back.out, avatars 0→1 back.out with stagger, lines draw after (avatarCount 6–16, label '50k builders'); bracket: lines draw 500 ms, pulses ~600 px/s leaf → final, final node flares with bloom; calendar fan-out: one event chip sends 4 curved Béziers (2 px, 100 ms stagger) to channel badges; week-in-merges: avatar bounces across its row at speed ∝ merged PRs (speed encodes value only with labels — DATA-14). **أرقام / params:** avatars 6–16; pulse ~600 px/s.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/avatar-cloud-network.md` · `kosif-one/vendor/hyperframes/registry/blocks/week-in-merges/week-in-merges.html` · `style:pm-madhav-xo-f97f20` · `style:pm-bizibeast-10f264`
- **شوهد أيضًا / also seen:** `style:pm-ismailfahmi-557268` · `style:pm-yunn260414-60d996`
- **تثبيت / install:** `npm i -D hyperframes@0.8.164 && npx hyperframes add avatar-cloud`
- **ترخيص / license:** HyperFrames Apache-2.0; its runtime uses GSAP (GSAP standard no-charge license, not OSI)

#### DATA-103 · أدوات التحليل الخلفية · Analysis back-office skills · 📄 موصوف / documented only
- **ماذا / what:** مهارات المالك لتحضير البيانات قبل التحريك: SQL، دفاتر بايثون، نماذج إكسل مالية، وتقدير الاحتمالات. — Owner skills for preparing data before animating: SQL, Python notebooks, Excel financial models, forecasting.
- **متى أستخدمها / when:** عندما تأتي البيانات خامًا أو تحتاج حسابًا قبل الرسم — raw data or calculations before charting.
- **كيف / how:** Load the matching SKILL.md (sql-data-analysis, notebooks-python-analysis, excel-financial-models, forecasting-probability) and follow its steps; output a clean CSV/JSON that the chart scene reads at the top of the composition (data arrays first, so values are easy to swap).
- **الدليل / proof:** `100-superskills/skills/sql-data-analysis/SKILL.md` · `100-superskills/skills/notebooks-python-analysis/SKILL.md` · `100-superskills/skills/excel-financial-models/SKILL.md` · `100-superskills/skills/forecasting-probability/SKILL.md`

#### DATA-104 · تقاطع فن والأشرطة الطيفية · Venn overlap & spectrum indicator · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** دائرتان بمزج multiply تنزلقان لتلتقيا، وشريط طيفي بعلامة تنزلق إلى الموضع. — Two multiply-blended circles slide together; a rainbow spectrum bar with a sliding marker.
- **متى أستخدمها / when:** التقاطع بين فئتين، موقع على مقياس — overlap of two sets, position on a scale.
- **كيف / how:** Venn: mix-blend-mode multiply, 700 ms ease, overlap label appears after contact; spectrum: 20 gradient segments, marker slides with the one-scalar rule and a value label. **أرقام / params:** 700 ms; 20 segments.
- **الدليل / proof:** `style:pm-rneayan-474bcf` · `style:pm-reflex-cloud-72ffe5` · `style:pm-madebyjmayala-b9204d`

#### DATA-105 · أيقونة مخطط أعمدة · Mini bar-chart hero icon · 🟢 جاهز / ready
- **ماذا / what:** بطاقة متجهة بأربعة أعمدة صاعدة تصلح استعارة مالية/بيانات (بلا بيانات حقيقية). — A vector card with four rising accent bars as a finance/data metaphor (no data binding).
- **متى أستخدمها / when:** رمز في عنوان أو انتقال — a symbol in a title or transition, never as evidence.
- **كيف / how:** icon(ctx,'chart',r,…) bars height r·(.26 + .35·i); if numbers are shown next to it, replace it with a real chart. **أرقام / params:** 4 bars.
- **الدليل / proof:** `fastify-motion-bro/web/editorial.js:26`

## توليفات قوية / power combos

- **الرقم المنطوق يصير رسمًا** — DATA-19 + DATA-29 + مزامنة الكلمات (AUDIO/words.json): إطار وصول العدّاد = بداية الكلمة المنطوقة، والحلقة على الجانب الحر من المتحدث. — the counter lands on the spoken word's start frame.
- **قصة كينوت بلا قطع** — DATA-90 + DATA-77 + DATA-40 + DATA-41 + DATA-70 + DATA-59: كرة → شبكة 10×10 → شريط → زووم → دونات، كل انتقال تحوّل لنفس البيانات.
- **سباق على الإيقاع** — DATA-37 + MUSIC/beat map: حدود الفترات على الضربات القوية (1000 ms ≈ 60 BPM أو كل ضربتين عند 120 BPM)، وتسمية الفترة تتبدل على الـdownbeat.
- **عدّاد فوق اللقطات مع ترجمة عربية** — DATA-33 + ARAB (أرقام ثابتة العرض وعزل الاتجاه) + تدرج لوني للّقطة: عتّم 45٪ واترك الرقم أبيض بكامل التباين.
- **إثبات اجتماعي في 4 ثوانٍ** — DATA-74 + DATA-71 + DATA-102 في بطاقات تنقلب rotateX 90→0 بفارق 120 ms.
- **من الصدمة إلى الخلاصة** — DATA-87 → DATA-51 → DATA-58 → DATA-18: يطابق قوس القصة في DATA-04.
- **فيلم + ملف** — أي مشهد بيانات + DATA-95: نفس CSV يغذي الفيلم وملف .xlsx بجدول ورسم أصلي يسلَّم مع الفيديو.
- **خريطة رحلة بأرقام حقيقية** — DATA-28 + MAP (style:map-journey): كيلومترات هافرساين حقيقية موزعة على طول القوس، ونقاط تقدم تمتلئ لكل محطة.
- **توهج للبيانات بدون كذب** — DATA-32 + GLOW (توهج متعدد الطبقات) على الرقم والنقطة الأخيرة فقط، لا على الأعمدة (لا ظلال ولا تدرجات على علامات البيانات).
- **سبورة رياضيات** — DATA-60 + DATA-63 + DRAW (رسم بخط اليد ورأس قلم): المحاور ترسم نفسها ثم المنحنى بحبر لوني.

## أخطاء ممنوعة / never do

- **نابض أو تجاوز على عمود بيانات** — العمود الذي يتجاوز قيمته 100 ms يكذب 100 ms؛ النوابض للشارات فقط. — spring/backOut on data bars lies for its overshoot.
- **محور مقطوع بلا إعلان** — أعمدة لا تبدأ من صفر تضخم الفرق؛ اطبع المدى وعلامة الكسر أو ابدأ من صفر. — truncated axes inflate differences.
- **رقم مخترع بلا وسم** — كل رقم من مصدر، أو «توضيحي» داخل الإطار؛ لا تنشر أرقام إنفوجرافيك مولد بالذكاء الاصطناعي قبل إعادة كتابتها في الكود. — invented or AI-raster figures shipped as fact.
- **عدّاد ينتهي بقيمة مقرّبة أو مهتزة** — الإطار الأخير = القيمة الدقيقة، وtabular-nums دائمًا وإلا يرتعش العرض. — counters must land exact with tabular figures.
- **قلب محور الزمن في العربية** — الزمن يبقى من اليسار لليمين؛ اعكس التخطيطات الفئوية فقط، ونظام أرقام واحد للفيلم كله. — never mirror the time axis; never mix ٠١٢ and 012.
- **دائرة بشرائح كثيرة أو ثلاثية الأبعاد** — العين لا ترتب الزوايا المتقاربة، والمنظور يشوّه القراءة؛ ≤5 شرائح وإلا أعمدة. — 3D or many-slice pies distort.
- **نصف القطر خطيًا مع القيمة** — الفقاعة بقيمة مضاعفة تبدو أربعة أضعاف؛ r ∝ √value. — linear radius quadruples perceived size.
- **وصل الفجوات أو رسمها صفرًا** — المفقود يبدو مفقودًا (#777777، خط مكسور أو متقطع موسوم). — gaps drawn as zeros mislead.
- **لوحات ويب في الفيديو** — جداول طويلة، وسائل إيضاح صغيرة منفصلة، 6 لوحات، وإعدادات مكتبة افتراضية: المشاهد لا يستطيع التوقف للبحث. — web dashboards don't read at video speed.
- **السرعة وحدها تحمل الكمية** — المشاهد لا يقارن السرعات؛ الكمية للطول واللون والتسمية. — never encode quantity with speed alone.
- **تمييزان في وقت واحد** — عنصر واحد 100٪ والباقي 35–45٪، ونهاية كل رسم تثبت ≥1500 ms. — two highlights cancel each other; no hold = unread.
- **Math.random أو حركة مكتبة داخلية في الرندر** — الإطارات تُلتقط بالبحث seek(t)؛ استخدم بذرة ثابتة وعطّل animation في Chart.js/ECharts. — non-deterministic frames flicker between renders.

## أقوى 5 حركات توقيع / 5 signature moves

1. **DATA-15 + DATA-35 — قيمة واحدة، أعمدة من الصفر، أرقام تعد معها.** 600–800 ms cubic-bezier(.22,1,.36,1)، تتابع min(80,700/n) ms، والرقم الدقيق في الإطار الأخير. أول ما تمد يدك إليه في أي مقارنة.
2. **DATA-50 / DATA-51 — خط يُرسم وعدّاد عند القلم.** مُثبت هنا بالرندر؛ 1000–1400 ms لكل 1000 px، نقاط بنابض 14/160، مساحة إلى 18٪، ثم الخلاصة تحت الرسم.
3. **DATA-21 — عداد الأسطوانة للرقم البطل.** تأخير 40 ms لكل خانة، ضبابية عمودية 0–8 px، الأصفار البادئة 30٪، وتوهج عند الهبوط على الكلمة المنطوقة.
4. **DATA-77 — 100 نقطة تتلون مع عدّاد النسبة.** أسرع طريقة ليفهم مشاهد الهاتف نسبة؛ ترتيب ملء من اليمين، ووحدة مكتوبة «كل نقطة = 1٪».
5. **DATA-59 — نفس البيانات تتحول بلا قطع.** المحاور تخرج قبل 200 ms، الأعمدة تنثني إلى أقواس 900 ms cubic-bezier(.65,0,.35,1)، والمجموع يعد في الوسط — توقيع style:infographic.
