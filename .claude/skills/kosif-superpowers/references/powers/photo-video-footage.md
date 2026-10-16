# الصور والفيديو الخام — Photos & footage

> فصل مُجمَّع آليًا من 200 ملاحظة حصاد (مستودعات KOSIF + أطلس المهارات + 253 فيديو مرجعي)، مدموجة إلى **197 قدرة** مرتبة من الأقوى دليلًا. لم يُحرَّر يدويًا بعد — تحقّق من الدليل قبل الادعاء.
> Auto-compiled chapter: 197 powers deduplicated by name from 200 harvested atoms; strongest evidence first.

**الحالة:** ✅ مُثبت هنا 17 · 🟢 جاهز 33 · 📦 بأمر تثبيت 64 · 🔑 مفتاح/خدمة 11 · 👁 شوهد في فيديو 11 · 📄 موصوف 59 · 💡 فكرة 2

#### FOOT-01 · مشغل المقدمة السينمائية المتكيف · Adaptive cinematic intro player · ✅ مُثبت هنا
- **ماذا / what:** An optional full-screen film overlay that picks 4K or 720p by viewport and network, falls back gracefully, and never blocks the real entry screen.
- **كيف / how:** 4K only if width>=1100px and effectiveType not slow-2g/2g/3g and not saveData; on error retry 720p once; poster fallback; failsafe close 14 s; close 950 ms after 'ended'; skip if seen this session, deep link, reduced motion, saveData or deviceMemory<=2; muted autoplay + sound toggle; focus trap Tab/Shift+Tab; Escape skips; shell.inert while open.
- **أرقام / params:** breakpoint 1100px; failsafe 14000ms; end hold 950ms; key kosif-earth-intro-seen-v1
- **الدليل / proof:** `kosif-earth-ci-fork/ui/art/brand/earth-intro-20261009.js` · `kosif-earth-ci-fork/unlock.html:151` · `kosif-earth-ci-fork/tools/brand_art.test.mjs`

#### FOOT-02 · شخصية مسطحة فوق خلفية واقعية · Flat figure over photoreal background (collage) · ✅ مُثبت هنا
- **ماذا / what:** Intentional collage: photoreal rooms/streets with lighting and depth while the stick figure stays flat and visibly distinct.
- **كيف / how:** BACKGROUNDS.real block + style note in output.
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/stickman.mjs:5,47`

#### FOOT-03 · لقطة السيارة البطولية · Automotive studio hero shot · ✅ مُثبت هنا
- **ماذا / what:** Prompt 1: photoreal ad image at premium 3/4 front low angle, 85 mm look at f/2.8, neutral studio, large softbox key front-left, thin right rim, soft floor reflection, whole car visible.
- **كيف / how:** Generated after brand/model/year/trim/colour confirmation; no invented trim.
- **أرقام / params:** 85 mm; f/2.8; key front-left; rim right
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/car-exploded.mjs:56`

#### FOOT-04 · مكتبة خطوات تحضير الطعام · Food assembly recipe library · ✅ مُثبت هنا
- **ماذا / what:** 19 five-step physical assembly sequences each paired with a specific foley sound (pizza, burger, donuts, fresh juice, soda, milkshake, tacos, candy, fries, fried chicken, hot dog, sandwich/sub, nachos, ramen, sushi roll, ice-cream sundae, chocolate cake/cupcake, iced coffee/latte, smoothie) plus dri…
- **كيف / how:** ACTIONS map + regex classification for unknown foods.
- **أرقام / params:** 19 recipes x 5 steps; menu of 20
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/food-flow.mjs:3-28,46-61`

#### FOOT-05 · أقفال مشهد الطعام · Food scene locks (chef/set/camera/pace) · ✅ مُثبت هنا
- **ماذا / what:** Same chef (medium-brown hands, ivory rolled sleeves, charcoal apron, silver wristband, face hidden until tasting), same warm stone kitchen with copper lamp, golden overhead practical + left softbox, 45° three-quarter 50 mm shallow-DOF tripod shot, no speech or music.
- **كيف / how:** chef/set/camera/pace constants in every prompt.
- **أرقام / params:** 45°; 50 mm; 10 s clips
- **الدليل / proof:** `fastify-motion-bro/scripts/profiles/food-flow.mjs:30-33`

#### FOOT-06 · كشف اللقطات · scenes shot detection · ✅ مُثبت هنا
- **ماذا / what:** scdet (fallback select=scene) boundaries, thumbnail sheet, split, timeline spec with cuts.
- **كيف / how:** python scripts/kmotion.py scenes CLIP.mp4 --sheet shots.png --timeline edit.json [--split --transition fade]
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md`

#### FOOT-07 · حماية الوجوه · privacy face blur · ✅ مُثبت هنا
- **ماذا / what:** Faces pixelated/blurred/boxed with tracking, margin, hold through misses; manual regions with time windows; YuNet>Haar>skin heuristic.
- **كيف / how:** python scripts/kmotion.py privacy CLIP.mp4 --out safe.mp4 --mode pixelate|blur|box --region x,y,w,h[,from,to]
- **أرقام / params:** YuNet model not shipped
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md`

#### FOOT-08 · كشف اللقطات وتحويلها إلى تايملاين · Scene/shot detection to timeline · ✅ مُثبت هنا
- **ماذا / what:** Cuts in a real video are detected into shots, a contact sheet is drawn and a timeline spec with transitions is generated.
- **كيف / how:** scenes.detect(clip, threshold=10, min_len=.5) → {scenes:[{start,end}]}; scenes.sheet(clip, rep, png); scenes.timeline_spec(clip, rep, 'fade').
- **أرقام / params:** test: 3 shots found at 2.0 s and 4.0 s ±0.15
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_v6.py:113`

#### FOOT-09 · مترجم تايملاين JSON · JSON timeline compiler (cuts, ramps, overlays) · ✅ مُثبت هنا
- **ماذا / what:** A JSON spec of clips, images and colour cards with in/out, zoom, grade, speed ramps and transitions, plus text, lower-third, logo, progress bar and caption overlays, compiles into one FFmpeg render with a QA gate.
- **كيف / how:** timeline.build(spec, out, workers, inspect) → report {seconds, transitions, audio, gate{lufs}}; ramp [[t, speed]…] → setpts with log(); atempo chain (0.25 → atempo=0.5,atempo=0.5); ratio '1:1' → 1080×1080; overlays text anim 'rise', box '#00000080', lower-third, image upper-right scale .5, progress #E7B65A 4 px, captions style 'tiktok'.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_v6.py:34` · `100-superskills/skills/kosif-montage-motion/tests/test_v6.py:64`

#### FOOT-10 · مونتاج صور وفيديو على الإيقاع مع ملاءمة ذكية · Mixed photo+video beat montage with smart fit · ✅ مُثبت هنا
- **ماذا / what:** A folder of clips and photos is cut to music; landscape media in 9:16 is shown whole over a blurred copy, same-shape media fills; *.edit.mp4 copies replace originals.
- **كيف / how:** montage.gather([dir]); montage._fit_chain(file, 1080, 1920) → 'split=2…' (blur background) or 'scale=…'; montage.cut([dir], music, out, ratio='9:16', punch=False).
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_fetch_lab.py:93`

#### FOOT-11 · مكتبة الوسائط المحلية مع الفحص · Local media library with probe · ✅ مُثبت هنا
- **ماذا / what:** Drag-and-drop upload of video/audio/image/caption files into workbench/media, each probed (duration, video, audio) and classified as video/audio/image/data; files can be deleted and their paths copied into recipes and timelines.
- **كيف / how:** POST /api/media (multipart 'file', streamed in 1 MB chunks, name collisions suffixed with a timestamp), GET /api/media, DELETE /api/media/NAME; probe via tools.probe(); index in workbench/media/.index.json; files served at /media/NAME.
- **أرقام / params:** accepted: .mp4 .mov .mkv .webm .avi .m4v .mp3 .wav .m4a .aac .flac .ogg .png .jpg .jpeg .webp .gif .json .txt .srt; ≤ 4 GB per file; names ≤ 150 chars
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:58` · `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:353` · `100-superskills/skills/kosif-montage-motion/tests/test_web.py:145`

#### FOOT-12 · تبويب التايملاين: محرر JSON مع شريط محسوب · Timeline tab: JSON editor with computed strip · ✅ مُثبت هنا
- **ماذا / what:** Edit a timeline spec as JSON, validate it on the server, see a strip of clips (with speed/ramp badges), transition markers and overlay bars, save it under workbench/timelines, render it with the delivery gate, ask Claude, or import a KOSIF Studio project.
- **كيف / how:** POST /api/timeline/validate {spec} → timeline.summary(); /api/timeline/save, /list, /NAME, /example; render = save + job recipe 'timeline' with --inspect 1; drawStrip() in app.js positions blocks by seconds.
- **أرقام / params:** info line: seconds · size · fps · clips · transitions · overlays
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:511` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/app.js:158` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/app.js:176`

#### FOOT-13 · استيراد مشروع Studio إلى تايملاين · Studio project → timeline import · ✅ مُثبت هنا
- **ماذا / what:** Converts a KOSIF Studio browser project (.kosif.json) into a full timeline spec for the FFmpeg pipeline, matching media by name in the library (or a named folder) and returning a mapping report.
- **كيف / how:** POST /api/studio/import {project, name?, media_dir?, size?} → studio_import.convert(); or recipe studio-import (project, --out out/studio.json, --media DIR, --render out/studio.mp4); timeline tab button «استيراد مشروع Studio».
- **أرقام / params:** saved under workbench/timelines/NAME.json
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:528` · `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:42` · `100-superskills/skills/kosif-montage-motion/tests/test_web.py:250`

#### FOOT-14 · محرر KOSIF Studio في المتصفح · KOSIF Studio browser montage editor · ✅ مُثبت هنا
- **ماذا / what:** A local, upload-free browser editor: import video/images/audio, arrange scenes on a timeline, add text and shape layers with animations, a soundtrack, undo/redo, project save/open, live preview and two export paths.
- **كيف / how:** Serve the site and open /studio/ (or build the one-page Studio Cloud artifact). Library | preview canvas | inspector | timeline with tracks المشاهد / الطبقات / الصوت.
- **أرقام / params:** limits: 60 s project, 24 clips, 24 overlays, 48 assets, 200 MB per file, 500 MB total, project JSON ≤ 1 MB; canvas 1280×720 / 720×1280 / 720×720
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/index.html` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:1` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/model.mjs:1`

#### FOOT-15 · تحرير اللقطات · Clip editing: trim, duration, volume, reorder, duplicate · ✅ مُثبت هنا
- **ماذا / what:** Each scene clip can be trimmed inside its source, given a duration, have its own sound level, be moved earlier/later, duplicated or deleted; scenes play back to back without overlap.
- **كيف / how:** Inspector for selected clip; transaction() snapshots for undo; sanitizeProject() clamps trim to source duration − 0.1 s and the total to 60 s.
- **أرقام / params:** duration ≥ 0.1 s; volume 0–1; images default 5 s
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:46` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/model.mjs:13`

#### FOOT-16 · إعادة التلوين مع حفظ الظلال · recolor (keeps shading) · ✅ مُثبت هنا
- **ماذا / what:** Changes one colour into another inside an optional region while keeping the folds, shadows and highlights of the original by scaling HSV saturation and value.
- **كيف / how:** recolor(img, src_hex, dst_hex, tolerance=40, region=(x0,y0,x1,y1), keep_shading=True) via color_mask (soft 1.5 blur).
- **أرقام / params:** local edits use tolerance 34; example tolerance 42
- **الدليل / proof:** `kosif-studio/edit_pack.py:36` · `kosif-studio/edit_pack.py:50` · `kosif-studio/tests/test_studio.py:410`

#### FOOT-17 · أوامر تبديل الألوان محلياً بالعربية والإنجليزية · Local colour-swap commands in Arabic and English (no AI) · ✅ مُثبت هنا
- **ماذا / what:** Understands 'غيّر الذهبي إلى الأزرق' / 'make the gold blue' including ال, tanween and feminine forms, finds the nearest colour layer and writes recolor lines for its biggest parts instantly.
- **كيف / how:** edit_pack.parse_colour_request(text) -> (src_hex, dst_hex); local_edit(path, text) picks layer by weighted HSV distance; Studio 🧩 uses it before asking an AI.
- **أرقام / params:** 18 named colours (أحمر #d62828, أزرق #2f6fd6, أخضر #2e9e5b, أصفر #f2c94c, ذهبي #d4a53a, برتقالي #f08a24, بني #7a4b2a, وردي #f06aa8, بنفسجي #7a4fd1, رمادي #8a8a8a, أسود #111111, أبيض #f5f5f5, سماوي #2fb8d6, فضي #c0c0c0, بيج #e8d9b5, زيتي #7f8c2a, كحلي #1f2d6b, عنابي #7b1e2b); HSV match limit .6; up t…
- **الدليل / proof:** `kosif-studio/edit_pack.py:226` · `kosif-studio/edit_pack.py:260` · `kosif-studio/edit_pack.py:285`

#### FOOT-18 · إزالة الترجمة المحروقة · decaption · 🟢 جاهز
- **ماذا / what:** Erase burned-in captions and a fixed credit line.
- **كيف / how:** python scripts/kmotion.py decaption CLIP.mp4 --out CLEAN.mp4
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md` · `100-superskills/skills/kosif-montage-motion/scripts/decaption.py`

