#!/usr/bin/env python3
"""Explicit Black Dragon invocation choice and USIP council orchestration contracts.

This module *plans* the activation of the complete catalog or a reviewed
task-relevant subset. It never silently executes a tool or fabricates LLM
reviewer output. Every catalog entry remains represented in either mode.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import _black_dragon_brain as brain

MODES = ("all", "smart")
COUNCIL = (
    ("contrarian", "المعارض", "Which assumption could invalidate the proposed solution?"),
    ("first_principles", "مفكر المبادئ الأولى", "What is the real problem and simplest test of success?"),
    ("expansionist", "الموسّع", "What useful adjacent capability or opportunity is being missed?"),
    ("outsider", "الغريب", "What would confuse a newcomer or hide a critical dependency?"),
    ("executor", "المنفّذ", "Which ordered steps, permissions and proof make this deliverable real?"),
)
PROTOCOL_SOURCES = (
    "PROTOCOL.md",
    "references/protocol/A13-pro-council.md",
    "references/protocol/A38-v58-thinking-books-github-pulse.md",
    "references/protocol/A30-council-100.md",
    "references/protocol/A49-v65-dragon-in-pipeline.md",
)


def invocation() -> dict:
    """A machine-readable conversational choice, *not* permission to execute."""
    return {
        "schema": "kosif.black-dragon.invocation.v1",
        "trigger": ["استدعِ التنين الأسود", "شغّل التنين الأسود", "invoke black dragon"],
        "question_ar": "عايز التنين الأسود يستخدم كل القدرات بتوزيع ذكي، ولا يختار القدرات الأنسب للمهمة؟",
        "question_en": "Use the full capability catalog, or choose a focused set intelligently?",
        "options": [
            {"id": "all", "label_ar": "كل القدرات", "effect": "Assign EVERY catalog item a stage and method; attempt every approved reviewed adapter with its prerequisites."},
            {"id": "smart", "label_ar": "اختيار ذكي", "effect": "Inspect the entire catalog; execute only a scored, dependency-closed set of reviewed adapters."},
        ],
        "approval": "Choosing a mode is not permission for paid, external, mutating or unreviewed actions.",
    }


def select(task: str, inventory: dict, adapters: dict, mode: str,
           skill_root: Path | None = None) -> tuple[dict, dict, dict]:
    """Return a complete plan and the eligible reviewed adapters for this mode."""
    if mode not in MODES:
        raise ValueError("activation must be all or smart")
    full = brain.plan(task, inventory, adapters, skill_root=skill_root)
    if mode == "all" or not adapters:
        chosen = set(adapters)
    else:
        by_part: dict[str, list[str]] = {}
        for key in sorted(adapters):
            part = full["items"][key]["part"]
            by_part.setdefault(part, []).append(key)
        def rank(key: str) -> tuple:
            entry = full["items"][key]
            return (-int(entry["priority"]), -int(entry["weight"] == "lead"), key)
        chosen = set()
        # Give each represented execution stage a reviewed candidate first.
        for keys in by_part.values():
            chosen.add(min(keys, key=rank))
        # Then add task-matching candidates up to a bounded focus budget.
        budget = min(len(adapters), max(len(chosen), 12))
        for key in sorted(adapters, key=rank):
            if len(chosen) >= budget:
                break
            if full["items"][key]["priority"] > 0 or not chosen:
                chosen.add(key)
        # Do not omit an adapter dependency merely because its score is low.
        pending = list(chosen)
        while pending:
            key = pending.pop()
            for dependency in full["items"][key]["depends_on"]:
                if dependency in adapters and dependency not in chosen:
                    chosen.add(dependency)
                    pending.append(dependency)
    selected = {key: adapters[key] for key in sorted(chosen)}
    plan = full if len(selected) == len(adapters) else brain.plan(
        task, inventory, selected, skill_root=skill_root)
    if set(plan["items"]) != set(inventory):
        raise ValueError("Activation cannot omit a catalog entry")
    decision = {
        "schema": "kosif.black-dragon.activation.v1",
        "mode": mode,
        "catalog_examined": len(inventory),
        "catalog_assigned": len(plan["items"]),
        "reviewed_adapters_available": len(adapters),
        "reviewed_adapters_selected": len(selected),
        "selected_adapter_ids": sorted(selected),
        "unselected_reviewed_adapters": sorted(set(adapters) - set(selected)),
        "reason": ("Full catalog and all reviewed adapters scheduled" if mode == "all"
                   else "All entries examined; ranked reviewed adapters and dependency closure"),
        "execution_authorized": False,
        "notice": "Assignment is not execution. A separate approval and evidence receipts are required.",
    }
    return plan, selected, decision


def council_plan(task: str, activation: dict) -> dict:
    """Protocol-aligned handoffs, without pretending five independent minds ran."""
    stages = [
        {"id": "understand", "protocol": "request card / success criteria", "needs": []},
        {"id": "inventory", "protocol": "scan all sources with complete coverage", "needs": ["understand"]},
        {"id": "frame", "protocol": "SEE lenses, dependencies and risk", "needs": ["inventory"]},
        {"id": "council", "protocol": "five critical perspectives, dissent and evidence", "needs": ["frame"]},
        {"id": "architectures", "protocol": "compare A/B/C, acceptance gates, select the plan", "needs": ["council"]},
        {"id": "execute", "protocol": "run only reviewed, authorized adapters in dependency waves",
         "needs": ["architectures"]},
        {"id": "verify", "protocol": "independent artifact/receipt audit and user delivery", "needs": ["execute"]},
    ]
    out = {
        "schema": "kosif.black-dragon.usip-council.v1",
        "task": task,
        "activation": activation["mode"],
        "status": "planned-not-executed",
        "protocol_sources": list(PROTOCOL_SOURCES),
        "stages": stages,
        "members": [{"id": mid, "name_ar": ar, "review_prompt": question,
                     "status": "awaiting-genuine-review"} for mid, ar, question in COUNCIL],
        "decision_gate": "Do not accept an architecture until objections, alternate evidence, permissions and execution checks are addressed.",
        "external_reviewers_invoked": False,
        "note": "Council prompts are a workflow contract. Separate real reviewer outputs must be ingested and checked before claiming a council verdict.",
    }
    raw = json.dumps(out, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    out["plan_sha256"] = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    return out


def _static_source(record: dict, repo_root: Path, skill_root: Path) -> dict:
    """Read and fingerprint a registered tool's source; never import or run it."""
    raw = record.get("path")
    root_name = record.get("root", "repo")
    if root_name not in ("repo", "skill") or not isinstance(raw, str) or not raw.strip():
        return {"status": "invalid_metadata", "reason": "Missing path or unsupported root"}
    rel = Path(raw)
    if rel.is_absolute() or ".." in rel.parts:
        return {"status": "unsafe_path", "reason": "Absolute/traversal source path"}
    root = (skill_root if root_name == "skill" else repo_root).resolve()
    target = root / rel
    if any(node.is_symlink() for node in (target, *target.parents) if node != root):
        return {"status": "unsafe_path", "reason": "Symlink in source path"}
    if not target.resolve().is_relative_to(root):
        return {"status": "unsafe_path", "reason": "Source escapes declared root"}
    if not target.is_file():
        return {"status": "missing_source", "reason": "Declared source file does not exist"}
    try:
        digest = hashlib.sha256()
        with target.open("rb") as stream:
            for chunk in iter(lambda: stream.read(65536), b""):
                digest.update(chunk)
    except OSError as exc:
        return {"status": "source_unreadable", "reason": type(exc).__name__}
    return {"status": "inspected", "source": f"{root_name}/{rel.as_posix()}",
            "source_sha256": digest.hexdigest()}


