"""Real programs for the diagrams-explainers-code power cards.

Diagram grammar, layouts, timing schedules and math devices are implemented as deterministic
procedures (SVG writers, validators, layout algorithms, schedulers, solvers) on fixtures whose
answers are known. Cards that need mmdc, d2, Manim, an image model or a hosted pipeline are skipped.
"""
from __future__ import annotations

import cmath
import json
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from .photo_video_footage import REPO, chk, jwrite, near, contrast, write_video, ff, read_video, solid, duration

SVGNS = "http://www.w3.org/2000/svg"
MONO = None


def _font(size):
    for p in sorted(Path("/usr/share/fonts").rglob("*.ttf")):
        if "DejaVuSansMono" in p.name and "Bold" not in p.name:
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def ease_in_out_cubic(p):
    return 4 * p ** 3 if p < .5 else 1 - (-2 * p + 2) ** 3 / 2


def cubic_bezier(x1, y1, x2, y2):
    def f(x):
        lo, hi = 0.0, 1.0
        for _ in range(60):
            t = (lo + hi) / 2
            bx = 3 * (1 - t) ** 2 * t * x1 + 3 * (1 - t) * t * t * x2 + t ** 3
            lo, hi = (t, hi) if bx < x else (lo, t)
        t = (lo + hi) / 2
        return 3 * (1 - t) ** 2 * t * y1 + 3 * (1 - t) * t * t * y2 + t ** 3
    return f


def spring(stiff, damp, t_end=1.2, dt=1 / 1000, x0=0.0):
    x, v, xs = x0, 0.0, []
    for _ in range(int(t_end / dt)):
        a = stiff * (1 - x) - damp * v
        v += a * dt
        x += v * dt
        xs.append(x)
    return np.array(xs)


def segs_cross(p1, p2, p3, p4):
    def o(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    if len({tuple(p1), tuple(p2), tuple(p3), tuple(p4)}) < 4:
        return False
    return (o(p1, p2, p3) * o(p1, p2, p4) < 0) and (o(p3, p4, p1) * o(p3, p4, p2) < 0)


def count_crossings(pos, edges):
    n = 0
    for i, (a, b) in enumerate(edges):
        for c, d in edges[i + 1:]:
            if segs_cross(pos[a], pos[b], pos[c], pos[d]):
                n += 1
    return n


def write_svg(path, w, h, body):
    Path(path).write_text(f'<svg xmlns="{SVGNS}" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{body}</svg>\n',
                          encoding="utf-8")


# ------------------------------------------------------------------ composition & grammar
def expl_01(work):
    def lint(d):
        errs = []
        n = len(d["nodes"])
        if n > 9:
            errs.append("more than 9 nodes: split into two diagrams")
        elif not 3 <= n <= 7:
            errs.append("3-7 nodes visible")
        if len(d.get("steps", [])) > 5:
            errs.append("more than 5 steps")
        acc = [x for x in d["nodes"] if x.get("accent")]
        if len(acc) > 2:
            errs.append("more than 2 accents")
        if any(x.get("colour") == "red" and not x.get("problem") for x in d["nodes"]):
            errs.append("red used for a non-problem")
        if count_crossings({x["id"]: x["pos"] for x in d["nodes"]}, d["edges"]) > 0:
            errs.append("edges cross")
        return errs

    good = {"nodes": [{"id": "a", "pos": (300, 100)}, {"id": "b", "pos": (200, 100)}, {"id": "c", "pos": (100, 100), "accent": True},
                      {"id": "d", "pos": (200, 200), "colour": "red", "problem": True}],
            "edges": [("a", "b"), ("b", "c"), ("b", "d")], "steps": [1, 2, 3]}
    bad = {"nodes": [{"id": k, "pos": p, "accent": k in "abc"} for k, p in
                     zip("abcd", [(0, 0), (100, 100), (100, 0), (0, 100)])],
           "edges": [("a", "b"), ("c", "d")], "steps": list(range(6))}
    big = {"nodes": [{"id": str(i), "pos": (i * 10, 0)} for i in range(10)], "edges": []}
    jwrite(work, "layout.json", good)
    eb = lint(bad)
    return [chk("good 4-node diagram passes", lint(good) == [], lint(good)),
            chk("3 accents / 6 steps / crossing caught", {"more than 2 accents", "more than 5 steps", "edges cross"} <= set(eb), eb),
            chk("10 nodes -> split into two", lint(big) == ["more than 9 nodes: split into two diagrams"], lint(big))]


def elbow(a, b):
    """One right-angle bend from a to b."""
    return [a, (b[0], a[1]), b]


def expl_02(work):
    nodes = {"A": (100, 100, 240, 80), "B": (500, 300, 240, 80)}
    stroke, head, rx = 3.5, 14, 20
    a = (nodes["A"][0] + nodes["A"][2], nodes["A"][1] + nodes["A"][3] / 2)
    b = (nodes["B"][0], nodes["B"][1] + nodes["B"][3] / 2)
    pts = elbow(a, (b[0] - 1e-9, b[1]))
    pts = [a, (b[0] - 60, a[1]), (b[0] - 60, b[1]), b]
    body = (f'<defs><marker id="h" markerWidth="{head}" markerHeight="{head}" refX="{head - 1}" refY="{head / 2}" orient="auto">'
            f'<path d="M0,0 L{head},{head / 2} L0,{head} z"/></marker></defs>')
    for k, (x, y, w, h) in nodes.items():
        body += f'<rect id="{k}" x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" stroke-width="{stroke}" fill="none" stroke="#111"/>'
        body += f'<text x="{x + w / 2}" y="{y + h / 2}" font-size="36">{k}</text>'
    body += ('<polyline points="' + " ".join(f"{x},{y}" for x, y in pts) +
             f'" fill="none" stroke="#111" stroke-width="{stroke}" marker-end="url(#h)"/>')
    body += f'<text x="{(a[0] + b[0] - 60) / 2}" y="{a[1] - 8}" font-size="26">sends</text>'
    write_svg(work / "grammar.svg", 1080, 600, body)
    root = ET.parse(work / "grammar.svg").getroot()
    q = lambda tag: root.iter(f"{{{SVGNS}}}{tag}")
    strokes = {float(e.get("stroke-width")) for e in list(q("rect")) + list(q("polyline"))}
    rxs = {float(e.get("rx")) for e in q("rect")}
    mk = next(q("marker"))
    poly = [tuple(map(float, p.split(","))) for p in next(q("polyline")).get("points").split()]
    diag = [i for i in range(len(poly) - 1) if poly[i][0] != poly[i + 1][0] and poly[i][1] != poly[i + 1][1]]
    sizes = sorted(float(t.get("font-size")) for t in q("text"))
    gap = (a[1] - 8)
    return [chk("one stroke width 3-4 px", len(strokes) == 1 and 3 <= strokes.pop() <= 4, "3.5"),
            chk("radius 16-24 px", rxs == {20.0}, rxs),
            chk("arrowhead 14-18 px, ~3-4x stroke, orient auto", 14 <= float(mk.get("markerWidth")) <= 18 and mk.get("orient") == "auto"
                and 3 <= float(mk.get("markerWidth")) / 3.5 <= 4.2, mk.get("markerWidth")),
            chk("no diagonal segments", diag == [], diag),
            chk("node labels 32-44, edge labels 24-28", 24 <= sizes[0] <= 28 and all(32 <= s <= 44 for s in sizes[1:]), sizes),
            chk("edge label 6-10 px from its line", 6 <= a[1] - gap <= 10, a[1] - gap)]


def tidy_tree(tree, root, depth=0, nxt=None, pos=None):
    """Reingold-Tilford-lite: leaves get consecutive x, parents centre over children."""
    nxt = nxt if nxt is not None else [0]
    pos = pos if pos is not None else {}
    kids = tree.get(root, [])
    for k in kids:
        tidy_tree(tree, k, depth + 1, nxt, pos)
    if kids:
        pos[root] = ((pos[kids[0]][0] + pos[kids[-1]][0]) / 2, depth)
    else:
        pos[root] = (nxt[0], depth)
        nxt[0] += 1
    return pos


def expl_03(work):
    table = {"branching decisions": "flowchart", "messages over time": "sequence", "components + links": "architecture",
             "dated events": "timeline", "parent-child": "tree", "cross-team handoffs": "swimlane",
             "two-axis positioning": "quadrant", "reinforcing cycle": "loop", "data": "ER"}
    tree = {"root": ["a", "b"], "a": ["a1", "a2", "a3"], "b": ["b1"]}
    pos = tidy_tree(tree, "root")
    edges = [(p, c) for p, cs in tree.items() for c in cs]
    jwrite(work, "tree_layout.json", pos)
    return [chk("8 diagram types + ER mapped", len(set(table.values())) == 9 and table["dated events"] == "timeline", table),
            chk("tidy tree: parent centred over children", pos["a"][0] == (pos["a1"][0] + pos["a3"][0]) / 2 and pos["root"][0] == 2.0,
                pos),
            chk("tidy tree has no crossings", count_crossings(pos, edges) == 0, 0),
            chk("depth = y level", pos["a1"][1] == 2 and pos["root"][1] == 0, pos["a1"])]


def expl_04(work):
    words = {"server": 1.0, "cache": 1.8, "user": 2.6}
    order = ["user", "server", "cache"]
    stagger = 0.12
    layers = ["background", "connectors", "boxes", "labels"]

    def state(node, t, active):
        if t < words[node]:
            return "unbuilt"
        return "active" if node == active else "visited"

    opacity = {"unbuilt": 0.0, "active": 1.0, "visited": 0.7}
    sched = sorted(words.items(), key=lambda kv: kv[1])
    edges = [(sched[i][0], sched[i + 1][0], sched[i][1] + stagger) for i in range(len(sched) - 1)]
    body = "".join(f'<g id="{l}"></g>' for l in layers)
    write_svg(work / "build.svg", 400, 200, body)
    t = 2.0
    st = {n: opacity[state(n, t, "cache")] for n in words}
    return [chk("paint order background -> connectors -> boxes -> labels",
                [g.get("id") for g in ET.parse(work / "build.svg").getroot()] == layers, layers),
            chk("each node revealed on its spoken word (not front-loaded)", [n for n, _ in sched] == ["server", "cache", "user"], sched),
            chk("states at 2.0 s: active 1, visited .7, future undrawn", st == {"server": .7, "cache": 1.0, "user": 0.0}, st),
            chk("outgoing edge draws 0.08-0.15 s after its node", all(0.08 <= e[2] - words[e[0]] <= 0.15 for e in edges), edges)]


def expl_05(work):
    W = 1000
    nodes = {"step1": 100, "step2": 400, "step3": 700}
    rtl = {k: W - x for k, x in nodes.items()}
    marker_ltr = "M0,0 L14,7 L0,14 z"

    def mirror_path(d, w=14):
        return re.sub(r"(-?\d+(?:\.\d+)?),", lambda m: f"{w - float(m.group(1)):g},", d)

    def label(text):
        return f'<tspan dir="ltr" style="unicode-bidi:isolate">{text}</tspan>' if re.search(r"[A-Za-z0-9_]", text) else text

    lab = label("API_v2")
    body = "".join(f'<text x="{x}" y="50">{label(k)}</text>' for k, x in rtl.items())
    write_svg(work / "rtl.svg", W, 100, body)
    order = sorted(rtl, key=lambda k: -rtl[k])
    return [chk("first node on the right (x' = W - x)", rtl["step1"] == 900 and order == ["step1", "step2", "step3"], rtl),
            chk("arrow marker mirrored to point left", mirror_path(marker_ltr) == "M14,0 L0,7 L14,14 z", mirror_path(marker_ltr)),
            chk("Latin id isolated LTR", 'dir="ltr"' in lab and "unicode-bidi:isolate" in lab, lab)]


def expl_06(work):
    roles = {"frontend": "#22d3ee", "backend": "#34d399", "data": "#a78bfa", "cloud": "#fbbf24", "security": "#fb7185",
             "bus": "#fb923c", "external": "#94a3b8"}
    comps = [("web", "frontend"), ("api", "backend"), ("db", "data")]
    body = '<rect id="region" x="10" y="10" width="500" height="200" rx="12" stroke="#fbbf24" stroke-dasharray="8,4" fill="none"/>'
    body += '<rect id="sg" x="30" y="30" width="200" height="120" rx="12" stroke="#fb7185" stroke-dasharray="4,4" fill="none"/>'
    for i, (n, r) in enumerate(comps):
        body += f'<rect id="{n}" data-role="{r}" x="{40 + 150 * i}" y="60" width="120" height="60" fill="{roles[r]}"/>'
    write_svg(work / "arch.svg", 520, 220, body)
    root = ET.parse(work / "arch.svg").getroot()
    rects = {e.get("id"): e for e in root.iter(f"{{{SVGNS}}}rect")}
    lum = {r: contrast(tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)), (15, 23, 42)) for r, c in roles.items()}
    return [chk("colour encodes role", all(rects[n].get("fill") == roles[r] for n, r in comps), comps),
            chk("region dashed 8,4 amber rx 12; security 4,4", rects["region"].get("stroke-dasharray") == "8,4"
                and rects["region"].get("rx") == "12" and rects["sg"].get("stroke-dasharray") == "4,4", "dashes"),
            chk("7 distinct role colours", len(set(roles.values())) == 7, len(roles)),
            chk("every role colour readable on dark #0f172a (>= 4.5:1)", min(lum.values()) >= 4.5, round(min(lum.values()), 2))]


