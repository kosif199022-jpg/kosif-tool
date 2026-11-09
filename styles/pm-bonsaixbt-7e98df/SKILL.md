---
name: pm-bonsaixbt-7e98df
description: A 20-second 4:5 vertical piece in deep violet: a fixed two-tone headline, a huge frame counter climbing to 600, a five-item pipeline checklist ticking green, a terminal at the bottom typing commands, and in the centre a neon tunnel of nested rectangles from which a UI card emerges, gets clicked and exports, then a looping workflow ring, ending on a '20 s = 600 frames' card. Use to make a new video in this look (Kinetic type); address it by ID pm-bonsaixbt-7e98df.
---

# KOSIF TOOL — Frame-accurate edits with Remotion / شرح التحرير بدقة الإطار داخل نفق إطارات

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/bonsaixbt-7e98df
- Video: https://www.promptsmotion.com/__l5e/assets-v1/3adbd36e-c62e-45f1-9a77-b9916f422378/6b7b41882b9bc8a6.mp4
- Credit: unknown (https://x.com/bonsaixbt/status/2113751074414744061)
- Source type: Skill · Origin: PromptsMotion
- Published on source: 2026-10-23
- Reference aspect: 4:5 (1080×1334)
- Technologies named by the source: Remotion
- Creator's public prompt length: about 114 words (not reproduced here)
- Popularity rank on source library: #90

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
مقطع عمودي 4:5 مدته 20 ثانية بالبنفسجي الداكن: عنوان ثابت أعلاه وعداد إطارات ضخم يصعد من 0 إلى 600، قائمة خطوات من خمسة بنود تُعلَّم بالأخضر، طرفية أسفل تُكتب فيها أوامر، وفي الوسط نفق مستطيلات نيون بنفسجية تخرج منه بطاقة واجهة تُضغط وتصدّر، ثم حلقة خطوات العمل، وينتهي بـ«20 ثانية = 600 إطار».

A 20-second 4:5 vertical piece in deep violet: a fixed two-tone headline, a huge frame counter climbing to 600, a five-item pipeline checklist ticking green, a terminal at the bottom typing commands, and in the centre a neon tunnel of nested rectangles from which a UI card emerges, gets clicked and exports, then a looping workflow ring, ending on a '20 s = 600 frames' card.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Remotion, React, CSS, SVG), suggested duration (20 s), aspect 4:5, difficulty 3/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Kinetic type / تايبوغرافي متحرك, Code / كود.
- [playbooks/kinetic-type.md](../../playbooks/kinetic-type.md)
- [playbooks/code.md](../../playbooks/code.md)

Category tactics:
* Animate readable words in timed beats; sync emphasis to spoken words; preserve Arabic shaping and RTL; never split joined letters.
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
4. `python3 tools/kosif.py scaffold pm-bonsaixbt-7e98df <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
