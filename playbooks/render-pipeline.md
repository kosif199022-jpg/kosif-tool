# Preview and render pipeline — خط أنابيب المعاينة والرندر

This playbook describes how a KOSIF film goes from code to a verified MP4: deterministic rendering, previews before the final render, choosing between Remotion and Playwright + ffmpeg, platform encoding specs and the delivery gate.

يصف هذا الدليل كيف ينتقل فيلم KOSIF من الكود إلى MP4 موثّق: الرندر الحتمي، المعاينة قبل الرندر النهائي، الاختيار بين Remotion وPlaywright مع ffmpeg، مواصفات الترميز لكل منصة، وبوابة التسليم.

## 1. When to use — متى تستخدمه

Before every render. The user approves a preview first unless they pre-authorized the final render.

**بالعربية:** قبل كل رندر. يوافق المستخدم على المعاينة أولًا ما لم يأذن مسبقًا بالرندر النهائي.

## 2. Visual grammar — القواعد البصرية

Preview artefacts:

- Contact sheet: 8 evenly spaced labelled frames (`--preview`) for layout, type size and colour checks.
- Short clip: 2–4 s around the most complex moment, at half resolution, for motion checks.
- Full render only after approval.

**بالعربية:** لوحة من 8 إطارات للتخطيط والأحجام والألوان، ومقطع قصير 2–4 ثوانٍ لأصعب لحظة لفحص الحركة، والرندر الكامل بعد الموافقة.

## 3. Motion mechanics — ميكانيكا الحركة

**Which renderer:**

| need | use |
|---|---|
| HTML/Canvas/SVG film with `window.__kosif.seek(t)` | `node tools/render_html.cjs --in film.html --out film.mp4` (seek mode) |
| Any page with CSS/WAAPI/GSAP animations and no hook | `tools/render_html.cjs --mode virtual` (virtual time) |
| React composition, editable props, Studio preview | Remotion (`starters/remotion`, `npx remotion render`) |
| Three.js | seek mode with `preserveDrawingBuffer: true`, or `@remotion/three` |

Screen recording is never used for delivery: it drops frames and is not reproducible.

**Determinism rules:** frame = f(t); seeded randomness; fonts loaded before frame 0 (`window.__kosifReady`); no network-dependent assets at render time (download and license them first); fixed viewport and device scale.

**On the KOSIF cloud machine:** Playwright is at `/opt/node-tools/node_modules/playwright`, Chromium under `/opt/pw-browsers` (never run `playwright install`). Remotion needs the classic headless shell: `starters/remotion/remotion.config.ts` picks `/opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell` automatically.

**بالعربية:** للصفحات ذات `seek` استخدم `render_html.cjs` في وضع seek، وللصفحات بحركات CSS بلا خطاف استخدم وضع virtual، ولمشاريع React القابلة للتعديل استخدم Remotion. لا تسجيل شاشة للتسليم. الإطار دالة في الزمن، والخطوط محمّلة قبل الإطار الأول، ولا أصول من الشبكة أثناء الرندر.

## 4. Scene recipes — وصفات المشاهد

**A — Standard delivery (التسليم القياسي)**

| step | command |
|---|---|
| 1 preview | `node tools/render_html.cjs --in film.html --out out/film.mp4 --preview` (writes `out/film_preview.png`) |
| 2 motion check | `node tools/render_html.cjs --in film.html --out out/check.mp4 --start 4 --duration 3 --width 540 --height 960` |
| 3 approval | show both to the user |
| 4 final | `node tools/render_html.cjs --in film.html --out out/film.mp4 --fps 30 --audio voice.mp3` |
| 5 gate | `python3 tools/verify_video.py out/film.mp4 --aspect 9:16 --fps 30 --duration 15 --audio voice.mp3` |
| 6 report | fill `TEST_REPORT.md` with the measured values |

**B — Remotion delivery:** `npx remotion still KosifFilm out/still.png --frame=60`, then `npx remotion render KosifFilm out/film.mp4 --props=props.json`, then the same gate.

**C — Multi-platform:** render the master at the largest aspect, then re-compose (not crop blindly) per platform; each export passes the gate.

## 5. Implementation — التنفيذ

Encoding specs follow the owner-approved **export standard** in [`export-standard.md`](export-standard.md) (same or better, never lower): 1080×1920, 30 fps, H.264 High CRF 17 preset slow, BT.709, the user's audio stream-copied, MP4 `+faststart`, no 4K unless the user asks, colour matched to the source.

| platform | aspect / size | fps | video | audio |
|---|---|---|---|---|
| Reels / TikTok / Shorts (default) | 9:16, 1080×1920 | 30 | H.264 High, yuv420p, BT.709, CRF 17, preset slow | user's track copied as-is; else AAC 48 kHz 320 kbps |
| YouTube | 16:9, 1920×1080 (3840×2160 only when asked) | 24/30/60 | H.264 High CRF 17, preset slow, `+faststart` | copied as-is; else AAC 48 kHz 320 kbps |
| Feed | 1:1 1080×1080 or 4:5 1080×1350 | 30 | H.264 High CRF 17, preset slow | copied as-is; else AAC 320 kbps |

