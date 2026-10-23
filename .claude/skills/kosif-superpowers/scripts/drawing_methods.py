#!/usr/bin/env python3
"""KOSIF Drawing Methods Atlas: drawing-book method cards and layered SVG construction demos.

`list`, `find`, `show` and `plan` read data/drawing_methods_atlas.json (original summaries of methods
taught in drawing books; no book text or images). `prompt` turns chosen methods into an
image-generation prompt without calling any model. `draw head|figure|character|forms|bounce|shadow` writes a
deterministic, editable SVG whose groups are the method's stages (guide, construction, final,
silhouette), and `check` reads such an SVG back and measures it against the cards' checks. `review` is the
gate before delivery: every <g data-figure> must be one connected body and every data-contact must touch.

Pure stdlib; no network, no credits. Not model training and not proof of professional art quality.
"""
import argparse
import json
import math
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "data" / "drawing_methods_atlas.json"
BOOKS = ROOT / "data" / "creative_books_200_index.json"
SCHEMA = "kosif.drawing.methods_atlas.v1"
SVG_NS = "http://www.w3.org/2000/svg"
STAGES = ("guide", "construction", "final", "silhouette")
KIND_METHODS = {"head": ["DM-09", "DM-03", "DM-24"], "figure": ["DM-06", "DM-07", "DM-08", "DM-12"],
                "character": ["DM-13", "DM-14", "DM-15", "DM-16"], "forms": ["DM-03", "DM-04", "DM-19"],
                "bounce": ["DM-27", "DM-28"], "shadow": ["DM-32", "DM-19"]}
KIND_WORDS = {"head": ["head", "face", "portrait", "رأس", "وجه", "بورتريه", "ملامح"],
              "figure": ["figure", "pose", "body", "gesture", "جسم", "وضعية", "جسد", "حركة", "إيماءة"],
              "character": ["character", "cartoon", "mascot", "شخصية", "كرتون", "ماسكوت"],
              "forms": ["shape", "form", "sphere", "cylinder", "شكل", "أشكال", "كرة", "أسطوانة"],
              "bounce": ["animation", "animate", "bounce", "timing", "انيميشن", "تحريك", "رسوم متحركة", "تنط", "توقيت"],
              "shadow": ["cast shadow", "shadow construction", "ظل ساقط", "بناء الظل"]}


# ------------------------------------------------------------------ atlas

def load_atlas(path=ATLAS):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("schema") != SCHEMA:
        raise ValueError("unsupported atlas schema")
    ids = [m["id"] for m in data["methods"]]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate method id")
    known = set(ids)
    library = {b["id"] for b in data.get("user_library", [])}
    for m in data["methods"]:
        missing = [b for b in m["books"] if b.startswith("UBK-") and b not in library]
        if missing:
            raise ValueError(f"{m['id']} names books missing from user_library: {', '.join(missing)}")
    for stage in data["pipeline"]:
        for mid in stage["methods"]:
            if mid not in known:
                raise ValueError(f"pipeline stage {stage['stage']} names unknown method {mid}")
    return data


def book_ids(path=BOOKS):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return {b["id"] for lib in data["libraries"].values() for b in lib}


def norm(text):
    text = text.lower()
    for a, b in (("أ", "ا"), ("إ", "ا"), ("آ", "ا"), ("ة", "ه"), ("ى", "ي"), ("ـ", "")):
        text = text.replace(a, b)
    return re.sub(r"[ً-ْ]", "", text)


STOP = {"ارسم", "رسم", "ارسملي", "عايز", "عاوز", "اريد", "اعمل", "draw", "drawing", "make", "want", "the", "and"}


def words(text):
    return [w for w in re.findall(r"[\w؀-ۿ]+", norm(text)) if len(w) > 1 and w not in STOP]


def score(method, query):
    q = words(query)
    if not q:
        return 0
    tags = " ".join(norm(t) for t in method["tags"])
    name = norm(method["name_en"] + " " + method["name_ar"])
    body = norm(method["principle_en"] + " " + method["principle_ar"])
    tag_tokens = {t for t in words(tags) if len(t) >= 3}
    s = 0
    for w in q:
        stem = w[2:] if w.startswith("ال") and len(w) > 4 else w
        s += 3 * (stem in tags or any(t in stem for t in tag_tokens)) + 2 * (stem in name) + (stem in body)
    return s


def find(data, query, top=5):
    ranked = sorted(((score(m, query), m["id"]) for m in data["methods"]), key=lambda t: (-t[0], t[1]))
    by_id = {m["id"]: m for m in data["methods"]}
    return [{"id": i, "score": s, "name_en": by_id[i]["name_en"], "name_ar": by_id[i]["name_ar"],
             "domain": by_id[i]["domain"]} for s, i in ranked[:top] if s > 0]


def guess_kind(query):
    q = norm(query)
    hits = {k: sum(norm(w) in q for w in ws) for k, ws in KIND_WORDS.items()}
    best = max(hits, key=lambda k: (hits[k], k == "character"))
    return best if hits[best] else "character"


def plan(data, query, limit=4):
    kind = guess_kind(query)
    picked = [m["id"] for m in find(data, query, top=limit)]
    for mid in KIND_METHODS[kind]:
        if len(picked) >= limit:
            break
        if mid not in picked:
            picked.append(mid)
    by_id = {m["id"]: m for m in data["methods"]}
    stages = []
    for st in data["pipeline"]:
        use = [mid for mid in st["methods"] if mid in picked]
        if use or st["stage"] in ("intent", "verify"):
            stages.append({"stage": st["stage"], "ar": st["ar"], "en": st["en"],
                           "methods": [{"id": mid, "name_ar": by_id[mid]["name_ar"], "steps": by_id[mid]["steps"],
                                        "checks": by_id[mid]["checks"]} for mid in use]})
    return {"schema": "kosif.drawing.plan.v1", "request": query, "kind": kind, "methods": picked,
            "stages": stages,
            "demo_command": f"python3 scripts/drawing_methods.py draw {kind} --out out/{kind}.svg",
            "verify_command": f"python3 scripts/drawing_methods.py check --svg out/{kind}.svg",
            "status": "PLAN_ONLY_NOTHING_DRAWN"}


def prompt(data, subject, method_ids=None, style=""):
    by_id = {m["id"]: m for m in data["methods"]}
    ids = method_ids or [f["id"] for f in find(data, subject, top=3)] or KIND_METHODS[guess_kind(subject)][:3]
    unknown = [i for i in ids if i not in by_id]
    if unknown:
        raise ValueError("unknown method id(s): " + ", ".join(unknown))
    terms = []
    for i in ids:
        for t in by_id[i]["prompt_terms"]:
            if t not in terms:
                terms.append(t)
    parts = [subject.strip()] + ([style.strip()] if style.strip() else []) + terms
    checks = [c for i in ids for c in by_id[i]["checks"]]
    return {"schema": "kosif.drawing.prompt.v1", "prompt": ", ".join(parts),
            "negative": "extra fingers, broken anatomy, inconsistent light direction, muddy values, tangents, text artifacts",
            "methods": ids, "review_checks": checks,
            "note": "Prompt text only; no image model was called. Name methods, not living artists, and review the result against review_checks."}


# ------------------------------------------------------------------ svg helpers

def f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".") if isinstance(v, float) else str(v)


def el(tag, **attrs):
    parts = []
    for k, v in attrs.items():
        if v is None:
            continue
        k = k.rstrip("_").replace("__", ":").replace("_", "-")
        parts.append(f'{k}="{f(v) if isinstance(v, (int, float)) else v}"')
    return f"<{tag} {' '.join(parts)}/>"


def pts(points):
    return " ".join(f"{f(x)},{f(y)}" for x, y in points)


def svg_doc(kind, w, h, layers, attrs, title):
    head = [f'<svg xmlns="{SVG_NS}" width="{w}" height="{h}" viewBox="0 0 {w} {h}" data-kosif-kind="{kind}" '
            + " ".join(f'data-{k}="{v}"' for k, v in attrs.items()) + ">",
            f"<title>{title}</title>", el("rect", x=0, y=0, width=w, height=h, fill="#fbf8f1")]
    style = {"guide": 'opacity="0.55" fill="none" stroke="#7aa6c2" stroke-width="1.5"',
             "construction": 'opacity="0.7" fill="none" stroke="#c0623b" stroke-width="2"',
             "final": 'fill="none" stroke="#1d1b19" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"',
             "silhouette": 'fill="#111" stroke="none"'}
    body = []
    for name in STAGES:
        body.append(f'<g id="stage-{name}" {style[name]}>')
        body.extend(layers.get(name, []))
        body.append("</g>")
    return "\n".join(head + body + ["</svg>"]) + "\n"


def landmark(name, x, y, **extra):
    return el("circle", class_="lm", data_name=name, cx=round(x, 2), cy=round(y, 2), r=4,
              **{f"data_{k}": v for k, v in extra.items()})


