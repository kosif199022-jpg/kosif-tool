---
name: kosif-black-dragon
description: "التنين الأسود: new independent skill that studies the KOSIF catalog, links each original source to one traceable entry, and synthesizes new task-specific working methods without invoking legacy tools by default."
---

# التنين الأسود — Black Dragon (Native Fusion)

**Product:** one new skill with its own analysis and synthesis logic. It is not a wrapper around thousands of old scripts.

## Working contract

1. Open and extract every catalog entry, preserving its original ID, source path, source SHA-256, methods, requirements, and any actual code-file fingerprint.
2. Link the entry immediately to the new Black Dragon source ledger. No orphan entries and no double counting.
3. Distinguish the four completion levels: **source-linked**, **machine-extracted**, **native-implemented**, **real-execution-verified**. Never label extraction as implementation.
4. Synthesize overlapping knowledge into a coherent new approach, preserving non-overlapping constraints. Keep original references as an audit trail, not as mandatory runtime dependencies.
5. Turn extracted insights into native executable features when practical. Only mark a feature implemented after its new code exists. Count executed only from real task evidence.
6. Original Black Dragon / Dragon Mind / standalone tool routing is **off by default**; legacy IDs can be returned as **optional links**, without executing them.

## Commands

Run from repository root:

    python3 .claude/skills/kosif-black-dragon/scripts/black_dragon.py index --out out/black-dragon-fusion-01
    python3 .claude/skills/kosif-black-dragon/scripts/black_dragon.py compose "اعمل مونتاج سينمائي على الإيقاع" --index out/black-dragon-fusion-01/sources.jsonl
    python3 .claude/skills/kosif-black-dragon/scripts/black_dragon.py verify --out out/black-dragon-fusion-01

To include *only optional pointers* to catalog entries, add `--legacy-links` to compose. No external process, paid model, or original adapter is invoked by these commands.

## Native reasoning absorbed from Dragon Mind

The new `scripts/native_mind.py` **contains its own** 26-faculty taxonomy and six-stage cognitive
cycle, based on Dragon Mind's controlled vocabulary. It does **not** import or run
`kosif-dragon-mind`, the legacy `black_dragon.py`, or their adapters.

`compose` now includes a `native_mind` result with:

- Task-specific faculty classification and the six thinking stages:
  frame → explore → decide → build → verify → learn.
- Native, source-traceable merging of identical method fragments. **Different
  constraints are preserved**, even when methods are similar.
- Typed input/output handoffs and an explicit critic for missing inputs.
- A source-ID lineage for every extracted method and a clear distinction between
  native thinking implemented and original features not yet reimplemented.
- Original tool references remain links only when `--legacy-links` is explicitly requested.

## Catalog-wide native fusion atlas

The `index` command now creates **`fusion_atlas.json`** in addition to `sources.jsonl`:
it feeds *all catalog records* through the independent 26-faculty native mind,
combines exactly repeated instructions without losing their contributing source IDs,
and retains each distinct instruction and original source lineage. Unlike task-specific
`compose`, the atlas is built across the full indexed catalog rather than the
top 12 matching sources. Markdown skills, playbooks and protocols contribute their
full original text rather than headings alone. `verify` also checks the atlas hash
and every source ID in its membership list. A changed or missing atlas fails verification.

The atlas is **a knowledge artifact, not an executable substitute for 7,000 programs**.
Semantic equivalence, conflicts, execution, and media/API capabilities still require
further implementation and evidence. Optional pointers to old tools remain disabled
by default; no legacy process is executed during fusion.

This is a first **native cognitive fusion engine**. It is deterministic text/knowledge
synthesis; it does not independently render video, transcribe audio, or execute all
underlying programs. Source hashing, extraction, reasoning, implementation, and
actual execution must continue to be reported as separate milestones.

## Verified composition and Arabic matching

- Task lookup now normalizes Arabic diacritics, tatweel and common Alef variants; it retains original tokens while also matching common prefixes such as `الـ`, `والـ` and `للـ`. This is deterministic lexical matching, not a semantic language model.
- When a sibling `fusion_atlas.json` exists, `compose` checks its checksum, the source-index checksum and its full source-ID membership against `summary.json`. Modified or stale indexes and atlases fail closed; regenerate with `index` instead of presenting unverified synthesis.
- `verify` rejects out-of-root paths and symlinked source/code references even if the referenced bytes happen to hash to the expected value.
- These checks are **local integrity guards, not cryptographic signatures, authority validation, or runtime execution proofs**. Running the old tools remains disabled by default.

