---
name: kosif-shadow-theatre
description: Make shadow-theatre / silhouette motion-graphics films (مسرح الظل، مشاهد بالظلال) from code — bodies that join into trees, boats and buildings, figures that grow as they near the lamp, iris and spotlight transitions over projected gradient skies. Use when the user wants scenes "like the shadow act" (Attraction-style), a silhouette story, or to analyse a shadow-theatre video and build original scenes in that style.
---

# KOSIF Shadow Theatre — مسرح الظل

بالعربي: المهارة دي بتعمل أفلام «مسرح ظل» حقيقية من كود: سما متدرجة بإضاءة بروجكتور، أجسام سودا بمفاصل بتتحرك وبتتجمع وتعمل شجرة أو مركب أو مبنى، شخص يقرّب من اللمبة فيكبر ظله ويغبش، وفتحات ضوء (دايرة، قلب، نجمة، قوس) بتفتح وتقفل المشهد. كل فريم بيترسم من ملف مشهد JSON، فتقدر تطلع صور ثابتة وتعدّل قبل الرندر.

**Status:** working engine, tested here (`tests/test_shadow_theatre.py`), one original demo film (`scenes/lantern-keeper.json`, «حارس الفانوس»).
Pure Python (numpy + Pillow) + ffmpeg. No browser, no paid service, no copied media.

## Front door

```bash
ST=.claude/skills/kosif-shadow-theatre/scripts/shadow_theatre.py
python3 $ST doctor                                  # numpy / Pillow / ffmpeg present?
python3 $ST library                                 # poses, costumes, cycles, props, backdrops, iris shapes, techniques
python3 $ST analyze <reference.mp4> --out out/shadow/<job>/ref     # cuts, lit-screen palette, silhouette share, contact sheet
python3 $ST check  <scene.json>                     # timing + style grammar (fails with reasons)
python3 $ST stills <scene.json> --out out/shadow/<job>/stills --times 2,7.5,12
python3 $ST render <scene.json> --out out/shadow/<job>/film.mp4 [--preview] [--no-audio]
```

`render` writes the owner's export standard by default (1080×1920, 30 fps, H.264 High CRF 17 slow, BT.709, `+faststart`)
through `kosif-superpowers/scripts/export_profile.py`. The score is an original synth pad generated per chapter with a
low swell on each cue (AAC 320k because it is a mixed track). If the user gives music, render `--no-audio` and mux their
track by stream copy, cutting chapters on their beats (`cues`).

## Workflow (director first, then code)

1. **Reference (optional).** If the user uploads a shadow act, run `analyze` and open `contact.jpg`. Name what you see in
   the grammar below (which techniques, which palette, how chapters change). Say plainly if you could not open it.
2. **Story in chapters.** 3 to 6 chapters, each one image the audience can name in two words (a tree, a boat, a giant,
   a home). One emotional turn. One chapter is `memorable`. Make an original story; never re-stage someone else's act.
3. **Write the scene JSON** (copy `scenes/lantern-keeper.json`). Grammar and every field: `references/scene-grammar.md`.
4. `check` until PASS. It enforces: scenes tile the duration, ≥3 scenes, varied lengths, no repeated non-blackout
   transition back to back, every scene has a silhouette, ≥4 style techniques used, a `body-build` moment, a memorable scene.
5. `stills` at the middle of every chapter and at each body-build moment. Look at them. A body-build must read as the
   object without explanation; if it reads as "people standing", move bodies closer, overlap them more, add a held prop
   (`foliage`, `lantern`) — that is what real troupes do too.
6. `render --preview` (half size, 15 fps) for timing, then the full render. Verify with `ffprobe` (size, fps, duration, audio).

## The style in eight techniques (what makes it read as shadow theatre)

| technique | how the engine does it |
|---|---|
| `body-build` | several `human` actors key from neutral poses into poses that overlap into one object (`trunk` + leaning `frond` bodies = tree, `hull` + `sail` = boat) |
| `morph` | the same actors change pose in place; no cut between pictures |
| `depth-scale` | `depth` 0→1 moves a body toward the lamp: shadow grows ×(1+2.2·depth) away from the lamp axis and softens (penumbra blur) |
| `iris` | scene `iris` (circle, heart, star, arch) scales open/closed; outside it the cloth stays unlit |
| `spotlight` | scene `spot` (or a backdrop with one) — a radial pool whose radius can be keyed (`r_keys`) |
| `walk-in` | `cycle: {type: walk}` while `x` keys carry the figure in from off-screen |
| `prop-cutout` | props with punched holes let light through: `lantern`, `skyline` windows, `crescent` |
| `blackout` | `fade_in` / `fade_out` dim the lamp to the faint cloth between chapters |

Measured look of the reference act (details in `references/style-analysis.md`): pure black, slightly soft silhouettes;
projected skies with a bright horizon band (lime-green/teal/pale-blue) under deep blue-violet tops, or a crimson field with
a white central pool; rounded-corner screen inside a dark stage; picture changes by morph, blackout and iris, while the
11 hard cuts in 227 s are all TV camera cuts to judges and audience.

## Rules

- Original scenes only: draw from the grammar, not from a specific act's choreography or story beats. Credit a reference
  by name and link if the user supplied it; never commit its frames or audio.
- Silhouettes stay black and readable: one clear outline per idea, profile poses read better than frontal ones.
- Bodies keep human proportions (costumes `plain`, `dress`, `child`, `elder`); scale `height` for distance, not width.
- Do not claim a film was rendered or checked without the `render` JSON line and a look at stills.
- Long renders: run in the background (repo rule: never `sleep` to wait). A 22 s film at 1080×1920 rendered in about 4 minutes here.

## Files

- `scripts/shadow_theatre.py` — CLI (doctor, library, analyze, check, stills, render, synth score).
- `scripts/shadow_engine.py` — renderer: keyframes + easing, articulated body (forward kinematics, 16 poses, 5 cycles),
  13 props, 6 backdrops, clouds, lamp hotspot, depth/penumbra, iris, spotlight, screen frame, grain.
- `scenes/lantern-keeper.json` — demo: «حارس الفانوس», 22 s, 4 chapters (arrival in the amber desert; a tree of bodies;
  a dance where one body grows into a giant; a boat of bodies under the crescent, closed by an arch iris).
- `references/lantern-keeper-sheet.jpg` — one frame per second of the rendered demo (proof).
- `references/scene-grammar.md` — every JSON field. `references/style-analysis.md` — the reference analysis.
