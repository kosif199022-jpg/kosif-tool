#!/usr/bin/env python3
"""Route vetted, non-executable Atlas method guidance with source provenance.

Never executes, imports, installs or dynamically fetches third-party skills.
This selector enriches KOSIF Superpowers; REA/Ghidra remain separate live tools.
"""
import argparse
import json
from pathlib import Path
import re
import sys

MANIFEST = Path(__file__).resolve().parent.parent / "data" / "atlas-reviewed-methods-20261020.json"
SCHEMA = "kosif.superpowers.atlas.reviewed-methods.v3"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
TOKEN = re.compile(r"[\w\u0600-\u06ff]+", re.UNICODE)

def load_manifest(path=MANIFEST):
    data=json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if data.get("schema") != SCHEMA: raise ValueError("unrecognized provenance schema")
    methods=data.get("methods")
    if not isinstance(methods,list) or not methods: raise ValueError("no methods")
    seen=set()
    for m in methods:
        for key in ("id","domain","name","keywords","method","path","sha256","upstream","source_commit"):
            if not m.get(key): raise ValueError("missing "+key)
        if not HEX64.fullmatch(str(m["sha256"])): raise ValueError("invalid sha256")
        if m["id"] in seen: raise ValueError("duplicate method")
        seen.add(m["id"])
        if not str(m["path"]).startswith("skills/") or ".." in m["path"].split("/"):
            raise ValueError("invalid provenance path")
        if m["source_commit"] != data["source_commit"]: raise ValueError("source revision mismatch")
        if m["review_state"] != "text_read_metadata_candidate_not_runtime_verified":
            raise ValueError("unsafe status")
        if m["third_party_code_executed"] is not False or m["third_party_code_copied"] is not False:
            raise ValueError("unsupported provenance claim")
    return data

def route(task, domain=None, top=3, manifest=None):
    if not isinstance(task,str) or not (1 <= len(task) <= 1500): raise ValueError("task length")
    if not 1 <= top <= 5: raise ValueError("top out of range")
    data=manifest or load_manifest()
    if domain and domain not in {m["domain"] for m in data["methods"]}:
        raise ValueError("unknown domain")
    source=task.casefold()
    tokens=set(TOKEN.findall(source))
    ranked=[]
    for m in data["methods"]:
        if domain and m["domain"]!=domain: continue
        matches=[w for w in m["keywords"] if w.casefold() in tokens or (len(w)>3 and w.casefold() in source)]
        if not matches:continue
        score=10*len(set(matches)) + max(map(len,matches))
        ranked.append((-score,m["id"],m,matches))
    ranked.sort()
    selected=[]
    for _,_,m,matches in ranked[:top]:
        selected.append({"method_id":m["id"],"domain":m["domain"],"source_skill":m["name"],
                         "task_keywords":matches,"original_guidance":m["method"],"sha256":m["sha256"],
                         "atlas_path":m["path"],"source_commit":m["source_commit"],
                         "upstream":m["upstream"],"license_claimed":m["license_claimed"],
                         "status":"static_source_read_only_not_executed"})
    return {"schema":"kosif.superpowers.atlas.task-guidance.v3","task":task,"selected":selected,
            "fallback":"native_superpowers_capabilities" if not selected else None,
            "does_not_execute_external_code":True,
            "live_tools_not_automatically_enabled":True,
            "note":"Run-time capabilities still require installed tool checks and explicit approval for side effects."}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--task")
    g.add_argument("--doctor",action="store_true")
    g.add_argument("--list",action="store_true")
    p.add_argument("--domain")
    p.add_argument("--top",type=int,default=3)
    args=p.parse_args()
    manifest=load_manifest()
    if args.doctor:
        from collections import Counter
        out={"healthy":True,"schema":SCHEMA,"methods":len(manifest["methods"]),
             "domains":dict(Counter(m["domain"] for m in manifest["methods"])),
             "source_texts_inspected":manifest["source_texts_inspected"],
             "verified_runtime_skills":0,"source_code_executed":False}
    elif args.list:
        out=[{"id":m["id"],"name":m["name"],"domain":m["domain"]} for m in manifest["methods"]]
    else:
        out=route(args.task,args.domain,args.top,manifest)
    print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=="__main__":
    try:main()
    except (ValueError,OSError,KeyError,TypeError,json.JSONDecodeError) as exc:
        print(str(exc),file=sys.stderr)
        sys.exit(2)
