# كرة تهرب من اثنتي عشرة حلقة — Ball escaping twelve rings

> مقطع عمودي مدته نحو 32 ثانية على أرضية كحلية شبه سوداء: كرة بيضاء متوهجة ترتد داخل اثنتي عشرة حلقة متحدة المركز بفجوات دوارة، ألوانها من الوردي في الوسط إلى البنفسجي والأزرق ثم الفيروزي في الخارج. كلما عبرت الكرة فجوة تذوب الحلقة إلى نقاط متوهجة وينقص عدّاد الحلقات المتبقية، حتى تهرب الكرة وتظهر ESCAPED. ثم بطاقة ختام.
>
> A roughly 32-second vertical clip on a near-black navy ground: a glowing white ball ricochets inside twelve concentric rings with rotating gaps, coloured from pink at the centre through purple and blue to teal outside. Each time the ball slips through a gap, that ring dissolves into glowing dots and the rings-left counter drops, until the ball escapes, 'ESCAPED.' appears and an end card follows.

ملف تعريفي أصلي من إعداد KOSIF، رُوجع وصُحّح مقابل إطارات مأخوذة من فيديو المرجع (2026-10-16)؛ التوقيتات والألوان قراءات تقريبية من تلك الإطارات، فراجع المرجع للتفاصيل الدقيقة.
Original KOSIF brief, revised against frames sampled from the reference video (2026-10-16); timings and colours are approximate readings from those frames, so check the reference for fine detail.

- المرجع / Reference: https://www.promptsmotion.com/kantamk-61f410
- التصنيفات / Categories: —
- النسبة المقترحة / Aspect: 9:16 · المدة / Duration: 32 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: HTML Canvas, Web Audio

## الفكرة
الموضوع محاكاة فيزيائية مرضية مصممة للانتشار: سؤال افتتاحي ثابت يدعو المشاهد إلى التخمين، وكرة تحاول الهرب من اثنتي عشرة حلقة. كل ارتداد يعزف النغمة التالية من لحن مولّد برمجياً، وكل هروب يذيب حلقة ويغير لون العدّاد. لقطة واحدة متصلة بلا قطع حتى الهروب الأخير، ثم قطع حاد إلى بطاقة نصية تقول إن كل شيء مصنوع بالكود.

## Concept
The subject is a satisfying physics simulation designed to spread: a fixed hook question invites the viewer to guess, and a ball tries to escape twelve rings. Each bounce plays the next note of a procedurally generated melody, and each escape dissolves a ring and recolours the counter. It is one continuous take with no cuts until the last escape, then a hard cut to a text card saying everything is made with code.

## المشاهد المقترحة
- 0-3 ث: إطار عمودي: سؤال افتتاحي من سطرين أعلاه، عدّاد الحلقات المتبقية تحته، اثنتا عشرة حلقة متحدة المركز من الوردي في الداخل إلى الفيروزي في الخارج لكل منها فجوة؛ ووسم تشغيل الصوت قرب الأسفل.
- 3-10 ث: الكرة المتوهجة ترتد بسرعة ثابتة داخل الحلقة الأعمق؛ كل اصطدام يولد دائرة محيطية رفيعة تتسع وتتلاشى في نحو 200 مللي ثانية وخط أثر مستدق يتلاشى في نحو 300 مللي ثانية.
- 10-20 ث: الهروب يتكرر كل نحو 2.2 ثانية: حين تعبر الكرة فجوة تذوب الحلقة إلى 40-80 نقطة متوهجة تتبعثر للخارج وتتلاشى في نحو ثانيتين؛ العدّاد ينقص ويتغير لونه ليطابق الحلقة التالية.
- 20-26 ث: لم يبق إلا الحلقات الزرقاء والفيروزية الخارجية؛ الحلقة النشطة تبدو أسطع وأسمك بينما تقترب الكرة من الفجوة الأخيرة.
- 26-26.7 ث: الكرة تهرب من الحلقة الأخيرة وتغادر الإطار بخط أبيض خاطف؛ وتظهر ESCAPED. كبيرة في الوسط.
- 26.7-31.8 ث: قطع حاد إلى بطاقة ختام سوداء بثلاثة أسطر قصيرة مكدسة تقول إن الصورة والنغمات كلها كود.

