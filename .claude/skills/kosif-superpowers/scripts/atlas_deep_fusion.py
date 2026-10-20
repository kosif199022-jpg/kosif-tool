#!/usr/bin/env python3
"""KOSIF Atlas -> Superpowers: read-only, provenance-aware capability discovery.

Third-party skill prose is DATA, never executable instructions. No imports of
third-party code, installation, git, subprocesses, or network calls.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

SCHEMA = "kosif.superpowers.atlas-fusion.v1"
DOMAINS = {
    "reasoning": ("reasoning", "critical thinking", "planning", "decision", "logic", "思考", "تفكير", "تحليل", "استدلال"),
    "agents": ("agent", "workflow", "orchestration", "multi-agent", "prompt", "وكيل", "وكلاء", "برومبت"),
    "engineering": ("debug", "test", "refactor", "architecture", "code review", "software", "برمجة", "كود", "اختبار"),
    "reverse_engineering": ("reverse engineering", "decompile", "binary", "ghidra", "malware analysis", "هندسة عكسية"),
    "security": ("security", "audit", "vulnerability", "threat", "privacy", "أمن", "ثغرات", "حماية"),
    "finance": ("finance", "accounting", "ifrs", "tax", "excel", "financial", "محاسبة", "مالي", "مخزون"),
    "media_motion": ("animation", "motion", "video", "blender", "render", "ffmpeg", "3d", "موشن", "فيديو", "رندر"),
    "design": ("design", "ui", "ux", "illustration", "draw", "graphic", "رسم", "تصميم", "واجهات"),
    "research": ("research", "search", "verification", "scientific", "fact", "بحث", "مصادر", "تحقق"),
    "web_apps": ("browser", "web app", "react", "frontend", "website", "cloud", "متصفح", "تطبيق"),
    "documents": ("pdf", "document", "office", "powerpoint", "word", "spreadsheet", "مستند", "عروض"),
    "language": ("arabic", "translation", "writing", "localization", "لغة", "عربي", "ترجمة"),
}
SAFE_LICENSES = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "CC0-1.0", "0BSD", "Unlicense"}
TOKEN_RE = re.compile(r"[\w\u0600-\u06ff]+", re.UNICODE)

def _load(path):
    raw = Path(path).read_bytes()
    data = json.loads(raw.decode("utf-8-sig"))
    if not isinstance(data, dict) or not isinstance(data.get("skills"), list):
        raise ValueError("Invalid Atlas index schema")
    if data.get("count") != len(data["skills"]):
        raise ValueError("Atlas index count mismatch")
    return data, hashlib.sha256(raw).hexdigest()

def _tokens(s):
    return set(TOKEN_RE.findall(str(s or "").casefold()))

def _contains(haystack, needle):
    return needle.casefold() in str(haystack or "").casefold()

def _row_ok(row):
    return (row.get("verdict") == "READ_ONLY_OK"
            and not row.get("risk_flags")
            and row.get("license") in SAFE_LICENSES)

def _validate_path(root, candidate):
    # Do not follow user-provided absolute paths or traversal
    candidate = str(candidate).replace("\\", "/")
    if candidate.startswith("/") or ".." in candidate.split("/") or not candidate.startswith("skills/"):
        return None
    rel = Path(candidate)
    path = (Path(root) / rel / "SKILL.md").resolve()
    base = Path(root).resolve()
    return path if path.is_relative_to(base) else None

def _sample_source(root, row):
    p = _validate_path(root, row.get("path", ""))
    if p is None:
        return {"source_state": "unsafe_path"}
    if not p.is_file():
        return {"source_state": "not_checked_out", "skill_md": str(p)}
    if p.stat().st_size > 1024*1024:
        return {"source_state": "too_large"}
    data = p.read_bytes()
    txt = data.decode("utf-8-sig", errors="replace")
    # These are only heuristic text warnings; no claim of security certification.
    patterns = ("curl | bash", "wget | bash", "disable security", "ignore previous instructions",
                "rm -rf", "api_key", "private_key", "prompt injection")
    flags = [x for x in patterns if x in txt.casefold()]
    return {
        "source_state": "inspected_text_only",
        "skill_md": str(p),
        "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data),
        "has_frontmatter": txt.lstrip().startswith("---"),
        "headings": len(re.findall(r"^#{1,4}\s", txt, flags=re.M)),
        "static_warning_patterns": flags,
        "executable_files_declared": sum(str(x).lower().endswith((".py",".js",".sh",".ps1",".exe",".dll")) for x in row.get("files", [])),
    }

def _search(rows, query, domain, max_count):
    query_toks = _tokens(query)
    if not query_toks and not domain:
        return []
    words = DOMAINS.get(domain, ()) if domain else ()
    ranked = []
    for row in rows:
        name = str(row.get("skill", ""))
        desc = str(row.get("description", ""))
        score = 0
        for word in query_toks:
            if word in _tokens(name): score += 9
            elif word in _tokens(desc): score += 2
        if query_toks and not score: continue
        if domain:
            matches = [x for x in words if _contains(name, x) or _contains(desc, x)]
            if not matches: continue
            score += 3 + min(len(matches), 3)
        if row.get("complete"): score += 1
        if _row_ok(row): score += 2
        ranked.append((score, row))
    ranked.sort(key=lambda t: (-t[0], str(t[1].get("skill","")), str(t[1].get("id",""))))
    return [r for _,r in ranked[:max_count]]

def build_report(main_path, copyleft_path, query="", domain="", limit=30, source_root=None):
    main, mainhash = _load(main_path)
    copy, copyhash = _load(copyleft_path)
    allrows = main["skills"] + copy["skills"]
    risks = Counter()
    license_counts = Counter()
    verdict_counts = Counter()
    completeness = Counter()
    ids = set()
    defects = []
    for scope, rows in (("main",main["skills"]),("copyleft",copy["skills"])):
        for row in rows:
            if not isinstance(row, dict):
                defects.append(scope + ":non-dict-row");continue
            key = (scope, str(row.get("id")))
            if key in ids: defects.append(scope + ":duplicate-id:" + key[1])
            ids.add(key)
            license_counts[str(row.get("license") or "UNKNOWN")] += 1
            verdict_counts[str(row.get("verdict") or "UNKNOWN")] += 1
            completeness[str(row.get("complete"))] += 1
            for flag in row.get("risk_flags", []): risks[str(flag)] += 1
            if not str(row.get("path","")).startswith("skills/"):
                defects.append(scope + ":invalid-path:" + key[1])
    selected = _search(main["skills"],query,domain,limit)
    out=[]
    for r in selected:
        item={k:r.get(k) for k in ("id","plugin","skill","description","source","license","path","verdict","risk_flags","complete")}
        item["eligibility"] = ("metadata_candidate_only" if _row_ok(r) else "reference_only_manual_review")
        item["execution_verified"] = False
        if source_root: item["source_inspection"] = _sample_source(source_root, r)
        out.append(item)
    return {
        "schema":SCHEMA,
        "origin":{"repository":"kosif199022-jpg/kosif-atlas","main_sha256":mainhash,"copyleft_sha256":copyhash},
        "inventory":{"main":len(main["skills"]),"copyleft":len(copy["skills"]),"total":len(allrows),
                     "read_only_metadata":verdict_counts["READ_ONLY_OK"],
                     "review_before_install":verdict_counts["REVIEW_BEFORE_INSTALL"],
                     "safe_license_and_no_risk_metadata_candidates":sum(_row_ok(r) for r in main["skills"]),
                     "licenses":dict(license_counts.most_common()),"verdicts":dict(verdict_counts),
                     "complete_flags":dict(completeness),"risk_flags":dict(risks.most_common()),
                     "structural_errors":defects[:50]},
        "query":query,"domain":domain or None,"selected":out,"selected_count":len(out),
        "trust":{"metadata_audit_only":True,"imports_third_party_code":False,"executes_skills":False,
                 "installs_deps":False,"makes_network_calls":False,
                 "copyleft_merge_allowed":False,"verified_runtime_capabilities":0,
                 "note":"Read-only metadata + optional static SKILL.md inspection. Manual review and real tests required before importing behavior."},
    }

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--index", required=True, type=Path)
    ap.add_argument("--copyleft", required=True, type=Path)
    ap.add_argument("--query", default="")
    ap.add_argument("--domain", choices=tuple(DOMAINS))
    ap.add_argument("--limit", type=int, default=30)
    ap.add_argument("--source-root", type=Path)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args(argv)
    if not 1 <= args.limit <= 300: ap.error("--limit must be 1..300")
    report = build_report(args.index,args.copyleft,args.query,args.domain,args.limit,args.source_root)
    result=json.dumps(report,ensure_ascii=False,indent=2)
    if args.output: args.output.write_text(result+"\n",encoding="utf-8")
    else: print(result)
    return 1 if report["inventory"]["structural_errors"] else 0

if __name__=="__main__":
    try: sys.exit(main())
    except (ValueError,OSError,json.JSONDecodeError) as exc: print(str(exc),file=sys.stderr);sys.exit(2)
