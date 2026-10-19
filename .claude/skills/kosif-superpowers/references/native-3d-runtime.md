# KOSIF Native 3D — independent core (no Blender required)

This original Python software renderer is an independently implemented **small subset of 3D**, not a copy of Blender or a replacement for its modeling suites. It requires Pillow for images and FFmpeg for MP4, with no Blender, Ghidra or REA runtime dependency.

Invoke from the skill folder:
- python scripts/native_3d.py doctor
- python scripts/native_3d.py render --scene templates/native-3d-demo.json --output demo.png
- python scripts/native_3d.py render --scene templates/native-3d-demo.json --output demo.mp4

The bounded kosif.native3d.v1 JSON schema supports cube/sphere/cylinder mesh primitives, location and yaw keyframes, orthographic camera, face-shaded colored triangles, PNG stills and H.264 MP4 output. It has **no** Blender installation or plugin requirement. Runtime limits: 60 objects, 240 frames, 1,280 pixels on each image dimension. The renderer uses depth-sorted triangle faces rather than an exact per-pixel z-buffer; it does not support Blender feature parity, complex character rigging, physical simulation, geometry nodes, materials or Cycles lighting.

Use the existing Blender bridge for advanced 3D production. REA/Ghidra findings do not authorize copying third-party code; this is an independently implemented runtime.