#### FOOT-19 · تثبيت الفيديو · stabilize · 🟢 جاهز
- **ماذا / what:** vidstab 2-pass when built in, else deshake.
- **كيف / how:** python scripts/kmotion.py stabilize CLIP.mp4 --out steady.mp4
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md` · `kosif-studio/motion/tools.py:303`

#### FOOT-20 · قص دقيق بالإطار · Frame-accurate trim · 🟢 جاهز
- **ماذا / what:** Cuts a part of a clip by seconds with re-encode for accuracy.
- **كيف / how:** python tools.py trim CLIP --from 3.2 --to 9.8 --out part.mp4
- **أرقام / params:** crf 18 yuv420p, AAC 192k 48 kHz
- **الدليل / proof:** `kosif-studio/motion/tools.py:247` · `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:82`

#### FOOT-21 · تقديم اللقطات الخام والملء العمودي · Presenting raw screenshots and vertical fills · 🟢 جاهز
- **ماذا / what:** Never show a raw screenshot: give it rounded corners, shadow and a designed background or device/browser frame; for 9:16 place the whole landscape frame over a blurred enlarged copy rather than a centre crop that hides the action.
- **كيف / how:** CSS frame or ffmpeg: split -> scale+boxblur background -> overlay centred foreground.
- **أرقام / params:** radius 12-16px; 9:16 = 1080x1920 whole frame over blurred fill
- **الدليل / proof:** `kosif-atlas/skills/166-demo-video/535-demo-video` · `kosif-atlas/skills/1511-homie/3903-video` · `kosif-atlas/skills/1511-homie/3903-video/references/DELIVERY.md`

#### FOOT-22 · معالجة الصور المولدة بـ ImageMagick · ImageMagick post-processing of generated stills · 🟢 جاهز
- **ماذا / what:** Crop, cut out, convert and grade generated images locally before animating them.
- **كيف / how:** Fill-crop: -resize WxH^ -gravity center -extent WxH; white-to-alpha: -fuzz 10% -transparent white then -channel A -blur 0x1 -level 50%,100%; -trim +repage; WebP -quality 85; warm grade -modulate 100,110,105; contrast -contrast-stretch 2%x1%. Here the binary is 'convert' (IM6), not 'magick'.
- **أرقام / params:** fuzz 10-15%; q85
- **الدليل / proof:** `kosif-atlas/skills/881-codex-seo/1954-seo-image-gen`

#### FOOT-23 · خلفية صورة المكتب المشمس · Sunlit office photo backdrop · 🟢 جاهز
- **ماذا / what:** Real daylight meeting-room photo used full-bleed behind the EARTH door with green-tinted translucent gradients (no full-image tint).
- **كيف / how:** background: linear-gradient(135deg,rgba(7,33,27,.16),rgba(250,249,242,.35)), url(earth-office-sunlit-4k.webp) center/cover fixed; mobile swaps to 1600x1200 file with scroll attachment.
- **أرقام / params:** 4k webp 1.6 MB; mobile 1600x1200 265 KB
- **الدليل / proof:** `kosif-earth-ci-fork/ui/art/brand/earth-office-sunlit-4k.webp` · `kosif-earth-ci-fork/ui/art/brand/earth-office-sunlit-mobile.webp` · `kosif-earth-ci-fork/ui/art/brand/earth-office-door.css`

#### FOOT-24 · قص الصمت · silence jump-cut · 🟢 جاهز
- **ماذا / what:** Remove pauses picture+sound in one pass.
- **كيف / how:** python scripts/kmotion.py silence CLIP.mp4 --out cut.mp4 --threshold -35 --min 0.45 --pad 0.08
- **أرقام / params:** −35 dB, 0.45 s, 0.08 s pad
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md`

#### FOOT-25 · قص ودمج وتكرار · trim / concat / loop · 🟢 جاهز
- **ماذا / what:** Trim range; concat with unified sizes/rates and silent padding; loop with tail dissolving into head.
- **كيف / how:** python scripts/kmotion.py trim --from --to; concat a b; loop --seconds 30
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md`

#### FOOT-26 · لقطة كل الإطارات مفتاحية · All-intra footage plate · 🟢 جاهز
- **ماذا / what:** Convert clip so composition seeks frame-exactly via <video data-start>.
- **كيف / how:** python scripts/kmotion.py footage CLIP
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md`

#### FOOT-27 · مقاطع فيديو داخل التكوين · Footage clips in compositions · 🟢 جاهز
- **ماذا / what:** Real video clips placed on the timeline with data-start/data-duration are shown only in their span and sought frame-accurately.
- **كيف / how:** <video data-start data-duration muted> (convert to all-intra with motion.py footage) inside the page; shim seeks currentTime = t - start.
- **أرقام / params:** visibility hidden outside span; tolerance 0.5 ms
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:474` · `100-superskills/skills/kosif-montage-motion/scripts/motion.py:548`

#### FOOT-28 · تحليل فيديو مرجعي · Video breakdown analyze · 🟢 جاهز
- **ماذا / what:** Beats ≤3s, per-beat hex palette, motion energy, pan, transition guess, loudness, tempo, onsets.
- **كيف / how:** kmotion analyze VIDEO --max-beat 3.0 [--transcribe] [--batch DIR]
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/analyze.py`

#### FOOT-29 · قص ودمج وتثبيت · Trim/concat/stabilize · 🟢 جاهز
- **ماذا / what:** Frame-accurate trim, fitted concat, vidstab stabilize.
- **كيف / how:** tools.py trim|concat|stabilize
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/tools.py`

#### FOOT-30 · كشف اللقطات · Scene detection · 🟢 جاهز
- **ماذا / what:** FFmpeg scdet shot list, sheet, split, timeline spec.
- **كيف / how:** scenes.py CLIP --threshold 10 --min 0.5 [--sheet|--split|--timeline --transition fade]
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/scenes.py`

#### FOOT-31 · إخفاء الوجوه · Face privacy · 🟢 جاهز
- **ماذا / what:** Tracked pixelate/blur/box of faces or regions, timed.
- **كيف / how:** privacy.py CLIP --mode pixelate --strength 18 --pad 0.25 --every 2 --hold 0.6
- **أرقام / params:** detectors yunet>haar>skin
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/privacy.py` · `100-superskills/skills/kosif-montage-motion/scripts/faces.py`

#### FOOT-32 · مثال مواصفة التايملاين · Timeline spec example (clips, ramps, overlays, ducked music) · 🟢 جاهز
- **ماذا / what:** The built-in example shows the full vocabulary a timeline accepts: trimmed clips with Ken-Burns zoom and grades, a speed ramp, a still with zoom, a colour card, a rising Arabic title on a translucent box, a lower-third, a progress bar and music ducked under clip audio at −14 LUFS.
- **كيف / how:** GET /api/timeline/example (timeline.EXAMPLE); kmotion timeline --example edit.json.
- **أرقام / params:** ratio 9:16, fps 30, bg #0d1b2a; clip_a in 0 out 4 zoom 1.0→1.08 grade teal_orange transition circleopen 0.6 s; clip_b in 2 out 7 ramp [[0,1.0],[2.0,0.3],[4.0,1.0]] transition slideup; photo 3 s zoom 1.0→1.15 fadeblack 0.8 s; color #000000 0.8 s; text size 110 anim rise box #00000080 0.4–3.4 s; lower…
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:896` · `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:578`

#### FOOT-33 · تحليل التعريض والمفتاح النغمي للصورة · Image exposure and tonal-key analysis · 🟢 جاهز
- **ماذا / what:** Measures luma percentiles, used dynamic range, contrast, clipped highlights and crushed shadows, shadow/mid/highlight zones, high/mid/low-key and an exposure verdict for a still or a frame.
- **كيف / how:** python3 scripts/omni/image_analyze.py IMAGE [--summary]; image EXIF-transposed and downscaled to 1600 px max side; Rec.709 luma.
- **أرقام / params:** clip high = any channel ≥ 250; crushed = luma ≤ 5; overexposed if mean > 185 or clipped > 5%; underexposed if mean < 60 or crushed > 15%; zones <85, 85–170, ≥170; verified on cat.gif: overexposed high-key, mean 226.2
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/omni/image_analyze.py:120`

#### FOOT-34 · اقتراحات إصلاح الصورة بالعربية · Image fix suggestions in Arabic · 🟢 جاهز
- **ماذا / what:** Arabic advice from the measurements: lower exposure for burnt areas, lift shadows, widen tonal range, sharpen/focus, denoise, correct a colour cast, recrop onto a thirds point.
- **كيف / how:** suggest(report), summary_ar(report) with --summary.
- **أرقام / params:** clipped > 2%, crushed > 10%, dynamic range < 120, not sharp, noisy, cast ≠ neutral, off-grid
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/omni/image_analyze.py:207` · `100-superskills/skills/kosif-montage-motion/scripts/omni/image_analyze.py:243`

