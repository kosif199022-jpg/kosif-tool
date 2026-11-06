---
name: pm-davidmarcus-a28a60
description: A 23-second vertical social promo in quiet Swiss style: large black sans headlines on an off-white faint grid with a fixed page header and an underlined section tab, flipping at times to charcoal pages; giant currency codes swap above a country counter, a settlement line fills between two currencies, a product list stacks and dims, a terminal types a payment call, and it ends on logo and URL. Use to make a new video in this look (Kinetic type); address it by ID pm-davidmarcus-a28a60.
---

# KOSIF TOOL — Lightspark social promo video / ترويج سويسري بسيط لبنية دفع عالمية بالطول

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/davidmarcus-a28a60
- Video: https://www.promptsmotion.com/__l5e/assets-v1/a195f260-68f2-46e4-92a2-a061e9a7c8d0/6e920d9e1242adad.mp4
- Credit: @davidmarcus (https://x.com/davidmarcus/status/2103275618045686217)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-09-25 · credited model: Opus 5.5 · effort: Max
- Reference aspect: 9:16 (1080×1920)
- Creator's public prompt length: about 20 words (not reproduced here)
- Popularity rank on source library: #84

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
ترويج اجتماعي عمودي مدته 23 ثانية بأسلوب سويسري هادئ: عناوين سوداء كبيرة بخط بلا زوائد على خلفية أوف وايت بشبكة باهتة، مع رأس صفحة ثابت وتبويب قسم مسطّر، تتبدل أحياناً إلى صفحات فحمية؛ رموز عملات ضخمة تتبدل مع عداد دول، خط تسوية بين عملتين يمتلئ، قائمة منتجات تتكدس وتخفت، طرفية كود تكتب أمر دفع، وختام بالشعار والرابط.

A 23-second vertical social promo in quiet Swiss style: large black sans headlines on an off-white faint grid with a fixed page header and an underlined section tab, flipping at times to charcoal pages; giant currency codes swap above a country counter, a settlement line fills between two currencies, a product list stacks and dims, a terminal types a payment call, and it ends on logo and URL.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Remotion, React, CSS), suggested duration (23 s), aspect 9:16, difficulty 2/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Kinetic type / تايبوغرافي متحرك, Product UI / واجهات المنتج.
- [playbooks/kinetic-type.md](../../playbooks/kinetic-type.md)
- [playbooks/product-ui.md](../../playbooks/product-ui.md)

Category tactics:
* Animate readable words in timed beats; sync emphasis to spoken words; preserve Arabic shaping and RTL; never split joined letters.
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
4. `python3 tools/kosif.py scaffold pm-davidmarcus-a28a60 <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
