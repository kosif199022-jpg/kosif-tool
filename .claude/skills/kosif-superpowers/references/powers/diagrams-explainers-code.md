# المخططات والشرح والكود — Diagrams, explainers & code

> فصل مُجمَّع آليًا من 241 ملاحظة حصاد (مستودعات KOSIF + أطلس المهارات + 253 فيديو مرجعي)، مدموجة إلى **240 قدرة** مرتبة من الأقوى دليلًا. لم يُحرَّر يدويًا بعد — تحقّق من الدليل قبل الادعاء.
> Auto-compiled chapter: 240 powers deduplicated by name from 241 harvested atoms; strongest evidence first.

**الحالة:** ✅ مُثبت هنا 6 · 🟢 جاهز 15 · 📦 بأمر تثبيت 64 · 🔑 مفتاح/خدمة 4 · 👁 شوهد في فيديو 98 · 📄 موصوف 43 · 💡 فكرة 10

#### EXPL-01 · التوأم الهيكلي — حل الجملونات · Structural Twin truss solver · ✅ مُثبت هنا
- **ماذا / what:** Linear-elastic pin-jointed 2D/3D truss solver: reactions, axial force/stress, first-limit ranking, hypothetical brittle removal, swap and recompute.
- **كيف / how:** python scripts/kmotion.py structural --sample|--model geo.json --swap AB --area 0.0002 --fracture-scale 3.2 --out twin.json
- **أرقام / params:** schema kosif.structural-twin.v0.1; ≤400 nodes/1600 members; sample A-B-C 12000 N → first limit 2.9463x; bunny 35 nodes/109 members first limit 2.38x
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/STRUCTURAL_TWIN.md` · `100-superskills/skills/kosif-montage-motion/PHYSICS_ADDENDUM_AR.md` · `kosif-studio/motion/structural_twin.py:128` · `kosif-studio/motion/structural_twin.py:242`

#### EXPL-02 · أسهم تلتصق بالحواف · Edge-snapped, tangent-correct arrows · ✅ مُثبت هنا
- **ماذا / what:** Connectors end exactly at the target outline and arrowheads follow the curve's final tangent.
- **كيف / how:** SVG <marker orient='auto'> with refX near tip; curve modes straight, cubic with perpendicular bow, orthogonal-h/v, waypoints. Marker ~3-4x stroke width.
- **أرقام / params:** markerWidth 3 (mm); bow e.g. 14mm
- **الدليل / proof:** `kosif-atlas/skills/2657-figures/10114-svg-primitives` · `kosif-atlas/skills/2657-figures/10113-svg-figure`

#### EXPL-03 · ترتيب طبقات ثابت · Deterministic layer paint order · ✅ مُثبت هنا
- **ماذا / what:** Paint background -> connectors -> boxes -> labels so lines pass under shapes.
- **كيف / how:** Group SVG into named <g> layers in registration order; animate layers in the same order for build-up reveals.
- **الدليل / proof:** `kosif-atlas/skills/2657-figures/10114-svg-primitives`

#### EXPL-04 · لوحة التوأم التفاعلية · Twin HUD viewer twinview · ✅ مُثبت هنا
- **ماذا / what:** Offline standalone HTML dashboard with baseline, swap and load slider (linear scaling).
- **كيف / how:** python scripts/kmotion.py twinview twin.json --out twin.html
- **أرقام / params:** tested at 1365 and 390 px
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/STRUCTURAL_TWIN.md` · `100-superskills/skills/kosif-montage-motion/PHYSICS_ADDENDUM_AR.md`

#### EXPL-05 · توأم إنشائي · Structural twin truss overlay · ✅ مُثبت هنا
- **ماذا / what:** Draws a truss model in 3D over a character/object, members coloured by utilisation (green -> yellow -> red), joints riding rig parts, grow/hide/break/flash per member.
- **كيف / how:** const tw=K3S.trussOverlay(model, {nodeParts, radius, jointRadius}); tw.update({alpha, jointAlpha, utilOf(id), camera, flash(id)}). Model from structural_twin.py.
- **أرقام / params:** member r .0022 m; joint r .0042; util stops 0 (.35,1,.72) .5 (.75,1,.45) .8 (1,.86,.35) 1.0 (1,.36,.28)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/shape-kit.js:395` · `100-superskills/skills/kosif-montage-motion/scripts/kit/shape-kit.js:401`

#### EXPL-06 · قالب النقاط · Template: bullet-list · ✅ مُثبت هنا
- **ماذا / what:** Title, rule, then up to six items slide in each with a circle and a pen-drawn check mark.
- **كيف / how:** python scripts/mtemplates.py new NAME --template bullet-list --set key=value ... [--seconds S --size WxH --fps F] -> projects/NAME/index.html (+ fonts, gsap, motion-kit); preview in a browser; render with motion.py render.
- **أرقام / params:** 8 s; title, items split by '|' (max 6), accent #5BD1A5, bg1 #10233a, bg2 #071321; item gap .35-.7 s; check path drawn .3 s
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/templates/motion/bullet-list.html` · `100-superskills/skills/kosif-montage-motion/scripts/mtemplates.py:58`

#### EXPL-07 · جلسة الطرفية كمشهد · Terminal session as a scene · 🟢 جاهز
- **ماذا / what:** Developer-tool beats as a terminal: prompt glyph, characters typed one by one, block caret blinking on hard steps, output appearing after a settle; real sessions can be captured as asciinema .cast and rendered to GIF.
- **كيف / how:** HTML terminal with tl.call per character (or TextPlugin); or generate a synthetic .cast JSON and replay it in the composition (asciinema/agg are external installs).
- **أرقام / params:** typing 15-20 cps for tech; caret 11x22px steps(1); settle ms after each command
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md` · `kosif-atlas/skills/2734-charly-check/10674-record` · `kosif-atlas/skills/166-demo-video/535-demo-video`

#### EXPL-08 · كتابة حرف بحرف مع مؤشر · Character typing with blinking cursor · 🟢 جاهز
- **ماذا / what:** Terminal-style reveal by updating textContent over time, with a stepped cursor blink.
- **كيف / how:** tl.call per char at (i/len)*0.9s; cursor tl.to opacity 0 duration 0.12 yoyo repeat 20 ease steps(1). Not for Arabic per-letter (shaping changes) — reveal Arabic by mask instead.
- **أرقام / params:** blink 0.12s
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md`

#### EXPL-09 · ظهور عقد الرحلة بالتتابع · Journey nodes pop-in stagger · 🟢 جاهز
- **ماذا / what:** Five stage nodes pop up with spring after the line starts drawing; done = teal fill + check, current = violet with 4px halo.
- **كيف / how:** li animation kosif-journey-node with nth-child delays.
- **أرقام / params:** 260ms spring; translate 7px + scale .88 -> 1; delays 180/225/270/315/360 ms (45ms step); node 36px, border 2px
- **الدليل / proof:** `kosif-audit-pro/app/globals.css:998` · `kosif-audit-pro/components/kosif/overview.tsx:56`

#### EXPL-10 · كشف سلسلة التتبع تتابعيًا · Trace chain sequential reveal · 🟢 جاهز
- **ماذا / what:** Source -> request -> procedure -> result -> decision cards appear one by one, then short connector ticks grow between them.
- **كيف / how:** li keyframe kosif-trace-node with 50ms step delays; li::after connector 8x2px scaleX 0->1.
- **أرقام / params:** nodes 260ms, delays 170/220/270/320/370 ms; connectors 160ms at 340ms, transform-origin right
- **الدليل / proof:** `kosif-audit-pro/app/globals.css:2191` · `kosif-audit-pro/app/globals.css:2223` · `kosif-audit-pro/components/kosif/views.tsx:467`

#### EXPL-11 · خطوط تدفق متحركة · Marching-ants flow edges · 🟢 جاهز
- **ماذا / what:** Connections in a flow map animate their dash offset so inputs/drafts visibly flow; outputs stay solid.
- **كيف / how:** SVG line stroke-dasharray 7 6 (inputs, warn colour) or 3 5 (drafts, violet); @keyframes pf-flow{to{stroke-dashoffset:-26}} 1.6s linear infinite; vector-effect non-scaling-stroke; dot-grid canvas radial-gradient 1px every 24px.
- **أرقام / params:** dash 7/6 and 3/5; offset -26; 1.6s
- **الدليل / proof:** `kosif-earth-ci-fork/ui/components/studio.css:25`

#### EXPL-12 · خريطة الاستوديو: الكيان في المنتصف · Studio node map (entity in the middle) · 🟢 جاهز
- **ماذا / what:** Reusable shell that draws an entity with what feeds it on one side and what it yields on the other as draggable number-carrying nodes over a dot grid, with an inspector and fixed tabs.
- **كيف / how:** SK.studio.mount(root,spec) -> {paint,focus,focused}; nodes 150px x >=80px absolutely positioned translate(-50%,-50%); hover scale 1.025; drag stores positions; edges as SVG lines classed in/draft/out/note.
- **أرقام / params:** dot grid 24px; node radius --sk-r
- **الدليل / proof:** `kosif-earth-ci-fork/ui/components/studio.js` · `kosif-earth-ci-fork/ui/components/studio.css`

#### EXPL-13 · شرطات متدفقة · Marching dashes (flowDash) · 🟢 جاهز
- **ماذا / what:** Animated dashed line flow for pipes, routes and data flow diagrams.
- **كيف / how:** MOTION.flowDash(tl, path, at, dur, {pattern, cycles}).
- **أرقام / params:** pattern '28 22'; 6 cycles over the duration; linear
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:247`

#### EXPL-14 · منظر تخطيطي ومفكك · Schematic / wireframe / exploded view · 🟢 جاهز
- **ماذا / what:** Fades a character from plush to lime edge-lines over a ghost, explodes parts from the body and shows dashed joint rings.
- **كيف / how:** const s=K3.schematic(root,{color, ghost, lineOpacity, angle}); s.set(k, camera); s.explode(k); s.joints(k).
- **أرقام / params:** lines #a8ff3c max opacity .42; ghost #f7f8f2 .55; explode 1.1x radial; joint ring .1-.125
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/lab-kit.js:135`

#### EXPL-15 · تعليقات مرتبطة بالمجسم · Projected 3D callouts · 🟢 جاهز
- **ماذا / what:** Dashed ring on a 3D anchor projected to screen, leader line, label card and live measurement chip.
- **كيف / how:** h.addCallout({anchor, label, title, text, side, radius, measure(t)}); set callout.show 0..1 each frame.
- **أرقام / params:** ring radius 4.5% H dashed 2px accent; card 14-22% W; leader dx 9% W, dy -14% H
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/lab-kit.js:233`

#### EXPL-16 · بناء نموذج الجمالون من التشريح · Truss model authoring from anatomy · 🟢 جاهز
- **ماذا / what:** A truss is laid on a character's anatomy: ground contacts pinned, two four-node rings (pelvis, chest) cross-braced, neck, skull nodes with 4-nearest-neighbour bracing, ear triangles to mid and tip, member areas by region.
- **كيف / how:** node(name, p, owner) with head-local + NECK offset and ear Euler XYZ (three.js order) rotation; bar(a,b) dedupe; knn(head, 4); area 1.2e-4 body, 4.0e-5 ear roots, 4.2e-5/3.4e-5 ear; PLUSH E 8 MPa, strength 2 MPa; loads crown −1.9 N, ear tip (−.12, 0, −.048) N.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/twin/build_truss.py:46` · `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/twin/build_truss.py:114`

