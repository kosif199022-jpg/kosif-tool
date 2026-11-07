# شرح تفاعلي ثلاثي الأبعاد لمحرك صاروخ Raptor 3 بمقطع عرضي — Interactive Raptor 3 rocket engine explainer

> تسجيل شاشة مدته 10 ثوانٍ لصفحة ويب تفاعلية ثلاثية الأبعاد: محرك صاروخ على منصة اختبار في حظيرة ليلية يطلق لهباً بنفسجياً طويلاً بعقد صدمة، مع لوحة عنوان وأرقام أداء يساراً ولوحة أزرار أعلى اليمين؛ نقرة على «مقطع عرضي» تشق المحرك فتظهر المضخات والأنابيب الملونة بملصقات، ثم تقترب الكاميرا ببطء بينما يتتبع مسار الأكسجين.
>
> A 10-second screen capture of an interactive 3D web page: a rocket engine on a night test stand fires a long violet plume with shock diamonds, framed by a title card and stat readouts on the left and a control panel top-right; a click on 'cutaway' slices the engine open to reveal labelled colour-coded pumps and pipes, then the camera slowly pushes in while the oxygen path is highlighted.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/konstantinsaifo-96fc89
- التصنيفات / Categories: diagrams, 3d
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 10 s · الصعوبة / Difficulty: 5/5
- التقنية المقترحة / Stack: Three.js, WebGL, React, CSS

## الفكرة
الفكرة أن يرى المشاهد ما لا يراه عادة: داخل محرك صاروخ أثناء الاشتعال. المشهد ثلاثي الأبعاد حقيقي في المتصفح (منصة اختبار بمسامير، أرضية زرقاء معدنية، إضاءة كاشفة من الأعلى)، والواجهة فوقه زجاجية داكنة بسيطة تسمح بالتحكم: متابعة سائل معين، الارتفاع، طريقة عرض المحرك (كامل، مقطع، مفكك) وشريط دفع. الإيقاع هادئ: لقطة ثابتة تقريباً للهب ثم تحول واحد كبير عند فتح المقطع.

## Concept
The idea is to show what nobody normally sees: the inside of a rocket engine while it fires. The scene is real-time 3D in the browser (a bolted test stand, a steel-blue floor, a top spotlight) and the UI on top is minimal dark glass with controls: follow a fluid, altitude, engine view (whole, cutaway, exploded) and a throttle slider. The pacing is calm: an almost static hold on the plume, then one big change when the cutaway opens.

## المشاهد المقترحة
- 0-4 ث: لقطة عريضة بزاوية ثلاثة أرباع: المحرك مثبت على لوح مثقب داكن ويطلق لهباً بنفسجياً ناعماً بعقدتي صدمة أو ثلاث لامعة وملصقات صغيرة طافية؛ العنوان وفقرة المقدمة وثلاث بطاقات أرقام أعلى اليسار، لوحة التحكم أعلى اليمين، وشارة مسار صغيرة أسفل الوسط.
- 4-4.6 ث: المؤشر ينقر زر المقطع العرضي: الفوهة تصبح شفافة بلون برتقالي وردي ساخن، والغلاف ينكشف عن الأنابيب الداخلية.
- 4.6-7 ث: عرض المقطع: أنابيب برتقالية معزولة تنحني فوق المحرك، كتلة مضخة حمراء، مضخات أكسجين سماوية وغرفة احتراق ليلكية، لكل منها ملصق داكن صغير بخط إشارة؛ ونص اليسار يتبدل لشرح مسار السائل.
- 7-8 ث: المؤشر يختار مرشح الأكسجين (الشارة تضيء بالسماوي)؛ أجزاء الأكسجين تتوهج أكثر وبقية الأجزاء تخفت قليلاً.
- 8-10 ث: اقتراب بطيء مع دوران خفيف نحو المضخات والغرفة؛ اللهب يملأ نصف الكادر الأيمن وينتهي المقطع والحركة مستمرة.

