# أدوات المجال `edit` (18 أداة)

> مولّد من `data/tools.json`. [الفهرس الرئيسي](../README.md) · `python3 scripts/hub.py tool <id>` للبطاقة الحية.

### `cinema-lab` — معمل السينما: كشف القطعات، حذف الصمت، تايملاين OTIO/EDL، ألوان LUT، تثبيت الكاميرا، تأطير ذكي بالطول، حركة كاميرا، مراجعة A/B / Cinema Lab: scene cuts, silence cut, OTIO/EDL timelines, LUT looks, stabilise, smart portrait reframe, camera moves, A/B review

| الحقل | القيمة |
|---|---|
| المسار | `scripts/cinema_lab.py` (جذر: skill) |
| المجال | `edit` |
| الدليل | `tested-here` |
| العائلات | `photo-video-footage`, `transitions-cuts`, `camera-composition-layout`, `color-palette-grading` |

**ما تفعله:** محركات تصوير ومونتاج مكتوبة بكودنا من أفكار PySceneDetect وAuto-Editor وOpenTimelineIO وOpenColorIO وOpenCV وvid.stab وMotion Canvas/Remotion وOpenRV، وتشتغل بـ FFmpeg وNumPy في السحابة: يكشف القطعات ويطلع ستوري بورد، يحذف الصمت مع الحفاظ على تزامن الصوت والصورة، يصدّر التايملاين OTIO وEDL لبرامج المونتاج، يعمل ألوان سينمائية بملفات .cube، يثبت الكاميرا المهزوزة ويقيس الاهتزاز قبل وبعد، يحوّل الفيديو العريض لطولي 1080x1920 بكاميرا ذكية بتتبع الحركة، يعمل حركات كاميرا ناعمة على صورة أو فيديو، ويطلع فيديو مقارنة A/B بتايم كود ومقاييس SSIM/PSNR.

**What it does:** Cinematography and editing engines rebuilt in our own code from ideas in PySceneDetect, Auto-Editor, OpenTimelineIO, OpenColorIO, OpenCV, vid.stab, Motion Canvas/Remotion and OpenRV, running on FFmpeg + NumPy in a cloud sandbox. Detects scene cuts (FFmpeg scdet, or the real PySceneDetect ContentDetector when installed) with a storyboard contact sheet; removes silences with frame-grid cuts that keep audio and video in sync; exports any segment plan as OpenTimelineIO JSON (read back with the opentimelineio package when present) and a CMX3600 EDL for Kdenlive/Shotcut/Resolve/Premiere; builds portable 33^3 .cube looks and applies them with lut3d; stabilises with two-pass vid.stab and measures shake before/after by phase correlation; reframes landscape footage to a 1080x1920 portrait crop by tracking motion and detail with a smoothed, speed-capped virtual camera that re-aims at scene cuts; renders eased push-in/pan/tilt/ken-burns camera moves on stills or clips; and makes A/B side-by-side or wipe review videos with burnt-in timecode and SSIM/PSNR.

#### متى تُستدعى

- «Find every cut in this video and give me a storyboard of the scenes»
- «Remove the silent pauses from this talking video automatically»
- «Export the edit as an OTIO or EDL timeline I can open in Kdenlive, Resolve or Premiere»
- «Give this clip a teal and orange cinematic look and save the LUT»
- «Stabilise this shaky phone footage»
- «Turn this wide 16:9 video into a portrait crop that follows the action»
- «Add a slow cinematic push-in on this photo»
- «Compare the original and the graded version side by side»
- «اكشف القطعات والمشاهد في الفيديو واعملي ستوري بورد»
- «احذف السكتات والصمت من الفيديو تلقائي»
- «صدّر المونتاج تايملاين يفتح في كدينلايف أو ريزولف»
- «اعمل للفيديو لون سينمائي تيل أورنج»
- «ثبّت الفيديو المهزوز»
- «حوّل الفيديو العريض لفيديو بالطول يتابع الحركة»
- «اعمل زووم سينمائي بطيء على الصورة»
- «قارن الأصلي بالمعدّل جنب بعض»

#### الأوامر

- **doctor**: Check ffmpeg filters (scdet, lut3d, vid.stab, zoompan, sendcmd, ssim), optional Python libraries and the export defaults.
  - `python3 scripts/cinema_lab.py doctor`
- **scenes**: Detect cuts (--engine auto\|ffmpeg\|pyscenedetect) into scenes.json, plus storyboard.jpg and scenes.otio/.edl.
  - `python3 scripts/cinema_lab.py scenes --input ./film.mp4 --out ./scenes --sheet --timeline`
- **silence-cut**: Find silences (--noise dB, --min-silence s), keep speech with a margin snapped to the frame grid, render one synced file (or --plan-only).
  - `python3 scripts/cinema_lab.py silence-cut --input ./talk.mp4 --output ./tight.mp4 --timeline`
- **timeline**: Turn a kosif.segments.v1 plan into edit.otio and edit.edl.
  - `python3 scripts/cinema_lab.py timeline --plan ./scenes/scenes.json --out ./edit`
- **grade**: Apply a named look (teal-orange, bleach-bypass, warm-film, cool-night, noir, golden-hour) or --lut file.cube; measures the frame before/after. --cube-out alone exports the LUT.
  - `python3 scripts/cinema_lab.py grade --input ./clip.mp4 --output ./graded.mp4 --look teal-orange --strength 0.8 --cube-out ./teal.cube`
- **stabilize**: Two-pass vid.stab (or --deshake), audio copied; reports mean and p95 frame-to-frame shift before and after.
  - `python3 scripts/cinema_lab.py stabilize --input ./shaky.mp4 --output ./steady.mp4`
- **reframe**: Track motion and detail, smooth the virtual camera, re-aim at scene cuts and crop to 1080x1920; writes the camera path.
  - `python3 scripts/cinema_lab.py reframe --input ./wide.mp4 --output ./reel.mp4`
- **camera**: Eased push-in, pull-out, pan, tilt or ken-burns on a still or a clip, supersampled to avoid jitter.
  - `python3 scripts/cinema_lab.py camera --input ./photo.jpg --output ./push.mp4 --move push-in --duration 5`
- **review**: Side-by-side or wipe A/B review with labels and timecode; --metrics adds SSIM and PSNR.
  - `python3 scripts/cinema_lab.py review --a ./before.mp4 --b ./after.mp4 --output ./ab.mp4 --mode wipe --metrics`
- **tests**: Run 23 tests (export settings checked against export_profile.py): planning maths, LUTs, tracking and real FFmpeg runs (skipped without ffmpeg/numpy).
  - `python3 -m unittest discover -s evals -p 'test_cinema_lab.py' -v`

#### المتطلبات والأمان

- binaries: ffmpeg, ffprobe
- optional: scenedetect[opencv], opentimelineio
- python: numpy
- الأمان: writes-files
- الموافقة: Use only media the user owns or is licensed to edit; sources are never modified and outputs are new files.
- الحدود: Scene detection is a frame-difference score: soft dissolves and fast flashes can be missed or doubled, so check the storyboard. Silence cut re-encodes the audio (cutting changes timing) and works on loudness, not words; music beds hide pauses. Reframe tracks motion and detail energy, not faces or a named subject, and cannot recover action outside the crop. Looks are hand-built creative LUTs, used only when a look is asked for (the export standard matches colour to the source by default), not a calibrated ACES/OCIO pipeline. Stabilise cannot fix motion blur or rolling shutter. Camera moves are 2D crops, not 3D parallax.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_cinema_lab.py`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/edit.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:cinema-lab --evidence <ملف>`.

### `cinematic-broll-render` — تصيير لقطات B-roll بحركة كاميرا / Cinematic B-roll Renderer

| الحقل | القيمة |
|---|---|
| المسار | `scripts/cinematic_broll_render.py` (جذر: skill) |
| المجال | `edit` |
| الدليل | `tested-here` |
| العائلات | `photo-video-footage`, `camera-composition-layout`, `engines-render-pipeline`, `qa-verification` |

**ما تفعله:** يصيّر فيديو B-roll حقيقيًا بحركة كاميرا (تقريب وابتعاد وتحريك جانبي) عبر FFmpeg، انطلاقًا من قائمة EDL جاهزة للإنتاج وبيان لقطات مرخّصة. ينسخ مسار الصوت الأصلي دون أي تعديل، ويتحقق من عدد الإطارات ومن تطابق بصمة الصوت.

**What it does:** Renders a real camera-motion B-roll video master with FFmpeg from a production-ready cinematic_cut_planner EDL and a licensed footage manifest (push-in, pull-back and pan per shot, exact frame counts), stream-copies the original audio and verifies frame count and audio bitstream hash.

#### متى تُستدعى

- «صيّر لي فيديو B-roll بحركة كاميرا على الصوت الأصلي من غير ما يتغير»
- «طلّع لي ماستر فيديو من اللقطات المعتمدة والصوت الأصلي»
- «Render the EDL into a real video with slow push-ins and keep my audio bit-identical»
- «Turn the approved footage plan into an MKV master with Ken Burns camera moves»