def thumbnail(shapes, w, h, scale=0.16, margin=12):
    tx, ty = w - w * scale - margin, margin
    return [f'<g transform="translate({f(tx)},{f(ty)}) scale({scale})">',
            el("rect", x=0, y=0, width=w, height=h, fill="#fbf8f1", stroke="#999", stroke_width=6)] + shapes + ["</g>"]


# ------------------------------------------------------------------ head (DM-09)

def draw_head(yaw=30.0, pitch=0.0, size=600):
    if not -75 <= yaw <= 75 or not -40 <= pitch <= 40:
        raise ValueError("yaw must be in [-75, 75] and pitch in [-40, 40] degrees")
    R, cx, cy = size * 0.24, size / 2, size * 0.40
    ya, pa = math.radians(yaw), math.radians(pitch)

    def proj(x, y, z):
        x1, z1 = x * math.cos(ya) + z * math.sin(ya), -x * math.sin(ya) + z * math.cos(ya)
        y2, z2 = y * math.cos(pa) - z1 * math.sin(pa), y * math.sin(pa) + z1 * math.cos(pa)
        return cx + x1, cy + y2, z2

    def curve(points3d, front_only=True):
        """SVG path data; with front_only the hidden half is left out and each visible run is its own subpath."""
        runs, run = [], []
        for x, y, z in (proj(*p) for p in points3d):
            if z >= -1e-6 or not front_only:
                run.append((x, y))
            elif run:
                runs.append(run)
                run = []
        if run:
            if runs and front_only and runs[0][0] == run[-1]:
                runs[0] = run + runs[0][1:]
            else:
                runs.append(run)
        return " ".join("M" + " L".join(f"{f(round(x, 2))},{f(round(y, 2))}" for x, y in r) for r in runs if len(r) > 1)

    def ring(fn, n=72):
        return [fn(2 * math.pi * i / n) for i in range(n + 1)]

    d, r = 0.8 * R, 0.6 * R
    guide, cons, final = [], [], []
    guide.append(el("circle", cx=cx, cy=cy, r=R))
    guide.append(el("line", x1=cx - R * 1.4, y1=cy, x2=cx + R * 1.4, y2=cy, stroke_dasharray="6 6"))
    # side planes: circles of radius r in the planes x = +-d (only the one facing the viewer is drawn)
    for side in (1, -1):
        rim = ring(lambda t: (side * d, r * math.sin(t), r * math.cos(t)))
        nz = proj(side, 0, 0)[2] - proj(0, 0, 0)[2]
        if nz > 0.02:
            cons.append(el("path", d=curve(rim, False), data_part=f"side-plane-{'r' if side > 0 else 'l'}"))
    centre = ring(lambda t: (0.0, R * math.sin(t), R * math.cos(t)))
    brow = ring(lambda t: (R * math.sin(t), 0.0, R * math.cos(t)))
    cons.append(el("path", d=curve(centre), data_part="centre-line"))
    cons.append(el("path", d=curve(brow), data_part="brow-line"))
    u = r
    marks = {"hairline": (-u, math.sqrt(R * R - u * u)), "brow": (0.0, R), "nose": (u, 0.95 * R), "chin": (2 * u, 0.55 * R)}
    lms = []
    for name, (y3, z3) in marks.items():
        x, y, _ = proj(0.0, y3, z3)
        lms.append(landmark(name, x, y, y3d=round(y3 / R, 4)))
    top_y3, eye_y3 = -R, (-R + 2 * u) / 2
    for name, y3 in (("skull-top", top_y3), ("eye-line", eye_y3)):
        x, y, _ = proj(0.0, y3, math.sqrt(max(R * R - y3 * y3, 0)) if name == "eye-line" else 0.0)
        lms.append(landmark(name, x, y, y3d=round(y3 / R, 4)))
    cons.extend(lms)
    # jaw: ear root -> jaw angle -> chin, both sides
    for side in (1, -1):
        jaw = [(side * 0.78 * R, 0.45 * R, -0.12 * R), (side * 0.62 * R, 0.98 * R, 0.08 * R),
               (side * 0.2 * R, 1.18 * R, 0.5 * R), (0.0, 2 * u, 0.55 * R)]
        final.append(el("polyline", points=pts([proj(*p)[:2] for p in jaw]), data_part="jaw"))
    # cranium outline: the ball's rim from one ear root over the top to the other (t = 150..390 degrees)
    skull = [(R * math.cos(math.radians(t)), R * math.sin(math.radians(t)), 0.0) for t in range(150, 391, 5)]
    final.append(el("polyline", points=pts([proj(*p)[:2] for p in skull]), data_part="cranium"))
    for side in (1, -1):
        ex, ey, ez = proj(side * 0.36 * R, eye_y3, math.sqrt(R * R - (0.36 * R) ** 2 - eye_y3 ** 2))
        if ez > 0:
            squash = max(0.25, math.cos(math.radians(yaw)) if side * yaw > 0 else 1.0)
            final.append(el("ellipse", cx=round(ex, 2), cy=round(ey, 2), rx=round(0.14 * R * squash, 2),
                            ry=round(0.06 * R, 2), data_part="eye"))
        ax, ay, az = proj(side * d, 0.3 * R, -0.18 * R)
        if az > -0.35 * R:
            final.append(el("ellipse", cx=round(ax, 2), cy=round(ay, 2), rx=round(0.09 * R, 2), ry=round(0.2 * R, 2),
                            data_part="ear"))
    nose = [(-0.12 * R, u, 0.9 * R), (0.0, u + 0.03 * R, 1.02 * R), (0.12 * R, u, 0.9 * R)]
    final.append(el("polyline", points=pts([proj(*p)[:2] for p in nose]), data_part="nose"))
    mouth = [(x * R, 0.86 * R, 0.86 * R) for x in (-0.22, -0.08, 0.0, 0.08, 0.22)]
    final.append(el("polyline", points=pts([proj(*p)[:2] for p in mouth]), data_part="mouth"))
    sil = [el("circle", cx=cx, cy=cy, r=R), el("polygon", points=pts([proj(*p)[:2] for p in
           [(-0.78 * R, 0.4 * R, 0), (-0.62 * R, 0.98 * R, 0.08 * R), (0, 2 * u, 0.55 * R),
            (0.62 * R, 0.98 * R, 0.08 * R), (0.78 * R, 0.4 * R, 0)]]))]
    layers = {"guide": guide, "construction": cons, "final": final, "silhouette": thumbnail(sil, size, size)}
    return svg_doc("head", size, size, layers, {"yaw": f(float(yaw)), "pitch": f(float(pitch)), "methods": "DM-09 DM-03"},
                   "Ball-and-plane head construction"), {"yaw": yaw, "pitch": pitch}


# ------------------------------------------------------------------ figure (DM-06, DM-07, DM-08, DM-12)

POSES = {
    # lean (deg, + leans right), shoulder tilt, hip tilt, weight side (+1 viewer's right, 0 both), arm targets, foot offsets
    "stand": {"lean": 0, "sh": 0, "hip": 0, "weight": 0, "arms": ((-0.55, 0.0), (0.55, 0.0)), "feet": (-0.45, 0.45), "lift": (0, 0)},
    "contrapposto": {"lean": 0, "sh": -5, "hip": 7, "weight": 1, "arms": ((-0.6, 0.05), (0.75, -0.1)), "feet": (-0.9, 0.0), "lift": (0.25, 0)},
    "walk": {"lean": 4, "sh": -3, "hip": 3, "weight": 1, "arms": ((-0.2, -0.2), (0.9, 0.15)), "feet": (-1.1, 0.35), "lift": (0.45, 0)},
    "action": {"lean": 14, "sh": -12, "hip": 9, "weight": 1, "arms": ((-1.6, -2.4), (1.4, -0.4)), "feet": (-2.0, 0.6), "lift": (0.8, 0)},
}


def two_bone(root, target, l1, l2, bend):
    dx, dy = target[0] - root[0], target[1] - root[1]
    dist = max(1e-6, min(math.hypot(dx, dy), l1 + l2 - 1e-6))
    a = math.atan2(dy, dx)
    cos_b = max(-1.0, min(1.0, (l1 * l1 + dist * dist - l2 * l2) / (2 * l1 * dist)))
    ang = a + bend * math.acos(cos_b)
    mid = (root[0] + l1 * math.cos(ang), root[1] + l1 * math.sin(ang))
    tip_ang = math.atan2(target[1] - mid[1], target[0] - mid[0])
    return mid, (mid[0] + l2 * math.cos(tip_ang), mid[1] + l2 * math.sin(tip_ang))


def rot(cx, cy, x, y, deg):
    a = math.radians(deg)
    return cx + (x - cx) * math.cos(a) - (y - cy) * math.sin(a), cy + (x - cx) * math.sin(a) + (y - cy) * math.cos(a)


def taper(a, b, wa, wb):
    ang = math.atan2(b[1] - a[1], b[0] - a[0]) + math.pi / 2
    ox, oy = math.cos(ang), math.sin(ang)
    return [(a[0] + ox * wa, a[1] + oy * wa), (b[0] + ox * wb, b[1] + oy * wb),
            (b[0] - ox * wb, b[1] - oy * wb), (a[0] - ox * wa, a[1] - oy * wa)]


