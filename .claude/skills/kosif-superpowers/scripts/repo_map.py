#!/usr/bin/env python3
"""Repo map: the most important files and symbols of a codebase in a small budget / خريطة المستودع.

Reads source files statically (Python through ast, JavaScript/TypeScript, Go and Rust through line patterns), finds
where each name is defined and which other files mention it, ranks files with PageRank over that reference graph
(optionally pulled toward focus files or words), and prints the top files with their definition lines until a
character budget is spent. A coding agent gets the shape of a repository without reading all of it.

    python3 scripts/repo_map.py map <dir> [--budget 6000] [--focus <file-or-word> ...] [--json]
    python3 scripts/repo_map.py defs <dir> <name>          # where a name is defined and who mentions it
    python3 scripts/repo_map.py --self-test

Read-only: it parses text and never imports, runs or builds anything from the target, so it is safe on an untrusted
checkout. The idea of a ranked repository map comes from Aider (Apache-2.0); this is our own stdlib implementation.
Python 3.8+ standard library only.
"""
from __future__ import annotations

import argparse
import ast
import json
import math
import re
import sys
import tempfile
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", "venv", ".venv", "env", "__pycache__", "dist", "build", ".next", ".cache", "vendor",
             "target", "coverage", ".mypy_cache", ".pytest_cache", "site-packages", ".tox", "out"}
EXT = {".py": "py", ".js": "js", ".mjs": "js", ".cjs": "js", ".jsx": "js", ".ts": "js", ".tsx": "js", ".go": "go", ".rs": "rs"}
MAX_BYTES = 400_000
COMMON = {"self", "this", "cls", "none", "true", "false", "null", "undefined", "main", "test", "init", "data", "value",
          "name", "path", "file", "args", "kwargs", "result", "error", "options", "config", "index", "type", "list", "dict",
          "string", "number", "object", "console", "require", "module", "exports", "default", "return", "async", "await",
          "function", "const", "let", "var", "class", "import", "from", "export", "print", "len", "range", "open", "str",
          "int", "float", "bool", "json", "re", "os", "sys", "get", "set", "run", "new", "props", "state", "item", "items"}
JS_DEF = [
    (re.compile(r"^\s*(?:export\s+)?(?:default\s+)?(?:async\s+)?function\s*\*?\s*([A-Za-z_$][\w$]*)\s*\("), "function"),
    (re.compile(r"^\s*(?:export\s+)?(?:default\s+)?(?:abstract\s+)?class\s+([A-Za-z_$][\w$]*)"), "class"),
    (re.compile(r"^\s*(?:export\s+)?(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*(?::[^=]+)?=\s*(?:async\s*)?(?:\([^)]*\)|[A-Za-z_$][\w$]*)\s*=>"), "function"),
    (re.compile(r"^\s*(?:export\s+)?(?:interface|type|enum)\s+([A-Za-z_$][\w$]*)"), "type"),
]
GO_DEF = [(re.compile(r"^func\s+(?:\([^)]*\)\s*)?([A-Za-z_]\w*)\s*\("), "function"),
          (re.compile(r"^type\s+([A-Za-z_]\w*)\s+(?:struct|interface)"), "type")]
RS_DEF = [(re.compile(r"^\s*(?:pub(?:\([^)]*\))?\s+)?(?:async\s+)?fn\s+([A-Za-z_]\w*)"), "function"),
          (re.compile(r"^\s*(?:pub(?:\([^)]*\))?\s+)?(?:struct|enum|trait)\s+([A-Za-z_]\w*)"), "type")]
IDENT = re.compile(r"[A-Za-z_$][\w$]*")


def source_files(root: Path) -> list:
    out = []
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.suffix not in EXT:
            continue
        rel = p.relative_to(root)
        if any(part in SKIP_DIRS or (part.startswith(".") and part not in (".",)) for part in rel.parts[:-1]):
            continue
        if p.stat().st_size > MAX_BYTES or p.name.endswith((".min.js", ".d.ts")):
            continue
        out.append(p)
    return out


def py_defs(text: str) -> list:
    try:
        tree = ast.parse(text)
    except (SyntaxError, ValueError):
        return []
    lines = text.splitlines()
    defs = []
    kinds = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
    top = [n for n in tree.body if isinstance(n, kinds)]
    nodes = top + [m for c in top if isinstance(c, ast.ClassDef) for m in c.body if isinstance(m, kinds)]
    for node in nodes:  # module level and class members only: nested helpers are not part of the map
        sig = lines[node.lineno - 1].strip() if node.lineno - 1 < len(lines) else node.name
        kind = "class" if isinstance(node, ast.ClassDef) else "function"
        defs.append({"name": node.name, "line": node.lineno, "kind": kind, "sig": sig[:160]})
    return sorted(defs, key=lambda d: d["line"])


