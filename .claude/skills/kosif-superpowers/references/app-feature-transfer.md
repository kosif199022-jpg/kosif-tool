# قدرات التطبيقات المحللة — Analyzed app capabilities (APPX)

<div dir="rtl">

**من أين جاءت:** في 2026-10-18 حُللت ثلاثة مثبّتات وضعها المالك في مجلد العمل بأداة REA v6.7.0 وأداة `scripts/installer_triage.py`، بلا تشغيل أي منها: CapCut وCanva 1.126.1 وAdobe Premiere Pro. السجل الكامل في [proofs/windows-installers-rea](../proofs/windows-installers-rea/README.md). كل ميزة وجدناها صارت قدرة في عائلة [app-feature-transfer](powers/app-feature-transfer.md) (APPX-01…APPX-30)، ومعها وصفة مفتوحة تبنيها أنت.

**القاعدة:** نستلهم الميزة ولا ننسخ الكود. لا يدخل هذا المستودع أي سطر من كود Canva أو CapCut أو Adobe أو DxO أو Phase One أو غيرها؛ ولا تُشغَّل أو تُفتح أدوات الكسر (Crack وPatch وKeyGen) أبدًا؛ نسجّل الحقيقة البنيوية (اسم نافذة، مرساة API، امتداد ملف) ثم نكتب تنفيذًا أصليًا بأدوات مفتوحة ونثبته باختبار قابل للقياس.

</div>

## الفهرس / contents

