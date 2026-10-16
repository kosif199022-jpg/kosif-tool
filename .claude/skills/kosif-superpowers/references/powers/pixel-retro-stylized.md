# البكسل والريترو والأساليب الخاصة — Pixel, retro & stylised

> **قوتك هنا:** تصنع البكسل كما يجب — دقة منطقية صغيرة، إحداثيات صحيحة، تكبير بأقرب جار، وإضاءة تتدرج عبر اللوحة أو مصفوفة Bayer لا عبر الشفافية — ثم تضيف الطباعة القديمة (هافتون، ريزوغراف، حبرين)، الـ CRT والـ VHS، الـ ASCII، والغليتش بجرعات قصيرة.
> **أقوى دليل:** مختبر هنا: مشهد 320×180 بلوحة Game Boy من 4 ألوان ودخول بعتبة Bayer 4×4، كُبّر ×6 بـ `scale=…:flags=neighbor` إلى 1920×1080 (48 إطارًا، تباين داخل الكتلة 2.37 فقط بعد الترميز)، ثم غليتش `rgbashift` وخطوط مسح وحبيبات، وASCII وهافتون؛ واختبارات `dither.mjs` (Floyd-Steinberg/Atkinson…) نجحت 3/3، وثيمات Fastify الريترو مقفلة بالاختبارات.
> **You can:** build pixel cutscenes, sprites and tiles, retro print and screen looks, ASCII/halftone/LED post passes and beat-anchored glitch — in Canvas, Pillow, ffmpeg or WebGL.
> **32 powers follow** — ✅ 10 · 🟢 4 · 📦 3 · 🔑 0 · 👁 5 · 📄 9 · 💡 1.

**الحالة / status:** ✅ مُثبت هنا (كود + اختبار أو رندر في هذه الحاوية) · 🟢 جاهز (كود المالك يعمل بلا إضافات) · 📦 بأمر تثبيت · 🔑 مفتاح أو خدمة · 👁 شوهد في فيديو أنتجتَه (وصفة البناء مرفقة) · 📄 موصوف فقط · 💡 فكرة.
مسارات الدليل نسبية إلى `/home/user/`؛ `style:<id>` = فيديو مرجعي أنتجتَه سابقًا (ملاحظاته في `kosif-tool/styles/<id>/`).

**فحص هذه الحاوية (2026-10-16):** numpy + Pillow (بكسل ودثر Bayer ولوحة مقفلة) ✔ · ffmpeg `flags=neighbor` و`rgbashift` و`noise` و`drawgrid` ✔ · `node --test dither.test.mjs` 3/3 ✔ · Fastify production-profiles (ثيمات J/K/N/Q) 10/10 ✔ · مشاهد WebGL للهافتون/ASCII تحتاج Chromium (موجود) ولم تُرندر هنا.

## الفهرس / contents
- **البكسل آرت — Pixel art** — RETRO-01 … RETRO-09 (9)
- **الطباعة القديمة والورق — Retro print & paper** — RETRO-10 … RETRO-15 (6)
- **الشاشات القديمة: CRT وVHS وLED — Old screens: CRT, VHS & LED** — RETRO-16 … RETRO-21 (6)
- **ASCII والخلايا والدثر — ASCII, cell patterns & dither passes** — RETRO-22 … RETRO-25 (4)
- **الغليتش — Glitch** — RETRO-26 … RETRO-28 (3)
- **الثيمات المقفلة والأساليب الخاصة — Locked themes & special styles** — RETRO-29 … RETRO-31 (3)
- توليفات قوية / power combos · أخطاء ممنوعة / never do · أقوى 5 حركات توقيع / 5 signature moves
- **إضافات v2 — v2 additions** — RETRO-X01 (1)

## البكسل آرت — Pixel art

_دقة منطقية صغيرة، أعداد صحيحة، أقرب جار — ولا ضبابية ولا شفافية ولا تدرجات ناعمة._

#### RETRO-01 · مشهد بكسل في ملف HTML واحد · Self-contained pixel cutscene (one HTML) · ✅ مُثبت هنا / proven here
- **ماذا / what:** مشهد Canvas 2D بدقة منطقية صغيرة يُكبَّر بمعامل صحيح، بخطوة منطق 60 Hz وعِفريتات 8–12 إطارًا/ث، وبارالاكس وحوار يُكتب، وواجهة seek للرندر الدقيق. — A Canvas 2D scene at a tiny logical resolution, integer-scaled, 60 Hz logic, 8–12 fps sprites, parallax, typed dialogue and a seek hook for frame-accurate rendering.
- **متى أستخدمها / when:** فاصل ريترو، قصة لعبة، ريل حنين — retro chapters, game stories, nostalgia reels.
- **كيف / how:** Logical 160×144, 240×160 or 320×180; ctx.imageSmoothingEnabled=false; Math.round every position; CSS image-rendering:pixelated; embed sprites as offscreen canvases; expose window.__pixelScene {seek, frameDataURL, play, duration} (or window.__kosif.seek) and render with kosif-tool render_html.cjs, or render frames and upscale with ffmpeg. Verified here: a 320×180 scene upscaled ×6 with flags=neighbor stayed blocky (mean intra-block std 2.37 after H.264). **أرقام / params:** 320×180 ×6 = 1920×1080 · 60 Hz logic · sprites 8–12 fps.

```bash
ffmpeg -framerate 24 -i f_%03d.png -vf "scale=1920:1080:flags=neighbor" \
  -c:v libx264 -pix_fmt yuv420p -crf 18 pixel.mp4     # 320x180 x6, no smoothing
```

- **الدليل / proof:** `kosif-atlas/skills/2460-pixel-art/9526-scene/SKILL.md` · `kosif-tool/tools/render_html.cjs` · `kosif-tool/styles/pixel-art/SKILL.md` · `style:pm-hoyoyoda-3a5c08`

#### RETRO-02 · الإضاءة والتلاشي بدثر Bayer · Bayer-dither fades & palette-stepped light · ✅ مُثبت هنا / proven here
- **ماذا / what:** التلاشي وتغير الضوء يتدرجان عبر ألوان اللوحة أو مصفوفة Bayer 4×4/8×8، لا عبر الشفافية أو التدرج أو الضبابية. — Fades and light changes step through palette colours or a 4×4/8×8 Bayer matrix — never alpha, gradients or blur.
- **متى أستخدمها / when:** كل دخول/خروج/غروب في مشهد بكسل — every fade in a pixel scene.
- **كيف / how:** Per pixel compare the fade level with B[y%4][x%4]/16 (4×4 = 0 8 2 10 / 12 4 14 6 / 3 11 1 9 / 15 7 13 5); quantise brightness to the palette ramp with the same threshold as offset. Verified here with the Game Boy ramp #0f380f #306230 #8bac0f #9bbc0f: output frames contain exactly 4 colours. **أرقام / params:** Bayer 4×4 / 8×8 · 4-colour ramp.

