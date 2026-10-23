#!/usr/bin/env python3
"""Motion physics: springs, CSS cubic-bezier, staggers and keyframe sampling per frame / فيزياء الحركة.

Deterministic numbers a motion scene can paste in, for HTML/SVG, Remotion, Manim or After Effects expressions:

    python3 scripts/motion_physics.py spring --from 0 --to 1 [--stiffness 170 --damping 26 --mass 1 --velocity 0] [--fps 30] [--css NAME]
    python3 scripts/motion_physics.py bezier 0.25 0.1 0.25 1 [--frames 30]        # CSS cubic-bezier, solved like a browser
    python3 scripts/motion_physics.py stagger --count 12 --each 0.06 [--from center|first|last|edges|<index>] [--grid 4x3] [--ease out]
    python3 scripts/motion_physics.py keyframes --track "0:0,0.5:120,1.2:100" [--ease "cubic-bezier(.2,.8,.2,1)"] [--fps 30]
    python3 scripts/motion_physics.py --self-test

spring integrates a damped spring (mass, stiffness, damping, initial velocity) with a fixed sub-step and reports every
frame until it settles, the settle time and the overshoot; with --css it prints @keyframes. The spring parameters
follow react-spring's tension/friction model (MIT), the stagger options follow anime.js (MIT), and the bezier solver
follows the CSS easing definition; all code here is our own. Python 3.8+ standard library only.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys

NAMED = {  # CSS named easings as cubic-bezier control points
    "linear": (0.0, 0.0, 1.0, 1.0), "ease": (0.25, 0.1, 0.25, 1.0), "ease-in": (0.42, 0.0, 1.0, 1.0),
    "ease-out": (0.0, 0.0, 0.58, 1.0), "ease-in-out": (0.42, 0.0, 0.58, 1.0),
    "in": (0.42, 0.0, 1.0, 1.0), "out": (0.0, 0.0, 0.58, 1.0), "in-out": (0.42, 0.0, 0.58, 1.0),
    "out-expo": (0.16, 1.0, 0.3, 1.0), "out-back": (0.34, 1.56, 0.64, 1.0), "in-out-cubic": (0.65, 0.0, 0.35, 1.0),
}


# ------------------------------------------------------------------ cubic-bezier
def bezier(x1: float, y1: float, x2: float, y2: float):
    """Return f(x) -> y for a CSS cubic-bezier(x1, y1, x2, y2); x1 and x2 must be in [0, 1]."""
    if not (0 <= x1 <= 1 and 0 <= x2 <= 1):
        raise ValueError("cubic-bezier x values must be within 0..1")

    def coord(t, a, b):
        return 3 * a * t * (1 - t) ** 2 + 3 * b * t * t * (1 - t) + t ** 3

    def dcoord(t, a, b):
        return 3 * a * (1 - t) ** 2 + 6 * (b - a) * t * (1 - t) + 3 * (1 - b) * t * t

    def solve_t(x):
        t = x
        for _ in range(8):  # Newton
            err = coord(t, x1, x2) - x
            if abs(err) < 1e-7:
                return t
            d = dcoord(t, x1, x2)
            if abs(d) < 1e-6:
                break
            t -= err / d
        lo, hi, t = 0.0, 1.0, x  # bisection fallback
        for _ in range(60):
            v = coord(t, x1, x2)
            if abs(v - x) < 1e-7:
                break
            lo, hi = (t, hi) if v < x else (lo, t)
            t = (lo + hi) / 2
        return t

    def f(x):
        if x <= 0:
            return 0.0
        if x >= 1:
            return 1.0
        return coord(solve_t(x), y1, y2)
    return f


def parse_ease(spec: str):
    s = (spec or "linear").strip().lower()
    if s in NAMED:
        return bezier(*NAMED[s])
    m = re.fullmatch(r"cubic-bezier\(\s*([-\d.]+)\s*,\s*([-\d.]+)\s*,\s*([-\d.]+)\s*,\s*([-\d.]+)\s*\)", s)
    if m:
        return bezier(*(float(g) for g in m.groups()))
    m = re.fullmatch(r"steps\(\s*(\d+)\s*\)", s)
    if m:
        n = int(m.group(1))
        return lambda x: min(1.0, math.floor(max(0.0, x) * n) / n) if x < 1 else 1.0
    raise ValueError(f"unknown easing: {spec} (named: {', '.join(sorted(NAMED))}, cubic-bezier(a,b,c,d), steps(n))")


# ------------------------------------------------------------------ spring
def spring(frm: float, to: float, stiffness: float = 170.0, damping: float = 26.0, mass: float = 1.0, velocity: float = 0.0,
           fps: int = 30, rest: float = 0.001, max_seconds: float = 10.0) -> dict:
    if mass <= 0 or stiffness <= 0 or damping < 0 or fps <= 0:
        raise ValueError("mass and stiffness must be > 0, damping >= 0, fps > 0")
    span = (to - frm) or 1.0
    x, v = frm, velocity
    sub = 16
    dt = 1.0 / fps / sub
    frames, settled_at, peak = [round(x, 6)], None, frm
    max_frames = int(max_seconds * fps)
    for i in range(1, max_frames + 1):
        for _ in range(sub):  # semi-implicit Euler
            a = (-stiffness * (x - to) - damping * v) / mass
            v += a * dt
            x += v * dt
        frames.append(round(x, 6))
        peak = max(peak, x) if to >= frm else min(peak, x)
        if abs(x - to) <= rest * abs(span) and abs(v) <= rest * abs(span) * fps:
            settled_at = i
            frames[-1] = round(to, 6)
            break
    zeta = damping / (2 * math.sqrt(stiffness * mass))
    overshoot = max(0.0, (peak - to) / span) if to >= frm else max(0.0, (to - peak) / -span)
    return {"from": frm, "to": to, "stiffness": stiffness, "damping": damping, "mass": mass, "velocity": velocity, "fps": fps,
            "damping_ratio": round(zeta, 4), "regime": "under-damped (bounces)" if zeta < 1 else ("critically damped" if zeta == 1 else "over-damped"),
            "settled": settled_at is not None, "frames": len(frames), "seconds": round((len(frames) - 1) / fps, 4),
            "overshoot_pct": round(100 * overshoot, 2), "values": frames}


def css_keyframes(name: str, values: list, prop: str = "transform", unit_fn=None) -> str:
    unit_fn = unit_fn or (lambda v: f"translateY({v:.3f}px)")
    n = len(values) - 1 or 1
    lines = [f"@keyframes {name} {{"]
    for i, v in enumerate(values):
        lines.append(f"  {100 * i / n:.3f}% {{ {prop}: {unit_fn(v)}; }}")
    lines.append("}")
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------------ stagger
def stagger(count: int, each: float, start: float = 0.0, origin: str = "first", grid: tuple = None, ease: str = "linear") -> list:
    """Delay (seconds) per element. origin: first | last | center | edges | <index>; grid (cols, rows) uses 2-D distance."""
    if count <= 0 or each < 0:
        raise ValueError("count must be > 0 and each >= 0")
    if grid:
        cols, rows = grid
        if cols * rows < count:
            raise ValueError("grid is smaller than count")
        pos = [(i % cols, i // cols) for i in range(count)]
        if origin == "center":
            o = ((cols - 1) / 2, (rows - 1) / 2)
        elif origin == "last":
            o = pos[-1]
        elif origin.isdigit():
            o = pos[int(origin)]
        else:
            o = pos[0]
        dist = [math.hypot(x - o[0], y - o[1]) for x, y in pos]
        if origin == "edges":
            c = ((cols - 1) / 2, (rows - 1) / 2)
            d2 = [math.hypot(x - c[0], y - c[1]) for x, y in pos]
            dist = [max(d2) - d for d in d2]
    else:
        idx = list(range(count))
        if origin == "first":
            dist = [float(i) for i in idx]
        elif origin == "last":
            dist = [float(count - 1 - i) for i in idx]
        elif origin == "center":
            c = (count - 1) / 2
            dist = [abs(i - c) for i in idx]
        elif origin == "edges":
            c = (count - 1) / 2
            dist = [c - abs(i - c) for i in idx]
        elif origin.isdigit():
            o = int(origin)
            if o >= count:
                raise ValueError("origin index out of range")
            dist = [float(abs(i - o)) for i in idx]
        else:
            raise ValueError(f"unknown origin: {origin}")
    top = max(dist) or 1.0
    f = parse_ease(ease)
    return [round(start + f(d / top) * top * each, 6) for d in dist]


# ------------------------------------------------------------------ keyframes
def parse_track(spec: str) -> list:
    pts = []
    for part in spec.split(","):
        t, _, v = part.partition(":")
        pts.append((float(t), float(v)))
    if len(pts) < 2 or any(b[0] <= a[0] for a, b in zip(pts, pts[1:])):
        raise ValueError("a track needs two or more 'time:value' points with increasing times")
    return pts


def sample(track: list, fps: int = 30, ease: str = "linear") -> list:
    f = parse_ease(ease)
    t0, t1 = track[0][0], track[-1][0]
    out = []
    for i in range(int(round((t1 - t0) * fps)) + 1):
        t = t0 + i / fps
        for (a, va), (b, vb) in zip(track, track[1:]):
            if a <= t <= b + 1e-9:
                u = (t - a) / (b - a)
                out.append(round(va + (vb - va) * f(min(1.0, u)), 6))
                break
    return out


def self_test() -> int:
    bad = []
    e = bezier(*NAMED["ease"])
    if abs(e(0.5) - 0.8024) > 0.002:  # CSS 'ease' at x=0.5 ≈ 0.8024
        bad.append(("ease(0.5)", e(0.5)))
    if bezier(0, 0, 1, 1)(0.37) - 0.37 > 1e-6:
        bad.append("linear bezier")
    s = spring(0, 1)
    if not s["settled"] or not (0.4 < s["seconds"] < 1.5) or s["overshoot_pct"] > 1.0:
        bad.append(("default spring", s["seconds"], s["overshoot_pct"]))
    w = spring(0, 100, stiffness=180, damping=8)
    if w["overshoot_pct"] < 20 or w["regime"] != "under-damped (bounces)":
        bad.append(("wobbly", w["overshoot_pct"], w["regime"]))
    if spring(0, 1)["values"] != spring(0, 1)["values"]:
        bad.append("determinism")
    if stagger(5, 0.1) != [0.0, 0.1, 0.2, 0.3, 0.4]:
        bad.append(("stagger first", stagger(5, 0.1)))
    if stagger(5, 0.1, origin="center") != [0.2, 0.1, 0.0, 0.1, 0.2]:
        bad.append(("stagger center", stagger(5, 0.1, origin="center")))
    g = stagger(9, 0.1, origin="center", grid=(3, 3))
    if g[4] != 0.0 or abs(g[0] - g[8]) > 1e-9 or not g[0] > g[1]:
        bad.append(("grid", g))
    k = sample(parse_track("0:0,1:10"), fps=10)
    if len(k) != 11 or k[5] != 5.0:
        bad.append(("keyframes", k))
    if "@keyframes pop" not in css_keyframes("pop", [0, 1]):
        bad.append("css")
    try:
        parse_ease("bogus")
        bad.append("bad ease accepted")
    except ValueError:
        pass
    for b in bad:
        print("FAIL", b)
    print("self-test OK" if not bad else f"self-test: {len(bad)} failure(s)")
    return 1 if bad else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--self-test", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    sp = sub.add_parser("spring")
    sp.add_argument("--from", dest="frm", type=float, default=0.0)
    sp.add_argument("--to", type=float, default=1.0)
    sp.add_argument("--stiffness", type=float, default=170.0, help="react-spring 'tension'")
    sp.add_argument("--damping", type=float, default=26.0, help="react-spring 'friction'")
    sp.add_argument("--mass", type=float, default=1.0)
    sp.add_argument("--velocity", type=float, default=0.0)
    sp.add_argument("--fps", type=int, default=30)
    sp.add_argument("--css", metavar="NAME", help="print @keyframes NAME (translateY px) instead of JSON")
    bz = sub.add_parser("bezier")
    bz.add_argument("points", nargs=4, type=float)
    bz.add_argument("--frames", type=int, default=30)
    st = sub.add_parser("stagger")
    st.add_argument("--count", type=int, required=True)
    st.add_argument("--each", type=float, required=True, help="seconds between neighbours")
    st.add_argument("--start", type=float, default=0.0)
    st.add_argument("--from", dest="origin", default="first")
    st.add_argument("--grid", help="COLSxROWS")
    st.add_argument("--ease", default="linear")
    kf = sub.add_parser("keyframes")
    kf.add_argument("--track", required=True, help="time:value pairs, e.g. 0:0,0.5:120,1.2:100")
    kf.add_argument("--ease", default="linear")
    kf.add_argument("--fps", type=int, default=30)
    a = ap.parse_args(argv)
    try:
        if a.self_test:
            return self_test()
        if a.cmd == "spring":
            r = spring(a.frm, a.to, a.stiffness, a.damping, a.mass, a.velocity, a.fps)
            print(css_keyframes(a.css, r["values"]) if a.css else json.dumps(r, indent=1))
            return 0
        if a.cmd == "bezier":
            f = bezier(*a.points)
            vals = [round(f(i / a.frames), 6) for i in range(a.frames + 1)]
            print(json.dumps({"cubic_bezier": a.points, "frames": a.frames, "values": vals}, indent=1))
            return 0
        if a.cmd == "stagger":
            grid = tuple(int(x) for x in a.grid.lower().split("x")) if a.grid else None
            print(json.dumps({"delays": stagger(a.count, a.each, a.start, a.origin, grid, a.ease)}, indent=1))
            return 0
        if a.cmd == "keyframes":
            vals = sample(parse_track(a.track), a.fps, a.ease)
            print(json.dumps({"fps": a.fps, "frames": len(vals), "values": vals}, indent=1))
            return 0
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
