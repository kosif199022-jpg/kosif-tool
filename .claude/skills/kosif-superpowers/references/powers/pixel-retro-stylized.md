# البكسل والريترو والأساليب الخاصة — Pixel, retro & stylised

> فصل مُجمَّع آليًا من 92 ملاحظة حصاد (مستودعات KOSIF + أطلس المهارات + 253 فيديو مرجعي)، مدموجة إلى **92 قدرة** مرتبة من الأقوى دليلًا. لم يُحرَّر يدويًا بعد — تحقّق من الدليل قبل الادعاء.
> Auto-compiled chapter: 92 powers deduplicated by name from 92 harvested atoms; strongest evidence first.

**الحالة:** ✅ مُثبت هنا 5 · 🟢 جاهز 7 · 📦 بأمر تثبيت 41 · 👁 شوهد في فيديو 20 · 📄 موصوف 16 · 💡 فكرة 3

#### RETRO-01 · سبرايت بكسل بلوحة ألوان مقفلة · Palette-locked pixel sprite spec · ✅ مُثبت هنا
- **ماذا / what:** Author small sprites as character grids mapped to a fixed palette; larger ones via a procedural Python generator.
- **كيف / how:** Pillow: rows of palette keys -> PNG at 1x, upscale nearest-neighbor x8 for preview; hand grids up to ~24x24. Rules: silhouette first, one light direction, hue-shifted ramps, selective outline, no pillow shading, no dithering on small sprites.
- **أرقام / params:** scale 8 preview; <=24x24 hand grid
- **الدليل / proof:** `kosif-atlas/skills/2460-pixel-art/9527-sprite`

#### RETRO-02 · ثيم J وحشي حمضي · Kinetic theme J Brutalist Acid · ✅ مُثبت هنا
- **ماذا / what:** Locked kinetic-typography look for Flow prompts: flat black ultra-condensed heavy sans.
- **كيف / how:** kinetic-flow setup {"theme":"J"} -> STYLE LOCK paragraph repeated verbatim in every clip prompt (background, hero type colour, small type colour, finish, overlay, animation, transition, end card).
- **أرقام / params:** background #BDBDB8, accent/hero #C6FF00, small #0A0A0A; flat black ultra-condensed heavy sans; industrial chrome + black rubber; concrete grain, harsh top light, blank tape tabs, grid; hard snapping acid highlight punch; glitch cut + whip-slide; acid-lime box slams under wordmark
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/kinetic-flow.mjs:13`

#### RETRO-03 · ثيم K ريترو السبعينات الدافئ · Kinetic theme K Retro 70s Warm · ✅ مُثبت هنا
- **ماذا / what:** Locked kinetic-typography look for Flow prompts: rounded heavy warm-brown retro serif.
- **كيف / how:** kinetic-flow setup {"theme":"K"} -> STYLE LOCK paragraph repeated verbatim in every clip prompt (background, hero type colour, small type colour, finish, overlay, animation, transition, end card).
- **أرقام / params:** background #F3E3C3, accent/hero #E8732C, small #5A3A22; rounded heavy warm-brown retro serif; matte faded analog objects; film grain, warm vignette, orange/mustard sunburst corner; wobbly 70s bounce-in; sunburst stripe wipe; sunburst rotating behind brand
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/kinetic-flow.mjs:14`

#### RETRO-04 · ثيم N قص ورقي · Kinetic theme N Paper Craft Cutout · ✅ مُثبت هنا
- **ماذا / what:** Locked kinetic-typography look for Flow prompts: flat black thick sans with tiny cut-paper shadow.
- **كيف / how:** kinetic-flow setup {"theme":"N"} -> STYLE LOCK paragraph repeated verbatim in every clip prompt (background, hero type colour, small type colour, finish, overlay, animation, transition, end card).
- **أرقام / params:** background #F2EBDD, accent/hero #D94032, small #1A1A1A; flat black thick sans with tiny cut-paper shadow; layered cardstock + paper fibres; torn-paper corners, kraft texture, shadows; stepped stop-motion cutout slides; physical paper sheet slide; paper folds reveal brand
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/kinetic-flow.mjs:17`

#### RETRO-05 · ثيم Q كروم Y2K القزحي · Kinetic theme Q Y2K Chrome Iridescent · ✅ مُثبت هنا
- **ماذا / what:** Locked kinetic-typography look for Flow prompts: black wide heavy sans with subtle iridescent outline.
- **كيف / how:** kinetic-flow setup {"theme":"Q"} -> STYLE LOCK paragraph repeated verbatim in every clip prompt (background, hero type colour, small type colour, finish, overlay, animation, transition, end card).
- **أرقام / params:** background #E9ECF2, accent/hero #141414, small #5A5F6E; black wide heavy sans with subtle iridescent outline; liquid chrome with iridescent reflections; pale lilac gradient, chrome droplets, star sparkles; shimmer sweep with snap stretch; liquid silver morph wipe; chrome blob uncovers wordmark
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/kinetic-flow.mjs:20`

#### RETRO-06 · دورات حركة بكسلية برمجية · Procedural sprite cycles · 🟢 جاهز
- **ماذا / what:** One draw(direction, pose) generator produces every frame from parameters (limb angles, step phase, bob, arm swing, squash) so fixes propagate to all frames.
- **كيف / how:** Plan cycles in a table (key poses, frame counts, durations); RPG Maker MZ walk = 3 patterns 0-1-2-1 at 48x48; mirror only symmetric designs then shade; GIF delays in 10ms units floor 20ms; VFX fade by stepping down a palette ramp; hold impact frames.
- **أرقام / params:** MZ 48x48; GIF min 20ms
- **الدليل / proof:** `kosif-atlas/skills/2460-pixel-art/9525-animate/SKILL.md` · `kosif-atlas/skills/2460-pixel-art/9530-vfx/SKILL.md`