#### EXPL-17 · توأم إنشائي · Structural truss twin · 🟢 جاهز
- **ماذا / what:** Illustrative 2D/3D pin-jointed truss analysis + offline dashboard (#081213 bg, mint #9dffb4).
- **كيف / how:** structural_twin.py --sample --out r.json; twin_dashboard.py r.json --out d.html
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/structural_twin.py` · `100-superskills/skills/kosif-montage-motion/scripts/twin_dashboard.py:763`

#### EXPL-18 · خطوط متقطعة متدفقة · Flowing dashes · 🟢 جاهز
- **ماذا / what:** Marches a dash pattern along a path to show flow (water, data, current).
- **كيف / how:** MOTION.flowDash(tl, path, at, dur, {pattern, cycles}).
- **أرقام / params:** pattern '28 22', 6 cycles, linear
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:247`

#### EXPL-19 · هيكل إنشائي فوق الشخصية · Structural truss overlay on a rig · 🟢 جاهز
- **ماذا / what:** 3D truss members and joints coloured by utilisation that ride the character rig.
- **كيف / how:** K3S.trussOverlay(model, {nodeParts}) fed by structural_twin.py output.
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/shape-kit.js:401`

#### EXPL-20 · وضع المخطط: سلكي ومفكك ومفاصل · Schematic modes: wireframe, exploded view, joint markers · 🟢 جاهز
- **ماذا / what:** Fades solid parts toward lime wireframe edges, explodes parts away from the body, shows dashed rings at pivots.
- **كيف / how:** s = K3.schematic(root, {color}); s.set(amount); s.explode(k); s.joints(k).
- **أرقام / params:** line colour #a8ff3c, line opacity 0.42, ghost #f7f8f2
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/lab-kit.js:135`

#### EXPL-21 · التوأم الإنشائي · Structural twin (truss solver) + dashboard · 🟢 جاهز
- **ماذا / what:** Illustrative 2D/3D pin-jointed truss analysis (SHAPE, JOINT, LOAD, BREAK, SWAP, RANK) whose numbers drive an explainer film and an offline dashboard; not certified FEA.
- **كيف / how:** python structural_twin.py MODEL.json (kmotion structural) ; twin_dashboard.py; bunny_twin project shows it in 3D.
- **أرقام / params:** linear elastic, axial only, no buckling
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/structural_twin.py` · `kosif-one/tools/kosif-studio/motion/references/STRUCTURAL_TWIN.md` · `kosif-one/tools/kosif-studio/motion/twin_dashboard.py`

#### EXPL-22 · صناديق تتسع لنصها تلقائيًا · Auto-fit labeled boxes · 📦 بأمر تثبيت
- **ماذا / what:** Box size computed from measured text bbox plus padding so labels never overflow.
- **كيف / how:** fontTools glyph advance measurement (or canvas measureText in browser), then rect = bbox + padding; center with text-anchor middle + dominant-baseline middle. For Arabic use browser measuring (shaping).
- **أرقام / params:** padding 2mm
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2657-figures/10114-svg-primitives` · `kosif-atlas/skills/2657-figures/10113-svg-figure`

#### EXPL-23 · مخططات Mermaid من نص · Mermaid text-to-diagram · 📦 بأمر تثبيت
- **ماذا / what:** Flowchart, sequence, class, state, ER, Gantt diagrams from text; rendering also validates syntax.
- **كيف / how:** mmdc -i x.mmd -o x.svg -t dark|forest -b transparent; then animate SVG nodes (stagger opacity/draw-on edges). Needs npm @mermaid-js/mermaid-cli (Puppeteer).
- **أرقام / params:** themes default/dark/forest/neutral
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/1245-mermaid-cli/2925-mermaid-cli`

#### EXPL-24 · مخططات D2 · D2 declarative diagrams with animated GIF · 📦 بأمر تثبيت
- **ماذا / what:** Declarative diagram language with dagre/elk layouts, many themes, outputs SVG/PNG/PDF and animated GIF.
- **كيف / how:** d2 binary; d2 --theme N --layout elk in.d2 out.svg; tala layout is paid.
- **أرقام / params:** layouts dagre, elk, tala(paid)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2173-tools-plugin/7914-d2-diagrams`

#### EXPL-25 · كتابة ملفات Excalidraw · Excalidraw JSON authoring · 📦 بأمر تثبيت
- **ماذا / what:** Generate .excalidraw JSON scenes (rectangles, ellipses, diamonds, arrows, lines, free text) for an editable whiteboard look.
- **كيف / how:** Write JSON per schema; render via excalidraw render template in headless browser or open in excalidraw.com; large diagrams built section by section.
- **أرقام / params:** roughness 1, fontFamily 1/3
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2790-work/11181-draw-excalidraw` · `kosif-atlas/skills/2966-pwdev-excalidraw/12488-excalidraw`

#### EXPL-26 · مخطط معماري داكن وفاتح · Dark/light architecture diagram themes · 📦 بأمر تثبيت
- **ماذا / what:** Dark SVG theme by default, div-based light theme for print; groupings as boundaries (VPC, cluster).
- **كيف / how:** HTML -> headless PNG. Ideas only.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/x4919-visual-gen/x20317-architecture-diagram`

#### EXPL-27 · اختيار خوارزمية تخطيط الشبكات · Graph layout algorithm choice · 📦 بأمر تثبيت
- **ماذا / what:** Trees, DAGs, block diagrams and networks each need a different layout engine.
- **كيف / how:** Rooted tree/decision tree -> tidy tree (Reingold-Tilford/Buchheim); flows, state machines, dependencies -> layered Sugiyama; ports/ERDs -> layered + orthogonal routing; undirected networks -> stress/Kamada-Kawai/Fruchterman-Reingold (multilevel when large); distance from root -> radial; cycles -> circular. Prefer stable layouts when animating between revisions.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2690-build-web-data-visualization/10326-node-link-and-diagram-layout/references/algorithm-selection.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10326-node-link-and-diagram-layout/SKILL.md`

#### EXPL-28 · مخططات SVG برمجية · Programmatic SVG schematics · 📦 بأمر تثبيت
- **ماذا / what:** Python builder for boxes-and-arrows with auto-fit text, edge-snapped arrows and deterministic layer order.
- **كيف / how:** Canvas in mm units; layers registered in paint order (background -> connectors -> boxes -> labels); LabeledBox auto-sizes from measured text + padding; Arrow.connect snaps to box edges, curved arrows keep tangent-correct heads via marker orient=auto; save SVG (+PNG via cairosvg). The same ideas are easy to hand-write in JS for animation.
- **أرقام / params:** font 7 pt default; padding 2 mm
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2657-figures/10114-svg-primitives/SKILL.md`

#### EXPL-29 · شبكة مفاهيم بقوة الجذب · Force-directed concept graph · 📦 بأمر تثبيت
- **ماذا / what:** A mind-map outline (root, branches, children, colors) rendered as an animated force graph.
- **كيف / how:** Convert the JSON outline to nodes/links; run a force simulation (d3-force or force-graph) for N ticks offline, then animate nodes settling from the center in branch order; branch color per top-level node; cap depth ~6.
- **أرقام / params:** max depth 6
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/30-learning/39-forcegraph-exporter/SKILL.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10326-node-link-and-diagram-layout/references/algorithm-selection.md`

#### EXPL-30 · تشغيل أمر في الطرفية · Code Terminal Run · 📦 بأمر تثبيت
- **ماذا / what:** Token-chrome terminal: prompt types deterministically, executes after a beat, output lines print on cues, fresh prompt appears.
- **كيف / how:** Install with `npx hyperframes add code-terminal-run` (copies to compositions/components/code-terminal-run.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chr…
- **أرقام / params:** prompt_glyph $; cadence uniform|human; vars: prompt_glyph=$; cadence=human[uniform|human]; cues=; accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add code-terminal-run` (copies to compositions/components/code-terminal-run`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/code-terminal-run/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/code-terminal-run/code-terminal-run.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/code-terminal-run.mdx`

#### EXPL-31 · محور الكوكبة · Constellation Hub · 📦 بأمر تثبيت
- **ماذا / what:** Feature nodes light up in narration order while real-length SVG connectors draw out from a central hub, ending in a lockup.
- **كيف / how:** Install with `npx hyperframes add constellation-hub` (copies to compositions/components/constellation-hub.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chr…
- **أرقام / params:** nodes "Capture,Compose,Render,Share"; cues; vars: hub_label=Product; nodes=Capture,Compose,Render,Share; cues=; accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add constellation-hub` (copies to compositions/components/constellation-hub`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/constellation-hub/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/constellation-hub/constellation-hub.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/constellation-hub.mdx`

#### EXPL-32 · تجميع بطاقات الميزات · Grid Card Assemble · 📦 بأمر تثبيت
- **ماذا / what:** N capability cards (thin icon draws on, mono label, optional body) stagger into a grid or list then hold.
- **كيف / how:** Install with `npx hyperframes add grid-card-assemble` (copies to compositions/components/grid-card-assemble.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless C…
- **أرقام / params:** items list; layout grid|list; columns 0=auto; vars: items=Capture,Compose,Render,Publish; layout=grid[grid|list]; columns=0(0..4); cues=; accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add grid-card-assemble` (copies to compositions/components/grid-card-assemble`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/grid-card-assemble/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/grid-card-assemble/grid-card-assemble.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/grid-card-assemble.mdx`

#### EXPL-33 · نواة ومدارات · Locked Nucleus Orbit · 📦 بأمر تثبيت
- **ماذا / what:** Fixed nucleus with deterministic satellite orbits that settle into a composed lockup.
- **كيف / how:** Install with `npx hyperframes add locked-nucleus-orbit` (copies to compositions/components/locked-nucleus-orbit.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headle…
- **أرقام / params:** satellites 4; vars: label=core; accent=green[green|blue|violet]; satellites=4(3..6)
- **تثبيت / install:** `npx hyperframes add locked-nucleus-orbit` (copies to compositions/components/locked-nucleus-orbit`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/locked-nucleus-orbit/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/locked-nucleus-orbit/locked-nucleus-orbit.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/locked-nucleus-orbit.mdx`

#### EXPL-34 · الإحاطة الدائرية · Radial Surround · 📦 بأمر تثبيت
- **ماذا / what:** Hairline chips assemble on an ellipse around a fixed centre subject and can converge inward with edge dim.
- **كيف / how:** Install with `npx hyperframes add radial-surround` (copies to compositions/components/radial-surround.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromiu…
- **أرقام / params:** chips list; close_in true; vars: center_label=Your team; chips=Docs,Tickets,Dashboards,Inbox,Chat,Sheets; close_in=True; cues=; accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add radial-surround` (copies to compositions/components/radial-surround`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/radial-surround/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/radial-surround/radial-surround.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/radial-surround.mdx`

#### EXPL-35 · محاكي الطرفية · Terminal Simulator · 📦 بأمر تثبيت
- **ماذا / what:** Terminal window types commands and streams log output.
- **كيف / how:** Install with `npx hyperframes add terminal-simulator` (copies to compositions/components/terminal-simulator.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless C…
- **تثبيت / install:** `npx hyperframes add terminal-simulator` (copies to compositions/components/terminal-simulator`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/terminal-simulator/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/terminal-simulator/terminal-simulator.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/terminal-simulator.mdx`

#### EXPL-36 · كود على لوح ثلاثي الأبعاد · Code 3D Extrude · 📦 بأمر تثبيت
- **ماذا / what:** Syntax-highlighted code on a lit, beveled WebGL slab rotating through space to a readable rest.
- **كيف / how:** Install with `npx hyperframes add code-3d-extrude` (copies the full composition to compositions/code-3d-extrude.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: Three.js 0.147.0 (CDN), Canvas 2D painter, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 8 s; 1920x1080; duration 8 s
- **تثبيت / install:** `npx hyperframes add code-3d-extrude` (copies the full composition to compositions/code-3d-extrude`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/code-3d-extrude/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/code-3d-extrude/code-3d-extrude.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/code-3d-extrude.mdx`

#### EXPL-37 · فرق الكود · Code Diff · 📦 بأمر تثبيت
- **ماذا / what:** Colour diff: removed lines collapse in red, added lines expand in green.
- **كيف / how:** Install with `npx hyperframes add code-diff` (copies the full composition to compositions/code-diff.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 6 s; 1920x1080; duration 6 s
- **تثبيت / install:** `npx hyperframes add code-diff` (copies the full composition to compositions/code-diff`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/code-diff/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/code-diff/code-diff.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/code-diff.mdx`

#### EXPL-38 · إبراز سطر كود · Code Highlight Sweep · 📦 بأمر تثبيت
- **ماذا / what:** Highlight band sweeps a target line while context dims.
- **كيف / how:** Install with `npx hyperframes add code-highlight` (copies the full composition to compositions/code-highlight.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 5 s; 1920x1080; duration 5 s
- **تثبيت / install:** `npx hyperframes add code-highlight` (copies the full composition to compositions/code-highlight`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/code-highlight/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/code-highlight/code-highlight.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/code-highlight.mdx`

#### EXPL-39 · تحول الكود · Code Morph · 📦 بأمر تثبيت
- **ماذا / what:** One snippet morphs into another: tokens glide, leavers fade, enterers fade in (Shiki Magic Move behaviour on paused GSAP).
- **كيف / how:** Install with `npx hyperframes add code-morph` (copies the full composition to compositions/code-morph.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 7 s; 1920x1080; duration 7 s
- **تثبيت / install:** `npx hyperframes add code-morph` (copies the full composition to compositions/code-morph`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/code-morph/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/code-morph/code-morph.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/code-morph.mdx`

#### EXPL-40 · كود من الجزيئات · Code Particle Assemble · 📦 بأمر تثبيت
- **ماذا / what:** Thousands of GPU points fly to the exact glyph pixels of syntax-highlighted code.
- **كيف / how:** Install with `npx hyperframes add code-particle-assemble` (copies the full composition to compositions/code-particle-assemble.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: Three.js 0.147.0 (CDN), WebGL fragment shader, Canvas 2D painter, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** WebGL; 8 s; 1920x1080; duration 8 s
- **تثبيت / install:** `npx hyperframes add code-particle-assemble` (copies the full composition to compositions/code-particle-assemble`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/code-particle-assemble/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/code-particle-assemble/code-particle-assemble.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/code-particle-assemble.mdx`

#### EXPL-41 · تمرير الكود · Code Scroll To Line · 📦 بأمر تثبيت
- **ماذا / what:** Camera scrolls a long file to centre and spotlight a target line.
- **كيف / how:** Install with `npx hyperframes add code-scroll` (copies the full composition to compositions/code-scroll.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 6 s; 1920x1080; duration 6 s
- **تثبيت / install:** `npx hyperframes add code-scroll` (copies the full composition to compositions/code-scroll`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/code-scroll/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/code-scroll/code-scroll.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/code-scroll.mdx`

#### EXPL-42 · كود يذوب بالشيدر · Code Shader Dissolve · 📦 بأمر تثبيت
- **ماذا / what:** Fragment shader resolves code out of seeded noise with a chromatic dissolve front and edge glow.
- **كيف / how:** Install with `npx hyperframes add code-shader-dissolve` (copies the full composition to compositions/code-shader-dissolve.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: Three.js 0.147.0 (CDN), WebGL fragment shader, Canvas 2D painter, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 7 s; 1920x1080; duration 7 s
- **تثبيت / install:** `npx hyperframes add code-shader-dissolve` (copies the full composition to compositions/code-shader-dissolve`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/code-shader-dissolve/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/code-shader-dissolve/code-shader-dissolve.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/code-shader-dissolve.mdx`

#### EXPL-43 · طرفية آبل برو · Code Snippet - Apple Terminal Pro · 📦 بأمر تثبيت
- **ماذا / what:** Apple Terminal "Pro" profile: black background, grey text, lime cursor, per-character shell typing.
- **كيف / how:** Install with `npx hyperframes add code-snippet-apple-terminal-pro` (copies the full composition to compositions/code-snippet-apple-terminal-pro.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 12 s; 1920x1080; duration 12 s
- **تثبيت / install:** `npx hyperframes add code-snippet-apple-terminal-pro` (copies the full composition to compositions/code-snippet-apple-terminal-pro`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/code-snippet-apple-terminal-pro/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/code-snippet-apple-terminal-pro/code-snippet-apple-terminal-pro.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/code-snippet-apple-terminal-pro.mdx`

#### EXPL-44 · محرر في إس كود داكن 2026 · Code Snippet - Dark 2026 · 📦 بأمر تثبيت
- **ماذا / what:** VS Code workbench with activity bar, sidebar, tabs, terminal, status bar and per-character typing in the Dark 2026 theme.
- **كيف / how:** Install with `npx hyperframes add code-snippet-dark-2026` (copies the full composition to compositions/code-snippet-dark-2026.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: inline SVG, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 11 s; 1920x1080; duration 11 s
- **تثبيت / install:** `npx hyperframes add code-snippet-dark-2026` (copies the full composition to compositions/code-snippet-dark-2026`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/code-snippet-dark-2026/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/code-snippet-dark-2026/code-snippet-dark-2026.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/code-snippet-dark-2026.mdx`

#### EXPL-45 · محرر في إس كود داكن حديث · Code Snippet - Dark Modern · 📦 بأمر تثبيت
- **ماذا / what:** Same VS Code workbench typing scene in the Dark Modern theme.
- **كيف / how:** Install with `npx hyperframes add code-snippet-dark-modern` (copies the full composition to compositions/code-snippet-dark-modern.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: inline SVG, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 11 s; 1920x1080; duration 11 s
- **تثبيت / install:** `npx hyperframes add code-snippet-dark-modern` (copies the full composition to compositions/code-snippet-dark-modern`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/code-snippet-dark-modern/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/code-snippet-dark-modern/code-snippet-dark-modern.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/code-snippet-dark-modern.mdx`

#### EXPL-46 · كتابة الكود · Code Typing · 📦 بأمر تثبيت
- **ماذا / what:** Token-streamed typing with a caret that tracks the frontier, no CSS animation.
- **كيف / how:** Install with `npx hyperframes add code-typing` (copies the full composition to compositions/code-typing.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 5 s; 1920x1080; duration 5 s
- **تثبيت / install:** `npx hyperframes add code-typing` (copies the full composition to compositions/code-typing`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/code-typing/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/code-typing/code-typing.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/code-typing.mdx`

#### EXPL-47 · مخطط القرار · Flowchart · 📦 بأمر تثبيت
- **ماذا / what:** Animated decision tree: SVG connectors, sticky-note nodes, cursor interaction and typing correction.
- **كيف / how:** Install with `npx hyperframes add flowchart` (copies the full composition to compositions/flowchart.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: inline SVG, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 1920x1080; 12 s; Google Fonts: Inter; 1920x1080; duration 12 s
- **تثبيت / install:** `npx hyperframes add flowchart` (copies the full composition to compositions/flowchart`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/flowchart/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/flowchart/flowchart.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/flowchart.mdx`

#### EXPL-48 · مخطط القرار العمودي · Flowchart Vertical · 📦 بأمر تثبيت
- **ماذا / what:** Portrait version of the decision-tree flowchart.
- **كيف / how:** Install with `npx hyperframes add flowchart-vertical` (copies the full composition to compositions/flowchart-vertical.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: inline SVG, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 1440x2560; 12 s; Google Fonts: Inter; 1440x2560; duration 12 s
- **تثبيت / install:** `npx hyperframes add flowchart-vertical` (copies the full composition to compositions/flowchart-vertical`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/flowchart-vertical/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/flowchart-vertical/flowchart-vertical.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/flowchart-vertical.mdx`

#### EXPL-49 · شجرة القرار · Example project: decision-tree · 📦 بأمر تثبيت
- **ماذا / what:** Animated branching flowchart example project (10 s, Inter). [Local copy lacks its sub-compositions: compositions/decision_tree.html.]
- **كيف / how:** Starter project: `npx hyperframes init --example decision-tree` style scaffold (index.html mounts sub-compositions via data-composition-src); reuse its palette/type as a style reference.
- **أرقام / params:** 1920x1080; 10 s
- **تثبيت / install:** `npx hyperframes init --example decision-tree` style scaffold (index`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/examples/decision-tree/registry-item.json` · `kosif-one/vendor/hyperframes/registry/examples/decision-tree/index.html`

#### EXPL-50 · مرجع التقنيات البصرية الثلاث عشرة · Visual techniques reference (13) · 📦 بأمر تثبيت
- **ماذا / what:** SVG path drawing, Canvas 2D procedural art (hash noise driven by a GSAP proxy), CSS 3D transforms, per-word kinetic type, Lottie, video compositing, char-by-char typing, variable-font axis animation, MotionPathPlugin, velocity-matched transitions, audio-reactive animation, clip-path reveal masks, We…
- **كيف / how:** techniques.md sections 1-13 + 'when to use what' energy table.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/techniques.md`

#### EXPL-51 · فئة موشن: إبراز مقال إخباري · Motion-graphics category: News article highlight · 📦 بأمر تثبيت
- **ماذا / what:** Category module: article text at readable size slides up, keyword highlighted in place + source card.
- **كيف / how:** Director sets category 'news' in shot-plan.json; builder follows motion-graphics/categories/news/module.md reuse-first.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/motion-graphics/categories/news/module.md` · `kosif-one/vendor/hyperframes/skills/motion-graphics/SKILL.md`

#### EXPL-52 · فيديو شرح بلا وجه · Faceless explainer workflow · 📦 بأمر تثبيت
- **ماذا / what:** Arbitrary text to a narrated explainer (up to ~3 min, sweet spot 30-90 s) where every visual is invented typography, abstract graphics, diagrams or data-viz: preset -> frame.md, storyboard + SCRIPT.md, background audio, per-frame time-coded shot sequences, parallel frame workers, captions, transitio…
- **كيف / how:** build-frame.mjs --preset <name>; audio.mjs --script SCRIPT.md --storyboard STORYBOARD.md --voice <id> &; audio.mjs sync-durations / fetch-sfx; frame-packets.mjs; captions.mjs build; assemble-index.mjs; transitions.mjs inject + verify; lint; check; snapshot; preview; render.
- **أرقام / params:** default voice Marcia (HeyGen) / am_michael (Kokoro)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/faceless-explainer/SKILL.md` · `kosif-one/vendor/hyperframes/skills/faceless-explainer/scripts/frame-packets.test.mjs` · `kosif-one/vendor/hyperframes/skills/faceless-explainer/scripts/audio.test.mjs`

#### EXPL-53 · أنواع إطارات طلب الدمج · PR frame types and treatments · 📦 بأمر تثبيت
- **ماذا / what:** hook, problem, change, diff, before_after, mechanism (show runtime behavior, not code), impact, evidence (+N/-M, passing test, benchmark), credits, cta mapped to code-editorial treatments (Cover, Statement, Pull-quote, navy Code Surface, Number/Impact, Closing).
- **كيف / how:** pr-to-video/references/story-design.md.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/pr-to-video/references/story-design.md`

#### EXPL-54 · كتلة تحريك الكود: code-diff · Code animation block: code-diff · 📦 بأمر تثبيت
- **ماذا / what:** Unified diff in an editor window: removed lines collapse red, added expand green, staggered (6 s); exactly 2 states.
- **كيف / how:** npx hyperframes add code-diff; fill __TOKENS states / __BLOCK params per pr-to-video/references/code-vocabulary.md.
- **تثبيت / install:** `npx hyperframes add code-diff`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/pr-to-video/references/code-vocabulary.md` · `kosif-one/vendor/hyperframes/registry/blocks/code-diff`

#### EXPL-55 · كتلة تحريك الكود: code-morph · Code animation block: code-morph · 📦 بأمر تثبيت
- **ماذا / what:** One snippet transforms into another; shared tokens glide (FLIP), leavers fade, enterers fade in (7 s).
- **كيف / how:** npx hyperframes add code-morph; fill __TOKENS states / __BLOCK params per pr-to-video/references/code-vocabulary.md.
- **تثبيت / install:** `npx hyperframes add code-morph`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/pr-to-video/references/code-vocabulary.md` · `kosif-one/vendor/hyperframes/registry/blocks/code-morph`

#### EXPL-56 · كتلة تحريك الكود: code-typing · Code animation block: code-typing · 📦 بأمر تثبيت
- **ماذا / what:** Per-character typewriter reveal with gliding caret (5 s).
- **كيف / how:** npx hyperframes add code-typing; fill __TOKENS states / __BLOCK params per pr-to-video/references/code-vocabulary.md.
- **تثبيت / install:** `npx hyperframes add code-typing`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/pr-to-video/references/code-vocabulary.md` · `kosif-one/vendor/hyperframes/registry/blocks/code-typing`

#### EXPL-57 · كتلة تحريك الكود: code-highlight · Code animation block: code-highlight · 📦 بأمر تثبيت
- **ماذا / what:** Blue band sweeps one line, the rest dims (5 s; line 0-based).
- **كيف / how:** npx hyperframes add code-highlight; fill __TOKENS states / __BLOCK params per pr-to-video/references/code-vocabulary.md.
- **تثبيت / install:** `npx hyperframes add code-highlight`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/pr-to-video/references/code-vocabulary.md` · `kosif-one/vendor/hyperframes/registry/blocks/code-highlight`

#### EXPL-58 · كتلة تحريك الكود: code-scroll · Code animation block: code-scroll · 📦 بأمر تثبيت
- **ماذا / what:** Camera scrolls a long file to center a target line and dims the rest (6 s; line 1-based).
- **كيف / how:** npx hyperframes add code-scroll; fill __TOKENS states / __BLOCK params per pr-to-video/references/code-vocabulary.md.
- **تثبيت / install:** `npx hyperframes add code-scroll`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/pr-to-video/references/code-vocabulary.md` · `kosif-one/vendor/hyperframes/registry/blocks/code-scroll`

#### EXPL-59 · كتلة تحريك الكود: code-3d-extrude · Code animation block: code-3d-extrude · 📦 بأمر تثبيت
- **ماذا / what:** Code on a lit beveled 3D slab that rotates and settles (8 s, WebGL).
- **كيف / how:** npx hyperframes add code-3d-extrude; fill __TOKENS states / __BLOCK params per pr-to-video/references/code-vocabulary.md.
- **تثبيت / install:** `npx hyperframes add code-3d-extrude`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/pr-to-video/references/code-vocabulary.md` · `kosif-one/vendor/hyperframes/registry/blocks/code-3d-extrude`

#### EXPL-60 · كتلة تحريك الكود: code-particle-assemble · Code animation block: code-particle-assemble · 📦 بأمر تثبيت
- **ماذا / what:** GPU particles scatter then fly to glyph pixels and resolve to syntax color (8 s, WebGL).
- **كيف / how:** npx hyperframes add code-particle-assemble; fill __TOKENS states / __BLOCK params per pr-to-video/references/code-vocabulary.md.
- **تثبيت / install:** `npx hyperframes add code-particle-assemble`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/pr-to-video/references/code-vocabulary.md` · `kosif-one/vendor/hyperframes/registry/blocks/code-particle-assemble`

#### EXPL-61 · كتلة تحريك الكود: code-shader-dissolve · Code animation block: code-shader-dissolve · 📦 بأمر تثبيت
- **ماذا / what:** Code compiles into existence from seeded noise with a moving dissolve front + edge glow (7 s, WebGL).
- **كيف / how:** npx hyperframes add code-shader-dissolve; fill __TOKENS states / __BLOCK params per pr-to-video/references/code-vocabulary.md.
- **تثبيت / install:** `npx hyperframes add code-shader-dissolve`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/pr-to-video/references/code-vocabulary.md` · `kosif-one/vendor/hyperframes/registry/blocks/code-shader-dissolve`

#### EXPL-62 · إطار الآلية: تحريك سلوك الكود · Mechanism beat: animate what code does · 📦 بأمر تثبيت
- **ماذا / what:** Show runtime behavior instead of code: retry/backoff request lifecycle (fire -> 500 -> growing wait -> retry -> 200), cache racing lanes (cold DB vs cached), serial lane reshaping into parallel lanes, race bug then fixed flow, performance bars racing, tangled call-graph untangling, data flowing a ne…
- **كيف / how:** Invented SVG/GSAP diagram or flowchart / flowchart-vertical / data-chart blocks.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/pr-to-video/references/code-vocabulary.md`

#### EXPL-63 · وضع المخطط والتفجير · schematic wire↔plush / explode / joints · 📦 بأمر تثبيت
- **ماذا / what:** set(k) wire↔plush, explode(k), joints(k) dashed pivots.
- **كيف / how:** shape-kit.js / lab-kit.js in a 3D project; read references/shape-kit.md
- **أرقام / params:** schematic
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:101` · `100-superskills/skills/kosif-montage-motion/SKILL.md:113` · `100-superskills/skills/kosif-montage-motion/CHANGELOG.md`

#### EXPL-64 · تراكب الجملون · trussOverlay · 📦 بأمر تثبيت
- **ماذا / what:** Structural twin drawn in 3D over a sculpt.
- **كيف / how:** shape-kit.js / lab-kit.js in a 3D project; read references/shape-kit.md
- **أرقام / params:** K3S.trussOverlay
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:101` · `100-superskills/skills/kosif-montage-motion/SKILL.md:113` · `100-superskills/skills/kosif-montage-motion/CHANGELOG.md`

#### EXPL-65 · رموز المعنى في verse · verse meaning symbols · 📦 بأمر تثبيت
- **ماذا / what:** Draws a symbol above a line by concept: sun, moon, heart, clock, money, trophy, road, question, check, home, rain, light; counts up spoken numbers.
- **كيف / how:** python scripts/kmotion.py verse (CONCEPTS, concept_of)
- **أرقام / params:** 12 symbols
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md`

#### EXPL-66 · فيلم التوأم الإنشائي · Structural twin film (truss analysis as animation) · 📦 بأمر تثبيت
- **ماذا / what:** A cute object becomes an illustrative 3D pin-jointed truss whose real solver output drives the film: joints pop on, members grow, load rises, the weakest member breaks, a thicker part is swapped in and failure modes are ranked.
- **كيف / how:** python projects/bunny_twin/twin/build_truss.py → model.json (35 nodes, 109 members, 5 pinned supports), report.json, assets/twin.js; S.trussOverlay(local, {nodeParts, radius .0015, jointRadius .0032}) bound to rig parts; utilOf(id) = util·L; flash on weak member; kmotion render projects/bunny_twin --engine studio --blur 2.
- **أرقام / params:** baseline first limit 2.38× (earL_out-crown, tension) → after ×2.6 area swap 3.77×; break at 3.0× → mechanism
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/twin/build_truss.py:1` · `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:71` · `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/assets/twin.js`

#### EXPL-67 · أسهم أحمال ملونة بالشدة · Load arrows coloured by magnitude · 📦 بأمر تثبيت
- **ماذا / what:** Force arrows (cylinder shaft + cone head) sit on the loaded points, grow with load and shift hue from yellow toward red as the load approaches failure.
- **كيف / how:** makeArrow(len): Cylinder r .0032 + Cone .011×.022; colour setHSL(lerp(.14, .02, (L−1.5)/1.5), 1, .62); scale .8+.25·L/Lmax; ear arrow rotated −π/2 and removed after the break.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:86` · `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/src/main.js:162`

#### EXPL-68 · وسوم مثبتة بقياسات حية · Anchored callouts with live measurements · 📦 بأمر تثبيت
- **ماذا / what:** Callouts attach to 3D joints and show a bilingual label, a title, a description and a measurement that can vary with time.
- **كيف / how:** H1 = hud(root, W, H, {title, subtitle, seed}); H1.addCallout({anchor: joint, label 'THE EAR · الأذن', title, text, side, measure: t → '0.42 m'}); co.show = pulse(t, a, b); H1.update(t, camera, {stage, side, duration}).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/lab_rabbit_lion/src/main.js:32` · `100-superskills/skills/kosif-montage-motion/scripts/projects/lab_rabbit_lion/src/main.js:69`

#### EXPL-69 · شرح علمي ثلاثي الأبعاد بأربع مراحل · Four-stage science explainer in 3D · 📦 بأمر تثبيت
- **ماذا / what:** A cinematic explainer that times numbered Arabic stage labels to what the 3D world shows: evaporation, condensation, precipitation, runoff.
- **كيف / how:** labels revealWords/hideWords: ١ 3.3–6.1 s, ٢ 6.9–9.3 s, ٣ 10.1–12.5 s, ٤ 13.1–15.1 s; world states (vapour 2.6–7.2, clouds 5.8–9.4, storm 9.5–13.4, river 12.6–14.4) align; end title 15.7 s.
- **أرقام / params:** 17 s 1920×1080 30 fps
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/water_cycle_3d/index.html:59` · `100-superskills/skills/kosif-montage-motion/scripts/projects/water_cycle_3d/src/main.js:83`

#### EXPL-70 · رسومات استعارية لجملة منطوقة · Metaphor graphics for a spoken claim · 📦 بأمر تثبيت
- **ماذا / what:** Each spoken idea gets one simple drawn metaphor beside the speaker: a 24-hour clock for 'with yourself 24 hours', a rising path for 'your dream', a weight rail with a counter dropping 94→76 kg for 'your weight', a car drawing driving off for 'your car', a time bar draining right-to-left for 'wasting…
- **كيف / how:** SVG groups #clock #dream #scale #car #timebar #endring each drawn/animated only while its words are spoken (see speech() times).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:58` · `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:220` · `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:267`

#### EXPL-71 · تكامل: Manim Community · Integration: Manim Community · 📦 بأمر تثبيت
- **ماذا / what:** Catalogued skill/MCP/library (link only; not installed here).
- **كيف / how:** see official setup
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`

#### EXPL-72 · ستايل دورة الماء التعليمي المسطح · Flat educational water cycle (style) · 📦 بأمر تثبيت
- **ماذا / what:** A 10 s 16:9 flat classroom explainer: one fixed wide view of sea, sun, sky and mountain; four stages (evaporation, condensation, precipitation, collection) each with one main motion, a white caption bar on top, a stage-tracker pill bar at the bottom and an orange loop arrow to close.
- **كيف / how:** Single SVG + render(t) in plain JS; Cairo 700/800; capture to MP4 with Playwright + ffmpeg.
- **أرقام / params:** 1920x1080, 30 fps, 300 frames; stages 1.5-4.0 / 4.0-6.1 / 6.1-8.0 / 8.0-8.9 / recap 8.9-10
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/water-cycle-animation/index.html` · `kosif-one/projects/water-cycle-animation/DESIGN.md` · `kosif-one/projects/water-cycle-animation/STORYBOARD.md`

#### EXPL-73 · سهم الدورة الختامي · Recap loop arrow draw-on · 📦 بأمر تثبيت
- **ماذا / what:** A big orange loop arrow draws around the whole scene to say 'and it repeats'; the arrowhead marker is attached only when the stroke is complete.
- **كيف / how:** pathLength=1 dash draw 8.9-9.8 s eased; marker-end url(#head) set when progress > .98; colour #FF7A00 9 px.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/water-cycle-animation/index.html:30-32` · `kosif-one/projects/water-cycle-animation/index.html:76` · `kosif-one/projects/water-cycle-animation/index.html:181-185`

#### EXPL-74 · شريط المراحل · Stage tracker pills (RTL) · 📦 بأمر تثبيت
- **ماذا / what:** A bottom bar of numbered stage pills, ordered right-to-left, where the current stage fills orange and all stages light up together in the recap.
- **كيف / how:** 4 pills 260x70 rx35 at y 968, x = 1395 - i*290; fill mix(#FFFFFF,#FF7A00,on), text mix(#0B2545,#FFFFFF,on); on = max(fadeWin(stage), seg(8.9,9.3)*.85).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/water-cycle-animation/index.html:131-136` · `kosif-one/projects/water-cycle-animation/index.html:193-198`

#### EXPL-75 · أسهم الحرارة المتحركة · Heat arrows (marching dashes) · 📦 بأمر تثبيت
- **ماذا / what:** Dashed orange arrows from the sun to the sea whose dashes march to show energy flowing.
- **كيف / how:** stroke #FF9E2C 7 px dasharray '20 18'; dashoffset -140t; opacity fadeWin(1.6,4.1,.35); sun rays rotate 18 deg/s and pulse 1+.06 sin(4PI t) while heating.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/water-cycle-animation/index.html:45-48` · `kosif-one/projects/water-cycle-animation/index.html:141-145`

#### EXPL-76 · اختيار نوع المخطط · Mermaid diagram type picker · 📦 بأمر تثبيت
- **ماذا / what:** flow→flowchart, time→sequence, data→ER, decisions→decision tree; mindmap too.
- **كيف / how:** write diagram.mmd, export with mmdc if present else raw SVG
- **أرقام / params:** max 12 nodes; one direction TB or LR; every arrow labelled; B/W readable
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/diagrams-mermaid-architecture/SKILL.md:21`

#### EXPL-77 · تيار متقطع متحرك · Flowing dash current · 📦 بأمر تثبيت
- **ماذا / what:** Animates a dashed stroke to show flow (current, data, water) along a path.
- **كيف / how:** MOTION.flowDash(tl, path, at, dur, {pattern, cycles}).
- **أرقام / params:** pattern '28 22', 6 cycles, linear
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:247`

#### EXPL-78 · طبقة الجملون الإنشائي · Structural truss overlay · 📦 بأمر تثبيت
- **ماذا / what:** 3D members and joints of a structural-twin model, joints riding rig parts, members coloured by utilisation with flash/hide/grow/gap per member.
- **كيف / how:** const tr = K3S.trussOverlay(report.model, {nodeParts, radius, jointRadius}); tr.update({alpha, utilOf, camera, flash}).
- **أرقام / params:** utilisation ramp 0 (.35,1,.72) -> .5 (.75,1,.45) -> .8 (1,.86,.35) -> 1 (1,.36,.28); member r 2.2 mm, joint 4.2 mm
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/shape-kit.js:395`

#### EXPL-79 · أوضاع المخطط · Schematic modes (wire, explode, joints) · 📦 بأمر تثبيت
- **ماذا / what:** Every part gets an edge overlay and ghost; fade plush -> wireframe, explode parts from the body, show dashed joint rings that face the camera.
- **كيف / how:** const s = K3.schematic(root, {color, ghost, lineOpacity, angle}); s.set(k, camera); s.explode(k); s.joints(k).
- **أرقام / params:** lime #a8ff3c lines max .42, ghost #f7f8f2 .55, solids fade to 8%; explode ×1.1 radial
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/lab-kit.js:135`

#### EXPL-80 · تحويل الصورة إلى برنامج بايثون مطابق · Image to standalone Pillow program (exact) · 📦 بأمر تثبيت
- **ماذا / what:** Writes a self-contained Python program: the picture's colour regions as readable draw.polygon calls (largest first, editable), then the original's embedded bytes complete every pixel the drawing missed; running it writes an identical PNG and verifies itself.
- **كيف / how:** python studio.py --image-code photo.jpg or python to_python.py img [out.py]; Studio 📤 button; holes joined even-odd by _bridge.
- **أرقام / params:** trace max_side 520; base64 lines of 100 chars; README reports a 900x900 ad -> 3,394 polygons, 0 differing pixels
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/to_python.py:1` · `kosif-studio/to_python.py:90` · `kosif-studio/scenes/5.py`

#### EXPL-81 · شرح دورة المياه ثنائي الأبعاد · 2D water-cycle explainer · 📦 بأمر تثبيت
- **ماذا / what:** 17 s SVG/GSAP explainer: dawn sunrise with title slam, evaporation vapour with arrows drawn upward, clouds snapping and darkening, camera push to the peak with rain, lightning and snow, river drawing to the sea, a golden loop ring through four stages.
- **كيف / how:** projects/water_cycle: M.drawPath ×9, M.flowDash, M.vapour, M.rain, M.flash, M.camera, M.grain, M.vignette
- **أرقام / params:** beats 0-2.7 / 2.8-6.4 / 6.2-9.4 / 9.5-12.8 / 12.4-15.1 / 15.2-17 s; palette #FFD166 #FFE8C2 #7FD4FF #5EC8FF #2A6F97 #0D1B2A
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/projects/water_cycle/index.html:152` · `kosif-studio/out/water_cycle.mp4` · `kosif-studio/tests/test_studio.py:629`

#### EXPL-82 · رسومات تقنية · Style: Tech blueprint (tech-blueprint) · 📦 بأمر تثبيت
- **ماذا / what:** Engineering-drawing look: thin cyan/white line art on a dark blue grid that draws itself, with dimension lines and callouts.
- **كيف / how:** SVG paths on a 24px grid; stroke-dashoffset draw-on at 900-1200 px/s, nodes pop with spring d14 s160, camera pans 700-1000ms cubic-bezier(.65,0,.35,1). Scaffold: python3 tools/kosif.py scaffold tech-blueprint <dir>.
- **أرقام / params:** stroke 3-4px; arrowheads 14-18px; zoom max 1.8
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `style:tech-blueprint` · `kosif-tool/playbooks/diagrams.md`

#### EXPL-83 · مخططات · Category: Diagrams · 📦 بأمر تثبيت
- **ماذا / what:** Capability family 'diagrams' (37 catalog entries) with a dedicated bilingual playbook of timings and recipes.
- **كيف / how:** Read playbooks/diagrams.md (visual grammar, motion mechanics, scene recipes, QA); build in starters/html-canvas or starters/remotion; filter catalog with python3 tools/kosif.py list --category diagrams.
- **أرقام / params:** <=7 nodes; stroke 3-4px; node pop spring d14 s160; edge 900-1200px/s; camera 700-1000ms; zoom<=1.8
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/playbooks/diagrams.md` · `kosif-tool/catalog/categories.json` · `kosif-tool/catalog/meta.json`

#### EXPL-84 · كود · Category: Code · 📦 بأمر تثبيت
- **ماذا / what:** Capability family 'code' (38 catalog entries) with a dedicated bilingual playbook of timings and recipes.
- **كيف / how:** Read playbooks/code.md (visual grammar, motion mechanics, scene recipes, QA); build in starters/html-canvas or starters/remotion; filter catalog with python3 tools/kosif.py list --category code.
- **أرقام / params:** mono 28-40px, <=14 lines; typing 25-45 cps; caret 530ms; frame budget <50ms; seeded noise
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/playbooks/code.md` · `kosif-tool/catalog/categories.json` · `kosif-tool/catalog/meta.json`

#### EXPL-85 · كتابة بتذبذب مزروع · Seeded typing animation · 📦 بأمر تثبيت
- **ماذا / what:** Character typing with jitter, punctuation pauses and blinking caret; long code pasted as block.
- **كيف / how:** Remotion Typed component: per-char delay (1/cps)×(0.8+random(`k${i}`)×0.4) + 0.3 s after [.,;:]; caret ▍.
- **أرقام / params:** 25–45 cps (default 35) ±20% jitter; 250–400 ms after punctuation; caret 530 ms; paste fade 200 ms
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/playbooks/code.md:25` · `kosif-tool/playbooks/code.md:55-67`

#### EXPL-86 · توليد أيقونات بخلفية شفافة · Transparent icon generation · 🔑 مفتاح/خدمة
- **ماذا / what:** Generate flat icons with alpha for explainers, themed by a shared palette.
- **كيف / how:** Request transparent background from the image model; if the PNG comes back opaque, remove near-white by threshold (Pillow) or use BiRefNet via rembg + onnxruntime for complex edges; batch with a template 'a flat icon of a {item}'; 1024 px square.
- **أرقام / params:** 1024 px; threshold or BiRefNet
- **الدليل / proof:** `kosif-atlas/skills/2657-figures/10115-transparent-icons`

#### EXPL-87 · مخططات ومحرر كود · Diagram and code-editor film categories · 🔑 مفتاح/خدمة
- **ماذا / what:** Claude-coded diagrams (3-5 labelled nodes appearing in order, drawn connectors with moving flow dots) and dark code editors (line numbers, LTR monospace typing token by token with palette syntax colours, result panel).
- **كيف / how:** FILM_CATS 'diagrams' and 'code'; templates concept, what-is, timeline, how-to, code-explain, dev-tool.
- **الدليل / proof:** `app/public/js/00_editor.js:2007` · `app/public/js/00_editor.js:1777`

#### EXPL-88 · فيديو شرح طلب الدمج البرمجي · PR-to-video code-change explainer · 🔑 مفتاح/خدمة
- **ماذا / what:** A GitHub PR (URL / owner/repo#N) becomes a changelog / feature-reveal / fix / refactor explainer: gh fetch of pr.json + diff.patch (paginated files), offline ingest to tokens/text/people, contributor avatars for a credits close, code-editorial design, frame workers, captions, render.
- **كيف / how:** node fetch-pr.mjs --pr <ref> --out-dir ./capture; node ingest.mjs --pr-json ... --diff ...; node fetch-people-avatars.mjs --people ...; then the shared narrative pipeline.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/pr-to-video/SKILL.md` · `kosif-one/vendor/hyperframes/skills/pr-to-video/scripts/fetch-pr.mjs` · `kosif-one/vendor/hyperframes/skills/pr-to-video/scripts/ingest.mjs`

#### EXPL-89 · تكامل: Manim MCP · Integration: Manim MCP · 🔑 مفتاح/خدمة
- **ماذا / what:** Catalogued skill/MCP/library (link only; not installed here).
- **كيف / how:** see official setup
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`

#### EXPL-90 · إثبات بصري بطيران الخلايا · Cell-flight visual proof · 👁 شوهد في فيديو
- **ماذا / what:** for each source cell centre, lerp to a target cell centre in the rotated hypotenuse grid, rotate to the hypotenuse angle, add hop = h*sin(pi t); stagger cells; counter = arrived count; glow square on 
- **كيف / how:** for each source cell centre, lerp to a target cell centre in the rotated hypotenuse grid, rotate to the hypotenuse angle, add hop = h*sin(pi t); stagger cells; counter = arrived count; glow square on completion
- **أرقام / params:** 25 cells, stagger ~120 ms, hop 20 px
- **الدليل / proof:** `style:chalkboard`

#### EXPL-91 · مقارنة نسب بكرات تصغر · Shrinking-sphere scale comparison · 👁 شوهد في فيديو
- **ماذا / what:** row of spheres sized by sqrt(value) (with min clamp for tiny), staggered pop-in right-to-left with arrows and % captions
- **أرقام / params:** 4 spheres, stagger 250 ms
- **الدليل / proof:** `style:infographic`

#### EXPL-92 · نقاط بيانات تطير على قوس منقط · Data packets along dotted arc · 👁 شوهد في فيديو
- **ماذا / what:** quadratic bezier between two projected world points; dashed stroke; 3-5 glowing dots offset along t with stagger
- **أرقام / params:** dash 4/6, dot r 4, ~1.5 s
- **الدليل / proof:** `style:isometric`

#### EXPL-93 · علم ينبثق وكارت ورقي متصل · Pop-up flag + pinned paper card · 👁 شوهد في فيديو
- **ماذا / what:** on arrival: flag scaleY 0->1 spring (~300 ms) with stamp SFX; card fades+slides 12px with shadow, dotted curved leader to flag; card shows city in Ruqaa, date in red, one fact line
- **أرقام / params:** card bg #efe3c4, border double 1px, shadow 0 8px 20px rgba(0,0,0,.25)
- **الدليل / proof:** `style:map-journey`

#### EXPL-94 · معاينة وكود ومعادلة جنبًا إلى جنب · Preview + code + formula triptych · 👁 شوهد في فيديو
- **ماذا / what:** left: framed canvas with ruler and red playhead; right: monospace code with orange literals; below: serif italic formula; playhead time drives both the shapes and a highlighted code line
- **أرقام / params:** playhead label 't = 1.97 s', mono 12-14 px
- **الدليل / proof:** `style:plotter`

#### EXPL-95 · مخطط عقد بإشارة متحركة · Node wire signal flow · 👁 شوهد في فيديو
- **ماذا / what:** boxes connected by orthogonal lines that draw on; an orange dot travels along the active wire; invalid route marked with an orange X
- **أرقام / params:** wire draw 500 ms, dot travel 800 ms
- **الدليل / proof:** `style:plotter`

#### EXPL-96 · محور متوهج بخطوط توصيل · Glowing hub with connector spokes · 👁 شوهد في فيديو
- **ماذا / what:** App icon in rounded square with orange bloom; SVG cubic curves draw (stroke-dashoffset) to 4 stat cards that then fade in and count
- **أرقام / params:** glow blur 30-40 px, line draw 400 ms, stagger 150 ms
- **الدليل / proof:** `style:pm-0xfemyn-e114d3`

#### EXPL-97 · بطاقتا مقارنة بعلامات صح وخطأ · Two-option trade-off cards · 👁 شوهد في فيديو
- **ماذا / what:** two cards side by side with coloured headers, rows with green check or black cross boxes, rotated stickers summarising each option, cost note below
- **أرقام / params:** rows stagger 120 ms
- **الدليل / proof:** `style:pm-0xnfrith-5be616`

#### EXPL-98 · صفحة كلمات كأشرطة تمتلئ · Known-words bar page · 👁 شوهد في فيديو
- **ماذا / what:** Represent text as rounded rectangles of word widths; fill them dark progressively to show comprehension; mark unknown word in accent
- **أرقام / params:** row fill 120-200 ms per row, bar height 8 px radius 4 px
- **الدليل / proof:** `style:pm-1stnoel-c20a89`

#### EXPL-99 · مخطط بحساب حي · Live math diagram · 👁 شوهد في فيديو
- **ماذا / what:** wireframe isometric box, highlighted vector, side panel of values computing then result counter
- **الدليل / proof:** `style:pm-adamdesgns-478d6d`

#### EXPL-100 · خريطة معرفة شعاعية · Radial knowledge graph · 👁 شوهد في فيديو
- **ماذا / what:** hero card at centre; satellite cards placed on an ellipse; lines draw from centre outward, tag pills sit on the lines; dot grid behind
- **أرقام / params:** 10 nodes, line draw 300 ms, stagger 50 ms
- **الدليل / proof:** `style:pm-agonaliu-466a8f`

#### EXPL-101 · بطاقات خطوات مرقمة · Numbered step cards · 👁 شوهد في فيديو
- **ماذا / what:** Eyebrow 'HOW IT WORKS' tracked caps; three white cards with yellow circular number badge, outline icon and bold label slide/fade in left-to-right
- **أرقام / params:** card 240x210 px, radius 16, stagger ~1.2-1.5 s
- **الدليل / proof:** `style:pm-alex-prompter-1ea044`

#### EXPL-102 · خطوات مرقمة · Numbered steps · 👁 شوهد في فيديو
- **ماذا / what:** cards with number badge connected by dashed line
- **الدليل / proof:** `style:pm-amitsingha89-150378`

#### EXPL-103 · مسار متوهج للتوجيه · Glowing route path · 👁 شوهد في فيديو
- **ماذا / what:** bezier from node to chosen target with stroke glow
- **أرقام / params:** 600 ms
- **الدليل / proof:** `style:pm-amol909s-27533e`

#### EXPL-104 · شبكة حسابات تتفرع · Fan-out avatar network · 👁 شوهد في فيديو
- **ماذا / what:** N coloured avatar squares spring out from a centre object along straight lines with stagger
- **أرقام / params:** N=5, stagger 120 ms, spring overshoot 1.1
- **الدليل / proof:** `style:pm-anthonyriera-9b1b2a`

#### EXPL-105 · مسار عشوائي · Random walk path · 👁 شوهد في فيديو
- **ماذا / what:** polyline random steps drawn progressively
- **الدليل / proof:** `style:pm-apoorvjain25-d24184`

#### EXPL-106 · تدفق أتمتة بعقد وخطوط · Automation node flow · 👁 شوهد في فيديو
- **ماذا / what:** Three cards (trigger, engine, result) connected by straight lines that draw left to right; status chips pop under each as data passes
- **أرقام / params:** line draw 300 ms each; chips pop 200 ms; engine card dark with live dot
- **الدليل / proof:** `style:pm-bizibeast-10f264`

#### EXPL-107 · منحنى توقيت حي · Live easing HUD · 👁 شوهد في فيديو
- **ماذا / what:** small cubic-bezier plot in corner with dot following current ease
- **الدليل / proof:** `style:pm-blue-clarity-ef56d0`

#### EXPL-108 · مخطط سلسلة إشارة بروابط موجية · Signal-chain diagram with wave links · 👁 شوهد في فيديو
- **ماذا / what:** row of outlined boxes (title + mono sub-label) connected by animated sine-wave segments; draw left to right, waves scroll to show flow; a larger waveform label above
- **أرقام / params:** box stroke 1 px yellow/green, wave amplitude 4 px, scroll 60 px/s
- **الدليل / proof:** `style:pm-blueoctopusai-dd17bd`

#### EXPL-109 · تضخيم مقياس لتوضيح فكرة · Exaggerated-scale visualisation · 👁 شوهد في فيديو
- **ماذا / what:** scale a subtle physical property (field crown) vertically ×N with a tint and label 'shown ×9.6' plus callout tags 'FLAT CHORD' vs 'CROWN'
- **أرقام / params:** scale ×5-10, tint teal 40%
- **الدليل / proof:** `style:pm-blueoctopusai-dd17bd`

#### EXPL-110 · تفرع منتج إلى عدة منصات · One-to-many marketplace branches · 👁 شوهد في فيديو
- **ماذا / what:** Glowing product node on the left; three bezier curves draw to stacked platform cards on the right with travelling light dots; each card shows a signal-bar meter that fills
- **أرقام / params:** curve draw 500 ms stagger 150 ms, dot travel 700 ms
- **الدليل / proof:** `style:pm-ceowinkz-7c776b`

#### EXPL-111 · مخطط ربط مركزي · Hub-spoke integration graph · 👁 شوهد في فيديو
- **ماذا / what:** center logo, lines draw to service pills
- **أرقام / params:** 600 ms each
- **الدليل / proof:** `style:pm-charlesmendez-73b6e4`

#### EXPL-112 · شطب القاعدة الخاطئة وعلامة صح · Strike-through wrong rule + checkmark · 👁 شوهد في فيديو
- **ماذا / what:** red line draws over 'linear = robotic', then blue 'ease in-out' with a drawn check
- **أرقام / params:** strike 250 ms, check 300 ms
- **الدليل / proof:** `style:pm-chatgptastra-0d95c7`

#### EXPL-113 · سباق منحنيات التسهيل · Easing comparison race · 👁 شوهد في فيديو
- **ماذا / what:** Draw cubic-bezier graph with handles; three balls on tracks animate linear vs ease-out vs custom simultaneously
- **أرقام / params:** 1 s loops
- **الدليل / proof:** `style:pm-crazyalphaaa-bc7e75`

#### EXPL-114 · طبقات شفافة متراكبة إيزومترية · Isometric translucent layer stack · 👁 شوهد في فيديو
- **ماذا / what:** CSS rotateX(55deg) rotateZ(-45deg) rounded plates, opacity gradient light→solid blue, stack with 18 px offset; top plate lifted with dashed outline; leader lines draw right then mono labels fade in
- **أرقام / params:** 6-7 plates, blue #1f7bf2, glow below
- **الدليل / proof:** `style:pm-ddryo-loos-300829`

#### EXPL-115 · خطوط تفرع ترسم من بطاقة إلى قائمة · Connector-line branch reveal · 👁 شوهد في فيديو
- **ماذا / what:** From a source card draw thin curved SVG paths to target rows using stroke-dashoffset, then fade the rows in staggered
- **أرقام / params:** stroke 1 px grey-blue, 400-500 ms per branch, 150 ms stagger
- **الدليل / proof:** `style:pm-elliot-garreffa-f334bc`

#### EXPL-116 · شريط مكدس الاستدعاء · Call-stack breadcrumb HUD · 👁 شوهد في فيديو
- **ماذا / what:** top bar of mono chips, each coloured per genre with pause icon; active chip filled with play icon; push/pop chips with slide
- **أرقام / params:** chip h 22px, mono 12px, push 200 ms
- **الدليل / proof:** `style:pm-emollick-8661a8`

#### EXPL-117 · خطوط توزيع بيانات · Data fan-out lines · 👁 شوهد في فيديو
- **ماذا / what:** code block left, bezier lines to chips with travelling dots
- **الدليل / proof:** `style:pm-ezshine-c90d73`

#### EXPL-118 · تعرّف على عناصر الصورة وفرزها · Photo object detection sort · 👁 شوهد في فيديو
- **ماذا / what:** overlay corner-bracket boxes on items in a photo, show 'identifying' status, then thumbnails fly into labelled bucket cards with counts
- **أرقام / params:** 4 buckets, fly 500 ms with ease-in-out
- **الدليل / proof:** `style:pm-gabrielbuzziv-4ff0c6`

#### EXPL-119 · سلسلة موارد بأسهم متقطعة · Resource chain diagram · 👁 شوهد في فيديو
- **ماذا / what:** circular icon nodes connected by dashed arrows that draw on left-to-right, labels under each
- **أرقام / params:** dash 6/6, 300 ms per link
- **الدليل / proof:** `style:pm-gigabit-million-16b3a0`

#### EXPL-120 · بطاقة أمر مع تظليل أحمر للكلمات الخاطئة · Prompt card with red problem highlights · 👁 شوهد في فيديو
- **ماذا / what:** dark rounded card (#3f3b37) with cream monospace text typed in; then red rectangles scale-X from 0 behind the faulty words, text turns light
- **أرقام / params:** type ~30 ms/char, highlight wipe 250 ms each, stagger 300 ms
- **الدليل / proof:** `style:pm-henkvaness-0e06af`

#### EXPL-121 · شرح منحنى التسارع · Easing graph explainer · 👁 شوهد في فيديو
- **ماذا / what:** axes (position/time) draw on, Bezier S-curve with handles draws, playhead line scrubs while a square moves on a track below in sync
- **أرقام / params:** cubic-bezier(.65,0,.35,1)
- **الدليل / proof:** `style:pm-himanshutwtxs-5f4b43`

#### EXPL-122 · طرفية تحديث بأمر واحد · Terminal one-command update · 👁 شوهد في فيديو
- **ماذا / what:** Dark terminal window prints log lines sequentially, final line in green as success
- **أرقام / params:** line every 120 ms, mono 12 px
- **الدليل / proof:** `style:pm-iammxfschr-d68f90`

#### EXPL-123 · محرر كود بجانب معاينة حية · Code editor + live preview split · 👁 شوهد في فيديو
- **ماذا / what:** Left pane types code char-by-char with syntax colours and line numbers; right pane shows the result reacting (sprite jumps when the jump() line completes); test checklist ticks below
- **أرقام / params:** ~25 chars/s; caret blink 500ms
- **الدليل / proof:** `style:pm-ibrahimwasim240-809370`

#### EXPL-124 · خطوات مرقمة مع شريط تقدم · Numbered step flow with stepper · 👁 شوهد في فيديو
- **ماذا / what:** big mono 01–04, headline with accent word, top 4-segment bar fills
- **الدليل / proof:** `style:pm-imthatcarlos-e04bfe`

#### EXPL-125 · افتتاحية طرفية تكتب كوداً · Terminal typewriter opener · 👁 شوهد في فيديو
- **ماذا / what:** dot-grid dark field, small label line, '>' prompt with code typed at fixed cadence and a block cursor, underline rule and a tiny return-key chip with tagline
- **أرقام / params:** ~30 ms/char
- **الدليل / proof:** `style:pm-influencer-seo-ce8c33`

#### EXPL-126 · خريطة ذهنية دائرية · Radial mind-map · 👁 شوهد في فيديو
- **ماذا / what:** central illustrated circle, 5 circular icon nodes around, arrows draw, labels under
- **أرقام / params:** stagger 120ms
- **الدليل / proof:** `style:pm-itisrazak-3ad902`

#### EXPL-127 · أسلاك إشارة · Signal wires · 👁 شوهد في فيديو
- **ماذا / what:** SVG bezier paths with glowing dots animating along length
- **أرقام / params:** dash offset, 1.2 s
- **الدليل / proof:** `style:pm-jayscambler-3f8889`

#### EXPL-128 · تحديد منقّط مع طمس · Dashed marquee blur · 👁 شوهد في فيديو
- **ماذا / what:** draw a dashed selection rectangle over part of a text/UI element, then apply backdrop blur inside it with a cursor nearby
- **أرقام / params:** dash 4/4 px, blur 12 px, 300 ms
- **الدليل / proof:** `style:pm-jhylee95-e1152f`

#### EXPL-129 · كود مجرد بأشرطة · Abstract code as pills · 👁 شوهد في فيديو
- **ماذا / what:** rounded rects of syntax colours + bracket glyphs on rows
- **أرقام / params:** radius 50%
- **الدليل / proof:** `style:pm-kamstudiolabs-c9bb28`

#### EXPL-130 · تمييز خطأ أحمر · Error highlight sweep · 👁 شوهد في فيديو
- **ماذا / what:** red band scaleX across line + squiggle draw
- **أرقام / params:** 0.6 s
- **الدليل / proof:** `style:pm-kamstudiolabs-c9bb28`

#### EXPL-131 · رقائق الرموز مع أرقامها · Token chips with ids · 👁 شوهد في فيديو
- **ماذا / what:** Split a phrase into tokens, render each as rounded pastel chip in mono with small grey id number beneath, pop in with stagger
- **أرقام / params:** radius 8px, stagger 90 ms, scale 0.8→1 back-out
- **الدليل / proof:** `style:pm-kloss-xyz-15182a`

#### EXPL-132 · حوار طرفية · Terminal typewriter dialogue · 👁 شوهد في فيديو
- **ماذا / what:** amber mono text typed with caret in bordered panel
- **أرقام / params:** 30 ms/char
- **الدليل / proof:** `style:pm-kloss-xyz-fe0c31`

#### EXPL-133 · أقواس الانتباه · Attention arcs · 👁 شوهد في فيديو
- **ماذا / what:** arcs from one word to others, weight=stroke width, highlight token
- **الدليل / proof:** `style:pm-kloss-xyz-fe0c31`

#### EXPL-134 · عرض الالتفاف بالبكسل · Pixel convolution demo · 👁 شوهد في فيديو
- **ماذا / what:** pixel digit, kernel square scanning, heatmap output
- **الدليل / proof:** `style:pm-kloss-xyz-fe0c31`

#### EXPL-135 · مخطط تكاملات مركزي · Hub-and-spoke integrations diagram · 👁 شوهد في فيديو
- **ماذا / what:** centre app icon, 8 labelled tool nodes around it; dashed connectors draw out from centre with a travelling dot
- **أرقام / params:** connectors draw 400 ms stagger 50 ms
- **الدليل / proof:** `style:pm-kmasiff-cc72cb`

#### EXPL-136 · تسميات مرتبطة بالأجزاء · 3D callout labels · 👁 شوهد في فيديو
- **ماذا / what:** project 3D points to screen, pill labels with leader line
- **الدليل / proof:** `style:pm-konstantinsaifo-96fc89`

#### EXPL-137 · خطوط توضيحية تشير لعناصر الواجهة · Callout leader lines to UI · 👁 شوهد في فيديو
- **ماذا / what:** from points on a rendered page, draw thin amber elbow lines outward to mono labels at the frame sides; draw-on 300 ms each, stagger 80 ms
- **أرقام / params:** 1 px amber, small square end-cap, label mono 10 px
- **الدليل / proof:** `style:pm-kyonax-on-tech-aabc1d`

#### EXPL-138 · شجرة عقد متتالية · Tree/AST node cascade · 👁 شوهد في فيديو
- **ماذا / what:** indented boxed nodes (document > heading > paragraph > codeBlock) appear one by one with elbow connectors drawn on, key:value metadata in mono next to each
- **أرقام / params:** stagger 120 ms, box border 1 px grey, label mono
- **الدليل / proof:** `style:pm-kyonax-on-tech-aabc1d`

#### EXPL-139 · محور مركزي بأذرع للتكاملات · Hub and spoke integrations · 👁 شوهد في فيديو
- **ماذا / what:** Central blob with gooey arms growing to labelled nodes (pill tags), small dots travelling along arms
- **أرقام / params:** 6-7 arms; stagger 80ms
- **الدليل / proof:** `style:pm-leadnotifi-e83f94`

#### EXPL-140 · خط زمني للعملية بأيقونات مرسومة · Process timeline with doodle icons · 👁 شوهد في فيديو
- **ماذا / what:** horizontal marker line draws, circular nodes pop at steps, hand-drawn icons (mic, music note, frame) and a dashed badge 'OK?' appear above, labels in handwriting below
- **أرقام / params:** node pop 200 ms back.out
- **الدليل / proof:** `style:pm-lemomo-ai-0d9cff`

#### EXPL-141 · منحنى نابض مرسوم بجانب النص · Spring curve graph with text · 👁 شوهد في فيديو
- **ماذا / what:** Plot the easing function in a small framed graph, a dot runs along it synced to the text animation using the same spring
- **أرقام / params:** spring(1, 100, 10, 0) style; graph 20% width
- **الدليل / proof:** `style:pm-levabashidze-2d713a`

#### EXPL-142 · طرفية تثبيت · Terminal install · 👁 شوهد في فيديو
- **ماذا / what:** dark rounded panel, typed command, check lines
- **الدليل / proof:** `style:pm-lexnlin-6161a6`

#### EXPL-143 · تحويل القاطع إلى مماس · Secant-to-tangent limit animation · 👁 شوهد في فيديو
- **ماذا / what:** ValueTracker dt from 2 → 0.001 (exponential ease); line through (a,f(a)) and (a+dt,f(a+dt)) redrawn via always_redraw; DecimalNumber shows dt and slope
- **أرقام / params:** dt 2→1→0.1→0.01→0.001, each step ~2-3 s, run_time per step with smooth
- **الدليل / proof:** `style:pm-linearuncle-5d2bae`

#### EXPL-144 · اشتقاق جبري بألوان دلالية · Colour-coded algebra derivation · 👁 شوهد في فيديو
- **ماذا / what:** MathTex with isolated substrings; colour terms that cancel in red, final result in green; TransformMatchingTex between lines
- **أرقام / params:** line spacing ~12% H; each line Write ~1.5 s
- **الدليل / proof:** `style:pm-linearuncle-5d2bae`

#### EXPL-145 · تأطير أجزاء المعادلة بشروح · Boxed formula annotation · 👁 شوهد في فيديو
- **ماذا / what:** SurroundingRectangle around numerator/denominator with small caption above/below in matching colour, Create ~0.6 s
- **أرقام / params:** stroke 2px, buff 0.08
- **الدليل / proof:** `style:pm-linearuncle-5d2bae`

#### EXPL-146 · شبكة ساعات للروتين · Clock-face routine grid · 👁 شوهد في فيديو
- **ماذا / what:** duplicate scene into grid to show monotony
- **الدليل / proof:** `style:pm-loicrambo-ad6830`

#### EXPL-147 · شجرة قرارات · Decision branch tree · 👁 شوهد في فيديو
- **ماذا / what:** faded options around, line draws to highlighted pill
- **الدليل / proof:** `style:pm-macrohou-33959d`

#### EXPL-148 · افتتاحية طرفية تترجم كودًا · Compile-terminal opener · 👁 شوهد في فيديو
- **ماذا / what:** Mono prompt typed per char, then 'compiling X.cpp [■■■■■] ok' rows whose block bars fill
- **أرقام / params:** typing 30 ms/char, bar fill 300 ms each, rows stagger 150 ms
- **الدليل / proof:** `style:pm-madhav-xo-f97f20`

#### EXPL-149 · رسم بدوائر فورييه · Fourier epicycle drawing · 👁 شوهد في فيديو
- **ماذا / what:** DFT of path, chain of rotating vectors, trail glow
- **الدليل / proof:** `style:pm-math-files-39c9d0`

#### EXPL-150 · تتبع الجيب · Unit-circle sine trace · 👁 شوهد في فيديو
- **ماذا / what:** point on circle projects to scrolling sine
- **الدليل / proof:** `style:pm-math-files-39c9d0`

#### EXPL-151 · عُقد تتصل بخطوط إلى شعار مركزي · Nodes wired to hub logo · 👁 شوهد في فيديو
- **ماذا / what:** three labels at top arc; lines stroke-draw from each to the centre (~300 ms staggered) then the hub logo pops with ring
- **أرقام / params:** line 1 px #4b6fd8
- **الدليل / proof:** `style:pm-maxalexweber-67688b`

#### EXPL-152 · إقلاع بسطر طرفية يُكتب · Terminal typewriter boot · 👁 شوهد في فيديو
- **ماذا / what:** mono 12 px dim text '> verb…' typed at ~40 ms/char with caret
- **أرقام / params:** colour #566992
- **الدليل / proof:** `style:pm-maxalexweber-67688b`

#### EXPL-153 · شرطات متدفقة على مسار · Flow dashes along path · 👁 شوهد في فيديو
- **ماذا / what:** animate dash offset along tube/curve; color codes power/data/heat
- **الدليل / proof:** `style:pm-mdaman010-e7226a`

#### EXPL-154 · تسميات بخطوط إشارة · Leader-line callouts · 👁 شوهد في فيديو
- **ماذا / what:** dot + line + label anchored to 3D point projected
- **الدليل / proof:** `style:pm-mdaman010-e7226a`

#### EXPL-155 · توصيل العقد · Node connector graph · 👁 شوهد في فيديو
- **ماذا / what:** pills connected by curved bezier lines with a travelling dot
- **الدليل / proof:** `style:pm-melvynx-6cde6c`

#### EXPL-156 · سحابة رقاقات كود عائمة · Floating code-chip cloud · 👁 شوهد في فيديو
- **ماذا / what:** 20-30 mono pills with random positions, slow sine drift 4-8 px, opacity 0.4-0.9 around hero text
- **الدليل / proof:** `style:pm-misbahsy-80eaec`

#### EXPL-157 · مخطط موزع ومحاور · Hub-and-spoke router graph · 👁 شوهد في فيديو
- **ماذا / what:** left inputs → central card → right list; connectors with moving dash offset, 80 ms stagger
- **الدليل / proof:** `style:pm-misbahsy-80eaec`

#### EXPL-158 · مسار الاحتياط · Failover path · 👁 شوهد في فيديو
- **ماذا / what:** request pill → diamond node; red failed branch then green success branch draws on 400 ms
- **الدليل / proof:** `style:pm-misbahsy-80eaec`

#### EXPL-159 · أقواس زوايا للتركيز · Corner crop brackets · 👁 شوهد في فيديو
- **ماذا / what:** four L-shaped 1 px marks placed at a region's corners, animate from larger rect to target rect
- **أرقام / params:** arm 12 px, ease-out 300 ms
- **الدليل / proof:** `style:pm-moguzbulbul-6311b6`

#### EXPL-160 · أسهم قياس بملاحظات · Annotated dimension arrows · 👁 شوهد في فيديو
- **ماذا / what:** line with end ticks/arrowhead plus tiny mono uppercase label describing the change
- **أرقام / params:** mono 9px tracking .1em
- **الدليل / proof:** `style:pm-moguzbulbul-6311b6`

#### EXPL-161 · سلسلة خطوات معاملة · Transaction step chain · 👁 شوهد في فيديو
- **ماذا / what:** Dashed container labelled 'one transaction'; slightly rotated paper chips appear and straighten into a vertical chain joined by arrows
- **أرقام / params:** chip rot ±6°→0, stagger 0.6 s
- **الدليل / proof:** `style:pm-nikolajankovic-ce4ff4`

#### EXPL-162 · شجرة تفرّع اتصال · Branching connection tree · 👁 شوهد في فيديو
- **ماذا / what:** Address chip at top, curved hand-drawn lines draw-on to N boxes below, focus box circled with yellow highlighter
- **أرقام / params:** draw-on 0.8 s each
- **الدليل / proof:** `style:pm-nikolajankovic-ce4ff4`

#### EXPL-163 · خريطة نظام بفقاعات · Bubble ecosystem map · 👁 شوهد في فيديو
- **ماذا / what:** Scatter hand-drawn ellipses with protocol names and small empty blobs, connected by dotted paths; tiny boat icon traverses
- **أرقام / params:** ~9 named + 12 empty blobs
- **الدليل / proof:** `style:pm-nikolajankovic-ce4ff4`

#### EXPL-164 · سجل أحداث ملوّن · Colour-coded event log · 👁 شوهد في فيديو
- **ماذا / what:** Monospace table of last 6 events: time, id, status (green/red), remaining; new rows push old ones up
- **أرقام / params:** 6 rows; columns aligned by fixed char widths
- **الدليل / proof:** `style:pm-parkerrex-1a54fe`

#### EXPL-165 · مخطط شلال · Cascade flow diagram · 👁 شوهد في فيديو
- **ماذا / what:** stacked boxes with arrows revealing sequentially
- **الدليل / proof:** `style:pm-polydao-7a572b`

#### EXPL-166 · مخطط محور وأذرع · Hub and spoke diagram · 👁 شوهد في فيديو
- **ماذا / what:** centre icon, labels around, thin lines
- **الدليل / proof:** `style:pm-prasad-pilla-2c0cba`

#### EXPL-167 · لوحة قياسات حية بأرقام تتغير · Live telemetry HUD · 👁 شوهد في فيديو
- **ماذا / what:** Two mono panels with symbol label + right-aligned tabular value updated from a physics model each frame; switch values to ∞ / 'lost' at the horizon
- **أرقام / params:** amber labels #e0a060, white values, 1 px rule; 2 decimals
- **الدليل / proof:** `style:pm-rebutonepress-810f78`

#### EXPL-168 · افتتاح بسطر طرفية · Terminal cold open · 👁 شوهد في فيديو
- **ماذا / what:** Mono '$ command --' typed with block cursor on black
- **أرقام / params:** 50 ms/char
- **الدليل / proof:** `style:pm-robvjourney-ce3e1a`

#### EXPL-169 · مؤشر خطوات · Six-step stepper · 👁 شوهد في فيديو
- **ماذا / what:** circles linked by line; active ring, done = filled check, line fills
- **الدليل / proof:** `style:pm-ror-fly-9950f1`

#### EXPL-170 · قائمة مكوّنات بعلامات صح مرسومة · Checklist with drawn ticks and pointer · 👁 شوهد في فيديو
- **ماذا / what:** rows of circle + amount + name; upcoming rows at 45% opacity, an arrow glyph slides to the active row, on completion stroke-dash draw a check mark inside the circle
- **أرقام / params:** tick draw ~250 ms, arrow move ~300 ms easeOutCubic
- **الدليل / proof:** `style:pm-sarut0bisasuke-cefa43`

#### EXPL-171 · تسمية بخط مؤشر · Leader-line callout · 👁 شوهد في فيديو
- **ماذا / what:** project 3D anchor to screen, draw 1px line + bold label + grey sub, fade 300 ms
- **الدليل / proof:** `style:pm-sayan-shanky-f850d8`

#### EXPL-172 · شبكة شركاء · Avatar network bloom · 👁 شوهد في فيديو
- **ماذا / what:** avatars pop around centre logo with green value pills
- **الدليل / proof:** `style:pm-steventey-0d20e4`

#### EXPL-173 · رسم توضيحي يبنى مع الصوت · Synced diagram build · 👁 شوهد في فيديو
- **ماذا / what:** Each labelled arrow/icon fades+draws at its word timestamp
- **أرقام / params:** stagger by words.json
- **الدليل / proof:** `style:pm-sudo-kiran-6609ed`

#### EXPL-174 · مخطط عقد بنقاط متدفقة · Node pill diagram with flowing dots · 👁 شوهد في فيديو
- **ماذا / what:** SVG bezier connectors draw-on 500 ms, dot travelling along path
- **الدليل / proof:** `style:pm-sudo-kiran-b055de`

#### EXPL-175 · مصفوفة كتلية بالتهشير تتفرّع · Hatched block matrix refinement · 👁 شوهد في فيديو
- **ماذا / what:** draw a hatched square, arrow, then the same square split into 2x2 blocks with diagonal blocks cross-hatched in a new colour, arrow, then nested sub-blocks — shows recursive structure
- **أرقام / params:** 3 stages left->right, hatch spacing ~8 px
- **الدليل / proof:** `style:pm-tak3sh8-be5012`

#### EXPL-176 · شبكة عُقد بحواف موجبة وسالبة · Graph network with signed edges · 👁 شوهد في فيديو
- **ماذا / what:** place N nodes on a circle, each with an up/down arrow glyph; draw every pair edge one by one coloured by sign
- **أرقام / params:** N=7-8, edge draw ~80 ms stagger
- **الدليل / proof:** `style:pm-tak3sh8-be5012`

#### EXPL-177 · شجرة هرمية مع خطوط مستويات · Ultrametric tree with level guides · 👁 شوهد في فيديو
- **ماذا / what:** binary tree drawn root-down, dashed horizontal level lines labelled in different colours, leaf dots appear last with a caption
- **أرقام / params:** 3 levels, 8 leaves
- **الدليل / proof:** `style:pm-tak3sh8-be5012`

#### EXPL-178 · بطاقة كود JSON تُكتب · Typed JSON prompt card · 👁 شوهد في فيديو
- **ماذا / what:** Thin lime-bordered box with pink filename tab; mono text types with block cursor; small tag chips float around it
- **أرقام / params:** ~30 chars/s; chips drift 10px
- **الدليل / proof:** `style:pm-techhalla-7acbc2`

#### EXPL-179 · مخطط معماري يرسم نفسه · Architecture flow draw-on · 👁 شوهد في فيديو
- **ماذا / what:** nodes as outlined pills, connector lines draw 300ms then dot pulses travel along
- **الدليل / proof:** `style:pm-techyoutbe-945b56`

#### EXPL-180 · مخطط مقارنة التسهيل · Easing comparison diagram · 👁 شوهد في فيديو
- **ماذا / what:** Plot a cubic-bezier curve with handles and a dot travelling along it; beside it three horizontal tracks where dots move with linear, ease-out and custom eases simultaneously, with % readouts; headline
- **كيف / how:** Plot a cubic-bezier curve with handles and a dot travelling along it; beside it three horizontal tracks where dots move with linear, ease-out and custom eases simultaneously, with % readouts; headline 'TIMING IS EVERYTHING.'
- **أرقام / params:** cubic-bezier(0.85,0,0.15,1), 1.2 s loop
- **الدليل / proof:** `style:pm-teslachartz-c58b32`

#### EXPL-181 · خطوط تعارض بين الملاحظات · Conflict connector lines · 👁 شوهد في فيديو
- **ماذا / what:** SVG lines from cards to node with ≠ badge
- **الدليل / proof:** `style:pm-theviableedge-9065be`

#### EXPL-182 · جولة شجرة ملفات · Terminal file tree walkthrough · 👁 شوهد في فيديو
- **ماذا / what:** dark panel, highlight bar steps rows
- **الدليل / proof:** `style:pm-theviableedge-9065be`

#### EXPL-183 · شجرة انشقاق · Party split tree · 👁 شوهد في فيديو
- **ماذا / what:** pills joined by elbow connectors
- **الدليل / proof:** `style:pm-triglyceee-bd5b08`

#### EXPL-184 · لوحة JSON · JSON response panel · 👁 شوهد في فيديو
- **ماذا / what:** syntax coloured lines appear + 200 OK pill
- **الدليل / proof:** `style:pm-tstfully-0aa6b4`

#### EXPL-185 · طرفية مع بطاقة تعريف · Terminal + definition card split · 👁 شوهد في فيديو
- **ماذا / what:** macOS-style dark terminal left 60%, typed lines 30–40 ms/char; right card with big mono command in accent + one-line meaning
- **الدليل / proof:** `style:pm-yunn260414-60d996`

#### EXPL-186 · ثلاث لوحات تشبيه · Analogy panel triptych · 👁 شوهد في فيديو
- **ماذا / what:** 3 bordered cards each own accent colour, icon+title+caption, active one glows
- **الدليل / proof:** `style:pm-yunn260414-60d996`

#### EXPL-187 · رسم شجرة الفروع · Branch graph draw-on · 👁 شوهد في فيديو
- **ماذا / what:** nodes as rings on a line, branch curves down with spring, label pill on HEAD
- **الدليل / proof:** `style:pm-yunn260414-60d996`

#### EXPL-188 · نظام البطاقات للفيديو الشارح · Explainer card system for essays · 📄 موصوف
- **ماذا / what:** A coherent card kit: full-screen chapter cards, principle cards with boxes/arrows whose spoken element turns red, before/after tables with a red circle on the spoken row, keyword pops, numbered titles.
- **كيف / how:** Chapter card: pastel ground #EFE6F7, yellow #FFD400 heavy type with #1A1A1A outline at 6% of glyph height, glyphs 14% of frame height, 3-4 s, 1-2 stickers. Principle card: white ground, labels 3.5% height #1A1A1A, spoken element turns #E53935 0.3 s after it is said. Table: row count x 2 s. Keyword pop: #FFD400 + outline, 1-3 words, 6% height, 0.8-2 s. Numbered title: 8% height, 2-3 s. Author as HTML/CSS/JS timeline in the kosif scaffold, preview with node tools/render_html.cjs --preview, render …
- **أرقام / params:** #EFE6F7 #FFD400 #1A1A1A #E53935; 14%/8%/6%/3.5% heights; highlight delay 0.3 s
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2461-davinciresolve-style-essay/SKILL.md`

#### EXPL-189 · لقطة الوثيقة مع قلم التظليل · Source-document highlighter shot · 📄 موصوف
- **ماذا / what:** Show the original source document unchanged with a translucent yellow highlighter sweeping across the sentence being spoken, held 3-5 s.
- **كيف / how:** Screenshot or render the document page, animate a semi-transparent yellow rectangle (mix-blend multiply) growing along the line timed to words.json; for Arabic sweep right-to-left.
- **أرقام / params:** 3-5 s; yellow translucent
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2461-davinciresolve-style-essay/SKILL.md`

#### EXPL-190 · قواعد تركيب مخطط الشرح · Explainer diagram composition rules · 📄 موصوف
- **ماذا / what:** Reduce a system to 3-7 role-level components and at most 5 steps; choose left-to-right or top-to-bottom reading with the fewest crossings; circled step numbers only when order matters; normal flow in neutral lines, only problems/errors/bottlenecks in red, yellow reserved for the single hero; in a se…
- **كيف / how:** Build as SVG in the HTML engine with a fixed layout JSON reused across scenes, animating highlight changes between frames.
- **أرقام / params:** 3-7 components; <=5 steps; 1 yellow hero
- **الدليل / proof:** `kosif-atlas/skills/1098-akbun-presentation/2476-akbun-presentation-visual/SKILL.md`

#### EXPL-191 · MG-081/083 دائرة تتحول لدورة وكرة تنقل الفكرة · MG-081/083 Cycle diagram and travelling token · 📄 موصوف
- **ماذا / what:** Four icons spread on a circle and arrows grow between them in order (MG-081); a small ball travels three stations and changes colour by each stage's function (MG-083).
- **كيف / how:** MG-081: 0-1 title, 1-7 stages, 7-10 full cycle; direction readable even muted. MG-083: 0-1 enter, 1-7 stations, 7-9 result; Bezier path with stops and markers; colour change must mean something. SVG paths + dashoffset arrows.
- **أرقام / params:** 10 s / 9 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-explainers.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### EXPL-192 · MG-084 خطأ ثم تصحيح بصري · MG-084 Mistake then visual correction · 📄 موصوف
- **ماذا / what:** A wrong example freezes, gets ringed, slides aside and the correct version appears.
- **كيف / how:** 0-2 example, 2-3 alert, 3-6 fix, 6-8 summary; freeze frame, masks, sequential comparison; illustrate dangerous actions instead of filming them.
- **أرقام / params:** 8 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-explainers.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### EXPL-193 · MG-087 مسار قرار مرئي · MG-087 Visual decision path · 📄 موصوف
- **ماذا / what:** A question appears, two coloured branches extend and an example case travels to its outcome.
- **كيف / how:** 0-2 question, 2-5 branches, 5-8 example path, 8-10 result; shape lines + text cards with the chosen branch highlighted; high-stakes advice needs expert review.
- **أرقام / params:** 10 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-explainers.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### EXPL-194 · MG-088 مقارنة سرعة دون تضليل · MG-088 Fair speed comparison · 📄 موصوف
- **ماذا / what:** Two objects cover the same distance next to a visible clock.
- **كيف / how:** 0-1 conditions, 1-6 motion, 6-8 result; identical paths and fixed distances with timers; any change in time or distance between the two is stated.
- **أرقام / params:** 8 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-explainers.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### EXPL-195 · MG-090 معادلة تتكون خطوة خطوة · MG-090 Equation built step by step (bidi-safe) · 📄 موصوف
- **ماذا / what:** Givens appear, then the operator, then the result, with the term being explained tinted; constant spacing between separate text layers. Inside Arabic narration the numbers and symbols must keep their direction - never mirror the equation. Pair with math-exposition habits: define each symbol before u…
- **كيف / how:** 0-2 givens, 2-5 operation, 5-8 result, 8-10 read. Render math with KaTeX/MathJax SVG (CDN) or pre-rendered SVG; wrap formulas in an LTR isolate (dir=ltr / unicode-bidi:isolate) inside RTL captions; reveal terms by opacity/colour keys.
- **أرقام / params:** 10 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-explainers.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md` · `kosif-atlas/skills/994-write-math/2278-write-math/SKILL.md`

#### EXPL-196 · إطار شرح تعليمي أحادي اللون · Learning-mono explainer frame · 📄 موصوف
- **ماذا / what:** Minimal black-and-white 16:9 study frames: white background, title #111111 at top-left, body #333333, annotations #767676, unfilled 1-2 px boxes, dashed grey grouping boxes, thin arrows with small triangular heads and 2-4-word labels; one red accent #D93025 (second accent blue #1A73E8 only when the …
- **كيف / how:** Build natively as SVG/HTML (no image model, so text is exact), animate arrows/labels with dashoffset and stagger in KOSIF render_html.cjs (/home/user/kosif-tool/tools/render_html.cjs: HTML/SVG + CSS/WAAPI or window.__kosif.seek(t) -> Playwright frame capture -> ffmpeg); narration carries the long explanation.
- **أرقام / params:** accent <5%; margin 5-7%; 3-5 points; title <=40 chars; labels <=4 words
- **الدليل / proof:** `kosif-atlas/skills/1094-akbun-draw/2418-akbun-draw-learning-mono/SKILL.md`

#### EXPL-197 · نافذة كود مشروحة بأسهم وتعليقات · Annotated code-window figure · 📄 موصوف
- **ماذا / what:** Code explainer look: rounded dark editor window #2A2622 with three traffic-light dots; white handwritten-marker title, no logos; syntax colours keys #E06C9F, strings #E5A86B, numbers #A78BFA, punctuation light grey; at most 3 highlights as green outline boxes #7EE787 with hand-drawn yellow curved ar…
- **كيف / how:** Render in HTML with pre-tokenised spans or Prism/highlight.js (CDN) and animate: window in -> lines reveal -> box draws -> arrow draws -> callout pops, in KOSIF render_html.cjs (/home/user/kosif-tool/tools/render_html.cjs: HTML/SVG + CSS/WAAPI or window.__kosif.seek(t) -> Playwright frame capture -> ffmpeg); text stays exact unlike image models.
- **أرقام / params:** 4:3; 4-12 lines; <=3 callouts; 60/35 split
- **الدليل / proof:** `kosif-atlas/skills/1094-akbun-draw/2426-akbun-generateimage-code/SKILL.md`

#### EXPL-198 · حدود الإغلاق البصري للأيقونات المختصرة · Closure limits for minimal icons · 📄 موصوف
- **ماذا / what:** Implied or minimal shapes stop working below about 24 px, for novice or cross-cultural audiences and in high-stakes information; pair minimal icons with labels, make critical marks explicit and test at the smallest rendered size (e.g. 9:16 phone).
- **كيف / how:** Render a contact sheet at final scale and inspect.
- **أرقام / params:** <~24 px
- **الدليل / proof:** `kosif-atlas/skills/1503-universal-design-principles/3811-closure-completion-cost/SKILL.md`

#### EXPL-199 · طبقة اقتباس مقال · Article excerpt overlay · 📄 موصوف
- **ماذا / what:** Quote a source on top of running footage: paper panel #FAFAF6 with #171717 text, 75-90% width, ≥5% margins, body glyph 3-4% H; in 0.15-0.3 s, hold for reading, out 0.15-0.25 s; optional red underline #D92D20 (stroke 0.25-0.4% H, 10-20% glyph gap), ellipse callout with 20-35% padding, yellow highligh…
- **كيف / how:** HTML/GSAP or Remotion layer above V1; Resolve Fusion on overlay track
- **أرقام / params:** see what
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2430-akbun-davinciresolve-article-overlay/SKILL.md`

#### EXPL-200 · مواصفات بطاقات الشرح · Explainer card specs · 📄 موصوف
- **ماذا / what:** Chapter card: full-screen pastel (#EFE6F7-like) with bold #FFD400 title outlined #1A1A1A (outline 6% of glyph), glyph 14% H, 3-4 s; principle card: white, boxes/arrows/labels 3.5% H, element turns #E53935 0.3 s after it is spoken; before/after table 3 columns with red circle on spoken row; numbered …
- **كيف / how:** HyperFrames HTML per card (data-width/height/fps match timeline) -> render mp4 -> place on GFX track
- **أرقام / params:** see what
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2461-davinciresolve-style-essay/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2458-davinciresolve-gfx-hyperframes/SKILL.md`

#### EXPL-201 · خط ثابت العرض للكود · Monospace for code · 📄 موصوف
- **ماذا / what:** Code on screen reads best in monospace with generous leading and tinted background.
- **كيف / how:** JetBrains Mono/Geist Mono, line-height 1.6, background tint.
- **أرقام / params:** lh 1.6
- **الدليل / proof:** `kosif-atlas/skills/1503-universal-design-principles/3825-legibility-contrast-and-spacing/SKILL.md` · `kosif-atlas/skills/2722-vercel/10536-geist/SKILL.md`

#### EXPL-202 · SVG بوحدة الملليمتر · mm-unit SVG with matching viewBox · 📄 موصوف
- **ماذا / what:** Set width/height in mm with an equal viewBox so every coordinate and font-size is a mm length.
- **كيف / how:** Hand SVG or Python string; font-size pt*25.4/72 for mm.
- **أرقام / params:** 7pt = 2.47mm
- **الدليل / proof:** `kosif-atlas/skills/2657-figures/10113-svg-figure`

#### EXPL-203 · مفردات الأنماط البصرية · Visual pattern vocabulary for explainers · 📄 موصوف
- **ماذا / what:** Fan-out, convergence, tree, cycle, cloud, assembly line (chaos->order), side-by-side, gap/break, lines-as-structure timelines.
- **كيف / how:** Map concept to pattern; timelines = line + 10-20px dots + free labels; animate in reading order.
- **أرقام / params:** dots 10-20px
- **الدليل / proof:** `kosif-atlas/skills/2790-work/11181-draw-excalidraw`

#### EXPL-204 · لوحة JSON Canvas · JSON Canvas board layout · 📄 موصوف
- **ماذا / what:** Open spec for spatial boards: nodes (text, file, link, group) with x,y,width,height and edges with sides/arrows.
- **كيف / how:** Write .canvas JSON; can serve as a storyboard/mind-map source that a script turns into animated SVG camera moves.
- **الدليل / proof:** `kosif-atlas/skills/3013-obsidian-second-brain/12869-json-canvas`

#### EXPL-205 · قواعد الرسم التخطيطي التحريري · Editorial diagram grammar · 📄 موصوف
- **ماذا / what:** Minimal, legible explainer diagrams: delete first, one or two accented nodes, strict connector rules.
- **كيف / how:** Target density 4/10, more than ~9 nodes means two diagrams; accent on <=2 nodes; right-angle rounded elbows (no diagonals); 6-10 px gap between arrow label and line; no overlapping connectors; >=12 px between attach points on one edge; no connector behind a non-endpoint box; arrows drawn before boxes; 4 px grid. Palette roles paper #f5f5f5, ink #2d3142, muted #4f5d75, soft #7a8399, accent #eb6c36, link #2e5aa8.
- **أرقام / params:** density 4/10; <=9 nodes; label gap 6-10 px; attach spacing >=12 px; 4 px grid
- **الدليل / proof:** `kosif-atlas/skills/345-visuals/1242-html-diagram/SKILL.md` · `kosif-atlas/skills/345-visuals/1242-html-diagram/references/svg-primitives.md`

#### EXPL-206 · اختيار نوع المخطط التوضيحي · Diagram type chooser · 📄 موصوف
- **ماذا / what:** Eight diagram types cover most explainers; if a table says it better, use the table.
- **كيف / how:** Branching decisions -> flowchart; messages over time between actors -> sequence; components and links -> architecture; dated events -> timeline; parent-child -> tree; cross-team handoffs -> swimlane; two-axis positioning -> quadrant; reinforcing cycle -> loop. Pick the dominant axis when two fit.
- **أرقام / params:** 8 types
- **الدليل / proof:** `kosif-atlas/skills/345-visuals/1242-html-diagram/SKILL.md` · `kosif-atlas/skills/2212-majestic-misc/8300-show-me/SKILL.md`

#### EXPL-207 · ألوان دلالية لمخططات البنية · Architecture diagram semantic colors · 📄 موصوف
- **ماذا / what:** Dark-theme system diagrams where color encodes component type and dashed rectangles mark boundaries.
- **كيف / how:** Frontend cyan #22d3ee, backend emerald #34d399, data violet #a78bfa, cloud amber #fbbf24, security rose #fb7185, message bus orange #fb923c, external slate #94a3b8; regions dashed 8,4 amber rx 12; security groups dashed 4,4. Ideas only (copyleft-folder source).
- **أرقام / params:** dash 8,4 / 4,4; rx 12
- **الدليل / proof:** `kosif-atlas/skills/x4919-visual-gen/x20317-architecture-diagram/SKILL.md`

#### EXPL-208 · قواعد الدقة والوضوح لشرح الأطفال · Science-accuracy and legibility rules for kids' explainers · 📄 موصوف
- **ماذا / what:** Never show wrong science (vapour rises from the sea, clouds form by cooling, rain falls on land, water returns to the sea); one main motion per stage; no flashing; text >= 40 px at 1080p and contrast >= 4.5:1.
- **كيف / how:** Check against DESIGN.md 'What NOT to Do' before rendering.
- **الدليل / proof:** `kosif-one/projects/water-cycle-animation/DESIGN.md`

#### EXPL-209 · المسطح التعليمي · Flat Explainer style · 📄 موصوف
- **ماذا / what:** Light flat palette with one orange highlight for current stage; one main motion per stage; self-drawing strokes.
- **كيف / how:** Copy style sheet section into DESIGN.md, then build via claude-animation-studio render(t).
- **أرقام / params:** bg #EAF7FF; highlight #FF7A00; Cairo 800/700; text 40px+; pathLength=1 dashoffset
- **الدليل / proof:** `100-superskills/skills/trend-animation-styles/references/styles.md`

#### EXPL-210 · شرح تعليمي بخطوات سببية · Causal-step explainer · 📄 موصوف
- **ماذا / what:** Concept split into 3-6 causal steps, one sentence each, fixed camera, one mover per stage, stage bar at bottom, fact-check every claim.
- **كيف / how:** Narration 2.5 words/s; on-screen text shorter than spoken; test via imaginary student.
- **أرقام / params:** 3-6 steps; 2.5 w/s; 40px+; 4.5:1
- **الدليل / proof:** `100-superskills/skills/explainer-edu-animation/SKILL.md`

#### EXPL-211 · شرح وحلّ خطوة بخطوة بالتحقق · Math & Science Tutor · 📄 موصوف
- **ماذا / what:** Owner-built skill "Math & Science Tutor" (own words): workflow guidance for math & science tutor; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill math-science-tutor (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/math-science-tutor/SKILL.md`

#### EXPL-212 · تصميم أنظمة قبل البناء · Software Architecture & ADRs · 📄 موصوف
- **ماذا / what:** Owner-built skill "Software Architecture & ADRs" (own words): workflow guidance for software architecture & adrs; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill software-architecture-adr (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/software-architecture-adr/SKILL.md`

#### EXPL-213 · لوحات SVG مصغرة · SVG thumbnail storyboard frames · 📄 موصوف
- **ماذا / what:** Simple rect/circle SVG thumbs showing composition per shot.
- **كيف / how:** write thumbs.svg
- **الدليل / proof:** `100-superskills/skills/storyboard-shotlist/SKILL.md:24`

#### EXPL-214 · ألوان أدوار العقد · Role-coloured diagram nodes · 📄 موصوف
- **ماذا / what:** Source, processing, storage, external role colours with measured contrast.
- **كيف / how:** Mermaid classDef
- **الدليل / proof:** `100-superskills/skills/diagrams-mermaid-architecture/SKILL.md:24`

#### EXPL-215 · شرح التوأم الإنشائي · Structural twin six-beat explainer · 📄 موصوف
- **ماذا / what:** Pin-jointed 2D/3D truss solved linear-elastically, then filmed as SHAPE→JOINT→LOAD→BREAK→SWAP→RANK with measured units and on-screen 'illustrative' labels.
- **كيف / how:** python scripts/kmotion.py structural --sample --out twin.json --swap AB --area 0.0002 --fracture-scale 3.2; twinview twin.json --out twin.html; K3S.trussOverlay in 3D.
- **أرقام / params:** bunny: 35 nodes, 109 members, chosen felt values; first limit 2.38× at earL_out-crown; removal at 3.0× -> mechanism; swap 2.6× area -> limit 3.77×, bottleneck moves to earL_front-crown
- **الدليل / proof:** `kosif-studio/motion/references/STRUCTURAL_TWIN.md`

#### EXPL-216 · طباعة الكود على الشاشة · On-screen code typography · 📄 موصوف
- **ماذا / what:** Real monospace, limited lines, one syntax theme, highlight 1–3 lines, plausible correct code.
- **أرقام / params:** 28–40 px at 1080 width; ≤ 14 lines
- **الدليل / proof:** `kosif-tool/playbooks/code.md:15-16`

#### EXPL-217 · تمييز سطر الكود · Code line highlight · 📄 موصوف
- **ماذا / what:** Band slides behind key line, others dim.
- **أرقام / params:** 250 ms ease-out cubic; others 50%
- **الدليل / proof:** `kosif-tool/playbooks/code.md:26`

#### EXPL-218 · تمرير بأسطر كاملة · Whole-line scrolling · 📄 موصوف
- **ماذا / what:** Scroll code by whole lines.
- **أرقام / params:** 200–300 ms per step ease-in-out
- **الدليل / proof:** `kosif-tool/playbooks/code.md:27`

#### EXPL-219 · وصفة أمر ونتيجة · Command and result recipe · 📄 موصوف
- **ماذا / what:** Terminal scales in, command types, enter flash, output in blocks, success highlight with push.
- **أرقام / params:** 0–300 ms scale from 0.96; 300–1300 type 35 cps; 1300–1600 caret/enter; 1600–2400 3 output blocks; 2400–3000 highlight + 3% push
- **الدليل / proof:** `kosif-tool/playbooks/code.md:35-43`

#### EXPL-220 · كشف الفرق · Diff reveal · 📄 موصوف
- **ماذا / what:** Removed lines collapse red, added expand green, unchanged slide.
- **أرقام / params:** removed 250 ms; added 300 ms
- **الدليل / proof:** `kosif-tool/playbooks/code.md:49`

#### EXPL-221 · قواعد العقد والروابط · Diagram node/edge grammar · 📄 موصوف
- **ماذا / what:** One shape family, one stroke width, straight or one-bend orthogonal edges, curves only for feedback loops.
- **أرقام / params:** radius 16–24 px; stroke 3–4 px; arrowheads 14–18 px; node labels 32–44 px; edge labels 24–28 px
- **الدليل / proof:** `kosif-tool/playbooks/diagrams.md:15-20`

#### EXPL-222 · حد سبع عقد · Seven-node chapter limit · 📄 موصوف
- **ماذا / what:** At most 7 nodes visible; bigger systems in chapters with camera moves.
- **أرقام / params:** ≤ 7 nodes
- **الدليل / proof:** `kosif-tool/playbooks/diagrams.md:16`

#### EXPL-223 · حالات العقد · Active/visited/future node states · 📄 موصوف
- **ماذا / what:** Active node accent, visited ink at 70%, future not drawn.
- **أرقام / params:** visited 70%
- **الدليل / proof:** `kosif-tool/playbooks/diagrams.md:19`

#### EXPL-224 · الترتيب السببي · Causal reveal order · 📄 موصوف
- **ماذا / what:** Node appears, outgoing edge draws, next node pops when pen arrives.
- **الدليل / proof:** `kosif-tool/playbooks/diagrams.md:26`

#### EXPL-225 · نبضة بيانات على الرابط · Data pulse along edge · 📄 موصوف
- **ماذا / what:** Dot travels edge path repeatedly while flow is described.
- **كيف / how:** getPointAtLength.
- **أرقام / params:** dot 10–14 px; 600–900 ms in-out; 400 ms gaps
- **الدليل / proof:** `kosif-tool/playbooks/diagrams.md:29`

#### EXPL-226 · رأس التشغيل للخط الزمني · Timeline playhead · 📄 موصوف
- **ماذا / what:** Constant-speed playhead; markers pop on arrival, labels after; current era band.
- **أرقام / params:** axis draw 600 ms; marker pop 200 ms; label +120 ms
- **الدليل / proof:** `kosif-tool/playbooks/diagrams.md:31` · `kosif-tool/playbooks/diagrams.md:50`

#### EXPL-227 · وصفة عملية من ثلاث خطوات · Three-step process recipe · 📄 موصوف
- **ماذا / what:** Node-edge-node chain with dimming and final data pulse.
- **أرقام / params:** nodes pop 0/900/1800 ms spring 14/160; edges 300–900, 1200–1800; hold 2100–3600 with pulse
- **الدليل / proof:** `kosif-tool/playbooks/diagrams.md:37-46`

#### EXPL-228 · التكبير على مكوّن · Zoom into component · 📄 موصوف
- **ماذا / what:** Whole system hold, camera to one node, node opens into sub-diagram.
- **أرقام / params:** 2 s hold; scale 1.5 in 900 ms; crossfade 300 ms
- **الدليل / proof:** `kosif-tool/playbooks/diagrams.md:48`

#### EXPL-229 · مخطط قبل وبعد · Before/after diagram · 📄 موصوف
- **ماذا / what:** Duplicate diagram; after copy redraws only changed edges in accent.
- **الدليل / proof:** `kosif-tool/playbooks/diagrams.md:52`

#### EXPL-230 · عكس المخطط للعربية · Mirrored RTL diagrams · 📄 موصوف
- **ماذا / what:** First node on right, arrows point left, arrowhead markers mirrored; Latin ids isolated.
- **الدليل / proof:** `kosif-tool/playbooks/diagrams.md:18` · `kosif-tool/playbooks/diagrams.md:71`

#### EXPL-231 · ترتيب بناء المخطط · Diagram build-up reveal order · 💡 فكرة
- **ماذا / what:** Reveal diagram nodes, then connectors drawing on, then labels, following reading order (RTL for Arabic).
- **كيف / how:** Use layer order from svg-primitives; stagger 0.08-0.15s per node.
- **أرقام / params:** stagger 0.08-0.15s
- **الدليل / proof:** `kosif-atlas/skills/2657-figures/10114-svg-primitives` · `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md`

#### EXPL-232 · نموذج مجرة الأدلة · Evidence galaxy graph model · 💡 فكرة
- **ماذا / what:** Four-node chain account -> evidence -> standard -> finding meant to drive a node-link 'galaxy' visual of audit traceability.
- **كيف / how:** Data object with nodes[] and links[] plus traceEvidence(id) helper; no renderer exists.
- **أرقام / params:** 4 nodes, 3 links
- **الدليل / proof:** `kosif-audit-studio/cinema/evidenceGalaxy.js`

#### EXPL-233 · مسار توريد · Supply route with traveling box · 💡 فكرة
- **ماذا / what:** Route line draws through nodes; icon travels at constant speed and pauses at each node which pops.
- **كيف / how:** SVG path + getPointAtLength.
- **أرقام / params:** draw 1200 ms; node pop 150 ms; pause 200 ms
- **الدليل / proof:** `style:pm-ceowinkz-7c776b`

#### EXPL-234 · شجرة ملفات إلى أعمدة · Folder tree to bar chart · 💡 فكرة
- **ماذا / what:** Nested folder lines extrude into bars of line counts from the real repo.
- **كيف / how:** Data from repo (cloc) → bars counting up.
- **أرقام / params:** 600 ms count
- **الدليل / proof:** `style:pm-danilowm-d3720d`

#### EXPL-235 · بطاقات استدعاء الأدوات · Tool-call cards montage · 💡 فكرة
- **ماذا / what:** Agent tool events (read/search/edit/test/error) as cards snapping on beats with file-tree pulses.
- **كيف / how:** Cards enter (0.22,1,0.36,1) 420 ms; exit (0.4,0,1,1) 260 ms.
- **أرقام / params:** ≥900 ms on screen; ≤3 stacked
- **الدليل / proof:** `style:pm-jake11moran-a269c4`

#### EXPL-236 · مسح الفرق ونقاط الاختبار · Diff wipe + test dots · 💡 فكرة
- **ماذا / what:** Green wipe over red diff, test dots fill one by one, bracket burst.
- **كيف / how:** Clip wipe.
- **الدليل / proof:** `style:pm-jake11moran-a269c4`

#### EXPL-237 · خط زمني بتحريك جانبي · Lateral dolly timeline · 💡 فكرة
- **ماذا / what:** One continuous lateral camera along a track, slowing near dense clusters.
- **كيف / how:** cubic-bezier(0.4,0,0.2,1) per segment.
- **أرقام / params:** 30% speed in clusters
- **الدليل / proof:** `style:pm-kloss-xyz-fe0c31`

#### EXPL-238 · بطاقات المعالم · Milestone card rise with micro-anim · 💡 فكرة
- **ماذا / what:** Cards rise from marker; SVG illustration completes micro-animation.
- **كيف / how:** spring damping 20.
- **أرقام / params:** 400 ms, 40 px; micro 1-1.5 s
- **الدليل / proof:** `style:pm-kloss-xyz-fe0c31`

#### EXPL-239 · شرح زجاج اللف · Spin-glass overlap matrix explainer · 💡 فكرة
- **ماذا / what:** Matrix uniform -> nested Parisi blocks -> tree.
- **أرقام / params:** camera 800 ms easeInOutQuad, <=5 moves
- **الدليل / proof:** `style:pm-tak3sh8-be5012`

#### EXPL-240 · تسميات بخط قائد · Leader-line feature labels · 💡 فكرة
- **ماذا / what:** 1 px line draws 250 ms; text +150 ms; 2-4 words
- **أرقام / params:** shadow blur 40 px 8%
- **الدليل / proof:** `style:pm-techyoutbe-945b56`
