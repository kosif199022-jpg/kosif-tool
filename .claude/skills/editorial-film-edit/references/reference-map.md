# Reference map

This copy of the skill ships **without reference media** (no photos, frame overviews or MP4 examples were included in the repository). The visual grammar is fully described in [style-guide.md](style-guide.md) and implemented in `implementation/browser-reference/`.

## Working without bundled media
1. Ask the user for 2–4 references they are allowed to use (their own previous edits, licensed footage or stills), or work from the style guide alone.
2. If references are provided, place them in the project folder (not in the skill folder) and record them in the project's own manifest with source and usage terms.
3. To study motion in a reference video, extract a frame sheet and short frame sequences, e.g. `ffmpeg -i ref.mp4 -vf "fps=2,scale=480:-1,tile=6x4" -frames:v 1 sheet.png`.
4. A cover image cannot show motion; judge entrances, grain and transitions from frames or playback.

## If media are added to the skill later
Put them in `references/photos/`, `references/videos/`, `references/frames/` and list each file in [media-manifest.json](media-manifest.json) with path, provenance, licence and SHA-256.