def draw_figure(heads=8.0, pose="contrapposto", width=600, height=1000):
    if not 2 <= heads <= 9:
        raise ValueError("heads must be between 2 and 9")
    if pose not in POSES:
        raise ValueError("pose must be one of " + ", ".join(POSES))
    p = POSES[pose]
    H, top, cx = height * 0.84, height * 0.07, width / 2
    h = H / heads
    rest = H - h
    unit = rest / 7.0                      # body below the chin in 8-head-canon units
    chin_y = top + h
    y = {k: chin_y + v * unit for k, v in {"shoulder": 0.33, "nipple": 1.0, "navel": 1.9, "crotch": 3.0,
                                            "knee": 5.0, "ankle": 6.75, "foot": 7.0}.items()}
    sh_w = h * (1.2 + 0.8 * (heads - 2) / 6)
    hip_w = 0.8 * sh_w
    s = p["weight"] or 1
    pelvis_x = cx + (0.3 * h * s if p["weight"] else 0)
    lean = math.tan(math.radians(p["lean"])) * (y["crotch"] - top)
    neck = (cx + lean * 0.5, chin_y + 0.15 * unit)
    head_c = (cx + lean * 0.6, top + h / 2)
    rib_c = (neck[0] - lean * 0.1, (y["shoulder"] + y["navel"]) / 2)
    pel_c = (pelvis_x, (y["navel"] + y["crotch"]) / 2 + 0.25 * unit)
    hips = [rot(pel_c[0], pel_c[1], pel_c[0] + sx * hip_w / 2, pel_c[1] + 0.2 * unit, p["hip"]) for sx in (-1, 1)]
    shoulders = [rot(rib_c[0], rib_c[1], rib_c[0] + sx * sh_w / 2, y["shoulder"], p["sh"]) for sx in (-1, 1)]
    thigh, shin = y["knee"] - y["crotch"] + 0.2 * unit, y["ankle"] - y["knee"]
    feet = []
    for i, off in enumerate(p["feet"]):
        support = p["weight"] and (i == 1)
        fx = neck[0] if support else hips[i][0] + off * h * 0.5
        feet.append((fx, y["ankle"] - (p["lift"][0] * unit if not support and p["weight"] else 0)))
    if not p["weight"]:
        feet = [(hips[0][0] + p["feet"][0] * h * 0.3, y["ankle"]), (hips[1][0] + p["feet"][1] * h * 0.3, y["ankle"])]
    upper, fore = 1.75 * unit, 1.1 * unit
    guide, cons, final, sil = [], [], [], []
    for k in range(int(math.floor(heads)) + 1):
        yy = top + k * h
        guide.append(el("line", x1=40, y1=round(yy, 2), x2=width - 40, y2=round(yy, 2), stroke_dasharray="4 8"))
        guide.append(f'<text x="14" y="{f(round(yy + 4, 2))}" font-size="14" fill="#7aa6c2" stroke="none">{k}</text>')
    support_foot = feet[1] if p["weight"] else ((feet[0][0] + feet[1][0]) / 2, feet[0][1])
    loa = f"M{f(round(head_c[0], 2))},{f(round(top, 2))} Q{f(round(rib_c[0] - lean * 0.6 - s * 0.25 * h * bool(p['weight']), 2))},{f(round(pel_c[1], 2))} {f(round(support_foot[0], 2))},{f(round(y['foot'], 2))}"
    cons.append(f'<path d="{loa}" stroke="#d1301f" stroke-width="3" data-part="line-of-action"/>')
    cons.append(el("ellipse", cx=round(head_c[0], 2), cy=round(head_c[1], 2), rx=round(h * 0.38, 2), ry=round(h * 0.5, 2), data_part="head"))
    rib_ry = (y["navel"] - y["shoulder"]) / 2
    cons.append(el("ellipse", cx=round(rib_c[0], 2), cy=round(rib_c[1], 2), rx=round(sh_w * 0.4, 2), ry=round(rib_ry, 2),
                   transform=f"rotate({f(float(p['sh']))} {f(round(rib_c[0], 2))} {f(round(rib_c[1], 2))})",
                   data_part="rib-cage", data_tilt=p["sh"]))
    pel_h = (y["crotch"] - y["navel"]) * 0.75
    cons.append(el("rect", x=round(pel_c[0] - hip_w / 2, 2), y=round(pel_c[1] - pel_h / 2, 2), width=round(hip_w, 2),
                   height=round(pel_h, 2), rx=round(h * 0.15, 2),
                   transform=f"rotate({f(float(p['hip']))} {f(round(pel_c[0], 2))} {f(round(pel_c[1], 2))})",
                   data_part="pelvis", data_tilt=p["hip"]))
    bean = f"M{f(round(rib_c[0] - sh_w * 0.3, 2))},{f(round(rib_c[1] + rib_ry * 0.6, 2))} Q{f(round((rib_c[0] + pel_c[0]) / 2 - sh_w * 0.25, 2))},{f(round(y['navel'], 2))} {f(round(pel_c[0] - hip_w * 0.42, 2))},{f(round(pel_c[1] - pel_h * 0.3, 2))} M{f(round(rib_c[0] + sh_w * 0.3, 2))},{f(round(rib_c[1] + rib_ry * 0.6, 2))} Q{f(round((rib_c[0] + pel_c[0]) / 2 + sh_w * 0.25, 2))},{f(round(y['navel'], 2))} {f(round(pel_c[0] + hip_w * 0.42, 2))},{f(round(pel_c[1] - pel_h * 0.3, 2))}"
    cons.append(f'<path d="{bean}" data-part="bean"/>')
    limbs = []
    for i in range(2):
        knee, ankle = two_bone(hips[i], feet[i], thigh, shin, bend=(1 if i == 0 else -1) * (1 if p["lean"] >= 0 else -1))
        limbs.append((hips[i], knee, ankle, h * 0.22, h * 0.16, h * 0.1))
        toe = (ankle[0] + (-1 if i == 0 else 1) * h * 0.25, y["foot"] - (feet[i][1] != y["ankle"]) * p["lift"][0] * unit)
        final.append(el("line", x1=round(ankle[0], 2), y1=round(ankle[1], 2), x2=round(toe[0], 2), y2=round(toe[1], 2), data_part="foot"))
        lms_name = f"foot-{'l' if i == 0 else 'r'}"
        cons.append(landmark(lms_name, ankle[0], max(ankle[1], toe[1]) + (y["foot"] - y["ankle"]) * 0.5, support=int(bool(p["weight"]) and i == 1)))
    for i in range(2):
        tx, ty = p["arms"][i]
        target = (shoulders[i][0] + tx * h * 0.6 + (-1 if i == 0 else 1) * 0.15 * h, y["crotch"] + ty * unit)
        elbow, wrist = two_bone(shoulders[i], target, upper, fore, bend=1 if i == 1 else -1)
        limbs.append((shoulders[i], elbow, wrist, h * 0.13, h * 0.1, h * 0.07))
        final.append(el("ellipse", cx=round(wrist[0], 2), cy=round(wrist[1] + 0.2 * h, 2), rx=round(0.1 * h, 2), ry=round(0.2 * h, 2), data_part="hand"))
    for a, b, c, wa, wb, wc in limbs:
        for j in (a, b, c):
            cons.append(el("circle", cx=round(j[0], 2), cy=round(j[1], 2), r=round(max(3.0, h * 0.06), 2), data_part="joint"))
        for seg in (taper(a, b, wa, wb), taper(b, c, wb, wc)):
            final.append(el("polygon", points=pts(seg), data_part="limb"))
            sil.append(el("polygon", points=pts(seg)))
    final.append(el("ellipse", cx=round(head_c[0], 2), cy=round(head_c[1], 2), rx=round(h * 0.38, 2), ry=round(h * 0.5, 2), data_part="head"))
    torso = [shoulders[0], shoulders[1], hips[1], hips[0]]
    final.append(el("polygon", points=pts(torso), data_part="torso"))
    sil += [el("ellipse", cx=round(head_c[0], 2), cy=round(head_c[1], 2), rx=round(h * 0.38, 2), ry=round(h * 0.5, 2)),
            el("polygon", points=pts(torso))]
    cons += [landmark("head-top", head_c[0], top), landmark("chin", head_c[0], chin_y), landmark("neck", neck[0], neck[1]),
             landmark("crotch", pel_c[0], y["crotch"])]
    layers = {"guide": guide, "construction": cons, "final": final, "silhouette": thumbnail(sil, width, height, 0.14)}
    attrs = {"heads": f(float(heads)), "pose": pose, "head-unit": f(round(h, 2)), "methods": "DM-06 DM-07 DM-08 DM-12"}
    return svg_doc("figure", width, height, layers, attrs, f"{f(float(heads))}-head mannequin, {pose}"), attrs