Manual encode from frames (WAV voice: swap `-c:a copy -t …` for `-c:a aac -b:a 320k -ar 48000 -af apad -shortest`):

```bash
ffmpeg -framerate 30 -i frames/frame_%06d.png -i voice.mp3 -map 0:v -map 1:a \
  -vf "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p" \
  -c:v libx264 -preset slow -crf 17 -profile:v high -pix_fmt yuv420p \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv \
  -c:a copy -t <video seconds> -movflags +faststart out/film.mp4
```

### Waiting on a long render — انتظار رندر طويل

Never wait with `sleep N; check` (`sleep 60; grep "^frame" render.log | tail -1`), chained sleeps or `python -c "time.sleep(60)"`: Claude Code blocks them, and so does the repo hook `.claude/hooks/no_sleep_wait.py`. Start the job detached and let it report its own progress:

| step | command | how to run it |
|---|---|---|
| start | `python3 tools/job.py start --dir out/<job>/render -- node tools/render_html.cjs --in film.html --out out/film.mp4 --audio voice.mp3` | plain Bash, returns at once |
| follow | `python3 tools/job.py wait --dir out/<job>/render` | Monitor tool: one `PROGRESS frame 120/450` line at most every 20 s, then `DONE exit=0` or `FAILED exit=N` with the log tail |
| or: one notice | `python3 tools/job.py wait --dir out/<job>/render --quiet` | Bash with `run_in_background: true`: you are woken once when it ends |
| peek now | `python3 tools/job.py status --dir out/<job>/render` | plain Bash, never waits |
| stop | `python3 tools/job.py stop --dir out/<job>/render` | plain Bash |

The same works for ffmpeg encodes, Remotion, yt-dlp downloads and installs. Other options: run the command itself with Bash `run_in_background: true`, or wait for a condition with a Monitor `until grep -q VERIFY out/<job>/render/job.log; do sleep 2; done`. A Monitor must also catch failure (`job.py wait` always ends with DONE or FAILED). Keep working on the next step while the job runs; do not chain shorter sleeps to get around the block.

**Remote sandboxes over MCP (Higgsfield `sandbox_exec`):** the client cuts each call at 60 s even with `timeout_seconds: 120`, and the standard sandbox has a single CPU. Start encodes with `background: true` (one encode per call, `-preset slow` or `medium`, never `veryslow` there), poll the returned status/log files with short calls, and run `ffprobe`/`md5sum`/`split` only after the job is done. See appendix A29, section «مهلة أداة MCP».

**بالعربية:** لا تنتظر أبدًا بـ `sleep 60; grep ...` ولا بسلسلة sleep: Claude Code يمنعها. شغّل الرندر بـ `tools/job.py start`، وتابعه بـ `job.py wait` داخل أداة Monitor (سطر تقدّم كل 20 ثانية ثم DONE أو FAILED) أو في الخلفية بـ `--quiet` (تنبيه واحد عند الانتهاء)، و`job.py status` لنظرة سريعة بلا انتظار.

Seek contract for your own pages: `window.__kosif = { duration, fps, seek(t) }` plus optional `window.__kosifReady`. See `starters/html-canvas/index.html`.

Photo films (a photo behind lyrics, Ken Burns, pans, parallax, handheld shake): draw every photo layer through `tools/photo_cover.js` (`KosifCover.drawPhoto(ctx, img, { W, H, zoom, fx, fy, ox, oy, rot, blur })`). It scales to cover (never to the frame width alone), floors the zoom at cover, raises it for rotation and blur, and clamps pans so no edge of the photo shows, for any photo aspect ratio. Before the preview, run `node tools/check_frame_cover.cjs --in film/index.html --variants "style=1;style=2;style=3;style=4;style=5" --samples 48`: it renders sample frames of every style and exits 3 if any frame shows an empty edge.

**بالعربية (أفلام الصور):** ارسم كل طبقة صورة عبر `tools/photo_cover.js` حتى تغطي الصورة الإطار كله في كل حركة كاميرا ولأي مقاس صورة، ثم شغّل `tools/check_frame_cover.cjs` على كل الستايلات قبل المعاينة؛ يفشل لو ظهرت حافة فاضية في أي إطار.

**بالعربية:** المواصفات في الجدول أعلاه: 9:16 بدقة 1080×1920 و30 إطارًا لريلز وتيك توك، و16:9 ليوتيوب، و1:1 أو 4:5 للخلاصات، كلها H.264 وyuv420p وصوت AAC بجهارة −14 LUFS.

## 6. Arabic and RTL notes — ملاحظات العربية

Fonts must be local or loaded before rendering; a fallback font in the final render changes Arabic shaping and width. Check the contact sheet for clipped diacritics and reversed numbers before the full render.

**بالعربية:** يجب أن تكون الخطوط محمّلة قبل الرندر، فالخط البديل يغيّر تشكيل العربية وعرضها. افحص لوحة الإطارات بحثًا عن تشكيل مقصوص أو أرقام معكوسة قبل الرندر الكامل.

