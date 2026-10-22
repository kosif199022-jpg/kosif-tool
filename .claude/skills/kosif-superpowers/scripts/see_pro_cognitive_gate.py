#!/usr/bin/env python3
"""KOSIF SEE Pro Cognitive Packet Gate.

Validates declared reasoning-route contracts, handoffs and evidence *metadata*.
It cannot verify remote tools, evaluate idea quality or activate Full Pro.
Run:
  python3 scripts/see_pro_cognitive_gate.py --self-test
  python3 scripts/see_pro_cognitive_gate.py check --file cognitive_packet.json
Python stdlib only. No network, secrets, filesystem mutation or model invocations.
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path

SCHEMA = "kosif.seepro.cognitive-packet.v1"
PACKS = {
    "kosif-research-evidence", "kosif-agent-contracts", "kosif-eval-trust",
    "kosif-engineering-reliability", "kosif-product-strategy",
    "kosif-finance-data", "kosif-prompt-architecture", "kosif-media-motion",
    "kosif-skill-orchestrator",
}
LEVELS = {"L0", "L1", "L2", "L3"}
MODES = {"fast", "standard", "deep", "full_pro"}
KINDS = {"any", "brief", "spec", "plan", "sources", "code", "dataset", "report",
         "document", "image", "audio", "video", "model3d", "font", "prompt", "evidence", "package"}
RELATIONS = {"sequence", "parallel", "complement", "substitute", "verify", "refine", "fallback"}
STATUS = {"proposed", "method_loaded", "executor_exposed", "executed", "verified"}
SECRET = re.compile(r"(?i)(?:sk-proj-[a-z0-9_-]{12,}|gh[pousr]_[a-z0-9]{20,}"
                    r"|xox[baprs]-[a-z0-9-]{16,}|bearer\s+[a-z0-9._-]{20,})")


def as_list(x):
    return x if isinstance(x, list) else []


def as_dict(x):
    return x if isinstance(x, dict) else {}


def validate(p):
    """Return (errors, warnings, summary). No side effects; no remote proof inference."""
    e, w = [], []
    if not isinstance(p, dict):
        return ["PACKET_NOT_OBJECT"], [], {}
    if p.get("schema") != SCHEMA:
        e.append("SCHEMA_MISMATCH")
    level, mode = p.get("level"), p.get("mode")
    if level not in LEVELS:
        e.append("LEVEL_INVALID")
    if mode not in MODES:
        e.append("MODE_INVALID")
    stage0 = as_dict(p.get("stage0"))
    if level in {"L2", "L3"}:
        for field in ("goal", "artifact", "success_criteria"):
            if not stage0.get(field):
                e.append("STAGE0_MISSING_" + field.upper())
    methods = as_list(p.get("methods"))
    seen = set()
    cap = 4 if mode in {"deep", "full_pro"} else 2
    dynamic = 0
    if len(methods) > cap:
        e.append("METHOD_PACK_LIMIT")
    for item in methods:
        if not isinstance(item, dict):
            e.append("METHOD_ENTRY_INVALID")
            continue
        name, typ = item.get("name"), item.get("type", "local")
        if typ not in ("local", "dynamic"):
            e.append("METHOD_TYPE_INVALID")
        if typ == "local" and name not in PACKS:
            e.append("UNKNOWN_STABLE_PACK")
        if typ == "dynamic":
            dynamic += 1
            if not item.get("source_read"):
                e.append("DYNAMIC_SOURCE_NOT_READ")
            if not item.get("coverage_gap"):
                e.append("DYNAMIC_WITHOUT_NAMED_GAP")
        if name in seen:
            e.append("DUPLICATE_PACK")
        seen.add(name)
    if dynamic > (2 if mode in {"deep", "full_pro"} else 1):
        e.append("DYNAMIC_SPECIALIST_LIMIT")

    nodes = as_list(as_dict(p.get("composition")).get("nodes"))
    edges = as_list(as_dict(p.get("composition")).get("edges"))
    ids = set()
    nodemap = {}
    for n in nodes:
        if not isinstance(n, dict):
            e.append("NODE_INVALID")
            continue
        nid = n.get("id")
        if not isinstance(nid, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{0,31}", nid):
            e.append("NODE_ID_INVALID")
            continue
        if nid in ids:
            e.append("DUPLICATE_NODE_ID")
        ids.add(nid)
        nodemap[nid] = n
        for k in ("input_kind", "output_kind"):
            if n.get(k) not in KINDS:
                e.append("NODE_KIND_INVALID")
        if n.get("executor_state", "proposed") not in STATUS:
            e.append("EXECUTOR_STATE_INVALID")
    for link in edges:
        if not isinstance(link, dict):
            e.append("EDGE_INVALID")
            continue
        a, b = link.get("from"), link.get("to")
        if a not in ids or b not in ids or a == b:
            e.append("EDGE_ENDPOINT_INVALID")
            continue
        if link.get("relation") not in RELATIONS:
            e.append("EDGE_RELATION_INVALID")
        kind = link.get("kind")
        if kind not in KINDS:
            e.append("EDGE_KIND_INVALID")
        if (kind != "any" and nodemap[a].get("output_kind") not in ("any", kind)):
            e.append("EDGE_SOURCE_KIND_MISMATCH")
        if (kind != "any" and nodemap[b].get("input_kind") not in ("any", kind)):
            e.append("EDGE_TARGET_KIND_MISMATCH")
    if level in {"L2", "L3"} and nodes and not edges and len(nodes) > 1:
        w.append("NO_TYPED_HANDOFFS")

    opts = as_list(p.get("options"))
    if level in {"L2", "L3"} and p.get("phase") == "planning":
        letters = {x.get("id") for x in opts if isinstance(x, dict)}
        if not {"A", "B", "C"}.issubset(letters):
            e.append("THREE_PLANS_MISSING")
        strategies = [x.get("strategy_key") for x in opts if isinstance(x, dict)
                      and x.get("id") in {"A", "B", "C"}]
        if len(strategies) != 3 or any(not s for s in strategies) or len(set(strategies)) != 3:
            e.append("PLANS_NOT_MEANINGFULLY_DISTINCT")

    claims, receipts = as_dict(p.get("claims")), as_dict(p.get("receipts"))
    if claims.get("full_pro_completed") is True:
        fp = as_dict(receipts.get("full_pro"))
        if (mode != "full_pro" or not fp.get("request_id")
                or fp.get("status") != "completed" or fp.get("runtime_verified") is not True
                or fp.get("executor_qa_pass") is not True):
            e.append("FULL_PRO_CLAIM_UNPROVEN")
    if claims.get("executed") is True:
        execution = as_dict(receipts.get("execution"))
        if not (execution.get("request_id") and execution.get("executor")
                and execution.get("status") == "executed"):
            e.append("EXECUTION_CLAIM_UNPROVEN")
    if claims.get("verified") is True:
        qa = as_dict(receipts.get("qa"))
        if not (claims.get("executed") is True and qa.get("passed") is True and qa.get("artifact")):
            e.append("VERIFIED_CLAIM_UNPROVEN")
    count = claims.get("reviewers_executed", 0)
    peer = as_list(receipts.get("reviewers"))
    if isinstance(count, bool) or not isinstance(count, int) or count < 0:
        e.append("REVIEWER_COUNT_INVALID")
    elif count > len({v.get("request_id") for v in peer if isinstance(v, dict)
                     and v.get("status") == "completed" and v.get("request_id")}):
        e.append("REVIEWERS_CLAIM_UNPROVEN")

    for f in as_list(p.get("facts")):
        if isinstance(f, dict) and f.get("status") == "supported" and not f.get("source"):
            e.append("FACT_SOURCE_MISSING")
    num = as_dict(p.get("numeric"))
    if num.get("exact_claim") is True and not (num.get("deterministic_receipt")
                                              and num.get("independent_check") is True):
        e.append("EXACT_NUMERIC_CLAIM_UNPROVEN")
    scope = as_dict(p.get("privacy"))
    if scope.get("cross_tenant_data") is True and scope.get("approved") is not True:
        e.append("CROSS_TENANT_DENIED")
    if scope.get("export_raw_client_data") is True:
        e.append("RAW_CLIENT_DATA_EXPORT_DENIED")
    if SECRET.search(json.dumps(p, ensure_ascii=False)):
        e.append("SECRET_PATTERN_DETECTED")
    if mode == "full_pro" and not claims.get("full_pro_completed"):
        w.append("FULL_PRO_NOT_COMPLETED_NO_COMPLETION_CLAIM")
    return sorted(set(e)), sorted(set(w)), {
        "schema": SCHEMA, "level": level, "mode": mode, "methods": len(methods),
        "dynamic": dynamic, "nodes": len(ids), "edges": len(edges),
        "status": "PASS" if not e else "HARD_FAIL",
    }


def self_test():
    base = {"schema": SCHEMA, "level": "L3", "mode": "deep", "phase": "planning",
            "stage0": {"goal": "Produce a film", "artifact": "video",
                       "success_criteria": ["real MP4 validated by ffprobe"]},
            "methods": [{"name": "kosif-media-motion"},
                        {"name": "kosif-eval-trust"}],
            "composition": {"nodes": [
                {"id": "N1", "input_kind": "audio", "output_kind": "video"},
                {"id": "N2", "input_kind": "video", "output_kind": "report"}],
                "edges": [{"from": "N1", "to": "N2", "relation": "verify", "kind": "video"}]},
            "options": [{"id": "A", "strategy_key": "simple-timeline"},
                        {"id": "B", "strategy_key": "procedural-motion"},
                        {"id": "C", "strategy_key": "cinematic-stock-edit"}],
            "claims": {"executed": False, "verified": False, "full_pro_completed": False,
                       "reviewers_executed": 0},
            "privacy": {"cross_tenant_data": False}}
    assert validate(base)[0] == [], validate(base)
    cases = [
        ({"mode": "full_pro", "claims": {"full_pro_completed": True}}, "FULL_PRO_CLAIM_UNPROVEN"),
        ({"methods": [{"name": n} for n in sorted(PACKS)]}, "METHOD_PACK_LIMIT"),
        ({"composition": {"nodes": base["composition"]["nodes"],
                          "edges": [{"from": "N1", "to": "N2", "relation": "verify", "kind": "audio"}]}},
         "EDGE_SOURCE_KIND_MISMATCH"),
        ({"options": [{"id": i, "strategy_key": "same"} for i in "ABC"]},
         "PLANS_NOT_MEANINGFULLY_DISTINCT"),
        ({"numeric": {"exact_claim": True}}, "EXACT_NUMERIC_CLAIM_UNPROVEN"),
        ({"privacy": {"cross_tenant_data": True, "approved": False}}, "CROSS_TENANT_DENIED"),
        ({"claims": {"reviewers_executed": 500}}, "REVIEWERS_CLAIM_UNPROVEN"),
        ({"claims": {"executed": True}}, "EXECUTION_CLAIM_UNPROVEN"),
        ({"claims": {"verified": True}}, "VERIFIED_CLAIM_UNPROVEN"),
        ({"facts": [{"status": "supported", "claim": "X"}]}, "FACT_SOURCE_MISSING"),
    ]
    for patch, expected in cases:
        test = copy.deepcopy(base)
        test.update(patch)
        errors = validate(test)[0]
        assert expected in errors, (expected, errors)
    return len(cases) + 1


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd")
    check = sub.add_parser("check")
    check.add_argument("--file", type=Path, required=True)
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args(argv)
    if args.self_test:
        print(json.dumps({"self_tests_passed": self_test()}, ensure_ascii=False))
        return 0
    if args.cmd != "check":
        p.error("Use --self-test or check --file PACKET.json")
    if not args.file.is_file() or args.file.stat().st_size > 1_000_000:
        print("Invalid cognitive packet file", file=sys.stderr)
        return 2
    try:
        packet = json.loads(args.file.read_text(encoding="utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        print("Invalid JSON: " + str(exc), file=sys.stderr)
        return 2
    errors, warnings, summary = validate(packet)
    print(json.dumps({"summary": summary, "errors": errors, "warnings": warnings},
                     ensure_ascii=False, indent=2))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