#### الأوامر

- **render**: Checks EDL coverage and readiness, verifies each clip's license evidence, sha256, dimensions and length, renders every scene with an ffmpeg zoompan camera move to its exact frame count, concatenates the shots, muxes the original audio with -c:a copy, verifies frames and an identical audio packet hash, and prints a JSON report. It refuses to overwrite --out.
  - `python3 scripts/cinematic_broll_render.py --edl ./edl.json --manifest ./clips.json --audio ./voice.wav --out ./out/master.mkv --width 1080 --height 1920`

#### المتطلبات والأمان

- binaries: ffmpeg, ffprobe
- الأمان: runs-external-programs
- الموافقة: Renders the user's footage and audio with local ffmpeg: confirm each clip's license evidence and the user's rights to the audio before running.
- الحدود: Produces only a camera-motion B-roll master (every shot starts at its clip's first frame) with no captions, Arabic text, graphics, transitions or audio mix, and its rights checks trust the manifest's declared flags.

#### الاختبارات والأدلة

- `tests/test_cinematic_broll_render.py`
- مرجع: `docs/KOSIF_MEDIA_EDITOR_DEEP_RESEARCH_20261019.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/edit.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:cinematic-broll-render --evidence <ملف>`.

### `cinematic-cut-planner` — مُخطِّط قطعات اللقطات الحقيقية / Footage-First Cut Planner

| الحقل | القيمة |
|---|---|
| المسار | `scripts/cinematic_cut_planner.py` (جذر: skill) |
| المجال | `edit` |
| الدليل | `tested-here` |
| العائلات | `photo-video-footage`, `transitions-cuts`, `audio-sync-captions`, `camera-composition-layout` |

**ما تفعله:** يبني قائمة قرارات مونتاج (EDL) حتمية بصيغة JSON من توقيت الكلمات وبيان لقطات مرخّصة ومراجَعة: يقسّم المشاهد عند وقفات الكلام (0.6 ثانية فأكثر) أو حين يبلغ المشهد 7 ثوانٍ، ويختار لكل مشهد اللقطة الأنسب بحسب الوسوم، ويحدد حركة الكاميرا، ويسجّل النواقص بدل اختلاق لقطات.

**What it does:** Builds a deterministic JSON edit decision list (kosif.edl.v1) from word timings and a reviewed, licensed footage manifest: splits scenes at speech pauses of 0.6 s or more or once a scene reaches 7 s, picks the best tag-matching clip per scene, assigns camera moves and lists blockers instead of inventing footage.

#### متى تُستدعى

- «عندي تعليق صوتي وتوقيت كلمات ولقطات مرخصة، اعمل لي خطة مونتاج»
- «أبي EDL للفيديو مع حركة كاميرا لكل مشهد»
- «وزّع لقطات الـ B-roll على الجمل حسب الكلام»
- «Plan which licensed B-roll clip goes under each spoken phrase»
- «Make an edit decision list from words.json and my footage manifest»

#### الأوامر

- **plan**: Validates the words, rejects clips without license_verified=true, reviewed_frames>=3, contains_text=false, contains_excluded_people=false and is_moving_video=true, builds frame-exact 1080x1920 scenes covering the whole audio, and writes the EDL (creating parent dirs, overwriting silently). It prints {file,scenes,blockers,ready} and exits 0 when production_ready, 2 when blockers remain.
  - `python3 scripts/cinematic_cut_planner.py --words ./words.json --clips ./clips.json --duration 48.5 --fps 30 --out ./out/edl.json`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: Nothing to approve for running it, but the license_verified, reviewed_frames, contains_text and contains_excluded_people flags in clips.json must come from the user's real review of the footage; Claude must not set them by inference.
- الحدود: Plans only: it does not inspect footage pixels, transcribe, download or render anything, and matches clips purely by word/tag overlap.

#### الاختبارات والأدلة

- `tests/test_cinematic_cut_planner.py`
- `tests/test_cinematic_broll_render.py`
- مرجع: `docs/REA_FILM_EDIT_CAPABILITY_STUDY_20261019.md`
- مرجع: `docs/KOSIF_MEDIA_EDITOR_DEEP_RESEARCH_20261019.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/edit.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:cinematic-cut-planner --evidence <ملف>`.

### `creative-quality-gate` — بوابة جودة خطة المونتاج / Reference-edit structural quality gate

| الحقل | القيمة |
|---|---|
| المسار | `scripts/creative_quality_gate.py` (جذر: skill) |
| المجال | `edit` |
| الدليل | `tested-here` |
| العائلات | `qa-verification`, `transitions-cuts`, `audio-sync-captions` |

**ما تفعله:** يدقّق ملف خطة مونتاج مرجعي من KOSIF ‏(plan.json بمخطط kosif.reference-edit.v1). يتحقق من اتساق ساعة الإطارات، ومن تتابع اللقطات بلا فجوات ولا تداخل، ومن أن نبضات الإيقاع داخل حدود لقطاتها، ومن أنه لا توجد كلمة موقّتة تعبر قطعًا حادًا، ومن سلامة أسماء ملفات الوسائط المحلية (ومن وجودها فعلًا إن أُعطي مشروع Remotion)، ومن صدق مؤشرات الإثبات. ثم يكتب تقرير تدقيق JSON جديدًا حالته إما structurally_verified_render_pending (سليم بنيويًا وبانتظار التصيير) أو blocked (محجوب).

**What it does:** Audits a KOSIF reference-edit plan.json (schema kosif.reference-edit.v1). It checks the fps/frame clock, gap-free and overlap-free shot frames, bounded pulse cues, that no aligned word crosses a hard cut, safe local media names (and, with an optional Remotion project, that those files exist), and honest evidence flags. It writes a new audit JSON whose status is structurally_verified_render_pending or blocked.

#### متى تُستدعى

- «افحص خطة المونتاج دي قبل الريندر: فيه فجوات بين اللقطات؟»
- «تأكد إن ما في كلمة مقطوعة بين لقطتين في plan.json»
- «تحقّق من أن مشروع Remotion يحتوي كل المقاطع البديلة المذكورة في الخطة»
- «Run the quality gate on my Remotion reference-edit plan»
- «Check that every frame belongs to exactly one shot and the evidence flags are honest»

#### الأوامر

- **audit**: Validates the plan and writes a NEW audit JSON (exclusive create: an existing file is refused, and the --out parent folder must already exist). Prints {status, failures, audit} and exits 0 when all five gates pass, or 2 when any gate fails or the input/output path is invalid.
  - `python3 scripts/creative_quality_gate.py ./my-project/src/plan.json --out ./out/quality-audit.json`
- **audit-with-project**: Also requires every referenced clip_NNN.<ext> and audio.<ext> file to exist under <project>/public/assets.
  - `python3 scripts/creative_quality_gate.py ./my-project/src/plan.json --project-dir ./my-project --out ./out/quality-audit.json`
- **inspect_plan (import)**: Runs the same checks in memory and returns the report dict without writing anything. scripts/reference_edit_engine.py calls this automatically before it finishes a project and writes quality-audit.json.
  - `python3 -c "import sys,json; sys.path.insert(0,'scripts'); import creative_quality_gate as q; print(q.inspect_plan(json.load(open('./plan.json')))['status'])"`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: —
- الحدود: It checks only the plan's structure and timing logic; it never renders or inspects the MP4's visuals, audio sync, rights or aesthetic quality.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_creative_quality_gate.py`
- مرجع: `.claude/skills/kosif-superpowers/references/creative-quality-gates.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/edit.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:creative-quality-gate --evidence <ملف>`.

### `dua-wednesday` — دعاء يوم الأربعاء — محرك ريل دعاء موشن جرافيك 9:16 / Wednesday-morning dua reel (دعاء يوم الأربعاء) — 9:16 motion-graphics dua engine

| الحقل | القيمة |
|---|---|
| المسار | `scripts/dua_wednesday.py` (جذر: skill) |
| المجال | `edit` |
| الدليل | `tested-here` |
| العائلات | `transitions-cuts`, `audio-sync-captions`, `photo-video-footage`, `formats-platforms` |

**ما تفعله:** يعيد أسلوب ريل دعاء صباح الأربعاء المعتمد على لقطات وصوت جديدين: عبارة لكل لقطة مرخصة بقطع قبل بداية الصوت وتسعة انتقالات مختلفة، ونص عربي كلمة كلمة بتوقيت Whisper وطاقة الصوت مع تمييز ذهبي للكلمة المنطوقة، وعنوان اليوم بخط رقعة ذهبي تحت محراب يُرسم ويعلوه هلال، وغبار ذهبي وأشعة وتوهج وتدرج دافئ. الصوت يُنسخ دون أي تعديل ويُتحقق منه بايتًا ببايت.

**What it does:** Rebuilds the approved Wednesday-morning dua reel style on new footage and voice: one dua phrase per licensed shot cut just before the voice onset with nine different transitions (light leak, whip, gold ink reveal, zoom-through, gold iris, film burn, spin zoom, bokeh, slide), word-by-word Arabic text timed with faster-whisper and audio energy with a gold karaoke highlight, a gold Ruqaa day title under a drawn-on mihrab crowned by a crescent, golden dust, god rays, bloom, warm grade and grain. The voice is stream-copied and checked byte for byte.

#### متى تُستدعى

- «اعمل الفيديو ده بنفس استايل دعاء يوم الأربعاء»
- «دعاء الصباح ريلز بنفس الأسلوب مع لقطات جديدة»
- «Make this dua video in the same Wednesday dua style»
- «حوّل فيديو الدعاء ده لموشن جرافيك 9:16 بخطوط ذهبية وانتقالات»

#### الأوامر

- **doctor**: Lists binaries, Python modules, Playwright and fonts.
  - `python3 scripts/dua_wednesday.py doctor`
- **fetch**: Downloads the source (yt-dlp, TikTok fallback) and stream-copies its audio to voice.m4a.
  - `python3 scripts/dua_wednesday.py fetch "https://vt.tiktok.com/XXXX/" --job ./dua1`
- **caption-times**: On-screen caption onsets of the reference reel.
  - `python3 scripts/dua_wednesday.py caption-times ./dua1/source.mp4`
- **asr**: faster-whisper word timings + energy-refined phrase onsets → words.json, lines.draft.json.
  - `python3 scripts/dua_wednesday.py asr --job ./dua1 --model medium`
- **init**: Copies the approved Wednesday project.json to edit.
  - `python3 scripts/dua_wednesday.py init --job ./dua1`
- **prep**: Licensed clips → 1080×1920 30 fps sharpened mezzanine (SRC:X sets the crop).
  - `python3 scripts/dua_wednesday.py prep --job ./dua1 sunrise.mp4 candle.mp4:556`
- **sprites**: Renders title, date, subtitle and per-word dua sprites in Chromium.
  - `python3 scripts/dua_wednesday.py sprites --job ./dua1`
- **stills**: Review frames.
  - `python3 scripts/dua_wednesday.py stills --job ./dua1 --t 1.6,5.4,20`
- **render**: Parallel render, concat, untouched audio, TikTok copy, frame and audio checks.
  - `python3 scripts/dua_wednesday.py render --job ./dua1 --workers 4`

#### المتطلبات والأمان

- binaries: ffmpeg, ffprobe, node
- node: playwright
- optional: pip:faster-whisper, bin:yt-dlp
- python: numpy, opencv-python-headless
- الأمان: runs-external-programs
- الموافقة: fetch downloads the user's link (and may call the public tikwm.com endpoint for TikTok); asr downloads a Whisper model from huggingface.co once; footage must be the user's own or licensed (Mixkit, CC).
- الحدود: Fixed 1080×1920 layout for short Arabic phrases; ASR drafts need a human spelling pass; licensed stock is often 720p landscape, so crops are upscaled; loudness is left as in the source.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_dua_wednesday.py`
- مرجع: `.claude/skills/kosif-superpowers/dua-wednesday/WORKFLOW.md`
- مرجع: `.claude/skills/kosif-superpowers/dua-wednesday/README.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:dua-wednesday --evidence <ملف>`.

### `fast-edit` — التعديل السريع: قص فوري يعرف الإطارات المفتاحية، مغيّر صوت، تفتيح الفيديو المظلم، استخراج الصوت / Fast Edit: keyframe-aware instant cut, voice presets, low-light lift, audio extract

| الحقل | القيمة |
|---|---|
| المسار | `scripts/fast_edit.py` (جذر: skill) |
| المجال | `edit` |
| الدليل | `tested-here` |
| العائلات | `photo-video-footage`, `transitions-cuts`, `audio-sync-captions` |

**ما تفعله:** عمليات سريعة على ملف واحد بإيصال JSON: يعرض الإطارات المفتاحية، ويقص بالنسخ المباشر لو البداية على إطار مفتاحي وإلا يعيد الترميز بدقة ويقول قد إيه كان النسخ هيبدأ بدري، ويغيّر الصوت بنفس معدل العينة ونفس الطول، ويفتّح الفيديو المظلم ويقيس الإضاءة قبل وبعد، ويستخرج الصوت بدون إعادة ترميز لما ينفع.

**What it does:** Single-file FFmpeg operations with JSON receipts: lists keyframes; cuts by stream copy when the start sits on (or within a tolerance of) a keyframe and by exact re-encode otherwise, reporting how far a copy would have drifted; applies voice presets (chipmunk, deep, robot, echo, radio, telephone) at the file's real sample rate with the length kept and video stream-copied; lifts low-light video with an optional denoise and measures mean luma before and after, skipping clips that are already bright; extracts audio bit-exact when the container allows it.

#### متى تُستدعى

- «Cut a clip from 1:05 to 1:40 instantly without re-encoding if possible»
- «Make this voice sound like a chipmunk / robot / radio without changing its length»
- «Brighten this dark night video and remove the noise»
- «Extract the audio from this video without losing quality»
- «قص الفيديو من الدقيقة دي للدقيقة دي بسرعة من غير ما يبوظ الجودة»
- «غيّر الصوت لصوت روبوت أو صوت تخين»
- «فتّح الفيديو المظلم وشيل التشويش»
- «استخرج الصوت من الفيديو»

#### الأوامر

- **doctor**: Check ffmpeg/ffprobe and list the voice presets.
  - `python3 scripts/fast_edit.py doctor`
- **keyframes**: List video keyframe times and the largest gap between them.
  - `python3 scripts/fast_edit.py keyframes --input ./clip.mp4`
- **cut**: Cut [start, end): stream copy when the start is within --tolerance of a keyframe, exact re-encode otherwise (--mode copy\|exact forces one); the receipt gives the copy drift and measured stream durations.
  - `python3 scripts/fast_edit.py cut --input ./clip.mp4 --start 65 --end 100 --output ./cut.mp4`
- **voice**: Apply a voice preset at the real sample rate, keeping the length; video is stream-copied (audio-only extensions drop it).
  - `python3 scripts/fast_edit.py voice --input ./talk.mp4 --preset robot --output ./robot.mp4`
- **brighten**: Lift shadows and midtones (strength 0..1, optional hqdn3d denoise), audio stream-copied; reports mean luma before/after and skips clips that are already bright unless --force-lift.
  - `python3 scripts/fast_edit.py brighten --input ./night.mp4 --denoise --output ./lifted.mp4`
- **extract-audio**: Extract the first audio stream: bit-exact copy when the extension can hold the codec, otherwise re-encoded (WAV, FLAC, MP3, M4A, AAC, Opus, Ogg).
  - `python3 scripts/fast_edit.py extract-audio --input ./clip.mp4 --output ./voice.m4a`
- **tests**: Run 17 tests: cut planning, filter building and real FFmpeg runs (skipped without ffmpeg).
  - `python3 -m unittest discover -s evals -p 'test_fast_edit.py' -v`

#### المتطلبات والأمان

- binaries: ffmpeg, ffprobe
- الأمان: writes-files
- الموافقة: Use only media the user owns or is licensed to edit; outputs are new files.
- الحدود: One file per command, no timeline. A copy cut starts on the keyframe at or before the start and may keep a frame or two past the end (B-frame reordering); use --mode exact for frame accuracy. Voice presets are classic DSP effects, not AI voice conversion. Brighten is a fixed tone curve measured by mean luma, not a learned low-light model.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_fast_edit.py`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/edit.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:fast-edit --evidence <ملف>`.

### `kosif-timeline` — محرر KOSIF Timeline: مونتاج متعدد المسارات مع تراجع وإعادة / KOSIF Timeline: genuine multitrack video, image and audio editor

| الحقل | القيمة |
|---|---|
| المسار | `scripts/kosif_timeline.py` (جذر: skill) |
| المجال | `edit` |
| الدليل | `tested-here` |
| العائلات | `photo-video-footage`, `transitions-cuts`, `audio-sync-captions`, `engines-render-pipeline` |

**ما تفعله:** مشروع مونتاج يحفظ المسارات واللقطات والصوت، ويسمح بالقص والتحريك والتلاشي والتراجع والإعادة، ويصدر فيديو H264 بصوت AAC بعد التحقق.

**What it does:** Original non-destructive JSON timeline with trimmed sources, ordered video/image layers, per-clip alpha fades, independent audio mixing, reversible move/trim/fade edits, H264/AAC export via FFmpeg and FFprobe verification.

#### متى تُستدعى

- «Cut, trim, and position several owned videos/images/audio clips on a timeline»
- «Produce a multitrack MP4 with overlapping fades and mixed music»
- «رتب مقاطع الفيديو والصور والصوت على تايملاين وصدّر MP4»

#### الأوامر

- **doctor**: Check FFmpeg/FFprobe installation and project schema support.
  - `python3 scripts/kosif_timeline.py doctor`
- **demo**: Create fully synthetic audio/video/image source files and an editable JSON timeline, then render and verify MP4.
  - `python3 scripts/kosif_timeline_demo.py --dir ./kosif-timeline-new-demo`
- **check**: Validate local media, track/clip bounds, stream metadata and source durations.
  - `python3 scripts/kosif_timeline.py check --project ./project.json`
- **render**: Render ordered video/image layers and mixed audio to FFprobe-verified H264/AAC with SHA256 receipt.
  - `python3 scripts/kosif_timeline.py render --project ./project.json --output ./new-export.mp4`
- **edit**: Create immutable project revision for clip move, trim, or fade.
  - `python3 scripts/kosif_timeline.py edit --project ./project.json --operation move --clip badge --start 0.6 --output ./revision.json`
- **undo**: Restore one edit snapshot without changing original project.
  - `python3 scripts/kosif_timeline.py undo --project ./revision.json --output ./undone.json`
- **redo**: Re-apply a previously undone project revision.
  - `python3 scripts/kosif_timeline.py redo --project ./undone.json --output ./redone.json`
- **tests**: Run 17 end-to-end/unit regression tests including real video/audio export and undo/redo.
  - `python3 scripts/test_kosif_timeline.py`

#### المتطلبات والأمان

- binaries: ffmpeg, ffprobe
- python: Pillow
- الأمان: writes-files
- الموافقة: Use only media that belongs to the user or is licensed for reuse, output a new file, no commercial proprietary source code.
- الحدود: Command-line/JSON editor not visual drag/drop; <=60s, 1..30fps, 32 clips, 12 tracks, <=300M pixel-frames, 1GB per source. Basic alpha fades only, no frame-level keyframes, captions, camera capture, AI editing, color grading, or word alignment in this tool. Audio AAC is re-encoded.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/scripts/test_kosif_timeline.py`
- مرجع: `.claude/skills/kosif-superpowers/references/kosif-timeline-multitrack-20261020.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:kosif-timeline --evidence <ملف>`.

### `kosif-timeline-demo` — تجربة مونتاج KOSIF Timeline تلقائية بملفات أصلية مولدة / KOSIF Timeline one-command synthetic media demo

| الحقل | القيمة |
|---|---|
| المسار | `scripts/kosif_timeline_demo.py` (جذر: skill) |
| المجال | `edit` |
| الدليل | `tested-here` |
| العائلات | `photo-video-footage`, `transitions-cuts`, `engines-render-pipeline` |

**ما تفعله:** توليد مصادر صوت وفيديو وصورة تجريبية محليًا ثم إخراج مشروع تايملاين قابل للتعديل وفيديو مع تقرير تحقق بضغطة أمر.

**What it does:** Generate fresh, synthetic H264 video, PCM WAV and PNG media, a complete editable 3-track timeline JSON and a verified 36-frame H264/AAC MP4 in a new folder.

#### متى تُستدعى

- «Prove the KOSIF multitrack timeline works with a reproducible end-to-end video»
- «Build a local self-contained demo before applying real owned footage»
- «جرّب مونتاج مسارات الفيديو والصوت والصور وتأكد من التصدير»

#### الأوامر

- **run-demo**: Generate a fresh project folder containing source assets, timeline project.json, H264/AAC timeline.mp4 and receipt.json.
  - `python3 scripts/kosif_timeline_demo.py --dir ./fresh-kosif-timeline-demo`

#### المتطلبات والأمان

- binaries: ffmpeg, ffprobe
- python: Pillow
- الأمان: writes-files
- الموافقة: Never use third-party files; runs only FFmpeg synthetic generators and Pillow, creates a new directory.
- الحدود: Smoke/demo only at 480x270, 3 sec, 12fps. Does not implement a graphical editor; non-destructive original media only.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/scripts/test_kosif_timeline.py`
- مرجع: `.claude/skills/kosif-superpowers/references/kosif-timeline-multitrack-20261020.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:kosif-timeline-demo --evidence <ملف>`.

### `look-pipeline` — خط اللوك: تلوين واحد لـ ffmpeg وSVG وGLSL / Look pipeline: one colour grade for ffmpeg, SVG/CSS and GLSL

| الحقل | القيمة |
|---|---|
| المسار | `scripts/look_pipeline.py` (جذر: skill) |
| المجال | `edit` |
| الدليل | `tested-here` |
| العائلات | `color-palette-grading`, `app-feature-transfer`, `photo-video-footage` |

**ما تفعله:** كُتبت بعد دراسة «مونتاجي»: 11 لوكًا وثمانية معاملات تصبح خطوة خطية ومصفوفة 3×3، تخرج بالأرقام نفسها لـ ffmpeg وSVG وCSS وGLSL فتتطابق المعاينة والتصدير؛ verify يقيس الفرق بكسلًا بكسلًا، وapply يلوّن فيديو في ملف جديد.

**What it does:** Written after a read-only study of the Montaji Arabic video editor: eleven colour looks (natural, vivid, bright, warm, cool, cinematic, vintage, faded, dramatic, mono, night-dua) and eight parameters become one per-channel affine step plus one 3x3 matrix, emitted with the same numbers as an ffmpeg chain (lutrgb + colorchannelmixer + vignette), an SVG filter, CSS and a GLSL shader. verify pushes a test frame through ffmpeg and compares every pixel with the reference maths; apply grades a video into a new file.

#### متى تُستدعى

- «لوّن الفيديو ده لوك سينمائي وخلي المعاينة زي التصدير»
- «Give me the same warm grade as an ffmpeg filter and a CSS filter»
- «Check that my web preview colour matches the exported MP4»
- «عايز فلتر أبيض وأسود للفيديو»

#### الأوامر

- **presets**: The eleven looks and their parameters.
  - `python3 scripts/look_pipeline.py presets`
- **build**: Emit one look for ffmpeg, svg, css, glsl or json, with --set overrides.
  - `python3 scripts/look_pipeline.py build --preset cinematic --amount 0.8 --target ffmpeg`
- **verify**: ffmpeg output vs the reference maths on a 64x36 test frame; exits 1 above the tolerance.
  - `python3 scripts/look_pipeline.py verify --all`
- **apply**: Grade a video into a new H.264 file, audio copied; refuses to overwrite.
  - `python3 scripts/look_pipeline.py apply in.mp4 graded.mp4 --preset warm --amount 0.6`

#### المتطلبات والأمان

- binaries: ffmpeg
- الأمان: writes-files
- الموافقة: apply writes a new file next to the user's media and never overwrites the source.
- الحدود: Per-pixel looks only (no curves, LUT files or skin masks); vignette is emitted for every renderer but left out of the parity check; SVG and GLSL parity follow from the same numbers and are not rendered here.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_look_pipeline.py`
- مرجع: `.claude/skills/kosif-superpowers/references/app-studies/montaji.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:look-pipeline --evidence <ملف>`.

### `mimic` — محرك محاكاة الفيديو المرجعي / KOSIF Mimic reference rebuilder

| الحقل | القيمة |
|---|---|
| المسار | `scripts/mimic/` (جذر: skill) |
| المجال | `edit` |
| الدليل | `tested-here` |
| العائلات | `photo-video-footage`, `transitions-cuts`, `typography-arabic`, `color-palette-grading` |

**ما تفعله:** محرك بايثون يحلّل فيديو مرجعيًا (مصمَّم للريلز العمودية) إلى ملف spec.json يضم: اللقطات، والانتقالات مصنّفةً ضمن 65 نوعًا مع منحنيات تقدّمها المقاسة، وأحداث النص العربي المتحرك مع أسلوبه ومرشحي الخط، والطابع اللوني (تدرج Lab، والتعتيم الطرفي، والحبيبات، والأشرطة السوداء، والتلاشي). ثم يعيد بناء الفيلم نفسه بلقطات بديلة جديدة في ملف MP4 واحد بترميز H.264 مع نسخ مسار الصوت الأصلي كما هو دون تعديل.

**What it does:** A Python engine that analyses a reference video (built for vertical reels) into spec.json: shots, transitions classified among 65 kinds with measured progress curves, animated Arabic text events with their style and font candidates, and the look (Lab grade, vignette, grain, letterbox, fades). It then rebuilds the same film from new replacement clips into one H.264 MP4 that copies the original audio stream untouched.

#### متى تُستدعى

- «عايز نفس الفيديو ده بس باللقطات بتاعتي»
- «حلّل الريل المرجعي: الانتقالات والكتابة والخطوط والألوان»
- «أبي أعيد بناء هالفيديو بمقاطعي مع نفس النص والتوقيت»
- «Rebuild this reference reel with my own footage, same transitions and text timing»
- «Analyse the transitions, text animation and colour look of this reference video»

#### الأوامر

- **analyze**: Writes work/spec.json, the Arabic work/analysis.md, review sheets in work/sheets (plus frames/text/cache folders), and copies the original audio stream into work/audio without re-encoding (plus a 48 kHz WAV for analysis). Optional arguments: text_color, sensitivity, skip_text, deep.
  - `python3 -c "import sys; sys.path.insert(0,'scripts/mimic'); import mm_analyze; mm_analyze.analyze('./in.mp4','./work')"`
- **match_fonts**: Ranks Arabic font faces (shipped OFL fonts, the fetched cache, work/fonts and system fonts) against each text line's mask and updates spec.json plus font sheets. Each line's text must first be typed into spec.json (or come from OCR); otherwise the event gets a 'no line text yet' note. Optional arguments: families, top, engine, extra_dirs, include_system.
  - `python3 -c "import sys; sys.path.insert(0,'scripts/mimic'); import mm_fonts; mm_fonts.match('./work')"`
- **build_preview**: Renders a half-size work/remake_preview.mp4 and work/build/preview/build_report.json. Every shots[].replacement.path must be set in spec.json.
  - `python3 -c "import sys; sys.path.insert(0,'scripts/mimic'); import mm_build; mm_build.build('./work', preview=True)"`
- **build_placeholder**: Draft render that uses shot-coloured placeholder plates wherever replacement footage is missing.
  - `python3 -c "import sys; sys.path.insert(0,'scripts/mimic'); import mm_build; mm_build.build('./work', preview=True, placeholder=True)"`
- **build**: Full-size work/remake.mp4: H.264 bt709 CRF 17 (preset medium), same size and frame count, with the original audio stream copied (-c:a copy).
  - `python3 -c "import sys; sys.path.insert(0,'scripts/mimic'); import mm_build; mm_build.build('./work')"`
- **make_reference**: Generates a synthetic 9:16 ground-truth reference (ref.mp4, truth.json, clips/*.mp4) with known transitions, text events and fonts. Options: --w, --h, --fonts (default proofs/_shared/fonts). Needs OpenCV.
  - `python3 scripts/mimic/synthetic/make_reference.py ./out/ref`
- **run_synthetic**: End-to-end regression: analyses the synthetic reference, fills each line's text from truth.json, matches fonts and prints the TRANSITIONS / TEXT EVENTS / FONTS scorecard. --skip-analyze reuses an existing work/spec.json.
  - `python3 scripts/mimic/synthetic/run_synthetic.py ./out/ref ./out/work`
- **make_candidates**: Meant to write synthetic replacement-clip candidates and decoys plus candidates.json. Currently broken: the burned-in-text decoy loads scripts/mimic/assets/fonts/Cairo-700.ttf, which does not exist, so it fails after the first 8 clips. Takes a bare positional OUT_DIR (no argparse).
  - `python3 scripts/mimic/synthetic/make_candidates.py ./out/candidates`
- **fonts-list**: Lists the usable faces with Arabic coverage (core bundle from proofs/_shared/fonts and fonts/kosif-jumuah, the cache, and system fonts) with weight, style and source. Read-only.
  - `python3 scripts/mimic/mm_fonts_lib.py list`
- **fonts-fetch**: NETWORK: sparse-clones github.com/google/fonts with git (or falls back to raw.githubusercontent.com) and copies or instances OFL Arabic families into --dest (default ~/.cache/kosif-mimic/fonts). --only takes google/fonts ofl directory names.
  - `python3 scripts/mimic/mm_fonts_lib.py fetch --only amiri cairo`
- **fonts-build-ofl**: Copies or instances catalogue families from a local google/fonts 'ofl' checkout into --dest and writes fonts.json (offline). --ofl is required in practice: without it the script crashes with a TypeError.
  - `python3 scripts/mimic/mm_fonts_lib.py build-ofl --ofl ./google-fonts/ofl --dest ./out/fonts`

#### المتطلبات والأمان

- binaries: ffmpeg
- network: true
- optional: bin:ffprobe, bin:git, bin:tesseract, pip:imageio-ffmpeg, pip:opencv-python, pip:scipy
- python: Pillow, fonttools, numpy
- الأمان: network
- الموافقة: The user must confirm the right to analyse the reference video and must supply owned or licensed replacement footage (no platform scraping). mm_fonts_lib.py fetch downloads Google Fonts (OFL) from GitHub into ~/.cache/kosif-mimic/fonts, so confirm network use and that write location first.
- الحدود: OCR runs only when tesseract and assets/tessdata/ara.traineddata are present (neither is shipped), so event text is normally typed by hand; there are no stickers or emoji; commercial Thuluth/Diwani faces become the closest free font unless the user supplies the file; and accuracy on real footage is lower than the synthetic proof (6/6 transitions, 5/5 fonts, 3/5 text timing within ±2 frames).

#### الاختبارات والأدلة

- `tests/test_mimic.py`
- مرجع: `.claude/skills/kosif-superpowers/references/mimic.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/edit.md`
- مرجع: `.claude/skills/kosif-superpowers/references/capabilities.md`
- مرجع: `.claude/skills/kosif-superpowers/proofs/mimic-synthetic/README.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:mimic --evidence <ملف>`.

### `montage-pro` — فريق مونتاج برو (صوت أو فيديو إلى مونتاج أو موشن) / Montage Pro task force (audio/video to montage or motion)

| الحقل | القيمة |
|---|---|
| المسار | `scripts/montage_pro.py` (جذر: skill) |
| المجال | `edit` |
| الدليل | `tested-here` |
| العائلات | `transitions-cuts`, `audio-sync-captions`, `photo-video-footage`, `formats-platforms` |

**ما تفعله:** فريق من 13 دورًا لملف صوت أو فيديو مرفوع: يقيس المادة، ويعرض قائمة خيارات وخطة مراحل، ويجلب لقطات مرخصة بأسلوب IDM مع سجل حقوق، ويوحد الصيغ، وينتج فيلم موشن أو مصوّرًا صوتيًا أو إعادة تأطير أو ريلًا مختصرًا أو لوكًا سينمائيًا أو مشروع Remotion، مع فحص كل ناتج والحفاظ على الصوت الأصلي، وأمر transcribe يكتب توقيت الكلمات (words.json بصيغة kosif-words/1) محليًا بـ faster-whisper مع تخطي الصمت ورفض الكتابة داخل jobs/ أو الملفات المتتبعة.

**What it does:** A 13-role team over an uploaded audio or video: measures it (ffprobe, loudness, energy cues, cuts, contact sheet), offers an option menu with a stage plan, acquires licensed footage IDM-style (segmented resumable download, DASH/HLS grab, rights.json), conforms to an edit mezzanine with proxies, and builds a kinetic film, visualizer, reframe, highlight reel, look or a reference-remix Remotion project, each verified with verify_video.py; the master audio is never modified; its transcribe command writes word timings (kosif-words/1 words.json) locally with faster-whisper, skipping silence and refusing to write into jobs/ or tracked paths.

#### متى تُستدعى

- «رفعت فويس اعمل له موشن جرافيك»
- «اعمل ريلز من الفيديو ده على أقوى اللقطات»
- «Turn this interview into a 9:16 reel with a cinematic look»
- «حمّل اللقطة دي برخصتها وجهزها للمونتاج»
- «فرّغ الصوت ده كلمة كلمة بتوقيتها عشان الكتابة تمشي مع الصوت»
- «Transcribe my Arabic voice-over into word timings for captions»

#### الأوامر

- **doctor**: Tools present and ready options.
  - `python3 scripts/montage_pro.py doctor`
- **intake**: Measures the media into job1/intake.json.
  - `python3 scripts/montage_pro.py intake ./voice.wav --job ../../../out/job1`
- **transcribe**: Decodes the audio with ffmpeg to 16 kHz mono and runs faster-whisper (CPU, int8, word timestamps, Silero VAD) into job1/words.json in schema kosif-words/1 (source sha256, engine, words, phrases); drops segments above --no-speech-threshold and lists them; skips when the source and engine are unchanged unless --force; refuses jobs/, git-tracked or un-ignored targets unless --allow-tracked; exit 2 with one line when ffmpeg, faster-whisper or the cached model is missing. After an earlier intake it also refreshes JOB/work/cues.json so a later build uses the new words.
  - `python3 scripts/montage_pro.py transcribe ./voice.m4a --job ../../../out/job1 --language ar --local-only`
- **intake with transcription**: Opt-in: transcribes right after the probe so the cue mapper imports the aligned words; plain intake is unchanged.
  - `python3 scripts/montage_pro.py intake ./voice.m4a --job ../../../out/job1 --transcribe --local-only`
- **options**: Option menu with team, pipeline, status and a stage plan.
  - `python3 scripts/montage_pro.py options ../../../out/job1 --brief "ريلز حماسي"`
- **build**: Renders and verifies the option; optional separate -14 LUFS delivery copy.
  - `python3 scripts/montage_pro.py build ../../../out/job1 --option kinetic-film --style kinetic --deliver-mix`
- **acquire**: Licence-gated download or stream grab into job1/footage with rights.json.
  - `python3 scripts/montage_pro.py acquire https://example.com/clip.mp4 --job ../../../out/job1 --license "CC0" --source-page https://example.com/page`

#### المتطلبات والأمان

- binaries: ffmpeg, ffprobe
- optional: bin:chromium, bin:node, bin:yt-dlp, pip:faster-whisper, pip:numpy
- الأمان: runs-external-programs
- الموافقة: build runs ffmpeg/Chromium and writes new files in the job folder; acquire downloads only with a licence note and refuses DRM sources
- الحدود: broll-documentary, character and 3d-scene need words.json, clips or a scene JSON first; tests use synthetic media, not real user footage. Transcription word-timing accuracy is not measured against a reference: on the 14.7 s Arabic dua audio (medium, int8, 4 CPU cores) it took 14–28 s per run and three runs gave byte-identical words.json.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_montage_pro.py`
- مرجع: `.claude/skills/kosif-superpowers/montage-pro/README.md`
- مرجع: `.claude/skills/kosif-superpowers/montage-pro/IDM_STUDY.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:montage-pro --evidence <ملف>`.

### `motion-reference-probe` — فاحص توقيت الفيديو المرجعي / Reference Video Timing Probe

| الحقل | القيمة |
|---|---|
| المسار | `scripts/motion_reference_probe.py` (جذر: skill) |
| المجال | `edit` |
| الدليل | `tested-here` |
| العائلات | `transitions-cuts`, `photo-video-footage` |

**ما تفعله:** يقرأ فيديو محليًا مصرّحًا به عبر ffprobe لاستخراج المدة والأبعاد ومعدل الإطارات ووجود الصوت، ويشغّل اختياريًا كشف تغيّر المشاهد عبر FFmpeg، ثم يخرج تقرير توقيت بصيغة JSON بنقاط القطع المرشّحة والمقاطع، وهو مُدخل تحتاجه أدوات المونتاج اللاحقة.

**What it does:** Reads an authorized local video with ffprobe (duration, size, fps, audio presence) and optionally runs ffmpeg scene-change detection, producing a JSON timing report of cut candidates and segments that downstream KOSIF edit tools require.

#### متى تُستدعى

- «شوف الفيديو المرجعي ده فيه كام قطع وفين»
- «أبي أعرف مدة وأبعاد ومعدل فريمات هالفيديو»
- «Detect the cut points in this reference reel»
- «Get duration, resolution and fps of my clip before editing»
- «حلّل إيقاع القطعات في الفيديو المرجعي قبل ما نبني المونتاج»

#### الأوامر

- **metadata**: Runs ffprobe only and prints the full JSON report (width, height, fps_rational, duration_seconds, audio_present, one segment) to stdout; it writes nothing.
  - `python3 scripts/motion_reference_probe.py ./in.mp4`
- **cuts**: Also runs ffmpeg select=gt(scene,threshold),showinfo to list cut candidates (>=0.25 s apart, not within 0.2 s of the ends) and segments, saves them to a new JSON file (never overwrites) and prints {status,saved,cuts}.
  - `python3 scripts/motion_reference_probe.py ./in.mp4 --cuts --threshold 0.35 --out ./cuts.json`

#### المتطلبات والأمان

- binaries: ffprobe
- optional: bin:ffmpeg
- الأمان: runs-external-programs
- الموافقة: Reads a user-supplied local video with ffprobe/ffmpeg: confirm the user owns or is authorized to analyze it.
- الحدود: Cut candidates are heuristic scene-change detections that can miss dissolves or fire on flashes, and it does no object, motion, speech or semantic analysis.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_motion_reference_probe.py`
- `.claude/skills/kosif-superpowers/evals/test_reference_visual_style.py`
- مرجع: `.claude/skills/kosif-superpowers/references/executable-creative-motion.md`
- مرجع: `.claude/skills/kosif-superpowers/references/reference-edit-execution.md`
- مرجع: `.claude/skills/kosif-superpowers/references/reference-visual-transfer.md`
- مرجع: `.claude/skills/kosif-superpowers/references/capability-operating-manual.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/edit.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/motion.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:motion-reference-probe --evidence <ملف>`.

### `nle-export` — تصدير للبرامج: افتح تايملاين KOSIF في دافنشي وفاينال كت وبريمير وبلندر وكاب كات / NLE Export: open a KOSIF timeline in DaVinci Resolve, Final Cut Pro, Premiere Pro, Blender or CapCut

| الحقل | القيمة |
|---|---|
| المسار | `scripts/nle_export.py` (جذر: skill) |
| المجال | `edit` |
| الدليل | `tested-here` |
| العائلات | `photo-video-footage`, `transitions-cuts`, `audio-sync-captions`, `engines-render-pipeline` |

**ما تفعله:** يحوّل مشروع التايملاين أو خطة القطع لملفات تايملاين قابلة للتعديل بتشاور على الميديا الأصلية: FCPXML لفاينال كت ودافنشي، XML لبريمير ودافنشي، EDL لكل مسار، سكربت بلندر بالتلاشي والأماكن، ترجمة SRT من words.json وقائمة قطع لكاب كات، مع إيصال فيه البصمة واللي الصيغة مقدرتش تنقله.

**What it does:** Turns a kosif.timeline.v1 project or a kosif.edl.v1 cut plan into editable timelines that point at the original media: FCPXML 1.9 (Final Cut Pro, Resolve), FCP7 XML v5 (Premiere Pro, Resolve), one CMX3600 EDL per track, a Blender Video Sequencer script that also carries fades and layout, SRT captions from words.json and a numbered CapCut cut list. Times are snapped to frames with the largest drift reported, and a receipt lists SHA-256 per file and what each format could not carry.

#### متى تُستدعى

- «Open this KOSIF edit in DaVinci Resolve / Final Cut Pro / Premiere so I can keep editing»
- «Export the timeline as FCPXML, XML or EDL»
- «Build this cut in Blender's video sequencer»
- «افتح المونتاج ده في دافنشي ريزولف أو فاينال كت أو بريمير»
- «صدّر التايملاين لبلندر أو كاب كات وطلّع ملف ترجمة SRT»

#### الأوامر

- **export**: Write the timelines (fcpxml, xmeml, edl, blender, srt, capcut; default the first four), HANDOFF.md with the import steps per editor and receipt.json; refuses to overwrite unless --force.
  - `python3 scripts/nle_export.py export --project ./project.json --out ./nle --formats all --words ./words.json`
- **export (cut plan)**: Same from a cinematic_cut_planner.py kosif.edl.v1 plan, adding the voice-over as an audio track; scenes without footage stay as gaps with a warning.
  - `python3 scripts/nle_export.py export --project ./edit_plan.json --audio ./voice.wav --out ./nle`
- **formats**: List the formats and which editor opens each.
  - `python3 scripts/nle_export.py formats`
- **tests**: Run 11 tests: every format's structure and frame maths, overwrite refusal, cut-plan input, the CLI, a read-back through OpenTimelineIO and a real Blender sequencer build, each skipped when that library is missing.
  - `python3 -m unittest discover -s evals -p 'test_nle_export.py' -v`

#### المتطلبات والأمان

- optional: ffprobe (reads real source lengths and sizes), opentimelineio + otio-fcpx-xml-adapter, otio-fcp-adapter, otio-cmx3600-adapter (test read-back only), Blender 4.2+ or the bpy module (to run the generated script)
- الأمان: writes-files
- الموافقة: Use only media the user owns or may edit; the timelines only reference files, they do not copy them.
- الحدود: Integer frame rates only (no 29.97/23.976 drop-frame). Fades and position/size reach Blender only; Resolve, Final Cut and Premiere get cuts, trims, tracks and volume, and HANDOFF.md lists what to redo there. EDL holds one track per file and no overlaps. CapCut has no public timeline import, so it gets a cut list plus SRT. Not opened in the commercial editors on this machine: the files are checked by parsing, by OpenTimelineIO's independent readers and by running the Blender script in Blender 5.2 (bpy); the script also handles the Blender 4.x trim API.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_nle_export.py`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/edit.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:nle-export --evidence <ملف>`.

### `reel-factory` — مصنع الريلز: صوت وتوقيت كلمات ولقطات مرخصة ← ريلز 9:16 مفحوص / Reel factory: voice + word timings + licensed shots → verified 9:16 reel

| الحقل | القيمة |
|---|---|
| المسار | `scripts/reel_factory.py` (جذر: skill) |
| المجال | `edit` |
| الدليل | `tested-here` |
| العائلات | `transitions-cuts`, `audio-sync-captions`, `typography-arabic`, `formats-platforms`, `qa-verification` |

**ما تفعله:** غلاف رفيع فوق الأدوات الموجودة: يسجّل حقوق الصوت المعلنة ورخصة كل لقطة في rights.json (إرشادي لا يمنع — الفجوات تُسجَّل وتُذكر مرة)، ويأخذ words.json أو يشغّل transcribe، ويخطط لقطة لكل جملة مع انتقالات متمركزة على القطع (المدة = الصوت + ثانية)، ويبني لوحة لقطات 4:5 بـ ffmpeg، ويرسم مشهدًا عربيًا كلمة بكلمة (رقعة وكوفي، إطار ذهبي يُرسم، التوقيع والإشادة داخل المنطقة الآمنة، أنماط متغيرة) عبر render_html.cjs، ثم يدمج الصوت الأصلي بلا إعادة ترميز ويفحص الناتج بـ verify_video.py --source-audio. المخرجات في out/reels/<slug> المتجاهَل من git.

**What it does:** A thin wrapper over existing tools: records the audio's declared rights and every shot's licence in rights.json (advisory, never blocking — gaps are listed and said once), takes words.json or runs montage_pro transcribe, plans one shot per phrase with xfades centred on the cuts (duration = audio + 1 s), builds a 4:5 footage plate with ffmpeg, renders a word-by-word Arabic scene (Aref Ruqaa / Reem Kufi, gold frame draw-on, handle and credit inside the safe zone, parametric styles) through tools/render_html.cjs, muxes the original audio with -c copy and gates the result with verify_video.py --source-audio. Outputs go to the git-ignored out/reels/<slug>.

#### متى تُستدعى

- «اعمل ريلز دعاء من صوتي ولقطات Pexels دي بتوقيت الكلمات»
- «حوّل التسجيل ده لريلز 9:16 عليه الكلام كلمة كلمة واسمي»
- «Make a 9:16 Arabic word-synced reel from my voice and these licensed clips»
- «Make a reel and keep a record of the audio and footage rights beside it»

#### الأوامر

- **plan**: Runs the input checks, writes OUT/rights.json (declared rights and any gaps) and OUT/plan.json (phrases, cuts, transitions, style, duration, words check) without rendering.
  - `python3 scripts/reel_factory.py plan --audio ./voice.m4a --audio-rights owned --words ./words.json --shots-manifest ./stock/manifest.json --shot-ids 17928486,8165467,20382699 --title "دعاء يوم الخميس" --handle @kosif`
- **build**: Plan, plate, scene, render, -c copy mux and verify_video --source-audio; writes OUT/reel.mp4, TEST_REPORT.md and build.json (inputs sha256, commands, results). Exit 4 when the build or the verification fails.
  - `python3 scripts/reel_factory.py build --audio ./voice.m4a --audio-rights direct-permission --audio-rights-evidence https://example.com/permission --transcribe --local-only --shots ./shots.json --credit "الصوت: @x" --style rose-dusk`
- **draft**: Renders a 540x960 check copy with the same 9:16 checks.
  - `python3 scripts/reel_factory.py build --audio ./voice.m4a --audio-rights owned --words ./words.json --shots ./shots.json --draft`

#### المتطلبات والأمان

- binaries: ffmpeg, ffprobe, node
- node: playwright
- optional: pip:faster-whisper, pip:numpy
- الأمان: runs-external-programs
- الموافقة: It never fetches or publishes anything; the rights you declare for the audio and the shots are recorded in rights.json with any gaps (by the owner's decision this is advisory and never stops a build), it writes only under the chosen out folder (never jobs/, tracked paths or the skill folder unless --allow-tracked), and it never re-encodes the user's audio.
- الحدود: The rights record only checks that declarations and evidence were supplied in the right shape; it does not verify a permission or licence and does not stop a build that lacks them. Word-timing accuracy is not measured against a reference. One template family (four palettes, three transition sets, three frames; a numeric seed never repeats a preset exactly); about 0.26 s per 1080x1920 frame here, so about 2 min for a 15 s reel.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_reel_factory.py`
- مرجع: `.claude/skills/kosif-superpowers/montage-pro/README.md`
- مرجع: `.claude/skills/kosif-superpowers/proofs/pro-council-20261022/README.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:reel-factory --evidence <ملف>`.

### `reference-edit-engine` — محرك إعادة بناء المونتاج المرجعي / Reference Edit Engine

| الحقل | القيمة |
|---|---|
| المسار | `scripts/reference_edit_engine.py` (جذر: skill) |
| المجال | `edit` |
| الدليل | `tested-here` |
| العائلات | `transitions-cuts`, `audio-sync-captions`, `engines-render-pipeline`, `color-palette-grading` |

**ما تفعله:** يحوّل تقرير القطعات المستخرج من فيديو مرجعي، مع إشارات الصوت والبصمة البصرية والمقاطع المملوكة اختياريًا، إلى مشروع Remotion جديد قابل للتعديل لم يُصيَّر بعد، بلقطات مضبوطة على مستوى الإطار وقطعات لا تقسم الكلمات، مع تقرير فحص من بوابة الجودة.

**What it does:** Turns a motion_reference_probe cut report (plus optional audio cues, visual fingerprint and owned replacement clips) into a new, unrendered, editable Remotion React project with frame-exact shots, word-safe cuts and a quality-gate audit.

#### متى تُستدعى

- «عايز أعمل مونتاج بنفس إيقاع قطعات الفيديو ده بس بلقطاتي أنا»
- «أبي أعيد بناء مونتاج هالفيديو المرجعي كمشروع Remotion أقدر أعدّله»
- «حوّل توقيت القطعات وألوان الفيديو المرجعي إلى مشروع مونتاج جديد»
- «Rebuild this reference video's cut rhythm as an editable Remotion project»
- «Match the cut timing of this reel to my voiceover without splitting words»

#### الأوامر

- **build-project**: Converts the probe's cut candidates into a 1080x1920 frame-exact shot plan and writes a new Remotion project (package.json, src/index.jsx, src/Root.jsx, src/Video.jsx, src/plan.json, decision-report.json, quality-audit.json, README.md); the reference duration is the clock and captions are placeholders ('مشهد N').
  - `python3 scripts/reference_edit_engine.py --probe ./cuts.json --out ./new-edit`
- **build-project-with-audio-and-look**: Uses the kosif.audio-cues.v1 duration as master clock, scales the reference cuts to it, moves cuts off word interiors to the nearest word edge (fails if that is more than 0.5 s away), captions shots from the aligned words, adds per-shot pulse frames from onset candidates and applies measured per-shot palettes from the visual fingerprint.
  - `python3 scripts/reference_edit_engine.py --probe ./cuts.json --cues ./cues.json --visual ./reference-look.json --fps 30 --out ./new-edit`
- **build-project-with-owned-media**: Also copies one user-owned clip per shot and/or an optional audio track (from {"clips":[...],"audio":"voice.wav"}) into public/assets/ as clip_NNN.ext / audio.ext after rejecting traversal, symlinks, bad extensions, empty files and files over 350 MB (800 MB total).
  - `python3 scripts/reference_edit_engine.py --probe ./cuts.json --cues ./cues.json --manifest ./my-assets.json --assets-dir ./my-assets --out ./new-edit`

#### المتطلبات والأمان

- optional: bin:node, npm:@remotion/cli, npm:react, npm:react-dom, npm:remotion
- الأمان: writes-files
- الموافقة: Copies user-supplied replacement clips/audio into the new project: confirm the user owns or licensed them. Running npm install or a Remotion render on the generated project needs separate approval and a Remotion commercial-license review.
- الحدود: Generates source code only: it does not install Remotion, render an MP4, inspect replacement media durations or codecs, understand shot content or reproduce the reference's effects, and output is fixed at 1080x1920.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_reference_edit_engine.py`
- `.claude/skills/kosif-superpowers/evals/test_reference_visual_style.py`
- `.claude/skills/kosif-superpowers/evals/test_creative_quality_gate.py`
- `.claude/skills/kosif-superpowers/evals/test_music_rhythm_engine.py`
- مرجع: `.claude/skills/kosif-superpowers/references/reference-edit-execution.md`
- مرجع: `.claude/skills/kosif-superpowers/references/reference-visual-transfer.md`
- مرجع: `.claude/skills/kosif-superpowers/references/creative-quality-gates.md`
- مرجع: `.claude/skills/kosif-superpowers/references/music-rhythm-execution.md`
- مرجع: `.claude/skills/kosif-superpowers/references/capability-operating-manual.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/edit.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/audio.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:reference-edit-engine --evidence <ملف>`.

### `reference-visual-fingerprint` — البصمة البصرية للفيديو المرجعي / Reference Visual Fingerprint

| الحقل | القيمة |
|---|---|
| المسار | `scripts/reference_visual_fingerprint.py` (جذر: skill) |
| المجال | `edit` |
| الدليل | `tested-here` |
| العائلات | `color-palette-grading`, `photo-video-footage`, `camera-composition-layout` |

**ما تفعله:** يفكّ ترميز فيديو محلي مصرّح به بدقة 64×36 وبمعدل إطارين في الثانية عبر FFmpeg، ويقيس لكل لقطة لوحة الألوان والإضاءة والتباين والتشبّع ومقدار التغيّر ومرشّحات الإزاحة التقريبية، ثم يكتب بصمة JSON يستطيع محرك المونتاج المرجعي تحويلها إلى ألوان مشاهد جديدة.

**What it does:** Decodes an authorized local video at 64x36 and 2 fps with ffmpeg and measures per-shot palette, luma, contrast, saturation, frame change and coarse translation candidates, writing a JSON fingerprint that reference_edit_engine can apply as new shot colors.

#### متى تُستدعى

- «استخرج ألوان وإضاءة كل لقطة من الفيديو المرجعي»
- «أبي ألوان مشاهدي تشبه ألوان هالفيديو»
- «Measure the palette and brightness of each shot in this reference video»
- «Is there camera panning in this reference? Give me motion candidates»

#### الأوامر

- **fingerprint-per-shot**: Validates that the probe report came from a --cuts run of the same video (duration within 0.25 s), samples frames at 64x36 and 2 fps, computes per-sample stats and per-shot sections (palette, luma, contrast, saturation, change ratio, horizontal/vertical translation candidate), and writes a new JSON file.
  - `python3 scripts/reference_visual_fingerprint.py ./in.mp4 --probe ./cuts.json --out ./reference-look.json`
- **fingerprint-whole**: Same measurement without a cut report, so the whole video is one section.
  - `python3 scripts/reference_visual_fingerprint.py ./in.mp4 --out ./reference-look.json`

#### المتطلبات والأمان

- binaries: ffmpeg, ffprobe
- الأمان: runs-external-programs
- الموافقة: Decodes a user-supplied local video with ffmpeg: confirm the user owns or is authorized to analyze it.
- الحدود: Measures coarse low-resolution pixel statistics only (3-bit-quantized palette, uncalibrated luma, sparse translation guesses), not accurate color grading, object or camera tracking, or semantic understanding.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_reference_visual_fingerprint.py`
- `.claude/skills/kosif-superpowers/evals/test_reference_visual_style.py`
- مرجع: `.claude/skills/kosif-superpowers/references/reference-visual-transfer.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/edit.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:reference-visual-fingerprint --evidence <ملف>`.

### `script-storyboard` — من السيناريو إلى الستوري بورد والأنيماتك / Script-to-Storyboard Animatic

| الحقل | القيمة |
|---|---|
| المسار | `scripts/script_storyboard.py` (جذر: skill) |
| المجال | `edit` |
| الدليل | `tested-here` |
| العائلات | `transitions-cuts`, `camera-composition-layout`, `audio-sync-captions` |

**ما تفعله:** يقرأ مسرحية أو سيناريو بالعربي أو الإنجليزي (نص أو PDF) ويكتب قائمة لقطات بصيغة kosif.storyboard.v1: الفصول والمشاهد، ولقطة واسعة تأسيسية لكل مشهد، ولقطات حوار يتغير حجمها مع تغيّر المتكلم أو الانفعال، وإرشادات المسرح، ومدة كل لقطة من عدد الكلمات، والشخصيات وعدد جملها، والأسماء المكتوبة بطريقتين، وإيقاع كل فصل، وتقسيم العمل لحلقات قصيرة تحت حد زمني. ثم يصيّر أنيماتك MP4 دقيق الإطارات من بطاقات لونية أو صور ولقطات المستخدم، مع صوت رئيسي اختياري، بمعيار تصدير KOSIF.

**What it does:** Reads an Arabic or English play or screenplay (text or PDF) and writes a kosif.storyboard.v1 shot list: acts, scenes, an establishing wide shot per scene, dialogue shots that change size on a speaker change or emotional cue, stage directions, word-count durations, characters with line counts, likely duplicate spellings of a name, pacing per act and short-form episodes under a time limit. It then renders a frame-exact animatic MP4 from colour cards or the user's own images and clips, with an optional master audio track, at the KOSIF export standard.

#### متى تُستدعى

- «حوّل المسرحية دي لستوري بورد ولقطات»
- «عندي سيناريو PDF عايز أقسمه لحلقات ريلز دقيقة ونص»
- «اعمل أنيماتك بالتوقيت على التعليق الصوتي من الستوري بورد»
- «Turn this screenplay into a shot list with durations»
- «Split my play into 90-second episodes and render a timing animatic»

#### الأوامر

- **parse**: Extracts the text (pdftotext for PDF), cleans bidi marks and presentation forms, re-joins wrapped lines, builds acts/scenes/shots with sizes, camera moves and durations, and writes the storyboard with characters, warnings, pacing and episodes. Prints a one-line JSON summary.
  - `python3 scripts/script_storyboard.py parse ./script.pdf --first-page 8 --last-page 60 --out ./out/storyboard.json --episode-seconds 90`
- **blank**: Writes an empty storyboard template with evenly timed colour shots.
  - `python3 scripts/script_storyboard.py blank --out ./out/storyboard.json --title Demo --duration 15 --shots 3`
- **render**: Renders each shot (its source image/clip cropped to fill, or a colour card) on exact frame boundaries, concatenates them, scales the timeline to the master audio when given (stream-copying AAC/MP3/ALAC, else AAC 320k), and writes <out>.report.json with frames per shot.
  - `python3 scripts/script_storyboard.py render --storyboard ./out/storyboard.json --episode 1 --audio ./voice.m4a --out ./out/episode1.mp4`

#### المتطلبات والأمان

- binaries: ffmpeg, ffprobe
- optional: pdftotext
- الأمان: writes-files
- الموافقة: Nothing to approve; it reads only the script the user supplied and writes the files named by --out.
- الحدود: Shot sizes and durations are rule-based suggestions from the text layout, not a director's reading; it writes no text on frames, generates no footage, and a script whose dialogue is not in 'NAME: line' form comes out as stage directions.

#### الاختبارات والأدلة

- `tests/test_script_storyboard.py`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/edit.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:script-storyboard --evidence <ملف>`.

### `video-workflow-bridge` — جسر سير عمل الفيديو / Video Workflow Bridge

| الحقل | القيمة |
|---|---|
| المسار | `scripts/video_workflow_bridge.py` (جذر: skill) |
| المجال | `edit` |
| الدليل | `tested-here` |
| العائلات | `transitions-cuts`, `audio-sync-captions`, `qa-verification` |

**ما تفعله:** ينتج ملفات JSON حتمية وغير إتلافية لمسارين من مسارات المونتاج: خطة مونتاج نصية تحوّل نطاقات الكلمات المختارة إلى مقاطع فيديو محددة بالإطارات، وعلامات مراجعة دقيقة على مستوى الإطار مع رموز زمنية (timecode) وإحداثيات بكسل اختيارية، دون أن يقرأ الوسائط أو يقصّها أو يصيّرها.

**What it does:** Generates deterministic, non-destructive JSON for two editor workflows: a text-based paper edit that turns selected word ranges into frame-bounded video-only segments, and frame-accurate review markers with timecodes and optional pixel anchors; it never reads, cuts or renders media.

#### متى تُستدعى

- «عايز أقص الفيديو بالكلام: خلّي الكلمات من 1 لـ 3 ومن 7 لـ 9»
- «حوّل ملاحظات المراجعة لعلامات على إطارات محددة بالتايم كود»
- «Make a text-based paper edit from words.json»
- «Convert review comments with x/y positions to frame-accurate markers»

#### الأوامر

- **paper-edit**: Reads words (list or {words:[...]}, each with word/start/end), keeps the 1-based word ranges, merges consecutive words into source frame runs (floor start, ceil end), lays them end-to-end on an output timeline and writes kosif.video-paper-edit.v1. Audio is never processed.
  - `python3 scripts/video_workflow_bridge.py paper-edit templates/ik-wave-words.json --keep "1-3,5" --fps 30 --out ./out/paper-edit.json`
- **review**: Converts [{time,comment,x?,y?}] notes into sorted markers (kosif.frame-review.v1), each with a stable 12-hex id, an exact frame, HH:MM:SS:FF timecode and an optional pixel point from normalized x/y.
  - `python3 scripts/video_workflow_bridge.py review ./notes.json --duration 60 --fps 30 --width 1080 --height 1920 --out ./out/review-markers.json`

#### المتطلبات والأمان

- الأمان: writes-files
- الموافقة: —
- الحدود: Produces cut and review plans only: it never cuts, renders or plays media, and its paper-edit segments must not be applied to an audio master.

#### الاختبارات والأدلة

- `.claude/skills/kosif-superpowers/evals/test_video_workflow_bridge.py`
- مرجع: `.claude/skills/kosif-superpowers/references/global-video-platforms-2026-10-19.md`
- مرجع: `.claude/skills/kosif-superpowers/references/app-feature-transfer.md`
- مرجع: `.claude/skills/kosif-superpowers/references/guides/edit.md`

#### عند الفشل (A29)

- ابدأ بـ `think.py recover --message "<نص الخطأ>"`، ثم سجّل `fusionforge.py trace --project <slug> --id <FUSE-ID> --stage <stage> --node <N> --action "<ما جُرّب>" --result failed --error-class <الصنف> --tool tool:video-workflow-bridge --evidence <ملف>`.

