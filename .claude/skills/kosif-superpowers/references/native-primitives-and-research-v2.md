# KOSIF Independent Geometry and Feature Truth

Original Blender-free software renderer: cone and torus added to cube/sphere/
cylinder. CPU flat shading, painter or per-pixel depth buffer, orthographic
camera, object motion/yaw keyframes, PNG and H.264 MP4 (FFmpeg required).
Five-second sample: templates/native-3d-primitives-demo.json.
Tests: python -m unittest discover -s .claude/skills/kosif-superpowers/evals -p test_native_primitives.py -v.
These are bounded primitives, not full Blender modeling, simulation or Cycles.

REA/Ghidra are suitable for authorized executable binary inspection, but
Blender public source and API tests provide stronger feature evidence.
Official Blender GPLv3 source: https://projects.blender.org/blender/blender.
Cycles may be separately integrated after checking its own file-specific
license, build requirements and test outcomes.

Other source-led candidates:
- SVG-Edit MIT vector canvas/editor: https://github.com/SVG-Edit/svgedit
- AutoDraw ML stroke suggestion, NOT full generative rendering; no copied
  proprietary Google artist assets: https://experiments.withgoogle.com/autodraw
- receptron/laya MIT Jev-compatible ONNX adapter for decision choice/score/
  noul, NOT an image/video engine: https://github.com/receptron/laya
  Model bundle approx 1.7GB, NOT installed or executed by this change.
- Photopea/Kleki/Magma/Pixlr/Canva and commercial browser apps: public
  feature survey and authorized APIs only; no private server code recovered.
- Actual hosted multi-tenant browser needs independently validated isolation,
  authentication and network egress controls; browser_scout is only local.

Latest prior local static audit: 2,109 readable files in Desktop Tajriba,
plus owner GitHub repo metadata counts 24 and 2. Neither is a line-by-line
audit of source/binaries. Atlas 14,793 indexed external records are metadata
until source/license/runtime gates establish genuine skill execution.

## REA + Ghidra fresh bounded runtime result (2026-10-20)

REA v6.7.0 ran a successful read-only Ghidra 12.1.4 inspection of the
official Blender 5.2.2 Windows BlendThumb.dll (SHA256
7230681cc83424fbdcd67438019a5af64068f073d98c15b3a58e37d0717d2fc4).
The summary recorded 9 defined image segments, 557 Ghidra-defined procedures,
and 237 defined strings. Local private evidence is retained at
KOSIF_RESEARCH_PRIVATE_20261019/REA_GHIDRA_BLENDER_THUMB_20261020.json.
This is the Windows thumbnail helper, NOT Blender's renderer, IK, geometry
node engine, GPU pipeline, or a complete source-code reconstruction.
These binary inventory numbers are not counts of user-facing features.