# ------------------------------------------------------------------ character (DM-13..DM-16)

AGES = {"child": (3.0, 0.56, 1.25), "teen": (4.5, 0.5, 1.0), "adult": (6.0, 0.46, 0.85), "elder": (5.5, 0.48, 0.8)}
EXPRESSIONS = {  # inner-brow rotation (deg, + = inner end up), brow lift, lid opening, mouth curve (+ smile), open mouth
    "neutral": (0, 0, 1.0, 0.0, False), "happy": (-4, -2, 0.7, 1.0, False), "sad": (16, 0, 0.8, -0.6, False),
    "angry": (-22, 4, 0.75, -0.3, False), "surprised": (0, -12, 1.35, 0.0, True)}
SECONDARY = {"circle": "square", "square": "circle", "triangle": "circle"}
PALETTE = {"circle": ("#f2b04a", "#5a8fd8"), "square": ("#5f7f52", "#d9a441"), "triangle": ("#6d3f8c", "#e0503a")}


def shape_el(shape, cx, cy, w, h, **kw):
    if shape == "circle":
        return el("ellipse", cx=round(cx, 2), cy=round(cy, 2), rx=round(w / 2, 2), ry=round(h / 2, 2), **kw), math.pi * w * h / 4
    if shape == "square":
        return el("rect", x=round(cx - w / 2, 2), y=round(cy - h / 2, 2), width=round(w, 2), height=round(h, 2),
                  rx=round(min(w, h) * 0.12, 2), **kw), w * h
    pts3 = [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx, cy + h / 2)]
    return el("polygon", points=pts(pts3), **kw), w * h / 2


def draw_character(shape="circle", age="child", expression="happy", width=600, height=900):
    if shape not in SECONDARY or age not in AGES or expression not in EXPRESSIONS:
        raise ValueError("shape: circle|square|triangle, age: " + "|".join(AGES) + ", expression: " + "|".join(EXPRESSIONS))
    heads, eye_frac, eye_scale = AGES[age]
    brow_rot, brow_lift, lid, curve, open_mouth = EXPRESSIONS[expression]
    main_c, accent = PALETTE[shape]
    H, top, cx = height * 0.8, height * 0.08, width / 2
    hh = H / heads
    hw = hh * (1.0 if shape != "square" else 0.95)
    body_h = H - hh - hh * 0.9
    body_w = hw * {"circle": 1.25, "square": 1.15, "triangle": 1.5}[shape]
    sec = SECONDARY[shape]
    guide, cons, final, sil = [], [], [], []
    guide.append(el("line", x1=cx, y1=top, x2=cx, y2=top + H, stroke_dasharray="6 6"))
    for k in range(int(heads) + 1):
        guide.append(el("line", x1=60, y1=round(top + k * hh, 2), x2=width - 60, y2=round(top + k * hh, 2), stroke_dasharray="3 9"))
    head_cy, body_cy = top + hh / 2, top + hh + body_h / 2
    head_shape = "circle" if shape == "triangle" and age == "child" else shape
    parts = []
    for name, shp, x, yy, w, h, fill in (("head", head_shape, cx, head_cy, hw, hh, "#f6d7b8"),
                                         ("body", shape, cx, body_cy, body_w, body_h, main_c)):
        node, area = shape_el(shp, x, yy, w, h, fill=fill, data_part=name, data_shape=shp)
        parts.append((name, shp, area))
        final.append(node)
        sil.append(shape_el(shp, x, yy, w, h)[0])
        cons.append(shape_el(shp, x, yy, w, h, data_part=name + "-mass")[0])
    leg_h = hh * 0.9
    for side in (-1, 1):
        fx = cx + side * body_w * 0.22
        final.append(el("line", x1=round(fx, 2), y1=round(top + hh + body_h - 4, 2), x2=round(fx, 2), y2=round(top + H - leg_h * 0.25, 2), data_part="leg"))
        node, area = shape_el(sec, fx + side * hh * 0.08, top + H - leg_h * 0.12, hh * 0.42, leg_h * 0.25, fill=accent, data_part="foot", data_shape=sec)
        final.append(node)
        sil.append(shape_el(sec, fx + side * hh * 0.08, top + H - leg_h * 0.12, hh * 0.42, leg_h * 0.25)[0])
        parts.append(("foot", sec, area))
        hx, hy = cx + side * (body_w / 2 + hh * 0.35), body_cy + body_h * 0.05
        final.append(el("line", x1=round(cx + side * body_w * 0.4, 2), y1=round(body_cy - body_h * 0.25, 2), x2=round(hx, 2), y2=round(hy, 2), data_part="arm"))
        node, area = shape_el(sec, hx, hy, hh * 0.24, hh * 0.24, fill=accent, data_part="hand", data_shape=sec)
        final.append(node)
        sil.append(shape_el(sec, hx, hy, hh * 0.24, hh * 0.24)[0])
        parts.append(("hand", sec, area))
    eye_y = top + hh * eye_frac
    eye_dx, er = hw * 0.2, hh * 0.085 * eye_scale
    cons.append(el("line", x1=round(cx - hw / 2, 2), y1=round(eye_y, 2), x2=round(cx + hw / 2, 2), y2=round(eye_y, 2), data_part="eye-line"))
    for side in (-1, 1):
        ex = cx + side * eye_dx
        final.append(el("ellipse", cx=round(ex, 2), cy=round(eye_y, 2), rx=round(er, 2), ry=round(er * lid, 2), fill="#fff", data_part="eye", data_emotion=expression))
        final.append(el("circle", cx=round(ex, 2), cy=round(eye_y, 2), r=round(er * 0.45, 2), fill="#1d1b19", data_part="pupil"))
        by = eye_y - er * 1.7 + brow_lift
        inner, outer = (ex - side * er, by), (ex + side * er * 1.1, by)
        ang = -side * brow_rot
        a, b = rot(ex, by, inner[0], inner[1], ang), rot(ex, by, outer[0], outer[1], ang)
        final.append(el("line", x1=round(a[0], 2), y1=round(a[1], 2), x2=round(b[0], 2), y2=round(b[1], 2), data_part="brow", data_emotion=expression))
    my, mw = top + hh * min(0.86, eye_frac + 0.27), hw * 0.22
    if open_mouth:
        final.append(el("ellipse", cx=round(cx, 2), cy=round(my, 2), rx=round(mw * 0.35, 2), ry=round(mw * 0.45, 2), fill="#7a2b22", data_part="mouth", data_emotion=expression))
    else:
        final.append(f'<path d="M{f(round(cx - mw, 2))},{f(round(my, 2))} Q{f(round(cx, 2))},{f(round(my + curve * mw * 0.6, 2))} {f(round(cx + mw, 2))},{f(round(my, 2))}" data-part="mouth" data-emotion="{expression}"/>')
    cons += [landmark("head-top", cx, top), landmark("chin", cx, top + hh), landmark("foot", cx, top + H), landmark("eye", cx, eye_y)]
    sizes = sorted({round(a) for _, _, a in parts}, reverse=True)
    attrs = {"shape": shape, "secondary": sec, "age": age, "heads": f(heads), "expression": expression,
             "palette": f"{main_c} {accent}", "methods": "DM-13 DM-14 DM-15 DM-16"}
    layers = {"guide": guide, "construction": cons, "final": final, "silhouette": thumbnail(sil, width, height, 0.14)}
    return svg_doc("character", width, height, layers, attrs, f"{shape} {age} character, {expression}"), dict(attrs, mass_sizes=len(sizes))


# ------------------------------------------------------------------ forms (DM-03, DM-04, DM-19)

