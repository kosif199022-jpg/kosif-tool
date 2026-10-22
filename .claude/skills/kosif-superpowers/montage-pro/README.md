# مونتاج برو — Montage Pro (فريق مهمة المونتاج والموشن والـ3D)

ارفع **صوتًا** أو **فيديو** واطلب «مونتاج» أو «موشن جرافيك»، فيعمل فريق من 13 دورًا متخصصًا بخطوات مرتبة، ويعرض عليك **قائمة خيارات قوية** ثم ينفّذ ما تختاره ويتحقق منه. Upload an audio or a video; a 13-role team measures it, offers an option menu, builds the chosen option and verifies it.

## الفهرس / contents
- كيف يعمل / how it works
- الفريق / the team
- قائمة الخيارات / the option menu
- التفريغ ومصنع الريلز / transcription and the reel factory
- مكتب التحميل والحقوق (فكرة IDM) / the download desk
- ما تعلمناه من IDM بـ REA وGhidra / what we learnt from IDM
- قواعد لا تُكسر / rules

## كيف يعمل / how it works

```bash
SKILL_DIR=.claude/skills/kosif-superpowers
python3 $SKILL_DIR/scripts/montage_pro.py doctor                       # ما الجاهز على هذا الجهاز
python3 $SKILL_DIR/scripts/montage_pro.py intake my.mp4 --job job1     # المحلل: مدة، مسارات، جهارة، طاقة الصوت، القطعات، ورقة إطارات
python3 $SKILL_DIR/scripts/montage_pro.py options job1 --brief "ريلز حماسي"   # المخرج: قائمة الخيارات + خطة مرحلية (خريطة ذهنية)
python3 $SKILL_DIR/scripts/montage_pro.py build job1 --option reframe --style 9:16 --title "عنوان" --deliver-mix
```

النتيجة في `job1/out/` وتقرير كل خطوة في `job1/report.json`. كل ملف ناتج يمر على `verify_video.py` (الترميز، المقاس، fps، الصوت، الجهارة، ومطابقة طول الصوت الأصلي). الصوت الأصلي لا يُلمس: تُسجَّل بصمته SHA-256 عند الاستقبال ويُعاد فحصها بعد البناء؛ ونسخة تسليم بجهارة −14 LUFS تُنتج **منفصلة** بـ `--deliver-mix`.

## الفريق / the team

`python3 $SKILL_DIR/scripts/montage_pro.py team` — التعريف الكامل في `data/montage_pro_team.json`:

| الدور | المهمة | البوابة قبل التسليم |
|---|---|---|
| المخرج | العقد ومعيار القبول واختيار الخيار | موجز مكتوب بمعايير قبول |
| محلل المادة | قياس الصوت والفيديو بلا تخمين | intake.json بقيم مقاسة فقط |
| كاتب السيناريو | نصوص الشاشة والترجمة العربية | كل كلمة لها مصدر |
| مكتب المادة والحقوق | تحميل مجزأ قابل للاستئناف، التقاط البث، مكتبات مرخصة | سطر rights.json لكل ملف |
| مهندس التحويل | ميزانين CFR H.264/AAC 48k وبروكسي 540p | توحيد fps والصيغة |
| المونتير | خطة قطع على القطعات والطاقة والكلمات | EDL متصل بلا فجوات |
| مصمم الموشن | كلمات متحركة ورسم وكاميرا بحركة حقيقية | مشهد حتمي seek(t) |
| الرسام | شخصيات أصلية وIK وحركات | مصدر طبقات قابل للتعديل |
| فنان 3D | 3D حقيقي عند الحاجة فقط | إطارات معدودة |
| مهندس الصوت | يحفظ الأصل وينتج مزيج تسليم منفصل | البصمة لم تتغير |
| الملوّن | لوك وتلوين وحبيبات وتعتيم | قبل/بعد |
| مهندس الرندر | معاينة ثم رندر نهائي | موافقة المعاينة |
| مراقب الجودة | verify_video وتقرير صادق | قيم مقاسة |

## قائمة الخيارات / the option menu

| الخيار | لـ | الحالة هنا | ماذا ينتج |
|---|---|---|---|
| `kinetic-film` | صوت/فيديو | ✅ شُغّل | فيلم موشن (kinetic/doodle/cinematic) على الصوت الأصلي + HTML قابل للتعديل |
| `visualizer` | صوت/فيديو | ✅ شُغّل | موجة/طيف/دائرة 9:16 بعنوان وخلفية متدرجة |
| `reframe` | فيديو | ✅ شُغّل | 9:16 أو 1:1 أو 4:5 بخلفية مموهة |
| `highlight-reel` | فيديو | ✅ شُغّل | ريل بطول محدد من أقوى اللقطات (قطعات مقاسة + طاقة الصوت) |
| `look` | فيديو | ✅ شُغّل | teal-orange / warm / mono / film + صور قبل/بعد |
| `reference-remix` | فيديو | ✅ يولّد المشروع | مشروع Remotion بإيقاع مونتاج الفيديو (يحتاج npm install للرندر) |
| `broll-documentary` | صوت/فيديو | 🧩 يحتاج words.json ولقطات مرخصة | مونتاج وثائقي بلقطات حقيقية |
| `character` | صوت | 🧩 يحتاج words.json | شخصية مرسومة تتحرك على الكلمات |
| `3d-scene` | صوت/فيديو | 🧩 يحتاج مشهد JSON | مشهد ثلاثي الأبعاد بحركة كاميرا |

