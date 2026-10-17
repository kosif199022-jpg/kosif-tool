# Reference inspection — رصد المرجع قبل التنفيذ

The **observe** superpower. AGENTS.md rule 3 says: open the referenced page and video when your tools permit, and never claim to have watched what you could not open. STYLE.md then separates what you *observed* from what you *assumed*. This note explains how to reach the media lawfully, what to measure and how the measurements land in STYLE.md.

**بالعربية:** قوة «رصد المرجع». تقول القاعدة الثالثة في AGENTS.md: افتح صفحة المرجع والفيديو إن سمحت أدواتك، ولا تزعم أبدًا أنك شاهدت ما لم تستطع فتحه. ثم يفصل STYLE.md بين ما **لاحظته** وما **افترضته**. يشرح هذا الملف كيف تصل إلى الوسيط بشكل مشروع، وماذا تقيس، وكيف تنتقل القياسات إلى STYLE.md.

## 1. Permission first — الإذن أولًا

- Fetch only media you have the right to analyse: the user's own files, material its site explicitly permits, or public references whose terms allow viewing. Never log in with someone else's account, never bypass a paywall, never touch DRM or encrypted streams (the fetch script refuses `#EXT-X-KEY`).
- What you fetch is working material. It lives in `.kosif-cache/` (git-ignored), is never committed, never rehosted and never cut into the deliverable. The catalog policy (`catalog/SCHEMA.md`) forbids third-party media under `styles/` or `catalog/`.
- If you cannot reach the video, write exactly that in STYLE.md and in the delivery notes, and treat the brief as a director's proposal.

**بالعربية:** اجلب فقط ما يحق لك تحليله؛ لا تجاوز لجدران الدفع ولا للمحتوى المشفّر. ما تجلبه مادة عمل في `.kosif-cache/` ولا يُرفع إلى المستودع ولا يُستخدم داخل الفيلم. وإن لم تصل إلى الفيديو فاكتب ذلك صراحةً.

## 2. Three ways to the media — ثلاث طرق إلى الوسيط

| situation | what to do |
|---|---|
| The page embeds a direct `.mp4` / `.webm`, or Open Graph `og:video` points to one | `python3 .claude/skills/kosif-superpowers/scripts/fetch_reference.py <page-url>` discovers it (video/source tags, OG and Twitter player tags, JSON-LD `contentUrl`, media URLs inside scripts) and fetches the first direct file; `--list` shows all candidates, `--pick N` chooses one. |
| The player streams HLS (`.m3u8`) | Same script: it reads the master playlist, picks the highest-bandwidth variant, downloads the segments in parallel (plus a separate audio rendition when the stream splits them), refuses encrypted streams, and remuxes with `ffmpeg -c copy` into `reference.mp4`. |
| The player uses a `blob:` URL (Media Source Extensions) and nothing in the HTML names the file | The real URL exists only inside the browser tab. Open the browser's network panel while the video plays and filter by `m3u8` / `mp4`, or use a page-scanning browser extension (an unpacked MV3 extension that lists `<video>`/`<source>` sources and `performance` resource entries across all frames does this; load your own copy through `chrome://extensions` in developer mode — this skill does not vendor third-party browser code). Then pass the discovered URL to the script. For long-tail sites, `yt-dlp` (see `repos.md`, *observe*) performs the same extraction when the site permits downloads. |

The script's outputs, under `.kosif-cache/reference/<slug>/`:

| file | content |
|---|---|
| `reference.mp4` | the remuxed download (or `download.<ext>` / `stream.ts` when ffmpeg is absent) |
| `probe.json` | duration, fps, width × height, aspect label, codecs, audio channels |
| `contact.png` | 8 evenly spaced frames in a 4 × 2 sheet (`--frames` changes the count) |
| `cuts.json` | scene-cut timestamps from `select='gt(scene,0.3)'` (`--scene` tunes the threshold) |
| `palette.json` | up to 8 dominant colours from `palettegen` |
| `REPORT.md` | bilingual summary with a reminder of what belongs in STYLE.md |

