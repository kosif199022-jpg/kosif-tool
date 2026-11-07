# رسومات تقنية — مخطط هندسي أزرق يُرسم خطاً خطاً — رسومات تقنية

> ريل عمودي 9:16 على ورق مخطط هندسي أزرق داكن بشبكة سماوية باهتة، تُرسم فيه آلة أو جهاز أو مبنى بخطوط بيضاء رفيعة كأنها بقلم رسم فني، ثم تنفصل أجزاؤه في عرض مُفكَّك وتظهر خطوط الأبعاد والأسهم والتسميات العربية بخط هندسي أحادي، مع ختم عنوان في زاوية الورقة.
>
> A 9:16 reel on deep cyanotype-blue blueprint paper with a faint cyan grid, where a machine, device or building is traced in thin white drafting lines, then splits into an exploded view while dimension lines, leader arrows and monospace Arabic/English labels write on, finishing on a stamped title block in the corner.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://github.com/kosif199022-jpg/kosif-one
- التصنيفات / Categories: diagrams, hand-drawn
- النسبة المقترحة / Aspect: 9:16 · المدة / Duration: 35 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: Remotion, React, SVG

## الفكرة
كل شيء يُفهم من خلال طريقة بنائه: الفيديو يعامل الموضوع كوثيقة هندسية. لا ألوان طبيعية ولا ظلال، فقط خطوط بيضاء على أزرق المخطط، والمعلومة تأتي عبر خطوط الأبعاد والمقاطع العرضية والتكبير على التفاصيل. الكاميرا ثابتة على الورقة وتتحرك فقط بزوم وانزلاق دقيق كأن العين تقرأ المخطط، والإيقاع هادئ ومنهجي.

## Concept
Things are explained by how they are built: the video treats its subject as an engineering document. No natural colour or shading, only white linework on blueprint blue, with information carried by dimension lines, cross-sections and detail call-outs. The camera stays on the sheet and only zooms or slides precisely, like an eye reading a drawing, at a calm, methodical pace.

## المشاهد المقترحة
- 0-2 ث: الشبكة تظهر على ورق #0d3b66؛ علامات المحاذاة وإطار رفيع يُرسمان من الزوايا إلى الداخل؛ ويظهر إطار جدول العنوان أسفل اليمين.
- 2-8 ث: يُرسم محيط العنصر الرئيسي بالأبيض (#eaf4ff، سُمك 2 بكسل)، الحدود الخارجية أولاً ثم الأجزاء الداخلية، مع علامة تصويب صغيرة على رأس الخط.
- 8-14 ث: تمتد خطوط الأبعاد بنهاياتها القصيرة من العنصر، وتُكتب الأرقام والتسميات بخط أحادي بجانب كل خط.
- 14-22 ث: عرض مُفكَّك: تنزلق الأجزاء متباعدة على خطوط محور متقطعة (0.8 ث لكل جزء) ويأخذ كل جزء دائرة ترقيم.
- 22-30 ث: تكبير تفصيلة: دائرة متقطعة حول مفصل، ثم دفع للكاميرا (1.2 ث) إلى مقطع مكبّر مظلل بخطوط مائلة.
- 30-35 ث: تعود الأجزاء لتتجمع؛ يمتلئ جدول العنوان باسم الفيديو بالعربية والتاريخ والمقياس، ويُطبع ختم اعتماد أحمر (#e4572e) بضربة من 110٪ إلى 100٪.

## Proposed scenes
- 0-2s: The grid fades in on #0d3b66 paper; registration marks and a thin border draw from the corners inwards; a title block outline appears bottom-right.
- 2-8s: The main object outline traces in white (#eaf4ff, 2 px), outer contour first, then inner parts, with a small crosshair riding the line tip.
- 8-14s: Dimension lines with end ticks extend from the object; numbers and labels type on in monospace beside each one.
- 14-22s: Exploded view: parts slide apart along dashed centre lines (0.8 s each, easeInOutCubic) and each part gets a numbered balloon.
- 22-30s: Detail call-out: a dashed circle on one joint, then a camera push (1.2 s) into an enlarged section with hatching.
- 30-35s: Parts reassemble; the title block fills with the video title in Arabic, date and scale, and a red approval stamp (#e4572e) thumps in at 110% to 100%.

## قواعد الحركة
- الألوان: الورق #0d3b66، الشبكة #3d6f99 بشفافية 35٪ (خط رئيسي كل 5 مربعات)، الخطوط #eaf4ff، الخطوط المتقطعة الثانوية #8fb8de، ولون تمييز واحد #e4572e للأختام والتحذيرات فقط.
- كل خط يُرسم تدريجياً بسرعة رسم ثابتة (نحو 600 بكسل/ث)؛ الحدود الخارجية قبل التفاصيل الداخلية، ولا شيء يظهر دفعة واحدة.
- التسميات بخط أحادي صغير (IBM Plex Sans Arabic للعربي وIBM Plex Mono للأرقام) ومربوطة دائماً بخط إشارة؛ والعربية من اليمين لليسار تُكتب كلمة كلمة دون تقطيع الحروف المتصلة.
- الأجزاء في العرض المفكك تتحرك على خطوط محور مستقيمة فقط بتسارع وتباطؤ ناعم؛ بلا دوران ولا ارتداد.
- حركة الكاميرا زوم وانزلاق دقيق (1-1.5 ث) بين مناطق الورقة؛ والورقة نفسها لا تميل أبداً.
- لا تعبئة لونية إلا التظليل المائل 45 درجة في المقاطع؛ لا تدرجات ولا ظلال سوى تعتيم خفيف جداً لأطراف الورقة.
- الفرق عن السبورة البيضاء والسبورة الطباشيرية: لا يد ولا قلم ظاهر ولا اهتزاز؛ الخطوط مستقيمة بالمسطرة وتقنية.

## Motion rules
- Palette: paper #0d3b66, grid #3d6f99 at 35% opacity (major every 5 cells), linework #eaf4ff, secondary dashed lines #8fb8de, single accent #e4572e only for stamps and warnings.
- Every line draws on with stroke-dashoffset at a constant drafting speed (about 600 px/s); outer contour before inner details, never all at once.
- Labels use a monospace face (IBM Plex Sans Arabic for Arabic, IBM Plex Mono for numbers), uppercase-feel, small, always attached to a leader line; Arabic stays RTL and is typed word by word, never letter-split.
- Exploded views move only along straight axis lines with easeInOutCubic; no rotation, no bounce.
- Camera moves are precise zooms and pans (1-1.5 s, easeInOutQuad) between areas of the sheet; the sheet itself never tilts.
- No fills except 45-degree hatching on cut sections; no gradients or shadows besides a very faint paper vignette.
- Different from whiteboard/chalkboard: no hand, no marker, no wobble; lines are ruler-straight and technical.

## Facts stated by the source (rewritten in our words)
- Catalogued as a KOSIF original style named for technical drawings, in the Diagrams and Hand-drawn categories.

## Assumptions
Authored KOSIF definition, not an observed reference: there is no reference video for this base style (its page is the KOSIF repo root), so palette hex values, type choices, timings and scene beats are original KOSIF design decisions, not measurements. Assumed a 9:16 reel of about 35 s explaining how an object is built; the exploded view and title block are proposed signature beats.

## Keywords
blueprint, technical drawing, exploded view, dimension lines, cyanotype, engineering, line draw-on, مخطط هندسي, رسم تقني, بلوبرنت, عرض مفكك, خطوط أبعاد, هندسة
