#!/usr/bin/env python3
"""KOSIF Black Dragon: fan out EVERY catalog entry and verify actual execution.

No relevant-skill filtering. Bounded parallel dispatch, evidence-based receipts.
No shell commands, automatic payments, uploads or installations.
"""
from __future__ import annotations
import argparse
import concurrent.futures as futures
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
import _cinema_all_skills as audit
import _black_dragon_brain as brain

REPO = audit.REPO.resolve()
SCHEMA = "kosif.black-dragon.v1"
MAX_WORKERS = 32

def _inside(child: Path, parent: Path) -> bool:
    return child == parent or parent in child.parents

def _load_adapters(path: Path | None) -> dict:
    if path is None:
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("Adapters must be a JSON object keyed by catalog ID")
    for key, spec in raw.items():
        if not isinstance(key, str) or not isinstance(spec, dict):
            raise ValueError("Invalid adapter entry")
        if not isinstance(spec.get("script"), str) or not isinstance(spec.get("args", []), list):
            raise ValueError("Each adapter needs a script path and args list")
        if not all(isinstance(arg, str) for arg in spec["args"]):
            raise ValueError("Adapter args must be strings")
    return raw

def _safe_script(path: str) -> Path:
    rel = Path(path)
    if rel.is_absolute() or ".." in rel.parts or rel.suffix != ".py":
        raise ValueError("Adapter script must be a repo-relative .py path")
    absolute = (REPO / rel).resolve()
    if not _inside(absolute, REPO) or not absolute.is_file():
        raise ValueError("Adapter script not found inside repository")
    if any(p.is_symlink() for p in (REPO / rel, *(REPO / rel).parents)):
        raise ValueError("Adapter scripts may not traverse symlinks")
    return absolute

def _safe_job(job: Path) -> Path:
    result = job.resolve()
    if result == REPO or _inside(REPO, result):
        raise ValueError("Job folder cannot be repository root or ancestor")
    if _inside(result, REPO) and not _inside(result, REPO / "out"):
        raise ValueError("In-repository jobs must live under out/")
    if any(p.is_symlink() for p in (job, *job.parents)):
        raise ValueError("Symlinked job folders are forbidden")
    if (result / "all_skills_ledger.json").exists():
        raise ValueError("Job already has an immutable inventory; use a new folder")
    return result

