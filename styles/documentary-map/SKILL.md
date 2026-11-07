---
name: documentary-map
description: A 9:16 documentary reel over a desaturated, film-grained realistic terrain map: the camera swoops from a regional view down to pinned cities, black-and-white archival photos appear in slightly tilted frames with Ken Burns drift, and a large date ribbon and serif Arabic place names anchor each stop. Use to make a new video in this look (Diagrams); address it by ID documentary-map.
---

# KOSIF TOOL — خريطة وثائقية / خريطة وثائقية — خريطة واقعية مع صور أرشيفية وتواريخ

## Primary motion reference (المرجع)
- Page: https://github.com/kosif199022-jpg/kosif-one
- Video: see source page
- Credit: KOSIF + attributed sources
- Source type: Style · Origin: KOSIF original style

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
ريل وثائقي عمودي 9:16 على خريطة تضاريس واقعية بألوان باهتة وحبوب فيلم، تنقضّ الكاميرا من رؤية إقليمية إلى مدن محددة بدبابيس، وتظهر صور أرشيفية بالأبيض والأسود في إطارات مائلة قليلاً بحركة كين بيرنز، مع شريط تاريخ كبير وأسماء أماكن بخط سيريف عربي.

A 9:16 documentary reel over a desaturated, film-grained realistic terrain map: the camera swoops from a regional view down to pinned cities, black-and-white archival photos appear in slightly tilted frames with Ken Burns drift, and a large date ribbon and serif Arabic place names anchor each stop.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Remotion, React, WebGL, CSS), suggested duration (36 s), aspect 9:16, difficulty 4/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Diagrams / مخططات, Photos / صور.
- [playbooks/diagrams.md](../../playbooks/diagrams.md)
- [playbooks/photos.md](../../playbooks/photos.md)

Category tactics:
* Reveal nodes in causal order; draw SVG edges with dash offsets; move the camera between relationships deliberately.
* Use original or licensed photos in layered camera rigs with planar parallax, dynamic masks and depth-aware transitions.

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
4. `python3 tools/kosif.py scaffold documentary-map <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
