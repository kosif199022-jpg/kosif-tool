# KOSIF Structural Twin — trustworthy structural schematic → experiments

**Status:** executable illustrative v0.2 for 2D (plane) and 3D (space) *pin-jointed* elastic trusses. It is **not** a general continuum/3D mechanical simulator, a certified FEA package, or evidence that Anthropic has shipped the capability alleged in an internet post.

## Source and lesson
The 2026-10-08 user-provided social-media screenshot and ~40s motion video show an appealing six-stage framing and a neon instrument-panel visual style. Treat these as **creative inspiration**, not proof of physically valid inferred dimensions, force measurements or material properties. The photographed plush character is a *visual*, not trustworthy calibrated geometry. Never auto-infer engineering inputs as if measured.

## Implemented phases
1. **SHAPE** — ingest explicit node coordinates (m), unique bar endpoints, member areas (m²), Young's moduli (Pa), and material strengths (Pa). Validate all numeric inputs, shape, sizes and finite bounds.
2. **JOINT** — explicitly represent ideal frictionless pin joints and x/y constrained nodal supports; validate stability during solve. **DO NOT** imply arbitrary rigid, hinge, geared, welded, compliant or robotic joints are implemented.
3. **LOAD** — apply point loads in newtons; build a linear-elastic 2D truss global stiffness system, solve nodal displacement with pivoting and compute support reactions, axial force and stress; verify equilibrium.
4. **BREAK** — rank first-strength-limit multipliers. Optional hypothetical *brittle removal* at a supplied load-scale, re-solve after each idealized removed bar, and report singularity or termination. It is NOT a validated physical fracture/buckling/fatigue model.
5. **SWAP** — change one member's positive area, Young's modulus or strength, then recompute the entire system. Reveal new bottlenecks; strengthening the original weak component does not necessarily raise the global limit.
6. **RANK** — ascending force-multiplier to idealized *material axial-stress limit* (excluding buckling), with deterministic tiebreak by member id, after each case.

## Data contract
- JSON `nodes`: `{ "A": [0, 0], ...}` (2D) or `{ "A": [0, 0, 0], ...}` (3D — every node the same length; supports may use `z`, loads `fz_n`). `elements`: array of `{id,a,b,area_m2,young_pa,strength_pa}`.
- `supports`: node to an array of `x` / `y` directions; `loads`: array `{node,fx_n,fy_n}`.
- Output: `schema=kosif.structural-twin.v0.1` with `baseline`, `hypothetical_failure_path`, optional `swap`, `source_note`, `scope_warning`.
- Scope: 2D or 3D truss, small deformations, linear elastic, pin connections, static point load, axial force only. No dynamics, buckling, bending, shear, moment, material plasticity, friction, contact, vibration, fluid flow, collision, real-object geometry or building-code certification.

## Typical workflow
```
python scripts/kmotion.py structural --sample --out twin.json --swap AB --area 0.0002 --fracture-scale 3.2
python scripts/kmotion.py twinview twin.json --out twin.html
python scripts/kmotion.py proplan --task 'اصنع شرح SHAPE JOINT LOAD BREAK SWAP RANK لهيكل مفصلي' --seconds 18
python -m unittest discover -s tests -v
```
Replace `--sample` with `--model verified_geometry.json` to analyze known dimensions/materials; unknown material inputs must stay unknown. The dashboard runs offline from embedded report data and presents the baseline, swap and a load visualizer. Slider scales the *linear response*, not a new nonlinear solve. For any proposed physical hardware design, consult a qualified engineer and perform validated modeling and experimental tests.

## Media integration
When making an educational 3D scene or reel, use six storyboard beats SHAPE→JOINT→LOAD→BREAK→SWAP→RANK. Use topology-correct callouts, before/after side by side, measured units, clear captions, support reaction diagrams, and rank labels. Only report forces from actual simulation output and input provenance; annotate every hypothetical failure or artistic deformation. Do not present animation as physics proof.

## Security / privacy / authority
Offline / no external libraries / no `eval` / no arbitrary code execution. Input JSON is untrusted; typed validation and model-size ceilings. No external image or network references in standalone HTML. No upload of private engineering models without user authorization. Full Pro is a separate, request-bound KOSIF Think runtime and cannot be established by any local planning script, static HTML or unverified receipts.

## 3D space trusses (v0.2) and the bunny example
`analyse()` detects the dimension from the node coordinates. A 3D node has 3 DOF; every free node needs at least three
non-coplanar members or the stiffness matrix is singular and the solve fails closed ("Unstable or ill-conditioned").
With NumPy present the reduced stiffness is checked by its smallest eigenvalue and solved by LU; without NumPy the
original pure-Python eliminator runs. Verified against the symmetric tripod hand calculation (`tests/test_space_truss.py`).

`scripts/projects/bunny_twin/twin/build_truss.py` puts 35 nodes on a sculpted plush bunny (feet, pelvis, chest, neck,
skull, ear roots, ear tips) and 109 members, with **chosen, not measured** felt-proxy values. Solved: first limit
2.38× at the left ear root (`earL_out-crown`); at 3.0× the idealized removal of that member leaves a mechanism (the
ear flops); swapping it for a 2.6× area member raises the first limit to 3.77× and moves the bottleneck to
`earL_front-crown`. The film shows exactly these numbers and says on screen that the values are illustrative.
