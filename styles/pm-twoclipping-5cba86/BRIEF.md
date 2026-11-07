# شكل واحد يتحول عبر حالات الواجهة: من زر إلى مشغل إلى رسم بياني — Shape morphing through UI states

> حلقة مربعة مدتها 14 ثانية على رمادي فاتح دافئ: عنصر أسود واحد مستدير يتحول بلا قطع من زر «توليد» إلى مؤشر تحميل دائري ثم كبسولة ثم بطاقة مشغل موسيقى بغلاف متدرج، ثم شريط صوت، ثم مفتاح تبديل، ثم مبدّل أيام وأسابيع وأشهر، ثم بطاقة رسم بياني بيضاء بعداد ومنحنى، ثم لوحة أوامر يُكتب فيها، ثم إشعار، ويعود زراً كما بدأ، ومؤشر فأرة يقود كل تحول بنقرة.
>
> A 14-second square loop on warm light grey: one rounded black element morphs without cuts from a Generate button into a spinner, a music-player card with a gradient cover, a volume bar, a toggle, a Day/Week/Month switch, a white chart card, a command palette that types, a toast, and back to the button, a cursor clicking each change.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/twoclipping-5cba86
- التصنيفات / Categories: product-ui, shapes, charts
- النسبة المقترحة / Aspect: 1:1 · المدة / Duration: 14 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: React, CSS, HTML Canvas, Remotion

## الفكرة
الفكرة أن الواجهة كائن حي واحد لا شاشات منفصلة: كل نقرة تعيد تشكيل نفس الكتلة إلى المكوّن التالي، فيتغير نصف القطر والعرض والارتفاع واللون بانسيابية بينما يتلاشى المحتوى القديم بضبابية ويظهر الجديد. الأسلوب مونوكروم صارم (أسود، أبيض، رمادي) بلمسة لون واحدة في غلاف الأغنية، وظلال ناعمة، وخط سانس نظيف، فيبدو كعرض لمكتبة مكونات فاخرة.

## Concept
The idea is that the interface is one living object rather than separate screens: each click reshapes the same mass into the next component, so radius, width, height and colour change fluidly while the old content blurs out and the new content resolves. The style is strict monochrome (black, white, grey) with a single colour accent in the song cover, soft shadows and a clean sans, so it reads like a showcase for a premium component library.

## المشاهد المقترحة
- 0-1 ث: زر كبسولة أسود بنص أبيض على رمادي فاتح؛ المؤشر ينقر فتنكمش الكبسولة إلى دائرة سوداء ويدور بداخلها قوس تحميل رفيع.
- 1-2.3 ث: الدائرة تتمدد إلى كبسولة عريضة بمصغرة مربعة متدرجة وموجة صوت صغيرة، ثم تطول إلى بطاقة سوداء مستديرة: غلاف ملون (برتقالي إلى وردي إلى بنفسجي) وعنوان وسطر صغير.
- 2.3-3.6 ث: حالة المشغل: شريط تقدم بالزمن المنقضي والمتبقي وأيقونات السابق والإيقاف والتالي؛ المؤشر يسحب نقطة التقدم فيتحدث الزمن، ثم تتضبب البطاقة وهي تنضغط.
- 3.6-5 ث: البطاقة تصير كبسولة صوت رفيعة بأيقونة سماعة؛ المؤشر يسحب الامتلاء الأبيض من شبه الفراغ إلى الامتلاء وتكتسب الأيقونة موجات صوت.
- 5-6.2 ث: تنكمش إلى مفتاح تبديل: مقبض أبيض ينقره المؤشر، والمسار يتلاشى من الرمادي الداكن إلى الفاتح.
- 6.2-7.3 ث: المفتاح يتسع إلى مبدّل أبيض (يوم، أسبوع، شهر) بكبسولة سوداء نشطة تنزلق بين الخيارات بضبابية حركة.
- 7.3-9.6 ث: المبدّل يكبر إلى بطاقة رسم بياني بيضاء: عداد كبير يتدحرج إلى إجمالي جديد، منحنى أسود ناعم بتعبئة رمادية خفيفة، نقطة مرور وتلميح داكن؛ وتبديل التبويب يعيد تشكيل المنحنى وينخفض العداد.
- 9.6-14 ث: البطاقة تتحول إلى لوحة أوامر: نص إرشادي وعناصر قائمة واستعلام يُكتب حرفاً حرفاً فيصفّي القائمة؛ ثم يطويها الإدخال إلى إشعار أسود بأيقونة حالة تتحول إلى علامة صح، ثم يعود الإشعار إلى زر «توليد» الأصلي لحلقة بلا فواصل.

