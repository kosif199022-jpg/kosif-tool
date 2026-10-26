# shape-kit — 3D shapes and cute characters from signed distance fields (v1.3)

`scripts/kit/shape-kit.js` → `window.K3S`. Load it after `three-kit.bundle.js`; no npm, no bundling, no downloads.
New 3D projects (`kmotion new NAME --3d`) get it automatically in `assets/`.

## Why SDFs
A character is a short list of soft primitives (spheres, ellipsoids, round cones, boxes, tori) blended with a
*smooth union* radius `k`. The blend is what makes a plush toy read as one stitched, stuffed object instead of
balls glued together. The mesher turns the field into a watertight triangle mesh with correct normals and
vertex colours — no modelling package, no assets, fully deterministic.

```js
const S = K3S.sculpt().color("#f2e4d8")
  .ellipsoid([0, .088, 0], [.071, .082, .064])                 // torso
  .ellipsoid([-.044, .046, .012], [.04, .042, .048], { k: .022 }) // thigh, blended 22 mm
  .capsule([.05, .12, .03], [.03, .08, .06], .02, .017, { k: .014 })   // arm: round cone r 20 → 17 mm
  .ellipsoid([0, .07, .0135], [.0125, .05, .0085], { op: "sub", k: .005, color: "#ff9fb8" })  // carve + tint
  .paint([.045, .04, .05], .016, "#ff8fab", { soft: .009 })      // blush: colour only
const geo = S.mesh({ cells: 120 });          // geo.userData.stats → grid, evals, triangles, ms
const mesh = new THREE.Mesh(geo, K3S.plushMaterial());
```

| Call | What it does |
|---|---|
| `sphere(c, r, o)` · `ellipsoid(c, [rx,ry,rz], o)` · `capsule(a, b, r1, r2, o)` · `box(c, [hx,hy,hz], round, o)` · `torus(c, R, r, o)` | primitives; `o.rot = [rx, ry, rz]` (Euler XYZ), `o.k` blend radius, `o.color` |
| `o.op` | `"add"` (smooth union, default) · `"sub"` (smooth carve) · `"and"` (smooth intersection) |
| `paint(c, r, colour, { soft, radii, amount })` | colour stamp, no geometry (blush, belly patch, paw pads) |
| `dist(x,y,z)` · `colorAt` · `project(p)` · `hit(from, dir)` | query the field: place eyes/buttons where a ray from the front meets the face |
| `mesh({ cells, project })` | surface nets, coarse-to-fine (only blocks near the surface are evaluated at full resolution — a sphere at 64 cells evaluates < 60 % of the grid), vertices projected onto the true surface |
| `plushMaterial(o)` | felt: vertex colours, velvet sheen, a fuzz rim in the fabric's own colour, object-space fibre noise (no UVs) |
| `glossMaterial` · `eye({ r })` · `tube(points, r, colour)` | glossy eyes with two catch-lights, mouths and stitches |
| `studioBackdrop` · `stageDisc` · `makeLitePost` | background, a measuring disc with a scan sweep, the fast post stack (bloom + grade only) |
| `trussOverlay(model, { nodeParts })` | a structural-twin truss in 3D whose joints ride the rig (ears bend, the truss bends) |
| `bunny(o)` | the reference character: rigged `body · head · earL · earR · tail · eyes · mouth · scarf` |

Cost (measured, Node 22, one core): a 136-cell body ≈ 1.5 s, the whole bunny (274k triangles) ≈ 4 s in headless
Chromium. Meshing runs once at page load; frames only move the rig.

## The cute recipe (what made the bunny read as "كيوت")
Numbers from the bunny, in metres; scale them together.
1. **Head ≥ body.** Head width 0.16 vs torso 0.14; head sits low on a short neck (no visible neck).
2. **Eyes low and wide.** Eye centres at ~45 % of the head height, spaced ~0.4 × head width, glossy black,
   slightly tall (`tall: 1.12`), two catch-lights in the upper-outer quadrant — the single biggest "cute" lever.
3. **Chubby cheeks + small muzzle.** Two cheek ellipsoids blended with `k ≈ 0.02` give the baby-face silhouette;
   the nose is tiny (≤ 1/8 of head width) and pink; the mouth is a 1 mm "w" tube.
4. **Soft everything.** Blend radii 10–30 mm; no hard edges except the flat seat (`box` carve) so it sits.
5. **Short limbs, big feet.** Arms are round cones tucked against the belly; feet are flattened ellipsoids
   pointing forward with pink pads (`paint`).
6. **Pastel palette, one accent.** Warm cream fur `#f2e4d8`, lighter belly, pink inner ears/blush/nose; one
   complementary accent (the mint scarf) that ties to the film's UI colour.
7. **Light like a toy photo.** Warm soft key from front-left-top with shadows, low hemisphere fill, two coloured
   rims (mint + pink) from behind, `tone: "neutral"` so pastels stay true. Keep bloom subtle (threshold ≥ 0.9):
   white plush + strong bloom = a glowing blob.
8. **Act alive.** Breathing (±0.6 %), one blink, ear secondary motion, a hop with squash on landing.

## Rig and motion
Parts are `THREE.Group` pivots placed at anatomical joints (neck, ear roots, tail), so a rotation bends the
character naturally. Drive them with springs (`spring(t, t0, freq, damping)` in the bunny film): an ear flop at
1.5 Hz / ζ 0.42 stays under the 80 px/frame speed gate at 1080×1920; 2.2 Hz / ζ 0.28 did not.

Example film: `scripts/projects/bunny_twin` (5 s, 1080×1920, SHAPE→JOINT→LOAD→BREAK→SWAP→RANK).
