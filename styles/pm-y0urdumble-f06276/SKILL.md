---
name: pm-y0urdumble-f06276
description: A 16-second vertical split: on top, a voxel 3D scene on a periwinkle floor with stars where a cute orange cube character beams a builder ray to assemble a moustached, sunglassed man in a mustard suit layer by layer, rigs him and both dance; below, a dark dashboard with stage tabs, a progress bar, a beat grid of key-pose diamonds and a command log typing line by line. Use to make a new video in this look (3D); address it by ID pm-y0urdumble-f06276.
---

# KOSIF TOOL — Dancing voxel character built in Blender / شخصية فوكسل تُبنى وتُركّب لها مفاصل وترقص مع لوحة سجل حية

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/y0urdumble-f06276
- Video: https://www.promptsmotion.com/__l5e/assets-v1/8b36f2b6-0297-4c7b-8a54-9e7223b37048/6ad473ff41c72803.mp4
- Credit: unknown (https://x.com/Y0urDumble/status/2113374545302200732)
- Source type: Skill · Origin: PromptsMotion
- Published on source: 2026-10-22
- Reference aspect: other (1080×1500)
- Creator's public prompt length: about 103 words (not reproduced here)
- Popularity rank on source library: #223

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
فيديو عمودي مدته 16 ثانية بقسمين: في الأعلى مشهد فوكسل ثلاثي الأبعاد على أرضية بنفسجية بنجوم، فيه مكعب برتقالي لطيف بوجه يشير بشعاع ليبني رجلاً بنظارة شمسية وشارب وبدلة خردلية طبقة طبقة، ثم تُضاف المفاصل ويرقص الاثنان؛ وفي الأسفل لوحة داكنة بتبويبات المراحل وشريط تقدم وخط إيقاع بنقاط مفاتيح وسجل أوامر يُكتب سطراً سطراً.

A 16-second vertical split: on top, a voxel 3D scene on a periwinkle floor with stars where a cute orange cube character beams a builder ray to assemble a moustached, sunglassed man in a mustard suit layer by layer, rigs him and both dance; below, a dark dashboard with stage tabs, a progress bar, a beat grid of key-pose diamonds and a command log typing line by line.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Three.js, React, Remotion), suggested duration (16 s), aspect 1080x1500, difficulty 4/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: 3D / ثلاثي الأبعاد, Characters / شخصيات, Code / كود.
- [playbooks/3d.md](../../playbooks/3d.md)
- [playbooks/characters.md](../../playbooks/characters.md)
- [playbooks/code.md](../../playbooks/code.md)

Category tactics:
* Choose real 3D only when the camera needs it; otherwise layer 2.5D; keep lighting and materials consistent across scenes.
* Use consistent model sheets and rigs, key poses, anticipation and follow-through, readable expressions and walk cycles.
* Write genuine time-varying vector, Canvas, React or WebGL motion; seed all randomness; never a slideshow of stills.

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
4. `python3 tools/kosif.py scaffold pm-y0urdumble-f06276 <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
