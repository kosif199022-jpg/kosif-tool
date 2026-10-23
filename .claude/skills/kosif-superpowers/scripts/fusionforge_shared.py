#!/usr/bin/env python3
"""FusionForge shared learning: publish ONLY independently QA-verified, human-reviewed, sanitized workflow structures.

This is an optional companion to FusionForge v2 (it does not change v2 project-private behavior).
Run from the kosif-tool repo root:
  python3 .claude/skills/kosif-superpowers/scripts/fusionforge_shared.py audit
  python3 .claude/skills/kosif-superpowers/scripts/fusionforge_shared.py review-template --signature <sha256> \
      > out/fusionforge/_shared/reviews/<sha256>.json      # blank review to fill in by a human, then approve
  python3 .claude/skills/kosif-superpowers/scripts/fusionforge_shared.py approve --signature <sha256>
  python3 .claude/skills/kosif-superpowers/scripts/fusionforge_shared.py recall --kind video

Source recipes and proposals remain under out/fusionforge/<project>/. Cross-project reuse reads ONLY
out/fusionforge/_shared/registry.json, which contains neither goals, project names, user text,
paths, evidence, secrets, traces, nor observed results. No automatic approval or transfer.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
from collections import defaultdict
from types import SimpleNamespace
from pathlib import Path

SCHEMA = 'kosif.fusionforge.shared.v1'
RX_PROJECT = re.compile(r'[A-Za-z0-9_-]{1,70}\Z')
RX_ID = re.compile(r'FUSE-[0-9]{8}-[0-9a-f]{10}\Z')
RX_SHA = re.compile(r'[0-9a-f]{64}\Z')
RX_PROOF = re.compile(r'evidence/[0-9a-f]{64}(?:\.[a-z0-9]{1,10})?\Z')
RX_EXEC = re.compile(r'(?:human|(?:tool|bin|method|mcp):[A-Za-z0-9_./+-]{1,110})\Z')
STAGES = {'understand','research','plan','build','create','refine','assemble','verify','deliver'}
KINDS = {'brief','spec','plan','sources','code','dataset','report','document','image','audio','video',
         'model3d','font','prompt','evidence','package','any'}
RELATIONS = {'sequence','parallel','complement','substitute','verify','refine','fallback'}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read(path: Path, limit: int = 4_000_000) -> dict:
    if path.is_symlink() or not path.is_file() or path.stat().st_size > limit:
        raise ValueError('invalid file')
    value = json.loads(path.read_text('utf-8'))
    if not isinstance(value, dict):
        raise ValueError('expected JSON object')
    return value


def signature(proposal: dict) -> str:
    s = proposal.get('sanitized') or {}
    ns, es = s.get('nodes'), s.get('edges')
    if not isinstance(ns, list) or not ns or not isinstance(es, list):
        raise ValueError('invalid graph')
    keep = []
    for n in ns:
        if not isinstance(n, dict) or n.get('stage') not in STAGES or not RX_EXEC.fullmatch(str(n.get('executor',''))):
            raise ValueError('invalid node')
        if not isinstance(n.get('inputs'), list) or not isinstance(n.get('outputs'), list):
            raise ValueError('bad node ports')
        if any(k not in KINDS for k in n['inputs']+n['outputs']):
            raise ValueError('unknown artifact kind')
        keep.append([n['stage'], n['executor'], n['inputs'], n['outputs']])
    for e in es:
        if (not isinstance(e, list) or len(e) != 4 or e[0] not in STAGES or e[1] not in STAGES
                or e[2] not in KINDS or e[3] not in RELATIONS):
            raise ValueError('invalid edge')
    raw = json.dumps([sorted(keep), sorted(es)], sort_keys=True).encode('utf-8')
    return digest(raw)


def from_recipe(recipe: dict) -> dict:
    """Reconstruct precisely the private engine's promotion graph, excluding lesson strings."""
    chosen=(recipe.get('plan_choice') or {}).get('nodes') or []
    nodes={n['id']:n for n in recipe.get('nodes',[]) if isinstance(n,dict) and isinstance(n.get('id'),str)}
    if not chosen or any(k not in nodes for k in chosen):
        raise ValueError('invalid chosen nodes')
    caps=recipe.get('capabilities') or {}
    snodes=[]
    for nid in chosen:
        n=nodes[nid]
        snodes.append({'stage':n['stage'],'executor':n['executor']['ref'],
            'capabilities':[{'name_en':(caps.get(c) or {}).get('name_en'),
                'atoms_sha256':(caps.get(c) or {}).get('atoms_sha256')}
                for c in n.get('capability_ids',[])],
            'inputs':sorted(p['kind'] for p in n['inputs']),
            'outputs':sorted(p['kind'] for p in n['outputs']),
            'acceptance':n.get('acceptance','')})
    selected=set(chosen)
    sedges=sorted([nodes[e['from']]['stage'],nodes[e['to']]['stage'],e['kind'],e['relation']]
        for e in recipe.get('edges',[]) if isinstance(e,dict) and e.get('from') in selected and e.get('to') in selected)
    return {'nodes':snodes,'edges':sedges}


