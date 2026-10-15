# جولة التقنيات: ريل الخمس عشرة ثانية — Motion techniques showreel

> ريل مدته 15 ثانية تقوده كاميرا واحدة متصلة عبر ستة عوالم صغيرة، كل عالم يستعرض تقنية (جسيمات، هندسة ثلاثية، سوائل، أقنعة، صور) وينتهي بما يبدأ به التالي.
>
> A 15-second reel driven by one continuous camera through six micro-worlds, each demonstrating a technique (particles, 3D geometry, fluids, masks, photos) and ending as the next begins.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/lukasersil-0ed38e
- التصنيفات / Categories: charts, kinetic-type, shapes, particles, photos
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 15 s · الصعوبة / Difficulty: 5/5
- التقنية المقترحة / Stack: Remotion, Three.js, WebGL

## الفكرة
الموضوع ريل شخصي لمصمم موشن يريد عرض أوسع طيف ممكن من التقنيات المتقدمة في 15 ثانية دون أن يبدو كخليط عشوائي. الهدف التواصلي هو إقناع مدير فني بأن صاحب الريل يتحكم في الإيقاع والانتقال والإضاءة والعمق بقدر تحكمه في المؤثرات. ما يميز اللغة الحركية أن كل تقنية تُسلّم للتي تليها مادياً: الحرف يتفتت جسيمات، الجسيمات تتكثف جسماً ثلاثياً، الجسم يصبح ممراً، والممر يتموج سائلاً؛ فلا يوجد قطع واحد، بل سلسلة تحوّلات تتابعها الكاميرا.

## Concept
The subject is a personal reel for a motion designer who wants to show the widest possible spread of advanced techniques in 15 seconds without it reading as a random pile of effects. The goal is to convince an art director that the author controls pacing, transitions, lighting and depth as much as the effects themselves. What makes the motion language distinctive is that each technique physically hands off to the next: a letter shatters into particles, particles condense into a 3D solid, the solid extrudes into a corridor, the corridor ripples into liquid; there is not a single cut, only a chain of transformations the camera follows.

## المشاهد المقترحة
- 0-2 ث: كلمة واحدة ضخمة تضرب الإطار بتدرج لكل حرف، ثم تتفتت حروفها إلى نحو 4,000 جسيم تتناثر نحو العدسة.
- 2-5 ث: تدور الجسيمات إلى الداخل وتتكثف جسماً متعدد الأوجه يدور بإضاءة حافة؛ تدور الكاميرا 40 درجة بينما تنبثق حواف الجسم إلى الخارج.
- 5-8 ث: تصبح الانبثاقات جدران ممر؛ تطير الكاميرا عبره بينما تنفتح أقنعة هندسية على الجدران كاشفة صوراً تنزلق في parallax.
- 8-11 ث: يسيل الجدار البعيد: حقل إزاحة يشوّه آخر صورة إلى حقل لوني، وعبارات حركية تركب الموجات بخطوط قاعدة تتبع التشوه.
- 11-13 ث: يهدأ السائل إلى أرضية؛ ترتفع منها أعمدة رسم بياني كأفق مدينة، وتميل الكاميرا لأعلى ويلف الأعمدة ضباب عمق.
- 13-15 ث: ينهار كل شيء نحو نقطة ضوء واحدة تتحول إلى بطاقة اسم المصمم؛ تثبيت ثانية على الأسود مع الاسم.

## Proposed scenes
- 0-2s: One oversized word slams into frame with per-letter stagger, then its glyphs shatter into roughly 4,000 particles that scatter toward the lens.
- 2-5s: The particles swirl inward and condense into a rotating faceted solid with a rim light; the camera orbits 40 degrees while the solid's edges extrude.
- 5-8s: The extrusions become walls of a corridor; the camera flies through as geometric masks on the walls open to reveal photographs sliding past in parallax.
- 8-11s: The far wall liquefies: a displacement field warps the last photo into a colour field, and kinetic phrases ride the waves with their baselines following the distortion.
- 11-13s: The liquid settles into a floor; bars of a chart rise from it like a skyline, the camera tilts up and the bars catch depth fog.
- 13-15s: Everything collapses toward a single point of light that resolves into the designer's name card; hold 1 second on black with the name.

