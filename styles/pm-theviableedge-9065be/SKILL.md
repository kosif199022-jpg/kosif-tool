---
name: pm-theviableedge-9065be
description: A 15-second service promo on warm off-white paper: evidence cards surround a headline whose struck-out word becomes an orange 'context', red conflict lines link the cards, a dark terminal shows a folder tree and a superseded price, a green test checklist passes, a handoff folder shrinks away, and a two-line headline with four coloured squares closes it. Use to make a new video in this look (Kinetic type); address it by ID pm-theviableedge-9065be.
---

# KOSIF TOOL — Second brain service promo / إعلان خدمة «العقل الثاني»: من فوضى الملفات إلى حزمة تسليم مُختبرة

## Primary motion reference (المرجع)
- Page: https://www.promptsmotion.com/theviableedge-9065be
- Video: https://www.promptsmotion.com/__l5e/assets-v1/65733401-5999-4cda-844e-eade0c2de997/453edf35ee497bd2.mp4
- Credit: @TheViableEdge (https://x.com/TheViableEdge/status/2104207707980869918)
- Source type: Prompt · Origin: PromptsMotion
- Published on source: 2026-09-27 · credited model: Opus 5.5 · effort: Max
- Reference aspect: 16:9 (1280×720)
- Creator's public prompt length: about 27 words (not reproduced here)
- Popularity rank on source library: #16

Observe this exact reference before implementing when browser or video tools permit. Analyze sampled frames, scale, easing, transitions, framing, camera, acting, palette and typography. If you cannot watch it, say so; this guide alone does not prove visual similarity.

## Creative brief (الملف الإبداعي)
إعلان خدمة مدته 15 ثانية على خلفية ورقية فاتحة: بطاقات مبعثرة (جدول أسعار، ملاحظة لاصقة، بريد، رسالة صوتية) حول جملة «ليست مشكلة أوامر» تُشطب كلمتها وتُستبدل بـ«سياق» برتقالية، ثم خطوط تعارض حمراء بين البطاقات مع عدّاد ملاحظات، ثم نافذة طرفية داكنة بشجرة مجلدات وسعر قديم مشطوب وجديد معتمد، فقائمة اختبارات خضراء، فمجلد تسليم يتقلص، وختام بعنوان من سطرين ومربعات أربعة ملونة.

A 15-second service promo on warm off-white paper: evidence cards surround a headline whose struck-out word becomes an orange 'context', red conflict lines link the cards, a dark terminal shows a folder tree and a superseded price, a green test checklist passes, a handoff folder shrinks away, and a two-line headline with four coloured squares closes it.

Read the full original brief in [BRIEF.md](BRIEF.md): proposed scenes, motion rules (ar/en), stack (Remotion, React, CSS), suggested duration (15 s), aspect 16:9, difficulty 3/5.

## Categories and playbooks (التصنيفات والدلائل)
Categories: Kinetic type / تايبوغرافي متحرك, Product UI / واجهات المنتج, Code / كود.
- [playbooks/kinetic-type.md](../../playbooks/kinetic-type.md)
- [playbooks/product-ui.md](../../playbooks/product-ui.md)
- [playbooks/code.md](../../playbooks/code.md)

Category tactics:
* Animate readable words in timed beats; sync emphasis to spoken words; preserve Arabic shaping and RTL; never split joined letters.
* Recreate interface states as independent layers; animate meaningful cursor, tap, modal, scroll and focus interactions with consistent depth and realistic timings.
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
4. `python3 tools/kosif.py scaffold pm-theviableedge-9065be <project-dir>` creates STYLE.md, PLAN.md, TEST_REPORT.md, words.json and a starter; fill STYLE.md (observed vs assumed) and PLAN.md (scene by scene).
5. Create original assets and editable code. Use music/SFX only when requested, provided or licensed.
6. Preview: `node tools/render_html.cjs --in <page> --out preview.mp4 --preview` gives a contact sheet; compare several timestamps against the reference and fix motion mechanics and timing.
7. Show the preview before the final render unless the user pre-authorized rendering.
8. Render, then verify duration, fps, frame count and audio stream (fill TEST_REPORT.md); deliver the MP4 with the editable sources.

## Attribution
Reference and creator are linked above. Third-party videos, prompts, assets and music are never redistributed or claimed as KOSIF-owned. Source terms: https://www.promptsmotion.com/terms
