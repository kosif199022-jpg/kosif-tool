# شكل واحد يتحول عبر حالات الواجهة — Shape morphing through UI states

> عنصر واحد لا يُقطع أبدًا يتحول من زر إلى مشغّل إلى مخطط إلى لوحة أوامر على شبكة 120 BPM، ويقوده مؤشر يضغط ويسحب فعلًا.
>
> One never-cut element morphs from button to player to chart to command palette on a 120 BPM grid, driven by a cursor that really clicks and drags.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/twoclipping-5cba86
- التصنيفات / Categories: product-ui, charts, kinetic-type, shapes, particles, characters, photos, music, code
- النسبة المقترحة / Aspect: 1:1 · المدة / Duration: 14 s · الصعوبة / Difficulty: 5/5
- التقنية المقترحة / Stack: CSS, SVG, HTML Canvas

## الفكرة
الموضوع فيديو مربع لحركة واجهات بمستوى Dribbble: شكل واحد يمر بثماني إلى اثنتي عشرة حالة واجهة دون قطع، فيتغير حجمه ونصف قطره ولونه بينما يتبدل محتواه بضبابية قصيرة. الهدف إثبات إتقان حركة الواجهات الدقيقة، لا عرض قوالب. ما يميز اللغة الحركية أن كل قيمة دالة صرفة في الزمن عبر نوابض بصيغة مغلقة، وأن المؤشر هو الممثل الوحيد الذي يسبب كل تغيير، وأن الإطار الأخير مطابق للأول فتدور الحلقة بلا توقف.

## Concept
The subject is a square UI-motion film at Dribbble quality: one shape passes through eight to twelve interface states without a cut, changing size, radius and colour while its content swaps behind a short blur. The goal is to prove mastery of micro-interaction motion rather than show templates. The motion language is defined by closed-form springs that make every value a pure function of time, by a cursor that is the sole actor causing every change, and by a last frame identical to the first so the loop never stutters.

## المشاهد المقترحة
- 0-2 ث (المازورة 1): يضغط المؤشر زرًا بيضاويًا؛ ينكمش إلى حلقة دوّارة؛ وتنغلق الحلقة على علامة صح في الضربة الرابعة.
- 2-4 ث (المازورة 2): تتسع علامة الصح إلى كبسولة إشعار، ثم تكبر إلى مشغّل موسيقى مدمج يتحول فيه رمز التشغيل إلى إيقاف مؤقت عند النقر.
- 4-6 ث (المازورة 3): يسحب المؤشر شريط التقدم؛ ينبسط المشغّل إلى منزلق أفقي؛ السحب بعد النهاية يمدد المسار ويعود بنابض عند الإفلات.
- 6-8 ث (المازورة 4): ينكمش المنزلق إلى مفتاح تبديل ينقلب على الضربة؛ ويستطيل المقبض إلى إبراز سائل ينزلق بين ثلاثة تبويبات.
- 8-10 ث (المازورة 5): تتفتح التبويبات إلى مخطط خطي يرسم نفسه؛ يحوم المؤشر فيتبع تلميح أقرب نقطة.
- 10-14 ث (المازورتان 6-7): ينطوي المخطط إلى شريط أوامر؛ الحروف المكتوبة ترشّح الصفوف؛ الإدخال يطلق إشعارًا منبثقًا؛ ينكمش الإشعار إلى الزر الأصلي ويعود المؤشر إلى وضعه الأول.

## Proposed scenes
- 0-2s (bar 1): The cursor presses a pill button; it tightens into a spinning ring; the ring closes into a tick mark on beat 4.
- 2-4s (bar 2): The tick widens into a capsule notification, then grows into a compact music player whose play glyph morphs into pause on the click.
- 4-6s (bar 3): The cursor drags the progress; the player flattens into a horizontal slider; dragging past the end stretches the track and it springs back on release.
- 6-8s (bar 4): The slider shrinks into a switch that flips on the beat; the knob elongates into a liquid highlight sliding between three tabs.
- 8-10s (bar 5): The tabs unfold into a line chart that draws itself; the cursor hovers and a tooltip follows the nearest point.
- 10-14s (bars 6-7): The chart folds into a command bar; typed letters filter rows; enter fires a toast; the toast shrinks back into the original button and the cursor returns to its start pose.

