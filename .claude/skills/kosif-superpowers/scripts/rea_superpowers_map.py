#!/usr/bin/env python3
"""REA-approach map of the superpowers skill — خريطة سوبر باور بمنهج REA.

REA (https://github.com/morluto/rea, MIT) treats a source tree it does not execute as *historical
reference*: a content-addressed inventory, typed relationships, explicit exclusions and stated
limitations. This tool applies the same discipline to this skill and joins it with the catalog, so
Claude can answer "what is here, how is it wired, what is missing" from one file instead of guessing:

  structure    files per area and kind, from a content-addressed walk (sha256 per file)
  graph        Python import and invoke edges between scripts and tests (ast, nothing executed),
               plus the JavaScript require/import edges REA reported in its last receipt
  links        script <-> tools.json entry <-> tests <-> CI <-> powers <-> families
  gaps         unregistered, untested or orphan scripts, tests CI never runs, tools.json paths that
               do not exist, references missing from the layout index, broken relative links in
               references, families without a runnable tool
  atlas        coverage of the Atlas safe core per theme (atlas_5000), zero-coverage themes and the
               next candidates to distil

  python3 scripts/rea_superpowers_map.py build            # writes data/superpowers_rea_map.json,
                                                          #   references/superpowers-rea-map.{md,html}
  python3 scripts/rea_superpowers_map.py build --check    # exit 1 when the outputs are stale
  python3 scripts/rea_superpowers_map.py stats [--json]
  python3 scripts/rea_superpowers_map.py gaps [--kind script_untested] [--json]
  python3 scripts/rea_superpowers_map.py node atlas_5000  # a script stem, tool id, family or path
  python3 scripts/rea_superpowers_map.py ingest-rea --summary S.json --graph G.json
  python3 scripts/rea_superpowers_map.py --self-test

ingest-rea turns the output of `rea import-reference-source <skill dir>` (run separately, once with
`--detail summary --outline-depth 1` and once in full, both `--format json`) into the committed
receipt proofs/rea-superpowers-map/receipt.json. The REA output is read as untrusted JSON: only
known fields are kept, and paths are kept only when they are relative and inside the tree.
This tool never runs REA, never opens the network and never executes the files it maps.
Python 3.8+ standard library.
"""
from __future__ import annotations

import argparse
import ast
import collections
import fnmatch
import hashlib
import html
import json
import re
import sys
import tempfile
from pathlib import Path

SK = Path(__file__).resolve().parents[1]
REPO = SK.parents[2]
SCHEMA = "kosif.superpowers.rea-map.v1"
OUT_JSON = "data/superpowers_rea_map.json"
OUT_MD = "references/superpowers-rea-map.md"
OUT_HTML = "references/superpowers-rea-map.html"
RECEIPT = "proofs/rea-superpowers-map/receipt.json"
SKIP_DIRS = {".git", "__pycache__", "node_modules", "out", ".pytest_cache"}
GENERATED = {OUT_JSON, OUT_MD, OUT_HTML}
GAP_KINDS = ("script_orphan", "script_unregistered", "script_untested", "test_not_in_ci", "tool_path_missing",
             "tool_file_missing", "reference_unlisted", "broken_link", "family_without_tool")
MD_LINK = re.compile(r"\]\(([^)\s#]+)(?:#[^)]*)?\)")
PY_REF = re.compile(r"(?:scripts|evals)/([A-Za-z0-9_]+)\.py")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def walk(root: Path) -> list:
    """Content-addressed inventory: one row per regular file, sorted, symlinks recorded not followed."""
    rows = []
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root).as_posix()
        if any(part in SKIP_DIRS for part in p.relative_to(root).parts):
            continue
        if p.is_symlink():
            rows.append({"path": rel, "kind": "symlink"})
        elif p.is_file() and rel not in GENERATED:
            rows.append({"path": rel, "kind": "file", "size": p.stat().st_size, "sha256": sha256(p)})
    return rows


