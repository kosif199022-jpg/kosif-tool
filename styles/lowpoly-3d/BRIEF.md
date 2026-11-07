# عالم ثلاثي الأبعاد بمجسمات Low Poly — مجسمات Low Poly

> عالم صغير ثلاثي الأبعاد بمجسمات مضلعة مسطحة التظليل وألوان باستيل: جزيرة أو مشهد على قاعدة تدور الكاميرا حوله، عناصر تنبثق من الأرض بنابض، ضوء شمس ناعم وظلال بسيطة، وتسميات عربية مسطحة فوق المشهد.
>
> A tiny 3D world built from flat-shaded faceted low-poly models in pastel colours: an island or diorama on a base that the camera slowly orbits, objects pop up from the ground with springy scale, soft sun light and simple shadows, and flat Arabic labels floating over the scene.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://github.com/kosif199022-jpg/kosif-one
- التصنيفات / Categories: 3d
- النسبة المقترحة / Aspect: 9:16 · المدة / Duration: 32 s · الصعوبة / Difficulty: 4/5
- التقنية المقترحة / Stack: Remotion, React, Three.js, WebGL

## الفكرة
الفكرة تُشرح كأنها مجسم ألعاب على طاولة: كل مفهوم مجسم بسيط بأوجه واضحة، والكاميرا تدور حول العالم الصغير وتقترب من كل جزء. البساطة الهندسية تجعل الثلاثي الأبعاد خفيفًا ولطيفًا وسريع التصيير، وتمنح إحساس اللعبة.

## Concept
The idea is explained like a toy diorama on a table: every concept is a simple model with clear facets, and the camera circles the little world and moves in on each part. Geometric simplicity makes the 3D light, friendly and fast to render, with a game-like feel.

## المشاهد المقترحة
- 0-3 ث: سماء باستيل فارغة؛ قاعدة جزيرة مضلعة ترتفع إلى الكادر بارتداد، والكاميرا تدور ببطء منذ البداية.
- 3-9 ث: أول مجموعة تنبثق (أشجار، بيت، صخور) مجسمًا بعد آخر بتكبير نابضي من الصفر ونفخة غبار صغيرة؛ وتسمية مسطحة تثبت فوقها.
- 9-15 ث: الكاميرا تلتف 60° إلى منطقة ثانية؛ ومسار أو نهر يُرسم عبر الجزيرة ليصل الأجزاء.
- 15-22 ث: شخصية أو مركبة صغيرة (مضلعة أيضًا) تتحرك على المسار؛ وتحوّل الضوء من النهار إلى الغروب يعلن مرور الوقت.
- 22-28 ث: المجسم الأهم يكبر عن الباقي؛ والكاميرا تقترب بزاوية منخفضة؛ والرسالة الأساسية تظهر نصًا مسطحًا.
- 28-32 ث: الكاميرا تصعد إلى منظر ثلاثة أرباع علوي للجزيرة كلها؛ ويستقر العنوان والحساب.

## Proposed scenes
- 0-3s: Empty pastel sky; a faceted island base rises into frame with a bounce, the camera already orbiting slowly.
- 3-9s: First cluster pops up (trees, house, rocks) one object at a time with springy scale from 0 and a small dust puff; a flat label pins above.
- 9-15s: The camera arcs 60° to a second area; a path or river draws across the island connecting the parts.
- 15-22s: A small character or vehicle (also low-poly) moves along the path; a day-to-sunset light shift marks time passing.
- 22-28s: The key object grows larger than the rest; the camera pushes in to a low angle; the main message appears as flat text.
- 28-32s: The camera pulls up to a top three-quarter view of the whole island; title and handle settle.

## قواعد الحركة
- الهندسة: 50-800 مثلث لكل مجسم، تظليل مسطح (بلا نعومة في الأوجه)، وبلا خامات؛ اللون لكل وجه عبر لون الرؤوس أو المادة.
- الكاميرا: دوران مستمر 4-8° في الثانية حول المجسم، والتفاف بين المناطق 900-1400 مللي ثانية بتسارع وتباطؤ، ومجال رؤية 30-40° لإحساس الألعاب.
- الانبثاق: تكبير 0 ← 1.1 ← 1 في 450 مللي ثانية (نابض) بتتابع 90-140 مللي ثانية، مع نفخة غبار من 6-10 جسيمات.
- الإضاءة: شمس اتجاهية دافئة مع إضاءة نصف كروية مساعدة؛ ظلال ناعمة؛ ولون الضوء يتحول خلال 2-3 ثوانٍ لتغيّر وقت اليوم.
- اللوحة: سماء #bfe3f0، عشب #8fd18b، رمل #f3d9a4، ماء #5fb7d9، صخر #a7a3b5، سقف مرجاني #ff8a72، خشب #b9825a، والتسميات بحبر #24303b على شارات بيضاء #ffffff.
- التسميات HTML أو مستويات مسطحة مواجهة للكاميرا؛ والعربية ككلمات كاملة بـTajawal أو Cairo 700 بحجم 44-64 بكسل.
- الفرق عن 3D السينمائي والأيزومتريك: السينمائي إضاءة واقعية وعدسات سينما؛ والأيزومتريك منظر عمودي ثابت بإحساس ثنائي الأبعاد؛ أما Low Poly فثلاثي حقيقي بكاميرا منظورية تدور ومجسمات ألعاب مضلعة.

## Motion rules
- Geometry: 50-800 triangles per object, flat shading (no smooth normals), no textures; colour per face via vertex or material colour.
- Camera: continuous orbit 4-8°/s around the diorama, arcs between areas 900-1400 ms ease-in-out, perspective FOV 30-40° for a toy look.
- Pop-ins: scale 0→1.1→1 in 450 ms (spring), staggered 90-140 ms, with a 6-10 particle dust puff.
- Lighting: one warm directional sun plus hemisphere fill; soft shadow map; light colour lerps for time-of-day changes over 2-3 s.
- Palette: sky #bfe3f0, grass #8fd18b, sand #f3d9a4, water #5fb7d9, rock #a7a3b5, roof coral #ff8a72, wood #b9825a, labels ink #24303b on white #ffffff chips.
- Labels are HTML or flat planes facing the camera; Arabic as whole words in Tajawal or Cairo 700, 44-64 px.
- Difference from cinematic-3d and isometric: cinematic-3d is realistic lighting and film lenses; isometric is a fixed orthographic 2D look; lowpoly-3d is true 3D with an orbiting perspective camera and faceted toy models.

## Facts stated by the source (rewritten in our words)
- The public description states nothing specific beyond the title.

## Assumptions
This is an authored KOSIF definition, not an observed reference: there is no reference video for this base style, so palette, type, timings and beats are a design decision written for KOSIF, to be refined per project.

## Keywords
low poly, lowpoly 3d, diorama, flat shading, pastel 3d, orbit camera, toy world, لو بولي, ثلاثي الأبعاد, مجسمات, عالم صغير, ألوان باستيل, كاميرا دوارة
