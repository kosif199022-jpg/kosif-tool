# Canva 1.126.1 — design capabilities (2026-10-19)

<div dir="rtl">

**ماذا يثبت:** فُكّ مثبّت Canva الموجود في مجلد المالك مرة ثانية بـ `installer_triage.py unpack --authorized` (7-Zip، بلا تشغيل)، ثم عُدّت كلمات ميزات التصميم في ملفات `app.asar` النصية (998 ملفًا، فُحص منها 822). في المرة الأولى (2026-10-18) سُجّلت قدرات الغلاف فقط: النوافذ والتسجيل والجسر والمصهرات. أما هذه المرة فكانت مراسي محرر التصميم نفسه، وكل منها صار عملية في `scripts/app_studio.py` مثبتة في `evals/test_app_studio.py`.

**ما لم نفعله:** لم يُشغَّل Canva، ولم يُنسخ منه أي سطر كود. ما سُجّل هنا أسماء ومعرّفات وأعداد فقط، والتنفيذ كله أصلي بأدوات مفتوحة.

</div>

| Anchor in `app.asar` (names and counts only) | Where | Became |
|---|---|---|
| `bleedMicrons`, `backgroundBleed`, `setBackgroundBleed`, `resizeBleedBackground` (bleed ×72) | `dist/main.js` | `print-pdf` (APPX-97) |
| “crop marks”, “PDF Print” in the export dialog | `*.strings.js` (every UI language) | `print-pdf` |
| `rgbToCmykColorMappings`, `cmykColor`, `spotColorCmykAlternative` | `main.js` | `print-pdf cmyk=1 profile=` |
| `DUOTONE` | `main.js` | `duotone` (APPX-90), image filter in `design` |
| `Collage`, `collage_` (×16) | renderer bundle | `collage` (APPX-91) |
| `PHOTO_TO_MOCKUP`, `MockupBundle`, `mockupTemplateIds`, `previewMockupBundleId` | `main.js` | `mockup` (APPX-92) |
| QR encoder (“qr code” ×12) | vendor bundle | `qr` (APPX-93, decoded back to verify) |
| `presentationml`, `Presentations`, `PRESENTATION_PHOTO_AND_VIDEO_ANIMATIONS` | `main.js`, renderer | `pptx` (APPX-96), `text-anim` (APPX-98) |
| “Transparent background” download option | `*.strings.js` | `remove-bg` → transparent PNG (APPX-14) |
| template ×215, element ×303, shadow ×356, outline ×262, font ×2,159, rtl ×714, arabic ×113 | all text entries | `design` template engine with Arabic text effects (APPX-88) |
| resize ×122 | all text entries | `resize-design` Magic Resize (APPX-89) |
| brand ×205, chart ×17 | all text entries | `palette` (APPX-94), `chart` (APPX-95) |
| Whiteboards (×29) | renderer | not rebuilt (real-time collaboration) |

**What it does not prove:** that these anchors are Canva's server-side features or how Canva implements them; counts include ordinary uses of common words. Canva's AI features (Magic Design, Magic Expand, Background Remover's model) are not reproduced; `remove-bg` is classical GrabCut and is checked against a known mask (IoU > 0.85).

Found while proving: Cairo, Lalezar and Tajawal lack some Arabic presentation forms (isolated alef, teh, seen), and Aref Ruqaa / Reem Kufi have none. Without libraqm those letters would draw as empty boxes. `app_studio.py` now maps a missing isolated form to its base letter and falls back to the bundled Amiri when other forms are missing. matplotlib 3.11 shapes Arabic itself, so `chart` passes text through there and reshapes only on older versions.
