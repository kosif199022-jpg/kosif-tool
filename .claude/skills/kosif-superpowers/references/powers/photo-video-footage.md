# الصور والفيديو الخام — Photos & footage

> **قوتك هنا:** تأخذ صور المستخدم ولقطاته الخام كما هي وتصنع منها فيلمًا: تكشف القطعات، تختار أنشط النوافذ، تثبّت وتنظّف وتمسح الترجمة القديمة وتموّه المارة، ثم تحرّك الصور بكين بيرنز وبارالاكس وتضع اللقطات داخل تكوين HTML بدقة الإطار.
> **أقوى دليل:** اختبارات `kosif-montage-motion` شغّلتُها هنا (كشف اللقطات، مترجم التايملاين ومنحدرات السرعة، دراسة المرجع mimic، الملاءمة 9:16) واختبار مسح الترجمة في `kosif-studio`، وتثبيت vidstab ولوح all-intra على مقطع اختبار، و11 وصفة ffmpeg (كروما، تشويش، zoompan، perspective، pixelize، scdet…) نجحت كلها في هذه الحاوية.
> **You can:** source with credits, triage, cut, restore, matte, animate stills and auto-edit. **58 powers follow** — ✅ 15 · 🟢 17 · 📦 7 · 🔑 3 · 👁 2 · 📄 14 · 💡 0.

**الحالة / status:** ✅ مُثبت هنا (كود + اختبار أو رندر في هذه الحاوية) · 🟢 جاهز (كود المالك يعمل بلا إضافات) · 📦 بأمر تثبيت · 🔑 مفتاح أو خدمة · 👁 شوهد في فيديو أنتجتَه (وصفة البناء مرفقة) · 📄 موصوف فقط · 💡 فكرة.
مسارات الدليل نسبية إلى `/home/user/`؛ `style:<id>` = فيديو مرجعي أنتجتَه سابقًا (ملاحظاته في `kosif-tool/styles/<id>/`).

**فحص سريع لهذه الحاوية (2026-10-16):** ffmpeg 6.1.1 مع vidstab وrubberband ✔ · OpenCV 5.0 قابل للاستيراد (بلا ملفات Haar) · ImageMagick 6 باسم `convert` ✔ · yt-dlp وscipy وrembg غير مثبتة · pexels/pixabay محجوبان (403)، وWikimedia وarchive.org متاحان.

## الفهرس / contents
- **جلب الوسائط وحقوقها — Sourcing, ingest & rights** — FOOT-01 … FOOT-07 (7)
- **الفرز والتحليل — Triage & analysis** — FOOT-08 … FOOT-15 (8)
- **القص والدمج والسرعة — Cutting, joining & speed** — FOOT-16 … FOOT-23 (8)
- **الترميم والتنظيف — Restoration & cleanup** — FOOT-24 … FOOT-30 (7)
- **التركيب والعزل والتتبع — Compositing, matting & tracking** — FOOT-31 … FOOT-38 (8)
- **الصور إلى حركة — Photos into motion** — FOOT-39 … FOOT-46 (8)
- **اللقطات داخل التكوين والعرض — Footage inside compositions** — FOOT-47 … FOOT-53 (7)
- **المونتاج التلقائي — Auto-edit workflows** — FOOT-54 … FOOT-58 (5)
- توليفات قوية / power combos · أخطاء ممنوعة / never do · أقوى 5 حركات توقيع / 5 signature moves

## جلب الوسائط وحقوقها — Sourcing, ingest & rights

_قبل القص: من أين جاءت اللقطة، وهل يحق لك استخدامها، وهل وصلت بنسخة صالحة للتحرير._

#### FOOT-01 · انضباط ترخيص الصور واللقطات · Media licensing discipline · 📄 موصوف / documented only
- **ماذا / what:** مسموح: ما أكّده المستخدم، الملكية العامة/CC0، CC BY مع الإسناد، والمخزون بإيصال؛ ممنوع: لقطات المراجع والمكشوط وND وNC التجاري. — Allowed: user-confirmed, PD/CC0, CC BY with attribution, receipted stock; banned: reference frames, scraped media, ND, NC in commercial work.
- **متى أستخدمها / when:** قبل وضع أي صورة أو لقطة في الفيلم — before any photo or clip enters the film.
- **كيف / how:** One ASSETS.md row per file (source, licence, author, URL). Editorial-only images never go in ads; people need model releases; AI images only when asked and declared. Faceless channels: any clip showing the speaker's face even for one frame is audio-only; sample 1 frame/s through face detection. **أرقام / params:** one ASSETS.md row per file
- **الدليل / proof:** `kosif-tool/playbooks/photos.md:11` · `kosif-atlas/skills/1096-akbun-editvideo/2451-davinciresolve-beats-devtalk/SKILL.md`

#### FOOT-02 · تنزيل لقطة مفتوحة مع إيصال مصدر · Open-footage downloader with provenance · 🟢 جاهز / ready
- **ماذا / what:** ينزّل رابط HTTPS واحدًا من مضيف مسموح، يرفض صفحات التحدي، يحدّ الحجم، ويكتب إيصالًا بالبصمة والرخصة. — Downloads one explicit HTTPS URL from an allow-listed open host, refuses challenge pages, caps size and writes a hashed provenance receipt.
- **متى أستخدمها / when:** لقطات Wikimedia أو مخزون مفتوح — Wikimedia or open stock clips.
- **كيف / how:** python motion.py openclip URL --out clip.mp4 [--license-note '…'] (open_footage.py). Here: commons.wikimedia.org and archive.org are reachable; pexels.com, pixabay.com and NASA images answer 403 from this container — ask the user for files instead. **أرقام / params:** hosts *.wikimedia.org, *.pexels.com; https only; 64 KiB–500 MiB; timeout 120 s; SHA-256 sidecar .source.json (kosif-open-footage-v1)
- **الدليل / proof:** `kosif-studio/motion/open_footage.py` · `kosif-studio/motion/test_open_footage.py` · `kosif-studio/motion/references/voice-open-footage-upgrade-2026-10-10.md`

#### FOOT-03 · جلب من المنصات مع الاعتمادات · Social/Pinterest fetch with credits (yt-dlp) · 📦 بأمر تثبيت / one install
- **ماذا / what:** روابط بنترست وتيك توك وإنستغرام ويوتيوب وX إلى مكتبة وسائط بنسخة تحرير وملف اعتمادات. — Pinterest, TikTok, Instagram, YouTube and X links into a media library with an edit-safe copy and a credits file.
- **متى أستخدمها / when:** عندما يعطيك المستخدم روابط مرجعية أو لقطاته — when the user hands you links to their own or licensed media.
- **كيف / how:** python scripts/kmotion.py fetch URL… --max 30 --only video|image [--list] [--cookies]; edit copy H.264 yuv420p CFR ≤ 60 fps + AAC 48 kHz; fetch-credits.json; duplicates skipped. The test skips here because yt-dlp is not installed. Safe single-URL variant: https only, global IPs only, ≤ 150 MB, ≤ 900 s, ≤ 720p, sha256 receipt. TikTok needs an impersonation backend (curl_cffi) — otherwise ask for the file. Downloaded media keeps its source licence: reference ≠ permission. **أرقام / params:** --max 30; edit copy ≤ 60 fps
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/fetch.py` · `100-superskills/skills/kosif-montage-motion/tests/test_fetch_lab.py:66` · `kosif-one/projects/KOSIF_Motion_Ghorba/tools/kosif_c_video_fetch.py:24-49`
- **📦 تثبيت / install:** `pip install yt-dlp`

#### FOOT-04 · مجمع لقطات بأسئلة بحث ثنائية اللغة · Per-shot bilingual footage pool · 📄 موصوف / documented only
- **ماذا / what:** كل لقطة في المرجع تُوصف بـ 1–3 عبارات بحث إنجليزية وعربية لتجمع لقطات جديدة بنفس المعنى. — Each reference shot is described by 1–3 English + Arabic searches so new footage with the same meaning lands in one pool.
- **متى أستخدمها / when:** «اعمل مثل هذا الريل بلقطات أخرى» — 'make this reel with other footage'.
- **كيف / how:** shots[].query e.g. ['incense burner smoke aesthetic', 'bakhoor mabkhara']; 2–3 candidates per shot, clip ≥ shot length (or ≥ 0.67× when slowed), ≥ 720p, no watermark or burned text; credit every pin. When the host is unreachable publish an intermediary page with key frames and search buttons for the user to fetch. **أرقام / params:** 2–3 candidates/shot; ≥ 720p
- **الدليل / proof:** `kosif-one/projects/mimic-jumuah/study/mimic.json` · `100-superskills/skills/kosif-montage-motion/references/mimic.md` · `kosif-one/tools/kosif-mimic/SKILL.md`

#### FOOT-05 · مكتبة وسائط محلية مع فحص · Local media library with probe · 🟢 جاهز / ready
- **ماذا / what:** رفع بالسحب والإفلات، كل ملف يُفحص (مدة، فيديو، صوت) ويُصنف. — Drag-and-drop upload, every file probed (duration, video, audio) and classified.
- **متى أستخدمها / when:** استوديو الويب المحلي — the local web studio.
- **كيف / how:** POST /api/media (multipart, 1 MB chunks), GET/DELETE /api/media/NAME; index in workbench/media/.index.json. Accepts mp4 mov mkv webm avi m4v mp3 wav m4a aac flac ogg png jpg webp gif json txt srt; ≤ 4 GB per file. **أرقام / params:** ≤ 4 GB/file; names ≤ 150 chars
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:58` · `100-superskills/skills/kosif-montage-motion/tests/test_web.py:145`

