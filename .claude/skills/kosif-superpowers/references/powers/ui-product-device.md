# الواجهات والمنتجات والأجهزة — UI, product & devices

> فصل مُجمَّع آليًا من 448 ملاحظة حصاد (مستودعات KOSIF + أطلس المهارات + 253 فيديو مرجعي)، مدموجة إلى **446 قدرة** مرتبة من الأقوى دليلًا. لم يُحرَّر يدويًا بعد — تحقّق من الدليل قبل الادعاء.
> Auto-compiled chapter: 446 powers deduplicated by name from 448 harvested atoms; strongest evidence first.

**الحالة:** ✅ مُثبت هنا 6 · 🟢 جاهز 27 · 📦 بأمر تثبيت 122 · 🔑 مفتاح/خدمة 9 · 👁 شوهد في فيديو 207 · 📄 موصوف 58 · 💡 فكرة 17

#### UI-01 · تسجيل صفحة بخطوات مبرمجة · Scripted page recording steps · ✅ مُثبت هنا
- **ماذا / what:** Drive a page with a JSON steps file (wait, waitFor selector/text/js, click with gliding cursor, tap, drag with hold, hover, held keys, typing, wheel scroll over time, goto, captions) and record it in real time.
- **كيف / how:** Write own Playwright script (playwright 1.56 + Chromium installed) mirroring the step grammar; captions -> captions.vtt. The atlas record-page.mjs is reference only (needs puppeteer-core; do not run unreviewed).
- **أرقام / params:** settle 1.5s before recording; click glide 450ms; type 70ms/key; caption 3s default; step timeout 20s; max 600s; phone = 360x640 page at 3x
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3903-video/references/RECORD.md` · `kosif-atlas/skills/1511-homie/3903-video/scripts/record-page.mjs` · `kosif-atlas/skills/1511-homie/3903-video/references/examples/site-walkthrough.json`

#### UI-02 · مؤشر اصطناعي وحلقة ضغط · Synthetic cursor and press ring · ✅ مُثبت هنا
- **ماذا / what:** Draw a small arrow and a click ring inside the page so they appear in captured frames; the arrow glides with ease-in-out and first appears from a short offset; the ring scales out and fades.
- **كيف / how:** Inject a fixed-position div; glide with easeInOutQuad via requestAnimationFrame; ring via element.animate keyframes; real mouse follows in steps so hover styles fire.
- **أرقام / params:** ring scale 0.45->1.25, opacity 1->0, 420ms ease-out; first approach from (-140, +90)px; glide 450ms
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3903-video/scripts/record-page.mjs` · `kosif-atlas/skills/1412-agent-browser/3350-agent-browser/references/video-recording.md`

#### UI-03 · تفاعلات الضغط والمرور الدقيقة · Press and hover micro-interactions · ✅ مُثبت هنا
- **ماذا / what:** Buttons press down and shrink slightly, lift on hover, and inline icons nudge in the reading direction; metric cards lift and tilt their icon.
- **كيف / how:** active: translateY(1px) scale(.985), svg scale(.92); hover (pointer:fine): translateY(-1px); inline-end icon translateX(-3px), inline-start 2px; icon-action rotate(-7deg) scale(1.06); metric hover -2px + icon rotate(-4deg) scale(1.06).
- **أرقام / params:** button transitions 150ms ease-out on color, background, border, shadow, transform, opacity only
- **الدليل / proof:** `kosif-audit-pro/app/globals.css:215` · `kosif-audit-pro/app/globals.css:223` · `kosif-audit-pro/app/globals.css:1256`

#### UI-04 · مشغّل HTML مستقل بشريط تقديم وحركة مخفّضة · Standalone HTML player with seek and reduced-motion · ✅ مُثبت هنا
- **ماذا / what:** The SVG short ships as an offline web page with play/pause, restart, a 0–12 s range slider with 0.01 s steps, a readout, MP4 download link and prefers-reduced-motion respect; ?capture hides chrome.
- **كيف / how:** build.cjs templates an Arabic RTL page; rAF tick advances current by min(dt,0.1 s) and auto-stops at 12 s; window.render(t) clamps 0–12; window.setPlaying(bool).
- **أرقام / params:** theme #060d17 / #08121c, focus ring #ffb769, accent #71e5d2
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/build.cjs:6` · `100-superskills/skills/kosif-montage-motion/scripts/projects/midnight_cat/player-test.cjs:1`

#### UI-05 · تطبيق ويب عربي مع اختبارات · Arabic-first RTL web app pattern with e2e checks · ✅ مُثبت هنا
- **ماذا / what:** Dependency-free RTL/LTR app with light/dark themes, artifact db storage, PDF/CSV/XLSX export, ZATCA QR, and e2e tests including no sideways scroll at 390 px.
- **كيف / how:** node --test tests/core.test.mjs (15 pass here); node tests/e2e.mjs in Edge.
- **أرقام / params:** 390 px phone check; 14 screens
- **الدليل / proof:** `kosif-one/tools/kosif-web/docs/05-architecture.md` · `kosif-one/tools/kosif-web/docs/06-final-report.md` · `kosif-one/tools/kosif-web/tests/core.test.mjs`

#### UI-06 · شريط التقدم · Progress bar · ✅ مُثبت هنا
- **ماذا / what:** 14 px accent bar grows across the bottom proportional to t/duration.
- **كيف / how:** #progress width=(t/DURATION*100)%
- **أرقام / params:** height 14 px, #7ee8d2
- **الدليل / proof:** `kosif-tool/starters/html-canvas/index.html:46` · `kosif-tool/starters/html-canvas/index.html:211`

#### UI-07 · بطاقة مائلة ثلاثية الأبعاد بلمعان · 3D tilt card with sheen · 🟢 جاهز
- **ماذا / what:** A card rotates slightly toward the pointer in perspective with a diagonal sheen; considered a tired default if used as the main idea.
- **كيف / how:** transform: perspective(1000px) rotateX/rotateY from pointer; ::before linear-gradient sheen opacity 0->1.
- **أرقام / params:** hover rotateX 5deg rotateY -5deg 0.5s ease-out-expo; JS tilt +-10deg; sheen rgba(255,255,255,0.1)
- **الدليل / proof:** `kosif-atlas/skills/3438-ux-design/14124-top-design/references/animation-patterns.md` · `kosif-atlas/skills/880-superloopy/1944-superloopy-slides/animation-patterns.md` · `kosif-atlas/skills/342-kernel/1223-frontend/reference/component-sources.md`

#### UI-08 · جدول ردود الفعل الدقيقة · Press/hover/toggle/shake micro-feedback table · 🟢 جاهز
- **ماذا / what:** Exact feedback motions for UI moments that appear in product demos: press, hover, toggle, accordion, toast, drawer, skeleton, success check, error shake, arrival bounce.
- **كيف / how:** CSS transitions or Framer Motion; the shake is keyframes on x.
- **أرقام / params:** press scale 0.97-0.98 in 50-100ms ease-out; hover scale 1.02; toggle 150-250ms; expand 200-300ms; fade 150-300ms; drawer 200-400ms (in 300/out 250); modal 250ms scale .95->1 (out 200ms); skeleton->content 200-400ms; check draw 300-500ms; shake x [0,-10,10,-10,10,0] 0.4s; bounce spring 200-400ms; car…
- **الدليل / proof:** `kosif-atlas/skills/3438-ux-design/14121-microinteractions/references/feedback-patterns.md` · `kosif-atlas/skills/3529-ui-design/14308-interaction-design` · `kosif-atlas/skills/3529-ui-design/14308-interaction-design/references/microinteraction-patterns.md`

#### UI-09 · شريط تقدم التمرير بنابض · Scroll progress bar with spring · 🟢 جاهز
- **ماذا / what:** A top bar whose width tracks reading progress smoothed by a spring.
- **كيف / how:** Framer Motion useScroll -> useSpring -> scaleX; or CSS animation-timeline: scroll().
- **أرقام / params:** spring stiffness 100, damping 30
- **الدليل / proof:** `kosif-atlas/skills/3529-ui-design/14308-interaction-design/references/scroll-animations.md`

#### UI-10 · تسجيل صفحة بسكريبت خطوات · Scripted page recording · 🟢 جاهز
- **ماذا / what:** A steps file drives a real page in a headless browser (click, tap, drag, hover, key, type, scroll, goto, wait, waitFor) with optional caption per step, a visible cursor and press rings; frames the page did not repaint are held and counted, not interpolated; warn under 20 fps.
- **كيف / how:** Implement with Playwright (available here) recording video or per-frame screenshots, write captions.vtt from step times, then cut it like any capture.
- **أرقام / params:** warn <20 fps
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3903-video/SKILL.md` · `kosif-atlas/skills/1511-homie/3903-video/references/RECORD.md`

#### UI-11 · تبديل الوضع الداكن المحفوظ · Persistent dark-mode toggle · 🟢 جاهز
- **ماذا / what:** Theme is an attribute on the root element, saved with workspace state in localStorage and restored on first animation frame.
- **كيف / how:** pro: document.documentElement.dataset.theme = dark|light inside setState; studio: :root[data-theme=dark].
- **أرقام / params:** storage schema 1; restore inside requestAnimationFrame
- **الدليل / proof:** `kosif-audit-pro/components/kosif/workspace.tsx:240` · `kosif-audit-pro/components/kosif/workspace.tsx:406`

#### UI-12 · مؤشر العنصر النشط في الشريط · Rail active indicator bar · 🟢 جاهز
- **ماذا / what:** Thin bar grows from 20% to full height on the active nav item; mobile bottom nav uses a top bar growing horizontally; the icon lifts slightly.
- **كيف / how:** ::after 3px bar, transform scaleY(0.2)->1 spring, opacity fast; mobile ::before 3px scaleX .25->1.
- **أرقام / params:** opacity 160ms ease-cinematic; transform 260ms spring; icon translateX(-2px) scale(1.04) / translateY(-2px) scale(1.06)
- **الدليل / proof:** `kosif-audit-pro/app/globals.css:527` · `kosif-audit-pro/app/globals.css:2765`

#### UI-13 · دوران أيقونة تبديل الثيم · Theme-toggle icon orbit · 🟢 جاهز
- **ماذا / what:** Sun/moon icon spins in from 75 degrees and grows when the theme flips.
- **كيف / how:** keyframe kosif-theme-orbit on .theme-toggle svg, transform-origin center.
- **أرقام / params:** 260ms spring; rotate 75deg scale .72 opacity .4 -> 0deg/1/1
- **الدليل / proof:** `kosif-audit-pro/app/globals.css:403` · `kosif-audit-pro/app/globals.css:429`

#### UI-14 · ظهور الأيقونة المرن · Icon pop-in · 🟢 جاهز
- **ماذا / what:** Hero action icon tile pops in with rotation settling to zero.
- **كيف / how:** keyframe kosif-action-icon on 64px tile.
- **أرقام / params:** 460ms spring, delay 260ms; translate 8px, scale .82, rotate 6deg -> 0
- **الدليل / proof:** `kosif-audit-pro/app/globals.css:1159` · `kosif-audit-pro/app/globals.css:1281`

#### UI-15 · ظهور شارة القرار · Decision result badge pop · 🟢 جاهز
- **ماذا / what:** Accept/reject confirmation line pops in with a small spring scale.
- **كيف / how:** keyframe kosif-decision-result.
- **أرقام / params:** 260ms spring; translate 5px, scale .92 -> 1
- **الدليل / proof:** `kosif-audit-pro/app/globals.css:1573`

#### UI-16 · إبراز الهدف عند الانتقال · Anchor-target spotlight · 🟢 جاهز
- **ماذا / what:** When a gate row is navigated to by URL hash (:target) it gets a tinted background, outline ring and a settle animation.
- **كيف / how:** :target / :focus-visible rule + keyframe kosif-gate-spotlight; scroll-margin-block-start 92px.
- **أرقام / params:** 720ms ease-cinematic; opacity .72, 5px, scale .992 -> 1; outline 3px ring 28%
- **الدليل / proof:** `kosif-audit-pro/app/globals.css:1940` · `kosif-audit-pro/app/globals.css:1955`

#### UI-17 · نقطة حالة بهالة · Status dot with halo · 🟢 جاهز
- **ماذا / what:** 8-9px dot coloured by state with a soft 4px halo ring.
- **كيف / how:** ::before circle; box-shadow 0 0 0 4px soft colour.
- **أرقام / params:** verified teal, attention amber, default muted; studio #54d89c with rgba(84,216,156,.12) halo
- **الدليل / proof:** `kosif-audit-pro/app/globals.css:855` · `kosif-audit-studio/styles.css:116`

#### UI-18 · حصر المرور على المؤشر الدقيق · Pointer-aware hover gating · 🟢 جاهز
- **ماذا / what:** Hover lifts and sheens only apply on devices with real hover and a fine pointer; touch targets stay >=44px.
- **كيف / how:** @media (hover: hover) and (pointer: fine) { ... }; @media (pointer: coarse) min-block-size 42/38px.
- **أرقام / params:** touch min 44px
- **الدليل / proof:** `kosif-audit-pro/app/globals.css:223` · `kosif-audit-pro/patch/kosif-v17.css`

#### UI-19 · بطاقة مؤشر بحافة ملوّنة · KPI tile with accent edge · 🟢 جاهز
- **ماذا / what:** White tile on mist ground, soft shadow, a 4px tone-coloured edge on the reading side, ring 'of N', and a lift on hover for tiles that open something.
- **كيف / how:** surfaces.css :root[data-look=kosif] .sk-kpi etc.; .skk4 cards with SKCharts.ring.
- **أرقام / params:** edge 4px; radius --sk-r-l 18px
- **الدليل / proof:** `kosif-earth-ci-fork/ui/ds/surfaces.css` · `kosif-earth-ci-fork/docs/design/KOSIF-LUXE.md`

#### UI-20 · معمارية الثيمات: الشكل × الوضع × العلامة · Look x theme x brand token architecture + theme studio · 🟢 جاهز
- **ماذا / what:** One token set re-skinned by html[data-look] (14 looks), [data-theme] light/dark and [data-brand] variants, plus a studio that overlays font, accent, corner radius, text scale and high-contrast as inline tokens; screens never hard-code colour.
- **كيف / how:** LOOKS list (22 entries incl. night pairs and auto) with 4-swatch previews; RADII sharp 4/6/8 or round 12/16/22; --sk-zoom scale; data-contrast; density compact.
- **أرقام / params:** looks: kosif, kosif-night, cobalt(+night), navygold(+night), najd(+night), heritage(+night), executive, audit, midnight, notebook, aurora(+night), vivid(+night), oasis(+night), graphite, onyx, auto
- **الدليل / proof:** `kosif-earth-ci-fork/ui/layouts/shell.js:29` · `kosif-earth-ci-fork/ui/ds/tokens.css` · `kosif-earth-ci-fork/docs/rebuild/DESIGN_SYSTEM.md`

#### UI-21 · شريط بطل لوحة القيادة · Dashboard hero band (video + WebGL + title) · 🟢 جاهز
- **ماذا / what:** A 190px hero band stacking a looping brand clip, the crystal-world canvas fading in on top, and the company name, hidden on non-today tabs.
- **كيف / how:** .skc-world: banner.webp poster background, <video muted loop playsinline preload=none data-src=dashboard.mp4> opacity .85, canvas opacity 0 -> 1 over 1.4s, mount density .6 seed 20261004; title 26px/800, eyebrow 11.5px .14em.
- **أرقام / params:** height 190px (150 on phones)
- **الدليل / proof:** `kosif-earth-ci-fork/ui/features/command-center.js:19` · `kosif-earth-ci-fork/ui/features/luxe-screens.css:7`

#### UI-22 · مؤشر الواجهة والنقطة المتتبعة · UI cursor / tracking-dot accents · 🟢 جاهز
- **ماذا / what:** Optional editorial accents: UI cursors with micro click, starbursts, tracking dot; a cursor and a screen icon exist in the icon set.
- **كيف / how:** Use icon 'cursor'/'screen' as hero, mention cursor micro-click in motion prompt.
- **الدليل / proof:** `fastify-motion-bro/docs/VIRAL-EDITORIAL-DNA.md:24` · `fastify-motion-bro/scripts/viral-editorial.mjs:65` · `fastify-motion-bro/web/editorial.js:20,25`

#### UI-23 · ثيم واجهة الاستوديو · Studio UI theme · 🟢 جاهز
- **ماذا / what:** Dark rounded-panel web UI with lime action buttons and responsive stack under 780 px.
- **كيف / how:** web/styles.css.
- **أرقام / params:** bg #0a0d17, text #eef3ff, panels #121829/#151c2d, border #293247, accent #d3f76a, muted #91a4c5/#aabbd8, status #8ccfc9; radius 20 px; breakpoint 780 px
- **الدليل / proof:** `fastify-motion-bro/web/styles.css`

#### UI-24 · مؤشر فأرة بفيزياء · Cursor with physics · 🟢 جاهز
- **ماذا / what:** An SVG arrow cursor moving along a Hermite path through timed stops, with press feedback on click.
- **كيف / how:** c=MOTION.cursor(stage,{size,fill,stroke}); MOTION.moveCursor(tl,c,[{t,x,y},...],{hold:[t...]}); MOTION.press(tl,c,at,{target,down}).
- **أرقام / params:** size 28 px (h x1.22); drop-shadow 0 6px 8px .28; press scale .88 over 4 f, back in 8 f; target .97 over 4 f / 10 f
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:404` · `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:414` · `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:432`

#### UI-25 · قرص قياس · Measuring stage disc (HUD floor) · 🟢 جاهز
- **ماذا / what:** Shader disc with grid, rings, 36 ticks and a scan sweep, plus a contact shadow.
- **كيف / how:** const d=K3S.stageDisc({radius, color, shadow}); d.userData.mat.uniforms.uScan.value = 0..1.
- **أرقام / params:** radius .32 m; colour #9dffb4; rings at .985 and .62; shadow opacity .42
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/shape-kit.js:343`

#### UI-26 · واجهة لوحة القياس · Instrument-panel HUD frame · 🟢 جاهز
- **ماذا / what:** DOM HUD around the 3D picture: title strip with stage chip and clock, timeline bar strip, side notes, three animated chart panels, frame border.
- **كيف / how:** const h=K3.hud(root, W, H, {title, subtitle, accent, ink, paper, panels, font, seed}); h.update(t, camera, {stage, side, duration}).
- **أرقام / params:** accent #a8ff3c; ink #0f1512; paper #f4f2ec; top 8.5% H, bottom 20% H; bars W/7; mono font IBM Plex Mono/Consolas
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/lab-kit.js:207`

#### UI-27 · المراجعة: سحب وتحجيم العناصر على الإطار · Review: drag-move and corner-resize on the frame · 🟢 جاهز
- **ماذا / what:** In Edit mode (E) the video pauses; clicking an element selects it, dragging moves it and dragging a corner scales it uniformly from the opposite corner; values are % of the frame and saved automatically as path→value edits.
- **كيف / how:** overlay pointer handlers in the review page; edits stored as '<id>.@box' = [x,y,w,h] (one decimal); a 14 px grab radius for corner handles nw/ne/sw/se; numeric Scale %/X/Y fields (scale step 5, x/y step 0.5).
- **أرقام / params:** box [x,y,w,h] in % of frame; uniform scale ≥ 0.1
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:600` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:734`

#### UI-28 · المراجعة: اختصارات لوحة المفاتيح · Review: keyboard transport (works on Arabic keyboards) · 🟢 جاهز
- **ماذا / what:** Space play/pause, ←/→ one frame, Shift+←/→ one second, [ and ] previous/next scene, E edit mode, N note mode, Esc back to preview; uses physical key codes so it still works when the keyboard layout is Arabic.
- **كيف / how:** keydown handler on ev.code (KeyE, KeyN, BracketLeft/Right); speed buttons ½×, 1×, 2×; loop-scene toggle.
- **أرقام / params:** frame step = 1/fps; speeds 0.5/1/2
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:954` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:320`

#### UI-29 · التعديل المباشر والتراجع والاختصارات · Direct manipulation, undo/redo and shortcuts · 🟢 جاهز
- **ماذا / what:** Drag a visible layer on the preview to move it; 60-step undo/redo; Space play, ←/→ one frame (1/24 s), Ctrl/⌘+Z undo, Ctrl/⌘+Shift+Z redo, Delete removes the selection; fullscreen preview.
- **كيف / how:** pointer handlers on the canvas; transaction()/history(); keydown handler.
- **أرقام / params:** undo depth 60
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:159` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:167` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:170`

#### UI-30 · مؤشر ماوس واقعي · Physics cursor with Hermite path and press · 🟢 جاهز
- **ماذا / what:** A drawn arrow cursor that travels through timed stops on a Hermite curve (zero velocity at holds) and clicks with a press and target dip.
- **كيف / how:** c=MOTION.cursor(stage,{size,fill}); MOTION.moveCursor(tl,c,[{t,x,y}...],{hold}); MOTION.press(tl,c,at,{target,down}).
- **أرقام / params:** size 28 px, drop shadow 0 6 8 .28; travel 36-48 f, arcs 15-25%; press scale 0.88 over 4 f, recover 8 f; target 0.97
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:404` · `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:426` · `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:432`

#### UI-31 · واجهة قياس بشروحات مسقطة · Instrument-panel HUD with projected callouts · 🟢 جاهز
- **ماذا / what:** Title strip, stage tag, clock, bar strip, bottom chart panels and callouts projected from 3D anchors framing the picture.
- **كيف / how:** hud = K3.hud(root, W, H, {title, subtitle, accent, ink, paper, font}); hud.addCallout({anchor, label, title, text, side}); hud.update(t, camera, state).
- **أرقام / params:** accent #a8ff3c, ink #0f1512, paper #f4f2ec; IBM Plex Mono; top 8.5% H, bottom 20% H
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/lab-kit.js:207`

#### UI-32 · هاتف 2.5D على Canvas · Canvas 2.5D phone (drawPhone) · 🟢 جاهز
- **ماذا / what:** 2D canvas fakes yaw by cos(yaw) width squash + slight shear; shadow, clip, screen canvas, island, glare gradient.
- **كيف / how:** ctx.transform(cos(rad), sin(rad)*0.12, 0, 1, 0, 0); roundRect clip; drawImage(screenCanvas).
- **أرقام / params:** PHONE 420×900 r 60 bezel 12; shadowBlur 90; valid below 28° yaw
- **الدليل / proof:** `kosif-tool/playbooks/phone.md:146-179`

#### UI-33 · واجهة منتج على Canvas · Canvas product-UI draw(t) · 🟢 جاهز
- **ماذا / what:** Seek-mode canvas with screen arrival, card stagger, button press and arc cursor.
- **كيف / how:** render_html --mode seek --fps 30 --seed 7.
- **أرقام / params:** colours #0b0d12 bg, #161a23 panel, #1f2430 cards, #19c37d button
- **الدليل / proof:** `kosif-tool/playbooks/product-ui.md:163-203`

#### UI-34 · تحويل موقع إلى فيديو · Website-to-video capture workflow · 📦 بأمر تثبيت
- **ماذا / what:** Capture a site's assets, design tokens and screenshots, then script, storyboard, voice and build a composition from them.
- **كيف / how:** Steps: capture -> design -> script -> storyboard -> VO -> build -> validate; reuse captured Lottie JSON, videos and fonts; mix techniques per tone (high impact: per-word type + velocity cuts + counters; premium: variable font + Lottie + slow cuts).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/SKILL.md` · `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md`

#### UI-35 · زر مغناطيسي · Magnetic button / card · 📦 بأمر تثبيت
- **ماذا / what:** Interactive elements follow the pointer by a fraction of its offset from their centre and spring back on leave.
- **كيف / how:** On move: tween x,y = offset*factor; on leave: elastic return. In video, drive with the synthetic cursor path.
- **أرقام / params:** button factor 0.3, 0.3s power2.out; return 0.5s elastic.out(1,0.5); cards factor 0.1
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/3438-ux-design/14124-top-design/references/animation-patterns.md` · `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion`

#### UI-36 · تسجيل المتصفح مع مؤشر ولوحة لقطات · Browser recording CLI with cursor and contact sheet · 📦 بأمر تثبيت
- **ماذا / what:** Record the active tab to webm/mp4 at 1-60 fps with an animated pointer overlay and an automatic contact sheet.
- **كيف / how:** agent-browser record start demo.webm --cursor --contact-sheet --fps 60; needs agent-browser install + ffmpeg (libvpx/libx264).
- **أرقام / params:** default 30 fps; 60 for motion studies; 1-15 for long timelines
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/1412-agent-browser/3350-agent-browser` · `kosif-atlas/skills/1412-agent-browser/3350-agent-browser/references/video-recording.md`

#### UI-37 · تسجيل سطح المكتب مع طبقات علوية · Desktop recording with compositor overlays · 📦 بأمر تثبيت
- **ماذا / what:** On Wayland (wlroots) record the desktop with wf-recorder and show title cards, lower-thirds, watermark, countdown, highlight and fade overlays rendered by the compositor so no post edit is needed.
- **كيف / how:** wf-recorder -f out.mp4 -r 60 [--audio]; gtk4-layer-shell overlay daemon; not usable in this headless container.
- **أرقام / params:** overlay types text/lower-third/watermark/countdown/highlight/fade; auto-hide duration e.g. 5s; title bg rgba(0,0,0,0.7) font 64
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2759-charly-selkies/10912-wf-recorder` · `kosif-atlas/skills/2734-charly-check/10677-wl-overlay` · `kosif-atlas/skills/2734-charly-check/10674-record`

#### UI-38 · من إطار فيجما إلى كود وحركة · Figma frame -> code/motion handoff · 📦 بأمر تثبيت
- **ماذا / what:** Pull node structure, fills, strokes, radii, shadows, typography, auto-layout spacing, variables per mode and Dev Mode snippets for a frame, then rebuild it as HTML/CSS layers ready to animate.
- **كيف / how:** Parse URL (file key after /design/ or /file/; node-id 123-456 == 123:456); auto-layout -> flexbox; RGBA floats 0-1 -> hex; REST export /v1/images/:key?ids=..&format=png&scale=2 or plugin exportAsync. Needs Figma token/desktop MCP (external service).
- **أرقام / params:** scale 2 PNG export; variables per light/dark mode
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/1381-figma/3252-figma-implementing` · `kosif-atlas/skills/1381-figma/3252-figma-implementing/references/figma-mcp-tools.md` · `kosif-atlas/skills/1381-figma/3253-figma-setup`

#### UI-39 · تسجيل تبويب المتصفح · Browser tab screen recording · 📦 بأمر تثبيت
- **ماذا / what:** Capture a Chrome tab to MP4/WebM with timestamped caption cues for tutorial/demo footage.
- **كيف / how:** Chrome extension + node bridge (record.js list/start/caption/stop); here Playwright's recordVideo or ffmpeg x11grab are the in-container alternatives
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2354-power-platform/9079-record-screen/SKILL.md`

#### UI-40 · فيديو تعليمي من ملف YAML · YAML-defined tutorial video · 📦 بأمر تثبيت
- **ماذا / what:** Describe slides/screencast steps + narration in YAML, validate, then render with TTS narration and auto subtitles in a container; narration describes the action before it happens; brand presets hold colours/voice/logo.
- **كيف / how:** docker compose run video-guide-creator validate|generate guides/<slug>.yml (Edge TTS voices)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2836-video-guide/11537-video-guide-creator/SKILL.md`

#### UI-41 · تلاشي حواف التمرير · Scroll-edge fade masks · 📦 بأمر تثبيت
- **ماذا / what:** Scrollable areas fade their edges with a mask; with scroll-driven animations the fade appears only when there is more content in that direction (vendored shadcn utility).
- **كيف / how:** Utilities scroll-fade / -y / -x / -t / -b / -s / -e; mask-image linear-gradient; @supports (animation-timeline: scroll()) uses scroll(self y) with animation-range; static fallback otherwise.
- **أرقام / params:** fade size min(12%, spacing*10); reveal range spacing*24
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-audit-pro/vendor/shadcn-tailwind-4.13.0.css:97` · `kosif-audit-pro/vendor/shadcn-tailwind-4.13.0.LICENSE.md`

