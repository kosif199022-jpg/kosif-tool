# STYLE.md — {style_name}

> الاستايل: `{id}` · المصدر: {origin} · النوع: {type} · تاريخ الإنشاء: {date}
> Style: `{id}` · Origin: {origin} · Type: {type} · Created: {date}

هذا المستند يفصل بوضوح بين ما **شوهد فعلًا** في المرجع وما **افتُرض** لسد الفراغات. لا تنقل أي عنصر من قسم الافتراضات إلى قسم الملاحظات إلا بدليل (إطار مع طابع زمني).
This document separates what was **actually observed** in the reference from what was **assumed** to fill gaps. Nothing moves from Assumed to Observed without evidence (a frame with a timestamp).

## 1. المرجع / Reference

| البند / Item | القيمة / Value |
|---|---|
| الصفحة المرجعية / Reference page | {page} |
| الفيديو المرجعي / Reference video | {video} |
| صاحب المرجع / Credited creator | {creator} |
| الفئات / Categories | {categories} |
| دلائل الفئات / Category playbooks | {playbooks} |
| ملف المهارة / Skill file | {skill} |
| الملف الإبداعي / Creative brief | {brief} |
| المخرج المطلوب / Deliverable | {aspect} · {resolution} · {fps} fps · {duration} s · {frames} frames |
| التقنية المختارة / Chosen stack | {stack} |
| الصعوبة المقدّرة / Estimated difficulty | {difficulty} |

- [ ] شاهدتُ المرجع بأدواتي وأخذت لقطات منه / I watched the reference with my tools and sampled frames
- [ ] لم أستطع مشاهدة المرجع؛ كل ما يلي مبني على الوصف والتصنيفات / I could not watch the reference; everything below is inferred from its description and categories

## 2. ما لوحظ من المرجع / Observed from the reference

اكتب فقط ما رأيته. كل سطر يحمل زمنًا بالثواني ودليلًا (رقم الإطار أو الطابع الزمني).
Write only what you saw. Every row carries a time in seconds and evidence (frame number or timestamp).

| الزمن / Time (s) | الملاحظة / Observation | العنصر / Element | الدليل / Evidence |
|---|---|---|---|
| 0.0 | | | |
| | | | |
| | | | |

ملخص الإيقاع / Rhythm summary: عدد اللقطات، متوسط طول اللقطة، أسرع قطع، أبطأ حركة.
Shot count, average shot length, fastest cut, slowest move.

## 3. ما افترضته / Assumed

كل افتراض يذكر سببه وأثره لو كان خاطئًا، حتى يمكن مراجعته بسرعة بعد أول معاينة.
Each assumption states its reason and the impact if it is wrong, so it can be revisited after the first preview.

| الافتراض / Assumption | السبب / Reason | الأثر لو كان خاطئًا / Impact if wrong |
|---|---|---|
| | | |
| | | |

## 4. رموز التصميم / Design tokens

علّم كل قيمة بـ **مقاس** (من إطار فعلي) أو **مقدّر** (اختيار أصلي). القيم أدناه نقاط انطلاق لا أكثر.
Mark every value as **measured** (from a real frame) or **estimated** (an original choice). The values below are starting points only.

### 4.1 الألوان / Colors

| الرمز / Token | القيمة / Value | مقاس أم مقدّر / Measured or estimated | الاستخدام / Use |
|---|---|---|---|
| bg | #0B0F19 | estimated | الخلفية الرئيسية / main background |
| fg | #F5F7FA | estimated | النص الأساسي / primary text |
| accent | #FFB020 | estimated | التأكيد والإبراز / emphasis and highlights |
| muted | #8A93A6 | estimated | النص الثانوي والمحاور / secondary text and axes |
| line | #2A3346 | estimated | الخطوط والشبكات / strokes and grids |

### 4.2 الخطوط / Type

