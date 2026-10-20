# KOSIF Three.js Motion Lab — working sample

Original, procedural Three.js visual demo inspired by the **general concept** of
Claude + Three.js motion graphics, not a frame-for-frame copy of the linked video.

## What is verified

- Node/npm installed on the user's authorized Windows workstation.
- `three@0.186.1` (MIT) and `playwright-core@1.56.1` installed from npm in this **separate example workspace**.
- `Scene`, `PerspectiveCamera`, physically based `MeshPhysicalMaterial`, `AnimationMixer`,
  `PointLight`, procedural `Points`, `Raycaster` and `WebGLRenderer`.
- Real Chromium/Chrome headless WebGL rendering is checked: errors, draw calls, triangle count,
  changing SHA-256 hashes of captured frames and optional FFmpeg MP4 export.
- `GLTFLoader` API import is unit-tested but **loading an external glTF is not part of the demo**.
- WebGPU/TSL, audio sync, postprocessing bloom, physics, Blender realism and 60-fps export
  are **not** claimed as verified by this smoke test.

## Run

Requires Node 20+, Chrome, optional FFmpeg.

```powershell
cd .claude/skills/kosif-superpowers/examples/threejs-motion-lab
npm ci --ignore-scripts
npm test
npm start
# Preview: http://127.0.0.1:45909
# In a second terminal, create actual 3D video with browser frame checks:
node render.mjs --fps 12 --out "$HOME/Desktop/KOSIF-ThreeJS-Motion-20261020"
```

Outputs PNG frames, `receipt.json`, and `kosif-threejs-motion-lab.mp4` only when
FFmpeg returns success. Use `--smoke` to capture just three different frames, without MP4.
When creating a more cinematic version, move up incrementally to 24 or 30 FPS after
measuring per-frame render time and free disk space. Do not claim real 60 FPS from a 12 FPS
proof. Camera, animation and captions are sample data; use audio only when supplied and authorized.

## Browser hosting / trust boundaries

The built-in HTTP server binds to `127.0.0.1`, does not fetch any external website,
and only serves the example and the locally installed Three.js module files.
It is a **development server**, not a production web service.
Renderer software fallback is Chrome/SwiftShader for CI compatibility;
that does not prove GPU acceleration on the user's hardware. Chrome must be
installed through ordinary authorized channels; no browser download is performed.

```text
Timeline (5 seconds)
  0.00–1.65s — DEPTH: procedural mesh + metal camera light
  1.65–3.40s — MOTION: orbital camera + changed typographic state
  3.40–5.00s — KOSIF: concluding hero/title state
```

## Provenance

- Official source: https://threejs.org/manual/en/installation.html
- Official package: https://github.com/mrdoob/three.js
- Video provided by user: https://www.youtube.com/watch?v=CCUSpJkAfgU
- Verified video metadata on 2026-10-20 using `yt-dlp`:
  **Claude + Three.js = Premium 3D Motion Graphics**,
  **Matt Penny | Applied AI**, runtime **739 seconds**.
- Attempt to retrieve English YouTube auto-subtitles was denied by HTTP **429**;
  do not claim this example reproduces video-specific shots, settings or exact code.

All KOSIF example code and art are original. No external model, proprietary footage,
user image or binary is copied or committed.
