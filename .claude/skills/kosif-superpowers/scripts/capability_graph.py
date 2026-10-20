#!/usr/bin/env python3
"""Capability graph: one connected map of what Claude can do with this skill.

Layers: root → domains → families → (requirements they need · scripts that execute them · tests that prove the scripts).
Code edges come from a local AST pass over scripts/ (always current) merged with the Graphify MCP snapshot in
data/graphify_code_layer.json (cross-checked; marked with its commit).

    python3 scripts/capability_graph.py build              # write data/capability_graph.json + references/capability-graph.html
    python3 scripts/capability_graph.py build --check      # exit 1 if the committed files are stale (writes nothing)
    python3 scripts/capability_graph.py build --out-dir D  # write both files into D instead (tests)
    python3 scripts/capability_graph.py stats              # node/edge counts per layer
    python3 scripts/capability_graph.py path <FAMILY|REQ|SCRIPT>   # neighbours of one node (what it unlocks / needs / proves)

Stdlib only; the HTML is self-contained (no CDN) and works offline. Output is deterministic: every
collection is sorted, so two builds of the same tree are byte-identical on any machine.
"""
from __future__ import annotations

import ast
import json
import re
import signal
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
REPO = SKILL.parents[2] if SKILL.parent.name == "skills" else SKILL
OUT_JSON = SKILL / "data" / "capability_graph.json"
OUT_HTML = SKILL / "references" / "capability-graph.html"
GFY = SKILL / "data" / "graphify_code_layer.json"
SCRIPT_RE = re.compile(r"(?:scripts|tools)/[\w/.-]+\.(?:py|cjs|mjs|js)")


def load():
    sys.path.insert(0, str(HERE))
    import powers as P  # noqa: E402
    return P, P.load_powers()


def ast_imports():
    """script → local scripts it imports (module names resolved inside scripts/)."""
    mods = {p.stem: p for p in sorted(HERE.rglob("*.py")) if "__pycache__" not in p.parts}
    edges = []
    for p in mods.values():
        try:
            tree = ast.parse(p.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError):
            continue
        names = set()
        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                names |= {a.name.split(".")[0] for a in n.names}
            elif isinstance(n, ast.ImportFrom) and n.module:
                names.add(n.module.split(".")[0])
        for nm in sorted(names):
            if nm in mods and mods[nm] != p:
                edges.append((rel(p), rel(mods[nm])))
    return edges


def rel(p: Path) -> str:
    return p.relative_to(SKILL).as_posix()  # forward slashes on Windows too


def tests_for_scripts():
    """script → test files that mention it (repo tests/ and skill evals/)."""
    out = defaultdict(set)
    files = sorted((REPO / "tests").glob("*.py")) + sorted((SKILL / "evals").glob("*.py")) + sorted((SKILL / "evals").glob("*.mjs"))
    scripts = sorted(p for p in HERE.rglob("*") if p.suffix in (".py", ".cjs", ".mjs") and "__pycache__" not in p.parts)
    for t in files:
        try:
            txt = t.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for s in scripts:
            if s.name in txt:
                out[rel(s)].add(t.relative_to(REPO).as_posix() if REPO in t.parents else t.name)
    return out


