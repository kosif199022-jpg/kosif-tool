# tools/render_html.cjs — رندر HTML إلى فيديو حتمي / deterministic HTML → MP4

<div dir="rtl">

## بالعربية

يحوّل صفحة HTML متحركة إلى MP4 إطارًا بإطار عبر Chromium (Playwright) ثم يشفّرها بـ ffmpeg، فتحصل على نفس الفيديو في كل مرة، بلا إطارات ساقطة ولا اعتماد على سرعة الجهاز.

**وضعان:**

- `seek` — الصفحة تعرّف `window.__kosif = { duration, seek(t) }` (كما في `starters/html-canvas`). يستدعي الراندر `seek(i / fps)` لكل إطار ثم يلتقط الشاشة.
- `virtual` — أي صفحة (CSS animations, Web Animations, requestAnimationFrame, GSAP) بلا أي تعديل: يوقف الراندر ساعة المتصفح الافتراضية ويقدّمها بالضبط `1000 / fps` مللي ثانية لكل إطار.

يُكتشف الوضع تلقائيًا (seek إن وُجد `window.__kosif`)، ويمكن فرضه بـ `--mode`.

**أمثلة:**

```bash
# معاينة: 8 إطارات موزعة في لوحة واحدة (للموافقة قبل الرندر)
node tools/render_html.cjs --in film.html --out out/film.mp4 --preview   # writes out/film_preview.png

# رندر كامل 9:16 مع صوت أصلي يُدمج كما هو (بدون إعادة أخذ عينات)
node tools/render_html.cjs --in film.html --out out/film.mp4 --width 1080 --height 1920 --fps 30 --audio voice.mp3

# صفحة CSS عادية لمدة 6 ثوانٍ بالوضع الافتراضي
node tools/render_html.cjs --in page.html --out out/clip.mp4 --duration 6 --mode virtual

# رندر جزء من الفيلم فقط
node tools/render_html.cjs --in film.html --out out/part.mp4 --start 4 --duration 3
```

في النهاية يطبع الراندر سطر `VERIFY` من ffprobe (المدة، الإطارات، الأبعاد، الصوت) ويخرج برمز غير صفري إن اختلف الناتج عن الطلب بأكثر من إطار واحد.

</div>

## English

Renders an animated HTML page to MP4 frame by frame with headless Chromium (Playwright) and encodes with ffmpeg: identical output on every run, no dropped frames, independent of machine speed.

| option | meaning |
|---|---|
| `--in <file.html|URL>` | page to render (local file or http URL) |
| `--out <file>` | output `.mp4`; with `--preview` the contact sheet is written next to it as `<name>_preview.png` |
| `--aspect` | any frame: `9:16`, `16:9`, `4:5`, `3:4`, `21:9`, `2.35:1`, `1920x816`, or any name `tools/aspects.py` accepts (`reel`, `story`, `square`, `cinema`, Arabic names such as `مربع`) (sets width/height; ratios inside 9:16…16:9 get a 1080 px short side, wider/taller ones a 1920 px long side, always even) |
| `--width`, `--height` | viewport in CSS px (default 1080×1920; override `--aspect`) |
| `--fps` | frames per second (default 30) |
| `--duration`, `--start` | seconds; seek mode defaults to `window.__kosif.duration` |
| `--audio <file>` | muxed as AAC with `-shortest`; the audio is never resampled or time-stretched |
| `--mode seek|virtual` | force the driver (auto-detected otherwise) |
| `--preview` | render 8 evenly spaced frames into one labelled contact sheet |
| `--crf`, `--scale` | H.264 quality (default 17, the [export standard](../playbooks/export-standard.md); lower only) and device scale factor (`--scale 2` = 4K, only when the user asks) |
| `--frames-dir`, `--keep-frames` | keep the PNG frames |
| `--seed`, `--offline`, `--timeout`, `--settle` | determinism helpers (seeded `Math.random`, block network, load timeout, settle delay) |
| `--help`, `-h` | print the options and exit 0 |

An unknown option (a typo such as `--fsp 24`), a stray argument or a value option without its value is a usage error: the message and the usage go to stderr and the exit code is 1, so nothing renders with a silent default.

**Page contract for seek mode:** `window.__kosif = { duration, fps?, seek(t) }` where `seek(t)` draws the frame for time `t` synchronously or returns a promise; optional `window.__kosifReady` promise (e.g. `document.fonts.ready`). The starter in `starters/html-canvas/` implements it.

**Virtual-time mode:** the page needs nothing. Chromium's virtual clock is paused after load and advanced by exactly `1000/fps` ms per frame, so CSS/WAAPI time, `requestAnimationFrame` timestamps, timers and `Date.now()` are exact and reproducible.

Playwright is resolved from the current project, then `/opt/node-tools/node_modules/playwright`, then `KOSIF_PLAYWRIGHT`. Chromium comes from `PLAYWRIGHT_BROWSERS_PATH`; never run `playwright install` on the KOSIF cloud machine.

After rendering, gate the delivery with `python3 tools/verify_video.py out/film.mp4 --aspect 9:16 --fps 30 --duration 12 --audio voice.mp3`.
