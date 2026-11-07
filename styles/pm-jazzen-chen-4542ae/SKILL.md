---
name: pm-jazzen-chen-4542ae
description: A 30 s app-launch film on near-black navy built entirely around a laptop notch: two sparks trace its edges and ignite a green-to-amber-to-red glowing rim, quota labels branch out of it, a monospace line types itself, ASCII and binary character flows pour around it, then the notch expands into status, warning, statistics and approval cards before a wide laptop shot and a product name card. Use to make a new video in this look (Product UI); address it by ID pm-jazzen-chen-4542ae.
---

# KOSIF TOOL — AgentHud project motion video / إطلاق تطبيق نوتش متوهج: جزيرة ديناميكية لحصص وكلاء الذكاء الاصطناعي

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/jazzen-chen-4542ae
- Video: https://www.promptsmotion.com/__l5e/assets-v1/00d7e9a1-23c3-4525-b909-e307fcdeaab2/163da1ff9ba29ac8.mp4
- Credit: @Jazzen_Chen (https://x.com/Jazzen_Chen/status/2103751442393894989)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-09-26 · credited model: Opus 5.5 · effort: Max
- Reference aspect: 16:9 (1920×1080)
- Creator's public prompt length: about 10 words (not reproduced here)
- Popularity rank on source library: #125

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
فيديو إطلاق منتج مدته 30 ثانية على خلفية كحلية شبه سوداء يدور كله حول نوتش شاشة لابتوب: شرارتان تنزلقان على حوافه فتشعلان حدّاً متوهجاً متدرجاً من الأخضر إلى الأصفر إلى الأحمر، ثم وسوم الحصص تتفرع منه، وجملة بخط أحادي المسافة تُكتب حرفاً حرفاً، ثم أنماط ASCII وثنائية ملونة تنساب حوله، ثم يتمدد النوتش إلى بطاقات حالة وتحذير وإحصاءات وموافقة بنقرة، ثم لقطة لابتوب واسعة وبطاقة اسم المنتج.

A 30 s app-launch film on near-black navy built entirely around a laptop notch: two sparks trace its edges and ignite a green-to-amber-to-red glowing rim, quota labels branch out of it, a monospace line types itself, ASCII and binary character flows pour around it, then the notch expands into status, warning, statistics and approval cards before a wide laptop shot and a product name card.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Remotion, React, CSS, SVG, HTML Canvas), suggested duration (30 s), aspect 16:9, difficulty 4/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Product UI / واجهات المنتج, Kinetic type / تايبوغرافي متحرك, Charts / رسوم بيانية.
- [playbooks/product-ui.md](../../playbooks/product-ui.md)
- [playbooks/kinetic-type.md](../../playbooks/kinetic-type.md)
- [playbooks/charts.md](../../playbooks/charts.md)

Category tactics:
* Recreate interface states as independent layers; animate meaningful cursor, tap, modal, scroll and focus interactions with consistent depth and realistic timings.
* Animate readable words in timed beats; sync emphasis to spoken words; preserve Arabic shaping and RTL; never split joined letters.
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
4. `python3 tools/kosif.py scaffold pm-jazzen-chen-4542ae <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
