# تفاعلات واجهة دقيقة: أزرار ومفاتيح وإشعارات بحركة متقنة — واجهات دقيقة

> ريل عمودي مقرّب جداً على عناصر واجهة تطبيق: زر يُضغط ويتحول إلى مؤشر تحميل ثم علامة صح، مفتاح تبديل ينزلق، إشعار ينزل بنابض، وأيقونة قلب تنفجر بجسيمات، على خلفية فاتحة نظيفة بظلال ناعمة.
>
> A vertical reel zoomed in close on app interface elements: a button presses, turns into a spinner and then a check mark, a toggle slides, a notification drops in on a spring, and a heart icon bursts into particles, all on a clean light background with soft shadows.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://github.com/kosif199022-jpg/kosif-one
- التصنيفات / Categories: product-ui
- النسبة المقترحة / Aspect: 9:16 · المدة / Duration: 25 s · الصعوبة / Difficulty: 2/5
- التقنية المقترحة / Stack: React, Remotion, CSS, SVG, Lottie

## الفكرة
كل مشهد يعرض تفاعلاً واحداً صغيراً بتفصيل كامل، كأننا نضع الواجهة تحت المجهر. القيمة في جودة التسهيل والنوابض والتوقيت، لا في كثرة الشاشات. يختلف عن «عرض SaaS» الذي يمشي في رحلة مستخدم كاملة عبر شاشات المنتج، وعن «واجهات زجاجية» التي تعتمد على الشفافية والتمويه والعمق، فهنا العناصر مسطحة نظيفة والكاميرا قريبة جداً.

## Concept
Each scene shows one small interaction in full detail, as if the interface were under a microscope. The value is in easing, springs and timing quality, not in many screens. It differs from saas-demo, which walks a whole user journey across product screens, and from glass-ui, which relies on translucency, blur and depth; here elements are flat and clean and the camera is very close.

## المشاهد المقترحة
- 0-2 ث: الافتتاح: مؤشر أو إصبع ضخم ينقر زراً؛ ينضغط إلى 0.94 مع موجة، ويتحول نصه بتلاشٍ إلى مؤشر تحميل.
- 2-6 ث: مؤشر التحميل يكتمل إلى علامة صح مرسومة (رسم خط في 12 إطاراً) ويتحول الزر إلى الأخضر.
- 6-11 ث: الكاميرا تنزلق إلى مفتاح تبديل؛ ينزلق بنابض ويمتلئ مساره باللون، ويظهر تلميح فوقه بشرح قصير.
- 11-16 ث: بطاقة إشعار تنزل من الأعلى بنابض مخمد، ثم تُسحب جانباً من اليمين إلى اليسار.
- 16-21 ث: نقر أيقونة قلب: ارتداد في الحجم وامتلاء باللون وحلقة من 8 جسيمات تنطلق.
- 21-25 ث: ابتعاد: كل المكونات تصطف في شبكة مرتبة تعرض مجموعة العناصر، ثم اسم المنتج.

## Proposed scenes
- 0-2s: Hook: a giant cursor or finger taps a button; it squashes to 0.94, ripples, and the label crossfades to a spinner.
- 2-6s: The spinner completes into a drawn check mark (stroke draw 12 frames) and the button turns green.
- 6-11s: Camera glides to a toggle; it slides with a spring, the track colour fills, and a tooltip pops above with a caption.
- 11-16s: A notification card drops from the top with a damped spring, then is swiped away right-to-left.
- 16-21s: A heart icon is tapped: scale bounce, colour fill, and a ring of 8 particles bursts out.
- 21-25s: Pull back: all components arrange into a tidy grid showing the component set, then the product name.

## قواعد الحركة
- الألوان: خلفية #f5f6fa، أسطح #ffffff بظل 0 12px 32px rgba(20,24,40,0.10)، رئيسي #4f46e5، نجاح #16a34a، خطر #ef4444، نص #111827 وخافت #6b7280.
- نوابض لا حركة خطية: صلابة نحو 300 وتخميد نحو 24 لحركات الواجهة؛ والضغط ينضغط إلى 0.94-0.96 في 4 إطارات ثم يعود بتجاوز طفيف.
- الكاميرا قريبة (العناصر تملأ 40-70% من العرض) وتنتقل بين المكونات بانزلاق 16-20 إطاراً؛ ولا قطع.
- كل تغيير حالة له سبب ونتيجة: نقرة أو مؤشر يسبقه دائماً بـ 3-6 إطارات.
- نصوص الواجهة العربية بخط واجهات نظيف (مثل IBM Plex Sans Arabic أو Noto Sans Arabic) بحجم 36-48 بكسل؛ والتصميم معكوس لاتجاه اليمين لليسار (المفاتيح تمتلئ من اليمين، السحب للإغلاق نحو اليسار، سهم الرجوع يشير لليمين).
- الأيقونات خطية بسمك 2 بكسل تتحول أو تُرسم بدلاً من أن تُستبدل فجأة.
- الشرح تحت كل مكون بنص خافت، 6 كلمات كحد أقصى.

## Motion rules
- Palette: background #f5f6fa, surfaces #ffffff with shadow 0 12px 32px rgba(20,24,40,0.10), primary #4f46e5, success #16a34a, danger #ef4444, text #111827 / muted #6b7280.
- Springs, not linear tweens: stiffness about 300, damping about 24 for UI moves; presses squash to 0.94-0.96 in 4 frames and release with a slight overshoot.
- Camera is close (elements fill 40-70% of width) and moves between components with 16-20 frame ease-in-out glides; no cuts.
- Every state change has cause and effect: a tap or cursor always precedes it by 3-6 frames.
- Arabic UI labels in a clean UI face (e.g. IBM Plex Sans Arabic or Noto Sans Arabic) 36-48 px; layouts mirrored for RTL (toggles fill right-to-left, swipes dismiss leftward, back arrows point right).
- Icons are 2 px stroke line icons that morph or draw on rather than swap.
- Captions explaining each interaction sit below the component in muted text, max 6 words.

## Facts stated by the source (rewritten in our words)
- KOSIF lists this as an original style named for micro interfaces, tagged product UI.

## Assumptions
Authored KOSIF definition, not an observed reference: the record points only to the repo root, so there was no video to watch. Palette hex values, fonts, timings and scene beats are design choices written for this style, not measurements.

## Keywords
micro interactions, ui animation, button, toggle, notification, spring, app ui, تفاعلات دقيقة, واجهة تطبيق, زر, إشعار, تحريك الواجهة, تصميم منتجات
