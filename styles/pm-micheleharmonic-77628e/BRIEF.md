# مونتاج أنمي حماسي عمودي لمنصة GravityDEX — GravityDEX anime hype edit

> مونتاج عمودي قصير بروح الأنمي يربط منصة تداول لامركزية بشخصية مقاتلة أصلية تتحكم بالجاذبية، بقطع على الإيقاع ولمسات glitch.
>
> A vertical anime-style hype edit that fuses a decentralised exchange with an original gravity-wielding fighter, cut hard to the beat with glitch accents.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://www.promptsmotion.com/micheleharmonic-77628e
- التصنيفات / Categories: —
- النسبة المقترحة / Aspect: 9:16 · المدة / Duration: 15 s · الصعوبة / Difficulty: 4/5
- التقنية المقترحة / Stack: Remotion, GSAP, HTML Canvas

## الفكرة
الموضوع منصة تداول لامركزية اسمها يحيل إلى الجاذبية، ويريد صاحب الطلب مونتاجًا يستلهم شخصية أنمي شهيرة قادرة على التحكم بالفراغ والجاذبية. بما أن تلك الشخصية ملكية فكرية لطرف ثالث، يعتمد هذا البريف شخصية أصلية بأسلوب الأنمي (ظل مقاتل بعصبة عين) تُرسم كخطوط وأشكال مسطّحة، وتُترجم فكرة الجاذبية إلى حركة: رموز العملات تُسحب إلى مدار حول الشعار، وخطوط الرسم البياني تنكسر وتنجذب نحو المركز. الهدف إثارة الحماس للمنصة في 15 ثانية بلغة حركة عنيفة الإيقاع: قطع على كل ضربة، دفعات تكبير سريعة، خطوط سرعة شعاعية، ولمعات بيضاء قصيرة جدًا.

## Concept
The subject is a decentralised exchange whose name evokes gravity, and the request is an edit inspired by a famous anime character who controls space and gravity. Because that character is third-party IP, this brief uses an original anime-style figure (a blindfolded fighter silhouette) drawn as flat shapes and lines, and translates the gravity idea into motion: token symbols are pulled into orbit around the logo, and chart lines bend and collapse toward the centre. The goal is to hype the exchange in 15 seconds with a hard-hitting motion language: a cut on every beat, fast punch-ins, radial speed lines and very short white flash frames.

## المشاهد المقترحة
- 0-1ث: إطار أسود مع ضربة باص واحدة؛ يقتحم الشعار النصي بمقياس 140% ثم يستقر على 100% بينما تنطلق خطوط سرعة شعاعية إلى الخارج.
- 1-4ث: ثلاث قطعات سريعة على الإيقاع: ظل المقاتل جانبيًا، لقطة قريبة مشرّحة بأسلوب glitch لعصبة العين، ثم يد مرفوعة تحمل كرة صغيرة من الفراغ المشوّه.
- 4-8ث: تتمدد الكرة إلى لوحة مبادلة: رمزا عملتين ينزلقان نحو بعضهما، وخط السعر يندفع عبر الشاشة وينحني كأن كتلة تجذبه.
- 8-12ث: انفجار جاذبي: تنكمش الشاشة كلها نحو المركز، تدور حلقة من أيقونات العملات حول الشعار بسرعة متزايدة، ويقتحم عنوان حركي عن سرعة المبادلة كلمة كلمة.
- 12-15ث: الختام: الشعار في المنتصف، يتجمّد المدار، يهدأ الانقسام اللوني، ويثبت سطر دعوة واحد مع معرّف المنصة حتى الضربة الأخيرة.

