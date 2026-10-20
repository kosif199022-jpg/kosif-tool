#!/usr/bin/env python3
"""Stratified read-only Atlas source review for KOSIF Superpowers.

Never imports, executes, installs, or follows instructions in third-party skills.
Use 'plan' before sparse-checking out selected sources and 'audit' afterward.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import sys

from atlas_deep_fusion import DOMAINS, _load, _row_ok, _validate_path

SCHEMA = "kosif.atlas.stratified-review.v2"
WARNINGS = {
    "one_liner_install": re.compile(r"(?:curl|wget)\s+[^\r\n|]{0,250}\|\s*(?:ba)?sh|iwr\s+.{0,250}\|\s*iex", re.I),
    "disable_protection": re.compile(r"disable.{0,35}(?:antivirus|defender|firewall|security)|turn off.{0,30}(?:safety|security)", re.I),
    "remote_command": re.compile(r"(?:powershell|pwsh)\s+-enc(?:odedcommand)?|(?:base64\s+-d|base64\.b64decode)\s*", re.I),
    "destructive_shell": re.compile(r"rm\s+-rf\s+[~/]|Remove-Item\s+.{0,80}-Recurse", re.I),
    "credential_reference": re.compile(r"\b(?:ANTHROPIC_API_KEY|OPENAI_API_KEY|GITHUB_TOKEN|AWS_SECRET_ACCESS_KEY|password)\b", re.I),
    "prompt_override_language": re.compile(r"ignore\s+(?:all\s+)?previous\s+instructions|system\s+prompt|bypass\s+permissions", re.I),
    "data_upload_instruction": re.compile(r"(?:upload|send|post).{0,65}(?:credential|private key|secret token)", re.I),
}
EXT_SCRIPT = {".py",".js",".mjs",".sh",".ps1",".bat",".cmd",".exe",".dll",".wasm",".jar",".so",".dylib"}
SOURCE_LIMIT = 500_000
REGEX_LIMIT = 150_000

def hits(row, words):
    text=(str(row.get("skill",""))+" "+str(row.get("description",""))).lower()
    return sum(1 for w in words if w.lower() in text)

def select(main, copy, per_domain=24, risky_per_domain=8, copyleft_limit=15):
    selected=[]
    seen=set()
    for domain,words in DOMAINS.items():
        ranked=sorted(main["skills"],key=lambda r:(-hits(r,words),str(r.get("skill","")),str(r.get("id",""))))
        eligible=[r for r in ranked if hits(r,words) and _row_ok(r)]
        review=[r for r in ranked if hits(r,words) and not _row_ok(r)]
        for group,budget in ((eligible,per_domain),(review,risky_per_domain)):
            count=0
            for row in group:
                if count>=budget: break
                path=str(row.get("path",""))
                if path in seen or _validate_path(Path("."),path) is None: continue
                selected.append({"scope":"main","domain":domain,"id":row.get("id"),"skill":row.get("skill"),
                    "path":path,"source":row.get("source"),"license":row.get("license"),
                    "verdict":row.get("verdict"),"complete":row.get("complete"),
                    "risk_flags":row.get("risk_flags") or [],"file_count_claimed":len(row.get("files") or [])})
                seen.add(path)
                count+=1
    c=0
    for row in sorted(copy["skills"],key=lambda r:(str(r.get("skill","")),str(r.get("id","")))):
        if c>=copyleft_limit: break
        path=str(row.get("path",""))
        if path in seen or _validate_path(Path("."),path) is None:continue
        selected.append({"scope":"copyleft_reference_only","domain":"license-review","id":row.get("id"),
            "skill":row.get("skill"),"path":path,"source":row.get("source"),"license":row.get("license"),
            "verdict":row.get("verdict"),"complete":row.get("complete"),
            "risk_flags":row.get("risk_flags") or [],"file_count_claimed":len(row.get("files") or [])})
        seen.add(path)
        c+=1
    return selected

def overview(main,copy):
    allrows=main["skills"]+copy["skills"]
    names=defaultdict(list); descriptions=Counter(); licenses=Counter(); status=Counter()
    missing_meta=Counter(); risks=Counter(); claimed_file_total=0; complete=0
    for row in allrows:
        names[str(row.get("skill","")).casefold().strip()].append(str(row.get("path","")))
        descriptions[str(row.get("description","")).casefold().strip()]+=1
        licenses[str(row.get("license","unknown"))]+=1
        status[str(row.get("verdict","unknown"))]+=1
        claimed_file_total+=len(row.get("files") or [])
        complete+=int(row.get("complete") is True)
        for f in ("skill","description","path","source","license","verdict"):
            if not row.get(f):missing_meta[f]+=1
        for r in row.get("risk_flags") or []:risks[str(r)]+=1
    duplicate_names={k:len(v) for k,v in names.items() if k and len(v)>1}
    return {
        "total":len(allrows),"main":len(main["skills"]),"copyleft":len(copy["skills"]),
        "unique_normalized_skill_names":len(names),
        "reused_names":len(duplicate_names),
        "records_in_reused_names":sum(duplicate_names.values()),
        "most_reused_names":dict(Counter(duplicate_names).most_common(24)),
        "duplicate_description_groups":sum(v>1 for v in descriptions.values() if v),
        "records_in_duplicate_descriptions":sum(v for k,v in descriptions.items() if k and v>1),
        "claimed_complete_folders":complete,
        "claimed_file_count_sum":claimed_file_total,
        "license_labels":dict(licenses.most_common()),"verdicts":dict(status),
        "risk_flags":dict(risks.most_common()),
        "missing_metadata_fields":dict(missing_meta),
        "confirmed_executable_skills":0,"confirmed_safe_skills":0
    }

def _read_source(root,entry):
    p=_validate_path(root,entry["path"])
    if not p:return {"state":"rejected_path"}
    # Reject symbolic links and files outside checkout by inspecting the full path.
    current=p
    while current != Path(root).resolve() and current != current.parent:
        if current.is_symlink():return {"state":"rejected_symlink"}
        current=current.parent
    if not p.is_file():return {"state":"not_checked_out"}
    size=p.stat().st_size
    if size>SOURCE_LIMIT:return {"state":"skipped_large_file","bytes":size}
    raw=p.read_bytes()
    content=raw.decode("utf-8-sig",errors="replace")
    limited=content[:REGEX_LIMIT]
    flags=[name for name,rx in WARNINGS.items() if rx.search(limited)]
    top=content[:4096]
    heading_titles=re.findall(r"(?m)^#{1,3}\s+(.{1,110})$",limited)
    skill_dir=p.parent
    scripts=0
    source_note=False
    seen_relative_count=0
    # This only inspects direct file/directory names; never traverses or executes scripts.
    try:
        for child in skill_dir.iterdir():
            seen_relative_count+=1
            if seen_relative_count>250:break
            if child.is_file() and child.suffix.lower() in EXT_SCRIPT:scripts+=1
        plug=skill_dir.parent
        source_note=(plug/"SOURCE.md").is_file()
    except (PermissionError,OSError):pass
    has_frontmatter=content.lstrip("\ufeff").startswith("---\n")
    declared_name=re.search(r"(?m)^name:\s*(.{1,150})\s*$",top)
    declared_desc=re.search(r"(?m)^description:\s*(.{1,200})\s*$",top)
    md_links=re.findall(r"\]\(([^)]+)\)",limited)
    relative_refs=sum(1 for x in md_links if not x.startswith(("http://","https://","#","mailto:")))
    external_urls=len(re.findall(r"https?://[^\s<>\]\)\"']+",limited))
    has_recipes=bool(re.search(r"(?im)^\s*(?:##\s+(?:usage|workflow|procedure|examples|how to|steps|instructions)|(?:step\s+\d+|الخطوة\s+\d+))",limited))
    return {
        "state":"text_inspected_not_executed","sha256":hashlib.sha256(raw).hexdigest(),
        "size_bytes":len(raw),"line_count":content.count("\n")+1,
        "frontmatter_present":has_frontmatter,
        "frontmatter_name_matches":bool(declared_name and declared_name.group(1).strip().strip("'\"").casefold()==str(entry["skill"]).casefold()),
        "frontmatter_description_present":bool(declared_desc),
        "source_note_found":source_note,"headings":heading_titles[:12],
        "headings_count":len(heading_titles),"warnings":flags,
        "source_direct_scripts_count":scripts,
        "referenced_relative_links_count":relative_refs,
        "external_url_count":external_urls,
        "has_instructional_procedure_pattern":has_recipes,
        "classification":"manual_review_required" if flags or entry["scope"]!="main" or not _row_ok(entry) else "potential_guidance_candidate_not_verified"
    }

def audit(root,plan,meta):
    stats=Counter()
    inspected=[]
    for row in plan["selected"]:
        reading=_read_source(root,row)
        stats[reading["state"]]+=1
        for flag in reading.get("warnings",[]):stats["warning:"+flag]+=1
        inspected.append({**row,"source_audit":reading})
    return {
        "schema":SCHEMA,"mode":"audit","atlas_index_sha256":plan["atlas_index_sha256"],
        "catalog":meta,"source_sample_plan_size":len(plan["selected"]),
        "static_audit_counts":dict(stats),
        "audited_files":inspected,
        "execution_receipts":0,
        "claim_limit":"Read-only source-text sampling only; not all files and not dynamic verification. Never auto-install or run third-party skills."
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("mode",choices=["plan","audit"])
    p.add_argument("--index",required=True,type=Path)
    p.add_argument("--copyleft",required=True,type=Path)
    p.add_argument("--root",type=Path)
    p.add_argument("--plan-file",type=Path)
    p.add_argument("--output",required=True,type=Path)
    p.add_argument("--per-domain",type=int,default=24)
    p.add_argument("--risky-per-domain",type=int,default=8)
    p.add_argument("--copyleft-limit",type=int,default=15)
    args=p.parse_args()
    main,h1=_load(args.index);copy,h2=_load(args.copyleft)
    meta=overview(main,copy)
    if args.mode=="plan":
        if not 1<=args.per_domain<=70 or not 0<=args.risky_per_domain<=30 or not 0<=args.copyleft_limit<=85:
            p.error("sampling limits out of bounds")
        result={"schema":SCHEMA,"mode":"plan","atlas_index_sha256":{"main":h1,"copyleft":h2},
          "catalog":meta,"selected":select(main,copy,args.per_domain,args.risky_per_domain,args.copyleft_limit),
          "selection_note":"Stratified sample, not a full 14,793-source review."}
    else:
        if not args.root or not args.plan_file:p.error("audit needs --root and --plan-file")
        plan=json.loads(args.plan_file.read_text(encoding="utf-8-sig"))
        if plan.get("schema")!=SCHEMA or plan.get("mode")!="plan" or plan["atlas_index_sha256"]!={"main":h1,"copyleft":h2}:
            raise ValueError("stale/invalid plan or source index changed")
        result=audit(args.root,plan,meta)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"mode":args.mode,"total":meta["total"],"sample_count":len(result.get("selected",result.get("audited_files",[]))),"stats":result.get("static_audit_counts"),"output":str(args.output)},ensure_ascii=False))
if __name__=="__main__":
    try:main()
    except (OSError,ValueError,KeyError,TypeError,json.JSONDecodeError) as exc:
        print(type(exc).__name__+": "+str(exc),file=sys.stderr);sys.exit(2)
