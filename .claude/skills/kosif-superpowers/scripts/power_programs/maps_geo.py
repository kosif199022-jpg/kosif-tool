"""Real programs for the maps-geo power cards.

Geodesy (haversine, great circles, projections), cartographic rules (normalisation, classing,
sqrt symbol sizing, label anchors), path preparation and globe maths run as deterministic numpy /
shapely procedures on fixtures with known answers. Cards that need MapLibre/Cesium in a browser,
API keys, network data (Overture, Overpass, tiles) or uninstalled CLIs (tippecanoe, duckdb) are skipped.
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from .photo_video_footage import REPO, chk, jwrite, near

R_EARTH = 6371.0088


def haversine(a, b):
    lon1, lat1, lon2, lat2 = map(math.radians, (*a, *b))
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return 2 * R_EARTH * math.asin(math.sqrt(h))


def to_vec(lonlat):
    lon, lat = map(math.radians, lonlat)
    return np.array([math.cos(lat) * math.cos(lon), math.cos(lat) * math.sin(lon), math.sin(lat)])


def to_lonlat(v):
    v = v / np.linalg.norm(v)
    return (math.degrees(math.atan2(v[1], v[0])), math.degrees(math.asin(v[2])))


def great_circle(a, b, n=100):
    va, vb = to_vec(a), to_vec(b)
    om = math.acos(np.clip(va @ vb, -1, 1))
    return [to_lonlat((math.sin((1 - t) * om) * va + math.sin(t * om) * vb) / math.sin(om)) for t in np.linspace(0, 1, n)]


def line_len(pts):
    return sum(haversine(pts[i], pts[i + 1]) for i in range(len(pts) - 1))


def slice_along(pts, d):
    out, acc = [pts[0]], 0.0
    for p, q in zip(pts, pts[1:]):
        s = haversine(p, q)
        if acc + s >= d:
            u = (d - acc) / s if s else 0
            out.append((p[0] + (q[0] - p[0]) * u, p[1] + (q[1] - p[1]) * u))
            return out
        out.append(q)
        acc += s
    return out


def ortho(lonlat, lon0, lat0):
    lon, lat = map(math.radians, lonlat)
    l0, p0 = math.radians(lon0), math.radians(lat0)
    x = math.cos(lat) * math.sin(lon - l0)
    y = math.cos(p0) * math.sin(lat) - math.sin(p0) * math.cos(lat) * math.cos(lon - l0)
    z = math.sin(p0) * math.sin(lat) + math.cos(p0) * math.cos(lat) * math.cos(lon - l0)
    return x, y, z


MECCA, CAIRO, CASA, RIYADH = (39.83, 21.42), (31.24, 30.04), (-7.59, 33.57), (46.72, 24.69)


def map_01(work):
    def choose(story):
        if story["spatial"] in ("distance", "neighbours", "routes", "clustering"):
            return {"chart": "map", "inset": None}
        return {"chart": "sorted bar", "inset": 0.15}

    a = choose({"spatial": "ranking"})
    b = choose({"spatial": "routes"})
    (work / "PLAN.md").write_text(f"chart: {a['chart']} (ranking across regions; locator inset {a['inset']:.0%})\n")
    return [chk("ranking -> sorted bar + ~15% locator inset", a == {"chart": "sorted bar", "inset": 0.15}, a),
            chk("routes -> a real map", b["chart"] == "map", b),
            chk("choice and reason written to PLAN.md", "ranking" in (work / "PLAN.md").read_text(), "PLAN.md")]


def map_02(work):
    table = {"driving": "road", "delivery": "road", "traffic": "road", "hiking": "topo", "flood": "topo", "wildfire": "topo",
             "regional comparison": "admin", "damage": "imagery", "land use": "imagery", "dense events": "neutral",
             "whole planet": "globe"}
    jwrite(work, "substrates.json", table)
    return [chk("6 substrates cover the purposes", set(table.values()) == {"road", "topo", "admin", "imagery", "neutral", "globe"},
                sorted(set(table.values()))),
            chk("flood -> topo, damage -> imagery", table["flood"] == "topo" and table["damage"] == "imagery", "ok")]


def map_03(work):
    def family(data):
        return {"area_rate": "choropleth", "point_magnitude": "proportional symbol", "dense_points": "cluster/heat",
                "movement": "flow", "noisy_small_areas": "hex grid", "continuous": "raster"}[data]

    vals = [100, 25]
    r = [math.sqrt(v) for v in vals]
    area_ratio = (r[0] / r[1]) ** 2
    jwrite(work, "families.json", {k: family(k) for k in ("area_rate", "point_magnitude", "movement")})
    return [chk("point magnitude -> proportional symbols", family("point_magnitude") == "proportional symbol", "symbols"),
            chk("r = sqrt(v): 4x value -> 4x area, 2x radius", area_ratio == 4 and r[0] / r[1] == 2, (r, area_ratio)),
            chk("noisy small areas -> hex grid", family("noisy_small_areas") == "hex grid", "hex")]


def map_04(work):
    def merc_scale(lat):
        return 1 / math.cos(math.radians(lat))

    def equal_earth(lon, lat):
        A1, A2, A3, A4 = 1.340264, -0.081106, 0.000893, 0.003796
        th = math.asin(math.sqrt(3) / 2 * math.sin(math.radians(lat)))
        lam = math.radians(lon)
        x = 2 * math.sqrt(3) * lam * math.cos(th) / (3 * (9 * A4 * th ** 8 + 7 * A3 * th ** 6 + 3 * A2 * th ** 2 + A1))
        y = A4 * th ** 9 + A3 * th ** 7 + A2 * th ** 3 + A1 * th
        return x, y

    def cell_area(proj, lon, lat, d=1.0):
        p = [proj(lon, lat), proj(lon + d, lat), proj(lon + d, lat + d), proj(lon, lat + d)]
        return 0.5 * abs(sum(p[i][0] * p[(i + 1) % 4][1] - p[(i + 1) % 4][0] * p[i][1] for i in range(4)))

    def sphere_area(lat, d=1.0):
        return math.radians(d) * (math.sin(math.radians(lat + d)) - math.sin(math.radians(lat)))

    ee = [cell_area(equal_earth, 0, la) / sphere_area(la) for la in (0, 30, 60, 75)]
    merc_greenland = merc_scale(72) ** 2 / merc_scale(0) ** 2
    jwrite(work, "projections.json", {"equal_earth_area_ratio": ee, "mercator_area_inflation_72N": merc_greenland})
    return [chk("Equal Earth keeps area (ratio constant within 0.5%)", max(ee) / min(ee) < 1.005, [round(x, 4) for x in ee]),
            chk("Mercator inflates 72N areas ~10x", 9 < merc_greenland < 11, round(merc_greenland, 2))]


def jenks_like_quantiles(vals, k):
    return list(np.quantile(vals, np.linspace(0, 1, k + 1)))


def map_05(work):
    regions = {"A": (900, 1_000_000), "B": (300, 100_000), "C": (500, 2_000_000), "D": (150, 40_000), "E": (60, 50_000),
               "F": (2000, 10_000_000)}
    rate = {k: c / p * 100_000 for k, (c, p) in regions.items()}
    raw_top = max(regions, key=lambda k: regions[k][0])
    rate_top = max(rate, key=rate.get)
    k = 5
    br = jenks_like_quantiles(list(rate.values()), k)
    cls = {r: min(k - 1, int(np.searchsorted(br[1:-1], v, side="right"))) for r, v in rate.items()}
    blues = ["#eff3ff", "#bdd7e7", "#6baed6", "#3182bd", "#08519c"]
    legend = {"title": "cases per 100,000", "classes": [f"{br[i]:.0f}-{br[i + 1]:.0f}" for i in range(k)]}
    jwrite(work, "choropleth.json", {"rate": rate, "class": cls, "legend": legend})
    return [chk("raw count leader differs from rate leader", raw_top == "F" and rate_top == "D", (raw_top, rate_top)),
            chk("D = 150/40,000 = 375 per 100k", near(rate["D"], 375, 1e-9), rate["D"]),
            chk("5 sequential classes; top class holds the top rate", len(legend["classes"]) == 5 and cls["D"] == 4, cls),
            chk("legend has units", "per 100,000" in legend["title"], legend["title"])]


def map_06(work):
    pts = [(10 + 0.1 * i, 10) for i in range(5)] + [(50 + 0.1 * i, 50) for i in range(20)]

    def groups(points, r=2.0):
        out = []
        for p in points:
            for g in out:
                if math.dist(g[0], p) < r:
                    g.append(p)
                    break
            else:
                out.append([p])
        return out

    def strategy(g):
        return "spiderfy" if len(g) <= 8 else f"cluster badge {len(g)}"

    def spiderfy(g, rad=12):
        c = np.mean(g, 0)
        return [tuple(c + rad * np.array([math.cos(2 * math.pi * k / len(g)), math.sin(2 * math.pi * k / len(g))])) for k in range(len(g))]

    gs = groups(pts)
    st = [strategy(g) for g in gs]
    sp = spiderfy(gs[0])
    sizes = [30, 5, 18]
    draw_order = sorted(range(3), key=lambda i: -sizes[i])
    jwrite(work, "overlap.json", {"strategies": st})
    return [chk("5 overlapping -> spiderfy, 20 -> cluster badge", st == ["spiderfy", "cluster badge 20"], st),
            chk("spiderfied points no longer overlap", min(math.dist(a, b) for i, a in enumerate(sp) for b in sp[i + 1:]) > 2, "spread"),
            chk("smaller symbols drawn above larger", [sizes[i] for i in draw_order] == [30, 18, 5], draw_order)]


def map_07(work):
    def render(zoom):
        poly_width = 100 * zoom
        label_px = 28
        stroke = 2
        density = "country" if zoom < 2 else "region" if zoom < 4 else "city"
        return {"poly": poly_width, "label": label_px, "stroke": stroke, "labels": density}

    a, b = render(1), render(3)
    svg = '<path d="M0 0 L10 0" vector-effect="non-scaling-stroke" stroke-width="2"/>'
    (work / "layer.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg">{svg}</svg>')
    steps = [render(z)["labels"] for z in (1, 1.5, 2.5, 3.9, 4.1)]
    return [chk("geography scales with zoom", b["poly"] == 3 * a["poly"], (a["poly"], b["poly"])),
            chk("labels and strokes stay screen-stable", a["label"] == b["label"] and a["stroke"] == b["stroke"], a["label"]),
            chk("label density changes in steps", steps == ["country", "country", "region", "region", "city"], steps),
            chk("non-scaling-stroke set", "non-scaling-stroke" in (work / "layer.svg").read_text(), "svg")]


def map_08(work):
    W, H = 1000, 600
    bounds = (-20, 60, 15, 40)  # lon0, lon1, lat0, lat1

    def proj(lon, lat):
        return ((lon - bounds[0]) / (bounds[1] - bounds[0]) * W, (bounds[3] - lat) / (bounds[3] - bounds[2]) * H)

    def inv(x, y):
        return (bounds[0] + x / W * (bounds[1] - bounds[0]), bounds[3] - y / H * (bounds[3] - bounds[2]))

    ledger = [{"layer": "cities", "source": "manual", "license": "CC0", "date": "2026-11-01", "crs": "EPSG:4326",
               "order": "[lng, lat]", "measured": True}]
    jwrite(work, "ledger.json", ledger)
    checks = {n: inv(*proj(*p)) for n, p in {"Mecca": MECCA, "Cairo": CAIRO, "Casablanca": CASA}.items()}
    swapped = proj(MECCA[1], MECCA[0])
    return [chk(">= 3 spot checks round-trip within 1e-9 deg", all(np.allclose(checks[n], p) for n, p in
                                                                    {"Mecca": MECCA, "Cairo": CAIRO, "Casablanca": CASA}.items()), checks),
            chk("Cairo -> Mecca great-circle ~1,282 km", near(haversine(CAIRO, MECCA), 1282, 15), round(haversine(CAIRO, MECCA), 1)),
            chk("[lat, lng] swap lands Mecca elsewhere (caught)", math.dist(swapped, proj(*MECCA)) > 100, swapped),
            chk("ledger rows carry source, license, date, CRS", all({"source", "license", "date", "crs"} <= set(r) for r in ledger), ledger)]


def map_09(work):
    style = {"measured": "solid", "estimated": "dashed", "schematic": "hatched"}

    def lint(layers, topic):
        errs = []
        for l in layers:
            if style[l["status"]] != l["style"]:
                errs.append(f"{l['id']}: {l['status']} must be {style[l['status']]}")
            if not l.get("date"):
                errs.append(f"{l['id']}: undated")
        if topic == "human harm" and any(l.get("particles") for l in layers):
            errs.append("no particle flows for human harm")
        return errs

    layers = [{"id": "camps", "status": "measured", "style": "solid", "date": "2026-10-01"},
              {"id": "flows", "status": "estimated", "style": "solid", "date": "", "particles": True}]
    e = lint(layers, "human harm")
    jwrite(work, "sensitive_lint.json", e)
    return [chk("estimated layer drawn solid caught", any("estimated must be dashed" in x for x in e), e),
            chk("undated state caught", any("undated" in x for x in e), e),
            chk("particle flow for displacement refused", "no particle flows for human harm" in e, e)]


def map_10(work):
    n = 8
    stagger = 0.06
    fills = [k * stagger for k in range(n)]
    L = 500

    def dashoffset(p):
        return L * (1 - p)

    def flyer(p, pts):
        return pts[min(len(pts) - 1, int(p * (len(pts) - 1)))]

    pts = [(i, 0) for i in range(101)]
    return [chk("country fills 40-80 ms apart", 0.04 <= fills[1] - fills[0] <= 0.08, fills[:3]),
            chk("arc drawn by dashoffset L -> 0", dashoffset(0) == L and dashoffset(1) == 0, dashoffset(0.5)),
            chk("flyer rides the drawn head", flyer(0.5, pts) == (50, 0), flyer(0.5, pts))]


def map_11(work):
    def engine(need):
        return {"location context": "static plate", "editorial vector": "d3-topojson", "real basemap": "maplibre",
                "3d buildings": "mapbox", "terrain flyover": "cesium"}[need]

    shots = [{"need": "location context"}, {"need": "editorial vector"}]
    plan = [dict(s, engine=engine(s["need"])) for s in shots]
    jwrite(work, "engines.json", plan)
    return [chk("one engine per shot", all(isinstance(p["engine"], str) for p in plan) and len(plan) == 2, plan),
            chk("context only -> static plate (most deterministic)", plan[0]["engine"] == "static plate", plan[0]),
            chk("terrain -> cesium", engine("terrain flyover") == "cesium", "cesium")]


def map_12(work):
    out = (192, 108)
    push = 1.08
    plate = Image.new("RGB", (int(math.ceil(out[0] * push)), int(math.ceil(out[1] * push))), (200, 210, 190))
    d = ImageDraw.Draw(plate)
    d.polygon([(40, 20), (150, 30), (160, 100), (30, 90)], fill=(150, 170, 140))
    plate.save(work / "plate.png")

    def frame(t, T=5.0):
        s = 1.0 + (push - 1.0) * min(t / T, 1)
        w, h = out[0] * push / s, out[1] * push / s
        cx, cy = plate.width / 2, plate.height / 2
        return plate.crop((round(cx - w / 2), round(cy - h / 2), round(cx + w / 2), round(cy + h / 2))).resize(out)

    f0, f1 = frame(0), frame(5)
    f1.save(work / "frame_end.png")
    return [chk("plate >= output at the push-in scale", plate.width >= out[0] * push and plate.height >= out[1] * push, plate.size),
            chk("exact output aspect", out[0] * 9 == out[1] * 16, out),
            chk("push-in 1.00 -> 1.08 changes framing", not np.array_equal(np.asarray(f0), np.asarray(f1)), "differs")]


def map_14(work):
    base = 6.0
    waypoints = [4.0, 5.0, 6.0]
    scales = [2 ** (z - base) for z in waypoints]
    plate = (3840, 2160)

    def transform(z, centre, plate_centre=(1920, 1080)):
        s = 2 ** (z - base)
        return s, (960 - centre[0] * s, 540 - centre[1] * s)

    s, (tx, ty) = transform(5.0, (2000, 1000))
    target_on_screen = (2000 * s + tx, 1000 * s + ty)
    return [chk("base zoom = largest waypoint zoom: every scale <= 1", max(scales) <= 1 and scales == [0.25, 0.5, 1.0], scales),
            chk("plate <= 4096 px", max(plate) <= 4096, plate),
            chk("translate keeps the target centre mid-frame", target_on_screen == (960, 540), target_on_screen)]


def map_22(work):
    style = {"layers": [{"id": "water", "type": "fill"}, {"id": "place-label", "type": "symbol"},
                        {"id": "road-label", "type": "symbol"}, {"id": "country border", "type": "line"},
                        {"id": "other border", "type": "line"}, {"id": "disputed border", "type": "line"}]}
    import re
    kept = [l for l in style["layers"] if l["type"] != "symbol" and not re.search(r"other border", l["id"], re.I)]
    jwrite(work, "decluttered.json", {"layers": kept})
    ids = [l["id"] for l in kept]
    return [chk("all symbol layers removed", not any(l["type"] == "symbol" for l in kept), ids),
            chk("inner borders removed, country + disputed kept", ids == ["water", "country border", "disputed border"], ids)]


def map_23(work):
    def source(kind):
        return "custom-geojson" if kind in ("proposed", "historical", "disputed", "sequenced") else "provider-paint-only"

    def layer_filter(props):
        return {k: v for k, v in props.items() if v is not None}

    got = {k: source(k) for k in ("context", "sequenced", "disputed")}
    f = layer_filter({"filter": None, "paint": {"line-color": "#f00"}})
    jwrite(work, "sources.json", got)
    return [chk("draw-on geometry baked as custom GeoJSON", got["sequenced"] == "custom-geojson", got),
            chk("context stays provider paint-only", got["context"] == "provider-paint-only", got),
            chk("absent optional props omitted (no filter: undefined)", "filter" not in f, f)]


def map_24(work):
    from shapely.geometry import LineString, mapping
    def choose(n_features, mb):
        if n_features <= 300 and mb <= 5:
            return "geojson"
        return "vector-tiles (EPSG:3857)"

    t = np.linspace(0, 20 * math.pi, 20000)
    line = LineString(np.column_stack([t, np.sin(t) + 0.001 * np.sin(57 * t)]))
    gj = json.dumps(mapping(line))
    mb = len(gj) / 1e6
    simp = line.simplify(0.01)
    gj2 = json.dumps(mapping(simp))
    (work / "line_simplified.geojson").write_text(gj2)
    return [chk("200 features, 1 MB -> GeoJSON", choose(200, 1) == "geojson", "geojson"),
            chk("50,000 features -> vector tiles", choose(50000, 40).startswith("vector-tiles"), "mvt"),
            chk("simplify a heavy line, shape kept within tolerance", len(gj2) < 0.2 * len(gj) and line.hausdorff_distance(simp) <= 0.011,
                (round(mb, 3), len(gj2), round(line.hausdorff_distance(simp), 4)))]


def map_28(work):
    import heapq
    # braided river: two channels between bars, main chain must go source->mouth without bouncing
    nodes = {"S": (0, 0), "a": (1, 0.3), "b": (1, -0.3), "c": (2, 0.25), "d": (2, -0.25), "e": (2.2, 0.0), "M": (3, 0)}
    edges = [("S", "a"), ("S", "b"), ("a", "c"), ("b", "d"), ("c", "e"), ("d", "e"), ("e", "M"), ("a", "b"), ("c", "d")]
    adj = {n: [] for n in nodes}
    for u, v in edges:
        w = math.dist(nodes[u], nodes[v])
        adj[u].append((v, w))
        adj[v].append((u, w))

    def dijkstra(s, t):
        pq, dist, prev = [(0, s)], {s: 0}, {}
        while pq:
            d, u = heapq.heappop(pq)
            if u == t:
                break
            for v, w in adj[u]:
                if d + w < dist.get(v, 1e9):
                    dist[v], prev[v] = d + w, u
                    heapq.heappush(pq, (d + w, v))
        path = [t]
        while path[-1] != s:
            path.append(prev[path[-1]])
        return path[::-1], dist[t]

    def greedy(s, t):
        path, cur, seen = [s], s, {s}
        while cur != t and len(path) < 20:
            nxt = min((v for v, _ in adj[cur] if v not in seen), key=lambda v: math.dist(nodes[cur], nodes[v]), default=None)
            if nxt is None:
                break
            path.append(nxt)
            seen.add(nxt)
            cur = nxt
        return path

    sp, d = dijkstra("S", "M")
    gr = greedy("S", "M")
    monotone = all(nodes[sp[i + 1]][0] >= nodes[sp[i]][0] for i in range(len(sp) - 1))
    jwrite(work, "river_path.json", {"shortest": sp, "greedy": gr})
    return [chk("shortest path goes source -> mouth monotonically", monotone and sp[0] == "S" and sp[-1] == "M", sp),
            chk("greedy nearest-endpoint chaining bounces between channels", any(
                abs(nodes[gr[i + 1]][0] - nodes[gr[i]][0]) < 1e-9 for i in range(len(gr) - 1)), gr)]


def corridor(pts, step=0.1, smooth_km=2.8, passes=2, damp=0.45):
    pts = np.asarray(pts, float)
    seg = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    cum = np.concatenate([[0], np.cumsum(seg)])
    s = np.arange(0, cum[-1], step)
    res = np.column_stack([np.interp(s, cum, pts[:, 0]), np.interp(s, cum, pts[:, 1])])
    k = int(round(smooth_km / step))
    out = res.copy()
    for _ in range(passes):
        pad = np.pad(out, ((k, k), (0, 0)), mode="edge")
        ker = np.ones(2 * k + 1) / (2 * k + 1)
        out = np.column_stack([np.convolve(pad[:, i], ker, mode="valid") for i in range(2)])
    a, b = out[0], out[-1]
    chord = a + np.outer(np.linspace(0, 1, len(out)), b - a)
    return res, chord + (out - chord) * (1 - damp)


def map_29(work):
    rng = np.random.default_rng(3)
    x = np.linspace(0, 40, 400)
    y = 3 * np.sin(x / 6) + rng.normal(0, 0.4, len(x))
    raw = np.column_stack([x, y])
    res, cor = corridor(raw)
    head = lambda p: np.degrees(np.arctan2(np.diff(p[:, 1]), np.diff(p[:, 0])))
    dh_raw, dh_cor = np.abs(np.diff(head(res))).max(), np.abs(np.diff(head(cor))).max()
    spacing = np.linalg.norm(np.diff(res, axis=0), axis=1)
    np.save(work / "corridor.npy", cor)
    return [chk("resampled every 0.1 km of arc (chords <= 0.1, median 0.1)", spacing.max() <= 0.1 + 1e-9 and near(float(np.median(spacing)), 0.1, 0.005), round(float(np.median(spacing)), 4)),
            chk("heading deltas change gradually after smoothing", dh_cor < 0.1 * dh_raw and dh_cor < 2, (round(dh_raw, 1), round(dh_cor, 3))),
            chk("DAMP 0.45 pulls deviation toward the chord", np.abs(cor[:, 1] - np.linspace(cor[0, 1], cor[-1, 1], len(cor))).max()
                < np.abs(res[:, 1]).max(), "damped")]


def pole_of_inaccessibility(poly, grid=46):
    from shapely.geometry import Point
    minx, miny, maxx, maxy = poly.bounds
    best = None
    for x in np.linspace(minx, maxx, grid):
        for y in np.linspace(miny, maxy, grid):
            p = Point(x, y)
            if poly.contains(p):
                d = poly.exterior.distance(p)
                if best is None or d > best[0]:
                    best = (d, (x, y))
    return best


def map_30(work):
    from shapely.geometry import Polygon, Point
    # C-shaped country: centroid falls outside the land
    poly = Polygon([(0, 0), (10, 0), (10, 2), (2, 2), (2, 8), (10, 8), (10, 10), (0, 10)])
    c = poly.centroid
    d, p = pole_of_inaccessibility(poly)
    nudged = (p[0] + 0, p[1] + 0.6)
    jwrite(work, "label_anchor.json", {"centroid": [c.x, c.y], "pole": p, "nudged": nudged})
    return [chk("centroid of the C-shape lies outside the polygon", not poly.contains(c), (round(c.x, 2), round(c.y, 2))),
            chk("46x46 grid pole lies inside, ~1 unit from every edge", poly.contains(Point(*p)) and d >= 0.95, (p, round(d, 3))),
            chk("operator nudge [0, 0.6] applied", near(nudged[1] - p[1], 0.6, 1e-12), nudged)]


def norm_ar(s):
    s = s.lower().strip()
    for a, b in (("أ", "ا"), ("إ", "ا"), ("آ", "ا"), ("ة", "ه"), ("ى", "ي")):
        s = s.replace(a, b)
    if s.startswith("ال"):
        s = s[2:]
    return " ".join(s.split())


def map_31(work):
    aliases = {"riyadh": ["الرياض", "riyadh", "ar riyad"], "medina": ["المدينة المنورة", "المدينه المنوره", "madinah", "medina"],
               "abha": ["أبها", "abha"], "jizan": ["جازان", "جيزان", "jazan", "jizan"]}
    index = {norm_ar(a): k for k, al in aliases.items() for a in al}
    queries = {"رياض": "riyadh", "  الرياض ": "riyadh", "ابها": "abha", "المدينة  المنورة": "medina", "RIYADH": "riyadh",
               "جيزان": "jizan", "تبوك": None}
    got = {q: index.get(norm_ar(q)) for q in queries}
    jwrite(work, "matches.json", got)
    return [chk(f"'{q.strip()}' -> {w}", got[q] == w, got[q]) for q, w in queries.items()]


def map_32(work):
    route = great_circle(RIYADH, CAIRO, 100)
    L = line_len(route)
    direct = haversine(RIYADH, CAIRO)

    def progress(f):
        if f < 0.2:
            return 0.0
        if f > 0.82:
            return 1.0
        p = (f - 0.2) / 0.62
        return 4 * p ** 3 if p < .5 else 1 - (-2 * p + 2) ** 3 / 2

    part = slice_along(route, max(0.001, L * progress(0.51)))
    jwrite(work, "route.geojson", {"type": "LineString", "coordinates": route})
    return [chk("100 points on the geodesic", len(route) == 100, len(route)),
            chk("polyline length equals the great-circle distance (~1,627 km)", near(L, direct, 0.5) and near(direct, 1627, 20),
                (round(L, 1), round(direct, 1))),
            chk("travel window 20% -> 82%, half drawn at its midpoint", progress(0.1) == 0 and progress(0.9) == 1 and
                near(line_len(part), L / 2, 2), round(line_len(part), 1)),
            chk("minimum slice 0.001 km at start", len(slice_along(route, 0.001)) == 2, "0.001")]


def map_33(work):
    pal = {"paper": "#EAD9B5", "edge": "#C9AA72", "sea": "#BFCDBE", "ink": "#3B2716", "route": "#9C2A1C", "gold": "#B8862B",
           "desk": "#24170E", "card": "#F4E9D0"}
    lines = ["مكة: ولد النبي", "المدينة: الهجرة", "بدر: المعركة", "أحد: المعركة", "الخندق: الحصار", "الحديبية: الصلح", "مكة: الفتح"]
    wps = 1.9
    durations = [len(l.replace(":", " ").split()) / wps for l in lines]
    from .photo_video_footage import contrast, hexrgb
    cr = contrast(hexrgb(pal["ink"]), hexrgb(pal["paper"]))
    jwrite(work, "journey.json", {"stops": lines, "seconds": durations})
    return [chk("7 stops, each 'place: what happened'", len(lines) == 7 and all(":" in l for l in lines), len(lines)),
            chk("read at 1.9 words/s", near(durations[0], 3 / 1.9, 1e-9), round(durations[0], 3)),
            chk("ink on paper readable (>= 7:1)", cr >= 7, round(cr, 2)),
            chk("route #9C2A1C", pal["route"] == "#9C2A1C", pal["route"])]


def map_34(work):
    K = 20.0

    def proj(lon, lat, latc=30.0):
        return ((lon + 18) * K * math.cos(math.radians(latc)), (47 - lat) * K)

    x0, y0 = proj(-18, 47)
    xm, ym = proj(MECCA[0], MECCA[1])
    x1, _ = proj(-17, 47)
    x2, _ = proj(-17, 47, latc=24)
    return [chk("origin lon -18 / lat 47 maps to (0,0)", (x0, y0) == (0.0, 0.0), (x0, y0)),
            chk("Mecca at ((39.83+18)*K*cos30, (47-21.42)*K)", near(xm, 57.83 * K * math.cos(math.radians(30)), 1e-9)
                and near(ym, 25.58 * K, 1e-9), (round(xm, 2), round(ym, 2))),
            chk("1 deg lon squashed by cos(30) = 0.866 K", near(x1, K * 0.8660254, 1e-6), x1),
            chk("Saudi centre latitude 24 gives cos(24)", near(x2 / K, math.cos(math.radians(24)), 1e-12), x2 / K)]


def catmull(pts, n=50):
    pts = np.asarray(pts, float)
    P = np.vstack([pts[0], pts, pts[-1]])
    out = []
    for i in range(1, len(P) - 2):
        for t in np.linspace(0, 1, n, endpoint=False):
            p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(pts[-1])
    return np.array(out)


def map_35(work):
    stops = [(0, 0), (100, 30), (200, 0), (300, 60), (400, 0), (500, 40), (600, 0)]
    path = catmull(stops)
    cum = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(path, axis=0), axis=1))])
    stop_len = [cum[np.argmin(np.linalg.norm(path - np.array(s), axis=1))] for s in stops]
    speed, dwell = 100.0, 0.5
    sched, t = [], 0.0
    for i, L in enumerate(stop_len):
        if i:
            t += (L - stop_len[i - 1]) / speed
        sched.append((t, t + dwell))
        t += dwell

    def length_at(tq):
        for i, (a, b) in enumerate(sched):
            if tq < a:
                prev_dep = sched[i - 1][1]
                return stop_len[i - 1] + (tq - prev_dep) * speed
            if tq <= b:
                return stop_len[i]
        return stop_len[-1]

    def head(tq):
        L = length_at(tq)
        k = np.searchsorted(cum, L)
        return path[min(k, len(path) - 1)]

    mid = (sched[1][1] + sched[2][0]) / 2
    jwrite(work, "schedule.json", sched)
    return [chk("7 stops with arrive/depart", len(sched) == 7, len(sched)),
            chk("head dwells at stop 3", np.allclose(head(sched[2][0] + 0.25), path[np.searchsorted(cum, stop_len[2])]), "dwell"),
            chk("constant arc-length speed between stops", near(length_at(mid) - length_at(mid - 0.2), 20, 1e-6),
                length_at(mid) - length_at(mid - 0.2)),
            chk("head reaches the last stop at the end of the schedule", np.allclose(head(sched[-1][1] + 1), path[-1]), "end")]


def map_36(work):
    def rot_x(t, T=4.0):
        p = min(t / T, 1)
        return 55 * (1 - (1 - p) ** 3)

    def billboard(angle):
        return -angle

    def project(y, angle, persp=1600):
        a = math.radians(angle)
        yz, z = y * math.cos(a), y * math.sin(a)
        return yz * persp / (persp + z)

    a = rot_x(4.0)
    top, bot = project(-400, a), project(400, a)
    return [chk("tilt 0 -> 55 deg (50-60) over the descent", rot_x(0) == 0 and near(a, 55, 1e-9), a),
            chk("sprites counter-rotate to stand upright", billboard(a) + a == 0, billboard(a)),
            chk("perspective foreshortens the far edge", abs(top) > abs(bot), (round(top, 1), round(bot, 1)))]


def map_37(work):
    mg45 = {"title": (0, 1), "stations": (1, 7), "overview": (7, 10)}
    st = [1 + k * 6 / 4 for k in range(4)]
    mg46 = {"map": (0, 1), "route": (1, 5), "summary": (5, 8)}

    def dash(approx):
        return "6 4" if approx else None

    return [chk("MG-045: 10 s, 4 stations evenly in 1-7 s", mg45["overview"][1] == 10 and st == [1.0, 2.5, 4.0, 5.5], st),
            chk("MG-046: 8 s, route 1-5 s", mg46["summary"][1] == 8 and mg46["route"] == (1, 5), mg46),
            chk("approximate path dashed, true route solid", dash(True) == "6 4" and dash(False) is None, "dash")]


def back_out(p, s=2.0):
    p -= 1
    return 1 + (s + 1) * p ** 3 + s * p ** 2


def map_38(work):
    pts = np.array([(0, 0), (300, 0), (300, 200), (600, 200)], float)
    cum = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))])
    L = cum[-1]
    stations = cum[1:]
    T = 3.0

    def drawn(t):
        return L * min(t / T, 1)

    def pop(i, t):
        t0 = T * stations[i] / L
        p = min(max((t - t0) / 0.25, 0), 1)
        return 0 if t < t0 else back_out(p)

    peak = max(pop(0, T * stations[0] / L + k * 0.25 / 100) for k in range(101))
    return [chk("3 s draw: full length at 3 s", drawn(3.0) == L, L),
            chk("station pops exactly when drawn >= its length", pop(0, T * stations[0] / L - 1e-6) == 0 and
                pop(0, T * stations[0] / L + 1e-3) > 0, round(T * stations[0] / L, 3)),
            chk("pop overshoots ~1.15 then settles at 1", 1.1 <= peak <= 1.2 and near(pop(0, 3.0), 1, 1e-9), round(peak, 3))]


def map_39(work):
    pts = np.array([(0, 400), (100, 300), (200, 320), (300, 150), (400, 100)], float)
    cum = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))])
    L = cum[-1]

    def avatar(p):
        s = L * p
        i = min(np.searchsorted(cum, s, side="right") - 1, len(pts) - 2)
        u = (s - cum[i]) / (cum[i + 1] - cum[i])
        pos = pts[i] + u * (pts[i + 1] - pts[i])
        d = pts[i + 1] - pts[i]
        return pos, math.degrees(math.atan2(d[1], d[0]))

    off = lambda p: L * (1 - p)
    pos, ang = avatar(0.5)
    return [chk("solid lime dashoffset = L(1-p)", off(0) == L and off(1) == 0, round(off(0.5), 2)),
            chk("avatar at getPointAtLength(L*p): path length to it = L/2", near(
                float(cum[np.searchsorted(cum, L / 2) - 1] + np.linalg.norm(pos - pts[np.searchsorted(cum, L / 2) - 1])), L / 2, 1e-9),
                pos.tolist()),
            chk("avatar rotated to the path tangent", ang == math.degrees(math.atan2(pts[3][1] - pts[2][1], pts[3][0] - pts[2][0]))
                or ang == math.degrees(math.atan2(pts[2][1] - pts[1][1], pts[2][0] - pts[1][0])), round(ang, 2)),
            chk("4:5 frame", 1080 * 5 == 1350 * 4, "1080x1350")]


def map_40(work):
    d = work / "doc"
    r = subprocess.run([sys.executable, str(REPO / "tools" / "kosif.py"), "scaffold", "documentary-map", str(d)],
                       capture_output=True, text=True, timeout=60, cwd=REPO)
    files = sorted(p.name for p in d.iterdir()) if d.is_dir() else []
    kb = lambda t: 1.0 + 0.06 * min(t / 5.0, 1)
    return [chk("scaffold writes STYLE.md, PLAN.md, TEST_REPORT.md, words.json",
                r.returncode == 0 and {"STYLE.md", "PLAN.md", "TEST_REPORT.md", "words.json"} <= set(files), files),
            chk("Ken Burns 1.00 -> 1.06 over 5 s", kb(0) == 1 and near(kb(5), 1.06, 1e-12), kb(2.5))]


def map_42(work):
    hub = np.array([0.0, 0.0, 0.0])
    cities = [np.array([200.0 * math.cos(a), 0.0, 200.0 * math.sin(a)]) for a in np.linspace(0, 2 * math.pi, 5, endpoint=False)]

    def curve(a, b, t):
        c = (a + b) / 2 + np.array([0, 90, 0])
        return (1 - t) ** 2 * a + 2 * (1 - t) * t * c + t * t * b

    def draw_range(i, k, index_count=80 * 6 * 6):
        return int(index_count * min(max(k * 1.4 - i * 0.08, 0), 1))

    apex = max(curve(hub, cities[0], t)[1] for t in np.linspace(0, 1, 101))
    return [chk("quadratic arc lifts 90 at the control point -> apex 45", near(apex, 45, 1e-9), apex),
            chk("arc ends at its city", np.allclose(curve(hub, cities[2], 1.0), cities[2]), "end"),
            chk("draw range clamp(k*1.4 - i*0.08) staggers the 5 arcs", [draw_range(i, 0.5) for i in range(5)] ==
                [int(2880 * min(max(0.7 - i * 0.08, 0), 1)) for i in range(5)] and draw_range(4, 1.0) == 2880,
                [draw_range(i, 0.5) for i in range(5)])]


def map_43(work):
    segs = 220

    def reveal(p, radial=8):
        return int(segs * p) * radial * 6

    def flow(t, speed=0.9):
        return (t * speed) % 1.0

    return [chk("reveal(p) sets draw range proportional to p", reveal(0.5) == 110 * 48 and reveal(1.0) == 220 * 48, reveal(0.5)),
            chk("flow offsets the normal map at .9/s, wrapping", near(flow(1.0), 0.9, 1e-12) and near(flow(2.0), 0.8, 1e-12), flow(2.0)),
            chk("flattened tube: radius 11 x .3 = 3.3 thick", near(11 * 0.3, 3.3, 1e-12), 3.3)]


def map_44(work):
    from shapely.geometry import LineString, Point, Polygon
    countries = {"A": Polygon([(0, 0), (4, 0), (4, 4), (0, 4)]), "B": Polygon([(4, 0), (8, 0), (8, 4), (4, 4)]),
                 "C": Polygon([(8, 0), (12, 0), (12, 4), (8, 4)])}
    river = LineString([(1, 2), (5, 2), (5, 3), (11, 3)])
    start, end = 0.3, 8.0

    def entry_fraction(poly):
        for s in np.linspace(0, river.length, 2001):
            if poly.contains(river.interpolate(s)) or poly.boundary.distance(river.interpolate(s)) < 1e-9 and s > 0:
                if poly.contains(river.interpolate(min(s + 1e-3, river.length))):
                    return s / river.length
        return None

    trig = {k: start + entry_fraction(p) * (end - start) for k, p in countries.items()}

    def fill(t, k):
        dt = t - trig[k] - 2.5
        if dt < 0:
            return 0.0
        p = min(dt / 1.0, 1)
        return 0.625 * min(p / 0.6, 1) if p < 0.6 else 0.625 + (0.5 - 0.625) * (p - 0.6) / 0.4

    fa = round((3 / 11), 4)
    return [chk("A triggers at the river start (0.3 s)", near(trig["A"], 0.3, 1e-9), trig),
            chk("B triggers where the river enters it (3/11 of length)", near(trig["B"], 0.3 + 3 / 11 * 7.7, 0.01), round(trig["B"], 3)),
            chk("fill overshoots to .625 then settles .5", near(max(fill(trig["A"] + 2.5 + x / 100, "A") for x in range(101)), .625, 1e-9)
                and near(fill(trig["A"] + 3.5, "A"), .5, 1e-9), fa),
            chk("border draw takes a constant 2.5 s before the fill", fill(trig["C"] + 2.4, "C") == 0, "2.5 s")]


def map_45(work):
    W, H = 1000, 820
    lon0, lon1, lat0, lat1 = 34.4, 56.2, 15.9, 32.6
    c = math.cos(math.radians(24))
    sx = W / ((lon1 - lon0) * c)
    sy = H / (lat1 - lat0)
    s = min(sx, sy)

    def project(lat, lon):
        return ((lon - lon0) * c * s, (lat1 - lat) * s)

    def bubble(v, vmax, level):
        k = {"region": 58, "city": 26}[level]
        return max(6, math.sqrt(v / vmax) * k)

    x, y = project(RIYADH[1], RIYADH[0])
    vals = {"Riyadh": 400, "Makkah": 100, "Jazan": 1}
    r = {k: bubble(v, 400, "region") for k, v in vals.items()}
    dist = lambda v: max(3.5, math.sqrt(v) * 9)
    return [chk("Riyadh projects inside the 1000x820 frame", 0 < x < W and 0 < y < H, (round(x, 1), round(y, 1))),
            chk("lon scaled by cos(24)", near(project(20, 45.4)[0] - project(20, 44.4)[0], c * s, 1e-9), c),
            chk("region bubbles r = max(6, sqrt(v/max)*58)", r == {"Riyadh": 58.0, "Makkah": 29.0, "Jazan": 6}, r),
            chk("district floor 3.5", dist(0.01) == 3.5, dist(0.01))]


def heat(v, vmax):
    steps = ["#cfe3fb", "#9cc5f5", "#5f9fea", "#2f77d6", "#0b4fb0"]
    if v <= 0:
        return "var(--sk-line)"
    return steps[min(max(math.ceil(v / vmax * 5), 1), 5) - 1]


def map_46(work):
    got = [heat(v, 100) for v in (0, 1, 20, 21, 60, 100)]
    from .photo_video_footage import rel_lum, hexrgb
    lums = [float(rel_lum(hexrgb(h))) for h in ["#cfe3fb", "#9cc5f5", "#5f9fea", "#2f77d6", "#0b4fb0"]]
    return [chk("ceil(v/max*5) classes", got == ["var(--sk-line)", "#cfe3fb", "#cfe3fb", "#9cc5f5", "#5f9fea", "#0b4fb0"], got),
            chk("single-hue ramp gets darker monotonically", all(a > b for a, b in zip(lums, lums[1:])), [round(l, 3) for l in lums])]


def map_48(work):
    vals = {"A": 900, "B": 100, "C": 400}
    rmax = 30
    r = {k: rmax * math.sqrt(v / max(vals.values())) for k, v in vals.items()}
    order = sorted(vals, key=lambda k: -r[k])

    def grow(t, dur=0.5):
        return back_out(min(t / dur, 1), 1.70158)

    return [chk("area proportional: r = sqrt(v)", r == {"A": 30.0, "B": 10.0, "C": 20.0}, r),
            chk("smaller bubbles drawn on top", order == ["A", "C", "B"], order),
            chk("grow 0 -> r with back-out overshoot", near(grow(0), 0, 1e-12) and near(grow(0.5), 1, 1e-9) and max(grow(x / 100) for x in range(51)) > 1,
                "back-out")]


def map_49(work):
    flows = [("A", "B", 100), ("A", "C", 25)]
    pos = {"A": np.array([0.0, 0.0]), "B": np.array([400.0, 0.0]), "C": np.array([0.0, 300.0])}

    def arc(a, b):
        mid = (a + b) / 2
        chord = b - a
        n = np.array([-chord[1], chord[0]]) / np.linalg.norm(chord)
        return a, mid + n * 0.2 * np.linalg.norm(chord), b

    p0, c, p1 = arc(pos["A"], pos["B"])
    apex = 0.5 * np.linalg.norm(c - (p0 + p1) / 2)
    width = {f"{a}{b}": 1 + 7 * v / 100 for a, b, v in flows}
    return [chk("control point lifted 20% of the chord", near(np.linalg.norm(c - (p0 + p1) / 2), 80, 1e-9), c.tolist()),
            chk("quadratic apex = half the lift", near(apex, 40, 1e-9), apex),
            chk("width proportional to volume", width == {"AB": 8.0, "AC": 2.75}, width)]


def map_50(work):
    grid = {"KW": (2, 0), "SA": (1, 1), "BH": (2, 1), "QA": (3, 1), "YE": (1, 2), "OM": (3, 2), "AE": (2, 2)}
    size = 30

    def hex_centre(q, r):
        return (size * math.sqrt(3) * (q + 0.5 * (r % 2)), size * 1.5 * r)

    centres = {k: hex_centre(*v) for k, v in grid.items()}
    dmin = min(math.dist(a, b) for i, a in enumerate(centres.values()) for b in list(centres.values())[i + 1:])
    vals = {"SA": 100, "AE": 60, "KW": 20, "QA": 15, "OM": 10, "BH": 5, "YE": 1}
    fills = {k: heat(v, 100) for k, v in vals.items()}
    stagger = {k: 0.05 * (q + r) for k, (q, r) in grid.items()}
    return [chk("every region one equal hexagon, none overlap", near(dmin, size * math.sqrt(3), 1e-9), round(dmin, 3)),
            chk("fill from the MAP-46 ramp", fills["SA"] == "#0b4fb0" and fills["YE"] == "#cfe3fb", fills),
            chk("diagonal reveal stagger", stagger["SA"] < stagger["AE"] < stagger["OM"], stagger)]


def map_52(work):
    def sizes(width):
        k = width / 1920
        return {"circle_r": 12 * k, "stroke": 4 * k, "text": 28 * k, "halo": 3 * k}

    fc = {"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": list(CAIRO)},
                                                     "properties": {"name": "Cairo"}}]}
    layers = [{"id": "dots", "type": "circle", "paint": {"circle-color": "#f03b20", "circle-radius": 12, "circle-stroke-width": 4,
                                                          "circle-stroke-color": "#fff"}},
              {"id": "names", "type": "symbol", "layout": {"text-field": ["get", "name"], "text-anchor": "top", "text-offset": [0, 0.9],
                                                           "text-size": 28, "text-allow-overlap": True},
               "paint": {"text-halo-width": 3, "text-halo-color": "#fff"}}]
    jwrite(work, "layers.json", {"source": fc, "layers": layers})
    return [chk("circle r12 stroke 4 #f03b20", layers[0]["paint"]["circle-radius"] == 12 and layers[0]["paint"]["circle-color"] == "#f03b20",
                layers[0]["paint"]),
            chk("x2 at 4K", sizes(3840) == {"circle_r": 24, "stroke": 8, "text": 56, "halo": 6}, sizes(3840)),
            chk("coordinates in [lng, lat]", fc["features"][0]["geometry"]["coordinates"] == [31.24, 30.04], "lnglat")]


def map_53(work):
    streets = 12
    st = [k * 0.045 for k in range(streets)]

    def pin_y(i, t, stagger=0.06, dur=0.4):
        p = min(max((t - i * stagger) / dur, 0), 1)
        if p < 1 / 2.75:
            b = 7.5625 * p * p
        elif p < 2 / 2.75:
            q = p - 1.5 / 2.75
            b = 7.5625 * q * q + .75
        elif p < 2.5 / 2.75:
            q = p - 2.25 / 2.75
            b = 7.5625 * q * q + .9375
        else:
            q = p - 2.625 / 2.75
            b = 7.5625 * q * q + .984375
        return -40 * (1 - b)

    def ring(t):
        p = min(t / 0.9, 1)
        return 1 + 1.4 * p, 0.6 * (1 - p)

    return [chk("streets 30-60 ms apart", 0.03 <= st[1] <= 0.06, st[1]),
            chk("pins drop -40 -> 0 px with bounce, 60 ms stagger", pin_y(0, 0) == -40 and near(pin_y(0, 0.4), 0, 1e-9)
                and pin_y(1, 0.06) == -40, pin_y(0, 0.2)),
            chk("pulse ring 1 -> 2.4 and .6 -> 0 over 900 ms", ring(0.9) == (2.4, 0.0) and ring(0) == (1, 0.6), ring(0.45))]


def map_54(work):
    rng = np.random.default_rng(5)
    cities = {"Riyadh": ((500, 300), 0.5), "Jeddah": ((200, 380), 0.3), "Dammam": ((700, 250), 0.2)}
    n = 800
    names = list(cities)
    assign = rng.choice(len(names), n, p=[cities[c][1] for c in names])
    ang = rng.uniform(0, 2 * math.pi, n)
    rad = rng.uniform(0, 1, n) ** 0.5 * rng.uniform(40, 80, n)
    target = np.array([cities[names[a]][0] for a in assign], float) + np.column_stack([np.cos(ang), np.sin(ang)]) * rad[:, None]
    start = rng.uniform(0, 1000, (n, 2))
    x, v = start.copy(), np.zeros_like(start)
    for _ in range(300):
        a = 120 * (target - x) - 22 * v
        v += a / 100
        x += v / 100
    counts = {c: int((assign == i).sum()) for i, c in enumerate(names)}
    dist = np.array([np.linalg.norm(x[i] - cities[names[assign[i]]][0]) for i in range(n)])
    return [chk("~800 dots assigned by weight", sum(counts.values()) == 800 and counts["Riyadh"] > counts["Jeddah"] > counts["Dammam"], counts),
            chk("springs settle onto their discs", np.abs(x - target).max() < 0.5, round(float(np.abs(x - target).max()), 4)),
            chk("clusters within 80 px of the city", dist.max() <= 80 + 0.5, round(float(dist.max()), 2))]


def map_55(work):
    W, H = 200, 100
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).ellipse([30, 20, 120, 80], fill=255)
    m = np.asarray(mask) > 0
    dots = [(x, y) for y in range(0, H, 8) for x in range(0, W, 8) if m[y, x]]
    pill = lambda t: back_out(min(t / 0.25, 1), 1.70158)
    im = Image.new("RGB", (W, H), "#f5f6fa")
    d = ImageDraw.Draw(im)
    for x, y in dots:
        d.ellipse([x - 2, y - 2, x + 2, y + 2], fill="#111318")
    im.save(work / "dots.png")
    return [chk("dots only on land (mask)", all(m[y, x] for x, y in dots) and len(dots) > 50, len(dots)),
            chk("grid gap 8 px", all(x % 8 == 0 and y % 8 == 0 for x, y in dots), "8 px"),
            chk("pill pops in 250 ms back-out", near(pill(0), 0, 1e-12) and near(pill(0.25), 1, 1e-9) and max(pill(t / 1000) for t in range(251)) > 1,
                "back-out")]


def map_56(work):
    rng = np.random.default_rng(9)
    n = 1534
    lon = rng.uniform(-180, 180, n)
    val = rng.gamma(2, 10, n)
    hmax = 120
    h = val / val.max() * hmax

    def grown(i, t, T=2.0):
        start = (lon[i] + 180) / 360 * T * 0.7
        return h[i] * min(max((t - start) / (T * 0.3), 0), 1)

    west, east = int(np.argmin(lon)), int(np.argmax(lon))
    return [chk("1534 points", n == 1534, n),
            chk("height proportional to value", near(h[np.argmax(val)], hmax, 1e-9) and near(h[0] / h[1], val[0] / val[1], 1e-9), "prop"),
            chk("sweep grows west before east", grown(west, 0.5) > 0 and grown(east, 0.5) == 0, (grown(west, .5), grown(east, .5)))]


def map_58(work):
    sun = np.array([1, 0.2, 0.5])
    sun /= np.linalg.norm(sun)

    def smoothstep(a, b, x):
        t = np.clip((x - a) / (b - a), 0, 1)
        return t * t * (3 - 2 * t)

    def shade(normal, view=np.array([0, 0, 1.0])):
        o = normal @ sun * 0.5 + 0.5
        dn = smoothstep(0.4, 0.6, o)
        lights = (1 - o) ** 2 * 1.5
        fres = (1 - abs(normal @ view)) ** 4 * 0.3
        return dn, lights, fres

    dn_day, l_day, _ = shade(sun)
    dn_night, l_night, _ = shade(-sun)
    _, _, f_rim = shade(np.array([1.0, 0, 0]))
    _, _, f_centre = shade(np.array([0, 0, 1.0]))
    cloud_uv = lambda t: (0.01 * t) % 1
    return [chk("sun-facing side is day (1), far side night (0)", dn_day == 1 and dn_night == 0, (dn_day, dn_night)),
            chk("city lights only at night: (1-o)^2*1.5", l_day == 0 and near(l_night, 1.5, 1e-12), (l_day, l_night)),
            chk("fresnel rim strongest at the limb (pow 4 x .3)", near(f_rim, 0.3, 1e-12) and f_centre == 0, (f_rim, f_centre)),
            chk("clouds drift .01 uv per second", near(cloud_uv(50), 0.5, 1e-12), cloud_uv(50))]


def map_59(work):
    rng = np.random.default_rng(11)
    nile = lambda z: 18 * math.sin(z / 95) + 9 * math.sin(z / 31)
    z = rng.uniform(0, 1200, 9000)
    river = np.column_stack([[nile(q) for q in z], z])
    a = rng.uniform(-0.75, 0.75, 11000)
    r = rng.uniform(0, 1, 11000) ** 0.7 * 230
    delta = np.column_stack([r * np.sin(a), 1200 + r * np.cos(a)])
    counts = {"river": 9000, "delta": 11000, "cairo": 2600, "alex": 1400, "towns": 1600}
    total = sum(counts.values())
    ang = np.arctan2(delta[:, 0], delta[:, 1] - 1200)
    return [chk("points follow x(z) = 18 sin(z/95) + 9 sin(z/31)", np.allclose(river[:, 0], [nile(q) for q in z]), "nile"),
            chk("delta fan within +-0.75 rad and 230 units", np.abs(ang).max() <= 0.75 + 1e-9 and r.max() <= 230, round(float(np.abs(ang).max()), 3)),
            chk("lit point groups total ~26k (9,000+11,000+2,600+1,400+1,600)", total == 25600 and len(river) + len(delta) == 20000, total)]


def map_60(work):
    land = [(lon, lat) for lon in range(-180, 180, 6) for lat in range(-60, 75, 6) if (lon - 20) ** 2 / 3000 + lat ** 2 / 900 < 1]

    def frame(t, speed=8):
        lon0 = speed * t
        out = []
        for p in land:
            x, y, z = ortho(p, lon0, 15)
            if z >= 0:
                out.append((x, y, 0.5 + 0.5 * z))
        return out

    f0 = frame(0)
    xs = [ortho(p, 0, 15) for p in land]
    back = [p for p, (x, y, z) in zip(land, xs) if z < 0]
    centre = ortho((0, 15), 0, 15)
    return [chk("back-facing dots culled (z < 0)", len(f0) == len(land) - len(back), (len(f0), len(back))),
            chk("projection centre maps to (0,0,1)", np.allclose(centre, (0, 0, 1)), centre),
            chk("8 deg/s: after 45 s the globe shows the same dots again", len(frame(45)) == len(f0) and len(frame(22.5)) != len(f0), (len(f0), len(frame(22.5)))),
            chk("dot size/alpha grows with depth", max(f0, key=lambda d: d[2])[2] <= 1 and min(f0, key=lambda d: d[2])[2] >= 0.5, "depth")]


def map_61(work):
    a, b = (-74.0, 40.7), (2.35, 48.86)
    steps = 64
    pts = great_circle(a, b, steps)
    lift = 0.15

    def lifted(i):
        u = i / (steps - 1)
        return 1 + lift * math.sin(math.pi * u)

    vis = [ortho(p, -30, 45)[2] >= 0 for p in pts]
    hidden = [ortho(p, 150, 0)[2] < 0 for p in pts]
    return [chk("64 slerp steps between the cities", len(pts) == 64 and np.allclose(pts[0], a) and np.allclose(pts[-1], b), len(pts)),
            chk("middle lifted 10-20% of r", near(max(lifted(i) for i in range(steps)), 1.15, 0.002), round(max(lifted(i) for i in range(steps)), 4)),
            chk("arc visible facing the camera, culled from behind", all(vis) and all(hidden), (sum(vis), sum(hidden)))]


def map_62(work):
    labels = [("Cairo", CAIRO), ("Riyadh", RIYADH), ("Casablanca", CASA), ("Mecca", MECCA)]
    speed = 0.15

    def visible(t):
        lon0 = math.degrees(speed * t)
        return [n for n, p in labels if ortho(p, lon0, 20)[2] > 0]

    pops = [k * 0.2 for k in range(len(labels))]
    v0 = visible(0)
    half = visible(math.pi / speed)
    return [chk("4-6 labels popping 200 ms apart", 4 <= len(labels) <= 6 and np.allclose(pops, [0, .2, .4, .6]), pops),
            chk("all front-facing at start", len(v0) == 4, v0),
            chk("after half a turn (0.15 rad/s) labels behind are hidden", half == [], half)]


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
    "MAP-01": map_01, "MAP-02": map_02, "MAP-03": map_03, "MAP-04": map_04, "MAP-05": map_05, "MAP-06": map_06,
    "MAP-07": map_07, "MAP-08": map_08, "MAP-09": map_09, "MAP-10": map_10, "MAP-11": map_11, "MAP-12": map_12,
    "MAP-14": map_14, "MAP-22": map_22, "MAP-23": map_23, "MAP-24": map_24, "MAP-28": map_28, "MAP-29": map_29,
    "MAP-30": map_30, "MAP-31": map_31, "MAP-32": map_32, "MAP-33": map_33, "MAP-34": map_34, "MAP-35": map_35,
    "MAP-36": map_36, "MAP-37": map_37, "MAP-38": map_38, "MAP-39": map_39, "MAP-40": map_40, "MAP-42": map_42,
    "MAP-43": map_43, "MAP-44": map_44, "MAP-45": map_45, "MAP-46": map_46, "MAP-48": map_48, "MAP-49": map_49,
    "MAP-50": map_50, "MAP-52": map_52, "MAP-53": map_53, "MAP-54": map_54, "MAP-55": map_55, "MAP-56": map_56,
    "MAP-58": map_58, "MAP-59": map_59, "MAP-60": map_60, "MAP-61": map_61, "MAP-62": map_62,
}
PROGRAMS = {k: _recorded(v) for k, v in _PROGRAMS.items()}
