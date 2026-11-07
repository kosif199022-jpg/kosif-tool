---
name: pm-faroukzy-9ff23e
description: A 4-minute animated short in a soft 3D-illustrated look: a small white robot keeps a red-and-white lighthouse from sunset into a stormy night, hears a distress call on an old radio, gives its glowing chest core to restart the dead lamp so the beam saves a ship, and is revived at dawn by a girl and a captain, with named subtitles. Use to make a new video in this look (Characters); address it by ID pm-faroukzy-9ff23e.
---

# KOSIF TOOL — The Last Light animated short / فيلم قصير متحرك: روبوت حارس المنارة يهب ضوءه لإنقاذ سفينة

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/faroukzy-9ff23e
- Video: https://www.promptsmotion.com/__l5e/assets-v1/6cba7cd8-1d0f-496c-ac18-0ec8afebf0b8/ea9ec5678809e9e7.mp4
- Credit: @faroukzy (https://x.com/faroukzy/status/2103387771180138551)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-09-25 · credited model: Opus 5.5 · effort: Max
- Reference aspect: 16:9 (1280×720)
- Creator's public prompt length: about 9 words (not reproduced here)
- Popularity rank on source library: #183

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
فيلم قصير متحرك مدته 4 دقائق بأسلوب رسوم دافئة ثلاثية الأبعاد ناعمة: من الفضاء إلى الغروب فوق منارة حمراء وبيضاء على صخرة، روبوت أبيض صغير بوجه شاشة ونواة مضيئة في صدره يعتني بالمصباح، ثم ليل وعاصفة ونداء استغاثة عبر راديو قديم وسفينة تقترب من الصخور، فينطفئ المصباح ويضع الروبوت نواته فيه فيشق الشعاع العاصفة، وينتهي بفجر وفتاة وقبطانة تعيدان إليه الحياة، مع ترجمة بأسماء المتحدثين وأشرطة سينمائية في الذروة.

A 4-minute animated short in a soft 3D-illustrated look: a small white robot keeps a red-and-white lighthouse from sunset into a stormy night, hears a distress call on an old radio, gives its glowing chest core to restart the dead lamp so the beam saves a ship, and is revived at dawn by a girl and a captain, with named subtitles.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Three.js, WebGL, Remotion, Web Audio), suggested duration (240 s), aspect 16:9, difficulty 5/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Characters / شخصيات, 3D / ثلاثي الأبعاد.
- [playbooks/characters.md](../../playbooks/characters.md)
- [playbooks/3d.md](../../playbooks/3d.md)

Category tactics:
* Use consistent model sheets and rigs, key poses, anticipation and follow-through, readable expressions and walk cycles.
* Choose real 3D only when the camera needs it; otherwise layer 2.5D; keep lighting and materials consistent across scenes.

## Original creative direction (التوجيه الإبداعي)
Produce a NEW video from the user's own concept, voice or footage, inspired by this reference.
* Start from a consistent geometry system and original design tokens; document measured versus estimated colors, type, line weights, easing and camera in STYLE.md.
* Give every scene an audio interval and a visual action. Plan creation order, camera movement, transition and sound cue at sentence or phrase granularity in PLAN.md.
* Everything animates: paths draw in sequence, rigs move, information is revealed causally. Static slideshow transitions are not acceptable.
* Build editable, deterministic animation with Remotion/React, SVG/Canvas (see starters/html-canvas) or Three.js for true spatial scenes; render with tools/render_html.cjs or Remotion. Never imply integrations that are not installed.
* Default 9:16, 1080×1920, 30 fps, H.264 MP4 with AAC audio. Respect the user's aspect ratio, duration, branding and timeline.
* Existing AUDIO is master time: keep the voice untouched, transcribe, align words and animate to verified timestamps; aim for ≤ 100 ms on key words and check it.
* For source VIDEO, preserve the authorized material and align the treatment to real cuts, actions and phrases. For TEXT, write short narration and a timestamped scene plan.
* Arabic needs RTL shaping and phone-safe typography; never split joined letters to animate them (see playbooks/arabic-typography.md).
* Entrances 250–600 ms, accents 120–300 ms, transitions 300–800 ms as first estimates; refine after inspecting the reference.
* Preserve legibility, hierarchy, emotional pacing and performance.

## Claude production runbook (خطوات الإنتاج)
1. Read CLAUDE.md, AGENTS.md, this skill, STYLE.json, BRIEF.md (if present) and the playbooks above.
2. Open the source page and inspect the video where possible; never copy it into this repository.
3. Gather the user's assets; ask at most one batch of necessary questions.
4. `python3 tools/kosif.py scaffold pm-faroukzy-9ff23e <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
