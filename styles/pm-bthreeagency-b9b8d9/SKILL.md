---
name: pm-bthreeagency-b9b8d9
description: A short (about 11 s) near-4:3 mobile UI clip: a phone centred on a light grey canvas shows a 'Badges' screen with a navy sky, a gold hexagon badge whose sunrise-and-river art draws in, then a gold ring burst, falling sparkles and the badge name fading up; the camera pushes in as a yellow hand cursor taps the badge so it pulses and gleams, with a row of other badges, one locked, below. Use to make a new video in this look (Kinetic type); address it by ID pm-bthreeagency-b9b8d9.
---

# KOSIF TOOL — Badge unlock screen animation / شاشة فتح شارة إنجاز ذهبية في تطبيق جوال مع بريق متساقط ومؤشر تفاعلي

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/bthreeagency-b9b8d9
- Video: https://www.promptsmotion.com/__l5e/assets-v1/2a5831e4-5d37-47fd-a3ef-c729df7a636d/80a2dbd149970991.mp4
- Credit: @BThreeAgency (https://x.com/BThreeAgency/status/2103739079745827092)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-09-26 · credited model: Opus 5.5 · effort: Max
- Reference aspect: 4:3 (1408×1080)
- Creator's public prompt length: about 73 words (not reproduced here)
- Popularity rank on source library: #127

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
لقطة واجهة جوال قصيرة (نحو 11 ثانية) بنسبة قريبة من 4:3: هاتف في المنتصف على خلفية رمادية فاتحة يعرض صفحة «الشارات» بسماء كحلية، شارة سداسية ذهبية يُرسم داخلها شروق ونهر ثم تنفجر حلقة ذهبية وبريق يتساقط ويظهر اسم الشارة، ثم تقترب الكاميرا ومؤشر يد أصفر يلمس الشارة فتنبض وتلمع، وتحتها صف شارات أخرى بعضها مقفل.

A short (about 11 s) near-4:3 mobile UI clip: a phone centred on a light grey canvas shows a 'Badges' screen with a navy sky, a gold hexagon badge whose sunrise-and-river art draws in, then a gold ring burst, falling sparkles and the badge name fading up; the camera pushes in as a yellow hand cursor taps the badge so it pulses and gleams, with a row of other badges, one locked, below.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (React, CSS, HTML Canvas, Remotion), suggested duration (11 s), aspect 1408:1080, difficulty 3/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Kinetic type / تايبوغرافي متحرك, Particles / جسيمات.
- [playbooks/kinetic-type.md](../../playbooks/kinetic-type.md)
- [playbooks/particles.md](../../playbooks/particles.md)

Category tactics:
* Animate readable words in timed beats; sync emphasis to spoken words; preserve Arabic shaping and RTL; never split joined letters.
* Use deterministic seeded particles with explicit emitters, fields, attraction and decay that carry story meaning, not decoration.

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
4. `python3 tools/kosif.py scaffold pm-bthreeagency-b9b8d9 <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
