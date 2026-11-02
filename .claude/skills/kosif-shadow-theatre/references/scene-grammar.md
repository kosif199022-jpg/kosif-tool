# Scene grammar — `kosif.shadow-theatre.scene.v1`

Units: `x` = fraction of the screen width (0 left, 1 right; values outside put an actor off-screen), `y` = fraction of
the screen height (1 = bottom edge), `height` / `scale` = fraction of the screen height. Angles in degrees. Times inside a
scene are seconds from the scene start.

## Film

| field | default | meaning |
|---|---|---|
| `width`, `height`, `fps` | 1080, 1920, 30 | output (owner standard). Use 1920×1080 for a stage-wide film. |
| `duration` | last scene end | must equal the last scene's `end` |
| `seed` | 7 | clouds and grain |
| `lamp` | `{x:0.5}` | lamp axis; `depth` spreads shadows away from it |
| `screen` | margin 0.045, radius 0.07 | rounded screen; `top`/`bottom` override vertical margins |
| `penumbra`, `depth_blur` | 1.2, 12 | base edge softness and extra blur at depth 1 (work-resolution pixels) |
| `shadow_leak`, `grain`, `stage_color` | 0.05, 0.006, (5,5,14) | how much light shows through a shadow, film grain, the dark stage |

## Scene

| field | meaning |
|---|---|
| `start`, `end` | seconds; scenes tile the film with no gap |
| `backdrop` | `dawn-green`, `night-blue`, `teal-mist`, `crimson-spot`, `desert-amber`, `moon-indigo`, or `{stops:[[pos,[r,g,b]],...], clouds}` |
| `spot` | `{x, y, r, color, r_keys:[{t, scale}]}` radial light pool (keyed radius via `scale`) |
| `clouds`, `cloud_speed` | cloud contrast (0–0.2) and drift in px/s |
| `fade_in`, `fade_out` | lamp dim at the edges (blackout) |
| `iris` | `{shape: circle|heart|star|arch, x, y, soft, keys:[{t, scale}]}` — scale ≥ 3 means fully open |
| `transition_in` | label for the checker: `blackout`, `iris`, `swell`, `morph`, `cut` |
| `techniques` | which of the eight techniques the scene shows (checked) |
| `memorable` | the image the audience keeps (at least one) |
| `chord`, `cues` | synth chord for the score (`["D3","A3","D4"]`) and extra swell times (film seconds) |
| `actors` | list below; all shadows merge into one silhouette layer per frame |

## Actor

Common: `keys: [{t, x, y, scale, depth, rot, opacity, ease}]` — numeric fields interpolate with the *next* key's `ease`
(`linear`, `in`, `out`, `inout` default, `smooth`, `hold`). `blur` adds softness to one actor.

`type: "human"` (default)
- `costume`: `plain`, `dress`, `child`, `elder` (elder holds a stick in the front hand)
- `height`: body height; `facing`: 1 right / -1 left; `grounded` (default true) puts the lowest foot on `y`; false puts the hip at `y`
- `pose` in keys: a name (`stand`, `arms_up`, `reach_up`, `offer`, `lunge`, `dance_arc`, `spin`, `crouch`, `kneel`, `bow`,
  `frond`, `trunk`, `hull`, `sail`, `carry`, `embrace`) or an object `{base: "stand", torso: 20, arm_a: 150, ...}` with any
  of `torso, head, arm_a, elbow_a, arm_b, elbow_b, leg_a, knee_a, leg_b, knee_b`. Poses blend joint by joint between keys.
- `cycle`: `{type: walk|sway|wave|breathe|flutter, period, amp, phase}` procedural motion on top of the keyed pose.

Joint convention: 0° = limb hanging straight down, +90° = pointing forward, 180° = up. Arms are relative to the torso,
legs are absolute; elbow/knee add to the parent limb. `torso` is the lean forward from upright.

`type: "prop"` with `shape`:
`sun`/`circle`, `crescent`, `heart`, `star`, `arch`, `bird` (flaps; `params.flap`), `palm` (`params.period`),
`foliage` (leafy branch held by a performer; `params.seed`, `leaves`), `skyline` (domes, minarets, cut windows),
`dunes` (full width; `params.drift`), `waves` (full width; `params.period`), `lantern` (cut-out fanous, swings;
`params.chain`), `hand` (big hand, fingers up at rot 0).

## Recipes for body-builds

- **Tree:** a tall `trunk` body in the centre, two bodies on each side leaning outward (`torso` 20–30) with arms up,
  `foliage` props fading in at the hands 0.5 s after the pose lands.
- **Boat:** one body in `hull` with `grounded:false` just above a `waves` band, a `sail` body standing on it, a child at the bow.
- **Giant:** key `depth` 0 → 0.6–0.9 over 1.5–2 s while the pose changes; the other dancer stays at depth 0 for scale contrast.
- **Arch/gate:** two `lunge` bodies facing each other with front arms meeting overhead.
