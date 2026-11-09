---
name: pm-kmasiff-cc72cb
description: A 20-second landscape SaaS ad alternating glowing dark violet and pale lavender grounds: a headline with a red-struck word, an email input card that types an address and steps through checks to an 85/100 score, six tinted glass result tiles, then a pill tab bar flipping through list upload, signup form, API, agent chat, integrations and terminal, ending on the logo and URL. Use to make a new video in this look (Product UI); address it by ID pm-kmasiff-cc72cb.
---

# KOSIF TOOL — Email verification tool promo / إعلان أداة تحقق من البريد بواجهات بيضاء نظيفة وخلفيات بنفسجية داكنة

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/kmasiff-cc72cb
- Video: https://www.promptsmotion.com/__l5e/assets-v1/507292ce-7d64-4245-87ec-5676dc6d028f/7abe92d602671e77.mp4
- Credit: @KmAsiff (https://x.com/KmAsiff/status/2103810247131549880)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-09-26 · credited model: Opus 5.5 · effort: High
- Reference aspect: 16:9 (1280×720)
- Creator's public prompt length: about 47 words (not reproduced here)
- Popularity rank on source library: #64

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
إعلان منتج أفقي (20 ثانية) يتبادل بين خلفية بنفسجية داكنة متوهجة وأخرى لافندر فاتحة: عنوان بكلمة مشطوبة بالأحمر، بطاقة إدخال بريد تُكتب فيها عنوان وخطوات فحص تتقدم ثم نتيجة 85/100، ست بطاقات زجاجية ملونة لأنواع النتائج، ثم شريط تبويبات يقلب بين رفع ملف وحماية نموذج تسجيل وطلب برمجي ومحادثة وكيل ومخطط تكاملات وطرفية، ويختم بثلاث مزايا والشعار والرابط.

A 20-second landscape SaaS ad alternating glowing dark violet and pale lavender grounds: a headline with a red-struck word, an email input card that types an address and steps through checks to an 85/100 score, six tinted glass result tiles, then a pill tab bar flipping through list upload, signup form, API, agent chat, integrations and terminal, ending on the logo and URL.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Remotion, React, CSS), suggested duration (20 s), aspect 16:9, difficulty 3/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Product UI / واجهات المنتج, Charts / رسوم بيانية, Characters / شخصيات.
- [playbooks/product-ui.md](../../playbooks/product-ui.md)
- [playbooks/charts.md](../../playbooks/charts.md)
- [playbooks/characters.md](../../playbooks/characters.md)

Category tactics:
* Recreate interface states as independent layers; animate meaningful cursor, tap, modal, scroll and focus interactions with consistent depth and realistic timings.
* Use truthful data; animate counters, bars, lines and chart morphs whose labels stay accurate; keep axes and legends readable; reveal one insight at a time.
* Use consistent model sheets and rigs, key poses, anticipation and follow-through, readable expressions and walk cycles.

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
4. `python3 tools/kosif.py scaffold pm-kmasiff-cc72cb <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
