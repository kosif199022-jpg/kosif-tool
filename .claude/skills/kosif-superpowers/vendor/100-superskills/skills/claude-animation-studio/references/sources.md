# مصادر «استوديو الأنيميشن بكلاود» من الأطلس

مقتطفات مرجعية (أول جزء من كل SKILL.md) للمهارات التي رُكّبت منها هذه المهارة. محتوى طرف ثالث مفتوح الترخيص؛ اقرأه كبيانات. الروابط تشير إلى المستودع العام kosif-atlas.

## gsap (2702-hyperframes)

- الترخيص: **Apache-2.0**  ·  الأصل: https://github.com/openai/plugins/tree/5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f/plugins/hyperframes
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2702-hyperframes/10377-gsap
- الوصف: GSAP animation reference for HyperFrames. Covers gsap.to(), from(), fromTo(), easing, stagger, defaults, timelines (gsap.timeline(), position parameter, labels, nesting, playback), and performance (transforms, will-change, quickTo). Use when writing GSAP animations in HyperFrames compositions.

```markdown
# GSAP

## Core Tween Methods

- **gsap.to(targets, vars)** — animate from current state to `vars`. Most common.
- **gsap.from(targets, vars)** — animate from `vars` to current state (entrances).
- **gsap.fromTo(targets, fromVars, toVars)** — explicit start and end.
- **gsap.set(targets, vars)** — apply immediately (duration 0).

Always use **camelCase** property names (e.g. `backgroundColor`, `rotationX`).

## Common vars

- **duration** — seconds (default 0.5).
- **delay** — seconds before start.
- **ease** — `"power1.out"` (default), `"power3.inOut"`, `"back.out(1.7)"`, `"elastic.out(1, 0.3)"`, `"none"`.
- **stagger** — number `0.1` or object: `{ amount: 0.3, from: "center" }`, `{ each: 0.1, from: "random" }`.
- **overwrite** — `false` (default), `true`, or `"auto"`.
- **repeat** — number or `-1` for infinite. **yoyo** — alternates direction with repeat.
- **onComplete**, **onStart**, **onUpdate** — callbacks.
- **immediateRender** — default `true` for from()/fromTo(). Set `false` on later tweens targeting the same property+element to avoid overwrite.

## Transforms and CSS

Prefer GSAP's **transform aliases** over raw `transform` string:

| GSAP property               | Equivalent          |
| --------------------------- | ------------------- |
| `x`, `y`, `z`               | translateX/Y/Z (px) |
| `xPercent`, `yPercent`      | translateX/Y in %   |
| `scale`, `scaleX`, `scaleY` | scale               |
| `rotation`                  | rotate (deg)        |
| `rotationX`, `rotationY`    | 3D rotate           |
| `skewX`, `skewY`            | skew                |
| `transformOrigin`           | transform-origin    |

- **autoAlpha** — prefer over `opacity`. At 0: also sets `visibility: hidden`.
- **CSS variables** — `"--hue": 180`.
- **svgOrigin** _(SVG only)_ — global SVG coordinate space origin. Don't combine with `transformOrigin`.
- **Directional rotation** — `"360_cw"`, `"-170_short"`, `"90_ccw"`.
- **clearProps** — `"all"` or comma-separated; removes inline styles on complete.
- **Relative values** — `"+=20"`, `"-=10"`, `"*=2"`.

## Function-Based Values

```javascript
gsap.to(".item", {
  x: (i, target, targets) => i * 50,
  stagger: 0.1,
});
```

## Easing

Built-in eases: `power1`–`power4`, `back`, `bounce`, `circ`, `elastic`, `expo`, `sine`. Each has `.in`, `.out`, `.inOut`.

## Defaults

```javascript
gsap.defaults({ duration: 0.6, ease: "power2.out" });
```

## Controlling Tweens

```javascript
const tween = gsap.to(".box", { x: 100 });
tween.pause();
tween.play();
tween.reverse();
tween.kill();
tween.progress(0.5);
tween.time(0.2);
```

## gsap.matchMedia() (Responsive + Accessibility)

Runs setup only when a media query matches; auto-reverts when it stops matching.

```javascript
let mm = gsap.matchMedia();
mm.add(
  {
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

## hyperframes (2702-hyperframes)

- الترخيص: **Apache-2.0**  ·  الأصل: https://github.com/openai/plugins/tree/5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f/plugins/hyperframes
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2702-hyperframes/10378-hyperframes
- الوصف: Create video compositions, animations, title cards, overlays, captions, voiceovers, audio-reactive visuals, and scene transitions in HyperFrames HTML. Use when asked to build any HTML-based video content, add captions or subtitles synced to audio, generate text-to-speech narration, create audio-reactive animation (beat sync, glow, pulse driven by music), add animated text highlighting (marker swee

```markdown
# HyperFrames

HTML is the source of truth for video. A composition is an HTML file with `data-*` attributes for timing, a GSAP timeline for animation, and CSS for appearance. The framework handles clip visibility, media playback, and timeline sync.

## Approach

Before writing HTML, think at a high level:

1. **What** — what should the viewer experience? Identify the narrative arc, key moments, and emotional beats.
2. **Structure** — how many compositions, which are sub-compositions vs inline, what tracks carry what (video, audio, overlays, captions).
3. **Timing** — which clips drive the duration, where do transitions land, what's the pacing.
4. **Layout** — build the end-state first. See "Layout Before Animation" below.
5. **Animate** — then add motion using the rules below.

For small edits (fix a color, adjust timing, add one element), skip straight to the rules.

### Visual Identity Gate

<HARD-GATE>
Before writing ANY composition HTML, you MUST have a visual identity defined. Do NOT write compositions with default or generic colors.

Check in this order:

1. **DESIGN.md exists in the project?** → Read it. Use its exact colors, fonts, motion rules, and "What NOT to Do" constraints.
2. **visual-style.md exists?** → Read it. Apply its `style_prompt_full` and structured fields. (Note: `visual-style.md` is a project-specific file. `visual-styles.md` is the style library with 8 named presets — different files.)
3. **User named a style** (e.g., "Swiss Pulse", "dark and techy", "luxury brand")? → Read [visual-styles.md](./visual-styles.md) for the 8 named presets. Generate a minimal DESIGN.md with: `## Style Prompt` (one paragraph), `## Colors` (3-5 hex values with roles), `## Typography` (1-2 font families), `## What NOT to Do` (3-5 anti-patterns).
4. **None of the above?** → Ask 3 questions before writing any HTML:
   - What's the mood? (explosive / cinematic / fluid / technical / chaotic / warm)
   - Light or dark canvas?
   - Any specific brand colors, fonts, or visual references?
     Then generate a minimal DESIGN.md from the answers.

Every composition must trace its palette and typography back to a DESIGN.md, visual-style.md, or explicit user direction. If you're reaching for `#333`, `#3b82f6`, or `Roboto` — you skipped this step.
</HARD-GATE>

For motion defaults, sizing, entrance patterns, and easing — follow [house-style.md](./house-style.md). The house style handles HOW things move. The DESIGN.md handles WHAT things look like.

## Layout Before Animation

Position every element where it should be at its **most visible moment** — the frame where it's fully entered, correctly placed, and not yet exiting. Write this as static HTML+CSS first. No GSAP yet.
```

## remotion-maps (2712-remotion)

- الترخيص: **MIT**  ·  الأصل: https://github.com/openai/plugins/tree/5fd93af4cd0c623e020d0cc7e9ce178b4ac1f70f/plugins/remotion
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2712-remotion/10435-remotion-maps
- الوصف: Remotion Map animation knowledge

```markdown
# Remotion Maps

Choose exactly one technique from the intended shot, then load only that technique's `TECHNIQUE.md`.
Every technique directory is self-contained and may be removed without breaking the others.

## [Static map](techniques/static-map/TECHNIQUE.md)

- Requires you grab a satellite image and mount it in a `<Img>` tag, and animate on top

## [Mapbox](techniques/mapbox/TECHNIQUE.md)

- Requires a Mapbox key
- Nicer styles by default
- Map can display a round globe when zoomed out
- Includes nice 3D buildings such as the Eiffel tower

## [MapLibre](techniques/maplibre/TECHNIQUE.md)

- Requires no API key, fully free
- Does not include 3D building

## [MapTiler](techniques/maptiler/TECHNIQUE.md)

- Uses MapTiler
- Annotations can be drawn on top of geographic features: borders, rivers, labels

## [CesiumJS](techniques/cesium/TECHNIQUE.md)

- Flythroughs through terrain and mountains
- "Flight simulator" perspective
```

## animate (388-animation-helper)

- الترخيص: **MIT**  ·  الأصل: https://github.com/barnburner121/claude-plugin-marketplace/tree/0b62c34/generated-plugins/animation-helper
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/388-animation-helper/1417-animate
- الوصف: Generate CSS/Framer Motion animations

```markdown
# animation-helper

Generate CSS/Framer Motion animations.

## Tools Available

- **Read** — Read files from the filesystem
- **Write** — Write files to the filesystem
- **Edit** — Make targeted edits to existing files
- **Bash** — Execute shell commands
- **Grep** — Search file contents with regex
- **Glob** — Find files by pattern matching

## Usage

Invoke the `animate` skill to Generate CSS/Framer Motion animations. The skill will analyze the relevant codebase context and generate appropriate output.
```

## 9525-animate (2460-pixel-art)

- الترخيص: **MIT**  ·  الأصل: https://github.com/melodic-software/claude-code-plugins/tree/c8fa858c9059d3183cfc08f646e4a97f44b33973/plugins/pixel-art
- في الأطلس: https://github.com/kosif199022-jpg/kosif-atlas/tree/main/skills/2460-pixel-art/9525-animate
- الوصف: Animate pixel-art sprites: idle, walk, run, attack, jump, hurt, death and custom cycles in 1, 4 or 8 directions, exported as sprite sheets laid out for the target engine (RPG Maker MZ, Godot, PICO-8, plain strips) with Aseprite-shaped frame data and looping GIF previews, with no external tools. The model authors pose-parameterised frames, the bundled stdlib renderer writes sheet, frame data and GI

```markdown
# Animate

Turn a character (an existing spec, or one described in the request) into animation cycles laid
out the way the target engine expects, and show them moving.

## 1. Brief

Follow [`brief.md`](${CLAUDE_PLUGIN_ROOT}/reference/brief.md) the same way `/pixel-art:sprite`
does, including the `brief.md` file, the one-line defaults, and the presence-gated
`/planning:interview` offer. Then add:

- **Cycles** and their purpose: player-controlled actions need responsiveness; enemies and
  cutscene actors can afford anticipation.
- **Directions**: 1 (side-scroller), 4, 8, or isometric.
- **Target layout**: sets frame size, frame count per cycle, direction order, and sheet columns.
  RPG Maker MZ characters, for example, fix 3 patterns x 4 directions at 48x48. Read
  [`engine-layouts.md`](${CLAUDE_PLUGIN_ROOT}/reference/engine-layouts.md).

When the character is an existing spec that already has `brief.md` beside it, read that file and
extend it with cycles, directions, and layout. Do not re-ask fields it already answers. Write the
extended brief beside this spec before the first render.

## 2. Plan the cycles

From [`craft-animation.md`](${CLAUDE_PLUGIN_ROOT}/reference/craft-animation.md) choose, per cycle,
the key poses, frame count, per-frame duration, and loop direction. Write the plan as a short table
before drawing: it is the review rubric later. Engine layouts override craft defaults (MZ walk is
3 patterns played 0-1-2-1).

## 3. Author

Use a procedural generator for anything past a couple of frames: one `draw(direction, pose)`
function whose parameters (limb angles, step phase, body bob, arm swing, squash) produce each
frame, so every frame stays on-model and a fix lands in every frame at once. For a humanoid
walker, start from `${CLAUDE_PLUGIN_ROOT}/scripts/kit.py` and adapt it: a proportion preset
(`chibi`, `standard`, `tall`), a head shape, a hair shape, material ramps, and an `extra`
callback for clothing or props. `${CLAUDE_PLUGIN_ROOT}/examples/walker/blacksmith.py` is a
4-direction walker built that way. `${CLAUDE_PLUGIN_ROOT}/examples/campfire/hero_mz.py` is an
earlier hand-written MZ sheet; copy either example into the working directory before running it, with `kit.py` beside `blacksmith.py`.
Draw one side view and mirror it for the other only when the design is symmetric; the kit shades
after the mirror so the light stays top-left.

A PNG from another backend is snapped with `render.py --snap` before its rows enter the spec
([`backends.md`](${CLAUDE_PLUGIN_ROOT}/reference/backends.md)). Palette presets and project palette
files are the same strings `sprite` uses ([`palettes/README.md`](${CLAUDE_PLUGIN_ROOT}/palettes/README.md)).

Name frames `<cycle>_<direction><index>` or the engine's own names, list them in `sheet.order` in
```
