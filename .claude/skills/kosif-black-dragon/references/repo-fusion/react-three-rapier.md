# pmndrs/react-three-rapier — REA dissection (@ae5c3fede5ca, ≈1.5k★, MIT © 2022 Poimandres)

## What it really does
React Three Fiber bindings for the Rapier physics engine (WASM, `@dimforge/rapier3d-compat`). The core is `components/Physics.tsx`: a fixed-timestep accumulator driven by the wall clock (587-641), interpolation between previous and current body state by accumulator/timeStep (643-705), sleep/wake handling (670-700), collision started/ended events (708-), and solver parameters (iterations, linear error, CCD substeps; 436-449). Utilities generate colliders from mesh geometry (utils-collider.ts:327), instanced bodies, interaction-group bitmasks and joint hooks.

## Capabilities (10)
Native: fixed-step accumulator, state interpolation, sleeping, collision events with frame numbers, solver params.
Source-linked: colliders from geometry (utils-collider.ts:327), InstancedRigidBodies.tsx, interaction-groups.ts, hooks/joints.ts, contact pair filters (Physics.tsx:603).

## Covered vs new
The physics-math skill covers single-body fall, bounce and projectiles. New: multi-body contacts (ball–ball, ball–wall) with friction, spin, sleep and a per-impact frame number for SFX sync, all on a frame clock.

## Native: native_rapier_bake.py (stdlib)
Own code porting the ideas: the wall-clock dt is replaced by the video frame clock (frame/fps), so the output is bit-identical on every run. Dynamic circles vs static boxes/circles, 2D. Subcommands: bake, example, self-test. Output: per-frame transforms JSON + contact events with frame numbers.
Self-test: `SELF-TEST PASS (10 checks)` — first impact 0.637 s vs analytic 0.639 s; rebound apex 0.505 vs 0.500 (e²h); deterministic sha256; render-fps independent; settles and sleeps; momentum conserved; elastic velocity swap; rolling spin; bake round-trip 90 frames / 12 events.
Limits: no dynamic boxes or joints; stacking stability is basic and does not match Rapier.

## REA log
analyze_javascript_application on components/Physics.tsx → ev_d03814b1f9c6c87b99cc2d3837e07b899f3713b39e8405daf96e89375af757ab: 1 file, 0 parse failures, 20 files intentionally not selected; no IPC, network or child processes (plain React). Rest read by hand. No target needed closing.
