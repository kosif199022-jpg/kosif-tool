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
