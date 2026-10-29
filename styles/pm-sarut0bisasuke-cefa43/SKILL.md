---
name: pm-sarut0bisasuke-cefa43
description: A silent 30-second recipe explainer on a split screen: a cream paper panel on the left with a wobbly hand-drawn rocks glass and an oz ruler, and a beige sidebar on the right with a handwritten title and an ingredient checklist. Ice drops, two bottles and a cream jug tilt in and pour while the liquid rises, a fraction counter ticks and a 5-step progress bar fills; cream diffuses as clouds into the dark layer, a stirrer swirls, and it ends on a handwritten sign-off with ink splatter.
---

# KOSIF TOOL — White Russian recipe animation / وصفة الوايت روشن من الكأس الفارغة إلى الكوكتيل

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/sarut0bisasuke-cefa43
- Video: https://www.promptsmotion.com/__l5e/assets-v1/b27a9489-7c2e-4c45-b5b8-c2bd96ad0a8a/f79a2b1e73613312.mp4
- Credit: @Sarut0biSasuke (https://x.com/Sarut0biSasuke/status/2103418429248069973)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-09-25 · credited model: Opus 5.5 · effort: Max
- Reference aspect: 16:9 (1920×1080)
- Technologies named by the source: HTML
- Creator's public prompt length: about 56 words (not reproduced here)
- Popularity rank on source library: #45

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
شرح وصفة مدته 30 ثانية بلا صوت على شاشة منقسمة: لوح ورقي كريمي يساراً بكأس مرسوم بخط مرتعش ومسطرة أونصات، وشريط جانبي بيج يميناً بعنوان مكتوب باليد وقائمة مكونات. تسقط مكعبات الثلج، ثم تميل زجاجتان وإبريق قشدة وتسكب بينما يرتفع السائل ويعدّ عدّاد كسور وشريط من خمس خطوات يمتلئ؛ تنتشر القشدة كغيوم في الطبقة الداكنة، ويدور المحرّك، وينتهي بعبارة مكتوبة باليد مع رذاذ حبر.

A silent 30-second recipe explainer on a split screen: a cream paper panel on the left with a wobbly hand-drawn rocks glass and an oz ruler, and a beige sidebar on the right with a handwritten title and an ingredient checklist. Ice drops, two bottles and a cream jug tilt in and pour while the liquid rises, a fraction counter ticks and a 5-step progress bar fills; cream diffuses as clouds into the dark layer, a stirrer swirls, and it ends on a handwritten sign-off with ink splatter.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (HTML Canvas, SVG, CSS), suggested duration (30 s), aspect 16:9, difficulty 3/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Charts / رسوم بيانية, Diagrams / مخططات, Code / كود.
- [playbooks/charts.md](../../playbooks/charts.md)
- [playbooks/diagrams.md](../../playbooks/diagrams.md)
- [playbooks/code.md](../../playbooks/code.md)

Category tactics:
* Use truthful data; animate counters, bars, lines and chart morphs whose labels stay accurate; keep axes and legends readable; reveal one insight at a time.
* Reveal nodes in causal order; draw SVG edges with dash offsets; move the camera between relationships deliberately.
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
4. `python3 tools/kosif.py scaffold pm-sarut0bisasuke-cefa43 <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
