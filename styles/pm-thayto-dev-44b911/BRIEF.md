# ترويج خطة Pro لأداة ملاءمة السيرة الذاتية — AjustaCV Pro pricing promo

> فيلم ترويجي مدته 15 ثانية يظهر سيرة ذاتية تعيد تشكيل نفسها لتطابق وظيفة، ثم يكشف بطاقة تسعير الخطة الاحترافية.
>
> A 15-second promo where a résumé reshapes itself to fit a job posting, then the Pro pricing card lands as the payoff.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/thayto-dev-44b911
- التصنيفات / Categories: charts, kinetic-type
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 15 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: Remotion, React, CSS

## الفكرة
الموضوع أداة تعدل السيرة الذاتية لتلائم إعلان وظيفة محدداً، والفيلم ترويج لخطتها الاحترافية المدفوعة. الهدف إقناع المشاهد بالقيمة قبل عرض السعر: نرى المستند يتحسن أمام أعيننا ودرجة المطابقة ترتفع، ثم يأتي السعر كخلاصة منطقية. اللغة الحركية تعتمد على مستند حي: أسطر نصية تعيد ترتيب نفسها، كلمات مفتاحية تضيء عند مطابقتها، وشريط تقدم يتحول إلى رقم كبير قبل أن ينبسط إلى بطاقة تسعير.

## Concept
The subject is a tool that tailors a résumé to a specific job posting, and the film promotes its paid Pro tier. The goal is to prove value before showing price: the document visibly improves, the match score climbs, and the price arrives as the logical conclusion. The motion language is a living document: text lines reorder themselves, keywords light up as they match, and a progress bar becomes a big number before unfolding into a pricing card.

## المشاهد المقترحة
- 0-3 ث: تنزلق صفحة سيرة ذاتية عادية من الحافة السفلية وتدخل بطاقة إعلان وظيفة من اليمين؛ تستقر كلتاهما بتسهيل خروج 350 مللي ثانية ويُرسم خط رابط رفيع بينهما.
- 3-7 ث: تنبض الكلمات المفتاحية في الإعلان بلون التمييز واحدة تلو الأخرى (بفاصل 120 مللي ثانية)؛ تعيد الأسطر المطابقة في السيرة ترتيبها نحو الأعلى بزنبركات وتعيد كتابة نفسها بمسح آلة كاتبة.
- 7-10 ث: يمسح مقياس دائري لدرجة المطابقة من 41 إلى 92 بالمئة خلال 900 مللي ثانية بتسهيل خروج؛ يتدحرج الرقم صعوداً وتزداد سماكة الحلقة عند الاكتمال.
- 10-13 ث: يتسع المقياس إلى بطاقة تسعير الخطة الاحترافية: اسم الخطة في الأعلى، السعر مع وحدة شهرية، وأربعة صفوف مزايا تدفع بتدرج 80 مللي ثانية؛ تميل البطاقة درجتين نحو الكاميرا بلطف.
- 13-15 ث: ينقر المؤشر زر الترقية؛ يمتلئ الزر، تنكمش البطاقة إلى الشعار ويثبت سطر شعار واحد لآخر 700 مللي ثانية.

## Proposed scenes
- 0-3s: A plain résumé page slides up from the bottom edge and a job posting card slides in from the right; both settle with a 350 ms ease-out and a thin connector line draws between them.
- 3-7s: Keywords in the posting pulse in the accent colour one at a time (120 ms apart); matching lines in the résumé reorder upward on springs and rewrite themselves with a typewriter wipe.
- 7-10s: A circular match-score gauge sweeps from 41 to 92 percent in 900 ms with an ease-out; the number rolls up and the gauge ring thickens on completion.
- 10-13s: The gauge expands into the Pro pricing card: plan name at top, price with a per-month unit, and four benefit rows that push in on 80 ms staggers; the card gets a subtle 2-degree tilt toward the camera.
- 13-15s: A cursor clicks the upgrade button; the button fills, the card contracts to the logo and a one-line tagline holds for the last 700 ms.

## قواعد الحركة
- تعيد أسطر المستند ترتيبها بزنبرك (صلابة 160 وتخميد 20) ولا تتقاطع أبداً؛ تبدأ حركة كل سطر بعد 50 مللي ثانية من السابق.
- تمييز الكلمات المفتاحية تعبئة خلفية تمسح من اليسار إلى اليمين خلال 180 مللي ثانية؛ يتبدل لون النص عند منتصف المسح.
- مقياس الدرجة قوس واحد يحركه stroke-dashoffset بمنحنى cubic-bezier(0.22, 1, 0.36, 1) خلال 900 مللي ثانية؛ يستخدم الرقم المنحنى نفسه ليتفق الحلقة والعدد.
- دخول بطاقة التسعير: تكبير من 0.92 إلى 1 مع الشفافية خلال 300 مللي ثانية، تنزلق صفوف المزايا 16 بكسل لأعلى بتدرج 80 مللي ثانية؛ يهبط رقم السعر أخيراً ووحيداً.
- الكاميرا: ثابتة في مرحلة المستند، دفعة واحدة 5% على بطاقة التسعير، لا دوران.
- اللوحة: صفحة بيضاء، نص داكن، لون تمييز واحد للمطابقات والمقياس وزر الترقية؛ يمكن لبطاقة Pro استخدام سطح داكن معكوس لتتميز.
- ممنوع: قصاصات ورقية عند الترقية، وهج نابض حول السعر، أكثر من سعر واحد على الشاشة، نماذج مستندات ضبابية وصور وجوه جاهزة.

## Motion rules
- Document lines reorder with a spring (stiffness 160, damping 20) and never cross each other; each line's move starts 50 ms after the previous.
- Keyword highlights are a background fill that wipes left to right over 180 ms; text colour switches at the 50% mark of the wipe.
- The score gauge is a single arc driven by stroke-dashoffset with cubic-bezier(0.22, 1, 0.36, 1) over 900 ms; the numeral uses the same curve so ring and number agree.
- Pricing card entrance: scale from 0.92 to 1 with opacity in 300 ms, benefit rows slide 16 px up with 80 ms stagger; the price numeral lands last and alone.
- Camera: static for the document phase, one 5% push-in on the pricing card, no orbit.
- Palette: white page, dark text, one accent for matches, the gauge and the upgrade button; the Pro card may use a darker inverted surface to stand apart.
- Banned: confetti on upgrade, pulsing glow around the price, more than one price on screen, blurry document mockups and stock headshots.

## Facts stated by the source (rewritten in our words)
- The requested length is 15 seconds and the piece is framed as a portfolio-quality reel.
- The public title names a CV-tailoring product and its Pro pricing as the subject.
- Public tags are charts and kinetic type.

## Assumptions
The product's actual features and price are unknown; the job-matching flow, the 41-to-92 score and the four-benefit card are placeholders to be replaced with real product data. Scene order and palette are proposed.

## Keywords
pricing promo, resume builder, job match score, gauge animation, document reorder, keyword highlight, upgrade cta, saas pricing card, سيرة ذاتية, بطاقة تسعير, درجة مطابقة, ترقية الخطة, مستند حي, ترويج اشتراك
