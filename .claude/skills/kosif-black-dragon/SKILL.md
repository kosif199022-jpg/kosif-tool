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

It reads the original **120 Dragon Mind frameworks**, **63 Superpowers mental models**, and **47 thinking-core power records**, assigns every record to exactly one primary expert and may share nonexclusive secondary lenses. Counts are source records, not independent agents, live tools, or unique methods after semantic deduplication. The independent native Black Dragon's existing media boundary remains unchanged.

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