```python
B = np.array([[0,8,2,10],[12,4,14,6],[3,11,1,9],[15,7,13,5]])/16
show = fade > B[yy%4, xx%4]                 # ordered-dither fade mask
lvl = np.clip((v*3.999 + (B[yy%4,xx%4]-.5)*.9).astype(int), 0, 3)
img = palette[lvl] * show[..., None]        # 4-colour ramp only
```

- **الدليل / proof:** `kosif-atlas/skills/2460-pixel-art/9526-scene/SKILL.md` · `kosif-atlas/skills/2460-pixel-art/9530-vfx/SKILL.md`

#### RETRO-03 · عفريتات مقفلة اللوحة ومولّد الوضعيات · Palette-locked sprites & procedural pose generator · 🟢 جاهز / ready
- **ماذا / what:** عفريتات صغيرة كشبكات حروف مربوطة بلوحة ثابتة، والكبيرة يولّدها draw(direction, pose) من زوايا الأطراف وطور الخطوة فيبقى كل إطار على النموذج. — Small sprites as character grids mapped to a fixed palette; larger ones from a draw(direction, pose) generator so every frame stays on-model.
- **متى أستخدمها / when:** شخصيات بكسل ودورات مشي — pixel characters and walk cycles (CHAR).
- **كيف / how:** Pillow: rows of palette keys → PNG at 1×, nearest ×8 preview; hand grids ≤~24×24 (observed 16×16 ×3). Rules: silhouette first, one light direction (top-left), hue-shifted ramps, palette roles highlight/base/shadow/line, selective 1 px connected outline, no pillow shading, no dithering on small sprites. Cycles planned in a table (key poses, frame counts, durations); RPG Maker MZ walk = 3 patterns 0-1-2-1 at 48×48; mirror only symmetric designs; GIF delays in 10 ms units, floor 20 ms; hold impact frames; sizes 16/32/48. **أرقام / params:** ≤24×24 hand grid · MZ 48×48 · GIF ≥20 ms.
- **الدليل / proof:** `kosif-atlas/skills/2460-pixel-art/9527-sprite` · `kosif-atlas/skills/2460-pixel-art/9525-animate/SKILL.md` · `100-superskills/skills/pixel-art-game-assets/SKILL.md:22` · `style:pm-aisongman-71ffac`

#### RETRO-04 · مؤثرات بكسل بخطوات اللوحة · Palette-stepped pixel VFX sheets · 📄 موصوف / documented only
- **ماذا / what:** شرارات وضربات وانفجارات كأوراق عفريتات تتلاشى بالنزول على سلّم اللوحة، مع إمساك إطار الارتطام. — Sparks, slashes and explosions as sprite sheets that fade down a palette ramp, holding the impact frame.
- **متى أستخدمها / when:** ضربات ومعارك ولحظات ارتطام — hits and impacts.
- **كيف / how:** Python stdlib renderer from a spec; timing table first; sheet in engine order + preview GIF; contact/pass checks; 2–4 review rounds. Radial speed lines (anime/manga) flicker per frame behind the hit. **أرقام / params:** GIF ≥20 ms · hold impact.
- **الدليل / proof:** `kosif-atlas/skills/2460-pixel-art/9530-vfx/SKILL.md` · `100-superskills/skills/pixel-art-game-assets/SKILL.md:24` · `style:pm-allforbigfire-86ff3c`

#### RETRO-05 · البلاطات والبارالاكس · Seamless tiles & parallax rules · 📄 موصوف / documented only
- **ماذا / what:** بلاطات blob-47 أو 16 زاوية، ولكل خلفية قطع مملوءة وفارغة وحواف وزوايا داخلية وخارجية ومعزولة؛ وطبقات البارالاكس أبطأ وأغمق وأقل تفصيلًا مع العمق. — blob-47 or 16-tile corner sets covering every transition; parallax layers slower, darker and simpler with depth.
- **متى أستخدمها / when:** عوالم ألعاب وخلفيات متحركة — game worlds and scrolling backdrops.
- **كيف / how:** Preview a 3×3 repeat to catch seams; test on a compact map exercising every transition and narrow passage; pad atlas cells against bleed; the scroll step must divide the loop width; RPG Maker A1–A5/B–E layouts; render pans via render_html.cjs. **أرقام / params:** blob-47 · 16-tile corner · 3×3 seam preview.
- **الدليل / proof:** `kosif-atlas/skills/2460-pixel-art/9528-tileset` · `kosif-atlas/skills/1526-gamegen/4172-game-tilesets/SKILL.md` · `100-superskills/skills/pixel-art-game-assets/references/sources.md:9`

#### RETRO-06 · حركة على شبكة صحيحة والرسم على الاثنين · Integer-grid motion & animating on twos · ✅ مُثبت هنا / proven here
- **ماذا / what:** كل حركة تقفز بكسلًا كاملًا على شبكة منخفضة، والحركة «على الاثنين» (12 رسمة/ث) تعطي إحساس اليد والستوب موشن. — All motion snaps to whole pixels on a low-res grid; animating on twos (12 drawings/s) gives a hand-made, stop-motion feel.
- **متى أستخدمها / when:** أي مشهد بكسل أو قص ورقي — pixel scenes and cutout looks.
- **كيف / how:** Math.round(x) on the logical grid (verified: an 8×8 block moved in 1 px steps); quantise time: t2 = floor(t*12)/12 for twos, or 12 fps steps for snappy paper cutouts (pop/drop/slide with short settle, no slow CGI drift — Fastify theme N and the vox collage profile request it in prompts). **أرقام / params:** 12 drawings/s · 1 px steps.

```js
const tq = Math.floor(t * 12) / 12;          // on twos at 24 fps
const x = Math.round(x0 + v * tq);           // whole logical pixels only
```

- **الدليل / proof:** `kosif-tool/playbooks/characters.md:29` · `kosif-tool/styles/pm-0xevinho-3777d8/BRIEF.md` · `fastify-motion-bro/scripts/profiles/vox-history.mjs:11,50`

