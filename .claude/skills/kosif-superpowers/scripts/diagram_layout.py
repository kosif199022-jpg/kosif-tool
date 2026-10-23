#!/usr/bin/env python3
"""KOSIF diagram layout — lint, deterministic layered layout and SVG for node/edge diagrams.

تخطيط المخططات: فحص الرسم البياني وتخطيط طبقي حتمي وتصدير SVG بألوان الأدوار وعناوين عربية من اليمين لليسار.
Diagram layout: graph lint, deterministic layered (longest-path) layout and SVG export with role colours,
arrow markers and Arabic labels (direction rtl). Standard library only, no network.

graph.json: {"nodes": [{"id": "a", "label": "...", "role": "frontend|backend|data|cloud|security|bus|user|external"}],
             "edges": [{"from": "a", "to": "b", "label": "..."}], "direction": "lr|tb" (optional)}

Subcommands (run from the skill root):
  lint graph.json [--max-label 24] [--max-nodes 9]
      dangling edges, duplicate ids, self-loops, cycles (strongly connected components), orphan nodes,
      long labels, too many nodes for one diagram, unlabelled edges
      e.g. python3 scripts/diagram_layout.py lint graph.json
  layout graph.json [--rtl] [--direction lr|tb]
      layer = longest path from a source (cycle edges are reversed and reported); in-layer order by
      the mean position of predecessors (input order breaks ties); pixel boxes and edge anchor points;
      --rtl mirrors x (x' = W - x - w) so the flow reads right to left
      e.g. python3 scripts/diagram_layout.py layout graph.json --rtl
  svg graph.json [--rtl] [--direction lr|tb] [--out FILE.svg] [--theme dark|light]
      SVG in paint order background > connectors > boxes > labels, role colours, arrow markers;
      Arabic labels carry direction="rtl", Latin labels inside an RTL diagram are isolated as ltr
      e.g. python3 scripts/diagram_layout.py svg graph.json --rtl --out /tmp/flow.svg
  --self-test   offline check, exits 0 on success

lint and layout print JSON; svg prints the SVG (or writes only the --out file). Bad input exits 2.
"""
import argparse
import json
import re
import sys
from xml.sax.saxutils import escape

NODE_W, NODE_H, GAP_MAIN, GAP_CROSS, MARGIN = 180, 80, 90, 40, 40
ROLE = {"dark": {"frontend": "#22d3ee", "backend": "#34d399", "data": "#a78bfa", "cloud": "#fbbf24",
                 "security": "#fb7185", "bus": "#fb923c", "user": "#e2e8f0", "external": "#94a3b8",
                 "default": "#94a3b8", "bg": "#0f172a", "fill": "#1e293b", "text": "#f8fafc", "edge": "#cbd5e1"},
        "light": {"frontend": "#0891b2", "backend": "#059669", "data": "#7c3aed", "cloud": "#d97706",
                  "security": "#e11d48", "bus": "#ea580c", "user": "#334155", "external": "#64748b",
                  "default": "#64748b", "bg": "#ffffff", "fill": "#f8fafc", "text": "#111111", "edge": "#333333"}}
AR = re.compile(r"[؀-ۿݐ-ݿ]")


class Bad(Exception):
    pass


def load(path):
    try:
        with open(path, encoding="utf-8") as fh:
            g = json.load(fh)
    except (OSError, ValueError) as e:
        raise Bad("cannot read JSON %s: %s" % (path, e))
    if not isinstance(g, dict) or not isinstance(g.get("nodes"), list):
        raise Bad("graph needs a 'nodes' list")
    edges = g.get("edges", [])
    if not isinstance(edges, list):
        raise Bad("'edges' must be a list")
    for i, n in enumerate(g["nodes"]):
        if not isinstance(n, dict) or not str(n.get("id", "")).strip():
            raise Bad("node %d needs an 'id'" % (i + 1))
    for i, e in enumerate(edges):
        if not isinstance(e, dict) or "from" not in e or "to" not in e:
            raise Bad("edge %d needs 'from' and 'to'" % (i + 1))
    g["edges"] = edges
    return g


def ids(g):
    return [str(n["id"]) for n in g["nodes"]]


def sccs(nodes, adj):
    """Tarjan, iterative, deterministic order."""
    index, low, on, stack, out, c = {}, {}, set(), [], [], [0]
    for root in nodes:
        if root in index:
            continue
        work = [(root, 0)]
        while work:
            v, i = work.pop()
            if i == 0:
                index[v] = low[v] = c[0]
                c[0] += 1
                stack.append(v)
                on.add(v)
            nb = adj.get(v, [])
            if i < len(nb):
                work.append((v, i + 1))
                w = nb[i]
                if w not in index:
                    work.append((w, 0))
                elif w in on:
                    low[v] = min(low[v], index[w])
                continue
            for w in nb:
                if w in on and index[w] > index[v]:
                    low[v] = min(low[v], low[w])
            if low[v] == index[v]:
                comp = []
                while True:
                    w = stack.pop()
                    on.discard(w)
                    comp.append(w)
                    if w == v:
                        break
                out.append(sorted(comp, key=nodes.index))
    return out