#### FOOT-35 · خطة الغربة ٢ ومراجعة المقاطع · Ghorba v2 clip pool review (style plan) · 🟢 جاهز
- **ماذا / what:** Second pass on the exile theme: a pool of 22 clips across six song sections (s00-s05) reviewed on a 32-slot contact sheet; no render script yet, so the look is the same muted vertical realism planned for the full song.
- **كيف / how:** make_contact.py grabs frame at 2 s per clip into an 8x4 sheet (192x342 cells, bg #11121b) and writes clip_manifest.json.
- **أرقام / params:** 22 clips listed; sections s00-s05
- **الدليل / proof:** `kosif-one/projects/ghorba-motion-v2/make_contact.py` · `kosif-one/projects/ghorba-motion-v2/clip_manifest.json`

#### FOOT-36 · مقاطع فيديو قابلة للتقديم بدقة · Seekable all-intra footage clips · 🟢 جاهز
- **ماذا / what:** Re-encodes a clip as all-intra so a composition's <video data-start> can be sought frame-exactly while rendering.
- **كيف / how:** python motion.py footage CLIP.mp4 --out projects/X/assets/clip.mp4 [--from 0 --dur 5 --width 1280 --fps 30].
- **أرقام / params:** width 1280, 30 fps
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/motion.py:496` · `kosif-one/tools/kosif-studio/motion/qa.py`

#### FOOT-37 · اختيار أنشط جزء من اللقطة · Motion-energy shot picking · 🟢 جاهز
- **ماذا / what:** For each slot the most active unused window of the next clip is chosen by frame-difference energy.
- **كيف / how:** montage.energy(clip, fps=6) + montage.pick(...).
- **أرقام / params:** energy sampled at 6 fps
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/montage.py:105` · `kosif-one/tools/kosif-studio/motion/montage.py:115`

#### FOOT-38 · ترميم اللقطات · Footage restoration chain · 🟢 جاهز
- **ماذا / what:** Temporal denoise, Lanczos reframe, cleaner blacks, highlight roll-off, warmer mids and contrast-adaptive sharpening.
- **كيف / how:** FFmpeg hqdn3d=1.2:1.2:3:3,scale..:flags=lanczos,eq=contrast=1.12:brightness=-0.015:saturation=1.07:gamma=0.97,curves=...,colorbalance=...,cas=0.3.
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/reel.py:35`

#### FOOT-39 · قص ودمج دقيق · Frame-accurate trim and concat · 🟢 جاهز
- **ماذا / what:** Trim by seconds and join clips of different sizes fitted to one size/fps.
- **كيف / how:** python tools.py trim CLIP --from 3.2 --to 9.8 --out p.mp4; tools.py concat A B ... --out all.mp4 [--size 1080x1920 --fps 30].
- **أرقام / params:** H.264 crf 18 preset medium + 48 kHz AAC
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/tools.py:1`

#### FOOT-40 · تثبيت اللقطات · Stabilise footage · 🟢 جاهز
- **ماذا / what:** Two-pass vidstab stabilisation, or deshake when vidstab is missing.
- **كيف / how:** python tools.py stabilize CLIP --out steady.mp4 [--strength 10].
- **أرقام / params:** strength 10 (vidstab present here)
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/tools.py:1`

#### FOOT-41 · تعديل الصورة وتغيير الألوان · Picture edit loop with local recolour · 🟢 جاهز
- **ماذا / what:** Describes a picture's colour layers and writes a keyed Pillow edit program; 'change A to B' (Arabic or English) recolours locally keeping shading; other edits go to Claude.
- **كيف / how:** python edit_pack.py photo.jpg 'make the shirt red'; tools recolor, adjust, tint, paint, write, erase, flip, draw; original kept as <<KOSIF:ORIGINAL:...>> key.
- **الدليل / proof:** `kosif-one/tools/kosif-studio/edit_pack.py` · `kosif-one/tools/kosif-studio/README.md`

#### FOOT-42 · ضبط السطوع والتباين والتشبع والحدة · adjust (brightness, contrast, saturation, sharpness) · 🟢 جاهز
- **ماذا / what:** ImageEnhance-based adjustment of a region.
- **كيف / how:** adjust(img, region, brightness, contrast, saturation, sharpness).
- **أرقام / params:** 1.0 = unchanged
- **الدليل / proof:** `kosif-studio/edit_pack.py:65`

#### FOOT-43 · صبغ بلون · tint wash · 🟢 جاهز
- **ماذا / what:** Blends a region toward a colour.
- **كيف / how:** tint(img, hex, amount=.3, region).
- **أرقام / params:** amount 0..1
- **الدليل / proof:** `kosif-studio/edit_pack.py:76`

#### FOOT-44 · رسم مضلع وكتابة نص · paint polygon and write text · 🟢 جاهز
- **ماذا / what:** Draws a filled polygon or writes Latin text (custom font file for other scripts) onto the picture.
- **كيف / how:** paint(img, [(x,y)...], hex, outline, width); write(img, text, xy, size=32, hex, font_file).
- **أرقام / params:** write defaults to arial.ttf then Pillow default
- **الدليل / proof:** `kosif-studio/edit_pack.py:83` · `kosif-studio/edit_pack.py:88`

#### FOOT-45 · إزالة عنصر صغير · erase (blur-fill removal) · 🟢 جاهز
- **ماذا / what:** Removes something small by filling the region with its blurred surroundings through a feathered mask.
- **كيف / how:** erase(img, region, softness=14).
- **أرقام / params:** pad = 3*softness; mask blur softness/2
- **الدليل / proof:** `kosif-studio/edit_pack.py:98`

#### FOOT-46 · قلب الصورة · flip / mirror · 🟢 جاهز
- **ماذا / what:** Mirrors the whole picture horizontally or vertically.
- **كيف / how:** flip(img, horizontal=True).
- **الدليل / proof:** `kosif-studio/edit_pack.py:110`

#### FOOT-47 · قناع نطاق لوني · Colour-range mask · 🟢 جاهز
- **ماذا / what:** Soft mask of pixels close to a colour within an optional box — the selection behind recolor.
- **كيف / how:** color_mask(img, hex, tolerance=40, region, soft=1.5).
- **أرقام / params:** distance = ((r+g)/2 + b)/1.5 style weighted channel average
- **الدليل / proof:** `kosif-studio/edit_pack.py:36`

#### FOOT-48 · تجهيز لقطة حقيقية قابلة للبحث · All-intra footage prep for compositions · 🟢 جاهز
- **ماذا / what:** Re-encodes a clip so every frame is a keyframe, letting a <video> inside a composition be sought frame-exactly; prints the tag to paste.
- **كيف / how:** python motion.py footage CLIP --out projects/X/assets/clip.mp4 [--from 0 --dur 5 --width 1280 --fps 30]
- **أرقام / params:** libx264 -g 1 crf 16 preset medium, lanczos scale, muted, yuv420p, +faststart
- **الدليل / proof:** `kosif-studio/motion/motion.py:496` · `kosif-studio/motion/qa.py:423`

#### FOOT-49 · دمج مقاطع مختلفة الأحجام · Fit-and-join concat · 🟢 جاهز
- **ماذا / what:** Joins clips in order, fitting each inside one frame size with letterbox and filling silent clips with silence so audio never breaks.
- **كيف / how:** python tools.py concat A.mp4 B.mp4 --out all.mp4 [--size 1080x1920 --fps 30]
- **أرقام / params:** pad black; anullsrc 48 kHz stereo
- **الدليل / proof:** `kosif-studio/motion/tools.py:256`

#### FOOT-50 · مكوّن بارالاكس للصور · ParallaxPhoto component (Remotion + Canvas) · 🟢 جاهز
- **ماذا / what:** One camera function (pan + drift + linear zoom) multiplied by layer depth, in Remotion and Canvas seek versions.
- **كيف / how:** Remotion Img+staticFile; Canvas window.__kosifReady loads layers then exposes seek.
- **أرقام / params:** 1080×1920, 5 s, bg #0b0b0d
- **الدليل / proof:** `kosif-tool/playbooks/photos.md:103-185`

#### FOOT-51 · مونتاج مستقل أو متتابع · Clip editing: independent vs ripple · 📦 بأمر تثبيت
- **ماذا / what:** Two timeline models for cutting footage in code: absolutely placed clips (gaps/overlaps allowed) or ripple sequences where changing one clip shifts all later ones.
- **كيف / how:** Independent: each <Video from trimBefore durationInFrames> hardcoded; ripple: <TransitionSeries> of <TransitionSeries.Sequence durationInFrames> wrapping <Video trimBefore>.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10436-remotion-markup/video-editing.md`

#### FOOT-52 · فيديو ولوتي داخل التكوين · Video and Lottie inside HTML compositions · 📦 بأمر تثبيت
- **ماذا / what:** Embed footage (muted, playsinline, object-fit cover in a rounded frame) and Lottie vector animations (dotlottie-player or lottie-web with autoplay false for seeking) inside the timeline.
- **كيف / how:** For deterministic renders seek video.currentTime and lottie goToAndStop(frame) from the master clock; lottie-web from npm/CDN.
- **أرقام / params:** frame 680x840 radius 16 example; lottie pop scale 0.3->1 0.35s back.out(1.6)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md`

#### FOOT-53 · خط حماية الخصوصية لصانع محتوى بلا وجه · Faceless-creator privacy pipeline · 📦 بأمر تثبيت
- **ماذا / what:** For faceless channels the speaker's face never appears: clips where the face is identifiable are used for audio only; frames are sampled at 1 s and run through face detection; bystander faces are masked or the shot is swapped.
- **كيف / how:** ffmpeg fps=1 frame dumps + an OpenCV/mediapipe face detector (needs install) or manual review; blur/mosaic masks via ffmpeg boxblur on tracked boxes.
- **أرقام / params:** sample 1 frame/s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2451-davinciresolve-beats-devtalk/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2460-davinciresolve-story-devtalk/SKILL.md`

#### FOOT-54 · أدوات الرؤية الحاسوبية للمونتاج · Vision toolbox for editing · 📦 بأمر تثبيت
- **ماذا / what:** Detection/tracking (YOLO family) for auto-reframe, tracked callouts and face blur; promptable segmentation (SAM) for roto mattes; CLIP embeddings for text search over footage; transfer-learn rather than train from scratch; real-time budget at 30 fps is ~33 ms per frame - profile decode/copy, not onl…
- **كيف / how:** pip install ultralytics / segment-anything / open_clip (needs install + model downloads); batch-process extracted frames offline, then feed coordinates/mattes into ffmpeg or KOSIF overlays.
- **أرقام / params:** 30 fps ~= 33 ms/frame
- **تثبيت / install:** `pip install ultralytics / segment-anything / open_clip (needs install + model downloads)`
- **الدليل / proof:** `kosif-atlas/skills/2259-computer-vision-engineering/8608-cv-model-training-and-evaluation/SKILL.md` · `kosif-atlas/skills/2259-computer-vision-engineering/8611-vision-inference-optimization/SKILL.md` · `kosif-atlas/skills/1441-ultralytics-dev/3441-ultralytics-platform/SKILL.md`

#### FOOT-55 · مكتبة وسائط ذاتية الاستضافة مع بحث ذكي · Self-hosted media library with AI search · 📦 بأمر تثبيت
- **ماذا / what:** Immich indexes photos and videos with CLIP smart search, face clustering and OCR; existing folders can be mounted read-only as external libraries; API key via x-api-key header; web UI on port 2283, ML service on 3003.
- **كيف / how:** docker compose up (needs install; not available here); query its REST API to find shots by text before editing.
- **أرقام / params:** port 2283
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/3631-immich/14704-immich/SKILL.md`

#### FOOT-56 · تايملاين زمني متعدد الكاميرات · Chronological multi-camera timeline · 📦 بأمر تثبيت
- **ماذا / what:** Build the base edit by sorting all clips on recorded time, correcting per-camera clock offsets measured from one pair of clips of the same moment; pick timeline fps as the most common clip fps.
- **كيف / how:** Read Date Recorded / Date Created metadata (Resolve clip properties or ffprobe creation_time / exiftool), --offset prefix=seconds; dry-run table of file, time, camera, resolution, fps, gamma
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2443-akbun-davinciresolve-timeline-chrono/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2445-akbun-davinciresolve-workflow/SKILL.md`

#### FOOT-57 · قص البدايات المعيبة حسب الجهاز · Device-aware bad-head trimming · 📦 بأمر تثبيت
- **ماذا / what:** Phone clips often start with ~1 s of white/out-of-focus frames while exposure settles. Compare the first 2 s against a reference window 2-5 s in: trim until mean luma is within ±20% and focus (Laplacian variance) recovers; skip clips <5 s; gimbal cameras need no trim.
- **كيف / how:** ffmpeg extract frames; numpy/OpenCV Laplacian variance (cv2 not installed -> pip install opencv-python-headless) or ffmpeg signalstats YAVG
- **أرقام / params:** ref window 2-5 s; ±20% luma
- **تثبيت / install:** `pip install opencv-python-headless) or ffmpeg signalstats YAVG ref window 2-5 s`
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2454-davinciresolve-cut-travelflow/SKILL.md`

#### FOOT-58 · تمويه الوجوه للخصوصية · Face privacy mosaic · 📦 بأمر تثبيت
- **ماذا / what:** Blur/mosaic bystander faces: detect on start/middle/end frames (+every 5 s if >10 s) at full resolution, treat faces ≥40 px tall at 4K as identifiable, cover the whole region faces pass through with one soft window (softness ≥30% of window), block size ≈ 1/4 of the smallest face height; split nodes …
- **كيف / how:** OpenCV YuNet cv2.FaceDetectorYN (needs install + model) -> Resolve Power Window + Mosaic Blur 0.4; ffmpeg alternative: crop region -> pixelize/boxblur -> overlay, or avgblur in a feathered mask via alphamerge.
- **أرقام / params:** face ≥40 px; softness ≥30%; block = face/4; strength 0.4
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2456-davinciresolve-face-mosaic/SKILL.md` · `kosif-atlas/skills/1096-akbun-editvideo/2457-davinciresolve-face-privacy/SKILL.md`

#### FOOT-59 · استخراج الرسوم المتميزة من فيديو · Distinct-drawing extraction from a clip · 📦 بأمر تثبيت
- **ماذا / what:** Collapse a video into unique drawings by treating frames with few changed pixels as repeats, rather than mean-diff dedup.
- **كيف / how:** Grayscale (RGB2GRAY), threshold midway between ink and paper gray modes; repeat test = few pixels changed by a large gray step; store [k, pts, t1] index. Implementable with ffmpeg + numpy/opencv.
- **أرقام / params:** threshold T=(ink_mode+paper_mode)/2 e.g. 125.5
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2414-animation/9357-rotoscope`

#### FOOT-60 · وصفات رفع الدقة · Upscaling recipes (latent, ESRGAN, tiled) · 📦 بأمر تثبيت
- **ماذا / what:** Raise resolution of generated stills with the best quality per VRAM.
- **كيف / how:** Three-stage: generate → 2× model upscale (4x-UltraSharp, RealESRGAN_x4plus, anime_6B for illustration) → VAEEncode → KSampler denoise 0.35 → FaceDetailer; latent second pass denoise 0.35-0.5 (0.2-0.3 minimal, 0.65+ reworks); UltimateSDUpscale tiles 512 (SD1.5)/1024 (SDXL) with 32-64 px padding.
- **أرقام / params:** denoise 0.35-0.5; tile 512/1024; padding 32-64
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/2819-comfyui/11445-comfyui-workflow-design`

#### FOOT-61 · نماذج رؤية محلية عبر Transformers.js · Local in-browser/Node vision models (Transformers.js) · 📦 بأمر تثبيت
- **ماذا / what:** Run segmentation and depth-estimation models in JavaScript without an API key, e.g. to cut subjects out of a generated plate or build a depth map for 2.5D parallax.
- **كيف / how:** npm @huggingface/transformers; pipeline('image-segmentation') or pipeline('depth-estimation'); dtype q4/q8/fp16/fp32; device 'webgpu' in browsers, CPU in Node; models download from the Hub on first use.
- **أرقام / params:** dtype q4|q8|fp16|fp32
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-atlas/skills/1514-huggingface-skills/3946-transformers-js`

#### FOOT-62 · خلفية صورة أو فيديو · Picture/video backgrounds with dim and blur · 📦 بأمر تثبيت
- **ماذا / what:** Any image or looping muted video becomes the backdrop behind audio-only clips, films or a keyed-out speaker.
- **كيف / how:** drawBG(): cover fit, blur(b*m/100 px) scaled 1.1, images get a slow 5% breathing zoom, dim black overlay; video synced as t%duration.
- **أرقام / params:** dim 0-0.8; blur 0-6
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:2443` · `app/public/js/00_editor.js:2456`

#### FOOT-63 · مونتاج تلقائي للقطات على الإيقاع · Automatic beat montage of uploaded clips · 📦 بأمر تثبيت
- **ماذا / what:** Edits up to 24 clips/photos into a montage: studies every clip, lets the AI order them from a numbered contact sheet, cuts on the beat with camera moves, transitions and SFX.
- **كيف / how:** MON.run: MON.probe per clip (samples every clamp(D/30,0.5,2) s: motion, sharpness, brightness; internal cuts where motion > 45; 192 px thumb) in parallel batches of 3; MON.sheet 4-column numbered contact sheet; AI decides order, hook title, 0-6 lines, pace and grade; MON.lengths from pace or a reference fingerprint, snapped to beats within 0.4 s; MON.bestWindow picks lively, sharp, well-lit windows away from cuts and reuse; MON.assign round-robin; cuts -> S.cuts with zoom.sync 'ai'; camera from …
- **أرقام / params:** <= 24 clips; target 4-180 s (default min(avail,30))
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:1865` · `app/public/js/10_studio.js:2036` · `app/public/js/10_studio.js:2069`

#### FOOT-64 · ريلز من فيديو طويل · Reels from a long video · 📦 بأمر تثبيت
- **ماذا / what:** Cuts 1-8 vertical reels out of a long talk: transcribe, choose self-contained hook-to-payoff highlights ending on full sentences, then build each with captions, a title hook, talking-head camera, cleaned speech and a quiet bed.
- **كيف / how:** REELS.find({count,length}): count default 5 (>600 s), 3 (>180 s) else 2, max 8; length 15-75 s default 40; AI picks from a timed transcript (<= 24000 chars); local fallback REELS.local scores windows by words/second snapped to sentences (sentences break on .!؟?… or > 9 s).
- **أرقام / params:** 1-8 reels; 15-75 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/10_studio.js:4017` · `app/public/js/10_studio.js:4032` · `app/public/js/10_studio.js:4039`

#### FOOT-65 · إزالة الخلفية السادة أو الخضرا · Chroma key (any backdrop colour) · 📦 بأمر تثبيت
- **ماذا / what:** Keys out a plain or green backdrop behind a speaker and composites them over a new background.
- **كيف / how:** chromaMask(): 240 px wide probe, YCbCr chroma distance /128 + luma term (0.9 weight for neutral keys, 0.2 otherwise), soft edge between 0.55*tol and tol with smoothstep; mask blurred W/360 px and used with source-in; pickKey samples four 8x8 corner patches of a 64x64 frame.
- **أرقام / params:** key default #00b140; tol 0.05-0.6 (default 0.22)
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:2468` · `app/public/js/00_editor.js:2494` · `app/public/js/00_editor.js:2505`

#### FOOT-66 · عزل الشخص بالذكاء المحلي · Person segmentation cut-out (MediaPipe) · 📦 بأمر تثبيت
- **ماذا / what:** Isolates the person with MediaPipe Selfie Segmentation and places them over any background.
- **كيف / how:** loadSeg(): script from cdn.jsdelivr.net @mediapipe/selfie_segmentation@0.1.1675465747, modelSelection 1, 20 s init timeout; segFrame per frame (awaited per frame in HQ render).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:2466` · `app/public/js/00_editor.js:2478`

#### FOOT-67 · إزالة خلفية الصورة · Image background removal by edge flood fill · 📦 بأمر تثبيت
- **ماذا / what:** Makes a single-colour backdrop of a logo/product picture transparent.
- **كيف / how:** removeImgBG(): scale to <= 1100 px, corner colours must agree (spread <= 70) else refuse; flood fill from all edges with tolerance 46+0.5*spread; anti-alias edge pixels to alpha <= 150; exported PNG replaces the layer.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/public/js/00_editor.js:2572`

#### FOOT-68 · جلب الوسائط من اللينكات وبنترست · Link and Pinterest media fetch · 📦 بأمر تثبيت
- **ماذا / what:** Downloads videos/images from links (yt-dlp, gallery-dl, Pinterest pins/boards/search, page og:video) to use as reference, track or main content.
- **كيف / how:** basma_media.py on 127.0.0.1:8771 (/api/ping, /api/media, /api/search, /api/file/<id>), yt-dlp '-f best[ext=mp4]/best' with --no-playlist for single videos or --playlist-end N; gallery-dl --range 1-N; HTML fallback for Pinterest; 40_linkmedia.js panel; vite proxies to 8771 and /api/basma-page finds og:video in public pages with SSRF-guarded redirects.
- **أرقام / params:** timeouts yt-dlp 60 s, gallery-dl 45 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `app/basma_media.py` · `app/app/applet/basma_media.py` · `app/public/js/40_linkmedia.js:1`

#### FOOT-69 · أمر: إزالة الخلفية · CLI: remove-background · 📦 بأمر تثبيت
- **ماذا / what:** Matte a person to .webm/.mov/.png alpha; --background-output inverse plate; --device auto|cpu|coreml|cuda; --quality fast(crf30)|balanced(18)|best(12).
- **كيف / how:** npx hyperframes remove-background ... (or bun packages/cli); add --json for agent output.
- **أرقام / params:** Matte a person to .webm/.mov/.png alpha; --background-output inverse plate; --device auto|cpu|coreml|cuda; --quality fast(crf30)|balanced(18)|best(12).
- **تثبيت / install:** `npx hyperframes remove-background`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/packages/cli.mdx` · `kosif-one/vendor/hyperframes/packages/cli/src/commands`

#### FOOT-70 · أمر: معالجة الوسائط · CLI: media-treatment · 📦 بأمر تثبيت
- **ماذا / what:** Apply colour grading / effects to one img/video via --selector --grading JSON --apply --analyze --clear --dry-run; --capabilities lists families/presets/palettes.
- **كيف / how:** npx hyperframes media-treatment ... (or bun packages/cli); add --json for agent output.
- **أرقام / params:** Apply colour grading / effects to one img/video via --selector --grading JSON --apply --analyze --clear --dry-run; --capabilities lists families/presets/palettes.
- **تثبيت / install:** `npx hyperframes media-treatment`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/packages/cli.mdx` · `kosif-one/vendor/hyperframes/packages/cli/src/commands`

#### FOOT-71 · منحدرات السرعة · Speed ramps · 📦 بأمر تثبيت
- **ماذا / what:** Rate lane on media clips for slow-mo/speed-up.
- **كيف / how:** data-automation target 'rate' points t (clip seconds) v 0.1-10 with curve.
- **أرقام / params:** v clamp 0.1-10
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/reference/speed-ramps.mdx`

#### FOOT-72 · فصل الشخص عن الخلفية · Background removal compositing · 📦 بأمر تثبيت
- **ماذا / what:** Place subject cutout over/behind scene elements, same data-start for plate and cutout.
- **كيف / how:** remove-background then layer two <video>.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/guides/remove-background.mdx`

#### FOOT-73 · سينماغراف · Cinemagraph · 📦 بأمر تثبيت
- **ماذا / what:** Still photo with one feathered living region (steam over a cup) driven only by seek time with a period that divides the duration, so the loop is seamless.
- **كيف / how:** Install with `npx hyperframes add cinemagraph` (copies the full composition to compositions/cinemagraph.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 10 s; swap placeholder for still + masked looping video; 1920x1080; duration 10 s
- **تثبيت / install:** `npx hyperframes add cinemagraph` (copies the full composition to compositions/cinemagraph`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/cinemagraph/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/cinemagraph/cinemagraph.html`

#### FOOT-74 · تزيين الإطار المجمد · Freeze-Frame Dressing · 📦 بأمر تثبيت
- **ماذا / what:** Paper, tape and flash dressing around a freeze-frame or background-removed subject.
- **كيف / how:** Install with `npx hyperframes add freeze-frame-dressing` (copies the full composition to compositions/freeze-frame-dressing.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 4 s; 1920x1080; duration 4 s
- **تثبيت / install:** `npx hyperframes add freeze-frame-dressing` (copies the full composition to compositions/freeze-frame-dressing`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/freeze-frame-dressing/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/freeze-frame-dressing/freeze-frame-dressing.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/freeze-frame-dressing.mdx`

#### FOOT-75 · شبكة الوسائط · Rounded Media Grid · 📦 بأمر تثبيت
- **ماذا / what:** N-up rounded media grid (2-up, 3-up, 4-up, 3x2, hero+2) with inside-scale framing and staggered box-in entrance.
- **كيف / how:** Install with `npx hyperframes add mk-placeholder-grid` (copies the full composition to compositions/mk-placeholder-grid.html plus its assets); reference it from index.html with data-composition-src or open it standalone; edit inline constants/variables; preview `npx hyperframes preview`, render `npx hyperframes render`. Engine: GSAP 3.14.2 paused timeline (window.__timelines).
- **أرقام / params:** 8 s; 1920x1080; duration 8 s
- **تثبيت / install:** `npx hyperframes add mk-placeholder-grid` (copies the full composition to compositions/mk-placeholder-grid`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/mk-placeholder-grid/registry-item.json` · `kosif-one/vendor/hyperframes/registry/blocks/mk-placeholder-grid/mk-placeholder-grid.html` · `kosif-one/vendor/hyperframes/docs/catalog/blocks/mk-placeholder-grid.mdx`

#### FOOT-76 · القطع والتشذيب والتقسيم · Hard cut / trim / split / splice · 📦 بأمر تثبيت
- **ماذا / what:** Footage editing by attributes: a cut is adjacent clips; trim in/out with data-media-start + data-duration; split a source into multiple ranges by several <video> clips of the same src.
- **كيف / how:** creator-editing-recipes.md §Hard cut, Trim, Split/splice, Duplicate, Reorder; shift later data-start values by the delta.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-core/references/creator-editing-recipes.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-core/references/tracks-and-clips.md`

#### FOOT-77 · تجميد اللقطة · Freeze / hold frame · 📦 بأمر تثبيت
- **ماذا / what:** Hold a moment with an <img> still clip of the frame for N seconds; arbitrary mid-source freeze needs a preprocessed still or segment via media-use.
- **كيف / how:** <img src=held-frame.png class=clip data-start=2 data-duration=1>; decide audio continue/trim/silence explicitly.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-core/references/creator-editing-recipes.md`

#### FOOT-78 · السرعة الثابتة والتصوير البطيء · Constant speed / slow motion · 📦 بأمر تثبيت
- **ماذا / what:** data-playback-rate plays a clip at constant rate with pitch-preserved sound.
- **كيف / how:** consumed source = timeline duration x rate; rate range 0.1..10.
- **أرقام / params:** rate 0.1-10
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-core/references/creator-editing-recipes.md`

#### FOOT-79 · تدرج السرعة عبر مسار الأتمتة · Speed ramp via automation rate lane · 📦 بأمر تثبيت
- **ماذا / what:** Variable speed is a 'rate' lane in data-automation JSON on the clip; sections that are sub-compositions are split into halves and later starts shifted by the length change (new length = old/rate).
- **كيف / how:** data-automation='{"version":1,"lanes":[{"target":"rate","points":[{t,v}...]}]}'.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-core/references/creator-editing-recipes.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-audio/references/attributes.md`

#### FOOT-80 · نسخ مجموعة مقاطع إلى زمن آخر · Copy a group of clips to another time · 📦 بأمر تثبيت
- **ماذا / what:** Duplicate a set of clips and their tweens shifted by a constant offset; swap a media file by changing src only.
- **كيف / how:** creator-editing-recipes.md §Copy a group / §Add media / §Swap a media file.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-core/references/creator-editing-recipes.md`

#### FOOT-81 · مخطط مشهد: تحول من الفيديو إلى النص · Blueprint: Video-text pivot · 📦 بأمر تثبيت
- **ماذا / what:** A product video holds center, slides aside to hand weight to a hero stat, then kinetic text types into the vacated center sealed by a gradient pill.
- **كيف / how:** Pick from hyperframes-animation/blueprints-index.md by role, then read hyperframes-animation/blueprints/video-text-pivot.md for the multi-phase recipe; cite blueprint id per beat in the storyboard.
- **أرقام / params:** duration 6-8 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints/video-text-pivot.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-animation/blueprints-index.md`

#### FOOT-82 · نص خلف الشخص · Composition pattern: text behind subject · 📦 بأمر تثبيت
- **ماذا / what:** Headline sits between the full mp4 base and a transparent cutout of the presenter so the silhouette occludes the text.
- **كيف / how:** `npx hyperframes remove-background presenter.mp4 -o presenter.webm`; layers z1 base mp4, z2 headline, z3 alpha webm cutout in lockstep.
- **أرقام / params:** 3 layers
- **تثبيت / install:** `npx hyperframes remove-background presenter`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-creative/references/composition-patterns.md`

#### FOOT-83 · إزالة الخلفية من الفيديو · Remove background (alpha cutout) · 📦 بأمر تثبيت
- **ماذا / what:** Produces a transparent webm cutout of a presenter for text-behind-subject or overlays.
- **كيف / how:** npx hyperframes remove-background presenter.mp4 -o presenter.webm (see media-use remove-background reference).
- **تثبيت / install:** `npx hyperframes remove-background presenter`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-creative/references/composition-patterns.md` · `kosif-one/vendor/hyperframes/skills/media-use/audio/references/remove-background.md`

#### FOOT-84 · القص بالنص المفرغ · Transcript-based cut (text editing of footage) · 📦 بأمر تثبيت
- **ماذا / what:** Compiles word timestamps and cut decisions into exact kept segments: remove ranges, filler words and silences.
- **كيف / how:** node <skill>/scripts/transcript-cut.mjs --input talk.mp4 --transcript talk.transcribe.json --remove '12.41-15.02,88.3-91.7' --remove-fillers 'um,uh,like' --cut-silence 0.8 --out talk.cut.mp4 [--plan].
- **أرقام / params:** cut-silence 0.8 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/media-use/references/operations.md` · `kosif-one/vendor/hyperframes/skills/media-use/scripts/transcript-cut.mjs` · `kosif-one/vendor/hyperframes/skills/media-use/scripts/transcript-cut.test.mjs`

#### FOOT-85 · إزالة الخلفية · Background removal (u2net / HeyGen) · 📦 بأمر تثبيت
- **ماذا / what:** Local u2net cutouts of images/video to transparent webm with quality/device options and a 3-layer plate+content+cutout template; HeyGen CLI higher-quality option.
- **كيف / how:** npx hyperframes remove-background in.mp4 -o out.webm [--quality] [--device] [--background-output plate.mp4]; heygen background-removal.
- **تثبيت / install:** `npx hyperframes remove-background in`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/media-use/audio/references/remove-background.md` · `kosif-one/vendor/hyperframes/skills/media-use/references/operations.md`

#### FOOT-86 · استخراج قناع المتحدث · Subject matting for occlusion · 📦 بأمر تثبيت
- **ماذا / what:** Per-frame subject alpha via the CLI's remove-background (u2net_human_seg equivalent, 320x320 input, ~9 fps on CoreML) feeding text-behind-subject compositing.
- **كيف / how:** node scripts/matte.cjs <project> (run by prepare.sh).
- **أرقام / params:** 320x320; ~9 fps
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/embedded-captions/scripts/matte.cjs` · `kosif-one/vendor/hyperframes/skills/embedded-captions/references/failure-modes.md`

#### FOOT-87 · إعادة تغليف فيديو المتحدث ببطاقات مصممة · Talking-head recut with designed overlay cards · 📦 بأمر تثبيت
- **ماذا / what:** Packages an existing interview/podcast clip (footage untouched) with transcript-synced cards: kinetic titles, lower-thirds, data callouts, pull-quotes, side panels, PiP, while the video wrapper tweens between layouts.
- **كيف / how:** Steps: check env -> work dir -> ffprobe metadata + ffmpeg audio -> `hyperframes transcribe` -> correct transcript -> storyboard.json (schemaVersion 3, composition{fps,width,height,durationSeconds,layout,themeId,seed}, videoTrack, cards[zone,startSec]) -> per-card HTML -> assemble index.html with one paused master timeline window.__timelines['talking-head-recut'] -> render.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/talking-head-recut/SKILL.md` · `kosif-one/vendor/hyperframes/skills/talking-head-recut/media-contract.test.mjs`

#### FOOT-88 · معالجات المونتاج على شبكة الإيقاع · Montage asset treatments on the beat grid · 📦 بأمر تثبيت
- **ماذا / what:** Three ways to weave user media: beat_cut (one clip per anchor on a beat_cut frame), ken_burns (slow push on one clip in a phrase_flow frame), bg_under_text (clip dimmed behind a template/free group).
- **كيف / how:** references/montage.md rules; stage with scripts/stage-assets.mjs.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/music-to-video/references/montage.md`

#### FOOT-89 · جلب الوسائط · fetch media yt-dlp · 📦 بأمر تثبيت
- **ماذا / what:** Pinterest pins/boards and TikTok/Instagram/YouTube/X into media library; edit-safe copy H.264 yuv420p CFR ≤60 AAC 48 kHz; credits json.
- **كيف / how:** python scripts/kmotion.py fetch URL… --max 30 --only video|image --list --cookies
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md`

#### FOOT-90 · إظهار اللقطة من باهت إلى ملوّن · Footage desaturate-to-colour reveal · 📦 بأمر تثبيت
- **ماذا / what:** The opening frame of real footage starts dimmed and desaturated and blooms into full colour as the hook word lands.
- **كيف / how:** tl.fromTo('#plate', {filter:'saturate(.55) brightness(.92)'}, {filter:'saturate(1) brightness(1)', 0.6 s, power3.out}, 0.40) with #dim overlay 0.42→0 in 0.55 s.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:144` · `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:148`

#### FOOT-91 · لقطة حقيقية مع رسومات فوقها · Real footage plate with graphics on top · 📦 بأمر تثبيت
- **ماذا / what:** A vertical talking clip is the plate; graphics, light layers, particles and captions live in HTML above it, and a virtual camera moves the plate.
- **كيف / how:** <div id=cam><video id=plate src=assets/plate.mp4 data-start=0 data-duration=20.566 muted></div> + .layer stack (#bloom, #rays, #scrim gradient 52%→.74, #vig, #dim, #particles) + SVG graphics + typography; prepare plate with kmotion footage (seekable).
- **أرقام / params:** 1080×1920, 30 fps, 20.566 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:45` · `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:46`

#### FOOT-92 · إخفاء الوجوه والمناطق · Face/region privacy masks · 📦 بأمر تثبيت
- **ماذا / what:** Faces or given regions are pixelated, blurred or boxed in every frame, keeping audio; detector falls back from YuNet to Haar to a skin-colour detector.
- **كيف / how:** faces.which() ∈ {yunet, haar, skin}; faces.detect(frame, min_frac); privacy.pixelate(frame, box, 10); privacy.anonymize(clip, out, mode='box', regions=[parse_region('0.1,0.1,0.3,0.3', W, H)]).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_v6.py:132`

#### FOOT-93 · جلب الوسائط مع حفظ الاعتمادات · Media fetch with credits (yt-dlp) · 📦 بأمر تثبيت
- **ماذا / what:** Links are downloaded into a media folder with an edit copy that keeps sound, a fetch-credits.json recording the source, duplicate skipping and image download.
- **كيف / how:** fetch.fetch([url], out) → {fetched:[{edit}], skipped:[{why:'already fetched'}]}; fetch._download_image(url, dir).
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_fetch_lab.py:66`

#### FOOT-94 · محاكاة ريل: دراسة · Reel mimic: study · 📦 بأمر تثبيت
- **ماذا / what:** Measures a reference reel: every cut/dissolve/dip/slide boundary to the frame, shot lengths, look, text zone, fades, flashes, audio.
- **كيف / how:** python scripts/kmotion.py mimic study REF.mp4 --out PROJECT/study -> shots.jpg, strip.jpg (frame/0.5 s), text/shot_XX.png, search/shot_XX.jpg, mimic.json
- **أرقام / params:** boundary types: cut, dissolve, fadeblack, fadewhite, slide*; ~30 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/mimic.md` · `100-superskills/skills/kosif-montage-motion/scripts/mimic.py` · `100-superskills/skills/kosif-montage-motion/tests/test_mimic.py`

#### FOOT-95 · رفع طبقة التصميم الثابت · Overlay layer lift + erase/snap · 📦 بأمر تثبيت
- **ماذا / what:** Auto-extracts the fixed design layer (titles, badges) as overlay.png; erases creator logos; snaps moving badges by HSV.
- **كيف / how:** mimic layer DIR --erase x0,y0,x1,y1 ; --snap x0,y0,x1,y1@SHOT:hmin,hmax,smin,vmin; layer.fade_in
- **أرقام / params:** gold HSV e.g. 18,40,80,140
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/mimic.md`

#### FOOT-96 · جمع لقطات من بنترست · Pinterest footage pool · 📦 بأمر تثبيت
- **ماذا / what:** Collect mood-matched clips: user signs in, search videos, scrape pin links, check, fetch only video with credits.
- **كيف / how:** pinterest.com/search/videos/?q=..., JS a[href*='/pin/'], kmotion fetch --list LINKS, kmotion fetch LINKS --only video --out PROJECT/pool; fetch-credits.json
- **أرقام / params:** clips >= shot clip length (or >=0.67x slowed); 2-3 candidates/shot; queries 2-4 per shot English first
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/mimic.md` · `100-superskills/skills/kosif-montage-motion/references/operating-manual.md` · `100-superskills/skills/kosif-montage-motion/scripts/fetch.py`

#### FOOT-97 · مونتاج تلقائي على الموسيقى · Auto montage to music · 📦 بأمر تثبيت
- **ماذا / what:** Beats, best windows, photo pushes, landscape over blurred copy, -14 LUFS, credits.
- **كيف / how:** kmotion montage MEDIA --music track --ratio 9:16 [--grade][--voice][--captions]
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/operating-manual.md` · `100-superskills/skills/kosif-montage-motion/scripts/montage.py`

#### FOOT-98 · ريل من مقطع كلام · Talking clip to reel · 📦 بأمر تثبيت
- **ماذا / what:** Auto-directed reel, silence cuts, smart aspect, captions.
- **كيف / how:** kmotion reel CLIP | direct CLIP | silence | aspect | captions
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/operating-manual.md` · `100-superskills/skills/kosif-montage-motion/scripts/reel.py` · `100-superskills/skills/kosif-montage-motion/scripts/direct.py`

#### FOOT-99 · كشف المشاهد · Scene detect to timeline · 📦 بأمر تثبيت
- **ماذا / what:** One clip per detected shot.
- **كيف / how:** kmotion scenes CLIP --timeline edit.json
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/timeline-schema.md` · `100-superskills/skills/kosif-montage-motion/scripts/scenes.py`

#### FOOT-100 · فحص وتنزيل دبابيس Pinterest بالتوازي · Parallel Pinterest probe and download (yt-dlp) · 📦 بأمر تثبيت
- **ماذا / what:** Checks many Pinterest pin IDs at once for a downloadable video and its size, then downloads the good ones with a manifest.
- **كيف / how:** ThreadPoolExecutor(6-7) running yt-dlp --ignore-config --no-playlist --skip-download --socket-timeout 6 --retries 1 --print '%(duration)s|%(width)s|%(height)s|%(ext)s'; download with -f 'b[ext=mp4][height<=1920]/b[height<=1920]/b' --max-filesize 70M, ffprobe each file, write manifest.json with rights 'unverified'.
- **أرقام / params:** workers 5-7; timeout 18-24 s probe, 95 s download; max 70 MB
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/KOSIF_Motion_Ghorba/tools/probe_pins.py` · `kosif-one/projects/KOSIF_Motion_Ghorba/tools/probe_pins_v2.py` · `kosif-one/projects/KOSIF_Motion_Ghorba/tools/download_pins.py`

#### FOOT-101 · أداة جلب فيديو آمنة من رابط عام · KOSIF C Video Fetch (safe public URL fetcher) · 📦 بأمر تثبيت
- **ماذا / what:** Downloads exactly one video from a public HTTPS link with strict safety rules and converts it to a phone-safe MP4 with an integrity receipt.
- **كيف / how:** Validate URL (https only, no credentials, port 443, no localhost/.local/.internal, every resolved IP must be global); yt-dlp formats 'bv*[height<=720]+ba/b[height<=720]/best[height<=720]' then 'b[height<=720]/best' into an isolated temp dir; exactly one media file; ffmpeg normalise to H.264 crf 24 veryfast + AAC 128k, faststart, max 1280x720; write KOSIF-C-Video-receipt.json with sha256.
- **أرقام / params:** MAX_BYTES 150 MB, MAX_SECONDS 900, MAX_HEIGHT 720; yt-dlp timeout 270 s; ffmpeg 450 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/KOSIF_Motion_Ghorba/tools/kosif_c_video_fetch.py:24-49` · `kosif-one/projects/KOSIF_Motion_Ghorba/tools/kosif_c_video_fetch.py:83-133` · `kosif-one/projects/KOSIF_Motion_Ghorba/pinterest_via_kosif/sources.json`

#### FOOT-102 · فحص فيديو مرجعي · Reference reel probe (TikTok/Pinterest) · 📦 بأمر تثبيت
- **ماذا / what:** Before copying a look, probe the reference link for title, id and duration without downloading; this log shows TikTok failing (no impersonation target) and a Pinterest 'smooth & clean marketing reel' of 25.567 s succeeding.
- **كيف / how:** yt-dlp --no-playlist --skip-download --socket-timeout 12 --print title/id/duration; for TikTok install an impersonation backend (curl_cffi) or ask the user for the file.
- **أرقام / params:** Pinterest pin 935904366328038869, 25.567 s
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/KOSIF_Motion_TikTok_Reference/source_probe.txt`

#### FOOT-103 · رفع الطبقة الثابتة مع مسح العلامة · Overlay layer lift with watermark erase · 📦 بأمر تثبيت
- **ماذا / what:** Separates the fixed design that stays on screen across the reference (a frame/ornament) into a transparent PNG, erasing the creator's handle/watermark boxes, so it can be reused or retyped.
- **كيف / how:** mimic layer DIR --erase x0,y0,x1,y1 (fractions); layer {template_share, coverage, erase boxes, snap box with HSV range, fade_in}; then overlays[] reuse overlay.png per shot with fade in/out.
- **أرقام / params:** 4 erase boxes e.g. [0.18,0.722,0.8,0.758]; coverage .0811; fade_in .45
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/mimic-jumuah/study/mimic.json` · `kosif-one/projects/mimic-jumuah/study/mimic.timeline.json`

#### FOOT-104 · استعلامات بحث لكل لقطة · Per-shot bilingual stock queries · 📦 بأمر تثبيت
- **ماذا / what:** Each reference shot is described as 1-2 Pinterest searches (English plus Arabic terms) so new footage with the same meaning can be fetched into one pool.
- **كيف / how:** shots[].query e.g. ['incense burner smoke aesthetic','bakhoor mabkhara'], ['quran candles tasbih aesthetic'], ['red roses coffee aesthetic']; fetch pins per theme (pins.txt) into pool/ with fetch-credits.json (creator, duration, edit copy).
- **أرقام / params:** pool 43 videos; themes incense 12, quran 10, flowers 10, roses 10, coffee 1
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/projects/mimic-jumuah/study/mimic.json` · `kosif-one/projects/mimic-jumuah/pins.txt` · `kosif-one/projects/mimic-jumuah/pool/fetch-credits.json`

#### FOOT-105 · مسح الترجمة المحروقة · Burned-in caption eraser (decaption) · 📦 بأمر تثبيت
- **ماذا / what:** Finds caption ink (white/yellow near black outline) in a band, rebuilds locked-off shots from per-pixel median of uncovered frames and inpaints moving shots; removes fixed credit lines.
- **كيف / how:** python decaption.py VIDEO --out CLEAN.mp4 [--band 0.45:0.56] [--keep-credit] [--report].
- **أرقام / params:** inpaint only runs >= 22% frame width; masks carried +-3 frames
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/decaption.py`

#### FOOT-106 · إعادة رسم مطابقة تماماً · Exact redraw (block in -> refine -> touches) · 📦 بأمر تثبيت
- **ماذا / what:** Paints any image from blank in three stages and ends identical pixel for pixel; photo plans (6/10/16/24 block colours, 32-128 tones) chosen by Jev.
- **كيف / how:** studio.py --image photo.jpg (mode مطابق تماماً) / exact.py.
- **أرقام / params:** plan measured in ~3 s on a reduced copy
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-one/tools/kosif-studio/exact.py` · `kosif-one/tools/kosif-studio/README.md`

#### FOOT-107 · حزمة برنامج التعديل لأي ذكاء اصطناعي · Keyed edit program package for any AI · 📦 بأمر تثبيت
- **ماذا / what:** Edits an existing picture through a small Pillow program that holds a key instead of the image, plus a colour-layer description; any AI edits only between markers and the studio restores the original bytes before running.
- **كيف / how:** python edit_pack.py photo.jpg "make the shirt red" prints the package; edit_program() stores code/originals/<sha16>.b64; restore() swaps <<KOSIF:ORIGINAL:sha>> back; with_edits() fills # EDITS START/END.
- **أرقام / params:** key = first 16 hex of SHA-1; description up to 14 layers with name, hex, share, bbox, centre, big parts
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/edit_pack.py:1` · `kosif-studio/edit_pack.py:116` · `kosif-studio/edit_pack.py:211`

#### FOOT-108 · إزالة الترجمة المحروقة · Burned-caption eraser (decaption) · 📦 بأمر تثبيت
- **ماذا / what:** Finds caption strokes (white or saturated yellow next to a black outline), the caption band and fixed credit pixels; rebuilds locked-off shots from the per-pixel median of uncovered samples and inpaints moving shots, carrying masks through fades.
- **كيف / how:** python decaption.py VIDEO --out CLEAN.mp4 [--band 0.45:0.56 --keep-credit]
- **أرقام / params:** white V>205 S<55; yellow H 16-38 S>110 V>150; dark V<70 within 9 px ellipse; line join 31×13; min run 45 px (moving shots 22 % width ≥60); band ±14 px; credit white >55 % of frames; locked if outside-band motion ≤1.2; masks ±3 frames; Telea inpaint r 9 (specks r 4); output crf 12
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/decaption.py:38` · `kosif-studio/motion/decaption.py:99` · `kosif-studio/tests/test_studio.py:850`

#### FOOT-109 · اكتشاف القطعات · Shot-cut detection (decaption.analyse) · 📦 بأمر تثبيت
- **ماذا / what:** Local-maximum frame-difference cuts robust to codecs spreading a cut over two frames; also gives per-frame luminance.
- **كيف / how:** decaption.analyse(path, band)
- **أرقام / params:** 90×160 grey; thr max(12, 6×median); >4× local median (±15 frames); min 5 frames apart
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/decaption.py:63`

#### FOOT-110 · ريل تلقائي بأمر واحد · One-command talking-clip reel · 📦 بأمر تثبيت
- **ماذا / what:** Raw talking clip → finished vertical short: transcribe and decaption in parallel, restore + reframe, voice chain, music only if none, karaoke captions + credit in one encode, −14 LUFS, delivery gate.
- **كيف / how:** python reel.py CLIP.mp4 --out FINAL.mp4 [--size 1080x1920 --model large-v3 --music auto|none|bed.wav --style reels --no-decaption --no-captions --credit '...' --transcript words.json]
- **أرقام / params:** intermediate crf 12 fast; final crf 16 medium +faststart; proof IMG_9262 reel: gate ok, −14.5 LUFS, TP −2.7, caption band 598-706, credit 12,842 px
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-studio/motion/reel.py:92` · `kosif-studio/out/reel_test/IMG_9262_reel.reel.json`

#### FOOT-111 · بارالاكس · Style: 2D parallax (parallax-2d) · 📦 بأمر تثبيت
- **ماذا / what:** Photo cut into layers moving at depth-proportional speeds.
- **كيف / how:** Layer depth factors bg 0.15, mid 0.45, subject 1.0, occluder 1.4; oversize layers; blurred 1.3x bg copy. Scaffold: python3 tools/kosif.py scaffold parallax-2d <dir>.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `style:parallax-2d` · `kosif-tool/playbooks/photos.md`

#### FOOT-112 · مونتاج مختلط · Style: Viral mixed media (viral-mixed-media) · 📦 بأمر تثبيت
- **ماذا / what:** Fast collage of footage, cut-outs, stickers and big text.
- **كيف / how:** Beat-cut every 1-2s, cut-outs with contact shadow, kinetic type 7 words max, grain 2-4%. Scaffold: python3 tools/kosif.py scaffold viral-mixed-media <dir>.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `style:viral-mixed-media` · `kosif-tool/playbooks/ads.md`

#### FOOT-113 · مونتاج تحريري · Style: Editorial montage (editorial) · 📦 بأمر تثبيت
- **ماذا / what:** Magazine-like editorial layouts mixing photos and serif/sans type.
- **كيف / how:** Photo rig + type grid; masks and wipes 350-500ms; one grade, grain, vignette. Scaffold: python3 tools/kosif.py scaffold editorial <dir>.
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `style:editorial` · `kosif-tool/playbooks/kinetic-type.md`

#### FOOT-114 · صور · Category: Photos · 📦 بأمر تثبيت
- **ماذا / what:** Capability family 'photos' (34 catalog entries) with a dedicated bilingual playbook of timings and recipes.
- **كيف / how:** Read playbooks/photos.md (visual grammar, motion mechanics, scene recipes, QA); build in starters/html-canvas or starters/remotion; filter catalog with python3 tools/kosif.py list --category photos.
- **أرقام / params:** Ken Burns 1.00->1.06 over 4-6s max 1.12; parallax 0.15/0.45/1.0/1.4; grain 2-4%; vignette 10-15%; scrim 0.6->0
- **تثبيت / install:** `see arsenal-libraries.md`
- **الدليل / proof:** `kosif-tool/playbooks/photos.md` · `kosif-tool/catalog/categories.json` · `kosif-tool/catalog/meta.json`

#### FOOT-115 · عزل الصوت وإزالة الضوضاء بالذكاء · AI audio isolation / denoise · 🔑 مفتاح/خدمة
- **ماذا / what:** Strip background noise/music from a dialogue recording before editing.
- **كيف / how:** ElevenLabs audioIsolation endpoint (stream variant for big files); local alternative: ffmpeg afftdn/arnndn (no key).
- **أرقام / params:** <=500MB; billed 1000 chars/min
- **الدليل / proof:** `kosif-atlas/skills/1847-elevenlabs-pack/5515-elevenlabs-core-workflow-b`

#### FOOT-116 · رفع دقة الفيديو مرة واحدة بعد الدمج · Video upscale once after final concat · 🔑 مفتاح/خدمة
- **ماذا / what:** AI video upscalers sharpen resolution but cannot fix blur or shake; run them once on the finished cut, not per segment.
- **كيف / how:** Generate at native target resolution, concat with ffmpeg -f concat -c copy, then Topaz/ByteDance upscale; skip 60 fps unless the platform needs it.
- **أرقام / params:** Topaz 720p 1, 1080p 2, 4K 8 credits/s; 60 fps ×2
- **الدليل / proof:** `kosif-atlas/skills/259-quickdesign/865-quickdesign` · `kosif-atlas/skills/2976-pwdev-social-media/12579-asset-upscale`

#### FOOT-117 · المونتاج الذكي الكامل من الكلام · Smart full montage from speech (AutoEdit) · 🔑 مفتاح/خدمة
- **ماذا / what:** Audio/video -> word-level transcript -> scenario and scenes -> matching footage from Pexels/Pixabay/Pinterest/Wikimedia/Gemini -> cuts on the words -> synced captions -> review -> render -> share.
- **كيف / how:** window.BasmaAutoEdit.run: defaults aspect 9:16, pace med, capWords 2, motion med; sources pexels/pixabay/pinterest/commons (+gemini off); extras mg (Claude motion graphics), sfx, vfx, gvid (Veo hero shot, off); 19 camera ids; vfxPlan picks grade/particles/grain/leak/vignette/letterbox/transition and up to 4 'flash' accents (implemented as crash_zoom).
- **الدليل / proof:** `app/public/js/50_autoedit.js:4` · `app/public/js/50_autoedit.js:10` · `app/public/js/50_autoedit.js:427`

#### FOOT-118 · مونتاج احترافي بالقوالب · Pro montage with template inserts · 🔑 مفتاح/خدمة
- **ماذا / what:** Base autopilot edit, then Claude picks the best Prompt Motion template for the footage, plans beats from what is said and codes motion inserts in that template's style (hook, key-point graphics, charts/lists, outro CTA); Gemini paints photo B-roll and Veo one hero shot when allowed.
- **كيف / how:** window.PROMONT: PM.ensureWords (transcribe first), PM.pick (Claude chooses template), PM.run (inserts via writeCode, pool of parallel jobs); calm mode respected.
- **الدليل / proof:** `app/public/js/30_promontage.js:5` · `app/public/js/30_promontage.js:41` · `app/public/js/30_promontage.js:108`

#### FOOT-119 · بحث في المكتبات المجانية مع الحقوق · Free stock media search with credits · 🔑 مفتاح/خدمة
- **ماذا / what:** Finds free images, videos or audio for a moment, prefers the right orientation, and keeps author/licence for credits; Gemini or Claude judges relevance.
- **كيف / how:** Server route /api/basma-stock (vite middleware): Openverse (license_type=commercial,modification), Wikimedia Commons (filetype), Pexels (key, portrait video preferring ~1280 px height) and Pixabay (key); images < 600 px dropped; STOCK.judge keeps relevant results; STOCK.credits[] {title,by,license,page,src}.
- **الدليل / proof:** `app/public/js/10_studio.js:4437` · `app/public/js/10_studio.js:4448` · `app/public/js/10_studio.js:4559`

#### FOOT-120 · تحميل من المنصات · Social URL fetch (yt-dlp) · 🔑 مفتاح/خدمة
- **ماذا / what:** Fetch TikTok/Instagram/Facebook/YouTube/X media.
- **كيف / how:** kmotion fetch URL
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/operating-manual.md` · `100-superskills/skills/kosif-montage-motion/scripts/fetch.py` · `100-superskills/skills/kosif-montage-motion/tests/test_fetch_lab.py`

#### FOOT-121 · جلب الوسائط · Media fetch · 🔑 مفتاح/خدمة
- **ماذا / what:** yt-dlp Pinterest/TikTok/IG/YT fetch + edit-safe H.264 copy.
- **كيف / how:** kmotion fetch URL --max 30 --only video
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/fetch.py`

#### FOOT-122 · جلب لقطات من بنترست · Pinterest footage sourcing with fallback page · 🔑 مفتاح/خدمة
- **ماذا / what:** Per-shot Pinterest search queries (English + Arabic); download best video variant when reachable, otherwise publish an intermediary page with keyframes and search buttons for the user to fetch clips. Credit the pins.
- **كيف / how:** SKILL.md step 4: BaseSearchResource / PinResource endpoints; >= 720p, no watermarks/burned text.
- **الدليل / proof:** `kosif-one/tools/kosif-mimic/SKILL.md`

#### FOOT-123 · جلب لقطات بنترست · Pinterest footage sourcing · 🔑 مفتاح/خدمة
- **ماذا / what:** Per-shot 3-5 EN+AR queries; >=720p, no watermark/burned text; Pinterest resource endpoints when reachable, else intermediary artifact page with search buttons and paste boxes; credit pin links.
- **كيف / how:** Documented API paths BaseSearchResource, PinResource; HLS master via ffmpeg
- **الدليل / proof:** `100-superskills/skills/kosif-mimic/SKILL.md`

#### FOOT-124 · جلب لقطات مفتوحة · Open-footage ingestion with provenance · 🔑 مفتاح/خدمة
- **ماذا / what:** Download stock clips only from allowlisted hosts with HTTPS, redirect revalidation, HTML-challenge rejection, size cap and a provenance sidecar.
- **كيف / how:** motion.py openclip URL (open_footage.py).
- **أرقام / params:** hosts Pexels + Wikimedia; 500 MiB cap; .source.json with SHA-256, bytes, URLs, host, licence note; no login/paywall/anti-bot bypass
- **الدليل / proof:** `kosif-studio/motion/references/voice-open-footage-upgrade-2026-10-10.md`

#### FOOT-125 · تنزيل لقطات مفتوحة مع إثبات المصدر · Open-footage downloader with provenance · 🔑 مفتاح/خدمة
- **ماذا / what:** Downloads one explicit HTTPS media URL from an allow-listed open/stock host, refuses HTML/challenge pages, caps size, hashes the bytes and writes a provenance receipt.
- **كيف / how:** python motion.py openclip URL --out clip.mp4 [--license-note '...'] (or open_footage.py)
- **أرقام / params:** hosts *.pexels.com, *.wikimedia.org; https only; ≤500 MiB; ≥64 KiB; timeout 120 s; SHA-256; sidecar .source.json schema kosif-open-footage-v1
- **الدليل / proof:** `kosif-studio/motion/open_footage.py:1` · `kosif-studio/motion/test_open_footage.py:1`

#### FOOT-126 · شاشات فيديو مقسومة · Split-screen footage panels · 👁 شوهد في فيديو
- **ماذا / what:** 2 panels, one footage, one info card
- **الدليل / proof:** `style:pm-andginja-333d32`

#### FOOT-127 · شاشة مقسومة بين القناع والنتيجة · Split-screen matte vs composite · 👁 شوهد في فيديو
- **ماذا / what:** left half shows the colour-key matte/false-colour pass, right half the final composite; a vertical divider wipes across
- **أرقام / params:** divider 2 px, wipe 600 ms
- **الدليل / proof:** `style:pm-blueoctopusai-dd17bd`

#### FOOT-128 · لقطات اللعب كخلفية · Gameplay as background plate · 👁 شوهد في فيديو
- **ماذا / what:** screen-record the real product, darken with navy multiply overlay and vignette so oversized type stays legible
- **أرقام / params:** overlay 40-55%
- **الدليل / proof:** `style:pm-deifosv-04e4d3`

#### FOOT-129 · مزج لقطات حقيقية مع واجهة · Real footage + UI hybrid · 👁 شوهد في فيديو
- **ماذا / what:** Use supplied talking-head clip both full-bleed and inside phone UI for continuity
- **الدليل / proof:** `style:pm-gautam-mer1-2ae354`

#### FOOT-130 · كولاج نيون بطبقات متحركة · Psychedelic collage parallax · 👁 شوهد في فيديو
- **ماذا / what:** layer cut-out images (bust, flowers, grids) at different depths, slow scale 1.0->1.08 and offset per layer; saturate 1.4, add grain
- **أرقام / params:** 3-5 layers
- **الدليل / proof:** `style:pm-gizakdag-b8c59e`

#### FOOT-131 · تمويه فسيفسائي · Pixel mosaic privacy blur · 👁 شوهد في فيديو
- **ماذا / what:** quantize face region to blocks with red corner brackets
- **أرقام / params:** block 16px
- **الدليل / proof:** `style:pm-heyiammallik-e72d17`

#### FOOT-132 · شرائح الفلاتر · Filter strips · 👁 شوهد في فيديو
- **ماذا / what:** same photo in N columns with CSS filter each, labels below, reveal stagger 80 ms
- **الدليل / proof:** `style:pm-oliahmed205-3e31c4`

#### FOOT-133 · قبل/بعد · Before/after split · 👁 شوهد في فيديو
- **ماذا / what:** vertical divider sliding across
- **الدليل / proof:** `style:pm-quickdesignio-dd93d0`

#### FOOT-134 · قص المتحدث ووضعه فوق عوالم متبدلة · Rotoscoped subject over swapped worlds · 👁 شوهد في فيديو
- **ماذا / what:** Segment the speaker per frame (matting model), add 6-8 px white outline, composite over a different generated backdrop per segment; cut backdrop on sentence boundaries
- **أرقام / params:** outline 6-8 px white, soft shadow 20 px
- **الدليل / proof:** `style:pm-sab8a-364a5a`

#### FOOT-135 · صورة المنتج في سياق · Mockup-in-context photo · 👁 شوهد في فيديو
- **ماذا / what:** composite print into wall/hand photos with shadow
- **الدليل / proof:** `style:pm-twoclipping-221cab`

#### FOOT-136 · جدار فيديوهات · Video tile wall · 👁 شوهد في فيديو
- **ماذا / what:** grid of 9:16 tiles at varied offsets drifting slowly
- **الدليل / proof:** `style:pm-twoclipping-6dd14e`

#### FOOT-137 · قص غير هدام مقابل إعادة الترميز · Non-destructive trim vs ffmpeg re-encode · 📄 موصوف
- **ماذا / what:** Prefer trim props in the composition; if a standalone trimmed file is needed, re-encode from the exact frame to avoid frozen first frames.
- **كيف / how:** ffmpeg -ss 00:00:05 -i in.mp4 -to 00:00:10 -c:v libx264 -c:a aac out.mp4 (stream copy can freeze until next keyframe). Remotion bundles ffmpeg via npx remotion ffmpeg/ffprobe.
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10436-remotion-markup/ffmpeg.md` · `kosif-atlas/skills/235-mas-video-lab/756-losslesscut/SKILL.md`

#### FOOT-138 · استخراج إطارات الغلاف والأغلفة المتحركة · Thumbnail frame mining and loop covers · 📄 موصوف
- **ماذا / what:** Pick cover frames that explain the video at a glance: sample across the whole duration, skip transition, blurred, first/last frames, shortlist visually distinct candidates with timestamps; animated covers use a short gentle-motion window with matching ends.
- **كيف / how:** ffmpeg -vf "select='gt(scene,0.3)',scale=640:-1,tile=4x3" for a contact sheet, or the thumbnail filter; for composed videos render the chosen moment directly from the composition at each target size; loop seam via brief crossfade; check at phone size.
- **أرقام / params:** scene threshold ~0.3 (tunable); loop crossfade ~0.4 s
- **الدليل / proof:** `kosif-atlas/skills/101-video-skills/222-video-thumbnails/SKILL.md`

#### FOOT-139 · خطة تسجيل الشاشة وإعداداته · Screen-recording plan and capture defaults · 📄 موصوف
- **ماذا / what:** Storyboards end with a screen-recording table (order, shot, window, cursor actions/inputs, length, prep) so all captures are done in one pass with consistent settings.
- **كيف / how:** Defaults: capture at native monitor resolution (e.g. 3840x2160), 30 fps matching the timeline, per-window capture, enlarged cursor, mic and system audio on separate tracks, hardware H.264/H.265 at CQP 18-20, editor font >=16 pt (terminal 18 pt), notifications off, history and private tabs cleared.
- **أرقام / params:** 3840x2160; 30 fps; CQP 18-20; font >=16 pt
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2449-akbun-vlog-storyboard/SKILL.md`

#### FOOT-140 · S08 وثائقي معلوماتي · S08 Documentary evidence · 📄 موصوف
- **ماذا / what:** Real photos, visible dates and references, maps; light moves on archive material, show the evidence then explain. Builds context; facts and archive need verification and rights, and decoration must never look like evidence.
- **كيف / how:** ffmpeg zoompan/HTML transforms on archive stills, citation captions, map routes; KOSIF render_html.cjs (/home/user/kosif-tool/tools/render_html.cjs: HTML/SVG + CSS/WAAPI or window.__kosif.seek(t) -> Playwright frame capture -> ffmpeg)
- **أرقام / params:** cost medium; MG-045 MG-046 MG-068 MG-075 MG-078 MG-084 MG-088
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/styles.md`

#### FOOT-141 · MG-038 مقارنة قبل وبعد صادقة · MG-038 Honest before/after wipe · 📄 موصوف
- **ماذا / what:** A divider moves between the original and the result in the same framing.
- **كيف / how:** 0-1 s define both, 1-4 s divider moves, 4-6 s stop; linear moving mask + divider line + date/condition label. Never change lighting or lens between sides to fake improvement. Local: ffmpeg overlay with animated crop, or HTML clip-path inset animation.
- **أرقام / params:** 6 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-product-ads.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### FOOT-142 · MG-051 عنوان خلف المتحدث · MG-051 Title behind the speaker · 📄 موصوف
- **ماذا / what:** A large title appears behind the interviewee's body while the face stays clear.
- **كيف / how:** 0-1 s shot, 1-2 s title reveal, 2-5 s hold. Isolate the person (rotoscoping) above the title layer; check hair and hands and never cover eyes or mouth. Local: person matte from rembg/RVM/SAM2 (needs install) or MediaPipe selfie segmentation in the browser -> ffmpeg overlay order plate -> title -> person.
- **أرقام / params:** 5 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-tracking-compositing.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### FOOT-143 · MG-052/060 تسمية متتبعة ودائرة اهتمام · MG-052/060 Tracked callout and attention ring · 📄 موصوف
- **ماذا / what:** A dot and short leader line stay pinned to a moving product part (MG-052); a thin circle approaches a small detail and follows it during the explanation (MG-060).
- **كيف / how:** MG-052: 0-1 intro, 1-2 line appears, 2-6 track; track to a null, hide the label when the target is occluded or leaves frame. MG-060: 0-1 appear, 1-4 follow, 4-5 out; never cover the evidence. Local: OpenCV point tracker (pip install opencv-python - needs install) or manual keys every few frames + interpolation, overlay drawn in HTML at the tracked coordinates.
- **أرقام / params:** 6 s / 5 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-tracking-compositing.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### FOOT-144 · MG-053/059 إدراج بمنظور مثبت بأربع نقاط · MG-053/059 Planar corner-pin inserts · 📄 موصوف
- **ماذا / what:** A sticker follows a wall's perspective while the camera moves (MG-053); a blank card held in a hand becomes a simple diagram that follows its tilt, fingers staying on top (MG-059).
- **كيف / how:** MG-053: planar track + corner pin with matched grain and blur; no fake certificates/ads. MG-059: four-point corner pin + finger masks + their shadow. Local: 4-corner keyframes (manual or OpenCV homography) -> CSS matrix3d per frame or ffmpeg perspective filter; add matching noise.
- **أرقام / params:** 6 s each
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-tracking-compositing.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### FOOT-145 · MG-058 تجميد شخص واستمرار الخلفية · MG-058 Freeze the subject, keep the world moving · 📄 موصوف
- **ماذا / what:** A performer freezes inside a frame while a short background keeps moving - highlights a sports/art moment.
- **كيف / how:** 0-1 s motion, 1-3 s subject frozen, 3-4 s return; freeze frame of the person + mask + clean plate where needed; check the ghost of the original body in the background (it is not removed automatically). Local: ffmpeg frame extract + segmentation alpha overlaid on the running plate.
- **أرقام / params:** 4 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-tracking-compositing.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### FOOT-146 · MG-078 صورة أرشيف تنفتح على الحاضر · MG-078 Archive photo opens onto the present · 📄 موصوف
- **ماذا / what:** An old print's frame expands until it matches the same place in modern footage, then dissolves.
- **كيف / how:** 0-2 photo, 2-5 match, 5-8 modern scene; perspective corner pin + scale, then a tuned dissolve; show the photo date and avoid implying a false location match. Sound moves from old to modern ambience.
- **أرقام / params:** 8 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-cinematic-titles.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### FOOT-147 · MG-092 أثر حركة رياضي متدرج · MG-092 Chronophotography ghost poses · 📄 موصوف
- **ماذا / what:** Three frozen, spaced poses show the phases of a jump or throw around the athlete, then motion resumes.
- **كيف / how:** 0-1 action, 1-3 poses appear, 3-5 back to motion; frozen and isolated frames with opacity and a colour gradient. The copies are time markers, not extra people. Local: ffmpeg frame extraction + person segmentation (needs install).
- **أرقام / params:** 5 s; 3 poses
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-music-sports.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### FOOT-148 · زوايا تصوير دون إظهار الوجه · Faceless framing kit · 📄 موصوف
- **ماذا / what:** Setups for creators who don't show their face: top-down desk (hands, keyboard, notes), over-the-shoulder onto the monitor, chest-down frontal, objects and space (monitor glow, coffee, empty chair, window), side view of hands; review every clip and tag any with a face visible even for one frame (suff…
- **كيف / how:** Shot-list guidance; auto-tag or blur faces locally with a detector (OpenCV/MediaPipe - needs install) and ffmpeg boxblur over the box.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2447-akbun-vlog-shootplan/SKILL.md`

#### FOOT-149 · تشخيص قبل تكبير الصورة · Upscale triage · 📄 موصوف
- **ماذا / what:** Diagnose before upscaling: jagged edges from low resolution -> yes; uniform blur from missed focus -> no; JPEG blocks or high-ISO noise -> partially; pixelated logo -> fetch the vector instead; re-export from the original or vector at the right scale whenever possible; never overwrite the source (sa…
- **كيف / how:** Check resolution with ffprobe/PIL; modest scaling with Lanczos (ffmpeg scale flags=lanczos); AI upscalers need install (Real-ESRGAN) or keys (Freepik/Magnific).
- **الدليل / proof:** `kosif-atlas/skills/2976-pwdev-social-media/12579-asset-upscale/SKILL.md`

#### FOOT-150 · إزالة اللقطات المكررة · Footage de-duplication · 📄 موصوف
- **ماذا / what:** Embed frames or stills and cluster near-duplicates to thin a footage/photo pool before a montage.
- **كيف / how:** FiftyOne brain compute_similarity with mobilenet-v2 (needs install, app must run); lightweight local alternative: perceptual hash (dHash) with PIL + numpy, which runs here.
- **الدليل / proof:** `kosif-atlas/skills/3385-fiftyone/13900-fiftyone-find-duplicates/SKILL.md`

#### FOOT-151 · تجميع اللقطات المكررة · Duplicate-take grouping · 📄 موصوف
- **ماذا / what:** Clips shot within 2 minutes whose middle-frame luma histograms correlate ≥0.9 are duplicates; keep the sharpest/best-exposed/most stable one after user confirmation.
- **كيف / how:** ffmpeg mid-frame extract; histogram correlation in numpy
- **أرقام / params:** Δt ≤ 2 min; corr ≥ 0.9
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2454-davinciresolve-cut-travelflow/SKILL.md`

#### FOOT-152 · التثبيت عند ثبوت الاهتزاز فقط · Stabilisation only when measured shaky · 📄 موصوف
- **ماذا / what:** Stabilise only clips whose inter-frame motion is measurably jittery; prefer similarity mode (less warping) and check crop ≤10%.
- **كيف / how:** Resolve Stabilizer: Mode Similarity, Cropping Ratio 0.5 (raise by 0.1 if crop >10% or edges bend), Smooth 0.25, Strength 1.0, Zoom on. ffmpeg local: vidstabdetect=shakiness=5:accuracy=15 -> vidstabtransform=smoothing=30:zoom=0:optzoom=1,unsharp=5:5:0.8 (libvidstab present) or deshake.
- **أرقام / params:** Resolve 0.5/0.25/1.0; crop ≤10%
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2454-davinciresolve-cut-travelflow/SKILL.md`

#### FOOT-153 · مفتاح اللون الأخضر · Chroma key green screen · 📄 موصوف
- **ماذا / what:** Remove a green/blue background and composite over new footage or graphics.
- **كيف / how:** [fg]chromakey=0x00FF00:similarity=0.10..0.18:blend=0.05..0.1,despill=type=green[k];[bg][k]overlay ; YUV sources prefer chromakey, RGB use colorkey; Remotion/HTML alternative with WebM alpha
- **أرقام / params:** similarity 0.1-0.18; blend 0.05-0.1
- **الدليل / proof:** `kosif-atlas/skills/235-mas-video-lab/754-ffmpeg/SKILL.md`

#### FOOT-154 · إزالة التشويش والتوضيح · Video denoise and sharpen · 📄 موصوف
- **ماذا / what:** Clean low-light noise and restore edge clarity before grading.
- **كيف / how:** hqdn3d=4:3:6:4.5 (fast), nlmeans=s=3..5 (slow, better), then unsharp=5:5:0.6; for archival: chromanr
- **الدليل / proof:** `kosif-atlas/skills/235-mas-video-lab/754-ffmpeg/SKILL.md`

#### FOOT-155 · اختيار أكثر اللقطات حركة · Busiest-moment shot picking · 📄 موصوف
- **ماذا / what:** Rank footage segments by measured motion to fill beat slots, not guesses.
- **كيف / how:** ffmpeg frame-diff / scene score per second, pick top per bar.
- **الدليل / proof:** `kosif-atlas/skills/1511-homie/3903-video`

#### FOOT-156 · حماية النص فوق الفيديو · Text-over-footage protection · 📄 موصوف
- **ماذا / what:** Text over busy footage passes in some frames and fails in others; add protection.
- **كيف / how:** Dark scrim/gradient (black 40-60% opacity) behind caption band, solid pill box, or text shadow/stroke; sample luminance per frame with ffmpeg signalstats to verify.
- **أرقام / params:** scrim 40-60%
- **الدليل / proof:** `kosif-atlas/skills/1503-universal-design-principles/3825-legibility-contrast-and-spacing/SKILL.md`

#### FOOT-157 · تشخيص الحاجة لرفع الدقة قبل الإنفاق · Upscale diagnosis before spending · 📄 موصوف
- **ماذا / what:** Upscaling restores size and sharpness, not missing information.
- **كيف / how:** Jagged edges → upscale; uniform blur from missed focus → no; heavy JPEG blocks or high-ISO noise → partial; pixelated logo → find the SVG; save as name_upN.png and never overwrite the source; re-export from vector at the right scale first.
- **الدليل / proof:** `kosif-atlas/skills/2976-pwdev-social-media/12579-asset-upscale`

#### FOOT-158 · رسوم الحبر التراثية · Heritage ink-wash illustrations · 📄 موصوف
- **ماذا / what:** Sepia ink-wash style raster art of mountains, palms and sheep for the heritage look.
- **كيف / how:** WebP stills: hero 652x296, landscape 512x348, sheep 308x216.
- **أرقام / params:** sepia/parchment tones
- **الدليل / proof:** `kosif-earth-ci-fork/ui/art/hero.webp` · `kosif-earth-ci-fork/ui/art/landscape.webp` · `kosif-earth-ci-fork/ui/art/sheep.webp`

#### FOOT-159 · وصفات FFmpeg للعمليات · FFmpeg media operations recipes · 📄 موصوف
- **ماذا / what:** Lossless trim (-ss/-to -c copy), 16:9 -> 9:16 center crop (crop=ih*9/16:ih,scale=1080:1920), concat stitching, silence cut via auto-editor (threshold 4%), scene detection via scenedetect detect-adaptive, HEVC source handling.
- **كيف / how:** references/operations.md commands; prefer in-composition data-media-start / clip-path over physical re-encodes.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/media-use/references/operations.md`

#### FOOT-160 · محرك المونتاج الموجه · Directed-edit engine (directed.html) · 📄 موصوف
- **ماذا / what:** Turns an EDIT spec (from direct.py) over a talking-head plate into one timeline: per-shot slow push on the subject, keyword punches, three text levels, motifs, chapters and a deliberate end.
- **كيف / how:** direct.py writes edit.js (window.EDIT: shots, camera punches, captions, keys, motifs, chapters, payoff, credit, palette); directed.html builds the GSAP timeline; sizes designed at 1080 px width.
- **أرقام / params:** push per shot power1.inOut; punch expo.out 0.14 s then -60% over 0.6 s; hook dim .38 -> 0 in .55 s; ivory #F5F0E6; accent #E7B65A; end dim 0.32 s
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/templates/directed.html:44`

#### FOOT-161 · لقطات تحت النص · Footage plate under type · 📄 موصوف
- **ماذا / what:** Optional video plate: alternating push-in/ease-out per shot, kick nudges, payoff brightens, scrim keeps type legible; or one still image per section with slow push.
- **كيف / how:** verse.py fills {{PLATE}} and V.cuts / V.images.
- **أرقام / params:** push 1.04 -> 1.10 (odd shots 1.10 -> 1.04) smoothstep; kick +1.8%; brightness +22% x flare; images scale 1.04 -> 1.13
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/templates/verse.html:140` · `100-superskills/skills/kosif-montage-motion/templates/verse.html:202`

#### FOOT-162 · تغطية بي-رول · B-roll cover · 📄 موصوف
- **ماذا / what:** Cover silences and abstract explanation with real footage or 3D support.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/montage_grammar.md`

#### FOOT-163 · اتساق المواد · Material coherence rule · 📄 موصوف
- **ماذا / what:** One mood, one light, output shape, real resolution disclosed.
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/references/operating-manual.md`

#### FOOT-164 · ريلز تلقائي من مقطع متكلم · Auto reel from a talking clip · 📄 موصوف
- **ماذا / what:** One file in, a finished vertical reel out: transcription, cuts, captions in a chosen style and the speaker's credit.
- **كيف / how:** From the studio: recipe 'reel' (form in the الوصفات tab, POST /api/jobs {recipe:'reel', args} or MCP kosif_run); equivalent CLI `python scripts/kmotion.py reel …`.
- **أرقام / params:** clip (file); --out out/FINAL.mp4; --model large-v3|small|auto; --credit text; --style reels|tiktok|hormozi|boxed|minimal|cinema|punchy (default reels)
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:21`

#### FOOT-165 · مونتاج موجّه إلى مشروع قابل للتعديل · Directed edit → editable project · 📄 موصوف
- **ماذا / what:** Builds an editable composition project from a talking clip with word timing, camera moves and a climax, instead of a flat render.
- **كيف / how:** From the studio: recipe 'direct' (form in the الوصفات tab, POST /api/jobs {recipe:'direct', args} or MCP kosif_run); equivalent CLI `python scripts/kmotion.py direct …`.
- **أرقام / params:** clip; --name directed; --credit
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:25`

#### FOOT-166 · كشف القطعات · Shot-boundary detection · 📄 موصوف
- **ماذا / what:** Finds the cuts in a video and outputs shots as JSON, a contact sheet PNG, an optional timeline spec and optional split files.
- **كيف / how:** From the studio: recipe 'scenes' (form in the الوصفات tab, POST /api/jobs {recipe:'scenes', args} or MCP kosif_run); equivalent CLI `python scripts/kmotion.py scenes …`.
- **أرقام / params:** clip; --threshold 10 (0–100); --sheet out/shots.png; --timeline; --split DIR
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:45`

#### FOOT-167 · تمويه الوجوه أو منطقة · Face / region privacy masking · 📄 موصوف
- **ماذا / what:** Pixelates, blurs or boxes faces (tracked) or a fixed region with an optional time window; sound untouched.
- **كيف / how:** From the studio: recipe 'privacy' (form in the الوصفات tab, POST /api/jobs {recipe:'privacy', args} or MCP kosif_run); equivalent CLI `python scripts/kmotion.py privacy …`.
- **أرقام / params:** clip; --out out/safe.mp4; --mode pixelate|blur|box (default pixelate); --strength 18; --region x,y,w,h[,from,to]
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:48`

#### FOOT-168 · إزالة الترجمة المحروقة · Burned-in caption removal · 📄 موصوف
- **ماذا / what:** Removes subtitles already burned into a video.
- **كيف / how:** From the studio: recipe 'decaption' (form in the الوصفات tab, POST /api/jobs {recipe:'decaption', args} or MCP kosif_run); equivalent CLI `python scripts/kmotion.py decaption …`.
- **أرقام / params:** video; --out out/clean.mp4
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:80`

#### FOOT-169 · تثبيت الاهتزاز · Shake stabilisation · 📄 موصوف
- **ماذا / what:** Stabilises shaky handheld footage.
- **كيف / how:** From the studio: recipe 'stabilize' (form in the الوصفات tab, POST /api/jobs {recipe:'stabilize', args} or MCP kosif_run); equivalent CLI `python scripts/kmotion.py stabilize …`.
- **أرقام / params:** clip; --out out/steady.mp4
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/recipes.py:81`

#### FOOT-170 · كتالوج الكاميرات وطابعها · Camera body look catalog · 📄 موصوف
- **ماذا / what:** Camera names used as look cues in prompts.
- **كيف / how:** Name a body in the camera layer to imply its character.
- **أرقام / params:** ARRI Alexa 65 / Mini LF (skin, DR); RED V-Raptor 8K / Komodo 6K (global shutter); Sony Venice 2 (dual ISO, roll-off); IMAX 70mm; Hasselblad X2D; Blackmagic URSA 12K; DJI Ronin 4D; iPhone Pro / Pixel Pro; GoPro/FPV; VHS camcorder (lo-fi)
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-cinema-director/references/visual-catalog.md`

#### FOOT-171 · مخطط تحليل الفيديو إلى مشاهد · Video-to-scene analysis schema · 📄 موصوف
- **ماذا / what:** Schema for breaking existing footage into scenes for re-creation or editing (from the user's Cinema AI Director app).
- **كيف / how:** Sample ~12 evenly spaced frames (<= 1024 px); per scene start/end, shotType, cameraMotion, lighting, mood, start/end image prompts, video prompt; characters with best timestamp + face box (0-1000 normalised, crop with 20% padding); environments as style refs; scene N end frame = scene N+1 start. Implement with ffmpeg select + Claude vision.
- **أرقام / params:** 12 samples; 1024 px; bbox 0-1000; 20% padding
- **الدليل / proof:** `kosif-one/tools/kosif-omni/skills/kosif-prompt-master/references/books-drive-ledger.md`

#### FOOT-172 · قص دقيق إطارياً · Frame-accurate trim (re-encode) · 📄 موصوف
- **ماذا / what:** Cut at any frame by re-encoding the segment.
- **كيف / how:** ffmpeg -ss T -i in -to D -c:v libx264 -crf 18 -preset slow -c:a aac -b:a 192k -pix_fmt yuv420p -movflags +faststart
- **أرقام / params:** crf 18, aac 192k
- **الدليل / proof:** `100-superskills/skills/pro-video-editor-ffmpeg/references/ffmpeg-recipes.md`

#### FOOT-173 · قص بلا فقد على إطار مفتاحي · Lossless keyframe trim · 📄 موصوف
- **ماذا / what:** Stream-copy cut that only works on I-frames; otherwise 2-5 s frozen start.
- **كيف / how:** ffmpeg -ss T -i in -to D -c copy -avoid_negative_ts make_zero -movflags +faststart; check keyframes with probe.py --keyframes; else Smart-cut (re-encode only to nearest I-frame).
- **الدليل / proof:** `100-superskills/skills/pro-video-editor-ffmpeg/references/ffmpeg-recipes.md`

#### FOOT-174 · دمج بلا ترميز · Concat demuxer join · 📄 موصوف
- **ماذا / what:** Join same-codec clips without re-encode.
- **كيف / how:** printf file list > list.txt; ffmpeg -f concat -safe 0 -i list.txt -c copy -movflags +faststart
- **الدليل / proof:** `100-superskills/skills/pro-video-editor-ffmpeg/references/ffmpeg-recipes.md`

#### FOOT-175 · دمج مصادر مختلفة مع توحيد · Concat filter with normalisation · 📄 موصوف
- **ماذا / what:** Join heterogeneous clips by forcing fps, scale-cover crop and SAR.
- **كيف / how:** per input: fps=30,scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1 then concat=n=N:v=1:a=1
- **أرقام / params:** fps 30, 1920x1080
- **الدليل / proof:** `100-superskills/skills/pro-video-editor-ffmpeg/references/ffmpeg-recipes.md`

#### FOOT-176 · الوثائقي التوضيحي · Documentary Explainer · 📄 موصوف
- **ماذا / what:** Warm dark neutral with ivory and red/gold accent; slow Ken Burns on photos, divider lines scaleX, counting numbers, maps light up.
- **كيف / how:** Copy style sheet section into DESIGN.md, then build via claude-animation-studio render(t).
- **أرقام / params:** #15130F, #EFE6D8, #C0392B; Amiri 700 + IBM Plex Sans Arabic 500; Ken Burns 1.0->1.08 over 6 s
- **الدليل / proof:** `100-superskills/skills/trend-animation-styles/references/styles.md`

#### FOOT-177 · أنواع صور المتجر · Ecommerce image types · 📄 موصوف
- **ماذا / what:** Hero on white, lifestyle, detail, size comparison; product 85% of frame, no text on hero; real logo composited not generated.
- **أرقام / params:** 85% fill
- **الدليل / proof:** `100-superskills/skills/product-photo-mockups/SKILL.md:21`

#### FOOT-178 · استخراج مقاطع شورتس · Shorts candidate extraction with handles · 📄 موصوف
- **ماذا / what:** 20 candidates with in/out timecodes, frame conversion, pre/post handles feasibility (60 s + 2x15 s needs 90 s).
- **كيف / how:** DaVinci Resolve skill excerpt
- **الدليل / proof:** `100-superskills/skills/reels-shorts-factory/references/sources.md:148`

#### FOOT-179 · مونتاج على الإيقاع مع تلوين · Beat montage with grades · 📄 موصوف
- **ماذا / what:** Edit footage to a beat: quick ~1 s and breathing ~3 s shots, cuts on beats, breathing shots end on downbeats, most active window per clip, fill-crop, zoom punches on downbeats, grades, sidechain ducking.
- **كيف / how:** montage.py cut CLIPS --music TRACK / motion.py montage.
- **أرقام / params:** formats 9:16/16:9/1:1/4:5; punches 2× supersampled; grades teal_orange, golden_hour, cyberpunk, vintage_film (seeded grain), matrix_tech, clean_commercial, magma_night (+ blue_hour, sodium_night); -14 LUFS / -1 dBTP
- **الدليل / proof:** `kosif-studio/motion/references/hyperframes-authoring.md` · `kosif-studio/motion/montage.py:42`

#### FOOT-180 · دفع داخل صورة 2.5D · 2.5D photo push · 📄 موصوف
- **ماذا / what:** Photo split into 3 layers (sky, subject, foreground) with parallax push.
- **كيف / how:** 3 PNG layers; camera scale.
- **أرقام / params:** push 8% over 4 s
- **الدليل / proof:** `kosif-tool/playbooks/3d.md:46`

#### FOOT-181 · متحدث مع ترجمة · Talking-head + captions · 📄 موصوف
- **ماذا / what:** Keep speaker video untouched, captions in bottom safe area, emphasis words enlarged.
- **الدليل / proof:** `kosif-tool/playbooks/audio-sync.md:53`

#### FOOT-182 · مونتاج إيقاعي · Beat-cut montage · 📄 موصوف
- **ماذا / what:** Clips change on strong beats, each trimmed to most active section.
- **أرقام / params:** 15 frames per clip
- **الدليل / proof:** `kosif-tool/playbooks/music.md:47`

#### FOOT-183 · انضباط ترخيص الصور · Image licensing discipline · 📄 موصوف
- **ماذا / what:** Allowed: user/client-confirmed, PD/CC0, CC BY with attribution, receipted stock; banned: reference frames, scraped, ND, NC commercial, editorial in ads; model releases; AI images only when asked and declared; ASSETS.md row per file.
- **الدليل / proof:** `kosif-tool/playbooks/photos.md:11`

#### FOOT-184 · متى نتجاوز البارالاكس · Skip-parallax threshold · 📄 موصوف
- **ماذا / what:** Use clean Ken Burns if source too small or subject inseparable.
- **أرقام / params:** long side < 1600 px → no parallax
- **الدليل / proof:** `kosif-tool/playbooks/photos.md:9`

#### FOOT-185 · ترتيب العمق والعنوان بين الطبقات · Fixed depth order with title sandwich · 📄 موصوف
- **ماذا / what:** Background, mid, cut-out subject, graphics; title between background and subject.
- **أرقام / params:** ≤ 3 layers
- **الدليل / proof:** `kosif-tool/playbooks/photos.md:18-19`

#### FOOT-186 · إخفاء الحواف · Edge-hiding oversize + blurred backplate · 📄 موصوف
- **ماذا / what:** Oversize each layer and place blurred enlarged background copy behind.
- **كيف / how:** Remotion scale (1+(zoom−1)·d)·(1.04+0.12·d).
- **أرقام / params:** oversize 2× max travel + 4%; backplate 1.3× blur 24 px
- **الدليل / proof:** `kosif-tool/playbooks/photos.md:20` · `kosif-tool/playbooks/photos.md:129`

#### FOOT-187 · تمويه العمق · Depth blur cue · 📄 موصوف
- **ماذا / what:** Blur proportional to simulated distance behind focal layer; never blur subject.
- **أرقام / params:** ~1 px per 100 px distance; sample blur bg 3, mid 1
- **الدليل / proof:** `kosif-tool/playbooks/photos.md:22` · `kosif-tool/playbooks/photos.md:151-153`

#### FOOT-188 · تدرج خلف النص على الصور · Gradient scrim for text on photos · 📄 موصوف
- **ماذا / what:** Text on busy photo sits on a gradient scrim, not a black box.
- **أرقام / params:** opacity 0.6→0 over 35% frame height; contrast ≥ 4.5:1; min text 36 px
- **الدليل / proof:** `kosif-tool/playbooks/photos.md:23` · `kosif-tool/playbooks/photos.md:197`

#### FOOT-189 · قاعدة دقة المصدر · Source resolution rule · 📄 موصوف
- **ماذا / what:** Long side ≥ 1.5× displayed size at max scale.
- **أرقام / params:** 1080×1920 at 1.12 → ~2400 px long side
- **الدليل / proof:** `kosif-tool/playbooks/photos.md:26`

#### FOOT-190 · كين بيرنز الصحيح · Ken Burns done well · 📄 موصوف
- **ماذا / what:** Constant-velocity push/pan, alternating moves, no eased stops; pans RTL for Arabic.
- **كيف / how:** linear or cubic-bezier(0.37,0,0.63,1) before cut.
- **أرقام / params:** 1.00→1.06 over 4–6 s (1–1.5%/s); ceiling 1.12; pan < 6% width
- **الدليل / proof:** `kosif-tool/playbooks/photos.md:32`

#### FOOT-191 · معاملات البارالاكس المستوي · Planar parallax depth factors · 📄 موصوف
- **ماذا / what:** Layer offset = camera offset × depth factor; same direction; intentional move + perpetual two-sine drift.
- **كيف / how:** x = 6·sin(2πt/7)+4·sin(2πt/11); y periods 9 s/13 s.
- **أرقام / params:** bg 0.15, mid 0.45, subject 1.0, occluder 1.4; zoom ≤ 1.10; move 1200–2400 ms cubic-bezier(0.45,0,0.55,1); drift ≤ 12 px; pans 30–60 px/s; push 1.5–3%/s; rotation ≤ 0.3°/s
- **الدليل / proof:** `kosif-tool/playbooks/photos.md:34`

#### FOOT-192 · وصفة الثبات الوثائقي · Documentary hold recipe · 📄 موصوف
- **ماذا / what:** One photo with linear push/pan and right-entering lower third.
- **أرقام / params:** 0–400 enter; 0–4500 push 1.055 pan 4%; 600–1100 lower third feather 1.5%; exit 4200–4500, next at 4433
- **الدليل / proof:** `kosif-tool/playbooks/photos.md:48-55`

#### FOOT-193 · وصفة كشف بارالاكس ثلاثي · Three-layer parallax reveal recipe · 📄 موصوف
- **ماذا / what:** Layers fade, subject pops, 40 px pan, title slides between bg and subject, drift.
- **أرقام / params:** bg scale 1.15 mid 1.06; subject 200–800 spring 14/120; pan 400–2600; title 900–1400; push 1.5%/s
- **الدليل / proof:** `kosif-tool/playbooks/photos.md:57-65`

#### FOOT-194 · من الكولاج إلى صورة البطل · Collage to hero · 📄 موصوف
- **ماذا / what:** 2×3 grid enters from top-right, drifts, collapses to one hero photo.
- **أرقام / params:** 60 ms stagger 400 ms; drift 20 px; exits 250 ms 40 ms stagger; hero push 1.06
- **الدليل / proof:** `kosif-tool/playbooks/photos.md:67-74`

#### FOOT-195 · قواعد الصور للعربية · RTL photo layout rules · 📄 موصوف
- **ماذا / what:** Reveals RTL, grids from top-right, subject left/text right, never mirror photos with writing/flags/logos/steering; pills inherit layer transform.
- **أرقام / params:** margins 5%/12%
- **الدليل / proof:** `kosif-tool/playbooks/photos.md:193-199`

#### FOOT-196 · رسم يدوي فوق الفيديو · Hand-drawn style on twos over live video · 💡 فكرة
- **ماذا / what:** Doodle arrows/circles over footage animated on twos with boil to feel hand-made.
- **كيف / how:** Overlay SVG/canvas layer composited with ffmpeg overlay; seed changes every 2 frames.
- **الدليل / proof:** `kosif-atlas/skills/2414-animation/9355-learn-style` · `kosif-atlas/skills/2712-remotion/10436-remotion-markup/text-highlights.md`

#### FOOT-197 · ومضات كولاج · Photo-collage flash beat · 💡 فكرة
- **ماذا / what:** Scanned detail crops flash in on a fixed tempo with click per hit.
- **كيف / how:** Hard-cut crops per 300 ms.
- **أرقام / params:** 300 ms tempo
- **الدليل / proof:** `style:pm-abderrahmen-g-9e8ed0`
