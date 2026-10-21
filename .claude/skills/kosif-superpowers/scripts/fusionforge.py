#!/usr/bin/env python3
"""KOSIF FusionForge: compose catalog superpowers into project-scoped, evidence-based reusable recipes.

From repository root:
  python3 .claude/skills/kosif-superpowers/scripts/fusionforge.py propose "طلبك" --project project_id
  python3 .claude/skills/kosif-superpowers/scripts/fusionforge.py record --project project_id --id FUSE-... --status tested --evidence QA.json
  python3 .claude/skills/kosif-superpowers/scripts/fusionforge.py record --project project_id --id FUSE-... --status verified --evidence QA.json --qa-pass
  python3 .claude/skills/kosif-superpowers/scripts/fusionforge.py trace --project project_id --id FUSE-... --stage create --action "Executed renderer" --tool ffmpeg --evidence frame.png
  python3 .claude/skills/kosif-superpowers/scripts/fusionforge.py catalog --project project_id
  python3 .claude/skills/kosif-superpowers/scripts/fusionforge.py show --project project_id --id FUSE-...

Uses only Python stdlib; does not execute powers, install tools, contact external models,
auto-promote to global catalogs or publish project records. Human/model creative review
refines generated workflow proposals. Verified means caller asserted QA with file evidence.
"""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
import re
import uuid
from collections import Counter
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
REPO = SKILL.parents[2] if len(SKILL.parents) > 2 else SKILL
CATALOG = SKILL / "data" / "superpowers.json"
DEFAULT_ROOT = REPO / "out" / "fusionforge"
BRIDGE = {
    "فيديو": "video montage motion cinematic render", "مونتاج": "video montage cut motion render",
    "صوت": "audio speech synchronization voice", "الصوت": "audio speech voice sync",
    "رسم": "svg illustration animation", "تحريك": "motion animation", "خطوط": "fonts typography arabic",
    "محاسبة": "accounting finance reconciliation", "مخزون": "inventory data accounting",
    "برمجة": "code engineering software", "تطبيق": "app application code design",
    "توليف": "fusion skills capability integration", "مهارات": "skill capability methods",
    "بحث": "research evidence", "خطة": "planning strategy", "اختبار": "quality tests verification"
}
STOP = set("the and for with from this that into make your في من على عايز اعمل اريد ابي بشكل".split())
ROLE = {"mind":"plan","strategy":"plan","research":"research","craft":"create",
        "code":"build","build":"build","data":"verify","docs":"deliver",
        "media":"create","motion":"create"}
STAGES = ("understand", "research", "plan", "build", "create", "refine", "verify", "deliver")
ID_PATTERN = r"FUSE-[0-9]{8}-[0-9a-f]{10}"

def words(value):
    raw = str(value or "").lower().replace("أ","ا").replace("إ","ا").replace("آ","ا")
    found = re.findall(r"[a-z][a-z0-9+#-]{2,}|[\u0621-\u064a]{3,}",raw)
    extra = " ".join(BRIDGE.get(w,"") for w in found)
    return {w for w in found+extra.split() if w not in STOP}

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

def space_for(args):
    if not re.fullmatch(r"[a-zA-Z0-9_-]{1,70}",args.project):
        raise ValueError("Invalid project ID (letters/numbers/_/- only)")
    return (Path(args.root)/args.project).resolve()

def recipe_path(space, rid):
    if not re.fullmatch(ID_PATTERN, rid):
        raise ValueError("Invalid recipe ID")
    return space/"recipes"/(rid+".json")

def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def refresh_index(space):
    recipes=[]
    for path in sorted((space/"recipes").glob("FUSE-*.json")):
        item=read(path)
        recipes.append({"id":item["id"],"goal":item["goal"],"status":item["status"],
                        "capability_count":len(item.get("capabilities",[])),
                        "evidence_count":len(item.get("evidence",[])),
                        "path":str(path.relative_to(space))})
    index={"schema":"kosif.fusionforge.index.v1","project":space.name,
           "total":len(recipes),"verified":sum(r["status"]=="verified" for r in recipes),
           "recipes":recipes}
    save(space/"index.json",index)
    return index

