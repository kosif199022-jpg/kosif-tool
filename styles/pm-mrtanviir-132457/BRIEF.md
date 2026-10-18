# ريل مهارات موشن: أربعة فصول على إيقاع واحد — Claude motion designer showreel

> ريل مهارات موشن سريع مدته 15 ثانية مقطوع على شبكة 120 نبضة في الدقيقة: نقاط، حرف داخل دائرة، كلمات ضخمة على الأحمر، مربع أزرق مستدير بمقابض تحويل، زهرة نقاط فيلوتاكسية، شبكة نقاط بموجة، سحابة جسيمات ثلاثية الأبعاد، شريط مخطط يرسم منحنى على الأصفر، نص على مسارات دائرية، وختام Claude.
>
> A fast 15-second motion-skills reel cut on a 120 BPM grid: dots, a letter in a circle, giant uppercase words on red, a blue rounded square with transform handles, a phyllotaxis dot flower, a waving dot grid, a 3D particle cloud, a striped ribbon drawing a curve on yellow, text on circular paths and a closing serif signature.

ملف تعريفي أصلي من إعداد KOSIF، رُوجع وصُحّح مقابل إطارات مأخوذة من فيديو المرجع (2026-10-16)؛ التوقيتات والألوان قراءات تقريبية من تلك الإطارات، فراجع المرجع للتفاصيل الدقيقة.
Original KOSIF brief, revised against frames sampled from the reference video (2026-10-16); timings and colours are approximate readings from those frames, so check the reference for fine detail.

- المرجع / Reference: https://www.promptsmotion.com/mrtanviir-132457
- التصنيفات / Categories: charts, kinetic-type
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 15 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: Remotion, React, SVG, Three.js

## الفكرة
الموضوع ريل يقوم مقام السيرة الذاتية لمصمم موشن. كل لقطة مهارة واحدة على حقل لوني مسطح خاص (أسود، أحمر، أبيض دافئ، أزرق كهربائي، أصفر): خط ضخم، تحويل شكل بمقابض محرر، أنماط توليدية، جسيمات ثلاثية الأبعاد، رسم مسار، ونص دائري. يربطها إطار HUD ثابت يعرض الإيقاع والعدّاد الزمني، والقطع يقع على الإيقاع.

## Concept
The subject is a reel that stands in for a motion designer's CV. Each shot shows one skill on its own flat colour field (black, red, warm white, electric blue, yellow): giant type, a shape transform with editor handles, generative patterns, 3D particles, a path draw and circular text. A constant HUD frame shows BPM and timecode, and cuts land on the beat.

## المشاهد المقترحة
- 0-1.3 ث: حقل شبه أسود داخل إطار HUD؛ نقطتان حمراوان تظهران وتنجرفان نحو بعضهما.
- 1.3-2.5 ث: قرص أحمر بحلقة بيضاء يحتضن حرف E كبيراً ينزلق ويملؤه.
- 2.5-3.8 ث: قطع إلى الأحمر: كلمات سوداء ضخمة بأحرف كبيرة يقصّها الإطار تصطدم على سطرين وقوس مؤشر يؤطر الكلمة التالية.
- 3.8-5 ث: أسود: مربع أزرق مستدير داخل مقابض تحويل مع قراءة للدوران يتكبر ويدور كعرض محرر.
- 5-7.5 ث: أبيض دافئ: زهرة نقاط فيلوتاكسية سوداء تدور وتتفتح، ثم شبكة نقاط كاملة تمر بها موجة جيبية تلوّن النقاط بالأحمر.
- 7.5-8.8 ث: أزرق كهربائي: سحابة ثلاثية الأبعاد من جسيمات بيضاء تدور بشكل قطرة.
- 8.8-11.3 ث: أصفر: شريط مخطط بالأحمر والأبيض والأزرق يدخل من اليسار ويرسم منحنى عريضاً عبر الإطار.
- 11.3-15 ث: أسود: حلقات متحدة المركز من كلمات المهارات تدور بعكس بعضها على مسارات دائرية؛ ثم نقطة حمراء على الأبيض الدافئ تكبر إلى توقيع ختامي بخط سيريف ونقطة حمراء وسطر الدور بأحرف كبيرة متباعدة.

