# الهوية والشعار — Brand & logo

> فصل مُجمَّع آليًا من 218 ملاحظة حصاد (مستودعات KOSIF + أطلس المهارات + 253 فيديو مرجعي)، مدموجة إلى **216 قدرة** مرتبة من الأقوى دليلًا. لم يُحرَّر يدويًا بعد — تحقّق من الدليل قبل الادعاء.
> Auto-compiled chapter: 216 powers deduplicated by name from 218 harvested atoms; strongest evidence first.

**الحالة:** ✅ مُثبت هنا 11 · 🟢 جاهز 27 · 📦 بأمر تثبيت 44 · 🔑 مفتاح/خدمة 7 · 👁 شوهد في فيديو 89 · 📄 موصوف 33 · 💡 فكرة 5

#### BRAND-01 · بناء شعار SQC · SQC mark construction (S + crystal Q with audit tick + C) · ✅ مُثبت هنا
- **ماذا / what:** Geometric monogram: S as a rounded stroke path, Q as a hexagonal cut crystal with inner facet lines whose tail is an audit check-mark, C as an open arc, and a 45-degree diamond dot.
- **كيف / how:** SVG viewBox 300x110: S path stroke 19; hex polygon 150,16 183,35 183,73 150,92 117,73 117,35 with facet fill + stroke 15; facets stroke 5 opacity .55; tick M164 80 l13 13 28-33 stroke 17; C arc stroke 19; rect 12x12 rotate(45). Ledger gradients #f6c39b -> #f2732d -> #a53e07; letters white->#f1e3d3 (on dark) or #3a2f27->#1d1814 (on light).
- **أرقام / params:** logo 800x110 with SMART QUALITY CONTROL Montserrat 800 32px textLength 455
- **الدليل / proof:** `kosif-earth-ci-fork/ui/art/sqc-mark.svg` · `kosif-earth-ci-fork/ui/art/sqc-mark-dark.svg` · `kosif-earth-ci-fork/ui/art/sqc-logo.svg`

#### BRAND-02 · شعار سحابة KOSIF · KOSIF cloud mark · ✅ مُثبت هنا
- **ماذا / what:** Outline cloud glyph with a small doorway at its base, stroked with a peach-to-saffron gradient.
- **كيف / how:** SVG viewBox 96x64, stroke 6.5 round joins; icon version on gradient #d9530e -> #110e0b at scale 3.2.
- **أرقام / params:** gradient #f2a36b -> #d9530e
- **الدليل / proof:** `kosif-earth-ci-fork/ui/art/kosif-cloud.svg` · `kosif-earth-ci-fork/ui/art/kosif-icon.svg`

#### BRAND-03 · مكتبة البطاقات الختامية · Kinetic end-card library (17) · ✅ مُثبت هنا
- **ماذا / what:** Per-theme brand outros, e.g. letters assemble from charcoal swirl, cyan outline draws then fills, single gold glint, white wordmark on red, chrome blob uncovers wordmark; added only to the last clip and only for a user-owned wordmark.
- **كيف / how:** theme.endcard appended when i==n-1 and brand set.
- **أرقام / params:** 17 end cards
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/kinetic-flow.mjs:4-20,115`

#### BRAND-04 · خانة شعار المستخدم · User-owned wordmark slot · ✅ مُثبت هنا
- **ماذا / what:** Only a user-owned wordmark may appear (top-centre strip, end card on the final clip); no fake logos, no AI-added logos or labels.
- **كيف / how:** kinetic brand field; prompts contain 'no logos/watermarks'.
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/kinetic-flow.mjs:101,115` · `fastify-motion-bro/scripts/profiles/car-exploded.mjs:56` · `fastify-motion-bro/skills/kinetic-flow/SKILL.md:13`

#### BRAND-05 · قوالب الموشن الثمانية · Motion templates (8) · ✅ مُثبت هنا
- **ماذا / what:** title-card, lower-third, stat-counter, quote-card, logo-reveal, countdown, end-card, bullet-list — Arabic-first, Cairo embedded.
- **كيف / how:** python scripts/kmotion.py template list; template new NAME --template title-card --set title=… sub=… accent=#E7B65A
- **أرقام / params:** accent #E7B65A
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md`

#### BRAND-06 · قالب كشف الشعار · Template: logo-reveal · ✅ مُثبت هنا
- **ماذا / what:** Pen draws the logo outline, fill springs in with flash and sparkles, name and tagline reveal, slow push.
- **كيف / how:** python scripts/mtemplates.py new NAME --template logo-reveal --set key=value ... [--seconds S --size WxH --fps F] -> projects/NAME/index.html (+ fonts, gsap, motion-kit); preview in a browser; render with motion.py render.
- **أرقام / params:** 6 s; name 'KOSIF', tagline, accent #E7B65A, bg1 #0f1a2b, bg2 #06101c; path = SVG path in a 120x136 viewBox (default hexagon-in-hexagon); draw 1.25 s; fill at 1.5 s
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/templates/motion/logo-reveal.html` · `100-superskills/skills/kosif-montage-motion/scripts/mtemplates.py:48`

#### BRAND-07 · تحويل ألوان CSS بما فيها oklch · CSS colour normaliser incl. oklch · ✅ مُثبت هنا
- **ماذا / what:** Brand colours scraped from a site's CSS in any syntax (#abc, rgb with slash alpha, hsl, oklch) normalise to hex for the film palette.
- **كيف / how:** launch.to_hex('#abc')→#aabbcc; 'rgb(255 0 0 / 50%)'→#ff0000; 'hsl(120,100%,50%)'→#00ff00; 'oklch(100% 0 0)'→#ffffff; 'oklch(0.5 0 0)'→#636363; invalid → None; launch.init(site) writes material.json {palette, fonts, ctas, lang}.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_launch.py:22` · `100-superskills/skills/kosif-montage-motion/tests/test_launch.py:30`

#### BRAND-08 · استخراج مواد فيديو إطلاق من موقع · Site-to-launch-video material extraction · ✅ مُثبت هنا
- **ماذا / what:** From a website folder, title, description, fonts (Google Fonts link), CSS custom-property palette and CTAs are extracted and a launch plan is written with the right aspect and a one-sentence pitch question.
- **كيف / how:** launch.init(site_dir, 'polished', 'vertical', 18, out) → material.json {palette, fonts, ctas, lang}, brag-plan.md (1080×1920, 'ما هو، في جملة واحدة؟').
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_launch.py:30`

#### BRAND-09 · نظام تصميم ورق الدفتر · 'Ledger paper' design system palette · ✅ مُثبت هنا
- **ماذا / what:** Cream canvas, thin dark ink borders, whisper shadows, outline pill buttons and one saffron accent, with light and dark tokens.
- **كيف / how:** CSS tokens in src/kosif.css per docs/04-design-system.md.
- **أرقام / params:** paper #fbf8f3/#161310; paper-2 #f3ece2/#1f1b17; card #fffdf9/#1c1814; ink #1d1814/#f5ede3; ink-2 #4b4139; ink-3 #7b6f64; rule-soft #e0d5c8; accent #d9530e/#f2732d; good #2c7a4b; warn #a76a10; bad #b3261e; info #2f5f8f
- **الدليل / proof:** `kosif-one/tools/kosif-web/docs/04-design-system.md`

#### BRAND-10 · مشهد الشعار المتتبَّع بأسلوب رسام اللافتات · Traced picture as a sign-painter scene · ✅ مُثبت هنا
- **ماذا / what:** A traced image becomes a picture program: radial dark backdrop, soft drop shadow of the silhouette, then one step per colour layer, largest first, each growing from its own centroid.
- **كيف / how:** vector_scene.build(data) fits the art into 1080x730 on the 1200x800 sheet.
- **أرقام / params:** backdrop radial #3d3648 -> #221e2a -> #121016 (r 760); shadow offset 12, alpha .45, blur 18; layer weight 1.0
- **الدليل / proof:** `kosif-studio/vector_scene.py:8` · `kosif-studio/tests/test_studio.py:988`

#### BRAND-11 · بطاقة شعار ختامية برسم المسار · Logo card with path draw-on (canvas starter) · ✅ مُثبت هنا
- **ماذا / what:** Closing card springs up 120 px and scales 0.94->1, then a K-like monogram path inside a rounded square draws on with dashoffset.
- **كيف / how:** card spring 160/17 over 0.1-0.7 s; logoPath dashoffset prog(local,0.4,1.2,inOutCubic)
- **أرقام / params:** card radius 48, gradient 170deg #1a2744->#111a30, shadow 0 40 120 rgba(0,0,0,.5); logo 220 px, rect rx16 #7ee8d2, stroke #062a24 7
- **الدليل / proof:** `kosif-tool/starters/html-canvas/index.html:34` · `kosif-tool/starters/html-canvas/index.html:177`

#### BRAND-12 · تغليف الشعار النقطي في SVG · Raster logo embedded as SVG · 🟢 جاهز
- **ماذا / what:** Pixel-identical SVG wrapper with base64 image when no vector source exists; not real vectorization.
- **كيف / how:** viewBox = pixel size from identify; <image href='data:image/png;base64,..'>. Use Potrace only for monochrome marks.
- **الدليل / proof:** `kosif-atlas/skills/2981-designer-skill/12626-raster-logo-svg`

#### BRAND-13 · شعار كاشف برو المصغر · KOSIF Pro favicon mark · 🟢 جاهز
- **ماذا / what:** 32px aubergine rounded square with a stroked white K and a teal dot.
- **كيف / how:** Inline SVG: rect rx 8 fill #2F1B68; path M9 7V25 M9 16L21 7 M9 16L22 25 stroke #FFFFFF width 3 round caps/joins; circle cx24 cy8 r3 #2EA6A6.
- **أرقام / params:** 32x32; stroke 3; teal dot r3
- **الدليل / proof:** `kosif-audit-pro/public/favicon.svg`

#### BRAND-14 · أيقونة تطبيق كاشف بتدرج وعلامة صح · KOSIF Studio app icon (gradient K + check) · 🟢 جاهز
- **ماذا / what:** 512px app icon: diagonal indigo-violet-pink gradient tile, solid white K polygon, emerald check badge; maskable full-bleed variant.
- **كيف / how:** SVG linearGradient x1 0 y1 0 x2 1 y2 1 stops #6366f1 0, #8b5cf6 .56, #ec4899 1; rect rx 112; check circle r54 #10b981 with 18px white stroke.
- **أرقام / params:** 512x512; rx 112 (maskable 0); badge r 54 / 47
- **الدليل / proof:** `kosif-audit-studio/icon.svg` · `kosif-audit-studio/icon-maskable.svg` · `kosif-audit-studio/manifest.webmanifest`

#### BRAND-15 · تركيبات علامة كاشف · Brand mark lockups · 🟢 جاهز
- **ماذا / what:** Several 'K' marks: aubergine mono square (pro), lavender-to-mint gradient tile (legacy), pale-mint leaf-shaped serif K (KOSIF 4), purple gradient tile (editorial/V5), lilac gradient tile (research lab).
- **كيف / how:** pro .brand-mark 44px #2f1b68 mono K 24px/700 + wordmark mono 20px ls .04em; legacy 42px gradient 145deg #f8efff -> #d9c3ff 60% -> #8fd8cd text #3b1272 weight 900; KOSIF4 42x46 #dbf6cd radius 13px 4px 13px 4px Georgia serif 34px; editorial gradient 145deg #4b2377 -> #24113f radius 14px.
- **أرقام / params:** wordmark letter-spacing .12-.16em
- **الدليل / proof:** `kosif-audit-pro/app/globals.css:348` · `kosif-audit-studio/styles.css:100` · `kosif-audit-studio/studio.css:26`

#### BRAND-16 · مجموعة أيقونات SVG مضمنة · Inline SVG sprite icon set (29 symbols) · 🟢 جاهز
- **ماذا / what:** Single hidden <svg> with 29 stroke icons referenced via <use href='#i-...'>, styled globally (stroke currentColor 1.8, round caps).
- **كيف / how:** <svg class='svg-sprite'><symbol id='i-mic' viewBox='0 0 24 24'>...</symbol></svg>; svg { stroke: currentColor; stroke-width:1.8 }.
- **أرقام / params:** 24x24 viewBox; ids: grid, upload, target, route, alert, book, file, inbox, users, report, play, search, moon, sun, menu, check, download, plus, filter, x, shield, link, trash, chart, gavel, command, mic, mic-off, print
- **الدليل / proof:** `kosif-audit-studio/legacy.html` · `kosif-audit-studio/styles.css:80`

#### BRAND-17 · وصفة أيقونة التطبيق · App icon recipe (radial glow + glass sheen) · 🟢 جاهز
- **ماذا / what:** 512px rounded-square icon: radial gradient background from an off-centre highlight, a white top sheen fading out at mid-height, the mark scaled 1.4, and a letter-spaced caption.
- **كيف / how:** radialGradient cx .28 cy .18 r 1.05 (#3a2f27 -> #1d1814 .55 -> #110e0b); rect rx 112; inset rect rx 104 with white .16 -> 0 at .5; mark translate(46 178) scale(1.4); text QUALITY CONTROL Montserrat 800 30px letter-spacing 3.
- **أرقام / params:** sizes 192 / 512 / 180 (apple-touch, rx 0)
- **الدليل / proof:** `kosif-earth-ci-fork/ui/art/sqc-icon.svg` · `kosif-earth-ci-fork/tools/brand/make_marks.py`

#### BRAND-18 · شعار الكبش التراثي · Ram emblem (heritage) · 🟢 جاهز
- **ماذا / what:** Flat vector ram head with a thick spiral horn and ridge strokes, brown tones on cream inside a rounded square.
- **كيف / how:** SVG 512, clipPath rx 112; horn strokes 50 and 34px round; ridges 5px.
- **أرقام / params:** #f4ead8 bg; #5b3519 / #7a4a24 / #9a6632 / #6e4420; eye #2b1a0f
- **الدليل / proof:** `kosif-earth-ci-fork/ui/art/ram.svg` · `kosif-earth-ci-fork/docs/rebuild/DESIGN_SYSTEM.md`

#### BRAND-19 · زخرفة فاصلة · Ornament divider · 🟢 جاهز
- **ماذا / what:** Tiny diamond-and-dots letterhead ornament for print strips.
- **كيف / how:** SVG 28x14: outlined diamond stroke 1.2, filled inner diamond, two dots r 1.2.
- **أرقام / params:** #8a5a2b / #b8864e
- **الدليل / proof:** `kosif-earth-ci-fork/ui/art/ornament.svg`

#### BRAND-20 · معالجات الكلمة الشعارية · Wordmark treatments (KOSIF EARTH) · 🟢 جاهز
- **ماذا / what:** Latin wordmarks built purely in CSS: 'KOSIF EARTH' with tracked caps and amber EARTH over video, and a door wordmark with large KOSIF plus a widely spaced 'E A R T H' tag.
- **كيف / how:** intro: Montserrat 800 clamp(15px,2.2vw,24px) letter-spacing .09em, b{color:#e8bd76}, text-shadow 0 2px 16px rgba(0,0,0,.35); door: .wm::before content 'KOSIF' 800 35px; ::after 'E A R T H' 700 12px #b9f3cd.
- **الدليل / proof:** `kosif-earth-ci-fork/ui/art/brand/earth-intro-20261009.css:8` · `kosif-earth-ci-fork/ui/art/brand/earth-office-door.css`

#### BRAND-21 · قالب تصميم إطار: Biennale Yellow · Frame preset: Biennale Yellow · 🟢 جاهز
- **ماذا / what:** Ready-made video design system 'Biennale Yellow' (1920x1080 primary, 9:16 and 1:1 documented) with type ramp, palette, components, a frame showcase and a caption skin.
- **كيف / how:** Adopt hyperframes-creative/frame-presets/biennale-yellow/FRAME.md as project frame.md; preview frame-showcase.html; caption-skin.html styles captions.
- **أرقام / params:** fonts: Instrument Serif display + Archivo + JetBrains Mono; colors: paper #E9E5DB, sun #F1EE2E, haze #F0DA7C, ink #1B2566, ember #E26B4A
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/biennale-yellow/FRAME.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/biennale-yellow/frame-showcase.html` · `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/biennale-yellow/caption-skin.html`

