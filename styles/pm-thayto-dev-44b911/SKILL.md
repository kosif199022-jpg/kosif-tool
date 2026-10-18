---
name: pm-thayto-dev-44b911
description: A calm 15-second promo for a CV-tailoring tool's Pro plan: a serif question about how many applications it takes beside a fanning stack of job cards that counts up, a per-job price list against a fixed Pro card, a feature grid, a dark cost-per-day slide, a payment card and a logo end on royal blue.
---

# KOSIF TOOL — AjustaCV Pro pricing promo / ترويج خطة Pro لأداة ملاءمة السيرة الذاتية

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/thayto-dev-44b911
- Video: https://www.promptsmotion.com/__l5e/assets-v1/de1f1c38-57a4-40e4-aac9-bd28a594705f/eeac9a4b52462637.mp4
- Credit: @thayto_dev (https://x.com/thayto_dev/status/2104200591278739735)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-09-27 · credited model: Opus 5.5 · effort: Max
- Reference aspect: 16:9 (1920×1080)
- Creator's public prompt length: about 26 words (not reproduced here)
- Popularity rank on source library: #6

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
إعلان هادئ مدته 15 ثانية لخطة Pro في أداة تكييف السيرة الذاتية: سؤال بخط سيريف عن عدد الوظائف مع رزمة بطاقات وظائف تتفتح وتعدّ، ثم مقارنة سعر لكل وظيفة مقابل بطاقة Pro ثابتة، شبكة مزايا، شريحة تكلفة يومية داكنة، بطاقة دفع، وختام بالشعار على أزرق ملكي.

A calm 15-second promo for a CV-tailoring tool's Pro plan: a serif question about how many applications it takes beside a fanning stack of job cards that counts up, a per-job price list against a fixed Pro card, a feature grid, a dark cost-per-day slide, a payment card and a logo end on royal blue.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Remotion, React, CSS), suggested duration (15 s), aspect 16:9, difficulty 2/5.

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
4. `python3 tools/kosif.py scaffold pm-thayto-dev-44b911 <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