#### RETRO-07 · ديوراما بكسل بانعكاس ماء · Pixel diorama with water reflection · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** ارسم المشهد على Canvas صغير (~480×270)، اعكس النصف العلوي في البحيرة بلون أغمق وإزاحة جيبية أفقية لكل صف، ثم كبّر ×4. — Render at ~480×270, mirror the upper half into the lake with a darker tint and per-row sine offset, upscale ×4.
- **متى أستخدمها / when:** لقطات بكسل هادئة وغروب — calm pixel landscapes.
- **كيف / how:** Ripple amplitude 1–2 px, row phase speed 2 rad/s; striped sun + reflection lines for a pixel sunset stage at 320×180; parallax hills. **أرقام / params:** ripple 1–2 px · 2 rad/s · ×4.
- **الدليل / proof:** `style:pm-0xevinho-3777d8` · `style:pm-pluginplay-3d4006`

#### RETRO-08 · واجهات ألعاب 8-بت: HUD وحوار وبطاقة عنوان · 8-bit HUD, dialogue box & game title card · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** خط بكسل لـ LEVEL/العملات/الوقت، تلال بارالاكس، صندوق حوار بإطار وكتابة حرفًا حرفًا، وبطاقة عنوان كتلية تختفي عند البدء. — Pixel-font HUD, parallax hills, bordered dialogue box with typewriter text, blocky title card.
- **متى أستخدمها / when:** «حياتك كلعبة»، قصص ألعاب، فواصل — game metaphors (STORY).
- **كيف / how:** Pixel scale 4×, typewriter 30 ms/char (Latin; Arabic types per word, ARAB-29); caption box yellow with black border, year tag, 1-frame pop; grid digit reveal: 30 px cells inside the glyph mask flip to the accent with radial stagger; icon assembled from squares appearing at random with the top squares flickering. **أرقام / params:** scale 4× · 30 ms/char · 30 px cells.
- **الدليل / proof:** `style:pm-emollick-8661a8` · `style:pm-ivanfioravanti-bd9261` · `style:pm-pluginplay-3d4006` · `style:pm-raphaelaubryy-4b137e` · `style:pm-robvjourney-ce3e1a`

#### RETRO-09 · فاصل بكسل داخل مونتاج حديث · Pixel chapter break inside a modern edit · 💡 فكرة / idea
- **ماذا / what:** أدخل مشهد بكسل (سماء مدثّرة، بارالاكس، حوار يُكتب) كفاصل فصل داخل فيلم حديث. — Insert a retro pixel cutscene as a chapter break inside a modern edit.
- **متى أستخدمها / when:** كسر الإيقاع في فيلم طويل — pattern interrupt (STORY).
- **كيف / how:** Render at 320×180, upscale nearest ×6 to 1920×1080 with -sws_flags neighbor (or scale flags=neighbor), xfade in with a pixelize transition (TRANS) and back. **أرقام / params:** ×6 nearest.
- **الدليل / proof:** `kosif-atlas/skills/2460-pixel-art/9526-scene/SKILL.md`

## الطباعة القديمة والورق — Retro print & paper

_حبران أو ثلاثة، مزج multiply، وحبيبات خفيفة — والنص الأساسي يبقى مقروءًا._

#### RETRO-10 · هافتون وشاشات CMYK · Halftone & CMYK screens · ✅ مُثبت هنا / proven here
- **ماذا / what:** نقاط تكبر وتصغر بالإضاءة في خلايا ثابتة، أو أربع شبكات CMYK بزوايا مختلفة مضروبة معًا لشكل الطباعة. — Dots sized by luma in fixed cells, or four rotated CMYK grids multiplied for a print look.
- **متى أستخدمها / when:** ملصقات، كوميكس، هوية طباعية — posters, comics, print identity (TEX).
- **كيف / how:** Shader: uvPixel = size*floor(uv/size); cellUV = fract(uv/size); luma = dot(rgb, (0.2126, 0.7152, 0.0722)); r = R*(0.1+luma) (or 0.1 + (1−luma) for ink on paper); smoothstep with fwidth AA; 3×3 neighbour sampling breaks the grid; gooey via smooth-min; CMYK angles C15 M75 Y0 K45. Verified here as a Pillow still (cell 12 px over 1920×1080). Threshold reveal (MG-109): few dots 0–1 s → density 1–3 s → clear image 3–5 s; test moiré and compression before fine dots. HyperFrames halftone-field: LED-wall dots on simplex flow, cell 54, palette #00AAFF #C2FF67 #6600FF #000000. **أرقام / params:** luma .2126/.7152/.0722 · CMYK 15/75/0/45° · cell 12 px.
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md` · `kosif-atlas/skills/97-frontend-design-director/206-frontend-design-director/examples/webgl/halftone.frag` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-collage-textures.md` · `kosif-one/vendor/hyperframes/registry/blocks/halftone-field/halftone-field.html`

#### RETRO-11 · ريزوغراف وانزياح الحبر · Risograph misregistration & two-ink print · ✅ مُثبت هنا / proven here
- **ماذا / what:** طبقتا حبر تنزاحان قليلًا ثم تنطبقان حول رسم بسيط فتعطي طابعًا مطبوعًا. — Two ink layers drift slightly then register around a simple drawing.
- **متى أستخدمها / when:** أفلام فنية، هوية محلية، شروح بطابع ورقي — print-flavoured pieces.
- **كيف / how:** Duplicate the layer in the second ink, offset 4–6 px, mix-blend-mode:multiply; MG-104 timing 0–1 s paper, 1–3 s drift, 3–5 s settle; grain via ffmpeg noise=alls=8:allf=t (ran here); verified here with Pillow ImageChops.multiply — a 6 px drift of pink #FF48B0 over blue #0078BF on paper #F2EBDD gives 4 colours (paper, two fringes, overlap), registered gives 2; keep the main text copy registered and readable. S10 printed-retro family: 2–3 colour separations, stepped boil offsets, card swaps; texture weakens small text. **أرقام / params:** offset 4–6 px · drift 1–3 s · grain alls=8.

```css
.ink2 { mix-blend-mode: multiply; transform: translate(calc(var(--d) * 5px), calc(var(--d) * -3px)); }
/* --d: 1 → 0 between 1 s and 3 s, then registered */
```

- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/styles.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-collage-textures.md` · `style:pm-rneayan-474bcf` · `kosif-one/vendor/hyperframes/docs/guides/media-effects.mdx`

#### RETRO-12 · الذكريات على شرائط الفيلم · Memories on film strips · 📄 موصوف / documented only
- **ماذا / what:** صورتان تركبان شريطي فيلم بسرعتين مختلفتين وتتوقفان عند عنوان — للسير والذكريات. — Two photos ride two film strips at different speeds and stop on a title.
- **متى أستخدمها / when:** سيرة ذاتية، ذكرى، تكريم — biographies and memorials (PHOTO).
- **كيف / how:** MG-075: 0–2 s strips enter, 2–5 s photos pass, 5–8 s title; repeated masks, slight exposure variation, faint projector sound; fake damage must never hide faces or falsify dates. **أرقام / params:** 8 s.
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-cinematic-titles.md`

#### RETRO-13 · ملصق مسطّح من صورة (k ألوان) · Flat-paint poster vectorisation (k colours) · 🟢 جاهز / ready
- **ماذا / what:** تُنعَّم الصورة بفلتر يحفظ الحواف وتُجمع في k لون Lab فتصير ملصقًا مسطحًا يتكبر بلا حدود. — Edge-preserving smoothing + k Lab colours turn a photo into a flat-paint poster that scales without limit.
- **متى أستخدمها / when:** أغلفة بأسلوب ملصق، تحويل صورة لرسم — poster looks.
- **كيف / how:** vectorize.trace(path, colors=k) (auto when the input looks like a photo): bilateralFilter + cv2.kmeans KMEANS_PP; k = 24 default (4 or 6 for small images); simplify 1.1, min_area 2.5, sharpen 0.4; export SVG (FMT painter export). **أرقام / params:** k 24 · simplify 1.1 · min_area 2.5.
- **الدليل / proof:** `kosif-studio/vectorize.py:164` · `kosif-studio/vectorize.py:188`

#### RETRO-14 · معالجات الصورة الطباعية في HyperFrames · HyperFrames print treatments (engraving, crosshatch, Kuwahara, two-ink, halftone) · 📦 بأمر تثبيت / one install
- **ماذا / what:** معالجات غير متلفة للصور والفيديو: حفر، تهشير، رسم Kuwahara، حبران، هافتون، دثر مرتب، شاشة أحادية. — Non-destructive image/video treatments: engraving, crosshatch, Kuwahara paint, two-ink, halftone, ordered dither, mono screen.
- **متى أستخدمها / when:** تحويل لقطات حقيقية إلى طابع مطبوع — stylising real footage.
- **كيف / how:** `npx hyperframes media-treatment --selector <css> --apply` (or the Studio) writes data attributes; the source file stays untouched. Pair with a two-colour palette from BRAND.
- **تثبيت / install:** `npm i -D hyperframes@0.8.164`
- **رخصة / license:** Apache-2.0
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/guides/media-effects.mdx`

#### RETRO-15 · عالم المانغا: خطوط سرعة وحبر · Manga speed-line burst world · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** الموضوع بلا لون وبعتبة تباين عالية، خطوط سرعة شعاعية خلفه، رشات حبر، هافتون، مؤثرات صوتية مكتوبة عموديًا، وبالون كلام. — Desaturated high-contrast subject, radial speed-line burst, ink splatters, halftone, stacked SFX text, speech balloon.
- **متى أستخدمها / when:** ذروة أكشن أو ريل أنمي — action peaks, anime reels.
- **كيف / how:** Contrast 1.6, 60–90 radial lines; for Arabic replace katakana SFX with short Arabic onomatopoeia set vertically per word (ARAB); balloon white with tail. **أرقام / params:** contrast 1.6 · 60–90 lines.
- **الدليل / proof:** `style:pm-sab8a-364a5a` · `style:pm-allforbigfire-86ff3c`

## الشاشات القديمة: CRT وVHS وLED — Old screens: CRT, VHS & LED

_خطوط مسح، انحناء، تشويش شريط، وشاشات نقطية — كإطار يروي الزمن لا كفلتر عشوائي._

#### RETRO-16 · CRT وخطوط المسح وVHS · CRT, scanlines & VHS damage · ✅ مُثبت هنا / proven here
- **ماذا / what:** خطوط مسح وانحناء الشاشة وتلف الشريط وفصل القنوات وتنعيم الألوان — لتقول «ماضٍ» أو «شاشة قديمة». — Scanlines, curvature, tape damage, channel separation and chroma softening.
- **متى أستخدمها / when:** إعلان قديم، أرشيف، تلفزيون منزلي — infomercials, archive, home TV looks.
- **كيف / how:** ffmpeg (ran here): drawgrid=w=iw:h=4:t=1:c=black@0.25 for 2 px scanlines on 4 px period + noise=alls=8:allf=t grain + rgbashift for channel separation. CSS: repeating-linear-gradient(transparent 0 2px, rgba(0,0,0,.1) 2px 4px); tracking noise 2–3 lines. HyperFrames treatments: Tape Damage, Film Artifacts, Scanlines, CRT Curvature, Channel Separation, Chroma Softening. Infomercial look (observed): purple sunburst, CRT prop, yellow slanted "CALL NOW!" block, VHS PLAY/clock OSD. **أرقام / params:** scanline 2 px / 4 px period · grain alls=8 · VHS noise 2–3 lines.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/guides/media-effects.mdx` · `kosif-atlas/skills/2981-designer-skill/12625-designer-skill/reference/aesthetic-systems.md` · `style:pm-emollick-8661a8`