#### BRAND-22 · قالب تصميم إطار: BlockFrame · Frame preset: BlockFrame · 🟢 جاهز
- **ماذا / what:** Ready-made video design system 'BlockFrame' (1920x1080 primary, 9:16 and 1:1 documented) with type ramp, palette, components, a frame showcase and a caption skin.
- **كيف / how:** Adopt hyperframes-creative/frame-presets/blockframe/FRAME.md as project frame.md; preview frame-showcase.html; caption-skin.html styles captions.
- **أرقام / params:** fonts: Inter 800-900 uppercase + Space Grotesk; 4px black borders (neo-brutalist); colors: black #000, offwhite #FFFDF5, pink #FE90E8, blue #C0F7FE, green #99E885, yellow #F7CB46, cream #FFDC8B
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/blockframe/FRAME.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/blockframe/frame-showcase.html` · `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/blockframe/caption-skin.html`

#### BRAND-23 · قالب تصميم إطار: Blue Professional · Frame preset: Blue Professional · 🟢 جاهز
- **ماذا / what:** Ready-made video design system 'Blue Professional' (1920x1080 primary, 9:16 and 1:1 documented) with type ramp, palette, components, a frame showcase and a caption skin.
- **كيف / how:** Adopt hyperframes-creative/frame-presets/blue-professional/FRAME.md as project frame.md; preview frame-showcase.html; caption-skin.html styles captions.
- **أرقام / params:** fonts: Space Grotesk display/numerals + Inter body; colors: bg #fdfae7, cobalt #1e2bfa, text #111111/#6b6b6b/#9a9a9a, positive #059669, negative #dc2626
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/blue-professional/FRAME.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/blue-professional/frame-showcase.html` · `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/blue-professional/caption-skin.html`

#### BRAND-24 · قالب تصميم إطار: Bold Poster · Frame preset: Bold Poster · 🟢 جاهز
- **ماذا / what:** Ready-made video design system 'Bold Poster' (1920x1080 primary, 9:16 and 1:1 documented) with type ramp, palette, components, a frame showcase and a caption skin.
- **كيف / how:** Adopt hyperframes-creative/frame-presets/bold-poster/FRAME.md as project frame.md; preview frame-showcase.html; caption-skin.html styles captions.
- **أرقام / params:** fonts: Shrikhand tilted display + Libre Baskerville body + Space Grotesk chrome; stacked text-shadow; 3px+1.5px double border; colors: bg #FFFFFF, dark #1C1410, red #D8000F, light #F5F2EF
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/bold-poster/FRAME.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/bold-poster/frame-showcase.html` · `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/bold-poster/caption-skin.html`

#### BRAND-25 · قالب تصميم إطار: Broadside · Frame preset: Broadside · 🟢 جاهز
- **ماذا / what:** Ready-made video design system 'Broadside' (1920x1080 primary, 9:16 and 1:1 documented) with type ramp, palette, components, a frame showcase and a caption skin.
- **كيف / how:** Adopt hyperframes-creative/frame-presets/broadside/FRAME.md as project frame.md; preview frame-showcase.html; caption-skin.html styles captions.
- **أرقام / params:** fonts: Barlow body + IBM Plex Mono labels (0.14em); hairline dividers; colors: ink #111111, fire-orange #E85D26, cream #F0ECE5, muted #888880
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/broadside/FRAME.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/broadside/frame-showcase.html` · `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/broadside/caption-skin.html`

#### BRAND-26 · قالب تصميم إطار: Capsule · Frame preset: Capsule · 🟢 جاهز
- **ماذا / what:** Ready-made video design system 'Capsule' (1920x1080 primary, 9:16 and 1:1 documented) with type ramp, palette, components, a frame showcase and a caption skin.
- **كيف / how:** Adopt hyperframes-creative/frame-presets/capsule/FRAME.md as project frame.md; preview frame-showcase.html; caption-skin.html styles captions.
- **أرقام / params:** fonts: Bodoni Moda display + Space Grotesk; radial accent glows + grain overlay; colors: cream #F5F5F0, ink #1A1A1A, coral #E85D4E, lime #C4D94E, lavender #C5B5E0, sky #8BB4F7, violet #A06CE8, yellow #F2D160, peach #F5B895
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/capsule/FRAME.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/capsule/frame-showcase.html` · `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/capsule/caption-skin.html`

#### BRAND-27 · قالب تصميم إطار: Cartesian · Frame preset: Cartesian · 🟢 جاهز
- **ماذا / what:** Ready-made video design system 'Cartesian' (1920x1080 primary, 9:16 and 1:1 documented) with type ramp, palette, components, a frame showcase and a caption skin.
- **كيف / how:** Adopt hyperframes-creative/frame-presets/cartesian/FRAME.md as project frame.md; preview frame-showcase.html; caption-skin.html styles captions.
- **أرقام / params:** fonts: Playfair Display 400 + Inter; five warm-stone tones; colors: bg #EDE8E0/#E2DBD1, text #1A1A1A/#5A5A5A, accent #8A8178, line #B8B0A4
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/cartesian/FRAME.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/cartesian/frame-showcase.html` · `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/cartesian/caption-skin.html`

#### BRAND-28 · قالب تصميم إطار: Cobalt Grid · Frame preset: Cobalt Grid · 🟢 جاهز
- **ماذا / what:** Ready-made video design system 'Cobalt Grid' (1920x1080 primary, 9:16 and 1:1 documented) with type ramp, palette, components, a frame showcase and a caption skin.
- **كيف / how:** Adopt hyperframes-creative/frame-presets/cobalt-grid/FRAME.md as project frame.md; preview frame-showcase.html; caption-skin.html styles captions.
- **أرقام / params:** fonts: Newsreader display + Hanken Grotesk + DM Mono; colors: paper #F0EBDE/#E6E0CE, ink #1F2BE0, ink-soft #5560E5
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/cobalt-grid/FRAME.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/cobalt-grid/frame-showcase.html` · `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/cobalt-grid/caption-skin.html`

#### BRAND-29 · قالب تصميم إطار: Code Editorial · Frame preset: Code Editorial · 🟢 جاهز
- **ماذا / what:** Ready-made video design system 'Code Editorial' (1920x1080 primary, 9:16 and 1:1 documented) with type ramp, palette, components, a frame showcase and a caption skin.
- **كيف / how:** Adopt hyperframes-creative/frame-presets/code-editorial/FRAME.md as project frame.md; preview frame-showcase.html; caption-skin.html styles captions.
- **أرقام / params:** fonts: EB Garamond display + Inter + JetBrains Mono on warm-navy code surface; coral spike mark (fonts shipped, OFL); colors: ink #141413, cream #FAF9F5, tile #EFE9DE, coral #CC785C, navy #181715
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/code-editorial/FRAME.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/code-editorial/frame-showcase.html` · `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/code-editorial/caption-skin.html`

#### BRAND-30 · قالب تصميم إطار: Coral · Frame preset: Coral · 🟢 جاهز
- **ماذا / what:** Ready-made video design system 'Coral' (1920x1080 primary, 9:16 and 1:1 documented) with type ramp, palette, components, a frame showcase and a caption skin.
- **كيف / how:** Adopt hyperframes-creative/frame-presets/coral/FRAME.md as project frame.md; preview frame-showcase.html; caption-skin.html styles captions.
- **أرقام / params:** fonts: Bebas Neue uppercase tracked + Inter; 45-degree diagonal hatch; colors: coral #E85D5D, cream #F5F0E8, black #1A1A1A, gray #6B6B6B
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/coral/FRAME.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/coral/frame-showcase.html` · `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/coral/caption-skin.html`

#### BRAND-31 · قالب تصميم إطار: Creative Mode · Frame preset: Creative Mode · 🟢 جاهز
- **ماذا / what:** Ready-made video design system 'Creative Mode' (1920x1080 primary, 9:16 and 1:1 documented) with type ramp, palette, components, a frame showcase and a caption skin.
- **كيف / how:** Adopt hyperframes-creative/frame-presets/creative-mode/FRAME.md as project frame.md; preview frame-showcase.html; caption-skin.html styles captions.
- **أرقام / params:** fonts: Archivo Black display + Space Grotesk + JetBrains Mono taxonomy; four accents; colors: cream #EFE9D9, ink #0F0F0F, green #1F8A4C, pink #F06CA8, orange #E85A1F, yellow #F5C518
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/creative-mode/FRAME.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/creative-mode/frame-showcase.html` · `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/creative-mode/caption-skin.html`

#### BRAND-32 · قالب تصميم إطار: Daisy Days · Frame preset: Daisy Days · 🟢 جاهز
- **ماذا / what:** Ready-made video design system 'Daisy Days' (1920x1080 primary, 9:16 and 1:1 documented) with type ramp, palette, components, a frame showcase and a caption skin.
- **كيف / how:** Adopt hyperframes-creative/frame-presets/daisy-days/FRAME.md as project frame.md; preview frame-showcase.html; caption-skin.html styles captions.
- **أرقام / params:** fonts: Fredoka One + Quicksand; charcoal 3px outlines, hard offset shadows 6/4px no blur; colors: cream #F5F0E6, turquoise #7ECDC0, pink #F7C8D4, butter #FDE68A, mint #A8E6CF, lavender #D4A5E8, peach #FFCBA4, sky #A8D8F0, coral #F8635F
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/daisy-days/FRAME.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/daisy-days/frame-showcase.html` · `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/daisy-days/caption-skin.html`

#### BRAND-33 · قالب تصميم إطار: Editorial Forest · Frame preset: Editorial Forest · 🟢 جاهز
- **ماذا / what:** Ready-made video design system 'Editorial Forest' (1920x1080 primary, 9:16 and 1:1 documented) with type ramp, palette, components, a frame showcase and a caption skin.
- **كيف / how:** Adopt hyperframes-creative/frame-presets/editorial-forest/FRAME.md as project frame.md; preview frame-showcase.html; caption-skin.html styles captions.
- **أرقام / params:** fonts: Source Serif 4 (opsz axis) display + JetBrains Mono 500 uppercase chrome; flat paper depth; colors: green #2e4a2a, pink #e89cb1, cream #efe7d4, ink #1a1a17
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/editorial-forest/FRAME.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/editorial-forest/frame-showcase.html` · `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/editorial-forest/caption-skin.html`

#### BRAND-34 · شريط علامة مع نقطة متوهجة · HUD brand bar with glowing dot · 🟢 جاهز
- **ماذا / what:** A frosted top bar holds a glowing status dot, a two-tone wordmark and a pill flag, used across the film and the dashboard for a consistent product identity.
- **كيف / how:** #bar height 76 px, 2 px border rgba(157,255,180,.28), radius 26, bg rgba(8,26,25,.62), backdrop blur 6px; dot 18 px lime with 22 px glow; 'KOSIF STRUCTURAL TWIN' Grotesk 30 px ls .06em; flag Mono 20 px '3D · SIM'.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/bunny_twin/index.html:25` · `100-superskills/skills/kosif-montage-motion/examples/structural-twin-demo.html:6`

#### BRAND-35 · مظهر بطاقة العنوان في مشغل manifest · Manifest title-card canvas look · 🟢 جاهز
- **ماذا / what:** The browser picture of a manifest scene: dark slate background with an accent radial glow, a faint grid, three slowly rotating accent ellipses, an accent dot easing in, a rising Arabic title, a subtitle, a mono 'KOSIF / MOTION' mark, a scene counter and a progress bar.
- **كيف / how:** drawFrame(canvas, manifest, t) in manifest-player.js; pure in t (same t → same frame).
- **أرقام / params:** bg #11171b; glow centre (.28w,.25h) radius .8w accent+alpha 0x32; grid #ffffff0c every unit/12; ellipses radius unit*(.17+k*.045), alpha .12+k*.13, rotate t*.12+i*.3; ease = easeOutCubic over first 25% of a scene; title 600 weight Tahoma unit*.066 #f2f4f3 rising (1−e)*unit*.05; subtitle unit*.023 #b…
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/manifest-player.js:3`

#### BRAND-36 · المراجعة: لوحة هوية العلامة · Review: brand style panel (colours, fonts, logo) · 🟢 جاهز
- **ماذا / what:** Global brand colours (used everywhere via 'brand.<id>' references), headline/body fonts chosen from a curated list rendered in their own face, and a swappable logo.
- **كيف / how:** stylePane(); edits stored as brand.color.<id>, brand.font.<id>, brand.logo; colour fields require #RRGGBB.
- **أرقام / params:** font list order switches to Arabic-first when reel lang starts with 'ar'
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:762` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/review/index.html:336`

#### BRAND-37 · غلاف بعنوان عربي · Poster frame with Arabic title · 🟢 جاهز
- **ماذا / what:** Grabs a frame and sets an Arabic title on it for a cover/thumbnail.
- **كيف / how:** python tools.py thumb FILM --out cover.jpg [--at 2.0] [--text عنوان] [--size 1080x1920].
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/tools.py:1`

