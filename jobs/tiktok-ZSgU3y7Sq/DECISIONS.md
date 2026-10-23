# دعاء «اللهم إني أتبرأ من حولي وقوتي» — الحرم المكي تحت المطر · سجل القرارات

- المرجع: https://vt.tiktok.com/ZSgU3y7Sq/ — صاحبه **@ali1.697** (قناة «قــــران»)، وليس حساب المستخدم. مدته 47 ث، 720×1280، نُشر 15-10-2026
- أسلوب المرجع: لقطات هادئة للكعبة والحرم وبرج الساعة، كاميرا بطيئة، انتقالات ناعمة، نص أبيض صغير بخط نسخ مشكول في منتصف الشاشة يظهر جملة جملة، ومطر على الكعبة ليلًا في آخره ثم إظلام
- الصوت: −13.0 LUFS، ذروته −3.1 dBFS. التفريغ بنموذج large-v3 في `source/words_large.json`، وفيه آية الأحقاف 15 (﴿رَبِّ أَوْزِعْنِي…﴾) تحتاج نصها المضبوط
- مصادر اللقطات: Mixkit وCoverr لا يوجد فيهما الحرم؛ Vecteezy معاينات بعلامة مائية؛ Pexels وPixabay متاحان عبر API بمفتاح مجاني فقط؛ Wikimedia محجوب مؤقتًا (429)
- مفتاح Pexels غير متاح: إصدار المفاتيح الجديدة متوقف من Pexels (لقطة شاشة من المستخدم، 21-10-2026). البدائل: يرفع المستخدم اللقطات بنفسه، أو أنيميشن مرسوم
- الحل: Claude يحمّل من Pexels مباشرة برقم الفيديو (رابط التحميل العام، بلا مفتاح)، والأرقام من بحث الويب. حمّل 17 لقطة (`build/pexels_urls.txt`)، منها 14 للحرم، ومطر حقيقي على خلفية سوداء (36344044) يُدمج فوق اللقطات
- الخطة المعتمدة: B «مطر الرحمة» مع الاقتراحات (الصوت مع ذكر @ali1.697، Amiri، الجمعة 23.10.2026 · 12 جمادى الأولى 1448، @kosif)
- الحالة: تم الرندر والتسليم، والتقرير في TEST_REPORT.md

## إزالة الملفات المشتقة / derived files removed (2026-10-22)

بقرار المالك أُزيلت من الريبو العام الملفات المشتقة من صوت أو فيديو حسابات أخرى (نص مفرّغ بتوقيت الكلمات، كلمات الأغنية، ورقة إطارات المصدر). تبقى محليًا فقط وصارت متجاهَلة في `.gitignore`. لإعادة توليد التوقيت محليًا: `python3 .claude/skills/kosif-superpowers/scripts/montage_pro.py transcribe <audio> --out out/<job>/words.json`.
By the owner's decision, files derived from other accounts' audio or video (word-timed transcripts, lyrics, source contact sheets) were removed from the public repo; they stay local only and are now git-ignored. The film HTML that loaded them needs a regenerated words file next to it.