def load_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def py_edges(root: Path, files: list) -> dict:
    """ast-only: import edges to local modules and invoke edges (string constants naming scripts/x.py)."""
    stems = {Path(f).stem for f in files}
    edges, failures = [], []
    for f in files:
        src = Path(f).stem
        try:
            tree = ast.parse((root / f).read_text(encoding="utf-8"), filename=f)
        except (SyntaxError, UnicodeDecodeError, OSError) as e:
            failures.append({"path": f, "error": type(e).__name__})
            continue
        found = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                found |= {("imports", a.name.split(".")[0]) for a in node.names}
            elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                found.add(("imports", node.module.split(".")[0]))
            elif isinstance(node, ast.Constant) and isinstance(node.value, str) and ".py" in node.value:
                found |= {("invokes", m) for m in PY_REF.findall(node.value)}
        for kind, dst in sorted(found):
            if dst in stems and dst != src:
                edges.append({"from": src, "to": dst, "kind": kind})
    return {"edges": edges, "parse_failures": failures}


def ci_patterns(text: str) -> tuple:
    names = set(re.findall(r"(test_[A-Za-z0-9_*]+\.py)", text))
    skill_discover_all = bool(re.search(r"discover -s \S*kosif-superpowers/evals(?! -p)", text))
    return names, skill_discover_all


def in_ci(test_name: str, names: set, all_evals: bool) -> bool:
    return all_evals or any(fnmatch.fnmatch(test_name, n) for n in names)


