#!/usr/bin/env python3
"""Run *method-only* routing for the reviewed KOSIF Atlas guidance.

This is NOT a third-party skill executor; it doesn't connect to REA/Ghidra or
request device permissions. Never treat catalog matches as runtime receipts.
"""
import argparse
import json
from pathlib import Path

ROUTES = {
 "cause_chain_and_reversal_check": ("root cause","5 why","5-why","السبب الجذري","تحليل السبب","جذر المشكلة"),
 "premortem_with_kill_criteria": ("pre-mortem","premortem","what could fail","failure modes","ماذا لو فشلت","مخاطر الخطة"),
 "agent_runtime_layers_and_approval": ("agent security","agent permission","agent guardrail","runtime guardrail","أمان الوكلاء","صلاحيات الوكيل"),
 "agent_tool_trust_boundary_model": ("threat model","agentic security","prompt injection","tool abuse","نمذجة التهديد","حقن برومبت"),
 "binary_trace_evidence_checklist": ("reverse engineering","disassembly","decompile","ghidra","hopping binary","هندسة عكسية","غيدرا","جفرة"),
 "weekly_liquidity_projection": ("13 week","13-week","cash flow forecast","cashflow forecast","توقع التدفق النقدي","توقع السيولة","التدفقات النقدية"),
 "tax_ledger_reconciliation": ("tax reconciliation","vat reconciliation","reconcile tax","مطابقة الضريبة","مطابقة ضريبة","تسوية الضريبة"),
 "react_composition_render_qa": ("remotion","react video","video composition","فيديو ريأكت","موشن ريأكت"),
 "media_transcode_probe_validation": ("ffmpeg","video transcode","video encode","ترميز الفيديو","فحص تصدير الفيديو","تصدير mp4"),
 "tokenized_spacing_and_type": ("design tokens","ui spacing","responsive ui","ui design","تصميم واجهات","تباعد الواجهات","تطوير الواجهة","مسافات الواجهة"),
 "claim_to_evidence_validation": ("verify citations","citation audit","source verification","check references","التحقق من الاستشهادات","تدقيق المصادر","راجع المصادر"),
 "interactive_ui_regression": ("frontend testing","playwright","browser ui test","اختبار الواجهات","اختبر الواجهات","اختبار المتصفح"),
 "redaction_with_integrity_receipts": ("redaction","redact document","pii removal","تنقيح مستند","إخفاء معلومات حساسة","حجب بيانات حساسة"),
 "readiness_gate_before_report": ("xbert ias","independent activity statement","ias-prep"),
 "human_language_style_checks": ("humanize writing","anti-ai writing","natural writing","صياغة بشرية","اجعل النص طبيعي","أزل أسلوب الذكاء"),
}
ORDER=list(ROUTES)
def route(task,manifest,max_methods=2):
    if not 1<=max_methods<=2:raise ValueError("method cap is 1..2")
    text=task.casefold()
    sources={item["method"]:item for item in manifest.get("method_candidates",[])}
    ranked=[]
    for method,terms in ROUTES.items():
        if method not in sources:continue
        matches=[x for x in terms if x.casefold() in text]
        if not matches:continue
        # More precise/longer phrases outrank short shared words
        score=max(map(len,matches))+min(2,len(matches))
        ranked.append((score,ORDER.index(method),method,matches))
    ranked.sort(key=lambda v:(-v[0],v[1]))
    picked=[]
    for score,_,key,matches in ranked[:max_methods]:
        s=sources[key]
        picked.append({"method":key,"matched_terms":matches,"atlas_skill":s["skill"],
          "source_path":s["source_path"],"sha256":s["sha256"],
          "upstream":s["upstream"],"status":"method_candidate_guidance_only",
          "third_party_code_executed":False,"executor_exposed":False})
    return {
      "schema":"kosif.superpowers.atlas.method-route.v1",
      "input_task":task,"selected_count":len(picked),"selected":picked,
      "fallback":"native_kosif_superpowers" if not picked else None,
      "scope":"Reviewed methods only, max two; native catalog remains primary; permission/device/execution requires separate live verification."
    }
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--task",required=True)
    p.add_argument("--manifest",type=Path)
    p.add_argument("--max-methods",type=int,default=2)
    args=p.parse_args()
    manifest_path=args.manifest or (Path(__file__).resolve().parent.parent/"data/atlas-method-provenance-20261020.json")
    data=json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    if data.get("schema")!="kosif.superpowers.atlas.method-provenance.v2":
        p.error("unknown provenance manifest")
    print(json.dumps(route(args.task,data,args.max_methods),ensure_ascii=False,indent=2))
if __name__=="__main__":main()
