# ريل عرض القدرات: فصول الحركة الأربعة — Motion design showreel

> ريل 20 ثانية يستعرض أربعة فصول متتابعة (الخط، البيانات، الشكل، الإيقاع) بخيط طباعي واحد يربطها دون قطع.
>
> A 20s range reel in four chapters (type, data, form, rhythm) tied together by one typographic thread and zero hard cuts.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/samuel-spitz-974923
- التصنيفات / Categories: charts, kinetic-type
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 20 s · الصعوبة / Difficulty: 4/5
- التقنية المقترحة / Stack: Remotion, React, SVG

## الفكرة
ريل أعمال يجمع أربعة تخصصات (الطباعة الحركية، تصوير البيانات، الشكل، الإيقاع) في فيلم واحد متصل بلا قطع صريح حتى الفصل الأخير. الهدف إقناع المشاهد خلال عشرين ثانية بأن المصمم يتقن المجال كله لا جزءاً منه. ما يميز لغة الحركة أن كل فصل يولد من عنصر الفصل السابق: خط الأساس يصبح سكة كاميرا، والحروف تتحول إلى أعمدة بيانية، ومحيط المخطط ينتفخ ليصبح شكلاً.

## Concept
A portfolio reel that gathers four disciplines (kinetic type, data visualisation, form, rhythm) into one continuous film with no hard cut until the last chapter. The goal is to convince a viewer in twenty seconds that the designer commands the whole field, not a corner of it. The motion language is distinctive because each chapter is born from an element of the previous one: the baseline becomes a camera rail, letters become bars, a chart outline inflates into a shape.

## المشاهد المقترحة
- 0-3ث: عنوان افتتاحي: كلمة لكل تخصص تصعد حرفاً حرفاً، ثم تستقر الحروف على خط أساس واحد يتحول إلى سكة تقود الكاميرا نحو الفصل الأول.
- 3-7ث: فصل الخط: عبارة رئيسية تنقسم إلى ثلاثة أوزان (رفيع، عادي، ثقيل) تنزلق فوق بعضها بسرعات مختلفة؛ كلمة واحدة تنقلب إلى العربية ثم تعود لإثبات التعامل الثنائي اللغة.
- 7-11ث: فصل البيانات: حروف العبارة تنهار لتصبح أعمدة؛ المخطط يعد قيمه صعوداً، ثم تتصل قمم الأعمدة بخط بياني يمتد إلى مساحة مظللة، وتسمية توضيحية تتبع الذروة.
- 11-14ث: فصل الشكل: محيط المساحة البيانية ينتفخ إلى كتلة مستديرة تتقسم إلى شبكة بلاطات تدور ثلاثي الأبعاد لتكشف شعاراً.
- 14-18ث: فصل الإيقاع: قطعات حادة على النبض: ثلاث ضربات لونية تملأ الإطار، كل واحدة تحمل رقماً (سنوات، مشاريع، عملاء) مع عداد.
- 18-20ث: الخاتمة: كل العناصر تنطوي عائدة إلى خط الأساس الافتتاحي؛ الاسم والدور يثبتان 1.2 ثانية أخيرة مع تنفس خفيف في المقياس.

## Proposed scenes
- 0-3s: Opening title: one word per discipline rises letter by letter; the letters settle onto a single baseline, and that baseline becomes a camera rail that carries us into chapter one.
- 3-7s: TYPE chapter: a headline phrase splits into three weights (thin, regular, black) that slide past each other at different speeds; one word flips to Arabic and back to prove bilingual handling.
- 7-11s: DATA chapter: the headline letters collapse into bars; the bar chart counts up to its values, the bar tops connect into a line that extrudes into an area, and a callout label tracks the peak.
- 11-14s: FORM chapter: the area outline inflates into a rounded blob; the blob subdivides into a grid of tiles that rotate in 3D to reveal a logo mark.
- 14-18s: RHYTHM chapter: hard-synced beat edits: three full-frame colour slams, each carrying one number (years, projects, clients) with a counter.
- 18-20s: Close: every element folds back into the baseline from the intro; name and role sit still for the final 1.2s with a subtle breathing scale.

## قواعد الحركة
- منحنى الحركة الرئيسي للمواضع: cubic-bezier(0.16, 1, 0.3, 1) خلال 600-800ms؛ يُمنع المنحنى الخطي لأي عنصر تتابعه العين.
- الانتقال بين الفصول تحوّل لا قطع: عنصر من الفصل المنتهي يصبح أول عنصر في الفصل التالي (خط الأساس إلى سكة، الحروف إلى أعمدة، المحيط إلى كتلة). القطع الحاد مسموح داخل فصل الإيقاع فقط.
- الكاميرا: كاميرا افتراضية واحدة متصلة؛ التحريك الأفقي بنفس منحنى العناصر، والتقريب محصور بين 1.0 و1.35x؛ لا اهتزاز للكاميرا في أي موضع.
- الطباعة: تدرج دخول الحروف 30-40ms؛ الكلمات تدخل من 24px أسفل موضعها مع ضبابية 4px تزول خلال 180ms؛ لا دوران للحروف خارج فصل الخط.
- المخططات: الأعمدة تنمو من الصفر بنابض 500ms (stiffness 170, damping 22)؛ العدادات الرقمية تستخدم ease-out خلال 900ms وتثبت على العدد الصحيح النهائي.
- اللون (مقترح): أساس داكن محايد، ومحايد فاتح للنصوص، ولون مشبع واحد لا يتجاوز 10% من أي إطار؛ ضربات فصل الإيقاع يجوز أن تعكس الأساس واللون المشبع لإطار واحد فقط.
- ممنوع: وهج العدسة الجاهز، ظلال أعرض من 8px، قصاصات الاحتفال، أكثر من خطين، وأي عنصر ينجرف بلا غاية.

## Motion rules
- Master easing for position moves: cubic-bezier(0.16, 1, 0.3, 1) over 600-800ms; never linear for anything the eye tracks.
- Chapter transitions are morphs, not cuts: an element of the outgoing chapter becomes the first element of the incoming one (baseline to rail, letters to bars, outline to blob). Hard cuts are allowed only inside the RHYTHM chapter.
- Camera: one continuous virtual camera; pans travel on the same easing as elements, zoom limited to 1.0-1.35x; no camera shake anywhere.
- Typography: letter stagger 30-40ms; words enter from 24px below with a 4px blur that clears in 180ms; no per-letter rotation outside the TYPE chapter.
- Charts: bars grow from zero on a 500ms spring (stiffness 170, damping 22); value counters use ease-out over 900ms and snap to the final integer.
- Colour (proposed): one dark neutral base, one light neutral for type, one saturated accent covering no more than 10% of any frame; the RHYTHM slams may invert base and accent for exactly one frame each.
- Banned: stock lens flares, drop shadows wider than 8px, confetti particles, more than two typefaces, any element drifting without purpose.

## Facts stated by the source (rewritten in our words)
- The creator asked for a piece that could anchor a top-tier designer's demo reel and double as a visual CV.
- The instruction was to demonstrate the widest possible range of skills and push execution quality to the limit.
- Tagged on the source page as charts and kinetic type; frame size listed as 1920x1080.

## Assumptions
The four-chapter structure, the 20s runtime, the palette and every timing are my proposal; the source gives no duration, colours or scene list.

## Keywords
showreel, ريل أعمال, portfolio reel, عرض مهارات, kinetic typography, طباعة حركية, bar chart morph, مخطط بياني, chapter transitions, انتقالات متصلة, designer résumé, remotion reel, 1080p
