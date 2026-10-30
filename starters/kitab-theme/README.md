# ثيم «كتاب» — حزمة نظام بصري للواجهات

لوحة دافئة مرساتها `#FBF4E1` مع سلّم قهوة للحبر وذهب للتأكيد، ووضع ليلي «مقهى الليل»، وخطوط عربية مستضافة محلياً (Alexandria للعناوين، IBM Plex Sans Arabic للمتن والأرقام، Amiri للاقتباس). التفاصيل الكاملة: [KITAB-THEME.md](KITAB-THEME.md).

## المحتوى

| الملف | الدور |
|---|---|
| `public/kosif-kitab-theme.css` | الرموز (`--kc-*`) والمكوّنات وشريط العلّامة والوضع الليلي و`@font-face` |
| `public/kosif-kitab-theme.js` | يُبقي الورقة آخر `<head>` ويلوّن `theme-color` حسب الوضع |
| `public/fonts/*.woff2` | الخطوط مقسّمة عربي/لاتيني، رخصتها في `public/fonts/OFL.txt` |
| `scripts/apply-kitab-theme.mjs` | يرحّل الألوان القديمة إلى الرموز (`--check`، `--revert`) |
| `scripts/wire-kitab-theme.mjs` | يوصل الثيم برؤوس الصفحات و`sw.js` (`--check`) |

## الاستعمال في أي موقع

انسخ `public/` إلى جذر الموقع (المسارات مطلقة: `/fonts/...` و`/kosif-kitab-theme.css`) ثم أضف في `<head>`:

```html
<link rel="stylesheet" href="/kosif-kitab-theme.css">
<script src="/kosif-kitab-theme.js" defer></script>
```

غيّر اللوحة من `:root` في ملف CSS وحده. السكربتان في `scripts/` مكتوبان لهيكل تطبيق Kosif (قائمة ملفات `public/v36*.css` و`src/suite-edge.js` وغيرها)، فعدّل القائمتين في أعلاهما قبل تشغيلهما على مشروع آخر، وشغّلهما بـ `--check` أولاً.

ملاحظة الدقة: المرساة `#FBF4E1` مأخوذة من وسم `theme-color` المنشور لـ kitabcaffe.com، وبقية السلّم والخطوط استنتاج بحسب الدور لا مطابقة بصرية.
