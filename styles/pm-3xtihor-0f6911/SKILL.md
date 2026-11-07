---
name: pm-3xtihor-0f6911
description: A 15-second showreel with viewfinder corners and timecode: a red ball drops with onion-skin ghosts, giant words smear across an orange field, a cream square morphs on blue with bezier handles, grids breathe, a 3D cylinder of motion terms spins, a five-tile bento board shows skills, and a particle vortex condenses into the name with a red-dot end card. Use to make a new video in this look (Kinetic type); address it by ID pm-3xtihor-0f6911.
---

# KOSIF TOOL — Claude motion designer showreel / شوريل مصمم موشن: حلقة نصوص ثلاثية الأبعاد وألواح مهارات

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/3xtihor-0f6911
- Video: https://www.promptsmotion.com/__l5e/assets-v1/13227fa7-74be-482d-a23d-6bf3b9eb00ec/c35fbff0a7436791.mp4
- Credit: @3xtihor (https://x.com/3xtihor/status/2103551886272159839)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-09-25 · credited model: Opus 5.5 · effort: Max
- Reference aspect: 16:9 (1280×720)
- Creator's public prompt length: about 26 words (not reproduced here)
- Popularity rank on source library: #104

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
شوريل مدته 15 ثانية بإطار عدسة ورقم وقت وعلامة إيقاع: كرة حمراء تسقط بآثار متكررة على خط بمقياس، ثم كلمتان ضخمتان على حقل برتقالي (الثانية تتمدد ضبابياً)، مربع كريمي يتحول إلى مثلث وزهرة على أزرق بمقابض بيزيه، شبكة مربعات ثم نقاط تتنفس، حلقة أسطوانية دوارة من نصوص الموشن بالليموني والأحمر والوردي، لوحة شبكية من خمس بطاقات مهارات، دوامة جسيمات تتجمع في اسم، وختام بالاسم ونقطة حمراء.

A 15-second showreel with viewfinder corners and timecode: a red ball drops with onion-skin ghosts, giant words smear across an orange field, a cream square morphs on blue with bezier handles, grids breathe, a 3D cylinder of motion terms spins, a five-tile bento board shows skills, and a particle vortex condenses into the name with a red-dot end card.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Remotion, React, SVG, Three.js, HTML Canvas), suggested duration (15 s), aspect 16:9, difficulty 4/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Kinetic type / تايبوغرافي متحرك, Shapes / أشكال, Particles / جسيمات, 3D / ثلاثي الأبعاد.
- [playbooks/kinetic-type.md](../../playbooks/kinetic-type.md)
- [playbooks/shapes.md](../../playbooks/shapes.md)
- [playbooks/particles.md](../../playbooks/particles.md)
- [playbooks/3d.md](../../playbooks/3d.md)

Category tactics:
* Animate readable words in timed beats; sync emphasis to spoken words; preserve Arabic shaping and RTL; never split joined letters.
* Build a geometric system; morph only compatible paths; animate scale, squash and stretch, rotation and easing with controlled geometry.
* Use deterministic seeded particles with explicit emitters, fields, attraction and decay that carry story meaning, not decoration.
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
4. `python3 tools/kosif.py scaffold pm-3xtihor-0f6911 <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
