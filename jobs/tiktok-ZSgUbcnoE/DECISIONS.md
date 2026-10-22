# دعاء يوم الخميس (2) — سجل القرارات

- المصدر: https://vt.tiktok.com/ZSgUbcnoE/ (@oaun.11، نُشر 21-10-2026)، مدته 27.1 ث، 720×1280، 30 إطارًا في الثانية
- الصوت: جهارته −19.5 LUFS وذروته −5.8 dBFS (أخفض من معيار تيك توك)
- النص: يبدأ بآية {وَلَسَوْفَ يُعْطِيكَ رَبُّكَ فَتَرْضَىٰ} (الضحى 5)، ثم الدعاء. التفريغ الآلي في `source/words_raw.json`، ولازم تصحيح الآية بنصها المضبوط
- طلب المستخدم: لقطات واضحة، فلا شيء يغطي اللقطة أو يجعلها غير واضحة. إبداع في الحركة والانتقالات والخطوط
- القرارات (اعتمدها المستخدم بـ«زي ما انت عايز»): الخطة B «خط النور»؛ رفع الصوت +5 dB بالتساوي فقط؛ التاريخ 22.10.2026 · ١١ جمادى الأولى ١٤٤٨ هـ؛ الاسم @kosif؛ لقطات مساجد وصباح ومعنى الكلام؛ الآية بخط مميز وتشكيل كامل
- التصميم: لوحة فيديو صافية 1000×926 بإطار ذهبي، والنص خارجها؛ المؤثرات وقت الانتقالات فقط
- الحالة: تم الرندر والتسليم، والتقرير في TEST_REPORT.md

## إزالة الملفات المشتقة / derived files removed (2026-10-22)

بقرار المالك أُزيلت من الريبو العام الملفات المشتقة من صوت أو فيديو حسابات أخرى (نص مفرّغ بتوقيت الكلمات، كلمات الأغنية، ورقة إطارات المصدر). تبقى محليًا فقط وصارت متجاهَلة في `.gitignore`. لإعادة توليد التوقيت محليًا: `python3 .claude/skills/kosif-superpowers/scripts/montage_pro.py transcribe <audio> --out out/<job>/words.json`.
By the owner's decision, files derived from other accounts' audio or video (word-timed transcripts, lyrics, source contact sheets) were removed from the public repo; they stay local only and are now git-ignored. The film HTML that loaded them needs a regenerated words file next to it.
