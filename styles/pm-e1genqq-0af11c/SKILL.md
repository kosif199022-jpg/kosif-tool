---
name: pm-e1genqq-0af11c
description: A two-minute dark browser screen recording demoing a motion-film plugin, from a typed chat request and a streamed shot plan to the repo's style gallery, install and render docs, then a calm cream product film with a bold two-line headline and three task cards that tick one by one until the last turns deep green. Use to make a new video in this look (Product UI); address it by ID pm-e1genqq-0af11c.
---

# KOSIF TOOL — Lemo Opuscar motion film plugin / عرض شاشة لإضافة أفلام موشن: من الطلب إلى فيلم منتج هادئ بلون أخضر

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/e1genqq-0af11c
- Video: https://www.promptsmotion.com/__l5e/assets-v1/01aa8fac-9adc-4980-ba5a-ae7dce4ce3e8/75facbc6303ed970.mp4
- Credit: unknown (https://x.com/e1genqq/status/2114030972505059431)
- Source type: Skill · Origin: PromptsMotion
- Published on source: 2026-10-24
- Reference aspect: 16:9 (1920×1080)
- Creator's public prompt length: about 103 words (not reproduced here)
- Popularity rank on source library: #225

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
تسجيل شاشة مدته نحو دقيقتين لمتصفح بوضع داكن يعرض أداة إضافة لصنع أفلام الموشن: طلب يُكتب في محادثة ثم خطة مكتوبة طويلة بلقطات وتوقيتات، ثم صفحة المستودع بمعرض أساليب مصغرة وتعليمات التثبيت وجدول أوامر التصيير، ثم ثلاثة إطارات مفتاحية وأخيراً فيلم منتج بسيط على خلفية كريمية: عنوان عريض من سطرين يساراً وثلاث بطاقات مهام يميناً تُعلَّم واحدة تلو الأخرى حتى يتحول الزر الأخير إلى أخضر غامق ويظهر زر دعوة للفعل.

A two-minute dark browser screen recording demoing a motion-film plugin, from a typed chat request and a streamed shot plan to the repo's style gallery, install and render docs, then a calm cream product film with a bold two-line headline and three task cards that tick one by one until the last turns deep green.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Remotion, React, CSS), suggested duration (119 s), aspect 16:9, difficulty 2/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Product UI / واجهات المنتج, Code / كود, Ads / إعلانات.
- [playbooks/product-ui.md](../../playbooks/product-ui.md)
- [playbooks/code.md](../../playbooks/code.md)
- [playbooks/ads.md](../../playbooks/ads.md)

Category tactics:
* Recreate interface states as independent layers; animate meaningful cursor, tap, modal, scroll and focus interactions with consistent depth and realistic timings.
* Write genuine time-varying vector, Canvas, React or WebGL motion; seed all randomness; never a slideshow of stills.
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
4. `python3 tools/kosif.py scaffold pm-e1genqq-0af11c <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
