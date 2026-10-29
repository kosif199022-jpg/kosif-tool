# المونتاج وإعادة بناء الفيديو المرجعي — Editing and reference-based edits

قراءة فيديو مرجعي (قطعات، ألوان، إيقاع) وإعادة بناء مونتاج قابل للتعديل بأصول المستخدم، وتخطيط لقطات حقيقية ورندرها، وبوابات الجودة، ومحرك المحاكاة، وجسر سير العمل للمنصات العالمية.

Reading a reference video (cuts, colour, rhythm) and rebuilding an editable edit with the user's assets; footage-first cut planning and B-roll rendering; quality gates; the mimic engine; global video platform workflow adapters.

Commands below are typed from the skill folder (`.claude/skills/kosif-superpowers/`) unless they say otherwise; `$SKILL_DIR` means that folder.

<!-- hub:area:edit:start -->

**الأدوات / tools (18)** — `python3 scripts/hub.py tool <id>` for every command, requirement and limit:

| tool | what it does | start with | evidence |
|---|---|---|---|
| `cinematic-broll-render` | Renders a real camera-motion B-roll video master with FFmpeg from a production-ready cinematic_cut_planner EDL and a licensed footage manifest (push-in, pull-back and pan per shot, exact frame counts), stream-copies the original audio and verifies frame count and audio bitstream hash. | `python3 scripts/cinematic_broll_render.py --edl ./edl.json --manifest ./clips.json --audio ./voice.wav --out ./out/master.mkv --width 1080 --height 1920` | tested-here |
| `cinematic-cut-planner` | Builds a deterministic JSON edit decision list (kosif.edl.v1) from word timings and a reviewed, licensed footage manifest: splits scenes at speech pauses of 0.6 s or more or once a scene reaches 7 s, picks the best tag-matching clip per scene, assigns camera moves and lists blockers instead of inventing footage. | `python3 scripts/cinematic_cut_planner.py --words ./words.json --clips ./clips.json --duration 48.5 --fps 30 --out ./out/edl.json` | tested-here |
| `creative-quality-gate` | Audits a KOSIF reference-edit plan.json (schema kosif.reference-edit.v1). It checks the fps/frame clock, gap-free and overlap-free shot frames, bounded pulse cues, that no aligned word crosses a hard cut, safe local media names (and, with an optional Remotion project, that those files exist), and honest evidence flags. It writes a new audit JSON whose status is structurally_verified_render_pending or blocked. | `python3 scripts/creative_quality_gate.py ./my-project/src/plan.json --out ./out/quality-audit.json` | tested-here |
| `mimic` | A Python engine that analyses a reference video (built for vertical reels) into spec.json: shots, transitions classified among 65 kinds with measured progress curves, animated Arabic text events with their style and font candidates, and the look (Lab grade, vignette, grain, letterbox, fades). It then rebuilds the same film from new replacement clips into one H.264 MP4 that copies the original audio stream untouched. | `python3 -c "import sys; sys.path.insert(0,'scripts/mimic'); import mm_analyze; mm_analyze.analyze('./in.mp4','./work')"` | tested-here |
| `motion-reference-probe` | Reads an authorized local video with ffprobe (duration, size, fps, audio presence) and optionally runs ffmpeg scene-change detection, producing a JSON timing report of cut candidates and segments that downstream KOSIF edit tools require. | `python3 scripts/motion_reference_probe.py ./in.mp4` | tested-here |
| `reference-edit-engine` | Turns a motion_reference_probe cut report (plus optional audio cues, visual fingerprint and owned replacement clips) into a new, unrendered, editable Remotion React project with frame-exact shots, word-safe cuts and a quality-gate audit. | `python3 scripts/reference_edit_engine.py --probe ./cuts.json --out ./new-edit` | tested-here |
| `reference-visual-fingerprint` | Decodes an authorized local video at 64x36 and 2 fps with ffmpeg and measures per-shot palette, luma, contrast, saturation, frame change and coarse translation candidates, writing a JSON fingerprint that reference_edit_engine can apply as new shot colors. | `python3 scripts/reference_visual_fingerprint.py ./in.mp4 --probe ./cuts.json --out ./reference-look.json` | tested-here |
| `video-workflow-bridge` | Generates deterministic, non-destructive JSON for two editor workflows: a text-based paper edit that turns selected word ranges into frame-bounded video-only segments, and frame-accurate review markers with timecodes and optional pixel anchors; it never reads, cuts or renders media. | `python3 scripts/video_workflow_bridge.py paper-edit templates/ik-wave-words.json --keep "1-3,5" --fps 30 --out ./out/paper-edit.json` | tested-here |
| `kosif-timeline` | Original non-destructive JSON timeline with trimmed sources, ordered video/image layers, per-clip alpha fades, independent audio mixing, reversible move/trim/fade edits, H264/AAC export via FFmpeg and FFprobe verification. | `python3 scripts/kosif_timeline.py doctor` | tested-here |
| `kosif-timeline-demo` | Generate fresh, synthetic H264 video, PCM WAV and PNG media, a complete editable 3-track timeline JSON and a verified 36-frame H264/AAC MP4 in a new folder. | `python3 scripts/kosif_timeline_demo.py --dir ./fresh-kosif-timeline-demo` | tested-here |
| `montage-pro` | A 13-role team over an uploaded audio or video: measures it (ffprobe, loudness, energy cues, cuts, contact sheet), offers an option menu with a stage plan, acquires licensed footage IDM-style (segmented resumable download, DASH/HLS grab, rights.json), conforms to an edit mezzanine with proxies, and builds a kinetic film, visualizer, reframe, highlight reel, look or a reference-remix Remotion project, each verified with verify_video.py; the master audio is never modified; its transcribe command writes word timings (kosif-words/1 words.json) locally with faster-whisper, skipping silence, re-running once without VAD the spans its silence filter dropped so sung or recited verses come back marked recovered, decoding with ffmpeg or PyAV, and refusing to write into jobs/ or tracked paths. | `python3 scripts/montage_pro.py doctor` | tested-here |
| `reel-factory` | A thin wrapper over existing tools: records the audio's declared rights and every shot's licence in rights.json (advisory, never blocking — gaps are listed and said once), takes words.json or runs montage_pro transcribe, plans one shot per phrase with xfades centred on the cuts (duration = audio + 1 s), builds a 4:5 footage plate with ffmpeg, renders a word-by-word Arabic scene (Aref Ruqaa / Reem Kufi, gold frame draw-on, handle and credit inside the safe zone, parametric styles) through tools/render_html.cjs, muxes the original audio with -c copy and gates the result with verify_video.py --source-audio. Outputs go to the git-ignored out/reels/<slug>. | `python3 scripts/reel_factory.py plan --audio ./voice.m4a --audio-rights owned --words ./words.json --shots-manifest ./stock/manifest.json --shot-ids 17928486,8165467,20382699 --title "دعاء يوم الخميس" --handle @kosif` | tested-here |
| `dua-wednesday` | Rebuilds the approved Wednesday-morning dua reel style on new footage and voice: one dua phrase per licensed shot cut just before the voice onset with nine different transitions (light leak, whip, gold ink reveal, zoom-through, gold iris, film burn, spin zoom, bokeh, slide), word-by-word Arabic text timed with faster-whisper and audio energy with a gold karaoke highlight, a gold Ruqaa day title under a drawn-on mihrab crowned by a crescent, golden dust, god rays, bloom, warm grade and grain. The voice is stream-copied and checked byte for byte. | `python3 scripts/dua_wednesday.py doctor` | tested-here |
| `look-pipeline` | Written after a read-only study of the Montaji Arabic video editor: eleven colour looks (natural, vivid, bright, warm, cool, cinematic, vintage, faded, dramatic, mono, night-dua) and eight parameters become one per-channel affine step plus one 3x3 matrix, emitted with the same numbers as an ffmpeg chain (lutrgb + colorchannelmixer + vignette), an SVG filter, CSS and a GLSL shader. verify pushes a test frame through ffmpeg and compares every pixel with the reference maths; apply grades a video into a new file. | `python3 scripts/look_pipeline.py presets` | tested-here |
| `fast-edit` | Single-file FFmpeg operations with JSON receipts: lists keyframes; cuts by stream copy when the start sits on (or within a tolerance of) a keyframe and by exact re-encode otherwise, reporting how far a copy would have drifted; applies voice presets (chipmunk, deep, robot, echo, radio, telephone) at the file's real sample rate with the length kept and video stream-copied; lifts low-light video with an optional denoise and measures mean luma before and after, skipping clips that are already bright; extracts audio bit-exact when the container allows it. | `python3 scripts/fast_edit.py doctor` | tested-here |
| `nle-export` | Turns a kosif.timeline.v1 project or a kosif.edl.v1 cut plan into editable timelines that point at the original media: FCPXML 1.9 (Final Cut Pro, Resolve) with opacity keyframes, audio fades and position/size, FCP7 XML v5 (Premiere Pro, Resolve) with fades as dip-to-black transitions, one CMX3600 EDL per track, OpenTimelineIO JSON (Resolve 18.5+), a Blender Video Sequencer script with fades and layout, SRT captions from words.json and a numbered CapCut cut list. Integer and NTSC rates (23.976, 29.97, 59.94) are exact; times snap to frames with the largest drift reported, and a receipt lists SHA-256 per file and what each format could not carry. | `python3 scripts/nle_export.py export --project ./project.json --out ./nle --formats all --words ./words.json` | tested-here |
| `cinema-lab` | Cinematography and editing engines rebuilt in our own code from ideas in PySceneDetect, Auto-Editor, OpenTimelineIO, OpenColorIO, OpenCV, vid.stab, Motion Canvas/Remotion and OpenRV, running on FFmpeg + NumPy in a cloud sandbox. Detects scene cuts (FFmpeg scdet, or the real PySceneDetect ContentDetector when installed) with a storyboard contact sheet; removes silences with frame-grid cuts that keep audio and video in sync; exports any segment plan as OpenTimelineIO JSON (read back with the opentimelineio package when present) and a CMX3600 EDL for Kdenlive/Shotcut/Resolve/Premiere; builds portable 33^3 .cube looks and applies them with lut3d; stabilises with two-pass vid.stab and measures shake before/after by phase correlation; reframes landscape footage to a 1080x1920 portrait crop by tracking motion and detail with a smoothed, speed-capped virtual camera that re-aims at scene cuts; renders eased push-in/pan/tilt/ken-burns camera moves on stills or clips; and makes A/B side-by-side or wipe review videos with burnt-in timecode and SSIM/PSNR. | `python3 scripts/cinema_lab.py doctor` | tested-here |
| `script-storyboard` | Reads an Arabic or English play or screenplay (text or PDF) and writes a kosif.storyboard.v1 shot list: acts, scenes, an establishing wide shot per scene, dialogue shots that change size on a speaker change or emotional cue, stage directions, word-count durations, characters with line counts, likely duplicate spellings of a name, pacing per act and short-form episodes under a time limit. It then renders a frame-exact animatic MP4 from colour cards or the user's own images and clips, with an optional master audio track, at the KOSIF export standard. | `python3 scripts/script_storyboard.py parse ./script.pdf --first-page 8 --last-page 60 --out ./out/storyboard.json --episode-seconds 90` | tested-here |

