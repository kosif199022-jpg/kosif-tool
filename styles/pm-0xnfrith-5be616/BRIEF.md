# شرح ملكية المهام بين الأجهزة بأسلوب بطاقات ملونة جريئة — Celld job ownership explainer

> فيلم شرح تقني صامت مدته نحو 53 ثانية بأسلوب «نيو بروتاليزم» على خلفية كريمية: بطاقات مسطحة بحدود سوداء سميكة وظلال مصمتة بالوردي والسماوي والأخضر الفاتح والأصفر، تحكي مشكلة مؤقت على جهاز واحد يتعطل، ثم جهازين يطلقان الأمر مرتين، ثم الحل: دلو تخزين مشترك أصفر فيه «ورقة ملكية» يكتب فيها أول جهاز اسمه، وعقود إيجار بأشرطة عد تنازلي، وجهاز يستلم المهمة حين ينتهي عقد المالك، وختام بجدول مقارنة بين خيارين.
>
> A silent ~53-second neo-brutalist tech explainer on cream: thick-bordered pink, cyan, mint and yellow cards show a single timer machine dying, two machines firing twice, then a shared yellow bucket with an ownership sheet, lease countdown bars, a backup machine taking over, the old owner stopping itself, and a two-option comparison table.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/0xnfrith-5be616
- التصنيفات / Categories: diagrams
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 53 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: Remotion, React, SVG, CSS

## الفكرة
الفكرة شرح مفهوم أنظمة موزعة (من يملك المهمة المجدولة) بلغة بصرية مرحة وواضحة: كل جهاز بطاقة بحرف كبير (A، B، C) ولون خاص، والقناة التي تستقبل الرسائل لوحة ثابتة على اليمين، والدلو المشترك هو «الحكَم». القصة مسألة وحلها: لماذا يفشل الحل البسيط، ولماذا يفشل الحل المضاعف، وكيف يحل قفل الملكية مع عقد الإيجار المشكلتين معاً. العناوين أسئلة وأجوبة قصيرة بأحرف كبيرة ثقيلة.

## Concept
The idea is to explain a distributed-systems concept (who owns the scheduled job) in a playful, clear visual language: each machine is a card with a big letter (A, B, C) and its own colour, the channel receiving messages is a fixed panel on the right, and the shared bucket is the 'referee'. The story is a problem and its solution: why the simple setup fails, why the doubled setup fails, and how an ownership lock with a lease solves both. Headlines are short questions and answers in heavy uppercase.

## المشاهد المقترحة
- 0-6 ث: بطاقة جهاز واحد (وردية) تعرض مؤقتاً كبيراً؛ يطلق الأمر في 8:00 فتظهر علامة صح في لوحة القناة؛ ثم تصبح البطاقة رمادية بتظليل مائل وملصق «DOWN»، وتبقى خانة 20:00 في القناة فارغة وملاحظة تقول إن أحداً لم يُبلَّغ.
- 6-12 ث: الخلفية تتحول إلى الأخضر: بطاقتا جهازين تطلق كل منهما 8:00؛ وسم «أُرسل مرتين» يركب خطاً منحنياً إلى القناة حيث يُحاط سطران متطابقان بدائرة مرسومة باليد.
- 12-17 ث: عودة إلى الكريمي: العنوان يقدم الأداة كحَكَم واحد لعدة أجهزة؛ دلو أصفر كبير يسقط، والأجهزة A وB وC تتصل به بخطوط، وتظهر ورقة فيها سطر مالك فارغ، وملاحظة تقول إن الدلو تخزين مشترك.
- 17-24 ث: الخطوة 1، احجز المهمة: بطاقة قاعدة تقول اكتب اسمك فقط إن كان السطر فارغاً؛ حرف A يطير إلى سطر المالك، وحرفا B وC يرتدان بوسم «مرفوض» ويظهر ختم «فائز واحد».
- 24-30 ث: الخطوة 2، جدّد أو اخسر: أشرطة عقود A وB وC تمتلئ وتفرغ مع تجديد كل جهاز كل بضع ثوانٍ؛ وملاحظة تشرح أن العقد يدوم 10 ثوانٍ؛ ويطلق A أمر 8:00 في القناة.
- 30-39 ث: المالك يتعطل: يصبح A رمادياً بملصق DOWN، ويفرغ شريط عقده إلى 0 ثانية مع وسم «منتهٍ»؛ فيحجز B الورقة ويصبح المالك ويطلق 20:00 في القناة.
- 39-46 ث: ماذا لو عاد A؟ تعود بطاقته وعليها 20:00، يتحقق من الورقة فيحصل على وسم «ليست لك» ويوقف نفسه؛ وملاحظة تقول بلا عقد لا إرسال، فلا يمكن أن يتكرر الأمر.
- 46-53 ث: المقارنة: بطاقتا خيارين (جهاز واحد بمؤقت مقابل الأداة على جهازين أو ثلاثة) تمتلئ صفوفهما بعلامات صح خضراء وعلامة خطأ حمراء، وتنبثق ملصقات «بسيط» و«موثوق»، ويلخص العنوان الأخير: عدة أجهزة رخيصة، مؤقت واحد، ولا تكرار أبداً.

