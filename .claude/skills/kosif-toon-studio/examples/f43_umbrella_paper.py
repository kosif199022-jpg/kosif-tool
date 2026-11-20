#!/usr/bin/env python3
"""43 «الشمسية المقلوبة» in way D «الورق الحي» Living Paper (paperkit), to compare with f42 (way A).
Same 9 shots, timings, captions, credit, watermark and sound plan as f42 (its story helpers are imported, not copied):
the world is rebuilt as torn-paper gouache plates in depth, the characters are white-bordered stickers animated on twos
with line boil, and Specs's science moments get self-drawing chalk doodles.
    python3 f43_umbrella_paper.py OUT.mp4                      # full render (multi-process)
    python3 f43_umbrella_paper.py OUT --stills 1,5.5,11.5,18.5 # style frames -> OUT_sheet.jpg
"""
import importlib.util, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "engine"))
import cv2, numpy as np
import toonkit as tk
import paperkit as pk
from toonkit import sm, key, lerp, lerp2, INK, WHITE, WATER

_spec = importlib.util.spec_from_file_location("f42", os.path.join(HERE, "f42_umbrella.py"))
f42 = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(f42)

D, W, H = f42.D, tk.W, tk.H
SHOTS, GY_FAR, GY_NEAR, GY_CU = f42.SHOTS, f42.GY_FAR, f42.GY_NEAR, f42.GY_CU
hand_pt, rider, bowl, umbrella, tube, tears = f42.hand_pt, f42.rider, f42.bowl, f42.umbrella, f42.tube, f42.tears

MOOD = {"rain": "rain", "rain_cu": "rain", "road": "dawn", "desert": "desert", "desert_cu": "desert", "sunset": "sunset"}
DOF = {"ride_rain": 0.25, "cap_laugh": 1.0, "bowl_cu": 1.0, "specs_wait": 1.0, "next_day": 0.15, "ride_desert": 0.25,
       "cap_jealous": 1.0, "specs_sip": 1.0, "share": 0.3}


# ------------------------------------------------------------------ plates (static paper layers per background)
def cloud_paper(g, x, y, s, col):
    tk.cloud(g, x, y, s, col)
    g.ellipse((x + 10 * s, y + 46 * s), (118 * s, 10 * s), tuple(int(v * .86) for v in col))


def tufts(g, x, base, s, col, n=7, seed=0):
    rng = np.random.default_rng(seed)
    for i in range(n):
        a = -math.pi / 2 + (i - n / 2) * 0.22 + rng.uniform(-.1, .1); L = s * rng.uniform(120, 230)
        tip = (x + L * math.cos(a), base + L * math.sin(a)); w = 22 * s
        g.poly([(x - w, base + 20), tip, (x + w, base + 20)], tuple(int(v * rng.uniform(.85, 1.1)) for v in col))


def house(g, x, base, s, wall, roof):
    g.rect((x - 46 * s, base - 70 * s), (x + 46 * s, base), wall, 0)
    g.poly([(x - 60 * s, base - 66 * s), (x, base - 118 * s), (x + 60 * s, base - 66 * s)], roof)
    g.rect((x - 12 * s, base - 40 * s), (x + 8 * s, base - 22 * s), (120, 200, 240), 0)


def mesas(g, base, col, seed=3):
    for x0, w, h in ((-40, 300, 190), (330, 180, 120), (640, 420, 230), (980, 200, 150)):
        g.poly([(x0, base), (x0 + w * .12, base - h), (x0 + w * .88, base - h), (x0 + w, base)], col)
        g.rect((x0 + w * .1, base - h - 8), (x0 + w * .9, base - h + 6), tuple(min(255, int(v * 1.12)) for v in col), 0)


def sky_plate(top, bot, y1=H):
    return pk.cutout(*pk.matte(lambda g: g.vgrad(0, y1, top, bot) if y1 >= H else (g.vgrad(0, y1, top, bot), g.vgrad(y1, H, bot, bot))),
                     edge=None, gouache=1.0, seed=1)


