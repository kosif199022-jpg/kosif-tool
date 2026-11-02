"""Shadow-theatre renderer: projected backdrop, articulated body silhouettes, props, depth, iris and spotlight.

Pure Python + numpy + Pillow. Each frame is drawn from a scene spec (JSON) as a function of time, so any
frame can be rendered alone (stills) and the film is deterministic.

Units: x is a fraction of the screen width, y a fraction of the screen height (y=1 is the bottom edge),
sizes (figure height, prop scale) are fractions of the screen height. Angles are degrees.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

# --------------------------------------------------------------------------- easing and keyframes

EASES = {
    "linear": lambda u: u,
    "in": lambda u: u * u * u,
    "out": lambda u: 1 - (1 - u) ** 3,
    "inout": lambda u: 4 * u * u * u if u < 0.5 else 1 - (-2 * u + 2) ** 3 / 2,
    "smooth": lambda u: u * u * (3 - 2 * u),
    "hold": lambda u: 0.0,
}

ANIM_FIELDS = ("x", "y", "scale", "depth", "rot", "opacity", "height")


def _lerp(a, b, u):
    return a + (b - a) * u


def sample_keys(keys: list[dict], t: float) -> dict:
    """Interpolate numeric fields and named poses between keyframes (keys sorted by t)."""
    if not keys:
        return {}
    if t <= keys[0]["t"]:
        k = dict(keys[0])
        k["_pose_mix"] = (k.get("pose"), k.get("pose"), 0.0)
        return k
    if t >= keys[-1]["t"]:
        k = dict(keys[-1])
        k["_pose_mix"] = (k.get("pose"), k.get("pose"), 0.0)
        return k
    for a, b in zip(keys, keys[1:]):
        if a["t"] <= t <= b["t"]:
            span = max(1e-6, b["t"] - a["t"])
            u = EASES.get(b.get("ease", "inout"), EASES["inout"])((t - a["t"]) / span)
            out = {}
            for f in ANIM_FIELDS:
                if f in a or f in b:
                    va, vb = a.get(f, b.get(f)), b.get(f, a.get(f))
                    out[f] = _lerp(va, vb, u)
            for f in ("facing", "shape", "costume"):
                if f in a:
                    out[f] = a[f]
            out["_pose_mix"] = (a.get("pose"), b.get("pose", a.get("pose")), u)
            return out
    return dict(keys[-1])


# --------------------------------------------------------------------------- body model

# Limb directions: 0 = straight down, +90 = forward (+x when facing right), 180 = up.
# Arms are measured relative to the torso, legs are absolute. Elbow/knee are bends added to the parent.
JOINTS = ("torso", "head", "arm_a", "elbow_a", "arm_b", "elbow_b", "leg_a", "knee_a", "leg_b", "knee_b")

POSES: dict[str, dict] = {
    "stand":      dict(torso=0, head=0, arm_a=8, elbow_a=6, arm_b=-8, elbow_b=-6, leg_a=4, knee_a=0, leg_b=-4, knee_b=0),
    "arms_up":    dict(torso=0, head=-10, arm_a=160, elbow_a=8, arm_b=-160, elbow_b=-8, leg_a=6, knee_a=0, leg_b=-6, knee_b=0),
    "reach_up":   dict(torso=-6, head=-25, arm_a=172, elbow_a=0, arm_b=35, elbow_b=10, leg_a=8, knee_a=0, leg_b=-14, knee_b=18),
    "offer":      dict(torso=8, head=10, arm_a=80, elbow_a=10, arm_b=70, elbow_b=20, leg_a=12, knee_a=0, leg_b=-10, knee_b=0),
    "lunge":      dict(torso=12, head=0, arm_a=105, elbow_a=0, arm_b=-110, elbow_b=0, leg_a=45, knee_a=-45, leg_b=-38, knee_b=0),
    "dance_arc":  dict(torso=-16, head=-15, arm_a=150, elbow_a=25, arm_b=-105, elbow_b=-10, leg_a=12, knee_a=0, leg_b=-70, knee_b=45),
    "spin":       dict(torso=4, head=5, arm_a=95, elbow_a=0, arm_b=-95, elbow_b=0, leg_a=0, knee_a=0, leg_b=20, knee_b=-60),
    "crouch":     dict(torso=35, head=15, arm_a=40, elbow_a=30, arm_b=20, elbow_b=40, leg_a=85, knee_a=-110, leg_b=60, knee_b=-95),
    "kneel":      dict(torso=10, head=20, arm_a=60, elbow_a=40, arm_b=30, elbow_b=50, leg_a=85, knee_a=-85, leg_b=-10, knee_b=-80),
    "bow":        dict(torso=70, head=10, arm_a=-60, elbow_a=0, arm_b=-70, elbow_b=0, leg_a=2, knee_a=0, leg_b=-2, knee_b=0),
    "frond":      dict(torso=58, head=20, arm_a=140, elbow_a=45, arm_b=115, elbow_b=-35, leg_a=-25, knee_a=0, leg_b=-45, knee_b=0),
    "trunk":      dict(torso=0, head=0, arm_a=150, elbow_a=-40, arm_b=-150, elbow_b=40, leg_a=2, knee_a=0, leg_b=-2, knee_b=0),
    "hull":       dict(torso=90, head=-30, arm_a=-5, elbow_a=0, arm_b=-15, elbow_b=0, leg_a=-90, knee_a=0, leg_b=-96, knee_b=0),
    "sail":       dict(torso=-4, head=-20, arm_a=176, elbow_a=0, arm_b=125, elbow_b=-25, leg_a=6, knee_a=0, leg_b=-6, knee_b=0),
    "carry":      dict(torso=-4, head=-15, arm_a=165, elbow_a=-25, arm_b=-165, elbow_b=25, leg_a=10, knee_a=0, leg_b=-10, knee_b=0),
    "embrace":    dict(torso=14, head=18, arm_a=85, elbow_a=50, arm_b=70, elbow_b=60, leg_a=10, knee_a=0, leg_b=-8, knee_b=0),
}

COSTUMES = {
    # proportions as a fraction of the figure height (fleshy, like real bodies on a screen, not stick men)
    "plain": dict(head=0.068, torso=0.30, upper_arm=0.17, forearm=0.16, thigh=0.25, shin=0.245, w_chest=0.155, w_hip=0.125, w_limb=0.062),
    "dress": dict(head=0.066, torso=0.29, upper_arm=0.165, forearm=0.155, thigh=0.25, shin=0.245, w_chest=0.13, w_hip=0.115, w_limb=0.05),
    "child": dict(head=0.09, torso=0.28, upper_arm=0.15, forearm=0.14, thigh=0.22, shin=0.21, w_chest=0.15, w_hip=0.13, w_limb=0.066),
    "elder": dict(head=0.068, torso=0.29, upper_arm=0.165, forearm=0.155, thigh=0.25, shin=0.24, w_chest=0.16, w_hip=0.13, w_limb=0.06),
}


def resolve_pose(name_or_dict) -> dict:
    if isinstance(name_or_dict, dict):
        base = dict(POSES["stand"])
        if "base" in name_or_dict:
            base.update(POSES[name_or_dict["base"]])
        base.update({k: v for k, v in name_or_dict.items() if k in JOINTS})
        return base
    if name_or_dict is None:
        return dict(POSES["stand"])
    if name_or_dict not in POSES:
        raise KeyError(f"unknown pose {name_or_dict!r}; known: {', '.join(sorted(POSES))}")
    return dict(POSES[name_or_dict])


def mix_pose(mix) -> dict:
    a, b, u = mix
    pa, pb = resolve_pose(a), resolve_pose(b)
    return {j: _lerp(pa[j], pb[j], u) for j in JOINTS}


def apply_cycle(pose: dict, cycle: dict | None, t: float) -> dict:
    """Procedural motion on top of the keyed pose: walk, sway, wave, breathe."""
    if not cycle:
        return pose
    p = dict(pose)
    kind, period = cycle.get("type", "walk"), max(0.05, float(cycle.get("period", 1.0)))
    amp = float(cycle.get("amp", 1.0))
    ph = 2 * math.pi * (t / period + float(cycle.get("phase", 0.0)))
    s = math.sin(ph)
    if kind == "walk":
        p["leg_a"] += 26 * amp * s
        p["leg_b"] -= 26 * amp * s
        p["knee_a"] += -32 * amp * max(0.0, -s)
        p["knee_b"] += -32 * amp * max(0.0, s)
        p["arm_a"] -= 20 * amp * s
        p["arm_b"] += 20 * amp * s
    elif kind == "sway":
        p["torso"] += 7 * amp * s
        p["arm_a"] += 12 * amp * s
        p["arm_b"] += 12 * amp * s
    elif kind == "wave":
        p["elbow_a"] += 28 * amp * s
        p["arm_a"] += 8 * amp * math.sin(ph * 0.5)
    elif kind == "breathe":
        p["torso"] += 2.5 * amp * s
        p["head"] += 3 * amp * s
    elif kind == "flutter":  # fronds in wind
        p["elbow_a"] += 14 * amp * s
        p["elbow_b"] += 14 * amp * math.sin(ph + 1.3)
        p["torso"] += 3 * amp * math.sin(ph + 0.6)
    return p


def _dir(deg: float, facing: int) -> tuple[float, float]:
    r = math.radians(deg)
    return facing * math.sin(r), math.cos(r)


def body_skeleton(pose: dict, costume: str, h_px: float, facing: int):
    """Forward kinematics with the hip at (0,0). Returns joints dict and proportions."""
    c = COSTUMES.get(costume, COSTUMES["plain"])
    L = {k: v * h_px for k, v in c.items()}
    tor = math.radians(pose["torso"])
    up = (facing * math.sin(tor), -math.cos(tor))
    hip = (0.0, 0.0)
    chest = (up[0] * L["torso"], up[1] * L["torso"])
    hr = math.radians(pose["torso"] + pose["head"] * 0.6)
    hu = (facing * math.sin(hr), -math.cos(hr))
    neck = (chest[0] + hu[0] * L["head"] * 0.55, chest[1] + hu[1] * L["head"] * 0.55)
    head = (neck[0] + hu[0] * L["head"] * 1.05, neck[1] + hu[1] * L["head"] * 1.05)
    j = {"hip": hip, "chest": chest, "neck": neck, "head": head}
    for side in ("a", "b"):
        a1 = pose["arm_" + side] + pose["torso"]
        d1 = _dir(a1, facing)
        sh = (chest[0] - up[0] * L["torso"] * 0.06, chest[1] - up[1] * L["torso"] * 0.06)
        el = (sh[0] + d1[0] * L["upper_arm"], sh[1] + d1[1] * L["upper_arm"])
        d2 = _dir(a1 + pose["elbow_" + side], facing)
        wr = (el[0] + d2[0] * L["forearm"], el[1] + d2[1] * L["forearm"])
        j["sh_" + side], j["el_" + side], j["wr_" + side] = sh, el, wr
        l1 = pose["leg_" + side]
        e1 = _dir(l1, facing)
        kn = (hip[0] + e1[0] * L["thigh"], hip[1] + e1[1] * L["thigh"])
        e2 = _dir(l1 + pose["knee_" + side], facing)
        ft = (kn[0] + e2[0] * L["shin"], kn[1] + e2[1] * L["shin"])
        j["kn_" + side], j["ft_" + side] = kn, ft
    return j, L


def _capsule(draw: ImageDraw.ImageDraw, p, q, w, fill=255):
    draw.line([p, q], fill=fill, width=max(1, int(round(w))))
    r = w / 2
    for c in (p, q):
        draw.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], fill=fill)


def draw_body(draw, ox, oy, pose, costume, h_px, facing, grounded):
    j, L = body_skeleton(pose, costume, h_px, facing)
    if grounded:  # put the lowest point (foot or knee) on the ground line oy
        low = max(j["ft_a"][1], j["ft_b"][1], j["kn_a"][1], j["kn_b"][1], j["hip"][1] + L["w_hip"] * 0.5)
        oy = oy - low - L["w_limb"] * 0.4
    P = {k: (ox + v[0], oy + v[1]) for k, v in j.items()}
    wl = L["w_limb"]
    # legs
    for s in ("a", "b"):
        _capsule(draw, P["hip"], P["kn_" + s], wl * 1.25)
        _capsule(draw, P["kn_" + s], P["ft_" + s], wl * 0.95)
        fx, fy = P["ft_" + s]
        draw.polygon([(fx - wl * 0.45, fy - wl * 0.4), (fx + facing * wl * 1.5, fy + wl * 0.05), (fx - wl * 0.45, fy + wl * 0.3)], fill=255)
    # torso quad
    hx, hy = P["hip"]
    cx, cy = P["chest"]
    dx, dy = cx - hx, cy - hy
    n = math.hypot(dx, dy) or 1
    nx, ny = -dy / n, dx / n
    wc, wh = L["w_chest"] / 2, L["w_hip"] / 2
    draw.polygon([(hx + nx * wh, hy + ny * wh), (cx + nx * wc, cy + ny * wc), (cx - nx * wc, cy - ny * wc), (hx - nx * wh, hy - ny * wh)], fill=255)
    _capsule(draw, P["chest"], P["neck"], wl * 0.9)
    draw.ellipse([cx - wc * 1.05, cy - wc * 1.05, cx + wc * 1.05, cy + wc * 1.05], fill=255)
    draw.ellipse([hx - wh * 1.1, hy - wh * 1.1, hx + wh * 1.1, hy + wh * 1.1], fill=255)
    # head (slightly egg-shaped) + hair detail
    r = L["head"]
    gx, gy = P["head"]
    draw.ellipse([gx - r * 0.86, gy - r, gx + r * 0.86, gy + r], fill=255)
    if costume in ("dress", "child"):
        bx = gx - facing * r * 0.95
        draw.ellipse([bx - r * 0.42, gy - r * 0.2, bx + r * 0.42, gy + r * 0.62], fill=255)
    if costume == "elder":  # bent walking stick in the front hand
        wx, wy = P["wr_a"]
        draw.line([(wx, wy), (wx + facing * r * 0.6, oy + 0.0)], fill=255, width=max(1, int(wl * 0.45)))
    # skirt
    if costume in ("dress", "child"):
        hem = h_px * (0.36 if costume == "dress" else 0.25)
        ml = math.radians((pose["leg_a"] + pose["leg_b"]) * 0.5)
        hx2, hy2 = hx + facing * math.sin(ml) * hem, hy + math.cos(ml) * hem
        ww = h_px * (0.13 if costume == "dress" else 0.11)
        draw.polygon([(hx - wh * 1.2, hy - h_px * 0.05), (hx + wh * 1.2, hy - h_px * 0.05), (hx2 + ww, hy2), (hx2 - ww, hy2)], fill=255)
    # arms last (they cross the torso)
    for s in ("a", "b"):
        _capsule(draw, P["sh_" + s], P["el_" + s], wl * 1.0)
        _capsule(draw, P["el_" + s], P["wr_" + s], wl * 0.8)
        wx, wy = P["wr_" + s]
        draw.ellipse([wx - wl * 0.45, wy - wl * 0.45, wx + wl * 0.45, wy + wl * 0.45], fill=255)


# --------------------------------------------------------------------------- props


def _poly(draw, pts, fill=255):
    draw.polygon([(float(x), float(y)) for x, y in pts], fill=fill)


def shape_points(shape: str, n: int = 160) -> list[tuple[float, float]]:
    """Unit outlines centred on (0,0), radius ~0.5. Used for props and iris masks."""
    pts = []
    if shape == "circle":
        pts = [(0.5 * math.cos(a), 0.5 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, n, endpoint=False)]
    elif shape == "heart":
        for a in np.linspace(0, 2 * math.pi, n, endpoint=False):
            x = 16 * math.sin(a) ** 3
            y = 13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a)
            pts.append((x / 34, -y / 34 - 0.03))
    elif shape == "star":
        for i in range(10):
            a = -math.pi / 2 + i * math.pi / 5
            r = 0.5 if i % 2 == 0 else 0.21
            pts.append((r * math.cos(a), r * math.sin(a)))
    elif shape == "arch":  # pointed arch / mihrab window
        pts = [(-0.3, 0.5), (-0.3, -0.05)]
        for a in np.linspace(math.pi, math.pi * 4 / 3, 24):
            pts.append((0.3 + 0.6 * math.cos(a), -0.05 + 0.45 * math.sin(a)))
        for a in np.linspace(math.pi * 5 / 3, math.pi * 2, 24):
            pts.append((-0.3 + 0.6 * math.cos(a), -0.05 + 0.45 * math.sin(a)))
        pts += [(0.3, -0.05), (0.3, 0.5)]
    else:
        raise KeyError(f"unknown outline {shape!r}")
    return pts


def draw_prop(img: Image.Image, shape: str, cx: float, cy: float, s: float, rot: float, t: float, params: dict):
    """s = prop size in pixels. (cx, cy) = anchor (centre, or base centre for grounded things)."""
    d = ImageDraw.Draw(img)
    cr, sr = math.cos(math.radians(rot)), math.sin(math.radians(rot))

    def T(x, y):
        return cx + (x * cr - y * sr) * s, cy + (x * sr + y * cr) * s

    if shape in ("circle", "heart", "star", "arch", "sun"):
        _poly(d, [T(x, y) for x, y in shape_points("circle" if shape == "sun" else shape)])
    elif shape == "crescent":
        _poly(d, [T(x, y) for x, y in shape_points("circle")])
        _poly(d, [T(x * 0.92 + 0.2, y * 0.92 - 0.1) for x, y in shape_points("circle")], fill=0)
    elif shape == "bird":
        f = math.sin(2 * math.pi * t * params.get("flap", 2.2))
        wy = -0.35 * f
        pts = [(-0.5, wy), (-0.25, -0.05 + wy * 0.3), (-0.05, 0.02), (0, -0.04), (0.05, 0.02), (0.25, -0.05 + wy * 0.3),
               (0.5, wy), (0.28, 0.05 + wy * 0.25), (0.06, 0.1), (0, 0.13), (-0.06, 0.1), (-0.28, 0.05 + wy * 0.25)]
        _poly(d, [T(x, y) for x, y in pts])
    elif shape == "palm":  # anchor = base of trunk, s = total height
        sway = math.sin(2 * math.pi * t / params.get("period", 3.0)) * 0.03
        trunk = []
        for i in range(21):
            u = i / 20
            x = 0.12 * math.sin(u * 1.6) + sway * u * u
            w = 0.035 * (1 - u) + 0.018
            trunk.append((x, -u, w))
        left = [T(x - w, y) for x, y, w in trunk]
        right = [T(x + w, y) for x, y, w in reversed(trunk)]
        _poly(d, left + right)
        top = trunk[-1]
        for k, ang in enumerate((-160, -125, -95, -60, -25, 10, 150, 35)):
            a = math.radians(ang + 8 * math.sin(2 * math.pi * t / params.get("period", 3.0) + k))
            ln = 0.42 if abs(ang) < 140 else 0.3
            frond = []
            for i in range(13):
                u = i / 12
                fx = top[0] + math.cos(a) * ln * u
                fy = top[1] + math.sin(a) * ln * u + 0.28 * u * u
                frond.append((fx, fy, 0.045 * math.sin(math.pi * min(0.999, u + 0.05))))
            _poly(d, [T(x, y - w) for x, y, w in frond] + [T(x, y + w) for x, y, w in reversed(frond)])
        for k in range(3):
            bx, by = top[0] - 0.03 + 0.03 * k, top[1] + 0.05
            x0, y0 = T(bx - 0.022, by - 0.022)
            x1, y1 = T(bx + 0.022, by + 0.022)
            d.ellipse([min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)], fill=255)
    elif shape == "skyline":  # domes and minarets, anchor = bottom centre, s = height
        base = [(-1.1, 0), (-1.1, -0.18), (1.1, -0.18), (1.1, 0)]
        _poly(d, [T(x, y) for x, y in base])
        for dx, r in ((0.0, 0.32), (-0.55, 0.16), (0.55, 0.16)):
            dome = [(dx + r * math.cos(a), -0.18 - 0.05 - r * 1.05 * math.sin(a)) for a in np.linspace(0, math.pi, 40)]
            _poly(d, [T(x, y) for x, y in [(dx + r, -0.17)] + dome + [(dx - r, -0.17)]])
            _poly(d, [T(x, y) for x, y in [(dx - 0.012, -0.22 - r * 1.05), (dx, -0.33 - r * 1.05), (dx + 0.012, -0.22 - r * 1.05)]])
        for mx in (-0.92, 0.92):
            _poly(d, [T(x, y) for x, y in [(mx - 0.045, -0.18), (mx - 0.035, -0.85), (mx + 0.035, -0.85), (mx + 0.045, -0.18)]])
            _poly(d, [T(x, y) for x, y in [(mx - 0.07, -0.62), (mx + 0.07, -0.62), (mx + 0.07, -0.66), (mx - 0.07, -0.66)]])
            _poly(d, [T(x, y) for x, y in [(mx - 0.035, -0.85), (mx, -1.0), (mx + 0.035, -0.85)]])
        # cut arched windows: light passes through, like a punched shadow puppet
        for wx in (-0.3, -0.1, 0.1, 0.3):
            _poly(d, [T(x * 0.11 + wx, y * 0.2 - 0.1) for x, y in shape_points("arch")], fill=0)
    elif shape == "dunes":  # full-width ground band; s = band height, cx ignored
        w = img.size[0]
        ph = t * params.get("drift", 0.0)
        pts = [(0, cy)]
        for i in range(0, 101):
            u = i / 100
            y = cy - s * (0.55 + 0.25 * math.sin(u * 7.0 + 1.3 + ph) + 0.2 * math.sin(u * 15.0 + ph * 1.7))
            pts.append((u * w, y))
        pts.append((w, cy))
        _poly(d, pts)
    elif shape == "waves":
        w = img.size[0]
        ph = 2 * math.pi * t / params.get("period", 2.4)
        pts = [(0, cy + s)]
        for i in range(0, 161):
            u = i / 160
            y = cy - s * (0.5 + 0.28 * math.sin(u * 18 - ph) + 0.18 * math.sin(u * 41 + ph * 1.4))
            pts.append((u * w, y))
        pts.append((w, cy + s))
        _poly(d, pts)
    elif shape == "lantern":  # Ramadan fanous; anchor = hanging ring, s = height
        sw = math.sin(2 * math.pi * t / params.get("period", 2.8)) * 6
        c2, s2 = math.cos(math.radians(rot + sw)), math.sin(math.radians(rot + sw))

        def U(x, y):
            return cx + (x * c2 - y * s2) * s, cy + (x * s2 + y * c2) * s

        if params.get("chain", 0):
            d.line([U(0, -params["chain"]), U(0, 0)], fill=255, width=max(1, int(s * 0.015)))
        ring = [U(0.06 * math.cos(a), 0.05 + 0.05 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 24)]
        _poly(d, ring)
        _poly(d, [U(0.03 * math.cos(a), 0.05 + 0.025 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 16)], fill=0)
        body = [(-0.08, 0.1), (0.08, 0.1), (0.2, 0.24), (0.2, 0.56), (0.28, 0.62), (0.13, 0.82), (0.0, 0.9),
                (-0.13, 0.82), (-0.28, 0.62), (-0.2, 0.56), (-0.2, 0.24)]
        _poly(d, [U(x, y) for x, y in body])
        for wx in (-0.1, 0.1):  # cut-out windows let the light through
            _poly(d, [U(x * 0.13 + wx, y * 0.3 + 0.42) for x, y in shape_points("arch")], fill=0)
        _poly(d, [U(x * 0.08, y * 0.08 + 0.72) for x, y in shape_points("star")], fill=0)
    elif shape == "foliage":  # a leafy branch held by a performer; anchor = centre, s = diameter
        rng = np.random.default_rng(int(params.get("seed", 3)))
        n = int(params.get("leaves", 60))
        for i in range(n):
            a, r = rng.random() * 2 * math.pi, 0.42 * math.sqrt(rng.random())
            lx, ly = r * math.cos(a), r * math.sin(a) * 0.7
            lx += 0.015 * math.sin(2 * math.pi * t / params.get("period", 2.0) + i)
            la = rng.random() * math.pi
            ln, lw = 0.09 + 0.05 * rng.random(), 0.04
            leaf = []
            for k in range(16):
                u = 2 * math.pi * k / 16
                ex, ey = ln * math.cos(u), lw * math.sin(u)
                leaf.append((lx + ex * math.cos(la) - ey * math.sin(la), ly + ex * math.sin(la) + ey * math.cos(la)))
            _poly(d, [T(x, y) for x, y in leaf])
        for k in range(4):  # twigs to the hand
            a = math.radians(60 + 20 * k)
            x0, y0 = T(0, 0.35)
            x1, y1 = T(0.25 * math.cos(a + math.pi), -0.25 * math.sin(a))
            _capsule(d, (x0, y0), (x1, y1), s * 0.018)
    elif shape == "hand":  # a big hand entering from an edge; anchor = wrist, s = length, rot 0 = fingers up
        _poly(d, [T(x, y) for x, y in [(-0.17, 0.1), (0.17, 0.1), (0.2, -0.35), (-0.2, -0.35)]])
        for fx, ln, ang in ((-0.15, 0.42, -10), (-0.05, 0.55, -3), (0.05, 0.58, 2), (0.15, 0.48, 9)):
            a = math.radians(ang)
            p = (fx, -0.3)
            q = (fx + math.sin(a) * ln, -0.3 - math.cos(a) * ln)
            x0, y0 = T(*p)
            x1, y1 = T(*q)
            _capsule(d, (x0, y0), (x1, y1), s * 0.085)
        x0, y0 = T(0.18, -0.05)
        x1, y1 = T(0.42, -0.32)
        _capsule(d, (x0, y0), (x1, y1), s * 0.09)
    else:
        raise KeyError(f"unknown prop shape {shape!r}")


# --------------------------------------------------------------------------- backdrops

BACKDROPS = {
    # vertical gradient stops (position 0 = top of screen, 1 = bottom), RGB 0-255; measured on the reference
    # act and then pushed toward a projected-gel look. `spot` adds a radial light pool.
    "dawn-green":  {"stops": [(0, (34, 52, 140)), (0.42, (104, 150, 214)), (0.72, (178, 214, 70)), (1, (64, 120, 38))], "clouds": 0.10},
    "night-blue":  {"stops": [(0, (30, 20, 120)), (0.45, (108, 160, 226)), (1, (150, 186, 250))], "clouds": 0.12},
    "teal-mist":   {"stops": [(0, (46, 76, 118)), (0.35, (74, 114, 138)), (0.65, (96, 144, 136)), (1, (140, 184, 182))], "clouds": 0.14},
    "crimson-spot": {"stops": [(0, (70, 6, 34)), (1, (110, 12, 40))], "clouds": 0.05,
                     "spot": {"x": 0.5, "y": 0.42, "r": 0.42, "color": (236, 238, 255)}},
    "desert-amber": {"stops": [(0, (60, 30, 90)), (0.4, (214, 110, 70)), (0.7, (250, 196, 110)), (1, (220, 150, 80))], "clouds": 0.08},
    "moon-indigo":  {"stops": [(0, (10, 12, 60)), (0.5, (40, 48, 128)), (1, (88, 110, 190))], "clouds": 0.09,
                     "spot": {"x": 0.68, "y": 0.22, "r": 0.2, "color": (210, 220, 255)}},
}


def _gradient(h, w, stops):
    ys = np.linspace(0, 1, h, dtype=np.float32)
    out = np.zeros((h, 3), np.float32)
    pos = [s[0] for s in stops]
    for ch in range(3):
        out[:, ch] = np.interp(ys, pos, [s[1][ch] for s in stops])
    return np.repeat(out[:, None, :] / 255.0, w, axis=1)


def _noise(h, w, seed, octaves=4):
    rng = np.random.default_rng(seed)
    acc = np.zeros((h, w), np.float32)
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        gh, gw = max(2, h // (64 >> o)), max(2, w // (64 >> o))
        g = (rng.random((gh, gw)) * 255).astype(np.uint8)
        up = np.asarray(Image.fromarray(g).resize((w, h), Image.BICUBIC), np.float32) / 255.0
        acc += up * amp
        tot += amp
        amp *= 0.5
    acc /= tot
    return (acc - acc.mean()) / (acc.std() + 1e-6)


# --------------------------------------------------------------------------- renderer


@dataclass
class Frame:
    rgb: np.ndarray  # HxWx3 uint8


class ShadowRenderer:
    def __init__(self, spec: dict):
        self.spec = spec
        self.W, self.H = int(spec.get("width", 1080)), int(spec.get("height", 1920))
        self.fps = float(spec.get("fps", 30))
        self.seed = int(spec.get("seed", 7))
        sc = spec.get("screen", {})
        m = float(sc.get("margin", 0.045))
        mx = int(self.W * m)
        self.sx0, self.sy0 = mx, int(self.H * float(sc.get("top", m * 1.6)))
        self.sx1, self.sy1 = self.W - mx, self.H - int(self.H * float(sc.get("bottom", m * 1.6)))
        self.sw, self.sh = self.sx1 - self.sx0, self.sy1 - self.sy0
        self.hw, self.hh = self.W // 2, self.H // 2  # work resolution for masks
        self.leak = float(spec.get("shadow_leak", 0.05))
        self.blur_base = float(spec.get("penumbra", 1.2))
        self._screen = self._screen_mask(float(sc.get("radius", 0.07)))
        self._bd_cache: dict = {}
        self._stage = np.array(spec.get("stage_color", (5, 5, 14)), np.float32) / 255.0
        yy, xx = np.mgrid[0:self.H, 0:self.W].astype(np.float32)
        self._u = (xx - self.sx0) / self.sw
        self._v = (yy - self.sy0) / self.sh
        r2 = ((self._u - 0.5) / 0.75) ** 2 + ((self._v - 0.48) / 0.75) ** 2
        self._hotspot = np.clip(1.08 - 0.42 * r2, 0.45, 1.1)[..., None]
        cl = _noise(max(8, self.H // 3), max(8, self.W // 10), self.seed)  # wide, flat cloud banks
        cl = ((cl * 0.18 + 0.5).clip(0, 1) * 255).astype(np.uint8)
        self._clouds = np.asarray(Image.fromarray(cl).resize((self.W, self.H), Image.BICUBIC), np.float32) / 255.0

    # screen geometry --------------------------------------------------
    def _screen_mask(self, radius):
        img = Image.new("L", (self.W, self.H), 0)
        r = int(min(self.sw, self.sh) * radius)
        ImageDraw.Draw(img).rounded_rectangle([self.sx0, self.sy0, self.sx1, self.sy1], radius=r, fill=255)
        img = img.filter(ImageFilter.GaussianBlur(max(2, self.W // 220)))
        return (np.asarray(img, np.float32) / 255.0)[..., None]

    def to_px(self, x, y, work=True):
        k = 0.5 if work else 1.0
        return (self.sx0 + x * self.sw) * k, (self.sy0 + y * self.sh) * k

    # backdrop -----------------------------------------------------------
    def backdrop(self, scene: dict, t_local: float) -> np.ndarray:
        name = scene.get("backdrop", "night-blue")
        preset = dict(BACKDROPS[name]) if isinstance(name, str) else dict(name)
        key = name if isinstance(name, str) else id(scene)
        if key not in self._bd_cache:
            base = np.zeros((self.H, self.W, 3), np.float32)
            g = _gradient(self.sh, self.sw, preset["stops"])
            base[self.sy0:self.sy1, self.sx0:self.sx1] = g
            self._bd_cache[key] = base
        img = self._bd_cache[key].copy()
        spot = scene.get("spot", preset.get("spot"))
        if spot:
            r = spot["r"]
            if "r_keys" in spot:
                r = sample_keys(spot["r_keys"], t_local).get("scale", r)
            col = np.array(spot.get("color", (236, 238, 255)), np.float32) / 255.0
            dist = np.sqrt(((self._u - spot["x"]) * self.sw / self.sh) ** 2 + (self._v - spot["y"]) ** 2)
            pool = np.clip(1 - (dist / max(1e-3, r)) ** 2, 0, 1) ** 1.3
            img = img * (1 - pool[..., None]) + col * pool[..., None]
        amt = float(scene.get("clouds", preset.get("clouds", 0.1)))
        if amt:
            drift = int(t_local * float(scene.get("cloud_speed", 14))) % self._clouds.shape[1]
            c = np.roll(self._clouds, -drift, axis=1)
            img = img * (1 + (c[..., None] - 0.5) * 2 * amt * 2.2)
        return img

    # silhouettes --------------------------------------------------------
    def actor_layer(self, actor: dict, t_local: float):
        k = sample_keys(actor.get("keys", [{"t": 0}]), t_local)
        if k.get("opacity", 1.0) <= 0.003:
            return None, 0.0, 0.0
        depth = float(k.get("depth", actor.get("depth", 0.0)))
        grow = 1.0 + 2.2 * depth  # closer to the lamp -> bigger shadow
        img = Image.new("L", (self.W, self.H), 0)  # drawn at full res, then halved (antialias)
        x, y = float(k.get("x", 0.5)), float(k.get("y", 0.93))
        # growth is around the light's axis (centre of screen), the way a real lamp projects
        lx = float(self.spec.get("lamp", {}).get("x", 0.5))
        if depth:  # the shadow spreads away from the lamp axis sideways and grows upward from the floor line
            x = lx + (x - lx) * grow
        px, py = self.to_px(x, y, work=False)
        if actor.get("type", "human") == "human":
            h = float(k.get("height", actor.get("height", 0.42))) * self.sh * grow * float(k.get("scale", 1.0))
            pose = mix_pose(k.get("_pose_mix", (actor.get("pose"), actor.get("pose"), 0)))
            pose = apply_cycle(pose, actor.get("cycle"), t_local)
            facing = int(k.get("facing", actor.get("facing", 1)))
            draw_body(ImageDraw.Draw(img), px, py, pose, actor.get("costume", "plain"), h, facing, actor.get("grounded", True))
        else:
            s = float(k.get("scale", actor.get("scale", 0.2))) * self.sh * grow
            draw_prop(img, actor["shape"], px, py, s, float(k.get("rot", 0)), t_local, actor.get("params", {}))
        img = img.resize((self.hw, self.hh), Image.BILINEAR)
        blur = self.blur_base + depth * float(self.spec.get("depth_blur", 12))
        blur += float(actor.get("blur", 0))
        if blur > 0.3:
            img = img.filter(ImageFilter.GaussianBlur(blur))
        return np.asarray(img, np.float32) / 255.0, float(k.get("opacity", 1.0)), depth

    def iris_mask(self, scene: dict, t_local: float):
        iris = scene.get("iris")
        if not iris:
            return None
        k = sample_keys(iris["keys"], t_local)
        sc = float(k.get("scale", 3.0))
        if sc >= 2.9:
            return None
        img = Image.new("L", (self.hw, self.hh), 0)
        cx, cy = self.to_px(float(iris.get("x", 0.5)), float(iris.get("y", 0.5)))
        s = sc * self.sh * 0.5
        if s > 0.5:
            pts = [(cx + px * s, cy + py * s) for px, py in shape_points(iris.get("shape", "circle"))]
            ImageDraw.Draw(img).polygon(pts, fill=255)
        img = img.filter(ImageFilter.GaussianBlur(float(iris.get("soft", 2.5))))
        return np.asarray(img.resize((self.W, self.H), Image.BILINEAR), np.float32)[..., None] / 255.0

    def scene_at(self, t: float):
        for s in self.spec["scenes"]:
            if s["start"] <= t < s["end"]:
                return s
        return self.spec["scenes"][-1]

    def light_level(self, scene: dict, t: float) -> float:
        fi, fo = float(scene.get("fade_in", 0.5)), float(scene.get("fade_out", 0.5))
        a = 1.0
        if fi > 0:
            a = min(a, (t - scene["start"]) / fi)
        if fo > 0:
            a = min(a, (scene["end"] - t) / fo)
        return float(EASES["smooth"](min(1.0, max(0.0, a))))

    def render(self, t: float) -> Frame:
        scene = self.scene_at(t)
        tl = t - scene["start"]
        bd = self.backdrop(scene, tl)
        shadow = np.zeros((self.hh, self.hw), np.float32)
        for actor in scene.get("actors", []):
            m, op, _ = self.actor_layer(actor, tl)
            if m is not None:
                np.maximum(shadow, m * op, out=shadow)
        sh = np.asarray(Image.fromarray((shadow * 255).astype(np.uint8)).resize((self.W, self.H), Image.BILINEAR), np.float32)[..., None] / 255.0
        lit = bd * self._hotspot * (1 - sh * (1 - self.leak))
        light = self.light_level(scene, t)
        iris = self.iris_mask(scene, tl)
        lmask = self._screen * light
        if iris is not None:
            lmask = lmask * iris
        # unlit screen is not pure black: a faint cloth tone, like the real screen between cues
        cloth = self._screen * np.array((0.035, 0.035, 0.07), np.float32)
        out = lit * lmask + cloth * (1 - lmask) + self._stage * (1 - self._screen)
        rng = np.random.default_rng(int(t * self.fps) + self.seed)
        grain = rng.normal(0, float(self.spec.get("grain", 0.006)), (self.hh, self.hw)).astype(np.float32)
        grain = np.repeat(np.repeat(grain, 2, 0), 2, 1)[: self.H, : self.W, None]
        out = np.clip(out + grain, 0, 1)
        return Frame((out * 255 + 0.5).astype(np.uint8))
