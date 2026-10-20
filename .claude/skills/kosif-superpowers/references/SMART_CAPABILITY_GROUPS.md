# KOSIF unified capability groups

Source: 5,296 powers / 62 families / 15 integrated-domain candidates.

> These are navigation/integration **candidates**, not evidence that all tools were merged into one runtime.

| Group | Arabic | Powers | Families |
|---|---|---:|---:|
| `research` | البحث والمعرفة | 54 | 3 |
| `thinking` | التفكير والتخطيط والاستراتيجية | 291 | 8 |
| `agents` | الوكلاء والتوجيه الذكي | 141 | 3 |
| `software` | البرمجة وبناء التطبيقات | 525 | 6 |
| `drawing` | الرسم والأشكال والتصميم | 297 | 5 |
| `images` | الصور والتحرير والتوليد | 296 | 5 |
| `3d` | الثري دي والمحاكاة والرندر | 754 | 5 |
| `motion` | الموشن والمونتاج والسينما | 1,224 | 7 |
| `audio` | الصوت والموسيقى والتعليق | 420 | 3 |
| `type` | الخطوط والنصوص العربية واللاتينية | 210 | 3 |
| `data` | البيانات والرسوم والمواقع | 253 | 4 |
| `documents` | المستندات والكتابة | 110 | 4 |
| `quality` | الاختبارات والجودة والأمان | 453 | 4 |
| `reverse` | التحليل العكسي وفحص البرامج | 241 | 1 |
| `misc` | قدرات مساندة غير مصنفة | 27 | 1 |

## Integration approach

Keep all original IDs, statuses, requirements and proofs. Use a common entrypoint per group while testing actual component interoperability. No deletion of originals before regression tests.

## Workflows (design targets, not yet tested)

### البرمجة وبناء التطبيقات (`software`)
التصميم → البرمجة → الاختبار → النشر

### الرسم والأشكال والتصميم (`drawing`)
الخطوط والمسارات → الأشكال والهندسة → الدمج في مشهد/لوحة → التصدير والتحقق

### الصور والتحرير والتوليد (`images`)
استيراد الصورة → التحرير والتلوين → التوليد الاختياري → تصدير النتيجة

### الثري دي والمحاكاة والرندر (`3d`)
إنشاء/استيراد المجسم → الخامات والإضاءة → المحاكاة/التحريك → الرندر والتحقق

### الموشن والمونتاج والسينما (`motion`)
القصة والستوريبورد → التوقيت والكاميرا → التحريك والمونتاج → التصدير

### الصوت والموسيقى والتعليق (`audio`)
المعالجة → المزامنة → التعليق والترجمة → التحقق

### البيانات والرسوم والمواقع (`data`)
الاستيراد والتنظيف → التحليل → الرسم والخرائط → التصدير

### الاختبارات والجودة والأمان (`quality`)
الجرد → التقييم → اختبارات الانحدار → إثبات النتائج

