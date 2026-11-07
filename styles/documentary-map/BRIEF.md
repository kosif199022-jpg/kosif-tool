# خريطة وثائقية — خريطة واقعية مع صور أرشيفية وتواريخ — خريطة وثائقية

> ريل وثائقي عمودي 9:16 على خريطة تضاريس واقعية بألوان باهتة وحبوب فيلم، تنقضّ الكاميرا من رؤية إقليمية إلى مدن محددة بدبابيس، وتظهر صور أرشيفية بالأبيض والأسود في إطارات مائلة قليلاً بحركة كين بيرنز، مع شريط تاريخ كبير وأسماء أماكن بخط سيريف عربي.
>
> A 9:16 documentary reel over a desaturated, film-grained realistic terrain map: the camera swoops from a regional view down to pinned cities, black-and-white archival photos appear in slightly tilted frames with Ken Burns drift, and a large date ribbon and serif Arabic place names anchor each stop.

ملف تعريفي أصلي من إعداد KOSIF، مشتق من عنوان المرجع وتصنيفاته ووصفه العام فقط؛ لم تتم مشاهدة الفيديو عند كتابته، فتحقّق من المرجع قبل الإنتاج.
Original KOSIF brief derived only from the reference title, tags and public description; the video was not watched when it was written, so verify against the reference before production.

- المرجع / Reference: https://github.com/kosif199022-jpg/kosif-one
- التصنيفات / Categories: diagrams, photos
- النسبة المقترحة / Aspect: 9:16 · المدة / Duration: 36 s · الصعوبة / Difficulty: 4/5
- التقنية المقترحة / Stack: Remotion, React, WebGL, CSS

## الفكرة
الخريطة هنا مسرح للتاريخ الحقيقي وليست رسماً توضيحياً: صور قمر صناعي أو تضاريس حقيقية، وصور ووثائق أرشيفية، وتواريخ. كل محطة في القصة = نزول على مكان + صورة + تاريخ + جملة. النبرة جادة وسينمائية مثل البرامج الوثائقية، والانتقالات طيران فوق الأرض بين الأماكن.

## Concept
The map is a stage for real history, not an illustration: satellite or terrain imagery, archival photos and documents, and dates. Each story stop = descend on a place + one photo + one date + one sentence. The tone is serious and cinematic like a TV documentary, with transitions flying over the ground between places.

## المشاهد المقترحة
- 0-3 ث: رؤية إقليمية واسعة مع دوران بطيء درجتين وحبوب فيلم وتعتيم أطراف؛ والعنوان بخط سيريف عربي يظهر فوق تدرج داكن أعلى الشاشة.
- 3-8 ث: تنقضّ الكاميرا (1.8 ث) إلى المدينة الأولى؛ يسقط دبوس مع حلقة موجية ويخرج منه اسم المكان.
- 8-14 ث: إطار صورة أرشيفية ينزلق بميل -3 درجات بحافة ورقية وينجرف 4٪ (كين بيرنز)؛ وشريط تاريخ مثل «1919» يعدّ أو يتقلب.
- 14-22 ث: الكاميرا تطير إلى المحطة الثانية بينما يُرسم خط مسار أو حدود رفيع على التضاريس؛ صورة وتاريخ ثانيان.
- 22-30 ث: المحطة الثالثة: منطقة تمتلئ بلون أحمر شفاف #b23a2e مع تعليق قصير.
- 30-36 ث: ابتعاد إلى الرؤية الواسعة يُظهر كل الدبابيس والخطوط الواصلة؛ ثم سطر ختامي وذكر المصدر.

## Proposed scenes
- 0-3s: Wide regional view, slow rotation of 2 degrees, grain and vignette; the title in serif Arabic fades up over a dark gradient at the top.
- 3-8s: Camera dives (1.8 s, easeInOutCubic) to the first city; a pin drops with a shockwave ring and the place name slides out from it.
- 8-14s: An archival photo frame slides in at -3 degrees with a paper border, drifting 4% (Ken Burns); a date ribbon '1919' counts or flips in.
- 14-22s: The camera flies to stop two while a thin route or border line draws on the terrain; second photo and date.
- 22-30s: Stop three: a region highlight floods with a translucent red #b23a2e area and a short caption.
- 30-36s: Pull out to the wide view showing all pins and connecting lines; a closing line and source credit fade in.

## قواعد الحركة
- تلوين الخريطة: تضاريس باهتة (تشبع 30-40٪)، ظلال مرفوعة إلى #1f2326 وإضاءات #d9d2c3؛ مع حبوب فيلم متحركة 3-4٪ وتعتيم أطراف ناعم طوال الوقت.
- ألوان التمييز: أحمر الدبابيس والمسار #b23a2e، التسميات أبيض مكسور #f2ede4 بحد داكن 1 بكسل، وشريط التاريخ أسود #111 بأرقام بيضاء مكسورة.
- الخطوط: سيريف عربي (أميري أو نوتو نسخ عربي عريض) للأسماء والعناوين، وخط بسيط (IBM Plex Sans Arabic) للتعليقات؛ من اليمين لليسار دون تقطيع للحروف.
- الكاميرا: كل انتقال بين المحطات طيران بإحساس ثلاثي الأبعاد (ابتعاد قليل ثم انزلاق ثم اقتراب) مدته 1.5-2.5 ث؛ والخريطة لا تُقطع أبداً.
- الصور الأرشيفية: أبيض وأسود أو بني قديم، بحافة ورقية، ميل بين -4 و+4 درجات، انجراف كين بيرنز 3-5٪، وظل ناعم.
- الإيقاع يتبع التعليق الصوتي: محطة لكل مجموعة جمل، بثبات 4-7 ث لكل محطة.
- الفرق عن رحلة على الخريطة: تضاريس حقيقية وصور ونبرة وثائقية رصينة، لا خريطة ورقية مرسومة مع شخصية مسافرة.

## Motion rules
- Map grade: desaturated terrain (saturation 30-40%), shadows lifted to #1f2326, highlights #d9d2c3; 3-4% animated film grain and a soft vignette at all times.
- Accents: pin and route red #b23a2e, labels off-white #f2ede4 with a 1 px dark stroke, date ribbon black #111 with off-white numerals.
- Typography: serif Arabic (Amiri or Noto Naskh Arabic Bold) for names and titles, a clean sans (IBM Plex Sans Arabic) for captions; RTL, no letter splitting.
- Camera: every move between stops is a 3D-feeling fly (zoom out slightly, pan, zoom in) of 1.5-2.5 s with easeInOutCubic; the map never cuts.
- Archival photos: black and white or sepia, paper border, -4 to +4 degree tilt, 3-5% Ken Burns drift, drop shadow 0 8 24 rgba(0,0,0,.4).
- Pacing follows narration: one stop per sentence group, holding 4-7 s each.
- Different from map-journey: real terrain and photos with a sober documentary tone, not an illustrated parchment map with a travelling character.

## Facts stated by the source (rewritten in our words)
- Catalogued as a KOSIF original style named for a documentary map, in the Diagrams and Photos categories.

## Assumptions
Authored KOSIF definition, not an observed reference: there is no reference video for this base style (its page is the KOSIF repo root), so palette hex values, type choices, timings and scene beats are original KOSIF design decisions, not measurements. Assumed a 9:16 reel of about 36 s with narration; terrain tiles and archival photos must come from the user or properly licensed sources.

## Keywords
documentary, map, archival photos, ken burns, terrain, history, film grain, pins, خريطة وثائقية, وثائقي, صور أرشيفية, تاريخ, تضاريس, خريطة