def draw_forms(eye_level=0.45, width=900, height=600):
    if not 0.1 <= eye_level <= 0.9:
        raise ValueError("eye-level must be a fraction of the height between 0.1 and 0.9")
    ey, view = height * eye_level, height * 1.2
    guide = [el("line", x1=0, y1=round(ey, 2), x2=width, y2=round(ey, 2), stroke_dasharray="8 6", data_part="eye-level")]
    cons, final, sil = [], [], []
    defs = ['<defs><radialGradient id="lit" cx="0.35" cy="0.3" r="0.75"><stop offset="0" stop-color="#fff6e6"/>'
            '<stop offset="0.55" stop-color="#e6b98a"/><stop offset="0.56" stop-color="#7d5b4a"/><stop offset="0.9" stop-color="#5b4034"/>'
            '<stop offset="1" stop-color="#7a5a4c"/></radialGradient></defs>']
    sx, sy, sr = width * 0.2, height * 0.55, height * 0.15
    final += defs + [el("ellipse", cx=round(sx + sr * 0.5, 2), cy=round(sy + sr * 0.95, 2), rx=round(sr * 1.1, 2), ry=round(sr * 0.25, 2),
                         fill="#2b211c", opacity="0.55", stroke="none", data_part="cast-shadow"),
                      el("circle", cx=sx, cy=sy, r=sr, fill="url(#lit)", data_part="sphere")]
    cons.append(f'<path d="M{f(round(sx - sr * 0.55, 2))},{f(round(sy - sr * 0.84, 2))} A{f(sr)},{f(sr)} 0 0 0 {f(round(sx + sr * 0.84, 2))},{f(round(sy + sr * 0.55, 2))}" data-part="terminator"/>')
    sil.append(el("circle", cx=sx, cy=sy, r=sr))
    # cylinder: ellipses open wider the further they are from eye level (DM-04)
    cx_, rx, top, bot = width * 0.52, height * 0.12, height * 0.2, height * 0.8
    rings = []
    for yy in (top, (top + bot) / 2, bot):
        dist = yy - ey
        ry = rx * abs(math.sin(math.atan2(abs(dist), view)))
        rings.append(el("ellipse", cx=round(cx_, 2), cy=round(yy, 2), rx=round(rx, 2), ry=round(max(ry, 0.5), 2),
                        data_part="cylinder-ellipse", data_dist=round(dist, 2)))
    cons += rings
    final.append(el("line", x1=round(cx_ - rx, 2), y1=round(top, 2), x2=round(cx_ - rx, 2), y2=round(bot, 2), data_part="cylinder-side"))
    final.append(el("line", x1=round(cx_ + rx, 2), y1=round(top, 2), x2=round(cx_ + rx, 2), y2=round(bot, 2), data_part="cylinder-side"))
    final += [rings[0], rings[-1]]
    sil.append(el("rect", x=round(cx_ - rx, 2), y=round(top, 2), width=round(2 * rx, 2), height=round(bot - top, 2)))
    kx, kb, kt, kw = width * 0.82, height * 0.78, height * 0.25, height * 0.13
    kry = kw * abs(math.sin(math.atan2(abs(kb - ey), view)))
    final += [el("polyline", points=pts([(kx - kw, kb), (kx, kt), (kx + kw, kb)]), data_part="cone"),
              el("ellipse", cx=round(kx, 2), cy=round(kb, 2), rx=round(kw, 2), ry=round(kry, 2), data_part="cylinder-ellipse",
                 data_dist=round(kb - ey, 2))]
    sil.append(el("polygon", points=pts([(kx - kw, kb), (kx, kt), (kx + kw, kb)])))
    layers = {"guide": guide, "construction": cons, "final": final, "silhouette": thumbnail(sil, width, height, 0.14)}
    attrs = {"eye-level": f(round(ey, 2)), "methods": "DM-03 DM-04 DM-19", "light": "upper-left"}
    return svg_doc("forms", width, height, layers, attrs, "Sphere, cylinder and cone under one light"), attrs


# ------------------------------------------------------------------ bounce (DM-27, DM-28)

def draw_bounce(frames=13, height_frac=0.55, width=900, height=600):
    """One bounce, apex to apex, timed on even frames: gravity gives the slow-in/slow-out spacing (close drawings
    at the top, wide near the ground); stretch along the path near contact, squash on contact, constant area."""
    if frames % 2 == 0 or not 7 <= frames <= 25:
        raise ValueError("frames must be odd and between 7 and 25")
    if not 0.2 <= height_frac <= 0.8:
        raise ValueError("bounce-height must be a fraction of the height between 0.2 and 0.8")
    ground, r = height * 0.85, height * 0.045
    top = ground - r - height * height_frac
    mid, x0, x1 = frames // 2, width * 0.08, width * 0.92
    vx = (x1 - x0) / (frames - 1)
    fall = ground - r - top
    centres = []
    for i in range(frames):
        s = abs(i - mid) / mid                             # 0 on contact, 1 at either apex
        centres.append((x0 + vx * i, ground - r - fall * s * (2 - s)))   # height = H(1 - t^2), t = time from the apex
    guide = [el("line", x1=0, y1=round(ground, 2), x2=width, y2=round(ground, 2), data_part="ground"),
             el("polyline", points=pts([(round(x, 2), round(y, 2)) for x, y in centres]), stroke_dasharray="5 6",
                data_part="arc")]
    cons, final, sil = [], [], []
    for i, (x, y) in enumerate(centres):
        cons.append(el("line", x1=round(x, 2), y1=round(ground + 14, 2), x2=round(x, 2), y2=round(ground + 30, 2),
                       data_part="spacing-tick", data_frame=i))
        cons.append(f'<text x="{f(round(x - 4, 2))}" y="{f(round(ground + 46, 2))}" font-size="12" fill="#c0623b" stroke="none">{i}</text>')
    for i, (x, y) in enumerate(centres):
        contact = i == mid
        if contact:
            k = 1.45                                       # squash: wider and flatter, same area
            rx, ry, ang, cy = r * k, r / k, 0.0, ground - r / k
        else:
            near = 1 - abs(i - mid) / mid                  # 0 at the apex, ->1 next to the ground
            k = 1 + 0.5 * near ** 2                         # stretch grows with speed
            (ax, ay), (bx, by) = centres[max(i - 1, 0)], centres[min(i + 1, frames - 1)]
            ang = math.degrees(math.atan2(by - ay, bx - ax)) - 90   # long axis along the direction of travel
            rx, ry, cy = r / k, r * k, y
        final.append(el("ellipse", cx=round(x, 2), cy=round(cy, 2), rx=round(rx, 3), ry=round(ry, 3),
                        transform=f"rotate({f(round(ang, 2))} {f(round(x, 2))} {f(round(cy, 2))})" if ang else None,
                        data_part="ball", data_frame=i, data_contact=int(contact)))
        sil.append(el("ellipse", cx=round(x, 2), cy=round(cy, 2), rx=round(rx, 3), ry=round(ry, 3)))
    attrs = {"frames": frames, "radius": f(round(r, 3)), "ground": f(round(ground, 2)), "methods": "DM-27 DM-28"}
    layers = {"guide": guide, "construction": cons, "final": final, "silhouette": thumbnail(sil, width, height, 0.14)}
    return svg_doc("bounce", width, height, layers, attrs, "Bouncing ball: arc, spacing, squash and stretch"), attrs


# ------------------------------------------------------------------ cast shadow (DM-32)

def _meet(p1, p2, p3, p4):
    """Intersection of line p1-p2 with line p3-p4."""
    d = (p1[0] - p2[0]) * (p3[1] - p4[1]) - (p1[1] - p2[1]) * (p3[0] - p4[0])
    if abs(d) < 1e-9:
        raise ValueError("light and object edge are parallel; move the light")
    a, b = p1[0] * p2[1] - p1[1] * p2[0], p3[0] * p4[1] - p3[1] * p4[0]
    return ((a * (p3[0] - p4[0]) - (p1[0] - p2[0]) * b) / d, (a * (p3[1] - p4[1]) - (p1[1] - p2[1]) * b) / d)