1. [What each installer really is](#1-what-each-installer-really-is)
2. [Video-editor features → proven open recipes](#2-video-editor-features--proven-open-recipes)
3. [Canva desktop: evidence from its own bytes](#3-canva-desktop-evidence-from-its-own-bytes)
4. [Installer architecture](#4-installer-architecture)
5. [How to use this family](#5-how-to-use-this-family)
6. [Second batch: photo developers, type, vector, procedural, download](#6-second-batch-2026-10-19-photo-developers-type-vector-procedural-download)
7. [App Studio — run every feature on the user's own files (requirements)](#7-app-studio--run-every-feature-on-the-users-own-files)
9. [Global video platforms and two original workflow adapters](#9-global-video-platforms-and-two-original-workflow-adapters-2026-10-19)

## 1. What each installer really is

| | CapCut | Canva 1.126.1 | Adobe Premiere Pro |
|---|---|---|---|
| File | 2.9 MB, signed Bytedance Pte. Ltd. | 213.6 MB, signed Canva | 3.4 MB, signed Adobe Inc. |
| Installer | NSIS-3 Unicode | NSIS-3 Unicode | UPX-packed "Creative Cloud Set-up" (Adobe Installer 2.14.0.43) |
| Payload | `res.zip` (installer skin, 23 languages) + `shell_downloader.dll`, `downloader_nsis_plugin.dll`, `BgWorker.dll` | `app-64.7z` + `app-32.7z` → Electron app, `resources/app.asar` (23 MB, 998 files) | none: the product is downloaded by Creative Cloud |
| What we can learn | installer architecture only | the whole desktop shell | installer architecture only |

So the **editor** features of CapCut and Premiere are *not* in these files. They are listed below from the vendors' public product documentation and marked as such; the open recipe that rebuilds each one was proved here on synthetic media ([proofs/app-feature-transfer](../proofs/app-feature-transfer/README.md), 17/17).

## 2. Video-editor features → proven open recipes

| Feature (app) | Power | Recipe in one line |
|---|---|---|
| Speed curve (CapCut) | APPX-01 ✅ | trim + `setpts` per segment + concat |
| Chroma key (CapCut, Premiere Ultra Key) | APPX-02 ✅ | `chromakey` + `overlay` |
| Auto reframe 9:16 (Premiere, CapCut) | APPX-03 ✅ | OpenCV subject centroid → smoothed crop → raw pipe to x264 |
| Scene edit detection (Premiere) | APPX-04 ✅ | `select='gt(scene,0.3)',showinfo` |
| Loudness −14 LUFS (both) | APPX-05 ✅ | `loudnorm` then `ebur128` check |
| Filters / Lumetri looks | APPX-06 ✅ | generated `.cube` + `lut3d` |
| Remove pauses (CapCut) | APPX-07 ✅ | `silencedetect` → `silenceremove` keeping a 0.5 s breath |
| Auto beat (CapCut) | APPX-08 ✅ | energy flux peaks → BPM |
| Keyframed punch-in (both) | APPX-10 ✅ | `zoompan` (+ EASE curves) |
| Auto ducking (both) | APPX-11 ✅ | `sidechaincompress` |
| Enhance Speech / reduce noise | APPX-12 ✅ | `afftdn` + high-pass (classic DSP, not Adobe's model) |
| Auto captions / Speech to Text | APPX-13 ✅ | faster-whisper word timestamps → SRT |
| Remove background (CapCut, Canva) | APPX-14 ✅ | GrabCut (rembg 📦 for hair) |
| EDL / project interchange (Premiere) | APPX-15 ✅ | CMX3600 writer + ffmpeg conform |
| Reverse + freeze (CapCut) | APPX-16 ✅ | `reverse` + `tpad=stop_mode=clone` |
| Cover suggestion (CapCut, Canva) | APPX-17 ✅ | Laplacian sharpness + colourfulness |

## 3. Canva desktop: evidence from its own bytes

From `installer_triage.py fingerprint`, REA `inspect-electron-fuses` and REA `analyze-javascript-application` (preload + package.json):

- **Three renderer windows**: `desktop_chrome_v2` (the editor shell), `desktop_recording` (pages `display_media_picker`, `mission_control`, `overlay`, `talking_head`) and `desktop_offline_fallback`. → APPX-09 ✅ camera bubble, APPX-18 📄 display picker, APPX-19 📄 control + overlay windows, APPX-20 📄 offline fallback.
- **RTL shipped as separate builds**: every page exists as `.ltr`/`.rtl` CSS and HTML. → APPX-21 📄 (directly useful for Arabic apps).
- **16 file associations** including HEIC and Apple Keynote/Numbers/Pages. → APPX-22 📄.
- **One bridge, two members**: `ElectronBridge {onPageBuildIdentityReady, requestMessagePort}`; the web app talks to the shell over a MessagePort. → APPX-23 📄.
- **Fuses** (REA): RunAsNode, NODE_OPTIONS and inspect arguments disabled; cookie encryption, embedded ASAR integrity and only-load-from-ASAR enabled. → APPX-24 ✅ (the check is proven here).
- **Shell services** (anchor counts in `dist/main.js`): electron-updater/autoUpdater (77), Sentry (150) + crashReporter (9), safeStorage, `setAsDefaultProtocolClient` and `canva://notification`, `protocol.handle`, Tray, Notification, nativeTheme, spell-check dictionary, utilityProcess, webRequest. → APPX-25…27 📄.

## 4. Installer architecture

- Dual-arch NSIS payload (Canva) → APPX-28 📄.
- Online bootstrapper (CapCut: libcurl + BoringSSL with `sha256//` public-key pinning, MD5 check, signature checker, background worker, 23 UI languages; Adobe: UPX-packed Creative Cloud setup) → APPX-29 📄.
- Signature first, then triage, never run → APPX-30 ✅.

## 5. How to use this family

1. `python scripts/powers.py suggest "<طلبك>"` — names like CapCut/كاب كات, Canva/كانفا, Premiere/بريمير route here.
2. Open the record (`powers.py show APPX-13`) and run its `how` line; `proofs/app-feature-transfer/smoke.py` holds a working version of every ✅ recipe.
3. For a new app: `installer_triage.py scan` → `unpack --authorized` → `fingerprint` → REA (`route` prints the commands) → add what you found as new APPX records with the lowest honest badge, and a proof before ✅.

## 6. Second batch (2026-10-19): photo developers, type, vector, procedural, download

Analysed with REA 6.7.0 + `installer_triage.py`, nothing executed, no crack/patch/keygen opened ([BATCH_2026-10-19.md](../proofs/windows-installers-rea/BATCH_2026-10-19.md)).

| App | Evidence (names only) | Powers |
|---|---|---|
| DxO PhotoLab 4 | MSI hidden in PE resources → 45+ `DxO.PhotoLab.Correction.*` assemblies; REA read `NoiseRemovalMethod {High, Prime, DeepPrime}`, `KeystoningAutoMode`, `Compatibility.V7…V15` | APPX-31…36, 38, 43, 50 ✅ · APPX-51, 52 📄 |
| Capture One 21 | Inno payload: ~1,200 camera `.icm`, Presets60, Styles, StyleBrushes, PrintTemplates, AutoCrop | APPX-36, 37, 40, 41, 43 ✅ · APPX-53, 54 📄 |
| JPEGmini Pro 3.2 | .NET WPF MSI, SmartAssembly-obfuscated | APPX-39 ✅ |
| FontLab 7 | Inno payload: PythonQt, FreeType, HarfBuzz, kerning-pair frequency data | APPX-44 ✅ · APPX-55 📄 |
| Affinity Designer 1.10 | libgeometry, libocio, libpsd, libxmp, lens data | APPX-34, 42, 45 ✅ |
| Houdini 18.5 | VEX, PDG, KineFX, HDA/OTL CHOPs | APPX-45…47 ✅ · APPX-56 📄 |
| IDM 6.43 | signed Tonec installer, browser-integration DLL | APPX-48 ✅ |
| Adobe Animate 2024 | offline package (FLPR + 6 deps): FLCreateJS, SVGExport, GLTFExporter, TexturePacker, FlashIK | APPX-49 ✅ · APPX-58 📄 |
| Owner's projects | `virtualcam` (OBS virtual camera), `TikPlayer` (Android) → `apps/` | APPX-59, 60 📄 |
| ACDSee, Dreamweaver, Lightroom | RAR5 with encrypted headers: not opened (password not guessed) | APPX-42 from public docs |

Triage gained: Inno Setup detection (+ `innoextract`), payloads inside PE resources, encrypted RAR, MSI routes and Adobe offline packages (APPX-57 ✅, 22 unit tests).

## 7. App Studio — run every feature on the user's own files

<div dir="rtl">

**ما هو:** `scripts/app_studio.py` أداة سطر أوامر واحدة تنفّذ 61 عملية من قدرات البرامج المحللة على ملفات المستخدم الحقيقية، صورة واحدة أو مجلدًا كاملًا (`batch`)، وتطبع سطر JSON فيه الناتج والمقاييس. كلها مثبتة في `evals/test_app_studio.py` (45 اختبارًا داخل مجلد اسمه عربي، فالمسارات العربية على Windows مضمونة).

**متطلبات الاستخدام:** شغّل أولًا `python $SKILL_DIR/scripts/app_studio.py doctor`، فيطبع العمليات الجاهزة وسطر التثبيت لكل ما ينقص. على Windows استخدم `python` بدل `python3`.

</div>

| المتطلب / requirement | التثبيت / install | يفتح / unlocks |
|---|---|---|
| Python 3.9+ | python.org أو `winget install Python.Python.3.13` | كل العمليات |
| `pip:numpy` + `pip:opencv` | `pip install numpy opencv-python-headless` | كل عمليات الصور والتصميم الإجرائي |
| `pip:pillow` | `pip install pillow` | watermark، jpegmini، contact-sheet، pdf، exif، rename، catalog، icc، tween |
| `pip:arabic-reshaper` (اختياري) | `pip install arabic-reshaper python-bidi` | وصل الحروف العربية في العلامة المائية حين يغيب libraqm؛ الخط Amiri مرفق في `proofs/_shared/fonts` |
| `pip:fonttools` | `pip install fonttools brotli` | font-build، font-inspect، font-subset (woff2 يحتاج brotli) |
| `pip:shapely` | `pip install shapely` | boolean |
| `pip:segno` | `pip install segno` | qr (Canva QR) |
| `pip:matplotlib` | `pip install matplotlib` | chart |
| `pip:office` | `pip install python-pptx` | pptx |
| ffmpeg (اختياري) | `winget install Gyan.FFmpeg` | text-anim إلى MP4 (GIF بدونه) |
| `model:yunet` (OpenCV 5 فقط) | `face_detection_yunet_2023mar.onnx` من opencv_zoo، ثم `KOSIF_YUNET=<path>` | faces (في OpenCV 4 يعمل بلا نموذج) |
| شبكة / network | — | download فقط؛ كل الباقي يعمل دون اتصال |
| `innoextract` + 7-Zip | `scoop install innoextract 7zip` | تحليل مثبّتات جديدة (`installer_triage.py`)، لا لاستخدام القدرات |

```bash
python $SKILL_DIR/scripts/app_studio.py doctor
python $SKILL_DIR/scripts/app_studio.py ops صور
python $SKILL_DIR/scripts/app_studio.py develop in.jpg -o out.jpg --set wb=grey exposure=0.3 curve=s vibrance=0.25
python $SKILL_DIR/scripts/app_studio.py batch jpegmini ./shop -o ./shop_small --set delta=0.01
```

| op | APPX | app (evidence) | ماذا / what | requires |
|---|---|---|---|---|
| `dehaze` | APPX-31 | DxO ClearView | إزالة الضباب — remove haze (dark-channel prior) | pip:numpy, pip:opencv |
| `denoise` | APPX-32 | DxO Noise (High/Prime) | تقليل الضوضاء — noise reduction: fast (bilateral) or nlm | pip:numpy, pip:opencv |
| `keystone` | APPX-33 | DxO Perspective / ViewPoint | تصحيح المنظور — perspective: auto quad or points=x,y;x,y;x,y;x,y | pip:numpy, pip:opencv |
| `lens` | APPX-34 | DxO Distortion, Affinity lens data | تصحيح تشوه العدسة — undistort with k1 (k2, focal) | pip:numpy, pip:opencv |
| `ca` | APPX-35 | DxO ChromaticAberration | إزالة الزيغ اللوني — register R/B to G by radial scale | pip:numpy, pip:opencv |
| `develop` | APPX-36 | DxO WhiteBalance/ToneCurve/HSL, Capture One, Lightroom Basic | تطوير: توازن أبيض وتعريض ومنحنى وتشبع — wb=grey|none, temp, tint, exposure (EV), contrast, curve, saturation, vibrance | pip:numpy, pip:opencv |
| `grain` | APPX-37 | Capture One Film Grain, DxO Grain | حبيبات فيلم — amount (σ), size | pip:numpy, pip:opencv |
| `vignette` | APPX-37 | DxO CreativeVignetting, Lightroom | تعتيم الأطراف — amount 0..1, start radius | pip:numpy, pip:opencv |
| `watermark` | APPX-38 | DxO Watermark, Lightroom export | علامة مائية — text= or logo=, opacity, pos=br|bl|tr|tl|c, size | pip:pillow, pip:numpy, pip:opencv |
| `jpegmini` | APPX-39 | JPEGmini | ضغط JPEG إدراكي — smallest quality within delta SSIM of q95 | pip:pillow, pip:numpy, pip:opencv |
| `contact-sheet` | APPX-40 | Capture One PrintTemplates, Lightroom Print | ورقة تواصل PDF — cols, rows, page=A4|letter, title | pip:pillow |
| `preset` | APPX-41 | Capture One Styles, DxO presets, Lightroom presets | تطبيق إعداد مسبق — preset=file.json (ops: develop/grain/vignette/curve…) | pip:numpy, pip:opencv |
| `xmp` | APPX-42 | Lightroom, ACDSee, DxO Search.Metadata, Affinity libxmp | ملف XMP جانبي — rating 0-5, label, keywords=a,b (adds), read=1 | stdlib |
| `horizon` | APPX-43 | DxO Horizon, Capture One AutoCrop | تقويم الأفق — auto angle from long lines (or angle=), crop=1 | pip:numpy, pip:opencv |
| `hdr` | APPX-50 | DxO Smart Lighting, Lightroom HDR merge | دمج تعريضات HDR — 2+ bracketed images → exposure fusion | pip:numpy, pip:opencv |
| `sharpen` | APPX-61 | DxO UnsharpMask, Lightroom Detail | توضيح الحدة — amount, radius, threshold | pip:numpy, pip:opencv |
| `clarity` | APPX-62 | DxO Texture/Microcontrast, Lightroom Clarity | وضوح وملمس — amount (−1..1), radius (large = clarity, small = texture) | pip:numpy, pip:opencv |
| `hsl` | APPX-63 | DxO HSL / ColorAccentuation, Lightroom HSL, Capture One Color Editor | تحكم لوني لكل نطاق — band=green hue=+10 sat=-0.5 lum=+0.2 (bands: red orange yellow green aqua blue purple magenta) | pip:numpy, pip:opencv |
| `bw` | APPX-64 | DxO ChannelMixer, Lightroom B&W, Capture One Black and White | أبيض وأسود بخلط القنوات — r g b weights (default 0.3 0.59 0.11), tone=sepia|none | pip:numpy, pip:opencv |
| `split-tone` | APPX-65 | DxO Toning, Lightroom Color Grading | تلوين الظلال والإضاءات — shadows=#hex highlights=#hex balance amount | pip:numpy, pip:opencv |
| `redeye` | APPX-66 | DxO RedEyes | إزالة احمرار العين — auto (eye detector) or box=x,y,w,h | pip:numpy, pip:opencv |
| `repair` | APPX-67 | DxO Repair, Lightroom Heal/Remove, Affinity Inpainting | إزالة عنصر/ترميم — mask=mask.png (white = remove) or box=x,y,w,h; method=telea|ns | pip:numpy, pip:opencv |
| `moire` | APPX-68 | DxO Moire | إزالة التموج (مواريه) — FFT notch of periodic peaks; strength | pip:numpy, pip:opencv |
| `tilt-shift` | APPX-69 | DxO TiltShift | تأثير المجسم (تلت-شيفت) — center 0..1, band, blur, saturation | pip:numpy, pip:opencv |
| `bg-blur` | APPX-70 | DxO CreativeBlur, Lightroom Lens Blur | تغبيش الخلفية — auto subject (GrabCut) or box=x,y,w,h; blur | pip:numpy, pip:opencv |
| `crop` | APPX-71 | Lightroom/Capture One crop, DxO Crop | قص بنسبة — aspect=1:1|4:5|9:16|16:9, focus=center|subject | pip:numpy, pip:opencv |
| `resize` | APPX-72 | JPEGmini/Lightroom export, ACDSee batch resize | تغيير المقاس — long=2048 or width= / height=, sharpen=1 | pip:numpy, pip:opencv |
| `icc` | APPX-53 | Capture One camera profiles, DxO ICC / soft-proof | تحويل ملف اللون — to=srgb|path.icc, from=path.icc (default: embedded or sRGB) | pip:pillow |
| `auto-tone` | APPX-73 | Lightroom Auto, ACDSee Auto Lighting, DxO Smart Lighting | ضبط تلقائي للإضاءة — clip % for levels | pip:numpy, pip:opencv |
| `exif` | APPX-74 | ACDSee/Lightroom metadata panel | قراءة بيانات الصورة وGPS — prints EXIF incl. GPS as JSON | pip:pillow |
| `dedupe` | APPX-75 | ACDSee Duplicate Finder, Lightroom | كشف الصور المكررة والمتشابهة — threshold (Hamming bits, default 6) | pip:numpy, pip:opencv |
| `faces` | APPX-76 | ACDSee/Lightroom People, Capture One | كشف الوجوه — boxes as JSON; draw=1 writes a preview | pip:numpy, pip:opencv |
| `rename` | APPX-77 | ACDSee/Lightroom batch rename | إعادة تسمية دفعة — pattern={date}_{n:04d}{ext} (date from EXIF), dry=1 | pip:pillow |
| `catalog` | APPX-78 | Lightroom Catalog, ACDSee database | فهرسة مكتبة الصور — folder → SQLite (path, size, exif, gps, rating, keywords, dhash) | pip:pillow, pip:numpy, pip:opencv |
| `search` | APPX-78 | Lightroom/ACDSee search and smart collections | بحث في المكتبة — q=word, min_rating=, camera= | stdlib |
| `boolean` | APPX-45 | Affinity Designer, Xara, Houdini he_boolean | عمليات بوليانية متجهة — IN = JSON [{"circle":[x,y,r]}|{"rect":[x,y,w,h]}|{"poly":[[x,y],…]}] ; mode=union|difference|intersection|xor ; fill | pip:shapely |
| `trace` | APPX-79 | Affinity/Xara bitmap to vector | تحويل صورة إلى متجه SVG — colors=4 (k-means), smooth (epsilon px) | pip:numpy, pip:opencv |
| `pdf` | APPX-80 | Affinity/Xara export, Lightroom/JPEGmini album | صور إلى PDF — dpi=300 | pip:pillow |
| `scatter` | APPX-81 | Houdini Scatter/Copy to Points, Affinity symbols | نثر عناصر إجرائيًا — w h count seed min_dist shape=circle|star size jitter → SVG (Poisson-disc) | pip:numpy, pip:opencv |
| `noise-field` | APPX-82 | Houdini Mountain/Noise SOP, VEX noise | حقل ضوضاء إجرائي (أرض/سحب/تموج) — w h scale octaves seed mode=gray|terrain|clouds → PNG (fractal value noise) | pip:numpy, pip:opencv |
| `lsystem` | APPX-83 | Houdini L-System SOP | نمو نباتي/زخرفي (L-system) — axiom rules=F:FF+[+F-F-F]-[-F+F+F] iterations angle step → SVG | stdlib |
| `chops` | APPX-46 | Houdini CHOPs (Lag, Noise, Cycle, Envelope, Spring) | عمليات منحنيات الحركة — IN = keys JSON [[t,v],…] ; fps, lag=τ s, noise=amp, noise_freq, spring=k:damping → JSON curve per frame | pip:numpy, pip:opencv |
| `font-build` | APPX-44 | FontLab 7 | بناء خط من رسومات SVG — IN = folder of SVGs named by character or uniXXXX (e.g. A.svg, uni0628.svg) ; family, upm, kern="A V -80;V A -80", fea=file | pip:fonttools |
| `font-inspect` | APPX-84 | FontLab font info / Glyphs panel | فحص خط — names, glyph count, scripts (Arabic coverage), features, kerning pairs | pip:fonttools |
| `font-subset` | APPX-85 | FontLab export / web fonts | تقليص خط للويب — text= or unicodes=, flavor=woff2|woff | pip:fonttools |
| `tween` | APPX-49 | Adobe Animate classic/motion tween + TexturePacker + onion skin | حركة متوسطة وورقة رسوم — IN = sprite PNG ; from=x,y to=x,y frames fps ease=inout|in|out|back w h cols onion=1 | pip:pillow |
| `lottie` | APPX-86 | Adobe Animate export (Bodymovin/Lottie), Canvas | تصدير Lottie JSON — w h fps frames from=x,y to=x,y shape=circle|rect size color ease | stdlib |
| `ik` | APPX-87 | Adobe Animate Bone tool (FlashIK), Houdini KineFX | حل عظمتين (IK) — l1 l2 target=x,y → joint angles + positions JSON | stdlib |
| `download` | APPX-48 | Internet Download Manager | تنزيل مجزأ قابل للاستئناف — IN = URL ; parts=6, sha256= (verify) | stdlib |
| `design` | APPX-88 | Canva editor (templates, text effects, frames, gradients) | تصميم من قالب JSON (نصوص عربية وصور وأشكال) — IN = design.json {size|width,height, background, elements:[text|image|rect|ellipse|line]} → PNG/JPG/PDF | pip:pillow, pip:numpy |
| `resize-design` | APPX-89 | Canva Magic Resize | مقاسات متعددة لكل المنصات من تصميم واحد — sizes=instagram-post,story,youtube-thumbnail,… (or all) ; mode=smart|pad-blur|pad-color ; color=#hex → OUT_DIR | pip:numpy, pip:opencv |
| `remove-bg` | APPX-14 | Canva Background Remover, CapCut | إزالة الخلفية إلى PNG شفاف — box=x,y,w,h around the subject (default: centre 70%) ; feather px → transparent PNG | pip:numpy, pip:opencv |
| `duotone` | APPX-90 | Canva Duotone filter (DUOTONE in app.asar) | تأثير اللونين (Duotone) — dark=#hex light=#hex | pip:pillow, pip:numpy |
| `collage` | APPX-91 | Canva grids / Collage | كولاج وشبكات صور — IN = images or folder ; layout=grid|hero|strip ; cols ; size=instagram-post|WxH ; gap ; radius ; bg | pip:pillow |
| `mockup` | APPX-92 | Canva Mockups (PHOTO_TO_MOCKUP, MockupBundle in app.asar) | وضع التصميم داخل صورة واقعية (موك أب) — IN = design, scene photo ; quad=x,y;x,y;x,y;x,y (TL;TR;BR;BL) or auto (largest bright quad) ; shade=0..1 | pip:numpy, pip:opencv |
| `qr` | APPX-93 | Canva QR code app (vendor QR library in app.asar) | رمز QR بألوان وشعار — IN = text/URL ; dark=#hex light=#hex scale border logo=path ; error=h when a logo is used → PNG/SVG (decoded back to verify) | pip:segno, pip:opencv |
| `palette` | APPX-94 | Canva Brand Kit / colour palette from photo | لوحة ألوان الهوية من شعار أو صورة — colors=5 → JSON (hex, share, best text colour + WCAG contrast) + swatch PNG | pip:numpy, pip:opencv, pip:pillow |
| `chart` | APPX-95 | Canva Charts | رسم بياني بعناوين عربية — IN = data.json {labels:[…], values:[…]} or CSV label,value ; kind=bar|line|pie|donut ; title ; color ; font → PNG/SVG | pip:matplotlib |
| `pptx` | APPX-96 | Canva Presentations (presentationml export in app.asar) | عرض تقديمي PowerPoint — IN = slide images/designs (PNG/JPG or design.json) in order ; notes=file.txt (one line per slide) → .pptx 16:9 | pip:office, pip:pillow |
| `print-pdf` | APPX-97 | Canva Print PDF (bleed, crop marks, CMYK in app.asar) | PDF جاهز للمطبعة: نزيف وعلامات قص وCMYK — IN = design image ; width_mm height_mm (trim) ; bleed_mm=3 ; marks=1 ; cmyk=1 ; dpi=300 ; profile=CMYK.icc (optional, accurate) | pip:pillow |
| `text-anim` | APPX-98 | Canva text animations (Rise, Typewriter, Fade, Pop) | تحريك نص عربي إلى GIF أو MP4 — text ; style=rise|typewriter|fade|pop ; size=story|WxH ; font ; color ; bg ; seconds ; fps → .gif or .mp4 (ffmpeg) | pip:pillow, pip:numpy |

**Honesty rules:** `verified` is true only when the op measured its own postcondition (SSIM for `jpegmini`, keyword round-trip for `xmp`, SHA-256 for `download`, minimum distance for `scatter`, reach error for `ik`). These are open, classical methods, not the vendors' algorithms (DeepPRIME, ClearView Plus, Lightroom's AI masks).

**Limits:** anchor counts prove code presence, not that a feature runs; minified aliases can hide APIs (REA proved 0 Electron identities in Canva's 6.8 MB main bundle for exactly that reason). Vendor-documented features are listed as context; only the open recipes carry ✅.

## 9. Global video platforms and two original workflow adapters (2026-10-19)

See [Global video platform capability atlas](global-video-platforms-2026-10-19.md) for vendor-attributed features, clean-room routes, and verified vs unavailable capabilities. scripts/video_workflow_bridge.py adds tested text-selected video-only paper-edit manifests inspired by Descript/Premiere and timecode/position-accurate review markers inspired by Frame.io. It is a non-destructive manifest generator, not an imported vendor editor. Its use never licenses proprietary models or third-party videos.
