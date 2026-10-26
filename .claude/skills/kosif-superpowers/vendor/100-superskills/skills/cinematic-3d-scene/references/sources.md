# مصادر «مشهد سينمائي ثلاثي الأبعاد» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## webgpu-threejs-tsl (2221-webgpu-threejs-tsl)

- الترخيص: **MIT**  ·  الأصل: https://github.com/managedcode/dotnet-skills/tree/8f26916118d9ad737db167bf1cd032455414b0c0/external-sources/upstreams/webgpu-claude-skill
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2221-webgpu-threejs-tsl/8405-webgpu-threejs-tsl
- الوصف: Comprehensive guide for developing WebGPU-enabled Three.js applications using TSL (Three.js Shading Language). Covers WebGPU renderer setup, TSL syntax and node materials, compute shaders, post-processing effects, and WGSL integration. Use this skill when working with Three.js WebGPU, TSL shaders, node materials, or GPU compute in Three.js.

```markdown
# WebGPU Three.js with TSL

TSL (Three.js Shading Language) is a node-based shader abstraction that lets you write GPU shaders in JavaScript instead of GLSL/WGSL strings.

## Quick Start

```javascript
import * as THREE from 'three/webgpu';
import { color, time, oscSine } from 'three/tsl';

const renderer = new THREE.WebGPURenderer();
await renderer.init();

const material = new THREE.MeshStandardNodeMaterial();
material.colorNode = color(0xff0000).mul(oscSine(time));
```

## Skill Contents

### Documentation
- `docs/core-concepts.md` - Types, operators, uniforms, control flow
- `docs/materials.md` - Node materials and all properties
- `docs/compute-shaders.md` - GPU compute with instanced arrays
- `docs/post-processing.md` - Built-in and custom effects
- `docs/wgsl-integration.md` - Custom WGSL functions
- `docs/device-loss.md` - Handling GPU device loss and recovery
- `docs/limits-and-features.md` - WebGPU device limits and optional features

### Examples
- `examples/basic-setup.js` - Minimal WebGPU project
- `examples/custom-material.js` - Custom shader material
- `examples/particle-system.js` - GPU compute particles
- `examples/post-processing.js` - Effect pipeline
- `examples/earth-shader.js` - Complete Earth with atmosphere

### Templates
- `templates/webgpu-project.js` - Starter project template
- `templates/compute-shader.js` - Compute shader template

### Reference
- `REFERENCE.md` - Quick reference cheatsheet

## Key Concepts

### Import Pattern
```javascript
// Always use the WebGPU entry point
import * as THREE from 'three/webgpu';
import { /* TSL functions */ } from 'three/tsl';
```

### Node Materials
Replace standard material properties with TSL nodes:
```javascript
material.colorNode = texture(map);        // instead of material.map
material.roughnessNode = float(0.5);      // instead of material.roughness
material.positionNode = displaced;         // vertex displacement
```

### Method Chaining
TSL uses method chaining for operations:
```javascript
// Instead of: sin(time * 2.0 + offset) * 0.5 + 0.5
time.mul(2.0).add(offset).sin().mul(0.5).add(0.5)
```

### Custom Functions
Use `Fn()` for reusable shader logic:
```javascript
const fresnel = Fn(([power = 2.0]) => {
  const nDotV = normalWorld.dot(viewDir).saturate();
  return float(1.0).sub(nDotV).pow(power);
});
```

## When to Use This Skill

- Setting up Three.js with WebGPU renderer
- Creating custom shader materials with TSL
- Writing GPU compute shaders
- Building post-processing pipelines
- Migrating from GLSL to TSL
- Implementing visual effects (particles, water, terrain, etc.)

## Resources

- [Three.js TSL Wiki](https://github.com/mrdoob/three.js/wiki/Three.js-Shading-Language)
```

## three-webgl-game (2696-game-studio)

