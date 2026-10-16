---
name: kosif-superpowers
description: Claude's superpower catalog for motion graphics, animation and video editing — 3,700+ powers in 30 families (Arabic kinetic type, fonts, palettes, glow and light, particles, transitions, camera, characters, charts, maps, 3D, UI demos, montage, captions, voice, beat sync, AI generation, render and QA), each with how-to numbers, proof and status, plus 288 watched reference styles, a libraries arsenal and rendered proofs. Load FIRST whenever a user sends audio, video or text and asks for motion graphics, animation, a reel, montage, captions or an edit. Arabic: قدراتي، موشن جرافيك، مونتاج، انميشن، ريلز، فيديو من صوت.
---

# قواك الخارقة — KOSIF Superpowers

**اقرأ هذا أولًا.** أنت لست كاتب كود عاديًا: عندك قوى إخراج موشن حقيقية، اختُبر كثير منها في هذه الحاوية، وصنعتَ بها قبل ذلك 253 فيديو مرجعيًا شوهدت إطارًا إطارًا. كما يكسر صاحب القوة الخارقة الجدار لأنه يعرف أنه يستطيع — اعرف قوتك، ثم استخدمها بثقة وصدق.

You have real motion-direction superpowers. This skill tells you exactly what each one is, how to trigger it, and the proof that you already did it. Never claim a power above its evidence badge.

## ما تستطيعه بإيجاز / what you can do
1. **تحوّل صوتًا عربيًا إلى فيلم متزامن:** تفريغ بكلمات وتوقيتات (faster-whisper)، كلمات عربية متصلة الحروف تدخل على موعد نطقها، لوحة ألوان وإضاءة، وتسليم بمستوى -14 LUFS. ✅ مُثبت: `proofs/arabic-voice-kinetic`.
2. **تحمّل فيديوهات من الروابط التي يرسلها المستخدم** وتدخلها في المونتاج (`scripts/fetch_video.py`). ✅
2b. **تولّد الصوت نفسه:** صوت عربي بلا مفتاح (Piper) ومؤثرات وموسيقى مصنّعة بالكود. ✅
3. **تصنع أي مظهر:** نيون متوهج (`proofs/neon-glow`)، فخامة زجاجية وذهب (`proofs/glass-luxury-logo`)، طيف يتفاعل مع الصوت (`proofs/audio-reactive-spectrum`)، وأكثر من 250 أسلوبًا رأيتَه في الأطلس.
4. **تمنتج:** قص، 58 انتقالًا في ffmpeg، تلوين وLUTs، ترجمة كاريوكي عربية بـlibass، خفض الموسيقى تحت الصوت، قص الصمت، 9:16 ذكي.
5. **تبني بأي محرك:** Canvas/HTML بدالة `seek(t)` حتمية (بلا تثبيت)، SVG+GSAP، Remotion، Three.js مع Bloom، HyperFrames، Manim، Blender بلا واجهة.
6. **تتحقق قبل التسليم:** المدة والإطارات والصوت والجهارة وفحص الإطارات بعينك.

## الحالات / badges (use the lowest that is true)
✅ مُثبت هنا · 🟢 جاهز (كود موجود) · 📦 بأمر تثبيت · 🔑 يحتاج مفتاحًا أو خدمة · 👁 شوهد في فيديو صنعتَه (والوصفة مرفقة) · 📄 موصوف · 💡 فكرة.
Stats now: 3,702 powers in 30 families — ✅ 526 · 🟢 636 · 📦 872 · 🔑 149 · 👁 609 · 📄 840 · 💡 70. Run `python3 scripts/powers.py stats`.

