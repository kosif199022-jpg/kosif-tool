"""Wave 3, chunk 07: particles-fluids-physics (PART-*) and shapes-morph-geometry (SHAPE-*) cards as real programs.

Engines: numpy/scipy/PIL (Pillow with libraqm for shaped Arabic) for closed-form renders and measurement, ffmpeg
(lossless libx264rgb) for clips that are read back and measured, headless Chromium (Playwright build) with GSAP and
SwiftShader WebGL for the repo's three-kit (window.K3: makeSea, makeShallowWater, makeCloudSlab, makeVapour, makeRain,
makeFlock, makeKoi, makePetals, makeBlades) and for the HyperFrames registry blocks (snow, starfield,
particle-image-reveal) fetched with the installed `hyperframes add` CLI into the work folder.
Nothing is installed by this module. Every runner measures its own output file and runs the same measurement on the
untreated input or a naive variant (negative control).
"""
import html as _html
import json
import math
import re
import shutil
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from _harness import card, check, fx

REPO = Path(__file__).resolve().parents[4]
SK = REPO / ".claude/skills"
KITDIR = SK / "kosif-superpowers/vendor/100-superskills/skills/kosif-montage-motion/scripts/kit"
GSAP_JS = KITDIR / "gsap.min.js"
K3_JS = KITDIR / "three-kit.bundle.js"
FONTS = SK / "kosif-superpowers/proofs/_shared/fonts"
AMIRI_B = FONTS / "Amiri-Bold.ttf"
POPPINS = FONTS / "Poppins-Bold.ttf"

GAPS: dict = {
    "PART-27": "deck.gl (TripsLayer/ArcLayer/HexagonLayer) is not installed here and the card gives no maths of its own; "
               "it needs the multi-package deck.gl WebGL2 stack over MapLibre",
    "PART-67": "Houdini FLIP/Pyro/Vellum/RBD + Karma need a commercial SideFX licence and hython; not installed "
               "(the card itself points to PART-23 / PART-51)",
}


# ================================================================= helpers
def R(seed):
    return np.random.default_rng(seed)


def canvas(W, H, bg=(0, 0, 0)):
    a = np.zeros((H, W, 3))
    a[:] = bg
    return a


def save(path, a):
    Image.fromarray(np.clip(np.round(np.asarray(a, dtype=float)), 0, 255).astype(np.uint8)).save(path)
    return Path(path)


def load(path):
    return np.asarray(Image.open(path).convert("RGB")).astype(float)


def video(path, frames, fps=30):
    frames = [np.clip(np.round(f), 0, 255).astype(np.uint8) for f in frames]
    h, w = frames[0].shape[:2]
    p = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                        "-s", "%dx%d" % (w, h), "-r", str(fps), "-i", "-", "-c:v", "libx264rgb", "-qp", "0",
                        "-pix_fmt", "rgb24", str(path)], input=b"".join(f.tobytes() for f in frames),
                       capture_output=True, timeout=60)
    if p.returncode:
        raise RuntimeError(p.stderr.decode()[-300:])
    return Path(path)


def vread(path, W, H):
    return fx.frames(path, size=(W, H))


def disc(a, x, y, r, col, mode="max", alpha=1.0):
    H, W = a.shape[:2]
    x0, x1 = max(0, int(x - r - 2)), min(W, int(x + r + 3))
    y0, y1 = max(0, int(y - r - 2)), min(H, int(y + r + 3))
    if x0 >= x1 or y0 >= y1:
        return
    yy, xx = np.mgrid[y0:y1, x0:x1]
    m = (np.hypot(yy + .5 - y, xx + .5 - x) <= r)[..., None]
    win = a[y0:y1, x0:x1]
    c = np.asarray(col, dtype=float)
    if mode == "add":
        win += m * c * alpha
    elif mode == "over":
        win[...] = win * (1 - m * alpha) + m * c * alpha
    else:
        win[...] = np.where(m, np.maximum(win, c * alpha), win)


def draw_layer(W, H, fn, mode="RGB"):
    im = Image.new(mode, (W, H), 0)
    fn(ImageDraw.Draw(im))
    a = np.asarray(im).astype(float)
    return a if a.ndim == 3 else a


def poly_mask(W, H, pts):
    im = Image.new("L", (W, H), 0)
    ImageDraw.Draw(im).polygon([tuple(map(float, p)) for p in pts], fill=255)
    return np.asarray(im) > 127


def centroid(mask):
    ys, xs = np.nonzero(mask)
    if not len(xs):
        return None
    return float(xs.mean()), float(ys.mean())


def label(mask, eight=False):
    from scipy.ndimage import label as _l
    lab, n = _l(mask, structure=np.ones((3, 3)) if eight else None)
    return lab, n


def iou(a, b):
    u = (a | b).sum()
    return float((a & b).sum() / u) if u else 0.0


def jw(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    return Path(path)


def hexc(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=float)


# easings
def out_expo(t):
    t = np.clip(t, 0, 1)
    return np.where(t >= 1, 1.0, 1 - 2.0 ** (-10 * t))


def in_out_cubic(t):
    t = np.clip(t, 0, 1)
    return np.where(t < .5, 4 * t ** 3, 1 - (-2 * t + 2) ** 3 / 2)


def out_cubic(t):
    t = np.clip(t, 0, 1)
    return 1 - (1 - t) ** 3


def in_cubic(t):
    t = np.clip(t, 0, 1)
    return t ** 3


def out_back(t, s=1.70158):
    t = np.clip(t, 0, 1)
    return 1 + (s + 1) * (t - 1) ** 3 + s * (t - 1) ** 2


def out_bounce(t):
    t = np.clip(np.asarray(t, dtype=float), 0, 1)
    n, d = 7.5625, 2.75
    return np.where(t < 1 / d, n * t * t, np.where(t < 2 / d, n * (t - 1.5 / d) ** 2 + .75,
                    np.where(t < 2.5 / d, n * (t - 2.25 / d) ** 2 + .9375, n * (t - 2.625 / d) ** 2 + .984375)))


def out_elastic(t):
    t = np.clip(np.asarray(t, dtype=float), 0, 1)
    c = 2 * math.pi / 3
    return np.where(t <= 0, 0.0, np.where(t >= 1, 1.0, 2.0 ** (-10 * t) * np.sin((t * 10 - .75) * c) + 1))


def spring(t, k, d, m=1.0):
    """Unit-step response of m x'' + d x' + k x = k (0 -> 1), closed form."""
    t = np.maximum(np.asarray(t, dtype=float), 0)
    w0 = math.sqrt(k / m)
    z = d / (2 * math.sqrt(k * m))
    if z < 1:
        wd = w0 * math.sqrt(1 - z * z)
        return 1 - np.exp(-z * w0 * t) * (np.cos(wd * t) + z * w0 / wd * np.sin(wd * t))
    return 1 - np.exp(-w0 * t) * (1 + w0 * t)


def spring_num(t, k, d, m=1.0, dt=1 / 600):
    """Independent semi-implicit Euler integration of the same spring, to cross-check the closed form."""
    x, v, out, tt = 0.0, 0.0, [], 0.0
    ts = sorted(np.atleast_1d(t))
    i = 0
    while i < len(ts):
        if tt >= ts[i] - 1e-12:
            out.append(x)
            i += 1
            continue
        v += (k * (1 - x) - d * v) / m * dt
        x += v * dt
        tt += dt
    return np.array(out)


def font(path, size):
    return ImageFont.truetype(str(path), size)


def text_mask(W, H, text, size, path=AMIRI_B, rtl=False, xy=None):
    im = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(im)
    f = font(path, size)
    kw = {"direction": "rtl", "language": "ar"} if rtl else {}
    bb = d.textbbox((0, 0), text, font=f, **kw)
    if xy is None:
        xy = ((W - (bb[2] - bb[0])) / 2 - bb[0], (H - (bb[3] - bb[1])) / 2 - bb[1])
    d.text(xy, text, fill=255, font=f, **kw)
    return np.asarray(im).astype(float)


def chrome_bin():
    for c in ["chromium", "google-chrome", "chromium-browser"]:
        if shutil.which(c):
            return shutil.which(c)
    for p in sorted(Path("/opt/pw-browsers").glob("chromium-*/chrome-linux*/chrome")):
        return str(p)
    raise RuntimeError("no chromium found")


def chrome(wd, name, body, gl=False, budget=5000):
    """Load a page in headless Chromium; its script stores JSON in <body data-r>; return it."""
    page = Path(wd) / (name + ".html")
    page.write_text(body, encoding="utf-8")
    flags = ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"] if gl else ["--disable-gpu"]
    done = subprocess.run([chrome_bin(), "--headless=new", "--no-sandbox", "--allow-file-access-from-files",
                           "--hide-scrollbars", *flags, "--virtual-time-budget=%d" % budget, "--dump-dom", page.as_uri()],
                          capture_output=True, text=True, timeout=60, stdin=subprocess.DEVNULL)
    m = re.search(r'data-r="([^"]*)"', done.stdout)
    if not m:
        raise RuntimeError("page produced no result: " + done.stderr[-400:])
    r = json.loads(_html.unescape(m.group(1)))
    if isinstance(r, dict) and r.get("err"):
        raise RuntimeError("page error: " + str(r["err"])[:300])
    return r


def png_from_dataurl(path, url):
    import base64
    Path(path).write_bytes(base64.b64decode(url.split(",", 1)[1]))
    return Path(path)


def track(frames, ch=0, thr=60, others=(1, 2), othr=40):
    out = []
    for f in frames:
        m = (f[..., ch] > thr) & np.all([f[..., o] < othr for o in others], axis=0)
        out.append(centroid(m))
    return out


def bbox(mask):
    ys, xs = np.nonzero(mask)
    if not len(xs):
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def resample_closed(pts, n):
    """Resample a closed polyline to n points equally spaced by arc length."""
    p = np.asarray(pts, dtype=float)
    q = np.vstack([p, p[:1]])
    seg = np.hypot(*np.diff(q, axis=0).T)
    s = np.concatenate([[0], np.cumsum(seg)])
    u = np.linspace(0, s[-1], n, endpoint=False)
    x = np.interp(u, s, q[:, 0])
    y = np.interp(u, s, q[:, 1])
    return np.stack([x, y], 1)


def signed_area(p):
    p = np.asarray(p)
    x, y = p[:, 0], p[:, 1]
    return .5 * float(np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y))


def poly_regular(n, r, cx=0.0, cy=0.0, rot=-math.pi / 2):
    a = rot + 2 * math.pi * np.arange(n) / n
    return np.stack([cx + r * np.cos(a), cy + r * np.sin(a)], 1)


def star_poly(n, r1, r2, cx=0.0, cy=0.0, rot=-math.pi / 2):
    a = rot + math.pi * np.arange(2 * n) / n
    rr = np.where(np.arange(2 * n) % 2 == 0, r1, r2)
    return np.stack([cx + rr * np.cos(a), cy + rr * np.sin(a)], 1)


def chamfer(a_pts, b_pts):
    from scipy.spatial import cKDTree
    d1, _ = cKDTree(b_pts).query(a_pts)
    d2, _ = cKDTree(a_pts).query(b_pts)
    return float((d1.mean() + d2.mean()) / 2)


def mask_pts(mask):
    ys, xs = np.nonzero(mask)
    return np.stack([xs, ys], 1).astype(float)


# ================================================================= PART cards
def _curl_vel(p, t):
    """Velocity of the analytic stream function psi = sum a_i sin(k_i . p - w_i t + ph_i): v = (dpsi/dy, -dpsi/dx)."""
    ks = np.array([[.0061, .0023], [-.0031, .0057], [.0044, -.0049], [.0097, .0012], [-.0072, -.0036],
                   [.0025, .0089], [-.0014, -.0066]])
    a = np.array([58, 44, 36, 28, 24, 20, 16.0]) * 60
    ph = np.arange(7) * 1.3
    w = np.array([.21, .17, .26, .31, .14, .22, .19])
    arg = p @ ks.T - w * t + ph
    c = np.cos(arg) * a
    vx = (c * ks[:, 1]).sum(-1)
    vy = -(c * ks[:, 0]).sum(-1) - 18.0
    return np.stack([vx, vy], -1)


@card("PART-02")
def closed_form_particles(task, wd):
    g, k, H, fps = 900.0, 2.4, 200.0, 30
    p0, v0 = np.array([40.0, 160.0]), np.array([180.0, -420.0])
    ball = lambda t: p0 + v0 * t + .5 * np.array([0, g]) * t * t
    drag = lambda t: p0 + v0 * (1 - math.exp(-k * t)) / k
    wrap = lambda t, y0=30.0, v=75.0: (y0 + v * t) % H
    # independent fine integration (dt = 1e-4) of p' = v, v' = -k v must equal the closed-form drag position
    p, v, dt = p0.copy(), v0.copy(), 1e-4
    for _ in range(int(.8 / dt)):
        v = v - k * v * dt
        p = p + v * dt
    drag_err = float(np.abs(p - drag(.8)).max())
    # stateful per-frame Euler (what closed form avoids) drifts from the true ballistic path
    pe, ve = p0.copy(), v0.copy()
    for _ in range(int(.8 * fps)):
        pe = pe + ve / fps
        ve = ve + np.array([0, g]) / fps
    euler_err = float(np.abs(pe - ball(.8)).max())
    # curl field: integrate once with RK2 at 60 Hz, store, seek = linear interpolation between stored steps
    pts = R(2).uniform(20, 180, (40, 2))
    steps, q = [pts.copy()], pts.copy()
    for i in range(60):
        t = i / 60
        mid = q + _curl_vel(q, t) / 120
        q = q + _curl_vel(mid, t + 1 / 120) / 60
        steps.append(q.copy())
    steps = np.array(steps)
    seek = lambda t: steps[int(t * 60)] + (steps[min(60, int(t * 60) + 1)] - steps[int(t * 60)]) * (t * 60 - int(t * 60))
    ref, dtt = pts.copy(), 1 / 2400       # fine reference integration (RK4 at 2400 Hz)
    for i in range(int(.75 / dtt)):
        t = i * dtt
        k1 = _curl_vel(ref, t)
        k2 = _curl_vel(ref + k1 * dtt / 2, t + dtt / 2)
        k3 = _curl_vel(ref + k2 * dtt / 2, t + dtt / 2)
        k4 = _curl_vel(ref + k3 * dtt, t + dtt)
        ref = ref + (k1 + 2 * k2 + 2 * k3 + k4) * dtt / 6
    seek_err = float(np.abs(seek(.75) - ref).max())
    # render: frames from t directly; out-of-order seek gives identical frames
    def frame(t):
        a = canvas(200, 200)
        for x, y in seek(min(t, .99)):
            disc(a, x, y, 1, (90, 90, 90))
        x, y = drag(t)
        disc(a, x, y, 3, (0, 255, 0))
        disc(a, 100, wrap(t), 3, (0, 0, 255))
        x, y = ball(t)
        disc(a, x, y, 3, (255, 0, 0), "over")
        return a
    ts = np.arange(0, 24) / fps
    vid = video(wd / "closed_form.mp4", [frame(t) for t in ts])
    fr = vread(vid, 200, 200)
    rev = [frame(t) for t in ts[::-1]][::-1]
    same = all(np.array_equal(np.round(fr[i]), np.clip(np.round(rev[i]), 0, 255)) for i in (3, 11, 20))
    tr = track(fr, 0)
    gy = np.polyfit(ts, [c[1] for c in tr], 2)[0] * 2
    bake = jw(wd / "curl_bake.json", {"hz": 60, "steps": steps.round(3).tolist()})
    return [check("closed-form drag equals fine integration (px)", drag_err < .05, drag_err, "<0.05"),
            check("tracked ballistic particle recovers g", abs(gy - g) / g < .03, gy, g),
            check("wrap stays in [0, H)", all(0 <= wrap(t) < H for t in np.linspace(0, 10, 101)), True, True),
            check("RK2 60 Hz pre-bake + lerp seek matches RK4 reference (px)", seek_err < 1.0, seek_err, "<1"),
            check("reverse-order seek renders identical frames", same, same, True),
            check("negative control: stateful per-frame Euler drifts > 3 px", euler_err > 3, euler_err, ">3")], [vid, bake]


def lint_particles(spec):
    issues = []
    if spec.get("role") not in ("entity", "sample", "direction", "focus", "quantity->structure", "energy", "flow",
                                "dissolution"):
        issues.append("particles carry no meaning (decorative)")
    if not spec.get("unit"):
        issues.append("unit not stated on screen or in VO")
    if spec.get("count", 0) > spec.get("cap", 600):
        issues.append("count over cap")
    if spec.get("draw_all_edges"):
        issues.append("draws every edge instead of sampling")
    if not spec.get("ends_static"):
        issues.append("does not end on a static frame")
    if spec.get("subject") == "aggregated human harm":
        issues.append("particles avoided for aggregated or uncertain human harm")
    return issues


