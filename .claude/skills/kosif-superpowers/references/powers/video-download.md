# تحميل الفيديو من الروابط — Video download

> **قوتك هنا:** المستخدم يرسل روابط فيديوهات، فتحمّلها بنفسك وتدخلها في المونتاج. أصل الفكرة: سكربت المالك «Cinema C V32» (غلاف yt-dlp لـa-Shell على الآيفون) — أُعيدت كتابتها لـLinux وجُرّبت هنا.

#### DL-01 · تحميل فيديو من أي رابط · Download video from any URL · ✅ مُثبت هنا
- **ماذا / what:** yt-dlp يدعم مئات المواقع (YouTube, TikTok, Instagram, Facebook, X, Vimeo, archive.org…) — تعطيه رابطًا فيعطيك ملفًا جاهزًا للمونتاج.
- **كيف / how:** python3 scripts/fetch_video.py URL [URL…] -o clips/ --quality 1080 ؛ سلسلة بدائل: bv*+ba/b ← bv*+ba/b/best ← إعادة بمحاكاة متصفح (Safari/Chrome عبر curl_cffi). 8 أجزاء متوازية، 10 إعادات.
- **أرقام / params:** --concurrent-fragments 8 · --retries 10 · --socket-timeout 30 · -o '%(title).120B [%(id)s].%(ext)s'
- **تثبيت / install:** `pip install yt-dlp curl_cffi`
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/scripts/fetch_video.py` · `owner-upload:8cc9be77-c32.sh (Cinema C V32)`

#### DL-02 · قائمة روابط دفعة واحدة · Batch of links from a file · ✅ مُثبت هنا
- **ماذا / what:** أرسل المستخدم روابط كثيرة؟ ضعها في ملف نصي وحمّلها كلها، مع manifest.json يسجل كل ملف.
- **كيف / how:** python3 scripts/fetch_video.py --urls links.txt -o clips/ ؛ سطور تبدأ بـ# تُتجاهل؛ الخروج غير صفري إن فشل رابط.
- **أرقام / params:** manifest.json: url,file,duration,width,height,fps,vcodec,acodec,title,uploader,license
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/scripts/fetch_video.py`

#### DL-03 · جودة محددة أو صوت فقط · Quality cap or audio-only · ✅ مُثبت هنا
- **ماذا / what:** اختر السقف: 2160/1080/720/480 أو best، أو استخرج الصوت m4a فقط (للتفريغ أو الموسيقى المرجعية).
- **كيف / how:** --quality 720 ← bv*[height<=720]+ba ؛ --quality audio ← -x --audio-format m4a
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/scripts/fetch_video.py`

#### DL-04 · نسخة آمنة للمونتاج · Edit-safe H.264/AAC copy · ✅ مُثبت هنا
- **ماذا / what:** بعض الملفات (ogv/webm/vp9/av1/متغير الإطارات) تتعب المحررات؛ --safe يبني نسخة H.264+AAC+yuv420p+faststart مضمونة، ويحتفظ بالأصل.
- **كيف / how:** --safe ← ffmpeg -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart (أصل Cinema C Photos-SAFE)
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/scripts/fetch_video.py` · `owner-upload:8cc9be77-c32.sh`

#### DL-05 · كوكيز للمحتوى الخاص · Cookies for private / age-gated posts · 🟢 جاهز
- **ماذا / what:** للمنشورات الخاصة أو المقيّدة بالعمر من حساب المستخدم نفسه: ملف cookies.txt بصيغة Netscape يصدّره المستخدم من متصفحه.
- **كيف / how:** --cookies cookies.txt ؛ لا تحفظ الكوكيز في المستودع ولا تطبعها ولا تُرسلها لأحد؛ تخص حساب المستخدم فقط.
- **الدليل / proof:** `owner-upload:8cc9be77-c32.sh`

#### DL-06 · محاكاة متصفح عند الحظر · Browser impersonation retry · 🟢 جاهز
- **ماذا / what:** إن رفض الموقع الطلب العادي، يعيد المحاولة مرة واحدة كأنه Safari أو Chrome (يحتاج curl_cffi).
- **كيف / how:** --impersonate safari|chrome ؛ يُكتشف تلقائيًا من --list-impersonate-targets
- **تثبيت / install:** `pip install curl_cffi`
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/scripts/fetch_video.py` · `owner-upload:8cc9be77-c32.sh`

#### DL-07 · تحديث yt-dlp عند تغيّر الموقع · Update yt-dlp when a site breaks · ✅ مُثبت هنا
- **ماذا / what:** أغلب أخطاء TikTok/Instagram تُحل بتحديث yt-dlp.
- **كيف / how:** python3 scripts/fetch_video.py --update ؛ --doctor يفحص yt-dlp وffmpeg والمحاكاة
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/scripts/fetch_video.py`

