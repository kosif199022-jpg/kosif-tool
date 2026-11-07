# أشكال سائلة لامعة تتحول وتندمج كقطرات معدن ملون — أشكال سائلة

> ريل عمودي ناعم تتحرك فيه كتل سائلة لامعة بألوان متدرجة: قطرات تندمج وتنفصل كالزئبق الملون، تتحول من دائرة إلى رقم إلى أيقونة، وتنكسر الإضاءة على سطحها، مع كلمات قليلة تطفو بين الأشكال.
>
> A smooth vertical reel of glossy liquid blobs in gradient colours: drops merge and split like coloured mercury, morph from sphere to number to icon, with light bending across their surfaces and a few words floating between the shapes.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://github.com/kosif199022-jpg/kosif-one
- التصنيفات / Categories: shapes, 3d
- النسبة المقترحة / Aspect: 9:16 · المدة / Duration: 28 s · الصعوبة / Difficulty: 4/5
- التقنية المقترحة / Stack: Three.js, WebGL, React, Remotion

## الفكرة
الفكرة أن المادة نفسها هي الرسالة: كتلة سائلة واحدة تتشكل من جديد في كل مشهد لتصبح الرمز التالي في القصة، فلا قطع بين الأفكار بل تحول مستمر. الإحساس فاخر وهادئ يناسب العلامات التقنية والعطور والمقدمات. يختلف عن «مخططات متحولة» بأن التحول هنا عضوي وسائل وليس بيانات، وعن مشاهد 3D السينمائية بأنه تجريدي بلا عالم أو شخصيات.

## Concept
The idea is that the material is the message: one liquid mass re-forms in every scene into the next symbol of the story, so ideas never cut, they flow. The feel is premium and calm, suited to tech brands, fragrance and intros. It differs from morph-charts because the morph is organic and fluid rather than data, and from cinematic-3d because it is abstract, with no world or characters.

## المشاهد المقترحة
- 0-3 ث: الافتتاح: قطرة واحدة تسقط في منتصف الإطار وتتناثر لتصبح كرة مترجرجة بلمعة براقة.
- 3-9 ث: الكرة تتمدد وتنقسم إلى ثلاث قطرات صغيرة تدور حول المركز؛ وأول كلمة من العنوان ترتفع بينها.
- 9-16 ث: القطرات تندمج من جديد بعنق متصل، وتتحول الكتلة إلى رقم أو أيقونة كبيرة للمعلومة الأساسية.
- 16-23 ث: الكاميرا تدور ببطء حول الشكل؛ والألوان تسري داخله كالحبر في الزيت؛ ويظهر سطر نص ثانٍ.
- 23-28 ث: الشكل يذوب إلى بركة صغيرة ثم يعيد تشكيل نفسه شعاراً يستقر بترجرج خفيف؛ ويظهر الشعار النصي.

## Proposed scenes
- 0-3s: Hook: a single drop falls into frame centre, splashes into a wobbling sphere with a glossy highlight.
- 3-9s: The sphere stretches and splits into three smaller drops that orbit; the first headline word rises between them.
- 9-16s: The drops merge back with a metaball neck and the mass morphs into a large numeral or icon for the key fact.
- 16-23s: Camera slowly orbits the shape; colours flow through it like ink in oil; a second line of text appears.
- 23-28s: The shape melts down into a puddle that reforms as the logo, settling with a soft jiggle; the tagline fades in.

## قواعد الحركة
- الألوان: خلفية #0e0b1f تتدرج نحو #1d1440، تدرج السائل #ff4fd8 ثم #7a5cff ثم #2fd3ff، اللمعة #ffffff، النص #f2efff.
- الأشكال كتل اندماجية أو أشكال مسافة موقّعة مع إضاءة حواف ولمعة حادة واحدة؛ والسطوح تترجرج بضوضاء بطيئة (دورة 1.5-2.5 ثانية).
- كل الانتقالات تحولات: لا قطع ولا تلاشي بين المشاهد؛ كل تحول يستمر 18-30 إطاراً بتسهيل بطيء في البداية والنهاية مع ترجرج صغير (2-3 اهتزازات مخمدة) عند الاستقرار.
- الاندماج والانقسام يظهران دائماً عنقاً واضحاً يرق قبل أن ينقطع.
- النص قليل (5 كلمات كحد أقصى على الشاشة) بخط عربي رفيع (مثل Tajawal Light أو IBM Plex Sans Arabic Light) بحجم 56-72 بكسل، يرتفع 20 بكسل مع ظهور في 12 إطاراً.
- الكاميرا تنساب ببطء (دوران 10-20 درجة في المشهد)، ولا تهتز أبداً.

## Motion rules
- Palette: background #0e0b1f fading to #1d1440, liquid gradient #ff4fd8 -> #7a5cff -> #2fd3ff, highlight #ffffff, text #f2efff.
- Shapes are metaballs or SDF blobs with fresnel rim light and one sharp specular highlight; surfaces wobble with low-frequency noise (period 1.5-2.5 s).
- All transitions are morphs: no cuts, no fades between scenes; each morph lasts 18-30 frames with a slow-in slow-out ease and a small jiggle (2-3 damped oscillations) on settle.
- Merges and splits always show a visible neck that thins before snapping.
- Text is minimal (max 5 words on screen), light Arabic sans (e.g. Tajawal Light or IBM Plex Sans Arabic Light) 56-72 px, rises 20 px with a fade over 12 frames.
- Camera drifts slowly (orbit 10-20 degrees per scene), never shakes.

## Facts stated by the source (rewritten in our words)
- KOSIF lists this as an original style named for liquid shapes, tagged shapes and 3D.

## Assumptions
Authored KOSIF definition, not an observed reference: the record points only to the repo root, so there was no video to watch. Palette hex values, fonts, timings and scene beats are design choices written for this style, not measurements.

## Keywords
liquid, morph, metaballs, fluid shapes, glossy, blob, abstract 3d, أشكال سائلة, تحول, سائل, زئبق, تجريدي, انسيابي
