# الصور والتصميم والخطوط — Image, design and fonts

App Studio: أكثر من مئة عملية على صور المستخدم وتصاميمه (تطوير، إصلاح، مؤثرات، Canva، Paint.NET، Photoshop)، ومختبر مطابقة الخطوط العربية.

App Studio's 100+ operations on the user's own photos and designs (develop, repair, effects, Canva-style design, Paint.NET and Photoshop-style effects) and the Arabic font fidelity lab.

Commands below are typed from the skill folder (`.claude/skills/kosif-superpowers/`) unless they say otherwise; `$SKILL_DIR` means that folder.

<!-- hub:area:image:start -->

**الأدوات / tools (1)** — `python3 scripts/hub.py tool <id>` for every command, requirement and limit:

| tool | what it does | start with | evidence |
|---|---|---|---|
| `render-text` | Renders text samples in candidate font files through headless Chromium (HarfBuzz shaping) and saves one tightly cropped PNG per item, plus renders.json with the box sizes, so you can match a reference typeface. | `node scripts/render_text.cjs ./spec.json ./out/` | tested-elsewhere |

<!-- hub:area:image:end -->

## الفهرس / contents

1. [قدرات التطبيقات المحللة — Analyzed app capabilities (APPX)](#قدرات-التطبيقات-المحللة--analyzed-app-capabilities-appx)
2. [Arabic font fidelity lab](#arabic-font-fidelity-lab)

## قدرات التطبيقات المحللة — Analyzed app capabilities (APPX)

حين يطلب المستخدم ميزة «مثل CapCut أو Canva أو Premiere أو DxO أو Capture One أو JPEGmini أو FontLab أو Houdini أو IDM أو Animate» (منحنى سرعة، كروما، إعادة تأطير 9:16، ترجمة تلقائية، خفض الموسيقى، فقاعة كاميرا فوق تسجيل الشاشة، LUT، EDL…) أو يبني تطبيق سطح مكتب ويريد أنماط هذه التطبيقات، افتح [app-feature-transfer.md](../app-feature-transfer.md) وعائلة [APPX](../powers/app-feature-transfer.md). المزايا اكتُشفت بتحليل مثبّتاتها بـ REA؛ 17 وصفة تحرير ✅ مثبتة بأدوات مفتوحة (`proofs/app-feature-transfer/smoke.py`، 17/17)، و13 نمطًا معماريًا من Canva والمثبّتات (2 منها ✅ والباقي 📄). **الدفعة الثانية (APPX-31…60):** مطوّرات الصور والتصميم: DxO PhotoLab (إزالة الضباب، تقليل الضوضاء، المنظور، العدسة، الزيغ اللوني، الأفق، دمج التعريضات، علامة مائية)، وCapture One (منحنيات وتوازن لون، حبيبات وتعتيم أطراف، أوراق تواصل، إعدادات مسبقة بإصدارات)، وJPEGmini (ضغط JPEG بشرط SSIM)، وLightroom/ACDSee (ملفات XMP جانبية)، وFontLab (بناء خط بتقنين)، وAffinity/Houdini (عمليات بوليانية، قنوات حركة Lag/Noise، مخطط مهام بتخزين مؤقت)، وIDM (تنزيل مجزأ قابل للاستئناف)، وAnimate (حركة متوسطة بتسهيل، قشرة بصل، ورقة رسوم): 20 وصفة ✅ (`proofs/app-feature-transfer/smoke_studio.py`، 20/20)، وأنماط معمارية 📄، ومشروعا المالك `apps/virtualcam` و`apps/tikplayer`.

**استخدم القدرات على ملفات المستخدم (App Studio):** كل ما سبق صار أوامر تعمل على ملفات المستخدم الحقيقية: `python $SKILL_DIR/scripts/app_studio.py doctor` أولًا (يطبع الجاهز وسطر تثبيت الناقص)، ثم `app_studio.py <op> IN -o OUT --set k=v` أو `batch <op> FOLDER -o OUT_DIR`. 104 عملية: تطوير الصور (dehaze، denoise، keystone، lens، ca، develop، hsl، bw، split-tone، clarity، sharpen، hdr، auto-tone، horizon، crop، resize، icc)، الإصلاح (redeye، repair، moire)، المؤثرات (grain، vignette، tilt-shift، bg-blur، watermark بالعربية)، المكتبة (xmp، exif، dedupe، faces، rename، catalog، search، contact-sheet، pdf، jpegmini)، التصميم والإجراءات (trace، boolean، scatter، noise-field، lsystem، chops)، الخطوط (font-build، font-inspect، font-subset)، الأنيميشن (tween، lottie، ik) والتنزيل (download). **وتصميم Canva (APPX-88…98):** `design` (قالب JSON بنصوص عربية وتأثيرات shadow/outline/glow/neon وصور بإطار وتدرجات)، و`resize-design` (تغيير المقاس السحري لـ 16 مقاسًا)، و`remove-bg` (PNG شفاف)، و`duotone`، و`collage`، و`mockup`، و`qr` (يُقرأ للتحقق)، و`palette` (ألوان الهوية مع تباين WCAG)، و`chart` (عناوين عربية)، و`pptx`، و`print-pdf` (نزيف وعلامات قص وCMYK)، و`text-anim` (نص عربي متحرك GIF/MP4)؛ الدليل [CANVA_DESIGN_2026-10-19.md](../../proofs/windows-installers-rea/CANVA_DESIGN_2026-10-19.md). **والرسم والرندر (APPX-99…119):** 30 مؤثرًا من Paint.NET (oil-paint، ink-sketch، twist، zoom-blur، crystallize، levels…)، و`blend` بـ 24 وضع مزج و`layers` إلى OpenRaster، و`lut-make`/`lut` و`sky-replace` و`liquify` و`lens-blur` (Photoshop)، وفرش الرسّام `paint` و`fill` و`coloring-book` و`sticker`؛ و`scripts/blender_cinema.py` لرندر Cycles سينمائي بخمسة أساليب وحركات كاميرا إلى MP4 (يحتاج Blender أو `pip install bpy`)؛ الدليل [PAINT_PHOTOSHOP_BLENDER_2026-10-20.md](../../proofs/windows-installers-rea/PAINT_PHOTOSHOP_BLENDER_2026-10-20.md). **متطلبات الاستخدام:** Python 3.9+ و`pip install numpy opencv-python-headless pillow` للأساس، و`fonttools brotli` للخطوط، و`shapely` للعمليات البوليانية، و`segno` لرموز QR، و`matplotlib` للرسوم البيانية، و`python-pptx` للعروض، وffmpeg اختياريًا لـ MP4، و`arabic-reshaper python-bidi` للنص العربي حين يغيب libraqm، ونموذج YuNet لكشف الوجوه في OpenCV 5، والشبكة للتنزيل فقط. الجدول الكامل في [app-feature-transfer.md §7](../app-feature-transfer.md). الدليل: `evals/test_app_studio.py` (45/45) و`evals/test_app_studio_paint.py` (12/12) و`evals/test_blender_cinema.py` (7/7). نستلهم ولا ننسخ كود أي تطبيق؛ ولتطبيق جديد: triage → unpack → fingerprint → REA → سجلات APPX جديدة بأدنى شارة صادقة.

## Arabic font fidelity lab

When asked to **match, imitate, identify or create typography** (including Arabic calligraphy in a user-supplied image/video), use `scripts/font_fidelity_lab.py` with **user-authorized font files**, inspect GSUB/GPOS/cmap/axes, render shaped Arabic with libraqm, rank visual candidates against a tightly cropped reference, and independently compare multiple phrases. Follow the [font matching workflow](../font-matching.md) (observe the type, render candidates, decide); [font-innovation-50.md](../font-innovation-50.md) is only a research index of related repositories. Exact font identification requires evidence; do not assert it from pixel similarity alone. For the uploaded KOSIF Jumuah kit, inspect its OFL and Amiri/Bodoni Moda derivative sources; never commit its font binaries blindly.
