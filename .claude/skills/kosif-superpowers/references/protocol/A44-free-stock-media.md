# A44 · صور وفيديو مجانية للمونتاج (USIP v6.0)

> **متى تقرأه / when to read:** أي طلب لقطات أو صور مجانية أو «بدون حقوق» أو مفتوحة الترخيص، خلفيات أو B-roll لمونتاج أو ريلز، أو سؤال «أي موقع مجاني يسمح بالاستخدام التجاري؟» · [العودة إلى النواة / back to the core](../../PROTOCOL.md#متى-تفتح-الملاحق--appendix-triggers)

الفكرة: من أي محادثة، ندوّر في المواقع المجانية عن فيديو وصور تخدم المونتاج، ونحمّل كل ملف **ومعاه ترخيصه وسطر النسب**، بدل ما نجيب ملفات مجهولة الحقوق.

## 1. الأداتان (من جذر المستودع)

| النوع | الأداة | ابدأ بـ |
|---|---|---|
| فيديو (لقطات، B-roll) | `scripts/free_footage.py` (17 موقعًا في `data/free_footage_sources.json`) | `python3 .claude/skills/kosif-superpowers/scripts/free_footage.py search "night city" --orientation portrait --limit 6` |
| صور (خلفيات، لوحات، مخطوطات، فضاء) | `scripts/free_photos.py` (7 مصادر) | `python3 .claude/skills/kosif-superpowers/scripts/free_photos.py search "desert dunes" --orientation portrait --commercial` |

نفس المسار للاثنين: **search ← معاينة ← download ← ATTRIBUTION.md**.

1. `search "<كلمات إنجليزي>"`: النتائج تتجمّع في `out/free-footage/last_search.json` أو `out/free-photos/last_search.json` (بحث جديد لا يمسح القديم).
2. معاينة قبل التحميل: `free_footage.py preview` (ورقة لقطات) أو `free_photos.py sheet` (صفحة صور)، واستبعد ما فيه وجوه أو كتابة أو شعارات لا تريدها.
3. `download <id>... --out <مجلد المهمة>/stock`: كل ملف ومعه `<الملف>.json` فيه الترخيص وسطر النسب والبصمة.
4. `ATTRIBUTION.md` في نفس المجلد يتحدّث تلقائيًا: انسخ منه أسطر النسب للوصف أو آخر الفيديو.

روابط الصفحات المباشرة (Pexels وMixkit وPixabay وCoverr وكل ملف `.mp4`) تمر بـ `scripts/fetch_video.py` و`scripts/stock_fetch.py` كما في [A19](A19-field-lessons-montage.md).

## 2. المصادر

**فيديو** (التفاصيل الكاملة: `free_footage.py sources`):

| الموقع | بلا مفتاح؟ | الترخيص | النسب | تجاري |
|---|---|---|---|---|
| Mixkit | نعم | Free أو Restricted حسب اللقطة | غير لازم | Free نعم، Restricted لا |
| Coverr | نعم | Coverr License | غير لازم | نعم |
| Wikimedia Commons | نعم | لكل ملف (CC0، ملك عام، CC BY/BY-SA) | غالبًا لازم | حسب الملف |
| Internet Archive | نعم | ادعاء الرافع (يُعلَّم المشكوك فيه) | لازم | حسب الملف |
| NASA | نعم | إرشادات ناسا | اذكر ناسا | نعم بلا إيحاء بالتأييد |
| مكتبة الكونجرس (v6.5) | نعم | ملكية عامة في أمريكا: الأداة بتاخد بس الأفلام المنشورة لحد 1930 (سنة 2026) | اختياري (سطر المكتبة مفضّل) | نعم، وافحص الحماية برا أمريكا (`check-abroad`) |
| Europeana (v6.5) | `EUROPEANA_API_KEY` مجاني | لكل كليب: PD أو CC0 أو CC BY أو CC BY-SA بس | لازم لـ BY | نعم؛ ملفات مباشرة بس، روابط يوتيوب بتتساب |
| Pexels / Pixabay | مفتاح مجاني | Pexels License / Pixabay Content License | غير لازم | نعم |

**صور** (`free_photos.py sources`):

| المصدر | بلا مفتاح؟ | الترخيص | النسب | ملاحظة |
|---|---|---|---|---|
| Openverse | نعم | لكل صورة: CC BY، BY-SA، CC0، PDM | لازم لـ BY | محرك فوق 800 مليون صورة، الترخيص كما يعلنه الموقع الأصلي |
| Wikimedia Commons | نعم | لكل ملف | غالبًا لازم | أماكن وتاريخ وطبيعة |
| NASA Images | نعم | إرشادات ناسا | اذكر ناسا | فضاء والأرض من المدار |
| The Met Open Access | نعم | CC0 | غير لازم | فن إسلامي ومخطوطات وخط وآثار (الملك العام فقط) |
| Pexels | `PEXELS_API_KEY` | Pexels License | غير لازم | صور حديثة وطولية كثيرة |
| Pixabay | `PIXABAY_API_KEY` | Pixabay Content License | غير لازم | حتى 1280 بكسل عبر الـ API |
| Unsplash | `UNSPLASH_ACCESS_KEY` | Unsplash License | شروط الـ API تطلبه | الأداة تبلّغ Unsplash بكل تحميل كما تشترط، وتتخطى Unsplash+ المدفوع |

المفاتيح مجانية من صفحات المطورين (pexels.com/api، pixabay.com/api/docs، unsplash.com/developers) وتوضع في متغيرات بيئة الجلسة، **ولا تُلصق في المحادثة أبدًا**. بدونها تعمل المصادر المجانية بلا مفتاح.

## 3. قواعد الترخيص (إلزامية)

1. **الأداة تسجّل الترخيص ولا تمنحه.** ما في الـ sidecar هو ما يعلنه الموقع؛ في عمل مدفوع افتح `page_url` وتأكد.
2. **ND مرفوض افتراضيًا:** المونتاج تعديل، فالترخيص الذي يمنع التعديل لا يصلح (`--allow-nd` للمرجع فقط).
3. **عمل تجاري أو إعلان ← `--commercial`:** يستبعد NC وMixkit Restricted والتراخيص غير المؤكدة.
4. **الناس والعلامات التجارية:** ترخيص الصورة لا يعني موافقة الشخص الظاهر أو صاحب الشعار؛ في الإعلانات تجنّب الوجوه الواضحة والشعارات أو اطلب إذنًا.
5. **النسب:** كل سطر «required» في `ATTRIBUTION.md` يُكتب في وصف الفيديو أو نهايته؛ «optional» مستحب.
6. **Pinterest وإنستغرام ويوتيوب ليست مصادر ترخيص:** مرجع إلهام ورابط فقط.
7. **لا تجاوز:** صفحة تحقق Cloudflare أو 403 أو 429 تُبلَّغ كما هي ويُترك الموقع، ولا تغيير هوية المتصفح. اقترح جهاز المستخدم أو رفع الملف.

## 4. بلا مستودع أو بلا شبكة

ابحث بنفسك في روابط البحث (`https://mixkit.co/free-stock-video/discover/<كلمة>/`، `https://coverr.co/s?q=<كلمة>`، `https://www.pexels.com/search/videos/<كلمة>/`، `https://pixabay.com/videos/search/<كلمة>/`، `https://openverse.org/search/?q=<كلمة>`، `https://unsplash.com/s/photos/<كلمة>`، `https://commons.wikimedia.org/w/index.php?search=<كلمة>&title=Special:MediaSearch`) وأعطِ المستخدم جدولًا: الرابط، الترخيص، النسب، تجاري؟ ولا تقل «حمّلت» بلا ملف فعلي.

## 5. حالة الوصول المقاسة (30-10-2026 من الجلسة السحابية)

ناسا أجابت وحُمّلت صورة بترخيصها؛ ويكيميديا أجابت ثم حدّت المعدل (429)؛ واجهة متحف المتروبوليتان رفضت أحيانًا بجدار حماية (403)؛ وOpenverse لم تُجب (504). هذه المحوّلات مختبرة بلا شبكة في `evals/test_free_photos.py` وتعمل عادة من جهاز منزلي. أعد القياس قبل الادعاء.
