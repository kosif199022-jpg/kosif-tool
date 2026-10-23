#!/usr/bin/env python3
"""Evidence-first read-only audit of external Atlas skill bodies.

Fetches bounded raw SKILL.md (and selected code files), never executes them.
Security matches are review signals, not malware determinations.
Writes full fetched content only to caller's private output directory.
"""
from __future__ import annotations
import argparse
import concurrent.futures
import collections
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import time
import urllib.error
import urllib.request

BASE="https://raw.githubusercontent.com/kosif199022-jpg/kosif-atlas/main/"
TOKENS={
    "mind":["thinking","reasoning","decision","creativ","critical","logic","verify","planning","problem-solv","research","memory","uncertainty","eval"],
    "motion":["blender","render","cycles","video","film","animation","cinemat","motion","3d","character","light","camera","audio","music","storyboard","ffmpeg"],
    "audit":["account","audit","finance","fraud","risk","excel","data","analytics","security","database","forensic"],
    "engineering":["code","software","typescript","javascript","debug","architecture","browser","test","automation","agent","mcp","reverse"],
}
THREATS={
    "remote_script_execution":re.compile(r"(?:\b(?:curl|wget)\b.{0,180}(?:\|\s*(?:bash|sh)\b))|(?:\b(?:iex|Invoke-Expression)\b)",re.I),
    "destructive_shell":re.compile(r"(?:\brm\s+-rf\b)|(?:\b(?:Remove-Item|del|rmdir)\b.{0,90}(?:-Recurse|-Force|/s))|(?:\bformat\s+[a-z]:)",re.I),
    "secret_collection":re.compile(r"(?:\b(?:\.env|api.?key|password|secret|private.?key|token)\b.{0,80}\b(?:send|post|upload|exfiltrat|print))|(?:\b(?:send|post|upload|exfiltrat)\b.{0,80}\b(?:\.env|api.?key|password|secret|private.?key|token))",re.I),
    "prompt_instruction_override":re.compile(r"(?:ignore (?:all )?(?:previous|earlier|system|developer) instructions)|(?:reveal your (?:system|hidden) prompt)|(?:override (?:safety|system|developer) rules)",re.I),
    "shell_mutation":re.compile(r"\b(?:npm\s+install|pip\s+install|brew\s+install|winget\s+install|sudo\s+|chmod\s+\+x|docker\s+run)\b",re.I),
}
EXEC_EXT={".js",".mjs",".cjs",".ts",".py",".sh",".ps1"}
def sha(data):return hashlib.sha256(data).hexdigest()
def valid_rel(rel):
    p=PurePosixPath(str(rel).replace("\\","/"))
    if p.is_absolute() or ".." in p.parts or not p.parts:return False
    return all(x and x not in (".","..") for x in p.parts)
def fetch(rel,max_bytes):
    if not valid_rel(rel):return "INVALID_PATH",None
    url=BASE+"/".join(urllib.parse.quote(p,safe="-._~") for p in PurePosixPath(rel).parts)
    request=urllib.request.Request(url,headers={"User-Agent":"KOSIF-Audit-Bounded/1.0","Accept":"text/plain"})
    try:
        with urllib.request.urlopen(request,timeout=22) as response:
            data=response.read(max_bytes+1)
            if len(data)>max_bytes:return "TOO_LARGE",None
            return "FETCHED",data
    except urllib.error.HTTPError as e:return "HTTP_"+str(e.code),None
    except (urllib.error.URLError,TimeoutError,OSError) as e:return "NETWORK_"+type(e).__name__,None
def score(x):
    body=(str(x.get("skill",""))+" "+str(x.get("description",""))).lower()
    points={k:sum(8 if t in str(x.get("skill","")).lower() else 2 if t in body else 0 for t in values) for k,values in TOKENS.items()}
    scripts=[f for f in x.get("files",[]) if Path(f).suffix.lower() in EXEC_EXT]
    return points,scripts
