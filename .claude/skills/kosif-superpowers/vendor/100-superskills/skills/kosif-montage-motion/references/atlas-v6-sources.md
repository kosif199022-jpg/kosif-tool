# What v6 took from where (2026-10-09)

Sources read for this release and what each one changed. Nothing was copied verbatim; the Atlas skills were read as
untrusted reference and re-expressed in this kit's own code and rules.

| Source | Taken |
|---|---|
| `KOSIF-Motion-Workbench-complete-source-v3.zip` (site/lib/motion.ts, app/api, app/mcp, python-render-service/service.py, skill-client) | The whole contract of the local site: `make_plan`/`validate_plan`/`compile_plan` ported line by line (the 13 `domain.cjs` cases pass in Python), `drawFrame` as `manifest-player.js`, the strict manifest model and the Pillow frame of the render service, the job-token render API (404/409/422 semantics, ffprobe verification), the 4 MCP tools. Its README/VERIFICATION set the honesty rules (what is proven, what is not). |
| `kosif-montage-motion-site-v5.3-python.zip` | `render_client.py` + its 13 mocked tests, the public (anonymous) `site_bridge.py` and its 31 tests (one skips on Windows without symlink rights), `python-render.md`, `audit-v5.3-python.md`, `LEGACY_WORKFLOWS.md`. |
| `KOSIF-Montage-Motion-v5.1-Voice2Motion.zip` | Already inside v5.2 (`audio2motion`); checked, nothing newer. |
| v5.2 (الاداة/kosif-montage-motion) | The base: every v5.2 script, kit, template, test and reference stays; the v5.2 audit fixes (safe names, escaping, encoder exit codes, UTF-8 consoles) are kept over the v5.3 copies. |
| `ultra-motion-montage` skill (smart_montage.py, qa_inspector.py) | The caption `tiktok` style family and the "4 words, the spoken word alone pops" rule; the 6 grades were already in v5. |
| Atlas `remotion/remotion-captions` (10431) | Captions as timed JSON (`startMs/endMs` → `start/end/words`), 1–4 words at a time for vertical video → the `tiktok`/`hormozi` styles' `max_words`. |
| Atlas `akbun-editvideo/davinciresolve-face-mosaic` (2456) | Mask only what is needed, keep the background, expand the mask a little, track across the clip, verify start/middle/end → `kmotion privacy` (pad, hold, review note). |
| Atlas `akbun-editvideo/davinciresolve-youtube-shorts` (2466) | Record the source's facts before editing, never modify the source, check feasibility (60 s + handles), inspect representative frames; "an API call is not proof of framing" → `platforms` warnings and the gate-before-claim rule. |
| Atlas `akbun-editvideo/akbun-davinciresolve-cut-new-york` (2433) | Cut rhythm: alternate wide/medium/detail, don't cut every beat, keep place changes even off-beat, simple cuts by default → `scenes --timeline` defaults to cuts, transitions only when asked. |
| Atlas `akbun-editvideo/akbun-davinciresolve-caption-template` (2431) | Letter height 3.5–4.5 % of the frame, margins ≥ 8 %, one line preferred, two max, keyword 2–3× the guide line, no random pops → caption sizes and the `minimal` style. |
| Atlas `mas-video-lab/ffmpeg` (754) | Deterministic `-filter_complex` authoring, keyframe interval alignment (`-g fps`), stream health via ffprobe JSON → the timeline compiler's intermediates and offsets measured from the picture's frames. |
| Atlas `streaming-media-engineering/transcoding-and-abr-ladder` (9243) | Ladders are per-title and every bitrate is `[verify-at-use]`; H.264 as the reach floor → `platforms.py` ceilings marked as commonly published, never silent trims. |
| Atlas `lvtd-skills/game-smooth-curves-and-motion` (8088) | Continuity targets (C1 tangents) and arc-length-style parameterisation → speed ramps integrated exactly (log map), raised-cosine zoom. |
| Atlas `video-skills/brand-grid-video` (213) | Review rendered frames at the opening, each cut and the closing; watch at phone size → the site's project panel shows frames and the phone sheet. |
| Atlas `youtube/creator-visual-director` (13229), `film-video-production/define-the-deliverables` (8773) | Deliverables named up front (ratio, length, platform) → the platforms recipe and the export poster. |
| `kosif-audit-pro` (GitHub) | Its UI motion rule — motion only on `transform`/`opacity`, respect `prefers-reduced-motion`, never animate numbers — informed the site's CSS (no transitions on data) and the quiet job/strip panels. |
| `kosif-atlas` / `kosif-atlas-private` (local mirrors) | The 355 video/motion/animation entries were listed with the index; the ones above were read. No vendored code. |
| `kosif-studio` (local repo) | `ai_bridge.py` → `claude_bridge.py` (CLI discovery, API key route, copy/paste package); the engine copy there is older than v6. |
