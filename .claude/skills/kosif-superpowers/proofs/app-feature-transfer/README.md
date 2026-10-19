# app-feature-transfer — مزايا CapCut وCanva وPremiere بأدوات مفتوحة (2026-10-18)

<div dir="rtl">

**ماذا يثبت:** `smoke.py` يعيد بناء 17 ميزة من مزايا المحررات الثلاثة بأدوات مفتوحة (FFmpeg وNumPy وOpenCV وfaster-whisper) على وسائط مولّدة، ولكل ميزة شرط قابل للقياس: مدة، أو علوّ صوت بوحدة LUFS، أو مواضع القطعات، أو IoU للقناع، أو كلمات مفرّغة بتوقيتها. النتيجة 17/17 على Windows 11 (`results.json`). أول تشغيل نجح فيه 11 فقط؛ الإخفاقات الستة كانت أخطاء في الاختبار نفسه (عرض قصّ فردي، و`-v error` يخفي إحصاءات astats، ومقياس حواف لا يناسب التكبير، وتعبير قصّ لكل إطار يتجاوز محلل FFmpeg، و`drawbox` لا يقبل متغيّر الزمن هنا) وأصلحت قبل منح الشارة ✅.

**ما لا يثبته:** هذه ليست نماذج CapCut أو Adobe (مثل Enhance Speech أو إزالة الخلفية بالذكاء الاصطناعي)، بل بدائل كلاسيكية مفتوحة تحقق النتيجة نفسها على حالات الاختبار. لم يُنسخ أي كود من التطبيقات.

</div>

**What it proves:** `smoke.py` rebuilds 17 editor features with open tools on synthetic media and checks a measurable postcondition for each (duration, LUFS, cut times, mask IoU, timed transcript). 17/17 on Windows 11, FFmpeg 8 build, Python 3.13 — see `results.json`. Rerun: `python smoke.py` (needs ffmpeg/ffprobe, numpy, opencv-python; faster-whisper with a cached `base.en` model and a local TTS for APPX-13).

| id | feature (seen in) | postcondition checked |
|---|---|---|
| APPX-01 | speed curve (CapCut) | 2 s@1× + 2 s@0.5× + 2 s@2× = 7.0 s ±0.15 |
| APPX-02 | chroma key (CapCut, Premiere) | no key colour left, subject kept |
| APPX-03 | auto reframe 9:16 (Premiere Auto Reframe, CapCut) | moving subject stays inside the 404×720 crop |
| APPX-04 | scene edit detection (Premiere) | cuts found at 1.5 s and 3.0 s ±0.1 |
| APPX-05 | loudness to −14 LUFS (both) | integrated −14.0 LUFS |
| APPX-06 | LUT look (CapCut filters, Lumetri) | grey → R>G>B after warm .cube |
| APPX-07 | remove pauses (CapCut) | 1.5 s pause found at 1.0–2.5 s, clip 3.5 → 2.5 s |
| APPX-08 | beat markers (CapCut) | 8 beats, 120 BPM ±2 |
| APPX-09 | camera bubble over screen recording (Canva recording studio) | round mask: centre camera, corner screen |
| APPX-10 | keyframed punch-in (both) | subject area ×2.16 for zoom 1.5 |
| APPX-11 | auto ducking (both) | music bed −8 dB or more under the voice |
| APPX-12 | speech noise reduction (both) | noise above 3 kHz −7.6 dB |
| APPX-13 | auto captions with word timing (CapCut, Premiere Speech to Text) | transcript contains the spoken words, monotonic SRT |
| APPX-14 | background removal on a still (CapCut, Canva) | IoU 0.93 with the true subject |
| APPX-15 | EDL interchange + conform (Premiere) | 2 events conformed to 2.50 s |
| APPX-16 | reverse + freeze frame (CapCut) | 3.0 s, first frame = source end |
| APPX-17 | automatic cover pick (CapCut, Canva) | sharpest/most colourful frame saved |

## Second batch — photo, type, vector, procedural, download (2026-10-19)

