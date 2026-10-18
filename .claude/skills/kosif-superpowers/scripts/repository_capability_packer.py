#!/usr/bin/env python3
"""KOSIF: inspect and safely package repository sources as evidence for capability transfer.

No dynamic code execution, import, install, network access, or auto-promotion to proven skill.
Provides deterministic code-only ZIP exports and machine-readable capability transfer plans.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import zipfile

MAX_ITEMS = 20000
MAX_BYTES = 120 * 1024 * 1024
MAX_MEMBER = 12 * 1024 * 1024
MAX_RATIO = 220
SKIP_NAMES = {'.git', '.hg', '.svn', 'node_modules', '__pycache__', '.next', 'dist', 'build', 'coverage', '.venv', 'venv', '.tox', '.pytest_cache', '.mypy_cache'}
SKIP_FILES = {'.env', '.env.local', '.env.production', 'id_rsa', 'id_ed25519', 'credentials.json', 'secrets.json', '.npmrc', '.pypirc', '.netrc', '.DS_Store'}
SKIP_SUFFIX = {'.pyc', '.pyo', '.zip', '.tar', '.gz', '.7z', '.rar', '.mp4', '.mov', '.webm', '.mp3', '.wav', '.flac', '.exe', '.dll', '.so', '.dylib', '.p12', '.pem', '.key', '.sqlite', '.db'}
EXT_LANG = {'.py':'Python', '.js':'JavaScript', '.mjs':'JavaScript', '.jsx':'JavaScript', '.ts':'TypeScript', '.tsx':'TypeScript', '.rs':'Rust', '.go':'Go', '.html':'HTML', '.css':'CSS', '.svg':'SVG', '.c':'C', '.cpp':'C++', '.java':'Java', '.sh':'Shell'}
SIGNALS = {
 'python': {'paths': ('pyproject.toml', 'setup.py', 'requirements.txt'), 'extensions': ('.py',), 'lesson':'Python package/tool adapter'},
 'javascript': {'paths': ('package.json',), 'extensions': ('.js','.mjs','.ts','.tsx'), 'lesson':'JavaScript runtime adapter'},
 'skill': {'paths': ('SKILL.md', 'skills/'), 'extensions': (), 'lesson':'Skill workflow and invocation rules'},
 'tests': {'paths': ('tests/', 'test/', 'evals/', 'pytest.ini', 'vitest.config.ts'), 'extensions': (), 'lesson':'Executable acceptance and regression tests'},
 'motion': {'paths': ('remotion.config.ts', 'src/compositions/', 'src/Composition.tsx'), 'extensions': (), 'lesson':'Timeline/render integration candidate'},
}

class UnsafeRepository(ValueError): pass

def safe_member(name):
    """Reject traversal/ambiguous ZIP member paths; then decide whether to skip."""
    if not isinstance(name, str) or not name or '\\' in name or '\x00' in name:
        raise UnsafeRepository('invalid path')
    path = PurePosixPath(name)
    if path.is_absolute() or '..' in path.parts or any(':' in p for p in path.parts):
        raise UnsafeRepository('unsafe archive path: ' + name[:100])
    parts = path.parts
    if not parts or any(p in SKIP_NAMES for p in parts): return None
    fname = parts[-1]
    if fname in SKIP_FILES or fname.startswith('.env.') or path.suffix.lower() in SKIP_SUFFIX:
        return None
    return str(path)

def _read_input(source):
    p=Path(source).resolve()
    if not p.exists(): raise FileNotFoundError(p)
    rows=[]; skipped=[]; total=0
    if p.is_dir():
        root=p
        for f in sorted(p.rglob('*')):
            if not f.is_file(): continue
            rel=f.relative_to(root).as_posix()
            target=safe_member(rel)
            if target is None: skipped.append(rel); continue
            if f.is_symlink(): skipped.append(rel); continue
            sz=f.stat().st_size
            if sz>MAX_MEMBER: skipped.append(rel + ': oversize'); continue
            total+=sz
            if total>MAX_BYTES or len(rows)>=MAX_ITEMS: raise UnsafeRepository('repository size/file limit exceeded')
            rows.append((target, f.read_bytes()))
    elif p.is_file() and zipfile.is_zipfile(p):
        with zipfile.ZipFile(p) as z:
            files=[n for n in z.infolist() if not n.is_dir()]
            if len(files)>MAX_ITEMS*3: raise UnsafeRepository('archive has excessive entries')
            seen=set()
            for member in files:
                target=safe_member(member.filename)
                if target is None: skipped.append(member.filename); continue
                if target in seen: raise UnsafeRepository('duplicate member: '+target)
                seen.add(target)
                if ((member.external_attr>>16)&0o170000)==stat.S_IFLNK:
                    skipped.append(target+': symlink'); continue
                if member.file_size>MAX_MEMBER: skipped.append(target+': oversize'); continue
                if member.compress_size and member.file_size/member.compress_size>MAX_RATIO:
                    raise UnsafeRepository('unsafe compression ratio: '+target)
                total+=member.file_size
                if total>MAX_BYTES or len(rows)>=MAX_ITEMS: raise UnsafeRepository('archive expansion/file limit exceeded')
                data=z.read(member)
                if len(data)!=member.file_size: raise UnsafeRepository('size mismatch')
                rows.append((target,data))
        # GitHub source archives typically contain one generated enclosing folder.
        first={r[0].split('/',1)[0] for r in rows}
        if len(first)==1 and all('/' in name for name,_ in rows):
            rows=[(name.split('/',1)[1], data) for name,data in rows]
    else: raise UnsafeRepository('source must be a directory or ZIP archive')
    if not rows: raise UnsafeRepository('no safe source code files found')
    return sorted(rows), skipped

def inspect(source):
    rows, skipped=_read_input(source)
    langs={}; paths={}
    for name,dat in rows:
        paths[name.lower()]=True
        lang=EXT_LANG.get(Path(name).suffix.lower())
        if lang: langs[lang]=langs.get(lang,0)+1
    signals=[]
    for key, entry in SIGNALS.items():
        has_path=any(p.lower().endswith(entry['paths']) or any(p.lower().startswith(s.lower()) for s in entry['paths'] if s.endswith('/')) for p in paths)
        has_ext=any(Path(p).suffix.lower() in entry['extensions'] for p in paths)
        if has_path or has_ext: signals.append({'capability_area':key,'candidate':'inferred_from_file_structure','implementation_hint':entry['lesson'],'executable_integrated':False})
    license_files=[p for p in paths if Path(p).name.lower() in ('license','license.md','license.txt','copying','notice')]
    return {'schema':'kosif.repository-transfer.v1','source_name':Path(source).name,'safe_files':len(rows),'safe_bytes':sum(len(x[1]) for x in rows),
      'excluded_files':len(skipped),'excluded_examples':skipped[:20], 'languages':langs,
      'potential_capabilities':signals,'license_files':license_files,
      'reuse_allowed':False,'reason':'Inspect actual file/dependency licenses and provenance first; existence is not permission',
      'integration_status':'candidate_not_executed','runtime_verified':False,
      'next_steps':['select a concrete feature and acceptance test','review source and transitive licenses','implement narrow local adapter','run sandbox regression tests','only then promote evidence status'],
      'sha256_manifest':{k:hashlib.sha256(b).hexdigest() for k,b in rows}}

def pack(source, output, report_path=None):
    out=Path(output).resolve(); src=Path(source).resolve()
    if out==src or (src.is_dir() and src in out.parents): raise UnsafeRepository('output must be outside input repository')
    rows,_=_read_input(src)
    out.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,body in rows:
            info=zipfile.ZipInfo(name, date_time=(1980,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
            z.writestr(info,body,compress_type=zipfile.ZIP_DEFLATED,compresslevel=6)
    report=inspect(src)
    report['package_sha256']=hashlib.sha256(out.read_bytes()).hexdigest()
    if report_path:
        r=Path(report_path).resolve()
        if r==src or r==out or (src.is_dir() and src in r.parents):raise UnsafeRepository('report path cannot overwrite source or ZIP')
        r.parent.mkdir(parents=True,exist_ok=True)
        r.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return report

def main(argv=None):
    a=argparse.ArgumentParser(description=__doc__);sub=a.add_subparsers(dest='cmd',required=True)
    i=sub.add_parser('inspect');i.add_argument('source');i.add_argument('--out')
    p=sub.add_parser('pack');p.add_argument('source');p.add_argument('--out',required=True);p.add_argument('--report')
    args=a.parse_args(argv)
    try:
        result=inspect(args.source) if args.cmd=='inspect' else pack(args.source,args.out,args.report)
        if args.cmd=='inspect' and args.out:
            Path(args.out).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({k:v for k,v in result.items() if k!='sha256_manifest'},ensure_ascii=False,indent=2))
        return 0
    except (UnsafeRepository, OSError, zipfile.BadZipFile) as e:
        print('repository pack blocked: '+str(e),file=sys.stderr);return 2
if __name__=='__main__': raise SystemExit(main())