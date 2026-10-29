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

# لقطات ثابتة عند أزمنة محددة لفحص الفيلم، بلا فيديو
node tools/render_html.cjs --in film.html --out out/film.mp4 --stills 0,1.5,2.25s,1:04   # writes out/film_stills/
```

في النهاية يطبع الراندر سطر `VERIFY` من ffprobe (المدة، الإطارات، الأبعاد، الصوت، وبصمة الصوت `audio_md5`) ويخرج برمز غير صفري إن اختلف الناتج عن الطلب بأكثر من إطار واحد.

**لقطات عند أزمنة محددة (`--stills`):** بدل سكربت Playwright مؤقت، يأخذ `--stills` قائمة أزمنة مفصولة بفواصل (ثوانٍ مثل `1.5` أو `2.25s`، أو دقائق:ثوانٍ مثل `1:04`، حتى 64 زمنًا)، فيقدّم الصفحة إلى كل زمن ويحفظ `still_<t>.png` (الزمن بثلاث خانات عشرية) ولوحة واحدة `stills_grid.png` مكتوب على كل خانة فيها زمنها، وملف `stills.json` يصف كل لقطة؛ ولا يرمّز فيديو. المجلد الافتراضي بجوار `--out` باسم `<اسم الملف>_stills/`، و`--stills-dir` يغيّره (وحينها يمكن الاستغناء عن `--out`). في وضع seek تُرسم اللحظة نفسها بالضبط، وفي الوضع الافتراضي virtual تُؤخذ أقرب لقطة على شبكة `--fps` ويُكتب رقمها `#n`. يُتجاهل `--audio` و`--start` هنا. إن لم يكن في ffmpeg مرشّح drawtext تُكتب الأزمنة بأرقام مرسومة بـdrawbox، فاللوحة مُعنونة دائمًا.

**إثبات أن الصوت لم يُمس (`audio_md5`):** حين يُنسخ الصوت كما هو (AAC أو MP3 أو ALAC) يحسب الراندر بصمة MD5 لحِزم الصوت في الملف الأصلي وفي الناتج دون فك ترميزها (`ffmpeg -map 0:a:0 -c copy -f md5 -`، ويمر AAC عبر `aac_adtstoasc` على الجانبين كما يفعل `verify_video.py --source-audio`)، ويكتب في سطر `VERIFY` إحدى ثلاث: `audio_md5=match` (متطابق بايتًا ببايت)، أو `audio_md5=differs (src N packets, out M packets)` مع شرح واضح على stderr يقول هل الحزم الباقية مطابقة وقُصّ ما بعد آخر إطار (مسموح) أم تغيّرت البايتات نفسها، أو `audio_md5=reencoded` حين أُعيد ترميز الصوت (WAV وFLAC). الاختلاف لا يُفشل الرندر أبدًا لكنه يُقال بصوت عالٍ. ولا تُعِد دمج الصوت بعد الرندر بـ`ffmpeg -shortest`: هذا ما أسقط آخر حزمة AAC من قبل، بينما ناتج الراندر نفسه كان مطابقًا. ومع `--report <file.json>` تُكتب القيم نفسها في ملف JSON.

**حماية القرص:** إطار PNG بمقاس 1080×1920 يأخذ نحو 3.4 ميغابايت، فرندر 90 ثانية بـ30 إطارًا يحتاج قرابة 10 غيغابايت في مجلد مؤقت. لذلك قبل أول إطار يقدّر الراندر الحجم (عدد الإطارات × العرض × الارتفاع × 1.7 بايت + 10%) ويقارنه بالمساحة الحرة على قرص مجلد الإطارات، بعد خصم ما ستكتبه عمليات رندر أخرى تعمل الآن؛ فإن لم يتّسع توقف بالرمز 2 وذكر المطلوب والمتاح والحلول: `--frames-dir` على قرص أكبر، أو تحرير مساحة، أو رندر جزء أقصر بـ`--start` و`--duration`. الخيار `--no-space-check` يتخطى هذا الفحص.
وعند بدء كل رندر يسرد على stderr مجلدات `kosif-frames-*` المؤقتة الأقدم من 6 ساعات (بقايا رندر مقطوع) مع أحجامها، و`--clean-stale` يحذفها هي فقط: مجلداته المؤقتة بالاسم `kosif-frames-XXXXXX` التي لا تحوي إلا إطارات الرندر، ولا يلمس أبدًا مجلد `--frames-dir` (يُعلَّم بملف `.kosif-user-frames`) ولا المجلد المستخدم ولا مجلدًا يحويه. وإذا أُوقف الرندر بـCtrl+C أو SIGTERM أو SIGHUP حذف مجلد إطاراته المؤقت وخرج بالرمز 130 أو 143 أو 129. أما `kill -9` فلا يمكن التقاطه، وبقاياه يحذفها `--clean-stale` لاحقًا.

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
| `--audio <file>` | AAC, MP3 and ALAC are stream-copied byte for byte and cut at the last video frame, and the copy is proved by packet MD5 (`audio_md5=`, see *Audio proof*); other codecs (WAV, FLAC …) are encoded to AAC 320k with `-shortest` (`audio_md5=reencoded`); the audio is never resampled or time-stretched |
| `--mode seek|virtual` | force the driver (auto-detected otherwise) |
| `--preview` | render 8 evenly spaced frames into one labelled contact sheet |
| `--stills <times>` | instead of a video, capture the film at these times (seconds such as `1.5` or `2.25s`, or `m:ss` such as `1:04`; comma-separated, read to the millisecond, sorted, at most 64): `still_<t>.png`, a labelled `stills_grid.png` and `stills.json` (see *Stills*) |
| `--stills-dir <dir>` | where the stills go (default `<out name>_stills/` next to `--out`; with it `--out` may be omitted) |
| `--report <file.json>` | also write a JSON report: the VERIFY values and the audio proof (render), the contact sheet (preview) or the stills manifest (stills) |
| `--crf`, `--scale` | H.264 quality (default 17, the [export standard](../playbooks/export-standard.md); lower only) and device scale factor (`--scale 2` = 4K, only when the user asks) |
| `--frames-dir`, `--keep-frames` | keep the PNG frames (`--frames-dir` also moves them to a disk of your choice and marks that folder with a `.kosif-user-frames` file so `--clean-stale` never deletes it) |
| `--no-space-check` | skip the free-space pre-flight (see *Disk guard*) |
| `--clean-stale` | delete the renderer's own temp folders (`kosif-frames-XXXXXX` holding only frames) older than 6 h before rendering; without it they are only listed |
| `--seed`, `--offline`, `--timeout`, `--settle` | determinism helpers (seeded `Math.random`, block network, load timeout, settle delay) |
| `--help`, `-h` | print the options and exit 0 |