## Proposed scenes
- 0-1s: Black frame, a single bass hit; the wordmark smashes in at 140% scale and snaps to 100% while radial speed lines streak outward.
- 1-4s: Three rapid cuts on the beat: the fighter silhouette in profile, a glitch-sliced close-up of the blindfold, then a hand raised with a small sphere of distorted space.
- 4-8s: The sphere expands into a swap panel: two token symbols slide toward each other, a price line races across and bends as if pulled by mass.
- 8-12s: Gravity burst: the whole screen warps toward the centre, a ring of token icons orbits the logo at increasing speed, and a kinetic headline about fast swaps slams in word by word.
- 12-15s: Final lock-up: logo centred, orbit freezes, chromatic split settles, and a one-line call to action with the platform handle holds for the last beat.

## قواعد الحركة
- قطع على كل ضربة أثناء مقاطع الذروة (مقترح 150 نبضة في الدقيقة أي 400 مللي ثانية لكل ضربة) وعلى كل ضربة ثانية فيما عداها؛ لا تتجاوز أي لقطة 1.2 ثانية.
- تقفز دفعات التقريب من مقياس 1.00 إلى 1.15 في إطار واحد ثم تعود بمنحنى easeOutExpo خلال 350 مللي ثانية.
- خطوط السرعة شعاعية تُرسم من حافة الإطار نحو المركز، 80-140 خطًا، يعيش كل منها 3-5 إطارات، وتتجدد عند كل ضربة.
- لمسة glitch: إزاحة شرائح أفقية حتى 24 بكسل وانزياح قنوات RGB بمقدار 4-6 بكسل، لمدة 2-4 إطارات فقط بعد كل ضربة.
- الطباعة: خط عريض مضغوط مائل للعناوين، يدخل بتجاوز لإطارين (من مقياس 1.3 إلى 1.0) ويخرج بقطع حاد لا بتلاشٍ أبدًا.
- إطارات الومض بيضاء أو بلون تأكيد واحد، لا تتجاوز إطارين متتاليين، ولا تزيد على ثلاث ومضات في الثانية التزامًا بإرشادات الحساسية الضوئية.
- اتجاه الألوان (مقترح): قاعدة كحلية داكنة وسوداء، لون كهربائي واحد لتأثير الجاذبية، ونص أبيض؛ لا تتجاوز اللوحة ثلاثة ألوان.
- ممنوع: أي إطارات أو رسوم أو صوت من الأنمي نفسه، والتلاشي البطيء، وانزياحات Ken Burns، وطبقات lens flare الجاهزة.

## Motion rules
- Cut on every beat during drops (proposed 150 BPM, so 400 ms per beat) and on every second beat elsewhere; no shot longer than 1.2 s.
- Punch-ins jump from scale 1.00 to 1.15 in a single frame and relax back with easeOutExpo over 350 ms.
- Speed lines are radial strokes drawn from the frame edge toward centre, 80-140 lines, living 3-5 frames each, regenerated on every hit.
- Glitch accent: horizontal slice displacement of up to 24 px and RGB channel offset of 4-6 px, active only for 2-4 frames after a hit.
- Typography: heavy condensed italic for headlines, entering with a 2-frame overshoot (scale 1.3 to 1.0) and leaving by a hard cut, never a fade.
- Flash frames are white or a single accent colour, never more than 2 consecutive frames, and never more than three flashes per second to stay within photosensitivity guidance.
- Colour direction (proposed): deep navy and black base, one electric accent for the gravity effect, white type; the palette never exceeds three hues.
- Banned: any frames, artwork or audio from the anime itself, slow crossfades, Ken Burns drifts and stock lens-flare overlays.

## Facts stated by the source (rewritten in our words)
- The creator wanted an intense crossover edit between the GravityDEX brand and a well-known anime character.
- No duration, stack, tags or structure are given; the page's frame size is vertical (1080 by 1920).

## Assumptions
Only the brand, the anime crossover idea and the vertical format are stated; the 15-second length, the original substitute character, the beat grid and all effects are my proposed direction, chosen so that no third-party anime assets are reproduced.

## Keywords
مونتاج حماسي, أنمي, تداول لامركزي, عملات رقمية, قطع على الإيقاع, خطوط سرعة, جاذبية, anime edit, dex, crypto, beat cut, glitch, speed lines, vertical
