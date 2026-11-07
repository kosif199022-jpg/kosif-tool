# الأدوات اللي لازم تتحمل — بروتوكول مونتاج التنين الأسود

لما تقول «التنين الأسود، مونتاج» ومعاك فيديو، التنين بيعدّي على ٧ محطات. الصفحة دي بتقولك بالظبط إيه اللي لازم يبقى متثبت على جهازك عشان كل محطة تشتغل كويس، وإيه اللي بيقع لو أداة ناقصة.

القائمة الرسمية (اللي الكود بيقراها) في `data/required_tools.json`. الصفحة دي شرح ليها.

## اتأكد في ثانية

```bash
python3 .claude/skills/kosif-dragon-montage/scripts/dm_doctor.py doctor            # جدول + حكم لكل محطة
python3 .claude/skills/kosif-dragon-montage/scripts/dm_doctor.py install-plan --os windows   # أوامر التثبيت للناقص بس
```

- الـ doctor **مبيثبتش حاجة**؛ بيكشف بس. بيطلع بـ exit 0 لو كل الأدوات «اللازمة» موجودة.
- عشان تثبّت: على ويندوز شغّل `scripts/install_tools.ps1`، وعلى لينكس/ماك `scripts/install_tools.sh`. الاتنين بيثبتوا الناقص بس، ولو شغّلتهم تاني مش هيعملوا حاجة.
- مكتبات بايثون بتتحط في `.venv` جوه الريبو؛ شغّل المونتاج بـ `.venv\Scripts\python.exe` (ويندوز) أو `.venv/bin/python`.

## المحطات

| المحطة | اسمها | الأدوات اللازمة ليها |
|---|---|---|
| `analyze` | العين الأولى | Python 3.10+, FFmpeg, FFprobe, NumPy, Pillow |
| `think` | يفهم المطلوب ويفكر بإبداع | Python 3.10+ |
| `taste` | يختار الذوق | Python 3.10+, NumPy |
| `direct` | يكتب المونتاج | Python 3.10+ |
| `render` | يرندر | Python 3.10+, FFmpeg, FFprobe |
| `review` | يتفرج وينقد | Python 3.10+, FFmpeg, FFprobe, NumPy, Pillow |
| `generate` | يولّد الناقص | Python 3.10+, FFmpeg, FFprobe |

## ١) لازم — من غيرها المحطة متشتغلش

| الأداة | ليه مهمة | لو مش موجودة | الحجم | ويندوز |
|---|---|---|---|---|
| **Python 3.10+** | اللغة اللي كل محطات المونتاج مكتوبة بيها | مفيش ولا محطة تشتغل | ~100 MB | winget `Python.Python.3.13` |
| **FFmpeg** | القص والتركيب والتلوين والانتقالات والصوت والترجمة المحروقة والتصدير | مفيش رندر خالص؛ مفيش استخراج صوت ولا صور للفحص | ~80-150 MB | winget `Gyan.FFmpeg` |
| **FFprobe** | يقيس الفيديو: المدة والأبعاد والفريمات ووجود الصوت | المحطة الأولى متقدرش تقرا الفيديو؛ والتحقق من الرندر يقع | بييجي مع ffmpeg | winget `Gyan.FFmpeg` |
| **NumPy** | حسابات الجودة (حدة/إضاءة/اهتزاز) وطاقة الصوت | مفيش تقييم للقطات، فاختيار أحسن لقطة بيبقى عشوائي | ~40 MB | `py -m pip install "numpy>=1.26"` |
| **Pillow** | صور مصغرة للقطات وورقة المعاينة وفريمات المراجعة | مفيش contact sheet ولا فريمات للنقد | ~10 MB | `py -m pip install "pillow>=10"` |

## ٢) مهمة — من غيرها الشغل بيطلع أضعف بوضوح