## Evidence and limits

`sources.jsonl` stores one machine-extracted link per catalog entry with its source hash and code fingerprint (where a local file exists). `summary.json` stores the exact input count and index hash. `verify` detects changed or missing sources. These are fast bookkeeping checks, **not** 7,000 functional test runs.

The current implementation covers full-catalog extraction, exact linking, catalog-wide method grouping and lineage, task-specific native composition, and integrity checking. It **does not** claim that every catalog method has been rewritten into one runtime program, or that every original feature has been manually reviewed. Those milestones require actual further code and cannot be inferred from a generated index.

## Creative Council — no artistic gatekeepers

The new independent creative council has **12 expert roles** (not a rights officer): chair, analyst, dramatic writer, creative director, visual director, motion/render engineer, adversarial critic, decision specialist, researcher, systems thinker, audience advocate, and learning specialist.

It reads **443 core cognition records across nine datasets, plus 82 contextual Atlas Mind operating records (525 total)**: 159 Dragon Mind frameworks, 63 Superpowers mental models, 47 thinking-core powers, 29 creativity powers, 14 planning powers, 41 prompt-design powers, 18 strategy powers, 64 book-derived methods and eight reasoning modes, as well as 82 Atlas Mind workflow/memory/verification methods. It assigns every record to one primary expert, with nonexclusive secondary lenses. The 63 mirror cards in `data/powers/mental-models.json` are not double-counted. An independent set of 100 persona profiles is consulted only as optional specialist prompts. Counts are not independent agents, live tools, or semantically unique methods. See [the reviewed source audit](../../../docs/BLACK_DRAGON_THINKING_REVIEW_20261106.md).

From the repository root:

```bash
python3 .claude/skills/kosif-black-dragon/scripts/creative_council.py roster
python3 .claude/skills/kosif-black-dragon/scripts/black_dragon.py council "اعمل مونتاج درامي من صوت" --out out/creative-council.json
python3 .claude/skills/kosif-black-dragon/scripts/creative_council.py verdict --plan out/creative-council.json --submissions submissions.json --out out/verdict.json
```

There is **no compulsory member quorum, debate-round count, artistic rights seat, rights veto, or forced final vote**. The optional rounds are proposals, cross-examination, and scoring, and may be supplied partly or not at all. Unscored or incomplete opinions stay advisory, without invented winners or evidence. The optional weighted scoring uses only provided criteria and never proves aesthetic merit. A claim of independent expert runs needs corresponding distinct run IDs; simulated or unverified opinions are clearly labelled.

**Safety and action boundary:** no hard artistic censorship or veto seat, but council planning cannot itself pay for tools, upload media or publish anything. Those actions still require the appropriate authorization and actual licence/rights checks at the execution stage. Do not claim a video, preview, independent council debate, or completed media QA from a planning receipt.

Run the quick tests with:

```bash
python3 -m unittest discover -s tests -p test_black_dragon_creative_council.py
```


## Book-informed judgment guard (Thinking, Fast and Slow)

A new optional cognitive review is implemented at
scripts/judgment_guard.py and exposed through the Black Dragon CLI:

~~~bash
python3 .claude/skills/kosif-black-dragon/scripts/black_dragon.py think-review \
  --input video_brief.json --out out/judgment-review.json

python3 -m unittest discover -s tests -p test_black_dragon_judgment_guard.py
~~~

It uses eleven documented lenses from the 468-page user-supplied edition
of *Thinking, Fast and Slow*: two-system workflow metaphor, hard-question
substitution, missing evidence / WYSIATI, base rates, anchoring, availability,
expert intuition, outside view, premortem, framing and remembering versus
experiencing the edit. It assigns review questions to existing council seats,
without reinstating a rights seat or mandatory debate cycles.

**Important:** This is deterministic, adaptive review planning rather than
a new independent AI reasoner. It does not assert that any video has been
rendered, any audience response measured, or any cognitive bias solved.
See docs/BLACK_DRAGON_KAHNEMAN_THINKING_UPGRADE_20261106.md for source page
numbers, sample inputs, testing and limitations.