- الترخيص: **MIT**  ·  الأصل: https://github.com/openai/plugins/tree/5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f/plugins/game-studio
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2696-game-studio/10369-three-webgl-game
- الوصف: Implement browser-game runtimes with plain Three.js. Use when the user wants imperative scene control in TypeScript or Vite with GLB assets, loaders, physics, and low-level WebGL debugging.

```markdown
# Three WebGL Game

## Overview

Use this skill for the default non-React 3D path in the plugin. This is not generic WebGL advice. It is an opinionated stack for browser 3D work:

- `three`
- TypeScript
- Vite
- GLB or glTF 2.0 assets
- Three.js loaders such as `GLTFLoader`, `DRACOLoader`, and `KTX2Loader`
- Rapier JS for physics
- SpectorJS for GPU and frame debugging
- DOM overlays for HUD, menus, and settings

Use this skill when the project wants direct scene, camera, renderer, and game-loop control. If the app already lives in React, route to `../react-three-fiber-game/SKILL.md` instead.

## Use This Skill When

- the app is plain TypeScript or Vite rather than React-first
- the project wants direct imperative control over the render loop
- the user asks for Three.js specifically
- the runtime needs engine-like control over scene, camera, loaders, and physics

## Do Not Use This Skill When

- the 3D scene lives inside an existing React app
- the main problem is shipped-asset optimization rather than runtime code
- the user explicitly chose Babylon.js or PlayCanvas

## Core Rules

1. Keep simulation state outside Three.js objects.
   - Game rules, AI, quest state, timers, and progression should not live inside meshes or materials.
2. Treat the render graph as an adapter.
   - Scene graph, cameras, materials, loaders, and post-processing are view concerns layered over simulation state.
3. Keep camera behavior explicit.
   - Orbit, follow, chase, rail, and first-person styles each need their own control boundary.
4. Keep UI out of WebGL unless the presentation absolutely depends on it.
   - Menus, HUD, inventories, and settings should default to DOM.
5. Use GLB or glTF 2.0 as the default shipping model format.
   - Do not build the runtime around DCC-native formats.
6. Use Rapier instead of ad hoc collision code when the game has meaningful 3D physics or collision response.
7. Keep the first playable view low-chrome.
   - Default to one compact objective or status cluster plus transient prompts.
   - Long notes, lore, and controls references should be collapsed until asked for.
   - Do not frame the scene with multiple equal-weight cards during normal play.

## Initial Scaffold UX

For exploration, traversal, and character-control prototypes, start with a sparse shell:

- one edge-aligned objective chip
- one transient controls hint
- one optional compact status strip

Only add larger UI surfaces when the game loop truly requires them. Journal, quest log, codex, map, and settings surfaces should open on demand, not occupy the viewport by default.

## Recommended Structure

Use the module shape in `../../references/three-webgl-architecture.md`, then keep these boundaries clean:

- `simulation/`: rules, progression, state, and AI
```

## web-3d-asset-pipeline (2696-game-studio)

- الترخيص: **MIT**  ·  الأصل: https://github.com/openai/plugins/tree/5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f/plugins/game-studio
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2696-game-studio/10370-web-3d-asset-pipeline
- الوصف: Prepare and optimize browser-game 3D assets. Use when the user asks for GLB or glTF shipping work, including Blender cleanup and export, collision or LOD setup, compression, texture packaging, and runtime validation.