#### BRAND-38 · هوية بصرية أولاً · DESIGN.md identity gate · 🟢 جاهز
- **ماذا / what:** Mandatory DESIGN.md: 3-5 role colours, Arabic+Latin font, motion rules, do-not list.
- **كيف / how:** new_scene.py writes the template.
- **أرقام / params:** default palette bg #0F1A2B ink #F4F7FF accent #F6C76B second #2B86E0
- **الدليل / proof:** `100-superskills/skills/claude-animation-studio/scripts/new_scene.py` · `100-superskills/examples/demo2d/DESIGN.md`

#### BRAND-39 · عقد اختيار عائلة الأيقونات · Icon family selection contract · 📦 بأمر تثبيت
- **ماذا / what:** Choose one real SVG icon family per piece from a 26-family catalog (Lucide, Phosphor, Tabler, Radix, Carbon, Heroicons v1/v2, Iconoir, Remix, Fluent, etc.), use its native grid sizes and currentColor, verify the exact license.
- **كيف / how:** Local SVG components, no icon fonts or runtime CDN lookups.
- **أرقام / params:** Radix 15x15 grid; Carbon 16/20/24/32
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/97-frontend-design-director/206-frontend-design-director/references/iconography.md`

#### BRAND-40 · توكنز التصميم بثلاث طبقات · Three-tier design tokens · 📦 بأمر تثبيت
- **ماذا / what:** primitive (color.blue.600) -> semantic (color.text.default) -> component (button.bg.primary); themes swap semantic values only.
- **كيف / how:** Author W3C DTCG JSON ($value/$type), transform with Style Dictionary (npm, needs install) into CSS vars; scope themes via [data-theme][data-brand]. For video: a theme.json consumed by Remotion/GSAP scenes so one file re-brands every scene.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2278-design-systems-engineering/8697-design-token-architecture` · `kosif-atlas/skills/1394-stark/3327-design-tokens`

#### BRAND-41 · استخدام أيقونات Lucide · Lucide icon usage (pro) · 📦 بأمر تثبيت
- **ماذا / what:** Navigation and actions use lucide-react icons with data-icon placement hooks for directional nudges.
- **كيف / how:** import { Home, ListChecks, ClipboardCheck, FileCheck2, ShieldAlert, Scale, ChartNoAxesCombined, BookOpen, FileText, Bell, Moon, Sun, Upload, Menu ... } from 'lucide-react'.
- **أرقام / params:** default size 16px (size-4) in buttons; 18-28px in tiles
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-audit-pro/components/kosif/app-shell.tsx:4`

#### BRAND-42 · استيراد خط الهوية · Brand font import from files · 📦 بأمر تثبيت
- **ماذا / what:** Loads a user's TTF/OTF/WOFF/WOFF2 into the page and the caption font list, guessing family and weight from the file name.
- **كيف / how:** BRAND.addFont: FontFace(family, arrayBuffer,{weight}) + document.fonts.add; weight from name: black/heavy 900, extrabold 800, semibold 600, bold 700, medium 500, light/thin 300, variable/vf '100 900'; stored in IndexedDB 'basma-brand'.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:2612`

#### BRAND-43 · ألوان الهوية من اللوجو · Logo-derived brand palette · 📦 بأمر تثبيت
- **ماذا / what:** Derives primary/accent/text/bg colours from a logo image.
- **كيف / how:** BRAND.colorsFromImage: 64x64 sample, skip alpha<128, near-black (<40) and near-white grey; 4096 buckets weighted 1+2*saturation; distinct colours (L1>90); accent falls back to primary lightened 45%; bg dark #0d0d10 or primary*0.15.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:2608`

#### BRAND-44 · قراءة دليل الهوية · Brand guide parsing (CSS/JSON/PDF/zip) · 📦 بأمر تثبيت
- **ماذا / what:** Reads a brand folder, zip, JSON/CSS/text guide or PDF and fills logo, fonts, palette, name, handle and tagline.
- **كيف / how:** BRAND.importFiles: JSZip 3.10.1 from cdnjs, logo by name /logo|شعار|mark|icon|brand/ or first SVG; fonts by extension; BRAND.fromText finds #hex near primary/accent/background/text keywords (Arabic too) and 24 known font names; PDF via pdf.js (12 pages).
- **أرقام / params:** fonts recognised: Cairo, Tajawal, Almarai, IBM Plex Sans Arabic, Noto Kufi/Sans/Naskh Arabic, Readex Pro, Alexandria, Lalezar, Reem Kufi, Changa, Rubik, El Messiri, Amiri, Aref Ruqaa, Marhey, Lemonada, Harmattan, Markazi Text, Montserrat, Poppins, Inter, Roboto
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:2632` · `app/public/js/10_studio.js:2640`

#### BRAND-45 · طبقات صور حرة · Free picture layers (logo/product/sticker) · 📦 بأمر تثبيت
- **ماذا / what:** Pictures placed freely over the video: drag to move, wheel to resize, with entrance animation, opacity, timing and paste-from-clipboard.
- **كيف / how:** addLayer(): x,y fractions, width 0.04-2.5 of short side (wheel x1.06/0.94), anims pop (settle 'pop'), rise (U.E.out 0.5 s, 6% rise), fade (0.4 s), float (sin 1.6t, 1.2% m), none; shadow 3% m; 'make background', 'remove background', 'edit with Gemini' actions.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:2546` · `app/public/js/00_editor.js:2553`

#### BRAND-46 · حقيبة الهوية مع اللوجو وكارت النهاية · Brand kit with watermark and end card · 📦 بأمر تثبيت
- **ماذا / what:** Saved brand (logo, fonts, palette, name, handle, tagline, extra pictures) is applied to every film, montage and caption: palette lock, caption font, handle, corner logo watermark and an animated end card.
- **كيف / how:** BRAND.apply/layers: watermark at (0.84,0.07) width 16% on 9:16 or (0.9,0.1) width 12% otherwise, opacity 0.88, fade; end card scene 'brandend' 2.6 s at the end when duration > 6 s: radial bg primary 35%, logo 34% m with pop settle, name, tagline (accent) and handle staged at 0.35/0.6/0.85 s; brand pictures available to code scenes via u.image; persisted in localStorage + IndexedDB 'basma-brand'.
- **أرقام / params:** end card 2.6 s; watermark op 0.88
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:2580` · `app/public/js/10_studio.js:2658` · `app/public/js/10_studio.js:2670`

#### BRAND-47 · مولّد الشعار والأيقونات · Logo/icon generator script (SVG + headless PNG) · 📦 بأمر تثبيت
- **ماذا / what:** Python script that writes the four SQC SVGs from one parametric body() and rasterises PNG icons with a headless browser.
- **كيف / how:** python3 tools/brand/make_marks.py (from repo root): builds sqc-mark/-dark/logo/icon SVG, then Playwright (Python) chromium channel msedge screenshots at 192/512/180 with transparent background and writes payload/*.png.b64.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-earth-ci-fork/tools/brand/make_marks.py`

