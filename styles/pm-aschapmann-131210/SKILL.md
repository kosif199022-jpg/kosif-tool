---
name: pm-aschapmann-131210
description: A 30-second dark launch film for a forum marketing tool: it opens on a tilted wall of forum-post cards behind a word-by-word headline, then three pain cards with realistic UI examples, a small red sailing-ship mascot riding glowing line waves under the product name, a post card that gets an AI draft reply typed beneath it, a three-step timeline, and a red sunrise behind the sea with a letter-pop logo reveal.
---

# KOSIF TOOL — SaaS launch video / فيلم إطلاق منتج SaaS مبرمج في Remotion

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/aschapmann-131210
- Video: https://www.promptsmotion.com/__l5e/assets-v1/6f465be6-2b08-4b41-920e-c4a76a362dfd/95e1a12f4d8b8329.mp4
- Credit: @aschapmann (https://x.com/aschapmann/status/2104230888812724497)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-09-27 · credited model: Opus 5.5 · effort: Max
- Reference aspect: 16:9 (1920×1080)
- Technologies named by the source: Remotion, SVG
- Creator's public prompt length: about 178 words (not reproduced here)
- Popularity rank on source library: #95

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
فيلم إطلاق مدته 30 ثانية لأداة تسويق عبر المنتديات على خلفية داكنة: يبدأ بجدار مائل من بطاقات المنشورات خلف عنوان يظهر كلمة كلمة، ثم ثلاث بطاقات ألم بأمثلة واجهة حقيقية، سفينة شراعية حمراء صغيرة تبحر على أمواج خطية متوهجة تحت اسم المنتج، بطاقة منشور يُكتب تحتها رد مقترح، خط زمني من ثلاث مراحل، وختام بشروق أحمر خلف البحر وكشف الشعار حرفاً حرفاً.

A 30-second dark launch film for a forum marketing tool: it opens on a tilted wall of forum-post cards behind a word-by-word headline, then three pain cards with realistic UI examples, a small red sailing-ship mascot riding glowing line waves under the product name, a post card that gets an AI draft reply typed beneath it, a three-step timeline, and a red sunrise behind the sea with a letter-pop logo reveal.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Remotion, React, SVG), suggested duration (30 s), aspect 16:9, difficulty 3/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Product UI / واجهات المنتج, Charts / رسوم بيانية, Kinetic type / تايبوغرافي متحرك, Characters / شخصيات, Photos / صور, Music / موسيقى, Code / كود.
- [playbooks/product-ui.md](../../playbooks/product-ui.md)
- [playbooks/charts.md](../../playbooks/charts.md)
- [playbooks/kinetic-type.md](../../playbooks/kinetic-type.md)
- [playbooks/characters.md](../../playbooks/characters.md)
- [playbooks/photos.md](../../playbooks/photos.md)
- [playbooks/music.md](../../playbooks/music.md)
- [playbooks/code.md](../../playbooks/code.md)

Category tactics:
* Recreate interface states as independent layers; animate meaningful cursor, tap, modal, scroll and focus interactions with consistent depth and realistic timings.
* Use truthful data; animate counters, bars, lines and chart morphs whose labels stay accurate; keep axes and legends readable; reveal one insight at a time.
* Animate readable words in timed beats; sync emphasis to spoken words; preserve Arabic shaping and RTL; never split joined letters.
* Use consistent model sheets and rigs, key poses, anticipation and follow-through, readable expressions and walk cycles.
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
4. `python3 tools/kosif.py scaffold pm-aschapmann-131210 <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
