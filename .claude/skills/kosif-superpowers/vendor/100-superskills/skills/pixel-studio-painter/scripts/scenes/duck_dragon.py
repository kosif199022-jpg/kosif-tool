"""بطّة شجاعة في مواجهة تنين عملاق — a small white duck charges a colossal dragon in a night storm.

Low camera behind and beside the duck, looking up. Warm fire light from the dragon against cold storm and moon
light; rain through the flames, steam at the collision zone, frozen a fraction of a second before impact.
16:9 inside letterbox bars. Every shape is vector code, so it renders at any size.
"""
from __future__ import annotations

import math
import random

from dragon_girl import belly_plates, cloud, flame, ridge, spikes, tongue, wing
from render import (Step, dots, ellipse, fill, glow, grade, grain, lin, path, poly, rad, rect, rim, stroke,
                    translate, tube, union, vignette)

TITLE = "بطّة شجاعة في مواجهة تنين عملاق"
TOP, BOTTOM = 62, 738                       # 1200 x 676 = 16:9 between the bars
MOUTH = (694, 262)                          # between the dragon's open jaws
IMPACT = (556, 414)                         # the fire's leading edge: a beat before it reaches the duck
MOON = (150, 128)
DUCK = (262, 578)                           # the duck's body centre


def rain(seed, n, x0, x1, y0, y1, length, width, slant=-0.22):
    r = random.Random(seed)
    lines = []
    for _ in range(n):
        x, y = r.uniform(x0, x1), r.uniform(y0, y1)
        ln = length * r.uniform(.6, 1.3)
        lines.append([(x, y), (x + slant * ln, y + ln)])
    return stroke(lines, width)


def leaf(base, tip, width, bend=0.0, n=10):
    """One feather: a narrow leaf from base to tip, as a single polygon (so it can be outlined)."""
    bx, by = base
    tx, ty = tip
    L = math.hypot(tx - bx, ty - by) or 1
    nx, ny = -(ty - by) / L, (tx - bx) / L
    left, right = [], []
    for k in range(n + 1):
        t = k / n
        w = width * math.sin(math.pi * min(1, t * 1.15)) * (1 - .35 * t)
        cx = bx + (tx - bx) * t + nx * bend * math.sin(math.pi * t)
        cy = by + (ty - by) * t + ny * bend * math.sin(math.pi * t)
        left.append((cx + nx * w / 2, cy + ny * w / 2))
        right.append((cx - nx * w / 2, cy - ny * w / 2))
    return [left + right[::-1]]


def duck_shape():
    """The duck around its body centre (0, 0), facing right: plump body, short thick neck, round head, broad
    spatulate bill, wings raised and spread, mid-stride."""
    body = path("M -104 -4 C -86 -46 -32 -70 24 -66 C 66 -62 92 -40 94 -6 C 96 28 64 54 18 58 "
                "C -32 62 -78 44 -104 -4 Z")
    tail = path("M -98 -8 L -136 -34 L -124 -10 L -140 -14 L -108 8 Z")
    neck = tube([(46, -42), (62, -66), (78, -86)], [32, 27, 25])
    head = path("M 66 -104 C 66 -130 86 -146 108 -146 C 130 -146 144 -132 142 -112 C 140 -94 126 -84 106 -84 "
                "C 84 -84 66 -88 66 -104 Z")
    bill_up = path("M 130 -116 C 148 -122 170 -118 184 -104 C 186 -98 180 -95 172 -96 C 158 -98 142 -100 128 -100 Z")
    bill_lo = path("M 128 -97 C 146 -94 164 -92 176 -88 C 168 -82 150 -82 126 -88 Z")
    eye = ellipse(114, -118, 4.8, 4.8)
    brow = tube([(104, -127), (113, -129.5), (123, -126)], [1.8, 2.1, 1.2], n=4)
    legs = union(tube([(22, 50), (44, 90), (62, 116)], [8, 5.5, 4.2]), tube([(-12, 52), (-36, 86), (-62, 110)], [8, 5.5, 4.2]))
    feet = union(poly([(58, 112), (100, 118), (91, 124), (98, 131), (74, 131), (62, 124)]),
                 poly([(-58, 106), (-92, 110), (-85, 116), (-94, 123), (-68, 123), (-56, 116)]))
    sh, el, wr = (6, -48), (-30, -146), (-20, -238)
    covert = path("M 6 -48 C -8 -112 -28 -176 -20 -238 C -62 -206 -94 -152 -100 -92 C -82 -62 -40 -50 6 -48 Z")
    prim = [(-74, -326), (-104, -308), (-132, -278), (-150, -242), (-162, -206), (-164, -172)]
    second = [(-112, -160), (-118, -128), (-112, -96), (-94, -66)]
    feathers = [leaf((wr[0] - 4 * k, wr[1] + 8 * k), tip, 22 - k, bend=6) for k, tip in enumerate(prim)]
    for k, tip in enumerate(second):
        base = (el[0] + (sh[0] - el[0]) * k / 4, el[1] + (sh[1] - el[1]) * k / 4)
        feathers.append(leaf(base, tip, 26, bend=4))
    far_wing = union(path("M -22 -54 C -44 -124 -74 -194 -100 -250 C -130 -236 -156 -200 -170 -154 "
                          "C -154 -112 -112 -72 -22 -54 Z"),
                     *[leaf((-100, -244), (-124 - 8 * k, -290 + 16 * k), 14, bend=3) for k in range(4)])
    wet = union(tube([(-64, -18), (-20, -8), (34, -12)], [1.2, 1.5, .8], n=5),
                tube([(-54, 14), (0, 22), (44, 14)], [1.2, 1.5, .8], n=5),
                tube([(-82, -2), (-60, 20)], [1, .6], n=3), tube([(20, -40), (40, -20)], [1, .6], n=3))
    return {"body": union(body, tail), "neck": neck, "head": head, "bill_up": bill_up, "bill_lo": bill_lo,
            "eye": eye, "brow": brow, "legs": legs, "feet": feet, "covert": covert, "feathers": feathers,
            "far_wing": far_wing, "wet": wet}


