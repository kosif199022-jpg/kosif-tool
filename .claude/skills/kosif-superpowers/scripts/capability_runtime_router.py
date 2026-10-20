#!/usr/bin/env python3
"""KOSIF capability-first router: precise runbooks, real preflight and permission ledger.

Read-only. No network, no subprocess, no package installs, no account access.
Always distinguishes source files, host prerequisites, user consent, and execution.
Python 3.8+ standard library. Use at the START of a Claude skill session.
"""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "data" / "capability_routes.json"
MAX_RECORDS = 100

def load_registry(path=CATALOG):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema") != "kosif.capability-routes.v1":
        raise ValueError("wrong capability routing schema")
    routes = data.get("routes")
    if not isinstance(routes, list) or not 1 <= len(routes) <= MAX_RECORDS:
        raise ValueError("routes list missing or too long")
    unique = set()
    for entry in routes:
        if not isinstance(entry, dict):
            raise ValueError("route must be object")
        ident = entry.get("id")
        if not isinstance(ident, str) or not re.fullmatch("[a-z0-9]+(?:-[a-z0-9]+)*", ident) or ident in unique:
            raise ValueError("invalid/duplicate capability id")
        unique.add(ident)
        if not isinstance(entry.get("title"), str) or not entry["title"]:
            raise ValueError("missing route title")
        aliases = entry.get("aliases")
        if not isinstance(aliases, list) or not aliases or len(aliases)>40 or any(not isinstance(x,str) or not x or len(x)>100 for x in aliases):
            raise ValueError("invalid route aliases")
        script = entry.get("script")
        if script is not None:
            if not isinstance(script, str) or not re.fullmatch(r"scripts/[a-z0-9_]+\.py",script):
                raise ValueError("local script path outside approved skill scripts directory")
        for key in ("requires","permissions"):
            values = entry.get(key)
            if not isinstance(values, list) or len(values)>30 or any(not isinstance(x,str) or not re.fullmatch(r"[A-Za-z0-9_.-]+",x) for x in values):
                raise ValueError("invalid requirement or permission")
        for key in ("summary","proof"):
            if not isinstance(entry.get(key),str) or not entry[key]:
                raise ValueError("missing "+key)
    return routes

def _ready_tools(required):
    present,missing = [],[]
    for exe in required:
        # Never infer that a Python import means a model's weights exist.
        # Other requirements are CLI names, not shell fragments.
        if shutil.which(exe): present.append(exe)
        else: missing.append(exe)
    return present,missing

def assess(entry, skill_root=ROOT):
    script = entry.get("script")
    source = (Path(skill_root) / script).is_file() if script else False
    present,missing = _ready_tools(entry["requires"])
    # This is DISCOVERY, never execution: no auth or credentials can be proved
    # by a catalogue or by an opt-in flag.
    if not script:
        status = "external_not_integrated"
    elif not source:
        status = "source_file_missing"
    elif missing:
        status = "missing_host_prerequisites"
    else:
        status = "source_present_not_executed"
    return {
        "id":entry["id"], "title":entry["title"], "purpose":entry["title"], "note":entry["summary"],
        "status":status, "source_present":bool(source),
        "present_binaries":present, "missing_binaries":missing,
        "runbook":("python3 \"$SKILL_DIR/"+script+"\" "+(entry.get("subcommand") or "")).strip() if script else None,
        "permissions_required_not_granted":entry["permissions"],
        "permission_status":"not_verified_requires_host_or_user_authorization",
        "external_source_optional":entry.get("external") or None,
        "test_or_postcondition":entry["proof"],
        "executed_in_current_request":False,
        "verified_in_current_request":False,
    }

def _normalize(s):
    return " ".join(re.findall(r"[\w\u0600-\u06ff]+", s.casefold(), flags=re.UNICODE))

def route(task, entries, limit=5, skill_root=ROOT):
    if not isinstance(task,str) or not task.strip() or len(task)>500:
        raise ValueError("task must be 1..500 characters")
    cleaned=_normalize(task)
    terms=set(cleaned.split())
    scored=[]
    for row in entries:
        score=0
        hits=[]
        for alias in row["aliases"]:
            needle=_normalize(alias)
            if not needle:continue
            if needle in cleaned and (len(needle.split())>1 or needle==cleaned):
                weight=12 if len(needle.split())>1 else 8
            else:
                token=set(needle.split())
                weight=2 if token and token.issubset(terms) else 0
            if weight:
                score+=weight
                hits.append(alias)
        if score:
            scored.append((score,row["id"],row,hits))
    scored.sort(key=lambda x:(-x[0],x[1]))
    return [{"relevance_score":score,"matched":hits[:8],**assess(row,skill_root)}
            for score,_,row,hits in scored[:limit]]

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    g=ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--task",help="task in Arabic/English; recommend matching executable skills")
    g.add_argument("--id",help="inspect exact capability ID")
    g.add_argument("--doctor",action="store_true",help="inspect all registered capability prerequisites")
    g.add_argument("--list",action="store_true",help="show the declared capability names")
    ap.add_argument("--limit",type=int,default=5)
    ap.add_argument("--json",action="store_true",help="machine-readable output; safe default")
    args=ap.parse_args(argv)
    try:
        records=load_registry()
        if not 1 <= args.limit <= 20:
            raise ValueError("limit must be 1..20")
        if args.list:
            output={"schema":"kosif.capability-list.v1","count":len(records),
                    "capabilities":[{"id":r["id"],"title":r["title"]} for r in records]}
        elif args.doctor:
            output={"schema":"kosif.capability-doctor.v1",
                    "count":len(records),
                    "probes":[assess(r) for r in records],
                    "important":"Host tools, user permissions and verified media outputs cannot be inferred from this report"}
        elif args.id:
            item=next((r for r in records if r["id"]==args.id),None)
            if not item: raise ValueError("unknown capability ID")
            output={"schema":"kosif.capability-inspection.v1",**assess(item)}
        else:
            output={"schema":"kosif.capability-routing.v1","task":args.task,
                    "choices":route(args.task,records,args.limit),
                    "important":"A source file is not a completed action; obtain permission, run, verify outputs"}
        print(json.dumps(output,indent=2,ensure_ascii=False))
        return 0
    except (ValueError,OSError,json.JSONDecodeError) as exc:
        print(json.dumps({"status":"failed","error":str(exc)},ensure_ascii=False),file=sys.stderr)
        return 2

if __name__=="__main__":
    sys.exit(main())
