# تحميل الفيديو للمونتاج — Video download for montage

عندما يرسل المستخدم **روابط** فيديوهات، حمّلها بنفسك بـ`scripts/fetch_video.py` (غلاف yt-dlp) ثم اعمل بها المونتاج. الأفكار من سكربت المالك `Cinema C V32` (سلسلة بدائل الصيغ، إعادة بمحاكاة متصفح، كوكيز، نسخة آمنة للمحررات، تحديث yt-dlp، ومعمل صوت)؛ النسخة هنا مكتوبة من جديد لـLinux وليست نسخًا منه.

## الأوامر
```bash
pip install yt-dlp curl_cffi                      # مرة واحدة (ffmpeg مثبت أصلًا)
python3 scripts/fetch_video.py --doctor           # يفحص الأدوات
python3 scripts/fetch_video.py URL1 URL2 -o clips --quality 1080 --safe
python3 scripts/fetch_video.py --urls links.txt -o clips        # قائمة روابط
python3 scripts/fetch_video.py URL --quality audio              # صوت فقط m4a
python3 scripts/fetch_video.py URL --cookies cookies.txt        # محتوى خاص من حساب المستخدم
python3 scripts/fetch_video.py --update                         # عند تغيّر الموقع
```
الناتج: ملفات باسم `العنوان [المعرّف]` + `manifest.json` (المدة، الأبعاد، الإطارات، الترميز، العنوان، الرافع، الترخيص إن كشفه الموقع) + نسخة `.safe.mp4` عند `--safe`.

## ما جُرّب هنا (2026-10-16)
| الموقع | النتيجة |
|---|---|
| archive.org | ✅ تحميل كامل 26MB، 370 ث، مع ترخيص Public Domain في المانيفست، ونسخة آمنة H.264 |
| روابط خاطئة | ✅ تفشل برسالة واضحة والخروج غير صفري |
| YouTube | ⚠️ يقرأ البيانات، لكن تحميل الفيديو يعطي 403 من عنوان الخادم السحابي |
| Vimeo | ⚠️ يطلب تسجيل دخول (كوكيز) |
| Wikimedia Commons | ⚠️ 403 من هنا |
| TikTok / Instagram / Facebook | لم تُجرَّب روابط فعلية؛ الصفحات متاحة، ومحتاجة غالبًا تحديث yt-dlp أو كوكيز |

إن فشل رابط هنا: لا تدّعِ نجاحه. اطلب من المستخدم رفع الملف، أو أعطه الأمر ليشغّله على جهازه (يعمل غالبًا هناك) ثم يرفع الناتج.

## القواعد
- حمّل فقط محتوى للمستخدم أو مرخّصًا أو يملك حق استخدامه؛ اذكر المصدر والترخيص من المانيفست في `STYLE.md` والتسليم. لا تعِد نشر مقاطع الغير.
- الكوكيز تخص المستخدم: لا تُحفظ في المستودع ولا تُطبع ولا تُرسل لأي جهة.
- بعد التحميل: `--safe` ثم أكمل المسار: قياس المدة والقطعات ← تفريغ الصوت ← قص وانتقالات وتلوين ← ترجمة عربية ← loudnorm -14 ← `verify_video.py`.
- مهارة أخرى في سكربت المالك لم تُنقل بعد: «معمل الصوت» (فصل الصوت/الموسيقى بـDemucs عبر Replicate بمفتاح، وإزالة ضوضاء بنموذج arnndn) — موصوفة في الفصل music-beat-sound وتحتاج مفتاحًا.

## نسخة الآيفون / a-Shell — Cinema C V34 Studio (2026-10-17)
سكربت المالك مطوَّر في [`tools/a-shell/Cinema_C_V34_Studio_iPhone.sh`](../../../../tools/a-shell/Cinema_C_V34_Studio_iPhone.sh)، ويعمل كله داخل a-Shell بـffmpeg بلا libx264.
- **التحميل (V33):** نسخ بلا ترميز لملفات H.264/HEVC إلى الصور؛ سلسلة مشفّرات تُفحص قبل الاستخدام (VideoToolbox ← libx264 ← MPEG-4) تعالج خطأ `-12903`؛ سقف الجودة بـ`-S res:N` (الضلع الأقصر)؛ رابط من نص المشاركة أو الحافظة؛ كل ملفات المنشور؛ تحديث yt-dlp وإعادة المحاولة؛ `c --safe` و`c --doctor`.
- **V34:** جزء فقط من الفيديو (`--download-sections`)، ترجمة عربية/إنجليزية SRT مدمجة كـmov_text، `c --batch` مع حفظ الروابط الفاشلة، `c --history`.
- **الاستوديو `c --studio`** بوصفات من الكتالوج: قص بلا فقد أو دقيق، ضغط لحجم 16/25/50MB بمحاولة ثانية عند التجاوز، ريلز 9:16 بخلفية مموهة (FMT: gblur ثم boxblur ثم تصغير/تكبير)، GIF بميزانية 15MB (FMT palettegen)، غلاف JPG، جهارة -14 LUFS بمرورين (BEAT-01)، قص الصمت (silencedetect + select)، كتم، صوت فقط.
- **الاختبار:** في الحاوية بمحاكي ffmpeg يرفض libx264 وVideoToolbox، وyt-dlp وهمي لمسارات التحميل، ومكتبة yt-dlp الحقيقية لاختيار الصيغ. لم يُشغَّل على آيفون حقيقي.

## 100-source licensed media discovery — NEW

See [100 source websites and license checks](stock-media-100.md). Before acquiring stock for montage use `scripts/media_sources.py search` then `plan` and `download` with verified per-item `--rights` and `--evidence-url`. This builds an asset-level rights and SHA-256 manifest and reuses the current yt-dlp downloader. Never infer permissions merely because a site is indexed.
