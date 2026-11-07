---
name: pm-konstantinsaifo-96fc89
description: A 10-second screen capture of an interactive 3D web page: a rocket engine on a night test stand fires a long violet plume with shock diamonds, framed by a title card and stat readouts on the left and a control panel top-right; a click on 'cutaway' slices the engine open to reveal labelled colour-coded pumps and pipes, then the camera slowly pushes in while the oxygen path is highlighted. Use to make a new video in this look (Diagrams); address it by ID pm-konstantinsaifo-96fc89.
---

# KOSIF TOOL — Interactive Raptor 3 rocket engine explainer / شرح تفاعلي ثلاثي الأبعاد لمحرك صاروخ Raptor 3 بمقطع عرضي

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/konstantinsaifo-96fc89
- Video: https://www.promptsmotion.com/__l5e/assets-v1/3d7b51cb-3120-4ad3-ba5a-56751722d3f4/konstantinsaifo-96fc89-video_url.mp4
- Credit: @konstantinsaifo (https://x.com/konstantinsaifo/status/2104094723887501736)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-09-27 · credited model: Opus 5.5
- Reference aspect: 16:9 (1920×1080)
- Creator's public prompt length: about 47 words (not reproduced here)
- Popularity rank on source library: #2

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
تسجيل شاشة مدته 10 ثوانٍ لصفحة ويب تفاعلية ثلاثية الأبعاد: محرك صاروخ على منصة اختبار في حظيرة ليلية يطلق لهباً بنفسجياً طويلاً بعقد صدمة، مع لوحة عنوان وأرقام أداء يساراً ولوحة أزرار أعلى اليمين؛ نقرة على «مقطع عرضي» تشق المحرك فتظهر المضخات والأنابيب الملونة بملصقات، ثم تقترب الكاميرا ببطء بينما يتتبع مسار الأكسجين.

A 10-second screen capture of an interactive 3D web page: a rocket engine on a night test stand fires a long violet plume with shock diamonds, framed by a title card and stat readouts on the left and a control panel top-right; a click on 'cutaway' slices the engine open to reveal labelled colour-coded pumps and pipes, then the camera slowly pushes in while the oxygen path is highlighted.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Three.js, WebGL, React, CSS), suggested duration (10 s), aspect 16:9, difficulty 5/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Diagrams / مخططات, 3D / ثلاثي الأبعاد.
- [playbooks/diagrams.md](../../playbooks/diagrams.md)
- [playbooks/3d.md](../../playbooks/3d.md)

Category tactics:
* Reveal nodes in causal order; draw SVG edges with dash offsets; move the camera between relationships deliberately.
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
4. `python3 tools/kosif.py scaffold pm-konstantinsaifo-96fc89 <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
