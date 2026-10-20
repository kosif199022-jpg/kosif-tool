# الدفعة الرابعة: Paint.NET وPhotoshop 2025 والرسّام وBlender بأداة REA (2026-10-20)

<div dir="rtl">

## بالعربية

**ماذا يثبت:** شُغّل REA v6.7.0 (من سطر الأوامر، لأن خادم MCP انقطع عند إعادة الاتصال) على أربعة أهداف في هذا الحاسوب، وتحوّلت ميزاتها إلى قدرات تعمل على ملفات المستخدم:

| الهدف | الطريق | ما قرأناه (أسماء فقط) | صار |
|---|---|---|---|
| Paint.NET 4.2.13 (مثبّت في مجلد المالك) | `installer_triage scan` → NSIS → `unpack` → `PaintDotNet_x64.msi` (`7z -tCompound`) → CAB → 314 ملفًا | REA `inspect_managed_artifact`: الملف `_1C3F…AC` هو `PaintDotNet.Effects.dll` 4.213.7521.38873؛ `inspect-managed-members`: 152 نوعًا منها 64 مؤثرًا (OilPainting وInkSketch وPencilSketch وTwist وBulge وPolarInversion وDents وFrostedGlass وTile وZoomBlur وRadialBlur وMotionBlur وSurfaceBlur وUnfocus وFragment وMedian وEmboss وRelief وEdgeDetect وOutline وPixelate وCrystalize وGlow وSoftenPortrait وJulia/MandelbrotFractal وLevels وCurves وPosterize وSepia وInvertColors وAutoLevel وAddNoise…) ومعاملاتها (BrushSize وCoarseness وInkOutline وColoring وPencilTipSize…) | APPX-99…104: ‏30 مؤثرًا وتوليد كسيريات |
| Photoshop 2025 ‏26.1 (حزمة دون اتصال) | `scan` → `adobe-offline-package PHSP 26.1` وتبعياتها | 8,284 اسم ملف: 14 مرشّح ‎.8bf (Liquify وLens Blur وAdaptive Wide Angle وVanishingPoint…) و27 LUT في Presets/3DLUTs و27 مجلد نماذج sensei و8 SuperCaf (Select_Subject وDepthPrediction وCMGAN وTiledCMGANSR وWire وPeopleDistractor…) وSky_Presets | APPX-105…109 وصفات مفتوحة، APPX-118 خريطة الذكاء 📄 |
| الرسّام Microsoft Paint ‏11.2605.81.0 (مثبّت) | قراءة فقط داخل WindowsApps | REA على `PaintUI.winmd`: ‏588 نوعًا؛ `AIFeature = Cocreator, ImageCreator, GenerativeFill, StickerGenerator, Reimagine, ColoringBook`؛ `ToolKind`؛ ومن `PaintTools.dll`: CalligraphicTool وAirBrushTool وMagicEraserTool وObjectSelectTool وFloodFillOperation وطبقات `LayerStack`؛ ونماذج ONNX على الجهاز (seg وinseg وmager) | APPX-110…113 وصفات، APPX-119 خريطة 📄 |
| Blender ‏5.2.2 LTS (نسخة محمولة في ‎~/KOSIF-Tools/Blender5.2) | REA `analyze` على المجلد (إسقاط JavaScript: 64 ملف JS/JSON، بلا Electron) و`inspect-pe-resources` على blender.exe (113 MB: ‏20 موردًا) ثم جرد bpy الحي | 2,499 مشغّلًا و4,023 نوعًا و102 عقدة تظليل و92 مركّبًا و274 هندسية، 4 سماوات (Multiple Scattering…)، 7 عدسات بانورامية، مركّب Blender 5 (`scene.compositing_node_group`) | APPX-114…117 مثبتة برندرات Cycles حقيقية |

**ما لم نفعله:** لم يُشغَّل أي مثبّت أو تطبيق هدف. **Windows Defender يحجب `Set-up.exe` في مجلد Photoshop 2025** (وكذلك ملفات Patch وKeyGen في مجلدات أخرى، وsetup في Lightroom)، فتركناه كما هو؛ وصار `installer_triage.py` يبلّغ عن هذا (`unreadable` / `antivirus`) بدل أن يتوقف. مجلدات SketchBook وFilmPack وXara لا تحوي إلا ملفات Crack/Patch، فلم تُفتح. لم يُنسخ أي كود أو نموذج أو LUT أو preset من أي تطبيق.

**النتائج على الجهاز (Windows 11، معالج i7-1165G7 دون GPU):**

