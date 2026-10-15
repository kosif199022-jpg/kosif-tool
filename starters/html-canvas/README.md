# KOSIF html-canvas starter — قالب فيلم حتمي بدون اعتماديات

<div dir="rtl">

## بالعربية

فيلم تجريبي 9:16 (1080×1920، 30 إطار/ث، 12 ثانية) مبني بـ HTML + Canvas + SVG بلا أي مكتبة. كل إطار دالة خالصة في الزمن `t`، لذلك يمكن لـ `tools/render_html.cjs` أن يطلب أي إطار بالترتيب ويحصل على النتيجة نفسها في كل مرة.

**ما يثبته القالب:**

- خط زمني بمشاهد لها بداية ونهاية (`timeline.js` → `KOSIF.Timeline`).
- مكتبة إيزنج: `outCubic`, `inOutCubic`, `outExpo`, `outBack`, `spring(x, stiffness, damping)`.
- كاميرا بمفاتيح حركة (`cameraAt` + `applyCamera`) تطبّق translate/scale/rotate على `#world`.
- رسم مسار SVG تدريجيًا بـ `pathLength="1"` و`stroke-dashoffset`.
- جسيمات Canvas بعشوائية مزروعة (`rng(seed)`) فمواقعها دالة في الزمن لا تتغير بين التشغيلات.
- تايبوغرافي عربي حركي: الكلمات تدخل ككلمات كاملة (لا تُفكَّك الحروف أبدًا) مع `dir="rtl"`.
- ترجمة متزامنة على مستوى الكلمة من `words.js` (نفس بيانات `words.json`): تُعرض الجملة الحالية وتُضاء الكلمة المنطوقة.
- شريط تقدم، منطقة آمنة اختيارية، وأزرار معاينة حيّة (تشغيل/سحب/`?t=3.2` للقفز لزمن معيّن).

**المعاينة الحيّة:** افتح `index.html` في المتصفح (أو `npx http-server` من جذر المستودع ثم `/starters/html-canvas/`). مسطرة السحب في الأسفل، والمسافة للتشغيل/الإيقاف.

**تغيير الكلمات والتوقيتات:** عدّل `words.json` ثم حوّله إلى `words.js`:

```bash
python3 tools/words_convert.py starters/html-canvas/words.json starters/html-canvas/words.js
# أو من ترجمة/تفريغ: SRT / VTT / Whisper JSON
python3 tools/words_convert.py captions.srt my-film/words.js
```

**الرندر:**

```bash
# لوحة إطارات للموافقة قبل الرندر
node tools/render_html.cjs --in starters/html-canvas/index.html --out out/preview.png --preview
# الفيلم كاملًا مع الصوت الأصلي كما هو
node tools/render_html.cjs --in starters/html-canvas/index.html --out out/film.mp4 --fps 30 --audio voice.mp3
# فحص التسليم
python3 tools/verify_video.py out/film.mp4 --aspect 9:16 --fps 30 --duration 12 --audio voice.mp3
```

**كيف تبني فيلمك:** انسخ المجلد (أو `python3 tools/kosif.py scaffold <id> <dir> --starter html-canvas`)، عدّل قائمة `scenes` في `index.html` (لكل مشهد `t0`, `t1`, `draw(t, p, local)`)، مفاتيح الكاميرا `camKeys`، البيانات `series`، وكلمات العنوان. احتفظ بالقاعدة الذهبية: لا حالة متراكمة؛ كل شيء يُحسب من `t`.

</div>

## English

A 9:16 sample film (1080×1920, 30 fps, 12 s) built with HTML + Canvas + SVG and no libraries. Every frame is a pure function of time `t`, so `tools/render_html.cjs` can ask for frames in order and always get identical pixels.

**What it demonstrates**

- A scene timeline with start/end per scene (`timeline.js` → `KOSIF.Timeline`).
- Easing library: `outCubic`, `inOutCubic`, `outExpo`, `outBack`, `spring(x, stiffness, damping)`.
- A keyframed camera (`cameraAt` + `applyCamera`) transforming `#world`.
- SVG path draw-on with `pathLength="1"` and `stroke-dashoffset`.
- Seeded Canvas particles (`rng(seed)`) whose positions are a function of time.
- Kinetic Arabic type: words enter as whole words (letters are never split), inside `dir="rtl"`.
- Word-level captions from `words.js` (same data as `words.json`): the current phrase is shown and the spoken word is highlighted.
- Progress bar, optional safe-area overlay and live controls (play, scrub, `?t=3.2` to jump).

**Live preview:** open `index.html` directly (or serve the repo with `npx http-server` and visit `/starters/html-canvas/`). Space toggles play.

**Renderer contract:** the page exposes `window.__kosif = { duration, fps, seek(t) }` and `window.__kosifReady` (a promise that resolves after fonts load). `seek(t)` must draw the frame for time `t` synchronously (or return a promise). Controls hide automatically under the renderer (`navigator.webdriver`).

**Words and timing:** edit `words.json`, then regenerate `words.js` with `python3 tools/words_convert.py starters/html-canvas/words.json starters/html-canvas/words.js` (also accepts SRT, VTT, Whisper JSON and CSV).

**Render:**

```bash
node tools/render_html.cjs --in starters/html-canvas/index.html --out out/preview.png --preview
node tools/render_html.cjs --in starters/html-canvas/index.html --out out/film.mp4 --fps 30 --audio voice.mp3
python3 tools/verify_video.py out/film.mp4 --aspect 9:16 --fps 30 --duration 12 --audio voice.mp3
```

**Build your own film:** copy the folder (or `python3 tools/kosif.py scaffold <id> <dir> --starter html-canvas`), edit the `scenes` array in `index.html` (each has `t0`, `t1`, `draw(t, p, local)`), the `camKeys` keyframes, the `series` data and the title words. Keep the golden rule: no accumulated state, everything derives from `t`.