## Source-linked external Atlas candidate bridge (2026-11-06)

The **current 525** core/contextual source records remain separately counted and uniquely
assigned to the 12 council seats. A new **non-executing candidate bridge** reads
`docs/atlas_thinking_candidates_20261106.json`, pinned to Atlas commit
`99bb108dff169880dd531359f474a01b73c4b233`, and routes its **26 inspected
source paths** to those same seats, recording an exact byte-duplicate pair. It
does **not** count the sample as complete Atlas coverage.

`scripts/atlas_council_bridge.py` provides **23 locally adapted, source-linked
planning procedures** (nine cognitive-operation labels + fourteen reasoning-pattern
labels) with a primary seat, optional supporting seats, a question, expected evidence,
and a source trace. These are candidate *procedures*, not 23 proven novel mental
models or runnable external agents. They are returned under `external_atlas`
when using `black_dragon.py council`, and appear in each relevant council seat.
They do not inflate `total_source_records=525`, do not fetch third-party code,
and cannot perform autonomous research, execution, or media rendering.

Test the integration from repository root with:

~~~bash
python3 -m unittest discover -s tests -p 'test_black_dragon_atlas_council_bridge.py' -v
python3 .claude/skills/kosif-black-dragon/scripts/black_dragon.py council "فكر في سبب مشكلة البرنامج واختر خطة إصلاح" --out out/council-with-atlas.json
~~~

The bridge validates source paths, roles, pinned source commit, and the known
duplicate reference before planning. Title/keyword relevance is only lexical;
semantic de-duplication of all external Atlas skills and end-to-end agent execution
remain separate, uncompleted work. CI must pass before merging to `main`.

## Combined book-to-council thinking integration (PR #238 + PR #233)

The Dragon Mind's **39** new `tfs-*` frameworks from *Thinking, Fast and Slow* are
counted once within the 525 native source records, alongside the 82 existing
contextual Atlas Mind records. The updated book record reports 468 PDF pages
with 584 page-cited insights; the PDF is not committed. Three older frameworks
were also enriched with book references and are not counted again.

The council calls the **existing** `dragon_mind.py scan_traps` function during
planning, rather than approximating its logic. It routes task-linked
questions, correction moves and PDF page citations to each trap's primary
expert and the critic seat, without adding a compulsory quorum or a
rights-only member. The complete summary is returned as
`kahneman_review`; each seat receives `kahneman_review_questions`.
The always-checked WYSIATI, substitution and overconfidence questions are
precautionary **hypotheses**, not proof that a real person or model has a bias.

Together, the external Atlas candidate procedures and book guards are
advisory reasoning scaffolds. They do not claim independently run experts,
actual tool execution or superior results without measured comparisons.
Verify tests on the combined PR head before merging into `main`.


## Wired into the Black Dragon engine (2026-11-07)

The council is now a registered program of the main engine
(`kosif-superpowers/scripts/black_dragon.py`), not just a file in the repo:

- **Adapter `skill:kosif-black-dragon`** (recipe `creative-council` in
  `_black_dragon_skill.py`). `black_dragon.py run ... --execute-adapters` convenes the
  council on the task twice and checks: 12 distinct seats, all 525 records with one
  primary seat each, a stable fingerprint, 31 Kahneman traps loaded with the three
  System 2 gates routed to the critic, 23 Atlas procedures routed to seats, the
  11-lens `think-review`, and a known-answer verdict (the clearly better route must
  win; a fake `INDEPENDENT` claim without run IDs must be refused).
- **`compose`** now returns `thinking_guards`: Dragon Mind's real `scan_traps` on the
  task, with question, debiasing move, book pages and reviewing seats.
- **`think-review`** now adds `book_trap_scan` (the full 31-trap scanner) next to the
  11 fixed lenses.
- The **`dragon-mind`** adapter now also checks the book: the always-on gates are in
  the plan, a planted anchor is caught with pages 103–108, and page 69 is served
  from the 468-page record.

Try it:

~~~bash
python3 .claude/skills/kosif-superpowers/scripts/_black_dragon_skill.py creative-council out/cc.json --task="اختار أفضل خطة مونتاج"
~~~

These are still planning and scoring steps: no agent, model, media or paid tool runs.