## 7. Audio sync — المزامنة مع الصوت

Set the film duration to the audio duration and let the renderer mux the audio in its one pass: `render_html.cjs --audio voice.m4a` stream-copies an AAC/MP3/ALAC track byte for byte (every other codec, such as WAV, FLAC, Opus, Vorbis or AC-3, becomes AAC 320k and reports `audio_md5=reencoded`, so it has no byte proof). Confirm with `verify_video.py --audio` that lengths match within 50 ms. Stills at chosen times for review: `render_html.cjs --stills 0,1.5,3.2` (see [tools/render_html.md](../tools/render_html.md)).

**The renderer's MP4 is the master (lesson of 2026-10-29):**

1. Never re-mux the master with `-shortest`. It ends the file at the shorter stream, so it can cut the last breath or word of the audio (such a pass once dropped the last AAC packet while the renderer's own file was byte-identical), and the audio is no longer the source. Fix a length problem in the scene (duration = audio duration) and render again; never in a second ffmpeg pass.
2. Prove the audio is the source by MD5. The renderer's VERIFY line ends with `audio_md5=match` when the copied track is byte-identical, or `audio_md5=differs (src N packets, out M packets)` with stderr saying whether packets were only cut after the last video frame (allowed) or changed; `--report out/film.report.json` keeps the proof. For any other file, `python3 tools/verify_video.py out/film.mp4 --aspect 9:16 --fps 30 --duration <s> --source-audio voice.m4a` runs the same packet check and must report `"md5_match": true`. A WAV/FLAC source is re-encoded (`audio_md5=reencoded`), so it cannot match: say so in `TEST_REPORT.md` and check the length with `--audio` instead.

**بالعربية:** اجعل مدة الفيلم مساوية لمدة الصوت، واترك الرندر يدمج الصوت في مروره الوحيد (`--audio` ينسخ تيار AAC/MP3/ALAC كما هو)، وتحقق أن الفرق أقل من 50 مللي ثانية. **ملف المُرندر هو الماستر:** (1) لا يُعاد دمجه بـ `-shortest` أبدًا، فهو يُنهي الملف عند أقصر تيار وقد يقص آخر نفَس أو كلمة من الصوت (أسقط آخر حزمة AAC من قبل) فلا يعود الصوت هو المصدر؛ أصلح المدة في المشهد وأعد الرندر، لا في تمريرة ffmpeg ثانية. (2) اقرأ `audio_md5=` في سطر VERIFY (`match` يعني أنه صوتك بايتًا ببايت)، ولأي ملف آخر طابق بصمة MD5 للصوت مع المصدر بـ `verify_video.py --source-audio` ويجب أن تكون `md5_match` صحيحة؛ مصدر WAV/FLAC يُعاد ترميزه (`reencoded`) فلا يطابق، فاذكر ذلك في `TEST_REPORT.md` وافحص المدة بـ `--audio`.

## 8. Quality checklist — قائمة الفحص

1. Preview approved (or pre-authorized)?
2. Same frame renders identically twice?
3. Fonts loaded before frame 0?
4. Duration, fps and frame count match the request?
5. yuv420p and even dimensions?
6. Audio present, AAC, untouched (VERIFY `audio_md5=match`, or `differs` with only a cut after the last frame)?
7. −14 LUFS ±1.5, true peak ≤ −1 dBTP?
8. First and last frames intentional?
9. Editable sources delivered with the MP4?
10. TEST_REPORT.md filled with measured values?
11. Photo films: `check_frame_cover.cjs` passes for every style (no empty edge in any frame)?
12. The delivered file is the renderer's MP4, never re-muxed with `-shortest`, and its audio MD5 matches the source (VERIFY `audio_md5=match` or `verify_video.py --source-audio` `md5_match: true`), or TEST_REPORT.md says why it cannot?

## 9. Anti-patterns — أخطاء شائعة

Screen-recording a browser; rendering before approval; `Math.random()` per frame; fonts from a CDN that fails mid-render; odd dimensions; yuv444 output that phones cannot play; claiming checks that were not run; waiting on a render with `sleep N; check` instead of `tools/job.py wait`; re-muxing the renderer's MP4 with `-shortest` (it can cut the audio's tail).

**بالعربية:** تسجيل الشاشة، الرندر قبل الموافقة، عشوائية في كل إطار، خطوط من شبكة تتعطل أثناء الرندر، أبعاد فردية، صيغة ألوان لا تعمل على الهواتف، وادعاء فحوص لم تُجرَ، وانتظار الرندر بـ `sleep` بدل `tools/job.py wait`، وإعادة دمج ملف المُرندر بـ `-shortest` (قد يقص ذيل الصوت).

## 10. Related styles — استايلات ذات صلة

Every style uses this pipeline. Good first tests: `pm-ror-fly-9950f1` (Negroni recipe animation), `kinetic-arabic`, `infographic`, `product`.
