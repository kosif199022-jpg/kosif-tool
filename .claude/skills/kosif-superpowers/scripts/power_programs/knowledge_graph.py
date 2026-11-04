"""Programs for the knowledge-graph family.

The Graphify CLI and hosted MCP are not installed (GRAPH-01..14 are skipped). The graph methods
that need no Graphify runtime run here on self-built fixtures: index-freshness honesty, a
codebase map from Python ASTs (god nodes), constrained vocabulary expansion, discrete
confidence labels, a seeded force layout with BFS draw-on frames, Graph RAG with modularity
communities, and dual-level retrieval with incremental merges.
"""
from __future__ import annotations
import ast
import re
from collections import Counter, defaultdict, deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from ._lang_common import save, eq, truth, words


# ---------- GRAPH-15 index-snapshot honesty ----------
def freshness_report(answer_meta, head, changed_files, query_files):
    stale = answer_meta["commit"] != head
    unindexed = sorted(set(query_files) & set(changed_files)) if stale else []
    rep = {"repo": answer_meta["repo"], "graph_source": "hosted", "indexed_at": answer_meta["indexed_at"],
           "indexed_commit": answer_meta["commit"], "head": head, "stale": stale,
           "nodes": answer_meta["nodes"], "edges": answer_meta["edges"]}
    if unindexed:
        rep["fallback"] = {"files": unindexed, "source": "local CLI or grep", "status": "GRAPHIFY_NOT_EXECUTED",
                           "next_step": "graphify extract --code-only on the working tree"}
    return rep


def g15(work: Path):
    meta = {"repo": "kosif-tool", "indexed_at": "2026-10-18T10:00Z", "commit": "629a59b", "nodes": 1255, "edges": 2135}
    r = freshness_report(meta, "8f1c2d0", ["tools/aspects.py", "README.md"], ["tools/aspects.py", "tools/kosif.py"])
    r2 = freshness_report(meta, "629a59b", [], ["tools/kosif.py"])
    save(work, "freshness.json", {"diverged": r, "fresh": r2})
    req = {"repo", "graph_source", "indexed_at", "nodes", "edges"}
    return [eq("diverged index detected", r["stale"], True),
            eq("unindexed file routed to local source", r["fallback"]["files"], ["tools/aspects.py"]),
            eq("not-executed label", r["fallback"]["status"], "GRAPHIFY_NOT_EXECUTED"),
            truth("report fields present", req <= set(r)), eq("matching commit is fresh", r2["stale"], False)]