def build(check: bool = False, out_dir: Path = None):
    P, pw = load()
    reg = json.loads((SKILL / "data" / "requirements.json").read_text(encoding="utf-8"))
    nodes, edges = {}, []

    def node(i, kind, label, **kw):
        nodes.setdefault(i, {"id": i, "kind": kind, "label": label, **kw})

    node("root", "root", "KOSIF Superpowers", count=len(pw))
    fams = defaultdict(list)
    for p in pw:
        fams[p["family"]].append(p)
    for fam, rows in fams.items():
        dom = rows[0].get("domain") or P.DEFAULT_DOMAIN
        st = Counter(r.get("status") for r in rows)
        ttl = P.family_title(fam)
        node(f"dom:{dom}", "domain", dom)
        node(f"fam:{fam}", "family", ttl[1] if isinstance(ttl, tuple) else fam, ar=ttl[0] if isinstance(ttl, tuple) else "",
             prefix=P.prefix_of(rows[0]), count=len(rows), proven=st.get("proven", 0), status=dict(st))
        edges.append(("root", f"dom:{dom}", "has", 1))
        edges.append((f"dom:{dom}", f"fam:{fam}", "has", len(rows)))
        req = Counter(k for r in rows for k in (r.get("requires") or []))
        for k, n in req.most_common(8):
            v = reg.get(k, {})
            node(f"req:{k}", "requirement", k, ar=v.get("ar", ""), en=v.get("en", ""), install=v.get("install", ""), req_kind=v.get("kind", ""))
            edges.append((f"fam:{fam}", f"req:{k}", "needs", n))
        scr = Counter()
        for r in rows:
            for m in SCRIPT_RE.findall(" ".join([str(r.get("how", "")), " ".join(r.get("proof") or [])])):
                m = m.split("kosif-superpowers/")[-1]
                if (SKILL / m).exists():
                    scr[m] += 1
        for s, n in scr.most_common(10):
            node(f"script:{s}", "script", s)
            edges.append((f"fam:{fam}", f"script:{s}", "runs", n))
    # code layer
    for a, b in ast_imports():
        node(f"script:{a}", "script", a); node(f"script:{b}", "script", b)
        edges.append((f"script:{a}", f"script:{b}", "imports", 1))
    gfy = json.loads(GFY.read_text(encoding="utf-8")) if GFY.exists() else {}
    confirmed = 0
    local = {(a, b) for a, b, k, _ in edges if k == "imports"}
    for e in gfy.get("file_edges", []):
        a, b = f"script:{e['from']}", f"script:{e['to']}"
        if (a, b) in local:
            confirmed += 1
        elif e["from"].startswith("scripts/") and (SKILL / e["from"]).exists() and (SKILL / e["to"]).exists():
            node(a, "script", e["from"]); node(b, "script", e["to"])
            edges.append((a, b, "graphify:" + e["rel"], e.get("conf", 1)))
    for s, tests in sorted(tests_for_scripts().items()):
        if f"script:{s}" not in nodes:
            continue
        for t in sorted(tests):
            node(f"test:{t}", "test", t)
            edges.append((f"script:{s}", f"test:{t}", "tested_by", 1))
    for ex in gfy.get("executors_ranked", []):
        k = f"script:{ex['file']}"
        if k in nodes:
            nodes[k]["executor_score"] = ex["score"]
    data = {"generated_by": "scripts/capability_graph.py", "graphify": {k: gfy.get(k) for k in ("commit", "indexed_at", "graph")},
            "graphify_import_edges_confirmed_locally": confirmed,
            "nodes": list(nodes.values()), "edges": [{"from": a, "to": b, "rel": k, "w": w} for a, b, k, w in edges]}
    outputs = {OUT_JSON: json.dumps(data, ensure_ascii=False, indent=1) + "\n", OUT_HTML: html(data)}
    if check:
        stale = [rel(p) for p, text in outputs.items() if not p.is_file() or p.read_text(encoding="utf-8") != text]
        if stale:
            print("capability graph is stale: " + ", ".join(stale) + " — run: python3 scripts/capability_graph.py build", file=sys.stderr)
            return 1
        print("capability graph up to date")
        return 0
    written = []
    for p, text in outputs.items():
        dest = Path(out_dir) / p.name if out_dir else p
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8")
        written.append(str(dest) if out_dir else rel(p))
    kinds = Counter(n["kind"] for n in nodes.values())
    print(f"wrote {' and '.join(written)} · nodes {dict(kinds)} · edges {len(edges)} · graphify edges confirmed {confirmed}")
    return 0