def choose(rows,limit):
    pools=collections.defaultdict(list)
    for x in rows:
        if not isinstance(x,dict):continue
        points,scripts=score(x)
        bucket=max(points,key=points.get) if any(points.values()) else "other"
        pools[bucket].append((max(points.values())+(5 if scripts else 0)+(2 if x.get("risk_flags") else 0),x))
    for group in pools:
        pools[group].sort(key=lambda t:(-t[0],str(t[1].get("id",0))))
    chosen=[];seen=set()
    # Give each family a real code-review sample; then fill by score
    order=["mind","motion","audit","engineering","other"]
    quota={"mind":0.18,"motion":0.25,"audit":0.19,"engineering":0.26,"other":0.12}
    for key in order:
        n=max(1,int(limit*quota[key]))
        for _,x in pools.get(key,[])[:n]:
            if x["id"] not in seen:chosen.append(x);seen.add(x["id"])
    if len(chosen)<limit:
        left=sorted((v for key in pools for v in pools[key] if v[1]["id"] not in seen),key=lambda z:(-z[0],str(z[1]["id"])))
        chosen.extend(x for _,x in left[:limit-len(chosen)])
    return chosen[:limit]
def inspect_text(data):
    text=data.decode("utf-8",errors="replace")
    matches={k:[] for k in THREATS}
    for number,line in enumerate(text.splitlines(),1):
        for cat,pat in THREATS.items():
            if pat.search(line):
                if len(matches[cat])<8:matches[cat].append(number)
    headings=re.findall(r"^#{1,3} ([^\r\n]{1,160})",text,re.M)
    return {"lines":text.count("\n")+1,"headings":headings[:12],
            "indicators":{k:v for k,v in matches.items() if v},
            "chars":len(text)}
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--index",required=True)
    p.add_argument("--copyleft-index",default=None)
    p.add_argument("--out",required=True)
    p.add_argument("--limit",type=int,default=200)
    p.add_argument("--workers",type=int,default=10)
    p.add_argument("--max-bytes",type=int,default=180000)
    p.add_argument("--scripts-per-skill",type=int,default=2)
    a=p.parse_args()
    if not 1<=a.limit<=1000 or not 1<=a.workers<=16:p.error("batch resource limits exceeded")
    sources=[json.loads(Path(a.index).read_text(encoding="utf-8"))["skills"]]
    if a.copyleft_index:sources.append(json.loads(Path(a.copyleft_index).read_text(encoding="utf-8"))["skills"])
    rows=[dict(x,license_scope="copyleft_reference" if i else "standard") for i,seq in enumerate(sources) for x in seq]
    selection=choose(rows,a.limit)
    dest=Path(a.out).resolve()
    dest.mkdir(parents=True,exist_ok=True)
    jobs=[]
    for x in selection:
        mainrel=str(PurePosixPath(x["path"])/"SKILL.md")
        jobs.append((x,"skill",mainrel))
        scripts=[f for f in x.get("files",[]) if Path(f).suffix.lower() in EXEC_EXT]
        for f in scripts[:a.scripts_per_skill]:
            jobs.append((x,"code",str(PurePosixPath(x["path"])/f)))
    def task(job):
        x,kind,rel=job
        status,content=fetch(rel,a.max_bytes)
        record={"skill_id":x.get("id"),"skill_name":x.get("skill"),"kind":kind,
                "path":rel,"status":status,"license_claim":x.get("license"),
                "license_scope":x.get("license_scope"),"origin":x.get("source"),
                "risk_flags":x.get("risk_flags") or [],"verdict":x.get("verdict")}
        if content is not None:
            record.update(sha256=sha(content),bytes=len(content),details=inspect_text(content))
            target=dest/"source"/str(x["id"])/kind/Path(rel).name
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(content)
            record["local_evidence"]=str(target.relative_to(dest)).replace("\\","/")
        return record
    start=time.monotonic()
    with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as pool:
        result=list(pool.map(task,jobs))
    tally=collections.Counter(x["status"] for x in result)
    categories=collections.Counter(cat for row in result if row.get("details") for cat in row["details"]["indicators"])
    byid={x["id"]:x for x in selection}
    resultfile=dest/"records.json"
    resultfile.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    report={"schema":"kosif.atlas.content-audit.v1","method":"bounded static SKILL.md and script source retrieval; no execution",
      "selection":"deterministic topic-stratified priority; not random/full coverage",
      "index_record_count":len(rows),"selected_skills":len(selection),"requested_files":len(jobs),
      "statuses":dict(tally),"risk_indicator_counts":dict(categories),
      "downloaded_skill_bodies":sum(r["kind"]=="skill" and r["status"]=="FETCHED" for r in result),
      "downloaded_code_files":sum(r["kind"]=="code" and r["status"]=="FETCHED" for r in result),
      "elapsed_seconds":round(time.monotonic()-start,2),
      "not_verified":"Neither static indicators nor source availability prove correctness, safety or full feature equivalence.",
      "records_path":str(resultfile)}
    (dest/"summary.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)
if __name__=="__main__":main()
