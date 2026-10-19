#!/usr/bin/env python3
"""Bounded REA source-analysis of user-owned repos. Private evidence stays local.

Requires an explicit --private-output outside Git, authenticated GitHub access,
and installed REA CLI. Clones only selected repositories with Git blob filtering.
No installation scripts or repo code are run.
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

def execute(cmd,timeout=120):
    return subprocess.run(cmd,capture_output=True,text=True,encoding="utf-8",
                          errors="replace",timeout=timeout)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--private-output",type=Path,required=True)
    ap.add_argument("--rea-cli",type=Path,required=True)
    ap.add_argument("--max-size-kb",type=int,default=8000)
    ap.add_argument("--max-repos",type=int,default=16)
    a=ap.parse_args()
    base=a.private_output.resolve()
    if not base.exists(): ap.error("private inventory directory missing")
    inventory=base/"owner_repositories_PRIVATE_LOCAL.json"
    if not inventory.is_file(): ap.error("run owner inventory first")
    if not a.rea_cli.is_file(): ap.error("installed REA CLI not found")
    if (base/".git").exists(): ap.error("private evidence directory cannot be a git repo")
    entries=json.loads(inventory.read_text(encoding="utf-8"))
    candidates=[v for v in entries if v.get("language") in ("JavaScript","TypeScript","HTML")
                and 0 < (v.get("size_kb") or 0) <= a.max_size_kb]
    candidates.sort(key=lambda x:(x.get("size_kb",0),x["repository"]))
    results=[]
    cache=base/"source_clones"
    cache.mkdir(parents=True,exist_ok=True)
    evidence=base/"rea_evidence"
    evidence.mkdir(parents=True,exist_ok=True)
    for repo in candidates[:a.max_repos]:
        name=repo["repository"]
        safe=name.replace("/","__")
        directory=cache/safe
        print("START",safe,flush=True)
        record={"repository":name,"private":bool(repo["private"]),
                "size_kb":repo["size_kb"],"language":repo["language"],
                "rea_source_analyzed":False,"status":"pending"}
        try:
            if not (directory/".git").is_dir():
                # Partial/shallow repo checkout; never runs a repository installer.
                r=execute(["git","-c","core.longpaths=true","clone","--depth","1",
                           "--filter=blob:none","--single-branch","--quiet",
                           "https://github.com/"+name+".git",str(directory)],timeout=160)
                if r.returncode:
                    raise RuntimeError("clone failed: "+r.stderr[:250])
            # REA statically reads source, does not execute it.
            t=execute(["node",str(a.rea_cli),"analyze-javascript-application",str(directory),
                       "--max-heap-mb","384","--analysis-timeout-ms","40000",
                       "--format","json"],timeout=100)
            dest=evidence/(safe+".json")
            if t.returncode or not t.stdout.strip():
                record["status"]="rea_failed"
                record["error"]=(t.stderr or t.stdout)[:300]
            else:
                try:
                    j=json.loads(t.stdout)
                    normalized=j.get("normalized_result") or {}
                    stats=normalized.get("statistics") or {}
                    dest.write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding="utf-8")
                    record.update({"rea_source_analyzed":True,
                         "status":"static_javascript_analysis_completed",
                         "js_files_parsed":stats.get("parsed_javascript_files",0),
                         "ast_nodes":stats.get("visited_ast_nodes",0),
                         "findings":stats.get("findings",0),
                         "source_code_limitations":"Static JS only; not runtime feature verification",
                         "evidence_id":j.get("evidence_id")})
                except ValueError as e:
                    record["status"]="unparsed_rea_output"
                    record["error"]=str(e)
        except Exception as e:
            record["status"]="failed"
            record["error"]=str(e)[:300]
        results.append(record)
        (base/"rea_owned_repo_results_PRIVATE_LOCAL.json").write_text(
            json.dumps(results,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        print("RESULT",safe,record["status"],record.get("js_files_parsed"),
              record.get("findings"),flush=True)
    public={"attempted":len(results),"rea_completed":sum(bool(x["rea_source_analyzed"]) for x in results),
            "parsed_js_files":sum(int(x.get("js_files_parsed") or 0) for x in results),
            "findings":sum(int(x.get("findings") or 0) for x in results),
            "private_evidence_shared":False,
            "notice":"Metadata/tree inspection covered every owned repository separately; this REA batch analyzes eligible subset only."}
    print(json.dumps(public,ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    sys.exit(main())