## Proposed scenes
- 0-1.3s: Near-black field inside a HUD frame; two red dots appear and drift toward each other.
- 1.3-2.5s: A red disc with a white ring holds a large E that slides in and fills it.
- 2.5-3.8s: Cut to red: giant black uppercase words cropped by the frame slam in on two lines, a bracket cursor framing the next word.
- 3.8-5s: Black: a blue rounded square inside transform handles with a rotation readout scales and rotates like an editor demo.
- 5-7.5s: Warm white: a black phyllotaxis dot flower spins and blooms, then a full dot grid where a sine wave sweeps red through the dots.
- 7.5-8.8s: Electric blue: a 3D cloud of white particles rotates as a teardrop form.
- 8.8-11.3s: Yellow: a red, white and blue striped ribbon enters from the left and draws a sweeping curve across the frame.
- 11.3-15s: Black: concentric rings of skill words counter-rotate on circular paths; then a red dot on warm white grows into the closing serif wordmark with a red full stop and a spaced caps role line.

## قواعد الحركة
- القطع على شبكة 120 نبضة في الدقيقة: تغيير لقطة كل مازورة أو نصف مازورة (نحو 1.25-1.9 ثانية) مع تبديل لون الخلفية في كل قطعة.
- HUD ثابت: أقواس زوايا، عدّاد مازورات، وسم BPM وعدّاد زمني بخط أحادي صغير على حواف الإطار.
- كل لقطة تعرض تقنية واحدة: اصطدام الخط، مقابض التحويل، دوران فيلوتاكسي، موجة جيبية على شبكة النقاط، سحابة نقاط ثلاثية الأبعاد، رسم مسار الشريط، ونص على دائرة.
- الأنماط التوليدية محسوبة لا مرسومة: تباعد بالزاوية الذهبية للزهرة، وموجة جيبية بإزاحة طور عبر الشبكة.
- الكلمات الضخمة يقصها الإطار وتصطدم خلال 150-250 مللي ثانية؛ التوقيع السيريف يستقر بهدوء في النهاية.
- اللوحة: شبه أسود #111113، أزرق كهربائي #343df3، أحمر #ef4136، أصفر #f2c744 وأبيض دافئ #f1ede8.
- الخط: هندسي 900 بأحرف كبيرة للاصطدامات، سيريف عرض للتوقيع، وأحادي صغير للـ HUD.

## Motion rules
- Cut on a 120 BPM grid: a shot change every bar or half bar (about 1.25-1.9 s), each cut swapping the background colour.
- Constant HUD: corner brackets, bar counter, BPM label and timecode in tiny mono at the frame edges.
- Each shot demonstrates one technique only: type slam, transform handles, phyllotaxis rotation, dot-grid sine sweep, 3D point cloud, ribbon path draw, text on a circle.
- Generative patterns are computed, not drawn: golden-angle spacing for the flower, a phase-shifted sine across the grid.
- Giant words are cropped by the frame and slam in within 150-250 ms; the serif signature resolves calmly at the end.
- Palette: near-black #111113, electric blue #343df3, red #ef4136, yellow #f2c744 and warm white #f1ede8.
- Type: geometric sans 900 uppercase for slams, a serif display for the signature, tiny mono for HUD.

## Facts stated by the source (rewritten in our words)
- Length is fixed at 15 seconds.
- Purpose: a self-promotional reel used as a designer's résumé piece.
- Tagged on the site as charts and kinetic type; no stack, colours or scene order are given.

## Assumptions
Observed from frames sampled every ~1.26 s: the shot list, colour fields, HUD with a 120 BPM label and the closing signature. Assumed: exact cut positions between samples and the music; the 1280x720 reference is read as 16:9.

## Keywords
showreel, self promo, beat cuts, 120 bpm, phyllotaxis, dot grid wave, particle cloud, ribbon draw, circular text, hud overlay, ريل مصمم, قطع على الإيقاع, أنماط توليدية, نص دائري
