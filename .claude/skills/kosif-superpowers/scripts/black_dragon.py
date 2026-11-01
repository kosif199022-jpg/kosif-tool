#!/usr/bin/env python3
"""KOSIF Black Dragon: use EVERY capability of every type and verify what really ran.

Inventory: installed skills, catalogued powers, registered tools, fused
superpowers, motion styles, motion playbooks and USIP protocol rules. Nothing
is filtered out: the brain gives each entry a part of the job, a mode and a
weight, and every entry gets a written brief line with the hash of its source.

Evidence tiers, never mixed up in the report:
  assigned  - in the plan with a part, mode and application (all entries)
  probed    - a read-only tool answered `--help` here (opt-in --probe-tools)
  executed  - a reviewed adapter ran on the task, wrote a nonempty artifact and
              a SHA-256 receipt (opt-in --adapters FILE --execute-adapters)
Bounded parallel dispatch. No shell strings, payments, uploads or installs.
"""
from __future__ import annotations
import argparse
import concurrent.futures as futures
import json
import hashlib
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
import _cinema_all_skills as audit
import _black_dragon_brain as brain
import _black_dragon_pro_max as pro_max

REPO = audit.REPO.resolve()
SCHEMA = "kosif.black-dragon.v2"
MAX_WORKERS = 32
PROBE_TIMEOUT = 30
REVIEWED_ADAPTERS = audit.SKILL / "data" / "black_dragon_adapters.json"


def _file_sha(path: Path, cache: dict) -> str | None:
    if path not in cache:
        cache[path] = audit.sha256(path) if path.is_file() else None
    return cache[path]


def full_inventory(skill: Path | None = None, repo: Path | None = None) -> dict:
    """Every capability of every type. Fails loudly on duplicates or broken sources."""
    skill = skill or audit.SKILL
    repo = repo or REPO
    entries = audit.catalog(skill)

    def add(key: str, meta: dict) -> None:
        if key in entries:
            raise ValueError("Duplicate catalog entry: " + key)
        entries[key] = meta

    sp = json.loads((skill / "data" / "superpowers.json").read_text(encoding="utf-8"))
    for row in sp.get("items", []):
        if not isinstance(row, dict) or not row.get("id"):
            raise ValueError("Superpower missing ID")
        add("superpower:" + row["id"], {"kind": "superpower", "source": "data/superpowers.json"})
    styles = repo / "catalog" / "styles.json"
    if styles.is_file():
        for row in json.loads(styles.read_text(encoding="utf-8")):
            if not isinstance(row, dict) or not row.get("id"):
                raise ValueError("Style missing ID")
            add("style:" + row["id"], {
                "kind": "style", "source": "catalog/styles.json",
                "text": " ".join([str(row.get("name", "")), str(row.get("name_ar", "")),
                                  " ".join(map(str, row.get("category") or [])),
                                  " ".join(map(str, row.get("tech") or [])), "motion style reference"])})
    playbooks = repo / "playbooks"
    for path in sorted(playbooks.glob("*.md")) if playbooks.is_dir() else []:
        add("playbook:" + path.stem, {"kind": "playbook", "source": str(path.relative_to(repo)),
                                      "text": path.stem.replace("-", " ") + " playbook " +
                                      path.read_text(encoding="utf-8")[:400]})
    core = skill / "PROTOCOL.md"
    rules = ([core] if core.is_file() else []) + sorted((skill / "references" / "protocol").glob("A*.md"))
    for path in rules:
        head = path.read_text(encoding="utf-8")[:400]
        add("protocol:" + path.stem, {"kind": "protocol", "source": str(path.relative_to(skill)),
                                      "text": "protocol rule " + head})
    return entries


def _source_path(key: str, meta: dict) -> Path:
    src = Path(str(meta.get("source", "")))
    kind = meta.get("kind")
    if kind == "skill":
        return audit.SKILL.parent / src
    if kind in ("style", "playbook"):
        return REPO / src
    return audit.SKILL / src


