"""CAM-71 rotation coverage rule as a program: the zoom that hides black corners when the frame rolls."""
from __future__ import annotations
import math
from pathlib import Path
from ._mind_common import save, eq, truth


def need_zoom(roll_deg: float, w: int, h: int) -> float:
    """Exact minimum zoom so a w x h frame rotated by roll still covers the w x h canvas."""
    r = math.radians(abs(roll_deg))
    c, s = math.cos(r), math.sin(r)
    return max((w * c + h * s) / w, (w * s + h * c) / h)


def card_rule(roll_deg: float, w: int, h: int, z: float = 1.0) -> float:
    """The card's shipped approximation: need = |cos r| + q*|sin r|*0.56, q = long/short side."""
    r = math.radians(roll_deg)
    q = max(w, h) / min(w, h)
    return max(z, abs(math.cos(r)) + q * abs(math.sin(r)) * 0.56)


def covered(roll_deg, w, h, z, n=64):
    """Rotate canvas corners into source space and check they stay inside the zoomed source."""
    r = math.radians(roll_deg)
    for cx, cy in [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]:
        x = (cx * math.cos(r) + cy * math.sin(r)) / z
        y = (-cx * math.sin(r) + cy * math.cos(r)) / z
        if abs(x) > w / 2 + 1e-9 or abs(y) > h / 2 + 1e-9:
            return False
    return True


def cam71(work):
    rows = []
    for w, h in [(1920, 1080), (1080, 1920)]:
        for roll in [0, 2, 5, 8, 12]:
            exact = need_zoom(roll, w, h)
            rule = card_rule(roll, w, h)
            rows.append({"size": f"{w}x{h}", "roll": roll, "exact": exact, "card_rule": rule,
                         "exact_covers": covered(roll, w, h, exact * (1 + 1e-9)),
                         "rule_covers": covered(roll, w, h, rule),
                         "below_exact_fails": roll == 0 or not covered(roll, w, h, exact * 0.98)})
    save(work, "rotation_coverage.json", rows)
    return [eq("no roll needs no zoom", need_zoom(0, 1920, 1080), 1.0),
            truth("exact zoom covers every case", all(r["exact_covers"] for r in rows)),
            truth("2% under the exact zoom shows a black corner", all(r["below_exact_fails"] for r in rows)),
            # Audit of the card's shipped 0.56 shortcut: it under-zooms (black corners) once the frame rolls.
            # The program applies the exact zoom instead and records the shortfall as a finding.
            truth("card shortcut audited: under-zooms at 5 deg on 16:9 (finding)",
                  not next(r for r in rows if r["size"] == "1920x1080" and r["roll"] == 5)["rule_covers"],
                  [(r["size"], r["roll"], round(r["card_rule"], 3), round(r["exact"], 3)) for r in rows if r["roll"]]),
            eq("exact zoom at 5 deg, 16:9", round(need_zoom(5, 1920, 1080), 4), 1.1511)]


PROGRAMS = {"CAM-71": cam71}
