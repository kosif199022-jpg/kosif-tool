"""Real programs for the 3d-spatial power cards.

The 3D maths each card relies on (perspective pre-scale, isometric projection, painter's algorithm,
Fibonacci spheres, SDF raymarching, ACES, banking from curvature, lighting ratios, procedural
placement rules, spline cameras) runs in numpy and is drawn with Pillow where a picture is the
result. Cards that need a live WebGL/three.js renderer, Blender, Cesium keys or HyperFrames are skipped.
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from .photo_video_footage import REPO, chk, jwrite, near, write_wav, read_wav, hexrgb

FONT = REPO / ".claude/skills/kosif-superpowers/proofs/_shared/fonts/Amiri-Bold.ttf"


def _recorded(fn):
    """Keep the computed observations as the program's output file when it draws nothing else."""
    def run(work):
        checks = fn(work)
        if not any(p.is_file() and p.stat().st_size for p in Path(work).rglob("*")):
            jwrite(work, f"{fn.__name__}.json", [{"check": n, "passed": bool(ok), "observed": str(o)} for n, ok, o in checks])
        return checks
    run.__name__ = fn.__name__
    return run


def sine_io(p):
    return 0.5 - 0.5 * math.cos(math.pi * min(max(p, 0), 1))


def rot_y(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def rot_x(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


CUBE_V = np.array([[x, y, z] for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)], float)
CUBE_F = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]


def soft_render(verts, faces, R, size=200, d=5.0, f=300.0, light=np.array([0.3, 0.5, -1.0]), ambient=0.0, diffuse=1.0):
    """Rotate, perspective-project with f/(z+d), painter-sort by mean z, flat-shade max(0, n.l)."""
    light = light / np.linalg.norm(light)
    v = verts @ R.T
    proj = np.column_stack([size / 2 + f * v[:, 0] / (v[:, 2] + d), size / 2 - f * v[:, 1] / (v[:, 2] + d)])
    centre = v.mean(0)
    drawn = []
    for face in faces:
        p = v[list(face)]
        n = np.cross(p[1] - p[0], p[2] - p[0])
        n /= np.linalg.norm(n)
        if n @ (p.mean(0) - centre) < 0:
            n = -n
        drawn.append((p[:, 2].mean(), face, n))
    drawn.sort(key=lambda t: -t[0])  # far (large z) first
    im = Image.new("RGB", (size, size), (0, 0, 0))
    dr = ImageDraw.Draw(im)
    shades = []
    for z, face, n in drawn:
        k = ambient + diffuse * max(0.0, float(n @ -light))
        g = int(round(255 * min(k, 1)))
        dr.polygon([tuple(proj[i]) for i in face], fill=(g, g, g))
        shades.append((z, g))
    return im, shades, proj


def d3_01(work):
    def decide(shot):
        real = {"turntable", "fly-through", "world", "point cloud", "terrain", "trajectory", "globe"}
        if shot in real:
            return "three.js seek scene"
        return "DOM/canvas layers (2.5D)"

    def camera(kind):
        return "orthographic" if kind == "chart-like" else "perspective"

    plan = {s: decide(s) for s in ("turntable", "title card", "terrain", "photo parallax")}
    (work / "PLAN.md").write_text("\n".join(f"{k}: {v}" for k, v in plan.items()))
    return [chk("orbit/terrain shots -> real 3D", plan["turntable"] == plan["terrain"] == "three.js seek scene", plan),
            chk("photo parallax and titles -> 2.5D layers", plan["photo parallax"].startswith("DOM"), plan),
            chk("chart-like 2.5D -> orthographic", camera("chart-like") == "orthographic", "ortho")]


def d3_02(work):
    P = 1200
    layers = {"bg": -400, "mid": -120, "subject": 0, "occluder": 200}
    pre = {k: (P - z) / P for k, z in layers.items()}
    apparent = {k: pre[k] * P / (P - z) for k, z in layers.items()}

    def orbit(t, T=2.5):
        return 8 * math.sin(2 * math.pi * t / T) / 2

    def parallax(z, ry_deg, P=P):
        return -z * math.sin(math.radians(ry_deg)) * P / (P - z)

    shifts = {k: parallax(z, 6) for k, z in layers.items()}
    peak = max(abs(orbit(x / 100)) for x in range(251))
    jwrite(work, "depth_rig.json", {"prescale": pre, "shift_at_6deg": shifts})
    return [chk("pre-scale (1200 - z)/1200 makes every layer fill the frame (apparent 1.0)",
                all(near(a, 1, 1e-12) for a in apparent.values()), pre),
            chk("depth separation: layers shift by depth under rotateY 6 deg", shifts["bg"] > shifts["mid"] > shifts["subject"] > shifts["occluder"],
                {k: round(v, 1) for k, v in shifts.items()}),
            chk("8 deg orbit (+-4) stays within rotateY <= 6", near(peak, 4, 1e-3) and peak <= 6, peak)]


def d3_03(work):
    W, H = 160, 90
    Z = {"bg": 0.45, "subject": 1.0, "fg": 1.22}
    base = {}
    for name, x in (("bg", 40), ("subject", 80), ("fg", 120)):
        im = Image.new("L", (W, H), 0)
        ImageDraw.Draw(im).rectangle([x - 3, 40, x + 3, 50], fill=255)
        base[name] = np.asarray(im, float)

    def cam(t):
        if t <= 1:
            return 1.0
        return 1.0 + 0.12 * sine_io((min(t, 6) - 1) / 5)

    def frame(t):
        out = np.zeros((H, W))
        for name, img in base.items():
            s = cam(t) ** Z[name]
            pil = Image.fromarray(img.astype(np.uint8))
            w2, h2 = round(W * s), round(H * s)
            sc = np.asarray(pil.resize((w2, h2), Image.BILINEAR), float)
            x0, y0 = (w2 - W) // 2, (h2 - H) // 2
            out = np.maximum(out, sc[y0:y0 + H, x0:x0 + W])
        return out

    def cx(img, lo, hi):
        cols = img[:, lo:hi].sum(0)
        return lo + (cols * np.arange(hi - lo)).sum() / cols.sum()

    f0, f6, f8 = frame(0), frame(6), frame(8)
    Image.fromarray(f6.astype(np.uint8)).save(work / "depth_frame_6s.png")
    move = {n: abs(cx(f6, lo, hi) - cx(f0, lo, hi)) for n, lo, hi in (("bg", 0, 60), ("fg", 100, 160))}
    return [chk("0-1 s hold, 6-8 s stop", np.array_equal(frame(0), frame(1)) and np.array_equal(f6, f8), "hold/stop"),
            chk("foreground (Z 1.22) moves more than background (Z 0.45)", move["fg"] > 2 * move["bg"] > 0, {k: round(v, 2) for k, v in move.items()}),
            chk("scale = camera^Z", near(cam(6) ** 1.22, 1.12 ** 1.22, 1e-12), round(cam(6) ** 1.22, 4))]


