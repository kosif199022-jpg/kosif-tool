# دراسة «مونتاجي» — Montaji study (2026-10-23)

<div dir="rtl">

**ما هو:** «مونتاجي» 1.0.0 (`app.montaji.editor`) محرر فيديو بسيط بالعربي للماك بمعالج Apple، على طريقة CapCut: مسار رئيسي مغناطيسي، ونصوص عربية متحركة، وفلاتر ألوان، وانتقالات، وترجمة تلقائية تعمل على الجهاز بلا إنترنت، وقراءة نص بصوت الماك، وتصدير MP4. شاركه المالك من Google Drive كملف `Montaji-1.0.0-arm64.dmg` (69 ميجا).

**كيف درسناه:** نزّلنا الملف إلى مجلد فارغ مؤقت (بعد تجاوز صفحة تحذير Drive للملفات الكبيرة)، وفككنا الـ DMG (UDIF بضغط LZMA، فيه قسم HFS+) باستعمال 7-Zip 24.09، ثم قرأنا الملفات كنصوص فقط. **لم نشغّل التطبيق، ولا أي ملف تنفيذي أو سكربت بداخله.** الملفات التنفيذية (Mach-O arm64) لم نقرأ منها إلا النصوص الظاهرة.

**القاعدة:** كود التطبيق نفسه بلا رخصة (`"private": true`)، فلم ننسخ منه سطرًا ولا ثابتًا ولا قائمة. أخذنا **الأفكار** فقط، وكتبنا تنفيذًا أصليًا بثوابت وقوائم من عندنا، وأثبتناه باختبارات. المكونات مفتوحة المصدر داخله (FFmpeg بـ GPL-3، وNode.js وwhisper.cpp وSilero VAD بـ MIT) نذكرها بأسمائها ونستعملها كأدوات مستقلة كما نفعل دائمًا.

</div>

## الفهرس / contents

