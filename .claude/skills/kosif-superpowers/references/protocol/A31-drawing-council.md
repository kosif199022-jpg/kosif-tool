# A31 — مجلس خبراء الرسم / Drawing council (USIP v5.5)

> **متى تقرأه / when to read:** قبل إرسال أي صورة أو رسمة أو ستوريبورد أو إطار مرسوم (القانون 27)، بعد أن يمر فحص `drawing_methods.py review`. [العودة إلى النواة](../../PROTOCOL.md#متى-تفتح-الملاحق--appendix-triggers)

> **الحالة هنا / backing:** قابل للتنفيذ ومختبر: `scripts/drawing_council.py` (`roster`، `plan`، `ingest`، `verdict`) و`evals/test_drawing_council.py`. السكربت لا يستدعي نموذجًا: يشغّل الفحوص الآلية ويكتب برومبت كل خبير ويحسب الحكم. الخبراء يشغّلهم Claude نفسه وكلاءَ مستقلين (Agent أو Workflow) يفتح كل منهم PNG بنفسه؛ وبلا أداة وكلاء تُكتب الإجابات في السياق نفسه وتُسجَّل `--simulated` ويقول المحضر SIMULATED.

## الفهرس / contents

- [لماذا هذا المجلس](#لماذا-هذا-المجلس)
- [الخبراء الأحد عشر](#الخبراء-الأحد-عشر)
- [التشغيل خطوة بخطوة](#التشغيل-خطوة-بخطوة)
- [الحكم والإيصال](#الحكم-والإيصال)
- [الربط بالمجلس العام](#الربط-بالمجلس-العام)
- [الحدود](#الحدود)

## لماذا هذا المجلس

رسمة «رجل ينقذ قطة» خرجت والحوض منفصل عن الصدر. القانون 27 أضاف فحص الاتصال الآلي، لكن الاتصال وحده لا يضمن صورة منطقية وجميلة: النسب والإيماءة والمنظور والضوء واللون والتكوين والخط والتعبير تحتاج عيونًا متخصصة. هذا المجلس يحوّل بطاقات أطلس الرسم الـ48 (المستخلصة من كتب الرسم، [الأطلس](../drawing-methods-atlas.md)) إلى أحد عشر خبيرًا، لكل منهم بطاقاته وفحوصها وأخطاؤها الشائعة وشروط رفض صريحة. كل بطاقة عند خبير واحد بالضبط.

## الخبراء الأحد عشر

الجدول مولَّد من `drawing_council.py roster --markdown` (عمود «كتب» عدد الكتب التي تستند إليها بطاقات الخبير):

| الخبير | يركّز على | البطاقات | كتب | شروط الرفض (veto) |
|---|---|---|---|---|
| E01 خبير الرؤية والبناء / Observation and construction | هل بُني كل شيء من أشكال بسيطة لها حجم، وهل المقاسات والفراغات السالبة صحيحة؟ | DM-01 DM-02 DM-03 DM-04 DM-41 DM-42 DM-44 | 30 | A form reads flat or broken where it should turn in space؛ Measured proportions between objects contradict what they are |
| E02 خبير التشريح والنسب / Anatomy and proportion | النسب بوحدة الرأس، والقفص والحوض والمفاصل، واليد والرأس والقماش. | DM-07 DM-08 DM-09 DM-10 DM-11 DM-34 | 24 | A limb or segment length is impossible for the body (beyond foreshortening)؛ Wrong number of limbs, fingers or joints, or a joint bends the wrong way |
| E03 خبير الإيماءة والحركة / Gesture and motion | خط الفعل، والاندفاع، والفعل لا الاسم، ودورة المشي والجري، والانضغاط والتمدد والتوقيت. | DM-06 DM-29 DM-30 DM-45 DM-27 DM-28 DM-17 | 14 | The pose does not perform the action the brief asks for؛ The body is stiff and symmetrical where the action needs a line of action |
| E04 حارس المنطق والفيزياء / Logic and physics guardian | جسم واحد متصل لكل شخصية، وكل يد أو قدم تلمس ما تمسكه أو تقف عليه، والوزن فوق قاعدة الارتكاز، ولا شيء يطفو بلا سبب. | DM-12 | 7 | Any body is in pieces (neck, waist or a limb not joined)؛ A hand or foot does not touch what holds it, or a body is held by nothing؛ The weight would make the figure or object fall |
| E05 خبير المنظور والفراغ / Perspective and space | خط أفق واحد، ونقاط تلاشٍ متسقة، والأشخاص والأشياء بالمقياس الصحيح في العمق. | DM-05 DM-31 DM-37 DM-39 | 10 | Two parts of the scene use incompatible horizons or vanishing points؛ A figure or object has an impossible size for its depth |
| E06 خبير الضوء والقيم / Light and value | مصدر ضوء واحد مقروء، وعائلة ضوء وعائلة ظل، وظلال ساقطة تتبع المصدر، وتجميع القيم. | DM-19 DM-20 DM-32 DM-33 | 17 | Shadows or highlights contradict the light direction |
| E07 خبير اللون / Colour | حرارة اللون ولوحة محدودة متناغمة، والبشرة والتظليل، والتباين الذي يخدم نقطة التركيز. | DM-21 DM-36 | 10 | Colours clash with the mood of the brief or make the focal point unreadable |
| E08 خبير التكوين والسرد / Composition and storytelling | نقطة تركيز واحدة، ومسار العين، والأشكال التي تحمل الشعور، ووضوح القصة من نظرة. | DM-22 DM-23 DM-26 | 12 | The story of the brief cannot be read at a glance؛ The focal point is lost or there are two competing ones |
| E09 خبير الخط والتشطيب / Line and finish | أوزان الخط، والتراكب، والملمس، ونظافة الحواف والتقاطعات (لا مماسات مزعجة). | DM-24 DM-47 DM-48 | 14 | Tangents, stray marks or uneven line weights make shapes unreadable |
| E10 خبير تصميم الشخصيات والتعبير / Character design and expression | لغة الأشكال، والسيلويت المقروء، والجاذبية، وتعبير الوجه والعين والحاجب، والشعر ككتل. | DM-13 DM-14 DM-15 DM-16 DM-18 DM-35 DM-40 DM-43 DM-46 | 27 | The expression contradicts the emotion of the brief؛ The silhouette does not read |
| E11 خبير الحيوان والطبيعة / Animals and nature | بناء الحيوان من خط العمود الفقري وكتل الصدر والحوض، والأشجار والنبات من أشكال بسيطة. | DM-25 DM-38 | 10 | An animal's anatomy or pose is impossible for that animal |

## التشغيل خطوة بخطوة

```bash
SK=.claude/skills/kosif-superpowers
# 1. القانون 27 أولًا: review حتى PASS، ثم صيّر PNG وافتحه
python3 $SK/scripts/drawing_methods.py review --svg scene.svg
# 2. خطط المجلس: يشغّل review ومقاييس النغمة ويكتب prompts/E01..E11.md
python3 $SK/scripts/drawing_council.py plan --png scene.png --svg scene.svg --source gen.py --style "<الستايل>" --brief "<الطلب>" --dir out/<work>/council-r1
# من الجولة الثانية: --baseline <أحسن PNG سابق> (كل خبير يقول better/same/worse)
# 3. شغّل الخبراء: وكيل مستقل لكل برومبت يفتح الصورة ويعيد JSON، ثم سجّل كل إجابة
python3 $SK/scripts/drawing_council.py ingest --dir out/<work>/council-r1 --expert E04 --file e04.json
# 4. الحكم: verdict.json وminutes.md؛ الرمز 0 = PASS
python3 $SK/scripts/drawing_council.py verdict --dir out/<work>/council-r1
```

إن خرج FAIL: نفّذ `required_fixes` كلها، وأعد التصيير والفحص، وخطط مجلسًا جديدًا في مجلد جديد (`council-r2`)؛ الإجابات مربوطة ببصمة PNG، فلا تُحسب إجابة عن صورة قديمة.

ثلاث قواعد تمنع أن تسوء الرسمة وهي تُصلَّح (درس الجولات الأولى لرسمة الرجل والقطة: كل جولة أُعيد فيها بناء المشهد لإرضاء كل خبير وحده فخرجت أسوأ من الأولى):
- **ملاحظة بكودها:** حين يكون للرسمة SVG أو مولّد (`--svg` و`--source`) فكل ملاحظة فيها fix تحمل `code`: `where` (الملف:السطر والعنصر بـdata-figure/data-part أو id، أو دالة المولّد) و`cause` (القيمة أو الإحداثي أو المنطق المسبِّب) و`change` (التعديل نفسه)، و`ingest` يرفض ما ينقصه ذلك. والبرومبت يحمل خريطة الأجزاء المسمّاة بأسطرها.
- **تثبيت الستايل (`--style`):** كل تصليح داخل ستايل الرسمة وألوانها وتكوينها؛ لا يُشدّ الكرتون المسطح نحو شبه الواقعية.
- **المقارنة بأحسن نسخة (`--baseline`):** كل خبير يقول `vs_baseline` (better/same/worse)، وإن قال أكثر من نصفهم worse فالجولة FAIL مهما أصلحت: تُحفظ النسخة الأحسن ويُصلَّح عيبها هي. وأصلح ملف الرسمة نفسه ولا تعد بناءها من الصفر.

## الحكم والإيصال

PASS يحتاج كل هذا معًا: كل فحص آلي PASS (فحص الاتصال، وفحوص البطاقات حين يكون للرسمة نوع)، وأجاب الخبراء الأحد عشر عن الصورة نفسها، ولا veto ولا fix مفتوح، وكل درجة (صحة، حِرفة، جمال) 3 على الأقل من 5، ومتوسط الجمال 3.5 على الأقل. والمحضر يذكر الوضع: REAL_AGENTS حين أجاب كل خبير وكيلًا مستقلًا، وSIMULATED حين كتب سياق واحد أي إجابة. تُسلَّم الصورة مع `verdict.json` و`minutes.md`.

## الربط بالمجلس العام

`drawing_council.py roster --personas` يخرج الخبراء بصيغة شخصيات المجلس العام (`kosif.council-personas.v1`، المعرّفات D01…D11)، ونسخة منها في `data/drawing_council_personas.json`؛ فيمكن لـ`council.py plan --personas-file data/drawing_council_personas.json` (ملحق A30 للمجلس العام) أن يجلسهم في نقاش الخطط. مجلس الرسم نفسه يبقى بصيغته (`kosif.drawing-council.v1`، pass/fix/veto) لأنه يحكم على صورة لا على خطط.

## الحدود

الفحوص الآلية تقيس الهندسة والنغمة فقط. الدرجات أحكام مسجّلة من الخبراء وفق بطاقاتهم، لا برهان على الجمال؛ ولا تقل «المجلس أثبت أن الصورة جميلة»، بل «أجاز المجلس الصورة بمتوسط جمال X، بوضع REAL_AGENTS أو SIMULATED». والبطاقات ملخصات لطرق الكتب لا الكتب نفسها.