def lint(g, max_label=24, max_nodes=9):
    f = []
    seen, dup = set(), []
    for i in ids(g):
        if i in seen:
            dup.append(i)
        seen.add(i)
    for d in dup:
        f.append({"code": "DUPLICATE_ID", "severity": "error", "id": d})
    nodes = list(dict.fromkeys(ids(g)))
    adj, touched = {n: [] for n in nodes}, set()
    for k, e in enumerate(g["edges"]):
        a, b = str(e["from"]), str(e["to"])
        miss = [x for x in (a, b) if x not in seen]
        if miss:
            f.append({"code": "DANGLING_EDGE", "severity": "error", "edge": k, "from": a, "to": b, "missing": miss})
            continue
        touched.update((a, b))
        if a == b:
            f.append({"code": "SELF_LOOP", "severity": "warn", "edge": k, "id": a})
        if b not in adj[a]:
            adj[a].append(b)
        if not str(e.get("label", "")).strip():
            f.append({"code": "UNLABELLED_EDGE", "severity": "info", "edge": k, "from": a, "to": b})
        elif len(str(e["label"])) > max_label:
            f.append({"code": "LONG_LABEL", "severity": "warn", "edge": k, "length": len(str(e["label"]))})
    cycles = [c for c in sccs(nodes, adj) if len(c) > 1]
    for c in cycles:
        f.append({"code": "CYCLE", "severity": "warn", "nodes": c})
    for n in g["nodes"]:
        i = str(n["id"])
        if i not in touched and len(nodes) > 1:
            f.append({"code": "ORPHAN", "severity": "warn", "id": i})
        lab = str(n.get("label", i))
        if len(lab) > max_label:
            f.append({"code": "LONG_LABEL", "severity": "warn", "id": i, "length": len(lab)})
    if len(nodes) > max_nodes:
        f.append({"code": "TOO_MANY_NODES", "severity": "warn", "count": len(nodes), "max": max_nodes,
                  "fix": "split into two diagrams or chapters"})
    errors = sum(x["severity"] == "error" for x in f)
    return {"kind": "kosif.diagram_layout.lint.v1", "nodes": len(nodes), "edges": len(g["edges"]),
            "cycles": cycles, "errors": errors,
            "warnings": sum(x["severity"] == "warn" for x in f),
            "verdict": "fail" if errors else "pass", "findings": f}


