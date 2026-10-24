# Code bricks — REA + static analysis of the 86 styles

`data/86_style_code_bricks.json` decomposes each of the 86 reference styles from its actual source code, not from its name or description. Evidence label: `E2_STATIC_CODE` (mechanism inferred from code; nothing executed or rendered).

## How it was produced

```bash
# 1. split the user's archive into a local tree (never committed: third-party text)
python3 -I .claude/skills/kosif-infinite-matrices/scripts/kmx_atlas_extract.py \
  --archive ai-style-atlas-prompts-FULL.zip --out /tmp/atlas-ref
# -> lib/harness.js, lib/sound.js, styles/<id>.js (86), cards/<id>.json, manifest.json (sha256 of each)

# 2. REA (github.com/morluto/rea, npm rea-agents 6.7.0, MIT), installed locally without install scripts
npm install --ignore-scripts rea-agents@6.7.0
npx rea import-reference-source /tmp/atlas-ref --detail summary --outline-depth 1 --format json   # inventory receipt
# one run over all files truncates REA's semantic graph (result budget), so run batches of 6 style files:
npx rea analyze-javascript-application /tmp/atlas-ref --artifact-format directory \
  --source-path styles/a.js ... --source-path styles/f.js --format json > batch_NN.json

# 3. combine lexical scan + REA batches into the committed, derived-only file
python3 .claude/skills/kosif-infinite-matrices/scripts/kmx_bricks.py analyze --src /tmp/atlas-ref --rea batch_*.json
```

REA facts recorded in the file: 15 runs, 1,121,538 AST nodes visited, 766,274 semantic nodes, 856,213 relations, 7,422 function fingerprints, no run truncated, all 86 style modules analysed.

## What each style record holds

- `bricks`: up to five labels per brick, ranked by frequency in the code
  - **state:** particle arrays, polyline points, grid cells, glyphs, noise values, palette
  - **operation:** path geometry, primitive shapes, fill/stroke, gradients, transforms, clip masks, compositing, alpha, blur, pixel read/write, offscreen layers, image compositing, text, patterns, dashes
  - **law:** periodic (sin/cos), exponential, power curves, distance fields, angle fields, quantize, noise fields, seeded random, interpolation, easing, clamp
  - **time:** eased reveal, periodic in t, stepped frames, history resampling, beat windows
  - **memory:** cached texture, trail by resampling earlier t, iterative build
  - **feedback:** within-frame pixel post-process, field steering geometry
- `features`: the raw counts behind every label, plus compositing modes used
- `rea`: functions, call sites, bindings, relations by type (reads, calls, writes, captures, aliases …), multi-line fingerprints and `shares_function_bodies_with`
- `tag_support`: whether the code supports each analyst tag from the earlier index

## Findings

1. **Every style is a pure function of time.** 0/86 carry pixels or state from one frame to the next. History is faked: 3/86 recompute earlier `t` inside the frame; most use cached textures (static memory, 82/86).
2. **The mechanism the glass recipe needs does not exist in the references.** A persistent material memory that changes later motion has to be simulated outside the frame and played back, which is what the engine does.
3. **Shared code lineage.** REA fingerprints show 38 styles reusing the same multi-line function bodies, in 10 clusters (the largest: whiteboard, chalkboard, blueprint, ballpoint-notebook, napkin-sketch, sketchbook-pencil, ukiyo-e and 11 more). Pairing two styles from one cluster is not an independent combination, so `recipe validate` and `ideate` refuse it.
4. **The earlier analyst tags hold up.** 202 of 211 checkable tags (95.7%) are supported by a matching code pattern. The 9 unsupported ones: watercolor·noise, papercraft·shadow, math-anim·ease, deep-sea·particles, chalkboard·particles, holographic-foil·reflection, win95·trace, gouache-poster·shadow, ms-paint·noise. These may use other helpers; they need a manual look before anyone relies on them.
5. **55/86 read pixels back inside a frame** (procedural textures, halftones, dithering) and **23/86 steer geometry with a computed field**. Only these 23 have a native "field drives motion" operator; the glass recipe takes its dynamics parent (flow-field) from that group.

## Limits of this analysis

- Pattern matching over code can miss a mechanism written in an unusual way or count an unrelated variable name (for example `cells` in a comment-free helper). Labels are evidence for a human, not proof.
- REA fingerprints prove identical normalized code, not identical behaviour; REA itself says so.
- No style was reconstructed or rendered in this pass (still E2, not E3).
