"""فتاة تقاتل تنيناً — a girl holds off a dragon's fire on a cliff under a full moon.

Every shape, light and spark below is vector code, so the picture renders at any size without losing quality.
Light comes from three places: the moon behind the dragon (cool), the dragon's fire (warm), the girl's sword (cyan).
"""
from __future__ import annotations

import math
import random

from render import (Step, catmull, dots, ellipse, fill, glow, grade, grain, lin, path, poly, rad, rect, rim,
                    translate, tube, union, vignette)

TITLE = "فتاة تقاتل تنيناً"
MOON, MOON_R = (845, 232), 150
MOUTH = (633, 352)


# ── helpers ────────────────────────────────────────────────────────────────────────────────────────────────
def ridge(seed, base, amp, x0=-20, x1=1220, rough=0.55, peaks=()):
    """A mountain ridge by midpoint displacement; returns the filled shape down to the bottom of the sheet."""
    r = random.Random(seed)
    pts = [(x0, base - r.uniform(0, amp)), (x1, base - r.uniform(0, amp))]
    a = amp
    for _ in range(7):
        nxt = [pts[0]]
        for p, q in zip(pts, pts[1:]):
            nxt.append(((p[0] + q[0]) / 2, (p[1] + q[1]) / 2 + r.uniform(-a, a) * 0.5))
            nxt.append(q)
        pts, a = nxt, a * rough
    for px, ph, pw in peaks:      # carve chosen peaks
        pts = [(x, y - ph * max(0.0, 1 - abs(x - px) / pw)) for x, y in pts]
    return [[(x0, 820)] + pts + [(x1, 820)]]


def cloud(cx, cy, w, h, n, seed):
    r = random.Random(seed)
    out = []
    for _ in range(n):
        x = cx + r.uniform(-w / 2, w / 2)
        taper = 1 - abs(x - cx) / (w / 2) * 0.6
        out += ellipse(x, cy + r.uniform(-h / 3, h / 3) * taper, r.uniform(w * .07, w * .16), r.uniform(h * .3, h * .6) * taper)
    return out


def spikes(spine, radii, every=6, size=1.0, side=1):
    """Small spines along the top of a body tube."""
    pts = catmull(spine, 8)
    import numpy as np
    rr = np.interp(np.linspace(0, len(radii) - 1, len(pts)), range(len(radii)), radii)
    out = []
    for i in range(2, len(pts) - 2, every):
        (ax, ay), (bx, by) = pts[i - 1], pts[i + 1]
        tx, ty = bx - ax, by - ay
        d = math.hypot(tx, ty) or 1
        tx, ty = tx / d, ty / d
        nx, ny = -ty * side, tx * side
        if ny > 0:
            nx, ny = -nx, -ny
        x, y, r = pts[i][0], pts[i][1], rr[i]
        h, b = (4 + r * .45) * size, (2 + r * .18) * size
        bx0, by0 = x + nx * r * .8, y + ny * r * .8
        out.append([(bx0 - tx * b, by0 - ty * b), (bx0 + tx * b, by0 + ty * b),
                    (bx0 + nx * h - tx * b * 1.3, by0 + ny * h - ty * b * 1.3)])
    return out


def belly_plates(spine, radii):
    """The plated underside of neck and chest: a lighter band along the bottom of the body, ribbed across."""
    import numpy as np
    pts = catmull(spine, 8)
    rr = np.interp(np.linspace(0, len(radii) - 1, len(pts)), range(len(radii)), radii)
    centre, rad_, ribs = [], [], []
    for i, (x, y) in enumerate(pts):
        (ax, ay), (bx, by) = pts[max(i - 1, 0)], pts[min(i + 1, len(pts) - 1)]
        d = math.hypot(bx - ax, by - ay) or 1
        nx, ny = -(by - ay) / d, (bx - ax) / d
        if ny < 0:
            nx, ny = -nx, -ny
        centre.append((x + nx * rr[i] * .55, y + ny * rr[i] * .55))
        rad_.append(rr[i] * .42)
        if i % 4 == 2:
            ribs.append(tube([(x + nx * rr[i] * .2, y + ny * rr[i] * .2), (x + nx * rr[i] * .97, y + ny * rr[i] * .97)],
                             [.7, .5], n=3))
    return tube(centre, rad_), union(*ribs)


