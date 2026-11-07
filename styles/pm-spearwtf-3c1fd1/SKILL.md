---
name: pm-spearwtf-3c1fd1
description: A 30 s 16:9 pitch ad that opens on a soft blue button on white being clicked, then cuts to dark, shallow-focus 3D close-ups (red arcade button, rainbow light tunnel, slot reels, coin, stadium, LED board, dice, flying forms), each tagged with a heavy italic uppercase word beside a four-stripe logo, ending on an RGB-split glitching wordmark and a yellow button. Use to make a new video in this look (Ads); address it by ID pm-spearwtf-3c1fd1.
---

# KOSIF TOOL — Chain.wtf pitch video / إعلان عرض جريء لمنصة مراهنات بلقطات ثلاثية الأبعاد سينمائية وتشويش ألوان

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/spearwtf-3c1fd1
- Video: https://www.promptsmotion.com/__l5e/assets-v1/f835f58f-4502-4b5b-9506-4400a7a58320/34feada745273718.mp4
- Credit: @SPEARwtf (https://x.com/SPEARwtf/status/2103857153308029058)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-09-26 · credited model: Opus 5.5 · effort: Max
- Reference aspect: 16:9 (1920×1080)
- Creator's public prompt length: about 7 words (not reproduced here)
- Popularity rank on source library: #162

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
إعلان 16:9 مدته 30 ثانية يبدأ بزر أزرق ناعم على أبيض يُضغط، ثم يقطع إلى ظلام سينمائي بلقطات ثلاثية الأبعاد قريبة بعمق ميدان ضحل (زر أحمر كبير، نفق ضوء بقوس قزح، بكرات آلة قمار، عملة تدور، ملعب، لوحة LED، نرد، استمارات تتطاير) مع عنوان مائل عريض لكل فئة بجانب شعار من أربعة خطوط ملونة، وينتهي بشعار يتشوش بانفصال ألوان وخطوط سرعة وزر أصفر.

A 30 s 16:9 pitch ad that opens on a soft blue button on white being clicked, then cuts to dark, shallow-focus 3D close-ups (red arcade button, rainbow light tunnel, slot reels, coin, stadium, LED board, dice, flying forms), each tagged with a heavy italic uppercase word beside a four-stripe logo, ending on an RGB-split glitching wordmark and a yellow button.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Remotion, React, Three.js, WebGL, CSS), suggested duration (30 s), aspect 16:9, difficulty 5/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Ads / إعلانات, 3D / ثلاثي الأبعاد, Kinetic type / تايبوغرافي متحرك.
- [playbooks/ads.md](../../playbooks/ads.md)
- [playbooks/3d.md](../../playbooks/3d.md)
- [playbooks/kinetic-type.md](../../playbooks/kinetic-type.md)

Category tactics:
* Hook in the first second; one feature per beat; clear price or call-to-action card; brand-consistent logo reveal.
* Choose real 3D only when the camera needs it; otherwise layer 2.5D; keep lighting and materials consistent across scenes.
* Animate readable words in timed beats; sync emphasis to spoken words; preserve Arabic shaping and RTL; never split joined letters.

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
4. `python3 tools/kosif.py scaffold pm-spearwtf-3c1fd1 <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
