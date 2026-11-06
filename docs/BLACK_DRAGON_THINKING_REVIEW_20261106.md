# Black Dragon — cognition inventory review (2026-11-06)

## Result and exact scope

This is a **source-level review and deterministic routing audit**, not proof of
404 separate intelligences, semantic equivalence, independent LLM calls, or
successful film production. The independent Black Dragon `creative_council.py`
now reads nine original cognitive data sources and routes **404/404 distinct
source records to 12 primary seats**. Each entry retains its original ID,
source path, source-reported maturity, and optional secondary roles.

| Original source (relative to repo root) | Count |
|---|---:|
| `.claude/skills/kosif-dragon-mind/data/frameworks.json` | 120 frameworks |
| `.claude/skills/kosif-superpowers/data/mental_models.json` | 63 models |
| `.claude/skills/kosif-superpowers/data/powers/thinking-core.json` | 47 powers |
| `.claude/skills/kosif-superpowers/data/powers/creativity-engine.json` | 29 powers |
| `.claude/skills/kosif-superpowers/data/powers/planning-execution.json` | 14 powers |
| `.claude/skills/kosif-superpowers/data/powers/prompt-craft.json` | 41 powers |
| `.claude/skills/kosif-superpowers/data/powers/strategy-finance.json` | 18 powers |
| `.claude/skills/kosif-superpowers/data/thinking_books.json` — `methods` | 64 methods |
| `.claude/skills/kosif-superpowers/data/reasoning_modes.json` — `modes` | 8 modes |
| **Total source records, before meaning-level deduplication** | **404** |

The `data/powers/mental-models.json` file has **63 entries mirroring the 63
standalone mental-model IDs** and is *not* counted a second time. The
`data/council_100.json` file has **100 optional persona profiles** (20 in
each of five evidence lanes). They are supplementary role templates, not
cognitive methods, agents, or execution proofs; all 100 can be assigned as
potential advisers without creating a rights seat.

## Primary assignments, exactly once per record

| Seat | Source records |
|---|---:|
| Chair / organizer | 15 |
| Meaning and first-principles analyst | 68 |
| Dramatic story writer | 15 |
| Creative director | 46 |
| Visual director | 31 |
| Video, motion, render engineer | 44 |
| Adversarial critic | 52 |
| Decision and trade-off specialist | 55 |
| Evidence researcher | 35 |
| Systems thinker | 23 |
| Audience and platform representative | 3 |
| Experiment and learning specialist | 17 |
| **Total** | **404** |

**Coverage assertion:** 404 distinct IDs; 0 duplicate IDs; 0 unassigned primary
roles in a read-only consistency check against the current source manifests.
The audience specialist has few **primary** methods but receives additional
**secondary** lenses from story, communication and product frameworks, plus
optional audience persona templates. A primary role count is not the quantity
of opinions to solicit in a meeting.

## Duplication and quality of source claims

A conservative normalization of English method names detects **25 repeated
name groups comprising 55 record occurrences** across the 404 inputs, including
*Inversion*, *Pre-mortem*, *SCAMPER*, *OODA Loop*, *Bayesian Updating* and
*First Principles*. Not all similar methods share the same name, and sharing
the same name does not prove the underlying procedures are equivalent. Preserve
every original ID and source when presenting a merged lens.

The five `powers` families together contain 149 records with source-declared
maturity: **122 documented**, **17 historically labelled proven**, **8 ready**,
and **2 install-dependent**. The other **255** frameworks, models, book methods
and reasoning modes do not use those power statuses. No historical `proven`
label was independently re-tested in this review. There is no new numerical
claim about tools or media that were executed.

Review of engine implementations:

- `scripts/think.py`: concrete deterministic reasoning scaffolds, model
  ranking, option matrices, sensitivity, Bayesian calculations, critiques
  and checks; the scaffolds do not themselves understand scene emotion.
- `scripts/decision_math.py`: numerical calculations, useful for practical
  trade-offs, not a cinematic director.
- `kosif-dragon-mind/scripts/dragon_mind.py`: six-stage cognitive cycle and
  source-aware faculty routing; partly lexical framework selection.
- `kosif-black-dragon/scripts/native_mind.py`: independent text-based method
  fusion, 26 faculties and typed handoffs, *not* actual editing or an LLM.
- `scripts/council.py` and `scripts/llm_council.py`: prepare prompts and
  validate the received evidence/positions; they do not invoke model agents.
- `scripts/thinking_books.py`: structured, checkable scaffolds derived from
  **64 methods / metadata of 40 books**, not a claim of reading full books.
- `scripts/creative_reasoning_bridge.py`: deterministic audio-cue-to-storyboard
  transformations, explicitly not neural emotion understanding.
- `scripts/invention_lab.py`: systematic falsifiable idea generation, not
  automatically validated expert reasoning.
- `scripts/creative_principles.py`: specific local creative exercises; an
  exercise working does not prove an appealing edit.

## Problems found, with corrective direction

1. **Lexical routing is not deep comprehension.** Use the method's own
   situation, question, output and check when assigning it to a scene;
   compare what it changes in an actual video, not just token overlap.
2. **Near-duplicate knowledge inflates apparent cognitive power.** Canonicalize
   equivalent methods into reusable *lenses* while retaining multiple source
   IDs, distinct conditions and divergent warnings.
3. **Council debate is not an automatic multi-model deliberation.** One-model
   roleplay must be labelled simulated. Only genuine independent runs with
   distinct IDs, recorded proposals and evidence justify an independent
   deliberation claim.
4. **Audience and emotional direction are underrepresented as primary
   categories.** Draw on the story/visual frameworks, audience profiles,
   `A8-motion-brain.md`, timed script/audio evidence, and genuine preview review.
5. **Tool choice must follow dramatic intent.** After finding emotion,
   composition, shot/transition and timing, choose between licensed footage,
   code-motion, 3D and hybrid; verify the actual renderer and media output.
6. **Some powers are contextual.** Financial optimization, robotics and
   accounting methods are indexed but never auto-run as filmmaking tools.
7. **No compulsory artistic quorum or member veto.** The requested rights
   seat was removed; the critic retains failure analysis. Permissions for
   paid tools, external upload or publishing remain execution boundaries,
   not votes over creative quality.
8. **No full execution test has been confirmed.** The test file is present.
   A passing repository CI run and one end-to-end video job with actual
   preview/media validation are still required before calling the new council
   production-ready.

## Reproducible commands

From repo root:

```bash
python3 .claude/skills/kosif-black-dragon/scripts/creative_council.py roster
python3 .claude/skills/kosif-black-dragon/scripts/black_dragon.py council "اعمل ريلز سينمائي من صوت" --out out/council.json
python3 -m unittest discover -s tests -p 'test_black_dragon_creative_council.py'
```

The first command should report role counts for **404** entries on the current
inputs; tests must actually run in an environment with the repository sources.
Do not confuse a read-only mapping audit with those Python execution results.
