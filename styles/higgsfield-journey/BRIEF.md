# جولة سينمائية بكاميرا تطير عبر مشاهد متصلة بلا قطع — جولة سينمائية

> ريل عمودي يبدو كرحلة كاميرا طائرة واحدة: الكاميرا تندفع عبر نافذة أو باب أو سحابة إلى مكان جديد، كل مشهد مولد بالذكاء الاصطناعي أو صورة واقعية بعمق، والانتقالات «عبور» مستمرة بلا قطع، مع عناوين عربية قليلة تظهر في كل محطة.
>
> A vertical reel that feels like one continuous flying-camera trip: the camera dives through a window, door or cloud into each new place, every location an AI-generated shot or a depth-layered photo, with seamless fly-through transitions and a short Arabic title at each stop.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://github.com/kosif199022-jpg/kosif-one
- التصنيفات / Categories: 3d, photos
- النسبة المقترحة / Aspect: 9:16 · المدة / Duration: 30 s · الصعوبة / Difficulty: 4/5
- التقنية المقترحة / Stack: Remotion, React, WebGL

## الفكرة
الفكرة رحلة: من مكان إلى مكان، أو من الماضي إلى الحاضر، أو من الفكرة إلى المنتج، والكاميرا لا تتوقف. كل محطة لقطة سينمائية مولدة (مثل حركات الكاميرا في أدوات الفيديو التوليدي: اندفاع، دوران، صعود)، وتُربط اللقطات بنقاط عبور يتشابه فيها الشكل أو اللون. يختلف عن «مشاهد 3D السينمائية» بأنه يعتمد على لقطات مولدة أو صور وليس على مشهد مبني، وعن «عالم التمرير» بأن الحركة اندفاع كاميرا في العمق وليست تمريراً جانبياً.

## Concept
The idea is a journey: place to place, past to present, or idea to product, and the camera never stops. Each stop is a cinematic generated shot (using generative-video camera moves such as dolly-in, orbit, crane up), and shots are joined at pass-through points where shape or colour match. It differs from cinematic-3d because it relies on generated shots or photos rather than a built scene, and from scroll-world because motion is a camera dive into depth rather than a sideways scroll.

## المشاهد المقترحة
- 0-2 ث: الافتتاح: انقضاض جوي مباشر إلى مدينة، والسحب تندفع أمام العدسة.
- 2-8 ث: المحطة الأولى: الكاميرا تخترق نافذة مضيئة إلى داخل مكان؛ وعنوان المكان العربي القصير يظهر في الثلث العلوي.
- 8-14 ث: عبور مطابق: الكاميرا تطير داخل شيء داكن (فنجان، نفق، بؤبؤ عين) يصبح الانتقال إلى المحطة الثانية.
- 14-20 ث: المحطة الثانية: دوران حول موضوع في زمن أو مكان جديد؛ والإضاءة تتحول من الدافئ إلى البارد أثناء الحركة.
- 20-26 ث: المحطة الثالثة: صعود رافعة خارج المشهد يكشف المنظر الواسع؛ وتظهر الرسالة الأساسية.
- 26-30 ث: الختام: ابتعاد أخير نحو السماء يذوب في الشعار.

## Proposed scenes
- 0-2s: Hook: an aerial dive straight down into a city, clouds rushing past the lens.
- 2-8s: Stop one: the camera pushes through a lit window into an interior; a short Arabic place title fades in at the top third.
- 8-14s: Match pass: the camera flies into a dark object (a cup, a tunnel, a pupil) that becomes the transition into stop two.
- 14-20s: Stop two: an orbit around a subject in a new era or setting; light changes from warm to cool during the move.
- 20-26s: Stop three: crane up out of the scene to reveal the wide landscape; the main message appears.
- 26-30s: Ending: final pull-back into the sky that dissolves into the logo.

## قواعد الحركة
- زخم أمامي متصل: سرعة الكاميرا لا تصل إلى الصفر أبداً؛ وكل لقطة تبدأ بالسرعة التي انتهت بها السابقة (تسريع من 1 إلى 2.5 عند نقاط العبور ثم عودة).
- الانتقالات عبور عند نقاط متطابقة (فجوة داكنة، ضوء ساطع، شكل أو لون متشابه) مع تمويه حركة 4-8 إطارات وتمويه تقريب خفيف؛ ولا تداخل تلاشي أطول من 6 إطارات.
- كل محطة 4-6 ثوانٍ؛ واللقطات المولدة تُخطط لكل محطة بحركة كاميرا محددة (اقتراب، دوران، صعود، انقضاض FPV) وإحساس عدسة ثابت.
- تلوين كل المحطات نحو مظهر واحد: سواد مرفوع #121417 وإضاءات دافئة #ffcf99، لتبدو اللقطات المولدة فيلماً واحداً.
- العناوين العربية بخط رفيع نظيف (مثل IBM Plex Sans Arabic Light) بحجم 48-60 بكسل في الثلث العلوي، تظهر في 10 إطارات وتختفي قبل نقطة العبور التالية.
- عند استخدام صور بدل فيديو مولد، تُقسم إلى 3-5 طبقات عمق وتتحرك كاميرا افتراضية داخلها (2.5D).

## Motion rules
- One continuous forward momentum: camera speed never drops to zero; each shot starts at the speed the previous one ended (speed ramp 1x -> 2.5x through pass points, then back).
- Transitions are pass-throughs at matched points (dark hole, bright light, same shape or colour) with 4-8 frames of motion blur and a slight zoom blur; no crossfades longer than 6 frames.
- Each stop is 4-6 s; generated clips are planned per stop with an explicit camera move (dolly-in, orbit, crane up, FPV dive) and consistent lens feel.
- Grade all stops toward one look: lifted blacks #121417, warm highlights #ffcf99, so generated shots feel like one film.
- Arabic titles: clean light sans (e.g. IBM Plex Sans Arabic Light) 48-60 px, placed in the top third, fade in over 10 frames and out before the next pass point.
- When using photos instead of generated video, split them into 3-5 depth layers and move a virtual camera through them (2.5D).

## Facts stated by the source (rewritten in our words)
- KOSIF lists this as an original style named cinematic journey, tagged 3D and photos; the id refers to Higgsfield, a generative video tool.

## Assumptions
Authored KOSIF definition, not an observed reference: the record points only to the repo root, so there was no video to watch. Palette hex values, fonts, timings and scene beats are design choices written for this style, not measurements. The link to Higgsfield-style generated camera moves is inferred from the style id; generated clips must come from the user's own generations.

## Keywords
camera journey, fly-through, seamless transition, ai video, fpv, generated shots, travel, جولة سينمائية, رحلة, انتقال سلس, كاميرا طائرة, فيديو مولد, سفر