def draw_shadow(light_x=0.15, light_h=0.4, width=900, height=600):
    """Point-light cast shadow built the way perspective courses teach it: the foot of the light on the ground is the
    shadow's vanishing point; each shadow corner is where the ray from that foot through a base point meets the ray
    from the light through the matching top point."""
    if not 0.05 <= light_x <= 0.95 or not 0.1 <= light_h <= 0.45:
        raise ValueError("light-x must be in [0.05, 0.95] and light-height in [0.1, 0.45] (fractions of the frame)")
    hz = height * 0.38
    foot = (width * light_x, height * 0.6)
    light = (foot[0], foot[1] - height * light_h)
    base = [(width * 0.44, height * 0.74), (width * 0.56, height * 0.77), (width * 0.62, height * 0.69), (width * 0.50, height * 0.67)]
    hgt = [height * 0.13 * (b[1] - hz) / (height * 0.84 - hz) * 1.25 for b in base]   # nearer corners stand taller
    tops = [(b[0], b[1] - hh) for b, hh in zip(base, hgt)]
    shadow_tops = []
    for b, t in zip(base, tops):
        s = _meet(foot, b, light, t)
        if (s[0] - foot[0]) * (b[0] - foot[0]) + (s[1] - foot[1]) * (b[1] - foot[1]) <= 0:
            raise ValueError("the light is not above the ground in front of the object; raise or move it")
        shadow_tops.append(s)
    pole_b, pole_t = (width * 0.32, height * 0.78), (width * 0.32, height * 0.6)
    pole_s = _meet(foot, pole_b, light, pole_t)
    guide = [el("line", x1=0, y1=round(hz, 2), x2=width, y2=round(hz, 2), stroke_dasharray="8 6", data_part="horizon"),
             el("line", x1=round(light[0], 2), y1=round(light[1], 2), x2=round(foot[0], 2), y2=round(foot[1], 2), data_part="light-drop")]
    cons, final = [], []
    for (b, t, s, name) in [*((b, t, s, f"corner-{i}") for i, (b, t, s) in enumerate(zip(base, tops, shadow_tops))),
                            (pole_b, pole_t, pole_s, "pole")]:
        cons.append(el("line", x1=round(foot[0], 2), y1=round(foot[1], 2), x2=round(s[0], 2), y2=round(s[1], 2), data_part="ground-ray"))
        cons.append(el("line", x1=round(light[0], 2), y1=round(light[1], 2), x2=round(s[0], 2), y2=round(s[1], 2), data_part="light-ray"))
        cons.append(el("circle", class_="sh", cx=round(s[0], 2), cy=round(s[1], 2), r=4, data_name=name,
                       data_base=f"{f(round(b[0], 2))},{f(round(b[1], 2))}", data_top=f"{f(round(t[0], 2))},{f(round(t[1], 2))}"))
    # shadow shape: convex hull of the base and the projected tops (the box sits on its own shadow)
    hull_pts = _hull(base + shadow_tops)
    final.append(el("polygon", points=pts([(round(x, 2), round(y, 2)) for x, y in hull_pts]), fill="#3a3a46", opacity="0.6",
                    stroke="none", data_part="cast-shadow"))
    final.append(el("polygon", points=pts([(round(pole_b[0] - 3, 2), round(pole_b[1], 2)), (round(pole_b[0] + 3, 2), round(pole_b[1], 2)),
                                           (round(pole_s[0], 2), round(pole_s[1], 2))]), fill="#3a3a46", opacity="0.6", stroke="none",
                    data_part="cast-shadow"))
    near = [0, 1, 2]
    final.append(el("polygon", points=pts([(round(x, 2), round(y, 2)) for x, y in tops]), fill="#f3e3c8", data_part="box-top"))
    for i, j in zip(near, near[1:]):
        final.append(el("polygon", points=pts([(round(p[0], 2), round(p[1], 2)) for p in (base[i], base[j], tops[j], tops[i])]),
                        fill="#c9a77f" if i == 0 else "#8e6f55", data_part="box-side"))
    final.append(el("line", x1=round(pole_b[0], 2), y1=round(pole_b[1], 2), x2=round(pole_t[0], 2), y2=round(pole_t[1], 2), data_part="pole"))
    final.append(el("circle", cx=round(light[0], 2), cy=round(light[1], 2), r=9, fill="#ffd25e", data_part="light"))
    sil = [el("polygon", points=pts(_hull(base + tops))), el("rect", x=round(pole_b[0] - 3, 2), y=round(pole_t[1], 2), width=6,
                                                           height=round(pole_b[1] - pole_t[1], 2))]
    attrs = {"light": f"{f(round(light[0], 2))},{f(round(light[1], 2))}", "light-foot": f"{f(round(foot[0], 2))},{f(round(foot[1], 2))}",
             "methods": "DM-32 DM-19"}
    layers = {"guide": guide, "construction": cons, "final": final, "silhouette": thumbnail(sil, width, height, 0.14)}
    return svg_doc("shadow", width, height, layers, attrs, "Cast shadow from a point light"), attrs


def _hull(points):
    p = sorted(set(points))
    if len(p) < 3:
        return p

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for q in p:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], q) <= 0:
            lower.pop()
        lower.append(q)
    for q in reversed(p):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], q) <= 0:
            upper.pop()
        upper.append(q)
    return lower[:-1] + upper[:-1]


# ------------------------------------------------------------------ check

def _q(tag):
    return f"{{{SVG_NS}}}{tag}"