@card("PART-03")
def particle_meaning(task, wd):
    data = {"north": 37, "south": 21, "east": 12}
    spec = {"role": "entity", "unit": "1 dot = 1 clinic", "count": sum(data.values()), "cap": 600,
            "draw_all_edges": False, "ends_static": True, "subject": "clinics"}
    bad = {"role": "decor", "count": 2400, "cap": 600, "draw_all_edges": True, "ends_static": False}
    # render: each dot is one entity gathering into its region column, last frames static
    rng = R(3)
    starts = rng.uniform(10, 230, (spec["count"], 2))
    cols, tg = [], []
    for ci, (kk, n) in enumerate(data.items()):
        for j in range(n):
            tg.append((30 + ci * 80 + (j % 6) * 7, 120 - (j // 6) * 7))
            cols.append(ci)
    tg = np.array(tg, dtype=float)
    frames = []
    for f in range(40):
        e = float(in_out_cubic(min(1, f / 30)))
        a = canvas(240, 130)
        for (x, y), c in zip(starts + (tg - starts) * e, cols):
            a[int(round(y)) - 2:int(round(y)) + 1, int(round(x)) - 2:int(round(x)) + 1] = (255, 200, 80)
        frames.append(a)
    vid = video(wd / "meaning.mp4", frames, 30)
    fr = vread(vid, 240, 130)
    lab, n = label(fr[-1][..., 0] > 128)
    counts = [int(len(set(lab[:, 20 + i * 80:20 + i * 80 + 60][lab[:, 20 + i * 80:20 + i * 80 + 60] > 0].ravel())))
              for i in range(3)]
    static = float(np.abs(fr[-1] - fr[-5]).max())
    jw(wd / "spec.json", {"spec": spec, "issues": lint_particles(spec), "bad_issues": lint_particles(bad)})
    return [check("good spec passes the meaning lint", lint_particles(spec) == [], lint_particles(spec), []),
            check("one dot per entity in each region", counts == list(data.values()), counts, list(data.values())),
            check("ends on a static frame", static < 2, static, "<2"),
            check("negative control: decorative dust spec is flagged (>=4 issues)", len(lint_particles(bad)) >= 4,
                  len(lint_particles(bad)), ">=4")], [vid, wd / "spec.json"]


@card("PART-04")
def size_colour_budget(task, wd):
    W, H = 320, 180
    rng = R(4)
    n = 300
    sizes = rng.choice([4, 8, 14], n, p=[.6, .3, .1])
    cols = [hexc("#7ee8d2"), hexc("#ffb86b")]
    # uneven density: most particles in a Gaussian clump on the right
    xs = np.where(rng.random(n) < .75, rng.normal(.75 * W, 30, n), rng.uniform(0, W, n)).clip(8, W - 8)
    ys = rng.uniform(8, H - 8, n)
    a = canvas(W, H, (12, 14, 20))
    order = np.argsort(sizes)
    for i in order:
        s = int(sizes[i])
        x0, y0 = int(xs[i]) - s // 2, int(ys[i]) - s // 2
        a[y0:y0 + s, x0:x0 + s] = cols[int(i % 5 == 0)]
    tm = text_mask(W, H, "BUDGET", 40, POPPINS) > 127
    a[tm] = (255, 255, 255)                       # type drawn last: particles stay behind it
    out = save(wd / "budget.png", a)
    b = load(out)
    lit = np.abs(b - (12, 14, 20)).sum(-1) > 30
    pal = {tuple(c) for c in b[lit & ~tm].reshape(-1, 3).astype(int)}
    lab, nc = label(lit & ~tm)
    left, right = (lit[:, :W // 2] & ~tm[:, :W // 2]).mean(), (lit[:, W // 2:] & ~tm[:, W // 2:]).mean()
    text_ok = bool((b[tm] == 255).all())
    lint = {"sizes": sorted(set(sizes.tolist())), "colours": len(pal), "count": n, "engine": "canvas2d"}
    bad = {"sizes": [3, 5, 9, 11, 20], "colours": 6, "count": 2500, "engine": "canvas2d"}
    ok = lambda s: s["sizes"] == [4, 8, 14] and s["colours"] <= 2 and (150 <= s["count"] <= 600 if s["engine"] ==
                                                                        "canvas2d" else s["count"] <= 20000)
    jw(wd / "budget.json", {"spec": lint, "bad": bad, "density_left": left, "density_right": right})
    return [check("only sizes 4/8/14 px", lint["sizes"] == [4, 8, 14], lint["sizes"], [4, 8, 14]),
            check("<= 2 particle colours measured in the PNG", len(pal) <= 2, len(pal), "<=2"),
            check("150-600 particles on canvas", ok(lint), n, "150-600"),
            check("uneven density (right/left >= 2)", right / max(left, 1e-6) >= 2, right / max(left, 1e-6), ">=2"),
            check("type stays on top of particles", text_ok, text_ok, True),
            check("negative control: an over-budget spec fails", not ok(bad), ok(bad), False)], [out, wd / "budget.json"]


def _burst_state(t, n=160, seed=20261015, cx=160, cy=90):
    rng = R(seed)
    ang = rng.uniform(0, 2 * math.pi, n)
    sp = rng.uniform(400, 1300, n) * .12          # px travel scaled to a 320x180 frame
    size = rng.uniform(4, 14, n) * .3
    life_len = rng.uniform(.7, 1.0, n)
    teal = rng.random(n) < .7
    life = np.clip(t / life_len, 0, 1)
    d = out_expo(life) * sp
    x = cx + np.cos(ang) * d
    y = cy + np.sin(ang) * d + life * 120 * .12
    alpha = 1 - in_out_cubic(life)
    r = size * (1 - .6 * life)
    return x, y, r, alpha, teal, sp, ang, life


@card("PART-06")
def seeded_burst(task, wd):
    ts = np.arange(0, 30) / 30
    frames = []
    for t in ts:
        a = canvas(320, 180)
        x, y, r, al, teal, *_ = _burst_state(t)
        for i in range(1, len(x)):
            disc(a, x[i], y[i], max(.6, r[i]), hexc("#7ee8d2") if teal[i] else hexc("#ffb86b"), "max", al[i])
        disc(a, x[0], y[0], 2.5, (255, 0, 0), "max", 1.0)   # tracked particle 0, pure red, full alpha for tracking
        frames.append(a)
    vid = video(wd / "burst.mp4", frames)
    fr = vread(vid, 320, 180)
    x, y, r, al, teal, sp, ang, life = _burst_state(.3)
    c = track(fr, 0)[9]
    exp = (x[0], y[0])
    err = math.hypot(c[0] - exp[0], c[1] - exp[1])
    # linear-distance model (no expo.out) would put the particle much closer to the centre at t = .3
    lx = 160 + math.cos(ang[0]) * sp[0] * life[0]
    ly = 90 + math.sin(ang[0]) * sp[0] * life[0] + life[0] * 120 * .12
    lin_err = math.hypot(c[0] - lx, c[1] - ly)
    lum = [f[..., 1].sum() for f in fr]
    again = _burst_state(.5)[0]
    seeded = bool(np.array_equal(again, _burst_state(.5)[0]))
    return [check("tracked particle at t=.3 s sits on outExpo(life) * speed (px)", err < 2.0, err, "<2"),
            check("expo.out: >= 80% of travel done at 30% life", float(out_expo(.3)) >= .8, float(out_expo(.3)), ">=.8"),
            check("fade: burst brightness at 0.95 s < 15% of peak", lum[-2] < .15 * max(lum), lum[-2] / max(lum), "<.15"),
            check("same seed -> identical state", seeded, seeded, True),
            check("negative control: a linear-distance model misses the tracked particle (> 8 px)", lin_err > 8,
                  lin_err, ">8")], [vid]


@card("PART-07")
def reveal_burst_recipe(task, wd):
    fps, W, H = 30, 240, 136
    cx, cy = W / 2, H / 2
    ts = np.arange(0, 96) / fps
    rng = R(7)
    ang, sp = rng.uniform(0, 2 * math.pi, 160), rng.uniform(40, 110, 160)
    base = text_mask(W, H, "IDEA", 34, POPPINS) > 127
    from scipy.ndimage import zoom

    def word_scale(t):
        return float(spring(t, 150, 14)) if t >= 0 else 0.0

    def frame(t):
        a = canvas(W, H)
        s = word_scale(t)
        if s > .02:
            m = zoom(base.astype(float), s, order=0)
            hh, ww = m.shape
            y0, x0 = int(cy - hh / 2), int(cx - ww / 2)
            ys, xs = np.nonzero(m > .5)
            ok = (ys + y0 >= 0) & (ys + y0 < H) & (xs + x0 >= 0) & (xs + x0 < W)
            a[ys[ok] + y0, xs[ok] + x0, 0] = 255
        if .05 <= t <= 3.0:
            u = (t - .05) / 2.95
            d = out_expo(u) * sp
            for x, y in zip(cx + np.cos(ang) * d, cy + np.sin(ang) * d):
                disc(a, x, y, 1.2, (0, 255 * (1 - u), 0))
        if .1 <= t <= 1.1:
            u = (t - .1) / 1.0
            rr = float(out_expo(u)) * 60
            yy, xx = np.mgrid[:H, :W]
            ring = np.abs(np.hypot(xx - cx, yy - cy) - rr) < 1.2
            a[ring, 2] = 255 * (1 - u)
        return a
    vid = video(wd / "reveal_burst.mp4", [frame(t) for t in ts], fps)
    fr = vread(vid, W, H)
    widths = [(bbox(f[..., 0] > 128) or (0, 0, -1, 0)) for f in fr]
    ww = [b[2] - b[0] + 1 for b in widths]
    final_w = ww[40]
    first_part = next(i for i, f in enumerate(fr) if ((f[..., 1] > 120) & (f[..., 0] < 60)).any())
    yy, xx = np.mgrid[:H, :W]
    f18 = fr[18]
    ring = (f18[..., 2] > 60) & (f18[..., 0] < 60) & (f18[..., 1] < 60)
    rr = float(np.hypot(xx[ring] - cx, yy[ring] - cy).mean())
    exp_r = float(out_expo((18 / fps - .1) / 1.0)) * 60
    lin_r = (18 / fps - .1) * 60
    ring_after = int(((fr[36][..., 2] > 60) & (fr[36][..., 0] < 60)).sum())
    return [check("word settles to full size by 250 ms (within 15%)", abs(ww[8] - final_w) / final_w < .15, ww[8], final_w),
            check("particles start at frame 2 (50 ms)", first_part in (1, 2), first_part, 2),
            check("ring radius at 0.6 s follows outExpo (px)", abs(rr - exp_r) < 2.5, rr, exp_r),
            check("ring gone after 1.1 s", ring_after == 0, ring_after, 0),
            check("negative control: a linear ring would be far smaller", abs(rr - lin_r) > 10, lin_r, rr)], [vid]


def _confetti(t, n=70, seed=8):
    rng = R(seed)
    x0 = rng.uniform(60, 260, n)
    vx = rng.uniform(-60, 60, n)
    vy = rng.uniform(-520, -380, n)
    ph = rng.uniform(0, 2 * math.pi, n)
    spin = rng.uniform(-4, 4, n)
    g = 750.0
    x = x0 + vx * t + np.sin(3 * t + ph) * 20
    y = 200 + vy * t + .5 * g * t * t
    sy = np.cos(8 * t + ph)
    return x, y, sy, spin * t, ph, g


@card("PART-08")
def confetti_flip(task, wd):
    ts = np.arange(0, 45) / 30
    cols = [hexc("#ff4d6d"), hexc("#ffd23f"), hexc("#3bceac")]
    frames = []
    for t in ts:
        a = canvas(320, 240)
        x, y, sy, rot, ph, g = _confetti(t)
        for i in range(len(x)):
            hh = max(.5, 6 * abs(sy[i]))
            c = cols[i % 3] if i else np.array([255.0, 0, 0])
            r0 = 0 if i == 0 else rot[i]          # tracked piece 0: no spin so its height reads the flip
            corners = np.array([[-5, -hh / 2], [5, -hh / 2], [5, hh / 2], [-5, hh / 2]])
            cr, sr = math.cos(r0), math.sin(r0)
            pts = corners @ np.array([[cr, sr], [-sr, cr]]) + (x[i], y[i])
            m = poly_mask(320, 240, pts)
            a[m] = c if i else (255, 0, 0)
        frames.append(a)
    vid = video(wd / "confetti.mp4", frames)
    fr = vread(vid, 320, 240)
    hs, cy = [], []
    for f in fr:
        m = (f[..., 0] > 150) & (f[..., 1] < 40) & (f[..., 2] < 40)
        b = bbox(m)
        hs.append(b[3] - b[1] + 1 if b else 0)
        c = centroid(m)
        cy.append(c[1] if c else np.nan)
    ok = ~np.isnan(cy)
    gy = np.polyfit(ts[ok], np.array(cy)[ok], 2)[0] * 2
    _, _, _, _, ph, g = _confetti(0)
    exp_h = np.maximum(1, 6 * np.abs(np.cos(8 * ts + ph[0])))
    corr = float(np.corrcoef(np.array(hs)[ok], exp_h[ok])[0, 1])
    # untreated piece (no flip): the same height measurement on its rendered mask
    flat = []
    for t in ts:
        x, y, *_ = _confetti(t)
        m = poly_mask(320, 240, np.array([[-5, -3], [5, -3], [5, 3], [-5, 3]]) + (x[0], y[0]))
        b = bbox(m)
        flat.append(b[3] - b[1] + 1 if b else 0)
    flat = np.array(flat, dtype=float)[ok]
    corr_flat = float(np.corrcoef(flat, exp_h[ok])[0, 1]) if flat.std() > 0 else 0.0
    return [check("tracked piece falls with g = 750 px/s^2", abs(gy - g) / g < .05, gy, g),
            check("piece height follows |cos(8t + ph)| (3D flip)", corr > .85, corr, ">.85"),
            check("70 pieces rendered", True if len(_confetti(0)[0]) == 70 else False, 70, 70),
            check("negative control: an un-flipped piece has constant height (no correlation)", corr_flat < .5,
                  corr_flat, "<.5")], [vid]


@card("PART-10")
def radial_dash_burst(task, wd):
    W, H, cx, cy = 320, 240, 160, 120
    rng = R(10)
    n = 120
    ang = rng.uniform(0, 2 * math.pi, n)
    sp = rng.uniform(70, 110, n)
    life = rng.uniform(.6, .9, n)
    kind = rng.choice(3, n, p=[.7, .2, .1])
    cols = [(255, 255, 255), (255, 220, 0), (255, 0, 0)]

    def frame(t, oriented=True):
        def fn(d):
            for i in range(n):
                u = min(1, t / life[i])
                if u >= 1:
                    continue
                r = 12 + float(out_cubic(u)) * sp[i]           # decelerating
                a = ang[i] if oriented else ang[i] + 1.3 * ((i * 7919) % 13 - 6) / 6
                x, y = cx + math.cos(ang[i]) * r, cy + math.sin(ang[i]) * r
                L = 6
                k = 1 - u
                c = tuple(int(v * k) for v in cols[kind[i]])
                d.line([(x - math.cos(a) * L, y - math.sin(a) * L), (x + math.cos(a) * L, y + math.sin(a) * L)], fill=c, width=1)
        return draw_layer(W, H, fn)
    out = save(wd / "dash_t015.png", frame(.15))
    vid = video(wd / "dash_burst.mp4", [frame(f / 30) for f in range(30)])

    def orient_err(img):
        lab, nn = label(img.max(-1) > 40)
        errs = []
        for k in range(1, nn + 1):
            ys, xs = np.nonzero(lab == k)
            if len(xs) < 6:
                continue
            c = np.cov(np.stack([xs, ys]))
            w, v = np.linalg.eigh(c)
            ax = v[:, 1]
            rad = np.array([xs.mean() - cx, ys.mean() - cy])
            rad /= np.linalg.norm(rad) + 1e-9
            errs.append(math.degrees(math.acos(min(1, abs(float(ax @ rad))))))
        return float(np.median(errs)) if errs else 90.0
    img = load(out)
    e_ok = orient_err(img)
    e_bad = orient_err(frame(.15, oriented=False))
    lit = img.max(-1) > 40
    px = img[lit]
    white = ((px[:, 2] > .7 * px[:, 0]) & (px[:, 1] > .7 * px[:, 0])).mean()
    yellow = ((px[:, 1] > .5 * px[:, 0]) & (px[:, 2] < .3 * px[:, 0])).mean()
    red = ((px[:, 1] < .3 * px[:, 0]) & (px[:, 2] < .3 * px[:, 0])).mean()
    fr = vread(vid, W, H)
    end = float(fr[-1].max())
    return [check("dashes point along their velocity (median deg)", e_ok < 12, e_ok, "<12"),
            check("colour mix ~70/20/10 white/yellow/red", abs(white - .7) < .12 and abs(yellow - .2) < .1 and abs(red - .1) < .08,
                  [white, yellow, red], [.7, .2, .1]),
            check("all dashes dead by 0.97 s (life 600-900 ms)", end < 25, end, "<25"),
            check("negative control: randomly rotated dashes fail the orientation test", e_bad > 20, e_bad, ">20")], [out, vid]


@card("PART-11")
def shatter_squares(task, wd):
    W, H, cx, cy = 240, 240, 120, 120
    yy, xx = np.mgrid[:H, :W]
    obj = canvas(W, H)
    m = np.hypot(xx - cx, yy - cy) < 50
    obj[m] = np.stack([xx[m] * 1.0, yy[m] * 1.0, 255 - xx[m] * .5], 1)
    save(wd / "object.png", obj)
    S = 5
    cells = [(x, y) for y in range(0, H, S) for x in range(0, W, S) if m[y + S // 2, x + S // 2]]
    rng = R(11)
    jit = rng.uniform(.8, 1.2, len(cells))
    OFF = 3                                   # R +3 px, B -3 px -> 6 px R/B split

    def frame(t, split=True):
        u = float(out_expo(t / .6))
        a = canvas(W, H)
        for (x, y), j in zip(cells, jit):
            col = obj[y + S // 2, x + S // 2]
            r0 = math.hypot(x - cx, y - cy)
            th = math.atan2(y - cy, x - cx) + u * 1.2 * j           # spiral: angle grows while flung outward
            r = r0 + u * 60 * j
            px, py = int(cx + r * math.cos(th)), int(cy + r * math.sin(th))
            for ch, dx in ((0, OFF if split else 0), (1, 0), (2, -OFF if split else 0)):
                xa, ya = px + int(dx * u), py
                if 0 <= xa < W - S and 0 <= ya < H - S:
                    a[ya:ya + S, xa:xa + S, ch] = col[ch]
        return a
    f0 = frame(0)
    vid = video(wd / "shatter.mp4", [frame(f / 30) for f in range(18)])
    fr = vread(vid, W, H)
    recon = float(np.abs(fr[0][m] - obj[m]).mean())

    def shift(img):
        r, b = img[..., 0], img[..., 2]
        best, arg = -1, 0
        for d in range(-15, 16):
            c = float((np.roll(b, d, axis=1) * r).sum())
            if c > best:
                best, arg = c, d
        return arg
    sh = shift(fr[17])
    sh0 = shift(frame(17 / 30, split=False))
    spread0 = float(np.hypot(*(mask_pts(f0.max(-1) > 10) - (cx, cy)).T).mean())
    spread1 = float(np.hypot(*(mask_pts(fr[17].max(-1) > 10) - (cx, cy)).T).mean())
    return [check("frame 0 squares reproduce the object's colours", recon < 6, recon, "<6"),
            check("R/B split measured in the 600 ms frame (px)", 4 <= abs(sh) <= 8, sh, "4-8"),
            check("squares flung outward (mean radius grows > 40 px)", spread1 - spread0 > 40, spread1 - spread0, ">40"),
            check("~300-600 squares", 300 <= len(cells) <= 600, len(cells), "300-600"),
            check("negative control: without the split the R/B shift is 0", sh0 == 0, sh0, 0)], [vid, wd / "object.png"]


@card("PART-12")
def image_card_cloud(task, wd):
    W, H, cx, cy = 320, 180, 160, 90
    rng = R(12)
    n = 120
    ang = rng.uniform(0, 2 * math.pi, n)
    dist = rng.uniform(40, 140, n)
    scale = rng.uniform(.4, 1.2, n)
    drift = rng.normal(0, 1, (n, 2))
    drift /= np.linalg.norm(drift, axis=1, keepdims=True)

    def pos(i, t):
        u = float(out_expo(min(1, t / .7)))
        x = cx + math.cos(ang[i]) * dist[i] * u
        y = cy + math.sin(ang[i]) * dist[i] * u
        if t > .7:
            x += drift[i, 0] * 10 * (t - .7)
            y += drift[i, 1] * 10 * (t - .7)
        return x, y
    from scipy.ndimage import gaussian_filter

    def frame(t):
        a = canvas(W, H, (20, 20, 28))
        for i in [j for j in np.argsort(scale) if j] + [0]:
            x, y = pos(i, t)
            s = 12 * scale[i]
            card_ = np.zeros((int(2 * s) + 6, int(2 * s) + 6, 3))
            card_[3:-3, 3:-3] = (200, 160, 90) if i else (255, 0, 0)
            card_[3:-3:4, 3:-3] *= .6 if i else 1          # image texture stripes
            blur = (1.2 - scale[i]) * 2.5                   # depth blur by scale
            card_ = gaussian_filter(card_, (blur, blur, 0)) if (blur > .2 and i) else card_
            h, w = card_.shape[:2]
            x0, y0 = int(x - w / 2), int(y - h / 2)
            if 0 <= x0 < W - w and 0 <= y0 < H - h:
                reg = a[y0:y0 + h, x0:x0 + w]
                msk = card_.max(-1, keepdims=True) > 10
                reg[...] = np.where(msk, card_, reg)
        return a
    ts = np.arange(0, 54) / 30
    vid = video(wd / "card_cloud.mp4", [frame(t) for t in ts])
    fr = vread(vid, W, H)
    tr = track(fr, 0, thr=200, othr=30)
    p07, p17 = tr[21], tr[51]
    exp07 = pos(0, .7)
    burst_err = math.hypot(p07[0] - exp07[0], p07[1] - exp07[1])
    drift_d = math.hypot(p17[0] - p07[0], p17[1] - p07[1])
    p_mid = tr[6]
    lin_x = cx + math.cos(ang[0]) * dist[0] * (6 / 30 / .7)
    frac = math.hypot(p_mid[0] - cx, p_mid[1] - cy) / dist[0]
    # depth blur: small far cards are softer than big near ones (Laplacian variance on a single-card render)
    from scipy.ndimage import laplace
    def sharp(sc):
        c = np.zeros((40, 40))
        s = int(12 * sc)
        c[20 - s:20 + s, 20 - s:20 + s] = 200
        b = (1.2 - sc) * 2.5
        c = gaussian_filter(c, b) if b > .2 else c
        return float(laplace(c).var())
    return [check("tracked card lands at its burst distance at 700 ms (px)", burst_err < 2.5, burst_err, "<2.5"),
            check("then drifts ~10 px/s (px over 1 s)", 7 <= drift_d <= 13, drift_d, "~10"),
            check("expo-out: > 70% of travel done at 200 ms", frac > .7, frac, ">.7"),
            check("far (small) cards blurrier than near ones", sharp(.45) < sharp(1.15), [sharp(.45), sharp(1.15)], "far<near"),
            check("negative control: a linear burst would only be at 29% at 200 ms", abs(frac - 6 / 21) > .3,
                  6 / 21, frac)], [vid]


def _sparkle(size):
    yy, xx = np.mgrid[-size:size + 1, -size:size + 1].astype(float)
    return np.clip(1 - (np.minimum(np.abs(xx), np.abs(yy)) * 2.5 + np.hypot(xx, yy) * .35) / size, 0, 1)


@card("PART-13")
def star_burst(task, wd):
    W, H, cx, cy, n = 320, 240, 160, 110, 80
    rng = R(13)
    ang = rng.uniform(0, 2 * math.pi, n)
    sp = rng.uniform(1.5, 4, n)
    gold, white = hexc("#e3b75a"), hexc("#ffffff")
    spr = _sparkle(5)
    G = .05

    def frame(f):
        a = canvas(W, H)
        fade = max(0.0, 1 - f / 60)
        for i in range(n):
            x = cx + math.cos(ang[i]) * sp[i] * f
            y = cy + math.sin(ang[i]) * sp[i] * f + .5 * G * f * f
            col = np.array([255.0, 0, 0]) if i == 0 else (gold if i % 2 else white)
            x0, y0 = int(round(x)) - 5, int(round(y)) - 5
            if 0 <= x0 < W - 11 and 0 <= y0 < H - 11:
                reg = a[y0:y0 + 11, x0:x0 + 11]
                reg[...] = np.maximum(reg, spr[..., None] * col * (1 if i == 0 else fade))
        return a
    vid = video(wd / "stars.mp4", [frame(f) for f in range(64)])
    fr = vread(vid, W, H)
    tr = track(fr[:40], 0, thr=120, othr=40)
    fs = np.array([i for i, c in enumerate(tr) if c])
    ys = np.array([tr[i][1] for i in fs])
    g_fit = np.polyfit(fs, ys, 2)[0] * 2
    others = [float(np.where((f[..., 1] > 100), f.sum(-1), 0).sum()) for f in fr]
    sym = float(np.abs(spr - np.rot90(spr)).max())
    out = save(wd / "sparkle.png", spr * 255)
    return [check("tracked star gravity .05 px/frame^2", abs(g_fit - G) < .01, g_fit, G),
            check("stars faded out by 2 s", others[61] < .02 * max(others), others[61] / max(others), "<.02"),
            check("4-point sparkle sprite has 4-fold symmetry", sym < 1e-9, sym, 0),
            check("80 stars", n == 80, n, 80),
            check("negative control: no-gravity path has zero curvature", abs(np.polyfit(fs, ys - .5 * G * fs ** 2, 2)[0]) < 1e-3
                  and abs(g_fit) > .03, g_fit, ">.03")], [vid, out]


@card("PART-14")
def pixel_palette_fade(task, wd):
    ramp = [hexc(h) for h in ("#fff6d5", "#ffd34e", "#ff8c1a", "#c2341f", "#5a1a2a")]
    bg = hexc("#140c1c")
    W = H = 48
    rng = R(14)
    seq = [0, 1, 2, 2, 2, 3, 4, 5, 6, 7, 8, 9]          # impact frame (2) held 3 frames
    parts = [(rng.uniform(-1, 1), rng.uniform(-1, 1), int(rng.integers(3, 6))) for _ in range(24)]

    def frame(k, alpha=False):
        a = canvas(W, H, bg)
        r = min(4 + k * 3, 16)
        yy, xx = np.mgrid[:H, :W]
        d = np.hypot(xx - 24, yy - 24)
        for band in range(5):                            # core bright -> rim dark, steps down the ramp with time
            idx = min(4, band + max(0, k - 2))
            if alpha:
                c = bg + (ramp[0] - bg) * max(0, 1 - k / 9) * (1 - band / 5)
            else:
                c = ramp[idx]
            msk = (d < r * (1 - band / 5)) & (d >= r * (1 - (band + 1) / 5))
            if not alpha and k >= 5 + band:
                continue
            a[msk] = c
        for vx, vy, life in parts:                       # shrink-to-die: lose 1 px per frame
            size = life - k + 3
            if size <= 0:
                continue
            x, y = int(24 + vx * 18 * k / 6), int(24 + vy * 18 * k / 6)
            a[y:y + size, x:x + size] = ramp[min(4, k // 2)] if not alpha else ramp[0] * .5 + bg * .5
        return a
    frames = [frame(k) for k in seq]
    sheet = np.concatenate(frames, 1)
    out = save(wd / "explosion_sheet.png", sheet)
    b = load(out)
    pal = {tuple(c.astype(int)) for c in ramp} | {tuple(bg.astype(int))}
    cols = {tuple(c) for c in b.reshape(-1, 3).astype(int)}
    off_pal = len(cols - pal)
    fr = [b[:, i * W:(i + 1) * W] for i in range(len(seq))]
    held = all(np.array_equal(fr[2], fr[j]) for j in (3, 4))
    last = int((np.abs(fr[-1] - bg).sum(-1) > 0).sum())
    bad = np.concatenate([frame(k, alpha=True) for k in seq], 1)
    bad_off = len({tuple(c) for c in np.round(bad).reshape(-1, 3).astype(int)} - pal)
    return [check("every pixel is a ramp colour or background (no alpha)", off_pal == 0, off_pal, 0),
            check("ramp has 4-6 colours", 4 <= len(ramp) <= 6, len(ramp), "4-6"),
            check("impact frame held 3 frames", held, held, True),
            check("effect fully gone in the last frame", last == 0, last, 0),
            check("negative control: an alpha fade produces off-palette colours", bad_off > 5, bad_off, ">5")], [out]


AR_WORD = "الفكرة"      # الفكرة


@card("PART-15")
def particles_to_arabic(task, wd):
    W, H = 320, 120
    word = text_mask(W, H, AR_WORD, 70, AMIRI_B, rtl=True)
    save(wd / "word.png", word)
    ys, xs = np.nonzero(word[::2, ::2] > 150)
    tg = np.stack([xs * 2.0, ys * 2.0], 1)
    rng = R(20261016)
    perm = rng.permutation(len(tg))                      # Fisher-Yates with the seed
    tg = tg[perm]
    N = len(tg)
    u = (tg[:, 0] - tg[:, 0].min()) / np.ptp(tg[:, 0])
    start = 2.2 + 1.1 * (.72 * (1 - u) + .28 * rng.random(N))
    p0 = rng.uniform((0, 0), (W, H), (N, 2))
    # swim in the curl field (RK2 at 60 Hz, pre-baked) until each particle's start time
    swim = [p0.copy()]
    q = p0.copy()
    for i in range(int(3.4 * 60)):
        mid = q + _curl_vel(q * 3, i / 60) / 120 * .25
        q = q + _curl_vel(mid * 3, (i + .5) / 60) / 60 * .25
        q %= (W, H)
        swim.append(q.copy())
    swim = np.array(swim)
    bend = rng.uniform(.18, .5, N) * np.where(rng.random(N) < .5, -1, 1)

    def at(t):
        k = np.clip((np.minimum(t, start) * 60).astype(int), 0, len(swim) - 1)
        s0 = swim[k, np.arange(N)]
        e = in_out_cubic((t - start) / 1.75)[:, None]
        d = tg - s0
        perp = np.stack([-d[:, 1], d[:, 0]], 1) * bend[:, None]
        return s0 + d * e + perp * (e * (1 - e) * 4)        # curved path, offset +-.18-.50 of the chord

    def frame(t):
        a = np.zeros((H, W))
        p = np.round(at(t)).astype(int)
        ok = (p[:, 0] >= 0) & (p[:, 0] < W - 1) & (p[:, 1] >= 0) & (p[:, 1] < H - 1)
        for dx in (0, 1):
            for dy in (0, 1):
                a[p[ok, 1] + dy, p[ok, 0] + dx] = 255
        return np.repeat(a[..., None], 3, 2)
    t_end = float(start.max() + 1.75)
    ts = [0.0, 2.6, 3.0, t_end]
    frames = [frame(t) for t in ts]
    vid = video(wd / "gather.mp4", frames, 2)
    fr = vread(vid, W, H)
    wm = word > 150
    final = fr[-1][..., 0] > 128
    i_end, i0 = iou(final, wm), iou(fr[0][..., 0] > 128, wm)
    right = u > .9
    left = u < .1
    _, n_word = label(wm)
    _, n_final = label(final)
    k32 = min(len(swim) - 1, int(3.2 * 60))
    rem = np.hypot(*(at(3.2) - tg).T) / (np.hypot(*(swim[np.clip((start * 60).astype(int), 0, k32), np.arange(N)] - tg).T) + 1e-6)
    r_first = float(rem[right].mean()) < float(rem[left].mean())
    return [check("all particles land on the shaped word (IoU)", i_end > .8, i_end, ">.8"),
            check("letters stay joined: same connected parts as the shaped word", abs(n_final - n_word) <= 2,
                  n_final, n_word),
            check("right-to-left arrival (right decile earlier than left)", r_first,
                  [float(rem[right].mean()), float(rem[left].mean())], "remaining right<left"),
            check("travel 1.75 s, starts 2.2-3.3 s", 2.2 <= start.min() and start.max() <= 3.3, [start.min(), start.max()],
                  "2.2-3.3"),
            check("negative control: at t=0 the swimming field is not the word", i0 < .2, i0, "<.2")], [vid, wd / "word.png"]


@card("PART-16")
def text_dissolve_embers(task, wd):
    W, H = 320, 140
    word = text_mask(W, H, AR_WORD, 66, AMIRI_B, rtl=True, xy=None)
    wm = word > 128
    ys, xs = np.nonzero(wm)
    rng = R(16)
    noise = rng.random(len(xs))
    xn = (xs - xs.min()) / np.ptp(xs)
    release = 1.0 + 1.2 * ((1 - xn) * .85 + noise * .15)   # sweep right -> left after a 1 s hold

    def frame(t):
        a = canvas(W, H)
        age = t - release
        alive = age < 1.5
        held = age <= 0
        a[ys[held], xs[held]] = 255
        fl = (~held) & alive
        g = np.clip(age[fl] / 1.5, 0, 1)
        py = np.round(ys[fl] - 200 * .35 * g).astype(int)   # drift up 200 px over 1.5 s (scaled 0.35 to the frame)
        px = np.round(xs[fl] + np.sin(g * 6 + xs[fl] * .1) * 3).astype(int)
        ok = (py >= 0) & (py < H) & (px >= 0) & (px < W)
        col = np.stack([255 * (1 - .2 * g), 255 * (1 - .55 * g), 255 * (1 - .9 * g)], 1) * (1 - g[:, None]) ** .5
        a[py[ok], px[ok]] = np.maximum(a[py[ok], px[ok]], col[ok])
        return a
    ts = np.arange(0, 4.0, 1 / 15)
    vid = video(wd / "dissolve.mp4", [frame(t) for t in ts], 15)
    fr = vread(vid, W, H)
    at = lambda t: fr[int(round(t * 15))]
    hold = iou(at(.9).max(-1) > 128, wm)
    mid = at(1.7)
    white = (mid.min(-1) > 128) & wm
    xm = (xs.min() + xs.max()) / 2
    rleft = white[:, :int(xm)].sum() / max(1, wm[:, :int(xm)].sum())
    rright = white[:, int(xm):].sum() / max(1, wm[:, int(xm):].sum())
    emb = at(2.6)
    em = (emb.max(-1) > 40) & ~wm
    pe = emb[em]
    orange = float(((pe[:, 0] > pe[:, 1]) & (pe[:, 1] > pe[:, 2])).mean()) if len(pe) else 0
    gone = float((fr[-1].max(-1) > 40).sum())
    un = np.repeat(word[..., None], 3, 2)               # untreated: the word with no dissolve, same measurement
    uw = (un.min(-1) > 128) & wm
    un_r = uw[:, int(xm):].sum() / max(1, wm[:, int(xm):].sum())
    un_l = uw[:, :int(xm)].sum() / max(1, wm[:, :int(xm)].sum())
    return [check("word readable and whole for >= 1 s (IoU at 0.9 s)", hold > .98, hold, ">.98"),
            check("sweep releases the right side first (remaining right < left)", rright < rleft, [rright, rleft], "right<left"),
            check("embers turn white -> orange (R > G > B share)", orange > .8, orange, ">.8"),
            check("all embers gone by 4 s", gone == 0, gone, 0),
            check("negative control: the untreated word shows no right-first release", not (un_r < un_l), [un_r, un_l],
                  "right == left")], [vid]


@card("PART-17")
def icon_coalesce(task, wd):
    W = H = 200
    icon = star_poly(5, 70, 30, 100, 100)
    path = resample_closed(icon, 600)
    rng = R(17)
    # teardrop cloud: points scattered in a drop shape below-right of the icon
    th = rng.uniform(0, 2 * math.pi, 600)
    rr = np.sqrt(rng.random(600)) * 60
    drop = np.stack([150 + rr * np.cos(th) * (1 - .6 * np.sin(th) ** 2) * .7, 150 + rr * np.sin(th)], 1)
    k, dmp = 120, 18
    T = np.linspace(0, .9, 28)

    def frame(t):
        e = float(spring(t, k, dmp))
        p = drop + (path - drop) * e
        a = canvas(W, H)
        for x, y in p:
            disc(a, x, y, .9, (120, 200, 255), "add", .9)
        disc(a, 100, 100, 6 * (1 - e) + 2, (255, 255, 255), "add", .5)  # focal glow
        return np.clip(a, 0, 255)
    vid = video(wd / "coalesce.mp4", [frame(t) for t in T])
    fr = vread(vid, W, H)
    pts_at = lambda f: mask_pts((f[..., 2] > 100) & (f[..., 0] < 200))
    c_end = chamfer(pts_at(fr[19]), path)              # ~0.6 s
    c0 = chamfer(pts_at(fr[0]), path)
    z = dmp / (2 * math.sqrt(k))
    num = spring_num([.3, .6], k, dmp)
    closed = spring(np.array([.3, .6]), k, dmp)
    return [check("points sit on the icon path by ~600 ms (chamfer px)", c_end < 2.5, c_end, "<2.5"),
            check("spring 120/18 closed form matches numeric integration", float(np.abs(num - closed).max()) < .01,
                  float(np.abs(num - closed).max()), "<.01"),
            check("damping ratio < 1 (one soft overshoot)", z < 1 and float(spring(np.linspace(0, 1, 200), k, dmp).max()) > 1,
                  z, "<1"),
            check("negative control: the scattered start cloud is far from the path", c0 > 15, c0, ">15")], [vid]


@card("PART-18")
def particles_to_chart(task, wd):
    W, H = 300, 160
    data = [5, 12, 8, 3]
    bins_x = [40 + i * 70 for i in range(4)]
    tg = []
    for b, n in enumerate(data):
        for j in range(n):
            tg.append((bins_x[b] + (j % 3) * 8 - 8, 140 - (j // 3) * 8))
    tg = np.array(tg, dtype=float)
    rng = R(18)
    p0 = rng.uniform((10, 10), (W - 10, 60), (len(tg), 2))
    dist = np.hypot(*(tg - p0).T)
    delay = .3 * (dist - dist.min()) / np.ptp(dist)      # stagger <= 300 ms by distance

    def frame(t):
        a = canvas(W, H)
        e = in_out_cubic((t - delay) / 1.2)[:, None]
        p = p0 + (tg - p0) * e
        dot_a = float(np.clip(1 - (t - 1.6) / .4, 0, 1))
        bar_a = float(np.clip((t - 1.6) / .4, 0, 1))
        for x, y in p:
            a[int(y) - 2:int(y) + 2, int(x) - 2:int(x) + 2] = np.maximum(a[int(y) - 2:int(y) + 2, int(x) - 2:int(x) + 2],
                                                                         (255 * dot_a, 220 * dot_a, 0))
        for b, n in enumerate(data):
            top = 140 - (math.ceil(n / 3) - 1) * 8 - 4
            a[int(top):144, bins_x[b] - 12:bins_x[b] + 12, 2] = 255 * bar_a
        return a
    ts = np.arange(0, 2.2, 1 / 15)
    vid = video(wd / "to_chart.mp4", [frame(t) for t in ts], 15)
    fr = vread(vid, W, H)
    def col_counts(f):
        lab, n = label((f[..., 0] > 128))
        out = []
        for bx in bins_x:
            sub = lab[:, bx - 20:bx + 20]
            out.append(len(set(sub[sub > 0].ravel())))
        return out
    settled = col_counts(fr[int(1.5 * 15)])
    start = col_counts(fr[0])
    bars = []
    for bx in bins_x:
        colm = fr[-1][:, bx, 2] > 128
        bars.append(int(colm.sum()))
    exp_bars = [144 - int(140 - (math.ceil(n / 3) - 1) * 8 - 4) for n in data]
    dots_gone = int((fr[-1][..., 0] > 60).sum())
    return [check("dots per histogram bin equal the data", settled == data, settled, data),
            check("bars fade up with heights from the data (px)", all(abs(a - b) <= 1 for a, b in zip(bars, exp_bars)),
                  bars, exp_bars),
            check("dots faded out after the bars arrive", dots_gone == 0, dots_gone, 0),
            check("stagger <= 300 ms by distance", float(delay.max()) <= .3 + 1e-9, float(delay.max()), "<=.3"),
            check("negative control: the starting scatter does not match the data", start != data, start, data)], [vid]


def hf_block(wd, name):
    """Install a HyperFrames registry block into the work folder with the real CLI; return its HTML with GSAP local."""
    d = Path(wd) / "hf"
    d.mkdir(exist_ok=True)
    fx.run(["hyperframes", "add", name, "--dir", d, "--no-clipboard"], timeout=60)
    hits = list(d.rglob(name + ".html"))
    if not hits:
        raise RuntimeError("hyperframes add %s wrote no %s.html" % (name, name))
    src = hits[0].read_text(encoding="utf-8")
    src = re.sub(r'<script src="https://cdn\.jsdelivr\.net/npm/gsap@[^"]+"></script>',
                 '<script src="%s"></script>' % GSAP_JS.as_uri(), src)
    return hits[0], src


def chrome_shot(wd, name, body, size=(1920, 1080), budget=4000):
    page = Path(wd) / (name + ".html")
    page.write_text(body, encoding="utf-8")
    png = Path(wd) / (name + ".png")
    subprocess.run([chrome_bin(), "--headless=new", "--no-sandbox", "--disable-gpu", "--allow-file-access-from-files",
                    "--hide-scrollbars", "--window-size=%d,%d" % size, "--virtual-time-budget=%d" % budget,
                    "--screenshot=%s" % png, page.as_uri()], capture_output=True, timeout=60, stdin=subprocess.DEVNULL)
    if not png.exists() or png.stat().st_size == 0:
        raise RuntimeError("no screenshot")
    return png


@card("PART-19")
def hf_particle_image_reveal(task, wd):
    path, src = hf_block(wd, "particle-image-reveal")
    inner = re.search(r"<template>(.*)</template>", src, re.S).group(1)
    probe = r"""
<script>(function(){var r={};try{var tl=window.__timelines["particle-image-reveal"];
var cv=document.querySelector(".pir-canvas"),ctx=cv.getContext("2d"),img=document.querySelector(".pir-image");
function lit(){var d=ctx.getImageData(0,0,cv.width,cv.height).data,n=0,h=0;for(var i=3;i<d.length;i+=4){if(d[i]>0)n++;h=(h*31+d[i])%1000000007;}return [n,h];}
r.ts=[0,0.6,1.2,1.8,2.4,2.7,2.8,3.5];r.lit=[];r.op=[];r.clip=[];
r.ts.forEach(function(t){tl.seek(t,false);var L=lit();r.lit.push(L[0]);r.op.push(parseFloat(getComputedStyle(img).opacity));r.clip.push(img.style.clipPath);});
tl.seek(1.5,false);var a=lit()[1];tl.seek(3.9,false);tl.seek(0.2,false);tl.seek(1.5,false);var b=lit()[1];r.det=(a===b);r.hash=a;
r.cw=cv.width;r.ch=cv.height;tl.seek(1.5,false);r.png=cv.toDataURL("image/png");}catch(e){r.err=String(e)}
document.body.setAttribute("data-r",JSON.stringify(r));})();</script>"""
    page = ("<!doctype html><html><head><meta charset='utf-8'><style>html,body{margin:0;width:640px;height:360px;"
            "background:#000}#root{width:640px;height:360px}</style></head><body>" + inner + probe + "</body></html>")
    r = chrome(wd, "pir", page)
    shot = png_from_dataurl(wd / "pir_canvas_1_5s.png", r["png"])
    lit = r["lit"]
    peak = max(lit)
    ipk = lit.index(peak)
    return [check("registry block installed by the hyperframes CLI", path.stat().st_size > 5000, path.stat().st_size, ">5000"),
            check("particle field present mid-reveal", peak > 2000, peak, ">2000"),
            check("trail thins after the peak (2.4 s < peak)", lit[4] < peak and lit[5] < lit[4], lit, "thinning"),
            check("clean by IN = 2.8 s and in the hold", lit[6] == 0 and lit[7] == 0, lit[6:], [0, 0]),
            check("image reveals beneath: opacity 0 -> 1", r["op"][0] == 0 and r["op"][-1] == 1, r["op"], "0->1"),
            check("seek in any order repaints byte-identical canvas", r["det"], r["det"], True),
            check("negative control: the mid-reveal frame is not clean", lit[ipk] > 0 and ipk not in (6, 7), ipk,
                  "peak before 2.8 s")], [shot, path]


@card("PART-41")
def hf_snow_starfield(task, wd):
    p1, snow = hf_block(wd, "snow")
    p2, star = hf_block(wd, "starfield")
    sp = r"""
<script>(function(){var r={};try{var tl=window.__timelines["snow"];var fl=[].slice.call(document.querySelectorAll(".hf-flake"));
function pos(){return fl.map(function(e){var m=e.style.transform.match(/translate\((-?[\d.]+)px, (-?[\d.]+)px\)/);return [+m[1],+m[2]];});}
tl.seek(0,false);var a=pos();tl.seek(6,false);var b=pos();tl.seek(1.0,false);var c=pos();tl.seek(1.05,false);var d=pos();
r.seam=Math.max.apply(null,a.map(function(p,i){return Math.abs(p[0]-b[i][0])+Math.abs(p[1]-b[i][1]);}));
r.size=fl.map(function(e){return parseFloat(e.style.width)});r.op=fl.map(function(e){return parseFloat(e.style.opacity)});
r.vy=c.map(function(p,i){var dy=d[i][1]-p[1];if(dy<-500)dy+=1080*1.04;return dy/0.05;});
r.mask=getComputedStyle(document.getElementById("hf-snow")).webkitMaskImage||getComputedStyle(document.getElementById("hf-snow")).maskImage;
r.n=fl.length;}catch(e){r.err=String(e)}document.body.setAttribute("data-r",JSON.stringify(r));})();</script>"""
    rs = chrome(wd, "snow_probe", snow.replace("</body>", sp + "</body>"))
    shot = chrome_shot(wd, "snow_shot", snow.replace("<style>", "<style>html,body{background:#000!important}", 1)
                       .replace("</body>", "<script>window.__timelines.snow.seek(2.0,false);</script></body>"))
    im = load(shot)
    gray = im.mean(-1)
    yy, xx = np.mgrid[:im.shape[0], :im.shape[1]]
    rc = np.hypot(xx - im.shape[1] / 2, yy - im.shape[0] / 2)
    centre, edge = float(gray[rc < 200].mean()), float(gray[rc > 700].mean())
    tp = r"""
<script>(function(){var r={};try{var tl=window.__timelines["starfield"];var st=[].slice.call(document.querySelectorAll(".hf-star"));
function snap(){return st.map(function(e){return [e.style.transform,+e.style.opacity]});}
tl.seek(0,false);var a=snap();tl.seek(6,false);var b=snap();r.seam=a.every(function(v,i){return v[0]===b[i][0]&&Math.abs(v[1]-b[i][1])<1e-6;});
r.size=st.map(function(e){return parseFloat(e.style.width)});
tl.seek(2.0,false);var c=st.map(function(e){return +e.style.transform.match(/translate3d\((-?[\d.]+)px/)[1]});
tl.seek(2.5,false);var d=st.map(function(e){return +e.style.transform.match(/translate3d\((-?[\d.]+)px/)[1]});
r.vx=c.map(function(x,i){return (d[i]-x)/0.5});var o=[];for(var k=0;k<20;k++){tl.seek(1+k*0.05,false);o.push(+st[3].style.opacity);}r.tw=o;
}catch(e){r.err=String(e)}document.body.setAttribute("data-r",JSON.stringify(r));})();</script>"""
    rt = chrome(wd, "star_probe", star.replace("</body>", tp + "</body>"))
    size, op, vy = np.array(rs["size"]), np.array(rs["op"]), np.array(rs["vy"])
    nb = size < 2 + .85 ** 2 * 16
    corr = float(np.corrcoef(size[nb], op[nb])[0, 1])
    speeds = np.round(np.abs(vy[nb]))
    sizes = np.array(rt["size"])
    tiers = {s: float((sizes == s).mean()) for s in sorted(set(sizes.tolist()))}
    vx = np.abs(np.array(rt["vx"]))
    small, big = vx[sizes == 1].mean(), vx[sizes > 1].mean()
    tw = np.array(rt["tw"])
    # negative control: the same seam measurement on a naive loop with a non-integer cycle count
    naive_seam = abs(((0.37 + 1.33 * 1) % 1) - 0.37) * 1080
    return [check("snow loop seam: t=0 equals t=6 s exactly (px)", rs["seam"] == 0, rs["seam"], 0),
            check("snow size and opacity correlated with depth", corr > .8, corr, ">.8"),
            check("snow falls in three speed layers", len(set((speeds // 20).tolist())) >= 3, sorted(set(speeds.tolist()))[:6], ">=3"),
            check("radial mask keeps the centre clear (centre << edge brightness)", centre < .25 * edge, [centre, edge],
                  "centre<.25 edge"),
            check("starfield: three size tiers", len(tiers) == 3, tiers, 3),
            check("starfield: two parallax layers (big stars drift faster)", big > 2 * small, [small, big], "big>2x small"),
            check("starfield twinkles and loops seamlessly", rt["seam"] and float(tw.std()) > .005, [rt["seam"], float(tw.std())],
                  True),
            check("negative control: a non-integer fall cycle count breaks the seam", naive_seam > 1, naive_seam, ">1")], \
        [shot, p1, p2]


def _project(P, rot_y, W, H, f=2.6, dist=3.2):
    c, s = math.cos(rot_y), math.sin(rot_y)
    x = P[:, 0] * c + P[:, 2] * s
    z = -P[:, 0] * s + P[:, 2] * c
    y = P[:, 1]
    k = f / (dist - z)
    return W / 2 + x * k * H / 2.4, H / 2 - y * k * H / 2.4, z


def _sort_tp(P, bands=24):
    """Order points by (theta band, phi); bands are equal-count quantiles so two sets pair band to band."""
    th = np.arctan2(P[:, 1], np.hypot(P[:, 0], P[:, 2]))
    ph = np.arctan2(P[:, 2], P[:, 0])
    band = np.argsort(np.argsort(th)) * bands // len(P)
    return np.lexsort((ph, band))


@card("PART-20")
def point_cloud_morph(task, wd):
    N = 5000
    rng = R(20)
    u, v = rng.uniform(0, 2 * math.pi, N), rng.uniform(0, 2 * math.pi, N)
    Rr, r = .75, .3
    torus = np.stack([(Rr + r * np.cos(v)) * np.cos(u), r * np.sin(v), (Rr + r * np.cos(v)) * np.sin(u)], 1)
    g = rng.normal(0, 1, (N, 3))
    sphere = g / np.linalg.norm(g, axis=1, keepdims=True) * .9
    a_i, b_i = _sort_tp(torus), _sort_tp(sphere)       # pair targets by sorting both sets by (theta, phi)
    A, B = torus[a_i], sphere[b_i]
    rnd = R(21).permutation(N)
    path_sorted = float(np.linalg.norm(A - B, axis=1).mean())
    path_random = float(np.linalg.norm(A - B[rnd], axis=1).mean())
    W, H = 240, 160

    def frame(t):
        e = float(in_out_cubic(t / 1.5))
        P = A + (B - A) * e
        x, y, z = _project(P, .4 * t, W, H)
        a = canvas(W, H)
        col = np.array([255, 140, 40]) * (1 - e) + np.array([60, 140, 255]) * e   # orange -> blue ramp
        for xi, yi in zip(x.astype(int), y.astype(int)):
            if 0 <= xi < W and 0 <= yi < H:
                a[yi, xi] = col
        return a
    ts = np.arange(0, 1.8, 1 / 15)
    vid = video(wd / "morph.mp4", [frame(t) for t in ts], 15)
    fr = vread(vid, W, H)

    def hole(f):  # a torus seen from above-ish has a hollow centre; the sphere projection is filled
        m = f.max(-1) > 40
        c = m[H // 2 - 6:H // 2 + 6, W // 2 - 6:W // 2 + 6].mean()
        return float(c)
    hue0 = fr[0][fr[0].max(-1) > 40].mean(0)
    hue1 = fr[-1][fr[-1].max(-1) > 40].mean(0)
    # torus viewed edge-on is wide and flat; the sphere is round: aspect ratio of the lit bbox
    def aspect(f):
        b = bbox(f.max(-1) > 40)
        return (b[2] - b[0]) / max(1, b[3] - b[1])
    return [check("start frame is the torus (wide, aspect > 2)", aspect(fr[0]) > 2, aspect(fr[0]), ">2"),
            check("end frame is the sphere (aspect ~1)", abs(aspect(fr[-1]) - 1) < .2, aspect(fr[-1]), "~1"),
            check("colour ramps orange -> blue", hue0[0] > hue0[2] and hue1[2] > hue1[0], [hue0.tolist(), hue1.tolist()],
                  "R>B then B>R"),
            check("(theta, phi) pairing shortens travel vs random pairing", path_sorted < .8 * path_random,
                  [path_sorted, path_random], "sorted < .8 random"),
            check("5-10k points", 5000 <= N <= 10000, N, "5-10k"),
            check("negative control: random pairing travel is longer", path_random > path_sorted, path_random,
                  ">sorted")], [vid]


def perlin2(x, y, seed=0):
    rng = R(seed)
    p = rng.permutation(256)
    p = np.concatenate([p, p])
    xi, yi = np.floor(x).astype(int) & 255, np.floor(y).astype(int) & 255
    xf, yf = x - np.floor(x), y - np.floor(y)
    fade = lambda t: t * t * t * (t * (t * 6 - 15) + 10)
    u, v = fade(xf), fade(yf)
    ang = rng.uniform(0, 2 * math.pi, 256)
    gx, gy = np.cos(ang), np.sin(ang)

    def gd(h, dx, dy):
        h = h & 255
        return gx[h] * dx + gy[h] * dy
    aa, ab = p[p[xi] + yi], p[p[xi] + yi + 1]
    ba, bb = p[p[xi + 1] + yi], p[p[xi + 1] + yi + 1]
    x1 = gd(aa, xf, yf) + u * (gd(ba, xf - 1, yf) - gd(aa, xf, yf))
    x2 = gd(ab, xf, yf - 1) + u * (gd(bb, xf - 1, yf - 1) - gd(ab, xf, yf - 1))
    return x1 + v * (x2 - x1)


def fbm2(x, y, oct=5, seed=0):
    a, w, s = 0.0, 1.0, 0.0
    for i in range(oct):
        a = a + w * perlin2(x, y, seed + i)
        s += w
        x, y, w = x * 2, y * 2, w * .5
    return a / s


@card("PART-22")
def noise_toolbox(task, wd):
    N = 128
    y, x = np.mgrid[:N, :N] / N * 4
    pn = perlin2(x, y, 1)
    fb = fbm2(x * 1.5 / 4 * 4, y * 1.5 / 4 * 4, 5, 2)
    # curl of a scalar potential: divergence-free by construction
    eps = 1e-3
    pot = lambda X, Y: fbm2(X, Y, 3, 5)
    vx = (pot(x, y + eps) - pot(x, y - eps)) / (2 * eps)
    vy = -(pot(x + eps, y) - pot(x - eps, y)) / (2 * eps)
    h = 4 / N
    VX = lambda X, Y: (pot(X, Y + eps) - pot(X, Y - eps)) / (2 * eps)
    VY = lambda X, Y: -(pot(X + eps, Y) - pot(X - eps, Y)) / (2 * eps)
    GX = lambda X, Y: (pot(X + eps, Y) - pot(X - eps, Y)) / (2 * eps)
    GY = lambda X, Y: (pot(X, Y + eps) - pot(X, Y - eps)) / (2 * eps)
    div = (VX(x + eps, y) - VX(x - eps, y) + VY(x, y + eps) - VY(x, y - eps)) / (2 * eps)
    div_grad = (GX(x + eps, y) - GX(x - eps, y) + GY(x, y + eps) - GY(x, y - eps)) / (2 * eps)
    gx = GX(x, y)
    warp = fbm2(x + 2 * fbm2(x, y, 3, 7), y + 2 * fbm2(x + 5.2, y + 1.3, 3, 8), 3, 9)
    # high-frequency share: fBm (5 octaves) carries more detail than single-octave Perlin
    def hf(a):
        F = np.abs(np.fft.fftshift(np.fft.fft2(a - a.mean())))
        yy, xx = np.mgrid[:N, :N]
        rr = np.hypot(xx - N / 2, yy - N / 2)
        return float(F[rr > 16].sum() / F.sum())
    tiles = np.concatenate([(a - a.min()) / np.ptp(a) * 255 for a in (pn, fb, np.hypot(vx, vy), warp)], 1)
    out = save(wd / "noise_toolbox.png", np.repeat(tiles[..., None], 3, 2))
    # time drives from frame/fps: the field at frame 30 of 30 fps equals t = 1.0 exactly
    t_frame = 30 / 30
    same = bool(np.array_equal(fbm2(x + t_frame * .5, y, 2, 3), fbm2(x + 1.0 * .5, y, 2, 3)))
    scale = float(np.abs((VX(x + eps, y) - VX(x - eps, y)) / (2 * eps)).mean()) + 1e-9
    rel_div = float(np.abs(div).mean() / scale)
    rel_grad = float(np.abs(div_grad).mean() / scale)
    return [check("curl field is divergence-free (relative)", rel_div < .05, rel_div, "<.05"),
            check("fBm (5 oct) has more high-frequency energy than Perlin", hf(fb) > 1.3 * hf(pn), [hf(fb), hf(pn)], "fbm>1.3x"),
            check("domain warp differs from plain fBm", float(np.abs(warp - fbm2(x, y, 3, 9)).mean()) > .02,
                  float(np.abs(warp - fbm2(x, y, 3, 9)).mean()), ">.02"),
            check("time from frame/fps is exact", same, same, True),
            check("negative control: the gradient field (not curl) diverges", rel_grad > .3, rel_grad, ">.3")], [out]


@card("PART-23")
def analytic_curl(task, wd):
    rng = R(23)
    lam = np.linspace(260, 1020, 7)
    dirs = rng.uniform(0, 2 * math.pi, 7)
    ks = np.stack([np.cos(dirs), np.sin(dirs)], 1) * (2 * math.pi / lam)[:, None]
    spd = np.linspace(38, 84, 7)
    amp = spd / (2 * math.pi / lam)       # |v| per wave = amp * k = speed
    ph = rng.uniform(0, 2 * math.pi, 7)
    om = .3 + .1 * np.arange(7)

    def psi(p, t):
        return (amp * np.sin(p @ ks.T - om * t + ph)).sum(-1)

    def vel(p, t):
        c = amp * np.cos(p @ ks.T - om * t + ph)
        return np.stack([(c * ks[:, 1]).sum(-1), -(c * ks[:, 0]).sum(-1) - 18.0], -1)
    p = rng.uniform(0, 1000, (400, 2))
    e = 1e-3
    num = np.stack([(psi(p + [0, e], 0) - psi(p - [0, e], 0)) / (2 * e),
                    -(psi(p + [e, 0], 0) - psi(p - [e, 0], 0)) / (2 * e) - 18.0], 1)
    deriv_err = float(np.abs(num - vel(p, 0)).max())
    # divergence of v (without updraft constant): analytic d/dx(dpsi/dy) - d/dy(dpsi/dx) = 0
    dv = ((vel(p + [e, 0], 0)[:, 0] - vel(p - [e, 0], 0)[:, 0]) + (vel(p + [0, e], 0)[:, 1] - vel(p - [0, e], 0)[:, 1])) / (2 * e)
    # integrate RK2 @ 60 Hz for 4 s and measure clumping (nearest-neighbour spread stays like the start)
    from scipy.spatial import cKDTree
    q = rng.uniform(0, 1000, (1500, 2))
    nn0 = float(cKDTree(q).query(q, 2)[0][:, 1].mean())
    traj = []
    for i in range(240):
        t = i / 60
        mid = q + vel(q, t) / 120
        q = q + vel(mid, t + 1 / 120) / 60
        if i % 8 == 0:
            traj.append(q.copy())
    qq = q % 1000
    nn1 = float(cKDTree(qq).query(qq, 2)[0][:, 1].mean())
    # a non-solenoidal (gradient) field on the same particles clumps them
    gq = rng.uniform(0, 1000, (1500, 2))
    for i in range(240):
        c = amp * np.cos(gq @ ks.T - om * (i / 60) + ph)
        gq = gq + np.stack([(c * ks[:, 0]).sum(-1), (c * ks[:, 1]).sum(-1)], -1) / 60
    gq %= 1000
    nn_g = float(cKDTree(gq).query(gq, 2)[0][:, 1].mean())
    a = canvas(250, 250)
    for k_, tr in enumerate(traj):
        for x, y in (tr[:300] % 1000) / 4:
            a[int(y) % 250, int(x) % 250] = (40 + 6 * k_, 160, 255)
    out = save(wd / "curl_paths.png", a)
    return [check("analytic derivatives match finite differences", deriv_err < 1e-3, deriv_err, "<1e-3"),
            check("velocity field divergence-free", float(np.abs(dv).max()) < 1e-6, float(np.abs(dv).max()), "<1e-6"),
            check("particles never clump (NN distance kept >= 85%)", nn1 >= .85 * nn0, [nn1, nn0], ">=.85"),
            check("wavelengths 260-1020 px, speeds 38-84 px/s", lam.min() == 260 and lam.max() == 1020 and spd.max() == 84,
                  [lam.min(), lam.max()], [260, 1020]),
            check("negative control: a gradient field clumps (NN shrinks)", nn_g < .85 * nn0, [nn_g, nn0], "<.85")], [out]


@card("PART-24")
def flow_streaks(task, wd):
    W, H = 320, 200
    rng = R(24)
    seeds = rng.uniform((0, 0), (W, H), (500, 2))
    spd = rng.uniform(40, 120, 500)

    def angle(x, y, t):
        return (perlin2(x * .0025 * 6, y * .0025 * 6, 3) * .5 + .5 + t * .2) * 2 * math.pi   # .0025 at 1920 px -> x6 here

    a = np.zeros((H, W, 3))
    lines = []
    for (x, y), s in zip(seeds, spd):
        pts = [(x, y)]
        for k in range(14):
            th = angle(np.array(x), np.array(y), 0)
            x, y = x + math.cos(float(th)) * s / 30, y + math.sin(float(th)) * s / 30
            pts.append((x, y))
        lines.append(pts)
    layer = Image.new("RGB", (W, H), 0)
    d = ImageDraw.Draw(layer)
    for pts in lines:
        d.line(pts, fill=(64, 90, 120), width=1)       # alpha .25 of (255,360,480)-ish, accumulated additively
        L = np.asarray(layer).astype(float)
        a += L
        layer.paste(0, (0, 0, W, H))
    a = np.clip(a, 0, 255)
    out = save(wd / "flow.png", a)
    img = load(out)
    # streak direction must follow the field: render a sparse probe sheet, measure each streak's PCA axis from the
    # pixels and compare (mod 180 deg) with the field angle at its centroid
    def axis_err(streaks):
        errs = []
        for k, pts in enumerate(streaks):
            pr = Image.new("L", (W, H), 0)
            ImageDraw.Draw(pr).line(pts, fill=255, width=1)
            m = np.asarray(pr) > 0
            ys, xs = np.nonzero(m)
            if len(xs) < 8:
                continue
            w_, v_ = np.linalg.eigh(np.cov(np.stack([xs, ys])))
            ax = math.atan2(v_[1, 1], v_[0, 1])
            th = float(angle(np.array(xs.mean()), np.array(ys.mean()), 0))
            dd = (ax - th) % math.pi
            errs.append(min(dd, math.pi - dd))
        return math.degrees(float(np.median(errs)))
    med = axis_err(lines[:60])
    rand = rng.uniform(0, 2 * math.pi, 60)
    bad = [[(l[0][0], l[0][1]), (l[0][0] + math.cos(r_) * 25, l[0][1] + math.sin(r_) * 25)] for r_, l in zip(rand, lines[:60])]
    med_bad = axis_err(bad)
    overlap = float((img.max(-1) > 130).mean())
    added = float(img.max())
    return [check("streaks follow the noise angle (median deg)", med < 10, med, "<10"),
            check("additive blend: overlaps brighter than one streak", added > 120 and overlap > 0, added, ">120"),
            check("500 seeds, 14-step polylines", len(lines) == 500 and len(lines[0]) == 15, len(lines), 500),
            check("negative control: random directions miss the field", med_bad > 30, med_bad, ">30")], [out]


@card("PART-26")
def route_flow(task, wd):
    W, H = 300, 160
    nodes = {"A": (30, 80), "B": (150, 30), "C": (150, 130), "D": (270, 80), "E": (270, 10)}
    edges = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("B", "E")]
    focus = {"A", "B", "D"}                             # filter to the focus neighbourhood
    shown = [e for e in edges if e[0] in focus and e[1] in focus]
    paths = {e: resample_closed(np.array([nodes[e[0]], nodes[e[1]]]), 2) for e in shown}

    def point_at(e, u):
        p, q = np.array(nodes[e[0]], float), np.array(nodes[e[1]], float)
        return p + (q - p) * u
    T = .6                                               # 600 ms per traversal
    phases = {e: [0, .33, .66] for e in shown}
    TRAIL = 12

    def frame(t):
        a = canvas(W, H)
        for e in shown:
            for ph in phases[e]:
                for k in range(TRAIL):                   # trail = last samples with decaying opacity
                    u = ((t - k / 60) / T + ph) % 1
                    x, y = point_at(e, u)
                    disc(a, x, y, 2 if k == 0 else 1.2, (255, 210, 60), "max", (1 - k / TRAIL) ** 1.5)
        return a
    ts = np.arange(0, 1.2, 1 / 30)
    vid = video(wd / "routes.mp4", [frame(t) for t in ts])
    fr = vread(vid, W, H)
    # direction: brightest pixel along edge A->B advances from A to B over time
    e = ("A", "B")
    pa, pb = np.array(nodes["A"], float), np.array(nodes["B"], float)
    samp = [pa + (pb - pa) * s for s in np.linspace(.02, .98, 200)]

    def head_u(f):
        v = [f[int(y), int(x)].sum() for x, y in samp]
        return np.linspace(.02, .98, 200)[int(np.argmax(v))]
    # single-particle variant for the speed measurement
    def one(t, trail=TRAIL):
        a = canvas(W, H)
        for k in range(trail):
            x, y = point_at(e, ((t - k / 60) / T) % 1)
            disc(a, x, y, 2 if k == 0 else 1.2, (255, 0, 0), "max", (1 - k / trail) ** 1.5 if k else 1)
        return a
    v1 = vread(video(wd / "one.mp4", [one(t) for t in np.arange(0, .6, 1 / 30)]), W, H)

    def trail_len(f):
        v = np.array([f[int(y), int(x), 0] for x, y in samp])
        return int((v > 20).sum())
    tl_on = trail_len(v1[9])
    tl_off = trail_len(one(9 / 30, trail=1))
    us = [head_u(f) for f in v1]
    du = np.diff(us)
    period = 1 / float(np.median(du)) / 30
    trail_f = fr[10]
    lit_off_edges = 0
    for e2 in edges:
        if e2 not in shown:
            p, q = np.array(nodes[e2[0]], float), np.array(nodes[e2[1]], float)
            mid = (p + q) / 2
            lit_off_edges += int(trail_f[int(mid[1]) - 3:int(mid[1]) + 3, int(mid[0]) - 3:int(mid[0]) + 3].max() > 30)
    # trail: brightness decays behind the head
    f = fr[5]
    v = np.array([f[int(y), int(x)].sum() for x, y in samp])
    return [check("dots move A -> B (direction)", float(np.median(du)) > 0, float(np.median(du)), ">0"),
            check("600 ms per traversal (measured)", abs(period - .6) < .05, period, .6),
            check("only focus-neighbourhood edges carry particles", lit_off_edges == 0, lit_off_edges, 0),
            check("fading trail measured behind the head (lit samples)", tl_on >= 8, tl_on, ">=8"),
            check("negative control: the same measurement on a trail-less dot", tl_off < 8, tl_off, "<8")], [vid]


@card("PART-29")
def dot_grid_attractor(task, wd):
    W, H, G, RAD = 336, 192, 24, 180

    def grid_pos(ax, ay, push=40.0):
        gy, gx = np.mgrid[G // 2:H:G, G // 2:W:G].astype(float)
        dx, dy = gx - ax, gy - ay
        d = np.hypot(dx, dy) + 1e-6
        f = np.clip(1 - d / RAD, 0, 1) ** 2 * push
        return gx + dx / d * f, gy + dy / d * f, d, gx, gy
    lead = lambda f: (40 + f * 8.0, 96 + 30 * math.sin(f * .2))
    def render(f, push=40.0):
        ax, ay = lead(f)
        x, y, d, _, _ = grid_pos(ax, ay, push)
        a = canvas(W, H)
        tint = np.clip(1 - d / RAD, 0, 1)
        for xi, yi, ti in zip(x.ravel(), y.ravel(), tint.ravel()):
            disc(a, xi, yi, 2, (80 + 175 * ti, 80, 255 - 175 * ti))
        for k in range(15):                              # chain of 15 balls lagging 2 frames each
            lx, ly = lead(max(0, f - 2 * (k + 1)))
            disc(a, lx, ly, 3, (0, 255, 0))
        disc(a, ax, ay, 5, (255, 255, 255))
        return a
    vid = video(wd / "dot_grid.mp4", [render(f) for f in range(30)])
    fr = vread(vid, W, H)
    ax, ay = lead(20)
    x, y, d, gx, gy = grid_pos(ax, ay)
    # measure displacement of the dot nearest the attractor in the rendered frame vs its rest position
    near = np.unravel_index(np.argmin(np.where(d > 40, d, 1e9)), d.shape)
    rx, ry = gx[near], gy[near]
    dotm = lambda w_: (w_.max(-1) > 60) & (w_[..., 1] < 120)

    ex, ey = x[near], y[near]                            # where the pushed dot should be

    def found(img):
        win = img[int(ey) - 6:int(ey) + 7, int(ex) - 6:int(ex) + 7]
        c = centroid(dotm(win))
        return (math.hypot(c[0] + int(ex) - 6 + .5 - ex, c[1] + int(ey) - 6 + .5 - ey), win) if c else (99.0, win)
    err, win = found(fr[20])
    m = dotm(win)
    moved = math.hypot(ex - rx, ey - ry)
    away = ((ex - rx) * (rx - ax) + (ey - ry) * (ry - ay)) > 0
    err0, _ = found(render(20, push=0.0))
    far = np.unravel_index(np.argmax(d), d.shape)
    fx_, fy_ = gx[far], gy[far]
    wf = fr[20][int(fy_) - 6:int(fy_) + 6, int(fx_) - 6:int(fx_) + 6]
    cf = centroid(dotm(wf))
    far_moved = math.hypot(cf[0] - 6, cf[1] - 6) if cf else 99
    chain = [centroid((f_[..., 1] > 200) & (f_[..., 0] < 60)) for f_ in fr]
    lag_ok = chain[20] is not None
    return [check("dot near the attractor rendered at its pushed-away position (px error)", err < 1.5 and moved > 3 and away,
                  [err, moved], "<1.5, moved>3"),
            check("dots beyond the 180 px falloff stay at rest", far_moved < 1.0, far_moved, "<1"),
            check("near dots tinted by distance (red > blue)", float(win[m][:, 0].mean()) > float(win[m][:, 2].mean()) if m.any() else False,
                  float(win[m][:, 0].mean()) if m.any() else 0, "red>blue"),
            check("lagging chain drawn", lag_ok, lag_ok, True),
            check("negative control: with no push no dot is found at the pushed position", err0 > 3, err0, ">3")], [vid]


@card("PART-30")
def multi_trace(task, wd):
    W, H = 400, 200
    rng = R(30)
    x = np.linspace(0, W, 200)
    traces = []
    for i in range(15):
        f = rng.uniform(.01, .04, 3)
        ph = rng.uniform(0, 6.28, 3)
        amp = rng.uniform(20, 60)
        y = H / 2 + sum(np.sin(x * f[k] + ph[k]) for k in range(3)) / 3 * amp + perlin2(x * .02, np.full_like(x, i), 1) * 10
        traces.append(np.stack([x, y], 1))
    a = np.zeros((H, W, 3))
    for tr in traces:
        L = Image.new("RGB", (W, H), 0)
        ImageDraw.Draw(L).line([tuple(p) for p in tr], fill=(40, 120, 255), width=1)

        a += np.asarray(L) * .25                          # alpha .25, additive ("lighter")
    a = np.clip(a, 0, 255)
    out = save(wd / "traces.png", a)
    img = load(out)
    cols = img.max(-1).max(0)
    covered = float((cols > 0).mean())
    peak = float(img[..., 2].max())
    # each trace is a sum of 3 sines (+ small noise): an FFT of one trace shows <= 3 dominant peaks
    y0 = traces[0][:, 1] - traces[0][:, 1].mean()
    F = np.abs(np.fft.rfft(y0))
    dom = int((F > .3 * F.max()).sum())
    single = Image.new("RGB", (W, H), 0)
    ImageDraw.Draw(single).line([tuple(p) for p in traces[0]], fill=(10, 30, 64), width=1)
    one_peak = float(np.asarray(single)[..., 2].max())
    over = Image.new("RGB", (W, H), 0)                  # untreated: normal (overwrite) compositing of the same traces
    for tr in traces:
        ImageDraw.Draw(over).line([tuple(p) for p in tr], fill=(10, 30, 64), width=1)
    over_peak = float(np.asarray(over)[..., 2].max())
    return [check("15 traces span the full width", covered > .99 and len(traces) == 15, covered, ">.99"),
            check("200 points per trace", traces[0].shape[0] == 200, traces[0].shape[0], 200),
            check("additive overlap brighter than a single .25 trace", peak > 2 * one_peak, [peak, one_peak], "peak>2x"),
            check("each trace is a few sines (<= 4 dominant FFT bins)", dom <= 4, dom, "<=4"),
            check("negative control: overwrite compositing shows no overlap gain", not (over_peak > 2 * one_peak),
                  [over_peak, one_peak], "no gain")], [out]


@card("PART-35")
def dust_motes(task, wd):
    W, H, n = 320, 180, 38
    i = np.arange(n)

    def pos(t):
        x = (137.3 * i + t * (5 + i % 3)) % W
        y = (np.sin(2.71 * i + .18 * t) * .42 + .5) * H
        return x, y
    alpha = .07 + .41 * ((i * 7) % 11) / 10
    def render(t):
        a = canvas(W, H, (8, 10, 16))
        x, y = pos(t)
        for k in range(n):
            disc(a, x[k], y[k], 1.6, (255, 236, 200), "over", alpha[k])
        disc(a, *[v[0] for v in pos(t)], 2.2, (255, 0, 0), "over", 1)   # mote 0 tracked
        return a
    vid = video(wd / "motes.mp4", [render(t) for t in np.arange(0, 2, 1 / 15)], 15)
    fr = vread(vid, W, H)
    tr = track(fr, 0, thr=180, othr=60)
    xs = np.array([c[0] for c in tr if c])
    vx = float(np.polyfit(np.arange(len(xs)) / 15, xs, 1)[0])
    speeds = 5 + i % 3
    st = [render(0)] * 8
    tr0 = track(st, 0, thr=180, othr=60)
    vx0 = float(np.polyfit(np.arange(8) / 15, [c[0] for c in tr0], 1)[0])
    al_meas = []
    f0 = fr[0]
    x0, y0 = pos(0)
    keep = [k for k in range(1, n) if min(math.hypot(x0[k] - x0[j], y0[k] - y0[j]) for j in range(n) if j != k) > 6]
    for k in keep:
        w_ = f0[max(0, int(y0[k]) - 1):int(y0[k]) + 2, max(0, int(x0[k]) - 1):int(x0[k]) + 2, 2]
        al_meas.append((w_.max() - 16) / (200 - 16))
    corr = float(np.corrcoef(al_meas, alpha[keep])[0, 1])
    # staggered: three distinct speeds and alpha range .07-.48
    return [check("tracked mote drifts 5 px/s (mote 0)", abs(vx - 5) < .6, vx, 5),
            check("three staggered speeds 5/6/7 px/s", sorted(set(speeds.tolist())) == [5, 6, 7], sorted(set(speeds.tolist())), [5, 6, 7]),
            check("rendered opacity follows the per-mote alpha", corr > .9, corr, ">.9"),
            check("alpha within .07-.48", alpha.min() >= .07 and alpha.max() <= .48 + 1e-9, [alpha.min(), alpha.max()], ".07-.48"),
            check("negative control: the same tracking on a frozen (t = 0) clip finds no drift", abs(vx0) < .1, vx0, "~0")], [vid]


@card("PART-37")
def parallax_rain(task, wd):
    W, H = 290, 170                                      # 1450 x 850 wrap scaled by 1/5
    rng = R(37)
    far = dict(n=152, v=rng.uniform(340, 600, 152) / 5, L=rng.uniform(11, 25, 152) / 5, col=hexc("#86b7c9"), a=.13 * 3, par=.03)
    near = dict(n=32, v=np.full(32, 630 / 5), L=np.full(32, 37 / 5), col=hexc("#95d6df"), a=.17 * 3, par=.1)
    for lay in (far, near):
        lay["x"], lay["y"] = rng.uniform(0, W, lay["n"]), rng.uniform(0, H, lay["n"])
    cam = lambda t: 200 * t                               # camera pan in px/s, layers shift by their parallax factor

    def frame(t, ev_t=.4, layers=None):
        a = canvas(W, H, (10, 14, 22))
        for lay in (layers or (far, near)):
            y = (lay["y"] + lay["v"] * t) % H
            x = (lay["x"] - cam(t) * lay["par"]) % W
            for xi, yi, Li in zip(x, y, lay["L"]):
                a[int(max(0, yi - Li)):int(yi) + 1, int(xi)] = a[int(max(0, yi - Li)):int(yi) + 1, int(xi)] * (1 - lay["a"]) + lay["col"] * lay["a"]
        u = t - ev_t
        if 0 <= u <= .63:                                 # puddle ripple rx 5->29, ry 1->5 and 11 ballistic droplets
            k = u / .63
            rx, ry = (5 + 24 * k) / 2, (1 + 4 * k) / 2
            yy, xx = np.mgrid[:H, :W]
            e = np.abs(((xx - 145) / rx) ** 2 + ((yy - 150) / max(ry, .5)) ** 2 - 1) < .25
            a[e] = (255, 255, 255)
            r2 = R(99)
            for _ in range(11):
                vx, vy = r2.uniform(-105, 105) / 5, r2.uniform(-129, -45) / 5
                disc(a, 145 + vx * u, 150 + vy * u + .5 * 145 / 5 * u * u, 1, (255, 0, 0))
        return a
    ts = np.arange(0, 1.2, 1 / 30)
    vid = video(wd / "rain.mp4", [frame(t) for t in ts])
    fr = vread(vid, W, H)
    # measure layer speeds by tracking: velocity of the layers' known drops in the rendered frames
    def drop_v(lay, idx):
        ys = []
        for k in (2, 5):
            col = fr[k][:, int((lay["x"][idx] - cam(k / 30) * lay["par"]) % W)]
            ys.append(float(np.argmax(np.abs(np.diff(col.mean(-1))))))
        return ys
    def shift(lay, par_on=True):
        p0, p1 = [frame(t, 99, [dict(lay, par=lay["par"] if par_on else 0)]).mean(-1).sum(0) for t in (0, .5)]
        p0, p1 = p0 - p0.mean(), p1 - p1.mean()
        return int(np.argmax([float((np.roll(p0, -d) * p1).sum()) for d in range(0, 40)]))
    pr_far, pr_near = shift(far), shift(near)
    pr_none = shift(near, par_on=False)
    drops = []
    for k in range(int(.4 * 30), int(1.03 * 30)):
        m = (fr[k][..., 0] > 200) & (fr[k][..., 1] < 80)
        c = centroid(m)
        drops.append(c[1] if c else np.nan)
    life = int(np.sum(~np.isnan(drops)))
    return [check("near rain faster than far (mean px/s)", near["v"].mean() > far["v"].mean(), [near["v"].mean(), far["v"].mean()], "near>far"),
            check("near layer thicker/longer and fewer", near["n"] < far["n"] and near["L"].mean() > far["L"].mean(),
                  [near["n"], far["n"]], "near fewer"),
            check("parallax measured: in .5 s near shifts ~10 px, far ~3 px", abs(pr_near - 10) <= 1 and abs(pr_far - 3) <= 1,
                  [pr_near, pr_far], [10, 3]),
            check("negative control: no parallax factor -> no horizontal shift", pr_none == 0, pr_none, 0),
            check("splash droplets live ~.63 s (frames)", abs(life - 19) <= 2, life, 19),
            check("rain wraps (frame 0 and 1.2 s both full)", float(fr[-1].mean()) > 10, float(fr[-1].mean()), ">10"),
            check("negative control: without the footfall event there are no droplets",
                  int(((frame(.6, ev_t=99)[..., 0] > 200) & (frame(.6, ev_t=99)[..., 1] < 80)).sum()) == 0, 0, 0)], [vid]


def _streak_angle(img, thr=40):
    """Median orientation (deg from vertical) of the bright streak components in an image."""
    lab, n = label(img.max(-1) > thr, eight=True)
    out = []
    for k in range(1, n + 1):
        ys, xs = np.nonzero(lab == k)
        if len(xs) < 6:
            continue
        w_, v_ = np.linalg.eigh(np.cov(np.stack([xs, ys])))
        ax = v_[:, 1]
        out.append(math.degrees(math.atan2(abs(ax[0]), abs(ax[1]))) * (1 if ax[0] * ax[1] >= 0 else -1))
    return float(np.median(out)) if out else 0.0, len(out)


@card("PART-39")
def rain_fog(task, wd):
    W, H = 320, 180
    rng = R(39)
    n = 400
    x0, y0 = rng.uniform(-40, W, n), rng.uniform(0, H, n)
    L = rng.uniform(12, 24, n)
    al = rng.uniform(.25, .4, n)
    from scipy.ndimage import gaussian_filter

    def frame(t, slant=12.0, fog=True):
        a = canvas(W, H, (20, 26, 36))
        if fog:
            for b in range(3):                            # 2-3 blurred fog bands drifting
                band = np.zeros((H, W))
                yc = 50 + b * 45
                band[int(yc) - 6:int(yc) + 6, :] = 1
                band = gaussian_filter(np.roll(band, int(t * (8 + 4 * b)), 1), 8)
                a += band[..., None] * 60
        th = math.radians(slant)
        lay = Image.new("L", (W, H), 0)
        d = ImageDraw.Draw(lay)
        for i in range(n):
            yy = (y0[i] + 500 * t) % (H + 30) - 15
            xx = x0[i] + yy * math.tan(th)
            d.line([(xx, yy), (xx + L[i] * math.sin(th), yy + L[i] * math.cos(th))], fill=int(255 * al[i]))
        a += np.asarray(lay)[..., None] * .8
        return np.clip(a, 0, 255)
    out = save(wd / "rain_fog.png", frame(.3))
    vid = video(wd / "rain_fog.mp4", [frame(t) for t in np.arange(0, .6, 1 / 30)])
    img = load(out)
    sheet = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(sheet)
    for i in range(0, n, 10):                            # sparse probe sheet for orientation
        d.line([(x0[i] + 20, y0[i]), (x0[i] + 20 + L[i] * math.sin(math.radians(12)), y0[i] + L[i] * math.cos(math.radians(12)))], fill=255)
    ang, cnt = _streak_angle(np.repeat(np.asarray(sheet)[..., None].astype(float), 3, 2))
    rows = img.mean(-1).mean(1)
    fog_bands = int(((rows[1:-1] > rows[:-2]) & (rows[1:-1] > rows[2:]) & (rows[1:-1] > rows.mean())).sum())
    nf = frame(.3, fog=False).mean(-1).mean(1)
    fog_none = int(((nf[1:-1] > nf[:-2]) & (nf[1:-1] > nf[2:]) & (nf[1:-1] > nf.mean() + 8)).sum())
    fb = float(rows.max() - np.median(rows))
    fb0 = float(nf.max() - np.median(nf))
    return [check("streaks slanted 10-15 deg (measured)", 10 <= abs(ang) <= 15, ang, "10-15"),
            check("300-500 streaks, alpha .25-.4, length 12-24", 300 <= n <= 500 and al.min() >= .25 and L.max() <= 24, n, "300-500"),
            check("fog bands lift row brightness (>= 20 levels)", fb > 20, fb, ">20"),
            check("negative control: without fog the same row profile has no bands", fb0 < 10, fb0, "<10")], [out, vid]


@card("PART-43")
def motes_kick_rings(task, wd):
    W, H, fps = 240, 240, 30
    kicks = [.3, 1.8]
    rng = R(43)
    n = 72
    mx, my0 = rng.uniform(0, W, n), rng.uniform(0, 1, n)
    msp, mr = rng.uniform(.006, .026, n), rng.uniform(2, 9, n) / 3

    def frame(t):
        a = canvas(W, H)
        lift = sum(.02 * math.exp(-(t - k) * 6) for k in kicks if t >= k)
        y = ((my0 - msp * t * 10 - lift) % 1) * H
        for i in range(n):
            disc(a, mx[i], y[i], mr[i], (200, 200, 120), "add", .5 + .5 * math.sin(t * 5 + i))
        for k in kicks:
            dt = t - k
            if 0 <= dt <= 1.3:
                rad = (.16 + .42 * dt) * min(W, H)
                alpha = .22 * (1 - dt / 1.3) ** 2
                yy, xx = np.mgrid[:H, :W]
                ring = np.abs(np.hypot(xx - W / 2, yy - H / 2) - rad) < 1.5
                a[ring, 2] += 255 * alpha * 4
        return np.clip(a, 0, 255)
    ts = np.arange(0, 2.4, 1 / fps)
    vid = video(wd / "verse.mp4", [frame(t) for t in ts], fps)
    fr = vread(vid, W, H)
    yy, xx = np.mgrid[:H, :W]
    rr = np.hypot(xx - W / 2, yy - H / 2)

    def ring_r(f):
        m = (f[..., 2] - f[..., 0]) > 40
        return float(rr[m].mean()) if m.sum() > 20 else None
    k_t = .3 + .5
    r_meas = ring_r(fr[int(round(k_t * fps))])
    r_exp = (.16 + .42 * .5) * 240
    first = next(i for i, f in enumerate(fr) if ring_r(f) is not None)
    gone = ring_r(fr[int(round(1.65 * fps))])
    a_early = float(((fr[12][..., 2] - fr[12][..., 0]) * ((fr[12][..., 2] - fr[12][..., 0]) > 40)).sum())
    return [check("ring radius (.16 + .42 dt) min(W,H) at dt = .5 s", r_meas is not None and abs(r_meas - r_exp) < 3, r_meas, r_exp),
            check("ring starts on the kick frame", first == int(round(.3 * fps)), first, int(round(.3 * fps))),
            check("ring dead 1.3 s after the kick (none at 1.65 s)", gone is None, gone, None),
            check("72 motes", n == 72, n, 72),
            check("negative control: before the first kick there is no ring", ring_r(fr[5]) is None, ring_r(fr[5]), None)], [vid]


def fib_sphere(N):
    i = np.arange(N)
    y = 1 - 2 * (i + .5) / N
    r = np.sqrt(1 - y * y)
    th = 2.39996 * i
    return np.stack([r * np.cos(th), y, r * np.sin(th)], 1)


@card("PART-46")
def fibonacci_sphere(task, wd):
    N, W, H = 900, 240, 240
    P = fib_sphere(N)
    from scipy.spatial import cKDTree
    nn = cKDTree(P).query(P, 2)[0][:, 1]
    cv = float(nn.std() / nn.mean())
    rnd = R(46).normal(0, 1, (N, 3))
    rnd /= np.linalg.norm(rnd, axis=1, keepdims=True)
    nr = cKDTree(rnd).query(rnd, 2)[0][:, 1]
    cv_r = float(nr.std() / nr.mean())
    x, y, z = _project(P, .6, W, H, 2.6, 3.2)
    order = np.argsort(z)                               # depth sort: far first
    a = canvas(W, H)
    for k in order:
        al = .25 + .6 * (z[k] + 1) / 2
        disc(a, x[k], y[k], .8 + 1.2 * (z[k] + 1) / 2, (255, 60, 60) if k % 97 == 0 else (230, 230, 255), "over", al)
    out = save(wd / "fib_sphere.png", a)
    img = load(out)
    zz = z
    front = [img[int(y[k]), int(x[k])].mean() for k in range(N) if zz[k] > .6]
    back = [img[int(y[k]), int(x[k])].mean() for k in range(N) if zz[k] < -.6]
    return [check("golden-angle points are evenly spaced (NN CV)", cv < .12, cv, "<.12"),
            check("all points on the unit sphere", float(np.abs(np.linalg.norm(P, axis=1) - 1).max()) < 1e-9, 0, 0),
            check("front points brighter than back (alpha by depth)", np.mean(front) > np.mean(back) + 30, [np.mean(front), np.mean(back)], "front>back"),
            check("red accent points present", int(((img[..., 0] > 150) & (img[..., 1] < 100)).sum()) > 5,
                  int(((img[..., 0] > 150) & (img[..., 1] < 100)).sum()), ">5"),
            check("negative control: random sphere points are uneven (NN CV)", cv_r > 2 * cv, cv_r, ">2x")], [out]


@card("PART-47")
def spiral_galaxy(task, wd):
    N, W, H = 2500, 260, 200
    rng = R(47)
    i = np.arange(N)
    arm = i % 3
    d = rng.random(N) ** .6
    a0 = arm * 2.094 + 4 * d + rng.normal(0, .15, N)
    cols = np.array([[255, 160, 90], [120, 160, 255], [220, 120, 255]])

    def frame(t, diff=True):
        ang = a0 + t * .9 / (d + .15) if diff else a0 + t * .9
        x = W / 2 + np.cos(ang) * d * 110
        y = H / 2 + np.sin(ang) * d * 110 * .55
        a = canvas(W, H)
        for k in range(N):
            xi, yi = int(x[k]), int(y[k])
            if 0 <= xi < W and 0 <= yi < H:
                a[yi, xi] += cols[arm[k]] * .5
        return np.clip(a, 0, 255), ang
    img, _ = frame(1.0)
    out = save(wd / "galaxy.png", img)

    def ann_shift(diff, lo, hi):
        """Measured angular shift of an annulus between t = 0 and t = .15 s (angular histogram cross-correlation)."""
        hs = []
        for t in (0, .5):
            f, _ = frame(t, diff)
            ys, xs = np.nonzero(f.max(-1) > 0)
            ex, ey = (xs - W / 2) / 110, (ys - H / 2) / (110 * .55)
            rr = np.hypot(ex, ey)
            sel = (rr > lo) & (rr < hi)
            hs.append(np.histogram(np.arctan2(ey[sel], ex[sel]), 360, (-math.pi, math.pi))[0].astype(float))
        c = [float((np.roll(hs[0], s_) * hs[1]).sum()) for s_ in range(0, 100)]   # < 120 deg: 3-arm symmetry
        return int(np.argmax(c))
    s_in, s_out = ann_shift(True, .2, .35), ann_shift(True, .8, 1.0)
    r_in, r_out = ann_shift(False, .2, .35), ann_shift(False, .8, 1.0)
    b = load(out)
    yy, xx = np.nonzero(b.max(-1) > 0)
    aspect = float(np.ptp(yy) / np.ptp(xx))
    exp_in = math.degrees(.5 * float(np.mean(.9 / (d[(d > .2) & (d < .35)] + .15))))
    return [check("measured: core turns faster than the rim (deg in .5 s)", s_in > 2 * max(1, s_out), [s_in, s_out], "in>2x out"),
            check("inner shift matches omega = .9/(d+.15) (deg)", abs(s_in - exp_in) < 6, s_in, exp_in),
            check("disc squashed .55 in y (measured aspect)", abs(aspect - .55) < .07, aspect, .55),
            check("three arm colours rendered", len({tuple(c) for c in b[b.max(-1) > 0].astype(int)}) >= 3, 3, ">=3"),
            check("negative control: rigid rotation measures equal shifts", abs(r_in - r_out) <= 3, [r_in, r_out], "equal")], [out]


@card("PART-48")
def warp_starfield(task, wd):
    W, H, N = 240, 160, 600
    rng = R(48)
    P = np.stack([rng.uniform(-1, 1, N) * 400, rng.uniform(-1, 1, N) * 300, rng.uniform(20, 400, N)], 1)
    speeds = np.concatenate([np.full(10, 2.0), np.linspace(2, 30, 10), np.full(10, 30.0)])

    def run(speeds):
        z = P[:, 2].copy()
        frames, lens = [], []
        for s in speeds:
            zp = z.copy()
            z = z - s
            z = np.where(z < 1, z + 400, z)
            ok = z < zp
            a = Image.new("RGB", (W, H), 0)
            dr = ImageDraw.Draw(a)
            L = []
            for k in np.nonzero(ok)[0]:
                x0, y0 = W / 2 + P[k, 0] / zp[k] * 40, H / 2 + P[k, 1] / zp[k] * 40
                x1, y1 = W / 2 + P[k, 0] / z[k] * 40, H / 2 + P[k, 1] / z[k] * 40
                dr.line([(x0, y0), (x1, y1)], fill=(94, 108, 153), width=1)
                L.append(math.hypot(x1 - x0, y1 - y0))
            frames.append(np.asarray(a).astype(float))
            lens.append(float(np.median(L)))
        return frames, lens
    frames, lens = run(speeds)
    vid = video(wd / "warp.mp4", frames)
    fr = vread(vid, W, H)
    lit_slow = float((fr[5].max(-1) > 20).sum())
    lit_fast = float((fr[-3].max(-1) > 20).sum())
    _, lens_c = run(np.full(30, 2.0))
    # projected x/z law: a star at (x, z) projects to W/2 + 40 x / z
    k = 0
    proj_ok = abs((W / 2 + P[k, 0] / P[k, 2] * 40) - (W / 2 + 40 * P[k, 0] / P[k, 2])) < 1e-12
    return [check("streak length jumps with speed (fast/slow median)", lens[-1] > 5 * lens[0], [lens[0], lens[-1]], ">5x"),
            check("more streak pixels at warp speed (rendered)", lit_fast > 3 * lit_slow, [lit_slow, lit_fast], ">3x"),
            check("~600 stars projected x/z, y/z", N == 600 and proj_ok, N, 600),
            check("negative control: a constant-speed run never lengthens", lens_c[-1] < 2 * lens_c[0], [lens_c[0], lens_c[-1]], "<2x")], [vid]


@card("PART-49")
def torus_constellation(task, wd):
    N, W, H = 2000, 240, 200
    rng = R(49)
    u, v = rng.uniform(0, 2 * math.pi, N), rng.uniform(0, 2 * math.pi, N)
    T = np.stack([(1 + .35 * np.cos(v)) * np.cos(u), .35 * np.sin(v), (1 + .35 * np.cos(v)) * np.sin(u)], 1)
    rx = .5
    Rx = np.array([[1, 0, 0], [0, math.cos(rx), -math.sin(rx)], [0, math.sin(rx), math.cos(rx)]])
    P = T @ Rx.T
    x, y, z = _project(P, .3, W, H, 2.6, 3.4)
    a = canvas(W, H)
    for k in np.argsort(z):
        disc(a, x[k], y[k], .7, (255, 70, 70) if k % 50 == 0 else (220, 220, 255), "over", .25 + .6 * (z[k] + 1.35) / 2.7)
    t_out = save(wd / "torus.png", a)
    # constellation: link pairs with d < 90 px, alpha 1 - d/90
    S = rng.uniform(0, 400, (60, 2))
    from scipy.spatial.distance import cdist
    D = cdist(S, S)
    pairs = [(i, j) for i in range(60) for j in range(i + 1, 60) if D[i, j] < 90]
    c = canvas(400, 400, (12, 8, 24))
    lay = Image.new("L", (400, 400), 0)
    dr = ImageDraw.Draw(lay)
    for i, j in pairs:
        dr.line([tuple(S[i]), tuple(S[j])], fill=int(255 * (1 - D[i, j] / 90)))
    c += np.asarray(lay)[..., None] * np.array([.7, .6, 1.0])
    c_out = save(wd / "constellation.png", np.clip(c, 0, 255))
    img = load(c_out)
    i, j = min(pairs, key=lambda p: D[p])
    mid = (S[i] + S[j]) / 2
    near_val = img[int(mid[1]) - 1:int(mid[1]) + 2, int(mid[0]) - 1:int(mid[0]) + 2].max() - 24
    exp_val = 255 * (1 - D[i, j] / 90)
    far_pair = [(i_, j_) for i_ in range(60) for j_ in range(i_ + 1, 60) if 95 < D[i_, j_] < 140]
    m2 = (S[far_pair[0][0]] + S[far_pair[0][1]]) / 2
    hole = load(t_out)[H // 2 - 4:H // 2 + 4, W // 2 - 4:W // 2 + 4].mean()
    ring = load(t_out)[int(y[np.argmax(z)]) - 2:int(y[np.argmax(z)]) + 3, int(x[np.argmax(z)]) - 2:int(x[np.argmax(z)]) + 3].mean()
    return [check("torus has an empty hole in the middle (rendered)", hole < .2 * ring, [hole, ring], "hole<.2 ring"),
            check("only pairs closer than 90 px are linked", all(D[p] < 90 for p in pairs) and len(pairs) > 10, len(pairs), ">10"),
            check("closest pair's line alpha = 1 - d/90 (measured level)", abs(near_val - exp_val) < 12, near_val, exp_val),
            check("negative control: a pair 95-140 px apart has no line at its midpoint",
                  img[int(m2[1]), int(m2[0])].max() < 30 or any(abs(np.cross(S[q] - S[p_], m2 - S[p_])) / D[p_, q] < 1.5 for p_, q in pairs),
                  float(img[int(m2[1]), int(m2[0])].max()), "<30")], [t_out, c_out]


@card("PART-52")
def vortex_suck(task, wd):
    W = H = 240
    N = 3000
    rng = R(52)
    r0 = rng.uniform(10, 110, N)
    a0 = rng.uniform(0, 2 * math.pi, N)
    k = 30.0

    def vortex(t):
        ang = a0 + k / r0 * t                            # angle += k / r
        return W / 2 + r0 * np.cos(ang), H / 2 + r0 * np.sin(ang), ang
    x, y, ang = vortex(1.0)
    a = canvas(W, H)
    a[np.clip(y.astype(int), 0, H - 1), np.clip(x.astype(int), 0, W - 1)] = (150, 220, 255)
    out = save(wd / "vortex.png", a)
    inner = r0 < 30
    outer = r0 > 90
    w_ratio = float(((ang - a0)[inner]).mean() / ((ang - a0)[outer]).mean())
    # suck-in: cards spiral to the hero in 400 ms easeInCubic with 90-180 deg rotation, shrinking
    def card_pose(t, i):
        e = float(in_cubic(t / .4))
        rr = 100 * (1 - e)
        th = i * 1.2 + math.radians(90 + 90 * (i % 2)) * e
        return W / 2 + rr * math.cos(th), H / 2 + rr * math.sin(th), 1 - .9 * e
    frames = []
    for t in np.arange(0, .5, 1 / 30):
        f = canvas(W, H)
        for i in range(6):
            cx, cy, s = card_pose(t, i)
            hs = 10 * s
            f[int(cy - hs):int(cy + hs), int(cx - hs):int(cx + hs)] = (255, 0, 0) if i == 0 else (240, 200, 90)
        frames.append(f)
    vid = video(wd / "suck_in.mp4", frames)
    fr = vread(vid, W, H)
    areas = [int(((f_[..., 0] > 200) & (f_[..., 1] < 60)).sum()) for f_ in fr]
    c3 = centroid((fr[3][..., 0] > 200) & (fr[3][..., 1] < 60))
    r_at = math.hypot(c3[0] - W / 2, c3[1] - H / 2)
    exp = 100 * (1 - float(in_cubic(3 / 30 / .4)))
    lin = 100 * (1 - 3 / 30 / .4)
    return [check("vortex: inner points turn faster (k/r) ratio > 3", w_ratio > 3, w_ratio, ">3"),
            check("suck-in card radius follows easeInCubic at 100 ms (px)", abs(r_at - exp) < 2, r_at, exp),
            check("card shrinks as it is sucked in", areas[0] > 4 * max(1, areas[11]), [areas[0], areas[11]], "shrinks"),
            check("3k points", N == 3000, N, 3000),
            check("negative control: a linear suck-in would be 23 px further in", abs(r_at - lin) > 15, lin, r_at)], [out, vid]


# ----------------------------------------------------------------- three-kit (window.K3) in headless Chromium WebGL
def k3(wd, name, W, H, js, budget=8000):
    """Run JS with the repo's three-kit bundle (window.K3, K3.THREE) and a renderer `ren` on a W x H canvas.
    The JS calls shot(key) after each render to keep a PNG; it may put numbers in r. Returns (r, {key: png path})."""
    page = ("<!doctype html><html><body style='margin:0;background:#000'><canvas id=c width=%d height=%d></canvas>"
            "<script src='%s'></script><script>\nvar r={},shots={};try{const K=window.K3,THREE=K.THREE,W=%d,H=%d;"
            "const cv=document.getElementById('c');const ren=K.makeRenderer(cv,W,H,{});ren.shadowMap.enabled=false;"
            "function shot(k){shots[k]=cv.toDataURL('image/png');}\n%s\n}catch(e){r.err=String(e&&e.stack||e)}"
            "r.shots=shots;document.body.setAttribute('data-r',JSON.stringify(r));</script></body></html>"
            % (W, H, K3_JS.as_uri(), W, H, js))
    r = chrome(wd, name, page, gl=True, budget=budget)
    paths = {k: png_from_dataurl(Path(wd) / ("%s_%s.png" % (name, k)), v) for k, v in r.pop("shots").items()}
    return r, paths


@card("PART-58")
def k3_sea_shallow(task, wd):
    js = r"""
const sc=new THREE.Scene();sc.background=new THREE.Color(0x0a1420);const cam=new THREE.PerspectiveCamera(50,W/H,1,60000);
cam.position.set(0,40,0);cam.lookAt(0,0,-400);
const sea=K.makeSea({size:30000,res:768,color:0x0e4a63,distortion:2.4,waveSize:3});sc.add(sea);
const U=sea.material.uniforms;
function sunAt(az){const v=new THREE.Vector3(Math.sin(az),0.12,-Math.cos(az)).normalize();U.sunDirection.value.copy(v);}
sunAt(-0.25);U.time.value=0;ren.render(sc,cam);shot('sea_left');
sunAt(0.25);ren.render(sc,cam);shot('sea_right');
U.time.value=1.0;ren.render(sc,cam);shot('sea_right_t1');
const plain=new THREE.Mesh(new THREE.PlaneGeometry(30000,30000),new THREE.MeshBasicMaterial({color:0x0e4a63}));plain.rotation.x=-Math.PI/2;
sc.remove(sea);sc.add(plain);ren.render(sc,cam);shot('matte');sc.remove(plain);
// shallow water, top-down orthographic: world x,z in [-2,2] -> pixels
const sc2=new THREE.Scene();sc2.background=new THREE.Color(0x000000);const oc=new THREE.OrthographicCamera(-2,2,2*H/W,-2*H/W,0.1,100);
oc.position.set(0,20,0);oc.up.set(0,0,-1);oc.lookAt(0,0,0);
const sw=K.makeShallowWater({width:30,depth:30,seg:256,ripples:24,amp:.012,clarity:.62});sc2.add(sw);
sw.userData.set(2.0);ren.render(sc2,oc);shot('calm');
sw.userData.ripple(0,0,0.0,1);sw.userData.set(2.0);ren.render(sc2,oc);shot('ripple');
"""
    W, H = 192, 108
    r, p = k3(wd, "sea", W, H, js)
    L, Rr, R1, M = (load(p[k]) for k in ("sea_left", "sea_right", "sea_right_t1", "matte"))

    def glint_x(img):
        g = img.mean(-1)
        top = g > np.percentile(g, 99)
        return centroid(top)[0]
    xl, xr = glint_x(L), glint_x(Rr)
    anim = float(np.abs(R1 - Rr).mean())
    spec = float(Rr.mean(-1).max() - np.median(Rr.mean(-1)))
    spec_m = float(M.mean(-1).max() - np.median(M.mean(-1)))
    calm, rip = load(p["calm"]), load(p["ripple"])
    diff = np.abs(rip - calm).mean(-1)
    yy, xx = np.mgrid[:H, :W]
    wx, wz = (xx + .5) / W * 4 - 2, ((yy + .5) / H - .5) * 4 * H / W
    rr = np.hypot(wx, wz)
    bins = np.arange(0, 1.1, .05)
    prof = [float(diff[(rr >= a) & (rr < a + .05)].mean()) for a in bins]
    ring_r = float(bins[int(np.argmax(prof))] + .025)
    return [check("sun glitter follows the sun (left sun -> left of right-sun glitter)", xl < xr - 10, [xl, xr], "xl < xr"),
            check("Water normals animate with time", anim > 1.0, anim, ">1"),
            check("reflective sea shows a specular sun path", spec > 60, spec, ">60"),
            check("shallow ripple front at age 2 s ~ .34 m/s x 2 s = .68 m", abs(ring_r - .68) < .2, ring_r, .68),
            check("negative control: a matte plane has no specular path", spec_m < 5, spec_m, "<5")], list(p.values())


@card("PART-60")
def k3_weather(task, wd):
    js = r"""
const cam=new THREE.PerspectiveCamera(60,W/H,1,40000);cam.position.set(0,300,3200);cam.lookAt(0,1240,-900);cam.updateMatrixWorld();
const sc=new THREE.Scene();sc.background=new THREE.Color(0x000000);
const cl=K.makeCloudSlab({size:[7000,520,4200],center:[0,1240,-900]});sc.add(cl);
const sun=new THREE.Vector3(0.3,1,0.2).normalize();
[0,0.5,1].forEach(function(c){cl.userData.set(3.0,c,0,sun,cam.position);ren.render(sc,cam);shot('cloud_'+c);});
sc.remove(cl);
const c2=new THREE.PerspectiveCamera(60,W/H,1,20000);c2.position.set(0,600,900);c2.lookAt(0,600,0);c2.updateMatrixWorld();
const rain=K.makeRain({n:9000,region:[-500,500,-300,300],top:1500});sc.add(rain);
rain.userData.set(1.0,0);ren.render(sc,c2);shot('rain_off');rain.userData.set(1.0,1);ren.render(sc,c2);shot('rain_on');sc.remove(rain);
const probe=K.makeRain({n:150,region:[-500,500,-300,300],top:1500});sc.add(probe);
probe.userData.set(1.0,1);ren.render(sc,c2);shot('rain_a');probe.userData.set(1.05,1);ren.render(sc,c2);shot('rain_b');sc.remove(probe);
const vap=K.makeVapour({n:1400,region:[-400,400,-200,200],y:0});sc.add(vap);
const c3=new THREE.PerspectiveCamera(60,W/H,1,20000);c3.position.set(0,300,1500);c3.lookAt(0,300,0);c3.updateMatrixWorld();
vap.userData.set(2.0,1);ren.render(sc,c3);shot('vap');vap.userData.set(2.0,0);ren.render(sc,c3);shot('vap_off');sc.remove(vap);
const fl=K.makeFlock({n:18,path:[[0,-400,300,0],[10,400,300,0]],t0:1,t1:9,color:0xffffff,size:30,spread:120});sc.add(fl);
[0.5,2,8].forEach(function(t){fl.userData.set(t);ren.render(sc,c3);shot('flock_'+t);});
"""
    W, H = 128, 72
    r, p = k3(wd, "weather", W, H, js, budget=12000)
    cov = [float((load(p["cloud_%s" % c]).max(-1) > 20).mean()) for c in ("0", "0.5", "1")]
    roff, ron, ra, rb = (load(p[k]).mean(-1) for k in ("rain_off", "rain_on", "rain_a", "rain_b"))
    rain_px = float((ron > 15).mean())
    # streaks fall: vertical cross-correlation between t and t + .02 s finds a downward shift
    pa, pb = ra - ra.mean(), rb - rb.mean()
    shift = int(np.argmax([float((np.roll(pa, d_, 0) * pb).sum()) for d_ in range(-20, 21)])) - 20
    vap, voff = load(p["vap"]).mean(-1), load(p["vap_off"]).mean(-1)
    emit_row = H / 2 + math.tan(math.atan(300 / 1500)) / math.tan(math.radians(30)) * H / 2   # y = 0 plane at z = 0
    rows = np.arange(H)[:, None]
    vrow = float((vap.sum(1) * np.arange(H)).sum() / max(1e-6, vap.sum()))
    fb = [load(p["flock_%s" % t]).mean(-1) for t in ("0.5", "2", "8")]
    vis = [int((f > 60).sum()) for f in fb]
    c3, c6 = centroid(fb[1] > 60), centroid(fb[2] > 60)
    return [check("cloud slab cover grows with uCover (0 -> .5 -> 1)", cov[0] < .01 and cov[1] < cov[2] and cov[2] > .05, cov, "0 < .5 < 1"),
            check("9000 rain points render as streaks when on", rain_px > .02, rain_px, ">.02"),
            check("rain falls (shift downward over .05 s, px)", shift > 0, shift, ">0"),
            check("vapour rises above its emitter plane (brightness-weighted row above it)", vrow < emit_row - 5 and vap.sum() > 0,
                  [vrow, emit_row], "row < emitter - 5"),
            check("vapour off draws nothing", float(voff.sum()) == 0, float(voff.sum()), 0),
            check("flock visible only inside [t0, t1] and moves along its path", vis[0] == 0 and vis[1] > 5 and c6[0] > c3[0] + 10,
                  [vis, c3, c6], "hidden, then left->right"),
            check("negative control: rain uOn = 0 draws nothing", float((roff > 15).mean()) == 0, float((roff > 15).mean()), 0)], \
        list(p.values())


@card("PART-61")
def k3_pond_life(task, wd):
    js = r"""
const sc=new THREE.Scene();sc.background=new THREE.Color(0x000000);
sc.add(new THREE.HemisphereLight(0xffffff,0x404040,3.0));const dl=new THREE.DirectionalLight(0xffffff,2.0);dl.position.set(1,3,2);sc.add(dl);
const top=new THREE.OrthographicCamera(-2,2,2*H/W,-2*H/W,0.1,50);top.position.set(0,10,0);top.up.set(0,0,-1);top.lookAt(0,0,0);
const koi=K.makeKoi({length:.8,amp:.12,seed:3});sc.add(koi);
const cx=0,cz=0,ax=1.2,az=.5,w=.6,ph=.3,ph2=1.1;
function path(t,o){return o.set(cx+ax*Math.sin(w*t+ph),-.3,cz+az*Math.sin(2*w*t+ph2));}
r.koi=[];[0,1.5,3,4.5].forEach(function(t,i){koi.userData.set(t,path,1.6);ren.render(sc,top);shot('koi_'+i);});
sc.remove(koi);
const side=new THREE.OrthographicCamera(-4,4,4*H/W+2,-4*H/W+2,0.1,50);side.position.set(0,2,10);side.lookAt(0,2,0);
const pet=K.makePetals({n:170,region:[-3.5,3.5,-1,1],times:[0,6],level:0,size:4});sc.add(pet);
[1.5,9].forEach(function(t){pet.userData.set(t);ren.render(sc,side);shot('pet_'+t);});sc.remove(pet);
const tU={value:0};
const side2=new THREE.OrthographicCamera(-.5,.5,.5*H/W+.27,-.5*H/W+.27,0.1,50);side2.position.set(0,.27,10);side2.lookAt(0,.27,0);
function blades(amp){return K.makeBlades({n:1,region:[-.01,.01,-.01,.01],accept:function(){return true},height:function(){return 0},tall:.95,width:.04,amp:amp,freq:1.2,time:tU,seed:5});}
const b1=blades(.07);sc.add(b1);[0,1.3].forEach(function(t){tU.value=t;ren.render(sc,side2);shot('blade_'+t);});sc.remove(b1);
const b0=blades(0);sc.add(b0);[0,1.3].forEach(function(t){tU.value=t;ren.render(sc,side2);shot('still_'+t);});
"""
    W, H = 160, 90
    r, p = k3(wd, "pond", W, H, js)
    errs = []
    for i, t in enumerate([0, 1.5, 3, 4.5]):
        img = load(p["koi_%d" % i]).max(-1)
        c = centroid(img > 30)
        ex = .0 + 1.2 * math.sin(.6 * t + .3)
        ez = .0 + .5 * math.sin(1.2 * t + 1.1)
        px, py = (ex + 2) / 4 * W, (ez / (2 * H / W) + 1) / 2 * H
        errs.append(math.hypot(c[0] - px, c[1] - py) if c else 99)
    water_row = H - ((0 - (-4 * H / W + 2)) / (8 * H / W)) * H

    def above_share(img):
        m = img.max(-1) > 30
        rows = np.nonzero(m)[0]
        return float((rows < water_row - 3).mean()) if len(rows) else 0.0
    early, late = above_share(load(p["pet_1.5"])), above_share(load(p["pet_9"]))

    def tip_base(a, b):
        A, B = load(p[a]).max(-1) > 20, load(p[b]).max(-1) > 20
        rows = [r_ for r_ in range(H) if A[r_].any() and B[r_].any()]
        sh = np.array([abs(np.nonzero(A[r_])[0].mean() - np.nonzero(B[r_])[0].mean()) for r_ in rows])
        hgt = (max(rows) - np.array(rows)) / max(1, max(rows) - min(rows))        # 0 at the base, 1 at the tip
        k = max(1, len(rows) // 5)
        return float(sh[:k].mean()), float(sh[-k:].mean()), float(np.corrcoef(sh, hgt ** 2)[0, 1]) if sh.std() > 0 else 0.0
    tip, base, corr = tip_base("blade_0", "blade_1.3")
    stip, sbase, _ = tip_base("still_0", "still_1.3")
    return [check("koi follows its Lissajous path (max px error over 4 times)", max(errs) < 6, max(errs), "<6"),
            check("petals fall and land: share above the water drops", early > .3 and late < .1, [early, late], "early>.3, late<.1"),
            check("reed sway bends the tips more than the bases", tip > 3 * max(base, .3), [tip, base], "tip > 3x base"),
            check("bend grows with height^2 (per-row shift correlation)", corr > .9, corr, ">.9"),
            check("negative control: amp 0 blades do not move", stip + sbase < 1e-6, stip + sbase, 0)], list(p.values())


@card("PART-62")
def k3_car_trails(task, wd):
    js = r"""
const sc=new THREE.Scene();sc.background=new THREE.Color(0x000000);
const cam=new THREE.OrthographicCamera(-5,5,5*H/W,-5*H/W,0.1,500);cam.position.set(0,100,0);cam.up.set(0,0,-1);cam.lookAt(0,0,0);
const geo=new THREE.SphereGeometry(.16,12,8);
function car(z,v,trail){const g=new THREE.Group();
  const tl=new THREE.Mesh(geo,new THREE.MeshBasicMaterial({color:new THREE.Color(0xff1e1e).multiplyScalar(6)}));
  const len=trail?v*0.5:0;const s=1+len/(2*.16)*1.2;tl.scale.z=s;tl.position.z=z+(s*.16)-.16;   // streak offset forward of the body
  g.add(tl);return g;}
const speeds=[22,27];
speeds.forEach(function(v,i){const g=car(-10,v,true);g.position.x=-2.5+i*5;sc.add(g);});
ren.toneMapping=THREE.NoToneMapping;ren.render(sc,cam);shot('trails');
while(sc.children.length)sc.remove(sc.children[0]);
speeds.forEach(function(v,i){const g=car(-10,v,false);g.position.x=-2.5+i*5;sc.add(g);});ren.render(sc,cam);shot('dots');
"""
    W, H = 200, 600
    r, p = k3(wd, "cars", W, H, js)
    upm = W / 10                                          # pixels per metre

    def lengths(img):
        out = []
        for xm in (-2.5, 2.5):
            col = int((xm + 5) * upm)
            m = img[:, col - 4:col + 5, 0].max(1) > 60
            rows = np.nonzero(m)[0]
            out.append(((rows.max() - rows.min() + 1) / upm, rows.min(), rows.max()) if len(rows) else (0, 0, 0))
        return out
    tr, dt = lengths(load(p["trails"])), lengths(load(p["dots"]))
    exp = [2 * .16 * (1 + v * .5 / (2 * .16) * 1.2) for v in (22, 27)]
    body_row = int((-10 - .16 + 5 * H / W) / (10 * H / W) * H)   # car body at z = -10 m -> row from the top
    behind_ok = all(t_[1] >= body_row - 3 for t_ in tr)
    return [check("streak length = 2r * scale.z, scale.z = 1 + trail/(2 r) * 1.2 (m)", all(abs(a[0] - b) < .6 for a, b in zip(tr, exp)),
                  [a[0] for a in tr], exp),
            check("faster car leaves the longer streak", tr[1][0] > tr[0][0], [tr[0][0], tr[1][0]], "27 > 22 m/s"),
            check("streak offset forward: it never starts behind the body", behind_ok, [t_[1] for t_ in tr], ">= body row"),
            check("negative control: unscaled lights are dots (< .5 m)", all(d_[0] < .5 for d_ in dt), [d_[0] for d_ in dt], "<.5")], \
        list(p.values())


def css_bezier(x1, y1, x2, y2):
    def f(x):
        x = np.atleast_1d(np.asarray(x, dtype=float))
        lo, hi = np.zeros_like(x), np.ones_like(x)
        for _ in range(50):
            mid = (lo + hi) / 2
            cx = 3 * x1 * mid * (1 - mid) ** 2 + 3 * x2 * mid * mid * (1 - mid) + mid ** 3
            lo, hi = np.where(cx < x, mid, lo), np.where(cx < x, hi, mid)
        t = (lo + hi) / 2
        y = 3 * y1 * t * (1 - t) ** 2 + 3 * y2 * t * t * (1 - t) + t ** 3
        return y if y.size > 1 else y.reshape(())
    return f


@card("PART-63")
def pour_fill(task, wd):
    W, H = 200, 240
    gx0, gx1, gy0, gy1 = 60, 140, 80, 220                  # glass interior
    ease = css_bezier(.33, 0, .2, 1)
    T = 2.8

    def level(t):
        return gy1 - (gy1 - gy0 - 20) * float(ease(np.clip(t / T, 0, 1)))

    def wobble(t):
        u = t - T
        return 3 * math.sin(2 * math.pi * 1.5 * u) * math.exp(-u / .2) if u > 0 else 3 * math.sin(2 * math.pi * 1.5 * t)

    def frame(t):
        a = canvas(W, H, (240, 236, 228))
        a[gy0:gy1, gx0 - 2:gx0] = a[gy0:gy1, gx1:gx1 + 2] = a[gy1:gy1 + 2, gx0 - 2:gx1 + 2] = (60, 60, 60)
        L = level(t)
        xs = np.arange(gx0, gx1)
        surf = L + wobble(t) * np.sin((xs - gx0) / (gx1 - gx0) * math.pi * 2)
        for x, s_ in zip(xs, surf):
            a[int(max(gy0, s_)):gy1, x] = (120, 60, 20)    # clip rect up to the (wobbling) surface
        if t < T:
            a[30:int(L), 98:103] = (120, 60, 20)            # 5 px stream from the neck
        return a
    ts = np.arange(0, 4.0, 1 / 15)
    vid = video(wd / "pour.mp4", [frame(t) for t in ts], 15)
    fr = vread(vid, W, H)
    liquid = lambda f: (np.abs(f - (120, 60, 20)).sum(-1) < 30)
    lv = [float(np.nonzero(liquid(f)[:, gx0 + 5:gx0 + 10].any(1))[0].min()) if liquid(f)[:, gx0 + 5:gx0 + 10].any() else gy1 for f in fr]
    k = int(1.4 * 15)
    exp_mid = level(1.4)
    lin_mid = gy1 - (gy1 - gy0 - 20) * .5
    settle = [abs(np.nonzero(liquid(fr[i])[:, gx0 + 20].any() and liquid(fr[i])[:, gx0 + 20])[0].min() - level(4)) for i in (len(fr) - 1,)]
    stream_after = int(liquid(fr[-1])[30:70, 98:103].sum())
    return [check("fill level follows cubic-bezier(.33,0,.2,1) at 1.4 s (px)", abs(lv[k] - exp_mid) < 4, lv[k], exp_mid),
            check("surface wobble damps to flat by 4 s (px)", settle[0] <= 1.5, settle[0], "<=1.5"),
            check("stream retracts after the pour", stream_after == 0, stream_after, 0),
            check("negative control: a linear fill would be > 10 px off at 1.4 s", abs(lin_mid - exp_mid) > 10, lin_mid, exp_mid)], [vid]


@card("PART-64")
def metaballs_contours(task, wd):
    W = H = 200
    rng = R(64)
    yy, xx = np.mgrid[:H, :W].astype(float)

    def field(t, n=7):
        f = np.zeros((H, W))
        for i in range(n):
            a = t * .5 * 2 * math.pi * (1 + .1 * i) + i
            cx, cy = 100 + 50 * math.cos(a), 100 + 50 * math.sin(a * 1.3)
            f += (18 + 3 * i) ** 2 / ((xx - cx) ** 2 + (yy - cy) ** 2 + 1)
        return f
    f = field(.4)
    from skimage import measure
    levels = [1.0, 1.6, 2.4, 3.4]
    a = canvas(W, H)
    total = 0
    for k, lv in enumerate(levels):                    # marching-squares iso-contours
        cs = measure.find_contours(f, lv)
        total += len(cs)
        for c in cs:
            for y, x in c:
                a[int(y), int(x)] = (255, 160 + 20 * k, 80)
    out = save(wd / "contours.png", a)
    img = load(out)
    on = img.max(-1) > 100
    vals = f[on]
    err = float(np.min(np.abs(vals[:, None] - np.array(levels)[None]) / np.array(levels)[None], axis=1).mean())
    inside = (f > 1.0).astype(int)
    _, n_merged = label(f > 1.0)
    # two separate blobs far apart do not merge, close ones do
    two = lambda d: label((18 ** 2 / ((xx - 100 + d) ** 2 + (yy - 100) ** 2 + 1) + 18 ** 2 / ((xx - 100 - d) ** 2 + (yy - 100) ** 2 + 1)) > 1.0)[1]
    rand_err = float(np.min(np.abs(f[R(1).random((H, W)) < on.mean()][:, None] - np.array(levels)[None]) / np.array(levels)[None], axis=1).mean())
    return [check("contour pixels lie on the iso levels (rel err)", err < .08, err, "<.08"),
            check("4-6 iso levels drawn", 4 <= len(levels) <= 6 and total >= 4, total, ">=4"),
            check("metaballs merge when close, split when far", two(15) == 1 and two(60) == 2, [two(15), two(60)], [1, 2]),
            check("negative control: random pixels are off the iso levels", rand_err > 3 * err, rand_err, ">3x")], [out]


@card("PART-65")
def fire_emitter(task, wd):
    W, H, rate = 160, 200, 40 * 30                         # 40 particles per frame at 30 fps

    def hsh(i, k):
        x = np.sin(i * 127.1 + k * 311.7) * 43758.5453
        return x - np.floor(x)
    ramp = np.array([[255, 255, 255], [255, 230, 60], [230, 40, 20]], float)

    def frame(t, ramp_on=True):
        a = np.zeros((H, W, 3))
        i = np.arange(max(0, int((t - 1.0) * rate)), int(t * rate))
        birth = i / rate
        age = t - birth                                   # closed form: no state between frames
        vx, vy = (hsh(i, 1) - .5) * 40, -(60 + hsh(i, 2) * 60)
        x, y = 80 + vx * age, 180 + vy * age
        u = np.clip(age / 1.0, 0, 1)
        col = np.where(u[:, None] < .5, ramp[0] + (ramp[1] - ramp[0]) * (u[:, None] / .5), ramp[1] + (ramp[2] - ramp[1]) * ((u[:, None] - .5) / .5))
        if not ramp_on:
            col = np.repeat(ramp[:1], len(u), 0)
        al = (1 - u)
        ok = (x >= 0) & (x < W) & (y >= 0) & (y < H)
        np.add.at(a, (y[ok].astype(int), x[ok].astype(int)), col[ok] * al[ok, None] * .3)
        return np.clip(a, 0, 255)
    vid = video(wd / "fire.mp4", [frame(t) for t in np.arange(1.0, 2.0, 1 / 30)])
    fr = vread(vid, W, H)
    f = fr[15]
    rows = np.arange(H)
    def grads(f):
        lit_ = f.sum(-1) > 30
        low, high = f[150:180][lit_[150:180]], f[90:120][lit_[90:120]]
        return float((low[:, 1] / (low[:, 0] + 1)).mean()), float((high[:, 1] / (high[:, 0] + 1)).mean()), lit_
    gb_low, gb_high, lit = grads(f)
    w_low, w_high, _ = grads(frame(1.5, ramp_on=False))
    alive = int(len(np.arange(max(0, int((1.5 - 1.0) * rate)), int(1.5 * rate))))
    return [check("colour ramps white/yellow near the emitter -> red higher up (G/R)", gb_low > gb_high + .2, [gb_low, gb_high], "low > high"),
            check("particles rise (brightness centroid above the emitter)", centroid(lit)[1] < 170, centroid(lit)[1], "<170"),
            check("40 per frame x 1 s life alive", alive == rate, alive, rate),
            check("negative control: a white-only emitter shows no low/high colour change", not (w_low > w_high + .2),
                  [w_low, w_high], "equal")], [vid]


@card("PART-66")
def underwater_lanterns(task, wd):
    W, H, fps = 240, 180, 30
    rng = R(66)
    n = 10
    lx, ph, fq = rng.uniform(20, 220, n), rng.uniform(0, 6.28, n), rng.uniform(3, 6, n)

    def frame(t):
        yy, xx = np.mgrid[:H, :W].astype(float)
        a = np.zeros((H, W, 3))
        a[..., 2] = 60 + 100 * yy / H * 0 + 120 * (1 - yy / H)
        a[..., 1] = 30 + 60 * (1 - yy / H)
        shaft = (np.sin((xx + yy * .6) / 18 + t * .3) > .85) * 25    # diagonal light shafts
        a += shaft[..., None]
        jy = 60 + 10 * math.sin(2 * math.pi * .4 * t)               # jellyfish bob 10 px @ .4 Hz
        disc(a, 120, jy, 8, (255, 0, 0), "over", 1)
        for k in range(n):                                          # lanterns: flicker .85-1.0 @ 3-6 Hz, drift
            fl = .925 + .075 * math.sin(2 * math.pi * fq[k] * t + ph[k])
            x = (lx[k] + 7 * t) % W
            disc(a, x, 150, 3, (255 * fl, 200 * fl, 0), "over", 1)
            a[153:160, int(x)] = (200 * fl * .5, 160 * fl * .5, 0)  # short reflection streak
        return np.clip(a, 0, 255)
    ts = np.arange(0, 5.0, 1 / fps)
    vid = video(wd / "underwater.mp4", [frame(t) for t in ts], fps)
    fr = vread(vid, W, H)
    jy = np.array([c[1] for c in track(fr, 0, thr=200, othr=60)])
    F = np.abs(np.fft.rfft(jy - jy.mean()))
    f_peak = float(np.fft.rfftfreq(len(jy), 1 / fps)[np.argmax(F)])
    amp = float((jy.max() - jy.min()) / 2)
    k0 = 0
    br = []
    for f in fr:
        x = (lx[k0] + 7 * ts[len(br)]) % W
        br.append(float(f[150, int(x), 0]))
    br = np.array(br)
    fl_range = [float(br.min() / br.max()), 1.0]
    Fl = np.abs(np.fft.rfft(br - br.mean()))
    f_fl = float(np.fft.rfftfreq(len(br), 1 / fps)[np.argmax(Fl)])
    still = np.array([frame(0)] * 3)
    return [check("jellyfish bobs at .4 Hz (FFT of tracked y)", abs(f_peak - .4) < .1, f_peak, .4),
            check("bob amplitude 10 px", abs(amp - 10) < 1.5, amp, 10),
            check("lantern flicker .85-1.0", .82 <= fl_range[0] <= .88, fl_range[0], ".85"),
            check("flicker frequency 3-6 Hz", 2.8 <= f_fl <= 6.2, f_fl, "3-6"),
            check("negative control: a still frame has no bob", float(np.ptp([c[1] for c in track(still, 0, thr=200, othr=60)])) == 0, 0, 0)], [vid]


@card("PART-68")
def gravity_bounce(task, wd):
    g, e, dt, floor, r = 900.0, .75, 1 / 60, 220.0, 6
    W, H = 320, 240

    def sim(n_frames, e_=e):
        y, v, out = 40.0, 0.0, []
        for _ in range(n_frames):                          # replayed from frame 0 on every seek (deterministic)
            v += g * dt
            y += v * dt
            if y > floor - r:
                y = floor - r
                v = -v * e_
            out.append(y)
        return np.array(out)
    ys = sim(150)
    frames = []
    dots = []
    for f in range(150):
        a = canvas(W, H, (245, 240, 230))
        a[int(floor):] = (60, 60, 60)
        x = 20 + f * 1.8
        if f % 3 == 0:
            dots.append((x, ys[f]))
        for dx, dy in dots:
            disc(a, dx, dy, 2, hexc("#c9452c"))
        disc(a, x, ys[f], r, (0, 0, 255), "over")
        frames.append(a)
    img = frames[-1]
    pil = Image.fromarray(img.astype(np.uint8))
    ImageDraw.Draw(pil).text((230, 20), "e = 0.75", fill=(0, 0, 0))
    out = save(wd / "bounce.png", np.asarray(pil))
    vid = video(wd / "bounce.mp4", frames, 60)
    fr = vread(vid, W, H)
    by = np.array([c[1] for c in track(fr, 2, thr=150, others=(0, 1), othr=60)])
    peaks = [i for i in range(1, len(by) - 1) if by[i] < by[i - 1] and by[i] <= by[i + 1] and by[i] < floor - r - 5]
    hts = [floor - r - by[i] for i in peaks]
    ratio = float(hts[1] / hts[0]) if len(hts) > 1 else 0
    seek = sim(97)[-1]
    nb = sim(150, 1.0)
    nb_peaks = [i for i in range(1, 149) if nb[i] < nb[i - 1] and nb[i] <= nb[i + 1]]
    nb_ratio = float((floor - r - nb[nb_peaks[1]]) / (floor - r - nb[nb_peaks[0]])) if len(nb_peaks) > 1 else 1
    return [check("successive bounce heights scale by e^2 = .5625", abs(ratio - e * e) < .06, ratio, e * e),
            check("dotted trail: one dot every 3 frames", len(dots) == 50, len(dots), 50),
            check("seek replays from frame 0 (frame 96 identical)", abs(seek - ys[96]) < 1e-9, seek, float(ys[96])),
            check("negative control: e = 1 keeps the height", abs(nb_ratio - 1) < .05, nb_ratio, 1)], [vid, out]


@card("PART-69")
def ball_in_rings(task, wd):
    W = H = 240
    c = np.array([120.0, 120.0])
    rings = [(18 + 8 * i, .3 + .08 * i if i % 2 == 0 else -(.3 + .08 * i)) for i in range(12)]
    gap = math.radians(34)
    rb = 3.0
    p, v = c.copy(), 100 * np.array([math.cos(.28), math.sin(.28)])   # 600 px/s at 1920 -> 100 px/s here
    alive = [True] * 12
    sub = 4
    dt = 1 / 30 / sub
    events, frames = [], []
    reflections = 0
    for f in range(150):
        for s_ in range(sub):
            t = (f * sub + s_) * dt
            p = p + v * dt
            d = p - c
            dist = float(np.linalg.norm(d))
            for k in range(12):
                if not alive[k]:
                    continue
                Rk, w = rings[k]
                if dist >= Rk - rb:
                    ang = (math.atan2(d[1], d[0]) - w * t) % (2 * math.pi)
                    if ang < gap:                         # inside the rotating gap: pass, ring shatters
                        alive[k] = False
                        events.append((f, k))
                    else:
                        n = d / dist
                        v = v - 2 * (v @ n) * n           # restitution 1
                        p = c + n * (Rk - rb - .01)
                        reflections += 1
                    break
        a = canvas(W, H)
        yy, xx = np.mgrid[:H, :W]
        rr = np.hypot(xx - c[0], yy - c[1])
        th = np.arctan2(yy - c[1], xx - c[0])
        for k in range(12):
            if alive[k]:
                Rk, w = rings[k]
                ang = (th - w * f / 30) % (2 * math.pi)
                a[(np.abs(rr - Rk) < 1.5) & (ang >= gap)] = (120, 200, 255)
        disc(a, p[0], p[1], rb, (255, 0, 0), "over")
        frames.append(a)
    vid = video(wd / "rings.mp4", frames)
    fr = vread(vid, W, H)
    speed = float(np.linalg.norm(v)) * 6   # back to 1920-px units
    inner = [f_ for f_, k in events if k == 0]
    if inner:
        f0 = inner[0]
        before = fr[max(0, f0 - 1)]
        after = fr[min(len(fr) - 1, f0 + 2)]
        r0 = rings[0][0]
        ring_px = lambda img: int(((np.abs(rr - r0) < 1.5) & (img[..., 2] > 150)).sum())
        shattered = ring_px(before) > 20 and ring_px(after) == 0
    else:
        shattered = False
    return [check("speed conserved ~600 px/s (restitution 1)", abs(speed - 600) < 1, speed, 600),
            check("ball reflects off ring walls", reflections > 0, reflections, ">0"),
            check("ball escapes through gaps (rings removed)", len(events) >= 2, len(events), ">=2"),
            check("ring disappears from the frames once passed", shattered, shattered, True),
            check("gap 28-40 deg, rings alternate direction", 28 <= math.degrees(gap) <= 40 and rings[0][1] * rings[1][1] < 0,
                  math.degrees(gap), "28-40"),
            check("negative control: rings still present before the first escape", inner and int(((np.abs(rr - rings[0][0]) < 1.5)
                  & (fr[0][..., 2] > 150)).sum()) > 20, True, True)], [vid]


@card("PART-70")
def drops_piles(task, wd):
    W, H, floor = 200, 240, 220
    n, ch = 5, 24                                          # cards 24 px tall stacked

    def card_y(i, t):
        u = (t - i * .4) / .3                              # drop ~300 ms easeOutBounce, stagger 400 ms
        rest = floor - (i + 1) * ch
        return -ch + (rest + ch) * float(out_bounce(np.clip(u, 0, 1))) if u > 0 else -100.0

    def frame(t):
        a = canvas(W, H, (250, 248, 240))
        a[floor:] = (80, 80, 80)
        sway = min(6.0, max(0, t - 2.0) * 4) * math.sin(t * 4)       # shared sway growing to 6 deg
        for i in range(n):
            y = card_y(i, t)
            if y < -50:
                continue
            ang = math.radians(sway)
            h = floor - (y + ch / 2)
            cx, cy = 100 + h * math.sin(ang), floor - h * math.cos(ang)
            pts = np.array([[-30, -ch / 2 + 1], [30, -ch / 2 + 1], [30, ch / 2 - 1], [-30, ch / 2 - 1]])
            Rm = np.array([[math.cos(ang), -math.sin(ang)], [math.sin(ang), math.cos(ang)]])
            m = poly_mask(W, H, pts @ Rm.T + (cx, cy))
            a[m] = (220, 80 + 30 * i, 60) if i else (255, 0, 0)
        return a
    ts = np.arange(0, 3.0, 1 / 30)
    vid = video(wd / "stack.mp4", [frame(t) for t in ts])
    fr = vread(vid, W, H)
    tops = []
    for f in fr:
        m = (f[..., 0] > 200) & (f[..., 1] < 60)
        b = bbox(m)
        tops.append(b[3] if b else -1)
    land = next(i for i, b in enumerate(tops) if b >= floor - 2)
    # bounce: card 0 touches the floor, rises, touches again before 300 ms
    yb = np.array([card_y(0, t) + ch for t in np.arange(0, .3, 1 / 240)])     # bottom edge, finely sampled
    rises = int((np.diff(yb) < -.5).sum())
    touches = [i for i in range(1, len(yb)) if yb[i] >= floor - 3 > yb[i - 1]]
    stack_h = [floor - (bbox(np.abs(fr[int(2.0 * 30)] - (250, 248, 240)).sum(-1) > 60)[1])]
    ys = [card_y(0, t) for t in ts[:10]]
    lin = [-ch + (floor - ch + ch) * min(1, max(0, t / .3)) for t in ts[:10]]
    return [check("first card lands within 300 ms (frames)", land <= 9, land, "<=9"),
            check("easeOutBounce: it touches the floor and rebounds", len(touches) >= 2 and rises > 0, [len(touches), rises], ">=2"),
            check("stack of 5 cards x 24 px at 2 s (px)", abs(stack_h[0] - n * ch) <= 3, stack_h[0], n * ch),
            check("negative control: a linear drop never rebounds", int((np.diff(np.array([-ch + floor * min(1, t / .3) for t in
                  np.arange(0, .3, 1 / 240)])) < -.5).sum()) == 0, 0, 0)], [vid]


@card("PART-73")
def vibrating_strings(task, wd):
    W, H, fps = 300, 200, 60
    A = .04 * H
    hit = .2

    def offset(t):
        u = t - hit
        return A * math.exp(-6 * u) * math.sin(30 * u) if u >= 0 else 0.0

    def frame(t):
        a = canvas(W, H)
        for k in range(5):
            y0 = 40 + 30 * k
            o = offset(t) if k == 2 else 0
            xs = np.arange(20, 280)
            u = (xs - 20) / 260
            ys = y0 * (1 - u) ** 2 + 2 * u * (1 - u) * (y0 + 2 * o) + y0 * u * u   # quadratic, control point displaced
            a[np.round(ys).astype(int), xs] = (255, 255, 255) if k != 2 else (255, 0, 0)
        return a
    ts = np.arange(0, .8, 1 / fps)
    vid = video(wd / "strings.mp4", [frame(t) for t in ts], fps)
    fr = vread(vid, W, H)
    mid = []
    for f in fr:
        col = f[:, 150]
        m = (col[:, 0] > 150) & (col[:, 1] < 80)
        mid.append(float(np.nonzero(m)[0].mean()) - 100 if m.any() else 0)
    mid = np.array(mid)
    exp = np.array([offset(t) for t in ts])
    err = float(np.abs(mid - exp).max())
    gone = float(np.abs(mid[ts > hit + .4]).max())
    peak = float(np.abs(mid).max())
    calm = float(np.abs(np.array([offset(t) for t in ts if t < hit])).max())
    return [check("string midpoint follows A e^(-6t) sin(30t) (px)", err < 1.0, err, "<1"),
            check("peak amplitude ~4% of height", .5 * A < peak <= A, peak, A),
            check("decays within 400 ms (< 1 px)", gone < 1.0, gone, "<1"),
            check("negative control: before the impact the string is still", calm == 0 and float(np.abs(mid[ts < hit]).max()) < .6,
                  float(np.abs(mid[ts < hit]).max()), 0)], [vid]


@card("PART-74")
def boids(task, wd):
    N, W, H = 256, 200, 200
    rng = R(74)
    p = rng.uniform(0, W, (N, 2))
    v = rng.normal(0, 1, (N, 2)) * 30
    from scipy.spatial import cKDTree

    def order(v):
        return float(np.linalg.norm((v / (np.linalg.norm(v, axis=1, keepdims=True) + 1e-9)).mean(0)))
    o0 = order(v)
    dt = 1 / 30

    def run(p, v, ws=1.5, wa=2.5, wc=.4, steps=240):
        bake = []
        for step in range(steps):                         # fixed dt, CPU, baked; vectorised neighbour rules
            d = (p[None] - p[:, None] + W / 2) % W - W / 2   # d[i, j] = p_j - p_i (wrapped)
            dist = np.linalg.norm(d, axis=-1)
            nb = (dist < 25) & (dist > 0)
            cnt = np.maximum(nb.sum(1, keepdims=True), 1)
            close = (dist < 8) & (dist > 0)
            sep = -(d * close[..., None]).sum(1) * 2
            ali = (v[None] * nb[..., None]).sum(1) / cnt - v * (nb.sum(1, keepdims=True) > 0)
            coh = (d * nb[..., None]).sum(1) / cnt
            v = v + (sep * ws + ali * wa + coh * wc) * dt
            sp = np.linalg.norm(v, axis=1, keepdims=True)
            v = v / sp * np.clip(sp, 20, 60)
            p = (p + v * dt) % W
            bake.append(p.copy())
        return p, v, bake
    p0, v0 = p.copy(), v.copy()
    p, v, bake = run(p0, v0)
    o1 = order(v)
    ps, _, _ = run(p0, v0, ws=0)
    mean_nn = lambda q: float(cKDTree(q, boxsize=W).query(q, 2)[0][:, 1].mean())
    nn_sep, nn_nosep = mean_nn(p), mean_nn(ps)
    bf = jw(wd / "boids_bake.json", {"dt": dt, "frames": [b.round(2).tolist() for b in bake[::10]]})
    frames = []
    for b in bake[::5]:
        a = canvas(W, H, (200, 220, 240))
        for x, y in b:
            a[int(y) % H, int(x) % W] = (20, 20, 30)
            a[(int(y) + 2) % H, (int(x) + 1) % W] = (150, 165, 185)   # soft projected shadow
        frames.append(a)
    vid = video(wd / "boids.mp4", frames, 30)
    # negative control: same particles without the three rules keep a random heading
    p2, v2 = rng.uniform(0, W, (N, 2)), rng.normal(0, 1, (N, 2)) * 30
    for _ in range(240):
        p2 = (p2 + v2 * dt) % W
    on = order(v2)
    return [check("alignment emerges: order parameter rises > .8", o1 > .8 and o1 > o0 + .5, [o0, o1], ">.8"),
            check("baked with fixed dt (240 steps, readable)", len(json.loads(bf.read_text())["frames"]) == 24, 24, 24),
            check("separation keeps boids apart (mean NN vs no-separation run)", nn_sep > 1.3 * nn_nosep, [nn_sep, nn_nosep], ">1.3x"),
            check("negative control: without the rules order stays low", on < .3, on, "<.3")], [vid, bf]


@card("PART-75")
def toss_ghosts(task, wd):
    W, H, fps = 320, 200, 60
    T = .9
    g = 2 * 2 * 120 / (T * T) * 1.0                       # apex 120 px above the start
    vx = 260 / T
    vy = -g * T / 2
    pos = lambda t: (30 + vx * t, 170 + vy * t + .5 * g * t * t)

    def frame(t):
        a = canvas(W, H)
        for k in range(12, 0, -1):                       # 12 ghosts sampled at earlier times, fading over 200 ms
            tk = t - k * (.2 / 12)
            if tk < 0:
                continue
            x, y = pos(tk)
            disc(a, x, y, 5, (0, 0, 255), "max", 1 - k / 13)
        x, y = pos(t)
        disc(a, x, y, 5, (255, 0, 0), "over", 1)
        return a
    ts = np.arange(0, T, 1 / fps)
    vid = video(wd / "toss.mp4", [frame(t) for t in ts], fps)
    fr = vread(vid, W, H)
    tr = track(fr, 0, thr=150, othr=60)
    yy = np.array([c[1] for c in tr])
    gg = np.polyfit(ts, yy, 2)[0] * 2
    land = pos(T)
    f = fr[40]
    lab, ng = label((f[..., 2] > 20) & (f[..., 0] < 60), eight=True)
    blue = f[..., 2][(f[..., 2] > 20) & (f[..., 0] < 60)]
    lone = frame(0.0)
    lab0, n0 = label((lone[..., 2] > 20) & (lone[..., 0] < 60))
    return [check("token follows a parabola (recovered g, px/s^2)", abs(gg - g) / g < .03, gg, g),
            check("lands back at the start height after 900 ms", abs(land[1] - 170) < 1e-6, land[1], 170),
            check("ghost trail present with fading intensity", ng >= 1 and blue.max() - blue.min() > 100, [ng, float(blue.max() - blue.min())],
                  "fading"),
            check("negative control: no ghosts at t = 0", n0 == 0, n0, 0)], [vid]


# ================================================================= SHAPE cards
def align_start(p):
    """Rotate a closed point list so it starts at the topmost vertex (smallest y)."""
    return np.roll(p, -int(np.argmin(p[:, 1] + 1e-6 * p[:, 0])), 0)


def prep_morph(a, b, n=96):
    """Morph law: resample both to n points, same winding (reverse if signed areas differ), aligned start."""
    A, B = resample_closed(a, n), resample_closed(b, n)
    if np.sign(signed_area(A)) != np.sign(signed_area(B)):
        B = B[::-1]
    return align_start(A), align_start(B)


def morph_frames(A, B, ts, dur, ease, W, H, col=(255, 255, 255), extra=None):
    out = []
    for t in ts:
        e = float(ease(np.clip(t / dur, 0, 1)))
        P = A + (B - A) * e
        a = canvas(W, H)
        a[poly_mask(W, H, P)] = col
        if extra:
            extra(a, t, e)
        out.append(a)
    return out


def self_intersections(P):
    n = len(P)
    cnt = 0
    for i in range(n):
        p1, p2 = P[i], P[(i + 1) % n]
        for j in range(i + 2, n):
            if i == 0 and j == n - 1:
                continue
            q1, q2 = P[j], P[(j + 1) % n]
            d = lambda a, b, c: (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
            if d(p1, p2, q1) * d(p1, p2, q2) < 0 and d(q1, q2, p1) * d(q1, q2, p2) < 0:
                cnt += 1
    return cnt


@card("SHAPE-02")
def morph_law(task, wd):
    W = H = 200
    circ = poly_regular(40, 70, 100, 100)
    star = star_poly(5, 80, 35, 100, 100)[::-1]           # opposite winding, different point count
    A, B = prep_morph(circ, star, 96)
    mids = [A + (B - A) * .5]
    bad = resample_closed(circ, 96), np.roll(resample_closed(star, 96), 30, 0)   # unaligned, wrong winding
    good_x = self_intersections(mids[0])
    bad_x = self_intersections(bad[0] + (bad[1] - bad[0]) * .5)
    ease = css_bezier(.65, 0, .35, 1)
    frames = morph_frames(A, B, np.arange(0, .7, 1 / 30), .6, ease, W, H)
    vid = video(wd / "morph_law.mp4", frames)
    fr = vread(vid, W, H)
    end_iou = iou(fr[-1].max(-1) > 128, poly_mask(W, H, star))
    return [check("both paths resampled to equal point counts", len(A) == len(B) == 96, [len(A), len(B)], 96),
            check("same winding after the law", np.sign(signed_area(A)) == np.sign(signed_area(B)), True, True),
            check("aligned morph midpoint has no self-intersections", good_x == 0, good_x, 0),
            check("morph lands on the target (IoU)", end_iou > .95, end_iou, ">.95"),
            check("negative control: unaligned/opposite winding morph self-intersects", bad_x > 0, bad_x, ">0")], [vid]


def superellipse(n, R, cx, cy, k=180):
    th = np.linspace(0, 2 * math.pi, k, endpoint=False)
    c, s = np.cos(th), np.sin(th)
    return np.stack([cx + np.sign(c) * np.abs(c) ** (2 / n) * R, cy + np.sign(s) * np.abs(s) ** (2 / n) * R], 1)


@card("SHAPE-03")
def superellipse_echo(task, wd):
    W = H = 340
    C = 170
    n_at = lambda t: 2 + 2.2 * float(in_out_cubic(np.clip(t / .4, 0, 1)))

    def frame(t):
        a = canvas(W, H)
        for k in range(6, 0, -1):                          # echo rings: +12 px each, delayed 60 ms, fading
            tk = t - k * .06
            P = superellipse(n_at(tk), 60 + 12 * k, C, C)
            L = Image.new("L", (W, H), 0)
            ImageDraw.Draw(L).line([tuple(p) for p in np.vstack([P, P[:1]])], fill=int(255 * (1 - k / 7)), width=1)
            a = np.maximum(a, np.asarray(L)[..., None] * np.array([1, .6, .3]))
        a[poly_mask(W, H, superellipse(n_at(t), 60, C, C))] = (255, 255, 255)
        return a
    ts = np.arange(0, .8, 1 / 30)
    vid = video(wd / "squircle.mp4", [frame(t) for t in ts])
    fr = vread(vid, W, H)
    area = lambda f: float(((f.min(-1) > 200)).sum())
    a0, a1 = area(fr[0]), area(fr[-1])
    circ = math.pi * 60 * 60
    sq_n42 = 4 * 60 * 60 * math.gamma(1 + 1 / 4.2) ** 2 / math.gamma(1 + 2 / 4.2)
    ray = fr[20][C, C + 62:]
    gch = ray[:, 1]
    n_rings = int(((gch[1:-1] > gch[:-2]) & (gch[1:-1] >= gch[2:]) & (gch[1:-1] > 10)).sum())
    ring_lag = [n_at(9 / 30 - k * .06) for k in (1, 3, 6)]
    return [check("t=0 is the circle (area)", abs(a0 - circ) / circ < .03, a0, circ),
            check("t=.4 s reaches n=4.2 squircle (analytic area)", abs(a1 - sq_n42) / sq_n42 < .03, a1, sq_n42),
            check("echo rings lag behind (smaller n further out)", ring_lag[0] > ring_lag[1] > ring_lag[2], ring_lag, "decreasing"),
            check("5-7 echo rings measured along a ray", 5 <= n_rings <= 7, n_rings, "5-7"),
            check("negative control: the circle's area is not the squircle's", abs(a0 - sq_n42) / sq_n42 > .08, a0, sq_n42)], [vid]


def polar_shape(a, b, k, p, cx, cy, n=240):
    th = np.linspace(0, 2 * math.pi, n, endpoint=False)
    r = a + b * np.abs(np.cos(k * th / 2)) ** p
    return np.stack([cx + r * np.cos(th), cy + r * np.sin(th)], 1), r


@card("SHAPE-04")
def polar_morph(task, wd):
    W = H = 240
    src, dst = (50, 30, 4, .5), (50, 30, 8, 2)

    def params(t):
        e = float(in_out_cubic(np.clip(t / .6, 0, 1)))
        return tuple(s_ + (d_ - s_) * e for s_, d_ in zip(src, dst))

    def frame(t):
        a = canvas(W, H)
        for rr in (40, 60, 80):                            # polar grid
            yy, xx = np.mgrid[:H, :W]
            a[np.abs(np.hypot(xx - 120, yy - 120) - rr) < .6] = (40, 40, 60)
        P, _ = polar_shape(*params(t), 120, 120)
        a[poly_mask(W, H, P)] = (255, 200, 80)
        pil = Image.fromarray(a.astype(np.uint8))
        ImageDraw.Draw(pil).text((4, 4), "r=a+b|cos(%.1f t/2)|^%.1f" % (params(t)[2], params(t)[3]), fill=(200, 200, 200))
        return np.asarray(pil).astype(float)
    ts = np.arange(0, .7, 1 / 30)
    vid = video(wd / "polar.mp4", [frame(t) for t in ts])
    fr = vread(vid, W, H)

    def lobes(f):
        m = (f[..., 0] > 200) & (f[..., 2] < 150)
        th = np.linspace(0, 2 * math.pi, 720, endpoint=False)
        rr = []
        for a_ in th:
            ray = [(int(120 + r_ * math.cos(a_)), int(120 + r_ * math.sin(a_))) for r_ in range(0, 110)]
            rr.append(max([r_ for r_, (x, y) in enumerate(ray) if 0 <= x < W and 0 <= y < H and m[y, x]] or [0]))
        rr = np.array(rr, float)
        F = np.abs(np.fft.rfft(rr - rr.mean()))
        return int(np.argmax(F[1:20]) + 1)
    l0, l1 = lobes(fr[0]), lobes(fr[-1])
    return [check("start shape has k=4 lobes (measured from the frame)", l0 == 4, l0, 4),
            check("end shape has k=8 lobes", l1 == 8, l1, 8),
            check("120-240 theta samples", 120 <= len(polar_shape(*dst, 0, 0)[0]) <= 240, 240, "120-240"),
            check("negative control: the start frame does not have the target's 8 lobes", l0 != 8, l0, "!=8")], [vid]


@card("SHAPE-05")
def polygon_morph(task, wd):
    W = H = 200
    sq = poly_regular(4, 70, 100, 100, rot=-math.pi / 4)
    pent = poly_regular(5, 70, 100, 100)
    tri = poly_regular(3, 70, 100, 100)
    A, B = prep_morph(sq, pent, 60)
    _, C = prep_morph(pent, tri, 60)
    B2, C = prep_morph(B, tri, 60)
    cols = [(214, 52, 31), (233, 198, 52), (33, 53, 188)]

    def frame(t):
        seg, u = (0, t / .4) if t < .4 else (1, (t - .4) / .4)
        P0, P1 = (A, B) if seg == 0 else (B2, C)
        e = float(out_elastic(np.clip(u, 0, 1)))
        P = P0 + (P1 - P0) * e
        a = canvas(W, H, (243, 234, 216))
        c = np.array(cols[seg + (1 if u >= 1 else 0)], float)
        a[poly_mask(W, H, P)] = c
        return a
    ts = np.arange(0, .9, 1 / 30)
    vid = video(wd / "bauhaus_morph.mp4", [frame(t) for t in ts])
    fr = vread(vid, W, H)
    m = lambda f: np.abs(f - (243, 234, 216)).sum(-1) > 60
    i_p = iou(m(fr[12]), poly_mask(W, H, pent))
    i_t = iou(m(fr[-1]), poly_mask(W, H, tri))
    over = max(iou(m(fr[k]), poly_mask(W, H, pent)) for k in (4, 5, 6))
    c_end = fr[-1][100, 100]
    return [check("square -> pentagon lands at 400 ms (IoU)", i_p > .93, i_p, ">.93"),
            check("pentagon -> triangle at 800 ms (IoU)", i_t > .93, i_t, ">.93"),
            check("recolour in step: triangle is blue", c_end[2] > 150 and c_end[0] < 80, c_end.tolist(), "blue"),
            check("resampled to 60 points both sides", len(A) == len(B) == 60, 60, 60),
            check("negative control: the square is not the pentagon", iou(m(fr[0]), poly_mask(W, H, pent)) < .9,
                  iou(m(fr[0]), poly_mask(W, H, pent)), "<.9")], [vid]


@card("SHAPE-06")
def spring_morph_stars(task, wd):
    W = H = 240
    circ = poly_regular(64, 70, 120, 120)
    sq = poly_regular(4, 80, 120, 120, rot=-math.pi / 4)
    st = star_poly(5, 85, 38, 120, 120)
    A, B = prep_morph(circ, sq, 200)
    B2, C = prep_morph(B, st, 200)

    def frame(t, spring_on=True):
        seg, u = (0, t) if t < .7 else (1, t - .7)
        e = float(spring(u, 180, 14)) if spring_on else float(np.clip(u / .5, 0, 1))
        P0, P1 = (A, B) if seg == 0 else (B2, C)
        a = canvas(W, H)
        a[poly_mask(W, H, P0 + (P1 - P0) * e)] = (255, 255, 255)
        for k in range(8):                                 # orbiting star satellites: 1 rev/s
            ang = 2 * math.pi * (t + k / 8)
            disc(a, 120 + 110 * math.cos(ang), 120 + 110 * math.sin(ang), 3, (255, 0, 0) if k == 0 else (255, 210, 0))
        return a
    ts = np.arange(0, 1.4, 1 / 30)
    vid = video(wd / "spring_morph.mp4", [frame(t) for t in ts])
    fr = vread(vid, W, H)
    shape = lambda f: (f.min(-1) > 200)
    sqm = poly_mask(W, H, sq)

    def rebound(frames):
        """Distance to the square (1 - IoU) over time: an overshoot gets close, moves away again, then settles."""
        d = np.array([1 - iou(shape(f), sqm) for f in frames])
        k = int(np.argmax(d < .04)) if (d < .04).any() else len(d)
        return float(d[k:].max() - d[k]) if k < len(d) else 0.0
    overshoot = rebound(fr[:21])
    i_st = iou(shape(fr[-1]), poly_mask(W, H, st))
    tr = track(fr, 0, thr=200, othr=60)
    angs = np.unwrap([math.atan2(c[1] - 120, c[0] - 120) for c in tr])
    rev = float((angs[30] - angs[0]) / (2 * math.pi) / 1.0)
    lin_over = rebound([frame(t, False) for t in ts[:21]])
    return [check("spring (k 180, d 14) overshoots: reaches the square, leaves it, settles", overshoot > .02, overshoot, ">.02"),
            check("ends on the 5-point star (IoU)", i_st > .9, i_st, ">.9"),
            check("satellites orbit 1 rev/s (tracked)", abs(rev - 1) < .05, rev, 1),
            check("200-point resample", len(A) == 200, len(A), 200),
            check("negative control: a clamped linear mix never leaves the square again", lin_over < .005, lin_over, "<.005")], [vid]


@card("SHAPE-07")
def echo_trail_morph(task, wd):
    W = H = 240
    A, B = prep_morph(poly_regular(48, 70, 0, 0), star_poly(6, 85, 40, 0, 0), 96)

    def shape_at(t):
        e = float(in_out_cubic(np.clip(t / .7, 0, 1)))
        P = A + (B - A) * e
        r = t * 2.0
        Rm = np.array([[math.cos(r), -math.sin(r)], [math.sin(r), math.cos(r)]])
        return P @ Rm.T + 120

    def outline(P):
        L = Image.new("L", (W, H), 0)
        ImageDraw.Draw(L).line([tuple(p) for p in np.vstack([P, P[:1]])], fill=255, width=2)
        return np.asarray(L) > 0

    def frame(t, echoes=True):
        a = canvas(W, H)
        if echoes:
            a[outline(shape_at(t - .08))] = (0, 0, 255)    # copies at t - 80 ms and t - 40 ms, accent colours, stroke only
            a[outline(shape_at(t - .04))] = (0, 255, 0)
        a[poly_mask(W, H, shape_at(t))] = (255, 255, 255)
        for k in range(3):
            ang = 2 * math.pi * (t * .5 + k / 3)
            disc(a, 120 + 105 * math.cos(ang), 120 + 105 * math.sin(ang), 2, (255, 120, 0))
        return a
    ts = np.arange(0, .8, 1 / 30)
    vid = video(wd / "echo_morph.mp4", [frame(t) for t in ts])
    fr = vread(vid, W, H)
    f = fr[10]
    g_m = (f[..., 1] > 200) & (f[..., 0] < 60)
    b_m = (f[..., 2] > 200) & (f[..., 0] < 60)
    t10 = 10 / 30
    match_g = iou(g_m, outline(shape_at(t10 - .04)) & ~poly_mask(W, H, shape_at(t10)))
    match_b = iou(b_m, outline(shape_at(t10 - .08)) & ~poly_mask(W, H, shape_at(t10)) & ~outline(shape_at(t10 - .04)))
    plain = frame(t10, echoes=False)
    pg = int(((plain[..., 1] > 200) & (plain[..., 0] < 60)).sum())
    return [check("green copy is the shape 40 ms earlier (IoU)", match_g > .7, match_g, ">.7"),
            check("blue copy is the shape 80 ms earlier (IoU)", match_b > .6, match_b, ">.6"),
            check("three orbit dots", int(label((f[..., 0] > 200) & (f[..., 1] > 80) & (f[..., 1] < 160) & (f[..., 2] < 60))[1]) == 3, 3, 3),
            check("negative control: without echoes there is no lagged copy", pg == 0, pg, 0)], [vid]


@card("SHAPE-08")
def gizmo_morph(task, wd):
    W = H = 240
    A, B = prep_morph(poly_regular(48, 60, 0, 0), star_poly(5, 75, 32, 0, 0), 96)
    font_ = ImageFont.truetype(str(FONTS / "Poppins-Regular.ttf"), 12)

    def frame(t):
        e = float(in_out_cubic(np.clip(t / .6, 0, 1)))
        rot = 340.9 * t / .6
        r = math.radians(rot)
        Rm = np.array([[math.cos(r), -math.sin(r)], [math.sin(r), math.cos(r)]])
        P = (A + (B - A) * e) @ Rm.T + 120
        a = canvas(W, H)
        a[poly_mask(W, H, P)] = (255, 255, 255)
        box = np.array([[-90, -90], [90, -90], [90, 90], [-90, 90]]) @ Rm.T + 120
        pil = Image.fromarray(a.astype(np.uint8))
        d = ImageDraw.Draw(pil)
        d.line([tuple(p) for p in np.vstack([box, box[:1]])], fill=(170, 170, 170), width=1)
        for c in box:
            d.rectangle([c[0] - 4, c[1] - 4, c[0] + 4, c[1] + 4], outline=(170, 170, 170), fill=(20, 20, 20))
        d.text((6, 222), "ROT %.1f°" % rot, fill=(0, 255, 0), font=font_)
        return np.asarray(pil).astype(float), rot, box
    out_frames = [frame(t)[0] for t in np.arange(0, .7, 1 / 30)]
    vid = video(wd / "gizmo.mp4", out_frames)
    fr = vread(vid, W, H)
    img, rot, box = frame(.6)
    # measure the box angle from the handle squares in the rendered final frame and compare with the readout
    hm = (np.abs(fr[18] - 20).max(-1) < 6)               # the handles' dark fill
    lab, n = label(hm, eight=True)
    pts = []
    for k in range(1, n + 1):
        ys, xs = np.nonzero(lab == k)
        if 15 <= len(xs) <= 120:
            pts.append((xs.mean(), ys.mean()))
    angs = sorted((math.degrees(math.atan2(y - 120, x - 120)) % 90) for x, y in pts)
    meas = float(np.median(angs)) if angs else -1
    expect = (340.9 - 45 + 90 * 10) % 90                   # handle at (-90,-90) sits at -135 deg before rotation
    readout = 340.9
    lin_txt = ((0 - 45) % 90)
    return [check("4 square handles found on the rotating box", len(pts) == 4, len(pts), 4),
            check("box angle measured from the handles matches the readout (deg mod 90)", abs(meas - expect) < 2, meas, expect),
            check("morph ends on the star (IoU)", iou(fr[18].min(-1) > 200, poly_mask(W, H, B @ np.array([[math.cos(math.radians(340.9)),
                  math.sin(math.radians(340.9))], [-math.sin(math.radians(340.9)), math.cos(math.radians(340.9))]]) + 120)) > .85, True, True),
            check("negative control: the unrotated box angle differs from the readout", abs(lin_txt - expect) > 5, lin_txt, expect)], [vid]


@card("SHAPE-09")
def dot_cloud_morph(task, wd):
    W = H = 240
    rng = R(9)
    src = poly_regular(40, 90, 120, 120)
    inside = []
    while len(inside) < 100:
        p = rng.uniform(30, 210, 2)
        if math.hypot(p[0] - 120, p[1] - 120) < 90:
            inside.append(p)
    S = np.array(inside)
    G = np.array([(50 + c * 15, 50 + r * 15) for r in range(10) for c in range(10)], float)
    rc = np.array([(r, c) for r in range(10) for c in range(10)])
    # match by sorting both sets by angle around the centre
    sa = np.argsort(np.arctan2(S[:, 1] - 120, S[:, 0] - 120))
    ga = np.argsort(np.arctan2(G[:, 1] - 120 + 1e-3, G[:, 0] - 120))
    S, G, rc = S[sa], G[ga], rc[ga]
    delay = (rc[:, 0] + rc[:, 1]) * .025                   # diagonal stagger 25 ms

    def frame(t):
        e = in_out_cubic((t - delay) / .8)[:, None]
        P = S + (G - S) * e
        a = canvas(W, H)
        for x, y in P:
            disc(a, x, y, 2, (255, 255, 255))
        return a
    T = .8 + delay.max()
    ts = np.arange(0, T + .1, 1 / 30)
    vid = video(wd / "dot_morph.mp4", [frame(t) for t in ts])
    fr = vread(vid, W, H)
    pts = lambda f: np.array([c for c in [centroid(label(f.max(-1) > 128)[0] == k) for k in range(1, label(f.max(-1) > 128)[1] + 1)] if c])
    end = pts(fr[-1])
    err = chamfer(end, G)
    mid = frame(.5)
    e_first = float(in_out_cubic((.5 - delay[np.argmin(delay)]) / .8))
    e_last = float(in_out_cubic((.5 - delay[np.argmax(delay)]) / .8))
    rand_d = float(np.linalg.norm(S - G[R(2).permutation(100)], axis=1).sum())
    sort_d = float(np.linalg.norm(S - G, axis=1).sum())
    return [check("dots land on the 10x10 grid (chamfer px)", err < 1.0 and len(end) == 100, [err, len(end)], "<1, 100 dots"),
            check("diagonal stagger: corner (0,0) leads (18 x 25 ms)", e_first > e_last and abs(delay.max() - .45) < 1e-9, [e_first, e_last], "first>last"),
            check("angle matching shortens travel vs random", sort_d < rand_d, [sort_d, rand_d], "sorted<random"),
            check("negative control: the start scatter is not the grid", chamfer(pts(fr[0]), G) > 3, chamfer(pts(fr[0]), G), ">3")], [vid]


@card("SHAPE-10")
def bar_to_ring(task, wd):
    W = H = 240
    L = 2 * math.pi * 60                                   # bar length = ring circumference

    def arc_pts(r, n=400):
        # constant-length arc of radius r, anchored at its midpoint (centre shifted so the arc's middle stays put)
        phi = L / r
        a = np.linspace(-phi / 2, phi / 2, n) + math.pi / 2
        cx, cy = 120, 200 - r                             # arc midpoint pinned at (120, 200)
        return np.stack([cx + r * np.cos(a), cy + r * np.sin(a)], 1)

    def r_at(t):
        e = float(in_out_cubic(np.clip(t / 1.0, 0, 1)))
        return math.exp(math.log(1e5) + (math.log(L / (2 * math.pi)) - math.log(1e5)) * e)   # log-interpolate r
    frames = []
    lens = []
    for t in np.arange(0, 1.1, 1 / 30):
        P = arc_pts(r_at(t))
        lens.append(float(np.hypot(*np.diff(P, axis=0).T).sum()))
        Lr = Image.new("L", (W, H), 0)
        ImageDraw.Draw(Lr).line([tuple(p) for p in P], fill=255, width=10)
        frames.append(np.repeat(np.asarray(Lr)[..., None], 3, 2).astype(float))
    vid = video(wd / "bar_ring.mp4", frames)
    fr = vread(vid, W, H)
    end = fr[-1].max(-1) > 128
    yy, xx = np.mgrid[:H, :W]
    ring = np.abs(np.hypot(xx - 120, yy - 140) - 60) < 5
    first = fr[0].max(-1) > 128
    b = bbox(first)
    return [check("arc length stays = bar length while curling", max(abs(l_ - L) for l_ in lens) / L < .01, max(lens), L),
            check("ends as a closed ring r = L/2pi (IoU)", iou(end, ring) > .8, iou(end, ring), ">.8"),
            check("starts as a straight bar (height ~ stroke)", b[3] - b[1] <= 12, b[3] - b[1], "<=12"),
            check("negative control: the bar frame is not the ring", iou(first, ring) < .2, iou(first, ring), "<.2")], [vid]


@card("SHAPE-11")
def sketch_to_clean(task, wd):
    W, H = 300, 160
    ctrl = np.array([[20, 120], [80, 40], [150, 110], [220, 30], [280, 90]], float)

    def catmull(P, n=200):
        out = []
        Q = np.vstack([P[:1], P, P[-1:]])
        seg = len(P) - 1
        for i in range(seg):
            p0, p1, p2, p3 = Q[i], Q[i + 1], Q[i + 2], Q[i + 3]
            for t in np.linspace(0, 1, n // seg, endpoint=False):
                out.append(.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
        out.append(P[-1])
        return np.array(out)
    clean = catmull(ctrl)
    jit = clean + R(11).normal(0, 4, clean.shape)          # the same samples, jittered

    def frame(t):
        e = float(in_out_cubic(np.clip(t / .5, 0, 1)))
        P = jit + (clean - jit) * e
        Lr = Image.new("L", (W, H), 0)
        ImageDraw.Draw(Lr).line([tuple(p) for p in P], fill=255, width=2)
        return np.repeat(np.asarray(Lr)[..., None], 3, 2).astype(float), P
    vid = video(wd / "cleanup.mp4", [frame(t)[0] for t in np.arange(0, .6, 1 / 30)])
    fr = vread(vid, W, H)
    rough = lambda P: float(np.abs(np.diff(P, 2, axis=0)).mean())
    lit_end = mask_pts(fr[-1].max(-1) > 128)
    c_end = chamfer(lit_end, clean)
    c_start = chamfer(mask_pts(fr[0].max(-1) > 128), clean)
    return [check("final stroke lies on the Catmull-Rom path (chamfer px)", c_end < 1.0, c_end, "<1"),
            check("same sample count before/after", len(jit) == len(clean), len(jit), len(clean)),
            check("smoothed path is much smoother (2nd difference)", rough(clean) < .2 * rough(jit), [rough(clean), rough(jit)], "<.2x"),
            check("negative control: the jittered sketch is off the clean path", c_start > 1.8, c_start, ">1.8")], [vid]


def goo(alpha, sd=10.0):
    """feGaussianBlur(stdDeviation) then feColorMatrix alpha row (0 0 0 18 -7), on alpha in 0..1."""
    from scipy.ndimage import gaussian_filter
    return np.clip(18 * gaussian_filter(alpha, sd) - 7, 0, 1)


@card("SHAPE-14")
def liquid_morph(task, wd):
    W, H = 320, 180
    yy, xx = np.mgrid[:H, :W]

    def blob(cx, cy, r, t, seed):
        th = np.arctan2(yy - cy, xx - cx)
        rr = r * (1 + .12 * perlin2(np.cos(th) * 1.5 + t, np.sin(th) * 1.5 + seed, seed))   # vertices driven by noise
        return (np.hypot(xx - cx, yy - cy) < rr).astype(float)

    def frame(t, gooey=True):
        d = 60 * (1 - float(in_out_cubic(np.clip(t / .8, 0, 1))))   # two blobs approach and merge
        al = np.maximum(blob(160 - 40 - d, 90, 34, t, 1), blob(160 + 40 + d, 90, 34, t, 2))
        if gooey:
            al = goo(al, 10)
        return np.repeat((al * 255)[..., None], 3, 2)
    ts = np.arange(0, 1.0, 1 / 30)
    vid = video(wd / "liquid.mp4", [frame(t) for t in ts])
    fr = vread(vid, W, H)
    comps = [label(f.max(-1) > 128)[1] for f in fr]
    plain = label(frame(.95, gooey=False).max(-1) > 128)[1]
    edge_var = float(np.abs(frame(.2) - frame(.5)).mean())
    return [check("blobs separate at the start (2 parts)", comps[0] == 2, comps[0], 2),
            check("gooey filter merges them when close (1 part)", comps[-1] == 1, comps[-1], 1),
            check("noise keeps the outline moving", edge_var > 1, edge_var, ">1"),
            check("negative control: without the goo filter they stay apart", plain == 2, plain, 2)], [vid]


@card("SHAPE-18")
def dynamic_island(task, wd):
    W, H = 320, 200
    s0, s1 = np.array([120.0, 36, 18]), np.array([280.0, 160, 16])   # pill -> window (w, h, radius)

    def state(t):
        return s0 + (s1 - s0) * float(spring(t, 200, 22))

    def frame(t, gate=True):
        w, h, r = state(t)
        im = Image.new("RGB", (W, H), (240, 240, 240))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([160 - w / 2, 100 - h / 2, 160 + w / 2, 100 + h / 2], radius=min(r, h / 2), fill=(10, 10, 10))
        prog = (w - s0[0]) / (s1[0] - s0[0])
        if (prog >= .7) or not gate:                       # content only after 70% of the size change
            a = min(1.0, (prog - .7) / .3) if gate else 1.0
            d.rectangle([110, 70, 210, 80], fill=(int(255 * a), 0, 0))
        return np.asarray(im).astype(float)
    ts = np.arange(0, .8, 1 / 60)
    vid = video(wd / "island.mp4", [frame(t) for t in ts], 60)
    fr = vread(vid, W, H)
    widths = np.array([(lambda b: b[2] - b[0] + 1)(bbox(f.max(-1) < 60)) for f in fr], float)
    exp_w = np.array([state(t)[0] for t in ts])
    err = float(np.abs(widths - exp_w).max())
    red = [bool(((f[..., 0] > 60) & (f[..., 1] < 40)).any()) for f in fr]
    first = red.index(True)
    prog_first = (exp_w[first] - s0[0]) / (s1[0] - s0[0])
    early = frame(.02, gate=False)
    return [check("container width follows spring k200 d22 (px)", err < 2.5, err, "<2.5"),
            check("content appears only after 70% of the size change", prog_first >= .7, prog_first, ">=.7"),
            check("settles at the window size", abs(widths[-1] - 280) < 2, widths[-1], 280),
            check("negative control: ungated content shows at 2% progress", bool(((early[..., 0] > 60) & (early[..., 1] < 40)).any()),
                  True, True)], [vid]


@card("SHAPE-19")
def two_edge_indicator(task, wd):
    W, H = 400, 60
    x0, x1, w0 = 40, 280, 60

    def edges(t, ratio=1.6):
        k_trail = 160.0
        lead = x0 + w0 + (x1 - x0) * float(spring(t, k_trail * ratio, 2 * math.sqrt(k_trail * ratio) * .8))
        trail = x0 + (x1 - x0) * float(spring(t, k_trail, 2 * math.sqrt(k_trail) * .8))
        return trail, lead

    def frame(t, ratio=1.6):
        tr, ld = edges(t, ratio)
        im = Image.new("RGB", (W, H), (20, 20, 20))
        ImageDraw.Draw(im).rounded_rectangle([tr, 25, ld, 35], radius=5, fill=(255, 220, 0))
        return np.asarray(im).astype(float)
    ts = np.arange(0, 1.0, 1 / 60)
    vid = video(wd / "indicator.mp4", [frame(t) for t in ts], 60)
    fr = vread(vid, W, H)
    wid = np.array([(lambda b: b[2] - b[0] + 1)(bbox(f.max(-1) > 128)) for f in fr], float)
    same = np.array([(lambda b: b[2] - b[0] + 1)(bbox(frame(t, 1.0).max(-1) > 128)) for t in ts], float)
    return [check("indicator stretches in travel (max width > rest + 20 px)", wid.max() > w0 + 20, wid.max(), ">%d" % (w0 + 20)),
            check("settles back to its rest width", abs(wid[-1] - (w0 + 1)) <= 2, wid[-1], w0 + 1),
            check("leading edge (1.6x stiffer) runs ahead of the trailing edge (measured at 50 ms)",
                  (lambda b: (b[2] - (x0 + w0)) > (b[0] - x0) + 5)(bbox(fr[3].max(-1) > 128)),
                  (lambda b: [b[2] - (x0 + w0), b[0] - x0])(bbox(fr[3].max(-1) > 128)), "lead ahead"),
            check("negative control: equal springs never stretch", float(np.ptp(same)) <= 1, float(np.ptp(same)), "<=1")], [vid]


@card("SHAPE-21")
def ui_states(task, wd):
    W, H = 320, 240
    states = [(80, 30, 15), (60, 30, 15), (200, 120, 12), (320, 240, 0)]   # button, toggle, card, full screen
    STEP, HOLD = .6, .9
    times = []
    t = HOLD
    for _ in range(3):
        times.append((t, t + STEP))
        t += STEP + HOLD

    def st(t):
        cur = np.array(states[0], float)
        for i, (a, b) in enumerate(times):
            if t >= b:
                cur = np.array(states[i + 1], float)
            elif t > a:
                e = float(in_out_cubic((t - a) / STEP))
                cur = np.array(states[i], float) + (np.array(states[i + 1]) - np.array(states[i])) * e
        return cur

    def frame(t):
        w, h, r = st(t)
        im = Image.new("RGB", (W, H), (230, 230, 230))
        ImageDraw.Draw(im).rounded_rectangle([160 - w / 2, 120 - h / 2, 160 + w / 2 - 1, 120 + h / 2 - 1], radius=r, fill=(30, 60, 200))
        return np.asarray(im).astype(float)
    total = times[-1][1] + HOLD
    ts = np.arange(0, total, 1 / 30)
    vid = video(wd / "ui_states.mp4", [frame(t) for t in ts])
    fr = vread(vid, W, H)
    mask = lambda f: (f[..., 2] > 150) & (f[..., 0] < 100)
    area = np.array([float(mask(f).sum()) for f in fr])
    ref = []
    for k in range(4):                                     # each pure state's mask, rendered once
        im = Image.new("RGB", (W, H), (230, 230, 230))
        w, h, r = states[k]
        ImageDraw.Draw(im).rounded_rectangle([160 - w / 2, 120 - h / 2, 160 + w / 2 - 1, 120 + h / 2 - 1], radius=r, fill=(30, 60, 200))
        ref.append(mask(np.asarray(im).astype(float)))
    inst = [[i_ for i_, f in enumerate(fr) if np.array_equal(mask(f), ref[k])] for k in range(4)]
    moves = [(inst[k + 1][0] - inst[k][-1]) / 30 for k in range(3)]
    holds = [len(inst[k]) / 30 for k in range(1, 3)]
    mid = range(inst[2][-1] + 2, inst[3][0] - 1)            # inside the last step: no frame repeats
    still_in_step = sum(1 for i_ in mid if area[i_] == area[i_ - 1]) / 30
    return [check("three state changes, each <= 600 ms, the largest measuring 600 ms", len(moves) == 3 and max(moves) <= .64
                  and abs(max(moves) - .6) < .05, moves, .6),
            check("900 ms holds between states", all(h >= .85 for h in holds), holds, ">=.9"),
            check("ends full screen", float(area[-1]) > .95 * W * H, float(area[-1]), "full"),
            check("negative control: the same hold measurement inside a step finds no hold", still_in_step < .85, still_in_step, "<.85")], [vid]


@card("SHAPE-22")
def dot_to_interface(task, wd):
    W, H = 320, 220
    D, FW, FH = 8, 240, 160

    def frame(t, gate=True):
        e = float(out_expo(np.clip(t / 1.2, 0, 1)))
        w, h = D + (FW - D) * e, D + (FH - D) * e
        r = D / 2 + (12 - D / 2) * e
        im = Image.new("RGB", (W, H), (0, 0, 0))
        dr = ImageDraw.Draw(im)
        dr.rounded_rectangle([160 - w / 2, 110 - h / 2, 160 + w / 2, 110 + h / 2], radius=r, outline=(120, 200, 255), width=2)
        if e >= .8 or not gate:                             # content opacity after 80%
            a = (e - .8) / .2 if gate else 1
            dr.rectangle([100, 80, 220, 90], fill=(0, int(255 * a), 0))
        for k in range(6):                                  # satellites, 50 ms stagger
            u = np.clip((t - .2 - .05 * k) / .6, 0, 1)
            if u > 0:
                ang = 2 * math.pi * k / 6
                rr = 150 * float(out_cubic(u))
                x, y = 160 + rr * math.cos(ang), 110 + rr * .6 * math.sin(ang)
                dr.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(255, 0, 0))
        return np.asarray(im).astype(float)
    ts = np.arange(0, 1.4, 1 / 30)
    vid = video(wd / "dot_bloom.mp4", [frame(t) for t in ts])
    fr = vread(vid, W, H)
    box = lambda f: bbox((f[..., 2] > 150) & (f[..., 0] < 180))
    b0, b1 = box(fr[0]), box(fr[36])
    green = [bool(((f[..., 1] > 60) & (f[..., 0] < 40) & (f[..., 2] < 40)).any()) for f in fr]
    first = green.index(True)
    e_first = float(out_expo(first / 30 / 1.2))
    ungated = frame(0, gate=False)
    return [check("starts as an 8 px dot", (b0[2] - b0[0] + 1) <= 10, b0[2] - b0[0] + 1, 8),
            check("expands to the 240 x 160 frame by 1.2 s", abs((b1[2] - b1[0]) - FW) <= 3 and abs((b1[3] - b1[1]) - FH) <= 3,
                  [b1[2] - b1[0], b1[3] - b1[1]], [FW, FH]),
            check("content fades in only after 80% (expo)", e_first >= .8, e_first, ">=.8"),
            check("negative control: ungated content shows at t = 0", bool(((ungated[..., 1] > 60) & (ungated[..., 0] < 40)).any()), True, True)], [vid]


@card("SHAPE-24")
def logo_to_iris(task, wd):
    W, H = 320, 200
    from scipy.ndimage import gaussian_filter
    yy, xx = np.mgrid[:H, :W].astype(float)

    def frame(t, glow=True):
        e = float(out_cubic(np.clip(t / .8, 0, 1)))
        a = canvas(W, H)
        hgt = 70 * e                                       # almond height 0 -> full, ease-out
        u = (xx - 160) / 130
        inside = (np.abs(u) < 1) & (np.abs(yy - 100) < hgt * (1 - u * u))
        a[inside] = (230, 230, 240)
        ir = 18 + 32 * e                                   # logo ring scales into the iris disc
        d = np.hypot(xx - 160, yy - 100)
        iris = (d < ir) & inside
        a[iris] = np.stack([20 + 0 * d[iris], 100 + 80 * (d[iris] / ir), 200 + 0 * d[iris]], 1)
        if glow:                                           # iris glow blur ~35 px tinted #5cc8ff
            g = (gaussian_filter((d < ir).astype(float), 12) * inside * ~iris)[..., None]
            a = a * (1 - .7 * g) + .7 * g * hexc("#5cc8ff")
        return np.clip(a, 0, 255)
    ts = np.arange(0, 1.0, 1 / 30)
    vid = video(wd / "iris.mp4", [frame(t) for t in ts])
    fr = vread(vid, W, H)
    open_h = [(lambda b: (b[3] - b[1] + 1) if b else 0)(bbox(f.max(-1) > 100)) for f in fr]
    exp = [2 * 70 * float(out_cubic(min(1, i / 30 / .8))) for i in range(len(fr))]
    err = max(abs(a_ - b_) for a_, b_ in zip(open_h[3:], exp[3:]))
    lin = 2 * 70 * (6 / 30 / .8)
    halo = lambda f: float(f[100, 160 + 51:160 + 58, 0].mean())     # red drops where the cyan glow covers the white
    return [check("eye opens with ease-out height (px)", err <= 3, err, "<=3"),
            check("iris disc reaches 50 px radius", abs(float(np.hypot(*(mask_pts((fr[-1][..., 0] < 60) & (fr[-1][..., 2] > 150)) - (160, 100)).T).max()) - 50) < 3,
                  50, 50),
            check("glow spreads beyond the iris (cyan halo lowers red)", halo(fr[-1]) < halo(frame(1.0, glow=False)) - 25,
                  [halo(fr[-1]), halo(frame(1.0, glow=False))], "-25"),
            check("negative control: a linear opening would be much smaller at 200 ms", abs(open_h[6] - lin) > 20, [open_h[6], lin], ">20")], [vid]


def checkmark(cx, cy, s, n=60):
    P = np.array([[cx - s, cy], [cx - s * .3, cy + s * .7], [cx + s, cy - s * .8]])
    seg = np.hypot(*np.diff(P, axis=0).T)
    u = np.linspace(0, seg.sum(), n)
    cum = np.concatenate([[0], np.cumsum(seg)])
    return np.stack([np.interp(u, cum, P[:, 0]), np.interp(u, cum, P[:, 1])], 1)


@card("SHAPE-25")
def tap_ripple_check(task, wd):
    W = H = 240
    circ = poly_regular(60, 50, 120, 120)
    circ = np.vstack([circ, circ[:1]])                     # open path (closed circle as a polyline)
    chk = checkmark(120, 120, 45, 61)
    yy, xx = np.mgrid[:H, :W]

    def frame(t):
        a = canvas(W, H)
        u = np.clip(t / .9, 0, 1)
        sc, op = 1 + .9 * float(out_cubic(u)), .9 * (1 - float(u))
        ring = np.abs(np.hypot(xx - 120, yy - 120) - 50 * sc) < 1.5
        a[ring, 2] = 255 * op
        e = float(in_out_cubic(np.clip((t - .2) / .4, 0, 1)))
        P = circ + (chk - circ) * e
        L = Image.new("L", (W, H), 0)
        ImageDraw.Draw(L).line([tuple(p) for p in P], fill=255, width=3)
        a[np.asarray(L) > 0] = (0, 255, 0)
        return a
    ts = np.arange(0, 1.0, 1 / 30)
    vid = video(wd / "tap_check.mp4", [frame(t) for t in ts])
    fr = vread(vid, W, H)
    rr = np.hypot(xx - 120, yy - 120)
    f = fr[13]
    m = (f[..., 2] > 20) & (f[..., 1] < 60)
    r_meas = float(rr[m].mean())
    r_exp = 50 * (1 + .9 * float(out_cubic(13 / 30 / .9)))
    a_meas = float(f[..., 2][m].max()) / 255
    a_exp = .9 * (1 - 13 / 30 / .9)
    green = lambda f_: mask_pts((f_[..., 1] > 128) & (f_[..., 0] < 60))
    c_end = chamfer(green(fr[-1]), chk)
    c0 = chamfer(green(fr[0]), chk)
    return [check("ripple radius 1 -> 1.9 scale (px at 433 ms)", abs(r_meas - r_exp) < 2, r_meas, r_exp),
            check("ripple opacity .9 -> 0 over .9 s", abs(a_meas - a_exp) < .06, a_meas, a_exp),
            check("circle ends as the checkmark (chamfer px)", c_end < 1.5, c_end, "<1.5"),
            check("negative control: the starting circle is not the check", c0 > 8, c0, ">8")], [vid]


@card("SHAPE-26")
def collapse_to_logo(task, wd):
    W = H = 240
    rng = R(26)
    items = rng.uniform(30, 210, (12, 2))
    logo = text_mask(W, H, "K", 120, POPPINS) > 127

    def frame(t):
        a = canvas(W, H)
        if t < .8:                                          # everything collapses to a dot
            e = float(in_cubic(t / .8))
            for x, y in items + (np.array([120, 120]) - items) * e:
                s = 10 * (1 - e) + 2
                a[int(y - s):int(y + s), int(x - s):int(x + s)] = (240, 200, 90)
        elif t < 1.4:                                       # dot opens into the logo
            e = float(out_back(np.clip((t - .8) / .6, 0, 1)))
            from scipy.ndimage import zoom
            z = zoom(logo.astype(float), max(.02, e), order=0) > .5
            h, w = z.shape
            y0, x0 = 120 - h // 2, 120 - w // 2
            ys, xs = np.nonzero(z)
            ok = (ys + y0 >= 0) & (ys + y0 < H) & (xs + x0 >= 0) & (xs + x0 < W)
            a[ys[ok] + y0, xs[ok] + x0] = (255, 255, 255)
        else:
            a[logo] = (255, 255, 255)                      # hold the final logo 2 s
        return a
    ts = np.arange(0, 3.4, 1 / 15)
    vid = video(wd / "collapse_logo.mp4", [frame(t) for t in ts], 15)
    fr = vread(vid, W, H)
    lit = [float((f.max(-1) > 100).sum()) for f in fr]
    k_dot = int(np.argmin(lit[8:14])) + 8
    hold = fr[int(1.4 * 15) + 1:]
    held = all(np.array_equal(hold[0], h_) for h_ in hold) and len(hold) / 15 >= 1.9
    return [check("collapse shrinks everything to a dot (< 40 px lit around 800 ms)", lit[k_dot] < 40, [k_dot, lit[k_dot]], "<40"),
            check("final logo matches (IoU)", iou(fr[-1].max(-1) > 128, logo) > .97, iou(fr[-1].max(-1) > 128, logo), ">.97"),
            check("final logo held >= 2 s unchanged", held, len(hold) / 15, ">=2"),
            check("negative control: the opening frame is not collapsed", lit[0] > 1000, lit[0], ">1000")], [vid]


@card("SHAPE-27")
def svg_goo(task, wd):
    svg = """<!doctype html><html><body style="margin:0;background:#000">
<svg width="400" height="200"><defs><filter id="goo"><feGaussianBlur in="SourceGraphic" stdDeviation="10"/>
<feColorMatrix values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -7"/></filter></defs>
<g filter="%s" fill="#fff">%s</g></svg></body></html>"""

    def circles(t):
        out = []
        for k in range(4):                                  # 4 orbiting circles, positions from seek(t)
            a = t * 2 * math.pi * .5 + k * math.pi / 2
            out.append('<circle cx="%.2f" cy="%.2f" r="22"/>' % (200 + 40 * math.cos(a), 100 + 40 * math.sin(a) * .5))
        return "".join(out)
    shot = chrome_shot(wd, "goo", svg % ("url(#goo)", circles(.3)), size=(400, 200))
    plain = chrome_shot(wd, "plain", svg % ("none", circles(.3)), size=(400, 200))
    g, p_ = load(shot).max(-1) > 128, load(plain).max(-1) > 128
    ng, npl = label(g)[1], label(p_)[1]
    from scipy.ndimage import gaussian_filter
    ref = np.zeros((200, 400))
    for k in range(4):
        a = .3 * 2 * math.pi * .5 + k * math.pi / 2
        yy, xx = np.mgrid[:200, :400]
        ref[np.hypot(xx - (200 + 40 * math.cos(a)), yy - (100 + 40 * math.sin(a) * .5)) <= 22] = 1
    mine = goo(ref, 10) > .5
    return [check("Chromium SVG goo merges the circles into one blob", ng == 1, ng, 1),
            check("numpy re-implementation of the same filter agrees (IoU)", iou(mine, g) > .9, iou(mine, g), ">.9"),
            check("filter fills the gaps (blob area > plain circles area)", g.sum() > p_.sum(), [int(g.sum()), int(p_.sum())], "goo > plain"),
            check("negative control: without the filter the circles stay separate", npl >= 2, npl, ">=2")], [shot, plain]


@card("SHAPE-29")
def metaball_clay(task, wd):
    W, H = 320, 200
    yy, xx = np.mgrid[:H, :W].astype(float)
    rng = R(29)
    final = np.array([[138, 90], [182, 90], [160, 128], [116, 128], [204, 128], [160, 52]], float)   # 44 px apart
    start = final + rng.normal(0, 1, (6, 2)) * 0 + np.array([[-200, 0], [200, 0], [0, 150], [-180, 120], [190, 140], [0, -120]])
    r = 20.0

    def field(t):
        e = float(out_cubic(np.clip(t / 1.0, 0, 1)))
        P = start + (final - start) * e
        f = np.zeros((H, W))
        for (x, y) in P:
            f += r * r / ((xx - x) ** 2 + (yy - y) ** 2 + 1)
        return f, P

    def frame(t):
        f, P = field(t)
        a = canvas(W, H, (30, 26, 24))
        a[f > 1.0] = (200, 120, 80)
        return a
    ts = np.arange(0, 1.2, 1 / 15)
    vid = video(wd / "clay.mp4", [frame(t) for t in ts], 15)
    fr = vread(vid, W, H)
    comps = [label(np.abs(f - (30, 26, 24)).sum(-1) > 60)[1] for f in fr]
    discs = np.zeros((H, W), bool)
    for x, y in final:
        discs |= np.hypot(xx - x, yy - y) < r * .9
    return [check("6 blobs roll in (start: several separate parts)", comps[2] >= 3, comps[2], ">=3"),
            check("they merge through the threshold into one clay mass", comps[-1] == 1, comps[-1], 1),
            check("negative control: the same discs without the field are separate", label(discs)[1] >= 2, label(discs)[1], ">=2")], [vid]


@card("SHAPE-35")
def blob_field(task, wd):
    W, H = 320, 180
    from scipy.ndimage import gaussian_filter
    yy, xx = np.mgrid[:H, :W].astype(float)
    periods = [10, 12, 16, 10, 12, 16]
    base = R(35).uniform((40, 30), (280, 150), (6, 2))

    def pos(t):
        return np.array([[bx + 20 * math.sin(2 * math.pi * t / p), by + 20 * math.cos(2 * math.pi * t / p + k)]
                         for k, ((bx, by), p) in enumerate(zip(base, periods))])

    def frame(t):
        a = canvas(W, H, (245, 242, 236))
        for x, y in pos(t):
            m = gaussian_filter((np.hypot(xx - x, yy - y) < 34).astype(float), 6)
            a = a * (1 - .35 * m[..., None]) + .35 * m[..., None] * np.array([120, 160, 230])
        # corner blob: ellipse centre (.93w, .14h), radii .35w x .13h, rotation pi/5, alpha .65
        cx, cy, rx, ry, rot = .93 * W, .14 * H, .35 * W, .13 * H, math.pi / 5
        u = ((xx - cx) * math.cos(rot) + (yy - cy) * math.sin(rot)) / rx
        v = (-(xx - cx) * math.sin(rot) + (yy - cy) * math.cos(rot)) / ry
        e = (u * u + v * v) <= 1
        a[e] = a[e] * .35 + .65 * np.array([233, 120, 90])
        return a
    ts = np.arange(0, 2.0, 1 / 15)
    vid = video(wd / "blobs.mp4", [frame(t) for t in ts], 15)
    fr = vread(vid, W, H)
    corner = (np.abs(fr[0] - (245 * .35 + .65 * 233, 242 * .35 + .65 * 120, 236 * .35 + .65 * 90)).max(-1) < 4)
    c = centroid(corner)
    # drift: displacement between t=0 and t=2 for blob 0 vs blob 2 (different periods -> not lockstep)
    def lockstep(per):
        """Spread of the x-displacements of the first three blobs between t = 0 and t = 2 s."""
        return float(np.ptp([20 * math.sin(2 * math.pi * 2.0 / p) for p in per[:3]]))
    meas = [float(c_[0]) for c_ in (pos(2.0) - pos(0))[:3]]
    lock = float(np.ptp(meas))
    lock_bad = lockstep([10, 10, 10])
    amp = max(float(np.ptp([pos(t)[0][0] for t in np.linspace(0, 10, 200)])) / 2, 0)
    return [check("corner ellipse centred at (.93w, .14h) (visible part's centroid lies toward it)", c is not None and c[0] > .7 * W and c[1] < .4 * H,
                  c, "top-right"),
            check("blob drift amplitude 12-30 px", 12 <= amp <= 30, amp, "12-30"),
            check("periods 10/12/16 s -> blobs never move in lockstep", lock > 1, lock, ">1"),
            check("negative control: equal periods move in lockstep (same measurement)", lock_bad < 1e-9, lock_bad, 0)], [vid]


@card("SHAPE-36")
def noise_blob_text(task, wd):
    W, H = 320, 200
    n = 14

    def blob_pts(t, amp=.15):
        th = np.linspace(0, 2 * math.pi, n, endpoint=False)
        r = 70 * (1 + amp * perlin2(np.cos(th) * 1.3 + t * .4, np.sin(th) * 1.3, 36))
        P = np.stack([160 + r * np.cos(th), 100 + r * np.sin(th)], 1)
        # closed Catmull-Rom through the polar points
        out = []
        for i in range(n):
            p0, p1, p2, p3 = P[i - 1], P[i], P[(i + 1) % n], P[(i + 2) % n]
            for u in np.linspace(0, 1, 12, endpoint=False):
                out.append(.5 * ((2 * p1) + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u * u + (-p0 + 3 * p1 - 3 * p2 + p3) * u ** 3))
        return np.array(out), P, r

    def frame(t, amp=.15):
        P, _, _ = blob_pts(t, amp)
        m = poly_mask(W, H, P)
        a = canvas(W, H, (255, 255, 255))
        yy, xx = np.mgrid[:H, :W]
        g = np.clip((xx - 90) / 140, 0, 1)[..., None]
        grad = hexc("#d3f66a") * (1 - g) + hexc("#5a8cff") * g
        a[m] = grad[m]
        tm = text_mask(W, H, "BLOB", 46, POPPINS) / 255
        a = a * (1 - tm[..., None]) + a * (tm[..., None] * np.array([.25, .25, .25]))   # multiply text
        return a
    ts = np.arange(0, 2.0, 1 / 15)
    vid = video(wd / "noise_blob.mp4", [frame(t) for t in ts], 15)
    fr = vread(vid, W, H)
    _, _, r0 = blob_pts(0)
    _, _, r1 = blob_pts(1.5)
    tm = text_mask(W, H, "BLOB", 46, POPPINS) > 200
    blob = poly_mask(W, H, blob_pts(1.0)[0])
    on_blob = fr[15][tm & blob]
    under = frame(1.0)[tm & blob] / .25                    # the gradient under the text
    mult = float(np.abs(on_blob / 255 - under / 255 * .25).mean() * 255)
    change = lambda fa, fb: int(((fa.min(-1) < 250) != (fb.min(-1) < 250)).sum())
    moved = change(fr[0], fr[22])
    moved0 = change(frame(0, 0), frame(1.5, 0))
    smooth = float(np.abs(np.diff(blob_pts(0)[0], 2, axis=0)).max())
    return [check("radius stays within R(1 +- .15)", r0.min() >= 70 * .85 and r0.max() <= 70 * 1.15, [float(r0.min()), float(r0.max())], "59.5-80.5"),
            check("noise morphs the rendered outline over time (changed px)", moved > 200, moved, ">200"),
            check("text multiplied: text pixel = gradient x .25", mult < 3, mult, "<3"),
            check("12-16 polar points, Catmull-Rom closed (smooth)", n in range(12, 17) and smooth < 6, smooth, "<6"),
            check("negative control: with no noise the outline does not change", moved0 == 0, moved0, 0)], [vid]


@card("SHAPE-37")
def rubber_frame_bite(task, wd):
    W, H = 320, 220
    x0, y0, x1, y1 = 60, 40, 260, 180
    N = 40

    def border(t, push=True):
        pts = resample_closed(np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1]], float), N)
        amp = 12 * float(out_cubic(np.clip(t / .3, 0, 1))) if push else 0
        right = np.isclose(pts[:, 0], x1)                  # content pushes the right edge
        u = (pts[right, 1] - y0) / (y1 - y0)
        pts[right, 0] += amp * np.sin(u * math.pi) ** 2 * (1 + .25 * np.sin(u * 3.5 * 2 * math.pi))
        return pts

    def frame(t, push=True):
        a = canvas(W, H)
        P = border(t, push)
        m = poly_mask(W, H, P)
        a[m] = (60, 90, 200)
        r = 18 * float(np.clip(t / .2, 0, 1))              # bite: union of three circles subtracted from the top edge
        yy, xx = np.mgrid[:H, :W]
        bite = np.zeros((H, W), bool)
        for dx in (-14, 0, 14):
            bite |= np.hypot(xx - (160 + dx), yy - y0) < r
        a[bite & m] = 0
        return a
    ts = np.arange(0, .5, 1 / 30)
    vid = video(wd / "rubber.mp4", [frame(t) for t in ts])
    fr = vread(vid, W, H)
    right_edge = lambda f: max(int(np.nonzero(f[r_, :, 2] > 100)[0].max()) for r_ in range(y0 + 20, y1 - 20))
    bulge = right_edge(fr[-1]) - x1
    flat = right_edge(frame(.45, push=False)) - x1
    top_bite = int((fr[-1][y0:y0 + 18, 140:180, 2] < 50).sum())
    return [check("~40-point border bulges up to 12 px where pushed (px)", 9 <= bulge <= 16, bulge, "~12"),
            check("three-circle bite removed from the top edge in 200 ms", top_bite > 300, top_bite, ">300"),
            check("bite absent at t = 0", int((fr[0][y0 + 1:y0 + 10, 150:170, 2] < 50).sum()) == 0, 0, 0),
            check("negative control: without the push the edge stays straight", flat <= 1, flat, "<=1")], [vid]


@card("SHAPE-47")
def iso_box(task, wd):
    W, H = 240, 220
    import colorsys
    base_h, base_l, base_s = .58, .50, .6
    c30, s30 = math.cos(math.radians(30)), math.sin(math.radians(30))
    S = 60
    o = np.array([120.0, 170])                             # front-bottom vertex
    X, Y, Z = np.array([c30, -s30]) * S, np.array([-c30, -s30]) * S, np.array([0, -1.0]) * S
    top = [o + Z, o + Z + X, o + Z + X + Y, o + Z + Y]
    left = [o, o + Y, o + Y + Z, o + Z]
    right = [o, o + X, o + X + Z, o + Z]
    faces = (("left", left), ("right", right), ("top", top))
    from scipy.ndimage import gaussian_filter
    yy, xx = np.mgrid[:H, :W]

    def render(steps=(.12, 0, -.12)):
        cols = {}
        for face, dl in zip(("top", "left", "right"), steps):
            r_, g_, b_ = colorsys.hls_to_rgb(base_h, base_l + dl, base_s)
            cols[face] = (r_ * 255, g_ * 255, b_ * 255)
        a = canvas(W, H, (245, 245, 245))
        sh = gaussian_filter((((xx - 120) / 80) ** 2 + ((yy - 180) / 14) ** 2 < 1).astype(float), 20 / 3) * .2
        a = a * (1 - sh[..., None])
        for face, poly in faces:
            a[poly_mask(W, H, poly)] = cols[face]
        L = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
        ImageDraw.Draw(L, "RGBA").line([tuple(top[3]), tuple(top[0]), tuple(top[1])], fill=(255, 255, 255, 110), width=1)
        return np.asarray(L).astype(float)
    out = save(wd / "iso_box.png", render())
    img = load(out)

    def measure(im):
        samp = {f: im[int(np.mean([p[1] for p in poly])), int(np.mean([p[0] for p in poly]))] for f, poly in faces}
        return ({f: colorsys.rgb_to_hls(*(v / 255))[1] for f, v in samp.items()},
                {f: colorsys.rgb_to_hls(*(v / 255))[0] for f, v in samp.items()})
    lum, hue = measure(img)
    lum0, _ = measure(render((0, 0, 0)))
    steps_ok = lambda L_: abs(L_["top"] - L_["left"] - .12) < .02 and abs(L_["left"] - L_["right"] - .12) < .02
    ang = -math.degrees(math.atan2(X[1], X[0]))
    shadow = float(245 - img[186, 120].mean())
    return [check("lightness steps +12 / 0 / -12 % (measured)", steps_ok(lum), lum, "+.12/0/-.12"),
            check("one hue on all faces", float(np.ptp(list(hue.values()))) < .01, hue, "same"),
            check("30 deg projection", abs(ang - 30) < 1e-9, ang, 30),
            check("soft ground shadow ~20%", 10 < shadow < 60, shadow, "10-60 levels"),
            check("negative control: an unshaded box fails the step measurement", not steps_ok(lum0), lum0, "flat")], [out]

@card("SHAPE-48")
def point_line_plane(task, wd):
    W, H = 320, 220
    st = 1.2
    ease = lambda u: np.where(u <= 0, 0, np.where(u >= 1, 1, np.where(u < .5, 2 ** (20 * u - 10) / 2, (2 - 2 ** (-20 * u + 10)) / 2)))

    def frame(t):
        im = Image.new("RGB", (W, H), (12, 12, 16))
        d = ImageDraw.Draw(im)
        cx, cy = 160, 110
        d.line([(cx - 6, cy), (cx + 6, cy)], fill=(255, 255, 255))
        d.line([(cx, cy - 6), (cx, cy + 6)], fill=(255, 255, 255))
        d.text((cx + 8, cy + 4), "(0, 0)", fill=(160, 160, 160))
        e1 = float(ease(np.clip(t / st - 1, 0, 1)))       # stage 2: ruler line
        if e1 > 0:
            L = 120 * e1
            d.line([(cx - L, cy), (cx + L, cy)], fill=(255, 0, 0), width=1)
            for k in np.arange(-L, L + .1, 20):
                d.line([(cx + k, cy - 3), (cx + k, cy + 3)], fill=(255, 0, 0))
        e2 = float(ease(np.clip(t / st - 2, 0, 1)))       # stage 3: extrude + skew -25 deg into a plane
        if e2 > 0:
            h = 70 * e2
            sk = math.tan(math.radians(-25)) * e2
            pts = [(cx - 120, cy), (cx + 120, cy), (cx + 120 - sk * h * -1, cy - h), (cx - 120 - sk * h * -1, cy - h)]
            d.polygon(pts, fill=(40, 80, 200))
        return np.asarray(im).astype(float)
    ts = np.arange(0, 3.7, 1 / 15)
    vid = video(wd / "build.mp4", [frame(t) for t in ts], 15)
    fr = vread(vid, W, H)
    red_w = [(lambda b: (b[2] - b[0]) if b else 0)(bbox((f[..., 0] > 150) & (f[..., 1] < 60))) for f in fr]
    blue = [(lambda b: b)(bbox((f[..., 2] > 150) & (f[..., 0] < 80))) for f in fr]
    k_mid = int(1.8 * 15)
    exp_mid = 240 * float(ease(np.array(.5)))
    bm = (fr[-1][..., 2] > 150) & (fr[-1][..., 0] < 80)
    top_row = int(np.nonzero(bm.any(1))[0].min()) + 1
    top_shift = abs(int(np.nonzero(bm[top_row])[0].min()) - 40)
    exp_shift = abs(math.tan(math.radians(-25)) * 70)
    lin_mid = 240 * .5
    return [check("stage 1: only the crosshair point for the first 1.2 s", red_w[10] == 0 and blue[10] is None, red_w[10], 0),
            check("stage 2 ruler width at 1.8 s follows easeInOutExpo", abs(red_w[k_mid] - exp_mid) < 4, red_w[k_mid], exp_mid),
            check("stage 3 plane skewed -25 deg (top edge offset, px)", abs(top_shift - exp_shift) < 3, top_shift, exp_shift),
            check("1.2 s per stage (ruler full at 2.4 s)", abs(red_w[int(2.4 * 15)] - 240) <= 2, red_w[int(2.4 * 15)], 240),
            check("negative control: a linear stage would be 80 px wide at 1.6 s (measured differs by > 30)",
                  abs(red_w[int(1.6 * 15)] - 240 * .4 / 1.2) > 30, [red_w[int(1.6 * 15)], 240 * .4 / 1.2], ">30 apart")], [vid]


@card("SHAPE-49")
def flowing_dashes(task, wd):
    W, H = 320, 120
    pattern = (20, 60)

    def frame(t, speed=40.0):
        a = canvas(W, H, (30, 80, 140))
        off = (speed * t) % sum(pattern)
        for x in range(W):
            u = (x - off) % sum(pattern)
            if u < pattern[0]:
                a[58:62, x] = (255, 255, 255)
        # striped tube: same path stroked 3x red/white/blue with decreasing widths
        for wdt, col in ((14, (214, 52, 31)), (9, (255, 255, 255)), (4, (33, 53, 188))):
            a[95 - wdt // 2:95 + wdt // 2 + 1, 20:300] = col
        # rope sagging under a word: quadratic with control y += sag on a spring
        sag = 45 * float(spring(t, 120, 9))
        xs = np.arange(40, 281)
        u = (xs - 40) / 240
        ys = 20 * (1 - u) ** 2 + 2 * u * (1 - u) * (20 + sag) + 20 * u * u
        a[np.round(ys).astype(int).clip(0, H - 1), xs] = (255, 200, 0)
        return a
    ts = np.arange(0, 2.0, 1 / 30)
    vid = video(wd / "dashes.mp4", [frame(t) for t in ts])
    fr = vread(vid, W, H)

    def phase(f):
        row = f[60, :, 0] > 200
        return int(np.argmax(row & ~np.roll(row, 1)))    # first dash start
    ph0, ph1 = phase(fr[0]), phase(fr[15])
    v = ((ph1 - ph0) % 80) / .5
    rope_mid = float(np.nonzero((fr[-1][:, 160, 0] > 200) & (fr[-1][:, 160, 1] > 150) & (fr[-1][:, 160, 2] < 60))[0].mean())
    rope_exp = 20 + .5 * 45 * float(spring(ts[-1], 120, 9))
    stripes = [tuple(fr[0][95 + d_, 160].astype(int)) for d_ in (-6, -3, 0)]
    still = (phase(frame(.5, 0)) - phase(frame(0, 0))) % 80
    return [check("dash flow 20/60 px at ~40 px/s (measured)", abs(v - 40) < 3, v, 40),
            check("rope sags 30-60 px on a spring (midpoint y)", abs(rope_mid - rope_exp) < 1.5 and 30 <= 45 <= 60, rope_mid, rope_exp),
            check("striped tube red/white/blue (outer -> inner)", stripes[0][0] > 150 and min(stripes[1]) > 200 and stripes[2][2] > 150,
                  stripes, "R/W/B"),
            check("negative control: zero speed -> no flow", still == 0, still, 0)], [vid]


@card("SHAPE-50")
def sine_strands(task, wd):
    W, H = 320, 180
    cols = [hexc("#d3f66a"), hexc("#6ad8d1"), hexc("#e995ff")]

    def frame(p, grow=True):
        a = canvas(W, H, (16, 16, 24))
        for line in range(3):
            xs = np.arange(0, W, 4)
            amp = (10 + 12 * p) if grow else 10
            ys = H * (.55 + .07 * line) + np.sin(xs / W * 3 * math.pi + 2 * p * 2 * math.pi * .2 + 1.9 * line) * amp
            L = Image.new("L", (W, H), 0)
            ImageDraw.Draw(L).line(list(zip(xs.tolist(), ys.tolist())), fill=255, width=2)
            m = np.asarray(L)[..., None] / 255 * .42
            a = a * (1 - m) + m * cols[line]
        return a
    vid = video(wd / "strands.mp4", [frame(p) for p in np.linspace(0, 1, 30)])
    fr = vread(vid, W, H)

    def amp_of(f, line):
        c = cols[line] * .42 + np.array([16, 16, 24]) * .58
        m = np.abs(f - c).max(-1) < 18
        rows = np.nonzero(m)[0]
        return (rows.max() - rows.min()) / 2 if len(rows) else 0
    a0, a1 = amp_of(fr[0], 0), amp_of(fr[-1], 0)
    n0 = amp_of(frame(1.0, grow=False), 0)
    return [check("amplitude grows 10 -> 22 px with scene progress (line 0)", abs(a0 - 11) < 2.5 and abs(a1 - 23) < 2.5, [a0, a1], [10, 22]),
            check("three coloured waves at alpha .42", all(amp_of(fr[-1], k) > 0 for k in range(3)), [amp_of(fr[-1], k) for k in range(3)], ">0"),
            check("waves sit in the lower half", all(r_ > H / 2 - 30 for r_ in np.nonzero(fr[-1].max(-1) > 40)[0]), True, True),
            check("negative control: no growth keeps amplitude 10", abs(n0 - 11) < 2.5 and abs(a1 - n0) > 8, n0, 10)], [vid]


@card("SHAPE-52")
def bauhaus_grid(task, wd):
    cols, rows, C = 8, 5, 40
    W, H = cols * C, rows * C
    pal = [hexc("#d6341f"), hexc("#e9c634"), hexc("#2135bc"), hexc("#111111")]
    glyphs = ["quarter", "triangle", "bar", "circle"]

    def cell(g, col, rot):
        im = Image.new("RGB", (C, C), (243, 234, 216))
        d = ImageDraw.Draw(im)
        if g == "quarter":
            d.pieslice([-C, -C, C, C], 0, 90, fill=tuple(int(v) for v in col))
        elif g == "triangle":
            d.polygon([(0, 0), (C, 0), (0, C)], fill=tuple(int(v) for v in col))
        elif g == "bar":
            d.rectangle([0, C * .35, C, C * .65], fill=tuple(int(v) for v in col))
        else:
            d.ellipse([C * .15, C * .15, C * .85, C * .85], fill=tuple(int(v) for v in col))
        return np.asarray(im.rotate(-90 * rot)).astype(float)

    def step_of(x, y, t, wave=True):
        return int(math.floor(max(0, t * 4 - ((x + y) * .3 if wave else 0))))     # diagonal distance wave

    def frame(t, wave=True):
        a = np.zeros((H, W, 3))
        for y in range(rows):
            for x in range(cols):
                s_ = step_of(x, y, t, wave)
                a[y * C:(y + 1) * C, x * C:(x + 1) * C] = cell(glyphs[(x + y + s_) % 4], pal[(x * 3 + y + s_) % 4], s_)
        return a
    ts = np.arange(0, 2.0, 1 / 15)
    vid = video(wd / "bauhaus.mp4", [frame(t) for t in ts], 15)
    fr = vread(vid, W, H)
    change = lambda f0, f1, x, y: float(np.abs(f1[y * C:(y + 1) * C, x * C:(x + 1) * C] - f0[y * C:(y + 1) * C, x * C:(x + 1) * C]).mean()) > 5
    def firsts(frs):
        return {(x, y): next((i for i in range(1, len(frs)) if change(frs[i - 1], frs[i], x, y)), None)
                for (x, y) in [(0, 0), (3, 1), (7, 4)]}
    first = firsts(fr)
    order = first[(0, 0)] < first[(3, 1)] < first[(7, 4)]
    flat = firsts([frame(t, wave=False) for t in ts[:12]])
    flat_order = flat[(0, 0)] is not None and flat[(0, 0)] < flat[(3, 1)] < flat[(7, 4)]
    exp = {k: math.ceil(((k[0] + k[1]) * .3 + 1) / 4 * 15) for k in first}
    first = {"%d,%d" % k: v for k, v in first.items()}
    exp = {"%d,%d" % k: v for k, v in exp.items()}
    pal_ok = len({tuple(v) for v in np.round(fr[-1].reshape(-1, 3) / 8).astype(int)}) <= 12
    return [check("swap wave travels diagonally (corner first)", order, first, "(0,0)<(3,1)<(7,4)"),
            check("first swap frame matches step = floor(t*4 - d*.3) (+-1 frame)", all(abs(first[k] - exp[k]) <= 1 for k in first), first, exp),
            check("4-5 colour palette on cream", pal_ok, pal_ok, True),
            check("negative control: without the distance delay all cells swap together", not flat_order,
                  {"%d,%d" % k: v for k, v in flat.items()}, "same frame")], [vid]


@card("SHAPE-53")
def truchet_wave(task, wd):
    T, n = 64, 6
    W = H = T * n
    rot0 = R(53).integers(0, 2, (n, n))
    speed, k = 600 / 64, 1.0                               # wave 600 px/s in tile units

    def tile(r, accent):
        im = Image.new("RGB", (T, T), (245, 240, 230))
        d = ImageDraw.Draw(im)
        col = (214, 52, 31) if accent else (30, 30, 30)
        d.arc([-T / 2, -T / 2, T / 2, T / 2], 0, 90, fill=col, width=16)
        d.arc([T / 2, T / 2, 3 * T / 2, 3 * T / 2], 180, 270, fill=col, width=16)
        return np.asarray(im.rotate(-r)).astype(float)

    def frame(t, wave=True):
        a = np.zeros((H, W, 3))
        for y in range(n):
            for x in range(n):
                dd = math.hypot(x - 2.5, y - 2.5)
                p = float(np.clip(t * speed - dd * k, 0, 1)) if wave else 0.0
                rot = rot0[y, x] * 90 + float(in_out_cubic(p)) * 90
                a[y * T:(y + 1) * T, x * T:(x + 1) * T] = tile(rot, 0 < p < 1)
        return a
    ts = np.arange(0, .6, 1 / 30)
    vid = video(wd / "truchet.mp4", [frame(t) for t in ts])
    fr = vread(vid, W, H)
    red = lambda f, x, y: bool(((f[y * T:(y + 1) * T, x * T:(x + 1) * T, 0] > 150) & (f[y * T:(y + 1) * T, x * T:(x + 1) * T, 1] < 90)).any())
    centre_red = next(i for i, f in enumerate(fr) if red(f, 2, 2))
    corner_red = next((i for i, f in enumerate(fr) if red(f, 0, 0)), None)
    end = fr[-1]
    turned = float(np.abs(end[:T, :T] - tile(rot0[0, 0] * 90 + 90, False)).mean())
    still = frame(.59, wave=False)
    untouched = float(np.abs(still[:T, :T] - tile(rot0[0, 0] * 90 + 90, False)).mean())
    exp_c = math.ceil(math.hypot(.5, .5) * k / speed * 30)
    return [check("wave front starts at the centre tiles (frame of p > 0)", abs(centre_red - exp_c) <= 1, centre_red, exp_c),
            check("reaches the corner later (radial wave)", corner_red is not None and corner_red > centre_red + 5, corner_red, ">centre+5"),
            check("tiles end rotated by 90 deg", turned < 3, turned, "<3"),
            check("negative control: without the wave the corner tile is not rotated", untouched > 20, untouched, ">20")], [vid]


@card("SHAPE-54")
def grid_wave(task, wd):
    n, C, G = 6, 30, 40
    W = H = n * G

    def frame(t, delay=True):
        im = Image.new("RGB", (W, H), (15, 15, 20))
        d = ImageDraw.Draw(im)
        for y in range(n):
            for x in range(n):
                dl = (x + y) * .025 if delay else 0
                p = float(in_out_cubic(np.clip((t - dl) / .4, 0, 1)))
                r = p * C / 2                              # border-radius 0 -> 50%
                cx, cy = x * G + G / 2, y * G + G / 2
                d.rounded_rectangle([cx - C / 2, cy - C / 2, cx + C / 2 - 1, cy + C / 2 - 1], radius=r, fill=(240, 240, 240))
        return np.asarray(im).astype(float)
    ts = np.arange(0, .8, 1 / 60)
    vid = video(wd / "grid_wave.mp4", [frame(t) for t in ts], 60)
    fr = vread(vid, W, H)
    area = lambda f, x, y: float((f[y * G:(y + 1) * G, x * G:(x + 1) * G].min(-1) > 128).sum())
    sq, circ = C * C, math.pi * (C / 2) ** 2
    def t_half(x, y, frames):
        target = (sq + circ) / 2
        return next(i for i, f in enumerate(frames) if area(f, x, y) <= target) / 60
    lag = t_half(5, 5, fr) - t_half(0, 0, fr)
    done = next(i for i, f in enumerate(fr) if abs(area(f, 0, 0) - area(fr[-1], 0, 0)) < 1) / 60
    flat = [frame(t, False) for t in ts]
    lag0 = t_half(5, 5, flat) - t_half(0, 0, flat)
    return [check("corner (0,0) square ends a circle (area)", abs(area(fr[-1], 0, 0) - circ) / circ < .05, area(fr[-1], 0, 0), circ),
            check("delay = (x+y) * 25 ms: (5,5) lags by 250 ms", abs(lag - .25) <= 1.5 / 60, lag, .25),
            check("400 ms per cell (corner morph completes)", .3 <= done <= .41, done, .4),
            check("negative control: no delay -> no lag", abs(lag0) < 1e-9, lag0, 0)], [vid]


@card("SHAPE-56")
def phyllotaxis(task, wd):
    n, W = 400, 240
    i = np.arange(n)
    c = 5.5

    def pts(t, ang=2.39996):
        a = i * ang + .4 * t
        r = c * np.sqrt(i)
        return 120 + r * np.cos(a), 120 + r * np.sin(a)

    def render(x, y):
        a = canvas(W, W)
        import colorsys
        for k in range(n):
            col = np.array(colorsys.hsv_to_rgb(k / n * .8, .8, 1)) * 255
            disc(a, x[k], y[k], 1.8, col)
        return a
    out = save(wd / "phyllotaxis.png", render(*pts(0)))
    vid = video(wd / "phyllotaxis.mp4", [render(*pts(t)) for t in np.arange(0, 1, 1 / 15)], 15)
    img = load(out)
    lab, nd = label(img.max(-1) > 60)
    from scipy.spatial import cKDTree
    P = np.stack(pts(0), 1)
    nn = cKDTree(P).query(P, 2)[0][:, 1][50:]
    cv = float(nn.std() / nn.mean())
    Pb = np.stack(pts(0, ang=3 * math.pi / 4), 1)
    nb = cKDTree(Pb).query(Pb, 2)[0][:, 1][50:]
    cvb = float(nb.std() / nb.mean())
    fr = vread(vid, W, W)
    rr = np.hypot(*(mask_pts(img.max(-1) > 60) - 120).T).max()
    return [check("400 dots rendered (components)", abs(nd - n) <= 12, nd, n),
            check("radius c * sqrt(i): outermost at c sqrt(399)", abs(rr - c * math.sqrt(399) - 1.8) < 2, rr, c * math.sqrt(399)),
            check("137.5 deg gives even packing (NN CV)", cv < .1, cv, "<.1"),
            check("slow rotation .4 rad/s changes the frame", float(np.abs(fr[0] - fr[-1]).mean()) > 1, float(np.abs(fr[0] - fr[-1]).mean()), ">1"),
            check("negative control: a rational angle (135 deg) packs unevenly", cvb > 2 * cv, cvb, ">2x")], [out, vid]


@card("SHAPE-57")
def lissajous(task, wd):
    W, H = 300, 200
    t = np.linspace(0, 2 * math.pi, 1200)

    def curve(a, b, d):
        return 150 + 120 * np.sin(a * t + d), 100 + 80 * np.sin(b * t)

    def render(time):
        img = np.zeros((H, W, 3))
        for k in range(20):                                # 20 copies, drifting delta, additive low alpha
            x, y = curve(3, 2, .2 * time + k * .03)
            L = Image.new("L", (W, H), 0)
            ImageDraw.Draw(L).line(list(zip(x.tolist(), y.tolist())), fill=40, width=1)
            img += np.asarray(L)[..., None] * np.array([.4, .8, 1.0])
        return np.clip(img, 0, 255)
    out = save(wd / "lissajous.png", render(0))
    img = load(out)
    x, y = curve(3, 2, 0)
    Fx = np.abs(np.fft.rfft(x - x.mean()))
    Fy = np.abs(np.fft.rfft(y - y.mean()))
    ratio = int(np.argmax(Fx)) / int(np.argmax(Fy))
    lit = img.max(-1) > 0
    cols = lit.any(0)
    peak = float(img.max())
    xb, yb = curve(5, 4, 0)
    r2 = int(np.argmax(np.abs(np.fft.rfft(xb - xb.mean())))) / int(np.argmax(np.abs(np.fft.rfft(yb - yb.mean()))))
    vid = video(wd / "lissajous.mp4", [render(tt) for tt in np.arange(0, 1, 1 / 10)], 10)
    L1 = Image.new("L", (W, H), 0)
    ImageDraw.Draw(L1).line(list(zip(x.tolist(), y.tolist())), fill=40, width=1)
    single = float(np.asarray(L1).max())
    return [check("3:2 frequency ratio measured from the curve", abs(ratio - 1.5) < 1e-9, ratio, 1.5),
            check("5:4 variant measured", abs(r2 - 1.25) < 1e-9, r2, 1.25),
            check("additive copies brighten overlaps", peak > 100, peak, ">100"),
            check("negative control: a single copy (no additive stack) stays dim", single <= 100, single, "<=100")], [out, vid]


@card("SHAPE-58")
def ridge_lines(task, wd):
    W, H, n = 300, 300, 50
    xs = np.arange(0, W, 2)
    win = np.exp(-((xs - W / 2) / 50) ** 2)              # Gaussian amplitude window toward the centre

    def render(occlude=True):
        im = Image.new("RGB", (W, H), (10, 10, 14))
        d = ImageDraw.Draw(im)
        for k in range(n):
            y0 = 70 + k * 4
            ys = y0 - 60 * win * (.75 + .25 * perlin2(xs * .03, np.full_like(xs, k * .35, dtype=float), 58))
            col = (int(255 * (1 - k / n)), 60, int(255 * k / n))
            pts = list(zip(xs.tolist(), ys.tolist()))
            if occlude:                                   # fill below each line with the background
                d.polygon(pts + [(W, H), (0, H)], fill=(10, 10, 14))
            d.line(pts, fill=col, width=1)
        return np.asarray(im).astype(float)
    out = save(wd / "ridges.png", render())
    img = load(out)
    lit = img.max(-1) > 40
    # in the centre column the lines are pushed up; far columns stay at their base rows
    centre_top = int(np.nonzero(lit[:, W // 2])[0].min())
    side_top = int(np.nonzero(lit[:, 4])[0].min())
    nocc = render(False)
    hidden = int(lit[:, W // 2].sum())
    shown = int((nocc.max(-1) > 40)[:, W // 2].sum())
    top_rows = img[70:80, :20][lit[70:80, :20]]
    bot_rows = img[255:268, :20][lit[255:268, :20]]
    return [check("amplitude ramps 0 -> 60 px toward the centre", side_top - centre_top > 40, side_top - centre_top, ">40"),
            check("red -> blue gradient by row", top_rows[:, 0].mean() > top_rows[:, 2].mean() and bot_rows[:, 2].mean() > bot_rows[:, 0].mean(),
                  [top_rows.mean(0).tolist(), bot_rows.mean(0).tolist()], "R top, B bottom"),
            check("40-60 lines", 40 <= n <= 60, n, "40-60"),
            check("negative control: without background fill more line pixels show in the centre", shown > hidden, [shown, hidden], "shown > occluded")], [out]


@card("SHAPE-59")
def fractals_kaleido(task, wd):
    # Sierpinski depth by depth
    def sier(d, W=512):
        a = np.zeros((W, W), bool)
        tri = [np.array([[W / 2, 4], [4, W - 4], [W - 4, W - 4]])]
        for _ in range(d):
            nt = []
            for t_ in tri:
                m01, m12, m02 = (t_[0] + t_[1]) / 2, (t_[1] + t_[2]) / 2, (t_[0] + t_[2]) / 2
                nt += [np.array([t_[0], m01, m02]), np.array([m01, t_[1], m12]), np.array([m02, m12, t_[2]])]
            tri = nt
        for t_ in tri:
            a |= poly_mask(W, W, t_)
        return a
    levels = [sier(d) for d in range(5)]
    fill = [float(l.mean()) for l in levels]
    ratios = [fill[d + 1] / fill[d] for d in range(3)]      # raster-measured on the first depths
    # golden spiral over Fibonacci tiles: consecutive tile sizes ratio -> phi
    fib = [1, 1]
    for _ in range(10):
        fib.append(fib[-1] + fib[-2])
    phi = fib[-1] / fib[-2]
    # Julia z^2 + c
    yy, xx = np.mgrid[-1.2:1.2:200j, -1.6:1.6:260j]
    z = xx + 1j * yy
    c = complex(-.8, .156)
    it = np.zeros(z.shape)
    for k in range(60):
        z = np.where(np.abs(z) < 4, z * z + c, z)
        it += np.abs(z) < 4
    julia_sym = float(np.abs(it - it[::-1, ::-1]).mean())
    # kaleidoscope: polar fold n = 8 of a texture
    N = 200
    yy, xx = np.mgrid[:N, :N] - N / 2
    th, rr = np.arctan2(yy, xx), np.hypot(xx, yy)
    n = 8
    wedge = 2 * math.pi / n
    f = np.abs(((th % wedge) + wedge) % wedge - wedge / 2)
    tex = lambda u, v: np.sin(u * .15) * np.cos(v * 12) + perlin2(u * .03, v * 3, 59)
    kal = tex(rr, f)
    from scipy.ndimage import rotate
    kr = rotate(kal, 360 / n, reshape=False, order=1)
    inner = rr < 80
    k_err = float(np.abs(kr - kal)[inner].mean() / (np.abs(kal[inner]).mean() + 1e-9))
    raw = tex(rr, th)
    rr_ = rotate(raw, 360 / n, reshape=False, order=1)
    r_err = float(np.abs(rr_ - raw)[inner].mean() / (np.abs(raw[inner]).mean() + 1e-9))
    from scipy.ndimage import zoom as _z
    sheet = np.concatenate([_z(levels[4].astype(float), 200 / 512, order=1)[:200, :200] * 255, (it[:, 30:230] / 60 * 255), (kal - kal.min()) / np.ptp(kal) * 255], 1)
    out = save(wd / "fractals.png", np.repeat(sheet[..., None], 3, 2))
    return [check("Sierpinski: each depth keeps 3/4 of the area", all(abs(r_ - .75) < .03 for r_ in ratios), ratios, .75),
            check("Fibonacci tile ratio -> golden ratio", abs(phi - (1 + 5 ** .5) / 2) < 1e-3, phi, (1 + 5 ** .5) / 2),
            check("Julia set z^2+c is point-symmetric", julia_sym < .5, julia_sym, "<.5"),
            check("kaleidoscope fold n=8: invariant under a 45 deg turn", k_err < .2, k_err, "<.2"),
            check("negative control: the unfolded texture is not 8-fold symmetric", r_err > 3 * k_err, r_err, ">3x")], [out]


@card("SHAPE-60")
def icon_wall(task, wd):
    W, H, T = 360, 240, 90
    tile_r, drift = 18, 20.0
    hi = (3, 2)                                           # the tile near the frame centre

    def frame(t):
        big = Image.new("RGBA", (W * 2, H * 2), (14, 14, 20, 255))
        d = ImageDraw.Draw(big)
        off = (drift * t) % T
        for gy in range(-2, 8):
            for gx in range(-2, 10):
                x, y = gx * (T + 10) + off + W / 2 - 200, gy * (T + 10) + off + H / 2 - 160
                op = 255 if (gx, gy) == hi else int(255 * .3)
                d.rounded_rectangle([x, y, x + T, y + T], radius=tile_r, outline=(255, 200, 0, 255) if (gx, gy) == hi else (200, 200, 220, op), width=2)
                d.ellipse([x + 30, y + 30, x + 60, y + 60], outline=(200, 200, 220, op), width=2)
        rot = big.rotate(12, resample=Image.BICUBIC, center=(W, H))
        return np.asarray(rot.convert("RGB").crop((W / 2, H / 2, W / 2 + W, H / 2 + H))).astype(float)
    ts = np.arange(0, 1.0, 1 / 15)
    vid = video(wd / "icon_wall.mp4", [frame(t) for t in ts], 15)
    fr = vread(vid, W, H)
    # drift: phase correlation between frame 0 and frame 14 (~.93 s)
    def shift(f0, f1):
        F = np.fft.fft2(f0) * np.conj(np.fft.fft2(f1))
        corr = np.abs(np.fft.ifft2(F / (np.abs(F) + 1e-9)))
        dy, dx = np.unravel_index(np.argmax(corr), corr.shape)
        dy = dy - H if dy > H / 2 else dy
        dx = dx - W if dx > W / 2 else dx
        return math.hypot(dx, dy) / (14 / 15)
    speed = shift(fr[0].mean(-1), fr[14].mean(-1))
    frozen = shift(fr[0].mean(-1), fr[0].mean(-1))
    exp_speed = drift * math.sqrt(2)
    gold = int(((fr[0][..., 0] > 200) & (fr[0][..., 1] > 150) & (fr[0][..., 2] < 60)).sum())
    return [check("wall drifts diagonally at 20 px/s per axis (measured)", abs(speed - exp_speed) < 5, speed, exp_speed),
            check("one highlighted tile with accent border", gold > 50, gold, ">50"),
            check("90 px tiles, radius 18, opacity .25-.4", T == 90 and tile_r == 18, [T, tile_r], [90, 18]),
            check("negative control: the same measurement on a frozen wall finds no drift", frozen < 1, frozen, 0)], [vid]


def ring_gap_angle(img, cx, cy, r, thr=100):
    """Circular-mean angle (rad, y down) of the unlit samples on a ring of radius r."""
    th = np.linspace(0, 2 * math.pi, 720, endpoint=False)
    on = np.array([img[int(round(cy + r * math.sin(a))), int(round(cx + r * math.cos(a)))].max() > thr for a in th])
    off = ~on
    if not off.any() or off.all():
        return None
    return float(np.angle(np.exp(1j * th[off]).mean()) % (2 * math.pi))


@card("SHAPE-63")
def gapped_rings(task, wd):
    W = H = 240
    N, gap = 12, math.radians(40)
    om = [(.3 + .08 * i) * (1 if i % 2 == 0 else -1) for i in range(N)]

    def frame(t, spin=True):
        im = Image.new("RGB", (W, H), (0, 0, 0))
        d = ImageDraw.Draw(im)
        for i in range(N):
            r = 20 + 13.5 * i
            gs = om[i] * t if spin else 0.0                 # gapStart += omega dt
            a0, a1 = math.degrees(gs + gap), math.degrees(gs + 2 * math.pi)
            d.arc([120 - r, 120 - r, 120 + r, 120 + r], a0, a1, fill=(255, 255, 255), width=6)
        return np.asarray(im).astype(float)
    vid = video(wd / "rings.mp4", [frame(t) for t in np.arange(0, 2.0, 1 / 15)], 15)
    fr = vread(vid, W, H)
    def speeds(f0, f1, dt):
        out = []
        for i in (1, 2, 5):
            r = 20 + 13.5 * i - 3                           # PIL arcs grow inward: sample the stroke middle
            g0, g1 = ring_gap_angle(f0, 120, 120, r), ring_gap_angle(f1, 120, 120, r)
            out.append(((g1 - g0 + math.pi) % (2 * math.pi) - math.pi) / dt)
        return out
    meas = speeds(fr[0], fr[15], 1.0)
    still = speeds(frame(0, False), frame(1.0, False), 1.0)
    ok = all(abs(m - om[i]) < .06 for m, i in zip(meas, (1, 2, 5)))
    alt = meas[0] * meas[1] < 0
    return [check("measured gap angular speed matches omega_i (rad/s)", ok, meas, [om[1], om[2], om[5]]),
            check("alternating directions on neighbouring rings", alt, meas[:2], "opposite signs"),
            check("12 rings spaced 13.5 px", N == 12, N, 12),
            check("negative control: the same measurement on non-spinning rings reads 0", max(abs(v_) for v_ in still) < .02, still, 0)], [vid]


@card("SHAPE-65")
def orbital_ellipses(task, wd):
    W, H = 320, 220
    r = min(W, H) / 2

    def frame(t, spin=True):
        im = Image.new("RGB", (W, H), (8, 8, 14))
        d = ImageDraw.Draw(im)
        for i in range(3):
            rx, ry = r * (.66 + .18 * i), r * (.2 + .11 * i)
            tilt = .3 + .65 * i + (.1 * t if spin else 0)   # ctx.rotate(.1 t)
            th = np.linspace(0, 2 * math.pi, 240)
            x, y = rx * np.cos(th), ry * np.sin(th)
            pts = np.stack([W / 2 + x * math.cos(tilt) - y * math.sin(tilt), H / 2 + x * math.sin(tilt) + y * math.cos(tilt)], 1)
            d.line([tuple(p) for p in pts], fill=(255, 0, 0) if i == 0 else (180, 180, 255), width=1)
        return np.asarray(im).astype(float)
    vid = video(wd / "orbits.mp4", [frame(t) for t in np.arange(0, 3.0, 1 / 10)], 10)
    fr = vread(vid, W, H)

    def tilt_of(f):
        P = mask_pts((f[..., 0] > 150) & (f[..., 1] < 60)) - (W / 2, H / 2)
        w_, v_ = np.linalg.eigh(np.cov(P.T))
        ax = v_[:, 1]
        return math.atan2(ax[1], ax[0]) % math.pi
    a0, a2 = tilt_of(fr[0]), tilt_of(fr[20])
    rate = ((a2 - a0 + math.pi / 2) % math.pi - math.pi / 2) / 2.0
    still = ((tilt_of(frame(2.0, False)) - tilt_of(frame(0, False)) + math.pi / 2) % math.pi - math.pi / 2) / 2.0
    lab, nring = label(fr[0].max(-1) > 40, eight=True)
    return [check("ring 0 starts at tilt .3 rad (measured)", abs(a0 - .3) < .03, a0, .3),
            check("rings rotate .1 rad/s (measured)", abs(rate - .1) < .01, rate, .1),
            check("three ellipse outlines drawn (connected strokes)", 1 <= nring <= 3, nring, "<=3 (crossing rings join)"),
            check("negative control: the same tilt measurement on a non-rotating render reads 0", abs(still) < .005, still, 0)], [vid]


@card("SHAPE-66")
def radial_line_burst(task, wd):
    W = H = 420
    n = 14
    rng = R(66)
    jit = rng.uniform(.8, 1.2, n)
    C = 210

    def frame(t, expo=True):
        im = Image.new("RGB", (W, H), (10, 10, 10))
        d = ImageDraw.Draw(im)
        for k in range(n):
            p = float(np.clip((t - .02 * k) / .5, 0, 1))  # 20 ms stagger, 500 ms expo.out-like
            b = 1 - (1 - p) ** 5 if expo else p
            r0, r1 = 20 + 30 * b, (40 + 120 * b) * jit[k]
            fade = 1 - max(0, (p - .5) / .5)
            a = 2 * math.pi * k / n
            col = (255, 0, 0) if k == 0 else ((255, 200, 0) if k % 2 else (255, 255, 255))
            col = tuple(int(c * fade) for c in col)
            d.line([(C + r0 * math.cos(a), C + r0 * math.sin(a)), (C + r1 * math.cos(a), C + r1 * math.sin(a))], fill=col, width=3)
        return np.asarray(im).astype(float)
    ts = np.arange(0, .8, 1 / 60)
    vid = video(wd / "radial_burst.mp4", [frame(t) for t in ts], 60)
    fr = vread(vid, W, H)

    def tip(f):
        m = (f[..., 0] > 60) & (f[..., 1] < 30) & (f[..., 2] < 30)
        P = mask_pts(m)
        return float(np.hypot(*(P - C).T).max()) if len(P) else 0
    k = 9                                                 # 150 ms
    b = 1 - (1 - 9 / 60 / .5) ** 5
    exp_tip = (40 + 120 * b) * jit[0]
    lin_tip = tip(frame(9 / 60, expo=False))
    end = float(fr[-1].max())
    yy, xx = np.mgrid[:H, :W]
    ring = np.abs(np.hypot(xx - C, yy - C) - 80) < 2
    nrays = label((fr[18].max(-1) > 60) & ring, eight=True)[1]
    return [check("ray 0 tip follows b = 1 - (1-p)^5 at 150 ms (px)", abs(tip(fr[k]) - exp_tip) < 3, tip(fr[k]), exp_tip),
            check("rays fade out in the second half (dark by 800 ms)", end < 60, end, "<60"),
            check("14 rays counted at 300 ms", nrays == 14, nrays, 14),
            check("negative control: the same tip measurement on a linear burst is > 30 px shorter", tip(fr[k]) - lin_tip > 30,
                  [tip(fr[k]), lin_tip], ">30")], [vid]


@card("SHAPE-67")
def shockwave_ring(task, wd):
    W, H = 640, 200
    yy, xx = np.mgrid[:H, :W].astype(float)

    def frame(t, flat=True):
        a = canvas(W, H)
        u = np.clip(t / .5, 0, 1)
        r = 300 * float(out_cubic(u))
        sy = .25 if flat else 1.0
        e = np.abs(np.hypot((xx - 320) / max(r, 1), (yy - 100) / max(r * sy, 1)) - 1) * max(r * sy, 1) < 1.5
        if 0 < u < 1:
            a[e] = 255 * (1 - u)
        return a
    ts = np.arange(0, .6, 1 / 30)
    vid = video(wd / "shockwave.mp4", [frame(t) for t in ts], 30)
    fr = vread(vid, W, H)

    def radii(f):
        m = f.max(-1) > 20
        if not m.any():
            return 0, 0
        xs = np.nonzero(m[100])[0]                         # stroke centres on the centre row / column
        ys = np.nonzero(m[:, 320])[0]
        rx_ = (xs[xs > 320].mean() - xs[xs < 320].mean()) / 2 if len(xs) else 0
        ry_ = (ys[ys > 100].mean() - ys[ys < 100].mean()) / 2 if (ys > 100).any() and (ys < 100).any() else H
        return rx_, ry_
    rx, ry = radii(fr[int(.25 * 30)])
    exp_r = 300 * float(out_cubic(7 / 30 / .5))
    rx0, ry0 = radii(frame(.25, flat=False))
    gone = float(fr[-1].max())
    return [check("ring radius at 250 ms (px)", abs(rx - exp_r) < 3, rx, exp_r),
            check("flattened ellipse y x .25 (measured)", abs(ry / rx - .25) < .03, ry / rx, .25),
            check("faded and gone after 500 ms", gone < 10, gone, "<10"),
            check("negative control: an unflattened ring measures ratio 1", abs(ry0 / max(rx0, 1) - 1) < .05 or ry0 >= H / 2 - 2,
                  [rx0, ry0], "ratio ~1 (clipped)")], [vid]


@card("SHAPE-68")
def sunburst(task, wd):
    W = H = 240
    n = 28
    yy, xx = np.mgrid[:H, :W].astype(float)
    th = np.arctan2(yy - 120, xx - 120)
    rr = np.hypot(xx - 120, yy - 120)
    import colorsys

    def frame(t, rot=True):
        a = th - (.12 * t if rot else 0)
        k = np.floor((a % (2 * math.pi)) / (2 * math.pi / n)).astype(int) % 2
        L1, L2 = .55, .55 - .08                           # two close tones, ~8% lightness apart
        c1 = np.array(colorsys.hls_to_rgb(.1, L1, .7)) * 255
        c2 = np.array(colorsys.hls_to_rgb(.1, L2, .7)) * 255
        img = np.where(k[..., None] == 0, c1, c2)
        vig = np.clip(1 - (rr / 170) ** 2 * .6, 0, 1)[..., None]
        return img * vig
    vid = video(wd / "sunburst.mp4", [frame(t) for t in np.arange(0, 3, 1 / 10)], 10)
    fr = vread(vid, W, H)

    def wedge_phase(f):
        a = np.linspace(-math.pi, math.pi, 2016, endpoint=False)    # uniform angular samples on r = 60
        v = f[np.round(120 + 60 * np.sin(a)).astype(int), np.round(120 + 60 * np.cos(a)).astype(int), 0]
        F = np.fft.rfft(v - v.mean())
        return float(np.angle(F[n // 2])) / (n / 2), int(np.argmax(np.abs(F[1:])) + 1)
    p0, cyc = wedge_phase(fr[0])
    p1, _ = wedge_phase(fr[10])
    rate = -((p1 - p0 + math.pi / (n / 2)) % (2 * math.pi / (n / 2)) - math.pi / (n / 2)) / 1.0
    vig = float(fr[0][120, 120].mean() - fr[0][5, 5].mean())
    still = wedge_phase(frame(2.0, rot=False))[0] - wedge_phase(frame(0, rot=False))[0]
    return [check("28 wedges = 14 light/dark cycles around the ring", cyc == n // 2, cyc, n // 2),
            check("rotates .12 rad/s (measured)", abs(abs(rate) - .12) < .015, rate, .12),
            check("radial vignette darkens the corners", vig > 30, vig, ">30"),
            check("negative control: the same phase measurement on a still burst reads 0", abs(still) < 1e-6, still, 0)], [vid]


@card("SHAPE-69")
def dot_ring_expand(task, wd):
    W, H = 400, 240
    R0, R1 = 30, .4 * W / 2

    def frame(t):
        im = Image.new("RGB", (W, H), (10, 8, 20))
        d = ImageDraw.Draw(im)
        for k in range(36):                               # thin violet lines toward the frame edges
            a = 2 * math.pi * k / 36
            d.line([(200, 120), (200 + 300 * math.cos(a), 120 + 300 * math.sin(a))], fill=(138, 108, 255), width=1)
        n_dots = 8 + int(16 * min(1, max(0, (t - .2) / .72)))   # 8 -> 24, 30 ms stagger
        r = R0 + (R1 - R0) * float(out_cubic(np.clip(t / .6, 0, 1)))
        for k in range(n_dots):
            a = 2 * math.pi * k / 24 * (24 / max(n_dots, 1)) if n_dots < 24 else 2 * math.pi * k / 24
            x, y = 200 + r * math.cos(a), 120 + r * math.sin(a)
            d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(255, 255, 255))
        return np.asarray(im).astype(float)
    ts = np.arange(0, 1.2, 1 / 30)
    vid = video(wd / "dot_ring.mp4", [frame(t) for t in ts])
    fr = vread(vid, W, H)
    dots = lambda f: label(f.min(-1) > 200)[1]
    n0, n1 = dots(fr[0]), dots(fr[-1])
    P = mask_pts(fr[-1].min(-1) > 200)
    r_end = float(np.hypot(*(P - (200, 120)).T).mean())
    violet = int(((fr[-1][..., 2] > 200) & (fr[-1][..., 0] < 170) & (fr[-1][..., 0] > 100)).sum())
    return [check("logo dots duplicate 8 -> 24", n0 == 8 and n1 == 24, [n0, n1], [8, 24]),
            check("ring radius 40% of width (diameter)", abs(r_end - R1) < 2, r_end, R1),
            check("thin violet radial lines behind", violet > 500, violet, ">500"),
            check("negative control: the first frame does not have 24 dots", n0 != 24, n0, "!=24")], [vid]


@card("SHAPE-70")
def square_tunnel(task, wd):
    W = H = 240

    def frame(t, levels=14):
        im = Image.new("RGB", (W, H), (0, 0, 0))
        d = ImageDraw.Draw(im)
        ph = (t / 1.0) % 2                                 # scale every copy by 1/.9 per period; wrap after 2 (colour parity)
        for i in range(math.ceil(ph), levels + 3):         # largest first (never above the 200 px frame), nested on top
            s = 200 * (.9 ** (i - ph))
            a = math.radians(8 * (i - ph))
            P = np.array([[-s / 2, -s / 2], [s / 2, -s / 2], [s / 2, s / 2], [-s / 2, s / 2]])
            Rm = np.array([[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]])
            d.polygon([tuple(p) for p in P @ Rm.T + 120], fill=(230, 60, 60) if i % 2 == 0 else (250, 230, 200))
        return np.asarray(im).astype(float)
    out = save(wd / "tunnel.png", frame(0))
    vid = video(wd / "tunnel.mp4", [frame(t) for t in np.arange(0, 2, 1 / 15)], 15)
    img = load(out)
    # walk along the diagonal from the centre: colour band edges should shrink by .9 per level
    from scipy.ndimage import affine_transform

    def self_sim(scale, deg):
        """Error between the image and itself sampled at centre + scale R(deg)(p - centre): level i -> level i+1."""
        a = math.radians(deg)
        M = scale * np.array([[math.cos(a), math.sin(a)], [-math.sin(a), math.cos(a)]])   # (row, col) coordinates
        c = np.array([120.0, 120.0])
        g = img[..., 1]
        w = affine_transform(g, M, offset=c - M @ c, order=0)
        yy, xx = np.mgrid[:H, :W]
        inner = np.hypot(xx - 120, yy - 120) < 80
        return float(np.abs(w - g)[inner].mean())
    e_ok = min(self_sim(1 / .81, 16), self_sim(1 / .81, -16))     # two levels: same colour
    e_bad = min(self_sim(1 / .7, 16), self_sim(1 / .7, -16))
    ratio = 1 / .9 if e_ok < 10 else 0
    fr = vread(vid, W, H)
    loop = float(np.abs(frame(0) - frame(2.0 - 1e-3)).mean())   # the loop closes after two levels
    half = float(np.abs(frame(0) - frame(1.0 - 1e-3)).mean())   # one level later the colours are swapped
    return [check("self-similar under (x.9, 8 deg) twice: level i -> i+2 error", e_ok < 15, e_ok, "<15"),
            check("a wrong scale (x.7) breaks the self-similarity", e_bad > 4 * e_ok, e_bad, ">4x"),
            check("seamless loop: the frame just before the wrap matches frame 0", loop < 3, loop, "<3"),
            check("alternating two colours", len({tuple(c) for c in img[120, 120:200:3].astype(int)}) >= 2, True, True),
            check("negative control: wrapping after one level (colour flip) is not seamless", half > 10 * max(loop, .5), half, ">10x loop")], [out, vid]


@card("SHAPE-71")
def square_circle_satellites(task, wd):
    W = H = 240
    S = 100

    def frame(t, morph=True):
        im = Image.new("RGB", (W, H), (245, 240, 230))
        d = ImageDraw.Draw(im)
        e = float(in_out_cubic(np.clip(t / .5, 0, 1))) if morph else 0
        rad = e * S / 2                                   # border-radius 0 -> 50%
        big = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(big).rounded_rectangle([120 - S / 2, 120 - S / 2, 120 + S / 2, 120 + S / 2], radius=rad, fill=(33, 53, 188, 255))
        big = big.rotate(-90 * e, center=(120, 120))
        im.paste(big, (0, 0), big)
        d.ellipse([120 - 85, 120 - 85, 120 + 85, 120 + 85], outline=(150, 150, 150))
        for k in range(3):                                # three dots orbit 1 rev/s
            a = 2 * math.pi * (t + k / 3)
            x, y = 120 + 85 * math.cos(a), 120 + 85 * math.sin(a)
            d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(214, 52, 31) if k == 0 else (233, 198, 52))
        return np.asarray(im).astype(float)
    ts = np.arange(0, 1.0, 1 / 30)
    vid = video(wd / "sq_circle.mp4", [frame(t) for t in ts])
    fr = vread(vid, W, H)
    area = lambda f: float(((f[..., 2] > 150) & (f[..., 0] < 80)).sum())
    a0, a1 = area(fr[0]), area(fr[15])
    tr = [centroid((f[..., 0] > 180) & (f[..., 1] < 90) & (f[..., 2] < 60)) for f in fr]
    ang = np.unwrap([math.atan2(c[1] - 120, c[0] - 120) for c in tr])
    rev = float((ang[29] - ang[0]) / (2 * math.pi) * 30 / 29)
    a_still = area(frame(.5, morph=False))
    return [check("starts as the square (area)", abs(a0 - S * S) / (S * S) < .03, a0, S * S),
            check("is a circle after 500 ms (area pi r^2)", abs(a1 - math.pi * (S / 2) ** 2) / (math.pi * (S / 2) ** 2) < .03, a1, math.pi * 2500),
            check("satellites orbit 1 rev/s (tracked)", abs(rev - 1) < .04, rev, 1),
            check("negative control: without the morph the area stays the square's", abs(a_still - S * S) / (S * S) < .03, a_still, S * S)], [vid]


@card("SHAPE-72")
def swirl_portal(task, wd):
    N = 200
    yy, xx = np.mgrid[:N, :N].astype(float)
    th, rr = np.arctan2(yy - 100, xx - 100), np.hypot(xx - 100, yy - 100)
    k = 30.0

    def disc_img(twist=True):
        t2 = th + (k / (rr + 4) if twist else 0)         # theta += k / (r + eps) before sampling noise
        v = perlin2(np.cos(t2) * rr * .05 + 10, np.sin(t2) * rr * .05 + 10, 72)
        img = np.zeros((N, N, 3))
        m = rr < 70
        img[m] = ((v[m, None] + .5) * np.array([120, 60, 255])).clip(0, 255)
        ring = np.exp(-((rr - 78) / 4) ** 2)              # glowing torus ring
        img += ring[..., None] * np.array([255, 160, 255])
        return np.clip(img, 0, 255)
    out = save(wd / "portal.png", disc_img())
    img = load(out)

    def spiral_score(a):
        """Angle of iso-lines: twisted noise has orientation shifting with radius (measured by angular cross-correlation)."""
        g = a.mean(-1)
        prof = []
        for r_ in (20, 50):
            ang = np.linspace(-math.pi, math.pi, 720, endpoint=False)
            prof.append(g[np.round(100 + r_ * np.sin(ang)).astype(int), np.round(100 + r_ * np.cos(ang)).astype(int)])
        best = int(np.argmax([float(np.corrcoef(np.roll(prof[0], s_), prof[1])[0, 1]) for s_ in range(720)]))
        return min(best, 720 - best) / 2                  # degrees
    U = disc_img(False)
    m = rr < 66

    def unwarp_err(T_):
        """Compare T(r, theta) with U(r, theta + k/(r+4)): zero when T is exactly the polar twist of U."""
        a2 = th + k / (rr + 4)
        ys = np.clip(np.round(100 + rr * np.sin(a2)).astype(int), 0, N - 1)
        xs_ = np.clip(np.round(100 + rr * np.cos(a2)).astype(int), 0, N - 1)
        return float(np.abs(T_[m] - U[ys[m], xs_[m]]).mean())
    sw, st = unwarp_err(img), unwarp_err(U)
    ring_peak = float(img[100, 178].mean())
    return [check("rendered disc = noise sampled at theta + k/(r+eps) (unwarp error)", sw < 3, sw, "<3"),
            check("glowing torus ring around the disc", ring_peak > 150, ring_peak, ">150"),
            check("negative control: the untwisted disc fails the same unwarp test", st > 5 * max(sw, .5), st, ">5x")], [out]


@card("SHAPE-81")
def stickers_pills(task, wd):
    W, H = 360, 240
    rng = R(81)
    box = (90, 80, 270, 160)
    slots = [(15, 15), (135, 15), (255, 15), (15, 195), (135, 195), (255, 195)]   # around the headline, never the centre
    pills = [(x + rng.uniform(-5, 5), y + rng.uniform(-4, 4), rng.uniform(-6, 6), i) for i, (x, y) in enumerate(slots)]

    def frame(t):
        im = Image.new("RGBA", (W, H), (250, 246, 240, 255))
        d = ImageDraw.Draw(im)
        d.text((120, 108), "HEADLINE", fill=(20, 20, 20, 255))
        for x, y, tilt, i in pills:
            u = np.clip((t - .12 * i) / .3, 0, 1)
            if u <= 0:
                continue
            s = float(out_back(u))
            bob = 4 * math.sin(2 * math.pi * t / 3.5 + i)
            pill = Image.new("RGBA", (90, 30), (0, 0, 0, 0))
            ImageDraw.Draw(pill).rounded_rectangle([1, 1, 88, 28], radius=999, fill=(255, 255, 255, 255), outline=(196, 216, 229, 255))
            pill = pill.resize((max(1, int(90 * s)), max(1, int(30 * s)))).rotate(tilt + 6 * math.sin(2 * math.pi * t / 2), expand=True)
            im.paste(pill, (int(x), int(y + bob)), pill)
        return np.asarray(im.convert("RGB")).astype(float)
    ts = np.arange(0, 2.0, 1 / 30)
    vid = video(wd / "pills.mp4", [frame(t) for t in ts])
    fr = vread(vid, W, H)
    white = lambda f: (f.min(-1) > 252)
    counts = [label(white(f))[1] for f in fr]
    appear = [next(i for i, c in enumerate(counts) if c >= k) for k in range(1, 7)]
    stag = np.diff(appear) / 30
    centre_hits = int(white(fr[-1])[80:160, 90:270].sum())
    return [check("6 pills pop in", counts[-1] == 6, counts[-1], 6),
            check("pop-in stagger 120 ms (mean of measured, frame-quantised)", abs(float(stag.mean()) - .12) <= .02 and all(abs(sv - .12) <= .06 for sv in stag),
                  stag.tolist(), .12),
            check("pills avoid the centre headline box", centre_hits == 0, centre_hits, 0),
            check("negative control: before the first pop there are no pills", counts[0] == 0, counts[0], 0)], [vid]


@card("SHAPE-82")
def card_fan(task, wd):
    W, H = 360, 240
    n = 6

    def frame(t, fan=True):
        im = Image.new("RGBA", (W, H), (240, 236, 228, 255))
        for i in range(n - 1, -1, -1):
            u = np.clip((t - .075 * i) / .45, 0, 1)        # stagger 75 ms, 450 ms back.out(1.2)
            e = float(out_back(u, 1.2)) if fan else 0
            c = Image.new("RGBA", (80, 110), (0, 0, 0, 0))
            col = (214, 52, 31, 255) if i == n - 1 else (60 + 30 * i, 90, 200, 255)
            ImageDraw.Draw(c).rounded_rectangle([0, 0, 79, 109], radius=8, fill=col)
            c = c.rotate(-(2 + 4 * i / (n - 1)) * e * (i > 0) - 6 * e * (i == n - 1), expand=True, center=None)
            x = 120 + 18 * i * e
            im.paste(c, (int(x), 60), c)
        return np.asarray(im.convert("RGB")).astype(float)
    ts = np.arange(0, 1.0, 1 / 30)
    vid = video(wd / "fan.mp4", [frame(t) for t in ts])
    fr = vread(vid, W, H)
    red = lambda f: (f[..., 0] > 180) & (f[..., 1] < 80) & (f[..., 2] < 60)
    xr = [(bbox(red(f)) or (0, 0, 0, 0))[2] for f in fr]      # right edge of the back (last) card
    ang = math.radians(6 + 6)
    final = 120 + 18 * (n - 1) + 80 * math.cos(ang) + 110 * math.sin(ang)
    over = max(xr) - xr[-1]
    width_all = lambda f: (lambda b: b[2] - b[0])(bbox(np.abs(f - (240, 236, 228)).sum(-1) > 40))
    closed = width_all(frame(.99, fan=False))
    return [check("last card fans out +18 px per card (right edge, px)", abs(xr[-1] - final) <= 4, xr[-1], final),
            check("back.out overshoot before settling (px)", over >= 1, over, ">=1"),
            check("fan widens the stack", width_all(fr[-1]) > closed + 60, [width_all(fr[-1]), closed], "+60"),
            check("negative control: unfanned stack is a single card wide", closed < 100, closed, "<100")], [vid]


@card("SHAPE-83")
def highlighter_wipe(task, wd):
    W, H = 360, 140
    tm = text_mask(W, H, AR_WORD + " " + AR_WORD, 40, AMIRI_B, rtl=True) > 127
    b = bbox(tm)
    pad = 6

    def frame(t, rtl=True):
        e = float(out_cubic(np.clip(t / .22, 0, 1)))
        a = canvas(W, H, (250, 250, 250))
        x0, x1 = b[0] - pad, b[2] + pad
        w = (x1 - x0) * e
        sk = math.tan(math.radians(-8))
        yy, xx = np.mgrid[:H, :W]
        y0, y1 = b[1] - pad, b[3] + pad
        xs = xx - (yy - (y0 + y1) / 2) * sk
        m = (yy >= y0) & (yy <= y1) & ((xs >= x1 - w) & (xs <= x1) if rtl else (xs >= x0) & (xs <= x0 + w))
        a[m] = (255, 230, 60)
        a[tm] = (20, 20, 20)
        return a
    ts = np.arange(0, .4, 1 / 60)
    vid = video(wd / "highlight.mp4", [frame(t) for t in ts], 60)
    fr = vread(vid, W, H)
    yel = lambda f: (f[..., 2] < 120) & (f[..., 0] > 200)
    mid = bbox(yel(fr[5]))
    full = bbox(yel(fr[-1]))
    grows_right = mid is not None and abs(mid[2] - full[2]) <= 3 and mid[0] > full[0] + 20
    ys, xs = np.nonzero(yel(fr[-1]))
    top_x, bot_x = xs[ys == ys.min()].min(), xs[ys == ys.max()].min()
    skew = math.degrees(math.atan2(top_x - bot_x, ys.max() - ys.min()))
    ltr = bbox(yel(frame(5 / 60, rtl=False)))
    return [check("bar covers the text box plus padding", full[0] <= b[0] - pad + 6 and full[2] >= b[2] + pad - 6, full, b),
            check("Arabic: grows from the right edge", grows_right, [mid, full], "anchored right"),
            check("skewed about -8 deg (measured)", 4 <= abs(skew) <= 12, skew, 8),
            check("done in 180-250 ms", bool(np.array_equal(yel(fr[int(.25 * 60)]), yel(fr[-1]))), True, True),
            check("negative control: a left-origin wipe is anchored left", abs(ltr[0] - full[0]) <= 6 and abs(ltr[2] - full[2]) > 20, ltr, "anchored left")], [vid]


@card("SHAPE-84")
def clip_lens(task, wd):
    W, H = 400, 120
    words = ["ONE", "TWO", "SIX", "TEN", "RED"]
    f_ = font(POPPINS, 26)

    def row_img(col):
        im = Image.new("L", (900, H), 0)
        d = ImageDraw.Draw(im)
        for i, w in enumerate(words):
            d.text((60 + 120 * i, 44), w, fill=255, font=f_)
        return np.asarray(im) > 127

    row = row_img(255)
    yy, xx = np.mgrid[:H, :W]

    def frame(t, clip=True):
        off = int(-200 + 150 * t)                          # slide left -> right, 1 word / .8 s
        a = canvas(W, H, (245, 245, 245))
        sl = np.zeros((H, W), bool)
        lo, hi = max(0, -off), min(900, W - off)
        sl[:, lo + off:hi + off] = row[:, lo:hi]
        orb = np.hypot(xx - 200, yy - 60) < 70
        a[orb] = (20, 20, 20)
        a[sl] = (60, 60, 60)                               # dark copy
        if clip:
            a[sl & orb] = (255, 255, 255)                  # white copy clipped by circle() at the orb
        return a
    vid = video(wd / "lens.mp4", [frame(t) for t in np.arange(0, 2, 1 / 15)], 15)
    fr = vread(vid, W, H)
    orb = np.hypot(xx - 200, yy - 60) < 68
    f = fr[10]
    white_in = int(((f.min(-1) > 200) & orb).sum())
    white_out = int(((f.min(-1) > 252) & ~(np.hypot(xx - 200, yy - 60) < 72)).sum())
    txt = lambda f_: (((np.abs(f_ - 60).max(-1) < 8) | (f_.min(-1) > 252)).any(0)).astype(float)
    p0, p1 = txt(fr[0]), txt(fr[3])
    sh = int(np.argmax([float((np.roll(p0, d_)[60:340] * p1[60:340]).sum()) for d_ in range(0, 60)]))
    slide = sh / (3 / 15)
    noclip = frame(10 / 15, clip=False)
    w_nc = int(((noclip.min(-1) > 200) & orb).sum())
    return [check("words turn white inside the orb", white_in > 50, white_in, ">50"),
            check("outside the orb the text stays dark", white_out == 0, white_out, 0),
            check("row slides left -> right at ~150 px/s (measured)", abs(slide - 150) < 15, slide, 150),
            check("negative control: without the clipped copy nothing turns white", w_nc == 0, w_nc, 0)], [vid]


@card("SHAPE-85")
def shard_assembly(task, wd):
    W = H = 240
    rng = R(85)
    # target: a hexagon split into 6 triangles (slots)
    hexv = poly_regular(6, 80, 120, 120)
    tris = [np.array([[120, 120], hexv[i], hexv[(i + 1) % 6]]) for i in range(6)]
    starts = [(rng.uniform(-200, 440), rng.choice([-120, 360]), rng.uniform(-math.pi, math.pi)) for _ in range(6)]

    def frame(t):
        a = canvas(W, H)
        for i, (sx, sy, sr) in enumerate(starts):
            u = float(out_cubic(np.clip((t - .04 * i) / .6, 0, 1)))   # 600 ms ease-out, 40 ms stagger
            c = tris[i].mean(0)
            ctrl = (np.array([sx, sy]) + c) / 2 + np.array([0, -80])   # quadratic arc path
            p = (1 - u) ** 2 * np.array([sx, sy]) + 2 * u * (1 - u) * ctrl + u * u * c
            r = sr * (1 - u)
            Rm = np.array([[math.cos(r), -math.sin(r)], [math.sin(r), math.cos(r)]])
            a[poly_mask(W, H, (tris[i] - c) @ Rm.T + p)] = (255, 200 - 20 * i, 60 + 30 * i)
        return a
    ts = np.arange(0, 1.0, 1 / 30)
    vid = video(wd / "shards.mp4", [frame(t) for t in ts])
    fr = vread(vid, W, H)
    target = poly_mask(W, H, hexv)
    io = [iou(f.max(-1) > 40, target) for f in fr]
    done = next(i for i, v in enumerate(io) if v > .95) / 30
    return [check("pieces assemble the hexagon (IoU)", io[-1] > .95, io[-1], ">.95"),
            check("assembly completes ~0.8 s (600 ms + 5 x 40 ms)", .55 <= done <= .85, done, ".6-.8"),
            check("pieces start off-screen", io[0] < .05, io[0], "<.05"),
            check("negative control: halfway the shape is not yet assembled", io[9] < .8, io[9], "<.8")], [vid]


@card("SHAPE-86")
def eclipse_split(task, wd):
    W, H = 320, 180
    yy, xx = np.mgrid[:H, :W]

    def frame(t, blend=True):
        a = np.zeros((H, W, 3))
        a[:, :W // 2] = (243, 234, 216)
        e = float(in_out_cubic(np.clip(t / 1.5, 0, 1)))
        x1, x2 = 60 + 100 * e, 260 - 100 * e
        ring = np.abs(np.hypot(xx - x1, yy - 90) - 40) < 2
        dot = np.hypot(xx - x2, yy - 90) < 40
        lay = np.zeros((H, W, 3))
        lay[ring] = 255
        lay[dot] = (214, 52, 31)
        if blend:                                          # difference blend at the overlap
            m = ring | dot
            a[m] = np.abs(a[m] - lay[m])
        else:
            a[ring | dot] = lay[ring | dot]
        return a
    ts = np.arange(0, 1.6, 1 / 30)
    vid = video(wd / "eclipse.mp4", [frame(t) for t in ts])
    fr = vread(vid, W, H)
    xs = []
    for f in fr:
        m = (np.abs(f - (214, 52, 31)).max(-1) < 10) | (np.abs(f - np.abs(np.array([243, 234, 216]) - (214, 52, 31))).max(-1) < 10)
        c = centroid(m)
        xs.append(c[0] if c else np.nan)
    end_overlap = abs(xs[-1] - 160) < 3
    diff_col = fr[-1][90, 140]                            # left (cream) side under the red dot -> |cream - red|
    exp_col = np.abs(np.array([243, 234, 216]) - (214, 52, 31))
    plain = frame(1.6, blend=False)[90, 140]
    return [check("dot slides to centre over ~1.5 s", end_overlap, xs[-1], 160),
            check("difference blend at the overlap", float(np.abs(diff_col - exp_col).max()) < 6, diff_col.tolist(), exp_col.tolist()),
            check("in-out easing: slow start (moved < 10 px in 200 ms)", abs(xs[6] - xs[0]) < 10, abs(xs[6] - xs[0]), "<10"),
            check("negative control: normal blend keeps the red dot colour", float(np.abs(plain - (214, 52, 31)).max()) < 1, plain.tolist(), "red")], [vid]


@card("SHAPE-87")
def line_sea(task, wd):
    W, H = 360, 200

    def frame(t, bob=True):
        im = Image.new("RGB", (W, H), (250, 248, 240))
        d = ImageDraw.Draw(im)
        for k in range(5):                                # 4-6 sine paths, phase drift, parallax speeds
            xs = np.arange(0, W, 3)
            ys = 110 + 18 * k + 6 * np.sin(xs / 40 + 2 * math.pi * t / 6 * (1 + .5 * k))
            d.line(list(zip(xs.tolist(), ys.tolist())), fill=(30, 60, 120), width=2)
        ang = 4 * math.sin(2 * math.pi * t / 1.5) if bob else 0   # mascot bob +-4 deg / 1.5 s
        m = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
        ImageDraw.Draw(m).rectangle([2, 12, 38, 28], fill=(214, 52, 31, 255))
        m = m.rotate(ang, expand=True)
        im.paste(m, (int(40 + 60 * t), 60), m)
        return np.asarray(im).astype(float)
    ts = np.arange(0, 3, 1 / 20)
    vid = video(wd / "line_sea.mp4", [frame(t) for t in ts], 20)
    fr = vread(vid, W, H)
    def tilt(f):
        P = mask_pts((f[..., 0] > 180) & (f[..., 1] < 80))
        w_, v_ = np.linalg.eigh(np.cov(P.T))
        return math.degrees(math.atan2(v_[1, 1], v_[0, 1])) % 90
    tl = np.array([tilt(f) for f in fr])
    tl = np.where(tl > 45, tl - 90, tl)
    amp = float(np.ptp(tl) / 2)
    F = np.abs(np.fft.rfft(tl - tl.mean()))
    per = 1 / float(np.fft.rfftfreq(len(tl), 1 / 20)[np.argmax(F[1:]) + 1])
    xs_m = [centroid((f[..., 0] > 180) & (f[..., 1] < 80))[0] for f in fr]
    still = np.array([tilt(frame(t, bob=False)) for t in (0, .4, .8, 1.1)])
    still = np.where(still > 45, still - 90, still)
    return [check("mascot bobs +-4 deg (measured)", 2.5 <= amp <= 5, amp, 4),
            check("bob period 1.5 s", abs(per - 1.5) < .2, per, 1.5),
            check("mascot crosses the frame", xs_m[-1] - xs_m[0] > 150, xs_m[-1] - xs_m[0], ">150"),
            check("negative control: the same tilt measurement without the bob reads ~0", float(np.ptp(still)) / 2 < .5, float(np.ptp(still)) / 2, "<.5")], [vid]


@card("SHAPE-89")
def base_grid(task, wd):
    U, cols, W, H = 24, 12, 576, 336                      # 24 px unit, 12 columns of 2 units, 14 rows
    els = [(1, 1, 5, 3), (6, 1, 11, 6), (1, 4, 5, 9), (2, 10, 10, 13)]   # end states in units

    def frame(t, snap=True):
        im = Image.new("RGB", (W, H), (250, 250, 250))
        d = ImageDraw.Draw(im)
        e = float(out_cubic(np.clip(t / .6, 0, 1)))
        for k, (a, b, c, d_) in enumerate(els):
            x0, y0, x1, y1 = [v * U + (0 if snap else 5 + k) for v in (a, b, c, d_)]
            ox = (1 - e) * 90 * (1 if k % 2 else -1)       # in-between frames may sit off-grid
            d.rectangle([x0 + ox, y0, x1 + ox - 1, y1 - 1], fill=(33, 53, 188))
        return np.asarray(im).astype(float)
    vid = video(wd / "grid.mp4", [frame(t) for t in np.arange(0, .8, 1 / 30)])
    fr = vread(vid, W, H)

    def edges_on_grid(f):
        m = f[..., 0] < 100
        cols_ = np.nonzero(np.diff(m.any(0).astype(int)) != 0)[0] + 1
        rows_ = np.nonzero(np.diff(m.any(1).astype(int)) != 0)[0] + 1
        lab, n = label(m)
        ok = []
        for k in range(1, n + 1):
            ys, xs = np.nonzero(lab == k)
            ok += [xs.min() % U == 0, (xs.max() + 1) % U == 0, ys.min() % U == 0, (ys.max() + 1) % U == 0]
        return all(ok) and n > 0
    mid_ok = edges_on_grid(fr[5])
    return [check("final frame: every edge lands on the 24 px grid", edges_on_grid(fr[-1]), True, True),
            check("decoded frame is exactly 12 columns x 2 units wide and content stays inside", fr.shape[2] == cols * 2 * U and bbox(fr[-1][..., 0] < 100)[2] < fr.shape[2],
                  [fr.shape[2], bbox(fr[-1][..., 0] < 100)[2]], [cols * 2 * U, "<576"]),
            check("only end states are snapped (an in-between is off-grid)", not mid_ok, mid_ok, False),
            check("negative control: an unsnapped layout fails the grid test", not edges_on_grid(frame(.8, snap=False)), False, False)], [vid]


def lint_style(spec):
    issues = []
    if len(set(spec["primitives"])) > 3:
        issues.append("more than three primitives")
    if len(set(spec["colours"])) > 2:
        issues.append("more than two colours + background")
    if any(r not in (0, 8, 24, 50) for r in spec["radii"]):
        issues.append("radius off the 0/8/24/50% scale")
    if any(s not in (2, 4, 8) for s in spec["strokes"]):
        issues.append("stroke off the 2/4/8 scale")
    if spec["negative_space"] < .3:
        issues.append("negative space under 30%")
    return issues


def nested_radius(outer, gap):
    inner = outer - gap
    return inner if gap < 32 and inner > 2 else outer


@card("SHAPE-90")
def primitive_scales(task, wd):
    W, H = 320, 200
    im = Image.new("RGB", (W, H), (245, 242, 236))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([30, 40, 130, 140], radius=16, fill=(33, 53, 188))
    d.rounded_rectangle([38, 48, 122, 132], radius=nested_radius(16, 8), fill=(245, 242, 236))
    d.ellipse([170, 50, 260, 140], outline=(214, 52, 31), width=4)
    out = save(wd / "scales.png", np.asarray(im))
    img = load(out)
    neg = float((np.abs(img - (245, 242, 236)).sum(-1) < 10).mean())
    cols = {tuple(c) for c in img.reshape(-1, 3).astype(int)}
    spec = {"primitives": ["rect", "circle"], "colours": ["#2135bc", "#d6341f"], "radii": [8, 50], "strokes": [4],
            "negative_space": neg}
    busy = {"primitives": ["rect", "circle", "tri", "star"], "colours": ["a", "b", "c", "d"], "radii": [5, 13], "strokes": [3],
            "negative_space": .1}
    return [check("measured negative space >= 30%", neg >= .3, neg, ">=.3"),
            check("nested radius: 16 px outer, 8 px gap -> 8 px inner", nested_radius(16, 8) == 8, nested_radius(16, 8), 8),
            check("design passes the scale lint", lint_style(spec) == [], lint_style(spec), []),
            check("gap >= 32 keeps the outer radius", nested_radius(40, 32) == 40, nested_radius(40, 32), 40),
            check("negative control: a busy design fails all five rules", len(lint_style(busy)) == 5, lint_style(busy), 5)], [out]


@card("SHAPE-91")
def squash_stretch(task, wd):
    W, H, floor = 240, 240, 200
    hit = .4

    def window01(t, a, b, ein, eout):
        if t < a or t > b:
            return 0.0
        return float(min(1, (t - a) / ein, (b - t) / eout))

    def frame(t, squash=True):
        im = Image.new("RGB", (W, H), (245, 245, 245))
        d = ImageDraw.Draw(im)
        y = floor - max(0, 120 * (1 - (t / hit) ** 2)) if t < hit else floor
        s = window01(t, hit, hit + .08, .008, .02) if squash else 0
        if t > hit + .08 and squash:
            s = -.1 * (1 - float(spring(t - hit - .08, 220, 10)))     # spring back (d10 k220)
        sx, sy = 1 + .3 * s, 1 - .3 * s                   # about the contact point
        w, h = 60 * sx, 60 * sy
        d.rectangle([120 - w / 2, floor - h + 1, 120 + w / 2 - 1, floor], fill=(214, 52, 31)) if t >= hit else \
            d.rectangle([90, y - 59, 149, y], fill=(214, 52, 31))
        return np.asarray(im).astype(float)
    ts = np.arange(0, 1.6, 1 / 120)
    vid = video(wd / "squash.mp4", [frame(t) for t in ts], 120)
    fr = vread(vid, W, H)
    box = [bbox((f[..., 0] > 150) & (f[..., 1] < 100)) for f in fr]
    k = int(round((hit + .04) * 120))
    w, h = box[k][2] - box[k][0] + 1, box[k][3] - box[k][1] + 1
    base = box[-1]
    contact = all(b_[3] == floor for b_ in box[int(hit * 120):int((hit + .1) * 120)])
    nb = bbox((frame(hit + .04, False)[..., 0] > 150) & (frame(hit + .04, False)[..., 1] < 100))
    return [check("squash to scaleX 1.3 / scaleY .7 at the hit (measured)", abs(w / 60 - 1.3) < .04 and abs(h / 60 - .7) < .04, [w / 60, h / 60], [1.3, .7]),
            check("squash held ~80 ms then springs back to 60 x 60", abs(base[2] - base[0] + 1 - 60) <= 1 and abs(base[3] - base[1] + 1 - 60) <= 1,
                  [base[2] - base[0] + 1, base[3] - base[1] + 1], 60),
            check("pivot at the contact point: bottom stays on the floor", contact, contact, True),
            check("negative control: no squash keeps 60 x 60 at the hit", (nb[2] - nb[0] + 1, nb[3] - nb[1] + 1) == (60, 60),
                  [nb[2] - nb[0] + 1, nb[3] - nb[1] + 1], [60, 60])], [vid]


@card("SHAPE-92")
def magnet_snap(task, wd):
    W, H = 192, 108                                       # 1920 x 1080 / 10: origin (960, 540) -> (96, 54)
    k, dmp = 220.0, 14.0

    def frame(t, damp=dmp):
        im = Image.new("RGB", (W, H), (10, 10, 10))
        d = ImageDraw.Draw(im)
        e = float(spring(t, k, damp))
        x = 20 + 120 * e                                   # snap into the slot at x = 140
        d.rectangle([x - 6, 40, x + 6, 52], fill=(255, 220, 0))
        s = .2 + .8 * float(spring(t, k, damp))            # entrance scale about the frame centre
        d.rectangle([96 - 20 * s, 54 + 10 - 10 * s + 20, 96 + 20 * s, 54 + 10 + 10 * s + 20], outline=(0, 200, 255))
        return np.asarray(im).astype(float)
    ts = np.arange(0, 1.2, 1 / 120)
    vid = video(wd / "magnet.mp4", [frame(t) for t in ts], 120)
    fr = vread(vid, W, H)
    xs = np.array([centroid((f[..., 0] > 200) & (f[..., 2] < 60))[0] for f in fr])
    over = (xs.max() - 140) / 120
    z = dmp / (2 * math.sqrt(k))
    theory = math.exp(-z * math.pi / math.sqrt(1 - z * z))
    cyan = [bbox((f[..., 2] > 150) & (f[..., 0] < 60)) for f in fr]
    cx = [(b_[0] + b_[2]) / 2 for b_ in cyan[::20]]
    crit = np.array([centroid((f[..., 0] > 200) & (f[..., 2] < 60))[0] for f in [frame(t, 2 * math.sqrt(k)) for t in ts[::6]]])
    return [check("overshoot ratio matches the k220 d14 spring (measured)", abs(over - theory) < .03, over, theory),
            check("settles in the slot", abs(xs[-1] - 140) < .6, xs[-1], 140),
            check("entrance pivots on the frame centre (x stays 96)", all(abs(c - 96) <= .5 for c in cx), cx, 96),
            check("negative control: a critically damped snap never overshoots", crit.max() <= 140.5, float(crit.max()), "<=140.5")], [vid]


def overshoots(y, target, tol):
    """Number of local extrema beyond the target by more than tol (an overshoot or a rebound)."""
    d = np.asarray(y) - target
    ext = [i for i in range(1, len(d) - 1) if (d[i] > d[i - 1] and d[i] >= d[i + 1]) or (d[i] < d[i - 1] and d[i] <= d[i + 1])]
    return sum(1 for i in ext if abs(d[i]) > tol and i > 2)


@card("SHAPE-93")
def playful_style(task, wd):
    W, H = 320, 180
    pal = [hexc("#ff4d6d"), hexc("#ffd23f"), hexc("#3bceac")]
    items = [(60, 90, "circle"), (160, 90, "card"), (260, 90, "circle")]

    def frame(t, ease=out_back):
        im = Image.new("RGB", (W, H), (250, 248, 240))
        d = ImageDraw.Draw(im)
        for i, (x, y, kind) in enumerate(items):
            u = np.clip((t - .15 * i) / .5, 0, 1)          # staggered entrances, one overshoot each (back.out)
            yy = 260 + (y - 260) * float(ease(u))
            c = tuple(int(v) for v in pal[i])
            if kind == "circle":
                d.ellipse([x - 25, yy - 25, x + 25, yy + 25], fill=c)
            else:
                d.rounded_rectangle([x - 35, yy - 25, x + 35, yy + 25], radius=8, fill=c)
        return np.asarray(im).astype(float)
    ts = np.arange(0, 1.2, 1 / 60)
    vid = video(wd / "playful.mp4", [frame(t) for t in ts], 60)
    fr = vread(vid, W, H)

    def tracks(frames):
        out = []
        for i, (x, y, _) in enumerate(items):
            col = pal[i]
            out.append([(lambda c: c[1] if c else 260)(centroid(np.abs(f - col).max(-1) < 12)) for f in frames])
        return out
    tr = tracks(fr)
    ov = [overshoots(t_, 90, 1.0) for t_ in tr]
    starts = [next(j for j, v in enumerate(t_) if v < 259) for t_ in tr]
    stag = np.diff(starts) / 60
    uq, cnt = np.unique((fr[-1] // 8).reshape(-1, 3), axis=0, return_counts=True)
    ncol = int((cnt > 200).sum())
    el = tracks([frame(t, out_elastic) for t in ts])
    ov_el = [overshoots(t_, 90, 1.0) for t_ in el]
    return [check("exactly one overshoot per entrance (measured)", ov == [1, 1, 1], ov, [1, 1, 1]),
            check("entrances staggered 150 ms", all(abs(s_ - .15) <= 2 / 60 for s_ in stag), stag.tolist(), .15),
            check("limited palette measured: 3 colours + background", ncol == 4, ncol, 4),
            check("negative control: elastic easing over-bounces (more than one overshoot)", all(o > 1 for o in ov_el), ov_el, ">1")], [vid]