«شُغّل» = جُرّب على وسائط اصطناعية في هذه الحاوية (`evals/test_montage_pro.py`). فشل فحص الجهارة الوحيد في الاختبارات سببه هدوء ملف الاختبار، وتحله نسخة `--deliver-mix` (8/8).

## التفريغ ومصنع الريلز / transcription and the reel factory

اختيار مجلس البرو في 22-10 ([المحضر](../proofs/pro-council-20261022/README.md)): مسار تحليل محلي أولًا، ثم غلاف رفيع للريلز. (المجلس اقترح بوابة حقوق مانعة؛ قرار المالك في 22-10: تسجيل الحقوق إرشاديًا بلا منع.)

```bash
python3 $SKILL_DIR/scripts/montage_pro.py transcribe voice.m4a --job out/job1 --language ar --local-only   # words.json (kosif-words/1)
python3 $SKILL_DIR/scripts/reel_factory.py build --audio voice.m4a --audio-rights owned --words out/job1/words.json \
  --shots-manifest stock/manifest.json --shot-ids 17928486,8165467,20382699 --title "دعاء يوم الخميس" --handle @kosif
python3 $SKILL_DIR/scripts/verify_video.py reel.mp4 --aspect 9:16 --fps 30 --duration 15 --source-audio voice.m4a
```

- **`transcribe`:** faster-whisper محليًا (CPU، int8، توقيت لكل كلمة، VAD يتخطى الصمت والموسيقى) إلى `words.json` بصيغة `kosif-words/1`: بصمة المصدر والمحرك والكلمات والجمل. لا يكتب داخل `jobs/` أو ملف متتبَّع إلا بـ `--allow-tracked`. `intake --transcribe` يفرّغ قبل خريطة الإشارات. دقة التوقيت **لم تُقَس** مقابل مرجع؛ المقاس: 34 كلمة في 14–28 ثانية لمقطع 14.7 ث، وثلاث مرات بنتيجة متطابقة بايتًا ببايت.
- **`verify_video.py --source-audio`:** يطابق بصمة MD5 لحزم الصوت مع المصدر؛ عند التطابق تصبح الجهارة والذروة `[INFO]` «الصوت الأصلي محفوظ» بدل الفشل، لأن صوت المستخدم لا يُعاد ضبطه.
- **`reel_factory.py plan|build`:** يسجّل الحقوق المعلنة للصوت ورخصة كل لقطة في `rights.json` (الفجوات تُدرج وتُذكر مرة في `RIGHTS_NOTE` ولا توقف البناء)، ثم لقطة لكل جملة وانتقالات على القطع، ولوحة 4:5، ومشهد عربي كلمة بكلمة داخل المنطقة الآمنة، ودمج الصوت بلا إعادة ترميز، وفحص بالبصمة. المخرجات في `out/reels/<slug>` (متجاهَل من git).

## مكتب التحميل والحقوق (فكرة IDM) / the download desk

```bash
python3 $SKILL_DIR/scripts/montage_pro.py acquire URL --job job1 --license "CC0 / Pexels License / owner" --source-page PAGE_URL
python3 $SKILL_DIR/scripts/montage_pro.py convert job1
```

- **ملف مباشر** (mp4/mov/wav/…): تحميل مجزأ بستة نطاقات `Range` متوازية مع ملفات `.part` قابلة للاستئناف ثم دمج وبصمة SHA-256 (APPX-48).
- **صفحة بث** (YouTube وVimeo وX وTikTok وHLS `.m3u8` وDASH `.mpd`): التقاط بـ yt-dlp/ffmpeg عبر `fetch_video.py` وتحويل إلى H.264/AAC صالح للمونتاج.
- **مكتبات مرخصة:** `media_sources.py search` لـ100 موقع مع تلميح الرخصة.
- كل ملف يُسجَّل في `rights.json` بالرابط وصفحة المصدر والرخصة والبصمة. **يرفض الأمر العمل بلا رخصة أو `--owner`**، ولا يتجاوز DRM أو تسجيل الدخول.
- `convert` يحوّل كل شيء إلى ميزانين موحد (30fps CFR، H.264 CRF 18، AAC 48 kHz) وبروكسي 540p — دور «محوّل الفيديو» في IDM.

## ما تعلمناه من IDM بـ REA وGhidra / what we learnt from IDM

راجع [IDM_STUDY.md](IDM_STUDY.md): فحص ثابت للقراءة فقط لـ IDM 6.43 المثبّت على جهاز المالك، دون تشغيله ودون نسخ كوده.

## قواعد لا تُكسر / rules
- لا تدّعِ مشاهدة فيديو أو سماع صوت لم يُقَس؛ القيم من ffprobe/ffmpeg فقط.
- الصوت الأصلي يقود الزمن ولا يُعدَّل؛ مزيج التسليم ملف منفصل.
- لا تحميل بلا رخصة للأصل نفسه؛ لا تجاوز لحماية أو حساب؛ اذكر المصدر.
- معاينة قبل الرندر النهائي؛ ولا تسليم قبل verify_video.
