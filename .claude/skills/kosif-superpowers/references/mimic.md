# KOSIF Mimic — إعادة بناء فيديو مرجعي بلقطات جديدة / rebuild a reference video with new footage

<!-- English version follows the Arabic. -->

<div dir="rtl">

## بالعربية

**المهمة:** يعطيك المستخدم فيديو مرجعيًا عموديًا (لقطات + نص عربي + صوت) ويريد النسخة نفسها بلقطات جديدة. الكود في `scripts/mimic/` (بايثون 3.10+، numpy وPillow مع raqm وffmpeg؛ OpenCV وSciPy اختياريان ويسرّعان التتبع والانتقالات المخصصة). شغّل `python3 $SKILL_DIR/scripts/probe_env.py` أو `superpowers.py doctor` قبل أن تعد بشيء.

### الخطوات

1. **التحليل** — `python3 -c "import sys; sys.path.insert(0,'$SKILL_DIR/scripts/mimic'); import mm_analyze; mm_analyze.analyze('ref.mp4','work')"` يكتب `work/spec.json` و`work/analysis.md` ولوحات مراجعة في `work/sheets/` (اللقطات، الانتقالات مع منحنى التقدّم المقاس، أحداث النص، ومرشحو الخط لكل حدث). الصوت الأصلي يُنسخ إلى `work/audio/` بلا إعادة ترميز.
2. **المراجعة** — افتح `analysis.md` واللوحات مع المستخدم؛ صحّح نص كل حدث في `spec.json` (لا OCR مثبت هنا)، وثبّت الخط إن كان يملك الملف الأصلي بوضعه في `work/fonts/`.
3. **اللقطات البديلة** — لكل لقطة `shots[].replacement.path`. المصدر: ملفات المستخدم أو `scripts/media_sources.py` بترخيص موثّق في manifest. ممنوع تحميل Pinterest أو أي منصة بدون إذن؛ لا يوجد مسار تحميل في هذه النسخة عمدًا.
4. **البناء** — `mm_build.build('work', preview=True)` للمعاينة بنصف الحجم، ثم بلا `preview` للنهائي: H.264 bt709 CRF 17، نفس الأبعاد وعدد الإطارات، الصوت الأصلي منسوخًا. `placeholder=True` يعطي مسودة بخلفيات بلون اللقطة.
5. **التحقق** — `python3 tools/verify_video.py` من جذر المستودع، وقارن لوحة `work/sheets/texts.png` بالنتيجة.

### ما يُقاس وكيف

- **اللقطات:** فرق إطارات بوسيط الكتل مع إخفاء النص؛ القطع الحاد قمة معزولة، والانتقال التدريجي قمة فرق بتأخير 8 إطارات.
- **الانتقالات:** تصنيف بإعادة التركيب — 54 نوعًا من `xfade` في FFmpeg (منقولة إلى NumPy في `mm_transitions.py`، ترخيص LGPL-2.1+) و11 نوعًا من محررات الهاتف (zoomblur، blurcross، flash، dipblack/white، whip، spin…)، كل نوع يُرسم من الإطارين النقيين ويُختار مسار تقدّم رتيب. الناتج: النوع والمعاملات والمدى الدقيق ومنحنى التقدّم.
- **النص:** لون النص من ضربات رفيعة ثابتة عبر الإطارات، أقنعة لكل إطار، أحداث من الهضاب المستقرة، ألفا حقيقية حول الوضع المتتبَّع، نوع الحركة (كلمات، انزلاق، pop، blur، fade، cut) ومنحنيات ألفا/إزاحة/مقياس/حدّة، والأسلوب بالدقة الكاملة (الملء، الحدود، الظل بالمربعات الصغرى، التوهج، الصندوق).
- **الخطوط:** مكتبة = `proofs/_shared/fonts` + `fonts/kosif-jumuah` + خطوط المستخدم + خطوط النظام ذات التغطية العربية؛ `mm_fonts_lib.fetch` يجلب عائلات Google Fonts العربية (OFL) إن سُمح بالشبكة. المطابقة بأقنعة السطر نفسه في كل وجه.
- **المظهر:** إحصاءات Lab لكل لقطة ونقل لوني Reinhard كـLUT ثلاثي، تعتيم محلول من نسبة الزوايا للمركز، حبيبات معايرة لتنجو من H.264، أشرطة سوداء، تلاشي البداية والنهاية.

