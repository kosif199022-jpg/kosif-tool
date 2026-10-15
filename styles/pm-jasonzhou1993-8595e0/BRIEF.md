# ريل موشن ذاتي: عرض مهارات في 15 ثانية — Claude motion reel

> شوريل سريع مدته 15 ثانية يربط الطباعة الحركية والرسوم البيانية ومنظومات الأشكال في قطعة واحدة متصلة تعمل كبطاقة تعريف لمصمم موشن.
>
> A 15-second self-promotional showreel that chains kinetic type, animated charts and shape systems into one continuous portfolio piece.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/jasonzhou1993-8595e0
- التصنيفات / Categories: charts, kinetic-type
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 15 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: Remotion, React, SVG

## الفكرة
الموضوع هو ريل تعريفي يرافق سيرة ذاتية، يثبت فيه المصمم اتساع مهاراته في 15 ثانية فقط. الهدف التواصلي هو إقناع المشاهد بجودة الحِرفة لا بكثرة المؤثرات. ما يميز لغة الحركة هنا بناء الفصول: كل ثلاث ثوانٍ فصل لتخصص مختلف (نص، بيانات، أشكال، شعار) يربطها عنصر واحد متحوّل، نقطة تصبح مؤشراً ثم عموداً في رسم بياني ثم حرفاً.

## Concept
The subject is a résumé-style reel in which the designer proves range in just 15 seconds. The communication goal is to convince through craft rather than effect count. The distinctive motion language is its chaptering: every three seconds a different discipline (type, data, shapes, logo) takes over, all tied by one transforming motif, a dot that becomes a cursor, then a chart bar, then a letter.

## المشاهد المقترحة
- 0-2 ث: افتتاح بارد على نقطة واحدة تتمدد إلى خط ثم تنطبق على كلمة «MOTION» حرفاً حرفاً، مع ضربة طبل عند هبوط كل حرف.
- 2-5 ث: فصل الطباعة الحركية: ثلاث عبارات قصيرة («نص»، «بيانات»، «أشكال») تنزلق على محاور متناوبة عبر أقنعة كشف، وتخرج كل واحدة مع دخول التالية.
- 5-8 ث: فصل الرسوم البيانية: خط أساس الكلمة الأخيرة يتحول إلى محور سيني؛ ستة أعمدة تنمو بتأخير 60 مللي ثانية بينها، ثم تتحول إلى رسم خطي يُرسم مساره من اليسار إلى اليمين.
- 8-11 ث: فصل الأشكال: الرسم الخطي ينطوي إلى شبكة مربعات مستديرة الزوايا تدور وتغيّر ألوانها وتعيد تجميع نفسها في علامة تشبه الشعار.
- 11-13.5 ث: تسارع: العلامة تتكاثر في نفق من الخطوط الخارجية بينما يرتفع عداد رقمي (مشاريع، سنوات) بأرقام جدولية.
- 13.5-15 ث: استقرار على بطاقة ختام هادئة: الاسم والدور وسطر التواصل تستقر بتأخير 200 مللي ثانية؛ كل ما عداها يتلاشى عائداً إلى النقطة الأولى.

## Proposed scenes
- 0-2s: Cold open on a single dot that stretches into a line and snaps into the word 'MOTION' letter by letter, with a drum hit on each letter landing.
- 2-5s: Kinetic type chapter: three short claims ('Type', 'Data', 'Shapes') slide in on alternating axes through masked reveals, each exiting as the next enters.
- 5-8s: Chart chapter: the baseline of the last word becomes an x-axis; six bars grow with 60 ms staggered offsets, then morph into a line chart whose path draws left to right.
- 8-11s: Shape chapter: the line chart folds into a grid of rounded squares that rotate, recolour and reassemble into a logo-like mark.
- 11-13.5s: Speed ramp: the mark multiplies into a tunnel of outlines while a counter ticks up a figure (projects, years) in tabular numerals.
- 13.5-15s: Resolve on a calm end card: name, role and contact line settle with a 200 ms stagger; everything else fades back to the single dot.

## قواعد الحركة
- منحنى التسارع الأساسي: cubic-bezier(0.22, 1, 0.36, 1) (expo-out) للدخول بمدة 450-600 مللي ثانية؛ الخروج بمنحنى cubic-bezier(0.65, 0, 0.35, 1) خلال 300 مللي ثانية.
- تغيير الفصول بقطع حاد أو match-cut على النبضة؛ لا يتجاوز أي تلاشٍ 150 مللي ثانية في أي موضع.
- الكاميرا: مسرح ثنائي الأبعاد مع دفعة بطيئة واحدة لكل فصل (تكبير من 1.00 إلى 1.05 خلال 3 ثوانٍ)، تُعاد فقط عند القطع الحاد.
- الخط: خط sans هندسي واحد (Inter، أو IBM Plex Sans Arabic للنسخة العربية) بوزنين 500 و800؛ الحروف تدخل بتأخير 40 مللي ثانية وإزاحة رأسية 12 بكسل، ولا تُكشف بالشفافية وحدها أبداً.
- الرسوم البيانية: الأعمدة تنمو من خط الأساس بنابض (كتلة 1، صلابة 180، تخميد 22)؛ المسارات الخطية تُرسم بـ stroke-dashoffset خلال 700 مللي ثانية.
- اللون: خلفية داكنة واحدة، مقدمة فاتحة واحدة، ولون تمييز لا يغطي أكثر من 10% من الإطار؛ يتبدل لون التمييز مرة واحدة في كل فصل.
- ممنوع: القوالب الجاهزة، الاهتزاز العشوائي، أكثر من خطين، التلاشي البطيء، الجسيمات الزخرفية.

## Motion rules
- Primary easing: cubic-bezier(0.22, 1, 0.36, 1) (expo-out) for entrances lasting 450-600 ms; exits use cubic-bezier(0.65, 0, 0.35, 1) at 300 ms.
- Chapter changes are hard cuts or match-cuts on the beat; no dissolve anywhere may exceed 150 ms.
- Camera: a 2D stage with one slow push per chapter (scale 1.00 to 1.05 over 3 s), reset only on hard cuts.
- Type: one geometric sans (Inter, or IBM Plex Sans Arabic for the Arabic variant), weights 500 and 800; letters enter with a 40 ms stagger and a 12 px vertical offset, never by opacity alone.
- Charts: bars grow from the baseline on a spring (mass 1, stiffness 180, damping 22); line paths draw with stroke-dashoffset over 700 ms.
- Colour: one dark background, one light foreground, one accent covering at most 10% of the frame; the accent swaps once per chapter.
- Banned: stock templates, random jitter, more than two typefaces, slow fades, decorative particles.

## Facts stated by the source (rewritten in our words)
- Requested length is 15 seconds.
- The piece is meant to work as a personal showreel attached to a résumé.
- The creator asked for a dynamic, maximal result rather than a restrained one.
- Tagged on the site under charts and kinetic type; listed at 1920x1080.

## Assumptions
The source names only the length and the résumé-showreel purpose; the chaptered structure, chart-to-shape morphs, palette and easing values are proposed. Output size 1920x1080 is taken from the listing.

## Keywords
showreel, portfolio reel, kinetic typography, animated charts, shape morph, remotion, beat sync, بورتفوليو, طباعة حركية, رسوم بيانية متحركة, مقطع تعريفي, مصمم موشن, فصول حركية
