# تقرير مونتاج التنين الأسود

**المهمة:** اعمل ريل 40 ثانية من المناظرة دي بهوك قوي

**الفيديو النهائي:** `render/final.mp4` · المدة 41.4 ثانية · 1080×1920

**الفكرة المختارة:** مشكلة ← تقليب الوجع ← الحل × على البيت — المناظرة بهوك: المشكلة في جملة ملموسة برقم لو موجود ← تمن المشكلة لو فضلت ← الحل بيتشاف مش بيتحكي… في 40 ث، على البيت
**الهوك:** شاء الله أن يكون لقاء جميلة وأن نوصل فكرتنا بطريقة سالسة واد أنا قول لكي قبل
**ليه الفكرة دي:** B «مشكلة ← تقليب الوجع ← الحل × على البيت» كسب بـ 49 نقطة قصاد A (48). الهوك: «شاء الله أن يكون لقاء جميلة وأن نوصل فكرتنا بطريقة سالسة وا…» (0.32). الاختيار بيتقلب لو: hook +1 ← A، clarity -1 ← A، novelty -1 ← A؛ القرار هش، فالمجلس لازم يتشغّل قبل الرندر.

**اللوك:** map-journey · لون cinematic · كابشن karaoke
**ليه:** اخترت «رحلة على الخريطة» (map-journey) من كتالوج الستايلات (311)، لأن إحساسه ملحمي زي ما البريف عايز بالظبط، وطاقته 0.56 قريبة من المطلوب 0.82، وبيمشي مع نوع المحتوى (talking-head)، وفيه كلمات من فكرة المفهوم B: على. اللون: «سينمائي» (cinematic) — feeling:epic. الانتقالات: cut / match-cut / xfade-wipeleft / xfade-coverup. الكاميرا: ken-burns-left / punch-in / slow-push. الترجمة: karaoke. البدايل اللي كانت قريبة: whiteboard-cinematic (9.1)، pm-le0xet-da422b (8.5)، anime-action (8.2).

## الأرقام بأمانة
- أطر تفكير اتقرت واتطبقت على الفكرة: 21
- أدوات اشتغلت على فيديوك إنت: 18 (faster-whisper, ffmpeg.blackdetect, ffmpeg.ebur128, ffmpeg.ebur128-truepeak, ffmpeg.extract_audio, ffmpeg.frame, ffmpeg.loudnorm-apply, ffmpeg.loudnorm-measure, ffmpeg.render, ffmpeg.sample_frames, ffmpeg.silencedetect, ffmpeg.silencedetect+ebur128, ffprobe, opencv.contact_sheet, pyscenedetect, rms_energy, verify_video, video_eyes.motion)
- أدوات ناقصة: مفيش
- قطعات في المونتاج: 8
- فحص الجودة التقني: ما عدّاش
- لفات النقد والتصليح: 1 · الحكم: ship · الدرجة: 1.0

## كل قطعة وسببها
- `e001` c01 9.16→14.56: problem: strongest short line (5.4s, 1.7 w/s, question), quality 0.83, face — «هل أصبحت الواجبات المنزلية، إمتداد لما تعلمه في» | مشكلة: أقوى جملة قصيرة (5.4ث) فيها سؤال، جودة 0.83
- `e002` c01 1.58→7.42: problem: early, clear statement that sets the scene, quality 0.83, face — «واجب في الرياضيات، قراءة قصيدة، التجيز اليوم الثاني،» | مشكلة: جملة واضحة من الأول بتعرّف الحكاية، جودة 0.83 (trimmed at a word gap | اتقصّت عند فاصل بين كلمتين); ken-burns-left hides the jump cut | ken-burns-left عشان يخفي القفزة
- `e003` c01 79.76→87.60: build: mid-story line that moves the story on, quality 0.83, face — «فمن نظن نيلي إلى زهري القدسي أهلا بكي» | تصاعد: جملة من النص بتحرّك الحكاية، جودة 0.83
- `e004` c02 14.66→17.09: build: mid-story movement (motion 0.54), quality 0.37, face — shot c02-s005 | تصاعد: حركة في نص الحكاية (0.54)، جودة 0.37
- `e005` c02 19.40→20.04: build: mid-story movement (motion 1.00), quality 0.43, face — shot c02-s007 | تصاعد: حركة في نص الحكاية (1.00)، جودة 0.43
- `e006` c01 44.22→49.06: payoff: late, high-quality moment (q 0.83), quality 0.83, face — «في نور الفجري وموج البحري وشمس الصحراء تراني» | حصاد: لحظة قوية متأخرة بجودة 0.83، جودة 0.83
- `e007` c01 137.90→145.72: payoff: late, high-quality moment (q 0.83), quality 0.83, face — «اليوم في محورين المحور الأول سنبني الفكرة في» | حصاد: لحظة قوية متأخرة بجودة 0.83، جودة 0.83; ken-burns-left hides the jump cut | ken-burns-left عشان يخفي القفزة
- `e008` c01 49.14→55.74: cta: closing line, quality 0.83, face — «معكم ويار محمد أجب عثمان بطلات تحدي القراءة» | دعوة: جملة ختام، جودة 0.83 (trimmed at a word gap | اتقصّت عند فاصل بين كلمتين)

## اقتراحات توليد (محتاجة موافقتك قبل أي صرف)
- g01: music لـ music (40.0 ث)

## المراحل
- العين الأولى: ✓ (70.64 ث)
- يفهم المطلوب: ✓ (0.07 ث)
- يفكر بإبداع: ✓ (0.07 ث)
- يختار الذوق: ✓ (0.07 ث)
- يكتب المونتاج: ✓ (0.08 ث)
- اقتراحات التوليد: ✓ (0.06 ث)
- ينفّذ: ✓ (51.36 ث)
- يتفرج وينقد: ✓ (12.27 ث)
