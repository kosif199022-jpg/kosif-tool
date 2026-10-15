---
name: pm-ror-fly-9950f1
description: A 30-second square explainer that builds a Negroni ingredient by ingredient, with measurements appearing as each pour fills the glass.
---

# KOSIF TOOL — Negroni recipe animation / وصفة نيغروني متحركة من الكأس الفارغة إلى الكوكتيل

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/ror-fly-9950f1
- Video: https://www.promptsmotion.com/__l5e/assets-v1/08bb6efa-8c3c-48e4-85cd-e3938689e266/ded9c4785ba35a75.mp4
- Credit: @Ror_Fly (https://x.com/Ror_Fly/status/2102853258582880547)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-09-23 · credited model: Opus 5.5 · effort: Max
- Reference aspect: 1:1 (1080×1080)
- Technologies named by the source: HTML
- Creator's public prompt length: about 65 words (not reproduced here)
- Popularity rank on source library: #3

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
فيلم شرح مربع مدته 30 ثانية يبني كوكتيل نيغروني مكوناً بعد مكون مع المقادير وهي تُسكب في الكأس.

A 30-second square explainer that builds a Negroni ingredient by ingredient, with measurements appearing as each pour fills the glass.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (SVG, CSS, Remotion), suggested duration (30 s), aspect 1:1, difficulty 3/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Charts / رسوم بيانية, Diagrams / مخططات, Code / كود.
- [playbooks/charts.md](../../playbooks/charts.md)
- [playbooks/diagrams.md](../../playbooks/diagrams.md)
- [playbooks/code.md](../../playbooks/code.md)

Category tactics:
* Use truthful data; animate counters, bars, lines and chart morphs whose labels stay accurate; keep axes and legends readable; reveal one insight at a time.
* Reveal nodes in causal order; draw SVG edges with dash offsets; move the camera between relationships deliberately.
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
4. `python3 tools/kosif.py scaffold pm-ror-fly-9950f1 <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
