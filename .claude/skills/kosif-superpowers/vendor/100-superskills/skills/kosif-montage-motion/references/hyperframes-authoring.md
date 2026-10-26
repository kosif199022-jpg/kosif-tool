# HyperFrames authoring, as the renderer actually checks it (v0.8.139, measured here)

HyperFrames (heygen-com/hyperframes, Apache-2.0) turns one HTML file into a deterministic MP4: Puppeteer seeks the
page frame by frame, FFmpeg encodes. KOSIF Motion writes that HTML and renders it through HyperFrames' CLI when it
is installed in `motion/` (`npm install hyperframes gsap`), or through KOSIF Studio's own renderer (Playwright/Edge,
`window.render(t)`) — the kit's `shim` makes the same file work for both.

## The contract

```html
<html lang="ar">                                  <!-- never dir="rtl" on <html>: HyperFrames renders that blank -->
<script src="assets/gsap.min.js"></script>        <!-- local copy from node_modules/gsap; no CDN at render time -->
<script src="assets/motion-kit.js"></script>
<div id="root" data-composition-id="root" data-width="1920" data-height="1080" data-start="0" data-duration="17" data-fps="30">
  <audio id="ambience" src="assets/ambience.wav" data-start="0" data-duration="17" data-volume="0.9" data-fade-out="1"></audio>
  ...
  <script>
    const tl = gsap.timeline({ paused: true });    // paused: the runtime seeks it
    tl.to("#x", { x: 100, duration: 1 }, 2.5);      // the 3rd argument is the absolute time in seconds
    window.__timelines = window.__timelines || {};  // written literally: the linter looks for these two lines
    window.__timelines["root"] = tl;
    MOTION.shim("root", 17);                         // KOSIF Studio's renderer: window.render(t) + window.__ready
  </script>
</div>
```

- `data-start` / `data-duration` are **seconds**; `data-track-index` is only a Studio lane.
- Timed elements get `class="clip"` (the runtime keys visibility off `data-start`).
- Media needs an **`id`** (`<audio id=…>`), or it is silent in renders; `data-volume`, `data-fade-in/out`,
  `data-media-start` trim.
- Nested compositions: `<div data-composition-id="intro" data-composition-src="compositions/intro.html" data-start data-duration>`.
- Variables: `data-composition-variables` (schema on `<html>`), `--variables '{...}'` at render time,
  `window.__hyperframes.getVariables()` inside.
- Fonts: system fonts that the renderer auto-resolves (Segoe UI, Tahoma, Arial…) or an explicit `@font-face`
  (`src: local('…')` is enough for an OS font). Unknown family names fail lint.
- Seekable only: GSAP tweens, CSS animations (the runtime seeks `document.getAnimations()`), Lottie, Three.js via
  adapters. No `setTimeout`, no `requestAnimationFrame` state, no `Math.random` (use `MOTION.rng(seed)`).