```markdown
# Web 3D Asset Pipeline

## Overview

Use this skill for shipped 3D assets, not runtime scene code. The default output format for browser 3D work in this plugin is GLB or glTF 2.0. The goal is predictable runtime assets, not whatever the DCC tool happened to export first.

This guidance is engine-agnostic and can serve Three.js, React Three Fiber, Babylon.js, or PlayCanvas.

## Use This Skill When

- the task is about GLB or glTF shipping format
- the task is about model cleanup, texture packaging, compression, LOD, or collision proxies
- the runtime stack is already chosen and the remaining problem is asset quality or size

## Do Not Use This Skill When

- the task is about scene, camera, renderer, or game-loop structure
- the task is purely about React versus vanilla Three.js routing
- the user is still deciding between runtime engines

## Default Pipeline

1. Author and clean the source asset in a DCC tool such as Blender.
2. Export to GLB or glTF 2.0.
3. Optimize with glTF Transform.
4. Validate naming, pivots, transforms, material reuse, and texture budgets.
5. Add collision proxies, LOD strategy, and baked-lighting assumptions as needed.
6. Ship the optimized asset and load it with engine-native GLTF support.

## Format Rules

- Default shipping format: GLB or glTF 2.0.
- Do not treat FBX, OBJ, or DCC-native formats as the long-term runtime contract.
- Apply or normalize transforms before shipping.
- Keep units, pivots, and orientation conventions consistent across the whole asset set.

## Optimization Rules

- Use glTF Transform for pruning, deduplication, simplification, and packaging.
- Use geometry compression intentionally.
  - Draco is a valid option when decode cost and compatibility fit the runtime.
  - Meshopt is often a strong default for web delivery.
- Compress textures deliberately.
  - Use KTX2 or BasisU when the runtime stack supports it.
  - Use WebP or AVIF where they make sense in the broader asset pipeline.
- Reuse materials and textures where possible to cut memory and draw-call cost.

## Runtime-Ready Asset Rules

- Keep model hierarchy names stable and meaningful.
- Set pivots and origins for gameplay interaction, not just for DCC convenience.
- Author explicit collision proxies for physics-heavy scenes.
- Decide whether lighting is dynamic, baked, or hybrid before final export.
- Plan LODs for large environments or repeated props.
- Keep texture resolution proportional to on-screen use, not source-art ambition.

## Common Failure Modes

- Shipping raw DCC exports without cleanup
- Too many unique materials
- Texture sizes far above visible need
- Missing collision proxies
- Scale or pivot mismatches between assets
- Runtime code compensating for asset mistakes that should be fixed upstream

## References
```

## awwwards-motion (95-awwwards-motion)

- الترخيص: **MIT**  ·  الأصل: https://github.com/adamperlis/adam-plugins/tree/e41984f68ab8a53f028d078c6070ec8658fd41ac/plugins/awwwards-motion
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/95-awwwards-motion/204-awwwards-motion
- الوصف: Build Awwwards-quality web experiences with spring physics, GLSL shaders, R3F, post-processing, particles, Framer Motion, and interactive 3D. Use for creative coding, WebGL, cinematic UI, or award-winning motion design.

```markdown
# Awwwards-Quality Motion & Creative Web Development

You are an expert creative web developer specializing in GLSL shaders, React Three Fiber (R3F), Three.js, WebGL post-processing, particle systems, Framer Motion animations, and interactive 3D web experiences. You build things from first principles, with deep understanding of the math, and always with interactive, visual results.

This skill is inspired by the craft behind Awwwards Site of the Day winners — the sites that set the bar for motion, interaction, and visual fidelity on the web. It combines a physics-based motion system with a comprehensive creative coding toolkit, treating the interface like a physical, 3D environment rather than flat rectangles. The goal is to close the gap between what award-winning studios ship and what most teams think is possible.

Built from deep study of Maxime Heckel's blog (blog.maximeheckel.com), Codrops (tympanus.net/codrops), and the broader creative web ecosystem that drives Awwwards, FWA, and CSS Design Awards winners.

## Core Technology Stack

- **3D & Shaders**: React Three Fiber, Three.js, GLSL (vertex + fragment shaders), WebGL Render Targets / FBOs, @react-three/drei, @react-three/postprocessing, Lamina (composable shader layers), WebGPU/TSL (emerging)
- **Animation**: Framer Motion (layout animations, AnimatePresence, shared layout animations, Reorder), GSAP + ScrollTrigger, spring physics
- **Frontend**: React/Next.js, TypeScript, CSS Variables, MDX, Design Systems
- **Creative Coding Patterns**: Noise functions (Perlin, Simplex, Curl, FBM), Signed Distance Functions, Raymarching, Volumetric Rendering, Particle Systems (buffer geometry + FBO), Post-Processing Pipelines

---

## 1. Physics-Based Motion

All motion uses spring physics. Never use duration-based easing (`ease-in-out`, `cubic-bezier`). Springs feel alive because they respond to velocity, tension, and friction.

### Spring Constants

```
Stiffness: 300
Damping: 30
Mass: 1
```

### Behavior

- Elements slightly overshoot their target (1.05x scale) before settling to 1.0x
- Transitions land between 400ms–700ms depending on travel distance
- Motion should feel buttery-smooth with natural settle, not robotic

### Implementation

**Framer Motion (React):**
```jsx
<motion.div
  animate={{ scale: 1 }}
  transition={{
    type: "spring",
    stiffness: 300,
    damping: 30,
    mass: 1
  }}
