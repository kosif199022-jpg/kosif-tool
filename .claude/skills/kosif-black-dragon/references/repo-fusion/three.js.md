# three.js — REA dissection (r0.187 @3f7edc3d75e054bc755dad56c1c95c62f63a3561)

License: MIT (vendor only `build/*.js`; `examples/` holds third-party assets under other licenses). Stars ≈118k.

## New for the Dragon (vs vendored three.module.js + 3D playground + per-frame Playwright shots)
1. **Virtual clock for deterministic frames.** `src/nodes/core/NodeFrame.js:310-316` derives `time`/`deltaTime` from `performance.now()`; TSL `Timer.js:10-26`, `Oscillators.js:11` and `Clock.js:71,120` depend on it too, so frames differ run to run. Fix: inject `performance.now`, `Date.now` and `requestAnimationFrame` with a frame-indexed clock before modules load (`native_three.py clock-shim`). `Timer.js:156` accepts `update(timestamp)`. Always `await renderer.init()` before rendering (`Renderer.js:899`).
2. **Frame-render harness**: `index.html` with an importmap for `three/webgpu` + `three/tsl`, a Playwright driver with swiftshader flags, `renderFrame(n)`, optional `forceWebGL` (`WebGPURenderer.js:41-57`).
3. **TSL post-processing nodes** in `examples/jsm/tsl/display` (49 files): bloom, DoF, motionBlur, Lut3D, Film, CRT, BleachBypass, lensDirt, SSR, SSGI, GTAO, godrays, TAA. Temporal nodes (SSGI, TRAA, AfterImage) need sequential frames from 0, not random access.
4. **`TransitionNode`** (`TransitionNode.js:10`): textureA→textureB blend with mask + threshold; plus `curlNoise`, voronoi, Bayer, raymarching helpers.
5. **`docs/llms-full.txt`** (8,596 lines, offline, covers TSL); root `llms.txt` is 281 bytes and points to threejs.org.

Caveats: headless WebGPU varies by machine → use `forceWebGL:true` or swiftshader. `TextGeometry` does not shape Arabic.

## Native module: `native_three.py`
Commands: `catalog <repo>`, `clock-shim --fps N`, `harness <dir>`, `self-test` (`--json` goes before the command).
Self-test: `self-test OK: catalog parse, harness html+driver, virtual clock frame15@30fps=500ms` — the shim was executed in Node (performance.now=500ms, Date.now offset, rAF). The harness HTML was generated but NOT tried in a real browser/GPU.

## REA evidence log
- `open_binary` build/three.module.js sha256 a3428b319b769824bd315b9dc8efa6ae50dcacee9eff0acd2e27f345885cb190
- `inspect_artifact` summary → ev_555cf65bf72ed0f2ccfb0fcd20b17e1e4f701eb3ebc4b026e17c38827c18aed3 (one-file inventory, low value)
- `analyze_javascript_application` on build/ → provider_timeout 120s, partial ev_2d5cffb3f962a5cba0b592007a84c69fe231b931f4b0e3b3e7eb2551eded77de (not retried)
- `close_binary` done; `analyze_web_bundle` not run (needs a live CDP page)
- src/nodes, Renderer.js, tsl and llms read by hand (grep/sed).
