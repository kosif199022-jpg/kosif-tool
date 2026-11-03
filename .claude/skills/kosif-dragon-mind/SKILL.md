---
name: kosif-dragon-mind
description: The thinking brain of the Black Dragon («عقل التنين الأسود»). Use when a task should be thought through before the Black Dragon runs, when the owner asks to decompose, rank or fuse all capabilities, to check which ones the dragon can really use, or says «عقل التنين», «فكّر بالتنين», «فكك القدرات», «Dragon Mind». It decomposes every catalog entry into 26 faculties, measures a usability tier for each, folds them into super-faculties, and runs a six-step thinking cycle with book-derived frameworks and GitHub-measured architecture patterns, then hands focused IDs to black_dragon.py.
---

# KOSIF Dragon Mind — عقل التنين الأسود

One super-skill that sits **in front of** the Black Dragon (`kosif-superpowers/scripts/black_dragon.py`).
The dragon uses every capability; the mind decides *what each one is for*, *whether the dragon can really
use it*, and *which ones lead this task*. It never executes catalog tools, never spends, uploads or publishes.

## الفهرس / contents

1. [What it does](#what-it-does)
2. [Commands](#commands)
3. [Readiness tiers](#readiness-tiers)
4. [The thinking cycle](#the-thinking-cycle)
5. [Research data and its limits](#research-data-and-its-limits)
6. [Running the mind inside the dragon](#running-the-mind-inside-the-dragon)
7. [Every entry usable: the method applier](#every-entry-usable-the-method-applier)
8. [Rules](#rules)

## What it does

| step | command | result |
|---|---|---|
| تفكيك / decompose | `dragon_mind.py decompose` | every entry → up to 4 faculties (primary first) with input/output media kinds |
| قدرة الاستخدام / readiness | `dragon_mind.py readiness [--probe JOB]` | every entry → a tier T4…T0 with the reason; `--probe` runs the dragon's own `--help` probe on CLI tools |
| صهر / fuse | `dragon_mind.py fuse [--write\|--check]` | 26 super-faculties: members, tier mix, executors, champions, honest gaps and consent-gated external routes |
| تفكير / think | `dragon_mind.py think "<task>" [--deep] --out out/<work dir>` | `mind_trace.json` + `mind_report.md`: frameworks per stage, patterns, typed faculty graph, critic, hand-off commands |
| صحة / doctor | `dragon_mind.py doctor` | data files present, inventory reachable, snapshot fresh |
| محوّل / adapters | `dragon_mind.py adapters [--all] --out out/<job>/adapters.json` | reviewed adapters + the mind's own adapter; `--all` gives every other entry the method applier |
| ربط / link | `dragon_mind.py link [--write\|--check]` | `data/mind_links.json`: every entry linked to peers, next/prev stage, owner skill, specialist hint and faculty hub; exit 4 unless one connected network |
| تطبيق / apply | `card_apply.py ARTIFACT ENTRY_ID "<task>"` | one entry applied to the task: steps bound to the task, requirements checked here, acceptance checks, links; exit 3 when it cannot apply |
| تدقيق / audit | `dragon_mind.py audit --job out/black-dragon/<job>` | splits the dragon's receipts into tool adapters executed, mind executed and method cards applied (by status), re-checking every hash |
| سوبر باور / superpowers | `dragon_mind.py superpowers [--write]` | how many of the 483 superpowers have a real runner for every member power; `--write` gives those a chain adapter (`superpower_run.py`) |
| فك القفل / unlock | `dragon_mind.py unlock [--script out/<job>/unlock.sh]` | greedy install plan: which install makes the most entries ready here (installs nothing) |

Paths: scripts live in `.claude/skills/kosif-dragon-mind/scripts/`; run them from the repository root.

## Commands

```bash
python3 .claude/skills/kosif-dragon-mind/scripts/dragon_mind.py doctor
python3 .claude/skills/kosif-dragon-mind/scripts/dragon_mind.py fuse
python3 .claude/skills/kosif-dragon-mind/scripts/dragon_mind.py readiness --probe out/<job>/probe --out out/<job>/readiness.json
python3 .claude/skills/kosif-dragon-mind/scripts/dragon_mind.py think "اعمل ريلز موشن عربي لإطلاق منتج" --out out/<YYYYMMDD>-<name>
```

## Readiness tiers

| tier | meaning | counts as executed? |
|---|---|---|
| `T4-executable` | a reviewed Black Dragon adapter exists and its script is in the repo | only after `black_dragon.py run --execute-adapters` writes a SHA-256 receipt |
| `T3-runnable` | a registered CLI exists (argparse); `--probe` proves it starts | no — it started, it did not do the task |
| `T2-guided` | a skill / protocol / playbook file with a description Claude can follow | no |
| `T1-method` | a described knowledge card (power, superpower, style) | no |
| `T0-broken` | source missing or no description | must be fixed |

## The thinking cycle

`frame → explore → decide → build → verify → learn`. For each stage the mind picks one framework
(two with `--deep`) whose trigger words match the task, otherwise the stage default
(first principles, SCAMPER, expected value, MVP, pre-mortem, after-action review).
Each picked framework brings its questions, the artifact it must produce and a countable check.
Then the mind maps the task to faculties (task words + the five always-on faculties: plan, verify,
safety and rights, deliver, learn), chooses task-specific champions per faculty (task overlap, faculty
strength, tier), links nodes by typed handoffs (the output kind of an earlier node must feed the next) and
runs a critic: missing executor, broken handoff, no runnable verifier, consent needed.

## Research data and its limits

| file | source | what was measured |
|---|---|---|
| `data/frameworks.json` | curated operators from canonical thinking/product books | each framework's `book_evidence` = matches in the 10k-book corpus |
| `data/books_thinking.json` | goodbooks-10k (Goodreads metadata) | all 10,000 books screened by shelf tags; thinking/product/business/psychology books kept |
| `data/github_patterns.json` | GitHub search API metadata + README text of the most-starred repos | how many repos name each of 20 architecture patterns, with exemplars |
| `data/research_receipt.json` | — | the exact counts and the SHA-256 of every raw file |

Book analysis is **metadata analysis** (titles, authors, shelf tags, ratings), not reading the full text.
GitHub analysis is **lexical** (the repo's own description, topics and README name a pattern), not a code audit.
Rebuild with `scripts/_mind_research.py` from the raw files; never claim larger numbers than the receipt.

## Running the mind inside the dragon

```bash
python3 .claude/skills/kosif-dragon-mind/scripts/dragon_mind.py adapters --out out/black-dragon/<job>-adapters.json
python3 .claude/skills/kosif-superpowers/scripts/black_dragon.py run "<task>" --job out/black-dragon/<job> \
  --adapters out/black-dragon/<job>-adapters.json --probe-tools --execute-adapters
python3 .claude/skills/kosif-superpowers/scripts/black_dragon.py verify --job out/black-dragon/<job>
```

The entry `skill:kosif-dragon-mind` then runs as a reviewed adapter: the dragon executes the mind's
`think` on the task and keeps its report as a receipt-backed artifact. All other adapters stay read-only.

## Every entry usable: the method applier

Only a few hundred entries are programs; the rest are method cards, styles, skills and rules. The applier
(`scripts/card_apply.py`) makes each of them callable by the dragon: it reads the entry's own record
(SHA-256 checked), turns it into numbered steps bound to the task, checks its requirements on this machine and
writes the result. Its status is one of `applied-ready-here`, `applied-needs-install` (the missing package is
named, and `unlock` says what to install) or `applied-needs-connector` (needs a Claude connector or key with
consent). Report "method cards applied" as its own tier: it is not the Black Dragon's `validated` structural
check and not a reviewed tool adapter's `executed`; a procedure is not media that was produced.
`black_dragon.py` counts every receipt as executed (and may print `full_coverage: true`), so after a run with
`--all` always quote `dragon_mind.py audit --job ...`, which separates the tiers.
Generated real runners (`data/black_dragon_adapters_powers.json`, `data/black_dragon_adapters_styles.json`,
when present) are merged with the reviewed adapters first: an entry with a real runner never gets the applier,
and the hand-reviewed file wins over a generated one.

A superpower is a pipeline of member powers. `superpower_run.py ARTIFACT SP-ID TASK` runs each member's
real runner in order, hashes every step's output and exits 0 only when every member ran ("executed");
otherwise it writes "partial" or "none" and exits 3. `audit` counts these as `superpower_chain_executed`
and reports `real_executed` (programs that really ran) by kind, which is the number to quote.

```bash
python3 .claude/skills/kosif-dragon-mind/scripts/dragon_mind.py adapters --all --out out/black-dragon/<job>-all.json
python3 .claude/skills/kosif-superpowers/scripts/black_dragon.py run "<task>" --job out/black-dragon/<job> \
  --adapters out/black-dragon/<job>-all.json --probe-tools --execute-adapters --workers 16
```

## Rules

- Report three numbers separately: assigned, probed, executed. A tier is not execution.
- External executors (Higgsfield, Suno) are listed, never called: they spend credits or publish and need the owner's yes.
- Raw research files stay outside the repository; only aggregates and hashes are committed.
- After a catalog change run `dragon_mind.py fuse --write` and `dragon_mind.py link --write` so `data/mind_map.json` and `data/mind_links.json` match the live inventory (the applier falls back to the live inventory for a new entry).
- `unlock` never installs: the owner runs the commands where they want them.