def pattern_defs(text: str, patterns: list) -> list:
    defs = []
    for i, line in enumerate(text.splitlines(), 1):
        for rx, kind in patterns:
            m = rx.match(line)
            if m:
                defs.append({"name": m.group(1), "line": i, "kind": kind, "sig": line.strip()[:160]})
                break
    return defs


def scan(root: Path) -> dict:
    """{rel_path: {"defs": [...], "idents": {name: count}}}"""
    files = {}
    for p in source_files(root):
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        lang = EXT[p.suffix]
        defs = py_defs(text) if lang == "py" else pattern_defs(text, {"js": JS_DEF, "go": GO_DEF, "rs": RS_DEF}[lang])
        idents = {}
        for m in IDENT.finditer(text):
            w = m.group(0)
            idents[w] = idents.get(w, 0) + 1
        files[p.relative_to(root).as_posix()] = {"defs": defs, "idents": idents, "lang": lang}
    return files


def graph(files: dict) -> tuple:
    """Weighted edges referrer -> definer, with names defined in many files damped (an idf over definers)."""
    definers = {}
    for f, info in files.items():
        for d in info["defs"]:
            n = d["name"]
            if len(n) < 4 or n.lower() in COMMON or n.startswith("_"):
                continue
            definers.setdefault(n, set()).add(f)
    edges, used = {}, {}
    nfiles = max(1, len(files))
    for f, info in files.items():
        for name, defs_in in definers.items():
            cnt = info["idents"].get(name, 0)
            if not cnt:
                continue
            others = defs_in - {f}
            own = f in defs_in
            mentions = cnt - (1 if own else 0)
            if not others or mentions <= 0:
                continue
            specific = 1.0 if ("_" in name.strip("_") or re.search(r"[a-z][A-Z]", name) or name[:1].isupper()) else 0.3
            w = specific * math.sqrt(mentions) * math.log(1 + nfiles / len(defs_in))
            for g in others:
                edges[(f, g)] = edges.get((f, g), 0.0) + w / len(others)
                used.setdefault(g, {}).setdefault(name, 0)
                used[g][name] += mentions
    return edges, used


def pagerank(nodes: list, edges: dict, personal: dict = None, damping: float = 0.85, iters: int = 60) -> dict:
    n = len(nodes)
    if not n:
        return {}
    pers = personal or {x: 1.0 for x in nodes}
    total = sum(pers.values()) or 1.0
    pers = {x: pers.get(x, 0.0) / total for x in nodes}
    out_w = {}
    for (a, b), w in edges.items():
        out_w[a] = out_w.get(a, 0.0) + w
    rank = {x: 1.0 / n for x in nodes}
    for _ in range(iters):
        nxt = {x: (1 - damping) * pers[x] for x in nodes}
        sink = sum(rank[x] for x in nodes if x not in out_w)
        for x in nodes:
            nxt[x] += damping * sink * pers[x]
        for (a, b), w in edges.items():
            nxt[b] += damping * rank[a] * w / out_w[a]
        rank = nxt
    return rank


def build_map(root: Path, budget: int = 6000, focus: list = None) -> dict:
    files = scan(root)
    nodes = sorted(files)
    edges, used = graph(files)
    personal = None
    if focus:
        personal = {}
        for f in nodes:
            score = 0.0
            for q in focus:
                ql = q.lower()
                if ql in f.lower():
                    score += 10.0
                if any(ql in d["name"].lower() for d in files[f]["defs"]):
                    score += 5.0
            personal[f] = score + 0.01
    rank = pagerank(nodes, edges, personal)
    ordered = sorted(nodes, key=lambda f: (-rank[f], f))
    blocks, spent, shown = [], 0, []
    for f in ordered:
        defs = files[f]["defs"]
        if not defs:
            continue
        hot = used.get(f, {})
        defs_sorted = sorted(defs, key=lambda d: (-hot.get(d["name"], 0), d["line"]))[:12]
        defs_sorted.sort(key=lambda d: d["line"])
        block = f + ":\n" + "".join(f"│ {d['line']:>4}: {d['sig']}\n" for d in defs_sorted)
        if spent + len(block) > budget:
            if not blocks:
                blocks.append(block[:budget])
                shown.append(f)
            break
        blocks.append(block)
        spent += len(block)
        shown.append(f)
    return {"root": str(root), "files_scanned": len(files), "definitions": sum(len(i["defs"]) for i in files.values()),
            "edges": len(edges), "budget": budget, "chars": sum(len(b) for b in blocks), "files_shown": len(shown),
            "ranking": [{"file": f, "rank": round(rank[f], 5)} for f in ordered[:40]], "map": "".join(blocks)}