def build() -> list[Step]:
    S: list[Step] = []
    dx, dy = DUCK

    def D(shape):                                          # place the duck in the scene
        return [[(dx + x, dy + y) for x, y in q] for q in shape]

    # 1. the storm sky
    S.append(Step("السماء العاصفة", [fill(rect(0, 0, 1200, 800), lin((0, TOP), (0, BOTTOM), [
        (0, "#05080f"), (.35, "#0e1626"), (.62, "#1d2638"), (.8, "#2a2228"), (1, "#0a0809")]))], "sweep", weight=1.2))

    # 2. the moon behind the clouds, and heavy cloud masses
    clouds = union(cloud(220, 170, 560, 90, 18, 31), cloud(820, 90, 760, 80, 18, 32), cloud(520, 250, 900, 60, 16, 33))
    S.append(Step("القمر خلف الغيوم", [
        glow(ellipse(*MOON, 260), "#3d5a86", 90, .55),
        fill(ellipse(*MOON, 44), rad(MOON, 60, [(0, "#f1f6ff"), (1, "#a9bbd8")]), .9),
        glow(ellipse(*MOON, 70), "#cfe0ff", 24, .5),
        fill(clouds, "#0c111c", .88, blur=16),
        fill(translate(clouds, 10, -12), "#4a6286", .22, blur=18, mode="screen"),
        fill(translate(clouds, 0, 16), "#ff6a2a", .06, blur=22, mode="add")],
        "sweep", weight=1.0))

    # 3. lightning far away, between the wing and the mountains
    r = random.Random(5)
    bolt = [(1080, 230)]
    while bolt[-1][1] < 500:
        bolt.append((bolt[-1][0] + r.uniform(-24, 14), bolt[-1][1] + r.uniform(22, 38)))
    branch = [bolt[3]] + [(bolt[3][0] - 26 - 20 * k, bolt[3][1] + 24 * k + r.uniform(-6, 6)) for k in range(1, 4)]
    S.append(Step("البرق", [
        glow(stroke([bolt, branch], 8), "#7fa8ff", 22, .6),
        fill(stroke([bolt], 2.2), "#f4f8ff"), fill(stroke([branch], 1.3), "#dce8ff", .9),
        glow(ellipse(1060, 330, 220, 140), "#5d7fc4", 60, .25)],
        "down", origin=(1080, 230), weight=.5))

    # 4. distant mountains and the volcanic glow behind them
    far = ridge(41, 480, 110, peaks=[(240, 60, 160), (640, 40, 200)])
    near = ridge(43, 548, 70, peaks=[(980, 50, 160)])
    S.append(Step("الجبال البعيدة", [
        glow(rect(0, 440, 1200, 60), "#ff5a2a", 40, .18),
        fill(far, lin((0, 390), (0, 600), [(0, "#1e2638"), (1, "#121722")]), blur=.8),
        fill(near, lin((0, 470), (0, 640), [(0, "#141924"), (1, "#0b0e15")]), blur=.5)],
        "right", weight=.8))

    # 5. mist and the moon's light falling through the rain
    rays = union(*[poly([(MOON[0] - 20 + 40 * k, MOON[1]), (MOON[0] + 30 + 40 * k, MOON[1]),
                         (MOON[0] + 260 + 120 * k, BOTTOM), (MOON[0] + 120 + 110 * k, BOTTOM)]) for k in range(4)])
    S.append(Step("الضباب وأشعة القمر", [
        fill(rays, "#6f8fbf", .07, blur=26, mode="screen"),
        fill(rect(-50, 480, 1300, 70), "#5b6c86", .30, blur=26, mode="screen"),
        fill(rect(-50, 570, 1300, 60), "#3f4c62", .28, blur=24, mode="screen")],
        "down", weight=.6))

    # 6. the dragon, colossal: rock under its claw, body and neck, head, the wing over the whole sky
    spire = path("M 1000 650 L 1012 520 L 1030 452 L 1052 418 L 1076 410 L 1100 428 L 1116 470 L 1132 560 L 1150 650 Z")
    S.append(Step("الصخرة تحت مخلب التنين", [
        fill(spire, lin((1020, 410), (1130, 650), [(0, "#1c1e25"), (1, "#08090c")])),
        rim(spire, (-.8, -.6), 2.6, "#ff7a32", .5), rim(spire, (.3, -1), 2, "#8aa4cc", .45)],
        "rise", origin=(1075, 650), weight=.4))

    nw_mem, nw_bones, nw_veins = wing((1000, 120), (820, 60), (640, -4),
                                      [(290, 84), (318, 176), (436, 226), (576, 234), (716, 196)], (930, 176), sag=.3)
    S.append(Step("جناح التنين الشاهق فوق السماء", [
        fill(nw_mem, lin((500, -40), (700, 200), [(0, "#3a4866"), (.55, "#1d2536"), (1, "#0e121a")]), .95, blur=.5),
        fill(nw_mem, rad(MOON, 560, [(0, "#4c6a98"), (1, "#4c6a9800")]), .6, mode="screen"),
        fill(nw_veins, "#0a0d14", .75), fill(nw_bones, "#0a0c11"),
        rim(union(nw_mem, nw_bones), (-.3, -1), 3.2, "#c8dcff", .85),
        rim(nw_mem, (-.4, 1), 3.2, "#ff7a32", .4),
        fill(rect(-50, 390, 1300, 120), "#4a5a74", .16, blur=30, mode="screen")],
        "grow", origin=(1000, 120), weight=1.1))

    spine = [(872, 200), (912, 172), (962, 142), (1020, 122), (1090, 112), (1160, 120), (1230, 150), (1300, 196)]
    radii = [46, 54, 62, 72, 86, 98, 102, 98]
    body = tube(spine, radii)
    legs = union(tube([(1152, 196), (1124, 290), (1096, 352), (1074, 404)], [58, 44, 34, 26]),
                 ellipse(1112, 318, 30, 24, rot=-30),
                 *[tube([(1074, 404), (1074 + ex * .6, 404 + ey * .6), (1074 + ex, 404 + ey)], [9, 6, 1.4], n=5)
                   for ex, ey in [(-46, 18), (-22, 32), (6, 34), (30, 22)]])
    back = spikes(spine, radii, every=4, size=2.0)
    head = path("M 864 150 C 852 128 824 120 798 132 C 772 144 744 168 722 190 L 670 236 C 662 244 666 250 676 248 "
                "L 714 238 L 774 222 L 726 262 L 688 296 C 680 304 686 310 696 307 C 726 298 762 284 794 268 "
                "C 828 250 858 222 872 192 Z")
    horns = union(tube([(846, 140), (890, 108), (940, 94), (992, 98)], [13, 9, 5, 1.2]),
                  tube([(830, 134), (868, 96), (912, 76), (954, 74)], [10, 7, 4, 1]))
    jaw_spikes = union(poly([(792, 268), (830, 284), (806, 258)]), poly([(820, 250), (858, 262), (832, 240)]))
    teeth = union(*[poly([(x, y), (x + 7, y - 2), (x + 3.5, y + 11)]) for x, y in
                    [(680, 246), (696, 242), (712, 238), (728, 234), (744, 230)]],
                  *[poly([(x, y), (x + 7, y - 3), (x + 3, y - 13)]) for x, y in [(694, 300), (712, 293), (730, 286)]])
    belly, plates = belly_plates(spine[:6], radii[:6])
    scales = stroke([[(x + 8 * math.cos(a), y + 6 * math.sin(a)) for a in (math.pi * .15, math.pi * .5, math.pi * .85)]
                     for x, y in [(900 + 26 * i + (13 if j % 2 else 0), 150 + 16 * j) for i in range(10) for j in range(5)]
                     if (x - 1000) ** 2 / 220 ** 2 + (y - 170) ** 2 / 60 ** 2 < 1], 1.1)
    dragon = union(body, legs, back, head, horns, jaw_spikes)
    S.append(Step("جسد التنين العملاق", [
        fill(dragon, "#101218"),
        fill(union(body, legs, head), rad(MOUTH, 560, [(0, "#6a2a14"), (.35, "#2c140f"), (1, "#101218")]), .92),
        fill(belly, rad(MOUTH, 520, [(0, "#c0682e"), (.45, "#5a2a1a"), (1, "#181210")]), .9),
        fill(plates, "#07070a", .55),
        fill(scales, "#05060a", .45),
        rim(dragon, (-.2, -1), 3.2, "#a9c2ea", .62),
        rim(union(head, body[:80], legs, jaw_spikes), (-.8, .6), 4.5, "#ff7a32", .95)],
        "grow", origin=(1000, 150), weight=1.5))
    S.append(Step("رأس التنين وأسنانه وعينه", [
        fill(teeth, "#f0e2c8", .95),
        fill(ellipse(806, 156, 8, 4.5, rot=-28), "#ffcf4a"), glow(ellipse(806, 156, 9, 6), "#ff9a2a", 12, .95),
        fill(ellipse(807, 156, 2, 4, rot=-28), "#2a0a00")],
        "grow", origin=(806, 156), weight=.4))

    # 7. smoke, then the fire breath bending in the wind and stopping just short of the duck
    a, b = (MOUTH[0] - 4, MOUTH[1] + 6), IMPACT
    S.append(Step("الدخان", [fill(union(cloud(640, 260, 240, 70, 9, 51), cloud(600, 200, 200, 60, 7, 52)),
                                  "#211a1d", .5, blur=14)], "rise", weight=.4))
    S.append(Step("نار التنين", [
        glow(tube([a, b], [18, 64]), "#ff4a12", 42, .65),
        *[fill(flame(900 + k, a, b, 5, 36, 18, bend=(k - 3) * .5), "#ff3d0a", .5, blur=3, mode="add") for k in range(7)],
        *[fill(flame(920 + k, a, b, 3.5, 24, 10, bend=(k - 2) * .35), "#ff9326", .65, blur=2.4, mode="add") for k in range(5)],
        *[fill(flame(940 + k, a, b, 2.2, 13, 6), "#ffe7a2", .85, blur=1.8, mode="add") for k in range(3)],
        fill(flame(960, a, b, 1.4, 6.5, 3), "#ffffff", .75, blur=1.2, mode="add")],
        "grow", origin=MOUTH, weight=1.1))

    # 8. steam where the rain hits the fire, and the fire's leading edge curling outward
    steam = union(cloud(IMPACT[0] + 10, IMPACT[1] - 6, 170, 70, 10, 61), cloud(IMPACT[0] - 10, IMPACT[1] - 48, 120, 50, 7, 62))
    S.append(Step("البخار عند نقطة التصادم", [
        fill(steam, "#c9cfd8", .36, blur=12, mode="screen"),
        fill(translate(steam, 0, 10), "#ff8a3a", .22, blur=16, mode="add"),
        glow(ellipse(*IMPACT, 54, 38), "#fff0c0", 22, .6),
        *[fill(tongue(980 + k, [IMPACT, (IMPACT[0] + 34 * math.cos(t0), IMPACT[1] - 28 * math.sin(t0)),
                                (IMPACT[0] + 60 * math.cos(t0), IMPACT[1] - 46 * math.sin(t0))], 9, 1),
               "#ff6a1a", .55, blur=2.5, mode="add") for k, t0 in enumerate((.5, 1.3, 2.1, 2.8, 3.6, -.3))]],
        "grow", origin=IMPACT, weight=.6))

    # 9. foreground obsidian rocks, faceted and wet, and rain pools that mirror the fire
    back_rocks = path("M -20 700 L 40 650 L 96 664 L 150 630 L 206 652 L 252 640 L 330 662 L 390 646 L 452 672 "
                      "L 520 660 L 600 690 L 690 676 L 760 700 L 860 688 L 940 712 L 1220 700 L 1220 760 L -20 760 Z")
    front = path(f"M -20 {BOTTOM + 40} L -20 712 L 70 694 L 150 704 L 230 692 L 330 698 L 420 706 L 500 720 "
                 f"L 600 712 L 700 726 L 820 720 L 920 732 L 1220 728 L 1220 {BOTTOM + 40} Z")
    facets = union(poly([(150, 630), (206, 652), (186, 690), (130, 676)]), poly([(390, 646), (452, 672), (430, 700), (376, 690)]),
                   poly([(40, 650), (96, 664), (70, 696), (20, 690)]), poly([(690, 676), (760, 700), (730, 716), (668, 708)]))
    cracks = stroke([[(120, 700), (140, 724), (128, 744)], [(470, 712), (486, 730)], [(780, 724), (800, 742)],
                     [(300, 706), (290, 730)]], 1.2)
    pools = union(ellipse(560, 730, 130, 9), ellipse(840, 740, 96, 7), ellipse(120, 724, 70, 6))
    ripples = stroke([q + [q[0]] for q in union(ellipse(520, 730, 18, 2.4), ellipse(608, 732, 12, 1.8),
                                                ellipse(850, 740, 16, 2), ellipse(130, 724, 10, 1.4))], .8)
    rocks = union(back_rocks, front)
    S.append(Step("الصخور البركانية المبللة", [
        fill(back_rocks, lin((0, 630), (0, 760), [(0, "#262a34"), (.5, "#121318"), (1, "#060608")])),
        fill(facets, lin((0, 630), (0, 720), [(0, "#4a5870"), (1, "#16181f")]), .95),
        fill(front, lin((0, 690), (0, 800), [(0, "#1c1f27"), (1, "#050506")])),
        fill(rocks, rad(IMPACT, 560, [(0, "#ff8a3a"), (.5, "#ff8a3a33"), (1, "#ff8a3a00")]), .35, mode="add"),
        rim(rocks, (.7, -1), 2.6, "#ff9a4a", .8),
        rim(union(rocks, facets), (-.4, -1), 1.8, "#9fb5da", .55),
        fill(cracks, "#030304", .9),
        fill(pools, lin((0, 715), (0, 750), [(0, "#4a2c1a"), (1, "#0d0a0c")])),
        fill(pools, rad(IMPACT, 480, [(0, "#ffc070"), (1, "#ffc07000")]), .55, mode="add"),
        fill(ripples, "#c8d6ee", .55)],
        "sweep", weight=1.0))

    # 10. the duck: far wing, body, near wing with its feathers, bill and feet, then the light on wet feathers
    dk = duck_shape()
    S.append(Step("جناح البطّة البعيد", [
        fill(D(dk["far_wing"]), lin((dx - 170, dy - 290), (dx, dy - 60), [(0, "#a3aec0"), (1, "#5d6879")]))],
        "grow", origin=(dx - 60, dy - 140), weight=.5))
    duck_body = union(D(dk["body"]), D(dk["neck"]), D(dk["head"]))
    S.append(Step("جسد البطّة", [
        fill(D(dk["legs"]), "#e8771c"),
        fill(duck_body, lin((dx - 104, dy - 150), (dx + 140, dy + 60), [(0, "#cdd5e1"), (.5, "#eff2f6"), (1, "#f7efe4")])),
        fill(D(dk["body"]), rad((dx - 40, dy + 46), 130, [(0, "#8592a6"), (1, "#8592a600")]), .65),
        fill(D(dk["neck"]), rad((dx + 50, dy - 40), 40, [(0, "#9aa6b8"), (1, "#9aa6b800")]), .5),
        fill(duck_body, lin((dx - 110, 0), (dx + 96, 0), [(0, "#6f7d96"), (.5, "#6f7d9600"), (1, "#6f7d9600")]), .55),
        fill(D(dk["wet"]), "#8e9bb0", .7, blur=.6)],
        "rise", origin=(dx, dy + 116), weight=.9))
    feather_outline = stroke([q + [q[0]] for f in dk["feathers"] for q in D(f)], 1.1)
    S.append(Step("جناح البطّة المفرود ريشة ريشة", [
        fill(D(dk["covert"]), lin((dx - 100, dy - 240), (dx, dy - 50), [(0, "#e3e9f1"), (1, "#f5f7fa")])),
        *[fill(D(f), lin((dx - 20, dy - 238), (dx - 150, dy - 300), [(0, "#f2f5f9"), (1, "#c7d0dd")])) for f in dk["feathers"]],
        fill(feather_outline, "#8592a6", .75)],
        "grow", origin=(dx - 20, dy - 238), weight=1.0))
    S.append(Step("المنقار والعين والقدمان", [
        fill(D(dk["bill_up"]), lin((dx + 130, dy - 118), (dx + 184, dy - 100), [(0, "#f08a1c"), (1, "#ffb347")])),
        fill(D(dk["bill_lo"]), "#d6621a"),
        fill(D(ellipse(160, -110, 4, 1.6, rot=12)), "#7a3a10", .9),
        fill(D(dk["feet"]), "#f08a1c"),
        fill(D(dk["eye"]), "#0a0a0c"), fill(D(ellipse(115.8, -119.8, 1.4, 1.4)), "#ffffff"),
        fill(D(dk["brow"]), "#6f7a8c", .9)],
        "grow", origin=(dx + 150, dy - 110), weight=.5))
    duck_all = union(duck_body, D(dk["covert"]), *[D(f) for f in dk["feathers"]], D(dk["far_wing"]),
                     D(dk["bill_up"]), D(dk["bill_lo"]), D(dk["legs"]), D(dk["feet"]))
    S.append(Step("ضوء النار والقمر على الريش المبلل", [
        rim(duck_all, (1, -.4), 3.6, "#ffa04a", .95),
        rim(duck_all, (1, -.4), 10, "#ff6a2a", .3, soft=2.4),
        rim(duck_all, (-.5, -1), 2.4, "#bcd2f5", .72),
        glow(D(dk["head"]), "#ff9a4a", 30, .2)],
        "grow", origin=IMPACT, weight=.7))

    # 11. water bursting from the rocks under the duck's feet
    r = random.Random(71)
    splash = [(dx + r.gauss(10, 74), dy + 122 - abs(r.gauss(0, 28)), r.choice([1, 1.4, 1.8, 2.4])) for _ in range(110)]
    crowns = stroke([[(dx + 70 + 10 * k, dy + 130), (dx + 62 + 18 * k, dy + 96 - 7 * k)] for k in range(4)] +
                    [[(dx - 70 - 10 * k, dy + 124), (dx - 80 - 16 * k, dy + 96 - 6 * k)] for k in range(3)], 2.4)
    S.append(Step("الماء يتطاير تحت قدمي البطّة", [
        fill(crowns, "#d6e2f4", .72, blur=.8), fill(dots(splash), "#e4edfa", .85),
        fill(dots([(x, y, s * 2.5) for x, y, s in splash[:34]]), "#ff9a4a", .25, blur=2, mode="add")],
        "sparkle", weight=.4))

    # 12. rain: far, near, and drops lit by the fire
    S.append(Step("المطر البعيد", [fill(rain(81, 950, -40, 1240, TOP - 40, BOTTOM, 26, 1.0), "#9fb2cf", .22, blur=.4)],
                  "down", weight=.6))
    S.append(Step("المطر القريب", [
        fill(rain(82, 260, -40, 1240, TOP - 60, BOTTOM, 64, 1.9), "#c4d4ec", .3, blur=1.3),
        fill(rain(83, 240, 440, 820, 220, 560, 36, 1.3), "#ffb066", .55, blur=.6, mode="add")],
        "down", weight=.7))

    # 13. embers and sparks swirling in the wind
    r = random.Random(91)
    emb = []
    for _ in range(280):
        t = r.random()
        emb.append((a[0] + (b[0] - a[0]) * t + r.gauss(0, 54), a[1] + (b[1] - a[1]) * t + r.gauss(0, 42) - r.random() * 80,
                    r.choice([.6, .8, 1.1, 1.5])))
    S.append(Step("الشرر والجمر", [
        fill(dots(emb), "#ffd27a", .9, mode="add"),
        fill(dots([(x, y, s * 3) for x, y, s in emb if s > 1]), "#ff7a2a", .45, blur=2.4, mode="add")],
        "sparkle", weight=.5))

    # 14. grade, vignette, grain, and the 16:9 bars
    S.append(Step("اللمسات السينمائية", [
        grade(shadows="#0a1426", highlights="#ffe2c4", amount=.45, contrast=1.08),
        vignette(.6), grain(.02, 7)], "sweep", weight=.6))
    S.append(Step("إطار 16:9", [fill(rect(0, 0, 1200, TOP), "#000000"), fill(rect(0, BOTTOM, 1200, 800 - BOTTOM), "#000000")],
                  "sweep", weight=.3))
    return S