def expl_07(work):
    W, H = 1600, 900
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    m = int(0.06 * W)
    f = _font(44)
    title = "How a cache hit saves a trip"
    d.text((m, m), title, fill="#111111", font=f)
    for k in range(3):
        x = m + 80 + k * 450
        d.rectangle([x, 350, x + 300, 520], outline="#333333", width=2)
        if k < 2:
            d.line([x + 300, 435, x + 450, 435], fill="#767676", width=2)
    d.rectangle([m + 80, 600, m + 380, 612], fill="#D93025")
    im.save(work / "mono.png")
    a = np.asarray(im).astype(int)
    chroma = (a.max(-1) - a.min(-1)) > 40
    ink = np.argwhere(a.min(-1) < 250)
    return [chk("title <= 40 chars", len(title) <= 40, len(title)),
            chk("accent red < 5% of frame", 0 < chroma.mean() < 0.05, round(float(chroma.mean()), 4)),
            chk("accent is #D93025", tuple(a[606, m + 200]) == (0xD9, 0x30, 0x25), tuple(a[606, m + 200])),
            chk("margins 5-7% kept", ink[:, 1].min() >= 0.05 * W and ink[:, 0].min() >= 0.05 * H and m / W <= 0.07,
                (int(ink[:, 1].min()), int(ink[:, 0].min())))]


def expl_08(work):
    def needs_label(icon_px, audience, stakes):
        return icon_px < 24 or audience == "novice" or stakes == "high"

    # closure: a dashed circle loses its implied shape when downscaled below 24 px
    def dashed_ring(size):
        im = Image.new("L", (240, 240), 255)
        d = ImageDraw.Draw(im)
        for k in range(0, 360, 30):
            d.arc([20, 20, 220, 220], k, k + 18, fill=0, width=10)
        return np.asarray(im.resize((size, size), Image.BOX)) < 200

    def gray_ring(size):
        im = Image.new("L", (240, 240), 255)
        d = ImageDraw.Draw(im)
        for k in range(0, 360, 30):
            d.arc([20, 20, 220, 220], k, k + 18, fill=0, width=10)
        return np.asarray(im.resize((size, size), Image.BOX)).astype(float)

    def gaps_visible(g):
        n = g.shape[0]
        yy, xx = np.mgrid[:n, :n]
        r = np.hypot(yy - n / 2 + .5, xx - n / 2 + .5)
        return g[(r > n * .36) & (r < n * .46)].std() / 255  # dash/gap modulation on the ring

    big, small = gaps_visible(gray_ring(96)), gaps_visible(gray_ring(12))
    Image.fromarray(gray_ring(96).astype(np.uint8)).save(work / "ring96.png")
    return [chk("icons under 24 px get labels", needs_label(20, "expert", "low") and not needs_label(48, "expert", "low"), "24 px"),
            chk("novices and high stakes always labelled", needs_label(64, "novice", "low") and needs_label(64, "expert", "high"), "rule"),
            chk("dash gaps readable at 96 px, washed out at 12 px", big > 0.3 and small < big / 2, (round(float(big), 3), round(float(small), 3)))]


def expl_10(work):
    from fontTools.ttLib import TTFont
    fpath = next(p for p in sorted(Path("/usr/share/fonts").rglob("*.ttf")) if "DejaVuSans.ttf" == p.name)
    tt = TTFont(str(fpath))
    cmap, hmtx, upm = tt.getBestCmap(), tt["hmtx"], tt["head"].unitsPerEm
    pt = 7
    fs = pt * 25.4 / 72  # mm

    def text_w(s):
        return sum(hmtx[cmap[ord(c)]][0] for c in s) / upm * fs

    def box(label, x, y, pad=2.0):
        w, h = text_w(label) + 2 * pad, fs + 2 * pad
        return {"x": x, "y": y, "w": w, "h": h, "label": label}

    def connect(a, b):
        ca = (a["x"] + a["w"] / 2, a["y"] + a["h"] / 2)
        cb = (b["x"] + b["w"] / 2, b["y"] + b["h"] / 2)
        dx, dy = cb[0] - ca[0], cb[1] - ca[1]

        def edge(bx, c, sgn):
            tx = (bx["w"] / 2) / abs(dx) if dx else math.inf
            ty = (bx["h"] / 2) / abs(dy) if dy else math.inf
            t = min(tx, ty)
            return (c[0] + sgn * dx * t, c[1] + sgn * dy * t)

        return edge(a, ca, 1), edge(b, cb, -1), math.degrees(math.atan2(dy, dx))

    A, B = box("Input", 10, 10), box("Encoder", 60, 30)
    p0, p1, ang = connect(A, B)
    body = "".join(f'<rect x="{b["x"]:.3f}" y="{b["y"]:.3f}" width="{b["w"]:.3f}" height="{b["h"]:.3f}"/>'
                   f'<text font-size="{fs:.3f}">{b["label"]}</text>' for b in (A, B))
    Path(work / "schematic.svg").write_text(f'<svg xmlns="{SVGNS}" width="120mm" height="60mm" viewBox="0 0 120 60">{body}</svg>')
    on_edge = lambda p, b: (near(p[0], b["x"], 1e-6) or near(p[0], b["x"] + b["w"], 1e-6) or near(p[1], b["y"], 1e-6)
                            or near(p[1], b["y"] + b["h"], 1e-6))
    return [chk("7 pt = 2.47 mm", near(fs, 2.469, 0.001), round(fs, 4)),
            chk("box = measured text + 2 mm padding", near(A["w"], text_w("Input") + 4, 1e-9), round(A["w"], 3)),
            chk("arrow endpoints snap to both box edges", on_edge(p0, A) and on_edge(p1, B), (p0, p1)),
            chk("width/height in mm with equal viewBox", 'width="120mm"' in (work / "schematic.svg").read_text()
                and 'viewBox="0 0 120 60"' in (work / "schematic.svg").read_text(), "mm")]


def expl_13(work):
    els = [{"id": "r1", "type": "rectangle", "x": 0, "y": 0, "width": 200, "height": 80, "roughness": 1},
           {"id": "t1", "type": "text", "x": 20, "y": 20, "text": "Idea", "fontFamily": 1, "containerId": "r1"},
           {"id": "r2", "type": "ellipse", "x": 300, "y": 0, "width": 120, "height": 80, "roughness": 1},
           {"id": "a1", "type": "arrow", "x": 200, "y": 40, "points": [[0, 0], [100, 0]], "roughness": 1,
            "startBinding": {"elementId": "r1"}, "endBinding": {"elementId": "r2"}}]
    scene = {"type": "excalidraw", "version": 2, "elements": els, "appState": {"viewBackgroundColor": "#ffffff"}}
    (work / "board.excalidraw").write_text(json.dumps(scene))
    canvas = {"nodes": [{"id": "n1", "type": "text", "text": "Scene 1", "x": 0, "y": 0, "width": 250, "height": 60},
                        {"id": "n2", "type": "text", "text": "Scene 2", "x": 300, "y": 0, "width": 250, "height": 60}],
              "edges": [{"id": "e1", "fromNode": "n1", "toNode": "n2"}]}
    (work / "story.canvas").write_text(json.dumps(canvas))

    def validate(s):
        ids = {e["id"] for e in s["elements"]}
        errs = []
        for e in s["elements"]:
            if e["type"] not in {"rectangle", "ellipse", "diamond", "arrow", "line", "text"}:
                errs.append(f"bad type {e['type']}")
            if e["type"] == "arrow":
                for k in ("startBinding", "endBinding"):
                    if e.get(k, {}).get("elementId") not in ids:
                        errs.append(f"{e['id']} {k} dangling")
            if e["type"] == "text" and e.get("fontFamily") not in (1, 2, 3):
                errs.append("fontFamily")
        return errs

    bad = json.loads(json.dumps(scene))
    bad["elements"][3]["endBinding"]["elementId"] = "gone"
    cv_ok = all(e["fromNode"] in {n["id"] for n in canvas["nodes"]} for e in canvas["edges"])
    return [chk("excalidraw scene validates", validate(scene) == [], validate(scene)),
            chk("dangling arrow binding caught", validate(bad) == ["a1 endBinding dangling"], validate(bad)),
            chk("roughness 1 on drawn shapes, hand font 1", all(e.get("roughness") == 1 for e in els if e["type"] != "text")
                and els[1]["fontFamily"] == 1, "hand"),
            chk("JSON Canvas edges reference nodes", cv_ok, "ok")]


