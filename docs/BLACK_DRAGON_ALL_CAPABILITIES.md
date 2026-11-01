# KOSIF Black Dragon — التنين الأسود / Full Catalog Activation

**Invocation:** «استدعِ التنين الأسود» or «شغّل التنين الأسود». The owner's rule: **every capability is used, none is left out; the dragon's intelligence decides how and where each one is used.** The existing `kosif-web-film` remains the separate code-drawn video director; Black Dragon is an **orchestrator**, not a film renderer.

## What it uses (7,378 entries today)

`black_dragon.py inventory` counts every type, failing loudly on duplicates:

| kind | source | today |
|---|---|---:|
| skill | every `SKILL.md` under `.claude/skills/` | 472 |
| power | `data/powers/*.json` | 5,860 |
| tool | `data/tools.json` | 204 |
| superpower | `data/superpowers.json` (fused powers) | 482 |
| style | `catalog/styles.json` (motion style atlas) | 297 |
| playbook | `playbooks/*.md` | 19 |
| protocol | `PROTOCOL.md` + `references/protocol/A*.md` | 45 |

## How the brain decides "how" (`_black_dragon_brain.py`)

For the task it gives **every** entry:

- **part** — one of the seven stages of the capability mind map (`data/capability_mindmap.json`): افهم، خطّط، اصنع، حسّن، جمّع وارندر، تحقّق، سلّم.
- **mode** — `execute` (a reviewed adapter runs it), `run-tool`, `follow-skill`, `apply-method`, `protocol-rule`, `visual-reference` or `quality-gate`.
- **weight** — `lead` (the top 5 of its part for this task), `core` (shares words with the task) or `support` (still assigned, never dropped).
- **application** — one line saying what it does for this task.

Relevance orders and weights; it never removes. Adapter `depends_on` lists build dependency waves (Kahn order), and an entry whose prerequisite did not execute is blocked, not run. The brain is deterministic and lexical, not an LLM; the same task gives the same `assignment_sha256`.

## Evidence tiers (never mixed)

| tier | meaning | how |
|---|---|---|
| assigned | in the plan with part, mode, weight; one line in `briefs.jsonl` with the SHA-256 of its source file | always, all entries |
| probed | a CLI tool with argparse answered `--help` on this machine (it starts and its imports load) | `--probe-tools` |
| executed | a reviewed adapter ran on the task, exit 0, nonempty artifact, SHA-256 receipt checked | `--reviewed-adapters` or `--adapters FILE`, plus `--execute-adapters` |

`full_coverage=true` needs **every** entry executed with a receipt, so today the run honestly exits 4. Assigned and probed are never reported as executed.

## Try it (from repo root)

```bash
python3 .claude/skills/kosif-superpowers/scripts/black_dragon.py inventory
python3 .claude/skills/kosif-superpowers/scripts/black_dragon.py plan "اعمل مونتاج ريلز بصوت"
python3 .claude/skills/kosif-superpowers/scripts/black_dragon.py run "اعمل مونتاج ريلز بصوت" \
  --job out/black-dragon/<unique-job> --workers 8 --probe-tools --reviewed-adapters --execute-adapters
```

The job folder gets `black_dragon_report.md` (Arabic/English summary), `black_dragon_report.json`, `black_dragon_plan.json`, `briefs.jsonl`, `all_skills_ledger.json`, `all_skills_report.json`, `receipts/`, `artifacts/` and `probes/`. Measured on 2026-10-31 in a cloud container: 7,377 assigned, 186 of 204 tools started, 24 of 24 reviewed adapters executed with receipts, 0 failed, about 12 s.

### Reviewed adapters

`data/black_dragon_adapters.json` holds 24 read-only repo tools (brief, hub find, discovery, routers, thinking, council and gate self-tests, export standard, agent-guard rules, evidence audit…) run on the task through `scripts/_black_dragon_exec.py`, which keeps the tool's own exit code and writes its stdout as the artifact. To connect more, map an **exact catalog entry ID** to a repo-relative Python script and its argv:

```json
{
  "tool:YOUR_REAL_TOOL_ID": {
    "script": ".claude/skills/kosif-superpowers/scripts/_black_dragon_exec.py",
    "args": ["{artifact}", "path/to/tool.py", "--task", "{task}"],
    "depends_on": ["tool:skill-intelligence"]
  }
}
```

Execution is **explicitly opt-in**. Keep network calls, paid services, deployment, installation and uploads out of adapters unless the owner authorises them separately. No shell string is built from user text. Adapters run with the local user's permissions; this is not a sandbox, so review them.

## Limits

- A power card that is documentation has no command; it is assigned and briefed, not executed.
- Session connectors (MCP servers such as Higgsfield or Suno) are not in the repository inventory and are never called by Black Dragon.
- The audit cannot certify artistic quality or what a third-party executor really did.
- Cinema Pro and `kosif-web-film` remain the renderers for real montage; Black Dragon does not make an MP4 by being invoked.

### Tests

```bash
python3 -m unittest discover -s tests -p 'test_black_dragon*.py' -v
```

They cover inventory of every kind against its sources, part/mode/weight for every entry, determinism, dependency waves and blocked dependents, explicit execution gating, unsafe paths, job reuse, the `--help` probe, the exec wrapper's exit code and a real run of reviewed adapters with checked receipts. The `Black Dragon checks` workflow also runs a full job on every pull request and uploads its receipts.
