# الدعاء — ريل دعاء ليلة الجمعة — الدعاء

> ريل عمودي 9:16 مدته نحو 15 ثانية: عبارة دعاء واحدة = لقطة واحدة = سطر واحد على الشاشة. لقطات دافئة منخفضة الإضاءة (مصحف، ورد، مبخرة، شموع) تتبدل على بداية كل عبارة بانتقالات ضبابية ومرآة وزوم، بينما يبقى فوقها عنوان «الجُمُعَة» بخط ثلث أبيض وتاريخ اليوم وسطر ذهبي «ليلة جمعة مبـــاركة» وسطر الدعاء الأبيض بهالة داكنة ضيقة.
>
> A ~15 s vertical 9:16 reel: one spoken dua phrase = one shot = one on-screen line. Warm low-key shots (Quran, roses, incense, candles) cut on each phrase onset with blur, mirror and zoom transitions, under a persistent white Thuluth title «الجُمُعَة», the date, a gold subtitle and a white dua line with a tight dark halo.

ملف تعريفي أصلي من إعداد KOSIF، رُوجع وصُحّح مقابل إطارات مأخوذة من فيديو المرجع (2026-10-18)؛ التوقيتات والألوان قراءات تقريبية من تلك الإطارات، فراجع المرجع للتفاصيل الدقيقة.
Original KOSIF brief, revised against frames sampled from the reference video (2026-10-18); timings and colours are approximate readings from those frames, so check the reference for fine detail.

- المرجع / Reference: https://github.com/kosif199022-jpg/kosif-tool/tree/main/styles/dua
- التصنيفات / Categories: kinetic-type, music
- النسبة المقترحة / Aspect: 9:16 · المدة / Duration: 15.4 s · الصعوبة / Difficulty: 3/5
- التقنية المقترحة / Stack: HTML Canvas, CSS

## الفكرة
صوت الدعاء هو العمود الفقري: كل قطع يقع على بداية عبارة (متوسط الانحراف المقاس 0.10 ث)، وكل سطر يظهر 0.2 ث بعد القطع ويختفي 0.3 ث قبل التالي. النص ثابت لا يتحرك إلا رقم اليوم الذي يطير في قوس عند البداية وينجرف عند النهاية. الانتقالات تقع على الصورة فقط ولا يتأثر بها النص أبداً.

## Concept
The recited voice is the spine: every cut lands on a phrase onset (measured mean offset 0.10 s), each line fades in 0.2 s after its cut and out 0.3 s before the next. Text stays still; only the day number flies in on an arc at the start and drifts at the end. Transitions affect the footage only, never the text.

## المشاهد المقترحة
- 0–0.6 ث ظهور من الأسود؛ العنوان والتاريخ والسطر الذهبي يظهرون، ورقم اليوم يطير من المنتصف إلى مكانه (0.1→1.1 ث)
- لقطة العبارة الأولى (مبخرة ومصحف ووردة) مع أول سطر دعاء
- العبارات 2–6: لقطة دافئة لكل عبارة، القطع على بداية العبارة بانتقال ضبابي أو مرآة
- العبارة السابعة الأطول تأخذ أطول لقطة بعد قطع زووم
- لقطة «آمين» الأخيرة بعد ضبابية دوّارة؛ رقم اليوم ينجرف يساراً 40 بكسل ثم يختفي النص

## Proposed scenes
- 0–0.6 s fade from black; title, date and gold subtitle fade in; the day number flies from centre to its slot (0.1→1.1 s, easeOutCubic)
- Phrase 1 shot (incense, Quran, rose) with the first dua line
- Phrases 2–6: one warm still-life shot per phrase, cuts on onsets with blur-in or mirror-out transitions
- Phrase 7 (the longest) gets the longest shot after a push-in cut
- Final «آمين» shot after a spin/zoom blur; the day number drifts −40 px and the overlay fades out by the end

## قواعد الحركة
- القطع على بداية العبارة؛ طول اللقطة = طول العبارة
- سطر الدعاء: ظهور بالشفافية 0.17 ث، ثبات، اختفاء 0.15 ث
- رقم اليوم وحده يتحرك؛ بقية النص يظهر ويختفي فقط
- الانتقالات على الصورة تحت النص ولا تمس النص أبداً
- الصور الثابتة تأخذ زووم بطيء 3٪؛ الفيديو انجراف ≤ 3 بكسل/ث
- تلوين دافئ منخفض الإضاءة بلا تعتيم أطراف مضاف
- الصوت ينسخ كما هو دون أي تعديل

## Motion rules
- Cut on the phrase onset; shot length = phrase length
- Dua line: opacity in 0.17 s (easeOutQuad), static hold, out 0.15 s (easeInQuad)
- Only the day number moves; all other text only fades
- Transitions (blur_in, mirror_out_blur_in, zoom_out_cut, spin_zoom_blur) apply to footage below the text, never to text
- Stills get a 3 % slow push-in; video drifts ≤ 3 px/s
- Warm low-key grade: Lab L 28–42, a +4…+13, b +4…+23, no added vignette
- Copy the user's voice track untouched

## Facts stated by the source (rewritten in our words)
- Reference: 1080×1920, 60 fps, 15.43 s, 8 shots, 7 cuts at 1.67, 4.52, 6.30, 8.02, 9.76, 11.22, 14.18 s
- Text colours measured: white #FEFEFD, gold #FED27E, halo #0C0805
- Voice-dominant audio at −12.9 LUFS integrated, −2.3 dBTP

## Assumptions
Fonts are the closest OFL matches (Marhey 700 for the gold line, Scheherazade New Bold for the dua, the composed KOSIF Jumuah Thuluth title), not the reference app fonts. Transition curves are read from frames, not from a project file.

## Keywords
dua, دعاء, friday, جمعة, reel, vertical, arabic, thuluth, kinetic type, blur transition, voice sync, islamic
