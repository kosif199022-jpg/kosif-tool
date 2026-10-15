# إطلاق مكتبة الأدلة المرئية: فيديو منتج SaaS — Visual guides library launch

> فيديو إطلاق 30 ثانية بأسلوب منشورات إطلاق المنتجات على X: واجهة حقيقية في إطار جهاز، بطاقات ميزات، ومخطط يقيس الفائدة.
>
> A 30s X-style SaaS launch film: real product UI in a device frame, three feature cards, a benefit chart and a clean CTA.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/techyoutbe-945b56
- التصنيفات / Categories: product-ui, charts, photos
- النسبة المقترحة / Aspect: 16:9 · المدة / Duration: 30 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: Remotion, React, SVG

## الفكرة
الموضوع إطلاق ميزة «مكتبة الأدلة المرئية» (أدلة خطوة بخطوة مبنية من لقطات شاشة) داخل منتج SaaS معروف. الهدف أن يفهم المشاهد خلال ثلاثين ثانية ما تفعله الميزة ويراها تعمل فعلاً، بالصقل المعتاد في فيديوهات إطلاق المنتجات المستقلة. ما يميز اللغة الحركية أن الواجهة هي البطل: الكاميرا تتجول داخل واجهة حقيقية بقيادة المؤشر مع تقريبات ماكرو على الأزرار، والادعاءات تظهر كتسميات قصيرة ملتصقة بأجزاء الواجهة لا كشرائح منفصلة.

## Concept
The subject is the launch of a 'visual guides library' feature (step-by-step guides built from screenshots) inside a well-known SaaS product. The goal is that a viewer understands in thirty seconds what the feature does and sees it working, with the polish typical of indie product-launch clips. The motion language makes the interface the hero: the camera travels inside a real UI led by the cursor, with macro push-ins on buttons, and claims appear as short labels attached to UI parts rather than as separate slides.

## المشاهد المقترحة
- 0-3ث: الخطاف: سطح مكتب مزدحم بلقطات شاشة وأسهم يهتز قليلاً، ثم ينطبق كل شيء في بطاقة واحدة مرتبة؛ شعار المنتج النصي يظهر تحتها.
- 3-9ث: كشف المنتج: لقطة لصفحة المكتبة داخل إطار متصفح تتسع من 0.92 إلى 1.0 بينما يكبر ظل ناعم؛ المؤشر يمر فوق بطاقة دليل والكاميرا تدفع إلى 1.4x.
- 9-18ث: ثلاث ميزات، 3 ثوانٍ لكل منها: تسجيل سير عمل (نقطة تسجيل تنبض والخطوات تظهر في قائمة)، لقطات شاشة تلقائية (إطارات تنزلق في كومة عمودية بشارات مرقمة)، مشاركة بنقرة (حبة رابط تُنسخ وإشعار يؤكد).
- 18-23ث: مخطط الفائدة: أعمدة أفقية تقارن دقائق كتابة الدليل قبل وبعد؛ عمود «بعد» ينمو أخيراً وتسمية تعد نسبة الوقت الموفر.
- 23-27ث: شريط آراء: ثلاث بطاقات اقتباس قصيرة تنزلق بانجراف أفقي بطيء؛ الصور الرمزية دوائر بديلة ما لم تتوفر صور مرخصة.
- 27-30ث: الدعوة للفعل: الشعار النصي، سطر وصفي واحد، الرابط؛ الخلفية ثابتة ولا يتحرك سوى المؤشر الذي ينقر زر التجربة فيمتلئ الزر عند الضغط.

## Proposed scenes
- 0-3s: Hook: a cluttered desktop of screenshots and arrows shakes slightly, then everything snaps into one tidy card; the product wordmark fades in beneath it.
- 3-9s: Product reveal: a browser-framed capture of the library home scales from 0.92 to 1.0 while a soft shadow grows; the cursor hovers a guide card and the camera pushes in to 1.4x.
- 9-18s: Three features, 3s each: capture a workflow (a recording dot pulses, steps appear in a list), auto-generated screenshots (frames slot into a vertical stack with numbered badges), one-click sharing (a link pill copies and a toast confirms).
- 18-23s: Benefit chart: a horizontal bar chart compares minutes spent writing a guide before and after; the 'after' bar grows last and a label counts the percentage saved.
- 23-27s: Social proof strip: three short quote cards slide in on a slow horizontal drift; avatars are placeholder circles unless licensed photos exist.
- 27-30s: CTA: wordmark, one-line tagline, URL; the background holds still and only the cursor moves, clicking a 'Try it' button that fills on press.