def layout(g, rtl=False, direction=None):
    rep = lint(g)
    if rep["errors"]:
        raise Bad("graph has %d lint error(s); run lint first" % rep["errors"])
    direction = (direction or g.get("direction") or "lr").lower()
    if direction not in ("lr", "tb"):
        raise Bad("direction must be lr or tb")
    nodes = ids(g)
    pos = {n: k for k, n in enumerate(nodes)}
    # remove cycles: DFS in input order, back edges are reversed
    adj = {n: [] for n in nodes}
    for e in g["edges"]:
        a, b = str(e["from"]), str(e["to"])
        if a != b and b not in adj[a]:
            adj[a].append(b)
    state, reversed_edges = {}, []
    for r in nodes:
        if r in state:
            continue
        state[r] = 1
        work = [(r, iter(adj[r]))]
        while work:
            v, it = work[-1]
            w = next(it, None)
            if w is None:
                state[v] = 2
                work.pop()
            elif w not in state:
                state[w] = 1
                work.append((w, iter(adj[w])))
            elif state[w] == 1:
                reversed_edges.append([v, w])
    rev = set(map(tuple, reversed_edges))
    dag = {n: [] for n in nodes}
    for a in nodes:
        for b in adj[a]:
            x, y = (b, a) if (a, b) in rev else (a, b)
            if y not in dag[x]:
                dag[x].append(y)
    preds = {n: [] for n in nodes}
    for a in nodes:
        for b in dag[a]:
            preds[b].append(a)
    # longest path layering via Kahn order
    indeg = {n: len(preds[n]) for n in nodes}
    queue = [n for n in nodes if indeg[n] == 0]
    layer, order = {n: 0 for n in nodes}, []
    while queue:
        queue.sort(key=pos.get)
        v = queue.pop(0)
        order.append(v)
        for w in dag[v]:
            layer[w] = max(layer[w], layer[v] + 1)
            indeg[w] -= 1
            if indeg[w] == 0:
                queue.append(w)
    nl = max(layer.values()) + 1 if nodes else 0
    layers = [[n for n in nodes if layer[n] == L] for L in range(nl)]
    slot = {}
    for L, members in enumerate(layers):
        if L > 0:
            def key(n):
                ps = [slot[p] for p in preds[n] if p in slot]
                return (sum(ps) / len(ps) if ps else float("inf"), pos[n])
            members.sort(key=key)
        for k, n in enumerate(members):
            slot[n] = k
    widest = max((len(m) for m in layers), default=0)
    if direction == "lr":
        W = 2 * MARGIN + nl * NODE_W + max(nl - 1, 0) * GAP_MAIN
        H = 2 * MARGIN + widest * NODE_H + max(widest - 1, 0) * GAP_CROSS
    else:
        W = 2 * MARGIN + widest * NODE_W + max(widest - 1, 0) * GAP_CROSS
        H = 2 * MARGIN + nl * NODE_H + max(nl - 1, 0) * GAP_MAIN
    boxes = {}
    for L, members in enumerate(layers):
        if direction == "lr":
            span = len(members) * NODE_H + (len(members) - 1) * GAP_CROSS
            off = (H - 2 * MARGIN - span) / 2
            for k, n in enumerate(members):
                x = MARGIN + L * (NODE_W + GAP_MAIN)
                y = MARGIN + off + k * (NODE_H + GAP_CROSS)
                boxes[n] = [x, y]
        else:
            span = len(members) * NODE_W + (len(members) - 1) * GAP_CROSS
            off = (W - 2 * MARGIN - span) / 2
            for k, n in enumerate(members):
                boxes[n] = [MARGIN + off + k * (NODE_W + GAP_CROSS), MARGIN + L * (NODE_H + GAP_MAIN)]
    if rtl:
        for n in boxes:
            boxes[n][0] = W - boxes[n][0] - NODE_W
    meta = {str(n["id"]): n for n in g["nodes"]}
    out_nodes = []
    for n in nodes:
        x, y = boxes[n]
        out_nodes.append({"id": n, "label": str(meta[n].get("label", n)), "role": meta[n].get("role", "default"),
                          "layer": layer[n], "slot": slot[n], "x": _r(x), "y": _r(y), "w": NODE_W, "h": NODE_H})
    out_edges = []
    for k, e in enumerate(g["edges"]):
        a, b = str(e["from"]), str(e["to"])
        if a == b:
            continue
        (ax, ay), (bx, by) = boxes[a], boxes[b]
        if direction == "lr":
            right = bx > ax  # target lies to the right: leave from the right side, enter on the left
            p1 = [ax + NODE_W, ay + NODE_H / 2] if right else [ax, ay + NODE_H / 2]
            p2 = [bx, by + NODE_H / 2] if right else [bx + NODE_W, by + NODE_H / 2]
            if ax == bx:
                p1, p2 = [ax + NODE_W / 2, ay + (NODE_H if by > ay else 0)], [bx + NODE_W / 2, by + (0 if by > ay else NODE_H)]
        else:
            down = by >= ay
            p1 = [ax + NODE_W / 2, ay + (NODE_H if down else 0)]
            p2 = [bx + NODE_W / 2, by + (0 if down else NODE_H)]
        out_edges.append({"edge": k, "from": a, "to": b, "label": str(e.get("label", "")),
                          "reversed_for_layout": (a, b) in rev, "points": [[_r(p1[0]), _r(p1[1])], [_r(p2[0]), _r(p2[1])]]})
    return {"kind": "kosif.diagram_layout.layout.v1", "direction": direction, "rtl": bool(rtl),
            "width": _r(W), "height": _r(H), "layers": nl, "reversed_edges": reversed_edges,
            "nodes": out_nodes, "edges": out_edges}


def _r(v):
    v = round(v, 2)
    return int(v) if v == int(v) else v


def text_el(x, y, s, size, colour, rtl_doc, weight="600"):
    if AR.search(s):
        attrs = 'direction="rtl" unicode-bidi="embed"'
    elif rtl_doc:
        attrs = 'direction="ltr" unicode-bidi="isolate"'
    else:
        attrs = ""
    return ('<text x="%s" y="%s" text-anchor="middle" dominant-baseline="middle" font-size="%d" font-weight="%s" '
            'fill="%s" %s>%s</text>' % (x, y, size, weight, colour, attrs, escape(s))).replace("  ", " ").replace(" >", ">")


