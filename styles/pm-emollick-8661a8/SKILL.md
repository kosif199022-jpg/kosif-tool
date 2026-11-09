---
name: pm-emollick-8661a8
description: A 75 s recursion explainer that dives one screen deeper per TV genre (corporate explainer, green terminal, 8-bit game, nature doc, film noir, kids' TV, infomercial, gold trailer) down to a bare white HTML 'base case', then climbs back out in reverse while a breadcrumb bar on top tracks the depth. Use to make a new video in this look (Diagrams); address it by ID pm-emollick-8661a8.
---

# KOSIF TOOL — Recursion explained in genres / شرح التكرار الذاتي بفيديو يغوص داخل نفسه عبر أنواع تلفزيونية مختلفة

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/emollick-8661a8
- Video: https://www.promptsmotion.com/__l5e/assets-v1/05c4e4be-a136-4162-bb82-9711e11c486e/31ab0c99ba86325f.mp4
- Credit: @emollick (https://x.com/emollick/status/2103688362960019567)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-09-26 · credited model: Opus 5.5 · effort: Max
- Reference aspect: 16:9 (1920×1080)
- Creator's public prompt length: about 23 words (not reproduced here)
- Popularity rank on source library: #244

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
فيديو 75 ثانية يشرح التكرار الذاتي (Recursion) بأن ينزل عمقاً بعد عمق، وكل عمق بأسلوب تلفزيوني مختلف: عنوان جريء أحمر وأبيض، فيديو شرح شركاتي مسطّح، طرفية خضراء قديمة، لعبة 8-بت، وثائقي طبيعة عن السرخس، فيلم نوار بالأبيض والأسود، برنامج أطفال، إعلان تلفزيوني صاخب، تريلر سينمائي ذهبي، ثم صفحة HTML بيضاء عارية هي 'الحالة الأساسية'، قبل أن يصعد بالترتيب العكسي، مع شريط مكدس أعلى الشاشة يعرض العمق.

A 75 s recursion explainer that dives one screen deeper per TV genre (corporate explainer, green terminal, 8-bit game, nature doc, film noir, kids' TV, infomercial, gold trailer) down to a bare white HTML 'base case', then climbs back out in reverse while a breadcrumb bar on top tracks the depth.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Remotion, React, SVG, CSS, HTML Canvas), suggested duration (75 s), aspect 16:9, difficulty 5/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Diagrams / مخططات.
- [playbooks/diagrams.md](../../playbooks/diagrams.md)

Category tactics:
* Reveal nodes in causal order; draw SVG edges with dash offsets; move the camera between relationships deliberately.

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
4. `python3 tools/kosif.py scaffold pm-emollick-8661a8 <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