#### RETRO-07 · تأثير بكسلة · Pixelation post shader · 🟢 جاهز
- **ماذا / what:** Snap UVs to a cell grid; cellUV=fract(uv/size) allows per-cell patterns.
- **كيف / how:** uvPixel=size*floor(uv/size). Animate size for progressive depixelation (powers of 2).
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### RETRO-08 · هاف تون / طباعة نقطية · Halftone & CMYK halftone · 🟢 جاهز
- **ماذا / what:** Dots sized by luma; four rotated CMYK grids multiplied for print look.
- **كيف / how:** luma=dot(rgb,(0.2126,0.7152,0.0722)); r=R*(0.1+luma); smoothstep with fwidth AA; 3x3 neighbor sampling; gooey via smooth-min.
- **أرقام / params:** angles C15 M75 Y0 K45
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### RETRO-09 · مظاهر ASCII وLED وليغو · ASCII / threshold-matrix / LED / Lego / crochet looks · 🟢 جاهز
- **ماذا / what:** Family of post looks from per-cell shaping: ASCII glyph atlas by luma, 8x8 threshold matrices, staggered LED panels, Lego studs, woven crochet, fluted glass.
- **كيف / how:** Pixelate then shape each cell by luma/SDF; ASCII uses canvas texture of chars indexed by luma.
- **أرقام / params:** 8x8 matrices
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### RETRO-10 · مظهر القص بإيقاف الحركة · Stepped stop-motion cutout look · 🟢 جاهز
- **ماذا / what:** Stepped, snappy cut-paper motion used by theme N and the vox collage profile (pop/drop/slide with short settle, no slow CGI drift).
- **كيف / how:** Request in prompts; in Canvas could be emulated by quantising t to 12 fps steps (not implemented).
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/kinetic-flow.mjs:17` · `fastify-motion-bro/scripts/profiles/vox-history.mjs:11,50`

#### RETRO-11 · جليتش رقمي · Digital glitch stutter (2D) · 🟢 جاهز
- **ماذا / what:** Short seeded RGB-split and slice displacement that returns to clean.
- **كيف / how:** MOTION.glitch(tl, el, at, {dur, amp, seed}).
- **أرقام / params:** <=0.4 s (default 0.3 s), 30 steps/s, amp 10 px, red rgba(255,0,80,.7) / cyan rgba(0,200,255,.7) drop shadows, random inset slices
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:548`

#### RETRO-12 · تشويش مرتبط بتحليل الصوت · Analysis-keyed glitch pass (3D) · 🟢 جاهز
- **ماذا / what:** One post pass with chroma split, slice displacement, a negative tear, freeze monochrome and tape-speed warp, hashed per frame.
- **كيف / how:** makeGlitchPass(); glitch.set({chroma, slice, negative, mono, warp, frame}).
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/kit/three-kit.js:916`

#### RETRO-13 · أنماط المعالجة اللاحقة · Post-processing patterns · 📦 بأمر تثبيت
- **ماذا / what:** Screen-space looks built from pixelation cells: luma-sized halftone dots, SDF patterns, crochet/woven, fluted glass, moire, chromatic dispersion, refraction, fresnel.
- **كيف / how:** Cell UV from floor(uv/size); radius = uRadius*(0.1+luma) with luma weights 0.2126/0.7152/0.0722; smoothstep AA; chromatic aberration shift ~0.002; neighbor sampling to break the grid; backside-render trick for glass dispersion.
- **أرقام / params:** CA 0.002; luma 0.2126/0.7152/0.0722
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### RETRO-14 · معالجة نقطية ونمط الطباعة · Halftone / CMYK / pixel post-processing · 📦 بأمر تثبيت
- **ماذا / what:** Turn a scene into halftone dots, rotated CMYK screens, LED/Lego cells or ASCII by pixelating UVs and shaping each cell by luminance.
- **كيف / how:** Fragment shader: uvPixel = size*floor(uv/size); cellUV = fract(uv/size); dot radius from luma (0.2126,0.7152,0.0722); fwidth antialiasing; CMYK angles C15 M75 Y0 K45.
- **أرقام / params:** luma weights 0.2126/0.7152/0.0722; CMYK screen angles 15/75/0/45 deg
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion` · `kosif-atlas/skills/97-frontend-design-director/206-frontend-design-director/examples/webgl/halftone.frag`

#### RETRO-15 · مؤثرات بكسل بسلم ألوان · Palette-stepped pixel VFX sheets · 📦 بأمر تثبيت
- **ماذا / what:** Sparks, slashes, explosions as sprite-sheets that fade by stepping down a palette ramp, not alpha; hold the impact frame.
- **كيف / how:** Python stdlib renderer from a spec; timing table first; GIF delays ≥20ms in hundredths.
- **أرقام / params:** 2-4 review rounds
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2460-pixel-art/9530-vfx/SKILL.md`

#### RETRO-16 · مشهد بكسل متحرك في ملف HTML واحد · Self-contained pixel cutscene in HTML · 📦 بأمر تثبيت
- **ماذا / what:** Canvas 2D scene with fixed logical resolution, 60Hz step, sprite cadence 8-12fps, parallax, typed dialogue, optional embedded WAV.
- **كيف / how:** Single HTML, no libs; expose window seek(t)/frameDataURL/duration for frame capture; render to MP4 by stepping seek and piping PNGs to ffmpeg.
- **أرقام / params:** 160x144, 240x160, 320x180; integer upscale
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2460-pixel-art/9526-scene`

#### RETRO-17 · بكسلة وأنماط داخل الخلية · Pixelation and cell-local patterns · 📦 بأمر تثبيت
- **ماذا / what:** Snap UVs to a grid then shape each cell (bars, SDF dots, threshold matrices) for LED, receipt, Lego, crochet looks.
- **كيف / how:** GLSL: uvPixel = size*floor(uv/size); cellUV = fract(uv/size). Ideas also doable in canvas/ffmpeg.
- **أرقام / params:** 8x8 threshold matrices
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion`

#### RETRO-18 · مؤثر وسائط: Tape Damage · Media effect: Tape Damage · 📦 بأمر تثبيت
- **ماذا / what:** Non-destructive image/video treatment from the Tape Damage family.
- **كيف / how:** Studio or `hyperframes media-treatment --selector <css> --apply`; writes data attributes, source untouched.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/guides/media-effects.mdx`