#### RETRO-17 · لقطات تبدو على شاشة حقيقية · On-screen display & camcorder HUD · 📦 بأمر تثبيت / one install
- **ماذا / what:** شبكة وخطوط مسح وتظليل ولمعة مع التفاف ثلاثي الأبعاد كي تبدو اللقطة معروضة على شاشة؛ وواجهة كاميرا فيديو بنقطة REC وبطارية وتاريخ وعداد. — Grid, scanline, vignette and sheen with a 3D warp so footage reads as on a real display; camcorder HUD with REC dot, battery, date and counter.
- **متى أستخدمها / when:** لقطات أرشيف، «فيديو عائلي»، شاشات داخل القصة — home-video and screen-in-scene.
- **كيف / how:** `npx hyperframes add yt-screen-warp` / `camcorder-hud` (4 s overlay, 1920×1080, GSAP paused timeline) / `yt-lcd-background` (paper board with drifting scanlines, pixel grid, grain, blur-focus title with chromatic fringe, 10 s). Date and counter should come from the timeline, not the wall clock. **أرقام / params:** HUD 4 s · board 10 s.
- **تثبيت / install:** `npm i -D hyperframes@0.8.164`
- **رخصة / license:** Apache-2.0 registry; GSAP inside uses its standard licence.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/components/yt-screen-warp/yt-screen-warp.html` · `kosif-one/vendor/hyperframes/registry/blocks/camcorder-hud/camcorder-hud.html` · `kosif-one/vendor/hyperframes/registry/blocks/yt-lcd-background/yt-lcd-background.html`

#### RETRO-18 · لوحة LED نقطية وشريط أخبار · LED dot-matrix ticker · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** نص كنقاط مضيئة على لوحة داكنة، وصف شريط يمر بعلامات صعود وهبوط ملونة. — Text as glowing dots on a dark board with a scrolling ticker and coloured up/down markers.
- **متى أستخدمها / when:** أسعار، نتائج، لوحات ملاعب ومحطات — prices, scores, station boards (DATA).
- **كيف / how:** Dot pitch 4 px, glow blur 6 px, scroll 100 px/s; sample the text mask on a grid and draw circles (Canvas) — for Arabic draw the shaped text to an offscreen canvas first, then sample (never per letter). Staggered LED panel cells are part of the cell-pattern family. **أرقام / params:** pitch 4 px · glow 6 px · 100 px/s.
- **الدليل / proof:** `style:pm-spearwtf-3c1fd1` · `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md`

#### RETRO-19 · أثر الأوسيلوسكوب الفوسفوري · Oscilloscope phosphor trace · 📦 بأمر تثبيت / one install
- **ماذا / what:** شعاع CRT يرسم موجة على شبكة 10×8 بإثبات فوسفوري exp(−age/τ) ويسطع حيث يتباطأ. — A CRT beam sweeps a waveform across a 10×8 graticule with phosphor persistence exp(−age/τ), brighter where it slows.
- **متى أستخدمها / when:** صوت وتقنية وعلم — audio/science/tech pieces (BEAT).
- **كيف / how:** `npx hyperframes add oscilloscope-trace`: waveform sine|square|triangle|data, frequency 12, amplitude 3, persistence 100 ms, phosphor #5dff8f, sweep rate 5; Canvas 2D painter. Drive "data" from the audio envelope for an audio-reactive scope. **أرقام / params:** persistence 100 ms · #5dff8f · 10×8.
- **تثبيت / install:** `npm i -D hyperframes@0.8.164`
- **رخصة / license:** Apache-2.0
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/oscilloscope-trace/oscilloscope-trace.html`

#### RETRO-20 · سينث ويف / ريترو ويف · Synthwave / retrowave · 📄 موصوف / documented only
- **ماذا / what:** أرضية شبكة نيون، شمس متدرجة بخطوط، نص كروم — ثمانينيات. — Neon grid floor, banded gradient sun, chrome text — the 80s.
- **متى أستخدمها / when:** موسيقى إلكترونية، ألعاب، حنين الثمانينيات — synth music, gaming.
- **كيف / how:** `python3 tools/kosif.py scaffold retrowave <dir>`; Three.js or 2.5D perspective grid scrolling toward camera; sun as a vertical gradient with horizontal scanline gaps; layered blur glow (GLOW); neon stroke on the title. Observed in synthwave title videos.
- **الدليل / proof:** `kosif-tool/styles/retrowave/SKILL.md` · `kosif-tool/styles/retrowave/STYLE.json` · `style:pm-rendesr-86be44`

#### RETRO-21 · تليمتري CRT الداكن · Tactical telemetry / CRT-dark system · 📄 موصوف / documented only
- **ماذا / what:** نص فوسفوري على أسود غير كامل، خطوط مسح، وأخضر الطرفية على عنصر واحد فقط. — Phosphor text on near-black, scanlines, terminal green on one element only.
- **متى أستخدمها / when:** شرح تقني، أمن، بيانات حية — tech/security/data pieces.
- **كيف / how:** bg #0A0A0A/#121212 (never #000), fg #EAEAEA, red #E61919, green #4AF626 once; scanlines repeating-linear-gradient 2 px transparent / 2 px rgba(0,0,0,.1). Motion "haunted machine": quantised ticks, decode text, split-flap, radar sweep, no smooth easing (STORY personalities). **أرقام / params:** scanline period 4 px · green once.
- **الدليل / proof:** `kosif-atlas/skills/2981-designer-skill/12625-designer-skill/reference/aesthetic-systems.md` · `kosif-atlas/skills/342-kernel/1223-frontend/motion/haunted-machine.md`

## ASCII والخلايا والدثر — ASCII, cell patterns & dither passes

_قسّم الصورة إلى خلايا، ثم شكّل كل خلية بالإضاءة: حرف، نقطة، كتلة ليغو، أو عتبة._

