# أدوات المجال `image` (12 أداة)

> مولّد من `data/tools.json`. [الفهرس الرئيسي](../README.md) · `python3 scripts/hub.py tool <id>` للبطاقة الحية.

### `app-studio` — استوديو التطبيقات للصور والتصميم / App Studio photo & design CLI

| الحقل | القيمة |
|---|---|
| المسار | `scripts/app_studio.py` (جذر: skill) |
| المجال | `image` |
| الدليل | `tested-here` |
| العائلات | `app-feature-transfer`, `photo-video-footage`, `media-image-audio`, `typography-arabic` |

**ما تفعله:** أداة سطر أوامر واحدة تضم 104 عمليات للصور والتصميم والخطوط والتوليد الإجرائي والتنزيل، مستوحاة من برامج سطح المكتب مثل DxO وLightroom وCapture One وACDSee وJPEGmini وAffinity وXara وFontLab وHoudini وAnimate وIDM وCanva، إضافة إلى حزمة الرسم (43 عملية). تكتب معظم العمليات ملف ناتج، وتطبع كل عملية سطر JSON واحدًا فيه اسم العملية والناتج والمقاييس وعلامة التحقق.

**What it does:** One command line with 104 photo, design, font, procedural and download operations modelled on desktop apps (DxO, Lightroom, Capture One, ACDSee, JPEGmini, Affinity, Xara, FontLab, Houdini, Animate, IDM, Canva, plus the 43-op painting batch). Most ops write an output file, and every run prints one JSON line with the op, output, metrics and a verified flag.

#### متى تُستدعى

- «نضّف الصورة دي من الضباب وظبّط الإضاءة والألوان»
- «أبي أضغط صور المتجر كلها بدون ما تخرب الجودة»
- «Add an Arabic watermark to every photo in this folder»
- «اعمل لي بوست إنستغرام بنص عربي من قالب JSON وبعدين كبّره لكل المنصات»
- «Check this font's Arabic coverage and subset it to WOFF2»
- «Animate this Arabic title into a GIF or MP4»

#### الأوامر

- **--help**: Prints the usage docstring with examples.
  - `python3 scripts/app_studio.py --help`
- **doctor**: Lists every op as ready or missing, the pip install lines for what is missing, and whether Arabic shaping (raqm or reshaper fallback) is available.
  - `python3 scripts/app_studio.py doctor`
- **ops**: Lists the ops (name, APPX id, source app, params, Arabic name), filtered by an optional word.
  - `python3 scripts/app_studio.py ops font`
- **develop**: Applies white balance, exposure, tone curve and vibrance (Lightroom Basic style).
  - `python3 scripts/app_studio.py develop ./in.jpg -o ./out/out.jpg --set wb=grey exposure=0.3 curve=s vibrance=0.25`
- **dehaze**: Removes haze with the dark-channel prior and reports contrast before and after.
  - `python3 scripts/app_studio.py dehaze ./in.jpg -o ./out/clear.jpg --set strength=0.95`
- **jpegmini**: Finds the smallest JPEG quality whose SSIM stays within delta of q95; marked verified when the SSIM target is met.
  - `python3 scripts/app_studio.py jpegmini ./in.jpg -o ./out/small.jpg --set delta=0.01`
- **watermark**: Stamps a text watermark (Arabic shaped) or a logo with the given opacity and position.
  - `python3 scripts/app_studio.py watermark ./in.jpg -o ./out/wm.jpg --set text="© كسيف" opacity=0.4 pos=br`
- **design**: Renders a Canva-style JSON template (size, background, text/image/rect/ellipse/line elements, Arabic text effects) to PNG, JPG or PDF and checks that each text fits.
  - `python3 scripts/app_studio.py design ./post.json -o ./out/post.png`
- **resize-design**: Magic resize: writes one file per platform size (16 presets, or sizes=all) with smart, pad-blur or pad-color mode.
  - `python3 scripts/app_studio.py resize-design ./post.png -o ./out/sizes --set sizes=story,instagram-post`
- **text-anim**: Animates a text line (rise, typewriter, fade or pop) to a GIF, or to MP4 by piping frames into ffmpeg.
  - `python3 scripts/app_studio.py text-anim "مرحبا بكم" -o ./out/title.gif --set style=rise seconds=2 fps=24`
- **font-inspect**: Reports a font's family, style, glyph and code-point counts, Arabic letter coverage, GSUB/GPOS feature tags and whether it is variable (no kerning-pair list despite the ops text).
  - `python3 scripts/app_studio.py font-inspect proofs/_shared/fonts/Amiri-Regular.ttf`
- **font-subset**: Subsets a font to the given text or code points and saves TTF, WOFF or WOFF2 (flavor=woff2 also needs the brotli package, which doctor does not check).
  - `python3 scripts/app_studio.py font-subset proofs/_shared/fonts/Amiri-Regular.ttf -o ./out/amiri-sub.woff --set text="مرحبا بكم" flavor=woff`
- **catalog**: Indexes a photo folder into SQLite (path, size, EXIF, GPS, rating, keywords, dhash).
  - `python3 scripts/app_studio.py catalog ./photos -o ./out/photos.db`
- **search**: Searches a catalog database by word, minimum rating or camera.
  - `python3 scripts/app_studio.py search ./out/photos.db --set q=sunset`
- **rename**: Plans a batch rename from EXIF dates; it renames files only when dry=0.
  - `python3 scripts/app_studio.py rename ./photos --set pattern={date}_{n:04d}{ext} dry=1`
- **remove-bg**: Cuts the subject out with GrabCut around an optional box and saves a transparent PNG.
  - `python3 scripts/app_studio.py remove-bg ./in.jpg -o ./out/cutout.png --set box=100,90,120,120`
- **xmp**: Writes or merges an XMP sidecar (rating, label, keywords); without -o it writes <image>.xmp next to the photo, and read=1 only reads it.
  - `python3 scripts/app_studio.py xmp ./in.jpg -o ./out/in.xmp --set rating=4 keywords=sunset,beach`