#### RETRO-19 · مؤثر وسائط: Film Artifacts · Media effect: Film Artifacts · 📦 بأمر تثبيت
- **ماذا / what:** Non-destructive image/video treatment from the Film Artifacts family.
- **كيف / how:** Studio or `hyperframes media-treatment --selector <css> --apply`; writes data attributes, source untouched.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/guides/media-effects.mdx`

#### RETRO-20 · مؤثر وسائط: Scanlines · Media effect: Scanlines · 📦 بأمر تثبيت
- **ماذا / what:** Non-destructive image/video treatment from the Scanlines family.
- **كيف / how:** Studio or `hyperframes media-treatment --selector <css> --apply`; writes data attributes, source untouched.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/guides/media-effects.mdx`

#### RETRO-21 · مؤثر وسائط: CRT Curvature · Media effect: CRT Curvature · 📦 بأمر تثبيت
- **ماذا / what:** Non-destructive image/video treatment from the CRT Curvature family.
- **كيف / how:** Studio or `hyperframes media-treatment --selector <css> --apply`; writes data attributes, source untouched.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/guides/media-effects.mdx`

#### RETRO-22 · مؤثر وسائط: Channel Separation · Media effect: Channel Separation · 📦 بأمر تثبيت
- **ماذا / what:** Non-destructive image/video treatment from the Channel Separation family.
- **كيف / how:** Studio or `hyperframes media-treatment --selector <css> --apply`; writes data attributes, source untouched.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/guides/media-effects.mdx`

#### RETRO-23 · مؤثر وسائط: Digital Glitch · Media effect: Digital Glitch · 📦 بأمر تثبيت
- **ماذا / what:** Non-destructive image/video treatment from the Digital Glitch family.
- **كيف / how:** Studio or `hyperframes media-treatment --selector <css> --apply`; writes data attributes, source untouched.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/guides/media-effects.mdx`

#### RETRO-24 · مؤثر وسائط: Chroma Softening · Media effect: Chroma Softening · 📦 بأمر تثبيت
- **ماذا / what:** Non-destructive image/video treatment from the Chroma Softening family.
- **كيف / how:** Studio or `hyperframes media-treatment --selector <css> --apply`; writes data attributes, source untouched.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/guides/media-effects.mdx`

#### RETRO-25 · مؤثر وسائط: Halftone · Media effect: Halftone · 📦 بأمر تثبيت
- **ماذا / what:** Non-destructive image/video treatment from the Halftone family.
- **كيف / how:** Studio or `hyperframes media-treatment --selector <css> --apply`; writes data attributes, source untouched.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/guides/media-effects.mdx`

#### RETRO-26 · مؤثر وسائط: Two-Ink Print · Media effect: Two-Ink Print · 📦 بأمر تثبيت
- **ماذا / what:** Non-destructive image/video treatment from the Two-Ink Print family.
- **كيف / how:** Studio or `hyperframes media-treatment --selector <css> --apply`; writes data attributes, source untouched.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/guides/media-effects.mdx`

#### RETRO-27 · مؤثر وسائط: Ordered Dither · Media effect: Ordered Dither · 📦 بأمر تثبيت
- **ماذا / what:** Non-destructive image/video treatment from the Ordered Dither family.
- **كيف / how:** Studio or `hyperframes media-treatment --selector <css> --apply`; writes data attributes, source untouched.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/guides/media-effects.mdx`

#### RETRO-28 · مؤثر وسائط: Mono Screen · Media effect: Mono Screen · 📦 بأمر تثبيت
- **ماذا / what:** Non-destructive image/video treatment from the Mono Screen family.
- **كيف / how:** Studio or `hyperframes media-treatment --selector <css> --apply`; writes data attributes, source untouched.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/guides/media-effects.mdx`

#### RETRO-29 · مؤثر وسائط: ASCII (8 styles) · Media effect: ASCII (8 styles) · 📦 بأمر تثبيت
- **ماذا / what:** Non-destructive image/video treatment from the ASCII (8 styles) family.
- **كيف / how:** Studio or `hyperframes media-treatment --selector <css> --apply`; writes data attributes, source untouched.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/guides/media-effects.mdx`

#### RETRO-30 · مؤثر وسائط: Engraving · Media effect: Engraving · 📦 بأمر تثبيت
- **ماذا / what:** Non-destructive image/video treatment from the Engraving family.
- **كيف / how:** Studio or `hyperframes media-treatment --selector <css> --apply`; writes data attributes, source untouched.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/guides/media-effects.mdx`

#### RETRO-31 · مؤثر وسائط: Crosshatch · Media effect: Crosshatch · 📦 بأمر تثبيت
- **ماذا / what:** Non-destructive image/video treatment from the Crosshatch family.
- **كيف / how:** Studio or `hyperframes media-treatment --selector <css> --apply`; writes data attributes, source untouched.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/guides/media-effects.mdx`

#### RETRO-32 · مؤثر وسائط: Kuwahara Paint · Media effect: Kuwahara Paint · 📦 بأمر تثبيت
- **ماذا / what:** Non-destructive image/video treatment from the Kuwahara Paint family.
- **كيف / how:** Studio or `hyperframes media-treatment --selector <css> --apply`; writes data attributes, source untouched.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/guides/media-effects.mdx`

