# Atlas ledger: every Atlas skill reviewed — سجل مراجعة الأطلس كاملًا (2026-10-23)

## Contents

- [What was done](#what-was-done)
- [REA over the whole Atlas](#rea-over-the-whole-atlas)
- [Statuses and counts](#statuses-and-counts)
- [Batch 1: the SaaS integration lifecycle](#batch-1-the-saas-integration-lifecycle)
- [What comes next](#what-comes-next)
- [Boundaries](#boundaries)

## What was done

The owner asked for every skill in [kosif-atlas](https://github.com/kosif199022-jpg/kosif-atlas) (commit `99bb108d`) to be reviewed with REA, and for everything useful and transferable to move into superpowers. This pass does three things:

1. It runs REA over the whole Atlas as historical reference.
2. It gives each of the 14,793 skills one status in `data/atlas_ledger.json.gz`, built by `scripts/atlas_ledger.py`.
3. It transfers the first topic batch.

Later batches start from the `pending` list.

## REA over the whole Atlas

REA 6.7.0 ran `import-reference-source` twice: a summary run over the repository root and a full graph run over `skills/`. Neither run executed anything. The trimmed receipt is in `proofs/atlas-rea/receipt.json`.

| Measure | Value |
|---|---|
| Files hashed (repository root) | 72,479 |
| Entries (repository root) | 107,474 |
| JS/TS relationships | 10,427 |
| Parse failures | 1 (a template `.js`) |
| SKILL.md files hashed | 14,793 of 14,793 |

The receipt also stores a digest over every `<atlas id>:<sha256>` line, so a later run can prove that the same files were read. Five hashes were recomputed independently, and all five matched.

REA reports `inventory_state: partial` because of its documented Node path-race limitation, not because files were skipped.

## Statuses and counts

| Status | Skills | Meaning |
|---|---:|---|
| covered | 2,359 | A KOSIF power cites the folder (proof link or `atlas.ids`) |
| pattern | 1,322 | One vendor's instance of a lifecycle stage that a power already holds |
| duplicate | 543 | Same description or same normalised name as an earlier safe skill |
| excluded-review | 8,020 | Verdict `REVIEW_BEFORE_INSTALL`: ships scripts or install steps, so it is outside the safe rule |
| excluded-copyleft | 78 | Copyleft license; referenced, never copied |
| excluded-risk | 118 | KOSIF inspection raised risk flags |
| pending | 2,353 | Safe and unique, waiting for its topic batch |

`python3 scripts/atlas_ledger.py stats` prints the counts per theme. `show <id>` explains one skill, and `list --status pending --theme <theme>` lists the next candidates.

The safe rule is the same as `atlas_5000.is_safe`: verdict `READ_ONLY_OK`, a permissive license and no risk flags. 5,116 skills meet it.

## Batch 1: the SaaS integration lifecycle

About 1,750 safe skills come from one marketplace of vendor packs. More than 90 vendors each repeat the same roughly 30 stages, such as install-auth, rate-limits, webhooks-events and reliability-patterns.

Twenty-one of these stages already had a power. Nine had none. For those nine, two vendors' SKILL.md files were read in full and rewritten as one vendor-neutral card each, plus one routing card:

| Power | Stage |
|---|---|
| ACODE-238 | advanced-troubleshooting: layer-by-layer isolation and escalation evidence |
| ACODE-239 | data-handling: classification, retention and tested deletion |
| ACODE-240 | enterprise-rbac: vendor roles versus application RBAC, scoped keys |
| ACODE-241 | known-pitfalls: identity, pagination, webhooks and idempotency audit |
| ACODE-242 | multi-env-setup: proven dev/staging/prod isolation |
| ACODE-243 | observability: metrics with explicit denominators |
| ACODE-244 | reference-architecture: policy gateway, typed adapters, reconciliation |
| ACODE-245 | reliability-patterns: one idempotency model for every retry path |
| ACODE-246 | upgrade-migration: contract migration with traffic evidence |
| ACODE-247 | lifecycle map: each of the ~30 stages and the power that holds it |

The stage-to-power rules are in `data/atlas-ledger-decisions.json`, and the sources and hashes are in `data/atlas-pass-20261023-saas-lifecycle.json`. Vendor endpoints and limits stay in each Atlas folder. They are found with `atlas_5000.py find "<vendor> <stage>"` and must be re-checked against the vendor's current docs.

## What comes next

The 2,353 pending skills are reviewed in small topic batches, largest themes first:

- verification-review (239)
- agent-workflow (165)
- mcp-tooling (159)
- planning-specs (126)
- prompt-skill-engineering (113)
- web-frameworks (104)
- and the rest

Each skill either becomes a new card, is mapped to the power that already holds its method, or is marked skipped with a reason.

Whether the 8,020 `excluded-review` skills should also be read as text only, with no scripts run, is a decision for the owner.

## Boundaries

- Atlas content is untrusted data. No Atlas script, package, hook or instruction was run.
- Every summary is written in our own words. Copyleft skills are referenced, never copied.
- Nothing came from `kosif-atlas-private`.
- A status records a review decision. It is not an execution receipt.