#### FOOT-06 · تايملاين زمني متعدد الكاميرات · Chronological multi-camera timeline · 📄 موصوف / documented only
- **ماذا / what:** رتّب كل اللقطات على زمن التصوير مع تصحيح فرق ساعة كل كاميرا. — Sort every clip on recorded time, correcting each camera's clock offset.
- **متى أستخدمها / when:** رحلات وفعاليات صُورت بعدة أجهزة — trips and events shot on several devices.
- **كيف / how:** Read creation_time via ffprobe (or exiftool); measure one offset per camera from a pair of clips of the same moment (--offset prefix=seconds); timeline fps = the most common clip fps; dry-run table: file, time, camera, resolution, fps, gamma.
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2443-akbun-davinciresolve-timeline-chrono/SKILL.md`

#### FOOT-07 · إعدادات تسجيل الشاشة · Screen-capture defaults · 📄 موصوف / documented only
- **ماذا / what:** جدول تسجيل في آخر الستوري بورد وإعدادات موحدة لكل اللقطات. — A recording table at the end of the storyboard and one set of capture settings.
- **متى أستخدمها / when:** شروح البرمجيات والتطبيقات — software tutorials.
- **كيف / how:** Native resolution (e.g. 3840×2160), 30 fps matching the timeline, per-window capture, enlarged cursor, mic and system audio on separate tracks, H.264/H.265 CQP 18–20, editor font ≥ 16 pt (terminal 18), notifications off, history cleared. **أرقام / params:** 3840×2160; 30 fps; CQP 18–20
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2449-akbun-vlog-storyboard/SKILL.md`

## الفرز والتحليل — Triage & analysis

_قِس قبل أن تقص: أين القطعات، أي جزء هو الأنشط، أي لقطة مكررة، وهل الصورة محروقة._

#### FOOT-08 · كشف اللقطات إلى تايملاين · Scene/shot detection → timeline · ✅ مُثبت هنا / proven here
- **ماذا / what:** يكشف القطعات بـ scdet، يرسم لوحة لقطات، يقسّم، ويكتب مواصفة تايملاين بانتقالات. — Detects cuts with scdet, draws a contact sheet, splits, and writes a timeline spec with transitions.
- **متى أستخدمها / when:** أول خطوة مع أي فيديو خام أو مرجع — first step with any raw video or reference.
- **كيف / how:** python scripts/kmotion.py scenes CLIP.mp4 --sheet shots.png --timeline edit.json [--split DIR --transition fade]; API scenes.detect(clip, threshold=10, min_len=.5). Ran here: tests.test_v6 ScenesTests ok (3 shots found at 2.0 s and 4.0 s ±0.15). Robust variant in decaption.analyse: 90×160 grey diff, threshold max(12, 6×median), > 4× local median over ±15 frames, cuts ≥ 5 frames apart (codecs that smear a cut over two frames). **أرقام / params:** threshold 10 (0–100); min 0.5 s
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/scenes.py` · `100-superskills/skills/kosif-montage-motion/tests/test_v6.py:113` · `kosif-studio/motion/decaption.py:63`

#### FOOT-09 · لوحة لقطات واختيار الغلاف · Contact sheet & cover-frame mining · ✅ مُثبت هنا / proven here
- **ماذا / what:** عيّنات عبر المدة كلها في لوحة واحدة، ثم اختيار إطار غلاف يشرح الفيديو بنظرة. — Samples across the whole duration on one sheet, then a cover frame that explains the video at a glance.
- **متى أستخدمها / when:** مراجعة سريعة، أغلفة يوتيوب وريلز — quick review, YouTube/Reels covers.
- **كيف / how:** ffmpeg -i in.mp4 -vf "fps=2,scale=320:-1,tile=3x2" -frames:v 1 sheet.png, or select='gt(scene,0.3)' for change-driven sheets. Skip transition, blurred, first and last frames; shortlist distinct candidates with timestamps; for composed films render the chosen moment straight from the composition at each target size; animated covers loop with a ~0.4 s crossfade; check at phone size. تحققتُ منه في هذه الحاوية (ffmpeg 6.1.1، 2026-10-16) / verified in this container (ffmpeg 6.1.1, 2026-10-16). **أرقام / params:** scene ~0.3; loop crossfade ~0.4 s
- **الدليل / proof:** `kosif-atlas/skills/101-video-skills/222-video-thumbnails/SKILL.md` · `kosif-one/projects/ghorba-motion-v2/make_contact.py`

#### FOOT-10 · اختيار أنشط نافذة في اللقطة · Motion-energy window picking · 🟢 جاهز / ready
- **ماذا / what:** لكل خانة إيقاع تُختار أنشط نافذة غير مستخدمة من اللقطة التالية حسب طاقة فرق الإطارات. — For each beat slot the most active unused window of the next clip is chosen by frame-difference energy.
- **متى أستخدمها / when:** مونتاج على الموسيقى من لقطات خام — beat montage from raw clips.
- **كيف / how:** montage.energy(clip, fps=6) + montage.pick(…); rank segments by measured motion, never guess. Basma's probe samples every clamp(D/30, 0.5, 2) s for motion, sharpness and brightness and treats motion > 45 as an internal cut. **أرقام / params:** energy at 6 fps
- **الدليل / proof:** `kosif-one/tools/kosif-studio/motion/montage.py:105` · `kosif-studio/motion/montage.py:42` · `app/public/js/10_studio.js:1865`

#### FOOT-11 · قص البدايات المعيبة وتجميع المكرر · Bad-head trimming & duplicate-take grouping · 📄 موصوف / documented only
- **ماذا / what:** مقاطع الهاتف تبدأ بثانية بيضاء أو غير مركزة؛ واللقطات المتقاربة المتشابهة مكررة. — Phone clips start with ~1 s of white or soft frames; near-identical takes are duplicates.
- **متى أستخدمها / when:** تنظيف مجلد رحلة أو فعالية قبل المونتاج — cleaning a trip/event folder.
- **كيف / how:** Compare the first 2 s with a 2–5 s reference window: trim until mean luma is within ±20% and focus (Laplacian variance, cv2 is installed here) recovers; skip clips < 5 s; gimbal cameras need no trim. Duplicates: shot within 2 min and middle-frame luma histograms correlate ≥ 0.9 → keep the sharpest after the user confirms. Large pools: perceptual hash (dHash) with PIL + numpy. **أرقام / params:** ±20% luma; Δt ≤ 2 min; corr ≥ 0.9
- **الدليل / proof:** `kosif-atlas/skills/1096-akbun-editvideo/2454-davinciresolve-cut-travelflow/SKILL.md` · `kosif-atlas/skills/3385-fiftyone/13900-fiftyone-find-duplicates/SKILL.md`

#### FOOT-12 · تحليل تعريض الصورة ونصائح بالعربية · Image exposure analysis + Arabic fix advice · 🟢 جاهز / ready
- **ماذا / what:** يقيس نسب الإضاءة والمدى والقص والظلال المسحوقة ويحكم على التعريض، ثم يقترح الإصلاح بالعربية. — Measures luma percentiles, range, clipping and crushed shadows, gives an exposure verdict and Arabic fix advice.
- **متى أستخدمها / when:** قبل تحريك صور المستخدم — before animating the user's photos.
- **كيف / how:** python3 scripts/omni/image_analyze.py IMAGE [--summary]; EXIF-transposed, ≤ 1600 px, Rec.709 luma. Advice triggers: clipped > 2%, crushed > 10%, range < 120, soft, noisy, colour cast, subject off the thirds grid. **أرقام / params:** clip ≥ 250; crushed ≤ 5; over if mean > 185 or clipped > 5%; under if mean < 60 or crushed > 15%
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/omni/image_analyze.py:120` · `100-superskills/skills/kosif-montage-motion/scripts/omni/image_analyze.py:207`

#### FOOT-13 · دراسة ريل مرجعي بدقة الإطار · Reference-reel study (mimic) · ✅ مُثبت هنا / proven here
- **ماذا / what:** يقيس كل حد قطع أو ذوبان أو تعتيم أو انزلاق بالإطار، وأطوال اللقطات، والمظهر، ومنطقة النص، والصوت. — Measures every cut/dissolve/dip/slide boundary to the frame, shot lengths, look, text zone, fades, flashes and audio.
- **متى أستخدمها / when:** «اعمل مثل هذا» مع فيديو مرجعي — 'make it like this' with a reference video.
- **كيف / how:** python scripts/kmotion.py mimic study REF.mp4 --out PROJECT/study → shots.jpg, strip.jpg (frame/0.5 s), text/shot_XX.png, mimic.json. Then mimic layer DIR --erase x0,y0,x1,y1 lifts the fixed design layer as overlay.png (creator handles erased, badges snapped by HSV). Ran here: tests.test_mimic all ok (frame-exact cuts, dissolve place/length, dip, exposure fades inside a shot not counted as cuts). Measure the reference — never copy its media. **أرقام / params:** boundaries cut/dissolve/fadeblack/fadewhite/slide*
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/mimic.py` · `100-superskills/skills/kosif-montage-motion/tests/test_mimic.py` · `100-superskills/skills/kosif-montage-motion/references/mimic.md`

#### FOOT-14 · تحليل فيديو مرجعي إلى نبضات · Video breakdown to beats · 🟢 جاهز / ready
- **ماذا / what:** نبضات ≤ 3 ث مع لوحة ألوان لكل نبضة وطاقة الحركة والتحريك والانتقال المتوقع والجهارة والإيقاع. — Beats ≤ 3 s with a per-beat hex palette, motion energy, pan, likely transition, loudness, tempo and onsets.
- **متى أستخدمها / when:** فهم إيقاع ولون مرجع — understanding a reference's rhythm and colour.
- **كيف / how:** kmotion analyze VIDEO --max-beat 3.0 [--transcribe] [--batch DIR]. For a scene-by-scene recreation schema sample ~12 evenly spaced frames ≤ 1024 px and describe shot type, camera motion, lighting and mood per scene, with scene N's end frame = scene N+1's start. **أرقام / params:** beats ≤ 3 s; 12 samples ≤ 1024 px
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/analyze.py` · `kosif-one/tools/kosif-omni/skills/kosif-prompt-master/references/books-drive-ledger.md`

