# صيّاد الميديا — Media Hunter

بحث سريع في كتالوج فيه 615 موقع فيديو وصور وخامات وأيقونات للمونتاج، ومعاه بحث حي بالتوازي في 19 مصدر API (15 منهم شغالين من غير مفتاح). بيرجّع روابط ملفات حقيقية بدقتها ورخصتها، وتحميلها بأمر واحد بيسجّل المصدر كمان.

المحرك: `.claude/skills/kosif-black-dragon/tools/media_hunter/mh.py` (شغّله دايمًا بـ `python -I`، ومن جذر الريبو).

- **الكتالوج:** `tools/media_hunter/data/media_sites_615.csv`، ومعاه قوالب البحث في `tools/media_hunter/templates/out*.jsonl`.
- **الفهرس `catalog.db` والكاش (24 ساعة) و`last_results.json`:** بيتعملوا أوتوماتيك أول تشغيل في `~/.cache/kosif-media-hunter`. تقدر تغيّر المكان ده بـ `MH_CACHE`. الملفات دي مش بتتحفظ في git.
- **المخرجات (صفحات الروابط والتحميلات):** بتروح `out/media-hunter/`، أو المكان اللي في `MH_OUT`.
- **المتطلبات:** `httpx`، و`yt-dlp` لتحميل الأرشيف.

## الأمر الأساسي (استدعاء واحد)

```
python -I .claude/skills/kosif-black-dragon/tools/media_hunter/mh.py hunt "<english query>" --type video
```

- الأمر بيرجّع JSON فيه:
  - `results`: فيها `media_url` و`page_url` و`width`/`height` و`duration` و`license` و`source`، ورقم `n` بتستخدمه في التحميل.
  - `more_sites`: أنسب المواقع من الكتالوج، بروابط بحث جاهزة فيها الطلب نفسه.
- **ترجم طلب المستخدم لإنجليزي قصير ومحدد قبل ما تبعته.** مثلًا «جمل في الصحرا وقت الغروب» تبقى `camel desert sunset`. فيه قاموس عربي احتياطي.
- `--type`: `any` | `video` | `image` | `art` (متاحف CC0) | `hdri` | `texture` | `3d` | `icon` | `gif` | `wallpaper`
- الفلاتر: `--min-width 3840` (4K)، و`--orientation portrait` (ريلز 9:16)، و`--free`، و`--limit 30`، و`--per-source 15`.

## أوامر تانية

| الأمر | بيعمل إيه |
|---|---|
| `search "q" --type video` | زي hunt، بس بيطلّع جدول تقراه بعينك |
| `sites "q" [--type] [--free] [--json]` | أنسب المواقع من الكتالوج من غير نت (حوالي 40ms) |
| `links "q" [--type]` | صفحة HTML فيها روابط البحث في كل المواقع المناسبة |
| `get 1 4 7 -o "<مجلد الشغل>/footage"` | بيحمّل نتايج آخر hunt/search بأرقامها، وبيكتب `sources.txt` (المصدر والرابط والرخصة والمؤلف) |
| `keys` / `sources` | المصادر المفعّلة والمقفولة |
| `build` | بيعيد بناء الفهرس بعد ما تعدّل الكتالوج أو القوالب |

## المصادر الحية من غير مفتاح

- **فيديو:** Wikimedia Commons وNASA وInternet Archive وEuropeana.
- **صور:** Openverse وWikimedia وNASA وEuropeana وSmithsonian (`DEMO_KEY` العام) وWellcome.
- **فن ومتاحف CC0:** Art Institute Chicago وCleveland وV&A وSMK.
- **خامات وHDRI و3D:** Poly Haven وambientCG.
- **أيقونات وخلفيات:** Iconify (أيقونات) وWallhaven (خلفيات).

**المصادر المقفولة** هتفضل كده لحد ما تحط مفتاح مجاني في متغيرات البيئة أو في `keys.json`، والملف ده يتحط في مجلد الكاش أو جنب `mh.py`، ومتجاهَل في git (شوف `keys.example.json`). المصادر دي هي Pexels وPixabay، ودول أهم مصدرين لفوتيج ستوك 4K حديث، وكمان Unsplash وGIPHY.

## طريقة الشغل

1. شغّل `hunt` بطلب إنجليزي والنوع المناسب.
2. اعرض أحسن النتايج (المصدر والدقة والرخصة)، ومعاها من 3 لـ 5 مواقع من `more_sites`.
3. حمّل بـ `get` جوه مجلد الشغل، واتأكد من الملفات بـ ffprobe قبل ما تقول إنها اتحمّلت.
4. نبّه على الرخص المقيّدة: CC BY-NC، وBY-SA، و«حقوق محفوظة». ومحتوى Wallhaven حقوقه لأصحابه.
5. لو مصدر فشل، كمّل بالباقي. المصادر بتشتغل بالتوازي، ومهلة كل مصدر 8 ثواني.

## الفرق عن أدوات Superpowers

`free_photos.py` و`free_footage.py` و`stock_fetch.py` و`media_sources.py` لسه شغالين. الجديد هنا:

- كتالوج 615 موقع ببحث FTS بالعربي.
- متاحف CC0 (AIC وCleveland وV&A وSMK وSmithsonian وWellcome).
- Poly Haven وambientCG وIconify وWallhaven.
- بحث async متوازي بكاش.

بالمقابل، `stock_fetch.py` بيعمل scraping لـ Mixkit وCoverr، والمحرك ده لأ.
