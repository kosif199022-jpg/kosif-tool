#!/usr/bin/env python3
"""Black Dragon evidence guard v1.4: independent proof audit and critical path.

The guard reopens on-disk execution evidence and does not execute code.
It does not provide signed attestation or an OS sandbox.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import _cinema_all_skills as audit

SCHEMA = "kosif.black-dragon.evidence-guard.v1"


def execution_map(strategy: dict) -> dict:
    """Deterministic dependency longest path and runtime readiness, not LLM reasoning."""
    items = strategy["items"]
    waves = strategy["waves"]
    depth: dict[str, int] = {}
    predecessor: dict[str, str | None] = {}
    counted = set()
    width = 0
    for wave in waves:
        width = max(width, len(wave))
        for key in wave:
            if key in counted or key not in items:
                raise ValueError("Repeated or unknown entry in dependency wave: " + key)
            dependencies = items[key].get("depends_on", [])
            if not isinstance(dependencies, list):
                raise ValueError("Malformed dependency list")
            if any(d not in depth for d in dependencies):
                raise ValueError("Dependency wave is not topologically ordered")
            prior = max(dependencies, key=lambda d: (depth[d], d)) if dependencies else None
            depth[key] = (depth[prior] + 1) if prior else 1
            predecessor[key] = prior
            counted.add(key)
    if counted != set(items):
        raise ValueError("Dependency waves omitted registered entries")
    last = max(depth, key=lambda key: (depth[key], key)) if depth else None
    chain = []
    while last is not None:
        chain.append(last)
        last = predecessor[last]
    chain.reverse()
    ready = sum(1 for x in items.values() if x.get("adapter_ready") is True)
    return {"schema": SCHEMA + ".critical-path", "catalog_assigned": len(items),
            "execution_adapter_ready": ready,
            "documentation_or_unreviewed": len(items) - ready,
            "dependency_waves": len(waves),
            "max_parallel_wave_width": width,
            "critical_path_length": len(chain),
            "critical_path": chain,
            "truth": "Critical path is an unweighted dependency depth, NOT estimated wall-clock execution time"}


def _secure_file(value: object, root: Path) -> Path:
    """Reject symlinks or paths outside the selected immutable job subfolder."""
    if not isinstance(value, str) or not value:
        raise ValueError("Missing evidence path")
    path = Path(value)
    if not path.is_absolute() or path.is_symlink():
        raise ValueError("Evidence must be a regular absolute non-symlink path")
    resolved = path.resolve()
    if not resolved.is_relative_to(root.resolve()) or not resolved.is_file():
        raise ValueError("Evidence outside the job or not a file")
    # Also detect a symlinked intermediate path inside the job.
    for candidate in (path, *path.parents):
        if candidate == root.parent:
            break
        if candidate.is_symlink():
            raise ValueError("Symlink traversal in evidence path")
    return resolved


def examine_receipt(job: Path, key: str, item: dict, seen_artifacts: set[str]) -> list[str]:
    """Cross-check ledger summary, receipt bytes and artifact bytes independently."""
    issues = []
    receipt = item.get("receipt")
    if not isinstance(receipt, dict):
        return ["missing execution receipt"]
    try:
        source = _secure_file(receipt.get("receipt_path"), job / "receipts")
        if audit.sha256(source) != receipt.get("receipt_sha256"):
            issues.append("receipt SHA-256 mismatch")
        proof = json.loads(source.read_text(encoding="utf-8"))
        if not isinstance(proof, dict):
            return issues + ["invalid receipt JSON object"]
        artifact = _secure_file(proof.get("artifact"), job / "artifacts")
        if (proof.get("entry") != key or type(proof.get("exit_code")) is not int
                or proof["exit_code"] != 0):
            issues.append("receipt entry or exit code mismatch")
        if proof.get("artifact_sha256") != receipt.get("artifact_sha256"):
            issues.append("ledger and receipt artifact hashes differ")
        if not artifact.stat().st_size or audit.sha256(artifact) != proof.get("artifact_sha256"):
            issues.append("artifact SHA-256 mismatch or empty artifact")
        if str(artifact) != str(Path(receipt.get("artifact", "")).resolve()):
            issues.append("ledger artifact path differs from receipt")
        command = proof.get("command")
        if (not isinstance(command, list) or not command or
                not all(isinstance(c, str) and c for c in command) or
                command != receipt.get("command")):
            issues.append("ledger and receipt command differ")
        if str(artifact) in seen_artifacts:
            issues.append("artifact shared by multiple executed entries")
        seen_artifacts.add(str(artifact))
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        issues.append("invalid receipt or external artifact: " + str(exc)[:130])
    return issues


def verify_briefs(job: Path, entries: dict) -> tuple[dict[str, str], list[str]]:
    """Check each assignment source hash as recorded; unavailable sources stay unknown."""
    path = job / "briefs.jsonl"
    issues = []
    lines = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            issues.append("blank assignment brief")
            continue
        obj = json.loads(raw)
        if not isinstance(obj, dict) or not isinstance(obj.get("entry"), str):
            issues.append("malformed assignment brief")
        else:
            lines.append(obj)
    ids = [x["entry"] for x in lines]
    if len(ids) != len(entries) or set(ids) != set(entries):
        issues.append("missing, duplicate or extra assignments")
    fingerprints = {}
    for row in lines:
        key = row["entry"]
        if key not in entries:
            continue
        if row.get("kind") != entries[key].get("kind") or row.get("source") != entries[key].get("source"):
            issues.append(key + ": assignment/source metadata mismatch")
        canonical = json.dumps(row, ensure_ascii=False, sort_keys=True)
        fingerprints[key] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return fingerprints, issues


def verify_ledger(job: Path, entries: dict, ledger: dict, report: dict) -> dict:
    if not job.is_dir() or job.is_symlink():
        raise ValueError("Unknown or symlinked Black Dragon job")
    briefs, issues = verify_briefs(job, entries)
    counts = {"executed": 0, "blocked": 0, "failed": 0}
    seen_artifacts: set[str] = set()
    for key in sorted(entries):
        item = ledger["items"][key]
        if not isinstance(item, dict):
            issues.append(key + ": invalid ledger entry")
            continue
        status = item.get("status")
        if status not in counts:
            issues.append(key + ": unsupported status")
            continue
        counts[status] += 1
        assignment = item.get("assignment")
        if not isinstance(assignment, dict) or assignment.get("brief_sha256") != briefs.get(key):
            issues.append(key + ": missing or mismatched assignment digest")
        if item.get("attempts") != 1:
            issues.append(key + ": invalid execution attempts")
        if status == "executed":
            issues.extend(key + ": " + issue for issue in examine_receipt(job, key, item, seen_artifacts))
        elif not str(item.get("reason", "")).strip():
            issues.append(key + ": blocked/failed without reason")
    for status, count in counts.items():
        if report.get(status) != count:
            issues.append(status + ": report count differs from independent ledger")
    if report.get("scheduled") != len(entries) or report.get("assigned") != len(entries):
        issues.append("scheduled or assigned count mismatch")
    expected_all = len(entries) > 0 and counts["executed"] == len(entries) and not issues
    if bool(report.get("full_coverage")) != expected_all:
        issues.append("full coverage claim is inconsistent with receipts")
    return {"schema": SCHEMA + ".audit",
            "catalog_total": len(entries),
            "assigned": len(briefs),
            "verified_executed": counts["executed"],
            "blocked": counts["blocked"], "failed": counts["failed"],
            "integrity_passed": not issues,
            "every_capability_executed": expected_all and not issues,
            "issues": issues[:100],
            "evidence_truth": "Untrusted JSON receipts are self-reported, locally hash-checked; no external attestation",
            "ledger_sha256": audit.sha256(job / "all_skills_ledger.json"),
            "briefs_sha256": audit.sha256(job / "briefs.jsonl")}
