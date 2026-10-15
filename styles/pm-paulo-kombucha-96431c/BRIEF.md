# إعلان برنامج الإحالة بالتميمة — Mascot referral program promo

> إعلان موشن جرافيك في 15 ثانية تقوده تميمة العلامة لشرح برنامج الإحالة: ادعُ صديقًا، يربح كلاكما، والرسم البياني يثبت ذلك.
>
> A 15-second mascot-led motion spot explaining a referral programme: invite a friend, both of you win, and a growing chart proves it.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/paulo-kombucha-96431c
- التصنيفات / Categories: charts
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 15 s · الصعوبة / Difficulty: 2/5
- التقنية المقترحة / Stack: Remotion, SVG, React

## الفكرة
الموضوع برنامج إحالة لعلامة مشروبات (يُفترض كومبوتشا من اسم الحساب) تُقدّمه تميمة كرتونية ودودة. الهدف أن يفهم المشاهد في 15 ثانية آلية بسيطة: تشارك رابطك، ينضم صديقك، ويحصل الطرفان على مكافأة، ثم يضغط زر المشاركة. تتميّز لغة الحركة بتميمة مرنة بحركة ضغط وتمدّد واضحة، ورمز رابط يُقذف كالكرة بين شخصيتين، ورسم أعمدة ينمو فعليًا كجزء من الحكاية لا كشريحة إحصائية منفصلة.

## Concept
The subject is a referral programme for a beverage brand (assumed kombucha from the handle) presented by a friendly cartoon mascot. The goal is that in 15 seconds the viewer grasps a simple mechanic: share your link, a friend joins, both sides get a reward, then taps share. The motion language is a rubbery mascot with pronounced squash and stretch, a link token tossed like a ball between two characters, and a bar chart that grows as part of the story rather than as a separate statistics slide.

## المشاهد المقترحة
- 0-2 ث: تقفز التميمة من الحافة السفلية بارتداد يتجاوز الهدف 15% وتلوّح؛ يهبط عنوان من سطرين، سطر على كل نبضة.
- 2-6 ث: ينزلق ظل صديق من اليمين؛ تقذف التميمة رمز رابط متوهّجًا يرسم قوسًا بأثر حركة ويستقر في يد الصديق التي تمتلئ باللون عند الالتقاط.
- 6-10 ث: رسم المكافآت: عمود باسم أنت وعمود باسم صديقك ينموان معًا خلال 700 مللي ثانية، ثم يُكدَّس عمود ثالث باسم معًا فوقهما بينما تتصاعد القيم.
- 10-13 ث: ورقة مشاركة بثلاثة أزرار (نسخ الرابط، رسالة، رمز QR) تتفتّح من يد التميمة بفواصل 60 درجة؛ ويتموّج كل زر عند الضغط.
- 13-15 ث: ترفع التميمة إبهامها، ويظهر رمز الإحالة في شارة تحت نداء الفعل، ويثبت لون العلامة آخر 800 مللي ثانية.

## Proposed scenes
- 0-2s: The mascot pops up from the bottom edge with a 15% overshoot bounce and waves; a two-line headline drops in, one line per beat.
- 2-6s: A friend silhouette slides in from the right; the mascot tosses a glowing link token that arcs across with a motion trail and lands in the friend's hand, which fills with colour on catch.
- 6-10s: Reward chart: a bar labelled 'you' and a bar labelled 'your friend' grow in sync over 700ms, then a third bar 'together' stacks above them while the amounts tick up.
- 10-13s: A share sheet with three buttons (copy link, message, QR code) fans out from the mascot's hand at 60-degree intervals; each button ripples when tapped.
- 13-15s: The mascot gives a thumbs-up, the referral code appears in a pill under the call to action, and the brand colour holds for the last 800ms.

## قواعد الحركة
- تتحرك التميمة بمنحنى cubic-bezier(0.34, 1.56, 0.64, 1) مع انضغاط إلى 80% من الارتفاع عند الهبوط وتمدّد إلى 115% عند الانطلاق؛ وتتبع الأطراف بتداخل 60 مللي ثانية.
- يسير رمز الرابط على مسار قطع مكافئ خلال 900 مللي ثانية مع أثر حركة من 12 عيّنة يتلاشى خلال 200 مللي ثانية؛ وهو العنصر الوحيد المسموح له بأثر.
- تنمو أعمدة الرسم من ارتفاع صفر بمنحنى ease-out cubic خلال 700 مللي ثانية؛ وتتصاعد الأرقام بالمنحنى نفسه وتستقر بعد العمود بـ 100 مللي ثانية؛ وتُرسم خطوط المحاور بـ stroke-dashoffset خلال 300 مللي ثانية.
- الكاميرا ثابتة؛ يأتي التأكيد من اقتراب 1.06 على نبضة الرسم فقط لمدة 200 مللي ثانية.
- الخط: sans ثقيل مستدير للعناوين، سطران كحدّ أقصى، 72 بكسل على 1080p؛ العربية بخط عريض مستدير مع دخول على مستوى الكلمة (translateY من 24 بكسل إلى 0 خلال 240 مللي ثانية بتأخير 60 مللي ثانية).
- اللون: لون العلامة الأساسي على التميمة والأزرار، وخلفية فاتحة محايدة، ولون مكافأة واحد يُستخدم فقط للرمز والأعمدة وشارة الكود.
- تحتفظ كل نبضة بعنصرها البصري الرئيسي ثانية واحدة على الأقل قبل بدء الفعل التالي؛ ولا يتداخل دخولان بأكثر من 100 مللي ثانية.
- ممنوع: مظهر التصيير ثلاثي الأبعاد، وظلال أعمق من 12 بكسل، وأكثر من ثلاثة أعمدة في الرسم، وأي نص قانوني صغير على الشاشة.

## Motion rules
- Mascot moves on cubic-bezier(0.34, 1.56, 0.64, 1) with squash to 80% height on landing and stretch to 115% at take-off; limbs follow with a 60ms overlap.
- The link token travels on a parabolic path over 900ms with a 12-sample motion trail that fades over 200ms; it is the only element allowed a trail.
- Chart bars grow from a 0 height with ease-out cubic over 700ms; numbers count up with the same curve and settle 100ms after the bar; axis lines draw on with stroke-dashoffset in 300ms.
- Camera is static; emphasis comes from a 1.06 punch-in on the chart beat only, lasting 200ms.
- Type: a rounded heavy sans for headlines, two lines max, 72px at 1080p; Arabic in a rounded bold face with word-level entrance (translateY 24px to 0, 240ms, 60ms stagger).
- Colour: brand primary on the mascot and buttons, a neutral light background, one reward accent used only for the token, the bars and the code pill.
- Each beat holds its key visual for at least 1s before the next action starts; no two entrances overlap by more than 100ms.
- Banned: 3D render looks, drop shadows deeper than 12px, more than three bars in the chart, and any legal small print on screen.

## Facts stated by the source (rewritten in our words)
- Fixed length of 15 seconds.
- The topic is the brand's referral programme and the tone should be dynamic.
- The creator filed it under charts, and the title names a mascot as the presenter.

## Assumptions
The source gives only the duration, the topic and the chart tag; the kombucha brand, the two-sided reward, the link-toss gag and the three-button share sheet are proposed. Reward amounts are placeholders to be replaced with the real programme terms.

## Keywords
referral program, mascot animation, invite a friend, bar chart, share sheet, reward, brand promo, برنامج إحالة, تميمة متحركة, ادعُ صديقًا, رسم بياني, مكافأة, مشاركة الرابط
