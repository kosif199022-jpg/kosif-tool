---
name: dua
description: A ~15 s vertical 9:16 reel: one spoken dua phrase = one shot = one on-screen line. Warm low-key shots (Quran, roses, incense, candles) cut on each phrase onset with blur, mirror and zoom transitions, under a persistent white Thuluth title «الجُمُعَة», the date, a gold subtitle and a white dua line with a tight dark halo.
---

# KOSIF TOOL — الدعاء / الدعاء — ريل دعاء ليلة الجمعة

## Primary motion reference (المرجع)
- Page: https://github.com/kosif199022-jpg/kosif-tool/tree/main/styles/dua
- Video: see source page
- Credit: KOSIF (measured from an owner-supplied reel)
- Source type: Style · Origin: KOSIF original style
- Reference aspect: 9:16 (1080×1920)

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
ريل عمودي 9:16 مدته نحو 15 ثانية: عبارة دعاء واحدة = لقطة واحدة = سطر واحد على الشاشة. لقطات دافئة منخفضة الإضاءة (مصحف، ورد، مبخرة، شموع) تتبدل على بداية كل عبارة بانتقالات ضبابية ومرآة وزوم، بينما يبقى فوقها عنوان «الجُمُعَة» بخط ثلث أبيض وتاريخ اليوم وسطر ذهبي «ليلة جمعة مبـــاركة» وسطر الدعاء الأبيض بهالة داكنة ضيقة.

A ~15 s vertical 9:16 reel: one spoken dua phrase = one shot = one on-screen line. Warm low-key shots (Quran, roses, incense, candles) cut on each phrase onset with blur, mirror and zoom transitions, under a persistent white Thuluth title «الجُمُعَة», the date, a gold subtitle and a white dua line with a tight dark halo.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (HTML Canvas, CSS), suggested duration (15.4 s), aspect 9:16, difficulty 3/5.

## Ready-made kit (عدة جاهزة)
This style ships a measured spec and a working builder: read [kit/README.md](kit/README.md) first, then [ANALYSIS.md](ANALYSIS.md) and the machine-readable spec `dua.style.json`. Prefer the kit over rebuilding the look from scratch; it reproduces the measured timing, layout, colours and transitions with the user's own clips and voice.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Kinetic type / تايبوغرافي متحرك, Photos / صور.
- [playbooks/kinetic-type.md](../../playbooks/kinetic-type.md)
- [playbooks/photos.md](../../playbooks/photos.md)

Category tactics:
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
4. `python3 tools/kosif.py scaffold dua <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
