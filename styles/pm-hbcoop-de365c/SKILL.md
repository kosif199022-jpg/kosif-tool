---
name: pm-hbcoop-de365c
description: A 29 s 16:9 piece on cream paper where one shape evolves from a point to a line, a circle and a glossy black 3D sphere, then a glass lens over code, a ball bouncing with a red dotted trail, a particle flock and a halftone globe, before shrinking to the full stop of a typed sentence, each stage captioned 'FIG. N' in italic serif, with no cuts. Use to make a new video in this look (3D); address it by ID pm-hbcoop-de365c.
---

# KOSIF TOOL — Full Stop figure sequence / متتالية أشكال «شكل 1… شكل 9» على ورق كريمي: من نقطة إلى كرة وسرب وعالم

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/hbcoop-de365c
- Video: https://www.promptsmotion.com/__l5e/assets-v1/1457c28e-6c5e-4c84-b228-2b7b95bc61ac/3144fee272b6cd09.mp4
- Credit: @HBCoop_ (https://x.com/HBCoop_/status/2107139305324122491)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-10-05 · credited model: Opus 5.5 · effort: Max
- Reference aspect: 16:9 (1920×1080)
- Creator's public prompt length: about 17 words (not reproduced here)
- Popularity rank on source library: #230

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
مقطع 16:9 مدته نحو 29 ثانية على ورق كريمي هادئ يتطور فيه شكل واحد من نقطة إلى خط ثم دائرة ثم كرة سوداء لامعة ثلاثية الأبعاد بظل ناعم، ثم عدسة زجاجية تكسر سطور كود منسوخة على الأرض، وكرة ترتد تاركة أثراً منقطاً أحمر، وسرب جسيمات يتلوّى، وكرة أرضية بنقش نقطي تدور، ثم تعود نقطة وتصير نقطة نهاية جملة مكتوبة، وتحت كل مرحلة تعليق «شكل N» بخط مائل.

A 29 s 16:9 piece on cream paper where one shape evolves from a point to a line, a circle and a glossy black 3D sphere, then a glass lens over code, a ball bouncing with a red dotted trail, a particle flock and a halftone globe, before shrinking to the full stop of a typed sentence, each stage captioned 'FIG. N' in italic serif, with no cuts.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Remotion, React, Three.js, WebGL, SVG), suggested duration (29 s), aspect 16:9, difficulty 5/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: 3D / ثلاثي الأبعاد, Shapes / أشكال, Particles / جسيمات.
- [playbooks/3d.md](../../playbooks/3d.md)
- [playbooks/shapes.md](../../playbooks/shapes.md)
- [playbooks/particles.md](../../playbooks/particles.md)

Category tactics:
* Choose real 3D only when the camera needs it; otherwise layer 2.5D; keep lighting and materials consistent across scenes.
* Build a geometric system; morph only compatible paths; animate scale, squash and stretch, rotation and easing with controlled geometry.
* Use deterministic seeded particles with explicit emitters, fields, attraction and decay that carry story meaning, not decoration.

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
4. `python3 tools/kosif.py scaffold pm-hbcoop-de365c <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
