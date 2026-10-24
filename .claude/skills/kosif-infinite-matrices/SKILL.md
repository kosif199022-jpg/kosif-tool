---
name: kosif-infinite-matrices
description: Invent visual and motion systems from state, operation, rule, time and memory. Analyze KOSIF's 86 style research examples as evidence; synthesize new causal rules and test counterfactuals before claiming execution.
---

# KOSIF Infinite Matrices — المصفوفات اللانهائية

**Part of KOSIF Superpowers** · Status: research and numeric test skill, not a finished visual renderer.

## Core premise

The 86 reference styles are observations/results, not 86 atomic executable abilities. Decompose them to five *grammatical* bricks (NOT five renderer functions):
- **S / State:** numeric values, geometric geometry, color, material, positions, velocities, meaning, and sound.
- **O / Operation:** measuring, tracing, transforming, combining, propagating, masking, rasterizing.
- **F / Rule:** causal condition, equation, type requirements, boundary conditions, constraints.
- **t / Time:** frame steps, interpolation, rhythm, ordering, latency.
- **M / Memory and feedback:** distinguish *physical material history* within a running simulation from *research feedback* that scores previous ideas.

From the user's source archive a research audit indexed 86/86 styles across 14 families. It tagged 112 possible operator labels into 12 *hypothetical* root families; these are analyst labels, not 112 verified tools or irreducible primitives.

## Procedure

1. State the user goal as observable behavior; identify typed variables, coordinates, units, initial conditions.
2. Select source mechanisms by actual behavior rather than names. Track each parent style and the evidence of the extraction; see [causal taxonomy](references/causal-roots.md).
3. Assign independent roles to three sources: **structure**, **dynamics**, **finish**. Specify typed adapters and a new cross-operator causal coupling. Mere overlays or adjective mixing do NOT qualify as mechanism invention.
4. Write the law `S(t+dt) = F(S(t), O, M(t), inputs, constraints)` and `M(t+dt) = G(M(t),S(t), inputs)`. Predict what changes under an intervention.
5. Generate reproducible *hypothesis specifications* from an available 86-card catalog using `scripts/matrices.py`. Use controlled seeds; prohibit duplicate parent styles/families. An unrendered hypothesis is never a new tested renderer.
6. Perform a controlled experiment against an identical-input run with the cross-coupling disabled (A/B counterfactual). The bundled `scripts/glass_memory_probe.py` is a **numeric-only** reference, not a movie.
7. If renderer/rights available, render both A/B scenarios, inspect result, preserve original media, review visual quality and meaning, log lineage/params. Human review is required to promote a recipe.
8. Distinguish `PROPOSED`, `NUMERIC_TESTED`, `RENDER_TESTED`, and `PRODUCTION_READY`. Never call a scored proposal an autonomously learned skill.

## CLI

From repo root:

```bash
python3 .claude/skills/kosif-infinite-matrices/scripts/glass_memory_probe.py --json
python3 .claude/skills/kosif-infinite-matrices/scripts/matrices.py --catalog path/to/86_style_research_database.json --count 75 --seed 20261024
python3 -m unittest discover -s .claude/skills/kosif-infinite-matrices/tests -v
```

The 86-card source-grounded research database and extended methodology are in the separately delivered full research bundle (user-supplied archive analysis), **not checked into this PR**. Supply it with `--catalog`. The `matrices.py` CLI refuses to claim coverage without exactly 86 unique cards.

## Proof / guardrails

E1=reference indexed; E2=causal mechanism analyzed; E3=visual reconstruction verified; E4=independent runnable module and tests; E5=experimentally validated progressive improvement. The analysis is E1/E2. A numeric A/B experiment is not E3. New source operator ideas must be labelled as proposals, not proof of universal novelty.

Respect [parent Superpowers protocol](../kosif-superpowers/PROTOCOL.md), applicable AGENTS.md / original media rights / CI and consent gates. Do not merge/publish a new engine to main before existing tests and repository checks complete.