## Proposed scenes
- 0-1s: A black pill button with white label on light grey; the cursor clicks, the pill shrinks into a black circle and a thin spinner arc rotates inside.
- 1-2.3s: The circle stretches into a wide pill with a gradient square thumbnail and a tiny waveform, then grows taller into a rounded black card: cover art (orange to pink to violet), title and a small subtitle.
- 2.3-3.6s: Player state: a progress bar with elapsed and remaining time, previous/pause/next icons; the cursor drags the scrubber and the times update, then the card blurs as it compresses.
- 3.6-5s: The card becomes a slim volume pill with a speaker icon; the cursor drags the white fill from almost empty to full and the icon gains sound waves.
- 5-6.2s: It shrinks into a toggle switch: a white knob that the cursor flicks, the track fading from dark grey to light grey.
- 6.2-7.3s: The switch widens into a white segmented control (Day, Week, Month) with a black active pill that slides between options with motion blur.
- 7.3-9.6s: The control grows into a white chart card: a big counter that rolls to a new total, a smooth black line with soft grey fill, a hover dot and dark tooltip; switching tab reshapes the line and the counter drops.
- 9.6-14s: The card turns into a command palette: placeholder, list items, a query typed letter by letter that filters the list; Enter collapses it into a black toast with a status icon that ticks to a check, which then reshapes back into the original Generate button for a seamless loop.

## قواعد الحركة
- شكل واحد مستمر: لا قطع أبداً؛ كل حالة هي نفس الحاوية تستكمل العرض والارتفاع ونصف قطر الزوايا والتعبئة (أسود #0a0a0a أو أبيض #ffffff) بنابض نحو 400-600 مللي ثانية مع تجاوز خفيف.
- تبديل المحتوى: المحتوى الخارج يتضبب (8-12 بكسل) ويتلاشى في نحو 150 مللي ثانية بينما يتضح المحتوى الداخل؛ والحاوية نفسها تكتسب ضبابية حركة لحظية عند تغيّر الحجم الكبير.
- الخلفية رمادي فاتح دافئ #ecebe8 بتظليل حواف خافت؛ وظلال طويلة ناعمة تحت الحاوية (أسود بشفافية 0.15 وضبابية 30-40 بكسل).
- لمسة لون واحدة: تدرج الغلاف #ff8a3d إلى #ff4f8b إلى #7b5cff؛ وكل ما عداه أسود وأبيض ورماديات #3a3a3a / #9a9a9a / #d8d8d8.
- مؤشر فأرة واقعي بأسلوب ماك يقود القصة: يتحرك على منحنيات متباطئة، وينقر بانضغاط صغير (0.96) ويسحب أشرطة التقدم والمنزلقات.
- الخط: غروتسك نظيف متوسط للتسميات، رقم كبير متقارب للعداد، وخط أحادي للأزمنة؛ تغيير حالة كل 1-1.5 ثانية تقريباً وحلقة كاملة عند 14 ثانية.

## Motion rules
- One continuous shape: never cut; every state is the same container interpolating width, height, border-radius and fill (black #0a0a0a or white #ffffff) with a spring of about 400-600 ms and slight overshoot.
- Content swap: outgoing content blurs (8-12 px) and fades in about 150 ms while incoming content un-blurs; the container itself briefly gains motion blur during big size changes.
- Background warm light grey #ecebe8 with a faint vignette; soft long shadows under the container (rgba 0,0,0,0.15, 30-40 px blur).
- Single colour accent: the cover art gradient #ff8a3d to #ff4f8b to #7b5cff; everything else black, white and greys #3a3a3a / #9a9a9a / #d8d8d8.
- A realistic macOS-style arrow cursor drives the story: it travels on eased curves, clicks with a small press scale (0.96) and drags scrubbers and sliders.
- Type: clean grotesk (Inter / SF style) medium for labels, a large tight numeral for the counter, mono for timestamps; about one state change per 1-1.5 s and a perfect loop at 14 s.

## Facts stated by the source (rewritten in our words)
- The piece shows a single shape morphing through a sequence of interface states.
- The listed technologies are CSS, Canvas and HTML; no duration is stated.

## Assumptions
Observed from 24 frames sampled every ~0.59 s over 14.06 s: the button, spinner, pill, player card, volume bar, toggle, segmented control, chart card, command palette and toast states, the driving cursor and the loop back to the button. Assumed: spring constants and exact timings between samples, hex values (estimated), and any sound (an audio stream exists but was not analysed). The current categories list nearly every key; product-ui, shapes and charts fit best.

## Keywords
shape morph, ui states, component showcase, music player, toggle switch, segmented control, chart card, command palette, seamless loop, تحول الأشكال, حالات الواجهة, مكونات واجهة, مشغل موسيقى, لوحة أوامر, حلقة متكررة