1. [What is inside](#what-is-inside)
2. [How it works](#how-it-works)
3. [Ideas transferred](#ideas-transferred)
4. [The two new tools](#the-two-new-tools)
5. [What we did not take](#what-we-did-not-take)

## What is inside

| part | what it is | evidence |
|---|---|---|
| DMG | UDIF, LZMA-compressed blocks, GPT with one HFS+ volume (302 MB unpacked); sha256 `c90b687a…cb6ea` | 7-Zip 24.09 listing |
| `MacOS/montaji` | 149 KB Swift launcher: one `NSWindow` with a `WKWebView` pointed at the local server; reads `MONTAJI_SELFTEST`, sets `MONTAJI_PARENT_WATCH` | Mach-O symbols and strings |
| `Helpers/` | `node` 24.22.1, static `ffmpeg`/`ffprobe` 9.0.2, `whisper-cli` (whisper.cpp 1.9.5) | THIRD-PARTY-NOTICES.txt |
| `Resources/app/server/` | 6 ES modules, ~50 KB: HTTP server on `127.0.0.1:4719`, media library, export graph, jobs (export, captions, TTS), model downloads | source read as text |
| `Resources/app/public/` | vanilla-JS editor, ~190 KB: store (undo, autosave), timeline, preview compositor, inspector, panels, exporter, self-test; no framework, no bundler | source read as text |
| `Resources/models/` | `ggml-silero-v5.1.2.bin` voice-activity model (885 KB) | file name and size |
| data | projects, imports and exports under `~/Movies/Montaji`; speech models under `~/Library/Application Support/Montaji/models` | `lib.js` paths |

Speech models are downloaded on first use from the public whisper.cpp model repository: `large-v3-turbo-q5_0` (574 MB, "most accurate for Arabic") or `small-q5_1` (190 MB), each checked against a pinned SHA-256.

## How it works

1. **One model, two renderers.** A project is a media table plus tracks of items (the shape CapCut keeps in its draft file, simplified). The same module computes the layout for the browser preview and for the export, so what the canvas shows is what ffmpeg renders.
2. **Export = one ffmpeg filter graph.** Every clip is its own input with a fast seek; the main track is chained with `xfade`/`concat` (audio with `acrossfade`), overlays and text are composited with time-gated `overlay`, all audio is mixed with `amix` and a limiter. The graph is written to a file and passed with `-/filter_complex`.
3. **Text is drawn by the browser, not by ffmpeg.** Each text item is rasterised to a PNG in the canvas (correct Arabic shaping, stroke, shadow, rounded background), cropped to its rotated bounds, and ffmpeg only moves and fades it with expressions that mirror the preview easing.
4. **Colour is numbers.** A filter preset plus sliders becomes a per-channel affine step and a 3×3 matrix, emitted as `lutrgb` + `colorchannelmixer` for ffmpeg, an SVG filter for Chromium and a WebGL shader for WebKit.
5. **Captions run offline.** The timeline's audio is mixed to 16 kHz mono, whisper.cpp writes one word per entry with Silero VAD, and the words are grouped into short lines with reading rules and a filter for phrases the model invents.
6. **Media prep runs in a small queue** (two at a time): probe (rotation swaps width and height), poster, filmstrip sprite, waveform peaks, and a browser proxy only when the codec, pixel format or container would not play.

## Ideas transferred

Each idea became a record in [app-feature-transfer](../powers/app-feature-transfer.md) (APPX-140 to APPX-155), written in KOSIF's own words:

| idea | power | how KOSIF does it now |
|---|---|---|
| reading rules for caption lines | APPX-140 ✅ | `scripts/caption_lines.py group` |
| screen speech-model inventions | APPX-141 ✅ | `caption_lines.py` (phrase list + repeat-loop detection) and `lint` |
| one colour look for every renderer | APPX-142 ✅ | `scripts/look_pipeline.py build --target ffmpeg/svg/css/glsl` |
| measured preview/export parity | APPX-143 ✅ | `look_pipeline.py verify --all` (max 8-bit error ≤ 1 here) |
| magnetic main track with clamped transitions | APPX-144 | recipe: `xfade` offset = running length − transition |
| any speed with `atempo` | APPX-145 | recipe: split the factor into steps inside 0.5…100 |
| cheap blurred background fill | APPX-146 | recipe: quarter-size, `gblur`, upscale |
| text raster in reference units | APPX-147 | recipe: lay out at short side 1080, scale once |
| media prep for an editor | APPX-148 | recipe: poster, filmstrip sprite, peaks, proxy rule |
| hardware encoder with software fallback | APPX-149 | recipe: bits-per-pixel bitrate, retry on encoder errors |
| a safe local editor server | APPX-150 | checklist for loopback tools |
| verified model downloads | APPX-151 | `.part` + pinned SHA-256 + atomic rename |
| undo that groups slider drags | APPX-152 | snapshot stack + merge window + debounced atomic save |
| self-test inside the real host | APPX-153 | step report + pixel checks, written to a file |
| content-addressed media cache | APPX-154 | id = hash(path, size, mtime); resume interrupted work |
| offline Arabic speech stack | APPX-155 | whisper.cpp turbo/small + Silero VAD, word level |

## The two new tools

- **`caption_lines.py`** (`caption-lines`) turns word timings (atlas `words.json`, whisper.cpp `-oj`, faster-whisper) into SRT, VTT or JSON lines. A line breaks on: word count, characters, time on screen, a pause, a sentence end (`. ! ? ؟ ؛ : …`), or a comma once the line has two words. Short holes are closed, short lines are extended only into silence, Arabic lines can carry a right-to-left mark so players keep end punctuation in place, and suspected inventions (subtitle credits, "subscribe" outros, sound tags, punctuation-only lines, three identical lines in a row) are dropped and listed. `lint` checks overlaps, durations, reading speed and the same phrases in any caption file.
- **`look_pipeline.py`** (`look-pipeline`) holds eleven looks (natural, vivid, bright, warm, cool, cinematic, vintage, faded, dramatic, mono, night-dua) as parameters, turns them into one affine step and one matrix with KOSIF's own constants, and writes them for ffmpeg, SVG, CSS and GLSL. `verify` renders a test frame through ffmpeg and compares every pixel with the reference maths; `apply` grades a video into a new file.

Tests: `evals/test_caption_lines.py` (8) and `evals/test_look_pipeline.py` (6), both in CI.

## What we did not take

- No source file, constant table, preset list, font list, icon, stylesheet or text from Montaji is in this repository.
- The macOS-only parts (the `say` voice, AppleScript file pickers, VideoToolbox) are noted as ideas, not ported.
- We did not run the self-test, the server or any binary, so no claim here depends on Montaji's behaviour at run time; every ✅ above is proved by KOSIF's own tests.