def inspect_and_schedule(task: str, inventory: dict, adapters: dict,
                         tool_records: dict, repo_root: Path, skill_root: Path,
                         mode: str = "all") -> dict:
    """Inventory -> static inspection -> dependency plan -> approval gate.

    Covers ALL registered catalog tools in either mode; all mode selects ALL
    reviewed adapters, not arbitrary scripts. There is no subprocess/import of
    catalog tools and the result never grants permission to execute.
    """
    from collections import Counter

    if not isinstance(tool_records, dict):
        raise ValueError("Tool registry must be keyed by catalog ID")
    plan, selected, activation = select(task, inventory, adapters, mode, skill_root)
    if set(plan["items"]) != set(inventory):
        raise ValueError("Incomplete capability catalog")
    tool_ids = sorted(k for k, meta in inventory.items() if meta.get("kind") == "tool")
    rows = {}
    for key in tool_ids:
        record = tool_records.get(key)
        detail = (_static_source(record, repo_root, skill_root)
                  if isinstance(record, dict)
                  else {"status": "missing_metadata", "reason": "No matching tools.json record"})
        spec = selected.get(key)
        adapter_status = "not_selected" if key in adapters else "not_reviewed"
        if spec is not None:
            script = spec.get("script")
            arguments = spec.get("args", [])
            if not isinstance(script, str) or not isinstance(arguments, list) or not all(
                    isinstance(arg, str) for arg in arguments):
                adapter_status = "invalid_manifest"
            else:
                adapter_status = _static_source(
                    {"root": "repo", "path": script}, repo_root, skill_root)["status"]
                adapter_status = ("reviewed_candidate" if adapter_status == "inspected"
                                  else "adapter_" + adapter_status)
        item = plan["items"][key]
        purpose_fields = ("title_ar", "title_en", "summary_ar", "summary_en", "use_when", "area")
        purpose = " | ".join(str(record[k]) for k in purpose_fields
                             if isinstance(record, dict) and record.get(k))[:600]
        safety = str(record.get("safety") or "unknown") if isinstance(record, dict) else "unknown"
        rows[key] = {
            "id": key, "purpose": purpose or key,
            "kind": str(record.get("kind") or "undocumented") if isinstance(record, dict) else "unregistered",
            "stage": item["part"], "priority": item["priority"],
            "weight": item["weight"], "application": item["application"],
            "depends_on": item["depends_on"], "risk": safety,
            "inspection": detail, "adapter_status": adapter_status,
            "selected": key in selected,
            "execution_authorized": False,
        }
    # Validate source inspection before calling anything a runnable candidate.
    candidates = {k for k, row in rows.items()
                  if row["inspection"]["status"] == "inspected"
                  and row["adapter_status"] == "reviewed_candidate"}
    # A candidate cannot run if one of its adapter dependencies is not eligible.
    eligible = set(candidates)
    changed = True
    while changed:
        blocked = {key for key in eligible if any(
            dep not in selected or
            (dep.startswith("tool:") and dep not in eligible)
            for dep in plan["items"][key]["depends_on"])}
        changed = bool(blocked)
        eligible -= blocked
    for key, row in rows.items():
        row["readiness"] = (
            "candidate_requires_approval" if key in eligible else
            "dependency_blocked" if key in candidates else
            "inspection_blocked" if row["inspection"]["status"] != "inspected" else
            "review_required" if key in adapters else "knowledge_only"
        )
    stage_order = list(plan["parts"])
    stages = []
    for stage in stage_order:
        members = sorted((key for key in tool_ids if rows[key]["stage"] == stage),
                         key=lambda key: (-rows[key]["priority"], key))
        stages.append({"id": stage, "name": plan["parts"][stage]["ar"],
                       "tool_count": len(members), "tools": members})
    # The brain already computed dependency-correct waves over the full catalog.
    # Preserve them; never reorder by stage in a way that violates dependencies.
    waves = [[key for key in wave if key in eligible]
             for wave in plan["waves"]]
    waves = [wave for wave in waves if wave]
    result = {
        "schema": "kosif.black-dragon.tool-inspection.v1",
        "task": task, "mode": mode, "status": "planned_not_executed",
        "activation": activation,
        "catalog": {"examined": len(inventory), "assigned": len(plan["items"]),
                    "assignment_sha256": plan["assignment_sha256"]},
        "tools": rows, "stages": stages, "dependency_waves": waves,
        "council": council_plan(task, activation),
        "counts": {
            "catalog_tools": len(tool_ids),
            "statically_inspected": sum(r["inspection"]["status"] == "inspected" for r in rows.values()),
            "missing_or_unsafe": sum(r["inspection"]["status"] != "inspected" for r in rows.values()),
            "reviewed_adapters_selected": len(selected),
            "tool_candidates_after_dependencies": len(eligible),
            "execution_attempts": 0,
        },
        "approval_gate": {
            "required": True, "approved": False,
            "conditions": ["review purpose, permissions and dependency waves",
                           "approve external/write/paid actions independently",
                           "verify actual outputs and receipts after execution"],
        },
        "limitations": ("Static inspection verifies metadata, local paths and hashes; it does not "
                        "prove that a tool works. Assignment is not execution. Council is a planned "
                        "review contract, not five completed independent reviews."),
    }
    raw = json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    result["plan_sha256"] = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    return result
