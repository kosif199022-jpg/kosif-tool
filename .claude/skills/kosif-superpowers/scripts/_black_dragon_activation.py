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
