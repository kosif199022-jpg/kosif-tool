---
name: pm-jake11moran-a269c4
description: A warm, ink-outlined cartoon of about 53 seconds in a single fixed office: the agent is an orange box character with dot eyes and stubby arms behind a desk with a brass plaque. It starts asleep at night, a push-in to the monitor types the session start, then user messages arrive as paper airplanes that unfold into handwritten notes; the agent reacts with expressions while the monitor shows code, an image, a progress bar or a green check, rewards pile up on its head and the window cycles from day to night.
---

# KOSIF TOOL — Animated agent session story / حكاية جلسة الوكيل البرمجي

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/jake11moran-a269c4
- Video: https://www.promptsmotion.com/__l5e/assets-v1/d915b4b3-3f8d-4c54-a705-1214789e7328/df4cf983a810e9a5.mp4
- Credit: @jake11moran (https://x.com/jake11moran/status/2103247490237825416)
- Source type: Skill · Origin: PromptsMotion
- Published on source: 2026-09-24 · credited model: Opus 5.5 · effort: Max
- Reference aspect: 16:9 (1920×1080)
- Creator's public prompt length: about 31 words (not reproduced here)
- Popularity rank on source library: #79

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
فيلم كرتوني دافئ مدته نحو 53 ثانية في مكتب واحد ثابت: الوكيل شخصية صندوق برتقالي بعينين نقطيتين وذراعين قصيرتين خلف مكتب عليه لوحة نحاسية. يبدأ نائماً ليلاً، ثم تقريب إلى الشاشة التي تكتب بدء الجلسة، وتصل رسائل المستخدم كطائرات ورقية تنفتح إلى ملاحظات مكتوبة باليد؛ يتفاعل الوكيل بتعابير مختلفة والشاشة تعرض كوداً أو صورة أو شريط تقدم أو علامة صح، وتتراكم المكافآت على رأسه والنافذة تنتقل من النهار إلى الليل.

A warm, ink-outlined cartoon of about 53 seconds in a single fixed office: the agent is an orange box character with dot eyes and stubby arms behind a desk with a brass plaque. It starts asleep at night, a push-in to the monitor types the session start, then user messages arrive as paper airplanes that unfold into handwritten notes; the agent reacts with expressions while the monitor shows code, an image, a progress bar or a green check, rewards pile up on its head and the window cycles from day to night.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (CSS, GSAP, Web Audio), suggested duration (53 s), aspect 16:9, difficulty 4/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Characters / شخصيات, Code / كود.
- [playbooks/characters.md](../../playbooks/characters.md)
- [playbooks/code.md](../../playbooks/code.md)

Category tactics:
* Use consistent model sheets and rigs, key poses, anticipation and follow-through, readable expressions and walk cycles.
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
4. `python3 tools/kosif.py scaffold pm-jake11moran-a269c4 <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
