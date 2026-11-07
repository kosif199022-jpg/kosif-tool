---
name: chalkboard
description: A dark green chalkboard in a wooden frame: a moving stick of coloured chalk writes an Arabic handwritten title and draws a triangle and gridded squares in white, pink, blue and yellow, small unit squares travel to fill another square as visual proof, then the equation, numbers, a tick and a summary line are written while the camera pans around the board. Use to make a new video in this look (Hand-drawn); address it by ID chalkboard.
---

# KOSIF TOOL — سبورة طباشير / سبورة طباشير خضراء تشرح درسًا

## Primary motion reference (المرجع)
- Page: https://github.com/motalim-ai/motion-starter-kit/tree/main/styles/chalkboard
- Video: https://github.com/motalim-ai/motion-starter-kit/blob/main/styles/chalkboard/reference.mp4
- Credit: KOSIF + attributed sources
- Source type: Style · Origin: KOSIF original style

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
سبورة طباشير خضراء داكنة بإطار خشبي: قطعة طباشير ملونة تتحرك فتكتب العنوان العربي بخط يدوي وترسم المثلث والمربعات بالأبيض والوردي والأزرق والأصفر، مربعات صغيرة تنتقل لتملأ مربعًا آخر كإثبات، ثم تُكتب المعادلة والأرقام وعلامة صح وخلاصة، والكاميرا تتحرك بين أجزاء اللوح.

A dark green chalkboard in a wooden frame: a moving stick of coloured chalk writes an Arabic handwritten title and draws a triangle and gridded squares in white, pink, blue and yellow, small unit squares travel to fill another square as visual proof, then the equation, numbers, a tick and a summary line are written while the camera pans around the board.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Remotion, React, SVG), suggested duration (26 s), aspect 16:9, difficulty 3/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Hand-drawn / رسم يدوي.
- [playbooks/hand-drawn.md](../../playbooks/hand-drawn.md)

Category tactics:
* Order stroke draw-on like a human hand would; keep imperfection deliberate; pace reveals to narration.

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
4. `python3 tools/kosif.py scaffold chalkboard <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
