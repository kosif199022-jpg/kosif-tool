# ريل تعريفي لمصمم موشن بالذكاء الاصطناعي — Claude motion designer showreel

> ريل ذاتي مدته 15 ثانية يستعرض مهارات المصمم عبر نص حركي ورسوم بيانية حية وانتقالات متصلة بلا قطع.
>
> A 15-second self-portrait reel where the designer proves its craft through kinetic type, living charts and seamless morph transitions.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/stephanlivera-df17a2
- التصنيفات / Categories: charts, kinetic-type
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 15 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: Remotion, React, SVG

## الفكرة
الموضوع هو ريل تقديم شخصي: الذكاء الاصطناعي يقدم نفسه كمصمم موشن ويثبت ذلك بالفعل لا بالقول. الهدف التواصلي أن يخرج المشاهد مقتنعاً بالإتقان خلال 15 ثانية فقط. اللغة الحركية تعتمد على سلسلة مشاهد متولدة من بعضها: كل عنصر يتحول إلى العنصر التالي، والنص يُعامل كجسم فيزيائي له وزن وارتداد، والرسوم البيانية تُرسم كأنها تتنفس مع الإيقاع.

## Concept
The subject is a self-introduction: the AI presents itself as a motion designer and proves it through doing rather than claiming. The goal is to leave the viewer convinced of craft within 15 seconds. The motion language chains scenes that grow out of each other, treats type as a physical body with weight and bounce, and draws charts that breathe with the rhythm.

## المشاهد المقترحة
- 0-2.5 ث: نقطة واحدة على خلفية فاتحة تنتفخ لتصبح اسم المصمم بخط عريض؛ تهبط الحروف واحداً تلو الآخر بتجاوز زنبركي 1.15 مع دفع كاميرا خفيف بنسبة 4%.
- 2.5-5.5 ث: يتناثر الاسم إلى سحابة كلمات للمهارات (الطباعة، التسهيل، الأنظمة)؛ تدور الكلمات حول محور مشترك ثم تنقر إلى عمود محاذٍ لليسار بينما تُرسم خطوط قاعدية رفيعة.
- 5.5-9 ث: يتحول الخط القاعدي إلى محور سيني لرسم أعمدة؛ ترتفع ستة أعمدة بتدرج 80 مللي ثانية، ويتجاوز خط بياني هدفه ثم يستقر، ويتدحرج عداد رقمي إلى رقم مستدير.
- 9-12 ث: يمتد أطول عمود ليصبح كبسولة رأسية تتحول إلى إطار هاتف؛ تنزلق بداخله ثلاث بطاقات واجهة بعمق متوازي بينما تدور الكاميرا 6 درجات.
- 12-15 ث: ينكمش الإطار إلى نقطة تطير إلى المركز ويظهر الترويسة الختامية (الاسم + الدور + 'متاح')؛ يطابق الإطار الأخير نقطة البداية ليُغلق الريل حلقة.

## Proposed scenes
- 0-2.5s: A single period on an off-white canvas inflates into the designer's name set in a heavy grotesque; letters land one by one with a 1.15 spring overshoot and a subtle camera push of 4%.
- 2.5-5.5s: The name shatters into a word cloud of skills (typography, easing, systems); words orbit a shared pivot, then snap into a left-aligned stack while a thin baseline rules draw across.
- 5.5-9s: The baseline becomes the x-axis of a bar chart; six bars rise in staggered 80 ms steps, a line series overshoots and settles, and a callout counter rolls to a round number.
- 9-12s: The chart's tallest bar stretches into a vertical pill that becomes a phone-shaped frame; inside it, three UI cards slide in with parallax depth as the camera orbits 6 degrees.
- 12-15s: The frame contracts to a dot, the dot flies to the center and the closing lockup (name + role + 'available') resolves; the final frame mirrors the opening dot so the reel loops.

## قواعد الحركة
- التسهيل الأساسي زنبرك بصلابة 180 وتخميد 18 وكتلة 1؛ انزلاقات الواجهة تستخدم cubic-bezier(0.2, 0.8, 0.2, 1) خلال 450 مللي ثانية.
- لا قطع حاد: كل انتقال هو تحول شكلي أو مسح بقناع أو عبور بالتكبير؛ أطول ثبات ساكن 900 مللي ثانية.
- الكاميرا منصة افتراضية واحدة متصلة: دفع للأمام 3-6%، دوران لا يتجاوز 8 درجات، ولا اهتزاز أبداً.
- النص يتحرك حرفاً حرفاً بتدرج 40 مللي ثانية؛ الكلمات الخارجة والداخلة لا تتداخل على السطر نفسه.
- أعمدة الرسم البياني تنمو من الصفر بالزنبرك؛ الخطوط تُرسم عبر stroke-dashoffset خلال 600 مللي ثانية وتتجاوز هدفها 8% ثم تستقر.
- اللون: خلفية فاتحة واحدة، حبر داكن واحد، ولون تمييز واحد لا يشغل أكثر من 10% من الإطار.
- ممنوع: وهج العدسة، انفجارات الجسيمات، ظلال أعمق من 2 بكسل، اللقطات الجاهزة، والتلاشي إلى الأسود بين المشاهد.

## Motion rules
- Primary easing is a spring with stiffness 180, damping 18, mass 1; UI slides use cubic-bezier(0.2, 0.8, 0.2, 1) over 450 ms.
- No hard cuts: every transition is a morph, a mask wipe or a scale-through; the longest static hold is 900 ms.
- Camera is one continuous virtual rig: push-ins of 3-6%, orbits of at most 8 degrees, never a shake.
- Type animates per glyph with a 40 ms stagger; outgoing and incoming words never overlap on the same baseline.
- Chart bars grow from zero with the spring; line series draw with stroke-dashoffset over 600 ms and overshoot by 8% before settling.
- Colour: one light canvas, one near-black ink and a single accent used on no more than 10% of the frame at any time.
- Banned: lens flares, particle explosions, drop shadows deeper than 2 px, stock footage, and fade-to-black between scenes.

## Facts stated by the source (rewritten in our words)
- The creator asked for a 15-second piece.
- The piece is framed as a portfolio reel that stands in for a résumé.
- The public tags are charts and kinetic type.

## Assumptions
The source gives only the length and the résumé-reel framing; the scene order, the off-white palette, the chart content and the looping ending are proposed directions, not observed facts.

## Keywords
showreel, portfolio reel, kinetic typography, spring easing, bar chart animation, morph transition, ريل تعريفي, نص حركي, رسوم بيانية متحركة, انتقالات متصلة, سيرة ذاتية, self promo