def _tool_records() -> dict:
    try:
        rows = json.loads((audit.SKILL / "data" / "tools.json").read_text(encoding="utf-8"))["tools"]
        return {"tool:" + r["id"]: r for r in rows if isinstance(r, dict) and r.get("id")}
    except (OSError, ValueError, KeyError):
        return {}


def _probe(key: str, record: dict | None, job: Path) -> dict:
    """Ask an argparse CLI tool for --help (argparse exits before any action).

    Proves the tool starts on this machine with its imports, nothing more.
    """
    if record is None:
        return {"status": "not-probeable", "reason": "no registry record"}
    if record.get("kind") != "cli":
        return {"status": "not-probeable", "reason": f"kind={record.get('kind')}"}
    base = audit.SKILL if record.get("root") == "skill" else REPO
    target = base / str(record.get("path", ""))
    if target.suffix != ".py" or not target.is_file() or not _inside(target.resolve(), REPO):
        return {"status": "not-probeable", "reason": "not a Python file inside the repository"}
    try:
        if "argparse" not in target.read_text(encoding="utf-8", errors="replace"):
            return {"status": "not-probeable", "reason": "no argparse, --help is not known to be harmless"}
    except OSError as exc:
        return {"status": "not-probeable", "reason": str(exc)[:200]}
    name = re.sub(r"[^a-zA-Z0-9_.-]", "_", key)
    sandbox = job / "probes" / "cwd"
    sandbox.mkdir(parents=True, exist_ok=True)
    command = [sys.executable, str(target), "--help"]
    try:
        done = subprocess.run(command, cwd=sandbox, text=True, capture_output=True,
                              timeout=PROBE_TIMEOUT, check=False, stdin=subprocess.DEVNULL)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"status": "failed", "reason": str(exc)[:200], "command": command}
    out = job / "probes" / f"{name}.txt"
    out.write_text(done.stdout + done.stderr, encoding="utf-8")
    ok = done.returncode == 0 and out.stat().st_size > 0
    return {"status": "passed" if ok else "failed", "exit_code": done.returncode,
            "safety": record.get("safety"),
            "command": command, "output": str(out), "output_sha256": audit.sha256(out)}

def _inside(child: Path, parent: Path) -> bool:
    return child == parent or parent in child.parents