def find_defs(root: Path, name: str) -> dict:
    files = scan(root)
    where = [{"file": f, "line": d["line"], "sig": d["sig"]} for f, i in sorted(files.items()) for d in i["defs"] if d["name"] == name]
    users = sorted((f, i["idents"][name]) for f, i in files.items() if name in i["idents"])
    return {"name": name, "defined": where, "mentioned_in": [{"file": f, "count": c} for f, c in users]}


def self_test() -> int:
    bad = []
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "core").mkdir()
        (root / "node_modules").mkdir()
        (root / "core" / "engine.py").write_text("class RenderEngine:\n    def render_frame(self, t):\n        return t\n\n"
                                                 "def load_scene(path):\n    return path\n", encoding="utf-8")
        (root / "app.py").write_text("from core.engine import RenderEngine, load_scene\n\ndef main_loop():\n"
                                     "    e = RenderEngine()\n    s = load_scene('a')\n    e.render_frame(1)\n    e.render_frame(2)\n", encoding="utf-8")
        (root / "cli.py").write_text("from app import main_loop\n\ndef cli_entry():\n    main_loop()\n", encoding="utf-8")
        (root / "web.ts").write_text("export function drawTimeline(ctx: any) { return ctx }\nexport const easeOut = (t: number) => 1 - (1 - t) ** 2\n"
                                     "export class Scene {}\n", encoding="utf-8")
        (root / "ui.tsx").write_text("import { drawTimeline, easeOut, Scene } from './web'\nconst s = new Scene(); drawTimeline(easeOut(0.5))\n", encoding="utf-8")
        (root / "node_modules" / "junk.js").write_text("function ignored() {}\n", encoding="utf-8")
        (root / "broken.py").write_text("def oops(:\n", encoding="utf-8")
        m = build_map(root, budget=4000)
        ranking = [r["file"] for r in m["ranking"]]
        if ranking[0] not in ("core/engine.py", "web.ts"):
            bad.append(("top file", ranking[:3]))
        if any("node_modules" in r for r in ranking):
            bad.append("node_modules not skipped")
        if "class RenderEngine" not in m["map"] or "export function drawTimeline" not in m["map"]:
            bad.append(("defs in map", m["map"]))
        small = build_map(root, budget=60)
        if small["chars"] > 60:
            bad.append(("budget", small["chars"]))
        foc = build_map(root, budget=4000, focus=["cli"])
        if foc["ranking"][0]["file"] != "cli.py":
            bad.append(("focus", foc["ranking"][:2]))
        fd = find_defs(root, "load_scene")
        if fd["defined"][0]["file"] != "core/engine.py" or not any(u["file"] == "app.py" for u in fd["mentioned_in"]):
            bad.append(("defs", fd))
        if build_map(root) != build_map(root):
            bad.append("determinism")
    for b in bad:
        print("FAIL", b)
    print("self-test OK" if not bad else f"self-test: {len(bad)} failure(s)")
    return 1 if bad else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--self-test", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    m = sub.add_parser("map")
    m.add_argument("dir")
    m.add_argument("--budget", type=int, default=6000, help="characters of map to print (≈ tokens × 4)")
    m.add_argument("--focus", nargs="*", default=[], help="files or words to pull the ranking toward")
    m.add_argument("--json", action="store_true")
    d = sub.add_parser("defs")
    d.add_argument("dir")
    d.add_argument("name")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if a.cmd == "map":
        root = Path(a.dir)
        if not root.is_dir():
            ap.error(f"not a folder: {root}")
        res = build_map(root, a.budget, a.focus)
        if a.json:
            print(json.dumps(res, ensure_ascii=False, indent=1))
        else:
            print(res["map"], end="")
            print(f"— {res['files_shown']} of {res['files_scanned']} files · {res['definitions']} definitions · "
                  f"{res['edges']} reference edges · {res['chars']}/{res['budget']} chars")
        return 0
    if a.cmd == "defs":
        print(json.dumps(find_defs(Path(a.dir), a.name), ensure_ascii=False, indent=1))
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