def d3_04(work):
    thickness = 12.0
    N = int(round(thickness / 1.5))
    gold = [hexrgb(h) for h in ("#b4641a", "#f5b54a", "#fff1bc")]

    def layer_colour(i):
        u = i / (N - 1)
        a, b = (gold[0], gold[1]) if u < 0.5 else (gold[1], gold[2])
        w = u * 2 if u < 0.5 else (u - 0.5) * 2
        return tuple(int(round(a[k] + (b[k] - a[k]) * w)) for k in range(3))

    ang = math.radians(35)
    u_ax, v_ax = np.array([math.cos(ang), 0.0]), np.array([0.0, 1.0])
    normal = np.array([math.sin(ang), 0.0]) * 1.5
    shape = np.array([(-20, -20), (20, -20), (20, 20), (-20, 20)], float)
    M = np.column_stack([u_ax, v_ax])
    im = Image.new("RGB", (120, 100), (10, 10, 10))
    d = ImageDraw.Draw(im)
    for i in range(N):
        off = np.array([60, 50]) + normal * (N - 1 - i)
        d.polygon([tuple(off + M @ p) for p in shape], fill=layer_colour(i))
    im.save(work / "extrusion.png")
    a = np.asarray(im).astype(int)
    back_px = a[50, int(60 + 20 * math.cos(ang) + normal[0] * (N - 1)) - 1]
    front_px = a[50, 60]
    matrix = (u_ax[0], u_ax[1], v_ax[0], v_ax[1], 60, 50)
    return [chk("N = thickness / 1.5 px layers", N == 8, N),
            chk("back layer darker, lit face #fff1bc on top", tuple(front_px) == hexrgb("#fff1bc") and back_px.sum() < front_px.sum(),
                (tuple(front_px), tuple(back_px))),
            chk("one projection matrix(ux,uy,vx,vy,cx,cy)", near(matrix[0], math.cos(ang), 1e-12) and len(matrix) == 6, matrix)]


def iso(x, y, z, S=20, OX=200, OY=60):
    c30 = math.cos(math.radians(30))
    return OX + (x - y) * c30 * S, OY + (x + y) * 0.5 * S - z * S


def d3_05(work):
    items = [("tower", 2, 1, 0), ("tree", 0, 0, 0), ("house", 1, 1, 0), ("roof", 1, 1, 1), ("bush", 3, 2, 0)]
    order = sorted(items, key=lambda t: (t[1] + t[2], t[3]))
    im = Image.new("RGB", (400, 260), "white")
    d = ImageDraw.Draw(im)
    for name, x, y, z in order:
        cx, cy = iso(x, y, z)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(40, 80, 160))
    im.save(work / "iso.png")
    x1, y1 = iso(1, 0, 0)
    x0, y0 = iso(0, 0, 0)
    pitch = math.degrees(math.atan(1 / math.sqrt(2)))
    names = [o[0] for o in order]
    return [chk("+x step moves (cos30*S, 0.5*S)", near(x1 - x0, 0.8660254 * 20, 1e-6) and near(y1 - y0, 10, 1e-12), (x1 - x0, y1 - y0)),
            chk("depth order by x + y, elevated after what is beneath", names.index("roof") == names.index("house") + 1 and names[0] == "tree",
                names),
            chk("true isometric pitch 35.264 deg", near(pitch, 35.264, 1e-3), round(pitch, 4))]


def d3_06(work):
    n = 24
    gx, gz = np.meshgrid(np.arange(n) - n / 2 + 0.5, np.arange(n) - n / 2 + 0.5)
    r = np.hypot(gx, gz)
    A, f, w = 2.0, 0.8, 3.0

    def heights(t):
        return A * np.maximum(0, np.sin(r * f - w * t))

    def crest_radius(t):
        return (math.pi / 2 + w * t) / f

    h0, h1 = heights(0), heights(0.5)
    np.save(work / "heights.npy", h1)
    rr = np.linspace(0, 12, 24001)

    def crest_list(t):
        prof = A * np.maximum(0, np.sin(rr * f - w * t))
        pk = (prof[1:-1] > prof[:-2]) & (prof[1:-1] >= prof[2:]) & (prof[1:-1] > 0.999 * A)
        return rr[1:-1][pk]

    c0, c1 = crest_list(0), crest_list(0.5)
    crests = (np.round(c0[:2], 3).tolist(), np.round(c1[:2], 3).tolist())
    crest_moved = near(float(c1[np.argmin(np.abs(c1 - c0[0] - 0.5 * w / f))]), crest_radius(0.5), 1e-3) and near(c0[0], crest_radius(0), 1e-3)
    rng = np.random.default_rng(1)
    accent = rng.random((n, n)) < 0.05
    stagger = (r * 0.010)
    return [chk("A*max(0, sin(r f - w t)): heights in [0, A]", h0.min() == 0 and h0.max() <= A, (h0.min(), round(h0.max(), 3))),
            chk("crest travels outward at w/f = 3.75 units/s", crest_moved, crests),
            chk("~5% accent tops", 0.02 < accent.mean() < 0.08, round(float(accent.mean()), 3)),
            chk("10 ms stagger by distance", near(stagger.max() - stagger.min(), 0.01 * (r.max() - r.min()), 1e-12), "10 ms/unit")]


def d3_07(work):
    P = 1200
    rx, rz = math.radians(35), math.radians(-18)
    drift = 45.0

    def project(x, y):
        x, y = x * math.cos(rz) - y * math.sin(rz), x * math.sin(rz) + y * math.cos(rz)
        yy, z = y * math.cos(rx), y * math.sin(rx)
        s = P / (P + z)
        return x * s, yy * s, s

    near_s = project(0, -400)[2]
    far_s = project(0, 400)[2]
    pos = lambda t: drift * t
    return [chk("tilted plane: far row smaller than near row", far_s < 1 < near_s, (round(near_s, 3), round(far_s, 3))),
            chk("drift 30-60 px/s", 30 <= pos(1) - pos(0) <= 60, pos(1)),
            chk("rotateX 20-50, rotateZ -15..-20", 20 <= math.degrees(rx) <= 50 and -20 <= math.degrees(rz) <= -15, (35, -18))]