An unknown option (a typo such as `--fsp 24`), a stray argument or a value option without its value is a usage error: the message and the usage go to stderr and the exit code is 1, so nothing renders with a silent default.

Exit codes: 0 ok, 1 usage error, 2 render/encode failure or not enough disk space, 3 ffprobe disagrees with the request, 130/143/129 stopped by SIGINT/SIGTERM/SIGHUP.

**Stills.** To check a film at exact moments, `--stills` replaces a throwaway Playwright script: it loads the page once, seeks to each time in order and saves the frame, without encoding a video.

```bash
node tools/render_html.cjs --in film.html --out out/film.mp4 --stills 0,1.5,2.25s,1:04
# -> out/film_stills/still_0.000.png still_1.500.png still_2.250.png still_64.000.png stills_grid.png stills.json
node tools/render_html.cjs --in film.html --stills-dir out/check --stills 3.2,7.9 --width 540 --height 960
```

- Seek mode (`window.__kosif.seek`) draws exactly the requested time. Virtual mode can only stop on the frame grid, so it takes the nearest frame at `--fps` (frame `round(t × fps)`, labelled `#n`, its real time in `t_actual`); two times on the same frame give two copies of it.
- `stills_grid.png` tiles every still (one row up to 4, then 4, 6 or 8 columns) and prints its time on the tile: with ffmpeg's `drawtext` when it exists and works, otherwise with built-in digits drawn by `drawbox`, so the grid is always labelled.
- `stills.json` (`kosif.render_html.stills.v1`) lists each still's requested time `t`, drawn time `t_actual`, frame index, file and label, the driver, size, grid layout and the page's console errors. Other files in the folder are never deleted; a still of the same time is overwritten.
- `--audio` and `--start` are ignored (the times are film times); `--duration` is not needed, and a time past the page's `window.__kosif.duration` is captured with a warning. `--stills` and `--preview` cannot be combined.
- The same `--stills` list gives byte-identical stills on every run: at 270×480 and 540×960 a still at 2 s after one at 0.5 s was identical across 8 renders running at once, and at 540×960 it was identical whether or not 0.5 s was seeked first. At a tiny viewport (a 1080-wide page shrunk ten times, `--width 108`) Chromium can rasterise scaled text slightly differently depending on the time seeked before and on machine load (2 of 6 parallel runs differed), so check stills at 270 px wide or more.

**Audio proof.** When `--audio` is stream-copied (AAC, MP3, ALAC), the renderer proves it: it hashes the packets of the first audio stream of the source and of the output without decoding them (`ffmpeg -i X -map 0:a:0 -c copy -f md5 -`, plus `-f framemd5 -` for per-packet hashes; AAC goes through `-bsf:a aac_adtstoasc` on both sides, exactly as `tools/verify_video.py --source-audio` does, so a raw ADTS `.aac` source compares as the MP4 carries it). The VERIFY line then ends with one of:

