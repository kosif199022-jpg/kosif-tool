# الصور والتحرير والتوليد — Images & photo editing (`images`)

> مكتبة بروتوكول USIP v5.5، مولّدة بـ `scripts/smart_capabilities.py library` من `data/powers/*.json` و`data/tools.json`؛ لا تُحرَّر يدويًا. الدليل: [A28 اختيار القدرات](../protocol/A28-capability-routing.md) · [الفهرس](INDEX.md) · [النواة](../../PROTOCOL.md#متى-تفتح-الملاحق--appendix-triggers)

## الفهرس / contents

- [متى تستخدم هذه المجموعة / when](#متى-تستخدم-هذه-المجموعة--when)
- [الحالة بالأرقام / status](#الحالة-بالأرقام--status)
- [الأدوات القابلة للتشغيل / runnable tools](#الأدوات-القابلة-للتشغيل--runnable-tools)
- [العائلات / families](#العائلات--families)
- [كل القدرات / every power](#كل-القدرات--every-power)

## متى تستخدم هذه المجموعة / when

كلمات التوجيه: image photo photoshop paint color grading generate edit صور تعديل تلوين فوتوشوب توليد

خط العمل المقترح (هدف تصميم، لم يُختبر كوحدة واحدة): استيراد الصورة → التحرير والتلوين → التوليد الاختياري → تصدير النتيجة

العضوية في المجموعة تصنيف للتوجيه، لا دليل على أن القدرات تعمل معًا: اربطها بخط عمل مختبر فقط.

## الحالة بالأرقام / status

| الحالة | العدد | المعنى |
|---|---:|---|
| `proven` | 96 | ✅ proven: a proof exists in the catalog; still check its requirements here before calling it ready |
| `ready` | 42 | 🟢 ready: runnable without setup according to the catalog |
| `documented` | 96 | 📄 documented: a described method; needs building or wiring before it runs |
| `seen` | 22 | 👁 seen: observed in a reference or demo, not executed here |
| `install` | 27 | 📦 install: needs a package, binary or model first |
| `key` | 35 | 🔑 key: needs an account, key or paid service (ask before any spend) |
| `idea` | 2 | 💡 idea: not built |
| **المجموع** | **320** | |

## الأدوات القابلة للتشغيل / runnable tools

| الأداة | ما تفعله | ابدأ بـ | الدليل |
|---|---|---|---|
| `app-studio` | استوديو التطبيقات للصور والتصميم | `python3 scripts/app_studio.py --help` | tested-here |
| `app-studio-paint` | حزمة الرسم في استوديو التطبيقات | `python3 -c "import sys; sys.path.insert(0,'scripts'); import app_studio; print(app_studio.PAINT_BATCH['effects'])"` | tested-here |
| `cinematic-broll-render` | تصيير لقطات B-roll بحركة كاميرا | `python3 scripts/cinematic_broll_render.py --edl ./edl.json --manifest ./clips.json --audio ./voice.wav --out ./out/master.mkv --width 1080 --height 1920` | tested-here |
| `cinematic-cut-planner` | مُخطِّط قطعات اللقطات الحقيقية | `python3 scripts/cinematic_cut_planner.py --words ./words.json --clips ./clips.json --duration 48.5 --fps 30 --out ./out/edl.json` | tested-here |
| `creative-external-search` | بحث المصادر الإبداعية دون اتصال | `python3 scripts/creative_external_search.py search "kinetic typography" --kind repo --top 5` | tested-here |
| `dua-wednesday` | دعاء يوم الأربعاء — محرك ريل دعاء موشن جرافيك 9:16 | `python3 scripts/dua_wednesday.py doctor` | tested-here |
| `fetch-reference` | جلب المرجع المسموح وقياسه | `python3 scripts/fetch_reference.py https://example.com/page --list --json` | tested-here |
| `fetch-video` | تنزيل الفيديو من الروابط للمونتاج | `python3 scripts/fetch_video.py --doctor` | tested-elsewhere |
| `image-local-ai` | ذكاء الصور المحلي: إزالة الخلفية والملء الذكي بنموذج ONNX تختاره | `python3 scripts/image_local_ai.py models --json` | tested-here |
| `kosif-timeline` | محرر KOSIF Timeline: مونتاج متعدد المسارات مع تراجع وإعادة | `python3 scripts/kosif_timeline.py doctor` | tested-here |
| `kosif-timeline-demo` | تجربة مونتاج KOSIF Timeline تلقائية بملفات أصلية مولدة | `python3 scripts/kosif_timeline_demo.py --dir ./fresh-kosif-timeline-demo` | tested-here |
| `media-sources` | بوابة الوسائط المرخّصة | `python3 scripts/media_sources.py list` | tested-here |
| `mimic` | محرك محاكاة الفيديو المرجعي | `python3 -c "import sys; sys.path.insert(0,'scripts/mimic'); import mm_analyze; mm_analyze.analyze('./in.mp4','./work')"` | tested-here |
| `montage-pro` | فريق مونتاج برو (صوت أو فيديو إلى مونتاج أو موشن) | `python3 scripts/montage_pro.py doctor` | tested-here |
| `mosamem-rea-fusion` | تكامل مصمم وREA: فحص صور وتوليف مهارات آمن | `python3 scripts/mosamem_rea_fusion.py doctor` | tested-here |
| `motion-reference-probe` | فاحص توقيت الفيديو المرجعي | `python3 scripts/motion_reference_probe.py ./in.mp4` | tested-here |
| `rebalance-creative-repos` | إعادة موازنة فهرس المستودعات الإبداعية | `python3 scripts/rebalance_creative_repos.py run` | tested-elsewhere |
| `reference-edit-engine` | محرك إعادة بناء المونتاج المرجعي | `python3 scripts/reference_edit_engine.py --probe ./cuts.json --out ./new-edit` | tested-here |
| `reference-visual-fingerprint` | البصمة البصرية للفيديو المرجعي | `python3 scripts/reference_visual_fingerprint.py ./in.mp4 --probe ./cuts.json --out ./reference-look.json` | tested-here |
| `repo-ashell-cinema` | استوديو التنزيل Cinema C للآيفون | `sh tools/a-shell/Cinema_C_V34_Studio_iPhone.sh "https://www.youtube.com/watch?v=VIDEO_ID"` | tested-elsewhere |
| `repo-verify-video` | بوابة فحص تسليم الفيديو | `python3 tools/verify_video.py ./out/film.mp4 --aspect 9:16 --fps 30 --duration 12 --audio ./voice.mp3 --json ./out/report.json` | tested-here |
| `stock-fetch` | تحميل لقطات مجانية بلا مفتاح (Pexels وMixkit) | `python3 scripts/stock_fetch.py probe` | tested-here |
| `stream-grabber` | ملتقط بث DASH وHLS للمونتاج | `python3 scripts/stream_grabber.py find ./saved-page.html` | tested-here |
| `style-library` | مكتبة الأساليب: 586 أسلوبًا بصريًا بالاسم (86 من أطلس Futurepedia + 500 أصلي) — بحث ووصف وبرومنت وعينة وكتالوج PDF مصوّر | `python3 scripts/style_library.py groups` | tested-here |
| `unified-cinematic` | السينما الموحدة: مونتاج الفيديو مع الصوت وحركة الكاميرا | `python3 scripts/unified_cinematic.py doctor` | tested-here |
| `unified-media` | محرر الوسائط الموحد: صور ورسم وتحريك وفيديو | `python3 scripts/unified_media.py doctor` | tested-here |
| `verify-video` | بوابة فحص تسليم الفيديو | `python3 scripts/verify_video.py ./in.mp4 --aspect 9:16 --fps 30 --duration 15 --json ./out/report.json` | tested-here |

الأوامر نسبية إلى مجلد المهارة (أو جذر المستودع لأدوات `tools/`)؛ `python3 scripts/hub.py tool <id>` يعطي كل الأوامر والمتطلبات والحدود.

## العائلات / families

| العائلة | القدرات | الفصل |
|---|---:|---|
| `ai-generation` | 94 | [ai-generation.md](../powers/ai-generation.md) |
| `atlas-media` | 27 | [atlas-media.md](../powers/atlas-media.md) |
| `color-palette-grading` | 87 | [color-palette-grading.md](../powers/color-palette-grading.md) |
| `media-image-audio` | 41 | [media-image-audio.md](../powers/media-image-audio.md) |
| `photo-video-footage` | 71 | [photo-video-footage.md](../powers/photo-video-footage.md) |

## كل القدرات / every power

مرتبة بالحالة ثم العائلة ثم المعرّف. `hub.py` و`skill_intelligence.py deep <ID>` يعطيان بطاقة القدرة كاملة بدليلها.

| المعرّف | الاسم | English | الحالة | المتطلبات |
|---|---|---|---|---|
| `GEN-02` | القواعد الحديدية والكلمات القوية | Iron rules: physical cues beat hype words | proven | python3 |
| `GEN-10` | مصنع البرومبت: مواصفة واحدة ← تسع منصات | Prompt forge: one spec → 9 generator prompts | proven | python3, key:openai, key:video-gen |
| `GEN-11` | خصائص منصات الفيديو (DNA) | Video-model platform DNA (Veo / Runway / Kling / Sora) | proven | key:openai, key:video-gen |
| `GEN-12` | مواصفة الصورة الموحدة وستة مُنشئات | Image spec schema → 6 platform builders | proven | python3, key:video-gen |
| `GEN-13` | قوالب لقطات الفيديو لسبع منصات مع قص المدة | Shot list → 7 video-platform prompts with duration clamping | proven | python3, key:openai, key:video-gen |
| `GEN-14` | برومبتات اللقطات السباعية (kmotion aiprompts) | kmotion aiprompts: 7-layer per-shot prompts | proven | python3, key:openai, key:video-gen |
| `GEN-15` | من فيديو مرجعي إلى برومبت Omni Flash | Reference breakdown → Omni Flash generation prompt | proven | python3 |
| `GEN-16` | مواصفة مشهد مكتوبة وبصمة SHA-256 | Typed SceneSpec compile + SHA-256 digest | proven | python3 |
| `GEN-17` | أقفال الشخصية والأسلوب والمكان | Character / style / location locks | proven |  |
| `GEN-18` | واجهة الأنماط المرحلية (Fastify) | Stage-gated profile CLI | proven | node |
| `GEN-19` | سلاسل برومبتات الأنماط الخمسة | Five profile prompt series (stickman, fitness, car, history, food) | proven | node |
| `GEN-20` | حزمة الكينتك فلو واللقطة النظيفة | Kinetic Flow prompt pack + clean plate & overlay sheet | proven | npm:remotion, key:video-gen |
| `GEN-21` | برومبتات البوستر والحركة التحريرية | Viral-editorial poster + silent motion prompts | proven |  |
| `GEN-34` | استخراج الكود من رد الذكاء الاصطناعي | AI-reply code extraction | proven | chromium, pip:opencv |
| `COLOR-01` | أحد عشر لوكًا جاهزًا بـFFmpeg | Eleven FFmpeg grade presets | proven | ffmpeg, python3, imagemagick |
| `COLOR-02` | ترميم الفوتيج القديم | Restore grade for old or soft footage | proven | python3, imagemagick |
| `COLOR-03` | تلوينات مشاريع بسطر واحد | One-line project grades (muted Ghorba, navy door + RTL mirror) | proven |  |
| `COLOR-04` | خَبز أي تلوين في LUT | Bake any grade into a Hald CLUT / .cube and apply LUTs | proven | ffmpeg, pip:numpy |
| `COLOR-05` | لوكات المتصفح بالفلاتر وطبقات الدمج | Browser looks: CSS filter + blend-mode tint layers | proven | chromium |
| `COLOR-14` | كشف اللوج قبل LUT | Log detection before a conversion LUT | proven | ffmpeg |
| `COLOR-15` | التعريض حسب وقت اليوم | Exposure bands by time of day + cut jump caps | proven | ffmpeg |
| `COLOR-16` | توازن الأبيض بالبكسلات المحايدة | Neutral-pixel white balance | proven | ffmpeg |
| `COLOR-17` | تباين حول محور مع حماية القص | Pivot contrast with clip guard | proven | ffmpeg |
| `COLOR-18` | أرضية تشبع وانحدار سينمائي | Saturation floor with film roll-off | proven | ffmpeg |
| `COLOR-19` | تعزيز السماء فقط | Sky hue-window boost | proven | ffmpeg |
| `COLOR-22` | تحليل حرارة اللون والميل والتشبع | Colour analysis: CCT, cast, colourfulness, 6-colour palette | proven | python3 |
| `COLOR-23` | إزاحة الميرد واختيار الجل | Mired shift → CTO/CTB gel | proven | python3 |
| `COLOR-24` | استخراج الباليت وتسمية الألوان | Palette extraction, colour naming and ΔE | proven | pip:opencv |
| `COLOR-25` | باليت وخلفية لكل نبضة من المرجع | Reference palette + background per beat | proven | python3 |
| `COLOR-26` | نقل رينهارد إلى LUT لكل لقطة | Reinhard Lab transfer → per-shot .cube | proven | ffmpeg |
| `COLOR-27` | مطابقة اللقطات بنقل لوني محدود | Bounded colour transfer + Hungarian shot match | proven | python3 |
| `COLOR-29` | تغيير لون بلون مع الحفاظ على الظل | Local recolour A→B keeping shading (Arabic requests) | proven | pip:pillow |
| `COLOR-31` | هوية كاملة من لون واحد | One hex → full WCAG token set (+ 9 accent presets) | proven | python3, npm:axe |
| `COLOR-32` | هوية «دفتر KOSIF» | Dafter KOSIF ledger identity (default, light + night) | proven | node |
| `COLOR-34` | إعادة تلوين حسب الدور | Role-based palette remap (brandCSS) | proven | node |
| `COLOR-35` | تحويل انتقائي ذهبي→جليدي | Selective gold→ice hue rotation (image and video) | proven | pip:numpy |
| `COLOR-36` | باليتات الشيدر كمتغيرات | Shader palettes as uniforms (Crystal World) | proven | npm:three |
| `COLOR-37` | باليتات منتجات التدقيق | KOSIF audit palettes + cascade-order theming | proven | node |
| `COLOR-38` | ثيمات Kinetic Flow السبعة عشر | Kinetic-flow locked themes A–Q + custom R | proven | node |
| `COLOR-39` | باليتات الافتتاحي الفيروسي | Viral-editorial palettes 1–3 + 80/20 rule | proven | node |
| `COLOR-41` | باليتات القوالب وخاناتها | Starter palettes and palette slots | proven | npm:remotion |
| `COLOR-45` | ألوان الحالات الدلالية | Semantic status colours (soft-tint chips, 5-stop ladder) | proven | node |
| `COLOR-48` | التدرج الحراري بسبع محطات | Thermal 7-stop heat ramp | proven |  |
| `COLOR-50` | مولّد التناغم اللوني | Harmony generator 2D/3D + harmony detector | proven | chromium, npm:three, npm:gsap |
| `COLOR-52` | حساب التباين WCAG | WCAG contrast math, role tiers and alpha flattening | proven | python3, npm:axe |
| `COLOR-56` | قفل الأسلوب وبصمة المرجع | Style lock and reference style-DNA (+ exact hex after generation) | proven | npm:remotion |
| `COLOR-62` | تشطيب الرسام الفيلمي | Painter filmic curve, split-tone grade and grain | proven | pip:pillow, pip:opencv |
| `COLOR-63` | انضغاط الإضاءات العالية | Highlight roll-off quantiser | proven |  |
| `COLOR-64` | التعتيم الطرفي في كل محرك | Vignette in every engine | proven | ffmpeg, npm:three |
| `COLOR-65` | تدرجات بشفافية وأنماط دمج | Gradient paints with alpha stops and blend modes | proven |  |
| `COLOR-66` | قلب القطبية بين الفصول | Polarity flip ink↔paper at act boundaries | proven | chromium, npm:gsap |
| `COLOR-78` | أرضيات داكنة شعاعية | Radial dark grounds | proven |  |
| `MEDIA-01` | كتابة العربية على الصور بـ Pillow | Arabic text on images with Pillow (raqm) | proven | pip:pillow, fonts:arabic |
| `MEDIA-02` | لا تشكّل العربية مرتين | Never double-shape Arabic | proven | libreoffice, pip:pillow, pip:matplotlib, pip:office |
| `MEDIA-03` | التعرف على العربية والإنجليزية بـ tesseract | Arabic + English OCR with tesseract | proven | python3, tesseract |
| `MEDIA-04` | نقاط ضعف OCR العربي | Arabic OCR weak spots (digits, display fonts) | proven | tesseract, fonts:arabic |
| `MEDIA-05` | تقويم الصفحات المائلة | Deskew scans before OCR | proven | chromium, tesseract, pip:opencv |
| `MEDIA-06` | قس قبل أن تعالج | Measure preprocessing, do not assume it helps | proven | tesseract |
| `MEDIA-08` | عمليات OpenCV الأساسية | OpenCV basics (edges, threshold, warp) | proven | chromium, pip:opencv |
| `MEDIA-09` | ضغط الصور ومقارنة الجودة | Image compression with quality metrics | proven | chromium, pip:pillow, pip:opencv |
| `MEDIA-10` | استخراج لوحة الألوان | Dominant palette with k-means | proven | chromium, pip:numpy, pip:opencv |
| `MEDIA-11` | رموز QR والباركود | QR codes and barcodes (encode + decode) | proven | chromium, pip:opencv |
| `MEDIA-12` | ImageMagick من سطر الأوامر | ImageMagick 6 CLI | proven | imagemagick |
| `MEDIA-13` | SVG إلى PNG | SVG to PNG (cairosvg) | proven | python3, chromium |
| `MEDIA-14` | المراجعة البصرية لمخرجاتي | Look at your own outputs (vision QA) | proven | pip:pillow, pip:matplotlib |
| `MEDIA-15` | توليد إشارات صوتية للاختبار | Synthesize test audio | proven | pip:numpy, pip:soundfile |
| `MEDIA-16` | قياس طبقة الصوت | Pitch tracking (librosa YIN) | proven | pip:numpy, pip:librosa |
| `MEDIA-17` | كشف بدايات الأصوات والإيقاع | Onset and tempo detection | proven | pip:librosa |
| `MEDIA-18` | قياس الجهارة LUFS | Loudness measurement (LUFS) | proven | ffmpeg, pip:pyloudnorm |
| `MEDIA-19` | تطبيع الجهارة بمرورين خطّيين | Two-pass linear loudnorm to a target | proven | ffmpeg |
| `MEDIA-20` | كشف الصمت | Silence detection | proven | ffmpeg |
| `MEDIA-21` | صور الموجة والطيف | Waveform and spectrogram images | proven | ffmpeg |
| `MEDIA-22` | قص وتلاشي وتصدير بـ pydub | Slice, fade and export with pydub (Python 3.13) | proven | ffmpeg, python3 |
| `MEDIA-23` | تحويل الصيغ والتحقق من المدة | Transcode and verify duration | proven | ffmpeg |
| `MEDIA-24` | مؤثرات صوتية بـ pedalboard | Audio effects (pedalboard, GPL) | proven | python3 |
| `MEDIA-31` | music21: بناء المدونات الموسيقية وقراءتها وتحليل المقامات والأوتار | music21: Build, parse and analyse scores (MIDI/MusicXML): keys, chords, voice leading | proven | pip:music21 |
| `FOOT-08` | كشف اللقطات إلى تايملاين | Scene/shot detection → timeline | proven | python3 |
| `FOOT-09` | لوحة لقطات واختيار الغلاف | Contact sheet & cover-frame mining | proven | ffmpeg |
| `FOOT-13` | دراسة ريل مرجعي بدقة الإطار | Reference-reel study (mimic) | proven | python3 |
| `FOOT-16` | مترجم تايملاين JSON | JSON timeline compiler (cuts, ramps, overlays) | proven | ffmpeg |
| `FOOT-19` | منحدرات السرعة والتصوير البطيء | Speed ramps & slow motion | proven | npm:hyperframes |
| `FOOT-24` | تثبيت الاهتزاز | Stabilisation (vidstab 2-pass) | proven | python3 |
| `FOOT-25` | إزالة التشويش والتوضيح وسلسلة الترميم | Denoise, sharpen & restoration chain | proven | ffmpeg |
| `FOOT-26` | مسح الترجمة المحروقة | Burned-caption eraser (decaption) | proven | python3 |
| `FOOT-28` | مفتاح اللون الأخضر | Chroma key | proven | ffmpeg |
| `FOOT-29` | تعديل الصورة: إعادة تلوين تحفظ الظلال | Picture edits: shading-preserving recolour | proven | python3 |
| `FOOT-39` | كين بيرنز الصحيح | Ken Burns done well | proven | ffmpeg |
| `FOOT-47` | لوح لقطات كل إطاراته مفتاحية | All-intra seekable footage plate | proven | python3 |
| `FOOT-48` | عرض الأفقي في 9:16 فوق نسخة مموهة | Landscape in 9:16 over a blurred fill | proven | ffmpeg, imagemagick |
| `FOOT-53` | مشغل مقدمة سينمائية متكيف | Adaptive cinematic intro player | proven | node |
| `FOOT-54` | مونتاج تلقائي على الموسيقى | Auto montage to music | proven | imagemagick |
| `FOOT-D01` | ريل «الدعاء» من لقطاتك وصوتك | «الدعاء» Friday dua reel kit | proven | python3 |
| `FOOT-D02` | انتقالات كاب كات على الصورة فقط | CapCut-style transitions under fixed text | proven | python3 |
| `FOOT-D03` | قياس أسلوب ريل من الإطارات | Measure a reel's style from its frames | proven | ffmpeg, pip:numpy, pip:faster-whisper |
| `FOOT-X03` | القص الدقيق بالإطار يحتاج إعادة ترميز | Frame-accurate trims need a re-encode | proven | ffmpeg |
| `FOOT-X06` | فاحص المرجع المرخّص: صفحة أو ملف أو HLS ← قياسات | Permissioned reference inspector: page / direct / HLS → measurements | proven | python3 |
| `GEN-22` | بذور برومبت في كل سقالة | Per-shot AI prompt seeds written by the scaffold | ready |  |
| `GEN-23` | تخطيط موجه لنماذج الفيديو | ProPlan model-prompt stage with continuity locks | ready | python3, key:openai, key:video-gen |
| `GEN-24` | معادلة برومبت النماذج اللغوية ومدققها | LLM prompt formula + linter (prompts for agents & generators) | ready | python3 |
| `GEN-33` | أنت المولّد: صورة من وصف بالكود (SVG / Canvas / PIL / Three.js) | You are the generator: picture from a description as code | ready | pip:pillow, npm:three |
| `GEN-35` | جسر الذكاء في الاستوديو (Claude CLI / API / يدوي) | Studio AI bridge: Claude CLI → API → manual | ready | python3 |
| `GEN-86` | انضباط ميزانية التوليد المدفوع | Paid-generation budget discipline | ready |  |
| `GEN-89` | التمييز بين البرومبت والوسائط | Prompt ≠ media honesty rule | ready | ffmpeg |
| `COLOR-06` | سلسلة FFmpeg المُصدّرة من «بصمة» | Basma fingerprint grade chain export | ready | ffmpeg, python3 |
| `COLOR-07` | أمزجة فيلم الكلمات وتلوينها | Verse moods: palette plus matching footage grade | ready | python3 |
| `COLOR-33` | مظاهر KOSIF EARTH | KOSIF EARTH identity looks (14) | ready | node |
| `COLOR-40` | باليتات أفلام المالك | Owner film palettes from shipped projects | ready |  |
| `COLOR-42` | ثيمات HyperFrames وعقد الرموز | HyperFrames themes + 18-token contract | ready | npm:hyperframes |
| `COLOR-46` | باليتات آمنة لعمى الألوان | Colour-blind-safe categorical palettes | ready |  |
| `COLOR-49` | تدرجا ماغما والجبل | Magma colormap and alpine terrain ramp | ready |  |
| `COLOR-54` | لون تمييز واحد بمعنى واحد | One accent, one meaning (~5% of the frame) | ready | lean |
| `COLOR-57` | تحويل النغمات ACES وAgX وNeutral | Tone-mapping choice: ACES, AgX or Neutral | ready | chromium, npm:three |
| `COLOR-58` | تمريرة المظهر | Look pass: gamut mask, Purkinje night vision, split toning | ready | chromium, npm:three |
| `COLOR-59` | المنظور الجوي | Aerial perspective: 3-channel fog, fog toward the sun, sky bounce | ready | chromium, npm:three |
| `COLOR-60` | تمريرة تلوين الشيدر | Shader grade pass driven by story or music | ready | chromium, npm:three |
| `COLOR-61` | ألوان مصادر الضوء العملية | Named practical light colours (sodium, mercury, moon, flame) | ready | chromium, npm:three |
| `COLOR-69` | تحريك تدرج السماء ووقت اليوم | Sky-stop tweening: time of day and seasons | ready | npm:gsap |
| `COLOR-70` | التلوين كقصة | Grade change as story (drain, bloom, freeze to grey) | ready | npm:gsap |
| `MEDIA-35` | إزالة الخلفية محليًا بنموذج ONNX تختاره أنت | Remove a background offline with a user-supplied ONNX matte model | ready | pip:numpy, pip:pillow, pip:onnxruntime |
| `MEDIA-36` | ملء ذكي محلي لمنطقة محددة بقناع | Smart fill a masked area offline (MI-GAN-style ONNX) | ready | pip:numpy, pip:pillow, pip:onnxruntime |
| `MEDIA-37` | نماذج مثبتة بالبصمة: تحقق قبل التشغيل | Commit-pinned models: verify SHA-256 before use | ready | pip:onnxruntime |
| `FOOT-02` | تنزيل لقطة مفتوحة مع إيصال مصدر | Open-footage downloader with provenance | ready | python3 |
| `FOOT-05` | مكتبة وسائط محلية مع فحص | Local media library with probe | ready |  |
| `FOOT-10` | اختيار أنشط نافذة في اللقطة | Motion-energy window picking | ready | imagemagick |
| `FOOT-12` | تحليل تعريض الصورة ونصائح بالعربية | Image exposure analysis + Arabic fix advice | ready | python3 |
| `FOOT-14` | تحليل فيديو مرجعي إلى نبضات | Video breakdown to beats | ready |  |
| `FOOT-17` | قص دقيق بالإطار | Frame-accurate trim (re-encode) | ready | ffmpeg, python3 |
| `FOOT-18` | دمج مقاطع مختلفة دون كسر الصوت | Fit-and-join concat | ready | python3 |
| `FOOT-20` | قص الصمت | Silence jump-cut | ready | python3, npm:hyperframes |
| `FOOT-21` | تجميد إطار وتكرار حلقة | Freeze frame & loop | ready | ffmpeg, npm:hyperframes |
| `FOOT-22` | محرر KOSIF Studio في المتصفح | KOSIF Studio browser montage editor | ready | ffmpeg, imagemagick |
| `FOOT-30` | معالجة الصور بـ ImageMagick | ImageMagick still post-processing | ready | imagemagick |
| `FOOT-34` | تسمية متتبعة ودائرة اهتمام | Tracked callout & attention ring | ready | pip:opencv |
| `FOOT-40` | بارالاكس مستوي بمعاملات عمق | Planar parallax with depth factors | ready | npm:remotion |
| `FOOT-45` | أساليب الصور الجاهزة | Photo styles to scaffold | ready | python3, imagemagick |
| `FOOT-49` | لقطة متحدث تحت الرسوم | Real footage plate under graphics | ready |  |
| `FOOT-50` | محرك المونتاج الموجّه | Directed-edit engine | ready | npm:gsap |
| `FOOT-55` | ريل من مقطع كلام بأمر واحد | One-command talking-clip reel | ready | pip:faster-whisper |
| `GEN-01` | تشريح البرومبت السباعي والمعادلة الذهبية | Seven-layer prompt anatomy & golden formula | documented |  |
| `GEN-03` | قائمة النفي الأساسية والصياغة الإيجابية | Negative baseline vs positive framing | documented | key:video-gen |
| `GEN-04` | معادلة برومبت الصورة ذات الخانات الست | Six-slot still prompt formula | documented |  |
| `GEN-05` | برومبت سردي لنانو بنانا / Gemini | Narrative prose brief for Gemini / Nano Banana | documented | key:video-gen |
| `GEN-06` | دليل صياغة كل مولّد وترجمة صيغة ميدجورني | Per-generator syntax & Midjourney→natural-language translation | documented | key:video-gen |
| `GEN-07` | معادلة برومبت لقطة الفيديو | Video shot prompt formula | documented | key:video-gen |
| `GEN-08` | منع الموسيقى والترجمة المزيفة في الفيديو المولد | Suppress generated music bed & fake subtitles | documented | key:video-gen |
| `GEN-09` | حدود مولدات الفيديو الحالية | Known limits of current video generators | documented | imagemagick |
| `GEN-25` | مثال مصر 2120: حزمة برومبتات كاملة | Worked example: Egypt 2120 multi-platform pack | documented | key:video-gen, fonts:arabic |
| `GEN-26` | كتالوج الأساليب المسماة (أكثر من 30 مظهرًا) | Named look catalogue (30+ looks) | documented |  |
| `GEN-27` | مقدمات الأسلوب المتطابقة بايتًا | Byte-identical style preambles | documented |  |
| `GEN-28` | استخراج قفل الأسلوب | Style-lock extraction | documented |  |
| `GEN-29` | مكتبات المعدِّلات حسب المجال وقوالب التصوير | Domain modifiers, photo templates & camera bodies | documented |  |
| `GEN-30` | مفردات التلوين وحزم أسلوب الفيديو | Grade vocabulary, film stocks & video style packs | documented |  |
| `GEN-31` | وصفات أساليب كلينج بنطاقات cfg_scale | Kling style recipes with cfg_scale bands | documented | key:video-gen |
| `GEN-32` | البرومبت العكسي ونقد الصورة | Reverse prompt & image critique | documented | tesseract, key:video-gen |
| `GEN-46` | شجرة اختيار نموذج الصور والترخيص أولًا | Image-model routing tree (licence first) | documented | key:video-gen |
| `GEN-47` | وصفات ComfyUI: المُعيِّن والجدولة وقياس منحنيات الضوضاء | ComfyUI sampler/scheduler recipes & measured sigma curves | documented |  |
| `GEN-48` | LoRA وControlNet والترميم في ComfyUI | ComfyUI LoRA bands, ControlNet & inpainting | documented |  |
| `GEN-49` | شجرة اختيار نموذج الفيديو ومسودة رخيصة ثم نهائي | Video-model routing tree & cheap draft → premium final | documented | key:openai, key:video-gen |
| `GEN-50` | صورة مفتاحية أولًا ثم تحريكها | Keyframe-first image-to-video | documented |  |
| `GEN-62` | فيديو مفتوح الأوزان: Wan 2.x وLTX وAnimateDiff | Open-weights video: Wan 2.x, LTX-Video, AnimateDiff | documented | pip:torch |
| `GEN-63` | وصلة Higgsfield كمسار برومبت فقط | Higgsfield / paid clip route as prompt-only deliverable | documented | pip:higgsfield |
| `GEN-65` | كلمات أغنية وموجز Suno/Udio | Song lyrics + Suno/Udio brief | documented | key:video-gen |
| `GEN-71` | البحث في مكتبة برومبتات المالك | Owner prompt-system corpus search | documented |  |
| `GEN-83` | فرز: توليد أم تركيب | Generate-or-compose triage | documented |  |
| `GEN-84` | النص فوق الصورة لا داخلها | Overlay text, never bake it | documented | npm:remotion |
| `GEN-85` | المراسي الأربع للثبات البصري | Four anchors of visual consistency | documented |  |
| `GEN-87` | الترخيص أولًا وFirefly المحمي قانونيًا | Licence-first model choice & indemnified Firefly | documented | key:unspecified |
| `GEN-88` | الإفصاح عن الوسائط المصطنعة وحدود التوليد | Synthetic-media disclosure, provenance & ethical limits | documented |  |
| `GEN-G01` | خط إنتاج من موضوع إلى فيديو قصير | Topic-to-short pipeline with reviewable stages | documented | node, python3, chromium |
| `GEN-X02` | توليد متصل ثم قص | One continuous generation, then cut | documented |  |
| `AMEDIA-01` | تحويل نص لصوت واستنساخ وMؤثرات ElevenLabs | ElevenLabs TTS, cloning and sound effects | documented | key:elevenlabs, key:unspecified |
| `AMEDIA-02` | فحص تسليم المزيج النهائي ليوتيوب 4K | Final mix delivery check for YouTube 4K | documented | ffmpeg |
| `AMEDIA-03` | مجموعات مؤثرات لعبة بمستويات صوت | Game SFX sets with loudness classes | documented |  |
| `AMEDIA-04` | تفريغ سحابي مع فصل المتحدثين والتوقيت | Hosted STT with diarization and timestamps | documented | pip:pyannote |
| `AMEDIA-05` | إصلاح انحراف التوقيت في دمج الصوت | Joined-audio timestamp drift fix | documented | ffmpeg |
| `AMEDIA-06` | تفريغ محلي بـ whisper للملفات والبث | Local whisper transcription of files and live streams | documented | ffmpeg, yt-dlp, pip:faster-whisper |
| `AMEDIA-07` | صياغة كلمات الأغاني وموجّهات Suno | Lyrics and Suno music prompt crafting | documented | key:elevenlabs, key:video-gen |
| `AMEDIA-08` | صوت PipeWire داخل الحاويات | PipeWire audio in containers | documented | docker |
| `AMEDIA-09` | صوت ألعاب إجرائي بالكود | Procedural game audio from Python code | documented | ffmpeg, pip:numpy, pip:scipy |
| `AMEDIA-10` | مقطوعة مُصنَّعة بحلقات متصلة | Synthesized score with seamless loops | documented |  |
| `AMEDIA-11` | اختيار طبقة ASR/TTS لوكيل صوتي | Voice-agent ASR/TTS stack selection | documented |  |
| `AMEDIA-12` | توليد ومعايرة شرائط السبرايت | Anchored sprite strip generation and normalization | documented | python3 |
| `AMEDIA-13` | تريلر من لعب آلي حقيقي | Gameplay trailer from bot playthroughs | documented | ffmpeg |
| `AMEDIA-14` | صورة شرح تعليمية أحادية اللون | Monochrome learning explainer image | documented |  |
| `AMEDIA-15` | حركة نابضية وسطح زجاجي لمواقع بمستوى Awwwards | Spring-physics motion and a layered glass surface | documented | npm:gsap, npm:animejs |
| `AMEDIA-16` | نموذج الشيدر في React Three Fiber | GLSL shader mental model in React Three Fiber | documented | npm:three, npm:react |
| `AMEDIA-17` | هيرو بخط حركي منفوخ تتصادم حروفه | Kinetic inflated typography hero | documented | npm:matter |
| `AMEDIA-18` | حقل حراري يلطّخه الإصبع (شيدر واحد) | Thermal finger-trail field in one fragment shader | documented | npm:three |
| `AMEDIA-19` | انتقالات العرض في React حسب ما تعنيه الحركة | React View Transitions chosen by meaning | documented | chromium, npm:react |
| `AMEDIA-20` | حزمة تسليم من موجز إلى فيلم | Brief-to-film handoff kit with a named upload order | documented |  |
| `AMEDIA-21` | فيديو عرض المنتج بأنماط احتياطية | Product demo video pipeline with fallback modes | documented | ffmpeg |
| `AMEDIA-22` | تشخيص FFmpeg: إطار متغير، HLS متعدد الدقات، فحص التيار | FFmpeg diagnostics: VFR fix, aligned ABR HLS, stream health | documented | ffmpeg |
| `AMEDIA-23` | قص بلا فقد على الإطارات المفتاحية | Lossless keyframe-aligned cutting and smart cut | documented | ffmpeg |
| `AMEDIA-24` | مشهد After Effects بالسكربت: المواصفات أولاً | Scripted After Effects comps: spec first, rigs, render queue | documented |  |
| `AMEDIA-25` | تغليف الفيديو: عنوان ونص مصغّرة لا يتكرران | Video packaging: title and thumbnail text that never overlap | documented |  |
| `AMEDIA-26` | Substance Painter: مساحة لون PBR وخبز الخرائط | Substance Painter PBR colour space and baking | documented | python3, chromium |
| `AMEDIA-27` | Godot 4: سكربت مُنمّط وفيزياء وتصدير بلا واجهة | Godot 4: typed GDScript, physics timing, headless export | documented | chromium |
| `COLOR-08` | مكتبة اللوكات المسماة | Named film-stock and photo looks library | documented | pip:numpy, key:unspecified |
| `COLOR-13` | ترتيب عقد التلوين | Grade order: technical before creative | documented | ffmpeg |
| `COLOR-20` | لوكات مقاسة بأهداف السكوب | Scope-target looks (Japan summer, New York, Still, Tokyo night) | documented |  |
| `COLOR-21` | توجيه التلوين حسب اللقطة وأرضية الإضاءة | Per-shot-type direction, one light floor, value before colour | documented |  |
| `COLOR-43` | مكتبات باليتات جاهزة | Ready palette libraries (families, deck presets, recut themes, demo kit, dark ladders) | documented |  |
| `COLOR-44` | اللون حسب العاطفة والقطاع والثقافة | Brand colour by emotion, sector and culture | documented |  |
| `COLOR-47` | خرائط الألوان وتسلسل الرسم البياني | Colormap semantics and chart colour hierarchy | documented |  |
| `COLOR-51` | تدرجات إدراكية OKLCH وظلال بإزاحة الصبغة | Perceptual OKLCH ramps and hue-shifted shading | documented | chromium, npm:remotion |
| `COLOR-53` | الوضع الداكن بلا قلب | Dark variant without inversion | documented |  |
| `COLOR-82` | توحيد الطبقات | Unify the stack: one grade, grain, vignette | documented |  |
| `COLOR-83` | سلم المعالجة | Treatment ladder: colour → duotone → halftone → vector | documented | ffmpeg, npm:hyperframes |
| `COLOR-X01` | حزمة أسلوب مقيسة والتدريج بالقياس | Measured style pack and grading by measurement | documented |  |
| `MEDIA-38` | مصمم: محرر صور عربي أولًا بطبقات وأقنعة وتعديلات غير مدمّرة | Mosamem: Arabic-first image editor with layers, masks and non-destructive adjustments | documented | node |
| `MEDIA-39` | مصمم: فتح PSD بطبقاته وحفظ نسخة بطبقات | Mosamem: open layered PSD files and save a layered copy | documented |  |
| `MEDIA-40` | مصمم: تحديد عنصر بنقرة أو مربع (SAM 2.1 محليًا) | Mosamem: select an object from a click or a box (SAM 2.1 tiny, local) | documented | python3 |
| `FOOT-01` | انضباط ترخيص الصور واللقطات | Media licensing discipline | documented |  |
| `FOOT-04` | مجمع لقطات بأسئلة بحث ثنائية اللغة | Per-shot bilingual footage pool | documented |  |
| `FOOT-06` | تايملاين زمني متعدد الكاميرات | Chronological multi-camera timeline | documented | ffmpeg |
| `FOOT-07` | إعدادات تسجيل الشاشة | Screen-capture defaults | documented |  |
| `FOOT-11` | قص البدايات المعيبة وتجميع المكرر | Bad-head trimming & duplicate-take grouping | documented | pip:numpy, pip:pillow, pip:opencv |
| `FOOT-15` | تشخيص قبل رفع الدقة | Upscale triage | documented | ffmpeg |
| `FOOT-32` | عنوان خلف المتحدث | Title behind the speaker | documented | pip:z3 |
| `FOOT-35` | إدراج بمنظور مثبت بأربع نقاط | Planar corner-pin inserts | documented | ffmpeg, pip:opencv |
| `FOOT-36` | تجميد الشخص والعالم يمشي | Freeze the subject, keep the world moving | documented |  |
| `FOOT-38` | مقارنة قبل وبعد صادقة | Honest before/after wipe | documented | ffmpeg |
| `FOOT-41` | كشف بارالاكس ثلاثي ومن الكولاج إلى البطل | Three-layer reveal & collage → hero | documented |  |
| `FOOT-42` | حماية النص فوق الصور واللقطات | Text protection over photos & footage | documented | ffmpeg |
| `FOOT-43` | صورة أرشيف تنفتح على الحاضر | Archive photo opens onto the present | documented | fonts:arabic |
| `FOOT-44` | قواعد الصور للعربية | RTL photo layout rules | documented |  |
| `FOOT-P01` | إعادة مونتاج اللقطات من قائمة قطع محدودة | Bounded EDL recut: trim/concat with denoise and loudnorm | documented | ffmpeg |
| `FOOT-U01` | مطابقة المسودة بلقطات المصدر | Match a draft back to its source shots | documented |  |
| `FOOT-U02` | كاشف القفزات: اقطع قبل القفزة | Jump-cut finder: cut on the frame before | documented |  |
| `FOOT-U03` | قناع شخص بلا تعلم آلي | Person matte without ML | documented |  |
| `FOOT-X01` | انضباط مونتاج المادة الحقيقية | Real-footage edit discipline (source-to-programme map) | documented |  |
| `FOOT-X02` | فحص القدرة واختبارات قصيرة قبل التصدير | Capability preflight and short tests before an expensive export | documented |  |
| `FOOT-X04` | طبقات أدوات المونتاج وحالات المشروع | Footage editing layers and project-state hygiene | documented | ffmpeg, npm:remotion |
| `FOOT-X05` | عقد محاكاة فيديو مرجعي | Reference-video imitation contract (8 steps) | documented | ffmpeg, key:video-gen |
| `GEN-75` | بطاقات توليد من الضبابية إلى الوضوح | Blur-to-sharp 'Generating…' tiles | seen |  |
| `GEN-76` | صورة مولدة كمحتوى بطل داخل واجهة | AI photo as the 'result' inside a UI mock | seen |  |
| `GEN-77` | شريط استعراض أصول مولدة بإخراج فني واحد | AI-generated asset showreel with one art direction | seen |  |
| `GEN-78` | عمل فني سائل قزحي | Iridescent liquid artwork (generated or shaded) | seen |  |
| `GEN-79` | لقطة صلصال مولدة | Claymation AI shot | seen | ffmpeg |
| `GEN-80` | خلفية لوحة زيتية مولدة بحركة كن برنز | Painterly AI backdrop with slow Ken Burns | seen |  |
| `GEN-81` | كولاج مقصوص وبوابات زووم لا نهائي | Cutout collage portals for infinite zoom (generated or sourced cutouts) | seen | ffmpeg, pip:rembg |
| `COLOR-55` | أنظمة لونين أو ثلاثة صارمة | Strict two- and three-colour systems | seen |  |
| `COLOR-67` | فصول وضربات بحقول لونية | Colour-field chapter and beat flips | seen | npm:gsap, npm:hyperframes |
| `COLOR-68` | ضربة لون كامل للإطار | Full-bleed accent beat / brand flash fill | seen |  |
| `COLOR-71` | منطق الألوان السردي | Narrative colour logic (problem → solution) | seen |  |
| `COLOR-72` | لون لكل عنصر | Per-item hue coding at equal luminance | seen |  |
| `COLOR-73` | صبغة الإطار للحدث | Full-frame event tint and flash | seen |  |
| `COLOR-74` | حلقات بتدرج الصبغة ودوران اللون | Hue-indexed rings and slow hue rotation | seen |  |
| `COLOR-75` | عنوان بلونين وكلمة مميزة | Two-tone headline and accent word | seen |  |
| `COLOR-76` | شريط عينات الألوان | Swatch-strip reveal | seen |  |
| `COLOR-79` | أرضية ورقية كريمية | Warm paper editorial ground | seen |  |
| `COLOR-84` | تشطيب الكولاج العتيق مع الوميض | Vintage collage finish with exposure flicker | seen | ffmpeg |
| `COLOR-85` | لوحات الغروب والسايكدلك والدفع الأحادي | Sunset/synthwave, psychedelic and monohue-push palettes | seen | ffmpeg |
| `COLOR-86` | طين أبيض ولون للبيانات فقط | White clay render with colour only for data | seen |  |
| `FOOT-33` | متحدث مقصوص فوق عوالم متبدلة | Rotoscoped speaker over swapped worlds | seen |  |
| `FOOT-46` | شرائح الفلاتر وجدار الصور | Filter strips & tile walls | seen |  |
| `GEN-36` | صورة فوتوغرافية محلية sd-turbo أو Pollinations | Photo from prompt: local sd-turbo or Pollinations | install | pip:torch, network |
| `GEN-45` | تعديل قبل إعادة التوليد: توسيع وترميم وقص وتكبير | Edit before regenerate: outpaint, inpaint, cut-out, upscale | install | ffmpeg, pip:rembg |
| `GEN-74` | واجهات «جارٍ التوليد» من HyperFrames | AI-UI motion blocks (streaming text, typed prompt, chat reveal…) | install | npm:hyperframes |
| `COLOR-09` | نموذج تلوين HyperFrames | HyperFrames WebGL grade model, 17 presets and media-treatment CLI | install | npm:three, npm:hyperframes |
| `COLOR-10` | وصفات المعالجة وممرات الملاحظات | HyperFrames treatment recipes and feedback lanes | install | npm:hyperframes |
| `COLOR-11` | لوكات LUT مع بديل حتمي | LUT looks with deterministic buildCube fallback | install | npm:hyperframes |
| `COLOR-12` | كشف التلوين بالمقارنة | Grade Split Reveal (flat → graded sweep) | install | npm:three, npm:hyperframes |
| `COLOR-28` | إصلاح تلقائي ومطابقة مرجع في «بصمة» | Basma measured auto-fix, reference match and look classifier | install | npm:esbuild |
| `COLOR-30` | ألوان الشعار الحقيقية | Logo true colours + antialias-blend detection | install | chromium, pip:opencv |
| `COLOR-80` | خلفية بقع ضبابية متحركة | Drifting blob / mesh-gradient ambient ground | install | npm:gsap, npm:hyperframes |
| `COLOR-81` | لوحات شيدر WebGPU | WebGPU shader colour plates | install | chromium, npm:hyperframes |
| `MEDIA-07` | OCR بديل عبر pip | easyocr (pure-pip OCR) | install | tesseract, pip:torch, network |
| `MEDIA-25` | تحويل الكلام إلى نص محليًا | Local speech-to-text (faster-whisper) | install | pip:faster-whisper, network |
| `MEDIA-26` | فصل المسارات الصوتية | Stem separation (demucs) | install | pip:torch |
| `MEDIA-27` | إزالة الخلفية محليًا | Background removal (rembg) | install | pip:rembg |
| `MEDIA-28` | بيانات الصور الوصفية | Image metadata (EXIF) | install | pip:pillow |
| `MEDIA-30` | صيغ HEIC وصور الهواتف | HEIC/HEIF input from phones | install | pip:pillow |
| `MEDIA-32` | MediaPipe: تتبع الوجوه واليدين ووضعية الجسم لإعادة التأطير | MediaPipe: Track faces, hands and pose in footage for auto-reframing and overlays | install | pip:mediapipe |
| `MEDIA-33` | Ultralytics YOLO: كشف الأجسام وتقسيمها وتتبعها في الصور والفيديو | Ultralytics YOLO: Detect, segment and track objects in images and video | install | pip:ultralytics |
| `MEDIA-41` | مصمم: نواة البكسل مختبرة (دمج وتعديلات وتحديد ورسم) | Mosamem core: tested pixel math (blend modes, adjustments, selection, painting) | install | git |
| `FOOT-03` | جلب من المنصات مع الاعتمادات | Social/Pinterest fetch with credits (yt-dlp) | install | python3, yt-dlp |
| `FOOT-23` | مونتاج مستقل أو متتابع في Remotion | Remotion clip editing: independent vs ripple | install | ffmpeg, npm:remotion |
| `FOOT-27` | تمويه الوجوه والمناطق | Face & region privacy masks | install | ffmpeg, pip:opencv, pip:scipy, pip:onnxruntime |
| `FOOT-31` | عزل الشخص بقناع شفاف | Person matte / background removal | install | pip:torch, pip:rembg, npm:hyperframes, pip:mediapipe |
| `FOOT-37` | سينماغراف | Cinemagraph | install | npm:hyperframes |
| `FOOT-51` | إعادة تغليف المتحدث ببطاقات | Talking-head recut with designed cards | install | ffmpeg, npm:hyperframes |
| `FOOT-52` | فيديو ولوتي داخل HTML | Video & Lottie inside HTML compositions | install | npm:lottie |
| `GEN-37` | توليد وتعديل الصور بـ Gemini (نانو بنانا) | Gemini / Nano Banana image generate & edit | key | python3, key:video-gen |
| `GEN-38` | تحرير بمراجع متعددة قبل التحريك (نانو بنانا) | Nano Banana multi-reference edit before animation | key | key:video-gen |
| `GEN-39` | عائلة FLUX عبر Together وحلقة Kontext | FLUX via Together + Kontext edit round-trip + LoRA | key | python3, key:unspecified |
| `GEN-40` | GPT Image وIdeogram للصور ذات النص | GPT Image & Ideogram V4 (text-capable stills, edit, describe) | key | key:openai, key:video-gen |
| `GEN-41` | صور Higgsfield (Soul v2 / Marketing Studio / gpt_image_2) | Higgsfield image generation | key | pip:higgsfield |
| `GEN-42` | وصفة صور الهوية: كائن معدني وكريستال (ذهبي/جليدي) | Brand-still recipe: metal + crystal object on brand ground | key | pip:higgsfield |
| `GEN-43` | لقطات بمساحة فارغة للكتابة | AI plates that reserve typography space | key | key:unspecified |
| `GEN-44` | أيقونات شفافة بثيم وشرائط سبرايت ثابتة | Themed transparent icons & consistent sprite strips | key | pip:pillow, pip:rembg, key:openai |
| `GEN-51` | Seedance 2.5 عبر Higgsfield (محروس ومدفوع) | Seedance 2.5 text/image-to-video via Higgsfield (guarded) | key | pip:higgsfield, key:video-gen |
| `GEN-52` | حلقات فيديو Kling للهوية وواجهة Kling | Kling text/image-to-video API (+ real brand loops) | key | key:video-gen |
| `GEN-53` | فرشاة الحركة والقناع الثابت (سينماغراف) | Kling motion brush & static mask (cinemagraph) | key | key:video-gen |
| `GEN-54` | تمديد فيديو Kling بالتسلسل ونظام الرصيد | Kling extension chain & credit model | key | key:video-gen |
| `GEN-55` | واجهة Runway حسب النموذج والتزامن | Runway task API & concurrency model | key | key:video-gen |
| `GEN-56` | قواعد المراجع في Seedance 2.0 R2V | Seedance 2.0 reference-to-video grammar | key | pip:higgsfield, key:video-gen |
| `GEN-57` | لقطة أداء مولدة متزامنة مع مقطع الأغنية | Reference-to-video performance shot synced to a song slice | key | ffmpeg, key:video-gen |
| `GEN-58` | ثبات الصوت عبر مرجع صوتي | Voice continuity via reference audio | key | ffmpeg, key:unspecified |
| `GEN-59` | Veo عبر Gemini وقيود Sora 2 | Veo via Gemini & Sora 2 constraints | key | key:openai, key:video-gen |
| `GEN-60` | منصات التجميع: fal وTogether وWaveSpeed وHF Spaces وVertex | Aggregator hubs: fal, Together, WaveSpeed, HF Spaces, Vertex | key | pip:faster-whisper, key:video-gen |
| `GEN-61` | خياطة الإطارات وسلاسل البداية/النهاية | Frame stitching & start/end-image chains for long AI video | key | ffmpeg, key:video-gen |
| `GEN-64` | توليد الموسيقى: Lyria وMusicGen | Music generation: Lyria & MusicGen | key | python3, npm:hyperframes, key:unspecified |
| `GEN-66` | أمر واحد لجلب أي وسائط | Media resolve: one verb for any asset | key | npm:hyperframes, key:unspecified |
| `GEN-67` | مقدم افتراضي ودبلجة وترجمة فيديو وتكبير | Avatar presenter, dub, video translate & upscale | key | npm:hyperframes, key:unspecified |
| `GEN-68` | توليد مجسمات ثلاثية بالذكاء | Text/image → 3D model (Meshy, Tripo, Rodin, TRELLIS) | key | npm:three, npm:react, key:unspecified |
| `GEN-69` | توجيه مزودي الإبداع وشبكة الموصلات | Creative provider routing & connector mesh | key | pip:higgsfield, key:video-gen, key:unspecified |
| `GEN-70` | خوادم المالك: KOSIF Think وJev والمنصة الخاصة | Owner MCP runtimes: KOSIF Think, Jev arbiter, private Workbench | key | node, python3, key:unspecified |
| `GEN-72` | الرسم فوق لقطات مولدة (Draw-over) | Draw-over on generated bases | key | chromium, key:unspecified |
| `GEN-82` | فيلم موشن بستوري بورد يكتب Claude كوده | Storyboard-first motion film with Claude-written, sandboxed scene code | key | key:unspecified |
| `GEN-90` | خدمة الصور المصغرة المدفوعة | Thumbnail generation via paid MCP | key | key:openai, key:unspecified |
| `GEN-P01` | مراجعة ثانية مدفوعة من Claude API بقفلين | Optional paid Claude API second-opinion review (double opt-in) | key | ffmpeg, pip:anthropic, key:unspecified |
| `GEN-X01` | إنتاج فيديو مرجعي عبر Higgsfield | Higgsfield reference-video production parameters and prompt skeleton | key | pip:higgsfield, key:unspecified |
| `MEDIA-29` | توليد وتحسين الصور والأصوات بالذكاء الاصطناعي (مدفوع) | AI image/audio generation and upscaling (paid connector) | key | pip:higgsfield, key:unspecified |
| `MEDIA-34` | pyannote.audio: تحديد من تحدث ومتى لبناء ترجمة لكل | pyannote.audio: Label who spoke when, for per-speaker captions | key | pip:pyannote |
| `FOOT-56` | ريلز من فيديو طويل | Reels from a long video | key | key:unspecified |
| `FOOT-57` | المونتاج الذكي الكامل من الكلام | Smart full montage from speech (AutoEdit) | key | imagemagick, key:unspecified |
| `FOOT-58` | مونتاج لقطات المستخدم على الإيقاع (بصمة) | Basma automatic beat montage | key | imagemagick, key:unspecified |
| `GEN-73` | توليد ثم تتبّع | Generate-then-trace | idea | ffmpeg, pip:vtracer, npm:gsap, npm:remotion |
| `COLOR-77` | باليت مفهرسة من 16 لونًا | Indexed 16-colour palette with alternating accent flash | idea | pip:pillow, npm:hyperframes |
