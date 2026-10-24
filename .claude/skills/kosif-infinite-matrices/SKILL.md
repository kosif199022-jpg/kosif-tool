---
name: kosif-infinite-matrices
description: Invent new visual and motion systems from causal bricks (state, operation, law, time, memory, feedback) mined from the 86 reference styles; build a recipe, run an A/B/C counterfactual with seeds and dose-response, render it with the Superpowers atlas tools, and save the result in a hash-chained research ledger.
---

# KOSIF Infinite Matrices — المصفوفات اللانهائية

**Part of KOSIF Superpowers.** Status: working engine with one confirmed experiment (EXP-0001, `RENDER_TESTED`). The 283 hypothesis seeds are still `UNTESTED_UNRENDERED`.

بالعربي: المهارة دي مش بتخلط أساليب. بتفكك الـ86 أسلوب لعمليات بتنتج الشكل (حالة، عملية، قانون، زمن، ذاكرة، تغذية راجعة)، وبتركّب منها أسلوب جديد بقانون سببي، وبتثبت إن القانون ده هو السبب بمقارنة مع وبدون، وبترندره فيديو، وبتحفظ النتيجة في ذاكرة تراكمية.

## Front door

Everything runs through one CLI (stdlib Python; rendering needs node + Playwright + Chromium, MP4 also needs ffmpeg):

```bash
K=.claude/skills/kosif-infinite-matrices/scripts/kmx.py
python3 $K doctor                                     # what this machine can run, ledger chain, counts
python3 $K recipe validate .claude/skills/kosif-infinite-matrices/recipes/glass-remembers-light.json
python3 $K experiment --recipe <recipe.json> --out out/kmx/<slug> --render --mp4   # add --record to save it
python3 $K ledger stats                               # cumulative memory: experiments, ideas, ratings, 283 statuses
python3 $K rate --experiment EXP-0001 --score 4 --by "<reviewer>" --notes "..."
python3 $K ideate --count 10 --record                 # new parent triples, never a repeat, biased by feedback
python3 $K sources list                               # every source by sha256, rights, relevance, use
python3 $K bricks summary                             # REA + static-code decomposition of the 86 styles
python3 -m unittest discover -s .claude/skills/kosif-infinite-matrices/tests -v
```

From KOSIF Superpowers: `python3 .claude/skills/kosif-superpowers/scripts/hub.py tool infinite-matrices` prints the same commands; `hub.py find "زجاج بيتذكر الضوء"` routes here.

## Procedure

1. **Analyse sources as mechanisms, not names.** Read `data/86_style_code_bricks.json` (`kmx.py bricks show <id>`): per style, the six bricks inferred from its code plus REA function/call/data-flow counts. Pick parents by what their code does. See [code-bricks.md](references/code-bricks.md).
2. **Write a recipe** (`kosif.matrices.recipe.v1`, see [engine.md](references/engine.md)): three parents, one role each (structure / dynamics / finish), three different families, an operator actually tagged on each parent, all six bricks in words, the law as an equation, and counterfactual conditions that each change one field. `recipe validate` refuses parents whose code shares function bodies (REA fingerprints), because they are not independent sources.
3. **Run the experiment.** `experiment` simulates every condition from identical inputs, replicates over seeds, sweeps the coupling gain (dose-response) and returns `CONFIRMED_IN_MODEL` only when every check passes.
4. **Render.** `--render` writes `scene.html` (atlas page contract, reuses `kosif-superpowers/assets/atlas_harness.js` and `atlas_sound.js`), stills, and a pixel-level A/B/C difference; `--mp4` renders through `tools/render_html.cjs` with the offline atlas score. Look at the stills before claiming anything visual.
5. **Record.** `--record` appends the result to `memory/ledger.jsonl` with every artifact's sha256 and the source ids used. The same recipe hash cannot be recorded twice; a re-run is logged as a replication.
6. **Review.** A human rates the experiment (`rate`). Ratings and verdicts become Beta posteriors per operator that bias `ideate`. Nothing becomes `PRODUCTION_READY` without a human rating and a reviewed recipe.
7. **Register sources** before using them: `sources add --file ... --title ... --relevance core|method|context|not_relevant --rights ... --used-for "..."`. Same bytes under a new name become an alias. See [memory-and-sources.md](references/memory-and-sources.md).