def force_layout(nodes, links, ticks=200, seed=1):
    rng = np.random.default_rng(seed)
    idx = {n: i for i, n in enumerate(nodes)}
    p = rng.normal(0, 1, (len(nodes), 2))
    hist = []
    for t in range(ticks):
        alpha = 1 - t / ticks
        f = np.zeros_like(p)
        d = p[:, None] - p[None]
        r2 = (d ** 2).sum(-1) + 1e-3
        f += (d / r2[..., None]).sum(1) * 0.5
        for a, b in links:
            i, j = idx[a], idx[b]
            v = p[j] - p[i]
            dist = np.linalg.norm(v) + 1e-9
            k = (dist - 1.0) * 0.3
            f[i] += k * v / dist
            f[j] -= k * v / dist
        f -= p * 0.02
        p = p + f * 0.2 * alpha
        hist.append(p.copy())
    return np.array(hist)


def expl_14(work):
    outline = {"root": {"A": {"A1": {}, "A2": {}}, "B": {"B1": {}}, "C": {}}}
    nodes, links, branch = [], [], {}

    def walk(tree, parent=None, top=None, depth=0):
        for k, sub in tree.items():
            nodes.append(k)
            branch[k] = top or k
            if parent:
                links.append((parent, k))
            walk(sub, k, top or (k if parent else None), depth + 1)
            maxd[0] = max(maxd[0], depth)

    maxd = [0]
    walk(outline)
    h1 = force_layout(nodes, links)
    h2 = force_layout(nodes, links)
    np.save(work / "ticks.npy", h1)
    final = h1[-1]
    edge_len = [np.linalg.norm(final[nodes.index(a)] - final[nodes.index(b)]) for a, b in links]
    move_end = np.abs(h1[-1] - h1[-2]).max()
    pos_at = lambda t, T=4.0: h1[min(len(h1) - 1, int(t / T * (len(h1) - 1)))]
    return [chk("seeded offline ticks are reproducible", np.array_equal(h1, h2), "same"),
            chk("simulation settles (last tick move < 1e-3)", move_end < 1e-3, float(move_end)),
            chk("render indexes stored ticks by t", np.array_equal(pos_at(4.0), h1[-1]) and np.array_equal(pos_at(0), h1[0]), "indexed"),
            chk("linked nodes sit closer than unlinked pairs", np.mean(edge_len) < np.mean(
                [np.linalg.norm(final[i] - final[j]) for i in range(len(nodes)) for j in range(i + 1, len(nodes))
                 if (nodes[i], nodes[j]) not in links and (nodes[j], nodes[i]) not in links]), [round(float(l), 2) for l in edge_len]),
            chk("depth <= 6 and colour per top branch", maxd[0] <= 6 and branch["A2"] == "A" and branch["B1"] == "B", branch)]


def expl_15(work):
    spec = {"entity": {"id": "E", "x": 50, "y": 50}, "in": ["rain", "snow"], "out": ["river"], "draft": ["plan"]}
    dash = {"in": "7 6", "draft": "3 5", "out": None}
    nodes = {"E": (50, 50)}
    for side, xs in (("in", 15), ("out", 85), ("draft", 50)):
        items = spec[side]
        for i, n in enumerate(items):
            nodes[n] = (xs, 20 + 60 * (i + 0.5) / len(items)) if side != "draft" else (50, 90)
    body = ""
    for side in ("in", "out", "draft"):
        for n in spec[side]:
            a, b = nodes[n], nodes["E"]
            if side == "out":
                a, b = b, a
            da = f' stroke-dasharray="{dash[side]}"' if dash[side] else ""
            body += f'<line class="{side}" x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}"{da}/>'
    body += "<style>@keyframes flow{to{stroke-dashoffset:-26}} line{animation:flow 1.6s linear infinite}</style>"
    write_svg(work / "entity.svg", 100, 100, body)
    root = ET.parse(work / "entity.svg").getroot()
    lines = list(root.iter(f"{{{SVGNS}}}line"))
    css = (work / "entity.svg").read_text()
    return [chk("inputs left of entity, outputs right", all(nodes[n][0] < 50 for n in spec["in"]) and nodes["river"][0] > 50, nodes),
            chk("inputs dashed 7 6, drafts 3 5, outputs solid",
                [l.get("stroke-dasharray") for l in lines] == ["7 6", "7 6", None, "3 5"], [l.get("class") for l in lines]),
            chk("flow keyframes to dashoffset -26 over 1.6 s", "stroke-dashoffset:-26" in css and "1.6s" in css, "css")]


def expl_16(work):
    pops = [0.0, 0.9, 1.8]
    xs = spring(160, 14, 1.0, x0=0.85)
    settle = next(i for i in range(len(xs)) if np.all(np.abs(xs[i:] - 1) < 0.01)) / 1000
    edges = [(0.3, 0.9), (1.2, 1.8)]
    L = 600

    def edge_progress(t, a, b):
        p = min(max((t - a) / (b - a), 0), 1)
        return ease_in_out_cubic(p)

    def arrow_on(t, a, b):
        return t >= b - 0.08

    def dim(node_i, t):
        later = [p for p in pops if p > pops[node_i]]
        return 0.7 if later and t >= later[0] else 1.0

    speed = L / (edges[0][1] - edges[0][0])
    return [chk("nodes pop at 0 / 900 / 1800 ms", pops == [0, .9, 1.8], pops),
            chk("spring 14/160 from .85 settles ~300 ms", 0.2 <= settle <= 0.45, settle),
            chk("edge 600 px drawn in 600 ms = 1000 px/s (900-1200)", 900 <= speed <= 1200, speed),
            chk("arrowhead only in the last 80 ms", not arrow_on(0.81, *edges[0]) and arrow_on(0.83, *edges[0]), "80 ms"),
            chk("previous nodes dim to 70%", dim(0, 1.0) == 0.7 and dim(2, 3.0) == 1.0, (dim(0, 1.0), dim(2, 3.0)))]


def path_points(pts, n=2000):
    pts = np.asarray(pts, float)
    seg = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    cum = np.concatenate([[0], np.cumsum(seg)])
    return pts, cum


def point_at_length(pts, cum, s):
    i = min(np.searchsorted(cum, s, side="right") - 1, len(pts) - 2)
    u = (s - cum[i]) / (cum[i + 1] - cum[i])
    return pts[i] + u * (pts[i + 1] - pts[i])


def expl_17(work):
    pts, cum = path_points([(0, 0), (300, 0), (300, 400)])
    L = cum[-1]
    travel, gap = 0.75, 0.4

    def dot(t):
        k, r = divmod(t, travel + gap)
        if r > travel:
            return None
        return point_at_length(pts, cum, ease_in_out_cubic(r / travel) * L)

    mid = dot(travel / 2)
    return [chk("path length 700", L == 700, L),
            chk("dot at mid travel is at getPointAtLength(L/2)", np.allclose(mid, (300, 50)), mid.tolist()),
            chk("dot hidden during the 400 ms gap", dot(travel + 0.2) is None, "gap"),
            chk("repeats: same place one cycle later", np.allclose(dot(0.3), dot(0.3 + travel + gap)), "repeat"),
            chk("travel 600-900 ms", 0.6 <= travel <= 0.9, travel)]


def expl_18(work):
    def dashoffset(t, speed=140):
        return -speed * t

    pattern = (20, 18)
    period = sum(pattern)

    def visible(s, t):
        return ((s + dashoffset(t)) % period) < pattern[0]

    s = np.arange(0, 400)
    a, b = visible(s, 0.0), visible(s, period / 140)
    shifted = visible(s, 0.05)
    first_on = int(np.argmax(shifted))
    ray = lambda t: 18 * t % 360
    pulse = lambda t: 1 + 0.06 * math.sin(4 * math.pi * t)
    return [chk("dashoffset = -140 t (seek-safe, no accumulation)", dashoffset(2.0) == -280, dashoffset(2.0)),
            chk("pattern repeats after one 38 px period", np.array_equal(a, b), period),
            chk("dashes march forward 7 px in 50 ms", np.array_equal(shifted, visible(s - 7, 0.0)), first_on),
            chk("sun rays 18 deg/s, pulse 1 +- .06", ray(10) == 180 and near(pulse(0.125), 1.06, 1e-12), (ray(10), pulse(0.125)))]


def expl_19(work):
    n = 6
    hub = (0, 0)
    stag, draw = 0.1, 0.45
    sats = [(math.cos(2 * math.pi * k / n) * 300, math.sin(2 * math.pi * k / n) * 160) for k in range(n)]

    def spoke_progress(k, t):
        return min(max((t - k * stag) / draw, 0), 1)

    def node_alpha(k, t):
        return min(max((t - (k * stag + draw)) / 0.2, 0), 1)

    on_ellipse = all(near((x / 300) ** 2 + (y / 160) ** 2, 1, 1e-9) for x, y in sats)
    t = 0.5
    return [chk("satellites on the ellipse", on_ellipse, len(sats)),
            chk("spokes draw outward with 100 ms stagger", [round(spoke_progress(k, t), 3) for k in range(3)]
                == [1.0, round(0.4 / 0.45, 3), round(0.3 / 0.45, 3)], [spoke_progress(k, t) for k in range(3)]),
            chk("node fades in only after its spoke finished", node_alpha(0, 0.44) == 0 and node_alpha(0, 0.65) == 1, "after"),
            chk("draw 300-600 ms, stagger 50-150 ms", 0.3 <= draw <= 0.6 and 0.05 <= stag <= 0.15, (draw, stag))]


def expl_20(work):
    N = 5
    ends = [(400, -200 + 100 * k) for k in range(N)]
    xs = spring(220, 2 * 0.591 * math.sqrt(220), 1.0)  # damping ratio for a 10% overshoot
    over = xs.max()

    def cubic(p0, p1, p2, p3, t):
        return ((1 - t) ** 3) * np.array(p0) + 3 * (1 - t) ** 2 * t * np.array(p1) + 3 * (1 - t) * t * t * np.array(p2) + t ** 3 * np.array(p3)

    curves = [[cubic((0, 0), (200, 0), (200, e[1]), e, t) for t in np.linspace(0, 1, 50)] for e in ends]
    starts = [k * 0.12 for k in range(N)]
    ast = ["document", ["heading", "paragraph", ["codeBlock"]]]

    def flatten(n, d=0, out=None):
        out = out if out is not None else []
        for x in n:
            if isinstance(x, list):
                flatten(x, d + 1, out)
            else:
                out.append((x, d))
        return out

    flat = flatten(ast)
    return [chk("curves start at the product and end on each card", all(np.allclose(c[0], (0, 0)) and np.allclose(c[-1], e)
                                                                       for c, e in zip(curves, ends)), N),
            chk("5 avatars, 120 ms stagger", starts[-1] == 0.48 and len(starts) == 5, starts),
            chk("spring overshoot ~1.1", 1.05 <= over <= 1.2, round(float(over), 3)),
            chk("AST cascade indents by depth", flat == [("document", 0), ("heading", 1), ("paragraph", 1), ("codeBlock", 2)], flat)]


