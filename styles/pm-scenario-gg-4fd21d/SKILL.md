---
name: pm-scenario-gg-4fd21d
description: A 55-second cinematic live-action ad: one actor repeats the same motion across an office, mine, ice tunnel and neon corridor, a black title card, then white condensed captions ending on an italic word (change the cast, world, animal; keep the moves, camera; swap the product) over restyled takes, closing on a drink spot on sea cliffs. Use to make a new video in this look (Photos); address it by ID pm-scenario-gg-4fd21d.
---

# KOSIF TOOL — ALTER: restyle footage you already shot / إعلان أداة تعيد تصميم لقطات مصورة: بدّل كل شيء واحتفظ بالأداء

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/scenario-gg-4fd21d
- Video: https://www.promptsmotion.com/__l5e/assets-v1/23e640ac-fc5c-4e38-a2fd-1b8edd47df21/9338f0d221dfb1b0.mp4
- Credit: unknown (https://x.com/Scenario_gg/status/2113998556524646534)
- Source type: Skill · Origin: PromptsMotion
- Published on source: 2026-10-24
- Reference aspect: 16:9 (1920×1080)
- Creator's public prompt length: about 117 words (not reproduced here)
- Popularity rank on source library: #149

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
إعلان سينمائي مدته نحو 55 ثانية من لقطات حية: ممثل واحد يشرب القهوة في مكتب ثم يجد نفسه بالحركة نفسها في منجم ونفق جليدي وممر نيون، ثم بطاقة عنوان سوداء بكلمة ضخمة، وسلسلة من «CHANGE THE cast/world/animal» و«KEEP THE moves/camera» و«SWAP THE product» بعناوين بيضاء مكثفة ونهاية الجملة مائلة، تثبت فوق نسخ مختلفة من اللقطة الأصلية، وينتهي بإعلان مشروب على جرف بحري.

A 55-second cinematic live-action ad: one actor repeats the same motion across an office, mine, ice tunnel and neon corridor, a black title card, then white condensed captions ending on an italic word (change the cast, world, animal; keep the moves, camera; swap the product) over restyled takes, closing on a drink spot on sea cliffs.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Remotion, React, CSS), suggested duration (55 s), aspect 16:9, difficulty 5/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Photos / صور, Ads / إعلانات.
- [playbooks/photos.md](../../playbooks/photos.md)
- [playbooks/ads.md](../../playbooks/ads.md)

Category tactics:
* Use original or licensed photos in layered camera rigs with planar parallax, dynamic masks and depth-aware transitions.
* Hook in the first second; one feature per beat; clear price or call-to-action card; brand-consistent logo reveal.

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
4. `python3 tools/kosif.py scaffold pm-scenario-gg-4fd21d <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