#### RETRO-22 · تحويل المشهد إلى ASCII · ASCII render pass · ✅ مُثبت هنا / proven here
- **ماذا / what:** كل خلية تتحول إلى حرف من سلّم كثافة حسب إضاءتها، ويمكن أن تبدأ خشنة وتدقق حتى تُقرأ الصورة. — Each cell becomes a character from a density ramp by its luma; resolution can step coarse → fine until legible.
- **متى أستخدمها / when:** شعارات تقنية، افتتاح مطوّرين، كشف غامض — dev intros, mysterious reveals.
- **كيف / how:** Ramp " .:-=+*#%@" (verified here on an 80×45 sample); 120 columns for a full frame; colour per cell optional; draw the charset to a texture and index = floor(luma·N). HyperFrames ascii-render-pass resolves at 1.4 s (grid coarse|med|fine); ascii-trail-reveal sweeps an S-curve through a seeded grid to uncover a panel; 8 ASCII treatment styles. Arabic letters can be the glyph set — draw them as whole shaped glyphs per cell, never join across cells. **أرقام / params:** ramp 10 chars · 120 cols · resolve 1.4 s.
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md` · `kosif-one/vendor/hyperframes/registry/components/ascii-render-pass/ascii-render-pass.html` · `kosif-one/vendor/hyperframes/registry/components/ascii-trail-reveal/ascii-trail-reveal.html` · `style:pm-rames-jusso-589f80` · `style:pm-jacksonfall-54b2ac`

#### RETRO-23 · عائلة الخلايا: LED، ليغو، كروشيه، زجاج مموج · Cell-pattern family: LED, Lego, crochet, fluted glass, threshold matrices · 📄 موصوف / documented only
- **ماذا / what:** بعد التبكسل شكّل كل خلية: أعمدة LED، أزرار ليغو، نسيج كروشيه، زجاج مموج، مصفوفات عتبة 8×8، إيصال حراري. — After pixelating, shape each cell: LED bars, Lego studs, woven crochet, fluted glass, 8×8 threshold matrices, receipt print.
- **متى أستخدمها / when:** لوك مميز لريل أو هوية — distinctive looks.
- **كيف / how:** GLSL: uvPixel = size*floor(uv/size); cellUV = fract(uv/size); per-cell SDF or luma threshold; chromatic dispersion ~0.002 UV, fresnel, backside-render trick for glass dispersion; animate size in powers of two for progressive depixelation. Canvas or ffmpeg can do the simpler ones. **أرقام / params:** 8×8 matrices · CA 0.002 · size powers of 2.
- **الدليل / proof:** `kosif-atlas/skills/95-awwwards-motion/204-awwwards-motion/SKILL.md` · `kosif-atlas/skills/97-frontend-design-director/206-frontend-design-director/examples/webgl/halftone.frag`

#### RETRO-24 · الدثر المرتب والدثر بالانتشار · Ordered & error-diffusion dither passes · ✅ مُثبت هنا / proven here
- **ماذا / what:** مشهد يظهر من ضوضاء ثنائية اللون إلى صورة نظيفة بدثر Bayer، أو فيديو كامل بدثر Floyd-Steinberg/Atkinson بلوحة مخصصة. — A scene emerges from two-tone Bayer noise to clean, or a whole video is dithered with Floyd-Steinberg/Atkinson in a custom palette.
- **متى أستخدمها / when:** لوك Game Boy، ماكنتوش قديم، فن رقمي — retro computer looks.
- **كيف / how:** Exact offline: `node scripts/dither.mjs --input src.mp4 --out out.mp4 --algorithm atkinson --palette "#0f380f,#306230,#8bac0f,#9bbc0f" --point-size 3` (algorithms Floyd-Steinberg, Atkinson, Jarvis-Judice-Ninke, Stucki, Burkes, Sierra; dither.test.mjs passed 3/3 here). ffmpeg alternative: paletteuse=dither=bayer:bayer_scale=2 with a 4-colour palette. Registry ordered-dither-pass: matrix 2|4|8, levels 2–6, direction in|out, stateless per frame. Mascot render-state morph (observed): solid → 6 px ordered-dither halftone rising from the bottom → dashed 8/6 wireframe with guide ellipses. **أرقام / params:** Bayer 2/4/8 · point size 3 · GB palette.
- **رخصة / license:** HyperFrames is Apache-2.0.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/media-use/scripts/dither.mjs` · `kosif-one/vendor/hyperframes/skills/media-use/scripts/dither.test.mjs` · `kosif-one/vendor/hyperframes/registry/components/ordered-dither-pass/ordered-dither-pass.html` · `style:pm-anthonyriera-9b1b2a`

#### RETRO-25 · تموّج أوب آرت · Op-art concentric moiré · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** خطوط متحدة المركز من مركزين أو عتبة جيبية شعاعية، وتحريك الطور يعطي اهتزازًا بصريًا. — Concentric stripes from two centres or a radial sinusoid threshold; animate phase for vibrating moiré.
- **متى أستخدمها / when:** فواصل تجريبية، موسيقى، هوية جريئة — experimental interludes.
- **كيف / how:** Stripe 12 px in red/cream/black; threshold sin(2π·(r1 − r2)/λ + φ(t)); keep flashing below 3 Hz. **أرقام / params:** stripe 12 px · flash <3 Hz.
- **الدليل / proof:** `style:pm-ayushunleashed-ece3e3`

## الغليتش — Glitch

_الغليتش لكمة قصيرة (≤0.4 ث) ثم عودة للنظافة — مرتبط بحدث أو ضربة، لا خلفية دائمة._

#### RETRO-26 · تقطيع رقمي قصير للعناصر · DOM glitch stutter (motion-kit) · 🟢 جاهز / ready
- **ماذا / what:** إزاحة RGB وشرائح عشوائية مزروعة البذرة تعود للنظافة، على أي عنصر HTML. — Seeded RGB split and random slice displacement on any element, returning to clean.
- **متى أستخدمها / when:** لحظة ارتطام، كلمة تقنية، انتقال — hits, tech words, transitions.
- **كيف / how:** MOTION.glitch(tl, el, at, {dur, amp, seed}) in motion-kit.js: ≤0.4 s (default 0.3 s), 30 steps/s, amp 10 px, magenta rgba(255,0,80,.7) / cyan rgba(0,200,255,.7) drop shadows, random inset slices; kosif-studio tests assert the kit exports glitch. On Arabic text keep slices horizontal across the whole word (never split letters into spans). **أرقام / params:** ≤0.4 s · 30 steps/s · amp 10 px.
- **رخصة / license:** motion-kit uses GSAP (standard no-charge licence).
- **الدليل / proof:** `kosif-studio/motion/kit/motion-kit.js:548` · `kosif-one/tools/kosif-studio/motion/kit/motion-kit.js:548` · `kosif-studio/tests/test_studio.py:639` · `100-superskills/skills/kosif-montage-motion/references/craft-numbers.md`

#### RETRO-27 · تمريرة غليتش ثلاثية الأبعاد · Analysis-keyed 3D glitch pass · 🟢 جاهز / ready
- **ماذا / what:** تمريرة شيدر واحدة: فصل لوني، إزاحة شرائح، تمزق سالب، تجميد أحادي فضي، والتواء سرعة الشريط — مجزأة لكل إطار. — One shader pass: chroma split, band slice displacement, negative tear, cold-silver mono freeze, tape-speed warp, hashed per frame.
- **متى أستخدمها / when:** مشاهد Three.js وقت الضربات — 3D scenes on hits (3D, BEAT).
- **كيف / how:** const g = K3.makeGlitchPass(); composer.addPass(g); g.userData.set({chroma, slice, negative, mono, warp, frame}). 24 bands, slice shift ±0.06 on ~28% of bands, chroma 1.2% offset, warp .01; negative only for a few frames; mono = "time stopped". **أرقام / params:** 24 bands · ±0.06 on 28% · chroma 1.2%.
- **الدليل / proof:** `kosif-studio/motion/kit/three-kit.js:916` · `kosif-studio/motion/references/hyperframes-authoring.md`

