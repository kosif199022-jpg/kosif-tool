# Global video platforms -> original KOSIF capabilities (2026-10-19)

Status: evidence-based feature comparison and two **executable local workflow adapters**. This is NOT a copy of any proprietary application. Public vendor documentation supports feature descriptions; static REA on local installers supports only artifact-level observations. Product websites are NOT evidence that an equivalent KOSIF implementation exists.

## Source-backed capability and gap matrix

| Platform | Verified feature from the vendor | KOSIF action and status | Limitations |
|---|---|---|---|
| Adobe Premiere | Text-Based Editing, clip search, ripple/roll/slip/slide, multicam, Generative Extend | APPX-04 scene edits, APPX-15 EDL already verified locally; NEW non-destructive word-based paper edit manifest, executable with tests | The new manifest is NOT Premiere's editor. Generative Extend requires licensed Adobe cloud tools; not integrated |
| CapCut | Automatic captions, creator video editing | APPX-01 speed curves, APPX-02 keying, APPX-03 reframe, APPX-13 captions already exist | Real CapCut editor absent from bootstrapper; no proprietary model copied |
| Blackmagic DaVinci Resolve | Fusion node-based motion graphics, Resolve Edit and Fairlight sound workflows | Local KOSIF FFmpeg/SVG/Remotion composition is available or installable as separately probed; a Fusion-compatible node editor is only a design target | No built-in Resolve engine or proprietary Neural Engine |
| Descript | Text-based edits, filler removal, Studio Sound, transcripts, captions | NEW word-boundary video paper-edit manifest; APPX-07 pause removal and APPX-12 classical noise reduction existing | No speech regeneration or Descript AI model. Never paper-edit the untouched narration of a documentary |
| Kapwing | Smart Cut, auto subtitles, resize for social platforms, collaborative editor | APPX-07 pauses, APPX-03 auto reframe, APPX-13 captions existing | Live collaboration and cloud workspace not implemented |
| Runway | Timeline Studio, Edit Studio, visual editing Apps and Workflows | KOSIF can storyboard and export; Runway generation/editing requires an authorized external service | IMPORTANT: old Video Editor retired 2026-07-30; legacy Inpainting/Motion Tracking guides are NOT current APIs |
| Frame.io | Frame-accurate feedback, pinned spatial comments, project review | NEW frame-accurate review annotations tool, executable with tests | Local JSON markers only, not Frame.io's online collaboration, approval workflow, or synced projects |
| VEED | Subtitle generation and browser-based editing | Existing caption and platform exports; validate Arabic name spelling manually | Cloud subtitle APIs, subscriptions and translation not integrated |
| OpusClip | Prompt-driven highlight identification (ClipAnything) | Documentary hero beats and captions can be assembled locally; semantic highlight ranking is documented only | Requires separately tested model, licensed media and evaluation dataset |
| HeyGen | Video translation with synchronized lip movement | Translation/lip sync documented as a possible optional paid integration | No HeyGen keys or model execution verified |
| Canva | Templates, background removal, resizing, print layouts, animation | APPX-88 through APPX-98 are existing original KOSIF App Studio recipes, with tests | No Canva hosted editor, proprietary generative model or shared design library |
| Higgsfield | AI-directed cinematic video generation and camera motion | Store production-safe prompts and compatible SDK routes only when version, access and expense are verified | Cannot claim Higgsfield paid models are locally installed |

Primary public sources, consulted 2026-10-19:
- Premiere: https://www.adobe.com/products/premiere/features.html
- Adobe Generative Extend: https://helpx.adobe.com/premiere/desktop/edit-projects/edit-with-generative-ai/generative-extend-overview.html
- CapCut: https://www.capcut.com/tools/auto-caption-generator
- DaVinci Resolve: https://www.blackmagicdesign.com/sa/products/davinciresolve/whatsnew
- Descript: https://www.descript.com/video-editing
- Kapwing: https://www.kapwing.com/start
- Runway retirement and replacements: https://help.runwayml.com/hc/en-us/articles/19155664495379-Inpainting
- Runway deprecated features: https://help.runwayml.com/hc/en-us/articles/40213860628371-Deprecated-Standalone-Tools
- Frame.io: https://help.frame.io/en/articles/9105251-commenting-on-your-media
- VEED: https://www.veed.io/tools/auto-subtitle-generator-online
- OpusClip: https://www.opus.pro/clipanything
- HeyGen: https://www.heygen.com/translate
- Canva: https://www.canva.com/
- Higgsfield: https://higgsfield.ai/