- GSAP `fromTo` renders its *from* state immediately: never put `opacity: 1` in a from-state of something that must
  stay hidden until later (the kit's `drawPath` uses `set` + `immediateRender: false`).
- `marker-end` arrowheads show as soon as the path is visible; draw heads as separate shapes that land when the
  stroke arrives (`drawPath(..., { head })`).

## CLI (run from `motion/`; `motion.py` wraps these)

```bash
npx hyperframes check projects/x        # lint + runtime validation + layout/motion/contrast samples; fix every ✗
npx hyperframes snapshot projects/x     # key frames as PNG
npx hyperframes render projects/x -o out/x.mp4 -q looks -f 30      # draft | looks (CRF 16) | delivery
npx hyperframes render projects/x --resolution 4k                   # integer DPR upscale of the same composition
npx hyperframes doctor                  # Chrome headless shell (cached under ~/.cache/puppeteer), FFmpeg, memory
```

Environment: `HYPERFRAMES_SKIP_SKILLS=1` (no GitHub check at init), `PRODUCER_LOW_MEMORY_MODE=1` on an 8 GB machine
(one worker, screenshot capture), `PUPPETEER_EXECUTABLE_PATH` to use another Chrome. The npm `.cmd` wrappers break
on non-ASCII user paths: `motion.py` calls `node node_modules/hyperframes/bin/...` directly.

## What the checker enforced on the first real composition

| Finding | Fix |
|---|---|
| `missing_timeline_registry` although `MOTION.register` registered it | write the two `window.__timelines` lines literally |
| `media_missing_id` | `<audio id="ambience">` |
| `html_dir_attribute_breaks_render` | remove `dir="rtl"` from `<html>`, set `direction: rtl; unicode-bidi: isolate` on the text elements |
| `font_family_without_font_face` for Noto names | keep Segoe UI / Tahoma, or add `@font-face { src: local(...) }` |

## KOSIF Motion kit (assets/motion-kit.js)

`MOTION.ease` (slam / snap / drive / settle), `rng(seed)`, `svgEl`, `revealWords` / `hideWords` (word masks,
Arabic-safe), `drawPath` (pen stroke, optional arrowhead) / `flowDash` (moving current), `rain`, `vapour`,
`sparkle` (seeded), `camera` (the stage as one object), `flash`, `grain` (stepped, seekable), `vignette`,
`register`, `shim`. `motion.py new` scaffolds a project with the kit and GSAP copied in; `frames` renders key
frames for the 8-second gate; `check` runs HyperFrames' gate; `render` picks the engine; `measure` reports motion
energy (near-still share, peak, mean, longest freeze); `ambience.py` synthesises a deterministic soundtrack.

## Cinematic 3D compositions (Three.js) — the realism path

- Write the scene as an ES module (`src/main.js`) importing `three` and its `examples/jsm` addons; `motion.py bundle`
  turns it into one classic script (`assets/main.bundle.js`) that loads from file:// in any renderer.
- Everything is a function of `t`: sun elevation/azimuth, sea `time`, cloud cover, particle phases, camera keys.
  `composer.render(0)` with `FilmPass.uniforms.time = t`; no `Clock`, no `Math.random` (seeded Perlin / mulberry32).
- Building blocks that read as real: `Sky` (Preetham) + `ACESFilmicToneMapping` exposure; `Water` with a generated
  normal map (reflects the sky, sun glitter); terrain from seeded ridged FBM with slope/height vertex colours, shadows
  from the sun light; a raymarched cloud slab (36 steps, 3 light taps) on a box mesh; `Points` with seeded phases for
  vapour and rain (size capped, faded near the lens); `EffectComposer`: bloom (0.22 / 0.6 / 0.9), `BokehPass`
  (aperture 4e-5, maxblur 0.0035), grade + vignette ShaderPass, `FilmPass(0.16)`, `OutputPass`.
- Lighting lessons: a sun in front of the lens only at sunrise, then swing it to a side key; a camera-side fill light
  (no shadows) for valleys; keep exposure ≈ 0.5–0.62 and bloom threshold ≥ 0.9 or the frame whites out; lightning as
  a 2-frame spike of light + exposure, not a full-frame flash.
- GPU: `html_render.GPU_FLAGS` uses `--use-angle=d3d11`; `HTML_RENDER_SOFTWARE=1` forces SwiftShader. This machine:
  ~1.0–1.5 s per 1080p frame including the screenshot (≈ 10 min for 17 s at 30 fps).
- HyperFrames' own runtime drives GSAP/CSS, not a custom WebGL render loop; render 3D compositions with the studio
  engine (`motion.py render --engine studio`), which also muxes the `<audio>` clips.

### v2 lessons (forest, detail maps, god rays, lens flare)
- Detail that sells realism at film distances: a dense terrain mesh (560²) + tiled procedural albedo/normal maps
  (`CanvasTexture`, repeat 60–90), and an `InstancedMesh` forest (~20k two-tier conifers, seeded placement by height,
  slope and a clumping noise, `setColorAt` for per-tree colour, `castShadow` on the instanced mesh).
- Screen-space god rays must use a short stride (≈0.55 of the sun distance over 64 samples) with a per-pixel dither
  and a mask that keeps them above the sun's screen height — a long stride copies the sun glitter into a lattice
  across the water.
- `Lensflare` works with generated textures; it hides itself when the sun pixel is occluded.
- `mergeGeometries` from `three/examples/jsm/utils/BufferGeometryUtils.js` builds the two-tier crown.
- Cost on Iris Xe: 1.2–2 s per 1080p frame for far shots, up to 6 s when thousands of shadowed trees fill the frame.


### v3 lessons (koi pond: water you can see through, caustics, living things)
- **Realism blocks** in `kit/three-kit.js`: `makeShallowWater` (sum-of-sines swell with analytic normals, ripple rings that
  petals and fish leave, Fresnel reflection that mirrors the dark bank near the horizon and the sky above it, a GGX sun
  glint, transmission so the bed shows through), `addCaustics(material)` (a procedural caustic network added to the direct
  sunlight only, plus wavelength-dependent absorption with depth), `addSway` (wind on reeds/grass/leaves: bend ∝ height²),
  `makeKoi` (lofted body, fins, seeded kohaku/sanke/showa/ogon skin, a swim bend in the vertex shader that grows toward the
  tail and leans into turns), `makePetals` (fall with flutter, ring the water on landing, float and drift), `makePebbles`
  (smooth water-worn stones, colour families, clumping), `makeBlades`, `makeDappledSun` (a SpotLight with a canopy cookie:
  komorebi), `envFromGradient` (bounded sky gradient → PMREM), `cameraPath` (centripetal Catmull-Rom, never a dead stop).
- **The black-rectangle bug:** a PMREM of the Preetham `Sky` contains the sun disk (~1e4), which overflows half-float
  buffers; one Inf/NaN pixel is then spread by bloom into large black rectangles. Fixes now in the kit: `makePost` adds a
  guard pass right after the render pass (NaN/Inf → 0, clamp ≤ 48), and environments come from `envFromGradient`.
- A SpotLight with `decay = 0` behaves like a sun: intensity ≈ 3–5 (not thousands).
- Never look straight into a low sun over water with fog: the glint, the bloom and the fog add up to a white sheet. Put
  the sun to the side (azimuth ~90° from the view) and let the water mirror the banks.
- Water reads as water when its near-horizon reflection is dark (the far bank), not sky-bright.
- Caustic cells in a garden pond are 5–15 cm (`scale ≈ 5.5` in metres), not a metre.
- Under memory pressure (≈100 MB free) the page can take 1–5 minutes to build its procedural textures: `motion.py frames`
  now builds once and seeks every requested time; `texSize` (terrain, canopy) trims the build.

### Tooling added in v3
`motion.py lint` (determinism, contract, taste) · `motion.py sheet FILM` (contact 2 fps, phone 360 px, strip, first frame,
review.md rubric) · `motion.py speed FILM` (optical-flow px/frame → blur or redesign) · `motion.py beats TRACK` (bpm, beats,
downbeats, hits) · `motion.py study REF.mp4` (cuts, shot lengths, first change, energy, palette → style_guide.md) ·
`motion.py footage CLIP` (all-intra clip a composition seeks exactly via `<video data-start>`) · `score.py` (a soundtrack
on the beat grid: kick/clap/hats/sub/pad/pluck/lead, risers, booms, designed SFX from cues) · `ambience.py --sea 0 --drops
--brook` (ponds and rooms) · `film.py`/`motion.py render --blur k` now blurs every page (GSAP and canvas too), centred
shutter, float average; 3D pages keep their GPU accumulation (`window.__nativeBlur`).

### v3.1 — the sound drives the picture (kloss), real motion drives bodies (aicreataro)
- `motion.py channels TRACK` → per-frame JSON (fps, beats, downbeats, kicks, onsets, rms, bass/mid/high, onset, centroid,
  silence, pitch_dive, pitch_rise, speed, tape) + `spectrogram.png` (magma) + `spectrum_height.png`. A tape stop is heard
  two ways: a straight falling pitch line (r² > 0.9, > 15 st/s) or a whole-spectrum shift (> 30 st/s over 0.25 s), each
  held ≥ 4 frames; a state machine turns that into playback speed (stopping → stopped through the dead air → spin-up),
  and `tape` is its integral. In a page: `const C = MOTION.channels(json)` → `C.kick(t)`, `C.onset(t)`, `C.v("bass", t)`,
  `C.tape(t)`, `C.silent(t)`.
- Run the world on the tape clock and only the camera on the wall clock: the land, sparks and dust freeze in a stop while
  the camera keeps orbiting them (bullet time for free). `spectrumOnTape(img, ch)` re-samples the spectrogram onto tape
  time so the line under the camera is always what is heard.
- `makeSpectrumGround` (spectrogram → canyon: bass river in the middle, harmonics on the walls, lit rock with a derivative
  normal, lava only in the loudest cells, a playhead traced on the floor, fog; `half` keeps the plane edge out of frame),
  `makeGlitchPass` (chroma · slice · negative tear · mono freeze · warp — use them as accents: a negative held for 0.4 s on a
  dark scene becomes a grey flash; a cold monochrome reads as "time stopped"), `makeSparks` (event bursts on the tape clock).
- A chrome hero reflects the real scene with a `CubeCamera` (256², half float; hide the hero while it renders).
- `motion.py loopcheck FILM` proves a loop seam; `score.py` writes tape stops (`tape_stops_s`, `tape_starts_s`).
- `motion.py mocap VIDEO --out body.json` (fixed camera: median background, difference, morphology, seeded points) →
  `makeParticleBody(json)`; `loadModel(url)` brings a GLB with its animation sought to t; `addWave` for cloth and flags.
- `voice.py` speaks Arabic offline (Windows OneCore: Naayf); `<audio data-role="voice">` ducks the other clips (sidechain)
  in the mux, which then normalises to −14 LUFS.
- Async scenes: `build()` returns `{ ready }`; the page waits for it (and fonts) before `__ready` — the scene3d template does.

### v3.2 — taken from KOSIF Omni (Ultra Motion & Montage, Lighting, Vision, Aesthetics council)
- `montage.py cut CLIPS --music TRACK` / `motion.py montage`: edit any footage to a beat — a shot plan of quick (≈1 s) and
  breathing (≈3 s) shots with every cut on a beat and breathing shots ending on downbeats, the most active unused window of
  each clip (frame-difference energy), fill-crop to 9:16/16:9/1:1/4:5, zoom punches on downbeats that decay like a hit
  (2× supersampled so they do not stair-step), grades (teal_orange, golden_hour, cyberpunk, vintage_film with seeded grain,
  matrix_tech, clean_commercial, magma_night), hard cuts, music + clip sound + voice with real sidechain ducking, −14 LUFS /
  −1 dBTP, and karaoke captions.
- `montage.py captions VIDEO --spec caps.json`: one ASS event per spoken word (highlight colour + a 120 ms pop), so Arabic
  stays shaped and ordered; words get time by length; accepts `voice.py` timings; Noto Arabic fonts; safe bottom margin.
- `motion.py inspect FILM [--allow 6.6-7.3]`: the delivery gate — yuv420p/H.264/even size, truly black stretches (not dark
  designs; fades at the ends allowed), frozen stretches (an end hold is a warning; list designed holds), integrated LUFS and
  true peak, blown highlights and crushed blacks on sampled frames.
- `review.md` is now a two-reviewer P0/P1/P2 round with a fixer, plus the twelve lenses of the aesthetics council (world,
  character, action, camera, light, colour, VFX, atmosphere, materials, production design, composition, beauty).
- Light like a set: `lightRig(scene, { key, fillStops: 2, rimStops: 0.5, keyK: 5600, fillK: 6500, rimK: 4300 })` (a
  2-stop fill = a 5:1 lighting ratio), `kelvin(K)`, `gel(fromK, toK)` (mired shift → CTO/CTB), `falloffStops(d1, d2)`.

### v3.3 — the owner's reference books as code (references/book-lessons.md)
- **Shot language** (Veo 3 guide, 360° character sheet): `shot(kind, o)` for establishing · wide · medium · closeup ·
  extreme_closeup · low/high angle · birds_eye · dutch · tracking · crane_up/down · push_in · pull_back · orbit · arc ·
  handheld (seeded sway) · dolly_zoom (subject height held exactly) · whip_pan · turntable; `shotFromWords("low angle
  tracking shot")` combines words; `sequence([{ at, shot }])` cuts hard between shots; `applyShot(camera, s, post)`.
- **Lighting presets** (Joel Grimes): `lightPreset(scene, "rembrandt" | "clamshell" | "edgy" | "ultrasoft" | "short" |
  "broad" | "sun")`; softness is the source's apparent size: `softnessDeg(size, distance)` → shadow radius.
- **Colour** (Gurney, colour theory): `aerialPerspective()` (three-channel fog; fog colour must equal the horizon sky or far
  forms end darker than the sky), `fogTowardSun()` (reverse aerial perspective), `skyBounce()` (upfacing shadows cool,
  downfacing warm), `LIGHT_SOURCES` / `lightColor("sodium")`, `makeLookPass({ gamut, night, split })`, `harmony()`,
  `MOTION.palette()`; `makeRenderer(..., { tone: "agx" })` keeps lamp and taillight hues in the highlights.
- **Long exposure** (Night Photography): `render --blur 16 --shutter 30 --stack lighten` = a 1 s exposure per frame with
  the star-trail stack. A light that moves farther than its own size between sub-samples draws dots — stretch it by
  `trailLength(speed)` (or add samples). `--stack average` with a long shutter = silky water.
- Example `projects/blue_hour`: the same rock at 0.7/1.4/2.6/4.5 km turned blue and pale by air alone, sodium lamps against
  blue hour, cars as light trails, stars as arcs, a slow push-in at road height.
