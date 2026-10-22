# «خلي ولي مدير 2» — أنيميشن وموشن جرافيك · سجل القرارات

- المصدر: https://vt.tiktok.com/ZSgU7HTXj/ — صاحبه **@mo7moneam (Mohamed Moneam)**، وليس حساب المستخدم. نُشر 21-10-2026، مدته 59 ث، 720×1280
- المحتوى: مشهد كوميدي في سيارة بين «المدير» (قميص أزرق وكرافتة ونظارة شمس) وشاب (تيشيرت وردي وكاب)، وأغنية بلهجة عربية مكسّرة
- الصوت: جهارته −16.4 LUFS وذروته −2.5 dBFS. التفريغ الآلي (`source/words_raw.json`) ضعيف في اللهجة
- الطلب: بلا لقطات حقيقية (حسب الفهم)، أنيميشن وموشن جرافيك بكل المهارات، و«تفعيل البوت كود» (غير محدد)
- القرارات: المستخدم أكّد إذن تيك توك لاستخدام الصوت؛ الصوت فقط بلا لقطات حقيقية؛ كاريكاتير المدير (نظارة وكرافتة) والشاب؛ الخطة B «كرتون العربية» (موافق)
- الكلمات: من faster-whisper large-v3 مع تنظيف يدوي للهجة (`build/lyrics.json`)
- الحالة: تم الرندر والتسليم، والتقرير في TEST_REPORT.md

## إزالة الملفات المشتقة / derived files removed (2026-10-22)

بقرار المالك أُزيلت من الريبو العام الملفات المشتقة من صوت أو فيديو حسابات أخرى (نص مفرّغ بتوقيت الكلمات، كلمات الأغنية، ورقة إطارات المصدر). تبقى محليًا فقط وصارت متجاهَلة في `.gitignore`. لإعادة توليد التوقيت محليًا: `python3 .claude/skills/kosif-superpowers/scripts/montage_pro.py transcribe <audio> --out out/<job>/words.json`.
By the owner's decision, files derived from other accounts' audio or video (word-timed transcripts, lyrics, source contact sheets) were removed from the public repo; they stay local only and are now git-ignored. The film HTML that loaded them needs a regenerated words file next to it.