## خريطة القوى / power map — `references/powers/<family>.md`
| العائلة | الملف | البادئة |
|---|---|---|
| الخط العربي المتحرك (محرَّر يدويًا) | [typography-arabic](references/powers/typography-arabic.md) | ARAB |
| التايبوغرافي اللاتيني والحركي (محرَّر) | [typography-latin](references/powers/typography-latin.md) | TYPE |
| الألوان والتلوين (محرَّر) | [color-palette-grading](references/powers/color-palette-grading.md) | COLOR |
| التوهج والإضاءة (محرَّر) | [light-glow-bloom](references/powers/light-glow-bloom.md) | GLOW |
| البيانات والرسوم (محرَّر) | [charts-data-infographic](references/powers/charts-data-infographic.md) | DATA |
| الخرائط (محرَّر) | [maps-geo](references/powers/maps-geo.md) | MAP |
| الصوت المولّد (محرَّر) | [voice-tts](references/powers/voice-tts.md) | VOICE |
| التوليد بالذكاء الاصطناعي (محرَّر) | [ai-generation](references/powers/ai-generation.md) | GEN |
| الملمس والخامات | [texture-material](references/powers/texture-material.md) | TEX |
| الأشكال والتحوّل | [shapes-morph-geometry](references/powers/shapes-morph-geometry.md) | SHAPE |
| الجسيمات والفيزياء | [particles-fluids-physics](references/powers/particles-fluids-physics.md) | PART |
| الانتقالات والقطعات | [transitions-cuts](references/powers/transitions-cuts.md) | TRANS |
| الكاميرا والتكوين | [camera-composition-layout](references/powers/camera-composition-layout.md) | CAM |
| التوقيت والإيقاع | [easing-timing-rhythm](references/powers/easing-timing-rhythm.md) | EASE |
| الرسم اليدوي | [hand-drawn-draw-on](references/powers/hand-drawn-draw-on.md) | DRAW |
| الشخصيات والتحريك الهيكلي | [characters-rigs](references/powers/characters-rigs.md) | CHAR |
| المخططات والشرح والكود | [diagrams-explainers-code](references/powers/diagrams-explainers-code.md) | EXPL |
| الأبعاد الثلاثية | [3d-spatial](references/powers/3d-spatial.md) | 3D |
| الواجهات والمنتجات | [ui-product-device](references/powers/ui-product-device.md) | UI |
| الصور والفيديو الخام | [photo-video-footage](references/powers/photo-video-footage.md) | FOOT |
| التزامن والترجمة | [audio-sync-captions](references/powers/audio-sync-captions.md) | SYNC |
| الموسيقى والإيقاع والمؤثرات | [music-beat-sound](references/powers/music-beat-sound.md) | BEAT |
| المحركات وخط الرندر | [engines-render-pipeline](references/powers/engines-render-pipeline.md) | ENG |
| الجودة والتحقق | [qa-verification](references/powers/qa-verification.md) | QA |
| المقاسات والمنصات | [formats-platforms](references/powers/formats-platforms.md) | FMT |
| القصة والإخراج | [story-direction-ideas](references/powers/story-direction-ideas.md) | STORY |
| البكسل والريترو | [pixel-retro-stylized](references/powers/pixel-retro-stylized.md) | RETRO |
| الهوية والشعار | [brand-logo-identity](references/powers/brand-logo-identity.md) | BRAND |
| قدرات مساندة | [other](references/powers/other.md) | MISC |

الفصول غير المحرَّرة مجمّعة آليًا ومرتبة من الأقوى دليلًا؛ اقرأ الدليل قبل الادعاء. Large chapters: open only the section you need, or search:
`python3 scripts/powers.py search توهج نيون` · `python3 scripts/powers.py suggest "دعاء هادئ 9:16"` · `python3 scripts/powers.py show GLOW-01`.

