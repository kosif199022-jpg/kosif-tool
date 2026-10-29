---
name: pm-ceowinkz-7c776b
description: A 15-second B2B pitch from an Amazon wholesale company to brands, on a navy ground with a HUD frame and floating dust: a W logo inside a cyan ring drawing on, a red problem act (too many sellers, price sliding) with a Buy Box card whose price counts down, then a cyan solution act: price protected, a $10,000 paid-upfront order, a before/after listing rebuild, one product branching to three marketplaces, and a growth line whose arrow flies into the final logo.
---

# KOSIF TOOL — Amazon wholesale pitch video / عرض Winkz: لماذا نبيع منتجاتكم على أمازون

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/ceowinkz-7c776b
- Video: https://www.promptsmotion.com/__l5e/assets-v1/42f54c8b-759b-4cf2-b8ae-362443764810/a3a1ecf7d59c977a.mp4
- Credit: @ceowinkz (https://x.com/ceowinkz/status/2103647124126683602)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-09-26 · credited model: Opus 5.5 · effort: Max
- Reference aspect: 16:9 (1920×1080)
- Creator's public prompt length: about 30 words (not reproduced here)
- Popularity rank on source library: #161

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
عرض B2B مدته 15 ثانية من شركة جملة على أمازون إلى العلامات التجارية، على خلفية كحلية بإطار HUD وغبار طافٍ: شعار W داخل حلقة سماوية تُرسم، ثم فصل مشكلة أحمر (بائعون كثر، سعر ينهار) ببطاقة Buy Box يهبط سعرها، ثم فصل حل سماوي: حماية السعر، طلب مدفوع مقدماً بقيمة 10,000 دولار، إعادة بناء القائمة قبل وبعد، منتج يتفرع إلى ثلاثة أسواق، ومنحنى نمو يطير سهمه إلى الشعار الختامي.

A 15-second B2B pitch from an Amazon wholesale company to brands, on a navy ground with a HUD frame and floating dust: a W logo inside a cyan ring drawing on, a red problem act (too many sellers, price sliding) with a Buy Box card whose price counts down, then a cyan solution act: price protected, a $10,000 paid-upfront order, a before/after listing rebuild, one product branching to three marketplaces, and a growth line whose arrow flies into the final logo.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Remotion, React, SVG), suggested duration (15 s), aspect 16:9, difficulty 3/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Charts / رسوم بيانية.
- [playbooks/charts.md](../../playbooks/charts.md)

Category tactics:
* Use truthful data; animate counters, bars, lines and chart morphs whose labels stay accurate; keep axes and legends readable; reveal one insight at a time.

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
4. `python3 tools/kosif.py scaffold pm-ceowinkz-7c776b <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