**بالعربية:** ثلاث حالات: ملف مباشر في الصفحة، بث HLS، أو مشغّل يستخدم `blob:` فلا يظهر الرابط إلا داخل التبويب (لوحة الشبكة أو إضافة تفحص الصفحة). السكربت يحفظ الفيديو مع قياساته في `.kosif-cache/reference/`.

## 3. What to measure — ماذا تقيس

| measurement | tool | STYLE.md field |
|---|---|---|
| duration, fps, aspect, resolution | `probe.json` (ffprobe) | *Observed*: deliverable spec, scene count per second |
| cut rhythm | `cuts.json`; for finer control `scenedetect -i reference.mp4 detect-content list-scenes` (install first) | *Observed*: average shot length, where the pace changes |
| palette | `palette.json`; cross-check one frame with a colour picker | *Observed*: colour table (hex); mark tints you averaged as *estimated* |
| type scale | measure cap height on a 1080-px-wide frame extracted at full size (`ffmpeg -ss 4 -i reference.mp4 -frames:v 1 frame.png`) | *Observed*: type sizes in px of the reference frame; convert to your canvas |
| easing and durations | extract 12–24 consecutive frames around one entrance (`ffmpeg -ss 4.0 -i reference.mp4 -frames:v 24 -vf scale=540:-2 frames/f_%03d.png`) and plot position per frame | *Observed*: duration in ms and curve shape (ease-out, overshoot, linear); the exact bezier stays *Assumed* |
| camera | compare two frames 0.5 s apart for drift/zoom; OpenCV optical flow when installed | *Observed*: drift direction and speed in %/s; everything else *Assumed* |
| motion density | count moving elements per second in the contact sheet | *Assumed* until verified frame by frame |

Rules: numbers you measured are *Observed*; anything inferred from a still is *Assumed* until a frame sequence confirms it. Write the sampling you did ("8 frames + 2 frame sequences at 4.0 s and 9.2 s") so a reviewer can repeat it.

**بالعربية:** ما قسته رقمًا يذهب إلى «ما لاحظته»؛ وما استنتجته من صورة ثابتة يبقى في «ما افترضته» حتى تؤكده سلسلة إطارات. اكتب كيف أخذت العينات حتى يستطيع المراجع تكرارها.

## 4. From measurement to plan — من القياس إلى الخطة

1. Paste `probe.json` values into STYLE.md section *Observed* and set the deliverable spec (aspect, fps, duration) unless the user asked otherwise.
2. Turn `cuts.json` into the first draft of PLAN.md scene boundaries; when the user supplies audio, `words.json` wins and cuts only inform pacing.
3. Convert the palette into design tokens; name them (`--ink`, `--paper`, `--accent`) and record which are measured and which are chosen.
4. Decide the stack from what you observed: draw-on strokes and typography → `starters/html-canvas`; React props and Studio preview → `starters/remotion`; true depth → Three.js (see `capabilities.md`, *space*).
5. Keep `REPORT.md` next to the project for the review step; delete the cache before sharing the repository.

**بالعربية:** انقل القياسات إلى STYLE.md، وحوّل القطعات إلى حدود مشاهد أولية في PLAN.md (الصوت المرفق يتقدّم عليها)، وسمِّ الألوان كرموز تصميم، واختر الحزمة بحسب ما لاحظته، واحذف الكاش قبل مشاركة المستودع.

## 5. Limits — الحدود

- No DRM, no encrypted HLS, no login walls, no scraping behind paywalls, no mass downloading; one reference per request is the norm.
- Default size cap 400 MB (`--max-mb`); a reference clip rarely needs more than the first minute — trim with `ffmpeg -t 60` before analysis if the file is long.
- The cloud machine has ffmpeg and Playwright but no GPU; optical-flow or detection models run elsewhere and their results are imported as numbers, never as media.

**بالعربية:** لا DRM ولا بث مشفّر ولا جدران دخول ولا تحميل جماعي. السقف الافتراضي 400 ميغابايت، ومقطع المرجع نادرًا ما يحتاج أكثر من الدقيقة الأولى.
