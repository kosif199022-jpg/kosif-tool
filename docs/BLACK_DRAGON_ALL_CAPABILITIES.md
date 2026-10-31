# KOSIF Black Dragon — التنين الأسود / Full Catalog Activation

**Invocation:** «استدعِ التنين الأسود» or «شغّل التنين الأسود». This means **attempt every entry** in the installed inventory without task relevance filtering. The existing `kosif-web-film` remains the separate code-drawn video director; the new Black Dragon is an **orchestrator**, not a film renderer.

## What exists

`.claude/skills/kosif-superpowers/scripts/black_dragon.py` uses the same exhaustive inventory as `_cinema_all_skills.py`: every installed `SKILL.md`, catalogued power and registered tool. It schedules each item onto a bounded thread pool (1–32 workers, default 8), in one orchestration run, and produces an immutable inventory, per-item execution states, receipt files and a summary.

**Important technical distinction:** dispatching every item is possible; executing every item simultaneously is NOT universally possible. Many powers are conceptual cards, some tools need external accounts/media, and others cannot safely coexist or lack runnable adapters. Items without adapters are **blocked**, never mislabeled executed. `full_coverage=true` needs evidence for *every* item.

## Try it (from repo root)

```bash
python3 .claude/skills/kosif-superpowers/scripts/black_dragon.py inventory
python3 .claude/skills/kosif-superpowers/scripts/black_dragon.py run "اصنع مونتاج احترافي" --job out/black-dragon/first-run --workers 16
```

The second invocation inventories/distributes everything but defaults to **no adapter execution**; it will produce `out/black-dragon/first-run/black_dragon_report.json` and `all_skills_report.json` and return status **4**, accurately indicating incomplete full execution.

### Connect real executors

Provide a JSON mapping from an **exact catalog entry ID** to a repo-relative Python adapter file and its argument vector:

```json
{
  "tool:YOUR_REAL_TOOL_ID": {
    "script": "path/to/reviewed/readonly_adapter.py",
    "args": ["--task", "{task}", "--output", "{artifact}"]
  }
}
```

Only reviewed adapters meeting the contract (write a nonempty artifact at the `{artifact}` path; exit 0 on genuine success) should be registered. Run in a new output directory:

```bash
python3 .claude/skills/kosif-superpowers/scripts/black_dragon.py run "المهمة" --job out/black-dragon/real-run --workers 8 --adapters my_reviewed_adapters.json --execute-adapters
```

Execution is **explicitly opt-in**; avoid network calls, paid services, production deployment, installation or upload inside adapters without separate authorization. No shell commands are constructed from user text. Adapter scripts run under the local user's OS permissions, so **review them** before enabling; this is not an isolation sandbox. Concurrency is limited so memory, API quotas and media encoders are not flooded.

### Truthful evidence

An item counts as `executed` only if its adapter returns 0, writes an actual nonempty output and a receipt matches artifact SHA-256. Otherwise the status is `blocked` or `failed`. The report counts all three; "dispatched" is never "executed." A checkout without adapters therefore will **not** claim that thousands of skills were used. The audit cannot certify aesthetic excellence or independence of a third-party executor's asserted action.

The existing `Cinema Pro` and `kosif-web-film` renderers remain available for real montage. Black Dragon may coordinate them through individually tested adapters, but it does **not** automatically generate an MP4 simply by being invoked.

### Tests

```bash
python3 -m unittest tests/test_black_dragon.py
```

The tests cover exact inventory, partial/full receipt validation, explicit execution gating, unsafe paths and job reuse.

## User-facing operation

When user says **«استدعِ التنين الأسود»**, use the catalog inventory across **all** skills/powers/tools without relevance filtering; dispatch every item possible, with bounded parallel workers and reviewed adapters. Clearly identify blocked, failed and genuinely executed items. Do not claim literal same-millisecond simultaneous running or successful all-skills activation without evidence. Keep user permissions and free/paid limitations intact.
