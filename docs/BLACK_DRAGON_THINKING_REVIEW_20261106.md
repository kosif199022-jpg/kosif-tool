# Black Dragon — cognition inventory review (2026-11-06)

> **Combined-head update:** The current PR #233 branch also incorporates the
> separately authored PR #238 (Kahneman's *Thinking, Fast and Slow* page-indexed
> reasoning data). The inventory is now **443 core cognition records + 82
> contextual Atlas Mind records = 525 assigned records**, still **12 seats**.
> Earlier 404/486 figures below describe the pre-#238 audit, not the latest
> combined branch. The 26 sampled external Atlas paths and their 23 advisory
> thinking procedures are separate candidates, not 49 additional unique skills.
> CI and measured task-quality improvements remain to be verified.

## Unified Kahneman book and Council integration (PR #238 + PR #233)

The book branch provides a declared 468-page reading dataset containing 584
page-cited insights, adds 39 new `tfs-*` frameworks (31 explicitly marked
lexical trap hypotheses), and enriches three older frameworks with page
references. The combined council inventory includes the 39 only once, via the
same Dragon Mind frameworks source. The book itself is not committed.

The combined `creative_council.py plan` now calls Dragon Mind's own
`scan_traps(task, deep=True)`. Every resulting question carries the
source `framework:tfs-*` ID, referenced PDF pages, and an actionable
`debias_ar` check; it is routed to its primary expert plus the critic
seat. The three always-on checks (WYSIATI, question substitution and
overconfidence) are included when the book scanner returns them.

These are **lexical possible error prompts**, not proven biases and not
independent agent outputs. No review is compulsory and no new rights
member is introduced. The original 11-lens `judgment_guard.py` continues
to provide a separate structured review mode.

Integration test contracts: 159 frameworks (120+39), 525 total
records (443+82), 42 book-linked frameworks (39+3), 31 trap-labelled
new frameworks, 12 seats, unchanged 26 sampled Atlas candidate
paths, unchanged 23 Atlas planning procedure labels, exact source
references and no double-counting. A complete passing CI run on the
combined head is required before PR #233 may be merged into `main`.


## Result and exact scope

This is a **source-level review and deterministic routing audit**, not proof of
404 separate intelligences, semantic equivalence, independent LLM calls, or
successful film production. The independent Black Dragon `creative_council.py`
now reads nine original cognitive data sources and routes **404/404 distinct
core cognitive source records to 12 primary seats**, plus 82 contextual Atlas Mind
operating skills for **486/486** source records in the extended scope. Each entry retains its original ID,
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

## Contextual Atlas Mind operating methods (82 additional records)

`.claude/skills/kosif-superpowers/data/powers/atlas-mind.json` adds **82 separately
identified, historically documented contextual skills**, primarily concerned
with delegated work, memory, traceability, testing and planning. They are
routed to the same 12 seats, without automatic execution, in these counts:

| Seat | Core thinking | Contextual Atlas Mind | Extended total |
|---|---:|---:|---:|
| Chair | 15 | 20 | 35 |
| Analyst | 68 | 7 | 75 |
| Dramatic writer | 15 | 0 | 15 |
| Creative director | 46 | 0 | 46 |
| Visual director | 31 | 1 | 32 |
| Motion/render engineer | 44 | 12 | 56 |
| Adversarial critic | 52 | 17 | 69 |
| Decision specialist | 55 | 2 | 57 |
| Evidence researcher | 35 | 2 | 37 |
| Systems thinker | 23 | 0 | 23 |
| Audience specialist | 3 | 0 | 3 |
| Learning specialist | 17 | 21 | 38 |
| **Total** | **404** | **82** | **486** |

These 82 entries are *contextual operating methods*, not another 82 distinct
cinematic creative theories. Every source ID has exactly one primary assignment;
this role map does not establish semantic deduplication or effective agent runs.

There is also a `kosif-dragon-mind/data/books_thinking.json` list with **936
book metadata records** selected by shelf tags from 10,000 book entries. The
underlying texts were *not* read by that process, and these 936 records must
**not** be counted as 936 executable thinking methods.

### External KOSIF Atlas skill mirror — distinct scope

The separate [KOSIF Atlas](https://github.com/kosif199022-jpg/kosif-atlas)
includes third-party thinking skills such as:

- `thinking-tools/dialectic`: thesis/antithesis evidence collection with
  genuinely parallel agents *only when the required runner exists*;
- `thinking-tools/root-cause-investigator`: Five Whys and evidence-backed diagnosis;
- `sequential-thinking`: an MCP tool description, requires installation and runtime checks;
- `design-thinking/design-graph`: architecture/call-graph planning with review-before-install flags;
- `eigenthinking`: a nine-step method for capturing an expert's tacit process.

These are **sampled source files**, not an exhaustive audit of the external
Atlas index. Do not say that 486 covers the full Atlas skill universe or
install third-party scripts solely because a source card exists.

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

The first command should report role counts for **486** entries on the current
inputs (404 core plus 82 Atlas Mind contextual records); tests must actually run in an environment with the repository sources.
Do not confuse a read-only mapping audit with those Python execution results.

## November 6 PR base synchronization and CI regeneration

- Synced the latest `main` changes into the feature branch without merging PR #233 into `main`.
- Rebuilt the deterministic smart capability index using the repository's `smart_capabilities.py build` and `verify` commands after the merged manifest introduced the 211th tool (the older feature branch indexed 210).
- The single-use GitHub Actions rebuild workflow removed itself after generating and committing the index. The separate pull-request CI checks still need a fresh complete green run, and the PR remains a draft until then.
- The 486 thinking records are source-mapped and advisory; none of these regeneration steps establish independent model execution or a verified end-to-end media pipeline.