def wing(shoulder, elbow, wrist, tips, attach, sag=0.28):
    """Bat wing: arm bones, finger bones and a membrane whose edge sags between the finger tips."""
    def scallop(a, b):
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        cx, cy = mx + (wrist[0] - mx) * sag, my + (wrist[1] - my) * sag
        return [(a[0] + (b[0] - a[0]) * 0 + 0, a[1])] + [
            ((1 - t) ** 2 * a[0] + 2 * (1 - t) * t * cx + t * t * b[0],
             (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * cy + t * t * b[1]) for t in [k / 12 for k in range(1, 13)]]
    edge = [wrist, tips[0]]
    for a, b in zip(tips, tips[1:] + [attach]):
        edge += scallop(a, b)[1:]
    membrane = [edge + [shoulder, elbow]]
    bones = tube([shoulder, elbow, wrist], [8, 6, 4.5])
    fingers = union(*[tube([wrist, t], [3.4, 0.7], n=6) for t in tips])
    veins = union(*[tube([wrist, ((a[0] + b[0]) / 2 * .85 + wrist[0] * .15, (a[1] + b[1]) / 2 * .85 + wrist[1] * .15)],
                         [1.1, 0.3], n=4) for a, b in zip(tips, tips[1:])])
    claw = tube([wrist, (wrist[0] - 6, wrist[1] - 12), (wrist[0] - 2, wrist[1] - 19)], [3, 2, .5], n=5)
    return membrane, union(bones, fingers, claw), veins


def flame(seed, a, b, r0, r1, wob, n=10, bend=0.0):
    r = random.Random(seed)
    L = math.hypot(b[0] - a[0], b[1] - a[1])
    nx, ny = -(b[1] - a[1]) / L, (b[0] - a[0]) / L
    f, ph = r.uniform(1.6, 3.2), r.uniform(0, 6.3)
    pts, radii = [], []
    for i in range(n):
        t = i / (n - 1)
        w = math.sin(t * math.pi * f + ph) * wob * t + bend * math.sin(t * math.pi) * L * .12
        pts.append((a[0] + (b[0] - a[0]) * t + nx * w, a[1] + (b[1] - a[1]) * t + ny * w))
        radii.append((r0 + (r1 - r0) * t ** .75) * r.uniform(.75, 1.2) * (1 - .55 * t ** 6))
    return tube(pts, radii, n=6)


def tongue(seed, pts, r0, r1):
    r = random.Random(seed)
    rad_ = [r0 + (r1 - r0) * (i / (len(pts) - 1)) * r.uniform(.8, 1.1) for i in range(len(pts))]
    return tube(pts, rad_, n=7)


# ── the picture program ────────────────────────────────────────────────────────────────────────────────────
def build() -> list[Step]:
    S: list[Step] = []
    rnd = random.Random(11)

    # 1. sky
    S.append(Step("السماء", [fill(rect(0, 0, 1200, 800), lin((0, 0), (0, 800), [
        (0, "#05071a"), (.30, "#11133a"), (.55, "#2e1a48"), (.70, "#5c2440"), (.80, "#8c3a2e"), (1, "#1a0c10")]))],
        "sweep", weight=1.3))

    # 2. stars
    stars = []
    while len(stars) < 280:
        x, y = rnd.uniform(0, 1200), 480 * rnd.random() ** 1.7
        if math.hypot(x - MOON[0], y - MOON[1]) > MOON_R + 60:
            stars.append((x, y, rnd.choice([.45, .55, .7, .9, 1.25])))
    S.append(Step("النجوم", [
        fill(dots(stars), "#e4e9ff", .9, mode="add"),
        fill(dots([(x, y, r * 3.5) for x, y, r in stars if r > 1]), "#7f93ff", .35, blur=2.5, mode="add")],
        "sparkle", weight=.45))

    # 3. moon
    S.append(Step("القمر", [
        glow(ellipse(*MOON, MOON_R * 2.4), "#4f3f86", 70, .55),
        fill(ellipse(*MOON, MOON_R), rad((MOON[0] - 45, MOON[1] - 55), MOON_R * 1.55,
                                         [(0, "#fffaf0"), (.55, "#f7e6c2"), (1, "#dcb47e")])),
        fill(ellipse(800, 196, 50, 34, rot=-20), "#b99467", .30, blur=7),
        fill(ellipse(884, 268, 62, 40, rot=15), "#b99467", .26, blur=9),
        fill(ellipse(862, 170, 24, 18), "#c7a172", .26, blur=4),
        fill(ellipse(790, 290, 30, 20, rot=30), "#c09a6c", .2, blur=5),
        glow(ellipse(*MOON, MOON_R * 1.18), "#f1d29a", 26, .32)],
        "grow", origin=MOON, weight=.9))

    # 4. clouds: moonlit tops, fire-lit bellies low down
    c_hi1, c_hi2 = cloud(260, 190, 560, 64, 16, 1), cloud(1040, 92, 420, 50, 12, 2)
    c_moon = cloud(700, 338, 760, 40, 18, 3)
    c_low = cloud(160, 480, 520, 46, 14, 4)
    S.append(Step("الغيوم", [
        fill(c_hi1, "#1a1940", .78, blur=15), fill(translate(c_hi1, 6, -9), "#5b5590", .22, blur=17, mode="screen"),
        fill(c_hi2, "#1b1a44", .7, blur=14), fill(translate(c_hi2, -8, -8), "#6a64a3", .25, blur=15, mode="screen"),
        fill(c_moon, "#251c46", .62, blur=13), fill(translate(c_moon, 0, -7), "#c8a88a", .16, blur=14, mode="add"),
        fill(c_low, "#2a1730", .75, blur=14), fill(translate(c_low, 10, 12), "#ff6a2a", .20, blur=18, mode="add")],
        "sweep", weight=.9))

    # 5. far mountains + glow behind them
    far = ridge(5, 585, 120, peaks=[(150, 60, 180), (560, 40, 150)])
    S.append(Step("الجبال البعيدة", [
        glow(rect(0, 520, 1200, 60), "#a8455a", 40, .35),
        fill(far, lin((0, 470), (0, 700), [(0, "#4b3364"), (1, "#22182f")]), blur=.6),
        fill(translate(far, 0, -3), "#9a6a9a", .12, blur=4, mode="add")],
        "right", weight=.8))

    # 6. near mountains and a castle on a peak
    near = ridge(9, 640, 90, peaks=[(1030, 70, 140), (300, 30, 160)])
    castle = union(
        rect(1012, 520, 26, 70), rect(1046, 540, 18, 50), rect(990, 548, 16, 42),
        poly([(1008, 522), (1025, 486), (1042, 522)]), poly([(1043, 542), (1055, 518), (1067, 542)]),
        rect(1004, 562, 64, 40),
        *[rect(1012 + k * 7, 514, 4, 7) for k in range(4)])
    S.append(Step("الجبال القريبة والقلعة", [
        fill(near, lin((0, 540), (0, 760), [(0, "#1e1631"), (1, "#0e0a18")]), blur=.5),
        fill(castle, "#150f22", 1, blur=.3),
        fill(rect(1022, 538, 3, 5), "#ffbf5c", 1), fill(rect(1050, 556, 3, 4), "#ffbf5c", .9),
        glow(rect(1018, 534, 12, 26), "#ff9a3a", 7, .7)],
        "left", weight=.8))

    # 7. valley fog
    S.append(Step("ضباب الوادي", [
        fill(rect(-50, 615, 1300, 70), "#a86484", .26, blur=26, mode="screen"),
        fill(rect(-50, 690, 1300, 80), "#5c3550", .30, blur=30, mode="screen")],
        "sweep", weight=.5))

    # 8. the dragon — far wing first (behind the body)
    fw_mem, fw_bones, fw_veins = wing((882, 382), (952, 252), (1012, 150),
                                      [(1150, 92), (1188, 188), (1156, 282), (1086, 342)], (962, 414))
    S.append(Step("جناح التنين الخلفي", [
        fill(fw_mem, rad(MOON, 300, [(0, "#5a2232"), (.5, "#2b1220"), (1, "#110810")]), .97, blur=.4),
        fill(fw_veins, "#0c060c", .8), fill(fw_bones, "#0d070d"),
        rim(union(fw_mem, fw_bones), (-.3, -1), 2.2, "#d9b98a", .55)],
        "grow", origin=(882, 382), weight=.8))

    spine = [(716, 352), (748, 332), (786, 331), (820, 352), (852, 390), (896, 416), (950, 428), (1004, 420),
             (1050, 446), (1086, 500), (1100, 566), (1078, 628), (1034, 660), (995, 652), (982, 636)]
    radii = [15, 17, 19, 23, 33, 44, 47, 42, 33, 25, 18, 12, 7, 4, 1.5]
    body = tube(spine, radii)
    legs = union(
        tube([(872, 440), (880, 478), (862, 506), (838, 512)], [14, 10, 7, 5]),
        tube([(997, 444), (1032, 478), (1020, 520), (996, 532)], [20, 13, 8, 5]),
        *[tube([(838, 512), (838 + dx, 512 + dy)], [2.4, .5], n=4) for dx, dy in [(-12, 6), (-10, 12), (-3, 15)]],
        *[tube([(996, 532), (996 + dx, 532 + dy)], [2.6, .5], n=4) for dx, dy in [(-13, 5), (-10, 12), (-2, 15)]])
    back = spikes(spine[:-2], radii[:-2], every=5, size=1.1)
    head = path("M726 340 C718 326 702 318 686 321 C672 324 658 329 647 333 L630 339 C627 343 631 347 639 347 "
                "L668 349 L692 355 L666 359 L647 367 C640 370 641 375 648 375 C662 377 682 378 700 378 "
                "C714 377 724 372 730 364 Z")
    horns = union(tube([(716, 327), (736, 311), (762, 300), (790, 298)], [5.5, 4.2, 2.6, .6]),
                  tube([(705, 324), (722, 305), (744, 291), (764, 286)], [4.4, 3.4, 2, .5]))
    frill = union(poly([(724, 366), (748, 374), (731, 357)]), poly([(718, 372), (738, 386), (724, 366)]))
    teeth = union(*[poly([(x, 348), (x + 3, 348), (x + 1.5, 354)]) for x in (640, 650, 660, 670)],
                  *[poly([(x, 368), (x + 3, 366), (x + 1.2, 360.5)]) for x in (649, 659, 669)])
    dragon = union(body, legs, back, head, horns, frill)
    belly, plates = belly_plates(spine[:9], radii[:9])
    S.append(Step("جسم التنين", [
        fill(dragon, "#120a12"),
        fill(union(body, legs, head), rad(MOUTH, 360, [(0, "#6a2614"), (.45, "#2a0f10"), (1, "#120a12")]), .9),
        fill(belly, rad(MOUTH, 330, [(0, "#9a4a26"), (.5, "#4a1e16"), (1, "#1e0f10")]), .85),
        fill(plates, "#0a0508", .55),
        rim(dragon, (.25, -1), 2.4, "#f0d6a4", .75),
        rim(union(head, body[:60], legs), (-.85, .55), 3.2, "#ff7a2e", .9)],
        "grow", origin=(900, 420), weight=1.3))

    S.append(Step("رأس التنين وعينه", [
        fill(teeth, "#efe0c4", .95),
        fill(ellipse(689, 332, 3.4, 2.2, rot=-10), "#ffd166"),
        glow(ellipse(689, 332, 4, 3), "#ffae2a", 6, .9)],
        "grow", origin=(689, 332), weight=.35))

    # near wing in front, raised high over the moon
    nw_mem, nw_bones, nw_veins = wing((850, 388), (842, 256), (800, 120),
                                      [(700, 38), (652, 108), (684, 190), (758, 252)], (862, 412))
    S.append(Step("جناح التنين الأمامي", [
        fill(nw_mem, rad(MOON, 280, [(0, "#7a2c36"), (.45, "#3a1622"), (1, "#150a12")]), .96, blur=.4),
        fill(nw_veins, "#120810", .85), fill(nw_bones, "#100810"),
        rim(union(nw_mem, nw_bones), (.2, -1), 2.4, "#f3dcae", .7),
        rim(nw_mem, (-1, .4), 2.5, "#ff7a2e", .35)],
        "grow", origin=(850, 388), weight=.9))

    # 9. smoke above the fire
    smoke = union(cloud(560, 330, 180, 40, 8, 21), cloud(500, 300, 140, 34, 6, 22))
    S.append(Step("الدخان", [fill(smoke, "#2a1a24", .45, blur=12)], "rise", weight=.4))

    # 10. the fire breath; it lands on the girl's shield (her figure is scaled 1.4x around her feet)
    SH = (380 + (452 - 380) * 1.4 - 22, 619 + (460 - 619) * 1.4)
    a, b = (MOUTH[0] - 2, MOUTH[1] + 1), (SH[0] + 16, SH[1] - 2)
    S.append(Step("نار التنين", [
        glow(tube([a, b], [10, 46]), "#ff4a12", 34, .6),
        *[fill(flame(100 + k, a, b, 3, 30, 16, bend=(k - 3) * .45), "#ff3d0a", .5, blur=3, mode="add") for k in range(7)],
        *[fill(flame(200 + k, a, b, 2.5, 18, 9, bend=(k - 2) * .3), "#ff9326", .65, blur=2.4, mode="add") for k in range(5)],
        *[fill(tongue(450 + k, [(a[0] + (b[0] - a[0]) * f0, a[1] + (b[1] - a[1]) * f0),
                                (a[0] + (b[0] - a[0]) * (f0 + .07) - 4, a[1] + (b[1] - a[1]) * (f0 + .07) - 14 - 5 * k),
                                (a[0] + (b[0] - a[0]) * (f0 + .12) - 10, a[1] + (b[1] - a[1]) * (f0 + .12) - 26 - 7 * k)],
                          5, .5), "#ff6a1a", .55, blur=2.5, mode="add") for k, f0 in enumerate([.25, .45, .62, .78])],
        *[fill(flame(300 + k, a, b, 1.6, 9, 4), "#ffe7a2", .85, blur=1.8, mode="add") for k in range(3)],
        fill(flame(400, a, b, 1, 4.5, 2), "#ffffff", .75, blur=1.2, mode="add")],
        "grow", origin=MOUTH, weight=1.0))

    # 11. the cliff
    cliff = path("M-10 586 L46 578 L96 590 L150 597 L210 605 L262 612 L300 617 L340 619 L380 620 L430 621 "
                 "L466 622 L484 630 L494 652 L505 690 L518 734 L532 810 L-10 810 Z")
    rocks = union(ellipse(70, 586, 46, 20, rot=-8), ellipse(140, 600, 30, 12), ellipse(230, 612, 26, 9))
    cracks = union(tube([(470, 640), (480, 680), (474, 720), (490, 770)], [1.2, .9, .9, .5]),
                   tube([(300, 640), (330, 680), (322, 740)], [1, .8, .4]),
                   tube([(120, 640), (100, 700), (126, 780)], [1.1, .9, .5]))
    S.append(Step("الصخرة", [
        fill(union(cliff, rocks), lin((0, 580), (0, 800), [(0, "#1d131a"), (.4, "#0f0a10"), (1, "#060408")])),
        fill(cracks, "#030204", .9),
        rim(union(cliff, rocks), (.65, -1), 3, "#ff8a3a", .75),
        glow(ellipse(430, 624, 120, 12), "#ff7a30", 10, .45)],
        "sweep", weight=.9))

    # 12. the girl, designed 1:1 around her feet, then scaled up 1.4x
    K, FX, FY, DX = 1.4, 380, 619, -22

    def xf(shape):
        return [[(FX + (x - FX) * K + DX, FY + (y - FY) * K) for x, y in q] for q in shape]

    def xp(p):
        return (FX + (p[0] - FX) * K + DX, FY + (p[1] - FY) * K)
    cape = xf(path("M383 456 C366 457 346 461 326 468 C304 476 287 492 272 514 C283 509 293 513 299 523 "
                   "C306 515 315 515 322 525 C330 515 340 513 348 521 C355 512 362 509 369 513 "
                   "C372 500 376 492 380 486 Z"))
    cape_folds = xf(union(tube([(370, 470), (340, 486), (312, 508)], [.9, .8, .4], n=6),
                          tube([(376, 478), (352, 494), (330, 516)], [.8, .7, .3], n=6)))
    locks = [([(393, 427), (374, 431), (352, 435), (330, 440), (308, 446), (288, 450)], [9, 10, 9.4, 7.4, 4.6, 1]),
             ([(389, 436), (369, 445), (347, 451), (324, 459), (304, 467)], [6.5, 7, 5.4, 3, .7]),
             ([(395, 423), (373, 423), (351, 423), (330, 427), (311, 431)], [5, 5.6, 4.2, 2.4, .6]),
             ([(386, 440), (368, 452), (350, 462), (334, 474)], [4.5, 4.6, 3, .6])]
    hair_mass = path("M406 425 C399 416 386 416 381 424 C370 421 352 420 334 425 C322 429 313 436 305 444 "
                     "C318 444 330 446 340 452 C325 456 314 462 303 471 C320 467 336 466 350 462 "
                     "C364 458 376 452 386 446 C384 438 387 430 396 427 Z")
    hair = xf(union(hair_mass, *[tube(sp, rr) for sp, rr in locks]))
    strands = xf(union(*[tube([(x, y + off) for x, y in sp[:-1]], [.4] * (len(sp) - 1), n=6)
                         for sp, _ in locks for off in (-1.6, 1.8)]))
    head = xf(path("M386 446 C380 438 382 428 391 424 C399 420 407 424 409 432 C410 435 410 437 412 440 L410 442 "
                   "C411 444 409 445 409 446 C410 448 408 449 407 450 C404 453 400 453 396 452 L390 452 "
                   "C387 451 386 449 386 446 Z"))
    neck = xf(tube([(392, 449), (394, 458)], [3.5, 4.3]))
    torso = xf(path("M380 456 C392 450 403 452 407 458 C412 465 413 474 407 481 C403 487 401 492 400 497 "
                    "C401 502 403 507 404 512 L370 514 C369 506 371 500 372 495 C370 483 372 468 380 456 Z"))
    skirt = xf(path("M370 506 L404 508 C409 520 414 532 421 546 C410 548 400 545 392 548 C382 546 368 551 352 556 "
                    "C358 540 364 522 370 506 Z"))
    legs_g = xf(union(
        tube([(390, 520), (404, 540), (414, 561), (419, 578), (424, 598), (427, 610)], [10, 9, 6.6, 7.2, 5, 4.6]),
        tube([(376, 520), (366, 543), (356, 566), (345, 584), (334, 601), (328, 611)], [10, 8.6, 6.4, 6.8, 4.8, 4.4]),
        tube([(424, 605), (428, 615), (448, 619)], [5.2, 4.5, 3]),
        tube([(330, 606), (326, 615), (343, 619)], [5, 4.3, 3])))
    arm_shield = xf(union(tube([(402, 462), (413, 468), (422, 472)], [5, 4.4, 3.8]),
                          tube([(422, 472), (432, 466), (441, 458)], [3.9, 3.6, 3.1]), ellipse(442, 457, 3.6, 3.1)))
    arm_sword = xf(union(tube([(383, 459), (373, 452), (364, 447)], [5, 4.6, 4]),
                         tube([(364, 447), (359, 437), (356, 427)], [3.9, 3.5, 3.2]), ellipse(355, 424, 3.4, 3.2)))
    belt = xf(tube([(371, 505), (388, 507), (404, 508)], [1.7, 1.7, 1.7]))
    pauldron = xf(path("M393 456 C399 452 408 454 412 461 C408 465 400 466 395 463 Z"))
    bracer = xf(tube([(426, 470), (436, 463)], [4.1, 3.7]))
    shield_c = xp((452, 460))
    shield = ellipse(*shield_c, 10 * K, 31 * K, rot=-8)
    body_g = union(head, neck, torso, skirt, legs_g, arm_shield, arm_sword)
    girl = union(cape, hair, body_g)
    S.append(Step("الفتاة: الرداء والشعر", [
        fill(cape, lin(xp((380, 460)), xp((280, 520)), [(0, "#561019"), (1, "#24060c")])),
        fill(cape_folds, "#14030a", .6, blur=.6),
        fill(hair, lin(xp((395, 425)), xp((300, 455)), [(0, "#1a0f14"), (1, "#0c070b")])),
        fill(strands, "#4a3040", .35, blur=.25)],
        "grow", origin=xp((388, 450)), weight=.7))
    S.append(Step("الفتاة: الجسد", [
        fill(body_g, lin(xp((360, 0)), xp((425, 0)), [(0, "#0a070c"), (.6, "#170d12"), (1, "#3a1a14")])),
        fill(head, lin(xp((413, 440)), xp((393, 440)), [(0, "#d98252"), (.3, "#8a4428"), (.7, "#2a1410"),
                                                        (1, "#0c0810")]), .95),
        fill(neck, lin(xp((397, 452)), xp((389, 452)), [(0, "#6a301e"), (1, "#0c0810")]), .9),
        fill(xf(ellipse(403.6, 434.2, 1.7, .95, rot=-6)), "#120a0c"),
        fill(xf(ellipse(404.3, 433.9, .38, .38)), "#ffd8a0", .9),
        fill(xf(tube([(400.8, 431.2), (403.4, 430.4), (406, 430.9)], [.55, .6, .35], n=4)), "#160c0e", .9),
        fill(xf(tube([(407.2, 446.2), (409.6, 446.4)], [.35, .3], n=3)), "#3a1410", .8),
        rim(head, (1, -.1), 1.4, "#ffd9a8", 1, soft=.3),
        fill(skirt, lin(xp((360, 505)), xp((420, 550)), [(0, "#1a0e18"), (1, "#4a1a18")]), .85),
        fill(union(belt, pauldron, bracer), "#4a3426", 1),
        rim(union(pauldron, bracer, belt), (1, -.6), 1.6, "#ffcf8a", .9)],
        "rise", origin=xp((388, 619)), weight=.9))
    S.append(Step("الدرع", [
        fill(shield, lin((shield_c[0] - 14, shield_c[1] - 44), (shield_c[0] + 14, shield_c[1] + 44),
                         [(0, "#3a2a24"), (1, "#140c0e")])),
        fill(ellipse(*shield_c, 6.5 * K, 24 * K, rot=-8), "#0e080a", .5),
        rim(shield, (1, -.15), 6, "#ffb25a", 1),
        fill(ellipse(shield_c[0] + 3, shield_c[1], 4, 8), "#ffe0a0", .95)],
        "grow", origin=shield_c, weight=.35))

    # 13. light on the girl: fire from the right, sword from above
    S.append(Step("ضوء النار على الفتاة", [
        rim(girl, (1, -.12), 3, "#ffa04a", .95),
        rim(girl, (1, -.12), 8, "#ff6a2a", .35, soft=2),
        rim(union(hair, head, arm_sword, cape), (-.45, -1), 2.2, "#62d6ff", .6)],
        "grow", origin=shield_c, weight=.6))

    # 14. the glowing sword
    hilt, tip = xp((355, 423)), xp((314, 330))
    dx, dy = tip[0] - hilt[0], tip[1] - hilt[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    blade = poly([(hilt[0] + nx * 3, hilt[1] + ny * 3), (tip[0] + nx * .4, tip[1] + ny * .4), tip,
                  (hilt[0] - nx * 3, hilt[1] - ny * 3)])
    guard = tube([(hilt[0] + nx * 11, hilt[1] + ny * 11), (hilt[0] - nx * 11, hilt[1] - ny * 11)], [2.4, 2.4])
    S.append(Step("السيف المتوهج", [
        glow(blade, "#1a8cff", 40, .5), glow(blade, "#3fd0ff", 14, .95), glow(blade, "#b8f2ff", 4, 1),
        fill(blade, "#f2fdff"), fill(guard, "#2c2c3a"),
        fill(ellipse(hilt[0] - dx / L * 7, hilt[1] - dy / L * 7, 3, 3), "#2c2c3a")],
        "grow", origin=hilt, weight=.5))

    # 15. fire hits the shield and splashes around it
    sx, sy = shield_c[0] + 12, shield_c[1]
    ends = [((-2, -30), (-34, -74)), ((-2, -30), (-60, -62)), ((-2, -32), (-14, -92)), ((0, -28), (-48, -100)),
            ((-2, 30), (-32, 72)), ((-2, 30), (-62, 60)), ((-2, 32), (-16, 86)),
            ((4, -6), (34, -42)), ((4, 8), (32, 40))]
    splash = [((sx + p0[0], sy + p0[1]), (sx + p1[0], sy + p1[1])) for p0, p1 in ends]
    S.append(Step("ارتطام النار بالدرع", [
        glow(ellipse(sx - 14, sy, 300, 250), "#ff5a1a", 100, .32),
        *[fill(flame(600 + k, p0, p1, 9, 1.2, 7), "#ff5a14", .6, blur=3, mode="add") for k, (p0, p1) in enumerate(splash)],
        *[fill(flame(700 + k, p0, p1, 5, .6, 5), "#ffc06a", .75, blur=2, mode="add") for k, (p0, p1) in enumerate(splash)],
        glow(ellipse(sx, sy, 20, 40), "#fff2c8", 15, .9),
        fill(ellipse(sx + 2, sy, 8, 22), "#ffffff", .8, blur=4, mode="add")],
        "grow", origin=(sx, sy), weight=.6))

    # 16. embers
    emb = []
    r = random.Random(77)
    for _ in range(320):
        t = r.random()
        x = MOUTH[0] + (SH[0] - MOUTH[0]) * t + r.gauss(0, 44)
        y = MOUTH[1] + (SH[1] - MOUTH[1]) * t + r.gauss(0, 36) - r.random() * 100
        if math.hypot(x - 382, y - 364) > 30:          # keep sparks off her face
            emb.append((x, y, r.choice([.6, .8, 1, 1.3, 1.8])))
    for _ in range(120):
        emb.append((r.uniform(220, 760), r.uniform(380, 700), r.choice([.5, .7, 1])))
    S.append(Step("الشرر", [
        fill(dots(emb), "#ffd27a", .9, mode="add"),
        fill(dots([(x, y, s * 3) for x, y, s in emb if s > .9]), "#ff7a2a", .45, blur=2.5, mode="add")],
        "sparkle", weight=.5))

    # 17. finish: colour grade, vignette, film grain
    S.append(Step("اللمسات الأخيرة", [
        grade(shadows="#0b0820", highlights="#ffe9cf", amount=.45, contrast=1.06),
        vignette(.55), grain(.018, 3)],
        "sweep", weight=.7))
    return S