def shortlist(query,data,pool):
    q=words(query)
    ranked=[]
    for item in data.get("items",[]):
        label=" ".join([str(item.get("name_en","")),str(item.get("name_ar","")),
                        " ".join(item.get("focus",[])),
                        " ".join(item.get("families",{}).keys())])
        hits=len(q & words(label))
        if not hits:
            continue
        readiness=float(item.get("ready_now",0))/max(1,float(item.get("size",1)))
        ranked.append((round(10*hits/max(1,len(q)**0.5)+2*readiness,4),item))
    return sorted(ranked,key=lambda x:(-x[0],x[1]["id"]))[:pool]

def propose(args):
    data=read(Path(args.catalog_file))
    space=space_for(args)
    ranked=shortlist(args.goal,data,args.pool)
    prior=[]
    for p in (space/"recipes").glob("FUSE-*.json"):
        old=read(p)
        if old.get("status")!="verified":
            continue
        a,b=words(args.goal),words(old.get("goal",""))
        sim=len(a & b)/max(1,len(a | b))
        if sim>=0.20:
            prior.append((sim,old))
    prior.sort(key=lambda x:(-x[0],x[1]["id"]))
    remembered={c.get("id") for _,r in prior[:3] for c in r.get("capabilities",[])}
    ranked.sort(key=lambda x:(-(x[0]+(4 if x[1]["id"] in remembered else 0)),x[1]["id"]))
    if not ranked:
        raise ValueError("No grounded matching superpowers; refine keywords or inspect catalog.")
    selected,domain_counts=[],Counter()
    for score,s in ranked:
        domain=s.get("domain","unknown")
        if domain_counts[domain]>=max(3,args.max_capabilities//3):
            continue
        selected.append({"id":s["id"],"name":s.get("name_ar") or s.get("name_en"),
                         "domain":domain,"role":ROLE.get(domain,"refine"),"match":score,
                         "readiness_catalog_only":s.get("status_mix",{}),
                         "requirements":s.get("requires",[])[:5],
                         "proof_refs":s.get("proof",[])[:3],
                         "execution_state":"not_executed"})
        domain_counts[domain]+=1
        if len(selected)>=args.max_capabilities:
            break
    if not selected:
        raise ValueError("No viable distinct candidate superpowers")
    stages=[{"stage":stage,"capability_ids":[c["id"] for c in selected if c["role"]==stage],
             "input":"task contract or predecessor artifact",
             "output":"observable stage artifact","acceptance":"specific measured check required",
             "status":"not_run"} for stage in STAGES]
    now=dt.datetime.now(dt.timezone.utc).isoformat()
    rid="FUSE-"+dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d")+"-"+uuid.uuid4().hex[:10]
    record={
        "schema":"kosif.fusionforge.recipe.v1","id":rid,"project":args.project,
        "created_at":now,"updated_at":now,"status":"candidate",
        "goal":args.goal,"goal_sha256":hashlib.sha256(args.goal.encode()).hexdigest(),
        "catalog_sha256":hashlib.sha256(Path(args.catalog_file).read_bytes()).hexdigest(),
        "scanned_candidates":len(ranked),"capabilities":selected,"workflow":stages,
        "methods":[{"id":"A","method":"minimal reliable workflow"},
                   {"id":"B","method":"cross-domain new composition + synergy test"},
                   {"id":"C","method":"ambitious professional pipeline + stricter gates"}],
        "lessons_used_same_project_verified_only":[r["id"] for _,r in prior[:3]],
        "source_requirements":["Human review must validate actual node inputs/outputs and owners.",
                               "Test earliest uncertain step before execution.",
                               "Three approaches differ in architecture, not just capability counts."],
        "evidence":[],"observed_outcomes":[],
        "promotion":"project_candidate_only","global_publication":"requires_separate_approval",
        "next_step":"clarify material questions; select A/B/C; build, test, record evidence"
    }
    save(recipe_path(space,rid),record)
    refresh_index(space)
    return record

def trace(args):
    """Append a project-private, step-level workflow observation (not a proof of QA)."""
    space=space_for(args)
    path=recipe_path(space,args.id)
    recipe=read(path)
    if recipe["status"]=="verified":
        raise ValueError("Verified recipes are immutable; create a new experiment")
    if args.stage not in STAGES or not args.action.strip():
        raise ValueError("A valid workflow stage and non-empty action are required")
    fields=" ".join([args.action,args.tool or "",args.input or "",args.output or "",args.observed or ""])
    if re.search(r"(?i)(sk-proj-[a-z0-9_-]{6,}|ghp_[a-z0-9]{10,}|bearer\s+[a-z0-9._-]{12,}|xox[baprs]-)",fields):
        raise ValueError("Refusing likely secrets in execution trace")
    receipt={"stage":args.stage,"action":args.action,"tool":args.tool or "not_reported",
             "input_summary":args.input or "not_reported","output_summary":args.output or "not_reported",
             "observed":args.observed or "not_verified","reported_capability_ids":args.capabilities or [],
             "logged_at":dt.datetime.now(dt.timezone.utc).isoformat(),"evidence":None}
    if args.evidence:
        proof=Path(args.evidence).resolve()
        if not proof.is_file() or not proof.stat().st_size:
            raise ValueError("Evidence must be an existing nonempty file")
        receipt["evidence"]={"local_path":str(proof),
                             "sha256":hashlib.sha256(proof.read_bytes()).hexdigest()}
    recipe.setdefault("execution_trace",[]).append(receipt)
    recipe["updated_at"]=dt.datetime.now(dt.timezone.utc).isoformat()
    save(path,recipe)
    refresh_index(space)
    return receipt

def record(args):
    space=space_for(args)
    path=recipe_path(space,args.id)
    r=read(path)
    if r["status"]=="verified" and args.status!="verified":
        raise ValueError("Verified recipe is frozen; start another experiment")
    if args.status in {"tested","failed","verified"} and not args.evidence:
        raise ValueError("Tested/failed/verified require existing evidence file")
    if args.status=="verified" and not args.qa_pass:
        raise ValueError("Verified status requires --qa-pass; never infer it from prose")
    if args.evidence:
        ev=Path(args.evidence).resolve()
        if not ev.is_file() or ev.stat().st_size==0:
            raise ValueError("Evidence must be a non-empty existing local file")
        r["evidence"].append({"file_local":str(ev),"sha256":hashlib.sha256(ev.read_bytes()).hexdigest(),
                              "status":args.status,"qa_pass_asserted":bool(args.qa_pass),
                              "comment":args.note or "",
                              "recorded_at":dt.datetime.now(dt.timezone.utc).isoformat()})
    r["status"]=args.status
    r["updated_at"]=dt.datetime.now(dt.timezone.utc).isoformat()
    r["next_step"]="Reusable locally, global promotion needs approval" if args.status=="verified" else "Test and preserve evidence"
    save(path,r)
    refresh_index(space)
    return r

def main():
    p=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--root",default=str(DEFAULT_ROOT))
    p.add_argument("--catalog-file",default=str(CATALOG))
    sub=p.add_subparsers(dest="cmd",required=True)
    a=sub.add_parser("propose");a.add_argument("goal");a.add_argument("--project",required=True)
    a.add_argument("--pool",type=int,default=90);a.add_argument("--max-capabilities",type=int,default=24)
    a=sub.add_parser("record");a.add_argument("--project",required=True);a.add_argument("--id",required=True)
    a.add_argument("--status",required=True,choices=("candidate","planned","tested","verified","failed"))
    a.add_argument("--evidence");a.add_argument("--qa-pass",action="store_true");a.add_argument("--note")
    a=sub.add_parser("trace");a.add_argument("--project",required=True);a.add_argument("--id",required=True)
    a.add_argument("--stage",required=True,choices=STAGES)
    a.add_argument("--action",required=True);a.add_argument("--tool")
    a.add_argument("--input");a.add_argument("--output");a.add_argument("--observed")
    a.add_argument("--capabilities",nargs="*");a.add_argument("--evidence")
    a=sub.add_parser("catalog");a.add_argument("--project",required=True)
    a=sub.add_parser("show");a.add_argument("--project",required=True);a.add_argument("--id",required=True)
    args=p.parse_args()
    if args.cmd=="propose":
        if not (1<=args.pool<=300 and 2<=args.max_capabilities<=60):
            raise ValueError("Pool 1..300, max capabilities 2..60")
        result=propose(args)
    elif args.cmd=="record":
        result=record(args)
    elif args.cmd=="trace":
        result=trace(args)
    elif args.cmd=="catalog":
        result=refresh_index(space_for(args))
    else:
        result=read(recipe_path(space_for(args),args.id))
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
