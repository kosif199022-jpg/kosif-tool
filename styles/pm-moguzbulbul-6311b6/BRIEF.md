# شرح قرارات تصميم واجهة بمخطط هندسي شفاف — UX decision explainer animation

> شرح هادئ مدته 42 ثانية لإعادة تصميم صفحة سجل عميل في نظام إدارة علاقات: الصفحة الأصلية الرمادية تتحول إلى مخطط هندسي بخطوط سماوية وتعليقات قياس، ثم تعود معدّلة؛ خمسة مبادئ مرقمة (إجراء أساسي واحد، إخفاء الفراغ، العمل المفتوح أولاً، خط زمني واحد، الفعل في سياقه) بتعليق سفلي قصير لكل خطوة، حتى تكتمل الصفحة بلوحة رد جانبية.
>
> A calm 42-second explainer of a CRM record-page redesign on off-white: the grey original dissolves into a cyan blueprint wireframe with measurement callouts, then returns improved, across five numbered principles (one primary action, hide absence, open work first, one timeline, act in context), each with a short caption, until the page ends with a side reply panel.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/moguzbulbul-6311b6
- التصنيفات / Categories: product-ui, diagrams
- النسبة المقترحة / Aspect: 4:3 · المدة / Duration: 42 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: Remotion, React, CSS, SVG

## الفكرة
الموضوع تبرير قرارات تصميم واجهة خطوة بخطوة. كل قرار يمر بثلاث حالات: الواجهة كما هي، ثم «أشعة سينية» بمخطط سماوي يُبرز المشكلة بالقياسات والتسميات، ثم الواجهة بعد الإصلاح. لا ألوان صاخبة ولا قطعات؛ الإقناع يأتي من رؤية التغيير على الصفحة نفسها.

## Concept
The subject is justifying UI design decisions one step at a time. Each decision passes through three states: the interface as is, then an 'X-ray' cyan blueprint that exposes the problem with measurements and labels, then the interface after the fix. No loud colour and no cuts; persuasion comes from seeing the change on the same page.

## المشاهد المقترحة
- 0-7 ث: صفحة السجل الأصلية (شريط جانبي، رأس الشركة بستة أزرار متساوية، عمود تفاصيل طويل، تبويبات النشاط) على أوف وايت؛ تتلاشى إلى مخطط هندسي بقوس حول صف الأزرار، والتعليق 01 يذكر المشكلة؛ ثم ينكمش الصف إلى زر أساسي واحد وقائمة.
- 7-14 ث: الخطوة 02: عمود التفاصيل يتحول إلى مخطط، صفوفه الفارغة الكثيرة محددة ومعدودة؛ ثم ينكمش إلى سطر ملخص مضغوط تحت اسم الشركة، ويظهر تكملة التعليق بالسماوي.
- 14-21 ث: الخطوة 03: قائمة النشاط تحت الأشعة مع إبراز صف تذكير متأخر؛ وتُضاف بطاقة «تحتاجك» بثلاث مهام مفتوحة وشارات حالة (متأخر، بلا رد، مستحق) فوق السجل.
- 21-28 ث: الخطوة 04: شريط التبويبات والفلاتر يتحول إلى مخطط مع قياسات؛ ثم يندمج في «خط زمني» واحد بفلتر علاقة يجمع الرسائل والملاحظات وتغييرات الصفقة.
- 28-35 ث: الخطوة 05: المخطط يُظهر العمود ينزاح يساراً؛ ولوحة رد جانبية تنزلق من اليمين بالرسالة الواردة ومرفق ورد مقترح بزر إرسال.
- 35-42 ث: الصفحة النهائية تثبت بألوانها الكاملة، ثم تبتعد الكاميرا بلطف وتستقر.

