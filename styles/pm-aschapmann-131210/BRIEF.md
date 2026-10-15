# فيلم إطلاق منتج SaaS مبرمج في Remotion — SaaS launch video

> فيلم إطلاق مدته 30 ثانية مبني بالكامل بالكود في Remotion، يروي قصة السوق والألم والحل عبر أربع إلى خمس مشاهد وينتهي بشعار SVG متحرك.
>
> A 30-second, fully code-built Remotion launch film telling market, pain, fix and payoff in 4-5 scenes, ending on an animated SVG logo with tagline and URL.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/aschapmann-131210
- التصنيفات / Categories: product-ui, charts, kinetic-type, characters, photos, music, code
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 30 s · الصعوبة / Difficulty: 4/5
- التقنية المقترحة / Stack: Remotion, React, SVG

## الفكرة
الموضوع منتج SaaS يُقدَّم للمرة الأولى، والمادة الخام تُستخرج من صفحة الهبوط والكود الفعلي: النص والألوان والخط والشعار المحوَّل إلى SVG. الهدف أن تُقرأ القصة كخط واحد متصل: لماذا يهم هذا السوق، لماذا الوضع الحالي مؤلم، كيف يحل المنتج المشكلة، وماذا يحصل عليه المستخدم. لغة الحركة هي لغة فيلم منتج فاخر: كلمات تظهر واحدة تلو الأخرى بنوابض، دفعات كاميرا هادئة، عمق وتوهج، وعناصر تُبنى على الإيقاع مع مؤثر صوتي ناعم لكل ظهور وصمت فيما عدا ذلك.

## Concept
The subject is a SaaS product at launch, with raw material pulled from its real landing page and codebase: text, palette, typeface and a logo traced to SVG. The goal is a single continuous storyline: why this market matters, why today hurts, how the product fixes it, and what the user walks away with. The motion language is that of a premium product film: words arriving one by one on springs, gentle camera pushes, depth plus glow, elements assembling on the beat with a soft sound for each appearance and silence in between.

## المشاهد المقترحة
- 0-6 ث: لماذا يهم السوق: حقل متدرج داكن، عنوان من سطر واحد ينبثق كلمة كلمة بنابض (stiffness 180، damping 14)، دفعة كاميرا بطيئة بنسبة 4% على امتداد المشهد.
- 6-12 ث: ألم الوضع الحالي: ثلاث شظايا واجهة متشابكة تنجرف وتتداخل بتوهج خافت؛ عنوان قصير يواجهها؛ الكاميرا تنزاح 60 بكسل يساراً.
- 12-19 ث: كيف يحل المنتج المشكلة: الشظايا تلتحم في واجهة المنتج الحقيقية، الشعار المتتبَّع يظهر في زاوية، تسميات المزايا تُبنى على أرباع الإيقاع.
- 19-25 ث: ما الذي تحصل عليه: بطاقات النتائج تنزلق للأعلى بنوابض متتابعة، خط مخطط رفيع يُرسم خلال 900 مللي ثانية، كل بطاقة تحصل على نقرة صوتية ناعمة.
- 25-30 ث: كشف الشعار: مسارات SVG تُرسم خلال 700 مللي ثانية، التعبئة تتفتح بتوهج شعاعي، الشعار النصي يتلاشى تحته، عنوان الموقع يُكتب ويثبت 1.2 ثانية.

## Proposed scenes
- 0-6s: Why it matters: a dark gradient field, a one-line title springs in word by word (stiffness 180, damping 14), a slow 4% camera push across the scene.
- 6-12s: The pain today: three tangled UI fragments drift and overlap with dim glow; a short title counters them; camera pans 60px left.
- 12-19s: How it fixes it: fragments snap into the product's real interface, the traced logo appears in a corner, feature labels build in on quarter-beats.
- 19-25s: What you get: outcome cards slide up on staggered springs, a thin chart line draws across 900ms, each card gets one soft tick sound.
- 25-30s: Logo reveal: SVG paths draw over 700ms, the fill blooms with a radial glow, the tagline fades under it, the URL types in and holds 1.2s.

## قواعد الحركة
- نوابض لكل دخول: stiffness 170-200، damping 12-16، كتلة 1؛ لا حركات خطية أو ease-in-out للحركات الرئيسية.
- الخط الحركي يدخل كلمة كلمة بفاصل 70 مللي ثانية؛ لا تُكمل كلمة دخولها بعد بداية المشهد التالي.
- الكاميرا: دفعات بطيئة متصلة بنسبة 3-5% لكل مشهد أو انزياحات أقل من 80 بكسل؛ لا انزياحات خاطفة ولا دوران.
- كل مشهد يبقى مقروءاً: 1.8 ثانية على الأقل دون حركة على العنوان بعد استقراره.
- الصوت: مؤثر ناعم واحد لكل عنصر يظهر، وصمت فيما عدا ذلك؛ لا يُفترض وجود خلفية موسيقية.
- اللون والخط من موقع العلامة فقط؛ التوهج نسخة مموهة بشفافية 30%، لا مرشح bloom عام.
- الشعار SVG متجهي ليُرسم كخط ويُكبَّر؛ يُمنع الشعار النقطي.
- قبل التسليم تُفحص الإطارات بحثاً عن تداخل أو قص أو إيقاع متعجل؛ أي عنصر يظهر أقل من 400 مللي ثانية تُمدَّد مدته.

## Motion rules
- Springs for every entrance: stiffness 170-200, damping 12-16, mass 1; no linear or ease-in-out tweens for primary moves.
- Kinetic type enters word by word with 70ms spacing; a word never finishes its entrance after the next scene begins.
- Camera: continuous slow pushes of 3-5% scale per scene or pans under 80px; no whip pans, no rotation.
- Each scene stays readable: a minimum of 1.8s with no movement on the title after it settles.
- Audio: one soft SFX per appearing element, otherwise silence; no music bed is assumed.
- Colour and font come only from the brand's own site; glow is a blurred duplicate at 30% opacity, never a generic bloom filter.
- The logo is vector SVG so it can be stroke-drawn and scaled; a bitmap logo is banned.
- Before delivery, frames are inspected for overlaps, clipping and rushed beats; anything visible under 400ms is extended.

## Facts stated by the source (rewritten in our words)
- Length is fixed at 30 seconds and the whole film is written as Remotion code so it can be edited and re-rendered.
- Content is sourced from the product's own landing page and repository: story, text, palette, typeface and logo, with the logo traced into SVG.
- Narrative is four or five scenes, each with one short title: market importance, current pain, the product's fix, and what the user gains.
- Style notes: word-by-word kinetic type, spring easing, gentle camera pushes/pans, depth plus glow, elements assembling on the beat rather than popping in.
- Sound: one soft effect per appearing element and silence otherwise.
- Ending: a closing animated logo, then tagline and web address, followed by a self-check of rendered frames for overlaps, clipping or rushed timing.

## Assumptions
The product itself is a placeholder, so scene content assumes a generic B2B tool; specific timings, spring values and the dark gradient look are proposed, not stated.

## Keywords
remotion launch, spring easing, kinetic typography, camera push, logo reveal, svg logo, product film, code video, ساس, إطلاق, نوابض, شعار متحرك, قصة المنتج, برمجة الفيديو
