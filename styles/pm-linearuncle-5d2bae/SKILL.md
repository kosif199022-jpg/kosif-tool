---
name: pm-linearuncle-5d2bae
description: A 7.5-minute Manim-style maths lesson on dark navy: a car and speedometer, an s=t² curve where an orange secant shrinks into a yellow tangent beside a table converging on 2, the colour-boxed limit definition, the derivative plotted beside the original, a magnifier that straightens the curve, and a recap; yellow titles top-left, subtitles at the bottom. Use to make a new video in this look (Diagrams); address it by ID pm-linearuncle-5d2bae.
---

# KOSIF TOOL — Derivative concept explainer / شرح رياضي هادئ لمفهوم المشتقة على خلفية كحلية بأسلوب مانيم

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/linearuncle-5d2bae
- Video: https://www.promptsmotion.com/__l5e/assets-v1/9b3c3322-32a6-4ab8-9372-a8393c4e3d2b/7bff7a648fae9b92.mp4
- Credit: @LinearUncle (https://x.com/LinearUncle/status/2103128559174971663)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-09-24 · credited model: Opus 5.5 · effort: Max
- Reference aspect: 16:9 (1920×1080)
- Technologies named by the source: Manim
- Creator's public prompt length: about 31 words (not reproduced here)
- Popularity rank on source library: #216

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
درس رياضيات أفقي طويل (نحو 7 دقائق و37 ثانية) على خلفية كحلية داكنة بأسلوب مانيم: سيارة صغيرة وعداد سرعة، ثم منحنى s=t² تُرسم عليه قاطعة برتقالية تضيق حتى تصير مماساً أصفر، وجدول قيم يقترب من 2، ثم صيغة التعريف بإطارات ملونة، ودالة المشتقة بجانب الأصلية، وعدسة مكبرة تُظهر استقامة المنحنى، وملخص وأسئلة. العناوين صفراء أعلى اليسار والترجمة بالصينية أسفل الشاشة.

A 7.5-minute Manim-style maths lesson on dark navy: a car and speedometer, an s=t² curve where an orange secant shrinks into a yellow tangent beside a table converging on 2, the colour-boxed limit definition, the derivative plotted beside the original, a magnifier that straightens the curve, and a recap; yellow titles top-left, subtitles at the bottom.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (SVG, Remotion, React), suggested duration (457 s), aspect 16:9, difficulty 4/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Diagrams / مخططات.
- [playbooks/diagrams.md](../../playbooks/diagrams.md)

Category tactics:
* Reveal nodes in causal order; draw SVG edges with dash offsets; move the camera between relationships deliberately.

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
4. `python3 tools/kosif.py scaffold pm-linearuncle-5d2bae <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