## Proposed scenes
- 0-7s: The original record page (sidebar, company header with six equal buttons, long details column, activity tabs) sits on off-white; it fades to a blueprint with a bracket around the button row, and caption 01 states the problem; the row collapses to one primary button plus a menu.
- 7-14s: Step 02: the details column turns blueprint, its many empty rows outlined and counted; the column collapses into a compact summary line under the company name, and the caption's follow-up appears in cyan.
- 14-21s: Step 03: the activity list is X-rayed with a highlighted overdue reminder row; a 'Needs you' card with three open tasks and status chips (overdue, unanswered, due) is inserted above the feed.
- 21-28s: Step 04: the tab strip and filters are blueprinted and measured; they merge into a single 'Timeline' with a relationship filter showing emails, notes and deal changes together.
- 28-35s: Step 05: blueprint shows the column shifting left; a reply side panel slides in on the right with the incoming email, an attachment and a drafted answer with a send button.
- 35-42s: The final page holds in full colour, then gently pulls back and settles.

## قواعد الحركة
- إيقاع ثلاثي لكل خطوة: الواجهة الحقيقية (نحو ثانيتين)، تلاشٍ متقاطع في نحو 600 مللي ثانية إلى المخطط (نحو 2.5 ثانية)، ثم تلاشٍ إلى الواجهة المصلحة (نحو 2.5 ثانية).
- شكل المخطط: العناصر تصبح حدوداً سماوية #49b6d6 بتعبئة سماوية 15% وخطوط إرشاد متقطعة وأقواس زوايا ووسوم قياس صغيرة بخط أحادي بأحرف كبيرة؛ وباقي الصفحة يخفت إلى 20%.
- اللوحة: صفحة #f5f5f3، بطاقات #ffffff، حبر #121212، رمادي #8e8e8e، خطوط رفيعة #e4e4e4، سماوي #49b6d6، أحمر الحالة #e5484d، كهرماني #d9822b، شارة خضراء #2fb56a.
- التعليقات أسفل اليسار: رقم خطوة صغير وتسمية بأحرف كبيرة، ثم جملة بسيطة واحدة؛ وجملة الحل تظهر بعدها بالسماوي.
- تغييرات التخطيط تتحرك كإعادة تدفق حقيقية: الصفوف تنكمش بتسارع في الارتفاع (نحو 400 مللي ثانية)، البطاقات الجديدة تنزلق 8 بكسل للأسفل مع ظهور، واللوحة الجانبية تنزلق من اليمين.
- بلا قطعات وبلا حركة كاميرا حتى ابتعاد لطيف أخير بنحو 3%.
- الخط: خط واجهة محايد بأحجام صغيرة، مطابق لتطبيق حقيقي.

## Motion rules
- Three-state rhythm per step: real UI (about 2 s), cross-fade over about 600 ms to blueprint (about 2.5 s), then cross-fade to the fixed UI (about 2.5 s).
- Blueprint look: elements become cyan #49b6d6 outlines with 15% cyan fills, dashed guide lines, corner brackets and tiny uppercase mono measurement tags; the rest of the page fades to 20%.
- Palette: page #f5f5f3, cards #ffffff, ink #121212, grey #8e8e8e, hairlines #e4e4e4, cyan #49b6d6, status red #e5484d, amber #d9822b, green chip #2fb56a.
- Captions sit bottom-left: a tiny step number and uppercase label, then one plain sentence; the resolution sentence fades in after it in cyan.
- Layout changes animate as real reflow: rows collapse with height easing (about 400 ms), new cards slide down from 8 px with fade, the side panel slides in from the right.
- No cuts and no camera moves until the final gentle 3% pull-back.
- Type: neutral UI sans at small sizes, matching a real SaaS app.

## Facts stated by the source (rewritten in our words)
- The animation explains UX decisions made on a CRM company record page.
- It is listed as made with Opus 5.5.
- Tagged diagrams.

## Assumptions
Observed from 24 frames sampled every ~1.75 s over 42 s: the original page, the cyan blueprint states, the five numbered principles with captions and the final page with reply panel; no hard cuts were detected. The file has a soundtrack whose content was not analysed. The capture is 1280x960 (4:3) although the record says 16:9, so the aspect is set to 4:3; step timings are estimated between samples.

## Keywords
ux explainer, ui redesign, blueprint, wireframe, crm, design principles, before after, saas, شرح تجربة المستخدم, إعادة تصميم, مخطط هندسي, قبل وبعد, مبادئ التصميم, واجهة