def proof_valid(space: Path, evidence: dict) -> bool:
    if not isinstance(evidence, dict) or not RX_SHA.fullmatch(str(evidence.get('sha256',''))):
        return False
    stored = evidence.get('stored')
    if not isinstance(stored, str) or not RX_PROOF.fullmatch(stored):
        return False  # require copied local proof: not a remote-only or private absolute path
    file = space / stored
    if file.is_symlink() or not file.is_file() or file.stat().st_size > 5_242_880:
        return False
    return digest(file.read_bytes()) == evidence['sha256']


def verified_record(space: Path, recipe: dict, expected_id: str) -> str | None:
    """Return a unique local QA hash only if the recorded chosen workflow was executed and verified."""
    if (recipe.get('id') != expected_id or recipe.get('project') != space.name or recipe.get('status') != 'verified'
            or recipe.get('imported') or recipe.get('migrated_from') or recipe.get('legacy_unproven')):
        return None
    choice = recipe.get('plan_choice') or {}
    selected = choice.get('nodes') or []
    nodes = {n.get('id'): n for n in recipe.get('nodes',[]) if isinstance(n,dict)}
    traces = {t.get('seq'): t for t in recipe.get('traces',[]) if isinstance(t,dict)}
    if not selected or any(n not in nodes or nodes[n].get('status') not in ('passed','skipped') for n in selected):
        return None
    if not any(s.get('to') == 'verified' and s.get('evidence_sha256') for s in recipe.get('status_log',[]) if isinstance(s,dict)):
        return None
    if not any(e.get('status') == 'verified' and proof_valid(space,e) for e in recipe.get('evidence',[]) if isinstance(e,dict)):
        return None
    for nid in selected:
        n = nodes[nid]
        if n.get('stage') != 'verify' or n.get('status') != 'passed':
            continue
        t = traces.get(n.get('last_trace')) or {}
        if t.get('node') == nid and t.get('result') == 'passed' and proof_valid(space,t.get('evidence')):
            return t['evidence']['sha256']
    return None