- **batch**: Runs one op on every image in a folder (searched recursively) and prints one JSON summary with a failure count.
  - `python3 scripts/app_studio.py batch jpegmini ./photos -o ./out/small --set delta=0.01`
- **download**: Downloads a file in resumable parallel byte ranges with an optional sha256 check. This is the only op that uses the network.
  - `python3 scripts/app_studio.py download https://example.com/file.zip -o ./out/file.zip --set parts=6`
- **<any op>**: Every one of the 104 ops (dehaze, denoise, keystone, lens, hdr, faces, dedupe, trace, boolean, scatter, lsystem, font-build, tween, lottie, ik, collage, mockup, qr, palette, chart, pptx, print-pdf and the painting batch) runs with the same form: <op> IN [IN…] -o OUT [--set key=value …]; 'ops' prints them all with their parameters.
  - `python3 scripts/app_studio.py ops`

#### المتطلبات والأمان

- network: true
- optional: bin:ffmpeg, pip:arabic-reshaper, pip:brotli, pip:fonttools, pip:matplotlib, pip:python-bidi, pip:python-pptx, pip:segno, pip:shapely
- python: numpy, opencv-python-headless, pillow
- الأمان: network
- الموافقة: download fetches a user-supplied URL over the network (confirm the user has rights to the file). rename with dry=0 renames the user's files in place, and xmp without -o writes a sidecar next to the user's photo. text-anim to .mp4 runs ffmpeg. Installing missing pip packages (doctor prints the install lines) needs approval.
- الحدود: It uses classical OpenCV, Pillow and fontTools approximations of the named apps' features, with no AI models, no RAW decoding and no vendor parity; 'verified' is true only when an op measured its own postcondition, and doctor's 'ready' does not check brotli (WOFF2) or the YuNet model faces needs on OpenCV 5.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_app_studio.py`
- `.claude/skills/kosif-superpowers/evals/test_app_studio_paint.py`
- مرجع: `.claude/skills/kosif-superpowers/references/app-feature-transfer.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/image.md`
- مرجع: `.claude/skills/kosif-superpowers/references/powers/app-feature-transfer.md`
- مرجع: `.claude/skills/kosif-superpowers/proofs/windows-installers-rea/CANVA_DESIGN_2026-10-19.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:app-studio --evidence <ملف>`.

### `app-studio-paint` — حزمة الرسم في استوديو التطبيقات / App Studio painting batch

| الحقل | القيمة |
|---|---|
| المسار | `scripts/app_studio_paint.py` (جذر: skill) |
| المجال | `image` |
| الدليل | `tested-here` |
| العائلات | `app-feature-transfer`, `color-palette-grading`, `hand-drawn-draw-on`, `photo-video-footage` |

**ما تفعله:** وحدة بايثون تسجّل 43 عملية رسم داخل app_studio.py: ثلاثين مؤثرًا من Paint.NET، وصورًا كسيرية (فراكتال) لمجموعتي جوليا وماندلبروت، وأربعةً وعشرين وضعًا للمزج، وتسطيح مكدس الطبقات إلى PNG أو تصديره بصيغة OpenRaster، وصناعة جداول LUT بصيغة ‎.cube وتطبيقها، واستبدال السماء، والتسييل، وتمويه العدسة حسب العمق، وفرش برنامج الرسّام (MS Paint)، والتعبئة بالدلو، وصفحات التلوين، والملصقات.

**What it does:** A Python module that registers 43 painting ops in app_studio.py: 30 Paint.NET effects, Julia and Mandelbrot fractals, 24 blend modes, layer stacks to PNG or OpenRaster, .cube LUT making and applying, sky replacement, liquify, depth lens blur, MS Paint style brushes, bucket fill, coloring book pages and stickers.

#### متى تُستدعى

- «حوّل الصورة دي لرسم زيتي أو رسم بالرصاص»
- «ابغى فلتر سينمائي LUT تيل وأورنج وأطبّقه على صوري»
- «Replace the sky in this photo with a sunset»
- «Blend these two images with soft-light at 80% opacity»
- «اعمل صفحة تلوين للأطفال من الصورة دي»
- «Paint watercolor brush strokes from a JSON file into a PNG»

#### الأوامر

- **import**: app_studio.py loads the module and calls register(globals()). The return value {effects, blend_modes, brushes} is exposed as app_studio.PAINT_BATCH.
  - `python3 -c "import sys; sys.path.insert(0,'scripts'); import app_studio; print(app_studio.PAINT_BATCH['effects'])"`
- **ops paint**: Lists the painting ops with their APPX ids, parameters and Arabic names. Use the filter 'Paint.NET' for only the effects and fractals, or 'Photoshop' for the 7 Photoshop ops.
  - `python3 scripts/app_studio.py ops paint`
- **oil-paint**: Applies one Paint.NET effect. The same form runs all 30 effects (ink-sketch, twist, zoom-blur, crystallize, levels and the rest).
  - `python3 scripts/app_studio.py oil-paint ./in.jpg -o ./out/oil.jpg --set brush=4 coarseness=24`
- **blend**: Composites a top image over a base with one of 24 Photoshop-style blend modes.
  - `python3 scripts/app_studio.py blend ./base.jpg ./top.png -o ./out/blend.png --set mode=soft-light opacity=0.8`
- **layers**: Flattens a JSON layer stack (image or colour layers with opacity, mode and offset) to PNG, or writes an OpenRaster .ora that GIMP and Krita open.
  - `python3 scripts/app_studio.py layers ./layers.json -o ./out/art.ora`
- **lut-make**: Writes a 3D .cube LUT for one of 10 looks and checks it with a round trip.
  - `python3 scripts/app_studio.py lut-make - -o ./out/teal.cube --set look=teal-orange`
- **lut**: Applies any 3D .cube LUT to an image with an amount control.
  - `python3 scripts/app_studio.py lut ./in.jpg -o ./out/graded.jpg --set cube=./out/teal.cube`
- **sky-replace**: Detects the sky region and replaces it with a preset gradient or a sky image, with feathering and colour harmonizing.
  - `python3 scripts/app_studio.py sky-replace ./in.jpg -o ./out/sky.jpg --set sky=sunset`
- **liquify**: Warps the image with push, pinch, bloat or twirl, or with a list of steps from ops=liquify.json.
  - `python3 scripts/app_studio.py liquify ./in.jpg -o ./out/liq.jpg --set mode=twirl cx=0.5 cy=0.5 radius=0.3 strength=0.6`
- **lens-blur**: Blurs by depth with polygonal bokeh, using a depth map or an automatic bottom-near ramp.
  - `python3 scripts/app_studio.py lens-blur ./in.jpg -o ./out/lensblur.jpg --set depth=auto focus=0.8 radius=14`
- **paint**: Draws JSON strokes with 11 brushes (pencil, calligraphy, airbrush, oil, crayon, marker, watercolor, eraser and others).
  - `python3 scripts/app_studio.py paint ./strokes.json -o ./out/drawing.png`
- **fill**: Bucket fill from a seed point, contiguous or global, with a tolerance.
  - `python3 scripts/app_studio.py fill ./in.jpg -o ./out/fill.png --set x=10 y=10 color=#ff0000 tolerance=10`
