# البرمجة وبناء التطبيقات — Software & applications (`software`)

> مكتبة بروتوكول USIP v5.5، مولّدة بـ `scripts/smart_capabilities.py library` من `data/powers/*.json` و`data/tools.json`؛ لا تُحرَّر يدويًا. الدليل: [A28 اختيار القدرات](../protocol/A28-capability-routing.md) · [الفهرس](INDEX.md) · [النواة](../../PROTOCOL.md#متى-تفتح-الملاحق--appendix-triggers)

## الفهرس / contents

- [متى تستخدم هذه المجموعة / when](#متى-تستخدم-هذه-المجموعة--when)
- [الحالة بالأرقام / status](#الحالة-بالأرقام--status)
- [الأدوات القابلة للتشغيل / runnable tools](#الأدوات-القابلة-للتشغيل--runnable-tools)
- [العائلات / families](#العائلات--families)
- [كل القدرات / every power](#كل-القدرات--every-power)

## متى تستخدم هذه المجموعة / when

كلمات التوجيه: code programming apps api software frontend backend ui تطبيق برمجة واجهات تطوير

خط العمل المقترح (هدف تصميم، لم يُختبر كوحدة واحدة): التصميم → البرمجة → الاختبار → النشر

العضوية في المجموعة تصنيف للتوجيه، لا دليل على أن القدرات تعمل معًا: اربطها بخط عمل مختبر فقط.

## الحالة بالأرقام / status

| الحالة | العدد | المعنى |
|---|---:|---|
| `proven` | 111 | ✅ proven: a proof exists in the catalog; still check its requirements here before calling it ready |
| `ready` | 16 | 🟢 ready: runnable without setup according to the catalog |
| `documented` | 384 | 📄 documented: a described method; needs building or wiring before it runs |
| `seen` | 16 | 👁 seen: observed in a reference or demo, not executed here |
| `install` | 32 | 📦 install: needs a package, binary or model first |
| `key` | 7 | 🔑 key: needs an account, key or paid service (ask before any spend) |
| `idea` | 2 | 💡 idea: not built |
| **المجموع** | **568** | |

## الأدوات القابلة للتشغيل / runnable tools

| الأداة | ما تفعله | ابدأ بـ | الدليل |
|---|---|---|---|
| `app-studio` | استوديو التطبيقات للصور والتصميم | `python3 scripts/app_studio.py --help` | tested-here |
| `app-studio-paint` | حزمة الرسم في استوديو التطبيقات | `python3 -c "import sys; sys.path.insert(0,'scripts'); import app_studio; print(app_studio.PAINT_BATCH['effects'])"` | tested-here |
| `architecture-sizer` | مقدّر سعة الأنظمة | `python3 scripts/architecture_sizer.py --daily-requests 86400 --peak-factor 5 --payload-bytes 1000 --retention-days 7 --replica-rps 100 --target-utilization 0.5 --copies 2` | tested-here |
| `browser-scout` | مستكشف المواقع بالمتصفح | `python3 scripts/browser_scout.py doctor` | tested-here |
| `capability-graph` | باني خريطة القدرات المترابطة | `python3 scripts/capability_graph.py build` | tested-here |
| `installer-triage` | فرز المثبّتات | `python3 scripts/installer_triage.py scan ./setup.exe` | tested-here |
| `kosif-remote-commander` | خادم KOSIF Remote Commander | `python3 scripts/kosif_remote_superpowers.py doctor` | tested-here |
| `mosamem-rea-fusion` | تكامل مصمم وREA: فحص صور وتوليف مهارات آمن | `python3 scripts/mosamem_rea_fusion.py doctor` | tested-here |
| `motion-kit-bridge` | جسر توقيتات Motion Starter Kit | `python3 scripts/motion_kit_bridge.py styles` | tested-here |
| `motion-stack` | مولّد مشاريع بداية لمحركات الحركة | `python3 scripts/motion_stack.py list` | tested-here |
| `package-skill` | تحزيم المهارة للرفع إلى claude.ai | `python3 scripts/package_skill.py` | tested-here |
| `rea-owned-repo-batch` | تحليل REA لمستودعات المالك دفعةً واحدة | `python3 scripts/rea_owned_repo_batch.py --private-output "$HOME/kosif-private" --rea-cli ./node_modules/rea-agents/scripts/rea.mjs --max-repos 16 --max-size-kb 8000` | untested |
| `repository-capability-packer` | فحص المستودعات وحزمها | `python3 scripts/repository_capability_packer.py inspect ./repo --out ./repo-report.json` | tested-here |
| `source-scout` | مستكشف مصادر المجتمع | `python3 scripts/source_scout.py check` | tested-here |
| `web-app-study` | دراسة تطبيق ويب عام بـ REA (حقائق فقط) | `python3 scripts/web_app_study.py doctor` | tested-here |

الأوامر نسبية إلى مجلد المهارة (أو جذر المستودع لأدوات `tools/`)؛ `python3 scripts/hub.py tool <id>` يعطي كل الأوامر والمتطلبات والحدود.

## العائلات / families

| العائلة | القدرات | الفصل |
|---|---:|---|
| `app-feature-transfer` | 139 | [app-feature-transfer.md](../powers/app-feature-transfer.md) |
| `apps-artifacts` | 23 | [apps-artifacts.md](../powers/apps-artifacts.md) |
| `atlas-build` | 52 | [atlas-build.md](../powers/atlas-build.md) |
| `atlas-code` | 237 | [atlas-code.md](../powers/atlas-code.md) |
| `code-engineering` | 24 | [code-engineering.md](../powers/code-engineering.md) |
| `ui-product-device` | 93 | [ui-product-device.md](../powers/ui-product-device.md) |

## كل القدرات / every power

مرتبة بالحالة ثم العائلة ثم المعرّف. `hub.py` و`skill_intelligence.py deep <ID>` يعطيان بطاقة القدرة كاملة بدليلها.

| المعرّف | الاسم | English | الحالة | المتطلبات |
|---|---|---|---|---|
| `APPX-01` | منحنى السرعة | Speed curve (ramp) | proven | ffmpeg |
| `APPX-02` | مفتاح الكروما (الشاشة الخضراء) | Chroma key | proven | ffmpeg |
| `APPX-03` | إعادة التأطير التلقائي 9:16 | Auto reframe to 9:16 | proven | ffmpeg, pip:numpy, pip:opencv |
| `APPX-04` | كشف القطعات | Scene edit detection | proven | ffmpeg |
| `APPX-05` | توحيد علوّ الصوت للسوشيال | Loudness normalisation (-14 LUFS) | proven | ffmpeg |
| `APPX-06` | لون سينمائي من LUT | Colour look from a .cube LUT | proven | ffmpeg |
| `APPX-07` | حذف الوقفات والصمت | Pause and silence removal | proven | ffmpeg |
| `APPX-08` | علامات الإيقاع | Beat markers from audio | proven | pip:numpy |
| `APPX-09` | فقاعة الكاميرا فوق تسجيل الشاشة | Round camera bubble over a screen recording | proven | ffmpeg |
| `APPX-10` | تكبير بإطارات مفتاحية | Keyframed punch-in / Ken Burns | proven | ffmpeg |
| `APPX-100` | تشويهات: التواء وانتفاخ وانعكاس قطبي | Distort: twist, bulge, polar inversion, dents, frosted glass, tile reflection | proven | pip:numpy, pip:opencv |
| `APPX-101` | تغبيشات: تقريب ودوران وحركة وسطح | Blurs: zoom, radial, motion, surface, unfocus, fragment, median | proven | pip:numpy, pip:opencv |
| `APPX-102` | أسلبة: نقش وحواف وبكسلة وبلورات وتوهج | Stylize: emboss, relief, edge detect, outline, pixelate, crystallize, glow, soften portrait | proven | pip:numpy, pip:opencv |
| `APPX-103` | كسيريات جوليا وماندلبروت | Julia and Mandelbrot fractals | proven | pip:numpy, pip:opencv |
| `APPX-104` | تعديلات: مستويات وتقليل ألوان وسيبيا وضوضاء | Adjustments: levels, posterize, sepia, invert, auto level, add noise | proven | pip:numpy, pip:opencv |
| `APPX-105` | أوضاع المزج والطبقات (OpenRaster) | Blend modes (24) and layer stacks → PNG or OpenRaster | proven | pip:numpy, pip:pillow, pip:opencv |
| `APPX-106` | LUT سينمائي: صناعة وتطبيق | Cinematic 3D LUTs: make and apply .cube | proven | pip:numpy, pip:opencv |
| `APPX-107` | استبدال السماء | Sky replacement | proven | pip:numpy, pip:opencv |
| `APPX-109` | تغبيش العدسة بعمق وبوكيه | Lens blur with depth map and polygonal bokeh | proven | pip:numpy, pip:opencv |
| `APPX-11` | خفض الموسيقى تحت الصوت | Auto ducking | proven | ffmpeg |
| `APPX-110` | فرش الرسّام | MS Paint brushes on a canvas | proven | pip:numpy, pip:opencv |
| `APPX-111` | سطل التعبئة | Bucket fill (contiguous or global, with tolerance) | proven | pip:numpy, pip:opencv |
| `APPX-112` | صفحة تلوين من صورة | Coloring-book page from a photo | proven | pip:numpy, pip:opencv |
| `APPX-113` | ملصق بحد أبيض وظل | Sticker: cut-out with white border and soft shadow | proven | pip:numpy, pip:pillow, pip:opencv |
| `APPX-114` | رندر سينمائي بخمسة أساليب | Cinematic Cycles render presets (5 looks) | proven | python3, blender |
| `APPX-115` | حركة كاميرا سينمائية إلى MP4 | Camera moves with 180° motion blur → MP4 | proven | ffmpeg, python3, blender |
| `APPX-116` | تشطيب الفيلم في المركّب | Film finish in the Blender 5 compositor | proven | blender |
| `APPX-117` | جرد قدرات Blender الحي | Live Blender capability inventory | proven | python3, blender, npm:rea |
| `APPX-12` | تنقية الكلام من الضجيج | Speech noise reduction | proven | ffmpeg |
| `APPX-13` | ترجمة تلقائية بتوقيت الكلمات | Word-timed auto captions | proven | pip:faster-whisper |
| `APPX-14` | إزالة خلفية صورة | Background removal on a still | proven | pip:opencv |
| `APPX-15` | تصدير EDL ومطابقته | EDL interchange and conform | proven | ffmpeg |
| `APPX-16` | عكس المقطع وتجميد الإطار | Reverse and freeze frame | proven | ffmpeg |
| `APPX-17` | اختيار الغلاف تلقائيًا | Automatic cover pick | proven | pip:opencv |
| `APPX-24` | تقوية Electron بالـ fuses | Electron fuse hardening | proven | npm:rea |
| `APPX-30` | فرز المثبّت والتحقق من توقيعه | Installer triage and signature check | proven | python3, 7zip |
| `APPX-31` | إزالة الضباب | Dehaze (ClearView-style) | proven | chromium, pip:numpy, pip:opencv |
| `APPX-32` | تقليل الضوضاء بمستويات | Tiered noise reduction | proven | ffmpeg, chromium, pip:opencv |
| `APPX-33` | تصحيح المنظور تلقائيًا | Auto keystone / perspective | proven | chromium, pip:opencv |
| `APPX-34` | تصحيح تشوّه العدسة | Lens distortion correction | proven | chromium, pip:opencv |
| `APPX-35` | إزالة الزيغ اللوني | Lateral chromatic aberration removal | proven | chromium, pip:opencv |
| `APPX-36` | توازن الأبيض ومنحنى الدرجات وHSL | White balance + tone curve + HSL | proven | ffmpeg, chromium, pip:numpy, pip:opencv |
| `APPX-37` | حبيبات فيلم وتعتيم أطراف | Film grain + vignette | proven | ffmpeg, chromium, pip:numpy, pip:opencv |
| `APPX-38` | علامة مائية بشفافية دقيقة | Watermark with exact opacity | proven | ffmpeg, pip:pillow |
| `APPX-39` | ضغط JPEG إدراكي | Perceptual JPEG recompression (JPEGmini-style) | proven | chromium, pip:pillow, pip:opencv |
| `APPX-40` | ورقة تواصل وقوالب طباعة | Contact sheet / print templates | proven | pip:pillow |
| `APPX-41` | ملفات إعدادات مسبقة بإصدارات | Versioned preset / style files | proven | python3 |
| `APPX-42` | ملف XMP جانبي: تقييم ووسوم | XMP sidecar: rating, label, keywords | proven | python3 |
| `APPX-43` | تعديل الأفق تلقائيًا | Auto horizon straighten | proven | chromium, pip:opencv |
| `APPX-44` | بناء خط بتقنين الأزواج | Build a font with kerning | proven | pip:fonttools |
| `APPX-45` | عمليات بوليانية للأشكال المتجهة | Vector boolean operations | proven | pip:shapely |
| `APPX-46` | عمليات القنوات للحركة | Motion channel ops (CHOP-style) | proven | pip:numpy |
| `APPX-47` | مخطط مهام بتخزين مؤقت | Task graph with caching (PDG-style) | proven | python3 |
| `APPX-48` | تنزيل مجزأ قابل للاستئناف | Segmented, resumable download (IDM-style) | proven | python3 |
| `APPX-49` | حركة متوسطة وقشرة البصل وورقة رسوم | Eased tween, onion skin, sprite sheet | proven | pip:numpy, pip:pillow |
| `APPX-50` | دمج التعريضات والتحكم بالدرجات | Exposure fusion / selective tonal control | proven | chromium, pip:opencv |
| `APPX-53` | ملف لون لكل كاميرا | Per-camera colour profiles | proven | pip:pillow |
| `APPX-57` | كشف حمولات المثبّتات الخفية | Hidden installer payload detection | proven | python3, npm:rea, 7zip, innoextract |
| `APPX-61` | توضيح الحدة | Unsharp-mask sharpening | proven | chromium, pip:numpy, pip:pillow, pip:opencv |
| `APPX-62` | الوضوح والملمس | Clarity / texture (local contrast) | proven | chromium, pip:numpy, pip:pillow, pip:opencv |
| `APPX-63` | تحكم لوني لكل نطاق | HSL per colour band | proven | chromium, pip:numpy, pip:pillow, pip:opencv |
| `APPX-64` | أبيض وأسود بخلط القنوات | Black & white channel mixer | proven | chromium, pip:numpy, pip:pillow, pip:opencv |
| `APPX-65` | تلوين الظلال والإضاءات | Split toning / colour grading | proven | chromium, pip:numpy, pip:pillow, pip:opencv |
| `APPX-66` | إزالة احمرار العين | Red-eye removal | proven | chromium, pip:numpy, pip:pillow, pip:opencv |
| `APPX-67` | إزالة عنصر وترميم | Object removal / heal | proven | chromium, pip:numpy, pip:pillow, pip:opencv |
| `APPX-68` | إزالة التموج (مواريه) | Moiré removal | proven | chromium, pip:numpy, pip:pillow, pip:opencv |
| `APPX-69` | تأثير المجسم | Tilt-shift miniature | proven | chromium, pip:numpy, pip:pillow, pip:opencv |
| `APPX-70` | تغبيش الخلفية | Background blur (portrait) | proven | chromium, pip:numpy, pip:pillow, pip:opencv |
| `APPX-71` | قص بنسبة ذكي | Aspect crop with subject focus | proven | chromium, pip:numpy, pip:pillow, pip:opencv |
| `APPX-72` | تغيير المقاس | Resize for export | proven | chromium, pip:numpy, pip:pillow, pip:opencv |
| `APPX-73` | ضبط تلقائي للإضاءة | Auto tone / levels | proven | chromium, pip:numpy, pip:pillow, pip:opencv |
| `APPX-74` | قراءة بيانات الصورة وGPS | EXIF and GPS reader | proven | pip:pillow |
| `APPX-75` | كشف المكرر والمتشابه | Duplicate / near-duplicate finder | proven | chromium, pip:numpy, pip:pillow, pip:opencv |
| `APPX-77` | إعادة تسمية دفعة | Batch rename by EXIF date | proven | pip:pillow |
| `APPX-78` | فهرسة المكتبة والبحث | Photo catalog + search | proven | chromium, pip:numpy, pip:pillow, pip:opencv |
| `APPX-79` | تحويل صورة إلى متجه | Bitmap to vector (image trace) | proven | chromium, pip:numpy, pip:pillow, pip:opencv |
| `APPX-80` | صور إلى PDF | Images to PDF | proven | pip:pillow |
| `APPX-81` | نثر عناصر إجرائيًا | Procedural scatter (Poisson disc) | proven | chromium, pip:numpy, pip:pillow, pip:opencv |
| `APPX-82` | حقل ضوضاء إجرائي | Fractal noise field | proven | chromium, pip:numpy, pip:pillow, pip:opencv |
| `APPX-83` | نمو نباتي وزخرفي | L-system growth | proven | python3 |
| `APPX-84` | فحص خط | Font inspection | proven | pip:fonttools |
| `APPX-85` | تقليص خط للويب | Font subsetting | proven | pip:fonttools |
| `APPX-86` | تصدير Lottie | Lottie JSON export | proven | python3, npm:lottie |
| `APPX-87` | حل عظمتين (IK) | Two-bone inverse kinematics | proven | python3 |
| `APPX-88` | تصميم من قالب JSON | Template design (JSON → PNG/PDF) | proven | pip:numpy, pip:pillow, fonts:arabic, pip:arabic-reshaper |
| `APPX-89` | تغيير المقاس السحري | Magic Resize to every platform | proven | chromium, pip:numpy, pip:opencv |
| `APPX-90` | تأثير اللونين | Duotone | proven | pip:numpy, pip:pillow |
| `APPX-91` | كولاج وشبكات | Collage and grids | proven | pip:pillow |
| `APPX-92` | موك أب واقعي | Photo mockup | proven | chromium, pip:numpy, pip:opencv |
| `APPX-93` | رمز QR بشعار | QR code (verified) | proven | chromium, pip:opencv, pip:segno |
| `APPX-94` | ألوان الهوية | Brand palette (Brand Kit) | proven | chromium, pip:pillow, pip:opencv, npm:axe |
| `APPX-95` | رسم بياني بالعربية | Charts with Arabic labels | proven | pip:matplotlib, pip:arabic-reshaper |
| `APPX-96` | عرض PowerPoint | Presentation export (PPTX) | proven | pip:pillow, pip:office |
| `APPX-97` | PDF للمطبعة | Print PDF: bleed, crop marks, CMYK | proven | pip:pillow |
| `APPX-98` | نص متحرك | Text animation to GIF/MP4 | proven | ffmpeg, pip:numpy, pip:pillow |
| `APPX-99` | رسم زيتي وحبر ورصاص | Oil painting, ink sketch, pencil sketch | proven | pip:numpy, pip:opencv |
| `APP-04` | لوحة RTL بلا مكتبات | Dependency-free RTL dashboard page | proven |  |
| `APP-05` | لقطة شاشة بمقاس الهاتف وفحص الفيض | Phone-viewport screenshot + overflow check | proven | node, chromium |
| `APP-06` | من HTML إلى فيديو | HTML to MP4 renderer (repo tool) | proven | node, python3, chromium |
| `APP-09` | واجهة برمجية بـ FastAPI | HTTP APIs with FastAPI (tested in-process) | proven | python3 |
| `APP-10` | قوالب Jinja2 | Jinja2 templating | proven | python3 |
| `APP-11` | بناء خادم MCP (الإصدار 2) | Build an MCP server (mcp 2.x API) | proven | python3 |
| `CODE-03` | إثبات حزمة في بيئة معزولة | Prove a package in an isolated venv | proven | python3 |
| `CODE-23` | Hypothesis: اختبارات قائمة على الخصائص تولّد مدخلات فاشلة | Hypothesis: Property-based tests that generate and shrink failing inputs | proven | pip:hypothesis |
| `CODE-24` | Pandera: تعريف عقود بيانات لإطارات pandas وPolars وفرضها | Pandera: Declare and enforce schemas on pandas/Polars dataframes (data contracts) | proven | pip:pandas, pip:polars, pip:pandera |
| `UI-11` | مؤشر بفيزياء في motion-kit | motion-kit physics cursor + press + typeOn | proven | node, chromium |
| `UI-12` | واجهة منتج على Canvas بدالة draw(t) | Canvas product UI draw(t) recipe | proven | node, chromium |
| `UI-44` | شريط المراحل والحلقة والتقدم | Stepper, progress ring & progress bars | proven |  |
| `UI-80` | سطح زجاجي للواجهات | Glass surface stack | proven | chromium, npm:hyperframes |
| `UI-87` | مشغّل HTML مستقل بشريط تقديم | Standalone HTML player with seek & reduced motion | proven | node |
| `UI-X03` | تسجيل عرض واجهة بـPlaywright | Playwright UI demo recording (WebM) | proven | ffmpeg, node, chromium |
| `APPX-108` | التسييل (Liquify) | Liquify: push, pinch, bloat, twirl | ready | pip:numpy, pip:opencv |
| `UI-04` | إعادة بناء الشاشة كطبقات | Layered screen rebuild | ready |  |
| `UI-05` | حقيبة أصول من أجزاء حقيقية | Animation kit from real parts | ready | chromium, pip:pillow |
| `UI-14` | حلقة الضغط والتموج | Press ring & click ripple | ready |  |
| `UI-25` | كتابة بإيقاع بشري | Human-rhythm typing with caret | ready |  |
| `UI-34` | ضغط ومرور بمنطق القراءة | Press & hover with reading-direction nudges | ready |  |
| `UI-43` | مؤشرات التبويب والشريط النشط | Tab slide indicator & active rail bar | ready |  |
| `UI-45` | نقطة حالة بهالة وشارة مباشرة | Status dot with halo & live pill | ready |  |
| `UI-50` | هاتف 2.5D على Canvas | Canvas 2.5D phone (drawPhone) | ready |  |
| `UI-56` | موك أب HTML بلقطة 2× | HTML/CSS device & package mockup screenshot | ready | chromium |
| `UI-69` | لوحة قياس HUD وشروح مسقطة من 3D | Instrument-panel HUD & projected callouts | ready |  |
| `UI-72` | تسجيل صفحة بخطوات مبرمجة | Scripted page recording (Playwright) | ready | node, chromium |
| `UI-74` | فيلم إطلاق kmotion brag | kmotion brag launch film | ready | python3 |
| `UI-81` | معمارية الثيمات: الشكل × الوضع × العلامة | Look × theme × brand token architecture | ready |  |
| `UI-86` | أساليب KOSIF للواجهات | KOSIF UI styles to scaffold | ready | python3 |
| `UI-88` | مراجعة على الإطار: سحب وتحجيم واختصارات | Frame review: drag, resize & Arabic-safe shortcuts | ready |  |
| `APPX-118` | ميزات الذكاء في Photoshop: ما يقابلها | Photoshop AI features and their open counterparts | documented |  |
| `APPX-119` | ميزات الذكاء في الرسّام: ما يقابلها | MS Paint AI features and their open counterparts | documented |  |
| `APPX-120` | عقد الأمانة للتصميم بقائمة انحرافات مغلقة | Design fidelity contract with a closed deviation list | documented |  |
| `APPX-121` | التطابق أولًا ثم التكييف | Parity first, adaptation second | documented |  |
| `APPX-122` | حلقة التحقق البصري للواجهة مقابل المرجع | Visual verification loop for UI against a reference | documented | chromium, pip:pillow |
| `APPX-123` | استيراد واجهة من مستودع بقراءة أساس التصميم أولًا | Import UI from a repository by reading its design foundation first | documented | python3, git |
| `APPX-124` | الثيم كبيانات قابلة للنقل مع حقل نية المصمم | Theme as portable data with a designer-intent field | documented |  |
| `APPX-125` | قواعد افتراضية لإطارات الواجهات التفاعلية | Default rules for authored interactive UI frames | documented |  |
| `APPX-126` | التصميم مواصفة الشكل والمكوّن القديم مواصفة السلوك | Design is the look spec; the old component is the behaviour spec | documented |  |
| `APPX-127` | عقد أوامر مريح للوكيل | Agent-friendly command contract (JSON, non-interactive, dry-run, explicit states) | documented | python3 |
| `APPX-128` | فحص تمهيدي أولًا للحساب والسياق | Preflight probe first: auth, context and version as one JSON | documented | python3 |
| `APPX-129` | لوحة بصرية دائمة بجانب الوكيل | Persistent visual board beside the agent | documented |  |
| `APPX-130` | جلسة عمل بمرحلتين مع خط أساس وقائمة ملفات مسموحة | Two-phase work session with a baseline manifest and an editable-file allowlist | documented | python3 |
| `APPX-131` | تثبيت النسخة التي يراها المستخدم بالضبط | Pin exactly the version the user is looking at | documented | python3 |
| `APPX-132` | حزمة مراجع من التحديد تُعطى لكل العمّال | Selection-as-context reference bundle shared by every worker | documented |  |
| `APPX-133` | تنويعات على محاور مسمّاة جنبًا إلى جنب | Variant fan-out on named axes, side by side, never overwriting | documented | python3 |
| `APPX-134` | التعديل الحتمي أولًا والنموذج للباقي فقط | Deterministic-first edits; the model only for what cannot be rewritten safely | documented | python3 |
| `APPX-135` | نُسخ مرتبطة: نمط مشترك ومحتوى لكل سجل | Linked instances: shared style, per-record content | documented |  |
| `APPX-136` | نسخ لكل عنصر وارجع للخلف بدل مواصلة التلقين | Per-item revisions: roll back instead of piling on prompts | documented | python3 |
| `APPX-137` | الرسم التقريبي الموسوم للبنية والمرجع للمظهر | Labeled rough sketch for structure; reference for look | documented | python3 |
| `APPX-138` | جسر MCP باتجاهين مع تلميح التحديد الحالي | Two-way MCP bridge with a current-selection hint | documented | python3 |
| `APPX-139` | المهارات: تحميل بالوصف وتثبيت صريح واستيراد نصي آمن | Skills: description-matched loading, explicit pinning, safe text-only import | documented | python3 |
| `APPX-18` | منتقي الشاشة للتسجيل | Display-media picker for screen recording | documented |  |
| `APPX-19` | غرفة تحكم التسجيل | Recording mission-control and overlay windows | documented |  |
| `APPX-20` | واجهة احتياطية بلا إنترنت | Offline fallback renderer | documented |  |
| `APPX-21` | واجهات RTL مبنية مسبقًا | Prebuilt RTL bundles for Arabic | documented | node |
| `APPX-22` | اقترانات الملفات | File associations for media | documented | pip:pillow |
| `APPX-23` | جسر واحد بقناة MessagePort | Minimal context bridge over a MessagePort | documented |  |
| `APPX-25` | تحديث تلقائي | Auto update channel | documented | node |
| `APPX-26` | تقارير الأعطال | Crash and error reporting | documented | node |
| `APPX-27` | تكامل النظام | OS integration set | documented |  |
| `APPX-28` | مثبّت NSIS ثنائي المعمارية | Dual-architecture NSIS payload | documented | python3, 7zip |
| `APPX-29` | مثبّت تمهيدي عبر الإنترنت | Online bootstrap installer | documented |  |
| `APPX-51` | وحدة مستقلة لكل تصحيح | One plugin assembly per correction | documented | npm:rea |
| `APPX-52` | سلسلة توافق للإعدادات القديمة | Settings compatibility chain | documented |  |
| `APPX-54` | فرش التعديل المحلي كإعدادات | Local-adjustment brushes as presets | documented | pip:numpy, pip:opencv |
| `APPX-55` | حزمة هندسة الخطوط | Font engineering stack | documented | pip:fonttools |
| `APPX-56` | أصول إجرائية بمعاملات | Procedural digital assets | documented | blender, npm:three |
| `APPX-58` | خط تصدير الرسوم المتحركة | Animation export pipeline | documented | npm:three, npm:gsap, npm:lottie |
| `APPX-59` | كاميرا افتراضية من فيديو | Virtual camera from a video file | documented |  |
| `APPX-60` | مشغل فيديو عمودي بالسحب | Vertical swipe video player (Android) | documented |  |
| `APP-15` | اتجاه التصميم قبل الكود | Design direction before code | documented |  |
| `APP-16` | لمسات تجعل الواجهة أفضل | Interface polish numbers | documented |  |
| `APP-17` | اعرض ثلاثة خيارات بدل الأسئلة | Show three previews instead of asking | documented |  |
| `APP-18` | فصل المنشئ عن الناقد | Separate maker from critic | documented | chromium, git |
| `APP-19` | بوابة الإنهاء المرئية | Rendered finish gate | documented |  |
| `ABUILD-01` | تنفيذ خارطة الطريق تلقائياً: مرحلة لكل طلب دمج | Autonomous phase-per-PR roadmap execution loop | documented | claude:tools |
| `ABUILD-02` | مسجل قياس تشغيل بالملاحظة فقط | Observation-only run telemetry recorder | documented |  |
| `ABUILD-03` | خط وكلاء بأدوار ومراحل وأقفال كتابة واستئناف | Role-squad agent pipeline with stages, locks and resume | documented |  |
| `ABUILD-04` | تفكيك المواصفة إلى مهام صغيرة لوكلاء البرمجة | Spec-to-task decomposition for coding agents | documented |  |
| `ABUILD-05` | مسار توقيع وإصدار تطبيقات الجوال والمكتب | Mobile and desktop release signing pipeline | documented | os:macos |
| `ABUILD-06` | نموذج HTML تجريبي يجيب أسئلة مفتوحة | Open-question HTML prototype spike | documented |  |
| `ABUILD-07` | تنسيق بناء تطبيق كامل على مراحل | Phased full-stack app build orchestration | documented |  |
| `ABUILD-08` | تقييم النموذج مقابل معايير القبول | Prototype evaluation vs acceptance criteria | documented | chromium |
| `ABUILD-09` | توليد PWA مع service worker | PWA manifest and service worker generation | documented | chromium |
| `ABUILD-10` | هيكلة مشروع SaaS جاهز | SaaS boilerplate scaffold spec | documented | npm:react |
| `ABUILD-11` | حالة الاشتراكات وواجهة إدارة الاشتراك | Subscription store state and paywall UI | documented |  |
| `ABUILD-12` | نموذج أولي مؤقت للإجابة عن سؤال | Throwaway prototype to answer one question | documented |  |
| `ABUILD-13` | بناء موقع Wix هيدلس من وصفات SDK | Wix headless site build from SDK recipes | documented | chromium, key:unspecified |
| `ABUILD-14` | حلقة مراجع شجرة الوصولية لتحكم المتصفح | Accessibility-tree ref loop for browser agents | documented | node, chromium |
| `ABUILD-15` | استنساخ موقع بأدلة المتصفح | Browser-evidence website clone workflow | documented | chromium |
| `ABUILD-16` | تصحيح الصفحات الحية عبر Chrome DevTools MCP | Chrome DevTools MCP debugging of live pages | documented | chromium |
| `ABUILD-17` | خط لقطات Playwright داخل حاوية | Containerized Playwright screenshot pipeline | documented | chromium, docker |
| `ABUILD-18` | تشغيل متصفحات معزولة عبر بروتوكولاتها | Isolated headless Chrome/Firefox/Safari drivers over native protocols | documented | chromium |
| `ABUILD-19` | جلسات Playwright مسماة بمخرجات على القرص | Named-session Playwright CLI with disk artifacts | documented | node, chromium |
| `ABUILD-20` | كتابة اختبارات E2E مع فحص الوصولية والأداء | Playwright E2E authoring with lint, a11y and CWV scans | documented | python3, chromium |
| `ABUILD-21` | رفع ملف عبر Playwright MCP لحقل مخفي | Playwright MCP hidden file-input upload workaround | documented | chromium |
| `ABUILD-22` | إثبات السلوك المعروض بحكم نجح/فشل/معطل | Rendered-behavior proof with pass/fail/blocked verdict | documented | chromium |
| `ABUILD-23` | فحص جودة الواجهة بثلاثة عروض | Three-width responsive browser QA report | documented | network |
| `ABUILD-24` | ضبط مجمع الاتصالات وموثوقية قاعدة البيانات | Connection pool sizing and DB reliability playbook | documented |  |
| `ABUILD-25` | نص نسخ احتياطي لقاعدة البيانات مع الاحتفاظ والتشفير | Database backup script with retention and encryption | documented |  |
| `ABUILD-26` | تطور مخططات الأحداث وKafka | Event schema evolution and Kafka platform playbook | documented |  |
| `ABUILD-27` | قواعد Postgres وRedis المُدارة على المنصات | Managed Postgres and Redis on hosting platforms | documented |  |
| `ABUILD-28` | دليل الحوادث: احتواء وتشخيص واستعادة | Incident runbook: contain, diagnose, recover | documented |  |
| `ABUILD-29` | تصميم المراقبة: الإشارات الذهبية والتنبيهات | Observability design: golden signals and alerts | documented |  |
| `ABUILD-30` | استطلاع البنية وتدقيق التكلفة | Infra reconnaissance and cost audit | documented |  |
| `ABUILD-31` | تصميم مكوّن متاح افتراضيا | Accessible-by-default component pattern design | documented | npm:pa11y |
| `ABUILD-32` | إعداد هوية العلامة مع فحص التباين | Brand palette onboarding with WCAG gate | documented | npm:axe |
| `ABUILD-33` | حسابات الألوان وتخطيط CSS مع التباين | Color and CSS layout math with contrast | documented |  |
| `ABUILD-34` | التصميم عبر قيود مكانية وطباعية صريحة | Design by explicit spatial and type constraints | documented |  |
| `ABUILD-35` | نقد التصميم وتسليم المطورين وتدقيق النظام | Design critique, handoff and system audit | documented |  |
| `ABUILD-36` | اشتقاق وترقية نظام التصميم | Design-system retrofit and derivation workflow | documented |  |
| `ABUILD-37` | رموز التصميم DTCG لكل المنصات | DTCG design tokens multi-platform export | documented | npm:react |
| `ABUILD-38` | تدقيق تصميم الواجهة بالأدلة | Evidence-backed frontend design audit | documented | npm:react |
| `ABUILD-39` | استخراج بصمة التصميم من موقع حي | Extract Design DNA from live website | documented | npm:three |
| `ABUILD-40` | من ملف Figma إلى رموز وأصول وكود | Figma file to tokens, assets and code | documented |  |
| `ABUILD-41` | قراءة Figma عبر MCP أو REST | Figma read via MCP or REST fallback | documented |  |
| `ABUILD-42` | من Figma إلى كود مطابق | Figma to pixel-exact code plan | documented |  |
| `ABUILD-43` | تدقيق أداء الواجهة والاستجابة | Frontend performance and responsive audit | documented |  |
| `ABUILD-44` | اختبار الوصولية بلوحة المفاتيح مباشرة | Live keyboard accessibility test via browser | documented | npm:axe |
| `ABUILD-45` | صفحة هبوط فاخرة بحركة GSAP | Premium landing page with GSAP scroll motion | documented | npm:gsap |
| `ABUILD-46` | حلقة مقارنة لقطة الصفحة بالتصميم | Screenshot-vs-design pixel diff loop | documented | python3 |
| `ABUILD-47` | حلقة مقارنة لقطة الشاشة بالمرجع | Screenshot-vs-reference pixel diff loop | documented |  |
| `ABUILD-48` | معمارية رموز التصميم بثلاث طبقات | Three-tier design token architecture with theming | documented |  |
| `ABUILD-49` | تدقيق إتاحة WCAG 2.2: فحص وإصلاح وتحقق | WCAG 2.2 scan-fix-verify accessibility audit | documented | npm:axe |
| `ABUILD-50` | إصدار نسخة: وسم ونشر وتحقق | Cut a release: tag, GitHub release, verify | documented |  |
| `ABUILD-51` | صياغة التذاكر وأوصاف PR بهيكل ماذا/لماذا/كيف | What/Why/How ticket and PR drafting | documented |  |
| `ABUILD-52` | فرز أعطال الاتصال حسب مجال الخطأ دون تغيير الإعدادات | Fault-domain connectivity triage without touching config | documented |  |
| `ACODE-01` | اختبار حدود الحقن وتسليم القرار للبشر | Agent injection boundary and human-handoff tests | documented |  |
| `ACODE-02` | فحص أمان مسبق للوكيل بإيصال أخضر/أصفر/أحمر | Agent safety preflight with Green/Yellow/Red receipt | documented |  |
| `ACODE-03` | تدقيق سجلات جلسات الوكلاء بحثًا عن أسرار مسرّبة | Audit agent transcripts for leaked credentials | documented |  |
| `ACODE-04` | كتابة وفحص سكربتات سير عمل متعددة الوكلاء | Author and lint deterministic multi-agent workflow scripts | documented |  |
| `ACODE-05` | مقارنة وكلاء البرمجة في أشجار عمل معزولة | Benchmark Claude Code vs Codex in isolated worktrees | documented | python3, git |
| `ACODE-06` | إعادة هيكلة مرحلية بنقاط حفظ | Checkpointed multi-phase refactor surviving context limits | documented |  |
| `ACODE-07` | مرشحون متنافسون في worktrees ثم دمج الفائز | Competing worktree candidates, judged, one landed | documented | git, claude:tools |
| `ACODE-08` | تنسيق وكلاء أشجار العمل عبر رسائل وإيصالات | Coordinate worktree coding agents via mail and receipts | documented | git |
| `ACODE-09` | تفويض المهام لوكيل آخر مع بوابة مراجعة | Delegate to Codex or Claude with review gate | documented | git |
| `ACODE-10` | أنماط سير عمل دائم: ساجا وDAG | Durable workflow patterns: Temporal sagas and Airflow DAGs | documented | python3 |
| `ACODE-100` | صيد الأخطاء بمستويات إثبات | Bug hunt with tiered evidence findings | documented |  |
| `ACODE-101` | تشخيص فشل CI مع تنقيح السجلات | CI failure diagnosis with redacted logs | documented |  |
| `ACODE-102` | فرز أخطاء API بحسب الدليل وفئة الحالة | Evidence-based API error triage by status class | documented |  |
| `ACODE-103` | تصحيح الأخطاء بأربع مراحل منهجية | Four-phase reproduce-hypothesize-fix debugging | documented |  |
| `ACODE-104` | ماسح الإخفاقات الصامتة والأخطاء المبتلعة | Hidden-failure scanner for swallowed errors | documented |  |
| `ACODE-105` | دليل حوادث التكامل مع الاحتواء أولاً | Integration incident runbook with containment first | documented |  |
| `ACODE-106` | مراقبة التكاملات بالمقاييس والسجلات والتتبع | Integration observability: metrics, logs, traces, alerts | documented |  |
| `ACODE-107` | جلسة تصحيح Kubernetes بحاوية مؤقتة | kubectl debug ephemeral container session | documented |  |
| `ACODE-108` | عزل السبب الجذري طبقيًا قبل التعديل | Layered root-cause isolation before editing | documented |  |
| `ACODE-109` | تحليل السجلات للطلبات البطيئة وأنماط الخطأ | Log analysis for slow requests and error patterns | documented |  |
| `ACODE-11` | حلقة تطوير محلية ببيانات وهمية واختبار حي اختياري | Fixture-first local dev loop with opt-in live test | documented | key:unspecified |
| `ACODE-110` | خطة قياس مراقبة منخفضة التعدد | Low-cardinality observability instrumentation plan | documented |  |
| `ACODE-111` | إعادة بناء تجمد macOS من تقارير التشخيص | macOS freeze/panic reconstruction from DiagnosticReports | documented | os:macos |
| `ACODE-112` | فرضيات مرتبة قابلة للدحض مع قياس موسوم | Ranked falsifiable hypotheses with tagged instrumentation | documented |  |
| `ACODE-113` | حلقة تغذية راجعة قبل الفرضيات | Red-capable feedback loop before hypothesizing | documented | chromium |
| `ACODE-114` | إثبات الإصلاح باختبار أحمر ثم أخضر | Red-green-revert proof for bug fixes | documented | git |
| `ACODE-115` | حزمة تشخيص مُنقّحة بقائمة سماح | Redacted allowlist-based support debug bundle | documented |  |
| `ACODE-116` | حزمة تشخيص API منقّحة للدعم | Redacted API diagnostic bundle for support | documented |  |
| `ACODE-117` | تصحيح الأخطاء بالسبب الجذري أولاً | Root-cause-first debugging with one hypothesis | documented | git, pip:hypothesis |
| `ACODE-118` | سير عمل تصحيح مشكلة Sentry | Sentry issue debug-and-fix workflow | documented |  |
| `ACODE-119` | فحص الإخفاقات الصامتة في الفروقات | Silent failure scan on git diff | documented | python3, git |
| `ACODE-12` | حلقة مهام بوكلاء جدد ومراجعة مرحلتين | Fresh-subagent task loop with two-stage review | documented | git, claude:tools |
| `ACODE-120` | كاشف التراجع الصامت من بصمات السجل | Silent-fallback detector from log signatures | documented | python3 |
| `ACODE-121` | التحقق من استعادة النسخ الاحتياطي | Backup restore verification and DR rehearsal | documented |  |
| `ACODE-122` | حلقة إصلاح إخفاقات CI محدودة | Bounded CI failure repair loop | documented | gh |
| `ACODE-123` | تصميم تجربة فوضى مع نطاق الضرر وشروط الإيقاف | Chaos experiment design with blast radius and abort criteria | documented |  |
| `ACODE-124` | حكم فشل CI: منك أو من الفرع الرئيسي أو متقلب | CI failure verdict: yours, trunk-borne or flaky | documented |  |
| `ACODE-125` | تصميم خط CI: ترتيب وتخزين مؤقت | CI pipeline design: ordering, caching, required checks | documented |  |
| `ACODE-126` | النشر على المنصات السحابية عبر Blueprint أو Wrangler | Cloud platform deploy via Blueprint or Wrangler | documented |  |
| `ACODE-127` | تشخيص أعطال السحابة بفحص الصحة أولا | Cloud service triage via health-first diagnosis flow | documented |  |
| `ACODE-128` | تدقيق الحاويات وبودمان المتداخل | Container best-practice audit and rootless nesting | documented | docker |
| `ACODE-129` | أنماط Bash وzsh الدفاعية | Defensive Bash and zsh scripting conventions | documented |  |
| `ACODE-13` | عزل أوامر الوكيل على macOS بـ Seatbelt | macOS Seatbelt confinement for agent commands | documented | os:macos |
| `ACODE-130` | بوابة CI آمنة بلا أسرار للتكاملات | Fail-closed credential-free CI gate for integrations | documented |  |
| `ACODE-131` | مسار نشر Azure بثلاث بوابات | Gated Azure prepare-validate-deploy workflow | documented |  |
| `ACODE-132` | حوكمة GCP: التسلسل والشبكة والفوترة | GCP resource hierarchy, networking and billing governance | documented |  |
| `ACODE-133` | تشخيص فشل GitHub Actions عبر gh | GitHub Actions failure triage via gh | documented | gh |
| `ACODE-134` | تدقيق هدر تكلفة GitHub Actions | GitHub Actions FinOps waste audit | documented | gh |
| `ACODE-135` | محسّن تكلفة مشغلات GitHub Actions | GitHub Actions runner-cost optimizer | documented |  |
| `ACODE-136` | GitHub Actions إلى GCP عبر Workload Identity | GitHub Actions to GCP with Workload Identity Federation | documented |  |
| `ACODE-137` | تسليم GitOps عبر Argo CD أو Flux | GitOps delivery with Argo CD or Flux | documented |  |
| `ACODE-138` | بناء حاوية آمنة متعددة المراحل | Hardened multi-stage container build | documented | docker, trivy |
| `ACODE-139` | استعادة إصدارات Helm والتراجع | Helm release recovery and rollback | documented |  |
| `ACODE-14` | حلقة تجارب ذاتية بمقياس: احتفظ أو تراجع | Metric-driven autonomous experiment loop (keep or reset) | documented | python3, git |
| `ACODE-140` | بوابة CI للتكامل: فحوص بلا اتصال واختبار حي محمي | Integration CI gate: offline fixtures plus guarded live smoke | documented |  |
| `ACODE-141` | أساس منصة كوبرنتس متعددة المستأجرين | Kubernetes multi-tenant platform baseline | documented |  |
| `ACODE-142` | فحص ملفات workflow لمشاكل المشغلات الذاتية | Lint workflows for self-hosted runner pitfalls | documented |  |
| `ACODE-143` | تصميم خط نشر متعدد المراحل ببوابات | Multi-stage deployment pipeline design with gates | documented |  |
| `ACODE-144` | مصادقة CI بلا كلمات مرور عبر OIDC | Passwordless CI cloud auth via OIDC federation | documented |  |
| `ACODE-145` | دليل فرز الحوادث والتراجع | Platform incident triage and rollback runbook | documented |  |
| `ACODE-146` | قائمة نشر وتكامل CI حسب المنصة | Platform-specific deploy and CI integration checklist | documented |  |
| `ACODE-147` | خطة تغيير كوبرنيتس إنتاجية بمعايير SRE | Production Kubernetes change plan with SRE standards | documented |  |
| `ACODE-148` | إثبات عدم وجود مستهلك قبل حذف سر سحابي | Prove no consumer before destroying cloud secret | documented |  |
| `ACODE-149` | تطبيق Terraform من خطة محفوظة | Saved-plan non-interactive terraform apply | documented |  |
| `ACODE-15` | فحوص ما قبل التنفيذ لتصادم الوكلاء المتوازيين | Parallel agent collision pre-flight checks | documented | gh |
| `ACODE-150` | قائمة تحصين بيئة serverless | Serverless runtime hardening checklist | documented |  |
| `ACODE-151` | خطة نشر مرحلية مع تراجع وفصل الأسرار | Staged deployment plan with rollback and secret separation | documented |  |
| `ACODE-152` | نشر تكامل مرحلي مع كناري وإيصال تراجع | Staged integration deploy with canary and rollback receipt | documented |  |
| `ACODE-153` | هدم مرحلي لـ ECS بـ Terraform | Staged Terraform teardown for ECS capacity providers | documented |  |
| `ACODE-154` | وحدات Terraform وكشف الانحراف | Terraform and IaC module generation with drift checks | documented |  |
| `ACODE-155` | قواعد Terraform وبوابة سياسة للقراءة فقط | Terraform generation posture rules and read-only policy gate | documented |  |
| `ACODE-156` | بوابة سياسات خطة Terraform | Terraform plan policy gate (OPA) | documented |  |
| `ACODE-157` | كتابة workflows لـ GitHub Actions مع تحقق | Verified GitHub Actions workflow authoring | documented | gh |
| `ACODE-158` | تصميم تطبيق Agent SDK وخطافاته | Agent SDK app and hooks design | documented | key:openai |
| `ACODE-159` | حكم LLM معايَر ومدقَّق التحيز | Calibrated, bias-audited LLM-as-judge | documented |  |
| `ACODE-16` | عقد إطلاق وكلاء متوازيين مع فحص مسبق | Parallel agent dispatch contract with worktree preflight | documented | git, claude:tools |
| `ACODE-160` | تحصين حدود المعدل وإعادة المحاولة | Claude API rate-limit and retry hardening | documented |  |
| `ACODE-161` | حزمة تقييم LLM ثابتة بمجموعة ذهبية | Committed LLM eval suite with goldens | documented | python3 |
| `ACODE-162` | رصد تطبيقات الذكاء التوليدي بـ OpenTelemetry | GenAI observability with OpenTelemetry | documented |  |
| `ACODE-163` | خط RAG هجين مع إحالات | Hybrid-search RAG pipeline with citations | documented | pip:chromadb |
| `ACODE-164` | تحصين LangChain 1.0 للإنتاج | LangChain 1.0 production hardening | documented |  |
| `ACODE-165` | حالة وتدفق وكلاء LangGraph | LangGraph 1.0 agent state and flow | documented | python3 |
| `ACODE-166` | تخطيط ضبط نماذج اللغة SFT/DPO | LLM fine-tuning job planning (SFT/DPO/GRPO) | documented | pip:llama-cpp |
| `ACODE-167` | مراقبة LLM وتحليل الإخفاقات | LLM observability and failure triage | documented |  |
| `ACODE-168` | ترحيل مزود LLM إلى Bedrock | Migrate LLM provider SDK to Bedrock | documented | key:openai |
| `ACODE-169` | تفويض متعدد النماذج ورأي ثانٍ | Multi-model delegation and second opinion | documented |  |
| `ACODE-17` | فحص تمهيدي قبل بدء مهمة | Preflight check before starting an issue | documented | git |
| `ACODE-170` | تدقيق ذاكرة الـprompt المؤقتة وإصلاحها | Prompt-cache hit-rate audit and fix | documented |  |
| `ACODE-171` | دليل بناء وضبط خط RAG | RAG pipeline build and tuning guide | documented | pip:chromadb |
| `ACODE-172` | عقد مخرجات LLM منظمة موثوقة | Reliable structured LLM output contract | documented |  |
| `ACODE-173` | تتابع مزودي LLM عبر Router | Vendor failover waterfall via LiteLLM Router | documented | python3 |
| `ACODE-174` | بناء شجرة هجوم | Attack tree construction | documented | graphviz, npm:mermaid |
| `ACODE-175` | وثائق ما قبل الإطلاق للتطبيقات المولدة | Pre-ship documentation set for vibe-coded apps | documented |  |
| `ACODE-176` | تجهيز حزم الامتثال لأرقام Twilio | Twilio regulatory bundle provisioning | documented |  |
| `ACODE-177` | مخطط تسلسل موثق من نقطة دخول الكود | Cited sequence diagram from code entry point | documented | npm:mermaid |
| `ACODE-178` | البحث في مكتبة المكونات بسكربت مساعد | Component library lookup with helper script | documented | node |
| `ACODE-179` | بوابة جودة التصميم في CI | Design-quality CI gate with SARIF | documented |  |
| `ACODE-18` | استعادة سير عمل متوقف دون تكرار | Recover interrupted workflow run without duplicates | documented | git, gh |
| `ACODE-180` | بناء نظام رموز التصميم | Design token system scaffold | documented | npm:react |
| `ACODE-181` | فحص القيم الصلبة واستبدالها برموز | Hardcoded-style scan to design tokens | documented |  |
| `ACODE-182` | هيكلة مكون React مع shadcn وTailwind وStorybook | React component scaffold with shadcn, Tailwind, Storybook | documented | npm:react |
| `ACODE-183` | إعداد shadcn وUnoCSS لتنسيق المكونات | shadcn and UnoCSS component styling setup | documented | npm:react |
| `ACODE-184` | قواعد تركيب shadcn وTailwind | shadcn/ui and Tailwind composition rules | documented | npm:react |
| `ACODE-185` | فاحص وصولية HTML مع بقايا يدوية | Stdlib HTML accessibility linter with manual residue | documented | npm:axe |
| `ACODE-186` | مراجعة الوصولية وفق WCAG | WCAG four-principle accessibility review | documented | npm:axe, npm:pa11y |
| `ACODE-187` | بيفي: ECS وتدفق الحالات وخط الأصول | Bevy ECS, state flow and asset pipeline | documented |  |
| `ACODE-188` | حزمة ألعاب المتصفح وPhaser | Browser game stack, Phaser and web foundations | documented | npm:esbuild |
| `ACODE-189` | فيزياء خطوة ثابتة وكشف تصادم | Fixed-step physics and collision broadphase | documented |  |
| `ACODE-19` | خطافات ميزانية زمنية ناعمة للوكلاء الفرعيين | Soft wall-clock budget hooks for subagents | documented | claude:tools |
| `ACODE-190` | اختيار تمثيل الهندسة وSDF وتحويل الشبكات | Geometry, SDF and mesh-voxel conversion choice | documented |  |
| `ACODE-191` | أنماط معمارية لـ GDScript في Godot 4 | Godot 4 GDScript architecture patterns | documented | chromium |
| `ACODE-192` | فحص محرر Godot الحي عبر سطر الأوامر | Godot live-editor inspection via CLI | documented |  |
| `ACODE-193` | حلقة قياس أداء اللعبة | Measured game performance loop | documented |  |
| `ACODE-194` | وحدة DOTS وأتمتة محركات Unity وUnreal | Unity DOTS ECS and Unreal/Unity automation | documented | python3 |
| `ACODE-195` | تصنيف نتائج regex قبل الاستبدال الجماعي | Classify regex matches before bulk sweep | documented |  |
| `ACODE-196` | فحص الكود الميت وتنظيف الاستيراد | Dead code and import cleanup scan | documented |  |
| `ACODE-197` | إضافة رمز تشخيص منظم لمكتبة JS | Diagnostic code catalog entry | documented |  |
| `ACODE-198` | إدارة مهام todo.md عبر سكربتات | Markdown todo file task scripts | documented | python3 |
| `ACODE-199` | مزامنة متتبع الميزات مع TODO | Sync feature tracker with TODO | documented |  |
| `ACODE-20` | أساطيل أشجار عمل لمراحل وكلاء متوازية | Worktree fleets for parallel agent phases | documented | git |
| `ACODE-200` | تقسيم التغييرات إلى commits ذرية | Atomic commit splitting by purpose | documented | git |
| `ACODE-201` | مراقبة PR حتى يصبح جاهزا للدمج | Babysit PR until green and mergeable | documented | gh |
| `ACODE-202` | سجل تغييرات من الكوميتات | Changelog from commits, Keep a Changelog | documented | git |
| `ACODE-203` | رسالة commit بصيغة Conventional من التغييرات | Conventional commit from staged diff | documented | git |
| `ACODE-204` | خطافات تمنع أوامر git الخطرة | Dangerous git command guardrail hooks | documented |  |
| `ACODE-205` | محاكاة تعارضات قائمة الدمج | Merge queue conflict simulation | documented | git |
| `ACODE-206` | مراقبة طلب الدمج حتى الدمج | PR babysit loop to merge | documented | mcp:github |
| `ACODE-207` | وصف PR من الفروقات وقالب المستودع | PR body from diff using repo template | documented | git, gh, mcp:github |
| `ACODE-208` | فتح طلب دمج بوصف واضح | PR creation with reviewer-friendly body | documented | gh |
| `ACODE-209` | إزالة أسرار دُفعت من السجل المستضاف | Purge pushed secrets from hosted history | documented | git, gh |
| `ACODE-21` | معالجة 429: انتظار وتراجع أسي مع تشويش | 429 handler: Retry-After, backoff, jitter | documented |  |
| `ACODE-210` | إصدار نسخة مع سجل التغييرات والوسم | Release cut with changelog and tag | documented |  |
| `ACODE-211` | حل تعارضات الدمج وإعادة التأسيس | Resolve rebase and merge conflicts | documented | git |
| `ACODE-212` | تقسيم فرع إلى فروع بكوميت واحد | Split branch into one-commit branches | documented | git |
| `ACODE-213` | طلبات دمج متراكبة عبر gh stack | Stacked PRs with gh stack | documented |  |
| `ACODE-214` | طلبات دمج متراكمة مع Graphite وMergify | Stacked PRs with Graphite or Mergify | documented | node |
| `ACODE-215` | مسار من issue إلى PR بأشجار عمل معزولة | Worktree-isolated issue-to-PR flow | documented | git, gh |
| `ACODE-216` | إدارة worktree وتنظيفها بأمان | Worktree lifecycle and safe cleanup | documented | git |
| `ACODE-217` | تصميم أدوات الوكلاء: المستهلك نموذج لا إنسان | Agent tool design: the consumer is a model | documented | claude:tools |
| `ACODE-218` | حدود الثقة في الأدوات: الأسرار تُحقن والصلاحيات في الكود | Tool trust boundary: injected secrets, permissions in code | documented |  |
| `ACODE-219` | منع رفع الأسرار عند الالتزام | Block secrets at commit time | documented |  |
| `ACODE-22` | تحويل حالات المهام غير المتزامنة لأحداث | Async job state to durable internal events | documented |  |
| `ACODE-220` | مراجعة أمان للتغيير لا للمستودع كله | Change-scoped security review vs posture audit | documented |  |
| `ACODE-221` | التحقق من السلوك لا من التفاصيل الداخلية، بأوامر المستودع نفسه | Behaviour-level assertions per layer, with the repo's own commands | documented | node |
| `ACODE-222` | قاعدة الاعتماد في البنية النظيفة | Clean Architecture dependency rule | documented |  |
| `ACODE-223` | أداء الويب: الكمون قبل عرض النطاق | Web performance: latency before bandwidth | documented |  |
| `ACODE-224` | قياس التحسين مقابل خط أساس مُلتقط قبل التغيير | Measure improvement against a baseline captured before | documented |  |
| `ACODE-225` | jq: نموذج المرشّح لتدفق JSON | jq filter mental model for JSON streams | documented |  |
| `ACODE-226` | تصميم تطبيقات Apple: اختر المسار أولاً | Apple platform design: choose the track first | documented | npm:react, os:macos |
| `ACODE-227` | ضبط ruff للفحص والتنسيق دون فخ select | ruff lint and format without the select trap | documented | python3 |
| `ACODE-228` | إدارة مشاريع بايثون والسكربتات ببرنامج uv | Python projects, scripts and tools with uv | documented | python3 |
| `ACODE-229` | اختيار طريقة مواءمة التفضيلات DPO/ORPO/KTO/SimPO | Choosing DPO, ORPO, KTO or SimPO for preference tuning | documented |  |
| `ACODE-23` | قائمة صمود الخلفية أمام الاعتماديات | Backend resilience checklist for dependencies | documented |  |
| `ACODE-230` | تصميم خادم MCP: نموذج النشر ونمط الأدوات قبل الكود | MCP server design: deployment model and tool pattern before code | documented | python3, key:unspecified |
| `ACODE-231` | تدقيق كل الترقيات الممكنة بمصفوفة مخاطرة/عائد قبل التطبيق | Upgrade-everything audit with a risk/reward matrix | documented |  |
| `ACODE-232` | كشف الاختبارات الخضراء الكاذبة | False-green test detection | documented |  |
| `ACODE-233` | اختبار في فضاء مصغّر: تفكيك ادعاء التكافؤ قبل التجربة | Reduced-space test: decompose the equivalence claim first | documented |  |
| `ACODE-234` | اختبار استكشافي لتطبيق ويب بأدلة إعادة إنتاج كاملة | Exploratory web-app QA with full repro evidence | documented | chromium |
| `ACODE-235` | تدقيق الامتثال لـ GDPR انطلاقًا من جرد البيانات الشخصية | GDPR review built on a personal-data inventory | documented |  |
| `ACODE-236` | دليل سردي لمستودع غير مألوف للمساهمين الجدد | Narrative codebase guide for newcomers | documented | npm:mermaid |
| `ACODE-237` | تثبيت كل أسطح الإصدارات لتقوية سلسلة التوريد | Pin every version surface for supply-chain hardening | documented | node, python3 |
| `ACODE-24` | أنماط خدمات الواجهة الخلفية بعدة لغات | Backend service patterns: Node, Go, .NET, Django | documented |  |
| `ACODE-25` | اختيار وتخزين مفاتيح الـAPI بأمان | Choose and store API credentials safely | documented | chromium, key:unspecified |
| `ACODE-26` | اختيار واجهة Zoom المناسبة | Choose Zoom surface: REST, webhooks, WebSocket, SDK | documented | key:unspecified |
| `ACODE-27` | اختبار عقود API من جهة المستهلك بـ Pact | Consumer-driven API contract testing with Pact | documented |  |
| `ACODE-28` | استخراج عميل API مستقل من تسجيل HAR | Derive standalone API client from HAR recording | documented |  |
| `ACODE-29` | قائمة تحصين نقطة GraphQL | GraphQL endpoint hardening checklist | documented |  |
| `ACODE-30` | مصادقة JWT مع تدوير التحديث وصلاحيات الأدوار | JWT auth with refresh rotation and RBAC | documented | key:unspecified |
| `ACODE-31` | إعداد مصادقة API بأقل صلاحيات والتحقق منها | Least-privilege API auth setup and verification | documented | key:unspecified |
| `ACODE-32` | استقبال OAuth محلي مع ملفات رموز محمية | Local OAuth callback with 0600 token files | documented | key:unspecified |
| `ACODE-33` | فوترة بالاستهلاك مع تسجيل غير مكرر | Metered billing with idempotent usage | documented |  |
| `ACODE-34` | مدفوعات آمنة: دفتر مزدوج وتسوية | Money-safe payments: ledger, idempotency, reconciliation | documented |  |
| `ACODE-35` | تخطيط نمط OAuth والصلاحيات وتجديد الرموز | OAuth grant, scope and token-refresh planning | documented | key:unspecified |
| `ACODE-36` | اختبار تكامل يعدّ عدد إصدارات التوكن | OAuth token-mint counting integration test | documented | key:unspecified |
| `ACODE-37` | اختيار تدفق OAuth/OIDC حسب نوع العميل | OAuth2/OIDC flow selection by client type | documented | key:unspecified |
| `ACODE-38` | توليد مواصفة OpenAPI 3.1 واستخراجها من الكود | OpenAPI 3.1 spec generation and discovery | documented |  |
| `ACODE-39` | تدفقات مصادقة بلا كلمة مرور وJWT | Passwordless, passkey and JWT auth flows | documented | key:unspecified |
| `ACODE-40` | دليل دمج الدفع والفوترة | Payments and billing integration guide | documented |  |
| `ACODE-41` | عميل API يحترم حدود المعدل مع إعادة محاولة | Rate-limit-aware API client with bounded retry | documented |  |
| `ACODE-42` | مبادئ تصميم REST وGraphQL | REST and GraphQL API design principles | documented |  |
| `ACODE-43` | محدد معدل طلبات مشترك مع تراجع أسي | Shared rolling-window rate limiter with backoff | documented |  |
| `ACODE-44` | خط بناء مورد Express من مواصفة | Spec-driven Express resource build pipeline | documented | node |
| `ACODE-45` | إعداد SPF وDKIM وDMARC بمراحل | SPF, DKIM, DMARC staged rollout | documented |  |
| `ACODE-46` | قوالب SSE والمصادقة والزمن الحقيقي | SSE, auth, SSO and realtime scaffolds | documented |  |
| `ACODE-47` | قرارات تكامل Stripe والترقية | Stripe integration decisions and upgrades | documented |  |
| `ACODE-48` | دليل بناء رسائل وصوت Twilio | Twilio messaging and voice build guide | documented |  |
| `ACODE-49` | غلاف عميل API مُنمّط مع إعادة المحاولة | Typed API client adapter with retries | documented |  |
| `ACODE-50` | طبقة مهايئ مُنمّطة لـ SDK أو REST خارجي | Typed vendor SDK/REST adapter boundary | documented |  |
| `ACODE-51` | إعداد مفاتيح API وفحصها بأقل صلاحية | Vendor API credential setup and verification | documented | key:unspecified |
| `ACODE-52` | مستقبل ويبهوك موثّق وآمن من التكرار | Verified idempotent webhook receiver | documented |  |
| `ACODE-53` | مستهلك webhook: توقيع HMAC وإزالة التكرار | Webhook consumer: raw-body HMAC, dedupe, fast ack | documented |  |
| `ACODE-54` | مستقبل ويب هوك: توقيع وتكرار آمن | Webhook receiver: HMAC, idempotency, replay | documented |  |
| `ACODE-55` | مستقبل ويبهوك مع توقيع HMAC ومنع التكرار | Webhook receiver with HMAC and idempotency | documented |  |
| `ACODE-56` | خادم WebSocket بمصادقة وغرف واشتراكات | WebSocket server with handshake auth and rooms | documented |  |
| `ACODE-57` | محدد معدل طلبات API مع تراجع أسي | Cost-aware API rate limiter with backoff | documented |  |
| `ACODE-58` | دورة حياة أعلام الميزات وتدقيق الديون | Feature flag lifecycle and debt audit | documented |  |
| `ACODE-59` | مقارنة لقطات الذاكرة لكشف التسربات | Heap snapshot diff for web memory leaks | documented |  |
| `ACODE-60` | حزمة جاهزية التكامل للإنتاج | Integration production-readiness pack (hello, CI, observability) | documented |  |
| `ACODE-61` | تطبيق MCP بأداة وواجهة | MCP App tool plus UI resource | documented | npm:esbuild, npm:react, key:openai |
| `ACODE-62` | التقاط وفك حركة مرور التطبيق | Mitmproxy app traffic capture and decode | documented |  |
| `ACODE-63` | فحص امتثال تطبيق شوبيفاي قبل التقديم | Shopify App Store pre-submission compliance sweep | documented |  |
| `ACODE-64` | ضابط حدود معدل واجهات الموردين | Vendor API rate-limit governor | documented |  |
| `ACODE-65` | التحقق من توقيع الويب هوك مع منع التكرار | Webhook HMAC verify, dedupe, fast-ack | documented |  |
| `ACODE-66` | محافظ Circle وUSDC متعدد السلاسل | Circle USDC wallets and cross-chain balance | documented | node, key:unspecified |
| `ACODE-67` | قوالب بروتوكولات دي فاي وعقود NFT | DeFi protocol and NFT contract templates | documented |  |
| `ACODE-68` | تصميم إرسال معاملات EVM آمن | Safe EVM transaction submission design | documented |  |
| `ACODE-69` | اختبار العقود الذكية بهاردهات وفاوندري | Smart contract test suite with Hardhat and Foundry | documented | node, key:unspecified |
| `ACODE-70` | تدقيق أمان عقود سوليديتي | Solidity vulnerability audit and secure patterns | documented |  |
| `ACODE-71` | تطوير Sui Move وإعداد Solana | Sui Move and Solana network/keypair setup | documented |  |
| `ACODE-72` | قراءات EVM مكتوبة وواجهات NFT عبر viem | Typed EVM reads and NFT APIs with viem | documented | node, key:unspecified |
| `ACODE-73` | ورشة SLO وسياسة ميزانية الخطأ | SLO workshop with error budget policy | documented |  |
| `ACODE-74` | تدقيق وضغط ملفات تهيئة الوكيل | Agent onboarding file audit and compression | documented |  |
| `ACODE-75` | استعلام رسم المعرفة قبل مسح الملفات | Code knowledge graph queries before file scanning | documented |  |
| `ACODE-76` | خريطة مشروع مؤرخة مع وصفات التعديل | Dated codebase map with change recipes | documented |  |
| `ACODE-77` | مسح الكود الميت وصحة الاعتماديات | Dead code and dependency hygiene sweep | documented |  |
| `ACODE-78` | رسم اعتماديات موثق من ملفات البناء | Dependency graph cited from build manifests | documented | npm:mermaid |
| `ACODE-79` | هندسة عكسية وصفية لمواصفات قابلة للتتبع | Descriptive reverse engineering into traceable specs | documented |  |
| `ACODE-80` | شرح تغيير أو مسار كود بالأدلة | Explain a change or code path grounded in evidence | documented | git |
| `ACODE-81` | خوارزمية تعديل الكود القديم باختبارات التوصيف | Legacy code change algorithm with characterization tests | documented |  |
| `ACODE-82` | رسم المشروع بوكلاء متوازين وكشف التغيير | Parallel subagent mapping with merkle change detection | documented | claude:tools |
| `ACODE-83` | محلل Python AST يراعي الأسماء المستعارة والنطاق | Python AST analyzer with alias and scope handling | documented | python3 |
| `ACODE-84` | بحث وإعادة كتابة بنيوية بـ ast-grep | Structural search and rewrite with ast-grep | documented | node |
| `ACODE-85` | أنماط كتابة DAG في Airflow | Airflow DAG authoring patterns | documented | python3 |
| `ACODE-86` | تأليف موصل تزايدي بـ Airbyte CDK | Incremental connector authoring (Airbyte CDK) | documented | python3, key:unspecified |
| `ACODE-87` | بوابة أمان لأوامر SQL المدمرة مع تجربة جافة | Destructive-SQL safety gate with dry-run | documented |  |
| `ACODE-88` | مراجعة مخطط قاعدة البيانات بعدسات متعددة | Multi-lens database schema review | documented | lean |
| `ACODE-89` | ترقية Prisma من 6 إلى 7 | Prisma 6 to 7 upgrade procedure | documented | node |
| `ACODE-90` | توليد بيانات اختبار وكود ORM | Realistic test data seeding and ORM code generation | documented |  |
| `ACODE-91` | نموذج بيانات Redis وقائمة التشغيل | Redis data model and ops checklist | documented |  |
| `ACODE-92` | تصميم مخطط من وصف المجال | Schema design from domain description | documented |  |
| `ACODE-93` | ربط تطبيق Supabase وتوسيعه | Supabase app wiring and scaling | documented | npm:react |
| `ACODE-94` | سياسات RLS ومفاتيح Supabase الآمنة | Supabase RLS, auth and key hygiene | documented |  |
| `ACODE-95` | ترحيل مخطط قاعدة البيانات دون توقف | Zero-downtime expand/contract schema migration | documented |  |
| `ACODE-96` | خطة ترحيل Postgres بلا توقف | Zero-downtime Postgres migration playbook | documented | node |
| `ACODE-97` | تصحيح تنافسي بفرضيات متعددة ووكلاء | Adversarial competing-hypothesis debugging with agent team | documented | pip:hypothesis |
| `ACODE-98` | تصحيح عدائي متعدد الوكلاء بفرضيات متنافسة | Adversarial multi-agent competing-hypothesis debugging | documented |  |
| `ACODE-99` | فرز أخطاء API حسب الحالة ومعرّف التتبع | API error triage by status and trace ID | documented |  |
| `CODE-01` | ابحث قبل أن تبني | Search-first: adopt, extend, compose, build | documented | node, python3 |
| `CODE-02` | الوثائق الحية قبل الذاكرة | Live docs over memory | documented | node, claude:tools |
| `CODE-04` | دليل التعرّف على مستودع | Codebase onboarding guide | documented | git |
| `CODE-05` | قائمة أثر التغيير | Change-impact checklist | documented |  |
| `CODE-06` | حقائق قبل أول تعديل | Fact-forcing before the first edit | documented |  |
| `CODE-07` | اتبع أسلوب المستودع القائم | Inherit the repo's style | documented |  |
| `CODE-08` | التطوير بالاختبار أولًا | Test-driven development | documented |  |
| `CODE-09` | حلقة التحقق بست مراحل | Six-phase verification loop | documented | ffmpeg, node, git, key:unspecified |
| `CODE-10` | نقاط تفتيش وخط أساس للانحدار | Checkpoints, regression baselines and pass^k | documented |  |
| `CODE-11` | حلقة التشخيص من الجذر | Root-cause debugging loop | documented | pip:hypothesis |
| `CODE-12` | إصلاح البناء بأقل فرق | Minimal-diff build fixing | documented |  |
| `CODE-13` | صيد الأعطال الصامتة | Silent-failure and click-path hunt | documented |  |
| `CODE-14` | حلقة تحسين أداء مقاسة | Measured optimization loop | documented |  |
| `CODE-15` | معالجة أخطاء متينة | Resilient error handling | documented |  |
| `CODE-16` | قائمة مراجعة الكود | Code review checklist | documented |  |
| `CODE-18` | إعادة هيكلة آمنة | Safe refactoring | documented | key:graphify |
| `CODE-19` | سجل قرار معماري | Architecture decision record | documented |  |
| `CODE-20` | الحتمي أولًا والنموذج للذيل | Deterministic first, model for the tail | documented |  |
| `CODE-21` | ذاكرة مؤقتة ببصمة المحتوى | Content-hash cache | documented | key:graphify |
| `CODE-22` | نظافة الإيداع وكلمات الحالة | Commit hygiene & status words | documented | git |
| `UI-01` | العرض الصامت: الواجهة تحكي | Silent product demo — the UI tells the story | documented |  |
| `UI-02` | ثلاثية النية والفعل والاستجابة | Intent → action → response with real latency | documented |  |
| `UI-03` | محتوى واجهة حقيقي ومحلي | Real, locale-correct UI content | documented |  |
| `UI-06` | عكس الواجهة للعربية | RTL product-UI mirroring | documented |  |
| `UI-07` | لوحة البيانات داخل الإطار | Dashboard composition for a frame | documented |  |
| `UI-08` | تشريح التفاعل الدقيق كوحدة مشهد | Microinteraction anatomy as a beat | documented |  |
| `UI-09` | مقطع حلقة لمكوّن واحد | Seamless UI component loop (3–6 s) | documented |  |
| `UI-10` | عناوين أفعال بسيطة في الشروحات | Plain action labels in tutorials | documented |  |
| `UI-13` | تصميم حركة المؤشر | Cursor choreography rules | documented |  |
| `UI-24` | تحكم وهدف يتغيران معًا | Control ↔ target live sync | documented |  |
| `UI-26` | طلب يُكتب ثم يُرسل ثم يولّد | Prompt type → submit → generate | documented |  |
| `UI-33` | جدول ردود الفعل الدقيقة | Micro-feedback timing table | documented |  |
| `UI-35` | ضغط وتحرير زر نابض | Press-release spring button | documented |  |
| `UI-47` | ثوابت الهاتف البارامتري | Parametric phone constants | documented |  |
| `UI-48` | منظور الجهاز وسرعة دورانه | Device perspective, rotation caps & idle hover | documented |  |
| `UI-49` | دخول الجهاز وكشف البطل | Device entrance & hero reveal | documented | npm:remotion |
| `UI-52` | تسليم بين جهازين | Two-device turntable handoff | documented |  |
| `UI-58` | جولة تمرير مع شروحات | Scroll tour with callouts | documented |  |
| `UI-59` | خطوط شرح قائدة | Callout leader lines | documented |  |
| `UI-61` | وصفة النقر وفتح نافذة | Click → modal recipe | documented | npm:remotion |
| `UI-62` | صفحة ويب مائلة تتمرر | 3D tilted webpage scroll & perspective pan | documented | npm:gsap |
| `UI-64` | عدسة تكبير التفاصيل | Magnifier lens pass | documented |  |
| `UI-75` | وصفة فيديو ميزة حقيقية | Real-feature video recipe | documented | ffmpeg, node, chromium |
| `UI-78` | فيديو تعليمي من ملف YAML | YAML-defined tutorial video | documented | docker |
| `UI-79` | رموز تصميم الواجهة وسلالمها | UI tokens & Refactoring-UI scales | documented |  |
| `UI-85` | مخططات مشاهد الواجهة | UI scene blueprints | documented |  |
| `UI-89` | قواعد صفحات الويب المسلَّمة | Web deliverable rules (landing, perf, hover gating) | documented |  |
| `UI-X01` | المؤشر بطلًا | Cursor as protagonist | documented | chromium |
| `UI-X02` | تسليم المجسم وطبقات منفجرة | Mockup hand-off and exploded layers | documented |  |
| `UI-15` | مؤشر ماك معبّر يتجه مع حركته | Expressive directional macOS cursor | seen | os:macos |
| `UI-16` | مؤشر بهالة لونية يلاحق هدفًا متحركًا | Cursor with accent halo homing on a live target | seen |  |
| `UI-23` | ضغط اختصار لوحة المفاتيح | Keycap shortcut trigger | seen |  |
| `UI-27` | وكيل ينجز قائمة مهام | Agent progress theater & tool-call checklist | seen | npm:hyperframes |
| `UI-30` | لوحة أوامر وبحث يصفّي النتائج | Command palette & search filter | seen |  |
| `UI-31` | إجابة متدفقة وسجل حي | Streaming answer & live log | seen |  |
| `UI-42` | إعادة ترتيب قائمة وسطور | FLIP list reorder & self-reordering lines | seen |  |
| `UI-53` | نافذة متصفح أو ماك وهمية | Browser chrome & macOS frame mock | seen | os:macos |
| `UI-60` | اقتراب يقوده المؤشر | Cursor-led push-in & focus zoom | seen |  |
| `UI-63` | جدار بطاقات واجهة يطفو بعمق | Floating UI card wall in depth | seen |  |
| `UI-65` | نقطة ساخنة مع فقاعة إرشاد | Hotspot tooltip walkthrough | seen |  |
| `UI-68` | شبكة بنتو للميزات | Bento feature grid | seen |  |
| `UI-70` | مربع تتبع وماسح ضوئي | AI tracking box & scanner brackets | seen | tesseract |
| `UI-71` | مسرح أداة تصميم ومقابض تحديد | Design-tool canvas, selection handles & size tags | seen |  |
| `UI-82` | ستايل برومو المنتج | Product promo style (neon prompt + glass orb) | seen |  |
| `UI-83` | واجهة ملصقات بظل صلب | Sticker UI with hard offset shadow | seen |  |
| `APPX-76` | كشف الوجوه | Face detection | install | pip:opencv, pip:onnxruntime, model:yunet |
| `APP-07` | أُطر الواجهات الحديثة | Modern front-end scaffolds (vite, react, next, svelte, tailwind) | install | npm:esbuild, npm:react |
| `APP-08` | تطبيقات بيانات سريعة | Data apps (streamlit, gradio) | install | python3 |
| `APP-13` | خادم ملفات محلي للمعاينة | Local static server for previews | install | node, python3, chromium, claude:tools |
| `APP-20` | CadQuery: برمجة قطع صلبة بارامترية وتصديرها STEP أو | CadQuery: Script parametric solid parts and export STEP/STL for 3D printing | install | pip:cadquery |
| `APP-21` | OpenSCAD: تحويل نماذج ‎.scad إلى STL أو PNG | OpenSCAD: Render .scad models to STL/PNG headlessly | install | openscad |
| `APP-22` | axe-core: فحص صفحة معروضة وفق قواعد WCAG والإبلاغ | axe-core: Run WCAG checks on a rendered page and report violations | install | chromium, npm:axe |
| `APP-23` | Pa11y: تدقيق الروابط أو ملفات HTML المحلية لإمكانية | Pa11y: Audit URLs or local HTML for accessibility from the CLI | install | npm:pa11y |
| `UI-17` | المؤشر المغناطيسي | Magnetic cursor & magnetic buttons | install | npm:hyperframes, lean |
| `UI-18` | سحب وإفلات | Cursor drag & drop | install | npm:hyperframes |
| `UI-19` | تحديد نص ومستطيل وقائمة يمين | Text select, marquee select & context menu | install | npm:hyperframes |
| `UI-20` | مؤشرات متعاونين بأسمائها | Named multiplayer cursors | install | npm:hyperframes |
| `UI-21` | مؤشر وكيل ذكي | AI agent cursor | install | npm:hyperframes |
| `UI-22` | مؤشر اللمس على الهاتف | Touch indicator: tap & swipe | install | npm:hyperframes |
| `UI-28` | محادثة: فقاعات وكتابة جارية | Chat thread, bubbles & typing dots | install | npm:hyperframes |
| `UI-29` | طرفية ومحرر كود | Terminal & IDE scenes (24 theme blocks) | install | npm:hyperframes, os:macos |
| `UI-32` | كتابة في تطبيق الملاحظات | Notes-app typing story | install | npm:hyperframes |
| `UI-36` | قلب المفتاح وتبديل الثيم | Toggle flip & theme switch | install | npm:hyperframes |
| `UI-37` | من التحميل إلى علامة صح | Spinner → success check | install | npm:hyperframes |
| `UI-38` | حقل إدخال: خطأ واهتزاز ونجاح | Input feedback: error shake & valid state | install | npm:hyperframes |
| `UI-39` | هيكل لامع يتحول إلى محتوى | Skeleton shimmer → content | install | npm:hyperframes |
| `UI-40` | إشعارات: نظام وجزيرة ورصّة | Notifications: native pop, dynamic island, stacks | install | npm:hyperframes, os:macos |
| `UI-41` | تحول بطاقة إلى لوحة (FLIP) | Shared-element morph: card → panel (FLIP) | install | npm:hyperframes |
| `UI-51` | مكوّن Device في Remotion | Remotion Device component | install | npm:remotion, npm:react |
| `UI-54` | مروحة أجهزة وانفراد الهواتف | Multi-device splay & phone fan-out | install | npm:hyperframes |
| `UI-55` | آيفون وماك بوك ثلاثيا الأبعاد بشاشات حية | 3D GLTF iPhone & MacBook with live screens | install | chromium, npm:three, npm:gsap, npm:hyperframes |
| `UI-66` | مقارنة قبل وبعد | Before/after wipe & comparison split | install | npm:hyperframes |
| `UI-67` | دوار الشاشات والموكاب الثابت | Screen-flow carousel & sticky mock swap | install | npm:hyperframes |
| `UI-73` | التقاط موقع إلى فيديو | Website capture → video | install | chromium, npm:hyperframes, npm:lottie |
| `UI-77` | تسجيل المتصفح بمؤشر ولوحة لقطات | Browser recording CLI with cursor & contact sheet | install | ffmpeg, node, chromium |
| `UI-84` | مكتبة مكوّنات HyperFrames للواجهات | HyperFrames UI component registry | install | npm:hyperframes |
| `UI-X04` | رموز الحركة وصقل الواجهة | Motion tokens and interface polish (React UIs) | install | npm:animejs, npm:react |
| `APP-01` | نشر صفحة تفاعلية خاصة | Publish a private interactive page (Artifact) | key | npm:react, claude:tools |
| `APP-02` | قدرات الصفحة أثناء التشغيل | Artifact runtime capabilities | key | key:unspecified |
| `APP-03` | صفوف وتعليقات الصفحة | ArtifactData and ArtifactComments tools | key | claude:tools |
| `APP-12` | تطبيقات تستدعي Claude عبر API | Apps that call Claude via the API | key | node, pip:anthropic, key:unspecified |
| `APP-14` | بناء مواقع بالذكاء الاصطناعي (مدفوع) | Hosted website builder (Higgsfield, paid) | key | pip:higgsfield, key:unspecified |
| `CODE-17` | مراجعة طلب دمج بفريق وكلاء | PR review fan-out | key | gh, mcp:github, key:unspecified |
| `UI-76` | من فيجما إلى طبقات متحركة | Figma frame → animatable layers | key | key:unspecified |
| `UI-46` | لحظة احتفال توقيعية | Signature celebration moment | idea |  |
| `UI-57` | قلب الهاتف وتبديل الشاشة | Phone flip with mid-swap | idea |  |
