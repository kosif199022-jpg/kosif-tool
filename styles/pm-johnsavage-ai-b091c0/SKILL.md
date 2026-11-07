---
name: pm-johnsavage-ai-b091c0
description: A 15-second code-made showreel inside a monitor-style HUD frame: an ease curve, a huge black 'MOTION' on orange with script 'design', a neon-lit chrome blob, a morphing shape grid, a red particle vortex forming '100% CODE', ridgeline waves on blue, skill bars, a circular-text tunnel, and a glitching name card. Use to make a new video in this look (Kinetic type); address it by ID pm-johnsavage-ai-b091c0.
---

# KOSIF TOOL — Code-only motion design reel / بكرة موشن مكتوبة بالكود بالكامل بإطار شاشة عرض

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/johnsavage-ai-b091c0
- Video: https://www.promptsmotion.com/__l5e/assets-v1/c37fe97c-2f55-4cc9-a9bf-9b904c4038d1/0d19454ecd0d67d8.mp4
- Credit: @johnsavage_ai (https://x.com/johnsavage_ai/status/2103600308010041677)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-09-25 · credited model: Opus 5.5 · effort: Max
- Reference aspect: 16:9 (1920×1080)
- Creator's public prompt length: about 29 words (not reproduced here)
- Popularity rank on source library: #80

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
بكرة أعمال مدتها 15 ثانية بإطار واجهة تقنية (زوايا، رقم فصل، مؤقت زمني): نقطة بيضاء ترسم منحنى تخفيف، كلمة «MOTION» سوداء ضخمة على برتقالي مع «design» بخط يدوي مائل، كتلة كروم سائلة تعكس أضواء نيون أمام نص مائل، شبكة أشكال تتحول من دوائر إلى مربعات ومثلثات، دوامة جسيمات حمراء تتجمع في «100% CODE»، خطوط موجية بيضاء على أزرق، أشرطة مهارات، أنفاق نص دائري، ثم اسم ختامي ينهار.

A 15-second code-made showreel inside a monitor-style HUD frame: an ease curve, a huge black 'MOTION' on orange with script 'design', a neon-lit chrome blob, a morphing shape grid, a red particle vortex forming '100% CODE', ridgeline waves on blue, skill bars, a circular-text tunnel, and a glitching name card.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Three.js, WebGL, HTML Canvas, Remotion, React), suggested duration (15 s), aspect 16:9, difficulty 5/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Kinetic type / تايبوغرافي متحرك, Code / كود, Particles / جسيمات, 3D / ثلاثي الأبعاد.
- [playbooks/kinetic-type.md](../../playbooks/kinetic-type.md)
- [playbooks/code.md](../../playbooks/code.md)
- [playbooks/particles.md](../../playbooks/particles.md)
- [playbooks/3d.md](../../playbooks/3d.md)

Category tactics:
* Animate readable words in timed beats; sync emphasis to spoken words; preserve Arabic shaping and RTL; never split joined letters.
* Write genuine time-varying vector, Canvas, React or WebGL motion; seed all randomness; never a slideshow of stills.
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
4. `python3 tools/kosif.py scaffold pm-johnsavage-ai-b091c0 <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
