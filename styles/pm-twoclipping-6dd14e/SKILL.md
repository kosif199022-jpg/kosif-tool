---
name: pm-twoclipping-6dd14e
description: A 20-second product promo: black words type in on a warm cream gradient and a product link is pasted into a white app window, then it flips to black for a grid of creator selfies under a counter, a scored hooks list, a curved 3D carousel of vertical ad cards, a phone beside a launch panel, huge white result numbers, an orange payoff word and the logo. Use to make a new video in this look (Product UI); address it by ID pm-twoclipping-6dd14e.
---

# KOSIF TOOL — UGC ad generator promo / إعلان أداة توليد إعلانات UGC: من رابط منتج إلى حملة منطلقة

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/twoclipping-6dd14e
- Video: https://www.promptsmotion.com/__l5e/assets-v1/3e757fa5-3f31-44f0-a299-2af1da6e8e29/284ad368d1e815db.mp4
- Credit: @twoclipping (https://x.com/twoclipping/status/2102554209166000267)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-09-23 · credited model: Opus 5.5 · effort: Max
- Reference aspect: 16:9 (1920×1080)
- Technologies named by the source: CSS, HTML
- Creator's public prompt length: about 444 words (not reproduced here)
- Popularity rank on source library: #7

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
إعلان منتج مدته 20 ثانية يبدأ بكلمات سوداء تُكتب كلمة بكلمة على خلفية كريمية دافئة ثم نافذة تطبيق بيضاء يُلصق فيها رابط منتج، وبعدها يتحول كل شيء إلى أسود: شبكة صور سيلفي لصانعي محتوى مع عدّاد تحليل، قائمة «هوكات» بدرجات، شريط دوّار ثلاثي الأبعاد من بطاقات فيديو عمودية، هاتف بجانب لوحة إطلاق حملة، أرقام نتائج ضخمة بالأبيض، ثم كلمة برتقالية وشعار التطبيق.

A 20-second product promo: black words type in on a warm cream gradient and a product link is pasted into a white app window, then it flips to black for a grid of creator selfies under a counter, a scored hooks list, a curved 3D carousel of vertical ad cards, a phone beside a launch panel, huge white result numbers, an orange payoff word and the logo.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Remotion, React, CSS, Three.js, Web Audio), suggested duration (20 s), aspect 16:9, difficulty 4/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Product UI / واجهات المنتج, Phone / هاتف, Kinetic type / تايبوغرافي متحرك, Photos / صور, 3D / ثلاثي الأبعاد, Ads / إعلانات.
- [playbooks/product-ui.md](../../playbooks/product-ui.md)
- [playbooks/phone.md](../../playbooks/phone.md)
- [playbooks/kinetic-type.md](../../playbooks/kinetic-type.md)
- [playbooks/photos.md](../../playbooks/photos.md)
- [playbooks/3d.md](../../playbooks/3d.md)
- [playbooks/ads.md](../../playbooks/ads.md)

Category tactics:
* Recreate interface states as independent layers; animate meaningful cursor, tap, modal, scroll and focus interactions with consistent depth and realistic timings.
* Use 3D or 2.5D phone layers with believable screen perspective, shadow, touch interaction, device rotation and safe crops.
* Animate readable words in timed beats; sync emphasis to spoken words; preserve Arabic shaping and RTL; never split joined letters.
* Use original or licensed photos in layered camera rigs with planar parallax, dynamic masks and depth-aware transitions.
* Choose real 3D only when the camera needs it; otherwise layer 2.5D; keep lighting and materials consistent across scenes.
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
4. `python3 tools/kosif.py scaffold pm-twoclipping-6dd14e <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