def d3_08(work):
    def face(angle):
        a = angle % 360
        return "back" if 90 < a < 270 else "front"

    def flip_angle(t, T=1.2):
        return 360 * sine_io(t / T)

    beats = [0.0, 0.5, 1.0, 1.5, 2.0]
    span = 1.2
    seq = [face(flip_angle(t / 10)) for t in range(13)]
    (work / "flip.txt").write_text(" ".join(seq))
    return [chk("back face shown only between 90 and 270 deg", face(45) == "front" and face(180) == "back" and face(300) == "front", seq),
            chk("full 360 flip ends on the front", flip_angle(1.2) == 360 and face(flip_angle(1.2)) == "front", flip_angle(1.2)),
            chk("flip anchored to a downbeat, span within 0.8-1.6 s", 0.8 <= span <= 1.6 and 1.0 in beats, span)]


def d3_10(work):
    P, th = 1400, math.radians(50)

    def sprite(Y):
        Yp, z = Y * math.cos(th), Y * math.sin(th)
        return Yp, P / (P - z)

    a, b = sprite(-300), sprite(300)
    horizon = lambda H: [0.30 * H, 0.55 * H]
    return [chk("Y' = Y cos(theta)", near(sprite(300)[0], 300 * math.cos(th), 1e-12), round(sprite(300)[0], 2)),
            chk("scale = P/(P - z): sprites at the near edge larger", b[1] > 1 > a[1], (round(a[1], 3), round(b[1], 3))),
            chk("horizon in 30-55% of height", horizon(1080) == [324.0, 594.0], horizon(1080))]


def d3_12(work):
    k, s0, n, speed = 1.35, 0.05, 12, 0.8
    rng_ = k ** n

    def scales(t):
        return sorted((s0 * (k ** ((i + speed * t) % n))) for i in range(n))

    a, b = scales(0), scales(1 / speed)
    im = Image.new("L", (200, 200), 0)
    d = ImageDraw.Draw(im)
    for i, s in enumerate(scales(0.3)):
        r = s * 100
        rot = math.radians(7 * i)
        d.polygon([(100 + r * math.cos(rot + j * math.pi / 3), 100 + r * math.sin(rot + j * math.pi / 3)) for j in range(6)], outline=255)
    im.save(work / "tunnel.png")
    ratios = np.array(scales(0.37))
    return [chk("loop is seamless: after 1/speed s the same rings", np.allclose(a, b), (round(a[0], 4), round(b[0], 4))),
            chk("rings scale exponentially (constant ratio k)", np.allclose(ratios[1:] / ratios[:-1], k), round(float((ratios[1:] / ratios[:-1]).mean()), 4)),
            chk("6-20 layers", 6 <= n <= 20, n)]


def d3_16(work):
    def render(frame):
        R = rot_y(frame * 0.02) @ rot_x(0.4)
        im, shades, _ = soft_render(CUBE_V, CUBE_F, R, size=120, ambient=0.4, diffuse=0.8)
        return im, shades

    a, _ = render(45)
    b, _ = render(45)
    c, sh = render(46)
    a.save(work / "frame45.png")
    return [chk("same frame -> identical pixels (frame-driven)", np.array_equal(np.asarray(a), np.asarray(b)), "identical"),
            chk("next frame differs (rotation = frame*0.02)", not np.array_equal(np.asarray(a), np.asarray(c)), "differs"),
            chk("ambient 0.4 floor: no visible face darker than 0.4", min(g for _, g in sh) >= round(255 * 0.4) - 1, min(g for _, g in sh))]


def d3_19(work):
    R = rot_y(math.radians(30)) @ rot_x(math.radians(25))
    im, shades, proj = soft_render(CUBE_V, CUBE_F, R)
    im.save(work / "cube.png")
    a = np.asarray(im)
    v = CUBE_V @ R.T
    front_face = min(CUBE_F, key=lambda f: v[list(f)][:, 2].mean())
    c = proj[list(front_face)].mean(0)
    pix = int(a[int(c[1]), int(c[0]), 0])
    zs = [z for z, _ in shades]
    return [chk("painter's order back -> front (mean z descending)", zs == sorted(zs, reverse=True), [round(z, 2) for z in zs]),
            chk("nearest face is the visible pixel at its centre", pix == shades[-1][1], (pix, shades[-1][1])),
            chk("perspective f/(z+d): nearer vertices spread wider", np.ptp(proj[:, 0]) > 0, round(float(np.ptp(proj[:, 0])), 1))]


def fib_sphere(n):
    i = np.arange(n) + 0.5
    phi = np.arccos(1 - 2 * i / n)
    th = math.pi * (1 + 5 ** 0.5) * i
    return np.column_stack([np.cos(th) * np.sin(phi), np.sin(th) * np.sin(phi), np.cos(phi)])


def d3_20(work):
    n = 1000
    sph = fib_sphere(n)
    tor = np.column_stack([(1 + 0.35 * np.cos(np.linspace(0, 40 * math.pi, n))) * np.cos(np.linspace(0, 2 * math.pi, n)),
                           (1 + 0.35 * np.cos(np.linspace(0, 40 * math.pi, n))) * np.sin(np.linspace(0, 2 * math.pi, n)),
                           0.35 * np.sin(np.linspace(0, 40 * math.pi, n))])
    from scipy.spatial import cKDTree
    dnn = cKDTree(sph).query(sph, k=2)[0][:, 1]
    hemi = (sph[:, 2] > 0).mean()
    morph = lambda u: tor + (sph - tor) * u
    R = rot_y(math.radians(30))
    z = (sph @ R.T)[:, 2]
    size = 1 + 2 * (z + 1) / 2
    np.save(work / "points.npy", sph)
    return [chk("Fibonacci sphere: all points on the unit sphere", np.allclose(np.linalg.norm(sph, axis=1), 1), n),
            chk("even spread: nearest-neighbour spacing CV < 0.1, half per hemisphere", dnn.std() / dnn.mean() < 0.1 and near(hemi, 0.5, 0.01),
                (round(float(dnn.std() / dnn.mean()), 4), hemi)),
            chk("morph lerps torus -> sphere", np.allclose(morph(0), tor) and np.allclose(morph(1), sph), "lerp"),
            chk("size grows with depth z", np.corrcoef(z, size)[0, 1] > 0.999, "z->size")]


