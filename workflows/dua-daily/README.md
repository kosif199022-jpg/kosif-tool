# دعاء اليوم — قالب قصة يومية (1080×1920)

قالب متحرّك لدعاء كل يوم: اسم اليوم بخط رقعة فضي، اليوم والشهر الهجري (أم القرى) محسوبان من التاريخ، التاريخ الميلادي، قوس ذهبي وشمعة بلهب حي، ونص الدعاء يظهر سطراً سطراً على توقيت الصوت.

## الاستعمال

```bash
# 1) اكتب الإعداد: التاريخ والسطور بأوقاتها (ثوانٍ) والعلامة المائية ومسار الصوت
cp workflows/dua-daily/config_example.json my_dua.json

# 2) ابنِ صفحة المشهد
python3 workflows/dua-daily/scripts/dua_daily.py build my_dua.json --job out/dua-today

# 3) راجع لقطة لكل سطر قبل الإخراج
python3 workflows/dua-daily/scripts/dua_daily.py stills --job out/dua-today

# 4) أخرج الفيديو (معيار التصدير: 1080×1920، 30 إطار، H.264 High CRF 17، الصوت منسوخ كما هو)
python3 workflows/dua-daily/scripts/dua_daily.py render --job out/dua-today --out out/dua-today/dua.mp4
```

حقول الإعداد:

| الحقل | المعنى |
|---|---|
| `date` | التاريخ `YYYY-MM-DD`؛ منه اسم اليوم والتاريخ الهجري |
| `segments` | `[{start, end, text}]` بالثواني، متصاعدة؛ `\n` يكسر السطر |
| `watermark` | نص العلامة المائية فوق الشمعة |
| `audio` | ملف الصوت (اختياري)؛ يُنسخ دون إعادة ترميز إن كان AAC/MP3 |
| `dayLabel`, `hijriDay`, `hijriMonth` | تجاوز يدوي إذا اختلفت رؤية الهلال عن أم القرى |

المدة = نهاية آخر سطر. المشهد يُرسم على لوحة 720×1280 بكثافة 1.5، فالنص حاد عند 1080×1920.

## كيف يعمل

`template.html` لوحة canvas تُرسم كلها من دالة `render(t)`، و`build` يحقن الإعداد في الصفحة. المحرّك `tools/render_html.cjs` يزور كل إطار بـ `window.__kosif.seek(t)` بعد `window.__kosifReady` (تحميل الخطوط)، فالإخراج حتمي إطاراً بإطار، ثم يتحقق من المدة والإطارات والمقاس وبصمة الصوت (`VERIFY OK ... audio_md5=match`).

لخط تجاري تملكه: ضع ملف TTF في `fonts/` وغيّر `@font-face` في `template.html`.

## الأصل

مولّد رفعه صاحب المستودع (`dua_video_generator`، كان يعمل بـ Python Playwright بمقاس 720×1280). نُقل هنا إلى محرّك المستودع بمعيار التصدير الكامل. الخطوط في [CREDITS.md](CREDITS.md).
