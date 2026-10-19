# TikPlayer — مشغل فيديو عمودي بالسحب (Android)

<div dir="rtl">

مشروع المالك، منقول من مجلد العمل كما هو (قدرة APPX-60 في `kosif-superpowers`). مشغل بأسلوب تيك توك لفيديوهات الجهاز: سحب عمودي بين المقاطع، تشغيل تلقائي، نقرتان للإعجاب، شريط تقدم رفيع. مفيد لمعاينة ريلز KOSIF على الهاتف كما ستظهر للمشاهد.

</div>

- Kotlin, `compileSdk 34`, `minSdk 26`, package `com.aghnam.tikplayer`.
- Libraries: `androidx.viewpager2` (vertical pager), `androidx.media3:media3-exoplayer` + `media3-ui`, RecyclerView, Material.
- Videos come from `MediaStore` (runtime read-media permission) or a picked file.

Build (not done in the session that imported it; the folder has no Gradle wrapper):

```bash
gradle wrapper --gradle-version 8.7
./gradlew assembleDebug
```

or open the folder in Android Studio. Needs JDK 17 and the Android SDK (`engine:android` in `data/requirements.json`).