def collect(root: Path) -> dict:
    """No data from project-local recipes enters the published registry without all checks."""
    groups: dict[str,list[dict]] = defaultdict(list)
    # Fail closed if the source engine or its full V01-V12 validators are unavailable.
    import fusionforge as engine
    ctx = engine.Ctx(SimpleNamespace(root=str(root), now=None, catalog_file=None, tools_file=None))
    if not root.is_dir():
        return groups
    for space in sorted(root.iterdir()):
        if (not space.is_dir() or space.is_symlink() or space.name == '_shared'
                or not RX_PROJECT.fullmatch(space.name)):
            continue
        proposals = space / 'promotions'
        if not proposals.is_dir() or proposals.is_symlink():
            continue
        for p in proposals.glob('FUSE-*.proposal.json'):
            try:
                rid = p.name.removesuffix('.proposal.json')
                if not RX_ID.fullmatch(rid):
                    continue
                prop = read(p)
                if prop.get('schema') != 'kosif.fusionforge.promotion.v2' or prop.get('recipe_id') != rid:
                    continue
                sig = signature(prop)
                if sig != prop.get('graph_signature'):
                    continue
                recipe = read(space/'recipes'/f'{rid}.json')
                if prop['sanitized']['nodes'] != from_recipe(recipe)['nodes'] or prop['sanitized']['edges'] != from_recipe(recipe)['edges']:
                    continue
                qa_hash = verified_record(space,recipe,rid)
                if not qa_hash:
                    continue
                check = engine.validate_recipe(ctx,space,recipe)
                drift=check.get('drift') or {}
                if check['errors'] or drift.get('stale') or drift.get('unknown'):
                    continue
                engine.proven_here(ctx,space,recipe,check)
                groups[sig].append({'project':space.name,'id':rid,'qa_hash':qa_hash,'proposal':prop})
            except (OSError,ValueError,TypeError,KeyError,engine.FFError):
                continue
    return groups


def tier(rows: list[dict]) -> dict:
    # Repeated copies of the same QA output count once, even if renamed.
    distinct = {}
    for r in rows:
        distinct.setdefault(r['qa_hash'], r)
    clean = list(distinct.values())
    projects = len({r['project'] for r in clean})
    n = len(clean)
    status = ('shared_eligible' if n>=3 and projects>=3 else
              'local_trusted' if n>=2 else 'experimental' if n==1 else 'unproven')
    return {'tier':status,'independent_tests':n,'independent_projects':projects}


def public_graph(proposal: dict) -> dict:
    """Strictly allowlisted structural data; user text and project identifiers cannot leak."""
    signature(proposal)  # validates all port types, stage/executor enums and edges
    nodes = []
    for n in proposal['sanitized']['nodes']:
        atoms = []
        for c in n.get('capabilities',[]):
            atom = c.get('atoms_sha256') if isinstance(c,dict) else None
            if atom and RX_SHA.fullmatch(str(atom)):
                atoms.append(atom)
        nodes.append({'stage':n['stage'],'executor':n['executor'],
                      'inputs':sorted(n['inputs']),'outputs':sorted(n['outputs']),
                      'capability_fingerprints':sorted(set(atoms))})
    edges = [list(x) for x in proposal['sanitized']['edges']]
    return {'nodes':nodes,'edges':sorted(edges),'artifact_kinds':sorted({k for n in nodes for k in n['outputs'] if k not in ('any','evidence','package')})}


def approved_review(path: Path, sig: str) -> dict:
    rev=read(path, 16_384)
    required=('independent_qa','security_review','catalog_collision_check','privacy_review')
    if rev.get('signature')!=sig or rev.get('decision')!='approve' or any(rev.get(x) is not True for x in required):
        raise ValueError('all independent, security, catalog and privacy reviews must be approved')
    if not isinstance(rev.get('reviewer'),str) or not (2<=len(rev['reviewer'])<=100):
        raise ValueError('reviewer required')
    scenarios=rev.get('scenarios')
    if not isinstance(scenarios,list) or len(set(map(str,scenarios)))<3:
        raise ValueError('three distinct QA scenarios required')
    comparison=rev.get('baseline_comparison')
    if not isinstance(comparison,dict) or comparison.get('direction') not in ('higher','lower'):
        raise ValueError('baseline metric missing')
    a,b=comparison.get('baseline'),comparison.get('candidate')
    if not all(type(v) in (int,float) and abs(v)<1e12 for v in (a,b)):
        raise ValueError('baseline numbers invalid')
    if not (b>a if comparison['direction']=='higher' else b<a):
        raise ValueError('candidate did not outperform baseline')
    return {'reviewed':True,'improvement_direction':comparison['direction']}


