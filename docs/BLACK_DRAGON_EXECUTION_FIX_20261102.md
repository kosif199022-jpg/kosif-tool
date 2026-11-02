# Black Dragon executable adapter diagnosis — 2026-11-02

## Root cause

The Black Dragon catalog mixes executable **tools** with **skills, powers, styles, playbooks, protocol rules and other references**. The previous `run` CLI used an **empty adapter registry by default**, even though `data/black_dragon_adapters.json` contains reviewed tool adapters. Consequently, the ledger marked almost every catalog entry `blocked` with the generic `No executable adapter registered` message.

Registration is distinct from execution. A documented method is not a binary, and `--help` probes are not evidence of output production.

## Fix

- `run` and `plan` now load the bundled **reviewed** adapter registry by default. The `--adapters PATH` option still overrides it; `--reviewed-adapters` remains compatible.
- **Nothing executes by default.** `run` still needs `--execute-adapters`; paid, network, install and destructive workflows are not added.
- `doctor` reports indexed catalog counts, registered reviewed tool adapters, missing tool adapters, knowledge-only entries, unknown adapter IDs and invalid script paths.
- Ledger reasons distinguish missing **tool adapters** from **knowledge-only** entries.
- `reviewed_execution_complete` means *all selected reviewed adapters executed with receipts*. The existing `full_coverage` continues to indicate whether every catalog entry executed; it is not automatically upgraded to true.
- An opted-in run exits successfully when the reviewed adapter set completed, even if the full mixed catalog includes non-executable knowledge entries. A partial/failing reviewed run retains a nonzero result.

## Reproduce and verify

Run from the repository root:

```bash
python3 .claude/skills/kosif-superpowers/scripts/black_dragon.py doctor
python3 .claude/skills/kosif-superpowers/scripts/black_dragon.py plan "مونتاج فيديو"
python3 .claude/skills/kosif-superpowers/scripts/black_dragon.py run "مونتاج فيديو" --job out/black-dragon-adapter-check --execute-adapters --workers 4
python3 -m unittest discover -s tests -p 'test_black_dragon.py' -v
```

Choose a **new** job directory on subsequent runs. To inspect without allowing execution, omit `--execute-adapters`.

Actual audio/video production uses the already-existing dedicated pipeline. It is separate from catalog planning and requires an existing input file plus explicit execution:

```bash
python3 .claude/skills/kosif-superpowers/scripts/black_dragon.py media doctor
python3 .claude/skills/kosif-superpowers/scripts/black_dragon.py media run --input /path/to/clip.mp4 --job-name film-01 --execute --stabilize --reframe
python3 .claude/skills/kosif-superpowers/scripts/black_dragon.py media verify --job-name film-01
```

## Remaining work

The `tools_missing_reviewed_adapter` total is a **qualification backlog**. Each additional tool needs a known-safe supported command, dependency checks, sandbox rules, evidence artifacts and tests. Converting thousands of descriptive entries into thousands of nominal adapters would misrepresent executable coverage. Media transformations cannot be shown as completed until a real input has been processed and its output verified.