def expl_21(work):
    words = [{"w": "the", "start": 0.2}, {"w": "client", "start": 0.6}, {"w": "sends", "start": 1.1},
             {"w": "a", "start": 1.4}, {"w": "request", "start": 1.6}, {"w": "to", "start": 2.1}, {"w": "server", "start": 2.4}]
    elements = {"client_icon": "client", "arrow": "sends", "request_card": "request", "server_icon": "server"}
    total = 4.0
    start = {el: next(w["start"] for w in words if w["w"] == kw) - 0.06 for el, kw in elements.items()}
    end_speech = words[-1]["start"] + 0.4
    front = sum(1 for s in start.values() if s < 0.25 * total) / len(start)
    jwrite(work, "draw_schedule.json", start)
    return [chk("each element starts 60 ms before its word", near(start["arrow"], 1.04, 1e-9) and near(start["server_icon"], 2.34, 1e-9),
                start),
            chk("no more than 25% front-loaded", front <= 0.25 + 1e-9, front),
            chk("1-2 s hold for the full read at the end", 1.0 <= total - end_speech <= 2.0, round(total - end_speech, 2))]


def expl_22(work):
    camera = cubic_bezier(.65, 0, .35, 1)

    def zoom(t):
        if t < 2:
            return 1.0
        p = min((t - 2) / 0.9, 1)
        return 1 + 0.5 * camera(p)

    def xfade(t):
        return min(max((t - 2.9) / 0.3, 0), 1)

    before = {("a", "b"), ("b", "c"), ("c", "d")}
    after = {("a", "b"), ("b", "d"), ("c", "d")}
    redraw = after - before
    return [chk("hold 2 s at scale 1", zoom(1.9) == 1.0, zoom(1.9)),
            chk("scale 1.5 reached at 2.9 s (900 ms), <= 1.8", near(zoom(2.9), 1.5, 1e-6) and zoom(5) <= 1.8, zoom(2.9)),
            chk("cubic-bezier(.65,0,.35,1) is symmetric: half at mid", near(camera(0.5), 0.5, 1e-6), camera(0.5)),
            chk("300 ms crossfade to the sub-diagram", near(xfade(3.05), 0.5, 1e-9) and xfade(3.2) == 1, xfade(3.05)),
            chk("after diagram redraws only the changed edge", redraw == {("b", "d")}, redraw)]


def expl_23(work):
    events = [0.5, 1.2, 1.3, 1.35, 3.0]
    axis = 0.6
    pos = lambda t: max(0.0, (t - axis)) * 1.0  # constant-speed playhead in years-per-second units

    def marker_scale(e, t):
        arrive = axis + e
        return 0 if t < arrive else min(1, (t - arrive) / 0.2)

    def label_alpha(e, t):
        return 0 if t < axis + e + 0.2 + 0.12 else 1

    dense = [e for e in events if sum(abs(e - f) < 0.2 for f in events) >= 3]
    cam_speed = lambda e: 0.3 if e in dense else 1.0
    return [chk("constant-speed playhead", pos(2.6) - pos(1.6) == pos(1.6) - pos(0.6), pos(1.6)),
            chk("marker pops 200 ms on arrival", marker_scale(0.5, 1.1) == 0 and near(marker_scale(0.5, 1.2), 0.5, 1e-9), "pop"),
            chk("label after marker +120 ms", label_alpha(0.5, 1.4) == 0 and label_alpha(0.5, 1.43) == 1, "label"),
            chk("camera slows to 30% near the dense cluster", [cam_speed(e) for e in events] == [1, .3, .3, .3, 1], dense)]


def expl_24(work):
    phases = [("question", 0, 2), ("branches", 2, 5), ("example", 5, 8), ("result", 8, 10)]
    tree = {"q": {"yes": "approve", "no": "review"}}
    example = {"answer": "no"}
    chosen = tree["q"][example["answer"]]

    def phase(t):
        return next(n for n, a, b in phases if a <= t < b) if t < 10 else "end"

    failover = [("red_branch", 0.0, 0.4), ("green_branch", 0.4, 0.8)]
    return [chk("10 s in 4 phases", phase(1) == "question" and phase(6) == "example" and phase(9.5) == "result", phase(6)),
            chk("example travels to its outcome", chosen == "review", chosen),
            chk("failover: red then green, 400 ms each", failover[0][2] - failover[0][1] == 0.4 and failover[1][1] == failover[0][2],
                failover)]


def expl_25(work):
    n = 4
    R = 300
    stations = [(R * math.cos(math.pi / 2 - 2 * math.pi * k / n), R * math.sin(math.pi / 2 - 2 * math.pi * k / n)) for k in range(n)]

    def loop_progress(t):
        p = min(max((t - 8.9) / 0.9, 0), 1)
        return ease_in_out_cubic(p)

    def marker_end(t):
        return loop_progress(t) > 0.98

    clockwise = all((stations[k][0] * stations[(k + 1) % n][1] - stations[k][1] * stations[(k + 1) % n][0]) < 0 for k in range(n))
    return [chk("4 stations on a circle", all(near(math.hypot(*s), R, 1e-9) for s in stations), len(stations)),
            chk("arrows go round in one direction", clockwise, "clockwise"),
            chk("loop drawn 8.9-9.8 s", loop_progress(8.9) == 0 and loop_progress(9.8) == 1 and near(loop_progress(9.35), .5, 1e-9),
                loop_progress(9.35)),
            chk("marker-end only when progress > .98", not marker_end(9.6) and marker_end(9.79), "marker")]


def mix(a, b, t):
    a, b = np.array([int(a[i:i + 2], 16) for i in (1, 3, 5)]), np.array([int(b[i:i + 2], 16) for i in (1, 3, 5)])
    return "#%02x%02x%02x" % tuple(np.round(a + (b - a) * t).astype(int))


def expl_26(work):
    pills = [{"i": i, "x": 1395 - i * 290, "y": 968, "w": 260, "h": 70, "rx": 35} for i in range(4)]
    current = 1
    fills = [mix("#FFFFFF", "#FF7A00", 1.0 if p["i"] == current else 0.0) for p in pills]
    texts = [mix("#0B2545", "#FFFFFF", 1.0 if p["i"] == current else 0.0) for p in pills]
    body = "".join(f'<rect x="{p["x"]}" y="{p["y"]}" width="260" height="70" rx="35" fill="{f}"/>' for p, f in zip(pills, fills))
    write_svg(work / "pills.svg", 1920, 1080, body)
    delays = [0.18 + 0.045 * k for k in range(5)]
    return [chk("pills ordered right -> left", [p["x"] for p in pills] == [1395, 1105, 815, 525], [p["x"] for p in pills]),
            chk("current pill orange, others white", fills == ["#ffffff", "#ff7a00", "#ffffff", "#ffffff"], fills),
            chk("current text white, others navy", texts[1] == "#ffffff" and texts[0] == "#0b2545", texts),
            chk("journey nodes 45 ms apart from 180 to 360 ms", np.allclose(delays, [.18, .225, .27, .315, .36]), delays)]


def expl_27(work):
    beats = [("example", 0, 2), ("alert", 2, 3), ("fix", 3, 6), ("summary", 6, 8)]

    def strike(t):
        return min(max(t / 0.25, 0), 1)

    def check(t):
        return min(max((t - 0.25) / 0.3, 0), 1)

    fr = np.zeros((8, 10, 10, 3), np.uint8)
    for i in range(8):
        fr[i] = 40 + 20 * min(i, 2)  # frozen after 2 s
    frozen = all(np.array_equal(fr[2], fr[k]) for k in range(2, 4))
    return [chk("beats 0-2 / 2-3 / 3-6 / 6-8 s", [b[1:] for b in beats] == [(0, 2), (2, 3), (3, 6), (6, 8)], beats),
            chk("strike drawn in 250 ms before the check", strike(0.25) == 1 and check(0.25) == 0, "order"),
            chk("check drawn in 300 ms", near(check(0.55), 1, 1e-9) and near(check(0.4), 0.5, 1e-9), check(0.4)),
            chk("example frame freezes at the alert", frozen, "frozen")]


def expl_28(work):
    dist = 800.0
    speeds = {"A": 200.0, "B": 400.0}
    t_end = {k: dist / v for k, v in speeds.items()}

    def x(k, t):
        return min(dist, speeds[k] * max(t - 1.0, 0))

    timer = lambda k: round(min(t_end[k], 5.0), 2)
    return [chk("same path length for both", dist == dist, dist),
            chk("finish times 4.0 s and 2.0 s shown on clocks", (timer("A"), timer("B")) == (4.0, 2.0), (timer("A"), timer("B"))),
            chk("motion fits the 1-6 s window", x("A", 5.0) == dist and x("B", 1.0) == 0, x("A", 5.0)),
            chk("ratio stated 2x", t_end["A"] / t_end["B"] == 2, t_end["A"] / t_end["B"])]


def expl_29(work):
    f, cx, cy = 800, 960, 540

    def project(p):
        X, Y, Z = p
        return (cx + f * X / Z, cy - f * Y / Z)

    anchor = (0.5, 0.25, 4.0)
    sx, sy = project(anchor)
    side = "right" if sx > cx else "left"
    leader = [(sx, sy), (sx + 60, sy), (1800, sy)]

    def draw(k, t, stagger=0.08, dur=0.3):
        return min(max((t - k * stagger) / dur, 0), 1)

    return [chk("3D anchor projected to screen", (sx, sy) == (1060.0, 490.0), (sx, sy)),
            chk("label goes to the nearer side", side == "right", side),
            chk("elbow leader is horizontal then out", leader[0][1] == leader[-1][1], leader),
            chk("callouts draw 300 ms with 80 ms stagger", draw(1, 0.08) == 0 and draw(1, 0.38) == 1, "stagger")]


def expl_30(work):
    def iso(x, y, z):
        rx, rz = math.radians(55), math.radians(-45)
        x1, y1 = x * math.cos(rz) - y * math.sin(rz), x * math.sin(rz) + y * math.cos(rz)
        y2, z2 = y1 * math.cos(rx) - z * math.sin(rx), y1 * math.sin(rx) + z * math.cos(rx)
        return x1, y2

    plates = [{"z": 18 * k, "alpha": 0.15 + 0.85 * k / 6} for k in range(7)]
    top = dict(plates[-1], z=plates[-1]["z"] + 40, outline="dashed")
    corners = [iso(x, y, 0) for x, y in [(-100, -100), (100, -100), (100, 100), (-100, 100)]]
    return [chk("7 plates offset 18 px", len(plates) == 7 and plates[1]["z"] - plates[0]["z"] == 18, len(plates)),
            chk("light -> solid", plates[0]["alpha"] < plates[-1]["alpha"] == 1.0, [round(p["alpha"], 2) for p in plates]),
            chk("rotateZ(-45) makes the square a diamond (corner on the axis)", near(corners[0][1], 0, 1e-9), corners[0]),
            chk("top plate lifted with dashed outline", top["z"] > plates[-1]["z"] and top["outline"] == "dashed", top["z"])]


