---
name: kosif-stickman-director
description: Plan a stick-figure video as a director - turn a topic, article or script into an approved storyboard and ready video-generation prompts (Director mode, styles A1-A7), or into a narrated, captioned illustration video (Autopilot B1-B6) - using Stickman Video Director (kaomei, MIT), fetched on demand. Use for «اكتبلي برومبتات فيديو ستيك مان», «ستوري بورد ستيك مان», «فيديو ستيك مان بجيميناي», stickman video prompts, Stickman Video Director, directing-stickman-videos. For a stickman explainer drawn entirely by code from the owner's own voiceover, use kosif-stickman-studio instead.
---

# KOSIF Stickman Director — مخرج الستيك مان

بالعربي: المهارة دي بتاخد فكرة أو مقال أو سكريبت، وبتطلع منه خطة إخراج لفيديو ستيك مان: نسبة الشاشة والمدة والستايل، بعدين مقترح المخرج بالسرد والمشاهد، ولما توافق بتكتب برومبت لكل مقطع ١٠ ثواني جاهز لمولّد فيديو زي Gemini Omni Flash. وفيها كمان وضع «أوتوبايلوت» بيعمل الفيديو كامل بصوت وكابشن ورسوم بسيطة متحركة. المهارة من مستودع [kaomei/stickman-video-director](https://github.com/kaomei/stickman-video-director) (رخصة MIT).

## Which stickman skill — ما نكررش

| What the owner has / wants | Skill |
|---|---|
| A topic or script, and wants a storyboard plus prompts for a video model, or a ready-made style (classic black and white, modern pop, cave, cozy, rubber hose, retro TV, survival thriller, character explainer, meme) | **this skill** |
| Their own recorded voiceover, and wants a cinematic explainer drawn frame by frame by code (rim-lit 2.5D sets, 3D orbits, no AI image or video generator) | `kosif-stickman-studio` (GrowKaz kit) |
| A shadow-theatre or silhouette story | `kosif-shadow-theatre` |

Both can work together: this skill writes the story, scenes and narration; the studio renders it from the owner's voiceover.

## Get the upstream skill (not stored in this repository)

The upstream skill is about 485 MB (sound library, reference films, art kits), so only this wrapper lives here.

```bash
SV=.claude/skills/kosif-stickman-director/scripts/svd_kit.py
python3 -I $SV fetch                       # pinned commit 8ef02ec into out/stickman-video-director (gitignored)
python3 -I $SV status                      # commit, licence, SKILL.md, file counts
python3 -I $SV self-test                   # offline known-answer test of fetch/status
```

Then read `out/stickman-video-director/skills/directing-stickman-videos/SKILL.md` and follow it. To install it as its own Claude skill, copy that folder to `~/.claude/skills/directing-stickman-videos/` (ask first; it is 485 MB). For a newer upstream version pass `--commit <sha>` and review the diff first.

## KOSIF rules on top

- **Director mode (A1-A5) is text only:** proposals and prompts, no network, no credits. Show the proposal and wait for the owner's yes before writing the clip prompts, as the upstream skill says.
- **Autopilot (B1-B6) and A6/A7 call paid generation** (Gemini TTS and video, image tools; `GEMINI_API_KEY`). Show the plan and the expected spend and get the owner's yes before any paid call. Never write a key to a file. Higgsfield can stand in for generation with a yes.
- **Running upstream code:** `npm install` (`@napi-rs/canvas`, `sharp`), ffmpeg and Python run inside `out/stickman-video-director/`; ask before installing. Never commit renders or the upstream folder.
- **Delivery:** the KOSIF video export standard applies (`playbooks/export-standard.md`): 1080x1920 30 fps H.264 for 9:16 unless the owner asks otherwise.
- **Language:** the upstream default is English. When the owner writes in Arabic, say the narration language in the brief (Egyptian Arabic or MSA) and check Arabic captions with `playbooks/arabic-typography.md`.

## Credit

Stickman Video Director, © 2026 Stickman Video Director contributors (github.com/kaomei/stickman-video-director), MIT. Its bundled sound effects and music keep their own licences, listed upstream in `assets/b-audio-library/CREDITS.md`. This skill and `svd_kit.py` are KOSIF's own text and code. See `THIRD_PARTY_NOTICES.md`.
