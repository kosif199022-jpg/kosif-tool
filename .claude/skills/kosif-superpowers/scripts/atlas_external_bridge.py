#!/usr/bin/env python3
"""KOSIF Atlas searchable, read-only bridge; never imports or executes a skill."""
import argparse
import collections
import json
import os
from pathlib import Path
import re
import sys

STOP = set("the and for with from this that into your you are to of an a in or من في على الى إلى عن هذا هذه مع ال".split())
def norm(v):
    return re.sub(r"[^\w\u0600-\u06ff]+", " ", str(v or "").casefold()).strip()
def load(path):
    raw = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    items = raw if isinstance(raw,list) else raw.get("skills")
    if not isinstance(items,list): raise ValueError("Atlas index does not contain a skills list")
    return items
def family(item):
    text = norm(" ".join(str(item.get(k) or "") for k in ("skill","description","plugin")))
    domains = {
        "film-video-3d":("video","render","blender","3d","motion","film","animation","cinema","photography"),
        "development":("coding","program","code","developer","software","repository","api"),
        "research":("research","search","analysis","knowledge","evidence"),
        "thinking":("reason","decision","thinking","planning","logic"),
        "design":("graphic","design","draw","image","illustrat","typograph"),
        "audio":("audio","speech","music","voice","sound"),
    }
    counts={k:sum(t in text for t in tokens) for k,tokens in domains.items()}
    return max(counts,key=counts.get) if any(counts.values()) else "general"
def score(item,query):
    words=[s for s in norm(query).split() if len(s)>1 and s not in STOP]
    name=norm(item.get("skill"))
    hay=norm(item.get("description"))+" "+norm(item.get("plugin"))
    return sum((5 if w in name else 1 if w in hay else 0) for w in words)
def inspect_skill(root,entry):
    if not root: return "NOT_READ"
    base=Path(root).resolve()
    p=(base/str(entry.get("path",""))).resolve()
    if not p.is_relative_to(base): return "INVALID_PATH"
    p=p/"SKILL.md" if p.is_dir() else p
    if p.name!="SKILL.md" or not p.is_file(): return "SKILL_MD_MISSING"
    if p.stat().st_size>262144: return "SKILL_MD_TOO_LARGE"
    data=p.read_text(encoding="utf-8",errors="replace")
    return {"status":"READ_ONLY", "lines":data.count("\n")+1,
            "headings":re.findall(r"^#{1,3} .+",data,re.M)[:12]}
def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("action",choices=["stats","search"])
    p.add_argument("--index",default=os.getenv("KOSIF_ATLAS_INDEX"))
    p.add_argument("--copyleft-index",default=None,help="External copyleft index; reference only")
    p.add_argument("--query",default="")
    p.add_argument("--top",type=int,default=20)
    p.add_argument("--skill-root",default=None)
    p.add_argument("--audit-records",default=None,help="Private content-review receipts JSON; never executes referenced skill code")
    p.add_argument("--reviewed-manifest",default=str(Path(__file__).resolve().parent.parent / "data" / "atlas-reviewed" / "manifest.json"),help="Committed metadata-only reviewed skill receipts")
    a=p.parse_args(argv)
    if not a.index:p.error("pass --index or set KOSIF_ATLAS_INDEX")
    rows=load(a.index)
    for x in rows:
        if isinstance(x,dict):x["_scope"]="permissive_claimed"
    if a.copyleft_index:
        extra=load(a.copyleft_index)
        for x in extra:
            if isinstance(x,dict):x["_scope"]="copyleft_reference_only"
        rows+=extra
    audit={}
    if a.reviewed_manifest and Path(a.reviewed_manifest).is_file():
        for receipt in json.loads(Path(a.reviewed_manifest).read_text(encoding="utf-8")).get("skills",[]):
            audit[str(receipt["id"])]={"skill_body_read":bool(receipt.get("document_sha256")),
              "code_files_read":receipt.get("code_files_read",0),
              "review_indicators":set(receipt.get("content_indicators",[]))}
    if a.audit_records:
        for record in json.loads(Path(a.audit_records).read_text(encoding="utf-8")):
            key=str(record.get("skill_id"))
            entry=audit.setdefault(key,{"skill_body_read":False,"code_files_read":0,"review_indicators":set()})
            if record.get("status")=="FETCHED":
                if record.get("kind")=="skill":entry["skill_body_read"]=True
                if record.get("kind")=="code":entry["code_files_read"]+=1
            entry["review_indicators"].update(record.get("details",{}).get("indicators",{}).keys())
    if a.action=="stats":
        data={"entries":len(rows),
              "scopes":dict(collections.Counter(str(x.get("_scope","unknown")) for x in rows if isinstance(x,dict))),
              "license_labels":dict(collections.Counter(str(x.get("license","unknown")) for x in rows if isinstance(x,dict))),
              "risk_flagged":sum(bool(x.get("risk_flags")) for x in rows if isinstance(x,dict)),
              "verdicts":dict(collections.Counter(str(x.get("verdict","unknown")) for x in rows if isinstance(x,dict))),
              "domains":dict(collections.Counter(family(x) for x in rows if isinstance(x,dict))),
              "audit_skills_with_bodies":sum(x["skill_body_read"] for x in audit.values()),
              "proof_status":"INDEX_ONLY_NOT_RUNTIME_TESTED"}
    else:
        if not a.query:p.error("--query required")
        matches=sorted((x for x in rows if isinstance(x,dict)),key=lambda x:(-score(x,a.query),str(x.get("id",""))))
        matches=[x for x in matches if score(x,a.query)>0][:max(1,min(a.top,100))]
        data={"matches":[{"id":x.get("id"),"skill":x.get("skill"),"description":str(x.get("description",""))[:300],
                          "license":x.get("license"),"source":x.get("source"),"path":x.get("path"),
                          "risk_flags":x.get("risk_flags"),"verdict":x.get("verdict"),
                          "license_scope":x.get("_scope"),
                          "category":family(x),"inspection":(inspect_skill(a.skill_root,x) if a.skill_root else ("SOURCE_BODY_RECEIPT" if audit.get(str(x["id"]),{}).get("skill_body_read") else "NOT_READ")),
                          "content_audit":({**audit[str(x["id"])],"review_indicators":sorted(audit[str(x["id"])]["review_indicators"])} if str(x["id"]) in audit else {"skill_body_read":False}),
                          "execution":"NOT_EXECUTED"} for x in matches],
              "total_entries":len(rows),"query":a.query}
    print(json.dumps(data,ensure_ascii=False,indent=2))
if __name__=="__main__":
    try:main()
    except (OSError,ValueError,json.JSONDecodeError) as e:
        print(json.dumps({"error":str(e)},ensure_ascii=False),file=sys.stderr);raise SystemExit(2)