## قواعد الحركة
- لا قطع حاد في أي مكان: كل حد بين مشهدين هو morph أو حمل كاميرا أو match بملء الإطار؛ متوسط اللقطة 2.5 ثانية ولا تتجاوز أي لقطة 3 ثوان.
- الدخولات بمنحنى expo-out بقيمة cubic-bezier(0.19, 1, 0.22, 1) خلال 400-700 ms؛ التفكك (التفتت، التسييل) بمنحنى ease-in بقيمة cubic-bezier(0.7, 0, 0.84, 0) لتتراكم الطاقة قبل الانفلات.
- كاميرا ثلاثية واحدة طوال 15 ثانية مع مجال رؤية ينزاح بين 35 و60 درجة؛ تُمفتح الحركات كموضع مع look-at، ولا تُحرَّك الدورانات منفصلة أبداً.
- الجسيمات نقاط instanced على GPU، من 2,000 إلى 6,000 في كل لقطة، حجمها 1.5-3 px، مع تأخير لكل جسيم مشتق من بعده عن المركز لتُقرأ التدفقات كموجات.
- الإضاءة مفتاح واحد وحافة وضباب عمق يبدأ عند 60 بالمئة من عمق المشهد؛ الظلال ناعمة ولا تكون سوداء خالصة أبداً.
- الطباعة: خط grotesk فائق الثقل بوزنين فقط؛ النص يجلس دائماً على سطح أو مسار داخل المشهد ولا يطفو كطبقة مسطحة.
- اللون: قاعدة شبه سوداء، أبيض، ولونا تمييز لا يظهران معاً بكامل تشبعهما في اللحظة نفسها.
- ممنوع: lens flare، طبقات glitch، خامات جاهزة، أكثر من عائلة خط، تعبيرات اهتزاز أو wiggle، وأي crossfade.

## Motion rules
- No hard cuts anywhere: every scene boundary is a morph, a camera carry-through or a fill-the-frame match; the average beat is 2.5 s and no beat exceeds 3 s.
- Entrances use expo-out cubic-bezier(0.19, 1, 0.22, 1) over 400-700 ms; dissolutions (shatter, liquefy) use ease-in cubic-bezier(0.7, 0, 0.84, 0) so energy builds before release.
- One 3D camera for the full 15 s with field of view drifting between 35 and 60 degrees; moves are keyed as position plus look-at, never as separate rotation tweens.
- Particles are GPU-instanced points, 2,000-6,000 per beat, size 1.5-3 px, with per-particle delay derived from distance to the origin so flows read as waves.
- Lighting is a single key, a rim and depth fog starting at 60 percent of scene depth; shadows are soft and never pure black.
- Typography: one ultra-bold grotesk in exactly two weights; type always sits on a surface or path in the scene, never floats as a flat overlay.
- Colour: one near-black base, white, and two accents that are never on screen at full saturation at the same time.
- Banned: lens flares, glitch overlays, stock textures, more than one font family, shake or wiggle expressions, any crossfade.

## Facts stated by the source (rewritten in our words)
- Duration is stated as 15 seconds and the piece is framed as a portfolio reel meant to get a motion designer hired.
- The creator lists the techniques to cover: kinetic typography, transitions, 2D and 3D animation, abstract geometry, fluid simulation, particles, distortion, masking, compositing, lighting, depth and camera movement.
- The creator wants fast, confident pacing with every shot flowing into the next, and an art-directed feel rather than a loose effects collection.
- Site tags: charts, kinetic type, shapes, particles, photos.

## Assumptions
Stated: 15 seconds, the technique list, fast pacing, seamless transitions and the art-directed intent. Assumed: the six-world hand-off structure, particle counts, easing values, lighting setup and the two-accent palette.

## Keywords
showreel, portfolio reel, particles, جسيمات, 3d geometry, fluid distortion, masking, compositing, أقنعة, إضاءة, camera flythrough, كاميرا متصلة, morph transition, تشوه سائل, depth fog
