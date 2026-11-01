#!/usr/bin/env python3
"""Black Dragon Pro Max: exhaustive reasoning frames and independent evidence QA.

This is a deterministic orchestration/verification layer, not a larger model,
an external KOSIF Think run, or a claim that all skills executed successfully.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

import _cinema_all_skills as audit

SCHEMA = "kosif.black-dragon.pro-max.v1"


def preflight(task: str, strategy: dict, entries: dict) -> dict:
    """Provide alternative architectures, challenge checks and acceptance gates."""
    if not task.strip() or not entries:
        raise ValueError("Pro Max requires task and catalog")
    if strategy["selected_out"] or strategy["scheduled"] != len(entries):
        raise ValueError("Pro Max cannot omit a registered capability")
    return {
        "schema": SCHEMA,
        "mode": "pro-max",
        "task": task,
        "catalog_fingerprint": audit.fingerprint(entries),
        "assigned": len(entries),
        "architectures": {
            "A": "Use reviewed native adapters for the critical path; minimize work and risk",
            "B": "Distribute every catalog entry across the seven-part brain plan with receipts",
            "C": "Independently challenge plan B with failure cases and artifact verification",
        },
        "reasoning_lenses": [
            {"name": "first-principles", "question": "Which outputs actually prove the requested outcome?"},
            {"name": "contrarian", "question": "What would make the preferred plan wrong?"},
            {"name": "counterfactual", "question": "Would the smallest valid baseline achieve the same result?"},
            {"name": "dependencies", "question": "Which prerequisites must finish before dependent work?"},
            {"name": "risk-and-permissions", "question": "What requires the owner's separate approval?"},
            {"name": "independent-qa", "question": "Do the artifacts and SHA-256 receipts support every claim?"},
        ],
        "required_gates": [
            "catalog: no registered item removed",
            "assignments: one part/mode/brief per item",
            "dependencies: acyclic execution waves",
            "execution: reviewed adapters and permission gate",
            "evidence: nonempty output with matching SHA-256 receipt",
            "integrity: report counters and ledger agree",
            "truth: unavailable skills remain blocked; never imply external Full Pro runtime",
        ],
        "external_full_pro": "not-invoked",
        "limits": "Heuristic planning, not actual multiple LLM reviewers or unrestricted execution",
    }


def verify(job: Path, entries: dict, report: dict) -> dict:
    """Re-open on-disk evidence without trusting summary flags."""
    ledger = audit.load(job, entries)
    path = job / "briefs.jsonl"
    lines = [json.loads(s) for s in path.read_text(encoding="utf-8").splitlines()]
    ids = [line["entry"] for line in lines]
    if len(ids) != len(entries) or set(ids) != set(entries):
        raise ValueError("Missing, duplicate or extra Pro Max assignment briefs")
    briefs = {x["entry"]: hashlib.sha256(
        json.dumps(x, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
              for x in lines}
    counts = Counter()
    issues = []
    for key, item in ledger["items"].items():
        status = item.get("status")
        counts[status] += 1
        assignment = item.get("assignment", {})
        if assignment.get("brief_sha256") != briefs[key]:
            issues.append(key + ": missing or mismatched assignment")
        if status == "executed":
            receipt = item.get("receipt")
            if not isinstance(receipt, dict):
                issues.append(key + ": no execution receipt")
            else:
                artifact = Path(receipt.get("artifact", ""))
                if (not artifact.is_file() or artifact.stat().st_size == 0 or
                        audit.sha256(artifact) != receipt.get("artifact_sha256")):
                    issues.append(key + ": artifact/digest mismatch")
        elif status not in ("blocked", "failed"):
            issues.append(key + ": unsupported execution status")
    if (report["executed"] != counts["executed"] or
            report["blocked"] != counts["blocked"] or
            report["failed"] != counts["failed"] or
            report["scheduled"] != len(entries)):
        issues.append("Reported status counts differ from ledger")
    complete = (not issues and counts["executed"] == len(entries))
    if bool(report["full_coverage"]) != complete:
        issues.append("Full coverage claim is inconsistent with verified receipts")
    result = {"schema": SCHEMA, "mode": "pro-max",
              "catalog_total": len(entries), "assigned": len(lines),
              "verified_executed": counts["executed"],
              "blocked": counts["blocked"], "failed": counts["failed"],
              "integrity_passed": not issues,
              "every_capability_executed": complete and not issues,
              "external_full_pro_verified": False,
              "issues": issues[:100],
              "assignment_sha256": audit.sha256(path),
              "ledger_sha256": audit.sha256(job / "all_skills_ledger.json")}
    (job / "black_dragon_pro_max_qa.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result
