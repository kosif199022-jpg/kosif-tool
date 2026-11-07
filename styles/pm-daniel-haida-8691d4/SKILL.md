---
name: pm-daniel-haida-8691d4
description: A 14-second product film for a bookkeeping app: a gold app icon splits apart, then tilted navy dashboard cards float in dark 3D space with a huge profit figure and a gold line chart drawing on, a paper receipt that docks into a transactions list with green linked badges, an invoice flipping to paid with a yellow progress bar, a health ring filling to 94, and a gold wordmark end card. Use to make a new video in this look (Product UI); address it by ID pm-daniel-haida-8691d4.
---

# KOSIF TOOL — Taxtello bookkeeping app film / فيلم تطبيق محاسبة بلوحات داكنة مائلة ولمسات ذهبية

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/daniel-haida-8691d4
- Video: https://www.promptsmotion.com/__l5e/assets-v1/df78182e-9a17-452e-b8a6-325e4cea126c/2a7c361077060dc5.mp4
- Credit: @daniel_haida (https://x.com/daniel_haida/status/2104139720829636937)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-09-27 · credited model: Opus 5.5 · effort: Max
- Reference aspect: 16:9 (1920×1080)
- Technologies named by the source: CSS, D3, React, Remotion, SVG
- Creator's public prompt length: about 2082 words (not reproduced here)
- Popularity rank on source library: #24

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
فيلم منتج مدته 14 ثانية لتطبيق محاسبة: أيقونة ذهبية تنقسم، ثم لوحة أرباح كحلية مائلة في فضاء ثلاثي الأبعاد برقم ضخم ومنحنى ذهبي يُرسم، وإيصال ورقي يطفو ويُربط بقائمة الحركات بشارات خضراء، ثم حالة الفاتورة تتحول إلى «مدفوعة» وشريط تقدم أصفر، وحلقة نتيجة تمتلئ حتى 94، وينتهي بالشعار الذهبي وسطر وسم.

A 14-second product film for a bookkeeping app: a gold app icon splits apart, then tilted navy dashboard cards float in dark 3D space with a huge profit figure and a gold line chart drawing on, a paper receipt that docks into a transactions list with green linked badges, an invoice flipping to paid with a yellow progress bar, a health ring filling to 94, and a gold wordmark end card.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Remotion, React, SVG, CSS, Web Audio), suggested duration (14 s), aspect 16:9, difficulty 4/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Product UI / واجهات المنتج, Charts / رسوم بيانية, Ads / إعلانات.
- [playbooks/product-ui.md](../../playbooks/product-ui.md)
- [playbooks/charts.md](../../playbooks/charts.md)
- [playbooks/ads.md](../../playbooks/ads.md)

Category tactics:
* Recreate interface states as independent layers; animate meaningful cursor, tap, modal, scroll and focus interactions with consistent depth and realistic timings.
* Use truthful data; animate counters, bars, lines and chart morphs whose labels stay accurate; keep axes and legends readable; reveal one insight at a time.
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
4. `python3 tools/kosif.py scaffold pm-daniel-haida-8691d4 <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
