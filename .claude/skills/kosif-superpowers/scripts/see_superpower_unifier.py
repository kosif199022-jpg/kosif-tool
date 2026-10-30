#!/usr/bin/env python3
"""SEE → Superpowers unified thinking and capability planner (stdlib only).

This is a *planning adapter* on top of the existing KOSIF hub, never a second
capability registry or a claim that an external SEE/Full Pro model ran.
It preserves original power IDs, tool readiness, and proof boundaries.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import OrderedDict

PACKS = OrderedDict([
    ("kosif-research-evidence", ("research", "search", "sources", "citation", "fact", "verify source", "بحث", "مصادر", "دليل", "تحقق")),
    ("kosif-agent-contracts", ("agent", "automation", "connector", "computer", "whatsapp", "browser", "tool", "وكيل", "اتمت", "متصفح", "اداه", "ربط")),
    ("kosif-eval-trust", ("test", "qa", "audit", "validation", "security", "review", "اختبار", "تقييم", "مراجعه", "جوده", "تحقق")),
    ("kosif-engineering-reliability", ("code", "github", "debug", "fix", "app", "software", "api", "python", "برنامج", "برمجه", "كود", "تطوير", "مستودع")),
    ("kosif-product-strategy", ("product", "strategy", "business", "market", "decision", "roadmap", "تخطيط", "استراتيجيه", "منتج", "جدوي", "قرار")),
    ("kosif-finance-data", ("finance", "accounting", "excel", "bank", "ledger", "invoice", "vat", "financial", "محاسب", "مالي", "بنك", "فواتير", "ضريبه", "مخزون", "اكسل")),
    ("kosif-prompt-architecture", ("prompt", "instruction", "llm", "system prompt", "برومبت", "تعليمات", "توجيه", "صياغه")),
    ("kosif-media-motion", ("video", "motion", "audio", "image", "render", "reels", "animation", "فيديو", "مونتاج", "موشن", "صوره", "تصميم", "صوت", "رسم")),
    ("kosif-skill-orchestrator", ("skills", "superpowers", "fusion", "merge", "capability", "see", "مهار", "قدرات", "سوبر", "دمج", "توحيد", "قصيف")),
])

LENSES = OrderedDict([
    ("S0-01", "goal_and_acceptance"),
    ("S0-02", "independent_perspectives"),
    ("S0-03", "assumption_sensitivity"),
    ("S0-04", "premortem"),
    ("S0-05", "evidence_vs_inference"),
    ("S0-06", "scenarios_and_uncertainty"),
    ("S0-07", "hard_fail_and_verification"),
    ("S0-08", "user_requirements"),
    ("S0-09", "interfaces_and_dependencies"),
    ("S0-10", "deterministic_numbers"),
    ("S0-11", "causal_falsification"),
])
MODES = {"fast": 0, "standard": 2, "deep": 4, "full_pro": 4}
SENSITIVE = re.compile(r"(?i)\b(?:sk-proj-[a-z0-9_-]{12,}|gh[pousr]_[a-z0-9]{20,}|bearer\s+[a-z0-9._-]{20,})\b")


def normalize(value: str) -> str:
    s = re.sub(r"[\u064b-\u0652\u0640]", "", str(value).lower())
    for a, b in (("أ", "ا"), ("إ", "ا"), ("آ", "ا"), ("ة", "ه"), ("ى", "ي")):
        s = s.replace(a, b)
    return s


def redact(text: str) -> str:
    return SENSITIVE.sub("[REDACTED]", text)


def select_methods(task: str, mode: str = "standard") -> list[dict]:
    if mode not in MODES:
        raise ValueError("INVALID_MODE")
    if mode == "fast":
        return []
    query = normalize(task)
    ranked = []
    for order, (name, phrases) in enumerate(PACKS.items()):
        hits = [w for w in phrases if normalize(w) in query]
        if hits:
            ranked.append((-len(hits), order, name, hits))
    ranked.sort()
    selected = [dict(name=name, reason="task_keyword_match", matches=hits[:4], status="method_candidate")
                for _, _, name, hits in ranked[:MODES[mode]]]
    if not selected:
        selected = [{"name": "kosif-research-evidence", "reason": "general_evidence_default",
                     "matches": [], "status": "method_candidate"}]
    return selected


def unique_records(rows, key="id", max_count=8) -> list[dict]:
    seen, output = set(), []
    for item in rows or []:
        if not isinstance(item, dict):
            continue
        ident = item.get(key)
        if not isinstance(ident, str) or not ident or ident in seen:
            continue
        seen.add(ident)
        output.append(item)
        if len(output) >= max_count:
            break
    return output


def fuse(task: str, hub_result: dict, mode: str = "standard") -> dict:
    """Compose *candidate* methods with real hub metadata; perform no execution."""
    if not isinstance(hub_result, dict):
        raise ValueError("HUB_RESULT_REQUIRED")
    methods = select_methods(task, mode)
    tools = unique_records(hub_result.get("tools"), max_count=6)
    powers = unique_records(hub_result.get("powers"), max_count=10)
    selected_tools = []
    for row in tools:
        readiness = row.get("readiness")
        readiness = readiness if isinstance(readiness, dict) else {}
        state = readiness.get("state", "unknown")
        selected_tools.append({
            "id": row["id"], "readiness": state,
            "status": "executor_exposed" if state == "ready" else "candidate_only",
            "source": "hub.find", "executed": False, "verified": False,
        })
    graph = {
        "nodes": [
            {"id": "N0", "role": "frame_with_11_lenses", "input_kind": "any", "output_kind": "plan", "state": "planned"},
            {"id": "N1", "role": "route_existing_superpowers_and_see_methods", "input_kind": "plan", "output_kind": "plan", "state": "planned"},
            {"id": "N2", "role": "run_authorized_executor", "input_kind": "plan", "output_kind": "evidence", "state": "pending_execution"},
            {"id": "N3", "role": "independent_deterministic_qa", "input_kind": "evidence", "output_kind": "report", "state": "pending_execution"},
            {"id": "N4", "role": "deliver_with_receipt", "input_kind": "report", "output_kind": "package", "state": "pending_execution"},
        ],
        "edges": [
            {"from": "N0", "to": "N1", "kind": "plan"},
            {"from": "N1", "to": "N2", "kind": "plan"},
            {"from": "N2", "to": "N3", "kind": "evidence"},
            {"from": "N3", "to": "N4", "kind": "report"},
        ],
    }
    return {
        "schema": "kosif.see-superpowers.unified-plan.v1",
        "status": "PLAN_ONLY",
        "query": redact(task),
        "mode_requested": mode,
        "full_pro": {"requested": mode == "full_pro", "completed": False,
                     "status": "NOT_FULL_PRO" if mode == "full_pro" else "NOT_REQUESTED"},
        "thinking_lenses": list(LENSES.keys()),
        "see_domain_coverage": list(PACKS),
        "selected_see_methods": methods,
        "existing_superpowers": [{"id": p["id"], "family": p.get("family"),
                                  "status": "candidate_only"} for p in powers],
        "existing_tools": selected_tools,
        "graph": graph,
        "verified": False,
        "claims": {"executed": False, "verified": False, "reviewers_executed": 0},
        "limits": ["No private SEE source or model weights transferred",
                   "Readiness is not execution", "No cross-project data sharing",
                   "No Full Pro claim without independent request-bound receipt",
                   "Human approval needed for privileged or irreversible actions"],
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("plan", "self-test"))
    parser.add_argument("task", nargs="?", default="")
    parser.add_argument("--mode", choices=tuple(MODES), default="standard")
    args = parser.parse_args(argv)
    if args.command == "self-test":
        d = fuse("دمج قدرات SEE في سوبر باور", {"powers": [{"id": "SP-1"}, {"id": "SP-1"}]})
        assert len(d["existing_superpowers"]) == 1
        assert len(d["thinking_lenses"]) == 11 and len(d["see_domain_coverage"]) == 9
        assert not d["claims"]["executed"] and not d["verified"]
        print("PASS")
        return 0
    if not args.task.strip():
        parser.error("task is required")
    import hub  # Existing one front door; never create a second registry.
    result = hub.find(args.task)
    print(json.dumps(fuse(args.task, result, args.mode), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
