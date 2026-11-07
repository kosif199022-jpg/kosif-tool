---
name: pm-beamnxw-6d4fc1
description: A 15.6-second 4:5 piece styled as a studio dashboard: a red headline on top, a preview window playing a shallow-depth-of-field 3D shot of a red voxel character walking across a cream keyboard beside a glass jar and a tiny green robot, a row of tool cards lighting up in order beneath it, a pixel mascot speaking short captions, and a black terminal typing each stage's commands. Use to make a new video in this look (3D); address it by ID pm-beamnxw-6d4fc1.
---

# KOSIF TOOL — Small-world character film with Blender MCP / عالم صغير فوق لوحة مفاتيح: شخصية مكعبات داخل واجهة استوديو

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/beamnxw-6d4fc1
- Video: https://www.promptsmotion.com/__l5e/assets-v1/78085904-ce5d-42f0-9d87-a6c5baf15165/08e195def8391d36.mp4
- Credit: unknown (https://x.com/beamnxw/status/2113275303808160226)
- Source type: Skill · Origin: PromptsMotion
- Published on source: 2026-10-22
- Reference aspect: 4:5 (1440×1728)
- Technologies named by the source: Remotion
- Creator's public prompt length: about 114 words (not reproduced here)
- Popularity rank on source library: #145

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
مقطع رأسي 4:5 مدته 15.6 ثانية يشبه لوحة تحكم استوديو: في الأعلى عنوان أحمر، وفي الوسط نافذة معاينة تعرض لقطة سينمائية ثلاثية الأبعاد بعمق ميدان ضحل لشخصية حمراء من مكعبات صغيرة تمشي على لوحة مفاتيح كريمية بجانب برطمان زجاجي وروبوت أخضر صغير، وتحتها صف بطاقات الأدوات تضيء بالترتيب، وتميمة بكسلية تقول سطراً قصيراً، وطرفية سوداء تكتب أوامر كل مرحلة.

A 15.6-second 4:5 piece styled as a studio dashboard: a red headline on top, a preview window playing a shallow-depth-of-field 3D shot of a red voxel character walking across a cream keyboard beside a glass jar and a tiny green robot, a row of tool cards lighting up in order beneath it, a pixel mascot speaking short captions, and a black terminal typing each stage's commands.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Remotion, React, CSS, Three.js, Web Audio), suggested duration (15.6 s), aspect 4:5, difficulty 5/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: 3D / ثلاثي الأبعاد, Characters / شخصيات, Product UI / واجهات المنتج.
- [playbooks/3d.md](../../playbooks/3d.md)
- [playbooks/characters.md](../../playbooks/characters.md)
- [playbooks/product-ui.md](../../playbooks/product-ui.md)

Category tactics:
* Choose real 3D only when the camera needs it; otherwise layer 2.5D; keep lighting and materials consistent across scenes.
* Use consistent model sheets and rigs, key poses, anticipation and follow-through, readable expressions and walk cycles.
* Recreate interface states as independent layers; animate meaningful cursor, tap, modal, scroll and focus interactions with consistent depth and realistic timings.

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
4. `python3 tools/kosif.py scaffold pm-beamnxw-6d4fc1 <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
