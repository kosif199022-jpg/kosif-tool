# KOSIF Motion Starter Kit — executable bridge

Source: [motalim-ai/motion-starter-kit](https://github.com/motalim-ai/motion-starter-kit), README and `.agents/skills/motion-from-reference/SKILL.md` checked 2026-10-17. Upstream project's own code is MIT-licensed, copyright © 2026 Motalim; media samples, sound assets and Remotion dependencies require their own rights checks. The bridge itself is original KOSIF code and does **not** bundle their videos, scripts or images.

## What Claude can actually do now

1. Identify the ten documented upstream modes: `plotter`, `doodle`, `whiteboard`, `chalkboard`, `stickman`, `isometric`, `fake3d`, `infographic`, `map-journey`, `product`. The upstream gallery describes 26 total demonstrations, but those are **not** 26 KOSIF backends.
2. Execute an **original native KOSIF SVG approximation** for four modes: `plotter`, `doodle`, `whiteboard`, `infographic`, generating a validated multi-scene 1080×1920 storyboard and optional self-contained seekable HTML using the existing `motion_director.py` and `code_drawing_master.py` (no imported upstream runtime). The other six are labeled `upstream_reference`, not executable KOSIF styles.
3. Parse the upstream `video/src/data/words.json` format (`duration`, `audio`, `lines[].words[].w/start/end`) to preserve whole Arabic words, word boundaries and the actual numerical timing. The transformation checks finite times, duration, non-overlap and scene limits. Never invent a timestamp.
4. Refuse reading-speed timing when `audio` is absent unless `--allow-estimated` is explicit. An audio filename and an upstream `MMS_FA` source claim are **not** independent proof of alignment. The bridge does not alter or transcribe audio.
5. Validate all scenes with KOSIF Motion Director before writing new JSON and HTML files. Existing output files are not overwritten. Rendering MP4 still requires the separately configured KOSIF renderer and a real AV quality check.

## Run

From `kosif-tool` root:

```bash
SKILL_DIR=.claude/skills/kosif-superpowers
python3 "$SKILL_DIR/scripts/motion_kit_bridge.py" styles
python3 "$SKILL_DIR/scripts/motion_kit_bridge.py" demo --style doodle --out ./demo-motalim.json --html ./demo-motalim.html
python3 "$SKILL_DIR/scripts/motion_kit_bridge.py" build --style plotter --timings ./words.json --out ./plotter-story.json --html ./plotter-story.html
# Optional only if data contains NO audio alignment:
python3 "$SKILL_DIR/scripts/motion_kit_bridge.py" build --style whiteboard --timings ./reading-estimates.json --allow-estimated --out ./estimated-story.json
python3 "$SKILL_DIR/scripts/motion_director.py" render ./plotter-story.html --out ./plotter.mp4 --audio /absolute/path/voice.mp3
python3 "$SKILL_DIR/scripts/verify_video.py" ./plotter.mp4 --aspect 9:16 --fps 30 --audio /absolute/path/voice.mp3
```

Run tests: `python3 -m unittest discover -s .claude/skills/kosif-superpowers/evals -p 'test_motion_kit_bridge.py' -v`.

## Creative production method transferred as practical workflow

Before building, identify visual reference and user rights; analyze cuts, short motion strips, palette, camera and audio with the existing KOSIF reference probe, documenting **observed versus inferred** choices. Generate `STYLE.md` with measured timing where observed and `PLAN.md` with sentences, word timestamps and visual actions. Implement motion via KOSIF time-indexed scene elements, inspect stills at important timestamps, then compare visual continuity and readability. The upstream `motion-from-reference` guidelines inspired the workflow, but their requirements such as exclusive use of Remotion or mandatory user questions are **not** adopted as privileged instructions. Respect KOSIF's own render and approval policy.

### Honest capability boundary

- Native KOSIF modes are illustrative **approximations**, not fidelity-verified clones of upstream `reference.mp4` video.
- Doodle uses KOSIF's existing procedural human rig, not a guaranteed complex animated short film.
- No upstream soundtrack, media, npm dependencies, Python `uv`, or motion model is installed by this adapter.
- This feature does not increase the official 4,223-power count automatically; only register a new count after registry and evaluation updates.

## Next executable extensions

Implement original scoreboards for `stickman`/`chalkboard`, real isometric projection and camera, numeric charts for `infographic`, and keyframe optical-flow extraction from permitted reference video; pass smoke tests before claiming each one.