## Proposed scenes
- 0-4s: Wide three-quarter view: the engine bolted to a dark perforated plate fires a soft violet plume with two or three bright shock diamonds and small floating labels; the title, intro paragraph and three stat tiles sit top-left, the control panel top-right, a small breadcrumb pill bottom-centre.
- 4-4.6s: The cursor clicks the cutaway toggle: the nozzle turns translucent hot orange-pink and the casing peels away to show the inner plumbing.
- 4.6-7s: Cutaway view: orange insulated pipes arc over the top, a red turbopump block, cyan oxygen-side pumps and a lilac combustion chamber, each with a small dark leader-line label; the left text block swaps to a description of the flow.
- 7-8s: The cursor selects the oxygen fluid filter (pill highlights cyan); the oxygen-side parts glow brighter while others dim slightly.
- 8-10s: Slow push-in and slight orbit toward the pumps and chamber; the plume fills the right half of frame as the clip ends mid-move.

## قواعد الحركة
- مشهد ثلاثي الأبعاد حي بانجراف كاميرا بطيء ومستمر؛ وتغيير حالة حاد واحد فقط في المقطع كله (من كامل إلى مقطع عرضي).
- اللهب توهج حجمي جمعي بنفسجي #8a6cf0 يتدرج إلى لافندر #c9b8ff مع عقد صدمة بيضاء ساخنة ترتعش قليلاً.
- ترميز ألوان المقطع: الأنابيب المعزولة برتقالي #e3a23a، المضخة أحمر #d9583a، جانب الأكسجين سماوي #6fd3f0، الغرفة ليلكي #c7b6ff، على حظيرة شبه سوداء #0a0d1a وأرضية زرقاء معدنية #3a4f86.
- الواجهة ألواح زجاجية داكنة شبه شفافة #12151dcc بحدود فاتحة 1px؛ والزر النشط يصبح شارة بيضاء أو سماوية #66c8ff.
- الخط: خط هندسي بلا زوائد للعنوان (كبير والسطر الثاني سماوي)، نص رمادي صغير، وخط أحادي العرض لقيم الأرقام.
- تغييرات الحالة تنساب في نحو 400-600 مللي ثانية؛ والملصقات تظهر بتلاشٍ مع خطوط إشارة قصيرة بعد استقرار المقطع.
- مؤشر فأرة ظاهر يقود التفاعل، فيُقرأ العمل كعرض منتج وليس فيلماً.

## Motion rules
- Real-time 3D scene with a slow continuous camera drift; only one hard state change (whole to cutaway) in the whole clip.
- The plume is an additive volumetric glow, violet #8a6cf0 fading to lavender #c9b8ff with white-hot shock diamonds that flicker slightly.
- Cutaway colour code: insulated pipes orange #e3a23a, turbopump red #d9583a, oxygen side cyan #6fd3f0, chamber lilac #c7b6ff, against a near-black hangar #0a0d1a and steel-blue floor #3a4f86.
- UI is dark translucent glass panels #12151dcc with 1px light borders; the active toggle becomes a white or cyan #66c8ff pill.
- Type: a geometric sans for the title (large, cyan second line), small grey body text, and monospace for the stat values.
- State changes ease over about 400-600 ms; labels fade in with short leader lines after the cutaway settles.
- A visible cursor drives the interaction, so the piece reads as a product demo rather than a film.

## Facts stated by the source (rewritten in our words)
- The subject is an interactive explainer of the Raptor 3 rocket engine.
- The page lists diagrams as its only tag; no duration or stack is stated.

## Assumptions
Observed from 24 frames over the 10 s clip plus one full-size still: the test-stand scene, violet plume, the cutaway click, labelled colour-coded internals, the fluid filter and the slow push-in. The clip is low resolution (720x406) and has no audio track, so small UI text was read only approximately. Assumed: the exploded view and other controls exist but were not shown in action.

## Keywords
rocket engine, cutaway, interactive 3D, engineering explainer, turbopump, exhaust plume, Three.js, screen capture, محرك صاروخ, مقطع عرضي, شرح هندسي, ثلاثي الأبعاد تفاعلي, لهب
