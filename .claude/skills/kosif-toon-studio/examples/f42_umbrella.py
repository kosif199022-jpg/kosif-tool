#!/usr/bin/env python3
"""42 «الشمسية المقلوبة» (code-drawn version A, stickman-director pacing).
Rain: Specs rides with his umbrella held upside down like a bowl, filling with rainwater; Cap laughs under a normal umbrella.
Next day, desert, 50°C: Cap is cooking, Specs sips cool water through a tube from his umbrella-bowl and shares it at sunset.
Directing level: a new shot every 1.5-3.4 s, punch-in zoom on each cut, whip transitions, big Archivo Black captions popping in,
credit over a dark gradient at the end. Captions and credit are drawn in screen space after the camera (tk.camera_crop wrapper)."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
import os as _o, sys as _s; _s.path.insert(0, _o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "..", "engine"))
import toonkit as tk
from toonkit import sm, key, lerp, lerp2, INK, WHITE, WATER

D = 20.0
W, H = tk.W, tk.H
ARCH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts", "ArchivoBlack.ttf")
CAIRO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts", "Cairo-900.ttf")

# (start, end, background, kind)
SHOTS = [
    (0.0, 2.6, "rain", "ride_rain"),
    (2.6, 4.6, "rain_cu", "cap_laugh"),
    (4.6, 6.8, "rain_cu", "bowl_cu"),
    (6.8, 8.8, "rain_cu", "specs_wait"),
    (8.8, 10.3, "road", "next_day"),
    (10.3, 12.6, "desert", "ride_desert"),
    (12.6, 14.4, "desert_cu", "cap_jealous"),
    (14.4, 16.6, "desert_cu", "specs_sip"),
    (16.6, 20.0, "sunset", "share"),
]
CUTS = [s[0] for s in SHOTS[1:]]
CAPS = [  # text, t0, t1, screen y
    ("IT'S RAINING.", 0.15, 1.5, 300),
    ("WHY IS IT UPSIDE DOWN?!", 1.5, 2.6, 300),
    ("HAHAHA", 2.75, 4.5, 1560),
    ("JUST WAIT.", 7.0, 8.7, 1700),
    ("NEXT DAY...", 8.95, 10.2, 960),
    ("50°C", 10.45, 12.5, 300),
    ("WAIT... WHAT?", 12.75, 14.3, 1640),
    ("WHO'S LAUGHING NOW?", 14.55, 16.5, 1720),
    ("SHARING IS SMARTER.", 16.8, 18.4, 300),
]
TEAR = (250, 214, 150)
GY_FAR, GY_NEAR = 1330, 1450          # wide shots: Cap's lane (behind), Specs's lane (front)
GY_CU = 1800                           # close-ups


def shot_at(t):
    return max(i for i, s in enumerate(SHOTS) if s[0] <= t + 1e-6)


# ------------------------------------------------------------------ backgrounds (cached canvases)
BG = {}


def _rain_bg(g, gy):
    g.vgrad(0, gy - 160, (128, 112, 104), (176, 168, 160))
    tk.hills(g, gy - 230, 120, 560, (120, 124, 116)); tk.hills(g, gy - 170, 80, 340, (100, 116, 98), 2.0)
    for x in (80, 300, 840, 1010):
        tk.pine(g, x, gy - 150, 1.1, snow=False)
    g.vgrad(gy - 160, gy - 110, (86, 132, 92), (70, 116, 80))                       # verge
    g.vgrad(gy - 110, gy + 110, (112, 110, 112), (92, 90, 94))                       # wet asphalt
    g.line((-10, gy - 110), (W + 10, gy - 110), INK, 6); g.line((-10, gy + 110), (W + 10, gy + 110), INK, 6)
    g.vgrad(gy + 110, H, (78, 124, 84), (56, 96, 64))                                # foreground grass
    lay = g.layer()
    for x, y, rx in ((160, gy - 40, 120), (620, gy + 70, 150), (940, gy - 70, 90)):
        lay.ellipse((x, y), (rx, 14), (190, 186, 180))
    g.blend(lay, 0.5)


def _cu_rain_bg(g):
    g.vgrad(0, 1300, (128, 112, 104), (180, 172, 164))
    tk.hills(g, 1240, 140, 600, (120, 124, 116)); tk.hills(g, 1320, 90, 360, (100, 116, 98), 2.0)
    for x in (60, 980): tk.pine(g, x, 1330, 1.5, snow=False)
    g.vgrad(1320, H, (100, 98, 102), (80, 78, 84))


def _desert_bg(g, gy, sunset=False):
    if sunset:
        g.vgrad(0, gy - 100, (150, 90, 130), (110, 180, 255))
    else:
        g.vgrad(0, gy - 100, (190, 226, 252), (170, 230, 255))
    dune1 = (110, 150, 220) if sunset else (130, 196, 240)
    dune2 = (90, 128, 200) if sunset else (110, 176, 226)
    tk.hills(g, gy - 230, 110, 700, dune1); tk.hills(g, gy - 160, 70, 420, dune2, 1.4)
    for x, s in ((90, 1.0), (980, 1.2)):
        cactus(g, x, gy - 150, s, (70, 120, 90) if sunset else (80, 150, 96))
    sand_top = (100, 150, 214) if sunset else (126, 190, 236)
    g.vgrad(gy - 160, gy - 110, sand_top, sand_top)
    g.vgrad(gy - 110, gy + 110, (96, 96, 104) if sunset else (120, 126, 136), (84, 84, 92) if sunset else (104, 108, 118))
    g.line((-10, gy - 110), (W + 10, gy - 110), INK, 6); g.line((-10, gy + 110), (W + 10, gy + 110), INK, 6)
    g.vgrad(gy + 110, H, sand_top, (84, 136, 200) if sunset else (104, 170, 224))
    rng = np.random.default_rng(4)
    for _ in range(40):
        x, y = rng.uniform(0, W), rng.uniform(gy + 140, H - 20)
        g.ellipse((x, y), (rng.uniform(20, 50), 5), (90, 140, 200) if sunset else (100, 164, 216))
    if sunset: g.tint((0.86, 0.92, 1.06))


def _cu_desert_bg(g):
    g.vgrad(0, 1300, (190, 226, 252), (170, 230, 255))
    tk.hills(g, 1240, 160, 700, (130, 196, 240)); tk.hills(g, 1320, 90, 420, (110, 176, 226), 1.4)
    g.vgrad(1320, H, (126, 190, 236), (104, 170, 224))


def _road_bg(g):
    g.vgrad(0, 1100, (170, 200, 250), (150, 214, 255))
    tk.hills(g, 1100, 60, 700, (120, 180, 232))
    g.vgrad(1100, H, (126, 190, 236), (100, 166, 222))
    g.poly([(520, 1100), (560, 1100), (900, H), (180, H)], (110, 116, 126))           # road to the horizon
    g.poly([(520, 1100), (180, H)], INK, 6, False); g.poly([(560, 1100), (900, H)], INK, 6, False)
    for i in range(7):
        u0, u1 = (i / 7) ** 1.8, ((i + .5) / 7) ** 1.8
        y0, y1 = lerp(1100, H, u0), lerp(1100, H, u1)
        w0, w1 = lerp(3, 18, u0), lerp(3, 18, u1)
        g.poly([(540 - w0, y0), (540 + w0, y0), (540 + w1, y1), (540 - w1, y1)], (120, 220, 250))
    cactus(g, 170, 1300, 1.3, (80, 150, 96)); cactus(g, 930, 1240, 1.0, (80, 150, 96))
    rng = np.random.default_rng(9)
    for _ in range(30):
        x, y = rng.uniform(0, W), rng.uniform(1200, H - 20)
        if abs(x - 540) > 120 + (y - 1100) * 0.45: g.ellipse((x, y), (rng.uniform(20, 46), 5), (100, 164, 216))


def bgs():
    if not BG:
        for name, fn in (("rain", lambda g: _rain_bg(g, 1390)), ("rain_cu", _cu_rain_bg), ("desert", lambda g: _desert_bg(g, 1390)),
                         ("desert_cu", _cu_desert_bg), ("road", _road_bg), ("sunset", lambda g: _desert_bg(g, 1390, True))):
            g = tk.G(); fn(g); BG[name] = g.img
    return BG


def bg(g):
    pass


# ------------------------------------------------------------------ props
def cactus(g, x, base, s, col):
    g.capsule((x, base), (x, base - 220 * s), col, 46 * s)
    g.capsule((x - 50 * s, base - 90 * s), (x - 50 * s, base - 160 * s), col, 30 * s); g.capsule((x - 50 * s, base - 90 * s), (x - 10 * s, base - 90 * s), col, 30 * s)
    g.capsule((x + 50 * s, base - 120 * s), (x + 50 * s, base - 190 * s), col, 30 * s); g.capsule((x + 50 * s, base - 120 * s), (x + 10 * s, base - 120 * s), col, 30 * s)


def bike(g, X, gy, k, d, t, spin=True, col=(70, 70, 76)):
    P = lambda dx, dy: (X + d * dx * k, gy + dy * k)
    R, F, BB, S_, HT, BAR = P(-150, -95), P(150, -95), P(-10, -85), P(-70, -250), P(110, -235), P(120, -305)
    a = t * 9 if spin else 0.4
    g.shade((X, gy + 4), 260 * k, 22 * k)
    for c in (R, F):
        g.circle(c, 95 * k + 6, INK); g.circle(c, 95 * k, (60, 60, 64)); g.circle(c, 80 * k, (228, 228, 232))
        for i in range(6):
            q = a * -d + i * math.pi / 3
            g.line(c, (c[0] + 78 * k * math.cos(q), c[1] + 78 * k * math.sin(q)), (150, 150, 156), max(2, 3 * k))
        g.disc(c, 12 * k, (150, 150, 156), 4)
    for p, q in ((R, BB), (R, S_), (S_, BB), (S_, HT), (BB, HT), (HT, F)):
        g.line(p, q, INK, 18 * k); g.line(p, q, col, 10 * k)
    g.line(HT, BAR, INK, 14 * k); g.line(BAR, P(150, -310), INK, 14 * k)
    g.oval((S_[0], S_[1] - 6 * k), (36 * k, 11 * k), (40, 40, 44), 4)
    pa = BB[0] + 42 * k * math.cos(a), BB[1] + 42 * k * math.sin(a)
    pb = BB[0] - 42 * k * math.cos(a), BB[1] - 42 * k * math.sin(a)
    g.line(BB, pa, INK, 8 * k); g.line(BB, pb, INK, 8 * k)
    return dict(seat=S_, bar=BAR, pa=pa, pb=pb, P=P)


def umbrella(g, hand, k, d, t, col=(70, 60, 200)):
    """A normal umbrella held at `hand`: dome on top, J handle below."""
    top = (hand[0], hand[1] - 190 * k)
    g.line((hand[0], hand[1] + 40 * k), top, INK, 10 * k)
    g.ellipse((hand[0] - d * 20 * k, hand[1] + 40 * k), (20 * k, 20 * k), INK, 9 * k, 0, 0, 180)
    w, h = 240 * k, 130 * k; c = top
    pts = [(c[0] + w * math.cos(a), c[1] - h * math.sin(a)) for a in np.linspace(0, math.pi, 30)]
    scal = []
    for i in range(6):
        x0, x1 = c[0] - w + i * 2 * w / 6, c[0] - w + (i + 1) * 2 * w / 6
        for u in np.linspace(0, 1, 6): scal.append((lerp(x1, x0, u) if False else lerp(x0, x1, u), c[1] - 22 * k * math.sin(u * math.pi)))
    g.poly(pts + scal, col); g.poly(pts + scal, INK, 7)
    for i in range(1, 6):
        x = c[0] - w + i * 2 * w / 6
        g.poly([(c[0], c[1] - h), (x, c[1] - 22 * k)], (40, 36, 150), 4, False)
    g.ellipse((c[0] - w * .35, c[1] - h * .6), (w * .25, h * .18), (120, 116, 240), 0, -20)
    g.line((c[0], c[1] - h), (c[0], c[1] - h - 24 * k), INK, 8 * k)
    return top


def bowl(g, hand, k, d, t, fill=1.0, col=(200, 140, 60), ripples=True, spill=0.0, bubbles=0.0):
    """The umbrella held UPSIDE DOWN like a bowl: canopy concave up, filled with rainwater, the J handle poking up through the water."""
    w, dep = 230 * k, 120 * k
    c = (hand[0], hand[1] - 150 * k - dep)              # rim centre
    apex = (c[0], c[1] + dep)
    g.line(hand, apex, INK, 10 * k)                       # short tip below the canopy, held in the hand
    arc = [(c[0] + w * math.cos(a), c[1] + dep * math.sin(a)) for a in np.linspace(0, math.pi, 34)]
    g.poly(arc, col)
    lvl = c[1] + dep * (1 - min(1.0, fill)) - (10 * k if fill >= 1 else 0)
    if fill > 0.02:
        ww = []
        for a in np.linspace(0, math.pi, 40):
            p = (c[0] + w * math.cos(a), c[1] + dep * math.sin(a))
            if p[1] >= lvl: ww.append(p)
        hw = w * math.sqrt(max(0.0, 1 - ((lvl - c[1]) / dep) ** 2)) if lvl > c[1] else w
        surf = [(c[0] - hw + u * 2 * hw, lvl - (8 * k * math.sin(u * math.pi) if fill >= 1 else 0) + 4 * k * math.sin(u * 14 + t * 8)) for u in np.linspace(0, 1, 24)]
        g.poly(ww + surf, WATER)
        g.poly(surf, (255, 248, 230), 6, False)
        if ripples:
            rng = np.random.default_rng(int(t * 6))
            for i in range(3):
                ph = (t * 2.2 + i / 3) % 1; x = c[0] + (rng.uniform(-.6, .6)) * hw
                g.ellipse((x, lvl + 6 * k), (10 * k + 40 * k * ph, 4 * k + 12 * k * ph), (255, 250, 240), 3, 0)
        if bubbles > 0:
            for i in range(5):
                ph = (t * 1.6 + i / 5) % 1; x = c[0] + (i - 2) * 30 * k + 6 * k * math.sin(t * 5 + i)
                g.circle((x, lerp(c[1] + dep * .8, lvl + 10 * k, ph)), (5 + 6 * ph) * k, (255, 250, 240), 3)
    # canopy edge ribs and scalloped rim drawn over the water edge
    g.poly(arc, INK, 7, False)
    for i in range(1, 6):
        a = i * math.pi / 6
        g.line(apex, (c[0] + w * math.cos(a), c[1] + dep * math.sin(a)), (130, 90, 40), 4)
    for i in range(7):
        x = c[0] - w + i * 2 * w / 6
        g.disc((x, c[1] + 3), 7 * k, (60, 60, 64), 3)
    g.line((c[0] - w, c[1]), (c[0] + w, c[1]), INK, 6)
    # the J handle sticks up out of the water: unmistakably upside down
    top = (c[0], c[1] - 150 * k)
    g.line((c[0], lvl if fill > 0.02 else apex[1]), top, INK, 11 * k)
    g.ellipse((top[0] + d * 22 * k, top[1]), (22 * k, 22 * k), INK, 10 * k, 0, 180, 360)
    g.line((top[0] + d * 44 * k, top[1]), (top[0] + d * 44 * k, top[1] + 14 * k), INK, 10 * k)
    if spill > 0:                                          # brimming over both edges
        for s in (-1, 1):
            e = (c[0] + s * w, c[1] - 2)
            tk.stream(g, e, (e[0] + s * 40 * k, e[1] + 260 * k * spill), t + s, 8 * k)
    return dict(c=c, w=w, dep=dep, lvl=lvl, apex=apex)


def tube(g, a, b, t, k=1.0, sag=60, flow=True, ctrl=None):
    mid = ctrl or ((a[0] + b[0]) / 2, max(a[1], b[1]) + sag)
    pts = tk.bezier(a, mid, b, 30)
    g.poly(pts, INK, 15 * k, False); g.poly(pts, (240, 230, 214), 9 * k, False)
    if flow:
        n = len(pts)
        for i in range(4):
            j = int(((t * 1.4 + i / 4) % 1) * (n - 1))
            g.circle(pts[j], 5 * k, (220, 160, 80))


def tears(g, head, t, k=1.0, d=1, n=3):
    """Laugh tears squirting sideways out of both eyes."""
    r = 84 * k
    for s, ex in ((-1, head[0] + d * r * .10), (1, head[0] + d * r * .62)):
        for i in range(n):
            ph = (t * 2.4 + i / n) % 1
            p = (ex + s * (30 + 150 * ph) * k, head[1] - r * .02 + (-30 * ph + 140 * ph * ph) * k)
            g.shape([(p[0] - 8 * k, p[1]), (p[0], p[1] - 18 * k), (p[0] + 8 * k, p[1]), (p[0] + 5 * k, p[1] + 8 * k), (p[0] - 5 * k, p[1] + 8 * k)], TEAR, 3, (150, 110, 40))


def rain_drops_into(g, b, t, k=1.0):
    """Drops landing in the bowl with small crown splashes."""
    for i in range(4):
        ph = (t * 2.6 + i * .27) % 1
        x = b["c"][0] + (i - 1.5) * b["w"] * 0.42
        y0 = b["lvl"] - 420 * k
        if ph < 0.7:
            y = lerp(y0, b["lvl"], ph / 0.7)
            g.line((x + 10 * k, y - 34 * k), (x, y), (250, 240, 220), 5)
        else:
            tk.splash(g, (x, b["lvl"]), (ph - 0.7) / 0.3, 6, 60 * k, WATER, seed=i)


# ------------------------------------------------------------------ riders
def rider(g, who, X, gy, k, t, d=1, spin=True, face=None, hand_bar=True, rh=None, lh=None, bob=0.0):
    b = bike(g, X, gy, k, d, t, spin)
    S_ = b["seat"]
    gyf = S_[1] - 12 * k + 232 * k + bob
    face = face or {}
    lh = lh if lh is not None else (b["bar"] if hand_bar else None)
    a = tk.fig(g, who, S_[0], gyf, d, t, k=k, lean=40 * k, feet=[(b["pa"][0], b["pa"][1] - 4 * k), (b["pb"][0], b["pb"][1] - 4 * k)],
               lh=lh, rh=rh, shadow=False, **face)
    a["P"] = b["P"]; a["bar"] = b["bar"]
    return a


def hand_pt(X, gy, k, d, dx, dy):
    return (X + d * dx * k, gy + dy * k)


# ------------------------------------------------------------------ shots
def scroll_marks(g, t, gy, speed=900, col=(220, 220, 220)):
    for i in range(8):
        x = (i * 260 - t * speed) % 2080 - 300
        g.rect((x, gy - 6), (x + 120, gy + 6), col, 0)


def speed_streaks(g, c, t, d=1, n=4):
    for i in range(n):
        y = c[1] + (i - n / 2) * 34; L = 70 + 40 * ((i * 7 + int(t * 20)) % 3)
        g.line((c[0] - d * 30, y), (c[0] - d * (30 + L), y), (250, 250, 250), 5)


def ride(g, t, n, desert=False):
    """Wide two-shot on bikes. Cap behind (far lane, left), Specs in front (near lane, right)."""
    if not desert:
        scroll_marks(g, t, 1390, 900, (200, 200, 200))
        if 0.35 <= t < 0.6 and int(t * 30) % 2 == 0:
            tk.bolt(g, (900, -20), (760, 420), 4, 10)
    else:
        scroll_marks(g, t, 1390, 900, (120, 220, 250))
    # Cap
    kc, Xc = 0.92, 330
    bobc = 6 * abs(math.sin(t * 14)) if not desert else 0
    if desert:
        face = dict(eyes="sleepy", mouth="tongue", blush=1.0, sweat=5, brows="worried")
        rhc = None; hb = True
    else:
        face = dict(eyes="squeeze", mouth="laugh")
        rhc = hand_pt(Xc, GY_FAR, kc, 1, 175, -455)
        hb = False
    shade_hand = hand_pt(Xc, GY_FAR, kc, 1, -125, -505)
    a = rider(g, "cap", Xc, GY_FAR, kc, t, 1, face=face, hand_bar=hb, rh=rhc if not desert else shade_hand, lh=shade_hand if not desert else None, bob=bobc)
    umbrella(g, shade_hand, kc, 1, t, (64, 64, 200))
    if not desert:
        tk.laugh_marks(g, a["head"], t)
        g.line(a["rh"], (a["rh"][0] + 46, a["rh"][1] - 10), INK, 9)            # pointing finger
        tears(g, a["head"], t, 0.92, 1, 2)
    else:
        g.glow(a["head"], 200, (0, 0, 60), 0.5)
        tk.drops(g, a["head"], t, 3, 110, TEAR, 1.8)
    speed_streaks(g, a["P"](-260, -200), t)
    # Specs
    ks, Xs = 1.0, 725
    hs = hand_pt(Xs, GY_NEAR, ks, 1, 100, -505)
    sface = dict(eyes="happy", mouth="smile") if not desert else dict(eyes="happy", mouth="smile", look=(0.4, 0))
    s = rider(g, "specs", Xs, GY_NEAR, ks, t, 1, face=sface, lh=hs, rh=hand_pt(Xs, GY_NEAR, ks, 1, 120, -305))
    fill = sm(t / 2.4) * 0.6 + 0.4 if not desert else 1.0
    b = bowl(g, hs, ks, 1, t, fill, ripples=not desert)
    if not desert:
        rain_drops_into(g, b, t)
    else:
        tk.sparkles(g, (b["c"][0], b["lvl"] - 30), t, 4, 150, 16, (255, 255, 255))
    speed_streaks(g, s["P"](-260, -200), t)
    return a, s, b


def draw(g, t, n):
    i = shot_at(t); t0, t1, bgname, kind = SHOTS[i]
    np.copyto(g.img, bgs()[bgname])
    e = t - t0
    if kind == "ride_rain":
        ride(g, t, n)
        tk.rain(g, n, 1.0)
    elif kind == "cap_laugh":
        k, X = 1.9, 470
        hold = hand_pt(X, GY_CU, k, 1, -125, -505)
        bob = 26 * abs(math.sin(t * 15))
        a = rider(g, "cap", X, GY_CU, k, t, 1, spin=False, face=dict(eyes="squeeze", mouth="laugh", blush=0.5),
                  hand_bar=True, rh=hand_pt(X, GY_CU, k, 1, 60, -300), lh=hold, bob=bob)
        umbrella(g, (hold[0], hold[1] + bob), k, 1, t, (64, 64, 200))
        tk.laugh_marks(g, (a["head"][0] - 60, a["head"][1]), t)
        tk.laugh_marks(g, (a["head"][0] + 420, a["head"][1]), t, -1)
        tears(g, a["head"], t, k, 1, 3)
        tk.rain(g, n, 0.8)
    elif kind == "bowl_cu":
        k, X = 1.6, 470
        hs = hand_pt(X, GY_CU + 120, k, 1, 100, -505)
        s = rider(g, "specs", X, GY_CU + 120, k, t, 1, spin=False, face=dict(eyes="happy", mouth="smile", look=(0.2, -1)), lh=hs, rh=hand_pt(X, GY_CU + 120, k, 1, 120, -305))
        b = bowl(g, hs, k, 1, t, 1.0, spill=min(1.0, 0.4 + e / 1.2))
        rain_drops_into(g, b, t, k)
        for j in range(3):                                  # big drops splashing out over the rim
            u = ((e * 1.3) + j / 3) % 1
            tk.splash(g, (b["c"][0] + (j - 1) * b["w"] * 0.5, b["lvl"]), u, 8, 180, WATER, seed=11 + j)
        tk.rain(g, n, 0.8)
    elif kind == "specs_wait":
        k, X = 1.9, 520
        hs = hand_pt(X, GY_CU, k, 1, 100, -505)
        s = rider(g, "specs", X, GY_CU, k, t, 1, spin=False, face=dict(eyes="sleepy", mouth="smile", brows="flat", look=(1, 0)), lh=hs, rh=hand_pt(X, GY_CU, k, 1, 120, -305))
        bowl(g, hs, k, 1, t, 1.0)
        if e > 0.6: tk.sparkle(g, (s["head"][0] + 120, s["head"][1] - 40), 26 * out_pop(e - 0.6), WHITE, 7)
        if e > 0.9: tk.bulb(g, (s["head"][0] - 230, s["head"][1] - 260), (e - 0.9) / 0.4, t)
        tk.rain(g, n, 0.7)
    elif kind == "next_day":
        u = sm(e / 1.5)
        sy = lerp(1120, 760, u)
        g.glow((540, sy), 900, (40, 90, 140), 0.7)
        tk.sun(g, (540, sy), t, 170, (110, 214, 255))
        g.vgrad(1100, 1104, (100, 166, 222), (100, 166, 222))  # horizon line hides the rising sun's lower part
        heat_lines(g, t, 1150, 1400)
    elif kind == "ride_desert":
        tk.sun(g, (880, 300), t, 110, (110, 214, 255))
        ride(g, t, n, desert=True)
        heat_lines(g, t, 560, 900)
    elif kind == "cap_jealous":
        k, X = 1.9, 520
        hold = hand_pt(X, GY_CU, k, 1, -125, -505)
        tremble = 5 * math.sin(t * 50)
        a = rider(g, "cap", X + tremble, GY_CU, k, t, 1, spin=False,
                  face=dict(eyes="open", mouth="wavy", brows="worried", look=(1, 0.2), blush=1.0, sweat=6), lh=hold)
        umbrella(g, hold, k, 1, t, (64, 64, 200))
        g.glow(a["head"], 320, (0, 0, 80), 0.5)
        steam(g, a["top"], t, k)
    elif kind == "specs_sip":
        k, X = 1.6, 470
        hs = hand_pt(X, GY_CU + 120, k, 1, 100, -505)
        s = rider(g, "specs", X, GY_CU + 120, k, t, 1, spin=False, face=dict(eyes="closed", mouth="smile", blush=0.35), lh=hs, rh=hand_pt(X, GY_CU + 120, k, 1, 120, -305))
        b = bowl(g, hs, k, 1, t, 1.0 - 0.15 * sm(e / 2.0), ripples=False, bubbles=1.0)
        mouth = (s["head"][0] + 0.36 * 84 * k, s["head"][1] + 0.5 * 84 * k)
        tube(g, (b["c"][0] + 0.86 * b["w"], b["lvl"] + 14 * k), mouth, t, k, ctrl=(b["c"][0] + 1.25 * b["w"], mouth[1] + 40 * k))
        hearts(g, (s["head"][0] - 220, s["head"][1] - 160), t)
        tk.sparkles(g, s["head"], t, 5, 200, 18)
    elif kind == "share":
        share(g, t, e)


def out_pop(u):
    return tk.out_back(u / 0.3)


def heat_lines(g, t, y0, y1):
    lay = g.layer()
    for i in range(6):
        x = 100 + i * 170; y = y1 - ((t * 120 + i * 90) % (y1 - y0))
        pts = [(x + 14 * math.sin(v * 8 + t * 6 + i), y - v * 120) for v in np.linspace(0, 1, 10)]
        lay.poly(pts, (220, 240, 255), 5, False)
    g.blend(lay, 0.45)


def steam(g, top, t, k):
    lay = g.layer()
    for i in range(3):
        ph = (t * 1.5 + i / 3) % 1
        x = top[0] + (i - 1) * 60 * k + 10 * math.sin(t * 6 + i)
        lay.poly([(x + 12 * math.sin(v * 7 + t * 8), top[1] - 30 - ph * 160 - v * 80) for v in np.linspace(0, 1, 8)], (250, 250, 250), 8, False)
    g.blend(lay, 0.6)


def hearts(g, c, t):
    for i in range(3):
        ph = (t * 0.7 + i / 3) % 1; s = 0.8 + 0.6 * ph
        p = (c[0] + 40 * math.sin(t * 3 + i * 2), c[1] - 200 * ph)
        col = (120, 100, 250)
        g.circle((p[0] - 12 * s, p[1]), 14 * s + 4, INK); g.circle((p[0] + 12 * s, p[1]), 14 * s + 4, INK)
        g.poly([(p[0] - 27 * s, p[1] + 5 * s), (p[0] + 27 * s, p[1] + 5 * s), (p[0], p[1] + 34 * s)], INK, 8)
        g.circle((p[0] - 12 * s, p[1]), 14 * s, col); g.circle((p[0] + 12 * s, p[1]), 14 * s, col)
        g.poly([(p[0] - 25 * s, p[1] + 5 * s), (p[0] + 25 * s, p[1] + 5 * s), (p[0], p[1] + 30 * s)], col)


def share(g, t, e):
    tk.sun(g, (540, 980), t, 120, (90, 170, 255))
    g.vgrad(1080, 1084, (110, 150, 220), (110, 150, 220))
    k = 1.0
    # Cap on the left facing right, Specs on the right facing left; bikes stopped nose to nose
    Xc, Xs, gy = 290, 790, GY_NEAR
    laughing = e > 1.75
    hs = hand_pt(Xs, gy, k, -1, 100, -505)
    # tube end: Specs's mouth -> passed across -> Cap's mouth
    cap_mouth_est = (Xc + (-70 + 40 + 10 + 0.36 * 84) * k, gy + (-250 - 12 - 172 - 92 + 42) * k)
    specs_mouth_est = (Xs - (-70 + 40 + 10 + 0.36 * 84) * k, gy + (-250 - 12 - 172 - 92 + 42) * k)
    mid = (540, 920)
    u1, u2 = sm((e - 0.2) / 0.5), sm((e - 0.8) / 0.5)
    end = lerp2(lerp2(specs_mouth_est, mid, u1), cap_mouth_est, u2)
    cap_rh = end if e > 0.8 else None
    specs_lh = end if e < 1.0 else None
    if laughing:
        cface = dict(eyes="squeeze", mouth="laugh", bob=0)
        sface = dict(eyes="squeeze", mouth="laugh")
    else:
        cface = dict(eyes="closed" if e > 1.2 else "wide", mouth="o" if e > 1.2 else "o", brows=None if e > 1.2 else "worried")
        sface = dict(eyes="happy", mouth="smile")
    bob = 8 * abs(math.sin(t * 15)) if laughing else 0
    cface.pop("bob", None)
    a = rider(g, "cap", Xc, gy, k, t, 1, spin=False, face=cface, rh=cap_rh if not laughing else hand_pt(Xc, gy, k, 1, 60, -360), bob=bob)
    s = rider(g, "specs", Xs, gy, k, t, -1, spin=False, face=sface, lh=hs, rh=specs_lh if specs_lh is not None else hand_pt(Xs, gy, k, -1, 120, -305), bob=bob)
    b = bowl(g, hs, k, -1, t, 0.85, ripples=False)
    tend = end if not laughing else (a["rh"][0] + 10, a["rh"][1] - 10)
    tube(g, (b["c"][0] + 40, b["lvl"] + 30), tend, t, k, 80, flow=not laughing)
    if laughing:
        tk.laugh_marks(g, a["head"], t); tk.laugh_marks(g, s["head"], t, -1)
        tk.sparkles(g, (540, 760), t, 6, 260, 18, (200, 240, 255))
    if 1.3 < e < 1.75:
        tk.sparkles(g, a["head"], t, 4, 130, 14)


# ------------------------------------------------------------------ camera
CAMS = {  # per shot: keyframes in shot-local time (cx, cy, zoom)
    "ride_rain": [(0.0, (760, 820, 1.4)), (0.9, (740, 840, 1.34)), (2.0, (560, 980, 1.02)), (2.6, (540, 980, 1.0))],
    "cap_laugh": [(0.0, (560, 760, 1.18)), (2.0, (580, 740, 1.36))],
    "bowl_cu": [(0.0, (650, 560, 1.42)), (2.2, (640, 620, 1.22))],
    "specs_wait": [(0.0, (620, 760, 1.12)), (2.0, (660, 720, 1.34))],
    "next_day": [(0.0, (540, 1000, 1.3)), (1.5, (540, 960, 1.04))],
    "ride_desert": [(0.0, (380, 860, 1.3)), (0.8, (540, 930, 1.08)), (2.3, (540, 960, 1.0))],
    "cap_jealous": [(0.0, (560, 780, 1.12)), (1.8, (600, 740, 1.38))],
    "specs_sip": [(0.0, (620, 740, 1.32)), (2.2, (600, 800, 1.1))],
    "share": [(0.0, (540, 900, 1.3)), (1.0, (540, 940, 1.12)), (2.0, (540, 960, 1.04)), (3.4, (540, 960, 1.0))],
}


def cam(t):
    i = shot_at(t); t0, t1, _, kind = SHOTS[i]
    e = t - t0
    cx, cy, z = key(e, CAMS[kind])
    z = min(1.5, z * (1 + 0.07 * max(0.0, 1 - e / 0.25)))          # punch-in on every cut
    dx = dy = 0.0
    if kind == "cap_laugh": dy += 10 * abs(math.sin(t * 15))
    if kind == "cap_jealous":
        s = tk.shake(t, t0, 0.6, 24); dx += s[0] + 3 * math.sin(t * 60); dy += s[1]
    if kind == "ride_rain":
        s = tk.shake(t, 0.35, 0.4, 14); dx += s[0]; dy += s[1]
    if kind == "share" and e > 1.75: dy += 6 * abs(math.sin(t * 15))
    _NOW[0] = t
    return (cx + dx, cy + dy, z)


# ------------------------------------------------------------------ screen-space overlay (after the camera)
_NOW = [0.0]
_fc = {}


def font(p, s):
    if (p, s) not in _fc: _fc[(p, s)] = ImageFont.truetype(p, s)
    return _fc[(p, s)]


def text_rgba(txt, size, fp=ARCH, stroke=9, fill=(255, 255, 255), maxw=980):
    f = font(fp, size)
    bb = ImageDraw.Draw(Image.new("L", (4, 4))).textbbox((0, 0), txt, font=f, stroke_width=stroke)
    if bb[2] - bb[0] > maxw: return text_rgba(txt, int(size * maxw / (bb[2] - bb[0])), fp, stroke, fill, maxw)
    im = Image.new("RGBA", (bb[2] - bb[0] + 40, bb[3] - bb[1] + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((20 - bb[0] + 6, 20 - bb[1] + 8), txt, font=f, fill=(0, 0, 0, 120), stroke_width=stroke, stroke_fill=(0, 0, 0, 120))
    d.text((20 - bb[0], 20 - bb[1]), txt, font=f, fill=fill + (255,), stroke_width=stroke, stroke_fill=(20, 20, 24, 255))
    return im


def paste(fr, im, cx, cy, sc=1.0, a=1.0):
    if a <= 0.01 or sc <= 0.02: return fr
    if sc != 1.0: im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
    L = np.asarray(im).astype(np.float32)
    x0, y0 = int(cx - im.width / 2), int(cy - im.height / 2)
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + im.width), min(H, y0 + im.height)
    if xb <= xa or yb <= ya: return fr
    L = L[ya - y0:yb - y0, xa - x0:xb - x0]; al = L[..., 3:4] / 255 * a
    reg = fr[ya:yb, xa:xb].astype(np.float32)
    fr[ya:yb, xa:xb] = (reg * (1 - al) + L[..., 2::-1] * al).astype(np.uint8)
    return fr


CAPIM = {}
CRED = {}
_YY = _XX = None


def overlays(fr, t):
    global _YY, _XX
    if not CAPIM:
        for c in CAPS: CAPIM[c[0]] = text_rgba(c[0], 112 if c[0] in ("HAHAHA", "50°C") else 84)
        CRED["1"] = text_rgba("مونتاج وإخراج Mahmoud Elkosif", 58, CAIRO, 6)
        CRED["2"] = text_rgba("تابعني على فيسبوك", 50, CAIRO, 5, (255, 220, 120))
    i = shot_at(t); t0, _, _, kind = SHOTS[i]; e = t - t0
    if kind in ("ride_desert", "specs_sip", "cap_jealous"):                  # heat haze
        if _YY is None:
            _YY, _XX = np.mgrid[0:H, 0:W].astype(np.float32)
        amp = np.clip((_YY - H * 0.4) / (H * 0.6), 0, 1) * 2.5
        fr = cv2.remap(fr, _XX + amp * np.sin(_YY / 23.0 + t * 7.0), _YY, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    if i > 0 and e < 0.13:                                                   # whip in: motion blur + flash
        u = e / 0.13
        kk = int(70 * (1 - u)) | 1
        fr = cv2.filter2D(fr, -1, np.full((1, kk), 1 / kk, np.float32))
        fr = cv2.addWeighted(fr, 1, np.full_like(fr, 255), 0.3 * (1 - u), 0)
    nxt = [c for c in CUTS if 0 < c - t <= 0.07]
    if nxt:                                                                 # whip out
        u = 1 - (nxt[0] - t) / 0.07
        kk = int(50 * u) | 1
        fr = cv2.filter2D(fr, -1, np.full((1, kk), 1 / kk, np.float32))
    if kind == "share":
        fr = cv2.addWeighted(fr, 1, np.full_like(fr, (30, 80, 150)), 0.06, 0)
    for txt, c0, c1, y in CAPS:
        if c0 <= t <= c1:
            s = 0.6 + 0.4 * tk.out_back((t - c0) / 0.28)
            al = min(1, (c1 - t) / 0.15, (t - c0) / 0.06 + 0.3)
            fr = paste(fr, CAPIM[txt], W / 2, y, s, al)
    if t > 18.2:
        k = sm((t - 18.2) / 0.4)
        gr = np.clip((np.arange(H) - 1380) / 200, 0, 1)[:, None, None] * 0.62 * k
        fr = (fr * (1 - gr)).astype(np.uint8)
        fr = paste(fr, CRED["1"], W / 2, 1520 + 40 * (1 - k), 1, k)
        fr = paste(fr, CRED["2"], W / 2, 1620 + 40 * (1 - k), 1, k)
    return fr


_crop = tk.camera_crop


def _crop_post(canvas, cx, cy, zoom):
    return overlays(_crop(canvas, cx, cy, zoom), _NOW[0])


tk.camera_crop = _crop_post            # tk.run calls cam(t) then camera_crop: captions land in screen space, watermark on top


# ------------------------------------------------------------------ sound
def audio(path):
    m = tk.Mix(D, seed=42)
    # rain block (shots 1-4)
    m.sfx("rain_storm", 0, 0.5, dur=8.9, loop=True, fade=0.4)
    m.sfx("thunder_mid", 0.1, 0.5, dur=4.0)
    m.sfx("thunder_close", 0.35, 0.35, dur=2.5, fade=0.05)
    for tt in np.arange(0.0, 2.6, 0.45): m.tone(tt, 2400, 0.05, 0.03, 30)          # chain ticking
    m.ding(0.2, 0.12)                                                              # bike bell
    m.sfx("fill", 0.3, 0.22, dur=2.2)
    m.sfx("laugh_male", 1.6, 0.4)
    m.sfx("laugh_cartoon", 2.6, 0.8, dur=2.0)
    m.sfx("laugh_cartoon2", 3.6, 0.45)
    m.boing(3.0, 0.12); m.boing(3.8, 0.1)
    m.sfx("fill", 4.6, 0.6, dur=2.2)
    m.sfx("splash_big", 5.0, 0.3, dur=1.2); m.sfx("drips", 5.4, 0.4, dur=1.4)
    m.sfx("drips", 6.8, 0.35, dur=2.0)
    m.ding(7.7, 0.14)                                                              # idea bulb
    m.sfx("thunder_mid", 7.0, 0.25, dur=1.8)
    m.sfx("whoosh", 8.75, 0.6, dur=0.8)
    # desert block (shots 5-8)
    m.sfx("wind_storm", 8.8, 0.2, dur=7.8, loop=True, fade=0.5)
    m.rise(8.9, 1.3, 200, 700, 0.06)                                               # sun rising
    m.thump(10.3, 0.5)
    for tt in np.arange(10.3, 12.6, 0.45): m.tone(tt, 2200, 0.05, 0.025, 30)
    m.tone(11.0, 700, 0.6, 0.08, 3, 400); m.tone(11.8, 650, 0.6, 0.08, 3, 380)    # Cap panting
    m.boing(12.6, 0.3); m.slide_down(12.9, 0.12)
    m.noise(12.7, 0.6, 0.15, 3, 2)                                                 # sizzle
    m.sfx("pour", 14.45, 0.35, dur=1.5)
    m.sfx("bubble", 14.6, 0.55, dur=1.9)
    m.ding(15.2, 0.12)
    # sunset
    m.sfx("pour", 16.9, 0.25, dur=1.0); m.sfx("pop", 17.4, 0.25)
    m.sfx("bubble", 17.5, 0.35, dur=0.8)
    m.sfx("giggle", 16.8, 0.5, dur=1.8); m.sfx("laugh_male", 18.35, 0.5); m.sfx("laugh_cartoon2", 18.6, 0.4)
    m.sfx("birds_river", 16.6, 0.12, dur=3.4, fade=0.6)
    m.tune(0.0, 8.8, 1.0, 0.45, minor=True)
    m.tune(8.8, 16.6, 1.15, 0.45)
    m.tune(16.6, 20.0, 1.0, 0.6)
    m.tada(18.2, 0.3)
    for c in CUTS:                                                                 # every cut: whoosh + noise hit
        m.sfx("whoosh", c - 0.12, 0.35, dur=0.35, rate=1.3)
        m.noise(c - 0.05, 0.15, 0.3, 3, 18); m.thump(c, 0.25, 140)
    m.save(path)


if __name__ == "__main__":
    out = sys.argv[1]
    aud = None
    if "--stills" not in sys.argv:
        aud = out.replace(".mp4", ".m4a"); audio(aud)
    tk.run(out, D, bg, draw, cam, aud)
