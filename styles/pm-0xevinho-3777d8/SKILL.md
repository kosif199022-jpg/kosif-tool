---
name: pm-0xevinho-3777d8
description: A fixed 20-second night pixel-art diorama by a lake (moon, pines, campfire, red banner, rippling reflections) where a hero faces a training dummy. The hero swaps classes every few seconds (blue wizard, red wizard, knight, hooded rogue) and casts spells whose names type into a top banner while damage numbers stack like a combat log. The final spell draws a green candlestick rally that crashes into red candles, the screen floods red, a huge negative figure and REKT appear and the dummy is left charred.
---

# KOSIF TOOL — Pixel wizard crypto animation / ساحر بكسل يضرب دمية التدريب حتى التصفية

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/0xevinho-3777d8
- Video: https://www.promptsmotion.com/__l5e/assets-v1/95d25350-da05-43b9-8399-f97dc7ea4365/c78ae64ddaf2134f.mp4
- Credit: @0xEvinho (https://x.com/0xEvinho/status/2103212966703436195)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-09-24 · credited model: Opus 5.5 · effort: Max
- Reference aspect: 16:9 (1920×1080)
- Creator's public prompt length: about 9 words (not reproduced here)
- Popularity rank on source library: #221

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
مشهد بكسل آرت ليلي ثابت مدته 20 ثانية بجانب بحيرة (قمر، صنوبر، نار مخيم، راية حمراء، انعكاسات ماء متموجة) يواجه فيه بطل دمية تدريب. يبدل البطل فئته كل بضع ثوانٍ (ساحر أزرق، ساحر أحمر، فارس، لص بقلنسوة) ويلقي تعاويذ تُكتب أسماؤها في شريط علوي بينما تتكدس أرقام الضرر كسجل قتال. التعويذة الأخيرة ترسم شموع صعود خضراء تنهار إلى شموع حمراء، يغمر الأحمر الشاشة ويظهر رقم سالب ضخم وكلمة REKT.

A fixed 20-second night pixel-art diorama by a lake (moon, pines, campfire, red banner, rippling reflections) where a hero faces a training dummy. The hero swaps classes every few seconds (blue wizard, red wizard, knight, hooded rogue) and casts spells whose names type into a top banner while damage numbers stack like a combat log. The final spell draws a green candlestick rally that crashes into red candles, the screen floods red, a huge negative figure and REKT appear and the dummy is left charred.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (HTML Canvas, Remotion), suggested duration (20 s), aspect 16:9, difficulty 3/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: creative motion.
- (no category playbook yet)

Category tactics:
* Develop original choreography from the reference; verify imagery before claiming a match.

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
4. `python3 tools/kosif.py scaffold pm-0xevinho-3777d8 <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
