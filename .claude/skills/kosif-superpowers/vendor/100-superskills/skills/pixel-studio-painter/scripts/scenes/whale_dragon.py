"""الحوت والتنين — a humpback whale breaches out of a storm sea as a dragon dives on it, fire against water.

PROMPT (what this program paints):
  Photorealistic cinematic dark-fantasy still, 16:9. Night storm over open ocean. A colossal humpback whale
  breaches diagonally out of the sea in the right foreground, belly and throat pleats toward the camera, long
  white pectoral fin raised, knobbed head, mouth line running back to a small eye; water sheets off its flanks
  and explodes into spray. From the upper left an ancient dragon dives at it with wings spread, scaled hide,
  and unleashes a torrent of fire that meets the spray between them in a burst of steam. Lightning behind the
  clouds is the cold key light (steel blue); the fire is the warm key (amber-orange); the sea mirrors both.
  Heavy rain, airborne spray, deep blacks, volumetric mist, high dynamic range, physically believable water and
  fire, no cartoon look, no text.

Version 6: a real humpback profile built in its own frame and rotated into the breach; skin with subsurface
scattering and detail at three scales; a camera: background depth of field, motion-blurred rain and spray,
highlight bloom, a lens flare from the fire, chromatic fringing and filmic tone mapping.
"""
from __future__ import annotations

import math
import random

from dragon_girl import cloud, flame, spikes, tongue, wing
from render import (Step, bloom, catmull, chroma, defocus, dots, ellipse, fill, filmic, flare, glow, grain, lin,
                    motion_blur, noise, path, poly, rad, rect, relief, rim, scales, stroke, translate, tube, union,
                    vignette, water)

TITLE = "الحوت والتنين"
ROLLOFF = 1.0                          # the filmic curve does the tone mapping
TOP, BOTTOM = 62, 738
HORIZON = 468
BOLT = (1010, 120)
MOUTH = (628, 396)
IMPACT = (712, 338)
FIRE = (684, 356)
COLD = (BOLT[0], BOLT[1], 520, "#cfe0ff", 1.0)
WARM = (FIRE[0], FIRE[1], 150, "#ff8a3a", 1.7)
AMBIENT_SKY = (600, -400, 900, "#5a6c88", 0.35)
LIGHTS = [COLD, WARM, AMBIENT_SKY]

# the whale's own frame: x along the body from the snout (0) to the tail (700), y down toward the belly
HEAD, TAIL = (700, 290), (1200, 760)
_TH = math.atan2(TAIL[1] - HEAD[1], TAIL[0] - HEAD[0])
_C, _S = math.cos(_TH), math.sin(_TH)


def W(x, y):
    """Whale frame -> scene."""
    return (HEAD[0] + x * _C - y * _S, HEAD[1] + x * _S + y * _C)


def WS(shape):
    return [[W(x, y) for x, y in q] for q in shape]


def rain(seed, n, x0, x1, y0, y1, length, width, slant=-0.25):
    r = random.Random(seed)
    out = []
    for _ in range(n):
        x, y = r.uniform(x0, x1), r.uniform(y0, y1)
        ln = length * r.uniform(.6, 1.3)
        out.append([(x, y), (x + slant * ln, y + ln)])
    return stroke(out, width)


def spray(seed, cx, cy, n, sx, sy, up=1.0, sizes=(1, 1.4, 2, 2.8)):
    r = random.Random(seed)
    return [(cx + r.gauss(0, sx), cy - abs(r.gauss(0, sy)) * up + r.gauss(0, 6), r.choice(sizes)) for _ in range(n)]


def foam(seed, y, amp, n=26, x0=-40, x1=1240):
    r = random.Random(seed)
    pts = [(x0 + (x1 - x0) * k / n, y + math.sin(k * 1.7 + seed) * amp + r.uniform(-amp * .3, amp * .3)) for k in range(n + 1)]
    out = []
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        for k in range(6):
            t = k / 6
            out.append((ax + (bx - ax) * t + r.uniform(-3, 3), ay + (by - ay) * t + r.uniform(-2, 2), r.choice([1.2, 1.8, 2.6])))
    return out


