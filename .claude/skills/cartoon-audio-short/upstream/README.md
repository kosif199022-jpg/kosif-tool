# claude-animated-shorts (upstream, vendored)

Source: https://github.com/mromidev/claude-animated-shorts at commit `e3b817b6afc6cd413466d43f11ba31209e034bbf`, MIT (© 2026 Mr omi, see `claude-animated-shorts/LICENSE`).

The kit in `../kit/` is a lighter, Arabic-ready rebuild of this skill (no Remotion: three.js straight in headless Chromium). This folder keeps the full original next to it, so its depth is on hand:

| Path | Use it for |
|---|---|
| `claude-animated-shorts/UPSTREAM-SKILL.md` | The original 55-70 s pipeline (Remotion + `@remotion/three`), every rule and fix, and the final look values. Renamed from `SKILL.md` so it does not load as a second skill. |
| `claude-animated-shorts/templates/bridge/` | Full TypeScript source of "The Bridge That Fell for a Song": world builder, cast, ink, lens blur, grade, lights, card shading, story and camera. |
| `claude-animated-shorts/templates/audio/` | Synthesized sound in numpy + scipy: `dsp.py` (filters, reverb, BS.1770-4 loudness, LRA, true peak, 24-bit WAV), `sfx_gen.py` (40+ SFX synths: creaks, whooshes, splashes, crowds, birds, hammer), `instruments.py` + `music.py` (march score), `mix.py` (ducked mix, own limiter). |
| `claude-animated-shorts/templates/scripts/` | `short_qa.py` (frame-by-frame QA of a finished short), `sbs_sheet.py` (ours vs reference sheet), `bridge-stills.mjs`, shot merge helpers. |
| `claude-animated-shorts/references/` | `STYLE_BIBLE.md` and seven measured reports (motion, depth, textures, characters, lighting, outlines, grade). |

Left out on purpose: `references/frames/` and `references/sheets/` (about 18 MB of stills from another creator's videos). Upstream marks them for private style study only, so they are not redistributed here.

Two rules from the upstream skill stay in force: story, characters and voice are always our own, and the reference channel is never named or copied.

Black Dragon checks this folder inside the `skill:cartoon-audio-short` adapter (`_black_dragon_skill.py cartoon-short`, needs scipy): BS.1770 loudness against ffmpeg's ebur128, true peak on a known inter-sample peak, three SFX synths, `short_qa.py` on a clip with a planted black span, and `sbs_sheet.py`.
