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

Encoding specs:

| platform | aspect / size | fps | video | audio |
|---|---|---|---|---|
| Reels / TikTok / Shorts | 9:16, 1080×1920 | 30 | H.264 High, yuv420p, CRF 18–20, ≤ 60 s typical | AAC 48 kHz 192 kbps, −14 LUFS |
| YouTube | 16:9, 1920×1080 (or 3840×2160) | 24/30/60 | H.264 CRF 16–18, `+faststart` | AAC 48 kHz 192–320 kbps |
| Feed | 1:1 1080×1080 or 4:5 1080×1350 | 30 | H.264 CRF 18 | AAC 192 kbps |

Manual encode from frames:

```bash
ffmpeg -framerate 30 -i frames/frame_%06d.png -i voice.mp3 \
  -c:v libx264 -pix_fmt yuv420p -crf 18 -preset slow -movflags +faststart \
  -c:a aac -b:a 192k -shortest out/film.mp4
```

Seek contract for your own pages: `window.__kosif = { duration, fps, seek(t) }` plus optional `window.__kosifReady`. See `starters/html-canvas/index.html`.

Photo films (a photo behind lyrics, Ken Burns, pans, parallax, handheld shake): draw every photo layer through `tools/photo_cover.js` (`KosifCover.drawPhoto(ctx, img, { W, H, zoom, fx, fy, ox, oy, rot, blur })`). It scales to cover (never to the frame width alone), floors the zoom at cover, raises it for rotation and blur, and clamps pans so no edge of the photo shows, for any photo aspect ratio. Before the preview, run `node tools/check_frame_cover.cjs --in film/index.html --variants "style=1;style=2;style=3;style=4;style=5" --samples 48`: it renders sample frames of every style and exits 3 if any frame shows an empty edge.

**بالعربية (أفلام الصور):** ارسم كل طبقة صورة عبر `tools/photo_cover.js` حتى تغطي الصورة الإطار كله في كل حركة كاميرا ولأي مقاس صورة، ثم شغّل `tools/check_frame_cover.cjs` على كل الستايلات قبل المعاينة؛ يفشل لو ظهرت حافة فاضية في أي إطار.

**بالعربية:** المواصفات في الجدول أعلاه: 9:16 بدقة 1080×1920 و30 إطارًا لريلز وتيك توك، و16:9 ليوتيوب، و1:1 أو 4:5 للخلاصات، كلها H.264 وyuv420p وصوت AAC بجهارة −14 LUFS.

## 6. Arabic and RTL notes — ملاحظات العربية

Fonts must be local or loaded before rendering; a fallback font in the final render changes Arabic shaping and width. Check the contact sheet for clipped diacritics and reversed numbers before the full render.

**بالعربية:** يجب أن تكون الخطوط محمّلة قبل الرندر، فالخط البديل يغيّر تشكيل العربية وعرضها. افحص لوحة الإطارات بحثًا عن تشكيل مقصوص أو أرقام معكوسة قبل الرندر الكامل.

## 7. Audio sync — المزامنة مع الصوت

Mux the original audio without resampling (`-c:a aac` from the source, `-shortest`), set the film duration to the audio duration, and confirm with `verify_video.py --audio` that lengths match within 50 ms.

**بالعربية:** ادمج الصوت الأصلي دون إعادة أخذ عينات، واجعل مدة الفيلم مساوية لمدة الصوت، وتحقق أن الفرق أقل من 50 مللي ثانية.

## 8. Quality checklist — قائمة الفحص

1. Preview approved (or pre-authorized)?
2. Same frame renders identically twice?
3. Fonts loaded before frame 0?
4. Duration, fps and frame count match the request?
5. yuv420p and even dimensions?
6. Audio present, AAC, untouched?
7. −14 LUFS ±1.5, true peak ≤ −1 dBTP?
8. First and last frames intentional?
9. Editable sources delivered with the MP4?
10. TEST_REPORT.md filled with measured values?
11. Photo films: `check_frame_cover.cjs` passes for every style (no empty edge in any frame)?

## 9. Anti-patterns — أخطاء شائعة

Screen-recording a browser; rendering before approval; `Math.random()` per frame; fonts from a CDN that fails mid-render; odd dimensions; yuv444 output that phones cannot play; claiming checks that were not run.

**بالعربية:** تسجيل الشاشة، الرندر قبل الموافقة، عشوائية في كل إطار، خطوط من شبكة تتعطل أثناء الرندر، أبعاد فردية، صيغة ألوان لا تعمل على الهواتف، وادعاء فحوص لم تُجرَ.

## 10. Related styles — استايلات ذات صلة

Every style uses this pipeline. Good first tests: `pm-ror-fly-9950f1` (Negroni recipe animation), `kinetic-arabic`, `infographic`, `product`.
