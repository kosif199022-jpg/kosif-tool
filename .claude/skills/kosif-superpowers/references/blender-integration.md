# KOSIF Blender integration — independent implementation

This module is not an analysis or a copy of proprietary Blender internals. It uses
the documented Blender Python API and command-line interface. Blender is GPL-licensed:
https://developer.blender.org/docs/license/
Blender API: https://docs.blender.org/api/main/index.html
Blender command line: https://docs.blender.org/manual/en/4.2/advanced/command_line/arguments.html

## What exists

- scripts/blender_bridge.py doctor: discovers an existing blender executable without downloading or installing it.
- scripts/blender_bridge.py render --scene templates/blender-demo.json --output scene.glb
- .blend saves an editable Blender scene, .glb exports animated geometry,
  .png renders a still frame.
- Original scripts/blender_worker.py builds Blender meshes/materials/camera/
  lighting and locational keyframes from a strictly bounded JSON scene.
- No .blend project or arbitrary script from a third party is opened;
  Blender auto-execution is explicitly disabled.
- Run headless, use a separate process, validate inputs and output, refuse overwrite.

### Capability verification levels

doctor confirms detection only. Tests without Blender validate schema and
safe process invocation; they DO NOT prove rendering inside Blender.
To verify rendering, install an official Blender release (not an unknown installer),
then render the sample to each format, reopen the .blend, import the .glb
and inspect the actual output and 48-frame motion. Test the exact Blender version.

### Scope / provenance

This creates an independent bridge from KOSIF rather than transplanting code.
Other Adobe/Lightroom REA results are read-only static research, not a license
to copy third-party algorithms, binary fragments, UI assets or codecs.
External skill catalog entries are claims until runtime evidence establishes them.

## Verified five-second cat rescue

Original procedural demo: examples/blender_cat_rescue_5s.py, built with 70 Blender objects and 120 frames in vertical 480x854. Execute with locally installed Blender 5.2.2 headless using --background --factory-startup --disable-autoexec --python-exit-code 7 --python examples/blender_cat_rescue_5s.py. This saves a .blend scene and numbered PNG frames to KOSIF_RESEARCH_PRIVATE_20261019 under the user's home. Encode frames at 24 fps using FFmpeg to MP4. Verified movie at proofs/blender-cat-rescue-advanced-20261019/KOSIF_CAT_RESCUE_5_SECONDS.mp4. This remains simplified geometry, no audio, no realistic human model and no motion capture. For Blender-free rendering, use scripts/native_3d.py and its limited primitive mesh API.
