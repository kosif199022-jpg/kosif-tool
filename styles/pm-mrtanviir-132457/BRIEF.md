# ريل مهارات موشن: أربعة فصول على إيقاع واحد — Claude motion designer showreel

> ريل ترويج ذاتي في 15 ثانية يثبت أربع مهارات متتابعة: حروف حركية، مخططات تُبنى من الصفر، أشكال تتحول، وبطاقة توقيع ختامية.
>
> A 15-second self-promo reel proving four motion skills in sequence: kinetic type, charts built from zero, morphing shapes, and a signature end card.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/mrtanviir-132457
- التصنيفات / Categories: charts, kinetic-type
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 15 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: Remotion, React, SVG

## الفكرة
الموضوع ريل تعريفي قصير يقدّم المصمم كما تقدّم السيرة الذاتية صاحبها، لكن بالحركة بدل الكلمات. الهدف إقناع المشاهد خلال 15 ثانية بأن من صنعه يتقن الحروف والبيانات والإيقاع معاً. تتميز لغة الحركة بتقسيم الزمن إلى فصول قصيرة، لكل فصل مهارة واحدة، مع قطع حاد على شبكة إيقاعية ثابتة بحيث يدخل كل عنصر بتجاوز طفيف ويخرج بقفزة سريعة.

## Concept
The subject is a short self-introduction reel that presents the designer the way a CV would, but through movement instead of bullet points. The goal is to convince a viewer within 15 seconds that the author handles type, data and rhythm together. The motion language splits time into short chapters, one skill per chapter, with hard cuts on a fixed beat grid so every element enters with a slight overshoot and leaves with a fast snap.

## المشاهد المقترحة
- 0-1.5 ث: إطار أسود؛ كلمة عنوان واحدة تندفع حرفاً حرفاً بتأخير 60ms بين الحروف مع وميض أبيض لإطار واحد عند آخر حرف.
- 1.5-5 ث: فصل الحروف الحركية: ثلاث عبارات قصيرة (مقترح: Type / Data / Rhythm) تدور حول محور عمودي، وكل كلمة تتقلص من 140% إلى 100% بينما يرتفع خط قاعدتها 12px.
- 5-9 ث: فصل المخططات: ستة أعمدة تنمو من الصفر (400ms لكل عمود مع تأخير 80ms)، وخط بياني يُرسم عبر stroke-dashoffset خلال 1.2 ثانية، وعدّاد يتصاعد من 0 إلى 98%.
- 9-12.5 ث: فصل الأشكال: دائرة تتحول إلى مربع مستدير ثم مثلث عبر استيفاء مسارات SVG؛ تنقلب ألوان الخلفية مع كل تحول.
- 12.5-15 ث: بطاقة الختام: الاسم والدور وسطر التواصل تستقر بمنحنى ease-out خلال 600ms؛ ثبات تام لثانية واحدة.

## Proposed scenes
- 0-1.5s: Black frame; one headline word slams in letter by letter with a 60ms stagger and a one-frame white flash on the last letter.
- 1.5-5s: Kinetic-type chapter: three short claims (proposed: Type / Data / Rhythm) rotate on a vertical axis, each word scaling from 140% to 100% while its baseline shifts up 12px.
- 5-9s: Chart chapter: six bars grow from zero (400ms each, 80ms stagger), a line draws via stroke-dashoffset over 1.2s, and a counter eases from 0 to 98%.
- 9-12.5s: Shape chapter: a circle morphs into a rounded square then a triangle through SVG path interpolation; the background inverts on each morph.
- 12.5-15s: End card: name, role and a contact line settle with a 600ms ease-out; 1s static hold.

## قواعد الحركة
- شبكة إيقاعية بسرعة 120 BPM: كل قطع أو دخول يقع على مضاعفات 250ms أو 500ms.
- الدخول بمنحنى cubic-bezier(0.22, 1, 0.36, 1) خلال 450ms؛ الخروج بمنحنى cubic-bezier(0.64, 0, 0.78, 0) خلال 220ms، فالخروج أسرع من الدخول دائماً.
- تأخير الحروف 60ms ولا يتحرك أكثر من 12 حرفاً في اللحظة نفسها.
- أعمدة المخطط تتمدد على محور Y من نقطة ارتكاز سفلية؛ العدّادات تتسارع بمنحنى ease-out ولا تكون خطية أبداً.
- الكاميرا ثابتة باستثناء دفعتين للأمام بنسبة 4% تستغرق كل منهما ثانيتين؛ لا اهتزاز يدوي.
- اللوحة ثنائية اللون (أرضية داكنة ولون تمييز واحد)؛ يُسمح بالانقلاب الكامل فقط أثناء تحول الأشكال.
- عائلة خط grotesque واحدة بوزنين؛ تباعد الحروف يضيق من +8 إلى 0 عند استقرار كل كلمة.
- ممنوع: التلاشي المتقاطع، الظلال الساقطة، انفجارات الجسيمات الجاهزة، وأكثر من ثلاثة عناصر متحركة معاً.

## Motion rules
- Beat grid at 120 BPM: every cut and entry lands on a multiple of 250ms or 500ms.
- Entries use cubic-bezier(0.22, 1, 0.36, 1) over 450ms; exits use cubic-bezier(0.64, 0, 0.78, 0) over 220ms, so exits are always faster than entries.
- Letter stagger is 60ms and no more than 12 glyphs animate at the same time.
- Chart bars scale on Y from a bottom transform-origin; counters tween with ease-out, never linear.
- Camera stays static except two 4% push-ins lasting 2s each; no handheld shake.
- Palette is two-tone (dark ground plus one accent); a full inversion is allowed only during shape morphs.
- One grotesque family in two weights; tracking tightens from +8 to 0 as each word settles.
- Banned: crossfades, drop shadows, stock particle bursts, and more than three elements moving at once.

## Facts stated by the source (rewritten in our words)
- Length is fixed at 15 seconds.
- Purpose: a self-promotional reel used as a designer's résumé piece.
- Tagged on the site as charts and kinetic type; no stack, colours or scene order are given.

## Assumptions
The source only fixes the length and the résumé-reel purpose; the chapter structure, 120 BPM grid, two-tone palette and all timings are proposed. The 1280x720 frame is read as 16:9.

## Keywords
showreel, ريل مصمم, سيرة ذاتية متحركة, kinetic typography, bar chart animation, shape morph, beat grid, حروف حركية, مخطط متحرك, تحول الأشكال, self promo, remotion reel, قطع حاد