#### RETRO-28 · كلمة غليتش RGB على النوتات · RGB-split glitch word on the beat · ✅ مُثبت هنا / proven here
- **ماذا / what:** الكلمة ثلاث نسخ أحمر/سماوي/أبيض بإزاحات عشوائية، مقطعة إلى شرائح أفقية، تعيد الانطلاق كل ثُمن نوتة. — The word in red/cyan/white copies with random offsets, sliced horizontally, retriggered on 1/8 notes.
- **متى أستخدمها / when:** ريلز موسيقى إلكترونية وعروض تقنية — electronic music reels.
- **كيف / how:** Offset 4–12 px, 6–10 slices, retrigger 234 ms (1/8 at 128 BPM); after hits: slices ≤24 px, RGB 4–6 px for 2–4 frames. ffmpeg equivalent on whole frames (ran here): rgbashift=rh=-6:bh=6. Beat-anchored primitives (HyperFrames music-to-video): chromatic-split on snare/glitch/surge 0.1–0.6 s, binary-decrypt on roll/build 0.8–2.5 s, pixel-dissolve on transition/hard_stop 0.5–1.5 s, datamosh-smear on glitch/transition 0.4–1.2 s; scan-band sweeps a wordmark once at 12° with red/cyan only inside the band; rgb-glitch-text subtle|standard|extreme. **أرقام / params:** offset 4–12 px · 6–10 slices · 234 ms.
- **الدليل / proof:** `style:pm-ghinaiya-nirmal-5d8fec` · `kosif-tool/styles/pm-micheleharmonic-77628e/BRIEF.md` · `kosif-one/vendor/hyperframes/skills/music-to-video/references/motion-primitive-catalog.md` · `kosif-one/vendor/hyperframes/registry/components/scan-band/scan-band.html`

## الثيمات المقفلة والأساليب الخاصة — Locked themes & special styles

_لوك كامل في فقرة واحدة تُلصق حرفيًا في كل أمر — فتبقى كل اللقطات من نفس العالم._