def build(root: Path = SK, repo: Path = REPO, atlas=True) -> dict:
    inv = walk(root)
    files = [r["path"] for r in inv if r["kind"] == "file"]
    areas = collections.Counter(p.split("/")[0] if "/" in p else "(root)" for p in files)
    exts = collections.Counter((Path(p).suffix or "(none)") for p in files)
    scripts = sorted(p for p in files if p.startswith("scripts/") and p.endswith(".py") and p.count("/") == 1
                     and not Path(p).name.startswith("test_"))
    evals = sorted(p for p in files if p.endswith(".py") and p.count("/") == 1 and
                   (p.startswith("evals/") or (p.startswith("scripts/") and Path(p).name.startswith("test_"))))
    repo_tests = sorted(p.as_posix() for p in (repo / "tests").glob("test_*.py")) if (repo / "tests").is_dir() else []
    graph = py_edges(root, scripts + evals)
    tools_doc = load_json(root / "data/tools.json", {"tools": []})
    tools = tools_doc.get("tools", []) if isinstance(tools_doc, dict) else []
    ci_text = (repo / ".github/workflows/ci.yml").read_text(encoding="utf-8") if (repo / ".github/workflows/ci.yml").is_file() else ""
    ci_names, ci_all = ci_patterns(ci_text)
    powers = []
    for f in sorted((root / "data/powers").glob("*.json")):
        data = load_json(f, [])
        powers += data if isinstance(data, list) else []
    layout = load_json(root / "data/skill_layout.json", {"sections": []})
    listed = {x for s in layout.get("sections", []) for x in s.get("files", [])}
    globs = [g for s in layout.get("sections", []) for g in s.get("globs", [])]

    stem_of = {Path(s).stem: s for s in scripts}
    by_path = {}
    for t in tools:
        by_path.setdefault(t.get("path", ""), []).append(t.get("id"))
    test_refs = collections.defaultdict(set)
    for e in graph["edges"]:
        if e["from"].startswith("test_") and e["to"] in stem_of:
            test_refs[e["to"]].add("evals/" + e["from"] + ".py")
    for t in repo_tests:
        text = Path(t).read_text(encoding="utf-8", errors="replace")
        for stem in stem_of:
            if re.search(r"\b" + re.escape(stem) + r"\b", text):
                test_refs[stem].add("tests/" + Path(t).name)
    for t in tools:
        stem = Path(t.get("path", "")).stem
        for tp in t.get("tests", []):
            if stem in stem_of:
                test_refs[stem].add(tp.split("kosif-superpowers/")[-1])
    importers = collections.defaultdict(set)
    for e in graph["edges"]:
        if not e["from"].startswith("test_"):
            importers[e["to"]].add(e["from"])
    power_refs = collections.defaultdict(list)
    for p in powers:
        blob = " ".join(str(p.get(k, "")) for k in ("how", "install", "params", "proof", "source"))
        for stem in set(PY_REF.findall(blob)):
            if stem in stem_of:
                power_refs[stem].append(p.get("id"))

    nodes, gaps = [], []
    for s in scripts:
        stem = Path(s).stem
        tids = by_path.get(s, [])
        tests = sorted(test_refs.get(stem, ()))
        ci = bool(re.search(r"scripts/" + re.escape(stem) + r"\.py", ci_text))
        role = "registered" if tids else ("helper" if importers.get(stem) else "orphan")
        nodes.append({"id": stem, "path": s, "role": role, "tools": tids, "tests": tests,
                      "ci": ci, "imported_by": sorted(importers.get(stem, ())), "powers": sorted(power_refs.get(stem, []))[:12],
                      "power_count": len(power_refs.get(stem, []))})
        if role == "orphan":
            gaps.append({"kind": "script_orphan", "id": stem, "detail": "not in tools.json, imported by no script"})
        elif role == "helper":
            pass
        if not tids and role != "orphan" and not stem.startswith("_"):
            gaps.append({"kind": "script_unregistered", "id": stem, "detail": "helper imported by " + ", ".join(sorted(importers[stem])[:4])})
        if not tests and not ci:
            gaps.append({"kind": "script_untested", "id": stem, "detail": "no eval, repo test, tools.json test or CI step references it"})
    for e in evals:
        name = Path(e).name
        if name.startswith("test_") and e.startswith("evals/") and not in_ci(name, ci_names, ci_all):
            gaps.append({"kind": "test_not_in_ci", "id": name, "detail": "ci.yml names no pattern that runs it"})
    for t in tools:
        base = repo if t.get("root") == "repo" else root
        if t.get("path") and not (base / t["path"]).exists():
            gaps.append({"kind": "tool_path_missing", "id": t.get("id"), "detail": t["path"]})
        for ref in t.get("tests", []) + t.get("docs", []):
            if not (repo / ref).exists():
                gaps.append({"kind": "tool_file_missing", "id": t.get("id"), "detail": ref})
    for p in files:
        if p.startswith("references/") and p.endswith(".md") and p not in listed and not any(fnmatch.fnmatchcase(p, g) for g in globs):
            gaps.append({"kind": "reference_unlisted", "id": p, "detail": "not in data/skill_layout.json"})
    link_files = [p for p in files if p.endswith(".md") and (p.startswith("references/") or "/" not in p)]
    broken = 0
    for p in link_files:
        text = (root / p).read_text(encoding="utf-8", errors="replace")
        for target in sorted(set(MD_LINK.findall(text))):
            if re.match(r"^[a-z]+:", target) or target.startswith("/"):
                continue
            if not ((root / p).parent / target).exists():
                broken += 1
                gaps.append({"kind": "broken_link", "id": p, "detail": target})
    fam_power = collections.Counter(p.get("family") for p in powers)
    fam_tool = collections.Counter(f for t in tools for f in t.get("families", []))
    families = [{"id": f, "powers": n, "tools": fam_tool.get(f, 0)} for f, n in sorted(fam_power.items(), key=lambda kv: str(kv[0]))]
    for f in families:
        if not f["tools"]:
            gaps.append({"kind": "family_without_tool", "id": f["id"], "detail": f"{f['powers']} powers, no tools.json entry lists this family"})
    gaps.sort(key=lambda g: (GAP_KINDS.index(g["kind"]), str(g["id"]), g["detail"]))

    receipt = load_json(root / RECEIPT, None)
    rea = None
    if isinstance(receipt, dict) and receipt.get("schema") == "kosif.rea-receipt.v1":
        rea = {k: receipt.get(k) for k in ("importer_version", "vcs_head", "inventory_state", "counts", "languages",
                                            "limitations", "manifests")}
        rea["js_edges"] = receipt.get("relationships", [])
        rea["receipt"] = RECEIPT
    out = {"schema": SCHEMA,
           "method": "REA historical-reference discipline: content-addressed inventory, typed edges, explicit gaps and limitations; nothing executed",
           "structure": {"files": len(files), "symlinks": sum(r["kind"] == "symlink" for r in inv),
                         "bytes": sum(r.get("size", 0) for r in inv), "areas": dict(sorted(areas.items())),
                         "extensions": dict(exts.most_common(15))},
           "counts": {"scripts": len(scripts), "evals": len(evals), "repo_tests": len(repo_tests), "tools": len(tools),
                      "powers": len(powers), "families": len(families), "py_edges": len(graph["edges"]),
                      "roles": dict(collections.Counter(n["role"] for n in nodes)),
                      "gaps": dict(collections.Counter(g["kind"] for g in gaps)), "broken_links": broken},
           "scripts": nodes, "py_edges": graph["edges"], "parse_failures": graph["parse_failures"],
           "families": families, "gaps": gaps, "rea": rea,
           "limitations": ["Import edges come from ast and string constants; dynamic imports (importlib, runpy) are invisible.",
                           "A test 'references' a script when it imports it, names it in tools.json, or a repo test mentions its name; that is not coverage measurement.",
                           "JavaScript edges are REA's, as of the receipt's vcs head, and go stale until the receipt is refreshed.",
                           "Atlas 'covered' means a power cites the folder, not that the skill was run."]}
    if atlas:
        out["atlas"] = atlas_section(root)
    return out


