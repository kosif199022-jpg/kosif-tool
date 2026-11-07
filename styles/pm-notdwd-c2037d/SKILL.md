---
name: pm-notdwd-c2037d
description: A 12 s time-locked split screen comparing an AI helper app launch film (left) with its frame-matched remake for another product (right): pill name badge on pale sky gradient, app window push-in with cursor click, icon orbited by coloured squares, frosted menu-bar prompt, article morphing into image cards, glowing wordmark on black. Use to make a new video in this look (Product UI); address it by ID pm-notdwd-c2037d.
---

# KOSIF TOOL — Launch video remake comparison / مقارنة جنباً إلى جنب: فيديو إطلاق أصلي ونسخته المعاد بناؤها إطاراً بإطار

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/notdwd-c2037d
- Video: https://www.promptsmotion.com/__l5e/assets-v1/763e22ec-fb38-4dc7-97ab-079b78aaa520/a739b3361e83578f.mp4
- Credit: @notdwd (https://x.com/notdwd/status/2104401208958230764)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-09-28 · credited model: Opus 5.5 · effort: Max
- Reference aspect: 16:9 (1920×1080)
- Technologies named by the source: CSS, HTML, SVG
- Creator's public prompt length: about 1854 words (not reproduced here)
- Popularity rank on source library: #155

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
فيديو مقارنة مدته 12 ثانية بشاشة مقسومة إلى نصفين متطابقين التوقيت: إعلان إطلاق تطبيق مساعد بالذكاء الاصطناعي على اليسار ونسخة معاد بناؤها لمنتج آخر على اليمين، بالأسلوب نفسه: شارة اسم مستديرة على تدرج سماوي فاتح، تطبيق يكبر مع نقرة مؤشر، أيقونة تحيط بها مربعات ملونة تدور، شريط قوائم سطح مكتب بحقل كتابة زجاجي، صفحة مقالة تتحول إلى بطاقات بصور وعناوين، ثم شعار يتنفس وينتهي باسم متوهج على أسود.

A 12 s time-locked split screen comparing an AI helper app launch film (left) with its frame-matched remake for another product (right): pill name badge on pale sky gradient, app window push-in with cursor click, icon orbited by coloured squares, frosted menu-bar prompt, article morphing into image cards, glowing wordmark on black.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Remotion, React, CSS, SVG), suggested duration (12 s), aspect 16:9, difficulty 3/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Product UI / واجهات المنتج, Ads / إعلانات.
- [playbooks/product-ui.md](../../playbooks/product-ui.md)
- [playbooks/ads.md](../../playbooks/ads.md)

Category tactics:
* Recreate interface states as independent layers; animate meaningful cursor, tap, modal, scroll and focus interactions with consistent depth and realistic timings.
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
4. `python3 tools/kosif.py scaffold pm-notdwd-c2037d <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
