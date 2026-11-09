---
name: pm-stefan-3d-ai-c5f9fd
description: A silent ~77-second showcase of a cartoon-fantasy MMORPG: a split-screen opener, a character creator cycling races and classes beside a parchment panel, over-the-shoulder gameplay in wheat fields, a graveyard and a town square, then Unity editor and AI-terminal captures, crude low-poly prototypes, and a closing grid of overhead world maps. Use to make a new video in this look (Photos); address it by ID pm-stefan-3d-ai-c5f9fd.
---

# KOSIF TOOL — Old-school MMORPG built with Opus 5.5 / عرض لعبة MMORPG كلاسيكية: من اختيار الشخصية إلى كواليس البناء

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/stefan-3d-ai-c5f9fd
- Video: https://www.promptsmotion.com/__l5e/assets-v1/a8ee5003-bb48-4670-a7d6-31bc10edb740/video.mp4
- Credit: unknown (https://x.com/Stefan_3D_AI/status/2103778468660162615)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-09-26 · credited model: Opus 5.5 · effort: Max
- Reference aspect: 16:9 (1280×720)
- Creator's public prompt length: about 99 words (not reproduced here)
- Popularity rank on source library: #71

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
فيلم عرض مدته نحو 77 ثانية بلا صوت للعبة تقمص أدوار جماعية بأسلوب فانتازي كرتوني ملون: يبدأ بشاشة منقسمة بين منصة اختيار الشخصية وعالم اللعب، ثم شاشة إنشاء الشخصية تتنقل بين الأعراق والفئات مع لوحة رقّ وصفية، ثم لقطات لعب بكاميرا خلف الكتف في حقول قمح ومقبرة ليلية وساحة مدينة بنافورة سحرية، ثم لقطات من محرر Unity وطرفية الذكاء الاصطناعي، ونسخ بدائية مبكرة منخفضة المضلعات، وأخيراً شبكة خرائط علوية للعالم.

A silent ~77-second showcase of a cartoon-fantasy MMORPG: a split-screen opener, a character creator cycling races and classes beside a parchment panel, over-the-shoulder gameplay in wheat fields, a graveyard and a town square, then Unity editor and AI-terminal captures, crude low-poly prototypes, and a closing grid of overhead world maps.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Remotion, React), suggested duration (77 s), aspect 16:9, difficulty 2/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Photos / صور, Music / موسيقى, Code / كود.
- [playbooks/photos.md](../../playbooks/photos.md)
- [playbooks/music.md](../../playbooks/music.md)
- [playbooks/code.md](../../playbooks/code.md)

Category tactics:
* Use original or licensed photos in layered camera rigs with planar parallax, dynamic masks and depth-aware transitions.
* Cut and accent on measured beats; keep narration intelligible; duck music under voice; deliver at -14 LUFS.
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
4. `python3 tools/kosif.py scaffold pm-stefan-3d-ai-c5f9fd <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
