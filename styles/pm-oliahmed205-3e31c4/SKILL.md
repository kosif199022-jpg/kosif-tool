---
name: pm-oliahmed205-3e31c4
description: A 15-second photo-editing app promo on a glowing navy-violet field: a bold headline with a gradient lens O, a face scanned on a phone with a before/after slider, strips of one street in different looks, a pink brush erasing objects into pixels, a tilted photo wall, image-filled words and a gradient app icon end card. Use to make a new video in this look (Product UI); address it by ID pm-oliahmed205-3e31c4.
---

# KOSIF TOOL — Photo retouch app promo / إعلان تطبيق تعديل صور بتوهج بنفسجي ومقارنة قبل وبعد

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/oliahmed205-3e31c4
- Video: https://www.promptsmotion.com/__l5e/assets-v1/14d123c9-ee1c-4619-92b2-0fb0f6744bf8/7194fd51c41045bb.mp4
- Credit: @oliahmed205 (https://x.com/oliahmed205/status/2104679078465069378)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-09-28 · credited model: Opus 5.5 · effort: Max
- Reference aspect: 16:9 (1280×720)
- Creator's public prompt length: about 21 words (not reproduced here)
- Popularity rank on source library: #237

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
إعلان مدته 15 ثانية لتطبيق تعديل صور على خلفية كحلية بنفسجية متوهجة: عنوان أبيض عريض تصبح فيه إحدى الحروف عدسة بتدرج، صورة وجه بالأبيض والأسود، هاتف يمسح الوجه بنقاط ثم شريط مقارنة قبل وبعد مع بطاقات قيم، شرائح عمودية لنفس الشارع بفلاتر مختلفة، محو جسم من صورة شاطئ بفرشاة وردية يتفتت إلى بكسلات، جدار صور مائل، كلمات بحشو صور، وختام بأيقونة التطبيق.

A 15-second photo-editing app promo on a glowing navy-violet field: a bold headline with a gradient lens O, a face scanned on a phone with a before/after slider, strips of one street in different looks, a pink brush erasing objects into pixels, a tilted photo wall, image-filled words and a gradient app icon end card.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Remotion, React, CSS, HTML Canvas), suggested duration (15 s), aspect 16:9, difficulty 4/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Product UI / واجهات المنتج, Photos / صور, Phone / هاتف.
- [playbooks/product-ui.md](../../playbooks/product-ui.md)
- [playbooks/photos.md](../../playbooks/photos.md)
- [playbooks/phone.md](../../playbooks/phone.md)

Category tactics:
* Recreate interface states as independent layers; animate meaningful cursor, tap, modal, scroll and focus interactions with consistent depth and realistic timings.
* Use original or licensed photos in layered camera rigs with planar parallax, dynamic masks and depth-aware transitions.
* Use 3D or 2.5D phone layers with believable screen perspective, shadow, touch interaction, device rotation and safe crops.

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
4. `python3 tools/kosif.py scaffold pm-oliahmed205-3e31c4 <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
