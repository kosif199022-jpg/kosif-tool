---
name: pm-ratheejaisal-1f4538
description: A silent 20-second launch spot on a cool off-white ground: the logo reveals with a left-to-right mask, then a run of shots on one fixed layout (a bold two-line headline with a small mono kicker on the left, a white shadowed UI card on the right): claiming a handle, a profile card, a project list with Live pills, a revenue counter over a heatmap, a visitors counter with a sparkline, a revenue bar race, a founder directory on a dotted world map, a verified badge on a site and an end card with a CTA clicked by a cursor.
---

# KOSIF TOOL — founder.page launch video / فيديو إطلاق founder.page السريع

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/ratheejaisal-1f4538
- Video: https://www.promptsmotion.com/__l5e/assets-v1/2de11de5-a364-4eb2-a2d9-4a9c33888c4c/082ae40fc7e74279.mp4
- Credit: @RatheeJaisal (https://x.com/RatheeJaisal/status/2103774864742154698)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-09-26 · credited model: Opus 5.5 · effort: Max
- Reference aspect: 16:9 (1920×1080)
- Creator's public prompt length: about 24 words (not reproduced here)
- Popularity rank on source library: #141

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
إعلان إطلاق مدته 20 ثانية بلا صوت على خلفية بيضاء مائلة للرمادي البارد: كشف الشعار بقناع من اليسار إلى اليمين، ثم لقطات على تخطيط ثابت (عنوان عريض من سطرين مع وسم أحادي صغير يساراً وبطاقة واجهة بيضاء بظل يميناً): حجز اسم المستخدم، بطاقة ملف شخصي، قائمة مشاريع بشارات «مباشر»، عدّاد إيرادات فوق خريطة حرارية، عدّاد زوار بخط صغير، سباق أعمدة إيرادات، دليل مؤسسين على خريطة عالم منقطة، شارة توثيق داخل موقع، وبطاقة ختام بزر ينقره المؤشر.

A silent 20-second launch spot on a cool off-white ground: the logo reveals with a left-to-right mask, then a run of shots on one fixed layout (a bold two-line headline with a small mono kicker on the left, a white shadowed UI card on the right): claiming a handle, a profile card, a project list with Live pills, a revenue counter over a heatmap, a visitors counter with a sparkline, a revenue bar race, a founder directory on a dotted world map, a verified badge on a site and an end card with a CTA clicked by a cursor.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Remotion, React, CSS), suggested duration (20 s), aspect 16:9, difficulty 3/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Product UI / واجهات المنتج.
- [playbooks/product-ui.md](../../playbooks/product-ui.md)

Category tactics:
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
4. `python3 tools/kosif.py scaffold pm-ratheejaisal-1f4538 <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
