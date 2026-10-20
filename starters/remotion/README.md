# KOSIF Remotion Starter — قالب Remotion الأساسي

<div dir="rtl">

## بالعربية

قالب صغير وحقيقي لمشروع [Remotion v4](https://www.remotion.dev) جاهز للعمل مع أداة KOSIF.
يحتوي على تركيبة واحدة اسمها `KosifFilm` بقياس 1080×1920 (عمودي 9:16)، 30 إطاراً في الثانية، مدتها الافتراضية 12 ثانية، وثلاثة مشاهد:

1. **كشف العنوان**: كلمات العنوان تظهر واحدة تلو الأخرى بنابض (spring) متدرّج، ثم تتبعها كلمات مفتاحية على شكل أقراص.
2. **رسم بياني خطي SVG**: الخط يُرسم بـ `interpolate` عبر `stroke-dashoffset`، والنقاط تقفز بـ `spring` لحظة وصول القلم إليها، والرقم يعدّ تصاعدياً.
3. **بطاقة الشعار الختامية**: حلقة تُرسم حول علامة بسيطة، ثم العنوان وسطر الختام.

المشاهد الثلاثة تعيش داخل `CameraRig`: تحويل مجموعة واحد (translate + rotate + scale) يتحرك ببطء طوال الفيلم كأنه كاميرا. فوق كل ذلك طبقة **ترجمة على مستوى الكلمة** تقرأ `public/words.json` وتلوّن الكلمة الحالية بلون التمييز.

### الخصائص (props)

| الخاصية | النوع | المعنى |
|---|---|---|
| `title` | string | العنوان الرئيسي، يُقسَّم إلى كلمات ويظهر متدرّجاً ثم يُعاد في البطاقة الختامية |
| `words` | string[] | كلمات مفتاحية تظهر كأقراص تحت العنوان |
| `accent` | string | لون التمييز بأي صيغة CSS (يُفضَّل hex من ست خانات) |
| `lang` | `"ar"` أو `"en"` | يحدد اتجاه النص ونصوص الواجهة المدمجة |

### التثبيت

```bash
cd starters/remotion
npm install
```

### المعاينة

```bash
npm run preview
```

يفتح Remotion Studio في المتصفح على `http://localhost:3000` مع مخطط زمني وإمكانية تعديل الخصائص مباشرة.

### التصدير (render)

```bash
# بالخصائص الافتراضية
npm run render

# بخصائص مخصصة (JSON داخل السطر)
npx remotion render KosifFilm out/film.mp4 \
  --props='{"title":"تقرير الربع الثالث في دقيقة","words":["نمو","عملاء","إيرادات"],"accent":"#19c37d","lang":"ar"}'

# أو من ملف
npx remotion render KosifFilm out/film.mp4 --props=./props.example.json

# صورة ثابتة من إطار محدد
npm run still

# اختبار سريع لأول ثانية فقط
npx remotion render KosifFilm out/test.mp4 --frames=0-30
```

### الصوت كساعة رئيسية (master clock)

ضع ملف الصوت في `public/` (مثلاً `public/voice.mp3`) ثم افتح `src/Film.tsx` وغيّر:

```ts
const AUDIO_FILE: string = "voice.mp3";
```

هذا يضيف `<Audio src={staticFile("voice.mp3")} />` عند الإطار صفر، فتصبح أوقات `public/words.json` (بالثواني) محسوبة من بداية الصوت نفسه. لا تعدّل الصوت أبداً داخل القالب: الصورة تتبع الصوت وليس العكس.

لجعل **مدة الفيلم** تساوي مدة الصوت تلقائياً، ثبّت `@remotion/media-utils` واستخدم `calculateMetadata` في `src/Root.tsx`:

```bash
npm install @remotion/media-utils@4.0.535
```

```tsx
import { getAudioDurationInSeconds } from "@remotion/media-utils";
import { staticFile } from "remotion";

<Composition
  id="KosifFilm"
  /* ...الخصائص نفسها... */
  calculateMetadata={async () => {
    const seconds = await getAudioDurationInSeconds(staticFile("voice.mp3"));
    return { durationInFrames: Math.ceil(seconds * FPS) };
  }}
/>
```

أنشئ `public/words.json` من الصوت بأي أداة تفريغ تعطي أوقات الكلمات (مصفوفة من `{ "word", "start", "end" }` بالثواني). الترجمة تعرض الكلمات كاملة فقط، ولا تقسم الكلمة العربية أبداً.

### Chromium الموجود على الجهاز

لا يحتاج Remotion إلى تنزيل متصفح إذا وُجد Chromium محلياً. يبحث `remotion.config.ts` تلقائياً، بالترتيب، عن:

1. المتغير `KOSIF_BROWSER=/path/to/headless_shell`
2. نسخة `chromium_headless_shell-*` من Playwright تحت `$PLAYWRIGHT_BROWSERS_PATH` أو `/opt/pw-browsers` (الملف `chrome-linux/headless_shell`)
3. نسخة Chromium الكاملة `chromium-*` هناك كخيار أخير فقط

يشغّل Remotion المتصفح بأعلام headless الكلاسيكية، ونسخ Chromium الكاملة لم تعد تقبلها، لذلك استخدم headless shell. على هذا الجهاز مساره `/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell` (تحقق من الرقم بـ `ls /opt/pw-browsers/`). يمكنك أيضاً تمريره صراحة:

```bash
npx remotion render KosifFilm out/film.mp4 \
  --browser-executable=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
```

### الخطوط

قائمة الخطوط في `src/Film.tsx` و`src/Captions.tsx` تبدأ بخطوط عربية شائعة وتنتهي بـ `DejaVu Sans` (موجود على معظم أنظمة لينكس ويغطي العربية). لخط مخصص ضع الملف في `public/fonts/` وأضف `@font-face` عبر `staticFile(...)`، أو ثبّت `@remotion/google-fonts`.

### بنية الملفات

```
starters/remotion/
├── package.json          # preview / render / still / typecheck
├── tsconfig.json
├── remotion.config.ts    # نقطة الدخول + اختيار Chromium المحلي
├── props.example.json    # مثال --props
├── public/words.json     # ترجمة على مستوى الكلمة (عينة عربية)
└── src/
    ├── index.ts          # registerRoot
    ├── Root.tsx          # تركيبة KosifFilm
    ├── Film.tsx          # المشاهد الثلاثة + CameraRig
    ├── Captions.tsx      # ترجمة آمنة للعربية
    └── easing.ts         # دوال تسهيل بلا اعتماديات
```

</div>

---

## English

A small but real [Remotion v4](https://www.remotion.dev) project for KOSIF TOOL. One composition, `KosifFilm`, at 1080×1920 (vertical 9:16), 30 fps, 12 s by default, with three scenes:

1. **Title reveal**: the headline words spring in one after another with a stagger, followed by keyword pills.
2. **Animated SVG line chart**: the line is drawn with `interpolate` through `stroke-dashoffset`, each dot pops with a `spring` the moment the pen reaches it, and the headline number counts up.
3. **Closing logo card**: a ring draws around a simple mark, then the title and a closing line fade in.

All three scenes sit inside `CameraRig`, a single group transform (translate + rotate + scale) that drifts slowly across the whole film like a camera move. On top is a **word-level caption** layer that reads `public/words.json` and highlights the current word with the accent colour.

### Props

| prop | type | meaning |
|---|---|---|
| `title` | string | Headline; split into words for the staggered reveal and repeated on the closing card |
| `words` | string[] | Keywords shown as pills under the headline |
| `accent` | string | Accent colour, any CSS colour (6-digit hex recommended) |
| `lang` | `"ar"` or `"en"` | Text direction and the built-in UI strings |

### Install

```bash
cd starters/remotion
npm install
```

### Preview

```bash
npm run preview
```

Opens Remotion Studio at `http://localhost:3000` with a timeline and live prop editing.

### Render

```bash
# default props
npm run render

# custom props, inline JSON
npx remotion render KosifFilm out/film.mp4 \
  --props='{"title":"Q3 in one minute","words":["growth","customers","revenue"],"accent":"#19c37d","lang":"en"}'

# or from a file
npx remotion render KosifFilm out/film.mp4 --props=./props.example.json

# a still frame
npm run still

# quick smoke test, first second only
npx remotion render KosifFilm out/test.mp4 --frames=0-30
```

### Audio as the master clock

Put your file in `public/` (for example `public/voice.mp3`) and set, in `src/Film.tsx`:

```ts
const AUDIO_FILE: string = "voice.mp3";
```

That mounts `<Audio src={staticFile("voice.mp3")} />` at frame 0, so every time in `public/words.json` (seconds) is measured from the start of the audio. The template never edits or re-times the audio: picture follows sound, not the other way round.

To make the **film length** follow the audio length automatically, install `@remotion/media-utils` and add `calculateMetadata` to the composition in `src/Root.tsx`:

```bash
npm install @remotion/media-utils@4.0.535
```

```tsx
import { getAudioDurationInSeconds } from "@remotion/media-utils";
import { staticFile } from "remotion";

<Composition
  id="KosifFilm"
  /* ...same props as today... */
  calculateMetadata={async () => {
    const seconds = await getAudioDurationInSeconds(staticFile("voice.mp3"));
    return { durationInFrames: Math.ceil(seconds * FPS) };
  }}
/>
```

Generate `public/words.json` from the audio with any transcriber that outputs word timings (an array of `{ "word", "start", "end" }` in seconds). The caption layer only ever shows whole words and never splits an Arabic word.

### Using the Chromium already on this machine

Remotion does not need to download a browser when a Chromium already exists. `remotion.config.ts` looks, in order, for:

1. `KOSIF_BROWSER=/path/to/headless_shell` (environment variable)
2. a Playwright `chromium_headless_shell-*` build under `$PLAYWRIGHT_BROWSERS_PATH` or `/opt/pw-browsers` (`chrome-linux/headless_shell`)
3. a full Playwright `chromium-*` build there, only as a last resort

Remotion drives Chrome with the classic headless flags, which full Chromium builds no longer accept, so use the headless shell. On this machine it is `/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell` (check the number with `ls /opt/pw-browsers/`). You can also pass it explicitly, which overrides the config file:

```bash
npx remotion render KosifFilm out/film.mp4 \
  --browser-executable=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
```

### Fonts

The font stacks in `src/Film.tsx` and `src/Captions.tsx` start with common Arabic faces and end with `DejaVu Sans`, which ships with most Linux images and covers Arabic. For a custom face, put the file under `public/fonts/`, add an `@font-face` that points at `staticFile(...)`, or install `@remotion/google-fonts`.

### Type check

```bash
npm run typecheck
```

### Licence

MIT. Everything here is original KOSIF code; no third-party media, prompt text or code is included.
