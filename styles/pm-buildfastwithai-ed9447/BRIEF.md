# طائرة مروحية ثلاثية الأبعاد قابلة للطيران في ملف HTML واحد — Three.js Skyraider aircraft model

> عرض مدته 39 ثانية لطائرة هجوم مروحية من الحرب الباردة مبنية بالكود في Three.js: تقف على أرضية رملية مبلطة بجانب لوحة تحكم بيضاء، والكاميرا تدور حولها بينما تتحرك أجزاؤها (المروحة، الغطاء، القلابات، الأجنحة المطوية) ويتبدل طلاؤها وحمولتها، ثم تقلع فوق غابة إجرائية خضراء وتنتهي ببطاقة ختام بخط مكثف داكن.
>
> A 39-second showcase of a code-built Cold War propeller attack plane in Three.js: it sits on a tiled sand apron beside a white control panel while the camera orbits and its parts move (prop, canopy, flaps, folding wings) and its paint and stores swap, then it flies over a procedural green patchwork and ends on a dark condensed-type end card.

ملف تعريفي أصلي من إعداد KOSIF، رُوجع وصُحّح مقابل إطارات مأخوذة من فيديو المرجع (2026-11-06)؛ التوقيتات والألوان قراءات تقريبية من تلك الإطارات، فراجع المرجع للتفاصيل الدقيقة.
Original KOSIF brief, revised against frames sampled from the reference video (2026-11-06); timings and colours are approximate readings from those frames, so check the reference for fine detail.

- المرجع / Reference: https://www.promptsmotion.com/buildfastwithai-ed9447
- التصنيفات / Categories: 3d, product-ui
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 39 s · الصعوبة / Difficulty: 5/5
- التقنية المقترحة / Stack: Three.js, WebGL, HTML Canvas, CSS

## الفكرة
الفكرة استعراض قدرة: طائرة كاملة بتفاصيلها مصنوعة من هندسة إجرائية بلا ملفات نماذج ولا صور، والفيديو يثبت ذلك بالحركة. الشاشة مقسومة: المشهد ثلاثي الأبعاد يملأ نحو 80% يساراً، ولوحة إعدادات ضيقة يميناً يضغط فيها مؤشر حقيقي على الأزرار. فوق المشهد شريط عنوان صغير يتغير مع كل فصل، واسم الطائرة بخط مكثف ثقيل أسفل اليسار.

## Concept
The idea is a capability demo: a fully detailed aircraft built from procedural geometry with no model files or images, and the video proves it through motion. The screen is split: the 3D scene fills about 80% on the left and a narrow settings panel sits on the right, where a real cursor clicks the toggles. A small caption pill above the scene changes per chapter, and the aircraft name sits bottom-left in heavy condensed type.

## المشاهد المقترحة
- 0-3 ث: لقطة منخفضة بزاوية ثلاثة أرباع للطائرة على أرضية رملية مبلطة مع خط أشجار ضبابي؛ شريط عنوان يقول إنها بُنيت كملف HTML واحد؛ ويبدأ دوران بطيء.
- 3-9 ث: الكاميرا تلتف حول المقدمة بينما يضغط المؤشر في اللوحة: المروحة تدور (حلقة ضبابية صفراء عند الأطراف)، الغطاء ينزلق، والقلابات ومكابح الغوص تنفتح.
- 9-13 ث: تبديل الطلاء من تمويه أخضر وبيج إلى طلاء بحري أبيض ورمادي لامع، مع ظهور حمولات تحت الأجنحة (قنابل وصواريخ)؛ ومنزلق التقادم يغير الاتساخ.
- 13-16 ث: لقطة أمامية قريبة للمروحة الدائرة والمحرك النجمي مع عنوان يقول إن دالة واحدة تبني الطائرة كلها.
- 16-21 ث: العودة للتمويه؛ الأجنحة الخارجية تنطوي عمودياً للتخزين على حاملة الطائرات، من زاوية أمامية جانبية.
- 21-33 ث: تلاشٍ إلى السماء: الطائرة تطير آلياً فوق رقعة حقول إجرائية ضبابية وخصلات سحاب، والكاميرا تطاردها وتميل حولها.
- 33-39 ث: تلاشٍ متقاطع إلى بطاقة ختام بلون أخضر رمادي فاتح: وسم صغير، عنوان من سطرين بخط مكثف ثقيل، سطر فرعي بعبارة مظللة، وصف من أرقام صغيرة؛ ثم ثبات.

