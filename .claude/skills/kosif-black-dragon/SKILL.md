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

## Evidence and limits

`sources.jsonl` stores one machine-extracted link per catalog entry with its source hash and code fingerprint (where a local file exists). `summary.json` stores the exact input count and index hash. `verify` detects changed or missing sources. These are fast bookkeeping checks, **not** 7,000 functional test runs.

The initial implementation covers catalog discovery, extraction, exact source linking, simple native task matching, and provenance checking. It **does not** claim that every catalog method has been rewritten into one runtime program, or that every original feature has been manually reviewed. Those milestones require actual further code and cannot be inferred from a generated index.
