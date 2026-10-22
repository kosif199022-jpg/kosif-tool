# مصمم — محرر صور عربي أولًا / Mosamem, the Arabic-first image editor

مرجع حقائق فقط، تم التحقق منه في 2026-10-22 على نسخة المصدر `becfbe8` (الإصدار 0.1.0). Facts only, checked 2026-10-22 against source commit `becfbe8` (version 0.1.0).

- المستودع / repository: https://github.com/motalim-ai/mosamem
- الصانع / made by: Motalim (https://www.youtube.com/@motalim-ai)
- الرخصة / licence: **GPL-3.0-or-later**

## الفهرس / contents

1. [الرخصة: رابط فقط / Licence: link only](#الرخصة-رابط-فقط--licence-link-only)
2. [ما يفعله / What it does](#ما-يفعله--what-it-does)
3. [النماذج المحلية / Local AI models](#النماذج-المحلية--local-ai-models)
4. [ما تحققنا منه هنا / What was verified here](#ما-تحققنا-منه-هنا--what-was-verified-here)
5. [ماذا تفعل القدرات الخارقة به / What Superpowers can do with it](#ماذا-تفعل-القدرات-الخارقة-به--what-superpowers-can-do-with-it)
6. [علاقته بـ image_local_ai.py / How image_local_ai.py relates](#علاقته-بـ-image_local_aipy--how-image_local_aipy-relates)

## الرخصة: رابط فقط / Licence: link only

مستودع kosif-tool برخصة MIT، ومصمم برخصة GPL-3. لذلك **لا نسخ لأي كود من مصمم** إلى هذا المستودع: نصف ونربط وننسب فقط. الحقائق العامة (أسماء النماذج، روابطها، أحجامها، بصماتها SHA-256، رخصها) ليست كودًا، ونعيد ذكرها مع نسبتها إلى `src-tauri/src/ai/models.rs`.

kosif-tool is MIT; Mosamem is GPL-3. **No Mosamem code is copied into this repository**: describe, link and credit only. Public facts (model names, URLs, sizes, SHA-256 pins, licences) are not code; they are restated here with credit to `src-tauri/src/ai/models.rs`. The bundled fonts and the models keep their own licences (OFL 1.1, MIT, Apache-2.0), and the name "Mosamem" and its icon are not covered by its licence.

## ما يفعله / What it does

محرر صور سطح مكتب (Rust وTauri وSvelte) لماك (Apple silicon، macOS 13.4+) وويندوز 10/11، واجهته عربية من اليمين مع زر للإنجليزية. النسخة 0.1 تجريبية أولى بُنيت في يوم واحد؛ ما اكتمل وما لم يكتمل في `docs/status.md`.

A desktop image editor (Rust, Tauri, Svelte) for Mac (Apple silicon, macOS 13.4+) and Windows 10/11, Arabic RTL interface with English one click away. 0.1 is a first beta built in a single day; `docs/status.md` lists what is done and what is not.

| المجال / area | ما يقدمه / what it offers |
|---|---|
| الطبقات / layers | groups, blend modes, opacity and fill, clipping, locks, layer masks |
| تعديلات غير مدمّرة / non-destructive adjustments | Levels, Curves, Hue/Saturation, Brightness/Contrast, Exposure, Vibrance, Color Balance, Black & White, Gradient Map, Invert, Threshold |
| التحديد / selections | marquee, lasso, polygon lasso, magic wand, quick selection, object selection, refine edge |
| الرسم / painting | brush, eraser, clone stamp, healing and spot healing, gradient, paint bucket |
| النص العربي / Arabic text | HarfRust shaping, RTL and mixed text, diacritics, kashida justification, four OFL fonts (IBM Plex Sans Arabic, Cairo, Tajawal, Amiri); text stays editable |
| الأشكال والقلم / shapes and the Pen | rectangle, ellipse, polygon, star, line, Pen and Direct Selection with editable fill and stroke |
| أنماط الطبقات / layer styles | drop and inner shadow, outer glow, stroke, colour and gradient overlay |
| PSD | opens layered PSD and saves a layered copy (via ag-psd, MIT); limits in `docs/psd-report.md` |
| ذكاء محلي / local AI | Select Subject, Remove Background, Object Selection (click or box), Smart Fill, via ONNX Runtime |
| التصدير / export | PNG, JPEG, WebP, TIFF, HEIC (Mac): whole image, one layer or the selection |

الخصوصية: لا يرسل الصور لأي جهة، بلا تحليلات ولا حساب؛ الاستخدام الوحيد للشبكة تنزيل النموذج مرة واحدة بعد الموافقة. Privacy: pictures never leave the machine; the only network use is a one-time, consented model download (upstream test `tools/ai/no-network.sh`).

## النماذج المحلية / Local AI models

كل ملف مثبت على commit ويُتحقق من بصمته قبل الاستخدام. Each file is pinned to a commit and checked by SHA-256 before use.

| الميزة / feature | النموذج / model | الرخصة / licence | الملفات والحجم / files, size | SHA-256 (first file) |
|---|---|---|---|---|
| Select Subject, Remove Background | BiRefNet lite (ONNX, onnx-community) | MIT | `birefnet_lite_fp16.onnx`, 114,538,221 B | `d39b897c…bfec402` |
| Object Selection | SAM 2.1 hiera-tiny (ONNX, onnx-community) | Apache-2.0 | 4 files (encoder + decoder, each with `_data`), 88,491,751 B | `7773e79d…ecbd50a` |
| Smart Fill | MI-GAN pipeline v2 (Picsart AI Research) | MIT (code and weights) | `migan_pipeline_v2.onnx`, 28,079,181 B | `6f1f3530…a48c40b` |

الروابط الكاملة والبصمات الكاملة: `python3 scripts/image_local_ai.py models` (أو `--json`). Full URLs and digests: `python3 scripts/image_local_ai.py models` (or `--json`).

## ما تحققنا منه هنا / What was verified here

`cargo test -p mosamem-core` ran on 2026-10-22 outside this repository (cargo 1.97.0, commit `becfbe8`): **95 passed, 0 failed** — 86 unit tests (adjust 15, filter 9, heal 2, inpaint 1, paint 8, resample 7, select 11, style 7, text 13, vector 13) and 9 blend-formula tests. The 13 text tests are the shaping and layout goldens: joining forms, lam-alef ligature, stacked diacritics, mixed Arabic/Latin order, mirrored brackets, kashida justification (also with contextual fonts), font fallback, digit styles, box wrapping. An `--offline` attempt failed first because the crates were not cached; the online run fetched them through the proxy. The desktop app (`src-tauri`), PSD round-trip and the AI features were **not** run here: those remain upstream claims (📄).

## ماذا تفعل القدرات الخارقة به / What Superpowers can do with it

- **التوجيه / routing:** when a user wants a free, Arabic-first Photoshop-like editor, layered PSD opening, or on-device background removal without an account, point them to Mosamem's release page (powers MEDIA-38 to MEDIA-41, ARAB-91, ARAB-92).
- **مرجع للرياضيات / a specification:** its tests document blend-mode, adjustment and Arabic-shaping behaviour; read them as a specification, re-implement in MIT code from public formulas if needed, never copy.
- **الخطوط / fonts:** the four Arabic fonts are OFL 1.1; take them from their own upstream repositories with their `OFL.txt`.
- **الذكاء المحلي داخل KOSIF / local AI inside KOSIF:** use `image_local_ai.py` (below) with a model file the user chose to download.
- **حدود / limits:** do not claim Mosamem is installed, that its AI ran here, or that its PSD export matches Photoshop.

## علاقته بـ image_local_ai.py / How image_local_ai.py relates

`scripts/image_local_ai.py` هو تنفيذ مستقل برخصة MIT لنفس فكرة «نماذج مفتوحة على الجهاز»؛ لا يحتوي كودًا من مصمم. يقرأ نموذج ONNX يحدده المستخدم، ولا ينزّل أي شيء أبدًا: إن غاب النموذج يطبع الرابط المثبت ويطلب من المستخدم تنزيله بنفسه.

`scripts/image_local_ai.py` is an independent MIT implementation of the same on-device idea; it contains no Mosamem code. It loads an ONNX file the user supplies and never downloads: with no model it prints the pinned URL and exits 2.

| command | does | model I/O it expects |
|---|---|---|
| `models [--json]` | lists the three models with licence, source, size, pinned URL and SHA-256 | — |
| `verify-model FILE [--sha256 HEX]` | SHA-256 check; defaults to the known pin by file name; exit 1 on mismatch | — |
| `remove-bg --model M in.png out.png` | ImageNet-normalised RGB at the model's side (default 1024), sigmoid of the first output, soft alpha → RGBA PNG | float32 `[1,3,S,S]` → `[1,1,S,S]` logits |
| `inpaint --model M --mask hole.png in.png out.png` | grows the hole ~2 model px, runs the model, pastes back only the user's hole | `image` uint8 `[1,3,H,W]`, `mask` uint8 `[1,1,H,W]` (255 keep, 0 fill) → `result` |

Tests (`evals/test_image_local_ai.py`) build tiny synthetic ONNX graphs inside the test, so no real model is needed; they check behaviour and I/O, not the quality of BiRefNet or MI-GAN. SAM 2.1 is listed but not wrapped.