#### FOOT-15 · تشخيص قبل رفع الدقة · Upscale triage · 📄 موصوف / documented only
- **ماذا / what:** رفع الدقة يعيد الحجم والحدة لا المعلومة المفقودة. — Upscaling restores size and sharpness, not missing information.
- **متى أستخدمها / when:** صورة أو لقطة صغيرة يريد المستخدم تكبيرها — small sources the user wants bigger.
- **كيف / how:** Jagged edges from low resolution → upscale; uniform focus blur → no; JPEG blocks or ISO noise → partial; pixelated logo → fetch the SVG. Save as name_upN.png, never overwrite the source. Modest scaling with ffmpeg scale flags=lanczos; AI upscalers (Real-ESRGAN, Topaz) need install or keys and run once on the final concat, not per segment. Source rule: long side ≥ 1.5× displayed size at max scale (1080×1920 at 1.12 → ~2400 px). **أرقام / params:** long side ≥ 1.5× display
- **الدليل / proof:** `kosif-atlas/skills/2976-pwdev-social-media/12579-asset-upscale/SKILL.md` · `kosif-tool/playbooks/photos.md:26`

## القص والدمج والسرعة — Cutting, joining & speed

_قص دقيق بالإطار، دمج لا يكسر الصوت، وتايملاين JSON يُرندر بأمر واحد._

#### FOOT-16 · مترجم تايملاين JSON · JSON timeline compiler (cuts, ramps, overlays) · ✅ مُثبت هنا / proven here
- **ماذا / what:** مواصفة JSON للمقاطع والصور وبطاقات اللون مع قص وزوم وتلوين ومنحدرات سرعة وانتقالات وطبقات نص وترجمة تُرندر في أمر FFmpeg واحد مع بوابة جودة. — A JSON spec of clips, stills and colour cards with in/out, zoom, grade, speed ramps, transitions and text/caption overlays compiles into one FFmpeg render with a QA gate.
- **متى أستخدمها / when:** أي مونتاج من لقطات المستخدم — any edit from the user's footage.
- **كيف / how:** kmotion timeline --example edit.json, then timeline.build(spec, out, workers, inspect) → report {seconds, transitions, audio, gate{lufs}}. Ramps [[t, speed]…] → setpts with log(); atempo chain (0.25 → atempo=0.5,atempo=0.5); ratio '1:1' → 1080×1080; overlays: text anim 'rise' with box #00000080, lower-third, logo upper-right ×.5, progress #E7B65A 4 px, captions style 'tiktok'; music ducked under clip audio at −14 LUFS. Ran here: test_v6 TimelineTests (build_film, validation, text_png) and RampTests ok. **أرقام / params:** example: 9:16, 30 fps, bg #0d1b2a; clip zoom 1.0→1.08 grade teal_orange, circleopen 0.6 s; ramp [[0,1],[2,.3],[4,1]]
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_v6.py:34` · `100-superskills/skills/kosif-montage-motion/tests/test_v6.py:64` · `100-superskills/skills/kosif-montage-motion/scripts/timeline.py:896`

#### FOOT-17 · قص دقيق بالإطار · Frame-accurate trim (re-encode) · 🟢 جاهز / ready
- **ماذا / what:** اقطع من أي إطار بإعادة الترميز؛ القص بلا ترميز يعمل فقط على الإطارات المفتاحية. — Cut at any frame by re-encoding; stream-copy cuts only work on keyframes.
- **متى أستخدمها / when:** كل قص لملف مستقل — every standalone cut.
- **كيف / how:** python tools.py trim CLIP --from 3.2 --to 9.8 --out part.mp4 (crf 18 yuv420p, AAC 192k 48 kHz). Raw: ffmpeg -ss T -i in -to D -c:v libx264 -crf 18 -preset slow -c:a aac -b:a 192k -pix_fmt yuv420p -movflags +faststart. -c copy only when the in-point is an I-frame, otherwise 2–5 s of frozen picture; inside compositions prefer non-destructive trim props (data-media-start, trimBefore). **أرقام / params:** crf 18; AAC 192k
- **الدليل / proof:** `kosif-studio/motion/tools.py:247` · `100-superskills/skills/pro-video-editor-ffmpeg/references/ffmpeg-recipes.md` · `kosif-atlas/skills/2712-remotion/10436-remotion-markup/ffmpeg.md`

#### FOOT-18 · دمج مقاطع مختلفة دون كسر الصوت · Fit-and-join concat · 🟢 جاهز / ready
- **ماذا / what:** يدمج المقاطع بالترتيب ويلائم كل واحد في مقاس واحد ويملأ المقاطع الصامتة بصمت. — Joins clips in order, fitting each to one size and filling silent clips with silence so audio never breaks.
- **متى أستخدمها / when:** تجميع لقطات من هواتف ومصادر مختلفة — stitching clips from different phones/sources.
- **كيف / how:** python tools.py concat A.mp4 B.mp4 --out all.mp4 [--size 1080x1920 --fps 30] (pad black, anullsrc 48 kHz stereo). Same-codec clips: concat demuxer (-f concat -safe 0 -i list.txt -c copy). Mixed: per input fps=30,scale=W:H:force_original_aspect_ratio=increase,crop=W:H,setsar=1 then concat=n=N:v=1:a=1. **أرقام / params:** 48 kHz stereo silence fill
- **الدليل / proof:** `kosif-studio/motion/tools.py:256` · `100-superskills/skills/pro-video-editor-ffmpeg/references/ffmpeg-recipes.md`

#### FOOT-19 · منحدرات السرعة والتصوير البطيء · Speed ramps & slow motion · ✅ مُثبت هنا / proven here
- **ماذا / what:** سرعة متغيرة على اللقطة مع الحفاظ على طبقة الصوت، أو سرعة ثابتة بطيئة. — Variable speed along a clip with pitch-preserved audio, or a constant slow rate.
- **متى أستخدمها / when:** لحظة ذروة رياضية أو منتج — sports or product peak moments.
- **كيف / how:** Timeline ramp [[t, speed]…] (RampTests ok here) maps time with setpts and chains atempo (each factor 0.5–2). Quick check here: setpts='if(lt(T,1),PTS,PTS*2)' runs. HyperFrames: data-playback-rate 0.1–10 (consumed source = timeline × rate) or a 'rate' lane in data-automation; later starts shift by old/rate. Slow-mo below 0.5× from 30 fps footage stutters — ask for 60/120 fps sources. **أرقام / params:** atempo 0.5–2 per stage; rate 0.1–10
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_v6.py:64` · `kosif-one/vendor/hyperframes/skills/hyperframes-core/references/creator-editing-recipes.md` · `kosif-one/vendor/hyperframes/docs/reference/speed-ramps.mdx`

#### FOOT-20 · قص الصمت · Silence jump-cut · 🟢 جاهز / ready
- **ماذا / what:** يحذف الوقفات صورةً وصوتًا في مرور واحد. — Removes pauses from picture and sound in one pass.
- **متى أستخدمها / when:** مقاطع كلام وبودكاست — talking clips and podcasts.
- **كيف / how:** python scripts/kmotion.py silence CLIP.mp4 --out cut.mp4 --threshold -35 --min 0.45 --pad 0.08. Transcript-driven alternative (HyperFrames transcript-cut.mjs): remove ranges, filler words and silences ≥ 0.8 s from word timestamps. Keep 80 ms pads so words never clip. **أرقام / params:** −35 dB; min 0.45 s; pad 0.08 s
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md` · `kosif-one/vendor/hyperframes/skills/media-use/scripts/transcript-cut.mjs`

#### FOOT-21 · تجميد إطار وتكرار حلقة · Freeze frame & loop · 🟢 جاهز / ready
- **ماذا / what:** امسك لحظة بصورة ثابتة لمدة محددة، أو كرر مقطعًا بذيل يذوب في رأسه. — Hold a moment as a still for N seconds, or loop a clip with its tail dissolving into its head.
- **متى أستخدمها / when:** لحظة تأكيد أو خلفية متكررة — emphasis holds or looping backgrounds.
- **كيف / how:** Freeze: extract the frame (ffmpeg -ss T -frames:v 1) and place it as an <img> clip (data-start, data-duration), deciding audio continue/trim/silence explicitly. Loop: kmotion loop --seconds 30. Dress the freeze with paper/tape/flash (HyperFrames freeze-frame-dressing, 4 s).
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/SKILL.md` · `kosif-one/vendor/hyperframes/skills/hyperframes-core/references/creator-editing-recipes.md`