## قواعد الحركة
- لقطات الواجهة تُعاد بناؤها كمكونات برمجية أو تُؤخذ من لقطات مرخصة، ولا تُجلب أصول مجهولة الترخيص؛ اللقطات الحقيقية تُعرض داخل إطار جهاز SVG بدقتها الأصلية وتُكبر بالتحويل فقط.
- دفعات الكاميرا نحو الواجهة بمنحنى cubic-bezier(0.22, 1, 0.36, 1) خلال 900ms؛ أقصى تقريب 1.6x؛ كل دفعة يتبعها ثبات 300ms قبل الحركة التالية.
- المؤشر: سهم 24px يتحرك على منحنى بيزييه تربيعي خلال 350-450ms لكل رحلة، مع انضغاط نقرة إلى مقياس 0.9 لمدة 90ms؛ النقرات تقع على النبضات عند وجود موسيقى.
- تسميات الميزات: 2-4 كلمات ملتصقة بعنصر الواجهة الذي تصفه عبر خط دليل بسمك 1px يُرسم خلال 250ms؛ النص يظهر بعد اكتمال الخط بـ150ms.
- المخطط: الأعمدة تمتد خلال 700ms بمنحنى ease-out؛ عمود المقارنة ينتظر 400ms بعد الأول لإبراز الفرق؛ عداد النسبة يستمر 800ms وينتهي لحظة توقف العمود تماماً.
- الانتقال بين الميزات: انزلاق 20px للأعلى مع تلاشٍ متقاطع خلال 400ms؛ لا مسحات ولا انقلابات ثلاثية الأبعاد ولا كليشيه الغوص عبر الشاشة.
- اللون (مقترح): خلفية قريبة من الأبيض، لون العلامة على الأزرار وعمود «بعد» فقط، والنصوص بمحايد داكن؛ ظلال ناعمة (ضبابية 40px، عتامة 8%).
- ممنوع: ضبابية حركة على النصوص، انتقالات الصفير الجاهزة، أكثر من خط واحد خارج واجهة المنتج، ونص Lorem ipsum.

## Motion rules
- UI captures are rebuilt as code components or taken from licensed screenshots, never scraped assets of unclear licence; real screenshots sit inside an SVG device frame at native resolution and are scaled with transform only.
- Camera pushes into the UI use cubic-bezier(0.22, 1, 0.36, 1) over 900ms; max zoom 1.6x; every push is followed by a 300ms hold before the next move.
- Cursor: a 24px pointer travelling on a quadratic bezier, 350-450ms per trip, with a 90ms click squash to 0.9 scale; clicks land on beats wherever music exists.
- Feature labels: 2-4 words, attached to the UI element they describe by a 1px leader line that draws in 250ms; the label text fades in 150ms after the line completes.
- Chart: bars extend with a 700ms ease-out; the comparison bar waits 400ms after the first for contrast; the percentage counter runs 800ms and ends exactly when the bar stops.
- Transitions between features: a 20px upward slide with crossfade over 400ms; no wipes, no 3D flips, no zoom-through-the-screen cliche.
- Colour (proposed): near-white canvas, the product's brand colour on buttons and the 'after' bar only, text in a dark neutral; soft shadows (blur 40px, 8% opacity).
- Banned: motion blur on text, stock whoosh transitions, more than one typeface outside the product's own UI, Lorem ipsum placeholder copy.

## Facts stated by the source (rewritten in our words)
- The brief asks for a polished SaaS launch video modelled on the feature-and-benefit clips founders post on X when they ship something.
- The model was told to choose one widely recognised SaaS and source its real imagery from the web.
- The page title names the subject as a visual guides library launch; tags are product UI, charts and photos; frame 1920x1080.

## Assumptions
The 30s length, the three-feature structure, the comparison chart and the palette are my proposal; the specific SaaS is not named in the source, and I assume assets must be licensed or rebuilt as components rather than scraped.

## Keywords
saas launch, إطلاق منتج, product demo, عرض واجهة, feature video, device frame, cursor animation, مؤشر الماوس, benefit chart, مقارنة قبل وبعد, twitter launch video, ui showcase, شرح ميزات
