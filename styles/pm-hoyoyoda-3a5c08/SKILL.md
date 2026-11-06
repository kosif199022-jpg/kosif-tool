---
name: pm-hoyoyoda-3a5c08
description: A 12-second looping pixel-art harvest-moon night: a huge yellow moon with a rabbit pounding rice cakes, a violet starry sky, traditional houses with lit windows and lantern strings, tiny hanbok figures, a table filling with rice cakes, pixel rainbows from 4 s, a Korean and English greeting typing in, and a coloured stripe wipe that resets the loop. Use to make a new video in this look (Characters); address it by ID pm-hoyoyoda-3a5c08.
---

# KOSIF TOOL — Chuseok pixel night scene / ليلة تشوسوك بالبكسل: قمر الأرنب ومهرجان الفوانيس

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/hoyoyoda-3a5c08
- Video: https://www.promptsmotion.com/__l5e/assets-v1/b1aa8c8e-4509-4c7a-9079-d6dc1f10004a/6a8a13c844a6c95f.mp4
- Credit: @hoyoyoda (https://x.com/hoyoyoda/status/2103400046922543147)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-09-25 · credited model: Opus 5.5 · effort: Max
- Reference aspect: 16:9 (1920×1080)
- Creator's public prompt length: about 13 words (not reproduced here)
- Popularity rank on source library: #36

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
لوحة بكسل آرت متحركة مدتها 12 ثانية لليلة عيد الحصاد الكوري: قمر بدر أصفر ضخم في الوسط يدق فيه أرنب كعك الأرز، سماء بنفسجية بنجوم متلألئة وغيوم، صف من البيوت التقليدية بنوافذ مضيئة وأحبال فوانيس ملونة، شخصيات صغيرة بالهانبوك، طاولة يتراكم عليها الكعك، أقواس قزح من خطوط بكسل تظهر عند الثانية 4، ثم عنوان بالكورية والإنجليزية وستارة أشرطة ملونة تغلق الحلقة.

A 12-second looping pixel-art harvest-moon night: a huge yellow moon with a rabbit pounding rice cakes, a violet starry sky, traditional houses with lit windows and lantern strings, tiny hanbok figures, a table filling with rice cakes, pixel rainbows from 4 s, a Korean and English greeting typing in, and a coloured stripe wipe that resets the loop.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (HTML Canvas, React, Remotion), suggested duration (12 s), aspect 16:9, difficulty 3/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Characters / شخصيات, Particles / جسيمات, Kinetic type / تايبوغرافي متحرك.
- [playbooks/characters.md](../../playbooks/characters.md)
- [playbooks/particles.md](../../playbooks/particles.md)
- [playbooks/kinetic-type.md](../../playbooks/kinetic-type.md)

Category tactics:
* Use consistent model sheets and rigs, key poses, anticipation and follow-through, readable expressions and walk cycles.
* Use deterministic seeded particles with explicit emitters, fields, attraction and decay that carry story meaning, not decoration.
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
4. `python3 tools/kosif.py scaffold pm-hoyoyoda-3a5c08 <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
