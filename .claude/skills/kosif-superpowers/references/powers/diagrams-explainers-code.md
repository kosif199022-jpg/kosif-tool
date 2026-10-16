# المخططات والشرح والكود — Diagrams, explainers & code

> **قوتك هنا:** أنت تشرح بالحركة: مخطط يُبنى بالترتيب السببي مع الصوت، عقدة تقفز ثم رابط يُرسم ثم نبضة بيانات تجري، كود يُكتب ويُبرز ويتحول، معادلة تتكون خطوة خطوة دون أن تنعكس داخل جملة عربية، ونموذج هندسي حقيقي تُحسب أرقامه ثم تتحول إلى فيلم.
> **أقوى دليل:** حلّال «التوأم الإنشائي» شُغّل هنا فأعطى معامل أول انهيار 2.946× لعيّنة المثلث، ومرّت اختباراته (17/17)، ومرّ فحص القواعد الثابتة لتركيب دورة المياه في `kosif-studio`، واختبار تحويل الصورة إلى برنامج بايثون مطابق.
> **You can:** plan, lay out, build, animate and narrate diagrams, code scenes and math/science explainers — RTL-aware. **64 powers follow** — ✅ 2 · 🟢 11 · 📦 10 · 🔑 1 · 👁 12 · 📄 26 · 💡 2.

**الحالة / status:** ✅ مُثبت هنا (كود + اختبار أو رندر في هذه الحاوية) · 🟢 جاهز (كود المالك يعمل بلا إضافات) · 📦 بأمر تثبيت · 🔑 مفتاح أو خدمة · 👁 شوهد في فيديو أنتجتَه (وصفة البناء مرفقة) · 📄 موصوف فقط · 💡 فكرة.
مسارات الدليل نسبية إلى `/home/user/`؛ `style:<id>` = فيديو مرجعي أنتجتَه سابقًا (ملاحظاته في `kosif-tool/styles/<id>/`).

**قاعدة العربية:** في المخطط العربي العقدة الأولى يمينًا والأسهم تشير يسارًا، والكود والمعادلات والمعرّفات اللاتينية تبقى LTR معزولة داخل الجملة العربية (`kosif-tool/playbooks/diagrams.md` §RTL، `kosif-tool/playbooks/code.md`).

## الفهرس / contents
- **قواعد المخطط — Diagram grammar & composition** — EXPL-01 … EXPL-09 (9)
- **بناء المخططات بالكود — Building diagrams in code** — EXPL-10 … EXPL-15 (6)
- **حركة المخطط — Diagram motion recipes** — EXPL-16 … EXPL-31 (16)
- **الكود على الشاشة — Code on screen** — EXPL-32 … EXPL-43 (12)
- **الرياضيات والعلوم والهندسة — Math, science & engineering** — EXPL-44 … EXPL-55 (12)
- **بطاقات الشرح والوثائق — Explainer cards & documents** — EXPL-56 … EXPL-64 (9)
- توليفات قوية / power combos · أخطاء ممنوعة / never do · أقوى 5 حركات توقيع / 5 signature moves

## قواعد المخطط — Diagram grammar & composition

_قبل الحركة: كم عقدة، أي نوع، أي لون، وأي اتجاه._

#### EXPL-01 · قواعد تركيب مخطط الشرح · Explainer diagram composition · 📄 موصوف / documented only
- **ماذا / what:** اختزل النظام إلى 3–7 مكونات و5 خطوات كحد أقصى، باتجاه قراءة واحد وأقل تقاطعات، والأحمر للمشكلات فقط والأصفر لبطل واحد. — Reduce a system to 3–7 components and ≤5 steps, one reading direction, fewest crossings; red only for problems, one yellow hero.
- **متى أستخدمها / when:** أي مخطط شرح — any explainer diagram.
- **كيف / how:** ≤7 nodes visible at once (bigger systems in chapters with camera moves); density ~4/10 — more than ~9 nodes means two diagrams; circled step numbers only when order matters; neutral lines for normal flow; accent on ≤2 nodes; reuse one fixed layout JSON across scenes and animate only highlight changes; if a table says it better, use the table. **أرقام / params:** 3–7 nodes; ≤5 steps; ≤2 accents.
- **الدليل / proof:** `kosif-tool/playbooks/diagrams.md:16` · `kosif-atlas/skills/1098-akbun-presentation/2476-akbun-presentation-visual/SKILL.md` · `kosif-atlas/skills/345-visuals/1242-html-diagram/SKILL.md`

#### EXPL-02 · قواعد العقد والروابط · Node & edge grammar · 📄 موصوف / documented only
- **ماذا / what:** عائلة أشكال واحدة وسماكة خط واحدة، روابط مستقيمة أو بانحناءة قائمة واحدة، والمنحنيات لحلقات الرجوع فقط. — One shape family, one stroke width, straight or one-bend orthogonal edges, curves only for feedback loops.
- **متى أستخدمها / when:** رسم أي عقد وروابط — drawing any nodes and links.
- **كيف / how:** radius 16–24 px; stroke 3–4 px; arrowheads 14–18 px (SVG marker orient="auto", refX near the tip, ~3–4× stroke); node labels 32–44 px, edge labels 24–28 px at 1080 width; right-angle rounded elbows, no diagonals; 6–10 px gap between an arrow label and its line; ≥12 px between attach points on one edge; no connector behind a non-endpoint box; 4 px grid; editorial palette paper #f5f5f5, ink #2d3142, muted #4f5d75, soft #7a8399, accent #eb6c36, link #2e5aa8. **أرقام / params:** stroke 3–4; heads 14–18; labels 32–44 / 24–28 px.
- **الدليل / proof:** `kosif-tool/playbooks/diagrams.md:15` · `kosif-atlas/skills/345-visuals/1242-html-diagram/references/svg-primitives.md` · `kosif-atlas/skills/2657-figures/10114-svg-primitives`

#### EXPL-03 · اختيار نوع المخطط والتخطيط · Diagram type & layout chooser · 📄 موصوف / documented only
- **ماذا / what:** ثمانية أنواع تغطي معظم الشروح، ولكل بنية خوارزمية تخطيط تناسبها، والشكل نفسه يجب أن يحمل الحجة. — Eight types cover most explainers; each structure has its layout algorithm; shape carries the argument.
- **متى أستخدمها / when:** أول قرار في أي شرح بصري — the first decision in any visual explanation.
- **كيف / how:** branching decisions → flowchart; messages over time → sequence; components + links → architecture; dated events → timeline; parent–child → tree; cross-team handoffs → swimlane; two-axis positioning → quadrant; reinforcing cycle → loop; data → ER. Layouts: rooted trees → tidy tree (Reingold–Tilford/Buchheim); flows/state machines → layered Sugiyama (+ orthogonal routing for ports/ERDs); undirected networks → stress / Kamada–Kawai / Fruchterman–Reingold; distance from root → radial; cycles → circular; prefer stable layouts when animating revisions. Patterns: fan-out, convergence, cycle, assembly line chaos → order, side-by-side, gap (DRAW-43). **أرقام / params:** 8 types; ≤12 nodes in Mermaid.
- **الدليل / proof:** `kosif-atlas/skills/345-visuals/1242-html-diagram/SKILL.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10326-node-link-and-diagram-layout/references/algorithm-selection.md` · `100-superskills/skills/diagrams-mermaid-architecture/SKILL.md:21`

#### EXPL-04 · ترتيب البناء السببي وحالات العقد · Causal build order & node states · 📄 موصوف / documented only
- **ماذا / what:** تظهر العقدة، يُرسم رابطها الخارج، وتقفز التالية حين يصلها القلم؛ النشطة بلون التأكيد، المزورة 70%، والمستقبلية غير مرسومة. — Node appears, outgoing edge draws, next node pops when the pen arrives; active accent, visited 70%, future not drawn.
- **متى أستخدمها / when:** كل مخطط يُبنى أمام المشاهد — every diagram built on screen.
- **كيف / how:** paint order background → connectors → boxes → labels (lines pass under shapes) in named <g> layers, animated in the same order; node stagger 0.08–0.15 s; reading order RTL for Arabic; front-load nothing — reveal each node on its spoken word (EXPL-21). The whiteboard-draw proof film (verified 13/13) builds a cause → effect diagram this way: sun and water drop, then two causal arrows, then the plant and the circled result. **أرقام / params:** stagger 0.08–0.15 s; visited 70%.
- **الدليل / proof:** `kosif-tool/playbooks/diagrams.md:19` · `kosif-tool/playbooks/diagrams.md:26` · `kosif-tool/.claude/skills/kosif-superpowers/proofs/whiteboard-draw/README.md` · `kosif-atlas/skills/2657-figures/10114-svg-primitives`

