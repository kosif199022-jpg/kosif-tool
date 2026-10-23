# البرمجة وبناء التطبيقات — Software & applications

[← الفهرس الدقيق / micro index](README.md) · 692 powers

## الفهرس / contents

- [app-feature-transfer (build)](#app-feature-transfer-build)
- [apps-artifacts (build)](#apps-artifacts-build)
- [atlas-build (build)](#atlas-build-build)
- [atlas-code (code)](#atlas-code-code)
- [code-engineering (code)](#code-engineering-code)
- [ui-product-device (motion)](#ui-product-device-motion)


## app-feature-transfer (build)

chapter: [app-feature-transfer](../powers/app-feature-transfer.md) · card: `usip-library/cards/software/app-feature-transfer.md` · tools: `app-studio` · `app-studio-paint` · `browser-scout` · `caption-lines` · `installer-triage` · `look-pipeline` · `motion-kit-bridge` · `source-scout` …

| ID | | القدرة / power | SP | يحتاج / requires |
|---|---|---|---|---|
| APPX-31 | ✅ | إزالة الضباب · Dehaze (ClearView-style) | SP-0118 Dehaze (ClearView-style) | chromium, pip:numpy, pip:opencv |
| APPX-32 | ✅ | تقليل الضوضاء بمستويات · Tiered noise reduction | SP-0118 Dehaze (ClearView-style) | ffmpeg, chromium, pip:opencv |
| APPX-33 | ✅ | تصحيح المنظور تلقائيًا · Auto keystone / perspective | SP-0118 Dehaze (ClearView-style) | chromium, pip:opencv |
| APPX-34 | ✅ | تصحيح تشوّه العدسة · Lens distortion correction | SP-0118 Dehaze (ClearView-style) | chromium, pip:opencv |
| APPX-35 | ✅ | إزالة الزيغ اللوني · Lateral chromatic aberration removal | SP-0118 Dehaze (ClearView-style) | chromium, pip:opencv |
| APPX-36 | ✅ | توازن الأبيض ومنحنى الدرجات وHSL · White balance + tone curve + HSL | SP-0118 Dehaze (ClearView-style) | ffmpeg, chromium, pip:numpy, pip:opencv |
| APPX-37 | ✅ | حبيبات فيلم وتعتيم أطراف · Film grain + vignette | SP-0118 Dehaze (ClearView-style) | ffmpeg, chromium, pip:numpy, pip:opencv |
| APPX-38 | ✅ | علامة مائية بشفافية دقيقة · Watermark with exact opacity | SP-0118 Dehaze (ClearView-style) | ffmpeg, pip:pillow |
| APPX-39 | ✅ | ضغط JPEG إدراكي · Perceptual JPEG recompression (JPEGmini-style) | SP-0118 Dehaze (ClearView-style) | chromium, pip:pillow, pip:opencv |
| APPX-40 | ✅ | ورقة تواصل وقوالب طباعة · Contact sheet / print templates | SP-0118 Dehaze (ClearView-style) | pip:pillow |
| APPX-41 | ✅ | ملفات إعدادات مسبقة بإصدارات · Versioned preset / style files | SP-0118 Dehaze (ClearView-style) | python3 |
| APPX-42 | ✅ | ملف XMP جانبي: تقييم ووسوم · XMP sidecar: rating, label, keywords | SP-0118 Dehaze (ClearView-style) | python3 |
| APPX-43 | ✅ | تعديل الأفق تلقائيًا · Auto horizon straighten | SP-0118 Dehaze (ClearView-style) | chromium, pip:opencv |
| APPX-50 | ✅ | دمج التعريضات والتحكم بالدرجات · Exposure fusion / selective tonal control | SP-0118 Dehaze (ClearView-style) | chromium, pip:opencv |
| APPX-61 | ✅ | توضيح الحدة · Unsharp-mask sharpening | SP-0118 Dehaze (ClearView-style) | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-62 | ✅ | الوضوح والملمس · Clarity / texture (local contrast) | SP-0118 Dehaze (ClearView-style) | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-63 | ✅ | تحكم لوني لكل نطاق · HSL per colour band | SP-0118 Dehaze (ClearView-style) | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-64 | ✅ | أبيض وأسود بخلط القنوات · Black & white channel mixer | SP-0118 Dehaze (ClearView-style) | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-65 | ✅ | تلوين الظلال والإضاءات · Split toning / colour grading | SP-0118 Dehaze (ClearView-style) | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-66 | ✅ | إزالة احمرار العين · Red-eye removal | SP-0118 Dehaze (ClearView-style) | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-67 | ✅ | إزالة عنصر وترميم · Object removal / heal | SP-0118 Dehaze (ClearView-style) | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-68 | ✅ | إزالة التموج (مواريه) · Moiré removal | SP-0118 Dehaze (ClearView-style) | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-69 | ✅ | تأثير المجسم · Tilt-shift miniature | SP-0118 Dehaze (ClearView-style) | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-70 | ✅ | تغبيش الخلفية · Background blur (portrait) | SP-0118 Dehaze (ClearView-style) | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-71 | ✅ | قص بنسبة ذكي · Aspect crop with subject focus | SP-0118 Dehaze (ClearView-style) | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-72 | ✅ | تغيير المقاس · Resize for export | SP-0118 Dehaze (ClearView-style) | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-73 | ✅ | ضبط تلقائي للإضاءة · Auto tone / levels | SP-0118 Dehaze (ClearView-style) | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-120 | 📄 | عقد الأمانة للتصميم بقائمة انحرافات مغلقة · Design fidelity contract with a closed deviation list | SP-0119 Parity first, adaptation second | — |
| APPX-121 | 📄 | التطابق أولًا ثم التكييف · Parity first, adaptation second | SP-0119 Parity first, adaptation second | — |
| APPX-122 | 📄 | حلقة التحقق البصري للواجهة مقابل المرجع · Visual verification loop for UI against a reference | SP-0119 Parity first, adaptation second | chromium, pip:pillow |
| APPX-123 | 📄 | استيراد واجهة من مستودع بقراءة أساس التصميم أولًا · Import UI from a repository by reading its design foundation first | SP-0119 Parity first, adaptation second | python3, git |
| APPX-124 | 📄 | الثيم كبيانات قابلة للنقل مع حقل نية المصمم · Theme as portable data with a designer-intent field | SP-0119 Parity first, adaptation second | — |
| APPX-125 | 📄 | قواعد افتراضية لإطارات الواجهات التفاعلية · Default rules for authored interactive UI frames | SP-0119 Parity first, adaptation second | — |
| APPX-126 | 📄 | التصميم مواصفة الشكل والمكوّن القديم مواصفة السلوك · Design is the look spec; the old component is the behaviour spec | SP-0119 Parity first, adaptation second | — |
| APPX-127 | 📄 | عقد أوامر مريح للوكيل · Agent-friendly command contract (JSON, non-interactive, dry-run, explicit states) | SP-0119 Parity first, adaptation second | python3 |
| APPX-128 | 📄 | فحص تمهيدي أولًا للحساب والسياق · Preflight probe first: auth, context and version as one JSON | SP-0119 Parity first, adaptation second | python3 |
| APPX-129 | 📄 | لوحة بصرية دائمة بجانب الوكيل · Persistent visual board beside the agent | SP-0119 Parity first, adaptation second | — |
| APPX-130 | 📄 | جلسة عمل بمرحلتين مع خط أساس وقائمة ملفات مسموحة · Two-phase work session with a baseline manifest and an editable-file allowlist | SP-0119 Parity first, adaptation second | python3 |
| APPX-131 | 📄 | تثبيت النسخة التي يراها المستخدم بالضبط · Pin exactly the version the user is looking at | SP-0119 Parity first, adaptation second | python3 |
| APPX-132 | 📄 | حزمة مراجع من التحديد تُعطى لكل العمّال · Selection-as-context reference bundle shared by every worker | SP-0119 Parity first, adaptation second | — |
| APPX-133 | 📄 | تنويعات على محاور مسمّاة جنبًا إلى جنب · Variant fan-out on named axes, side by side, never overwriting | SP-0119 Parity first, adaptation second | python3 |
| APPX-134 | 📄 | التعديل الحتمي أولًا والنموذج للباقي فقط · Deterministic-first edits; the model only for what cannot be rewritten safely | SP-0119 Parity first, adaptation second | python3 |
| APPX-135 | 📄 | نُسخ مرتبطة: نمط مشترك ومحتوى لكل سجل · Linked instances: shared style, per-record content | SP-0119 Parity first, adaptation second | — |
| APPX-136 | 📄 | نسخ لكل عنصر وارجع للخلف بدل مواصلة التلقين · Per-item revisions: roll back instead of piling on prompts | SP-0119 Parity first, adaptation second | python3 |
| APPX-137 | 📄 | الرسم التقريبي الموسوم للبنية والمرجع للمظهر · Labeled rough sketch for structure; reference for look | SP-0119 Parity first, adaptation second | python3 |
| APPX-138 | 📄 | جسر MCP باتجاهين مع تلميح التحديد الحالي · Two-way MCP bridge with a current-selection hint | SP-0119 Parity first, adaptation second | python3 |
| APPX-139 | 📄 | المهارات: تحميل بالوصف وتثبيت صريح واستيراد نصي آمن · Skills: description-matched loading, explicit pinning, safe text-only import | SP-0119 Parity first, adaptation second | python3 |
| APPX-24 | ✅ | تقوية Electron بالـ fuses · Electron fuse hardening | SP-0120 Minimal context bridge over a MessagePo… | npm:rea |
| APPX-30 | ✅ | فرز المثبّت والتحقق من توقيعه · Installer triage and signature check | SP-0120 Minimal context bridge over a MessagePo… | python3, 7zip |
| APPX-53 | ✅ | ملف لون لكل كاميرا · Per-camera colour profiles | SP-0120 Minimal context bridge over a MessagePo… | pip:pillow |
| APPX-57 | ✅ | كشف حمولات المثبّتات الخفية · Hidden installer payload detection | SP-0120 Minimal context bridge over a MessagePo… | python3, npm:rea, 7zip, innoextract |
| APPX-20 | 📄 | واجهة احتياطية بلا إنترنت · Offline fallback renderer | SP-0120 Minimal context bridge over a MessagePo… | — |
| APPX-21 | 📄 | واجهات RTL مبنية مسبقًا · Prebuilt RTL bundles for Arabic | SP-0120 Minimal context bridge over a MessagePo… | node |
| APPX-22 | 📄 | اقترانات الملفات · File associations for media | SP-0120 Minimal context bridge over a MessagePo… | pip:pillow |
| APPX-23 | 📄 | جسر واحد بقناة MessagePort · Minimal context bridge over a MessagePort | SP-0120 Minimal context bridge over a MessagePo… | — |
| APPX-25 | 📄 | تحديث تلقائي · Auto update channel | SP-0120 Minimal context bridge over a MessagePo… | node |
| APPX-26 | 📄 | تقارير الأعطال · Crash and error reporting | SP-0120 Minimal context bridge over a MessagePo… | node |
| APPX-27 | 📄 | تكامل النظام · OS integration set | SP-0120 Minimal context bridge over a MessagePo… | — |
| APPX-28 | 📄 | مثبّت NSIS ثنائي المعمارية · Dual-architecture NSIS payload | SP-0120 Minimal context bridge over a MessagePo… | python3, 7zip |
| APPX-29 | 📄 | مثبّت تمهيدي عبر الإنترنت · Online bootstrap installer | SP-0120 Minimal context bridge over a MessagePo… | — |
| APPX-51 | 📄 | وحدة مستقلة لكل تصحيح · One plugin assembly per correction | SP-0120 Minimal context bridge over a MessagePo… | npm:rea |
| APPX-52 | 📄 | سلسلة توافق للإعدادات القديمة · Settings compatibility chain | SP-0120 Minimal context bridge over a MessagePo… | — |
| APPX-54 | 📄 | فرش التعديل المحلي كإعدادات · Local-adjustment brushes as presets | SP-0120 Minimal context bridge over a MessagePo… | pip:numpy, pip:opencv |
| APPX-55 | 📄 | حزمة هندسة الخطوط · Font engineering stack | SP-0120 Minimal context bridge over a MessagePo… | pip:fonttools |
| APPX-56 | 📄 | أصول إجرائية بمعاملات · Procedural digital assets | SP-0120 Minimal context bridge over a MessagePo… | blender, npm:three |
| APPX-58 | 📄 | خط تصدير الرسوم المتحركة · Animation export pipeline | SP-0120 Minimal context bridge over a MessagePo… | npm:three, npm:gsap, npm:lottie |
| APPX-140 | ✅ | سطور ترجمة بقواعد قراءة · Caption lines with reading rules | SP-0121 Offline Arabic speech stack | pip:faster-whisper |
| APPX-141 | ✅ | تنقية هلوسة نموذج التفريغ · Screen speech-model inventions | SP-0121 Offline Arabic speech stack | pip:faster-whisper |
| APPX-142 | ✅ | لوك ألوان واحد لكل المحركات · One colour look for every renderer | SP-0121 Offline Arabic speech stack | ffmpeg, python3 |
| APPX-143 | ✅ | إثبات تطابق المعاينة والتصدير بالقياس · Measured preview/export colour parity | SP-0121 Offline Arabic speech stack | ffmpeg, python3 |
| APPX-144 | 📄 | مسار رئيسي مغناطيسي بانتقالات محسوبة · Magnetic main track with clamped transitions | SP-0121 Offline Arabic speech stack | ffmpeg, python3 |
| APPX-145 | 📄 | أي سرعة صوت بسلسلة atempo · Any audio speed with an atempo chain | SP-0121 Offline Arabic speech stack | ffmpeg |
| APPX-146 | 📄 | خلفية مموهة رخيصة للمقاس العمودي · Cheap blurred background fill | SP-0121 Offline Arabic speech stack | ffmpeg |
| APPX-147 | 📄 | نص عربي مرسوم بوحدات مرجعية · Arabic text raster in reference units | SP-0121 Offline Arabic speech stack | ffmpeg |
| APPX-148 | 📄 | تجهيز الوسائط لمحرر · Media prep for an editor | SP-0121 Offline Arabic speech stack | ffmpeg |
| APPX-149 | 📄 | ترميز بالعتاد مع رجوع للبرمجي · Hardware encoder with software fallback | SP-0121 Offline Arabic speech stack | ffmpeg |
| APPX-150 | 📄 | خادم محلي آمن لأداة مونتاج · A safe local editor server | SP-0121 Offline Arabic speech stack | — |
| APPX-151 | 📄 | تنزيل نماذج موثَّق · Verified model downloads | SP-0121 Offline Arabic speech stack | network |
| APPX-152 | 📄 | تراجع يجمع سحب المنزلقات · Undo that groups slider drags | SP-0121 Offline Arabic speech stack | — |
| APPX-153 | 📄 | اختبار ذاتي داخل المضيف الحقيقي · Self-test inside the real host | SP-0121 Offline Arabic speech stack | — |
| APPX-154 | 📄 | ذاكرة وسائط بالمحتوى واستئناف · Content-addressed media cache with resume | SP-0121 Offline Arabic speech stack | — |
| APPX-155 | 📄 | تفريغ عربي محلي بلا إنترنت · Offline Arabic speech stack | SP-0121 Offline Arabic speech stack | pip:faster-whisper, network |
| APPX-01 | ✅ | منحنى السرعة · Speed curve (ramp) | SP-0122 Beat markers from audio | ffmpeg |
| APPX-02 | ✅ | مفتاح الكروما (الشاشة الخضراء) · Chroma key | SP-0122 Beat markers from audio | ffmpeg |
| APPX-03 | ✅ | إعادة التأطير التلقائي 9:16 · Auto reframe to 9:16 | SP-0122 Beat markers from audio | ffmpeg, pip:numpy, pip:opencv |
| APPX-04 | ✅ | كشف القطعات · Scene edit detection | SP-0122 Beat markers from audio | ffmpeg |
| APPX-05 | ✅ | توحيد علوّ الصوت للسوشيال · Loudness normalisation (-14 LUFS) | SP-0122 Beat markers from audio | ffmpeg |
| APPX-06 | ✅ | لون سينمائي من LUT · Colour look from a .cube LUT | SP-0122 Beat markers from audio | ffmpeg |
| APPX-07 | ✅ | حذف الوقفات والصمت · Pause and silence removal | SP-0122 Beat markers from audio | ffmpeg |
| APPX-08 | ✅ | علامات الإيقاع · Beat markers from audio | SP-0122 Beat markers from audio | pip:numpy |
| APPX-10 | ✅ | تكبير بإطارات مفتاحية · Keyframed punch-in / Ken Burns | SP-0122 Beat markers from audio | ffmpeg |
| APPX-11 | ✅ | خفض الموسيقى تحت الصوت · Auto ducking | SP-0122 Beat markers from audio | ffmpeg |
| APPX-12 | ✅ | تنقية الكلام من الضجيج · Speech noise reduction | SP-0122 Beat markers from audio | ffmpeg |
| APPX-13 | ✅ | ترجمة تلقائية بتوقيت الكلمات · Word-timed auto captions | SP-0122 Beat markers from audio | pip:faster-whisper |
| APPX-15 | ✅ | تصدير EDL ومطابقته · EDL interchange and conform | SP-0122 Beat markers from audio | ffmpeg |
| APPX-16 | ✅ | عكس المقطع وتجميد الإطار · Reverse and freeze frame | SP-0122 Beat markers from audio | ffmpeg |
| APPX-17 | ✅ | اختيار الغلاف تلقائيًا · Automatic cover pick | SP-0122 Beat markers from audio | pip:opencv |
| APPX-09 | ✅ | فقاعة الكاميرا فوق تسجيل الشاشة · Round camera bubble over a screen recording | SP-0123 QR code (verified) | ffmpeg |
| APPX-14 | ✅ | إزالة خلفية صورة · Background removal on a still | SP-0123 QR code (verified) | pip:opencv |
| APPX-88 | ✅ | تصميم من قالب JSON · Template design (JSON → PNG/PDF) | SP-0123 QR code (verified) | pip:numpy, pip:pillow, fonts:arabic, pip:arabic-reshaper |
| APPX-89 | ✅ | تغيير المقاس السحري · Magic Resize to every platform | SP-0123 QR code (verified) | chromium, pip:numpy, pip:opencv |
| APPX-90 | ✅ | تأثير اللونين · Duotone | SP-0123 QR code (verified) | pip:numpy, pip:pillow |
| APPX-91 | ✅ | كولاج وشبكات · Collage and grids | SP-0123 QR code (verified) | pip:pillow |
| APPX-92 | ✅ | موك أب واقعي · Photo mockup | SP-0123 QR code (verified) | chromium, pip:numpy, pip:opencv |
| APPX-93 | ✅ | رمز QR بشعار · QR code (verified) | SP-0123 QR code (verified) | chromium, pip:opencv, pip:segno |
| APPX-94 | ✅ | ألوان الهوية · Brand palette (Brand Kit) | SP-0123 QR code (verified) | chromium, pip:pillow, pip:opencv, npm:axe |
| APPX-95 | ✅ | رسم بياني بالعربية · Charts with Arabic labels | SP-0123 QR code (verified) | pip:matplotlib, pip:arabic-reshaper |
| APPX-96 | ✅ | عرض PowerPoint · Presentation export (PPTX) | SP-0123 QR code (verified) | pip:pillow, pip:office |
| APPX-97 | ✅ | PDF للمطبعة · Print PDF: bleed, crop marks, CMYK | SP-0123 QR code (verified) | pip:pillow |
| APPX-98 | ✅ | نص متحرك · Text animation to GIF/MP4 | SP-0123 QR code (verified) | ffmpeg, pip:numpy, pip:pillow |
| APPX-18 | 📄 | منتقي الشاشة للتسجيل · Display-media picker for screen recording | SP-0123 QR code (verified) | — |
| APPX-19 | 📄 | غرفة تحكم التسجيل · Recording mission-control and overlay windows | SP-0123 QR code (verified) | — |
| APPX-44 | ✅ | بناء خط بتقنين الأزواج · Build a font with kerning | SP-0124 L-system growth | pip:fonttools |
| APPX-45 | ✅ | عمليات بوليانية للأشكال المتجهة · Vector boolean operations | SP-0124 L-system growth | pip:shapely |
| APPX-46 | ✅ | عمليات القنوات للحركة · Motion channel ops (CHOP-style) | SP-0124 L-system growth | pip:numpy |
| APPX-47 | ✅ | مخطط مهام بتخزين مؤقت · Task graph with caching (PDG-style) | SP-0124 L-system growth | python3 |
| APPX-48 | ✅ | تنزيل مجزأ قابل للاستئناف · Segmented, resumable download (IDM-style) | SP-0124 L-system growth | python3 |
| APPX-49 | ✅ | حركة متوسطة وقشرة البصل وورقة رسوم · Eased tween, onion skin, sprite sheet | SP-0124 L-system growth | pip:numpy, pip:pillow |
| APPX-79 | ✅ | تحويل صورة إلى متجه · Bitmap to vector (image trace) | SP-0124 L-system growth | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-80 | ✅ | صور إلى PDF · Images to PDF | SP-0124 L-system growth | pip:pillow |
| APPX-81 | ✅ | نثر عناصر إجرائيًا · Procedural scatter (Poisson disc) | SP-0124 L-system growth | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-82 | ✅ | حقل ضوضاء إجرائي · Fractal noise field | SP-0124 L-system growth | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-83 | ✅ | نمو نباتي وزخرفي · L-system growth | SP-0124 L-system growth | python3 |
| APPX-84 | ✅ | فحص خط · Font inspection | SP-0124 L-system growth | pip:fonttools |
| APPX-85 | ✅ | تقليص خط للويب · Font subsetting | SP-0124 L-system growth | pip:fonttools |
| APPX-86 | ✅ | تصدير Lottie · Lottie JSON export | SP-0124 L-system growth | python3, npm:lottie |
| APPX-87 | ✅ | حل عظمتين (IK) · Two-bone inverse kinematics | SP-0124 L-system growth | python3 |
| APPX-100 | ✅ | تشويهات: التواء وانتفاخ وانعكاس قطبي · Distort: twist, bulge, polar inversion, dents, frosted glass, tile reflection | SP-0125 Oil painting, ink sketch, pencil sketch | pip:numpy, pip:opencv |
| APPX-101 | ✅ | تغبيشات: تقريب ودوران وحركة وسطح · Blurs: zoom, radial, motion, surface, unfocus, fragment, median | SP-0125 Oil painting, ink sketch, pencil sketch | pip:numpy, pip:opencv |
| APPX-102 | ✅ | أسلبة: نقش وحواف وبكسلة وبلورات وتوهج · Stylize: emboss, relief, edge detect, outline, pixelate, crystallize, glow, soften portrait | SP-0125 Oil painting, ink sketch, pencil sketch | pip:numpy, pip:opencv |
| APPX-103 | ✅ | كسيريات جوليا وماندلبروت · Julia and Mandelbrot fractals | SP-0125 Oil painting, ink sketch, pencil sketch | pip:numpy, pip:opencv |
| APPX-104 | ✅ | تعديلات: مستويات وتقليل ألوان وسيبيا وضوضاء · Adjustments: levels, posterize, sepia, invert, auto level, add noise | SP-0125 Oil painting, ink sketch, pencil sketch | pip:numpy, pip:opencv |
| APPX-99 | ✅ | رسم زيتي وحبر ورصاص · Oil painting, ink sketch, pencil sketch | SP-0125 Oil painting, ink sketch, pencil sketch | pip:numpy, pip:opencv |
| APPX-105 | ✅ | أوضاع المزج والطبقات (OpenRaster) · Blend modes (24) and layer stacks → PNG or OpenRaster | SP-0126 Blend modes (24) and layer stacks → PNG… | pip:numpy, pip:pillow, pip:opencv |
| APPX-106 | ✅ | LUT سينمائي: صناعة وتطبيق · Cinematic 3D LUTs: make and apply .cube | SP-0126 Blend modes (24) and layer stacks → PNG… | pip:numpy, pip:opencv |
| APPX-107 | ✅ | استبدال السماء · Sky replacement | SP-0126 Blend modes (24) and layer stacks → PNG… | pip:numpy, pip:opencv |
| APPX-109 | ✅ | تغبيش العدسة بعمق وبوكيه · Lens blur with depth map and polygonal bokeh | SP-0126 Blend modes (24) and layer stacks → PNG… | pip:numpy, pip:opencv |
| APPX-108 | 🟢 | التسييل (Liquify) · Liquify: push, pinch, bloat, twirl | SP-0126 Blend modes (24) and layer stacks → PNG… | pip:numpy, pip:opencv |
| APPX-118 | 📄 | ميزات الذكاء في Photoshop: ما يقابلها · Photoshop AI features and their open counterparts | SP-0126 Blend modes (24) and layer stacks → PNG… | — |
| APPX-110 | ✅ | فرش الرسّام · MS Paint brushes on a canvas | SP-0127 MS Paint brushes on a canvas | pip:numpy, pip:opencv |
| APPX-111 | ✅ | سطل التعبئة · Bucket fill (contiguous or global, with tolerance) | SP-0127 MS Paint brushes on a canvas | pip:numpy, pip:opencv |
| APPX-112 | ✅ | صفحة تلوين من صورة · Coloring-book page from a photo | SP-0127 MS Paint brushes on a canvas | pip:numpy, pip:opencv |
| APPX-113 | ✅ | ملصق بحد أبيض وظل · Sticker: cut-out with white border and soft shadow | SP-0127 MS Paint brushes on a canvas | pip:numpy, pip:pillow, pip:opencv |
| APPX-119 | 📄 | ميزات الذكاء في الرسّام: ما يقابلها · MS Paint AI features and their open counterparts | SP-0127 MS Paint brushes on a canvas | — |
| APPX-74 | ✅ | قراءة بيانات الصورة وGPS · EXIF and GPS reader | SP-0128 Photo catalog + search | pip:pillow |
| APPX-75 | ✅ | كشف المكرر والمتشابه · Duplicate / near-duplicate finder | SP-0128 Photo catalog + search | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-77 | ✅ | إعادة تسمية دفعة · Batch rename by EXIF date | SP-0128 Photo catalog + search | pip:pillow |
| APPX-78 | ✅ | فهرسة المكتبة والبحث · Photo catalog + search | SP-0128 Photo catalog + search | chromium, pip:numpy, pip:pillow, pip:opencv |
| APPX-76 | 📦 | كشف الوجوه · Face detection | SP-0128 Photo catalog + search | pip:opencv, pip:onnxruntime, model:yunet |
| APPX-114 | ✅ | رندر سينمائي بخمسة أساليب · Cinematic Cycles render presets (5 looks) | SP-0129 Live Blender capability inventory | python3, blender |
| APPX-115 | ✅ | حركة كاميرا سينمائية إلى MP4 · Camera moves with 180° motion blur → MP4 | SP-0129 Live Blender capability inventory | ffmpeg, python3, blender |
| APPX-116 | ✅ | تشطيب الفيلم في المركّب · Film finish in the Blender 5 compositor | SP-0129 Live Blender capability inventory | blender |
| APPX-117 | ✅ | جرد قدرات Blender الحي · Live Blender capability inventory | SP-0129 Live Blender capability inventory | python3, blender, npm:rea |
| APPX-59 | 📄 | كاميرا افتراضية من فيديو · Virtual camera from a video file | SP-0130 Vertical swipe video player (Android) | — |
| APPX-60 | 📄 | مشغل فيديو عمودي بالسحب · Vertical swipe video player (Android) | SP-0130 Vertical swipe video player (Android) | — |

## apps-artifacts (build)

chapter: [apps-artifacts](../powers/apps-artifacts.md) · card: `usip-library/cards/software/apps-artifacts.md` · tools: `lesson-integrity` · `mosamem-rea-fusion`

| ID | | القدرة / power | SP | يحتاج / requires |
|---|---|---|---|---|
| APP-04 | ✅ | لوحة RTL بلا مكتبات · Dependency-free RTL dashboard page | SP-0131 Publish a private interactive page (Art… | — |
| APP-05 | ✅ | لقطة شاشة بمقاس الهاتف وفحص الفيض · Phone-viewport screenshot + overflow check | SP-0131 Publish a private interactive page (Art… | node, chromium |
| APP-06 | ✅ | من HTML إلى فيديو · HTML to MP4 renderer (repo tool) | SP-0131 Publish a private interactive page (Art… | node, python3, chromium |
| APP-08 | 📦 | تطبيقات بيانات سريعة · Data apps (streamlit, gradio) | SP-0131 Publish a private interactive page (Art… | python3 |
| APP-22 | 📦 | axe-core: فحص صفحة معروضة وفق قواعد WCAG والإبلاغ · axe-core: Run WCAG checks on a rendered page and report violations | SP-0131 Publish a private interactive page (Art… | chromium, npm:axe |
| APP-23 | 📦 | Pa11y: تدقيق الروابط أو ملفات HTML المحلية لإمكانية · Pa11y: Audit URLs or local HTML for accessibility from the CLI | SP-0131 Publish a private interactive page (Art… | npm:pa11y |
| APP-01 | 🔑 | نشر صفحة تفاعلية خاصة · Publish a private interactive page (Artifact) | SP-0131 Publish a private interactive page (Art… | npm:react, claude:tools |
| APP-02 | 🔑 | قدرات الصفحة أثناء التشغيل · Artifact runtime capabilities | SP-0131 Publish a private interactive page (Art… | key:unspecified |
| APP-03 | 🔑 | صفوف وتعليقات الصفحة · ArtifactData and ArtifactComments tools | SP-0131 Publish a private interactive page (Art… | claude:tools |
| APP-24 | 📄 | تحدٍّ قابل للحل قبل عرضه · Check an interactive challenge is solvable before posing it | SP-0131 Publish a private interactive page (Art… | — |
| APP-25 | 📄 | مقياس 1-2-5 وتعريف بطولين · A 1-2-5 gauge scale and a two-length glossary | SP-0131 Publish a private interactive page (Art… | python3 |
| APP-26 | 📄 | مؤثرات من تسجيلات حقيقية في ملف واحد · One sound sprite cut from real CC0 recordings | SP-0131 Publish a private interactive page (Art… | python3 |
| APP-27 | 📄 | تفضيلات الحركة والعرض وشاشة تحميل فورية · Motion and display preferences and an inline loader | SP-0131 Publish a private interactive page (Art… | npm:three |
| APP-09 | ✅ | واجهة برمجية بـ FastAPI · HTTP APIs with FastAPI (tested in-process) | SP-0132 Build an MCP server (mcp 2.x API) | python3 |
| APP-10 | ✅ | قوالب Jinja2 · Jinja2 templating | SP-0132 Build an MCP server (mcp 2.x API) | python3 |
| APP-11 | ✅ | بناء خادم MCP (الإصدار 2) · Build an MCP server (mcp 2.x API) | SP-0132 Build an MCP server (mcp 2.x API) | python3 |
| APP-07 | 📦 | أُطر الواجهات الحديثة · Modern front-end scaffolds (vite, react, next, svelte, tailwind) | SP-0132 Build an MCP server (mcp 2.x API) | npm:esbuild, npm:react |
| APP-13 | 📦 | خادم ملفات محلي للمعاينة · Local static server for previews | SP-0132 Build an MCP server (mcp 2.x API) | node, python3, chromium, claude:tools |
| APP-20 | 📦 | CadQuery: برمجة قطع صلبة بارامترية وتصديرها STEP أو · CadQuery: Script parametric solid parts and export STEP/STL for 3D printing | SP-0132 Build an MCP server (mcp 2.x API) | pip:cadquery |
| APP-21 | 📦 | OpenSCAD: تحويل نماذج ‎.scad إلى STL أو PNG · OpenSCAD: Render .scad models to STL/PNG headlessly | SP-0132 Build an MCP server (mcp 2.x API) | openscad |
| APP-12 | 🔑 | تطبيقات تستدعي Claude عبر API · Apps that call Claude via the API | SP-0132 Build an MCP server (mcp 2.x API) | node, pip:anthropic, key:unspecified |
| APP-14 | 🔑 | بناء مواقع بالذكاء الاصطناعي (مدفوع) · Hosted website builder (Higgsfield, paid) | SP-0132 Build an MCP server (mcp 2.x API) | pip:higgsfield |
| APP-15 | 📄 | اتجاه التصميم قبل الكود · Design direction before code | SP-0133 Design direction before code | — |
| APP-16 | 📄 | لمسات تجعل الواجهة أفضل · Interface polish numbers | SP-0133 Design direction before code | — |
| APP-17 | 📄 | اعرض ثلاثة خيارات بدل الأسئلة · Show three previews instead of asking | SP-0133 Design direction before code | — |
| APP-18 | 📄 | فصل المنشئ عن الناقد · Separate maker from critic | SP-0133 Design direction before code | chromium, git |
| APP-19 | 📄 | بوابة الإنهاء المرئية · Rendered finish gate | SP-0133 Design direction before code | — |

## atlas-build (build)

chapter: [atlas-build](../powers/atlas-build.md) · card: `usip-library/cards/software/atlas-build.md` · tools: —

| ID | | القدرة / power | SP | يحتاج / requires |
|---|---|---|---|---|
| ABUILD-57 | 📄 | ملعب HTML تفاعلي في ملف واحد: أدوات تحكم ومعاينة حية وprompt جاهز للنسخ · Single-file interactive HTML playground: controls, live preview and a ready-to-copy prompt | SP-0131 Publish a private interactive page (Art… | — |
| ABUILD-28 | 📄 | دليل الحوادث: احتواء وتشخيص واستعادة · Incident runbook: contain, diagnose, recover | SP-0134 Figma to pixel-exact code plan | — |
| ABUILD-29 | 📄 | تصميم المراقبة: الإشارات الذهبية والتنبيهات · Observability design: golden signals and alerts | SP-0134 Figma to pixel-exact code plan | — |
| ABUILD-30 | 📄 | استطلاع البنية وتدقيق التكلفة · Infra reconnaissance and cost audit | SP-0134 Figma to pixel-exact code plan | — |
| ABUILD-31 | 📄 | تصميم مكوّن متاح افتراضيا · Accessible-by-default component pattern design | SP-0134 Figma to pixel-exact code plan | npm:pa11y |
| ABUILD-32 | 📄 | إعداد هوية العلامة مع فحص التباين · Brand palette onboarding with WCAG gate | SP-0134 Figma to pixel-exact code plan | npm:axe |
| ABUILD-33 | 📄 | حسابات الألوان وتخطيط CSS مع التباين · Color and CSS layout math with contrast | SP-0134 Figma to pixel-exact code plan | — |
| ABUILD-34 | 📄 | التصميم عبر قيود مكانية وطباعية صريحة · Design by explicit spatial and type constraints | SP-0134 Figma to pixel-exact code plan | — |
| ABUILD-35 | 📄 | نقد التصميم وتسليم المطورين وتدقيق النظام · Design critique, handoff and system audit | SP-0134 Figma to pixel-exact code plan | — |
| ABUILD-36 | 📄 | اشتقاق وترقية نظام التصميم · Design-system retrofit and derivation workflow | SP-0134 Figma to pixel-exact code plan | — |
| ABUILD-37 | 📄 | رموز التصميم DTCG لكل المنصات · DTCG design tokens multi-platform export | SP-0134 Figma to pixel-exact code plan | npm:react |
| ABUILD-38 | 📄 | تدقيق تصميم الواجهة بالأدلة · Evidence-backed frontend design audit | SP-0134 Figma to pixel-exact code plan | npm:react |
| ABUILD-39 | 📄 | استخراج بصمة التصميم من موقع حي · Extract Design DNA from live website | SP-0134 Figma to pixel-exact code plan | npm:three |
| ABUILD-40 | 📄 | من ملف Figma إلى رموز وأصول وكود · Figma file to tokens, assets and code | SP-0134 Figma to pixel-exact code plan | — |
| ABUILD-41 | 📄 | قراءة Figma عبر MCP أو REST · Figma read via MCP or REST fallback | SP-0134 Figma to pixel-exact code plan | — |
| ABUILD-42 | 📄 | من Figma إلى كود مطابق · Figma to pixel-exact code plan | SP-0134 Figma to pixel-exact code plan | — |
| ABUILD-43 | 📄 | تدقيق أداء الواجهة والاستجابة · Frontend performance and responsive audit | SP-0134 Figma to pixel-exact code plan | — |
| ABUILD-44 | 📄 | اختبار الوصولية بلوحة المفاتيح مباشرة · Live keyboard accessibility test via browser | SP-0134 Figma to pixel-exact code plan | npm:axe |
| ABUILD-45 | 📄 | صفحة هبوط فاخرة بحركة GSAP · Premium landing page with GSAP scroll motion | SP-0134 Figma to pixel-exact code plan | npm:gsap |
| ABUILD-46 | 📄 | حلقة مقارنة لقطة الصفحة بالتصميم · Screenshot-vs-design pixel diff loop | SP-0134 Figma to pixel-exact code plan | python3 |
| ABUILD-47 | 📄 | حلقة مقارنة لقطة الشاشة بالمرجع · Screenshot-vs-reference pixel diff loop | SP-0134 Figma to pixel-exact code plan | — |
| ABUILD-48 | 📄 | معمارية رموز التصميم بثلاث طبقات · Three-tier design token architecture with theming | SP-0134 Figma to pixel-exact code plan | — |
| ABUILD-49 | 📄 | تدقيق إتاحة WCAG 2.2: فحص وإصلاح وتحقق · WCAG 2.2 scan-fix-verify accessibility audit | SP-0134 Figma to pixel-exact code plan | npm:axe |
| ABUILD-50 | 📄 | إصدار نسخة: وسم ونشر وتحقق · Cut a release: tag, GitHub release, verify | SP-0134 Figma to pixel-exact code plan | — |
| ABUILD-52 | 📄 | فرز أعطال الاتصال حسب مجال الخطأ دون تغيير الإعدادات · Fault-domain connectivity triage without touching config | SP-0134 Figma to pixel-exact code plan | — |
| ABUILD-56 | 📄 | إعداد أجهزة الشبكة: تحقق قبل التطبيق، وترجمة بين لهجات المصنعين عبر المفاهيم، وقوالب آمنة · Network device config: validate before applying, translate between vendor dialects through concepts, safe templates | SP-0134 Figma to pixel-exact code plan | — |
| ABUILD-58 | 📄 | تحديد معمارية جهاز إلكتروني قبل أي مخطط: المتطلبات قبل القطع، ووحدة جاهزة أم لوحة مخصصة، وشجرة الطاقة، والتوافق الكهرومغناطيسي · Scope a hardware design before any schematic: requirements before parts, module vs custom PCB, the power tree, EMC posture | SP-0134 Figma to pixel-exact code plan | — |
| ABUILD-59 | 📄 | رحلة بناء موقع أو تحسينه بترتيب ثابت: الرسالة ثم التصميم ثم التحويل، وكل إصلاح فرضية قابلة للاختبار، وملف تتبع يستأنف منه · Website creation or improvement as a fixed-order journey: message, then design, then conversion; every fix a testable hypothesis; a tracker to resume from | SP-0134 Figma to pixel-exact code plan | pip:hypothesis |
| ABUILD-05 | 📄 | مسار توقيع وإصدار تطبيقات الجوال والمكتب · Mobile and desktop release signing pipeline | SP-0135 Throwaway prototype to answer one quest… | os:macos |
| ABUILD-06 | 📄 | نموذج HTML تجريبي يجيب أسئلة مفتوحة · Open-question HTML prototype spike | SP-0135 Throwaway prototype to answer one quest… | — |
| ABUILD-07 | 📄 | تنسيق بناء تطبيق كامل على مراحل · Phased full-stack app build orchestration | SP-0135 Throwaway prototype to answer one quest… | — |
| ABUILD-08 | 📄 | تقييم النموذج مقابل معايير القبول · Prototype evaluation vs acceptance criteria | SP-0135 Throwaway prototype to answer one quest… | chromium |
| ABUILD-09 | 📄 | توليد PWA مع service worker · PWA manifest and service worker generation | SP-0135 Throwaway prototype to answer one quest… | chromium |
| ABUILD-10 | 📄 | هيكلة مشروع SaaS جاهز · SaaS boilerplate scaffold spec | SP-0135 Throwaway prototype to answer one quest… | npm:react |
| ABUILD-11 | 📄 | حالة الاشتراكات وواجهة إدارة الاشتراك · Subscription store state and paywall UI | SP-0135 Throwaway prototype to answer one quest… | — |
| ABUILD-12 | 📄 | نموذج أولي مؤقت للإجابة عن سؤال · Throwaway prototype to answer one question | SP-0135 Throwaway prototype to answer one quest… | — |
| ABUILD-13 | 📄 | بناء موقع Wix هيدلس من وصفات SDK · Wix headless site build from SDK recipes | SP-0135 Throwaway prototype to answer one quest… | chromium, key:unspecified |
| ABUILD-54 | 📄 | تجهيز مستودع جديد أو تحديث قديم بترتيب ثابت للخطوات: الأساس ثم هيكل اللغة ثم CI والمدققات والأسرار والإصدار · Bootstrap a new repository or refresh an old one in a fixed order: foundation, language scaffold, CI, linters, secrets, release | SP-0135 Throwaway prototype to answer one quest… | lean |
| ABUILD-55 | 📄 | اختيار أداة المستودع الأحادي من القياس: اللغات والحجم والألم والحاجة للإحكام، وقائمة ما لا نتبناه الآن · Choose monorepo tooling from measurements: language mix, scale, pain and hermeticity, plus a do-not-adopt-yet list | SP-0135 Throwaway prototype to answer one quest… | node |
| ABUILD-14 | 📄 | حلقة مراجع شجرة الوصولية لتحكم المتصفح · Accessibility-tree ref loop for browser agents | SP-0136 Named-session Playwright CLI with disk… | node, chromium |
| ABUILD-15 | 📄 | استنساخ موقع بأدلة المتصفح · Browser-evidence website clone workflow | SP-0136 Named-session Playwright CLI with disk… | chromium |
| ABUILD-16 | 📄 | تصحيح الصفحات الحية عبر Chrome DevTools MCP · Chrome DevTools MCP debugging of live pages | SP-0136 Named-session Playwright CLI with disk… | chromium |
| ABUILD-17 | 📄 | خط لقطات Playwright داخل حاوية · Containerized Playwright screenshot pipeline | SP-0136 Named-session Playwright CLI with disk… | chromium, docker |
| ABUILD-18 | 📄 | تشغيل متصفحات معزولة عبر بروتوكولاتها · Isolated headless Chrome/Firefox/Safari drivers over native protocols | SP-0136 Named-session Playwright CLI with disk… | chromium |
| ABUILD-19 | 📄 | جلسات Playwright مسماة بمخرجات على القرص · Named-session Playwright CLI with disk artifacts | SP-0136 Named-session Playwright CLI with disk… | node, chromium |
| ABUILD-20 | 📄 | كتابة اختبارات E2E مع فحص الوصولية والأداء · Playwright E2E authoring with lint, a11y and CWV scans | SP-0136 Named-session Playwright CLI with disk… | python3, chromium |
| ABUILD-21 | 📄 | رفع ملف عبر Playwright MCP لحقل مخفي · Playwright MCP hidden file-input upload workaround | SP-0136 Named-session Playwright CLI with disk… | chromium |
| ABUILD-22 | 📄 | إثبات السلوك المعروض بحكم نجح/فشل/معطل · Rendered-behavior proof with pass/fail/blocked verdict | SP-0136 Named-session Playwright CLI with disk… | chromium |
| ABUILD-23 | 📄 | فحص جودة الواجهة بثلاثة عروض · Three-width responsive browser QA report | SP-0136 Named-session Playwright CLI with disk… | network |
| ABUILD-60 | 📄 | إعداد طرق التثبيت لأداة CLI: صيغة Homebrew tap وgo install وcargo install مع كشف اللغة وGoReleaser والقيود الخاصة بالمنصة · Set up installers for a CLI: a Homebrew tap formula plus go install and cargo install support, with language, GoReleaser and platform detection | SP-0136 Named-session Playwright CLI with disk… | os:macos |
| ABUILD-01 | 📄 | تنفيذ خارطة الطريق تلقائياً: مرحلة لكل طلب دمج · Autonomous phase-per-PR roadmap execution loop | SP-0137 Role-squad agent pipeline with stages,… | claude:tools |
| ABUILD-02 | 📄 | مسجل قياس تشغيل بالملاحظة فقط · Observation-only run telemetry recorder | SP-0137 Role-squad agent pipeline with stages,… | — |
| ABUILD-03 | 📄 | خط وكلاء بأدوار ومراحل وأقفال كتابة واستئناف · Role-squad agent pipeline with stages, locks and resume | SP-0137 Role-squad agent pipeline with stages,… | — |
| ABUILD-04 | 📄 | تفكيك المواصفة إلى مهام صغيرة لوكلاء البرمجة · Spec-to-task decomposition for coding agents | SP-0137 Role-squad agent pipeline with stages,… | — |
| ABUILD-51 | 📄 | صياغة التذاكر وأوصاف PR بهيكل ماذا/لماذا/كيف · What/Why/How ticket and PR drafting | SP-0137 Role-squad agent pipeline with stages,… | — |
| ABUILD-53 | 📄 | الإدراك وتقدير الحالة للروبوت: مزامنة الزمن والإطارات أولًا ثم دمج حساسات تغطي أعطال بعضها · Robot perception and state estimation: time and frames first, fuse complementary sensors, fail safe | SP-0137 Role-squad agent pipeline with stages,… | — |
| ABUILD-24 | 📄 | ضبط مجمع الاتصالات وموثوقية قاعدة البيانات · Connection pool sizing and DB reliability playbook | SP-0138 Connection pool sizing and DB reliabili… | — |
| ABUILD-25 | 📄 | نص نسخ احتياطي لقاعدة البيانات مع الاحتفاظ والتشفير · Database backup script with retention and encryption | SP-0138 Connection pool sizing and DB reliabili… | — |
| ABUILD-26 | 📄 | تطور مخططات الأحداث وKafka · Event schema evolution and Kafka platform playbook | SP-0138 Connection pool sizing and DB reliabili… | — |
| ABUILD-27 | 📄 | قواعد Postgres وRedis المُدارة على المنصات · Managed Postgres and Redis on hosting platforms | SP-0138 Connection pool sizing and DB reliabili… | — |

## atlas-code (code)

chapter: [atlas-code](../powers/atlas-code.md) · card: `usip-library/cards/software/atlas-code.md` · tools: `atlas-ledger`

| ID | | القدرة / power | SP | يحتاج / requires |
|---|---|---|---|---|
| ACODE-102 | 📄 | فرز أخطاء API بحسب الدليل وفئة الحالة · Evidence-based API error triage by status class | SP-0044 Generate standalone HTML API docs | — |
| ACODE-116 | 📄 | حزمة تشخيص API منقّحة للدعم · Redacted API diagnostic bundle for support | SP-0044 Generate standalone HTML API docs | — |
| ACODE-246 | 📄 | ترحيل عقد API لدى المزوّد بأدلة الحركة والقراءة المزدوجة · Vendor API contract migration with traffic evidence and dual reads | SP-0044 Generate standalone HTML API docs | — |
| ACODE-25 | 📄 | اختيار وتخزين مفاتيح الـAPI بأمان · Choose and store API credentials safely | SP-0044 Generate standalone HTML API docs | chromium, key:unspecified |
| ACODE-27 | 📄 | اختبار عقود API من جهة المستهلك بـ Pact · Consumer-driven API contract testing with Pact | SP-0044 Generate standalone HTML API docs | — |
| ACODE-28 | 📄 | استخراج عميل API مستقل من تسجيل HAR · Derive standalone API client from HAR recording | SP-0044 Generate standalone HTML API docs | — |
| ACODE-31 | 📄 | إعداد مصادقة API بأقل صلاحيات والتحقق منها · Least-privilege API auth setup and verification | SP-0044 Generate standalone HTML API docs | key:unspecified |
| ACODE-41 | 📄 | عميل API يحترم حدود المعدل مع إعادة محاولة · Rate-limit-aware API client with bounded retry | SP-0044 Generate standalone HTML API docs | — |
| ACODE-42 | 📄 | مبادئ تصميم REST وGraphQL · REST and GraphQL API design principles | SP-0044 Generate standalone HTML API docs | — |
| ACODE-49 | 📄 | غلاف عميل API مُنمّط مع إعادة المحاولة · Typed API client adapter with retries | SP-0044 Generate standalone HTML API docs | — |
| ACODE-51 | 📄 | إعداد مفاتيح API وفحصها بأقل صلاحية · Vendor API credential setup and verification | SP-0044 Generate standalone HTML API docs | key:unspecified |
| ACODE-57 | 📄 | محدد معدل طلبات API مع تراجع أسي · Cost-aware API rate limiter with backoff | SP-0044 Generate standalone HTML API docs | — |
| ACODE-64 | 📄 | ضابط حدود معدل واجهات الموردين · Vendor API rate-limit governor | SP-0044 Generate standalone HTML API docs | — |
| ACODE-99 | 📄 | فرز أخطاء API حسب الحالة ومعرّف التتبع · API error triage by status and trace ID | SP-0044 Generate standalone HTML API docs | — |
| ACODE-121 | 📄 | التحقق من استعادة النسخ الاحتياطي · Backup restore verification and DR rehearsal | SP-0045 GitHub Actions failure triage via gh | — |
| ACODE-123 | 📄 | تصميم تجربة فوضى مع نطاق الضرر وشروط الإيقاف · Chaos experiment design with blast radius and abort criteria | SP-0045 GitHub Actions failure triage via gh | — |
| ACODE-124 | 📄 | حكم فشل CI: منك أو من الفرع الرئيسي أو متقلب · CI failure verdict: yours, trunk-borne or flaky | SP-0045 GitHub Actions failure triage via gh | — |
| ACODE-125 | 📄 | تصميم خط CI: ترتيب وتخزين مؤقت · CI pipeline design: ordering, caching, required checks | SP-0045 GitHub Actions failure triage via gh | — |
| ACODE-126 | 📄 | النشر على المنصات السحابية عبر Blueprint أو Wrangler · Cloud platform deploy via Blueprint or Wrangler | SP-0045 GitHub Actions failure triage via gh | — |
| ACODE-127 | 📄 | تشخيص أعطال السحابة بفحص الصحة أولا · Cloud service triage via health-first diagnosis flow | SP-0045 GitHub Actions failure triage via gh | — |
| ACODE-128 | 📄 | تدقيق الحاويات وبودمان المتداخل · Container best-practice audit and rootless nesting | SP-0045 GitHub Actions failure triage via gh | docker |
| ACODE-129 | 📄 | أنماط Bash وzsh الدفاعية · Defensive Bash and zsh scripting conventions | SP-0045 GitHub Actions failure triage via gh | — |
| ACODE-130 | 📄 | بوابة CI آمنة بلا أسرار للتكاملات · Fail-closed credential-free CI gate for integrations | SP-0045 GitHub Actions failure triage via gh | — |
| ACODE-131 | 📄 | مسار نشر Azure بثلاث بوابات · Gated Azure prepare-validate-deploy workflow | SP-0045 GitHub Actions failure triage via gh | — |
| ACODE-132 | 📄 | حوكمة GCP: التسلسل والشبكة والفوترة · GCP resource hierarchy, networking and billing governance | SP-0045 GitHub Actions failure triage via gh | — |
| ACODE-133 | 📄 | تشخيص فشل GitHub Actions عبر gh · GitHub Actions failure triage via gh | SP-0045 GitHub Actions failure triage via gh | gh |
| ACODE-134 | 📄 | تدقيق هدر تكلفة GitHub Actions · GitHub Actions FinOps waste audit | SP-0045 GitHub Actions failure triage via gh | gh |
| ACODE-135 | 📄 | محسّن تكلفة مشغلات GitHub Actions · GitHub Actions runner-cost optimizer | SP-0045 GitHub Actions failure triage via gh | — |
| ACODE-136 | 📄 | GitHub Actions إلى GCP عبر Workload Identity · GitHub Actions to GCP with Workload Identity Federation | SP-0045 GitHub Actions failure triage via gh | — |
| ACODE-137 | 📄 | تسليم GitOps عبر Argo CD أو Flux · GitOps delivery with Argo CD or Flux | SP-0045 GitHub Actions failure triage via gh | — |
| ACODE-138 | 📄 | بناء حاوية آمنة متعددة المراحل · Hardened multi-stage container build | SP-0045 GitHub Actions failure triage via gh | docker, trivy |
| ACODE-139 | 📄 | استعادة إصدارات Helm والتراجع · Helm release recovery and rollback | SP-0045 GitHub Actions failure triage via gh | — |
| ACODE-140 | 📄 | بوابة CI للتكامل: فحوص بلا اتصال واختبار حي محمي · Integration CI gate: offline fixtures plus guarded live smoke | SP-0045 GitHub Actions failure triage via gh | — |
| ACODE-141 | 📄 | أساس منصة كوبرنتس متعددة المستأجرين · Kubernetes multi-tenant platform baseline | SP-0045 GitHub Actions failure triage via gh | — |
| ACODE-142 | 📄 | فحص ملفات workflow لمشاكل المشغلات الذاتية · Lint workflows for self-hosted runner pitfalls | SP-0045 GitHub Actions failure triage via gh | — |
| ACODE-143 | 📄 | تصميم خط نشر متعدد المراحل ببوابات · Multi-stage deployment pipeline design with gates | SP-0045 GitHub Actions failure triage via gh | — |
| ACODE-144 | 📄 | مصادقة CI بلا كلمات مرور عبر OIDC · Passwordless CI cloud auth via OIDC federation | SP-0045 GitHub Actions failure triage via gh | — |
| ACODE-145 | 📄 | دليل فرز الحوادث والتراجع · Platform incident triage and rollback runbook | SP-0045 GitHub Actions failure triage via gh | — |
| ACODE-146 | 📄 | قائمة نشر وتكامل CI حسب المنصة · Platform-specific deploy and CI integration checklist | SP-0045 GitHub Actions failure triage via gh | — |
| ACODE-148 | 📄 | إثبات عدم وجود مستهلك قبل حذف سر سحابي · Prove no consumer before destroying cloud secret | SP-0045 GitHub Actions failure triage via gh | — |
| ACODE-149 | 📄 | تطبيق Terraform من خطة محفوظة · Saved-plan non-interactive terraform apply | SP-0045 GitHub Actions failure triage via gh | — |
| ACODE-150 | 📄 | قائمة تحصين بيئة serverless · Serverless runtime hardening checklist | SP-0045 GitHub Actions failure triage via gh | — |
| ACODE-152 | 📄 | نشر تكامل مرحلي مع كناري وإيصال تراجع · Staged integration deploy with canary and rollback receipt | SP-0045 GitHub Actions failure triage via gh | — |
| ACODE-153 | 📄 | هدم مرحلي لـ ECS بـ Terraform · Staged Terraform teardown for ECS capacity providers | SP-0045 GitHub Actions failure triage via gh | — |
| ACODE-154 | 📄 | وحدات Terraform وكشف الانحراف · Terraform and IaC module generation with drift checks | SP-0045 GitHub Actions failure triage via gh | — |
| ACODE-155 | 📄 | قواعد Terraform وبوابة سياسة للقراءة فقط · Terraform generation posture rules and read-only policy gate | SP-0045 GitHub Actions failure triage via gh | — |
| ACODE-156 | 📄 | بوابة سياسات خطة Terraform · Terraform plan policy gate (OPA) | SP-0045 GitHub Actions failure triage via gh | — |
| ACODE-157 | 📄 | كتابة workflows لـ GitHub Actions مع تحقق · Verified GitHub Actions workflow authoring | SP-0045 GitHub Actions failure triage via gh | gh |
| ACODE-85 | 📄 | أنماط كتابة DAG في Airflow · Airflow DAG authoring patterns | SP-0045 GitHub Actions failure triage via gh | python3 |
| ACODE-86 | 📄 | تأليف موصل تزايدي بـ Airbyte CDK · Incremental connector authoring (Airbyte CDK) | SP-0045 GitHub Actions failure triage via gh | python3, key:unspecified |
| ACODE-160 | 📄 | تحصين حدود المعدل وإعادة المحاولة · Claude API rate-limit and retry hardening | SP-0046 Webhook receiver with HMAC and idempote… | — |
| ACODE-21 | 📄 | معالجة 429: انتظار وتراجع أسي مع تشويش · 429 handler: Retry-After, backoff, jitter | SP-0046 Webhook receiver with HMAC and idempote… | — |
| ACODE-22 | 📄 | تحويل حالات المهام غير المتزامنة لأحداث · Async job state to durable internal events | SP-0046 Webhook receiver with HMAC and idempote… | — |
| ACODE-23 | 📄 | قائمة صمود الخلفية أمام الاعتماديات · Backend resilience checklist for dependencies | SP-0046 Webhook receiver with HMAC and idempote… | — |
| ACODE-24 | 📄 | أنماط خدمات الواجهة الخلفية بعدة لغات · Backend service patterns: Node, Go, .NET, Django | SP-0046 Webhook receiver with HMAC and idempote… | — |
| ACODE-29 | 📄 | قائمة تحصين نقطة GraphQL · GraphQL endpoint hardening checklist | SP-0046 Webhook receiver with HMAC and idempote… | — |
| ACODE-30 | 📄 | مصادقة JWT مع تدوير التحديث وصلاحيات الأدوار · JWT auth with refresh rotation and RBAC | SP-0046 Webhook receiver with HMAC and idempote… | key:unspecified |
| ACODE-32 | 📄 | استقبال OAuth محلي مع ملفات رموز محمية · Local OAuth callback with 0600 token files | SP-0046 Webhook receiver with HMAC and idempote… | key:unspecified |
| ACODE-33 | 📄 | فوترة بالاستهلاك مع تسجيل غير مكرر · Metered billing with idempotent usage | SP-0046 Webhook receiver with HMAC and idempote… | — |
| ACODE-34 | 📄 | مدفوعات آمنة: دفتر مزدوج وتسوية · Money-safe payments: ledger, idempotency, reconciliation | SP-0046 Webhook receiver with HMAC and idempote… | — |
| ACODE-35 | 📄 | تخطيط نمط OAuth والصلاحيات وتجديد الرموز · OAuth grant, scope and token-refresh planning | SP-0046 Webhook receiver with HMAC and idempote… | key:unspecified |
| ACODE-37 | 📄 | اختيار تدفق OAuth/OIDC حسب نوع العميل · OAuth2/OIDC flow selection by client type | SP-0046 Webhook receiver with HMAC and idempote… | key:unspecified |
| ACODE-38 | 📄 | توليد مواصفة OpenAPI 3.1 واستخراجها من الكود · OpenAPI 3.1 spec generation and discovery | SP-0046 Webhook receiver with HMAC and idempote… | — |
| ACODE-39 | 📄 | تدفقات مصادقة بلا كلمة مرور وJWT · Passwordless, passkey and JWT auth flows | SP-0046 Webhook receiver with HMAC and idempote… | key:unspecified |
| ACODE-40 | 📄 | دليل دمج الدفع والفوترة · Payments and billing integration guide | SP-0046 Webhook receiver with HMAC and idempote… | — |
| ACODE-43 | 📄 | محدد معدل طلبات مشترك مع تراجع أسي · Shared rolling-window rate limiter with backoff | SP-0046 Webhook receiver with HMAC and idempote… | — |
| ACODE-44 | 📄 | خط بناء مورد Express من مواصفة · Spec-driven Express resource build pipeline | SP-0046 Webhook receiver with HMAC and idempote… | node |
| ACODE-46 | 📄 | قوالب SSE والمصادقة والزمن الحقيقي · SSE, auth, SSO and realtime scaffolds | SP-0046 Webhook receiver with HMAC and idempote… | — |
| ACODE-47 | 📄 | قرارات تكامل Stripe والترقية · Stripe integration decisions and upgrades | SP-0046 Webhook receiver with HMAC and idempote… | — |
| ACODE-52 | 📄 | مستقبل ويبهوك موثّق وآمن من التكرار · Verified idempotent webhook receiver | SP-0046 Webhook receiver with HMAC and idempote… | — |
| ACODE-53 | 📄 | مستهلك webhook: توقيع HMAC وإزالة التكرار · Webhook consumer: raw-body HMAC, dedupe, fast ack | SP-0046 Webhook receiver with HMAC and idempote… | — |
| ACODE-54 | 📄 | مستقبل ويب هوك: توقيع وتكرار آمن · Webhook receiver: HMAC, idempotency, replay | SP-0046 Webhook receiver with HMAC and idempote… | — |
| ACODE-55 | 📄 | مستقبل ويبهوك مع توقيع HMAC ومنع التكرار · Webhook receiver with HMAC and idempotency | SP-0046 Webhook receiver with HMAC and idempote… | — |
| ACODE-56 | 📄 | خادم WebSocket بمصادقة وغرف واشتراكات · WebSocket server with handshake auth and rooms | SP-0046 Webhook receiver with HMAC and idempote… | — |
| ACODE-04 | 📄 | كتابة وفحص سكربتات سير عمل متعددة الوكلاء · Author and lint deterministic multi-agent workflow scripts | SP-0047 Worktree fleets for parallel agent phas… | — |
| ACODE-05 | 📄 | مقارنة وكلاء البرمجة في أشجار عمل معزولة · Benchmark Claude Code vs Codex in isolated worktrees | SP-0047 Worktree fleets for parallel agent phas… | python3, git |
| ACODE-06 | 📄 | إعادة هيكلة مرحلية بنقاط حفظ · Checkpointed multi-phase refactor surviving context limits | SP-0047 Worktree fleets for parallel agent phas… | — |
| ACODE-07 | 📄 | مرشحون متنافسون في worktrees ثم دمج الفائز · Competing worktree candidates, judged, one landed | SP-0047 Worktree fleets for parallel agent phas… | git, claude:tools |
| ACODE-08 | 📄 | تنسيق وكلاء أشجار العمل عبر رسائل وإيصالات · Coordinate worktree coding agents via mail and receipts | SP-0047 Worktree fleets for parallel agent phas… | git |
| ACODE-10 | 📄 | أنماط سير عمل دائم: ساجا وDAG · Durable workflow patterns: Temporal sagas and Airflow DAGs | SP-0047 Worktree fleets for parallel agent phas… | python3 |
| ACODE-12 | 📄 | حلقة مهام بوكلاء جدد ومراجعة مرحلتين · Fresh-subagent task loop with two-stage review | SP-0047 Worktree fleets for parallel agent phas… | git, claude:tools |
| ACODE-16 | 📄 | عقد إطلاق وكلاء متوازيين مع فحص مسبق · Parallel agent dispatch contract with worktree preflight | SP-0047 Worktree fleets for parallel agent phas… | git, claude:tools |
| ACODE-165 | 📄 | حالة وتدفق وكلاء LangGraph · LangGraph 1.0 agent state and flow | SP-0047 Worktree fleets for parallel agent phas… | python3 |
| ACODE-17 | 📄 | فحص تمهيدي قبل بدء مهمة · Preflight check before starting an issue | SP-0047 Worktree fleets for parallel agent phas… | git |
| ACODE-18 | 📄 | استعادة سير عمل متوقف دون تكرار · Recover interrupted workflow run without duplicates | SP-0047 Worktree fleets for parallel agent phas… | git, gh |
| ACODE-195 | 📄 | تصنيف نتائج regex قبل الاستبدال الجماعي · Classify regex matches before bulk sweep | SP-0047 Worktree fleets for parallel agent phas… | — |
| ACODE-20 | 📄 | أساطيل أشجار عمل لمراحل وكلاء متوازية · Worktree fleets for parallel agent phases | SP-0047 Worktree fleets for parallel agent phas… | git |
| ACODE-215 | 📄 | مسار من issue إلى PR بأشجار عمل معزولة · Worktree-isolated issue-to-PR flow | SP-0047 Worktree fleets for parallel agent phas… | git, gh |
| ACODE-216 | 📄 | إدارة worktree وتنظيفها بأمان · Worktree lifecycle and safe cleanup | SP-0047 Worktree fleets for parallel agent phas… | git |
| ACODE-221 | 📄 | التحقق من السلوك لا من التفاصيل الداخلية، بأوامر المستودع نفسه · Behaviour-level assertions per layer, with the repo's own commands | SP-0047 Worktree fleets for parallel agent phas… | node |
| ACODE-278 | 📄 | تنظيف مساحة العمل القابل للتراجع: كشف افتراضي وحجر بدل الحذف · Reversible workspace hygiene: detect by default, quarantine instead of delete | SP-0047 Worktree fleets for parallel agent phas… | — |
| ACODE-281 | 📄 | تصحيح وكيل محادثة صوتي أو نصي دورًا بدور، ومحاكاة المحادثات الكاملة كاختبار انحدار · Debug a conversational agent turn by turn, and regression-test whole conversations by simulation | SP-0047 Worktree fleets for parallel agent phas… | — |
| ACODE-282 | 📄 | إصلاح فشل CI آليًا بـClaude Code: سير عمل لمستودع واحد أو قالب مشترك، مع حلقة من الاختبار إلى طلب الدمج · Automated CI-failure fixing with an AI agent: inline or reusable workflow, and the issue-to-PR loop | SP-0047 Worktree fleets for parallel agent phas… | — |
| ACODE-284 | 📄 | العمل الطويل داخل حدود الاستخدام: موجات محدودة، قراءة الاستخدام الحقيقي، وإيقاظ متسلسل · Long agent work inside usage windows: bounded waves, real usage reads, chained wake-ups | SP-0047 Worktree fleets for parallel agent phas… | claude:tools |
| ACODE-286 | 📄 | وكلاء الخلفية في المستودع: مخرجاتهم اقتراحات لا دمج، وأول المرشحين الآمنين · Continuous AI: background repository agents whose output is a proposal, never a merge | SP-0047 Worktree fleets for parallel agent phas… | — |
| ACODE-09 | 📄 | تفويض المهام لوكيل آخر مع بوابة مراجعة · Delegate to Codex or Claude with review gate | SP-0048 SystemVerilog review: types, always blo… | git |
| ACODE-186 | 📄 | مراجعة الوصولية وفق WCAG · WCAG four-principle accessibility review | SP-0048 SystemVerilog review: types, always blo… | npm:axe, npm:pa11y |
| ACODE-220 | 📄 | مراجعة أمان للتغيير لا للمستودع كله · Change-scoped security review vs posture audit | SP-0048 SystemVerilog review: types, always blo… | — |
| ACODE-252 | 📄 | إثبات بصري لواجهة طرفية (TUI) عبر PTY حقيقي ومتصفح محلي · Visual proof of a terminal UI through a real PTY and a local browser | SP-0048 SystemVerilog review: types, always blo… | — |
| ACODE-253 | 📄 | مراجعة إعداد Dependabot وفرز طلبات الترقية التي يفتحها · Dependabot config review and upgrade-PR triage | SP-0048 SystemVerilog review: types, always blo… | — |
| ACODE-255 | 📄 | مراجعة المخطط ولوحة PCB قبل التصنيع · Schematic and PCB layout review before fab | SP-0048 SystemVerilog review: types, always blo… | — |
| ACODE-256 | 📄 | تشخيص أعطال توقيع تطبيقات macOS والـentitlements · macOS code-signing and entitlements failure diagnosis | SP-0048 SystemVerilog review: types, always blo… | os:macos |
| ACODE-258 | 📄 | مراجعة كود SystemVerilog: الأنواع وكتل always والقابلية للتوليف · SystemVerilog review: types, always blocks, synthesisability | SP-0048 SystemVerilog review: types, always blo… | — |
| ACODE-262 | 📄 | مراجعة طلبات الدمج التي يكتبها وكيل: المواءمة مع المتطلبات والمراجع الوهمية · Agent-authored PR review: alignment passes and hallucinated references | SP-0048 SystemVerilog review: types, always blo… | — |
| ACODE-263 | 📄 | تصميم سعة المراجعة وبوابات الإصدار لعصر الوكلاء · Review capacity and release gates for agent-speed delivery | SP-0048 SystemVerilog review: types, always blo… | — |
| ACODE-265 | 📄 | جعل كتل check في Terraform تُفشل CI فعلًا · Make Terraform check blocks actually fail CI | SP-0048 SystemVerilog review: types, always blo… | — |
| ACODE-267 | 📄 | تشخيص أي بوابة صلاحيات رفضت الأمر، وخطر توريث قائمة السماح في خدمة · Which permission gate refused, and services that inherit an operator's allow-list | SP-0048 SystemVerilog review: types, always blo… | — |
| ACODE-273 | 📄 | تدقيق الفجوة بين ما يُفترض أن يفعله النظام وما يفعله الكود فعلًا · Intended-vs-implemented gap audit | SP-0048 SystemVerilog review: types, always blo… | — |
| ACODE-274 | 📄 | تثبيت قوائم مراجعة موحّدة يقرؤها Copilot وCodex وClaude عند مراجعة طلبات الدمج · Install shared review checklists for Copilot, Codex and Claude PR reviewers | SP-0048 SystemVerilog review: types, always blo… | — |
| ACODE-275 | 📄 | فرز فحص CI أحمر لمراجعة يقوم بها ذكاء اصطناعي: أربعة أسباب مختلفة · Triage a red AI-review CI check: four causes with opposite responses | SP-0048 SystemVerilog review: types, always blo… | — |
| ACODE-308 | 📄 | مراجعة جاهزية الخطة قبل بدء العمل بأدلة المستودع: تحقق من كل ادعاء عن الحالة الحالية، والعيوب الحقيقية فقط · Plan readiness review against repository evidence before work starts: verify every claim about current state, report real gaps only | SP-0048 SystemVerilog review: types, always blo… | mcp:github |
| ACODE-309 | 📄 | استرجاع عقد إعداد غير موثق من الملف التنفيذي المشحون: strings إلى ملف أولًا، ونص التعليمات ودوال التحقق معًا · Recover an undocumented settings contract from a shipped binary: strings to a file first, and read both the prompt text and the validator bodies | SP-0048 SystemVerilog review: types, always blo… | — |
| ACODE-311 | 📄 | هندسة إضافات Claude Code: تحويل مستودع أوامر وخطافات إلى إضافة، والتوافق مع Codex، والنشر، والتحديث برفع الإصدار، والنسخ الشخصية التي تحجب الحزمة · Claude Code plugin engineering: convert a commands-and-hooks repo, port to Codex, publish, ship updates by bumping the version, and audit personal copies that shadow the bundle | SP-0048 SystemVerilog review: types, always blo… | python3, mcp:github |
| ACODE-88 | 📄 | مراجعة مخطط قاعدة البيانات بعدسات متعددة · Multi-lens database schema review | SP-0048 SystemVerilog review: types, always blo… | lean |
| ACODE-120 | 📄 | كاشف التراجع الصامت من بصمات السجل · Silent-fallback detector from log signatures | SP-0049 Python projects, scripts and tools with… | python3 |
| ACODE-198 | 📄 | إدارة مهام todo.md عبر سكربتات · Markdown todo file task scripts | SP-0049 Python projects, scripts and tools with… | python3 |
| ACODE-223 | 📄 | أداء الويب: الكمون قبل عرض النطاق · Web performance: latency before bandwidth | SP-0049 Python projects, scripts and tools with… | — |
| ACODE-227 | 📄 | ضبط ruff للفحص والتنسيق دون فخ select · ruff lint and format without the select trap | SP-0049 Python projects, scripts and tools with… | python3 |
| ACODE-228 | 📄 | إدارة مشاريع بايثون والسكربتات ببرنامج uv · Python projects, scripts and tools with uv | SP-0049 Python projects, scripts and tools with… | python3 |
| ACODE-316 | 📄 | أداء React وNext.js بالأولوية: اقتل الشلالات والحزمة أولًا، ثم الخادم، ثم إعادة الرسم، ومراجعة بنمط diff أو كامل مع ESLint كحقيقة أرضية · React and Next.js performance by impact: kill waterfalls and bundle bloat first, then server work, then re-renders; review in diff or full mode with ESLint as ground truth | SP-0049 Python projects, scripts and tools with… | git, npm:react |
| ACODE-318 | 📄 | Next.js App Router (حتى v16): اكتشف الراوتر والنسخة وcacheComponents قبل الكتابة، مكونات خادم افتراضيًا، 'use client' عند الحد فقط، و'use cache' بدل خيارات fetch · Next.js App Router up to v16: detect router, version and cacheComponents before writing; Server Components by default, 'use client' only at the boundary, 'use cache' instead of fetch options | SP-0049 Python projects, scripts and tools with… | npm:react |
| ACODE-319 | 📄 | اكتب بلغة المشروع حسب ملفات أدواته: اقرأ go.mod وpyproject وCargo.toml وtsconfig وcsproj والـCI قبل أي API مقيدة بنسخة، ثم افتراضيات كل لغة، و'تم' فقط بعد الفحوص أو بتسمية ما لم يعمل · Write each language from its toolchain files: read go.mod, pyproject, Cargo.toml, tsconfig, csproj and CI before any version-gated API, then per-language defaults; done only when checks pass or each unrun check is named | SP-0049 Python projects, scripts and tools with… | python3 |
| ACODE-322 | 📄 | صور حاويات حسب اللغة: Go ثابت على scratch مع شهادات CA، وNode متعدد المراحل بذاكرة BuildKit واعتماديات إنتاج فقط، وPython على slim لا Alpine بنسخة واحدة للمرحلتين · Language-specific container images: static Go on scratch with CA certs, multi-stage Node with BuildKit cache and production-only deps, Python on slim not Alpine with one version for both stages | SP-0049 Python projects, scripts and tools with… | docker, pip:numpy, pip:pandas, npm:react |
| ACODE-323 | 📄 | فحوص Python السريعة من Astral وأخواتها: ty كمدقق أنواع تجريبي بنسخة مثبتة، وترحيل mypy إلى ty وblack إلى ruff format بخطاف محلي، وvulture للكود الميت بقائمة سماح · Fast Python checks: ty as a pinned beta type checker, mypy to ty and black to ruff-format migrations with a local pre-commit hook, vulture for dead code with a whitelist | SP-0049 Python projects, scripts and tools with… | python3 |
| ACODE-324 | 📄 | سكربت Python مساعد أصغر ما يمكن مقابل سكربت تسليمي: مكتبة قياسية وبلا تهيئة مشروع للمساعد، وحدود مكتوبة الأنواع تبدأ من object ثم تضيّق · Smallest trustworthy Python helper versus a deliverable script: stdlib and no project scaffolding for helpers, typed boundaries that start from object and narrow | SP-0049 Python projects, scripts and tools with… | python3, os:macos |
| ACODE-325 | 📄 | مديرا الحزم Bun وpnpm: إضافة مثبتة لا تتجاوز ملف القفل، تحديث آمن أو انتقائي، فحص القديم، ونشر npm بمعاينة dry-run وتوقيع provenance، وإعدادات pnpm في pnpm-workspace.yaml · Bun and pnpm package management: pinned adds that do not bypass the lockfile, safe or selective updates, outdated audits, npm publishing with dry-run and provenance, pnpm settings in pnpm-workspace.yaml | SP-0049 Python projects, scripts and tools with… | node |
| ACODE-327 | 📄 | التواريخ في TypeScript بـ Temporal: اختر النوع حسب المعنى، حوّل الطابع الزمني إلى تاريخ مرة واحدة عند الحد وبمنطقة زمنية مسماة، وخزّن نصوص ISO · Dates in TypeScript with Temporal: pick the type by meaning, convert a timestamp to a date once at the boundary in a named zone, store ISO strings | SP-0049 Python projects, scripts and tools with… | — |
| ACODE-329 | 📄 | حارس انجراف نسخ المكتبات: اقرأ النسخة المثبتة من ملف القفل، حمّل المهارات والمراجع التي تشحنها الحزمة نفسها، ولا تثق بالذاكرة في Zod 4 وVite 8 وAstro 7 وAngular 20 وTanStack وtsdown · Library version-drift guard: read the installed version from the lockfile, load the skills and docs the package itself ships, and do not trust memory for Zod 4, Vite 8, Astro 7, Angular 20, TanStack or tsdown | SP-0049 Python projects, scripts and tools with… | npm:esbuild |
| ACODE-83 | 📄 | محلل Python AST يراعي الأسماء المستعارة والنطاق · Python AST analyzer with alias and scope handling | SP-0049 Python projects, scripts and tools with… | python3 |
| ACODE-14 | 📄 | حلقة تجارب ذاتية بمقياس: احتفظ أو تراجع · Metric-driven autonomous experiment loop (keep or reset) | SP-0050 Stacked PRs with gh stack | python3, git |
| ACODE-200 | 📄 | تقسيم التغييرات إلى commits ذرية · Atomic commit splitting by purpose | SP-0050 Stacked PRs with gh stack | git |
| ACODE-201 | 📄 | مراقبة PR حتى يصبح جاهزا للدمج · Babysit PR until green and mergeable | SP-0050 Stacked PRs with gh stack | gh |
| ACODE-202 | 📄 | سجل تغييرات من الكوميتات · Changelog from commits, Keep a Changelog | SP-0050 Stacked PRs with gh stack | git |
| ACODE-203 | 📄 | رسالة commit بصيغة Conventional من التغييرات · Conventional commit from staged diff | SP-0050 Stacked PRs with gh stack | git |
| ACODE-204 | 📄 | خطافات تمنع أوامر git الخطرة · Dangerous git command guardrail hooks | SP-0050 Stacked PRs with gh stack | — |
| ACODE-205 | 📄 | محاكاة تعارضات قائمة الدمج · Merge queue conflict simulation | SP-0050 Stacked PRs with gh stack | git |
| ACODE-206 | 📄 | مراقبة طلب الدمج حتى الدمج · PR babysit loop to merge | SP-0050 Stacked PRs with gh stack | mcp:github |
| ACODE-207 | 📄 | وصف PR من الفروقات وقالب المستودع · PR body from diff using repo template | SP-0050 Stacked PRs with gh stack | git, gh, mcp:github |
| ACODE-208 | 📄 | فتح طلب دمج بوصف واضح · PR creation with reviewer-friendly body | SP-0050 Stacked PRs with gh stack | gh |
| ACODE-210 | 📄 | إصدار نسخة مع سجل التغييرات والوسم · Release cut with changelog and tag | SP-0050 Stacked PRs with gh stack | — |
| ACODE-211 | 📄 | حل تعارضات الدمج وإعادة التأسيس · Resolve rebase and merge conflicts | SP-0050 Stacked PRs with gh stack | git |
| ACODE-212 | 📄 | تقسيم فرع إلى فروع بكوميت واحد · Split branch into one-commit branches | SP-0050 Stacked PRs with gh stack | git |
| ACODE-213 | 📄 | طلبات دمج متراكبة عبر gh stack · Stacked PRs with gh stack | SP-0050 Stacked PRs with gh stack | — |
| ACODE-214 | 📄 | طلبات دمج متراكمة مع Graphite وMergify · Stacked PRs with Graphite or Mergify | SP-0050 Stacked PRs with gh stack | node |
| ACODE-106 | 📄 | مراقبة التكاملات بالمقاييس والسجلات والتتبع · Integration observability: metrics, logs, traces, alerts | SP-0051 OpenTelemetry instrumentation audit: SD… | — |
| ACODE-110 | 📄 | خطة قياس مراقبة منخفضة التعدد · Low-cardinality observability instrumentation plan | SP-0051 OpenTelemetry instrumentation audit: SD… | — |
| ACODE-112 | 📄 | فرضيات مرتبة قابلة للدحض مع قياس موسوم · Ranked falsifiable hypotheses with tagged instrumentation | SP-0051 OpenTelemetry instrumentation audit: SD… | — |
| ACODE-158 | 📄 | تصميم تطبيق Agent SDK وخطافاته · Agent SDK app and hooks design | SP-0051 OpenTelemetry instrumentation audit: SD… | key:openai |
| ACODE-162 | 📄 | رصد تطبيقات الذكاء التوليدي بـ OpenTelemetry · GenAI observability with OpenTelemetry | SP-0051 OpenTelemetry instrumentation audit: SD… | — |
| ACODE-243 | 📄 | قياس صحة تكامل خارجي ونتائجه بمقامات صريحة · Integration observability with explicit denominators | SP-0051 OpenTelemetry instrumentation audit: SD… | — |
| ACODE-249 | 📄 | تدقيق قياس OpenTelemetry: إعداد SDK ونظافة الـspans وانتشار السياق · OpenTelemetry instrumentation audit: SDK setup, span hygiene, propagation | SP-0051 OpenTelemetry instrumentation audit: SD… | — |
| ACODE-250 | 📄 | تدقيق تطبيق ويب تقدمي (PWA) وقائمة الإطلاق الحتمية · PWA audit and deterministic launch checklist | SP-0051 OpenTelemetry instrumentation audit: SD… | chromium |
| ACODE-254 | 📄 | تدقيق أذونات إضافة المتصفح وفق أقل صلاحية وManifest V3 · Browser-extension manifest audit: least privilege and MV3 | SP-0051 OpenTelemetry instrumentation audit: SD… | — |
| ACODE-26 | 📄 | اختيار واجهة Zoom المناسبة · Choose Zoom surface: REST, webhooks, WebSocket, SDK | SP-0051 OpenTelemetry instrumentation audit: SD… | key:unspecified |
| ACODE-260 | 📄 | تدقيق جاهزية الواجهة للتعريب والتدويل والاتجاه من اليمين · i18n readiness audit: hardcoded strings, concatenation, locale formats, RTL | SP-0051 OpenTelemetry instrumentation audit: SD… | — |
| ACODE-266 | 📄 | سجل تدقيق موقّع لكل استدعاء أداة يقوم به الوكيل · Signed, offline-verifiable audit trail for agent tool calls | SP-0051 OpenTelemetry instrumentation audit: SD… | claude:tools |
| ACODE-277 | 📄 | تدقيق طبقات التعليمات كلها: هل طُبّقت القاعدة يومًا؟ وأين تتعارض الطبقات؟ · Cross-layer instruction-stack audit: rule-firing evidence, conflicts, permission bypasses | SP-0051 OpenTelemetry instrumentation audit: SD… | — |
| ACODE-50 | 📄 | طبقة مهايئ مُنمّطة لـ SDK أو REST خارجي · Typed vendor SDK/REST adapter boundary | SP-0051 OpenTelemetry instrumentation audit: SD… | — |
| ACODE-105 | 📄 | دليل حوادث التكامل مع الاحتواء أولاً · Integration incident runbook with containment first | SP-0052 Integration production-readiness pack (… | — |
| ACODE-108 | 📄 | عزل السبب الجذري طبقيًا قبل التعديل · Layered root-cause isolation before editing | SP-0052 Integration production-readiness pack (… | — |
| ACODE-11 | 📄 | حلقة تطوير محلية ببيانات وهمية واختبار حي اختياري · Fixture-first local dev loop with opt-in live test | SP-0052 Integration production-readiness pack (… | key:unspecified |
| ACODE-13 | 📄 | عزل أوامر الوكيل على macOS بـ Seatbelt · macOS Seatbelt confinement for agent commands | SP-0052 Integration production-readiness pack (… | os:macos |
| ACODE-164 | 📄 | تحصين LangChain 1.0 للإنتاج · LangChain 1.0 production hardening | SP-0052 Integration production-readiness pack (… | — |
| ACODE-238 | 📄 | تشخيص أعطال تكامل SaaS المستعصية طبقةً طبقة · Layer-by-layer deep debugging of a stubborn SaaS integration | SP-0052 Integration production-readiness pack (… | — |
| ACODE-241 | 📄 | مراجعة مطبات التكامل المتكررة قبل الإصدار · Recurring integration pitfall audit before release | SP-0052 Integration production-readiness pack (… | — |
| ACODE-242 | 📄 | عزل بيئات التطوير والتجربة والإنتاج في التكامل · Prove dev/staging/production isolation for an integration | SP-0052 Integration production-readiness pack (… | key:unspecified |
| ACODE-244 | 📄 | معمارية مرجعية لتكامل خارجي: بوابة سياسات ومحوّل وتسوية · Reference architecture for a vendor integration: policy gateway, adapter, reconciliation | SP-0052 Integration production-readiness pack (… | — |
| ACODE-245 | 📄 | أنماط موثوقية تكامل خارجي: هوية عمل واحدة لكل إعادة · Integration reliability: one idempotency model for every retry path | SP-0052 Integration production-readiness pack (… | — |
| ACODE-279 | 📄 | لا تعديل بلا دليل على المالك: إثبات سلسلة من يرسم الناتج المرئي قبل إصلاحه · No proof, no edit: prove the owner chain of visible output before fixing it | SP-0052 Integration production-readiness pack (… | — |
| ACODE-303 | 📄 | تنظيف ملفات الإعداد الطبقية: احذف من ملف البيئة ما يطابق الأساس، وأثبت أن الإعداد الفعلي لم يتغير · Deduplicate layered config overlays, and prove the effective config did not change | SP-0052 Integration production-readiness pack (… | — |
| ACODE-60 | 📄 | حزمة جاهزية التكامل للإنتاج · Integration production-readiness pack (hello, CI, observability) | SP-0052 Integration production-readiness pack (… | — |
| ACODE-177 | 📄 | مخطط تسلسل موثق من نقطة دخول الكود · Cited sequence diagram from code entry point | SP-0053 Dead code and dependency hygiene sweep | npm:mermaid |
| ACODE-196 | 📄 | فحص الكود الميت وتنظيف الاستيراد · Dead code and import cleanup scan | SP-0053 Dead code and dependency hygiene sweep | — |
| ACODE-222 | 📄 | قاعدة الاعتماد في البنية النظيفة · Clean Architecture dependency rule | SP-0053 Dead code and dependency hygiene sweep | — |
| ACODE-231 | 📄 | تدقيق كل الترقيات الممكنة بمصفوفة مخاطرة/عائد قبل التطبيق · Upgrade-everything audit with a risk/reward matrix | SP-0053 Dead code and dependency hygiene sweep | — |
| ACODE-237 | 📄 | تثبيت كل أسطح الإصدارات لتقوية سلسلة التوريد · Pin every version surface for supply-chain hardening | SP-0053 Dead code and dependency hygiene sweep | node, python3 |
| ACODE-248 | 📄 | تدقيق التبعيات بأدوات كل منظومة: ثغرات وتأخر إصدارات ورخص وتبعيات غير مستخدمة · Ecosystem-native dependency audit: vulnerabilities, lag, licences, unused deps | SP-0053 Dead code and dependency hygiene sweep | node |
| ACODE-268 | 📄 | تبنّي إصدار رئيسي جديد لبوابة أمان تعتمد عليها · Adopting a new major of a security gate you consume | SP-0053 Dead code and dependency hygiene sweep | — |
| ACODE-74 | 📄 | تدقيق وضغط ملفات تهيئة الوكيل · Agent onboarding file audit and compression | SP-0053 Dead code and dependency hygiene sweep | — |
| ACODE-75 | 📄 | استعلام رسم المعرفة قبل مسح الملفات · Code knowledge graph queries before file scanning | SP-0053 Dead code and dependency hygiene sweep | — |
| ACODE-77 | 📄 | مسح الكود الميت وصحة الاعتماديات · Dead code and dependency hygiene sweep | SP-0053 Dead code and dependency hygiene sweep | — |
| ACODE-78 | 📄 | رسم اعتماديات موثق من ملفات البناء · Dependency graph cited from build manifests | SP-0053 Dead code and dependency hygiene sweep | npm:mermaid |
| ACODE-79 | 📄 | هندسة عكسية وصفية لمواصفات قابلة للتتبع · Descriptive reverse engineering into traceable specs | SP-0053 Dead code and dependency hygiene sweep | — |
| ACODE-80 | 📄 | شرح تغيير أو مسار كود بالأدلة · Explain a change or code path grounded in evidence | SP-0053 Dead code and dependency hygiene sweep | git |
| ACODE-101 | 📄 | تشخيص فشل CI مع تنقيح السجلات · CI failure diagnosis with redacted logs | SP-0054 Adversarial competing-hypothesis debugg… | — |
| ACODE-104 | 📄 | ماسح الإخفاقات الصامتة والأخطاء المبتلعة · Hidden-failure scanner for swallowed errors | SP-0054 Adversarial competing-hypothesis debugg… | — |
| ACODE-107 | 📄 | جلسة تصحيح Kubernetes بحاوية مؤقتة · kubectl debug ephemeral container session | SP-0054 Adversarial competing-hypothesis debugg… | — |
| ACODE-111 | 📄 | إعادة بناء تجمد macOS من تقارير التشخيص · macOS freeze/panic reconstruction from DiagnosticReports | SP-0054 Adversarial competing-hypothesis debugg… | os:macos |
| ACODE-115 | 📄 | حزمة تشخيص مُنقّحة بقائمة سماح · Redacted allowlist-based support debug bundle | SP-0054 Adversarial competing-hypothesis debugg… | — |
| ACODE-118 | 📄 | سير عمل تصحيح مشكلة Sentry · Sentry issue debug-and-fix workflow | SP-0054 Adversarial competing-hypothesis debugg… | — |
| ACODE-197 | 📄 | إضافة رمز تشخيص منظم لمكتبة JS · Diagnostic code catalog entry | SP-0054 Adversarial competing-hypothesis debugg… | — |
| ACODE-320 | 📄 | Go الاصطلاحي والتزامن: الوضوح ثم البساطة ثم الإيجاز، أخطاء مبكرة بلا تداخل، ولكل goroutine مالك وسياق إلغاء ومخرج، وerrgroup للأخطاء المشتركة · Idiomatic Go and concurrency: clarity, then simplicity, then concision; early error returns; every goroutine has an owner, a context and an exit; errgroup for shared errors | SP-0054 Adversarial competing-hypothesis debugg… | — |
| ACODE-328 | 📄 | تحقق من نوع TypeScript دون تثبيت المستودع الضخم: اقرأ رمز الخروج لا غياب الأخطاء، مترجم حقيقي بنسخة المستودع، رسم أنواع مصغر، خيارات tsconfig الأصلية، وثلاث نسخ · Verify a TypeScript fix without installing a huge monorepo: read the exit status, not absent errors; a real compiler at the repo's version; a minimal type graph; the repo's tsconfig options; three variants | SP-0054 Adversarial competing-hypothesis debugg… | node |
| ACODE-84 | 📄 | بحث وإعادة كتابة بنيوية بـ ast-grep · Structural search and rewrite with ast-grep | SP-0054 Adversarial competing-hypothesis debugg… | node |
| ACODE-97 | 📄 | تصحيح تنافسي بفرضيات متعددة ووكلاء · Adversarial competing-hypothesis debugging with agent team | SP-0054 Adversarial competing-hypothesis debugg… | pip:hypothesis |
| ACODE-98 | 📄 | تصحيح عدائي متعدد الوكلاء بفرضيات متنافسة · Adversarial multi-agent competing-hypothesis debugging | SP-0054 Adversarial competing-hypothesis debugg… | — |
| ACODE-159 | 📄 | حكم LLM معايَر ومدقَّق التحيز · Calibrated, bias-audited LLM-as-judge | SP-0055 Calibrated, bias-audited LLM-as-judge | — |
| ACODE-161 | 📄 | حزمة تقييم LLM ثابتة بمجموعة ذهبية · Committed LLM eval suite with goldens | SP-0055 Calibrated, bias-audited LLM-as-judge | python3 |
| ACODE-167 | 📄 | مراقبة LLM وتحليل الإخفاقات · LLM observability and failure triage | SP-0055 Calibrated, bias-audited LLM-as-judge | — |
| ACODE-168 | 📄 | ترحيل مزود LLM إلى Bedrock · Migrate LLM provider SDK to Bedrock | SP-0055 Calibrated, bias-audited LLM-as-judge | key:openai |
| ACODE-169 | 📄 | تفويض متعدد النماذج ورأي ثانٍ · Multi-model delegation and second opinion | SP-0055 Calibrated, bias-audited LLM-as-judge | — |
| ACODE-170 | 📄 | تدقيق ذاكرة الـprompt المؤقتة وإصلاحها · Prompt-cache hit-rate audit and fix | SP-0055 Calibrated, bias-audited LLM-as-judge | — |
| ACODE-172 | 📄 | عقد مخرجات LLM منظمة موثوقة · Reliable structured LLM output contract | SP-0055 Calibrated, bias-audited LLM-as-judge | — |
| ACODE-173 | 📄 | تتابع مزودي LLM عبر Router · Vendor failover waterfall via LiteLLM Router | SP-0055 Calibrated, bias-audited LLM-as-judge | python3 |
| ACODE-261 | 📄 | تقييم استكشافي للواجهة بثلاثة مقيّمين مستقلين ثم توفيق النتائج · Heuristic evaluation with three independent evaluators and reconciliation | SP-0055 Calibrated, bias-audited LLM-as-judge | — |
| ACODE-288 | 📄 | ترقية نقطة تدريب نموذج: أربع بوابات بالترتيب من جودة البيانات إلى الإطلاق التدريجي · Fine-tuned checkpoint promotion: four ordered gates from data quality to canary | SP-0055 Calibrated, bias-audited LLM-as-judge | — |
| ACODE-291 | 📄 | مزوّد مخصص لا يُستدعى أبدًا: التوجيه على اسم النموذج يسبق المزوّد في LiteLLM · A custom LLM provider that never runs: dispatch on the bare model name wins first | SP-0055 Calibrated, bias-audited LLM-as-judge | key:openai |
| ACODE-181 | 📄 | فحص القيم الصلبة واستبدالها برموز · Hardcoded-style scan to design tokens | SP-0056 Zero-downtime expand/contract schema mi… | — |
| ACODE-285 | 📄 | ترحيل منسق سير عمل دائم: جرد البنى ثم فصل التنسيق عن الآثار الجانبية · Migrate a durable-workflow orchestrator: inventory constructs, split orchestration from side effects | SP-0056 Zero-downtime expand/contract schema mi… | — |
| ACODE-301 | 📄 | الانتقال بين أداتين: لا تحذف القديمة إلا بإشارة تشغيل فعلية من الجديدة، ولا تتأخر في حذفها · Tool migration cutover: remove the incumbent only on an operational signal from the replacement, and not too late | SP-0056 Zero-downtime expand/contract schema mi… | — |
| ACODE-326 | 📄 | Deno كبديل متوافق مع npm: تثبيت وتشغيل بلا إعادة كتابة، deno ci بالقفل، ترحيل على درجات قابلة للتراجع، صلاحيات ضيقة، وصناديق Deno المعزولة لتشغيل كود غير موثوق · Deno as an npm-compatible runtime: install and run without rewrites, deno ci from the lock, migration in reversible rungs, narrow permissions, and Deno Sandboxes for untrusted code | SP-0056 Zero-downtime expand/contract schema mi… | node |
| ACODE-87 | 📄 | بوابة أمان لأوامر SQL المدمرة مع تجربة جافة · Destructive-SQL safety gate with dry-run | SP-0056 Zero-downtime expand/contract schema mi… | — |
| ACODE-89 | 📄 | ترقية Prisma من 6 إلى 7 · Prisma 6 to 7 upgrade procedure | SP-0056 Zero-downtime expand/contract schema mi… | node |
| ACODE-91 | 📄 | نموذج بيانات Redis وقائمة التشغيل · Redis data model and ops checklist | SP-0056 Zero-downtime expand/contract schema mi… | — |
| ACODE-92 | 📄 | تصميم مخطط من وصف المجال · Schema design from domain description | SP-0056 Zero-downtime expand/contract schema mi… | — |
| ACODE-93 | 📄 | ربط تطبيق Supabase وتوسيعه · Supabase app wiring and scaling | SP-0056 Zero-downtime expand/contract schema mi… | npm:react |
| ACODE-95 | 📄 | ترحيل مخطط قاعدة البيانات دون توقف · Zero-downtime expand/contract schema migration | SP-0056 Zero-downtime expand/contract schema mi… | — |
| ACODE-96 | 📄 | خطة ترحيل Postgres بلا توقف · Zero-downtime Postgres migration playbook | SP-0056 Zero-downtime expand/contract schema mi… | node |
| ACODE-01 | 📄 | اختبار حدود الحقن وتسليم القرار للبشر · Agent injection boundary and human-handoff tests | SP-0057 Design the agent harness, not just the… | — |
| ACODE-02 | 📄 | فحص أمان مسبق للوكيل بإيصال أخضر/أصفر/أحمر · Agent safety preflight with Green/Yellow/Red receipt | SP-0057 Design the agent harness, not just the… | — |
| ACODE-280 | 📄 | تصميم حزام الوكيل لا موجّهه فقط: عشر طبقات من تجميع الطلب إلى الاسترداد · Design the agent harness, not just the prompt: ten-part blueprint | SP-0057 Design the agent harness, not just the… | — |
| ACODE-290 | 📄 | مضيف مريض واحد أم الأسطول كله؟ وحدة المقياس ونسبة الحد الأقصى إلى المجموع · One sick host or the whole fleet? Get the metric unit and the Maximum-to-Sum ratio | SP-0057 Design the agent harness, not just the… | — |
| ACODE-294 | 📄 | تنفيذ أدوات الوكيل وتركيبها: مهلة محددة، ومهام غير متزامنة بمقبض، وقابلية التكرار الآمن، والتعويض، وسلم التجريد · Agent tool execution and composition: bounded time, async job handles, safe retries, compensation, the abstraction ladder | SP-0057 Design the agent harness, not just the… | claude:tools |
| ACODE-310 | 📄 | تحقق من مهارة أو سوق إضافات مقابل الوثائق الحالية المجلوبة حيًا: المطابقة والحداثة والصلاحية والانحراف عن الأصل · Verify a skill or plugin marketplace against current docs fetched live: conformance, currency, freshness and upstream drift | SP-0057 Design the agent harness, not just the… | — |
| ACODE-312 | 📄 | جعل أي وكيل آخر يحمّل ملفات SKILL.md: قائمة سطر لكل مهارة في التعليمات، وأداة load_skill للنص الكامل، وأولوية مسارات معلنة · Make any other agent host load SKILL.md files: a one-line menu in the system prompt, a load_skill tool for the full body, declared path precedence | SP-0057 Design the agent harness, not just the… | — |
| ACODE-313 | 📄 | البرومبت ككود: ملفات في المستودع، وقوالب بمتغيرات صريحة، ومراجعة بنتائج تقييم قبل وبعد، وتثبيت إصدار النموذج، وطرح تدريجي · Prompts as code: files in the repo, explicit-variable templates, review with before-and-after evals, pinned model versions, staged rollout | SP-0057 Design the agent harness, not just the… | — |
| ACODE-314 | 📄 | تنفيذ هجمات الفريق الأحمر على نظام ذكاء اصطناعي ضمن قواعد اشتباك: حقن مباشر وغير مباشر واستخراج وإساءة استخدام الأدوات · Run red-team attacks on an AI system under rules of engagement: direct and indirect injection, extraction, and tool abuse | SP-0057 Design the agent harness, not just the… | — |
| ACODE-315 | 📄 | تقييم جاهزية المستودع للوكلاء: مدخل واحد معتمد، وأدوار الحزام (حالة العمل، السجل، العقود، التحقق، الأدلة)، وأصغر تحسين تالٍ · Assess a repository's agent harness: one canonical entrypoint, harness roles (work state, ledger, contracts, validation, evidence), and the next smallest improvement | SP-0057 Design the agent harness, not just the… | — |
| ACODE-15 | 📄 | فحوص ما قبل التنفيذ لتصادم الوكلاء المتوازيين · Parallel agent collision pre-flight checks | SP-0058 Godot 4 GDScript architecture patterns | gh |
| ACODE-187 | 📄 | بيفي: ECS وتدفق الحالات وخط الأصول · Bevy ECS, state flow and asset pipeline | SP-0058 Godot 4 GDScript architecture patterns | — |
| ACODE-188 | 📄 | حزمة ألعاب المتصفح وPhaser · Browser game stack, Phaser and web foundations | SP-0058 Godot 4 GDScript architecture patterns | npm:esbuild |
| ACODE-189 | 📄 | فيزياء خطوة ثابتة وكشف تصادم · Fixed-step physics and collision broadphase | SP-0058 Godot 4 GDScript architecture patterns | — |
| ACODE-190 | 📄 | اختيار تمثيل الهندسة وSDF وتحويل الشبكات · Geometry, SDF and mesh-voxel conversion choice | SP-0058 Godot 4 GDScript architecture patterns | — |
| ACODE-191 | 📄 | أنماط معمارية لـ GDScript في Godot 4 · Godot 4 GDScript architecture patterns | SP-0058 Godot 4 GDScript architecture patterns | chromium |
| ACODE-192 | 📄 | فحص محرر Godot الحي عبر سطر الأوامر · Godot live-editor inspection via CLI | SP-0058 Godot 4 GDScript architecture patterns | — |
| ACODE-193 | 📄 | حلقة قياس أداء اللعبة · Measured game performance loop | SP-0058 Godot 4 GDScript architecture patterns | — |
| ACODE-194 | 📄 | وحدة DOTS وأتمتة محركات Unity وUnreal · Unity DOTS ECS and Unreal/Unity automation | SP-0058 Godot 4 GDScript architecture patterns | python3 |
| ACODE-151 | 📄 | خطة نشر مرحلية مع تراجع وفصل الأسرار · Staged deployment plan with rollback and secret separation | SP-0059 Feature flag lifecycle and debt audit | — |
| ACODE-199 | 📄 | مزامنة متتبع الميزات مع TODO · Sync feature tracker with TODO | SP-0059 Feature flag lifecycle and debt audit | — |
| ACODE-247 | 📄 | خريطة دورة حياة تكامل SaaS: من التثبيت إلى الحوادث · SaaS integration lifecycle map: install to incident | SP-0059 Feature flag lifecycle and debt audit | python3 |
| ACODE-270 | 📄 | تدقيق مشروع لعبة libGDX: الإعداد ودورة الشاشات والأصول والرسم · libGDX game project audit: setup, screen lifecycle, assets, rendering | SP-0059 Feature flag lifecycle and debt audit | — |
| ACODE-45 | 📄 | إعداد SPF وDKIM وDMARC بمراحل · SPF, DKIM, DMARC staged rollout | SP-0059 Feature flag lifecycle and debt audit | — |
| ACODE-58 | 📄 | دورة حياة أعلام الميزات وتدقيق الديون · Feature flag lifecycle and debt audit | SP-0059 Feature flag lifecycle and debt audit | — |
| ACODE-59 | 📄 | مقارنة لقطات الذاكرة لكشف التسربات · Heap snapshot diff for web memory leaks | SP-0059 Feature flag lifecycle and debt audit | — |
| ACODE-62 | 📄 | التقاط وفك حركة مرور التطبيق · Mitmproxy app traffic capture and decode | SP-0059 Feature flag lifecycle and debt audit | — |
| ACODE-65 | 📄 | التحقق من توقيع الويب هوك مع منع التكرار · Webhook HMAC verify, dedupe, fast-ack | SP-0059 Feature flag lifecycle and debt audit | — |
| ACODE-178 | 📄 | البحث في مكتبة المكونات بسكربت مساعد · Component library lookup with helper script | SP-0060 React component scaffold with shadcn, T… | node |
| ACODE-179 | 📄 | بوابة جودة التصميم في CI · Design-quality CI gate with SARIF | SP-0060 React component scaffold with shadcn, T… | — |
| ACODE-180 | 📄 | بناء نظام رموز التصميم · Design token system scaffold | SP-0060 React component scaffold with shadcn, T… | npm:react |
| ACODE-182 | 📄 | هيكلة مكون React مع shadcn وTailwind وStorybook · React component scaffold with shadcn, Tailwind, Storybook | SP-0060 React component scaffold with shadcn, T… | npm:react |
| ACODE-183 | 📄 | إعداد shadcn وUnoCSS لتنسيق المكونات · shadcn and UnoCSS component styling setup | SP-0060 React component scaffold with shadcn, T… | npm:react |
| ACODE-184 | 📄 | قواعد تركيب shadcn وTailwind · shadcn/ui and Tailwind composition rules | SP-0060 React component scaffold with shadcn, T… | npm:react |
| ACODE-304 | 📄 | نفاد جدول الملفات على مستوى النظام بسبب عمليات يتيمة: ENFILE أم EMFILE يحدد التشخيص كله · System-wide file table exhaustion from orphaned helper processes: ENFILE vs EMFILE decides the diagnosis | SP-0060 React component scaffold with shadcn, T… | os:macos |
| ACODE-317 | 📄 | صحة مكونات React: عقد المشروع أولًا، الحالة عند مالكها، الاشتقاق أثناء الرسم، Effect فقط لمزامنة نظام خارجي داخل hook مسمى، وref كملاذ أخير · React component correctness: local contract first, state at its owner, derive during render, Effects only to sync an external system inside a named hook, refs as a last resort | SP-0060 React component scaffold with shadcn, T… | npm:react |
| ACODE-330 | 📄 | Vue 3 بخريطة مكونات قبل الكود: Composition API مع script setup وTypeScript، حالة واحدة مصدرية والباقي مشتق، props للأسفل وevents للأعلى، Pinia وVue Router بحراسة واضحة · Vue 3 with a component map before code: Composition API with script setup and TypeScript, one source of truth and derived state, props down and events up, Pinia and Vue Router with clear guards | SP-0060 React component scaffold with shadcn, T… | npm:react |
| ACODE-109 | 📄 | تحليل السجلات للطلبات البطيئة وأنماط الخطأ · Log analysis for slow requests and error patterns | SP-0061 SLO workshop with error budget policy | — |
| ACODE-147 | 📄 | خطة تغيير كوبرنيتس إنتاجية بمعايير SRE · Production Kubernetes change plan with SRE standards | SP-0061 SLO workshop with error budget policy | — |
| ACODE-19 | 📄 | خطافات ميزانية زمنية ناعمة للوكلاء الفرعيين · Soft wall-clock budget hooks for subagents | SP-0061 SLO workshop with error budget policy | claude:tools |
| ACODE-259 | 📄 | تدقيق حالات الواجهة الأربع وحالات الحدود في مكونات React · UI state completeness and edge-case audit for React components | SP-0061 SLO workshop with error budget policy | npm:react |
| ACODE-283 | 📄 | معمارية وكيل صوتي وميزانية الزمن: سلسلة STT→LLM→TTS أم كلام إلى كلام · Voice-agent architecture and latency budget: cascade vs speech-to-speech | SP-0061 SLO workshop with error budget policy | — |
| ACODE-296 | 📄 | واجهة أوامر ودودة للبشر: شكل ثابت للمساعدة والأخطاء، وتلوين يحترم الطرفية، ومقياس من 21 نقطة · Human-friendly CLI: fixed help and error layouts, TTY-aware visuals, a 21-point score | SP-0061 SLO workshop with error budget policy | — |
| ACODE-73 | 📄 | ورشة SLO وسياسة ميزانية الخطأ · SLO workshop with error budget policy | SP-0061 SLO workshop with error budget policy | — |
| ACODE-66 | 📄 | محافظ Circle وUSDC متعدد السلاسل · Circle USDC wallets and cross-chain balance | SP-0062 Typed EVM reads and NFT APIs with viem | node, key:unspecified |
| ACODE-67 | 📄 | قوالب بروتوكولات دي فاي وعقود NFT · DeFi protocol and NFT contract templates | SP-0062 Typed EVM reads and NFT APIs with viem | — |
| ACODE-68 | 📄 | تصميم إرسال معاملات EVM آمن · Safe EVM transaction submission design | SP-0062 Typed EVM reads and NFT APIs with viem | — |
| ACODE-69 | 📄 | اختبار العقود الذكية بهاردهات وفاوندري · Smart contract test suite with Hardhat and Foundry | SP-0062 Typed EVM reads and NFT APIs with viem | node, key:unspecified |
| ACODE-70 | 📄 | تدقيق أمان عقود سوليديتي · Solidity vulnerability audit and secure patterns | SP-0062 Typed EVM reads and NFT APIs with viem | — |
| ACODE-71 | 📄 | تطوير Sui Move وإعداد Solana · Sui Move and Solana network/keypair setup | SP-0062 Typed EVM reads and NFT APIs with viem | — |
| ACODE-72 | 📄 | قراءات EVM مكتوبة وواجهات NFT عبر viem · Typed EVM reads and NFT APIs with viem | SP-0062 Typed EVM reads and NFT APIs with viem | node, key:unspecified |
| ACODE-114 | 📄 | إثبات الإصلاح باختبار أحمر ثم أخضر · Red-green-revert proof for bug fixes | SP-0063 False-green test detection | git |
| ACODE-232 | 📄 | كشف الاختبارات الخضراء الكاذبة · False-green test detection | SP-0063 False-green test detection | — |
| ACODE-233 | 📄 | اختبار في فضاء مصغّر: تفكيك ادعاء التكافؤ قبل التجربة · Reduced-space test: decompose the equivalence claim first | SP-0063 False-green test detection | — |
| ACODE-234 | 📄 | اختبار استكشافي لتطبيق ويب بأدلة إعادة إنتاج كاملة · Exploratory web-app QA with full repro evidence | SP-0063 False-green test detection | chromium |
| ACODE-36 | 📄 | اختبار تكامل يعدّ عدد إصدارات التوكن · OAuth token-mint counting integration test | SP-0063 False-green test detection | key:unspecified |
| ACODE-90 | 📄 | توليد بيانات اختبار وكود ORM · Realistic test data seeding and ORM code generation | SP-0063 False-green test detection | — |
| ACODE-163 | 📄 | خط RAG هجين مع إحالات · Hybrid-search RAG pipeline with citations | SP-0064 Hybrid-search RAG pipeline with citatio… | pip:chromadb |
| ACODE-171 | 📄 | دليل بناء وضبط خط RAG · RAG pipeline build and tuning guide | SP-0064 Hybrid-search RAG pipeline with citatio… | pip:chromadb |
| ACODE-225 | 📄 | jq: نموذج المرشّح لتدفق JSON · jq filter mental model for JSON streams | SP-0064 Hybrid-search RAG pipeline with citatio… | — |
| ACODE-287 | 📄 | تسليم المناوبة: خمسة أقسام إلزامية وتجربة تنبيه قبل خروج المناوب · On-call shift handoff: five mandatory sections and a test alert before sign-off | SP-0064 Hybrid-search RAG pipeline with citatio… | — |
| ACODE-289 | 📄 | خط التوصية والترتيب بست مراحل: مصادر، إثراء، تصفية، تقييم، اختيار، آثار غير متزامنة · Six-stage recommendation and ranking pipeline: source, hydrate, filter, score, select, side effects | SP-0064 Hybrid-search RAG pipeline with citatio… | pip:chromadb |
| ACODE-302 | 📄 | بحث الطرفية السريع: ripgrep وfd للمسح ثم fzf --filter للترتيب الضبابي دون تفاعل · Fast terminal search: ripgrep and fd to scan, then fzf --filter to fuzzy-rank non-interactively | SP-0064 Hybrid-search RAG pipeline with citatio… | — |
| ACODE-174 | 📄 | بناء شجرة هجوم · Attack tree construction | SP-0065 Twilio regulatory bundle provisioning | graphviz, npm:mermaid |
| ACODE-175 | 📄 | وثائق ما قبل الإطلاق للتطبيقات المولدة · Pre-ship documentation set for vibe-coded apps | SP-0065 Twilio regulatory bundle provisioning | — |
| ACODE-176 | 📄 | تجهيز حزم الامتثال لأرقام Twilio · Twilio regulatory bundle provisioning | SP-0065 Twilio regulatory bundle provisioning | — |
| ACODE-257 | 📄 | تطبيقات macOS بـSwiftUI: قياس خفيف بـLogger وتبنّي Liquid Glass بأقل تخصيص · macOS SwiftUI apps: lightweight Logger telemetry and minimal-chrome Liquid Glass | SP-0065 Twilio regulatory bundle provisioning | os:macos |
| ACODE-292 | 📄 | مزامنة متغيرات البيئة إلى launchd تسرّب متغيرات الجلسة: قائمة حظر قبل المزامنة · Login-environment sync to launchd leaks the current session's variables | SP-0065 Twilio regulatory bundle provisioning | os:macos |
| ACODE-48 | 📄 | دليل بناء رسائل وصوت Twilio · Twilio messaging and voice build guide | SP-0065 Twilio regulatory bundle provisioning | — |
| ACODE-185 | 📄 | فاحص وصولية HTML مع بقايا يدوية · Stdlib HTML accessibility linter with manual residue | SP-0066 Pick the linter and formatter stack fro… | npm:axe |
| ACODE-269 | 📄 | ترحيل أدوات الفحص: ESLint/Prettier إلى Biome وflake8/isort إلى ruff · Linter migration: ESLint/Prettier → Biome and flake8/isort → ruff | SP-0066 Pick the linter and formatter stack fro… | npm:react |
| ACODE-300 | 📄 | اختيار طقم المدققات والمنسقات من الملفات الموجودة فعلًا، مع ShellCheck وBiome وClippy · Pick the linter and formatter stack from the files that actually exist, with ShellCheck, Biome and Clippy | SP-0066 Pick the linter and formatter stack fro… | lean |
| ACODE-306 | 📄 | TLS المتبادل بين الخدمات: سلسلة الشهادات والتدوير وتشخيص فشل المصافحة · Mutual TLS between services: certificate hierarchy, rotation and handshake debugging | SP-0066 Pick the linter and formatter stack fro… | — |
| ACODE-307 | 📄 | قِس فجوة التوافق قبل التثبيت: عدّد ما تطلبه الأداة، واقرأ العقد المعلن، وجرّب الأوامر الآمنة فقط · Measure a compatibility gap before installing: enumerate what the tool needs, read the declared contract, probe read-only verbs | SP-0066 Pick the linter and formatter stack fro… | — |
| ACODE-321 | 📄 | Rust اصطلاحي: صمم البيانات قبل الكود، ملكية واستعارة قبل clone، Tokio وSerde بحدود واضحة، وclippy وrustfmt وnextest وllvm-cov كبوابات · Idiomatic Rust: model data before code, ownership and borrowing before clone, Tokio and Serde with clear boundaries, clippy, rustfmt, nextest and llvm-cov as gates | SP-0066 Pick the linter and formatter stack fro… | — |
| ACODE-235 | 📄 | تدقيق الامتثال لـ GDPR انطلاقًا من جرد البيانات الشخصية · GDPR review built on a personal-data inventory | SP-0067 GDPR review built on a personal-data in… | — |
| ACODE-239 | 📄 | دورة حياة البيانات المارّة بخدمة خارجية: تصنيف واحتفاظ وحذف · Data lifecycle governance for data sent through a SaaS vendor | SP-0067 GDPR review built on a personal-data in… | key:video-gen |
| ACODE-240 | 📄 | ربط أدوار المزوّد بصلاحيات التطبيق ومفاتيح الخدمة · Map vendor roles to application RBAC and scoped service keys | SP-0067 GDPR review built on a personal-data in… | — |
| ACODE-251 | 📄 | تجهيز مدخلات منقّحة من البيانات الشخصية قبل إرسالها لخدمة ذكاء اصطناعي خارجية · PII-redacted payload review before sending to an external AI | SP-0067 GDPR review built on a personal-data in… | — |
| ACODE-63 | 📄 | فحص امتثال تطبيق شوبيفاي قبل التقديم · Shopify App Store pre-submission compliance sweep | SP-0067 GDPR review built on a personal-data in… | — |
| ACODE-94 | 📄 | سياسات RLS ومفاتيح Supabase الآمنة · Supabase RLS, auth and key hygiene | SP-0067 GDPR review built on a personal-data in… | — |
| ACODE-166 | 📄 | تخطيط ضبط نماذج اللغة SFT/DPO · LLM fine-tuning job planning (SFT/DPO/GRPO) | SP-0068 Choosing DPO, ORPO, KTO or SimPO for pr… | pip:llama-cpp |
| ACODE-224 | 📄 | قياس التحسين مقابل خط أساس مُلتقط قبل التغيير · Measure improvement against a baseline captured before | SP-0068 Choosing DPO, ORPO, KTO or SimPO for pr… | — |
| ACODE-229 | 📄 | اختيار طريقة مواءمة التفضيلات DPO/ORPO/KTO/SimPO · Choosing DPO, ORPO, KTO or SimPO for preference tuning | SP-0068 Choosing DPO, ORPO, KTO or SimPO for pr… | — |
| ACODE-305 | 📄 | تحسين إعداد CircleCI بدءًا من خط أساس مقاس: الهدر أولًا ثم الذاكرة المؤقتة ثم التوازي الآمن · CircleCI config optimisation from a measured baseline: waste first, then caching, then safe parallelism | SP-0068 Choosing DPO, ORPO, KTO or SimPO for pr… | — |
| ACODE-272 | 📄 | تصميم حزمة تحقق موحدة للمستودع بطبقات وأوامر لكل نوع تغيير · Repository validation harness: layered matrix, one entrypoint, honest fallbacks | SP-0069 Home Assistant configuration validation… | — |
| ACODE-276 | 📄 | التحقق من إعدادات Home Assistant: YAML والأسرار والمفاتيح المكررة · Home Assistant configuration validation: YAML, secrets, duplicate keys | SP-0069 Home Assistant configuration validation… | docker |
| ACODE-295 | 📄 | واجهة أوامر للوكلاء أولًا: مخرجات منظمة كعقد بإصدار، وتحقق عند الحدود، ومقياس من 21 نقطة · Agent-first CLI: structured output as a versioned contract, validation at the boundary, a 21-point score | SP-0069 Home Assistant configuration validation… | — |
| ACODE-331 | 📄 | jq للـ JSON وyq للـ YAML وTOML وXML بدل مفسر عام: أدوات ضيقة الصلاحية يسهل اعتمادها، تمرير القيم بـ --arg، والتحقق من أي تطبيق yq وصيغة الإدخال · jq for JSON and yq for YAML, TOML and XML instead of a general interpreter: narrow tools that are easy to approve, values passed with --arg, and checks for which yq and which input format | SP-0069 Home Assistant configuration validation… | node, python3 |
| ACODE-76 | 📄 | خريطة مشروع مؤرخة مع وصفات التعديل · Dated codebase map with change recipes | SP-0070 Codebase onboarding guide | — |
| ACODE-81 | 📄 | خوارزمية تعديل الكود القديم باختبارات التوصيف · Legacy code change algorithm with characterization tests | SP-0070 Codebase onboarding guide | — |
| ACODE-82 | 📄 | رسم المشروع بوكلاء متوازين وكشف التغيير · Parallel subagent mapping with merkle change detection | SP-0070 Codebase onboarding guide | claude:tools |
| ACODE-100 | 📄 | صيد الأخطاء بمستويات إثبات · Bug hunt with tiered evidence findings | SP-0071 Four-phase reproduce-hypothesize-fix de… | — |
| ACODE-103 | 📄 | تصحيح الأخطاء بأربع مراحل منهجية · Four-phase reproduce-hypothesize-fix debugging | SP-0071 Four-phase reproduce-hypothesize-fix de… | — |
| ACODE-113 | 📄 | حلقة تغذية راجعة قبل الفرضيات · Red-capable feedback loop before hypothesizing | SP-0071 Four-phase reproduce-hypothesize-fix de… | chromium |
| ACODE-117 | 📄 | تصحيح الأخطاء بالسبب الجذري أولاً · Root-cause-first debugging with one hypothesis | SP-0071 Four-phase reproduce-hypothesize-fix de… | git, pip:hypothesis |
| ACODE-122 | 📄 | حلقة إصلاح إخفاقات CI محدودة · Bounded CI failure repair loop | SP-0071 Four-phase reproduce-hypothesize-fix de… | gh |
| ACODE-236 | 📄 | دليل سردي لمستودع غير مألوف للمساهمين الجدد · Narrative codebase guide for newcomers | SP-0074 Codebase map as motion graphics | npm:mermaid |
| ACODE-03 | 📄 | تدقيق سجلات جلسات الوكلاء بحثًا عن أسرار مسرّبة · Audit agent transcripts for leaked credentials | SP-0076 Secrets hygiene | — |
| ACODE-119 | 📄 | فحص الإخفاقات الصامتة في الفروقات · Silent failure scan on git diff | SP-0076 Secrets hygiene | python3, git |
| ACODE-209 | 📄 | إزالة أسرار دُفعت من السجل المستضاف · Purge pushed secrets from hosted history | SP-0076 Secrets hygiene | git, gh |
| ACODE-218 | 📄 | حدود الثقة في الأدوات: الأسرار تُحقن والصلاحيات في الكود · Tool trust boundary: injected secrets, permissions in code | SP-0076 Secrets hygiene | — |
| ACODE-219 | 📄 | منع رفع الأسرار عند الالتزام · Block secrets at commit time | SP-0076 Secrets hygiene | — |
| ACODE-264 | 📄 | تدقيق الأسرار في كل تاريخ git قبل جعل المستودع عامًا، وإعادة التدقيق حين يقدم · Whole-history secret audit before open-sourcing, and stale-audit reruns | SP-0076 Secrets hygiene | gitleaks |
| ACODE-217 | 📄 | تصميم أدوات الوكلاء: المستهلك نموذج لا إنسان · Agent tool design: the consumer is a model | SP-0077 REA MCP tool `goto_address` | claude:tools |
| ACODE-230 | 📄 | تصميم خادم MCP: نموذج النشر ونمط الأدوات قبل الكود · MCP server design: deployment model and tool pattern before code | SP-0077 REA MCP tool `goto_address` | python3, key:unspecified |
| ACODE-293 | 📄 | عقد أداة الوكيل: واجهة تُكتب كأنها prompt، وأخطاء مصنفة تعلّم التعافي، ومخرجات مقتصدة مع ترقيم بالمؤشر · Agent tool contract: interface written as a prompt, classified errors that teach recovery, lean paginated output | SP-0077 REA MCP tool `goto_address` | claude:tools, lean |
| ACODE-297 | 📄 | حزمة MCPB لخادم MCP محلي: ملف التعريف وإعدادات التثبيت والأمان الذي يقع على عاتقك · MCPB bundle for a local MCP server: manifest, install-time config, and the security you own | SP-0077 REA MCP tool `goto_address` | python3 |
| ACODE-298 | 📄 | فحص الإضافات قبل التثبيت وخطة ربط MCP بأقل صلاحية: أنماط هجوم 2026 وقرار ثبّت أو قيّد أو ارفض · Extension vetting before install, and a least-privilege MCP integration plan: 2026 attack patterns and an install/restrict/reject verdict | SP-0077 REA MCP tool `goto_address` | — |
| ACODE-299 | 📄 | نقل إعداد MCP في Claude Code بين الأجهزة: أربعة مفاتيح فقط من ~/.claude.json · Move Claude Code's MCP setup between machines: exactly four keys of ~/.claude.json | SP-0077 REA MCP tool `goto_address` | — |
| ACODE-61 | 📄 | تطبيق MCP بأداة وواجهة · MCP App tool plus UI resource | SP-0077 REA MCP tool `goto_address` | npm:esbuild, npm:react, key:openai |
| ACODE-226 | 📄 | تصميم تطبيقات Apple: اختر المسار أولاً · Apple platform design: choose the track first | SP-0080 Run inspect_macho without launching Hop… | npm:react, os:macos |
| ACODE-271 | 📄 | مراجعة هندسة المنصات: ويب أحادي الصفحة وPWA وموبايل وElectron وTauri · Cross-platform engineering review: SPA, PWA, mobile, Electron, Tauri | SP-0085 Passively inspect one Electron file page | npm:react |

## code-engineering (code)

chapter: [code-engineering](../powers/code-engineering.md) · card: `usip-library/cards/software/code-engineering.md` · tools: `architecture-sizer` · `capability-graph` · `kosif-remote-commander` · `motion-stack` · `package-skill` · `rea-owned-repo-batch` · `repo-map` · `repository-capability-packer`

| ID | | القدرة / power | SP | يحتاج / requires |
|---|---|---|---|---|
| CODE-23 | ✅ | Hypothesis: اختبارات قائمة على الخصائص تولّد مدخلات فاشلة · Hypothesis: Property-based tests that generate and shrink failing inputs | SP-0070 Codebase onboarding guide | pip:hypothesis |
| CODE-24 | ✅ | Pandera: تعريف عقود بيانات لإطارات pandas وPolars وفرضها · Pandera: Declare and enforce schemas on pandas/Polars dataframes (data contracts) | SP-0070 Codebase onboarding guide | pip:pandas, pip:polars, pip:pandera |
| CODE-25 | 🟢 | خريطة مستودع مرتبة بالأهمية · Ranked repository map | SP-0070 Codebase onboarding guide | python3 |
| CODE-17 | 🔑 | مراجعة طلب دمج بفريق وكلاء · PR review fan-out | SP-0070 Codebase onboarding guide | gh, mcp:github |
| CODE-04 | 📄 | دليل التعرّف على مستودع · Codebase onboarding guide | SP-0070 Codebase onboarding guide | git |
| CODE-05 | 📄 | قائمة أثر التغيير · Change-impact checklist | SP-0070 Codebase onboarding guide | — |
| CODE-06 | 📄 | حقائق قبل أول تعديل · Fact-forcing before the first edit | SP-0070 Codebase onboarding guide | — |
| CODE-07 | 📄 | اتبع أسلوب المستودع القائم · Inherit the repo's style | SP-0070 Codebase onboarding guide | — |
| CODE-08 | 📄 | التطوير بالاختبار أولًا · Test-driven development | SP-0070 Codebase onboarding guide | — |
| CODE-10 | 📄 | نقاط تفتيش وخط أساس للانحدار · Checkpoints, regression baselines and pass^k | SP-0070 Codebase onboarding guide | — |
| CODE-16 | 📄 | قائمة مراجعة الكود · Code review checklist | SP-0070 Codebase onboarding guide | — |
| CODE-18 | 📄 | إعادة هيكلة آمنة · Safe refactoring | SP-0070 Codebase onboarding guide | key:graphify |
| CODE-22 | 📄 | نظافة الإيداع وكلمات الحالة · Commit hygiene & status words | SP-0070 Codebase onboarding guide | git |
| CODE-26 | 📄 | تعديلات بكتل بحث واستبدال · Search/replace edit blocks | SP-0070 Codebase onboarding guide | — |
| CODE-09 | 📄 | حلقة التحقق بست مراحل · Six-phase verification loop | SP-0071 Four-phase reproduce-hypothesize-fix de… | ffmpeg, node, git, key:unspecified |
| CODE-11 | 📄 | حلقة التشخيص من الجذر · Root-cause debugging loop | SP-0071 Four-phase reproduce-hypothesize-fix de… | pip:hypothesis |
| CODE-12 | 📄 | إصلاح البناء بأقل فرق · Minimal-diff build fixing | SP-0071 Four-phase reproduce-hypothesize-fix de… | — |
| CODE-13 | 📄 | صيد الأعطال الصامتة · Silent-failure and click-path hunt | SP-0071 Four-phase reproduce-hypothesize-fix de… | — |
| CODE-14 | 📄 | حلقة تحسين أداء مقاسة · Measured optimization loop | SP-0071 Four-phase reproduce-hypothesize-fix de… | — |
| CODE-15 | 📄 | معالجة أخطاء متينة · Resilient error handling | SP-0071 Four-phase reproduce-hypothesize-fix de… | — |
| CODE-03 | ✅ | إثبات حزمة في بيئة معزولة · Prove a package in an isolated venv | SP-0072 Live docs over memory | python3 |
| CODE-01 | 📄 | ابحث قبل أن تبني · Search-first: adopt, extend, compose, build | SP-0072 Live docs over memory | node, python3 |
| CODE-02 | 📄 | الوثائق الحية قبل الذاكرة · Live docs over memory | SP-0072 Live docs over memory | node, claude:tools |
| CODE-19 | 📄 | سجل قرار معماري · Architecture decision record | SP-0072 Live docs over memory | — |
| CODE-20 | 📄 | الحتمي أولًا والنموذج للذيل · Deterministic first, model for the tail | SP-0072 Live docs over memory | — |
| CODE-21 | 📄 | ذاكرة مؤقتة ببصمة المحتوى · Content-hash cache | SP-0072 Live docs over memory | key:graphify |

## ui-product-device (motion)

chapter: [ui-product-device](../powers/ui-product-device.md) · card: `usip-library/cards/software/ui-product-device.md` · tools: `ui-beat`

| ID | | القدرة / power | SP | يحتاج / requires |
|---|---|---|---|---|
| UI-11 | ✅ | مؤشر بفيزياء في motion-kit · motion-kit physics cursor + press + typeOn | SP-0468 Cursor as protagonist | node, chromium |
| UI-X03 | ✅ | تسجيل عرض واجهة بـPlaywright · Playwright UI demo recording (WebM) | SP-0468 Cursor as protagonist | ffmpeg, node, chromium |
| UI-14 | 🟢 | حلقة الضغط والتموج · Press ring & click ripple | SP-0468 Cursor as protagonist | — |
| UI-72 | 🟢 | تسجيل صفحة بخطوات مبرمجة · Scripted page recording (Playwright) | SP-0468 Cursor as protagonist | node, chromium |
| UI-86 | 🟢 | أساليب KOSIF للواجهات · KOSIF UI styles to scaffold | SP-0468 Cursor as protagonist | python3 |
| UI-88 | 🟢 | مراجعة على الإطار: سحب وتحجيم واختصارات · Frame review: drag, resize & Arabic-safe shortcuts | SP-0468 Cursor as protagonist | — |
| UI-17 | 📦 | المؤشر المغناطيسي · Magnetic cursor & magnetic buttons | SP-0468 Cursor as protagonist | npm:hyperframes, lean |
| UI-18 | 📦 | سحب وإفلات · Cursor drag & drop | SP-0468 Cursor as protagonist | npm:hyperframes |
| UI-19 | 📦 | تحديد نص ومستطيل وقائمة يمين · Text select, marquee select & context menu | SP-0468 Cursor as protagonist | npm:hyperframes |
| UI-20 | 📦 | مؤشرات متعاونين بأسمائها · Named multiplayer cursors | SP-0468 Cursor as protagonist | npm:hyperframes |
| UI-21 | 📦 | مؤشر وكيل ذكي · AI agent cursor | SP-0468 Cursor as protagonist | npm:hyperframes |
| UI-22 | 📦 | مؤشر اللمس على الهاتف · Touch indicator: tap & swipe | SP-0468 Cursor as protagonist | npm:hyperframes |
| UI-77 | 📦 | تسجيل المتصفح بمؤشر ولوحة لقطات · Browser recording CLI with cursor & contact sheet | SP-0468 Cursor as protagonist | ffmpeg, node, chromium |
| UI-15 | 👁 | مؤشر ماك معبّر يتجه مع حركته · Expressive directional macOS cursor | SP-0468 Cursor as protagonist | os:macos |
| UI-16 | 👁 | مؤشر بهالة لونية يلاحق هدفًا متحركًا · Cursor with accent halo homing on a live target | SP-0468 Cursor as protagonist | — |
| UI-60 | 👁 | اقتراب يقوده المؤشر · Cursor-led push-in & focus zoom | SP-0468 Cursor as protagonist | — |
| UI-01 | 📄 | العرض الصامت: الواجهة تحكي · Silent product demo — the UI tells the story | SP-0468 Cursor as protagonist | — |
| UI-13 | 📄 | تصميم حركة المؤشر · Cursor choreography rules | SP-0468 Cursor as protagonist | — |
| UI-26 | 📄 | طلب يُكتب ثم يُرسل ثم يولّد · Prompt type → submit → generate | SP-0468 Cursor as protagonist | — |
| UI-35 | 📄 | ضغط وتحرير زر نابض · Press-release spring button | SP-0468 Cursor as protagonist | — |
| UI-61 | 📄 | وصفة النقر وفتح نافذة · Click → modal recipe | SP-0468 Cursor as protagonist | npm:remotion |
| UI-89 | 📄 | قواعد صفحات الويب المسلَّمة · Web deliverable rules (landing, perf, hover gating) | SP-0468 Cursor as protagonist | — |
| UI-X01 | 📄 | المؤشر بطلًا · Cursor as protagonist | SP-0468 Cursor as protagonist | chromium |
| UI-12 | ✅ | واجهة منتج على Canvas بدالة draw(t) · Canvas product UI draw(t) recipe | SP-0469 Canvas 2.5D phone (drawPhone) | node, chromium |
| UI-87 | ✅ | مشغّل HTML مستقل بشريط تقديم · Standalone HTML player with seek & reduced motion | SP-0469 Canvas 2.5D phone (drawPhone) | node |
| UI-50 | 🟢 | هاتف 2.5D على Canvas · Canvas 2.5D phone (drawPhone) | SP-0469 Canvas 2.5D phone (drawPhone) | — |
| UI-56 | 🟢 | موك أب HTML بلقطة 2× · HTML/CSS device & package mockup screenshot | SP-0469 Canvas 2.5D phone (drawPhone) | chromium |
| UI-51 | 📦 | مكوّن Device في Remotion · Remotion Device component | SP-0469 Canvas 2.5D phone (drawPhone) | npm:remotion, npm:react |
| UI-54 | 📦 | مروحة أجهزة وانفراد الهواتف · Multi-device splay & phone fan-out | SP-0469 Canvas 2.5D phone (drawPhone) | npm:hyperframes |
| UI-76 | 🔑 | من فيجما إلى طبقات متحركة · Figma frame → animatable layers | SP-0469 Canvas 2.5D phone (drawPhone) | key:unspecified |
| UI-53 | 👁 | نافذة متصفح أو ماك وهمية · Browser chrome & macOS frame mock | SP-0469 Canvas 2.5D phone (drawPhone) | os:macos |
| UI-71 | 👁 | مسرح أداة تصميم ومقابض تحديد · Design-tool canvas, selection handles & size tags | SP-0469 Canvas 2.5D phone (drawPhone) | — |
| UI-82 | 👁 | ستايل برومو المنتج · Product promo style (neon prompt + glass orb) | SP-0469 Canvas 2.5D phone (drawPhone) | — |
| UI-47 | 📄 | ثوابت الهاتف البارامتري · Parametric phone constants | SP-0469 Canvas 2.5D phone (drawPhone) | — |
| UI-48 | 📄 | منظور الجهاز وسرعة دورانه · Device perspective, rotation caps & idle hover | SP-0469 Canvas 2.5D phone (drawPhone) | — |
| UI-49 | 📄 | دخول الجهاز وكشف البطل · Device entrance & hero reveal | SP-0469 Canvas 2.5D phone (drawPhone) | npm:remotion |
| UI-52 | 📄 | تسليم بين جهازين · Two-device turntable handoff | SP-0469 Canvas 2.5D phone (drawPhone) | — |
| UI-X02 | 📄 | تسليم المجسم وطبقات منفجرة · Mockup hand-off and exploded layers | SP-0469 Canvas 2.5D phone (drawPhone) | — |
| UI-57 | 💡 | قلب الهاتف وتبديل الشاشة · Phone flip with mid-swap | SP-0469 Canvas 2.5D phone (drawPhone) | — |
| UI-04 | 🟢 | إعادة بناء الشاشة كطبقات · Layered screen rebuild | SP-0470 Real, locale-correct UI content | — |
| UI-05 | 🟢 | حقيبة أصول من أجزاء حقيقية · Animation kit from real parts | SP-0470 Real, locale-correct UI content | chromium, pip:pillow |
| UI-43 | 🟢 | مؤشرات التبويب والشريط النشط · Tab slide indicator & active rail bar | SP-0470 Real, locale-correct UI content | — |
| UI-39 | 📦 | هيكل لامع يتحول إلى محتوى · Skeleton shimmer → content | SP-0470 Real, locale-correct UI content | npm:hyperframes |
| UI-X04 | 📦 | رموز الحركة وصقل الواجهة · Motion tokens and interface polish (React UIs) | SP-0470 Real, locale-correct UI content | npm:animejs, npm:react |
| UI-63 | 👁 | جدار بطاقات واجهة يطفو بعمق · Floating UI card wall in depth | SP-0470 Real, locale-correct UI content | — |
| UI-83 | 👁 | واجهة ملصقات بظل صلب · Sticker UI with hard offset shadow | SP-0470 Real, locale-correct UI content | — |
| UI-03 | 📄 | محتوى واجهة حقيقي ومحلي · Real, locale-correct UI content | SP-0470 Real, locale-correct UI content | — |
| UI-06 | 📄 | عكس الواجهة للعربية · RTL product-UI mirroring | SP-0470 Real, locale-correct UI content | — |
| UI-07 | 📄 | لوحة البيانات داخل الإطار · Dashboard composition for a frame | SP-0470 Real, locale-correct UI content | — |
| UI-08 | 📄 | تشريح التفاعل الدقيق كوحدة مشهد · Microinteraction anatomy as a beat | SP-0470 Real, locale-correct UI content | — |
| UI-09 | 📄 | مقطع حلقة لمكوّن واحد · Seamless UI component loop (3–6 s) | SP-0470 Real, locale-correct UI content | — |
| UI-62 | 📄 | صفحة ويب مائلة تتمرر · 3D tilted webpage scroll & perspective pan | SP-0470 Real, locale-correct UI content | npm:gsap |
| UI-75 | 📄 | وصفة فيديو ميزة حقيقية · Real-feature video recipe | SP-0470 Real, locale-correct UI content | ffmpeg, node, chromium |
| UI-79 | 📄 | رموز تصميم الواجهة وسلالمها · UI tokens & Refactoring-UI scales | SP-0470 Real, locale-correct UI content | — |
| UI-80 | ✅ | سطح زجاجي للواجهات · Glass surface stack | SP-0471 Control ↔ target live sync | chromium, npm:hyperframes |
| UI-45 | 🟢 | نقطة حالة بهالة وشارة مباشرة · Status dot with halo & live pill | SP-0471 Control ↔ target live sync | — |
| UI-69 | 🟢 | لوحة قياس HUD وشروح مسقطة من 3D · Instrument-panel HUD & projected callouts | SP-0471 Control ↔ target live sync | — |
| UI-38 | 📦 | حقل إدخال: خطأ واهتزاز ونجاح · Input feedback: error shake & valid state | SP-0471 Control ↔ target live sync | npm:hyperframes |
| UI-41 | 📦 | تحول بطاقة إلى لوحة (FLIP) · Shared-element morph: card → panel (FLIP) | SP-0471 Control ↔ target live sync | npm:hyperframes |
| UI-55 | 📦 | آيفون وماك بوك ثلاثيا الأبعاد بشاشات حية · 3D GLTF iPhone & MacBook with live screens | SP-0471 Control ↔ target live sync | chromium, npm:three, npm:gsap, npm:hyperframes … |
| UI-66 | 📦 | مقارنة قبل وبعد · Before/after wipe & comparison split | SP-0471 Control ↔ target live sync | npm:hyperframes |
| UI-67 | 📦 | دوار الشاشات والموكاب الثابت · Screen-flow carousel & sticky mock swap | SP-0471 Control ↔ target live sync | npm:hyperframes |
| UI-31 | 👁 | إجابة متدفقة وسجل حي · Streaming answer & live log | SP-0471 Control ↔ target live sync | — |
| UI-42 | 👁 | إعادة ترتيب قائمة وسطور · FLIP list reorder & self-reordering lines | SP-0471 Control ↔ target live sync | — |
| UI-70 | 👁 | مربع تتبع وماسح ضوئي · AI tracking box & scanner brackets | SP-0471 Control ↔ target live sync | tesseract |
| UI-24 | 📄 | تحكم وهدف يتغيران معًا · Control ↔ target live sync | SP-0471 Control ↔ target live sync | — |
| UI-34 | 🟢 | ضغط ومرور بمنطق القراءة · Press & hover with reading-direction nudges | SP-0472 Plain action labels in tutorials | — |
| UI-74 | 🟢 | فيلم إطلاق kmotion brag · kmotion brag launch film | SP-0472 Plain action labels in tutorials | python3 |
| UI-73 | 📦 | التقاط موقع إلى فيديو · Website capture → video | SP-0472 Plain action labels in tutorials | chromium, npm:hyperframes, npm:lottie |
| UI-23 | 👁 | ضغط اختصار لوحة المفاتيح · Keycap shortcut trigger | SP-0472 Plain action labels in tutorials | — |
| UI-27 | 👁 | وكيل ينجز قائمة مهام · Agent progress theater & tool-call checklist | SP-0472 Plain action labels in tutorials | npm:hyperframes |
| UI-65 | 👁 | نقطة ساخنة مع فقاعة إرشاد · Hotspot tooltip walkthrough | SP-0472 Plain action labels in tutorials | — |
| UI-02 | 📄 | ثلاثية النية والفعل والاستجابة · Intent → action → response with real latency | SP-0472 Plain action labels in tutorials | — |
| UI-10 | 📄 | عناوين أفعال بسيطة في الشروحات · Plain action labels in tutorials | SP-0472 Plain action labels in tutorials | — |
| UI-58 | 📄 | جولة تمرير مع شروحات · Scroll tour with callouts | SP-0472 Plain action labels in tutorials | — |
| UI-59 | 📄 | خطوط شرح قائدة · Callout leader lines | SP-0472 Plain action labels in tutorials | — |
| UI-78 | 📄 | فيديو تعليمي من ملف YAML · YAML-defined tutorial video | SP-0472 Plain action labels in tutorials | docker |
| UI-25 | 🟢 | كتابة بإيقاع بشري · Human-rhythm typing with caret | SP-0473 Terminal & IDE scenes (24 theme blocks) | — |
| UI-81 | 🟢 | معمارية الثيمات: الشكل × الوضع × العلامة · Look × theme × brand token architecture | SP-0473 Terminal & IDE scenes (24 theme blocks) | — |
| UI-29 | 📦 | طرفية ومحرر كود · Terminal & IDE scenes (24 theme blocks) | SP-0473 Terminal & IDE scenes (24 theme blocks) | npm:hyperframes, os:macos |
| UI-32 | 📦 | كتابة في تطبيق الملاحظات · Notes-app typing story | SP-0473 Terminal & IDE scenes (24 theme blocks) | npm:hyperframes |
| UI-36 | 📦 | قلب المفتاح وتبديل الثيم · Toggle flip & theme switch | SP-0473 Terminal & IDE scenes (24 theme blocks) | npm:hyperframes |
| UI-30 | 👁 | لوحة أوامر وبحث يصفّي النتائج · Command palette & search filter | SP-0473 Terminal & IDE scenes (24 theme blocks) | — |
| UI-85 | 📄 | مخططات مشاهد الواجهة · UI scene blueprints | SP-0473 Terminal & IDE scenes (24 theme blocks) | — |
| UI-44 | ✅ | شريط المراحل والحلقة والتقدم · Stepper, progress ring & progress bars | SP-0474 Spinner → success check | — |
| UI-28 | 📦 | محادثة: فقاعات وكتابة جارية · Chat thread, bubbles & typing dots | SP-0474 Spinner → success check | npm:hyperframes |
| UI-37 | 📦 | من التحميل إلى علامة صح · Spinner → success check | SP-0474 Spinner → success check | npm:hyperframes |
| UI-33 | 📄 | جدول ردود الفعل الدقيقة · Micro-feedback timing table | SP-0474 Spinner → success check | — |
| UI-64 | 📄 | عدسة تكبير التفاصيل · Magnifier lens pass | SP-0474 Spinner → success check | — |
| UI-46 | 💡 | لحظة احتفال توقيعية · Signature celebration moment | SP-0474 Spinner → success check | — |
| UI-40 | 📦 | إشعارات: نظام وجزيرة ورصّة · Notifications: native pop, dynamic island, stacks | SP-0475 HyperFrames UI component registry | npm:hyperframes, os:macos |
| UI-84 | 📦 | مكتبة مكوّنات HyperFrames للواجهات · HyperFrames UI component registry | SP-0475 HyperFrames UI component registry | npm:hyperframes |
| UI-68 | 👁 | شبكة بنتو للميزات · Bento feature grid | SP-0475 HyperFrames UI component registry | — |