#### RETRO-33 · تحويل المشهد إلى أسكي · ASCII Render Pass · 📦 بأمر تثبيت
- **ماذا / what:** A slotted scene is rasterised once, its luminance grid is sampled and redrawn as ASCII glyphs from a density ramp; resolution steps coarse to fine until legible.
- **كيف / how:** Install with `npx hyperframes add ascii-render-pass` (copies to compositions/components/ascii-render-pass.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chr…
- **أرقام / params:** charset " .:-=+*#%@"; grid coarse|med|fine; resolve_at 1.4 s; vars: charset= .:-=+*#%@; grid=med[coarse|med|fine]; resolve_at=1.4(0.6..10); accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add ascii-render-pass` (copies to compositions/components/ascii-render-pass`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/ascii-render-pass/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/ascii-render-pass/ascii-render-pass.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/ascii-render-pass.mdx`

#### RETRO-34 · كشف بأثر أسكي · ASCII Trail Reveal · 📦 بأمر تثبيت
- **ماذا / what:** A fixed S-curve sweeps through a seeded ASCII grid, flipping cells away to uncover a labelled panel.
- **كيف / how:** Install with `npx hyperframes add ascii-trail-reveal` (copies to compositions/components/ascii-trail-reveal.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless C…
- **أرقام / params:** trail_width narrow|wide; vars: label=The reveal; accent=green[green|blue|violet]; trail_width=narrow[narrow|wide]
- **تثبيت / install:** `npx hyperframes add ascii-trail-reveal` (copies to compositions/components/ascii-trail-reveal`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/ascii-trail-reveal/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/ascii-trail-reveal/ascii-trail-reveal.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/ascii-trail-reveal.mdx`

#### RETRO-35 · تنقيط باير · Ordered Dither Pass · 📦 بأمر تثبيت
- **ماذا / what:** Bayer-matrix ordered dithering of a slotted scene: emerges from 2-tone noise to clean or dissolves back; stateless per frame.
- **كيف / how:** Install with `npx hyperframes add ordered-dither-pass` (copies to compositions/components/ordered-dither-pass.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless…
- **أرقام / params:** matrix 2|4|8; levels 2; direction in|out; vars: matrix=4[2|4|8]; direction=in[in|out]; levels=2(2..6); accent=green[green|blue|violet]; exit=none[none|fade|up]
- **تثبيت / install:** `npx hyperframes add ordered-dither-pass` (copies to compositions/components/ordered-dither-pass`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/ordered-dither-pass/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/ordered-dither-pass/ordered-dither-pass.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/ordered-dither-pass.mdx`

#### RETRO-36 · نص غليتش · RGB Glitch Text · 📦 بأمر تثبيت
- **ماذا / what:** RGB-offset copies of text jitter during a short glitch window.
- **كيف / how:** Install with `npx hyperframes add rgb-glitch-text` (copies to compositions/components/rgb-glitch-text.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromiu…
- **أرقام / params:** intensity subtle|standard|extreme; vars: text=GLITCH; intensity=standard[subtle|standard|extreme]; tone=ink[ink|paper|accent]
- **تثبيت / install:** `npx hyperframes add rgb-glitch-text` (copies to compositions/components/rgb-glitch-text`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/rgb-glitch-text/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/rgb-glitch-text/rgb-glitch-text.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/rgb-glitch-text.mdx`

#### RETRO-37 · شريط المسح · Scan Band · 📦 بأمر تثبيت
- **ماذا / what:** Diagonal distortion band sweeps a wordmark once, showing red/cyan split only inside the band.
- **كيف / how:** Install with `npx hyperframes add scan-band` (copies to compositions/components/scan-band.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium frame capt…
- **أرقام / params:** band_angle 12 deg; vars: wordmark=HYPERFRAMES; band_angle=12(-30..30)
- **تثبيت / install:** `npx hyperframes add scan-band` (copies to compositions/components/scan-band`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/scan-band/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/scan-band/scan-band.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/scan-band.mdx`

#### RETRO-38 · شاشة فيزيائية · On-Screen Display Effect · 📦 بأمر تثبيت
- **ماذا / what:** Grid, scanline, vignette and sheen overlay plus 3D-warp wrapper so footage reads as playing on a real display.
- **كيف / how:** Install with `npx hyperframes add yt-screen-warp` (copies to compositions/components/yt-screen-warp.html); mount on a `class="clip"` div via data-composition-src + data-start/data-duration/data-track-index and pass overrides as JSON in data-variable-values; colours/fonts come from the 18 theme tokens (accent enum green=--brand, blue=--accent, violet=--accent-2); extra duration becomes hold, never time-stretch; preview `npx hyperframes preview`, render `npx hyperframes render` (headless Chromium …
- **تثبيت / install:** `npx hyperframes add yt-screen-warp` (copies to compositions/components/yt-screen-warp`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/yt-screen-warp/registry-item.json` · `kosif-one/vendor/hyperframes/registry/components/yt-screen-warp/yt-screen-warp.html` · `kosif-one/vendor/hyperframes/docs/catalog/components/yt-screen-warp.mdx`

#### RETRO-39 · واجهة الكاميرا المنزلية · Camcorder HUD · 📦 بأمر تثبيت
- **ماذا / what:** Responsive REC dot, battery, editable date and timeline-driven counter overlay for camcorder looks.
- **كيف / how:** Install with `npx hyperframes add camcorder-hud` (copies the full composition to compositions/camcorder-hud.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 4 s overlay; 1920x1080; duration 4 s
- **تثبيت / install:** `npx hyperframes add camcorder-hud` (copies the full composition to compositions/camcorder-hud`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/camcorder-hud/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/camcorder-hud/camcorder-hud.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/camcorder-hud.mdx`

#### RETRO-40 · حقل الهافتون · Halftone Field · 📦 بأمر تثبيت
- **ماذا / what:** Full-bleed halftone LED-wall field: dot size and colour follow a slow simplex-noise flow.
- **كيف / how:** Install with `npx hyperframes add halftone-field` (copies the full composition to compositions/halftone-field.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: WebGL fragment shader, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** cellSize 54; frequency 2; speed 5; gamma 12; palette #00AAFF #C2FF67 #6600FF #000000; vars: frequency=2(1..10); speed=5(0..10); cellSize=54(1..100); gamma=12(1..20); paletteBias=2(0..20); palette1=#00AAFF; palette2=#C2FF67; palette3=#6600FF; palette4=#000000; background=#000000; quantize=False; 1920…
- **تثبيت / install:** `npx hyperframes add halftone-field` (copies the full composition to compositions/halftone-field`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/halftone-field/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/halftone-field/halftone-field.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/halftone-field.mdx`

#### RETRO-41 · راسم الإشارة · Oscilloscope Trace · 📦 بأمر تثبيت
- **ماذا / what:** CRT oscilloscope beam sweeps a waveform across a 10x8 graticule with closed-form phosphor persistence exp(-age/tau), brighter where the beam slows.
- **كيف / how:** Install with `npx hyperframes add oscilloscope-trace` (copies the full composition to compositions/oscilloscope-trace.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: Canvas 2D painter, GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** waveform sine|square|triangle|data; frequency 12; amplitude 3; persistenceMs 100; phosphorColor #5dff8f; sweepRate 5; vars: waveform=sine[sine|square|triangle|data]; frequency=12(0.1..200); amplitude=3(0.1..4); persistenceMs=100(1..1000); phosphorColor=#5dff8f; sweepRate=5(0.25..60); dataSeries=; 19…
- **تثبيت / install:** `npx hyperframes add oscilloscope-trace` (copies the full composition to compositions/oscilloscope-trace`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/oscilloscope-trace/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/oscilloscope-trace/oscilloscope-trace.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/oscilloscope-trace.mdx`

#### RETRO-42 · لوحة LCD · Scanline Board Background · 📦 بأمر تثبيت
- **ماذا / what:** Textured paper board with drifting scanlines, optional pixel grid, static grain, and blur-focus title with chromatic fringe.
- **كيف / how:** Install with `npx hyperframes add yt-lcd-background` (copies the full composition to compositions/yt-lcd-background.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 10 s; 1920x1080; duration 10 s
- **تثبيت / install:** `npx hyperframes add yt-lcd-background` (copies the full composition to compositions/yt-lcd-background`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/yt-lcd-background/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/yt-lcd-background/yt-lcd-background.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/yt-lcd-background.mdx`

#### RETRO-43 · تنقيط انتشار الخطأ الدقيق · Exact error-diffusion dither (offline) · 📦 بأمر تثبيت
- **ماذا / what:** Sequential Floyd-Steinberg, Atkinson, Jarvis-Judice-Ninke, Stucki, Burkes and Sierra dithers with a custom palette and point size on images/video.
- **كيف / how:** node <skill>/scripts/dither.mjs --input src.mp4 --out src.atkinson.mp4 --algorithm atkinson --palette '#0f380f,#306230,#8bac0f,#9bbc0f' --point-size 3.
- **أرقام / params:** Game Boy palette example #0f380f #306230 #8bac0f #9bbc0f
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/media-use/scripts/dither.mjs` · `kosif-one/vendor/hyperframes/skills/media-use/scripts/dither.test.mjs` · `kosif-one/vendor/hyperframes/skills/media-use/scripts/lib/error-diffusion.mjs`

#### RETRO-44 · حركة إيقاعية: chromatic-split · Beat motion primitive: chromatic-split · 📦 بأمر تثبيت
- **ماذا / what:** RGB channel split on a word, anchored to music events (snare / glitch / surge).
- **كيف / how:** Read music-to-video/references/motion-primitive-catalog.md and copy references/motion-primitives/chromatic-split/scene.html (runnable with vendored gsap); anchor to audiomap events.
- **أرقام / params:** anchor: snare / glitch / surge; best span 0.1-0.6 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/chromatic-split/scene.html` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitive-catalog.md`

#### RETRO-45 · حركة إيقاعية: binary-decrypt · Beat motion primitive: binary-decrypt · 📦 بأمر تثبيت
- **ماذا / what:** Scramble -> decode text, anchored to music events (roll / build).
- **كيف / how:** Read music-to-video/references/motion-primitive-catalog.md and copy references/motion-primitives/binary-decrypt/scene.html (runnable with vendored gsap); anchor to audiomap events.
- **أرقام / params:** anchor: roll / build; best span 0.8-2.5 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/binary-decrypt/scene.html` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitive-catalog.md`

#### RETRO-46 · حركة إيقاعية: pixel-dissolve · Beat motion primitive: pixel-dissolve · 📦 بأمر تثبيت
- **ماذا / what:** Pixelated dissolve, anchored to music events (transition / hard_stop).
- **كيف / how:** Read music-to-video/references/motion-primitive-catalog.md and copy references/motion-primitives/pixel-dissolve/scene.html (runnable with vendored gsap); anchor to audiomap events.
- **أرقام / params:** anchor: transition / hard_stop; best span 0.5-1.5 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/pixel-dissolve/scene.html` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitive-catalog.md`

#### RETRO-47 · حركة إيقاعية: datamosh-smear · Beat motion primitive: datamosh-smear · 📦 بأمر تثبيت
- **ماذا / what:** Datamosh motion smear, anchored to music events (glitch / transition).
- **كيف / how:** Read music-to-video/references/motion-primitive-catalog.md and copy references/motion-primitives/datamosh-smear/scene.html (runnable with vendored gsap); anchor to audiomap events.
- **أرقام / params:** anchor: glitch / transition; best span 0.4-1.2 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitives/datamosh-smear/scene.html` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitive-catalog.md`

#### RETRO-48 · الجلتش · glitch · 📦 بأمر تثبيت
- **ماذا / what:** Digital stutter accent.
- **كيف / how:** motion-kit.js window.MOTION inside a flat project; kmotion sync PROJECT after kit edits
- **أرقام / params:** ≤0.4 s; MOTION.glitch
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md:95` · `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md` · `100-superskills/skills/kosif-montage-motion/references/hyperframes-authoring.md`

#### RETRO-49 · تشويش رقمي · DOM glitch stutter · 📦 بأمر تثبيت
- **ماذا / what:** RGB-split drop-shadows plus random clip slices, seeded, returning to clean.
- **كيف / how:** MOTION.glitch(tl, el, at, {dur, amp, seed}).
- **أرقام / params:** ≤ .3 s, 30 steps/s, amp 10 px, magenta rgba(255,0,80,.7) / cyan rgba(0,200,255,.7)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:548`

#### RETRO-50 · مرشح التشويش · Analysis-keyed glitch pass · 📦 بأمر تثبيت
- **ماذا / what:** One shader pass with chroma split, band slice displacement, negative tear, cold-silver freeze monochrome and tape warp.
- **كيف / how:** const g = K3.makeGlitchPass(); composer.addPass(g); g.userData.set({chroma, slice, negative, mono, warp, frame}).
- **أرقام / params:** 24 bands, slice shift ±0.06 on ~28% bands, chroma 1.2% offset, warp .01; rule: negative only a few frames, mono = 'time stopped'
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:916` · `kosif-studio/motion/references/hyperframes-authoring.md`

#### RETRO-51 · تحويل الصورة إلى ملصق متجه بعدد ألوان · Photo poster vectorisation (k colours) · 📦 بأمر تثبيت
- **ماذا / what:** Photos are smoothed with an edge-preserving filter and grouped into k Lab colours, giving a flat-paint poster that scales without limit.
- **كيف / how:** vectorize.trace(path, colors=k) or auto when looks_like_photo; _photo_memberships uses bilateralFilter + cv2.kmeans KMEANS_PP.
- **أرقام / params:** k = 24 default; up 4 (>260 px) or 6; simplify 1.1; min_area 2.5; sharpen 0.4
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/vectorize.py:164` · `kosif-studio/vectorize.py:188` · `kosif-studio/scenes/1612747e-9555-4848-9125-39f7ef17c88e.json`

#### RETRO-52 · ريترو · Style: Retrowave (retrowave) · 📦 بأمر تثبيت
- **ماذا / what:** 80s synthwave: neon grid floor, sunset gradient, chrome text.
- **كيف / how:** Three.js or 2.5D perspective grid scrolling toward camera; gradient sun with scanline bands; bloom-like glow via layered blur. Scaffold: python3 tools/kosif.py scaffold retrowave <dir>.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `style:retrowave` · `kosif-tool/playbooks/ads.md`

#### RETRO-53 · بيكسل آرت · Style: Pixel art (pixel-art) · 📦 بأمر تثبيت
- **ماذا / what:** Sprite-based low-res pixel characters and worlds.
- **كيف / how:** Canvas at low internal res, imageSmoothingEnabled=false, integer upscale; sprite frames on twos. Scaffold: python3 tools/kosif.py scaffold pixel-art <dir>.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `style:pixel-art` · `kosif-tool/playbooks/characters.md`

#### RETRO-54 · مشهد بكسل مع انعكاس مائي · Pixel diorama with water reflection · 👁 شوهد في فيديو
- **ماذا / what:** Render scene to low-res canvas (~480x270), mirror the upper half into the lake with darker tint and per-row horizontal sine offset, upscale x4 with imageSmoothingEnabled=false
- **أرقام / params:** ripple amplitude 1-2 px, row phase speed 2 rad/s
- **الدليل / proof:** `style:pm-0xevinho-3777d8`

#### RETRO-55 · رسم شخصيات بكسل بالكود · Pixel sprite in code · 👁 شوهد في فيديو
- **ماذا / what:** draw sprites from char grids on canvas, imageSmoothing off
- **أرقام / params:** 16x16 scaled x3
- **الدليل / proof:** `style:pm-aisongman-71ffac`

#### RETRO-56 · خطوط سرعة شعاعية · Radial speed lines · 👁 شوهد في فيديو
- **ماذا / what:** random radial strokes flickering per frame
- **الدليل / proof:** `style:pm-allforbigfire-86ff3c`

#### RETRO-57 · تحوّل التميمة بين حالات رسم · Mascot render-state morph · 👁 شوهد في فيديو
- **ماذا / what:** swap the same silhouette between solid fill, ordered-dither halftone, and dashed outline wireframe with 3D guide ellipses; fill with dither rising from bottom
- **أرقام / params:** dither cell 6px, dash 8/6
- **الدليل / proof:** `style:pm-anthonyriera-9b1b2a`

#### RETRO-58 · خطوط أوب آرت متحدة المركز · Op-art concentric moiré · 👁 شوهد في فيديو
- **ماذا / what:** Concentric stripes from two centres or radial sinusoid threshold, animate phase for vibrating moiré
- **أرقام / params:** stripe 12px, red/cream/black
- **الدليل / proof:** `style:pm-ayushunleashed-ece3e3`

#### RETRO-59 · واجهة لعبة 8-بت مع صندوق حوار · 8-bit platformer HUD + dialogue · 👁 شوهد في فيديو
- **ماذا / what:** pixel font HUD (LEVEL/coins/TIME), pixel parallax hills, bordered dialogue box with typewriter caption
- **أرقام / params:** pixel scale 4x, typewriter 30 ms/char
- **الدليل / proof:** `style:pm-emollick-8661a8`

#### RETRO-60 · شريط إعلان تلفزيوني قديم · Infomercial lower third · 👁 شوهد في فيديو
- **ماذا / what:** purple sunburst, CRT TV prop, yellow slanted 'CALL NOW!' block + phone number bar, VHS PLAY/clock OSD, tracking noise lines
- **أرقام / params:** VHS noise 2-3 lines, scanlines 2px
- **الدليل / proof:** `style:pm-emollick-8661a8`

#### RETRO-61 · كلمة بتأثير الجلتش وفصل الألوان · RGB-split glitch word · 👁 شوهد في فيديو
- **ماذا / what:** render word 3x in red/cyan/white with random x offsets, slice into horizontal strips shifting randomly, flash coloured bars, retrigger on 1/8 notes
- **أرقام / params:** offset 4-12 px, 6-10 slices, retrigger 234 ms
- **الدليل / proof:** `style:pm-ghinaiya-nirmal-5d8fec`

#### RETRO-62 · مشهد بكسل مكبّر · Pixel scene upscale · 👁 شوهد في فيديو
- **ماذا / what:** Draw at 320x180 then scale 6x imageSmoothing off
- **الدليل / proof:** `style:pm-hoyoyoda-3a5c08`

#### RETRO-63 · بطاقة عنوان اللعبة · Game title card · 👁 شوهد في فيديو
- **ماذا / what:** dark translucent panel with blocky uppercase title, dismiss on start
- **الدليل / proof:** `style:pm-ivanfioravanti-bd9261`

#### RETRO-64 · شعار ASCII · ASCII logo · 👁 شوهد في فيديو
- **ماذا / what:** sample logo mask, render chars on grid
- **الدليل / proof:** `style:pm-jacksonfall-54b2ac`

#### RETRO-65 · مسرح غروب بكسلي · Pixel sunset stage · 👁 شوهد في فيديو
- **ماذا / what:** low-res canvas 320x180 upscaled nearest, striped sun, reflection lines
- **الدليل / proof:** `style:pm-pluginplay-3d4006`

#### RETRO-66 · لافتة بكسل · Pixel caption box · 👁 شوهد في فيديو
- **ماذا / what:** yellow box, black border, year tag, pop 1 frame
- **الدليل / proof:** `style:pm-pluginplay-3d4006`

#### RETRO-67 · تحويل صورة إلى ASCII · ASCII art render · 👁 شوهد في فيديو
- **ماذا / what:** Sample luminance grid, map to char ramp ' .:-=+*#%@', colour per cell
- **أرقام / params:** 120 cols
- **الدليل / proof:** `style:pm-rames-jusso-589f80`

#### RETRO-68 · كشف أرقام بشبكة بكسل · Pixel grid digit reveal · 👁 شوهد في فيديو
- **ماذا / what:** grid 30px cells; cells inside glyph mask flip to accent with radial stagger
- **الدليل / proof:** `style:pm-raphaelaubryy-4b137e`

#### RETRO-69 · عنوان نيون ريترو · Synthwave neon title · 👁 شوهد في فيديو
- **ماذا / what:** striped sun, perspective grid, neon stroke glow
- **الدليل / proof:** `style:pm-rendesr-86be44`

#### RETRO-70 · إزاحة سوء التسجيل · Misregistration offset · 👁 شوهد في فيديو
- **ماذا / what:** duplicate layer in second ink offset 4px, multiply
- **أرقام / params:** 4-6px
- **الدليل / proof:** `style:pm-rneayan-474bcf`

#### RETRO-71 · أيقونة بكسلية تتجمّع · Pixel icon assemble · 👁 شوهد في فيديو
- **ماذا / what:** Hand icon built from squares appearing randomly, top squares float/ flicker
- **الدليل / proof:** `style:pm-robvjourney-ce3e1a`

#### RETRO-72 · عالم مانغا بخطوط سرعة · Manga speed-line burst world · 👁 شوهد في فيديو
- **ماذا / what:** Desaturate + high-contrast threshold the subject, radial speed-line burst behind, ink splatters, halftone, stacked katakana SFX on the left, white speech balloon with tail
- **أرقام / params:** contrast 1.6, lines 60-90 radial
- **الدليل / proof:** `style:pm-sab8a-364a5a`

#### RETRO-73 · لوحة LED نقطية متحركة · LED dot-matrix ticker · 👁 شوهد في فيديو
- **ماذا / what:** Text rendered as glowing dots on a dark board, ticker row scrolls with coloured up/down markers
- **أرقام / params:** dot pitch 4 px, glow blur 6 px, scroll 100 px/s
- **الدليل / proof:** `style:pm-spearwtf-3c1fd1`

#### RETRO-74 · مشاهد البكسل وتلاشي اللوحة · Pixel scene timing & palette fades · 📄 موصوف
- **ماذا / what:** Pixel films run a fixed 60 Hz logic step with 8-12 fps sprite cadence at a small logical resolution, integer-scaled, with light changes stepped through palette or Bayer dither - never alpha, gradients or blur.
- **كيف / how:** Logical sizes 160x144, 240x160, 320x180; integer coordinates; embed sprites as offscreen canvases; expose window.__pixelScene {seek, frameDataURL, play, duration}; audio WAV inlined as data URL and muxed on record.
- **أرقام / params:** 60 Hz step; 8-12 fps sprites; 320x180
- **الدليل / proof:** `kosif-atlas/skills/2460-pixel-art/9526-scene/SKILL.md`

#### RETRO-75 · مشهد بكسل آرت في ملف HTML · Pixel-art scene as one HTML file · 📄 موصوف
- **ماذا / what:** Self-contained Canvas 2D cutscenes at a tiny logical resolution integer-scaled; fixed 60 Hz step; sprites animate at 8-12 fps; lighting and fades step through palette colors or Bayer dither, never alpha/blur; optional embedded WAV.
- **كيف / how:** Plain Canvas 2D, no libraries; expose a scene hook (window.__pixelScene / window.__kosif.seek) for frame-accurate rendering.
- **أرقام / params:** logical 160x144, 240x160 or 320x180; 60 Hz; sprite 8-12 fps; integer coords
- **الدليل / proof:** `kosif-atlas/skills/2460-pixel-art/9526-scene`

#### RETRO-76 · S10 ريترو مطبوع · S10 Printed retro · 📄 موصوف
- **ماذا / what:** Light grain, limited-ink printing, simple edges; slight intentional jitter and card swaps. Distinctive period identity; texture weakens small text and is not a way to hide a poor source.
- **كيف / how:** Two/three-colour separations with mix-blend-mode:multiply, ffmpeg noise=alls=8:allf=t (suggested) grain, stepped 'boil' offsets; KOSIF render_html.cjs (/home/user/kosif-tool/tools/render_html.cjs: HTML/SVG + CSS/WAAPI or window.__kosif.seek(t) -> Playwright frame capture -> ffmpeg)
- **أرقام / params:** cost medium; MG-024 MG-075 MG-104 MG-106 MG-109 MG-117
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/styles.md`

#### RETRO-77 · MG-075 ذاكرة داخل شرائط فيلم · MG-075 Memory on film strips · 📄 موصوف
- **ماذا / what:** Two photos ride two film strips at different speeds and stop on a title - for biographies and memories.
- **كيف / how:** 0-2 strips enter, 2-5 photos pass, 5-8 title; repeated masks, position animation, slight exposure variation; fake damage must never hide faces or falsify photo dates. Faint projector sound.
- **أرقام / params:** 8 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-cinematic-titles.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### RETRO-78 · MG-104 نمط طباعة ريزوغراف متحرك · MG-104 Animated risograph misregistration · 📄 موصوف
- **ماذا / what:** Two ink layers drift slightly then register around a simple drawing, giving a printed character.
- **كيف / how:** 0-1 paper, 1-3 drift, 3-5 settle; colour copies with multiply blend and limited offset; keep the main text copy readable and don't overdo misregistration. Local: CSS mix-blend-mode:multiply layers + grain.
- **أرقام / params:** 5 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-collage-textures.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### RETRO-79 · MG-109 طباعة خشنة تكشف صورة · MG-109 Halftone threshold reveal · 📄 موصوف
- **ماذا / what:** Printed dots multiply until the image becomes clear inside them.
- **كيف / how:** 0-1 few dots, 1-3 density, 3-5 clear image; halftone/dot-pattern mask with an animated threshold; test moire and compression before committing fine dots. Local: canvas per-cell dot radius = f(luma, t) or ImageMagick ordered-dither frames.
- **أرقام / params:** 5 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-collage-textures.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### RETRO-80 · خريطة اختبار البلاطات · Tileset coverage map · 📄 موصوف
- **ماذا / what:** For tiled backgrounds (square, isometric, hex) include filled, empty, edge, outer-corner, inner-corner and isolated pieces; test them on a compact map that exercises every transition and narrow passage; check seams, transparency, filtering, atlas bleed, half-cell offsets and isometric depth sorting …
- **كيف / how:** Tiles in PIL/SVG, test map assembled on canvas, pans rendered via KOSIF render_html.cjs (/home/user/kosif-tool/tools/render_html.cjs: HTML/SVG + CSS/WAAPI or window.__kosif.seek(t) -> Playwright frame capture -> ffmpeg); pad atlas cells to avoid bleed.
- **الدليل / proof:** `kosif-atlas/skills/1526-gamegen/4172-game-tilesets/SKILL.md`

#### RETRO-81 · تلاشي بنمط بيير · Bayer-dither fades and lighting · 📄 موصوف
- **ماذا / what:** Fades and light changes in pixel scenes step through palette colors or ordered Bayer dither patterns instead of gradients.
- **كيف / how:** Canvas 2D: 4x4 or 8x8 Bayer threshold matrix compared to fade level per pixel; integer scaling only.
- **أرقام / params:** Bayer 4x4/8x8
- **الدليل / proof:** `kosif-atlas/skills/2460-pixel-art/9526-scene`

#### RETRO-82 · البلاطات المتصلة والبارالاكس · Seamless tiles and parallax rules · 📄 موصوف
- **ماذا / what:** Tilesets as blob-47 or 16-tile corner sets; parallax layers get slower, darker and less detailed with depth and the scroll step must divide the loop width.
- **كيف / how:** Preview a 3x3 repeat to catch seams; procedural generator for sheets.
- **أرقام / params:** blob-47; 16-tile corner
- **الدليل / proof:** `kosif-atlas/skills/2460-pixel-art/9528-tileset`

#### RETRO-83 · تأثير فن الأسكي · ASCII art post-effect · 📄 موصوف
- **ماذا / what:** Map each cell's luma to a character from a glyph atlas texture.
- **كيف / how:** Canvas: draw charset to texture, sample index = floor(luma*N). Arabic letters could be used as glyph set.
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion`

#### RETRO-84 · لو-فاي · Lo-fi / Cozy loop · 📄 موصوف
- **ماذا / what:** Evening purple-blue with warm yellow and grain; 4-8 s loop of rain, steam, lamp flicker, breathing character.
- **كيف / how:** Copy style sheet section into DESIGN.md, then build via claude-animation-studio render(t).
- **أرقام / params:** #2B2D42->#5C5470, #F2C14E; Tajawal 500, Mulish/Karla; all motion 1-3 s, none faster than 0.8 s, no cuts
- **الدليل / proof:** `100-superskills/skills/trend-animation-styles/references/styles.md`

#### RETRO-85 · مولد سبرايت إجرائي · Procedural sprite generator draw(direction,pose) · 📄 موصوف
- **ماذا / what:** Parametric limb drawing keeps all frames on-model.
- **كيف / how:** python PIL generator
- **أرقام / params:** sizes 16/32/48; preview x4; GIF
- **الدليل / proof:** `100-superskills/skills/pixel-art-game-assets/SKILL.md:22`

#### RETRO-86 · لوحة بكسل مقفلة · Locked material palette (highlight/base/shadow/line) · 📄 موصوف
- **ماذا / what:** Palette by material roles, light from top-left, no off-palette colours, connected 1px outlines, constant volumes.
- **كيف / how:** spec palette
- **الدليل / proof:** `100-superskills/skills/pixel-art-game-assets/SKILL.md:23`

#### RETRO-87 · تايلسيت · Tilesets: RPG Maker A1-A5/B-E, blob-47, 16-tile corner · 📄 موصوف
- **ماذا / what:** Vendored sprite/tileset skills describing autotile layouts, seamless backgrounds, parallax layers.
- **كيف / how:** stdlib renderer described in atlas
- **أرقام / params:** blob-47; hand grids up to ~24x24
- **الدليل / proof:** `100-superskills/skills/pixel-art-game-assets/references/sources.md:9` · `100-superskills/skills/pixel-art-game-assets/references/sources.md:196`

#### RETRO-88 · ورقة سبرايت · Sprite sheet + held impact frames · 📄 موصوف
- **ماذا / what:** Engine-ordered sheet, preview GIF, held frames on hits, contact/pass checks.
- **كيف / how:** PIL
- **الدليل / proof:** `100-superskills/skills/pixel-art-game-assets/SKILL.md:24`

#### RETRO-89 · التحريك على اثنين أو واحد · Animating on twos vs ones · 📄 موصوف
- **ماذا / what:** On twos for hand-drawn/stop-motion feel, ones for smooth vector.
- **كيف / how:** Quantize t to 2-frame steps.
- **أرقام / params:** 12 drawings/s
- **الدليل / proof:** `kosif-tool/playbooks/characters.md:29`

#### RETRO-90 · مقاطع بكسل في المونتاج · Pixel-art montage segments · 💡 فكرة
- **ماذا / what:** Insert a retro pixel cutscene (dithered sky, parallax, typed dialogue) as a chapter break inside a modern edit.
- **كيف / how:** Render canvas scene frames at 320x180, upscale nearest x6 to 1920x1080 with ffmpeg -sws_flags neighbor.
- **أرقام / params:** x6 nearest
- **الدليل / proof:** `kosif-atlas/skills/2460-pixel-art/9526-scene`

#### RETRO-91 · حركة بكسل على شبكة صحيحة · Integer-grid pixel motion · 💡 فكرة
- **ماذا / what:** All motion snaps to whole pixels on a low-res grid upscaled with nearest-neighbour; no smoothing.
- **كيف / how:** Canvas at low res, imageSmoothingEnabled=false, Math.round positions, CSS image-rendering:pixelated upscale.
- **أرقام / params:** integer px steps; nearest-neighbour
- **الدليل / proof:** `style:pm-0xevinho-3777d8`

#### RETRO-92 · غليتش شرائح وإزاحة ألوان · Slice glitch + RGB split · 💡 فكرة
- **ماذا / what:** Short horizontal slice displacement and channel offset after hits.
- **كيف / how:** Canvas/shader slice offsets + per-channel translate for 2-4 frames.
- **أرقام / params:** slices <=24 px; RGB 4-6 px; 2-4 frames
- **الدليل / proof:** `style:pm-micheleharmonic-77628e`
