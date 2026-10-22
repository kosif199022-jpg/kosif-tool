# دعاء يوم الخميس — 22 أكتوبر 2026 · سجل القرارات

- المصدر: https://vt.tiktok.com/ZSgUXFhnA/ — فيديو المستخدم (@OAUN.11)، مدته 24.8 ث، 720×1280، بمعدل 30 إطارًا في الثانية
- الصوت: يُحفظ كما هو بلا أي تعديل (`source/audio_original.m4a`). جهارته الحالية −14.3 LUFS وذروته −0.3 dBFS
- التفريغ: `source/words_raw.json` (43 كلمة بتوقيتاتها، نموذج faster-whisper medium)
- التاريخ: الخميس 22 أكتوبر 2026، ويقابله 11 جمادى الأولى 1448 (بحساب أم القرى). الأصل كان 08.10.2026 = 27 ربيع الثاني
- المقاس: 9:16 (1080×1920)
- اللقطات: مساجد وإضاءات وأجواء صباحية، من مصادر مجانية فقط (Mixkit مؤكد)
- النص على الشاشة: التاريخ + كلمات الدعاء متزامنة مع الصوت + @kosif (عدّله المستخدم من @OAUN.11)
- الخطوط: توليفة إبداعية برخص مفتوحة (يختارها Claude)
- Higgsfield Katana: للتحليل فقط، بلا أي توليد صور أو فيديو
- الخطة المعتمدة: B «نور الكلمة» (21-10-2026)
- الحالة: تم الرندر والتسليم، والتقرير في TEST_REPORT.md
- تعديل 1: لقطة سقف المسجد (15694) استُبدلت بلقطة سجود داخل مسجد (34223) لأنها كانت ملتبسة؛ والاسم صار @kosif

## إزالة الملفات المشتقة / derived files removed (2026-10-22)

بقرار المالك أُزيلت من الريبو العام الملفات المشتقة من صوت أو فيديو حسابات أخرى (نص مفرّغ بتوقيت الكلمات، كلمات الأغنية، ورقة إطارات المصدر). تبقى محليًا فقط وصارت متجاهَلة في `.gitignore`. لإعادة توليد التوقيت محليًا: `python3 .claude/skills/kosif-superpowers/scripts/montage_pro.py transcribe <audio> --out out/<job>/words.json`.
By the owner's decision, files derived from other accounts' audio or video (word-timed transcripts, lyrics, source contact sheets) were removed from the public repo; they stay local only and are now git-ignored. The film HTML that loaded them needs a regenerated words file next to it.