def html(data: dict) -> str:
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    return """<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>KOSIF Capability Graph</title>
<style>
:root{--bg:#0f1115;--fg:#e9e6df;--mut:#9a968c;--line:#2a2d35;--acc:#e0b354;--ok:#5fbf7f;--req:#6aa5e8;--scr:#c58be0;--tst:#8fa3a0;--card:#171a20}
@media (prefers-color-scheme: light){:root:not([data-theme="dark"]){--bg:#faf8f3;--fg:#1d1c19;--mut:#6b675e;--line:#e2ddd2;--acc:#a06d00;--ok:#2f7d4a;--req:#2a63a8;--scr:#7b3e9c;--tst:#4e6461;--card:#fff}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,"Noto Naskh Arabic","Segoe UI",sans-serif}
header{padding:16px;border-bottom:1px solid var(--line)}h1{margin:0 0 4px;font-size:20px}header p{margin:0;color:var(--mut);font-size:13px}
.bar{display:flex;gap:8px;flex-wrap:wrap;padding:12px 16px}input{flex:1;min-width:180px;padding:8px 10px;border-radius:8px;border:1px solid var(--line);background:var(--card);color:var(--fg)}
.wrap{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.2fr);gap:12px;padding:0 16px 24px}@media(max-width:820px){.wrap{grid-template-columns:1fr}}
.col{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px;min-width:0}
.dom{margin:6px 0}.dom>b{display:block;color:var(--acc);font-size:13px;letter-spacing:.02em;margin:10px 0 4px}
.fam{display:flex;justify-content:space-between;gap:8px;padding:6px 8px;border-radius:8px;cursor:pointer}.fam:hover,.fam.on{background:color-mix(in srgb,var(--acc) 14%,transparent)}
.fam small{color:var(--mut)}.pill{display:inline-block;padding:1px 8px;border-radius:99px;border:1px solid var(--line);font-size:12px;margin:2px;white-space:nowrap}
.req{border-color:var(--req);color:var(--req)}.scr{border-color:var(--scr);color:var(--scr)}.tst{border-color:var(--tst);color:var(--tst)}.ok{color:var(--ok)}
h2{font-size:16px;margin:4px 0 8px}h3{font-size:13px;color:var(--mut);margin:14px 0 6px;font-weight:600}code{font-size:12px;word-break:break-all}
.meter{height:6px;background:var(--line);border-radius:4px;overflow:hidden;margin:6px 0}.meter i{display:block;height:100%;background:var(--ok)}
footer{color:var(--mut);font-size:12px;padding:0 16px 24px}
</style></head><body>
<header><h1>خريطة القدرات المترابطة — Capability graph</h1>
<p id="sum"></p></header>
<div class="bar"><input id="q" placeholder="ابحث: عائلة، أداة، سكربت… / search family, requirement, script"></div>
<div class="wrap"><div class="col" id="tree"></div><div class="col" id="detail"><h2>اختر عائلة / pick a family</h2><p style="color:var(--mut)">كل عائلة تُظهر ما تحتاجه (المستلزمات)، والسكربتات التي تنفّذها، والاختبارات التي تثبتها.</p></div></div>
<footer id="foot"></footer>
<script>
const G=""" + payload + """;
const N=Object.fromEntries(G.nodes.map(n=>[n.id,n]));const out={},inn={};
for(const e of G.edges){(out[e.from]??=[]).push(e);(inn[e.to]??=[]).push(e)}
const fams=G.nodes.filter(n=>n.kind==='family');const total=fams.reduce((a,f)=>a+f.count,0),prov=fams.reduce((a,f)=>a+f.proven,0);
document.getElementById('sum').textContent=`${total.toLocaleString()} قدرة · ${fams.length} عائلة · ✅ ${prov} · ${G.nodes.filter(n=>n.kind==='requirement').length} مستلزمًا · ${G.nodes.filter(n=>n.kind==='script').length} سكربتًا · ${G.nodes.filter(n=>n.kind==='test').length} ملف اختبار`;
document.getElementById('foot').textContent=`Code layer: local AST pass + Graphify index @ ${G.graphify.commit||'—'} (${G.graphify_import_edges_confirmed_locally} import edges confirmed). Generated by scripts/capability_graph.py.`;
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function tree(q=''){q=q.toLowerCase();const t=document.getElementById('tree');let h='';
 for(const d of (out.root||[]).map(e=>N[e.to]).filter((v,i,a)=>a.indexOf(v)===i)){
  const fs=(out[d.id]||[]).map(e=>N[e.to]).filter(f=>!q||JSON.stringify([f,(out[f.id]||[]).map(e=>N[e.to].label)]).toLowerCase().includes(q));
  if(!fs.length)continue;h+=`<div class="dom"><b>${esc(d.label)}</b>`;
  for(const f of fs.sort((a,b)=>b.count-a.count))h+=`<div class="fam" data-id="${esc(f.id)}"><span>${esc(f.ar||f.label)} <small>${esc(f.prefix)}</small></span><small>${f.count} · <span class="ok">✅${f.proven}</span></small></div>`;
  h+='</div>'}
 t.innerHTML=h||'<p>لا نتائج / no match</p>';t.querySelectorAll('.fam').forEach(el=>el.onclick=()=>{t.querySelectorAll('.fam').forEach(x=>x.classList.remove('on'));el.classList.add('on');show(el.dataset.id)})}
function show(id){const f=N[id];const o=out[id]||[];const req=o.filter(e=>e.rel==='needs').map(e=>[N[e.to],e.w]);const scr=o.filter(e=>e.rel==='runs').map(e=>[N[e.to],e.w]);
 const tests=[...new Set(scr.flatMap(([s])=>(out[s.id]||[]).filter(e=>e.rel==='tested_by').map(e=>N[e.to].label)))];
 const st=Object.entries(f.status).map(([k,v])=>`${k} ${v}`).join(' · ');
 let h=`<h2>${esc(f.ar)} — ${esc(f.label)}</h2><div class="meter"><i style="width:${(100*f.proven/f.count).toFixed(1)}%"></i></div><small style="color:var(--mut)">${f.count} قدرة · ${esc(st)}</small>`;
 h+=`<h3>يحتاج / needs (عدد القدرات)</h3>`+(req.length?req.map(([r,w])=>`<span class="pill req" title="${esc(r.install)}">${esc(r.label)} · ${w}</span>`).join(''):'<small>لا شيء خارجي — Claude والمهارة فقط</small>');
 h+=`<h3>تُنفَّذ بـ / executed by</h3>`+(scr.length?scr.map(([s,w])=>`<span class="pill scr">${esc(s.label)}${s.executor_score?' ★':''}</span>`).join(''):'<small>إجراءات يطبقها Claude مباشرة</small>');
 h+=`<h3>تثبتها اختبارات / proven by tests</h3>`+(tests.length?tests.map(t=>`<span class="pill tst">${esc(t)}</span>`).join(''):'<small>—</small>');
 h+=`<h3>أوامر / commands</h3><code>python3 scripts/powers.py family ${esc(id.slice(4))}</code><br><code>python3 scripts/requirements.py plan "&lt;task&gt;"</code>`;
 document.getElementById('detail').innerHTML=h}
document.getElementById('q').oninput=e=>tree(e.target.value);tree();
</script></body></html>
"""