## Status labels (use exactly these)

`UNTESTED_UNRENDERED` → `PROPOSED_RECIPE` → `NUMERIC_TESTED` → `RENDER_TESTED` → `PRODUCTION_READY` (or `REJECTED`). A hypothesis leaves `UNTESTED_UNRENDERED` only through `hypotheses mark ... --evidence <file>`, which stores the file's hash. Evidence ladder for analysis: E1 indexed, E2 mechanism analysed (`E2_STATIC_CODE` for the REA/code pass), E3 visual reconstruction verified, E4 runnable module + tests, E5 progressive improvement shown across generations.

## What exists now

| part | file | state |
|---|---|---|
| 86-style compact index (14 families, 112 tags) | `data/86_style_research_database.json` | E1/E2, from PR #131 |
| 283 hypothesis seeds | `data/283_hypothesis_seeds.json` | all `UNTESTED_UNRENDERED` |
| static code + REA decomposition of all 86 | `data/86_style_code_bricks.json` | `E2_STATIC_CODE`; 95.7% of checkable analyst tags supported by code |
| engine (recipe → simulation → metrics) | `scripts/kmx_engine.py` | tested |
| scene writer (atlas contract) | `scripts/kmx_scene.py`, `scripts/kmx_capture.cjs` | render-tested here |
| first experiment, glass that remembers light | `experiments/EXP-0001-glass-remembers-light/` | `CONFIRMED_IN_MODEL`, `RENDER_TESTED`, not yet human-rated |
| research ledger | `memory/ledger.jsonl` | hash-chained, 1 experiment |
| source registry | `sources/registry.json` | 23 sources, 29 file names |
| archive splitter (local only) | `scripts/kmx_atlas_extract.py` | writes third-party text outside git |

## Guardrails

- The causal claim is inside the numerical model only (same stimulus, same seed, one factor changed). It is not a claim about real optics or global novelty. Read [limits.md](references/limits.md).
- Never commit the extracted archive text or REA's raw output (third-party code); commit only derived numbers.
- An unrendered idea is a proposal. A numeric pass is not a visual pass. A rendered pass is not a human-approved style.
- Follow the [parent Superpowers protocol](../kosif-superpowers/PROTOCOL.md) for request levels, consent and publishing rules.

More: [engine.md](references/engine.md) · [code-bricks.md](references/code-bricks.md) · [memory-and-sources.md](references/memory-and-sources.md) · [examples.md](references/examples.md) · [limits.md](references/limits.md) · [sources-applied.md](references/sources-applied.md) · [causal-roots.md](references/causal-roots.md)


## Instagram reference research handoff (Superpowers TOOL-172)

The owner provided two unreviewed Instagram reference accounts, `@asirgokerr` and `@brkn.land`. For requests like "find reels about a 3D character morphing into pencil strokes", use:

```bash
I=.claude/skills/kosif-superpowers/scripts/instagram_reference_bridge.py
python3 $I plan "3D character transforms into pencil sketch"
python3 $I search "3D character sketch"
python3 $I propose https://www.instagram.com/reel/REALCODE/ --catalog .claude/skills/kosif-infinite-matrices/data/86_style_research_database.json --out out/ideas/KIG.json
```

`plan` generates third-party public search links, not results. Researchers must verify the reel and the right to view/analyse any footage first; `propose` maps metadata tags to candidate parent operators but is **not an executable recipe or validated discovery**. Only inspected frames should become observed mechanisms. Translate a reviewed proposal to the typed six-brick recipe in this skill, run a controlled A/B/C experiment, render, obtain human rating, and only then record an accepted capability in the KMX ledger. No Instagram scraping, media copying, or automatic promotion.

See [Instagram Discovery skill](../kosif-instagram-discovery/SKILL.md).