## قواعد الحركة
- الشبكة: 120 BPM، ضربة كل 500 ms، و7 مازورات = 14 ث؛ يُطلق تغيير الحالة على كل ضربة ويجب أن يستقر بصريًا خلال 350 ms.
- النوابض: استجابات خطوة تحليلية بنسبة تخميد نحو 0.85 وتردد طبيعي نحو 18 rad/s، والتجاوز بحد أقصى 3 بالمئة؛ القيمة التي تغير هدفها عدة مرات هي مجموع نابض لكل تغيير حتى يكون كل إطار دالة صرفة في t.
- التحول: العرض والارتفاع ونصف قطر الزوايا واللون تتداخل على العنصر نفسه؛ يخرج المحتوى الداخلي بضبابية 6 px خلال 120 ms ويدخل الجديد بعد 60 ms دون تراكب.
- التمدد: الحافة الأمامية والخلفية لإبراز التبويب ولمقبض المفتاح تركبان نابضين منفصلين (نحو 22 و16 rad/s) حتى تسبق الحافة الأمامية.
- المؤشر: يتحرك بنابض إلى كل هدف ويصل قبل الضربة بـ 150 ms؛ النقرة ضغط 90 ms بتصغير 0.92؛ أثناء السحب تُحسب القيمة مباشرة من موضع المؤشر.
- الكاميرا: تقريب بحيث تملأ الحالة الحالية نحو 70 بالمئة من الكادر، على نابض 10 rad/s؛ لا دوران ولا قطع.
- اللوحة والخط: أرضية بيضاء دافئة مائلة للرمادي، عناصر شبه سوداء وبيضاء، لون مميز واحد على الأكثر، خط واجهات sans نظيف واحد؛ لا تدرجات على العناصر، لا توهج، والظلال بضبابية لا تتجاوز 24 px.
- الحلقة والممنوعات: الإطار 840 مطابق للإطار 0 بما فيه موضع المؤشر وسرعته؛ ممنوع التسهيل المرتد، الجسيمات، الخمول لأكثر من ضربة، تفاوت سماكة الأيقونات، وأي مكوّن جاهز.

## Motion rules
- Grid: 120 BPM, one beat every 500 ms, 7 bars = 14 s; a state change is triggered on every beat and must be visually settled within 350 ms.
- Springs: analytic step responses with damping ratio about 0.85 and natural frequency about 18 rad/s, overshoot at most 3 percent; a value that retargets several times is the sum of one spring per retarget so each frame is a pure function of t.
- Morphing: width, height, corner radius and colour interpolate on the same element; inner content exits with a 6 px blur over 120 ms and the new content enters 60 ms later, never overlapping.
- Stretch: the leading and trailing edges of the tab highlight and the switch knob ride separate springs (about 22 and 16 rad/s) so the leading edge pulls ahead.
- Cursor: spring-moved to each target, arriving 150 ms before the beat; click = 90 ms press at scale 0.92; drags compute the value directly from cursor position while held.
- Camera: zoom so the current state fills about 70 percent of the frame, on a 10 rad/s spring; no rotation, no cuts.
- Palette and type: warm off-white ground, near-black and white controls, at most one accent, a single clean UI sans; no gradients on controls, no glows, shadows at most 24 px blur.
- Loop and bans: frame 840 equals frame 0 including cursor position and velocity; banned are bounce easing, particles, idle stretches longer than a beat, mismatched icon strokes and any stock component.

## Facts stated by the source (rewritten in our words)
- Single HTML file on a square 1440 stage; every style is computed from time inside one seek function with no CSS transitions, timers or carried state.
- One element morphs through 8-12 interface states chosen with the user; a cursor causes every change with real clicks and drags; the camera zooms so each state fills the frame.
- Tempo 120 BPM over 7 bars with an event on every beat, analysed from a royalty-free song; the last frame equals the first for a loop.
- Springs are closed-form step responses; leading and trailing edges use different springs for stretch.
- Rendered with Playwright at 60 fps using four sub-frames blended in ffmpeg for motion blur; a one-frame-per-beat contact sheet is checked first.
- Palette is warm light grey with black and white components and optionally one accent; the UI font is Geist; banned are bouncy easing, particle bursts, glows, gradients on chrome, mismatched strokes, dead time and template looks.

## Assumptions
The exact state order per bar, the spring constants and the 70 percent framing are proposals; the source fixes the stage, tempo, bar count, pure-function rendering, loop rule and the bans. The 14 s duration is derived from 7 bars at 120 BPM.

## Keywords
ui motion, micro-interactions, morphing, springs, cursor driven, seamless loop, beat grid, حركة واجهات, تحول الأشكال, نوابض, حلقة متصلة, مؤشر, تفاعلات دقيقة, dribbble