- **coloring-book**: Turns a photo into a clean black-and-white line page for colouring.
  - `python3 scripts/app_studio.py coloring-book ./in.jpg -o ./out/coloring.png`
- **sticker**: Cuts out the subject (or uses the PNG alpha) and adds a white border and a drop shadow, saved as a transparent PNG.
  - `python3 scripts/app_studio.py sticker ./in.jpg -o ./out/sticker.png --set box=90,50,140,140 border=12`
- **julia**: Renders a Julia set fractal. mandelbrot works the same way.
  - `python3 scripts/app_studio.py julia - -o ./out/julia.png`

#### المتطلبات والأمان

- python: numpy, opencv-python-headless, pillow
- الأمان: writes-files
- الموافقة: None beyond installing numpy, opencv-python-headless or pillow if they are missing: each op only reads its inputs and writes its -o output (sticker also writes and deletes a temporary <name>_cutout.png beside it).
- الحدود: It uses classical numpy and OpenCV re-implementations of Paint.NET, Photoshop and MS Paint features (sky and subject masks are heuristics, not AI), the results are not pixel-identical to those apps, and the module cannot run without app_studio.py.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_app_studio_paint.py`
- مرجع: `.claude/skills/kosif-superpowers/references/app-feature-transfer.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/image.md`
- مرجع: `.claude/skills/kosif-superpowers/references/powers/app-feature-transfer.md`
- مرجع: `.claude/skills/kosif-superpowers/proofs/windows-installers-rea/PAINT_PHOTOSHOP_BLENDER_2026-10-20.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:app-studio-paint --evidence <ملف>`.

### `design-tells` — كاشف علامات التصميم المولّد: فحص حتمي لصفحات HTML/CSS / Design tells: deterministic audit of HTML/CSS for the look every AI-generated page shares

| الحقل | القيمة |
|---|---|
| المسار | `scripts/design_tells.py` (جذر: skill) |
| المجال | `image` |
| الدليل | `tested-here` |
| العائلات | `ui-product-device`, `qa-verification`, `typography-arabic` |

**ما تفعله:** يفحص HTML وCSS بـ19 قاعدة (خط عام واحد، تدرج بنفسجي أزرق، بطاقات داخل بطاقات، تباين ضعيف، إيموجي، كل شيء في المنتصف، عبارات تسويقية جاهزة، عربي بلا خط عربي أو بلا RTL…) ويعطي درجة من 100 وإصلاحًا لكل علامة.

**What it does:** Scans HTML and CSS (inline, <style>, linked local sheets, CSS variables resolved) with 19 fixed rules: one generic sans for everything, purple-to-blue gradients, gradient heading text, cards nested in cards, grey text on colour, WCAG contrast below 4.5:1, an icon tile above every heading, emoji bullets, everything centred, one radius everywhere, heavy shadows, repeated glass blur, stock hype copy, placeholder images, Arabic text with a Latin-only font or without RTL, fade-in on everything, too many accent hues and no reduced-motion rule. Scores out of 100 with a fix per hit; exit 3 = REVISE.

#### متى تُستدعى

- «افحص الصفحة دي هل شكلها معمول بالذكاء الاصطناعي»
- «راجع تصميم الموقع قبل التسليم»
- «Audit this landing page for AI-slop design»
- «Is this Arabic page RTL with an Arabic font?»

#### الأوامر

- **audit**: Score and fixes; exit 3 = REVISE.
  - `python3 scripts/design_tells.py audit index.html`
- **rules**: The rule table.
  - `python3 scripts/design_tells.py rules`

#### المتطلبات والأمان

- الأمان: read-only
- الموافقة: Reads only the given files; never edits them.
- الحدود: Pattern rules find candidates and can be wrong; layout, imagery and taste still need a browser look at phone and desktop width.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_v58_mastery.py`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A38-v58-thinking-books-github-pulse.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:design-tells --evidence <ملف>`.

### `font-fidelity-lab` — مختبر مطابقة الخطوط العربية / Arabic-aware font fidelity lab

| الحقل | القيمة |
|---|---|
| المسار | `scripts/font_fidelity_lab.py` (جذر: skill) |
| المجال | `image` |
| الدليل | `tested-here` |
| العائلات | `typography-arabic`, `typography-latin` |

**ما تفعله:** يفحص خصائص OpenType لخط مرخّص: تغطية أحرف العبارة، وجداول GSUB وGPOS، والمحاور المتغيرة، واسم العائلة. ويرتّب مجلدًا من خطوط TTF/OTF مقارنةً بقصاصة دقيقة لنص مرجعي، إذ يرسم العبارة نفسها بتشكيل libraqm ويحسب نسبة تقاطع الأقنعة إلى اتحادها (IoU) بعد توحيد المقاس. والناتج قائمة مرشحين بصيغة JSON، لا ادعاء بتحديد الخط.

**What it does:** Inspects a licensed font's OpenType facts: cmap coverage of a phrase, GSUB/GPOS, variable axes and family name. It also ranks a folder of TTF/OTF fonts against a tight crop of reference text by rendering the same phrase with libraqm shaping and scoring normalized mask IoU. The output is JSON candidates, never a claimed identification.

#### متى تُستدعى

- «إيه أقرب خط للكتابة اللي في الصورة دي؟»
- «افحص ملف الخط ده: يدعم كل حروف «جمعة مباركة»؟»
- «أبي أطابق خط العنوان العربي من لقطة الشاشة مع خطوطي»
- «Rank my licensed fonts against this cropped Arabic title»
- «Inspect this TTF for Arabic coverage, GSUB/GPOS and variable axes»

#### الأوامر

- **inspect**: Prints font_fidelity_inspection_v1 JSON with file size, missing codepoints for --text (default «جمعة مباركة»), cmap size, GSUB/GPOS presence, fvar axes and family. Accepts .ttf/.otf/.woff/.woff2 (WOFF2 also needs brotli).
  - `python3 scripts/font_fidelity_lab.py inspect proofs/_shared/fonts/Amiri-Regular.ttf --text "جمعة مباركة"`
- **rank**: Renders --text in every .ttf/.otf found recursively under --fonts at 5 sizes (48–128) and compares it with the crop in both polarities. Prints font_fidelity_ranking_v1 with candidates sorted by IoU, best_size and status candidate_only or unsupported:<reason>; --top is clamped to 1–50.
  - `python3 scripts/font_fidelity_lab.py rank ./crop.png --text "جمعة مباركة" --fonts proofs/_shared/fonts --top 5`

#### المتطلبات والأمان

- optional: pip:brotli, pip:fonttools
- python: Pillow
- الأمان: read-only
- الموافقة: —
- الحدود: It ranks how closely each candidate renders one phrase (binary mask IoU at 5 fixed sizes) and does not identify an unknown proprietary typeface or prove an exact match.

#### الاختبارات والأدلة

- `tests/test_font_fidelity_lab.py`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/image.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:font-fidelity-lab --evidence <ملف>`.