def _rain_plates(cu):
    gy = 1390
    P = [("sky", sky_plate((112, 94, 86), (186, 178, 170)), 0.0)]
    P.append(("clouds", pk.paper(lambda g: [cloud_paper(g, x, y, s, c) for x, y, s, c in
                                            ((170, 150, 2.0, (146, 136, 132)), (640, 90, 2.5, (132, 122, 118)), (990, 270, 1.8, (158, 150, 146)),
                                             (430, 400, 1.4, (170, 164, 160)))], "torn", 11, gouache=0.8), 0.12))
    if not cu:
        P.append(("far", pk.paper(lambda g: (tk.hills(g, gy - 230, 120, 560, (126, 128, 118)), house(g, 860, gy - 290, 0.9, (190, 196, 210), (70, 70, 140))),
                                  "torn", 12, gouache=1.0), 0.35))
        P.append(("mid", pk.paper(lambda g: (tk.hills(g, gy - 170, 80, 340, (98, 114, 96), 2.0), [tk.pine(g, x, gy - 150, 1.1, snow=False) for x in (80, 300, 840, 1010)]),
                                  "torn", 13, gouache=1.0), 0.62))

        def ground(g):
            g.vgrad(gy - 160, gy - 110, (86, 132, 92), (70, 116, 80))
            g.vgrad(gy - 110, gy + 110, (112, 110, 112), (92, 90, 94))
            g.line((-10, gy - 110), (W + 10, gy - 110), INK, 5); g.line((-10, gy + 110), (W + 10, gy + 110), INK, 5)
            g.vgrad(gy + 110, H, (80, 124, 86), (52, 92, 60))
            for x, y, rx in ((160, gy - 40, 120), (620, gy + 70, 150), (940, gy - 70, 90)):
                g.ellipse((x, y), (rx, 14), (170, 166, 162))
        P.append(("ground", pk.paper(ground, "torn", 14, gouache=1.0), 1.0))
        P.append(("near", pk.paper(lambda g: (tufts(g, 40, 1960, 1.2, (60, 104, 66), 9, 1), tufts(g, 1050, 1950, 1.0, (54, 96, 62), 8, 2)),
                                   "torn", 15, gouache=0.6), 1.35))
    else:
        P.append(("far", pk.paper(lambda g: tk.hills(g, 1240, 140, 600, (126, 128, 118)), "torn", 12, gouache=1.0), 0.35))
        P.append(("mid", pk.paper(lambda g: (tk.hills(g, 1320, 90, 360, (98, 114, 96), 2.0), [tk.pine(g, x, 1330, 1.5, snow=False) for x in (60, 980)]),
                                  "torn", 13, gouache=1.0), 0.62))
        P.append(("ground", pk.paper(lambda g: (g.vgrad(1320, H, (104, 102, 106), (78, 76, 82)),
                                                [g.ellipse((x, y), (rx, 12), (150, 146, 142)) for x, y, rx in ((200, 1500, 140), (820, 1620, 170))]),
                                     "torn", 14, gouache=1.0), 1.0))
    return P


