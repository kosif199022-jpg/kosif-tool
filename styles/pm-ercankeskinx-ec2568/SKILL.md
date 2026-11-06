---
name: pm-ercankeskinx-ec2568
description: A 30-second screen capture of one web page scrolling through five sections, each with its own look: an architecture project index where the photo swaps as each name highlights, a product page for a recorder with live cards (battery count, waveform), a night-train route map drawing across a dark plum panel, a fanned deck of paint swatches that rotates, and a deep green footer with a giant wordmark. Use to make a new video in this look (Product UI); address it by ID pm-ercankeskinx-ec2568.
---

# KOSIF TOOL — Five scroll-based sections / خمسة أقسام ويب تتحرك مع التمرير: عرض تصميم تفاعلي

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/ercankeskinx-ec2568
- Video: https://www.promptsmotion.com/__l5e/assets-v1/00159639-d925-4498-a2fb-9e6ae8ca58fc/57ff5d70f234853d.mp4
- Credit: @ercankeskinx (https://x.com/ercankeskinx/status/2102995443818897906)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-09-24 · credited model: Opus 5.5 · effort: Max
- Reference aspect: other (1920×972)
- Creator's public prompt length: about 12 words (not reproduced here)
- Popularity rank on source library: #93

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
تسجيل شاشة مدته 30 ثانية لصفحة ويب واحدة تمر عبر خمسة أقسام بأسلوب مختلف لكل منها: فهرس مشاريع معمارية تتبدل صورته مع تمييز كل اسم، صفحة منتج لجهاز تسجيل ببطاقات حية (بطارية، موجة صوتية)، خريطة رحلة قطار ليلي تُرسم على خلفية برقوقية داكنة، مروحة عينات ألوان دهان تدور، ثم تذييل أخضر داكن بكلمة علامة ضخمة.

A 30-second screen capture of one web page scrolling through five sections, each with its own look: an architecture project index where the photo swaps as each name highlights, a product page for a recorder with live cards (battery count, waveform), a night-train route map drawing across a dark plum panel, a fanned deck of paint swatches that rotates, and a deep green footer with a giant wordmark.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (React, CSS, GSAP, SVG), suggested duration (30 s), aspect 1920x972, difficulty 3/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Product UI / واجهات المنتج, Kinetic type / تايبوغرافي متحرك, Photos / صور.
- [playbooks/product-ui.md](../../playbooks/product-ui.md)
- [playbooks/kinetic-type.md](../../playbooks/kinetic-type.md)
- [playbooks/photos.md](../../playbooks/photos.md)

Category tactics:
* Recreate interface states as independent layers; animate meaningful cursor, tap, modal, scroll and focus interactions with consistent depth and realistic timings.
* Animate readable words in timed beats; sync emphasis to spoken words; preserve Arabic shaping and RTL; never split joined letters.
* Use original or licensed photos in layered camera rigs with planar parallax, dynamic masks and depth-aware transitions.

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
4. `python3 tools/kosif.py scaffold pm-ercankeskinx-ec2568 <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
