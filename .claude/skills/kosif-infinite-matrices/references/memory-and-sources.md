# Cumulative memory and source registry

## Two kinds of memory

| kind | where | what it is |
|---|---|---|
| material memory | inside a simulation (`M` in the glass recipe) | physical history that changes later frames of one run |
| research memory | `memory/ledger.jsonl` | what earlier experiments, ideas and reviews concluded, kept across sessions |

## Ledger (`memory/ledger.jsonl`)

Append-only JSON lines, committed to git. Each event has `seq`, `at`, `type` and `prev_sha256` (the sha256 of the previous line), so any edit to an old line breaks the chain and `kmx.py ledger verify` fails; `append` refuses to write on a broken chain.

| type | written by | enforced rule |
|---|---|---|
| `experiment` | `experiment --record` | one per recipe hash; stores verdict, checks, effect sizes, dose ρ, render evidence, sha256 of every artifact, source ids |
| `replication` | `experiment --record --replication` | links to the first experiment it repeats |
| `idea` | `ideate --record` | parent/role signature must be new (not in the 283 seeds, not in the ledger) |
| `rating` | `rate` | must name an existing experiment and a reviewer; score 0..5 |
| `hypothesis_status` | `hypotheses mark` | leaving `UNTESTED_UNRENDERED` needs an evidence file; its sha256 is stored |

Feedback into new work: `kmx.py ideate` ranks candidate triples by Beta(1 + wins, 1 + losses) posteriors per (role, operator), where a win is a confirmed experiment or a rating ≥ 4. Untested ideas add nothing. This ports the human-rating loop of the owner's v0.1.0 prototype (SRC-003) onto verified ledger events.

Current state: 1 experiment (EXP-0001, glass that remembers light, `CONFIRMED_IN_MODEL`, `RENDER_TESTED`), 0 ratings, 283/283 hypotheses `UNTESTED_UNRENDERED`.

## Source registry (`sources/registry.json`)

Every file or link that fed the work, keyed by sha256: title, names it arrived under, kind, bytes, pages, URL, rights, relevance (`core`, `method`, `context`, `not_relevant`), what it was used for, and a note. Content is never stored in the repo. The same bytes uploaded again become an extra name on the existing record (six of this session's uploads were duplicates).

```bash
python3 .claude/skills/kosif-infinite-matrices/scripts/kmx.py sources add --file path/to/new.pdf \
  --title "Exact title" --relevance method --rights "Copyrighted; not redistributed" \
  --used-for "what it changed in the engine;second use"
python3 .claude/skills/kosif-infinite-matrices/scripts/kmx.py sources verify --file path/to/new.pdf
```

An experiment names its sources with `--sources SRC-001,SRC-002`; the test suite checks that every id exists. How each registered source actually changed the design is in [sources-applied.md](sources-applied.md).

In a cloud session the ledger only lasts if it is committed; local runs that should not become shared memory can use `experiment` without `--record`.