### الدليل والحدود

- الدليل: [proofs/mimic-synthetic](../proofs/mimic-synthetic/README.md) — مرجع اصطناعي بحقيقة أرضية: انتقالات 6/6، حركات نص 5/5، خطوط 5/5، توقيت ±2 إطار 3/5.
- الاختبار: `python3 -m unittest tests.test_mimic` من جذر المستودع (يُتخطى تلقائيًا ما لم تتوفر numpy وPillow وOpenCV وfontTools وffmpeg وffprobe؛ فمولّد المرجع الاصطناعي في `scripts/mimic/synthetic/` يحتاج OpenCV وإن كان اختياريًا في خط الأنابيب نفسه).
- حدود: لا OCR، لا ملصقات ولا رموز تعبيرية، الخطوط التجارية (ثلث/ديواني) تُستبدل بأقرب خط حر إلا إذا وفّر المستخدم الملف، والدقة على الفيديو الحقيقي أقل من الاصطناعي. قل ذلك للمستخدم قبل البدء.

</div>

## English

**Task:** the user hands over a vertical reference video (clips + Arabic text + audio) and wants the same film with new footage. Code lives in `scripts/mimic/` (Python 3.10+, numpy, Pillow with raqm, ffmpeg; OpenCV and SciPy optional but recommended for tracking and the custom transitions). Run `probe_env.py` or `superpowers.py doctor` before promising anything.

**Steps:** (1) analyse with `mm_analyze.analyze(ref, work)` → `spec.json`, `analysis.md`, review sheets, original audio copied; (2) review with the user, type each event's text into `spec.json` (no OCR installed), drop the real font in `work/fonts/` if they own it; (3) set `shots[].replacement.path` from the user's files or licensed sources found with `scripts/media_sources.py`, never by scraping Pinterest or any platform (this port deliberately ships no downloader); (4) `mm_build.build(work, preview=True)` then the full build: H.264 bt709 CRF 17, same size and frame count, original audio stream copied; `placeholder=True` gives a draft; (5) verify with `tools/verify_video.py` and compare the text sheet against the result.

**What is measured:** shot boundaries from a text-masked block-median frame difference; transitions classified by re-synthesis across 54 FFmpeg xfade kinds (NumPy port in `mm_transitions.py`, LGPL-2.1-or-later) plus 11 phone-editor kinds, with the exact span and the measured progress curve; the text layer with true alpha at the tracked pose, animation kind and curves, least-squares shadow, word onsets; fonts matched by mask comparison across the shipped OFL faces, user fonts, system fonts and optionally Google Fonts Arabic; the look as per-shot Lab stats, a Reinhard 3D LUT, solved vignette, calibrated grain, letterbox and fades.

**Proof and limits:** [proofs/mimic-synthetic](../proofs/mimic-synthetic/README.md) (6/6 transitions, 5/5 text animations, 5/5 fonts, timing ±2 frames 3/5 on a synthetic ground-truth reference); `tests/test_mimic.py` runs the harness and skips unless numpy, Pillow, OpenCV, fontTools, ffmpeg and ffprobe are all present (the synthetic reference generator in `scripts/mimic/synthetic/` needs OpenCV even though the pipeline itself does not). No OCR, no stickers or emoji, commercial Thuluth/Diwani faces are replaced by the closest free font unless supplied, and real footage scores lower than the synthetic case. Say so before starting.
