"""A traced picture (trace.py JSON) as a picture program: a backdrop, then one step per colour layer, largest first,
each growing out from its own centre, the way a sign painter blocks in colours."""
from __future__ import annotations

from render import H0, W0, Hole, Step, fill, lin, rad, rect, translate


def build(data: dict) -> list[Step]:
    w, h = data["size"]
    s = min(1080 / w, 730 / h)
    ox, oy = (W0 - w * s) / 2, (H0 - h * s) / 2

    def T(polys):
        return [(Hole if p["hole"] else list)((ox + x * s, oy + y * s) for x, y in p["pts"]) for p in polys]

    steps = [Step("الخلفية", [fill(rect(0, 0, W0, H0), rad((W0 / 2, H0 / 2 - 20), 760,
                                                         [(0, "#3d3648"), (.6, "#221e2a"), (1, "#121016")]))],
                  "sweep", weight=.9)]
    if data.get("silhouette"):
        sil = T(data["silhouette"])
        steps.append(Step("الظل", [fill(translate(sil, 0, 12), "#000000", .45, blur=18),
                                   fill(sil, lin((0, oy), (0, oy + h * s), [(0, "#ffffff"), (1, "#ffffff")]), .04,
                                        blur=30, mode="add")],
                          "grow", origin=(W0 / 2, H0 / 2), weight=.4))
    for L in data["layers"]:
        cx, cy = L["centre"]
        steps.append(Step(f"اللون {L['name']}", [fill(T(L["polys"]), L["color"])], "grow",
                          origin=(ox + cx * s, oy + cy * s), weight=1.0))
    return steps
