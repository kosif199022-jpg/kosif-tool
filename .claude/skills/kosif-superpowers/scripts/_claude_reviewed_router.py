#!/usr/bin/env python3
"""KOSIF reviewed-tool router: focused, receipt-verified execution for Claude.

This complements exhaustive Black Dragon. A subset is NEVER full-catalog coverage.
Only IDs present in the bundled reviewed-adapter registry may execute. No shell,
network server, auto-installation, deployment or blanket model permissions.
"""
from __future__ import annotations

import concurrent.futures
import hashlib
import hmac
import json
import os
import re
from collections import Counter
from pathlib import Path

import black_dragon as dragon
import _black_dragon_brain as brain

REPO = dragon.REPO
SCHEMA = "kosif.reviewed-tools.v1"
MAX_SELECTED = 8
MAX_WORKERS = 4
MAX_TIMEOUT = 120


def _registry() -> dict:
    raw = dragon._load_adapters(dragon.REVIEWED_ADAPTERS)
    if not raw or any(not k.startswith("tool:") for k in raw):
        raise ValueError("Reviewed adapter registry empty or invalid")
    return raw


def _inventory() -> dict:
    return dragon.full_inventory()


def _records() -> dict:
    return dragon._tool_records()


def _check_task(task: str) -> str:
    if not isinstance(task, str) or not task.strip() or len(task) > 2000:
        raise ValueError("task must be nonempty text of at most 2000 characters")
    return task.strip()


def _check_job_name(name: str) -> str:
    if not isinstance(name, str) or not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,47}", name):
        raise ValueError("job_name must be 1..48 safe ASCII characters")
    return name


def _job(name: str) -> Path:
    return REPO / "out" / "claude-reviewed-tools" / _check_job_name(name)


def _description(key: str, spec: dict, record: dict) -> str:
    pieces = [key, spec.get("why", "")]
    for name in ("title_ar", "title_en", "summary_ar", "summary_en", "area",
                 "keywords", "use_when", "families"):
        v = record.get(name, "")
        pieces.append(" ".join(map(str, v)) if isinstance(v, list) else str(v))
    return " ".join(pieces)


def route(task: str, limit: int = 8) -> dict:
    task = _check_task(task)
    if type(limit) is not int or not 1 <= limit <= 20:
        raise ValueError("limit must be an integer from 1 to 20")
    available, catalog, records = _registry(), _inventory(), _records()
    unknown = set(available) - set(catalog)
    if unknown:
        raise ValueError("Reviewed registry contains unknown catalog ID: " + sorted(unknown)[0])
    query_tokens = brain.tokens(task)
    ranked = []
    for key, spec in available.items():
        desc = _description(key, spec, records.get(key, {}))
        common = sorted(query_tokens & brain.tokens(desc))
        if not common and task.casefold() not in desc.casefold():
            continue
        bonus = 2 if task.casefold() in desc.casefold() else 0
        ranked.append({"id": key, "score": len(common) + bonus,
                       "matched_terms": common[:8],
                       "depends_on": spec.get("depends_on", []),
                       "purpose": str(spec.get("why", ""))[:180],
                       "registered": True, "runtime_verified": False})
    ranked.sort(key=lambda v: (-v["score"], v["id"]))
    return {"schema": SCHEMA + ".route", "task": task,
            "catalog_total": len(catalog), "reviewed_adapter_total": len(available),
            "matched": len(ranked), "candidates": ranked[:limit],
            "meaning": "Lexical suggestions only; no executors have run"}


def _select(ids: list[str], catalog: dict, adapters: dict) -> tuple[dict, dict]:
    if not isinstance(ids, list) or not 1 <= len(ids) <= MAX_SELECTED:
        raise ValueError("ids must contain 1..8 reviewed tool IDs")
    if any(not isinstance(k, str) for k in ids) or len(set(ids)) != len(ids):
        raise ValueError("IDs must be distinct strings")
    unknown = set(ids) - set(adapters)
    if unknown:
        raise ValueError("Unreviewed or unknown adapter: " + sorted(unknown)[0])
    if set(ids) - set(catalog):
        raise ValueError("Adapter missing from current installed catalog")
    # Never silently run extra prerequisites. Require caller to explicitly list them.
    for key in ids:
        missing = set(adapters[key].get("depends_on", [])) - set(ids)
        if missing:
            raise ValueError("Explicit prerequisite required for " + key + ": " + ", ".join(sorted(missing)))
    return ({key: catalog[key] for key in sorted(ids)},
            {key: adapters[key] for key in sorted(ids)})


