---
name: pm-slash1sol-b35cb1
description: A 24-second 3D short: a giant dark glass slab shaped like an animation app with a pastel timeline, a cute orange cube character walking along the tracks beside a glowing playhead, a low-poly green planet sprouting trees and houses as toast notes log each step, then a glowing orange neon title and a top-down pull-back. Use to make a new video in this look (Shapes); address it by ID pm-slash1sol-b35cb1.
---

# KOSIF TOOL — One-evening animated short with Blender and Remotion / فيلم قصير ثلاثي الأبعاد: شخصية مكعبة تمشي فوق واجهة برنامج مونتاج عملاقة

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/slash1sol-b35cb1
- Video: https://www.promptsmotion.com/__l5e/assets-v1/a7dede05-9a55-4b6d-9748-0053b756a475/aa898958d5e8c6b9.mp4
- Credit: unknown (https://x.com/slash1sol/status/2114484472456397194)
- Source type: Skill · Origin: PromptsMotion
- Published on source: 2026-10-25
- Reference aspect: 16:9 (1920×1080)
- Technologies named by the source: Remotion
- Creator's public prompt length: about 117 words (not reproduced here)
- Popularity rank on source library: #82

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
فيلم ثلاثي الأبعاد مدته نحو 24 ثانية: لوح زجاجي داكن عملاق يشبه واجهة برنامج تحريك بخط زمني من مسارات ملونة باستيل، تقف عليه شخصية مكعبة برتقالية لطيفة تمشي على المسارات ومؤشر التشغيل المضيء، وكرة كوكب خضراء منخفضة المضلعات تنبت فيها أشجار مخروطية وبيوت وغيوم بينما تظهر إشعارات صغيرة بخطوات البناء، ثم عنوان نيون برتقالي متوهج فوق الكوكب ولقطة ختامية علوية تبتعد عن المشهد كله.

A 24-second 3D short: a giant dark glass slab shaped like an animation app with a pastel timeline, a cute orange cube character walking along the tracks beside a glowing playhead, a low-poly green planet sprouting trees and houses as toast notes log each step, then a glowing orange neon title and a top-down pull-back.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Three.js, WebGL, Remotion, React), suggested duration (24 s), aspect 16:9, difficulty 5/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Shapes / أشكال, Characters / شخصيات, Photos / صور.
- [playbooks/shapes.md](../../playbooks/shapes.md)
- [playbooks/characters.md](../../playbooks/characters.md)
- [playbooks/photos.md](../../playbooks/photos.md)

Category tactics:
* Build a geometric system; morph only compatible paths; animate scale, squash and stretch, rotation and easing with controlled geometry.
* Use consistent model sheets and rigs, key poses, anticipation and follow-through, readable expressions and walk cycles.
* Use original or licensed photos in layered camera rigs with planar parallax, dynamic masks and depth-aware transitions.

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
4. `python3 tools/kosif.py scaffold pm-slash1sol-b35cb1 <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
