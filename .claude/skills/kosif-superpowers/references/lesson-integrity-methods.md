# دروس تفاعلية لا تكذب أرقامها — Lesson integrity methods

> **من أين جاءت / where these came from.** طرق لاحظناها في بناء منشور لكتاب فيزياء تفاعلي ثلاثي الأبعاد ([iamtechartist/every-joule-lesson1](https://github.com/iamtechartist/every-joule-lesson1))، مكتوبة هنا بكلامنا. المستودع بلا رخصة، فلم ننسخ منه كودًا ولا نصًا ولا صوتًا؛ الإيصال في [every-joule-study-20261023.md](every-joule-study-20261023.md). الأداة القابلة للتشغيل `scripts/lesson_integrity.py` مكتوبة من الصفر.
>
> Methods observed in a published build of an interactive 3D physics book, restated in our own words. The repository carries no licence, so no code, text or audio was copied. The runnable checker `scripts/lesson_integrity.py` is written from scratch.

## الفهرس / contents

- [متى تستعملها](#متى-تستعملها)
- [البطاقات](#البطاقات)
- [الأداة](#الأداة)
- [ما لا تفعله](#ما-لا-تفعله)

## متى تستعملها

أي شرح أو إنفوجراف أو فيديو تعليمي أو درس تفاعلي يعرض أرقامًا حقيقية (طاقة، أسعار، أحجام، نسب)، أو صفحة تعليمية سيعرضها معلّم على سبورة. When an explainer, infographic, lesson film or interactive page shows real numbers, or a page will be projected in a classroom.

## البطاقات

| # | الطريقة / method | ماذا تعني عمليًا |
|---|---|---|
| EJ-01 | **سجل قيم واحد بمصدر واقتباس** / one value registry, each value with a source and the supporting sentence | كل رقم يظهر للمشاهد له مدخل واحد: القيمة والوحدة وماذا يقيس والمدى إن وُجد ومرجع المصدر و**الجملة المقتبسة** التي تثبته. من يراجع يقرأ الجملة بدل فتح ملف PDF من 80 صفحة. |
| EJ-02 | **النص يشير إلى الرقم بالمعرّف** / text refers to numbers by id | الجمل تكتب `{v:shelf}` لا `1.5 m`. لو اختفى المعرّف أو لم تُعرف طريقة طباعة وحدته، يتوقف البناء ولا يطبع تخمينًا (fail closed). تغيير الرقم في السجل يغيّره في كل مكان. |
| EJ-03 | **ملف الفجوات** / an explicit gaps list | رقم لم نجد له مصدرًا يُترك فارغًا مع سبب مكتوب («لا كتلة موثقة لدراجة عادية؛ الحساب للراكب وحده»)، ولا يُخترع. الفجوة تظهر في التقرير كتحذير، والرقم الفارغ لا يُعرض. |
| EJ-04 | **مراجعة حقائق تصحح إلى الرقم المنشور** / a fact-check that restores the published figure | حين يختلف رقم محسوب بالتحويل (290 kcal × 4.184 = 1213) عن الرقم المنشور (1210 kJ)، نعرض المنشور ونكتب ملاحظة بالتصحيح، ثم نعيد حساب كل ما اشتُق منه. |
| EJ-05 | **القيم المشتقة تُعاد حسابها** / derived values are recomputed | المجموع أو الحاصل يُسجل بمعادلته (`sum` of a, b) ويُفحص كل بناء؛ لو تغيّر أحد الأجزاء ولم يتغير المجموع يفشل الفحص. |
| EJ-06 | **دفتر حفظ: ابحث عن كل وحدة** / a conservation ledger: find every joule | التحدي «أسقِط الكتاب وابحث عن كل الـ 14.7 J» يعني أن ما دخل = ما خرج (حركة، حرارة، صوت) ضمن سماحية، ولا قيمة سالبة. الكفاءة = المفيد ÷ الداخل. تصلح لأي كمية تُحفظ: طاقة، ميزانية، وقت، وقود. |
| EJ-07 | **تحدٍّ قابل للحل أولًا** / check a challenge is solvable before posing it | الهدف (ارتفاع الارتداد الثاني، مدى نابض) يُولّد من النموذج نفسه، ويُفحص أنه ممكن ضمن حدود الأداة؛ وإلا يقول الدرس صراحة إن الهدف غير ممكن من أي ارتفاع، بدل تحدٍّ مستحيل. |
| EJ-08 | **مقياس 1-2-5** / a 1-2-5 gauge scale | سعة العدّاد أو الوعاء = أصغر 1 أو 2 أو 5 × 10ⁿ تجعل القيمة تملأ 90% على الأكثر. أرقام مقروءة على المحور وامتلاء واضح بلا فيضان. |
| EJ-09 | **خريطة المنهج مع الخلافات** / a curriculum map that records disagreements | صفحة للمعلم تربط كل فكرة بمواصفة كل جهة امتحانات (برقم البند)، وتذكر أين تختلف المصطلحات (جهة تذكر «مخطط سانكي» وأخرى لا؛ جهة تعد الصوت انتقالًا وأخرى لا). |
| EJ-10 | **تعريف بطولين** / a glossary with a long and a short definition | لكل مصطلح جملة كاملة للصفحة وجملة قصيرة للتلميح أو الشريط. نفس المعنى، مقاسان. |
| EJ-11 | **صوت من تسجيلات حقيقية في ملف واحد** / one sound sprite from real recordings | كل المؤثرات مقطوعة من تسجيلات CC0، مضبوطة الجهارة، في ملف واحد مع قائمة مناطق (بداية، طول، تكرار، طبقات) وعلامة عينة واحدة في البداية للمحاذاة، وجدول اعتمادات بالرخصة لكل مؤثر، وبصمات المصادر. لا موسيقى ولا صوت مولّد. |
| EJ-12 | **تفضيلات الحركة والعرض** / motion and display preferences | احترام `prefers-reduced-motion` ووضع «ثابت» يتذكره المتصفح، ووضع «بروجكتر» بخط أكبر وتباين أعلى، وبديل نصي كامل حين لا يعمل WebGL أو JavaScript، ورابط تخطٍّ لقارئ الشاشة، وطباعة. وحفظ التفضيل داخل try/catch لأن التخزين قد يُمنع. |
| EJ-13 | **شاشة التحميل تُرسم قبل أي سكربت** / the loader is styled inline | CSS الحرج داخل الصفحة نفسها حتى تظهر الهوية فورًا وتُستعمل نفس ملفات الخط التي سيستعملها الكتاب فلا تُحمّل مرتين. |

## الأداة

`python3 scripts/lesson_integrity.py` (stdlib only):

```bash
python3 scripts/lesson_integrity.py values --registry values.json                 # EJ-01, EJ-03, EJ-05
python3 scripts/lesson_integrity.py render --registry values.json --content lesson.md --strict --out lesson.out.md   # EJ-02
python3 scripts/lesson_integrity.py ledger --file drop.json                       # EJ-06
python3 scripts/lesson_integrity.py scale 14.7                                    # EJ-08 → capacity 20
python3 scripts/lesson_integrity.py sprite --manifest sounds.json --credits CREDITS.md --duration 20   # EJ-11
python3 scripts/lesson_integrity.py --self-test
```

شكل السجل / registry shape:

```json
{"sources": {"spec": {"title": "Physics specification", "url": "https://example.org/spec.pdf"}},
 "values": {
   "shelf": {"value": 1.5, "unit": "m", "what": "shelf height",
             "source": {"ref": "spec", "quote": "a shelf 1.5 m above the floor"}},
   "bike":  {"value": null, "unit": "kg", "what": "bicycle mass", "gap": "no cited mass"},
   "total": {"value": 4210, "unit": "kJ", "what": "breakfast", "derived": {"op": "sum", "of": ["toast", "butter"]}}}}
```

Placeholders: `{v:id}` prints number and unit, `{v:id|2}` with two decimals, `{n:id}` the number alone; unit `fraction` prints as a percentage. `--strict` also flags numbers with units typed straight into the text. `render --out` writes nothing when any error is found. Use it before narrating numbers in a montage or explainer (the narration script is the content file), and before an infographic's labels are set.

## ما لا تفعله

- لا تتحقق من أن المصدر صحيح أو أن الاقتباس موجود فعلًا في المصدر؛ تتحقق فقط من أن الرقم موجود في الاقتباس المسجّل. قراءة المصدر ما زالت عمل إنسان أو أداة بحث.
- لا تحل نموذجًا فيزيائيًا ولا تولّد تحديات (EJ-07 طريقة، لا أداة).
- لا تقيس الجهارة ولا تقطع الصوت؛ فحص `sprite` يقرأ القائمة والاعتمادات فقط.
- It never copies or runs anything from the studied repository.