def smin(a, b, k=0.5):
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0, 1)
    return b + (a - b) * h - k * h * (1 - h)


def d3_21(work):
    c1, c2 = np.array([-0.6, 0, 0]), np.array([0.6, 0, 0])

    def sdf(p):
        return smin(np.linalg.norm(p - c1, axis=-1) - 0.5, np.linalg.norm(p - c2, axis=-1) - 0.5)

    def march(ro, rd, steps=96):
        t = np.zeros(len(ro))
        for _ in range(steps):
            d = sdf(ro + rd * t[:, None])
            t += d
        return t, np.abs(sdf(ro + rd * t[:, None])) < 1e-3

    W = 64
    ys, xs = np.mgrid[0:W, 0:W]
    ro = np.column_stack([(xs.ravel() - W / 2) / W * 3, (ys.ravel() - W / 2) / W * 3, np.full(W * W, -3.0)])
    rd = np.tile([0, 0, 1.0], (W * W, 1))
    t, hit = march(ro, rd)
    Image.fromarray((hit.reshape(W, W) * 255).astype(np.uint8)).save(work / "metaballs.png")
    t0, h0 = march(np.array([[-0.6, 0, -3.0]]), np.array([[0, 0, 1.0]]))
    bridge = hit.reshape(W, W)[W // 2, W // 2]
    hard_bridge = (min(np.linalg.norm(np.zeros(3) - c1), np.linalg.norm(np.zeros(3) - c2)) - 0.5) < 0
    return [chk("ray through a sphere centre hits at t = 3 - 0.5 = 2.5 (minus the blend)", h0[0] and 2.3 < t0[0] <= 2.5, round(float(t0[0]), 4)),
            chk("smooth union (k 0.5) fuses the gap a hard union leaves", bool(bridge) and not hard_bridge, "bridge"),
            chk("smin <= min of the two fields", bool(np.all(smin(np.linspace(0, 1, 9), np.linspace(1, 0, 9)) <= np.minimum(np.linspace(0, 1, 9),
                np.linspace(1, 0, 9)) + 1e-12)), "smin")]


def d3_25(work):
    n = 129
    x, z = np.meshgrid(np.linspace(0, 4600, n), np.linspace(0, 4600, n))
    h = 900 * np.exp(-((x - 2300) ** 2 + (z - 2300) ** 2) / 1.2e6) + 40 * np.sin(x / 300) * np.cos(z / 260)
    gy, gx = np.gradient(h, 4600 / (n - 1))
    slope = np.degrees(np.arctan(np.hypot(gx, gy)))
    pal = {"snow": "#f4f7fb", "rock": "#5d5a58", "grass": "#4e6e34", "sand": "#b9a77a"}

    def colour(hv, sl):
        if hv > 700:
            return "snow"
        if sl > 35:
            return "rock"
        if hv < 20:
            return "sand"
        return "grass"

    cls = np.vectorize(colour)(h, slope)
    img = np.array([[hexrgb(pal[c]) for c in row] for row in cls], np.uint8)
    Image.fromarray(img).save(work / "terrain_albedo.png")
    peak = np.unravel_index(np.argmax(h), h.shape)
    return [chk("peak is snow", cls[peak] == "snow", cls[peak]),
            chk("colour depends on height and slope (>= 3 classes)", len(set(cls.ravel())) >= 3, sorted(set(cls.ravel()))),
            chk("size 4600 m", x.max() == 4600, x.max())]


def d3_26(work):
    rng = np.random.default_rng(42)

    def height(x, z):
        return 200 + 0.1 * x

    def accept(x, z, h):
        return 0 <= h < 430

    def thin_prob(h):
        return 1.0 if h <= 300 else max(0.0, (430 - h) / 130)

    trees = []
    tries = 0
    while len(trees) < 22000 and tries < 60000:
        tries += 1
        x, z = rng.uniform(0, 3000), rng.uniform(0, 3000)
        h = height(x, z)
        if accept(x, z, h) and rng.random() < thin_prob(h):
            trees.append((x, z, h, 0.25 + rng.uniform(-0.035, 0.035)))
    t = np.array(trees)
    jwrite(work, "forest_stats.json", {"n": len(t)})
    low = ((t[:, 2] >= 200) & (t[:, 2] < 300)).sum() / 100
    high = ((t[:, 2] >= 380) & (t[:, 2] < 430)).sum() / 50
    return [chk("never above 430 m", t[:, 2].max() < 430, round(float(t[:, 2].max()), 1)),
            chk("thins between 300 and 430 m", high < 0.5 * low, (round(low, 1), round(high, 1))),
            chk("hue .25 +- .035, capped at 22000", np.all(np.abs(t[:, 3] - 0.25) <= 0.035) and len(t) <= 22000, len(t))]


def smooth(a, b, x):
    t = min(max((x - a) / (b - a), 0), 1)
    return t * t * (3 - 2 * t)


def d3_27(work):
    elev = lambda t: 2.5 + 24 * smooth(0, 6.5, t) - 8 * smooth(8, 10, t) + 12 * smooth(12.5, 15.5, t)
    turb = lambda overcast: 3 + 7 * overcast
    fog = lambda d, k=1.1e-4: 1 - math.exp(-(k * d) ** 2)
    vals = {t: elev(t) for t in (0, 7, 11, 16)}
    jwrite(work, "sun.json", vals)
    return [chk("dawn 2.5 -> day 26.5 -> overcast 18.5 -> clear 30.5", vals == {0: 2.5, 7: 26.5, 11: 18.5, 16: 30.5}, vals),
            chk("turbidity 3 + 7*overcast", turb(0) == 3 and turb(1) == 10, (turb(0), turb(1))),
            chk("FogExp2 1.1e-4: far ridge (12 km) mostly fogged, 1 km nearly clear", fog(12000) > 0.8 and fog(1000) < 0.02,
                (round(fog(12000), 3), round(fog(1000), 4)))]


def d3_28(work):
    heave = lambda t: .09 * math.sin(1.25 * t + .4) + .035 * math.sin(2.3 * t + 1.7)
    ts = np.linspace(0, 60, 6001)
    hv = np.array([heave(t) for t in ts])
    spec = np.abs(np.fft.rfft(hv - hv.mean()))
    fr = np.fft.rfftfreq(len(hv), ts[1] - ts[0]) * 2 * math.pi
    top = sorted(fr[np.argsort(spec)[-2:]])
    np.save(work / "heave.npy", hv)
    return [chk("heave stays within +-0.125 m", np.abs(hv).max() <= 0.125, round(float(np.abs(hv).max()), 4)),
            chk("two swell components at 1.25 and 2.3 rad/s", near(top[0], 1.25, 0.06) and near(top[1], 2.3, 0.06), [round(f, 3) for f in top])]


def d3_29(work):
    sun = np.array([math.cos(math.radians(5)), math.sin(math.radians(5)), 0])
    ramp = [hexrgb("#5a3a8a"), hexrgb("#b066a0"), hexrgb("#f0c09a")]
    W = 80
    ys, xs = np.mgrid[0:W, 0:W]
    nx, ny = (xs - W / 2) / (W / 2), -(ys - W / 2) / (W / 2)
    inside = nx ** 2 + ny ** 2 < 1
    nz = np.sqrt(np.clip(1 - nx ** 2 - ny ** 2, 0, 1))
    ndl = nx * sun[0] + ny * sun[1]
    band = np.digitize(ndl, [-0.2, 0.4])
    img = np.zeros((W, W, 3), np.uint8)
    for b in range(3):
        img[inside & (band == b)] = ramp[b]
    Image.fromarray(img).save(work / "toon_cloud.png")
    colours = {tuple(c) for c in img[inside]}
    return [chk("exactly 3 bands", colours == {tuple(r) for r in ramp}, len(colours)),
            chk("lit side (towards the low sun) is peach, far side violet", tuple(img[W // 2, W - 3]) == ramp[2] and tuple(img[W // 2, 2]) == ramp[0],
                (tuple(img[W // 2, W - 3]), tuple(img[W // 2, 2])))]


def d3_31(work):
    layers = [(700, 140), (1400, 260), (2600, 420), (4500, 650)]
    fov = math.radians(36)
    ang = [math.degrees(2 * math.atan(h / 2 / d)) for d, h in layers]
    ROAD_W = 6

    def flatten(dx):
        return smooth(ROAD_W, ROAD_W + 30, abs(dx))

    lights_km = 6.5
    light_px = 0.5 * 1080 / math.tan(fov / 2) * 2 / (lights_km * 1000)
    return [chk("farther ridges are taller but read smaller (angular height falls)", all(a > b for a, b in zip(ang, ang[1:])),
                [round(a, 2) for a in ang]),
            chk("terrain flattened on the road, untouched 30 m beyond", flatten(0) == 0 and flatten(ROAD_W + 30) == 1, (flatten(0), flatten(40))),
            chk("2 m lamp at 6.5 km is sub-pixel at fov 36 (a point of light)", light_px < 1, round(light_px, 3))]


def d3_32(work):
    beam = lambda s: 1.12 * math.sin(math.pi * (.13 + .87 * s)) ** .62
    sheer = lambda s: .78 + .62 * s ** 3.2 + .22 * (1 - s) ** 5
    keel = lambda s: -.62 * math.sin(math.pi * (.04 + .96 * s)) ** .45
    L, ns, nphi = 7.2, 72, 16
    verts = []
    for side in (-1, 1):
        for i in range(ns):
            s = i / (ns - 1)
            for j in range(nphi):
                phi = j / (nphi - 1)
                x = side * beam(s) * (1 - (1 - phi) ** 2.4)
                y = keel(s) + (sheer(s) - keel(s)) * phi
                verts.append((x, y, s * L))
    v = np.array(verts)
    np.save(work / "hull.npy", v)
    half = len(v) // 2
    smax = max(range(ns), key=lambda i: beam(i / (ns - 1))) / (ns - 1)
    return [chk("72 x 16 grid per side", len(v) == 2 * 72 * 16, len(v)),
            chk("mirror-symmetric", np.allclose(v[:half, 0], -v[half:, 0]) and np.allclose(v[:half, 1:], v[half:, 1:]), "mirror"),
            chk("widest ~ amidships (beam peaks at s ~ .43), max 1.12", 0.35 < smax < 0.5 and np.abs(v[:, 0]).max() <= 1.12, round(smax, 3)),
            chk("length 7.2 m, bow sheer rises to 1.40", near(v[:, 2].max(), 7.2, 1e-12) and near(sheer(1), 1.40, 1e-12), sheer(1))]


def hash2(x, y, seed=0):
    return (np.sin(x * 127.1 + y * 311.7 + seed * 74.7) * 43758.5453) % 1.0


def d3_33(work):
    gx, gz = np.meshgrid(np.arange(60), np.arange(70))
    keep = (gx % 6 != 0) & (gz % 7 != 0)
    buildings = int(min(keep.sum(), 2600))
    u, y = np.meshgrid(np.arange(0, 48, 0.05), np.arange(0, 96, 0.05))
    cu, cy = np.floor(u / 2.4), np.floor(y / 3.2)
    fu, fy = (u / 2.4) % 1, (y / 3.2) % 1
    pane = (fu > .18) & (fu < .82) & (fy > .22) & (fy < .78)
    out = {}
    for lit in (0.32, 0.8):
        on = hash2(cu, cy) > 1 - lit
        cells = {(a, b): v for a, b, v in zip(cu[pane].ravel(), cy[pane].ravel(), on[pane].ravel())}
        out[lit] = sum(cells.values()) / len(cells)
    Image.fromarray(((pane & (hash2(cu, cy) > 0.5)) * 255).astype(np.uint8)[::4, ::4]).save(work / "windows.png")
    pane_frac = pane.mean()
    return [chk("avenues skipped (gx%6, gz%7), up to 2600 buildings", not keep[0].any() and buildings == 2600, buildings),
            chk("lit fraction tracks the lit parameter (.32 / .8)", near(out[0.32], 0.32, 0.07) and near(out[0.8], 0.8, 0.07),
                {k: round(v, 3) for k, v in out.items()}),
            chk("window mask .18-.82 x .22-.78 = 35% of the facade", near(pane_frac, 0.64 * 0.56, 0.01), round(float(pane_frac), 4))]


def d3_35(work):
    g = 9.81

    def bank(v, kappa):
        return min(math.degrees(math.atan(v * v * kappa / g)), 80)

    R = 500
    return [chk("bank = atan(v^2 k / g): 100 m/s on a 500 m turn -> 63.9 deg", near(bank(100, 1 / R), math.degrees(math.atan(20 / g)), 1e-9)
                and near(bank(100, 1 / R), 63.88, 0.05), round(bank(100, 1 / R), 2)),
            chk("straight flight is level", bank(100, 0) == 0, 0),
            chk("capped at 80 deg", bank(300, 1 / 100) == 80, bank(300, 1 / 100))]


def d3_36(work):
    key, fill_stops = 1.0, 2
    fill = key / 2 ** fill_stops
    ratio = (key + fill) / fill
    fov_v = math.degrees(2 * math.atan(12 / 85))
    fov_h = math.degrees(2 * math.atan(18 / 85))
    jwrite(work, "light_rig.json", {"key": key, "fill": fill, "ratio": ratio, "K": [5600, 6500, 4300]})
    return [chk("fill 2 stops under the key -> 5:1 lighting ratio", ratio == 5.0, ratio),
            chk("85 mm on full frame ~ 24 deg (horizontal)", near(fov_h, 24, 0.2), (round(fov_h, 2), round(fov_v, 2))),
            chk("rim .5 stop", near(2 ** -0.5, 0.7071, 1e-4), round(2 ** -0.5, 4))]


def aces(x):
    a, b, c, d, e = 2.51, 0.03, 2.43, 0.59, 0.14
    return np.clip(x * (a * x + b) / (x * (c * x + d) + e), 0, 1)


def d3_38(work):
    rng = np.random.default_rng(2)
    hdr = np.full((64, 64), 0.3)
    hdr[30:34, 30:34] = 4.0
    thr = 0.85
    bright = np.where(aces(hdr) > thr, aces(hdr), 0)
    from scipy.ndimage import gaussian_filter
    bloom = gaussian_filter(bright, 3) * 0.5
    grain = rng.normal(0, 0.22 * 0.05, hdr.shape)
    out = np.clip(aces(hdr) + bloom + grain, 0, 1)
    srgb = np.where(out <= 0.0031308, 12.92 * out, 1.055 * out ** (1 / 2.4) - 0.055)
    Image.fromarray((srgb * 255).astype(np.uint8)).save(work / "post.png")
    return [chk("ACES maps 0 -> 0, compresses highlights below 1", aces(np.array(0.0)) == 0 and 0.95 < float(aces(np.array(4.0))) <= 1,
                round(float(aces(np.array(4.0))), 4)),
            chk("ACES known values: 0.18 -> 0.267, 1.0 -> 0.804 (highlights compressed)", near(float(aces(np.array(0.18))), 0.2669, 1e-3)
                and near(float(aces(np.array(1.0))), 0.8038, 1e-3), (round(float(aces(np.array(0.18))), 4), round(float(aces(np.array(1.0))), 4))),
            chk("threshold .85: only the hot spot blooms", bright[0, 0] == 0 and bright[31, 31] > 0, float(bright[31, 31])),
            chk("bloom spreads light beyond the hot spot", bloom[31, 37] > 0.001 and bloom[0, 0] < 1e-6, round(float(bloom[31, 37]), 4)),
            chk("sRGB output encode (0.5 linear -> 0.735)", near(1.055 * 0.5 ** (1 / 2.4) - 0.055, 0.7354, 1e-3), "srgb")]


def catmull_t(P, u):
    n = len(P) - 1
    i = min(int(u * n), n - 1)
    t = u * n - i
    p0, p1, p2, p3 = P[max(i - 1, 0)], P[i], P[i + 1], P[min(i + 2, n)]
    return 0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3)


def d3_43(work):
    d = work / "scaffold"
    r = subprocess.run([sys.executable, str(REPO / "tools" / "kosif.py"), "scaffold", "cinematic-3d", str(d)],
                       capture_output=True, text=True, timeout=60, cwd=REPO)
    words = [{"word": w, "start": s, "end": s + 0.4} for w, s in (("الجبل", 0.5), ("الوادي", 2.1), ("النهر", 3.9), ("البحر", 6.0))]
    P = np.array([(0, 5, 20), (10, 6, 10), (20, 4, 0), (30, 3, -10)], float)
    times = [w["start"] for w in words]

    def cam(t):
        if t <= times[0]:
            return P[0]
        for k in range(len(times) - 1):
            if t <= times[k + 1]:
                u = (k + sine_io((t - times[k]) / (times[k + 1] - times[k]))) / (len(P) - 1)
                return catmull_t(P, u)
        return P[-1]

    hits = [np.allclose(cam(t), P[i]) for i, t in enumerate(times)]
    v = [np.linalg.norm(cam(times[1] + e) - cam(times[1] - e)) for e in (1e-4,)]
    return [chk("cinematic-3d scaffold created", r.returncode == 0 and (d / "PLAN.md").is_file(), sorted(p.name for p in d.iterdir()) if d.is_dir() else r.stderr[-200:]),
            chk("camera sits on each waypoint at its narrated word", all(hits), hits),
            chk("ease-in-out: camera at rest on the word (velocity ~0)", v[0] < 1e-3, v[0])]


def d3_44(work):
    def plinth_y(t):
        if t >= 0.6:
            return 0.0
        p = t / 0.6
        return 2.0 * (1 - p * p)

    def orbit(t):
        return 90 * sine_io((t - 0.6) / 4.0) if t >= 0.6 else 0

    def callout(t):
        p = min(max((t - 2.0) / 0.4, 0), 1)
        return 1 - (1 - p) ** 3

    jwrite(work, "turntable.json", {"keys": [0, 0.6, 2.0, 2.4, 4.6, 6.0]})
    return [chk("drop lands at 0.6 s (ease-in quad)", plinth_y(0) == 2 and plinth_y(0.6) == 0 and plinth_y(0.3) == 1.5, plinth_y(0.3)),
            chk("orbit 90 deg from 0.6 to 4.6 s, half way at 2.6", orbit(4.6) == 90 and near(orbit(2.6), 45, 1e-9), orbit(2.6)),
            chk("callout draws 2.0-2.4 s, hero hold to 6.0", callout(2.4) == 1 and callout(1.9) == 0 and orbit(6.0) == 90, callout(2.2))]


def d3_45(work):
    parts = {"lid": np.array([0, 1.0, 0]), "body": np.array([0, 0, 0.0]), "base": np.array([0, -1.0, 0]), "button": np.array([1.0, 0, 0])}
    axis = {k: (v / np.linalg.norm(v) if np.linalg.norm(v) else np.zeros(3)) for k, v in parts.items()}

    def pos(name, t, i):
        tt = t - i * 0.15
        if tt < 1:
            e = 0
        elif tt < 3:
            e = sine_io((tt - 1) / 2)
        elif tt < 5:
            e = 1
        else:
            e = 1 - sine_io((tt - 5) / 2)
        return parts[name] + axis[name] * 1.5 * e

    names = list(parts)
    at4 = {n: pos(n, 4, i) for i, n in enumerate(names)}
    end = {n: pos(n, 7.5, i) for i, n in enumerate(names)}
    jwrite(work, "exploded.json", {k: v.tolist() for k, v in at4.items()})
    return [chk("parts move along their own axis (lid up, base down)", at4["lid"][1] == 2.5 and at4["base"][1] == -2.5, at4["lid"].tolist()),
            chk("no invented motion for the core part", np.allclose(at4["body"], 0), at4["body"].tolist()),
            chk("150 ms stagger between parts", pos("lid", 1.1, 0)[1] > 1 and pos("base", 1.1, 2)[1] == -1, "stagger"),
            chk("reassembled by 7 s (+stagger)", all(np.allclose(end[n], parts[n]) for n in names), "home")]


def d3_47(work):
    rng = np.random.default_rng(4)
    pts = rng.uniform(-1, 1, (5000, 3))
    planes = {"closed": 1.2, "half": 0.0}

    def clip(p, state, t):
        a, b = planes["closed"], planes[state]
        c = a + (b - a) * sine_io(t / 1.0)
        return p[p[:, 0] < c]

    terrain = rng.normal(0, 300, (50, 50))
    exaggeration = 3
    submerged = (terrain < 0).mean()
    label = f"vertical exaggeration x{exaggeration}"
    jwrite(work, "cutaway.json", {"label": label, "sea_level_m": 0, "submerged_fraction": submerged})
    half = clip(pts, "half", 1.0)
    return [chk("clip plane reveals in 1 s: all kept at 0 s, half at 1 s", len(clip(pts, "half", 0)) == 5000 and near(len(half) / 5000, 0.5, 0.03),
                len(half)),
            chk("sea-level sheet at 0 m covers the submerged terrain", 0.4 < submerged < 0.6, round(float(submerged), 3)),
            chk("exaggeration declared", "exaggeration x3" in label, label)]


def d3_48(work):
    chapters = [("assembled", 0.0, 0.25), ("exploded", 0.25, 0.5), ("mechanism", 0.5, 0.75), ("reassembled", 0.75, 1.0)]

    def pose(u):
        for name, a, b in chapters:
            if a <= u < b or (u == 1 and b == 1):
                return name, (u - a) / (b - a)

    fps, seconds = 30, 12
    to_u = lambda f: f / (fps * seconds - 1)
    poses = [pose(to_u(f))[0] for f in range(fps * seconds)]
    jwrite(work, "timeline.json", {"chapters": chapters})
    return [chk("one normalised 0-1 timeline drives all chapters", poses[0] == "assembled" and poses[-1] == "reassembled", (poses[0], poses[-1])),
            chk("frame time maps onto u (frame 180/359 ~ .5 -> mechanism)", pose(to_u(180))[0] == "mechanism", round(to_u(180), 4)),
            chk("chapters in narrative order", [c[0] for c in chapters] == list(dict.fromkeys(poses)), list(dict.fromkeys(poses)))]


def d3_49(work):
    from PIL import ImageFont, features
    import arabic_reshaper
    from bidi.algorithm import get_display
    text = "نور"
    font = ImageFont.truetype(str(FONT), 64)
    W, H = 512, 128
    tex = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(tex)
    if features.check("raqm"):
        d.text((W - 20, 20), text, font=font, fill=255, anchor="ra", direction="rtl")
        mode = "raqm rtl"
    else:
        d.text((W - 20, 20), get_display(arabic_reshaper.reshape(text)), font=font, fill=255, anchor="ra")
        mode = "reshaped"
    tex.save(work / "text_texture.png")
    a = np.asarray(tex) > 0
    ab = Image.new("L", (W, H), 0)
    if mode.startswith("raqm"):
        ImageDraw.Draw(ab).text((W - 20, 10), "اب", font=font, fill=255, anchor="ra", direction="rtl")
    else:
        ImageDraw.Draw(ab).text((W - 20, 10), get_display(arabic_reshaper.reshape("اب")), font=font, fill=255, anchor="ra")
    ink = (np.asarray(ab) > 0).sum(0)
    xs_ = np.where(ink > 0)[0]
    tall = int(np.argmax(ink))
    alef_cols = (int(xs_.min()), tall, int(xs_.max()))
    alef_right = tall > (xs_.min() + xs_.max()) / 2
    cols = np.where(a.any(0))[0]
    iso_w = sum(font.getbbox(ch)[2] - font.getbbox(ch)[0] for ch in text)

    def sphere_uv(theta, phi):
        return (theta / (2 * math.pi)) % 1, phi / math.pi

    spin = lambda t: (15 * t) % 360
    return [chk("right-to-left: in 'اب' the alef (first letter, tallest stroke) is on the right", alef_right, alef_cols),
            chk("letters joined (word narrower than its isolated letters side by side)", int(np.ptp(cols)) < iso_w, (int(np.ptp(cols)), iso_w, mode)),
            chk("texture wraps the sphere (u wraps at 2*pi)", near(sphere_uv(2 * math.pi + 0.5, 1)[0], sphere_uv(0.5, 1)[0], 1e-12), "uv"),
            chk("spin 15 deg/s", spin(24) == 0 and spin(1) == 15, spin(1))]


def cubic_bezier(x1, y1, x2, y2):
    def bez(t, a, b):
        return 3 * a * t * (1 - t) ** 2 + 3 * b * t * t * (1 - t) + t ** 3

    def solve(x):
        lo, hi = 0.0, 1.0
        for _ in range(60):
            mid = (lo + hi) / 2
            if bez(mid, x1, x2) < x:
                lo = mid
            else:
                hi = mid
        return bez((lo + hi) / 2, y1, y2)
    return solve


def d3_50(work):
    press = lambda t: -0.3 * math.sin(math.pi * min(max(t / 0.15, 0), 1))
    lid = lambda t: 110 * (1 - sine_io(t / 1.0))
    ease = cubic_bezier(.34, 1.56, .64, 1)
    pop = lambda t: 0.8 + 0.2 * ease(min(t / 0.35, 1))
    peak = max(pop(k / 1000) for k in range(351))
    jwrite(work, "interactions.json", {"press_ms": 150, "lid": [110, 0], "pop_peak": peak})
    return [chk("button press 150 ms: deepest at 75 ms, back up at 150", near(press(0.075), -0.3, 1e-12) and near(press(0.15), 0, 1e-12), press(0.075)),
            chk("lid 110 -> 0 in ~1 s", lid(0) == 110 and near(lid(1), 0, 1e-12) and near(lid(0.5), 55, 1e-9), lid(0.5)),
            chk("pop 0.8 -> 1 overshoots with cubic-bezier(.34,1.56,.64,1)", peak > 1.0 and near(pop(0.35), 1, 1e-6), round(peak, 4))]


def d3_51(work):
    sr = 8000
    t = np.arange(int(sr * 8)) / sr
    sig = 0.3 * np.sin(2 * math.pi * 220 * t) * (t < 6)
    kicks = [0.5, 1.5, 2.5, 3.5]
    for k in kicks:
        idx = (t >= k) & (t < k + 0.08)
        sig[idx] += 0.8 * np.sin(2 * math.pi * 60 * (t[idx] - k)) * np.exp(-(t[idx] - k) * 40)
    write_wav(work / "track.wav", sig, sr)
    x, sr2 = read_wav(work / "track.wav")
    x = x if x.ndim == 1 else x.mean(1)
    hop = sr // 30
    frames = len(x) // hop
    rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2)) for i in range(frames)])
    low = []
    for i in range(frames):
        seg = x[i * hop:(i + 1) * hop]
        sp = np.abs(np.fft.rfft(seg))
        fr = np.fft.rfftfreq(len(seg), 1 / sr)
        low.append(sp[fr < 120].sum() / (sp.sum() + 1e-9))
    low = np.array(low)
    onsets = [i / 30 for i in range(1, frames) if low[i] > 0.3 and low[i - 1] <= 0.3]
    silent = [i / 30 for i in range(frames) if rms[i] < 1e-3]
    jwrite(work, "channels.json", {"rms": rms.round(4).tolist(), "bass": low.round(3).tolist(), "kicks": onsets})
    meters_per_tape_second = 120 / 8
    return [chk("kicks found at 0.5/1.5/2.5/3.5 s (+-1 frame)", len(onsets) == 4 and all(abs(a - b) <= 1 / 30 + 1e-9 for a, b in zip(onsets, kicks)),
                [round(o, 3) for o in onsets]),
            chk("silence after 6 s detected (world freezes / negative)", bool(silent) and near(silent[0], 6.0, 1 / 30 + 1e-9), silent[:1]),
            chk("8 tape-seconds across 120 m = 15 m per second", meters_per_tape_second == 15, meters_per_tape_second)]


def d3_52(work):
    speed, bob_amp, bob_hz = 1.4, 0.02, 1.8
    fps = 30
    ts = np.arange(0, 10, 1 / fps)
    z = speed * ts
    y = 1.6 + bob_amp * np.sin(2 * math.pi * bob_hz * ts)
    spec = np.abs(np.fft.rfft(y - y.mean()))
    f = np.fft.rfftfreq(len(y), 1 / fps)[np.argmax(spec)]
    np.save(work / "camera_path.npy", np.column_stack([ts, y, z]))
    cuts = np.abs(np.diff(z)).max()
    return [chk("walks 1.4 m/s (14 m in 10 s)", near(z[-1] + speed / fps, 14, 1e-9), round(float(z[-1]), 3)),
            chk("head bob 2 cm at 1.8 Hz", near(np.ptp(y) / 2, 0.02, 1e-3) and near(f, 1.8, 0.1), (round(float(np.ptp(y) / 2), 4), f)),
            chk("no cuts: per-frame step constant", near(cuts, speed / fps, 1e-9), cuts)]


def d3_g01(work):
    def update(t):
        R = rot_y(0.9 * t) @ rot_x(0.3)
        return soft_render(CUBE_V, CUBE_F, R, size=240, ambient=0.2, diffuse=0.8)[0]

    fps = 30
    a = update(37 / fps)
    rng = np.random.default_rng(0)
    wall = 37 / fps + 1 / 60 + abs(rng.normal(0, 0.004))
    b = update(37 / fps)
    c = update(wall)
    a.save(work / "frame37.png")
    pr = lambda dpr: min(dpr, 2)
    return [chk("export t = frame/fps reproduces the frame exactly", np.array_equal(np.asarray(a), np.asarray(b)), "identical"),
            chk("a jittered wall-clock time does not (why not to use rAF timing)", not np.array_equal(np.asarray(a), np.asarray(c)), round(wall, 5)),
            chk("pixel ratio capped at 2", pr(3) == 2 and pr(1) == 1, pr(3))]


_PROGRAMS = {
    "3D-01": d3_01, "3D-02": d3_02, "3D-03": d3_03, "3D-04": d3_04, "3D-05": d3_05, "3D-06": d3_06, "3D-07": d3_07,
    "3D-08": d3_08, "3D-10": d3_10, "3D-12": d3_12, "3D-16": d3_16, "3D-19": d3_19, "3D-20": d3_20, "3D-21": d3_21,
    "3D-25": d3_25, "3D-26": d3_26, "3D-27": d3_27, "3D-28": d3_28, "3D-29": d3_29, "3D-31": d3_31, "3D-32": d3_32,
    "3D-33": d3_33, "3D-35": d3_35, "3D-36": d3_36, "3D-38": d3_38, "3D-43": d3_43, "3D-44": d3_44, "3D-45": d3_45,
    "3D-47": d3_47, "3D-48": d3_48, "3D-49": d3_49, "3D-50": d3_50, "3D-51": d3_51, "3D-52": d3_52, "3D-G01": d3_g01,
}
PROGRAMS = {k: _recorded(v) for k, v in _PROGRAMS.items()}