#### DL-08 · حدود هذه الحاوية السحابية · Limits of this cloud container · 📄 موصوف
- **ماذا / what:** جُرّب هنا: archive.org يعمل بالكامل؛ يوتيوب يعطي البيانات لكن 403 عند تحميل الفيديو (عنوان خادم سحابي)؛ Vimeo يطلب تسجيل دخول؛ ويكيميديا 403. على جهاز المستخدم أو بكوكيز تعمل المواقع الكبرى عادة.
- **كيف / how:** إن فشل الرابط هنا: اطلب من المستخدم رفع الملف، أو شغّل السكربت على جهازه ثم يرفع الناتج.
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/references/video-download.md`

#### DL-09 · المصدر ثم الاستخدام: ترخيص وحقوق · Rights check before editing · 📄 موصوف
- **ماذا / what:** manifest يسجّل حقل license إن كشفه الموقع (مثلًا Public Domain في archive.org). التحميل لمحتوى المستخدم أو المرخّص؛ لا إعادة نشر لمقاطع الغير بلا إذن؛ اذكر المصدر.
- **كيف / how:** اقرأ license وuploader من manifest.json، واذكرهما في STYLE.md وفي تسليم الفيلم.
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/scripts/fetch_video.py`

#### DL-10 · من الرابط إلى المونتاج · Link → analyse → montage · 🟢 جاهز
- **ماذا / what:** سلسلة كاملة: حمّل ← --safe ← قِس المدة والقطعات (scenedetect/ffmpeg scene) ← فرّغ الصوت (faster-whisper) ← قص على الإيقاع (librosa) ← انتقالات xfade وتلوين وترجمة عربية ← loudnorm -14 ← verify_video.
- **كيف / how:** انظر proofs/ffmpeg-montage وفصل FOOT وSYNC وTRANS.
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/references/video-download.md`

## إضافات مرفقات 2026-10-23 — 2026-10-23 upload additions

_من مراجعة مرفقات المالك: [owner-uploads-review-20261023.md](../owner-uploads-review-20261023.md). — From the owner-upload review._


#### DL-11 · سجل سلسلة Cinema C للآيفون · Cinema C iPhone lineage ledger (V13 → V34) · 📄 موصوف / documented
- **ماذا / what:** أداة واحدة عبر 17 نسخة: c ← رابط ← جودة ← تحميل ← MP4 آمن للآيفون ← الصور. السجل يحفظ ما تعلمته كل نسخة: V17 تتبع الملف الدقيق، V22 تحقق صارم (ffprobe + فك إطار + حجر Unverified + إصلاح آخر ملف)، V24 إزالة ffprobe و--print-to-file لأنها جمّدت a-Shell ورفض التخمين حين يكتمل أكثر من ملف، V25 نسخة PhotosSafe (H.264 VideoToolbox ثم libx264، AAC، yuv420p، faststart) بفحص فك إطار واحد، V26–V28 حصر ملف فيسبوك بأفضل جهد مع download-archive. — One tool across 17 versions; the ledger keeps what each version learned so V34 changes do not repeat paid mistakes.
- **متى أستخدمها / when:** حين تعدّل سكربت التحميل للآيفون أو يفشل الحفظ في الصور / when changing the iPhone downloader or a save-to-Photos fails
- **كيف / how:** اقرأ §3 من الملحق قبل تعديل tools/a-shell/Cinema_C_V34_Studio_iPhone.sh؛ لا تُعد last_output.txt (V24)؛ فيسبوك لملفك أو محتوى تملك حقه فقط، والكوكيز تبقى على الجهاز. **أرقام / params:** PhotosSafe: -c:v h264_videotoolbox -b:v 6000k || libx264 -crf 18 -preset veryfast; -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart; sanity: -frames:v 1 -f null
- **الرخصة / license:** owner
- **الدليل / proof:** `kosif-tool/.claude/skills/kosif-superpowers/references/owner-uploads-review-20261023.md`