| الأداة | ليه مهمة | لو مش موجودة | الحجم | ويندوز |
|---|---|---|---|---|
| **faster-whisper** | تفريغ الكلام العربي بتوقيت كل كلمة: ترجمة كاريوكي وقص على الكلام | مفيش ترجمة ولا قص على الجمل؛ الإيقاع بيعتمد على السكوت بس | ~100 MB + موديل small ~480 MB أول تشغيل | `py -m pip install "faster-whisper>=1.0"` |
| **PySceneDetect** | يلاقي القطعات (حدود اللقطات) بدقة | بيرجع لفلتر scene في ffmpeg وهو أقل دقة | ~5 MB | `py -m pip install "scenedetect>=0.6.4"` |
| **OpenCV (headless)** | قراءة الفريمات: الحدة والاهتزاز والوشوش والحركة وإعادة التأطير 9:16 | مفيش عدّ وشوش ولا قياس اهتزاز؛ والـ reframe بيبقى في النص بس | ~60 MB | `py -m pip install "opencv-python-headless>=4.9"` |
| **librosa** | يحسب BPM والبيتات عشان القطع يبقى على الإيقاع | القص على البيت مش متاح وفحص cuts-on-beat بيتخطى | ~60 MB (مع scipy/numba) | `py -m pip install "librosa>=0.10"` |
| **soundfile** | قراءة ملفات الصوت WAV لـ librosa و faster-whisper | librosa ممكن يفشل في قراءة الصوت | ~3 MB | `py -m pip install "soundfile>=0.12"` |
| **yt-dlp** | ينزل الفيديو من لينك تيك توك/إنستجرام/يوتيوب | لازم تدي الملف نفسه، مش لينك | ~15 MB | winget `yt-dlp.yt-dlp`, `py -m pip install yt-dlp` |
| **Node.js 18+** | يشغّل رندر HTML (العناوين والجرافيك) و Remotion و HyperFrames | مفيش عناوين متحركة/جرافيك HTML؛ الرندر بيبقى ffmpeg بس | ~90 MB | winget `OpenJS.NodeJS.LTS` |
| **Playwright** | يفتح صفحة HTML ويصوّرها فريم فريم | مفيش رندر لمشاهد HTML | ~10 MB | `npm i playwright@1.64.1` |
| **Chromium (Playwright browser)** | المتصفح اللي Playwright بيرندر بيه | Playwright موجود بس مش لاقي متصفح | ~170 MB | `node .kosif-node/node_modules/playwright/cli.js install chromium` |
| **Arabic font (Cairo / Noto Sans Arabic / Amiri)** | خط عربي سليم للترجمة المحروقة | الحروف العربية بتطلع مربعات أو مقطعة | ~1-30 MB | يدوي — شوف install-plan |

## ٣) إضافات — بتفتح مزايا زيادة (ثبّت اللي محتاجه بس)

| الأداة | ليه مهمة | لو مش موجودة | الحجم | ويندوز |
|---|---|---|---|---|
| **OpenTimelineIO** | يصدّر المونتاج لبريمير/ريزولف/فاينل كت كمشروع يتعدل | التصدير بيبقى FCPXML/EDL بس من غير قراءة تأكيد | ~5 MB | `py -m pip install "opentimelineio>=0.17"` |
| **MediaPipe** | تتبع ملامح الوش عشان القص الرأسي يفضل على الشخص | الـ reframe بيعتمد على OpenCV بس | ~50 MB | `py -m pip install mediapipe` |
| **pyloudnorm** | تأكيد ثاني لعلو الصوت LUFS | بيكتفي بقياس ffmpeg ebur128 | ~1 MB | `py -m pip install pyloudnorm` |
| **pedalboard** | تلميع الصوت: كومبريسور وإيكو وفلاتر | التلميع بيبقى فلاتر ffmpeg بس | ~20 MB | `py -m pip install pedalboard` |
| **imageio-ffmpeg** | نسخة ffmpeg احتياطي من pip لو مفيش ffmpeg على الجهاز | — | ~30 MB | `py -m pip install imageio-ffmpeg` |
| **PyTorch (CPU)** | المحرك اللي Demucs و WhisperX و EasyOCR محتاجينه | Demucs/WhisperX/EasyOCR ميشتغلوش | ~700 MB (CPU) | يدوي — شوف install-plan |
| **Demucs** | يفصل الصوت عن المزيكا (stems) | مفيش فصل صوت؛ الـ ducking بيبقى على الميكس كله | ~80 MB موديل + torch | `py -m pip install demucs` |
| **WhisperX** | محاذاة دقيقة جدًا لكل كلمة (كاريوكي مظبوط) | توقيتات faster-whisper كفاية في أغلب الحالات | ~1.2 GB موديل عربي + torch | `py -m pip install whisperx` |
| **EasyOCR** | يقرا الكلام المكتوب على الفيديو (عربي) | مش هيعرف إن فيه كلام محروق فممكن الترجمة تركب عليه | ~100 MB موديلات + torch | `py -m pip install easyocr` |
| **Tesseract OCR (+ara)** | OCR خفيف للنصوص الواضحة | —؛ ضعيف مع الخطوط المزخرفة | ~40 MB | winget `UB-Mannheim.TesseractOCR`, `py -m pip install pytesseract` |
| **Remotion (starters/remotion)** | جرافيك React متحرك (عناوين، لوجو، intro/outro) | العناوين بتبقى HTML/ffmpeg بس | ~300 MB node_modules | `npm ci --prefix starters/remotion` |
| **HyperFrames** | يحوّل تكوينات HTML لفيديو | — | ~50 MB | `npm i hyperframes@0.8.164` |
| **Manim** | أنيميشن شرح ورسوم بيانية متحركة | — | ~100 MB | `py -m pip install manim` |
| **Blender** | لقطات 3D (blender_cinema.py) | مفيش لقطات 3D محلية | ~1 GB | winget `BlenderFoundation.Blender` |
| **ImageMagick** | أوراق معاينة وتركيب صور سريع | Pillow بيعمل نفس الشغل أبطأ شوية | ~30 MB | winget `ImageMagick.ImageMagick` |
| **ExifTool** | يقرا دوران وتاريخ فيديوهات الآيفون ويشيل الـ GPS | — | ~10 MB | winget `OliverBetz.ExifTool` |
| **aria2** | تحميل أسرع بعدة اتصالات لـ yt-dlp | — | ~5 MB | winget `aria2.aria2` |
| **Deno** | yt-dlp محتاجه عشان يحل تحديات يوتيوب | بعض لينكات يوتيوب تفشل | ~100 MB | winget `DenoLand.Deno` |
| **edge-tts** | تعليق صوتي عربي مجاني (أونلاين) | — | ~1 MB | `py -m pip install edge-tts` |
| **Piper TTS** | تعليق صوتي عربي أوفلاين | — | ~20 MB + صوت ~60 MB | `py -m pip install piper-tts` |
| **rembg** | يشيل الخلفية من صورة/فريم | — | ~170 MB موديل | `py -m pip install rembg` |