<!-- hub:area:edit:end -->

## الفهرس / contents

1. [KOSIF Reference Edit Engine — إعادة بناء المونتاج قابل للتعديل](#kosif-reference-edit-engine--إعادة-بناء-المونتاج-قابل-للتعديل)
2. [KOSIF Creative Quality Gate — اختبار صحة القرار قبل التصيير](#kosif-creative-quality-gate--اختبار-صحة-القرار-قبل-التصيير)
3. [قياس بصمة الفيديو المرجعي — Reference Visual Intelligence](#قياس-بصمة-الفيديو-المرجعي--reference-visual-intelligence)
4. [Mimic engine / محرك المحاكاة — rebuild a reference with new footage](#mimic-engine--محرك-المحاكاة--rebuild-a-reference-with-new-footage)
5. [REA-backed cinematic editor capability study and footage-first EDL (2026-10-19)](#rea-backed-cinematic-editor-capability-study-and-footage-first-edl-2026-10-19)
6. [Footage-first FFmpeg film rendering and REA-derived editor benchmark (2026-10-19)](#footage-first-ffmpeg-film-rendering-and-rea-derived-editor-benchmark-2026-10-19)
7. [Global Video Platform Intelligence / Video Workflow Bridge (2026-10-19)](#global-video-platform-intelligence--video-workflow-bridge-2026-10-19)
8. [دعاء يوم الأربعاء — Wednesday-morning dua reel (2026-10-21)](#دعاء-يوم-الأربعاء--wednesday-morning-dua-reel-2026-10-21)
9. [التعديل السريع — Fast Edit: honest instant cut, voice presets, low-light lift (2026-10-23)](#التعديل-السريع--fast-edit-honest-instant-cut-voice-presets-low-light-lift-2026-10-23)
10. [من السيناريو إلى الستوري بورد — Script to storyboard and animatic (2026-10-25)](#من-السيناريو-إلى-الستوري-بورد--script-to-storyboard-and-animatic-2026-10-25)
11. [معمل السينما — Cinema Lab: 24 film repositories turned into runnable engines (2026-10-25)](#معمل-السينما--cinema-lab-24-film-repositories-turned-into-runnable-engines-2026-10-25)
12. [التسليم لبرامج المونتاج — NLE Export: DaVinci, Final Cut, Premiere, Blender, CapCut (2026-10-28)](#التسليم-لبرامج-المونتاج--nle-export-davinci-final-cut-premiere-blender-capcut-2026-10-28)
13. [التفريغ للتلاوة والأناشيد — Transcribing recited or sung audio (2026-10-29)](#التفريغ-للتلاوة-والأناشيد--transcribing-recited-or-sung-audio-2026-10-29)

**Katana analysis-only policy:** إذا طلب المستخدم تحليل صور/مقاطع أو مرجع مونتاج، طبّق [سياسة Katana في A8](../protocol/A8-motion-brain.md#katana--higgsfield--سياسة-التحليل-فقط-وحفظ-الرصيد): النتيجة ردود وتحليل نصي، وليس إعادة إنشاء/إخراج صور أو فيديو عبر Katana، ولا استخدام أرصدة توليد Higgsfield. لا تفترض أن Katana لديها واجهة تحليل read-only؛ عند عدم إثباتها استخدم أدوات فحص KOSIF/FFmpeg أو الرؤية مباشرة مع تمييز المصدر.

## KOSIF Reference Edit Engine — إعادة بناء المونتاج قابل للتعديل

عندما يطلب المستخدم محاكاة **طريقة مونتاج فيديو مرجعي** أو Kit شبيه بفكرة Katana، افتح [قدرة إعادة بناء المونتاج التنفيذية](../reference-edit-execution.md)، ولا تكتفِ بعرض المستودعات. المحرك الجديد يستخرج من تقرير FFmpeg توقيت القطعات، ويحوّلها إلى لقطات بإطارات دقيقة ومشروع Remotion بملفات React أصلية، ويتيح نسخ **لقطات المالك فقط** من Manifest محمي. يدعم إيقاع الصوت وتوقيت الكلمات المراجع، دون اختلاق تفسير للأغنية.

    python3 $SKILL_DIR/scripts/motion_reference_probe.py ./reference.mp4 --cuts --out ./cuts.json
    python3 $SKILL_DIR/scripts/reference_edit_engine.py --probe ./cuts.json --cues ./cues.json --fps 30 --out ./remotion-project
    python3 -m unittest discover -s $SKILL_DIR/evals -p test_reference_edit_engine.py -v

بعد التوليد: راجع خطة التحرير والحقوق وترخيص Remotion، ثم شغّل npm install / npm run studio / npm run render داخل مجلد المشروع، وتحقق من الفيلم بنفسك. النتائج المقاسة هنا: **توقيت المرشّحات وخطة قطع، لا استخراج Motion Vectors، ولا تشغيل Katana الأصلية، ولا إثبات جودة MP4 بدون الرندر**. أي أدوات SAM2 أو CoTracker أو Higgsfield خدمة منفصلة تُفعّل بإذن وتكلفة وترخيص واضح.

## KOSIF Creative Quality Gate — اختبار صحة القرار قبل التصيير

عندما تولّد خطة مونتاج أو تختار توقيت القطعات، استدعِ [محرك مراقبة الجودة والتفكير](../creative-quality-gates.md). **كود التنفيذ**: scripts/creative_quality_gate.py؛ يفحص صراحةً اتصال إطارات المشاهد بلا فجوات، وعدم فصل كلمات حقيقية موثّقة زمنيًا، وصحة مراجع الملفات البديلة، وصدق تقرير الإثبات. يستدعيه reference_edit_engine.py تلقائيًا، فيمنع تصدير مشروع خاطئ ويولّد quality-audit.json إلى جانب مصادر Remotion.

    python3 $SKILL_DIR/scripts/creative_quality_gate.py ./my-project/src/plan.json --project-dir ./my-project --out ./my-quality-report.json
    python3 -m unittest discover -s $SKILL_DIR/evals -p test_creative_quality_gate.py -v

اجتياز البوابات البنيوية لا يساوي فحصًا فنيًا أو نجاح MP4، ولا يعني أنه تم فهم مشاعر الأغنية. الأداء/المعنى/الحقوق/جودة العرض تتطلب اختبارًا مستقلاً وقرار المستخدم.

## قياس بصمة الفيديو المرجعي — Reference Visual Intelligence

لو المستخدم طلب **فهم ألوان وإضاءة ومونتاج فيديو مرجعي أو نقل خصائصه إلى مشاهد جديدة**، شغّل أدوات [دليل البصمة البصرية التنفيذي](../reference-visual-transfer.md). لا تعُد إلى مجرد روابط Katana أو SAM 2. هذه قدرة KOSIF أصلية لتوليد بيانات مقاسة من فيديو محلي مصرح به، مع فحص التراخيص والصلاحيات.

    python3 $SKILL_DIR/scripts/motion_reference_probe.py ./reference.mp4 --cuts --out ./cuts.json
    python3 $SKILL_DIR/scripts/reference_visual_fingerprint.py ./reference.mp4 --probe ./cuts.json --out ./visual.json
    python3 $SKILL_DIR/scripts/reference_edit_engine.py --probe ./cuts.json --visual ./visual.json --out ./new-remotion

النتيجة تقرير يقيس لقطات مصغرة 64×36 بمعدل 2 إطار/ثانية وبصمة الإضاءة والألوان والتغيرات المرئية، ثم مشروع Remotion جديد بألوان مشاهد مستقاة من القياسات. لا ينسخ صور المرجع ولا الصوت؛ ولا يصنّف حركة الكاميرا تصنيفًا مؤكدًا أو يفهم القصة دون تحليل إضافي. يتحقق من مصدر الفيديو ومدة التقرير وقيم الألوان قبل أي إنتاج. **أداة داخل المهارة ≠ ffmpeg مثبت ≠ فيديو مُنتج ومُراجع**. ثبّت أي تبعيات خارجية بموافقة، ولا تعتبر كود Katana الملكي متاحًا لمجرد وجود Higgsfield Skills.

## Mimic engine / محرك المحاكاة — rebuild a reference with new footage

- When the user wants "this video but with my clips", read [mimic.md](../mimic.md) and run `scripts/mimic/` (analyse → review `analysis.md` and sheets → set replacement clips → build → verify). The original audio is copied, never re-encoded; text, timing, transitions and look are measured, not guessed.
- Prove the analyser on the synthetic ground truth first (`scripts/mimic/synthetic/run_synthetic.py`, proof in `proofs/mimic-synthetic/`, test `tests/test_mimic.py`); footage comes from the user or licensed sources only, no platform scraping; `mm_transitions.py` is LGPL-2.1-or-later (FFmpeg xfade port).

## REA-backed cinematic editor capability study and footage-first EDL (2026-10-19)

For user requests involving video editors, animation apps, online motion-design services, or application feature discovery, consult [REA editor capability study](../../../../../docs/REA_FILM_EDIT_CAPABILITY_STUDY_20261019.md). This study distinguishes REA static artifact evidence from official product capability descriptions and from KOSIF implementations. It documents inspection limitations and prioritizes original, compatible implementations; it is **not** authority to launch untrusted installers, copy commercial code, defeat licenses, or capture unauthorized app traffic.

For tasks with original word-aligned audio and a reviewed real-footage manifest, use the **original footage-first edit decision planner** `scripts/cinematic_cut_planner.py` to produce a timecoded 9:16 shot plan, mandatory provenance gates, word cue markers and deterministic camera metadata. Execute `python scripts/cinematic_cut_planner.py --help` for its exact CLI. This is a **planner only**, not a downloader, detector, or renderer. It fails closed when assets are unlicensed, missing review flags, or insufficient in duration. Connect to the existing media-download, audio, text, rendering and verification playbooks to produce any final MP4.

REA CLI v6.7.0 was successfully invoked on Windows, but an REA MCP registration with Claude Code was **not verified**. Distinguish these states. Consult the studio's original first-party code and published vendor docs for feature design; do not import copyrighted editor binaries or proprietary implementation details.

## Footage-first FFmpeg film rendering and REA-derived editor benchmark (2026-10-19)

For a film request with immutable original audio and approved real footage, read [KOSIF deep editor study](../../../../../docs/KOSIF_MEDIA_EDITOR_DEEP_RESEARCH_20261019.md) and use `scripts/cinematic_cut_planner.py` to produce the EDL, followed by **`scripts/cinematic_broll_render.py`** to produce an actual camera-animated, frame-verified B-roll video with original audio stream copied unchanged into a compatible container. The render program requires a local asset manifest with independently verified footage licenses, frame review, SHA256 hashes, and a complete contiguous EDL; it refuses missing or mismatched sources and will not overwrite an output. Test with `python -m unittest discover -s tests -p test_cinematic_broll_render.py -v` in the repository root.

This is a **real intermediate video render**, not yet a final motion-graphics film: word-synced Arabic kinetic captions, advanced compositing, source acquisition and final social loudness export require separate verified modules. Do not claim those are implemented by this component. Reference editors provide feature ideas only; do not import proprietary code/assets.

## Global Video Platform Intelligence / Video Workflow Bridge (2026-10-19)

For requests to compare major editing services (Premiere, CapCut, Resolve, Descript, Kapwing, Runway, Frame.io, VEED, OpusClip, HeyGen, Canva, Higgsfield) or transfer editor capabilities, read [the source-backed global platform matrix](../global-video-platforms-2026-10-19.md) first, then the existing [APPX investigation records](../app-feature-transfer.md). Do not mistake public product claims or a bootstrapper for observed application behavior. Do not launch third-party installers, cracked applications or unknown patchers.

Two new clean-room local adapters support actual production work: scripts/video_workflow_bridge.py paper-edit words.json --keep "1-3,7-9" --fps 30 --out paper-edit.json creates frame-aligned VIDEO-ONLY edit decisions, while scripts/video_workflow_bridge.py review notes.json --duration 60 --fps 30 --out review-markers.json generates stable, frame-accurate spatial review notes. Both are deterministic JSON workflows, NOT licensed vendor AI/editor engines. Run python -m unittest discover -s evals -p test_video_workflow_bridge.py -v; raise status to verified only after a successful run.

For documentary/audio-master requests, NEVER apply paper-edit decisions to the original narration: preserve its source bytes/stream and fit captions and visual cuts to existing word timing. Frame-review notes can be used without touching the sound. Run REA via its verified CLI or an explicitly configured provider; REA doctor failures for optional native engines do not prevent static artifact inspection.

## دعاء يوم الأربعاء — Wednesday-morning dua reel (2026-10-21)

When the owner sends a dua video or voice and asks for «نفس استايل دعاء يوم الأربعاء» (the same Wednesday dua style), use
`dua-wednesday`: read [dua-wednesday/WORKFLOW.md](../../dua-wednesday/WORKFLOW.md) first, then `fetch` → `asr` → `init` →
licensed clips → `prep` → `sprites` → `stills` (review) → `render`. Keep the fixed idea (one phrase = one shot, a different
transition per cut, word-by-word gold karaoke text, mihrab + crescent, untouched voice, no star ornament); change the
footage, text, day title and dates, and add new animation on top only through `Engine.transition` or a new draw function.

## One colour look for preview and export

`look_pipeline.py` keeps a grade as numbers (a per-channel affine step, then a 3×3 matrix) and writes the same numbers for ffmpeg, an SVG/CSS filter and a GLSL shader, so a browser preview and the exported MP4 agree. `verify` measures that agreement on a test frame instead of assuming it.

    python3 $SKILL_DIR/scripts/look_pipeline.py build --preset cinematic --amount 0.8 --target svg
    python3 $SKILL_DIR/scripts/look_pipeline.py verify --all
    python3 $SKILL_DIR/scripts/look_pipeline.py apply ./in.mp4 ./graded.mp4 --preset warm

Background: [montaji.md](../app-studies/montaji.md).

## من السيناريو إلى الستوري بورد — Script to storyboard and animatic (2026-10-25)

لما يبعت المالك مسرحية أو سيناريو (نص أو PDF) ويطلب تقطيعه لقطات أو حلقات ريلز، استخدم `script-storyboard`. يقرأ الفصول والمشاهد والحوار بصيغة «الاسم: الجملة» و«الاسم (إرشاد): الجملة»، ويقترح حجم كل لقطة ومدتها، ويقسم العمل لحلقات تحت حد زمني، وينبهك لو اسم شخصية مكتوب بطريقتين.

When the owner sends a play or screenplay and wants it broken into shots or short-form episodes, `parse` it first, read the `warnings` (two spellings of one name) and `pacing.episodes`, fill each shot's `source` with the user's own images or clips where they exist, then `render` one episode at a time against the voice track. The animatic is for timing review only; the final film goes through Montage Pro or the motion runtime.

    python3 $SKILL_DIR/scripts/script_storyboard.py parse ./play.pdf --first-page 8 --last-page 60 --out ./out/storyboard.json --episode-seconds 90
    python3 $SKILL_DIR/scripts/script_storyboard.py render --storyboard ./out/storyboard.json --episode 1 --audio ./voice.m4a --out ./out/ep1.mp4

Ported from the owner's KOSIF Cinematic Toolkit (storyboard + master-audio render) and extended with the script parser, frame-exact cuts and the export standard. Do not commit the text of copyrighted scripts or books as fixtures; tests use original sample lines.

## معمل السينما — Cinema Lab: 24 film repositories turned into runnable engines (2026-10-25)

The owner sent 24 well-known open-source film, editing and VFX projects and asked to use them. `cinema_lab.py` keeps what runs in a cloud sandbox and rebuilds each idea in our own code on FFmpeg + NumPy; the real library is used only when it is installed (`scenedetect`, `opentimelineio`). Delivery settings come from `export_profile.py` ([export standard](../../../../../playbooks/export-standard.md)): 1080x1920 for vertical outputs, 30 fps, H.264 High CRF 17 preset slow, yuv420p, BT.709, `+faststart`, the audio copied whenever timing is unchanged and AAC 320k/48 kHz only when a cut forces a re-encode. `grade` is a creative look for when one is asked for; the standard's default stays colour matched to the source. Every command prints a `kosif.cinema_lab.receipt.v1` receipt with measurements.

    python3 $SKILL_DIR/scripts/cinema_lab.py doctor
    python3 $SKILL_DIR/scripts/cinema_lab.py scenes --input ./film.mp4 --out ./scenes --sheet --timeline
    python3 $SKILL_DIR/scripts/cinema_lab.py silence-cut --input ./talk.mp4 --output ./tight.mp4 --timeline
    python3 $SKILL_DIR/scripts/cinema_lab.py grade --input ./clip.mp4 --output ./graded.mp4 --look teal-orange --cube-out ./teal.cube
    python3 $SKILL_DIR/scripts/cinema_lab.py stabilize --input ./shaky.mp4 --output ./steady.mp4
    python3 $SKILL_DIR/scripts/cinema_lab.py reframe --input ./wide.mp4 --output ./reel.mp4
    python3 $SKILL_DIR/scripts/cinema_lab.py camera --input ./photo.jpg --output ./push.mp4 --move push-in
    python3 $SKILL_DIR/scripts/cinema_lab.py review --a ./before.mp4 --b ./after.mp4 --output ./ab.mp4 --mode wipe --metrics

A good chain for a reel from a wide film: `scenes --sheet` (look at the storyboard first) → `reframe` (the camera re-aims at each cut instead of panning across it) → `grade` → `review --mode wipe --metrics` against the ungraded reframe → `verify_video.py`.

| repository | what we took | where |
|---|---|---|
| PySceneDetect | content-difference cut detection, minimum scene length, real ContentDetector when installed | `scenes` |
| Storyboarder | one frame per shot with its time range as a storyboard sheet | `scenes --sheet` |
| Auto-Editor | silence → keep speech with a margin → one clean render | `silence-cut` (cuts snapped to the frame grid so A/V stay in sync) |
| OpenTimelineIO | the interchange timeline, written without the package and read back with it when present | `timeline`, `--timeline` |
| Kdenlive, Shotcut | they import the CMX3600 EDL and OTIO we write, so a cut can be finished by hand | `.edl`, `.otio` |
| LosslessCut | keyframe-aware stream-copy cutting | already in `fast_edit.py cut` |
| FFmpeg | the engine under every command (scdet, silencedetect, lut3d, vid.stab, zoompan, sendcmd, ssim/psnr) | all |
| OpenColorIO | looks as portable 3D LUTs (.cube) that OCIO, Resolve, Natron and Kdenlive read | `grade` |
| OpenCV | motion and detail tracking for a virtual camera operator, phase-correlation shake measurement | `reframe`, `stabilize` |
| Motion Canvas, Remotion | the camera as code: eased push-in, pan, tilt, ken-burns | `camera`; React/HTML scenes stay in `render_html.cjs` and the Remotion starters |
| OpenRV | shot review: A/B side-by-side or wipe, burnt-in timecode, SSIM/PSNR | `review` |
| Blender | already bridged (`blender_cinema.py`, `blender_motion_video.py`, `native_3d.py`) | — |
| Natron | node compositing stays outside; it reads our .cube looks and EDL | — |
| Nerfstudio, COLMAP | need a GPU and many photos of a real place; not practical in a CPU sandbox, run them on the owner's machine | — |
| libgphoto2, OBS Studio | drive a physical camera or capture a screen; they need the owner's device, not a cloud session | — |

Honest limits: scene detection is a difference score (soft dissolves can be missed, so look at the storyboard); silence cut works on loudness, not words, and re-encodes audio; reframe follows motion and detail, not faces; the looks are hand-built LUTs, not a calibrated ACES pipeline; stabilise cannot remove motion blur or rolling shutter; camera moves are 2D crops, not 3D parallax.

## التسليم لبرامج المونتاج — NLE Export: DaVinci, Final Cut, Premiere, Blender, CapCut (2026-10-28)

لما المستخدم يحب يكمّل المونتاج بإيده في برنامجه، متسلّمش MP4 بس: سلّم التايملاين نفسه. `scripts/nle_export.py` بياخد مشروع `kosif.timeline.v1` (من `kosif_timeline.py`) أو خطة قطع `kosif.edl.v1` (من `cinematic_cut_planner.py`) ويكتب ملفات بتشاور على الميديا الأصلية من غير نسخ ولا إعادة ترميز.

When the user wants to keep editing by hand, hand over the timeline, not only the MP4 (for a single segment plan as OTIO JSON or one EDL, `cinema_lab.py` already does it; this tool carries a full multitrack project):

```bash
python3 scripts/nle_export.py export --project ./project.json --out ./nle --formats all --words ./words.json
python3 scripts/nle_export.py export --project ./edit_plan.json --audio ./voice.wav --out ./nle   # from a cut plan
```

| editor | file | open with |
|---|---|---|
| DaVinci Resolve | `.fcpxml`, `.premiere.xml`, `.otio` (18.5+) or `.edl` | File → Import → Timeline |
| Final Cut Pro | `.fcpxml` (version 1.9) | File → Import → XML |
| Premiere Pro | `.premiere.xml` (FCP7 XML v5) or `.edl` | File → Import |
| Blender | `.blender_vse.py` | `blender --background --python X.blender_vse.py -- --save X.blend` |
| CapCut | `.capcut.md` + `.srt` | no timeline import exists; rebuild from the numbered list |

What travels everywhere: cuts, trims (source in/out), track order (video layers as lanes/tracks, audio below), per-clip volume, and video clips with or without their own sound. Fades: Blender (keyframed `blend_alpha`/`volume`), FCPXML (opacity keyframes in clip-local time and audio `fadeIn`/`fadeOut`) and the Premiere XML (Cross Dissolve / Cross Fade to and from black). Position/size: Blender and FCPXML (`adjust-conform none` + `adjust-transform`, position in percent of the frame height with the origin at the centre). EDL and OTIO carry cuts only; OTIO keeps fades and layout as metadata and splits overlapping clips onto extra tracks. `HANDOFF.md` lists what to redo by hand per editor. Rates: integers plus 23.976, 29.97, 47.952, 59.94 and 119.88 as exact rationals (`1001/30000s`, `<ntsc>TRUE`, Blender `fps_base` 1.001), non-drop timecode. Times snap to whole frames and `receipt.json` reports the largest drift, a SHA-256 per file and every warning.

Verification on this checkout: the tests parse each format, check frame maths, and, when OpenTimelineIO is installed, read the FCPXML, FCP7 XML, EDL and OTIO back through its independent adapters (including the Premiere dissolves and a 29.97 fps export); with `bpy` installed they build the sequencer in real Blender. Say plainly that the files were not opened in the commercial editors here.

## التفريغ للتلاوة والأناشيد — Transcribing recited or sung audio (2026-10-29)

Recited or sung passages over music score a high `no_speech_prob`, so `montage_pro.py transcribe` used to drop them as "silence/music": they appeared only in `dropped_segments`, with no word timings, and verse timing had to be redone by hand with `vad_filter=False`. In six earlier jobs (24–28 Oct) all 29 dropped segments were verse or lyric lines, 15 of them from a `--no-vad` run. Now each dropped span is re-run once **without VAD and without the previous text**, and its confident words are merged back marked `"recovered": true` (on each word, on the phrase and on its `dropped_segments` entry). The file's `recovery.windows` lists every span: re-run, skipped as silent, or rejected and why.

    python3 $SKILL_DIR/scripts/montage_pro.py transcribe ./verse.m4a --job ../../../out/job1 --language ar --local-only   # recovery on (default)
    python3 $SKILL_DIR/scripts/montage_pro.py transcribe ./verse.m4a --job ../../../out/job1 --no-recover                  # the old output
    python3 $SKILL_DIR/scripts/montage_pro.py transcribe ./song.m4a --job ../../../out/job1 --no-vad                       # whole file: no VAD, no conditioning

- **What comes back:** a re-run segment whose text is not one of the phrases models invent (the `caption_lines.py` list: subscribe outros, subtitle credits, sound tags, punctuation only), with `avg_logprob` ≥ −1 and `compression_ratio` ≤ 2.4 (Whisper's own bars). Its `no_speech_prob` is recorded, not gated, because that is what dropped the span. A span quieter than −50 dBFS RMS is silence and is not re-run. Punctuation-only tokens (a "-" left from a verse number) are left out, and recovered words never overlap or shorten a kept word.
- **`--no-vad`** decodes the whole file with `vad_filter=False` and `condition_on_previous_text=False`. That already is the re-run's setting, so its dropped segments are re-checked against the same bars without a second model call. `--no-speech-threshold 1` keeps every segment unchecked.
- **VAD gaps:** Silero VAD can also cut sung lines before the model hears them, and those never reach `dropped_segments`. Loud stretches of 2 s or more with no word are listed in `vad_gaps` (start, end, RMS level) with a warning to try `--no-vad`. Nothing is re-run there, because keeping music beds away from the model is what VAD is for. **For songs and recitation over music, start with `--no-vad`.**
- **Decoding:** ffmpeg turns the audio into a 16 kHz mono array; when ffmpeg is missing or fails, PyAV is opened directly. faster-whisper 1.2.1's own `decode_audio` passes `metadata_errors`, which av 19 rejects (`TypeError: open() got an unexpected keyword argument 'metadata_errors'`), and that is also what happens when `WhisperModel.transcribe` is given a file path, so the model only ever gets an array. `engine.decoder` says which decoder ran.
- **Older files:** a words.json written before these fields is still "up to date" when it dropped nothing (its words would not change; `--force` measures `vad_gaps` for it); one that dropped segments, or an old `--no-vad` file (which was decoded with the previous text), is redone.

Measured here (medium, int8, 4 CPU cores, `--local-only`): on the 63 s recitation from 28 Oct the first pass kept 14 words and dropped two verses (`no_speech_prob` 0.94 and 0.967); with recovery the file has 49 words, 35 of them recovered in two phrases (`avg_logprob` −0.149 and −0.219), the kept words untouched, in 34–79 s per run including the model load; two runs gave byte-identical files and the next was "up to date" in 0.05 s. `vad_gaps` flagged one 2.6 s stretch (42.64–45.2 s) where `--no-vad` finds the first syllables of the third verse. On the 60 s sung track from 24 Oct, the old `--no-vad` (still decoded with the previous text) kept 30 words and dropped 15 lyric lines; today's `--no-vad` drops nothing and keeps 78 words, while the default VAD run keeps 62 and reports `vad_gaps` 3 (21.1 s: the lines VAD cut). Over 12 s of digital silence and of pink noise at −36 dBFS, medium without VAD wrote «اشتركوا في القناة» (`avg_logprob` −0.72 and −0.62): the phrase list rejects it, and the silence is not even re-run. Not measured: word-timing accuracy against a reference, and whether a recovered word is right. Check recovered phrases before they become captions (`caption_lines.py` screens the invented phrases again). On the same 79.6 s song, model and version, the first pass dropped three lyric segments on 26 Oct and none today, so first-pass results can differ between sessions.