#### UI-42 · ستايل برومو المنتج · Product promo style · 📦 بأمر تثبيت
- **ماذا / what:** Launch-promo kinetic type with a neon prompt box, a glass orb and light/dark flips.
- **كيف / how:** STY.product: 16:9, tech, 2.2 wps, Readex Pro; bg #05050A light #F8F7FF ink #F5F3FF gray #8B88A6 dark #14122B violet #A88BFF/#6C3BFF blue #2F5BFF pink #D946EF orange #FF6A1A/#FF8A3D; KIT.productMode cycles big/prompt/orb/capsule and ends on 'end'; typing+click sfx on prompt lines, impact on the end card.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:794` · `app/public/js/10_studio.js:966`

#### UI-43 · مشغل ويب مضمن · Embeddable player web component · 📦 بأمر تثبيت
- **ماذا / what:** <hyperframes-player src controls> plays a composition in any page.
- **كيف / how:** @hyperframes/player.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/packages/player/README.md`

#### UI-44 · مؤشر وكيل ذكي · Agent Cursor · 📦 بأمر تثبيت
- **ماذا / what:** A named AI-agent pointer walks through a list of UI steps, typing each step label, ringing each click target and finishing on a check mark.
- **كيف / how:** Install with `npx hyperframes add agent-cursor` (copies to compositions/components/agent-cursor.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium fram…
- **أرقام / params:** targets as "x,y;x,y" percent pairs; accent hex #0a84ff; vars: agent_name=Agent; steps=Reading the page,Opening Settings,Turning on backups,Done; targets=25,47;76,30; accent=#0a84ff
- **تثبيت / install:** `npx hyperframes add agent-cursor` (copies to compositions/components/agent-cursor`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/agent-cursor/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/agent-cursor/agent-cursor.html` · `kosif-one/vendor/hyperframes/registry/components/agent-cursor/demo.html`

#### UI-45 · مجموعة صور ترتفع · Avatar Group Hover · 📦 بأمر تثبيت
- **ماذا / what:** Overlapping avatar row where avatars near a virtual hover point lift with distance falloff and spring back.
- **كيف / how:** Install with `npx hyperframes add avatar-group-hover` (copies to compositions/components/avatar-group-hover.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless C…
- **أرقام / params:** vars: size=standard[small|standard|large]; overlap=standard[tight|standard|loose]; accent=blue[blue|violet|green]
- **تثبيت / install:** `npx hyperframes add avatar-group-hover` (copies to compositions/components/avatar-group-hover`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/avatar-group-hover/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/avatar-group-hover/avatar-group-hover.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/avatar-group-hover.mdx`

#### UI-46 · قفزة شارة الإشعار · Badge Pop · 📦 بأمر تثبيت
- **ماذا / what:** Notification badge appears with an elastic scale pop and reveals its count (transitions.dev-inspired).
- **كيف / how:** Install with `npx hyperframes add badge-pop` (copies to compositions/components/badge-pop.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame capt…
- **أرقام / params:** vars: count=3; accent=red[red|blue|green|violet]; surface=light[light|dark]
- **تثبيت / install:** `npx hyperframes add badge-pop` (copies to compositions/components/badge-pop`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/badge-pop/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/badge-pop/badge-pop.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/badge-pop.mdx`

#### UI-47 · مسح قبل/بعد · Before After Wipe · 📦 بأمر تثبيت
- **ماذا / what:** Two full-bleed slots (before/after); a divider wipes the after layer across and rests at a set split.
- **كيف / how:** Install with `npx hyperframes add before-after-wipe` (copies to compositions/components/before-after-wipe.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chr…
- **أرقام / params:** rest_split 50 %; wipe_at 0.25 s; vars: label_a=Before; label_b=After; rest_split=50(0..100); wipe_at=0.25(0..8); accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add before-after-wipe` (copies to compositions/components/before-after-wipe`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/before-after-wipe/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/before-after-wipe/before-after-wipe.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/before-after-wipe.mdx`

#### UI-48 · مسرح المتصفح/الجهاز · Browser Device Stage · 📦 بأمر تثبيت
- **ماذا / what:** Token-styled browser, window or phone chrome whose screen is a slot (image/video/HTML) with skeleton default, a single settle entrance and optional crossfade to a second screen.
- **كيف / how:** Install with `npx hyperframes add browser-device-stage` (copies to compositions/components/browser-device-stage.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headle…
- **أرقام / params:** slots browser-device-stage-screen / -screen-b (host <template data-slot>); vars: chrome=browser[browser|window|phone]; title=app.example.com; swap_at=0(0..30); accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add browser-device-stage` (copies to compositions/components/browser-device-stage`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/browser-device-stage/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/browser-device-stage/browser-device-stage.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/browser-device-stage.mdx`

#### UI-49 · بوابة مسح الكاميرا · Camera Scan Gate · 📦 بأمر تثبيت
- **ماذا / what:** Camera/QR recognition beat: viewfinder sweep, corner brackets lock, confirmation pulse, then "Verified".
- **كيف / how:** Install with `npx hyperframes add camera-scan-gate` (copies to compositions/components/camera-scan-gate.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chrom…
- **أرقام / params:** scanColor var(--brand); sweepSpeed 1; vars: scanColor=var(--brand); targetLabel=Verified; sweepSpeed=1(0.8..1.6)
- **تثبيت / install:** `npx hyperframes add camera-scan-gate` (copies to compositions/components/camera-scan-gate`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/camera-scan-gate/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/camera-scan-gate/camera-scan-gate.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/camera-scan-gate.mdx`

#### UI-50 · تمدد البطاقة · Card Resize · 📦 بأمر تثبيت
- **ماذا / what:** Compact card grows into a detail panel (transitions.dev-inspired).
- **كيف / how:** Install with `npx hyperframes add card-resize` (copies to compositions/components/card-resize.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame …
- **أرقام / params:** surface paper|ink; accent ocean|forest|ember; elevation flat|raised|floating; vars: surface=paper[paper|ink]; accent=ocean[ocean|forest|ember]; elevation=raised[flat|raised|floating]
- **تثبيت / install:** `npx hyperframes add card-resize` (copies to compositions/components/card-resize`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/card-resize/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/card-resize/card-resize.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/card-resize.mdx`

#### UI-51 · رسالة دردشة · Chat Message · 📦 بأمر تثبيت
- **ماذا / what:** A single chat bubble arrives on a measured entry (scale 0.75, 0.12 s, from the sender corner): received/sent with real tail, emoji row, image or link card.
- **كيف / how:** Install with `npx hyperframes add chat-message` (copies to compositions/components/chat-message.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium fram…
- **أرقام / params:** type recv|sent|emoji|img|card; tail on|off; delivered on|off; vars: type=sent[recv|sent|emoji|img|card]; text=wait look 👀; cardTitle=HyperFrames — Write HTML, render pixel-perfect video; cardDomain=hyperframes.heygen.com; tail=on[on|off]; delivered=on[on|off]
- **تثبيت / install:** `npx hyperframes add chat-message` (copies to compositions/components/chat-message`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/chat-message/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/chat-message/chat-message.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/chat-message.mdx`

#### UI-52 · محادثة كاملة · Chat Thread · 📦 بأمر تثبيت
- **ماذا / what:** A full mountable messaging scene: status bar, contact pill, tailed bubbles, delivered receipt, emoji, media and link card, typing dots.
- **كيف / how:** Install with `npx hyperframes add chat-thread` (copies to compositions/components/chat-thread.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame …
- **أرقام / params:** messages "recv:...|sent:...|card:title~domain|emoji:..."; beat 1.7 s; vars: contact=Rachel; unread=12(0..99); messages=recv:what r u using for the launch video??|sent:wait look 👀|card:HyperFrames — Write HTML, render pixel-perfect video~hyperframes.heygen.com|recv:OMG IT&#39;S HTML|emoji:🤯🤯🤯|sent:re…
- **تثبيت / install:** `npx hyperframes add chat-thread` (copies to compositions/components/chat-thread`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/chat-thread/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/chat-thread/chat-thread.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/chat-thread.mdx`

#### UI-53 · شاشة مقسومة للمقارنة · Comparison Split · 📦 بأمر تثبيت
- **ماذا / what:** Muted before panel vs vivid after panel with a persistent divider wipe; horizontal or vertical.
- **كيف / how:** Install with `npx hyperframes add comparison-split` (copies to compositions/components/comparison-split.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chrom…
- **أرقام / params:** split 50; orientation horizontal|vertical; vars: split=50(0..100); orientation=horizontal[horizontal|vertical]; labelA=Before; labelB=After
- **تثبيت / install:** `npx hyperframes add comparison-split` (copies to compositions/components/comparison-split`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/comparison-split/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/comparison-split/comparison-split.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/comparison-split.mdx`

#### UI-54 · قائمة النقر الأيمن · Context Menu Cursor · 📦 بأمر تثبيت
- **ماذا / what:** Cursor right-clicks a file, a context menu blooms from its tip, hover tracks items and the picked action (duplicate/rename/trash/toast) plays out.
- **كيف / how:** Install with `npx hyperframes add cursor-context-menu` (copies to compositions/components/cursor-context-menu.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless…
- **أرقام / params:** items list; pick 2; tone light|dark; vars: items=Open,Rename,Duplicate,Share,Move to Trash; pick=2(0..9); tone=light[light|dark]
- **تثبيت / install:** `npx hyperframes add cursor-context-menu` (copies to compositions/components/cursor-context-menu`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/cursor-context-menu/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/cursor-context-menu/cursor-context-menu.html` · `kosif-one/vendor/hyperframes/registry/components/cursor-context-menu/demo.html`

#### UI-55 · سحب وإفلات · Drag and Drop Cursor · 📦 بأمر تثبيت
- **ماذا / what:** Cursor grabs a task card, lifts and tilts it, carries it to an empty column, drops with settle while the list closes the gap.
- **كيف / how:** Install with `npx hyperframes add cursor-drag-drop` (copies to compositions/components/cursor-drag-drop.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chrom…
- **أرقام / params:** accent #0a84ff; vars: card_label=Fix checkout validation; accent=#0a84ff; tone=light[light|dark]
- **تثبيت / install:** `npx hyperframes add cursor-drag-drop` (copies to compositions/components/cursor-drag-drop`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/cursor-drag-drop/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/cursor-drag-drop/cursor-drag-drop.html` · `kosif-one/vendor/hyperframes/registry/components/cursor-drag-drop/demo.html`

#### UI-56 · أثر المؤشر التعليمي · Cursor Glyph Trail · 📦 بأمر تثبيت
- **ماذا / what:** Tutorial cursor clicks through three steps leaving a distance-spaced dotted trail and numbered markers that fade per step.
- **كيف / how:** Install with `npx hyperframes add cursor-glyph-trail` (copies to compositions/components/cursor-glyph-trail.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless C…
- **أرقام / params:** path sweep|arc|zigzag; density low|med|high; fade 0.5; vars: glyphs=; density=med[low|med|high]; path=sweep[sweep|arc|zigzag]; fade=0.5; accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add cursor-glyph-trail` (copies to compositions/components/cursor-glyph-trail`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/cursor-glyph-trail/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/cursor-glyph-trail/cursor-glyph-trail.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/cursor-glyph-trail.mdx`

#### UI-57 · تحديد مستطيل · Marquee Select Cursor · 📦 بأمر تثبيت
- **ماذا / what:** Cursor drags a selection rectangle over a photo grid; every tile it touches rings and gets a check while a pill counts up.
- **كيف / how:** Install with `npx hyperframes add cursor-marquee-select` (copies to compositions/components/cursor-marquee-select.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (head…
- **أرقام / params:** start/end x,y %; vars: accent=#0a84ff; start_x=20.5(0..100); start_y=25.5(0..100); end_x=57(0..100); end_y=52(0..100); pill_label=selected
- **تثبيت / install:** `npx hyperframes add cursor-marquee-select` (copies to compositions/components/cursor-marquee-select`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/cursor-marquee-select/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/cursor-marquee-select/cursor-marquee-select.html` · `kosif-one/vendor/hyperframes/registry/components/cursor-marquee-select/demo.html`

#### UI-58 · تحديد نص · Text Select Cursor · 📦 بأمر تثبيت
- **ماذا / what:** Arrow becomes an I-beam, drags a character-by-character selection, a format toolbar rises and Bold is clicked.
- **كيف / how:** Install with `npx hyperframes add cursor-text-select` (copies to compositions/components/cursor-text-select.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless C…
- **أرقام / params:** vars: title=Spring release notes; text=Our spring release ships on Thursday. Teams can now share a live review link, collect time-stamped comments, and approve the final cut without leaving the editor. Early customers cut their review rounds in half.; phrase=approve the final cut; accent=#0a84ff
- **تثبيت / install:** `npx hyperframes add cursor-text-select` (copies to compositions/components/cursor-text-select`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/cursor-text-select/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/cursor-text-select/cursor-text-select.html` · `kosif-one/vendor/hyperframes/registry/components/cursor-text-select/demo.html`

#### UI-59 · مؤشر السهم الطائر · Dart Cursor · 📦 بأمر تثبيت
- **ماذا / what:** Bold outlined arrowhead dives in from camera depth with motion blur, squashes on two clicks and whips out.
- **كيف / how:** Install with `npx hyperframes add dart-cursor` (copies to compositions/components/dart-cursor.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame …
- **أرقام / params:** enter_from/exit_to right|left|top|bottom; blur 1; vars: tone=dark[dark|light]; target_x=34(5..95); target_y=58(5..95); target2_x=64(5..95); target2_y=46(5..95); enter_from=right[right|left|top|bottom]; exit_to=right[right|left|top|bottom]; blur=1(0..1.5)
- **تثبيت / install:** `npx hyperframes add dart-cursor` (copies to compositions/components/dart-cursor`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/dart-cursor/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/dart-cursor/dart-cursor.html` · `kosif-one/vendor/hyperframes/registry/components/dart-cursor/demo.html`

#### UI-60 · إطار الجهاز · Device Frame Stage · 📦 بأمر تثبيت
- **ماذا / what:** Phone/tablet mockup with screen slot rises onto stage, settles and idles with a float.
- **كيف / how:** Install with `npx hyperframes add device-frame-stage` (copies to compositions/components/device-frame-stage.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless C…
- **أرقام / params:** device phone|tablet; cutout none|island|notch; body graphite|silver; vars: device=phone[phone|tablet]; cutout=none[none|island|notch]; body=graphite[graphite|silver]
- **تثبيت / install:** `npx hyperframes add device-frame-stage` (copies to compositions/components/device-frame-stage`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/device-frame-stage/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/device-frame-stage/device-frame-stage.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/device-frame-stage.mdx`

#### UI-61 · تبديل التركيز · Focus Swap · 📦 بأمر تثبيت
- **ماذا / what:** Two side-by-side cards; one recedes with scale/blur/dim while the other comes to full focus.
- **كيف / how:** Install with `npx hyperframes add focus-swap` (copies to compositions/components/focus-swap.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame ca…
- **أرقام / params:** blurPx 6; dim 0.5; vars: focus=b[a|b]; blurPx=6(0..20); dim=0.5(0..1)
- **تثبيت / install:** `npx hyperframes add focus-swap` (copies to compositions/components/focus-swap`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/focus-swap/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/focus-swap/focus-swap.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/focus-swap.mdx`

#### UI-62 · لمسة الإصبع · Gesture Tap · 📦 بأمر تثبيت
- **ماذا / what:** Touch circle taps a mobile pill button which switches into a new labelled accent state.
- **كيف / how:** Install with `npx hyperframes add gesture-tap` (copies to compositions/components/gesture-tap.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame …
- **أرقام / params:** Follow -> Following; vars: tap_label=Follow; response_label=Following; accent=green[green|blue|violet]
- **تثبيت / install:** `npx hyperframes add gesture-tap` (copies to compositions/components/gesture-tap`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/gesture-tap/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/gesture-tap/gesture-tap.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/gesture-tap.mdx`

#### UI-63 · تحول الأيقونة · Icon Morph Beat · 📦 بأمر تثبيت
- **ماذا / what:** Icon morphs between state silhouettes, shifts to accent colour and pulses once on completion.
- **كيف / how:** Install with `npx hyperframes add icon-morph-beat` (copies to compositions/components/icon-morph-beat.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromiu…
- **أرقام / params:** pair mic-check|play-check|lock-unlock; vars: pair=mic-check[mic-check|play-check|lock-unlock]; accent=green[green|blue|violet]
- **تثبيت / install:** `npx hyperframes add icon-morph-beat` (copies to compositions/components/icon-morph-beat`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/icon-morph-beat/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/icon-morph-beat/icon-morph-beat.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/icon-morph-beat.mdx`

#### UI-64 · تبديل الأيقونة · Icon Swap · 📦 بأمر تثبيت
- **ماذا / what:** Scale-and-blur swap between two toolbar icons.
- **كيف / how:** Install with `npx hyperframes add icon-swap` (copies to compositions/components/icon-swap.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame capt…
- **أرقام / params:** shape rounded|circle|square; vars: tone=dark[dark|light|accent]; size=standard[small|standard|large]; shape=rounded[rounded|circle|square]; blur=standard[soft|standard|heavy]
- **تثبيت / install:** `npx hyperframes add icon-swap` (copies to compositions/components/icon-swap`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/icon-swap/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/icon-swap/icon-swap.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/icon-swap.mdx`

#### UI-65 · تغذية حقل الإدخال · Input Feedback · 📦 بأمر تثبيت
- **ماذا / what:** Input field with shake on error, clear affordance and success state.
- **كيف / how:** Install with `npx hyperframes add input-feedback` (copies to compositions/components/input-feedback.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium …
- **أرقام / params:** status valid|error; vars: status=valid[valid|error]; value=mia@example.com; hint=Looks good.
- **تثبيت / install:** `npx hyperframes add input-feedback` (copies to compositions/components/input-feedback`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/input-feedback/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/input-feedback/input-feedback.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/input-feedback.mdx`

#### UI-66 · المؤشر المغناطيسي · Magnetic Cursor · 📦 بأمر تثبيت
- **ماذا / what:** Soft dot pointer is pulled into toolbar buttons, morphing into their hover plate while icons lean toward it, presses one and leaves.
- **كيف / how:** Install with `npx hyperframes add magnetic-cursor` (copies to compositions/components/magnetic-cursor.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromiu…
- **أرقام / params:** visits "0,3"; press 2; vars: accent=#3b82f6; tone=light[light|dark]; visits=0,3; press=2(1..3)
- **تثبيت / install:** `npx hyperframes add magnetic-cursor` (copies to compositions/components/magnetic-cursor`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/magnetic-cursor/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/magnetic-cursor/magnetic-cursor.html` · `kosif-one/vendor/hyperframes/registry/components/magnetic-cursor/demo.html`

#### UI-67 · تحول القائمة · Menu Morph · 📦 بأمر تثبيت
- **ماذا / what:** Hamburger/plus icon morphs into a compact action menu.
- **كيف / how:** Install with `npx hyperframes add menu-morph` (copies to compositions/components/menu-morph.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame ca…
- **أرقام / params:** actions "Text, Image, Audio"; vars: actions=Text, Image, Audio; tone=ink[ink|green|blue|violet]; size=68(52..112)
- **تثبيت / install:** `npx hyperframes add menu-morph` (copies to compositions/components/menu-morph`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/menu-morph/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/menu-morph/menu-morph.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/menu-morph.mdx`

#### UI-68 · حزمة الانتقالات الدقيقة · Micro Transitions · 📦 بأمر تثبيت
- **ماذا / what:** Pack of micro UI motions: badge, dropdown, modal, tabs, tooltip, success check.
- **كيف / how:** Install with `npx hyperframes add micro-transitions` (copies to compositions/components/micro-transitions.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chr…
- **أرقام / params:** tone red|amber|violet; vars: badge=3; tooltip=Copied; tone=red[red|amber|violet]; travel=standard[close|standard|far]
- **تثبيت / install:** `npx hyperframes add micro-transitions` (copies to compositions/components/micro-transitions`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/micro-transitions/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/micro-transitions/micro-transitions.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/micro-transitions.mdx`

#### UI-69 · تحول النافذة المنبثقة · Modal Morph · 📦 بأمر تثبيت
- **ماذا / what:** Shared-element FLIP: small card becomes a full panel by transform only; children counter-scale and reflow onto measured targets as pure functions of time.
- **كيف / how:** Install with `npx hyperframes add modal-morph` (copies to compositions/components/modal-morph.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame …
- **أرقام / params:** expand_at 1.2 s; register calm|snappy; vars: from_scale=1; expand_at=1.2; register=calm[calm|snappy]; accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add modal-morph` (copies to compositions/components/modal-morph`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/modal-morph/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/modal-morph/modal-morph.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/modal-morph.mdx`

#### UI-70 · مروحة الأجهزة · Multi Device Splay · 📦 بأمر تثبيت
- **ماذا / what:** Phone, tablet and desktop mockups fan out from a centred stack and idle-float.
- **كيف / how:** Install with `npx hyperframes add multi-device-splay` (copies to compositions/components/multi-device-splay.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless C…
- **أرقام / params:** vars: accent=blue[green|blue|violet]
- **تثبيت / install:** `npx hyperframes add multi-device-splay` (copies to compositions/components/multi-device-splay`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/multi-device-splay/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/multi-device-splay/multi-device-splay.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/multi-device-splay.mdx`

#### UI-71 · مؤشرات متعددة · Multiplayer Cursors · 📦 بأمر تثبيت
- **ماذا / what:** Labelled collaborator cursors with glows drift into a shared centre to show live presence.
- **كيف / how:** Install with `npx hyperframes add multiplayer-cursors` (copies to compositions/components/multiplayer-cursors.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless…
- **أرقام / params:** cursorCount 4; labels Ana,Ken,Wen,Mia; vars: cursorCount=4(2..6); labels=Ana,Ken,Wen,Mia
- **تثبيت / install:** `npx hyperframes add multiplayer-cursors` (copies to compositions/components/multiplayer-cursors`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/multiplayer-cursors/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/multiplayer-cursors/multiplayer-cursors.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/multiplayer-cursors.mdx`

#### UI-72 · إشعار النظام · Native Notification Pop · 📦 بأمر تثبيت
- **ماذا / what:** One iOS/macOS-faithful banner drops in on an interruptible spring with soft overshoot, backdrop blur, app dot, title and body.
- **كيف / how:** Install with `npx hyperframes add native-notification-pop` (copies to compositions/components/native-notification-pop.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (…
- **أرقام / params:** os ios|macos; at 0.3 s; vars: title=Render complete; body=launch-cut.mp4 is ready to preview; app_label=HyperFrames; os=ios[ios|macos]; at=0.3(0..8); accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add native-notification-pop` (copies to compositions/components/native-notification-pop`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/native-notification-pop/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/native-notification-pop/native-notification-pop.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/native-notification-pop.mdx`

#### UI-73 · كتابة في الملاحظات · Notes Typing · 📦 بأمر تثبيت
- **ماذا / what:** Notes-app scene: bold title then body lines typed on a measured human keystroke rhythm with the caret riding each character.
- **كيف / how:** Install with `npx hyperframes add notes-typing` (copies to compositions/components/notes-typing.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium fram…
- **أرقام / params:** lines "a|b|c"; speed 1; vars: title=Things nobody told me|about video.; lines=my videos sucked|my tools cost $$$|and re-edits never end.; speed=1(0.5..2)
- **تثبيت / install:** `npx hyperframes add notes-typing` (copies to compositions/components/notes-typing`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/notes-typing/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/notes-typing/notes-typing.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/notes-typing.mdx`

#### UI-74 · تراكم الإشعارات · Notification Pileup · 📦 بأمر تثبيت
- **ماذا / what:** Mobile notifications arrive faster and faster, pushing the stack down into an anxious tower.
- **كيف / how:** Install with `npx hyperframes add notification-pileup` (copies to compositions/components/notification-pileup.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless…
- **أرقام / params:** count 7; speed 1; vars: count=7(4..10); speed=1(0.5..2); showBadges=yes[yes|no]
- **تثبيت / install:** `npx hyperframes add notification-pileup` (copies to compositions/components/notification-pileup`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/notification-pileup/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/notification-pileup/notification-pileup.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/notification-pileup.mdx`

#### UI-75 · رصة الإشعارات · Notification Stack · 📦 بأمر تثبيت
- **ماذا / what:** 1-5 notification cards slide into a stack on cues, newest on top; one grows and brightens as focus.
- **كيف / how:** Install with `npx hyperframes add notification-stack` (copies to compositions/components/notification-stack.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless C…
- **أرقام / params:** titles/bodies lists; expand -1; vars: titles=Build queued,Checks passed,Deploy live; bodies=Pipeline started for main,All 42 checks green,Now serving version 2.4; expand=-1(-1..4); cues=; accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add notification-stack` (copies to compositions/components/notification-stack`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/notification-stack/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/notification-stack/notification-stack.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/notification-stack.mdx`

#### UI-76 · خطوات التهيئة · Onboarding Stepper Flow · 📦 بأمر تثبيت
- **ماذا / what:** Onboarding flow with milestone rail, active step card and next button.
- **كيف / how:** Install with `npx hyperframes add onboarding-stepper-flow` (copies to compositions/components/onboarding-stepper-flow.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (…
- **تثبيت / install:** `npx hyperframes add onboarding-stepper-flow` (copies to compositions/components/onboarding-stepper-flow`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/onboarding-stepper-flow/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/onboarding-stepper-flow/onboarding-stepper-flow.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/onboarding-stepper-flow.mdx`

#### UI-77 · المؤشر العملاق · Oversized Cursor · 📦 بأمر تثبيت
- **ماذا / what:** macOS arrow at 3.5x size lands on a control, clicks it on, settles below it and exits.
- **كيف / how:** Install with `npx hyperframes add oversized-cursor` (copies to compositions/components/oversized-cursor.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chrom…
- **أرقام / params:** target_x/y 55 %; cursor_variant light|dark; vars: cursor_variant=light[light|dark]; target_x=55(15..85); target_y=55(15..85); click_label=Generate; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add oversized-cursor` (copies to compositions/components/oversized-cursor`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/oversized-cursor/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/oversized-cursor/oversized-cursor.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/oversized-cursor.mdx`

#### UI-78 · كشف اللوحة · Panel Reveal · 📦 بأمر تثبيت
- **ماذا / what:** Panel expands in height and its content fades in.
- **كيف / how:** Install with `npx hyperframes add panel-reveal` (copies to compositions/components/panel-reveal.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium fram…
- **أرقام / params:** width narrow|standard|wide; vars: title=Motion tokens; width=standard[narrow|standard|wide]; tone=paper[paper|ink]; reveal=fade[fade|solid]
- **تثبيت / install:** `npx hyperframes add panel-reveal` (copies to compositions/components/panel-reveal`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/panel-reveal/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/panel-reveal/panel-reveal.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/panel-reveal.mdx`

#### UI-79 · ضغطة الزر · Press Ripple · 📦 بأمر تثبيت
- **ماذا / what:** Cursor decelerates in, compresses with the target button, releases two small click rings while the label swaps to a check, then exits.
- **كيف / how:** Install with `npx hyperframes add press-ripple` (copies to compositions/components/press-ripple.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium fram…
- **أرقام / params:** press_at 0.9 s; done_label Saved; vars: label=Get started; done_label=Saved; target_x=50(8..92); target_y=50(8..92); press_at=0.9(0.9..10); cursor=light[light|dark]; accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add press-ripple` (copies to compositions/components/press-ripple`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/press-ripple/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/press-ripple/press-ripple.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/press-ripple.mdx`

#### UI-80 · اسحب للتحديث · Pull to Refresh · 📦 بأمر تثبيت
- **ماذا / what:** Mobile list pulls with nonlinear rubber-band resistance, arms at a threshold, shows a bounded loader, snaps back.
- **كيف / how:** Install with `npx hyperframes add pull-to-refresh` (copies to compositions/components/pull-to-refresh.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromiu…
- **أرقام / params:** pullDistance 120; spinnerStyle arrow|dots|ring; vars: pullDistance=120(60..220); spinnerStyle=ring[arrow|dots|ring]
- **تثبيت / install:** `npx hyperframes add pull-to-refresh` (copies to compositions/components/pull-to-refresh`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/pull-to-refresh/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/pull-to-refresh/pull-to-refresh.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/pull-to-refresh.mdx`

#### UI-81 · دوار الشاشات · Screen Flow Carousel · 📦 بأمر تثبيت
- **ماذا / what:** 2-5 app screens ride a rail; centre primary, neighbours recede; advances on cues with velocity-matched throw and long-tail catch while a caption swaps.
- **كيف / how:** Install with `npx hyperframes add screen-flow-carousel` (copies to compositions/components/screen-flow-carousel.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headle…
- **أرقام / params:** screens 3; cues; vars: screens=3(2..5); captions=; cues=; accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add screen-flow-carousel` (copies to compositions/components/screen-flow-carousel`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/screen-flow-carousel/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/screen-flow-carousel/screen-flow-carousel.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/screen-flow-carousel.mdx`

#### UI-82 · مسار الإعدادات · Settings Toggle Flow · 📦 بأمر تثبيت
- **ماذا / what:** Settings screen with preference rows, toggles and active-state feedback.
- **كيف / how:** Install with `npx hyperframes add settings-toggle-flow` (copies to compositions/components/settings-toggle-flow.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headle…
- **تثبيت / install:** `npx hyperframes add settings-toggle-flow` (copies to compositions/components/settings-toggle-flow`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/settings-toggle-flow/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/settings-toggle-flow/settings-toggle-flow.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/settings-toggle-flow.mdx`

#### UI-83 · لوحة سفلية نابضة · Sheet Spring-Up · 📦 بأمر تثبيت
- **ماذا / what:** Bottom sheet rushes up on a spring sampled frame-by-frame from reference footage, overshoots and settles.
- **كيف / how:** Install with `npx hyperframes add sheet-spring-up` (copies to compositions/components/sheet-spring-up.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromiu…
- **أرقام / params:** width 668 (400-900); radius 34 (16-48); vars: width=668(400..900); radius=34(16..48); tone=light[light|dark]
- **تثبيت / install:** `npx hyperframes add sheet-spring-up` (copies to compositions/components/sheet-spring-up`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/sheet-spring-up/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/sheet-spring-up/sheet-spring-up.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/sheet-spring-up.mdx`

#### UI-84 · مسار التسجيل · Signup Flow · 📦 بأمر تثبيت
- **ماذا / what:** Signup flow: social button, email, password and submit.
- **كيف / how:** Install with `npx hyperframes add signup-flow` (copies to compositions/components/signup-flow.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame …
- **تثبيت / install:** `npx hyperframes add signup-flow` (copies to compositions/components/signup-flow`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/signup-flow/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/signup-flow/signup-flow.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/signup-flow.mdx`

#### UI-85 · كشف الهيكل · Skeleton Reveal · 📦 بأمر تثبيت
- **ماذا / what:** Skeleton loader pulses then crossfades into real content.
- **كيف / how:** Install with `npx hyperframes add skeleton-reveal` (copies to compositions/components/skeleton-reveal.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromiu…
- **أرقام / params:** vars: name=Jane Cooper; detail=jane@example.com; tone=light[light|dark]
- **تثبيت / install:** `npx hyperframes add skeleton-reveal` (copies to compositions/components/skeleton-reveal`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/skeleton-reveal/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/skeleton-reveal/skeleton-reveal.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/skeleton-reveal.mdx`

#### UI-86 · شريط الحالات · State Chip Rail · 📦 بأمر تثبيت
- **ماذا / what:** Rail of mono status chips steps through states on a cue schedule (active ink, done dim, pending hollow) with optional badges.
- **كيف / how:** Install with `npx hyperframes add state-chip-rail` (copies to compositions/components/state-chip-rail.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromiu…
- **أرقام / params:** states "Queued,Reading,Drafting,Done"; vars: states=Queued,Reading,Drafting,Done; times=; badge_state=1(0..7); badges=; accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add state-chip-rail` (copies to compositions/components/state-chip-rail`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/state-chip-rail/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/state-chip-rail/state-chip-rail.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/state-chip-rail.mdx`

#### UI-87 · تبديل الموكاب الثابت · Sticky Mock Swap · 📦 بأمر تثبيت
- **ماذا / what:** Pinned product mock crossfades through accent-tinted feature states while matching captions rise and exit.
- **كيف / how:** Install with `npx hyperframes add sticky-mock-swap` (copies to compositions/components/sticky-mock-swap.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chrom…
- **أرقام / params:** vars: captions=Instant previews,Zero config,Ship on Friday; accent=violet[green|blue|violet]
- **تثبيت / install:** `npx hyperframes add sticky-mock-swap` (copies to compositions/components/sticky-mock-swap`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/sticky-mock-swap/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/sticky-mock-swap/sticky-mock-swap.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/sticky-mock-swap.mdx`

#### UI-88 · علامة النجاح · Success Check · 📦 بأمر تثبيت
- **ماذا / what:** Success check with ring pop, path draw and subtle rotate blur.
- **كيف / how:** Install with `npx hyperframes add success-check` (copies to compositions/components/success-check.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium fr…
- **أرقام / params:** tint green|blue|violet|amber; vars: tint=green[green|blue|violet|amber]; size=standard[small|standard|large]; ring=standard[subtle|standard|bold]; spin=standard[subtle|standard|bold]
- **تثبيت / install:** `npx hyperframes add success-check` (copies to compositions/components/success-check`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/success-check/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/success-check/success-check.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/success-check.mdx`

#### UI-89 · سحب الشريط · Swipe Rail · 📦 بأمر تثبيت
- **ماذا / what:** Touch circle drags a horizontal card rail with momentum carry and snap to next card.
- **كيف / how:** Install with `npx hyperframes add swipe-rail` (copies to compositions/components/swipe-rail.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame ca…
- **أرقام / params:** card_count 4; vars: card_count=4(3..5); accent=green[green|blue|violet]; card_label_prefix=Feature
- **تثبيت / install:** `npx hyperframes add swipe-rail` (copies to compositions/components/swipe-rail`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/swipe-rail/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/swipe-rail/swipe-rail.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/swipe-rail.mdx`

#### UI-90 · مؤشر التبويبات · Tabs Slide Indicator · 📦 بأمر تثبيت
- **ماذا / what:** Pill indicator slides between active tabs.
- **كيف / how:** Install with `npx hyperframes add tabs-slide-indicator` (copies to compositions/components/tabs-slide-indicator.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headle…
- **أرقام / params:** labels Plan,Debug,Ask; shape pill|rounded|square; vars: accent=ink[ink|green|blue|violet]; width=standard[compact|standard|wide]; shape=pill[pill|rounded|square]; labels=Plan,Debug,Ask
- **تثبيت / install:** `npx hyperframes add tabs-slide-indicator` (copies to compositions/components/tabs-slide-indicator`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/tabs-slide-indicator/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/tabs-slide-indicator/tabs-slide-indicator.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/tabs-slide-indicator.mdx`

#### UI-91 · واجهة القياس · Telemetry HUD · 📦 بأمر تثبيت
- **ماذا / what:** Quiet mono debug HUD around a slotted subject: corner brackets draw, label:value lines tick on cues, one readout in accent.
- **كيف / how:** Install with `npx hyperframes add telemetry-hud` (copies to compositions/components/telemetry-hud.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium fr…
- **أرقام / params:** readouts "fps:59.94,latency:11.8 ms,gpu:38%,heap:1.2 GB"; vars: readouts=fps:59.94,latency:11.8 ms,gpu:38%,heap:1.2 GB; emphasize=0(-1..7); cues=; accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add telemetry-hud` (copies to compositions/components/telemetry-hud`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/telemetry-hud/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/telemetry-hud/telemetry-hud.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/telemetry-hud.mdx`

#### UI-92 · قلب المفتاح · Toggle Flip · 📦 بأمر تثبيت
- **ماذا / what:** Oversized toggle flips with thumb overshoot, track colour crossfade and press-compress.
- **كيف / how:** Install with `npx hyperframes add toggle-flip` (copies to compositions/components/toggle-flip.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame …
- **أرقام / params:** size 40; vars: direction=on[on|off]; label=Auto-save; size=40(20..70)
- **تثبيت / install:** `npx hyperframes add toggle-flip` (copies to compositions/components/toggle-flip`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/toggle-flip/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/toggle-flip/toggle-flip.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/toggle-flip.mdx`

#### UI-93 · مؤشر اللمس · Touch Indicator · 📦 بأمر تثبيت
- **ماذا / what:** Translucent contact circle for mobile scenes: touches glass on the response frame, tap or swipe.
- **كيف / how:** Install with `npx hyperframes add touch-indicator` (copies to compositions/components/touch-indicator.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromiu…
- **أرقام / params:** gesture tap|swipe; vars: gesture=tap[tap|swipe]; polarity=light[light|dark]; targetX=50(0..100); targetY=55(0..100)
- **تثبيت / install:** `npx hyperframes add touch-indicator` (copies to compositions/components/touch-indicator`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/touch-indicator/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/touch-indicator/touch-indicator.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/touch-indicator.mdx`

#### UI-94 · مؤشر الكتابة · Typing Indicator · 📦 بأمر تثبيت
- **ماذا / what:** Three-dot "is typing" bubble pops at the thread edge, holds, vanishes when the message lands.
- **كيف / how:** Install with `npx hyperframes add typing-indicator` (copies to compositions/components/typing-indicator.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chrom…
- **أرقام / params:** size 124; tail on|off; vars: size=124(80..220); tone=dark[dark|light]; tail=on[on|off]
- **تثبيت / install:** `npx hyperframes add typing-indicator` (copies to compositions/components/typing-indicator`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/typing-indicator/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/typing-indicator/typing-indicator.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/typing-indicator.mdx`

#### UI-95 · محرر المتجهات · Vector Editor Rig · 📦 بأمر تثبيت
- **ماذا / what:** Dark design-tool chrome with a live pen path, anchors, bezier handles and selection frame.
- **كيف / how:** Install with `npx hyperframes add vector-editor-rig` (copies to compositions/components/vector-editor-rig.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chr…
- **أرقام / params:** tool pen|shape|type; vars: tool=pen[pen|shape|type]; pathLabel=Logo
- **تثبيت / install:** `npx hyperframes add vector-editor-rig` (copies to compositions/components/vector-editor-rig`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/vector-editor-rig/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/vector-editor-rig/vector-editor-rig.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/vector-editor-rig.mdx`

#### UI-96 · عرض تطبيق ثلاث شاشات · App Showcase · 📦 بأمر تثبيت
- **ماذا / what:** Fitness-app showcase with three floating phone screens (5.5 s).
- **كيف / how:** Install with `npx hyperframes add app-showcase` (copies the full composition to compositions/app-showcase.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: inline SVG, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Google Fonts: DM Sans; 1920x1080; duration 5.5 s
- **تثبيت / install:** `npx hyperframes add app-showcase` (copies the full composition to compositions/app-showcase`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/app-showcase/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/app-showcase/app-showcase.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/app-showcase.mdx`

#### UI-97 · آيفون الزجاج السائل · iOS 26 Liquid Glass Home Screen · 📦 بأمر تثبيت
- **ماذا / what:** 3D GLTF iPhone with an iOS 26-style home screen, liquid-glass icons, shader wallpaper, dock and glass notifications (HTML-in-Canvas).
- **كيف / how:** Install with `npx hyperframes add ios26-liquid-glass` (copies the full composition to compositions/ios26-liquid-glass.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: Three.js 0.147.0 (CDN), HTML-in-Canvas (canvas layoutsubtree + ctx.drawElementImage, experimental Chromium API), WebGL fragment shader, Canvas 2D painter, GSAP 3.14.2 pause…
- **أرقام / params:** models/iphone.glb + macbook.glb; 15 s; 1920x1080; duration 15 s
- **تثبيت / install:** `npx hyperframes add ios26-liquid-glass` (copies the full composition to compositions/ios26-liquid-glass`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/ios26-liquid-glass/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/ios26-liquid-glass/ios26-liquid-glass.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/ios26-liquid-glass.mdx`

#### UI-98 · إشعارات زجاجية · Liquid Glass Notification · 📦 بأمر تثبيت
- **ماذا / what:** Frosted glass notification cards floating over an aurora shader background (HTML-in-Canvas, WebGPU).
- **كيف / how:** Install with `npx hyperframes add liquid-glass-notification` (copies the full composition to compositions/liquid-glass-notification.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: Three.js (vendored/bundled), WebGL fragment shader, Canvas 2D painter, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 8 s; 1920x1080; duration 8 s
- **تثبيت / install:** `npx hyperframes add liquid-glass-notification` (copies the full composition to compositions/liquid-glass-notification`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/liquid-glass-notification/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/liquid-glass-notification/liquid-glass-notification.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/liquid-glass-notification.mdx`

#### UI-99 · ودجات زجاجية · Liquid Glass Widgets · 📦 بأمر تثبيت
- **ماذا / what:** Frosted glass stat cards, showcase panel and pill chips over an aurora shader (HTML-in-Canvas, WebGPU).
- **كيف / how:** Install with `npx hyperframes add liquid-glass-widgets` (copies the full composition to compositions/liquid-glass-widgets.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: Three.js (vendored/bundled), WebGL fragment shader, Canvas 2D painter, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 8 s; 1920x1080; duration 8 s
- **تثبيت / install:** `npx hyperframes add liquid-glass-widgets` (copies the full composition to compositions/liquid-glass-widgets`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/liquid-glass-widgets/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/liquid-glass-widgets/liquid-glass-widgets.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/liquid-glass-widgets.mdx`

#### UI-100 · ماك بوك تاهو · macOS Tahoe Liquid Glass Desktop · 📦 بأمر تثبيت
- **ماذا / what:** 3D MacBook GLTF with macOS Tahoe-style desktop, glass menu bar, Finder window, dock and cinematic device camera move (HTML-in-Canvas).
- **كيف / how:** Install with `npx hyperframes add macos-tahoe-liquid-glass` (copies the full composition to compositions/macos-tahoe-liquid-glass.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: Three.js 0.147.0 (CDN), HTML-in-Canvas (canvas layoutsubtree + ctx.drawElementImage, experimental Chromium API), WebGL fragment shader, Canvas 2D painter, GSAP …
- **أرقام / params:** 15 s; 1920x1080; duration 15 s
- **تثبيت / install:** `npx hyperframes add macos-tahoe-liquid-glass` (copies the full composition to compositions/macos-tahoe-liquid-glass`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/macos-tahoe-liquid-glass/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/macos-tahoe-liquid-glass/macos-tahoe-liquid-glass.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/macos-tahoe-liquid-glass.mdx`

#### UI-101 · قصة محادثة إعلانية · Message Thread Reveal · 📦 بأمر تثبيت
- **ماذا / what:** Phone conversation ad template: bubbles pop, typing dots, link card, emoji, receipts, thread scrolls up beat by beat to a closing card.
- **كيف / how:** Install with `npx hyperframes add message-thread-reveal` (copies the full composition to compositions/message-thread-reveal.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: inline SVG, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 1080x1920; 25.77 s; vars: contactName=Rachel; questionMessage=what r u using for the launch video??; teaserMessage=wait look 👀; cardImage=assets/card-image.jpg; cardTitle=HyperFrames | Write HTML, render pixel-perfect video; cardDomain=hyperframes.heygen.com; reactionMessage=OMG IT'S HTML; reactionE…
- **تثبيت / install:** `npx hyperframes add message-thread-reveal` (copies the full composition to compositions/message-thread-reveal`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/message-thread-reveal/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/message-thread-reveal/message-thread-reveal.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/message-thread-reveal.mdx`

#### UI-102 · قصة الملاحظات · Notes Reveal · 📦 بأمر تثبيت
- **ماذا / what:** Notes-app note typed character by character, page scrolls on settle curves per line, then cuts to a hand-lettered paper card.
- **كيف / how:** Install with `npx hyperframes add notes-reveal` (copies the full composition to compositions/notes-reveal.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: inline SVG, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Courier Prime + Permanent Marker bundled; 1080x1920; 24.85 s; vars: titleL1=Things nobody told me; titleL2=about video.; noteLine1=my videos sucked; noteLine2=my tools cost $$$; noteLine3=and re-edits never end.; noteLine4=then i tried writing html only; noteLine5=started HyperFrames three weeks ago…
- **تثبيت / install:** `npx hyperframes add notes-reveal` (copies the full composition to compositions/notes-reveal`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/notes-reveal/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/notes-reveal/notes-reveal.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/notes-reveal.mdx`

#### UI-103 · شلال الإشعارات · Notification Cascade · 📦 بأمر تثبيت
- **ماذا / what:** Phone notifications land and stack, each pushing the pile down, then the stack lifts into a closing card.
- **كيف / how:** Install with `npx hyperframes add notification-cascade` (copies the full composition to compositions/notification-cascade.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: inline SVG, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 1080x1920; 14 s; vars: notifTitle=New render; message1=Launch video is ready.; message2=All checks passed.; message3=4K render done in 92s.; message4=Published to the catalog.; appName=HyperFrames; headlineTop=SHIP VIDEO; headlineAccent=FROM HTML; footerText=hyperframes.heygen.com; brandLogo=assets/…
- **تثبيت / install:** `npx hyperframes add notification-cascade` (copies the full composition to compositions/notification-cascade`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/notification-cascade/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/notification-cascade/notification-cascade.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/notification-cascade.mdx`

#### UI-104 · قائمة المشاركة · Share-Sheet Carousel · 📦 بأمر تثبيت
- **ماذا / what:** Share sheet springs up from the phone bottom, cycles previews inside its card on a fast cut rhythm while the blurred ground swaps, ends on Accept tap.
- **كيف / how:** Install with `npx hyperframes add share-sheet-carousel` (copies the full composition to compositions/share-sheet-carousel.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 1080x1920; 7.23 s; vars: shareTitle=Share; senderName=HyperFrames; itemLabel=a video; stripText=OPEN-SOURCE VIDEO ENGINE · SHIP FROM HTML; acceptLabel=Accept; declineLabel=Decline; slideImage1=assets/slide-01.jpg; slideImage2=assets/slide-02.jpg; slideImage3=assets/slide-03.jpg; slideImage4=assets/s…
- **تثبيت / install:** `npx hyperframes add share-sheet-carousel` (copies the full composition to compositions/share-sheet-carousel`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/share-sheet-carousel/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/share-sheet-carousel/share-sheet-carousel.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/share-sheet-carousel.mdx`

#### UI-105 · إعلان إشعارات سلاك · Slack Notification Ad · 📦 بأمر تثبيت
- **ماذا / what:** Portrait lock screen filling with escalating Slack-style video requests before the payoff.
- **كيف / how:** Install with `npx hyperframes add slack-notification-ad` (copies the full composition to compositions/slack-notification-ad.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: inline SVG, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Inter bundled; 12 s; 1080x1920; duration 12 s
- **تثبيت / install:** `npx hyperframes add slack-notification-ad` (copies the full composition to compositions/slack-notification-ad`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/slack-notification-ad/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/slack-notification-ad/slack-notification-ad.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/slack-notification-ad.mdx`

#### UI-106 · رصة الرسائل · Thread Message Stack · 📦 بأمر تثبيت
- **ماذا / what:** Source-editable conversation stack with arbitrary incoming/outgoing messages.
- **كيف / how:** Install with `npx hyperframes add thread-message-stack` (copies the full composition to compositions/thread-message-stack.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 8 s; 1920x1080; duration 8 s
- **تثبيت / install:** `npx hyperframes add thread-message-stack` (copies the full composition to compositions/thread-message-stack`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/thread-message-stack/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/thread-message-stack/thread-message-stack.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/thread-message-stack.mdx`

#### UI-107 · كشف واجهة ثلاثي الأبعاد · 3D UI Reveal · 📦 بأمر تثبيت
- **ماذا / what:** Perspective 3D reveal of UI elements.
- **كيف / how:** Install with `npx hyperframes add ui-3d-reveal` (copies the full composition to compositions/ui-3d-reveal.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: inline SVG, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 13 s; Google Fonts: Inter; 1920x1080; duration 13 s
- **تثبيت / install:** `npx hyperframes add ui-3d-reveal` (copies the full composition to compositions/ui-3d-reveal`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/ui-3d-reveal/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/ui-3d-reveal/ui-3d-reveal.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/ui-3d-reveal.mdx`

#### UI-108 · آيفون وماك بوك حقيقيان · iPhone & MacBook 3D Showcase · 📦 بأمر تثبيت
- **ماذا / what:** GLTF iPhone 15 Pro Max and MacBook Pro with live HTML-in-Canvas screens, morphing glass lens, product-review camera choreography and 360 turntable.
- **كيف / how:** Install with `npx hyperframes add vfx-iphone-device` (copies the full composition to compositions/vfx-iphone-device.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: Three.js 0.147.0 (CDN), HTML-in-Canvas (canvas layoutsubtree + ctx.drawElementImage, experimental Chromium API), WebGL fragment shader, Canvas 2D painter, GSAP 3.14.2 paused …
- **أرقام / params:** 15 s; 1920x1080; duration 15 s
- **تثبيت / install:** `npx hyperframes add vfx-iphone-device` (copies the full composition to compositions/vfx-iphone-device`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/vfx-iphone-device/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/vfx-iphone-device/vfx-iphone-device.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/vfx-iphone-device.mdx`

#### UI-109 · بارالاكس الزجاج السائل · Liquid Glass · 📦 بأمر تثبيت
- **ماذا / what:** Liquid-glass parallax scene (Three 0.147 + EffectComposer/RenderPass, HTML-in-Canvas).
- **كيف / how:** Install with `npx hyperframes add vfx-liquid-glass` (copies the full composition to compositions/vfx-liquid-glass.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: Three.js 0.147.0 (CDN), HTML-in-Canvas (canvas layoutsubtree + ctx.drawElementImage, experimental Chromium API), WebGL fragment shader, Canvas 2D painter, GSAP 3.14.2 paused ti…
- **أرقام / params:** 20 s; Google Fonts: Inter; 1920x1080; duration 20 s
- **تثبيت / install:** `npx hyperframes add vfx-liquid-glass` (copies the full composition to compositions/vfx-liquid-glass`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/vfx-liquid-glass/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/vfx-liquid-glass/vfx-liquid-glass.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/vfx-liquid-glass.mdx`

#### UI-110 · المؤشر المغناطيسي في الكانفس · Magnetic · 📦 بأمر تثبيت
- **ماذا / what:** Magnetic cursor interaction rendered via HTML-in-Canvas.
- **كيف / how:** Install with `npx hyperframes add vfx-magnetic` (copies the full composition to compositions/vfx-magnetic.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: HTML-in-Canvas (canvas layoutsubtree + ctx.drawElementImage, experimental Chromium API), WebGL fragment shader, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 15 s; 1920x1080; duration 15 s
- **تثبيت / install:** `npx hyperframes add vfx-magnetic` (copies the full composition to compositions/vfx-magnetic`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/vfx-magnetic/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/vfx-magnetic/vfx-magnetic.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/vfx-magnetic.mdx`

#### UI-111 · إعلان تطبيق في يوتيوب · VPN YouTube Spot · 📦 بأمر تثبيت
- **ماذا / what:** Apple-style insert of a phone finding and installing a VPN app with sfx (sfx not shipped). [Local copy lacks 1 declared file(s), e.g. assets/vpn-sfx.wav.]
- **كيف / how:** Install with `npx hyperframes add vpn-youtube-spot` (copies the full composition to compositions/vpn-youtube-spot.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: inline SVG, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 7 s; 1920x1080; duration 7 s
- **تثبيت / install:** `npx hyperframes add vpn-youtube-spot` (copies the full composition to compositions/vpn-youtube-spot`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/vpn-youtube-spot/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/vpn-youtube-spot/vpn-youtube-spot.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/vpn-youtube-spot.mdx`

#### UI-112 · صفحة ويب مائلة ثلاثية الأبعاد تتمرر · 3D tilted webpage scroll · 📦 بأمر تثبيت
- **ماذا / what:** A full webpage as a tilted 3D card whose content scrolls with spring easing to reveal sections; pairs with keyword glow.
- **كيف / how:** Read hyperframes-animation/rules/3d-page-scroll.md; build on ONE paused GSAP timeline with fromTo explicit states, transforms/opacity only, deterministic hashes, inside a class=clip scene.
- **أرقام / params:** perspective + rotateY/rotateX tilt; border-radius 24 px; shadow 40px 30px 80px rgba(0,0,0,0.45)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/3d-page-scroll.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules-index.md`

#### UI-113 · مربع تتبع ذكاء اصطناعي · AI detection tracking box · 📦 بأمر تثبيت
- **ماذا / what:** Yellow L-bracket corner box with a fluctuating 95-99% confidence label follows a target on a sine arc; box derived from target each frame.
- **كيف / how:** Read hyperframes-animation/rules/ai-tracking-box.md; build on ONE paused GSAP timeline with fromTo explicit states, transforms/opacity only, deterministic hashes, inside a class=clip scene.
- **أرقام / params:** color #facc15; corners 48x48 px border 6 px; confidence 95-99%
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/ai-tracking-box.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules-index.md`

#### UI-114 · تمدد عنصر مثبت الحافة · Anchored layout expand · 📦 بأمر تثبيت
- **ماذا / what:** An edge-pinned container grows/collapses on one axis (pill -> dropdown, panel growing a sub-task stack) using mask + sheet slide or proxy scaleY with inverse counter-scale, since width/height tweens are banned.
- **كيف / how:** Read hyperframes-animation/rules/anchored-layout-expand.md; build on ONE paused GSAP timeline with fromTo explicit states, transforms/opacity only, deterministic hashes, inside a class=clip scene.
- **أرقام / params:** row fade stagger power2.out; collapse power3.in immediateRender false
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/anchored-layout-expand.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules-index.md`

#### UI-115 · ضغط وتحرير زر نابض · Press-release spring button · 📦 بأمر تثبيت
- **ماذا / what:** Linear compression then spring recovery on the same property with shadow shrink, release burst and background glow.
- **كيف / how:** Read hyperframes-animation/rules/press-release-spring.md; build on ONE paused GSAP timeline with fromTo explicit states, transforms/opacity only, deterministic hashes, inside a class=clip scene.
- **أرقام / params:** press linear scale 1->PRESS_SCALE; recovery spring
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/press-release-spring.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules-index.md`

#### UI-116 · ضغط المؤشر والزر معا · Cursor + button press reaction · 📦 بأمر تثبيت
- **ماذا / what:** Cursor approaches, lands, cursor and button compress together then spring back.
- **كيف / how:** Read hyperframes-animation/rules/physics-press-reaction.md; build on ONE paused GSAP timeline with fromTo explicit states, transforms/opacity only, deterministic hashes, inside a class=clip scene.
- **أرقام / params:** approach power2.inOut; press scale 1-PRESS_INTENSITY power1.in (to ~0.9); release back.out(BOUNCE)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/physics-press-reaction.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules-index.md`

#### UI-117 · نقرة المؤشر مع موجة دائرية · Cursor click ripple · 📦 بأمر تثبيت
- **ماذا / what:** Cursor moves to a target, depresses with it, and emits expanding ripple rings with attack-decay opacity; element in DOM from t=0 at opacity 0.
- **كيف / how:** Read hyperframes-animation/rules/cursor-click-ripple.md; build on ONE paused GSAP timeline with fromTo explicit states, transforms/opacity only, deterministic hashes, inside a class=clip scene.
- **أرقام / params:** ripple 100x100 px circle
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/cursor-click-ripple.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules-index.md`

#### UI-118 · سحب وإفلات بالمؤشر · Cursor drag and drop · 📦 بأمر تثبيت
- **ماذا / what:** Grab (press dip + lift), travel with a semi-transparent ghost locked to the cursor via matched tweens, drop-snap with selection chrome; fill-handle and corner-resize variants.
- **كيف / how:** Read hyperframes-animation/rules/cursor-drag.md; build on ONE paused GSAP timeline with fromTo explicit states, transforms/opacity only, deterministic hashes, inside a class=clip scene.
- **أرقام / params:** matched tweens same position/duration/ease; immediateRender false
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/cursor-drag.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules-index.md`

#### UI-119 · عدة مؤشرات تعمل معا · Multi-cursor collaborative choreography · 📦 بأمر تثبيت
- **ماذا / what:** 2-4 labeled cursors with name-tag pills work one canvas on interleaved beats, zone-partitioned paths, one payoff at a time.
- **كيف / how:** Read hyperframes-animation/rules/multi-cursor-choreography.md; build on ONE paused GSAP timeline with fromTo explicit states, transforms/opacity only, deterministic hashes, inside a class=clip scene.
- **أرقام / params:** actions on alternating beats ~1.2/2.6/4.0 s; legs power2.inOut; press scale 0.88 0.07 s yoyo
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/multi-cursor-choreography.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules-index.md`

#### UI-120 · تحكم وهدف يتغيران معا · Control-target live sync · 📦 بأمر تثبيت
- **ماذا / what:** A scrubbed/typed/picked control and its bound target change in the same beat: readout tween + target transform share one label, duration and ease.
- **كيف / how:** Read hyperframes-animation/rules/control-target-sync.md; build on ONE paused GSAP timeline with fromTo explicit states, transforms/opacity only, deterministic hashes, inside a class=clip scene.
- **أرقام / params:** tl.addLabel('edit1'); shared SCRUB_DUR/SCRUB_EASE
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules/control-target-sync.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/rules-index.md`

#### UI-121 · مخطط مشهد: عرض واجهة بمؤشر · Blueprint: Cursor UI demo · 📦 بأمر تثبيت
- **ماذا / what:** A custom cursor drives a reconstructed app UI through clicks/hovers/drags while the camera chases each interaction.
- **كيف / how:** Pick from hyperframes-animation/blueprints-index.md by role, then read hyperframes-animation/blueprints/cursor-ui-demo.md for the multi-phase recipe; cite blueprint id per beat in the storyboard.
- **أرقام / params:** duration 4.0-12.9 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/cursor-ui-demo.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints-index.md`

#### UI-122 · مخطط مشهد: عرض جهاز أو نافذة عائمة · Blueprint: Device surface showcase · 📦 بأمر تثبيت
- **ماذا / what:** A device mockup or floating window held as hero while screens cycle a real flow; static tour, push-scroll, 3D hand demo, stepwise flow, carousel.
- **كيف / how:** Pick from hyperframes-animation/blueprints-index.md by role, then read hyperframes-animation/blueprints/device-surface-showcase.md for the multi-phase recipe; cite blueprint id per beat in the storyboard.
- **أرقام / params:** duration 5-11.3 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/device-surface-showcase.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints-index.md`

#### UI-123 · مخطط مشهد: كتابة الطلب وإرساله وتوليد النتيجة · Blueprint: Prompt type-submit-generate · 📦 بأمر تثبيت
- **ماذا / what:** A prompt types into a real input and the machine answers: status theater into streaming answer, action log, diff cards, chart or artifact; or cut at submit.
- **كيف / how:** Pick from hyperframes-animation/blueprints-index.md by role, then read hyperframes-animation/blueprints/prompt-type-submit-generate.md for the multi-phase recipe; cite blueprint id per beat in the storyboard.
- **أرقام / params:** duration 5.2-12 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/prompt-type-submit-generate.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints-index.md`

#### UI-124 · مخطط مشهد: مسرح تقدم الوكيل الذكي · Blueprint: Agent progress theater · 📦 بأمر تثبيت
- **ماذا / what:** A trigger hands the frame to the machine: loaders and status phrases swap, then a checklist/findings card cascades and checks off, or a conversation builds to a push-in.
- **كيف / how:** Pick from hyperframes-animation/blueprints-index.md by role, then read hyperframes-animation/blueprints/agent-progress-theater.md for the multi-phase recipe; cite blueprint id per beat in the storyboard.
- **أرقام / params:** duration 4.2-11.6 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/agent-progress-theater.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints-index.md`

#### UI-125 · مخطط مشهد: تحرير لوحة مع تحديث حي · Blueprint: Panel edit live sync · 📦 بأمر تثبيت
- **ماذا / what:** Inspector panel bound to a target surface; a cursor scrubs/picks/retypes and the surface updates live in the same beat.
- **كيف / how:** Pick from hyperframes-animation/blueprints-index.md by role, then read hyperframes-animation/blueprints/panel-edit-live-sync.md for the multi-phase recipe; cite blueprint id per beat in the storyboard.
- **أرقام / params:** duration 5.3-11.9 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/panel-edit-live-sync.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints-index.md`

#### UI-126 · مخطط مشهد: تمرير السجل ثم كشف الناتج · Blueprint: Transcript scroll to artifact reveal · 📦 بأمر تثبيت
- **ماذا / what:** The frame travels down a long agent transcript/feed as evidence, then one focal interaction pivots into an artifact reveal.
- **كيف / how:** Pick from hyperframes-animation/blueprints-index.md by role, then read hyperframes-animation/blueprints/transcript-scroll-artifact-reveal.md for the multi-phase recipe; cite blueprint id per beat in the storyboard.
- **أرقام / params:** duration 5-11.8 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/transcript-scroll-artifact-reveal.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints-index.md`

#### UI-127 · أمثلة مشاهد جاهزة (13) · Worked scene examples (13 HTML) · 📦 بأمر تثبيت
- **ماذا / what:** Runnable 1920x1080 scene files: brand-reveal-assemble-zoom (5 s), comparison-split-cards (5 s), concept-demo-decode-pan (7 s), cta-morph-press (5.5 s), cta-orbit-collapse (6.5 s), demo-page-scroll-spotlight (9 s), hook-counter-burst (3.5 s), messaging-multi-phrase (7.5 s), metric-video-text-pivot (6…
- **كيف / how:** Open hyperframes-animation/examples/<name>.html as ground-truth for blueprints.
- **أرقام / params:** 1920x1080; 3.5-9 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/examples/hook-counter-burst.html` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/examples/proof-logo-chain.html`

#### UI-128 · استعلام العنصر المحدد في الاستوديو · Studio selection context query · 📦 بأمر تثبيت
- **ماذا / what:** When the user says 'this element', query the current Studio selection instead of guessing.
- **كيف / how:** npx hyperframes preview --context --json --context-fields selection; use selection.target.hfId.
- **تثبيت / install:** `npx hyperframes preview --context --json --context-fields selection`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-cli/SKILL.md`

#### UI-129 · فئة موشن: تحريك صفحة ويب · Motion-graphics category: Webpage animation · 📦 بأمر تثبيت
- **ماذا / what:** Category module: capture a URL then scroll-through, UI reveal, cursor demo, region callouts.
- **كيف / how:** Director sets category 'webpage' in shot-plan.json; builder follows motion-graphics/categories/webpage/module.md reuse-first.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/motion-graphics/categories/webpage/module.md` · `kosif-one/vendor/hyperframes/skills/motion-graphics/SKILL.md`

#### UI-130 · فئة موشن: بطاقة تغريدة متحركة · Motion-graphics category: Animated tweet card · 📦 بأمر تثبيت
- **ماذا / what:** Category module: real post (author, handle, avatar, text, metrics) animated ~4-8 s.
- **كيف / how:** Director sets category 'tweet' in shot-plan.json; builder follows motion-graphics/categories/tweet/module.md reuse-first.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/motion-graphics/categories/tweet/module.md` · `kosif-one/vendor/hyperframes/skills/motion-graphics/SKILL.md`

#### UI-131 · قوالب محرر الكود والطرفية · Code-snippet IDE/terminal theme blocks (24) · 📦 بأمر تثبيت
- **ماذا / what:** Ready ~11-12 s compositions of a full VS Code workbench (12 themes: dark-plus, light-plus, dark-modern, light-modern, dark-2026, light-2026, monokai, solarized-light, ...) with per-char typing and pytest terminal, or macOS Terminal.app (12 profiles: basic, clear-dark, clear-light, grass, homebrew, m…
- **كيف / how:** Install the theme block (e.g. code-snippet-dark-modern, code-snippet-apple-terminal-pro) and edit codeLines.
- **أرقام / params:** 24 themes
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/pr-to-video/references/code-vocabulary.md` · `kosif-one/vendor/hyperframes/registry/blocks/code-snippet-dark-modern`

#### UI-132 · واجهة HUD وتعليقات · HUD + projected callouts · 📦 بأمر تثبيت
- **ماذا / what:** Instrument panel HUD with title strip, timeline, charts; callouts projected from 3D each frame.
- **كيف / how:** shape-kit.js / lab-kit.js in a 3D project; read references/shape-kit.md
- **أرقام / params:** hud(root,W,H); addCallout({anchor,label,title,text,measure}); camera.updateMatrixWorld() first
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:101` · `100-superskills/skills/kosif-montage-motion/SKILL.md:113` · `100-superskills/skills/kosif-montage-motion/CHANGELOG.md`

#### UI-133 · مؤشر فأرة يتحرك ويضغط · Cursor actor with press · 📦 بأمر تثبيت
- **ماذا / what:** A synthetic mouse cursor travels through timed stops, presses a button (with the button reacting) and exits.
- **كيف / how:** cur = M.cursor(stage, {size:34}); M.moveCursor(tl, cur, [{t, x, y}…], {hold:[t]}); M.press(tl, cur, at, {target}); exit x +=180, y +=150, opacity 0, E.exit.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/index.html:84` · `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:404`

#### UI-134 · شرائح خطوات بحالات · HUD stepper chips with states · 📦 بأمر تثبيت
- **ماذا / what:** A six-step progress row (SHAPE JOINT LOAD BREAK SWAP RANK) shows done, current and failure states while the film plays.
- **كيف / how:** .chip Mono 21 px/700, radius 14; .done mint text; .on lime #d0ff6a fill with 34 px glow; .bad coral #ff907a fill; class recomputed per frame from stage index.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/index.html:30` · `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/index.html:92`

#### UI-135 · عرض واجهة: ضغط زر ثم شريط تقدم · Button press → progress bar UI demo · 📦 بأمر تثبيت
- **ماذا / what:** A product-demo beat: a button appears, a cursor clicks it, the button flattens into a progress bar that fills linearly while a frame counter climbs.
- **كيف / how:** #pill 400×100 radius 50 red; press at b(6); pill → scaleX 2.0/scaleY .24 in .34 s E.inOut; #bar 800×24 track #262b29; #fill width 0→800 linear 1.1 s ('data is linear'); counter 0→900 ',' separator 120 px.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/index.html:78` · `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/index.html:92`

#### UI-136 · فيديو إطلاق · Launch video brag · 📦 بأمر تثبيت
- **ماذا / what:** Site/app launch film.
- **كيف / how:** kmotion brag init DIR|URL -> plan -> build -> deliver
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/operating-manual.md` · `100-superskills/skills/kosif-montage-motion/scripts/launch.py` · `100-superskills/skills/kosif-montage-motion/tests/test_launch.py`

#### UI-137 · شريط تقدم · Progress bar overlay · 📦 بأمر تثبيت
- **ماذا / what:** Bar growing from right.
- **كيف / how:** overlays type progress {color,height,from,y}
- **أرقام / params:** height 10
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/timeline-schema.md`

#### UI-138 · تكامل: frontend-design skill · Integration: frontend-design skill · 📦 بأمر تثبيت
- **ماذا / what:** Catalogued skill/MCP/library (link only; not installed here).
- **كيف / how:** see official setup
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`

#### UI-139 · تكامل: Hana by Spline · Integration: Hana by Spline · 📦 بأمر تثبيت
- **ماذا / what:** Catalogued skill/MCP/library (link only; not installed here).
- **كيف / how:** see official setup
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`

#### UI-140 · تكامل: Rive CLI/RML · Integration: Rive CLI/RML · 📦 بأمر تثبيت
- **ماذا / what:** Catalogued skill/MCP/library (link only; not installed here).
- **كيف / how:** see official setup
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`

#### UI-141 · مؤشر فأرة بفيزياء لعروض الواجهات · Physics cursor for UI demos · 📦 بأمر تثبيت
- **ماذا / what:** A drawn cursor that moves through timed stops on Hermite curves (stopping at zero velocity where asked) and presses with a squash on clicks, also pressing the target.
- **كيف / how:** c=M.cursor(stage,{size:28,fill:'#111',stroke:'#fff'}); M.moveCursor(tl,c,[{t,x,y}...],{hold:[...]}) sampled 60 fps; M.press(tl,c,at,{target,down:.97}).
- **أرقام / params:** press to .88 over 4 frames, release 8 frames; travel 36-48 frames
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/whatsapp-motion/projects/success/assets/motion-kit.js:403-437`

#### UI-142 · موك أب HTML · HTML/CSS device/package mockup · 📦 بأمر تثبيت
- **ماذا / what:** Place image inside device/packaging with CSS shadows, screenshot at 2x.
- **كيف / how:** Playwright
- **أرقام / params:** 2x DPR
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/product-photo-mockups/SKILL.md:24`

#### UI-143 · مؤشر فأرة واقعي · UI cursor with physics · 📦 بأمر تثبيت
- **ماذا / what:** A drawn arrow cursor moved through timed stops by Hermite interpolation (zero-velocity holds), with press/hover feedback on a target.
- **كيف / how:** c = MOTION.cursor(stage,{size,fill,stroke}); MOTION.moveCursor(tl,c,[{t,x,y},...],{hold:[t...]}); MOTION.press(tl,c,at,{target,down}).
- **أرقام / params:** size 28 px (h ×1.22), drop-shadow 0 6 8 rgba(0,0,0,.28); press scale .88 over 4 f, back over 8 f; target .97; rule: arcs 15-25% of path, 36-48 f travel
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:404`

#### UI-144 · قرص القياس · Measuring stage disc with scan sweep · 📦 بأمر تثبيت
- **ماذا / what:** Shader disc with grid, rings, 36 ticks and a radial scan sweep, plus a contact shadow.
- **كيف / how:** const d = K3S.stageDisc({radius, color, shadow}); d.userData.mat.uniforms.uScan.value = r.
- **أرقام / params:** radius .32 m, colour #9dffb4, shadow opacity .42, grid R/8
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/shape-kit.js:343`

#### UI-145 · واجهة عدّادات · Instrument-panel HUD with 3D callouts · 📦 بأمر تثبيت
- **ماذا / what:** Title strip, timeline bars, three live chart panels and dashed-ring callouts projected from 3D anchors with leader lines and measurement chips.
- **كيف / how:** const H = K3.hud(root, W, H, {title, subtitle, panels, accent, ink, paper, font, seed}); H.addCallout({anchor, label, title, text, side, measure}); H.update(t, camera, {stage, side, duration}).
- **أرقام / params:** lime #a8ff3c, ink #0f1512, paper #f4f2ec; IBM Plex Mono/Consolas; top 8.5% H, bottom 20% H; bars every 7 px
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/lab-kit.js:207`

#### UI-146 · لصق أي شيء · Paste anything (Ctrl+V) routing · 📦 بأمر تثبيت
- **ماذا / what:** Ctrl+V on the window routes a copied picture to the image painter, copied image files to open_image, and copied code/SVG/HTML to the code panel which runs it.
- **كيف / how:** Studio.paste_any uses ImageGrab.grabclipboard and a regex for code markers.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/studio.py:1221`

#### UI-147 · لوحة الكود · Code panel for AI code · 📦 بأمر تثبيت
- **ماذا / what:** A dark code window with run (Ctrl+Enter), paste, copy, save/open file, save as scene, clear, copy-AI-instructions, edit button, examples dropdown and an error box showing the real traceback.
- **كيف / how:** Studio.open_code (Ctrl+K); examples from examples/ (pil_house.py, svg_rocket.svg, matplotlib_flower.py, broken_code.py).
- **أرقام / params:** editor bg #100e15, error box #1d1218 / #ff9a9a, Consolas 11
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/studio.py:658` · `kosif-studio/examples/pil_house.py` · `kosif-studio/examples/broken_code.py`

#### UI-148 · لغة عرض الواجهات بالمؤشر · Cursor-driven UI demo grammar · 📦 بأمر تثبيت
- **ماذا / what:** Product-demo beats: a pill lands with contact squash, a cursor travels a path and presses it, the button flattens into a progress bar, a prompt types on, the shape iris-floods the frame, counters roll and a code string decodes.
- **كيف / how:** M.cursor, moveCursor (with holds), press, typeOn, flood, counter, scramble, morphPath, squash
- **أرقام / params:** cursor size 30-34; typeOn cps 46; flood dur 0.3 s; counter 280→300 'fps'; morph circle→square 0.6 s; push 1→1.18
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/projects/kit_v3_demo/index.html:1` · `kosif-studio/motion/projects/showreel/index.html:78`

#### UI-149 · استعراض SaaS · Style: SaaS demo (saas-demo) · 📦 بأمر تثبيت
- **ماذا / what:** Rebuilt app UI with cursor, clicks and responses.
- **كيف / how:** Layered DOM/SVG UI; cursor 380-700ms cubic-bezier(.2,.8,.2,1); press 80/140ms; 8px grid, radii 8/16/24. Scaffold: python3 tools/kosif.py scaffold saas-demo <dir>.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `style:saas-demo` · `kosif-tool/playbooks/product-ui.md`

#### UI-150 · واجهات دقيقة · Style: UI micro-interactions (ui-micro) · 📦 بأمر تثبيت
- **ماذا / what:** Close-ups of single UI interactions: toggles, buttons, toasts.
- **كيف / how:** Hover 120-160ms, press scale 0.96, ripple 0->48px 320-400ms; focus zoom up to 1.4x with 2x render. Scaffold: python3 tools/kosif.py scaffold ui-micro <dir>.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `style:ui-micro` · `kosif-tool/playbooks/product-ui.md`

#### UI-151 · واجهة زجاجية · Style: Glass UI (glass-ui) · 📦 بأمر تثبيت
- **ماذا / what:** Frosted glassmorphism panels over colourful blurred backgrounds.
- **كيف / how:** CSS backdrop-filter blur + translucent fills + 1px inner highlight; use sparingly per playbook. Scaffold: python3 tools/kosif.py scaffold glass-ui <dir>.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `style:glass-ui` · `kosif-tool/playbooks/product-ui.md`

#### UI-152 · واجهات المنتج · Category: Product UI · 📦 بأمر تثبيت
- **ماذا / what:** Capability family 'product-ui' (82 catalog entries) with a dedicated bilingual playbook of timings and recipes.
- **كيف / how:** Read playbooks/product-ui.md (visual grammar, motion mechanics, scene recipes, QA); build in starters/html-canvas or starters/remotion; filter catalog with python3 tools/kosif.py list --category product-ui.
- **أرقام / params:** cursor 380-700ms cubic-bezier(.2,.8,.2,1); press 80ms/140ms spring k300 d20; 8px grid radii 8/16/24; 4 elevation tiers
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/playbooks/product-ui.md` · `kosif-tool/catalog/categories.json` · `kosif-tool/catalog/meta.json`

#### UI-153 · هاتف · Category: Phone · 📦 بأمر تثبيت
- **ماذا / what:** Capability family 'phone' (8 catalog entries) with a dedicated bilingual playbook of timings and recipes.
- **كيف / how:** Read playbooks/phone.md (visual grammar, motion mechanics, scene recipes, QA); build in starters/html-canvas or starters/remotion; filter catalog with python3 tools/kosif.py list --category phone.
- **أرقام / params:** screen 390x844; perspective 1200-1600px; yaw +-28 pitch +-8; entrance 700-900ms; tap ripple 0-64px 300ms; idle hover <=6px period>=3.2s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/playbooks/phone.md` · `kosif-tool/catalog/categories.json` · `kosif-tool/catalog/meta.json`

#### UI-154 · مكوّن Device في Remotion · Remotion Device component · 📦 بأمر تثبيت
- **ماذا / what:** React phone with spring entrance, tap press, glare pass, yaw-opposed shadow, island overlay.
- **كيف / how:** Inside CameraRig; uses easing.ts progress/easeOutExpo; perspective 1400; rotateX 4deg.
- **أرقام / params:** glare progress frames 10–36
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/playbooks/phone.md:106-143`

#### UI-155 · وصفة النقر وفتح نافذة · Click opens modal recipe · 📦 بأمر تثبيت
- **ماذا / what:** Cursor arc, hover, press, release, backdrop, panel spring, field stagger, focus zoom, dwell.
- **كيف / how:** Remotion CursorPress (travel 17 frames, pressAt 21, ripple 48 px, accent #19c37d) + modal at pressAt+5.
- **أرقام / params:** times 0/560/700/780/860/880/1000/1600/2200 ms; focus 1→1.3
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/playbooks/product-ui.md:77-89` · `kosif-tool/playbooks/product-ui.md:124-158`

#### UI-156 · واجهات وموبايل · UI and phone mockup film categories · 🔑 مفتاح/خدمة
- **ماذا / what:** Claude-coded product UI (windows from rounded rects, cursor on a curve that clicks, sliding panels, updating values) and phone mockups (rounded frame, clipped scrolling screen, tap ripples, eased tilt-in).
- **كيف / how:** FILM_CATS 'ui' and 'phone'; templates app-launch, saas-promo, feature-teaser, pricing, service-3, how-order, studio-reel.
- **الدليل / proof:** `app/public/js/00_editor.js:2007` · `app/public/js/00_editor.js:1777`

#### UI-157 · فيلم إطلاق منتج · Product launch film tool · 🔑 مفتاح/خدمة
- **ماذا / what:** Claude writes a launch story (hook, pain, reveal, 3 features, CTA); uploaded screen recordings/photos are cut fast on the beat under big kinetic titles, or a product-style motion film is drawn when there is no footage.
- **كيف / how:** AGENT.TOOLS.launch_film {product,pitch,duration}.
- **الدليل / proof:** `app/public/js/10_studio.js:4306` · `app/public/js/10_studio.js:4307`

#### UI-158 · تحويل موقع لفيديو · Website-to-video capture · 🔑 مفتاح/خدمة
- **ماذا / what:** Capture a URL to screenshots/assets then build product promo.
- **كيف / how:** hyperframes capture <url> --max-screenshots 21 --skip-vision.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/packages/cli.mdx`

#### UI-159 · التقاط موقع ويب · Website capture · 🔑 مفتاح/خدمة
- **ماذا / what:** Headless-Chrome crawl of a URL producing screenshots, extracted brand tokens (colors, fonts), text and assets, optional AI vision captions.
- **كيف / how:** npx hyperframes capture https://site -o ./capture [--json] [--skip-assets] [--skip-vision] [--max-screenshots 12] [--timeout 60000] [--capture-budget 90000].
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-cli/references/init-and-scaffold.md` · `kosif-one/vendor/hyperframes/packages/cli/src/commands/capture.ts`

#### UI-160 · فيديو إطلاق منتج من رابط موقع · Product launch video from a URL · 🔑 مفتاح/خدمة
- **ماذا / what:** Captures the real site (screenshots, tokens, text, assets, optional vision captions) and builds a narrated launch/promo or site tour (up to ~3 min, 30-90 s sweet spot) using the site's own visuals; hard stop on failed capture (no invented page).
- **كيف / how:** npx hyperframes capture '<URL>' -o ./capture --json; gate on ok:true and no capture/BLOCKED.md; then preset, storyboard, audio, frames, captions, transitions, render; stage-assets.mjs for user media.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/product-launch-video/SKILL.md` · `kosif-one/vendor/hyperframes/skills/product-launch-video/scripts/capture-skill-guardrails.test.mjs` · `kosif-one/vendor/hyperframes/skills/product-launch-video/scripts/stage-assets.test.mjs`

#### UI-161 · تكامل: Rive MCP · Integration: Rive MCP · 🔑 مفتاح/خدمة
- **ماذا / what:** Catalogued skill/MCP/library (link only; not installed here).
- **كيف / how:** see official setup
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`

#### UI-162 · تكامل: Figma MCP · Integration: Figma MCP · 🔑 مفتاح/خدمة
- **ماذا / what:** Catalogued skill/MCP/library (link only; not installed here).
- **كيف / how:** see official setup
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`

#### UI-163 · تكامل: Penpot MCP · Integration: Penpot MCP · 🔑 مفتاح/خدمة
- **ماذا / what:** Catalogued skill/MCP/library (link only; not installed here).
- **كيف / how:** see official setup
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`

#### UI-164 · تكامل: Paper Desktop MCP · Integration: Paper Desktop MCP · 🔑 مفتاح/خدمة
- **ماذا / what:** Catalogued skill/MCP/library (link only; not installed here).
- **كيف / how:** see official setup
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`

#### UI-165 · شريط مراحل يمتلئ · Progress stepper bar · 👁 شوهد في فيديو
- **ماذا / what:** white rounded card bottom-centre; 5 nodes connected by a line that fills; each node turns into a coloured check badge and label bolds when its stage starts
- **أرقام / params:** colours #f59e0b, #6366f1, #f59e0b, #14b8a6, #e11d48
- **الدليل / proof:** `style:isometric`

#### UI-166 · طلبات تعديل مع فرق الكود · Code diff edit rows · 👁 شوهد في فيديو
- **ماذا / what:** chat-like rows (Arabic request in a dark bar) reveal one by one; under each, the old line appears struck-through grey and the new line types in orange
- **أرقام / params:** row stagger ~1.2 s, strike draw 250 ms
- **الدليل / proof:** `style:plotter`

#### UI-167 · بطاقة سجل مباشر · Live log card · 👁 شوهد في فيديو
- **ماذا / what:** Dark rounded card with green live dot header, mono endpoint rows with check and '200' status appended/scrolling; footer price metric in accent
- **أرقام / params:** row interval ~120 ms, card radius 16 px
- **الدليل / proof:** `style:pm-0xfemyn-e114d3`

#### UI-168 · ساعة رقمية تتقدم دقيقة · Ticking clock display · 👁 شوهد في فيديو
- **ماذا / what:** big tabular numerals in a white box, flip 7:59→8:00 with small vertical slide; on reaching trigger time a message card drops into channel timeline
- **أرقام / params:** digit slide 200 ms
- **الدليل / proof:** `style:pm-0xnfrith-5be616`

#### UI-169 · جولة واجهة على هاتف · Phone UI walkthrough · 👁 شوهد في فيديو
- **ماذا / what:** Rounded phone frame with real app screens; state changes (select list item, tap word, play audio) animate with highlight, toast and button press
- **أرقام / params:** frame radius 40 px, shadow 0 30px 60px rgba(0,0,0,.12)
- **الدليل / proof:** `style:pm-1stnoel-c20a89`

#### UI-170 · بطاقة تعريف منبثقة مع إشعار حفظ · Definition pop card + saved toast · 👁 شوهد في فيديو
- **ماذا / what:** Selected word lifts into a card (word, translation, note) and a small pill toast with dot confirms saving
- **أرقام / params:** card scale 0.96->1 + fade 250 ms, toast 200 ms after
- **الدليل / proof:** `style:pm-1stnoel-c20a89`

#### UI-171 · قائمة مزايا تُعلّم تباعًا مع بطاقة سعر · Checklist tick-in pricing · 👁 شوهد في فيديو
- **ماذا / what:** Feature list items appear with check icon one by one (dim->solid), dark price card slides in beside
- **أرقام / params:** item stagger 300-400 ms aligned to narration
- **الدليل / proof:** `style:pm-1stnoel-c20a89`

#### UI-172 · ضغط اختصار لوحة المفاتيح · Keycap shortcut trigger · 👁 شوهد في فيديو
- **ماذا / what:** three rounded keycaps press down in sequence (translateY 3 px + shadow shrink); final key fills accent and triggers the next animation
- **أرقام / params:** 120 ms per key, 80 ms gap
- **الدليل / proof:** `style:pm-agonaliu-466a8f`

#### UI-173 · بحث يكتب نفسه ويظهر النتيجة · Type-to-search reveal · 👁 شوهد في فيديو
- **ماذا / what:** caret types a query, keyword recolours, then result card slides up with match meta line
- **أرقام / params:** 40 ms/char, result 350 ms easeOutBack
- **الدليل / proof:** `style:pm-agonaliu-466a8f`

#### UI-174 · نافذة متصفح وهمية · Browser chrome mock · 👁 شوهد في فيديو
- **ماذا / what:** Rounded window with traffic-light dots, URL pill, then the product UI inside; drop shadow 0 30px 60px rgba(0,0,0,.12)
- **أرقام / params:** radius 12px
- **الدليل / proof:** `style:pm-ai-baymax-0ef9dd`

#### UI-175 · مؤشر فأرة يتفاعل مع الواجهة · Simulated cursor interaction · 👁 شوهد في فيديو
- **ماذا / what:** SVG cursor moves on bezier paths with ease-in-out, switches to hand/I-beam on hover, click ripples, text typed into fields
- **أرقام / params:** move 600-900ms; click scale 0.9
- **الدليل / proof:** `style:pm-ai-baymax-0ef9dd`

#### UI-176 · تكبير البطاقة مع وصف · Card zoom tooltip · 👁 شوهد في فيديو
- **ماذا / what:** hovered card scales 2x with side tooltip
- **أرقام / params:** 150 ms
- **الدليل / proof:** `style:pm-aisongman-71ffac`

#### UI-177 · جدار شاشات مائل · Tilted screenshot wall · 👁 شوهد في فيديو
- **ماذا / what:** grid of screens rotateX/Z, panning
- **الدليل / proof:** `style:pm-aistocksavvy-3fb9f5`

#### UI-178 · إطار مقابض التحويل · Transform-handle frame · 👁 شوهد في فيديو
- **ماذا / what:** draw bbox with corner handles around rotating shape + rot readout
- **الدليل / proof:** `style:pm-ajith-io-b5626e`

#### UI-179 · تبويبات الخطوات · Step progress tabs · 👁 شوهد في فيديو
- **ماذا / what:** 3 coloured bars fill per step with checkmarks
- **الدليل / proof:** `style:pm-ajith-io-c52e09`

#### UI-180 · محاكاة رفع ملف · Mock upload flow · 👁 شوهد في فيديو
- **ماذا / what:** drop zone -> file card with progress then green check
- **أرقام / params:** ~1.5 s
- **الدليل / proof:** `style:pm-ajith-io-c52e09`

#### UI-181 · مقدمة كتابة الطلب في واجهة الدردشة · Prompt-typing intro · 👁 شوهد في فيديو
- **ماذا / what:** Recreate a chat composer card (greeting serif title, text box, send button) and type the brief at ~40 chars/s with blinking caret before cutting to the film
- **أرقام / params:** caret blink 530 ms
- **الدليل / proof:** `style:pm-alex-prompter-1ea044`

#### UI-182 · منزلق النتيجة · Score slider · 👁 شوهد في فيديو
- **ماذا / what:** slider fills to value with numeric readout
- **أرقام / params:** 0.88
- **الدليل / proof:** `style:pm-amol909s-27533e`

#### UI-183 · فقاعات سؤال وجواب · Chat bubble Q&A pop · 👁 شوهد في فيديو
- **ماذا / what:** grey question bubble then brand-colour answer bubble, scale 0->1 overshoot
- **أرقام / params:** 300 ms back.out
- **الدليل / proof:** `style:pm-anas0ra-e57aea`

#### UI-184 · نقر مؤشر على موقع · Cursor click on site mockup · 👁 شوهد في فيديو
- **ماذا / what:** cursor path to CTA, press scale 0.95, toast slides in
- **الدليل / proof:** `style:pm-andginja-333d32`

#### UI-185 · كتابة آلية مع كلمة متغيرة ملونة · Typewriter prompt with accent placeholder · 👁 شوهد في فيديو
- **ماذا / what:** type a query into a search/chat box; the variable placeholder '(your keyword)' renders in accent colour; blinking caret
- **أرقام / params:** 35 ms/char, caret blink 500 ms
- **الدليل / proof:** `style:pm-anthonyriera-9b1b2a`

#### UI-186 · حركة مؤشر فأرة مُخرجة · Fake cursor choreography · 👁 شوهد في فيديو
- **ماذا / what:** SVG cursor moves on bezier paths with ease-in-out to targets, press scale 0.9 on click, button state change
- **أرقام / params:** move 500-800 ms
- **الدليل / proof:** `style:pm-anthonyriera-9b1b2a`

#### UI-187 · مؤشر فأرة بهالة لونية ونقرة · Cursor with accent halo and click · 👁 شوهد في فيديو
- **ماذا / what:** arrow cursor homes on a live element position each frame (camera keeps drifting), a semi-transparent accent circle behind it; on click the halo shrinks/pulses and the target shows pressed state
- **أرقام / params:** halo #f0442c 40% alpha 36 px, click pulse 150 ms
- **الدليل / proof:** `style:pm-antonio-kodheli-490109`

#### UI-188 · تفتح البطاقة إلى صفحة التفاصيل · Tile bloom into detail page · 👁 شوهد في فيديو
- **ماذا / what:** FLIP-style: clicked tile scales/moves to the left video slot of the entry page while meta column and prompt block fade/slide in on the right
- **أرقام / params:** ~700 ms, stagger meta rows 60 ms
- **الدليل / proof:** `style:pm-antonio-kodheli-490109`

#### UI-189 · زر نسخ ثم إشعار تم النسخ · Copy button -> toast confirmation · 👁 شوهد في فيديو
- **ماذا / what:** cursor clicks 'Copy'; a black pill toast '✓ Copied' pops with scale 0.9->1 and fades
- **أرقام / params:** pop 200 ms, hold 600 ms
- **الدليل / proof:** `style:pm-antonio-kodheli-490109`

#### UI-190 · بداية من بكسل محدد بمقابض · Pixel selection origin · 👁 شوهد في فيديو
- **ماذا / what:** crosshair lines through centre, a blue square with 4 corner handles and a dimension tag '32 × 32' that scales up into the next scene
- **أرقام / params:** 500 ms, ease-in expo
- **الدليل / proof:** `style:pm-arjunsh1607-93005d`

#### UI-191 · رد مقترح يُكتب آليًا · AI draft reply typewriter · 👁 شوهد في فيديو
- **ماذا / what:** Under a post card, a 'Draft reply' box types text char by char with a solid coloured block caret; score badge pops on the post
- **أرقام / params:** 25-35 ms per char, caret blink 500 ms
- **الدليل / proof:** `style:pm-aschapmann-131210`

#### UI-192 · افتتاح بالطرفية · Terminal cold open · 👁 شوهد في فيديو
- **ماذا / what:** small dark terminal, prompt chevron, type command 40 ms/char, block cursor in accent
- **الدليل / proof:** `style:pm-astrodevil-3f2054`

#### UI-193 · دردشة وكيل ذكي بقائمة مهام تُشطب · Agent chat checklist · 👁 شوهد في فيديو
- **ماذا / what:** User bubble appears, assistant reply types, then a result card with checkbox list ticks each item with a small pop and a 'Ready' badge
- **أرقام / params:** tick stagger 250 ms; checkbox scale 0.6 -> 1
- **الدليل / proof:** `style:pm-bizibeast-10f264`

#### UI-194 · لوحة بيانات داكنة بخط أحادي · Dark mono data panel · 👁 شوهد في فيديو
- **ماذا / what:** translucent near-black rectangle with yellow mono header and key/value rows typed in; optional mini grid of green cells filling as progress
- **أرقام / params:** bg rgba(5,8,15,.85), mono 11 px, type 20 ms/char
- **الدليل / proof:** `style:pm-blueoctopusai-dd17bd`

#### UI-195 · بطاقات مهارات متناثرة · Dealt card cloud · 👁 شوهد في فيديو
- **ماذا / what:** Rounded cards with title + bullet subline spring in from below with random tilt ±8° around a central pill sentence
- **أرقام / params:** 6 cards, stagger 70 ms, spring k=180
- **الدليل / proof:** `style:pm-blushpetal795-0c85c2`

#### UI-196 · إضافة صفوف القائمة على الإيقاع · Beat-appended list rows · 👁 شوهد في فيديو
- **ماذا / what:** Inbox rows with line icon, serif title, tiny caps source; each new row enters on a beat with opacity 0->1 and y +8->0, divider line draws left->right
- **أرقام / params:** 250 ms easeOutQuad, one row per beat (~0.4-0.5 s)
- **الدليل / proof:** `style:pm-bogdandragomir-35e024`

#### UI-197 · إظهار جهازين قارئين · Device mockup reveal pair · 👁 شوهد في فيديو
- **ماذا / what:** Flat CSS e-reader (light bezel) and dark small reader, soft shadow, second slides in from right; screen content renders with noise-to-sharp
- **أرقام / params:** slide 400 ms easeOutCubic, shadow 0 20px 40px rgba(0,0,0,.12)
- **الدليل / proof:** `style:pm-bogdandragomir-35e024`

#### UI-198 · شريط مشغّل ثابت كمرساة · Persistent player bar anchor · 👁 شوهد في فيديو
- **ماذا / what:** Slim rounded pill at stage bottom with transport icons, thumbnail, title/artist, brand dot, progress bar advancing with time; stays while scenes change above
- **أرقام / params:** height 7% of stage, progress = t/duration
- **الدليل / proof:** `style:pm-brainextends-e19ac3`

#### UI-199 · كتابة بحث وظهور النتيجة · Search typewriter result · 👁 شوهد في فيديو
- **ماذا / what:** Input field appears, characters type at ~12 cps with caret, then one highlighted result row with thumbnail and green play icon slides down
- **أرقام / params:** row bg brand green at 15% alpha
- **الدليل / proof:** `style:pm-brainextends-e19ac3`

#### UI-200 · شريط دوّار بأطراف مقصوصة · Carousel strip with cropped edges · 👁 شوهد في فيديو
- **ماذا / what:** Horizontal row of covers translateX continuously, stage overflow:hidden crops edge cards; heading above, supporting line below
- **أرقام / params:** speed ~120 px/s
- **الدليل / proof:** `style:pm-brainextends-e19ac3`

#### UI-201 · شبكة أوسمة مقفلة ومفتوحة · Locked/unlocked badge grid · 👁 شوهد في فيديو
- **ماذا / what:** greyed icons with progress bars vs gold icons
- **الدليل / proof:** `style:pm-bthreeagency-b9b8d9`

#### UI-202 · لمسة مؤشر اليد · Hand cursor tap · 👁 شوهد في فيديو
- **ماذا / what:** pointer icon moves + scale pulse
- **الدليل / proof:** `style:pm-bthreeagency-b9b8d9`

#### UI-203 · لوحة تحكم حية · Live control panel overlay · 👁 شوهد في فيديو
- **ماذا / what:** right 20% panel with toggles; cursor clicks drive part animations
- **الدليل / proof:** `style:pm-buildfastwithai-ed9447`

#### UI-204 · تبديل بطاقة حالة · Status card swap · 👁 شوهد في فيديو
- **ماذا / what:** Glassy light-blue rounded card under product, content crossfades per beat with icon/number
- **أرقام / params:** beat ~1.25 s
- **الدليل / proof:** `style:pm-cansincengiz-me-cf68dd`

#### UI-205 · شريط زمني بمفاتيح حركة كواجهة · Timeline scrubber chrome · 👁 شوهد في فيديو
- **ماذا / what:** bottom bar with tick marks, diamond keyframes (filled when passed), chapter label above playhead, top-right timecode HH:MM:SS:FF
- **أرقام / params:** bar at 95% H, diamonds 8 px, mono/condensed 12 px
- **الدليل / proof:** `style:pm-chatgptastra-0d95c7`

#### UI-206 · مؤشر تقدم دائري بمربعات مدارية · Radial progress loader · 👁 شوهد في فيديو
- **ماذا / what:** outer arc stroke progress, inner tick ring, orbiting squares that fill blue as progress passes them, centre dot, % counter below
- **أرقام / params:** 0→62% over 1.2 s, 16 squares
- **الدليل / proof:** `style:pm-chatgptastra-0d95c7`

#### UI-207 · هبوط داخل إطار جهاز · Device frame landing · 👁 شوهد في فيديو
- **ماذا / what:** UI scales down into rounded phone bezel with toast notification
- **الدليل / proof:** `style:pm-dale-vaz-cc612a`

#### UI-208 · تحريك كاميرا فوق واجهة مائلة · Perspective UI pan · 👁 شوهد في فيديو
- **ماذا / what:** CSS rotateX 20° rotateY -15°, translate parent across
- **أرقام / params:** 3 s ease-in-out
- **الدليل / proof:** `style:pm-daniel-haida-8691d4`

#### UI-209 · تمثيل البحث في الواجهة · Search UI choreography · 👁 شوهد في فيديو
- **ماذا / what:** Type query char by char, filter chip activates, cursor clicks search button
- **أرقام / params:** 40 ms/char
- **الدليل / proof:** `style:pm-danilowm-d3720d`

#### UI-210 · شبكة بطاقات بوسم كود · Card grid with code tag · 👁 شوهد في فيديو
- **ماذا / what:** 2x4 rounded cards inside a dashed container, mono pill label '.class' at top-left; cards stagger in with blur and recolour through tints of one accent
- **أرقام / params:** accent #dd5027 + 3 tints, radius 12 px, stagger 50 ms
- **الدليل / proof:** `style:pm-ddryo-loos-300829`

#### UI-211 · قائمة أدوات وكيل ذكي تُشطب · Agent UI tool-call checklist · 👁 شوهد في فيديو
- **ماذا / what:** chat card with prompt text, then rows of tool calls each getting a green check in sequence (~250 ms apart), terminal pane alongside types output
- **أرقام / params:** mono 11-13 px, green check #2bb673
- **الدليل / proof:** `style:pm-ddryo-loos-300829`

#### UI-212 · إطار هاتف يعرض اللعبة · Phone mock-up with live game · 👁 شوهد في فيديو
- **ماذا / what:** rounded phone frame left, gameplay clip masked inside, theme switches inside on a beat; device chips appear one by one under the copy
- **أرقام / params:** chip stagger ~150 ms, pill outline 1.5 px lime
- **الدليل / proof:** `style:pm-deifosv-04e4d3`

#### UI-213 · تحول حاوية بين حالات الواجهة · Container morph between UI states · 👁 شوهد في فيديو
- **ماذا / what:** animate width/height/border-radius of one div; swap inner content with 150 ms fade
- **أرقام / params:** dur 500 ms, easeInOutCubic
- **الدليل / proof:** `style:pm-demonugc-4c5753`

#### UI-214 · مؤشر تحميل إلى علامة صح · Spinner to checkmark · 👁 شوهد في فيديو
- **ماذا / what:** rotating arc 0.8 s, collapse to circle, stroke-dashoffset check draw 250 ms
- **الدليل / proof:** `style:pm-demonugc-4c5753`

#### UI-215 · مؤشر فأرة كممثل · Scripted cursor actor · 👁 شوهد في فيديو
- **ماذا / what:** SVG cursor moves on bezier, scale 0.9 on click
- **أرقام / params:** glide 600 ms ease-out
- **الدليل / proof:** `style:pm-demonugc-4c5753`

#### UI-216 · كبسولات إنجازات · Win chips scatter · 👁 شوهد في فيديو
- **ماذا / what:** checked rounded chips pop in stagger 100 ms
- **الدليل / proof:** `style:pm-devius-maximus-beab45`

#### UI-217 · شريط تحميل · Progress bar tease · 👁 شوهد في فيديو
- **ماذا / what:** bar stuck at 9% with spinner joke
- **الدليل / proof:** `style:pm-devius-maximus-beab45`

#### UI-218 · موكاب هاتف · Phone UI mockup · 👁 شوهد في فيديو
- **ماذا / what:** rounded device frame, internal UI animates
- **الدليل / proof:** `style:pm-devius-maximus-beab45`

#### UI-219 · أيقونات تطبيقات عائمة حول العنوان · Floating app-icon tiles · 👁 شوهد في فيديو
- **ماذا / what:** White rounded tiles (radius 14 px, soft shadow) with icons placed on an invisible ellipse around the hero; each bobs with sine offset
- **أرقام / params:** amplitude 6-10 px, period 2.5-3.5 s, phase offset per tile
- **الدليل / proof:** `style:pm-elliot-garreffa-f334bc`

#### UI-220 · مؤشر فأرة وهمي يبرز صفًا · Fake cursor hover highlight · 👁 شوهد في فيديو
- **ماذا / what:** Animate an SVG arrow cursor along an eased path to a row; on arrival draw blue outline + light fill on that row
- **أرقام / params:** travel 600-800 ms easeInOutCubic; outline 1.5 px accent
- **الدليل / proof:** `style:pm-elliot-garreffa-f334bc`

#### UI-221 · بطاقة تتحول للخطوة التالية · Shared-element card morph · 👁 شوهد في فيديو
- **ماذا / what:** animate one card's width/height/position and crossfade its content to the next step's layout (FLIP)
- **أرقام / params:** 400-500 ms easeInOutCubic
- **الدليل / proof:** `style:pm-en-ra-81c6dd`

#### UI-222 · مؤشر يقود العرض · Scripted demo cursor · 👁 شوهد في فيديو
- **ماذا / what:** SVG cursor follows bezier paths to targets, scale 0.9 on click, triggers button states
- **أرقام / params:** move 500-700 ms
- **الدليل / proof:** `style:pm-en-ra-81c6dd`

#### UI-223 · سرد بأقسام بالتمرير · Scroll-driven section storytelling · 👁 شوهد في فيديو
- **ماذا / what:** pin each section, trigger animations at scroll progress
- **أرقام / params:** 5 sections ~6 s each
- **الدليل / proof:** `style:pm-ercankeskinx-ec2568`

#### UI-224 · قائمة تفاعلية تبدّل الصورة · Hover list with image swap · 👁 شوهد في فيديو
- **ماذا / what:** active item bold + bar marker, image crossfade 300 ms
- **الدليل / proof:** `style:pm-ercankeskinx-ec2568`

#### UI-225 · إعادة لعب حركة بحركة · Turn-by-turn board replay · 👁 شوهد في فيديو
- **ماذا / what:** place pieces every ~0.5 s with pop
- **الدليل / proof:** `style:pm-ezshine-c90d73`

#### UI-226 · شبكة شرائح نماذج · Model chip grid · 👁 شوهد في فيديو
- **ماذا / what:** avatar circle + name, stagger 60 ms
- **الدليل / proof:** `style:pm-ezshine-c90d73`

#### UI-227 · عرض أجهزة · Device mock finale · 👁 شوهد في فيديو
- **ماذا / what:** laptop + phone frames with live UI
- **الدليل / proof:** `style:pm-ezshine-c90d73`

#### UI-228 · شريط تعليق سفلي · Caption pill · 👁 شوهد في فيديو
- **ماذا / what:** rounded pill bottom centre with dash + sentence fading in
- **أرقام / params:** fade 300 ms
- **الدليل / proof:** `style:pm-fractadev-149adc`

#### UI-229 · تكدس فقاعات المحادثة · Chat bubble stack · 👁 شوهد في فيديو
- **ماذا / what:** bubbles slide y+12 and fade, alternate sides
- **أرقام / params:** stagger 500 ms
- **الدليل / proof:** `style:pm-fractadev-149adc`

#### UI-230 · تأشير حقول النموذج · Form field check-off · 👁 شوهد في فيديو
- **ماذا / what:** rows reveal with green check scaling 0->1
- **أرقام / params:** per row 300 ms
- **الدليل / proof:** `style:pm-fractadev-149adc`

#### UI-231 · تتابع إشعارات · Notification chip cascade · 👁 شوهد في فيديو
- **ماذا / what:** chips slide from below stagger 300 ms
- **الدليل / proof:** `style:pm-francoxavier33-d2dfd2`

#### UI-232 · قائمة تُشطب · Checklist strike · 👁 شوهد في فيديو
- **ماذا / what:** checkboxes fill and text strikes sequentially, progress bar
- **أرقام / params:** 150 ms/item
- **الدليل / proof:** `style:pm-francoxavier33-d2dfd2`

#### UI-233 · شرائح متصلة بخطوط منقطة · Chips connected by dotted lines · 👁 شوهد في فيديو
- **ماذا / what:** input chips appear left; dotted SVG paths draw from each chip into the phone UI
- **أرقام / params:** dash 2/4, draw 400 ms, stagger 120 ms
- **الدليل / proof:** `style:pm-gabrielbuzziv-4ff0c6`

#### UI-234 · ظهور الهاتف العائم · Floating phone reveal · 👁 شوهد في فيديو
- **ماذا / what:** Phone mockup rises from below frame on black, ease-out cubic
- **أرقام / params:** 600 ms, y 40%→0
- **الدليل / proof:** `style:pm-gautam-mer1-2ae354`

#### UI-235 · شبكة أنماط · Style variant grid · 👁 شوهد في فيديو
- **ماذا / what:** 3x2 grid of same frame with different caption styles labelled, stagger pop 60 ms
- **أرقام / params:** radius 16
- **الدليل / proof:** `style:pm-gautam-mer1-2ae354`

#### UI-236 · بطاقة ختامية بزر دعوة · CTA pill end card · 👁 شوهد في فيديو
- **ماذا / what:** dark rounded pill (radius 999) with white bold text and arrow; fade from 50% to 100% opacity and slight y settle 300 ms
- **أرقام / params:** padding 14x28px
- **الدليل / proof:** `style:pm-gonzalomacagno-2de1a9`

#### UI-237 · شبكة Bento لنظام التصميم · Bento design-system grid · 👁 شوهد في فيديو
- **ماذا / what:** 12-col grid with 24 px gutter and 5 modules: big red card with frame counter 'f 047/900' and progress bar, palette swatches, type specimen 'Aa' naming fonts, easing-curve plots labelled expo.out/power
- **كيف / how:** 12-col grid with 24 px gutter and 5 modules: big red card with frame counter 'f 047/900' and progress bar, palette swatches, type specimen 'Aa' naming fonts, easing-curve plots labelled expo.out/power3.inOut/back.out(1.7), BPM bar meter; modules reveal staggered
- **أرقام / params:** module stagger ~80 ms, counter linear to frame
- **الدليل / proof:** `style:pm-grace-sunnyy-29bc61`

#### UI-238 · إطار صفحة ويب وهمية · Fake web-page frame · 👁 شوهد في فيديو
- **ماذا / what:** render whole video as a browser page with embedded player & controls
- **الدليل / proof:** `style:pm-henkpoley-3d3407`

#### UI-239 · فهرس فصول ببطاقات أيقونات · Icon index grid · 👁 شوهد في فيديو
- **ماذا / what:** small cream cards with a thin line icon, two-digit number and serif label, popping in one by one in a 4-column grid to preview chapters
- **أرقام / params:** stagger ~400 ms, rise 12 px + fade
- **الدليل / proof:** `style:pm-henkvaness-0e06af`

#### UI-240 · بطاقات شاشات منظورية · Perspective screen cards · 👁 شوهد في فيديو
- **ماذا / what:** screenshots with rotateY -20°, slow drift, dark falloff
- **أرقام / params:** drift 40px/s
- **الدليل / proof:** `style:pm-heyiammallik-e72d17`

#### UI-241 · ظهور حاد مع صندوق تحديد · Bounding-box SNAP pop · 👁 شوهد في فيديو
- **ماذا / what:** word appears with zero easing in accent red, selection box with 8 handles and full-frame guide lines appear the same frame
- **أرقام / params:** cut, no tween
- **الدليل / proof:** `style:pm-himanshutwtxs-5f4b43`

#### UI-242 · رقائق رموز طائرة · Floating syntax chips · 👁 شوهد في فيديو
- **ماذا / what:** small rounded cards with tokens, spring scale 0→1, gentle float sine 2px/2s
- **الدليل / proof:** `style:pm-ho-ba-f3f0e9`

#### UI-243 · مؤشر يقود الواجهة · Self-driving cursor demo · 👁 شوهد في فيديو
- **ماذا / what:** bezier cursor path 600ms, click scale 0.9 + ring ripple, target button highlight
- **الدليل / proof:** `style:pm-hqmank-7c61f1`

#### UI-244 · سجل خطوات حي · Live action log panel · 👁 شوهد في فيديو
- **ماذا / what:** dark panel, mono lines appended with coloured verb tag (OBSERVE/CLICK/SCROLL)
- **الدليل / proof:** `style:pm-hqmank-7c61f1`

#### UI-245 · عرض تغيير لون التمييز · Accent recolour demo · 👁 شوهد في فيديو
- **ماذا / what:** Row of 6 swatches with a selection ring hopping; the UI mockup's highlight colour and the headline accent recolour in sync
- **أرقام / params:** hop every 350 ms
- **الدليل / proof:** `style:pm-iammxfschr-d68f90`

#### UI-246 · نافذة تأكيد تحذيرية · Danger confirm modal · 👁 شوهد في فيديو
- **ماذا / what:** Dark modal with red warning icon, SQL snippet block and red primary button pops in beside headline whose accent turns red
- **أرقام / params:** scale 0.96->1, 250 ms
- **الدليل / proof:** `style:pm-iammxfschr-d68f90`

#### UI-247 · لوحة كانبان يكتمل فيها السبرينت · Kanban sprint completion · 👁 شوهد في فيديو
- **ماذا / what:** Cards slide between TODO/DOING/DONE columns with count badges updating; checkmarks pop; burndown step-line descends; milestone dots light up in order
- **أرقام / params:** card move 400ms; stagger 150ms
- **الدليل / proof:** `style:pm-ibrahimwasim240-809370`

#### UI-248 · بطاقات ورقية كلوحة أفكار · Mood-board paper cards · 👁 شوهد في فيديو
- **ماذا / what:** Small document cards (table rows with grey value bars, plan drawing, sticky note) drop in with ±4 deg rotation and soft shadow, stamp scales in
- **أرقام / params:** drop 400 ms easeOutBack(1.4), stagger 150 ms
- **الدليل / proof:** `style:pm-ik-builds-b8bdcf`

#### UI-249 · تغير حالة البطاقة · UI card state change · 👁 شوهد في فيديو
- **ماذا / what:** input → confirm check badge crossfade
- **الدليل / proof:** `style:pm-imthatcarlos-e04bfe`

#### UI-250 · بطاقة أمر توليد مع شريط تقدّم · Prompt card with generate progress · 👁 شوهد في فيديو
- **ماذا / what:** rounded translucent card with prompt label and typed prompt, cursor clicks a pill button (ripple ring), thin progress bar fills while a tile grid on the right begins resolving tile by tile
- **أرقام / params:** click ripple 300 ms, progress ~1 s
- **الدليل / proof:** `style:pm-influencer-seo-ce8c33`

#### UI-251 · إطار مشغل فيديو · Player-card framing · 👁 شوهد في فيديو
- **ماذا / what:** place illustration inside rounded white card with progress bar and timecode
- **الدليل / proof:** `style:pm-itisrazak-3ad902`

#### UI-252 · شريط بطاقات · Card carousel · 👁 شوهد في فيديو
- **ماذا / what:** rounded cards slide horizontally
- **الدليل / proof:** `style:pm-jacksonfall-54b2ac`

#### UI-253 · حالة الشاشة كمؤشر تقدم · Monitor state as progress · 👁 شوهد في فيديو
- **ماذا / what:** Desk monitor content swaps: coloured code lines → image icon → progress bar fill → green screen with check, to narrate work state
- **أرقام / params:** check pop with sparkle 250 ms
- **الدليل / proof:** `style:pm-jake11moran-a269c4`

#### UI-254 · لوحة تحكم مائلة · Tilted dashboard reveal · 👁 شوهد في فيديو
- **ماذا / what:** perspective rotateX/Y small, slow drift
- **الدليل / proof:** `style:pm-jayscambler-3f8889`

#### UI-255 · مؤشر يحاكي الموافقة · Simulated cursor approval · 👁 شوهد في فيديو
- **ماذا / what:** animated cursor eases to button, press scale 0.95
- **أرقام / params:** 600 ms move
- **الدليل / proof:** `style:pm-jazzen-chen-4542ae`

#### UI-256 · أسهم شرح على الهاتف · Phone callout labels · 👁 شوهد في فيديو
- **ماذا / what:** Leader lines draw to labels in mono caps
- **أرقام / params:** stagger 120 ms
- **الدليل / proof:** `style:pm-jesscaroline7-1ff7cb`

#### UI-257 · نقطة ساخنة مع فقاعة إرشاد · Hotspot tooltip walkthrough · 👁 شوهد في فيديو
- **ماذا / what:** pulsing brand dot with ring on a target, cursor arrives, brand-blue tooltip card with copy, 'n of 4' counter and Back/Next buttons pops below
- **أرقام / params:** pulse 1 s loop, tooltip pop 200 ms
- **الدليل / proof:** `style:pm-jhylee95-e1152f`

#### UI-258 · دردشة ذكاء اصطناعي تقود الواجهة · AI chat drives UI split · 👁 شوهد في فيديو
- **ماذا / what:** left column: chat bubbles appear in sequence with typing; right column: product UI navigates to the referenced screen with a guided tooltip
- **أرقام / params:** bubble stagger ~600 ms, 40/60 split
- **الدليل / proof:** `style:pm-jhylee95-e1152f`

#### UI-259 · شارة حالة مباشرة · Live status pill · 👁 شوهد في فيديو
- **ماذا / what:** rounded pale-green pill with a pulsing green dot and text 'Agent online · time' under a hero word
- **أرقام / params:** dot pulse 1.2 s
- **الدليل / proof:** `style:pm-jhylee95-e1152f`

#### UI-260 · عنصر تحميل لامع يتحول إلى صورة · Skeleton shimmer to image reveal · 👁 شوهد في فيديو
- **ماذا / what:** Grey rounded placeholder with a diagonal light sweep loop, then crossfade + slight scale-in to the final image
- **أرقام / params:** shimmer 1.2 s loop, gradient 30% width; reveal 400 ms
- **الدليل / proof:** `style:pm-justincooperman-e7bbc4`

#### UI-261 · كتابة طلب ثم ضغط إرسال بالمؤشر · Prompt typing with cursor send · 👁 شوهد في فيديو
- **ماذا / what:** Type prompt character by character in a chat input, cursor moves to send button, button press and message bubble appears
- **أرقام / params:** 40 ms/char, caret 500 ms blink, click scale 0.92
- **الدليل / proof:** `style:pm-justincooperman-e7bbc4`

#### UI-262 · عدادات أداء على الشاشة · Performance HUD counters · 👁 شوهد في فيديو
- **ماذا / what:** Top-left serif title with key/bpm/gravity line; top-right clock 'm:ss.s / total', section name and 'N / total notes struck'; segmented top progress bar per section
- **أرقام / params:** update every frame, segments = sections
- **الدليل / proof:** `style:pm-kamstudiolabs-447565`

#### UI-263 · نقرة مؤشر على زر · Cursor click CTA · 👁 شوهد في فيديو
- **ماذا / what:** Cursor glides to button, press scale 0.95, dot burst ring around
- **الدليل / proof:** `style:pm-kangaroohere-b10f8d`

#### UI-264 · بطاقات واجهة مائلة عائمة · Floating tilted UI cards · 👁 شوهد في فيديو
- **ماذا / what:** perspective rotateY -15deg, slow drift
- **أرقام / params:** drift 10px
- **الدليل / proof:** `style:pm-kentcdodds-6fa8cf`

#### UI-265 · مسرح لوحة أداة تصميم · Design-tool canvas stage · 👁 شوهد في فيديو
- **ماذا / what:** Place all work as labelled frames on a large light canvas with a dot grid; add a file chip top-right, zoom-percentage badge bottom-left and keyboard-hint chip; move a virtual camera (scale + translate
- **كيف / how:** Place all work as labelled frames on a large light canvas with a dot grid; add a file chip top-right, zoom-percentage badge bottom-left and keyboard-hint chip; move a virtual camera (scale + translate on a container) instead of cutting
- **أرقام / params:** dot grid 24 px, canvas #e8e7e3
- **الدليل / proof:** `style:pm-kikelopezdesign-7cc9e8`

#### UI-266 · مؤشر متعاون باسم · Named multiplayer cursor · 👁 شوهد في فيديو
- **ماذا / what:** Accent-coloured arrow cursor with a pill name tag that follows bezier paths with ease-in-out and a slight overshoot; clicks shown by a brief scale-down
- **أرقام / params:** move 500-800 ms, tag radius 999
- **الدليل / proof:** `style:pm-kikelopezdesign-7cc9e8`

#### UI-267 · إطار تحديد مع وسم المقاس · Selection box with size tag · 👁 شوهد في فيديو
- **ماذا / what:** On click draw a 1.5 px accent rectangle around the frame with 4 square corner handles and a small filled accent tag below showing 'W x H'
- **أرقام / params:** appear 120-150 ms
- **الدليل / proof:** `style:pm-kikelopezdesign-7cc9e8`

#### UI-268 · شريط تقدّم السياق كواجهة · Context-bar progress HUD · 👁 شوهد في فيديو
- **ماذا / what:** Top HUD with model label, live red dot, thin progress bar = t/duration shown as 'context N%', and mm:ss.cs timer; persists over all scenes
- **أرقام / params:** bar 4px coral on #222, mono 22px at 1080w, margin 56px
- **الدليل / proof:** `style:pm-kloss-xyz-15182a`

#### UI-269 · بطاقة محادثة مع ردّ هيكلي · Chat card with skeleton reply · 👁 شوهد في فيديو
- **ماذا / what:** Rounded dark card, 'user' label, mono question typed on, then 3 grey skeleton bars grow to imply the answer loading
- **أرقام / params:** radius 40px, bar heights 30px, widths 40-70%
- **الدليل / proof:** `style:pm-kloss-xyz-15182a`

#### UI-270 · شريط مراحل بعلامات صح · Stepper pipeline with checks · 👁 شوهد في فيديو
- **ماذا / what:** 5 circle nodes on a line; the line fills accent from left node to node; each node pops to a filled check when reached; labels in mono under each
- **أرقام / params:** ~150 ms per node, node 18 px, line 3 px
- **الدليل / proof:** `style:pm-kmasiff-cc72cb`

#### UI-271 · شارات معلومات عائمة · Floating metric chips · 👁 شوهد في فيديو
- **ماذا / what:** small pill chips (dark '⏱ 0.7s', white '✉ 0 emails sent') pop at the corners of the main card with scale 0.8->1 and slight float
- **أرقام / params:** pop 200 ms back-out, float 4 px sine
- **الدليل / proof:** `style:pm-kmasiff-cc72cb`

#### UI-272 · عرض نموذج يقترح تصحيح الخطأ · Typo-suggestion form demo with cursor · 👁 شوهد في فيديو
- **ماذا / what:** type into a form field, show suggestion pill 'Did you mean …?', cursor moves and clicks it, field border turns green
- **أرقام / params:** type 45 ms/char, border colour change 200 ms
- **الدليل / proof:** `style:pm-kmasiff-cc72cb`

#### UI-273 · واجهة تحكم تفاعلية · Interactive control HUD · 👁 شوهد في فيديو
- **ماذا / what:** toggle chips and slider overlay on canvas
- **الدليل / proof:** `style:pm-konstantinsaifo-96fc89`

#### UI-274 · مؤشر وهمي · Fake cursor walkthrough · 👁 شوهد في فيديو
- **ماذا / what:** animated pointer with click scale 0.9
- **الدليل / proof:** `style:pm-l3d1c-0e35a3`

#### UI-275 · بلاطة توليد بنسبة · Generating tile progress · 👁 شوهد في فيديو
- **ماذا / what:** overlay % and gradient fill bar
- **الدليل / proof:** `style:pm-l3d1c-0e35a3`

#### UI-276 · لقطة واجهة مثبتة مع كتابة حيّة · Pinned screenshot with typing UI · 👁 شوهد في فيديو
- **ماذا / what:** real app/terminal screenshot as a card with dark rounded frame and shadow; overlay typed prompt/commands and tick rows sequentially
- **أرقام / params:** type 30-40 ms/char; tick every 300 ms
- **الدليل / proof:** `style:pm-lemomo-ai-0d9cff`

#### UI-277 · مقدمة بخط زمني HUD · HUD timeline intro · 👁 شوهد في فيديو
- **ماذا / what:** Thin baseline with ticks, playhead marker and corner timecode readouts on near-black; ball bounces on it
- **أرقام / params:** 1 px lines at 30% white, mono 10 px timecode
- **الدليل / proof:** `style:pm-leonkohli-6dc01b`

#### UI-278 · شريط بحث بحافة متدرجة متوهجة · Gradient-rim glowing search pill · 👁 شوهد في فيديو
- **ماذا / what:** White rounded pill with 1.5 px border using conic/linear gradient pink->violet->blue and a blurred copy below as underglow
- **أرقام / params:** radius 9999, glow blur 24 px opacity 0.35
- **الدليل / proof:** `style:pm-lester-tyy-f897f7`

#### UI-279 · عرض كتابة يقوده المؤشر · Cursor-driven typing demo · 👁 شوهد في فيديو
- **ماذا / what:** Animated cursor eases to field, click (scale 0.9), then characters appear on a fixed per-char interval with blinking caret
- **أرقام / params:** cursor bezier 600 ms, 60 ms/char, caret 530 ms blink
- **الدليل / proof:** `style:pm-lester-tyy-f897f7`

#### UI-280 · استعلام مع معاينة نتيجة · Query + preview dropdown · 👁 شوهد في فيديو
- **ماذا / what:** After a typed query, a small card drops under the field with thumbnail + venue caption
- **أرقام / params:** slide 12 px + fade 250 ms
- **الدليل / proof:** `style:pm-lester-tyy-f897f7`

#### UI-281 · مؤشر خط زمني · Timeline playhead · 👁 شوهد في فيديو
- **ماذا / what:** blocks track + line graph, blue playhead sweeps
- **الدليل / proof:** `style:pm-lexnlin-6161a6`

#### UI-282 · من الوصف إلى النتيجة · Prompt-to-result reveal · 👁 شوهد في فيديو
- **ماذا / what:** Dark empty frame, centred input pill; type prompt at ~35-50 ms/char, click send (button scale 0.9 + coloured ring pulse), then the result image fades/scales in full-frame
- **أرقام / params:** pill 600x48 px, ring 300 ms
- **الدليل / proof:** `style:pm-listudio-820c7b`

#### UI-283 · وكيل بقائمة مهام ولوحة لا نهائية · Agent checklist + canvas · 👁 شوهد في فيديو
- **ماذا / what:** Right chat panel: user request bubble, agent plan with 4 steps that tick in sequence; left canvas: connected node cards fill with images as each step completes; finish with a toast pill
- **أرقام / params:** tick every ~600 ms, node fill crossfade 300 ms
- **الدليل / proof:** `style:pm-listudio-820c7b`

#### UI-284 · عرض محادثة تستدعي أدوات · Chat-with-tools demo · 👁 شوهد في فيديو
- **ماذا / what:** Dark rounded window with title bar dots and a connector status; user message types into a right-aligned bubble; then tool-call rows (tool namespace · function) appear with spinner -> accent check; fin
- **كيف / how:** Dark rounded window with title bar dots and a connector status; user message types into a right-aligned bubble; then tool-call rows (tool namespace · function) appear with spinner -> accent check; final assistant line and result chip
- **أرقام / params:** type 35 ms/char, tool rows 600 ms apart
- **الدليل / proof:** `style:pm-majorbaguette-fb11d7`

#### UI-285 · نموذج ويب يملأ نفسه · Self-filling web form · 👁 شوهد في فيديو
- **ماذا / what:** Light card with fake URL bar; fields fill sequentially by typing, focus border moves to the active field, then submit button press
- **أرقام / params:** per field 0.6-1 s
- **الدليل / proof:** `style:pm-majorbaguette-fb11d7`

#### UI-286 · إشعار عثور · Found-item toast · 👁 شوهد في فيديو
- **ماذا / what:** top banner with icon, name, hint and n/N counter
- **الدليل / proof:** `style:pm-mandelduck-95fd08`

#### UI-287 · بناء بطاقة واجهة بمقاييس · Metric rows UI card build · 👁 شوهد في فيديو
- **ماذا / what:** Dark rounded card: left a post card, right 4 metric rows (label, pill tag, multiplier number, progress bar with median tick); draw bracket connector lines from post to rows, then per row: pill pop (sc
- **كيف / how:** Dark rounded card: left a post card, right 4 metric rows (label, pill tag, multiplier number, progress bar with median tick); draw bracket connector lines from post to rows, then per row: pill pop (scale 0.8->1), bar width grow, number count-up; colour bad metric pink and good ones green with 'BEAT CHANCE' outline badge
- **أرقام / params:** row stagger ~250 ms, bar grow 400 ms ease-out
- **الدليل / proof:** `style:pm-marouanegazouzi-6071d5`

#### UI-288 · زوايا ماسح ضوئي مع خط مسح · Scanner corner brackets + scan line · 👁 شوهد في فيديو
- **ماذا / what:** four L-shaped corners (different colours) snap from outside to frame a tilted card; a thin green line with soft glow sweeps top to bottom
- **أرقام / params:** corners 14 px stroke radius 12, snap 250 ms back-out, sweep 900 ms
- **الدليل / proof:** `style:pm-mehul4795-4a7007`

#### UI-289 · تظليل الأسطر كأنها محددة · Per-line OCR selection highlight · 👁 شوهد في فيديو
- **ماذا / what:** after the scan, semi-transparent lavender rectangles appear behind each line of the document in quick succession
- **أرقام / params:** stagger 70 ms, colour #c9cdf5 alpha 0.6
- **الدليل / proof:** `style:pm-mehul4795-4a7007`

#### UI-290 · بحث داخل الهاتف يصفّي النتائج · Phone search filter demo · 👁 شوهد في فيديو
- **ماذا / what:** phone mockup with list; query types into search field; non-matching rows fade to 30% and collapse, match moves up with yellow keyword highlight and '1 result'
- **أرقام / params:** type 80 ms/char, filter 400 ms
- **الدليل / proof:** `style:pm-mehul4795-4a7007`

#### UI-291 · فشل في الطرفية · Terminal fail beat · 👁 شوهد في فيديو
- **ماذا / what:** dark terminal types a command; dotted line to app; red X circle pops on connection
- **الدليل / proof:** `style:pm-melvynx-6cde6c`

#### UI-292 · تبديل نص داخل محرر · Live code token swap · 👁 شوهد في فيديو
- **ماذا / what:** editor card, highlight box around string, backspace+type new model name ~40 ms/char, synced ticker pill
- **الدليل / proof:** `style:pm-misbahsy-80eaec`

#### UI-293 · حقل كتابة متدرجة · Prompt typewriter field · 👁 شوهد في فيديو
- **ماذا / what:** chars appear 40 ms with caret, send button
- **الدليل / proof:** `style:pm-miskinho-443898`

#### UI-294 · تفرع بطاقة لعدة · One-to-many card fan · 👁 شوهد في فيديو
- **ماذا / what:** single card clones into platform variants spreading horizontally
- **أرقام / params:** stagger 80 ms
- **الدليل / proof:** `style:pm-miskinho-443898`

#### UI-295 · تبديل حالة التقويم · Calendar status flip · 👁 شوهد في فيديو
- **ماذا / what:** chips change Scheduled→Live with green check
- **الدليل / proof:** `style:pm-miskinho-443898`

#### UI-296 · طبقة المخطط الأزرق · Blueprint overlay mode · 👁 شوهد في فيديو
- **ماذا / what:** duplicate UI as outline-only version: 1 px cyan strokes, 8-10% cyan fill, text cyan; crossfade from solid UI to this layer while editing
- **أرقام / params:** stroke #3fb6d2 1px, fill rgba(63,182,210,.08), fade 400 ms
- **الدليل / proof:** `style:pm-moguzbulbul-6311b6`

#### UI-297 · مقابض تحديد كبرامج التصميم · Design-tool selection handles · 👁 شوهد في فيديو
- **ماذا / what:** show 8 small square handles around an element being dragged to signal 'editing'
- **أرقام / params:** handle 4px
- **الدليل / proof:** `style:pm-moguzbulbul-6311b6`

#### UI-298 · لوحة جانبية منزلقة · Slide-in side drawer · 👁 شوهد في فيديو
- **ماذا / what:** panel translates from right edge pushing content left
- **أرقام / params:** ~30% width, 500 ms ease-out
- **الدليل / proof:** `style:pm-moguzbulbul-6311b6`

#### UI-299 · بطاقة إحصاء تقفز · UI stat card punch · 👁 شوهد في فيديو
- **ماذا / what:** card glitch-in, percent counter, bars grow, cursor clicks button to 'sent'
- **أرقام / params:** counter 600 ms
- **الدليل / proof:** `style:pm-ndhabarde11-f155b4`

#### UI-300 · مؤشر فأرة معبّر · Expressive macOS cursor · 👁 شوهد في فيديو
- **ماذا / what:** SVG arrow (black fill, white outline, soft shadow) that glides with ease-out, rotates toward travel direction, scales up on hover, shrinks on press; camera zooms toward click
- **أرقام / params:** hover scale 1.55, press -15% over 3 frames
- **الدليل / proof:** `style:pm-notdwd-7de38a`

#### UI-301 · صندوق كتابة ينبثق ويكتب · Spring-out prompt box with typing · 👁 شوهد في فيديو
- **ماذا / what:** Glass box scales out from a menu-bar icon with width overshoot (~2.5%) then settles; type text ~1 char/frame with occasional 1-frame holds; caret always on
- **أرقام / params:** spring ~0.35 s, overshoot 1.025
- **الدليل / proof:** `style:pm-notdwd-7de38a`

#### UI-302 · مؤشر ماك يتجه حيث يتحرك · Directional macOS cursor · 👁 شوهد في فيديو
- **ماذا / what:** cursor rotation lerps toward velocity angle; hover scale 1.55, press shrink 15% for 3 frames; decelerating glide
- **أرقام / params:** 32x39 px arrow, black with white outline
- **الدليل / proof:** `style:pm-notdwd-c2037d`

#### UI-303 · كتابة بإيقاع بشري · Human-rhythm typing · 👁 شوهد في فيديو
- **ماذا / what:** ~1 char per frame with a 1-frame hold every 2-3 chars; caret always visible
- **أرقام / params:** seeded pattern, no Math.random
- **الدليل / proof:** `style:pm-notdwd-c2037d`

#### UI-304 · إطار شريط قوائم ماك · Mac menu-bar device frame · 👁 شوهد في فيديو
- **ماذا / what:** black bezel band with rounded corner, navy menu bar with white status icons, brand mark and three coloured dots, date/time text; wallpaper = blue gradient with thin white line art and a four-point spa
- **كيف / how:** black bezel band with rounded corner, navy menu bar with white status icons, brand mark and three coloured dots, date/time text; wallpaper = blue gradient with thin white line art and a four-point sparkle
- **أرقام / params:** menu bar ~60 px on 1080 stage
- **الدليل / proof:** `style:pm-notdwd-c2037d`

#### UI-305 · مقارنة قبل/بعد بمزلاج · Before/after split slider · 👁 شوهد في فيديو
- **ماذا / what:** clip-path inset on top image, animate divider x 0→100% ease-in-out 1.2 s
- **الدليل / proof:** `style:pm-oliahmed205-3e31c4`

#### UI-306 · شبكة نقاط الوجه · Face mesh draw-on · 👁 شوهد في فيديو
- **ماذا / what:** SVG dots pop stagger 20 ms then lines stroke-dashoffset 600 ms
- **الدليل / proof:** `style:pm-oliahmed205-3e31c4`

#### UI-307 · صف رقائق خيارات · Option chips row · 👁 شوهد في فيديو
- **ماذا / what:** three white rounded chips with mixed weight text ('Upload a CSV or PDF') pop in left to right below a pricing headline
- **أرقام / params:** stagger 100 ms, scale .95->1
- **الدليل / proof:** `style:pm-palashbagchi11-0a4b6b`

#### UI-308 · مؤشر وهمي يتفاعل مع الواجهة · Fake cursor UI walkthrough · 👁 شوهد في فيديو
- **ماذا / what:** typewriter text in an input field, then an arrow cursor glides on a bezier to a button, button scales 0.95 on click and triggers the next reveal
- **أرقام / params:** typing 40 ms/char, cursor move 500 ms easeInOut
- **الدليل / proof:** `style:pm-paulo-kombucha-96431c`

#### UI-309 · بطاقات بحدود سوداء · Brutalist bordered cards · 👁 شوهد في فيديو
- **ماذا / what:** 2px black border, header strip, mono label
- **الدليل / proof:** `style:pm-polydao-7a572b`

#### UI-310 · بطاقات مسار متتابعة · Sequential pipeline cards · 👁 شوهد في فيديو
- **ماذا / what:** 4 cards, active one tint lime + border, stagger 400 ms
- **الدليل / proof:** `style:pm-prasad-pilla-2c0cba`

#### UI-311 · قائمة أشرطة تقدم · Progress row list · 👁 شوهد في فيديو
- **ماذا / what:** rows with bar fill to 100% staggered
- **الدليل / proof:** `style:pm-prasad-pilla-2c0cba`

#### UI-312 · مربع تحديد · Selection box on headline · 👁 شوهد في فيديو
- **ماذا / what:** dashed box with handles + cursor
- **الدليل / proof:** `style:pm-quickdesignio-dd93d0`

#### UI-313 · صفوف تأشير · Checklist rows · 👁 شوهد في فيديو
- **ماذا / what:** dark pills with flag + name + check, staggered
- **أرقام / params:** 80 ms
- **الدليل / proof:** `style:pm-rammanq-f5a90f`

#### UI-314 · كتابة اسم المستخدم في حقل · Input claim typewriter · 👁 شوهد في فيديو
- **ماذا / what:** Input with fixed prefix 'domain/' and typed suffix at ~12 cps with caret, blue Claim button on right
- **أرقام / params:** field h 44px, radius 10px
- **الدليل / proof:** `style:pm-ratheejaisal-1f4538`

#### UI-315 · صفوف قائمة متتابعة بشارات حالة · Staggered list rows with status pills · 👁 شوهد في فيديو
- **ماذا / what:** Rows with app icon, name, MRR in mono and green 'Live' pill appear top to bottom with fade/slide
- **أرقام / params:** stagger 120 ms, translateY 8px
- **الدليل / proof:** `style:pm-ratheejaisal-1f4538`

#### UI-316 · جدار مصغرات يبرز المتميز · Outlier tile wall · 👁 شوهد في فيديو
- **ماذا / what:** Grid of cards, dim all but chosen to .3 opacity, scale 1.05
- **أرقام / params:** 27 tiles
- **الدليل / proof:** `style:pm-reyzostyle-b55864`

#### UI-317 · كتابة آلية داخل الواجهة · Typewriter in UI · 👁 شوهد في فيديو
- **ماذا / what:** Reveal chars 30/s with caret
- **الدليل / proof:** `style:pm-reyzostyle-b55864`

#### UI-318 · جدار بطاقات واجهة يطفو بعمق · Floating UI card wall in depth · 👁 شوهد في فيديو
- **ماذا / what:** grid of skeleton post cards (avatar circle, grey bars, icon badge) placed at varied translateZ; camera dolly in z; blur proportional to distance from focal plane
- **أرقام / params:** perspective 1200 px; 3-5 columns; blur 0-8 px; dolly 2 s
- **الدليل / proof:** `style:pm-robj3d3-b18fad`

#### UI-319 · سلسلة حالات سجل الوكلاء · Agent log status cascade · 👁 شوهد في فيديو
- **ماذا / what:** List rows flip queued→running with lime dot, stagger 150 ms; footer counters tick
- **الدليل / proof:** `style:pm-robvjourney-ce3e1a`

#### UI-320 · منزلقات إعدادات تتحرك مع ذكرها · Settings sliders synced to narration · 👁 شوهد في فيديو
- **ماذا / what:** Glass panel with mono 'CONTROLS', three labelled sliders; when a setting is spoken, its label goes black and the knob tweens to a new value while the percentage counts; the image's hue/seed changes an
- **كيف / how:** Glass panel with mono 'CONTROLS', three labelled sliders; when a setting is spoken, its label goes black and the knob tweens to a new value while the percentage counts; the image's hue/seed changes and the background wash follows
- **أرقام / params:** knob 500 ms ease-in-out, inactive label 40% grey
- **الدليل / proof:** `style:pm-rossaxbt-3085b7`

#### UI-321 · شريط تقدم وشارة الجزء · Runtime progress bar + segment chip · 👁 شوهد في فيديو
- **ماذا / what:** Thin red bar on the bottom edge width = t/duration; mono chip 'IDEA 0X · NAME' bottom-right updates at each segment
- **أرقام / params:** bar 6 px #e8203a
- **الدليل / proof:** `style:pm-sab8a-364a5a`

#### UI-322 · مفتاح تشغيل كمزحة بصرية · Toggle switch gag · 👁 شوهد في فيديو
- **ماذا / what:** iOS-style toggle animates off->on with label 'FULL BODY MODE ON' while reframing wider to show full body; ruler tick marks on the side
- **أرقام / params:** toggle 250 ms, reframe zoom-out 400 ms
- **الدليل / proof:** `style:pm-sab8a-364a5a`

#### UI-323 · بطاقات واجهة عائمة بعمق · Floating UI card stack with depth · 👁 شوهد في فيديو
- **ماذا / what:** HTML cards with large soft shadows, slight rotateY/rotateX on entry settling to 0, a second card overlapping the first
- **أرقام / params:** shadow 0 30px 60px rgba(30,30,60,.12), 700 ms easeOutQuart
- **الدليل / proof:** `style:pm-sachaarbonel-8f14f4`

#### UI-324 · طلب يُكتب ثم قائمة خطوات تكتمل · Prompt-to-checklist build · 👁 شوهد في فيديو
- **ماذا / what:** type the sentence with a caret, press send, then rows appear each with a green check scale-pop and pill tags
- **أرقام / params:** typing 35 ms/char, row stagger 450 ms, check pop 250 ms
- **الدليل / proof:** `style:pm-sachaarbonel-8f14f4`

#### UI-325 · مؤشرات متعاونين بأسمائهم · Named multiplayer cursors · 👁 شوهد في فيديو
- **ماذا / what:** SVG arrow cursors with coloured name tags moving along bezier paths with ease-in-out and a click squash
- **أرقام / params:** move 600-900 ms, tag colours per user
- **الدليل / proof:** `style:pm-sachaarbonel-8f14f4`

#### UI-326 · هاتف بعداد تقدم · Phone UI progress counter · 👁 شوهد في فيديو
- **ماذا / what:** Rounded phone mockup rotates in 3D; screen shows label 'Render', percent counter ticking and tile grid filling
- **أرقام / params:** counter 0->65% 1 s, tilt 15°
- **الدليل / proof:** `style:pm-sahildesigner23-ee3155`

#### UI-327 · انفراد الهواتف كمروحة · Phone fan-out · 👁 شوهد في فيديو
- **ماذا / what:** Start with one centred phone mockup, then duplicate into 5 phones that translate outwards and rotate ±6/±12 deg, outer ones slightly lower and smaller, all with soft shadow
- **أرقام / params:** 600 ms spring, 40 ms stagger from centre
- **الدليل / proof:** `style:pm-samuel-yostt-891f87`

#### UI-328 · بكرة صور عمودية كالسلوت · Slot-reel portrait scroller · 👁 شوهد في فيديو
- **ماذا / what:** Vertical strip of rounded portrait cards scrolled fast with vertical motion blur then decelerated to land on one card (ease out back)
- **أرقام / params:** 1.0 s, blur 0->30->0 px, overshoot 1.1
- **الدليل / proof:** `style:pm-samuel-yostt-891f87`

#### UI-329 · شريط تقدّم مقسّم للخطوات · Segmented step progress bar · 👁 شوهد في فيديو
- **ماذا / what:** N thin rounded bars across the top with mono uppercase labels; active bar fills left->right with accent colour, completed bars stay filled, active label coloured
- **أرقام / params:** 5 segments, 3 px tall, fill linear over step length
- **الدليل / proof:** `style:pm-sarut0bisasuke-cefa43`

#### UI-330 · ثلاث بطاقات لوحة بيانات · Dashboard card trio · 👁 شوهد في فيديو
- **ماذا / what:** Bar chart card, dark ring-progress card with toggle, line-chart card; slide/stagger in, values animate, cursor clicks toggle
- **أرقام / params:** stagger 100ms; ring fill 800ms
- **الدليل / proof:** `style:pm-shinskinakamoto-20190b`

#### UI-331 · نقرة مؤشر على زر · Cursor CTA click · 👁 شوهد في فيديو
- **ماذا / what:** cursor tweens to button, press scale 0.95, label types in
- **أرقام / params:** 0.6 s
- **الدليل / proof:** `style:pm-slvdev-64c45a`

#### UI-332 · ضغط الرابط إلى حبة · URL compress to pill · 👁 شوهد في فيديو
- **ماذا / what:** type long mono string, then collapse chars and morph container to rounded pill with icon
- **أرقام / params:** ~500 ms
- **الدليل / proof:** `style:pm-steventey-0d20e4`

#### UI-333 · إشعارات متتالية · Toast stack · 👁 شوهد في فيديو
- **ماذا / what:** cards slide from right stagger 300 ms
- **الدليل / proof:** `style:pm-steventey-0d20e4`

#### UI-334 · فاتورة تبنى سطرًا سطرًا · Invoice line build with struck overage · 👁 شوهد في فيديو
- **ماذا / what:** card on blurred pastel backdrop; rows fade-up staggered; one value struck through in red; total uses the odometer roll
- **أرقام / params:** row stagger 120 ms
- **الدليل / proof:** `style:pm-sudeepsd-1a3485`

#### UI-335 · بطاقات واجهة · UI card dashboard pop · 👁 شوهد في فيديو
- **ماذا / what:** coloured rounded cards, toggle, ring %, bars grow
- **الدليل / proof:** `style:pm-sudo-kiran-49176d`

#### UI-336 · مؤشر وهمي يضغط زراً · Fake cursor click · 👁 شوهد في فيديو
- **ماذا / what:** SVG cursor moves on bezier, button scales 0.95 on click
- **أرقام / params:** move 600 ms, press 120 ms
- **الدليل / proof:** `style:pm-sudo-kiran-4f8b59`

#### UI-337 · شبكة ميزات بنتو · Bento feature grid · 👁 شوهد في فيديو
- **ماذا / what:** rounded cards with mini animated UIs, pop in staggered
- **أرقام / params:** stagger 100 ms, radius 20px
- **الدليل / proof:** `style:pm-sudo-kiran-4f8b59`

#### UI-338 · مربع ماسح يتنقل ثم يقفل · Scanner box sweep and lock · 👁 شوهد في فيديو
- **ماذا / what:** outlined orange rectangle with box-shadow glow moves between N cards on each beat (0.5 s at 120 BPM), overshoot past the target then return; on lock fill accent, dim the rest to 30%, flash 100 ms
- **أرقام / params:** glow 0 0 24px #e8501f, step 250-500 ms, power3.inOut
- **الدليل / proof:** `style:pm-tankazunori0914-0fc886`

#### UI-339 · دوّار أغلفة · Cover carousel · 👁 شوهد في فيديو
- **ماذا / what:** 6-8 covers, slight 3D tilt, slide x with stagger 80ms
- **الدليل / proof:** `style:pm-techyoutbe-945b56`

#### UI-340 · ضغطة شراء بالمؤشر · Cursor purchase click · 👁 شوهد في فيديو
- **ماذا / what:** cursor moves to button, press, toast 'added' slides up
- **الدليل / proof:** `style:pm-techyoutbe-945b56`

#### UI-341 · شبكة مزايا متتابعة · Feature grid stagger · 👁 شوهد في فيديو
- **ماذا / what:** 3x2 cards with mini UI previews pop in 100ms stagger
- **الدليل / proof:** `style:pm-thayto-dev-44b911`

#### UI-342 · قائمة اختبارات ناجحة متتابعة · Test suite PASS stagger · 👁 شوهد في فيديو
- **ماذا / what:** rows with green PASS badges stagger 80 ms
- **الدليل / proof:** `style:pm-theviableedge-9065be`

#### UI-343 · واجهة ملصقات بظل مزاح صلب · Sticker UI with hard offset shadow · 👁 شوهد في فيديو
- **ماذا / what:** Cards, pills and buttons with 4-6 px dark outline, radius 24-40 px and a solid same-hue shadow offset 0,6 px (no blur)
- **أرقام / params:** stroke #2a1711; shadow offset y=6
- **الدليل / proof:** `style:pm-thilina-a-891c09`

#### UI-344 · تبديل الثيم كحدث بصري · Theme-toggle reveal · 👁 شوهد في فيديو
- **ماذا / what:** Segmented control; slide pink thumb to 'Dark' with ease-out 300 ms, then cross the whole scene palette from cream to chocolate
- **أرقام / params:** thumb travel 300ms easeOutCubic
- **الدليل / proof:** `style:pm-thilina-a-891c09`

#### UI-345 · ختم يُضرب على التذكرة · Stamp slam on ticket · 👁 شوهد في فيديو
- **ماذا / what:** rotated outlined stamp text scales from 1.6 to 1 with slight overshoot and opacity 0->1, small shake on the ticket
- **أرقام / params:** 150 ms in, overshoot 1.08, rotate -12 deg
- **الدليل / proof:** `style:pm-thismacapital-dfba20`

#### UI-346 · بطاقة مهام متبدلة مع نقاط تقدم · Cycling task card + step dots · 👁 شوهد في فيديو
- **ماذا / what:** single card swaps label/icon each beat with vertical slide, status pill 'in progress' spinner; dots fill one by one with 'n/6' label; final state check icon + blue outline
- **أرقام / params:** ~0.6 s per item, 6 steps
- **الدليل / proof:** `style:pm-thismacapital-dfba20`

#### UI-347 · مؤشر يقوم بالعرض · Scripted cursor UI demo · 👁 شوهد في فيديو
- **ماذا / what:** fake cursor path with click squash and state change on buttons
- **أرقام / params:** click 120 ms
- **الدليل / proof:** `style:pm-twoclipping-221cab`

#### UI-348 · بطاقات أجهزة بعمق · Device parallax cards · 👁 شوهد في فيديو
- **ماذا / what:** phone and browser at different z speeds over a streak gradient
- **الدليل / proof:** `style:pm-twoclipping-221cab`

#### UI-349 · واجهة اختيار مقاس وسعر · Product page price/config UI · 👁 شوهد في فيديو
- **ماذا / what:** swatches + size segmented control + price + CTA progress fill
- **الدليل / proof:** `style:pm-twoclipping-221cab`

#### UI-350 · سلسلة تحول لعنصر واحد · Single-element morph chain · 👁 شوهد في فيديو
- **ماذا / what:** one container whose width, height, border-radius and fill are springs retargeted at each beat; inner content layers per state with own enter/exit
- **أرقام / params:** springs stiffness ~300, damping ratio ~0.8 (tiny overshoot)
- **الدليل / proof:** `style:pm-twoclipping-5cba86`

#### UI-351 · مؤشر فأرة يقود الأحداث · Scripted cursor with real clicks/drags · 👁 شوهد في فيديو
- **ماذا / what:** cursor path as eased keyframes; press = scale 0.9 for 80 ms; while dragging, the control value is derived from cursor x; on release value springs to rest
- **أرقام / params:** cursor 28px macOS arrow
- **الدليل / proof:** `style:pm-twoclipping-5cba86`

#### UI-352 · سحب مطاطي بعد الحد الأقصى · Rubber-band overdrag · 👁 شوهد في فيديو
- **ماذا / what:** when dragged past max, container grows by overflow*0.3 (log-damped), springs back on release
- **أرقام / params:** max stretch ~8%
- **الدليل / proof:** `style:pm-twoclipping-5cba86`

#### UI-353 · لوحة أوامر مع كتابة وتصفية · Command palette typing filter · 👁 شوهد في فيديو
- **ماذا / what:** search field with caret; characters appear per beat subdivision; result rows fade/slide in, first row highlighted; enter collapses into toast
- **أرقام / params:** ~70 ms per char
- **الدليل / proof:** `style:pm-twoclipping-5cba86`

#### UI-354 · عداد توليد · Generation counter · 👁 شوهد في فيديو
- **ماذا / what:** 'generating n / 24' ticking label
- **الدليل / proof:** `style:pm-twoclipping-6dd14e`

#### UI-355 · كتابة في حقل · Typing in input field · 👁 شوهد في فيديو
- **ماذا / what:** caret + chars typed into focused field with accent border
- **الدليل / proof:** `style:pm-twoclipping-6dd14e`

#### UI-356 · كتابة في خانة محادثة · Chat input typewriter · 👁 شوهد في فيديو
- **ماذا / what:** chars 50ms, gradient glowing border
- **الدليل / proof:** `style:pm-ultimaxbt-2ddf1e`

#### UI-357 · مقابض التحويل · Transform gizmo · 👁 شوهد في فيديو
- **ماذا / what:** bounding box with handles + rotation label around shape
- **الدليل / proof:** `style:pm-umangratani-57f86a`

#### UI-358 · سحابة كبسولات كلمات · Floating pill cloud · 👁 شوهد في فيديو
- **ماذا / what:** rounded pills with tag score, scatter depth via scale/opacity
- **أرقام / params:** 30 pills
- **الدليل / proof:** `style:pm-utopyaszx-1b2f94`

#### UI-359 · بطاقة تكتب مع إحصاءات · Typewriter card + live stats · 👁 شوهد في فيديو
- **ماذا / what:** title typewriter 40 ms/char, side counters tick in sync
- **الدليل / proof:** `style:pm-utopyaszx-1b2f94`

#### UI-360 · مشهد طرفية يُكتب فيها أمر · Terminal typewriter scene · 👁 شوهد في فيديو
- **ماذا / what:** macOS window (traffic lights, title), monospace prompt '~ $', characters appended per frame, blinking block cursor
- **أرقام / params:** 35-45 ms/char; cursor blink 500 ms
- **الدليل / proof:** `style:pm-viktoroddy-98c1d8`

#### UI-361 · تمرير معرض داخل نافذة متصفح · Browser mockup gallery scroll · 👁 شوهد في فيديو
- **ماذا / what:** browser chrome with URL pill; inner grid of thumbnails scrolls with smooth easing; occasional cursor
- **أرقام / params:** scroll 600 px over 3 s, ease inOut
- **الدليل / proof:** `style:pm-viktoroddy-98c1d8`

#### UI-362 · تحويل عبارة لبند · Phrase underline to line item · 👁 شوهد في فيديو
- **ماذا / what:** underline colored phrase then add row in side panel
- **الدليل / proof:** `style:pm-visheshbaghell-3aba37`

#### UI-363 · مؤشر وهمي · Fake cursor clicks · 👁 شوهد في فيديو
- **ماذا / what:** cursor tween with click scale 0.9
- **الدليل / proof:** `style:pm-visheshbaghell-3aba37`

#### UI-364 · إطار متصفح · Browser window frame · 👁 شوهد في فيديو
- **ماذا / what:** traffic lights + dark top bar
- **الدليل / proof:** `style:pm-visheshbaghell-3aba37`

#### UI-365 · عرض نافذة متصفح · Browser-window showcase · 👁 شوهد في فيديو
- **ماذا / what:** rounded card with traffic lights + url bar, shadow 0 20px 60px rgba(0,0,0,.12), slide up 20 px fade 500 ms
- **الدليل / proof:** `style:pm-wani-shola-16ca7a`

#### UI-366 · إجابة مساعد متدفقة · Streaming assistant answer · 👁 شوهد في فيديو
- **ماذا / what:** question bubble then bullet lines appear line-by-line ~120 ms
- **الدليل / proof:** `style:pm-wani-shola-16ca7a`

#### UI-367 · أمر محادثة يغيّر المعاينة مباشرة · Chat command changes live preview · 👁 شوهد في فيديو
- **ماذا / what:** Type a command in a chat input (40-60 ms per char), send, then update a value in the preview card with a short flash outline
- **أرقام / params:** caret blink 500 ms; value crossfade 200 ms; accent outline 2 px
- **الدليل / proof:** `style:pm-wozu-co-242285`

#### UI-368 · مؤشر يضغط زر النشر · Cursor click to publish · 👁 شوهد في فيديو
- **ماذا / what:** Cursor eases to button, scales 0.9 on click, button dims, success pill drops in from top
- **أرقام / params:** travel 500 ms, click 120 ms, pill spring
- **الدليل / proof:** `style:pm-wozu-co-242285`

#### UI-369 · دخول واجهة بضبابية حركة · Motion-blurred UI entrance · 👁 شوهد في فيديو
- **ماذا / what:** Translate UI card from below with ease-out and frame-blend or CSS blur proportional to velocity
- **أرقام / params:** ~400 ms, blur 8–20 px
- **الدليل / proof:** `style:pm-xelandre-363f00`

#### UI-370 · بطاقة عدّاد تقييم · Score counter card · 👁 شوهد في فيديو
- **ماذا / what:** Profile card with numeric score ticking up (82→92) and mini bar icon
- **أرقام / params:** ~600 ms easeOut
- **الدليل / proof:** `style:pm-xelandre-363f00`

#### UI-371 · كتابة آلية بمؤشر مع رجوع الكاميرا · Typewriter with caret + camera pull-back · 👁 شوهد في فيديو
- **ماذا / what:** reveal chars by slice(0, floor(t*cps)); blinking caret 2 Hz; parent scale from 2.5->1 with transform-origin at first character, synchronized to typing progress
- **أرقام / params:** ~18 chars/s, caret 3px purple
- **الدليل / proof:** `style:product`

#### UI-372 · إخراج عرض منتج صامت · Silent product demo direction · 📄 موصوف
- **ماذا / what:** The UI, cursor and camera tell the story; words only name a beat or outcome. Start legible on frame one; camera moves to make the action visible then settles; cursor only for decisions with its tip on the target when the pressed state shows; one subject per beat; clear old props.
- **كيف / how:** Capture real UI or build a frame-accurate HTML port from its source when extreme zoom/camera is needed; compute animation from frame number; render stills at first frame, each action, each transition midpoint and last frame before full export; watch muted.
- **الدليل / proof:** `kosif-atlas/skills/101-video-skills/217-silent-product-demo` · `kosif-atlas/skills/101-video-skills/220-ui-tutorial-video` · `kosif-atlas/skills/101-video-skills/217-silent-product-demo/SKILL.md` · `kosif-atlas/skills/101-video-skills/215-feature-video/SKILL.md`

#### UI-373 · كشف المنتج بالفتحة · Aperture product reveal · 📄 موصوف
- **ماذا / what:** Narrow silhouette, mask opens, hold the product before its name; reuse the aperture for the transition to details.
- **كيف / how:** Planar clip mask (MOTION.iris or custom).
- **أرقام / params:** mask opens over 700 ms
- **الدليل / proof:** `kosif-studio/motion/references/motion-director.md` · `100-superskills/skills/kosif-montage-motion/references/motion-director.md`

#### UI-374 · سلالم المسافات والخط والظل · Refactoring-UI spacing, type and shadow scales · 📄 موصوف
- **ماذا / what:** Constrained scales that make mock UIs inside videos look professional: spacing steps, a ~1.2 modular type scale, two-part shadows, measured line lengths.
- **كيف / how:** Use when building faithful or fictional UI mockups as HTML for product-demo scenes.
- **أرقام / params:** spacing 4,8,16,24,32,48,64; type 12,14,16,18,20,24,30,36; hero 36px lh1.1, body 16px lh1.75; measure 45-75ch; shadow-sm 0 1px 2px .05, md 0 4px 6px .1, lg 0 10px 15px .1, xl 0 20px 25px .15
- **الدليل / proof:** `kosif-atlas/skills/3438-ux-design/14122-refactoring-ui`

#### UI-375 · سلّم حالات التحميل حسب مدة الانتظار · Loading-state ladder by wait length · 📄 موصوف
- **ماذا / what:** Choose the loading indicator from expected wait: nothing for very short waits, inline spinner, skeleton, determinate bar, then bar with percent and ETA; skeleton shimmer loops.
- **كيف / how:** Use in UI demo storytelling to show honest progress; shimmer = moving linear-gradient background.
- **أرقام / params:** <0.3s none; 0.3-1s inline spinner; 1-5s skeleton/spinner; 5-30s determinate bar; 30s+ bar + % + ETA; shimmer 1.5s loop; blank 600-800ms reads as broken
- **الدليل / proof:** `kosif-atlas/skills/3438-ux-design/14121-microinteractions/references/feedback-patterns.md` · `kosif-atlas/skills/3438-ux-design/14122-refactoring-ui` · `kosif-atlas/skills/1503-universal-design-principles/3791-expectation-effect-design-cues`

#### UI-376 · تشريح التفاعل الدقيق كوحدة مشهد · Microinteraction anatomy as a beat unit · 📄 موصوف
- **ماذا / what:** Every UI moment = trigger, rules, feedback, loops/modes; for a demo shot record trigger -> visible change -> settled state, and never animate success before the action completes.
- **كيف / how:** Storyboard each UI beat in these three columns; score with an 8-row diagnostic (score = passed/8*10).
- **أرقام / params:** feedback < 100ms for direct manipulation; animations < 500ms and interruptible
- **الدليل / proof:** `kosif-atlas/skills/3438-ux-design/14121-microinteractions` · `kosif-atlas/skills/97-frontend-design-director/206-frontend-design-director/references/motion.md`

#### UI-377 · لحظة احتفال مميزة · Signature celebration moment · 📄 موصوف
- **ماذا / what:** A distinctive branded reaction (like-burst particles, animated checkmark with confetti, witty loading lines) on a frequent visible action; must stay skippable.
- **كيف / how:** SVG/canvas particles (tsparticles MIT) or hand-made burst; place on the 'magic moment' beat of a product film.
- **أرقام / params:** 1-2 per product; removal test: if nobody misses it, it's decoration
- **الدليل / proof:** `kosif-atlas/skills/3438-ux-design/14121-microinteractions/references/signature-moments.md` · `kosif-atlas/skills/3438-ux-design/14121-microinteractions`

#### UI-378 · محاكاة السلوك الفيزيائي المعتدلة · Behavioral mimicry calibration · 📄 موصوف
- **ماذا / what:** UI motion borrows physical intuitions (momentum scroll, rubber-band edges, drawers sliding from the side, modals rising like cards) but with shortened fidelity so frequent actions stay fast.
- **كيف / how:** Choose entry direction by metaphor; use spring settle for momentum; keep timings in the standard ranges.
- **أرقام / params:** 150ms micro, 250-300ms transitions, 400-500ms larger
- **الدليل / proof:** `kosif-atlas/skills/1503-universal-design-principles/3766-mimicry-behavioral` · `kosif-atlas/skills/1369-boss/3175-ui-designer-interaction-specification`

#### UI-379 · مقطع حلقة لمكوّن واجهة · UI component loop clip · 📄 موصوف
- **ماذا / what:** A 3-6 s clip where one component performs one action and loops cleanly, usable in replies or product pages without titles.
- **كيف / how:** Fit whole cycles; for one-off actions return via a plausible reverse; locked camera or one subtle push; compare first vs last frame and watch several repeats.
- **أرقام / params:** 3-6s; one action; seamless loop
- **الدليل / proof:** `kosif-atlas/skills/101-video-skills/219-ui-component-clip`

#### UI-380 · قواعد تصميم حركة المؤشر · Cursor choreography rules for demos · 📄 موصوف
- **ماذا / what:** Pointer appears only when a decision is made; it travels on smooth curves at near-constant speed, lands its tip on the real hit target, holds through the press, and the UI response is visible before moving on.
- **كيف / how:** Plan waypoints per beat, interpolate with Catmull-Rom + arc-length (constant speed), dwell 200-400ms on target before press; verify tip-on-target in stills.
- **أرقام / params:** glide ~450ms per hop; ring 420ms
- **الدليل / proof:** `kosif-atlas/skills/101-video-skills/217-silent-product-demo` · `kosif-atlas/skills/101-video-skills/219-ui-component-clip` · `kosif-atlas/skills/101-video-skills/220-ui-tutorial-video`

#### UI-381 · أنماط البطل لمشاهد الهبوط · Hero archetype variants for landing scenes · 📄 موصوف
- **ماذا / what:** Hero layouts (centered, split, gradient, video background, minimal) and section orders with four style recipes (dark SaaS, clean minimal, bold startup, enterprise) usable as mock 'website' frames inside videos.
- **كيف / how:** Tailwind classes or plain CSS equivalents.
- **أرقام / params:** dark SaaS bg-gray-950 + violet-500; clean minimal white + blue-600 rounded-2xl; bold startup orange-500 rounded-3xl shadow-xl font-black; enterprise slate-50 + slate-900
- **الدليل / proof:** `kosif-atlas/skills/198-product-skills/634-landing-page-generator`

#### UI-382 · حلقة متكررة سلسة لعنصر واجهة · Seamless UI component loop · 📄 موصوف
- **ماذا / what:** A 3-6 s seamless loop featuring one real interface component (button, toggle, waveform, loader) with one action and a clear state change.
- **كيف / how:** Use the component's real size, colors, shadows and timing; fit whole periodic cycles into the duration; for one-shot actions return to the start via a plausible reverse; compare first vs last frame and watch several repeats for jumps or double triggers. Author as HTML/CSS/JS timeline in the kosif scaffold, preview with node tools/render_html.cjs --preview, render frames with Playwright + ffmpeg (both present here).
- **أرقام / params:** 3-6 s; locked camera or one subtle push
- **الدليل / proof:** `kosif-atlas/skills/101-video-skills/219-ui-component-clip/SKILL.md`

#### UI-383 · عناوين أفعال بسيطة في الشروحات · Plain action labels in tutorials · 📄 موصوف
- **ماذا / what:** Tutorial captions name the action in caps ('CHOOSE A FILE', 'PRESS RECORD', 'REVIEW THE RESULT') rather than decorative step numbers; open with the payoff, then explain steps over the action.
- **كيف / how:** One short line per decision; pointer moves to the exact target and holds through the press; keep menus/overlays where the app places them; if zooming makes UI unreadable, re-capture at higher resolution or rebuild the UI as DOM.
- **الدليل / proof:** `kosif-atlas/skills/101-video-skills/220-ui-tutorial-video/SKILL.md`

#### UI-384 · حقيبة أصول من أجزاء حقيقية · Animation kit from real parts · 📄 موصوف
- **ماذا / what:** Before animating, build a kit: rebuild product UI as live DOM with real strings and shoot it at 3-5x into plates, cut isolated transparent parts (each button, chip, node, icon) at >=1600 px, split the official SVG mark into layers that restack pixel-exact (~1/255 max difference), name files with the…
- **كيف / how:** Playwright element screenshots with omitBackground for transparent parts; PIL difference check for the mark layers; watch aspect errors (rendering 1200x800 parts into 224x160 stretches 7%).
- **أرقام / params:** >=1600 px parts; 3-5x capture; diff <=1/255
- **الدليل / proof:** `kosif-atlas/skills/2681-emulo/10272-video/SKILL.md`

#### UI-385 · S05 تقني شبكي · S05 Tech interface · 📄 موصوف
- **ماذا / what:** Grid, hairlines, UI cards, a highlight light; precise alignment, connectors forming, following one datum. Explains relations and steps; never invent UI or features, avoid meaningless HUD decoration.
- **كيف / how:** SVG grid + cards, stroke-dashoffset connectors, monospace labels; render via KOSIF render_html.cjs (/home/user/kosif-tool/tools/render_html.cjs: HTML/SVG + CSS/WAAPI or window.__kosif.seek(t) -> Playwright frame capture -> ffmpeg)
- **أرقام / params:** cost medium; MG-022 MG-025 MG-033 MG-047 MG-055 MG-112
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/styles.md`

#### UI-386 · MG-033 عدسة تكبير التفاصيل · MG-033 Magnifier lens · 📄 موصوف
- **ماذا / what:** A magnified circle glides over the product surface revealing texture with a label.
- **كيف / how:** 0-1 s product, 1-4 s lens pass, 4-6 s detail hold; enlarged copy inside a circular mask whose centre follows the lens path (clip-path:circle + compensating background-position). Don't present invented detail as real photography.
- **أرقام / params:** 6 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-product-ads.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### UI-387 · MG-040 بطاقة سعر تنكشف بالتقشير · MG-040 Peel-off price card · 📄 موصوف
- **ماذا / what:** A small paper corner peels to reveal the confirmed price and terms.
- **كيف / how:** 0-1 s product, 1-2 s peel, 2-5 s price and terms; animated mask + 2.5D fold (CSS rotate3d on a corner with gradient shading) + static text card. No fake countdowns or unconfirmed prices.
- **أرقام / params:** 5 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-product-ads.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### UI-388 · وصفة فيديو عرض ميزة حقيقية في منتج · Real-feature demo video recipe · 📄 موصوف
- **ماذا / what:** For software features write 'the user does X; the product visibly does Y', capture the real app (not mockups) with disposable test data, leave a little time before/after the action, cut waits only where it doesn't misrepresent the experience, keep one visual focus at a time, add words only when the …
- **كيف / how:** Playwright 1.56.1 (installed) for capture/recordVideo, ffmpeg for edit/reframe, overlays via KOSIF render_html.cjs (/home/user/kosif-tool/tools/render_html.cjs: HTML/SVG + CSS/WAAPI or window.__kosif.seek(t) -> Playwright frame capture -> ffmpeg).
- **أرقام / params:** formats 16:9, 4:5, 9:16, 1:1
- **الدليل / proof:** `kosif-atlas/skills/101-video-skills/215-feature-video/SKILL.md`

#### UI-389 · تجهيز تسجيل الشاشة · Screen-recording preparation · 📄 موصوف
- **ماذا / what:** Record screens at native monitor resolution with an enlarged cursor, editor/terminal font of at least 16 pt, notifications off, disposable data, and a little lead-in and lead-out; state while recording what changed on screen.
- **كيف / how:** OBS or Playwright capture; in post ffmpeg crop/zoompan on regions of interest; cursor highlight overlay if needed.
- **أرقام / params:** font >=16 pt
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2447-akbun-vlog-shootplan/SKILL.md` · `kosif-atlas/skills/101-video-skills/215-feature-video/SKILL.md`

#### UI-390 · طبقة زجاجية للواجهات · Glass surface stack (UI) · 📄 موصوف
- **ماذا / what:** Layered frosted panel for overlays on dark scenes.
- **كيف / how:** CSS backdrop-filter blur 28px (40px modals), fill rgba(255,255,255,.05), 1px gradient border .12->.02, shadow 0 24px 80px rgba(0,0,0,.25). Dark backgrounds only.
- **أرقام / params:** blur 28/40px
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### UI-391 · انجذاب مغناطيسي · Magnetic hover displacement · 📄 موصوف
- **ماذا / what:** Elements drift toward cursor by a fraction of offset and spring back; usable as simulated cursor in product videos.
- **كيف / how:** offset=(cursor-center)*0.1; spring back on leave.
- **أرقام / params:** factor 0.1
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### UI-392 · سطح زجاجي · Glass surface stack · 📄 موصوف
- **ماذا / what:** Backdrop blur + 5% white fill + gradient 1px border + large soft ambient shadow, on dark backgrounds only.
- **كيف / how:** CSS backdrop-filter blur(28px) (40px modals); box-shadow 0 24px 80px rgba(0,0,0,.25).
- **أرقام / params:** blur 28/40px
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion`

#### UI-393 · تكوين لوحة البيانات داخل إطار الفيديو · Dashboard composition for a video frame · 📄 موصوف
- **ماذا / what:** When a scene shows a dashboard (real or mock), one question dominates and everything else recedes.
- **كيف / how:** One focal view + subordinate context; 5-7 KPIs max (4-6 on an executive summary); keys next to the evidence; no equal-weight tile walls; animate tiles in 3-30 order (headline first). For operations scenes show stale/live states explicitly.
- **أرقام / params:** 5-7 KPIs; headline first
- **الدليل / proof:** `kosif-atlas/skills/3455-business-analytics/14162-kpi-dashboard-design/SKILL.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10335-visualization-strategy-and-critique/SKILL.md` · `kosif-atlas/skills/2690-build-web-data-visualization/10321-dashboards-and-real-time-visualization/references/monitoring-vs-analysis.md`

#### UI-394 · إشارة فيض التبويبات بالعربية · RTL tab overflow hint · 📄 موصوف
- **ماذا / what:** On narrow screens a 44px gradient on the inline-start edge (left in RTL) signals hidden tabs, with proximity scroll-snap; wide screens wrap tabs to two rows.
- **كيف / how:** nav.tabs::after gradient to left; .tabs-inner scroll-snap-type x proximity; min-width 900px -> flex-wrap.
- **أرقام / params:** fade 44px rgba(255,255,255,.92); scroll-padding 12px
- **الدليل / proof:** `kosif-audit-pro/patch/kosif-v17.css`

#### UI-395 · نماذج المنتج على الأجهزة · Product mockups (laptop dashboard, iPhone x4, audit execution) · 📄 موصوف
- **ماذا / what:** Approved marketing-style device composites: an iMac-style dashboard with KPI rings, grouped bars, 3x3 heatmap and navy rail; four iPhones on a stone plinth showing notifications, home, PBC requests and risks; an audit-execution laptop screen.
- **كيف / how:** WebP 1448x1086 each; use as style reference for device-frame product demos.
- **أرقام / params:** navy rail, white cards, blue/green bars, Arabic RTL UI
- **الدليل / proof:** `kosif-earth-ci-fork/docs/design/mockups/kosif-laptop-dashboard.webp` · `kosif-earth-ci-fork/docs/design/mockups/kosif-iphone.webp` · `kosif-earth-ci-fork/docs/design/mockups/kosif-laptop-audit-execution.webp`

#### UI-396 · شارة الجسم والتوقيت في المونتاج · Post-production body badge + timestamp · 📄 موصوف
- **ماذا / what:** A small labelled body-icon badge, target region and timestamp are added in the editor afterwards because AI video cannot draw them reliably.
- **كيف / how:** Documented instruction; not implemented as code.
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/fitness.mjs:35` · `fastify-motion-bro/skills/fitness/SKILL.md:14`

#### UI-397 · اتجاه إطلاق المنتج · Product-launch (brag) direction · 📄 موصوف
- **ماذا / what:** Product-launch teaser style inspired by latent-spaces/brag (MIT) with musical pacing; only a brief example and style id exist.
- **كيف / how:** Set style 'brag' and design launch scenes by hand.
- **الدليل / proof:** `fastify-motion-bro/examples/launch-16x9.json` · `fastify-motion-bro/docs/SOURCE_AUDIT.md:4` · `fastify-motion-bro/docs/ENGINE_ROUTER.md:7`

#### UI-398 · أنماط صفحات الهبوط ووصفات التخطيط · Landing page section patterns + layout recipes · 📄 موصوف
- **ماذا / what:** Reusable page structure and CSS recipes (also useful for product-demo animations of websites).
- **كيف / how:** Hero (<= 10-word outcome headline, one CTA, product in use) -> social proof -> 3-6 benefits -> 3 steps -> offer -> FAQ -> final CTA; container max-width 72rem padding 16/24 px; auto-fit grid minmax(16rem,1fr); app shell nav -> bottom bar <= 900 px; H1 clamp(28px,5vw,44px).
- **أرقام / params:** breakpoints 360/768/1024/1280; text measure ~68ch; touch >= 44 px
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-web-design/references/web-playbook.md` · `kosif-one/tools/kosif-omni/skills/kosif-web-design/SKILL.md`

#### UI-399 · ميزانية الأداء · Web performance budget · 📄 موصوف
- **ماذا / what:** Mobile targets for any HTML deliverable.
- **كيف / how:** AVIF/WebP + srcset, subset fonts with font-display swap + preload, defer scripts.
- **أرقام / params:** LCP <= 2.5 s, CLS <= 0.1, INP <= 200 ms, JS <= 170 KB gz first load
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-web-design/references/web-playbook.md`

#### UI-400 · واجهات زجاجية · Glassmorphism UI motion · 📄 موصوف
- **ماذا / what:** Frosted cards over deep gradient, cards rise and unblur with stagger, breathing glow.
- **كيف / how:** Copy style sheet section into DESIGN.md, then build via claude-animation-studio render(t).
- **أرقام / params:** gradient #0B1B3A->#1E3A8A; card rgba(255,255,255,.08) border .18 blur 26px radius 28px; accent #7DD3FC; y 40->0 blur 12->0 stagger 80 ms; IBM Plex Sans Arabic 600/Manrope 700; max 3 cards
- **الدليل / proof:** `100-superskills/skills/trend-animation-styles/references/styles.md`

#### UI-401 · حركات الواجهة الدقيقة · UI micro-interaction rules · 📄 موصوف
- **ماذا / what:** Every motion has function (guide/feedback/delight); springs; transform+opacity only; reduced-motion fallback; <=700 ms; 60 fps.
- **كيف / how:** Emit motion-tokens.json.
- **أرقام / params:** spring 300/30/1; stagger <500 ms; <=700 ms; <=3 flashes/s
- **الدليل / proof:** `100-superskills/skills/ui-motion-microinteractions/SKILL.md`

#### UI-402 · واجهة محاكاة سريعة · Simulated UI driven at speed · 📄 موصوف
- **ماذا / what:** Rebuild UI in DOM, cursor as momentum body, asymmetric click (fast down, short hold, slower up, pre-swell), one impact function drives shake/camera/blur; state changes caused by impacts.
- **الدليل / proof:** `100-superskills/skills/motion-director-pro/references/motion-floor.md`

#### UI-403 · تطبيقات واجهة حديثة بـ React/Next.js أو  · React Frontend App · 📄 موصوف
- **ماذا / what:** Owner-built skill "React Frontend App" (own words): workflow guidance for react frontend app; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill frontend-react-app (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/frontend-react-app/SKILL.md`

#### UI-404 · صفحة هبوط من ملف HTML واحد بمستوى الجوائ · Premium Landing Page · 📄 موصوف
- **ماذا / what:** Single-file HTML with inline CSS/JS, Google Fonts + GSAP from CDN, CSS colour variables, prefers-reduced-motion respected, 375px no horizontal scroll; mandatory 4-question brief (product/promise, audience, identity, tone). Reusable as a scroll-animated product page or a screen-recorded promo.
- **كيف / how:** Load skill landing-page-premium (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/landing-page-premium/SKILL.md`

#### UI-405 · تطبيقات جوال بـ Flutter أو React Native/ · Mobile App Builder · 📄 موصوف
- **ماذا / what:** Owner-built skill "Mobile App Builder" (own words): workflow guidance for mobile app builder; helps a video job only as supporting planning/production knowledge.
- **كيف / how:** Load skill mobile-app-builder (SKILL.md + references/sources.md) and follow its numbered steps; instruction-only, no scripts.
- **الدليل / proof:** `100-superskills/skills/mobile-app-builder/SKILL.md`

#### UI-406 · من الكود إلى الواجهة · Code-to-UI split · 📄 موصوف
- **ماذا / what:** Editor splits; right half renders the described component, morphing as lines highlight.
- **الدليل / proof:** `kosif-tool/playbooks/code.md:45`

#### UI-407 · ثوابت جهاز الهاتف · Phone device constants · 📄 موصوف
- **ماذا / what:** One parametric phone: screen size, concentric radii, bezel, island or notch.
- **أرقام / params:** screen 390×844 (19.5:9); screen radius 12–14% of width; bezel 2–3%; frame radius = screen radius + bezel; island 120×36 at 12 px; notch 210×34 r 20; Remotion sample R 52 BEZEL 12 frame #15171c
- **الدليل / proof:** `kosif-tool/playbooks/phone.md:17` · `kosif-tool/playbooks/phone.md:110`

#### UI-408 · واجهة حية داخل الشاشة · Live UI in screen at 2× · 📄 موصوف
- **ماذا / what:** Screen is clipped live DOM/SVG/Canvas at 2× density; island/home indicator painted after UI; message text outside device.
- **أرقام / params:** in-screen text ≥ 30 px; callouts ≥ 36 px
- **الدليل / proof:** `kosif-tool/playbooks/phone.md:19`

#### UI-409 · حدود منظور الجهاز · Device perspective limits · 📄 موصوف
- **ماذا / what:** Perspective distance and yaw/pitch caps; rest pose never at 0°.
- **أرقام / params:** perspective 1200–1600 px (~1.3× width); yaw ±28°; pitch ±8°; rest yaw −6° to −10°
- **الدليل / proof:** `kosif-tool/playbooks/phone.md:21`

#### UI-410 · دخول الهاتف · Phone entrance · 📄 موصوف
- **ماذا / what:** Rise while yaw settles off-axis.
- **كيف / how:** Remotion spring {damping 18, stiffness 90, mass 1.1}; or cubic-bezier(0.16,1,0.3,1).
- **أرقام / params:** 700–900 ms; rise 120–160 px; yaw −22°→−8°; opacity by 250 ms
- **الدليل / proof:** `kosif-tool/playbooks/phone.md:33` · `kosif-tool/playbooks/phone.md:115-117`

#### UI-411 · سرعة الدوران والتحويم · Device rotation speed and idle hover · 📄 موصوف
- **ماذا / what:** Rotation speed caps, small settle overshoot, slow subtle hover.
- **كيف / how:** 6·sin(2πt/3.2)
- **أرقام / params:** ≤ 40°/s reveal; ≤ 4°/s idle; overshoot 1–2°; hover ≤ 6 px period ≥ 3.2 s
- **الدليل / proof:** `kosif-tool/playbooks/phone.md:34-35`

#### UI-412 · نقرة الهاتف مع موجة · Phone tap with ripple · 📄 موصوف
- **ماذا / what:** Visible cue, press scale, spring release, ripple ring.
- **أرقام / params:** cue −60 ms; press 90 ms cubic-bezier(0.4,0,1,1) device 0.96 button 0.92; release spring {stiffness 240, damping 14}; ripple 0→64 px, 0.6→0 over 300 ms
- **الدليل / proof:** `kosif-tool/playbooks/phone.md:36` · `kosif-tool/playbooks/phone.md:59-68`

#### UI-413 · تمرير بطاقة لكل نبضة · Card-per-beat scroll · 📄 موصوف
- **ماذا / what:** Scroll in card steps with holds; device counter-rotates.
- **أرقام / params:** 450 ms move ≈ 62% screen height; hold ≥ 600 ms; never linear > 2 s; counter-rotate 2°; ≤ 5 cards
- **الدليل / proof:** `kosif-tool/playbooks/phone.md:38` · `kosif-tool/playbooks/phone.md:72-77`

#### UI-414 · خطوط الشرح القائدة · Callout leader lines · 📄 موصوف
- **ماذا / what:** Callouts outside device follow their element; leader lines draw.
- **أرقام / params:** rows 60–90 ms stagger; callout +120 ms; leader 260 ms cubic-bezier(0.16,1,0.3,1)
- **الدليل / proof:** `kosif-tool/playbooks/phone.md:39`

#### UI-415 · إشعار الجزيرة الديناميكية · Dynamic island notification · 📄 موصوف
- **ماذا / what:** Island expands, content staggers, holds, collapses.
- **أرقام / params:** 120×36→300×80 spring {stiffness 180, damping 16} ≈ 260 ms; content from 180 ms 60 ms stagger; hold to 2400; collapse 300 ms
- **الدليل / proof:** `kosif-tool/playbooks/phone.md:41` · `kosif-tool/playbooks/phone.md:89-96`

#### UI-416 · وصفة كشف الجهاز · Hero device reveal recipe · 📄 موصوف
- **ماذا / what:** Device rises, reflection pass, UI staggers in, headline words, push hold.
- **أرقام / params:** 0–900 rise 140 px; 350–1550 reflection; 600–1300 UI rows 70 ms; 1200–1800 headline spring 14/120; 900–4000 push 1.04 yaw drift ±1.5°
- **الدليل / proof:** `kosif-tool/playbooks/phone.md:49-57`

#### UI-417 · تسليم بين جهازين · Two-device turntable handoff · 📄 موصوف
- **ماذا / what:** Device A turns away and slides, B enters, shared element flies between on arc.
- **أرقام / params:** A yaw −8°→+28° slide 220 px; B +30°→+8° scale 0.9→1 over 1400 ms cubic-bezier(0.65,0,0.35,1); specular 500–700; shared element 700–1000; settle 1.5° overshoot spring 16/100
- **الدليل / proof:** `kosif-tool/playbooks/phone.md:79-87`

#### UI-418 · عكس واجهة الهاتف للعربية · RTL in-device UI mirroring · 📄 موصوف
- **ماذا / what:** Mirror interactions not hardware: back chevron right, new screen from left, tabs RTL, toggle on-left; island/buttons not mirrored; hero copy right of device with positive yaw.
- **كيف / how:** dir=rtl, logical CSS (marginInlineStart, insetInlineEnd); unicode-bidi:plaintext for phone numbers/times.
- **أرقام / params:** Arabic line height +10% in compact rows
- **الدليل / proof:** `kosif-tool/playbooks/phone.md:187-192`

#### UI-419 · إعادة بناء الشاشة كطبقات · Layered screen rebuild · 📄 موصوف
- **ماذا / what:** Screen as background→chrome→content→controls→overlays→pointer→callouts, each with own timeline; flattened PNG only as reference.
- **الدليل / proof:** `kosif-tool/playbooks/product-ui.md:17`

#### UI-420 · رموز تصميم الواجهة · UI design tokens · 📄 موصوف
- **ماذا / what:** Grid, radii, type sizes and four elevation tiers written in STYLE.md.
- **أرقام / params:** 8 px grid; radii 8/16/24; 1 headline + 2 UI sizes; shadows 0 2px 8px rgba(0,0,0,.12) → 0 24px 64px rgba(0,0,0,.35)
- **الدليل / proof:** `kosif-tool/playbooks/product-ui.md:18`

#### UI-421 · محتوى واجهة حقيقي · Real UI content rule · 📄 موصوف
- **ماذا / what:** Plausible locale-correct names, amounts, dates; no lorem, no inconsistent KPIs.
- **الدليل / proof:** `kosif-tool/playbooks/product-ui.md:19`

#### UI-422 · تصميم المؤشر حسب الإطار · Pointer design by framing · 📄 موصوف
- **ماذا / what:** Arrow for device-free, translucent tap circle in phones (never arrow on phone).
- **كيف / how:** SVG cursor path M4 2 L20 15 L12 16 L16 25 L12 26.5 L8 17.5 L4 21 Z.
- **أرقام / params:** arrow 22–26 px 1.5 px outline; tap circle 40–48 px at 25–35%
- **الدليل / proof:** `kosif-tool/playbooks/product-ui.md:20` · `kosif-tool/playbooks/product-ui.md:152`

#### UI-423 · عمق بلا حيل · Depth without gimmicks · 📄 موصوف
- **ماذا / what:** Depth from elevation, overlap and small chrome/content parallax, not 3D tilt/glass/glow.
- **أرقام / params:** parallax 2–4%
- **الدليل / proof:** `kosif-tool/playbooks/product-ui.md:23`

#### UI-424 · ثلاثية النية والفعل والاستجابة · Intent→action→response triad · 📄 موصوف
- **ماذا / what:** Pointer arrives, presses, UI responds after realistic latency.
- **أرقام / params:** latency 60–120 ms; 0 ms = slideshow; > 200 ms = bug
- **الدليل / proof:** `kosif-tool/playbooks/product-ui.md:29` · `kosif-tool/playbooks/product-ui.md:58`

#### UI-425 · وصفة الوصول والنظرة الأولى · Arrival and first look recipe · 📄 موصوف
- **ماذا / what:** Screen rises, shadow tier grows, chrome paints, cards stagger, push, caret dwell.
- **أرقام / params:** 0–520 rise; chrome 400–900 60 ms stagger; 6 cards 700–1300 50 ms; push 1.05 over 4 s
- **الدليل / proof:** `kosif-tool/playbooks/product-ui.md:66-75`

#### UI-426 · جولة تمرير مع شروحات · Scroll tour with callouts · 📄 موصوف
- **ماذا / what:** Callout draws, dwell, content scrolls while chrome stays with bg parallax, next callout.
- **أرقام / params:** scroll −720 px 800 ms cubic-bezier(0.45,0,0.15,1); bg parallax −24 px
- **الدليل / proof:** `kosif-tool/playbooks/product-ui.md:91-102`

#### UI-427 · تعبئة نموذج وتحقق ونجاح · Form fill → validation → success · 📄 موصوف
- **ماذا / what:** Focus ring, typing, tick, focus jump, submit, spinner, toast.
- **أرقام / params:** type 16 chars at 70 ms ±20; tick 240 ms; focus jump spring 170/20; spinner crossfade 120; toast spring 200/22 hold ~2 s
- **الدليل / proof:** `kosif-tool/playbooks/product-ui.md:104-116`

#### UI-428 · عكس واجهة المنتج للعربية · RTL product UI mirroring · 📄 موصوف
- **ماذا / what:** Sidebar right, primary action left, chevrons flipped, progress RTL, cursor starts bottom-right, forward nav from left, toasts top-left; cut typing at graphemes with Intl.Segmenter.
- **أرقام / params:** UI labels ≥ 28 px; lh 1.6–1.8; letter-spacing 0
- **الدليل / proof:** `kosif-tool/playbooks/product-ui.md:209-214`

#### UI-429 · قائمة عائمة وتحول الهامبرغر · Fluid island nav + hamburger morph · 📄 موصوف
- **ماذا / what:** Floating glass pill nav; lines rotate to X; fullscreen backdrop-blur-3xl overlay; links stagger up 100/150/200 ms.
- **كيف / how:** Tailwind classes.
- **الدليل / proof:** `kosif-one/vendor/ai-design-skills/skills/landing-page-design/SKILL.md`

#### UI-430 · قلب الهاتف · Phone flip with mid-swap · 💡 فكرة
- **ماذا / what:** Phone mockup flips 180° and swaps screen at 90°.
- **كيف / how:** CSS 3D rotateY; content swap at midpoint.
- **أرقام / params:** 700 ms; tilt ≤±8° Y
- **الدليل / proof:** `style:pm-cansincengiz-me-cf68dd`

#### UI-431 · تحميل هيكلي · Skeleton-to-content load · 💡 فكرة
- **ماذا / what:** Grey skeleton blocks fill into real UI.
- **كيف / how:** Crossfade per block.
- **أرقام / params:** 400 ms
- **الدليل / proof:** `style:pm-cansincengiz-me-cf68dd`

#### UI-432 · تمرير ثم تنويه · Scroll then callout · 💡 فكرة
- **ماذا / what:** In-screen scroll then callouts appear only after scroll ends.
- **كيف / how:** translateY.
- **أرقام / params:** 240 px over 600 ms ease-in-out; callout +150 ms
- **الدليل / proof:** `style:pm-cansincengiz-me-cf68dd`

#### UI-433 · تحول المتصفح لهاتف · Browser-to-phone morph · 💡 فكرة
- **ماذا / what:** Single tween of width/height/radius; content reflows not scales.
- **كيف / how:** CSS box tween ease-in-out.
- **أرقام / params:** 600 ms
- **الدليل / proof:** `style:pm-deifosv-04e4d3`

#### UI-434 · عرض التصدير · Export flow demo · 💡 فكرة
- **ماذا / what:** Tap ripple, progress bar, share sheet slide-up, device Y rotation.
- **كيف / how:** CSS.
- **أرقام / params:** bar 1600 ms; rotateY 12°
- **الدليل / proof:** `style:pm-gautam-mer1-2ae354`

#### UI-435 · صعود الهاتف · Phone rise spring + squash land · 💡 فكرة
- **ماذا / what:** Phone rises with overshoot; thumbnail lands with small squash.
- **كيف / how:** spring.
- **أرقام / params:** overshoot 1.08, 700 ms; 2 px squash
- **الدليل / proof:** `style:pm-l3d1c-0e35a3`

#### UI-436 · حلقة تقدم · Progress ring with Arabic labels · 💡 فكرة
- **ماذا / what:** Ring sweeps while Arabic status labels crossfade.
- **كيف / how:** SVG dashoffset.
- **أرقام / params:** 1200 ms; labels 150 ms; expand 400 ms easeOutQuint
- **الدليل / proof:** `style:pm-l3d1c-0e35a3`

#### UI-437 · لوحات من الحواف · Edge-staggered UI panels · 💡 فكرة
- **ماذا / what:** Panels slide from their own edges with stagger.
- **كيف / how:** cubic-bezier(0.25,1,0.5,1).
- **أرقام / params:** 600 ms; 60 ms stagger
- **الدليل / proof:** `style:pm-listudio-820c7b`

#### UI-438 · إعادة ترتيب FLIP · FLIP list reorder · 💡 فكرة
- **ماذا / what:** Cards reorder by sliding with FLIP transforms.
- **كيف / how:** FLIP.
- **أرقام / params:** 450 ms cubic-bezier(0.2,0.8,0.2,1); stagger 40-60 ms; 45 ms cascade
- **الدليل / proof:** `style:pm-melvynx-6cde6c`

#### UI-439 · مؤشر حقيقي · Real cursor on bezier paths · 💡 فكرة
- **ماذا / what:** Pointer moves on bezier paths; click is scale dip.
- **أرقام / params:** 250-400 ms; click 90 ms to 0.94
- **الدليل / proof:** `style:pm-melvynx-6cde6c`

#### UI-440 · لقطات واجهة سريعة · Snap-settle UI shots · 💡 فكرة
- **ماذا / what:** Short shots, elements back-out in, linear slide out.
- **أرقام / params:** avg shot 2.5 s, max 4 s; in 360 ms cubic-bezier(0.34,1.56,0.64,1); out 180 ms linear
- **الدليل / proof:** `style:pm-ratheejaisal-1f4538`

#### UI-441 · قلب بطاقات متتابع · Card-grid flip cascade · 💡 فكرة
- **ماذا / what:** 12-card rotateY cascade left to right.
- **أرقام / params:** rotateY 180° 350 ms; 90 ms cascade
- **الدليل / proof:** `style:pm-robvjourney-ce3e1a`

#### UI-442 · دخول وميل الزجاجة · Bottle enter-tilt-exit · 💡 فكرة
- **ماذا / what:** easeOutBack overshoot 1.15 600 ms; tilt 35° easeInOutSine
- **أرقام / params:** labels slide 24 px easeOutQuint 450 ms, dim to 40%
- **الدليل / proof:** `style:pm-sarut0bisasuke-cefa43`

#### UI-443 · ضغط الرابط · URL squeeze compression · 💡 فكرة
- **ماذا / what:** Long URL squeezes into short link.
- **أرقام / params:** cubic-bezier(0.7,0,0.2,1) 500 ms; springs 200/24
- **الدليل / proof:** `style:pm-steventey-0d20e4`

#### UI-444 · دفع داخل الواجهة · Cursor-led UI push-ins · 💡 فكرة
- **ماذا / what:** push cubic-bezier(0.22,1,0.36,1) 900 ms, max 1.6x, 300 ms hold; cursor 24 px quad bezier 350-450 ms, click squash 0.9 90 ms
- **الدليل / proof:** `style:pm-techyoutbe-945b56`

#### UI-445 · سطور تعيد ترتيبها · Self-reordering document lines · 💡 فكرة
- **ماذا / what:** spring 160/20; 50 ms offset; highlight wipe 180 ms, colour switch at 50%
- **الدليل / proof:** `style:pm-thayto-dev-44b911`

#### UI-446 · بطاقة السعر · Pricing card reveal · 💡 فكرة
- **ماذا / what:** scale 0.92->1 300 ms; rows 16 px 80 ms stagger; price last
- **الدليل / proof:** `style:pm-thayto-dev-44b911`