def _attempt(key: str, spec: dict | None, task: str, job: Path,
             approved: bool, timeout: int) -> dict:
    if spec is None:
        return {"status": "blocked", "reason": "No executable adapter registered"}
    if not approved:
        return {"status": "blocked", "reason": "Adapter execution not enabled"}
    try:
        script = _safe_script(spec["script"])
        from hashlib import sha256
        basename = re.sub(r"[^a-zA-Z0-9_.-]", "_", key)[:90] + "-" + sha256(key.encode()).hexdigest()[:10]
        artifact = job / "artifacts" / f"{basename}.txt"
        receipt = job / "receipts" / f"{basename}.json"
        args = [a.replace("{task}", task).replace("{artifact}", str(artifact))
                for a in spec.get("args", [])]
        command = [sys.executable, str(script), *args]
        completed = subprocess.run(command, cwd=REPO, text=True, capture_output=True,
                                   timeout=timeout, check=False, stdin=subprocess.DEVNULL)
        if completed.returncode or not artifact.is_file() or artifact.stat().st_size == 0:
            return {"status": "failed", "reason":
                    f"Adapter exit={completed.returncode}; missing output or error: {completed.stderr[-220:]}"}
        proof = {"entry": key, "exit_code": completed.returncode,
                 "command": command, "artifact": str(artifact),
                 "artifact_sha256": audit.sha256(artifact)}
        receipt.write_text(json.dumps(proof, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return {"status": "executed", "receipt": receipt}
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        return {"status": "failed", "reason": str(exc)[:350]}

def run(task: str, job: Path, adapters: dict, workers: int,
        allow_execution: bool, timeout: int, entries: dict | None = None) -> dict:
    if not task.strip():
        raise ValueError("Task is required")
    if not 1 <= workers <= MAX_WORKERS:
        raise ValueError("workers must be between 1 and 32")
    if not 1 <= timeout <= 3600:
        raise ValueError("timeout must be between 1 and 3600 seconds")
    job = _safe_job(job)
    inventory = audit.catalog() if entries is None else entries
    unknown = sorted(set(adapters) - set(inventory))
    if unknown:
        raise ValueError("Unknown adapter entry: " + unknown[0])
    strategy = brain.plan(task, inventory, adapters, skill_root=audit.SKILL if entries is None else None)
    audit.init(job, inventory)
    (job / "black_dragon_plan.json").write_text(json.dumps(strategy, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (job / "artifacts").mkdir()
    (job / "receipts").mkdir()
    outcomes = {}
    with futures.ThreadPoolExecutor(max_workers=workers) as pool:
        for wave in strategy["waves"]:
            running = {}
            for key in wave:
                predecessors = strategy["items"][key]["depends_on"]
                skipped = [d for d in predecessors if outcomes[d]["status"] != "executed"]
                if skipped:
                    outcomes[key] = {"status": "blocked",
                                     "reason": "Prerequisites not executed: " + ", ".join(skipped)}
                else:
                    running[pool.submit(_attempt, key, adapters.get(key),
                                        task, job, allow_execution, timeout)] = key
            for future in futures.as_completed(running):
                key = running[future]
                try:
                    outcomes[key] = future.result()
                except Exception as exc:
                    outcomes[key] = {"status": "failed", "reason": str(exc)[:350]}
    if set(outcomes) != set(inventory):
        raise ValueError("Black Dragon did not account for every catalog entry")
    ledger = audit.load(job, inventory)
    for key in inventory:
        item = ledger["items"][key]
        result = outcomes[key]
        item["attempts"] = 1
        item["status"] = result["status"]
        if result["status"] == "executed":
            try:
                item["receipt"] = audit.evidence(result["receipt"], key)
            except (OSError, ValueError) as exc:
                item["status"] = "failed"
                item["reason"] = "Evidence check failed: " + str(exc)
        else:
            item["reason"] = result["reason"]
    audit.save(job, ledger)
    coverage = audit.report(job, inventory)
    counts = Counter(x["status"] for x in ledger["items"].values())
    report = {"schema": SCHEMA, "task": task, "scheduled": len(inventory),
              "workers": workers, "adapter_count": len(adapters),
              "roles": strategy["roles"], "waves": len(strategy["waves"]),
              "brain_plan_file": str(job / "black_dragon_plan.json"),
              "selected_out": strategy["selected_out"],
              "executed": counts["executed"], "blocked": counts["blocked"],
              "failed": counts["failed"], "full_coverage": coverage["fully_executed"],
              "coverage_file": str(job / "all_skills_report.json"),
              "truth": "All entries dispatched; only receipt-verified work is executed"}
    (job / "black_dragon_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("inventory", help="Count every skill, power and tool")
    p = sub.add_parser("run", help="Fan out attempts to every catalog entry")
    p.add_argument("task")
    p.add_argument("--job", required=True, type=Path)
    p.add_argument("--adapters", type=Path)
    p.add_argument("--execute-adapters", action="store_true")
    p.add_argument("--workers", type=int, default=8)
    p.add_argument("--timeout", type=int, default=60)
    q = sub.add_parser("plan", help="Plan every catalog entry without execution")
    q.add_argument("task")
    q.add_argument("--adapters", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "inventory":
            entries = audit.catalog()
            print(json.dumps({"total": len(entries),
                              "by_kind": Counter(v["kind"] for v in entries.values())},
                             ensure_ascii=False, indent=2))
            return 0
        if args.command == "plan":
            inventory = audit.catalog()
            adapters = _load_adapters(args.adapters)
            if set(adapters) - set(inventory):
                raise ValueError("Unknown adapter entry")
            strategy = brain.plan(args.task, inventory, adapters, skill_root=audit.SKILL)
            print(json.dumps({k: v for k, v in strategy.items() if k != "items"},
                             ensure_ascii=False, indent=2))
            return 0
        report = run(args.task, args.job, _load_adapters(args.adapters),
                     args.workers, args.execute_adapters, args.timeout)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["full_coverage"] else 4
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print("black-dragon: " + str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
