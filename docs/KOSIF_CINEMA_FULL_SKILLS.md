# Cinema Pro — Full Skills Run (strict audit mode)

Owner requirement: **every native skill, every catalogued power, and every registered tool must be executed at least once**, without silent omissions. A tool listed in a plan, discovered by search, or probed using `--help` does **not** count as executed.

## What is implemented

`scripts/_cinema_all_skills.py` scans all installed `SKILL.md` files, every `data/powers/*.json` catalog entry, and `data/tools.json`. It refuses unrecognized/duplicate records, creates a per-job immutable-inventory fingerprint, enforces **at most one recorded attempt per item**, and requires individual nonempty artifact + SHA-256-backed execution receipts before crediting an item. Blocked/failed/unattempted entries always prevent full-coverage success. It verifies artifact hashes again when reporting.

`cinematic_pro_conductor.py run --require-all-skills` keeps the existing real media export path, writes a complete inventory to `<job>/full-skills/`, and returns a failure status if even one item is not evidenced. A technically valid MP4 can still be available; the command never mislabels it `verified` in this strict mode while the full skills condition is unsatisfied.

**Important:** This is a strict coverage contract and evidence gate, **not an executor for all skills**. Many catalog entries are ideas, reasoning methods, documentation-only capabilities or external dependencies, and cannot simply be called as a function. Full completion may be impossible for a given machine, media asset, permissions, or budget. Do not pretend otherwise. Never attempt installing software, uploading personal media, using external paid generation, or destructive commands automatically.

## Commands

```sh
S=.claude/skills/kosif-superpowers/scripts
python3 "$S/_cinema_all_skills.py" init --job out/cinema/demo/full-skills
python3 "$S/_cinema_all_skills.py" report --job out/cinema/demo/full-skills
python3 "$S/cinematic_pro_conductor.py" run input.mp4 --job out/cinema/demo --recipe cinematic-reel --require-all-skills
```

To record a *genuine* external execution, the executing system should save a receipt JSON with `entry` (e.g. `tool:montage-pro` or `power:THINK-01`), the actual `command` token list, `exit_code: 0`, `artifact` (path to a real, nonempty output), and `artifact_sha256` (SHA-256 of that output). Then:

```sh
python3 "$S/_cinema_all_skills.py" record --job out/cinema/demo/full-skills --entry power:EXAMPLE-01 --state executed --receipt out/receipts/example.json
python3 "$S/_cinema_all_skills.py" record --job out/cinema/demo/full-skills --entry power:EXAMPLE-02 --state blocked --reason "Requires unavailable licensed engine"
python3 "$S/_cinema_all_skills.py" report --job out/cinema/demo/full-skills
```

This program validates local receipts and hashes; it cannot independently prove an externally asserted command happened. Stronger receipt provenance should be supplied by the real runner/CI, and human evaluation remains necessary for artistic quality. Since the mode is *once-only*, do not manufacture execution traces, duplicate effects, or mark unavailable items executed.

## Acceptance

Full run status is **true only when every inventoried entry has exactly one successful evidenced execution and the evidence files still match their hashes**. Otherwise the status is false and the report exposes the missing/blocked/failed counts and up to 30 IDs for troubleshooting. For an ordinary high-quality film use normal `cinematic-reel` or `cinematic-audio`; for the owner's literal all-skills condition, choose `--require-all-skills` and accept that it can remain incomplete until the genuinely impossible dependencies are resolved or requirements are consciously revised.