/>
```

**GSAP:**
```js
gsap.to(element, {
  scale: 1,
  duration: 0.6,
  ease: "elastic.out(1, 0.5)"
});
```

**CSS (fallback only):**
```css
transition: transform 500ms cubic-bezier(0.34, 1.56, 0.64, 1);
```

## 2. The Glass Surface

Every elevated surface uses a multi-layered glass stack. This is not simple `backdrop-filter: blur()` — it is a composed material.

### Layer Stack (bottom to top)
```

## threejs-data-visualization (2690-build-web-data-visualization)

- الترخيص: **MIT**  ·  الأصل: https://github.com/openai/plugins/tree/5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f/plugins/build-web-data-visualization
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2690-build-web-data-visualization/10332-threejs-data-visualization
- الوصف: Render WebGL-accelerated data visualizations with Three.js, raw WebGL, deck.gl, luma.gl, PixiJS, Sigma.js, Plotly WebGL traces, ECharts GL, CesiumJS, Babylon.js, or related GPU libraries. Use when the visualization needs true spatial structure, dense 2D or 3D GPU rendering, particle or flow animation, volumetric views, or interactive exploration that adds real analytical value.

```markdown
# Three.js and WebGL Data Visualization

## Overview

Use this skill when the user truly benefits from 3D, GPU-heavy 2D, shader-driven animation, or WebGL-accelerated interaction. Three.js is appropriate for volumetric data, 3D point clouds, spatial trajectories, surfaces, scientific or immersive scenes, and custom particle systems. WebGL or WebGL-backed libraries are also appropriate for dense 2D scatterplots, animated networks, flow maps, particle trails, GPU aggregation, or custom shader effects that exceed practical SVG/DOM limits and are not a good fit for Canvas2D.

Default assumption: use the simplest truthful renderer that meets the scale and interaction requirements. 3D is justified only when depth carries analytical meaning. WebGL is justified when GPU throughput, shader control, large mark counts, or animation quality matter enough to offset accessibility, export, debugging, bundle, and GPU-memory costs. Cosmetic 3D or decorative particles are regressions.

Mobile GPUs, touch gestures, battery, thermal limits, and permissions can change the renderer choice. Use `../../references/foundations/mobile-first-responsive-visualization.md` for mobile portrait/landscape contracts, AR/camera/motion/vibration decisions, visual viewport behavior, spotty connection handling, and touch-first controls.

## Choose WebGL When

- the data is inherently spatial, volumetric, trajectory-based, or surface-based
- depth, orbit, slicing, or perspective reveals structure unavailable in 2D
- an editorial story needs camera states to reveal a meaningful surface, volume, terrain, or multiaxis relationship
- GPU instancing, texture-backed data, or shader-based rendering materially improves scale
- dense 2D plots, networks, or maps need hundreds of thousands to millions of marks, continuous pan or zoom, or real-time filtering
- animated flow, trips, particles, or transitions must remain smooth without generating thousands of DOM or SVG elements
- the view needs GPU picking, custom blending, post-processing, or shader effects tied to data attributes
- the experience needs immersive or exploratory navigation
- AR or camera-backed spatial inspection adds analytical value and has a non-permission fallback

## Avoid WebGL When

- the same comparison is clearer in 2D
- labels and exact values dominate the task
- the chart will mostly be consumed as a static document
- a declarative grammar, D3/SVG, or Canvas2D can handle the mark count with less maintenance and better export/accessibility
- the required effect is mostly decoration, novelty, or attention capture without a specific analytical verb
- the page will show many small charts where WebGL context pressure and GPU memory would outweigh per-chart speed

## Library Selection
```

