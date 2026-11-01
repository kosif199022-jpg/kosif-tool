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
import _black_dragon_evidence_guard as guard

SCHEMA = "kosif.black-dragon.pro-max.v2"


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
        "execution_map": guard.execution_map(strategy),
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
    """Reopen the job from disk and audit source assignments, receipts and artifacts.

    Hash receipts and actual artifacts rather than trusting the report. Failing
    verification writes an honest QA file and never silently upgrades coverage.
    """
    ledger = audit.load(job, entries)
    result = guard.verify_ledger(job, entries, ledger, report)
    result.update({
        "schema": SCHEMA,
        "mode": "pro-max",
        "external_full_pro_verified": False,
        "assignment_sha256": result["briefs_sha256"],
    })
    (job / "black_dragon_pro_max_qa.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def review_job(job: Path, entries: dict) -> dict:
    """Independently verify a completed run; no adapter or probe is executed."""
    path = job / "black_dragon_report.json"
    if path.is_symlink() or not path.is_file():
        raise ValueError("Job has no valid final report")
    report = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(report, dict) or report.get("mode") != "pro-max":
        raise ValueError("Only completed Pro Max jobs have the required QA contract")
    if not (job / "black_dragon_plan.json").is_file():
        raise ValueError("Missing Black Dragon plan")
    qa = verify(job, entries, report)
    return {"job": str(job.resolve()), "audit": qa,
            "truth": "Local receipt integrity verification only; no scripts executed or external sign-off"}