def build() -> list[Step]:
    S: list[Step] = []

    # 1. sky
    S.append(Step("السماء العاصفة", [
        fill(rect(0, 0, 1200, 800), lin((0, TOP), (0, HORIZON), [(0, "#05070c"), (.4, "#0e141e"), (.8, "#1f2835"), (1, "#2e3947")])),
        noise(rect(0, TOP, 1200, HORIZON - TOP), .35, 160, 11, "multiply", octaves=3),
        glow(ellipse(*BOLT, 420, 260), "#5f7fb3", 120, .55)],
        "sweep", weight=1.2))

    # 2. clouds as soft volumes
    deck = union(cloud(300, 150, 700, 120, 20, 41), cloud(820, 110, 760, 110, 20, 42), cloud(560, 250, 1000, 70, 18, 43))
    S.append(Step("الغيوم الركامية", [
        fill(deck, "#0b0f17", .9, blur=20),
        relief(deck, [COLD, (FIRE[0], FIRE[1], 260, "#ff7a2a", .9), AMBIENT_SKY], "#1c2430", .25, .9, .7, 8, .08,
               bumps=[(14, 46), (5, 14)], seed=12, soft=5, sss=8),
        fill(deck, "#0b0f17", .35, blur=16),
        fill(rect(-50, 380, 1300, 110), "#54637a", .2, blur=34, mode="screen")],
        "sweep", weight=1.0))

    # 3. lightning
    r = random.Random(7)
    bolt = [(BOLT[0], TOP + 10)]
    while bolt[-1][1] < 430:
        bolt.append((bolt[-1][0] + r.uniform(-30, 18), bolt[-1][1] + r.uniform(18, 34)))
    br = [bolt[5]] + [(bolt[5][0] + 30 + 24 * k, bolt[5][1] + 22 * k + r.uniform(-6, 6)) for k in range(1, 5)]
    S.append(Step("البرق", [
        glow(stroke([bolt, br], 10), "#8fb4ff", 30, .7),
        fill(stroke([bolt], 2.6), "#f6f9ff"), fill(stroke([br], 1.5), "#dde9ff", .9),
        fill(rect(0, TOP, 1200, HORIZON - TOP), rad(BOLT, 700, [(0, "#9fbcf0"), (1, "#9fbcf000")]), .18, mode="screen")],
        "down", origin=BOLT, weight=.5))

    # 4. the sea
    sea = rect(-50, HORIZON, 1300, BOTTOM + 50 - HORIZON)
    S.append(Step("البحر الهائج", [
        water(sea, [COLD, (FIRE[0], FIRE[1], 90, "#ff8a3a", 2.2), AMBIENT_SKY], "#060a0f", "#28323f", 20, 7, 7, 21, 70, 1.1),
        fill(sea, lin((0, HORIZON), (0, HORIZON + 60), [(0, "#4a5a6c"), (1, "#4a5a6c00")]), .5),
        *[fill(dots(foam(s, y, a)), "#dfe9f5", al, blur=2.6) for s, y, a, al in
          ((1, 496, 3, .16), (2, 532, 5, .2), (3, 584, 8, .28), (4, 648, 11, .34), (5, 712, 14, .4))],
        *[fill(dots(foam(s + 10, y, a, 40)), "#ffffff", .2, blur=1.0) for s, y, a in ((3, 584, 8), (4, 648, 11), (5, 712, 14))],
        *[fill(cloud(x, y, w, 10, 6, 70 + k), "#e8f0f8", .4, blur=4, mode="screen") for k, (x, y, w) in
          enumerate(((180, 660, 120), (420, 700, 150), (300, 590, 90), (560, 730, 110)))],
        fill(rect(-50, 440, 1300, 60), "#7f93ad", .26, blur=26, mode="screen")],
        "sweep", weight=1.2))

    # 5. the far swell, then the lens focuses on the subjects: everything so far goes slightly soft
    wall = path("M 520 520 C 600 452 760 404 900 392 C 1020 382 1140 398 1250 440 L 1250 640 L 520 640 Z")
    S.append(Step("جدار الموج وعمق المجال", [
        fill(wall, lin((0, 390), (0, 640), [(0, "#36465a"), (.5, "#17222e"), (1, "#17222e00")]), .95, blur=6),
        noise(wall, .45, 30, 23, "multiply", octaves=3, stretch=(3.0, 1.0)),
        fill(wall, rad(BOLT, 800, [(0, "#8eaad8"), (1, "#8eaad800")]), .25, mode="screen"),
        fill(dots(foam(9, 418, 10, 22, 600, 1250)), "#dfe9f5", .5, blur=1.5),
        fill(dots(spray(31, 900, 420, 160, 230, 30, 1.2, (1, 1.5, 2))), "#e9f1fb", .55, blur=.6),
        defocus(2.2)],
        "right", weight=.7))

    # 6. the dragon
    fw_mem, fw_bones, fw_veins = wing((300, 240), (390, 90), (470, -20), [(680, -40), (760, 70), (700, 180), (580, 250)], (400, 300), sag=.3)
    S.append(Step("جناح التنين البعيد", [
        relief(fw_mem, LIGHTS, "#1a2030", .2, .12, .3, 18, .25, bumps=[(1.5, 14), (.4, 4)], seed=51, fresnel=.5, fres_col="#8fa8d0", sss=3),
        fill(fw_mem, rad(FIRE, 420, [(0, "#ff7a2a"), (1, "#ff7a2a00")]), .25, mode="add"),
        fill(fw_veins, "#0a0d14", .7),
        relief(fw_bones, LIGHTS, "#141820", .2, .8, .5, 30, .5, fresnel=.3),
        defocus(1.2)],
        "grow", origin=(300, 240), weight=.7))

    spine = [(40, 120), (120, 160), (210, 214), (310, 272), (410, 318), (500, 348), (570, 372)]
    radii = [28, 42, 56, 66, 64, 54, 40]
    body = tube(spine, radii)
    neck_head = path("M 552 330 C 576 318 606 322 630 338 C 646 348 658 352 672 364 C 690 380 702 396 708 412 L 680 420 "
                     "C 666 410 652 404 640 402 L 610 406 L 650 436 C 660 446 652 454 640 450 C 612 442 586 424 570 402 "
                     "C 556 386 548 356 552 330 Z")
    horns = union(tube([(560, 332), (530, 296), (496, 270), (460, 258)], [11, 8.5, 5, 1.2]),
                  tube([(574, 326), (552, 288), (522, 258), (492, 242)], [8.5, 6.5, 3.8, 1]),
                  tube([(566, 352), (540, 356), (520, 372)], [6, 4, 1]), tube([(572, 372), (552, 384), (538, 402)], [5, 3.5, 1]))
    brow = path("M 596 340 C 612 334 628 338 640 350 C 630 348 616 348 600 352 Z")
    teeth = union(*[poly([(x, y), (x + 6, y - 1), (x + 3, y + 10)]) for x, y in [(646, 404), (660, 408), (674, 414)]],
                  *[poly([(x, y), (x + 6, y + 1), (x + 2.5, y - 8)]) for x, y in [(646, 430), (662, 436)]])
    legs = union(tube([(440, 340), (470, 410), (448, 470)], [28, 18, 12]),
                 *[tube([(448, 470), (448 + ex, 470 + ey)], [6, 1.2], n=4) for ex, ey in [(-28, 12), (-10, 24), (12, 22)]],
                 tube([(230, 236), (214, 312), (180, 360)], [22, 14, 9]))
    back = spikes(spine, radii, every=4, size=1.7)
    hide = union(body, neck_head, legs)
    S.append(Step("جسد التنين", [
        relief(union(hide, back), LIGHTS, lin((40, 120), (570, 420), [(0, "#1c1a20"), (.5, "#2a1a12"), (1, "#20160f")]),
               .14, .6, .42, 22, .35, bumps=[(2.4, 22), (1.2, 6), (.4, 2.5)], seed=52, fresnel=.3, fres_col="#8fa8d0",
               roughness=.6, sss=2),
        scales(hide, 8, "#000000", .22, .8),
        fill(hide, rad(MOUTH, 260, [(0, "#8a3a1a"), (1, "#8a3a1a00")]), .3, mode="add"),
        fill(neck_head, lin((552, 330), (708, 420), [(0, "#2a1a12"), (1, "#5a2a16")]), .35),
        fill(stroke([[(610, 406), (650, 436)], [(640, 402), (680, 420)]], 2.2), "#0a0608", .8, blur=.6),
        relief(horns, LIGHTS, "#1a1416", .18, .9, .5, 40, .6, bumps=[(.6, 3)]),
        fill(brow, "#140c10", .9),
        rim(union(hide, back), (.9, .7), 3.5, "#ff7a32", .6)],
        "grow", origin=(400, 300), weight=1.4))
    S.append(Step("رأس التنين", [
        fill(teeth, "#e8dcc4", .95), rim(teeth, (0, -1), 1, "#ffffff", .5),
        fill(ellipse(606, 358, 7, 4, rot=20), "#ffcf4a"), glow(ellipse(606, 358, 8, 6), "#ff9a2a", 10, .9),
        fill(ellipse(607, 358, 1.8, 3.8, rot=20), "#2a0a00")],
        "grow", origin=(606, 358), weight=.4))

    nw_mem, nw_bones, nw_veins = wing((330, 270), (250, 120), (150, 0), [(-10, 0), (-40, 120), (40, 250), (190, 330)], (340, 330), sag=.3)
    S.append(Step("جناح التنين الأمامي", [
        relief(nw_mem, LIGHTS, "#222a3c", .2, .12, .3, 18, .25, bumps=[(1.5, 14), (.4, 4)], seed=53, fresnel=.5, fres_col="#9fb6d8", sss=3),
        fill(nw_mem, rad(FIRE, 480, [(0, "#ff8a3a"), (1, "#ff8a3a00")]), .4, mode="add"),
        fill(nw_veins, "#0a0d14", .75),
        relief(nw_bones, LIGHTS, "#141820", .2, .8, .5, 30, .5, fresnel=.3)],
        "grow", origin=(330, 270), weight=.9))

    # 7. the whale, built in its own frame: humpback profile, pleated throat, long pectoral fin, fluke, knobbed head
    top = [(0, -16), (40, -46), (110, -82), (200, -108), (310, -122), (430, -112), (540, -82), (640, -44), (700, -18)]
    bottom = [(700, 22), (610, 56), (520, 92), (420, 118), (300, 130), (180, 116), (90, 78), (30, 36), (0, 8)]
    profile = [catmull(top + bottom, 10, closed=True)]
    hump = poly([(395, -112), (430, -136), (470, -110)])
    pleats = [[(26 + k * 3, 22 + k * 15), (120, 48 + k * 13), (240, 86 + k * 9), (360, 112 + k * 5)] for k in range(7)]
    mouth = catmull([(0, -4), (40, 14), (90, 34), (140, 52), (175, 64)], 8)
    fin_root, fin_tip = (235, 100), (70, 350)
    fin_pts = [fin_root, (190, 150), (150, 215), (115, 280), fin_tip]
    fin = tube(fin_pts, [36, 34, 30, 20, 6])
    fin_edge = [(x + 30 + 8 * math.sin(k), y + 10, 2.4 + (k < 3)) for k, (x, y) in enumerate(catmull(fin_pts, 2)[1:-1:2])]
    fluke = path("M 690 -18 C 740 -70 800 -100 850 -92 C 836 -60 820 -30 812 0 C 820 30 836 60 850 92 C 800 100 740 70 690 22 Z")
    tubercles = [(x, y, r) for x, y, r in [(18, -24, 3.4), (46, -40, 3.2), (78, -56, 3.2), (112, -70, 3), (30, -6, 2.8),
                                           (62, -22, 2.8), (96, -38, 2.6), (20, 12, 2.6), (54, 30, 2.6), (92, 44, 2.6)]]
    eye = (182, 60)
    body_shape = WS(union(profile, hump))
    fin_shape, fluke_shape = WS(fin), WS(fluke)
    skin = lin(W(300, -130), W(300, 140), [(0, "#0c1016"), (.45, "#1c232c"), (.75, "#4a5663"), (1, "#a9b3bc")])
    S.append(Step("جسد الحوت", [
        fill(fluke_shape, "#0e141a", .7),
        relief(fluke_shape, LIGHTS, lin(W(700, 0), W(850, 0), [(0, "#1c242c"), (1, "#3a4650")]), .14, .5, .4, 40, .5,
               bumps=[(1.2, 12), (.4, 3)], seed=66, fresnel=.3, roughness=.4),
        relief(body_shape, LIGHTS, skin, .12, .55, .38, 44, .42, bumps=[(2.0, 40), (.9, 12), (.3, 3.5)], seed=61,
               fresnel=.25, fres_col="#9fb6d8", sss=2.5, sss_col="#e8d8d0", roughness=.55),
        fill(body_shape, lin(W(300, -130), W(300, 20), [(0, "#070a0e"), (1, "#070a0e00")]), .45),
        fill(WS(stroke(pleats, 2.8)), "#141b23", .7, blur=1.1),
        fill(WS(stroke(pleats, .9)), "#dfe7ee", .4),
        fill(WS(stroke([mouth], 3.4)), "#0b0f14", .9, blur=.7),
        fill(WS(stroke([[(x, y + 3) for x, y in mouth]], 1.0)), "#9aa8b4", .4),
        fill(WS(tube([fin_root, (200, 140)], [46, 30])), "#0d1218", .5, blur=8),
        relief(fin_shape, LIGHTS, lin(W(*fin_root), W(*fin_tip), [(0, "#3a4650"), (.35, "#9fadb8"), (1, "#e6ecf0")]), .16, .6, .5, 40, .5,
               bumps=[(1.2, 10), (.4, 3)], seed=64, fresnel=.25, sss=2),
        fill(dots([(*W(x, y), r) for x, y, r in fin_edge]), "#aeb9c2", .8),
        fill(dots([(*W(x, y), r * .5) for x, y, r in fin_edge]), "#5a6873", .8),
        fill(dots([(*W(x, y), r) for x, y, r in tubercles]), "#2e3a46", .9),
        fill(dots([(*W(x - .8, y - .8), r * .45) for x, y, r in tubercles]), "#c2ccd6", .9),
        fill(ellipse(*W(*eye), 5, 3.6, rot=math.degrees(_TH) + 10), "#070a0e"), fill(ellipse(*W(eye[0] + 1.2, eye[1] - 1), 1.3, 1.3), "#dde8f3"),
        fill(body_shape, rad(IMPACT, 520, [(0, "#ff8a3a"), (1, "#ff8a3a00")]), .2, mode="add"),
        rim(union(body_shape, fin_shape), (.4, -1), 3, "#dbe8fb", .55),
        rim(union(body_shape, fin_shape), (-.8, .3), 4, "#ffa04a", .5, soft=1.6)],
        "rise", origin=(1000, 740), weight=1.6))

    # 8. water sheeting off the whale and bursting where it leaves the sea (then streaked by motion)
    S.append(Step("الماء ينهمر عن جسد الحوت", [
        fill(stroke([[(x, y), (x - 8, y + 60), (x - 24, y + 130)] for x, y in
                     [(1000, 500), (1040, 560), (1090, 610), (960, 470), (932, 440), (1120, 660), (1070, 600)]], 1.6),
             "#e6eff8", .5, blur=1.0, mode="screen"),
        fill(stroke([[(x, y), (x - 14, y + 120)] for x, y in [(1010, 520), (1060, 580), (1100, 630)]], .8), "#ffffff", .55),
        glow(ellipse(1140, 710, 220, 70), "#cfe0f2", 40, .4),
        fill(dots(spray(71, 1130, 710, 460, 160, 70, 1.4)), "#eef4fb", .8),
        fill(dots(spray(72, 1130, 710, 180, 190, 100, 1.6, (2.4, 3.2, 4))), "#ffffff", .35, blur=2),
        fill(dots(spray(73, 1130, 710, 120, 120, 40, 1.0)), "#ffb066", .3, blur=1.5, mode="add"),
        motion_blur(rect(900, 540, 400, 220), 7, 112, .7)],
        "rise", origin=(1140, 730), weight=.7))

    # 9. the fire
    a, b = (MOUTH[0] + 24, MOUTH[1] + 4), IMPACT
    S.append(Step("نار التنين", [
        glow(tube([a, b], [16, 60]), "#ff4a12", 44, .7),
        *[fill(flame(900 + k, a, b, 5, 34, 16, bend=(k - 3) * .5), "#ff3d0a", .5, blur=3, mode="add") for k in range(7)],
        *[fill(flame(920 + k, a, b, 3.5, 22, 9, bend=(k - 2) * .35), "#ff9326", .65, blur=2.4, mode="add") for k in range(5)],
        *[fill(flame(940 + k, a, b, 2.2, 12, 5), "#ffe7a2", .85, blur=1.8, mode="add") for k in range(3)],
        fill(flame(960, a, b, 1.4, 6, 3), "#ffffff", .75, blur=1.2, mode="add")],
        "grow", origin=MOUTH, weight=1.0))

    # 10. steam at the collision
    steam = union(cloud(IMPACT[0], IMPACT[1] - 20, 200, 90, 12, 81), cloud(IMPACT[0] - 30, IMPACT[1] - 70, 150, 60, 8, 82))
    S.append(Step("البخار عند التصادم", [
        fill(steam, "#d6dde6", .45, blur=12, mode="screen"),
        noise(steam, .5, 20, 83, "multiply", octaves=3),
        fill(translate(steam, 0, 14), "#ff8a3a", .32, blur=16, mode="add"),
        glow(ellipse(*IMPACT, 56, 40), "#fff0c0", 26, .7),
        *[fill(tongue(980 + k, [IMPACT, (IMPACT[0] + 36 * math.cos(t0), IMPACT[1] - 30 * math.sin(t0)),
                                (IMPACT[0] + 64 * math.cos(t0), IMPACT[1] - 50 * math.sin(t0))], 9, 1),
               "#ff6a1a", .5, blur=2.5, mode="add") for k, t0 in enumerate((.4, 1.2, 2.0, 2.8, 3.5, -.3))],
        fill(dots(spray(84, IMPACT[0], IMPACT[1], 140, 70, 60, 1.0, (1, 1.4, 2))), "#fff3d8", .7, blur=.6, mode="add")],
        "grow", origin=IMPACT, weight=.6))

    # 11. rain streaked by the exposure, spray in the air, embers
    S.append(Step("المطر والرذاذ", [
        fill(rain(91, 520, -40, 1240, TOP - 40, BOTTOM, 24, 1.0), "#a8bbd4", .15, blur=.4),
        fill(rain(92, 150, -40, 1240, TOP - 60, BOTTOM, 60, 1.8), "#cddcef", .2, blur=1.2),
        fill(rain(93, 160, 480, 900, 240, 560, 36, 1.3), "#ffb066", .4, blur=.6, mode="add"),
        fill(dots(spray(94, 600, 600, 220, 600, 120, .5, (.8, 1, 1.4))), "#e4edf8", .3, blur=.5),
        motion_blur(rect(0, TOP, 1200, BOTTOM - TOP), 6, 104, .35)],
        "down", weight=.8))
    r = random.Random(95)
    emb = []
    for _ in range(220):
        t = r.random()
        emb.append((a[0] + (b[0] - a[0]) * t + r.gauss(0, 50), a[1] + (b[1] - a[1]) * t + r.gauss(0, 40) - r.random() * 70,
                    r.choice([.6, .8, 1.1, 1.5])))
    S.append(Step("الشرر", [fill(dots(emb), "#ffd27a", .9, mode="add"),
                            fill(dots([(x, y, s * 3) for x, y, s in emb if s > 1]), "#ff7a2a", .45, blur=2.4, mode="add")],
                  "sparkle", weight=.4))

    # 12. the camera: bloom, a flare from the fire, chromatic fringing, filmic tone mapping, vignette, grain
    S.append(Step("الكاميرا: التوهّج والعدسة والفيلم", [
        fill(rect(-50, 380, 1300, 200), "#3f4d63", .06, blur=40, mode="screen"),
        bloom(.8, 24, .32, "#ffe6d0"),
        flare(IMPACT, "#ffb070", 100, 360, .38),
        chroma(1.1),
        filmic(1.0, 1.14, 1.04),
        vignette(.55), grain(.018, 9)], "sweep", weight=.7))
    S.append(Step("إطار 16:9", [fill(rect(0, 0, 1200, TOP), "#000000"), fill(rect(0, BOTTOM, 1200, 800 - BOTTOM), "#000000")],
                  "sweep", weight=.3))
    return S