## Proposed scenes
- 0-3s: Low three-quarter view of the plane on a tiled sand apron with a hazy tree line; a caption pill states it was built as one HTML file; slow orbit begins.
- 3-9s: Camera swings around the nose while the cursor toggles the panel: propeller spins up (yellow tip ring blur), canopy slides, flaps and dive brakes deploy.
- 9-13s: Paint swap from green-and-tan jungle camo to a glossy navy white/grey scheme, with wing stores (bombs, rockets) appearing under the wings; weathering slider changes grime.
- 13-16s: Head-on close-up of the spinning prop and radial engine with a caption that a single factory function builds the whole aircraft.
- 16-21s: Back to camo; the outer wings fold up vertically for carrier stowage, seen from the front quarter.
- 21-33s: Fade through to the sky: the plane flies on autopilot over a hazy procedural patchwork of fields and wisps of cloud, camera chasing and banking around it.
- 33-39s: Cross-fade to a pale sage end card with a small kicker, a two-line heavy condensed headline, a subline with a highlighted phrase and a row of small stats; hold.

## قواعد الحركة
- دوران كاميرا بطيء متصل بلا قطعات حادة؛ الفصول تتبدل بتغيير شريط العنوان وتلاشيين ناعمين (إلى الطيران عند نحو 21 ث، وإلى بطاقة الختام عند نحو 33 ث).
- كل جزء ميكانيكي يتحرك بتسهيله الخاص: تسارع المروحة بقرص ضبابي وحلقة صفراء عند الأطراف، انزلاق الغطاء، نزول القلابات والمكابح، وطي الجناح حول المفصل في نحو 1.5 ث.
- مؤشر ظاهر يتحكم في لوحة يمنى (أزرار مقسمة، منزلقات، بطاقات طلاء) ليرى المشاهد السبب والنتيجة.
- اللوحة: أرضية رملية #b9ad98، سماء ضبابية #d9dccf، تمويه أخضر #6f7f4a وبيج #c9b48a، أبيض بحري #e8e8e4، لوحة بيضاء #f6f5f0، حبر #2b2a26، أصفر أطراف المروحة #e3c33a، وبطاقة الختام أخضر رمادي #d4d6c8.
- الخط: عرض مكثف ثقيل لاسم الطائرة وبطاقة الختام، وخط بسيط صغير لأشرطة العناوين وتسميات اللوحة.
- قسم الطيران فيه ضباب جوي ناعم وملمس حقول ينزلق تحت الطائرة؛ والطائرة تميل برفق (نحو 20 درجة).

## Motion rules
- Continuous slow camera orbits with no hard cuts; chapters change by caption swap and two soft fades (into the flight at ~21 s, into the end card at ~33 s).
- Every mechanical part animates on its own easing: prop spin-up with a motion-blur disc and yellow tip ring, canopy slide, flap and brake drop, wing fold rotating about the hinge over ~1.5 s.
- Visible cursor drives a right-hand control panel (segmented toggles, sliders, livery cards) so viewers see cause and effect.
- Palette: sand apron #b9ad98, haze sky #d9dccf, camo green #6f7f4a and tan #c9b48a, navy white #e8e8e4, panel white #f6f5f0, ink #2b2a26, prop-tip yellow #e3c33a, end card sage #d4d6c8.
- Type: heavy condensed slab-ish display for the aircraft name and end card, small sans for caption pills and panel labels.
- Flight section uses soft atmospheric fog and a fields texture that scrolls under the plane; the plane banks gently (±20°).

## Facts stated by the source (rewritten in our words)
- The subject is a Douglas A-1H Skyraider built with Three.js.
- The source prompt is very short (about seven words) and lists Three.js as the technology.
- No duration, scene structure or style direction is given in the record.

## Assumptions
Observed from 24 frames sampled every ~1.6 s across 39 s: the split scene/panel layout, cursor-driven part animation, livery and stores swap, wing fold, autopilot flight over procedural fields and the end card. Assumed: exact hex values (estimated from frames), easing curves, and whether the screen recording was captured live or rendered; the audio track exists but was not analysed.

## Keywords
three.js, procedural 3d, aircraft, warbird, configurator, orbit camera, wing fold, flight sim, tech demo, طائرة, نموذج ثلاثي الأبعاد, هندسة إجرائية, عرض تقني, محاكاة طيران