#### FOOT-22 · محرر KOSIF Studio في المتصفح · KOSIF Studio browser montage editor · 🟢 جاهز / ready
- **ماذا / what:** محرر محلي بلا رفع: استيراد، مشاهد على تايملاين، طبقات نص وأشكال، صوت، تراجع، حفظ، ومعاينة حية. — A local upload-free editor: import, scenes on a timeline, text/shape layers, soundtrack, undo, save/open, live preview.
- **متى أستخدمها / when:** عندما يريد المستخدم التعديل بنفسه — when the user wants to edit by hand.
- **كيف / how:** Serve the site and open /studio/. Limits: 60 s project, 24 clips, 24 overlays, 48 assets, 200 MB per file, canvas 1280×720 / 720×1280 / 720×720. Projects import into the FFmpeg timeline: POST /api/studio/import → studio_import.convert() (StudioImportTests ok here). **أرقام / params:** 60 s; 24 clips; 200 MB/file
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/app.mjs:1` · `100-superskills/skills/kosif-montage-motion/scripts/web/static/studio/model.mjs:13` · `100-superskills/skills/kosif-montage-motion/scripts/web/server.py:528`

#### FOOT-23 · مونتاج مستقل أو متتابع في Remotion · Remotion clip editing: independent vs ripple · 📦 بأمر تثبيت / one install
- **ماذا / what:** نموذجان: مقاطع بمواضع مطلقة (فراغات وتداخل مسموح) أو تسلسل متتابع يزيح ما بعده. — Two models: absolutely placed clips (gaps/overlaps allowed) or ripple sequences where one change shifts all later clips.
- **متى أستخدمها / when:** أفلام Remotion فيها لقطات حقيقية — Remotion films with real footage.
- **كيف / how:** Independent: each <Video> with from/trimBefore/durationInFrames. Ripple: <TransitionSeries> of <TransitionSeries.Sequence durationInFrames> wrapping <Video trimBefore>. Remotion bundles ffmpeg via npx remotion ffmpeg/ffprobe.
- **الدليل / proof:** `kosif-atlas/skills/2712-remotion/10436-remotion-markup/video-editing.md`
- **📦 تثبيت / install:** `cd kosif-tool/starters/remotion && npm install`
- **⚖️ ترخيص / license:** Remotion برخصة الشركة؛ @remotion/transitions غير مرخصة MIT / Remotion company license; @remotion/transitions is UNLICENSED on npm.

## الترميم والتنظيف — Restoration & cleanup

_ثبّت، أزل التشويش، امسح الترجمة المحروقة، وموّه الوجوه — قبل أي تلوين._

#### FOOT-24 · تثبيت الاهتزاز · Stabilisation (vidstab 2-pass) · ✅ مُثبت هنا / proven here
- **ماذا / what:** تثبيت بمرورين عبر vidstab أو deshake عند غيابه — فقط عندما يكون الاهتزاز مقاسًا. — Two-pass vidstab stabilisation (deshake fallback) — only when shake is measured.
- **متى أستخدمها / when:** لقطات اليد المهتزة — shaky handheld footage.
- **كيف / how:** python tools.py stabilize CLIP --out steady.mp4 [--strength 10]: vidstabdetect shakiness=min(10,s) accuracy=15 → vidstabtransform smoothing=2 s optzoom=1 + unsharp 5:5:0.5; fallback deshake rx=ry=32. Ran here on a test clip: method 'vidstab (2-pass)', duration preserved. Prefer similarity mode and keep crop ≤ 10%; if edges bend, lower strength. **أرقام / params:** strength 10; crop ≤ 10%
- **الدليل / proof:** `kosif-studio/motion/tools.py:303` · `kosif-atlas/skills/1096-akbun-editvideo/2454-davinciresolve-cut-travelflow/SKILL.md`

#### FOOT-25 · إزالة التشويش والتوضيح وسلسلة الترميم · Denoise, sharpen & restoration chain · ✅ مُثبت هنا / proven here
- **ماذا / what:** نظّف ضوضاء الإضاءة المنخفضة واستعد حدة الحواف، ثم سوداء أنظف وانحناء إضاءات ودرجات وسطى أدفأ. — Clean low-light noise and restore edges, then cleaner blacks, highlight roll-off and warmer mids.
- **متى أستخدمها / when:** لقطات هاتف ليلية أو مضغوطة قبل التلوين — night or compressed phone clips before grading.
- **كيف / how:** Fast: hqdn3d=4:3:6:4.5,unsharp=5:5:0.6; better/slower: nlmeans=s=3..5; archival chroma: chromanr. Reel chain: hqdn3d=1.2:1.2:3:3, Lanczos reframe, eq=contrast=1.12:brightness=-0.015:saturation=1.07:gamma=0.97, curves, colorbalance, cas=0.3. تحققتُ منه في هذه الحاوية (ffmpeg 6.1.1، 2026-10-16) / verified in this container (ffmpeg 6.1.1, 2026-10-16). **أرقام / params:** hqdn3d 4:3:6:4.5; nlmeans s 3–5; cas 0.3
- **الدليل / proof:** `kosif-atlas/skills/235-mas-video-lab/754-ffmpeg/SKILL.md` · `kosif-one/tools/kosif-studio/motion/reel.py:35`

#### FOOT-26 · مسح الترجمة المحروقة · Burned-caption eraser (decaption) · ✅ مُثبت هنا / proven here
- **ماذا / what:** يجد حبر الترجمة الأبيض أو الأصفر بحد أسود، ويعيد بناء اللقطات الثابتة من وسيط البكسل ويرمم المتحركة. — Finds white/yellow caption ink next to a black outline; rebuilds locked-off shots from the per-pixel median and inpaints moving shots.
- **متى أستخدمها / when:** إعادة استخدام مقطع عليه ترجمة قديمة — reusing a clip with old burned subtitles.
- **كيف / how:** python decaption.py VIDEO --out CLEAN.mp4 [--band 0.45:0.56] [--keep-credit] [--report]. Ran here: test_decaption_erases_a_burned_caption ok. **أرقام / params:** white V>205 S<55; yellow H 16–38 S>110 V>150; dark outline V<70 within 9 px; masks ±3 frames; Telea inpaint r 9; output crf 12
- **الدليل / proof:** `kosif-studio/motion/decaption.py:38` · `kosif-studio/motion/decaption.py:99` · `kosif-studio/tests/test_studio.py:850`

#### FOOT-27 · تمويه الوجوه والمناطق · Face & region privacy masks · 📦 بأمر تثبيت / one install
- **ماذا / what:** وجوه أو مناطق تُبكسل أو تُموه أو تُغطى في كل إطار مع تتبع وهامش واستمرار عند ضياع الكشف، والصوت كما هو. — Faces or regions pixelated, blurred or boxed every frame with tracking, margin and hold through misses; audio untouched.
- **متى أستخدمها / when:** مارة في الخلفية، أطفال، لوحات سيارات — bystanders, children, number plates.
- **كيف / how:** python scripts/kmotion.py privacy CLIP.mp4 --out safe.mp4 --mode pixelate|blur|box [--strength 18 --pad 0.25 --every 2 --hold 0.6] [--region x,y,w,h[,from,to]]. Detectors YuNet > Haar > skin. Here cv2 5.0 is present but has no Haar data, the YuNet ONNX is not shipped, and the skin fallback needs scipy — the test errors on that import. Manual regions work. Rules: faces ≥ 40 px tall at 4K are identifiable; one soft window over the whole path (softness ≥ 30%); mosaic block ≈ face height/4. ffmpeg crop→pixelize→overlay is verified here. **أرقام / params:** block = face/4; softness ≥ 30%; strength 18
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/privacy.py` · `100-superskills/skills/kosif-montage-motion/scripts/faces.py` · `100-superskills/skills/kosif-montage-motion/tests/test_v6.py:132` · `kosif-atlas/skills/1096-akbun-editvideo/2456-davinciresolve-face-mosaic/SKILL.md`
- **📦 تثبيت / install:** `pip install scipy  # or put face_detection_yunet_2023mar.onnx in scripts/kit/models/`

#### FOOT-28 · مفتاح اللون الأخضر · Chroma key · ✅ مُثبت هنا / proven here
- **ماذا / what:** أزل خلفية خضراء أو زرقاء أو سادة وركّب المتحدث فوق لقطات أو رسوم جديدة. — Remove a green, blue or plain backdrop and composite the speaker over new footage or graphics.
- **متى أستخدمها / when:** متحدث أمام شاشة خضراء أو حائط سادة — a presenter on green or a plain wall.
- **كيف / how:** [fg]chromakey=0x00FF00:similarity=0.10..0.18:blend=0.05..0.1,despill=type=green[k];[bg][k]overlay (YUV sources chromakey, RGB colorkey). تحققتُ منه في هذه الحاوية (ffmpeg 6.1.1، 2026-10-16) / verified in this container (ffmpeg 6.1.1, 2026-10-16). Browser variant (Basma chromaMask): YCbCr chroma distance with a luma term, smoothstep soft edge between 0.55·tol and tol, mask blur W/360; auto key from four 8×8 corner patches. **أرقام / params:** similarity 0.10–0.18; blend 0.05–0.1; Basma key #00b140 tol 0.22
- **الدليل / proof:** `kosif-atlas/skills/235-mas-video-lab/754-ffmpeg/SKILL.md` · `app/public/js/00_editor.js:2468`

