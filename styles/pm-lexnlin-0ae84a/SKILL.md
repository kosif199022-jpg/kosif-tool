---
name: pm-lexnlin-0ae84a
description: A ~47 s launch film for a coding-agent UI skill: a typed line with an orange caret on pale paper, then a fast tour of dashboards (portfolio tracker, sales pipeline, bakery back office, mobile leave planner, household budget, café site) framed by orange corner brackets and tiny annotation tags, punctuated by short headlines whose last word turns orange, ending on the logo and an install command. Use to make a new video in this look (Product UI); address it by ID pm-lexnlin-0ae84a.
---

# KOSIF TOOL — TasteSkill dashboard launch film / فيلم إطلاق مهارة تصميم لوحات تحكم بذوق

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/lexnlin-0ae84a
- Video: https://www.promptsmotion.com/__l5e/assets-v1/57fcf626-af08-4e70-a4ea-a822dc11acfd/6953bc5fc952b2e3.mp4
- Credit: unknown (https://x.com/LexnLin/status/2112674349132194185)
- Source type: Skill · Origin: PromptsMotion
- Published on source: 2026-10-20
- Reference aspect: 16:9 (1920×1080)
- Creator's public prompt length: about 108 words (not reproduced here)
- Popularity rank on source library: #147

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
فيلم إطلاق مدته نحو 47 ثانية لمهارة وكيل برمجي تبني الواجهات: سطر كتابة بمؤشر برتقالي على ورق فاتح، ثم جولة سريعة في لوحات تحكم حقيقية (متتبع محافظ، خط مبيعات، مكتب خلفي لمخبز، مخطط إجازات على الهاتف، ميزانية منزلية، موقع مقهى) بأقواس تحديد برتقالية ووسوم تعليق صغيرة، تتخللها عناوين بيضاء قصيرة كلمتها الأخيرة برتقالية، وتنتهي بشعار المهارة وأمر التثبيت.

A ~47 s launch film for a coding-agent UI skill: a typed line with an orange caret on pale paper, then a fast tour of dashboards (portfolio tracker, sales pipeline, bakery back office, mobile leave planner, household budget, café site) framed by orange corner brackets and tiny annotation tags, punctuated by short headlines whose last word turns orange, ending on the logo and an install command.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Remotion, React, CSS), suggested duration (47 s), aspect 16:9, difficulty 4/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Product UI / واجهات المنتج, Charts / رسوم بيانية, Characters / شخصيات, Code / كود.
- [playbooks/product-ui.md](../../playbooks/product-ui.md)
- [playbooks/charts.md](../../playbooks/charts.md)
- [playbooks/characters.md](../../playbooks/characters.md)
- [playbooks/code.md](../../playbooks/code.md)

Category tactics:
* Recreate interface states as independent layers; animate meaningful cursor, tap, modal, scroll and focus interactions with consistent depth and realistic timings.
* Use truthful data; animate counters, bars, lines and chart morphs whose labels stay accurate; keep axes and legends readable; reveal one insight at a time.
* Use consistent model sheets and rigs, key poses, anticipation and follow-through, readable expressions and walk cycles.
* Write genuine time-varying vector, Canvas, React or WebGL motion; seed all randomness; never a slideshow of stills.

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
4. `python3 tools/kosif.py scaffold pm-lexnlin-0ae84a <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
