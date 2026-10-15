# فيلم إطلاق منتج بأسلوب الورق والقلم — Paper-style product launch film

> فيلم إطلاق مدته 15 ثانية على خلفية ورقية مع ملاحظات تُرسم بالقلم، وكرة فيزيائية، وخط ضخم متحرك، وتبديل حاد بين الفاتح والداكن.
>
> A 15s product launch on a paper canvas: marker notes draw themselves, a physics ball bounces, giant kinetic type and hard light/dark flips, one idea per 2s.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/ik-builds-b8bdcf
- التصنيفات / Categories: product-ui, charts, diagrams, kinetic-type, shapes, particles, characters, music, code
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 15 s · الصعوبة / Difficulty: 4/5
- التقنية المقترحة / Stack: GSAP, HTML Canvas, SVG

## الفكرة
الموضوع منتج برمجي يُشرح في خمس عشرة ثانية دون تعليق صوتي ودون لقطات مصورة، فالكلمات والرسوم وحدها تحمل الرسالة. الهدف أن يفهم المشتري ما يتعلمه المنتج فعلاً من بياناته لا الفكرة المجردة، لذلك تُكتب كل جملة بلغة العميل لا بلغة المحرّكين. ما يميز لغة الحركة هو التناقض المقصود: ورق فاتح هادئ تُخربش عليه ملاحظات بقلم تحبير، ثم تقطعه كرة ذات فيزياء حقيقية وكلمات ضخمة بخط Anton ولحظات انقلاب كامل إلى الوضع الداكن، بينما يصاحب كل ضربة بصرية صوت مطابق.

## Concept
The subject is a software product explained in fifteen seconds with no narration and no filmed footage; words and drawings carry the whole message. The goal is for a buyer to grasp what the product actually learns from their data rather than an abstraction, so every line is written in customer language, never animator vocabulary. The motion language lives on deliberate contrast: a calm paper canvas scribbled with ink-marker notes, interrupted by a ball with real physics, oversized Anton type and full flips into a dark mode, while every visual hit lands with a matching sound.

## المشاهد المقترحة
- 0-2 ث: تظهر الخلفية الورقية؛ ملاحظة بخط Caveat تكتب نفسها عبر stroke-dashoffset خلال 420 مللي ثانية وتطرح مشكلة المشتري؛ صوت خدش قلم خفيف.
- 2-5 ث: قطع حاد إلى الوضع الداكن الفحمي مع سقوط الطبول؛ كرة بجاذبية حقيقية تهبط من الأعلى وتنضغط عند الارتطام (120 مللي ثانية) وترتد مرتين بينما يصطدم عنوان من ثلاث كلمات بخط Anton كلمة كلمة.
- 5-8 ث: عودة إلى الورق على الإيقاع؛ أسهم بقلم تحبير ومخطط مرسوم باليد يشرحان الحلقة الأساسية للمنتج؛ تسميات صغيرة بلون التمييز تنبثق بتتابع 60 مللي ثانية.
- 8-11 ث: تبديل داكن ثانٍ؛ تُقذف الكرة مجدداً، وأثناء تحليقها تتجمع شظايا بطاقات الواجهة في عرض مبسط للمنتج مع أثر onion skin.
- 11-13.5 ث: يعود الضوء؛ جملة واحدة تصف ما يفعله المنتج تملأ الإطار بخط ضخم، كل كلمة تتجاوز موضعها ثم تستقر.
- 13.5-15 ث: شعار العلامة الحقيقي يُرسم كمسار خطي، والاسم يُكتب بجانبه، ضربة صوتية عميقة، ثبات 400 مللي ثانية، خروج نظيف.

## Proposed scenes
- 0-2s: Paper canvas fades up; a Caveat handwriting note writes itself via stroke-dashoffset (420ms) posing the buyer's problem; soft pen-scratch SFX.
- 2-5s: Hard cut to charcoal dark mode as the drums drop; a ball with real gravity falls from the top, squashes on landing (120ms) and bounces twice while a three-word Anton headline slams in word by word.
- 5-8s: Back to paper on the beat; marker arrows and a hand-drawn diagram sketch the product's core loop; small accent-colour labels pop in with 60ms stagger.
- 8-11s: Second dark switch; the ball is launched again and, while airborne, UI card fragments assemble into a simplified product view with onion-skin trails.
- 11-13.5s: Light returns; one sentence of what the product does fills the frame in giant type, each word overshooting then settling.
- 13.5-15s: The real logo mark draws in as a stroke path, the wordmark types in beside it, a sub-bass hit lands, 400ms hold, clean out.