- `evals/test_app_studio_paint.py`: ‏12 اختبارًا و71 حالة فرعية تنجح؛ كل مؤثر يقيس شرطه (مثلًا: posterize ≤ N قيمة، invert يعود بالعكس، الالتواء لا يغيّر ما خارج نصف القطر، كل خلية بكسلة ثابتة، LUT الهوية يعيد الصورة، ملف ‎.ora يبدأ بـ mimetype غير مضغوط، lens-blur يحفظ حدة مستوى التركيز).
- `evals/test_blender_cinema.py`: ‏7 اختبارات تنجح مع Blender 5.2.2 (جرد، رندر neon-night وgolden-hour، ودوران متحرك إلى MP4 مع ‎.blend).
- رندرات 640×360 بـ 24 عينة: product-hero ‏10.6 ث، golden-hour ‏15.5 ث، noir-volumetric ‏20.2 ث، neon-night ‏22.4 ث، anamorphic-epic ‏7.1 ث (2.39:1). دوران 12 إطارًا → H.264 ‏320×180 في 19 ث.

**أخطاء كشفها الإثبات وأُصلحت:** هالة حول الأفق في استبدال السماء (التنعيم كان يمدّ السماء القديمة فوق المباني)؛ قناع السماء يأكل مبنى أزرق (صار النمو مقيّدًا بإحصاء لون السماء)؛ lens-blur كان يغبّش مستوى التركيز نفسه إلى 40% من حدته (صار يمزج الأصل حيث دائرة التشتت < 2 بكسل)؛ ضباب عالمي في golden-hour سوّد الصورة (حجم العالم لا نهائي؛ صار صندوقًا محدودًا)؛ التركيز على مركز الصندوق بدل مقدمة الموضوع.

**حدود صادقة:** المؤثرات وصفات مفتوحة تعطي نتيجة مشابهة مقيسة، لا مطابقة لخوارزمية Paint.NET أو Adobe؛ ميزات الذكاء التوليدي (Generative Fill وCocreator وSuper Zoom) غير منقولة؛ مبنى بلون السماء تمامًا قد يُعدّ سماء؛ الرندر على CPU بطيء للجودة final (512 عينة).

</div>

## English

| Target | Route | REA / listing evidence (names only) | Became |
|---|---|---|---|
| Paint.NET 4.2.13 | triage → NSIS → 7-Zip → MSI as compound file → CAB | `PaintDotNet.Effects.dll` 4.213: 152 types, 64 `*Effect`, property names | APPX-99…104 (30 effects + 2 fractals) |
| Photoshop 2025 26.1 offline package | triage → `adobe-offline-package`; ZIP names | 14 filter plug-ins, 27 LUTs, 35 AI-model folders, Sky_Presets | APPX-105…109, APPX-118 (📄) |
| Microsoft Paint 11.2605.81.0 | read-only, `PaintUI.winmd` with REA | 588 types, `AIFeature`, `ToolKind`, brush tool classes, ONNX models | APPX-110…113, APPX-119 (📄) |
| Blender 5.2.2 LTS (portable) | REA `analyze` + `inspect-pe-resources`; live bpy inventory | 2,499 operators, 4,023 types, node-group compositor | APPX-114…117, Cycles render receipts |

Evidence: [`runs_2026-10-20.json`](runs_2026-10-20.json) (REA evidence ids, type names, counts, SHA-256 of every render).
Sheets: [Blender presets](paint_blender_2026-10-20/blender_presets.jpg) · [Paint.NET effects](paint_blender_2026-10-20/paintnet_effects.jpg) · [Photoshop and MS Paint ops](paint_blender_2026-10-20/photoshop_mspaint_ops.jpg).

**Rerun:**

```bash
python scripts/installer_triage.py scan "<Photoshop folder>"          # Set-up.exe → unreadable/antivirus
node <rea-agents>/scripts/rea.mjs inspect-managed-members <PaintDotNet.Effects.dll> --json
node <rea-agents>/scripts/rea.mjs inspect-managed-members "<Paint>/PaintUI.winmd" --json
python scripts/blender_cinema.py inventory -o blender.json
python scripts/blender_cinema.py render --preset neon-night --res 640x360 --quality preview --samples 24 -o neon.png
python -m pytest evals/test_app_studio_paint.py evals/test_blender_cinema.py -q
```

**What it does not prove:** that any recipe matches the vendor's algorithm, or anything about the generative AI features; render timings are for this CPU only.
