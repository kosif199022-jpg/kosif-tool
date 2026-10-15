# PLAN.md — {style_name}

> الاستايل: `{id}` · المخرج: {aspect} · {resolution} · {fps} fps · {duration} s ({frames} إطار) · تاريخ الإنشاء: {date}
> Style: `{id}` · Deliverable: {aspect} · {resolution} · {fps} fps · {duration} s ({frames} frames) · Created: {date}

## 1. الملخص / Summary

| البند / Item | القيمة / Value |
|---|---|
| الفكرة في جملة / One-line concept | |
| المادة المصدرية / Source material | |
| الساعة الرئيسية / Master clock | الصوت المرفق إن وُجد، وإلا فهذا الجدول / supplied audio when present, otherwise this table |
| المرجع / Reference | {page} |
| الدلائل / Playbooks | {playbooks} |
| التقنية / Stack | {stack} |

## 2. جدول المشاهد / Scene table

قواعد الجدول / Table rules:
- الأزمنة بالثواني من بداية الفيديو؛ لا فجوات ولا تداخل إلا في مدة الانتقال.
- كل مشهد له حركة واحدة واضحة على الأقل؛ "عرض نص" وحده ليس حركة.
- آخر مشهد ينتهي عند {duration} s تمامًا.
- Times are seconds from the start; no gaps and no overlap except the transition itself.
- Every scene has at least one clear motion; "show text" alone is not a motion.
- The last scene ends exactly at {duration} s.

| # | البداية / Start (s) | النهاية / End (s) | الحركة / Action | الكاميرا / Camera | الانتقال / Transition | الإشارة الصوتية / Audio cue | الأصول / Assets |
|---|---|---|---|---|---|---|---|
| 1 | 0.00 | | | | | | |
| 2 | | | | | | | |
| 3 | | | | | | | |
| 4 | | | | | | | |
| 5 | | {duration} | | | | | |

مفاتيح / Keys:
- الكاميرا / Camera: static · push-in · pull-back · pan · tilt · orbit · rack-focus
- الانتقال / Transition: cut · wipe · morph · mask-reveal · zoom-through · match-cut · dissolve
- الإشارة الصوتية / Audio cue: كلمة مفتاحية أو نبضة إيقاع أو مؤثر صوتي مع زمنه / a key word, a beat or an SFX with its time

## 3. توقيت الكلمات / Word timing

المصدر: `words.json` في هذا المجلد (مُفرّغ من الصوت المرفق). كل كلمة لها بداية ونهاية بالثواني؛ الكلمات المفتاحية تحمل `emphasis: true` وتقود لحظات التأكيد.
الهدف: انحراف ≤ 100 ms بين بداية الكلمة المفتاحية ولحظة الحركة المرتبطة بها.
Source: `words.json` in this folder (transcribed from the supplied audio). Every word has a start and an end in seconds; key words carry `emphasis: true` and drive the accent moments.
Target: ≤ 100 ms offset between a key word's start and its linked motion.

| الكلمة / Word | البداية / Start (s) | النهاية / End (s) | المشهد / Scene | تأكيد / Emphasis | الحركة المرتبطة / Linked motion |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |
| | | | | | |

قواعد / Rules:
- لا تُحرَّك الكلمة قبل سماعها؛ يُسمح بتقديم بصري حتى 80 ms فقط.
- الكلمة العربية تظهر كاملة متصلة الحروف، ويُحرَّك السطر أو الكلمة لا الحرف.
- A word never animates before it is heard; a visual lead of at most 80 ms is allowed.
- An Arabic word appears whole with joined letters; animate the line or the word, never the letter.

## 4. مكتبة الانتقالات المستخدمة / Transitions used

| الاسم / Name | المدة / Duration (ms) | المنحنى / Curve | أين / Where used |
|---|---|---|---|
| | | | |

## 5. قائمة الأصول / Assets checklist

| الأصل / Asset | النوع / Kind | المصدر / Source | الترخيص / License | جاهز / Ready |
|---|---|---|---|---|
| | | original / licensed | | [ ] |

## 6. خطة الرندر / Render plan

1. معاينة: لوحة إطارات (9–12 إطارًا) + مقطع قصير 3–5 ثوانٍ من أصعب مشهد. / Preview: a contact sheet (9–12 frames) + a 3–5 s clip of the hardest scene.
2. موافقة المستخدم على المعاينة قبل الرندر الكامل. / User approval of the preview before the full render.
3. الرندر النهائي: {resolution}، {fps} fps، H.264 MP4 مع AAC؛ الصوت الأصلي دون تعديل. / Final render: {resolution}, {fps} fps, H.264 MP4 with AAC; the original audio untouched.
4. تعبئة TEST_REPORT.md بالقيم المقاسة. / Fill TEST_REPORT.md with measured values.
5. تسليم الملفات المصدرية القابلة للتعديل مع الفيديو. / Deliver the editable sources with the video.
