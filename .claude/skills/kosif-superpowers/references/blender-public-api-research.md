# Evidence-scoped Blender 5.2.2 capability study — 2026-10-19

**Source:** official portable Blender 5.2.2 for Windows, downloaded from download.blender.org and SHA-256 matched to the published Scoop manifest. The local study used the official program's public Python bpy interface, plus a bounded REA/Ghidra investigation. None of the binary implementation is copied into KOSIF.

## Blender public API inventory (actual headless execution)

A read-only bpy namespace/type introspection on the installed Blender returned:
- 77 operator namespaces, 2,499 registered operator names, 4,023 bpy type names.
- The domain mapping is **overlapping**; do not add categories to derive unique totals.
- Modeling: 509 names across selected namespaces; sculpt/paint: 147; Grease Pencil/2D: 130; armature/pose/rig: 118; animation/NLA: 251; nodes: 191; rendering: 241; composition: 182; sequencing/audio/video: 250; physics: 71; import/export: 122; typography: 66.
- Source evidence is the generated local JSON at KOSIF_RESEARCH_PRIVATE_20261019/blender_API_evidence_20261019.json, not a copied source tree.

**Caution:** Counted commands are registration introspection, not performance or unit tests of each operator. Operators can depend on contexts, add-ons or other assets.

## REA / Ghidra bounded static study

- REA v6.7.0 successfully inspected the shipped blender-launcher.exe and blender_cpu_check.dll as PE artifacts, including reproducible digests and structure.
- Ghidra v12.1.4 through REA successfully completed a read-only static analysis of blender_cpu_check.dll with 8 observed segments, **121 Ghidra-defined procedures and 62 defined strings**. These are low-level binary observations, not 121 user-facing capabilities or analysis of Blender's modeling/rendering core.
- The complete blender.exe (113 MB), Cycles, geometry nodes, simulation nodes and GPU backend have **not** been comprehensively reverse engineered. Prefer the official open-source Blender repository, official API documentation and behavioral tests for functionality research.

## Actual tested KOSIF outputs

- The optional Blender-backed bridge produced PNG, GLB (including an animation channel) and editable .blend examples on the local PC.
- A separate original Blender rescue-cartoon proof of exactly 120 frames / 5 seconds at 24 fps was encoded into H.264 768×432 MP4; verification used ffprobe. Its project and MP4 are retained on the user's laptop; the repo has an independent proof directory.
- The Blender-free KOSIF native_3d.py uses only Pillow and FFmpeg, with no Blender runtime. It has an independently tested 5-second 640×360 MP4 demonstration with 120 H.264 frames. This is a **small software-rendering subset** only; not a full Blender replacement.

## Transfer plan

1. Retain the verified Blender bridge for advanced 3D.
2. Enhance the independent native core with proper z-buffer, mesh IO, scene graph, shading, IK, skinning, materials and compositing, in isolated reviewed commits.
3. For every added feature, require a real scene file, deterministic render output and pixel/frame assertions rather than a paper catalog badge.
4. Review every dependency's license; Blender's GPL does not grant a license to transplant arbitrary source into KOSIF under a different incompatible license.