def _load_adapters(path: Path | None) -> dict:
    if path is None:
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, dict) and isinstance(raw.get("adapters"), dict):
        raw = raw["adapters"]  # bundled file format: {"_comment": ..., "adapters": {...}}
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
        allow_execution: bool, timeout: int, entries: dict | None = None,
        probe_tools: bool = False, mode: str = "standard") -> dict:
    if not task.strip():
        raise ValueError("Task is required")
    if not 1 <= workers <= MAX_WORKERS:
        raise ValueError("workers must be between 1 and 32")
    if not 1 <= timeout <= 3600:
        raise ValueError("timeout must be between 1 and 3600 seconds")
    if mode not in ("standard", "pro-max"):
        raise ValueError("mode must be standard or pro-max")
    job = _safe_job(job)
    inventory = full_inventory() if entries is None else entries
    unknown = sorted(set(adapters) - set(inventory))
    if unknown:
        raise ValueError("Unknown adapter entry: " + unknown[0])
    strategy = brain.plan(task, inventory, adapters, skill_root=audit.SKILL if entries is None else None)
    pro_max_packet = pro_max.preflight(task, strategy, inventory) if mode == "pro-max" else None
    audit.init(job, inventory)
    if pro_max_packet is not None:
        (job / "black_dragon_pro_max_plan.json").write_text(
            json.dumps(pro_max_packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (job / "black_dragon_plan.json").write_text(json.dumps(strategy, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (job / "artifacts").mkdir()
    (job / "receipts").mkdir()
    # Every entry gets one brief line: its part, mode, weight, application and source hash.
    hashes, briefs = {}, {}
    with (job / "briefs.jsonl").open("w", encoding="utf-8") as fh:
        for key in sorted(inventory):
            meta, item = inventory[key], strategy["items"][key]
            line = json.dumps({"entry": key, "kind": meta.get("kind"), "part": item["part"],
                               "mode": item["mode"], "weight": item["weight"],
                               "application": item["application"],
                               "source": meta.get("source"),
                               "source_sha256": _file_sha(_source_path(key, meta), hashes)},
                              ensure_ascii=False, sort_keys=True)
            fh.write(line + "\n")
            briefs[key] = hashlib.sha256(line.encode("utf-8")).hexdigest()
    probes = {}
    if probe_tools:
        records = _tool_records()
        tools = [k for k in sorted(inventory) if inventory[k].get("kind") == "tool"]
        with futures.ThreadPoolExecutor(max_workers=workers) as pool:
            jobs = {pool.submit(_probe, k, records.get(k), job): k for k in tools}
            for future in futures.as_completed(jobs):
                probes[jobs[future]] = future.result()
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
        plan_item = strategy["items"][key]
        item["assignment"] = {"part": plan_item["part"], "mode": plan_item["mode"],
                              "weight": plan_item["weight"], "brief_sha256": briefs[key]}
        if key in probes:
            item["probe"] = probes[key]
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
    probe_counts = Counter(p["status"] for p in probes.values())
    briefs_file = job / "briefs.jsonl"
    report = {"schema": SCHEMA, "task": task, "scheduled": len(inventory),
              "by_kind": dict(sorted(Counter(v.get("kind", "?") for v in inventory.values()).items())),
              "assigned": len(briefs), "assignment_complete": set(briefs) == set(inventory),
              "assignment_sha256": strategy["assignment_sha256"],
              "briefs_file": str(briefs_file), "briefs_sha256": audit.sha256(briefs_file),
              "parts": {k: {"assigned": v["assigned"], "leads": v["leads"]} for k, v in strategy["parts"].items()},
              "modes": strategy["modes"], "weights": strategy["weights"],
              "probed": len(probes), "probe_passed": probe_counts["passed"],
              "probe_failed": probe_counts["failed"], "probe_not_probeable": probe_counts["not-probeable"],
              "workers": workers, "adapter_count": len(adapters),
              "roles": strategy["roles"], "waves": len(strategy["waves"]),
              "brain_plan_file": str(job / "black_dragon_plan.json"),
              "selected_out": strategy["selected_out"],
              "executed": counts["executed"], "blocked": counts["blocked"],
              "failed": counts["failed"], "full_coverage": coverage["fully_executed"],
              "coverage_file": str(job / "all_skills_report.json"),
              "truth": ("Every entry is assigned a part and mode with a brief line; 'probed' only means "
                        "a tool answered --help here; only receipt-verified adapter work is 'executed'")}
    report["mode"] = mode
    if pro_max_packet is not None:
        qa = pro_max.verify(job, inventory, report)
        report["pro_max"] = {"integrity_passed": qa["integrity_passed"],
                             "every_capability_executed": qa["every_capability_executed"],
                             "external_full_pro_verified": False,
                             "qa_file": str(job / "black_dragon_pro_max_qa.json")}
        if not qa["integrity_passed"]:
            raise ValueError("Pro Max evidence QA failed; see black_dragon_pro_max_qa.json")
    (job / "black_dragon_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (job / "black_dragon_report.md").write_text(_markdown(report, strategy, ledger), encoding="utf-8")
    return report


def _markdown(report: dict, strategy: dict, ledger: dict) -> str:
    """Short Arabic/English summary for the owner; the JSON files stay the evidence."""
    lines = [f"# التنين الأسود / Black Dragon — {report['task']}", "",
             f"- كل القدرات / all entries: **{report['scheduled']:,}** "
             f"({', '.join(f'{k} {v:,}' for k, v in report['by_kind'].items())})",
             f"- اتعيّن لها جزء وطريقة / assigned a part and mode: **{report['assigned']:,}** "
             f"(complete: {report['assignment_complete']})",
             f"- أدوات اشتغلت `--help` هنا / tools that start here: **{report['probe_passed']}** "
             f"of {report['probed']} probed",
             f"- اتنفذت فعلًا بإيصال / executed with receipt: **{report['executed']}** · "
             f"blocked {report['blocked']:,} · failed {report['failed']}",
             f"- full coverage (every entry executed): **{report['full_coverage']}**", "",
             "| الجزء / part | assigned | leads |", "|---|---:|---|"]
    for pid, part in strategy["parts"].items():
        leads = ", ".join(f"`{k}`" for k in part["leads"]) or "—"
        lines.append(f"| {part['ar']} / {part['en']} | {part['assigned']:,} | {leads} |")
    lines += ["", "| الطريقة / mode | entries |", "|---|---:|"]
    lines += [f"| {m} | {n:,} |" for m, n in report["modes"].items()]
    executed = [k for k, v in ledger["items"].items() if v["status"] == "executed"]
    if executed:
        lines += ["", "## اتنفذ بإيصال / executed with receipt", ""]
        for key in sorted(executed):
            r = ledger["items"][key]["receipt"]
            lines.append(f"- `{key}` → `{Path(r['artifact']).name}` sha256 `{r['artifact_sha256'][:16]}…`")
    lines += ["", "_" + report["truth"] + "_", ""]
    return "\n".join(lines)

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("inventory", help="Count every skill, power and tool")
    p = sub.add_parser("run", help="Fan out attempts to every catalog entry")
    p.add_argument("task")
    p.add_argument("--job", required=True, type=Path)
    p.add_argument("--adapters", type=Path)
    p.add_argument("--reviewed-adapters", action="store_true",
                   help="use the bundled reviewed adapters (data/black_dragon_adapters.json)")
    p.add_argument("--execute-adapters", action="store_true")
    p.add_argument("--mode", choices=("standard", "pro-max"), default="standard")
    p.add_argument("--workers", type=int, default=8)
    p.add_argument("--timeout", type=int, default=60)
    p.add_argument("--probe-tools", action="store_true",
                   help="run --help on every argparse CLI tool as a startup probe")
    q = sub.add_parser("plan", help="Plan every catalog entry without execution")
    q.add_argument("task")
    q.add_argument("--adapters", type=Path)
    q.add_argument("--mode", choices=("standard", "pro-max"), default="standard")
    args = parser.parse_args(argv)
    try:
        if args.command == "inventory":
            entries = full_inventory()
            print(json.dumps({"total": len(entries),
                              "by_kind": Counter(v["kind"] for v in entries.values())},
                             ensure_ascii=False, indent=2))
            return 0
        if args.command == "plan":
            inventory = full_inventory()
            adapters = _load_adapters(args.adapters)
            if set(adapters) - set(inventory):
                raise ValueError("Unknown adapter entry")
            strategy = brain.plan(args.task, inventory, adapters, skill_root=audit.SKILL)
            summary = {k: v for k, v in strategy.items() if k != "items"}
            if args.mode == "pro-max":
                summary["pro_max"] = pro_max.preflight(args.task, strategy, inventory)
            print(json.dumps(summary, ensure_ascii=False, indent=2))
            return 0
        if args.adapters and args.reviewed_adapters:
            raise ValueError("Use either --adapters or --reviewed-adapters")
        report = run(args.task, args.job,
                     _load_adapters(REVIEWED_ADAPTERS if args.reviewed_adapters else args.adapters),
                     args.workers, args.execute_adapters, args.timeout,
                     probe_tools=args.probe_tools, mode=args.mode)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["full_coverage"] else 4
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print("black-dragon: " + str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