def atlas_section(root: Path):
    sys.path.insert(0, str(root / "scripts"))
    try:
        import atlas_5000 as a5
        idx = a5.load_index(root / "data/atlas_capability_index.json.gz")
        cov = a5.coverage_map(root / "data/powers")
    except Exception as e:  # missing index in a trimmed copy: say so instead of failing the whole map
        return {"available": False, "reason": type(e).__name__}
    st = a5.stats(idx, cov)
    themes = sorted(({"theme": t, **v} for t, v in st["themes"].items()), key=lambda r: (r["coverage_pct"], -r["safe"], r["theme"]))
    nxt = [{"theme": g["theme"], "uncovered": g.get("uncovered"), "next": [{"id": c.get("id"), "skill": c.get("skill"), "plugin": c.get("plugin")} for c in g.get("next_candidates", [])]}
           for g in a5.gaps(idx, cov, top=8, per_theme=3)]
    return {"available": True, "atlas_total": st["atlas_total"], "safe_core": st["safe_core"], "covered": st["covered"],
            "coverage_pct": st["coverage_pct"], "themes": themes,
            "zero_coverage": [t["theme"] for t in themes if t["covered"] == 0], "next_candidates": nxt}


def render_md(m: dict) -> str:
    c, s = m["counts"], m["structure"]
    L = ["# Superpowers map, REA approach — خريطة سوبر باور بمنهج REA", "",
         "Generated by `scripts/rea_superpowers_map.py build`; do not edit by hand. The interactive page is "
         "[superpowers-rea-map.html](superpowers-rea-map.html); the data is `data/superpowers_rea_map.json`.", "",
         "## الفهرس / contents", "", "1. [Structure](#structure)", "2. [REA receipt](#rea-receipt)", "3. [Gaps](#gaps)",
         "4. [Atlas coverage](#atlas-coverage)", "5. [Limitations](#limitations)", "",
         "## Structure", "",
         f"- Files: {s['files']} ({s['bytes']:,} bytes), symlinks: {s['symlinks']}.",
         f"- Scripts: {c['scripts']} ({', '.join(f'{k} {v}' for k, v in sorted(c['roles'].items()))}); evals: {c['evals']}; repo tests: {c['repo_tests']}.",
         f"- tools.json entries: {c['tools']}; powers: {c['powers']} in {c['families']} families; Python edges: {c['py_edges']}.", "",
         "| Area | Files |", "|---|---:|"]
    L += [f"| {k} | {v} |" for k, v in s["areas"].items()]
    if m.get("rea"):
        r = m["rea"]
        L += ["", "## REA receipt", "",
              f"`rea import-reference-source` {r['importer_version']} at git {str(r['vcs_head'])[:12]}: inventory {r['inventory_state']}, "
              f"{r['counts'].get('entries')} entries, {r['counts'].get('files')} files, {r['counts'].get('relationships')} JS relationships, "
              f"{r['counts'].get('exclusions')} exclusions, {r['counts'].get('parse_failures')} parse failures. Languages: {', '.join(r['languages'] or [])}.",
              "", "REA's stated limitations: " + " ".join(r.get("limitations") or ["none"]),
              "", f"Receipt: `{r['receipt']}`."]
    L += ["", "## Gaps", "", "| Kind | Count |", "|---|---:|"]
    L += [f"| {k} | {v} |" for k, v in sorted(c["gaps"].items(), key=lambda kv: GAP_KINDS.index(kv[0]))]
    L += ["", "Run `python3 scripts/rea_superpowers_map.py gaps --kind <kind>` for the rows."]
    a = m.get("atlas") or {}
    if a.get("available"):
        L += ["", "## Atlas coverage", "",
              f"{a['covered']} of {a['safe_core']} safe-core skills are cited by a power ({a['coverage_pct']}%; Atlas total {a['atlas_total']}).",
              "", "| Theme | Safe | Covered | % |", "|---|---:|---:|---:|"]
        L += [f"| {t['theme']} | {t['safe']} | {t['covered']} | {t['coverage_pct']} |" for t in a["themes"]]
        L += ["", "Zero-coverage themes: " + (", ".join(a["zero_coverage"]) or "none") + "."]
    L += ["", "## Limitations", ""] + [f"- {x}" for x in m["limitations"]] + [""]
    return "\n".join(L)


