# Engine — recipe, law, conditions, metrics, render

## Pipeline

```
recipe.json ──validate──▶ kmx_engine.simulate (per condition) ──▶ metrics + replication + dose-response
                                   │                                        │
                                   └──▶ kmx_scene.write_scene ──▶ scene.html ──▶ kmx_capture.cjs (stills, pixel diff, WAV)
                                                                     └──▶ tools/render_html.cjs (MP4)
report.json / report.md ──▶ kmx_memory.record_experiment ──▶ memory/ledger.jsonl
```

One source of truth: the engine computes every number. The scene embeds those numbers and only draws them, so what is measured is what is seen. The 86 reference styles are pure functions of time (`frame = f(t)`, see [code-bricks.md](code-bricks.md)); a persistent material memory cannot live inside such a frame, so the engine simulates the history once and the page plays it back with `seek(t)`.

## Recipe schema (`kosif.matrices.recipe.v1`)

| field | meaning |
|---|---|
| `id`, `slug`, `title_en`, `title_ar` | identity |
| `parents[3]` | `{role, style_id, family, operator, why}` in the order structure, dynamics, finish. Distinct styles, distinct families, `operator` must be one of the parent's `operator_tags`, and no two parents may share code lineage (REA) |
| `bricks` | prose for `state`, `operation`, `law`, `time`, `memory`, `feedback` (all six required) |
| `grid`, `fps`, `duration`, `particles`, `seed` | simulation size and determinism |
| `stimulus` | the input (v1: `lemniscate_beam` with an on window) |
| `structure` | tessellation (v1: Voronoi tiles with per-tile absorption) |
| `memory` | `mode` (`persistent` or `instant`), `write`, `decay`, `diffusion`, `cap` |
| `coupling` | how memory steers dynamics: `gain`, `drag`, `flow`, `jitter`, `vmax` |
| `finish` | colours used by the scene |
| `conditions` | `A_full` plus counterfactuals; each `set` overrides dotted fields, e.g. `{"coupling.gain": 0}` |
| `metrics`, `acceptance` | trace threshold, settle time, required effect size, seeds, dose factors |

`recipe_hash` covers only fields that change the numbers, so renaming a recipe does not make it "new", and the ledger refuses to record the same hash twice.

## The law in v1 (glass that remembers light)

```
M(t+dt) = clamp( M + dt·(absorb_tile · write · L(t) − decay · M) + dt · diffusion · Δ_tile M , 0, cap )
v(t+dt) = (1 − drag) · v + dt · (gain · ∇M(p) + flow + jitter)
p(t+dt) = reflect( p + dt · v )
```

`Δ_tile` is the Laplacian restricted to neighbours in the same glass tile: lead lines stop diffusion (structure → memory). `∇M` is a bilinear central difference (memory → dynamics). Jitter uses the same seeded sequence in every condition, so conditions differ only by the field they change.

## Conditions

| condition | change | what it isolates |
|---|---|---|
| `A_full` | none | full mechanism |
| `B_no_coupling` | `coupling.gain = 0` | same memory field as A (checked bit for bit); motes ignore it → effect of the coupling |
| `C_no_memory` | `memory.mode = instant` | glass shows only the live beam; after the beam stops M = 0 → effect of persistence |

## Metrics and verdict

- **trace map:** persistent memory at the moment the beam switches off (A's field).
- **capture:** share of motes standing where the trace map is ≥ `trace_threshold` × its maximum; the **chance level** is the share of the pane that is on the trace.
- **main run:** capture curve per condition, memory remaining after the beam stops, end distance to A, identical-memory check.
- **replication:** A − B and A − C capture gains over every seed in `acceptance.seeds` (tiles and motes change with the seed), with mean, sd, min and a one-sided sign test.
- **dose-response:** A's capture for each coupling-gain factor, Spearman ρ.
- **verdict:** `CONFIRMED_IN_MODEL` only if B has A's memory, C has none after the beam stops, A beats B and C by the required margin in every seed, and ρ > 0.9.

EXP-0001 result: A−B +0.515 (sd 0.061, 8/8 seeds, min +0.428), A−C +0.340 (sd 0.040, 8/8, min +0.271), ρ = 1.0. Pixel check after the beam stops: A vs B differs on about 4% of pixels (motes only; the glow is identical by construction), A vs C on about 74% (the glow is gone in C).

## Scene page contract

The page works with both KOSIF renderers and the atlas storyboard convention:

- `window.seek(t)`, `window.DURATION`, `window.scoreSound`, `window.__ready`, `<canvas id="c">` → `kosif-superpowers/scripts/atlas_render.py` (needs Python Playwright).
- `window.__kosif = {duration, fps, seek}` → `tools/render_html.cjs` (node Playwright; used by `--mp4`).
- `?view=grid` (A | B | C | live chart), `?view=A_full` (one condition full frame), `?storyboard=1` (key frames with captions).
- `window.kmxPixelDiff(t)` renders two conditions identically and returns mean RGB difference and changed-pixel share.

It inlines `atlas_harness.js` (colour, noise, grain, layers), `atlas_sound.js` (offline score: riser, sparkles while the beam writes, a thud when it stops, a ding when the motes settle) and the repo font KOSIF Jumuah (OFL). Every frame is a pure function of `t`; `kmx_capture.cjs` checks it (`same_t_same_pixels`).

## Adding a recipe

v1 implements one stimulus (`lemniscate_beam`), one structure (Voronoi tiles) and one dynamics law (gradient steering). A new recipe that only changes numbers, parents' prose or conditions runs as is. A recipe with a new mechanism (for example memory written by the motes themselves, or a fold operator) needs a new adapter in `kmx_engine.py` plus a test that its counterfactual isolates one factor. Keep the rule: one condition, one changed field.

## Typed causal laws (v0.2 port, `scripts/kmx_laws.py`)

A second, smaller engine runs four particle laws from the owner's v0.2 causal studio (SRC-024). Each law has a typed contract (input port → output port) and one causal edge; arm B is arm A with only that edge removed, same light and same start positions.

| law | contract | edge removed in B |
|---|---|---|
| `trajectory_memory` | `ScalarField2D.grad → ParticleVelocity2D` | stored light → velocity |
| `material_memory` | `ScalarField2D.sample → MaterialOpacity` | stored light → material luminance |
| `elastic_memory` | `ScalarField2D.grad → ParticleDisplacement2D` | stored light → elastic displacement |
| `self_imprinting` | `ParticlePositions2D → ScalarField2D` | particles writing into the memory field (both arms still read it) |

`self_imprinting` is the "memory written by the motes" mechanism listed above as missing from v1. On top of v0.2's single A/B the port adds a dose sweep (gain × 0, 0.25, 0.5, 1): `CONFIRMED_IN_MODEL` needs zero effect at gain 0, an effect at full gain and Spearman ρ > 0.9. All four pass with ρ = 1.0. The arithmetic is unchanged from v0.2, so `tests/test_kmx_laws.py` checks the owner's demo metrics and SVG frame hashes exactly. `kmx.py laws run <recipe> --render <dir>` writes A/B SVG frames and a hash receipt (`laws verify <dir>/report.json`); keep those outputs out of git.
