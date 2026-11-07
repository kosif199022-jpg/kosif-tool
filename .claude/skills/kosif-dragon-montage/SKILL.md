---
name: kosif-dragon-montage
description: Black Dragon montage protocol («التنين الأسود، مونتاج»). Use when the owner gives one or more videos (and optionally music or a reference video) and asks the Black Dragon to edit, cut, montage or make a reel from them, or says «مونتاج بالتنين», «التنين الأسود مونتاج», «اعمل ريل من الفيديو ده», «اعمل زي الفيديو ده». It analyses the footage, thinks through three different creative concepts using the merged thinking registry, picks a look from 897 styles plus the matrices, writes a reasoned edit decision list, renders with ffmpeg (grade, camera moves, transitions, Arabic karaoke captions, ducked music, -14 LUFS), exports an editable project for CapCut/Premiere/Resolve, then reviews its own cut and fixes it for up to three rounds. Also states exactly which tools must be installed (doctor).
---

# Dragon Montage — بروتوكول مونتاج التنين الأسود

One command, eight stations, every station leaves a file you can open. Contracts
between stations: [CONTRACTS.md](CONTRACTS.md).

```bash
# 0. what is installed / missing, and how to install it (never installs by itself)
python3 .claude/skills/kosif-dragon-montage/scripts/dm_doctor.py doctor
python3 .claude/skills/kosif-dragon-montage/scripts/dm_doctor.py install-plan --os windows

# full protocol (same thing through the dragon: black_dragon.py montage edit …)
python3 .claude/skills/kosif-dragon-montage/scripts/dragon_montage.py edit "<طلب المالك>" \
  --clip a.mp4 [--clip b.mp4 …] [--music song.mp3] [--reference ref.mp4] \
  [--platform reel|story|youtube|square|landscape] [--seconds 45] [--style ID] [--invent] \
  [--rounds 3] [--preview] --job out/dragon-montage/<id>

# one station at a time
python3 .claude/skills/kosif-dragon-montage/scripts/dragon_montage.py station <analyze|brief|concepts|taste|direct|render|review|generate|mimic> --job DIR …
```

## The eight stations

| # | Station | Script | Writes | Reuses |
|---|---|---|---|---|
| 1 | العين الأولى (see the footage) | `dm_analyze.py` | analysis.json, thumbs, contact sheet | PySceneDetect / ffmpeg scdet, faster-whisper, librosa, OpenCV YuNet faces, ebur128, silencedetect, music_rhythm_engine fallback |
| 2 | يفهم المطلوب (brief) | `dm_think.py brief` | brief.json | Dragon Mind frame frameworks, editor_mind content/platform rules |
| 3 | يفكر بإبداع (3 concepts + decision) | `dm_think.py concepts` | concepts.json, council_prompt.md | data/mind_registry.json (274 frameworks merged from Dragon Mind, thinking_books, book_methods, mental_models), reel-hooks scoring, think.py decide + sensitivity, llm_council prompt pack, pre-mortem |
| 4 | يختار الذوق (look) | `dm_taste.py pick` | look.json | data/taste_index.json (311 catalog + 500 library + 86 atlas styles), grades/transitions/camera/caption_styles, kmx.py ideate (`--invent`), mimic override |
| 5 | يكتب المونتاج (director) | `dm_direct.py direct` | edl.json (every cut has a reason) | dm_edl.py converters ↔ kosif.timeline.v1, kosif.edl.v1, pro-video-editor EDL, nle_export |
| 6 | ينفّذ (render) | `dm_render.py render` | render/final.mp4, captions.srt, .ass, nle/ project files | ffmpeg filter graph, verify_video.py, nle_export.py |
| 7 | يتفرج وينقد (review) | `dm_review.py review` | review.json, frames, VISION_PROMPT.md | verify_video.py, video_eyes.py, blackdetect, silencedetect |
| 8 | يصلّح ويسلّم (fix + deliver) | `dm_direct.py direct --apply-review` → render → review | edl.rN.json history, report.md | keeps the best-scoring round |

Optional: `dm_generate.py gaps` (proposals for Kling/Higgsfield/Suno with prompts, never spends) and
`dm_mimic.py mimic --reference` («اعمل زي الفيديو ده»: copies a reference's shot rhythm, transitions and look).

## Claude's part (the creative eye)

The scripts are deterministic. Claude adds the taste they cannot measure:
1. After station 3, read `council_prompt.md` and run the council in your own reasoning when the
   decision is marked fragile; if you change the chosen concept, edit `concepts.json.decision.chosen`.
2. After station 7, open the frames listed in `review.json.frames` and follow `review/VISION_PROMPT.md`.
   Add notes and fixes: `dm_review.py review --job DIR --add-note "…" --fix e007:drop:"…"`,
   then `dragon_montage.py station direct --job DIR --apply-review` and re-render.
3. Read `GENERATE_AR.md`. Show the owner each proposal with its prompt and cost. Call the MCP tool
   only after the owner says yes in chat, then `dm_generate.py attach`.

## Rules

- Depth over breadth: each station uses the few tools that fit, and the report lists what was
  consulted separately from what ran on the owner's own media (`receipts.jsonl`, `owner_media: true`).
- Never spend credits, upload, publish or install without the owner's yes.
- A missing optional tool never crashes a station; it is listed under `missing` and in the report.
- Jobs live under `out/` or a path the owner names; sources are never modified.

## Required tools

See [references/TOOLS_AR.md](references/TOOLS_AR.md) (generated from `data/required_tools.json`).
Required: python 3.10+, ffmpeg, ffprobe, numpy, pillow. Recommended for professional results:
faster-whisper, PySceneDetect, OpenCV + YuNet face model, librosa, soundfile, yt-dlp, node,
Playwright/Chromium, an Arabic font (Cairo ships in `fonts/`).

## Tests

`python3 -m unittest discover -s tests -p "test_dragon_montage_*.py"`
