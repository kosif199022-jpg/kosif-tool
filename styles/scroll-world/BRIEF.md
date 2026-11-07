# عالم متصل يتكشف مع التمرير — عالم تمرير

> فيديو يحاكي التمرير في موقع تفاعلي فاخر: الكاميرا تنزل أو تتقدم داخل عالم واحد متصل، مقاطع تثبت ثم تتحول، عناصر ثلاثية الأبعاد تدور مع تقدم التمرير، ونصوص تظهر في أقسام، مع شريط تقدم ومؤشر تمرير صغير.
>
> A video that mimics scrolling through an award-style interactive website: the camera descends or advances through one continuous world, sections pin then transform, 3D objects rotate in step with scroll progress, text blocks reveal per section, with a slim progress bar and scroll hint.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://github.com/kosif199022-jpg/kosif-one
- التصنيفات / Categories: 3d, product-ui
- النسبة المقترحة / Aspect: 9:16 · المدة / Duration: 32 s · الصعوبة / Difficulty: 4/5
- التقنية المقترحة / Stack: Remotion, React, Three.js, GSAP

## الفكرة
الفيديو كله لقطة واحدة متصلة يقودها «التمرير»: كل قسم من القصة مرحلة في عالم واحد، والانتقال ليس قطعًا بل امتداد. الإحساس أن المشاهد يتصفح موقعًا مذهلًا بإصبعه. يناسب استعراض المنتجات والمشاريع ومواقع الويب والقصص التي لها تسلسل.

## Concept
The whole video is one continuous shot driven by a virtual 'scroll': each story section is a stage in a single world, and transitions are extensions, not cuts. The viewer feels they are swiping through a stunning website. It suits product and project showcases, websites and sequential stories.

## المشاهد المقترحة
- 0-3 ث: القسم الافتتاحي: مجسم ثلاثي كبير يطفو في المنتصف مع العنوان؛ وتلميح «مرّر» صغير ينبض في الأسفل.
- 3-9 ث: يبدأ التمرير الافتراضي: المجسم يدور بنسبة تقدم التمرير بينما ينزلق العنوان للأعلى ويخرج؛ ونص القسم الثاني يثبت على الجانب.
- 9-15 ث: الكاميرا تعبر المجسم (أو بوابة) إلى مساحة داخلية؛ والقسم الثالث يتكشف كبطاقات تتكدس مع التمرير.
- 15-22 ث: قسم أفقي مثبّت: العالم ينزلق جانبيًا عبر 3-4 لوحات بينما يستمر التمرير الرأسي، والأرقام تعدّ.
- 22-28 ث: العالم يبتعد ليُظهر أن كل الأقسام جزء من مشهد واحد؛ وشريط التقدم يقترب من 100%.
- 28-32 ث: قسم التذييل: الدعوة لفعل والرابط؛ والتمرير يتباطأ حتى يتوقف بارتداد خفيف.

## Proposed scenes
- 0-3s: Hero section: a large 3D object floats centre with the headline; a small 'scroll' hint pulses at the bottom.
- 3-9s: Virtual scroll starts: the object rotates proportionally to scroll progress while the headline slides up and out; section 2 text pins on the side.
- 9-15s: The camera passes through the object (or a portal) into an interior space; section 3 reveals as cards stacking with scroll.
- 15-22s: Horizontal pinned section: the world slides sideways through 3-4 panels while vertical scroll continues, numbers counting.
- 22-28s: The world zooms out to show every section was part of one landscape; the progress bar nears 100%.
- 28-32s: Footer section: call to action and URL; the scroll eases to a stop with slight overscroll bounce.

## قواعد الحركة
- كل شيء دالة في قيمة تمرير واحدة s(t) من 0 إلى 1 مع قصور ذاتي ناعم (تسارع في البداية وتباطؤ مع تجاوز 3-5% في النهاية)؛ ولا قطع أبدًا.
- الأقسام المثبتة تثبت خلال 15-25% من تقدم التمرير بينما يتحرك محتواها الداخلي، ثم تتحرر.
- دوران المجسم وموضع الكاميرا وظهور النصوص مرتبطة بـs بنطاقات محددة؛ والنص يظهر خلال 8-12% من التقدم.
- إطار الواجهة: إطار متصفح أو هاتف رفيع اختياري، شريط تقدم 3-4 بكسل، وأرقام أقسام 01/05؛ بشكل هادئ.
- العمق: 3-5 طبقات بسرعات مختلفة وضباب خفيف يفصل المقدمة عن الخلفية.
- اللوحة: حبر عميق #0e0f14، أبيض مكسور #f3f1ec، تأكيد برتقالي كهربائي #ff6a2b، سماوي ثانوي #8fb8ff، وتدرجات ناعمة بين الأقسام.
- الخط: عربي عرضي كبير (Readex Pro 700 أو IBM Plex Sans Arabic 700 بحجم 110-160 بكسل) محاذى لليمين مع تسميات لاتينية صغيرة بخط أحادي المسافة؛ والكتل النصية سطران على الأكثر.
- الفرق عن البارالاكس والجولة السينمائية: البارالاكس رسم مسطح بطبقات؛ والجولة السينمائية طيران عبر لقطات مولدة بالذكاء الاصطناعي؛ أما عالم التمرير فبإحساس واجهة ويب يقوده التمرير بأقسام مثبتة ومجسمات ثلاثية.

## Motion rules
- Everything is a function of one scroll value s(t) from 0 to 1, with smooth inertia (ease-in at start, ease-out with 3-5% overscroll at end); never cut.
- Pinned sections hold for 15-25% of scroll progress while their inner content animates, then release.
- 3D object rotation, camera position and text reveals map to s with clamped ranges; text reveals over 8-12% of progress.
- UI chrome: optional slim browser or phone frame, 3-4 px progress bar, section numbers 01/05; keep it subtle.
- Depth: 3-5 layers at different speeds and a soft fog to separate foreground from background.
- Palette: deep ink #0e0f14, off-white #f3f1ec, accent electric orange #ff6a2b, secondary sky #8fb8ff, soft gradients between sections.
- Type: large display Arabic (Readex Pro 700 or IBM Plex Sans Arabic 700, 110-160 px) right-aligned with small Latin mono labels; text blocks max 2 lines.
- Difference from parallax-2d and higgsfield-journey: parallax-2d is flat layered illustration; higgsfield-journey is a cinematic AI-footage fly-through; scroll-world is web-UI-like, scroll-driven with pinned sections and 3D objects.

## Facts stated by the source (rewritten in our words)
- The public description states nothing specific beyond the title.

## Assumptions
This is an authored KOSIF definition, not an observed reference: there is no reference video for this base style, so palette, type, timings and beats are a design decision written for KOSIF, to be refined per project. The 'scroll' is simulated as a timeline value in the render; no live website is recorded.

## Keywords
scroll world, scrollytelling, scroll driven, pinned sections, website showcase, 3d web, one shot, عالم تمرير, تمرير, موقع تفاعلي, استعراض موقع, لقطة واحدة, أقسام مثبتة