#### EXPL-05 · عكس المخطط للعربية · Mirrored RTL diagrams · 📄 موصوف / documented only
- **ماذا / what:** العقدة الأولى يمينًا والأسهم تشير يسارًا ورؤوسها معكوسة، والمعرفات اللاتينية معزولة. — First node on the right, arrows point left, mirrored markers, Latin ids isolated.
- **متى أستخدمها / when:** كل مخطط بنص عربي — every diagram with Arabic labels.
- **كيف / how:** mirror x positions (x' = W − x) or lay out with direction rtl; flip arrow marker paths; flows read right → left and top → bottom; Latin/code labels wrapped in dir="ltr" + unicode-bidi:isolate; stage-tracker pills ordered right → left (EXPL-26).
- **الدليل / proof:** `kosif-tool/playbooks/diagrams.md:18` · `kosif-tool/playbooks/diagrams.md:71`

#### EXPL-06 · ألوان دلالية للأدوار · Semantic role colours · 📄 موصوف / documented only
- **ماذا / what:** اللون يرمّز نوع المكون، والمستطيلات المتقطعة تحدد الحدود. — Colour encodes component type; dashed rectangles mark boundaries.
- **متى أستخدمها / when:** مخططات بنية تقنية — system architecture diagrams.
- **كيف / how:** dark theme: frontend cyan #22d3ee, backend emerald #34d399, data violet #a78bfa, cloud amber #fbbf24, security rose #fb7185, message bus orange #fb923c, external slate #94a3b8; regions dashed 8,4 amber rx 12, security groups dashed 4,4; light/print theme via plain divs. Role colours (source / processing / storage / external) via Mermaid classDef with measured contrast. Ideas only from a copyleft-declared folder — re-author, do not copy files. **أرقام / params:** dash 8,4 / 4,4; rx 12.
- **رخصة / license:** source folder declares WTFPL (copyleft-flagged in the atlas) — use the idea, not the files
- **الدليل / proof:** `kosif-atlas/skills/x4919-visual-gen/x20317-architecture-diagram/SKILL.md` · `100-superskills/skills/diagrams-mermaid-architecture/SKILL.md:24`

#### EXPL-07 · إطار الشرح الأحادي · Learning-mono explainer frame · 📄 موصوف / documented only
- **ماذا / what:** إطارات دراسة 16:9 بالأبيض والأسود: عنوان أعلى اليسار (يمين للعربية)، صناديق بخط 1–2 بكسل، أسهم رفيعة، ولون تأكيد أحمر واحد أقل من 5%. — Minimal black-and-white study frames with one red accent under 5%.
- **متى أستخدمها / when:** دروس جادة وشروح أكاديمية — serious lessons.
- **كيف / how:** white ground, title #111111 (≤40 chars), body #333333, annotations #767676, unfilled 1–2 px boxes, dashed grey grouping, thin arrows with small triangular heads and 2–4-word labels, accent #D93025 (second accent #1A73E8 only when needed), margins 5–7%, 3–5 points; build natively in SVG/HTML so text is exact; arrows and labels draw on with stagger; narration carries the long explanation. **أرقام / params:** accent < 5%; margin 5–7%.
- **الدليل / proof:** `kosif-atlas/skills/1094-akbun-draw/2418-akbun-draw-learning-mono/SKILL.md`

#### EXPL-08 · حدود الأيقونات المختصرة · Closure limits for minimal icons · 📄 موصوف / documented only
- **ماذا / what:** الأشكال الضمنية تتوقف عن العمل تحت 24 بكسل تقريبًا، وللجمهور المبتدئ وفي المعلومات الحساسة. — Implied shapes fail below ~24 px, for novices and in high-stakes info.
- **متى أستخدمها / when:** أيقونات صغيرة في فيديو عمودي — small icons in vertical video.
- **كيف / how:** pair minimal icons with labels, make critical marks explicit, render a contact sheet at the final 9:16 scale and inspect at phone size. **أرقام / params:** < ~24 px.
- **الدليل / proof:** `kosif-atlas/skills/1503-universal-design-principles/3811-closure-completion-cost/SKILL.md`

#### EXPL-09 · توليد أيقونات بخلفية شفافة · Transparent icon generation · 🔑 مفتاح أو خدمة / needs key
- **ماذا / what:** أيقونات مسطحة بقناة ألفا للشروح، بلوحة ألوان مشتركة. — Flat alpha icons themed by a shared palette.
- **متى أستخدمها / when:** حين لا توجد أيقونة SVG مناسبة — when no SVG icon fits.
- **كيف / how:** request a transparent background from the image model (key needed) with a template 'a flat icon of a {item}', 1024 px square; if it returns opaque, remove near-white by threshold in Pillow or use rembg (BiRefNet, pip install rembg onnxruntime); prefer drawing simple icons as SVG strokes (DRAW-13) when possible. **أرقام / params:** 1024 px; threshold or BiRefNet.
- **الدليل / proof:** `kosif-atlas/skills/2657-figures/10115-transparent-icons`

## بناء المخططات بالكود — Building diagrams in code

_أدوات تحوّل النص أو البيانات إلى مخطط قابل للتحريك._

#### EXPL-10 · مخططات SVG برمجية بالملليمتر · Programmatic SVG schematics · 📄 موصوف / documented only
- **ماذا / what:** صناديق تتسع لنصها، أسهم تلتصق بحافة الهدف ورأسها يتبع مماس المنحنى، ووحدات ملليمتر، وترتيب طبقات ثابت. — Auto-fit boxes, edge-snapped tangent-correct arrows, mm units and fixed layer order.
- **متى أستخدمها / when:** مخططات دقيقة قابلة للطباعة والتحريك — precise schematics.
- **كيف / how:** width/height in mm with an equal viewBox so coordinates and font-size are mm (font pt × 25.4/72, 7 pt = 2.47 mm); LabeledBox = measured text bbox + 2 mm padding (fontTools advances, or canvas measureText — browser measuring for Arabic shaping); Arrow.connect snaps to box edges, modes straight / cubic with perpendicular bow / orthogonal / waypoints, marker orient=auto; layers registered in paint order; save SVG (+ PNG via cairosvg); the same ideas are short to hand-write in JS for animation. **أرقام / params:** padding 2 mm; marker 3 mm; 7 pt.
- **رخصة / license:** BSD-3-Clause (atlas source)
- **الدليل / proof:** `kosif-atlas/skills/2657-figures/10114-svg-primitives/SKILL.md` · `kosif-atlas/skills/2657-figures/10113-svg-figure`

#### EXPL-11 · مخططات Mermaid من نص · Mermaid text-to-diagram · 📦 بأمر تثبيت / one install
- **ماذا / what:** مخططات انسيابية وتسلسلية وفئات وحالات وعلاقات وجانت من نص، والرندر نفسه يتحقق من الصياغة. — Flowchart, sequence, class, state, ER, Gantt from text; rendering validates syntax.
- **متى أستخدمها / when:** مخطط سريع يُبنى من وصف — a quick diagram from a description.
- **كيف / how:** mmdc -i x.mmd -o x.svg -t dark|forest|neutral -b transparent; one direction (TB or LR, RL for Arabic), ≤12 nodes, every arrow labelled, readable in B/W; then animate the SVG nodes in reading order (stagger opacity, draw-on edges with DRAW-01); fall back to hand SVG when mmdc is absent. **أرقام / params:** ≤12 nodes; themes default/dark/forest/neutral.
- **تثبيت / install:** `npm i -g @mermaid-js/mermaid-cli`
- **الدليل / proof:** `kosif-atlas/skills/1245-mermaid-cli/2925-mermaid-cli` · `100-superskills/skills/diagrams-mermaid-architecture/SKILL.md:21`

#### EXPL-12 · مخططات D2 · D2 declarative diagrams · 📄 موصوف / documented only
- **ماذا / what:** لغة مخططات تصريحية بتخطيط dagre أو elk وسمات كثيرة، تخرج SVG وPNG وPDF وGIF متحرك. — Declarative diagrams with dagre/elk layouts and many themes.
- **متى أستخدمها / when:** مخططات بنية كبيرة — large architecture diagrams.
- **كيف / how:** d2 --theme N --layout elk in.d2 out.svg (tala layout is paid); the d2 binary is not installed here and its installer host is unverified — prefer Mermaid or hand SVG unless the user supplies d2. **أرقام / params:** layouts dagre / elk / tala (paid).
- **الدليل / proof:** `kosif-atlas/skills/2173-tools-plugin/7914-d2-diagrams`

#### EXPL-13 · سبورة Excalidraw ولوحات JSON Canvas · Excalidraw & JSON Canvas boards · 📦 بأمر تثبيت / one install
- **ماذا / what:** مشاهد .excalidraw بأشكال وأسهم ونص حر بمظهر يدوي قابل للتحرير، ولوحات JSON Canvas مكانية تصلح مصدرًا لستوري بورد أو خريطة ذهنية. — Editable whiteboard scenes and spatial boards as storyboard sources.
- **متى أستخدمها / when:** شرح بإحساس سبورة أو خريطة ذهنية — whiteboard-feel explainers, mind maps.
- **كيف / how:** write elements per schema (rectangles, ellipses, diamonds, arrows, lines, text; roughness 1, fontFamily 1 hand / 3 mono); render through @excalidraw/excalidraw exportToSvg in headless Chromium, then draw strokes on (DRAW-01/27); large diagrams section by section. JSON Canvas: nodes {text|file|link|group, x, y, width, height} and edges {fromSide, toSide, arrows} → a script turns them into animated SVG with camera moves. **أرقام / params:** roughness 1; fontFamily 1/3.
- **تثبيت / install:** `npm i @excalidraw/excalidraw`
- **الدليل / proof:** `kosif-atlas/skills/2790-work/11181-draw-excalidraw` · `kosif-atlas/skills/2966-pwdev-excalidraw/12488-excalidraw` · `kosif-atlas/skills/3013-obsidian-second-brain/12869-json-canvas`

#### EXPL-14 · شبكة مفاهيم بقوة الجذب · Force-directed concept graph · 📦 بأمر تثبيت / one install
- **ماذا / what:** مخطط ذهني (جذر، فروع، أبناء، ألوان) يُرسم كشبكة قوى تستقر متحركة. — A mind-map outline rendered as an animated force graph.
- **متى أستخدمها / when:** خرائط معرفة، علاقات كثيرة — knowledge maps.
- **كيف / how:** convert the JSON outline to nodes/links; run d3-force OFFLINE for N ticks (seeded) and store positions per tick, then animate nodes settling from the centre in branch order by indexing the stored ticks with t (never a live simulation during render); colour per top-level branch; depth ≤6. **أرقام / params:** depth ≤6; seeded ticks.
- **تثبيت / install:** `npm i d3-force`
- **الدليل / proof:** `kosif-atlas/skills/30-learning/39-forcegraph-exporter/SKILL.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10326-node-link-and-diagram-layout/references/algorithm-selection.md`

#### EXPL-15 · خريطة الكيان في المنتصف · Entity node map with flow edges · 🟢 جاهز / ready
- **ماذا / what:** قالب يرسم كيانًا في المنتصف وما يغذيه من جهة وما ينتجه من الأخرى كعقد تحمل أرقامًا فوق شبكة نقاط، بخطوط تدفق متحركة. — An entity with inputs on one side and outputs on the other as number-carrying nodes over a dot grid.
- **متى أستخدمها / when:** شرح نظام محاسبي أو عملية أعمال — business/process systems.
- **كيف / how:** SK.studio.mount(root, spec) → {paint, focus, focused}; nodes 150 px × ≥80 px positioned translate(−50%, −50%), hover scale 1.025; edges as SVG lines classed in / draft / out / note; inputs dasharray 7 6 (warn colour), drafts 3 5 (violet), outputs solid; @keyframes flow to stroke-dashoffset −26 over 1.6 s linear; vector-effect non-scaling-stroke; dot grid radial-gradient 1 px every 24 px. **أرقام / params:** dash 7/6, 3/5; 1.6 s; grid 24 px.
- **الدليل / proof:** `kosif-earth-ci-fork/ui/components/studio.js` · `kosif-earth-ci-fork/ui/components/studio.css:25`

## حركة المخطط — Diagram motion recipes

_وصفات موقوتة لبناء المخطط وتحريكه._

#### EXPL-16 · عملية من ثلاث خطوات · Three-step process recipe · 📄 موصوف / documented only
- **ماذا / what:** سلسلة عقدة-رابط-عقدة مع خفوت السابق ونبضة بيانات ختامية. — Node-edge-node chain with dimming and a final data pulse.
- **متى أستخدمها / when:** «كيف يعمل» في 4 ثوانٍ — 'how it works' in 4 s.
- **كيف / how:** nodes pop at 0 / 900 / 1800 ms (scale .85 → 1, spring damping 14 stiffness 160, ~300 ms + 150 ms fade); edges draw 300–900 and 1200–1800 ms at 900–1200 px/s ease-in-out cubic with the arrowhead in the last 80 ms (DRAW-05); hold 2100–3600 ms with a data pulse; previous nodes dim to 70%. **أرقام / params:** 0/900/1800 ms; spring 14/160.
- **الدليل / proof:** `kosif-tool/playbooks/diagrams.md:37` · `kosif-tool/playbooks/diagrams.md:27`

#### EXPL-17 · نبضة بيانات على الرابط · Data pulse along edges · 📄 موصوف / documented only
- **ماذا / what:** نقطة أو نقاط متوهجة تجري على مسار الرابط مرارًا أثناء وصف التدفق. — Dots travel the edge path repeatedly while the flow is described.
- **متى أستخدمها / when:** تدفق بيانات، إشارة، طلب شبكة — data flow, signals, requests.
- **كيف / how:** dot 10–14 px at getPointAtLength(p·L), 600–900 ms in-out, 400 ms gaps; variants: 3–5 glowing dots offset along a dashed quadratic arc (dash 4/6, r 4, ~1.5 s); orange dot on the active orthogonal wire with an orange ✗ on an invalid route (draw 500 ms, travel 800 ms); sine-wave segments scrolling 60 px/s between boxes for signal chains; glowing route to the chosen target (600 ms). **أرقام / params:** dot 10–14 px; 600–900 ms; gaps 400 ms.
- **الدليل / proof:** `kosif-tool/playbooks/diagrams.md:29` · `kosif-tool/styles/isometric` · `kosif-tool/styles/plotter` · `kosif-tool/styles/pm-blueoctopusai-dd17bd`

#### EXPL-18 · خطوط تدفق متحركة · Marching-dash flow edges · 🟢 جاهز / ready
- **ماذا / what:** شرطات تسير على الخط لتبيّن التدفق: تيار، ماء، طاقة، بيانات. — Marching dashes show flow along a line.
- **متى أستخدمها / when:** أنابيب، كهرباء، حرارة، طلبات — pipes, current, heat, requests.
- **كيف / how:** MOTION.flowDash(tl, path, at, dur, {pattern:'28 22', cycles:6}) linear; seek-safe CSS/JS: dashoffset = −speed·t; water-cycle heat arrows #FF9E2C 7 px dasharray '20 18' dashoffset −140t with fade windows, sun rays rotating 18°/s and pulsing 1 + .06·sin(4πt); colour-code power / data / heat. **أرقام / params:** '28 22' × 6; '20 18' at −140 px/s.
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:247` · `kosif-one/projects/water-cycle-animation/index.html` · `kosif-earth-ci-fork/ui/components/studio.css:25`

#### EXPL-19 · محور وأذرع ومدارات · Hub-and-spoke, constellations & orbits · 📦 بأمر تثبيت / one install
- **ماذا / what:** كيان مركزي تُرسم منه خطوط إلى عقد حوله بالتتابع، أو بطاقات تتجمع على إهليلج، أو أقمار تستقر حول نواة. — A central hub drawing connectors to surrounding nodes, chips on an ellipse, satellites settling around a nucleus.
- **متى أستخدمها / when:** تكاملات منتج، فريق، منظومة — product integrations, ecosystems.
- **كيف / how:** lines draw from centre outward 300–600 ms with 50–150 ms stagger, then nodes fade in and count; hub glow blur 30–40 px; travelling dots on dashed spokes; gooey arms (6–7, stagger 80 ms); hero card centre with ~10 satellites on an ellipse and tag pills on the lines; reverse version: labels on a top arc stroke to the centre, then the hub logo pops with a ring. HyperFrames components: constellation-hub (nodes light in narration order), radial-surround (chips converge inward), locked-nucleus-orbit (3–6 satellites). **أرقام / params:** draw 300–600 ms; stagger 50–150 ms.
- **تثبيت / install:** `npx hyperframes add constellation-hub`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/constellation-hub/constellation-hub.html` · `kosif-one/vendor/hyperframes/registry/components/radial-surround/radial-surround.html` · `kosif-tool/styles/pm-kmasiff-cc72cb` · `kosif-tool/styles/pm-agonaliu-466a8f`

#### EXPL-20 · التفرع إلى عدة · Fan-out branches & tree cascades · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** منتج متوهج تتفرع منه منحنيات إلى منصات، أو حسابات تقفز من مركز، أو شجرة عقد متداخلة تظهر واحدة تلو الأخرى بروابط قائمة. — One-to-many curves, springing avatars, or nested tree cascades with elbow connectors.
- **متى أستخدمها / when:** «من مكان واحد إلى كل مكان»، بنية ملفات — one-to-many stories, file/AST trees.
- **كيف / how:** bezier curves draw 400–500 ms with 150 ms stagger to stacked cards, travelling light dots (700 ms) and signal-bar meters filling; N = 5 avatars spring out along straight lines (120 ms stagger, overshoot 1.1); AST cascade: indented boxed nodes (document > heading > paragraph > codeBlock) appear every 120 ms with elbow connectors and key:value mono metadata; hand-drawn branches from an address chip to N boxes (0.8 s each) with the focus box circled in yellow. **أرقام / params:** 400–500 ms; stagger 120–150 ms.
- **الدليل / proof:** `kosif-tool/styles/pm-ceowinkz-7c776b` · `kosif-tool/styles/pm-anthonyriera-9b1b2a` · `kosif-tool/styles/pm-kyonax-on-tech-aabc1d` · `kosif-tool/styles/pm-elliot-garreffa-f334bc`

#### EXPL-21 · مخطط يُبنى مع الصوت · Voice-synced diagram build · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** كل سهم وأيقونة وتسمية يظهر ويُرسم عند الطابع الزمني لكلمته المنطوقة. — Each labelled arrow/icon draws at its word timestamp.
- **متى أستخدمها / when:** شرح بتعليق صوتي — narrated explainers.
- **كيف / how:** map each diagram element to a keyword in words.json (faster-whisper word timestamps); start its draw-on 60 ms before the word; never front-load more than ~25% (EASE-44); hold the full diagram for a final 1–2 s read. **أرقام / params:** word − 60 ms.
- **الدليل / proof:** `kosif-tool/styles/pm-sudo-kiran-6609ed` · `kosif-tool/playbooks/audio-sync.md`

#### EXPL-22 · التكبير على مكوّن وقبل/بعد · Zoom into component & before/after diagram · 📄 موصوف / documented only
- **ماذا / what:** ثبات على النظام كله، الكاميرا تذهب لعقدة واحدة فتنفتح مخططًا فرعيًا؛ أو نسخة «بعد» تعيد رسم الروابط المتغيرة فقط بلون التأكيد. — Hold the system, camera to one node that opens into a sub-diagram; or redraw only the changed edges.
- **متى أستخدمها / when:** أنظمة متداخلة، تحسينات — nested systems, improvements.
- **كيف / how:** 2 s hold; scale 1.5 (zoom ≤1.8) in 900 ms then a 300 ms crossfade into the sub-diagram; camera pans 700–1000 ms cubic-bezier(.65,0,.35,1); before/after: duplicate the diagram and redraw only changed edges in the accent. **أرقام / params:** hold 2 s; ×1.5 / 900 ms; xfade 300 ms.
- **الدليل / proof:** `kosif-tool/playbooks/diagrams.md:48` · `kosif-tool/playbooks/diagrams.md:52`

#### EXPL-23 · الخط الزمني برأس تشغيل · Timeline with playhead · 📄 موصوف / documented only
- **ماذا / what:** رأس تشغيل بسرعة ثابتة، علامات تقفز عند وصوله والتسميات بعدها، وشريط الحقبة الحالية. — Constant-speed playhead; markers pop on arrival, labels after.
- **متى أستخدمها / when:** تاريخ، سيرة، مراحل مشروع — history, biographies, project phases.
- **كيف / how:** axis draws 600 ms; marker pop 200 ms; label +120 ms; current era band; one continuous lateral camera along the track slowing to 30% speed near dense clusters (cubic-bezier(.4,0,.2,1) per segment); milestone cards rise 400 ms / 40 px on a spring (damping 20) with a 1–1.5 s micro-animation; process timeline with doodle icons popping 200 ms back.out. **أرقام / params:** axis 600 / pop 200 / label +120 ms.
- **الدليل / proof:** `kosif-tool/playbooks/diagrams.md:31` · `kosif-tool/styles/pm-kloss-xyz-fe0c31/BRIEF.md` · `kosif-tool/styles/pm-lemomo-ai-0d9cff`

#### EXPL-24 · مسار قرار ومخطط انسيابي · Decision path & flowchart · 📦 بأمر تثبيت / one install
- **ماذا / what:** سؤال، فرعان ملونان، ومثال يسير إلى نتيجته؛ أو شجرة قرار بملاحظات لاصقة ومؤشر يتفاعل. — A question, two coloured branches, an example travelling to its outcome.
- **متى أستخدمها / when:** «ماذا أفعل لو…»، استكشاف أخطاء — decision guides, troubleshooting.
- **كيف / how:** MG-087: 0–2 s question, 2–5 branches, 5–8 example path, 8–10 result, chosen branch highlighted (high-stakes advice needs expert review); failover: request pill → diamond, red failed branch then green success branch draws in 400 ms; faded options with a line to the highlighted pill. HyperFrames blocks flowchart (12 s, 1920×1080) and flowchart-vertical (1440×2560) with sticky-note nodes and typing correction. **أرقام / params:** 10 s; branch draw 400 ms.
- **تثبيت / install:** `npx hyperframes add flowchart`
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-explainers.md` · `kosif-one/vendor/hyperframes/registry/blocks/flowchart/flowchart.html` · `kosif-tool/styles/pm-misbahsy-80eaec`

#### EXPL-25 · دورة ورمز ينتقل · Cycle diagram, travelling token & loop arrow · 🟢 جاهز / ready
- **ماذا / what:** أربع أيقونات على دائرة وأسهم تنمو بينها بالترتيب، وكرة تنقل الفكرة بين المحطات وتغير لونها، وسهم دائري ختامي يقول «وتتكرر». — Icons on a circle with arrows growing in order, a travelling token, and a closing loop arrow.
- **متى أستخدمها / when:** دورات طبيعية، دورة حياة منتج — natural cycles, lifecycles.
- **كيف / how:** MG-081: 0–1 s title, 1–7 stages, 7–10 full cycle (direction readable muted); MG-083: ball on a Bezier with stops, colour change only when it means something; water-cycle recap: big orange loop pathLength=1 drawn 8.9–9.8 s eased, marker-end attached only when progress > .98, #FF7A00 9 px. **أرقام / params:** 10 s; loop 8.9–9.8 s.
- **الدليل / proof:** `kosif-one/projects/water-cycle-animation/index.html` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-explainers.md`

#### EXPL-26 · شريط المراحل ومؤشر الخطوات · Stage tracker pills & steppers · 🟢 جاهز / ready
- **ماذا / what:** شريط حبوب مرقمة من اليمين يمتلئ فيه الحالي بالبرتقالي، ودوائر خطوات مترابطة، وعقد رحلة تقفز بالتتابع. — Numbered RTL stage pills, linked step circles and journey nodes popping in sequence.
- **متى أستخدمها / when:** شروح بمراحل، إجراءات — staged explainers, procedures.
- **كيف / how:** water cycle: 4 pills 260×70 rx 35 at y 968, x = 1395 − i·290, fill mix(#FFFFFF, #FF7A00, on), text mix(#0B2545, #FFFFFF, on), all light together in the recap; audit-pro journey: 5 nodes 36 px pop 260 ms spring (translate 7 px + scale .88 → 1) with delays 180–360 ms (45 ms step) after the line starts — done = teal + check, current = violet with 4 px halo; trace chain cards 260 ms at 50 ms steps with 8×2 px connectors scaling from the right; numbered step cards (yellow badge, outline icon) 1.2–1.5 s apart; 4-segment top bar filling with big mono 01–04. **أرقام / params:** pills 260×70; pop 260 ms; 45–50 ms steps.
- **الدليل / proof:** `kosif-one/projects/water-cycle-animation/index.html` · `kosif-audit-pro/app/globals.css:998` · `kosif-audit-pro/app/globals.css:2191`

#### EXPL-27 · خطأ ثم تصحيح · Mistake then correction · 📄 موصوف / documented only
- **ماذا / what:** مثال خاطئ يتجمد ويُحاط بدائرة وينزاح، ثم تظهر النسخة الصحيحة؛ أو قاعدة خاطئة تُشطب وبجانبها الصحيحة بعلامة صح. — A wrong example freezes, is ringed and slides aside; the correct version appears.
- **متى أستخدمها / when:** تصحيح مفاهيم شائعة — correcting common misconceptions.
- **كيف / how:** MG-084: 0–2 s example, 2–3 alert, 3–6 fix, 6–8 summary (freeze frame, masks, sequential comparison; illustrate dangerous actions instead of filming them); strike: red line draws over the wrong rule in 250 ms, then the right one with a drawn check in 300 ms (DRAW-19/21). **أرقام / params:** 8 s; strike 250 / check 300 ms.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-explainers.md` · `kosif-tool/styles/pm-chatgptastra-0d95c7`

#### EXPL-28 · مقارنة سرعة عادلة · Fair speed comparison · 📄 موصوف / documented only
- **ماذا / what:** جسمان يقطعان المسافة نفسها بجانب ساعة ظاهرة، وأي اختلاف في الزمن أو المسافة يُذكر. — Two objects cover the same distance beside a visible clock.
- **متى أستخدمها / when:** «أيهما أسرع»، أداء — performance comparisons.
- **كيف / how:** MG-088: 0–1 s conditions, 1–6 motion, 6–8 result; identical paths and fixed distances with on-screen timers; performance bars racing for code (EXPL-42). **أرقام / params:** 8 s.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-explainers.md`

#### EXPL-29 · تسميات بخطوط قائدة · Leader-line callouts (2D & 3D) · 🟢 جاهز / ready
- **ماذا / what:** نقطة وخط وتسمية تشير إلى جزء من واجهة أو مجسم، مع قياس حي يتغير مع الزمن. — Dot + leader line + label anchored to a UI point or projected 3D point, with live measurements.
- **متى أستخدمها / when:** شرح أجزاء منتج أو واجهة — explaining product or UI parts.
- **كيف / how:** 2D: thin amber elbow lines from page points to mono labels at the frame sides, draw-on 300 ms each, stagger 80 ms, small square end-cap; feature labels: 1 px line 250 ms, text +150 ms, 2–4 words, shadow blur 40 px at 8%. 3D: h.addCallout({anchor, label:'THE EAR · الأذن', title, text, side, radius, measure: t → '0.42 m'}) projects a dashed ring (4.5% H) to screen with a leader (dx 9% W, dy −14% H) and a card 14–22% W; callout.show 0..1 per frame. Corner crop brackets (L-marks, arm 12 px, 300 ms ease-out) and dimension arrows with tiny mono labels. **أرقام / params:** draw 250–300 ms; stagger 80 ms.
- **الدليل / proof:** `kosif-studio/motion/kit/lab-kit.js` · `100-superskills/skills/kosif-montage-motion/scripts/kit/lab-kit.js:233` · `kosif-tool/styles/pm-kyonax-on-tech-aabc1d` · `kosif-tool/styles/pm-techyoutbe-945b56/BRIEF.md`

#### EXPL-30 · طبقات شفافة إيزومترية · Isometric translucent layer stack · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** ألواح مدورة مائلة بزاوية إيزومترية تتدرج من شفافة إلى زرقاء مصمتة، واللوح العلوي مرفوع بإطار متقطع وتسميات بخطوط قائدة. — Rounded plates in isometric tilt stacked with an opacity ramp; the top plate lifts.
- **متى أستخدمها / when:** طبقات برمجيات، مكدسات — software layers, stacks.
- **كيف / how:** CSS transform rotateX(55deg) rotateZ(−45deg), 6–7 plates offset 18 px, light → solid blue #1f7bf2 with a glow below; top plate lifted with a dashed outline; leader lines draw right then mono labels fade in. **أرقام / params:** 6–7 plates; offset 18 px.
- **الدليل / proof:** `kosif-tool/styles/pm-ddryo-loos-300829`

#### EXPL-31 · التضخيم والمقارنة بالمقياس · Exaggerated scale & size comparison · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** ضخّم خاصية دقيقة رأسيًا ×N مع تسمية «مُضخّم ×9.6»، أو صفّ كرات أحجامها جذر القيمة. — Exaggerate a subtle property ×N with an honest label, or size spheres by √value.
- **متى أستخدمها / when:** فروقات صغيرة جدًا أو كبيرة جدًا — tiny or huge differences.
- **كيف / how:** scale ×5–10 with a teal 40% tint and the label 'shown ×N' plus callout tags; spheres sized by sqrt(value) with a minimum clamp for tiny values, staggered pop-in right → left (250 ms) with arrows and % captions — always state the exaggeration on screen. **أرقام / params:** ×5–10; sqrt sizing; stagger 250 ms.
- **الدليل / proof:** `kosif-tool/styles/pm-blueoctopusai-dd17bd` · `kosif-tool/styles/infographic`

## الكود على الشاشة — Code on screen

_كود حقيقي مقروء يُكتب ويُبرز ويتغير._

#### EXPL-32 · طباعة الكود على الشاشة · On-screen code typography · 📄 موصوف / documented only
- **ماذا / what:** خط أحادي العرض حقيقي، أسطر محدودة، سمة ألوان واحدة، إبراز 1–3 أسطر، وكود صحيح معقول. — Real monospace, limited lines, one syntax theme, 1–3 highlighted lines, plausible correct code.
- **متى أستخدمها / when:** كل مشهد كود — every code scene.
- **كيف / how:** mono 28–40 px at 1080 width, ≤14 lines, line-height 1.6, tinted background; JetBrains Mono / Geist Mono / IBM Plex Mono; code is always LTR, even inside an Arabic film (wrap in dir="ltr"); render with pre-tokenised spans so text is exact (never an image model). **أرقام / params:** 28–40 px; ≤14 lines; lh 1.6.
- **الدليل / proof:** `kosif-tool/playbooks/code.md:15` · `kosif-atlas/skills/1503-universal-design-principles/3825-legibility-contrast-and-spacing/SKILL.md`

#### EXPL-33 · كتابة بتذبذب مزروع · Seeded typing animation · 📦 بأمر تثبيت / one install
- **ماذا / what:** كتابة حرفًا حرفًا بتذبذب مزروع ووقفات بعد علامات الترقيم ومؤشر يومض، والكود الطويل يُلصق كتلة. — Per-character typing with seeded jitter, punctuation pauses and a blinking caret.
- **متى أستخدمها / when:** أوامر وكود قصير — commands and short code.
- **كيف / how:** per-char delay = (1/cps)·(0.8 + random(`k${i}`)·0.4) + 0.3 s after [.,;:]; 25–45 cps (default 35); caret ▍ 530 ms; long code pasted as a block with a 200 ms fade; Arabic never per letter — whole words or a mask (ARAB-01). Remotion Typed component in the playbook; the canvas port below needs nothing installed. **أرقام / params:** 35 cps ±20%; +250–400 ms punctuation; caret 530 ms.

```js
// seek-safe typed text: precompute cumulative times once, then index by t
function typedTimes(text, cps = 35, seed = 7) {
  const r = rng(seed), out = []; let acc = 0;
  for (const ch of text) { acc += (1 / cps) * (0.8 + r() * 0.4) + ('.,;:'.includes(ch) ? 0.3 : 0); out.push(acc); }
  return out;                                   // shown(t) = count of times ≤ t − start
}
```

- **تثبيت / install:** `cd kosif-tool/starters/remotion && npm i`
- **رخصة / license:** Remotion company license
- **الدليل / proof:** `kosif-tool/playbooks/code.md:25` · `kosif-tool/playbooks/code.md:55` · `kosif-tool/starters/html-canvas/timeline.js`

#### EXPL-34 · جلسة الطرفية · Terminal session scene · 📄 موصوف / documented only
- **ماذا / what:** نافذة طرفية تكبر، أمر يُكتب، وميض Enter، مخرجات على دفعات، وإبراز النجاح مع دفع كاميرا. — Terminal scales in, command types, enter flash, output in blocks, success highlight with a push.
- **متى أستخدمها / when:** أدوات المطورين وافتتاحيات تقنية — dev tools and tech openers.
- **كيف / how:** 0–300 ms scale from 0.96; 300–1300 ms type at 35 cps; 1300–1600 ms caret/enter flash; 1600–2400 ms 3 output blocks; 2400–3000 ms success highlight + 3% push. Openers: '$ command' typed 30–50 ms/char with a block cursor on black; compile rows whose block bars fill (300 ms each, rows 150 ms apart); log lines every 120 ms with the last one green; colour-coded event log (6 rows, fixed char widths, new rows push old up); terminal left 60% + definition card right. Real sessions can be captured as an asciinema .cast and replayed (external tools). **أرقام / params:** 0/300/1300/1600/2400/3000 ms.
- **الدليل / proof:** `kosif-tool/playbooks/code.md:35` · `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md` · `kosif-tool/styles/pm-madhav-xo-f97f20`

#### EXPL-35 · إبراز السطر والتمرير والخطأ · Line highlight, scroll & error sweep · 📄 موصوف / documented only
- **ماذا / what:** شريط ينزلق خلف السطر المهم والباقي يخفت، والتمرير بأسطر كاملة، وشريط أحمر مع خط متموج للخطأ. — A band behind the key line with others dimmed, whole-line scrolling, and a red error sweep.
- **متى أستخدمها / when:** شرح سطر بعينه — explaining a specific line.
- **كيف / how:** highlight band 250 ms ease-out cubic, others to 50%; scroll 200–300 ms per line ease-in-out (never fractional lines); error: red band scaleX 0 → 1 + squiggle draw 0.6 s; prompt card: cream mono typed ~30 ms/char, then red rectangles wipe behind faulty words (250 ms each, 300 ms apart) and the text turns light; file tree: a highlight bar steps rows. **أرقام / params:** 250 ms; 50% dim; 200–300 ms/line.
- **الدليل / proof:** `kosif-tool/playbooks/code.md:26` · `kosif-tool/playbooks/code.md:27` · `kosif-tool/styles/pm-henkvaness-0e06af`

#### EXPL-36 · كشف الفرق · Diff reveal · 📄 موصوف / documented only
- **ماذا / what:** الأسطر المحذوفة تنطوي بالأحمر، المضافة تتمدد بالأخضر، والثابتة تنزلق. — Removed lines collapse red, added expand green, unchanged slide.
- **متى أستخدمها / when:** شرح تغيير في الكود — explaining a code change.
- **كيف / how:** removed 250 ms, added 300 ms, staggered; exactly 2 states; variant: green wipe over a red diff, test dots fill one by one, bracket burst on pass. **أرقام / params:** 250 / 300 ms.
- **الدليل / proof:** `kosif-tool/playbooks/code.md:49` · `kosif-tool/styles/pm-jake11moran-a269c4/BRIEF.md`

#### EXPL-37 · نافذة كود مشروحة · Annotated code-window figure · 📄 موصوف / documented only
- **ماذا / what:** نافذة محرر داكنة مدورة بثلاث نقاط، ألوان صياغة محددة، وحتى 3 إبرازات بإطار أخضر وأسهم صفراء يدوية إلى ملاحظات. — A dark rounded editor window with ≤3 green-box highlights and hand-drawn yellow arrows.
- **متى أستخدمها / when:** شرح مقتطف كود في ريل — a code snippet in a reel.
- **كيف / how:** window #2A2622 with three traffic-light dots; keys #E06C9F, strings #E5A86B, numbers #A78BFA, punctuation light grey; highlights as green outline boxes #7EE787 with yellow curved arrows to callouts; 4:3, 4–12 lines, 60/35 split; animate window in → lines reveal → box draws → arrow draws → callout pops; Prism/highlight.js from a CDN or pre-tokenised spans. **أرقام / params:** ≤3 callouts; 4–12 lines.
- **الدليل / proof:** `kosif-atlas/skills/1094-akbun-draw/2426-akbun-generateimage-code/SKILL.md`

#### EXPL-38 · كود ومعاينة حية · Code + live preview split · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** لوح يكتب الكود بألوانه وأرقام أسطره، ولوح بجانبه يُظهر النتيجة تتفاعل لحظة اكتمال السطر. — One pane types code; the other shows the result reacting as each line completes.
- **متى أستخدمها / when:** دروس برمجة، ألعاب، رسم بالكود — coding lessons, creative coding.
- **كيف / how:** ~25 chars/s, caret blink 500 ms; the result pane reads the same t (the sprite jumps when the jump() line completes); test checklist ticks below; triptych variant: framed canvas with ruler and red playhead + mono code with orange literals + serif formula, the playhead time ('t = 1.97 s') drives both the shapes and the highlighted code line. **أرقام / params:** ~25 cps; caret 500 ms.
- **الدليل / proof:** `kosif-tool/styles/pm-ibrahimwasim240-809370` · `kosif-tool/styles/plotter`

#### EXPL-39 · كود مجرد ورقائق · Abstract code pills & token chips · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** الكود كأشرطة ملونة مجردة، أو رقائق رموز بأرقامها، أو سحابة رقائق كود عائمة، أو بطاقة JSON تُكتب. — Code as abstract coloured pills, token chips with ids, a floating chip cloud, or a typed JSON card.
- **متى أستخدمها / when:** ذكاء اصطناعي، نماذج لغوية، APIs — AI, LLMs, APIs.
- **كيف / how:** rows of rounded rects in syntax colours with bracket glyphs; tokens as pastel mono chips (radius 8 px) with grey ids beneath, stagger 90 ms, scale .8 → 1 back-out; 20–30 mono pills drifting 4–8 px sine at .4–.9 opacity around hero text; lime-bordered JSON card with a pink filename tab typed ~30 chars/s and chips drifting 10 px; JSON response lines + '200 OK' pill. **أرقام / params:** chips stagger 90 ms; drift 4–8 px.
- **الدليل / proof:** `kosif-tool/styles/pm-kloss-xyz-15182a` · `kosif-tool/styles/pm-misbahsy-80eaec` · `kosif-tool/styles/pm-techhalla-7acbc2`

#### EXPL-40 · كتل HyperFrames للكود · HyperFrames code blocks · 📦 بأمر تثبيت / one install
- **ماذا / what:** كتل جاهزة لكل حركة كود شائعة: كتابة، فرق، تحول، إبراز، تمرير، لوح ثلاثي، جسيمات، ذوبان بالشيدر، ومحررات وطرفيات. — Ready blocks for every common code motion.
- **متى أستخدمها / when:** فيديو تقني سريع بجودة عالية — fast, polished tech videos.
- **كيف / how:** npx hyperframes add <name>, fill __TOKENS states / __BLOCK params: code-typing (5 s, caret tracks the frontier), code-diff (6 s, 2 states), code-morph (7 s, Shiki-Magic-Move-style token glide), code-highlight (5 s, line 0-based), code-scroll (6 s, line 1-based), code-3d-extrude (8 s WebGL slab), code-particle-assemble (8 s GPU points to glyph pixels), code-shader-dissolve (7 s), code-snippet-apple-terminal-pro (12 s), code-snippet-dark-2026 / dark-modern (11 s VS Code workbench), code-terminal-run (cadence uniform|human), terminal-simulator, grid-card-assemble (capability cards). All 1920×1080, GSAP paused timeline (WebGL ones load three 0.147 from a CDN). **أرقام / params:** 13 blocks; 5–12 s.
- **تثبيت / install:** `npx hyperframes add code-morph`
- **رخصة / license:** Apache-2.0 (GSAP standard no-charge license inside)
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/pr-to-video/references/code-vocabulary.md` · `kosif-one/vendor/hyperframes/registry/blocks/code-morph/code-morph.html` · `kosif-one/vendor/hyperframes/registry/components/code-terminal-run/code-terminal-run.html` · `kosif-one/vendor/hyperframes/registry/blocks/code-3d-extrude/code-3d-extrude.html`

#### EXPL-41 · من طلب دمج أو نص إلى فيديو شرح · PR-to-video & faceless explainer pipelines · 📦 بأمر تثبيت / one install
- **ماذا / what:** طلب دمج على GitHub أو نص حر يتحول إلى فيديو شرح مروي بإطارات مخترعة (طباعة، مخططات، بيانات) وترجمة وانتقالات. — A GitHub PR or free text becomes a narrated explainer of invented frames.
- **متى أستخدمها / when:** سجل تغييرات، إعلان ميزة، شرح 30–90 ث — changelogs, feature reveals, 30–90 s explainers.
- **كيف / how:** PR: node fetch-pr.mjs --pr <ref> (gh) → ingest.mjs (tokens/text/people) → fetch-people-avatars.mjs → frames hook, problem, change, diff, before_after, mechanism, impact, evidence (+N/−M, passing test, benchmark), credits, cta in code-editorial treatments. Faceless: build-frame.mjs --preset → storyboard + SCRIPT.md → audio.mjs (voice; Kokoro local or HeyGen key) → frame-packets → captions → assemble → transitions inject/verify → lint/check/snapshot → render. Arabic voice and captions need the KOSIF voice and caption powers instead of the defaults. **أرقام / params:** sweet spot 30–90 s; ≤~3 min.
- **تثبيت / install:** `npm i -g hyperframes`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/pr-to-video/SKILL.md` · `kosif-one/vendor/hyperframes/skills/faceless-explainer/SKILL.md` · `kosif-one/vendor/hyperframes/skills/pr-to-video/references/story-design.md`

#### EXPL-42 · حرّك ما يفعله الكود · Mechanism beat: animate behaviour, not code · 📄 موصوف / documented only
- **ماذا / what:** أظهر سلوك التشغيل بدل الكود: دورة إعادة المحاولة، حارات الذاكرة المؤقتة، تحول التسلسلي إلى متوازٍ، سباق أداء، فك تشابك الاستدعاءات. — Show runtime behaviour instead of code.
- **متى أستخدمها / when:** شرح تحسين أو إصلاح — explaining an optimisation or fix.
- **كيف / how:** retry/backoff: fire → 500 → growing wait → retry → 200; cache lanes: cold DB vs cached racing; serial lane reshaping into parallel lanes; race bug then fixed flow; performance bars racing; tangled call graph untangling; build as invented SVG/GSAP diagrams; agent tool events (read/search/edit/test/error) as cards snapping on beats (enter (.22,1,.36,1) 420 ms, exit (.4,0,1,1) 260 ms, ≥900 ms on screen, ≤3 stacked) and a call-stack breadcrumb HUD of mono chips (push 200 ms). **أرقام / params:** cards ≥900 ms; ≤3 stacked.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/pr-to-video/references/code-vocabulary.md` · `kosif-tool/styles/pm-jake11moran-a269c4/BRIEF.md` · `kosif-tool/styles/pm-emollick-8661a8`

#### EXPL-43 · شجرة ملفات تتحول إلى أعمدة · Folder tree to bar chart · 💡 فكرة / idea
- **ماذا / what:** أسطر شجرة المجلدات تنبثق أعمدة بعدد أسطر الكود الحقيقي في المستودع. — Nested folder lines extrude into bars of real line counts.
- **متى أستخدمها / when:** «حجم مشروعي» — showing a codebase's size.
- **كيف / how:** count lines per folder from the real repo (cloc or wc -l), draw the tree, then extrude each row into a bar counting up in 600 ms; numbers must come from the repo, never invented. **أرقام / params:** count 600 ms.
- **الدليل / proof:** `kosif-tool/styles/pm-danilowm-d3720d/BRIEF.md`

## الرياضيات والعلوم والهندسة — Math, science & engineering

_أرقام حقيقية تحسب ثم تتحرك._

#### EXPL-44 · معادلة تتكون خطوة خطوة · Equation built step by step (bidi-safe) · 📦 بأمر تثبيت / one install
- **ماذا / what:** المعطيات ثم العملية ثم النتيجة، والحد المشروح ملوّن، والمعادلة لا تنعكس أبدًا داخل جملة عربية. — Givens, operator, result, the explained term tinted; never mirrored inside Arabic.
- **متى أستخدمها / when:** رياضيات وفيزياء — maths and physics.
- **كيف / how:** MG-090: 0–2 s givens, 2–5 operation, 5–8 result, 8–10 read; render with KaTeX (renderToString → HTML/SVG) or pre-rendered SVG; wrap formulas in an LTR isolate (dir="ltr", unicode-bidi:isolate) inside RTL captions; reveal terms by opacity/colour keys with constant spacing between separate layers; define each symbol before use. **أرقام / params:** 10 s.
- **تثبيت / install:** `npm i katex`
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-explainers.md` · `kosif-atlas/skills/994-write-math/2278-write-math/SKILL.md`

#### EXPL-45 · Manim للاشتقاق والنهايات · Manim derivations & limits · 📦 بأمر تثبيت / one install
- **ماذا / what:** اشتقاق جبري بألوان دلالية يتحول سطرًا إلى سطر، قاطع يصير مماسًا، وإطارات حول أجزاء المعادلة بشروح. — Colour-coded derivations, secant-to-tangent limits and boxed annotations.
- **متى أستخدمها / when:** شروح رياضية بأسلوب 3Blue1Brown الأصلي — maths explainers.
- **كيف / how:** MathTex with isolated substrings, cancelling terms red, result green, TransformMatchingTex between lines (line spacing ~12% H, Write ~1.5 s per line); ValueTracker dt 2 → 1 → 0.1 → 0.01 → 0.001 (each ~2–3 s, smooth) with always_redraw secant and DecimalNumber slope readout; SurroundingRectangle around numerator/denominator (stroke 2 px, buff .08) with captions in the matching colour (Create ~0.6 s); render with -qh at the target fps and mux the user's audio separately; Arabic text via Text() with an Arabic font, never inside MathTex. **أرقام / params:** Write 1.5 s; dt → 0.001.
- **تثبيت / install:** `pip install manim`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md` · `kosif-tool/styles/pm-linearuncle-5d2bae`

#### EXPL-46 · دوائر فورييه والجيب · Fourier epicycles & unit-circle sine · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** سلسلة متجهات دوّارة من تحويل فورييه ترسم مسارًا بأثر متوهج، ونقطة على دائرة تُسقط موجة جيبية متحركة. — Rotating DFT vectors draw a path with a glowing trail; a point on a circle projects a scrolling sine.
- **متى أستخدمها / when:** رياضيات جميلة، إشارات — beautiful maths, signals.
- **كيف / how:** sample the target path to N points, DFT → (freq, amp, phase) sorted by amplitude, at time t chain vectors amp·e^{i(freq·2πt/T + phase)} and draw the tip's trail (fading); unit circle: point (cos ωt, sin ωt) with a projection line to a sine scrolling right; all from t, no accumulation. **أرقام / params:** N terms; period T.
- **الدليل / proof:** `kosif-tool/styles/pm-math-files-39c9d0`

#### EXPL-47 · برهان بصري بطيران الخلايا · Cell-flight visual proof · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** كل خلية من مربع تطير إلى موضعها في مربع الوتر بالتتابع، وعداد للخلايا الواصلة، ووهج عند الاكتمال. — Each cell flies to its place in the hypotenuse square, with a counter and completion glow.
- **متى أستخدمها / when:** براهين هندسية، تحويل مساحات — geometric proofs.
- **كيف / how:** lerp source → target cell centre, rotate to the hypotenuse angle, hop = h·sin(πu); 25 cells, stagger ~120 ms, hop 20 px; counter = arrived count; glow square at the end. **أرقام / params:** 25 cells; 120 ms; hop 20 px.
- **الدليل / proof:** `kosif-tool/styles/chalkboard`

#### EXPL-48 · شروح تعلم الآلة · ML explainer devices · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** تمرير نواة على رقم بكسلي إلى خريطة حرارية، أقواس انتباه بين الكلمات، مصفوفة تتفرع كتلًا، شبكة بحواف موجبة وسالبة، وشجرة هرمية بمستويات. — Convolution scans, attention arcs, recursive block matrices, signed graphs and level trees.
- **متى أستخدمها / when:** شرح الذكاء الاصطناعي والفيزياء الإحصائية — AI and statistical-physics explainers.
- **كيف / how:** convolution: pixel digit, kernel square scanning, heatmap output; attention: arcs from one word to others, stroke width = weight; hatched square → 2×2 blocks with cross-hatched diagonal → nested sub-blocks (3 stages, hatch ~8 px); N = 7–8 nodes on a circle with ±-signed edges drawing 80 ms apart; binary tree root-down with dashed coloured level lines and leaf dots last; camera 800 ms easeInOutQuad, ≤5 moves. **أرقام / params:** edge stagger 80 ms; ≤5 camera moves.
- **الدليل / proof:** `kosif-tool/styles/pm-kloss-xyz-fe0c31` · `kosif-tool/styles/pm-tak3sh8-be5012` · `kosif-tool/styles/pm-tak3sh8-be5012/BRIEF.md`

#### EXPL-49 · لوحة قياسات حية · Live telemetry & math HUD · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** لوحتان أحاديتا العرض بقيم جدولية تُحدَّث من نموذج فيزيائي كل إطار، أو مخطط هندسي بقيم تُحسب أمامك. — Mono panels with tabular values updated each frame from a model.
- **متى أستخدمها / when:** فيزياء، فضاء، هندسة — physics, space, engineering.
- **كيف / how:** amber labels #e0a060, white right-aligned tabular values (2 decimals), 1 px rule; values computed from the same t as the picture; switch to ∞ / 'lost' at a horizon; wireframe isometric box with a highlighted vector and a side panel of values computing to a result counter. **أرقام / params:** 2 decimals; tabular-nums.
- **الدليل / proof:** `kosif-tool/styles/pm-rebutonepress-810f78` · `kosif-tool/styles/pm-adamdesgns-478d6d`

#### EXPL-50 · التوأم الإنشائي: حلّال الجملونات · Structural twin truss solver · ✅ مُثبت هنا / proven here
- **ماذا / what:** تحليل جملونات خطي مرن بمفاصل في 2D و3D: إزاحات، ردود أفعال، قوى محورية، شد وضغط، نسب استخدام، معاملات انهيار، وترتيب الأعضاء الأضعف، ومبادلة جزء وإعادة الحساب — أرقامه تقود فيلمًا ولوحة. — Linear-elastic pin-jointed truss analysis whose numbers drive a film and a dashboard.
- **متى أستخدمها / when:** «لماذا ينكسر هذا؟» شرح هندسي تعليمي — educational engineering explainers.
- **كيف / how:** python structural_twin.py --sample|--model m.json [--swap AB --area 0.0002 --young E --strength S --fracture-scale 2 --out r.json] (or kmotion.py structural); schema kosif.structural-twin.v0.1, ≤400 nodes / ≤1600 members; run here: sample triangle A(0,0) B(1,1) C(2,0) under 12 kN → first_failure_multiplier 2.946; tests 17/17 passed; twin_dashboard.py / kmotion twinview r.json --out twin.html gives an offline dashboard (baseline, swap, load slider; checked at 1365 and 390 px). Illustrative only — axial, no buckling/bending/fatigue, never for safety decisions (the output says so). **أرقام / params:** ≤400 nodes; sample 2.946×.
- **الدليل / proof:** `kosif-studio/motion/structural_twin.py:128` · `100-superskills/skills/kosif-montage-motion/tests/test_structural_twin.py` · `100-superskills/skills/kosif-montage-motion/references/STRUCTURAL_TWIN.md` · `100-superskills/skills/kosif-montage-motion/scripts/twin_dashboard.py:763`

#### EXPL-51 · فيلم التوأم الإنشائي · Structural twin film (truss on a character) · 🟢 جاهز / ready
- **ماذا / what:** جسم لطيف يصبح جملونًا ثلاثي الأبعاد توضيحيًا تقود حساباته الفيلم: المفاصل تظهر، الأعضاء تنمو، الحمل يرتفع، الأضعف ينكسر، جزء أثخن يُستبدل، وتُرتب أنماط الانهيار. — A cute object becomes a 3D truss whose solver output drives the film.
- **متى أستخدمها / when:** شرح هندسي ممتع — fun engineering explainers.
- **كيف / how:** build_truss.py lays the truss on anatomy (ground contacts pinned, pelvis/chest four-node rings cross-braced, skull nodes with 4-nearest-neighbour bracing, ear triangles; areas 1.2e-4 body, 4.0e-5 ear roots; plush E 8 MPa, strength 2 MPa; loads crown −1.9 N) → model.json (35 nodes, 109 members, 5 supports); K3S.trussOverlay(model, {nodeParts, radius .0015–.0022, jointRadius .0032–.0042}) rides rig parts, members coloured by utilisation (0 (.35,1,.72) → .5 (.75,1,.45) → .8 (1,.86,.35) → 1 (1,.36,.28)), flash on the weak member; load arrows (cylinder r .0032 + cone .011×.022) grow and shift hue yellow → red; six beats SHAPE → JOINT → LOAD → BREAK → SWAP → RANK; baseline first limit 2.38× (earL_out–crown, tension), break at 3.0× → mechanism, ×2.6 area swap → 3.77×. **أرقام / params:** 35 nodes / 109 members; 2.38× → 3.77×.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/twin/build_truss.py:46` · `100-superskills/skills/kosif-montage-motion/scripts/kit/shape-kit.js:395` · `kosif-studio/motion/references/STRUCTURAL_TWIN.md`

#### EXPL-52 · منظر تخطيطي ومفكك · Schematic, wireframe & exploded view · 🟢 جاهز / ready
- **ماذا / what:** الأجزاء تتحول من قطيفة إلى خطوط حواف ليمونية فوق شبح، وتنفصل عن الجسم، وتظهر حلقات متقطعة عند المفاصل. — Parts fade to lime edge lines over a ghost, explode from the body, and show dashed joint rings.
- **متى أستخدمها / when:** «كيف صُنع»، تشريح منتج — 'how it's made', product anatomy.
- **كيف / how:** const s = K3.schematic(root, {color:'#a8ff3c', ghost:'#f7f8f2', lineOpacity:.42, angle}); s.set(k, camera) (solids fade to 8%, ghost .55), s.explode(k) (×1.1 radial), s.joints(k) (camera-facing dashed rings .1–.125). **أرقام / params:** lines ≤.42; explode ×1.1.
- **الدليل / proof:** `kosif-studio/motion/kit/lab-kit.js:135` · `kosif-one/tools/kosif-studio/motion/kit/lab-kit.js:135`

#### EXPL-53 · شرح علمي ثلاثي الأبعاد بأربع مراحل · Four-stage 3D science explainer · 🟢 جاهز / ready
- **ماذا / what:** فيلم سينمائي يوقّت تسميات المراحل العربية المرقمة على ما يُظهره العالم ثلاثي الأبعاد: تبخر، تكاثف، هطول، جريان. — Numbered Arabic stage labels timed to what the 3D world shows.
- **متى أستخدمها / when:** دورات طبيعية وعمليات علمية — natural cycles and science processes.
- **كيف / how:** labels revealWords/hideWords: ١ 3.3–6.1 s, ٢ 6.9–9.3 s, ٣ 10.1–12.5 s, ٤ 13.1–15.1 s aligned with world states (vapour 2.6–7.2, clouds 5.8–9.4, storm 9.5–13.4, river 12.6–14.4); end title 15.7 s; 17 s 1920×1080 30 fps. **أرقام / params:** 17 s; 4 stages.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/water_cycle_3d/index.html:59` · `100-superskills/skills/kosif-montage-motion/scripts/projects/water_cycle_3d/src/main.js:83`

#### EXPL-54 · دورة الماء التعليمية المسطحة · Flat educational water cycle · ✅ مُثبت هنا / proven here
- **ماذا / what:** شرح صفي مسطح: منظر ثابت لبحر وشمس وجبل، أربع مراحل لكل منها حركة رئيسية واحدة، شريط تسمية أعلى، شريط مراحل أسفل، وسهم دورة ختامي. — A flat classroom explainer with one main motion per stage.
- **متى أستخدمها / when:** دروس أطفال علمية — kids' science lessons.
- **كيف / how:** kosif-one: single SVG + render(t), Cairo 700/800, 1920×1080 30 fps 300 frames, stages 1.5–4.0 / 4.0–6.1 / 6.1–8.0 / 8.0–8.9 / recap 8.9–10 s; kosif-studio water_cycle (17 s): M.drawPath ×9, flowDash, vapour, rain, flash, camera push, grain, vignette; beats 0–2.7 / 2.8–6.4 / 6.2–9.4 / 9.5–12.8 / 12.4–15.1 / 15.2–17 s; palette #FFD166 #FFE8C2 #7FD4FF #5EC8FF #2A6F97 #0D1B2A. The studio composition passes the static rules here (test run). **أرقام / params:** 10 s / 17 s; 1 motion per stage.
- **الدليل / proof:** `kosif-one/projects/water-cycle-animation/index.html` · `kosif-studio/motion/projects/water_cycle/index.html:152` · `kosif-studio/tests/test_studio.py:629` · `100-superskills/skills/trend-animation-styles/references/styles.md`

#### EXPL-55 · قواعد الدقة والوضوح للأطفال · Science accuracy & causal-step rules · 📄 موصوف / documented only
- **ماذا / what:** لا علم خاطئ أبدًا، حركة رئيسية واحدة لكل مرحلة، لا وميض، نص ≥40 بكسل وتباين ≥4.5:1، والمفهوم في 3–6 خطوات سببية. — Never wrong science, one main motion per stage, no flashing, text ≥40 px, contrast ≥4.5:1, 3–6 causal steps.
- **متى أستخدمها / when:** كل شرح تعليمي — every educational explainer.
- **كيف / how:** vapour rises from the sea, clouds form by cooling, rain falls on land, water returns to the sea; narration ~2.5 words/s with on-screen text shorter than spoken; fixed camera, one mover per stage, stage bar at the bottom; fact-check every claim; test the script on an imaginary student; supporting planning skills: math-science-tutor, software-architecture-adr. **أرقام / params:** ≥40 px; ≥4.5:1; 2.5 w/s.
- **الدليل / proof:** `kosif-one/projects/water-cycle-animation/DESIGN.md` · `100-superskills/skills/explainer-edu-animation/SKILL.md` · `100-superskills/skills/math-science-tutor/SKILL.md`

## بطاقات الشرح والوثائق — Explainer cards & documents

_بطاقات وفصول ومقتطفات تحمل الحجة._

#### EXPL-56 · نظام بطاقات الفيديو الشارح · Explainer card system · 📄 موصوف / documented only
- **ماذا / what:** بطاقات فصول ملونة، بطاقات مبادئ يتلون فيها العنصر المنطوق، جداول قبل/بعد بدائرة حمراء على الصف المنطوق، كلمات مفتاحية قافزة، وعناوين مرقمة. — Chapter, principle, table, keyword and numbered-title cards.
- **متى أستخدمها / when:** مقالات مصورة ويوتيوب تعليمي — video essays.
- **كيف / how:** chapter card: pastel #EFE6F7, #FFD400 heavy type outlined #1A1A1A at 6% of glyph height, glyphs 14% of frame height, 3–4 s, 1–2 stickers; principle card: white, labels 3.5% H #1A1A1A, the spoken element turns #E53935 0.3 s after it is said; table: rows × 2 s; keyword pop #FFD400 + outline, 1–3 words, 6% H, 0.8–2 s; numbered title 8% H, 2–3 s; author each card as HTML in the kosif scaffold and render with render_html.cjs. **أرقام / params:** 14/8/6/3.5% H; +0.3 s highlight.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2461-davinciresolve-style-essay/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2458-davinciresolve-gfx-hyperframes/SKILL.md`

#### EXPL-57 · الوثيقة المصدر وقلم التظليل · Source document & article excerpt overlay · 📄 موصوف / documented only
- **ماذا / what:** الوثيقة الأصلية كما هي مع قلم تظليل أصفر شفاف يمسح الجملة المنطوقة، أو مقتطف مقال على لوح ورقي فوق الفيديو. — The unchanged source page with a translucent highlighter on the spoken sentence, or an article excerpt panel over footage.
- **متى أستخدمها / when:** أخبار، تحقيقات، مقالات رأي — news, investigations, op-eds.
- **كيف / how:** highlighter: semi-transparent yellow rect (multiply) growing along the line timed to words.json, right → left for Arabic, held 3–5 s; excerpt: paper panel #FAFAF6 with #171717 text, 75–90% width, ≥5% margins, body 3–4% H, in 0.15–0.3 s, hold to read, out 0.15–0.25 s; optional red underline #D92D20 (0.25–0.4% H), ellipse callout 20–35% padding; news module: article slides up at readable size, keyword highlighted in place + source card. **أرقام / params:** hold 3–5 s; panel 75–90% W.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2430-akbun-davinciresolve-article-overlay/SKILL.md` · `kosif-one/vendor/hyperframes/skills/motion-graphics/categories/news/module.md`

#### EXPL-58 · فئات المخططات والكود في بصمة · Basma diagram & code film categories · 🟢 جاهز / ready
- **ماذا / what:** فئتا أفلام جاهزتان: مخططات من 3–5 عقد تظهر بالترتيب بروابط ونقاط تدفق، ومحرر كود داكن بأرقام أسطر وكتابة رمزًا رمزًا ولوح نتيجة. — Two film categories: ordered 3–5-node diagrams with flow dots, and dark code editors typing token by token with a result panel.
- **متى أستخدمها / when:** طلب سريع من محرر بصمة — quick requests in the Basma editor.
- **كيف / how:** FILM_CATS 'diagrams' and 'code' with templates concept, what-is, timeline, how-to, code-explain, dev-tool; code is LTR monospace with palette syntax colours.
- **الدليل / proof:** `app/public/js/00_editor.js:2007` · `app/public/js/00_editor.js:1777`

#### EXPL-59 · رسومات استعارية لكل جملة · Metaphor graphic per spoken claim · 🟢 جاهز / ready
- **ماذا / what:** كل فكرة منطوقة تحصل على استعارة مرسومة واحدة بجانب المتحدث تظهر فقط أثناء كلماتها: ساعة 24، مسار حلم، ميزان 94←76 كجم، سيارة، شريط وقت ينضب. — Each spoken idea gets one drawn metaphor that lives only while its words are spoken.
- **متى أستخدمها / when:** مونتاج متحدث تحفيزي — motivational talking-head edits.
- **كيف / how:** SVG groups #clock #dream #scale #car #timebar #endring, each drawn/animated only inside its speech() window; numbers count (94 → 76 kg) with tabular digits; time bar drains right → left; drawing details in DRAW-12.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:58` · `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:267`

#### EXPL-60 · بطاقات المقارنة والتشبيه والقوائم · Trade-off, analogy & checklist cards · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** بطاقتان متجاورتان بصفوف ✓/✗ وملصقات ملخصة، ثلاث لوحات تشبيه تتوهج النشطة منها، وقائمة بعلامات صح مرسومة ومؤشر ينتقل للصف النشط. — Side-by-side ✓/✗ cards, analogy triptychs and checklists with drawn ticks.
- **متى أستخدمها / when:** «هذا أم ذاك»، مكونات، خطوات وصفة — 'this or that', ingredients, recipe steps.
- **كيف / how:** trade-off: coloured headers, rows stagger 120 ms with green check / black cross boxes, rotated summary stickers, cost note below; analogy: 3 bordered cards each with its accent, icon + title + caption, active one glows; checklist: rows of circle + amount + name, upcoming at 45%, an arrow glyph slides to the active row (300 ms easeOutCubic), check drawn inside the circle (~250 ms). **أرقام / params:** rows 120 ms; tick 250 ms.
- **الدليل / proof:** `kosif-tool/styles/pm-0xnfrith-5be616` · `kosif-tool/styles/pm-yunn260414-60d996` · `kosif-tool/styles/pm-sarut0bisasuke-cefa43`

#### EXPL-61 · أدوات بصرية للشرح · Explainer visual devices · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** صفحة كلمات كأشرطة تمتلئ، تحديد منقط بطمس، فرز عناصر صورة في سلال، خريطة فقاعات لمنظومة، وسلسلة معاملة تستقيم. — Word-bar pages, dashed marquee blur, photo-object sorting, bubble ecosystem maps, straightening transaction chains.
- **متى أستخدمها / when:** شروح مفاهيم مجردة — abstract concept explainers.
- **كيف / how:** text as rounded rects of word widths filling dark row by row (120–200 ms/row, bar 8 px r 4) with the unknown word in accent; dashed 4/4 selection rect + 12 px backdrop blur in 300 ms; corner-bracket boxes on photo items, 'identifying' status, thumbnails fly 500 ms into 4 labelled buckets with counts; ~9 named hand-drawn ellipses + 12 empty blobs joined by dotted paths with a tiny boat traversing; paper chips rotated ±6° straighten into a vertical chain inside a dashed 'one transaction' box (0.6 s stagger); clock-face grid duplicates a scene to show monotony. **أرقام / params:** 120–200 ms/row; blur 12 px; fly 500 ms.
- **الدليل / proof:** `kosif-tool/styles/pm-1stnoel-c20a89` · `kosif-tool/styles/pm-jhylee95-e1152f` · `kosif-tool/styles/pm-gabrielbuzziv-4ff0c6` · `kosif-tool/styles/pm-nikolajankovic-ce4ff4`

#### EXPL-62 · أسلوب الرسومات التقنية · Tech blueprint style · 🟢 جاهز / ready
- **ماذا / what:** مظهر الرسم الهندسي: خطوط سماوية وبيضاء رفيعة على شبكة زرقاء داكنة ترسم نفسها، مع خطوط أبعاد وتسميات. — Engineering-drawing look: thin cyan/white line art on a dark blue grid that draws itself.
- **متى أستخدمها / when:** منتجات تقنية، هندسة، «كيف يعمل» — tech products, engineering.
- **كيف / how:** python3 tools/kosif.py scaffold tech-blueprint <dir>; SVG paths on a 24 px grid; draw-on 900–1200 px/s; nodes pop spring d14 s160; camera pans 700–1000 ms cubic-bezier(.65,0,.35,1); stroke 3–4 px, arrowheads 14–18 px, zoom ≤1.8. **أرقام / params:** grid 24 px; 900–1200 px/s.
- **الدليل / proof:** `kosif-tool/styles/tech-blueprint/SKILL.md` · `kosif-tool/styles/tech-blueprint/STYLE.json` · `kosif-tool/playbooks/diagrams.md`

#### EXPL-63 · لوحات ستوري بورد SVG مصغرة · SVG thumbnail storyboards · 📄 موصوف / documented only
- **ماذا / what:** مستطيلات ودوائر بسيطة في SVG تبيّن تكوين كل لقطة قبل البناء. — Simple rect/circle SVG thumbnails per shot.
- **متى أستخدمها / when:** اعتماد الخطة مع المستخدم — approving the plan.
- **كيف / how:** write thumbs.svg with one 16:9 or 9:16 frame per shot (subject boxes, text zones, arrows for camera moves) and show it before building.
- **الدليل / proof:** `100-superskills/skills/storyboard-shotlist/SKILL.md:24`

#### EXPL-64 · نموذج مجرة الأدلة · Evidence galaxy graph model · 💡 فكرة / idea
- **ماذا / what:** سلسلة من أربع عقد: حساب ← دليل ← معيار ← نتيجة، لتقود مرئيًا شبكيًا لتتبع التدقيق — لا يوجد عارض بعد. — A four-node account → evidence → standard → finding model meant to drive a node-link visual; no renderer exists.
- **متى أستخدمها / when:** شرح تتبع الأدلة في التدقيق — audit traceability explainers.
- **كيف / how:** data object with nodes[] and links[] plus traceEvidence(id); render with EXPL-19/17 (hub + data pulses) when needed. **أرقام / params:** 4 nodes, 3 links.
- **الدليل / proof:** `kosif-audit-studio/cinema/evidenceGalaxy.js`

## توليفات قوية / power combos

- **شرح «كيف يعمل» بالصوت / narrated how-it-works:** EXPL-03 + EXPL-04 + EXPL-21 + EXPL-16 + EXPL-17 + VOICE + ARAB-62 — نوع المخطط أولًا، كل عقدة تظهر عند كلمتها، رابط يُرسم ونبضة بيانات تجري.
- **ريل برمجي / dev reel:** EXPL-34 + EXPL-33 + EXPL-35 + EXPL-36 + UI — طرفية تكتب بتذبذب مزروع، إبراز السطر، ثم فرق أحمر/أخضر.
- **شرح هندسي ممتع / fun engineering:** EXPL-50 + EXPL-51 + EXPL-52 + CHAR-40 + 3D — أرنب يتحول إلى جملون، الحمل يرتفع، الأضعف ينكسر — بأرقام محسوبة هنا.
- **درس علوم للأطفال / kids' science:** EXPL-54 + EXPL-55 + EXPL-25 + EXPL-26 + DRAW-33 — حركة واحدة لكل مرحلة، شريط مراحل من اليمين، سهم دورة ختامي.
- **رياضيات بلغة عربية / Arabic maths:** EXPL-44 + EXPL-45 + ARAB-72 + DRAW-19 — معادلة LTR معزولة داخل سرد عربي، حد ملون، ودائرة يدوية حول النتيجة.
- **تكاملات منتج / product integrations:** EXPL-19 + EXPL-20 + GLOW + UI — شعار متوهج في المركز وأذرع تُرسم إلى الخدمات بنقاط تجري.
- **مقالة مصورة / video essay:** EXPL-56 + EXPL-57 + EXPL-27 + TRANS — بطاقات فصول، الوثيقة المصدر بقلم تظليل، وتصحيح الخطأ الشائع.
- **فيلم من طلب دمج / PR film:** EXPL-41 + EXPL-40 + EXPL-42 — آلية السلوك بدل الكود، ثم code-morph وأرقام +N/−M.

## أخطاء ممنوعة / never do

1. **لا أكثر من 7 عقد ظاهرة ولا أكثر من لون تأكيد لعقدتين** — يضيع المشاهد؛ قسّم إلى فصول (EXPL-01).
2. **لا تعكس المعادلة أو الكود داخل الجملة العربية** — الأرقام والرموز LTR معزولة دائمًا (EXPL-44/32).
3. **لا تكتب العربية حرفًا حرفًا في «الطرفية» أو الآلة الكاتبة** — يتكسر التشكيل؛ كلمات كاملة أو قناع (EXPL-33).
4. **لا تشغل محاكاة قوى حية أثناء الرندر** — احسبها مسبقًا ببذرة وفهرسها بالزمن (EXPL-14).
5. **لا تخترع أرقامًا هندسية أو علمية** — الجملون توضيحي وتقول ذلك على الشاشة، والأرقام من الحلّال لا من الخيال (EXPL-50/55).
6. **لا تبنِ المخطط كله ثم تثبته** — اكشفه بالترتيب السببي مع الصوت (EXPL-04/21).
7. **لا تطلب من مولد صور رسم كود أو مخطط بنص** — النص يتشوه؛ ابنه SVG/HTML حقيقيًا (EXPL-07/37).
8. **لا علم خاطئ ولا وميض في شروح الأطفال** — دقة أولًا ونص ≥40 بكسل (EXPL-55).
9. **لا تضخيم بلا تصريح** — اكتب «مُضخّم ×N» على الشاشة (EXPL-31).
10. **لا تنسخ ملفات المجلدات المصنفة copyleft من الأطلس** — خذ الفكرة وأعد كتابتها (EXPL-06).

## أقوى 5 حركات توقيع / 5 signature moves

1. **EXPL-16 — عملية من ثلاث خطوات:** عقد تقفز عند 0/900/1800 ملّي ثانية، روابط تُرسم، ونبضة بيانات — «كيف يعمل» في 4 ثوانٍ.
2. **EXPL-21 — مخطط يُبنى مع الصوت:** كل عنصر عند كلمته من words.json.
3. **EXPL-34 — جلسة الطرفية:** كتابة 35 حرفًا/ث، وميض Enter، مخرجات على دفعات، دفع 3% عند النجاح.
4. **EXPL-50 — التوأم الإنشائي:** أرقام هندسية حقيقية محسوبة هنا تتحول إلى فيلم ولوحة.
5. **EXPL-26 — شريط المراحل من اليمين:** حبوب مرقمة تمتلئ مع كل مرحلة وتضيء معًا في الخلاصة.