## Proposed scenes
- 0-3s: Vertical frame: a two-line hook question at the top, a 'N rings left' counter beneath, twelve concentric rings from pink inside to teal outside, each with a gap; a 'sound on' pill shows near the bottom.
- 3-10s: The glowing ball bounces at constant speed inside the innermost ring; each impact spawns a thin outline circle that expands and fades in about 200 ms and a tapered trail line fading over about 300 ms.
- 10-20s: Escapes come roughly every 2.2 s: when the ball passes a gap, that ring dissolves into 40-80 glowing dots that scatter outward and fade over about 2 s; the counter drops and shifts hue to match the next ring.
- 20-26s: Only the outer blue and teal rings remain; the active ring reads brighter and thicker as the ball works toward the last gap.
- 26-26.7s: The ball escapes the last ring and leaves the frame with a brief white streak; 'ESCAPED.' appears large in the centre.
- 26.7-31.8s: Hard cut to a black end card with three short stacked lines saying the visuals and the notes are pure code.

## قواعد الحركة
- فيزياء حتمية: سرعة كرة ثابتة، انعكاس حول العمودي على الدائرة، وفجوة كل حلقة تدور بسرعتها واتجاهها؛ ثبّت بذرة المحاكاة ليتكرر التصيير نفسه.
- بلا قطعات وبلا حركة كاميرا أثناء المحاكاة؛ قطعة حادة واحدة إلى بطاقة الختام عند نحو 26.7 ث.
- إزالة الحلقة ذوبان إلى نقاط متوهجة تنجرف للخارج وتتلاشى في نحو ثانيتين، لا اختفاء مفاجئ.
- استجابة عند كل تلامس: دائرة محيطية تتسع عند نقطة الاصطدام وخط أثر مستدق يتلاشى.
- الصوت: كل ارتداد يطلق النغمة التالية من لحن مولّد؛ والعدّاد يغير لونه مع الحلقة الحالية.
- اللوحة: كحلي مسود #0d0e1a مع رفع #141428، تدرج الحلقات وردي #ff5fc8 وبنفسجي #8a4dff وأزرق #4f6bff وفيروزي #3a8f9a، إضاءة سماوية #5ce1f5، أبيض #ffffff ونص رمادي #9aa0b4.
- عمودي 9:16 بهوامش آمنة لواجهات Shorts وReels؛ الخط هندسي عريض للسؤال والعدّاد وعادي للسطر السفلي.

## Motion rules
- Deterministic physics: constant ball speed, reflection about the circle normal, each ring's gap rotating at its own speed and direction; seed the simulation so the render is repeatable.
- No cuts and no camera moves during the simulation; a single hard cut to the end card at about 26.7 s.
- Ring removal is a dissolve into glowing dots that drift outward and fade over about 2 s, never a hard disappearance.
- Feedback on every contact: expanding outline circle at the impact point and a tapered fading trail line.
- Sound: each bounce triggers the next note of a generated melody; the counter changes hue with the current ring.
- Palette: navy-black #0d0e1a with #141428 lift, ring gradient pink #ff5fc8, violet #8a4dff, blue #4f6bff, teal #3a8f9a, cyan highlight #5ce1f5, white #ffffff and grey text #9aa0b4.
- Vertical 9:16 with safe margins for Shorts/Reels UI; type is a geometric sans bold for hook and counter, regular for the footer.

## Facts stated by the source (rewritten in our words)
- The only stated goal is a video with the potential to spread widely.
- The ball-and-twelve-rings subject comes from the public title, not from the prompt body.
- No duration, stack or structure is stated.

## Assumptions
Observed from the watched video: twelve gapped rotating rings with a pink-to-teal gradient, dot dissolves, the rings-left counter under a fixed hook, impact circles and trails, ESCAPED. and a hard cut to a code end card at about 26.7 s, total about 31.8 s. Assumed: the melody and per-bounce note mapping (audio not heard) and exact gap speeds.

## Keywords
physics simulation, bouncing ball, concentric rings, satisfying loop, viral short, rings left counter, procedural melody, dot dissolve, كرة مرتدة, محاكاة فيزيائية, حلقات, فيديو عمودي, نغمات مولدة