def svg(g, rtl=False, direction=None, theme="dark"):
    if theme not in ROLE:
        raise Bad("theme must be dark or light")
    L = layout(g, rtl, direction)
    P = ROLE[theme]
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="%s" height="%s" viewBox="0 0 %s %s" font-family="'
           "'Noto Sans Arabic', 'IBM Plex Sans Arabic', 'Segoe UI', sans-serif\"%s>"
           % (L["width"], L["height"], L["width"], L["height"], ' direction="rtl"' if rtl else ""),
           '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" '
           'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker></defs>' % P["edge"],
           '<g id="background"><rect width="100%%" height="100%%" fill="%s"/></g>' % P["bg"],
           '<g id="connectors" fill="none" stroke="%s" stroke-width="3">' % P["edge"]]
    labels = []
    for e in L["edges"]:
        (x1, y1), (x2, y2) = e["points"]
        if y1 == y2 or x1 == x2:
            d = "M%s,%s L%s,%s" % (x1, y1, x2, y2)
        elif L["direction"] == "lr":
            mx = _r((x1 + x2) / 2)
            d = "M%s,%s L%s,%s L%s,%s L%s,%s" % (x1, y1, mx, y1, mx, y2, x2, y2)
        else:
            my = _r((y1 + y2) / 2)
            d = "M%s,%s L%s,%s L%s,%s L%s,%s" % (x1, y1, x1, my, x2, my, x2, y2)
        out.append('<path id="e%d" d="%s" marker-end="url(#arrow)"/>' % (e["edge"], d))
        if e["label"]:
            labels.append(text_el(_r((x1 + x2) / 2), _r((y1 + y2) / 2 - 14), e["label"], 22, P["edge"], rtl, "400"))
    out.append("</g>")
    out.append('<g id="boxes">')
    for n in L["nodes"]:
        c = P.get(n["role"], P["default"])
        out.append('<rect id="n-%s" x="%s" y="%s" width="%s" height="%s" rx="18" fill="%s" stroke="%s" stroke-width="3"/>'
                   % (escape(n["id"]), n["x"], n["y"], n["w"], n["h"], P["fill"], c))
    out.append("</g>")
    out.append('<g id="labels">')
    for n in L["nodes"]:
        out.append(text_el(_r(n["x"] + n["w"] / 2), _r(n["y"] + n["h"] / 2), n["label"], 26, P["text"], rtl))
    out += labels
    out.append("</g></svg>")
    return "\n".join(out) + "\n"


def self_test():
    g = {"nodes": [{"id": "a", "label": "المستخدم", "role": "user"}, {"id": "b", "label": "API", "role": "backend"},
                   {"id": "c", "label": "DB", "role": "data"}],
         "edges": [{"from": "a", "to": "b", "label": "طلب"}, {"from": "b", "to": "c"}, {"from": "a", "to": "c"}]}
    L = layout(g)
    assert [n["layer"] for n in L["nodes"]] == [0, 1, 2]
    R = layout(g, rtl=True)
    assert R["nodes"][0]["x"] == L["width"] - L["nodes"][0]["x"] - NODE_W
    assert 'direction="rtl"' in svg(g, rtl=True)
    bad = {"nodes": [{"id": "a"}], "edges": [{"from": "a", "to": "z"}]}
    assert lint(bad)["verdict"] == "fail"
    print("self-test: OK")
    return 0


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv[:1] == ["--self-test"]:
        return self_test()
    ap = argparse.ArgumentParser(prog="diagram_layout.py",
                                 description="تخطيط المخططات — KOSIF diagram layout: lint, layered layout, SVG")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("lint")
    a.add_argument("graph")
    a.add_argument("--max-label", type=int, default=24)
    a.add_argument("--max-nodes", type=int, default=9)
    for name in ("layout", "svg"):
        p = sub.add_parser(name)
        p.add_argument("graph")
        p.add_argument("--rtl", action="store_true")
        p.add_argument("--direction", choices=("lr", "tb"))
        if name == "svg":
            p.add_argument("--out")
            p.add_argument("--theme", default="dark", choices=("dark", "light"))
    args = ap.parse_args(argv)
    try:
        g = load(args.graph)
        if args.cmd == "lint":
            print(json.dumps(lint(g, args.max_label, args.max_nodes), ensure_ascii=False, indent=1))
        elif args.cmd == "layout":
            print(json.dumps(layout(g, args.rtl, args.direction), ensure_ascii=False, indent=1))
        else:
            s = svg(g, args.rtl, args.direction, args.theme)
            if args.out:
                try:
                    with open(args.out, "w", encoding="utf-8") as fh:
                        fh.write(s)
                except OSError as e:
                    raise Bad("cannot write %s: %s" % (args.out, e))
                print(json.dumps({"written": args.out, "bytes": len(s.encode("utf-8"))}))
            else:
                sys.stdout.write(s)
    except Bad as e:
        print("diagram_layout: " + str(e), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
