---
name: pm-francoxavier33-d2dfd2
description: A 28-second vertical app ad on a cream-to-peach gradient: big serif headlines type in with a caret and an orange italic word on a brush highlight, a phone agenda rises in, task and 'done while you slept' cards pop, helper cards stack, helpers join a group thread one by one, a grocery list ticks off under food photos, a benefits list, then the app icon. Use to make a new video in this look (Product UI); address it by ID pm-francoxavier33-d2dfd2.
---

# KOSIF TOOL — Parenting app hype video / إعلان تطبيق للأهل: مساعدون أذكياء بعناوين سيريف دافئة

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/francoxavier33-d2dfd2
- Video: https://www.promptsmotion.com/__l5e/assets-v1/f3e74b5e-895e-4785-ad2e-9c0eed5afe68/afbed29764bc7c12.mp4
- Credit: @francoxavier33 (https://x.com/francoxavier33/status/2103486218323341663)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-09-25 · credited model: Opus 5.5 · effort: Max
- Reference aspect: other (886×1920)
- Creator's public prompt length: about 7 words (not reproduced here)
- Popularity rank on source library: #190

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
إعلان عمودي مدته 28 ثانية لتطبيق مساعدين للأهل على خلفية كريمية بتدرج خوخي: عناوين سيريف كبيرة تُكتب بمؤشر وكلمة مائلة برتقالية مسطرة بفرشاة، هاتف بشاشة يوم الجمعة يدخل من الأسفل، إشعار «تم» وشارة «أنجزت وأنت نائم»، بطاقات مساعدين تتراص، محادثة جماعية ينضم إليها المساعدون واحداً تلو الآخر، قائمة تسوق تُشطب بنودها وصور طعام، قائمة فوائد، ثم أيقونة التطبيق.

A 28-second vertical app ad on a cream-to-peach gradient: big serif headlines type in with a caret and an orange italic word on a brush highlight, a phone agenda rises in, task and 'done while you slept' cards pop, helper cards stack, helpers join a group thread one by one, a grocery list ticks off under food photos, a benefits list, then the app icon.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Remotion, React, CSS, Web Audio), suggested duration (28 s), aspect 886x1920, difficulty 3/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Product UI / واجهات المنتج, Phone / هاتف, Kinetic type / تايبوغرافي متحرك, Photos / صور, Ads / إعلانات.
- [playbooks/product-ui.md](../../playbooks/product-ui.md)
- [playbooks/phone.md](../../playbooks/phone.md)
- [playbooks/kinetic-type.md](../../playbooks/kinetic-type.md)
- [playbooks/photos.md](../../playbooks/photos.md)
- [playbooks/ads.md](../../playbooks/ads.md)

Category tactics:
* Recreate interface states as independent layers; animate meaningful cursor, tap, modal, scroll and focus interactions with consistent depth and realistic timings.
* Use 3D or 2.5D phone layers with believable screen perspective, shadow, touch interaction, device rotation and safe crops.
* Animate readable words in timed beats; sync emphasis to spoken words; preserve Arabic shaping and RTL; never split joined letters.
* Use original or licensed photos in layered camera rigs with planar parallax, dynamic masks and depth-aware transitions.
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
4. `python3 tools/kosif.py scaffold pm-francoxavier33-d2dfd2 <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