#### FOOT-29 · تعديل الصورة: إعادة تلوين تحفظ الظلال · Picture edits: shading-preserving recolour · ✅ مُثبت هنا / proven here
- **ماذا / what:** «غيّر الذهبي إلى الأزرق» يُفهم محليًا بلا ذكاء اصطناعي، ويعيد التلوين مع حفظ الطيات والظلال. — 'Change the gold to blue' is parsed locally without AI and recoloured while keeping folds and shadows.
- **متى أستخدمها / when:** تعديل لون منتج أو ملابس في صورة المستخدم — recolouring a product or garment in a user photo.
- **كيف / how:** python edit_pack.py photo.jpg 'make the shirt red'; recolor(img, src_hex, dst_hex, tolerance=40, region, keep_shading=True) scales HSV saturation/value; also adjust, tint, paint, write, erase (blur-fill), flip. 18 Arabic colour names (ذهبي #d4a53a، كحلي #1f2d6b، عنابي #7b1e2b …). The original is kept as a <<KOSIF:ORIGINAL:sha>> key so any AI edits a program, not the bytes. Ran here: local-edit and colour-request tests ok. **أرقام / params:** tolerance 34–42; HSV match ≤ .6
- **الدليل / proof:** `kosif-studio/edit_pack.py:36` · `kosif-studio/edit_pack.py:226` · `kosif-studio/tests/test_studio.py:410`

#### FOOT-30 · معالجة الصور بـ ImageMagick · ImageMagick still post-processing · 🟢 جاهز / ready
- **ماذا / what:** قص ملء، إزالة الأبيض إلى شفافية، تقليم، تحويل وتدفئة قبل التحريك. — Fill-crop, white-to-alpha, trim, convert and warm grade before animating.
- **متى أستخدمها / when:** تجهيز صور مولّدة أو منتجات — preparing generated or product stills.
- **كيف / how:** Here the binary is 'convert' (ImageMagick 6), not 'magick'. Fill-crop: -resize WxH^ -gravity center -extent WxH; white→alpha: -fuzz 10% -transparent white, then -channel A -blur 0x1 -level 50%,100%; -trim +repage; WebP -quality 85; warm -modulate 100,110,105; -contrast-stretch 2%x1%. Single-colour logo backdrop alternative (Basma removeImgBG): corner colours must agree (spread ≤ 70), edge flood fill, anti-aliased alpha. **أرقام / params:** fuzz 10–15%; q 85
- **الدليل / proof:** `kosif-atlas/skills/881-codex-seo/1954-seo-image-gen` · `app/public/js/00_editor.js:2572`

## التركيب والعزل والتتبع — Compositing, matting & tracking

_عزل الشخص ووضع النص خلفه، تثبيت ملصق على جدار يتحرك، وتجميد لحظة والعالم يمشي._

#### FOOT-31 · عزل الشخص بقناع شفاف · Person matte / background removal · 📦 بأمر تثبيت / one install
- **ماذا / what:** يخرج قصاصة شفافة للمتحدث (webm/mov/png ألفا) مع لوح خلفي معكوس اختياري. — Produces a transparent cut-out of the presenter (webm/mov/png alpha) with an optional inverse plate.
- **متى أستخدمها / when:** نص خلف المتحدث، متحدث فوق عوالم متبدلة — text behind subject, speaker over swapped worlds.
- **كيف / how:** npx hyperframes remove-background presenter.mp4 -o presenter.webm [--background-output plate.mp4] [--quality fast|balanced|best (crf 30/18/12)] [--device auto|cpu]; u2net human seg at 320×320, ~9 fps on CoreML (slower on CPU here). Alternatives: pip install rembg (stills/frames), MediaPipe selfie segmentation in the browser (CDN), Transformers.js image-segmentation / depth-estimation in Node (models from Hugging Face, reachable). **أرقام / params:** 320×320 matte; quality crf 30/18/12
- **الدليل / proof:** `kosif-one/vendor/hyperframes/docs/guides/remove-background.mdx` · `kosif-one/vendor/hyperframes/skills/media-use/audio/references/remove-background.md` · `kosif-one/vendor/hyperframes/skills/embedded-captions/scripts/matte.cjs` · `app/public/js/00_editor.js:2466`
- **📦 تثبيت / install:** `npx hyperframes remove-background in.mp4 -o out.webm`
- **⚖️ ترخيص / license:** HyperFrames Apache-2.0؛ مكتبة u2net وأوزانها تُنزَّل عند أول تشغيل / HyperFrames is Apache-2.0; u2net weights download on first run.

#### FOOT-32 · عنوان خلف المتحدث · Title behind the speaker · 📄 موصوف / documented only
- **ماذا / what:** عنوان كبير يظهر خلف جسد المتحدث ووجهه واضح. — A large title appears behind the speaker's body while the face stays clear.
- **متى أستخدمها / when:** افتتاح بودكاست أو مقابلة — podcast or interview openers.
- **كيف / how:** Three layers in lockstep with the same data-start: z1 full mp4 base, z2 headline, z3 alpha webm cut-out. Timing 0–1 s shot, 1–2 s title reveal, 2–5 s hold. Check hair and hands; never cover eyes or mouth. Photo version: title sandwiched between background and cut-out subject (≤ 3 layers). **أرقام / params:** 5 s; 3 layers
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/hyperframes-creative/references/composition-patterns.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-tracking-compositing.md` · `kosif-tool/playbooks/photos.md:18-19`

#### FOOT-33 · متحدث مقصوص فوق عوالم متبدلة · Rotoscoped speaker over swapped worlds · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** المتحدث مقصوص بحد أبيض فوق خلفية مختلفة لكل جملة. — The speaker, cut out with a white outline, sits over a different backdrop per sentence.
- **متى أستخدمها / when:** ريلز تعليمية مرحة — playful explainer reels.
- **كيف / how:** Matte per frame (FOOT-31), add a 6–8 px white outline and a 20 px soft shadow, swap the backdrop on sentence boundaries from words.json. **أرقام / params:** outline 6–8 px; shadow 20 px
- **الدليل / proof:** `style:pm-sab8a-364a5a`

#### FOOT-34 · تسمية متتبعة ودائرة اهتمام · Tracked callout & attention ring · 🟢 جاهز / ready
- **ماذا / what:** نقطة وخط قصير مثبتان على جزء متحرك، أو دائرة رفيعة تلاحق تفصيلة صغيرة أثناء الشرح. — A dot and short leader stay pinned to a moving part, or a thin ring follows a small detail during the explanation.
- **متى أستخدمها / when:** شرح جزء في منتج يتحرك — explaining a part of a moving product.
- **كيف / how:** Track to a null with an OpenCV point tracker (cv2 5.0 is importable here) or manual keys every few frames + interpolation; draw the overlay in HTML at the tracked coordinates. Hide the label when the target is occluded or leaves frame; never cover the evidence. Timing: 0–1 intro, 1–2 line appears, 2–6 track. **أرقام / params:** 6 s / 5 s beats
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-tracking-compositing.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/ideas-index.md`

#### FOOT-35 · إدراج بمنظور مثبت بأربع نقاط · Planar corner-pin inserts · 📄 موصوف / documented only
- **ماذا / what:** ملصق يتبع منظور حائط والكاميرا تتحرك، أو بطاقة في يد تصبح رسمًا يتبع ميلها والأصابع فوقها. — A sticker follows a wall's perspective as the camera moves, or a card held in a hand becomes a diagram following its tilt with fingers on top.
- **متى أستخدمها / when:** إعلانات ودمج رسومات في لقطات حقيقية — ads and graphics in real footage.
- **كيف / how:** Four-corner keyframes (manual or an OpenCV homography) → CSS matrix3d per frame, or ffmpeg perspective=x0:y0:x1:y1:x2:y2:x3:y3 (تحققتُ منه في هذه الحاوية (ffmpeg 6.1.1، 2026-10-16) / verified in this container (ffmpeg 6.1.1, 2026-10-16).). Add matching grain and blur; finger masks + their shadow stay on top. No fake certificates or ads. **أرقام / params:** 6 s each
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-tracking-compositing.md` · `kosif-atlas/skills/235-mas-video-lab/754-ffmpeg/SKILL.md`

#### FOOT-36 · تجميد الشخص والعالم يمشي · Freeze the subject, keep the world moving · 📄 موصوف / documented only
- **ماذا / what:** المؤدي يتجمد داخل الإطار والخلفية القصيرة تستمر. — The performer freezes while a short background keeps moving.
- **متى أستخدمها / when:** لحظة رياضية أو فنية — a sports or art highlight.
- **كيف / how:** 0–1 s motion, 1–3 s subject frozen, 3–4 s return: frozen frame of the person + matte overlaid on the running plate; a clean plate where the original body ghosts through. Chronophotography variant: 3 frozen, spaced poses with an opacity/colour gradient, then motion resumes — copies are time markers, not extra people. **أرقام / params:** 4 s; 3 ghost poses in 5 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-tracking-compositing.md` · `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-music-sports.md`

#### FOOT-37 · سينماغراف · Cinemagraph · 📦 بأمر تثبيت / one install
- **ماذا / what:** صورة ثابتة فيها منطقة واحدة حية (بخار فوق فنجان) بدورة تقسم المدة فتتكرر بلا قفزة. — A still with one feathered living region (steam over a cup) whose period divides the duration so it loops seamlessly.
- **متى أستخدمها / when:** خلفيات هادئة، قهوة، دعاء — calm backdrops, coffee, dua films.
- **كيف / how:** Driven only by seek time; period divides the clip length. HyperFrames block cinemagraph (10 s, swap the placeholder for your still + masked looping video). **أرقام / params:** 10 s; period | duration
- **الدليل / proof:** `kosif-one/vendor/hyperframes/registry/blocks/cinemagraph/cinemagraph.html`
- **📦 تثبيت / install:** `npx hyperframes add cinemagraph`
- **⚖️ ترخيص / license:** HyperFrames Apache-2.0؛ مكتبة u2net وأوزانها تُنزَّل عند أول تشغيل / HyperFrames is Apache-2.0; u2net weights download on first run.

#### FOOT-38 · مقارنة قبل وبعد صادقة · Honest before/after wipe · 📄 موصوف / documented only
- **ماذا / what:** خط فاصل يتحرك بين الأصل والنتيجة بنفس الكادر. — A divider moves between original and result in the same framing.
- **متى أستخدمها / when:** ترميم، تلوين، تعديل — restoration, grading, retouching.
- **كيف / how:** 0–1 s define both, 1–4 s divider moves, 4–6 s stop; linear mask + 2 px divider + date/condition label. Never change light or lens between the sides. Local: HTML clip-path inset, or ffmpeg overlay with an animated crop. Matte-vs-composite split (key pass left, final right) is a strong compositing reveal. **أرقام / params:** 6 s; divider 2 px; wipe 600 ms–1.2 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-product-ads.md` · `style:pm-blueoctopusai-dd17bd`

## الصور إلى حركة — Photos into motion

_كين بيرنز بسرعة ثابتة، بارالاكس بمعاملات عمق، ونص لا يغرق في الصورة._

#### FOOT-39 · كين بيرنز الصحيح · Ken Burns done well · ✅ مُثبت هنا / proven here
- **ماذا / what:** دفع أو تحريك بسرعة ثابتة، حركات متناوبة، بلا توقفات منحنية، والتحريك من اليمين للعربية. — Constant-velocity push or pan, alternating moves, no eased stops; pans run right-to-left for Arabic.
- **متى أستخدمها / when:** أي صورة ثابتة في فيلم — every still in a film.
- **كيف / how:** 1.00→1.06 over 4–6 s (1–1.5%/s), ceiling 1.12, pan < 6% of width; linear or cubic-bezier(0.37,0,0.63,1) before a cut. ffmpeg: zoompan=z='min(1+0.0004*on,1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=150:s=1080x1920:fps=30 (تحققتُ منه في هذه الحاوية (ffmpeg 6.1.1، 2026-10-16) / verified in this container (ffmpeg 6.1.1, 2026-10-16). — feed a source ≥ 1.5× the output to avoid zoompan jitter). Documentary hold: push 1.055 + pan 4% over 4.5 s, lower third enters 600–1100 ms. **أرقام / params:** 1.00→1.06 / 4–6 s; max 1.12
- **الدليل / proof:** `kosif-tool/playbooks/photos.md:32` · `kosif-tool/playbooks/photos.md:48-55` · `100-superskills/skills/trend-animation-styles/references/styles.md`

#### FOOT-40 · بارالاكس مستوي بمعاملات عمق · Planar parallax with depth factors · 🟢 جاهز / ready
- **ماذا / what:** إزاحة كل طبقة = إزاحة الكاميرا × معامل عمقها، مع حركة مقصودة وانجراف دائم بجيبين. — Layer offset = camera offset × depth factor, plus an intentional move and a perpetual two-sine drift.
- **متى أستخدمها / when:** صورة مقسومة لطبقات (سماء، شخص، مقدمة) — a photo cut into layers.
- **كيف / how:** x = 6·sin(2πt/7) + 4·sin(2πt/11), y periods 9 s / 13 s; one camera function (pan + drift + linear zoom) × depth in both Remotion and the Canvas seek version (ParallaxPhoto, 1080×1920, 5 s). Skip parallax when the long side < 1600 px or the subject can't be separated. Oversize each layer by 2× max travel + 4% and put a 1.3× copy blurred 24 px behind to hide edges; depth blur ~1 px per 100 px of distance (bg 3, mid 1), never on the subject. **أرقام / params:** bg 0.15 · mid 0.45 · subject 1.0 · occluder 1.4; zoom ≤ 1.10; drift ≤ 12 px; pans 30–60 px/s
- **الدليل / proof:** `kosif-tool/playbooks/photos.md:34` · `kosif-tool/playbooks/photos.md:103-185` · `kosif-tool/playbooks/photos.md:20` · `kosif-tool/playbooks/photos.md:22` · `kosif-tool/styles/parallax-2d/STYLE.json`

#### FOOT-41 · كشف بارالاكس ثلاثي ومن الكولاج إلى البطل · Three-layer reveal & collage → hero · 📄 موصوف / documented only
- **ماذا / what:** طبقات تظهر، الشخص يقفز، تحريك 40 بكسل، والعنوان ينزلق بين الخلفية والشخص؛ أو شبكة صور تنهار إلى صورة بطل. — Layers fade, the subject pops, a 40 px pan, the title slides between background and subject; or a photo grid collapses to one hero.
- **متى أستخدمها / when:** افتتاح سيرة أو قصة صور — biography or photo-story openers.
- **كيف / how:** Reveal: bg scale 1.15, mid 1.06; subject 200–800 ms spring 14/120; pan 400–2600 ms; title 900–1400 ms; push 1.5%/s. Collage: 2×3 grid enters from the top-right (RTL) with 60 ms stagger over 400 ms, drifts 20 px, exits 250 ms with 40 ms stagger, hero pushes 1.06. **أرقام / params:** subject spring 14/120; grid stagger 60 ms
- **الدليل / proof:** `kosif-tool/playbooks/photos.md:57-65` · `kosif-tool/playbooks/photos.md:67-74`

#### FOOT-42 · حماية النص فوق الصور واللقطات · Text protection over photos & footage · 📄 موصوف / documented only
- **ماذا / what:** النص فوق صورة مزدحمة يجلس على تدرج لا مربع أسود، ويُتحقق من التباين إطارًا بإطار. — Text over a busy picture sits on a gradient scrim, not a black box, and contrast is checked per frame.
- **متى أستخدمها / when:** كل نص فوق لقطة حقيقية — every caption over real footage.
- **كيف / how:** Gradient 0.6→0 over 35% of frame height, contrast ≥ 4.5:1, text ≥ 36 px; or a 40–60% black scrim, a solid pill, or stroke/shadow. Verify luminance in the caption band with ffmpeg signalstats YAVG per frame (تحققتُ منه في هذه الحاوية (ffmpeg 6.1.1، 2026-10-16) / verified in this container (ffmpeg 6.1.1, 2026-10-16).). Dark product plates: navy multiply overlay 40–55% + vignette so oversized type reads. **أرقام / params:** scrim 0.6→0 / 35% H; contrast ≥ 4.5:1
- **الدليل / proof:** `kosif-tool/playbooks/photos.md:23` · `kosif-tool/playbooks/photos.md:197` · `kosif-atlas/skills/1503-universal-design-principles/3825-legibility-contrast-and-spacing/SKILL.md` · `style:pm-deifosv-04e4d3`

#### FOOT-43 · صورة أرشيف تنفتح على الحاضر · Archive photo opens onto the present · 📄 موصوف / documented only
- **ماذا / what:** إطار صورة قديمة يتمدد حتى يطابق المكان نفسه في لقطة حديثة ثم يذوب. — An old print's frame expands to match the same place in modern footage, then dissolves.
- **متى أستخدمها / when:** وثائقي، تاريخ مدينة، قبل/بعد زمني — documentary, city history.
- **كيف / how:** 0–2 s photo, 2–5 s match (perspective corner pin + scale), 5–8 s modern scene with a tuned dissolve; show the photo date; never imply a false location match; sound moves from old to modern ambience. Documentary style: warm dark #15130F, ivory #EFE6D8, red #C0392B; Amiri 700 + IBM Plex Sans Arabic 500; Ken Burns 1.0→1.08 over 6 s. **أرقام / params:** 8 s
- **الدليل / proof:** `kosif-atlas/skills/motion-graphics-ar/motion-style-director/references/motion-cinematic-titles.md` · `100-superskills/skills/trend-animation-styles/references/styles.md`

#### FOOT-44 · قواعد الصور للعربية · RTL photo layout rules · 📄 موصوف / documented only
- **ماذا / what:** الكشف من اليمين، الشبكات من أعلى اليمين، الشخص يسار والنص يمين، ولا تعكس صورة فيها كتابة أو علم أو شعار. — Reveals RTL, grids from top-right, subject left and text right; never mirror photos with writing, flags, logos or steering wheels.
- **متى أستخدمها / when:** كل فيلم صور عربي — every Arabic photo film.
- **كيف / how:** Margins 5% / 12%; pills inherit their layer's transform; fixed depth order background → mid → cut-out subject → graphics. **أرقام / params:** margins 5%/12%
- **الدليل / proof:** `kosif-tool/playbooks/photos.md:193-199`

#### FOOT-45 · أساليب الصور الجاهزة · Photo styles to scaffold · 🟢 جاهز / ready
- **ماذا / what:** بارالاكس 2D، مونتاج مختلط فيروسي، ومونتاج تحريري — جاهزة للبناء. — 2D parallax, viral mixed media and editorial montage — ready to scaffold.
- **متى أستخدمها / when:** بداية أي فيلم صور في kosif-tool — starting a photo film.
- **كيف / how:** python3 tools/kosif.py scaffold parallax-2d|viral-mixed-media|editorial <dir>; list --category photos (34 entries). Viral mixed media: beat-cut every 1–2 s, cut-outs with contact shadow, ≤ 7 words of kinetic type, grain 2–4%. Editorial: photo rig + type grid, masks and wipes 350–500 ms, one grade, grain, vignette 10–15%.
- **الدليل / proof:** `kosif-tool/styles/parallax-2d/SKILL.md` · `kosif-tool/styles/viral-mixed-media/SKILL.md` · `kosif-tool/styles/editorial/SKILL.md` · `kosif-tool/playbooks/photos.md`

#### FOOT-46 · شرائح الفلاتر وجدار الصور · Filter strips & tile walls · 👁 شوهد في فيديو / seen in a reference video
- **ماذا / what:** الصورة نفسها في أعمدة بفلتر مختلف لكل عمود، أو جدار مربعات 9:16 تنجرف ببطء. — The same photo in N columns, each with its own filter; or a wall of 9:16 tiles drifting slowly.
- **متى أستخدمها / when:** عرض أنماط تلوين أو كمية محتوى — showing grade options or content volume.
- **كيف / how:** Columns reveal with 80 ms stagger and labels below; tile wall at varied offsets drifting 10–40 px/s; collage flash variant: scanned detail crops hard-cut every 300 ms with a click per hit. **أرقام / params:** stagger 80 ms; flash 300 ms
- **الدليل / proof:** `style:pm-oliahmed205-3e31c4` · `style:pm-twoclipping-6dd14e` · `kosif-tool/styles/pm-abderrahmen-g-9e8ed0/BRIEF.md`

## اللقطات داخل التكوين والعرض — Footage inside compositions

_الفيديو الحقيقي كطبقة في HTML: قابل للبحث بدقة الإطار، تحت النص، ومعروض بأناقة في 9:16._

#### FOOT-47 · لوح لقطات كل إطاراته مفتاحية · All-intra seekable footage plate · ✅ مُثبت هنا / proven here
- **ماذا / what:** يعيد ترميز المقطع بحيث كل إطار مفتاحي، فيُبحث <video> داخل التكوين بدقة الإطار، ويطبع الوسم الجاهز. — Re-encodes a clip so every frame is a keyframe, letting a <video> inside a composition seek frame-exactly; prints the tag to paste.
- **متى أستخدمها / when:** أي لقطة حقيقية داخل فيلم HTML — any real clip inside an HTML film.
- **كيف / how:** python motion.py footage CLIP --out projects/X/assets/clip.mp4 [--from 0 --dur 5 --width 1280 --fps 30] (libx264 -g 1 crf 16, Lanczos, muted, yuv420p, +faststart). In the page: <video data-start data-duration muted>; the motion-kit shim seeks currentTime = t − start, hides it outside its span and waits for 'seeked' (0.5 ms tolerance). Ran here: a 3 s test clip came out with all 90 frames as keyframes and the ready tag. **أرقام / params:** -g 1; crf 16; width 1280; 30 fps
- **الدليل / proof:** `kosif-studio/motion/motion.py:496` · `100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js:474` · `100-superskills/skills/kosif-montage-motion/scripts/motion.py:548`

#### FOOT-48 · عرض الأفقي في 9:16 فوق نسخة مموهة · Landscape in 9:16 over a blurred fill · ✅ مُثبت هنا / proven here
- **ماذا / what:** الإطار الأفقي كاملًا فوق نسخة مكبرة مموهة بدل قص الوسط الذي يخفي الحدث. — The whole landscape frame over a blurred enlarged copy instead of a centre crop that hides the action.
- **متى أستخدمها / when:** لقطات أفقية في ريلز — landscape clips in reels.
- **كيف / how:** split → scale+crop to 1080×1920 + boxblur=40:2 → overlay the 1080-wide foreground centred (تحققتُ منه في هذه الحاوية (ffmpeg 6.1.1، 2026-10-16) / verified in this container (ffmpeg 6.1.1, 2026-10-16).). The montage tool picks this chain automatically (_fit_chain, MixedMontage test ok here). Screenshots never appear raw: rounded 12–16 px corners, shadow and a designed background or device frame. **أرقام / params:** 1080×1920; boxblur 40:2; radius 12–16 px
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/tests/test_fetch_lab.py:93` · `kosif-atlas/skills/1511-homie/3903-video/references/DELIVERY.md`

#### FOOT-49 · لقطة متحدث تحت الرسوم · Real footage plate under graphics · 🟢 جاهز / ready
- **ماذا / what:** مقطع الكلام العمودي هو اللوح، والرسوم والضوء والجسيمات والترجمة طبقات HTML فوقه، وكاميرا افتراضية تحركه. — The vertical talking clip is the plate; graphics, light, particles and captions are HTML layers above it, with a virtual camera moving the plate.
- **متى أستخدمها / when:** ريل كلام مصقول — a polished talking reel.
- **كيف / how:** <div id=cam><video id=plate data-start=0 data-duration=… muted></div> + layers (#bloom, #rays, #scrim 52%→.74, #vig, #dim, #particles) + SVG + type; prepare the plate with FOOT-47. Opening: plate starts saturate(.55) brightness(.92) and blooms to full colour in 0.6 s power3.out as the hook word lands, dim overlay 0.42→0 in 0.55 s. Under kinetic type: alternate push 1.04→1.10 / 1.10→1.04 per shot (smoothstep), kick +1.8%, payoff brightness +22%. **أرقام / params:** 1080×1920, 30 fps; push 1.04↔1.10
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:45` · `100-superskills/skills/kosif-montage-motion/scripts/projects/premium_edit/index.html:144` · `100-superskills/skills/kosif-montage-motion/templates/verse.html:140`

#### FOOT-50 · محرك المونتاج الموجّه · Directed-edit engine · 🟢 جاهز / ready
- **ماذا / what:** يحوّل مواصفة تحرير فوق لقطة متحدث إلى تايملاين واحد: دفع بطيء لكل لقطة، ضربات كلمات مفتاحية، ثلاثة مستويات نص، فصول، ونهاية مقصودة. — Turns an edit spec over a talking-head plate into one timeline: slow push per shot, keyword punches, three text levels, chapters and a deliberate end.
- **متى أستخدمها / when:** «اعمل مونتاج لهذا الكلام» بمشروع قابل للتعديل — an editable directed edit.
- **كيف / how:** kmotion direct CLIP → edit.js (window.EDIT: shots, punches, captions, keys, motifs, chapters, payoff, credit, palette) → directed.html builds the GSAP timeline; sizes designed at 1080 px wide. **أرقام / params:** punch expo.out 0.14 s then −60% over 0.6 s; hook dim .38→0 in .55 s; ivory #F5F0E6; accent #E7B65A
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/templates/directed.html:44` · `100-superskills/skills/kosif-montage-motion/scripts/direct.py`
- **⚖️ ترخيص / license:** GSAP مدمج برخصة GSAP القياسية — ليست MIT / vendored GSAP under its standard license (not MIT).

#### FOOT-51 · إعادة تغليف المتحدث ببطاقات · Talking-head recut with designed cards · 📦 بأمر تثبيت / one install
- **ماذا / what:** مقابلة أو بودكاست كما هو، مع بطاقات متزامنة مع النص: عناوين، أسماء، أرقام، اقتباسات، لوحات جانبية، صورة داخل صورة. — An interview/podcast untouched, wrapped in transcript-synced cards: titles, lower-thirds, data callouts, pull-quotes, side panels, PiP.
- **متى أستخدمها / when:** مقاطع بودكاست للسوشيال — podcast clips for social.
- **كيف / how:** ffprobe + audio → hyperframes transcribe → corrected transcript → storyboard.json (schemaVersion 3; layout, themeId, seed; cards[zone, startSec]) → per-card HTML → one paused master timeline → render. Footage stays untouched; the wrapper tweens between layouts.
- **الدليل / proof:** `kosif-one/vendor/hyperframes/skills/talking-head-recut/SKILL.md` · `kosif-one/vendor/hyperframes/skills/talking-head-recut/media-contract.test.mjs`
- **📦 تثبيت / install:** `npx hyperframes transcribe talk.mp4`
- **⚖️ ترخيص / license:** Apache-2.0 + MIT (مقتبس من vtake-skills)

#### FOOT-52 · فيديو ولوتي داخل HTML · Video & Lottie inside HTML compositions · 📦 بأمر تثبيت / one install
- **ماذا / what:** لقطات مكتومة في إطار مستدير وحركات Lottie متجهة داخل التايملاين، تُبحث من الساعة الرئيسية. — Muted footage in a rounded frame and Lottie vector animations inside the timeline, sought from the master clock.
- **متى أستخدمها / when:** شعارات Lottie جاهزة أو لقطات منتج داخل التصميم — ready Lottie marks or product clips in a layout.
- **كيف / how:** Seek video.currentTime and lottie goToAndStop(frame) from t (autoplay false). Frame example 680×840 r16; Lottie pop 0.3→1 in 0.35 s back.out(1.6). Backdrops (Basma drawBG): cover fit, blur, 5% breathing zoom on stills, dim 0–0.8. **أرقام / params:** lottie pop 0.35 s back.out(1.6)
- **الدليل / proof:** `kosif-atlas/skills/2702-hyperframes/10381-website-to-hyperframes/references/techniques.md` · `app/public/js/00_editor.js:2443`
- **📦 تثبيت / install:** `npm i lottie-web`

#### FOOT-53 · مشغل مقدمة سينمائية متكيف · Adaptive cinematic intro player · ✅ مُثبت هنا / proven here
- **ماذا / what:** طبقة فيلم كامل الشاشة تختار 4K أو 720p حسب الشاشة والشبكة، ولا تحجب الشاشة الحقيقية أبدًا. — A full-screen film overlay that picks 4K or 720p by viewport and network and never blocks the real entry screen.
- **متى أستخدمها / when:** تسليم فيلم داخل موقع أو تطبيق — shipping a film inside a site or app.
- **كيف / how:** 4K only if width ≥ 1100 px, effectiveType not 2g/3g and no saveData; on error retry 720p once; poster fallback; failsafe close 14 s; close 950 ms after 'ended'; skip when seen this session, deep link, reduced motion, saveData or deviceMemory ≤ 2; muted autoplay + sound toggle; focus trap; Escape skips. Ran here: node tools/brand_art.test.mjs → pass 5, fail 0. **أرقام / params:** breakpoint 1100 px; failsafe 14 s; end hold 950 ms
- **الدليل / proof:** `kosif-earth-ci-fork/ui/art/brand/earth-intro-20261009.js` · `kosif-earth-ci-fork/tools/brand_art.test.mjs`

## المونتاج التلقائي — Auto-edit workflows

_من مجلد لقطات أو مقطع كلام إلى فيلم كامل بأمر واحد — ثم راجع._

#### FOOT-54 · مونتاج تلقائي على الموسيقى · Auto montage to music · ✅ مُثبت هنا / proven here
- **ماذا / what:** إيقاعات، أفضل النوافذ، دفع للصور، الأفقي فوق نسخة مموهة، −14 LUFS، واعتمادات. — Beats, best windows, photo pushes, landscape over a blurred copy, −14 LUFS and credits.
- **متى أستخدمها / when:** «ركّب لي هذه اللقطات على الأغنية» — 'cut these clips to this song'.
- **كيف / how:** kmotion montage MEDIA --music track --ratio 9:16 [--grade] [--voice] [--captions]; montage.cut([dir], music, out, ratio='9:16', punch=False). Ran here: MixedMontage folder-photos-and-fit test ok. Grammar: quick ~1 s and breathing ~3 s shots, breathing shots end on downbeats, zoom punches on downbeats (2× supersampled), grades teal_orange, golden_hour, cyberpunk, vintage_film, matrix_tech, clean_commercial, magma_night, blue_hour, sodium_night; sidechain ducking; −14 LUFS / −1 dBTP. **أرقام / params:** quick ~1 s / breathing ~3 s; −14 LUFS
- **الدليل / proof:** `100-superskills/skills/kosif-montage-motion/scripts/montage.py` · `100-superskills/skills/kosif-montage-motion/tests/test_fetch_lab.py:93` · `kosif-studio/motion/montage.py:42`

#### FOOT-55 · ريل من مقطع كلام بأمر واحد · One-command talking-clip reel · 🟢 جاهز / ready
- **ماذا / what:** مقطع كلام خام ← ريل عمودي: تفريغ ومسح ترجمة بالتوازي، ترميم وتأطير، سلسلة صوت، موسيقى عند الحاجة، كاريوكي واعتماد، −14 LUFS وبوابة تسليم. — Raw talking clip → finished vertical short: transcribe + decaption in parallel, restore + reframe, voice chain, music only if none, karaoke + credit, −14 LUFS, delivery gate.
- **متى أستخدمها / when:** «حوّل هذا الفيديو لريل» — 'turn this into a reel'.
- **كيف / how:** python reel.py CLIP.mp4 --out FINAL.mp4 [--size 1080x1920 --model large-v3|small --music auto|none|bed.wav --style reels|tiktok|hormozi|boxed|minimal|cinema|punchy --credit '…' --transcript words.json]. Owner's recorded run IMG_9262: gate ok, −14.5 LUFS, TP −2.7, caption band 598–706. Needs faster-whisper for transcription (see SYNC). **أرقام / params:** intermediate crf 12; final crf 16; −14 LUFS
- **الدليل / proof:** `kosif-studio/motion/reel.py:92` · `kosif-studio/out/reel_test/IMG_9262_reel.reel.json` · `100-superskills/skills/kosif-montage-motion/scripts/reel.py`

#### FOOT-56 · ريلز من فيديو طويل · Reels from a long video · 🔑 مفتاح أو خدمة / needs key or service
- **ماذا / what:** يقطع 1–8 ريلز من محاضرة طويلة: خطّاف إلى خلاصة ينتهي بجملة كاملة، ثم ترجمة وعنوان وكاميرا متحدث وصوت منظف. — Cuts 1–8 vertical reels from a long talk: self-contained hook-to-payoff highlights ending on full sentences, then captions, a hook title, talking-head camera and cleaned speech.
- **متى أستخدمها / when:** محاضرة أو بودكاست طويل — long lectures or podcasts.
- **كيف / how:** REELS.find({count, length}): count 5 (> 600 s), 3 (> 180 s) else 2, max 8; length 15–75 s (default 40); an AI picks from a timed transcript (≤ 24,000 chars). Local fallback REELS.local scores windows by words/second snapped to sentences (break on . ! ؟ ? … or > 9 s) — usable without a key. Shorts handles: 60 s + 2×15 s pre/post needs 90 s of source. **أرقام / params:** 1–8 reels; 15–75 s
- **الدليل / proof:** `app/public/js/10_studio.js:4017` · `app/public/js/10_studio.js:4039` · `100-superskills/skills/reels-shorts-factory/references/sources.md:148`

#### FOOT-57 · المونتاج الذكي الكامل من الكلام · Smart full montage from speech (AutoEdit) · 🔑 مفتاح أو خدمة / needs key or service
- **ماذا / what:** صوت أو فيديو ← تفريغ بالكلمة ← سيناريو ومشاهد ← لقطات مطابقة ← قطع على الكلمات ← ترجمة ← مراجعة ← رندر. — Audio/video → word-level transcript → scenario and scenes → matching footage → cuts on the words → captions → review → render.
- **متى أستخدمها / when:** تعليق صوتي يحتاج B-roll — voice-overs that need B-roll.
- **كيف / how:** window.BasmaAutoEdit.run (9:16, pace med, 2 caption words); sources Openverse/Wikimedia (+ Pexels/Pixabay with keys — blocked from this container), motion-graphics inserts, SFX, VFX plan (grade, particles, grain, leak, vignette, letterbox, ≤ 4 crash-zoom accents). Needs the Basma app and its AI keys. Rule: cover silences and abstract explanation with real footage, one mood and one light across the pool.
- **الدليل / proof:** `app/public/js/50_autoedit.js:4` · `app/public/js/50_autoedit.js:427` · `100-superskills/skills/kosif-montage-motion/references/montage_grammar.md`

#### FOOT-58 · مونتاج لقطات المستخدم على الإيقاع (بصمة) · Basma automatic beat montage · 🔑 مفتاح أو خدمة / needs key or service
- **ماذا / what:** حتى 24 لقطة وصورة: يدرس كل لقطة، يرتبها الذكاء من لوحة مرقمة، ويقطع على الإيقاع مع حركات كاميرا وانتقالات ومؤثرات. — Up to 24 clips/photos: probes each, an AI orders them from a numbered contact sheet, cuts on the beat with camera moves, transitions and SFX.
- **متى أستخدمها / when:** داخل تطبيق بصمة — inside the Basma app.
- **كيف / how:** MON.run: probe in parallel batches of 3; 4-column numbered sheet; AI decides order, hook title, 0–6 lines, pace and grade; lengths snapped to beats within 0.4 s; bestWindow picks lively, sharp, well-lit windows away from cuts. Pro variant (PROMONT) adds template motion inserts. **أرقام / params:** ≤ 24 clips; 4–180 s; snap ≤ 0.4 s
- **الدليل / proof:** `app/public/js/10_studio.js:1865` · `app/public/js/10_studio.js:2069` · `app/public/js/30_promontage.js:41`

## توليفات قوية / power combos

- **ريل من مقطع كلام / talking reel:** FOOT-55 + FOOT-26 + FOOT-48 + SYNC (كاريوكي من words.json) + BEAT (موسيقى مخفوضة −14 LUFS) + QA (بوابة التسليم) — مقطع خام إلى ريل عمودي بأمر واحد.
- **مونتاج رحلة على أغنية / trip montage:** FOOT-11 + FOOT-10 + FOOT-54 + FOOT-24 + COLOR (تلوين golden_hour) + TRANS (قطعات على الضربات) — لقطات هاتف منظفة ومقطوعة على الإيقاع.
- **وثائقي من صور أرشيف / archive documentary:** FOOT-39 + FOOT-40 + FOOT-43 + FOOT-42 + MAP (مسار) + VOICE (تعليق) — صور ثابتة تتنفس بسرعة ثابتة، وتاريخ ظاهر لكل صورة.
- **افتتاح بودكاست / podcast opener:** FOOT-31 + FOOT-32 + FOOT-51 + ARAB (عنوان ضخم) + GLOW (ضوء خلفي) — العنوان خلف المتحدث ووجهه واضح.
- **«اعمل مثل هذا الريل» / match a reference reel:** FOOT-13 + FOOT-04 + FOOT-16 + TRANS + QA — قِس الحدود بالإطار، اجمع لقطات بنفس المعنى، وأعد البناء بتايملاين JSON.
- **إعلان منتج بلقطات حقيقية / product ad on real footage:** FOOT-35 + FOOT-34 + FOOT-38 + UI (موك أب) + TYPE — ملصق يتبع المنظور وتسمية متتبعة ومقارنة صادقة.
- **فيلم دعاء هادئ بخلفية حية / calm dua film:** FOOT-37 + FOOT-49 + FOOT-42 + PART (غبار) + GLOW (أشعة) + VOICE (بلا موسيقى) — صورة حية واحدة ونص محمي.

## أخطاء ممنوعة / never do

1. **لا تستخدم لقطة بلا مصدر ورخصة** — المرجع ليس إذنًا؛ سطر في ASSETS.md لكل ملف (FOOT-01).
2. **لا تقطع بـ -c copy عند إطار غير مفتاحي** — يتجمد الفيديو 2–5 ث؛ أعد الترميز أو اقطع داخل التكوين (FOOT-17).
3. **لا تقص وسط الإطار الأفقي في 9:16 عندما يخفي الحدث** — ضع الإطار كاملًا فوق نسخة مموهة (FOOT-48).
4. **لا كين بيرنز بتوقف منحنٍ ولا تكبير فوق 1.12** — يبدو كسولًا ويكشف البكسلات؛ سرعة ثابتة ومصدر ≥ 1.5× (FOOT-39, FOOT-15).
5. **لا تعكس صورة فيها كتابة أو علم أو شعار أو مقود** — يفضح التلاعب (FOOT-44).
6. **لا نص فوق لقطة مزدحمة بلا حماية** — ينجح في إطار ويسقط في التالي؛ تدرج وقياس YAVG (FOOT-42).
7. **لا تثبيت لكل لقطة بلا قياس** — يشوّه الحواف ويقص؛ ثبّت ما يهتز فعلًا وقص ≤ 10% (FOOT-24).
8. **لا تغيّر الإضاءة أو العدسة بين جانبي قبل/بعد** — مقارنة مزيفة (FOOT-38).
9. **لا تطلب لقطات من Pexels أو Pixabay من هذه الحاوية** — 403؛ استخدم Wikimedia/archive.org أو ملفات المستخدم (FOOT-02).
10. **لا تُظهر وجه صانع محتوى «بلا وجه» ولو إطارًا واحدًا، ولا وجوه المارة دون تمويه** (FOOT-01, FOOT-27).
11. **لا ترفع الدقة لكل مقطع على حدة** — مرة واحدة على المونتاج النهائي، والضبابية لا تُصلح (FOOT-15).

## أقوى 5 حركات توقيع / 5 signature moves

1. **FOOT-08 + FOOT-09 — اقرأ اللقطات قبل أي شيء:** حدود القطع بـ scdet ولوحة لقطات في ثوانٍ.
2. **FOOT-16 — تايملاين JSON بأمر واحد:** قص وزوم وتلوين ومنحدر سرعة وانتقالات وطبقات نص، مع بوابة −14 LUFS.
3. **FOOT-39 + FOOT-40 — صورة تتنفس:** 1.00→1.06 في 4–6 ث، وطبقات بمعاملات 0.15/0.45/1.0/1.4.
4. **FOOT-49 + FOOT-47 — لقطة حقيقية تحت الرسوم:** لوح all-intra قابل للبحث، يزهر من باهت إلى ملون مع كلمة الخطّاف.
5. **FOOT-31 + FOOT-32 — النص خلف المتحدث:** ثلاث طبقات متزامنة والوجه دائمًا واضح.

## إضافات من Cinematic Director PRO v5

_مستخلصة من حزمة المالك KOSIF Claude Cinematic Director PRO v5 (انظر [cinematic-director-pro.md](../cinematic-director-pro.md)). مسارات الدليل `owner-upload:` تشير إلى ملفات داخل أرشيف المالك، لا إلى هذا المستودع._

#### FOOT-P01 · إعادة مونتاج اللقطات من قائمة قطع محدودة · Bounded EDL recut: trim/concat with denoise and loudnorm · ✅ مُثبت هنا / proven here
- **ماذا / what:** يأخذ فيديو أصليًا وقائمة نطاقات --cut START:END فيقصّها ويرتبها ويعيد قياسها إلى مقاس الهدف مع صوتها، ويترك الأصل كما هو. / Takes a source and explicit --cut ranges, trims, concatenates and reframes them with their audio, leaving the original untouched.
- **كيف / how:** ffprobe first; each range must be finite, 0 ≤ a < b ≤ duration+0.03 and ≥ 0.10 s; at most 30 cuts; refuses output == input. Per cut: trim + setpts, scale=W:H:force_original_aspect_ratio=decrease, pad centred, fps, setsar=1, yuv420p; audio atrim + asetpts + aresample=48000 (+ afftdn=nf=-25 with --denoise); concat=n:v=1:a=1; --normalize appends loudnorm=I=-16:TP=-1.5:LRA=11. No-audio sources get -an. Prints a JSON receipt (duration, streams, cuts, denoised). Re-ran here on the bundled 4 s test clip with --cut 0:1.2 --cut 2:3.4 --denoise --normalize → 2.625 s, h264 480×854 24 fps + AAC. Note: loudnorm here targets −16 LUFS; the superpowers delivery target is −14 LUFS, so pass the final mix through your own loudnorm step. **أرقام / params:** ≤30 cuts · ≥0.1 s each · afftdn nf=-25 · loudnorm I=-16 TP=-1.5 LRA=11 · crf 21 · default 480×854@24
- **الرخصة / license:** owner package (own work)
- **الدليل / proof:** `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/tools/video_edit.py` · `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/tests/test_v3_edit.py` · `owner-upload:KOSIF_SEE_ECC_Cinematic_v5/examples/Edited_Footage_Real.mp4`