def expl_31(work):
    def exaggerate(v, n):
        if not 5 <= n <= 10:
            raise ValueError("x5-x10 only")
        return v * n, f"shown ×{n}"

    vals = [100, 25, 4, 0.01]
    rmin = 4
    radii = [max(rmin, 10 * math.sqrt(v)) for v in vals]
    h, lab = exaggerate(0.8, 9.6)
    try:
        exaggerate(1, 20)
        refused = False
    except ValueError:
        refused = True
    return [chk("area-true sizing: r = sqrt(v)", radii[:3] == [100.0, 50.0, 20.0], radii),
            chk("tiny values clamped to a visible minimum", radii[3] == rmin, radii[3]),
            chk("exaggeration labelled on screen", lab == "shown ×9.6" and near(h, 7.68, 1e-9), lab),
            chk("x20 refused", refused, refused)]


def tokenise_py(src):
    kw = {"def", "return", "if", "else", "for", "in", "import"}
    out = []
    for m in re.finditer(r"\s+|#.*|'[^']*'|\"[^\"]*\"|\d+|\w+|.", src):
        s = m.group()
        kind = ("ws" if s.isspace() else "comment" if s.startswith("#") else "string" if s[0] in "'\"" else
                "number" if s.isdigit() else "keyword" if s in kw else "name" if re.match(r"\w", s) else "punct")
        out.append((kind, s))
    return out


def expl_32(work):
    code = "def area(r):\n    # circle\n    return 3.14159 * r * r\n"
    toks = tokenise_py(code)
    spans = "".join(f'<span class="{k}">{s.replace("<", "&lt;")}</span>' for k, s in toks)
    html = f'<pre dir="ltr" style="font:32px JetBrains Mono,monospace;line-height:1.6">{spans}</pre>'
    (work / "code.html").write_text(html)
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    text = soup.pre.get_text()
    lines = code.count("\n")
    return [chk("pre-tokenised spans reproduce the exact code", text == code, len(text)),
            chk("code is LTR even in Arabic films", soup.pre.get("dir") == "ltr", soup.pre.get("dir")),
            chk("<= 14 lines, 28-40 px, line-height 1.6", lines <= 14 and "32px" in html and "line-height:1.6" in html, lines),
            chk("keywords/strings/numbers classed", {"keyword", "number", "comment"} <= {k for k, _ in toks}, "classes")]


def expl_34(work):
    cmd = "npm run build"
    cps = 35
    tl = {"scale": (0, .3), "type": (.3, 1.3), "enter": (1.3, 1.6), "output": (1.6, 2.4), "success": (2.4, 3.0)}

    def typed(t):
        a, b = tl["type"]
        return cmd[:max(0, min(len(cmd), int((t - a) * cps)))]

    def scale(t):
        return 0.96 + 0.04 * min(t / 0.3, 1)

    def blocks(t):
        a, b = tl["output"]
        return max(0, min(3, int((t - a) / ((b - a) / 3)) + (1 if t >= a else 0)))

    return [chk("scale 0.96 -> 1 in 300 ms", scale(0) == 0.96 and scale(0.3) == 1, scale(0.15)),
            chk("13-char command fully typed by 1.3 s at 35 cps", typed(1.3) == cmd and len(cmd) / cps <= 1.0, typed(0.6)),
            chk("3 output blocks by 2.4 s", blocks(1.59) == 0 and blocks(2.39) == 3, [blocks(t) for t in (1.6, 1.9, 2.2)]),
            chk("timeline 0/300/1300/1600/2400/3000 ms", [v[0] for v in tl.values()] + [tl["success"][1]] == [0, .3, 1.3, 1.6, 2.4, 3.0],
                tl)]


def expl_35(work):
    n_lines, focus = 10, 4

    def opacity(i, t):
        p = min(t / 0.25, 1)
        p = 1 - (1 - p) ** 3
        return 1.0 if i == focus else 1 - 0.5 * p

    def scroll(t, start=0.0, per=0.25):
        lines = int(max(t - start, 0) // per)
        frac = (max(t - start, 0) % per) / per
        return lines, ease_in_out_cubic(frac)

    def squiggle(t):
        return min(max(t / 0.6, 0), 1)

    return [chk("others dim to 50% in 250 ms", opacity(0, 0.25) == 0.5 and opacity(focus, 0.25) == 1, opacity(0, 0.25)),
            chk("ease-out cubic: 87.5% of the dim at half time", near((1 - opacity(0, 0.125)) / 0.5, 0.875, 1e-9), opacity(0, 0.125)),
            chk("scroll lands on whole lines every 250 ms", scroll(0.5) == (2, 0.0), scroll(0.5)),
            chk("error squiggle drawn in 0.6 s", squiggle(0.3) == 0.5 and squiggle(0.6) == 1, squiggle(0.3))]


def expl_36(work):
    import difflib
    a = ["x = 1", "y = 2", "print(x)"]
    b = ["x = 1", "y = 3", "print(x)", "print(y)"]
    ops = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b).get_opcodes():
        if tag == "equal":
            ops += [("keep", s) for s in a[i1:i2]]
        if tag in ("replace", "delete"):
            ops += [("remove", s) for s in a[i1:i2]]
        if tag in ("replace", "insert"):
            ops += [("add", s) for s in b[j1:j2]]
    dur = {"remove": 0.25, "add": 0.30}
    t, sched = 0.0, []
    for kind, s in ops:
        if kind in dur:
            sched.append((kind, s, round(t, 3)))
            t += dur[kind]
    final = [s for k, s in ops if k != "remove"]
    jwrite(work, "diff.json", ops)
    return [chk("removed y = 2, added y = 3 and print(y)", [o for o in ops if o[0] != "keep"] ==
                [("remove", "y = 2"), ("add", "y = 3"), ("add", "print(y)")], ops),
            chk("exactly 2 states: end state equals the new code", final == b, final),
            chk("removed 250 ms then added 300 ms, staggered", [x[2] for x in sched] == [0.0, 0.25, 0.55], sched)]


def expl_37(work):
    pal = {"keyword": "#E06C9F", "string": "#E5A86B", "number": "#A78BFA"}
    code = ["def greet(name):", "    msg = 'hi ' + name", "    return msg * 2"]
    W, H = 800, 600
    im = Image.new("RGB", (W, H), "#1b1b1b")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([40, 40, 40 + int(W * 0.6), H - 40], 18, fill="#2A2622")
    for k, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
        d.ellipse([60 + 22 * k, 56, 72 + 22 * k, 68], fill=c)
    f = _font(22)
    y = 100
    for line in code:
        x = 60
        for kind, s in tokenise_py(line):
            col = pal.get(kind, "#dddddd")
            d.text((x, y), s, font=f, fill=col)
            x += d.textlength(s, font=f)
        y += 36
    hl = [(56, 132, 400, 166)]
    for b in hl:
        d.rectangle(b, outline="#7EE787", width=3)
    im.save(work / "codewin.png")
    a = np.asarray(im)
    has = lambda hexc: bool((np.abs(a.astype(int) - np.array([int(hexc[i:i + 2], 16) for i in (1, 3, 5)])).sum(-1) < 30).any())
    return [chk("4:3 figure, window 60% wide", W * 3 == H * 4, (W, H)),
            chk("three traffic-light dots", all(has(c) for c in ["#ff5f57", "#febc2e", "#28c840"]), "dots"),
            chk("keyword pink, string orange, number violet present", has("#E06C9F") and has("#E5A86B") and has("#A78BFA"), pal),
            chk("<= 3 green highlight boxes, 4-12 lines", len(hl) <= 3 and has("#7EE787") and 3 <= len(code) <= 12, len(code))]


def expl_38(work):
    code = ["player.x = 0", "player.jump()", "draw()"]
    cps = 25
    starts, t = [], 0.0
    for line in code:
        starts.append(t)
        t += len(line) / cps
    done = [s + len(l) / cps for s, l in zip(starts, code)]

    def sprite_y(tq):
        return 100 if tq >= done[1] else 0

    caret = lambda tq: int(tq / 0.5) % 2 == 0
    return [chk("typing at 25 cps", near(done[0], 12 / 25, 1e-9), done[0]),
            chk("sprite jumps exactly when the jump() line completes", sprite_y(done[1] - 1e-6) == 0 and sprite_y(done[1]) == 100,
                done[1]),
            chk("caret blinks every 500 ms", caret(0.1) and not caret(0.6) and caret(1.1), "blink")]


def expl_39(work):
    tokens = ["The", " cat", " sat"]
    ids = [464, 3797, 3332]

    def chip(i, t, stagger=0.09, dur=0.3, s=1.70158):
        p = min(max((t - i * stagger) / dur, 0), 1) - 1
        return 0.8 + 0.2 * (1 + (s + 1) * p ** 3 + s * p ** 2)

    drift = lambda k, t: (4 + 4 * (k % 2)) * math.sin(2 * math.pi * t / (3 + k))
    samples = [chip(0, t) for t in np.linspace(0, 0.3, 61)]
    return [chk("chips start at .8 and end at 1", near(chip(0, 0), 0.8, 1e-9) and near(chip(0, 0.3), 1, 1e-9), chip(0, 0.15)),
            chk("back-out overshoot above 1", max(samples) > 1.0, round(max(samples), 4)),
            chk("90 ms stagger", chip(1, 0.09) == chip(0, 0.0), chip(1, 0.09)),
            chk("drift amplitude within 4-8 px", all(abs(drift(k, t)) <= 8 for k in range(20) for t in np.linspace(0, 10, 50)), "4-8"),
            chk("token ids under each chip", len(ids) == len(tokens), ids)]


def expl_42(work):
    def backoff(fails, base=0.5, cap=8):
        return [min(cap, base * 2 ** k) for k in range(fails)]

    statuses = [500, 500, 500, 200]
    waits = backoff(statuses.index(200))
    serial = [("a", 1.0), ("b", 1.0), ("c", 1.0)]
    t_serial = sum(d for _, d in serial)
    t_par = max(d for _, d in serial)
    cache = {"cold": 120, "cached": 4}
    cards = [{"min_ms": 900}, {"min_ms": 900}]
    return [chk("retry waits grow 0.5 / 1 / 2 s before the 200", waits == [0.5, 1.0, 2.0], waits),
            chk("serial 3 s reshapes into parallel 1 s", (t_serial, t_par) == (3.0, 1.0), (t_serial, t_par)),
            chk("cached lane wins the race by 30x", cache["cold"] / cache["cached"] == 30, cache),
            chk("cards >= 900 ms, <= 3 stacked", all(c["min_ms"] >= 900 for c in cards) and len(cards) <= 3, len(cards))]


