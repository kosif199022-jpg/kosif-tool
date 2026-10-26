"""The plush bunny's structural twin: a 3D pin-jointed truss whose nodes sit on the bunny's anatomy (feet, pelvis,
chest, neck, skull, ear bases, ear tips), solved with structural_twin.py (3D).

Illustrative only: the member areas and the "plush" stiffness/strength are chosen values, NOT measured from a toy.
The rig transforms here mirror shape-kit.js bunny(): head pivot at NECK, ear pivots at EAR_* with Euler XYZ rotation.

    python build_truss.py            → twin/model.json, twin/report.json, assets/twin.js (window.TWIN for the film)
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))                      # scripts/
import structural_twin as st  # noqa: E402

NECK = (0.0, 0.152, 0.004)
EARS = {"L": ((-0.03, 0.123, -0.014), (-0.12, 0.0, 0.2)), "R": ((0.03, 0.123, -0.014), (-0.12, 0.0, -0.2))}


def rot_xyz(v, r):
    """three.js Euler 'XYZ': M = Rx · Ry · Rz, applied to a column vector."""
    x, y, z = v
    a, b, c = r
    x, y = x * math.cos(c) - y * math.sin(c), x * math.sin(c) + y * math.cos(c)          # Rz
    x, z = x * math.cos(b) + z * math.sin(b), -x * math.sin(b) + z * math.cos(b)         # Ry
    y, z = y * math.cos(a) - z * math.sin(a), y * math.sin(a) + z * math.cos(a)          # Rx
    return (x, y, z)


def add(a, b):
    return tuple(p + q for p, q in zip(a, b))


nodes, part = {}, {}


def node(name, p, owner="body"):
    nodes[name] = [round(v, 6) for v in p]
    part[name] = owner


# ground contact (pinned) and the body
for n, p in {"footL": (-0.04, 0.0, 0.06), "footR": (0.04, 0.0, 0.06), "seatL": (-0.055, 0.0, -0.005),
             "seatR": (0.055, 0.0, -0.005), "seatB": (0.0, 0.0, -0.045)}.items():
    node(n, p)
for n, p in {"hipL": (-0.05, 0.06, 0.012), "hipR": (0.05, 0.06, 0.012), "belly": (0.0, 0.062, 0.062), "back": (0.0, 0.07, -0.055),
             "ribL": (-0.045, 0.128, 0.002), "ribR": (0.045, 0.128, 0.002), "chest": (0.0, 0.124, 0.05), "spine": (0.0, 0.13, -0.042),
             "pawL": (-0.03, 0.084, 0.066), "pawR": (0.03, 0.084, 0.066), "neck": (0.0, 0.162, 0.004)}.items():
    node(n, p)
# head (head-local + NECK)
for n, p in {"jawL": (-0.062, 0.06, 0.0), "jawR": (0.062, 0.06, 0.0), "snout": (0.0, 0.05, 0.072), "nape": (0.0, 0.075, -0.062),
             "cheekL": (-0.04, 0.035, 0.05), "cheekR": (0.04, 0.035, 0.05), "crown": (0.0, 0.135, 0.0),
             "browL": (-0.04, 0.11, 0.035), "browR": (0.04, 0.11, 0.035)}.items():
    node(n, add(NECK, p), "head")
# ears (ear-local → head-local → world)
for s, (piv, r) in EARS.items():
    for n, p in {"in": (0.012 if s == "L" else -0.012, 0.0, 0.0), "out": (-0.012 if s == "L" else 0.012, 0.0, 0.0),
                 "front": (0.0, 0.002, 0.011), "mid": (0.0, 0.07, 0.0), "tip": (0.0, 0.13, 0.0)}.items():
        node(f"ear{s}_{n}", add(NECK, add(piv, rot_xyz(p, r))), f"ear{s}")

# members: anatomy first, then nearest-neighbour bracing inside each region
bars: list[tuple[str, str]] = []


def bar(a, b):
    if a != b and (a, b) not in bars and (b, a) not in bars:
        bars.append((a, b))


ground = ["footL", "footR", "seatL", "seatR", "seatB"]
for g in ground:
    for b in ("hipL", "hipR", "belly", "back"):
        if math.dist(nodes[g], nodes[b]) < 0.11:
            bar(g, b)
ring1, ring2 = ["hipL", "belly", "hipR", "back"], ["ribL", "chest", "ribR", "spine"]
for ring in (ring1, ring2):
    for i in range(4):
        bar(ring[i], ring[(i + 1) % 4])
    bar(ring[0], ring[2]); bar(ring[1], ring[3])
for i in range(4):
    bar(ring1[i], ring2[i]); bar(ring1[i], ring2[(i + 1) % 4])
for n in ring2:
    bar(n, "neck")
for s in "LR":
    bar(f"paw{s}", "chest"); bar(f"paw{s}", f"rib{s}"); bar(f"paw{s}", "belly"); bar(f"paw{s}", f"hip{s}")
head = ["jawL", "jawR", "snout", "nape", "cheekL", "cheekR", "crown", "browL", "browR"]
for h in ("jawL", "jawR", "snout", "nape", "cheekL", "cheekR"):
    bar("neck", h)
for h in ("jawL", "jawR", "nape", "chest", "spine"):
    pass
bar("ribL", "jawL"); bar("ribR", "jawR"); bar("chest", "cheekL"); bar("chest", "cheekR"); bar("spine", "nape")


def knn(names, k):
    for a in names:
        for b in sorted((n for n in names if n != a), key=lambda n: math.dist(nodes[a], nodes[n]))[:k]:
            bar(a, b)


knn(head, 4)
for s in "LR":
    e = [f"ear{s}_{n}" for n in ("in", "out", "front")]
    for i in range(3):
        bar(e[i], e[(i + 1) % 3])
    for b in e:
        bar(b, f"ear{s}_mid"); bar(b, "crown")
    bar(f"ear{s}_out", f"brow{s}"); bar(f"ear{s}_in", "nape"); bar(f"ear{s}_front", f"brow{s}")
    bar(f"ear{s}_mid", f"ear{s}_tip"); bar(f"ear{s}_front", f"ear{s}_tip"); bar(f"ear{s}_out", f"ear{s}_tip"); bar(f"ear{s}_in", f"ear{s}_tip")

PLUSH = {"young_pa": 8.0e6, "strength_pa": 2.0e6}           # illustrative felt-and-stuffing proxy, not measured


def area(a, b):
    if a.startswith("ear") and b.startswith("ear"):
        return 3.4e-5 if ("_mid" in a + b or "_tip" in a + b) else 4.2e-5      # thin ear "cartilage"
    if a.startswith("ear") or b.startswith("ear"):
        return 4.0e-5                                                           # ear roots into the skull
    return 1.2e-4


elements = [{"id": f"{a}-{b}", "a": a, "b": b, "area_m2": area(a, b), **PLUSH} for a, b in bars]
model = {"name": "Plush bunny — illustrative 3D space-truss proxy (values chosen, not measured)",
         "units": {"length": "m", "force": "N", "stress": "Pa"}, "nodes": nodes,
         "supports": {g: ["x", "y", "z"] for g in ground}, "elements": elements,
         "loads": [{"node": "crown", "fy_n": -1.9},                             # a gentle pat on the head
                   {"node": "earL_tip", "fx_n": -0.12, "fz_n": -0.048},         # a poke on the left ear
                   {"node": "earR_tip", "fx_n": 0.032}]}

if __name__ == "__main__":
    base = st.analyse(model)
    weakest = base["ranked_failure_modes"][0]
    swap_changes = {"area_m2": round(weakest["area_m2"] * 2.6, 9)}
    rep = st.report(model, weakest["id"], swap_changes, fracture_scale=float(sys.argv[1]) if len(sys.argv) > 1 else 3.0)
    rep["parts"] = part
    (HERE / "model.json").write_text(json.dumps(model, indent=1), encoding="utf-8")
    (HERE / "report.json").write_text(json.dumps(rep, indent=1, allow_nan=False), encoding="utf-8")
    film = {"model": {"nodes": nodes, "elements": [{"id": e["id"], "a": e["a"], "b": e["b"]} for e in elements], "loads": model["loads"]},
            "parts": part, "first": base["first_failure_multiplier"], "after_first": rep["swap"]["after"]["first_failure_multiplier"],
            "util": {m["id"]: m["utilization"] for m in base["members"]},
            "util_after": {m["id"]: m["utilization"] for m in rep["swap"]["after"]["members"]},
            "rank": [[m["id"], m["failure_load_multiplier"], m["mode"]] for m in base["ranked_failure_modes"][:3]],
            "rank_after": [[m["id"], m["failure_load_multiplier"], m["mode"]] for m in rep["swap"]["after"]["ranked_failure_modes"][:3]],
            "break": rep["hypothetical_failure_path"], "swap": {"id": rep["swap"]["element_id"], "changes": rep["swap"]["changes"], "factor": round(swap_changes["area_m2"] / weakest["area_m2"], 3)},
            "triangles_note": "measured in the page", "source": "structural_twin.py v0.2 (3D) — illustrative values, not a measured toy"}
    (HERE.parent / "assets" / "twin.js").write_text("window.TWIN = " + json.dumps(film, separators=(",", ":"), allow_nan=False) + ";\n", encoding="utf-8")
    after = rep["swap"]["after"]
    print(json.dumps({"nodes": len(nodes), "members": len(elements), "first_limit": base["first_failure_multiplier"],
                      "weakest": [(m["id"], m["failure_load_multiplier"]) for m in base["ranked_failure_modes"][:4]],
                      "break": rep["hypothetical_failure_path"]["steps"],
                      "swap": weakest["id"], "after_first_limit": after["first_failure_multiplier"],
                      "after_weakest": [(m["id"], m["failure_load_multiplier"]) for m in after["ranked_failure_modes"][:4]]}, indent=1))