def _desert_plates(kind):
    gy = 1390
    sunset = kind == "sunset"
    top, bot = ((110, 60, 130), (80, 160, 250)) if sunset else ((205, 140, 70), (165, 215, 248))
    P = [("sky", sky_plate(top, bot), 0.0)]
    ccol = (150, 150, 230) if sunset else (226, 234, 242)
    P.append(("clouds", pk.paper(lambda g: [cloud_paper(g, x, y, s, ccol) for x, y, s in ((200, 170, 1.3), (860, 120, 1.1), (560, 420, 0.9))], "torn", 21, gouache=0.7), 0.12))
    if kind == "road":
        P.append(("far", pk.paper(lambda g: (mesas(g, 1110, (120, 150, 214)), tk.hills(g, 1100, 60, 700, (116, 176, 230))), "torn", 22, gouache=1.0), 0.35))

        def ground(g):
            g.vgrad(1100, H, (126, 190, 236), (100, 166, 222))
            g.poly([(520, 1100), (560, 1100), (900, H), (180, H)], (110, 116, 126))
            g.poly([(520, 1100), (180, H)], INK, 5, False); g.poly([(560, 1100), (900, H)], INK, 5, False)
            for i in range(7):
                u0, u1 = (i / 7) ** 1.8, ((i + .5) / 7) ** 1.8
                y0, y1 = lerp(1100, H, u0), lerp(1100, H, u1); w0, w1 = lerp(3, 18, u0), lerp(3, 18, u1)
                g.poly([(540 - w0, y0), (540 + w0, y0), (540 + w1, y1), (540 - w1, y1)], (150, 230, 250))
            f42.cactus(g, 170, 1300, 1.3, (80, 150, 96)); f42.cactus(g, 930, 1240, 1.0, (80, 150, 96))
            rng = np.random.default_rng(9)
            for _ in range(30):
                x, y = rng.uniform(0, W), rng.uniform(1200, H - 20)
                if abs(x - 540) > 120 + (y - 1100) * 0.45: g.ellipse((x, y), (rng.uniform(20, 46), 5), (100, 164, 216))
        P.append(("ground", pk.paper(ground, "torn", 24, gouache=1.0), 1.0))
        return P
    mcol = (110, 104, 180) if sunset else (126, 160, 220)
    d1 = (110, 150, 220) if sunset else (130, 196, 240)
    d2 = (90, 128, 200) if sunset else (110, 176, 226)
    if kind == "desert_cu":
        P.append(("far", pk.paper(lambda g: (mesas(g, 1250, mcol), tk.hills(g, 1240, 160, 700, d1)), "torn", 22, gouache=1.0), 0.35))
        P.append(("mid", pk.paper(lambda g: (tk.hills(g, 1320, 90, 420, d2, 1.4), f42.cactus(g, 980, 1330, 1.3, (80, 150, 96))), "torn", 23, gouache=1.0), 0.62))
        P.append(("ground", pk.paper(lambda g: g.vgrad(1320, H, (126, 190, 236), (104, 170, 224)), "torn", 24, gouache=1.0), 1.0))
        return P
    P.append(("far", pk.paper(lambda g: (mesas(g, gy - 200, mcol), tk.hills(g, gy - 230, 110, 700, d1)), "torn", 22, gouache=1.0), 0.35))
    P.append(("mid", pk.paper(lambda g: (tk.hills(g, gy - 160, 70, 420, d2, 1.4),
                                         [f42.cactus(g, x, gy - 150, s, (70, 120, 90) if sunset else (80, 150, 96)) for x, s in ((90, 1.0), (980, 1.2))]),
                              "torn", 23, gouache=1.0), 0.62))
    sand_top = (100, 150, 214) if sunset else (126, 190, 236)

    def ground(g):
        g.vgrad(gy - 160, gy - 110, sand_top, sand_top)
        g.vgrad(gy - 110, gy + 110, (96, 96, 104) if sunset else (120, 126, 136), (84, 84, 92) if sunset else (104, 108, 118))
        g.line((-10, gy - 110), (W + 10, gy - 110), INK, 5); g.line((-10, gy + 110), (W + 10, gy + 110), INK, 5)
        g.vgrad(gy + 110, H, sand_top, (84, 136, 200) if sunset else (104, 170, 224))
        rng = np.random.default_rng(4)
        for _ in range(26):                                                    # dry cracks in the sand
            x, y = rng.uniform(0, W), rng.uniform(gy + 160, H - 30); pts = [(x, y)]
            for _ in range(4): pts.append((pts[-1][0] + rng.uniform(-40, 40), pts[-1][1] + rng.uniform(-14, 14)))
            g.poly(pts, (70, 110, 170) if sunset else (90, 146, 200), 3, False)
    P.append(("ground", pk.paper(ground, "torn", 24, gouache=1.0), 1.0))
    rock = (70, 96, 150) if sunset else (90, 130, 180)
    P.append(("near", pk.paper(lambda g: (g.oval((60, 1900), (150, 80), rock, 0), g.oval((1040, 1910), (120, 70), rock, 0),
                                          tufts(g, 160, 1950, 0.8, (60, 120, 110), 6, 3)), "torn", 25, gouache=0.8), 1.35))
    return P


PLATES = {}


def prepare():
    if PLATES: return
    PLATES["rain"] = _rain_plates(False); PLATES["rain_cu"] = _rain_plates(True)
    for k in ("desert", "desert_cu", "road", "sunset"): PLATES[k] = _desert_plates(k)


# ------------------------------------------------------------------ dynamic layers (on twos)
def paper_sun(g, c, t, r, col=(120, 226, 255), ray=(90, 200, 255)):
    for i in range(12):
        a = i * math.tau / 12 + t * 0.3
        g.poly([(c[0] + (r + 16) * math.cos(a - .11), c[1] + (r + 16) * math.sin(a - .11)), (c[0] + (r + 70) * math.cos(a), c[1] + (r + 70) * math.sin(a)),
                (c[0] + (r + 16) * math.cos(a + .11), c[1] + (r + 16) * math.sin(a + .11))], ray)
    g.circle(c, r, col); g.circle((c[0] - r * .2, c[1] - r * .22), r * .55, (200, 246, 255))