| `audio_md5=` | meaning |
|---|---|
| `match` | whole-stream MD5 and packet count equal: the output carries the source byte for byte |
| `differs (src N packets, out M packets)` | not byte-identical; stderr explains loudly. Usually the voice runs past the film and the packets after the last video frame were cut (the kept packets are named as byte-identical source packets 1…M; with `--start` the head is cut too). This trim is allowed and **never fails the render**. If a packet's bytes changed, stderr names the first one and says to re-render from the untouched source |
| `reencoded` | the codec cannot live in MP4 as-is (WAV, FLAC …), so it was encoded to AAC 320k: no byte-level proof is possible |
| `none` / `unknown (reason)` | no `--audio`, or ffmpeg could not hash a side (the render still succeeds) |

```text
VERIFY OK duration=1.000s fps=30 frames=30 size=270x480 audio=aac audio_md5=differs (src 72 packets, out 48 packets) file=out/film.mp4
[render_html] AUDIO NOT BYTE-IDENTICAL TO THE SOURCE: audio_md5=differs (src 72 packets, out 48 packets)
[render_html]   every output packet is byte-identical to source packets 1-48: nothing was re-encoded, packets were only cut.
[render_html]   cut: 24 packets after the last video frame (the film is 1s, the source audio ends at 1.5s). This trim is allowed; ...
```

Do not re-mux the renderer's output (for example `ffmpeg -i film.mp4 -i voice.m4a -c copy -shortest ...`): such a pass once dropped the last AAC packet while the renderer's own file was byte-identical. Mux the voice in the render with `--audio`, and check any later file with `python3 tools/verify_video.py <file> --source-audio voice.m4a`. With `--report out/film.report.json` the same values go to a JSON file (`kosif.render_html.report.v1`: `verify`, `audio_md5`, `audio.proof` with both MD5s, packet counts, the cut and the first changed packet, and `verify_line`).

**Disk guard.** PNG frames are large (about 3.4 MB per 1080×1920 frame, so 90 s at 30 fps is roughly 10 GB), and two renders sharing a small `/tmp` once filled it: Chromium's `Page.captureScreenshot` then failed with "Unable to capture screenshot", and the killed renders left 3–8 GB temp folders behind. Now:

- *Free-space pre-flight.* As soon as the frame count is known (before Chromium starts when `--duration` is given, otherwise right after the page reports its duration), the renderer estimates `frames × width × height × 1.7 bytes + 10%` at the capture size, reads the free space of the frames folder's filesystem with `fs.statfsSync` (Node ≥ 18.15; on older Node the check is skipped with a warning) and subtracts what other renders running now still have to write there (each temp frames folder carries a small `.kosif-render.json` with its pid and estimate). If the frames do not fit it exits 2 before the first frame and says how much is needed and free, and what to do: `--frames-dir` on a bigger disk, free space (or `--clean-stale`), or a shorter `--start`/`--duration` range. `--no-space-check` skips the check.
- *Stale folders.* Every run lists, on stderr, the renderer's own temp folders in the temp folder (`os.tmpdir()`, usually `/tmp`): named like `fs.mkdtemp` output (`kosif-frames-` plus 6 letters or digits), holding nothing but files a render writes (`frame_NNNNNN.png`, `preview_raw/tile_NN.png`, `.kosif-render.json`), owned by this user, not modified for 6 hours and whose render is no longer running, with their sizes. `--clean-stale` deletes exactly those. A folder with any other file or a subfolder, a `--frames-dir` folder (the renderer writes a `.kosif-user-frames` file into it), the folder this render uses and any folder that holds it are never touched. Folders kept with `--keep-frames` count as stale after 6 hours too.
- *Signals.* Ctrl+C (SIGINT), SIGTERM and SIGHUP remove the temp frames folder (unless `--keep-frames` or `--frames-dir` was given) and exit 130, 143 or 129. A signal that arrives while ffmpeg encodes is handled when ffmpeg returns. `kill -9` and the out-of-memory killer cannot be caught; `--clean-stale` removes what they leave once it is 6 hours old.

```bash
node tools/render_html.cjs --in film.html --out out/film.mp4 --clean-stale             # tidy /tmp first
node tools/render_html.cjs --in film.html --out out/film.mp4 --frames-dir /mnt/big/frames  # frames on a bigger disk
```

**Page contract for seek mode:** `window.__kosif = { duration, fps?, seek(t) }` where `seek(t)` draws the frame for time `t` synchronously or returns a promise; optional `window.__kosifReady` promise (e.g. `document.fonts.ready`). The starter in `starters/html-canvas/` implements it.

**Virtual-time mode:** the page needs nothing. Chromium's virtual clock is paused after load and advanced by exactly `1000/fps` ms per frame, so CSS/WAAPI time, `requestAnimationFrame` timestamps, timers and `Date.now()` are exact and reproducible.

Playwright is resolved from the current project, then `/opt/node-tools/node_modules/playwright`, then `KOSIF_PLAYWRIGHT`. Chromium comes from `PLAYWRIGHT_BROWSERS_PATH`; never run `playwright install` on the KOSIF cloud machine.

After rendering, gate the delivery with `python3 tools/verify_video.py out/film.mp4 --aspect 9:16 --fps 30 --duration 12 --audio voice.mp3`.