def check_svg(path):
    root = ET.parse(path).getroot()
    kind = root.get("data-kosif-kind")
    res = {"schema": "kosif.drawing.check.v1", "file": str(path), "kind": kind, "checks": []}

    def add(cid, ok, observed, method):
        res["checks"].append({"id": cid, "pass": bool(ok), "observed": observed, "method": method})

    groups = {g.get("id"): g for g in root.iter(_q("g")) if g.get("id")}
    for st in STAGES:
        add(f"stage-{st}", f"stage-{st}" in groups and len(list(groups[f"stage-{st}"])) > 0,
            "present" if f"stage-{st}" in groups else "missing", "DM-03")
    lm = {c.get("data-name"): c for c in root.iter(_q("circle")) if c.get("class") == "lm"}

    def ly(name):
        return float(lm[name].get("cy")) if name in lm else None

    if kind == "head":
        y3 = {k: float(lm[k].get("data-y3d")) for k in ("hairline", "brow", "nose", "chin", "skull-top", "eye-line") if k in lm}
        if len(y3) == 6:
            thirds = [y3["brow"] - y3["hairline"], y3["nose"] - y3["brow"], y3["chin"] - y3["nose"]]
            spread = (max(thirds) - min(thirds)) / max(thirds)
            add("face-thirds", spread <= 0.10, {"thirds": [round(t, 3) for t in thirds], "spread": round(spread, 3)}, "DM-09")
            mid = (y3["skull-top"] + y3["chin"]) / 2
            add("eyes-half-height", abs(y3["eye-line"] - mid) <= 0.05, {"eye": y3["eye-line"], "half": round(mid, 4)}, "DM-09")
            order = [ly(k) for k in ("hairline", "brow", "nose", "chin")]
            add("landmark-order", order == sorted(order), [round(v, 1) for v in order], "DM-09")
        else:
            add("landmarks", False, sorted(lm), "DM-09")
    elif kind == "figure":
        try:
            heads = float(root.get("data-heads"))
            top, chin = ly("head-top"), ly("chin")
            foot = max(ly("foot-l"), ly("foot-r"))
            measured = (foot - top) / (chin - top)
            add("heads-tall", abs(measured - heads) <= 0.2, {"planned": heads, "measured": round(measured, 2)}, "DM-07")
            if heads >= 7:
                mid = (top + foot) / 2
                add("pelvis-midpoint", abs(ly("crotch") - mid) <= 0.25 * (chin - top),
                    {"offset_heads": round((ly("crotch") - mid) / (chin - top), 3)}, "DM-07")
            tilts = {e.get("data-part"): float(e.get("data-tilt")) for e in root.iter() if e.get("data-tilt") is not None}
            sup = [n for n in ("foot-l", "foot-r") if lm[n].get("data-support") == "1"]
            if sup:
                dx = abs(float(lm[sup[0]].get("cx")) - float(lm["neck"].get("cx"))) / (chin - top)
                add("gravity-over-support", dx <= 0.3, {"dx_heads": round(dx, 3)}, "DM-12")
                add("counter-tilt", tilts.get("rib-cage", 0) * tilts.get("pelvis", 0) < 0, tilts, "DM-12")
            add("line-of-action", any(e.get("data-part") == "line-of-action" for e in root.iter()), "path", "DM-06")
        except (KeyError, TypeError, ValueError, ZeroDivisionError) as exc:
            add("landmarks", False, f"unreadable: {exc}", "DM-07")
    elif kind == "character":
        shape = root.get("data-shape")
        dom = [e.get("data-shape") for e in root.iter() if e.get("data-part") in ("head", "body") and e.get("data-shape")]
        add("dominant-shape", shape in dom, {"declared": shape, "head_body": dom}, "DM-13")
        sec = [e.get("data-shape") for e in root.iter() if e.get("data-part") in ("hand", "foot")]
        add("secondary-shape", bool(sec) and all(s != shape for s in sec), sorted(set(sec)), "DM-13")
        heads = float(root.get("data-heads"))
        measured = (ly("foot") - ly("head-top")) / (ly("chin") - ly("head-top"))
        add("age-ratio", abs(measured - heads) <= 0.2, {"planned": heads, "measured": round(measured, 2), "age": root.get("data-age")}, "DM-15")
        emo = {e.get("data-emotion") for e in root.iter() if e.get("data-emotion")}
        add("expression-consistent", len(emo) == 1, sorted(emo), "DM-16")
    elif kind == "forms":
        rings = [(abs(float(e.get("data-dist"))), float(e.get("ry")) / float(e.get("rx"))) for e in root.iter(_q("ellipse"))
                 if e.get("data-part") == "cylinder-ellipse" and e.get("data-dist") is not None]
        rings = sorted(set(rings))
        ok = len(rings) >= 2 and all(b[1] >= a[1] for a, b in zip(rings, rings[1:]))
        add("ellipses-widen-from-eye-level", ok, [[round(d, 1), round(r, 3)] for d, r in rings], "DM-04")
        add("single-light", root.get("data-light") is not None, root.get("data-light"), "DM-19")
    elif kind == "bounce":
        balls = sorted(((int(e.get("data-frame")), e) for e in root.iter(_q("ellipse")) if e.get("data-part") == "ball"),
                       key=lambda t: t[0])
        r = float(root.get("data-radius"))
        ground = float(root.get("data-ground"))
        areas = [float(e.get("rx")) * float(e.get("ry")) / (r * r) for _, e in balls]
        add("volume-preserved", bool(areas) and max(abs(a - 1) for a in areas) <= 0.03,
            {"area_ratio_min": round(min(areas), 3), "area_ratio_max": round(max(areas), 3)}, "DM-27")
        cxy = [(float(e.get("cx")), float(e.get("cy"))) for _, e in balls]
        gaps = [math.dist(a, b) for a, b in zip(cxy, cxy[1:])]
        n = len(gaps)
        add("slow-in-slow-out", n >= 4 and gaps[0] < gaps[n // 2 - 1] and gaps[-1] < gaps[n // 2],
            {"first": round(gaps[0], 1), "before_contact": round(gaps[n // 2 - 1], 1), "last": round(gaps[-1], 1)}, "DM-28")
        hit = [e for _, e in balls if e.get("data-contact") == "1"]
        ok = len(hit) == 1 and float(hit[0].get("rx")) > float(hit[0].get("ry")) and \
            abs(float(hit[0].get("cy")) + float(hit[0].get("ry")) - ground) <= 0.5
        add("squash-on-contact", ok, "contact frame wider than tall and touching the ground" if ok else "missing or floating", "DM-27")
        stretch = [e for _, e in balls if e.get("data-contact") == "0" and float(e.get("ry")) > float(e.get("rx")) * 1.05]
        add("stretch-near-contact", len(stretch) >= 2, len(stretch), "DM-27")
    elif kind == "shadow":
        light = [float(v) for v in root.get("data-light").split(",")]
        foot = [float(v) for v in root.get("data-light-foot").split(",")]
        worst = 0.0
        marks = [c for c in root.iter(_q("circle")) if c.get("class") == "sh"]
        for c in marks:
            s = (float(c.get("cx")), float(c.get("cy")))
            b = [float(v) for v in c.get("data-base").split(",")]
            t = [float(v) for v in c.get("data-top").split(",")]
            for p0, p1 in ((foot, b), (light, t)):
                ln = math.dist(p0, s) or 1.0
                worst = max(worst, abs((p1[0] - p0[0]) * (s[1] - p0[1]) - (p1[1] - p0[1]) * (s[0] - p0[0])) / ln)
        add("shadow-rays-meet", len(marks) >= 2 and worst <= 1.0, {"points": len(marks), "max_offset_px": round(worst, 3)}, "DM-32")
        add("light-above-its-foot", light[1] < foot[1] and abs(light[0] - foot[0]) < 0.5, {"light": light, "foot": foot}, "DM-32")
        add("cast-shadow-drawn", any(e.get("data-part") == "cast-shadow" for e in root.iter()), "polygon", "DM-19")
    else:
        add("kind", False, kind, "-")
    res["passed"] = sum(c["pass"] for c in res["checks"])
    res["total"] = len(res["checks"])
    res["status"] = "PASS" if res["passed"] == res["total"] else "FAIL"
    res["scope"] = "Geometry and structure against the method cards only; not an aesthetic or professional-quality judgement."
    return res


# ------------------------------------------------------------------ review (anatomy and contact gate before delivery)

def _mat_mul(a, b):
    return (a[0] * b[0] + a[2] * b[1], a[1] * b[0] + a[3] * b[1], a[0] * b[2] + a[2] * b[3],
            a[1] * b[2] + a[3] * b[3], a[0] * b[4] + a[2] * b[5] + a[4], a[1] * b[4] + a[3] * b[5] + a[5])


def _transform(text):
    m = (1, 0, 0, 1, 0, 0)
    for name, args in re.findall(r"(\w+)\s*\(([^)]*)\)", text or ""):
        v = [float(x) for x in re.findall(r"-?[\d.]+(?:e-?\d+)?", args)]
        if name == "translate":
            t = (1, 0, 0, 1, v[0], v[1] if len(v) > 1 else 0)
        elif name == "scale":
            t = (v[0], 0, 0, v[1] if len(v) > 1 else v[0], 0, 0)
        elif name == "rotate":
            a = math.radians(v[0])
            c, s_ = math.cos(a), math.sin(a)
            t = (c, s_, -s_, c, 0, 0)
            if len(v) == 3:
                t = _mat_mul(_mat_mul((1, 0, 0, 1, v[1], v[2]), t), (1, 0, 0, 1, -v[1], -v[2]))
        elif name == "matrix":
            t = tuple(v[:6])
        else:
            continue
        m = _mat_mul(m, t)
    return m


def _apply(m, p):
    return (m[0] * p[0] + m[2] * p[1] + m[4], m[1] * p[0] + m[3] * p[1] + m[5])


def _path_points(d, steps=12):
    toks = re.findall(r"[MmLlHhVvQqTtCcSsZz]|-?\d*\.?\d+(?:e-?\d+)?", d)
    out, cur, start, i, cmd, last_ctrl = [], (0.0, 0.0), (0.0, 0.0), 0, "M", None
    while i < len(toks):
        if re.match(r"[A-Za-z]", toks[i]):
            cmd = toks[i]
            i += 1
            if cmd in "Zz":
                out.append(start)
                cur = start
                continue
        rel = cmd.islower()
        n = {"M": 2, "L": 2, "H": 1, "V": 1, "Q": 4, "T": 2, "C": 6, "S": 4}[cmd.upper()]
        v = [float(t) for t in toks[i:i + n]]
        i += n
        ox, oy = cur if rel else (0.0, 0.0)
        u = cmd.upper()
        if u == "H":
            pts_ = [(v[0] + ox, cur[1])]
        elif u == "V":
            pts_ = [(cur[0], v[0] + oy)]
        else:
            pts_ = [(v[k] + ox, v[k + 1] + oy) for k in range(0, n, 2)]
        if u == "M":
            start = pts_[0]
            out.append(pts_[0])
            cmd = "l" if rel else "L"
        elif u in "LHV":
            out.append(pts_[0])
        else:
            if u == "T":
                pts_ = [(2 * cur[0] - last_ctrl[0], 2 * cur[1] - last_ctrl[1]) if last_ctrl else cur] + pts_
            if u == "S":
                pts_ = [(2 * cur[0] - last_ctrl[0], 2 * cur[1] - last_ctrl[1]) if last_ctrl else cur] + pts_
            ctrl = [cur] + pts_
            for k in range(1, steps + 1):
                t = k / steps
                q = ctrl
                while len(q) > 1:
                    q = [((1 - t) * a[0] + t * b[0], (1 - t) * a[1] + t * b[1]) for a, b in zip(q, q[1:])]
                out.append(q[0])
            last_ctrl = pts_[-2]
            cur = pts_[-1]
            continue
        last_ctrl = None
        cur = out[-1]
    return out


def _geometry(e, m):
    """Outline of one SVG element in page space: (points, closed, filled, half stroke width)."""
    tag = e.tag.split("}")[-1]
    g = lambda k, d=0.0: float(e.get(k, d))
    if tag in ("circle", "ellipse"):
        rx = g("r") if tag == "circle" else g("rx")
        ry = g("r") if tag == "circle" else g("ry")
        pts_ = [(g("cx") + rx * math.cos(a), g("cy") + ry * math.sin(a)) for a in (i * math.pi / 24 for i in range(48))]
        closed = True
    elif tag == "rect":
        x, y, w, h = g("x"), g("y"), g("width"), g("height")
        pts_, closed = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)], True
    elif tag == "line":
        pts_, closed = [(g("x1"), g("y1")), (g("x2"), g("y2"))], False
    elif tag in ("polyline", "polygon"):
        v = [float(t) for t in re.findall(r"-?[\d.]+", e.get("points", ""))]
        pts_, closed = list(zip(v[::2], v[1::2])), tag == "polygon"
    elif tag == "path":
        pts_ = _path_points(e.get("d", ""))
        closed = bool(re.search(r"[Zz]\s*$", e.get("d", "")))
    else:
        return None
    fill = e.get("data-fill", e.get("fill"))
    filled = closed or (fill not in (None, "none") and tag in ("path", "polyline"))
    scale = math.sqrt(abs(m[0] * m[3] - m[1] * m[2])) or 1.0
    half = float(e.get("stroke-width", "0") or 0) * scale / 2
    return [_apply(m, p) for p in pts_], filled, half


def _inside(p, poly):
    hit, j = False, len(poly) - 1
    for i in range(len(poly)):
        (xi, yi), (xj, yj) = poly[i], poly[j]
        if (yi > p[1]) != (yj > p[1]) and p[0] < (xj - xi) * (p[1] - yi) / ((yj - yi) or 1e-9) + xi:
            hit = not hit
        j = i
    return hit


def _seg_dist(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / ((dx * dx + dy * dy) or 1e-9)))
    return math.dist(p, (a[0] + t * dx, a[1] + t * dy))


def _gap(a, b):
    """Pixels of empty space between two parts; 0 when they touch or overlap."""
    (pa, fa, ha), (pb, fb, hb) = a, b
    if (fb and any(_inside(p, pb) for p in pa)) or (fa and any(_inside(p, pa) for p in pb)):
        return 0.0
    segs = lambda pts_: list(zip(pts_, pts_[1:] + pts_[:1])) if len(pts_) > 2 else [(pts_[0], pts_[-1])]
    best = min(min(_seg_dist(p, s0, s1) for s0, s1 in segs(pb)) for p in pa)
    best = min(best, min(min(_seg_dist(p, s0, s1) for s0, s1 in segs(pa)) for p in pb))
    return max(0.0, best - ha - hb)


def review_svg(path, tolerance=1.5):
    """Anatomy and contact gate: every figure is one connected body, every declared contact touches.

    Mark each body (person, animal, prop) as <g data-figure="name"> and each of its pieces with data-part;
    a piece that must rest on something else carries data-contact="<other part id or figure name>".
    """
    root = ET.parse(path).getroot()
    res = {"schema": "kosif.drawing.review.v1", "file": str(path), "tolerance_px": tolerance, "checks": []}

    def add(cid, ok, observed, method):
        res["checks"].append({"id": cid, "pass": bool(ok), "observed": observed, "method": method})

    figures, parts_by_id, contacts = {}, {}, []

    def walk(node, m, fig):
        m = _mat_mul(m, _transform(node.get("transform")))
        if node.get("data-figure"):
            fig = node.get("data-figure")
            figures.setdefault(fig, [])
        geo = _geometry(node, m) if node.get("data-part") else None
        if geo and geo[0]:
            name = node.get("data-part")
            if fig:
                figures[fig].append((name, geo))
            parts_by_id[node.get("id") or name] = geo
            if node.get("data-contact"):
                contacts.append((fig, name, node.get("data-contact"), geo))
        for child in node:
            walk(child, m, fig)

    walk(root, (1, 0, 0, 1, 0, 0), None)
    if not figures:
        add("figures-declared", False, "no <g data-figure> groups with data-part pieces", "DM-08")
    for fig, parts in figures.items():
        n = len(parts)
        link = {i: {i} for i in range(n)}
        for i in range(n):
            for j in range(i + 1, n):
                if _gap(parts[i][1], parts[j][1]) <= tolerance:
                    link[i].add(j)
                    link[j].add(i)
        seen, groups = set(), []
        for i in range(n):
            if i in seen:
                continue
            stack, comp = [i], []
            while stack:
                k = stack.pop()
                if k in seen:
                    continue
                seen.add(k)
                comp.append(parts[k][0])
                stack.extend(link[k] - seen)
            groups.append(sorted(comp))
        obs = {"parts": n, "pieces": len(groups)}
        if len(groups) > 1:
            main = max(groups, key=len)
            obs["detached"] = [g for g in groups if g is not main]
            obs["nearest_gap_px"] = {",".join(g): round(min(_gap(p[1], q[1]) for p in parts if p[0] in g
                                                            for q in parts if q[0] in main), 1)
                                     for g in obs["detached"]}
        add(f"one-body:{fig}", len(groups) == 1, obs, "DM-08")
    figure_geo = {f: [g for _, g in ps] for f, ps in figures.items()}
    for fig, name, target, geo in contacts:
        others = figure_geo.get(target) or ([parts_by_id[target]] if target in parts_by_id else [])
        if not others:
            add(f"contact:{fig}.{name}->{target}", False, "target not found", "DM-12")
            continue
        gap = min(_gap(geo, o) for o in others)
        add(f"contact:{fig}.{name}->{target}", gap <= tolerance, {"gap_px": round(gap, 1)}, "DM-12")
    supported = {f for f, _, _, _ in contacts if f}
    for fig in figures:
        if fig not in root.get("data-floating", "").split() and fig not in supported and not any(t == fig for _, _, t, _ in contacts):
            add(f"supported:{fig}", False, "nothing holds this figure up (add data-contact or data-floating)", "DM-12")
    res["passed"] = sum(c["pass"] for c in res["checks"])
    res["total"] = len(res["checks"])
    res["status"] = "PASS" if res["checks"] and res["passed"] == res["total"] else "FAIL"
    res["visual_review_still_required"] = [
        "Open the rendered PNG and look at it before sending",
        "Each body reads as one piece: neck joins head to chest, waist joins chest to hips, limbs start at joints",
        "Limb count, bend direction and lengths are plausible for the pose",
        "Hands and feet rest on what holds them; nothing hangs in the air without a reason",
        "Scale and perspective agree between figures and props; shadows follow one light",
    ]
    res["scope"] = "Touch geometry between declared parts only; it does not see the picture, judge anatomy beyond contact, or judge beauty."
    return res


# ------------------------------------------------------------------ cli

def emit(obj, out=None, force=False):
    blob = obj if isinstance(obj, str) else json.dumps(obj, ensure_ascii=False, indent=2) + "\n"
    if out:
        p = Path(out)
        if p.exists() and not force:
            raise ValueError(f"refusing to overwrite {p} (pass --force)")
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(blob, encoding="utf-8")
        if not isinstance(obj, str):
            return
        print(json.dumps({"wrote": str(p), "bytes": len(blob.encode("utf-8"))}, ensure_ascii=False))
    else:
        sys.stdout.write(blob)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--atlas", type=Path, default=ATLAS)
    sub = ap.add_subparsers(dest="cmd", required=True)
    ls = sub.add_parser("list", help="list method cards")
    ls.add_argument("--domain")
    fd = sub.add_parser("find", help="rank method cards for a request (Arabic or English)")
    fd.add_argument("query")
    fd.add_argument("--top", type=int, default=5)
    sh = sub.add_parser("show", help="print one method card")
    sh.add_argument("--id", required=True)
    pl = sub.add_parser("plan", help="ordered drawing plan (intent -> verify) for a request")
    pl.add_argument("query")
    pl.add_argument("--max", type=int, default=4)
    pl.add_argument("--out")
    pr = sub.add_parser("prompt", help="image-generation prompt built from method cards (no model is called)")
    pr.add_argument("subject")
    pr.add_argument("--methods", help="comma-separated ids, e.g. DM-13,DM-16")
    pr.add_argument("--style", default="")
    dr = sub.add_parser("draw", help="write a layered construction SVG")
    dr.add_argument("kind", choices=["head", "figure", "character", "forms", "bounce", "shadow"])
    dr.add_argument("--out", required=True)
    dr.add_argument("--force", action="store_true")
    dr.add_argument("--yaw", type=float, default=30.0)
    dr.add_argument("--pitch", type=float, default=0.0)
    dr.add_argument("--heads", type=float, default=8.0)
    dr.add_argument("--pose", default="contrapposto", choices=sorted(POSES))
    dr.add_argument("--shape", default="circle", choices=sorted(SECONDARY))
    dr.add_argument("--age", default="child", choices=sorted(AGES))
    dr.add_argument("--expression", default="happy", choices=sorted(EXPRESSIONS))
    dr.add_argument("--eye-level", type=float, default=0.45)
    dr.add_argument("--frames", type=int, default=13, help="bounce: odd frame count, apex to apex")
    dr.add_argument("--bounce-height", type=float, default=0.55)
    dr.add_argument("--light-x", type=float, default=0.15, help="shadow: light position across the frame")
    dr.add_argument("--light-height", type=float, default=0.4)
    ck = sub.add_parser("check", help="measure a drawn SVG against its method cards")
    ck.add_argument("--svg", required=True)
    ck.add_argument("--out")
    rv = sub.add_parser("review", help="anatomy and contact gate: one connected body per figure, declared contacts touch")
    rv.add_argument("--svg", required=True)
    rv.add_argument("--tolerance", type=float, default=1.5, help="largest gap in px still counted as touching")
    rv.add_argument("--out")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "draw":
            if args.kind == "head":
                svg, _ = draw_head(args.yaw, args.pitch)
            elif args.kind == "figure":
                svg, _ = draw_figure(args.heads, args.pose)
            elif args.kind == "character":
                svg, _ = draw_character(args.shape, args.age, args.expression)
            elif args.kind == "bounce":
                svg, _ = draw_bounce(args.frames, args.bounce_height)
            elif args.kind == "shadow":
                svg, _ = draw_shadow(args.light_x, args.light_height)
            else:
                svg, _ = draw_forms(args.eye_level)
            emit(svg, args.out, args.force)
            return 0
        if args.cmd == "check":
            res = check_svg(args.svg)
            emit(res, args.out)
            return 0 if res["status"] == "PASS" else 1
        if args.cmd == "review":
            res = review_svg(args.svg, args.tolerance)
            emit(res, args.out)
            return 0 if res["status"] == "PASS" else 1
        data = load_atlas(args.atlas)
        if args.cmd == "list":
            emit({"schema": data["schema"], "status": data["status"], "count": len(data["methods"]),
                  "methods": [{"id": m["id"], "domain": m["domain"], "name_ar": m["name_ar"], "name_en": m["name_en"]}
                              for m in data["methods"] if not args.domain or m["domain"] == args.domain]})
        elif args.cmd == "find":
            emit({"query": args.query, "results": find(data, args.query, args.top)})
        elif args.cmd == "show":
            card = next((m for m in data["methods"] if m["id"] == args.id), None)
            if card is None:
                raise ValueError("unknown method id")
            emit(card)
        elif args.cmd == "plan":
            emit(plan(data, args.query, args.max), args.out)
        else:
            ids = [s.strip() for s in args.methods.split(",")] if args.methods else None
            emit(prompt(data, args.subject, ids, args.style))
        return 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError, ET.ParseError) as exc:
        print("DRAWING_METHODS_ERROR: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