def sun_pos(kind, e):
    if kind == "next_day": return (540, lerp(1120, 760, sm(e / 1.5))), 170
    if kind == "ride_desert": return (880, 300), 110
    if kind in ("cap_jealous", "specs_sip"): return (930, 240), 120
    if kind == "share": return (860, 760), 105  # off to the side, above the heads
    return None, 0


def ride_chars(g, t, desert):
    """f42.ride without the road marks and lightning (those live on their own layers)."""
    kc, Xc = 0.92, 330
    bobc = 6 * abs(math.sin(t * 14)) if not desert else 0
    if desert: face = dict(eyes="sleepy", mouth="tongue", blush=1.0, sweat=5, brows="worried"); rhc = None; hb = True
    else: face = dict(eyes="squeeze", mouth="laugh"); rhc = hand_pt(Xc, GY_FAR, kc, 1, 175, -455); hb = False
    shade_hand = hand_pt(Xc, GY_FAR, kc, 1, -125, -505)
    a = rider(g, "cap", Xc, GY_FAR, kc, t, 1, face=face, hand_bar=hb, rh=rhc if not desert else shade_hand, lh=shade_hand if not desert else None, bob=bobc)
    umbrella(g, shade_hand, kc, 1, t, (64, 64, 200))
    if not desert:
        tk.laugh_marks(g, a["head"], t); g.line(a["rh"], (a["rh"][0] + 46, a["rh"][1] - 10), INK, 9); tears(g, a["head"], t, 0.92, 1, 2)
    else:
        tk.drops(g, a["head"], t, 3, 110, f42.TEAR, 1.8)
    f42.speed_streaks(g, a["P"](-260, -200), t)
    ks, Xs = 1.0, 725
    hs = hand_pt(Xs, GY_NEAR, ks, 1, 100, -505)
    s = rider(g, "specs", Xs, GY_NEAR, ks, t, 1, face=dict(eyes="happy", mouth="smile"), lh=hs, rh=hand_pt(Xs, GY_NEAR, ks, 1, 120, -305))
    b = bowl(g, hs, ks, 1, t, sm(t / 2.4) * 0.6 + 0.4 if not desert else 1.0, ripples=not desert)
    if not desert: f42.rain_drops_into(g, b, t)
    else: tk.sparkles(g, (b["c"][0], b["lvl"] - 30), t, 4, 150, 16, (255, 255, 255))
    f42.speed_streaks(g, s["P"](-260, -200), t)
    return dict(cap=a, specs=s, bowl=b)