# ---------- GRAPH-16 understand a codebase fast ----------
def import_graph(root: Path):
    edges = []
    for f in sorted(root.glob("*.py")):
        tree = ast.parse(f.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                edges.append((f.stem, node.module.split(".")[0]))
            elif isinstance(node, ast.Import):
                edges += [(f.stem, a.name.split(".")[0]) for a in node.names]
    local = {f.stem for f in root.glob("*.py")}
    return [(a, b) for a, b in edges if b in local]


def skill_index(root: Path):
    rows = []
    for sk in sorted(root.glob("*/SKILL.md")):
        text = sk.read_text()
        fm = re.match(r"---\n(.*?)\n---", text, re.S).group(1)
        meta = dict(l.split(": ", 1) for l in fm.splitlines() if ": " in l)
        rows.append({"name": meta["name"], "description": meta["description"], "lines": len(text.splitlines())})
    return rows


def g16(work):
    code = work / "repo"
    code.mkdir()
    (code / "core.py").write_text("def build():\n    return 1\n")
    for m in ("cli", "render", "export", "lint"):
        (code / f"{m}.py").write_text("from core import build\nimport json\n")
    (code / "render.py").write_text("from core import build\nimport export\n")
    edges = import_graph(code)
    deg = Counter(b for _, b in edges) + Counter(a for a, _ in edges)
    god = deg.most_common(1)[0][0]
    sk = work / "skills"
    for n, d in (("caption-ar", "Arabic captions"), ("beat-cut", "cut on beats")):
        (sk / n).mkdir(parents=True)
        (sk / n / "SKILL.md").write_text(f"---\nname: {n}\ndescription: {d}\n---\n# {n}\nbody\n")
    idx = skill_index(sk)
    nfiles = 612
    gate = "pick a subfolder" if nfiles > 500 else "map whole repo"
    save(work, "onboarding.json", {"edges": edges, "god_node": god, "skills": idx, "size_gate": gate})
    return [eq("local import edges", len(edges), 5), eq("god node = core abstraction", god, "core"),
            eq("skill index rows", [(r["name"], r["lines"]) for r in idx], [("beat-cut", 6), ("caption-ar", 6)]),
            eq(">500 files -> subfolder", gate, "pick a subfolder")]


# ---------- GRAPH-18 constrained vocabulary expansion ----------
TRANSLATE = {"فيديو": "video", "ترجمة": "caption", "قص": "cut", "صوت": "audio"}


def expand(question, labels, cap=12):
    vocab = Counter(t for l in labels for t in re.split(r"[_\W]+", l.lower()) if len(t) > 2)
    out = []
    for w in words(question):
        cands = [w, TRANSLATE.get(w)]
        for c in cands:
            if c and c in vocab and c not in out:
                out.append(c)
    return out[:cap]


def traversal_for(q):
    q = q.lower()
    if "break" in q or "affected" in q:
        return "affected"
    if re.search(r"how does .* reach|how .* gets? to", q):
        return "DFS"
    if "related" in q:
        return "path"
    return "BFS"


def g18(work):
    labels = ["build_prompt()", "render_video()", "caption_lines()", "cut_on_beats()", "audio_mix()",
              "export_profile()", "video_eyes()"]
    e1 = expand("كيف نعمل ترجمة فيديو", labels)
    e2 = expand("قصيدة جميلة", labels)
    big = expand(" ".join(f"tok{i}" for i in range(30)), [f"tok{i}_x" for i in range(30)])
    trav = [traversal_for(q) for q in ("what breaks if I change x", "how does main reach render",
                                       "are a and b related", "what is connected to export")]
    save(work, "expansion.json", {"e1": e1, "e2": e2, "traversal": trav})
    return [eq("Arabic words mapped only to tokens in the map", e1, ["caption", "video"]),
            eq("empty expansion -> stop", e2, []), eq("expansion capped at 12", len(big), 12),
            eq("traversal by question", trav, ["affected", "DFS", "path", "BFS"])]


# ---------- GRAPH-19 evidence labels ----------
STEPS = (0.95, 0.85, 0.75, 0.65, 0.55)


def label(edge):
    if edge.get("stated"):
        return ("EXTRACTED", None)
    c = edge["confidence"]
    if c < 0.55:
        return ("AMBIGUOUS", None)
    return ("INFERRED", min(STEPS, key=lambda s: (abs(s - c), -s)))


def g19(work):
    edges = [{"id": 1, "stated": True}, {"id": 2, "confidence": 0.93}, {"id": 3, "confidence": 0.71},
             {"id": 4, "confidence": 0.56}, {"id": 5, "confidence": 0.5}, {"id": 6, "confidence": 0.2}]
    lab = [(e["id"],) + label(e) for e in edges]
    save(work, "labels.json", lab)
    kept = [l for l in lab if l[1] == "AMBIGUOUS"]
    return [eq("stated -> EXTRACTED", lab[0][1], "EXTRACTED"),
            eq("snapped to discrete steps", [l[2] for l in lab[1:4]], [0.95, 0.75, 0.55]),
            truth("0.5 is never a default: becomes AMBIGUOUS", lab[4][1] == "AMBIGUOUS"),
            eq("ambiguous kept, not dropped", len(kept), 2), eq("all edges kept", len(lab), 6)]


# ---------- GRAPH-20 map as motion graphics ----------
def force_layout(nodes, edges, seed=7, iters=200):
    rng = np.random.default_rng(seed)
    pos = rng.uniform(-1, 1, (len(nodes), 2))
    idx = {n: i for i, n in enumerate(nodes)}
    for _ in range(iters):
        d = pos[:, None, :] - pos[None, :, :]
        dist = np.linalg.norm(d, axis=2) + 1e-3
        rep = (d / dist[..., None] ** 3).sum(axis=1) * 0.01
        att = np.zeros_like(pos)
        for a, b in edges:
            i, j = idx[a], idx[b]
            v = pos[j] - pos[i]
            att[i] += v * 0.05
            att[j] -= v * 0.05
        pos += rep + att
        pos -= pos.mean(axis=0)
    return pos


def bfs_order(edges, start):
    adj = defaultdict(list)
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    seen, q, order = {start}, deque([start]), []
    while q:
        n = q.popleft()
        for m in sorted(adj[n]):
            if m not in seen:
                seen.add(m)
                order.append((n, m))
                q.append(m)
    return order


def draw_frame(pos, nodes, order, t, size=96):
    im = Image.new("RGB", (size, size), (10, 10, 14))
    dr = ImageDraw.Draw(im)
    span = np.abs(pos).max() or 1
    xy = {n: tuple(((pos[i] / span) * 0.4 + 0.5) * size) for i, n in enumerate(nodes)}
    k = int(round(t * len(order)))
    for a, b in order[:k]:
        dr.line([xy[a], xy[b]], fill=(255, 200, 0), width=1)
    return im, k


def g20(work):
    nodes = ["core", "cli", "render", "export", "lint", "audio"]
    edges = [("core", "cli"), ("core", "render"), ("render", "export"), ("core", "lint"), ("render", "audio")]
    p1, p2 = force_layout(nodes, edges), force_layout(nodes, edges)
    order = bfs_order(edges, "core")
    f0, k0 = draw_frame(p1, nodes, order, 0.0)
    f1, k1 = draw_frame(p1, nodes, order, 1.0)
    f0.save(work / "frame_000.png")
    f1.save(work / "frame_end.png")
    a0 = np.asarray(f0)
    a1 = np.asarray(f1)
    return [truth("fixed seed -> identical layout", np.allclose(p1, p2)),
            eq("BFS draw-on order", order[:3], [("core", "cli"), ("core", "lint"), ("core", "render")]),
            eq("t=0 nothing drawn", int((a0[..., 0] == 255).sum()), 0),
            truth("t=1 all edges drawn", k1 == len(edges) and (a1[..., 0] == 255).sum() > 20, (k1, int((a1[..., 0] == 255).sum())))]


# ---------- GRAPH-22 Graph RAG ----------
REL = re.compile(r"(\b[A-Z][a-z]+\b) (founded|leads|acquired|partners with|funds) (\b[A-Z][a-z]+\b)")


def extract(chunks):
    ents, rels = {}, []
    for cid, text in chunks.items():
        for a, r, b in REL.findall(text):
            for e in (a, b):
                ents.setdefault(e.lower(), {"name": e, "chunks": set()})["chunks"].add(cid)
            rels.append((a.lower(), r, b.lower(), cid))
    return ents, rels


def modularity_communities(nodes, edges):
    """Greedy agglomerative modularity (Clauset-Newman-Moore style, small graphs)."""
    m = len(edges)
    deg = Counter()
    for a, b in edges:
        deg[a] += 1
        deg[b] += 1
    comm = {n: {n} for n in nodes}

    def q(cs):
        tot = 0.0
        for c in cs:
            lc = sum(1 for a, b in edges if a in c and b in c)
            dc = sum(deg[n] for n in c)
            tot += lc / m - (dc / (2 * m)) ** 2
        return tot
    cur = list(comm.values())
    best = q(cur)
    while True:
        cand = None
        for i in range(len(cur)):
            for j in range(i + 1, len(cur)):
                if not any((a in cur[i] and b in cur[j]) or (a in cur[j] and b in cur[i]) for a, b in edges):
                    continue
                trial = [c for k, c in enumerate(cur) if k not in (i, j)] + [cur[i] | cur[j]]
                v = q(trial)
                if cand is None or v > cand[0]:
                    cand = (v, trial)
        if not cand or cand[0] <= best:
            return cur, best
        best, cur = cand


def g22(work):
    chunks = {"c1": "Amal founded Nexa. Amal leads Nexa.", "c2": "Nexa acquired Lumo. Lumo partners with Nexa.",
              "c3": "Karim founded Sahl. Sahl acquired Wadi.", "c4": "Wadi partners with Sahl. Karim leads Wadi.",
              "c5": "Lumo funds Wadi."}
    ents, rels = extract(chunks)
    edges = sorted({tuple(sorted((a, b))) for a, _, b, _ in rels})
    comms, qv = modularity_communities(sorted(ents), edges)
    comms = sorted(sorted(c) for c in comms)
    summaries = [{"members": c, "summary": ", ".join(ents[n]["name"] for n in c)} for c in comms]

    def local(entity):
        nb = sorted({b if a == entity else a for a, b in edges if entity in (a, b)})
        cids = sorted({cid for a, _, b, cid in rels if entity in (a, b)})
        return nb, cids
    nb, cids = local("karim")
    save(work, "graph_rag.json", {"entities": {k: sorted(v["chunks"]) for k, v in ents.items()}, "edges": edges,
                                  "communities": summaries, "modularity": qv, "local_karim": [nb, cids]})
    return [eq("entities merged across chunks", len(ents), 6),
            eq("two communities split at the Lumo-Wadi bridge", comms,
               [["amal", "lumo", "nexa"], ["karim", "sahl", "wadi"]]),
            truth("modularity positive", qv > 0.3, round(qv, 3)),
            eq("local query: neighbours", nb, ["sahl", "wadi"]), eq("local query cites chunk ids", cids, ["c3", "c4"])]


# ---------- GRAPH-23 dual-level retrieval + incremental update ----------
class DualGraph:
    def __init__(self):
        self.nodes = {}
        self.rels = []

    def merge(self, doc_id, entities, relations):
        for name, typ in entities:
            key = (name.lower(), typ)
            self.nodes.setdefault(key, {"name": name, "type": typ, "docs": set()})["docs"].add(doc_id)
        for a, theme, b in relations:
            self.rels.append({"a": a.lower(), "b": b.lower(), "theme": theme, "doc": doc_id})

    def query(self, low, high):
        hits = Counter()
        for (n, _), v in self.nodes.items():
            if n in [w.lower() for w in low]:
                for d in v["docs"]:
                    hits[d] += 2
        for r in self.rels:
            if any(h in r["theme"] for h in high):
                hits[r["doc"]] += 1
        return [d for d, _ in sorted(hits.items(), key=lambda x: (-x[1], x[0]))]


def g23(work):
    g = DualGraph()
    g.merge("d1", [("Cairo", "city"), ("Metro", "system")], [("Metro", "public transport expansion", "Cairo")])
    g.merge("d2", [("Giza", "city")], [("Giza", "tourism growth", "Giza")])
    n_before = len(g.nodes)
    g.merge("d3", [("cairo", "city"), ("Monorail", "system")], [("Monorail", "public transport", "Cairo")])
    res = g.query(low=["Cairo"], high=["transport"])
    save(work, "dual_graph.json", {"nodes": {f"{k[0]}|{k[1]}": sorted(v["docs"]) for k, v in g.nodes.items()},
                                   "query": res})
    return [eq("incremental merge by name+type (cairo not duplicated)", len(g.nodes), n_before + 1),
            eq("merged node keeps both docs", sorted(g.nodes[("cairo", "city")]["docs"]), ["d1", "d3"]),
            eq("low+high union ranked", res, ["d1", "d3"]),
            truth("unrelated doc excluded", "d2" not in res)]


PROGRAMS = {"GRAPH-15": g15, "GRAPH-16": g16, "GRAPH-18": g18, "GRAPH-19": g19, "GRAPH-20": g20,
            "GRAPH-22": g22, "GRAPH-23": g23}
