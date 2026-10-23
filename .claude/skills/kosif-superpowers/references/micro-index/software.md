# البرمجة وبناء التطبيقات — Software & applications

[← الفهرس الدقيق / micro index](README.md) · 578 powers

## الفهرس / contents

- [app-feature-transfer (build)](#app-feature-transfer-build)
- [apps-artifacts (build)](#apps-artifacts-build)
- [atlas-build (build)](#atlas-build-build)
- [atlas-code (code)](#atlas-code-code)
- [code-engineering (code)](#code-engineering-code)
- [ui-product-device (motion)](#ui-product-device-motion)


## app-feature-transfer (build)

chapter: [app-feature-transfer](../powers/app-feature-transfer.md) · card: `usip-library/cards/software/app-feature-transfer.md` · tools: `app-studio` · `app-studio-paint` · `browser-scout` · `installer-triage` · `motion-kit-bridge` · `source-scout` · `web-app-study`

| ID | | القدرة / power | SP | يحتاج / requires |
|---|---|---|---|---|
| APPX-31 | ✅ | إزالة الضباب · Dehaze (ClearView-style) | SP-0104 Dehaze (ClearView-style) | chromium, pip:numpy, pip:opencv |
| APPX-32 | ✅ | تقليل الضوضاء بمستويات · Tiered noise reduction | SP-0104 Dehaze (ClearView-style) | ffmpeg, chromium, pip:opencv |
| APPX-33 | ✅ | تصحيح المنظور تلقائيًا · Auto keystone / perspective | SP-0104 Dehaze (ClearView-style) | chromium, pip:opencv |
| APPX-34 | ✅ | تصحيح تشوّه العدسة · Lens distortion correction | SP-0104 Dehaze (ClearView-style) | chromium, pip:opencv |
| APPX-35 | ✅ | إزالة الزيغ اللوني · Lateral chromatic aberration removal | SP-0104 Dehaze (ClearView-style) | chromium, pip:opencv |
| APPX-36 | ✅ | توازن الأبيض ومنحنى الدرجات وHSL · White balance + tone curve + HSL | SP-0104 Dehaze (ClearView-style) | ffmpeg, chromium, pip:numpy, pip:opencv |
| APPX-37 | ✅ | حبيبات فيلم وتعتيم أطراف · Film grain + vignette | SP-0104 Dehaze (ClearView-style) | ffmpeg, chromium, pip:numpy, pip:opencv |
| APPX-38 | ✅ | علامة مائية بشفافية دقيقة · Watermark with exact opacity | SP-0104 Dehaze (ClearView-style) | ffmpeg, pip:pillow |
| APPX-39 | ✅ | ضغط JPEG إدراكي · Perceptual JPEG recompression (JPEGmini-style) | SP-0104 Dehaze (ClearView-style) | chromium, pip:pillow, pip:opencv |
| APPX-40 | ✅ | ورقة تواصل وقوالب طباعة · Contact sheet / print templates | SP-0104 Dehaze (ClearView-style) | pip:pillow |
| APPX-41 | ✅ | ملفات إعدادات مسبقة بإصدارات · Versioned preset / style files | SP-0104 Dehaze (ClearView-style) | python3 |
| APPX-42 | ✅ | ملف XMP جانبي: تقييم ووسوم · XMP sidecar: rating, label, keywords | SP-0104 Dehaze (ClearView-style) | python3 |
| APPX-43 | ✅ | تعديل الأفق تلقائيًا · Auto horizon straighten | SP-0104 Dehaze (ClearView-style) | chromium, pip:opencv |
| APPX-50 | ✅ | دمج التعريضات والتحكم بالدرجات · Exposure fusion / selective tonal control | SP-0104 Dehaze (ClearView-style) | chromium, pip:opencv |
| APPX-61 | ✅ | توضيح الحدة · Unsharp-mask sharpening | SP-0104 Dehaze (ClearView-style) | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-62 | ✅ | الوضوح والملمس · Clarity / texture (local contrast) | SP-0104 Dehaze (ClearView-style) | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-63 | ✅ | تحكم لوني لكل نطاق · HSL per colour band | SP-0104 Dehaze (ClearView-style) | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-64 | ✅ | أبيض وأسود بخلط القنوات · Black & white channel mixer | SP-0104 Dehaze (ClearView-style) | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-65 | ✅ | تلوين الظلال والإضاءات · Split toning / colour grading | SP-0104 Dehaze (ClearView-style) | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-66 | ✅ | إزالة احمرار العين · Red-eye removal | SP-0104 Dehaze (ClearView-style) | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-67 | ✅ | إزالة عنصر وترميم · Object removal / heal | SP-0104 Dehaze (ClearView-style) | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-68 | ✅ | إزالة التموج (مواريه) · Moiré removal | SP-0104 Dehaze (ClearView-style) | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-69 | ✅ | تأثير المجسم · Tilt-shift miniature | SP-0104 Dehaze (ClearView-style) | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-70 | ✅ | تغبيش الخلفية · Background blur (portrait) | SP-0104 Dehaze (ClearView-style) | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-71 | ✅ | قص بنسبة ذكي · Aspect crop with subject focus | SP-0104 Dehaze (ClearView-style) | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-72 | ✅ | تغيير المقاس · Resize for export | SP-0104 Dehaze (ClearView-style) | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-73 | ✅ | ضبط تلقائي للإضاءة · Auto tone / levels | SP-0104 Dehaze (ClearView-style) | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-120 | 📄 | عقد الأمانة للتصميم بقائمة انحرافات مغلقة · Design fidelity contract with a closed deviation list | SP-0105 Parity first, adaptation second | — |
| APPX-121 | 📄 | التطابق أولًا ثم التكييف · Parity first, adaptation second | SP-0105 Parity first, adaptation second | — |
| APPX-122 | 📄 | حلقة التحقق البصري للواجهة مقابل المرجع · Visual verification loop for UI against a reference | SP-0105 Parity first, adaptation second | chromium, pip:pillow |
| APPX-123 | 📄 | استيراد واجهة من مستودع بقراءة أساس التصميم أولًا · Import UI from a repository by reading its design foundation first | SP-0105 Parity first, adaptation second | python3, git |
| APPX-124 | 📄 | الثيم كبيانات قابلة للنقل مع حقل نية المصمم · Theme as portable data with a designer-intent field | SP-0105 Parity first, adaptation second | — |
| APPX-125 | 📄 | قواعد افتراضية لإطارات الواجهات التفاعلية · Default rules for authored interactive UI frames | SP-0105 Parity first, adaptation second | — |
| APPX-126 | 📄 | التصميم مواصفة الشكل والمكوّن القديم مواصفة السلوك · Design is the look spec; the old component is the behaviour spec | SP-0105 Parity first, adaptation second | — |
| APPX-127 | 📄 | عقد أوامر مريح للوكيل · Agent-friendly command contract (JSON, non-interactive, dry-run, explicit states) | SP-0105 Parity first, adaptation second | python3 |
| APPX-128 | 📄 | فحص تمهيدي أولًا للحساب والسياق · Preflight probe first: auth, context and version as one JSON | SP-0105 Parity first, adaptation second | python3 |
| APPX-129 | 📄 | لوحة بصرية دائمة بجانب الوكيل · Persistent visual board beside the agent | SP-0105 Parity first, adaptation second | — |
| APPX-130 | 📄 | جلسة عمل بمرحلتين مع خط أساس وقائمة ملفات مسموحة · Two-phase work session with a baseline manifest and an editable-file allowlist | SP-0105 Parity first, adaptation second | python3 |
| APPX-131 | 📄 | تثبيت النسخة التي يراها المستخدم بالضبط · Pin exactly the version the user is looking at | SP-0105 Parity first, adaptation second | python3 |
| APPX-132 | 📄 | حزمة مراجع من التحديد تُعطى لكل العمّال · Selection-as-context reference bundle shared by every worker | SP-0105 Parity first, adaptation second | — |
| APPX-133 | 📄 | تنويعات على محاور مسمّاة جنبًا إلى جنب · Variant fan-out on named axes, side by side, never overwriting | SP-0105 Parity first, adaptation second | python3 |
| APPX-134 | 📄 | التعديل الحتمي أولًا والنموذج للباقي فقط · Deterministic-first edits; the model only for what cannot be rewritten safely | SP-0105 Parity first, adaptation second | python3 |
| APPX-135 | 📄 | نُسخ مرتبطة: نمط مشترك ومحتوى لكل سجل · Linked instances: shared style, per-record content | SP-0105 Parity first, adaptation second | — |
| APPX-136 | 📄 | نسخ لكل عنصر وارجع للخلف بدل مواصلة التلقين · Per-item revisions: roll back instead of piling on prompts | SP-0105 Parity first, adaptation second | python3 |
| APPX-137 | 📄 | الرسم التقريبي الموسوم للبنية والمرجع للمظهر · Labeled rough sketch for structure; reference for look | SP-0105 Parity first, adaptation second | python3 |
| APPX-138 | 📄 | جسر MCP باتجاهين مع تلميح التحديد الحالي · Two-way MCP bridge with a current-selection hint | SP-0105 Parity first, adaptation second | python3 |
| APPX-139 | 📄 | المهارات: تحميل بالوصف وتثبيت صريح واستيراد نصي آمن · Skills: description-matched loading, explicit pinning, safe text-only import | SP-0105 Parity first, adaptation second | python3 |
| APPX-24 | ✅ | تقوية Electron بالـ fuses · Electron fuse hardening | SP-0106 Minimal context bridge over a MessagePo… | npm:rea |
| APPX-30 | ✅ | فرز المثبّت والتحقق من توقيعه · Installer triage and signature check | SP-0106 Minimal context bridge over a MessagePo… | python3, 7zip |
| APPX-53 | ✅ | ملف لون لكل كاميرا · Per-camera colour profiles | SP-0106 Minimal context bridge over a MessagePo… | pip:pillow |
| APPX-57 | ✅ | كشف حمولات المثبّتات الخفية · Hidden installer payload detection | SP-0106 Minimal context bridge over a MessagePo… | python3, npm:rea, 7zip, innoextract |
| APPX-20 | 📄 | واجهة احتياطية بلا إنترنت · Offline fallback renderer | SP-0106 Minimal context bridge over a MessagePo… | — |
| APPX-21 | 📄 | واجهات RTL مبنية مسبقًا · Prebuilt RTL bundles for Arabic | SP-0106 Minimal context bridge over a MessagePo… | node |
| APPX-22 | 📄 | اقترانات الملفات · File associations for media | SP-0106 Minimal context bridge over a MessagePo… | pip:pillow |
| APPX-23 | 📄 | جسر واحد بقناة MessagePort · Minimal context bridge over a MessagePort | SP-0106 Minimal context bridge over a MessagePo… | — |
| APPX-25 | 📄 | تحديث تلقائي · Auto update channel | SP-0106 Minimal context bridge over a MessagePo… | node |
| APPX-26 | 📄 | تقارير الأعطال · Crash and error reporting | SP-0106 Minimal context bridge over a MessagePo… | node |
| APPX-27 | 📄 | تكامل النظام · OS integration set | SP-0106 Minimal context bridge over a MessagePo… | — |
| APPX-28 | 📄 | مثبّت NSIS ثنائي المعمارية · Dual-architecture NSIS payload | SP-0106 Minimal context bridge over a MessagePo… | python3, 7zip |
| APPX-29 | 📄 | مثبّت تمهيدي عبر الإنترنت · Online bootstrap installer | SP-0106 Minimal context bridge over a MessagePo… | — |
| APPX-51 | 📄 | وحدة مستقلة لكل تصحيح · One plugin assembly per correction | SP-0106 Minimal context bridge over a MessagePo… | npm:rea |
| APPX-52 | 📄 | سلسلة توافق للإعدادات القديمة · Settings compatibility chain | SP-0106 Minimal context bridge over a MessagePo… | — |
| APPX-54 | 📄 | فرش التعديل المحلي كإعدادات · Local-adjustment brushes as presets | SP-0106 Minimal context bridge over a MessagePo… | pip:numpy, pip:opencv |
| APPX-55 | 📄 | حزمة هندسة الخطوط · Font engineering stack | SP-0106 Minimal context bridge over a MessagePo… | pip:fonttools |
| APPX-56 | 📄 | أصول إجرائية بمعاملات · Procedural digital assets | SP-0106 Minimal context bridge over a MessagePo… | blender, npm:three |
| APPX-58 | 📄 | خط تصدير الرسوم المتحركة · Animation export pipeline | SP-0106 Minimal context bridge over a MessagePo… | npm:three, npm:gsap, npm:lottie |
| APPX-01 | ✅ | منحنى السرعة · Speed curve (ramp) | SP-0107 Beat markers from audio | ffmpeg |
| APPX-02 | ✅ | مفتاح الكروما (الشاشة الخضراء) · Chroma key | SP-0107 Beat markers from audio | ffmpeg |
| APPX-03 | ✅ | إعادة التأطير التلقائي 9:16 · Auto reframe to 9:16 | SP-0107 Beat markers from audio | ffmpeg, pip:numpy, pip:opencv |
| APPX-04 | ✅ | كشف القطعات · Scene edit detection | SP-0107 Beat markers from audio | ffmpeg |
| APPX-05 | ✅ | توحيد علوّ الصوت للسوشيال · Loudness normalisation (-14 LUFS) | SP-0107 Beat markers from audio | ffmpeg |
| APPX-06 | ✅ | لون سينمائي من LUT · Colour look from a .cube LUT | SP-0107 Beat markers from audio | ffmpeg |
| APPX-07 | ✅ | حذف الوقفات والصمت · Pause and silence removal | SP-0107 Beat markers from audio | ffmpeg |
| APPX-08 | ✅ | علامات الإيقاع · Beat markers from audio | SP-0107 Beat markers from audio | pip:numpy |
| APPX-10 | ✅ | تكبير بإطارات مفتاحية · Keyframed punch-in / Ken Burns | SP-0107 Beat markers from audio | ffmpeg |
| APPX-11 | ✅ | خفض الموسيقى تحت الصوت · Auto ducking | SP-0107 Beat markers from audio | ffmpeg |
| APPX-12 | ✅ | تنقية الكلام من الضجيج · Speech noise reduction | SP-0107 Beat markers from audio | ffmpeg |
| APPX-13 | ✅ | ترجمة تلقائية بتوقيت الكلمات · Word-timed auto captions | SP-0107 Beat markers from audio | pip:faster-whisper |
| APPX-15 | ✅ | تصدير EDL ومطابقته · EDL interchange and conform | SP-0107 Beat markers from audio | ffmpeg |
| APPX-16 | ✅ | عكس المقطع وتجميد الإطار · Reverse and freeze frame | SP-0107 Beat markers from audio | ffmpeg |
| APPX-17 | ✅ | اختيار الغلاف تلقائيًا · Automatic cover pick | SP-0107 Beat markers from audio | pip:opencv |
| APPX-09 | ✅ | فقاعة الكاميرا فوق تسجيل الشاشة · Round camera bubble over a screen recording | SP-0108 QR code (verified) | ffmpeg |
| APPX-14 | ✅ | إزالة خلفية صورة · Background removal on a still | SP-0108 QR code (verified) | pip:opencv |
| APPX-88 | ✅ | تصميم من قالب JSON · Template design (JSON → PNG/PDF) | SP-0108 QR code (verified) | pip:numpy, pip:pillow, fonts:arabic, pip:arabic-reshaper |
| APPX-89 | ✅ | تغيير المقاس السحري · Magic Resize to every platform | SP-0108 QR code (verified) | chromium, pip:numpy, pip:opencv |
| APPX-90 | ✅ | تأثير اللونين · Duotone | SP-0108 QR code (verified) | pip:numpy, pip:pillow |
| APPX-91 | ✅ | كولاج وشبكات · Collage and grids | SP-0108 QR code (verified) | pip:pillow |
| APPX-92 | ✅ | موك أب واقعي · Photo mockup | SP-0108 QR code (verified) | chromium, pip:numpy, pip:opencv |
| APPX-93 | ✅ | رمز QR بشعار · QR code (verified) | SP-0108 QR code (verified) | chromium, pip:opencv, pip:segno |
| APPX-94 | ✅ | ألوان الهوية · Brand palette (Brand Kit) | SP-0108 QR code (verified) | chromium, pip:pillow, pip:opencv, npm:axe |
| APPX-95 | ✅ | رسم بياني بالعربية · Charts with Arabic labels | SP-0108 QR code (verified) | pip:matplotlib, pip:arabic-reshaper |
| APPX-96 | ✅ | عرض PowerPoint · Presentation export (PPTX) | SP-0108 QR code (verified) | pip:pillow, pip:office |
| APPX-97 | ✅ | PDF للمطبعة · Print PDF: bleed, crop marks, CMYK | SP-0108 QR code (verified) | pip:pillow |
| APPX-98 | ✅ | نص متحرك · Text animation to GIF/MP4 | SP-0108 QR code (verified) | ffmpeg, pip:numpy, pip:pillow |
| APPX-18 | 📄 | منتقي الشاشة للتسجيل · Display-media picker for screen recording | SP-0108 QR code (verified) | — |
| APPX-19 | 📄 | غرفة تحكم التسجيل · Recording mission-control and overlay windows | SP-0108 QR code (verified) | — |
| APPX-44 | ✅ | بناء خط بتقنين الأزواج · Build a font with kerning | SP-0109 L-system growth | pip:fonttools |
| APPX-45 | ✅ | عمليات بوليانية للأشكال المتجهة · Vector boolean operations | SP-0109 L-system growth | pip:shapely |
| APPX-46 | ✅ | عمليات القنوات للحركة · Motion channel ops (CHOP-style) | SP-0109 L-system growth | pip:numpy |
| APPX-47 | ✅ | مخطط مهام بتخزين مؤقت · Task graph with caching (PDG-style) | SP-0109 L-system growth | python3 |
| APPX-48 | ✅ | تنزيل مجزأ قابل للاستئناف · Segmented, resumable download (IDM-style) | SP-0109 L-system growth | python3 |
| APPX-49 | ✅ | حركة متوسطة وقشرة البصل وورقة رسوم · Eased tween, onion skin, sprite sheet | SP-0109 L-system growth | pip:numpy, pip:pillow |
| APPX-79 | ✅ | تحويل صورة إلى متجه · Bitmap to vector (image trace) | SP-0109 L-system growth | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-80 | ✅ | صور إلى PDF · Images to PDF | SP-0109 L-system growth | pip:pillow |
| APPX-81 | ✅ | نثر عناصر إجرائيًا · Procedural scatter (Poisson disc) | SP-0109 L-system growth | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-82 | ✅ | حقل ضوضاء إجرائي · Fractal noise field | SP-0109 L-system growth | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-83 | ✅ | نمو نباتي وزخرفي · L-system growth | SP-0109 L-system growth | python3 |
| APPX-84 | ✅ | فحص خط · Font inspection | SP-0109 L-system growth | pip:fonttools |
| APPX-85 | ✅ | تقليص خط للويب · Font subsetting | SP-0109 L-system growth | pip:fonttools |
| APPX-86 | ✅ | تصدير Lottie · Lottie JSON export | SP-0109 L-system growth | python3, npm:lottie |
| APPX-87 | ✅ | حل عظمتين (IK) · Two-bone inverse kinematics | SP-0109 L-system growth | python3 |
| APPX-100 | ✅ | تشويهات: التواء وانتفاخ وانعكاس قطبي · Distort: twist, bulge, polar inversion, dents, frosted glass, tile reflection | SP-0110 Oil painting, ink sketch, pencil sketch | pip:numpy, pip:opencv |
| APPX-101 | ✅ | تغبيشات: تقريب ودوران وحركة وسطح · Blurs: zoom, radial, motion, surface, unfocus, fragment, median | SP-0110 Oil painting, ink sketch, pencil sketch | pip:numpy, pip:opencv |
| APPX-102 | ✅ | أسلبة: نقش وحواف وبكسلة وبلورات وتوهج · Stylize: emboss, relief, edge detect, outline, pixelate, crystallize, glow, soften portrait | SP-0110 Oil painting, ink sketch, pencil sketch | pip:numpy, pip:opencv |
| APPX-103 | ✅ | كسيريات جوليا وماندلبروت · Julia and Mandelbrot fractals | SP-0110 Oil painting, ink sketch, pencil sketch | pip:numpy, pip:opencv |
| APPX-104 | ✅ | تعديلات: مستويات وتقليل ألوان وسيبيا وضوضاء · Adjustments: levels, posterize, sepia, invert, auto level, add noise | SP-0110 Oil painting, ink sketch, pencil sketch | pip:numpy, pip:opencv |
| APPX-99 | ✅ | رسم زيتي وحبر ورصاص · Oil painting, ink sketch, pencil sketch | SP-0110 Oil painting, ink sketch, pencil sketch | pip:numpy, pip:opencv |
| APPX-105 | ✅ | أوضاع المزج والطبقات (OpenRaster) · Blend modes (24) and layer stacks → PNG or OpenRaster | SP-0111 Blend modes (24) and layer stacks → PNG… | pip:numpy, pip:pillow, pip:opencv |
| APPX-106 | ✅ | LUT سينمائي: صناعة وتطبيق · Cinematic 3D LUTs: make and apply .cube | SP-0111 Blend modes (24) and layer stacks → PNG… | pip:numpy, pip:opencv |
| APPX-107 | ✅ | استبدال السماء · Sky replacement | SP-0111 Blend modes (24) and layer stacks → PNG… | pip:numpy, pip:opencv |
| APPX-109 | ✅ | تغبيش العدسة بعمق وبوكيه · Lens blur with depth map and polygonal bokeh | SP-0111 Blend modes (24) and layer stacks → PNG… | pip:numpy, pip:opencv |
| APPX-108 | 🟢 | التسييل (Liquify) · Liquify: push, pinch, bloat, twirl | SP-0111 Blend modes (24) and layer stacks → PNG… | pip:numpy, pip:opencv |
| APPX-118 | 📄 | ميزات الذكاء في Photoshop: ما يقابلها · Photoshop AI features and their open counterparts | SP-0111 Blend modes (24) and layer stacks → PNG… | — |
| APPX-110 | ✅ | فرش الرسّام · MS Paint brushes on a canvas | SP-0112 MS Paint brushes on a canvas | pip:numpy, pip:opencv |
| APPX-111 | ✅ | سطل التعبئة · Bucket fill (contiguous or global, with tolerance) | SP-0112 MS Paint brushes on a canvas | pip:numpy, pip:opencv |
| APPX-112 | ✅ | صفحة تلوين من صورة · Coloring-book page from a photo | SP-0112 MS Paint brushes on a canvas | pip:numpy, pip:opencv |
| APPX-113 | ✅ | ملصق بحد أبيض وظل · Sticker: cut-out with white border and soft shadow | SP-0112 MS Paint brushes on a canvas | pip:numpy, pip:pillow, pip:opencv |
| APPX-119 | 📄 | ميزات الذكاء في الرسّام: ما يقابلها · MS Paint AI features and their open counterparts | SP-0112 MS Paint brushes on a canvas | — |
| APPX-74 | ✅ | قراءة بيانات الصورة وGPS · EXIF and GPS reader | SP-0113 Photo catalog + search | pip:pillow |
| APPX-75 | ✅ | كشف المكرر والمتشابه · Duplicate / near-duplicate finder | SP-0113 Photo catalog + search | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-77 | ✅ | إعادة تسمية دفعة · Batch rename by EXIF date | SP-0113 Photo catalog + search | pip:pillow |
| APPX-78 | ✅ | فهرسة المكتبة والبحث · Photo catalog + search | SP-0113 Photo catalog + search | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-76 | 📦 | كشف الوجوه · Face detection | SP-0113 Photo catalog + search | pip:opencv, pip:onnxruntime, model:yunet |
| APPX-114 | ✅ | رندر سينمائي بخمسة أساليب · Cinematic Cycles render presets (5 looks) | SP-0114 Live Blender capability inventory | python3, blender |
| APPX-115 | ✅ | حركة كاميرا سينمائية إلى MP4 · Camera moves with 180° motion blur → MP4 | SP-0114 Live Blender capability inventory | ffmpeg, python3, blender |
| APPX-116 | ✅ | تشطيب الفيلم في المركّب · Film finish in the Blender 5 compositor | SP-0114 Live Blender capability inventory | blender |
| APPX-117 | ✅ | جرد قدرات Blender الحي · Live Blender capability inventory | SP-0114 Live Blender capability inventory | python3, blender, npm:rea |
| APPX-59 | 📄 | كاميرا افتراضية من فيديو · Virtual camera from a video file | SP-0115 Virtual camera from a video file | — |
| APPX-60 | 📄 | مشغل فيديو عمودي بالسحب · Vertical swipe video player (Android) | SP-0115 Virtual camera from a video file | — |

## apps-artifacts (build)

chapter: [apps-artifacts](../powers/apps-artifacts.md) · card: `usip-library/cards/software/apps-artifacts.md` · tools: `mosamem-rea-fusion`

| ID | | القدرة / power | SP | يحتاج / requires |
|---|---|---|---|---|
| APP-04 | ✅ | لوحة RTL بلا مكتبات · Dependency-free RTL dashboard page | SP-0116 Publish a private interactive page (Art… | — |
| APP-05 | ✅ | لقطة شاشة بمقاس الهاتف وفحص الفيض · Phone-viewport screenshot + overflow check | SP-0116 Publish a private interactive page (Art… | node, chromium |
| APP-06 | ✅ | من HTML إلى فيديو · HTML to MP4 renderer (repo tool) | SP-0116 Publish a private interactive page (Art… | node, python3, chromium |
| APP-08 | 📦 | تطبيقات بيانات سريعة · Data apps (streamlit, gradio) | SP-0116 Publish a private interactive page (Art… | python3 |
| APP-22 | 📦 | axe-core: فحص صفحة معروضة وفق قواعد WCAG والإبلاغ · axe-core: Run WCAG checks on a rendered page and report violations | SP-0116 Publish a private interactive page (Art… | chromium, npm:axe |
| APP-23 | 📦 | Pa11y: تدقيق الروابط أو ملفات HTML المحلية لإمكانية · Pa11y: Audit URLs or local HTML for accessibility from the CLI | SP-0116 Publish a private interactive page (Art… | npm:pa11y |
| APP-01 | 🔑 | نشر صفحة تفاعلية خاصة · Publish a private interactive page (Artifact) | SP-0116 Publish a private interactive page (Art… | npm:react, claude:tools |
| APP-02 | 🔑 | قدرات الصفحة أثناء التشغيل · Artifact runtime capabilities | SP-0116 Publish a private interactive page (Art… | key:unspecified |
| APP-03 | 🔑 | صفوف وتعليقات الصفحة · ArtifactData and ArtifactComments tools | SP-0116 Publish a private interactive page (Art… | claude:tools |
| APP-17 | 📄 | اعرض ثلاثة خيارات بدل الأسئلة · Show three previews instead of asking | SP-0116 Publish a private interactive page (Art… | — |
| APP-19 | 📄 | بوابة الإنهاء المرئية · Rendered finish gate | SP-0116 Publish a private interactive page (Art… | — |
| APP-09 | ✅ | واجهة برمجية بـ FastAPI · HTTP APIs with FastAPI (tested in-process) | SP-0117 Build an MCP server (mcp 2.x API) | python3 |
| APP-10 | ✅ | قوالب Jinja2 · Jinja2 templating | SP-0117 Build an MCP server (mcp 2.x API) | python3 |
| APP-11 | ✅ | بناء خادم MCP (الإصدار 2) · Build an MCP server (mcp 2.x API) | SP-0117 Build an MCP server (mcp 2.x API) | python3 |
| APP-07 | 📦 | أُطر الواجهات الحديثة · Modern front-end scaffolds (vite, react, next, svelte, tailwind) | SP-0117 Build an MCP server (mcp 2.x API) | npm:esbuild, npm:react |
| APP-13 | 📦 | خادم ملفات محلي للمعاينة · Local static server for previews | SP-0117 Build an MCP server (mcp 2.x API) | node, python3, chromium, claude:tools |
| APP-20 | 📦 | CadQuery: برمجة قطع صلبة بارامترية وتصديرها STEP أو · CadQuery: Script parametric solid parts and export STEP/STL for 3D printing | SP-0117 Build an MCP server (mcp 2.x API) | pip:cadquery |
| APP-21 | 📦 | OpenSCAD: تحويل نماذج ‎.scad إلى STL أو PNG · OpenSCAD: Render .scad models to STL/PNG headlessly | SP-0117 Build an MCP server (mcp 2.x API) | openscad |
| APP-12 | 🔑 | تطبيقات تستدعي Claude عبر API · Apps that call Claude via the API | SP-0117 Build an MCP server (mcp 2.x API) | node, pip:anthropic, key:unspecified |
| APP-14 | 🔑 | بناء مواقع بالذكاء الاصطناعي (مدفوع) · Hosted website builder (Higgsfield, paid) | SP-0117 Build an MCP server (mcp 2.x API) | pip:higgsfield, key:unspecified |
| APP-15 | 📄 | اتجاه التصميم قبل الكود · Design direction before code | SP-0117 Build an MCP server (mcp 2.x API) | — |
| APP-16 | 📄 | لمسات تجعل الواجهة أفضل · Interface polish numbers | SP-0117 Build an MCP server (mcp 2.x API) | — |
| APP-18 | 📄 | فصل المنشئ عن الناقد · Separate maker from critic | SP-0117 Build an MCP server (mcp 2.x API) | chromium, git |

## atlas-build (build)

chapter: [atlas-build](../powers/atlas-build.md) · card: `usip-library/cards/software/atlas-build.md` · tools: —

| ID | | القدرة / power | SP | يحتاج / requires |
|---|---|---|---|---|
| ABUILD-49 | 📄 | تدقيق إتاحة WCAG 2.2: فحص وإصلاح وتحقق · WCAG 2.2 scan-fix-verify accessibility audit | SP-0116 Publish a private interactive page (Art… | npm:axe |
| ABUILD-28 | 📄 | دليل الحوادث: احتواء وتشخيص واستعادة · Incident runbook: contain, diagnose, recover | SP-0118 Figma to pixel-exact code plan | — |
| ABUILD-29 | 📄 | تصميم المراقبة: الإشارات الذهبية والتنبيهات · Observability design: golden signals and alerts | SP-0118 Figma to pixel-exact code plan | — |
| ABUILD-30 | 📄 | استطلاع البنية وتدقيق التكلفة · Infra reconnaissance and cost audit | SP-0118 Figma to pixel-exact code plan | — |
| ABUILD-31 | 📄 | تصميم مكوّن متاح افتراضيا · Accessible-by-default component pattern design | SP-0118 Figma to pixel-exact code plan | npm:pa11y |
| ABUILD-32 | 📄 | إعداد هوية العلامة مع فحص التباين · Brand palette onboarding with WCAG gate | SP-0118 Figma to pixel-exact code plan | npm:axe |
| ABUILD-33 | 📄 | حسابات الألوان وتخطيط CSS مع التباين · Color and CSS layout math with contrast | SP-0118 Figma to pixel-exact code plan | — |
| ABUILD-34 | 📄 | التصميم عبر قيود مكانية وطباعية صريحة · Design by explicit spatial and type constraints | SP-0118 Figma to pixel-exact code plan | — |
| ABUILD-35 | 📄 | نقد التصميم وتسليم المطورين وتدقيق النظام · Design critique, handoff and system audit | SP-0118 Figma to pixel-exact code plan | — |
| ABUILD-36 | 📄 | اشتقاق وترقية نظام التصميم · Design-system retrofit and derivation workflow | SP-0118 Figma to pixel-exact code plan | — |
| ABUILD-37 | 📄 | رموز التصميم DTCG لكل المنصات · DTCG design tokens multi-platform export | SP-0118 Figma to pixel-exact code plan | npm:react |
| ABUILD-38 | 📄 | تدقيق تصميم الواجهة بالأدلة · Evidence-backed frontend design audit | SP-0118 Figma to pixel-exact code plan | npm:react |
| ABUILD-39 | 📄 | استخراج بصمة التصميم من موقع حي · Extract Design DNA from live website | SP-0118 Figma to pixel-exact code plan | npm:three |
| ABUILD-40 | 📄 | من ملف Figma إلى رموز وأصول وكود · Figma file to tokens, assets and code | SP-0118 Figma to pixel-exact code plan | — |
| ABUILD-41 | 📄 | قراءة Figma عبر MCP أو REST · Figma read via MCP or REST fallback | SP-0118 Figma to pixel-exact code plan | — |
| ABUILD-42 | 📄 | من Figma إلى كود مطابق · Figma to pixel-exact code plan | SP-0118 Figma to pixel-exact code plan | — |
| ABUILD-43 | 📄 | تدقيق أداء الواجهة والاستجابة · Frontend performance and responsive audit | SP-0118 Figma to pixel-exact code plan | — |
| ABUILD-44 | 📄 | اختبار الوصولية بلوحة المفاتيح مباشرة · Live keyboard accessibility test via browser | SP-0118 Figma to pixel-exact code plan | npm:axe |
| ABUILD-45 | 📄 | صفحة هبوط فاخرة بحركة GSAP · Premium landing page with GSAP scroll motion | SP-0118 Figma to pixel-exact code plan | npm:gsap |
| ABUILD-46 | 📄 | حلقة مقارنة لقطة الصفحة بالتصميم · Screenshot-vs-design pixel diff loop | SP-0118 Figma to pixel-exact code plan | python3 |
| ABUILD-47 | 📄 | حلقة مقارنة لقطة الشاشة بالمرجع · Screenshot-vs-reference pixel diff loop | SP-0118 Figma to pixel-exact code plan | — |
| ABUILD-48 | 📄 | معمارية رموز التصميم بثلاث طبقات · Three-tier design token architecture with theming | SP-0118 Figma to pixel-exact code plan | — |
| ABUILD-05 | 📄 | مسار توقيع وإصدار تطبيقات الجوال والمكتب · Mobile and desktop release signing pipeline | SP-0119 Throwaway prototype to answer one quest… | os:macos |
| ABUILD-06 | 📄 | نموذج HTML تجريبي يجيب أسئلة مفتوحة · Open-question HTML prototype spike | SP-0119 Throwaway prototype to answer one quest… | — |
| ABUILD-07 | 📄 | تنسيق بناء تطبيق كامل على مراحل · Phased full-stack app build orchestration | SP-0119 Throwaway prototype to answer one quest… | — |
| ABUILD-08 | 📄 | تقييم النموذج مقابل معايير القبول · Prototype evaluation vs acceptance criteria | SP-0119 Throwaway prototype to answer one quest… | chromium |
| ABUILD-09 | 📄 | توليد PWA مع service worker · PWA manifest and service worker generation | SP-0119 Throwaway prototype to answer one quest… | chromium |
| ABUILD-10 | 📄 | هيكلة مشروع SaaS جاهز · SaaS boilerplate scaffold spec | SP-0119 Throwaway prototype to answer one quest… | npm:react |
| ABUILD-11 | 📄 | حالة الاشتراكات وواجهة إدارة الاشتراك · Subscription store state and paywall UI | SP-0119 Throwaway prototype to answer one quest… | — |
| ABUILD-12 | 📄 | نموذج أولي مؤقت للإجابة عن سؤال · Throwaway prototype to answer one question | SP-0119 Throwaway prototype to answer one quest… | — |
| ABUILD-13 | 📄 | بناء موقع Wix هيدلس من وصفات SDK · Wix headless site build from SDK recipes | SP-0119 Throwaway prototype to answer one quest… | chromium, key:unspecified |
| ABUILD-51 | 📄 | صياغة التذاكر وأوصاف PR بهيكل ماذا/لماذا/كيف · What/Why/How ticket and PR drafting | SP-0119 Throwaway prototype to answer one quest… | — |
| ABUILD-52 | 📄 | فرز أعطال الاتصال حسب مجال الخطأ دون تغيير الإعدادات · Fault-domain connectivity triage without touching config | SP-0119 Throwaway prototype to answer one quest… | — |
| ABUILD-14 | 📄 | حلقة مراجع شجرة الوصولية لتحكم المتصفح · Accessibility-tree ref loop for browser agents | SP-0120 Accessibility-tree ref loop for browser… | node, chromium |
| ABUILD-15 | 📄 | استنساخ موقع بأدلة المتصفح · Browser-evidence website clone workflow | SP-0120 Accessibility-tree ref loop for browser… | chromium |
| ABUILD-16 | 📄 | تصحيح الصفحات الحية عبر Chrome DevTools MCP · Chrome DevTools MCP debugging of live pages | SP-0120 Accessibility-tree ref loop for browser… | chromium |
| ABUILD-17 | 📄 | خط لقطات Playwright داخل حاوية · Containerized Playwright screenshot pipeline | SP-0120 Accessibility-tree ref loop for browser… | chromium, docker |
| ABUILD-18 | 📄 | تشغيل متصفحات معزولة عبر بروتوكولاتها · Isolated headless Chrome/Firefox/Safari drivers over native protocols | SP-0120 Accessibility-tree ref loop for browser… | chromium |
| ABUILD-19 | 📄 | جلسات Playwright مسماة بمخرجات على القرص · Named-session Playwright CLI with disk artifacts | SP-0120 Accessibility-tree ref loop for browser… | node, chromium |
| ABUILD-20 | 📄 | كتابة اختبارات E2E مع فحص الوصولية والأداء · Playwright E2E authoring with lint, a11y and CWV scans | SP-0120 Accessibility-tree ref loop for browser… | python3, chromium |
| ABUILD-21 | 📄 | رفع ملف عبر Playwright MCP لحقل مخفي · Playwright MCP hidden file-input upload workaround | SP-0120 Accessibility-tree ref loop for browser… | chromium |
| ABUILD-22 | 📄 | إثبات السلوك المعروض بحكم نجح/فشل/معطل · Rendered-behavior proof with pass/fail/blocked verdict | SP-0120 Accessibility-tree ref loop for browser… | chromium |
| ABUILD-23 | 📄 | فحص جودة الواجهة بثلاثة عروض · Three-width responsive browser QA report | SP-0120 Accessibility-tree ref loop for browser… | network |
| ABUILD-24 | 📄 | ضبط مجمع الاتصالات وموثوقية قاعدة البيانات · Connection pool sizing and DB reliability playbook | SP-0121 Connection pool sizing and DB reliabili… | — |
| ABUILD-25 | 📄 | نص نسخ احتياطي لقاعدة البيانات مع الاحتفاظ والتشفير · Database backup script with retention and encryption | SP-0121 Connection pool sizing and DB reliabili… | — |
| ABUILD-26 | 📄 | تطور مخططات الأحداث وKafka · Event schema evolution and Kafka platform playbook | SP-0121 Connection pool sizing and DB reliabili… | — |
| ABUILD-27 | 📄 | قواعد Postgres وRedis المُدارة على المنصات · Managed Postgres and Redis on hosting platforms | SP-0121 Connection pool sizing and DB reliabili… | — |
| ABUILD-50 | 📄 | إصدار نسخة: وسم ونشر وتحقق · Cut a release: tag, GitHub release, verify | SP-0121 Connection pool sizing and DB reliabili… | — |
| ABUILD-01 | 📄 | تنفيذ خارطة الطريق تلقائياً: مرحلة لكل طلب دمج · Autonomous phase-per-PR roadmap execution loop | SP-0122 Spec-to-task decomposition for coding a… | claude:tools |
| ABUILD-02 | 📄 | مسجل قياس تشغيل بالملاحظة فقط · Observation-only run telemetry recorder | SP-0122 Spec-to-task decomposition for coding a… | — |
| ABUILD-03 | 📄 | خط وكلاء بأدوار ومراحل وأقفال كتابة واستئناف · Role-squad agent pipeline with stages, locks and resume | SP-0122 Spec-to-task decomposition for coding a… | — |
| ABUILD-04 | 📄 | تفكيك المواصفة إلى مهام صغيرة لوكلاء البرمجة · Spec-to-task decomposition for coding agents | SP-0122 Spec-to-task decomposition for coding a… | — |

## atlas-code (code)

chapter: [atlas-code](../powers/atlas-code.md) · card: `usip-library/cards/software/atlas-code.md` · tools: `atlas-ledger`

| ID | | القدرة / power | SP | يحتاج / requires |
|---|---|---|---|---|
| ACODE-102 | 📄 | فرز أخطاء API بحسب الدليل وفئة الحالة · Evidence-based API error triage by status class | SP-0038 Generate standalone HTML API docs | — |
| ACODE-116 | 📄 | حزمة تشخيص API منقّحة للدعم · Redacted API diagnostic bundle for support | SP-0038 Generate standalone HTML API docs | — |
| ACODE-246 | 📄 | ترحيل عقد API لدى المزوّد بأدلة الحركة والقراءة المزدوجة · Vendor API contract migration with traffic evidence and dual reads | SP-0038 Generate standalone HTML API docs | — |
| ACODE-25 | 📄 | اختيار وتخزين مفاتيح الـAPI بأمان · Choose and store API credentials safely | SP-0038 Generate standalone HTML API docs | chromium, key:unspecified |
| ACODE-27 | 📄 | اختبار عقود API من جهة المستهلك بـ Pact · Consumer-driven API contract testing with Pact | SP-0038 Generate standalone HTML API docs | — |
| ACODE-28 | 📄 | استخراج عميل API مستقل من تسجيل HAR · Derive standalone API client from HAR recording | SP-0038 Generate standalone HTML API docs | — |
| ACODE-31 | 📄 | إعداد مصادقة API بأقل صلاحيات والتحقق منها · Least-privilege API auth setup and verification | SP-0038 Generate standalone HTML API docs | key:unspecified |
| ACODE-41 | 📄 | عميل API يحترم حدود المعدل مع إعادة محاولة · Rate-limit-aware API client with bounded retry | SP-0038 Generate standalone HTML API docs | — |
| ACODE-49 | 📄 | غلاف عميل API مُنمّط مع إعادة المحاولة · Typed API client adapter with retries | SP-0038 Generate standalone HTML API docs | — |
| ACODE-51 | 📄 | إعداد مفاتيح API وفحصها بأقل صلاحية · Vendor API credential setup and verification | SP-0038 Generate standalone HTML API docs | key:unspecified |
| ACODE-57 | 📄 | محدد معدل طلبات API مع تراجع أسي · Cost-aware API rate limiter with backoff | SP-0038 Generate standalone HTML API docs | — |
| ACODE-64 | 📄 | ضابط حدود معدل واجهات الموردين · Vendor API rate-limit governor | SP-0038 Generate standalone HTML API docs | — |
| ACODE-99 | 📄 | فرز أخطاء API حسب الحالة ومعرّف التتبع · API error triage by status and trace ID | SP-0038 Generate standalone HTML API docs | — |
| ACODE-29 | 📄 | قائمة تحصين نقطة GraphQL · GraphQL endpoint hardening checklist | SP-0039 REST, GraphQL, gRPC, WebSocket, SOAP | — |
| ACODE-42 | 📄 | مبادئ تصميم REST وGraphQL · REST and GraphQL API design principles | SP-0039 REST, GraphQL, gRPC, WebSocket, SOAP | — |
| ACODE-56 | 📄 | خادم WebSocket بمصادقة وغرف واشتراكات · WebSocket server with handshake auth and rooms | SP-0039 REST, GraphQL, gRPC, WebSocket, SOAP | — |
| ACODE-121 | 📄 | التحقق من استعادة النسخ الاحتياطي · Backup restore verification and DR rehearsal | SP-0040 GitHub Actions runner-cost optimizer | — |
| ACODE-122 | 📄 | حلقة إصلاح إخفاقات CI محدودة · Bounded CI failure repair loop | SP-0040 GitHub Actions runner-cost optimizer | gh |
| ACODE-123 | 📄 | تصميم تجربة فوضى مع نطاق الضرر وشروط الإيقاف · Chaos experiment design with blast radius and abort criteria | SP-0040 GitHub Actions runner-cost optimizer | — |
| ACODE-124 | 📄 | حكم فشل CI: منك أو من الفرع الرئيسي أو متقلب · CI failure verdict: yours, trunk-borne or flaky | SP-0040 GitHub Actions runner-cost optimizer | — |
| ACODE-125 | 📄 | تصميم خط CI: ترتيب وتخزين مؤقت · CI pipeline design: ordering, caching, required checks | SP-0040 GitHub Actions runner-cost optimizer | — |
| ACODE-126 | 📄 | النشر على المنصات السحابية عبر Blueprint أو Wrangler · Cloud platform deploy via Blueprint or Wrangler | SP-0040 GitHub Actions runner-cost optimizer | — |
| ACODE-127 | 📄 | تشخيص أعطال السحابة بفحص الصحة أولا · Cloud service triage via health-first diagnosis flow | SP-0040 GitHub Actions runner-cost optimizer | — |
| ACODE-128 | 📄 | تدقيق الحاويات وبودمان المتداخل · Container best-practice audit and rootless nesting | SP-0040 GitHub Actions runner-cost optimizer | docker |
| ACODE-129 | 📄 | أنماط Bash وzsh الدفاعية · Defensive Bash and zsh scripting conventions | SP-0040 GitHub Actions runner-cost optimizer | — |
| ACODE-130 | 📄 | بوابة CI آمنة بلا أسرار للتكاملات · Fail-closed credential-free CI gate for integrations | SP-0040 GitHub Actions runner-cost optimizer | — |
| ACODE-131 | 📄 | مسار نشر Azure بثلاث بوابات · Gated Azure prepare-validate-deploy workflow | SP-0040 GitHub Actions runner-cost optimizer | — |
| ACODE-132 | 📄 | حوكمة GCP: التسلسل والشبكة والفوترة · GCP resource hierarchy, networking and billing governance | SP-0040 GitHub Actions runner-cost optimizer | — |
| ACODE-133 | 📄 | تشخيص فشل GitHub Actions عبر gh · GitHub Actions failure triage via gh | SP-0040 GitHub Actions runner-cost optimizer | gh |
| ACODE-134 | 📄 | تدقيق هدر تكلفة GitHub Actions · GitHub Actions FinOps waste audit | SP-0040 GitHub Actions runner-cost optimizer | gh |
| ACODE-135 | 📄 | محسّن تكلفة مشغلات GitHub Actions · GitHub Actions runner-cost optimizer | SP-0040 GitHub Actions runner-cost optimizer | — |
| ACODE-136 | 📄 | GitHub Actions إلى GCP عبر Workload Identity · GitHub Actions to GCP with Workload Identity Federation | SP-0040 GitHub Actions runner-cost optimizer | — |
| ACODE-137 | 📄 | تسليم GitOps عبر Argo CD أو Flux · GitOps delivery with Argo CD or Flux | SP-0040 GitHub Actions runner-cost optimizer | — |
| ACODE-138 | 📄 | بناء حاوية آمنة متعددة المراحل · Hardened multi-stage container build | SP-0040 GitHub Actions runner-cost optimizer | docker, trivy |
| ACODE-139 | 📄 | استعادة إصدارات Helm والتراجع · Helm release recovery and rollback | SP-0040 GitHub Actions runner-cost optimizer | — |
| ACODE-140 | 📄 | بوابة CI للتكامل: فحوص بلا اتصال واختبار حي محمي · Integration CI gate: offline fixtures plus guarded live smoke | SP-0040 GitHub Actions runner-cost optimizer | — |
| ACODE-141 | 📄 | أساس منصة كوبرنتس متعددة المستأجرين · Kubernetes multi-tenant platform baseline | SP-0040 GitHub Actions runner-cost optimizer | — |
| ACODE-142 | 📄 | فحص ملفات workflow لمشاكل المشغلات الذاتية · Lint workflows for self-hosted runner pitfalls | SP-0040 GitHub Actions runner-cost optimizer | — |
| ACODE-143 | 📄 | تصميم خط نشر متعدد المراحل ببوابات · Multi-stage deployment pipeline design with gates | SP-0040 GitHub Actions runner-cost optimizer | — |
| ACODE-144 | 📄 | مصادقة CI بلا كلمات مرور عبر OIDC · Passwordless CI cloud auth via OIDC federation | SP-0040 GitHub Actions runner-cost optimizer | — |
| ACODE-145 | 📄 | دليل فرز الحوادث والتراجع · Platform incident triage and rollback runbook | SP-0040 GitHub Actions runner-cost optimizer | — |
| ACODE-146 | 📄 | قائمة نشر وتكامل CI حسب المنصة · Platform-specific deploy and CI integration checklist | SP-0040 GitHub Actions runner-cost optimizer | — |
| ACODE-148 | 📄 | إثبات عدم وجود مستهلك قبل حذف سر سحابي · Prove no consumer before destroying cloud secret | SP-0040 GitHub Actions runner-cost optimizer | — |
| ACODE-149 | 📄 | تطبيق Terraform من خطة محفوظة · Saved-plan non-interactive terraform apply | SP-0040 GitHub Actions runner-cost optimizer | — |
| ACODE-150 | 📄 | قائمة تحصين بيئة serverless · Serverless runtime hardening checklist | SP-0040 GitHub Actions runner-cost optimizer | — |
| ACODE-151 | 📄 | خطة نشر مرحلية مع تراجع وفصل الأسرار · Staged deployment plan with rollback and secret separation | SP-0040 GitHub Actions runner-cost optimizer | — |
| ACODE-152 | 📄 | نشر تكامل مرحلي مع كناري وإيصال تراجع · Staged integration deploy with canary and rollback receipt | SP-0040 GitHub Actions runner-cost optimizer | — |
| ACODE-153 | 📄 | هدم مرحلي لـ ECS بـ Terraform · Staged Terraform teardown for ECS capacity providers | SP-0040 GitHub Actions runner-cost optimizer | — |
| ACODE-154 | 📄 | وحدات Terraform وكشف الانحراف · Terraform and IaC module generation with drift checks | SP-0040 GitHub Actions runner-cost optimizer | — |
| ACODE-155 | 📄 | قواعد Terraform وبوابة سياسة للقراءة فقط · Terraform generation posture rules and read-only policy gate | SP-0040 GitHub Actions runner-cost optimizer | — |
| ACODE-156 | 📄 | بوابة سياسات خطة Terraform · Terraform plan policy gate (OPA) | SP-0040 GitHub Actions runner-cost optimizer | — |
| ACODE-157 | 📄 | كتابة workflows لـ GitHub Actions مع تحقق · Verified GitHub Actions workflow authoring | SP-0040 GitHub Actions runner-cost optimizer | gh |
| ACODE-85 | 📄 | أنماط كتابة DAG في Airflow · Airflow DAG authoring patterns | SP-0040 GitHub Actions runner-cost optimizer | python3 |
| ACODE-86 | 📄 | تأليف موصل تزايدي بـ Airbyte CDK · Incremental connector authoring (Airbyte CDK) | SP-0040 GitHub Actions runner-cost optimizer | python3, key:unspecified |
| ACODE-02 | 📄 | فحص أمان مسبق للوكيل بإيصال أخضر/أصفر/أحمر · Agent safety preflight with Green/Yellow/Red receipt | SP-0041 Worktree fleets for parallel agent phas… | — |
| ACODE-03 | 📄 | تدقيق سجلات جلسات الوكلاء بحثًا عن أسرار مسرّبة · Audit agent transcripts for leaked credentials | SP-0041 Worktree fleets for parallel agent phas… | — |
| ACODE-04 | 📄 | كتابة وفحص سكربتات سير عمل متعددة الوكلاء · Author and lint deterministic multi-agent workflow scripts | SP-0041 Worktree fleets for parallel agent phas… | — |
| ACODE-05 | 📄 | مقارنة وكلاء البرمجة في أشجار عمل معزولة · Benchmark Claude Code vs Codex in isolated worktrees | SP-0041 Worktree fleets for parallel agent phas… | python3, git |
| ACODE-07 | 📄 | مرشحون متنافسون في worktrees ثم دمج الفائز · Competing worktree candidates, judged, one landed | SP-0041 Worktree fleets for parallel agent phas… | git, claude:tools |
| ACODE-08 | 📄 | تنسيق وكلاء أشجار العمل عبر رسائل وإيصالات · Coordinate worktree coding agents via mail and receipts | SP-0041 Worktree fleets for parallel agent phas… | git |
| ACODE-10 | 📄 | أنماط سير عمل دائم: ساجا وDAG · Durable workflow patterns: Temporal sagas and Airflow DAGs | SP-0041 Worktree fleets for parallel agent phas… | python3 |
| ACODE-13 | 📄 | عزل أوامر الوكيل على macOS بـ Seatbelt · macOS Seatbelt confinement for agent commands | SP-0041 Worktree fleets for parallel agent phas… | os:macos |
| ACODE-15 | 📄 | فحوص ما قبل التنفيذ لتصادم الوكلاء المتوازيين · Parallel agent collision pre-flight checks | SP-0041 Worktree fleets for parallel agent phas… | gh |
| ACODE-158 | 📄 | تصميم تطبيق Agent SDK وخطافاته · Agent SDK app and hooks design | SP-0041 Worktree fleets for parallel agent phas… | key:openai |
| ACODE-159 | 📄 | حكم LLM معايَر ومدقَّق التحيز · Calibrated, bias-audited LLM-as-judge | SP-0041 Worktree fleets for parallel agent phas… | — |
| ACODE-16 | 📄 | عقد إطلاق وكلاء متوازيين مع فحص مسبق · Parallel agent dispatch contract with worktree preflight | SP-0041 Worktree fleets for parallel agent phas… | git, claude:tools |
| ACODE-161 | 📄 | حزمة تقييم LLM ثابتة بمجموعة ذهبية · Committed LLM eval suite with goldens | SP-0041 Worktree fleets for parallel agent phas… | python3 |
| ACODE-165 | 📄 | حالة وتدفق وكلاء LangGraph · LangGraph 1.0 agent state and flow | SP-0041 Worktree fleets for parallel agent phas… | python3 |
| ACODE-168 | 📄 | ترحيل مزود LLM إلى Bedrock · Migrate LLM provider SDK to Bedrock | SP-0041 Worktree fleets for parallel agent phas… | key:openai |
| ACODE-169 | 📄 | تفويض متعدد النماذج ورأي ثانٍ · Multi-model delegation and second opinion | SP-0041 Worktree fleets for parallel agent phas… | — |
| ACODE-17 | 📄 | فحص تمهيدي قبل بدء مهمة · Preflight check before starting an issue | SP-0041 Worktree fleets for parallel agent phas… | git |
| ACODE-170 | 📄 | تدقيق ذاكرة الـprompt المؤقتة وإصلاحها · Prompt-cache hit-rate audit and fix | SP-0041 Worktree fleets for parallel agent phas… | — |
| ACODE-172 | 📄 | عقد مخرجات LLM منظمة موثوقة · Reliable structured LLM output contract | SP-0041 Worktree fleets for parallel agent phas… | — |
| ACODE-18 | 📄 | استعادة سير عمل متوقف دون تكرار · Recover interrupted workflow run without duplicates | SP-0041 Worktree fleets for parallel agent phas… | git, gh |
| ACODE-19 | 📄 | خطافات ميزانية زمنية ناعمة للوكلاء الفرعيين · Soft wall-clock budget hooks for subagents | SP-0041 Worktree fleets for parallel agent phas… | claude:tools |
| ACODE-20 | 📄 | أساطيل أشجار عمل لمراحل وكلاء متوازية · Worktree fleets for parallel agent phases | SP-0041 Worktree fleets for parallel agent phas… | git |
| ACODE-26 | 📄 | اختيار واجهة Zoom المناسبة · Choose Zoom surface: REST, webhooks, WebSocket, SDK | SP-0041 Worktree fleets for parallel agent phas… | key:unspecified |
| ACODE-50 | 📄 | طبقة مهايئ مُنمّطة لـ SDK أو REST خارجي · Typed vendor SDK/REST adapter boundary | SP-0041 Worktree fleets for parallel agent phas… | — |
| ACODE-100 | 📄 | صيد الأخطاء بمستويات إثبات · Bug hunt with tiered evidence findings | SP-0042 Four-phase reproduce-hypothesize-fix de… | — |
| ACODE-101 | 📄 | تشخيص فشل CI مع تنقيح السجلات · CI failure diagnosis with redacted logs | SP-0042 Four-phase reproduce-hypothesize-fix de… | — |
| ACODE-103 | 📄 | تصحيح الأخطاء بأربع مراحل منهجية · Four-phase reproduce-hypothesize-fix debugging | SP-0042 Four-phase reproduce-hypothesize-fix de… | — |
| ACODE-104 | 📄 | ماسح الإخفاقات الصامتة والأخطاء المبتلعة · Hidden-failure scanner for swallowed errors | SP-0042 Four-phase reproduce-hypothesize-fix de… | — |
| ACODE-107 | 📄 | جلسة تصحيح Kubernetes بحاوية مؤقتة · kubectl debug ephemeral container session | SP-0042 Four-phase reproduce-hypothesize-fix de… | — |
| ACODE-108 | 📄 | عزل السبب الجذري طبقيًا قبل التعديل · Layered root-cause isolation before editing | SP-0042 Four-phase reproduce-hypothesize-fix de… | — |
| ACODE-111 | 📄 | إعادة بناء تجمد macOS من تقارير التشخيص · macOS freeze/panic reconstruction from DiagnosticReports | SP-0042 Four-phase reproduce-hypothesize-fix de… | os:macos |
| ACODE-112 | 📄 | فرضيات مرتبة قابلة للدحض مع قياس موسوم · Ranked falsifiable hypotheses with tagged instrumentation | SP-0042 Four-phase reproduce-hypothesize-fix de… | — |
| ACODE-113 | 📄 | حلقة تغذية راجعة قبل الفرضيات · Red-capable feedback loop before hypothesizing | SP-0042 Four-phase reproduce-hypothesize-fix de… | chromium |
| ACODE-114 | 📄 | إثبات الإصلاح باختبار أحمر ثم أخضر · Red-green-revert proof for bug fixes | SP-0042 Four-phase reproduce-hypothesize-fix de… | git |
| ACODE-115 | 📄 | حزمة تشخيص مُنقّحة بقائمة سماح · Redacted allowlist-based support debug bundle | SP-0042 Four-phase reproduce-hypothesize-fix de… | — |
| ACODE-117 | 📄 | تصحيح الأخطاء بالسبب الجذري أولاً · Root-cause-first debugging with one hypothesis | SP-0042 Four-phase reproduce-hypothesize-fix de… | git, pip:hypothesis |
| ACODE-118 | 📄 | سير عمل تصحيح مشكلة Sentry · Sentry issue debug-and-fix workflow | SP-0042 Four-phase reproduce-hypothesize-fix de… | — |
| ACODE-119 | 📄 | فحص الإخفاقات الصامتة في الفروقات · Silent failure scan on git diff | SP-0042 Four-phase reproduce-hypothesize-fix de… | python3, git |
| ACODE-234 | 📄 | اختبار استكشافي لتطبيق ويب بأدلة إعادة إنتاج كاملة · Exploratory web-app QA with full repro evidence | SP-0042 Four-phase reproduce-hypothesize-fix de… | chromium |
| ACODE-238 | 📄 | تشخيص أعطال تكامل SaaS المستعصية طبقةً طبقة · Layer-by-layer deep debugging of a stubborn SaaS integration | SP-0042 Four-phase reproduce-hypothesize-fix de… | — |
| ACODE-97 | 📄 | تصحيح تنافسي بفرضيات متعددة ووكلاء · Adversarial competing-hypothesis debugging with agent team | SP-0042 Four-phase reproduce-hypothesize-fix de… | pip:hypothesis |
| ACODE-98 | 📄 | تصحيح عدائي متعدد الوكلاء بفرضيات متنافسة · Adversarial multi-agent competing-hypothesis debugging | SP-0042 Four-phase reproduce-hypothesize-fix de… | — |
| ACODE-14 | 📄 | حلقة تجارب ذاتية بمقياس: احتفظ أو تراجع · Metric-driven autonomous experiment loop (keep or reset) | SP-0043 Stacked PRs with gh stack | python3, git |
| ACODE-200 | 📄 | تقسيم التغييرات إلى commits ذرية · Atomic commit splitting by purpose | SP-0043 Stacked PRs with gh stack | git |
| ACODE-201 | 📄 | مراقبة PR حتى يصبح جاهزا للدمج · Babysit PR until green and mergeable | SP-0043 Stacked PRs with gh stack | gh |
| ACODE-202 | 📄 | سجل تغييرات من الكوميتات · Changelog from commits, Keep a Changelog | SP-0043 Stacked PRs with gh stack | git |
| ACODE-203 | 📄 | رسالة commit بصيغة Conventional من التغييرات · Conventional commit from staged diff | SP-0043 Stacked PRs with gh stack | git |
| ACODE-204 | 📄 | خطافات تمنع أوامر git الخطرة · Dangerous git command guardrail hooks | SP-0043 Stacked PRs with gh stack | — |
| ACODE-205 | 📄 | محاكاة تعارضات قائمة الدمج · Merge queue conflict simulation | SP-0043 Stacked PRs with gh stack | git |
| ACODE-206 | 📄 | مراقبة طلب الدمج حتى الدمج · PR babysit loop to merge | SP-0043 Stacked PRs with gh stack | mcp:github |
| ACODE-207 | 📄 | وصف PR من الفروقات وقالب المستودع · PR body from diff using repo template | SP-0043 Stacked PRs with gh stack | git, gh, mcp:github |
| ACODE-208 | 📄 | فتح طلب دمج بوصف واضح · PR creation with reviewer-friendly body | SP-0043 Stacked PRs with gh stack | gh |
| ACODE-210 | 📄 | إصدار نسخة مع سجل التغييرات والوسم · Release cut with changelog and tag | SP-0043 Stacked PRs with gh stack | — |
| ACODE-211 | 📄 | حل تعارضات الدمج وإعادة التأسيس · Resolve rebase and merge conflicts | SP-0043 Stacked PRs with gh stack | git |
| ACODE-212 | 📄 | تقسيم فرع إلى فروع بكوميت واحد · Split branch into one-commit branches | SP-0043 Stacked PRs with gh stack | git |
| ACODE-213 | 📄 | طلبات دمج متراكبة عبر gh stack · Stacked PRs with gh stack | SP-0043 Stacked PRs with gh stack | — |
| ACODE-214 | 📄 | طلبات دمج متراكمة مع Graphite وMergify · Stacked PRs with Graphite or Mergify | SP-0043 Stacked PRs with gh stack | node |
| ACODE-215 | 📄 | مسار من issue إلى PR بأشجار عمل معزولة · Worktree-isolated issue-to-PR flow | SP-0043 Stacked PRs with gh stack | git, gh |
| ACODE-216 | 📄 | إدارة worktree وتنظيفها بأمان · Worktree lifecycle and safe cleanup | SP-0043 Stacked PRs with gh stack | git |
| ACODE-160 | 📄 | تحصين حدود المعدل وإعادة المحاولة · Claude API rate-limit and retry hardening | SP-0044 Payments and billing integration guide | — |
| ACODE-21 | 📄 | معالجة 429: انتظار وتراجع أسي مع تشويش · 429 handler: Retry-After, backoff, jitter | SP-0044 Payments and billing integration guide | — |
| ACODE-22 | 📄 | تحويل حالات المهام غير المتزامنة لأحداث · Async job state to durable internal events | SP-0044 Payments and billing integration guide | — |
| ACODE-23 | 📄 | قائمة صمود الخلفية أمام الاعتماديات · Backend resilience checklist for dependencies | SP-0044 Payments and billing integration guide | — |
| ACODE-32 | 📄 | استقبال OAuth محلي مع ملفات رموز محمية · Local OAuth callback with 0600 token files | SP-0044 Payments and billing integration guide | key:unspecified |
| ACODE-33 | 📄 | فوترة بالاستهلاك مع تسجيل غير مكرر · Metered billing with idempotent usage | SP-0044 Payments and billing integration guide | — |
| ACODE-34 | 📄 | مدفوعات آمنة: دفتر مزدوج وتسوية · Money-safe payments: ledger, idempotency, reconciliation | SP-0044 Payments and billing integration guide | — |
| ACODE-35 | 📄 | تخطيط نمط OAuth والصلاحيات وتجديد الرموز · OAuth grant, scope and token-refresh planning | SP-0044 Payments and billing integration guide | key:unspecified |
| ACODE-37 | 📄 | اختيار تدفق OAuth/OIDC حسب نوع العميل · OAuth2/OIDC flow selection by client type | SP-0044 Payments and billing integration guide | key:unspecified |
| ACODE-38 | 📄 | توليد مواصفة OpenAPI 3.1 واستخراجها من الكود · OpenAPI 3.1 spec generation and discovery | SP-0044 Payments and billing integration guide | — |
| ACODE-39 | 📄 | تدفقات مصادقة بلا كلمة مرور وJWT · Passwordless, passkey and JWT auth flows | SP-0044 Payments and billing integration guide | key:unspecified |
| ACODE-40 | 📄 | دليل دمج الدفع والفوترة · Payments and billing integration guide | SP-0044 Payments and billing integration guide | — |
| ACODE-43 | 📄 | محدد معدل طلبات مشترك مع تراجع أسي · Shared rolling-window rate limiter with backoff | SP-0044 Payments and billing integration guide | — |
| ACODE-44 | 📄 | خط بناء مورد Express من مواصفة · Spec-driven Express resource build pipeline | SP-0044 Payments and billing integration guide | node |
| ACODE-45 | 📄 | إعداد SPF وDKIM وDMARC بمراحل · SPF, DKIM, DMARC staged rollout | SP-0044 Payments and billing integration guide | — |
| ACODE-47 | 📄 | قرارات تكامل Stripe والترقية · Stripe integration decisions and upgrades | SP-0044 Payments and billing integration guide | — |
| ACODE-105 | 📄 | دليل حوادث التكامل مع الاحتواء أولاً · Integration incident runbook with containment first | SP-0045 Integration observability with explicit… | — |
| ACODE-106 | 📄 | مراقبة التكاملات بالمقاييس والسجلات والتتبع · Integration observability: metrics, logs, traces, alerts | SP-0045 Integration observability with explicit… | — |
| ACODE-11 | 📄 | حلقة تطوير محلية ببيانات وهمية واختبار حي اختياري · Fixture-first local dev loop with opt-in live test | SP-0045 Integration observability with explicit… | key:unspecified |
| ACODE-110 | 📄 | خطة قياس مراقبة منخفضة التعدد · Low-cardinality observability instrumentation plan | SP-0045 Integration observability with explicit… | — |
| ACODE-162 | 📄 | رصد تطبيقات الذكاء التوليدي بـ OpenTelemetry · GenAI observability with OpenTelemetry | SP-0045 Integration observability with explicit… | — |
| ACODE-164 | 📄 | تحصين LangChain 1.0 للإنتاج · LangChain 1.0 production hardening | SP-0045 Integration observability with explicit… | — |
| ACODE-167 | 📄 | مراقبة LLM وتحليل الإخفاقات · LLM observability and failure triage | SP-0045 Integration observability with explicit… | — |
| ACODE-241 | 📄 | مراجعة مطبات التكامل المتكررة قبل الإصدار · Recurring integration pitfall audit before release | SP-0045 Integration observability with explicit… | — |
| ACODE-242 | 📄 | عزل بيئات التطوير والتجربة والإنتاج في التكامل · Prove dev/staging/production isolation for an integration | SP-0045 Integration observability with explicit… | key:unspecified |
| ACODE-243 | 📄 | قياس صحة تكامل خارجي ونتائجه بمقامات صريحة · Integration observability with explicit denominators | SP-0045 Integration observability with explicit… | — |
| ACODE-245 | 📄 | أنماط موثوقية تكامل خارجي: هوية عمل واحدة لكل إعادة · Integration reliability: one idempotency model for every retry path | SP-0045 Integration observability with explicit… | — |
| ACODE-60 | 📄 | حزمة جاهزية التكامل للإنتاج · Integration production-readiness pack (hello, CI, observability) | SP-0045 Integration observability with explicit… | — |
| ACODE-173 | 📄 | تتابع مزودي LLM عبر Router · Vendor failover waterfall via LiteLLM Router | SP-0046 Supabase RLS, auth and key hygiene | python3 |
| ACODE-235 | 📄 | تدقيق الامتثال لـ GDPR انطلاقًا من جرد البيانات الشخصية · GDPR review built on a personal-data inventory | SP-0046 Supabase RLS, auth and key hygiene | — |
| ACODE-239 | 📄 | دورة حياة البيانات المارّة بخدمة خارجية: تصنيف واحتفاظ وحذف · Data lifecycle governance for data sent through a SaaS vendor | SP-0046 Supabase RLS, auth and key hygiene | — |
| ACODE-24 | 📄 | أنماط خدمات الواجهة الخلفية بعدة لغات · Backend service patterns: Node, Go, .NET, Django | SP-0046 Supabase RLS, auth and key hygiene | — |
| ACODE-240 | 📄 | ربط أدوار المزوّد بصلاحيات التطبيق ومفاتيح الخدمة · Map vendor roles to application RBAC and scoped service keys | SP-0046 Supabase RLS, auth and key hygiene | — |
| ACODE-244 | 📄 | معمارية مرجعية لتكامل خارجي: بوابة سياسات ومحوّل وتسوية · Reference architecture for a vendor integration: policy gateway, adapter, reconciliation | SP-0046 Supabase RLS, auth and key hygiene | — |
| ACODE-247 | 📄 | خريطة دورة حياة تكامل SaaS: من التثبيت إلى الحوادث · SaaS integration lifecycle map: install to incident | SP-0046 Supabase RLS, auth and key hygiene | python3 |
| ACODE-30 | 📄 | مصادقة JWT مع تدوير التحديث وصلاحيات الأدوار · JWT auth with refresh rotation and RBAC | SP-0046 Supabase RLS, auth and key hygiene | key:unspecified |
| ACODE-46 | 📄 | قوالب SSE والمصادقة والزمن الحقيقي · SSE, auth, SSO and realtime scaffolds | SP-0046 Supabase RLS, auth and key hygiene | — |
| ACODE-93 | 📄 | ربط تطبيق Supabase وتوسيعه · Supabase app wiring and scaling | SP-0046 Supabase RLS, auth and key hygiene | npm:react |
| ACODE-94 | 📄 | سياسات RLS ومفاتيح Supabase الآمنة · Supabase RLS, auth and key hygiene | SP-0046 Supabase RLS, auth and key hygiene | — |
| ACODE-177 | 📄 | مخطط تسلسل موثق من نقطة دخول الكود · Cited sequence diagram from code entry point | SP-0047 Dependency graph cited from build manif… | npm:mermaid |
| ACODE-222 | 📄 | قاعدة الاعتماد في البنية النظيفة · Clean Architecture dependency rule | SP-0047 Dependency graph cited from build manif… | — |
| ACODE-231 | 📄 | تدقيق كل الترقيات الممكنة بمصفوفة مخاطرة/عائد قبل التطبيق · Upgrade-everything audit with a risk/reward matrix | SP-0047 Dependency graph cited from build manif… | — |
| ACODE-237 | 📄 | تثبيت كل أسطح الإصدارات لتقوية سلسلة التوريد · Pin every version surface for supply-chain hardening | SP-0047 Dependency graph cited from build manif… | node, python3 |
| ACODE-74 | 📄 | تدقيق وضغط ملفات تهيئة الوكيل · Agent onboarding file audit and compression | SP-0047 Dependency graph cited from build manif… | — |
| ACODE-75 | 📄 | استعلام رسم المعرفة قبل مسح الملفات · Code knowledge graph queries before file scanning | SP-0047 Dependency graph cited from build manif… | — |
| ACODE-77 | 📄 | مسح الكود الميت وصحة الاعتماديات · Dead code and dependency hygiene sweep | SP-0047 Dependency graph cited from build manif… | — |
| ACODE-78 | 📄 | رسم اعتماديات موثق من ملفات البناء · Dependency graph cited from build manifests | SP-0047 Dependency graph cited from build manif… | npm:mermaid |
| ACODE-79 | 📄 | هندسة عكسية وصفية لمواصفات قابلة للتتبع · Descriptive reverse engineering into traceable specs | SP-0047 Dependency graph cited from build manif… | — |
| ACODE-80 | 📄 | شرح تغيير أو مسار كود بالأدلة · Explain a change or code path grounded in evidence | SP-0047 Dependency graph cited from build manif… | git |
| ACODE-220 | 📄 | مراجعة أمان للتغيير لا للمستودع كله · Change-scoped security review vs posture audit | SP-0048 Webhook receiver with HMAC and idempote… | — |
| ACODE-52 | 📄 | مستقبل ويبهوك موثّق وآمن من التكرار · Verified idempotent webhook receiver | SP-0048 Webhook receiver with HMAC and idempote… | — |
| ACODE-53 | 📄 | مستهلك webhook: توقيع HMAC وإزالة التكرار · Webhook consumer: raw-body HMAC, dedupe, fast ack | SP-0048 Webhook receiver with HMAC and idempote… | — |
| ACODE-54 | 📄 | مستقبل ويب هوك: توقيع وتكرار آمن · Webhook receiver: HMAC, idempotency, replay | SP-0048 Webhook receiver with HMAC and idempote… | — |
| ACODE-55 | 📄 | مستقبل ويبهوك مع توقيع HMAC ومنع التكرار · Webhook receiver with HMAC and idempotency | SP-0048 Webhook receiver with HMAC and idempote… | — |
| ACODE-58 | 📄 | دورة حياة أعلام الميزات وتدقيق الديون · Feature flag lifecycle and debt audit | SP-0048 Webhook receiver with HMAC and idempote… | — |
| ACODE-59 | 📄 | مقارنة لقطات الذاكرة لكشف التسربات · Heap snapshot diff for web memory leaks | SP-0048 Webhook receiver with HMAC and idempote… | — |
| ACODE-62 | 📄 | التقاط وفك حركة مرور التطبيق · Mitmproxy app traffic capture and decode | SP-0048 Webhook receiver with HMAC and idempote… | — |
| ACODE-63 | 📄 | فحص امتثال تطبيق شوبيفاي قبل التقديم · Shopify App Store pre-submission compliance sweep | SP-0048 Webhook receiver with HMAC and idempote… | — |
| ACODE-65 | 📄 | التحقق من توقيع الويب هوك مع منع التكرار · Webhook HMAC verify, dedupe, fast-ack | SP-0048 Webhook receiver with HMAC and idempote… | — |
| ACODE-06 | 📄 | إعادة هيكلة مرحلية بنقاط حفظ · Checkpointed multi-phase refactor surviving context limits | SP-0049 Dead code and import cleanup scan | — |
| ACODE-09 | 📄 | تفويض المهام لوكيل آخر مع بوابة مراجعة · Delegate to Codex or Claude with review gate | SP-0049 Dead code and import cleanup scan | git |
| ACODE-195 | 📄 | تصنيف نتائج regex قبل الاستبدال الجماعي · Classify regex matches before bulk sweep | SP-0049 Dead code and import cleanup scan | — |
| ACODE-196 | 📄 | فحص الكود الميت وتنظيف الاستيراد · Dead code and import cleanup scan | SP-0049 Dead code and import cleanup scan | — |
| ACODE-197 | 📄 | إضافة رمز تشخيص منظم لمكتبة JS · Diagnostic code catalog entry | SP-0049 Dead code and import cleanup scan | — |
| ACODE-221 | 📄 | التحقق من السلوك لا من التفاصيل الداخلية، بأوامر المستودع نفسه · Behaviour-level assertions per layer, with the repo's own commands | SP-0049 Dead code and import cleanup scan | node |
| ACODE-224 | 📄 | قياس التحسين مقابل خط أساس مُلتقط قبل التغيير · Measure improvement against a baseline captured before | SP-0049 Dead code and import cleanup scan | — |
| ACODE-225 | 📄 | jq: نموذج المرشّح لتدفق JSON · jq filter mental model for JSON streams | SP-0049 Dead code and import cleanup scan | — |
| ACODE-84 | 📄 | بحث وإعادة كتابة بنيوية بـ ast-grep · Structural search and rewrite with ast-grep | SP-0049 Dead code and import cleanup scan | node |
| ACODE-178 | 📄 | البحث في مكتبة المكونات بسكربت مساعد · Component library lookup with helper script | SP-0050 shadcn and UnoCSS component styling set… | node |
| ACODE-179 | 📄 | بوابة جودة التصميم في CI · Design-quality CI gate with SARIF | SP-0050 shadcn and UnoCSS component styling set… | — |
| ACODE-180 | 📄 | بناء نظام رموز التصميم · Design token system scaffold | SP-0050 shadcn and UnoCSS component styling set… | npm:react |
| ACODE-182 | 📄 | هيكلة مكون React مع shadcn وTailwind وStorybook · React component scaffold with shadcn, Tailwind, Storybook | SP-0050 shadcn and UnoCSS component styling set… | npm:react |
| ACODE-183 | 📄 | إعداد shadcn وUnoCSS لتنسيق المكونات · shadcn and UnoCSS component styling setup | SP-0050 shadcn and UnoCSS component styling set… | npm:react |
| ACODE-184 | 📄 | قواعد تركيب shadcn وTailwind · shadcn/ui and Tailwind composition rules | SP-0050 shadcn and UnoCSS component styling set… | npm:react |
| ACODE-185 | 📄 | فاحص وصولية HTML مع بقايا يدوية · Stdlib HTML accessibility linter with manual residue | SP-0050 shadcn and UnoCSS component styling set… | npm:axe |
| ACODE-186 | 📄 | مراجعة الوصولية وفق WCAG · WCAG four-principle accessibility review | SP-0050 shadcn and UnoCSS component styling set… | npm:axe, npm:pa11y |
| ACODE-181 | 📄 | فحص القيم الصلبة واستبدالها برموز · Hardcoded-style scan to design tokens | SP-0051 Zero-downtime expand/contract schema mi… | — |
| ACODE-87 | 📄 | بوابة أمان لأوامر SQL المدمرة مع تجربة جافة · Destructive-SQL safety gate with dry-run | SP-0051 Zero-downtime expand/contract schema mi… | — |
| ACODE-88 | 📄 | مراجعة مخطط قاعدة البيانات بعدسات متعددة · Multi-lens database schema review | SP-0051 Zero-downtime expand/contract schema mi… | lean |
| ACODE-89 | 📄 | ترقية Prisma من 6 إلى 7 · Prisma 6 to 7 upgrade procedure | SP-0051 Zero-downtime expand/contract schema mi… | node |
| ACODE-91 | 📄 | نموذج بيانات Redis وقائمة التشغيل · Redis data model and ops checklist | SP-0051 Zero-downtime expand/contract schema mi… | — |
| ACODE-92 | 📄 | تصميم مخطط من وصف المجال · Schema design from domain description | SP-0051 Zero-downtime expand/contract schema mi… | — |
| ACODE-95 | 📄 | ترحيل مخطط قاعدة البيانات دون توقف · Zero-downtime expand/contract schema migration | SP-0051 Zero-downtime expand/contract schema mi… | — |
| ACODE-96 | 📄 | خطة ترحيل Postgres بلا توقف · Zero-downtime Postgres migration playbook | SP-0051 Zero-downtime expand/contract schema mi… | node |
| ACODE-187 | 📄 | بيفي: ECS وتدفق الحالات وخط الأصول · Bevy ECS, state flow and asset pipeline | SP-0052 Godot 4 GDScript architecture patterns | — |
| ACODE-188 | 📄 | حزمة ألعاب المتصفح وPhaser · Browser game stack, Phaser and web foundations | SP-0052 Godot 4 GDScript architecture patterns | npm:esbuild |
| ACODE-189 | 📄 | فيزياء خطوة ثابتة وكشف تصادم · Fixed-step physics and collision broadphase | SP-0052 Godot 4 GDScript architecture patterns | — |
| ACODE-190 | 📄 | اختيار تمثيل الهندسة وSDF وتحويل الشبكات · Geometry, SDF and mesh-voxel conversion choice | SP-0052 Godot 4 GDScript architecture patterns | — |
| ACODE-191 | 📄 | أنماط معمارية لـ GDScript في Godot 4 · Godot 4 GDScript architecture patterns | SP-0052 Godot 4 GDScript architecture patterns | chromium |
| ACODE-192 | 📄 | فحص محرر Godot الحي عبر سطر الأوامر · Godot live-editor inspection via CLI | SP-0052 Godot 4 GDScript architecture patterns | — |
| ACODE-193 | 📄 | حلقة قياس أداء اللعبة · Measured game performance loop | SP-0052 Godot 4 GDScript architecture patterns | — |
| ACODE-194 | 📄 | وحدة DOTS وأتمتة محركات Unity وUnreal · Unity DOTS ECS and Unreal/Unity automation | SP-0052 Godot 4 GDScript architecture patterns | python3 |
| ACODE-120 | 📄 | كاشف التراجع الصامت من بصمات السجل · Silent-fallback detector from log signatures | SP-0053 Python projects, scripts and tools with… | python3 |
| ACODE-198 | 📄 | إدارة مهام todo.md عبر سكربتات · Markdown todo file task scripts | SP-0053 Python projects, scripts and tools with… | python3 |
| ACODE-199 | 📄 | مزامنة متتبع الميزات مع TODO · Sync feature tracker with TODO | SP-0053 Python projects, scripts and tools with… | — |
| ACODE-223 | 📄 | أداء الويب: الكمون قبل عرض النطاق · Web performance: latency before bandwidth | SP-0053 Python projects, scripts and tools with… | — |
| ACODE-227 | 📄 | ضبط ruff للفحص والتنسيق دون فخ select · ruff lint and format without the select trap | SP-0053 Python projects, scripts and tools with… | python3 |
| ACODE-228 | 📄 | إدارة مشاريع بايثون والسكربتات ببرنامج uv · Python projects, scripts and tools with uv | SP-0053 Python projects, scripts and tools with… | python3 |
| ACODE-83 | 📄 | محلل Python AST يراعي الأسماء المستعارة والنطاق · Python AST analyzer with alias and scope handling | SP-0053 Python projects, scripts and tools with… | python3 |
| ACODE-66 | 📄 | محافظ Circle وUSDC متعدد السلاسل · Circle USDC wallets and cross-chain balance | SP-0054 Typed EVM reads and NFT APIs with viem | node, key:unspecified |
| ACODE-67 | 📄 | قوالب بروتوكولات دي فاي وعقود NFT · DeFi protocol and NFT contract templates | SP-0054 Typed EVM reads and NFT APIs with viem | — |
| ACODE-68 | 📄 | تصميم إرسال معاملات EVM آمن · Safe EVM transaction submission design | SP-0054 Typed EVM reads and NFT APIs with viem | — |
| ACODE-70 | 📄 | تدقيق أمان عقود سوليديتي · Solidity vulnerability audit and secure patterns | SP-0054 Typed EVM reads and NFT APIs with viem | — |
| ACODE-71 | 📄 | تطوير Sui Move وإعداد Solana · Sui Move and Solana network/keypair setup | SP-0054 Typed EVM reads and NFT APIs with viem | — |
| ACODE-72 | 📄 | قراءات EVM مكتوبة وواجهات NFT عبر viem · Typed EVM reads and NFT APIs with viem | SP-0054 Typed EVM reads and NFT APIs with viem | node, key:unspecified |
| ACODE-232 | 📄 | كشف الاختبارات الخضراء الكاذبة · False-green test detection | SP-0055 Smart contract test suite with Hardhat… | — |
| ACODE-233 | 📄 | اختبار في فضاء مصغّر: تفكيك ادعاء التكافؤ قبل التجربة · Reduced-space test: decompose the equivalence claim first | SP-0055 Smart contract test suite with Hardhat… | — |
| ACODE-36 | 📄 | اختبار تكامل يعدّ عدد إصدارات التوكن · OAuth token-mint counting integration test | SP-0055 Smart contract test suite with Hardhat… | key:unspecified |
| ACODE-69 | 📄 | اختبار العقود الذكية بهاردهات وفاوندري · Smart contract test suite with Hardhat and Foundry | SP-0055 Smart contract test suite with Hardhat… | node, key:unspecified |
| ACODE-90 | 📄 | توليد بيانات اختبار وكود ORM · Realistic test data seeding and ORM code generation | SP-0055 Smart contract test suite with Hardhat… | — |
| ACODE-163 | 📄 | خط RAG هجين مع إحالات · Hybrid-search RAG pipeline with citations | SP-0056 RAG pipeline build and tuning guide | pip:chromadb |
| ACODE-166 | 📄 | تخطيط ضبط نماذج اللغة SFT/DPO · LLM fine-tuning job planning (SFT/DPO/GRPO) | SP-0056 RAG pipeline build and tuning guide | pip:llama-cpp |
| ACODE-171 | 📄 | دليل بناء وضبط خط RAG · RAG pipeline build and tuning guide | SP-0056 RAG pipeline build and tuning guide | pip:chromadb |
| ACODE-229 | 📄 | اختيار طريقة مواءمة التفضيلات DPO/ORPO/KTO/SimPO · Choosing DPO, ORPO, KTO or SimPO for preference tuning | SP-0056 RAG pipeline build and tuning guide | — |
| ACODE-174 | 📄 | بناء شجرة هجوم · Attack tree construction | SP-0057 Twilio regulatory bundle provisioning | graphviz, npm:mermaid |
| ACODE-175 | 📄 | وثائق ما قبل الإطلاق للتطبيقات المولدة · Pre-ship documentation set for vibe-coded apps | SP-0057 Twilio regulatory bundle provisioning | — |
| ACODE-176 | 📄 | تجهيز حزم الامتثال لأرقام Twilio · Twilio regulatory bundle provisioning | SP-0057 Twilio regulatory bundle provisioning | — |
| ACODE-48 | 📄 | دليل بناء رسائل وصوت Twilio · Twilio messaging and voice build guide | SP-0057 Twilio regulatory bundle provisioning | — |
| ACODE-109 | 📄 | تحليل السجلات للطلبات البطيئة وأنماط الخطأ · Log analysis for slow requests and error patterns | SP-0058 SLO workshop with error budget policy | — |
| ACODE-147 | 📄 | خطة تغيير كوبرنيتس إنتاجية بمعايير SRE · Production Kubernetes change plan with SRE standards | SP-0058 SLO workshop with error budget policy | — |
| ACODE-73 | 📄 | ورشة SLO وسياسة ميزانية الخطأ · SLO workshop with error budget policy | SP-0058 SLO workshop with error budget policy | — |
| ACODE-12 | 📄 | حلقة مهام بوكلاء جدد ومراجعة مرحلتين · Fresh-subagent task loop with two-stage review | SP-0059 Code review checklist | git, claude:tools |
| ACODE-81 | 📄 | خوارزمية تعديل الكود القديم باختبارات التوصيف · Legacy code change algorithm with characterization tests | SP-0059 Code review checklist | — |
| ACODE-82 | 📄 | رسم المشروع بوكلاء متوازين وكشف التغيير · Parallel subagent mapping with merkle change detection | SP-0059 Code review checklist | claude:tools |
| ACODE-236 | 📄 | دليل سردي لمستودع غير مألوف للمساهمين الجدد · Narrative codebase guide for newcomers | SP-0062 Understand any codebase or skill set fa… | npm:mermaid |
| ACODE-76 | 📄 | خريطة مشروع مؤرخة مع وصفات التعديل · Dated codebase map with change recipes | SP-0062 Understand any codebase or skill set fa… | — |
| ACODE-01 | 📄 | اختبار حدود الحقن وتسليم القرار للبشر · Agent injection boundary and human-handoff tests | SP-0064 Secrets hygiene | — |
| ACODE-209 | 📄 | إزالة أسرار دُفعت من السجل المستضاف · Purge pushed secrets from hosted history | SP-0064 Secrets hygiene | git, gh |
| ACODE-218 | 📄 | حدود الثقة في الأدوات: الأسرار تُحقن والصلاحيات في الكود · Tool trust boundary: injected secrets, permissions in code | SP-0064 Secrets hygiene | — |
| ACODE-219 | 📄 | منع رفع الأسرار عند الالتزام · Block secrets at commit time | SP-0064 Secrets hygiene | — |
| ACODE-217 | 📄 | تصميم أدوات الوكلاء: المستهلك نموذج لا إنسان · Agent tool design: the consumer is a model | SP-0065 REA MCP tool `goto_address` | claude:tools |
| ACODE-230 | 📄 | تصميم خادم MCP: نموذج النشر ونمط الأدوات قبل الكود · MCP server design: deployment model and tool pattern before code | SP-0065 REA MCP tool `goto_address` | python3, key:unspecified |
| ACODE-61 | 📄 | تطبيق MCP بأداة وواجهة · MCP App tool plus UI resource | SP-0065 REA MCP tool `goto_address` | npm:esbuild, npm:react, key:openai |
| ACODE-226 | 📄 | تصميم تطبيقات Apple: اختر المسار أولاً · Apple platform design: choose the track first | SP-0068 Run inspect_macho without launching Hop… | npm:react, os:macos |

## code-engineering (code)

chapter: [code-engineering](../powers/code-engineering.md) · card: `usip-library/cards/software/code-engineering.md` · tools: `architecture-sizer` · `capability-graph` · `kosif-remote-commander` · `motion-stack` · `package-skill` · `rea-owned-repo-batch` · `repository-capability-packer`

| ID | | القدرة / power | SP | يحتاج / requires |
|---|---|---|---|---|
| CODE-23 | ✅ | Hypothesis: اختبارات قائمة على الخصائص تولّد مدخلات فاشلة · Hypothesis: Property-based tests that generate and shrink failing inputs | SP-0059 Code review checklist | pip:hypothesis |
| CODE-24 | ✅ | Pandera: تعريف عقود بيانات لإطارات pandas وPolars وفرضها · Pandera: Declare and enforce schemas on pandas/Polars dataframes (data contracts) | SP-0059 Code review checklist | pip:pandas, pip:polars, pip:pandera |
| CODE-17 | 🔑 | مراجعة طلب دمج بفريق وكلاء · PR review fan-out | SP-0059 Code review checklist | gh, mcp:github, key:unspecified |
| CODE-04 | 📄 | دليل التعرّف على مستودع · Codebase onboarding guide | SP-0059 Code review checklist | git |
| CODE-05 | 📄 | قائمة أثر التغيير · Change-impact checklist | SP-0059 Code review checklist | — |
| CODE-06 | 📄 | حقائق قبل أول تعديل · Fact-forcing before the first edit | SP-0059 Code review checklist | — |
| CODE-07 | 📄 | اتبع أسلوب المستودع القائم · Inherit the repo's style | SP-0059 Code review checklist | — |
| CODE-08 | 📄 | التطوير بالاختبار أولًا · Test-driven development | SP-0059 Code review checklist | — |
| CODE-09 | 📄 | حلقة التحقق بست مراحل · Six-phase verification loop | SP-0059 Code review checklist | ffmpeg, node, git, key:unspecified |
| CODE-10 | 📄 | نقاط تفتيش وخط أساس للانحدار · Checkpoints, regression baselines and pass^k | SP-0059 Code review checklist | — |
| CODE-11 | 📄 | حلقة التشخيص من الجذر · Root-cause debugging loop | SP-0059 Code review checklist | pip:hypothesis |
| CODE-13 | 📄 | صيد الأعطال الصامتة · Silent-failure and click-path hunt | SP-0059 Code review checklist | — |
| CODE-14 | 📄 | حلقة تحسين أداء مقاسة · Measured optimization loop | SP-0059 Code review checklist | — |
| CODE-15 | 📄 | معالجة أخطاء متينة · Resilient error handling | SP-0059 Code review checklist | — |
| CODE-16 | 📄 | قائمة مراجعة الكود · Code review checklist | SP-0059 Code review checklist | — |
| CODE-18 | 📄 | إعادة هيكلة آمنة · Safe refactoring | SP-0059 Code review checklist | key:graphify |
| CODE-19 | 📄 | سجل قرار معماري · Architecture decision record | SP-0059 Code review checklist | — |
| CODE-22 | 📄 | نظافة الإيداع وكلمات الحالة · Commit hygiene & status words | SP-0059 Code review checklist | git |
| CODE-03 | ✅ | إثبات حزمة في بيئة معزولة · Prove a package in an isolated venv | SP-0060 Search-first: adopt, extend, compose, b… | python3 |
| CODE-01 | 📄 | ابحث قبل أن تبني · Search-first: adopt, extend, compose, build | SP-0060 Search-first: adopt, extend, compose, b… | node, python3 |
| CODE-02 | 📄 | الوثائق الحية قبل الذاكرة · Live docs over memory | SP-0060 Search-first: adopt, extend, compose, b… | node, claude:tools |
| CODE-12 | 📄 | إصلاح البناء بأقل فرق · Minimal-diff build fixing | SP-0060 Search-first: adopt, extend, compose, b… | — |
| CODE-20 | 📄 | الحتمي أولًا والنموذج للذيل · Deterministic first, model for the tail | SP-0060 Search-first: adopt, extend, compose, b… | — |
| CODE-21 | 📄 | ذاكرة مؤقتة ببصمة المحتوى · Content-hash cache | SP-0060 Search-first: adopt, extend, compose, b… | key:graphify |

## ui-product-device (motion)

chapter: [ui-product-device](../powers/ui-product-device.md) · card: `usip-library/cards/software/ui-product-device.md` · tools: `ui-beat`

| ID | | القدرة / power | SP | يحتاج / requires |
|---|---|---|---|---|
| UI-11 | ✅ | مؤشر بفيزياء في motion-kit · motion-kit physics cursor + press + typeOn | SP-0447 Cursor as protagonist | node, chromium |
| UI-X03 | ✅ | تسجيل عرض واجهة بـPlaywright · Playwright UI demo recording (WebM) | SP-0447 Cursor as protagonist | ffmpeg, node, chromium |
| UI-14 | 🟢 | حلقة الضغط والتموج · Press ring & click ripple | SP-0447 Cursor as protagonist | — |
| UI-72 | 🟢 | تسجيل صفحة بخطوات مبرمجة · Scripted page recording (Playwright) | SP-0447 Cursor as protagonist | node, chromium |
| UI-86 | 🟢 | أساليب KOSIF للواجهات · KOSIF UI styles to scaffold | SP-0447 Cursor as protagonist | python3 |
| UI-88 | 🟢 | مراجعة على الإطار: سحب وتحجيم واختصارات · Frame review: drag, resize & Arabic-safe shortcuts | SP-0447 Cursor as protagonist | — |
| UI-17 | 📦 | المؤشر المغناطيسي · Magnetic cursor & magnetic buttons | SP-0447 Cursor as protagonist | npm:hyperframes, lean |
| UI-18 | 📦 | سحب وإفلات · Cursor drag & drop | SP-0447 Cursor as protagonist | npm:hyperframes |
| UI-19 | 📦 | تحديد نص ومستطيل وقائمة يمين · Text select, marquee select & context menu | SP-0447 Cursor as protagonist | npm:hyperframes |
| UI-20 | 📦 | مؤشرات متعاونين بأسمائها · Named multiplayer cursors | SP-0447 Cursor as protagonist | npm:hyperframes |
| UI-21 | 📦 | مؤشر وكيل ذكي · AI agent cursor | SP-0447 Cursor as protagonist | npm:hyperframes |
| UI-22 | 📦 | مؤشر اللمس على الهاتف · Touch indicator: tap & swipe | SP-0447 Cursor as protagonist | npm:hyperframes |
| UI-77 | 📦 | تسجيل المتصفح بمؤشر ولوحة لقطات · Browser recording CLI with cursor & contact sheet | SP-0447 Cursor as protagonist | ffmpeg, node, chromium |
| UI-15 | 👁 | مؤشر ماك معبّر يتجه مع حركته · Expressive directional macOS cursor | SP-0447 Cursor as protagonist | os:macos |
| UI-16 | 👁 | مؤشر بهالة لونية يلاحق هدفًا متحركًا · Cursor with accent halo homing on a live target | SP-0447 Cursor as protagonist | — |
| UI-60 | 👁 | اقتراب يقوده المؤشر · Cursor-led push-in & focus zoom | SP-0447 Cursor as protagonist | — |
| UI-01 | 📄 | العرض الصامت: الواجهة تحكي · Silent product demo — the UI tells the story | SP-0447 Cursor as protagonist | — |
| UI-13 | 📄 | تصميم حركة المؤشر · Cursor choreography rules | SP-0447 Cursor as protagonist | — |
| UI-26 | 📄 | طلب يُكتب ثم يُرسل ثم يولّد · Prompt type → submit → generate | SP-0447 Cursor as protagonist | — |
| UI-35 | 📄 | ضغط وتحرير زر نابض · Press-release spring button | SP-0447 Cursor as protagonist | — |
| UI-61 | 📄 | وصفة النقر وفتح نافذة · Click → modal recipe | SP-0447 Cursor as protagonist | npm:remotion |
| UI-89 | 📄 | قواعد صفحات الويب المسلَّمة · Web deliverable rules (landing, perf, hover gating) | SP-0447 Cursor as protagonist | — |
| UI-X01 | 📄 | المؤشر بطلًا · Cursor as protagonist | SP-0447 Cursor as protagonist | chromium |
| UI-12 | ✅ | واجهة منتج على Canvas بدالة draw(t) · Canvas product UI draw(t) recipe | SP-0448 Canvas 2.5D phone (drawPhone) | node, chromium |
| UI-87 | ✅ | مشغّل HTML مستقل بشريط تقديم · Standalone HTML player with seek & reduced motion | SP-0448 Canvas 2.5D phone (drawPhone) | node |
| UI-50 | 🟢 | هاتف 2.5D على Canvas · Canvas 2.5D phone (drawPhone) | SP-0448 Canvas 2.5D phone (drawPhone) | — |
| UI-56 | 🟢 | موك أب HTML بلقطة 2× · HTML/CSS device & package mockup screenshot | SP-0448 Canvas 2.5D phone (drawPhone) | chromium |
| UI-51 | 📦 | مكوّن Device في Remotion · Remotion Device component | SP-0448 Canvas 2.5D phone (drawPhone) | npm:remotion, npm:react |
| UI-54 | 📦 | مروحة أجهزة وانفراد الهواتف · Multi-device splay & phone fan-out | SP-0448 Canvas 2.5D phone (drawPhone) | npm:hyperframes |
| UI-76 | 🔑 | من فيجما إلى طبقات متحركة · Figma frame → animatable layers | SP-0448 Canvas 2.5D phone (drawPhone) | key:unspecified |
| UI-53 | 👁 | نافذة متصفح أو ماك وهمية · Browser chrome & macOS frame mock | SP-0448 Canvas 2.5D phone (drawPhone) | os:macos |
| UI-71 | 👁 | مسرح أداة تصميم ومقابض تحديد · Design-tool canvas, selection handles & size tags | SP-0448 Canvas 2.5D phone (drawPhone) | — |
| UI-82 | 👁 | ستايل برومو المنتج · Product promo style (neon prompt + glass orb) | SP-0448 Canvas 2.5D phone (drawPhone) | — |
| UI-47 | 📄 | ثوابت الهاتف البارامتري · Parametric phone constants | SP-0448 Canvas 2.5D phone (drawPhone) | — |
| UI-48 | 📄 | منظور الجهاز وسرعة دورانه · Device perspective, rotation caps & idle hover | SP-0448 Canvas 2.5D phone (drawPhone) | — |
| UI-49 | 📄 | دخول الجهاز وكشف البطل · Device entrance & hero reveal | SP-0448 Canvas 2.5D phone (drawPhone) | npm:remotion |
| UI-52 | 📄 | تسليم بين جهازين · Two-device turntable handoff | SP-0448 Canvas 2.5D phone (drawPhone) | — |
| UI-X02 | 📄 | تسليم المجسم وطبقات منفجرة · Mockup hand-off and exploded layers | SP-0448 Canvas 2.5D phone (drawPhone) | — |
| UI-57 | 💡 | قلب الهاتف وتبديل الشاشة · Phone flip with mid-swap | SP-0448 Canvas 2.5D phone (drawPhone) | — |
| UI-04 | 🟢 | إعادة بناء الشاشة كطبقات · Layered screen rebuild | SP-0449 Real, locale-correct UI content | — |
| UI-05 | 🟢 | حقيبة أصول من أجزاء حقيقية · Animation kit from real parts | SP-0449 Real, locale-correct UI content | chromium, pip:pillow |
| UI-43 | 🟢 | مؤشرات التبويب والشريط النشط · Tab slide indicator & active rail bar | SP-0449 Real, locale-correct UI content | — |
| UI-39 | 📦 | هيكل لامع يتحول إلى محتوى · Skeleton shimmer → content | SP-0449 Real, locale-correct UI content | npm:hyperframes |
| UI-X04 | 📦 | رموز الحركة وصقل الواجهة · Motion tokens and interface polish (React UIs) | SP-0449 Real, locale-correct UI content | npm:animejs, npm:react |
| UI-63 | 👁 | جدار بطاقات واجهة يطفو بعمق · Floating UI card wall in depth | SP-0449 Real, locale-correct UI content | — |
| UI-83 | 👁 | واجهة ملصقات بظل صلب · Sticker UI with hard offset shadow | SP-0449 Real, locale-correct UI content | — |
| UI-03 | 📄 | محتوى واجهة حقيقي ومحلي · Real, locale-correct UI content | SP-0449 Real, locale-correct UI content | — |
| UI-06 | 📄 | عكس الواجهة للعربية · RTL product-UI mirroring | SP-0449 Real, locale-correct UI content | — |
| UI-07 | 📄 | لوحة البيانات داخل الإطار · Dashboard composition for a frame | SP-0449 Real, locale-correct UI content | — |
| UI-08 | 📄 | تشريح التفاعل الدقيق كوحدة مشهد · Microinteraction anatomy as a beat | SP-0449 Real, locale-correct UI content | — |
| UI-09 | 📄 | مقطع حلقة لمكوّن واحد · Seamless UI component loop (3–6 s) | SP-0449 Real, locale-correct UI content | — |
| UI-62 | 📄 | صفحة ويب مائلة تتمرر · 3D tilted webpage scroll & perspective pan | SP-0449 Real, locale-correct UI content | npm:gsap |
| UI-75 | 📄 | وصفة فيديو ميزة حقيقية · Real-feature video recipe | SP-0449 Real, locale-correct UI content | ffmpeg, node, chromium |
| UI-79 | 📄 | رموز تصميم الواجهة وسلالمها · UI tokens & Refactoring-UI scales | SP-0449 Real, locale-correct UI content | — |
| UI-80 | ✅ | سطح زجاجي للواجهات · Glass surface stack | SP-0450 Control ↔ target live sync | chromium, npm:hyperframes |
| UI-45 | 🟢 | نقطة حالة بهالة وشارة مباشرة · Status dot with halo & live pill | SP-0450 Control ↔ target live sync | — |
| UI-69 | 🟢 | لوحة قياس HUD وشروح مسقطة من 3D · Instrument-panel HUD & projected callouts | SP-0450 Control ↔ target live sync | — |
| UI-38 | 📦 | حقل إدخال: خطأ واهتزاز ونجاح · Input feedback: error shake & valid state | SP-0450 Control ↔ target live sync | npm:hyperframes |
| UI-41 | 📦 | تحول بطاقة إلى لوحة (FLIP) · Shared-element morph: card → panel (FLIP) | SP-0450 Control ↔ target live sync | npm:hyperframes |
| UI-55 | 📦 | آيفون وماك بوك ثلاثيا الأبعاد بشاشات حية · 3D GLTF iPhone & MacBook with live screens | SP-0450 Control ↔ target live sync | chromium, npm:three, npm:gsap, npm:hyperframes … |
| UI-66 | 📦 | مقارنة قبل وبعد · Before/after wipe & comparison split | SP-0450 Control ↔ target live sync | npm:hyperframes |
| UI-67 | 📦 | دوار الشاشات والموكاب الثابت · Screen-flow carousel & sticky mock swap | SP-0450 Control ↔ target live sync | npm:hyperframes |
| UI-31 | 👁 | إجابة متدفقة وسجل حي · Streaming answer & live log | SP-0450 Control ↔ target live sync | — |
| UI-42 | 👁 | إعادة ترتيب قائمة وسطور · FLIP list reorder & self-reordering lines | SP-0450 Control ↔ target live sync | — |
| UI-70 | 👁 | مربع تتبع وماسح ضوئي · AI tracking box & scanner brackets | SP-0450 Control ↔ target live sync | tesseract |
| UI-24 | 📄 | تحكم وهدف يتغيران معًا · Control ↔ target live sync | SP-0450 Control ↔ target live sync | — |
| UI-34 | 🟢 | ضغط ومرور بمنطق القراءة · Press & hover with reading-direction nudges | SP-0451 Plain action labels in tutorials | — |
| UI-74 | 🟢 | فيلم إطلاق kmotion brag · kmotion brag launch film | SP-0451 Plain action labels in tutorials | python3 |
| UI-73 | 📦 | التقاط موقع إلى فيديو · Website capture → video | SP-0451 Plain action labels in tutorials | chromium, npm:hyperframes, npm:lottie |
| UI-23 | 👁 | ضغط اختصار لوحة المفاتيح · Keycap shortcut trigger | SP-0451 Plain action labels in tutorials | — |
| UI-27 | 👁 | وكيل ينجز قائمة مهام · Agent progress theater & tool-call checklist | SP-0451 Plain action labels in tutorials | npm:hyperframes |
| UI-65 | 👁 | نقطة ساخنة مع فقاعة إرشاد · Hotspot tooltip walkthrough | SP-0451 Plain action labels in tutorials | — |
| UI-02 | 📄 | ثلاثية النية والفعل والاستجابة · Intent → action → response with real latency | SP-0451 Plain action labels in tutorials | — |
| UI-10 | 📄 | عناوين أفعال بسيطة في الشروحات · Plain action labels in tutorials | SP-0451 Plain action labels in tutorials | — |
| UI-58 | 📄 | جولة تمرير مع شروحات · Scroll tour with callouts | SP-0451 Plain action labels in tutorials | — |
| UI-59 | 📄 | خطوط شرح قائدة · Callout leader lines | SP-0451 Plain action labels in tutorials | — |
| UI-78 | 📄 | فيديو تعليمي من ملف YAML · YAML-defined tutorial video | SP-0451 Plain action labels in tutorials | docker |
| UI-25 | 🟢 | كتابة بإيقاع بشري · Human-rhythm typing with caret | SP-0452 Terminal & IDE scenes (24 theme blocks) | — |
| UI-81 | 🟢 | معمارية الثيمات: الشكل × الوضع × العلامة · Look × theme × brand token architecture | SP-0452 Terminal & IDE scenes (24 theme blocks) | — |
| UI-29 | 📦 | طرفية ومحرر كود · Terminal & IDE scenes (24 theme blocks) | SP-0452 Terminal & IDE scenes (24 theme blocks) | npm:hyperframes, os:macos |
| UI-32 | 📦 | كتابة في تطبيق الملاحظات · Notes-app typing story | SP-0452 Terminal & IDE scenes (24 theme blocks) | npm:hyperframes |
| UI-36 | 📦 | قلب المفتاح وتبديل الثيم · Toggle flip & theme switch | SP-0452 Terminal & IDE scenes (24 theme blocks) | npm:hyperframes |
| UI-30 | 👁 | لوحة أوامر وبحث يصفّي النتائج · Command palette & search filter | SP-0452 Terminal & IDE scenes (24 theme blocks) | — |
| UI-85 | 📄 | مخططات مشاهد الواجهة · UI scene blueprints | SP-0452 Terminal & IDE scenes (24 theme blocks) | — |
| UI-44 | ✅ | شريط المراحل والحلقة والتقدم · Stepper, progress ring & progress bars | SP-0453 Spinner → success check | — |
| UI-28 | 📦 | محادثة: فقاعات وكتابة جارية · Chat thread, bubbles & typing dots | SP-0453 Spinner → success check | npm:hyperframes |
| UI-37 | 📦 | من التحميل إلى علامة صح · Spinner → success check | SP-0453 Spinner → success check | npm:hyperframes |
| UI-33 | 📄 | جدول ردود الفعل الدقيقة · Micro-feedback timing table | SP-0453 Spinner → success check | — |
| UI-64 | 📄 | عدسة تكبير التفاصيل · Magnifier lens pass | SP-0453 Spinner → success check | — |
| UI-46 | 💡 | لحظة احتفال توقيعية · Signature celebration moment | SP-0453 Spinner → success check | — |
| UI-40 | 📦 | إشعارات: نظام وجزيرة ورصّة · Notifications: native pop, dynamic island, stacks | SP-0454 HyperFrames UI component registry | npm:hyperframes, os:macos |
| UI-84 | 📦 | مكتبة مكوّنات HyperFrames للواجهات · HyperFrames UI component registry | SP-0454 HyperFrames UI component registry | npm:hyperframes |
| UI-68 | 👁 | شبكة بنتو للميزات · Bento feature grid | SP-0454 HyperFrames UI component registry | — |