## thermal-finger-trail (100-ui-motion)

- الترخيص: **MIT**  ·  الأصل: https://github.com/adamperlis/adam-plugins/tree/e41984f68ab8a53f028d078c6070ec8658fd41ac/plugins/ui-motion
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/100-ui-motion/211-thermal-finger-trail
- الوصف: Build an interactive heat-camera field that a finger or cursor smears like wet paint — a WebGL fragment shader with a domain-warped thermal blob, a seven-stop heat ramp, a velocity-carrying pointer trail, and a press ripple. Use when the user wants a thermal/heatmap effect, a "finger through paint" or smudge interaction, a living gradient that reacts to touch, a trackpad/touch-surface hero, or the

```markdown
# Thermal Finger Trail

Use this skill to build a surface that looks like a thermal camera and responds to touch like wet paint: drag a finger across it and the heat field is dragged along with it, then slowly heals. Press, and a ripple pushes the colour outward and briefly heats it.

It comes from Clicker's trackpad disc (an iPhone app that turns the phone into a trackpad). On the site, the disc *is* the product: the place your finger goes.

![Clicker's thermal disc, mid-smear](assets/thermal-finger-trail-reference.png)

The complete working version is `references/thermal-finger-trail.html`: one file, no build step, with a DialKit tuning panel. Start from it rather than from scratch.

## When it fits

- A touch or pointer surface that should feel physical: a trackpad, a canvas, a hero object people want to play with.
- A brand that can carry a heat-camera palette (teal → green → yellow → orange → red).
- One focal object on a dark ground. It's a show-piece, not a background behind body copy: the field is busy and the contrast shifts constantly.

Don't put text over it, and don't run it full-screen on a page that also needs to scroll smoothly on low-end phones without the DPR cap below.

## How it works

Everything is one fragment shader on a single full-canvas triangle. There are no textures, no render targets and no feedback buffers: the "memory" of the finger is a short list of points passed in as uniforms each frame.

1. **The field.** Fractal noise (`fbm`, 5 octaves) warps the coordinates, and a second fbm, fed by the first, warps them again ("warp the warp"). That gives curling, fluid flow. A slow *melt* cycle (6 s) swells the warp and slumps the shape downward, then recovers.
2. **The blob.** In the warped space, a soft blob breathes between round and a touch tall or wide: a polar wobble of two low-frequency sines. Distance from its edge gives two values: `mask` (inside or outside) and `inside` (how deep).
3. **Heat.** Heat is a number from 0 to 1. Outside the blob it's a warm, noisy background (0.34–0.66, never white, never dark). Inside, it ramps from a cool core (0.20) to a hot rim (0.64). A hard contour is cut where green meets yellow, so the core reads crisp.
4. **Colour.** `thermal(heat)` maps heat through seven stops with `smoothstep` blends at 0, .12, .30, .45, .60, .78 and 1. Heat is capped at 0.75, so the field tops out at orange or red and never blows out to white.
5. **The finger.** JavaScript keeps the last 24 points of the pointer's path. Each holds a position, its **velocity** (the step from the previous point) and an **age** that fades from 1 to 0 over 1.6 s. In the shader, every point within reach pushes the coordinates along its own velocity:

   ```glsl
   vec2 disp = vec2(0.0);
   for (int i = 0; i < 24; i++) {
```