## What was observed on the authorized laptop

The owner's Desktop/تجربة contains a KOSIF repo, Adobe Premiere bootstrapper, CapCut bootstrapper, Canva installer, and multiple commercial image/design/motion tool archives. Many archives have third-party distribution names, some have crack/patch/keygen components. Do NOT run executables, activate installers, use keygens, break encryption or copy proprietary code.

Existing KOSIF evidence (before this change):
- proofs/windows-installers-rea/README.md: initial Canva, CapCut, Premiere analysis.
- proofs/windows-installers-rea/BATCH_2026-10-19.md: DxO, Capture One, JPEGmini, FontLab, Affinity, Houdini, IDM, Adobe Animate; 24 historical REA runs, 17 evidence IDs, no installers executed.
- proofs/windows-installers-rea/CANVA_DESIGN_2026-10-19.md: app.asar anchors used to build clean-room App Studio capabilities.

Newly verified in this session on Windows 11:
- Node.js 24.21.0 and REA CLI 6.7.0 installed; npm install completed successfully.
- REA inspect-artifact on the 3.37 MB Adobe setup: evidence ID ev_596c50fba174b091b0f07f19ba511805b8aea61e20843f8932d6d63ab184ee7f, SHA-256 25565eeb1cca35eb873b3ac939b79d3535f8ede1049b049b1e8a271762f63297.
- REA observed ONE PE root artifact with NO child entries. KOSIF triage identified UPX sections and Adobe Installer 2.14.0.43, NOT Premiere's editing capabilities.
- REA doctor says Node and host healthy; Hopper, Ghidra, IDA and other native providers unconfigured. Native pseudocode analysis therefore unavailable here.
- REA setup completed for **Claude Code only**: its MCP registration was added while preserving unrelated configuration, and upstream REA skill version 42 was installed. The setup doctor reports the Claude Code scope as healthy, but the active Claude Code session must be restarted to load this new MCP.

## Two new clean-room, executable KOSIF routes

Implementation: scripts/video_workflow_bridge.py (Python standard library only).

**1. Word-level paper-edit plan** -- adapted from the widely-used *concept* of text-based editing, not vendor source. It accepts corrected Arabic words.json and a list of word indices, constructs reproducible frame-bounded **video-only** source segments with word boundaries, and outputs a JSON decision manifest:

    python scripts/video_workflow_bridge.py paper-edit words.json --keep "1-3,7-9" --fps 30 --out paper-edit.json

Input format: [{"word":"في","start":0.13,"end":0.33},...]. It NEVER renders or modifies audio. If the user's narration is a strict audio master, do not apply the cuts to that original recording; use audio-sync and render playbooks to align visuals to its unchanged clock.

**2. Frame-accurate review note markers** -- an original local review contract with optional normalized (x, y) anchor and integer frame/timecode, inspired by Frame.io's reviewed public workflow.

    python scripts/video_workflow_bridge.py review notes.json --duration 60 --fps 30 --width 1080 --height 1920 --out review-markers.json

Input format: [{"time":1.23,"comment":"التشكيل مقصوص","x":0.25,"y":0.60}]. Positions map to exact pixel locations in the chosen composition. Output contains stable hashed IDs and timecodes. No cloud accounts or remote approvals are implied.

Tests:
    python -m unittest discover -s evals -p test_video_workflow_bridge.py -v

Before changing badge from 'code available' to 'verified': run tests in the actual device and demonstrate generated output. The algorithms are independent originals; neither implies vendor algorithm equivalence. Do not add vendor-branded output names, copy UI trade dress, bypass DRM, or redistribute copyrighted binaries.

## Prioritized opportunities (NOT implemented)

P1: film-accurate review overlay and on-frame UI from the JSON marker contract; P2: transcript-to-EDL preview and audited splice rendering for non-master source media; P3: automatic Arabic subtitle correction with editorial review; P4: semantic highlight ranking with measured human agreement; P5: node-based image graph with validated reusable operators; P6: human-authorized collaboration/version approvals. AI generative services are optional connections with explicit billing and rights checks.