## قواعد الحركة
- التسهيل: الدخول بـ back.out(1.7) خلال 500-700 مللي ثانية؛ الخروج بـ power3.in خلال 250-350 مللي ثانية؛ الكرة تتبع جاذبية حقيقية مع انضغاط 1.25x/0.8x عند الارتطام.
- الإيقاع: فكرة بصرية جديدة كل 1500-2000 مللي ثانية؛ لا يبقى شيء أكثر من ثانيتين دون تغيير حالة.
- الانتقالات: حركة رئيسية واحدة لكل قطع (انقلاب إلى الداكن، ضربة كرة، اصطدام كلمة)؛ يُمنع الدفع والانزلاق والتأرجح العام.
- الطباعة: خط Anton للعناوين بارتفاع 18-24% من الإطار، الكلمات تدخل بتتابع 80 مللي ثانية؛ ملاحظات Caveat تُرسم عبر stroke-dashoffset خلال 350-500 مللي ثانية.
- اللون: ورق فاتح، لون حبر واحد، لونا تمييز مخصصان للملاحظات؛ الوضع الداكن فحمي مشتق من اللوحة نفسها ويُبدَّل في إطار واحد لا بتلاشٍ متقاطع.
- الكاميرا: ثابتة بلا تقريب؛ يُوحى بالعمق فقط عبر onion skin وإطارات السحب (smear) والمتابعة (follow-through).
- كل حالة بداية تُعلن عند t=0 ليكون التمرير آمناً؛ لا يُخفى خروج عنصر خلف دخول آخر.
- ممنوع على الشاشة: شريط التمرير، الكود الزمني، عداد الإطارات، مصطلحات المحرّكين، نسب مئوية أو أسماء عملاء مخترعة. الصوت: مؤثر على كل ضربة، إتقان عند -14 LUFS و -2 dBTP.

## Motion rules
- Easing: entrances use back.out(1.7) at 500-700ms; exits use power3.in at 250-350ms; the ball follows true gravity with squash of 1.25x/0.8x on impact.
- Rhythm: a new visual idea every 1500-2000ms; nothing holds longer than 2s without a change of state.
- Transitions: one primary move per cut (a flip to dark, a ball strike, a word slam); push, slide and swing wipes are banned.
- Typography: Anton for headline type at 18-24% of frame height, words enter staggered 80ms apart; Caveat notes draw in via stroke-dashoffset over 350-500ms.
- Colour: a light paper canvas, one ink colour, two accents reserved for notes; dark mode is a charcoal derived from the same palette, switched in a single frame, never crossfaded.
- Camera: locked, no zooms; depth is suggested only by onion skins, smear frames and follow-through.
- Every from-state is declared at t=0 so scrubbing is safe; an exit is never hidden behind an entrance.
- Banned on screen: scrubbers, timecodes, fps counters, animator vocabulary, invented percentages or customer names. Audio: an SFX on every hit, master at -14 LUFS / -2 dBTP.

## Facts stated by the source (rewritten in our words)
- Runs 15 seconds, built with HyperFrames and GSAP, with no narration and no recorded footage.
- Visual world: a light paper canvas, marker-style notes that draw themselves, a ball with real physics, oversized kinetic type and abrupt light/dark switches.
- Pacing target: a fresh idea roughly every 1.5 to 2 seconds, with a sound effect on every impact.
- Typography: Anton for the big moving words, Caveat handwriting animated through stroke-dashoffset.
- Music is sectioned: drums drop out on the dark switch and while the ball is in the air, then return on the type and logo hits.
- Copy rules: speak to the buyer, name what the product learns, no invented numbers or customer names, no UI chrome, no animator vocabulary on screen.
- Ending: the real logo mark plus the product name set in the brand wordmark font, never a boxed logo image.
- Audio delivery: CC0 or generated sounds only, mastered to -14 LUFS and -2 dBTP.

## Assumptions
The product, palette, fonts and positioning are template placeholders in the source, so the beats above assume a generic B2B software product; the ball-and-flip sequence order is a proposed direction, not an observed one.

## Keywords
paper canvas, marker notes, physics ball, kinetic type, dark mode flip, gsap, hyperframes, sfx hits, anton font, ورق, قلم تحبير, كرة فيزيائية, خط ضخم, إطلاق منتج
