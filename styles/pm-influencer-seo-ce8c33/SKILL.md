---
name: pm-influencer-seo-ce8c33
description: A 15-second violet-on-black showreel for a generative media platform: a code terminal types a generate call over a dot grid, a cut to a generated macro of violet petals with water drops, then giant words VIDEO, AUDIO and 3D whose letters are filled with generated footage, with index numbers, model names and a waveform, a tilted wall of generated thumbnails, a counter rolling to 1,000+, a huge number over a portrait, a prompt card with a generate button, and the logo on white.
---

# KOSIF TOOL — fal motion design showreel / ريل استعراضي لمنصة fal في 15 ثانية

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/influencer-seo-ce8c33
- Video: https://www.promptsmotion.com/__l5e/assets-v1/6bcbc0d9-0ebc-49c1-b9a3-f8e30674d3e0/ccede8070131b87e.mp4
- Credit: @influencer_seo (https://x.com/influencer_seo/status/2104827314400026936)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-09-29 · credited model: Opus 5.5 · effort: Max
- Reference aspect: 16:9 (1920×1080)
- Creator's public prompt length: about 32 words (not reproduced here)
- Popularity rank on source library: #87

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
ريل استعراضي مدته 15 ثانية بالبنفسجي على الأسود لمنصة وسائط توليدية: طرفية تكتب استدعاء توليد فوق شبكة نقاط، قطع إلى لقطة ماكرو مولدة لبتلات بنفسجية بقطرات ماء، ثم كلمات ضخمة VIDEO وAUDIO و3D تمتلئ حروفها بلقطات مولدة مع أرقام فهرسة وأسماء نماذج وموجة صوتية، جدار مائل من الصور المصغرة، عدّاد يصل إلى 1,000+، رقم ضخم فوق صورة شخصية، بطاقة أمر بزر توليد، وختام بالشعار على الأبيض.

A 15-second violet-on-black showreel for a generative media platform: a code terminal types a generate call over a dot grid, a cut to a generated macro of violet petals with water drops, then giant words VIDEO, AUDIO and 3D whose letters are filled with generated footage, with index numbers, model names and a waveform, a tilted wall of generated thumbnails, a counter rolling to 1,000+, a huge number over a portrait, a prompt card with a generate button, and the logo on white.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Remotion, React, WebGL), suggested duration (15 s), aspect 16:9, difficulty 5/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Charts / رسوم بيانية, Kinetic type / تايبوغرافي متحرك.
- [playbooks/charts.md](../../playbooks/charts.md)
- [playbooks/kinetic-type.md](../../playbooks/kinetic-type.md)

Category tactics:
* Use truthful data; animate counters, bars, lines and chart morphs whose labels stay accurate; keep axes and legends readable; reveal one insight at a time.
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
4. `python3 tools/kosif.py scaffold pm-influencer-seo-ce8c33 <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