### `image-local-ai` — ذكاء الصور المحلي: إزالة الخلفية والملء الذكي بنموذج ONNX تختاره / Local image AI: remove background and smart fill with your own ONNX model

| الحقل | القيمة |
|---|---|
| المسار | `scripts/image_local_ai.py` (جذر: skill) |
| المجال | `image` |
| الدليل | `tested-here` |
| العائلات | `media-image-audio`, `typography-arabic` |

**ما تفعله:** يشغّل نماذج صور مفتوحة على الجهاز بلا شبكة: قناع موضوع بأسلوب BiRefNet يتحول إلى PNG شفاف (remove-bg) وملء ذكي بأسلوب MI-GAN لمنطقة محددة بقناع (inpaint). يعرض النماذج الثلاثة التي يثبتها مصمم (BiRefNet lite وSAM 2.1 tiny وMI-GAN) بروابط مثبتة وأحجام وبصمات SHA-256، ويتحقق من الملف المنزّل. لا ينزّل شيئًا أبدًا: إن غاب النموذج يطبع الرابط ويطلب من المستخدم تنزيله.

**What it does:** Runs open image models on this machine with no network: a BiRefNet-style subject matte turned into an RGBA PNG (remove-bg) and MI-GAN-style inpainting of a masked area (inpaint). It lists the three models Mosamem pins (BiRefNet lite MIT, SAM 2.1 tiny Apache-2.0, MI-GAN MIT) with commit-pinned URLs, sizes and SHA-256, and checks a downloaded file against its pin. It never downloads: with no model it prints the URL and asks the user to fetch it.

#### متى تُستدعى

- «شيل الخلفية من الصورة على جهازي من غير نت»
- «امسح الشخص ده من الصورة واملأ مكانه»
- «Remove the background offline with a local model»
- «Inpaint the masked area of this photo without uploading it»

#### الأوامر

