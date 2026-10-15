# بولد بايلوت: تسلّق الترتيب إلى المركز الأول — Bold Pilot SEO promo

> برومو 15 ثانية لعلامة Bold Pilot يحوّل تحسين محركات البحث إلى رحلة طيران: صف نتيجة يتسلق من المركز 38 إلى الأول ومخطط زيارات يقلع.
>
> A 15-second Bold Pilot promo that turns SEO into a flight: a result row climbs from rank 38 to 1, a traffic curve takes off, and keyword chips dock in formation.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/utopyaszx-1b2f94
- التصنيفات / Categories: charts, kinetic-type
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 15 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: Remotion, React, SVG

## الفكرة
الموضوع برومو قصير لعلامة Bold Pilot، وهي حسب عنوان الصفحة خدمة في مجال تحسين محركات البحث، مصاغ كأنه عرض مهارات لمصمم الحركة نفسه. الهدف أن يفهم المشاهد خلال ثوانٍ أن الخدمة ترفع الترتيب وتزيد الزيارات، وأن يرى في الوقت ذاته إتقاناً في التنفيذ. لغة الحركة تستعير استعارة الطيار: السهم الذي يمثل العلامة يصعد كطائرة تترك أثراً خلفها، والمخططات تُقرأ كعدادات ارتفاع، والقطع يتبع تسارعاً تصاعدياً لا يهدأ حتى اللوغو.

## Concept
The subject is a short promo for Bold Pilot, which the page title frames as an SEO service, written as if it were also the designer's own skills showcase. The goal is for a viewer to grasp within seconds that the service lifts rankings and traffic, while seeing craft in the execution. The motion language borrows the pilot metaphor: the brand's arrow glyph climbs like an aircraft leaving a contrail, charts read like altitude gauges, and the editing accelerates upward without pausing until the logo.

## المشاهد المقترحة
- 0-1 ث: حقل بحث يستقر في منتصف الإطار (260ms ease-out)، المؤشر يومض مرة، واستعلام من 12 حرفاً يُكتب بمعدل 50ms للحرف.
- 1-4 ث: قائمة نتائج تتراكم؛ صف العلامة يبدأ في المركز 38، والصفوف التي فوقه تنطوي واحداً تلو الآخر (80ms لكل صف) بينما يصعد، وشارة الترتيب تعد تنازلياً من 38 إلى 1 مع تجاوز بسيط لإطارين في النهاية.
- 4-8 ث: مخطط الزيارات: منحنى مساحي يُرسم من اليسار إلى اليمين خلال 1.8 ثانية بينما يركب رمز سهم على هيئة طائرة الخط تاركاً أثراً يتلاشى؛ أرقام المحور الرأسي تتصاعد بأرقام جدولية.
- 8-11.5 ث: ستة إلى ثمانية رقائق كلمات مفتاحية تطير من حواف الإطار وترسو في تشكيل من صفين (spring)، وتضيء رقاقة كل 300ms؛ ثلاثة أفعال (مقترح: Rank / Grow / Fly) تندفع بمعدل 350ms لكل كلمة.
- 11.5-15 ث: رمز الطائرة يميل ليشكّل اللوغو، والشعار النصي يستقر تحته، ويثبت الإطار 1.2 ثانية.

## Proposed scenes
- 0-1s: A search field snaps into centre frame (260ms ease-out), the caret blinks once, and a 12-character query types at 50ms per character.
- 1-4s: A results list stacks in; the brand's row starts at position 38, rows above it collapse one by one (80ms each) as it climbs, and a position badge counts down 38 to 1 with a final 2-frame overshoot.
- 4-8s: Traffic chart: an area curve draws left to right over 1.8s while a small arrow-aircraft glyph rides the line leaving a thinning contrail; y-axis labels count up in tabular figures.
- 8-11.5s: Six to eight keyword chips fly in from the frame edges and dock into a 2-row formation (spring), one chip highlighting every 300ms; three verbs (proposed: Rank / Grow / Fly) punch in at 350ms each.
- 11.5-15s: The aircraft glyph banks into the logo lockup, the tagline settles underneath, and the frame holds for 1.2s.

## قواعد الحركة
- كل صعود (شارة الترتيب، منحنى الزيارات، الرقائق) يستخدم ease-out quint أي cubic-bezier(0.22, 1, 0.36, 1)؛ لا يُسمح لأي عنصر يمثل النمو بأن يتباطأ مبكراً.
- رقائق الكلمات المفتاحية تتحرك بنابض (stiffness 180، damping 14، mass 1) وتستقر خلال 600ms.
- خطوط المخططات تُرسم خلال 1800ms بمنحنى ease-in-out؛ موضع رمز الطائرة يُحسب من المسار نفسه كي لا يسبق الخط ولا يتأخر عنه.
- الكاميرا تنجرف للأعلى 2% على امتداد الثواني الخمس عشرة لتعزيز إحساس الارتفاع؛ لا تكبير سوى دفعة 3% عند اللوغو.
- اللوحة: لون أرضية عميق ولون تمييز واحد عالي الوضوح (مقترح)؛ يُحجز لون التمييز لصف العلامة والطائرة والتركيبة الختامية فقط.
- الأرقام بأرقام جدولية وتُعدّ بمنحنى ease-out خلال 900ms؛ شارة الترتيب تعد تنازلياً وكل ما عداها تصاعدياً.
- الخط: grotesque مضغوط بوزن 900 للأفعال، وgrotesque عادي لنصوص الواجهة؛ الأفعال تدخل بقفزة حجم 110% ثم تستقر خلال 150ms.
- ممنوع: علامات محركات البحث الحقيقية أو لقطاتها، الكرات الأرضية الدوارة، التوهج، وأي تلاشٍ متقاطع.

## Motion rules
- Every climb (rank badge, traffic curve, chips) uses ease-out quint cubic-bezier(0.22, 1, 0.36, 1); nothing that represents growth is allowed to decelerate early.
- Keyword chips use a spring (stiffness 180, damping 14, mass 1) and settle within 600ms.
- Chart strokes draw over 1800ms with ease-in-out; the aircraft glyph's position is sampled from the same path so it never leads or lags the line.
- Camera drifts upward 2% over the full 15s to carry the altitude feeling; no zooms other than a 3% push on the logo.
- Palette: a deep ground colour plus one high-visibility accent (proposed); the accent is reserved for the brand's row, the aircraft and the final lockup.
- Numbers are set in tabular figures and count with ease-out over 900ms; the rank badge counts down, everything else counts up.
- Type: one condensed grotesque at weight 900 for verbs, a regular grotesque for UI text; verbs enter with a 110% scale pop and 150ms settle.
- Banned: real search-engine branding or screenshots, spinning globes, glow effects, and any crossfade.

## Facts stated by the source (rewritten in our words)
- Length is fixed at 15 seconds.
- The piece is for a brand named Bold Pilot and should double as a showcase of the designer's ability.
- The page title labels it an SEO promo; tags are charts and kinetic type.

## Assumptions
That Bold Pilot is an SEO service comes from the page title, not the prompt body; the pilot/altitude metaphor, the rank-38 starting point, the palette and all timings are proposed. 1920x1080 is read as 16:9.

## Keywords
seo, تحسين محركات البحث, ترتيب البحث, ranking climb, traffic chart, keyword chips, مخطط زيارات, كلمات مفتاحية, brand promo, برومو علامة, contrail, search results animation, سهم طائرة