#### BRAND-48 · متغيرات القالب · Composition variables / templating · 📦 بأمر تثبيت
- **ماذا / what:** Declare typed variables, bind them to text/src, override per instance or per render for personalised batches.
- **كيف / how:** data-composition-variables JSON; data-var-text, data-var-src; data-variable-values on host; window.__hyperframes.getVariables(); render --variables / --variables-file / --batch rows.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/concepts/variables.mdx` · `kosif-one/vendor/hyperframes/docs/packages/cli.mdx`

#### BRAND-49 · ختام الدعوة للفعل · CTA Close · 📦 بأمر تثبيت
- **ماذا / what:** Display-size action line lands word by word, one CTA capsule pops with a single overshoot, then total stillness.
- **كيف / how:** Install with `npx hyperframes add cta-close` (copies to compositions/components/cta-close.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame capt…
- **أرقام / params:** action_line; button_label; vars: action_line=Make it happen; button_label=Start now; accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add cta-close` (copies to compositions/components/cta-close`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/cta-close/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/cta-close/cta-close.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/cta-close.mdx`

#### BRAND-50 · قفل الدعوة للفعل · CTA Lockup · 📦 بأمر تثبيت
- **ماذا / what:** Closing lockup: action line, accent CTA pill, supporting microcopy, confident hold.
- **كيف / how:** Install with `npx hyperframes add cta-lockup` (copies to compositions/components/cta-lockup.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame ca…
- **أرقام / params:** microcopy "Free while in beta"; vars: action_line=Start building today; button_label=Get HyperFrames; microcopy=Free while in beta; accent=green[green|blue|violet]
- **تثبيت / install:** `npx hyperframes add cta-lockup` (copies to compositions/components/cta-lockup`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/cta-lockup/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/cta-lockup/cta-lockup.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/cta-lockup.mdx`

#### BRAND-51 · ختام الشعار · Logo Brand Close · 📦 بأمر تثبيت
- **ماذا / what:** Display wordmark cascades in letter by letter, accent period lands last, tagline and wide-tracked mono URL settle, dead-still hold.
- **كيف / how:** Install with `npx hyperframes add logo-brand-close` (copies to compositions/components/logo-brand-close.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chrom…
- **أرقام / params:** wordmark; tagline; url; vars: wordmark=HYPERFRAMES; tagline=Write HTML. Render video.; url=hyperframes.heygen.com; accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add logo-brand-close` (copies to compositions/components/logo-brand-close`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/logo-brand-close/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/logo-brand-close/logo-brand-close.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/logo-brand-close.mdx`

#### BRAND-52 · لسعة الشعار · Logo Sting · 📦 بأمر تثبيت
- **ماذا / what:** Wordmark slams to final scale, fires one accent ring and one white impact frame, then holds.
- **كيف / how:** Install with `npx hyperframes add logo-sting` (copies to compositions/components/logo-sting.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame ca…
- **أرقام / params:** vars: wordmark=HYPERFRAMES; accent=green[green|blue|violet]
- **تثبيت / install:** `npx hyperframes add logo-sting` (copies to compositions/components/logo-sting`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/logo-sting/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/logo-sting/logo-sting.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/logo-sting.mdx`

#### BRAND-53 · بطاقة الإثبات الاجتماعي · Social Proof Card · 📦 بأمر تثبيت
- **ماذا / what:** App-store style close: wordmark, five stars, proof line, three feature icons and CTA capsule in a quiet stagger.
- **كيف / how:** Install with `npx hyperframes add social-proof-card` (copies to compositions/components/social-proof-card.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chr…
- **أرقام / params:** vars: brand=HyperFrames; proof=12,000+ creators; cta=Start rendering free; f1=Write|plain HTML; f2=Render|pixel-perfect; f3=Own|every line
- **تثبيت / install:** `npx hyperframes add social-proof-card` (copies to compositions/components/social-proof-card`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/social-proof-card/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/social-proof-card/social-proof-card.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/social-proof-card.mdx`

#### BRAND-54 · بطاقة شهادة · Testimonial Card · 📦 بأمر تثبيت
- **ماذا / what:** Customer quote reveals at reading pace, then avatar, name and handle settle.
- **كيف / how:** Install with `npx hyperframes add testimonial-card` (copies to compositions/components/testimonial-card.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chrom…
- **أرقام / params:** rating 5; vars: quote=This changed how we ship.; author=Ken Tanaka; handle=@ken; rating=5(0..5)
- **تثبيت / install:** `npx hyperframes add testimonial-card` (copies to compositions/components/testimonial-card`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/testimonial-card/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/testimonial-card/testimonial-card.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/testimonial-card.mdx`

#### BRAND-55 · بطاقة شهادة مفصلة · Testimonial Proof Card · 📦 بأمر تثبيت
- **ماذا / what:** Quote revealed line by line through a soft mask, avatar disc, mono name/role, company mark and one accent-underlined phrase.
- **كيف / how:** Install with `npx hyperframes add testimonial-proof-card` (copies to compositions/components/testimonial-proof-card.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (he…
- **أرقام / params:** emphasis substring; vars: quote=We shipped our launch video in a single afternoon; name=Maya Chen; role=Head of Product; company=NORTHWIND; emphasis=single afternoon; accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add testimonial-proof-card` (copies to compositions/components/testimonial-proof-card`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/testimonial-proof-card/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/testimonial-proof-card/testimonial-proof-card.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/testimonial-proof-card.mdx`

#### BRAND-56 · شريط الثقة · Trust Strip · 📦 بأمر تثبيت
- **ماذا / what:** Monochrome row of wide-tracked mono wordmarks fading in left-to-right by opacity only, then still.
- **كيف / how:** Install with `npx hyperframes add trust-strip` (copies to compositions/components/trust-strip.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame …
- **أرقام / params:** marks list; tone muted|ink; vars: marks=Northwind, Acme Corp, Globex, Initech, Umbra; tone=muted[muted|ink]; cues=; accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add trust-strip` (copies to compositions/components/trust-strip`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/trust-strip/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/trust-strip/trust-strip.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/trust-strip.mdx`

#### BRAND-57 · بلاطات الشعار · Wordmark Tiles · 📦 بأمر تثبيت
- **ماذا / what:** Wordmark resolves from colour noise into correctly cropped glyph tiles through a spatial GSAP wave.
- **كيف / how:** Install with `npx hyperframes add wordmark-tiles` (copies to compositions/components/wordmark-tiles.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium …
- **أرقام / params:** columns 12; waveStagger 40 ms; vars: text=LAUNCH; columns=12(8..14); waveStagger=40(15..50)
- **تثبيت / install:** `npx hyperframes add wordmark-tiles` (copies to compositions/components/wordmark-tiles`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/wordmark-tiles/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/wordmark-tiles/wordmark-tiles.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/wordmark-tiles.mdx`

#### BRAND-58 · شعار مجسم · Extruded Logo · 📦 بأمر تثبيت
- **ماذا / what:** Beveled 3D letters flip up one by one, the word swings so light rakes across bevels, then holds readable; chrome, gold or matte.
- **كيف / how:** Install with `npx hyperframes add extruded-logo` (copies the full composition to compositions/extruded-logo.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: Three.js 0.184.0 (CDN), Canvas 2D painter, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** Three.js; Geist OFL; 1920x1080; duration 5 s
- **تثبيت / install:** `npx hyperframes add extruded-logo` (copies the full composition to compositions/extruded-logo`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/extruded-logo/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/extruded-logo/extruded-logo.html`

#### BRAND-59 · بطاقة ترويج الأفاتار · HeyGen Avatar Promo Card · 📦 بأمر تثبيت
- **ماذا / what:** Portrait offer card with a moving avatar mosaic and bold promo type (avatar mp4s and bgm not shipped locally). [Local copy lacks 11 declared file(s), e.g. assets/av_r1k1.mp4.]
- **كيف / how:** Install with `npx hyperframes add heygen-avatar-promo-card` (copies the full composition to compositions/heygen-avatar-promo-card.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 10 s; 1080x1920; duration 10 s
- **تثبيت / install:** `npx hyperframes add heygen-avatar-promo-card` (copies the full composition to compositions/heygen-avatar-promo-card`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/heygen-avatar-promo-card/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/heygen-avatar-promo-card/heygen-avatar-promo-card.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/heygen-avatar-promo-card.mdx`

#### BRAND-60 · خاتمة الشعار · Logo Outro · 📦 بأمر تثبيت
- **ماذا / what:** Logo assembles piece by piece with glow bloom, tagline fade and URL pill.
- **كيف / how:** Install with `npx hyperframes add logo-outro` (copies the full composition to compositions/logo-outro.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: inline SVG, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 6 s; Google Fonts: Inter; 1920x1080; duration 6 s
- **تثبيت / install:** `npx hyperframes add logo-outro` (copies the full composition to compositions/logo-outro`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/logo-outro/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/logo-outro/logo-outro.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/logo-outro.mdx`

#### BRAND-61 · مقدمة شعار يوتيوب · Logo Intro Sequence · 📦 بأمر تثبيت
- **ماذا / what:** Logo stamp pops on a lined board, kicker gives way to title with accent arrow chip, seeded line distortion.
- **كيف / how:** Install with `npx hyperframes add yt-logo-intro` (copies the full composition to compositions/yt-logo-intro.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: inline SVG, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 6 s; 1920x1080; duration 6 s
- **تثبيت / install:** `npx hyperframes add yt-logo-intro` (copies the full composition to compositions/yt-logo-intro`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/yt-logo-intro/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/yt-logo-intro/yt-logo-intro.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/yt-logo-intro.mdx`

#### BRAND-62 · ترويج منتج · Example project: product-promo · 📦 بأمر تثبيت
- **ماذا / what:** Multi-scene product promo (logo intro, canvas scenes, logo outro) with SVG assets (20 s). [Local copy lacks its sub-compositions: compositions/scene1-logo-intro.html, compositions/scene2-4-canvas.html, compositions/scene5-logo-outro.html.]
- **كيف / how:** Starter project: `npx hyperframes init --example product-promo` style scaffold (index.html mounts sub-compositions via data-composition-src); reuse its palette/type as a style reference.
- **أرقام / params:** 1920x1080; 20 s
- **تثبيت / install:** `npx hyperframes init --example product-promo` style scaffold (index`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/examples/product-promo/registry-item.json` · `kosif-one/vendor/hyperframes/registry/examples/product-promo/index.html`

#### BRAND-63 · سؤال التصميم: موجود أو اختيار بالعين أو تفويض · Design ask: have / pick-by-eye / leave · 📦 بأمر تثبيت
- **ماذا / what:** The design spec question has three states: use the user's frame.md/design.md, open 2-3 preset showcases in a browser so the user picks by eye (stored as style_preset), or let the workflow's design step decide/generate a design picker.
- **كيف / how:** Open frame-presets/<name>/frame-showcase.html for 2-3 fitting presets; record style_preset in BRIEF.md; for captured sites say the pick is layout bones, colors get remixed from the brand.
- **أرقام / params:** 2-3 presets shown
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes/references/capability-menu.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-creative/frame-presets/coral/frame-showcase.html`

#### BRAND-64 · مخطط مشهد: تجميع الشعار وتثبيته · Blueprint: Logo assemble lockup · 📦 بأمر تثبيت
- **ماذا / what:** A brand mark comes to exist (parts assemble, letters cascade, outline draws, camera pushes through negative space, spring bloom, morph from phrase, pixel streak) and resolves to a centered lockup + URL/CTA.
- **كيف / how:** Pick from hyperframes-animation/blueprints-index.md by role, then read hyperframes-animation/blueprints/logo-assemble-lockup.md for the multi-phase recipe; cite blueprint id per beat in the storyboard.
- **أرقام / params:** duration 4.4-11 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/logo-assemble-lockup.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints-index.md`

#### BRAND-65 · مخطط مشهد: تحول الشعار إلى زر دعوة ونقرة · Blueprint: CTA morph press · 📦 بأمر تثبيت
- **ماذا / what:** A resting brand mark condenses into a brighter CTA and a cursor lands a human-aimed click; hook variant morphs a lone pill into a menu/prompt card.
- **كيف / how:** Pick from hyperframes-animation/blueprints-index.md by role, then read hyperframes-animation/blueprints/cta-morph-press.md for the multi-phase recipe; cite blueprint id per beat in the storyboard.
- **أرقام / params:** duration 4-6 s (hook 5-7.5 s)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/cta-morph-press.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints-index.md`

#### BRAND-66 · ملف المواصفات البصرية frame.md · frame.md design spec (video-first DESIGN.md) · 📦 بأمر تثبيت
- **ماذا / what:** A design system rewritten for the camera: frontmatter tokens (colors, type ramp in cqw units, spacing, borders) are normative brand truth, prose is context; resolution order frame.md -> design.md -> DESIGN.md.
- **كيف / how:** hyperframes-creative/references/design-spec.md; adopt a preset FRAME.md as frame.md; build-frame.mjs applies it in narrative workflows.
- **أرقام / params:** type sizes in cqw (container-query width units)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-creative/references/design-spec.md` · `kosif-one/vendor/hyperframes/README.md`

#### BRAND-67 · منتقي التصميم بلوحات المزاج · Design picker mood boards · 📦 بأمر تثبيت
- **ماذا / what:** Generates contextual mood boards (architecture objects, palettes, preview_html with content tokens) served as an HTML page for the user to pick a direction.
- **كيف / how:** references/design-picker.md + templates/design-picker.html.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-creative/references/design-picker.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-creative/templates/design-picker.html`

#### BRAND-68 · فئة موشن: كشف الشعار · Motion-graphics category: Logo reveal · 📦 بأمر تثبيت
- **ماذا / what:** Category module: logo sting / lockup ~3-5 s, often alpha overlay; logo-outro block, svg-path-draw.
- **كيف / how:** Director sets category 'logo-reveal' in shot-plan.json; builder follows motion-graphics/categories/logo-reveal/module.md reuse-first.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/motion-graphics/categories/logo-reveal/module.md` · `kosif-one/vendor/hyperframes/skills/motion-graphics/SKILL.md`

#### BRAND-69 · قالب موسيقي: logo-split-lockup-pulse · Music template: logo-split-lockup-pulse · 📦 بأمر تثبيت
- **ماذا / what:** Two-part mark splits to open a gap, grows a center lockup per onset, snap-closes and pulses.
- **كيف / how:** Pick in music-to-video/references/template-catalog.md by frame pacing + mood; fill params in the storyboard; brand comes from frame.md; copy references/templates/logo-split-lockup-pulse/index.html (program.json where present).
- **أرقام / params:** 2-4 s (>4.5 s reads stretched)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/music-to-video/references/templates/logo-split-lockup-pulse/index.html` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/template-catalog.md`

#### BRAND-70 · دمج القالب مع هوية العلامة · Preset-to-frame.md remix (build-frame.mjs) · 📦 بأمر تثبيت
- **ماذا / what:** Copies a preset FRAME.md to frame.md and remixes brand tokens from capture/extracted/tokens.json onto the preset's color roles and swaps display/body fonts, plus copies the preset caption skin.
- **كيف / how:** node <skill>/scripts/build-frame.mjs --preset <name> --hyperframes .
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/faceless-explainer/scripts/build-frame.mjs` · `kosif-one/vendor/hyperframes/skills/product-launch-video/scripts/build-frame-colors.test.mjs` · `kosif-one/vendor/hyperframes/skills/product-launch-video/scripts/build-frame-subsets.test.mjs`

#### BRAND-71 · شعار يتجمع بضمّ المسافات بين الحروف · Lockup letter-spacing collapse · 📦 بأمر تثبيت
- **ماذا / what:** The end-card wordmark condenses from wide tracking and blur into tight tracking, then a travelling dot lands as its full stop.
- **كيف / how:** fromTo #lock {letterSpacing 0.22em, opacity 0.4, blur 8px} → {−0.03em, 1, 0} 0.8 s E.out; dot tween to (1403,584) scale 0.42 E.rest; M.push world 1→1.045 over 2.6 s.
- **أرقام / params:** 132 px/700 wordmark, 44 px subline
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/index.html:133` · `100-superskills/skills/kosif-montage-motion/scripts/projects/showreel/index.html:135`

#### BRAND-72 · إطار العلامة بغمر لوني · Brand flood end frame · 📦 بأمر تثبيت
- **ماذا / what:** The brand frame is a full-screen colour flood opened by an iris from the hero shape, with a Latin wordmark and an Arabic version line revealed word by word.
- **كيف / how:** #brand radial gold gradient; #b1 'KOSIF Motion' Space Grotesk 150 px/700 ls −0.03em; #b2 Cairo 78 px/800 'نسخة ٥٫٢'; revealWords at 4.15 s (0.6 s, stagger .06) and 4.35 s.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/five_sec/index.html:22` · `100-superskills/skills/kosif-montage-motion/scripts/projects/five_sec/index.html:84`

#### BRAND-73 · تكامل: canvas-design skill · Integration: canvas-design skill · 📦 بأمر تثبيت
- **ماذا / what:** Catalogued skill/MCP/library (link only; not installed here).
- **كيف / how:** see official setup
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`

#### BRAND-74 · قالب logo-reveal · Motion template logo-reveal · 📦 بأمر تثبيت
- **ماذا / what:** Arabic-first HTML/GSAP motion template 'logo-reveal'.
- **كيف / how:** mtemplates.py new NAME --template logo-reveal --set key=value [--seconds --size 1080x1920 --fps 30]; render via motion.py render --engine studio
- **أرقام / params:** SVG path pen-drawn then filled, viewBox 120x136
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/mtemplates.py:35`

#### BRAND-75 · تحويل الشعار إلى متجه · Logo/flat art vectorizer · 📦 بأمر تثبيت
- **ماذا / what:** Traces pure colours of a logo/icon (8x smooth upscale, edge-blend detection) into stacked polygons and an SVG; photos become 24-colour posters.
- **كيف / how:** vectorize.py (studio vector mode); vector_scene.build() grows each layer from its centre.
- **أرقام / params:** export 3840x2560
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-studio/vectorize.py` · `kosif-one/tools/kosif-studio/vector_scene.py` · `kosif-one/tools/kosif-studio/scenes/aghnam_logo.json`

#### BRAND-76 · تحويل لمتجه · Vectorize logo/photo to SVG · 📦 بأمر تثبيت
- **ماذا / what:** Traces logos with true colours and adjacent-blend test; photos k-means 24 colours; SVG + 3840x2560 export; vector_scene.py turns trace into layered program.
- **كيف / how:** python3 vectorize.py image
- **أرقام / params:** k=24
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/pixel-studio-painter/scripts/vectorize.py` · `100-superskills/skills/pixel-studio-painter/scripts/vector_scene.py`

#### BRAND-77 · تحويل الشعارات إلى متجه بألوانها الحقيقية · Logo/flat-art vectorisation with true colours · 📦 بأمر تثبيت
- **ماذا / what:** Traces an image into stacked vector colour layers with holes: it finds the pure colours (skipping antialias blends), enlarges smoothly so edges become curves, traces contours per colour and grows each layer slightly so no seams show.
- **كيف / how:** vectorize.trace(path) -> {source,size,photo,layers[{color,name,area,centre,polys[{hole,pts}]}],silhouette}; python vectorize.py img or studio.py --trace img.
- **أرقام / params:** up=8x cubic, simplify 0.85 px (approxPolyDP), grow 2 px ellipse dilation, sharpen 0.9, min_area 0.9, max_side 520, max 16 colours, min share 0.1%, colour merge distance 30
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/vectorize.py:1` · `kosif-studio/vectorize.py:188` · `kosif-studio/scenes/aghnam_logo.json`

#### BRAND-78 · إعلان منتج عربي: ذبيحة كاملة · Arabic product ad poster (whole lamb) · 📦 بأمر تثبيت
- **ماذا / what:** A vector product ad on a dark studio backdrop: gold-gradient Arabic headline, weight pill, rounded badge logo, cleaver and knife block, sheep with rim light, branded box with red band and phone numbers, garlic/spice/rosemary, three trays of meat with fat marbling, vignette and grain.
- **كيف / how:** python studio.py ad_whole_sheep; helpers rrect(), badge(), meat(), lines(); coordinates remapped by P()/M() (8/9 scale, +200 x).
- **أرقام / params:** badge #a8c13a/#ffffff/#e3161d; headline #f6e3b6 -> #c49c5c; pill #ead6b0 -> #cfb085; table #2a1010/#3a1616; meat #d24a52/#b3313b/#7e1e26; fat #f2d6cc; band #c91a1f
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/scenes/ad_whole_sheep.py:1` · `kosif-studio/scenes/ad_whole_sheep.py:27` · `kosif-studio/scenes/ad_whole_sheep.py:82`

#### BRAND-79 · عرض تتبّع شعار أغنام الوادي · Logo trace showcase (Aghnam al-Wadi) · 📦 بأمر تثبيت
- **ماذا / what:** A 155x183 client logo traced into 8 exact colour layers, exported as SVG and as a 1200x800 sign-painter reveal.
- **كيف / how:** studio.py --trace sources/aghnam_logo.png; scenes/aghnam_logo.json loads as an exact-colour scene.
- **أرقام / params:** colours #ffffff #f4040b #aec638 #090905 #89a53f #70933d #a3a39f #cedd26
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/scenes/aghnam_logo.json` · `kosif-studio/out/aghnam_logo.svg` · `kosif-studio/out/aghnam_logo_1200x800.png`

#### BRAND-80 · تجميع الشعار النهائي · Logo lockup assembly · 📦 بأمر تثبيت
- **ماذا / what:** End card where letters tighten from wide tracking and blur into place while the camera keeps breathing.
- **كيف / how:** gsap fromTo letterSpacing/opacity/filter + M.push
- **أرقام / params:** letter-spacing 0.22em→−0.03em, opacity .4→1, blur 8→0 px in 0.8 s; push 1→1.045 over 2.6 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/projects/showreel/index.html:127`

#### BRAND-81 · كشف شعار · Style: Logo reveal (logo-reveal) · 📦 بأمر تثبيت
- **ماذا / what:** Logo assembled from its own shapes via mask, draw-on or morph, then held.
- **كيف / how:** SVG logo paths; resample to 64-128 pts for morph 500-800ms; draw-on; 800-1200ms reveal + 1s hold. Scaffold: python3 tools/kosif.py scaffold logo-reveal <dir>.
- **أرقام / params:** reveal 800-1200ms
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `style:logo-reveal` · `kosif-tool/playbooks/ads.md`

#### BRAND-82 · بطاقة شعار بحلقة مرسومة وعلامة · Remotion logo card ring draw + chevron mark · 📦 بأمر تثبيت
- **ماذا / what:** Glass card springs in from scale .8, a r=150 accent ring draws around via dashoffset, an original stem+chevron mark springs in, then title and 'Made with KOSIF' line fade up.
- **كيف / how:** card spring damping 14 stiffness 90 mass 1.1; ring progress(8,40,inOutCubic); mark spring from frame 18 damping 11 stiffness 160; text progress(34,18)
- **أرقام / params:** card 760 px, radius 48, bg paper@.06, border paper@.12, stroke 34 for mark
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/starters/remotion/src/Film.tsx:449`

#### BRAND-83 · مقابلة الهوية لعميل بلا هوية · Brand-identity interview for no-brand clients · 🔑 مفتاح/خدمة
- **ماذا / what:** Short interview in three parts (product, brand feel via three adjectives and light/dark, shape language sharp vs rounded) mapped to font pairs and a color variant; the original generates pages via Google Stitch (external key).
- **كيف / how:** Ask at most 4 forcing questions (product+pitch, audience, brand overrides, tone) then commit; map adjectives to fonts e.g. technical -> Geist/Space Grotesk, warm -> Nunito Sans/Rubik/Manrope, authority -> IBM Plex Sans/Public Sans.
- **أرقام / params:** 28 font enums; 4 questions max
- **الدليل / proof:** `kosif-atlas/skills/3454-brand-landingpage/14160-brand-landingpage` · `kosif-atlas/skills/3454-brand-landingpage/14160-brand-landingpage/references/interview-framework.md` · `kosif-atlas/skills/3454-brand-landingpage/14160-brand-landingpage/references/stitch-architecture.md`

#### BRAND-84 · Recraft للمتجهات وأسلوب العلامة · Recraft for native vector and brand style · 🔑 مفتاح/خدمة
- **ماذا / what:** Recraft V3/V4 outputs true SVG vectors and accepts a brand-style upload, making it the route for icons, marks and illustration sets that must scale.
- **كيف / how:** Upload 3-10 on-brand references as a brand style, generate SVG, then animate the SVG paths directly (stroke draw-on, morph) in code; overlay exact brand hex afterwards.
- **أرقام / params:** 3-10 style refs
- **الدليل / proof:** `kosif-atlas/skills/2306-generative-web-media/8854-prompt-to-asset-routing` · `kosif-atlas/skills/2306-generative-web-media/8850-brand-conditioned-generation` · `kosif-atlas/skills/1446-marketing-skills/3504-image`

#### BRAND-85 · غلاف مرسوم من إطار حقيقي · Painted cover from a real frame · 🔑 مفتاح/خدمة
- **ماذا / what:** Use a real captured frame as the image reference so a painted cover keeps the true layout and promises nothing the product lacks.
- **كيف / how:** Pick the busiest frame, crop 16:9 around a focus point to 1600x900 under 400 KB; for a painted variant pass '@file:frame.png' as reference and describe what is on screen (palette, time of day, action), not the title.
- **أرقام / params:** 1600x900; <400 KB
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3889-art`

#### BRAND-86 · موجز شعار ضد الرداءة ومجموعة الشعار · Anti-slop logo brief and logo suite · 🔑 مفتاح/خدمة
- **ماذا / what:** Generated marks drift to a generic middle unless the brief is constrained; the curated vector, not a regenerated raster, is the deliverable.
- **كيف / how:** Positive constraints (works in one flat colour, reads at 16 px, mark works without wordmark), negatives (no gradient mesh, no swoosh/globe, avoid default SaaS blue), reference-anchored intent; generate many, human curates and modifies; spec primary, stacked, mark-only, wordmark-only, clear-space, min-size, mono.
- **أرقام / params:** favicon legibility 16 px
- **الدليل / proof:** `kosif-atlas/skills/2248-brand-identity-studio/8561-logo-and-visual-system-direction`

#### BRAND-87 · جلب الشعار الرسمي للعلامة · Official brand logo resolution · 🔑 مفتاح/خدمة
- **ماذا / what:** Fetches the official mark (theSVG.org, then GitHub org avatar, then domain favicon) and never redraws a logo by hand.
- **كيف / how:** npx hyperframes media-use resolve --type logo --intent 'stripe' --project .
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/media-use/references/resolve.md` · `kosif-one/vendor/hyperframes/skills/media-use/references/setup-providers.md`

#### BRAND-88 · الاستيراد من فيجما · Figma import: assets, tokens, components, storyboards, motion, shaders · 🔑 مفتاح/خدمة
- **ماذا / what:** Five phases: rendered assets (sanitized SVG) and brand tokens bound as var() via REST/CLI, components, Motion animations via an MCP connector translated to GSAP, shaders from connector or native export; a Figma SECTION of frames is read as motion states, not slides.
- **كيف / how:** figma/SKILL.md routing; separate scoped credentials for REST and MCP; determinism rules.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/figma/SKILL.md`

#### BRAND-89 · تكامل: Canva MCP · Integration: Canva MCP · 🔑 مفتاح/خدمة
- **ماذا / what:** Catalogued skill/MCP/library (link only; not installed here).
- **كيف / how:** see official setup
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/tools-catalog-2.md`

#### BRAND-90 · مربعات تدور وتثبت حول الأيقونة · Orbit-lock icon reveal · 👁 شوهد في فيديو
- **ماذا / what:** App squircle shrinks from large while a grey halo grows; 4 coloured rounded squares spin in counter-clockwise, decelerate and lock at N/E/S/W; then collapse into a row as icon shrinks
- **أرقام / params:** orbit r≈216 px, lock in ~0.5 s, squares 92 px
- **الدليل / proof:** `style:pm-notdwd-7de38a` · `style:pm-notdwd-c2037d`

#### BRAND-91 · بطاقة نهاية مع زر ومؤشر ينقر · CTA end card with cursor click · 👁 شوهد في فيديو
- **ماذا / what:** Logo + wordmark, tagline with accent phrase underlined, URL pill + filled CTA button; cursor glides in and button depresses (scale 0.96) on click
- **أرقام / params:** cursor move 500 ms easeOut, click scale 0.96 for 120 ms
- **الدليل / proof:** `style:pm-0xfemyn-e114d3`

#### BRAND-92 · بطاقات نيو-بروتاليست بظل صلب · Neo-brutalist card system · 👁 شوهد في فيديو
- **ماذا / what:** cards with 3 px black border, hard offset shadow (6px 6px 0 #111), pastel fill, white inner panel, uppercase pill label; each actor gets its own fill colour
- **أرقام / params:** radius 0-6 px; colours pink #f47fe0, cyan #c8f8f8, green #9bf08a, yellow #f0cf4a
- **الدليل / proof:** `style:pm-0xnfrith-5be616`

#### BRAND-93 · انفجار خطوط حول الشعار · Radial spark logo burst · 👁 شوهد في فيديو
- **ماذا / what:** logo icon spin-in, 40 radial lines shoot out and fade 400 ms
- **الدليل / proof:** `style:pm-adamdesgns-478d6d`

#### BRAND-94 · معرض أمثلة وشريط شعارات · Social-proof gallery + logo strip · 👁 شوهد في فيديو
- **ماذا / what:** Two rows of example cards drifting in opposite directions, edge fade masks; logo row marquee at bottom in grey
- **أرقام / params:** drift 20px/s; edge fade 10%
- **الدليل / proof:** `style:pm-ai-baymax-0ef9dd`

#### BRAND-95 · بطاقة ختام بشعار وشعار لفظي واسم · Logo + tagline + byline end card · 👁 شوهد في فيديو
- **ماذا / what:** Icon tile above product name, accent tagline below, tiny byline; build top-down with 200 ms stagger
- **أرقام / params:** icon 100 px, name 60 px, tagline 30 px
- **الدليل / proof:** `style:pm-alex-prompter-1ea044`

#### BRAND-96 · تجميع شعار المربعات · Tile logo assemble · 👁 شوهد في فيديو
- **ماذا / what:** 4 rounded tiles scale in and one recolours
- **أرقام / params:** stagger 100 ms
- **الدليل / proof:** `style:pm-amol909s-27533e`

#### BRAND-97 · بطاقة ختام فوق مشهد مموه · Blurred end card · 👁 شوهد في فيديو
- **ماذا / what:** darken+blur scene, logo, 2-line tagline, URL pill
- **أرقام / params:** fade 500 ms
- **الدليل / proof:** `style:pm-anas0ra-e57aea`

#### BRAND-98 · بطاقة ختام مع عمود بطاقات يتحرك · End card with scrolling tile column · 👁 شوهد في فيديو
- **ماذا / what:** left: big title + two-line tagline + black URL pill with red dot and soft shadow; right: a column of real preview tiles scrolls upward continuously
- **أرقام / params:** scroll ~60 px/s, pill shadow 0 12 24 rgba(0,0,0,.15)
- **الدليل / proof:** `style:pm-antonio-kodheli-490109`

#### BRAND-99 · شعار بحروف تقفز مع رابط · Letter-pop wordmark + URL pill · 👁 شوهد في فيديو
- **ماذا / what:** Logo icon then wordmark letters spring in individually with slight overshoot, tagline with coloured keywords, URL inside a rounded pill with arrow
- **أرقام / params:** letter stagger 50 ms, overshoot 1.1
- **الدليل / proof:** `style:pm-aschapmann-131210`

#### BRAND-100 · شريط شعارات متعدد · Multi-row logo marquee · 👁 شوهد في فيديو
- **ماذا / what:** 3 rows, alternating direction, center items bright, edges dim
- **الدليل / proof:** `style:pm-astrodevil-3f2054`

#### BRAND-101 · بطاقة نهاية بشعار ونقطة متوهجة · Wordmark end card with glow dot · 👁 شوهد في فيديو
- **ماذا / what:** Heavy extended wordmark, accent red dot as period with radial glow behind, underline draws on, mono tagline types in
- **أرقام / params:** glow radius 300px alpha 0.35, underline 500 ms
- **الدليل / proof:** `style:pm-ayushunleashed-ece3e3`

#### BRAND-102 · شعار ثلاثي الأبعاد متساوي القياس · Isometric logo end card · 👁 شوهد في فيديو
- **ماذا / what:** Build the logo from extruded coloured tiles in isometric view assembling together, wordmark wipes in beside, tagline below
- **أرقام / params:** extrusion 12 px, assemble 600 ms back-out
- **الدليل / proof:** `style:pm-bizibeast-10f264`

#### BRAND-103 · بطاقة ختام باسم يُكتب وروابط · Typed name end card with contact pills · 👁 شوهد في فيديو
- **ماذا / what:** Avatar badge + name typed with caret, underline rule draws, role line and outline pills for contacts pop in, script sign-off
- **أرقام / params:** type 40 ms/char, pills stagger 60 ms
- **الدليل / proof:** `style:pm-blushpetal795-0c85c2`

#### BRAND-104 · أغلفة قوائم تشغيل مصممة · Designed playlist sleeves · 👁 شوهد في فيديو
- **ماذا / what:** Flat colour squares with bold 2-line uppercase title, motif (concentric rings or vertical bars), tiny footer label
- **أرقام / params:** yellow/pink/blue/sage/purple/orange
- **الدليل / proof:** `style:pm-brainextends-e19ac3`

#### BRAND-105 · تجمّع العناصر نحو الشعار · Converge-to-logo end lockup · 👁 شوهد في فيديو
- **ماذا / what:** Covers converge to centre and scale down behind the icon which grows from the same point; icon then shifts left as wordmark and two-line tagline reveal
- **أرقام / params:** converge 800 ms, lockup gap 0.3em
- **الدليل / proof:** `style:pm-brainextends-e19ac3`

#### BRAND-106 · بطاقة صُنع بـ · Built-with end card · 👁 شوهد في فيديو
- **ماذا / what:** condensed display 2 lines + underlined subtitle + small specs row
- **الدليل / proof:** `style:pm-buildfastwithai-ed9447`

#### BRAND-107 · رسم حلقة حول الشعار · Logo ring draw-on · 👁 شوهد في فيديو
- **ماذا / what:** Black disc icon with logo; a thick cyan ring stroke draws around it with outer glow; tracked mono brand name fades below
- **أرقام / params:** ring 700 ms, stroke 14 px, glow 30 px
- **الدليل / proof:** `style:pm-ceowinkz-7c776b`

#### BRAND-108 · ظهور الشعار بتوهج · Logo glow resolve · 👁 شوهد في فيديو
- **ماذا / what:** Icon pops, wordmark types, soft accent radial glow, URL pill
- **الدليل / proof:** `style:pm-danilowm-d3720d`

#### BRAND-109 · شعار مع رقم إصدار متدرّج · Logo lockup with gradient version number · 👁 شوهد في فيديو
- **ماذا / what:** icon tile + bold wordmark + version number filled with blue→violet linear gradient, small mono URL underneath; fade/scale-in 500 ms
- **أرقام / params:** gradient #1f7bf2→#7b5cf5
- **الدليل / proof:** `style:pm-ddryo-loos-300829`

#### BRAND-110 · ختم دائري مسنن · Scalloped seal badge · 👁 شوهد في فيديو
- **ماذا / what:** Star-polygon with many points (~24) as rim, inner circle with number + label, rotate-in and gentle wobble
- **أرقام / params:** 24 points, rotate -30°->0, wobble ±3°
- **الدليل / proof:** `style:pm-deebeeeff-50fcd0`

#### BRAND-111 · دخول بطاقة الشعار بنابض · Logo card spring entrance · 👁 شوهد في فيديو
- **ماذا / what:** Rounded white card with accent border holds a raster logo; spring scale-in, later tween smaller and up for re-layout
- **أرقام / params:** spring k=200 d=14; shrink to 0.6 in 500 ms
- **الدليل / proof:** `style:pm-deebeeeff-50fcd0`

#### BRAND-112 · بطاقة ختام بأيقونة ورابط · App end card with URL pill · 👁 شوهد في فيديو
- **ماذا / what:** glowing rounded app icon, two-tone wordmark, tracked uppercase tagline, row of outline chips, solid lime URL pill button, all centred over dim footage
- **أرقام / params:** stagger 120 ms, hold 4-5 s
- **الدليل / proof:** `style:pm-deifosv-04e4d3`

#### BRAND-113 · ختم أحمر توقيعًا للمشهد · Seal stamp signature · 👁 شوهد في فيديو
- **ماذا / what:** After the last verse, stamp a small red square seal with scale 1.2 -> 1 and slight rough-edge texture
- **أرقام / params:** #c0302a, 150 ms punch, multiply blend
- **الدليل / proof:** `style:pm-demitiyageekzen-7770ad`

#### BRAND-114 · إطار ثابت للهوية حول كل المشاهد · Persistent broadcast chrome frame · 👁 شوهد في فيديو
- **ماذا / what:** Fix logo top-left, product mark + mono tag top-right, mono URL bottom-left and caption bottom-right across all scenes; only centre content changes
- **أرقام / params:** inset 4% each side; mono 11-12 px @1080p uppercase letterspacing 0.15em
- **الدليل / proof:** `style:pm-elliot-garreffa-f334bc`

#### BRAND-115 · شعار ضخم في التذييل · Giant footer wordmark · 👁 شوهد في فيديو
- **ماذا / what:** oversized text bleeding off bottom edge, slide up
- **الدليل / proof:** `style:pm-ercankeskinx-ec2568`

#### BRAND-116 · مصفوفة توليد علامات من معاملات · Parametric mark generator matrix · 👁 شوهد في فيديو
- **ماذا / what:** Rows = parameters (body, slot, depth, width, corner, turn, fill, offset), columns = values; highlight chosen cell per row, connect with a polyline, assemble final mark; caption total combinations
- **أرقام / params:** 8 params × 6 values = 1,679,616 combos; row stagger 120 ms
- **الدليل / proof:** `style:pm-fionntobin-97b7af`

#### BRAND-117 · الشعار ثم اسم العلامة ينزلق · Logo mark then wordmark slide · 👁 شوهد في فيديو
- **ماذا / what:** centre icon alone with radial glow, then shift left as serif wordmark reveals right, tagline + URL fade below
- **أرقام / params:** shift 400 ms, reveal mask 500 ms
- **الدليل / proof:** `style:pm-gabrielbuzziv-4ff0c6`

#### BRAND-118 · ختام أيقونة بتوهج · App icon glow end card · 👁 شوهد في فيديو
- **ماذا / what:** Icon centred on black with purple radial glow, name, tagline, store pill button
- **أرقام / params:** glow radius ~40% width
- **الدليل / proof:** `style:pm-gautam-mer1-2ae354`

#### BRAND-119 · بطاقة ختام باسم ونقطة حمراء · Wordmark + red dot end card · 👁 شوهد في فيديو
- **ماذا / what:** wide caps wordmark slides in letter by letter with motion blur, red dot pops with an expanding thin ring, italic subtitle and mono meta row
- **أرقام / params:** letters stagger 40 ms, ring scale 0->1 400 ms
- **الدليل / proof:** `style:pm-ghinaiya-nirmal-5d8fec`

#### BRAND-120 · شريط تاريخ مخطط · Striped date banner · 👁 شوهد في فيديو
- **ماذا / what:** 4 thin colour bars (violet, orange, pink, blue, each ~6px) above a white label box with dark bold uppercase date; bars scaleX 0->1 from left 300 ms then label fades
- **أرقام / params:** width 88% of frame
- **الدليل / proof:** `style:pm-gonzalomacagno-2de1a9`

#### BRAND-121 · شعار مع خط إطارات مفتاحية · Keyframe-diamond wordmark lockup · 👁 شوهد في فيديو
- **ماذا / what:** Red rotated-square diamond + heavy wordmark; below, a thin line draws left to right while diamond keyframes drop onto it; mono meta line (07 SCENES · 900 FRAMES · 128 BPM) types on; tagline with last 
- **كيف / how:** Red rotated-square diamond + heavy wordmark; below, a thin line draws left to right while diamond keyframes drop onto it; mono meta line (07 SCENES · 900 FRAMES · 128 BPM) types on; tagline with last words in accent; optional second-language subtitle; confetti squares drift
- **أرقام / params:** line draw 600 ms, key drop stagger 60 ms
- **الدليل / proof:** `style:pm-grace-sunnyy-29bc61`

#### BRAND-122 · بطاقة ختام مع حبوب · Logo end card with pills · 👁 شوهد في فيديو
- **ماذا / what:** logo + tagline + 3 pill tags stagger 80ms
- **الدليل / proof:** `style:pm-ho-ba-f3f0e9`

#### BRAND-123 · شعار بشرطات ملونة · Accent hyphen wordmark · 👁 شوهد في فيديو
- **ماذا / what:** WORD-WORD-WORD with hyphens in accent orange
- **الدليل / proof:** `style:pm-hqmank-7c61f1`

#### BRAND-124 · بطاقة رقم الإصدار · Version release card · 👁 شوهد في فيديو
- **ماذا / what:** Logo lockup, huge serif version number, accent rule draws under it, tracked 'OUT NOW' label fades in
- **أرقام / params:** rule draw 400 ms, label letter-spacing 0.2em
- **الدليل / proof:** `style:pm-iammxfschr-d68f90`

#### BRAND-125 · شعار بتدرج · Gradient wordmark end · 👁 شوهد في فيديو
- **ماذا / what:** teal→yellow linear gradient text over residual particles
- **الدليل / proof:** `style:pm-ismailfahmi-557268`

#### BRAND-126 · لوحات أعمال · Case-study panels · 👁 شوهد في فيديو
- **ماذا / what:** each case its own palette full-frame
- **الدليل / proof:** `style:pm-jacksonfall-54b2ac`

#### BRAND-127 · بطاقة ختام باسم ونقطة ملونة · Wordmark + dot end card · 👁 شوهد في فيديو
- **ماذا / what:** Lowercase heavy wordmark with an accent-coloured round period, hairline rule, tracked mono role line, italic serif CTA in accent, tiny chapter index footer
- **أرقام / params:** rule draws 400 ms; stagger 150 ms
- **الدليل / proof:** `style:pm-jasonzhou1993-8595e0`

#### BRAND-128 · بطاقة ختام بمدار · Orbiting logo end card · 👁 شوهد في فيديو
- **ماذا / what:** logo tile with ellipse orbit + small satellite dots
- **الدليل / proof:** `style:pm-jayscambler-3f8889`

#### BRAND-129 · نقطة ختام بلون العلامة · Brand full-stop dot · 👁 شوهد في فيديو
- **ماذا / what:** end every hero word with a circular period in the brand colour that pops in 1-2 frames after the word lands
- **أرقام / params:** dot = x-height * 0.45, scale 0 -> 1.2 -> 1 in 180 ms
- **الدليل / proof:** `style:pm-jhylee95-e1152f`

#### BRAND-130 · مزاوجة سيرف مع سانس ثقيل · Serif + heavy sans pairing · 👁 شوهد في فيديو
- **ماذا / what:** Editorial serif for headlines, wide tracked heavy sans for labels
- **أرقام / params:** tracking 0.3em
- **الدليل / proof:** `style:pm-kangaroohere-b10f8d`

#### BRAND-131 · بطاقة ختام بأمر تثبيت في الطرفية · Terminal install end card · 👁 شوهد في فيديو
- **ماذا / what:** logo wordmark large with accent glyph + a boxed terminal line '$ npm i ...' typed with blinking block cursor, version/tag line in mono
- **أرقام / params:** type 40 ms/char, cursor blink 500 ms
- **الدليل / proof:** `style:pm-kyonax-on-tech-aabc1d`

#### BRAND-132 · بطاقة ختام بسيطة · Minimal end card · 👁 شوهد في فيديو
- **ماذا / what:** Logo wordmark with lime dot, tracked mono tagline, lime pill CTA, URL below, on black
- **أرقام / params:** hold 3-4s
- **الدليل / proof:** `style:pm-leadnotifi-e83f94`

#### BRAND-133 · بطاقة شعار مع زر رابط · Logo end card with URL pill · 👁 شوهد في فيديو
- **ماذا / what:** Centred wordmark, one-line tagline with the same italic-serif emphasis word, white URL pill button with arrow, tiny footnote line; hold 4-6 s
- **أرقام / params:** fade 600 ms
- **الدليل / proof:** `style:pm-listudio-820c7b`

#### BRAND-134 · بطاقة شعار على أسود · Minimal logo end card on black · 👁 شوهد في فيديو
- **ماذا / what:** logo + name + url centered
- **الدليل / proof:** `style:pm-macrohou-33959d`

#### BRAND-135 · بطاقة اسم بخط عريض معدني · Chrome extended name card · 👁 شوهد في فيديو
- **ماذا / what:** Extended-wide uppercase name with vertical metallic gradient, spaced role line between hairlines, italic serif tagline with one accent-coloured word
- **أرقام / params:** name tracking 0.05em, tagline fade per word 120 ms
- **الدليل / proof:** `style:pm-madhav-xo-f97f20`

#### BRAND-136 · شريط أحمر مائل للعنوان · Diagonal red band title lockup · 👁 شوهد في فيديو
- **ماذا / what:** rotated (~-12 deg) crimson rectangle slams across; title in white on it; square outlined stamp glyph at corner; spaced Latin subtitle below on thin rule
- **أرقام / params:** band #cd002f, rotate -12deg, slam 150 ms
- **الدليل / proof:** `style:pm-majin-appsheet-2d3c1a`

#### BRAND-137 · بطاقة عنوان بإطار ذهبي · Framed title card · 👁 شوهد في فيديو
- **ماذا / what:** painting in gold frame, side panel with script title and CTA
- **الدليل / proof:** `style:pm-mandelduck-95fd08`

#### BRAND-138 · بطاقة نهاية بالشعار · Logo end card · 👁 شوهد في فيديو
- **ماذا / what:** Centred app icon tile, wordmark below, tagline, URL in outlined pill, small mono footer of 3 value propositions separated by dots; soft blue vignette behind
- **أرقام / params:** elements stagger 120 ms fade-up
- **الدليل / proof:** `style:pm-marouanegazouzi-6071d5`

#### BRAND-139 · زر نابض · Pulsing CTA button · 👁 شوهد في فيديو
- **ماذا / what:** red rounded icon with expanding rings and particle dots
- **أرقام / params:** ring 1s loop
- **الدليل / proof:** `style:pm-melvynx-6cde6c`

#### BRAND-140 · رسم الشعار خطاً ثم ملؤه · Logo stroke draw-on then fill · 👁 شوهد في فيديو
- **ماذا / what:** render logo shapes as open stroke chevrons, animate dashoffset, then fade fill to solid white with glow
- **أرقام / params:** draw ~1.5 s, fill 300 ms
- **الدليل / proof:** `style:pm-micheleharmonic-77628e`

#### BRAND-141 · كشف الشعار على خط أفق · Horizon-line logo reveal · 👁 شوهد في فيديو
- **ماذا / what:** thin bright horizontal line expands, glow arc above, logo slides in
- **الدليل / proof:** `style:pm-misbahsy-80eaec`

#### BRAND-142 · ختام بتجميع الشعار · Logo assemble ending · 👁 شوهد في فيديو
- **ماذا / what:** stroke grows into mark, wordmark fades, tagline
- **الدليل / proof:** `style:pm-miskinho-443898`

#### BRAND-143 · شعار بحروف ملونة مع أشكال كونفيتي · Per-letter colour wordmark with confetti · 👁 شوهد في فيديو
- **ماذا / what:** Each letter a different palette colour, pop-in stagger; underline bar wipes; geometric primitives (circle, triangle, ring, diamond, x) bob around; typewriter subtitle
- **أرقام / params:** letter stagger 60 ms, bob amplitude 6 px period 2 s
- **الدليل / proof:** `style:pm-motiondsgnr-9dcfa6`

#### BRAND-144 · بطاقة ختام بشعار نصي متوهج · Glowing wordmark end card · 👁 شوهد في فيديو
- **ماذا / what:** hard cut to black; centred white wordmark with text-shadow bloom (0 0 30px rgba(255,255,255,.5)) and subtle radial lift
- **أرقام / params:** hold ~2 s
- **الدليل / proof:** `style:pm-notdwd-c2037d`

#### BRAND-145 · بطاقة الشعار بنبضة · Logo end card ring pulse · 👁 شوهد في فيديو
- **ماذا / what:** icon scale 0→1 spring, expanding ring stroke opacity fade
- **الدليل / proof:** `style:pm-oliahmed205-3e31c4`

#### BRAND-146 · شعار بخط اليد وزر دعوة · Script wordmark + CTA end card · 👁 شوهد في فيديو
- **ماذا / what:** centred handwritten logotype fades from pale to brand red, tagline below, small black button 'Start free →', mono pricing footnote and domain
- **أرقام / params:** fade 600 ms
- **الدليل / proof:** `style:pm-palashbagchi11-0a4b6b`

#### BRAND-147 · بطاقة نهاية بنقطة معلّقة · Pendulum dot end card · 👁 شوهد في فيديو
- **ماذا / what:** empty frame, a thin line drops from the top with a blue dot swinging to rest (damped), name types in bottom-right
- **أرقام / params:** damping ~1.5 s
- **الدليل / proof:** `style:pm-pankajkumar-dev-0bee87`

#### BRAND-148 · بطاقة ختام بزر يُنقر · Clicked CTA end card · 👁 شوهد في فيديو
- **ماذا / what:** logo, two-line offer, CTA button with arrow and URL text; cursor moves in and clicks the button
- **أرقام / params:** hold ~2 s
- **الدليل / proof:** `style:pm-paulo-kombucha-96431c`

#### BRAND-149 · ختام بشعار وتوقيع · Logo resolve lockup · 👁 شوهد في فيديو
- **ماذا / what:** asterisk mark spins in centred, then slides left while wordmark + rule + tracked subtitle reveal on the right; tiny credits in bottom corners
- **أرقام / params:** ~1.5 s, ease-out cubic
- **الدليل / proof:** `style:pm-prasenx-8d9323`

#### BRAND-150 · شعار بكسلي مع كتابة · Pixel logo + typing · 👁 شوهد في فيديو
- **ماذا / what:** pixel squares assemble then mono typing
- **الدليل / proof:** `style:pm-quickdesignio-dd93d0`

#### BRAND-151 · كشف الشعار بقناع · Mask wordmark reveal · 👁 شوهد في فيديو
- **ماذا / what:** Icon pops, then wordmark revealed by a clip rect expanding left→right
- **أرقام / params:** clip 600 ms easeOutExpo
- **الدليل / proof:** `style:pm-ratheejaisal-1f4538`

#### BRAND-152 · بطاقة ختام بزر يُنقر · Cursor click CTA end card · 👁 شوهد في فيديو
- **ماذا / what:** Centred logo + tagline + blue pill button; cursor glides in and clicks (button scale 0.96→1)
- **أرقام / params:** cursor path 600 ms, click 120 ms
- **الدليل / proof:** `style:pm-ratheejaisal-1f4538`

#### BRAND-153 · بطاقة ختام بناء الحروف · Letter-build end card · 👁 شوهد في فيديو
- **ماذا / what:** letters appear one by one with red dot accent
- **الدليل / proof:** `style:pm-rendesr-86be44`

#### BRAND-154 · تمايل الشعار · Logo float bob · 👁 شوهد في فيديو
- **ماذا / what:** sin y offset on mascot logo
- **أرقام / params:** amp 6px, 2 s period
- **الدليل / proof:** `style:pm-rneayan-474bcf`

#### BRAND-155 · شعار بسيط مع "متاح الآن" · Minimal logo + 'Out now' end · 👁 شوهد في فيديو
- **ماذا / what:** Black glyph above product name in bold sans, small grey 'Out now' typed beneath; hold 2 s while music fades on a dB curve
- **أرقام / params:** hold 2 s
- **الدليل / proof:** `style:pm-rossaxbt-3085b7`

#### BRAND-156 · انفجار شعار نجمي · Asterisk logo burst · 👁 شوهد في فيديو
- **ماذا / what:** 12 spokes scale from 0 length out of centre dot with 25-35 ms stagger and backOut, inside a thin outline circle
- **أرقام / params:** spoke width 6px, coral #f04a35
- **الدليل / proof:** `style:pm-roundtablespace-d3a1be`

#### BRAND-157 · شعار ختامي مع زر ونقرة مؤشر · Logo lock-up + CTA click · 👁 شوهد في فيديو
- **ماذا / what:** App icon scales in alone at centre, slides left as the wordmark wipes in, tagline and button fade up; cursor glides to button and click ripple ring expands and fades
- **أرقام / params:** icon 400 ms back.out, ripple 0->60 px radius 400 ms
- **الدليل / proof:** `style:pm-samuel-yostt-891f87`

#### BRAND-158 · شعار بموجة صوتية ملونة · Waveform logo end card · 👁 شوهد في فيديو
- **ماذا / what:** Vertical rounded bars of varying height in rainbow palette animate like an equaliser next to a heavy wordmark; underline draws; status pill
- **أرقام / params:** 7 bars; 120ms stagger
- **الدليل / proof:** `style:pm-shinskinakamoto-20190b`

#### BRAND-159 · كشف الشعار ببكرات قمار · Slot reel logo reveal · 👁 شوهد في فيديو
- **ماذا / what:** Vertical reels with motion blur decelerate and land on the brand mark one reel after another
- **أرقام / params:** 3 reels, stop stagger 250 ms
- **الدليل / proof:** `style:pm-spearwtf-3c1fd1`

#### BRAND-160 · بطاقة نهاية بتدرج · Gradient mesh end card · 👁 شوهد في فيديو
- **ماذا / what:** blurred pastel blobs under logo + CTA buttons
- **الدليل / proof:** `style:pm-steventey-0d20e4`

#### BRAND-161 · كلمات تتبدل بالقطع مع نقطة مربعة · Square-dot kinetic word cuts · 👁 شوهد في فيديو
- **ماذا / what:** one uppercase word per beat, hard cut every 0.5 s, alternating navy-on-cream and white-on-navy, always ending in a yellow square full stop
- **أرقام / params:** beat 15-16 frames at 30 fps
- **الدليل / proof:** `style:pm-sudeepsd-1a3485`

#### BRAND-162 · نص دائري · Circular text ring · 👁 شوهد في فيديو
- **ماذا / what:** text on circle path rotating around logo
- **الدليل / proof:** `style:pm-sudiyasa-f48ac9`

#### BRAND-163 · تغليف أيقونة · App-icon wrap · 👁 شوهد في فيديو
- **ماذا / what:** rounded square gradient grows behind logo
- **الدليل / proof:** `style:pm-tdinh-me-815acb`

#### BRAND-164 · ختام باسم الحساب · Handle lock-up end · 👁 شوهد في فيديو
- **ماذا / what:** Vertical accent bar left of the handle, letters rise in stagger, underline wipes across, small mono call-to-action typed below with cursor
- **أرقام / params:** letters 60ms stagger; underline 400ms
- **الدليل / proof:** `style:pm-techhalla-7acbc2`

#### BRAND-165 · نقطة تسقط لتكمل الشعار · Dot-drop period on wordmark · 👁 شوهد في فيديو
- **ماذا / what:** Wordmark sits between two thin rules; a red dot (stretched while falling) drops from above and bounces to become the full stop; then subtitle and 'available for work' meta fade in
- **أرقام / params:** fall 400 ms, squash 0.7 on impact, 2 bounces
- **الدليل / proof:** `style:pm-teslachartz-c58b32`

#### BRAND-166 · بطاقة نهاية زرقاء · Brand blue end card · 👁 شوهد في فيديو
- **ماذا / what:** logo + badge + 2-line pitch + URL pill
- **الدليل / proof:** `style:pm-thayto-dev-44b911`

#### BRAND-167 · بطاقة عنوان بحروف متباعدة · Spaced-caps title card · 👁 شوهد في فيديو
- **ماذا / what:** light sans uppercase, tracking 0.5em, per-letter fade+y settle stagger 60 ms, small emblem above, tagline tiny below, then 'COMING YEAR'
- **أرقام / params:** on pure black, 6-8 s hold
- **الدليل / proof:** `style:pm-theparuchh-6e08c3`

#### BRAND-168 · أيقونات طعام لطيفة بوجوه · Kawaii flat icon set · 👁 شوهد في فيديو
- **ماذا / what:** Simple shapes with thick outline, dot eyes and small smile; consistent stroke and palette across 8-10 objects
- **أرقام / params:** stroke 4px; eyes 2 dots; smile arc
- **الدليل / proof:** `style:pm-thilina-a-891c09`

#### BRAND-169 · بطاقة ختام بزر دعوة · End card CTA · 👁 شوهد في فيديو
- **ماذا / what:** Logo + small caps subline, mascot centre, row of icons popping in stagger, pill CTA button with shadow, small store line
- **أرقام / params:** 3s hold; icons stagger 60ms
- **الدليل / proof:** `style:pm-thilina-a-891c09`

#### BRAND-170 · بطاقة نهاية بشعار يتضح · Logo resolve end card · 👁 شوهد في فيديو
- **ماذا / what:** icon with expanding ring, wordmark from blur to sharp, then tagline with blue second clause, bullet list and URL fade in
- **أرقام / params:** blur 16px->0, 500 ms
- **الدليل / proof:** `style:pm-thismacapital-dfba20`

#### BRAND-171 · بطاقة نهاية بالشعار · Wordmark end card · 👁 شوهد في فيديو
- **ماذا / what:** black bold lowercase word with period on off-white
- **الدليل / proof:** `style:pm-twoclipping-221cab`

#### BRAND-172 · النقطة كنقطة حرف · Dot as letter tittle · 👁 شوهد في فيديو
- **ماذا / what:** replace i-dot with accent circle that lands with bounce
- **الدليل / proof:** `style:pm-ultimaxbt-bbebf5`

#### BRAND-173 · نقطة حمراء كعلامة تجارية · Red-dot punctuation brand mark · 👁 شوهد في فيديو
- **ماذا / what:** wordmark ending with a period replaced by a red circle that pops with overshoot and a thin orbit ring
- **أرقام / params:** scale 0->1.2->1 in 250 ms, #e0262b
- **الدليل / proof:** `style:pm-vanshwtfff-db0466`

#### BRAND-174 · شارة صغيرة بنقطة حيّة · Pill label with live dot · 👁 شوهد في فيديو
- **ماذا / what:** rounded-full outlined pill, uppercase tracked micro text, red dot pulsing
- **أرقام / params:** font 11-13 px 700, letter-spacing 0.12em, border 1px
- **الدليل / proof:** `style:pm-viktoroddy-98c1d8`

#### BRAND-175 · ختام بشعار ينزلق ويكشف الاسم · Logo + wordmark mask reveal end card · 👁 شوهد في فيديو
- **ماذا / what:** Icon centred, slides left while wordmark is revealed by a left-to-right clip mask; URL fades below
- **أرقام / params:** 600 ms easeOutExpo
- **الدليل / proof:** `style:pm-wozu-co-242285`

#### BRAND-176 · ختام بالشعار وزر · Logo + CTA resolve · 👁 شوهد في فيديو
- **ماذا / what:** Logo mark assembles, tagline types, orange CTA button pops with scale 0.9→1
- **أرقام / params:** last 5 s
- **الدليل / proof:** `style:pm-xelandre-363f00`

#### BRAND-177 · نقطة كعلامة هوية · Dot as punctuation brand · 👁 شوهد في فيديو
- **ماذا / what:** orange circle used as period in JUST CODE. and 5.5
- **الدليل / proof:** `style:pm-zheke-38deff`

#### BRAND-178 · انفتاح اسم الشعار من خلف الأيقونة · Wordmark unfold from behind icon · 👁 شوهد في فيديو
- **ماذا / what:** icon spring pop scale 0->1; wordmark container maxWidth 0->auto with overflow hidden, pushes icon sideways; giant faint backdrop word at 6-8% opacity behind
- **أرقام / params:** spring damping ~12, unfold 0.5 s
- **الدليل / proof:** `style:product`

#### BRAND-179 · ورقة نظام الهوية للفيديو · Video brand system sheet · 📄 موصوف
- **ماذا / what:** A compact production rule-set so separate videos read as the same brand: palette roles, type families and safe sizes per format, framing, entrance/settle/transition/hold timing, sound roles, cover/closing treatment, export checks.
- **كيف / how:** Derive values from real design tokens and record the source for each; keep motion/design constants in one shared file (CSS :root or a JS config) used by every composition; compare exports side by side for drift.
- **أرقام / params:** roles: background, surface, text, accent
- **الدليل / proof:** `kosif-atlas/skills/101-video-skills/221-video-brand-system/SKILL.md` · `kosif-atlas/skills/101-video-skills/221-video-brand-system`

#### BRAND-180 · استخراج هوية الموقع · Site capture extraction set · 📄 موصوف
- **ماذا / what:** From a URL extract design tokens (top colors, font families/weights), visible text tagged by element, downloaded assets with descriptions, animation inventory, Lottie and video manifests, even WebGL shader source, plus full-height viewport screenshots.
- **كيف / how:** Playwright (installed globally, Chromium present): screenshot every viewport with ~30% overlap at 1920x1080; collect getComputedStyle colors/fonts; dump h1/p/a text with tag prefixes; list <canvas>, lottie, video. Optional Gemini vision for asset captions (key, ~$0.001/image).
- **أرقام / params:** scroll screenshots 1920x1080, ~30% overlap; summarize 5-7 colors, fonts, sections, CTAs, vibe sentence
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/step-1-capture.md` · `kosif-atlas/skills/3594-design-clone/14410-design-clone`

#### BRAND-181 · استخراج رموز التصميم من الأنماط المحسوبة · Computed-style design token extraction · 📄 موصوف
- **ماذا / what:** Turn a live page into a token map: radii (min/median/max -> small/medium/large, >=9999 -> pill), shadows grouped by blur into elevation levels, transition durations into micro/normal/macro and their easing, max content width, breakpoints, density.
- **كيف / how:** Playwright page.evaluate over all elements' getComputedStyle; dedupe and rank; store as tokens.json; use as mood input only (do not clone a brand).
- **أرقام / params:** breakpoint sweep 1440 -> 768 -> 390
- **الدليل / proof:** `kosif-atlas/skills/3594-design-clone/14410-design-clone` · `kosif-atlas/skills/895-brightdata-plugin/2042-design-mirror` · `kosif-atlas/skills/895-brightdata-plugin/2042-design-mirror/references/css-extraction.md`

#### BRAND-182 · MG-021 شعار يرسم بخط واحد · MG-021 Single-stroke logo draw then fill · 📄 موصوف
- **ماذا / what:** A line traces the logo outline, then the outline becomes a full fill.
- **كيف / how:** 0-2 s draw, 2-2.6 s fill, 2.6-4 s hold. SVG logo paths with stroke-dasharray/dashoffset, then cross-fade to the filled copy; simplify the reveal path for complex marks without changing the identity. Thin pen then short tone.
- **أرقام / params:** 4 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-brand-identity.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### BRAND-183 · MG-022/025 تجميع الشعار من كتل أو نقاط · MG-022/025 Assembled mark · 📄 موصوف
- **ماذا / what:** Three blocks slide in from different directions with different accelerations and lock into the symbol (MG-022), or a few dots leave a regular grid and travel to the logo contour before merging (MG-025).
- **كيف / how:** MG-022: 0-0.6 prep, 0.6-1.8 assemble, 1.8-3 hold; respect proportions and clear space. MG-025: 0-1 grid, 1-2.8 travel, 2.8-4 merge - computed start/end positions, no paid particle plugin needed: sample points with SVGPathElement.getPointAtLength and tween from grid slots.
- **أرقام / params:** 3 s / 4 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-brand-identity.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### BRAND-184 · MG-023/030 شعار بظل مار أو من ضباب · MG-023/030 Shadow-pass and fog logo reveals · 📄 موصوف
- **ماذا / what:** A slanted shadow sweeps a floor and leaves the logo looking engraved (MG-023, premium); thin fog drifts sideways to unveil the mark (MG-030, calm ending).
- **كيف / how:** MG-023: 0-1 floor, 1-2.8 shadow pass, 2.8-4 hold; masks + inner shadow + fake gradient light - say it is a 2D simulation without a 3D model. MG-030: 0-1 fog, 1-3 reveal, 3-5 hold; noise or fog footage as mask with opacity; don't let glow erase logo contrast. Local: CSS gradients/mask-position; SVG feTurbulence fog.
- **أرقام / params:** 4 s / 5 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-brand-identity.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### BRAND-185 · MG-024 ختم حبر للعلامة · MG-024 Ink stamp · 📄 موصوف
- **ماذا / what:** A stamp lands and leaves the logo with irregular ink edges - a crafted sign-off.
- **كيف / how:** 0-0.6 s drop, 0.6-1 s print, 1-2.5 s hold; short scale+rotation keys with an ink-texture luma matte (mask-image grunge). Keep a clean logo version for small sizes. Dry stamp hit.
- **أرقام / params:** 2.5 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-brand-identity.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### BRAND-186 · MG-027 شعار من نافذة سلبية · MG-027 Negative-space window reveal · 📄 موصوف
- **ماذا / what:** Coloured shapes close over the screen leaving a hole shaped exactly like the logo.
- **كيف / how:** 0-1.4 s shapes approach, 1.4-2 s hole forms, 2-3 s hold; inverted alpha matte (SVG mask with the logo as hole). Test contrast with light and dark logo versions.
- **أرقام / params:** 3 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-brand-identity.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### BRAND-187 · نظام هوية الفيديو · Video brand system · 📄 موصوف
- **ماذا / what:** Small production rulebook derived from real brand tokens: palette roles (bg/surface/text/accent), type families and safe sizes per format, framing/camera behaviour, entrance/settle/transition/hold timings, sound roles (voice, UI SFX, music, silence), cover/closing treatment, export checks; compare e…
- **كيف / how:** Keep values in one JSON/tokens file shared by compositions
- **الدليل / proof:** `kosif-atlas/skills/101-video-skills/221-video-brand-system/SKILL.md`

#### BRAND-188 · فحص رخصة الخط · Font license check · 📄 موصوف
- **ماذا / what:** Desktop/print font licences rarely cover web or video embedding; verify before shipping.
- **كيف / how:** Prefer OFL fonts (Google Fonts, Noto, Cairo, Tajawal, IBM Plex Sans Arabic); record licence per font in the project credits.
- **الدليل / proof:** `kosif-atlas/skills/3438-ux-design/14126-web-typography/SKILL.md` · `kosif-atlas/skills/motion-graphics-ar/motion-typography/references/quality-and-editors.md`

#### BRAND-189 · رموز خطوط الهوية · Brand typography tokens · 📄 موصوف
- **ماذا / what:** Store families, scale ratio, weights, leading and tracking as tokens reused across every scene.
- **كيف / how:** JSON/CSS variables: --font-display, --font-text, --scale-ratio, --lh-display; scaffold per style.
- **الدليل / proof:** `kosif-atlas/skills/1503-universal-design-principles/3823-hierarchy-typographic/SKILL.md` · `kosif-atlas/skills/2406-web-design/9323-design-tokens-scaffolding/SKILL.md`

#### BRAND-190 · مصفوفة الثيمات متعددة العلامات · Multi-brand theming matrix · 📄 موصوف
- **ماذا / what:** Brands × modes = themes; components never know which theme is active.
- **كيف / how:** e.g. {brandA,brandB}×{light,dark}=4 semantic maps; CSS vars or a JS object passed as Remotion props.
- **الدليل / proof:** `kosif-atlas/skills/2278-design-systems-engineering/8697-design-token-architecture`

#### BRAND-191 · مونتاج شبكة الهوية · Brand grid montage · 📄 موصوف
- **ماذا / what:** Multi-cell moving grid mixing real UI moments with mark, palette and type — staggered so one cell dominates at a time.
- **كيف / how:** Remotion/HTML grid: 2×2 for 16:9/1:1, vertical stack for 9:16; each cell its own clock, avoid simultaneous flashes; check first/last frame of each clip for blanks.
- **أرقام / params:** 2×2 or stacked
- **الدليل / proof:** `kosif-atlas/skills/101-video-skills/213-brand-grid-video`

#### BRAND-192 · موجز الشعار: الفكرة الواحدة · Logo brief: the ONE THING · 📄 موصوف
- **ماذا / what:** Before drawing: one impression, audience+primary surface, 2-3 competitors and their territory, hard constraints; then decide fit-in vs break-out of category.
- **كيف / how:** Write brief block (Brand, ONE THING, For, Surface, Personality 3-5 adjectives, Must/Must-not feel, colour constraints) and confirm.
- **الدليل / proof:** `kosif-atlas/skills/1567-tonone/4425-form-logo`

#### BRAND-193 · اختيار نوع الشعار · Mark-type choice · 📄 موصوف
- **ماذا / what:** Wordmark for short phonetic names; lettermark for long names; combination mark as default for new products; pictorial/abstract needs recognition investment.
- **الدليل / proof:** `kosif-atlas/skills/1567-tonone/4425-form-logo`

#### BRAND-194 · قواعد بناء شعار SVG · SVG logo construction rules · 📄 موصوف
- **ماذا / what:** Logos as pure vector with path outlines (no <text>), viewBox only, preserveAspectRatio xMidYMid, hard-coded hex, semantic group ids (#mark, #wordmark) so they can be animated.
- **كيف / how:** Write SVG by hand or via Python; outline fonts with fonttools/opentype.js (needs install) for wordmarks; ids enable draw-on and part animation.
- **أرقام / params:** 32px legibility test
- **الدليل / proof:** `kosif-atlas/skills/1567-tonone/4425-form-logo`

#### BRAND-195 · مولد شعار نصي/حرفي/أيقونة · Deterministic wordmark/monogram/favicon generator · 📄 موصوف
- **ماذا / what:** From a brand profile (palette + heading font) produce wordmark, rounded-square monogram and 64×64 favicon SVGs with aria labels.
- **كيف / how:** Node script lib/logo.mjs buildLogos(profile,{text}) in brand-forge; idea reproducible here with a short Python/JS SVG template.
- **أرقام / params:** favicon 64×64
- **الدليل / proof:** `kosif-atlas/skills/1708-brand-forge/4714-generate-logo`

#### BRAND-196 · مواصفات حزمة الشعار · Logo suite specification · 📄 موصوف
- **ماذا / what:** Primary lockup, stacked, mark alone, wordmark alone, clear-space in mark units (e.g. cap-height), min size, one-colour, reversed/B&W, do/don't gallery (stretch, recolor, respace, drop shadow).
- **كيف / how:** Acid test: mark must be identifiable in flat B&W. Produce each variant before animating the logo sting.
- **الدليل / proof:** `kosif-atlas/skills/2248-brand-identity-studio/8561-logo-and-visual-system-direction`

#### BRAND-197 · قيود ضد الطابع العام · Anti-slop generation constraints · 📄 موصوف
- **ماذا / what:** Escape the generic middle with specific positive, negative and reference-anchored constraints.
- **كيف / how:** Positive: 'identifiable in one flat colour', 'reads at 16px'. Negative: 'no gradient mesh', 'no swoosh/globe', 'avoid SaaS blue'. Anchored: 'like X restraint but warmer'. Generate many, human curates.
- **الدليل / proof:** `kosif-atlas/skills/2248-brand-identity-studio/8561-logo-and-visual-system-direction`

#### BRAND-198 · تشريح دليل الهوية · Brand book anatomy (10 parts) · 📄 موصوف
- **ماذا / what:** Strategy+archetype, logo suite, colour (HEX/RGB/OKLCH + WCAG pairs), type + license class, grid, icons, imagery, voice, do/don'ts, governance incl. AI-content rules.
- **كيف / how:** Build as a living HTML hub reading the token file rather than a static PDF.
- **الدليل / proof:** `kosif-atlas/skills/2248-brand-identity-studio/8557-brand-book-assembly`

#### BRAND-199 · بوابة ترخيص الخطوط والملكية · Font-license and IP gate · 📄 موصوف
- **ماذا / what:** Before calling a brand deliverable final, record the font web/video license class and route IP/registrability claims to review; log human curation and modification of AI concepts.
- **كيف / how:** Keep a curation-and-authorship log next to the project.
- **الدليل / proof:** `kosif-atlas/skills/2248-brand-identity-studio/8557-brand-book-assembly` · `kosif-atlas/skills/2248-brand-identity-studio/8558-brand-legal-and-licensing`

#### BRAND-200 · محرك قواعد أنظمة التصميم المخصصة · Bespoke design-system grammar engine · 📄 موصوف
- **ماذا / what:** Reverse-engineers ~140 DESIGN.md systems into rules+rationale and forward-generates a 9-section DESIGN.md for a brief, with checks for coherence (WCAG, OKLCH uniformity, hue harmony), archetype, kansei and neighbour distinctiveness.
- **كيف / how:** Read the grammar/ and source-design-systems/ as a style library; the python checks exist but are unreviewed third-party — reimplement the math rather than run them.
- **أرقام / params:** max 7 questions in interactive mode
- **الدليل / proof:** `kosif-atlas/skills/3593-bespoke-design-system/14409-bespoke-design-system/SKILL.md` · `kosif-atlas/skills/3593-bespoke-design-system/SOURCE.md`

#### BRAND-201 · مجموعة أيقونات من SVG · Favicon/app-icon set from SVG · 📄 موصوف
- **ماذا / what:** From one square SVG produce ICO 32, apple-touch 180, PWA 192/512, maskable 512 with 409 safe zone, dark-mode SVG via prefers-color-scheme.
- **كيف / how:** ImageMagick magick (v7) or convert (v6 present here); svgo optional.
- **أرقام / params:** 32,180,192,512; safe 409
- **الدليل / proof:** `kosif-atlas/skills/3170-generate-favicon/13499-generate-favicon`

#### BRAND-202 · لافتة SQC · SQC banner art (README) · 📄 موصوف
- **ماذا / what:** Wide dark banner with glossy blue-to-white 3D SQC letters and 'SMART QUALITY CONTROL / AI-Powered Audit & Assurance Platform'.
- **كيف / how:** JPEG 1320x215, used at the top of README.
- **أرقام / params:** blue gradient letters on near-black
- **الدليل / proof:** `kosif-earth-ci-fork/ui/art/sqc-banner.jpg` · `kosif-earth-ci-fork/README.md`

#### BRAND-203 · توقيع العلامة · Brand mark corner signature · 📄 موصوف
- **ماذا / what:** Maker's name with a gold hairline in a top corner, sliding in at 0.4 s.
- **كيف / how:** V.brand, V.brand_side in verse.js.
- **أرقام / params:** 26*k px, weight 600, letter-spacing .32em, #F7EBD0; line 70*k px rgba(231,182,90,.9); opacity .92
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/templates/verse.html:194`

#### BRAND-204 · برومبت شعار بسيط · Minimal logo mark prompt · 📄 موصوف
- **ماذا / what:** Template for a clean flat vector logo concept.
- **كيف / how:** 'Minimal modern logo mark for [brand], [symbol idea], flat vector, [2 colours HEX], balanced negative space, centered on white, no extra text' — then vectorise/clean manually; generators garble text.
- **أرقام / params:** 2 HEX colours; white background
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-image-studio/references/prompt-library.md`

#### BRAND-205 · 3 اتجاهات شعار · 3 radical logo directions as SVG · 📄 موصوف
- **ماذا / what:** Brief (3 values, audience, competitors, anti-references) then 3 different SVG logos, pick and refine.
- **كيف / how:** hand-coded SVG
- **أرقام / params:** readable at 24px; no gradients in mono version
- **الدليل / proof:** `100-superskills/skills/brand-identity-logo/SKILL.md:21`

#### BRAND-206 · قوالب الهوية · Brand kit templates · 📄 موصوف
- **ماذا / what:** Cover, square post, story, card + brand.md + tokens.json.
- **كيف / how:** HTML/SVG templates
- **الدليل / proof:** `100-superskills/skills/brand-identity-logo/SKILL.md:25`

#### BRAND-207 · منصة صوت العلامة · Brand voice platform (vendored) · 📄 موصوف
- **ماذا / what:** 3-5 voice attributes, tone-shift rules, do/don't-say, glossary, messaging hierarchy.
- **كيف / how:** read sources
- **أرقام / params:** 3-5 attributes
- **الدليل / proof:** `100-superskills/skills/brand-identity-logo/references/sources.md:210`

#### BRAND-208 · كشف الشعار من أشكال العلامة · Brand-shape logo reveal / sting · 📄 موصوف
- **ماذا / what:** Logo built from the brand's own shapes (mask, draw-on, morph), wordmark wipes, tagline follows.
- **كيف / how:** SVG draw-on + fill + wipe.
- **أرقام / params:** 800–1200 ms reveal, hold 1 s; tagline fades 200 ms after wordmark
- **الدليل / proof:** `kosif-tool/playbooks/ads.md:29` · `kosif-tool/playbooks/ads.md:52`

#### BRAND-209 · حشد إلى شعار · Crowd to logo · 📄 موصوف
- **ماذا / what:** Particles drift in flow field, gather into logo, solid logo crossfades.
- **أرقام / params:** drift 1.5 s; gather 1.2 s; crossfade 300 ms
- **الدليل / proof:** `kosif-tool/playbooks/particles.md:42`

#### BRAND-210 · نقطة إلى شعار · Dot-to-logo recipe · 📄 موصوف
- **ماذا / what:** Dot drops on arc, squashes, recovers, morphs to mark, wordmark wipes.
- **أرقام / params:** 0–400 drop ease-in quad; 400–480 squash; 480–800 spring 10/220; 800–1500 morph; 1500–1900 wordmark ease-out quint
- **الدليل / proof:** `kosif-tool/playbooks/shapes.md:35-43`

#### BRAND-211 · استخراج الهوية من CSS · Brand identity extraction from CSS · 📄 موصوف
- **ماذا / what:** Pull exact bg/accent/text hexes and display/body fonts from :root vars so video matches site.
- **كيف / how:** Parse styles.css custom properties; record in plan Visual identity block.
- **الدليل / proof:** `kosif-one/vendor/brag/skills/brag/references/step-1-inspect.md`

#### BRAND-212 · تشويه الشعار بالأثر · Trail displacement on logos/type · 💡 فكرة
- **ماذا / what:** Apply the smear displacement to a logo SDF, photo or rendered Arabic text texture for a liquid reveal.
- **كيف / how:** Replace blob with texture2D(textTex,fuv).
- **الدليل / proof:** `kosif-atlas/skills/100-ui-motion/211-thermal-finger-trail/SKILL.md`

#### BRAND-213 · رسم الشعار وتوهج · SVG logo draw + radial bloom fill · 💡 فكرة
- **ماذا / what:** Logo paths stroke-draw then fill blooms with radial glow; URL types and holds.
- **كيف / how:** stroke-dashoffset; radial gradient fade.
- **أرقام / params:** draw 700 ms; URL hold 1.2 s
- **الدليل / proof:** `style:pm-aschapmann-131210`

#### BRAND-214 · نبضتان للزر · Double CTA pulse · 💡 فكرة
- **ماذا / what:** CTA pulses twice before end freeze.
- **كيف / how:** scale keyframes.
- **أرقام / params:** 2 pulses
- **الدليل / proof:** `style:pm-cansincengiz-me-cf68dd`

#### BRAND-215 · تصاعد لون العلامة · Brand colour flood progression · 💡 فكرة
- **ماذا / what:** Brand colour grows from a 4px line to full-frame fill at the end.
- **أرقام / params:** 4 px line -> pills -> 100% last 2 s
- **الدليل / proof:** `style:pm-ratheejaisal-1f4538`

#### BRAND-216 · تجميع الشعار بنابض · Spring wordmark assembly · 💡 فكرة
- **ماذا / what:** spring stiffness 160 damping 15; 60 ms stagger
- **أرقام / params:** wide geometric 140 px; mono metrics 32 px
- **الدليل / proof:** `style:pm-robvjourney-ce3e1a`