## ٤) خدمات بمفاتيح (مش تثبيت)

دي مش برامج بتتحمل؛ دي حسابات مدفوعة أو مفاتيح. المونتاج بيشتغل من غيرها — بتحتاجها بس لو عايز التنين **يولّد** لقطات أو مزيكا أو صوت ناقص.

| الخدمة | بتعمل إيه | المتغير | ملاحظة |
|---|---|---|---|
| **Claude API** | المجلس الإبداعي لو اشتغل برّه Claude Code | `ANTHROPIC_API_KEY` | جوه Claude Code مش محتاجه. |
| **Google Gemini** | تفريغ سحابي بديل (tools/transcribe_audio.py) | `GEMINI_API_KEY` أو `GOOGLE_API_KEY` | مدفوعة |
| **Kling AI** | توليد لقطات B-roll ناقصة بالذكاء الاصطناعي | `KLING_ACCESS_KEY` + `KLING_SECRET_KEY` | مدفوعة |
| **Higgsfield** | توليد/تكبير فيديو وصور وإعادة تأطير | `HF_KEY` أو `HIGGSFIELD_API_KEY` | HF_KEY بالشكل key-id:key-secret، أو وصّل Higgsfield connector. · connector: Higgsfield MCP |
| **Suno** | توليد مزيكا أصلية للمونتاج | — | مفيش متغير بيئة في الريبو؛ بيشتغل من خلال Suno connector بس. · connector: Suno MCP |
| **ElevenLabs** | تعليق صوتي احترافي | `ELEVENLABS_API_KEY` | مدفوعة |
| **Pexels / Pixabay** | لقطات مجانية مرخصة لو ناقص B-roll | `PEXELS_API_KEY` أو `PIXABAY_API_KEY` | المفاتيح مجانية. |

حط المفاتيح في متغيرات البيئة (ويندوز: `setx GEMINI_API_KEY "..."` وافتح ترمينال جديد). عمرك ما تكتبها جوه ملف في الريبو.

## الآيفون (a-Shell)

a-Shell فيه `python3` و `ffmpeg` و `ffprobe` جاهزين، و `pip install yt-dlp` شغّال (سكربت Cinema C في `tools/a-shell/` بيستخدمهم). المكتبات التقيلة (OpenCV، faster-whisper، librosa، Node، Playwright) مش بتشتغل هناك، فالمونتاج الكامل بيتعمل على الكمبيوتر، والآيفون للتحميل والقص السريع. `dm_doctor.py install-plan --os ashell` بيقولك المتاح.

## اتعمل إزاي

القائمة اتجمعت من: `requirements/*.txt`، `KOSIF_SUPERPOWERS_ENVIRONMENT_REPORT.md`، `montage_pro.py doctor`، `black_dragon_media.py doctor`، `cinema_lab.py`، `tools/transcribe_audio.py`، `tools/a-shell/Cinema_C_V34_Studio_iPhone.sh`، `starters/remotion`، `kosif-montage-motion/requirements.txt`. لو أداة جديدة دخلت محطة، تتضاف في `data/required_tools.json` الأول، والـ doctor والسكربتات والصفحة دي بيمشوا وراها.
