# Three.js — KOSIF Superpowers 3D + Motion Capability Bridge

**Status:** Tested on the user's Windows workstation on 20 Oct 2026, limited to the recorded
Three.js example. This is a new **actual local renderer** accessible by Node + Chrome,
not an indication that the ChatGPT model itself has acquired native 3D execution.

## Capability matrix

| Capability | Verified in this run | Notes |
|---|---|---|
| Scene graph, camera, procedural geometries | YES | Native Three.js r186, mesh scene |
| PBR metallic materials, lights, color handling | YES | WebGL renderer real output |
| Shader pipeline | PARTIAL | Built-in materials only; no custom GLSL/TSL |
| Deterministic animation, kinetic captions | YES | `renderAt(milliseconds)`, original timeline |
| Particle fields | YES | Procedural `Points` |
| Raycaster interaction | API/STRUCTURE | Click handler included; interactive browser test not completed |
| glTF 2.0 loader | API IMPORT | No glTF payload actually loaded |
| WebGPU backend | NOT TESTED | WebGL verified; WebGPU has browser-dependent fallback |
| Blender rendering / offline photoreal | NOT INCLUDED | Three.js runs interactive real-time scenes |
| Frame capture / actual video | See run receipt | Chrome screenshots; FFmpeg verified only if receipt `ffmpegExport=true` |
| Sound/music beat synchronization | NOT INCLUDED | Requires supplied/licensed audio and explicit alignment |
| Native 60fps 1080x1920 output | NOT VERIFIED | Demo defaults to 720x1280 at 12 fps |

## Practical skills gained

1. **Script-to-scene:** turn a finite brief into a scene graph, camera and material plan.
2. **Deterministic stage lighting:** key/fill/rim lights plus tone mapping and material response.
3. **Timecode rendering:** fix each frame to one time value, not wall-clock playback.
4. **Cinematic object motion:** nested orbital rigs, turntable mesh animation, camera framing.
5. **Lightweight procedural particle fields:** reproducible seeded positions.
6. **Graphic overlays:** HTML/CSS headings and captions aligned with scene phases.
7. **Real delivery gate:** assert WebGL rendered objects, zero browser errors, and pixel differences.
8. **MP4 encoding:** FFmpeg command runs only on generated, verified frames.
9. **Portable 3D demo:** version-pinned dependencies in a standalone folder without copying
   `node_modules` or overwriting the canonical skill's original 4,751-power catalog.

## Recommended selection contract

- Triggers: `three.js`, `threejs`, `webgl`, `motion graphics 3d`,
  `motion graphics Claude`, `موشن جرافيك ثلاثي الأبعاد`, `مشهد 3D`.
- Prefer existing `kosif-media-motion` / existing native motion toolkit for non-3D editing.
- When 3D WebGL genuinely helps, inspect `examples/threejs-motion-lab` and choose the smallest
  independent part required, not entire assets or a new 3D engine.
- For actual work check current Node, npm, Chrome, FFmpeg, WebGL backend and rights to media;
  never assert browser/video creation from a `SKILL.md` mention alone.
- Any production merge into Earth or user websites needs isolated company/test data and
  existing site approvals; this task only extends KOSIF Superpowers.
- Current user's YouTube video metadata was retrieved but the auto-transcript was rate-limited;
  do **not** present shot-by-shot claims as verified.

## Real build / smoke

From `examples/threejs-motion-lab`:

```powershell
npm ci --ignore-scripts --no-audit
npm test
node render.mjs --smoke --out "C:\\Temp\\kosif-threejs-smoke"
node render.mjs --fps 12 --out "C:\\Temp\\kosif-threejs-video"
```

Read `receipt.json`; success requires `verifiedWebGL=true`, non-equal `frameHashes`,
zero `browserErrors`, and `ffmpegExport=true` **before saying video exported**.
Do not infer GPUs, WebGPU or high-quality 3D from installation alone.

## Source / licensing

Three.js MIT; Playwright-core Apache-2.0; npm pinning in project manifest/lock.
Official reference: https://threejs.org/manual/en/installation.html.
Provenance note: user-supplied URL https://www.youtube.com/watch?v=CCUSpJkAfgU;
metadata title "Claude + Three.js = Premium 3D Motion Graphics"
(Matt Penny | Applied AI, 739 seconds). No transcript was available (HTTP 429).
No video code or frames copied.