def render_html(m: dict) -> str:
    data = json.dumps({k: m[k] for k in ("counts", "structure", "scripts", "py_edges", "families", "gaps", "rea", "atlas") if k in m},
                      ensure_ascii=False, sort_keys=True).replace("</", "<\\/")
    return HTML.replace("__DATA__", data)


HTML = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Superpowers REA map</title>
<style>
:root{--bg:#fbfaf7;--fg:#1d1d1b;--mut:#6b6a66;--line:#e4e1da;--card:#fff;--acc:#2f5d8a;--bad:#a8432f;--ok:#3b7a4a}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#161615;--fg:#ecebe7;--mut:#a3a19b;--line:#33322f;--card:#1f1f1d;--acc:#7fb0df;--bad:#e08a75;--ok:#86c495}}
:root[data-theme=dark]{--bg:#161615;--fg:#ecebe7;--mut:#a3a19b;--line:#33322f;--card:#1f1f1d;--acc:#7fb0df;--bad:#e08a75;--ok:#86c495}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,sans-serif}
main{max-width:1100px;margin:0 auto;padding:20px 16px}
h1{font-size:22px;margin:0 0 4px}h2{font-size:17px;margin:28px 0 8px}
.mut{color:var(--mut)}.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:8px;margin:14px 0}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px}.kpi b{display:block;font-size:20px}
table{border-collapse:collapse;width:100%;font-size:13px}td,th{border-bottom:1px solid var(--line);padding:4px 6px;text-align:left;vertical-align:top}
.wrap{overflow-x:auto}input{width:100%;box-sizing:border-box;padding:8px;border:1px solid var(--line);border-radius:6px;background:var(--card);color:var(--fg)}
.bar{height:8px;background:var(--line);border-radius:4px;min-width:60px}.bar i{display:block;height:8px;background:var(--acc);border-radius:4px}
.tag{display:inline-block;padding:0 6px;border-radius:4px;border:1px solid var(--line);font-size:12px}
.orphan{color:var(--bad)}.registered{color:var(--ok)}details{margin:4px 0}
</style></head><body><main>
<h1>Superpowers map, REA approach</h1>
<p class="mut">Content-addressed inventory, typed edges, links to the catalog, gaps and Atlas coverage. Nothing was executed to build it.</p>
<div class="kpis" id="kpis"></div>
<h2>Gaps</h2><div id="gaps"></div>
<h2>Scripts</h2><input id="q" placeholder="Filter scripts, tools, tests or powers"><div class="wrap"><table id="scripts"></table></div>
<h2>Families</h2><div class="wrap"><table id="fams"></table></div>
<h2>Atlas coverage by theme</h2><div class="wrap"><table id="atlas"></table></div>
<h2>REA receipt</h2><div id="rea" class="mut"></div>
</main><script>
const M=__DATA__;const e=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const c=M.counts,k=[['Files',M.structure.files],['Scripts',c.scripts],['Tools',c.tools],['Powers',c.powers],['Families',c.families],['Python edges',c.py_edges],['Gaps',M.gaps.length]];
document.getElementById('kpis').innerHTML=k.map(([a,b])=>`<div class="kpi"><span class="mut">${a}</span><b>${b}</b></div>`).join('');
const byKind={};M.gaps.forEach(g=>(byKind[g.kind]=byKind[g.kind]||[]).push(g));
document.getElementById('gaps').innerHTML=Object.entries(byKind).map(([kd,rows])=>`<details><summary><b>${e(kd)}</b> <span class="tag">${rows.length}</span></summary><table>${rows.map(r=>`<tr><td>${e(r.id)}</td><td class="mut">${e(r.detail)}</td></tr>`).join('')}</table></details>`).join('')||'<p>No gaps.</p>';
const sc=document.getElementById('scripts');function draw(q){q=(q||'').toLowerCase();
sc.innerHTML='<tr><th>Script</th><th>Role</th><th>Tools</th><th>Tests</th><th>Imported by</th><th>Powers</th></tr>'+M.scripts.filter(s=>!q||JSON.stringify(s).toLowerCase().includes(q)).map(s=>`<tr><td>${e(s.id)}</td><td class="${e(s.role)}">${e(s.role)}</td><td>${e(s.tools.join(', '))}</td><td>${s.tests.length}</td><td>${e(s.imported_by.join(', '))}</td><td>${s.power_count}</td></tr>`).join('');}
draw();document.getElementById('q').addEventListener('input',ev=>draw(ev.target.value));
document.getElementById('fams').innerHTML='<tr><th>Family</th><th>Powers</th><th>Tools</th></tr>'+M.families.map(f=>`<tr><td>${e(f.id)}</td><td>${f.powers}</td><td class="${f.tools?'':'orphan'}">${f.tools}</td></tr>`).join('');
const A=M.atlas||{};document.getElementById('atlas').innerHTML=A.available?'<tr><th>Theme</th><th>Safe</th><th>Covered</th><th>Coverage</th></tr>'+A.themes.map(t=>`<tr><td>${e(t.theme)}</td><td>${t.safe}</td><td>${t.covered}</td><td><div class="bar"><i style="width:${Math.min(100,t.coverage_pct)}%"></i></div> ${t.coverage_pct}%</td></tr>`).join(''):'<tr><td>Atlas index not available.</td></tr>';
const R=M.rea;document.getElementById('rea').textContent=R?`rea import-reference-source ${R.importer_version} at ${String(R.vcs_head).slice(0,12)}: ${R.inventory_state} inventory, ${R.counts.entries} entries, ${R.counts.relationships} JS relationships. ${(R.limitations||[]).join(' ')}`:'No REA receipt committed.';
</script></body></html>
"""


def outputs(m: dict) -> dict:
    return {OUT_JSON: json.dumps(m, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
            OUT_MD: render_md(m), OUT_HTML: render_html(m)}


def ingest_rea(summary: Path, graph: Path, root: Path = SK) -> dict:
    s, g = load_json(summary, None), load_json(graph, None)
    if not isinstance(s, dict) or s.get("schema") != "HistoricalSourceSummary":
        raise SystemExit("summary is not a REA HistoricalSourceSummary JSON")
    if not isinstance(g, dict) or g.get("schema") != "HistoricalSourceGraph":
        raise SystemExit("graph is not a REA HistoricalSourceGraph JSON")
    def safe(p):
        return isinstance(p, str) and not p.startswith(("/", "..")) and "/../" not in p
    rels = sorted(({"from": r["from_path"], "to": r["to"], "kind": r.get("kind"), "resolution": r.get("resolution")}
                   for r in g.get("relationships", []) if safe(r.get("from_path"))), key=lambda r: (r["from"], r["to"]))
    man = s.get("manifest", {})
    rec = {"schema": "kosif.rea-receipt.v1", "tool": "rea import-reference-source", "authority": s.get("authority"),
           "importer_version": (s.get("provenance") or {}).get("importer_version"), "vcs_head": (s.get("vcs") or {}).get("head"),
           "manifest_id": man.get("manifest_id"), "graph_sha256": man.get("graph_sha256"), "root_sha256": man.get("root_sha256"),
           "inventory_state": s.get("inventory_state"), "counts": s.get("counts"), "languages": s.get("languages"),
           "manifests": [p for p in s.get("manifests", []) if safe(p)], "exclusions": s.get("exclusions"),
           "limitations": s.get("limitations"), "relationships": rels,
           "note": "Trimmed from REA output read as untrusted JSON; graph_sha256 and root_sha256 identify the full REA graph of the tree at vcs_head."}
    (root / RECEIPT).parent.mkdir(parents=True, exist_ok=True)
    (root / RECEIPT).write_text(json.dumps(rec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return rec


def find_node(m: dict, q: str):
    for s in m["scripts"]:
        if q in (s["id"], s["path"]):
            return {"type": "script", **s, "edges": [e for e in m["py_edges"] if q in (e["from"], e["to"])],
                    "gaps": [g for g in m["gaps"] if g["id"] == s["id"]]}
    for f in m["families"]:
        if f["id"] == q:
            return {"type": "family", **f}
    tools = [s for s in m["scripts"] if q in s["tools"]]
    if tools:
        return {"type": "tool", "id": q, "scripts": [s["id"] for s in tools]}
    rows = [g for g in m["gaps"] if g["id"] == q]
    return {"type": "path", "id": q, "gaps": rows} if rows else None


def self_test() -> int:
    with tempfile.TemporaryDirectory() as d:
        repo = Path(d)
        root = repo / ".claude/skills/kosif-superpowers"
        for sub in ("scripts", "evals", "data/powers", "references", ".github"):
            (root / sub).mkdir(parents=True, exist_ok=True)
        (repo / ".github/workflows").mkdir(parents=True)
        (root / "scripts/core.py").write_text("import helper\nCMD = 'python3 scripts/lonely.py'\n")
        (root / "scripts/helper.py").write_text("X = 1\n")
        (root / "scripts/lonely.py").write_text("print('x')\n")
        (root / "scripts/broken.py").write_text("def (\n")
        (root / "evals/test_core.py").write_text("import core\n")
        (root / "evals/test_skipped.py").write_text("import helper\n")
        (root / "data/tools.json").write_text(json.dumps({"tools": [
            {"id": "core", "path": "scripts/core.py", "root": "skill", "tests": [], "docs": ["nope.md"], "families": ["fam-a"]},
            {"id": "ghost", "path": "scripts/ghost.py", "root": "skill", "tests": [], "docs": [], "families": []}]}))
        (root / "data/powers/p.json").write_text(json.dumps([
            {"id": "A-1", "family": "fam-a", "how": "python3 scripts/core.py run"}, {"id": "B-1", "family": "fam-b", "how": ""}]))
        (root / "data/skill_layout.json").write_text(json.dumps({"sections": [{"files": ["references/listed.md"]}]}))
        (root / "references/listed.md").write_text("[ok](unlisted.md) [bad](missing.md) [web](https://x.y)\n")
        (root / "references/unlisted.md").write_text("x\n")
        (repo / ".github/workflows/ci.yml").write_text("run: python3 -m unittest discover -s x/kosif-superpowers/evals -p 'test_core.py'\n")
        m = build(root, repo, atlas=False)
        kinds = {(g["kind"], g["id"]) for g in m["gaps"]}
        roles = {s["id"]: s["role"] for s in m["scripts"]}
        checks = [
            (roles == {"broken": "orphan", "core": "registered", "helper": "helper", "lonely": "helper"}, f"roles {roles}"),
            ({"from": "core", "to": "lonely", "kind": "invokes"} in m["py_edges"], "invoke edge"),
            ([f["path"] for f in m["parse_failures"]] == ["scripts/broken.py"], "parse failure recorded"),
            (("test_not_in_ci", "test_skipped.py") in kinds and ("test_not_in_ci", "test_core.py") not in kinds, "ci patterns"),
            (("tool_path_missing", "ghost") in kinds and ("tool_file_missing", "core") in kinds, "tools.json paths"),
            (("reference_unlisted", "references/unlisted.md") in kinds, "layout index"),
            ([g["detail"] for g in m["gaps"] if g["kind"] == "broken_link"] == ["missing.md"], "broken links"),
            (("family_without_tool", "fam-b") in kinds and ("family_without_tool", "fam-a") not in kinds, "families"),
            (("script_untested", "core") not in kinds and ("script_untested", "lonely") in kinds, "tests"),
            (outputs(m) == outputs(build(root, repo, atlas=False)), "deterministic"),
            (next(s for s in m["scripts"] if s["id"] == "core")["powers"] == ["A-1"], "power links"),
        ]
        bad = [msg for ok, msg in checks if not ok]
        print(json.dumps({"self_test": "fail" if bad else "pass", "checks": len(checks), "failed": bad}))
        return 1 if bad else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--self-test", action="store_true", help="run the offline synthetic check and exit")
    sub = ap.add_subparsers(dest="cmd")
    b = sub.add_parser("build", help="write the JSON, Markdown and HTML map")
    b.add_argument("--check", action="store_true", help="exit 1 if the committed outputs differ")
    for name in ("stats", "gaps"):
        p = sub.add_parser(name)
        p.add_argument("--json", action="store_true")
        if name == "gaps":
            p.add_argument("--kind", choices=GAP_KINDS)
    n = sub.add_parser("node", help="one script, tool, family or path with its links")
    n.add_argument("id")
    i = sub.add_parser("ingest-rea", help="turn REA import-reference-source JSON into the committed receipt")
    i.add_argument("--summary", required=True, type=Path)
    i.add_argument("--graph", required=True, type=Path)
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if a.cmd == "ingest-rea":
        rec = ingest_rea(a.summary, a.graph)
        print(json.dumps({"receipt": RECEIPT, "vcs_head": rec["vcs_head"], "counts": rec["counts"]}))
        return 0
    if a.cmd is None:
        ap.print_help()
        return 2
    m = build()
    if a.cmd == "build":
        outs = outputs(m)
        if a.check:
            stale = [p for p, t in outs.items() if not (SK / p).is_file() or (SK / p).read_text(encoding="utf-8") != t]
            print(json.dumps({"stale": stale}))
            return 1 if stale else 0
        for p, t in outs.items():
            (SK / p).write_text(t, encoding="utf-8")
        print(json.dumps({"wrote": sorted(outs), "gaps": m["counts"]["gaps"]}))
        return 0
    if a.cmd == "stats":
        st = {"structure": m["structure"], "counts": m["counts"],
              "atlas": {k: m["atlas"].get(k) for k in ("safe_core", "covered", "coverage_pct", "zero_coverage")} if m.get("atlas") else None,
              "rea": {k: m["rea"][k] for k in ("importer_version", "vcs_head", "inventory_state", "counts")} if m.get("rea") else None}
        print(json.dumps(st, ensure_ascii=False, indent=None if a.json else 1))
        return 0
    if a.cmd == "gaps":
        rows = [g for g in m["gaps"] if not a.kind or g["kind"] == a.kind]
        if a.json:
            print(json.dumps(rows, ensure_ascii=False))
        else:
            for g in rows:
                print(f"{g['kind']:22} {g['id']}  {g['detail']}")
        return 0
    if a.cmd == "node":
        node = find_node(m, a.id)
        if node is None:
            print(json.dumps({"error": f"unknown node {a.id!r}"}))
            return 2
        print(json.dumps(node, ensure_ascii=False, indent=1))
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
