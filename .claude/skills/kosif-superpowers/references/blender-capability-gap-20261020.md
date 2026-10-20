# Evidence-led Blender and KOSIF gap review — 20 October 2026

## What was actually reviewed
- Official Blender 5.2.2 Windows runtime, obtained from blender.org, verified by SHA-256 before extraction. Blender Python source analysis on 810 packaged Python files (810 parsed); this is not analysis of every C++ function in Blender.
- REA 6.7.0 and Ghidra 12.1.4 read-only analyzed Blender's BlendThumb.dll. Ghidra inventoried **557 procedures and 237 strings**. BlendThumb is a thumbnail-helper DLL, not the whole 3D engine. No claim is made to have reverse engineered all Blender functions.
- KOSIF native_3d.py renders and exports MP4 without Blender. Local suite: 17/17 native_3d tests passed; separate three cat-rescue demo tests passed. These verify a limited software rasterizer and procedural demonstrations, not realistic character animation.
- KOSIF Blender bridge renders validated primitive scenes, .blend, .glb, .png; new blender_motion_video.py and Blender worker now produce H.264 MP4 headlessly with codec/frame verification. 24-frame/128x128 and 120-frame/256x256 real render tests passed.
- Desktop «تجربة»: recorded 2,552 files in 953 directories, 18,553,712,109 total bytes at last full read-only census; all files were inventoried, not all reverse engineered or executed.
- Atlas: 14,793 index entries (14,708 regular and 85 copyleft); all catalog records had static metadata classification, not line-by-line execution or source validation.

## Capability map

| Capability | KOSIF status | Gap |
|---|---|---|
| Primitive modeling (cube, sphere, cone, torus, cylinder) | Implemented in native_3d and Blender wrapper | Complex topology / subdivision / sculpt absent |
| Camera and object keyframes | Blender wrapper verified, native3d basic animation verified | Graph editor, bones constraints, 3D IK/FK absent |
| 3D depth buffering | Native3D z-buffer and primitive renderer tests verified | Antialiasing, global illumination, path tracing, transparent compositing limited or absent |
| H.264 video export | Verified via native3d/FFmpeg and Blender/Workbench/FFmpeg | Audio and multitrack timeline not present in Blender JSON wrapper |
| Materials and lighting | Blender API wrapper for simple diffuse colors and one light | PBR material graph, texture painting, volumetrics and Cycles equivalence not present in native3d |
| 2D human gestures/face | character_fullbody.py (walk/run/wave/smile/blink/nod) | Not full 3D skeleton, mocap, or accurate lip sync |
| Realistic rescue with person and cat | Procedural low-poly Blender demo 5 seconds | Licensed rigged realistic assets, acting, fur, physical contact and cinematic review needed |
| Grease Pencil, sculpt, geometry nodes, cloth/fluids, tracking | Research candidates from Blender capabilities | Not implemented or validated in native KOSIF renderer |

## Tool choice

REA/Ghidra installed and suited to read-only native binary examination; for open-source Blender the upstream source and documented bpy API generally give richer, more reliable semantic insight than decompiling binary and guessing its behavior. Hopper official downloads are for macOS/Linux; Windows version unsupported per hopperapp.com/faq.html. Do not install unofficial binaries, paid licenses or compromised installers.

## Transfer rules

Borrow ideas and public programming interfaces with proper source/licensing documentation. Original KOSIF code is not a direct transplant of Blender GPL engine modules. Any later Blender GPL source reuse requires complying with license terms. Third-party Atlas skills must be individually reviewed before execution or redistribution.

## Next evidence gates

1. Capture representative Blender/Cycles, 3D armature/rigging and Grease Pencil outputs.
2. Build original KOSIF feature implementations one at a time, with real artifact proof and regression tests.
3. Check Blender API and KOSIF native results at equivalent camera/geometry inputs; report measurable differences.
4. Audit remaining «تجربة» binaries selectively by risk/value; an all-files metadata census is not exhaustive decompilation.