## Proposed scenes
- 0-6s: One machine card (pink) shows a big countdown timer; it fires at 8:00 and a tick lands in the channel panel; then the card turns grey with diagonal hatching and a 'DOWN' sticker, the 20:00 slot in the channel stays empty and a note says nobody is told.
- 6-12s: Ground flips to green: two machine cards each fire 8:00; a 'sent twice' tag rides a curved line into the channel where two identical rows are circled with a hand-drawn ellipse.
- 12-17s: Back to cream: headline names the tool as one referee for many machines; a big yellow bucket drops in, machines A, B, C connect by lines, a sheet with a blank owner line appears and a note says the bucket is shared storage.
- 17-24s: Step 1, claim the job: a rule card says write your name only if the line is blank; A's letter tile flies into the owner line, B and C tiles bounce off with 'rejected' tags and a 'one winner' stamp appears.
- 24-30s: Step 2, check in or lose it: lease bars for A, B, C fill and drain as each machine renews every few seconds; a note explains a lease lasts 10 s; A fires 8:00 into the channel.
- 30-39s: The owner dies: A goes grey and DOWN, its lease bar drains to 0 s and gets an 'expired' tag; B claims the sheet, becomes owner and fires 20:00 into the channel.
- 39-46s: What if A wakes back up: A's card returns showing 20:00, checks the sheet, gets a 'not yours' tag, and stops itself; a note says no lease means no sending, so it cannot double-fire.
- 46-53s: Comparison: two option cards (one VM plus a timer versus the tool on 2-3 VMs) fill rows with green ticks and a red cross, 'simple' and 'reliable' stickers pop, and the final headline sums up: several cheap machines, one timer, never twice.

## قواعد الحركة
- بطاقات «نيو بروتاليزم»: تعبئة مسطحة، حدود سوداء #111111 بسمك 3 بكسل، ظلال مزاحة 6-8 بكسل بلا تمويه، ووسوم ملصقات مائلة قليلاً.
- اللوحة: خلفية كريمية #fbf8ec، وردي #f07ad8، سماوي #a8eef5، أخضر نعناعي #a6f08e، أصفر الدلو #f2c84b، خلفية خضراء لمشهد المشكلة #9be27a، رمادي #9a9a9a للأجهزة المتعطلة، وأحمر #e0453a لعلامات الخطأ.
- كل جهاز يحتفظ بلونه وحرفه طوال الفيلم؛ ولوحة القناة ثابتة على اليمين كلوحة نتائج لما أُطلق فعلاً.
- الخط: عناوين غروتسك مكثف ثقيل بأحرف كبيرة أعلى اليسار (مع كلمة مبرزة على وسم أصفر)، وسوم صغيرة بخط أحادي المسافة على البطاقات، وعنوان يُكتب بمؤشر.
- مفردات الحركة: البطاقات تنزلق وتستقر بتجاوز بسيط (نحو 250 مللي ثانية)، الملصقات تنبثق بحجم من 0 إلى 1.1 إلى 1، الحروف تطير في أقواس إلى خاناتها، والمرفوضة ترتد مع اهتزاز.
- أشرطة العقود تمتلئ وتفرغ خطياً بوسم 10 ثوانٍ؛ وانتهاء العقد يجعل الشريط يومض ويختمه بوسم «منتهٍ».
- زخارف: ملصقات نجمية تدور في الزوايا، وشرائح بخطوط تحذير مائلة؛ والانتقالات بين النبضات انزلاقات سريعة أو تقلب لون الخلفية، ولا تلاشي إلى الأسود.

## Motion rules
- Neo-brutalist cards: flat fills, 3 px black #111111 borders, hard 6-8 px offset shadows with no blur, slightly rotated sticker labels.
- Palette: cream #fbf8ec ground, pink #f07ad8, cyan #a8eef5, mint #a6f08e, bucket yellow #f2c84b, problem green ground #9be27a, grey #9a9a9a for dead machines, red #e0453a for crosses.
- Each machine keeps its colour and letter throughout; the channel panel stays fixed on the right as the scoreboard of what actually fired.
- Type: heavy condensed uppercase grotesk headlines top-left (a word highlighted on a yellow tag), small monospace labels on cards, a typed-on headline with a caret.
- Motion vocabulary: cards slide and settle with a small overshoot (about 250 ms), stickers pop with scale 0 to 1.1 to 1, tiles fly along arcs into slots, rejected tiles bounce back with a shake.
- Lease bars fill and drain linearly with a 10 s label; expiry flashes the bar and stamps an 'expired' pill.
- Decorative bits: spinning starburst stickers in corners, diagonal hazard-stripe chips; transitions between beats are quick slides or ground-colour flips, never fades to black.

## Facts stated by the source (rewritten in our words)
- It explains how the Celld tool handles job ownership.
- The source tags it under diagrams.

## Assumptions
Observed from 24 frames sampled every ~2.2 s over 53 s: the dying single timer, the double-fire problem, the shared bucket and ownership sheet, the claim step, the leases, the failover, the woken machine stopping itself and the comparison table. The audio track is digitally silent (about -91 dB). Exact animation timings and hex values are estimates from stills.

## Keywords
tech explainer, neo brutalism, distributed systems, leader election, lease lock, cron job, card diagram, failover, شرح تقني, نيو بروتاليزم, أنظمة موزعة, قفل الملكية, مهام مجدولة, مخطط بطاقات
