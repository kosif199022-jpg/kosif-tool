---
name: pm-shneural-2abdfa
description: A 32 s 16:9 piece playing two 15 s motion-designer showreels after black title cards: one on black in red-orange and blue (bouncing ball, rippling symbol grid, 3D block city, repeating MOTION type bands, particle swirl), the other in black, acid lime and chrome (huge stacked headlines beside twisting chrome shapes, a waveform beat screen, echoing words). Use to make a new video in this look (Kinetic type); address it by ID pm-shneural-2abdfa.
---

# KOSIF TOOL — Bold kinetic type showreel / شوريل تايبوغرافي جريء: نسختان بألوان أحمر وأزرق ثم ليموني وكروم

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/shneural-2abdfa
- Video: https://www.promptsmotion.com/__l5e/assets-v1/6d3f0a7b-698d-4ab4-a924-b1fda18583f2/297e7571f3711526.mp4
- Credit: @shneural (https://x.com/shneural/status/2103151003272962130)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-09-24 · credited model: Opus 5.5 · effort: Max
- Reference aspect: 16:9 (1920×1080)
- Creator's public prompt length: about 26 words (not reproduced here)
- Popularity rank on source library: #71

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
مقطع 16:9 مدته نحو 32 ثانية يعرض نسختين متتاليتين من شوريل مصمم حركة مدة كل منهما 15 ثانية بعد بطاقة عنوان سوداء: الأولى على الأسود بالأحمر البرتقالي والأزرق (كرة ترتد، شبكة رموز تتموّج، مدينة مكعبات ثلاثية الأبعاد، شرائط كلمة MOTION متكررة، دوامة جسيمات، شعار ختامي)، والثانية بالأسود والأخضر الليموني والكروم (عناوين ضخمة مكدّسة بجانب أشكال كروم ملتوية، شاشة إيقاع بموجة صوتية، وكلمات تتكرر كالصدى).

A 32 s 16:9 piece playing two 15 s motion-designer showreels after black title cards: one on black in red-orange and blue (bouncing ball, rippling symbol grid, 3D block city, repeating MOTION type bands, particle swirl), the other in black, acid lime and chrome (huge stacked headlines beside twisting chrome shapes, a waveform beat screen, echoing words).

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Remotion, React, Three.js, WebGL, CSS), suggested duration (32 s), aspect 16:9, difficulty 4/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Kinetic type / تايبوغرافي متحرك, 3D / ثلاثي الأبعاد, Shapes / أشكال.
- [playbooks/kinetic-type.md](../../playbooks/kinetic-type.md)
- [playbooks/3d.md](../../playbooks/3d.md)
- [playbooks/shapes.md](../../playbooks/shapes.md)

Category tactics:
* Animate readable words in timed beats; sync emphasis to spoken words; preserve Arabic shaping and RTL; never split joined letters.
* Choose real 3D only when the camera needs it; otherwise layer 2.5D; keep lighting and materials consistent across scenes.
* Build a geometric system; morph only compatible paths; animate scale, squash and stretch, rotation and easing with controlled geometry.

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
4. `python3 tools/kosif.py scaffold pm-shneural-2abdfa <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