#### RETRO-29 · ثيمات التايب الحركي المقفلة (J، K، N، Q) · Locked kinetic themes: Brutalist Acid · Retro 70s · Paper Craft · Y2K Chrome · ✅ مُثبت هنا / proven here
- **ماذا / what:** أربعة لوكات مقفلة لأوامر Flow: خلفية، لون البطل، لون الصغير، الخامة، الطبقة، الحركة، الانتقال، بطاقة النهاية — تُكرر حرفيًا في كل مقطع. — Four locked looks for Flow clip prompts repeated verbatim in every clip.
- **متى أستخدمها / when:** سلسلة مقاطع مولدة بنفس العالم — generated clip series (GEN).
- **كيف / how:** kinetic-flow setup {"theme":"J|K|N|Q"} → STYLE LOCK paragraph. J Brutalist Acid: bg #BDBDB8, hero #C6FF00, small #0A0A0A, ultra-condensed heavy sans, chrome + black rubber, concrete grain, harsh top light. K Retro 70s Warm: bg #F3E3C3, hero #E8732C, small #5A3A22, rounded heavy retro serif, film grain, warm vignette, mustard sunburst. N Paper Craft Cutout: bg #F2EBDD, hero #D94032, small #1A1A1A, thick sans with a tiny cut-paper shadow, cardstock fibres, torn corners, stepped stop-motion. Q Y2K Chrome Iridescent: bg #E9ECF2, hero #141414, small #5A5F6E, wide heavy sans with iridescent outline, liquid chrome, lilac gradient. Lock presence is asserted by the Fastify tests (10/10 here). **أرقام / params:** J #C6FF00 · K #E8732C · N #D94032 · Q #141414.
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/kinetic-flow.mjs:13` · `fastify-motion-bro/scripts/profiles/kinetic-flow.mjs:20` · `fastify-motion-bro/tests/production-profiles.test.mjs`

#### RETRO-30 · لوفاي دافئ متكرر · Lo-fi / cozy loop · 📄 موصوف / documented only
- **ماذا / what:** مساء بنفسجي-أزرق مع أصفر دافئ وحبيبات؛ حلقة 4–8 ث لمطر وبخار ووميض مصباح وشخصية تتنفس. — Purple-blue evening with warm yellow and grain; a 4–8 s loop of rain, steam, lamp flicker, a breathing character.
- **متى أستخدمها / when:** خلفيات دراسة، موسيقى هادئة، أدعية مسائية — study/ambient loops.
- **كيف / how:** Palette #2B2D42 → #5C5470 with #F2C14E; Tajawal 500 for Arabic, Mulish/Karla for Latin; every motion 1–3 s, none faster than 0.8 s, no cuts; seamless loop rules in FMT. **أرقام / params:** 4–8 s loop · motions 1–3 s · ≥0.8 s.
- **الدليل / proof:** `100-superskills/skills/trend-animation-styles/references/styles.md`

#### RETRO-31 · بذور لوكات الريترو · Retro seed presets (vintage OS, arcade, neobrutalism, neon) · 📄 موصوف / documented only
- **ماذا / what:** رموز تصميم جاهزة: نظام التسعينيات، الأركيد، النيو بروتاليزم، النيون — تبدأ منها ثم تفحص التباين. — Ready token seeds for 90s OS, arcade, neobrutalism and neon; run WCAG checks.
- **متى أستخدمها / when:** لوك ريترو سريع لواجهة أو ريل — quick retro looks (UI, BRAND).
- **كيف / how:** Vintage 90s OS: #008080 teal, #C0C0C0 surface, #000 text, Silkscreen. Pac-arcade: #2A3FE5, #F4B9B0, black stage, Press Start 2P, dotted borders. Neobrutalism: #FDC800 / #432DD7 on #FBFBF9, scale 13/15/17/21/27/35. Neon: #BBF351 / #00BCFF. Pixel/Latin display fonts need an Arabic partner (e.g. Lalezar or Reem Kufi, ARAB-11).
- **الدليل / proof:** `kosif-atlas/skills/3593-bespoke-design-system/14409-bespoke-design-system/source-design-systems/vintage/DESIGN.md` · `kosif-atlas/skills/3593-bespoke-design-system/14409-bespoke-design-system/source-design-systems/pacman/DESIGN.md` · `kosif-atlas/skills/3593-bespoke-design-system/14409-bespoke-design-system/source-design-systems/neobrutalism/DESIGN.md`

## توليفات قوية / power combos

- **قصة «حياتك لعبة» / life-as-a-game reel:** RETRO-01 + RETRO-08 + RETRO-02 + STORY (مستويات) + BEAT (8-bit) — مستويات بخط بكسل، عملات تعدّ، ودخول بدثر Bayer.
- **فاصل ريترو داخل فيلم حديث / retro interlude:** RETRO-09 + TRANS (pixelize) + RETRO-16 — لقطة بكسل 320×180 ×6 ثم عودة للحاضر بخطوط مسح.
- **إعلان قديم ساخر / ironic infomercial:** RETRO-16 + RETRO-17 + ARAB (عنوان «اتصل الآن» بالعربية) + VOICE — شمس بنفسجية وشاشة VHS.
- **افتتاح تقني / dev intro:** RETRO-22 + RETRO-26 + RETRO-21 + TYPE — شعار يتكون من حروف ثم يتنظف مع لكمة غليتش 0.3 ث.
- **ريل موسيقى إلكترونية / electronic track reel:** RETRO-28 + BEAT (ثُمن النوتة) + RETRO-27 + GLOW — كلمة تتقطع على الإيقاع ومشهد ثلاثي يتجمد أحاديًا.
- **ملصق مطبوع متحرك / animated print poster:** RETRO-10 + RETRO-11 + TEX (ورق) + BRAND — عتبة هافتون تكشف الصورة وحبران ينطبقان.
- **سلسلة مقاطع مولدة بلوك ريترو / generated retro series:** RETRO-29 + STORY (lock blocks) + GEN — ثيم K السبعيني في كل أمر حرفيًا.

## أخطاء ممنوعة / never do

1. **لا تكبير بتنعيم (bilinear/bicubic) لمشهد بكسل** — يذوب البكسل؛ flags=neighbor وimage-rendering:pixelated (RETRO-01).
2. **لا مواضع كسرية** — جزء البكسل يرتعش ويضبب؛ Math.round على الشبكة المنطقية (RETRO-06).
3. **لا تلاشي بالشفافية أو تدرج ناعم داخل البكسل** — اكسر اللوك؛ تدرّج اللوحة أو Bayer (RETRO-02).
4. **لا دثر على عفريتات صغيرة ولا تظليل «وسادة»** — يصير ضجيجًا؛ إضاءة باتجاه واحد وسلالم ملونة (RETRO-03).
5. **لا غليتش أطول من ~0.4 ث ولا كخلفية دائمة** — يتعب العين ويفقد اللكمة؛ اربطه بحدث (RETRO-26).
6. **لا تقسيم الكلمة العربية إلى حروف من أجل الغليتش أو ASCII أو LED** — الحروف تنفصل؛ ارسم الكلمة مشكّلة ثم اقطع الصورة (ARAB-01).
7. **لا وميض أو مواريه أسرع من 3 Hz** — خطر على مرضى الصرع؛ قلّل التردد (RETRO-25).
8. **لا هافتون دقيق جدًا قبل اختبار الضغط** — يتحول إلى مواريه بعد H.264 (RETRO-10).
9. **لا تلف مزيف يغطي الوجوه أو يزوّر التواريخ** — في أفلام الذكريات (RETRO-12).
10. **لا أسود #000 خالص في لوك CRT الداكن** — استخدم #0A0A0A/#121212 (RETRO-21).

## أقوى 5 حركات توقيع / 5 signature moves

1. **RETRO-01 — مشهد بكسل 320×180 ×6:** أبسط وأصدق ريترو، مجرَّب هنا حتى الترميز.
2. **RETRO-02 — دخول بدثر Bayer:** أربع ألوان Game Boy وعتبة 4×4 بدل الشفافية.
3. **RETRO-22 — ASCII يتدقق حتى يُقرأ:** خشن ← ناعم في 1.4 ث لشعار أو كشف.
4. **RETRO-28 — كلمة غليتش على ثُمن النوتة:** 6–10 شرائح وإزاحة 4–12 بكسل.
5. **RETRO-29 — ثيم مقفل:** فقرة لوك واحدة تُلصق حرفيًا في كل مقطع مولد.

## إضافات v2 — v2 additions

_قدرات أُضيفت في الإصدار الثاني من حزم المالك (higgsfield-motion-saas وhiggsfield-motion-claude ومهارة المونتاج التحريرية وفيلم الأغنية وKOSIF SEE) ومن مهارات ECC (رخصة MIT)، مكتوبة بكلماتنا. ✅ هنا = شُغّلت في جلسة 2026-10-16 وسجلها في [external-skills.md](../external-skills.md)؛ مسارات `owner-upload:` تشير إلى أرشيفات المالك لا إلى هذا المستودع. — v2 additions from the owner's packages and ECC skills (MIT), in our own words; ✅ = run in this session, log in external-skills.md; `owner-upload:` paths point into the owner's archives, not this repo._

#### RETRO-X01 · شاشة LED نقطية وكلمات بكسل حقيقية · LED dot lattice bulge and true pixel words · 📄 موصوف / documented only
- **ماذا / what:** شاشة نقاط LED تنتفخ كعدسة مع حواف لونية على مستوى النقطة، وكلمات بكسل تُرسم من خرائط 5×7 حقيقية لا من خط بكسل مكبر. — An LED dot screen that bulges like a lens with per-dot colour fringes, and pixel words drawn from real 5×7 bitmaps rather than an enlarged pixel font.
- **متى أستخدمها / when:** مظهر لوحة إعلانات LED أو ألعاب قديمة — an LED billboard or retro-game look.
- **كيف / how:** Barrel bulge on a dot lattice with k 0.10–0.17: position × (1 + k·r²), dot size × (1 + 1.6k·r²); dot-level fringes #FF2A3C / #2A6BFF at α 0.55 with 'lighter' compositing. A pixel TTF at 540 px renders rounded corners: draw 5×7 bitmaps cell by cell instead. **أرقام / params:** k 0.10–0.17; size ×(1 + 1.6k r²); fringe α .55.
- **الرخصة / license:** owner (no LICENSE file)
- **المصدر / source:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/code-engine.md`
- **الدليل / proof:** `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/code-engine.md` · `owner-upload:motion-saas_skill/higgsfield-motion-saas/references/client-taste.md`