def _file_hash(path: Path) -> str:
    return dragon.audit.sha256(path)


def _bounded_runtime(workers: int, timeout: int) -> None:
    if type(workers) is not int or not 1 <= workers <= MAX_WORKERS:
        raise ValueError("workers must be 1..4")
    if type(timeout) is not int or not 1 <= timeout <= MAX_TIMEOUT:
        raise ValueError("timeout must be 1..120")


def preview(task: str, ids: list[str], *, workers: int = 2, timeout: int = 60) -> dict:
    """Stable, read-only approval plan; never executes an adapter or creates a job.

    The SHA binds exact task, selected IDs, prerequisite waves, adapter
    definitions and script contents. It is NOT user consent or a signature.
    """
    task = _check_task(task)
    _bounded_runtime(workers, timeout)
    catalog, registered = _inventory(), _registry()
    selected, adapters = _select(ids, catalog, registered)
    strategy = brain.plan(task, selected, adapters)
    scripts = []
    for key in sorted(selected):
        spec = adapters[key]
        path = dragon._safe_script(spec["script"])
        if not any("{artifact}" in arg for arg in spec.get("args", [])):
            raise ValueError("Adapter needs {artifact} output placeholder: " + key)
        scripts.append({
            "id": key, "script": spec["script"], "script_sha256": _file_hash(path),
            "adapter_sha256": hashlib.sha256(json.dumps(
                spec, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest(),
            "depends_on": sorted(spec.get("depends_on", [])),
        })
    packet = {
        "schema": SCHEMA + ".approval-plan",
        "task": task,
        "selected": sorted(selected),
        "waves": strategy["waves"],
        "workers": workers, "timeout": timeout,
        "scripts": scripts,
        "catalog_fingerprint": dragon.audit.fingerprint(catalog),
        "registry_sha256": _file_hash(dragon.REVIEWED_ADAPTERS),
    }
    serialized = json.dumps(packet, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return {
        **packet,
        "approval_digest": hashlib.sha256(serialized.encode("utf-8")).hexdigest(),
        "execution_performed": False, "runtime_verified": False,
        "scope": "selected-reviewed-only",
        "approval_required": "Review exact IDs/commands and provide separate explicit consent; digest alone grants no permission",
    }


def _inside_file(file: str, job: Path, subfolder: str) -> Path:
    raw = Path(file)
    expected = (job / subfolder).resolve()
    actual = raw.resolve()
    if not actual.is_relative_to(expected) or raw.is_symlink() or not actual.is_file():
        raise ValueError("Receipt/artifact outside approved job")
    return actual


def review(job_name: str) -> dict:
    """Independently re-open immutable assignment + receipts and verify hashes."""
    job = _job(job_name)
    if not job.is_dir() or job.is_symlink() or not job.resolve().is_relative_to((REPO / "out" / "claude-reviewed-tools").resolve()):
        raise ValueError("Unknown reviewed tool job")
    path = job / "reviewed_execution.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != SCHEMA or data.get("scope") != "selected-reviewed-only":
        raise ValueError("Invalid reviewed execution ledger")
    selected = data.get("selected")
    if (not isinstance(selected, list) or not 1 <= len(selected) <= MAX_SELECTED or
            any(not isinstance(k, str) for k in selected) or len(selected) != len(set(selected))):
        raise ValueError("Invalid selected IDs")
    entries = data.get("entries", {})
    if not isinstance(entries, dict) or set(selected) != set(entries):
        raise ValueError("Missing or extra selected entries")
    issues, counts = [], Counter()
    for key in selected:
        item = entries[key]
        if not isinstance(item, dict):
            issues.append(key + ": malformed ledger entry")
            continue
        status = item.get("status")
        counts[status] += 1
        if status == "executed":
            try:
                receipt = _inside_file(item["receipt_path"], job, "receipts")
                proof = json.loads(receipt.read_text(encoding="utf-8"))
                artifact = _inside_file(proof["artifact"], job, "artifacts")
                if (proof.get("entry") != key or proof.get("exit_code") != 0 or
                        _file_hash(receipt) != item.get("receipt_sha256") or
                        not artifact.stat().st_size or
                        _file_hash(artifact) != proof.get("artifact_sha256")):
                    issues.append(key + ": receipt/artifact integrity mismatch")
            except (OSError, KeyError, TypeError, ValueError) as exc:
                issues.append(key + ": invalid receipt (" + str(exc)[:90] + ")")
        elif status not in ("blocked", "failed"):
            issues.append(key + ": unknown execution status")
    if sum(counts.values()) != len(selected):
        issues.append("Count mismatch")
    return {"schema": SCHEMA + ".review", "scope": "selected-reviewed-only",
            "selected": len(selected), "verified_executed": counts["executed"],
            "blocked": counts["blocked"], "failed": counts["failed"],
            "passed": not issues, "selected_subset_fully_executed": not issues and counts["executed"] == len(selected),
            "entire_catalog_executed": False, "issues": issues[:30]}


def execute(task: str, ids: list[str], job_name: str, *,
            permission: bool = False, workers: int = 2, timeout: int = 60,
            approval_digest: str | None = None) -> dict:
    """Explicitly selected, reviewed and independently verifiable local adapters."""
    task = _check_task(task)
    job = _job(job_name)
    if permission is not True or os.environ.get("KOSIF_ALLOW_ADAPTER_EXECUTION") != "1":
        raise PermissionError("Reviewed execution requires explicit MCP permission and KOSIF_ALLOW_ADAPTER_EXECUTION=1")
    _bounded_runtime(workers, timeout)
    if approval_digest is not None:
        if not isinstance(approval_digest, str) or not re.fullmatch(r"[0-9a-f]{64}", approval_digest):
            raise ValueError("Invalid approval_digest")
        current = preview(task, ids, workers=workers, timeout=timeout)["approval_digest"]
        if not hmac.compare_digest(approval_digest, current):
            raise PermissionError("Approval plan changed; preview the exact task, IDs, adapters and scripts again")
    catalog, registered = _inventory(), _registry()
    selected, adapters = _select(ids, catalog, registered)
    strategy = brain.plan(task, selected, adapters)
    # Validate all selected script paths before creating any job or executing a tool.
    for key, spec in adapters.items():
        dragon._safe_script(spec["script"])
        if not any("{artifact}" in arg for arg in spec.get("args", [])):
            raise ValueError("Adapter needs {artifact} output placeholder: " + key)
    job = dragon._safe_job(job)
    if job.exists():
        raise FileExistsError("Use a fresh job_name; reviewed jobs cannot be reused")
    job.mkdir(parents=True)
    (job / "receipts").mkdir()
    (job / "artifacts").mkdir()
    outcomes = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        for wave in strategy["waves"]:
            running = {}
            for key in wave:
                blockers = [d for d in strategy["items"][key]["depends_on"]
                            if outcomes[d]["status"] != "executed"]
                if blockers:
                    outcomes[key] = {"status": "blocked", "reason": "Prerequisite failed: " + ", ".join(blockers)}
                else:
                    running[pool.submit(dragon._attempt, key, adapters[key], task, job, True, timeout)] = key
            for future in concurrent.futures.as_completed(running):
                key = running[future]
                try:
                    outcomes[key] = future.result()
                except Exception as exc:
                    outcomes[key] = {"status": "failed", "reason": str(exc)[:180]}
    entries = {}
    for key in sorted(selected):
        outcome = outcomes[key]
        value = {"status": outcome["status"]}
        if outcome["status"] == "executed":
            try:
                verified = dragon.audit.evidence(outcome["receipt"], key)
                value.update({"receipt_path": verified["receipt_path"],
                              "receipt_sha256": verified["receipt_sha256"]})
            except (OSError, ValueError, KeyError) as exc:
                value = {"status": "failed", "reason": "Proof validation: " + str(exc)[:180]}
        else:
            value["reason"] = str(outcome.get("reason", "Unknown"))[:180]
        entries[key] = value
    ledger = {"schema": SCHEMA, "scope": "selected-reviewed-only", "task": task,
              "approval_digest": approval_digest,
              "catalog_size": len(catalog), "selected": sorted(selected), "entries": entries,
              "catalog_fingerprint": dragon.audit.fingerprint(catalog),
              "reviewed_registry_sha256": _file_hash(dragon.REVIEWED_ADAPTERS)}
    (job / "reviewed_execution.json").write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    checked = review(job_name)
    return {"job": str(job), "review": checked, "scope": "selected-reviewed-only",
            "truth": "Selected reviewed adapters only; never implies entire catalog executed"}