def cmd_stats():
    d = json.loads(OUT_JSON.read_text(encoding="utf-8"))
    print(Counter(n["kind"] for n in d["nodes"]), Counter(e["rel"] for e in d["edges"]))
    return 0


def cmd_path(key: str):
    d = json.loads(OUT_JSON.read_text(encoding="utf-8"))
    ids = [n["id"] for n in d["nodes"] if key.lower() in n["id"].lower() or key.lower() == str(n.get("prefix", "")).lower()]
    if not ids:
        print("no node"); return 1
    for i in ids[:3]:
        print(f"# {i}")
        for e in d["edges"]:
            if e["from"] == i:
                print(f"  → {e['rel']:>12} {e['to']} ({e['w']})")
            if e["to"] == i:
                print(f"  ← {e['rel']:>12} {e['from']} ({e['w']})")
    return 0


if __name__ == "__main__":
    if hasattr(signal, "SIGPIPE"):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")
    b = sub.add_parser("build", help="write (or --check) the graph JSON and HTML")
    b.add_argument("--check", action="store_true"); b.add_argument("--out-dir")
    sub.add_parser("stats", help="node/edge counts per layer")
    pa = sub.add_parser("path", help="neighbours of one node"); pa.add_argument("key")
    a = ap.parse_args()
    if a.cmd in (None, "build"):
        sys.exit(build(check=getattr(a, "check", False), out_dir=getattr(a, "out_dir", None)))
    sys.exit(cmd_stats() if a.cmd == "stats" else cmd_path(a.key))
