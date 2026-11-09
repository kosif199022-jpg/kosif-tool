---
name: pm-kloss-xyz-15182a
description: A 2.5-minute vertical first-person AI monologue on black under a fixed HUD with a filling context bar, timecode and live dot, mixing huge condensed cream and coral headlines, italic serif asides, counters, token chips, stamped poll bars, card grids and RGB glitches, then shifting to coral, paper and grey before fading out. Use to make a new video in this look (Product UI); address it by ID pm-kloss-xyz-15182a.
---

# KOSIF TOOL — Chaotic Claude POV video / مونولوج نموذج ذكاء اصطناعي بضمير المتكلم: تايبوغرافي عمودي بواجهة دردشة

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/kloss-xyz-15182a
- Video: https://www.promptsmotion.com/__l5e/assets-v1/76fba185-e002-4e5d-a992-b6c7eb7b26f0/4084c72a81a73964.mp4
- Credit: @kloss_xyz (https://x.com/kloss_xyz/status/2103664956482941143)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-09-26 · credited model: Opus 5.5 · effort: Max
- Reference aspect: 9:16 (1080×1920)
- Creator's public prompt length: about 61 words (not reproduced here)
- Popularity rank on source library: #203

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
فيديو عمودي طويل (نحو دقيقتين ونصف) يحكي فيه نموذج ذكاء اصطناعي بضمير المتكلم عمر محادثة واحدة، على خلفية سوداء تحت شريط علوي ثابت يعرض نسبة السياق المتزايدة وعداد الوقت ومؤشر بث أحمر: عناوين ضخمة مضغوطة بالكريمي والبرتقالي المحمر، أسطر سيريف مائلة، أعداد كبيرة، رموز نصية ملونة، أعمدة نسب مع أختام حمراء، شبكات بطاقات طلبات، تقويم، وومضات تشويش RGB، ثم تتحول الخلفية إلى برتقالي ثم ورق فاتح ثم رمادي حتى تنطفئ وتظهر شارة المنشئ.

A 2.5-minute vertical first-person AI monologue on black under a fixed HUD with a filling context bar, timecode and live dot, mixing huge condensed cream and coral headlines, italic serif asides, counters, token chips, stamped poll bars, card grids and RGB glitches, then shifting to coral, paper and grey before fading out.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Remotion, React, CSS, Web Audio), suggested duration (153 s), aspect 9:16, difficulty 4/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Product UI / واجهات المنتج, Characters / شخصيات, Music / موسيقى, Code / كود.
- [playbooks/product-ui.md](../../playbooks/product-ui.md)
- [playbooks/characters.md](../../playbooks/characters.md)
- [playbooks/music.md](../../playbooks/music.md)
- [playbooks/code.md](../../playbooks/code.md)

Category tactics:
* Recreate interface states as independent layers; animate meaningful cursor, tap, modal, scroll and focus interactions with consistent depth and realistic timings.
* Use consistent model sheets and rigs, key poses, anticipation and follow-through, readable expressions and walk cycles.
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
4. `python3 tools/kosif.py scaffold pm-kloss-xyz-15182a <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