def chars(g, t, kind, e):
    """f42.draw's character part per shot (environment, rain and sun removed). Returns anchors for the chalk."""
    A = {}
    if kind == "ride_rain": A = ride_chars(g, t, False)
    elif kind == "ride_desert": A = ride_chars(g, t, True)
    elif kind == "cap_laugh":
        k, X = 1.9, 470
        hold = hand_pt(X, GY_CU, k, 1, -125, -505); bob = 26 * abs(math.sin(t * 15))
        a = rider(g, "cap", X, GY_CU, k, t, 1, spin=False, face=dict(eyes="squeeze", mouth="laugh", blush=0.5), hand_bar=True, rh=hand_pt(X, GY_CU, k, 1, 60, -300), lh=hold, bob=bob)
        umbrella(g, (hold[0], hold[1] + bob), k, 1, t, (64, 64, 200))
        tk.laugh_marks(g, (a["head"][0] - 60, a["head"][1]), t); tk.laugh_marks(g, (a["head"][0] + 420, a["head"][1]), t, -1)
        tears(g, a["head"], t, k, 1, 3); A = dict(cap=a)
    elif kind == "bowl_cu":
        k, X = 1.6, 470
        hs = hand_pt(X, GY_CU + 120, k, 1, 100, -505)
        s = rider(g, "specs", X, GY_CU + 120, k, t, 1, spin=False, face=dict(eyes="happy", mouth="smile", look=(0.2, -1)), lh=hs, rh=hand_pt(X, GY_CU + 120, k, 1, 120, -305))
        b = bowl(g, hs, k, 1, t, 1.0, spill=min(1.0, 0.4 + e / 1.2))
        f42.rain_drops_into(g, b, t, k)
        for j in range(3):
            u = ((e * 1.3) + j / 3) % 1
            tk.splash(g, (b["c"][0] + (j - 1) * b["w"] * 0.5, b["lvl"]), u, 8, 180, WATER, seed=11 + j)
        A = dict(specs=s, bowl=b)
    elif kind == "specs_wait":
        k, X = 1.9, 520
        hs = hand_pt(X, GY_CU, k, 1, 100, -505)
        s = rider(g, "specs", X, GY_CU, k, t, 1, spin=False, face=dict(eyes="sleepy", mouth="smile", brows="flat", look=(1, 0)), lh=hs, rh=hand_pt(X, GY_CU, k, 1, 120, -305))
        b = bowl(g, hs, k, 1, t, 1.0)
        if e > 0.6: tk.sparkle(g, (s["head"][0] + 120, s["head"][1] - 40), 26 * f42.out_pop(e - 0.6), WHITE, 7)
        if e > 0.9: tk.bulb(g, (s["head"][0] - 230, s["head"][1] - 260), (e - 0.9) / 0.4, t)
        A = dict(specs=s, bowl=b)
    elif kind == "cap_jealous":
        k, X = 1.9, 520
        hold = hand_pt(X, GY_CU, k, 1, -125, -505); tremble = 5 * math.sin(t * 50)
        a = rider(g, "cap", X + tremble, GY_CU, k, t, 1, spin=False, face=dict(eyes="open", mouth="wavy", brows="worried", look=(1, 0.2), blush=1.0, sweat=6), lh=hold)
        umbrella(g, hold, k, 1, t, (64, 64, 200))
        f42.steam(g, a["top"], t, k); A = dict(cap=a)
    elif kind == "specs_sip":
        k, X = 1.6, 470
        hs = hand_pt(X, GY_CU + 120, k, 1, 100, -505)
        s = rider(g, "specs", X, GY_CU + 120, k, t, 1, spin=False, face=dict(eyes="closed", mouth="smile", blush=0.35), lh=hs, rh=hand_pt(X, GY_CU + 120, k, 1, 120, -305))
        b = bowl(g, hs, k, 1, t, 1.0 - 0.15 * sm(e / 2.0), ripples=False, bubbles=1.0)
        mouth = (s["head"][0] + 0.36 * 84 * k, s["head"][1] + 0.5 * 84 * k)
        a0, ctrl = (b["c"][0] + 0.86 * b["w"], b["lvl"] + 14 * k), (b["c"][0] + 1.25 * b["w"], mouth[1] + 40 * k)
        tube(g, a0, mouth, t, k, ctrl=ctrl)
        f42.hearts(g, (s["head"][0] - 220, s["head"][1] - 160), t)
        A = dict(specs=s, bowl=b, tube=(a0, ctrl, mouth))
    elif kind == "share":
        f42_share(g, t, e); A = dict()
    return A


def f42_share(g, t, e):
    """f42.share minus its sun (the sun is a paper layer behind the dunes here)."""
    real = tk.sun
    tk.sun = lambda *a, **k: None
    try:
        gv = g.vgrad
        g.vgrad = lambda *a, **k: None                      # f42.share also paints a horizon strip: not needed on paper
        f42.share(g, t, e)
    finally:
        tk.sun = real; g.vgrad = gv


def marks(g, t, desert):
    f42.scroll_marks(g, t, 1390, 900, (150, 230, 250) if desert else (215, 215, 215))


def fxl(g, t, n, kind, e):
    if kind == "ride_rain":
        tk.rain(g, n, 1.0)
        if 0.35 <= t < 0.6 and int(t * 30) % 2 == 0: tk.bolt(g, (900, -20), (760, 420), 4, 10)
    elif kind == "cap_laugh": tk.rain(g, n, 0.8)
    elif kind == "bowl_cu": tk.rain(g, n, 0.8)
    elif kind == "specs_wait": tk.rain(g, n, 0.7)
    elif kind == "next_day": f42.heat_lines(g, t, 1150, 1400)
    elif kind == "ride_desert": f42.heat_lines(g, t, 560, 900)


def heart(c, s):
    return [(c[0] + s * 16 * math.sin(a) ** 3 / 16, c[1] - s * (13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a)) / 16)
            for a in np.linspace(0, math.tau, 50)]