- **models**: Lists the three pinned open models with licence, source, size, URL and SHA-256 (facts from Mosamem's models.rs); downloads nothing.
  - `python3 scripts/image_local_ai.py models --json`
- **verify-model**: SHA-256 of a local file against --sha256 or the known pin for its file name; exit 1 on mismatch, 2 if missing.
  - `python3 scripts/image_local_ai.py verify-model birefnet_lite_fp16.onnx`
- **remove-bg**: ImageNet-normalised input at the model's side, sigmoid matte, soft alpha; writes an RGBA PNG and prints JSON with coverage.
  - `python3 scripts/image_local_ai.py remove-bg --model birefnet_lite_fp16.onnx in.png out.png --mask-out matte.png`
- **inpaint**: Grows the white mask area ~2 model px, runs an image/mask uint8 model, pastes back only the user's hole; prints JSON.
  - `python3 scripts/image_local_ai.py inpaint --model migan_pipeline_v2.onnx --mask hole.png in.png out.png`

#### المتطلبات والأمان

- optional: pip:numpy, pip:onnxruntime, pip:pillow
- الأمان: writes-files
- الموافقة: Writes only the named output files. It never downloads; fetching a model (28–115 MB) from the printed URL is the user's own decision.
- الحدود: Tested here only with synthetic ONNX graphs, so it checks I/O and behaviour, not BiRefNet or MI-GAN quality; SAM 2.1 is listed but not wrapped; CPU only.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_image_local_ai.py`
- مرجع: `.claude/skills/kosif-superpowers/references/mosamem-arabic-image-editor.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:image-local-ai --evidence <ملف>`.

### `mosamem-rea-fusion` — تكامل مصمم وREA: فحص صور وتوليف مهارات آمن / Mosamem x REA source-safe image preflight and capability fusion

| الحقل | القيمة |
|---|---|
| المسار | `scripts/mosamem_rea_fusion.py` (جذر: skill) |
| المجال | `image` |
| الدليل | `tested-here` |
| العائلات | `software-investigation`, `media-image-audio`, `apps-artifacts` |

**ما تفعله:** جسر أصلي يربط أساليب مصمم v0.1.0 ومسارات REA: 19 عقدة موثقة، فحص ترويسة PSD وPNG وJPEG والبصمة، والتخطيط لتحليل REA بعد الإذن. لا يشغّل مصمم ولا ينسخ كوده.

**What it does:** Independent, standard-library Mosamem v0.1.0/REA workflow bridge: 19 upstream-anchored methodology nodes, actual read-only PSD/PSB/PNG/JPEG header preflight and SHA256, consent-gated REA plan via existing bridge. Does not install or control Mosamem, run REA or import GPL code.

#### متى تُستدعى

- «ادمج إمكانيات Mosamem وREA في KOSIF Superpowers»
- «عايز أشوف PSD عندي متوافق مع مصمم؟»
- «استخدم مهارات الطبقات والنص العربي مع تحريك فيديو»
- «inspect PSD header before opening in an image editor»
- «plan an authorized REA analysis before trying to modify a program»

#### الأوامر

- **doctor**: Checks known Mosamem installed paths and calls existing rea_bridge.environment() (node --version only); no third-party binaries invoked.
  - `python3 scripts/mosamem_rea_fusion.py doctor`
- **catalog**: Returns 19 source-anchored potential handoffs with truthful implementation status.
  - `python3 scripts/mosamem_rea_fusion.py catalog`
- **inspect**: Parses file headers, SHA-256 and known Mosamem PSD compatibility warnings; writes new JSON only when requested.
  - `python3 scripts/mosamem_rea_fusion.py inspect picture.psd --out ./preflight.json`
- **plan**: Builds typed, non-executed workflow with QA and permission gates.
  - `python3 scripts/mosamem_rea_fusion.py plan "تحرير صورة بالعربية وإزالة خلفية" --domain image`
- **rea-plan**: Calls the existing REA static inspection planner on the supplied path; no target execution.
  - `python3 scripts/mosamem_rea_fusion.py rea-plan javascript ./my-authorized-app`

#### المتطلبات والأمان

- binaries: python3
- optional: bin:node, bin:rea, external Mosamem GUI, not automated
- الأمان: writes-files
- الموافقة: The bridge itself never installs, uploads, renders, invokes REA analysis or controls Mosamem. Using Mosamem GUI, downloading model weights or executing REA via rea_bridge.py run requires separate approval and correct licenses.
- الحدود: Standard-library header preflight only; does not edit or decode PSD, PNG/JPEG; Mosamem v0.1.0 GUI has no verified headless API; external GPL code is not embedded and source-described capabilities are not installed inside KOSIF.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_mosamem_rea_fusion.py`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A16-mosamem-rea-capability-fusion.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:mosamem-rea-fusion --evidence <ملف>`.

### `prompt-forge` — مصنع البرومبتات: برومبتات طبقية وفحص البرومبت وقائمة لقطات بإطارات دقيقة / Prompt forge: layered generator prompts, prompt lint and frame-exact shot lists

| الحقل | القيمة |
|---|---|
| المسار | `scripts/prompt_forge.py` (جذر: skill) |
| المجال | `image` |
| الدليل | `tested-here` |
| العائلات | `ai-generation` |

**ما تفعله:** يبني برومبتات الصور والفيديو والموسيقى والصوت من مواصفة طبقية واحدة، ويفحص البرومبت (كلمات المبالغة، الصفات المبهمة، التناقض، النفي فقط، غياب الموضوع أو الكاميرا، الطول) بالعربية والإنجليزية، ويقسم المدة على لقطات بإطارات مجموعها مضبوط.

**What it does:** Builds still-image, video, music and voice prompts from one layered spec (subject, action, setting, style, camera, light, constraints) with no brand names; lints a prompt for hype words, vague adjectives, contradictions, negative-only phrasing, missing subject or camera and length in Arabic and English; splits a target duration into per-shot video prompts whose frame counts sum exactly to total x fps.

#### متى تُستدعى

- «اكتب لي برومبت صورة وفيديو لنفس المشهد»
- «افحص البرومبت ده وقولي غلطه فين»
- «قسّم فيديو 12 ثانية على 4 لقطات ببرومبت لكل لقطة»
- «Write image and video prompts for this scene»
- «Lint my generation prompt»
- «Make a shot list whose durations add up to 15 seconds»

#### الأوامر

- **forge**: Per-target prompts from the layered spec, with word counts and warnings (--text prints only the prompts).
  - `python3 scripts/prompt_forge.py forge /tmp/spec.json --targets still-image,video,music,voice`
- **lint**: Findings with severity and fix, score 0-100 and pass/revise/fail verdict.
  - `python3 scripts/prompt_forge.py lint /tmp/prompt.txt --target video`
- **shotlist**: Per-shot video prompts with start/end frames; largest-remainder split so frames sum exactly to total*fps.
  - `python3 scripts/prompt_forge.py shotlist /tmp/shots.json --fps 30 --total 12 --max-shot 10`
- **self-test**: Offline self-check.
  - `python3 scripts/prompt_forge.py --self-test`

#### المتطلبات والأمان

- الأمان: read-only
- الموافقة: —
- الحدود: Rule-based text checks and templates: it does not call any generator or judge image quality, its word lists are finite (Arabic and English only), and generator-specific parameters are left to the user.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_prompt_forge.py`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:prompt-forge --evidence <ملف>`.

### `prompt-pack` — حزمة المطالبات: كل مطالبة في كتلة كود قابلة للنسخ مع فحص يحذّر فقط / Prompt pack: copyable prompts, one code block each, with a warn-only lint

| الحقل | القيمة |
|---|---|
| المسار | `scripts/prompt_pack.py` (جذر: skill) |
| المجال | `image` |
| الدليل | `tested-here` |
| العائلات | `prompt-craft`, `verification-evals` |

**ما تفعله:** يحوّل قائمة مطالبات أو مواصفة مشاهد/قصة إلى PACK.md وpack.json: كل مطالبة إنجليزية في كتلة كود واحدة (داخل dir="ltr" للصفحات العربية) والشرح العربي خارجها، مع لاحقة لكل محرك من data/prompt_engines.json. الفحص يحذّر فقط (تناقضات، شخصيات بلا فصل، أسماء استوديوهات/فنانين/علامات، مبالغات الجودة، نص داخل الصورة، غياب السلبيات) ولا يغيّر أي كلمة؛ ويرفض ما يشبه الأسرار. لا يستدعي أي محرك.

**What it does:** Turns a list of prompts or a scene/story spec into PACK.md and pack.json: every English prompt in ONE fenced block (wrapped in dir="ltr" for RTL pages), the Arabic explanation outside it, and a per-engine suffix from data/prompt_engines.json (Midjourney V7 flags marked version-sensitive, generic image negative line, generic video 'No subtitles or on-screen text.'). The lint only warns (contradictions, unseparated subjects, studio/artist/brand names, quality hype, text-in-image, missing negative baseline) and never rewrites a word; credential-like values are refused. It calls no engine.

#### متى تُستدعى

- «اكتب البرومبتات على شكل كود أقدر أنسخه»
- «جهّز برومبتات المشاهد لميدجورني وفيو»
- «Give me the scene prompts as copyable code blocks for Midjourney and Veo»
- «Lint these prompts for contradictions without changing them»

#### الأوامر

- **build**: Writes PACK.md (one fenced block per prompt, Arabic explanation outside, engine suffix appended once), pack.json with the lint warnings, and START-HERE.md when prompts list refs; --strict exits 2 on warnings.
  - `python3 scripts/prompt_pack.py build prompts.json --out out/demo/prompts --engine midjourney`
- **lint**: Prints warn-only findings as JSON (exit 2 when any, 3 when a credential-like value is found); the input is never modified.
  - `python3 scripts/prompt_pack.py lint prompts.json`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: Writes only inside the --out folder (refuses the skill folder, jobs/ and git-tracked paths); it calls no engine, spends nothing and publishes nothing.
- الحدود: Engine syntax is documented, not tested on the engine here; the lint is a heuristic warning list, not a content-policy filter, and it deliberately never substitutes words.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_prompt_pack.py`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A17-story-scene-charter.md`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A4-fusionforge-composition.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:prompt-pack --evidence <ملف>`.

### `render-text` — أداة عرض النص بخطوط مرشّحة / Font candidate text renderer

| الحقل | القيمة |
|---|---|
| المسار | `scripts/render_text.cjs` (جذر: skill) |
| المجال | `image` |
| الدليل | `tested-elsewhere` |
| العائلات | `typography-arabic`, `typography-latin` |

**ما تفعله:** يعرض عينات نصية بملفات خطوط مرشّحة عبر متصفح Chromium بلا واجهة (بتشكيل HarfBuzz)، ويحفظ صورة PNG مقصوصة بإحكام لكل عنصر مع ملف renders.json بأبعاد صناديق النص، لمقارنة المرشّحين جنبًا إلى جنب مع خط المرجع.

**What it does:** Renders text samples in candidate font files through headless Chromium (HarfBuzz shaping) and saves one tightly cropped PNG per item plus a renders.json of box sizes, so the candidates can be compared side by side against a reference typeface.

#### متى تُستدعى

- «طابق لي الخط اللي في الفيديو ده بأقرب خط مفتوح»
- «اعرض الجملة دي بخطوط Amiri ونوتو نسخ عشان أقارن بينهم»
- «أبي أعرف وش أقرب خط لخط هالتصميم»
- «Render this Arabic line in several candidate fonts so I can compare them»
- «Which open font matches the typeface in my reference frame?»

#### الأوامر

- **render**: Takes two positional arguments (spec file, output folder). Embeds each item's font as a data URL, shapes the text in Chromium, screenshots the text box plus 12 px padding to ./out/<id>.png, writes ./out/renders.json and prints 'id: WxH' per item. --help prints usage; a wrong argument count prints usage and exits 2.
  - `node scripts/render_text.cjs ./spec.json ./out/`

#### المتطلبات والأمان

- binaries: chromium, node
- node: playwright
- الأمان: runs-external-programs
- الموافقة: Launches headless Chromium and writes or overwrites <id>.png and renders.json in the chosen outdir (ids are limited to letters, digits, '-', '_' and '.', so they cannot leave it). Item text is set as plain text; an item's optional html field is inserted as markup, so use it only with trusted specs, and use font files the user is licensed to use.
- الحدود: Produces render crops for side-by-side comparison only; it does not identify or score a matching font.

#### الاختبارات والأدلة

- لا اختبار مسجل: الشارة لا تتجاوز 📄 حتى يُختبر هنا.
- مرجع: `.claude/skills/kosif-superpowers/references/font-matching.md`
- مرجع: `fonts/kosif-jumuah/README.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/image.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/sources.md`
- مرجع: `.claude/skills/kosif-superpowers/references/powers/typography-arabic.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:render-text --evidence <ملف>`.

### `style-library` — مكتبة الأساليب: 586 أسلوبًا بصريًا بالاسم (86 من أطلس Futurepedia + 500 أصلي) — بحث ووصف وبرومنت وعينة وكتالوج PDF مصوّر / Style library — 586 visual styles by name (86 Futurepedia-derived + 500 original): find, describe, prompt, swatch, illustrated PDF catalog

| الحقل | القيمة |
|---|---|
| المسار | `scripts/style_library.py` (جذر: skill) |
| المجال | `image` |
| الدليل | `tested-here` |
| العائلات | `prompt-craft`, `color-palette-grading`, `texture-material` |

**ما تفعله:** يجد أي أسلوب من 586 بالرقم أو الاسم العربي أو الإنجليزي أو بكلمات حرة: 86 طريقة معاد صياغتها من أطلس Futurepedia و500 أسلوب أصلي من KOSIF في 20 مجموعة. يطبع بطاقة الأسلوب (الشكل والمنطق والألوان والملمس والتكوين)، ويملأ وصفة البرومنت لموضوعك مع أسلوب ثانٍ بنسبة 30% اختياريًا، ويرسم عينة SVG إجرائية ثابتة، ويبني كتالوجًا مصورًا HTML وPDF.

**What it does:** Looks up any of 586 visual styles by id, English or Arabic name or free words: the 86 paraphrased Futurepedia AI Style Atlas methods and 500 original KOSIF styles in 20 groups (Arabic heritage, world crafts, material fusion, scientific imaging, natural process, architecture, futures, print, optics, textile, edible media, toys, interfaces, cartography, motion and time, sound, folk art, type and calligraphy, generative systems, cinematic genres). Prints a style card (look, logic, palette, texture, composition), fills its prompt recipe for a subject with an optional 30% accent style, draws a deterministic procedural SVG swatch, and builds an illustrated catalog (HTML, and PDF through headless Chromium).

#### متى تُستدعى

- «عايز أسلوب زليج النجوم لصورة»
- «ورّيني أساليب الخط العربي النيون»
- «ابعت لي كتالوج الأساليب PDF»
- «Describe the Cyanotype Sunprint style and give me a prompt»
- «Find a visual style for a food poster»

#### الأوامر

- **groups**: Lists the 34 groups (14 Futurepedia families + 20 KOSIF groups) with counts.
  - `python3 scripts/style_library.py groups`
- **find**: Ranks styles by Arabic or English words over names, look, logic, motif and group.
  - `python3 scripts/style_library.py find "خط عربي نيون"`
- **describe**: Prints one style card by id, slug, English or Arabic name.
  - `python3 scripts/style_library.py describe KS-001`
- **prompt**: Fills the style's prompt recipe for a subject, with an optional 30% accent style and a negative line.
  - `python3 scripts/style_library.py prompt KS-001 --subject "a reading corner" --mix FA-12`
- **swatch**: Writes one deterministic procedural SVG sample (refuses to overwrite).
  - `python3 scripts/style_library.py swatch KS-001 --out out/styles/ks-001.svg`
- **catalog**: Writes every swatch and an illustrated index.html; with --pdf renders JPEG swatches and an A4 PDF through headless Chromium, and --split-groups adds one PDF per group.
  - `python3 scripts/style_library.py catalog --out out/styles/catalog --pdf out/styles/catalog.pdf --split-groups`
- **self-test**: Offline checks of the data, lookups, prompts and swatch determinism.
  - `python3 scripts/style_library.py self-test`

#### المتطلبات والأمان

- optional: node + playwright (Chromium) for catalog --pdf
- الأمان: writes-files
- الموافقة: Writes only to the output path or new/empty folder you name; refuses to overwrite; no network, no paid generator, no third-party media.
- الحدود: Swatches are procedural sketches of a style's palette, texture and composition, not finished artwork; the 500 KS styles are original descriptions written for this library and have not each been produced as a real film or image. For a finished frame, feed the prompt to an image tool you choose, or build the scene with the motion engines.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_style_library.py`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/image.md`
- مرجع: `.claude/skills/kosif-superpowers/references/protocol/A15-futurepedia-style-atlas.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:style-library --evidence <ملف>`.

### `telegram-typography-atlas` — مكتبة KOSIF الشاملة للخطوط وأفكار التصميم من صادرات تيليجرام / KOSIF Telegram Typography Atlas — private-safe font knowledge and idea search

| الحقل | القيمة |
|---|---|
| المسار | `scripts/telegram_typography_atlas.py` (جذر: skill) |
| المجال | `image` |
| الدليل | `tested-here` |
| العائلات | `typography-arabic`, `typography-latin` |

**ما تفعله:** ابحث في فهرس بيانات 5,514 خطًا فريدًا من صادرات تيليجرام الخاصة بك (4,634 تدعم العربية): صف لكل عائلة بأوزانها، وكلمات الأنماط بالعربي (كوفي، رقعة، ديواني، ثلث، نسخ) مع تسامح الإملاء، وفلتر للرخص المفتوحة، و16 اتجاهًا تصميميًا أصليًا. الخطوط والرسائل والصور والمسارات تبقى على جهازك فقط.

**What it does:** Search a public metadata index of the 5,514 SHA-256-distinct fonts found in the user's own Telegram Desktop exports (4,634 with Arabic letters): one row per family with its styles, Arabic spelling-tolerant style words (كوفي، رقعة، ديواني، ثلث، نسخ), an open-license filter, and 16 original design directions. scan/enrich-zips rebuild the index on the user's machine (bounded, in-memory ZIP reads); refresh re-derives tags, name-based license flags, ideas and counts from the public index alone. Fonts, chats, images and local paths never leave the device.

#### متى تُستدعى

- «Pick an Arabic or Latin font for a logo, poster, brand, reel or kinetic text from the fonts the user already collected»
- «Find open-license (OFL) candidates in a style before designing, then measure them with font-fidelity-lab»
- «اختار لي خط رقعة أو كوفي أو ديواني من مكتبة خطوطي لبوستر أو شعار مع حالة الرخصة»

#### الأوامر

- **find**: Read-only search of the public index: style tags and name words, one row per family (styles, file copies, license status), open-claimed licenses first on ties.
  - `python3 scripts/telegram_typography_atlas.py find --index data/telegram-typography-catalog-complete-20261020.json "خط رقعة" --arabic-only --limit 15`
- **find (open licenses only)**: Only fonts whose embedded name table claims OFL, Apache or public domain; --latin keeps fonts that also cover Latin (bilingual logos). Still unverified: confirm the license at the official source before use.
  - `python3 scripts/telegram_typography_atlas.py find --index data/telegram-typography-catalog-complete-20261020.json "kufi logo" --arabic-only --latin --license open`
- **doctor**: Says which commands this machine can run: find and refresh need nothing extra; scan needs beautifulsoup4, fonttools and Pillow; WOFF2 inside ZIPs needs brotli.
  - `python3 scripts/telegram_typography_atlas.py doctor`
- **refresh**: Re-derive whole-word tags, name-based license flags (trial/demo/personal use), design ideas, counts and limitations from the public index alone; never overwrites.
  - `python3 scripts/telegram_typography_atlas.py refresh --index data/telegram-typography-catalog-complete-20261020.json --out ./refreshed.json`
- **scan**: On the user's machine: index loose TTF/OTF fonts, chat themes and image headers of ChatExport* folders into a public file and a separate private locator; refuses overwrites and outputs inside the exports. The private locator must be written outside any git checkout (on Windows %LOCALAPPDATA%\KOSIF\typography-private); the command refuses otherwise.
  - `python3 scripts/telegram_typography_atlas.py scan --root ./my-telegram-exports --public-out ./new-public.json --private-out ~/.local/share/kosif/typography-private/private-new.json`
- **enrich-zips**: Add fonts found inside ZIP archives: decompression capped per member, traversal/absolute/encrypted members refused, nothing extracted; an already-enriched catalog is refused; ideas and counts rebuilt over all fonts.
  - `python3 scripts/telegram_typography_atlas.py enrich-zips --root ./my-telegram-exports --public ./new-public.json --private ~/.local/share/kosif/typography-private/private-new.json --new-public ./complete.json --new-private ~/.local/share/kosif/typography-private/private-complete.json`

#### المتطلبات والأمان

- optional: pip:fonttools, pip:beautifulsoup4, pip:Pillow, pip:lxml, pip:brotli
- الأمان: writes-files
- الموافقة: Read only the user's authorized exported chat backups. Never upload raw messages, senders, URLs, font bytes, photo assets or private file locations to GitHub; use only actually licensed fonts for production.
- الحدود: Metadata and message keyword themes, not understanding of every photo (2,981 image headers read; 80 photos sampled once). 4 exports, 2,766 messages, 1,269 loose font files and 5,283 font members in 89 ZIPs gave 5,514 distinct font binaries (~2,412 family names). 1 ZIP unreadable and 36 ZIP fonts unparsed; EOT/.glyphs members, RAR, PDF and nested archives not indexed. Message-theme counts come from the original on-device tagger. License labels come from embedded names only and never grant permission (534 flagged restricted, 402 of them by trial/demo/personal-use/unlicensed names). find and refresh need only Python; scan needs fonttools, beautifulsoup4 and Pillow (optional list), WOFF2 in ZIPs needs brotli.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/scripts/test_telegram_typography_atlas.py`
- مرجع: `.claude/skills/kosif-superpowers/references/telegram-typography-knowledge-library.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:telegram-typography-atlas --evidence <ملف>`.

### `unified-media` — محرر الوسائط الموحد: صور ورسم وتحريك وفيديو / Unified Media: photo adjustments + drawn overlays + GIF/MP4

| الحقل | القيمة |
|---|---|
| المسار | `scripts/unified_media.py` (جذر: skill) |
| المجال | `image` |
| الدليل | `tested-here` |
| العائلات | `photo-video-footage`, `hand-drawn-draw-on`, `shapes-morph-geometry` |

**ما تفعله:** تعديل الصور والتعريض ورسم الخطوط والأشكال فوقها وتحريك الطبقات وتصدير صور وفيديو من أمر واحد.

**What it does:** One CLI links App Studio authorized local photo processing, Unified Draw freehand/geometric layers and Creative Paint keyframe animation for composited PNG/GIF/MP4.

#### متى تُستدعى

- «Edit a local photo and draw or animate shapes on it»
- «Overlay animated drawing on a photograph and export MP4»
- «اجمع صورة مع الرسم والموشن والتلوين في فيديو واحد»

#### الأوامر

- **doctor**: Check named filters and FFmpeg availability.
  - `python3 scripts/unified_media.py doctor`
- **photo-overlay**: Adjust local photo exposure and layer drawings on top; produce PNG.
  - `python3 scripts/unified_media.py render --photo templates/unified-media-demo-photo.png --scene templates/unified-draw-motion-demo.json --output ./overlay.png --effect develop --exposure 0.4`
- **motion-video**: Export photo+animated drawing as H.264 MP4 (max 300 frames).
  - `python3 scripts/unified_media.py render --photo templates/unified-media-demo-photo.png --scene templates/unified-draw-motion-demo.json --output ./overlay.mp4 --effect develop --exposure 0.4 --fps 12 --duration 2`
- **tests**: Run local photo/drawing/video integration regression suite.
  - `python3 scripts/test_unified_media.py`

#### المتطلبات والأمان

- optional: bin:ffmpeg
- python: Pillow, numpy, opencv-python
- الأمان: writes-files
- الموافقة: —
- الحدود: Source-limited editing, RGB raster overlays and 2D keyframing; centered cover crop; max 300 frames, no audio, no photo realism claim, no proprietary code, not all 5,185 powers integrated.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/scripts/test_unified_media.py`
- مرجع: `.claude/skills/kosif-superpowers/references/unified-media-integration.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:unified-media --evidence <ملف>`.