| الدور / Role | الخط / Family | الوزن / Weight | الحجم عند عرض 1080 px / Size at 1080 px width | ارتفاع السطر / Line height | الاتجاه / Direction |
|---|---|---|---|---|---|
| عنوان / Title | | 700 | 88–120 px | 1.15 | RTL |
| نص / Body | | 500 | 44–56 px | 1.4 | RTL |
| تسمية / Label | | 600 | 32–40 px | 1.2 | RTL |
| أرقام / Numerals | | 600 | 48–72 px | 1.0 | LTR inside RTL |

### 4.3 أوزان الخطوط المرسومة / Line weights

| العنصر / Element | السماكة / Stroke (px at 1080) | نهاية الخط / Cap | الزاوية / Join | مقاس أم مقدّر / Measured or estimated |
|---|---|---|---|---|
| مسار رئيسي / Primary path | 6 | round | round | estimated |
| مسار ثانوي / Secondary path | 3 | round | round | estimated |
| شبكة / Grid | 1.5 | butt | miter | estimated |

### 4.4 الإيزنج والتوقيت / Easing and timing

| الحركة / Motion | المنحنى / Curve | المدة / Duration (ms) | ملاحظة / Note |
|---|---|---|---|
| دخول / Entrance | cubic-bezier(0.22, 1, 0.36, 1) | 250–600 | |
| خروج / Exit | cubic-bezier(0.55, 0, 1, 0.45) | 200–400 | |
| تأكيد / Accent | cubic-bezier(0.34, 1.56, 0.64, 1) | 120–300 | overshoot على الكلمات المفتاحية / overshoot on key words |
| انتقال / Transition | cubic-bezier(0.65, 0, 0.35, 1) | 300–800 | |
| رسم المسار / Path draw | linear → ease-out | 400–1200 | بالتسلسل لا دفعة واحدة / sequential, never all at once |

### 4.5 الكاميرا / Camera

| اللقطة / Shot | الحركة / Move | المدى / Range | المنحنى / Curve | مقاس أم مقدّر / Measured or estimated |
|---|---|---|---|---|
| افتتاحية / Opening | push-in | 100% → 108% | ease-out | estimated |
| انتقال بين عناصر / Between elements | pan | ≤ 20% of frame | ease-in-out | estimated |
| ختام / Closing | pull-back | 105% → 100% | ease-in-out | estimated |

## 5. قواعد النص العربي / Arabic text rules

- يُعرض النص العربي RTL مع الحفاظ على اتصال الحروف؛ لا تُفكك الكلمة لتحريك حروفها، حرّك الكلمة أو السطر كوحدة.
- الأرقام والرموز اللاتينية داخل الجملة العربية تُعزل باتجاه LTR (bidi isolation).
- علامات الترقيم العربية (، ؛ ؟) تتبع اتجاه الجملة ولا تنعكس.
- Arabic renders RTL with joined letters; never split a word to animate its letters, animate the word or line as one unit.
- Latin numerals and symbols inside an Arabic sentence are isolated LTR (bidi isolation).
- Arabic punctuation follows the sentence direction and is never mirrored.

## 6. حدود الأمان على الهاتف / Phone-safe constraints

- هوامش آمنة 5% من كل جانب و 12% من الأعلى والأسفل في 9:16 (أشرطة الواجهة).
- أصغر حجم خط للنص المقروء 36 px عند عرض 1080 px؛ تحقق من المقروئية على معاينة بعرض 360 px.
- تباين النص على الخلفية ≥ 4.5:1.
- Safe margins of 5% on each side and 12% top and bottom in 9:16 (platform UI bars).
- Smallest readable text 36 px at 1080 px width; verify legibility on a 360 px wide preview.
- Text-to-background contrast ≥ 4.5:1.

## 7. ما لا يجوز / Do not

- لا شرائح ثابتة ولا انتقالات بلا سبب؛ كل عنصر له دخول وخروج وسبب حركي.
- لا نسخ لأي فيديو أو برومبت أو ميديا من المرجع؛ كل الأصول أصلية أو مرخّصة.
- لا تعديل في توقيت الصوت المرفق.
- No static slides and no unmotivated transitions; every element has an entrance, an exit and a reason to move.
- No copying of any video, prompt text or media from the reference; all assets are original or licensed.
- Never alter the timing of the supplied audio.