def chalk(kind, e, A, idx):
    ch = pk.Chalk(seed=idx // 30)
    U = lambda a, d: max(0.0, min(1.0, (e - a) / d))
    if kind == "ride_rain" and "bowl" in A:
        b = A["bowl"]; c = (b["c"][0], b["c"][1] - 40)
        ch.circle(c, b["w"] + 40, U(1.5, 0.45), ry=b["dep"] + 150)
        ch.arrow((c[0] - 330, c[1] - 330), (c[0] - b["w"] - 40, c[1] - 110), U(1.8, 0.35))
    elif kind == "bowl_cu" and "bowl" in A:
        b = A["bowl"]
        for j, dx in enumerate((-0.55, 0.0, 0.55)):
            x = b["c"][0] + dx * b["w"]
            ch.arrow((x + 30, b["lvl"] - 520), (x, b["lvl"] - 90), U(0.15 + j * 0.2, 0.4), bend=0.0, head=30)
        ch.line((b["c"][0] + b["w"] + 40, b["lvl"]), (b["c"][0] + b["w"] + 40, b["apex"][1]), U(1.0, 0.3), bend=0.0)
        ch.line((b["c"][0] + b["w"] + 20, b["lvl"]), (b["c"][0] + b["w"] + 60, b["lvl"]), U(1.0, 0.15), bend=0.0)
        ch.line((b["c"][0] + b["w"] + 20, b["apex"][1]), (b["c"][0] + b["w"] + 60, b["apex"][1]), U(1.2, 0.15), bend=0.0)
        ch.drop((b["c"][0] + b["w"] + 110, (b["lvl"] + b["apex"][1]) / 2), 34, U(1.3, 0.35))
    elif kind == "specs_wait" and "specs" in A:
        h = A["specs"]["head"]; c = (h[0] + 330, h[1] + 70); r = 74
        ch.circle(c, r, U(0.15, 0.4), over=10)
        if e > 0.5:
            a1 = -math.pi / 2 + (e - 0.5) * 9; a2 = -math.pi / 2 + (e - 0.5) * 0.9
            ch.path([c, (c[0] + r * .7 * math.cos(a1), c[1] + r * .7 * math.sin(a1))], 1.0)
            ch.path([c, (c[0] + r * .45 * math.cos(a2), c[1] + r * .45 * math.sin(a2))], 1.0)
        ch.arrow((c[0] - r - 40, c[1] + 40), (c[0] - 20, c[1] + r + 40), U(0.7, 0.4), bend=0.35)
    elif kind == "next_day":
        ch.arrow((180, 1060), (420, 740), U(0.25, 0.6), bend=-0.25)
    elif kind == "ride_desert":
        x, y0, y1 = 150, 190, 420
        ch.path([(x - 18, y1 - 30), (x - 18, y0), (x + 18, y0), (x + 18, y1 - 30)], U(0.2, 0.35))
        ch.circle((x, y1), 34, U(0.45, 0.25), over=0)
        ch.line((x, y1 - 10), (x, lerp(y1 - 10, y0 + 20, sm((e - 0.6) / 0.8))), 1.0 if e > 0.6 else 0, th=14, bend=0.0)
        for j in range(3): ch.line((x + 30, y0 + 40 + j * 50), (x + 52, y0 + 40 + j * 50), U(0.7 + j * .08, 0.1), bend=0.0)
    elif kind == "cap_jealous" and "cap" in A:
        h = A["cap"]["head"]
        for j, dx in enumerate((300, 360)):
            ch.line((h[0] + dx, h[1] - 330), (h[0] + dx - 14, h[1] - 190), U(0.3 + j * .15, 0.2), th=12, bend=0.0)
            ch.circle((h[0] + dx - 18, h[1] - 150), 9, U(0.5 + j * .15, 0.1), over=0)
    elif kind == "specs_sip" and "tube" in A:
        a0, ctrl, m = A["tube"]
        pts = [(x + 34, y - 30) for x, y in tk.bezier(a0, ctrl, m, 30)]
        ch.arrow(pts[0], pts[-1], 0, bend=0)                       # (keeps stroke ids stable)
        ch.path(pts, U(0.2, 0.6) / 0.85)
        if e > 0.71:
            q, b = pts[-3], pts[-1]; ang = math.atan2(b[1] - q[1], b[0] - q[0])
            for s in (1, -1): ch.path([b, (b[0] - 34 * math.cos(ang + s * .5), b[1] - 34 * math.sin(ang + s * .5))], U(0.71, 0.12))
        bw = A["bowl"]
        ch.drop((bw["c"][0] - bw["w"] - 40, bw["lvl"] - 120), 40, U(0.6, 0.35))
        ch.star((bw["c"][0] - bw["w"] + 40, bw["lvl"] - 230), 26, U(0.9, 0.3))
    elif kind == "share":
        ch.path(heart((540, 640), 120), U(1.85, 0.6))
        ch.star((330, 560), 26, U(2.2, 0.3)); ch.star((760, 540), 22, U(2.35, 0.3))
    return ch.render(idx)


_DYN = {}


def dyn(i, idx, tp):
    k = (i, idx)
    if k in _DYN: return _DYN[k]
    if len(_DYN) > 6: _DYN.clear()
    t0, t1, bgname, kind = SHOTS[i]
    e = tp - t0
    L = {}
    c, r = sun_pos(kind, e)
    if c: L["sun"] = pk.paper(lambda g: paper_sun(g, c, tp, r), "torn", 31, rim=6, boil=idx)
    if kind in ("ride_rain", "ride_desert"): L["marks"] = pk.paper(lambda g: marks(g, tp, kind == "ride_desert"), "torn", 32, rim=4)
    box = {}

    def dc(g): box["A"] = chars(g, tp, kind, e)
    L["chars"] = pk.cutout(*pk.matte(dc), edge="sticker", seed=33, boil=idx, gouache=0.45)
    fxd = lambda g: fxl(g, tp, idx, kind, e)
    if kind in ("ride_rain", "cap_laugh", "bowl_cu", "specs_wait", "next_day", "ride_desert"): L["fx"] = pk.fx(fxd)
    L["chalk"] = chalk(kind, e, box["A"], idx)
    _DYN[k] = L
    return L


def frame(t, n):
    i = f42.shot_at(t); t0, t1, bgname, kind = SHOTS[i]
    tp, idx = pk.twos(t); tp = max(tp, t0)
    Ld = dyn(i, idx, tp)
    cam = f42.cam(t)
    P = PLATES[bgname]
    lay = []
    for name, img, p in P:
        if name == "near": continue
        lay.append(pk.L(img, p, shadow=None if name == "sky" else pk.PLATE_SHADOW))
        if name == "sky" and "sun" in Ld: lay.append(pk.L(Ld["sun"], 0.05, shadow=None))
    if "marks" in Ld: lay.append(pk.L(Ld["marks"], 1.0, shadow=(4, 6, 4, 0.3)))
    lay.append(pk.L(Ld["chars"], 1.0, shadow=pk.STICKER_SHADOW, wrap=0.55))
    for name, img, p in P:
        if name == "near": lay.append(pk.L(img, p, shadow=(20, 26, 16, 0.35)))
    if "fx" in Ld: lay.append(pk.L(Ld["fx"], 1.08, shadow=None, soft=0.6))
    lay.append(pk.L(Ld["chalk"], 1.0, shadow=None, focus=True))
    e = t - t0
    mood = MOOD[bgname]
    light = None
    c, r = sun_pos(kind, e)
    if c:
        sx, sy = pk.project(c, cam, 0.05); light = (sx, sy, 1500, (120, 210, 255), 0.35)
    elif mood == "rain":
        light = (W * 0.75, -100, 1500, (255, 236, 220), 0.25)
    fr = pk.compose(lay, cam, mood, DOF[kind], light, n)
    if kind == "ride_rain" and 0.35 <= t < 0.6 and int(t * 30) % 2 == 0:
        fr = cv2.addWeighted(fr, 0.75, np.full_like(fr, 255), 0.25, 0)
    return fr


# ------------------------------------------------------------------ sound: f42's plan + chalk scratches
CHALK_T = [1.5, 1.8, 4.75, 4.95, 5.15, 5.6, 5.9, 6.95, 7.5, 9.05, 10.5, 10.9, 12.9, 14.6, 15.0, 15.3, 18.45]


def audio(path):
    real = tk.Mix.save

    def save(self, p):
        for c in CHALK_T:
            for j in range(3): self.noise(c + j * 0.07, 0.06, 0.10, 1, 25)
        real(self, p)
    tk.Mix.save = save
    try: f42.audio(path)
    finally: tk.Mix.save = real


if __name__ == "__main__":
    out = sys.argv[1]
    aud = None
    if "--stills" not in sys.argv:
        aud = out.replace(".mp4", ".m4a"); audio(aud)
    pk.run(out, D, frame, aud, overlay=f42.overlays, prepare=prepare)
