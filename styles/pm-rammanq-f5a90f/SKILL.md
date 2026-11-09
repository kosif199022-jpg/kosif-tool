---
name: pm-rammanq-f5a90f
description: A 42-second square investment-app promo in twelve numbered chapters, each with a huge black-and-blue headline over a chart that builds live: floating logos, a rising portfolio line, sector donut, holdings bars, dividend calendar on blue, a 2008 crash test and Monte Carlo fan on navy, efficient frontier, tax-form flags, a phone with an AI answer, then the logo. Use to make a new video in this look (Product UI); address it by ID pm-rammanq-f5a90f.
---

# KOSIF TOOL — AllInvestView product promo / ترويج تطبيق استثمار: اثنا عشر فصلاً من الرسوم البيانية الحية

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/rammanq-f5a90f
- Video: https://www.promptsmotion.com/__l5e/assets-v1/7ebee9da-6a9f-4650-be3c-c371f36bcf84/178ee6744e6e0614.mp4
- Credit: @rammanq (https://x.com/rammanq/status/2103788796022034553)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-09-26 · credited model: Opus 5.5 · effort: Max
- Reference aspect: 1:1 (720×720)
- Creator's public prompt length: about 17 words (not reproduced here)
- Popularity rank on source library: #113

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
ترويج مربع مدته 42 ثانية لتطبيق متابعة الاستثمارات، مقسم إلى فصول مرقمة بعناوين ضخمة بلونين (أسود وأزرق): شعارات شركات تطفو حول كلمة واحدة، منحنى محفظة صاعد بشعارات على نقاطه، دائرة توزيع تتلون، أعمدة مقتنيات، تقويم أرباح على خلفية زرقاء، مقارنة بالسوق، اختبار أزمة 2008 على الأسود، محاكاة مونت كارلو، حد الكفاءة، خيارات وسندات، تقارير ضرائب بأعلام الدول، هاتف ومساعد ذكي، ثم الشعار.

A 42-second square investment-app promo in twelve numbered chapters, each with a huge black-and-blue headline over a chart that builds live: floating logos, a rising portfolio line, sector donut, holdings bars, dividend calendar on blue, a 2008 crash test and Monte Carlo fan on navy, efficient frontier, tax-form flags, a phone with an AI answer, then the logo.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Remotion, React, SVG, Web Audio), suggested duration (42 s), aspect 1:1, difficulty 4/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Product UI / واجهات المنتج, Charts / رسوم بيانية.
- [playbooks/product-ui.md](../../playbooks/product-ui.md)
- [playbooks/charts.md](../../playbooks/charts.md)

Category tactics:
* Recreate interface states as independent layers; animate meaningful cursor, tap, modal, scroll and focus interactions with consistent depth and realistic timings.
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
4. `python3 tools/kosif.py scaffold pm-rammanq-f5a90f <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