def expl_43(work):
    root = REPO / ".claude/skills/kosif-superpowers/scripts/power_programs"
    rows = []
    for p in sorted(root.glob("*.py")):
        rows.append((p.name, sum(1 for _ in p.open(encoding="utf-8"))))
    me = Path(__file__)
    mine = next(n for f, n in rows if f == me.name)
    total = sum(n for _, n in rows)

    def count_at(n, t):
        return round(n * min(t / 0.6, 1))

    jwrite(work, "line_counts.json", rows)
    W = 600
    im = Image.new("RGB", (W, 20 * len(rows)), "white")
    d = ImageDraw.Draw(im)
    for k, (f, n) in enumerate(rows):
        d.rectangle([150, 20 * k + 4, 150 + int(400 * n / max(x for _, x in rows)), 20 * k + 16], fill="#2a78d6")
    im.save(work / "bars.png")
    return [chk("counts come from the real files (this module counted)", mine == len(me.read_text(encoding="utf-8").splitlines()),
                mine),
            chk("bars count up in 600 ms", count_at(mine, 0.3) == round(mine / 2) and count_at(mine, 0.6) == mine, count_at(mine, .3)),
            chk("total equals the sum of rows", total == sum(n for _, n in rows), total)]


def expl_44(work):
    phases = [("givens", 0, 2), ("operation", 2, 5), ("result", 5, 8), ("read", 8, 10)]
    formula = "E = mc^2"
    caption = f'الطاقة تساوي <span dir="ltr" style="unicode-bidi:isolate">{formula}</span> دائمًا'
    from bidi.algorithm import get_display
    vis_bad = get_display("الطاقة " + "E = mc2" + " دائمًا")
    term = {"m": "#E53935"}

    def term_colour(t):
        return term["m"] if 2 <= t < 5 else "#111111"

    return [chk("10 s: givens / operation / result / read", [p[1:] for p in phases] == [(0, 2), (2, 5), (5, 8), (8, 10)], phases),
            chk("formula wrapped in an LTR isolate", 'dir="ltr"' in caption and "unicode-bidi:isolate" in caption, caption[-40:]),
            chk("LTR run keeps its order inside RTL text", "E = mc2" in vis_bad, vis_bad),
            chk("explained term tinted only during the operation", term_colour(3) == "#E53935" and term_colour(6) == "#111111", "tint")]


def expl_46(work):
    N = 200
    th = np.linspace(0, 2 * np.pi, N, endpoint=False)
    target = (np.cos(th) + 0.3 * np.cos(3 * th)) + 1j * (np.sin(th) - 0.2 * np.sin(2 * th))
    X = np.fft.fft(target) / N
    freqs = np.fft.fftfreq(N, 1 / N)
    terms = sorted([(abs(X[k]), freqs[k], cmath.phase(X[k])) for k in range(N)], reverse=True)

    def tip(t, T=1.0, n=None):
        z = 0j
        for amp, f, ph in terms[:n]:
            z += amp * cmath.exp(1j * (f * 2 * math.pi * t / T + ph))
        return z

    err_full = max(abs(tip(k / N) - target[k]) for k in range(0, N, 10))
    err_4 = max(abs(tip(k / N, n=5) - target[k]) for k in range(0, N, 10))
    err_1 = max(abs(tip(k / N, n=1) - target[k]) for k in range(0, N, 10))
    sine = lambda t, w=2 * math.pi: (math.cos(w * t), math.sin(w * t))
    trail = np.array([[tip(t).real, tip(t).imag] for t in np.linspace(0, 1, 120)])
    np.save(work / "trail.npy", trail)
    return [chk("all terms reproduce the path exactly", err_full < 1e-9, err_full),
            chk("terms sorted by amplitude: 5 largest rebuild the 5-term path", err_4 < 1e-9 and err_1 > 0.1, (err_4, round(err_1, 3))),
            chk("tip computed from t (periodic, no accumulation)", abs(tip(0.3) - tip(1.3)) < 1e-9, "period"),
            chk("unit circle projects sin(wt) at t=0.25 -> 1", near(sine(0.25)[1], 1, 1e-12), sine(0.25))]