def write_atomic(path: Path, obj: dict) -> None:
    if path.parent.is_symlink():
        raise ValueError('refusing symlinked registry parent')
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.is_symlink():
        raise ValueError('refusing symlinked registry')
    fd,tmp=tempfile.mkstemp(dir=str(path.parent),prefix='.registry-',suffix='.tmp')
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as f:
            json.dump(obj,f,ensure_ascii=False,indent=2,sort_keys=True)
            f.write('\n')
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def registry(root: Path) -> dict:
    p=root/'_shared'/'registry.json'
    if p.parent.is_symlink():
        raise ValueError('refusing symlinked shared folder')
    if not p.exists():
        return {'schema':SCHEMA,'items':{}}
    obj=read(p)
    if obj.get('schema')!=SCHEMA or not isinstance(obj.get('items'),dict):
        raise ValueError('unknown registry schema')
    return obj


def main(argv=None) -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',default=os.environ.get('KOSIF_FUSIONFORGE_ROOT','out/fusionforge'))
    sp=p.add_subparsers(dest='cmd',required=True)
    sp.add_parser('audit')
    a=sp.add_parser('approve');a.add_argument('--signature',required=True)
    a=sp.add_parser('recall');a.add_argument('--kind',required=True,choices=sorted(KINDS))
    a=sp.add_parser('review-template');a.add_argument('--signature',required=True)
    args=p.parse_args(argv)
    root=Path(args.root).expanduser().resolve()
    try:
        if args.cmd == 'recall':
            approved=registry(root)['items']
            matches=[dict(signature=k,**v) for k,v in sorted(approved.items()) if args.kind in v.get('graph',{}).get('artifact_kinds',[])]
            print(json.dumps({'approved_matches':matches},ensure_ascii=False,indent=2))
            return 0
        if args.cmd == 'review-template':
            if not RX_SHA.fullmatch(args.signature):raise ValueError('invalid signature')
            print(json.dumps({'signature':args.signature,'decision':'pending','reviewer':'',
                'independent_qa':False,'security_review':False,'privacy_review':False,
                'catalog_collision_check':False,'scenarios':[],
                'baseline_comparison':{'metric':'','direction':'higher','baseline':None,'candidate':None}},indent=2))
            return 0
        found=collect(root)
        report={sig:tier(rows) for sig,rows in sorted(found.items())}
        if args.cmd=='audit':
            print(json.dumps({'signatures':report,'approved_count':len(registry(root)['items'])},ensure_ascii=False,indent=2))
            return 0
        sig=args.signature
        if not RX_SHA.fullmatch(sig):raise ValueError('invalid signature')
        if sig not in found or report[sig]['tier']!='shared_eligible':
            raise ValueError('need three independently proven recipes in three isolated projects')
        review=root/'_shared'/'reviews'/f'{sig}.json'
        if review.parent.is_symlink() or review.parent.parent.is_symlink():
            raise ValueError('refusing symlinked review folder')
        approved_review(review,sig)
        # Match invariant: all proposals under one signature have the same typed graph.
        graphs=[public_graph(r['proposal']) for r in found[sig]]
        if any(g!=graphs[0] for g in graphs[1:]):
            raise ValueError('sanitized graphs disagree')
        reg=registry(root)
        if sig in reg['items']:
            print(json.dumps({'status':'already_approved','signature':sig}))
            return 0
        reg['items'][sig]={'tier':'shared_approved','independent_tests':report[sig]['independent_tests'],
                          'independent_projects':report[sig]['independent_projects'],'graph':graphs[0]}
        write_atomic(root/'_shared'/'registry.json',reg)
        print(json.dumps({'status':'shared_approved','signature':sig}))
        return 0
    except (ValueError,OSError,TypeError,ImportError) as exc:
        print(f'fusionforge-shared: REJECTED: {exc}',file=__import__('sys').stderr)
        return 2

if __name__=='__main__':
    raise SystemExit(main())