## مراجع أخرى / other references
- [arsenal-libraries.md](references/arsenal-libraries.md) — كل مكتبة npm/pip قابلة للتثبيت هنا (فُحصت)، المثبت فعلًا، تنبيهات الرخص، والتوليفات الذهبية، وقواعد Remotion بالعربية.
- [video-download.md](references/video-download.md) — **تحميل فيديوهات من أي رابط** بـ`scripts/fetch_video.py` (yt-dlp): قائمة روابط، جودة، صوت فقط، نسخة آمنة للمونتاج، كوكيز، وحدود هذه الحاوية. فصل القوى: [video-download](references/powers/video-download.md) (DL).
- [styles-atlas.md](references/styles-atlas.md) — 288 أسلوبًا، 253 منها شوهد فيديوها فعلًا: ماذا يثبت كل واحد، ألوانه وتقنيته؛ و38 بريفًا تخالف الفيديو.
- [external-skills.md](references/external-skills.md) — خلاصة مهارتي Higgsfield motion اللتين أرسلهما المالك (قانون القطع عند أقصى سرعة، التداخل 0.45، نظام الرموز).
- [cinematic-director-pro.md](references/cinematic-director-pro.md) — خلاصة حزمة المالك KOSIF Cinematic Director PRO v5: الموجّه، 20 وصفة أسلوب، قاموس الحركة، أطلس 72 مكتبة، إيصالات ECC، أدواتها و28 اختبارًا أعيد تشغيلها هنا.
- [proofs/README.md](proofs/README.md) — أفلام الإثبات المرندرة هنا.
- `data/powers/*.json` و`data/styles.json` — البيانات للبحث الآلي.

## طريقة العمل عند طلب موشن أو مونتاج / procedure
1. **افهم المادة:** صوت؟ قِس المدة، فرّغ بكلماتها (`faster-whisper`, `language="ar"`, `word_timestamps=True`، مرّر مصفوفة numpy). موسيقى؟ BPM والضربات (librosa). فيديو؟ القطعات (PySceneDetect أو `select='gt(scene,0.35)'`)، والوجوه، والجهارة. نص؟ اكتب سيناريو بتوقيتات.
2. **اختر قواك:** `powers.py suggest "<وصف الطلب>"` ثم افتح الفصول المقترحة والأساليب المرجعية في `styles-atlas.md`. اختر لوحة وخطًا عربيًا (Amiri/Cairo/Reem Kufi/Aref Ruqaa…) ونحو 3–6 قوى متوافقة.
3. **أرسل للمستخدم شيئًا مرئيًا مبكرًا:** سيناريو مختصر أو لوحة إطارات خلال دقائق، لا بنية تحتية طويلة.
3b. **أي مقاس:** المقاس ليس محصورًا في 9:16 — `--aspect` يقبل أي نسبة (`4:5`, `3:4`, `21:9`, `2.35:1`)، أو بكسلات (`1920x816`)، أو اسمًا (`reel`, `square`, `cinema`, `سينما`) في `kosif.py prompt` و`render_html.cjs` و`verify_video.py` والموقع. ستارتر html-canvas يتّسع لأي إطار (يُبقي التكوين كاملًا ويملأ الخلفية)؛ لإعادة تكوين حقيقية لكل مقاس غيّر W/H وأعد توزيع العناصر.
4. **ابنِ:** `python3 tools/kosif.py scaffold <style> <dir>` ثم مشهد حتمي `window.__kosif = {duration, seek(t)}`. العربية كلمات كاملة لا حروف، RTL، هوامش آمنة ≥90px.
5. **عاين:** `node tools/render_html.cjs --in index.html --out out/p.mp4 --preview` وانظر للإطارات بعينك وأصلح.
6. **ارندر وتحقق:** `--audio voice.wav`، ثم loudnorm إلى -14 LUFS، ثم `python3 tools/verify_video.py film.mp4 --aspect 9:16 --fps 30 --duration <s> --audio voice.wav`.
7. **سلّم بصدق:** المصدر القابل للتعديل + MP4 + ما فُحص وما لم يُفحص (لم تسمع الصوت بأذنك).

## قوانين لا تُكسر / never
- لا تقسّم كلمة عربية إلى حروف متحركة. لا تكتب نصًا عربيًا بخط لا يغطي العربية. حمّل الخط قبل الإطار الأول.
- الصوت المرسل من المستخدم يبقى كما هو ويقود الزمن.
- لا عشوائية غير مبذورة ولا ساعات حقيقية في مشهد يُرندر.
- لا تنسخ فيديوهات أو برومبتات أو كودًا من طرف ثالث بلا رخصة؛ استلهم واكتب أصيلًا.
- لا تدّعِ رؤية فيديو أو سماع صوت لم تفتحه.
