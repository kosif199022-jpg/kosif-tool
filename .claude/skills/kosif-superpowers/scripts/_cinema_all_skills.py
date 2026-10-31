#!/usr/bin/env python3
"""Strict, evidence-led full-catalog coverage gate for KOSIF Cinema Pro.

This gate cannot turn documentation-only powers into executable programs.
It enumerates every SKILL.md, native power and registered tool. An execution
is credited only with an individual receipt and a real, nonempty artifact.
Missing, blocked, failed or unevidenced items prevent full-coverage success.
No arbitrary tools, network calls, installations or paid APIs run here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
REPO = SKILL.parents[2]
SCHEMA = "kosif.cinema.all-skills.v1"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def catalog(skill: Path = SKILL) -> dict:
    """No silent omissions: fail on unknown power format, missing ids or duplicates."""
    entries = {}
    for path in sorted(skill.parent.rglob("SKILL.md")):
        key = "skill:" + str(path.parent.relative_to(skill.parent))
        entries[key] = {"kind": "skill", "source": str(path.relative_to(skill.parent))}
    power_files = sorted((skill / "data" / "powers").glob("*.json"))
    if not power_files:
        raise ValueError("No power catalogs found")
    for path in power_files:
        obj = json.loads(path.read_text(encoding="utf-8"))
        rows = obj if isinstance(obj, list) else obj.get("powers") if isinstance(obj, dict) else None
        if not isinstance(rows, list):
            raise ValueError("Unrecognized catalog: " + str(path))
        for row in rows:
            if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not row["id"]:
                raise ValueError("Power missing ID: " + str(path))
            key = "power:" + row["id"]
            if key in entries:
                raise ValueError("Duplicate catalog entry: " + key)
            entries[key] = {"kind": "power", "source": str(path.relative_to(skill))}
    path = skill / "data" / "tools.json"
    obj = json.loads(path.read_text(encoding="utf-8"))
    tools = obj.get("tools")
    if not isinstance(tools, list):
        raise ValueError("Missing native tools")
    for row in tools:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not row["id"]:
            raise ValueError("Tool missing ID")
        key = "tool:" + row["id"]
        if key in entries:
            raise ValueError("Duplicate tool: " + key)
        entries[key] = {"kind": "tool", "source": str(path.relative_to(skill))}
    if not entries or not any(k.startswith("skill:") for k in entries):
        raise ValueError("No SKILL.md entries found")
    return dict(sorted(entries.items()))


def fingerprint(entries: dict) -> str:
    return hashlib.sha256(json.dumps(entries, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def init(job: Path, entries: dict) -> dict:
    job.mkdir(parents=True, exist_ok=True)
    ledger_path = job / "all_skills_ledger.json"
    if ledger_path.exists():
        raise ValueError("Ledger already exists; use report, not an overwrite")
    ledger = {
        "schema": SCHEMA,
        "catalog_fingerprint": fingerprint(entries),
        "coverage_required": len(entries),
        "items": {key: {**meta, "status": "not-executed", "attempts": 0, "receipt": None}
                  for key, meta in entries.items()},
    }
    ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return ledger


def load(job: Path, entries: dict) -> dict:
    ledger = json.loads((job / "all_skills_ledger.json").read_text(encoding="utf-8"))
    if ledger.get("schema") != SCHEMA or ledger.get("catalog_fingerprint") != fingerprint(entries):
        raise ValueError("Catalog changed or ledger invalid; start a fresh audited session")
    if set(ledger.get("items", {})) != set(entries):
        raise ValueError("Ledger does not cover every catalog item")
    return ledger


def save(job: Path, ledger: dict) -> None:
    (job / "all_skills_ledger.json").write_text(
        json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def evidence(receipt_path: Path, key: str) -> dict:
    """Accept a task-specific external execution receipt, never a bare success flag."""
    obj = json.loads(receipt_path.read_text(encoding="utf-8"))
    if obj.get("entry") != key or obj.get("exit_code") != 0:
        raise ValueError("Receipt entry/exit_code mismatch")
    if not isinstance(obj.get("command"), list) or not obj["command"] or not all(
            isinstance(p, str) and p for p in obj["command"]):
        raise ValueError("Receipt must name the command actually run")
    artifact = Path(obj.get("artifact", ""))
    if not artifact.is_file() or artifact.stat().st_size == 0:
        raise ValueError("Receipt needs an existing nonempty artifact")
    digest = sha256(artifact)
    if obj.get("artifact_sha256") != digest:
        raise ValueError("Artifact SHA-256 mismatch")
    return {"receipt_path": str(receipt_path.resolve()), "receipt_sha256": sha256(receipt_path),
            "artifact": str(artifact.resolve()), "artifact_sha256": digest,
            "command": obj["command"]}


def record(job: Path, entries: dict, key: str, state: str, receipt: Path | None, reason: str) -> dict:
    ledger = load(job, entries)
    if key not in ledger["items"]:
        raise ValueError("Unknown inventory entry: " + key)
    item = ledger["items"][key]
    if item["attempts"]:
        raise ValueError("Once-only execution: this entry already has a recorded attempt")
    if state == "executed":
        if receipt is None:
            raise ValueError("Executed state requires a real execution receipt")
        item["receipt"] = evidence(receipt, key)
    elif state in ("blocked", "failed"):
        if not reason.strip():
            raise ValueError("Blocked/failed entry requires an explanation")
        item["reason"] = reason
    else:
        raise ValueError("Invalid state")
    item["status"] = state
    item["attempts"] = 1
    save(job, ledger)
    return item


def report(job: Path, entries: dict) -> dict:
    ledger = load(job, entries)
    counts = Counter(row["status"] for row in ledger["items"].values())
    duplicated = [key for key, row in ledger["items"].items() if row["attempts"] > 1]
    missing = [key for key, row in ledger["items"].items() if row["status"] != "executed"]
    invalid = []
    for key, row in ledger["items"].items():
        if row["status"] == "executed":
            proof = row.get("receipt") or {}
            artifact = Path(proof.get("artifact", ""))
            source = Path(proof.get("receipt_path", ""))
            if not artifact.is_file() or not source.is_file() or not (
                    artifact.stat().st_size and sha256(artifact) == proof.get("artifact_sha256")
                    and sha256(source) == proof.get("receipt_sha256")):
                invalid.append(key)
    complete = not missing and not duplicated and not invalid and len(entries) > 0
    result = {"schema": SCHEMA + ".report", "total": len(entries),
              "executed": counts["executed"], "blocked": counts["blocked"],
              "failed": counts["failed"], "not_executed": counts["not-executed"],
              "duplicate_attempts": duplicated, "invalid_evidence": invalid,
              "uncovered_first_30": missing[:30], "fully_executed": complete,
              "truth": ("All catalog entries individually receipted" if complete else
                        "NOT FULLY EXECUTED; listing/probing a skill does not count")}
    (job / "all_skills_report.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    for cmd in ("init", "report", "record"):
        s = sub.add_parser(cmd)
        s.add_argument("--job", required=True, type=Path)
        if cmd == "record":
            s.add_argument("--entry", required=True)
            s.add_argument("--state", choices=("executed", "blocked", "failed"), required=True)
            s.add_argument("--receipt", type=Path)
            s.add_argument("--reason", default="")
    args = parser.parse_args(argv)
    try:
        entries = catalog()
        if args.cmd == "init":
            ledger = init(args.job, entries)
            result = {"catalog_entries": ledger["coverage_required"], "status": "not-executed"}
        elif args.cmd == "record":
            result = record(args.job, entries, args.entry, args.state, args.receipt, args.reason)
        else:
            result = report(args.job, entries)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 4 if args.cmd == "report" and not result["fully_executed"] else 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print("cinema-all-skills: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
