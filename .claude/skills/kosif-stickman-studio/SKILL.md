---
name: kosif-stickman-studio
description: Turn a voiceover into a cinematic stick-figure explainer video drawn entirely by code (GrowKaz Stickman studio) - rim-lit black stick figures in moody 2.5D sets, giant face close-ups, freeze-frames, animated numbers and blueprint diagrams, low-poly 3D orbit shots, generated music and SFX, Whisper word timings, 16:9 or 9:16. Use for «فيديو ستيك مان», «رسوم عيدان», «حوّل الفويس أوفر لفيديو أنيميشن», faceless YouTube explainers, "What If" videos, or when the owner sends the GrowKaz_Stickman plugin.
---

# KOSIF Stickman Studio — استوديو الستيك مان

بالعربي: المهارة دي بتحوّل أي فويس أوفر لفيديو أنيميشن كامل بشخصيات «ستيك مان» سودا عليها حافة نور، في ديكورات 2.5D بإضاءة سينمائية، مع لقطات وش قريبة، تجميد للزمن، أرقام ورسوم بيانية بتتحرك، شروحات «بلوبرنت» ولقطات 3D. كل فريم بيترسم بالكود وبيترندر فريم فريم، فالشخصيات ثابتة والنص حاد، ومفيش أي مولّد صور أو فيديو بالذكاء الاصطناعي.

**Where the engine comes from:** the studio kit is by **GrowKaz** (plugin `growkaz-stickman` 1.1.0). It has a named author and no licence file, and this repository is public, so the kit is **not** stored here. The owner keeps the original `GrowKaz_Stickman.plugin` privately (project files: `growkaz-stickman/GrowKaz_Stickman.plugin`) and `scripts/stickman_kit.py` installs it from there. This skill and its script are KOSIF's own text and code. Credit: `THIRD_PARTY_NOTICES.md`.

## Front door

```bash
SK=.claude/skills/kosif-stickman-studio/scripts/stickman_kit.py
python3 -I $SK inspect <GrowKaz_Stickman.plugin>             # skills, version, licence, refused paths, risk flags
python3 -I $SK install <GrowKaz_Stickman.plugin> --dest out/stickman-studio
python3 -I $SK status  --dest out/stickman-studio              # version, changed kit files, existing projects
python3 -I $SK self-test                                        # known-answer test (no plugin needed)
```

`install` copies only the plugin's `skills/make-2d-video/kit/` into `--dest`, refuses absolute or `..` paths, symlinks and oversized files, and never touches `projects/`. Keep the studio under `out/` (gitignored) so the vendor code and renders never reach the public repo. Then, inside the studio: `npm install`, `python3 tools/verify_kit.py` (expect 29/29), `python3 tools/doctor.py`. Ask before installing (ffmpeg, Node packages, Playwright Chromium, numpy, scipy, faster-whisper; about 1 GB, and Whisper downloads its model from huggingface.co). In a cloud sandbox reuse the pre-installed Playwright Chromium instead of `npx playwright install`.

**Security review of 1.1.0 (2026-11-07):** no hooks, no MCP servers, no slash-command shell lines, no API keys. The renderer serves files on `localhost` only. One sharp edge: `tools/doctor.py --install` runs its fix lines through a shell; run plain `doctor.py` and do the installs yourself. Re-run `inspect` on any new plugin version before installing it.

## The pipeline (eight stages)

| Stage | What happens | Studio command (inside the studio) |
|---|---|---|
| 1 Intake | voiceover (required), script (timed, plain or none), aspect, resolution, captions, music, SFX, title | — |
| 2 Studio | install or check the kit | `stickman_kit.py install`, `tools/doctor.py` |
| 3 Timeline | project folder, word timings, beat sheet | `tools/new_project.py`, `tools/parse_script.py` or `tools/transcribe.py`, `tools/beats.py` |
| 4 Story | `story/bible.md` (logline, cast with one signature colour each, locations, motifs, music plan), `scenes/cast.js`, `story/shots.json` | — |
| 5 Look | render the owner's own shots in the five preset grades and let them pick | `node render.mjs --project P --styles emerald,ember,arctic,sakura,retro --at t1,t2,t3 --scale 0.5` |
| 6 Shots | write sets and shots in batches of 8–12, contact-sheet QC after each batch | `node render.mjs --project P --sheet --scale 0.5`, `--stills`, `--from A --to B` |
| 7 Sound | music sections by mood, per-shot SFX and ambience | `audio/music.py`, `audio/sfx.py --list`, `audio/mix.py` |
| 8 Render | preview, final frame-by-frame render, mix, mux, QC | `node render.mjs --project P`, then `python3 audio/mix.py --project P` |

The kit's own guides (`references/style-bible.md`, `story-breakdown.md`, `engine-api.md`, `sound-design.md`, `render-qc.md`) stay in the owner's plugin; read them from the plugin or the installed studio before designing shots.

## KOSIF rules on top of the kit

1. **The narration is sacred.** Never rewrite, drop or reorder spoken words, and keep the owner's audio stream untouched (`playbooks/audio-sync.md`).
2. **Same look, new pictures.** Invent sets, props and actions for each script; the bundled example is for learning the API only.
3. **Look before rendering.** Open every contact sheet and still yourself before a long render. Never claim to have seen a frame you did not open.
4. **Owner export standard.** For delivery, set `config.json` to `"aspect": "9:16"`, `"resolution": "1080p"`, `"fps": 30` unless the owner asks otherwise, then finish with the repo's export profile (`playbooks/export-standard.md`, `.claude/skills/kosif-superpowers/scripts/export_profile.py`). No 4K unless asked.
5. **Long renders** go through `python3 tools/job.py start --dir <work>/job -- node render.mjs ...` and a Monitor wait, never `sleep` loops (`playbooks/render-pipeline.md` §5).
6. **Arabic voiceovers:** transcribe with `--lang ar` (the kit defaults to English) and check `timeline/transcript.txt` against the script; burn-in captions in Arabic follow `playbooks/arabic-typography.md`.
7. **Generated music** is a serviceable bed. For songs or premium scores, go to Suno first (appendix A46) with the owner's yes, or use the owner's own licensed track (`config.music.file`).
8. **Never publish the kit.** Keep the studio under `out/` or the owner's own folder; do not commit GrowKaz files to this repository.

## How it fits the rest of KOSIF

- **Black Dragon:** listed as `skill:kosif-stickman-studio`; its reviewed adapter runs `stickman_kit.py self-test` (known-answer, no plugin, no network). It does not render a film by itself.
- **Neighbours:** `kosif-shadow-theatre` (silhouette theatre, pure Python), `kosif-web-film` (motion-design promos), `saas-animation` (8–20 s product ads), `kosif-voice-studio` (make the voiceover first), Montage Pro (cut real footage). Pick stickman when the owner wants a narrated explainer with recurring characters.
