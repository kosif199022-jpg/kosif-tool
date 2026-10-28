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

**حماية القرص:** إطار PNG بمقاس 1080×1920 يأخذ نحو 3.4 ميغابايت، فرندر 90 ثانية بـ30 إطارًا يحتاج قرابة 10 غيغابايت في مجلد مؤقت. لذلك قبل أول إطار يقدّر الراندر الحجم (عدد الإطارات × العرض × الارتفاع × 1.7 بايت + 10%) ويقارنه بالمساحة الحرة على قرص مجلد الإطارات، بعد خصم ما ستكتبه عمليات رندر أخرى تعمل الآن؛ فإن لم يتّسع توقف بالرمز 2 وذكر المطلوب والمتاح والحلول: `--frames-dir` على قرص أكبر، أو تحرير مساحة، أو رندر جزء أقصر بـ`--start` و`--duration`. الخيار `--no-space-check` يتخطى هذا الفحص.
وعند بدء كل رندر يسرد على stderr مجلدات `kosif-frames-*` المؤقتة الأقدم من 6 ساعات (بقايا رندر مقطوع) مع أحجامها، و`--clean-stale` يحذفها هي فقط ولا يلمس المجلد المستخدم. وإذا أُوقف الرندر بـCtrl+C أو SIGTERM أو SIGHUP حذف مجلد إطاراته المؤقت وخرج بالرمز 130 أو 143 أو 129. أما `kill -9` فلا يمكن التقاطه، وبقاياه يحذفها `--clean-stale` لاحقًا.

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
| `--audio <file>` | AAC, MP3 and ALAC are stream-copied byte for byte and cut at the last video frame; other codecs (WAV, FLAC …) are encoded to AAC 320k with `-shortest`; the audio is never resampled or time-stretched |
| `--mode seek|virtual` | force the driver (auto-detected otherwise) |
| `--preview` | render 8 evenly spaced frames into one labelled contact sheet |
| `--crf`, `--scale` | H.264 quality (default 17, the [export standard](../playbooks/export-standard.md); lower only) and device scale factor (`--scale 2` = 4K, only when the user asks) |
| `--frames-dir`, `--keep-frames` | keep the PNG frames (`--frames-dir` also moves them to a disk of your choice) |
| `--no-space-check` | skip the free-space pre-flight (see *Disk guard*) |
| `--clean-stale` | delete `kosif-frames-*` temp folders older than 6 h before rendering; without it they are only listed |
| `--seed`, `--offline`, `--timeout`, `--settle` | determinism helpers (seeded `Math.random`, block network, load timeout, settle delay) |
| `--help`, `-h` | print the options and exit 0 |

An unknown option (a typo such as `--fsp 24`), a stray argument or a value option without its value is a usage error: the message and the usage go to stderr and the exit code is 1, so nothing renders with a silent default.

Exit codes: 0 ok, 1 usage error, 2 render/encode failure or not enough disk space, 3 ffprobe disagrees with the request, 130/143/129 stopped by SIGINT/SIGTERM/SIGHUP.

**Disk guard.** PNG frames are large (about 3.4 MB per 1080×1920 frame, so 90 s at 30 fps is roughly 10 GB), and two renders sharing a small `/tmp` once filled it: Chromium's `Page.captureScreenshot` then failed with "Unable to capture screenshot", and the killed renders left 3–8 GB temp folders behind. Now:

- *Free-space pre-flight.* As soon as the frame count is known (before Chromium starts when `--duration` is given, otherwise right after the page reports its duration), the renderer estimates `frames × width × height × 1.7 bytes + 10%` at the capture size, reads the free space of the frames folder's filesystem with `fs.statfsSync` (Node ≥ 18.15; on older Node the check is skipped with a warning) and subtracts what other renders running now still have to write there (each temp frames folder carries a small `.kosif-render.json` with its pid and estimate). If the frames do not fit it exits 2 before the first frame and says how much is needed and free, and what to do: `--frames-dir` on a bigger disk, free space (or `--clean-stale`), or a shorter `--start`/`--duration` range. `--no-space-check` skips the check.
- *Stale folders.* Every run lists, on stderr, the `kosif-frames-*` folders in the temp folder (`os.tmpdir()`, usually `/tmp`) that belong to this user, were not modified for 6 hours and whose render is no longer running, with their sizes. `--clean-stale` deletes exactly those; the folder this render uses is never touched. Folders kept with `--keep-frames` count as stale after 6 hours too.
- *Signals.* Ctrl+C (SIGINT), SIGTERM and SIGHUP remove the temp frames folder (unless `--keep-frames` or `--frames-dir` was given) and exit 130, 143 or 129. A signal that arrives while ffmpeg encodes is handled when ffmpeg returns. `kill -9` and the out-of-memory killer cannot be caught; `--clean-stale` removes what they leave once it is 6 hours old.

```bash
node tools/render_html.cjs --in film.html --out out/film.mp4 --clean-stale             # tidy /tmp first
node tools/render_html.cjs --in film.html --out out/film.mp4 --frames-dir /mnt/big/frames  # frames on a bigger disk
```

**Page contract for seek mode:** `window.__kosif = { duration, fps?, seek(t) }` where `seek(t)` draws the frame for time `t` synchronously or returns a promise; optional `window.__kosifReady` promise (e.g. `document.fonts.ready`). The starter in `starters/html-canvas/` implements it.

**Virtual-time mode:** the page needs nothing. Chromium's virtual clock is paused after load and advanced by exactly `1000/fps` ms per frame, so CSS/WAAPI time, `requestAnimationFrame` timestamps, timers and `Date.now()` are exact and reproducible.

Playwright is resolved from the current project, then `/opt/node-tools/node_modules/playwright`, then `KOSIF_PLAYWRIGHT`. Chromium comes from `PLAYWRIGHT_BROWSERS_PATH`; never run `playwright install` on the KOSIF cloud machine.

After rendering, gate the delivery with `python3 tools/verify_video.py out/film.mp4 --aspect 9:16 --fps 30 --duration 12 --audio voice.mp3`.
