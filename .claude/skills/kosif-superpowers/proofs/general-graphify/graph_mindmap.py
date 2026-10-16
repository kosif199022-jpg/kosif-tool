#!/usr/bin/env python3
"""graph -> communities -> mind map / من الخريطة إلى خريطة ذهنية.

Reads a graphify `graph.json` (NetworkX node-link) and prints a Mermaid
mindmap plus a plain Markdown outline:
  root = corpus, branch = community (named after its dominant source file),
  leaves = the most-connected symbols in that community, and a final list of
  the strongest cross-community bridges (where to look for coupling).
Python 3 standard library only. Never executes anything from the graph:
labels are treated as data and sanitised.

  python3 -I graph_mindmap.py graphify-out/graph.json [--top 5] [--title NAME]
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


def clean(label: str) -> str:
    # Mermaid treats ()[]{} as shape syntax; strip them and control chars.
    s = re.sub(r"[\x00-\x1f()\[\]{}\"`<>]", "", str(label or ""))
    return s.strip()[:60] or "?"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("graph")
    ap.add_argument("--top", type=int, default=5, help="leaves per community")
    ap.add_argument("--title", default="")
    a = ap.parse_args()

    g = json.loads(Path(a.graph).read_text(encoding="utf-8"))
    nodes = {n["id"]: n for n in g.get("nodes", [])}
    links = g.get("links") or g.get("edges") or []
    deg: Counter = Counter()
    pair: Counter = Counter()
    for e in links:
        s, t = e.get("source"), e.get("target")
        if s not in nodes or t not in nodes:
            continue
        deg[s] += 1
        deg[t] += 1
        # bridges: only edges between project symbols (stdlib hubs have no source file)
        if not (nodes[s].get("source_file") and nodes[t].get("source_file")):
            continue
        cs, ct = nodes[s].get("community"), nodes[t].get("community")
        if cs is not None and ct is not None and cs != ct:
            pair[tuple(sorted((cs, ct)))] += 1

    members: dict = defaultdict(list)
    for nid, n in nodes.items():
        members[n.get("community")].append(nid)

    def name_of(c) -> str:
        files = Counter(nodes[i].get("source_file") for i in members[c] if nodes[i].get("source_file"))
        top = files.most_common(2)
        if not top:
            return f"community {c}"
        name = Path(top[0][0]).name
        return name + (f" +{len(files) - 1}" if len(files) > 1 else "")

    order = sorted(members, key=lambda c: -len(members[c]))
    title = clean(a.title or Path(a.graph).resolve().parent.parent.name)
    names = {c: name_of(c) for c in order}

    print("```mermaid\nmindmap\n  root((" + title + "))")
    for c in order:
        # skip stdlib/import hubs (no source file) as leaves: they are noise
        leaves = [i for i in sorted(members[c], key=lambda i: -deg[i]) if nodes[i].get("source_file")][: a.top]
        print(f"    c{c}[{clean(names[c])} · {len(members[c])}]")
        for i in leaves:
            print(f"      {clean(nodes[i].get('label'))}")
    print("```\n")

    print(f"# {title}: {len(nodes)} nodes, {len(links)} edges, {len(order)} communities\n")
    for c in order:
        leaves = [i for i in sorted(members[c], key=lambda i: -deg[i]) if nodes[i].get("source_file")][: a.top]
        print(f"- **{names[c]}** (community {c}, {len(members[c])} nodes): " + ", ".join(f"`{clean(nodes[i].get('label'))}` ({deg[i]})" for i in leaves))
    print("\n## Bridges (cross-community edges)")
    for (x, y), k in pair.most_common(5):
        print(f"- {names[x]} <-> {names[y]}: {k} edges")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