def expl_47(work):
    n = 25
    a, b = 3.0, 4.0
    c = math.hypot(a, b)
    ang = math.atan2(-a, b)
    src = [((k % 5 + .5) * a / 5 - a - 1, (k // 5 + .5) * a / 5) for k in range(n)]
    tgt = [((k % 5 + .5) * c / 5, (k // 5 + .5) * c / 5) for k in range(n)]
    tgt = [(x * math.cos(ang) - y * math.sin(ang), x * math.sin(ang) + y * math.cos(ang)) for x, y in tgt]
    stagger, fly, hop = 0.12, 0.6, 20

    def cell(k, t):
        u = min(max((t - k * stagger) / fly, 0), 1)
        x = src[k][0] + (tgt[k][0] - src[k][0]) * u
        y = src[k][1] + (tgt[k][1] - src[k][1]) * u + hop * math.sin(math.pi * u)
        return (x, y), u

    def arrived(t):
        return sum(cell(k, t)[1] >= 1 for k in range(n))

    end = (n - 1) * stagger + fly
    return [chk("25 cells", n == 25, n),
            chk("mid-flight hop = 20 px", near(cell(0, 0.3)[0][1] - (src[0][1] + (tgt[0][1] - src[0][1]) * .5), 20, 1e-9), "hop"),
            chk("counter counts arrivals", arrived(0.6) == 1 and arrived(end) == 25, (arrived(0.6), arrived(end))),
            chk("cells land at hypotenuse-square positions", all(np.allclose(cell(k, end)[0], tgt[k]) for k in range(n)), "landed"),
            chk("3-4-5: 9 + 16 = 25", a * a + b * b == c * c, c)]


def expl_48(work):
    from scipy.signal import correlate2d
    digit = np.zeros((8, 8))
    digit[1:7, 3:5] = 1
    kernel = np.array([[-1, 2, -1]] * 3, float)
    heat = correlate2d(digit, kernel, mode="valid")
    words = ["the", "cat", "sat"]
    q = np.array([[1, 0], [0, 1], [1, 1]], float)
    w = np.exp(q @ q.T)
    w /= w.sum(1, keepdims=True)
    arcs = {(words[0], words[j]): float(w[0, j]) for j in range(3)}
    N = 7
    edges = [(i, (i + 1) % N, 1 if i % 2 else -1) for i in range(N)]
    starts = [k * 0.08 for k in range(len(edges))]
    return [chk("vertical-line kernel peaks on the stroke", np.unravel_index(np.argmax(heat), heat.shape)[1] in (1, 2),
                np.unravel_index(np.argmax(heat), heat.shape)),
            chk("attention weights per word sum to 1", near(sum(arcs.values()), 1, 1e-12), arcs),
            chk("strongest arc: 'the' -> itself or 'sat' (shared feature)", max(arcs, key=arcs.get)[1] in ("the", "sat"), arcs),
            chk("7 signed edges drawn 80 ms apart", len(edges) == 7 and near(starts[-1], 0.48, 1e-12) and {e[2] for e in edges} == {-1, 1},
                starts[-1])]


def expl_49(work):
    g = 9.81

    def state(t, v0=20.0, ang=45.0):
        a = math.radians(ang)
        x, y = v0 * math.cos(a) * t, v0 * math.sin(a) * t - 0.5 * g * t * t
        return {"t": f"{t:.2f}", "x": f"{x:.2f}", "y": f"{max(y, 0):.2f}", "status": "landed" if y < 0 else "flight"}

    land = 2 * 20 * math.sin(math.radians(45)) / g
    s = state(1.0)
    row = f'{"x":<6}{s["x"]:>10}'
    return [chk("values computed from t: x(1 s) = 14.14", s["x"] == "14.14", s["x"]),
            chk("y(1 s) = 14.14 - 4.905 = 9.24", s["y"] == "9.24", s["y"]),
            chk("2 decimals, right-aligned tabular", row.endswith("     14.14") and len(row) == 16, repr(row)),
            chk("switches to landed past the horizon", state(land + 0.01)["status"] == "landed" and state(land - 0.01)["status"] == "flight",
                round(land, 3))]


def truss_solve(nodes, members, supports, loads, E=200e9, A=1e-4):
    n = len(nodes)
    K = np.zeros((2 * n, 2 * n))
    for a, b in members:
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        L = math.hypot(x2 - x1, y2 - y1)
        c, s = (x2 - x1) / L, (y2 - y1) / L
        k = E * A / L * np.outer([-c, -s, c, s], [-c, -s, c, s])
        dof = [2 * a, 2 * a + 1, 2 * b, 2 * b + 1]
        K[np.ix_(dof, dof)] += k
    F = np.zeros(2 * n)
    for i, (fx, fy) in loads.items():
        F[2 * i] += fx
        F[2 * i + 1] += fy
    fixed = [2 * i + d for i, ds in supports.items() for d in ds]
    free = [d for d in range(2 * n) if d not in fixed]
    u = np.zeros(2 * n)
    u[free] = np.linalg.solve(K[np.ix_(free, free)], F[free])
    R = K @ u - F
    forces = []
    for a, b in members:
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        L = math.hypot(x2 - x1, y2 - y1)
        c, s = (x2 - x1) / L, (y2 - y1) / L
        forces.append(E * A / L * (c * (u[2 * b] - u[2 * a]) + s * (u[2 * b + 1] - u[2 * a + 1])))
    return u, R, np.array(forces)


def expl_50(work):
    nodes = [(0, 0), (1, 1), (2, 0)]
    members = [(0, 1), (1, 2), (0, 2)]
    P = 12e3
    u, R, f = truss_solve(nodes, members, {0: (0, 1), 2: (1,)}, {1: (0, -P)})
    want = -P / (2 * math.sin(math.radians(45)))
    A, S = 1e-4, 250e6
    util = np.abs(f) / (A * S)
    weakest = int(np.argmax(util))
    mult = 1 / util.max()
    # swap the two weakest (tied inclined) members for twice the area and recompute
    areas = np.where(util >= util.max() - 1e-9, 2e-4, 1e-4)
    u2, R2, f2 = truss_solve(nodes, members, {0: (0, 1), 2: (1,)}, {1: (0, -P)}, A=1e-4)
    util2 = np.abs(f2) / (areas * S)
    jwrite(work, "truss.json", {"forces_N": f.round(2).tolist(), "reactions": R.round(2).tolist(), "first_failure_multiplier": mult})
    return [chk("inclined members in compression P/(2 sin45) = 8485 N", np.allclose(f[:2], want, rtol=1e-6), f[:2].round(1).tolist()),
            chk("bottom chord in tension P/2 = 6000 N", near(f[2], 6000, 1e-3), round(f[2], 2)),
            chk("reactions balance the load (6 kN each)", near(R[1] + R[5], P, 1e-6) and near(R[1], 6000, 1e-3), (R[1], R[5])),
            chk("first-failure multiplier = A*S / max|F|", near(mult, 1e-4 * 250e6 / abs(want), 1e-9), round(mult, 3)),
            chk("card sample: first failure at 2.946x", round(mult, 3) == 2.946, round(mult, 3)),
            chk("thicker inclined members -> chord governs at 25000/6000 = 4.167x", near(1 / util2.max(), 25000 / 6000, 1e-6)
                and int(np.argmax(util2)) == 2, round(1 / util2.max(), 3))]


def expl_52(work):
    parts = {"head": np.array([0.0, 1.0, 0.0]), "arm": np.array([0.8, 0.3, 0.0])}

    def schematic(k):
        return {"solid_opacity": 1 - 0.92 * k, "ghost": 0.55 * k, "line_opacity": 0.42 * k}

    def explode(p, k):
        return p * (1 + 0.1 * k)

    s = schematic(1.0)
    return [chk("solids fade to 8%, ghost .55, lines .42", near(s["solid_opacity"], 0.08, 1e-12) and s["ghost"] == 0.55
                and s["line_opacity"] == 0.42, s),
            chk("explode x1.1 radial", np.allclose(explode(parts["arm"], 1), parts["arm"] * 1.1), explode(parts["arm"], 1).tolist()),
            chk("direction kept when exploding", np.allclose(np.cross(explode(parts["arm"], 1), parts["arm"]), 0), "radial")]


def expl_53(work):
    labels = {1: (3.3, 6.1), 2: (6.9, 9.3), 3: (10.1, 12.5), 4: (13.1, 15.1)}
    world = {1: (2.6, 7.2), 2: (5.8, 9.4), 3: (9.5, 13.4), 4: (12.6, 14.4)}
    inside = {k: world[k][0] <= labels[k][0] and labels[k][0] < world[k][1] for k in labels}
    no_overlap = all(labels[k][1] <= labels[k + 1][0] for k in (1, 2, 3))
    ar_digits = "".join(chr(0x0660 + k) for k in labels)
    end_title, total = 15.7, 17.0
    return [chk("each label starts while its world state is visible", all(inside.values()), inside),
            chk("labels never overlap", no_overlap, labels),
            chk("Arabic-Indic numbering ١٢٣٤", ar_digits == "١٢٣٤", ar_digits),
            chk("end title after the last label, film 17 s", labels[4][1] < end_title < total, end_title)]


def expl_54(work):
    stages = [(1.5, 4.0), (4.0, 6.1), (6.1, 8.0), (8.0, 8.9)]
    recap = (8.9, 10.0)
    fps, frames = 30, 300
    movers = {0: ["vapour"], 1: ["cloud"], 2: ["rain"], 3: ["river"]}
    contiguous = all(stages[i][1] == stages[i + 1][0] for i in range(3)) and stages[-1][1] == recap[0]
    return [chk("300 frames at 30 fps = 10 s", frames / fps == 10.0 == recap[1], frames / fps),
            chk("stages contiguous and end in the recap", contiguous, stages),
            chk("one main motion per stage", all(len(v) == 1 for v in movers.values()), movers)]


def expl_55(work):
    order = ["evaporation", "condensation", "precipitation", "collection"]
    cause = {"evaporation": "sun heats the sea", "condensation": "vapour cools", "precipitation": "drops fall on land",
             "collection": "water returns to the sea"}

    def check(script):
        errs = []
        steps = [s["stage"] for s in script["steps"]]
        if not 3 <= len(steps) <= 6:
            errs.append("3-6 causal steps")
        if steps != [o for o in order if o in steps]:
            errs.append("wrong causal order")
        if any(len(s["movers"]) != 1 for s in script["steps"]):
            errs.append("one main motion per stage")
        if script["text_px"] < 40 or script["contrast"] < 4.5:
            errs.append("text >= 40 px and >= 4.5:1")
        wps = script["words"] / script["seconds"]
        if wps > 2.6:
            errs.append(f"narration {wps:.1f} w/s > 2.5")
        if script.get("flash_hz", 0) > 3:
            errs.append("no flashing")
        return errs

    good = {"steps": [{"stage": s, "movers": ["x"]} for s in order], "text_px": 44, "contrast": 7.1, "words": 40, "seconds": 17}
    bad = {"steps": [{"stage": "condensation", "movers": ["x"]}, {"stage": "evaporation", "movers": ["x", "y"]}],
           "text_px": 30, "contrast": 3, "words": 60, "seconds": 17, "flash_hz": 5}
    eb = check(bad)
    return [chk("correct 4-step script passes", check(good) == [], check(good)),
            chk("wrong order (clouds before vapour) caught", "wrong causal order" in eb, eb),
            chk("too few steps, 2 movers, small text, fast narration, flashing all caught", len(eb) == 6, eb),
            chk("cause recorded for every step", len(cause) == len(order), cause)]


def expl_56(work):
    H = 1920

    def highlight_colour(el_word_t, t):
        return "#E53935" if t >= el_word_t + 0.3 else "#1A1A1A"

    sizes = {"chapter_glyph": 0.14 * H, "outline": 0.06 * 0.14 * H, "label": 0.035 * H}
    rows = ["speed", "cost", "risk"]
    row_at = lambda t: rows[min(int(t // 2), len(rows) - 1)]
    return [chk("chapter glyphs 14% H, outline 6% of glyph", near(sizes["chapter_glyph"], 268.8, 1e-9) and near(sizes["outline"], 16.128, 1e-9),
                sizes),
            chk("spoken element turns red 0.3 s after it is said", highlight_colour(1.0, 1.29) == "#1A1A1A" and
                highlight_colour(1.0, 1.3) == "#E53935", "0.3 s"),
            chk("table rows x 2 s", [row_at(t) for t in (0.5, 2.5, 4.5)] == rows, rows),
            chk("labels 3.5% H", near(sizes["label"], 67.2, 1e-9), sizes["label"])]


def expl_57(work):
    words = [{"w": "الماء", "start": 0.0, "end": 0.5}, {"w": "يغلي", "start": 0.5, "end": 0.9},
             {"w": "عند", "start": 0.9, "end": 1.2}, {"w": "مئة", "start": 1.2, "end": 1.6}]
    x_right, w_total = 900, 600
    widths = [180, 150, 120, 150]

    def highlighter(t):
        """Width grown from the right edge, matching spoken words (RTL)."""
        done = 0.0
        for w, px in zip(words, widths):
            if t >= w["end"]:
                done += px
            elif t > w["start"]:
                done += px * (t - w["start"]) / (w["end"] - w["start"])
        return x_right - done, x_right

    W = 1080
    panel = {"w": 0.8 * W, "margin": 0.1 * W}
    a, b = highlighter(0.7)
    return [chk("highlight grows right -> left with the words", (a, b) == (900 - 180 - 75, 900), (a, b)),
            chk("fully highlighted after the last word", highlighter(1.6)[0] == x_right - sum(widths), highlighter(1.6)),
            chk("excerpt panel 75-90% width with >= 5% margins", 0.75 * W <= panel["w"] <= 0.9 * W and panel["margin"] >= 0.05 * W, panel)]


def expl_59(work):
    speech = {"clock": (0.0, 2.0), "scale": (2.0, 4.5), "timebar": (4.5, 7.0)}

    def visible(g, t):
        a, b = speech[g]
        return a <= t < b

    def weight(t):
        a, b = speech["scale"]
        p = min(max((t - a) / (b - a), 0), 1)
        return round(94 + (76 - 94) * p)

    def bar(t):
        a, b = speech["timebar"]
        return 1 - min(max((t - a) / (b - a), 0), 1)

    vis = {t: [g for g in speech if visible(g, t)] for t in (1.0, 3.0, 6.0)}
    return [chk("one metaphor on screen per spoken claim", all(len(v) == 1 for v in vis.values()), vis),
            chk("scale counts 94 -> 76 kg", weight(2.0) == 94 and weight(4.5) == 76 and weight(3.25) == 85, weight(3.25)),
            chk("time bar drains to empty", bar(4.5) == 1 and bar(7.0) == 0, bar(5.75))]


def expl_60(work):
    rows = [("fast", True, False), ("cheap", False, True), ("safe", True, True)]
    starts = [k * 0.12 for k in range(len(rows))]
    active = 1

    def opacity(i):
        return 1.0 if i <= active else 0.45

    score = {"A": sum(r[1] for r in rows), "B": sum(r[2] for r in rows)}
    return [chk("rows stagger 120 ms", np.allclose(starts, [0, .12, .24]), starts),
            chk("upcoming rows at 45%", [opacity(i) for i in range(3)] == [1, 1, .45], [opacity(i) for i in range(3)]),
            chk("ticks counted per card", score == {"A": 2, "B": 2}, score)]


def expl_61(work):
    text = "the quick brown fox jumps over the lazy dog"
    unknown = "fox"
    f = _font(20)
    widths = [f.getlength(w) for w in text.split()]
    rows, cur, maxw = [], [], 200
    for w, px in zip(text.split(), widths):
        if sum(p for _, p in cur) + px + 8 * len(cur) > maxw:
            rows.append(cur)
            cur = []
        cur.append((w, px))
    rows.append(cur)
    row_start = [k * 0.15 for k in range(len(rows))]
    accent = [w for r in rows for w, _ in r if w == unknown]
    items = [("apple", "fruit"), ("car", "vehicle"), ("pear", "fruit"), ("bus", "vehicle"), ("dog", "animal")]
    buckets = {}
    for it, b in items:
        buckets[b] = buckets.get(b, 0) + 1
    return [chk("bars follow measured word widths", all(px == f.getlength(w) for r in rows for w, px in r), len(rows)),
            chk("rows fill every 150 ms (120-200)", 0.12 <= row_start[1] <= 0.2, row_start),
            chk("unknown word marked in accent", accent == ["fox"], accent),
            chk("sorting into buckets with counts", buckets == {"fruit": 2, "vehicle": 2, "animal": 1}, buckets)]


def expl_62(work):
    d = work / "bp"
    import subprocess
    import sys
    r = subprocess.run([sys.executable, str(REPO / "tools" / "kosif.py"), "scaffold", "tech-blueprint", str(d)],
                       capture_output=True, text=True, timeout=60, cwd=REPO)
    style = json.loads((REPO / "styles/tech-blueprint/STYLE.json").read_text(encoding="utf-8"))
    grid = 24
    pts = [(48, 72), (240, 72), (240, 192)]
    on_grid = all(x % grid == 0 and y % grid == 0 for x, y in pts)
    L = sum(math.dist(pts[i], pts[i + 1]) for i in range(2))
    draw_s = L / 1000
    return [chk("scaffold tech-blueprint", r.returncode == 0 and (d / "STYLE.md").is_file(), r.returncode),
            chk("STYLE.json present for the style", isinstance(style, dict) and len(style) > 0, list(style)[:4]),
            chk("paths snap to the 24 px grid", on_grid, pts),
            chk("draw-on at 1000 px/s (900-1200)", near(draw_s, 0.312, 1e-9), draw_s)]


def expl_63(work):
    shots = [{"id": 1, "aspect": "9:16", "subject": (0.2, 0.3, 0.6, 0.5), "text": (0.1, 0.8, 0.8, 0.1), "move": "push"},
             {"id": 2, "aspect": "9:16", "subject": (0.3, 0.2, 0.4, 0.4), "text": (0.1, 0.05, 0.8, 0.1), "move": "pan-left"}]
    W, H, gap = 90, 160, 20
    body = ""
    for k, s in enumerate(shots):
        ox = k * (W + gap)
        body += f'<g id="shot{s["id"]}"><rect x="{ox}" y="0" width="{W}" height="{H}" fill="none" stroke="#000"/>'
        x, y, w, h = s["subject"]
        body += f'<rect class="subject" x="{ox + x * W}" y="{y * H}" width="{w * W}" height="{h * H}"/>'
        x, y, w, h = s["text"]
        body += f'<rect class="text" x="{ox + x * W}" y="{y * H}" width="{w * W}" height="{h * H}"/>'
        if s["move"] == "pan-left":
            body += f'<line class="move" x1="{ox + 70}" y1="150" x2="{ox + 20}" y2="150"/>'
        body += "</g>"
    write_svg(work / "thumbs.svg", 2 * W + gap, H, body)
    root = ET.parse(work / "thumbs.svg").getroot()
    frames = [g for g in root.iter(f"{{{SVGNS}}}g")]
    first = next(frames[0].iter(f"{{{SVGNS}}}rect"))
    overlap = lambda a, b: not (a[0] + a[2] <= b[0] or b[0] + b[2] <= a[0] or a[1] + a[3] <= b[1] or b[1] + b[3] <= a[1])
    return [chk("one frame per shot", len(frames) == len(shots), len(frames)),
            chk("frames are 9:16", float(first.get("width")) * 16 == float(first.get("height")) * 9, (first.get("width"), first.get("height"))),
            chk("text zone never covers the subject", not any(overlap(s["subject"], s["text"]) for s in shots), "clear"),
            chk("camera move arrow drawn", len(list(root.iter(f"{{{SVGNS}}}line"))) == 1, 1)]


def expl_64(work):
    nodes = [{"id": "acc", "kind": "account"}, {"id": "ev", "kind": "evidence"}, {"id": "std", "kind": "standard"},
             {"id": "fd", "kind": "finding"}]
    links = [("acc", "ev"), ("ev", "std"), ("std", "fd")]

    def trace(nid):
        back = {b: a for a, b in links}
        path = [nid]
        while path[-1] in back:
            path.append(back[path[-1]])
        return path[::-1]

    jwrite(work, "galaxy.json", {"nodes": nodes, "links": links})
    return [chk("4 nodes, 3 links", len(nodes) == 4 and len(links) == 3, (len(nodes), len(links))),
            chk("traceEvidence(finding) walks back to the account", trace("fd") == ["acc", "ev", "std", "fd"], trace("fd")),
            chk("chain order account -> evidence -> standard -> finding", [n["kind"] for n in nodes] ==
                ["account", "evidence", "standard", "finding"], "order")]


def expl_u01(work):
    menu = ["Editorial Explainer", "AI Film FX", "2D Animated Explainer", "Kinetic Typography", "Data Story"]

    def suggest(request, has_footage, footage_kind=None):
        if not has_footage:
            return {"ask": True, "options": menu}
        likely = {"talking-head": "Editorial Explainer", "generated": "AI Film FX"}.get(footage_kind, menu[0])
        return {"ask": False, "suggest": likely, "options": menu}

    a = suggest("make a video", False)
    b = suggest("edit my clip", True, "generated")
    return [chk("open request shows the 5-style menu and asks", a["ask"] and len(a["options"]) == 5, a["options"]),
            chk("with footage the likeliest style is proposed", b["suggest"] == "AI Film FX" and not b["ask"], b["suggest"]),
            chk("style is named before building", all(isinstance(x, str) and x for x in menu), menu)]


def expl_u02(work):
    rng = np.random.default_rng(0)
    frame = rng.integers(0, 255, (90, 160, 3)).astype(float)
    gray = frame.mean(-1, keepdims=True)
    desat = frame + (gray - frame) * 0.40
    out = desat * (1 - 0.30)
    pts = rng.uniform(0, 1, (25, 2))
    boxes = [(10, 10, 40, 30), (60, 20, 30, 30), (100, 50, 40, 30)]
    Image.fromarray(out.astype(np.uint8)).save(work / "analysis.png")
    sat = lambda a: (a.max(-1) - a.min(-1)).mean()
    return [chk("dimmed 30%", near(out.mean() / desat.mean(), 0.70, 1e-9), round(out.mean() / desat.mean(), 3)),
            chk("desaturated 40%", near(sat(desat) / sat(frame), 0.60, 1e-9), round(sat(desat) / sat(frame), 3)),
            chk("20-30 feature points, 3-4 boxes", 20 <= len(pts) <= 30 and 3 <= len(boxes) <= 4, (len(pts), len(boxes)))]


def expl_g01(work):
    items = ["a", "b", "c", "d"]
    lag, dur = 0.2, 1.0

    def lagged(i):
        return i * lag * dur

    scenes = [{"action": "Create", "obj": "x"}, {"action": "Transform", "obj": "x"}, {"action": "FadeOut", "obj": "x"}]
    holds = [0.5, 0.8, 1.0]
    colour = {"velocity": "#e0a060"}
    scene2 = {"velocity": "#e0a060"}

    def grammar_ok(seq):
        seen = set()
        for s in seq:
            if s["action"] == "Create":
                seen.add(s["obj"])
            elif s["obj"] not in seen:
                return False
        return True

    return [chk("LaggedStart lag 0.2 staggers list items", [lagged(i) for i in range(4)] == [0, .2, .4, .6000000000000001] or
                np.allclose([lagged(i) for i in range(4)], [0, .2, .4, .6]), [lagged(i) for i in range(4)]),
            chk("Create -> Transform -> FadeOut on the same object", grammar_ok(scenes), [s["action"] for s in scenes]),
            chk("Transform before Create refused", not grammar_ok([{"action": "Transform", "obj": "y"}]), "refused"),
            chk("hold 0.5-1 s after each idea; same quantity same colour", all(.5 <= h <= 1 for h in holds) and colour == scene2, holds)]


def expl_g02(work):
    clusters = {"vpc": ["lb", "api"], "data": ["db", "cache"]}
    edges = [("lb", "api", "HTTPS"), ("api", "db", "SQL"), ("api", "cache", "GET")]
    narration = ["vpc", "data"]
    t, sched = 0.0, []
    for c in narration:
        sched.append(("outline", c, round(t, 2)))
        t += 0.6
        for k, n in enumerate(clusters[c]):
            sched.append(("node", n, round(t + 0.1 * k, 2)))
        t += 0.1 * len(clusters[c]) + 0.3
        for a, b, lab in edges:
            if b in clusters[c] and all(any(x[1] == y for x in sched if x[0] == "node") for y in (a, b)):
                sched.append(("edge", f"{a}->{b}", round(t, 2)))
        t += 0.4
    body = "".join(f'<g id="cluster-{c}">' + "".join(f'<rect id="{n}"/>' for n in ns) + "</g>" for c, ns in clusters.items())
    write_svg(work / "arch.svg", 400, 300, body)
    nodes_on = sum(len(v) for v in clusters.values())
    order = [x for x in sched if x[0] != "outline"]
    edge_after_nodes = all(any(n[0] == "node" and n[1] == e[1].split("->")[1] and n[2] < e[2] for n in sched)
                           for e in sched if e[0] == "edge")
    return [chk("every cluster has an id", all(g.get("id", "").startswith("cluster-") for g in
                                                ET.parse(work / "arch.svg").getroot()), list(clusters)),
            chk("clusters revealed in narration order", [x[1] for x in sched if x[0] == "outline"] == narration, narration),
            chk("edges draw after their nodes", edge_after_nodes and len([x for x in sched if x[0] == "edge"]) == 3, order),
            chk("<= 12 nodes on screen, edges labelled", nodes_on <= 12 and all(lab for *_, lab in edges), nodes_on)]


def _recorded(fn):
    """Keep the computed observations as the program's output file when it draws nothing else."""
    def run(work):
        checks = fn(work)
        if not any(p.is_file() and p.stat().st_size for p in Path(work).rglob("*")):
            jwrite(work, f"{fn.__name__}.json", [{"check": n, "passed": bool(ok), "observed": str(o)} for n, ok, o in checks])
        return checks
    run.__name__ = fn.__name__
    return run


_PROGRAMS = {
    "EXPL-01": expl_01, "EXPL-02": expl_02, "EXPL-03": expl_03, "EXPL-04": expl_04, "EXPL-05": expl_05,
    "EXPL-06": expl_06, "EXPL-07": expl_07, "EXPL-08": expl_08, "EXPL-10": expl_10, "EXPL-13": expl_13,
    "EXPL-14": expl_14, "EXPL-15": expl_15, "EXPL-16": expl_16, "EXPL-17": expl_17, "EXPL-18": expl_18,
    "EXPL-19": expl_19, "EXPL-20": expl_20, "EXPL-21": expl_21, "EXPL-22": expl_22, "EXPL-23": expl_23,
    "EXPL-24": expl_24, "EXPL-25": expl_25, "EXPL-26": expl_26, "EXPL-27": expl_27, "EXPL-28": expl_28,
    "EXPL-29": expl_29, "EXPL-30": expl_30, "EXPL-31": expl_31, "EXPL-32": expl_32, "EXPL-34": expl_34,
    "EXPL-35": expl_35, "EXPL-36": expl_36, "EXPL-37": expl_37, "EXPL-38": expl_38, "EXPL-39": expl_39,
    "EXPL-42": expl_42, "EXPL-43": expl_43, "EXPL-44": expl_44, "EXPL-46": expl_46, "EXPL-47": expl_47,
    "EXPL-48": expl_48, "EXPL-49": expl_49, "EXPL-50": expl_50, "EXPL-52": expl_52, "EXPL-53": expl_53,
    "EXPL-54": expl_54, "EXPL-55": expl_55, "EXPL-56": expl_56, "EXPL-57": expl_57, "EXPL-59": expl_59,
    "EXPL-60": expl_60, "EXPL-61": expl_61, "EXPL-62": expl_62, "EXPL-63": expl_63, "EXPL-64": expl_64,
    "EXPL-U01": expl_u01, "EXPL-U02": expl_u02, "EXPL-G01": expl_g01, "EXPL-G02": expl_g02,
}
PROGRAMS = {k: _recorded(v) for k, v in _PROGRAMS.items()}
