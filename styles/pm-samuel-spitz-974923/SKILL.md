---
name: pm-samuel-spitz-974923
description: A 15-second chaptered reel with a HUD frame: a red ring, a MOTION wordmark with an underline drawing on, a Bauhaus shape grid that recolours, a tilted 3D panel with a chrome sphere and italic 'depth', a large chrome sphere on dark silk with an orbiting red ellipse, 'TYPE.' on red, chrome-filled 'TIME.' and a REEL '26 end card with a flowing red line.
---

# KOSIF TOOL — Motion design showreel / ريل عرض القدرات: فصول الحركة الأربعة

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/samuel-spitz-974923
- Video: https://www.promptsmotion.com/__l5e/assets-v1/fc6c8ff8-b1bb-4c10-be28-8aec9f6ac350/fcb2b46f3c1ee1af.mp4
- Credit: @samuel_spitz (https://x.com/samuel_spitz/status/2103544855276503053)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-09-25 · credited model: Opus 5.5 · effort: Max
- Reference aspect: 16:9 (1920×1080)
- Creator's public prompt length: about 34 words (not reproduced here)
- Popularity rank on source library: #21

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
ريل فصول مدته 15 ثانية بإطار HUD: حلقة حمراء، كلمة MOTION بخط سفلي يُرسم، شبكة أشكال باوهاوس تتبدل ألوانها، لوح ثلاثي الأبعاد مائل مع كرة كروم وكلمة depth مائلة، كرة كروم كبيرة على حرير داكن يدور حولها مدار أحمر، TYPE. على الأحمر، TIME. بملمس كروم، وختام REEL '26 بخط أحمر منساب.

A 15-second chaptered reel with a HUD frame: a red ring, a MOTION wordmark with an underline drawing on, a Bauhaus shape grid that recolours, a tilted 3D panel with a chrome sphere and italic 'depth', a large chrome sphere on dark silk with an orbiting red ellipse, 'TYPE.' on red, chrome-filled 'TIME.' and a REEL '26 end card with a flowing red line.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Remotion, React, Three.js, SVG), suggested duration (15 s), aspect 16:9, difficulty 4/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Charts / رسوم بيانية, Kinetic type / تايبوغرافي متحرك.
- [playbooks/charts.md](../../playbooks/charts.md)
- [playbooks/kinetic-type.md](../../playbooks/kinetic-type.md)

Category tactics:
* Use truthful data; animate counters, bars, lines and chart morphs whose labels stay accurate; keep axes and legends readable; reveal one insight at a time.
* Animate readable words in timed beats; sync emphasis to spoken words; preserve Arabic shaping and RTL; never split joined letters.

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
4. `python3 tools/kosif.py scaffold pm-samuel-spitz-974923 <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
