---
name: pm-lemomo-ai-0d9cff
description: A ~71-second whiteboard tutorial on one large canvas: a visible marker hand-writes the title and draws boxes, arrows and a timeline while the camera pans and zooms across pasted screenshots of a style gallery site, a terminal and an AI chat, with a small orange pixel mascot, red-circled step numbers and bilingual subtitles, ending on a zoom-out that reveals the whole board as a map. Use to make a new video in this look (Diagrams); address it by ID pm-lemomo-ai-0d9cff.
---

# KOSIF TOOL — Whiteboard skill tutorial / شرح سبورة بيضاء لطريقة استخدام أداة صنع الأفلام مع لقطات شاشة

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/lemomo-ai-0d9cff
- Video: https://www.promptsmotion.com/__l5e/assets-v1/af9fff60-7901-4c6b-9389-c6906cdf3f03/da2ccfaad0ffbdde.mp4
- Credit: @lemomo_ai (https://x.com/lemomo_ai/status/2104070024575242622)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-09-27 · credited model: Opus 5.5 · effort: Max
- Reference aspect: 16:9 (1920×1080)
- Creator's public prompt length: about 27 words (not reproduced here)
- Popularity rank on source library: #159

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
فيديو تعليمي مدته نحو 71 ثانية بأسلوب سبورة بيضاء ممتدة: قلم ظاهر يكتب العنوان بخط يد ويرسم مربعات وأسهماً وخط زمن، بينما تجول الكاميرا فوق لوحة واحدة كبيرة ملصق عليها لقطات شاشة لموقع معرض الأساليب ونافذة الطرفية ومحادثة الذكاء الاصطناعي، مع تميمة بكسلية برتقالية صغيرة، وخطوات مرقمة داخل دوائر حمراء، وترجمة ثنائية اللغة أسفل الشاشة، وتنتهي بابتعاد يكشف اللوحة كلها كخريطة.

A ~71-second whiteboard tutorial on one large canvas: a visible marker hand-writes the title and draws boxes, arrows and a timeline while the camera pans and zooms across pasted screenshots of a style gallery site, a terminal and an AI chat, with a small orange pixel mascot, red-circled step numbers and bilingual subtitles, ending on a zoom-out that reveals the whole board as a map.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Remotion, React, SVG, CSS), suggested duration (71 s), aspect 16:9, difficulty 3/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Diagrams / مخططات, Characters / شخصيات.
- [playbooks/diagrams.md](../../playbooks/diagrams.md)
- [playbooks/characters.md](../../playbooks/characters.md)

Category tactics:
* Reveal nodes in causal order; draw SVG edges with dash offsets; move the camera between relationships deliberately.
* Use consistent model sheets and rigs, key poses, anticipation and follow-through, readable expressions and walk cycles.

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
4. `python3 tools/kosif.py scaffold pm-lemomo-ai-0d9cff <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
