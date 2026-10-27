#!/usr/bin/env python3
"""Overlapping null-camera rig: AE-style eases, camera path and an overlap checker.

The camera never moves by itself. Each move is one null with two keys on one
axis; the camera position is the sum of the eased null offsets. The next null
must start while the previous one is in its slow tail (83-95% of its distance
done), so the combined camera speed never drops to zero mid-comp.

Technique credit: Fares Toson ("Fares Motion" / pro-motion). See
playbooks/overlap-camera.md. Code written fresh for KOSIF (MIT).

Usage:
  python3 tools/overlap_rig.py graphs
  python3 tools/overlap_rig.py check [rig.json] [--json]
  python3 tools/overlap_rig.py css OUT IN

rig.json: {"nulls": [{"axis": "x", "d": -544, "f0": 0, "f1": 40, "graph": [0.0001, 1]}, ...]}
Without a file, `check` runs on the reference rig.
"""
import argparse
import json
import sys

# name: (out influence, in influence, feel)
GRAPHS = {
    "sharpEnd": (1.0, 0.35, "slow start, charges up, peak near 78% of the time"),
    "sharpMid": (0.7, 0.75, "soft ends, whip in the middle (section-to-section moves)"),
    "sharpStartHard": (0.0001, 1.0, "fires from frame 0, glides to rest (entrances, opening move)"),
    "sharpStartSoft": (0.32, 1.0, "quick start without the hit, long settle"),
    "sharpEndHard": (1.0, 0.0001, "slow all the way, slams in on the last frames (closing move)"),
}

REFERENCE_RIG = [
    {"axis": "x", "d": -544, "f0": 0, "f1": 40, "graph": [0.0001, 1]},
    {"axis": "x", "d": -1290, "f0": 20, "f1": 73, "graph": [0.747, 0.793]},
    {"axis": "x", "d": -1470, "f0": 60, "f1": 109, "graph": [0.727, 0.822]},
    {"axis": "x", "d": -447, "f0": 89, "f1": 119, "graph": [1, 0.0001]},
]

# The overlap window: start the next null when the previous one has done this share of its distance.
OVERLAP_MIN, OVERLAP_MAX = 0.80, 0.97


def _bez(a, b, t):
    return 3 * (1 - t) * (1 - t) * t * a + 3 * (1 - t) * t * t * b + t * t * t


def ae_ease(out, inf, p):
    """AE two-key ease, speed 0 at both keys. p = time progress 0..1 -> value progress 0..1."""
    if p <= 0:
        return 0.0
    if p >= 1:
        return 1.0
    lo, hi = 0.0, 1.0
    for _ in range(50):
        t = (lo + hi) / 2
        if _bez(out, 1 - inf, t) < p:
            lo = t
        else:
            hi = t
    return _bez(0, 1, (lo + hi) / 2)


def css(out, inf):
    return f"cubic-bezier({out:g}, 0, {1 - inf:g}, 1)"


def null_progress(n, f):
    span = max(1, n["f1"] - n["f0"])
    return ae_ease(n["graph"][0], n["graph"][1], (f - n["f0"]) / span)


def cam_at(nulls, f, base=(0.0, 0.0, 0.0)):
    c = list(base)
    for n in nulls:
        c["xyz".index(n["axis"])] += n["d"] * null_progress(n, f)
    return c


def speed(nulls, f, step=1.0):
    a, b = cam_at(nulls, f), cam_at(nulls, f + step)
    return sum((y - x) ** 2 for x, y in zip(a, b)) ** 0.5 / step


def check(nulls):
    """Return a report dict: per-handoff overlap and the combined speed profile."""
    issues = []
    for i, n in enumerate(nulls):
        if n["axis"] not in "xyz" or len(n["axis"]) != 1:
            issues.append(f"null {i + 1}: axis must be x, y or z")
        if n["f1"] <= n["f0"]:
            issues.append(f"null {i + 1}: f1 must be after f0")
    if issues:
        return {"ok": False, "issues": issues, "handoffs": []}
    order = sorted(nulls, key=lambda n: n["f0"])
    handoffs = []
    for i in range(1, len(order)):
        prev, nxt = order[i - 1], order[i]
        done = null_progress(prev, nxt["f0"])
        frames = prev["f1"] - nxt["f0"]
        entry = {"from": i, "to": i + 1, "prev_done": round(done, 3), "overlap_frames": frames}
        if frames <= 0:
            issues.append(f"null {i + 1} starts at {nxt['f0']} after null {i} ended at {prev['f1']}: the camera stops")
        elif not OVERLAP_MIN <= done <= OVERLAP_MAX:
            issues.append(
                f"null {i + 1} starts when null {i} is {done:.0%} done; aim for 83-95% (slow tail)"
            )
        handoffs.append(entry)
    first, last = order[0]["f0"], max(n["f1"] for n in order)
    speeds = [speed(order, f) for f in range(first, last - 1)]
    stall = min(speeds) if speeds else 0.0
    if speeds and stall < 0.5:
        issues.append(f"combined camera speed drops to {stall:.2f}px/frame inside the rig: it reads as a stop")
    return {
        "ok": not issues,
        "issues": issues,
        "handoffs": handoffs,
        "min_speed": round(stall, 2),
        "peak_speed": round(max(speeds), 2) if speeds else 0.0,
        "frames": [first, last],
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("graphs", help="list the five speed graphs with their CSS cubic-bezier")
    c = sub.add_parser("check", help="check a rig for overlap and camera stops")
    c.add_argument("rig", nargs="?")
    c.add_argument("--json", action="store_true")
    k = sub.add_parser("css", help="AE influences (0..1) -> CSS cubic-bezier")
    k.add_argument("out", type=float)
    k.add_argument("inf", type=float)
    a = ap.parse_args(argv)

    if a.cmd == "graphs":
        for name, (o, i, feel) in GRAPHS.items():
            print(f"{name:15} out {o:<7g} in {i:<7g} {css(o, i):34} {feel}")
        return 0
    if a.cmd == "css":
        print(css(a.out, a.inf))
        return 0
    nulls = REFERENCE_RIG
    if a.rig:
        with open(a.rig, encoding="utf-8") as fh:
            nulls = json.load(fh)["nulls"]
    rep = check(nulls)
    if a.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        for h in rep["handoffs"]:
            print(f"null {h['from']} -> {h['to']}: previous {h['prev_done']:.0%} done, overlap {h['overlap_frames']} frames")
        if "min_speed" in rep:
            print(f"camera speed: min {rep['min_speed']} px/frame, peak {rep['peak_speed']} px/frame")
        print("OK" if rep["ok"] else "FAIL")
        for s in rep["issues"]:
            print("  - " + s)
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
