---
name: pm-pluginplay-3d4006
description: A 26 s pixel-art gag: a man on a cliff at a purple retro sunset throws a boomerang each year while a yellow pixel caption types that year's AI milestone; it returns bigger and brighter, then a self-improvement loop spins a version counter to infinity, a white-flash blast, a smug face close-up, and the boomerang returns to scorch him in a cartoon explosion. Use to make a new video in this look (Characters); address it by ID pm-pluginplay-3d4006.
---

# KOSIF TOOL — Pixel art LLM history / تاريخ النماذج اللغوية بالبكسل: رجل يرمي بومرانغ

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/pluginplay-3d4006
- Video: https://www.promptsmotion.com/__l5e/assets-v1/9176db3a-d200-42e5-af68-acce718712d7/d3bc427ebf8a8f87.mp4
- Credit: @PluginPlay__ (https://x.com/PluginPlay__/status/2103910844677472343)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-09-26 · credited model: Opus 5.5 · effort: Max
- Reference aspect: 16:9 (1280×720)
- Technologies named by the source: HTML
- Creator's public prompt length: about 22 words (not reproduced here)
- Popularity rank on source library: #95

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
رسوم بكسل مدتها 26 ثانية: رجل على جرف فوق بحر عند غروب ريترو بنفسجي يرمي بومرانغ كل عام، وفوقه صندوق حوار أصفر بخط بكسل يكتب حدث العام (من ورقة الانتباه حتى الوكلاء). البومرانغ يعود كل مرة أكبر وأكثر توهجاً، ثم دورة تحسين ذاتي يتسارع فيها عداد الإصدار إلى اللانهاية، انفجار ضوئي، لقطة قريبة لوجه الرجل الراضي، ثم يرتد البومرانغ ويحرقه بانفجار كرتوني.

A 26 s pixel-art gag: a man on a cliff at a purple retro sunset throws a boomerang each year while a yellow pixel caption types that year's AI milestone; it returns bigger and brighter, then a self-improvement loop spins a version counter to infinity, a white-flash blast, a smug face close-up, and the boomerang returns to scorch him in a cartoon explosion.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (HTML Canvas, Web Audio), suggested duration (26 s), aspect 16:9, difficulty 3/5.

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
4. `python3 tools/kosif.py scaffold pm-pluginplay-3d4006 <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
