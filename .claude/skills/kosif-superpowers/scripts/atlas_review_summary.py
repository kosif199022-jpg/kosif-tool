#!/usr/bin/env python3
"""Generate compact evidence-backed method candidates from a static Atlas review."""
import argparse
import json
from pathlib import Path
from collections import Counter

PICKS = {
 "5why-root-cause": "cause_chain_and_reversal_check",
 "pre-mortem": "premortem_with_kill_criteria",
 "agent-runtime-guardrails": "agent_runtime_layers_and_approval",
 "agentic-threat-model": "agent_tool_trust_boundary_model",
 "binary-analysis-patterns": "binary_trace_evidence_checklist",
 "cashflow-13week": "weekly_liquidity_projection",
 "tax-reconciliation": "tax_ledger_reconciliation",
 "remotion": "react_composition_render_qa",
 "ffmpeg": "media_transcode_probe_validation",
 "design-constraints": "tokenized_spacing_and_type",
 "ai-citation-verification": "claim_to_evidence_validation",
 "frontend-testing-debugging": "interactive_ui_regression",
 "redaction-and-provenance": "redaction_with_integrity_receipts",
 "ias-prep": "readiness_gate_before_report",
 "anti-ai-writing-patterns": "human_language_style_checks",
}
def summarize(r):
    if r.get("schema")!="kosif.atlas.stratified-review.v2" or r.get("mode")!="audit":
        raise ValueError("expected Atlas source review v2")
    examined=[x for x in r["audited_files"] if x["source_audit"]["state"]=="text_inspected_not_executed"]
    selected={}
    for x in examined:
        if x["skill"] not in PICKS or x["scope"]!="main": continue
        # No duplicate copies of same skill family; preserve first observed.
        if x["skill"] not in selected:
            selected[x["skill"]]={
                "method":PICKS[x["skill"]],"skill":x["skill"],"atlas_id":x["id"],
                "source_path":x["path"]+"/SKILL.md","upstream":x["source"],
                "license_label":x["license"],"sha256":x["source_audit"]["sha256"],
                "warning_labels":x["source_audit"]["warnings"],
                "static_text_inspected":True,
                "executed":False,"runtime_verified":False,
                "guidance_candidate_only":True,
            }
    return {
        "schema":"kosif.superpowers.atlas.method-provenance.v2",
        "atlas_index_sha256":r["atlas_index_sha256"],
        "catalog_overview":{k:r["catalog"][k] for k in (
            "total","main","copyleft","unique_normalized_skill_names",
            "reused_names","records_in_reused_names",
            "duplicate_description_groups","records_in_duplicate_descriptions",
            "claimed_file_count_sum","claimed_complete_folders")},
        "inspected_sample_count":len(examined),
        "audit_sample_count":r["source_sample_plan_size"],
        "warning_counts":{k:v for k,v in r["static_audit_counts"].items() if k.startswith("warning:")},
        "classification_counts":dict(Counter(x["source_audit"].get("classification","not_checked") for x in r["audited_files"])),
        "method_candidates":[selected[k] for k in PICKS if k in selected],
        "method_candidate_count":len(selected),
        "all_methods_are_proposed_and_not_executed":True,
        "limitations":"Index metadata: 14,793; static source sampling: 395; 0 third-party skills executed or runtime-verified. No guarantee of license authenticity or security. REA/Ghidra are appropriate for binary artifacts; Atlas tree contains no .exe/.dll/.so/.wasm/.jar as observed at baseline."
    }
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--review",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args()
    d=json.loads(args.review.read_text(encoding="utf-8-sig"))
    result=summarize(d)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"sample":result["inspected_sample_count"],"candidate_count":result["method_candidate_count"],"classification":result["classification_counts"]}))
if __name__=="__main__":main()
