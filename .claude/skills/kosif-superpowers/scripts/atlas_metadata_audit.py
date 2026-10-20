#!/usr/bin/env python3
"""Non-executing validation of KOSIF Atlas third-party skill metadata.

Reading an index proves catalog coverage, NOT trustworthiness or ability to
run the actual skills. No network, shell, import or code execution.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit

def audit(main, copyleft):
    data=json.loads(Path(main).read_text(encoding="utf-8-sig"))
    copy=json.loads(Path(copyleft).read_text(encoding="utf-8-sig"))
    if any(not isinstance(d,dict) or not isinstance(d.get("skills"),list) for d in (data,copy)):
        raise ValueError("bad Atlas schema")
    stat=Counter()
    license_stats=Counter()
    verdicts=Counter()
    domains=Counter()
    seen=set()
    errors=[]
    examples=[]
    for origin,payload in (("main",data),("copyleft",copy)):
        if payload.get("count") != len(payload["skills"]):
            errors.append(origin+":index-count-mismatch")
        for row in payload["skills"]:
            if not isinstance(row,dict):
                errors.append(origin+":invalid-record")
                continue
            ident=(origin,str(row.get("id")))
            if ident in seen or str(row.get("id")) in ("None",""):
                errors.append(origin+":duplicate-or-missing-id:"+str(row.get("id")))
            seen.add(ident)
            for key in ("plugin","skill","description","license","source","path","verdict"):
                if not row.get(key):
                    errors.append(origin+":missing-"+key+":"+str(row.get("id")))
            license_stats[str(row.get("license","missing"))]+=1
            verdicts[str(row.get("verdict","unclassified"))]+=1
            src=str(row.get("source",""))
            u=urlsplit(src)
            if u.scheme != "https" or not u.hostname:
                stat["missing_verified_source_url"]+=1
                if len(examples)<12:
                    examples.append({"source":origin,"id":row.get("id"),"problem":"source-url"})
            else:
                domains[u.hostname]+=1
            if row.get("risk_flags"):
                stat["flagged_for_review"]+=1
            if origin=="copyleft":
                stat["copyleft_skill_records"]+=1
            elif row.get("complete") is True:
                stat["claimed_complete_folder"]+=1
            if row.get("verdict")=="REVIEW_BEFORE_INSTALL":
                stat["review_before_install"]+=1
            if row.get("verdict")=="READ_ONLY_OK":
                stat["read_only_classified"]+=1
    return {"schema":"kosif.atlas.metadata.v1",
            "main_records":len(data["skills"]),"copyleft_records":len(copy["skills"]),
            "examined":len(data["skills"])+len(copy["skills"]),
            "distinct_ids_in_scopes":len(seen),
            "claimed_license_labels":dict(license_stats),
            "claimed_verdicts":dict(verdicts),
            "inventory_counts":dict(stat),
            "source_domain_counts":dict(domains.most_common(15)),
            "structural_errors":errors[:40],
            "samples":examples,
            "live_capabilities_verified":0,
            "script_bodies_audited":0,
            "network_calls":False,"executes_skills":False,
            "limitations":"This audits metadata only, not every skill's actual source, safety, behavior, or license authenticity."}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--index",type=Path,required=True)
    p.add_argument("--copyleft",type=Path,required=True)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    result=audit(a.index,a.copyleft)
    text=json.dumps(result,ensure_ascii=False,indent=2)
    if a.output:
        if a.output.exists() or not a.output.parent.is_dir():
            raise ValueError("output must be a new file in an existing directory")
        a.output.write_text(text+"\n",encoding="utf-8")
    print(text)
    return 1 if result["structural_errors"] else 0

if __name__=="__main__":
    try:raise SystemExit(main())
    except (ValueError,OSError,json.JSONDecodeError) as e:
        print(str(e),file=sys.stderr);raise SystemExit(1)
