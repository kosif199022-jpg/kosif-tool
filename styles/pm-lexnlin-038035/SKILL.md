---
name: pm-lexnlin-038035
description: A ~14.5-second vertical ad on pure white where a single coral starburst travels as a brushstroke through black-and-white archive imagery (engravings, a dandelion, snowflakes, a horse ring, a marble bust, ink smoke, a rhinoceros) between one-word heavy-serif cues, then a drawn spiral leads to a closing line and the logo. Use to make a new video in this look (Kinetic type); address it by ID pm-lexnlin-038035.
---

# KOSIF TOOL — Engraving-style Claude ad / إعلان عمودي بالنقوش القديمة: نجمة الشعار تمر بين الأرشيف والكلمات

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/lexnlin-038035
- Video: https://www.promptsmotion.com/__l5e/assets-v1/00dd9421-f040-4496-8525-8ca813a81a00/7d336ebace422a92.mp4
- Credit: @LexnLin (https://x.com/LexnLin/status/2106101651010449796)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-10-02 · credited model: Opus 5.5 · effort: Max
- Reference aspect: 9:16 (1080×1920)
- Technologies named by the source: SVG
- Creator's public prompt length: about 168 words (not reproduced here)
- Popularity rank on source library: #137

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
إعلان عمودي مدته نحو 14.5 ثانية على أبيض ناصع: الشعار بنجمة برتقالية محمرة، ثم تتنقل النجمة كضربة فرشاة عبر صور أرشيفية بالأبيض والأسود (زهرة هندباء، رسم تشريحي، نقوش قديمة، رقاقات ثلج، حصان يعدو في دائرة، تمثال رخامي، دخان، كركدن منقوش)، وكلمات قصيرة بخط سيريف ثقيل، ثم دوامة خط تقود إلى عبارة الختام والشعار.

A ~14.5-second vertical ad on pure white where a single coral starburst travels as a brushstroke through black-and-white archive imagery (engravings, a dandelion, snowflakes, a horse ring, a marble bust, ink smoke, a rhinoceros) between one-word heavy-serif cues, then a drawn spiral leads to a closing line and the logo.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Remotion, React, SVG, Three.js), suggested duration (15 s), aspect 9:16, difficulty 3/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Kinetic type / تايبوغرافي متحرك, Photos / صور, Shapes / أشكال, Hand-drawn / رسم يدوي.
- [playbooks/kinetic-type.md](../../playbooks/kinetic-type.md)
- [playbooks/photos.md](../../playbooks/photos.md)
- [playbooks/shapes.md](../../playbooks/shapes.md)
- [playbooks/hand-drawn.md](../../playbooks/hand-drawn.md)

Category tactics:
* Animate readable words in timed beats; sync emphasis to spoken words; preserve Arabic shaping and RTL; never split joined letters.
* Use original or licensed photos in layered camera rigs with planar parallax, dynamic masks and depth-aware transitions.
* Build a geometric system; morph only compatible paths; animate scale, squash and stretch, rotation and easing with controlled geometry.
* Order stroke draw-on like a human hand would; keep imperfection deliberate; pace reveals to narration.

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
4. `python3 tools/kosif.py scaffold pm-lexnlin-038035 <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
