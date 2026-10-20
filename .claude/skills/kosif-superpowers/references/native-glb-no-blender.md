# KOSIF Native 3D: Blender-free GLB export (experimental)

Independent implementation: no Blender, Houdini, Adobe, Hopper, Ghidra, or REA required to execute it. This tool serializes strict original JSON into binary glTF 2.0 (.glb) with Python standard library only.

This is a small verified geometry/keyframe capability, NOT a complete renderer, rigging suite, sculpting platform, compositor, Grease Pencil implementation, or Blender replacement.

## Usage

From repo root:

    python .claude/skills/kosif-superpowers/scripts/native_glb.py --scene .claude/skills/kosif-superpowers/templates/blender-demo.json --output native-demo.glb

The output must not already exist and its folder must exist (otherwise an argparse error, exit 2); an invalid or unreadable scene prints `{"ok": false, "error": ...}` to stderr with exit 1. Input uses the existing kosif.blender.v1 schema from blender_bridge.py for cube/sphere, colors, positions, scales, keyframes, fps, and frame counts. That schema is Blender-style Z-up; like Blender's own glTF exporter, the GLB is written Y-up: positions (mesh vertices, node translations, keyframes) map (x, y, z) -> (x, z, -y) and scale (sx, sy, sz) -> (sx, sz, sy), so an object at [0, 0, 3] lands at glTF [0, 3, 0]. Unlike blender_bridge.py, the exporter never invokes Blender. GLB output can be opened in a glTF-compatible viewer.

## Verified scope and remaining gaps

- scripts/native_glb.py: original GLB header, JSON and binary chunks, scene graph, cube/sphere geometry, base color and linear translation keyframes, with Z-up to Y-up axis conversion.
- evals/test_native_glb.py: deterministic output, chunk checks, materials, animations, reject invalid input and sample-scene compatibility.
- Prototype checked with independent trimesh v4.11.1: two meshes and three graph nodes loaded. This is not proof of compatibility with every viewer.
- No interactive rasterization, camera systems, shader node graphs, advanced IK, character deformation, Blender physics, or MP4 output.
- No external downloads, external executables or dynamic Python source execution.
- Blender 5.2.2 bundled Python AST audit inspected 810 files; all parsed. Filename classifications (overlap allowed): animation/rig 150, video/composite 104, materials 84, geometry 36, drawing/brush 15. These are *source-path classifications*, not confirmed application capabilities. Blender C/C++ internals are outside that AST scope.
- A separate read-only REA/Ghidra investigation of selected Blender binary components is not the same thing as capability transfer.

Catalog status should describe this as LIMITED BLENDER-FREE GLB GEOMETRY AND ANIMATION OUTPUT, not as all Blender capabilities or an AI video generator.