<div dir="rtl">

**ماذا يثبت:** `smoke_studio.py` يعيد بناء 20 ميزة من برامج الدفعة الثانية (DxO PhotoLab وCapture One وJPEGmini وFontLab وAffinity وHoudini وIDM وAnimate) بأدوات مفتوحة، ولكل ميزة شرط قابل للقياس: PSNR أو SSIM أو خطأ الزوايا بالبكسل أو قيمة التقنين في GPOS أو SHA-256 للتنزيل أو ترتيب المهام. النتيجة 20/20 (`results_studio.json`). أول تشغيل نجح فيه 16، وكانت الإخفاقات الأربعة أخطاء في الاختبارات نفسها: شكل مصفوفة HoughLinesP في OpenCV 4.12، وقيمة غير متسقة في الإعداد المسبق، وإدخال float إلى Mertens بدل 8-bit، وعتبة SSIM مطلقة على نسيج ضوضاء. أُصلحت كلها قبل منح ✅.

**ما لا يثبته:** هذه ليست خوارزميات DxO (DeepPRIME وClearView Plus) ولا مقياس JPEGmini، بل طرق كلاسيكية منشورة (القناة الداكنة وNL-means وSSIM وHomography) تصل إلى نتيجة مقيسة مماثلة على بيانات اصطناعية.

</div>

| id | feature (seen in) | postcondition checked |
|---|---|---|
| APPX-31 | dehaze (DxO ClearView) | PSNR vs haze-free +4 dB, contrast ×2.5 |
| APPX-32 | tiered denoise (DxO `NoiseRemovalMethod`) | PSNR noisy 23.2 → 30 dB |
| APPX-33 | auto keystone (DxO Perspective `KeystoningAutoMode`) | corner error 1 px, restored PSNR 32 dB |
| APPX-34 | lens distortion (DxO Distortion, Affinity lens data) | PSNR 21 → 34.5 dB |
| APPX-35 | lateral CA (DxO ChromaticAberration) | channel scales recovered, PSNR 26 → 36 dB |
| APPX-36 | WB + tone curve + HSL (DxO, Capture One presets) | channel-mean spread 43.9 → 0 |
| APPX-37 | film grain + vignette (Capture One Presets60, DxO) | corner ×0.59, grain σ 7 |
| APPX-38 | watermark (DxO Watermark) | 40% opacity within 0.2 levels |
| APPX-39 | perceptual JPEG (JPEGmini) | 64% smaller within 0.01 SSIM of q95 |
| APPX-40 | contact sheet (Capture One PrintTemplates) | 14 images → 2 PDF pages |
| APPX-41 | versioned presets (Capture One Styles, DxO Compatibility.V*) | old schema migrates to the same pixels |
| APPX-42 | XMP sidecar (Lightroom, ACDSee, DxO, Affinity libxmp) | rating, label, Arabic keyword read back |
| APPX-43 | auto horizon (DxO Horizon, Capture One AutoCrop) | 3.49° found for 3.5°, residual 0.00° |
| APPX-44 | font with kerning (FontLab) | TTF saved, GPOS kern A/V −80 |
| APPX-45 | vector booleans (Affinity libgeometry, Houdini he_boolean) | areas exact, SVG written |
| APPX-46 | CHOP-style channels (Houdini Lag/Noise/Cycle/Envelope) | lag reaches 63% at τ |
| APPX-47 | task graph with cache (Houdini PDG) | rerun 0 tasks; one change reruns 2 |
| APPX-48 | segmented resumable download (IDM) | 6 ranged parts, resume, SHA-256 match |
| APPX-49 | tween, onion skin, sprite sheet (Animate) | keys hit, eased speed, 6×4 sheet + JSON |
| APPX-50 | exposure fusion (DxO Smart Lighting) | clipped highlights 65% → 2.4% |

Rerun: `python smoke_studio.py` (numpy, opencv-python, pillow, fontTools, shapely; the download check runs a local HTTP server on 127.0.0.1 only).
