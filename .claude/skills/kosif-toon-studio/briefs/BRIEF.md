# Brief for film makers (series «أبو كاب / أبو نضارة», season 2)

You make short silent cartoon reels: vertical 1080x1920, 30 fps, exactly 20.0 s each, with the Python engine in this folder.
Work only inside `/home/user/kosif-tool/out/20261115-toon/`. Do NOT edit `toonkit.py`, `films/toonx.py`, anything in `sfx/`,
or other people's files in `films/` and `done/`. Do not delete anything you did not create. No network, no installs, spend nothing.

## Read first, in full
- `toonkit.py`: the engine (surface `G` in 1080x1920 world units, scenery, effects, characters `tk.fig`, camera, `tk.run`, audio `tk.Mix` with real sound effects).
- `films/toonx.py`: extra helpers you may import (dashed lines, reach-clamped hands, a rotated figure for lying poses, birds, tufts, wavy arrows).
- `films/f01_cage.py` and `films/f08_spear.py`: two finished films. Copy their structure exactly: `audio()`, `bg()`, `draw()`, `cam()`, `__main__`.

## The series
Two recurring characters, and never any text, letters or digits on screen (no captions, no "Zzz", no numbers, no labels).
«cap» = the hasty mocker in a red cap. «specs» = the calm thinker with glasses.
Each film shows one REAL, surprising science fact. Cap does the obvious thing, fails, and laughs at Specs's odd-looking method.
Specs's method works because of real physics. The physics shown must be correct; do not exaggerate it into something false.

## Requirements for every film
- **Hook**: the first 1.5 s already shows the strange image, camera zoomed in on it, then pulls back. Prefer starting the story at that image over a flash-forward.
- **Clarity**: one idea, big readable staging, characters large in frame. Use zoom 1.0–1.45 via `cam(t)`; all action must be inside the frame at zoom 1.0.
  Show the mechanism visibly (cut-away view, `tk.arrow` for forces and flows, an inset if needed). `tk.bulb` when Specs gets the idea.
  One `tk.badge` pair near the end of the proof: red cross on Cap's way, green tick on Specs's way.
- **Fill the frame**: do not leave the lower third as empty ground. Put the ground line around y=1350–1450, or use the space for a cut-away, foreground plants, water, or a second layer of action.
- **Strong motion**: camera keyframes (`tk.key`), `tk.shake` on impacts, anticipation and overshoot (`tk.out_back`, `tk.out_bounce`), squash on landings,
  secondary motion everywhere (sweat, dust puffs, sparkles, swaying grass and trees, clouds, birds, butterflies).
- **Acting**: change `fig(eyes=, mouth=, brows=, blush=, sweat=)` clearly with the story. Cap laughing = `eyes="squeeze", mouth="laugh"` + `tk.laugh_marks`; shocked = `eyes="wide", mouth="o"`.
- **Look**: pretty layered backgrounds with depth (sky gradient, sun with glow, hills or mountains, trees, ground, grass, flowers); let the colour mood change with the story.
- **Sound** (`tk.Mix`): every visible action has a sound at the same moment. Use the real effects in `sfx/` wherever they fit
  (laughs: `laugh_cartoon`, `laugh_cartoon2`, `laugh_male`, `giggle`; water: `pour`, `splash_big`, `bubble`, `fill`, `river`, `drips`; `rain_*`, `thunder_*`, `wind_storm`, `explosion`, `birds_river`, `pop`, `clink`, `whoosh`)
  plus the synth helpers (`thump`, `clang`, `boing`, `ding`, `tada`, `rise`, `slide_down`, `steps`, `chirps`, `tune`). A light `m.tune` underneath, happier at the end.
- **Ending**: a warm last beat with both characters (Cap learns, they share the result). No end card.

## How to work, per film
1. Write `films/fNN_name.py` modelled on the examples.
2. Preview: `cd /home/user/kosif-tool/out/20261115-toon && python3 films/fNN_name.py prevNN --stills 0.5,2,4,6,8,10,12,14,16,18,19.5`
   writes `prevNN_sheet.jpg`. Open it with the Read tool and LOOK. Fix what reads badly (overlaps, things off-frame, unclear action, wrong facing, empty frames) and preview again
   until every beat is clear at a glance. Check a zoomed still of the key science moment.
3. Final: `python3 films/fNN_name.py done/NN_name.mp4` (writes the `.m4a` and the mp4 with audio). One render at a time.
4. Verify: `ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate -of compact done/NN_name.mp4` must show h264 1080x1920 30/1 + aac, duration 20.0.
5. Delete your own `prevNN*` files when done.

## Engine notes
- `fig(g, who, x, gy, d, t, ...)`: x is the hip x on ground line gy; d=+1 faces right, -1 left; `lh`/`rh` are world-coordinate hand targets (arm reach is about 200);
  `sit=True` sits on the ground; `crouch=0..1` squats; `walk=1.0` with a changing x walks; `soot=0..1` blackens; `k` scales the figure.
- Draw order is z-order. For see-through use `lay = g.layer(); ...draw on lay...; g.blend(lay, alpha)`. Colours are BGR.
- For a body partly sunk in water or sand, draw the fig, then draw the surface over the lower body.
- Keep per-frame work light.

## Report back
For each film: the output path, whether verification passed, two lines on what is on screen, and any weakness you could not fix.
