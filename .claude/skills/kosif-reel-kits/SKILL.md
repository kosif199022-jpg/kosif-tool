---
name: kosif-reel-kits
description: Install and run the three free Claude reel kits from the «خبير أونلاين» page - make-reel (one line to a finished Egyptian reel with a free voice), reel-maker (a reel system with a fixed brand style, word-timed captions, a presenter and an overlap check) and talking-character (a cartoon of the owner from one photo that talks with lip-sync). Use for «ريل من سطر واحد», «سيستم ريلز بستايل البراند», «كرتون شبهي بيتكلم», «شخصية كرتون بتتكلم بصوتي», make-reel, reel-maker, talking-character, Reel-Kit, Reel-Studio, Character-Kit.
---

# KOSIF Reel Kits — ريلز «خبير أونلاين»

بالعربي: دي التلات مهارات اللي صفحة «خبير أونلاين» بتديها ببلاش (epreneurs.link/Claude-FreeVideos): ريل كامل من سطر واحد، سيستم ريلز بستايل ثابت للبراند، وشخصية كرتون شبهك بتتكلم ببُق ماشي مع الكلام. الكود بتاعهم مش جوه الريبو ده (مفيش ملف رخصة والريبو عام)، فالنسخ الأصلية محفوظة عندك في ملفات المشروع (`reel-kits-khabeer/`)، والسكربت ده بيتأكد منها وبيثبتها.

## Which skill — ما نكررش

| What the owner has / wants | Use |
|---|---|
| Just an idea, and wants a quick finished reel with code-drawn scenes (paper style) | **make-reel** (this kit) |
| Many reels in one fixed brand look, word-timed captions, a small presenter, 4 voice routes | **reel-maker** (this kit) |
| A cartoon of themselves from one photo that talks with lip-sync | **talking-character** (this kit; Wan 2.7 and an image model are paid) |
| A recording of themselves talking to camera | `talking-head-reels` |
| A cartoon story from their own voiceover, no AI video | `cartoon-audio-short` |
| Only the hook and script | `kosif-reel-hooks` |
| A cinematic code-drawn promo or one-world film | `kosif-web-film` |
| The free Egyptian voice alone (edge-tts ar-EG Shakir / Salma) | `kosif-voice-studio`, which already has it |

## Install from the owner's copy

```bash
RK=.claude/skills/kosif-reel-kits/scripts/reel_kits.py
python3 -I $RK list                                                   # the 3 kits and their reviewed SHA-256
python3 -I $RK install /mnt/project-files/reel-kits-khabeer/make-reel.zip --dest out/reel-kits
python3 -I $RK install /mnt/project-files/reel-kits-khabeer/reel-maker.zip --dest out/reel-kits
python3 -I $RK install /mnt/project-files/reel-kits-khabeer/talking-character.zip --dest out/reel-kits
python3 -I $RK status                                                 # what is installed in out/reel-kits
python3 -I $RK self-test                                              # known-answer test (no kit needed)
```

Then read `out/reel-kits/<kit>/SKILL.md` and follow it, working inside `out/` (gitignored), so nothing from a kit reaches the public repository. On the owner's own computer the zips can instead be unzipped into `~/.claude/skills/`.

**Review of the versions pinned here (2026-11-16):** the scripts call only local `ffmpeg`/`ffprobe` and the `edge-tts` package, with no hooks, no MCP servers, no keys and no remote URLs. reel-maker bundles GSAP (GreenSock standard licence) and three Google Fonts (OFL). A zip with another hash is refused until it has been reviewed (`--allow-unpinned`).

## KOSIF rules on top

- **Show before spending:** the script and a voice preview go to the owner before the scenes, as the kits say. ElevenLabs, OpenAI TTS, Higgsfield image and Wan 2.7 lip-sync cost credits: show the plan and get a yes before each paid call; the free route is edge-tts plus code-drawn scenes.
- **Keys:** read from environment variables only, never written to a file.
- **Rendering:** the kits render with `npx -y hyperframes@0.8.97`; ask before installing Node packages. The macOS Chrome path in make-reel's stills step is replaced by the pre-installed Playwright Chromium in a cloud session.
- **Delivery:** the KOSIF export standard applies (`playbooks/export-standard.md`): 1080x1920, 30 fps, H.264, the voice untouched; check Arabic captions with `playbooks/arabic-typography.md`.

## Credit

The three kits and their videos are by the «خبير أونلاين» page (Instagram: epreneurshossam), shared free for everyone, with no licence file. This skill and `reel_kits.py` are KOSIF's own text and code. See `THIRD_PARTY_NOTICES.md`.
