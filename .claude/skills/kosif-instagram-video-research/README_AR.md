# KOSIF Instagram Video Research v1.0

مهارة للعثور على مراجع Reels حسب **موضوع الفيديو** بدل الاكتفاء باسم الحساب.

## المرجعان الجديدان
- https://www.instagram.com/asirgokerr/
- https://www.instagram.com/brkn.land/

الروابط جاءت من المستخدم. حاولنا فتح صفحاتهما مباشرة لكن الوصول العام فشل؛ لذلك لم نزعم مشاهدة كل فيديو أو معرفة تقنية إنتاجه. توجد نتائج عامة ثانوية لـ brkn.land عن السحاب والطبيعة والزهور والبحر والسماء الليلية، وإشارات لطبيعة/سفر من asirgokerr.

## ما الذي تنفذه الأداة؟
1. **Query understanding:** توسيع «غيوم» إلى clouds/cloudscape؛ «غروب» إلى sunset/golden hour.
2. **Search planning:** استعلامات مستهدفة للـReels العامة، استعلامات لكل من الحسابين، ورابط البحث داخل تطبيق Instagram (قد يتطلب تسجيل دخول).
3. **Optional automated discovery:** البحث في فهرس الويب العام عبر **Brave Search API** باستخدام `BRAVE_SEARCH_API_KEY` من البيئة، ثم حفظ الروابط العامة فقط.
4. **Local content reference index:** تخزين روابط الفيديوهات ووصفها ومصدرها ومستوى التحقق في SQLite مع إزالة التكرار.
5. **Ranking:** ترتيب نصي أولي للمراجع حسب التطابق والناشر المعروف عند توفره.
6. **Infinite Matrices handoff:** بعد التحقق بصريًا من الفيديو وبشكل قانوني، يصير مرجعًا بحثيًا لاستخراج آليات الحالة/العملية/القانون/الزمن/الذاكرة؛ لا نستنتجها من وصف فقط.

## التشغيل
```bash
python .claude/skills/kosif-instagram-video-research/instagram_research.py sources
python .claude/skills/kosif-instagram-video-research/instagram_research.py plan 'شلال وسط غابة'
python .claude/skills/kosif-instagram-video-research/instagram_research.py search 'غيوم' --accounts-only
python .claude/skills/kosif-instagram-video-research/instagram_research.py find 'غروب'
python -m unittest discover -s .claude/skills/kosif-instagram-video-research/tests -v
```

استخدم `BRAVE_SEARCH_API_KEY` في متغير بيئة فقط ولا تضعه في GitHub. بدون المفتاح تحصل على **روابط بحث، لا نتائج تم التحقق منها**.

## قيود صريحة
- ليس لدى Instagram Graph API بحث عام حر وشامل بكل مقاطع Reels بالكلمات. توجد إمكانات رسمية محدودة لملفات أعمال/منشئي محتوى مصرح لها وللوسوم حسب الصلاحيات. [Meta Instagram API](https://www.postman.com/meta/instagram/documentation/6yqw8pt/instagram-api).
- صفحات إنستجرام الخاصة أو غير المفهرسة لن تظهر في نتائج محرك الويب، وقد تتطلب الروابط تسجيل دخول.
- لا تنزيل قسري ولا نسخ أو إعادة نشر دون إذن أو حقوق مناسبة.
- البيانات المكتشفة من الويب **مؤشرات** وليست إثباتًا لتفاصيل الفيديو أو عدد المشاهدات أو أصالته.
- تحليل إطارات الفيديو/الصوت والبحث الدلالي الحقيقي يحتاج ملفات قانونية المصدر وتطويرًا لاحقًا.

## المرحلة القادمة
معالجة المرئيات المصرح بها: تحليل مشاهد ولقطات، Shot boundaries، حركة الكاميرا، palette، semantic embeddings وتخزين مجالات التصوير. ثم ربط نتائج الدراسة بمصفوفات الابتكار والقوانين السببية بدل تقليد المحتوى.

مرجع واجهة البحث المختارة: https://api-dashboard.search.brave.com/app/documentation/web-search
