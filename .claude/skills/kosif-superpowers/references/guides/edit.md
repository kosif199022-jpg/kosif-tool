# المونتاج وإعادة بناء الفيديو المرجعي — Editing and reference-based edits

قراءة فيديو مرجعي (قطعات، ألوان، إيقاع) وإعادة بناء مونتاج قابل للتعديل بأصول المستخدم، وتخطيط لقطات حقيقية ورندرها، وبوابات الجودة، ومحرك المحاكاة، وجسر سير العمل للمنصات العالمية.

Reading a reference video (cuts, colour, rhythm) and rebuilding an editable edit with the user's assets; footage-first cut planning and B-roll rendering; quality gates; the mimic engine; global video platform workflow adapters.

Commands below are typed from the skill folder (`.claude/skills/kosif-superpowers/`) unless they say otherwise; `$SKILL_DIR` means that folder.

<!-- hub:area:edit:start -->

**الأدوات / tools (12)** — `python3 scripts/hub.py tool <id>` for every command, requirement and limit:

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
| `montage-pro` | A 13-role team over an uploaded audio or video: measures it (ffprobe, loudness, energy cues, cuts, contact sheet), offers an option menu with a stage plan, acquires licensed footage IDM-style (segmented resumable download, DASH/HLS grab, rights.json), conforms to an edit mezzanine with proxies, and builds a kinetic film, visualizer, reframe, highlight reel, look or a reference-remix Remotion project, each verified with verify_video.py; the master audio is never modified; its transcribe command writes word timings (kosif-words/1 words.json) locally with faster-whisper, skipping silence and refusing to write into jobs/ or tracked paths. | `python3 scripts/montage_pro.py doctor` | tested-here |
| `reel-factory` | A thin wrapper over existing tools: records the audio's declared rights and every shot's licence in rights.json (advisory, never blocking — gaps are listed and said once), takes words.json or runs montage_pro transcribe, plans one shot per phrase with xfades centred on the cuts (duration = audio + 1 s), builds a 4:5 footage plate with ffmpeg, renders a word-by-word Arabic scene (Aref Ruqaa / Reem Kufi, gold frame draw-on, handle and credit inside the safe zone, parametric styles) through tools/render_html.cjs, muxes the original audio with -c copy and gates the result with verify_video.py --source-audio. Outputs go to the git-ignored out/reels/<slug>. | `python3 scripts/reel_factory.py plan --audio ./voice.m4a --audio-rights owned --words ./words.json --shots-manifest ./stock/manifest.json --shot-ids 17928486,8165467,20382699 --title "دعاء يوم الخميس" --handle @kosif` | tested-here |

<!-- hub:area:edit:end -->

## الفهرس / contents

1. [KOSIF Reference Edit Engine — إعادة بناء المونتاج قابل للتعديل](#kosif-reference-edit-engine--إعادة-بناء-المونتاج-قابل-للتعديل)
2. [KOSIF Creative Quality Gate — اختبار صحة القرار قبل التصيير](#kosif-creative-quality-gate--اختبار-صحة-القرار-قبل-التصيير)
3. [قياس بصمة الفيديو المرجعي — Reference Visual Intelligence](#قياس-بصمة-الفيديو-المرجعي--reference-visual-intelligence)
4. [Mimic engine / محرك المحاكاة — rebuild a reference with new footage](#mimic-engine--محرك-المحاكاة--rebuild-a-reference-with-new-footage)
5. [REA-backed cinematic editor capability study and footage-first EDL (2026-10-19)](#rea-backed-cinematic-editor-capability-study-and-footage-first-edl-2026-10-19)
6. [Footage-first FFmpeg film rendering and REA-derived editor benchmark (2026-10-19)](#footage-first-ffmpeg-film-rendering-and-rea-derived-editor-benchmark-2026-10-19)
7. [Global Video Platform Intelligence / Video Workflow Bridge (2026-10-19)](#global-video-platform-intelligence--video-workflow-bridge-2026-10-19)

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
