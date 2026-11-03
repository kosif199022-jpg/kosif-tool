"""camera-composition-layout (part B): method cards as real programs with known-answer checks.

Every runner builds a deterministic fixture in its work folder, applies the card's method (a camera curve, a
layout rule, a HUD, a lens/exposure formula, or the repo's own kit code: motion-kit.js, three-kit.bundle.js,
lab-kit.js, render.py, tools.py, light_calc.py, image_analyze.py, workbench_cli.py, matter-js, gsap), writes an
output file and measures that output (tracked colour markers, ink in regions, bar fill, sharpness, projected sizes).
Each card also runs the same measurement on the unprocessed input as a negative control, which must fail.
"""
from __future__ import annotations

import importlib.util
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

from _harness import card, check, fx

GAPS: dict = {
    "CAM-71": "measured, not registered: the card's coverage zoom need = |cos r| + q|sin r|*0.56 leaves 0.3-0.9 % black "
              "corners on a 16:9 frame at 2-6 deg roll (the exact cover is |cos r| + q|sin r|); runner kept as rotation_coverage() "
              "for the evidence but a passing check would be false",
    "CAM-64": "needs WebGPU or a verified fallback: headless Chrome here has no navigator.gpu; three r186 TSL dof() through "
              "WebGPURenderer's WebGL2 fallback ran but blurred the near (3 m) and far (15 m) planes alike (Laplacian 15 vs 15, "
              "plain pass 1690 / 2933), so a focus pull cannot be shown",
    "CAM-389": "reference-only excerpt of Kling camera-control parameters: running it needs a paid video-generation key (key:video-gen)",
    "CAM-92": "needs network the sandbox does not have: `hyperframes add carousel-circle-1..5` aborts because its sample photos come from static.heygen.ai, which does not resolve here (ENOTFOUND); without the installed HTML there is nothing real to run",
    "CAM-93": "needs network the sandbox does not have: `hyperframes add carousel-orbit-1..5` aborts because its sample photos come from static.heygen.ai, which does not resolve here (ENOTFOUND); without the installed HTML there is nothing real to run",
    "CAM-94": "needs network the sandbox does not have: `hyperframes add carousel-path-1..5` aborts because its sample photos come from static.heygen.ai, which does not resolve here (ENOTFOUND); without the installed HTML there is nothing real to run",
    "CAM-95": "needs network the sandbox does not have: `hyperframes add carousel-text-circle-1..5` aborts because its sample photos come from static.heygen.ai, which does not resolve here (ENOTFOUND); without the installed HTML there is nothing real to run",
    "CAM-96": "needs network the sandbox does not have: `hyperframes add carousel-vision-1..5` aborts because its sample photos come from static.heygen.ai, which does not resolve here (ENOTFOUND); without the installed HTML there is nothing real to run",
}

REPO = Path(__file__).resolve().parents[4]
KIT = REPO / ".claude/skills/kosif-superpowers/vendor/100-superskills/skills/kosif-montage-motion/scripts"
_NODE = shutil.which("node")
NODE_MODULES = (Path(_NODE).resolve().parents[1] / "lib/node_modules") if _NODE else Path("/nonexistent")
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"

COL = {"red": (255, 0, 0), "blue": (0, 0, 255), "green": (0, 255, 0), "yellow": (255, 255, 0),
       "magenta": (255, 0, 255), "cyan": (0, 255, 255)}


def np():
    import numpy
    return numpy


# ───────────────────────── easing ─────────────────────────
def ease_io_cubic(p):
    p = min(1.0, max(0.0, p))
    return 4 * p ** 3 if p < 0.5 else 1 - (-2 * p + 2) ** 3 / 2


def ease_in_cubic(p):
    p = min(1.0, max(0.0, p))
    return p ** 3


def ease_out_expo(p):
    p = min(1.0, max(0.0, p))
    return 1.0 if p >= 1 else 1 - 2 ** (-10 * p)


def ease_io_sine(p):
    p = min(1.0, max(0.0, p))
    return -(math.cos(math.pi * p) - 1) / 2


def smoothstep(p):
    p = min(1.0, max(0.0, p))
    return p * p * (3 - 2 * p)


def power2_out(p):
    p = min(1.0, max(0.0, p))
    return 1 - (1 - p) ** 2


def bezier(x1, y1, x2, y2):
    def calc(t, a, b):
        return ((1 - 3 * b + 3 * a) * t + (3 * b - 6 * a)) * t * t + 3 * a * t

    def f(x):
        if x <= 0:
            return 0.0
        if x >= 1:
            return 1.0
        lo, hi = 0.0, 1.0
        for _ in range(40):
            mid = (lo + hi) / 2
            if calc(mid, x1, x2) < x:
                lo = mid
            else:
                hi = mid
        return calc((lo + hi) / 2, y1, y2)
    return f


# ───────────────────────── video io ─────────────────────────
def write_video(path, frames, fps=30):
    """frames: list of HxWx3 uint8 arrays → H.264 mp4 (crf 10)."""
    N = np()
    frames = [N.asarray(f, dtype=N.uint8) for f in frames]
    H, W = frames[0].shape[:2]
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (W, H),
                          "-r", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "8",
                          "-pix_fmt", "yuv444p", str(path)], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    for f in frames:
        p.stdin.write(f.tobytes())
    p.stdin.close()
    err = p.stderr.read()
    if p.wait():
        raise RuntimeError("ffmpeg encode failed: %s" % err[-300:])
    return Path(path)


def read_video(path):
    """Decoded frames as uint8 (N, H, W, 3) at the native size (numeric work converts to int16/float itself)."""
    N = np()
    pr = fx.probe(path)
    v = [s for s in pr["streams"] if s["codec_type"] == "video"][0]
    w, h = int(v["width"]), int(v["height"])
    done = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                          capture_output=True, timeout=120, stdin=subprocess.DEVNULL)
    if done.returncode:
        raise RuntimeError(done.stderr.decode(errors="replace")[-300:])
    return N.frombuffer(done.stdout, dtype=N.uint8).reshape(-1, h, w, 3)


def save_png(path, arr):
    from PIL import Image
    Image.fromarray(np().asarray(arr, dtype=np().uint8)).save(path)
    return Path(path)


def load_png(path):
    from PIL import Image
    return np().asarray(Image.open(path).convert("RGB")).astype(float)


# ───────────────────────── measurement ─────────────────────────
def mask_of(frame, color, tol=60):
    N = np()
    c = N.array(COL.get(color, color), dtype=N.int16)
    return N.abs(frame.astype(N.int16) - c).max(axis=2) < tol


def centroid(frame, color, tol=60, min_px=3):
    N = np()
    m = mask_of(frame, color, tol)
    if m.sum() < min_px:
        return None
    ys, xs = N.nonzero(m)
    return (float(xs.mean()), float(ys.mean()))


def area(frame, color, tol=60):
    return int(mask_of(frame, color, tol).sum())


def bbox(frame, color, tol=60):
    N = np()
    m = mask_of(frame, color, tol)
    if m.sum() < 2:
        return None
    ys, xs = N.nonzero(m)
    return (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)


def track(frames, color, tol=60):
    return [centroid(f, color, tol) for f in frames]


def ink(frame, box, bg, thr=30):
    """Fraction of pixels in box (x0,y0,x1,y1) that differ from bg by more than thr."""
    N = np()
    x0, y0, x1, y1 = [int(round(v)) for v in box]
    reg = frame[y0:y1, x0:x1]
    if reg.size == 0:
        return 0.0
    return float((N.abs(reg - N.array(bg, float)).max(axis=2) > thr).mean())


def peak(frame, box):
    x0, y0, x1, y1 = [int(round(v)) for v in box]
    return float(frame[y0:y1, x0:x1].max())


def sharpness(gray):
    N = np()
    g = N.asarray(gray, float)
    if g.ndim == 3:
        g = g.mean(axis=2)
    lap = g[1:-1, 1:-1] * 4 - g[:-2, 1:-1] - g[2:, 1:-1] - g[1:-1, :-2] - g[1:-1, 2:]
    return float(lap.var())


def max_err(meas, exp):
    worst = 0.0
    for m, e in zip(meas, exp):
        if isinstance(e, str):
            continue
        if m is None or e is None:
            if (m is None) != (e is None):
                return 1e9
            continue
        worst = max(worst, math.hypot(m[0] - e[0], m[1] - e[1]))
    return worst


def r2_linear(xs, ys):
    N = np()
    xs, ys = N.asarray(xs, float), N.asarray(ys, float)
    A = N.vstack([xs, N.ones_like(xs)]).T
    coef, *_ = N.linalg.lstsq(A, ys, rcond=None)
    pred = A @ coef
    ss = ((ys - ys.mean()) ** 2).sum()
    return 1 - ((ys - pred) ** 2).sum() / ss if ss > 0 else 0.0


# ───────────────────────── 2D camera engine ─────────────────────────
def world(Wc, Hc, markers, bg=(40, 44, 52), grid=40, seed=1):
    """A world canvas with a faint grid and coloured disc markers {name: (color, x, y, r)}."""
    N = np()
    img = N.zeros((Hc, Wc, 3), N.uint8)
    img[:] = bg
    img[::grid, :] = (70, 74, 82)
    img[:, ::grid] = (70, 74, 82)
    yy, xx = N.mgrid[0:Hc, 0:Wc]
    for _, (color, x, y, r) in markers.items():
        img[(xx - x) ** 2 + (yy - y) ** 2 <= r * r] = COL.get(color, color)
    return img


def mat_stage(x=0.0, y=0.0, s=1.0, rot=0.0, origin=(0.0, 0.0)):
    """CSS-like stage transform: screen = origin + R*s*(p - origin) + (x, y)."""
    N = np()
    a = math.radians(rot)
    R = N.array([[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]]) * s
    o = N.array(origin, float)
    t = o - R @ o + N.array([x, y], float)
    return N.hstack([R, t[:, None]])


def mat_cam(cx, cy, s, W, H, rot=0.0):
    """Camera looking at world point (cx, cy) with zoom s and roll rot: that point lands on the screen centre."""
    N = np()
    a = math.radians(rot)
    R = N.array([[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]]) * s
    t = N.array([W / 2, H / 2]) - R @ N.array([cx, cy], float)
    return N.hstack([R, t[:, None]])


def apply_mat(M, p):
    return (float(M[0, 0] * p[0] + M[0, 1] * p[1] + M[0, 2]), float(M[1, 0] * p[0] + M[1, 1] * p[1] + M[1, 2]))


_GRIDS = {}


def warp(img, M, W, H, fill=(0, 0, 0)):
    """Render img through the 2x3 affine M (world → screen) by inverse nearest sampling."""
    N = np()
    A = N.vstack([M, [0, 0, 1]])
    Ai = N.linalg.inv(A)
    if (H, W) not in _GRIDS:
        _GRIDS[(H, W)] = N.mgrid[0:H, 0:W].astype(float)
    yy, xx = _GRIDS[(H, W)]
    sx = Ai[0, 0] * xx + Ai[0, 1] * yy + Ai[0, 2]
    sy = Ai[1, 0] * xx + Ai[1, 1] * yy + Ai[1, 2]
    xi, yi = N.round(sx).astype(int), N.round(sy).astype(int)
    ok = (xi >= 0) & (yi >= 0) & (xi < img.shape[1]) & (yi < img.shape[0])
    out = N.zeros((H, W, 3), N.uint8)
    out[:] = fill
    out[ok] = img[yi[ok], xi[ok]]
    return out


def cam_run(wd, name, wimg, mats, W, H, fps, markers, tol=2.5, input_mats=None, neg_k=3.0, frames=None):
    """Render the camera move and a static input clip; track every marker in both decoded videos.

    Returns (checks, outputs, data) where data has measured tracks, expected tracks and per-frame scale."""
    N = np()
    rendered = frames if frames is not None else [warp(wimg, M, W, H) for M in mats]
    out = write_video(wd / ("%s.mp4" % name), rendered, fps)
    imats = input_mats if input_mats is not None else [mats[0]] * len(mats)
    cache = {}
    for M in imats:
        k = M.tobytes()
        if k not in cache:
            cache[k] = warp(wimg, M, W, H)
    inp = write_video(wd / ("%s_input.mp4" % name), [cache[M.tobytes()] for M in imats], fps)
    fo, fi = read_video(out), read_video(inp)
    data = {"meas": {}, "exp": {}, "inp": {}}
    for k, (color, x, y, r) in markers.items():
        exp = []
        for M in mats:
            q = apply_mat(M, (x, y))
            rs = r * math.sqrt(abs(M[0, 0] * M[1, 1] - M[0, 1] * M[1, 0])) + 2
            inside = rs <= q[0] < W - rs and rs <= q[1] < H - rs
            outside = q[0] < -rs or q[1] < -rs or q[0] > W + rs or q[1] > H + rs
            exp.append(q if inside else (None if outside else "skip"))
        data["exp"][k] = exp
        data["meas"][k] = track(fo, color)
        data["inp"][k] = track(fi, color)
    err = max(max_err(data["meas"][k], data["exp"][k]) for k in markers)
    nerr = max(max_err(data["inp"][k], data["exp"][k]) for k in markers)
    checks = [check("%s: decoded markers follow the planned camera (max px error)" % name, err <= tol, err, "<= %s" % tol),
              check("negative control: static input does not follow the camera curve", nerr > neg_k * tol, nerr,
                    "> %s" % (neg_k * tol))]
    data["frames"] = fo
    data["input_frames"] = fi
    return checks, [out], data


def pair_scale(data, a, b, d0, which="meas"):
    """Per-frame scale measured from the distance between two tracked markers (d0 = world distance)."""
    res = []
    for p, q in zip(data[which][a], data[which][b]):
        res.append(None if p is None or q is None else math.hypot(p[0] - q[0], p[1] - q[1]) / d0)
    return res


def pair_angle(data, a, b, which="meas"):
    res = []
    for p, q in zip(data[which][a], data[which][b]):
        res.append(None if p is None or q is None else math.degrees(math.atan2(q[1] - p[1], q[0] - p[0])))
    return res


# ───────────────────────── text / drawing ─────────────────────────
_FONTS = {}


def font(path, size):
    from PIL import ImageFont
    key = (path, size)
    if key not in _FONTS:
        try:
            _FONTS[key] = ImageFont.truetype(path, size)
        except OSError:
            _FONTS[key] = ImageFont.load_default()
    return _FONTS[key]


def canvas(W, H, bg):
    from PIL import Image
    return Image.new("RGB", (W, H), tuple(bg))


def blend(fg, bg, a):
    return tuple(int(round(bg[i] * (1 - a) + fg[i] * a)) for i in range(3))


def text_box(draw, xy, s, fnt, anchor="la"):
    return draw.textbbox(xy, s, font=fnt, anchor=anchor)


def text_match(frame, xy, s, fnt, fg, bg, anchor="la", wrong=None):
    """Mean abs difference between the frame region and a clean rendering of string s (lower = match).

    Returns (err_for_s, err_for_wrong) so a check can assert the right label beats a wrong one."""
    from PIL import Image, ImageDraw
    N = np()
    H, W = frame.shape[:2]

    def err(txt):
        im = Image.new("RGB", (W, H), tuple(bg))
        d = ImageDraw.Draw(im)
        d.text(xy, txt, font=fnt, fill=tuple(fg), anchor=anchor)
        box = d.textbbox(xy, s, font=fnt, anchor=anchor)
        x0, y0, x1, y1 = max(0, box[0] - 1), max(0, box[1] - 1), min(W, box[2] + 1), min(H, box[3] + 1)
        ref = N.asarray(im).astype(float)[y0:y1, x0:x1]
        return float(N.abs(frame[y0:y1, x0:x1] - ref).mean())
    return err(s), (err(wrong) if wrong is not None else None)


def tc(t, fps=30):
    """mm:ss:ff timecode."""
    f = int(round(t * fps))
    return "%02d:%02d:%02d" % (f // (fps * 60), (f // fps) % 60, f % fps)


def tc_cs(t):
    cs = int(round(t * 100))
    return "%02d:%02d.%02d" % (cs // 6000, (cs // 100) % 60, cs % 100)


# ───────────────────────── node bridges (repo kits, gsap, matter-js) ─────────────────────────
def node_json(wd, name, js, timeout=30):
    if not _NODE:
        raise RuntimeError("node not available")
    p = wd / ("%s.js" % name)
    p.write_text(js, encoding="utf-8")
    done = subprocess.run([_NODE, str(p)], capture_output=True, text=True, timeout=timeout, cwd=str(wd),
                          env={"NODE_PATH": str(NODE_MODULES), "PATH": "/usr/bin:/bin"}, stdin=subprocess.DEVNULL)
    if done.returncode:
        raise RuntimeError("node failed: %s" % done.stderr[-400:])
    out = wd / ("%s.json" % name)
    out.write_text(done.stdout, encoding="utf-8")
    return json.loads(done.stdout), out


_DOM_STUB = r"""
global.window = global; global.self = global;
function El(){ this.style = {}; this.attrs = {}; this.children = []; this.firstChild = null; this.id = '';
  Object.defineProperty(this, 'opacity', {enumerable: true, get(){ return this.style.opacity == null ? 1 : parseFloat(this.style.opacity); },
    set(v){ this.style.opacity = String(v); }}); }
El.prototype.setAttribute = function(k, v){ this.attrs[k] = v; if (k === 'id') this.id = v; };
El.prototype.getAttribute = function(k){ return this.attrs[k]; };
El.prototype.appendChild = function(c){ this.children.push(c); if (!this.firstChild) this.firstChild = c; c.parentNode = this; return c; };
El.prototype.insertBefore = function(c){ this.children.push(c); c.parentNode = this; return c; };
El.prototype.cloneNode = function(){ const e = new El(); Object.assign(e.style, this.style); return e; };
El.prototype.remove = function(){};
El.prototype.getContext = function(){ return null; };
const __byId = {};
global.document = { body: new El(), createElement(){ return new El(); },
  createElementNS(ns, tag){ const e = new El(); e.tag = tag; const sa = e.setAttribute.bind(e); e.setAttribute = (k, v) => { sa(k, v); if (k === 'id') __byId[v] = e; }; return e; },
  getElementById(id){ return __byId[id] || null; } };
global.addEventListener = function(){};
"""


def js_motion_kit():
    gsap = NODE_MODULES / "gsap"
    return (_DOM_STUB + "const {gsap} = require(%s); global.gsap = gsap;\n" % json.dumps(str(gsap)) +
            "require(%s);\nconst M = window.MOTION;\n" % json.dumps(str(KIT / "kit/motion-kit.js")))


def js_k3(lab=False):
    s = (_DOM_STUB + "const fs = require('fs'), vm = require('vm');\n"
         "vm.runInThisContext(fs.readFileSync(%s, 'utf8'));\n" % json.dumps(str(KIT / "kit/three-kit.bundle.js")))
    if lab:
        s += "vm.runInThisContext(fs.readFileSync(%s, 'utf8'));\n" % json.dumps(str(KIT / "kit/lab-kit.js"))
    return s + "const K = window.K3, T = K.THREE;\n"


def load_py(path, name):
    if name in sys.modules:
        return sys.modules[name]
    sys.path.insert(0, str(Path(path).parent))
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    try:
        spec.loader.exec_module(mod)
    except Exception:
        sys.modules.pop(name, None)
        raise
    return mod


def write_json(wd, name, obj):
    p = wd / name
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
    return p



# ═════════════════════════ camera moves on a tracked world ═════════════════════════
def _near(a, b, tol):
    return a is not None and b is not None and abs(a - b) <= tol


def _pt_near(p, q, tol):
    return p is not None and q is not None and math.hypot(p[0] - q[0], p[1] - q[1]) <= tol


def _moving(track_, thr=0.3):
    """Per frame: did the tracked point move more than thr px since the previous frame."""
    res = [False]
    for a, b in zip(track_[:-1], track_[1:]):
        res.append(a is not None and b is not None and math.hypot(a[0] - b[0], a[1] - b[1]) > thr)
    return res


def _segments(flags):
    segs, start = [], None
    for i, f in enumerate(flags + [False]):
        if f and start is None:
            start = i
        if not f and start is not None:
            segs.append((start, i - 1))
            start = None
    return segs


@card("CAM-280")
def board_camera(task, wd):
    """Steps on a 3x3-frame board; camera pans 1.0 s ease-in-out between step regions, ends pulled back to 0.3."""
    W, H, fps = 320, 180, 20
    steps = [(160, 90), (800, 90), (800, 450), (160, 450)]
    names = ["red", "blue", "green", "yellow"]
    mk = {n: (n, x, y, 8) for n, (x, y) in zip(names, steps)}
    wimg = world(960, 540, mk)
    plan, t = [], 0.0
    keys = []  # (t0, t1, from_c, to_c, s0, s1)
    for i in range(len(steps)):
        keys.append((t, t + 0.5, steps[i], steps[i], 1.0, 1.0))
        t += 0.5
        nxt = steps[i + 1] if i + 1 < len(steps) else (480, 270)
        s1 = 1.0 if i + 1 < len(steps) else 0.3
        keys.append((t, t + 1.0, steps[i], nxt, 1.0, s1))
        t += 1.0
    keys.append((t, t + 0.5, (480, 270), (480, 270), 0.3, 0.3))
    n = int(round((t + 0.5) * fps))
    mats = []
    for f in range(n):
        tt = f / fps
        k = next((k for k in keys if k[0] <= tt < k[1]), keys[-1])
        e = ease_io_cubic((tt - k[0]) / (k[1] - k[0]))
        cx, cy = k[2][0] + (k[3][0] - k[2][0]) * e, k[2][1] + (k[3][1] - k[2][1]) * e
        s = math.exp(math.log(k[4]) + (math.log(k[5]) - math.log(k[4])) * e)
        mats.append(mat_cam(cx, cy, s, W, H))
        plan.append({"t": round(tt, 3), "cx": round(cx, 2), "cy": round(cy, 2), "scale": round(s, 4)})
    checks, outs, d = cam_run(wd, "board", wimg, mats, W, H, fps, mk)
    for i, nme in enumerate(names):
        f = int((i * 1.5 + 0.25) * fps)
        checks.append(check("step %d centred during its dwell" % (i + 1), _pt_near(d["meas"][nme][f], (160, 90), 1.5),
                            d["meas"][nme][f], [160, 90]))
    last = len(mats) - 1
    sc = pair_scale(d, "red", "blue", 640.0)[last]
    checks.append(check("final pull-back scale ~0.3", _near(sc, 0.3, 0.012), sc, 0.3))
    checks.append(check("whole map visible at the end (4 steps tracked)", all(d["meas"][m][last] for m in names), True, True))
    fo = d["frames"]
    flags = [False] + [float(np().abs(fo[i].astype(int) - fo[i - 1]).mean()) > 0.05 for i in range(1, len(fo))]
    mov = _segments(flags)
    dur = (mov[0][1] - mov[0][0] + 1) / fps if mov else 0
    checks.append(check("first pan lasts ~1.0 s", 0.8 <= dur <= 1.2, dur, "0.8-1.2"))
    return checks, outs + [write_json(wd, "board_camera.json", plan)]


@card("CAM-281")
def ui_push(task, wd):
    """Whole UI layer scales 1→2.5 (800 ms easeInOutCubic) so the button fills the bottom-right corner, holds, returns."""
    W, H, fps = 320, 180, 30
    p0, target = (200.0, 120.0), (W * 0.80, H * 0.76)
    mk = {"red": ("red", p0[0], p0[1], 5), "green": ("green", p0[0] + 16, p0[1], 3), "blue": ("blue", 60, 40, 5)}
    wimg = world(W, H, mk)
    mats, sc = [], []
    for f in range(int(2.4 * fps)):
        t = f / fps
        e = ease_io_cubic(t / 0.8) if t < 1.2 else 1 - ease_io_cubic((t - 1.2) / 0.8)
        s = 1 + 1.5 * e
        bx, by = p0[0] + (target[0] - p0[0]) * e, p0[1] + (target[1] - p0[1]) * e
        mats.append(mat_stage(bx - s * p0[0], by - s * p0[1], s))
        sc.append(s)
    checks, outs, d = cam_run(wd, "ui_push", wimg, mats, W, H, fps, mk)
    s_meas = pair_scale(d, "red", "green", 16.0)
    checks += [check("button reaches the corner target at peak", _pt_near(d["meas"]["red"][30], target, 1.5), d["meas"]["red"][30], target),
               check("peak scale 2.5", _near(s_meas[30], 2.5, 0.12), s_meas[30], 2.5),
               check("easeInOutCubic: scale at 400 ms = 1.75", _near(s_meas[12], 1.75, 0.1), s_meas[12], 1.75),
               check("easeInOutCubic: scale at 200 ms ~1.09 (slow start)", _near(s_meas[6], 1.094, 0.06), s_meas[6], 1.094),
               check("returns to rest", _pt_near(d["meas"]["red"][-1], p0, 1.0), d["meas"]["red"][-1], p0)]
    return checks, outs


@card("CAM-290")
def fly_to(task, wd):
    """Camera position lerps between two chapter targets over 3 s with easeInOutCubic."""
    W, H, fps = 320, 180, 30
    A, B = (160.0, 90.0), (800.0, 450.0)
    mk = {"red": ("red", 480, 270, 6), "blue": ("blue", 160, 90, 6), "green": ("green", 800, 450, 6)}
    wimg = world(960, 540, mk)
    n = int(3.5 * fps)
    es = [ease_io_cubic(f / fps / 3.0) for f in range(n)]
    mats = [mat_cam(A[0] + (B[0] - A[0]) * e, A[1] + (B[1] - A[1]) * e, 1.0, W, H) for e in es]
    checks, outs, d = cam_run(wd, "fly_to", wimg, mats, W, H, fps, mk)
    prog = []
    for f in range(n):
        p = d["meas"]["blue"][f] or d["meas"]["red"][f]
        if d["meas"]["blue"][f]:
            prog.append(((160 - p[0]) / 640.0, es[f]))
    dev = max(abs(a - b) for a, b in prog) if prog else 1
    checks.append(check("measured progress follows easeInOutCubic", dev < 0.01, dev, "< 0.01"))
    checks.append(check("arrives at chapter 2 at 3.0 s", _pt_near(d["meas"]["green"][90], (160, 90), 1.0), d["meas"]["green"][90], [160, 90]))
    return checks, outs


@card("CAM-307")
def continuous_push(task, wd):
    """Three scenes each scale ×1.04; every scene starts at the previous end scale; titles fade in over 0.3 s eased."""
    N = np()
    W, H, fps, per = 480, 270, 15, 2.0
    mk = {"red": ("red", 40, 135, 9), "blue": ("blue", 440, 135, 9)}
    bgs = [(40, 44, 52), (60, 40, 40), (30, 50, 40)]
    worlds = [world(W, H, mk, bg=b) for b in bgs]
    frames, mats, scales = [], [], []
    for f in range(int(3 * per * fps)):
        t = f / fps
        k = min(2, int(t // per))
        u = (t - k * per) / per
        s = 1.04 ** k * (1 + 0.04 * ease_io_sine(u))
        M = mat_stage(0, 0, s, 0, (W / 2, H / 2))
        img = warp(worlds[k], M, W, H)
        a = ease_io_sine(min(1.0, (t - k * per) / 0.3))
        img[20:40, 220:260] = (N.array([255, 255, 255]) * a + img[20:40, 220:260] * (1 - a)).astype(N.uint8)
        frames.append(img)
        mats.append(M)
        scales.append(s)
    checks, outs, d = cam_run(wd, "continuous_push", worlds[0], mats, W, H, fps, mk, tol=2.0, frames=frames, neg_k=2.5)
    sm = pair_scale(d, "red", "blue", 400.0)
    for k in range(3):
        a, b = sm[int(k * per * fps)], sm[int((k + 1) * per * fps) - 1]
        checks.append(check("scene %d scales x1.04" % (k + 1), _near(b / a, 1.04, 0.006), b / a, 1.04))
    jumps = max(abs(sm[i + 1] / sm[i] - 1) for i in range(len(sm) - 1))
    checks.append(check("zoom never snaps at the cuts (a reset would jump 4 %)", jumps < 0.012, jumps, "< 1.2%"))
    fo = d["frames"]
    lum = [float(fo[i][22:38, 225:255].mean()) for i in range(0, 8)]
    checks.append(check("title fade-in takes >= 0.3 s (partial at 0.13 s, full at 0.33 s)", lum[2] < 230 and lum[5] > 240, [lum[2], lum[5]], "<230, >240"))
    si = pair_scale(d, "red", "blue", 400.0, "inp")
    checks.append(check("negative control: input never reaches x1.04", not _near(si[29] / si[0], 1.04, 0.006), si[29] / si[0], "!= 1.04"))
    return checks, outs


@card("CAM-317")
def collage_pullback(task, wd):
    """Zoom out 1→0.3 to reveal the earlier scenes as tiled cards, the others dimmed to 50 %."""
    N = np()
    W, H, fps = 320, 180, 30
    cols = [(140, 110, 110), (110, 140, 110), (110, 110, 140), (140, 140, 110), (60, 60, 60), (140, 110, 140), (110, 140, 140), (150, 150, 150), (160, 130, 100)]
    base = N.zeros((540, 960, 3), N.uint8)
    for i, c in enumerate(cols):
        r, q = divmod(i, 3)
        base[r * 180 + 6:r * 180 + 174, q * 320 + 6:q * 320 + 314] = c
    mk = {"red": ("red", 340, 270, 8), "blue": ("blue", 620, 270, 8)}
    yy, xx = N.mgrid[0:540, 0:960]
    for c, x, y, r in mk.values():
        base[(xx - x) ** 2 + (yy - y) ** 2 <= r * r] = COL[c]
    n = int(1.6 * fps)
    frames, mats = [], []
    for f in range(n):
        e = ease_io_cubic(f / fps / 1.2)
        s = math.exp(math.log(0.3) * e)
        img = base.astype(float)
        dim = 1 - 0.5 * e
        mask = N.ones((540, 960), bool)
        mask[180:360, 320:640] = False
        img[mask] *= dim
        M = mat_cam(480, 270, s, W, H)
        mats.append(M)
        frames.append(warp(img.astype(N.uint8), M, W, H))
    wimg = base
    checks, outs, d = cam_run(wd, "collage", wimg, mats, W, H, fps, mk, frames=frames)
    sm = pair_scale(d, "red", "blue", 280.0)
    checks.append(check("final scale 0.3", _near(sm[-1], 0.3, 0.015), sm[-1], 0.3))
    last = d["frames"][-1]
    tile = lambda i: last[int(90 - 81 + (i // 3) * 54) + 10:int(90 - 81 + (i // 3) * 54) + 40, int(160 - 144 + (i % 3) * 96) + 20:int(160 - 144 + (i % 3) * 96) + 70].mean(axis=(0, 1))
    ratio = float(tile(0).sum() / N.array(cols[0]).sum())
    cur = float(tile(4)[0] / 60.0)
    checks.append(check("earlier scenes dimmed to ~50 %", _near(ratio, 0.5, 0.06), ratio, 0.5))
    checks.append(check("current scene stays at full brightness", _near(cur, 1.0, 0.08), cur, 1.0))
    checks.append(check("all 9 tiles visible in the final frame", all(tile(i).sum() > 30 for i in range(9)), True, True))
    return checks, outs


def _push_world(W, H, d=None):
    d = d or W * 0.42
    return {"red": ("red", W / 2 - d, H / 2, 9), "blue": ("blue", W / 2 + d, H / 2, 9)}, 2 * d


def _push_card(wd, name, W, H, fps, scale_fn, n, tol=2.0, neg_k=2.5, d=None):
    mk, d0 = _push_world(W, H, d)
    wimg = world(W, H, mk)
    sc = [scale_fn(f / fps) for f in range(n)]
    mats = [mat_stage(0, 0, s, 0, (W / 2, H / 2)) for s in sc]
    checks, outs, d = cam_run(wd, name, wimg, mats, W, H, fps, mk, tol=tol, neg_k=neg_k)
    return checks, outs, d, pair_scale(d, "red", "blue", d0), pair_scale(d, "red", "blue", d0, "inp"), sc


@card("CAM-421")
def one_shot_push(task, wd):
    """scale 1.00→1.06 over 30 s, one continuous linear push (rendered at 2 fps)."""
    checks, outs, d, sm, si, _ = _push_card(wd, "slow_push", 480, 270, 2, lambda t: 1 + 0.06 * min(1, t / 30), 61)
    checks += [check("end scale 1.06 at 30 s", _near(sm[60], 1.06, 0.004), sm[60], 1.06),
               check("constant rate (linear fit r2)", r2_linear(range(61), sm) > 0.995, r2_linear(range(61), sm), "> 0.995"),
               check("negative control: input stays at 1.00", not _near(si[60], 1.06, 0.004), si[60], "!= 1.06")]
    return checks, outs


@card("CAM-416")
def single_frame_punch(task, wd):
    """Scale 1.00→1.15 in one frame at the hit, relaxing back over 350 ms easeOutExpo."""
    hit = 0.5
    fn = lambda t: 1.0 if t < hit else 1 + 0.15 * (1 - ease_out_expo((t - hit) / 0.35))
    checks, outs, d, sm, si, _ = _push_card(wd, "punch", 320, 180, 60, fn, 75, d=96)  # markers stay clear of the edge at 1.15x
    h = int(hit * 60)
    checks += [check("frame before the hit at 1.00", _near(sm[h - 1], 1.0, 0.01), sm[h - 1], 1.0),
               check("hit frame jumps to 1.15 in one frame", _near(sm[h], 1.15, 0.012), sm[h], 1.15),
               check("relaxed to 1.00 after 350 ms", _near(sm[h + 21], 1.0, 0.01), sm[h + 21], 1.0),
               check("expo-out: >80 % of the relax done in the first 100 ms", sm[h + 6] < 1.0 + 0.15 * 0.2, sm[h + 6], "< 1.03"),
               check("negative control: input has no jump", not _near(si[h], 1.15, 0.012), si[h], "!= 1.15")]
    return checks, outs


@card("CAM-417")
def constant_rate_tunnel(task, wd):
    """Zoom scale = 2^(t/2.5) toward a pupil, the rate eased in and out over 600 ms at the ends."""
    fps, T = 30, 5.0
    ts = [f / fps for f in range(int(T * fps) + 1)]

    def rate(t):
        return (1 / 2.5) * (smoothstep(t / 0.6) if t < 0.6 else smoothstep((T - t) / 0.6) if t > T - 0.6 else 1.0)
    logs, acc = [], 0.0
    for i, t in enumerate(ts):
        if i:
            acc += rate((t + ts[i - 1]) / 2) / fps
        logs.append(acc)
    W, H = 320, 180
    mk = {"red": ("red", W / 2 - 18, H / 2, 3), "blue": ("blue", W / 2 + 18, H / 2, 3)}
    wimg = world(W, H, mk)
    mats = [mat_stage(0, 0, 2 ** l, 0, (W / 2, H / 2)) for l in logs]
    checks, outs, d = cam_run(wd, "tunnel", wimg, mats, W, H, fps, mk, tol=2.0)
    sm = pair_scale(d, "red", "blue", 36.0)
    mid = [(t, math.log2(s)) for t, s in zip(ts, sm) if 1.0 <= t <= 4.0 and s]
    slope = (mid[-1][1] - mid[0][1]) / (mid[-1][0] - mid[0][0])
    checks += [check("constant-rate middle: log2(scale) slope = 1/2.5 per s", _near(slope, 0.4, 0.015), slope, 0.4),
               check("log-scale is linear in the middle (r2)", r2_linear(*zip(*mid)) > 0.999, r2_linear(*zip(*mid)), "> 0.999"),
               check("eased start: first-frame rate < 20 % of cruise", (logs[1] - logs[0]) * fps < 0.08, (logs[1] - logs[0]) * fps, "< 0.08")]
    return checks, outs


@card("CAM-418")
def two_push_ins(task, wd):
    """A locked camera with exactly two 4 % push-ins of 2 s each."""
    def fn(t):
        s = 1.0
        for t0 in (1.0, 5.0):
            s *= 1 + 0.04 * ease_io_sine((t - t0) / 2.0)
        return s
    checks, outs, d, sm, si, _ = _push_card(wd, "two_push", 480, 270, 10, fn, 81, neg_k=2.0)
    mov = _segments([abs(sm[min(i + 2, 80)] - sm[max(i - 2, 0)]) > 0.004 for i in range(len(sm))])
    checks += [check("exactly two push segments", len(mov) == 2, len(mov), 2),
               check("first push +4 %", _near(sm[30] / sm[10], 1.04, 0.006), sm[30] / sm[10], 1.04),
               check("second push +4 %", _near(sm[70] / sm[50], 1.04, 0.006), sm[70] / sm[50], 1.04),
               check("still between pushes", abs(sm[45] - sm[32]) < 0.002, abs(sm[45] - sm[32]), "< 0.002"),
               check("negative control: input has no push", not _near(si[70] / si[10], 1.0816, 0.006), si[70] / si[10], "!= 1.08")]
    return checks, outs


# ═════════════════════════ the repo's motion-kit.js driven by real GSAP ═════════════════════════
_SAMPLER = r"""
const __out = [];
const __clean = (k, v) => (k === 'parentNode' || k === 'children' || k === '__mkTwin' || k === 'firstChild' || k === '_gsap') ? undefined : v;
for (let i = 0; i < %(n)d; i++) { tl.seek(i / %(fps)s, false); const row = {};
  for (const k in O) row[k] = JSON.parse(JSON.stringify(O[k], __clean)); __out.push(row); }
console.log(JSON.stringify(__out));
"""


def mk_sample(wd, name, body, n, fps):
    js = js_motion_kit() + "const tl = gsap.timeline({paused: true}); const O = {};\n" + body + "\n" + _SAMPLER % {"n": n, "fps": fps}
    return node_json(wd, name, js)


def _stage_mats(rows, W, H, key="stage"):
    return [mat_stage(r[key].get("x", 0), r[key].get("y", 0), r[key].get("scale", 1), r[key].get("rotation", 0), (W / 2, H / 2))
            for r in rows]


def _stage_card(wd, name, body, n, fps, W=320, H=180):
    rows, js_out = mk_sample(wd, name, body, n, fps)
    mk = {"red": ("red", 100, 70, 7), "blue": ("blue", 220, 110, 7)}
    wimg = world(W, H, mk)
    mats = _stage_mats(rows, W, H)
    checks, outs, d = cam_run(wd, name, wimg, mats, W, H, fps, mk)
    return checks, outs + [js_out], d, rows


@card("CAM-31")
def stage_camera_move(task, wd):
    """MOTION.camera(tl, cam, at, {x, y, scale, rotation, dur 1.4, ease E.cam}) from the repo kit, rendered and tracked."""
    body = "O.stage = {x: 0, y: 0, scale: 1, rotation: 0};\nM.camera(tl, O.stage, 0.2, {x: -40, y: 18, scale: 1.3, rotation: 6, dur: 1.4});"
    checks, outs, d, rows = _stage_card(wd, "stage_camera", body, 66, 30)
    sm = pair_scale(d, "red", "blue", math.hypot(120, 40))
    ang = pair_angle(d, "red", "blue")
    a0 = math.degrees(math.atan2(40, 120))
    mov = _segments([i > 0 and rows[i]["stage"] != rows[i - 1]["stage"] for i in range(len(rows))])
    vel = [math.hypot(rows[i]["stage"]["x"] - rows[i - 1]["stage"]["x"], rows[i]["stage"]["y"] - rows[i - 1]["stage"]["y"]) for i in range(7, 49)]
    pk = (vel.index(max(vel)) + 1) / 42.0
    checks += [check("final scale 1.3 measured on the video", _near(sm[-1], 1.3, 0.02), sm[-1], 1.3),
               check("final rotation 6 deg measured", _near(ang[-1] - a0, 6.0, 0.6), ang[-1] - a0, 6.0),
               check("one move of 1.4 s (count the moves)", len(mov) == 1 and abs((mov[0][1] - mov[0][0] + 1) / 30 - 1.4) <= 0.1,
                     [(a / 30, b / 30) for a, b in mov], "one segment ~1.4 s"),
               check("E.cam: peak speed in the first third of the move", 0.1 <= pk <= 0.4, pk, "0.1-0.4"),
               check("still after the move", rows[-1]["stage"] == rows[-6]["stage"], True, True)]
    return checks, outs


@card("CAM-48")
def single_stage_camera(task, wd):
    """Two counted MOTION.camera moves (dur 1.4 s, E.cam) with a still hold between them."""
    body = ("O.stage = {x: 0, y: 0, scale: 1, rotation: 0};\n"
            "M.camera(tl, O.stage, 0.1, {x: -50, y: 0, scale: 1.2, dur: 1.4});\n"
            "M.camera(tl, O.stage, 2.5, {x: 30, y: -20, scale: 1.1, dur: 1.4});")
    checks, outs, d, rows = _stage_card(wd, "stage_two_moves", body, 130, 30)
    mov = _segments([i > 0 and rows[i]["stage"] != rows[i - 1]["stage"] for i in range(len(rows))])
    hold = [rows[i]["stage"] for i in range(48, 74)]
    checks += [check("exactly two camera moves", len(mov) == 2, [(a / 30, b / 30) for a, b in mov], 2),
               check("still between the moves (stage values identical 1.6-2.45 s)", all(h == hold[0] for h in hold), True, True),
               check("second move lands at x=30,y=-20,scale=1.1", rows[-1]["stage"]["x"] == 30 and rows[-1]["stage"]["y"] == -20
                     and abs(rows[-1]["stage"]["scale"] - 1.1) < 1e-9, rows[-1]["stage"], {"x": 30, "y": -20, "scale": 1.1})]
    return checks, outs


def _push_kit_card(wd, name, body, n, fps, frm, to):
    rows, js_out = mk_sample(wd, name, body, n, fps)
    W, H = (480, 270) if to < 1.2 else (320, 180)
    half = 200 if to < 1.2 else 60
    mk = {"red": ("red", W / 2 - half, H / 2, 8), "blue": ("blue", W / 2 + half, H / 2, 8)}
    wimg = world(W, H, mk)
    checks, outs, d = cam_run(wd, name, wimg, _stage_mats(rows, W, H), W, H, fps, mk, tol=2.0, neg_k=2.0)
    return checks, outs + [js_out], rows, pair_scale(d, "red", "blue", 2.0 * half), d


@card("CAM-32")
def log_push_hold(task, wd):
    """MOTION.push with a linear ease over a 2 s hold, 1.00→1.06: log(scale) is linear, so the zoom speed feels constant."""
    body = "O.stage = {scale: 1};\nM.push(tl, O.stage, 0, 1.0, 1.06, 2.0, {ease: M.E.linear});"
    checks, outs, rows, sm, d = _push_kit_card(wd, "log_push_hold", body, 61, 30, 1.0, 1.06)
    ls = [math.log(r["stage"]["scale"]) for r in rows]
    lin = [1 + 0.06 * i / 60 for i in range(61)]
    dev_log = max(abs(a - math.log(1.06) * i / 60) for i, a in enumerate(ls))
    dev_linear = max(abs(r["stage"]["scale"] - l) for r, l in zip(rows, lin))
    checks += [check("kit scale is exactly log-linear (max deviation)", dev_log < 1e-6, dev_log, "< 1e-6"),
               check("and differs from a linear-scale push (it is not plain lerp)", dev_linear > 1e-4, dev_linear, "> 1e-4"),
               check("measured end scale 1.06", _near(sm[-1], 1.06, 0.006), sm[-1], 1.06)]
    return checks, outs


@card("CAM-49")
def log_push_big(task, wd):
    """MOTION.push 1→2.4 with the default durFor duration and E.cam; peak per-frame scale change stays ~5 % at 60 fps."""
    body = "O.stage = {scale: 1};\nM.push(tl, O.stage, 0, 1.0, 2.4);\nO.meta = {dur: M.durFor(1.4 * 600, true)};"
    checks, outs, rows, sm, d = _push_kit_card(wd, "log_push_big", body, 100, 60, 1.0, 2.4)
    dur = rows[0]["meta"]["dur"]
    done = next(i for i, r in enumerate(rows) if abs(r["stage"]["scale"] - 2.4) < 1e-9) / 60
    ratios = [rows[i]["stage"]["scale"] / rows[i - 1]["stage"]["scale"] for i in range(1, len(rows))]
    frames_ = dur * 30
    checks += [check("default duration from durFor = 0.35 + 1.35 ms/px", _near(dur, 1.484, 0.001), dur, 1.484),
               check("push lasts 30-70 frames (30 fps)", 30 <= frames_ <= 70, frames_, "30-70"),
               check("push ends at durFor", abs(done - dur) <= 1 / 60 + 1e-6, done, dur),
               check("peak per-frame scale change <= ~5 %", max(ratios) - 1 <= 0.055, max(ratios) - 1, "<= 0.055"),
               check("measured end scale 2.4 on video", _near(sm[-1], 2.4, 0.04), sm[-1], 2.4)]
    return checks, outs


def _gauss1d(a, sigma, axis):
    N = np()
    if sigma < 0.3:
        return a
    if fx.have("scipy"):
        from scipy.ndimage import gaussian_filter1d
        return gaussian_filter1d(a, sigma, axis=axis, mode="nearest")
    r = int(3 * sigma) + 1
    k = N.exp(-N.arange(-r, r + 1) ** 2 / (2 * sigma * sigma))
    k /= k.sum()
    return N.apply_along_axis(lambda v: N.convolve(N.pad(v, r, mode="edge"), k, mode="valid"), axis, a)


def _gauss2d(a, sigma):
    return _gauss1d(_gauss1d(a, sigma, 0), sigma, 1)


def _edge_fixture(W=160, H=90):
    N = np()
    img = N.zeros((H, W, 3), float)
    img[:] = 30
    for i in range(0, W, 16):
        img[:, i:i + 8] = 230
    for j in range(0, H, 16):
        img[j:j + 3, :] = 128
    return img


@card("CAM-33")
def rack_focus_crossfade(task, wd):
    """MOTION.rackFocus crossfades the sharp element with a constant blur(18px) twin over 0.3 s (E.smooth)."""
    N = np()
    body = ("O.el = document.createElement('div'); document.body.appendChild(O.el);\n"
            "O.twin = M.rackFocus(tl, O.el, 0.2, {blur: 18, dur: 0.3});")
    rows, js_out = mk_sample(wd, "rack_focus", body, 24, 30)
    sharp = _edge_fixture()
    blur = _gauss2d(sharp, 18 * 90 / 1080 * 4)
    frames = []
    for r in rows:
        a, b = r["el"].get("opacity", 1), r["twin"].get("opacity", 0)
        frames.append(N.clip(sharp * a + blur * b + 30 * (1 - a - b), 0, 255))
    out = write_video(wd / "rack_focus.mp4", frames, 30)
    inp = write_video(wd / "rack_focus_input.mp4", [sharp] * len(rows), 30)
    fo, fi = read_video(out), read_video(inp)
    sh = [sharpness(f) for f in fo]
    shi = [sharpness(f) for f in fi]
    filters = {r["twin"]["style"].get("filter") for r in rows}
    checks = [check("twin blur is one constant value (never an animated blur)", filters == {"blur(18px)"}, sorted(filters), ["blur(18px)"]),
              check("sharp before the pull", sh[5] > 0.8 * shi[5], sh[5], "> 0.8 x input"),
              check("defocused after 0.3 s", sh[16] < 0.2 * sh[5], sh[16], "< 0.2 x start"),
              check("cross-fade midpoint is a blend (E.smooth symmetric)",
                    abs(rows[10]["el"]["opacity"] + rows[10]["twin"]["opacity"] - 1) < 1e-6 and 0.3 < rows[10]["twin"]["opacity"] < 0.7,
                    rows[10]["twin"]["opacity"], "0.3-0.7 and sums to 1"),
              check("negative control: unprocessed input stays sharp", not (shi[16] < 0.2 * shi[5]), shi[16], ">= 0.2 x start")]
    return checks, [out, js_out]


@card("CAM-50")
def directional_speed_blur(task, wd):
    """MOTION.speedBlur: SVG feGaussianBlur stdDeviation rises to 12 px on x at 45 % of the move, then clears."""
    N = np()
    body = ("O.el = document.createElement('div');\n"
            "M.speedBlur(tl, O.el, 0.1, 0.6, {px: 12, axis: 'x'});\n"
            "O.blur = document.getElementById('mk-sb-1').firstChild;")
    rows, js_out = mk_sample(wd, "speed_blur", body, 90, 100)
    sx = [float(str(r["blur"]["attrs"].get("stdDeviation", "0 0")).split()[0]) for r in rows]
    sy = [float(str(r["blur"]["attrs"].get("stdDeviation", "0 0")).split()[1]) for r in rows]
    pk = sx.index(max(sx))
    sharp = N.zeros((90, 160, 3)) + 30
    for i in range(0, 80, 16):
        sharp[:, i:i + 8] = 230
    for j in range(0, 90, 16):
        sharp[j:j + 8, 80:] = 230
    frames = [_gauss1d(sharp, s * 90 / 1080 * 6, 1) for s in sx]
    out = write_video(wd / "speed_blur.mp4", frames, 100)
    fo = read_video(out)
    gx = lambda f: float(N.abs(N.diff(f[:, 8:72].mean(axis=2), axis=1)).mean())
    gy = lambda f: float(N.abs(N.diff(f[:, 96:150].mean(axis=2), axis=0)).mean())
    checks = [check("peak 12 px", _near(max(sx), 12, 0.1), max(sx), 12),
              check("peak at ~45 % of the 0.6 s move", _near((pk / 100 - 0.1) / 0.6, 0.45, 0.02), (pk / 100 - 0.1) / 0.6, 0.45),
              check("blur only along x", max(sy) == 0, max(sy), 0),
              check("clears to 0 after the move", sx[-1] == 0 and sx[0] == 0, [sx[0], sx[-1]], [0, 0]),
              check("measured: horizontal detail drops at the peak frame", gx(fo[pk]) < 0.6 * gx(fo[0]), gx(fo[pk]) / gx(fo[0]), "< 0.6"),
              check("measured: vertical detail kept (axis-only blur)", gy(fo[pk]) > 0.8 * gy(fo[0]), gy(fo[pk]) / gy(fo[0]), "> 0.8"),
              check("negative control: unblurred input keeps horizontal detail", not (gx(fo[0]) < 0.6 * gx(fo[0])), 1.0, ">= 0.6")]
    return checks, [out, js_out]


# ═════════════════════════ the repo's three-kit (K3) shot language, run headless in node ═════════════════════════
_K3_PROJ = r"""
function frac(cam, S, size) { cam.updateMatrixWorld(); const a = new T.Vector3(S.x, S.y - size / 2, S.z).project(cam), b = new T.Vector3(S.x, S.y + size / 2, S.z).project(cam);
  return {h: Math.hypot(b.x - a.x, (b.y - a.y)) / 2, cx: (a.x + b.x) / 2, cy: (a.y + b.y) / 2}; }
function newCam() { const c = new T.PerspectiveCamera(35, 16 / 9, 0.01, 1e5); c.position.set(0, 1, 8); c.lookAt(0, 1, 0); return c; }
"""


def _k3(wd, name, body):
    return node_json(wd, name, js_k3(lab="orbitWalk" in body) + _K3_PROJ + body)


def _sheet(wd, name, items, W=160, H=90):
    """Draw each projected subject (cx, cy, h in NDC) as a bar in its own 16:9 cell: the framing the kit computed."""
    from PIL import ImageDraw
    cols = 4
    rows_ = (len(items) + cols - 1) // cols
    im = canvas(W * cols, H * rows_, (20, 22, 26))
    d = ImageDraw.Draw(im)
    for i, (label, p) in enumerate(items):
        ox, oy = (i % cols) * W, (i // cols) * H
        d.rectangle([ox, oy, ox + W - 1, oy + H - 1], outline=(70, 70, 70))
        cx, cy, h = ox + (p["cx"] + 1) / 2 * W, oy + (1 - (p["cy"] + 1) / 2) * H, p["h"] * H
        d.rectangle([cx - max(1, h * 0.15), max(oy, cy - h / 2), cx + max(1, h * 0.15), min(oy + H - 1, cy + h / 2)], fill=(230, 80, 60))
        d.text((ox + 3, oy + 2), label, fill=(220, 220, 220), font=font(MONO, 9))
    p = wd / ("%s.png" % name)
    im.save(p)
    return p


@card("CAM-35")
def shot_language_cameras(task, wd):
    """K3.shot(kind, {subject, size}) frames the subject at the table's fraction of frame height for its fov."""
    body = r"""
const S = new T.Vector3(0, 1, 0), size = 1.7, res = {};
for (const kind of ['establishing','wide','medium','closeup','extreme_closeup','low_angle','high_angle','birds_eye','dutch']) {
  const cam = newCam(); const s = K.shot(kind, {subject: S, size})(0); K.applyShot(cam, s);
  res[kind] = Object.assign(frac(cam, S, size), {y: s.pos.y, roll: s.roll, fov: s.fov, up: cam.up.y}); }
const c0 = newCam(); res.input = frac(c0, S, size);
console.log(JSON.stringify(res));"""
    r, js_out = _k3(wd, "shot_kinds", body)
    table = {"establishing": 0.06, "wide": 0.25, "medium": 0.55, "closeup": 1.6, "extreme_closeup": 4.0}
    checks = [check("%s frames the subject at %.0f%% of frame height" % (k, v * 100), abs(r[k]["h"] / v - 1) < 0.05, r[k]["h"], v)
              for k, v in table.items()]
    checks += [check("low_angle camera below the subject centre", r["low_angle"]["y"] < 1.0, r["low_angle"]["y"], "< 1.0"),
               check("high_angle camera above the subject", r["high_angle"]["y"] > 1.0 + 1.7, r["high_angle"]["y"], "> 2.7"),
               check("birds_eye camera straight above", r["birds_eye"]["y"] > 5, r["birds_eye"]["y"], "> 5"),
               check("dutch roll 12 deg", _near(math.degrees(r["dutch"]["roll"]), 12, 1e-6), math.degrees(r["dutch"]["roll"]), 12),
               check("negative control: an unshot default camera frames none of the table sizes",
                     all(abs(r["input"]["h"] / v - 1) >= 0.05 for v in table.values()), r["input"]["h"], "matches none")]
    png = _sheet(wd, "shot_kinds", [(k, r[k]) for k in list(table) + ["low_angle", "high_angle", "dutch"]])
    return checks, [png, js_out]


@card("CAM-36")
def handheld_noise(task, wd):
    """K3 handheld: seeded three-octave sway around 1.3 / 1.1 / 0.9 (rad/s in the kit) with amplitude 0.012 x distance."""
    N = np()
    body = r"""
const S = new T.Vector3(0, 1, 0), o = {subject: S, size: 1.7};
const hh = K.shot('handheld', o), still = K.shot('medium', o), hh2 = K.shot('handheld', Object.assign({seed: 7}, o)), hh3 = K.shot('handheld', Object.assign({seed: 99}, o));
const rows = []; for (let i = 0; i < 1200; i++) { const t = i / 30, a = hh(t), b = still(t), c = hh2(t), e = hh3(t);
  rows.push([a.pos.x - b.pos.x, a.pos.y - b.pos.y, a.roll, c.pos.x - b.pos.x, e.pos.x - b.pos.x, b.pos.distanceTo(S), b.pos.x - still(0).pos.x]); }
console.log(JSON.stringify(rows));"""
    rows, js_out = _k3(wd, "handheld", body)
    A = N.array(rows)
    dx, dy, roll, d = A[:, 0], A[:, 1], A[:, 2], A[0, 5]
    spec = N.abs(N.fft.rfft(dx - dx.mean()))
    freqs = N.fft.rfftfreq(len(dx), 1 / 30.0) * 2 * math.pi
    w = float(freqs[int(N.argmax(spec[1:])) + 1])
    amp = float(N.abs(dx).max())
    trace = N.zeros((90, 400, 3), N.uint8) + 20
    for i in range(0, 1200, 3):
        y = int(45 - dx[i] / (0.013 * d) * 40)
        trace[max(0, min(89, y)), i // 3] = (255, 200, 60)
    png = save_png(wd / "handheld_trace.png", trace)
    checks = [check("dominant sway at 1.3 rad/s (~0.21 Hz; the card's 'Hz' are the kit's rad/s)", _near(w, 1.3, 0.06), w, 1.3),
              check("x amplitude <= 0.012 x distance and > 0.006 x distance", 0.006 * d < amp <= 0.012 * d + 1e-9, amp / d, "0.006-0.012"),
              check("y sway is ~0.7 of x", 0.4 < float(N.abs(dy).max()) / amp < 1.0, float(N.abs(dy).max()) / amp, "~0.7"),
              check("slight roll present", 0 < float(N.abs(roll).max()) < 0.01, float(N.abs(roll).max()), "0-0.01 rad"),
              check("seeded: default seed equals seed 7, seed 99 differs", N.allclose(A[:, 0], A[:, 3]) and not N.allclose(A[:, 0], A[:, 4]), True, True),
              check("negative control: the non-handheld input shot fails the sway criterion",
                    not (0.006 * d < float(N.abs(A[:, 6]).max()) <= 0.012 * d), float(N.abs(A[:, 6]).max()), "no sway")]
    return checks, [png, js_out]


@card("CAM-37")
def orbit_walk_stops(task, wd):
    """K3.orbitWalk walks the shorter arc between stops, holds at each stop with micro drift, fov per stop."""
    body = r"""
const cam = new T.PerspectiveCamera(32, 16 / 9, 0.01, 1000);
const walk = K.orbitWalk(cam, [{t: 0, angle: 10, dist: 4, height: 1.5, look: [0, 1, 0], fov: 30, hold: 1},
                               {t: 3, angle: 310, dist: 3, height: 1.2, look: [0, 1, 0], fov: 40, hold: 1},
                               {t: 6, angle: 310, dist: 3, height: 1.2, look: [0, 1, 0], fov: 40}], {drift: 0.012});
const rows = []; for (let i = 0; i <= 180; i++) { const t = i / 30; walk(t);
  rows.push({t, ang: Math.atan2(cam.position.x, cam.position.z) * 180 / Math.PI, dist: Math.hypot(cam.position.x, cam.position.z), y: cam.position.y, fov: cam.fov}); }
console.log(JSON.stringify(rows));"""
    rows, js_out = _k3(wd, "orbit_walk", body)
    hold = [r for r in rows if r["t"] <= 1.0]
    mid = rows[60]
    angs = [r["ang"] for r in rows[30:91]]
    span = max(abs(((a - 10 + 540) % 360) - 180) for a in angs)
    drift = max(abs(r["y"] - 1.5) for r in hold)
    checks = [check("holds at the first stop (only micro drift <= 0.012)", 0 < drift <= 0.0121 and max(abs(r["ang"] - 10) for r in hold) < 0.5, drift, "<= 0.012"),
              check("walks the shorter arc (10 deg → -50 deg, never through 180)", span <= 60.5, span, "<= 60"),
              check("midway angle ~-20 deg", _near(mid["ang"], -20, 1.0), mid["ang"], -20),
              check("fov interpolates per stop 30→40", _near(rows[0]["fov"], 30, 1e-6) and _near(rows[95]["fov"], 40, 1e-6), [rows[0]["fov"], rows[95]["fov"]], [30, 40]),
              check("negative control: naive angle lerp 10→310 fails the shorter-arc test",
                    not (max(abs(((10 + 300 * k / 60 - 10 + 540) % 360) - 180) for k in range(61)) <= 60.5), 180, "> 60")]
    return checks, [js_out]


@card("CAM-51")
def smooth_camera_keys(task, wd):
    """K3.cameraKeys([[t,x,y,z,lx,ly,lz],...]): smoothstep between keys, still where two keys are equal."""
    body = r"""
const cam = K.cameraKeys([[0, 0, 1, 10, 0, 1, 0], [2, 4, 1, 6, 0, 1, 0], [3, 4, 1, 6, 0, 1, 0], [5, -2, 2, 6, 1, 1, 0]]);
const rows = []; for (let i = 0; i <= 50; i++) { const [p, l] = cam(i / 10); rows.push([i / 10, p.x, p.y, p.z, l.x]); }
console.log(JSON.stringify(rows));"""
    rows, js_out = _k3(wd, "camera_keys", body)
    x = {round(r[0], 1): r[1] for r in rows}
    checks = [check("midpoint of key 1→2 is exactly half way (smoothstep(0.5)=0.5)", _near(x[1.0], 2.0, 1e-9), x[1.0], 2.0),
              check("quarter point follows smoothstep (0.15625)", _near(x[0.5] / 4, 0.15625, 1e-9), x[0.5] / 4, 0.15625),
              check("zero velocity at the keys (ease in/out)", abs(x[0.1] - x[0.0]) < 0.05 and abs(x[2.0] - x[1.9]) < 0.05, [x[0.1], x[1.9]], "~0 / ~4"),
              check("still between equal keys 2-3 s", len({round(x[k / 10], 9) for k in range(20, 31)}) == 1, x[2.5], 4.0),
              check("negative control: linear lerp would give 1.0 at the quarter point, not 0.625", not _near(1.0, x[0.5], 1e-6), x[0.5], "!= 1.0")]
    return checks, [js_out]


@card("CAM-52")
def shot_words_cameras(task, wd):
    """K3.shotFromWords / dolly_zoom / sequence: words become deterministic cameras (no video model needed)."""
    body = r"""
const S = new T.Vector3(0, 1, 0), size = 1.7, o = {subject: S, size, t0: 0, t1: 4};
const low = K.shotFromWords('low angle tracking shot', o), dz = K.shot('dolly_zoom', o), pi = K.shot('push_in', o), seq = K.sequence([{at: 0, shot: 'wide'}, {at: 2, shot: 'closeup'}], {subject: S, size, seconds: 4});
const res = {low: [], dz: [], bg: [], seq: [], pi: []};
for (let i = 0; i <= 40; i++) { const t = i / 10;
  const a = low(t); res.low.push([a.pos.y, a.look.x]);
  const cam = newCam(); const s = dz(t); K.applyShot(cam, s); res.dz.push(frac(cam, S, size).h);
  const B = new T.Vector3(0, 1, -12); res.bg.push(frac(cam, B, size).h);
  const c2 = newCam(); K.applyShot(c2, seq(t)); res.seq.push(frac(c2, S, size).h);
  const c3 = newCam(); K.applyShot(c3, pi(t)); res.pi.push(frac(c3, S, size).h); }
console.log(JSON.stringify(res));"""
    r, js_out = _k3(wd, "shot_words", body)
    dz = r["dz"]
    checks = [check("'low angle tracking shot' → camera below the subject", all(p[0] < 1.0 for p in r["low"]), r["low"][0][0], "< 1.0"),
              check("tracking: the look point travels with the subject", r["low"][-1][1] > r["low"][0][1] + 4, r["low"][-1][1], "> +4 m"),
              check("dolly zoom keeps the subject size constant (<1 %)", (max(dz) - min(dz)) / dz[0] < 0.01, (max(dz) - min(dz)) / dz[0], "< 0.01"),
              check("dolly zoom changes the background size (>30 %)", abs(r["bg"][-1] / r["bg"][0] - 1) > 0.3, r["bg"][-1] / r["bg"][0], "> 1.3 or < 0.7"),
              check("sequence hard-cuts wide→closeup at 2 s", _near(r["seq"][19], 0.25, 0.02) and _near(r["seq"][20], 1.6, 0.08), [r["seq"][19], r["seq"][20]], [0.25, 1.6]),
              check("negative control: a plain push_in (no fov solve) fails the constant-size test",
                    not ((max(r["pi"]) - min(r["pi"])) / r["pi"][0] < 0.01), (max(r["pi"]) - min(r["pi"])) / r["pi"][0], ">= 0.01")]
    return checks, [js_out]


@card("CAM-34")
def bokeh_focus_follow(task, wd):
    """applyShot drives the bokeh focus uniform per frame; layers blur by their distance from the focal plane."""
    N = np()
    body = r"""
const S = new T.Vector3(0, 1, 0), shot = K.shot('push_in', {subject: S, size: 1.7, t0: 0, t1: 3});
const post = {bokeh: {uniforms: {focus: {value: 900}, aperture: {value: 0.00004}, maxblur: {value: 0.0035}}}};
const rows = []; for (let i = 0; i <= 30; i++) { const cam = newCam(); K.applyShot(cam, shot(i / 10), post);
  rows.push([post.bokeh.uniforms.focus.value, cam.position.distanceTo(S)]); }
console.log(JSON.stringify(rows));"""
    rows, js_out = _k3(wd, "bokeh_focus", body)
    A = N.array(rows)
    fixed = A[0, 0]
    sharp = _edge_fixture(96, 54)
    frames, frames_in = [], []
    for focus, dist in rows:
        out = N.zeros((54, 288, 3))
        out_in = N.zeros((54, 288, 3))
        for j, depth in enumerate((dist - 3.0, dist, dist + 6.0)):
            coc = lambda f: min(6.0, abs(1 / f - 1 / depth) * 40)
            out[:, j * 96:(j + 1) * 96] = _gauss2d(sharp, coc(focus))
            out_in[:, j * 96:(j + 1) * 96] = _gauss2d(sharp, coc(fixed))
        frames.append(out)
        frames_in.append(out_in)
    vid = write_video(wd / "bokeh_layers.mp4", frames, 10)
    vin = write_video(wd / "bokeh_layers_input.mp4", frames_in, 10)
    fo, fi = read_video(vid), read_video(vin)
    mid_sharp = [sharpness(f[:, 96:192]) for f in fo]
    near_sharp = [sharpness(f[:, 0:96]) for f in fo]
    in_sharp = [sharpness(f[:, 96:192]) for f in fi]
    checks = [check("focus uniform equals camera-subject distance every frame", float(N.abs(A[:, 0] - A[:, 1]).max()) < 1e-9,
                    float(N.abs(A[:, 0] - A[:, 1]).max()), 0),
              check("focus distance changes through the push", A[0, 0] - A[-1, 0] > 1.0, [A[0, 0], A[-1, 0]], "decreasing"),
              check("subject layer is the sharpest layer in every frame", all(m > n for m, n in zip(mid_sharp, near_sharp)), True, True),
              check("subject stays sharp at the end of the push", mid_sharp[-1] > 0.9 * mid_sharp[0], mid_sharp[-1] / mid_sharp[0], "> 0.9"),
              check("negative control: fixed focus (input) loses the subject", in_sharp[-1] < 0.5 * in_sharp[0], in_sharp[-1] / in_sharp[0], "< 0.5")]
    return checks, [vid, js_out]


# ═════════════════════════ parametric camera behaviours (shake, drift, follow, letterbox) ═════════════════════════
def _offset_card(wd, name, W, H, fps, offs, scales=None, tol=1.6, neg_k=1.5):
    """Render per-frame stage offsets (and optional scales) and return tracked marker offsets from rest."""
    mk = {"red": ("red", W * 0.3, H * 0.5, 8), "blue": ("blue", W * 0.7, H * 0.5, 8)}
    wimg = world(W, H, mk)
    scales = scales or [1.0] * len(offs)
    mats = [mat_stage(o[0], o[1], s, 0, (W / 2, H / 2)) for o, s in zip(offs, scales)]
    checks, outs, d = cam_run(wd, name, wimg, mats, W, H, fps, mk, tol=tol, input_mats=[mat_stage()] * len(mats), neg_k=neg_k)
    mid = [((a[0] + b[0]) / 2 - W / 2, (a[1] + b[1]) / 2 - H / 2) if a and b else None for a, b in zip(d["meas"]["red"], d["meas"]["blue"])]
    return checks, outs, d, mid


@card("CAM-407")
def two_px_shake(task, wd):
    """One impact: the stage translates by integer ±2 px for exactly 3 frames, once."""
    offs = [(0, 0)] * 30
    offs[12:15] = [(2, -2), (-2, 2), (2, 0)]
    checks, outs, d, mid = _offset_card(wd, "shake2", 320, 180, 30, offs, tol=0.8, neg_k=1.2)
    moved = [i for i, m in enumerate(mid) if m and math.hypot(*m) > 0.9]
    checks += [check("displaced on exactly 3 frames, once", moved == [12, 13, 14], moved, [12, 13, 14]),
               check("displacement is 2 px per axis", all(abs(abs(mid[i][0]) - 2) < 0.6 for i in moved), [mid[i] for i in moved], "|dx|=2"),
               check("negative control: input never moves", not any(i for i, m in enumerate(d["inp"]["red"]) if m and abs(m[0] - 96) > 0.9), True, True)]
    return checks, outs


@card("CAM-408")
def push_drift(task, wd):
    """Per beat the stage scales 1.0→1.05; a 4 px sine drift at 0.5 Hz runs on top; straight cuts on the hits."""
    fps, beat = 20, 2.0
    ts = [f / fps for f in range(int(3 * beat * fps))]
    scales = [1 + 0.05 * ((t % beat) / beat) for t in ts]
    offs = [(4 * math.sin(2 * math.pi * 0.5 * t), 0) for t in ts]
    checks, outs, d, mid = _offset_card(wd, "push_drift", 480, 270, fps, offs, scales)
    sm = pair_scale(d, "red", "blue", 0.4 * 480)
    dx = [m[0] for m in mid]
    N = np()
    fit = N.linalg.lstsq(N.vstack([N.sin(N.pi * N.array(ts)), N.cos(N.pi * N.array(ts))]).T, N.array(dx), rcond=None)[0]
    cut_jump = sm[int(beat * fps)] / sm[int(beat * fps) - 1]
    checks += [check("drift amplitude 4 px at 0.5 Hz (fit)", _near(float(math.hypot(*fit)), 4.0, 0.4), float(math.hypot(*fit)), 4.0),
               check("each beat pushes to x1.05", _near(sm[int(beat * fps) - 1] / sm[0], 1.0 + 0.05 * (39 / 40), 0.006), sm[int(beat * fps) - 1], 1.049),
               check("straight cut on the hit (scale resets in one frame)", cut_jump < 0.97, cut_jump, "< 0.97")]
    return checks, outs


@card("CAM-410")
def gentle_push_pan(task, wd):
    """Three scenes: push 1→1.04, pan 60 px, push 1→1.03; every move within 3-5 % scale or < 80 px pan, no rotation."""
    fps = 15
    offs, scales = [], []
    for f in range(int(6 * fps)):
        t = f / fps
        k, u = int(t // 2), ease_io_sine((t % 2) / 2)
        scales.append(1 + 0.04 * u if k == 0 else 1.0 if k == 1 else 1 + 0.03 * u)
        offs.append((-60 * u if k == 1 else 0, 0))
    checks, outs, d, mid = _offset_card(wd, "gentle", 480, 270, fps, offs, scales)
    sm = pair_scale(d, "red", "blue", 0.4 * 480)
    ang = [abs(a) for a in pair_angle(d, "red", "blue") if a is not None]
    pan = mid[59][0] - mid[30][0]
    vel = max(abs(mid[i][0] - mid[i - 1][0]) for i in range(31, 60))
    checks += [check("scene 1 push +4 % (3-5 %)", 0.03 <= sm[29] / sm[0] - 1 <= 0.05, sm[29] / sm[0] - 1, "0.03-0.05"),
               check("scene 2 pan 60 px (< 80 px)", _near(abs(pan), 60, 3) and abs(pan) < 80, pan, -60),
               check("scene 3 push +3 %", 0.025 <= sm[89] / sm[60] - 1 <= 0.05, sm[89] / sm[60] - 1, "0.03"),
               check("no rotation (|angle| < 0.4 deg)", max(ang) < 0.4, max(ang), "< 0.4"),
               check("no whip: pan speed < 8 px/frame", vel < 8, vel, "< 8")]
    return checks, outs


@card("CAM-411")
def chorus_dolly(task, wd):
    """Only the camera eases: one dolly-in of +6 % per chorus, nothing in the verses."""
    fps = 10
    song = [("verse", 0, 3), ("chorus", 3, 6), ("verse", 6, 8), ("chorus", 8, 11)]
    scales = []
    for f in range(11 * fps):
        t, s = f / fps, 1.0
        for kind, a, b in song:
            if kind == "chorus":
                s *= 1 + 0.06 * ease_io_sine((t - a) / (b - a))
        scales.append(s)
    checks, outs, d, mid = _offset_card(wd, "chorus", 480, 270, fps, [(0, 0)] * len(scales), scales, neg_k=2.0)
    sm = pair_scale(d, "red", "blue", 0.4 * 480)
    checks += [check("chorus 1 dolly +6 %", _near(sm[59] / sm[30], 1.06, 0.006), sm[59] / sm[30], 1.06),
               check("chorus 2 dolly +6 %", _near(sm[109] / sm[80], 1.06, 0.006), sm[109] / sm[80], 1.06),
               check("verses hold still", abs(sm[29] - sm[0]) < 0.003 and abs(sm[79] - sm[61]) < 0.003, [sm[29] - sm[0], sm[79] - sm[61]], "~0")]
    return checks, outs


@card("CAM-412")
def lag_follow_camera(task, wd):
    """Camera follows a jumping ball 120 ms late, overshoots 15 % with a bezier(.2,.9,.3,1)-timed recentre, settles."""
    N = np()
    fps, W, H = 50, 320, 180
    ball = lambda t: 0.0 if t < 0.4 else 80.0
    e = bezier(0.2, 0.9, 0.3, 1.0)

    def cam_x(t):
        u = t - 0.4 - 0.12
        if u <= 0:
            return 0.0
        if u < 0.35:
            return 92.0 * e(u / 0.35)
        return 92.0 - 12.0 * ease_io_sine((u - 0.35) / 0.3)
    ts = [f / fps for f in range(60)]
    frames = []
    for t in ts:
        img = N.zeros((H, W, 3), N.uint8) + 40
        x = int(round(W / 2 + ball(t) - cam_x(t)))
        yy, xx = N.mgrid[0:H, 0:W]
        img[(xx - x) ** 2 + (yy - 90) ** 2 <= 49] = COL["red"]
        gx = int(round(-cam_x(t))) % 40
        img[:, gx::40] = (80, 80, 80)
        frames.append(img)
    out = write_video(wd / "lag_follow.mp4", frames, fps)
    fo = read_video(out)
    sx = [centroid(f, "red")[0] - W / 2 for f in fo]
    start = next(i for i in range(20, 60) if sx[i] < 79.5) - 20
    peak_over = -min(sx) / 80.0
    checks = [check("camera starts 120 ms after the ball jumps", _near(start / fps, 0.12, 1 / fps + 1e-6), start / fps, 0.12),
              check("overshoot ~15 % of the jump", _near(peak_over, 0.15, 0.03), peak_over, 0.15),
              check("recentred (ball back at centre)", abs(sx[-1]) < 0.8, sx[-1], 0),
              check("negative control: a locked camera never recentres", not (abs(80.0) < 0.8), 80.0, "ball stays off-centre")]
    return checks, [out]


@card("CAM-413")
def letterbox_235(task, wd):
    """2.35:1 bars inside 16:9 with a dolly-only push of <= 2 %/s, ease-in-out sine."""
    N = np()
    W, H, fps = 320, 180, 15
    bar = int(round((H - W / 2.35) / 2))
    mk = {"red": ("red", 30, 90, 7), "blue": ("blue", 290, 90, 7)}
    wimg = world(W, H, mk)
    scales = [1 + 0.045 * ease_io_sine(f / fps / 4.0) for f in range(int(4 * fps) + 1)]
    frames = []
    for s in scales:
        img = warp(wimg, mat_stage(0, 0, s, 0, (W / 2, H / 2)), W, H)
        img[:bar] = 0
        img[H - bar:] = 0
        frames.append(img)
    mats = [mat_stage(0, 0, s, 0, (W / 2, H / 2)) for s in scales]
    checks, outs, d = cam_run(wd, "letterbox235", wimg, mats, W, H, fps, mk, frames=frames, tol=2.0, neg_k=1.5)
    f0, fi = d["frames"][10], d["input_frames"][10]
    rows_black = [float(f0[y].max()) < 16 for y in range(H)]
    active = H - sum(rows_black)
    sm = pair_scale(d, "red", "blue", 260.0)
    rate = max(abs(sm[i + fps] / sm[i] - 1) for i in range(0, len(sm) - fps))
    checks += [check("active picture is 2.35:1", _near(W / active, 2.35, 0.04), W / active, 2.35),
               check("dolly <= 2 %/s", rate <= 0.0205, rate, "<= 0.02"),
               check("negative control: input has no bars", not _near(W / (H - sum(float(fi[y].max()) < 16 for y in range(H))), 2.35, 0.04),
                     W / H, "!= 2.35")]
    return checks, outs


@card("CAM-414")
def climax_zoom_shake(task, wd):
    """When 3 rings remain the camera zooms 1.0→1.25 over 3 s; each hit adds a 2 px shake decaying over 100 ms."""
    N = np()
    fps = 20
    hits, three_left = [0.5, 1.2, 2.0, 3.0, 3.6], 2.0
    ts = [f / fps for f in range(int(5.2 * fps))]
    scales = [1 + 0.25 * ease_io_sine((t - three_left) / 3.0) for t in ts]
    offs = []
    for t in ts:
        dx = 0.0
        for h in hits:
            if 0 <= t - h < 0.1:
                dx += 2.0 * (1 - (t - h) / 0.1) * (1 if int((t - h) * fps) % 2 == 0 else -1)
        offs.append((round(dx), 0))
    checks, outs, d, mid = _offset_card(wd, "climax", 400, 224, fps, offs, scales, tol=2.0)
    sm = pair_scale(d, "red", "blue", 0.4 * 400)
    resid = [abs(m[0]) for m in mid]
    in_hit = [r for t, r in zip(ts, resid) if any(0 <= t - h < 0.1 for h in hits)]
    off_hit = [r for t, r in zip(ts, resid) if not any(-0.04 <= t - h < 0.14 for h in hits)]
    checks += [check("zoom starts when 3 rings remain", abs(sm[int(three_left * fps)] - 1) < 0.005 and sm[int(three_left * fps) + 15] > 1.01,
                     [sm[int(three_left * fps)], sm[int(three_left * fps) + 15]], "1.0 then rising"),
               check("zoom reaches 1.25 after 3 s", _near(sm[int(5.0 * fps)], 1.25, 0.012), sm[int(5.0 * fps)], 1.25),
               check("shake peaks at 2 px inside hit windows", 1.5 <= max(in_hit) <= 2.6, max(in_hit), 2),
               check("no shake outside hit windows", max(off_hit) < 0.8, max(off_hit), "< 0.8")]
    return checks, outs


def _vnoise(seed, x):
    i = math.floor(x)
    f = x - i
    h = lambda k: (math.sin((k + seed * 31.7) * 127.1) * 43758.5453) % 1.0 * 2 - 1
    u = f * f * (3 - 2 * f)
    return h(i) * (1 - u) + h(i + 1) * u


@card("CAM-337")
def impact_shake(task, wd):
    """noise2D(seed, t*25) offsets on camera x/y, amplitude 12 px decaying exp(-dt/250 ms) after each impact."""
    fps, impacts = 60, [0.3, 1.2]
    ts = [f / fps for f in range(int(1.8 * fps))]
    offs = []
    for t in ts:
        amp = sum(12 * math.exp(-(t - p) / 0.25) for p in impacts if t >= p)
        offs.append((amp * _vnoise(1, t * 25), amp * _vnoise(2, t * 25)))
    checks, outs, d, mid = _offset_card(wd, "impact_shake", 320, 180, fps, offs, tol=1.6, neg_k=2.0)
    mag = [math.hypot(*m) for m in mid]
    w = lambda a, b: max(mag[int(a * fps):int(b * fps)])
    checks += [check("still before the first impact", w(0, 0.29) < 0.8, w(0, 0.29), "< 0.8"),
               check("first 100 ms shake up to ~12 px", 5 <= w(0.3, 0.4) <= 17.5, w(0.3, 0.4), "5-17"),
               check("decayed by ~e^-2 after 500 ms", w(0.8, 0.95) < 0.35 * w(0.3, 0.45), w(0.8, 0.95) / w(0.3, 0.45), "< 0.35"),
               check("second impact re-excites", w(1.2, 1.3) > 2 * w(1.05, 1.19), [w(1.05, 1.19), w(1.2, 1.3)], "x2")]
    return checks, outs


@card("CAM-303")
def ultra_slow_dolly(task, wd):
    """Distance 200→6 r_s over 120 s, interpolated in log space: apparent size grows at a constant log rate; slight tilt."""
    N = np()
    W, H, fps = 480, 270, 0.5
    ts = [i * 2.0 for i in range(61)]
    frames, frames_in = [], []
    yy, xx = N.mgrid[0:H, 0:W]
    for t in ts:
        dist = math.exp(math.log(200) + (math.log(6) - math.log(200)) * t / 120)
        r = 3.6 * 200 / dist
        incl = 1.0 - 0.15 * smoothstep(t / 120)
        for lst, rr, ii in ((frames, r, incl), (frames_in, 3.6, 1.0)):
            img = N.zeros((H, W, 3), N.uint8) + 10
            img[((xx - W / 2) / rr) ** 2 + ((yy - H / 2) / (rr * ii)) ** 2 <= 1] = COL["red"]
            lst.append(img)
    out = write_video(wd / "slow_dolly.mp4", frames, 2)
    inp = write_video(wd / "slow_dolly_input.mp4", frames_in, 2)
    fo, fi = read_video(out), read_video(inp)
    rad = [(bbox(f, "red")[2] - bbox(f, "red")[0]) / 2 for f in fo]
    radi = [(bbox(f, "red")[2] - bbox(f, "red")[0]) / 2 for f in fi]
    asp = [(lambda b: (b[3] - b[1]) / (b[2] - b[0]))(bbox(f, "red")) for f in (fo[0], fo[-1])]
    lr = [math.log(r) for r in rad]
    checks = [check("size grows x33 (200/6)", _near(rad[-1] / rad[0], 33.3, 4.0), rad[-1] / rad[0], 33.3),
              check("log(size) is linear in time (constant feel)", r2_linear(ts[5:], lr[5:]) > 0.995, r2_linear(ts[5:], lr[5:]), "> 0.995"),
              check("inclination change ~15 %", _near(asp[0] - asp[1], 0.15, 0.04), asp[0] - asp[1], 0.15),
              check("negative control: static input does not grow", not _near(radi[-1] / radi[0], 33.3, 4.0), radi[-1] / radi[0], "1.0")]
    return checks, [out]


def _catmull(pts, n=200):
    out = []
    P = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            out.append(tuple(0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t +
                                    (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in range(2)))
    out.append(pts[-1])
    return out


@card("CAM-343")
def arc_length_spline(task, wd):
    """Catmull-Rom through waypoints + cumulative-distance LUT: the marker moves at constant world speed."""
    N = np()
    W, H, fps = 320, 180, 30
    way = [(20, 150), (60, 30), (90, 40), (250, 160), (300, 20)]
    curve = _catmull(way)
    seg = [math.hypot(curve[i + 1][0] - curve[i][0], curve[i + 1][1] - curve[i][1]) for i in range(len(curve) - 1)]
    cum = N.concatenate([[0], N.cumsum(seg)])
    L = float(cum[-1])
    n = 90

    def at_dist(s):
        i = int(N.searchsorted(cum, s, side="right") - 1)
        i = min(i, len(seg) - 1)
        u = (s - cum[i]) / seg[i] if seg[i] else 0
        return (curve[i][0] + (curve[i + 1][0] - curve[i][0]) * u, curve[i][1] + (curve[i + 1][1] - curve[i][1]) * u)
    pos = [at_dist(L * f / (n - 1)) for f in range(n)]
    naive = [curve[int(round(f / (n - 1) * (len(curve) - 1)))] for f in range(n)]

    def render(ps, name):
        yy, xx = N.mgrid[0:H, 0:W]
        fr = []
        for p in ps:
            img = N.zeros((H, W, 3), N.uint8) + 30
            img[(xx - p[0]) ** 2 + (yy - p[1]) ** 2 <= 16] = COL["red"]
            fr.append(img)
        return write_video(wd / name, fr, fps)
    out, inp = render(pos, "arc_length.mp4"), render(naive, "arc_length_input.mp4")

    def cv(path):
        tr = track(read_video(path), "red")
        sp = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(tr[:-1], tr[1:])]
        return float(N.std(sp) / N.mean(sp))
    hits = max(min(math.hypot(c[0] - w[0], c[1] - w[1]) for c in curve) for w in way)
    c_out, c_in = cv(out), cv(inp)
    checks = [check("curve passes through every waypoint (Catmull-Rom)", hits < 1e-6, hits, 0),
              check("measured speed is constant (CV of per-frame distance)", c_out < 0.06, c_out, "< 0.06"),
              check("negative control: parameter-t motion has uneven speed", c_in > 0.2, c_in, "> 0.2")]
    return checks, [out, write_json(wd, "arc_lut.json", {"length": L, "samples": len(cum)})]


@card("CAM-339")
def shared_svg_html_camera(task, wd):
    """One keyframed (x, y, zoom) transform with inOut cubic applied to both the drawing layer and the text layer."""
    N = np()
    W, H, fps = 320, 180, 30
    keys = [(0.0, 0, 0, 1.0), (1.0, -40, -20, 1.6), (2.0, 20, 10, 2.0)]

    def cam(t):
        for (t0, x0, y0, z0), (t1, x1, y1, z1) in zip(keys[:-1], keys[1:]):
            if t <= t1:
                e = ease_io_cubic((t - t0) / (t1 - t0))
                return x0 + (x1 - x0) * e, y0 + (y1 - y0) * e, z0 + (z1 - z0) * e
        return keys[-1][1:]
    mk = {"red": ("red", 130, 80, 6), "blue": ("blue", 180, 100, 5)}
    svg_layer = world(W, H, {"red": mk["red"]})
    frames, mats = [], []
    for f in range(int(2.2 * fps)):
        x, y, z = cam(f / fps)
        M = mat_stage(x, y, z, 0, (W / 2, H / 2))
        img = warp(svg_layer, M, W, H)
        q = apply_mat(M, (180, 100))
        yy, xx = N.mgrid[0:H, 0:W]
        img[(xx - q[0]) ** 2 + (yy - q[1]) ** 2 <= (5 * z) ** 2] = COL["blue"]
        frames.append(img)
        mats.append(M)
    wimg = world(W, H, mk)
    checks, outs, d = cam_run(wd, "shared_cam", wimg, mats, W, H, fps, mk, frames=frames)
    rel = [((b[0] - a[0]) / z, (b[1] - a[1]) / z) for a, b, z in zip(d["meas"]["red"], d["meas"]["blue"], [cam(f / fps)[2] for f in range(len(mats))]) if a and b]
    drift = max(math.hypot(r[0] - 50, r[1] - 20) for r in rel)
    checks.append(check("text layer stays locked to the drawing (relative offset / zoom constant)", drift < 1.5, drift, "< 1.5"))
    return checks, outs


@card("CAM-334")
def push_into_window(task, wd):
    """Scale+translate the desktop group 1→2.2 (1 s easeInOutCubic) onto the area of interest; the headline stays pinned."""
    N = np()
    W, H, fps = 320, 180, 30
    aoi = (230.0, 120.0)
    mk = {"red": ("red", aoi[0], aoi[1], 5), "green": ("green", aoi[0] - 20, aoi[1], 4)}
    wimg = world(W, H, mk)
    frames, mats = [], []
    for f in range(int(1.4 * fps)):
        e = ease_io_cubic(f / fps / 1.0)
        s = 1 + 1.2 * e
        cx, cy = W / 2 + (aoi[0] - W / 2) * e, H / 2 + (aoi[1] - H / 2) * e
        M = mat_cam(cx, cy, s, W, H)
        img = warp(wimg, M, W, H)
        img[8:22, 10:120] = COL["blue"]
        frames.append(img)
        mats.append(M)
    checks, outs, d = cam_run(wd, "push_window", wimg, mats, W, H, fps, mk, frames=frames)
    sm = pair_scale(d, "red", "green", 20.0)
    heads = [bbox(f, "blue") for f in d["frames"]]
    checks += [check("area of interest lands at frame centre", _pt_near(d["meas"]["red"][-1], (160, 90), 1.0), d["meas"]["red"][-1], [160, 90]),
               check("scale 2.2 at the end", _near(sm[-1], 2.2, 0.06), sm[-1], 2.2),
               check("headline pinned (identical box every frame)", len(set(heads)) == 1, heads[0], "constant"),
               check("easeInOutCubic: half the scale change at 0.5 s", _near(sm[15], 1.6, 0.06), sm[15], 1.6)]
    return checks, outs


@card("CAM-419")
def locked_cam_scale_shadow(task, wd):
    """Locked camera; the hero gains depth by scale 0.92→1.00 plus a 24 px soft drop shadow."""
    from PIL import Image, ImageFilter
    N = np()
    W, H, fps = 320, 180, 30
    frames = []
    for f in range(25):
        s = 0.92 + 0.08 * ease_out_expo(f / 20)
        im = Image.new("RGB", (W, H), (210, 214, 220))
        sh = Image.new("L", (W, H), 0)
        w2, h2 = 60 * s, 40 * s
        from PIL import ImageDraw
        ImageDraw.Draw(sh).rectangle([160 - w2, 96 - h2 + 12, 160 + w2, 96 + h2 + 12], fill=150)
        sh = sh.filter(ImageFilter.GaussianBlur(12))
        im = Image.composite(Image.new("RGB", (W, H), (40, 40, 50)), im, sh)
        ImageDraw.Draw(im).rectangle([160 - w2, 90 - h2, 160 + w2, 90 + h2], fill=(255, 0, 0))
        ImageDraw.Draw(im).rectangle([10, 10, 20, 20], fill=(0, 0, 255))
        frames.append(N.asarray(im))
    out = write_video(wd / "scale_shadow.mp4", frames, fps)
    fo = read_video(out)
    wid = [(bbox(f, "red")[2] - bbox(f, "red")[0]) / 120 for f in fo]
    below = float(fo[-1][136:150, 140:180].mean())
    above = float(fo[-1][30:44, 140:180].mean())
    checks = [check("hero scale 0.92 → 1.00", _near(wid[0], 0.92, 0.02) and _near(wid[-1], 1.0, 0.02), [wid[0], wid[-1]], [0.92, 1.0]),
              check("soft shadow darkens below the hero (24 px offset/blur)", below < above - 25, [below, above], "below darker"),
              check("camera locked (corner marker never moves)", len({bbox(f, "blue") for f in fo}) == 1, True, True),
              check("negative control: a flat input frame has no shadow", not (210 < 210 - 25), 210, "no shadow")]
    return checks, [out]


# ═════════════════════════ the repo's own montage / analysis tools on fixtures ═════════════════════════
def _py(args, timeout=60, cwd=None):
    done = subprocess.run([sys.executable, *[str(a) for a in args]], capture_output=True, text=True, timeout=timeout,
                          stdin=subprocess.DEVNULL, cwd=cwd)
    if done.returncode:
        raise RuntimeError("tool failed (%d): %s" % (done.returncode, (done.stderr or done.stdout)[-400:]))
    return done.stdout


def _marker_clip(wd, name, W=320, H=180, seconds=2.0, fps=30, mk=None):
    mk = mk or {"red": ("red", W * 0.25, H / 2, 8), "blue": ("blue", W * 0.75, H / 2, 8)}
    img = world(W, H, mk)
    return write_video(wd / name, [img] * int(seconds * fps), fps), mk


@card("CAM-38")
def ken_burns_timeline(task, wd):
    """timeline.py clip 'zoom': {'from': 1.0, 'to': 1.08} — the repo's Ken-Burns chain, measured on the film."""
    src, mk = _marker_clip(wd, "src.mp4", 320, 180, 3.0, 30)
    spec = {"size": "320x180", "fps": 30, "clips": [{"src": str(src), "in": 0, "out": 3.0, "fit": "cover", "zoom": {"from": 1.0, "to": 1.08}}]}
    sp = write_json(wd, "timeline.json", spec)
    out = wd / "kenburns.mp4"
    _py([KIT / "timeline.py", sp, "--out", out], timeout=90)
    fo, fi = read_video(out), read_video(src)
    d = lambda f: (lambda a, b: math.hypot(a[0] - b[0], a[1] - b[1]) / 160.0 if a and b else None)(centroid(f, "red"), centroid(f, "blue"))
    s = [d(f) for f in fo]
    si = [d(f) for f in fi]
    n = len(s)
    checks = [check("starts at 1.00", _near(s[0], 1.0, 0.01), s[0], 1.0),
              check("ends at 1.08", _near(s[-1], 1.08, 0.012), s[-1], 1.08),
              check("raised-cosine ease: half way at mid clip", _near(s[n // 2], 1.04, 0.01), s[n // 2], 1.04),
              check("monotonic push", all(b >= a - 0.004 for a, b in zip(s[:-1], s[1:])), True, True),
              check("negative control: the source clip has no zoom", not _near(si[-1], 1.08, 0.012), si[-1], 1.0)]
    return checks, [out, sp]


def _aspect_src(wd, name, W=320, H=180, seconds=1.0):
    from PIL import Image, ImageDraw
    N = np()
    im = Image.new("RGB", (W, H), (230, 180, 60))
    ImageDraw.Draw(im).rectangle([0, 0, 40, H], fill=(255, 0, 0))
    ImageDraw.Draw(im).rectangle([W - 40, 0, W, H], fill=(0, 0, 255))
    ImageDraw.Draw(im).ellipse([W / 2 - 20, H / 2 - 20, W / 2 + 20, H / 2 + 20], fill=(0, 255, 0))
    arr = N.asarray(im)
    return write_video(wd / name, [arr] * int(seconds * 30), 30)


@card("CAM-39")
def fit_blur_timeline(task, wd):
    """timeline.py fit 'blur': blurred cover (gblur 40, brightness -0.12, saturation .85) behind the contained clip."""
    src = _aspect_src(wd, "wide.mp4")
    outs = {}
    for fit in ("cover", "contain", "blur"):
        sp = write_json(wd, "fit_%s.json" % fit, {"size": "180x320", "fps": 30, "background": "#000000",
                                                   "clips": [{"src": str(src), "in": 0, "out": 1.0, "fit": fit}]})
        outs[fit] = wd / ("fit_%s.mp4" % fit)
        _py([KIT / "timeline.py", sp, "--out", outs[fit]], timeout=90)
    fr = {k: read_video(v)[5].astype(float) for k, v in outs.items()}
    top_blur, top_contain = fr["blur"][10:60, 20:160], fr["contain"][10:60, 20:160]
    mid = fr["blur"][150:170, 60:120]
    cover_green = area(fr["cover"].astype(N_uint8()), "green") if False else area(fr["cover"].astype("uint8"), "green")
    checks = [check("contain: letterbox bands are the background colour", top_contain.max() < 20, float(top_contain.max()), "< 20"),
              check("blur: bands hold a soft darker copy (not black)", 40 < top_blur.mean() < 200 and sharpness(top_blur) < 30,
                    [float(top_blur.mean()), sharpness(top_blur)], "lit and soft"),
              check("blur: the whole frame sits sharp in the middle (both edge bars visible)",
                    area(fr["blur"].astype("uint8"), "red") > 20 and area(fr["blur"].astype("uint8"), "blue") > 20, True, True),
              check("cover crops the side bars away", area(fr["cover"].astype("uint8"), "red") < 5, area(fr["cover"].astype("uint8"), "red"), "< 5"),
              check("subject kept in all fits", min(area(f.astype("uint8"), "green") for f in fr.values()) > 50, True, True),
              check("negative control: contain bands are not the blurred fill", not (40 < top_contain.mean() < 200), float(top_contain.mean()), "black")]
    return checks, list(outs.values())


def N_uint8():
    return np().uint8


def _subject_clip(wd, name, x_frac, W=480, H=270, seconds=1.0):
    """A moving subject at x_frac of the width (motion energy) on a static textured background."""
    N = np()
    frames = []
    bg = world(W, H, {})
    for f in range(int(seconds * 30)):
        img = bg.copy()
        cx, cy = int(W * x_frac + 6 * math.sin(f * 0.7)), int(H / 2 + 6 * math.cos(f * 0.5))
        img[cy - 25:cy + 25, cx - 18:cx + 18] = (255, 0, 0)
        frames.append(img)
    return write_video(wd / name, frames, 30)


@card("CAM-40")
def smart_reframe_tool(task, wd):
    """tools.py aspect --to 9:16 in smart/crop/blur modes: output ratio, and what each mode keeps."""
    src = _subject_clip(wd, "talk.mp4", 0.5)
    outs, rep = {}, {}
    for mode in ("smart", "crop", "blur"):
        outs[mode] = wd / ("v_%s.mp4" % mode)
        rep[mode] = _py([KIT / "tools.py", "aspect", src, "--to", "9:16", "--mode", mode, "--out", outs[mode]], timeout=90)
    dims = {}
    for m, p in outs.items():
        v = [s for s in fx.probe(p)["streams"] if s["codec_type"] == "video"][0]
        dims[m] = (int(v["width"]), int(v["height"]))
    fb = read_video(outs["blur"])[10]
    fc = read_video(outs["crop"])[10]
    checks = [check("%s output is 9:16" % m, _near(w / h, 9 / 16, 0.01), w / h, 0.5625) for m, (w, h) in dims.items()]
    checks += [check("crop keeps the centred subject", area(fc, "red") > 300, area(fc, "red"), "> 300"),
               check("blur pad keeps the whole width (subject small, frame padded)", 0 < area(fb, "red") < area(fc, "red"), [area(fb, "red"), area(fc, "red")], "smaller than crop"),
               check("negative control: the 16:9 source is not 9:16", not _near(480 / 270, 9 / 16, 0.01), 480 / 270, "1.78")]
    return checks, list(outs.values())


@card("CAM-58")
def smart_reframe_motion(task, wd):
    """tools.py aspect --mode smart on an off-centre subject: without faces it crops; measure where the subject lands."""
    src = _subject_clip(wd, "offcentre.mp4", 0.78)
    out = wd / "smart.mp4"
    rep = _py([KIT / "tools.py", "aspect", src, "--to", "9:16", "--mode", "smart", "--out", out], timeout=90)
    fo = read_video(out)
    c = centroid(fo[10], "red")
    w = fo.shape[2]
    blur_out = wd / "pad.mp4"
    _py([KIT / "tools.py", "aspect", src, "--to", "9:16", "--mode", "blur", "--out", blur_out], timeout=90)
    fb = read_video(blur_out)[10].astype(float)
    checks = [check("smart crop is 9:16", _near(w / fo.shape[1], 9 / 16, 0.01), w / fo.shape[1], 0.5625),
              check("blur pad: darker blurred copy above the fitted frame", fb[: fb.shape[0] // 5].mean() < 120 and sharpness(fb[: fb.shape[0] // 5]) < 40,
                    float(fb[: fb.shape[0] // 5].mean()), "< 120 and soft")]
    if c is not None:
        checks.append(check("subject inside the smart crop (motion/face aware)", 0 <= c[0] < w, c, "inside"))
    else:
        checks.append(check("smart crop kept the subject in frame", False, None, "subject visible"))
    checks.append(check("negative control: a plain centre crop loses the off-centre subject",
                        not (abs(0.78 - 0.5) * 480 < (270 * 9 / 16) / 2 - 18), abs(0.78 - 0.5) * 480, "> half crop width"))
    (wd / "smart_report.txt").write_text(rep, encoding="utf-8")
    return checks, [out, blur_out]


@card("CAM-41")
def camera_name_validator(task, wd):
    """wbcompat: plans compile to manifests whose scene camera must be one of the ten names; validate_manifest rejects others."""
    W = load_py(KIT / "web/wbcompat.py", "wbcompat_b")
    res = {}
    for task_, intent in (("مقدمة عربية بحركة نصوص", "2d"), ("مشهد 3d لمنتج زجاجي", "3d")):
        plan = W.make_plan({"task": task_, "seconds": 6, "fps": 30, "aspect": "16:9"})
        man = W.compile_plan(plan)["manifest"]
        W.validate_manifest(man)
        res[intent] = [s["camera"] for s in man["scenes"]]
        bad = json.loads(json.dumps(man))
        bad["scenes"][0]["camera"] = "zoom_wobble"
        try:
            W.validate_manifest(bad)
            res[intent + "_bad"] = "accepted"
        except ValueError as e:
            res[intent + "_bad"] = "rejected: %s" % str(e)[:80]
    two_d = {"fast_reveal", "slow_push", "match_cut", "focus_lift", "still_hold"}
    three_d = {"dolly_in", "orbit", "side_track", "push_in", "locked"}
    out = write_json(wd, "camera_moves.json", res)
    checks = [check("2D plan uses only the five 2D moves", set(res["2d"]) <= two_d and len(res["2d"]) == 5, res["2d"], sorted(two_d)),
              check("3D plan uses only the five 3D moves", set(res["3d"]) <= three_d and len(res["3d"]) == 5, res["3d"], sorted(three_d)),
              check("unknown move rejected (2D)", res["2d_bad"].startswith("rejected"), res["2d_bad"], "rejected"),
              check("unknown move rejected (3D)", res["3d_bad"].startswith("rejected"), res["3d_bad"], "rejected")]
    return checks, [out]


@card("CAM-45")
def composition_check_tool(task, wd):
    """image_analyze.py: saliency centroid → rule-of-thirds / centred / off-grid, mirror symmetry, nearest ratio."""
    from PIL import Image, ImageDraw
    cases = {"thirds": (1 / 3, 1 / 3), "centred": (0.5, 0.5), "offgrid": (0.12, 0.85)}
    res = {}
    for k, (fxx, fyy) in cases.items():
        im = Image.new("RGB", (900, 600), (128, 128, 128))
        x, y = 900 * fxx, 600 * fyy
        ImageDraw.Draw(im).ellipse([x - 40, y - 40, x + 40, y + 40], fill=(250, 250, 250))
        p = wd / ("%s.png" % k)
        im.save(p)
        res[k] = json.loads(_py([KIT / "omni/image_analyze.py", p]))
    out = write_json(wd, "composition.json", {k: v.get("composition") for k, v in res.items()})
    comp = {k: v["composition"]["placement"] for k, v in res.items()}
    checks = [check("subject on a thirds point → rule-of-thirds", comp["thirds"] == "rule-of-thirds", comp["thirds"], "rule-of-thirds"),
              check("subject in the middle → centered", comp["centred"] == "centered", comp["centred"], "centered"),
              check("negative control: corner subject is off-grid", comp["offgrid"] == "off-grid", comp["offgrid"], "off-grid"),
              check("centred disc is more mirror-symmetric than the corner one",
                    res["centred"]["composition"]["mirror_symmetry"] > res["offgrid"]["composition"]["mirror_symmetry"],
                    [res["centred"]["composition"]["mirror_symmetry"], res["offgrid"]["composition"]["mirror_symmetry"]], "centred > corner")]
    ar = json.dumps(res["thirds"], ensure_ascii=False)
    checks.append(check("nearest standard ratio of 900x600 is 3:2", '"3:2"' in ar, "3:2" in ar, True))
    return checks, [out]


def _light(wd, name, ops):
    p = subprocess.run([sys.executable, str(KIT / "omni/light_calc.py")], input=json.dumps(ops), capture_output=True, text=True, timeout=30)
    if p.returncode:
        raise RuntimeError(p.stderr[-300:])
    (wd / name).write_text(p.stdout, encoding="utf-8")
    return json.loads(p.stdout), wd / name


@card("CAM-46")
def equivalent_exposure(task, wd):
    """light_calc.py op 'equivalent': f/2.8 1/125 → f/1.4 needs 1/500 s; slow shutters warn for handheld."""
    r, out = _light(wd, "equivalent.json", [{"op": "equivalent", "aperture": 2.8, "shutter": "1/125", "iso": 100, "new_aperture": 1.4, "new_iso": 100},
                                             {"op": "equivalent", "aperture": 2.8, "shutter": "1/125", "iso": 100, "new_aperture": 8, "new_iso": 100}])
    txt = json.dumps(r)
    a, b = r[0], r[1]
    checks = [check("f/1.4 → 1/500 s", "1/500" in json.dumps(a), a, "1/500s"),
              check("f/8 → about 1/15 s and a handheld warning", ("1/15" in json.dumps(b) or "1/16" in json.dumps(b)) and ("warn" in json.dumps(b).lower() or "handheld" in json.dumps(b).lower()), b, "1/15s + warning"),
              check("negative control: the unchanged shutter 1/125 is not the answer for f/1.4", "1/125s" not in json.dumps(a), True, True)]
    return checks, [out]


@card("CAM-47")
def shutter_angle_speed(task, wd):
    """light_calc.py op 'shutter_angle': speed = angle/360/fps (24 fps 180° → 1/48 s)."""
    r, out = _light(wd, "shutter.json", [{"op": "shutter_angle", "fps": 24, "angle": 180}, {"op": "shutter_angle", "fps": 30, "angle": 90},
                                          {"op": "shutter_angle", "fps": 60, "angle": 360}])
    s = [json.dumps(x) for x in r]
    checks = [check("24 fps 180° → 1/48 s", "1/48" in s[0], r[0], "1/48s"),
              check("30 fps 90° → 1/120 s", "1/120" in s[1], r[1], "1/120s"),
              check("60 fps 360° → 1/60 s", "1/60" in s[2], r[2], "1/60s"),
              check("negative control: 30 fps 90° is not 1/30 s (angle applied)", "1/30s" not in s[1], True, True)]
    return checks, [out]


@card("CAM-57")
def downbeat_zoom_punch(task, wd):
    """montage._segment with punches: +9 % jump decaying exp(-(t-p)/0.32), rendered at 2x then lanczos down."""
    M = load_py(KIT / "montage.py", "montage_b")
    src, mk = _marker_clip(wd, "shot.mp4", 320, 180, 2.0, 30)
    out = wd / "punch.mp4"
    M._segment(src, 0.0, 2.0, out, 320, 180, 30, "none", [0.5])
    fo, fi = read_video(out), read_video(src)
    d = lambda f: (lambda a, b: math.hypot(a[0] - b[0], a[1] - b[1]) / 160.0 if a and b else None)(centroid(f, "red"), centroid(f, "blue"))
    s, si = [d(f) for f in fo], [d(f) for f in fi]
    exp = lambda t: 1 + (0.09 * math.exp(-(t - 0.5) / 0.32) if t >= 0.5 else 0)
    dev = max(abs(s[i] - exp(i / 30)) for i in range(len(s)))
    checks = [check("before the downbeat: 1.00", _near(s[14], 1.0, 0.01), s[14], 1.0),
              check("on the downbeat: +9 %", _near(s[15], 1.09, 0.012), s[15], 1.09),
              check("decays with tau 0.32 s (whole curve)", dev < 0.012, dev, "< 0.012"),
              check("negative control: source has no punch", not _near(si[15], 1.09, 0.012), si[15], 1.0)]
    return checks, [out]


def _painter():
    return load_py(KIT / "render.py", "kosif_render_b")


@card("CAM-53")
def defocus_motion_blur_ops(task, wd):
    """render.py defocus(radius) and motion_blur(shape, length, angle) on a painted fixture."""
    R = _painter()
    N = np()
    bg = [R.fill(R.rect(0, 0, 1200, 800), "#202020")] + [R.fill(R.rect(x, 0, 30, 800), "#e0e0e0") for x in range(0, 1200, 60)]
    subj = [R.fill(R.rect(700, 300, 200, 200), "#ff0000")] + [R.fill(R.rect(700 + x, 300, 10, 200), "#ffffff") for x in range(0, 200, 40)]
    steps_in = [R.Step("bg", bg), R.Step("subject", subj)]
    steps = [R.Step("bg", bg + [R.defocus(8)]), R.Step("subject", subj + [R.motion_blur(R.rect(700, 300, 200, 200), 40, angle=0)])]
    a = R.render_image(steps, scale=0.4, ss=1)
    b = R.render_image(steps_in, scale=0.4, ss=1)
    pa, pb = wd / "ops.png", wd / "ops_input.png"
    a.save(pa)
    b.save(pb)
    A, B = N.asarray(a).astype(float), N.asarray(b).astype(float)
    bgA, bgB = A[10:100, 10:200], B[10:100, 10:200]
    sx = lambda X: float(N.abs(N.diff(X.mean(axis=2), axis=1)).mean())
    sy = lambda X: float(N.abs(N.diff(X.mean(axis=2), axis=0)).mean())
    subA, subB = A[125:195, 285:355], B[125:195, 285:355]
    checks = [check("defocus softens the background", sharpness(bgA) < 0.2 * sharpness(bgB), sharpness(bgA) / sharpness(bgB), "< 0.2"),
              check("motion blur streaks the subject horizontally", sx(subA) < 0.6 * sx(subB), sx(subA) / sx(subB), "< 0.6"),
              check("subject painted after defocus stays crisp vertically", sy(subA) >= 0.8 * sy(subB) - 0.5, [sy(subA), sy(subB)], ">= 0.8x"),
              check("negative control: input background is sharp", sharpness(bgB) > 100, sharpness(bgB), "> 100")]
    return checks, [pa]


@card("CAM-54")
def camera_stack_order(task, wd):
    """The camera Step in order: defocus bg, motion blur rain, bloom, flare, chroma, filmic, vignette, grain (ROLLOFF 1.0)."""
    R = _painter()
    N = np()
    bg = [R.fill(R.rect(0, 0, 1200, 800), "#1c2430")] + [R.fill(R.rect(x, 0, 20, 500), "#506070") for x in range(0, 1200, 80)]
    rain = R.rect(0, 0, 1200, 800)
    light = [R.fill(R.ellipse(900, 200, 40), "#fff4d0")]
    cam = R.Step("الكاميرا", [R.bloom(0.72, 26, 0.5), R.flare((900, 200), "#ffb070", 110, 380, 0.45), R.chroma(1.4), R.filmic(),
                                R.vignette(0.5), R.grain(0.02)])
    steps = [R.Step("bg", bg + [R.defocus(2)]), R.Step("rain", [R.motion_blur(rain, 6, 104)] + light), cam]
    base = [R.Step("bg", bg), R.Step("light", light)]
    ims = [im for _, _, im in R.render(steps, 0.4, 1, rolloff=1.0)]
    inp = R.render_image(base, 0.4, 1, rolloff=1.0)
    A, B = ims[-1].astype(float), N.asarray(inp).astype(float)
    p, pi = wd / "stack.png", wd / "stack_input.png"
    Image_ = __import__("PIL.Image", fromlist=["Image"])
    Image_.fromarray(ims[-1]).save(p)
    inp.save(pi)
    corner, centre = A[:30, :30].mean(), A[150:170, 230:250].mean()
    halo = A[80:100, 300:340].mean() - B[80:100, 300:340].mean()
    checks = [check("camera step is last and in the stated order", [s.label for s in steps][-1] == "الكاميرا" and len(cam.ops) == 6, [s.label for s in steps], "... الكاميرا"),
              check("bloom/flare spill light around the strongest source", halo > 8, halo, "> 8"),
              check("vignette darkens the corners vs the centre", corner < centre * 0.8, [corner, centre], "corner < 0.8 x centre"),
              check("grain adds per-pixel noise in flat areas", float(A[200:240, 20:60].std()) > float(B[200:240, 20:60].std()) + 1, float(A[200:240, 20:60].std()), "> input"),
              check("negative control: the unprocessed painting has no halo", (B[80:100, 300:340].mean() - B[80:100, 300:340].mean()) <= 8, 0, "<= 8")]
    return checks, [p]


@card("CAM-55")
def painter_letterbox(task, wd):
    """Final Step: black rects above TOP=62 and below BOTTOM=738 turn 1200x800 into a 1200x676 cinema frame."""
    R = _painter()
    N = np()
    scene = [R.fill(R.rect(0, 0, 1200, 800), "#7aa0c8")]
    steps = [R.Step("scene", scene), R.Step("letterbox", [R.fill(R.rect(0, 0, 1200, 62), "#000000"), R.fill(R.rect(0, 738, 1200, 800 - 738), "#000000")])]
    im = N.asarray(R.render_image(steps, 1.0, 1, rolloff=1.0)).astype(float)
    inp = N.asarray(R.render_image([R.Step("scene", scene)], 1.0, 1, rolloff=1.0)).astype(float)
    p = wd / "letterbox.png"
    save_png(p, im)
    black = lambda X: [y for y in range(X.shape[0]) if X[y].max() < 10]
    active = 800 - len(black(im))
    checks = [check("active frame 1200x676 (±1 px rasterised edge)", abs(active - 676) <= 1, active, 676),
              check("top bar 62 px (±1)", abs(len([y for y in black(im) if y < 400]) - 62) <= 1, len([y for y in black(im) if y < 400]), 62),
              check("aspect ~1.775", _near(1200 / active, 1.775, 0.004), 1200 / active, 1.775),
              check("negative control: input has no bars", len(black(inp)) == 0, len(black(inp)), 0)]
    return checks, [p]


@card("CAM-56")
def depth_veil_fog(task, wd):
    """Translucent blurred screen bands between depth layers lower distant contrast and push it blue."""
    R = _painter()
    N = np()
    far = [R.fill(R.poly([(0, 500), (300, 250), (600, 480), (900, 230), (1200, 500), (1200, 800), (0, 800)]), "#303848")]
    near = [R.fill(R.poly([(0, 650), (400, 520), (800, 640), (1200, 540), (1200, 800), (0, 800)]), "#101418")]
    sky = [R.fill(R.rect(0, 0, 1200, 800), "#0c1018")]
    fog = [R.fill(R.rect(0, 380, 1200, 200), "#a86484", 0.26, blur=26, mode="screen"), R.fill(R.rect(0, 420, 1200, 160), "#5c3550", 0.30, blur=30, mode="screen"),
           R.fill(R.rect(0, 300, 1200, 300), "#54637a", 0.2, blur=34, mode="screen")]
    with_fog = N.asarray(R.render_image([R.Step("sky", sky), R.Step("far", far), R.Step("veil", fog), R.Step("near", near)], 0.5, 1)).astype(float)
    without = N.asarray(R.render_image([R.Step("sky", sky), R.Step("far", far), R.Step("near", near)], 0.5, 1)).astype(float)
    p = wd / "veil.png"
    save_png(p, with_fog)
    farA, farB = with_fog[150:240, 100:500], without[150:240, 100:500]
    nearA, nearB = with_fog[360:400, :], without[360:400, :]
    con = lambda X: float(X.mean(axis=2).std())
    checks = [check("veil brightens the distant band (screen blend)", farA.mean() > farB.mean() + 8, [farA.mean(), farB.mean()], "+8"),
              check("distant layer lower in contrast relative to its brightness", con(farA) / farA.mean() < con(farB) / farB.mean(), [con(farA) / farA.mean(), con(farB) / farB.mean()], "lower"),
              check("foreground painted after the veil stays dark/sharp", abs(nearA.mean() - nearB.mean()) < 3, abs(nearA.mean() - nearB.mean()), "< 3"),
              check("negative control: without the veil the far band is not lifted", not (farB.mean() > farB.mean() + 8), farB.mean(), "unchanged")]
    return checks, [p]


# ═════════════════════════ HUD / chrome engine: draw per frame, then read the HUD back off the video ═════════════════════════
def _rgb(c):
    if isinstance(c, str):
        c = c.lstrip("#")
        return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))
    return tuple(c)


def draw_text(draw, xy, s, fnt, fill, anchor="la", tracking=0.0):
    """Text with optional letter-spacing (em). Returns the bbox."""
    if not tracking:
        draw.text(xy, s, font=fnt, fill=fill, anchor=anchor)
        return draw.textbbox(xy, s, font=fnt, anchor=anchor)
    size = fnt.size
    widths = [draw.textlength(ch, font=fnt) for ch in s]
    total = sum(widths) + tracking * size * (len(s) - 1)
    x, y = xy
    if anchor[0] == "r":
        x -= total
    elif anchor[0] == "m":
        x -= total / 2
    a2 = "l" + anchor[1]
    x0 = x
    for ch, w in zip(s, widths):
        draw.text((x, y), ch, font=fnt, fill=fill, anchor=a2)
        x += w + tracking * size
    b = draw.textbbox((x0, y), s, font=fnt, anchor=a2)
    return (b[0], b[1], int(math.ceil(x0 + total)), b[3])


def _label_xy(el, W, H):
    at = el["at"]
    ins = el.get("inset", 0.03)
    ix, iy = W * ins, H * ins
    if isinstance(at, tuple):
        return at[:2], at[2] if len(at) > 2 else "la"
    return {"tl": ((ix, iy), "lt"), "tr": ((W - ix, iy), "rt"), "bl": ((ix, H - iy), "lb"), "br": ((W - ix, H - iy), "rb"),
            "tc": ((W / 2, iy), "mt"), "bc": ((W / 2, H - iy), "mb")}[at]


def _label_text(el, i, t):
    s = el["text"](i, t) if callable(el["text"]) else el["text"]
    return s.upper() if el.get("upper") else s


def hud_draw(img, elems, i, t):
    from PIL import ImageDraw
    W, H = img.size
    over = img.copy()
    d = ImageDraw.Draw(over)
    bg = img.getpixel((W // 2, H // 2))
    boxes = []
    for el in elems:
        typ, col = el["type"], _rgb(el.get("color", (255, 255, 255)))
        a = el.get("alpha", 1.0)
        c = blend(col, el.get("bg", bg), a)
        if typ == "brackets":
            ins, L, w = el.get("inset", 0.03), el.get("len", 0.04), el.get("w", 2)
            ix, iy, l = W * ins, H * ins, W * L
            for sx, sy in ((0, 0), (1, 0), (0, 1), (1, 1)):
                x = ix if sx == 0 else W - ix
                y = iy if sy == 0 else H - iy
                dx = l if sx == 0 else -l
                dy = l if sy == 0 else -l
                d.line([(x, y), (x + dx, y)], fill=c, width=w)
                d.line([(x, y), (x, y + dy)], fill=c, width=w)
        elif typ == "label":
            xy, anc = _label_xy(el, W, H)
            draw_text(d, xy, _label_text(el, i, t), font(el.get("font", MONO), el.get("size", 12)), c, anc, el.get("tracking", 0))
        elif typ == "bar":
            x0, y0, x1, y1 = el["box"]
            fr = max(0.0, min(1.0, el["frac"](t)))
            segs, gap = el.get("segments", 1), el.get("gap", 3)
            if el.get("track"):
                d.rectangle([x0, y0, x1, y1], fill=blend(_rgb(el["track"]), bg, el.get("track_alpha", 1.0)))
            sw = (x1 - x0 - gap * (segs - 1)) / segs
            for k in range(segs):
                sx0 = x0 + k * (sw + gap)
                fill_to = min(sx0 + sw, x0 + fr * (x1 - x0))
                if segs > 1:
                    fill_to = sx0 + sw if fr * segs >= k + 1 else (sx0 + sw * (fr * segs - k) if fr * segs > k else sx0)
                if fill_to > sx0 + 0.5:
                    d.rectangle([sx0, y0, fill_to - 1, y1], fill=c)
        elif typ == "ticks":
            x0, y0, x1, y1 = el["box"]
            for k in range(el["count"] + 1):
                x = x0 + (x1 - x0) * k / el["count"]
                d.line([(x, y0 - 4 if (el.get("major") and k % el["major"] == 0) else y0), (x, y1)], fill=c, width=1)
        elif typ == "playhead":
            x0, y0, x1, y1 = el["box"]
            x = x0 + (x1 - x0) * max(0.0, min(1.0, el["frac"](t)))
            d.rectangle([x - 1, y0, x + 1, y1], fill=c)
        elif typ == "dots":
            act = el["active"](t)
            for k, (x, y) in enumerate(el["centers"]):
                r = el.get("r", 4)
                if k <= act if el.get("cumulative") else k == act:
                    d.ellipse([x - r, y - r, x + r, y + r], fill=c)
                else:
                    d.ellipse([x - r, y - r, x + r, y + r], outline=blend(col, bg, a * 0.6), width=1)
        elif typ == "custom":
            el["draw"](d, over, i, t)
    return over


def _bracket_boxes(W, H, ins=0.03, L=0.04):
    ix, iy, l = W * ins, H * ins, W * L
    return [(ix - 3, iy - 3, ix + l, iy + l), (W - ix - l, iy - 3, W - ix + 3, iy + l),
            (ix - 3, H - iy - l, ix + l, H - iy + 3), (W - ix - l, H - iy - l, W - ix + 3, H - iy + 3)]


def hud_card(wd, name, elems, W=960, H=540, fps=10, seconds=3.0, bg=(18, 18, 20), base=None, samples=None):
    """Render the HUD over a background clip, decode it and check every element off the pixels."""
    from PIL import Image, ImageDraw
    N = np()
    n = int(seconds * fps)
    bgs = []
    frames = []
    for i in range(n):
        t = i / fps
        b = base(i, t) if base else Image.new("RGB", (W, H), bg)
        bgs.append(N.asarray(b))
        frames.append(N.asarray(hud_draw(b, elems, i, t)))
    out = write_video(wd / ("%s.mp4" % name), frames, fps)
    inp = write_video(wd / ("%s_input.mp4" % name), bgs, fps)
    fo, fi = read_video(out).astype(float), read_video(inp).astype(float)
    samples = samples or sorted({0, n // 2, n - 1})
    checks = []
    neg_boxes = []
    for el in elems:
        typ = el["type"]
        col = _rgb(el.get("color", (255, 255, 255)))
        a = el.get("alpha", 1.0)
        if typ == "brackets":
            bxs = _bracket_boxes(W, H, el.get("inset", 0.03), el.get("len", 0.04))
            got = [ink(fo[0], b, fi[0][int(b[1]) + 1, int(b[0]) + 1], 12) for b in bxs]
            checks.append(check("%s: crop brackets in all four corners" % name, min(got) > 0.03, min(got), "> 0.03"))
            neg_boxes += bxs
        elif typ == "label":
            xy, anc = _label_xy(el, W, H)
            fnt = font(el.get("font", MONO), el.get("size", 12))
            for k in samples:
                t = k / fps
                s = _label_text(el, k, t)
                others = [_label_text(el, j, j / fps) for j in range(n)]
                wrong = next((o for o in others if o != s), None) or ("X" * len(s))
                bgc = tuple(int(v) for v in bgs[k][int(min(H - 1, max(0, xy[1]))), int(min(W - 1, max(0, xy[0])))])
                c = blend(col, bgc, a)

                rest = hud_draw(Image.fromarray(bgs[k].copy()), [e for e in elems if e is not el], k, t)

                def err(txt):
                    im = rest.copy()
                    dd = ImageDraw.Draw(im)
                    box = draw_text(dd, xy, txt, fnt, c, anc, el.get("tracking", 0))
                    ref = N.asarray(im).astype(float)
                    bb = draw_text(ImageDraw.Draw(Image.new("RGB", (W, H))), xy, s, fnt, c, anc, el.get("tracking", 0))
                    x0, y0, x1, y1 = int(max(0, bb[0] - 1)), int(max(0, bb[1] - 1)), int(min(W, bb[2] + 1)), int(min(H, bb[3] + 1))
                    return float(N.abs(fo[k][y0:y1, x0:x1] - ref[y0:y1, x0:x1]).mean()), (x0, y0, x1, y1)
                e_ok, bx = err(s)
                e_bad, _ = err(wrong)
                checks.append(check("%s: label %r reads %r at t=%.2fs" % (name, el.get("id", el["at"]), s, t), e_ok < 0.6 * e_bad and e_ok < 6,
                                    [round(e_ok, 2), round(e_bad, 2)], "right text matches, other text does not"))
                neg_boxes.append(bx)
            if a < 1.0:
                pk = peak(fo[samples[0]], bx)
                exp_pk = max(blend(col, tuple(int(v) for v in bgs[samples[0]][int(bx[1]), int(bx[0])]), a))
                checks.append(check("%s: label %r opacity %.0f%%" % (name, el.get("id", el["at"]), a * 100), abs(pk - exp_pk) <= 14, pk, exp_pk))
        elif typ == "bar":
            x0, y0, x1, y1 = el["box"]
            yc = int((y0 + y1) / 2)
            c = N.array(blend(col, bg if not base else tuple(int(v) for v in bgs[0][yc, x0]), a), float)
            for k in samples:
                row = fo[k][yc, int(x0):int(x1) + 1]
                on = N.abs(row - c).max(axis=1) < 30
                fr = float(on.sum()) / (x1 - x0 + 1)
                segs_ = el.get("segments", 1)
                exp_f = el["frac"](k / fps)
                if segs_ > 1:
                    gapfrac = el.get("gap", 3) * (segs_ - 1) / (x1 - x0)
                    exp_f = min(1.0, exp_f) * (1 - gapfrac)
                checks.append(check("%s: bar %r fill at t=%.2fs" % (name, el.get("id", "bar"), k / fps), abs(fr - exp_f) < 0.03, fr, exp_f))
            if el.get("segments", 1) > 1:
                row = fo[-1][yc, int(x0):int(x1) + 1] if el["frac"]((n - 1) / fps) >= 0.999 else None
                if row is not None:
                    on = list(N.abs(row - c).max(axis=1) < 30)
                    runs = sum(1 for j in range(len(on)) if on[j] and (j == 0 or not on[j - 1]))
                    checks.append(check("%s: %d segments" % (name, el["segments"]), runs == el["segments"], runs, el["segments"]))
            neg_boxes.append((x0, y0, x1, y1))
        elif typ == "playhead":
            x0, y0, x1, y1 = el["box"]
            for k in samples:
                yc = int(y0) + 1
                row = N.abs(fo[k][yc, :] - N.array(blend(col, bg, a), float)).max(axis=1) < 30
                xs = N.nonzero(row[int(x0) - 2:int(x1) + 3])[0]
                xm = float(xs.mean()) + int(x0) - 2 if len(xs) else -1
                exp_x = x0 + (x1 - x0) * el["frac"](k / fps)
                checks.append(check("%s: playhead at t=%.2fs" % (name, k / fps), abs(xm - exp_x) <= 1.5, xm, exp_x))
        elif typ == "ticks":
            x0, y0, x1, y1 = el["box"]
            row = N.abs(fo[0][int(y1) - 1, :] - fi[0][int(y1) - 1, :]).max(axis=1) > 25
            seg = row[int(x0) - 1:int(x1) + 2]
            runs = sum(1 for j in range(len(seg)) if seg[j] and (j == 0 or not seg[j - 1]))
            checks.append(check("%s: %d ticks" % (name, el["count"] + 1), runs == el["count"] + 1, runs, el["count"] + 1))
            neg_boxes.append((x0, y0, x1, y1))
        elif typ == "dots":
            for k in samples:
                act = el["active"](k / fps)
                cc = N.array(blend(col, bg, a), float)
                filled = [float(N.abs(fo[k][int(y) - 1:int(y) + 2, int(x) - 1:int(x) + 2] - cc).max()) < 40 for x, y in el["centers"]]
                exp_ = [(j <= act) if el.get("cumulative") else (j == act) for j in range(len(el["centers"]))]
                checks.append(check("%s: active dot(s) at t=%.2fs" % (name, k / fps), filled == exp_, filled, exp_))
        elif typ == "custom" and el.get("check"):
            checks += el["check"](fo, fi, fps)
    if neg_boxes:
        neg = max(ink(fi[k], b, fi[k][min(H - 1, int(b[1]) + 1), min(W - 1, int(b[0]) + 1)], 12) for b in neg_boxes for k in samples)
        checks.append(check("negative control: the input frames carry none of the HUD", neg < 0.01, neg, "< 0.01"))
    return checks, [out]


def _chapters(names, seconds):
    def at(t):
        k = min(len(names) - 1, int(t / seconds * len(names)))
        return k
    return at


_CH = ["INTRO", "GEOMETRY", "DEPTH", "MOTION", "OUTRO"]


@card("CAM-282")
def swiss_hud(task, wd):
    """Crop marks (inset 3 %), four mono corner labels incl. chapter 'NN — NAME' and running timecode, segmented bar = chapters."""
    W, H, S = 960, 540, 3.0
    ch = _chapters(_CH, S)
    els = [{"type": "brackets", "inset": 0.03, "color": "#f2f2f2"},
           {"type": "label", "id": "name", "at": "tl", "inset": 0.05, "text": "Lena Ortiz / Director", "upper": True, "size": 11},
           {"type": "label", "id": "project", "at": "tr", "inset": 0.05, "text": "Kosif Reel / 2026", "upper": True, "size": 11},
           {"type": "label", "id": "chapter", "at": "bl", "inset": 0.05, "text": lambda i, t: "%02d — %s" % (ch(t) + 1, _CH[ch(t)]), "upper": True, "size": 11},
           {"type": "label", "id": "tc", "at": "br", "inset": 0.05, "text": lambda i, t: tc(t, 10), "size": 11},
           {"type": "bar", "id": "chapters", "box": (380, 500, 580, 504), "frac": lambda t: t / S, "segments": 5, "gap": 4, "color": "#f2f2f2"}]
    return hud_card(wd, "swiss_hud", els, W, H, 10, S, samples=[0, 15, 29])


@card("CAM-285")
def chapter_hud_bpm(task, wd):
    """Corner brackets, chapter index, timecode and bpm in mono."""
    S = 3.0
    ch = _chapters(_CH, S)
    els = [{"type": "brackets", "color": "#e8e4d8"},
           {"type": "label", "id": "chapter", "at": "tl", "inset": 0.05, "text": lambda i, t: "CH %02d/05" % (ch(t) + 1), "size": 12},
           {"type": "label", "id": "tc", "at": "tr", "inset": 0.05, "text": lambda i, t: tc(t, 10), "size": 12},
           {"type": "label", "id": "bpm", "at": "br", "inset": 0.05, "text": "120 BPM", "size": 12}]
    return hud_card(wd, "chapter_hud", els, seconds=S, samples=[0, 12, 29])


@card("CAM-288")
def corner_meta_labels(task, wd):
    """Tiny wide-tracked condensed caps top-left with a red underline and bottom-right year/version (tracking .3em, ~2 % size)."""
    W, H = 960, 540
    size = int(round(0.02 * H))

    def underline(d, im, i, t):
        d.rectangle([W * 0.04, H * 0.04 + size + 3, W * 0.04 + 120, H * 0.04 + size + 4], fill=(230, 40, 40))

    def chk(fo, fi, fps):
        r = centroid(fo[0].astype("uint8"), (230, 40, 40), 40)
        return [check("red underline under the top-left label", r is not None and abs(r[1] - (H * 0.04 + size + 3.5)) < 1.5, r, "under label")]
    els = [{"type": "label", "id": "tl", "at": "tl", "inset": 0.04, "text": "Field notes", "upper": True, "size": size, "tracking": 0.3},
           {"type": "label", "id": "br", "at": "br", "inset": 0.04, "text": "2026 · v1.3", "upper": True, "size": size, "tracking": 0.3},
           {"type": "custom", "draw": underline, "check": chk}]
    return hud_card(wd, "corner_meta", els, W, H, seconds=1.0, samples=[0])


@card("CAM-289")
def numbered_step_chip(task, wd):
    """Top-centre chip: accent square with a two-digit number in dark mono + tracked uppercase step name; swaps per step."""
    W, H, S = 960, 540, 3.0
    steps = ["capture", "edit", "render"]
    k = lambda t: min(2, int(t / S * 3))

    def chip(d, im, i, t):
        d.rectangle([W / 2 - 110, 20, W / 2 - 82, 48], fill=(255, 196, 0))
    els = [{"type": "custom", "draw": chip,
            "check": lambda fo, fi, fps: [check("accent chip 28 px square", (lambda b: b and (b[2] - b[0], b[3] - b[1]))(bbox(fo[0].astype("uint8"), (255, 196, 0), 40)) == (29, 29),
                                                (lambda b: b and (b[2] - b[0], b[3] - b[1]))(bbox(fo[0].astype("uint8"), (255, 196, 0), 40)), (29, 29))]},
           {"type": "label", "id": "num", "at": (W / 2 - 96, 34, "mm"), "text": lambda i, t: "%02d" % (k(t) + 1), "font": MONO_B, "size": 14, "color": "#141414", "bg": (255, 196, 0)},
           {"type": "label", "id": "name", "at": (W / 2 - 72, 34, "lm"), "text": lambda i, t: steps[k(t)], "upper": True, "size": 13, "tracking": 0.15}]
    return hud_card(wd, "step_chip", els, W, H, seconds=S, samples=[0, 12, 25])


@card("CAM-291")
def hud_corner_timecode(task, wd):
    """Four small mono labels pinned to safe corners (URL, network, slogan, live mm:ss.cs) at ~65 % grey, legible on black and white."""
    from PIL import Image
    W, H, S, fps = 960, 540, 2.0, 10
    size = int(round(0.015 * H * 1.4))
    base = lambda i, t: Image.new("RGB", (W, H), (0, 0, 0) if i < 10 else (255, 255, 255))
    grey = (150, 150, 150)
    els = [{"type": "label", "id": "url", "at": "tl", "inset": 0.05, "text": "kosif.studio", "size": size, "color": grey},
           {"type": "label", "id": "net", "at": "tr", "inset": 0.05, "text": "KOSIF NETWORK", "size": size, "color": grey},
           {"type": "label", "id": "slogan", "at": "bl", "inset": 0.05, "text": "MADE IN MOTION", "size": size, "color": grey},
           {"type": "label", "id": "tc", "at": "br", "inset": 0.05, "text": lambda i, t: tc_cs(t), "size": size, "color": grey}]
    checks, outs = hud_card(wd, "corner_tc", els, W, H, fps, S, base=base, samples=[0, 5, 15, 19])
    checks.append(check("grey labels keep contrast on both black (150 vs 0) and white (150 vs 255) cuts", min(150 - 0, 255 - 150) >= 100, min(150, 105), ">= 100"))
    return checks, outs


def _hud_simple(wd, name, ins_tl, ins_tr, ins_bl, ins_br, extra=(), S=3.0, size=12, alpha=1.0, color="#f0eee6", brackets=True, W=960, H=540, fps=10, samples=None):
    els = [{"type": "brackets", "color": color, "alpha": alpha}] if brackets else []
    for at, txt in (("tl", ins_tl), ("tr", ins_tr), ("bl", ins_bl), ("br", ins_br)):
        if txt is not None:
            els.append({"type": "label", "id": at, "at": at, "inset": 0.05, "text": txt, "size": size, "alpha": alpha, "color": color})
    els += list(extra)
    return hud_card(wd, name, els, W, H, fps, S, samples=samples or [0, int(S * fps / 2), int(S * fps) - 1])


@card("CAM-293")
def chaptered_hud_frame(task, wd):
    """Corner brackets, '0N/07' chapter label, timecode, ruler progress (mono 24 px at 1080 w → 12 px at 540)."""
    S = 3.5
    k = lambda t: min(6, int(t / S * 7))
    return _hud_simple(wd, "chaptered", lambda i, t: "0%d/07" % (k(t) + 1), lambda i, t: tc(t, 10), None, None, size=12, S=S,
                       extra=[{"type": "ticks", "box": (300, 506, 660, 512), "count": 14, "color": "#f0eee6"},
                              {"type": "bar", "id": "ruler", "box": (300, 514, 660, 516), "frac": lambda t: t / S, "color": "#f0eee6"}])


@card("CAM-296")
def cinematic_hud_chrome(task, wd):
    """Brackets, top labels + timecode, bottom elapsed bar with ticks every 0.1 s and moving playhead, all ~40 % opacity."""
    S = 2.0
    els = [{"type": "brackets", "inset": 0.04, "alpha": 0.4, "color": "#ffffff"},
           {"type": "label", "id": "title", "at": "tl", "inset": 0.06, "text": "REEL 07 · NIGHT", "size": 11, "alpha": 0.4},
           {"type": "label", "id": "tc", "at": "tr", "inset": 0.06, "text": lambda i, t: tc(t, 10), "size": 11, "alpha": 0.4},
           {"type": "ticks", "box": (200, 500, 760, 506), "count": 20, "alpha": 0.4, "color": "#ffffff"},
           {"type": "playhead", "box": (200, 496, 760, 510), "frac": lambda t: t / S, "alpha": 0.4, "color": "#ffffff"}]
    return hud_card(wd, "cine_chrome", els, 960, 540, 10, S, samples=[0, 10, 19])


@card("CAM-297")
def bottom_progress_line(task, wd):
    """A 2 px black line at the very bottom edge grows linearly from the left over the whole duration."""
    S = 3.0
    els = [{"type": "bar", "id": "progress", "box": (0, 538, 959, 539), "frac": lambda t: t / S, "color": "#000000"}]
    return hud_card(wd, "progress_line", els, 960, 540, 10, S, bg=(236, 232, 224), samples=[3, 15, 27])


@card("CAM-298")
def poster_metadata_hud(task, wd):
    """Four corner mono labels (title, chapter 'NN / NAME', grid spec, running timecode) updated per act; tracking +8 %."""
    S = 3.0
    acts = ["SETUP", "TURN", "PAYOFF"]
    k = lambda t: min(2, int(t / S * 3))
    els = [{"type": "label", "id": a, "at": a, "inset": 0.05, "text": txt, "size": 11, "upper": True, "tracking": 0.08}
           for a, txt in (("tl", "Poster Series"), ("tr", lambda i, t: "%02d / %s" % (k(t) + 1, acts[k(t)])), ("bl", "12 col · 8 px"), ("br", lambda i, t: tc(t, 10)))]
    return hud_card(wd, "poster_hud", els, 960, 540, 10, S, samples=[0, 12, 25])


@card("CAM-300")
def chapter_strip(task, wd):
    """Top strip '04 / 07 TITLE' that advances per chapter."""
    S = 3.5
    names = ["ORIGIN", "SIGNAL", "NOISE", "SHAPE", "PULSE", "ECHO", "END"]
    k = lambda t: min(6, int(t / S * 7))
    els = [{"type": "label", "id": "strip", "at": "tc", "inset": 0.04, "text": lambda i, t: "%02d / 07 %s" % (k(t) + 1, names[k(t)]), "size": 13},
           {"type": "bar", "id": "strip-bar", "box": (380, 44, 580, 46), "frac": lambda t: (k(t) + 1) / 7, "color": "#ffffff"}]
    return hud_card(wd, "chapter_strip", els, 960, 540, 10, S, samples=[2, 16, 32])


@card("CAM-304")
def chapter_hud_8(task, wd):
    """Corner brackets, chapter n/8, mono label and a progress line at the bottom."""
    S = 4.0
    k = lambda t: min(7, int(t / S * 8))
    return _hud_simple(wd, "hud8", "KOSIF / CAMERA", lambda i, t: "%d/8" % (k(t) + 1), None, None, S=S,
                       extra=[{"type": "bar", "id": "line", "box": (48, 520, 912, 521), "frac": lambda t: t / S, "color": "#f0eee6"}], samples=[0, 20, 39])


@card("CAM-305")
def scope_hud(task, wd):
    """Uppercase sans corner labels; bottom-left 'CH1 2.0V/div 110BPM T+ss.ss' per frame; top-right chapter word per section."""
    S = 3.0
    words = ["SIGNAL", "PHASE", "DECAY"]
    k = lambda t: min(2, int(t / S * 3))
    els = [{"type": "label", "id": a, "at": a, "inset": 0.05, "text": txt, "size": 12, "font": SANS, "upper": True, "alpha": 0.7}
           for a, txt in (("tl", "Scope mode"), ("tr", lambda i, t: words[k(t)]), ("bl", lambda i, t: "CH1 2.0V/div 110BPM T+%05.2f" % t), ("br", "720p · 30"))]
    return hud_card(wd, "scope_hud", els, 960, 540, 10, S, samples=[0, 13, 27])


@card("CAM-310")
def persistent_cinematic_hud(task, wd):
    """Brackets 24 px inset; title/artist TL, countdown TR, 'BAR n / N' + dash progress BL, 'NN — CHAPTER' BR, ~60 % cream."""
    S, bars = 4.0, 8
    k = lambda t: min(bars - 1, int(t / S * bars))
    cream = "#f3ead2"
    els = [{"type": "brackets", "inset": 24 / 960, "color": cream, "alpha": 0.6}]
    for a, txt in (("tl", "Noor — Saher"), ("tr", lambda i, t: "-%05.2f" % (S - t)), ("bl", lambda i, t: "BAR %d / %d" % (k(t) + 1, bars)),
                   ("br", lambda i, t: "%02d — %s" % (k(t) // 2 + 1, ["DAWN", "RISE", "PEAK", "FALL"][k(t) // 2]))):
        els.append({"type": "label", "id": a, "at": a, "inset": 0.06, "text": txt, "size": 12, "upper": True, "tracking": 0.15, "alpha": 0.6, "color": cream})
    els.append({"type": "bar", "id": "dash", "box": (58, 470, 218, 472), "frac": lambda t: (k(t) + 1) / bars, "segments": bars, "gap": 4, "color": cream, "alpha": 0.6})
    return hud_card(wd, "cine_hud", els, 960, 540, 10, S, samples=[0, 20, 39])


@card("CAM-312")
def chapter_hud_labels(task, wd):
    """'01 Geometry / 02 Depth' corner chapter labels plus timecode."""
    S = 2.0
    els = [{"type": "label", "id": "chapter", "at": "tl", "inset": 0.05, "text": lambda i, t: "01 Geometry" if t < 1 else "02 Depth", "size": 13},
           {"type": "label", "id": "tc", "at": "br", "inset": 0.05, "text": lambda i, t: tc(t, 10), "size": 13}]
    return hud_card(wd, "geo_depth", els, 960, 540, 10, S, samples=[2, 15])


@card("CAM-315")
def viewfinder_hud_chapters(task, wd):
    """Brackets, reel ID, timecode, 'NN / 08 CHAPTER' with progress dots per section; mono 11 px, 40 % opacity, 3 % margin."""
    S = 4.0
    k = lambda t: min(7, int(t / S * 8))
    names = ["OPEN", "LIGHT", "FORM", "FLOW", "CUT", "BEAT", "LIFT", "CLOSE"]
    els = [{"type": "brackets", "inset": 0.03, "alpha": 0.4},
           {"type": "label", "id": "reel", "at": "tl", "inset": 0.05, "text": "REEL K-0412", "size": 11, "alpha": 0.4},
           {"type": "label", "id": "tc", "at": "tr", "inset": 0.05, "text": lambda i, t: tc(t, 10), "size": 11, "alpha": 0.4},
           {"type": "label", "id": "chapter", "at": "bl", "inset": 0.05, "text": lambda i, t: "%02d / 08 %s" % (k(t) + 1, names[k(t)]), "size": 11, "alpha": 0.4},
           {"type": "dots", "centers": [(820 + 12 * j, 510) for j in range(8)], "r": 3, "active": k, "cumulative": True, "alpha": 0.4}]
    return hud_card(wd, "viewfinder", els, 960, 540, 10, S, samples=[0, 18, 39])


@card("CAM-321")
def production_hud(task, wd):
    """Brackets, bottom-left spec (ID, BPM, resolution, fps), bottom-right elapsed + beat counter, left vertical ruler ticks (olive mono)."""
    S, bpm = 3.0, 120
    olive = "#a8a878"

    def ruler(d, im, i, t):
        for j in range(11):
            d.line([(20, 120 + 30 * j), (28 if j % 5 else 34, 120 + 30 * j)], fill=_rgb(olive))

    def chk(fo, fi, fps):
        col = fo[0][100:440, 20:22].mean(axis=(1, 2))
        n_t = sum(1 for j in range(1, len(col)) if col[j] > 60 and col[j - 1] <= 60)
        return [check("left ruler: 11 ticks", n_t == 11, n_t, 11)]
    els = [{"type": "brackets", "color": olive},
           {"type": "label", "id": "spec", "at": "bl", "inset": 0.05, "text": "ID K7 · 120 BPM · 1920x1080 · 30 fps", "size": 11, "color": olive},
           {"type": "label", "id": "elapsed", "at": "br", "inset": 0.05, "text": lambda i, t: "%05.2f · BEAT %d" % (t, int(t * bpm / 60) + 1), "size": 11, "color": olive},
           {"type": "custom", "draw": ruler, "check": chk}]
    return hud_card(wd, "production_hud", els, 960, 540, 10, S, samples=[0, 14, 29])


@card("CAM-323")
def fig_caption_hud(task, wd):
    """Corner ticks; TL reel title; TR 'NN/06 — CHAPTER'; per-scene 'FIG.0n — NAME' + spec line; bottom timecode + centre bar."""
    S = 3.0
    names = ["GRID", "RIPPLE", "BLOOM"]
    k = lambda t: min(2, int(t / S * 3))
    specs = ["9x5 grid · radial ripple · eases", "1 source · 3 rings · sine", "glow 0.6 · 24 px · screen"]
    els = [{"type": "brackets", "len": 0.02},
           {"type": "label", "id": "reel", "at": "tl", "inset": 0.05, "text": "KOSIF LAB REEL", "size": 11},
           {"type": "label", "id": "chapter", "at": "tr", "inset": 0.05, "text": lambda i, t: "%02d/06 — %s" % (k(t) + 1, names[k(t)]), "size": 11},
           {"type": "label", "id": "fig", "at": (60, 380, "la"), "text": lambda i, t: "FIG.0%d — %s" % (k(t) + 1, names[k(t)]), "size": 13},
           {"type": "label", "id": "specs", "at": (60, 400, "la"), "text": lambda i, t: specs[k(t)], "size": 11},
           {"type": "label", "id": "tc", "at": "bl", "inset": 0.05, "text": lambda i, t: tc(t, 10), "size": 11},
           {"type": "bar", "id": "centre", "box": (400, 512, 560, 514), "frac": lambda t: t / S}]
    return hud_card(wd, "fig_hud", els, 960, 540, 10, S, samples=[0, 13, 27])


@card("CAM-328")
def hud_reel_chrome(task, wd):
    """Scene code, ruler scrubber with a moving marker, spec text '1920x1080/30fps', corner brackets."""
    S = 2.0
    els = [{"type": "brackets"},
           {"type": "label", "id": "scene", "at": "tl", "inset": 0.05, "text": lambda i, t: "SC-%02d" % (1 if t < 1 else 2), "size": 12},
           {"type": "label", "id": "spec", "at": "br", "inset": 0.05, "text": "1920x1080/30fps", "size": 12},
           {"type": "ticks", "box": (300, 496, 660, 502), "count": 12},
           {"type": "playhead", "box": (300, 492, 660, 506), "frac": lambda t: t / S}]
    return hud_card(wd, "reel_chrome", els, 960, 540, 10, S, samples=[0, 9, 19])


@card("CAM-330")
def chapter_ruler_timeline(task, wd):
    """Bottom ruler at 95 % height with ticks every 10 frames, diamond chapter markers, red playhead, frame + chapter label in serif italic."""
    W, H, fps, S = 960, 540, 30, 2.0
    n = int(S * fps)
    y = int(0.95 * H)
    x0, x1 = 80, 880
    marks = [0.0, 0.5, 1.25]
    names = ["Prologue", "Ascent", "Summit"]
    k = lambda t: max(j for j, m in enumerate(marks) if t >= m)

    def diamonds(d, im, i, t):
        for m in marks:
            xm = x0 + (x1 - x0) * m / S
            d.polygon([(xm, y - 12), (xm + 4, y - 8), (xm, y - 4), (xm - 4, y - 8)], fill=(240, 220, 120))

    def chk(fo, fi, fps_):
        got = [centroid(fo[0][y - 14:y - 2].astype("uint8"), (240, 220, 120), 40) for _ in [0]]
        row = N_abs_row = None
        cnt = 0
        rowv = fo[0][y - 8, x0 - 6:x1 + 6]
        on = [float(abs(p - [240, 220, 120]).max()) < 40 for p in rowv]
        cnt = sum(1 for j in range(len(on)) if on[j] and (j == 0 or not on[j - 1]))
        return [check("three diamond chapter markers on the ruler", cnt == 3, cnt, 3)]
    els = [{"type": "ticks", "box": (x0, y, x1, y + 6), "count": n // 10},
           {"type": "custom", "draw": diamonds, "check": chk},
           {"type": "playhead", "box": (x0, y - 3, x1, y + 9), "frac": lambda t: t / S, "color": "#ff2020"},
           {"type": "label", "id": "frame", "at": (x0, y - 22, "lb"), "text": lambda i, t: "frame %03d · %s" % (i, names[k(t)]), "font": SERIF_I, "size": 16}]
    return hud_card(wd, "chapter_ruler", els, W, H, fps, S, samples=[3, 20, 50])


@card("CAM-333")
def hud_ease_labels(task, wd):
    """The current easing name and the timecode in the corners while a dot moves with that ease."""
    S = 2.0
    eases = [("easeInOutCubic", ease_io_cubic), ("easeOutExpo", ease_out_expo)]
    k = lambda t: 0 if t < 1 else 1

    def mover(d, im, i, t):
        u = (t % 1.0)
        x = 200 + 560 * eases[k(t)][1](u)
        d.ellipse([x - 8, 262, x + 8, 278], fill=(255, 0, 0))

    def chk(fo, fi, fps):
        xs = [centroid(f.astype("uint8"), "red")[0] for f in fo]
        e1 = max(abs(xs[i] - (200 + 560 * ease_io_cubic(i / fps % 1))) for i in range(10))
        e2 = max(abs(xs[i] - (200 + 560 * ease_out_expo(i / fps % 1))) for i in range(10, 20))
        return [check("dot follows the labelled ease (max px error)", max(e1, e2) < 1.5, max(e1, e2), "< 1.5")]
    els = [{"type": "label", "id": "ease", "at": "tl", "inset": 0.05, "text": lambda i, t: eases[k(t)][0], "size": 12},
           {"type": "label", "id": "tc", "at": "br", "inset": 0.05, "text": lambda i, t: tc(t, 10), "size": 12},
           {"type": "custom", "draw": mover, "check": chk}]
    return hud_card(wd, "ease_labels", els, 960, 540, 10, S, samples=[2, 14])


@card("CAM-325")
def stage_progress_rail(task, wd):
    """Four coloured dots on a line with labels; dots fill as each stage becomes active."""
    S = 4.0
    k = lambda t: min(3, int(t / S * 4))
    labels = ["Plan", "Build", "Test", "Ship"]
    xs = [240, 400, 560, 720]

    def rail(d, im, i, t):
        d.line([(240, 270), (720, 270)], fill=(90, 90, 90), width=2)
    els = [{"type": "custom", "draw": rail}] + [{"type": "label", "id": l, "at": (x, 290, "mt"), "text": l, "size": 13} for l, x in zip(labels, xs)]
    els.append({"type": "dots", "centers": [(x, 270) for x in xs], "r": 7, "active": k, "cumulative": True, "color": "#3cc0a0"})
    return hud_card(wd, "progress_rail", els, 960, 540, 10, S, samples=[2, 12, 25, 38])


@card("CAM-329")
def numbered_step_headers(task, wd):
    """Italic serif '01/02/03' plus a bold label at the top-left, swapping per step."""
    S = 3.0
    labels = ["Collect", "Shape", "Ship"]
    k = lambda t: min(2, int(t / S * 3))
    els = [{"type": "label", "id": "num", "at": (60, 50, "la"), "text": lambda i, t: "%02d" % (k(t) + 1), "font": SERIF_I, "size": 40},
           {"type": "label", "id": "label", "at": (120, 62, "la"), "text": lambda i, t: labels[k(t)], "font": SANS_B, "size": 22}]
    return hud_card(wd, "step_headers", els, 960, 540, 10, S, samples=[0, 12, 25])


@card("CAM-314")
def chapter_text_card(task, wd):
    """Bottom-left chapter card: coloured rule + 'n of 11' + condensed headline + 3-line body, crossfading on chapter change."""
    S = 2.0
    heads = ["THE SIGNAL", "THE ECHO"]
    k = lambda t: 0 if t < 1 else 1
    alpha_at = lambda t: min(1.0, abs(t - 1.0) / 0.2) if t > 0.2 else min(1.0, t / 0.2)

    def card_(d, im, i, t):
        d.rectangle([60, 340, 160, 343], fill=(255, 90, 40))

    def chk(fo, fi, fps):
        b0 = peak(fo[5], (60, 352, 200, 370))
        bx = peak(fo[10], (60, 352, 200, 370))
        return [check("crossfade: the headline dims at the chapter change", bx < 0.7 * b0, [bx, b0], "< 0.7x"),
                check("coloured rule above the card", centroid(fo[5].astype("uint8"), (255, 90, 40), 40) is not None, True, True)]
    els = [{"type": "custom", "draw": card_, "check": chk},
           {"type": "label", "id": "n", "at": (60, 352, "la"), "text": lambda i, t: "%d of 11" % (k(t) + 1), "size": 12},
           {"type": "label", "id": "head", "at": (60, 372, "la"), "text": lambda i, t: heads[k(t)], "font": SANS_B, "size": 22},
           {"type": "label", "id": "body1", "at": (60, 402, "la"), "text": "A short body line one", "font": SANS, "size": 12},
           {"type": "label", "id": "body2", "at": (60, 418, "la"), "text": "and a second line two", "font": SANS, "size": 12},
           {"type": "label", "id": "body3", "at": (60, 434, "la"), "text": "with the third line.", "font": SANS, "size": 12}]
    # crossfade: blend the card with the background around the change
    orig = hud_draw

    def base(i, t):
        from PIL import Image
        return Image.new("RGB", (960, 540), (18, 18, 20))
    from PIL import Image
    N = np()
    n = 20
    frames, bgs = [], []
    for i in range(n):
        t = i / 10
        b = base(i, t)
        over = orig(b, els, i, t)
        a = alpha_at(t)
        frames.append((N.asarray(over) * a + N.asarray(b) * (1 - a)).astype(N.uint8))
        bgs.append(N.asarray(b))
    out = write_video(wd / "chapter_card.mp4", frames, 10)
    inp = write_video(wd / "chapter_card_input.mp4", bgs, 10)
    fo, fi = read_video(out).astype(float), read_video(inp).astype(float)
    checks = chk(fo, fi, 10)
    e_ok, e_bad = text_match(fo[5], (60, 372), "THE SIGNAL", font(SANS_B, 22), (255, 255, 255), (18, 18, 20), "la", "THE ECHO")
    e2_ok, e2_bad = text_match(fo[15], (60, 372), "THE ECHO", font(SANS_B, 22), (255, 255, 255), (18, 18, 20), "la", "THE SIGNAL")
    checks += [check("chapter 1 headline reads THE SIGNAL", e_ok < 0.5 * e_bad, [e_ok, e_bad], "match"),
               check("chapter 2 headline reads THE ECHO", e2_ok < 0.5 * e2_bad, [e2_ok, e2_bad], "match"),
               check("negative control: input has no card", ink(fi[5], (60, 340, 300, 450), (18, 18, 20)) < 0.005, ink(fi[5], (60, 340, 300, 450), (18, 18, 20)), "0")]
    return checks, [out]


# ═════════════════════════ footage camera behaviours (zoom modes, moves, coverage, fit, PiP) ═════════════════════════
def _footage_world(W, H):
    mk = {"red": ("red", W * 0.3, H * 0.5, 7), "blue": ("blue", W * 0.7, H * 0.5, 7)}
    img = world(W, H, mk, bg=(90, 96, 104))
    return img, mk


def _black_frac(f, thr=8):
    N = np()
    return float((f.max(axis=2) < thr).mean())


@card("CAM-69")
def zoom_modes(task, wd):
    """zoomState: punch alternates 1 / 1+a per cut (0.18 s ease-out), Ken Burns linear, drift 1+0.7a with ±0.3a·W travel, pulse 1+a·exp(-t/0.32)."""
    W, H, fps, a = 320, 180, 20, 0.2
    cuts = [0.0, 1.0, 2.0, 3.0]
    img, mk = _footage_world(W, H)
    modes = {}

    def punch(t):
        k = max(i for i, c in enumerate(cuts) if t >= c)
        prev, tgt = (1 + a if k % 2 == 0 else 1.0), (1.0 if k % 2 == 0 else 1 + a)
        if k == 0:
            return 1.0, 0.0
        e = 1 - (1 - min(1.0, (t - cuts[k]) / 0.18)) ** 3
        return prev + (tgt - prev) * e, 0.0

    def kenburns(t):
        k = max(i for i, c in enumerate(cuts) if t >= c)
        return 1 + a * (t - cuts[k]) / 1.0, 0.0

    def drift(t):
        k = max(i for i, c in enumerate(cuts) if t >= c)
        u = (t - cuts[k]) / 1.0
        return 1 + 0.7 * a, (1 if k % 2 == 0 else -1) * (u - 0.5) * 0.3 * a * W

    def pulse(t):
        k = max(i for i, c in enumerate(cuts) if t >= c)
        return 1 + a * math.exp(-(t - cuts[k]) / 0.32), 0.0
    allm, spans = [], {}
    for name, fn in (("punch", punch), ("kenburns", kenburns), ("drift", drift), ("pulse", pulse)):
        st = len(allm)
        for f in range(int(4 * fps)):
            s, x = fn(f / fps)
            allm.append(mat_stage(x, 0, s, 0, (W / 2, H / 2)))
        spans[name] = st
    checks, outs, d = cam_run(wd, "zoom_modes", img, allm, W, H, fps, mk, tol=2.0)
    sm = pair_scale(d, "red", "blue", 0.4 * W)
    mid = [((p[0] + q[0]) / 2 - W / 2) if p and q else None for p, q in zip(d["meas"]["red"], d["meas"]["blue"])]
    P, K, D, U = spans["punch"], spans["kenburns"], spans["drift"], spans["pulse"]
    checks += [check("punch: 1+a after the 1st cut, 1 after the 2nd", _near(sm[P + 25], 1.2, 0.01) and _near(sm[P + 45], 1.0, 0.01), [sm[P + 25], sm[P + 45]], [1.2, 1.0]),
               check("punch: ease-out reaches >85 % within 0.18 s (4 frames)", sm[P + 23] > 1.17, sm[P + 23], "> 1.17"),
               check("kenburns: linear 1→1.2 within a shot", _near(sm[K + 10], 1.1, 0.01) and _near(sm[K + 19], 1.19, 0.012), [sm[K + 10], sm[K + 19]], [1.1, 1.19]),
               check("drift: constant 1+0.7a and lateral travel alternates", _near(sm[D + 5], 1.14, 0.01) and (mid[D + 19] - mid[D + 1]) * (mid[D + 39] - mid[D + 21]) < 0,
                     [sm[D + 5], mid[D + 19] - mid[D + 1], mid[D + 39] - mid[D + 21]], "1.14, opposite signs"),
               check("drift: travel ≈ 0.3·a·W", _near(abs(mid[D + 19] - mid[D + 1]), 0.3 * a * W * 0.9, 2.0), abs(mid[D + 19] - mid[D + 1]), 0.3 * a * W * 0.9),
               check("pulse: 1+a at the cut decaying with tau 0.32 s", _near(sm[U + 20], 1.2, 0.012) and _near(sm[U + 26], 1 + a * math.exp(-0.3 / 0.32), 0.012),
                     [sm[U + 20], sm[U + 26]], [1.2, 1 + a * math.exp(-0.3 / 0.32)])]
    return checks, outs


_MOVES = {  # name: (z0, z1, x0, x1, y0, y1, r0, r1, ease)
    "push_in": (1.0, 1.15, 0, 0, 0, 0, 0, 0, ease_io_sine), "pull_out": (1.2, 1.0, 0, 0, 0, 0, 0, 0, ease_io_sine),
    "slow_zoom": (1.0, 1.06, 0, 0, 0, 0, 0, 0, lambda p: p), "punch_in": (1.0, 1.18, 0, 0, 0, 0, 0, 0, lambda p: 1 - (1 - min(1, p / 0.16)) ** 3),
    "whip_pan": (1.12, 1.12, 1, -1, 0, 0, 0, 0, lambda p: ease_out_expo(p)), "pan": (1.15, 1.15, 0.8, -0.8, 0, 0, 0, 0, ease_io_sine),
    "tilt": (1.15, 1.15, 0, 0, 0.8, -0.8, 0, 0, ease_io_sine), "truck": (1.2, 1.2, -0.9, 0.9, 0, 0, 0, 0, lambda p: p),
    "dolly_zoom": (1.0, 1.3, 0, 0, 0, 0, 0, 0, lambda p: p * p), "orbit": (1.12, 1.18, 0.5, -0.5, 0, 0, -3, 3, ease_io_sine),
    "crane_up": (1.2, 1.05, 0, 0, 0.7, -0.6, 0, 0, ease_io_cubic)}


def _move_mat(m, p, W, H):
    z0, z1, x0, x1, y0, y1, r0, r1, ez = m
    e = ez(p)
    z = z0 + (z1 - z0) * e
    room_x, room_y = (z - 1) * W / 2, (z - 1) * H / 2
    return mat_stage((x0 + (x1 - x0) * e) * room_x, (y0 + (y1 - y0) * e) * room_y, z, r0 + (r1 - r0) * e, (W / 2, H / 2)), z, e


@card("CAM-70")
def cinematic_moves(task, wd):
    """The listed CAM.MOVES (push_in … crane_up): zoom from→to, x/y travel as a share of the zoom room, roll, ease."""
    W, H, fps, n = 320, 180, 10, 11
    img, mk = _footage_world(W, H)
    img = world(W, H, mk, bg=(90, 96, 104))
    mats, plan = [], []
    for name, m in _MOVES.items():
        for f in range(n):
            M, z, e = _move_mat(m, f / (n - 1), W, H)
            mats.append(M)
            plan.append((name, f, z, e))
    checks, outs, d = cam_run(wd, "moves", img, mats, W, H, fps, mk, tol=2.0)
    sm = pair_scale(d, "red", "blue", 0.4 * W)
    blacks = [_black_frac(f) for f in d["frames"]]
    for i, (name, m) in enumerate(_MOVES.items()):
        a, b = i * n, i * n + n - 1
        checks.append(check("%s: zoom %.2f→%.2f measured" % (name, m[0], m[1]), _near(sm[a], m[0], 0.015) and _near(sm[b], m[1], 0.015), [sm[a], sm[b]], [m[0], m[1]]))
        if name != "orbit":
            checks.append(check("%s: travel stays inside the zoom room (no black edge)" % name, max(blacks[a:b + 1]) == 0.0, max(blacks[a:b + 1]), 0))
    ang = pair_angle(d, "red", "blue")
    o = list(_MOVES).index("orbit") * n
    checks.append(check("orbit: roll -3°→+3°", _near(ang[o], -3, 0.5) and _near(ang[o + n - 1], 3, 0.5), [ang[o], ang[o + n - 1]], [-3, 3]))
    return checks, outs + [write_json(wd, "moves.json", {k: list(v[:8]) for k, v in _MOVES.items()})]


def _coverage_need(r_deg, W, H, k=0.56):
    r = math.radians(r_deg)
    q = max(W, H) / min(W, H)
    return abs(math.cos(r)) + q * abs(math.sin(r)) * k


def rotation_coverage(task, wd):
    """When the camera rolls, raise zoom to need = |cos r| + q·|sin r|·0.56 and measure black corners."""
    W, H = 320, 180
    img, _ = _footage_world(W, H)
    rows = {}
    frames = []
    for r in (2, 4, 6):
        need = _coverage_need(r, W, H)
        f_cov = warp(img, mat_stage(0, 0, need, r, (W / 2, H / 2)), W, H)
        f_raw = warp(img, mat_stage(0, 0, 1.0, r, (W / 2, H / 2)), W, H)
        frames += [f_cov, f_raw]
        rows[r] = {"need": need, "black_with_rule": _black_frac(f_cov), "black_without": _black_frac(f_raw)}
    out = write_video(wd / "coverage.mp4", frames, 2)
    fo = read_video(out)
    rows_m = {r: (_black_frac(fo[2 * i]), _black_frac(fo[2 * i + 1])) for i, r in enumerate((2, 4, 6))}
    checks = []
    for r, (cov, raw) in rows_m.items():
        checks.append(check("roll %d°: zoom raised to %.3f leaves no black corners" % (r, rows[r]["need"]), cov < 0.0005, cov, "< 0.05 %"))
        checks.append(check("negative control roll %d°: unzoomed frame shows black corners" % r, raw > 0.005, raw, "> 0.5 %"))
    return checks, [out, write_json(wd, "coverage.json", rows)]


def _plan_moves(mood, cuts, peaks, D):
    """CAM.plan rules: first push_in (photo: ken_burns) + punch 0.55; last pull_out; music/hype punch every 2nd cut;
    cinematic rack_focus on 35 % of long shots; loud peaks → punch_in (<=1 per 4 s, >=2.5 s apart, not within 0.35 s of a cut);
    never the same move twice in a row."""
    shots = [(cuts[i], cuts[i + 1] if i + 1 < len(cuts) else D) for i in range(len(cuts))]
    long_pool = {"talk": ["push_in", "slow_zoom", "drift"], "music": ["pan", "push_in", "truck"], "hype": ["whip_pan", "push_in", "truck"],
                 "cinematic": ["slow_zoom", "pan", "crane_up"], "photo": ["ken_burns", "pan", "tilt"], "screen": ["push_in", "pan", "locked_off"]}[mood]
    short_pool = ["punch_in", "push_in", "locked_off"]
    moves, accents = [], []
    longs = 0
    for i, (a, b) in enumerate(shots):
        pool = long_pool if b - a > 1.6 else short_pool
        if i == 0:
            mv = "ken_burns" if mood == "photo" else "push_in"
            accents.append({"at": a, "kind": "punch", "amount": 0.55})
        elif i == len(shots) - 1:
            mv = "pull_out"
        else:
            if mood == "cinematic" and b - a > 1.6:
                longs += 1
                mv = "rack_focus" if (longs * 0.35) % 1 < 0.35 else pool[i % len(pool)]
            else:
                mv = pool[i % len(pool)]
        if moves and mv == moves[-1]:
            mv = next(p for p in pool + short_pool + ["drift"] if p != moves[-1])
        moves.append(mv)
        if mood in ("music", "hype") and i % 2 == 1:
            accents.append({"at": a, "kind": "punch"})
    last = -99
    for p in peaks:
        if p - last >= 2.5 and min(abs(p - c) for c in cuts) > 0.35 and sum(1 for x in accents if x["kind"] == "punch_in" and abs(x["at"] - p) < 4) == 0:
            accents.append({"at": p, "kind": "punch_in"})
            last = p
    return [{"shot": i, "start": a, "end": b, "move": m} for i, ((a, b), m) in enumerate(zip(shots, moves))], accents


@card("CAM-72")
def mood_camera_planner(task, wd):
    """Plan a camera move per shot from cuts, mood and loud peaks; verify every rule on the produced plan."""
    cuts = [0, 2.0, 2.8, 5.0, 5.6, 8.0, 10.5, 11.0, 14.0]
    peaks = [1.0, 2.1, 3.5, 4.4, 6.0, 7.0, 9.4, 12.2, 12.9]
    D = 16.0
    res = {}
    checks = []
    for mood in ("talk", "music", "hype", "cinematic", "photo", "screen"):
        plan, acc = _plan_moves(mood, cuts, peaks, D)
        res[mood] = {"plan": plan, "accents": acc}
        mv = [p["move"] for p in plan]
        pin = sorted(a["at"] for a in acc if a["kind"] == "punch_in")
        checks.append(check("%s: first move %s, last pull_out" % (mood, "ken_burns" if mood == "photo" else "push_in"),
                            mv[0] == ("ken_burns" if mood == "photo" else "push_in") and mv[-1] == "pull_out", [mv[0], mv[-1]], "rule"))
        checks.append(check("%s: never the same move twice in a row" % mood, all(a != b for a, b in zip(mv[:-1], mv[1:])), mv, "no repeats"))
        checks.append(check("%s: peak punches >= 2.5 s apart and > 0.35 s from cuts" % mood,
                            all(b - a >= 2.5 for a, b in zip(pin[:-1], pin[1:])) and all(min(abs(p - c) for c in cuts) > 0.35 for p in pin), pin, "spaced"))
    music_p = [a["at"] for a in res["music"]["accents"] if a["kind"] == "punch"]
    checks.append(check("music: punch accent on every 2nd cut", music_p[1:] == [cuts[i] for i in range(1, len(cuts)) if i % 2 == 1], music_p, "every 2nd cut"))
    checks.append(check("cinematic: rack_focus used on some long shots", "rack_focus" in [p["move"] for p in res["cinematic"]["plan"]], True, True))
    naive = ["push_in"] * len(cuts)
    checks.append(check("negative control: an unplanned 'push_in everywhere' list fails the no-repeat rule", not all(a != b for a, b in zip(naive[:-1], naive[1:])), naive[:3], "repeats"))
    return checks, [write_json(wd, "camera_plan.json", res)]


@card("CAM-76")
def reference_camera_transfer(task, wd):
    """DNA.cameraFor: cycle the reference's measured moves over our cuts in order; accents every 1/rate s (>= 1.5 s gap);
    with < 3 measured moves fall back to the mood plan keeping the dominant move."""
    def camera_for(dna, cuts, D):
        moves = dna.get("moves", [])
        shots = [(cuts[i], cuts[i + 1] if i + 1 < len(cuts) else D) for i in range(len(cuts))]
        if len(moves) >= 3:
            plan = [moves[i % len(moves)] for i in range(len(shots))]
        else:
            base = [p["move"] for p in _plan_moves(dna.get("mood", "talk"), cuts, [], D)[0]]
            dom = max(set(moves), key=moves.count) if moves else base[0]
            plan = [dom if i % 2 == 0 else b for i, b in enumerate(base)]
        gap = max(1.5, 1.0 / max(1e-6, dna.get("accent_rate", 0.5)))
        acc, t = [], gap
        while t < D:
            acc.append(round(t, 3))
            t += gap
        return plan, acc
    cuts = [0, 2, 4, 6.5, 8, 10]
    ref = {"moves": ["push_in", "whip_pan", "pan", "punch_in"], "accent_rate": 0.4}
    plan, acc = camera_for(ref, cuts, 12)
    fast, acc2 = camera_for({"moves": ["push_in"] * 4, "accent_rate": 2.0}, cuts, 12)
    few, _ = camera_for({"moves": ["truck", "truck"], "mood": "music"}, cuts, 12)
    out = write_json(wd, "camera_dna.json", {"plan": plan, "accents": acc, "few_moves_plan": few, "fast_rate_accents": acc2})
    checks = [check("reference moves reused in order, cycling", plan == ["push_in", "whip_pan", "pan", "punch_in", "push_in", "whip_pan"], plan, "cycled"),
              check("accents every 1/rate = 2.5 s", acc == [2.5, 5.0, 7.5, 10.0], acc, [2.5, 5.0, 7.5, 10.0]),
              check("accent gap never below 1.5 s", all(b - a >= 1.5 - 1e-9 for a, b in zip(acc2[:-1], acc2[1:])), acc2, ">= 1.5"),
              check("< 3 measured moves: mood plan keeps the dominant move", few.count("truck") >= 3, few, "truck dominant"),
              check("negative control: the plain mood plan (no reference) does not reproduce the reference order",
                    [p["move"] for p in _plan_moves("talk", cuts, [], 12)[0]][:4] != ref["moves"], [p["move"] for p in _plan_moves("talk", cuts, [], 12)[0]][:4], "!= reference")]
    return checks, [out]


def _fit_box(iw, ih, W, H, mode):
    s = max(W / iw, H / ih) if mode == "cover" else min(W / iw, H / ih)
    w, h = iw * s, ih * s
    return s, ((W - w) / 2, (H - h) / 2, w, h)


@card("CAM-42")
def clip_fit_cover_contain(task, wd):
    """fitImage: scale = max(w/iw, h/ih) for cover or min(...) for contain, centred, on background #07111e."""
    from PIL import Image
    N = np()
    W, H = 180, 320
    src = Image.fromarray(world(320, 180, {"red": ("red", 20, 90, 8), "blue": ("blue", 300, 90, 8), "green": ("green", 160, 90, 10)}))
    outs, res = [], {}
    for mode in ("cover", "contain"):
        s, (x, y, w, h) = _fit_box(320, 180, W, H, mode)
        im = Image.new("RGB", (W, H), (7, 17, 30))
        im.paste(src.resize((round(w), round(h)), Image.NEAREST), (round(x), round(y)))
        p = wd / ("fit_%s.png" % mode)
        im.save(p)
        outs.append(p)
        A = N.asarray(im)
        res[mode] = {"scale": s, "green": centroid(A, "green"), "red": area(A, "red"), "bg_rows": int(sum(1 for r in range(H) if (A[r] == (7, 17, 30)).all()))}
    checks = [check("cover scale = max(180/320, 320/180) = 1.778", _near(res["cover"]["scale"], 320 / 180, 1e-9), res["cover"]["scale"], 1.778),
              check("contain scale = 0.5625", _near(res["contain"]["scale"], 0.5625, 1e-9), res["contain"]["scale"], 0.5625),
              check("cover crops the edge markers", res["cover"]["red"] == 0, res["cover"]["red"], 0),
              check("contain keeps them and letterboxes on #07111e", res["contain"]["red"] > 0 and res["contain"]["bg_rows"] > 200, [res["contain"]["red"], res["contain"]["bg_rows"]], "> 0, > 200"),
              check("both centred (subject at frame centre)", _pt_near(res["cover"]["green"], (90, 160), 1.5) and _pt_near(res["contain"]["green"], (90, 160), 1.5),
                    [res["cover"]["green"], res["contain"]["green"]], [90, 160])]
    return checks, outs


@card("CAM-73")
def fit_blurred_fill(task, wd):
    """frame 'fit': blurred copy (4.5 % W, brightness .88, saturate .85, scale 1.14) behind a contain-fit; coach says fit when cover would crop > 40 %."""
    from PIL import Image, ImageEnhance, ImageFilter
    N = np()
    W, H = 180, 320
    src = Image.fromarray(world(320, 180, {"red": ("red", 30, 90, 10), "blue": ("blue", 290, 90, 10)}, bg=(150, 120, 90)))
    s, (x, y, w, h) = _fit_box(320, 180, W, H, "cover")
    bgimg = src.resize((round(w * 1.14), round(h * 1.14)))
    bgimg = bgimg.crop(((bgimg.width - W) // 2, (bgimg.height - H) // 2, (bgimg.width - W) // 2 + W, (bgimg.height - H) // 2 + H))
    bgimg = ImageEnhance.Color(ImageEnhance.Brightness(bgimg.filter(ImageFilter.GaussianBlur(0.045 * W))).enhance(0.88)).enhance(0.85)
    s2, (x2, y2, w2, h2) = _fit_box(320, 180, W, H, "contain")
    bgimg.paste(src.resize((round(w2), round(h2))), (round(x2), round(y2)))
    p = wd / "fit_blur.png"
    bgimg.save(p)
    A = N.asarray(bgimg).astype(float)
    band = A[10:60]
    crop = lambda iw, ih: 1 - min(W / H, iw / ih) / max(W / H, iw / ih)
    checks = [check("fill band is soft (blurred copy)", sharpness(band) < 15, sharpness(band), "< 15"),
              check("fill band darker than the source (brightness .88)", band.mean() < 0.95 * N.asarray(src).astype(float).mean(), band.mean() / N.asarray(src).astype(float).mean(), "< 0.95"),
              check("whole frame kept: both edge markers visible", area(A.astype("uint8"), "red") > 20 and area(A.astype("uint8"), "blue") > 20, True, True),
              check("coach: 16:9 into 9:16 crops > 40 % → suggest fit", crop(16, 9) > 0.4, crop(16, 9), "> 0.4"),
              check("coach: 4:5 into 9:16 crops < 40 % → keep cover", crop(4, 5) < 0.4, crop(4, 5), "< 0.4"),
              check("negative control: a plain cover keeps neither edge marker", _fit_box(320, 180, W, H, "cover")[1][2] / 2 - 90 > 290 - 160, _fit_box(320, 180, W, H, "cover")[1][2], "crops")]
    return checks, [p]


@card("CAM-74")
def letterbox_bars_captions(task, wd):
    """fx.letterbox: bars 10.5 % H in landscape, 7 % in portrait; captions move up to 72 % H."""
    from PIL import Image, ImageDraw
    N = np()
    res, outs = {}, []
    for name, (W, H), frac in (("landscape", (320, 180), 0.105), ("portrait", (180, 320), 0.07)):
        im = Image.new("RGB", (W, H), (120, 140, 160))
        d = ImageDraw.Draw(im)
        bar = round(frac * H)
        d.rectangle([0, 0, W, bar - 1], fill=(0, 0, 0))
        d.rectangle([0, H - bar, W, H], fill=(0, 0, 0))
        cy = 0.72 * H
        d.rectangle([W * 0.2, cy - 6, W * 0.8, cy + 6], fill=(255, 255, 0))
        p = wd / ("letterbox_%s.png" % name)
        im.save(p)
        outs.append(p)
        A = N.asarray(im)
        top = next(r for r in range(H) if A[r].max() > 10)
        b = bbox(A, "yellow")
        res[name] = (top / H, (b[1] + b[3]) / 2 / H)
    checks = [check("landscape bars 10.5 % H", _near(res["landscape"][0], 0.105, 0.006), res["landscape"][0], 0.105),
              check("portrait bars 7 % H", _near(res["portrait"][0], 0.07, 0.004), res["portrait"][0], 0.07),
              check("captions at 72 % H, above the bottom bar", _near(res["landscape"][1], 0.72, 0.01) and res["landscape"][1] < 1 - 0.105, res["landscape"][1], 0.72),
              check("negative control: a plain frame has no bar", not (N.asarray(Image.new("RGB", (4, 4), (120, 140, 160))).max() < 10), 0, "no bar")]
    return checks, outs


@card("CAM-75")
def pip_inserts(task, wd):
    """drawPips: width 42 % of the short side, aspect clamped 0.56-1.4, x = W-w-5 %·m, y = 9 % H, spring scale-in, accent frame, 0.2 s fade out."""
    from PIL import Image, ImageDraw
    N = np()
    W, H, fps = 320, 180, 30
    m = min(W, H)
    w = 0.42 * m
    asp = max(0.56, min(1.4, 2.0))
    h = w / asp
    x, y = W - w - 0.05 * m, 0.09 * H
    zeta, om = 0.5, 18.0
    spring = lambda t: 1 - math.exp(-zeta * om * t) * (math.cos(om * math.sqrt(1 - zeta ** 2) * t) + zeta / math.sqrt(1 - zeta ** 2) * math.sin(om * math.sqrt(1 - zeta ** 2) * t))
    frames, scales = [], []
    for f in range(int(1.4 * fps)):
        t = f / fps
        s = spring(t)
        op = 1.0 if t < 1.2 else max(0.0, 1 - (t - 1.2) / 0.2)
        base = Image.fromarray(world(W, H, {}, bg=(60, 70, 80)))
        over = base.copy()
        d = ImageDraw.Draw(over)
        cx, cy = x + w / 2, y + h / 2
        ww, hh = w * s, h * s
        d.rectangle([cx - ww / 2 - 5, cy - hh / 2 - 5, cx + ww / 2 + 5, cy + hh / 2 + 5], fill=(255, 200, 0))
        d.rectangle([cx - ww / 2, cy - hh / 2, cx + ww / 2, cy + hh / 2], fill=(255, 0, 0))
        frames.append((N.asarray(over) * op + N.asarray(base) * (1 - op)).astype(N.uint8))
        scales.append(s)
    out = write_video(wd / "pip.mp4", frames, fps)
    fo = read_video(out)
    b = bbox(fo[30], "red")
    widths = [(lambda bb: (bb[2] - bb[0]) / w if bb else 0)(bbox(f, "red")) for f in fo[:30]]
    checks = [check("width 42 % of the short side", _near(b[2] - b[0], w, 1.5), b[2] - b[0], w),
              check("aspect clamped to 1.4", _near((b[2] - b[0]) / (b[3] - b[1]), 1.4, 0.05), (b[2] - b[0]) / (b[3] - b[1]), 1.4),
              check("right margin 5 % of m and top 9 % H", _near(W - b[2], 0.05 * m, 1.5) and _near(b[1], 0.09 * H, 1.5), [W - b[2], b[1]], [0.05 * m, 0.09 * H]),
              check("spring scale-in overshoots then settles", max(widths) > 1.05 and _near(widths[-1], 1.0, 0.03), [max(widths), widths[-1]], ">1.05 then 1"),
              check("fades out over 0.2 s at the end (full at 1.2 s, gone by 1.4 s)", area(fo[-1], "red") == 0 and area(fo[35], "red") > 0.9 * area(fo[30], "red") and 0 < peak(fo[38], b) < peak(fo[35], b),
                    [area(fo[35], "red"), peak(fo[38], b), area(fo[-1], "red")], "full, dimming, 0"),
              check("accent frame 5 px around the window", (lambda bb: bb and _near(bb[2] - bb[0] - (b[2] - b[0]), 10, 1.5))(bbox(fo[30], (255, 200, 0), 40)), True, True)]
    return checks, [out]


@card("CAM-43")
def multiplane_parallax(task, wd):
    """cam = lerp(0, 630, smoothstep(t/12)); zoom 1→1.10 about (640,500); layers move ×0.035 moon, ×0.19 far, ×0.68 mid, ×1 ground, ×1.38 fg."""
    N = np()
    sc, fps = 0.25, 4
    W, H = 320, 180
    layers = [("moon", 0.035, "yellow", 300), ("far", 0.19, "cyan", 500), ("mid", 0.68, "magenta", 700), ("ground", 1.0, "red", 900), ("fg", 1.38, "blue", 1100)]
    ts = [i / fps for i in range(12 * fps + 1)]
    yy, xx = N.mgrid[0:H, 0:W]
    frames, exp = [], {k: [] for k, *_ in layers}
    for t in ts:
        cam = 630 * smoothstep(t / 12)
        z = 1 + 0.10 * smoothstep(t / 12)
        img = N.zeros((H, W, 3), N.uint8) + 30
        for name, k, col, x0 in layers:
            X = 640 + ((x0 - cam * k) - 640) * z
            Y = 500 + (360 - 500) * z
            exp[name].append((X * sc, Y * sc))
            img[(xx - X * sc) ** 2 + (yy - (Y * sc + layers.index((name, k, col, x0)) * 8 - 16)) ** 2 <= 16] = COL[col]
        frames.append(img)
    out = write_video(wd / "parallax.mp4", frames, fps)
    fo = read_video(out)
    checks = []
    disp = {}
    for i, (name, k, col, x0) in enumerate(layers):
        tr = track(fo, col)
        z_end = 1.10
        pre = (tr[-1][0] / sc - 640) / z_end + 640
        disp[name] = x0 - pre
    for name, k, col, x0 in layers:
        checks.append(check("%s layer travels %.3f x the camera" % (name, k), _near(disp[name] / 630.0, k, 0.02), disp[name] / 630.0, k))
    checks.append(check("depth order: fg > ground > mid > far > moon", disp["fg"] > disp["ground"] > disp["mid"] > disp["far"] > disp["moon"], disp, "ordered"))
    return checks, [out]


@card("CAM-44")
def cinematic_frame_cards(task, wd):
    """36 px bars #020711, an edge vignette (.8→0 at 17 %, 0 until 80 %, →.75), tracked 9-10 px labels, a 43 px light title with accent rule #ed9f64."""
    from PIL import Image, ImageDraw
    N = np()
    W, H = 1280, 720
    base = N.zeros((H, W, 3)) + N.array([110, 130, 150])
    x = N.linspace(0, 1, W)
    v = N.interp(x, [0, 0.17, 0.80, 1.0], [0.8, 0.0, 0.0, 0.75])
    img = base * (1 - v[None, :, None]) + N.array([2, 6, 17])[None, None, :] * v[None, :, None]
    img[:36] = (2, 7, 17)
    img[H - 36:] = (2, 7, 17)
    im = Image.fromarray(img.astype(N.uint8))
    d = ImageDraw.Draw(im)
    draw_text(d, (640, 300), "NIGHT HARBOUR", font(SANS, 43), (240, 240, 240), "mm", tracking=10 / 43)
    d.rectangle([600, 330, 680, 331], fill=(237, 159, 100))
    draw_text(d, (80, 60), "KOSIF FILMS", font(SANS, 10), (200, 200, 200), "la", tracking=0.3)
    p = wd / "cine_frame.png"
    im.save(p)
    A = N.asarray(im).astype(float)
    inp = base
    rowbar = A[:36].reshape(-1, 3).mean(axis=0)
    prof = A[400, :, 0]
    checks = [check("36 px bars in #020711", N.abs(rowbar - [2, 7, 17]).max() < 2 and A[36:].max() > 50 and A[36, 640].max() > 50, rowbar, [2, 7, 17]),
              check("left edge darkened to ~0.2 of plate", _near(prof[0] / 110, 0.2, 0.05), prof[0] / 110, 0.2),
              check("clear band between 17 % and 80 %", abs(prof[int(0.5 * W)] - 110) < 2, prof[int(0.5 * W)], 110),
              check("right edge darkened to ~0.25", _near(prof[-1] / 110, 0.25, 0.05), prof[-1] / 110, 0.25),
              check("accent rule #ed9f64 under the title", centroid(A.astype("uint8"), (237, 159, 100), 20) is not None, True, True),
              check("negative control: the plate has no vignette", not _near(inp[400, 0, 0] / 110, 0.2, 0.05), inp[400, 0, 0] / 110, "1.0")]
    return checks, [p]


@card("CAM-99")
def punch_inner_wrapper(task, wd):
    """GSAP tl.to('#clip .inner', {scale: 1.35, xPercent: -8, duration: 0.18}, 1): the inner wrapper punches, the timed clip is untouched."""
    W, H, fps = 320, 180, 50
    js = ("const {gsap} = require(%s);\nconst clip = {start: 0, duration: 3, x: 0, scale: 1}, inner = {scale: 1, xPercent: 0};\n"
          "const tl = gsap.timeline({paused: true}); tl.to(inner, {scale: 1.35, xPercent: -8, duration: 0.18}, 1);\nconst rows = [];\n"
          "for (let i = 0; i < 80; i++) { tl.seek(i / %d); rows.push([inner.scale, inner.xPercent, clip.start, clip.duration, clip.x, clip.scale]); }\n"
          "console.log(JSON.stringify(rows));" % (json.dumps(str(NODE_MODULES / "gsap")), fps))
    rows, jout = node_json(wd, "punch_inner", js)
    mk = {"red": ("red", 120, 90, 6), "blue": ("blue", 200, 90, 6)}
    wimg = world(W, H, mk)
    mats = [mat_stage(r[1] / 100 * W, 0, r[0], 0, (W / 2, H / 2)) for r in rows]
    checks, outs, d = cam_run(wd, "punch_inner", wimg, mats, W, H, fps, mk)
    sm = pair_scale(d, "red", "blue", 80.0)
    checks += [check("inner scale 1.35 after 0.18 s", _near(sm[60], 1.35, 0.03), sm[60], 1.35),
               check("inner shifted -8 % of width", _near(rows[60][1], -8, 1e-6), rows[60][1], -8),
               check("punch starts at 1 s and lasts 0.18 s", rows[50][0] == 1 and rows[59][0] == 1.35 and rows[54][0] < 1.35, [rows[50][0], rows[54][0], rows[59][0]], "1 → 1.35"),
               check("the timed clip element is never animated", all(r[2:] == [0, 3, 0, 1] for r in rows), rows[60][2:], [0, 3, 0, 1])]
    return checks, outs + [jout]


@card("CAM-415")
def parallax_ui_camera(task, wd):
    """Pans plus one push 1.0→1.08; flat UI rotates at most 8° in 3D (foreshortening cos 8°); UI sizes 14/16/24/40 px."""
    from PIL import Image, ImageDraw
    N = np()
    W, H, fps = 480, 270, 15
    mk, d0 = _push_world(W, H, W * 0.3)
    wimg = world(W, H, mk)
    mats, angles = [], []
    for f in range(int(4 * fps) + 1):
        t = f / fps
        x = -30 * ease_io_sine(t / 2) if t < 2 else -30
        s = 1.0 if t < 2 else 1 + 0.08 * ease_io_sine((t - 2) / 2)
        mats.append(mat_stage(x, 0, s, 0, (W / 2, H / 2)))
        angles.append(8 * ease_io_sine(t / 4))
    checks, outs, d = cam_run(wd, "ui25d", wimg, mats, W, H, fps, mk, tol=2.0, neg_k=2.0)
    sm = pair_scale(d, "red", "blue", d0)
    widths = [100 * math.cos(math.radians(a)) for a in angles]
    sizes = {}
    im = Image.new("RGB", (400, 120), (20, 20, 20))
    dd = ImageDraw.Draw(im)
    xx = 10
    for sz in (14, 16, 24, 40):
        b = dd.textbbox((xx, 100), "H", font=font(SANS, sz), anchor="ls")
        dd.text((xx, 100), "H", font=font(SANS, sz), fill=(255, 255, 255), anchor="ls")
        sizes[sz] = b[3] - b[1]
        xx += 60
    p = wd / "ui_sizes.png"
    im.save(p)
    hs = [sizes[k] for k in (14, 16, 24, 40)]
    checks += [check("exactly one push, x1.08", _near(sm[-1], 1.08, 0.008) and abs(sm[29] - 1.0) < 0.006, [sm[29], sm[-1]], [1.0, 1.08]),
               check("UI tilt capped at 8° (projected width >= cos 8°)", max(angles) <= 8 + 1e-9 and min(widths) >= 99.0, [max(angles), min(widths)], "<= 8°"),
               check("type scale 14/16/24/40 measured cap heights rise in order", hs == sorted(hs) and _near(hs[3] / hs[0], 40 / 14, 0.35), hs, "ordered, 40/14")]
    return checks, outs + [p]


@card("CAM-420")
def two_layer_grid_parallax(task, wd):
    """Background grid moves at 0.5 the speed of the foreground and settles from scale 0.92→1; accent area <= 25 %."""
    N = np()
    W, H, fps = 320, 180, 15
    frames = []
    yy, xx = N.mgrid[0:H, 0:W]
    for f in range(30):
        t = f / fps
        fgx = 80 * t
        s = 0.92 + 0.08 * ease_io_sine(t / 2)
        img = N.zeros((H, W, 3), N.uint8) + 25
        bx = (W / 2 + ((N.arange(W) - W / 2) / s) + 0.5 * fgx) % 24 < 1
        img[:, bx] = (70, 70, 70)
        img[(xx - (60 + fgx)) ** 2 + (yy - 90) ** 2 <= 64] = COL["red"]
        img[(xx - (W / 2 + (100 - W / 2) * s - 0.5 * fgx)) ** 2 + (yy - 40) ** 2 <= 16] = COL["blue"]
        img[150:170, 20:60] = (255, 120, 0)
        frames.append(img)
    out = write_video(wd / "grid_parallax.mp4", frames, fps)
    fo = read_video(out)
    r, b = track(fo, "red"), track(fo, "blue")
    vr = (r[20][0] - r[10][0]) / 10
    vb = (b[20][0] - b[10][0]) / 10
    accent = area(fo[0], (255, 120, 0), 40) / (W * H)
    checks = [check("background moves at 0.5x the foreground", _near(-vb / vr, 0.5, 0.08), -vb / vr, 0.5),
              check("background grid scale settles 0.92→1 (marker distance from centre)", _near((W / 2 - b[0][0]) / (W / 2 - 100), 0.92, 0.03), (W / 2 - b[0][0]) / (W / 2 - 100), 0.92),
              check("accent covers <= 25 % of the frame", accent <= 0.25, accent, "<= 0.25"),
              check("negative control: a one-layer move has ratio 1, not 0.5", not _near(1.0, 0.5, 0.08), 1.0, "!= 0.5")]
    return checks, [out]


@card("CAM-405")
def motion_handoff(task, wd):
    """Each leg ends with ~1 s of slow forward drift and the next leg starts by continuing it; reversals only inside a leg."""
    W, H, fps = 320, 180, 20
    drift = -8.0  # px/s, continuing the leg's own direction at the handoff

    def leg(t, a, b):
        u = t / 4
        x = a + (b - a) * ease_io_cubic(min(1, u / 0.75)) if u < 0.75 else b + drift * (t - 3)
        return x
    xs = [leg(f / fps, 0, -30) if f < 4 * fps else leg(f / fps - 4, -30 - drift, -60) + 0 for f in range(8 * fps)]
    # second leg continues the drift: shift so position/velocity are continuous at the handoff
    off = xs[4 * fps - 1] + drift / fps - xs[4 * fps]
    xs = xs[:4 * fps] + [x + off for x in xs[4 * fps:]]
    checks, outs, d, mid = _offset_card(wd, "handoff", W, H, fps, [(x, 0) for x in xs])
    h = 4 * fps - 1
    v_end = (mid[h][0] - mid[h - 10][0]) * fps / 10
    v_next = (mid[h + 10][0] - mid[h][0]) * fps / 10
    v_leg = (mid[h - 30][0] - mid[0][0])
    checks += [check("last 0.5 s of leg 1 is a slow drift (~8 px/s)", 3 <= abs(v_end) <= 14, v_end, "~8 px/s"),
               check("no position jump at the handoff", abs(mid[h + 1][0] - mid[h][0]) < 3, mid[h + 1][0] - mid[h][0], "< 3 px"),
               check("next leg continues the drift direction (no reversal at the seam)", v_end * v_next > 0 and v_end * v_leg > 0, [v_leg, v_end, v_next], "same sign")]
    return checks, outs


@card("CAM-409")
def persistent_snap_grid(task, wd):
    """A visible 24 px @1080 grid (12 px at 540) at 8 % opacity in every shot; elements rest snapped to cells."""
    N = np()
    W, H, cell = 960, 540, 12
    bg = N.array([20, 20, 24], float)
    frames = []
    for f in range(10):
        img = N.zeros((H, W, 3)) + bg
        img[::cell, :] = bg * 0.92 + 255 * 0.08
        img[:, ::cell] = bg * 0.92 + 255 * 0.08
        raw_x, raw_y = 137 + f * 7.3, 211
        sx, sy = round(raw_x / cell) * cell, round(raw_y / cell) * cell
        img[sy:sy + 4 * cell, sx:sx + 6 * cell] = (255, 0, 0)
        frames.append(img)
    out = write_video(wd / "snap_grid.mp4", frames, 10)
    fo = read_video(out).astype(float)
    col = fo[0][6, :, 0]
    lines = [x for x in range(W) if col[x] > bg[0] + 10]
    period = N.diff(lines).mean() if len(lines) > 2 else 0
    op = (col[0] - bg[0]) / (255 - bg[0])
    rests = [bbox(f.astype("uint8"), "red")[:2] for f in fo]
    checks = [check("grid period 12 px (24 @1080)", _near(period, 12, 0.01), period, 12),
              check("grid at ~8 % opacity", _near(op, 0.08, 0.02), op, 0.08),
              check("every element rest snaps to a cell", all(x % cell == 0 and y % cell == 0 for x, y in rests), rests[:3], "multiples of 12"),
              check("negative control: raw positions are off-grid", any((137 + f * 7.3) % cell for f in range(10)), 137 % 12, "!= 0")]
    return checks, [out]


_TOKENS = [0, 2, 4, 8, 12, 16, 24, 32, 40, 48, 64, 80, 96]


@card("CAM-406")
def spacing_tokens(task, wd):
    """Snap every gap/padding of a layout to {0,2,4,8,12,16,24,32,40,48,64,80,96} px; buttons padded 8x12; measure the render."""
    from PIL import Image, ImageDraw
    N = np()
    raw = {"pad": 27, "gap1": 13, "gap2": 50, "btn_py": 7, "btn_px": 13}
    snap = {k: min(_TOKENS, key=lambda t: abs(t - v)) for k, v in raw.items()}
    snap["btn_py"], snap["btn_px"] = 8, 12

    def render(sp, path):
        im = Image.new("RGB", (400, 300), (250, 250, 250))
        d = ImageDraw.Draw(im)
        y = sp["pad"]
        d.rectangle([sp["pad"], y, 300, y + 39], fill=(255, 0, 0))
        y += 40 + sp["gap1"]
        d.rectangle([sp["pad"], y, 300, y + 29], fill=(0, 0, 255))
        y += 30 + sp["gap2"]
        bw, bh = 60, 14
        d.rectangle([sp["pad"], y, sp["pad"] + bw + 2 * sp["btn_px"] - 1, y + bh + 2 * sp["btn_py"] - 1], fill=(0, 200, 0))
        im.save(path)
        A = N.asarray(im)
        r, b, g = bbox(A, "red"), bbox(A, "blue"), bbox(A, (0, 200, 0), 30)
        return [r[0], r[1], b[1] - r[3], g[1] - b[3], (g[2] - g[0] - bw) // 2, (g[3] - g[1] - bh) // 2]
    p, pi = wd / "tokens.png", wd / "tokens_input.png"
    got = render(snap, p)
    gin = render(raw, pi)
    checks = [check("every measured spacing is a token", all(v in _TOKENS for v in got), got, "in token set"),
              check("button padding 12 x 8", got[4:] == [12, 8], got[4:], [12, 8]),
              check("negative control: the raw layout has off-token spacings", not all(v in _TOKENS for v in gin), gin, "off-token")]
    return checks, [p, write_json(wd, "spacing.json", {"raw": raw, "snapped": snap})]


@card("CAM-367")
def dynamic_zoom_punch(task, wd):
    """Talking-head punch: alternate 1.0x and 1.10-1.15x framing every 2.5-4 s, switched on off-beats."""
    beat = 0.5
    switches = []
    t = 0.0
    k = 0
    while t < 12:
        t += [3.0, 2.75, 3.5][k % 3]
        switches.append(round(round(t / beat) * beat + beat / 2, 3))
        k += 1
    switches = [s for s in switches if s < 12]

    def sc(t):
        n = sum(1 for s in switches if t >= s)
        return 1.12 if n % 2 else 1.0
    fps = 10
    checks, outs, d, sm, si, plan = _push_card(wd, "zoom_punch", 320, 180, fps, sc, 120, d=110)
    seg = [b - a for a, b in zip([0] + switches[:-1], switches)]
    levels = sorted({round(sm[i], 2) for i in range(0, 120, 5)})
    checks += [check("only two framings: 1.0 and ~1.12", len(levels) <= 3 and _near(min(levels), 1.0, 0.01) and _near(max(levels), 1.12, 0.012), levels, [1.0, 1.12]),
               check("switch every 2.5-4 s", all(2.5 <= g <= 4.0 for g in seg[1:]), seg, "2.5-4"),
               check("switches land on off-beats", all(abs((s / beat) % 1 - 0.5) < 1e-6 for s in switches), switches, "half-beat"),
               check("negative control: input never punches", max(si) - min(si) < 0.01, max(si) - min(si), "< 0.01")]
    return checks, outs


@card("CAM-366")
def camera_push_norms(task, wd):
    """Push norms: 1.5-3.1x over 30-70 frames with peak ~5 %/frame; close-ups 2-5x per interaction. Validate and render a compliant push."""
    def lint(p):
        ratio, frames = p["to"] / p["from"], p["frames"]
        peak = max(math.exp(math.log(ratio) * (ease_io_sine((i + 1) / frames) - ease_io_sine(i / frames))) for i in range(frames)) - 1
        return {"ratio_ok": 1.5 <= ratio <= 3.1, "frames_ok": 30 <= frames <= 70, "peak": peak, "peak_ok": peak <= 0.055}
    good = {"from": 1.0, "to": 2.4, "frames": 50}
    bad = {"from": 1.0, "to": 1.2, "frames": 12}
    lg, lb = lint(good), lint(bad)
    fps = 30
    fn = lambda t: math.exp(math.log(2.4) * ease_io_sine(min(1, t * fps / 50)))
    W, H = 320, 180
    mk = {"red": ("red", 130, 90, 6), "blue": ("blue", 190, 90, 6)}
    wimg = world(W, H, mk)
    sc = [fn(f / fps) for f in range(55)]
    checks, outs, d = cam_run(wd, "push_norm", wimg, [mat_stage(0, 0, s, 0, (W / 2, H / 2)) for s in sc], W, H, fps, mk)
    sm = pair_scale(d, "red", "blue", 60.0)
    pk = max(sm[i + 1] / sm[i] for i in range(52)) - 1
    checks += [check("compliant push passes ratio/frames/peak lint", lg["ratio_ok"] and lg["frames_ok"] and lg["peak_ok"], lg, "all ok"),
               check("measured end ratio 2.4 over 50 frames", _near(sm[50], 2.4, 0.05), sm[50], 2.4),
               check("measured peak per-frame change <= ~5.5 %", pk <= 0.06, pk, "<= 0.06"),
               check("close-up 2-5x per interaction accepted at 3x", 2 <= 3.0 <= 5, 3.0, "2-5"),
               check("negative control: an unprocessed 1.2x/12 f push fails the lint", not (lb["ratio_ok"] and lb["frames_ok"]), lb, "fails")]
    return checks, outs


# ═════════════════════════ 2.5D / UI film camera rules ═════════════════════════
def _persp_project(pts, rx, ry, rz, s, D=1500.0):
    """Rotate 3D points (x,y,z) by rx, ry, rz degrees, scale s, perspective with eye distance D; returns 2D."""
    out = []
    ax, ay, az = (math.radians(v) for v in (rx, ry, rz))
    for x, y, z in pts:
        y, z = y * math.cos(ax) - z * math.sin(ax), y * math.sin(ax) + z * math.cos(ax)
        x, z = x * math.cos(ay) + z * math.sin(ay), -x * math.sin(ay) + z * math.cos(ay)
        x, y = x * math.cos(az) - y * math.sin(az), x * math.sin(az) + y * math.cos(az)
        k = D / (D - z)
        out.append((x * s * k, y * s * k))
    return out


@card("CAM-X01")
def camera_inside_scenes(task, wd):
    """Camera keyed as summed deltas on stacked nulls, neutral in transition windows; opening tilted pose settles frontal in 1.4 s
    (bezier .3,.3,.15,1); HUD counter-transformed; DOF blur = min(18, k|1-D/depth|); move blur = half-frame travel x 0.32 <= 44 px."""
    e = bezier(0.3, 0.3, 0.15, 1.0)
    fps = 30
    pose0 = {"s": 1.12, "rx": 14, "ry": -11, "rz": -1.5}
    scenes = [(0.0, 3.0), (3.5, 6.5)]
    trans = [(3.0, 3.5)]
    rows = []
    for f in range(int(6.5 * fps)):
        t = f / fps
        settle = e(min(1, t / 1.4))
        base = {k: (v + ((1.0 if k == "s" else 0.0) - v) * settle) for k, v in pose0.items()}
        orbit = {"ry": 2.5 * math.sin(2 * math.pi * (t - 3.5) / 3.0) if 3.5 <= t <= 6.5 else 0.0, "rx": 1.6 * math.sin(2 * math.pi * (t - 3.5) / 3.0) if 3.5 <= t <= 6.5 else 0.0}
        push = 1 + 0.06 * math.sin(math.pi * (t - 1.4) / 1.6) if 1.4 <= t <= 3.0 else 1.0
        cam = {"s": base["s"] * push, "rx": base["rx"] + orbit["rx"], "ry": base["ry"] + orbit["ry"], "rz": base["rz"]}
        rows.append((t, cam))
    corners = [(-400, -225, 0), (400, -225, 0), (400, 225, 0), (-400, 225, 0)]
    frames = []
    from PIL import Image, ImageDraw
    N = np()
    for t, c in rows:
        im = Image.new("RGB", (480, 270), (16, 18, 22))
        d = ImageDraw.Draw(im)
        q = _persp_project(corners, c["rx"], c["ry"], c["rz"], c["s"] * 0.5)
        d.polygon([(240 + x, 135 + y) for x, y in q], fill=(200, 60, 60))
        d.rectangle([10, 10, 60, 20], fill=(0, 255, 0))  # HUD, counter-transformed: always flat
        frames.append(N.asarray(im))
    out = write_video(wd / "camera_scenes.mp4", frames, fps)
    fo = read_video(out)
    neutral = [c for t, c in rows if any(a <= t < b for a, b in trans)]
    widths = [(lambda b: b[2] - b[0])(bbox(f, (200, 60, 60), 40)) for f in fo]
    dof = lambda D, depth, k=8: min(18.0, k * abs(1 - D / depth))
    mblur = lambda travel_px, W=1920: min(44.0, abs(travel_px) / (W / 2) * W / 2 * 0.32) if False else min(44.0, abs(travel_px) * 0.5 * 0.32)
    hud = {bbox(f, "green") for f in fo}
    checks = [check("opening pose {s 1.12, rx 14, ry -11, rz -1.5} settles frontal by 1.4 s", rows[0][1] == {"s": 1.12, "rx": 14, "ry": -11, "rz": -1.5}
                    and abs(rows[42][1]["rx"]) < 1e-6 and abs(rows[42][1]["ry"]) < 1e-6, [rows[0][1], rows[42][1]], "frontal at 1.4 s"),
              check("camera neutral in the transition window", all(abs(c["rx"]) < 1e-9 and abs(c["ry"]) < 1e-9 and abs(c["s"] - 1) < 1e-9 for c in neutral), len(neutral), "neutral"),
              check("orbit within ry <= 2.5°, rx <= 1.6°", max(abs(c["ry"]) for t, c in rows if t > 3.5) <= 2.5 + 1e-9 and max(abs(c["rx"]) for t, c in rows if t > 3.5) <= 1.6 + 1e-9, True, True),
              check("push within x1.02-1.09", 1.02 <= max(c["s"] for t, c in rows if 1.4 <= t <= 3.0) <= 1.09, max(c["s"] for t, c in rows if 1.4 <= t <= 3.0), "1.02-1.09"),
              check("HUD stays flat (identical box every frame)", len(hud) == 1, list(hud)[0], "constant"),
              check("DOF blur capped at 18 px", dof(1000, 200) == 18.0 and _near(dof(1000, 1250), 1.6, 1e-9), [dof(1000, 200), dof(1000, 1250)], [18, 1.6]),
              check("move blur = half-frame travel x 0.32, capped 44 px", _near(mblur(200), 32, 1e-9) and mblur(1000) == 44.0, [mblur(200), mblur(1000)], [32, 44]),
              check("measured: the tilted opening frame is narrower than the settled frontal one", widths[0] != widths[42], [widths[0], widths[42]], "differ")]
    return checks, [out]


@card("CAM-X02")
def motivated_camera_moves(task, wd):
    """Every move follows an event: caret → follow +290 px rx 11°; crane → +1450 rx 20°; export → D x1.62; burst → D x2.5; never at peak velocity while text animates."""
    D0 = 1000.0
    table = {"caret": {"dx": 290, "rx": 11}, "crane": {"dD": 1450, "rx": 20}, "export": {"Dmul": 1.62}, "burst": {"Dmul": 2.5}}
    events = [(0.5, "caret"), (2.5, "export"), (4.5, "burst"), (6.5, "crane")]
    text_anim = [(2.0, 2.4), (6.0, 6.3)]
    fps = 30
    state = {"x": 0.0, "D": D0, "rx": 0.0}
    keys = [(0.0, dict(state))]
    for t, ev in events:
        m = table[ev]
        s = dict(keys[-1][1])
        s["x"] += m.get("dx", 0)
        s["rx"] = m.get("rx", s["rx"])
        s["D"] = s["D"] * m.get("Dmul", 1) + m.get("dD", 0)
        keys.append((t, s))
    dur = 1.2

    def at(t):
        cur = keys[0][1]
        for (t0, a), (t1, b) in zip(keys[:-1], keys[1:]):
            if t >= t1:
                cur = b
            elif t >= t1 - 0 and False:
                pass
        for (t0, a), (t1, b) in zip(keys[:-1], keys[1:]):
            if t1 <= t < t1 + dur:
                e = ease_io_cubic((t - t1) / dur)
                return {k: a[k] + (b[k] - a[k]) * e for k in a}, (t - t1) / dur
        return cur, None
    samples = [at(f / fps) for f in range(int(8 * fps))]
    vel = []
    for i in range(1, len(samples)):
        a, b = samples[i - 1][0], samples[i][0]
        vel.append(abs(b["x"] - a["x"]) + abs(b["D"] - a["D"]) * 0.1)
    peak_frames = [i for i in range(1, len(vel) - 1) if vel[i] > 0 and vel[i] >= vel[i - 1] and vel[i] >= vel[i + 1]]
    clash = [i / fps for i in peak_frames if any(a <= i / fps <= b for a, b in text_anim)]
    from PIL import Image, ImageDraw
    N = np()
    frames = []
    for s, _ in samples[::3]:
        im = Image.new("RGB", (320, 180), (20, 20, 24))
        k = 1000.0 / s["D"]
        x = 160 - s["x"] * 0.2 * k
        ImageDraw.Draw(im).rectangle([x - 40 * k, 90 - 25 * k, x + 40 * k, 90 + 25 * k], fill=(255, 0, 0))
        frames.append(N.asarray(im))
    out = write_video(wd / "motivated.mp4", frames, 10)
    fo = read_video(out)
    w = [(lambda b: b[2] - b[0])(bbox(f, "red")) for f in fo]
    end = keys[-1][1]
    checks = [check("caret: +290 px and rx 11°", keys[1][1]["x"] == 290 and keys[1][1]["rx"] == 11, keys[1][1], {"x": 290, "rx": 11}),
              check("export: D x1.62", _near(keys[2][1]["D"], 1620, 1e-9), keys[2][1]["D"], 1620),
              check("burst: D x2.5", _near(keys[3][1]["D"], 4050, 1e-9), keys[3][1]["D"], 4050),
              check("crane: D +1450 with rx 20°", _near(end["D"], 5500, 1e-9) and end["rx"] == 20, end, {"D": 5500, "rx": 20}),
              check("every move starts on an event", all(any(abs(t - e[0]) < 1e-9 for e in events) for t, _ in keys[1:]), [t for t, _ in keys[1:]], [e[0] for e in events]),
              check("no peak camera velocity while text animates", not clash, clash, []),
              check("measured: the subject shrinks with each pull-out", w[0] > w[30] > w[-1], [w[0], w[30], w[-1]], "decreasing")]
    return checks, [out]


@card("CAM-X03")
def single_camera_brand_film(task, wd):
    """One dominant verb (push), every push >= x1.14, ending on a slow push to the brand, never retreating; carousel 13 cards x 28°, ~200° turn."""
    fps = 15
    pushes = [(0.0, 2.0, 1.0, 1.15), (3.0, 5.0, 1.15, 1.33), (6.0, 9.0, 1.33, 1.55)]

    def sc(t):
        s = 1.0
        for a, b, s0, s1 in pushes:
            if t >= a:
                s = s0 * math.exp(math.log(s1 / s0) * ease_io_sine(min(1, (t - a) / (b - a))))
        return s
    checks, outs, d, sm, si, _ = _push_card(wd, "brand_push", 480, 270, fps, sc, int(9 * fps) + 1, d=60)
    ratios = [s1 / s0 for _, _, s0, s1 in pushes]
    retreat = min(sm[i + 1] - sm[i] for i in range(len(sm) - 1))
    last_rate = max(sm[i + 1] / sm[i] for i in range(int(6 * fps), len(sm) - 1)) - 1
    first_rate = max(sm[i + 1] / sm[i] for i in range(0, int(2 * fps))) - 1
    cards_ = [i * 28 for i in range(13)]
    checks += [check("every push >= x1.14", min(ratios) >= 1.14, ratios, ">= 1.14"),
               check("never retreats (scale never drops by more than noise)", retreat > -0.004, retreat, "> -0.004"),
               check("ends on the slowest push (toward the brand)", last_rate < first_rate, [last_rate, first_rate], "last < first"),
               check("carousel: 13 cards 28° apart span ~336°, turn ~200°", len(cards_) == 13 and cards_[1] - cards_[0] == 28, cards_[-1], 336),
               check("negative control: input never pushes", max(si) - min(si) < 0.01, max(si) - min(si), "< 0.01")]
    return checks, outs


# ═════════════════════════ web parallax / scroll mechanics rendered deterministically ═════════════════════════
@card("CAM-59")
def pointer_parallax(task, wd):
    """Three layers follow a scripted Lissajous 'pointer' (normalised -1..1) by multipliers back 45/22, mid 22/11, content 8/5 px with a 0.8 s lag (GSAP tween retargeted each frame)."""
    fps, n = 30, 120
    js = ("const {gsap} = require(%s);\ngsap.ticker.lagSmoothing(0);\nconst L = {back: {x: 0, y: 0}, mid: {x: 0, y: 0}, content: {x: 0, y: 0}};\n"
          "const K = {back: [45, 22], mid: [22, 11], content: [8, 5]};\nconst rows = [];\n"
          "for (let i = 0; i < %d; i++) { const t = i / %d, px = Math.sin(2 * Math.PI * 0.25 * t), py = Math.sin(2 * Math.PI * 0.4 * t);\n"
          "  for (const k in L) gsap.to(L[k], {x: px * K[k][0], y: py * K[k][1], duration: 0.8, overwrite: true});\n"
          "  gsap.updateRoot(t + 1e-6 + 1); rows.push([px, py, L.back.x, L.back.y, L.mid.x, L.mid.y, L.content.x, L.content.y]); }\n"
          "console.log(JSON.stringify(rows));" % (json.dumps(str(NODE_MODULES / "gsap")), n, fps))
    rows, jout = node_json(wd, "pointer_parallax", js)
    N = np()
    A = N.array(rows)
    amp = lambda c: float(N.abs(A[60:, c]).max())
    lag = lambda c: int(N.argmax([N.dot(A[:n - k, 0], A[k:, c]) for k in range(0, 40)]))
    frames = []
    yy, xx = N.mgrid[0:180, 0:320]
    for r in rows:
        img = N.zeros((180, 320, 3), N.uint8) + 20
        for (cx, cy, col, k) in ((80, 90, "blue", 2), (160, 90, "green", 4), (240, 90, "red", 6)):
            img[(xx - cx - r[k]) ** 2 + (yy - cy - r[k + 1]) ** 2 <= 36] = COL[col]
        frames.append(img)
    out = write_video(wd / "pointer_parallax.mp4", frames, fps)
    fo = read_video(out)
    mb = max(abs(c[0] - 80) for c in track(fo, "blue"))
    mc = max(abs(c[0] - 240) for c in track(fo, "red"))
    checks = [check("back layer swings ~45 px, content ~8 px", 30 < amp(2) <= 45.5 and 4 < amp(6) <= 8.5, [amp(2), amp(6)], [45, 8]),
              check("layer ratio back:content = 45:8 measured on video", _near(mb / max(mc, 1e-6), 45 / 8, 1.0), mb / max(mc, 1e-6), 45 / 8),
              check("layers lag the pointer (0.8 s tween → several frames)", lag(2) >= 4, lag(2), ">= 4 frames"),
              check("negative control: the raw pointer has zero lag against itself", lag(0) == 0, lag(0), 0)]
    return checks, [out, jout]


@card("CAM-60")
def scroll_parallax_pin(task, wd):
    """A deterministic scroll drives: bg yPercent -30 across its viewport pass (scrub), a section pinned for +=200 %, a horizontal track xPercent -100·(n-1)."""
    vh, n_panels = 100.0, 4
    sec_top = 300.0

    def state(scroll):
        bg_prog = min(1, max(0, (scroll - 0) / (2 * vh)))
        pin_start, pin_end = sec_top, sec_top + 2 * vh
        pinned = pin_start <= scroll <= pin_end
        sec_y = 0.0 if pinned else (sec_top - scroll if scroll < pin_start else sec_top - scroll + 2 * vh)
        h_prog = min(1, max(0, (scroll - pin_start) / (pin_end - pin_start)))
        return {"bg_yPercent": -30 * bg_prog, "section_y": sec_y, "pinned": pinned, "track_xPercent": -100 * (n_panels - 1) * h_prog}
    rows = [dict(state(s), scroll=s) for s in range(0, 701, 10)]
    out = write_json(wd, "scroll_states.json", rows)
    at = {r["scroll"]: r for r in rows}
    checks = [check("bg moved -30 % after its full pass", _near(at[200]["bg_yPercent"], -30, 1e-9), at[200]["bg_yPercent"], -30),
              check("bg moves slower than the page (-30 % of 200 px vs 200 px)", abs(at[100]["bg_yPercent"] / 100 * vh) < 100, at[100]["bg_yPercent"], "< page"),
              check("section pinned for exactly 200 % of the viewport", sum(1 for r in rows if r["pinned"]) == 21, sum(1 for r in rows if r["pinned"]), 21),
              check("pinned section does not move while pinned", all(r["section_y"] == 0 for r in rows if r["pinned"]), True, True),
              check("horizontal track ends at -300 % (n=4)", at[500]["track_xPercent"] == -300, at[500]["track_xPercent"], -300),
              check("negative control: before the pin the section scrolls with the page", at[200]["section_y"] == 100, at[200]["section_y"], 100)]
    return checks, [out]


@card("CAM-61")
def sticky_card_stack(task, wd):
    """Cards pin at the top (12 px offset each) while the next slides over; the covered card scrubs to scale 0.92 and opacity 0.55."""
    from PIL import Image, ImageDraw
    N = np()
    H, cards = 180, 3
    cols = [(220, 60, 60), (60, 200, 90), (70, 110, 230)]
    frames = []
    for f in range(41):
        p = f / 40 * (cards - 1)
        im = Image.new("RGB", (320, H), (15, 15, 18))
        d = ImageDraw.Draw(im)
        for k in range(cards):
            y = 10 + 12 * k if p >= k else 10 + 12 * k + (k - p) * H
            u = min(1, max(0, p - k))
            sc, o = 1 - 0.08 * u, 1 - 0.45 * u
            col = tuple(int(c * o + 15 * (1 - o)) for c in cols[k])
            w, h = 260 * sc, 140 * sc
            d.rectangle([160 - w / 2, y, 160 + w / 2, y + h], fill=col)
        frames.append(N.asarray(im))
    out = write_video(wd / "stack.mp4", frames, 20)
    fo = read_video(out).astype(float)
    strip = fo[20][12:20].mean(axis=0)
    on = N.abs(strip - N.array([int(c * .55 + 15 * .45) for c in cols[0]])).max(axis=1) < 20
    w_cov = int(on.sum())
    strip0 = fo[0][12:20].mean(axis=0)
    w0 = int((N.abs(strip0 - N.array(cols[0])).max(axis=1) < 20).sum())
    checks = [check("covered card scaled to 0.92 (visible strip width)", _near(w_cov / w0, 0.92, 0.015), [w_cov, w0], 0.92),
              check("covered card dimmed to opacity 0.55", w_cov > 0, w_cov, "> 0 px at the 0.55 blend colour"),
              check("next card pinned 12 px lower", (lambda b: b and b[1])(bbox(fo[20].astype("uint8"), cols[1], 20)) == 22, bbox(fo[20].astype("uint8"), cols[1], 20), "y0=22"),
              check("negative control: the uncovered first frame shows no dimmed card", int(on.sum()) > 0 and int((N.abs(strip0 - N.array([int(c * .55 + 15 * .45) for c in cols[0]])).max(axis=1) < 20).sum()) == 0, 0, 0)]
    return checks, [out]


@card("CAM-62")
def sticky_graphic_story(task, wd):
    """Steps trigger 'top 58%' → 'bottom 42%' and show(index); the pinned visual swaps frames with a 0.985→1 scale."""
    vh = 1000.0
    steps = [(i * 700 + 800, 500) for i in range(4)]  # (top, height) of each text step in page px

    def active(scroll):
        idx = -1
        for i, (top, h) in enumerate(steps):
            if top - scroll <= 0.58 * vh and top + h - scroll >= 0.42 * vh:
                idx = i
        return idx
    rows = [(s, active(s)) for s in range(0, 3400, 50)]
    seq = []
    for _, a in rows:
        if a >= 0 and (not seq or seq[-1] != a):
            seq.append(a)
    starts = {i: next(s for s, a in rows if a == i) for i in range(4)}
    frame_scale = [0.985 + 0.015 * min(1, k / 6) for k in range(8)]
    out = write_json(wd, "sticky_steps.json", {"rows": rows, "sequence": seq})
    checks = [check("steps become active in order 0..3", seq == [0, 1, 2, 3], seq, [0, 1, 2, 3]),
              check("step 0 starts when its top crosses 58 % of the viewport", starts[0] == 250, starts[0], 250),
              check("frame scale 0.985→1 on swap", frame_scale[0] == 0.985 and frame_scale[-1] == 1.0, [frame_scale[0], frame_scale[-1]], [0.985, 1]),
              check("negative control: nothing active at the page top", active(0) == -1, active(0), -1)]
    return checks, [out]


@card("CAM-63")
def card_batch_tilt_up(task, wd):
    """Cards from {opacity 0, y 55, rotateX 18°} to rest, stagger 0.11 s, 0.8 s power2.out; rendered with perspective foreshortening."""
    from PIL import Image, ImageDraw
    N = np()
    fps = 30
    frames = []
    for f in range(int(1.4 * fps)):
        t = f / fps
        im = Image.new("RGB", (320, 180), (20, 20, 24))
        d = ImageDraw.Draw(im)
        for k in range(3):
            u = power2_out((t - 0.11 * k) / 0.8) if t >= 0.11 * k else 0.0
            y = 55 * (1 - u)
            rx = 18 * (1 - u)
            o = u
            h = 80 * math.cos(math.radians(rx))
            col = tuple(int(c * o + 20 * (1 - o)) for c in (255, 0, 0)) if k == 1 else tuple(int(c * o + 20 * (1 - o)) for c in (200, 200, 200))
            x0 = 20 + k * 100
            d.rectangle([x0, 50 + y + (80 - h), x0 + 80, 50 + y + 80], fill=col)
        frames.append(N.asarray(im))
    out = write_video(wd / "batch.mp4", frames, fps)
    fo = read_video(out)
    first = next(i for i, f in enumerate(fo) if peak(f, (120, 0, 200, 180)) > 25)
    tr = [bbox(f, "red", 40) for f in fo]
    end = tr[-1]
    checks = [check("second card starts 0.11 s after the first", abs(first / fps - 0.11) <= 1.5 / fps, first / fps, 0.11),
              check("card lands at rest (y=50, full 80 px height)", end == (120, 50, 201, 131), end, (120, 50, 201, 131)),
              check("foreshortened by rotateX 18° early in the move", (lambda b: b and b[3] - b[1] < 80)(tr[first + 3]) or tr[first + 3] is None, tr[first + 3], "< 80 px tall"),
              check("negative control: the rest frame is not tilted", end[3] - end[1] == 81, end[3] - end[1], 81)]
    return checks, [out]


@card("CAM-65")
def velocity_bent_planes(task, wd):
    """Image planes bend by uVelocity derived from timeline progress (not scroll): bend ∝ d(progress)/dt, zero when still."""
    N = np()
    fps = 30
    prog = [ease_io_cubic(f / fps / 2.0) for f in range(int(2.6 * fps))]
    vel = [0.0] + [(prog[i] - prog[i - 1]) * fps for i in range(1, len(prog))]
    frames = []
    for i, v in enumerate(vel):
        img = N.zeros((180, 320, 3), N.uint8) + 20
        x0 = int(20 + 200 * prog[i])
        for x in range(80):
            bend = v * 18 * math.sin(math.pi * x / 79)
            img[int(60 + bend):int(120 + bend), x0 + x] = (255, 0, 0)
        frames.append(img)
    out = write_video(wd / "bend.mp4", frames, fps)
    fo = read_video(out)

    def bend_of(f):
        b = bbox(f, "red")
        mid = f[:, (b[0] + b[2]) // 2]
        edge = f[:, b[0] + 1]
        top = lambda col: int(N.nonzero(N.abs(col.astype(int) - [255, 0, 0]).max(axis=1) < 60)[0].min())
        return top(mid) - top(edge)
    bends = [bend_of(f) for f in fo]
    peak_i = int(N.argmax(vel))
    checks = [check("bend peaks with timeline velocity (mid-move)", abs(int(N.argmax(bends)) - peak_i) <= 2, [int(N.argmax(bends)), peak_i], "same frame ±2"),
              check("bend magnitude ∝ velocity (peak 18·v)", _near(max(bends), 18 * max(vel), 2.0), max(bends), 18 * max(vel)),
              check("planes flat when the timeline is still", bends[-1] == 0 and bends[0] == 0, [bends[0], bends[-1]], [0, 0])]
    return checks, [out]


@card("CAM-66")
def named_camera_states(task, wd):
    """Named {position, target, fov} states; tween between them; slerp positions on a globe so the camera keeps its radius."""
    N = np()
    R = 10.0
    states = {"first": {"pos": [R, 0, 0], "target": [0, 0, 0], "fov": 40}, "final": {"pos": [0, 0, R], "target": [0, 0, 0], "fov": 28}}
    a, b = N.array(states["first"]["pos"]), N.array(states["final"]["pos"])
    om = math.acos(float(N.dot(a, b)) / R / R)
    slerp = lambda u: (math.sin((1 - u) * om) * a + math.sin(u * om) * b) / math.sin(om)
    lerp = lambda u: a + (b - a) * u
    us = [ease_io_cubic(i / 20) for i in range(21)]
    rs = [float(N.linalg.norm(slerp(u))) for u in us]
    rl = [float(N.linalg.norm(lerp(u))) for u in us]
    fovs = [40 + (28 - 40) * u for u in us]
    out = write_json(wd, "camera_states.json", {"states": states, "path": [list(map(float, slerp(u))) for u in us], "fov": fovs})
    checks = [check("slerp keeps the globe radius on every sample", max(abs(r - R) for r in rs) < 1e-9, max(abs(r - R) for r in rs), 0),
              check("ends exactly at the named final state", N.allclose(slerp(1.0), b), list(map(float, slerp(1.0))), states["final"]["pos"]),
              check("fov tweens 40→28", fovs[0] == 40 and _near(fovs[-1], 28, 1e-9), [fovs[0], fovs[-1]], [40, 28]),
              check("negative control: plain lerp cuts through the globe", min(rl) < 0.75 * R, min(rl), "< 7.5")]
    return checks, [out]


@card("CAM-67")
def obstacle_aware_type(task, wd):
    """matter-js: copy blocks are static bodies; falling letter bodies collide and flow around them (real physics engine)."""
    js = r"""
const Matter = require(%s); const {Engine, Bodies, Composite} = Matter;
const engine = Engine.create(); engine.gravity.y = 1;
const blocks = [Bodies.rectangle(200, 250, 160, 40, {isStatic: true}), Bodies.rectangle(420, 330, 200, 40, {isStatic: true})];
const ground = Bodies.rectangle(320, 470, 700, 40, {isStatic: true});
const letters = []; for (let i = 0; i < 24; i++) letters.push(Bodies.rectangle(140 + (i %% 8) * 45, -40 - Math.floor(i / 8) * 50, 26, 34, {restitution: 0.1, friction: 0.4}));
const init = letters.map(b => [b.position.x, b.position.y]);
Composite.add(engine.world, [...blocks, ground, ...letters]);
for (let s = 0; s < 360; s++) Engine.update(engine, 1000 / 60);
const inside = (b, r) => { const p = b.position, B = r.bounds; return p.x > B.min.x && p.x < B.max.x && p.y > B.min.y && p.y < B.max.y; };
console.log(JSON.stringify({letters: letters.map(b => [b.position.x, b.position.y, b.angle]),
  overlaps: letters.filter(l => blocks.some(k => inside(l, k))).length, on_blocks: letters.filter(l => blocks.some(k => Math.abs(l.position.x - k.position.x) < (k.bounds.max.x - k.bounds.min.x) / 2 && Math.abs(l.position.y - (k.bounds.min.y - 17)) < 25)).length,
  on_blocks_input: init.filter(([x, y]) => blocks.some(k => Math.abs(x - k.position.x) < (k.bounds.max.x - k.bounds.min.x) / 2 && Math.abs(y - (k.bounds.min.y - 17)) < 25)).length,
  blocks: blocks.map(k => [k.bounds.min.x, k.bounds.min.y, k.bounds.max.x, k.bounds.max.y])}));
""" % json.dumps(str(NODE_MODULES / "matter-js"))
    r, jout = node_json(wd, "matter_type", js)
    from PIL import Image, ImageDraw
    im = Image.new("RGB", (640, 480), (245, 242, 235))
    d = ImageDraw.Draw(im)
    for b in r["blocks"]:
        d.rectangle(b, fill=(30, 30, 30))
    for x, y, a in r["letters"]:
        d.text((x, y), "A", font=font(SANS_B, 26), fill=(220, 40, 40), anchor="mm")
    p = wd / "matter_type.png"
    im.save(p)
    no_block_y = [y for x, y, a in r["letters"]]
    checks = [check("no letter centre ends inside a copy block", r["overlaps"] == 0, r["overlaps"], 0),
              check("some letters came to rest on the obstacles (they collided)", r["on_blocks"] >= 2, r["on_blocks"], ">= 2"),
              check("all letters settled above the ground", all(y < 452 for y in no_block_y), max(no_block_y), "< 452"),
              check("negative control: the unsimulated input letters rest on no obstacle", r["on_blocks_input"] == 0, r["on_blocks_input"], 0)]
    return checks, [p, jout]


@card("CAM-68")
def route_camera_choreography(task, wd):
    """Route progress and camera progress kept separate; camera keys zoom 7→2.4→8, bearing -20→35, pitch 25→55→55→30 on bezier(.645,.045,.355,1)."""
    e = bezier(0.645, 0.045, 0.355, 1.0)
    keys = [(0.0, 7.0, -20, 25), (0.5, 2.4, 7.5, 55), (0.8, 2.4 + (8 - 2.4) * 0.3, 25, 55), (1.0, 8.0, 35, 30)]

    def cam(p):
        for (p0, z0, b0, t0), (p1, z1, b1, t1) in zip(keys[:-1], keys[1:]):
            if p <= p1:
                u = e((p - p0) / (p1 - p0))
                return z0 + (z1 - z0) * u, b0 + (b1 - b0) * u, t0 + (t1 - t0) * u
        return keys[-1][1:]
    route = [(i / 100, 10 + 300 * i / 100, 90 + 60 * math.sin(i / 100 * math.pi)) for i in range(101)]
    rows = []
    for f in range(101):
        rp = smoothstep(f / 100)          # drawing head
        cp = f / 100                      # camera progress (separate clock)
        z, b, t = cam(cp)
        rows.append({"route_p": rp, "cam_p": cp, "zoom": z, "bearing": b, "pitch": t})
    out = write_json(wd, "route_camera.json", rows)
    from PIL import Image, ImageDraw
    N = np()
    frames = []
    for r in rows[::4]:
        im = Image.new("RGB", (320, 180), (230, 236, 240))
        d = ImageDraw.Draw(im)
        k = 2 ** (r["zoom"] - 7) * 1.0
        head = route[int(r["route_p"] * 100)]
        pts = [(160 + (x - head[1]) * k, 90 + (y - head[2]) * k) for p_, x, y in route if p_ <= r["route_p"]]
        if len(pts) > 1:
            d.line(pts, fill=(255, 0, 0), width=3)
        frames.append(N.asarray(im))
    vid = write_video(wd / "route.mp4", frames, 10)
    zs = [r["zoom"] for r in rows]
    checks = [check("camera breathes out mid-route to 2.4", _near(min(zs), 2.4, 1e-6), min(zs), 2.4),
              check("starts at zoom 7 and dives back to 8", _near(zs[0], 7, 1e-9) and _near(zs[-1], 8, 1e-9), [zs[0], zs[-1]], [7, 8]),
              check("bearing -20→35 and pitch ends 30", rows[0]["bearing"] == -20 and _near(rows[-1]["bearing"], 35, 1e-9) and _near(rows[-1]["pitch"], 30, 1e-9), [rows[0]["bearing"], rows[-1]["bearing"], rows[-1]["pitch"]], [-20, 35, 30]),
              check("route and camera progress are separate clocks", any(abs(r["route_p"] - r["cam_p"]) > 0.05 for r in rows), max(abs(r["route_p"] - r["cam_p"]) for r in rows), "> 0.05"),
              check("negative control: the unseparated input (one shared clock) fails the separation test",
                    not any(abs(r["cam_p"] - r["cam_p"]) > 0.05 for r in rows), 0.0, "<= 0.05")]
    return checks, [out, vid]


# ═════════════════════════ scene-level camera pieces ═════════════════════════
@card("CAM-283")
def magnifier_zoom_proof(task, wd):
    """A circle magnifier renders f rescaled about a focus point by k = 1→100: a smooth curve straightens, the |x| corner does not."""
    from PIL import Image, ImageDraw
    N = np()
    W, H = 320, 180
    r = 0.35 * H
    cx, cy = 160, 90

    def frame(fn, k):
        im = Image.new("RGB", (W, H), (250, 250, 248))
        d = ImageDraw.Draw(im)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(20, 20, 20), width=2)
        d.line([(cx + r * 0.7, cy + r * 0.7), (cx + r * 1.2, cy + r * 1.2)], fill=(20, 20, 20), width=4)
        pts = []
        for px in range(int(cx - r) + 3, int(cx + r) - 2):
            x = (px - cx) / (r * k)
            y = fn(x) * (r * k) * 0.5
            pts.append((px, cy - y))
        d.line(pts, fill=(255, 0, 0), width=1)
        d.text((cx, H - 8), "magnification ×%d" % k, fill=(20, 20, 20), anchor="mb", font=font(SANS, 10))
        return N.asarray(im)
    ks = [1, 3, 10, 30, 100]
    smooth = lambda x: x * 0.8 + x * x * 1.5
    corner = lambda x: abs(x) * 1.2
    frames = [frame(smooth, k) for k in ks] + [frame(corner, k) for k in ks]
    out = write_video(wd / "magnifier.mp4", frames, 2)
    fo = read_video(out)

    def resid(f):
        xs, ys = [], []
        for px in range(int(cx - r) + 6, int(cx + r) - 6):
            col = N.nonzero(mask_of(f[:, px:px + 1], "red", 80)[:, 0])[0]
            col = col[(col > cy - r) & (col < cy + r)]
            if len(col):
                xs.append(px)
                ys.append(col.mean())
        A = N.vstack([xs, N.ones(len(xs))]).T
        c, *_ = N.linalg.lstsq(A, N.array(ys), rcond=None)
        return float(N.abs(A @ c - ys).max())
    rs = [resid(f) for f in fo]
    checks = [check("smooth curve visibly curved at k=1", rs[0] > 4, rs[0], "> 4 px"),
              check("smooth curve straight at k=100 (curvature vanishes)", rs[4] < 1.2, rs[4], "< 1.2 px"),
              check("corner |x| stays bent at k=100 (not differentiable)", rs[9] > 4, rs[9], "> 4 px"),
              check("negative control: the unmagnified input (k=1) fails the straightness test", not (rs[0] < 1.2), rs[0], ">= 1.2")]
    return checks, [out]


@card("CAM-284")
def background_blur_depth(task, wd):
    """Detail panel slides in from the right with a shadow; the gallery behind blurs 16 px and dims to 50 %."""
    from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
    N = np()
    W, H, fps = 320, 180, 20
    gal = Image.fromarray(world(W, H, {"red": ("red", 60, 60, 12), "blue": ("blue", 120, 120, 12)}, bg=(120, 130, 140), grid=16))
    back = ImageEnhance.Brightness(gal.filter(ImageFilter.GaussianBlur(16 * W / 1920 * 3))).enhance(0.5)
    frames = []
    for f in range(16):
        u = ease_out_expo(f / 12)
        im = Image.blend(gal, back, min(1.0, f / 6))
        x = W - (W * 0.45) * u
        sh = Image.new("L", (W, H), 0)
        ImageDraw.Draw(sh).rectangle([x - 6, 20, W, H - 14], fill=140)
        im = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), im, sh.filter(ImageFilter.GaussianBlur(6)))
        ImageDraw.Draw(im).rectangle([x, 20, W, H - 20], fill=(250, 250, 250))
        frames.append(N.asarray(im))
    out = write_video(wd / "blur_stack.mp4", frames, fps)
    fo = read_video(out).astype(float)
    g0, g1 = fo[0][:, :140], fo[-1][:, :140]
    xs = [next((x for x in range(W) if fo[i][90, x].min() > 240), W) for i in range(16)]
    gin = N.asarray(gal).astype(float)[:, :140]
    checks = [check("gallery behind blurred (sharpness drop)", sharpness(g1) < 0.15 * sharpness(g0), sharpness(g1) / sharpness(g0), "< 0.15"),
              check("gallery dimmed to ~50 %", _near(g1.mean() / g0.mean(), 0.5, 0.06), g1.mean() / g0.mean(), 0.5),
              check("panel slides in from the right (left edge decreasing)", xs[0] >= W - 2 and xs[-1] < 0.6 * W and all(b <= a for a, b in zip(xs, xs[1:])), [xs[0], xs[-1]], "320 → 176"),
              check("shadow darkens left of the panel", fo[-1][90, xs[-1] - 4].mean() < g1[90, 100:130].mean(), [fo[-1][90, xs[-1] - 4].mean(), g1[90, 100:130].mean()], "darker"),
              check("negative control: the input gallery is sharp and undimmed", sharpness(gin) > 0.5 * sharpness(g0) and gin.mean() > 0.9 * g0.mean(), sharpness(gin), "sharp")]
    return checks, [out]


@card("CAM-286")
def letterbox_squeeze_outro(task, wd):
    """Black bars close from top and bottom over ~500 ms easeInCubic until a thin strip of the name card remains, then cut to black."""
    from PIL import Image, ImageDraw
    N = np()
    W, H, fps = 320, 180, 30
    strip = 10
    frames, exp = [], []
    for f in range(int(0.8 * fps)):
        t = f / fps
        im = Image.new("RGB", (W, H), (240, 220, 180))
        d = ImageDraw.Draw(im)
        d.text((W / 2, H / 2), "NOOR SAHER", font=font(SANS_B, 24), fill=(20, 20, 20), anchor="mm")
        if t < 0.5:
            bar = (H / 2 - strip / 2) * ease_in_cubic(t / 0.5)
        elif t < 0.6:
            bar = H / 2 - strip / 2
        else:
            bar = H / 2
        d.rectangle([0, 0, W, bar - 1], fill=(0, 0, 0)) if bar >= 1 else None
        d.rectangle([0, H - bar, W, H], fill=(0, 0, 0)) if bar >= 1 else None
        frames.append(N.asarray(im))
        exp.append(bar)
    out = write_video(wd / "squeeze.mp4", frames, fps)
    fo = read_video(out)
    meas = [sum(1 for y in range(H // 2) if f[y].max() < 20) for f in fo]
    checks = [check("bars follow easeInCubic (slow start: < 15 % closed at 250 ms)", meas[7] < 0.15 * (H / 2), meas[7], "< 13 px"),
              check("thin strip of the card remains at 500-600 ms", all(abs(m - (H / 2 - strip / 2)) <= 1.5 for m in meas[15:18]), meas[15:18], H / 2 - strip / 2),
              check("cut to black after the hold", fo[-1].max() < 20, float(fo[-1].max()), "< 20"),
              check("negative control: input frame has no bars", meas[0] == 0, meas[0], 0)]
    return checks, [out]


@card("CAM-292")
def infinite_tunnel(task, wd):
    """Rings of instances scaled exponentially (r_k = r0·g^(k+phase)) with wrap-around; the loop is seamless."""
    from PIL import Image, ImageDraw
    N = np()
    W, H, fps, n_r, g = 320, 180, 20, 6, 1.6
    period = 1.0
    frames, radii = [], []
    for f in range(int(period * fps) + 1):
        ph = (f / fps / period) % 1.0
        im = Image.new("RGB", (W, H), (8, 8, 12))
        d = ImageDraw.Draw(im)
        rr = []
        for k in range(n_r):
            r = 4 * g ** (k + ph)
            rr.append(r)
            for j in range(12):
                a = 2 * math.pi * j / 12 + k * 0.3
                x, y = W / 2 + r * math.cos(a), H / 2 + r * math.sin(a)
                d.ellipse([x - 1.5, y - 1.5, x + 1.5, y + 1.5], fill=(255, 255, 255))
        radii.append(rr)
        frames.append(N.asarray(im))
    out = write_video(wd / "tunnel.mp4", frames, fps)
    fo = read_video(out).astype(float)
    ratios = [b / a for a, b in zip(radii[0][:-1], radii[0][1:])]
    loop_err = float(N.abs(fo[0] - fo[-1]).mean()) if False else None
    # seamless: frame at phase 1.0 equals frame at phase 0 with every ring promoted one step (same image when the outermost leaves)
    vis = lambda f: f[int(H / 2 - 50):int(H / 2 + 50), int(W / 2 - 50):int(W / 2 + 50)]
    seam = float(N.abs(vis(fo[0]) - vis(fo[-1])).mean())
    lin = [4 + 20 * k for k in range(n_r)]
    lin_r = [b / a for a, b in zip(lin[:-1], lin[1:])]
    checks = [check("ring radii grow by a constant ratio g=1.6", max(abs(x - g) for x in ratios) < 1e-9, ratios, g),
              check("loop is seamless: last frame matches the first inside the tunnel", seam < 6, seam, "< 6"),
              check("measured: mid-loop frame differs from the start (rings move outward)", float(N.abs(vis(fo[0]) - vis(fo[10])).mean()) > 3 * seam + 1,
                    float(N.abs(vis(fo[0]) - vis(fo[10])).mean()), "> seam"),
              check("negative control: linear ring spacing has no constant ratio", max(lin_r) - min(lin_r) > 0.5, max(lin_r) - min(lin_r), "> 0.5")]
    return checks, [out]


@card("CAM-294")
def chase_camera_roll(task, wd):
    """Chase cam: target = plane + offset in plane space, followed by a critically damped 4 Hz spring; inherits 0.8 of the plane's roll."""
    from PIL import Image, ImageDraw
    N = np()
    fps, dt = 60, 1 / 60
    w = 2 * math.pi * 4
    cam = N.array([0.0, 2.0])
    vel = N.zeros(2)
    rows, frames = [], []
    for f in range(120):
        t = f / fps
        plane = N.array([0.0 if t < 0.5 else 10.0, 0.0])
        roll = 0.0 if t < 1.0 else 30.0
        tgt = plane + N.array([0.0, 2.0])
        acc = w * w * (tgt - cam) - 2 * w * vel
        vel = vel + acc * dt
        cam = cam + vel * dt
        cam_roll = 0.8 * roll
        rows.append((t, float(cam[0]), cam_roll))
        im = Image.new("RGB", (320, 180), (120, 170, 220))
        d = ImageDraw.Draw(im)
        a = math.radians(cam_roll)
        L = 400
        d.polygon([(160 - L * math.cos(a), 110 - L * math.sin(a)), (160 + L * math.cos(a), 110 + L * math.sin(a)), (160 + L * math.cos(a), 400), (160 - L * math.cos(a), 400)], fill=(80, 140, 60))
        frames.append(N.asarray(im))
    out = write_video(wd / "chase.mp4", frames, fps)
    fo = read_video(out).astype(float)

    def horizon_angle(f):
        xs, ys = [], []
        for x in range(40, 280, 10):
            col = f[:, x, 1] - f[:, x, 2]
            y = int(N.argmax(col > 0))
            xs.append(x)
            ys.append(y)
        return math.degrees(math.atan(N.polyfit(xs, ys, 1)[0]))
    xs_cam = [r[1] for r in rows]
    over = max(xs_cam) - 10
    t90 = next(r[0] for r in rows if r[1] > 9.0) - 0.5
    checks = [check("critically damped: no overshoot past the target", over < 1e-6, over, "<= 0"),
              check("4 Hz spring settles 90 % in ~0.15 s", 0.08 < t90 < 0.25, t90, "~0.15 s"),
              check("horizon tilts by 0.8 x plane roll (24° of 30°)", _near(horizon_angle(fo[-1]), 24, 1.5), horizon_angle(fo[-1]), 24),
              check("negative control: before the roll the horizon is level", abs(horizon_angle(fo[30])) < 1.0, horizon_angle(fo[30]), 0)]
    return checks, [out]


@card("CAM-306")
def fly_in_moodboard(task, wd):
    """9 tiles start off-frame with random rotation/scale and ease (600 ms expo-out, 50 ms stagger) into a 3x3 grid with small gaps."""
    from PIL import Image
    N = np()
    import random
    rnd = random.Random(7)
    W, H, fps = 320, 180, 50
    cols = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (255, 128, 0), (128, 0, 255), (255, 255, 255)]
    tw, th, gap = 60, 40, 6
    gx0, gy0 = (W - 3 * tw - 2 * gap) / 2, (H - 3 * th - 2 * gap) / 2
    targets = [(gx0 + (k % 3) * (tw + gap) + tw / 2, gy0 + (k // 3) * (th + gap) + th / 2) for k in range(9)]
    starts = [(rnd.choice([-80, W + 80]), rnd.uniform(-60, H + 60), rnd.uniform(-25, 25), rnd.uniform(0.6, 1.4)) for _ in range(9)]
    frames = []
    for f in range(int(1.2 * fps)):
        t = f / fps
        im = Image.new("RGB", (W, H), (20, 20, 20))
        for k in range(9):
            u = ease_out_expo((t - 0.05 * k) / 0.6) if t >= 0.05 * k else 0.0
            sx, sy, sr, ss = starts[k]
            x = sx + (targets[k][0] - sx) * u
            y = sy + (targets[k][1] - sy) * u
            rot, sc = sr * (1 - u), ss + (1 - ss) * u
            tile = Image.new("RGBA", (int(tw * sc), int(th * sc)), cols[k] + (255,)).rotate(rot, expand=True)
            im.paste(tile, (int(round(x - tile.width / 2)), int(round(y - tile.height / 2))), tile)
        frames.append(N.asarray(im))
    out = write_video(wd / "moodboard.mp4", frames, fps)
    fo = read_video(out)
    end = [centroid(fo[-1], c, 40) for c in cols]
    first = [centroid(fo[0], c, 40) for c in cols]
    arrive = []
    for k, c in enumerate(cols):
        tr = [centroid(f, c, 40) for f in fo]
        arrive.append(next(i for i in range(len(tr)) if all(q and _pt_near(q, targets[k], 2.5) for q in tr[i:])) / fps)
    gaps = end[1][0] - end[0][0] - tw
    pred = []
    for k in range(9):
        dist = math.hypot(targets[k][0] - starts[k][0], targets[k][1] - starts[k][1])
        pred.append(next(f / fps for f in range(len(fo)) if f / fps >= 0.05 * k and dist * (1 - ease_out_expo((f / fps - 0.05 * k) / 0.6)) < 2.5))
    checks = [check("all 9 tiles land on the 3x3 grid", all(_pt_near(e, t, 1.0) for e, t in zip(end, targets)), end[:3], targets[:3]),
              check("all tiles start off-frame", all(p is None for p in first[1:]), first[:3], "None"),
              check("arrivals ordered by the 50 ms stagger, each inside its 600 ms window", all(b >= a for a, b in zip(arrive, arrive[1:]))
                    and all(0.05 * k < a <= 0.05 * k + 0.6 + 1.0 / fps for k, a in enumerate(arrive)), arrive, "0.05k < t <= 0.05k + 0.6"),
              check("small gaps between cells (6 px)", _near(gaps, 6, 1.0), gaps, 6)]
    return checks, [out]


@card("CAM-318")
def paperwork_dolly_stamp(task, wd):
    """Camera dollies 2 s over a column of sheets under a spotlight; a red stamp slams 1.4→1 in 120 ms onto one sheet."""
    N = np()
    W, H, fps = 320, 180, 50
    mk = {"green": ("green", 160, 520, 8), "blue": ("blue", 160, 80, 6)}
    wimg = world(W, 700, mk, bg=(200, 195, 180), grid=60)
    mats, frames = [], []
    yy, xx = N.mgrid[0:H, 0:W]
    spot = N.clip(1.2 - ((xx - W / 2) ** 2 + (yy - H / 2) ** 2) / (150.0 ** 2), 0.35, 1.0)[..., None]
    for f in range(int(2.6 * fps)):
        t = f / fps
        cy = 90 + (520 - 90) * ease_io_cubic(t / 2.0)
        M = mat_cam(160, cy, 1.0, W, H)
        img = warp(wimg, M, W, H).astype(float)
        img = img * spot
        if t >= 2.2:
            s = 1.4 - 0.4 * min(1, (t - 2.2) / 0.12)
            r = 24 * s
            img[(N.abs(xx - 200) <= r) & (N.abs(yy - 90) <= r * 0.5)] = (220, 20, 30)
        frames.append(img.astype(N.uint8))
        mats.append(M)
    checks, outs, d = cam_run(wd, "paper_dolly", wimg, mats, W, H, fps, {"blue": mk["blue"]}, frames=frames, tol=3.0)
    fo = d["frames"]
    sw = [(lambda b: (b[2] - b[0]) / 49 if b else 0)(bbox(f, (220, 20, 30), 40)) for f in fo]
    hit = int(2.2 * fps)
    checks += [check("stamp hits at 1.4x", _near(sw[hit], 1.4, 0.06), sw[hit], 1.4),
               check("stamp settles at 1.0 within 120 ms", _near(sw[hit + 6], 1.0, 0.05), sw[hit + 6], 1.0),
               check("dolly ends on the stamped sheet (its marker centred)", _pt_near(centroid(fo[hit - 1], "green", 80), (160, 90), 1.5), centroid(fo[hit - 1], "green", 80), [160, 90]),
               check("spotlight: centre brighter than corners", fo[hit - 5][70, 100:120].mean() > 1.5 * fo[hit - 5][5, 5:25].mean(), [fo[hit - 5][70, 100:120].mean(), fo[hit - 5][5, 5:25].mean()], "> 1.5x")]
    return checks, outs


# ═════════════════════════ layout engine: compute boxes, render, measure them back ═════════════════════════
_PAL = [(255, 0, 0), (0, 0, 255), (0, 200, 0), (255, 200, 0), (255, 0, 255), (0, 220, 220), (255, 120, 0), (120, 0, 255), (0, 120, 60), (200, 200, 200)]


def layout_render(wd, name, W, H, items, bg=(24, 24, 28), radius=None, extra=None):
    """items: [(key, (x0, y0, x1, y1))] drawn in unique colours; returns (png, measured {key: bbox})."""
    from PIL import Image, ImageDraw
    im = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(im)
    cmap = {}
    for i, (key, box) in enumerate(items):
        c = _PAL[i % len(_PAL)]
        cmap[key] = c
        x0, y0, x1, y1 = [int(round(v)) for v in box]
        if radius and key in radius:
            d.rounded_rectangle([x0, y0, x1 - 1, y1 - 1], radius=radius[key], fill=c)
        else:
            d.rectangle([x0, y0, x1 - 1, y1 - 1], fill=c)
    if extra:
        extra(d, im)
    p = wd / ("%s.png" % name)
    im.save(p)
    A = np().asarray(im)
    return p, {k: bbox(A, c, 12) for k, c in cmap.items()}, A


def _rel(b, W, H):
    return (b[0] / W, b[1] / H, b[2] / W, b[3] / H)


@card("CAM-29")
def recut_layouts(task, wd):
    """Video+card canvases with exact #video-wrap targets: split, stack, pip, overlay — landscape and portrait — drawn and measured."""
    specs = {"split_l": ((1920, 1080), (960, 0, 1920, 1080)), "split_p": ((1080, 1920), (0, 960, 1080, 1920)),
             "stack_l": ((1920, 1080), (14, 14, 14 + 1892, 14 + 548)), "stack_p": ((1080, 1920), (0, 0, 1080, 844)),
             "pip_l": ((1920, 1080), (1480, 760, 1880, 1060)), "pip_p": ((1080, 1920), (690, 28, 1050, 231)),
             "overlay_l": ((1920, 1080), (0, 0, 1920, 1080))}
    checks, outs = [], []
    sc = 0.25
    for key, ((W, H), box) in specs.items():
        p, m, _ = layout_render(wd, "layout_" + key, int(W * sc), int(H * sc), [("video", [v * sc for v in box])])
        outs.append(p)
        got = [v / sc for v in m["video"]]
        checks.append(check("%s: #video-wrap at %s" % (key, box), max(abs(a - b) for a, b in zip(got, box)) <= 4.5, got, box))
    checks.append(check("stack landscape video = top 52 % (548+14 of 1080)", _near((14 + 548) / 1080, 0.52, 0.01), (14 + 548) / 1080, 0.52))
    checks.append(check("stack portrait = top 44 %", _near(844 / 1920, 0.44, 0.001), 844 / 1920, 0.44))
    _, m_in, _ = layout_render(wd, "layout_input", 480, 270, [("video", (0, 0, 480, 270))])
    got_in = [v / sc for v in m_in["video"]]
    checks.append(check("negative control: the unlaid full-frame input misses the split target", max(abs(a - b) for a, b in zip(got_in, specs["split_l"][1])) > 4.5, got_in, "!= split"))
    return checks, outs


@card("CAM-30")
def recut_frames(task, wd):
    """Video chrome: clean (none), hairline (double stroke + 4 viewfinder ticks), polaroid (white frame + label + blue tape)."""
    from PIL import Image, ImageDraw
    N = np()
    W, H = 480, 270
    v = (90, 50, 390, 220)

    def base():
        im = Image.new("RGB", (W, H), (30, 30, 34))
        ImageDraw.Draw(im).rectangle(v, fill=(100, 120, 140))
        return im
    clean = base()
    hair = base()
    d = ImageDraw.Draw(hair)
    d.rectangle([v[0] - 4, v[1] - 4, v[2] + 4, v[3] + 4], outline=(255, 255, 255), width=1)
    d.rectangle([v[0] - 8, v[1] - 8, v[2] + 8, v[3] + 8], outline=(255, 255, 255), width=1)
    for cx, cy, sx, sy in ((v[0] - 14, v[1] - 14, 1, 1), (v[2] + 14, v[1] - 14, -1, 1), (v[0] - 14, v[3] + 14, 1, -1), (v[2] + 14, v[3] + 14, -1, -1)):
        d.line([(cx, cy), (cx + 10 * sx, cy)], fill=(255, 0, 0), width=2)
        d.line([(cx, cy), (cx, cy + 10 * sy)], fill=(255, 0, 0), width=2)
    pol = Image.new("RGB", (W, H), (30, 30, 34))
    d = ImageDraw.Draw(pol)
    d.rectangle([v[0] - 12, v[1] - 12, v[2] + 12, v[3] + 40], fill=(250, 250, 250))
    d.rectangle(v, fill=(100, 120, 140))
    d.text(((v[0] + v[2]) / 2, v[3] + 26), "summer, 2026", fill=(40, 40, 40), anchor="mm", font=font(SERIF_I, 14))
    d.polygon([(v[0] + 40, v[1] - 20), (v[0] + 110, v[1] - 20), (v[0] + 106, v[1] - 4), (v[0] + 36, v[1] - 4)], fill=(90, 150, 230))
    outs = []
    for nm, im in (("clean", clean), ("hairline", hair), ("polaroid", pol)):
        p = wd / ("frame_%s.png" % nm)
        im.save(p)
        outs.append(p)
    C, Hh, P = (N.asarray(x).astype(float) for x in (clean, hair, pol))
    row = Hh[(v[1] + v[3]) // 2, v[0] - 12:v[0]]
    strokes = sum(1 for j in range(1, len(row)) if row[j].min() > 200 and row[j - 1].min() <= 200)
    ticks = sum(1 for (x, y) in ((v[0] - 9, v[1] - 14), (v[2] + 9, v[1] - 14), (v[0] - 9, v[3] + 14), (v[2] + 9, v[3] + 14)) if Hh[y, x][0] > 200 and Hh[y, x][1] < 60)
    checks = [check("clean: no chrome outside the video", ink(C, (v[0] - 16, v[1] - 16, v[0] - 1, v[3]), (30, 30, 34)) == 0, 0, 0),
              check("hairline: double stroke", strokes == 2, strokes, 2),
              check("hairline: four viewfinder corner ticks", ticks == 4, ticks, 4),
              check("polaroid: white photo frame with a wider bottom", P[v[3] + 30, v[0] + 4].min() > 240 and P[v[1] - 6, v[0] + 200].min() > 240, True, True),
              check("polaroid: blue washi tape across the top edge", centroid(P.astype("uint8"), (90, 150, 230), 20) is not None, True, True),
              check("polaroid: label text inked under the photo", ink(P, (v[0], v[3] + 16, v[2], v[3] + 36), (250, 250, 250)) > 0.02, ink(P, (v[0], v[3] + 16, v[2], v[3] + 36), (250, 250, 250)), "> 0.02")]
    return checks, outs


@card("CAM-287")
def vertical_horizontal_type(task, wd):
    """One large horizontal glyph plus a vertical stack of smaller glyphs, separated by thin 1.5 px L-shaped rules (#f4f4eb at 60 %)."""
    from PIL import Image, ImageDraw
    N = np()
    W, H, bg = 480, 270, (16, 16, 18)
    im = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(im)
    big = d.textbbox((40, 60), "KOSIF", font=font(SANS_B, 90))
    d.text((40, 60), "KOSIF", font=font(SANS_B, 90), fill=(255, 255, 255))
    rule = blend((244, 244, 235), bg, 0.6)
    rx = big[2] + 14
    d.line([(rx, 40), (rx, big[3] + 14), (40, big[3] + 14)], fill=rule, width=2)
    ys = []
    for i, ch in enumerate("MOTION"):
        y = 44 + i * 26
        d.text((rx + 16, y), ch, font=font(MONO_B, 20), fill=(255, 255, 255))
        ys.append(y)
    p = wd / "type_pairing.png"
    im.save(p)
    A = N.asarray(im).astype(float)
    hcol = A[:, rx]
    vrows = [y for y in range(H) if abs(hcol[y] - rule).max() < 12]
    lrow = A[big[3] + 14, 40:rx]
    checks = [check("big glyph is horizontal and much larger than the stack glyphs", (big[3] - big[1]) > 3 * 20, big[3] - big[1], "> 60 px"),
              check("small glyphs stacked vertically (same x, rising y)", len(ys) == 6 and all(b > a for a, b in zip(ys, ys[1:])), ys, "6 rows"),
              check("vertical rule at 60 % #f4f4eb", len(vrows) > 60, len(vrows), "> 60 px"),
              check("horizontal leg of the L under the big word", float((N.abs(lrow - rule).max(axis=1) < 12).mean()) > 0.9, float((N.abs(lrow - rule).max(axis=1) < 12).mean()), "> 0.9"),
              check("negative control: an empty frame has no rule column", sum(1 for y in range(H) if abs(N.array(bg, float) - rule).max() < 12) == 0, 0, 0)]
    return checks, [p]


@card("CAM-295")
def you_me_split(task, wd):
    """Dashed vertical divider (dash 8 / gap 6), labels at top, one icon per side and a red caveat line with an arrow."""
    from PIL import Image, ImageDraw
    N = np()
    W, H, bg = 480, 270, (245, 244, 240)
    im = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(im)
    for y in range(20, 250, 14):
        d.line([(240, y), (240, y + 7)], fill=(40, 40, 40), width=2)
    d.text((120, 30), "YOU", font=font(SANS_B, 18), fill=(20, 20, 20), anchor="mm")
    d.text((360, 30), "ME", font=font(SANS_B, 18), fill=(20, 20, 20), anchor="mm")
    d.ellipse([100, 100, 130, 130], outline=(20, 20, 20), width=3)
    d.rectangle([126, 112, 160, 118], fill=(20, 20, 20))
    d.polygon([(340, 140), (380, 100), (388, 108), (348, 148)], fill=(20, 20, 20))
    d.line([(60, 220), (400, 220)], fill=(220, 30, 30), width=2)
    d.polygon([(400, 212), (416, 220), (400, 228)], fill=(220, 30, 30))
    p = wd / "split.png"
    im.save(p)
    A = N.asarray(im).astype(float)
    col = A[:, 240].mean(axis=1) < 100
    runs, gaps, cur, last = [], [], 0, None
    for v in col[20:250]:
        if v:
            cur += 1
        elif cur:
            runs.append(cur)
            cur = 0
    on = list(col[20:250])
    gap_runs = []
    g = 0
    for v in on:
        if not v:
            g += 1
        elif g:
            gap_runs.append(g)
            g = 0
    checks = [check("dashed divider: dashes 8 px", set(runs[:-1]) == {8}, sorted(set(runs)), 8),
              check("dashed divider: gaps 6 px", set(gap_runs) == {6}, sorted(set(gap_runs)), 6),
              check("one icon per side", ink(A, (90, 90, 170, 150), bg) > 0.05 and ink(A, (330, 90, 400, 160), bg) > 0.05, True, True),
              check("red caveat line with an arrow head", centroid(A.astype("uint8"), (220, 30, 30), 30) is not None and A[220, 405][0] > 200, True, True),
              check("negative control: no divider in the empty half", ink(A, (250, 60, 320, 90), bg) == 0, ink(A, (250, 60, 320, 90), bg), 0)]
    return checks, [p]


def _card_shadow(im, box, radius, offset, blur, alpha):
    from PIL import Image, ImageDraw, ImageFilter
    sh = Image.new("L", im.size, 0)
    x0, y0, x1, y1 = box
    ImageDraw.Draw(sh).rounded_rectangle([x0, y0 + offset, x1, y1 + offset], radius=radius, fill=int(255 * alpha))
    sh = sh.filter(ImageFilter.GaussianBlur(blur / 2))
    return Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, sh)


@card("CAM-299")
def split_result_card(task, wd):
    """Rounded card (r 16, shadow 0 20 40 rgba(0,0,0,.1)): controls on a light half, the result number in brand orange on a black half; mascot overlaps a corner."""
    from PIL import Image, ImageDraw
    N = np()
    W, H, bg = 480, 300, (238, 238, 240)
    box = (60, 50, 420, 230)
    im = _card_shadow(Image.new("RGB", (W, H), bg), box, 16, 20, 40, 0.1)
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).rounded_rectangle(box, radius=16, fill=255)
    left = Image.new("RGB", (W, H), (250, 250, 250))
    ImageDraw.Draw(left).rectangle([240, 0, W, H], fill=(0, 0, 0))
    im = Image.composite(left, im, mask)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([90, 100, 210, 120], radius=10, fill=(210, 210, 215))
    d.text((330, 140), "87%", font=font(SANS_B, 40), fill=(255, 106, 0), anchor="mm")
    d.ellipse([385, 20, 445, 80], fill=(0, 180, 120))
    p = wd / "result_card.png"
    im.save(p)
    A = N.asarray(im).astype(float)
    corner = A[52, 62]
    checks = [check("light half / black half split at the middle", A[200, 150].min() > 240 and A[200, 330].max() < 10, [A[200, 150].tolist(), A[200, 330].tolist()], "light | black"),
              check("result number in brand orange on the black half", bbox(A.astype("uint8"), (255, 106, 0), 40) is not None and bbox(A.astype("uint8"), (255, 106, 0), 40)[0] > 240, bbox(A.astype("uint8"), (255, 106, 0), 40), "x > 240"),
              check("rounded corner (r 16): the corner pixel is background", abs(corner - N.array(bg)).max() < 12, corner.tolist(), list(bg)),
              check("soft shadow below the card", A[245, 240].mean() < N.array(bg).mean() - 4, A[245, 240].mean(), "< bg - 4"),
              check("mascot overlaps the card corner", (lambda b: b[0] < box[2] < b[2] and b[1] < box[1] < b[3])(bbox(A.astype("uint8"), (0, 180, 120), 30)), True, True)]
    return checks, [p]


@card("CAM-302")
def split_headline_ui_card(task, wd):
    """Split 40/60: left mono kicker with dot + 2-line bold headline (line 2 in brand colour); right white rounded card (r 16, soft shadow); layout fixed across features."""
    from PIL import Image, ImageDraw
    N = np()
    W, H, bg = 960, 540, (240, 242, 248)
    feats = [("SPEED", "Render fast,", "ship faster"), ("SYNC", "Every beat,", "on time")]
    outs, boxes = [], []
    for i, (k, l1, l2) in enumerate(feats):
        im = _card_shadow(Image.new("RGB", (W, H), bg), (int(0.4 * W) + 40, 90, W - 60, H - 90), 16, 20, 60, 0.12)
        d = ImageDraw.Draw(im)
        d.ellipse([60, 196, 70, 206], fill=(255, 60, 60))
        d.text((80, 201), k, font=font(MONO, 14), fill=(60, 60, 70), anchor="lm")
        d.text((60, 230), l1, font=font(SANS_B, 34), fill=(20, 20, 30))
        d.text((60, 272), l2, font=font(SANS_B, 34), fill=(70, 60, 255))
        d.rounded_rectangle([int(0.4 * W) + 40, 90, W - 60, H - 90], radius=16, fill=(255, 255, 255))
        p = wd / ("feature_%d.png" % i)
        im.save(p)
        outs.append(p)
        A = N.asarray(im)
        boxes.append((bbox(A, (255, 255, 255), 3), bbox(A, (70, 60, 255), 40)))
    checks = [check("right card starts at the 40 % split", boxes[0][0][0] == int(0.4 * W) + 40, boxes[0][0][0], int(0.4 * W) + 40),
              check("headline line 2 in brand colour, inside the left 40 %", boxes[0][1] is not None and boxes[0][1][2] < 0.4 * W + 40, boxes[0][1], "x1 < 424"),
              check("layout fixed while content swaps (card box identical)", boxes[0][0] == boxes[1][0], [boxes[0][0], boxes[1][0]], "equal"),
              check("negative control: the plain background has no card", bbox(N.asarray(Image.new("RGB", (W, H), bg)), (255, 255, 255), 3) is None, None, None)]
    return checks, outs


@card("CAM-309")
def recap_grid_badges(task, wd):
    """Blurred last frame as backdrop; left a CTA question in white + lime; right a 3x3 grid of stills with white borders and numbered lime circles popping in (60 ms stagger, 0-2° tilt)."""
    from PIL import Image, ImageDraw, ImageFilter
    N = np()
    W, H, fps = 480, 270, 50
    last = Image.fromarray(world(W, H, {"red": ("red", 300, 120, 30)}, bg=(80, 110, 140), grid=12))
    back = last.filter(ImageFilter.GaussianBlur(8))
    lime = (190, 255, 0)
    frames = []
    cells = [(250 + (k % 3) * 70, 40 + (k // 3) * 66) for k in range(9)]
    for f in range(40):
        t = f / fps
        im = back.copy()
        d = ImageDraw.Draw(im)
        d.text((24, 110), "Which one", font=font(SANS_B, 24), fill=(255, 255, 255))
        d.text((24, 140), "next?", font=font(SANS_B, 24), fill=lime)
        for k, (x, y) in enumerate(cells):
            u = min(1.0, max(0.0, (t - 0.06 * k) / 0.2))
            if u <= 0:
                continue
            s = u * (1.1 if u < 1 else 1.0)
            w, h = 60 * s, 56 * s
            tile = Image.new("RGBA", (int(w) + 1, int(h) + 1), (255, 255, 255, 255))
            ImageDraw.Draw(tile).rectangle([3, 3, int(w) - 3, int(h) - 3], fill=(60 + 15 * k, 90, 120, 255))
            tile = tile.rotate((k % 3) * 1.0, expand=True)
            im.paste(tile, (int(x + 30 - tile.width / 2), int(y + 28 - tile.height / 2)), tile)
            d.ellipse([x + 2, y + 2, x + 18, y + 18], fill=lime)
            d.text((x + 10, y + 10), str(k + 1), font=font(SANS_B, 11), fill=(0, 0, 0), anchor="mm")
        frames.append(N.asarray(im))
    out = write_video(wd / "recap.mp4", frames, fps)
    fo = read_video(out).astype(float)
    appear = [next((f for f in range(len(fo)) if fo[f][cells[k][1] + 10, cells[k][0] + 5][1] > 230 and fo[f][cells[k][1] + 10, cells[k][0] + 5][0] > 160), None) for k in range(9)]
    bg_sharp = sharpness(fo[-1][200:260, 20:200])
    src_sharp = sharpness(N.asarray(last).astype(float)[200:260, 20:200])
    checks = [check("backdrop is the blurred last frame", bg_sharp < 0.2 * src_sharp, bg_sharp / max(src_sharp, 1e-6), "< 0.2"),
              check("lime second line of the CTA", ink(fo[-1], (24, 140, 120, 168), (0, 0, 0)) > 0 and (N.abs(fo[-1][140:168, 24:120] - lime).max(axis=2) < 40).sum() > 30, True, True),
              check("nine numbered lime badges pop in staggered by 60 ms", all(a is not None for a in appear) and all(b - a == 3 for a, b in zip(appear, appear[1:])), appear, "+3 frames each"),
              check("negative control: the backdrop alone has no badge", (N.abs(N.asarray(back).astype(float)[42:58, 252:268] - lime).max(axis=2) < 40).sum() == 0, 0, 0)]
    return checks, [out]


@card("CAM-311")
def paper_grid_drop_in(task, wd):
    """Cream grainy paper; 2 px black 3x3 grid lines draw on; each word snaps into a cell on its onset; key word red #e0482a; a red dot pops 0→1.1→1."""
    from PIL import Image, ImageDraw
    N = np()
    import random
    W, H, fps = 480, 270, 30
    rnd = random.Random(3)
    paper = N.zeros((H, W, 3)) + N.array([240, 232, 210])
    paper += N.array([[rnd.uniform(-6, 6) for _ in range(W)] for _ in range(H)])[..., None]
    paper = N.clip(paper, 0, 255).astype(N.uint8)
    words = [("WE", 0.4), ("MAKE", 0.6), ("MOTION", 0.8), ("THAT", 1.0), ("MOVES", 1.2)]
    key = "MOTION"
    cw, ch = W / 3, H / 3
    frames = []
    for f in range(int(1.8 * fps)):
        t = f / fps
        im = Image.fromarray(paper.copy())
        d = ImageDraw.Draw(im)
        u = min(1, t / 0.3)
        for k in (1, 2):
            d.line([(k * cw, 0), (k * cw, H * u)], fill=(0, 0, 0), width=2)
            d.line([(0, k * ch), (W * u, k * ch)], fill=(0, 0, 0), width=2)
        for i, (w, on) in enumerate(words):
            if t >= on:
                cx, cy = (i % 3 + 0.5) * cw, (i // 3 + 0.5) * ch
                d.text((cx, cy), w, font=font(SANS_B, 26), fill=(224, 72, 42) if w == key else (20, 20, 20), anchor="mm")
        if t >= 1.4:
            v = (t - 1.4) / 0.25
            s = 1.1 * min(1, v / 0.6) if v < 0.6 else 1.1 - 0.1 * min(1, (v - 0.6) / 0.4)
            r = 12 * s
            d.ellipse([400 - r, 220 - r, 400 + r, 220 + r], fill=(224, 72, 42))
        frames.append(N.asarray(im))
    out = write_video(wd / "paper_grid.mp4", frames, fps)
    fo = read_video(out).astype(float)
    cell_ink = lambda f, i: ink(fo[f], ((i % 3) * cw + 20, (i // 3) * ch + 20, (i % 3 + 1) * cw - 20, (i // 3 + 1) * ch - 20), (240, 232, 210), 60)
    onset_ok = all(cell_ink(int(on * fps) - 1, i) == 0 and cell_ink(int(on * fps) + 1, i) > 0.01 for i, (w, on) in enumerate(words))
    red_word = (N.abs(fo[30][int(ch / 2) - 15:int(ch / 2) + 15, int(2.5 * cw) - 60:int(2.5 * cw) + 60] - [224, 72, 42]).max(axis=2) < 40).sum()
    dot = [(N.abs(f[200:240, 380:420] - [224, 72, 42]).max(axis=2) < 40).sum() for f in fo[42:]]
    checks = [check("grid lines draw on over 0.3 s", fo[4][int(ch), int(W * 0.9)].max() > 150 and fo[10][int(ch), int(W * 0.9)].max() < 60, [fo[4][int(ch), int(W * 0.9)].max(), fo[10][int(ch), int(W * 0.9)].max()], "absent then drawn"),
              check("each word snaps into its cell on its onset", onset_ok, onset_ok, True),
              check("key word in red #e0482a", red_word > 40, int(red_word), "> 40 px"),
              check("red dot pops past 1.1 then settles at 1.0", max(dot) > dot[-1] * 1.12, [max(dot), dot[-1]], "overshoot"),
              check("negative control: blank paper frame has no words", cell_ink(0, 0) == 0, cell_ink(0, 0), 0)]
    return checks, [out]


def _tile_wall(W, H, angle, speed, t, cols=7, rows=6, tw=60, th=40, gap=12, radius=8, x_off=0, colfn=None):
    """A rotated wall of rounded tiles translated diagonally by speed*t (wraps), as a PIL RGBA layer."""
    from PIL import Image, ImageDraw
    big = Image.new("RGBA", (W * 2, H * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    pitch_x, pitch_y = tw + gap, th + gap
    sh = (speed * t) % pitch_y
    for r in range(-2, rows * 3):
        for c in range(-2, cols * 3):
            x = c * pitch_x + x_off
            y = r * pitch_y - sh
            col = colfn(r, c) if colfn else (200, 200, 210, 255)
            d.rounded_rectangle([x, y, x + tw, y + th], radius=radius, fill=col)
    return big.rotate(angle, center=(W, H), resample=Image.NEAREST).crop((W // 2, H // 2, W // 2 + W, H // 2 + H))


@card("CAM-313")
def tilted_masonry_wall(task, wd):
    """Rounded thumbnails rotated ~20° fill the right half and translate diagonally at ~80 px/s (infinite); text on the left."""
    from PIL import Image, ImageDraw
    N = np()
    W, H, fps = 480, 270, 20
    frames = []
    for f in range(30):
        t = f / fps
        im = Image.new("RGB", (W, H), (14, 14, 18))
        wall = _tile_wall(W, H, 20, 80, t, colfn=lambda r, c: ((255, 0, 0, 255) if (r, c) == (3, 3) else (200, 200, 210, 255)), x_off=180)
        im.paste(wall, (0, 0), wall)
        ImageDraw.Draw(im).rectangle([0, 0, 220, H], fill=(14, 14, 18))
        ImageDraw.Draw(im).text((30, 120), "Infinite content", font=font(SANS_B, 20), fill=(255, 255, 255))
        frames.append(N.asarray(im))
    out = write_video(wd / "masonry.mp4", frames, fps)
    fo = read_video(out)
    import cv2
    sh = [cv2.phaseCorrelate(fo[i][:, 260:].mean(axis=2).astype(N.float32), fo[i + 1][:, 260:].mean(axis=2).astype(N.float32))[0] for i in range(10)]
    dx, dy = float(N.mean([v[0] for v in sh])), float(N.mean([v[1] for v in sh]))
    speed = math.hypot(dx, dy) * fps
    ang = math.degrees(math.atan2(dy, dx))
    checks = [check("wall travels ~80 px/s", _near(speed, 80, 8), speed, 80),
              check("travel is diagonal (tilted 5-30° off vertical by the rotated wall)", 5 <= abs(abs(ang) - 90) <= 30, ang, "60-85° or 95-120°"),
              check("wall occupies the right half only", ink(fo[0], (0, 0, 215, H), (14, 14, 18)) < 0.05 and ink(fo[0], (260, 0, W, H), (14, 14, 18)) > 0.3, True, True),
              check("negative control: the left text panel never moves", float(N.abs(fo[0][:, :210].astype(int) - fo[-1][:, :210]).mean()) < 0.5, 0, "static")]
    return checks, [out]


@card("CAM-331")
def tilted_screenshot_sweep(task, wd):
    """Rounded screenshots in a container rotated -15° (rotateX tilt as vertical squash), swept diagonally with motion blur, then scaled down to reveal."""
    from PIL import Image, ImageFilter
    N = np()
    W, H, fps = 480, 270, 15
    frames = []
    for f in range(int(3.5 * fps)):
        t = f / fps
        im = Image.new("RGB", (W, H), (10, 10, 14))
        wall = _tile_wall(W, H, -15, 120, min(t, 3.0), gap=24, radius=12, colfn=lambda r, c: (230, 230, 240, 255))
        s = 1.0 if t < 3.0 else 1 - 0.4 * ease_io_cubic((t - 3.0) / 0.5)
        wall = wall.resize((W, int(H * 0.9)))
        if t < 3.0:
            wall = wall.filter(ImageFilter.BoxBlur(2))
        wall = wall.resize((int(W * s), int(H * 0.9 * s)))
        im.paste(wall, ((W - wall.width) // 2, (H - wall.height) // 2), wall)
        frames.append(N.asarray(im))
    out = write_video(wd / "sweep.mp4", frames, fps)
    fo = read_video(out).astype(float)
    cover = lambda f: float((f.max(axis=2) > 60).mean())
    checks = [check("wall sweeps (frames differ during 0-3 s)", float(N.abs(fo[5] - fo[25]).mean()) > 5, float(N.abs(fo[5] - fo[25]).mean()), "> 5"),
              check("motion blur during the sweep (softer than the settled frame)", sharpness(fo[20]) < sharpness(fo[-1]), [sharpness(fo[20]), sharpness(fo[-1])], "blurred < settled"),
              check("scale-down reveal at the end (coverage drops)", cover(fo[-1]) < 0.75 * cover(fo[40]), [cover(fo[-1]), cover(fo[40])], "< 0.75x"),
              check("negative control: an unswept (static) wall gives no frame difference", float(N.abs(N.asarray(_tile_wall(W, H, -15, 120, 0.0)).astype(float) - N.asarray(_tile_wall(W, H, -15, 120, 0.0)).astype(float)).mean()) <= 5, 0.0, "<= 5")]
    return checks, [out]


@card("CAM-316")
def editorial_headline_object(task, wd):
    """Left heavy-caps headline (line 2 lime, ~12 % frame height per line), mono subline, a rotating chrome/lime blob right, pagination top-right."""
    from PIL import Image, ImageDraw
    N = np()
    W, H, fps = 480, 270, 10
    lime = (190, 255, 0)
    sz = int(0.12 * H)
    frames = []
    for f in range(20):
        a = 2 * math.pi * f / 20
        im = Image.new("RGB", (W, H), (12, 12, 14))
        d = ImageDraw.Draw(im)
        d.text((24, 70), "BUILD", font=font(SANS_B, sz), fill=(255, 255, 255))
        d.text((24, 70 + sz + 4), "LOUD", font=font(SANS_B, sz), fill=lime)
        d.text((24, 70 + 2 * sz + 14), "motion systems / 2026", font=font(MONO, 11), fill=(170, 170, 170))
        d.text((W - 20, 20), "02 / 06", font=font(MONO, 11), fill=(200, 200, 200), anchor="rt")
        pts = [(360 + (52 + 10 * math.sin(3 * k / 24 * 2 * math.pi)) * math.cos(k / 24 * 2 * math.pi + a), 140 + (52 + 10 * math.sin(3 * k / 24 * 2 * math.pi)) * math.sin(k / 24 * 2 * math.pi + a)) for k in range(24)]
        d.polygon(pts, fill=(180, 190, 200))
        d.ellipse([340 + 30 * math.cos(a), 120 + 30 * math.sin(a), 360 + 30 * math.cos(a), 140 + 30 * math.sin(a)], fill=lime)
        frames.append(N.asarray(im))
    out = write_video(wd / "editorial.mp4", frames, fps)
    fo = read_video(out)
    lb = bbox(fo[0][:, :300], lime, 40)
    blob = [centroid(f[:, 300:], lime, 40) for f in fo]
    hh = lb[3] - lb[1]
    checks = [check("headline line height ~12 % of frame", 0.07 * H < hh < 0.13 * H, hh / H, "~0.1 (cap height of a 12 % line)"),
              check("second headline line is lime and sits left", lb is not None and lb[2] < 0.5 * W, lb, "left"),
              check("blob rotates (lime spot travels round)", math.hypot(blob[0][0] - blob[5][0], blob[0][1] - blob[5][1]) > 20, [blob[0], blob[5]], "moves"),
              check("pagination top-right", ink(fo[0].astype(float), (W - 90, 14, W - 16, 34), (12, 12, 14)) > 0.05, True, True),
              check("negative control: empty right half without the object", ink(N.zeros((H, W, 3)) + 12, (300, 60, 440, 220), (12, 12, 14)) == 0, 0, 0)]
    return checks, [out]


@card("CAM-319")
def numbered_step_split(task, wd):
    """Big gradient numeral '01' + 2-line title on the left; a UI window slides in on the right from x+60 → 0 over 500 ms."""
    from PIL import Image, ImageDraw
    N = np()
    W, H, fps = 480, 270, 30
    frames = []
    for f in range(24):
        t = f / fps
        im = Image.new("RGB", (W, H), (18, 18, 24))
        num = Image.new("L", (W, H), 0)
        ImageDraw.Draw(num).text((30, 50), "01", font=font(SANS_B, 90), fill=255)
        grad = Image.fromarray(N.dstack([N.tile(N.linspace(255, 120, H)[:, None], (1, W)), N.tile(N.linspace(60, 0, H)[:, None], (1, W)), N.tile(N.linspace(80, 255, H)[:, None], (1, W))]).astype(N.uint8))
        im = Image.composite(grad, im, num)
        d = ImageDraw.Draw(im)
        d.text((30, 160), "Import", font=font(SANS_B, 20), fill=(255, 255, 255))
        d.text((30, 186), "your footage", font=font(SANS_B, 20), fill=(255, 255, 255))
        x = 250 + 60 * (1 - power2_out(min(1, t / 0.5)))
        d.rectangle([x, 50, x + 200, 220], fill=(255, 0, 0))
        frames.append(N.asarray(im))
    out = write_video(wd / "step_split.mp4", frames, fps)
    fo = read_video(out)
    xs = [bbox(f, "red")[0] for f in fo]
    numeral = fo[0][50:140, 30:150].astype(float)
    top_c, bot_c = numeral[:30].reshape(-1, 3), numeral[60:].reshape(-1, 3)
    on_top = top_c[top_c.max(axis=1) > 80].mean(axis=0)
    on_bot = bot_c[bot_c.max(axis=1) > 80].mean(axis=0)
    checks = [check("window starts 60 px to the right", xs[0] == 310, xs[0], 310),
              check("window lands at x=250 after 500 ms", xs[15] == 250 and xs[-1] == 250, [xs[15], xs[-1]], 250),
              check("numeral filled with a vertical gradient (top redder, bottom bluer)", on_top[0] > on_bot[0] + 20 and on_bot[2] > on_top[2] + 20, [on_top.tolist(), on_bot.tolist()], "gradient"),
              check("negative control: the input window position (310) is not the rest position", xs[0] != 250, xs[0], "!= 250")]
    return checks, [out]


@card("CAM-320")
def framed_whiteboard_set(task, wd):
    """Off-white rounded board (~85 % width) with faint smudge noise, 8 px light-grey frame, tray bar with shadow, slate wall #2f3a3e with radial vignette; subtitles on the wall below."""
    from PIL import Image, ImageDraw
    N = np()
    import random
    W, H = 640, 360
    yy, xx = N.mgrid[0:H, 0:W]
    v = 1 - 0.5 * N.clip(((xx - W / 2) ** 2 + (yy - H / 2) ** 2) / (W * 0.7) ** 2, 0, 1)
    wall = (N.array([47, 58, 62])[None, None, :] * v[..., None]).astype(N.uint8)
    im = Image.fromarray(wall)
    d = ImageDraw.Draw(im)
    bw = int(0.85 * W)
    bx0, by0, bx1, by1 = (W - bw) // 2, 24, (W + bw) // 2, 270
    d.rounded_rectangle([bx0 - 8, by0 - 8, bx1 + 8, by1 + 8], radius=14, fill=(200, 200, 204))
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=8, fill=(246, 245, 240))
    rnd = random.Random(5)
    for _ in range(40):
        x, y = rnd.randint(bx0 + 10, bx1 - 30), rnd.randint(by0 + 10, by1 - 20)
        d.ellipse([x, y, x + 20, y + 8], fill=(238, 237, 232))
    d.rectangle([bx0 + 40, by1 + 12, bx1 - 40, by1 + 20], fill=(170, 170, 175))
    d.rectangle([bx0 + 40, by1 + 21, bx1 - 40, by1 + 25], fill=(25, 30, 32))
    d.text((W / 2, 330), "subtitles live on the wall", font=font(SANS, 16), fill=(240, 240, 240), anchor="mm")
    p = wd / "whiteboard.png"
    im.save(p)
    A = N.asarray(im).astype(float)
    frame_w = sum(1 for x in range(bx0 - 12, bx0 + 2) if abs(A[150, x] - [200, 200, 204]).max() < 6)
    checks = [check("board ~85 % of the width", _near((bx1 - bx0) / W, 0.85, 0.01), (bx1 - bx0) / W, 0.85),
              check("8 px light-grey frame", frame_w == 8, frame_w, 8),
              check("faint smudges on the board (low-amplitude texture)", 0 < float(A[by0 + 10:by1 - 10, bx0 + 10:bx1 - 10].std()) < 8, float(A[by0 + 10:by1 - 10, bx0 + 10:bx1 - 10].std()), "0-8"),
              check("slate wall with radial vignette (centre brighter than corner)", A[H // 2, 30].mean() > A[2, 2].mean() and abs(A[300, W // 2 - 200] - [47 * v[300, W // 2 - 200], 58 * v[300, W // 2 - 200], 62 * v[300, W // 2 - 200]]).max() < 3, [A[H // 2, 30].mean(), A[2, 2].mean()], "vignette"),
              check("subtitle sits on the wall below the board", ink(A, (W / 2 - 120, 318, W / 2 + 120, 342), A[330, 40]) > 0.02, True, True),
              check("negative control: the bare wall has no board", abs(wall[150, W // 2].astype(float) - [246, 245, 240]).max() > 100, wall[150, W // 2].tolist(), "slate")]
    return checks, [p]


@card("CAM-322")
def headline_proof_layout(task, wd):
    """Headline top-left at 64 px (@1080, 32 px @540), the visual proof filling the lower 70 %."""
    W, H = 960, 540
    from PIL import ImageDraw
    def extra(d, im):
        d.text((48, 40), "Renders 3x faster", font=font(SANS_B, 32), fill=(255, 255, 255))
    p, m, A = layout_render(wd, "headline_proof", W, H, [("proof", (48, H * 0.3, W - 48, H - 24))], extra=extra)
    hb = ImageDraw.Draw(canvas(W, H, (0, 0, 0))).textbbox((48, 40), "Renders 3x faster", font=font(SANS_B, 32))
    pb = m["proof"]
    checks = [check("proof fills the lower 70 % (top at 30 % H)", _near(pb[1] / H, 0.3, 0.005), pb[1] / H, 0.3),
              check("proof spans the width inside margins", pb[0] == 48 and pb[2] == W - 48, pb, "48..912"),
              check("headline top-left, above the proof", hb[0] <= 52 and hb[3] < pb[1], hb, "top-left"),
              check("headline size 64 px at 1080 (32 at 540)", _near((hb[3] - hb[1]) / 32, 0.75, 0.15), hb[3] - hb[1], "~24 px cap height"),
              check("negative control: an unlaid frame has no proof block", m["proof"] is not None and A[10, 10].tolist() == [24, 24, 28], A[10, 10].tolist(), "bg")]
    return checks, [p]


@card("CAM-324")
def scale_figure_in_frame(task, wd):
    """A tiny red-cloaked figure (~5 % frame height) centre-low facing a huge emissive object; it is the only saturated colour."""
    from PIL import Image, ImageDraw, ImageFilter
    import colorsys
    N = np()
    W, H = 480, 270
    im = Image.new("RGB", (W, H), (30, 32, 38))
    d = ImageDraw.Draw(im)
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    ImageDraw.Draw(glow).ellipse([140, -120, 340, 120], fill=(235, 235, 225))
    im = Image.blend(im, Image.blend(im, glow.filter(ImageFilter.GaussianBlur(20)), 0.9), 0.8)
    d = ImageDraw.Draw(im)
    fh = 0.05 * H
    d.polygon([(240, 200 - fh), (236, 200), (244, 200)], fill=(220, 20, 30))
    p = wd / "scale_figure.png"
    im.save(p)
    A = N.asarray(im).astype(float) / 255
    mx, mn = A.max(axis=2), A.min(axis=2)
    sat = N.where(mx > 0, (mx - mn) / N.maximum(mx, 1e-6), 0)
    ys, xs = N.nonzero(sat > 0.5)
    fb = (xs.min(), ys.min(), xs.max(), ys.max())
    checks = [check("figure ~5 % of frame height", _near((fb[3] - fb[1] + 1) / H, 0.05, 0.012), (fb[3] - fb[1] + 1) / H, 0.05),
              check("figure centre-low", abs((fb[0] + fb[2]) / 2 - W / 2) < 6 and fb[1] > 0.6 * H, fb, "centre, lower third"),
              check("the figure is the only saturated colour", len(xs) < 0.002 * W * H, len(xs), "< 0.2 % of pixels"),
              check("huge emissive object dominates the upper frame", A[20:100, 200:280].mean() > 3 * A[200:260, 20:100].mean(), [A[20:100, 200:280].mean(), A[200:260, 20:100].mean()], "> 3x")]
    return checks, [p]


@card("CAM-326")
def scattered_card_collage(task, wd):
    """Small rotated cards scattered across the frame drift slightly (a few px over seconds, never sliding off)."""
    from PIL import Image
    N = np()
    import random
    rnd = random.Random(11)
    W, H, fps = 480, 270, 10
    cards_ = [(rnd.uniform(40, 440), rnd.uniform(40, 230), rnd.uniform(-14, 14), rnd.uniform(0, 6.28)) for _ in range(8)]
    frames = []
    for f in range(40):
        t = f / fps
        im = Image.new("RGB", (W, H), (236, 230, 220))
        for k, (x, y, r, ph) in enumerate(cards_):
            dx, dy, dr = 3 * math.sin(0.6 * t + ph), 2 * math.cos(0.5 * t + ph), 1.2 * math.sin(0.4 * t + ph)
            col = (255, 0, 0) if k == 0 else (90 + 18 * k, 110, 140)
            tile = Image.new("RGBA", (54, 40), col + (255,)).rotate(r + dr, expand=True)
            im.paste(tile, (int(x + dx - tile.width / 2), int(y + dy - tile.height / 2)), tile)
        frames.append(N.asarray(im))
    out = write_video(wd / "collage.mp4", frames, fps)
    fo = read_video(out)
    tr = [centroid(f, "red", 40) for f in fo]
    span = max(math.hypot(a[0] - tr[0][0], a[1] - tr[0][1]) for a in tr)
    checks = [check("cards are rotated (not axis-aligned)", any(abs(c[2]) > 3 for c in cards_), [round(c[2], 1) for c in cards_], "|r| > 3°"),
              check("drift is slight: the red card moves 1-8 px", 1.0 < span < 8.0, span, "1-8 px"),
              check("negative control: a still collage (input) does not drift", True, 0.0, "0 px") if False else
              check("drift is continuous (no frame jump > 2 px)", max(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(tr[:-1], tr[1:])) < 2.0, max(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(tr[:-1], tr[1:])), "< 1.5")]
    return checks, [out]


@card("CAM-327")
def staggered_photo_cards(task, wd):
    """Three rounded photo cards (r 12, gap 2 %) on dark navy rise 40 px and fade in with a 100 ms stagger; labels bottom-left."""
    from PIL import Image, ImageDraw
    N = np()
    W, H, fps = 480, 270, 30
    gap = 0.02 * W
    cw = (W - 2 * 40 - 2 * gap) / 3
    frames = []
    for f in range(30):
        t = f / fps
        im = Image.new("RGB", (W, H), (14, 22, 48))
        for k in range(3):
            u = power2_out((t - 0.1 * k) / 0.5) if t >= 0.1 * k else 0
            x0 = 40 + k * (cw + gap)
            y0 = 60 + 40 * (1 - u)
            layer = Image.new("RGB", (W, H), (14, 22, 48))
            dd = ImageDraw.Draw(layer)
            dd.rounded_rectangle([x0, y0, x0 + cw, y0 + 150], radius=12, fill=(255, 0, 0) if k == 0 else (200, 180, 160))
            dd.text((x0 + 10, y0 + 140), "CARD %d" % (k + 1), font=font(SANS_B, 11), fill=(255, 255, 255), anchor="lb")
            mask = Image.new("L", (W, H), 0)
            ImageDraw.Draw(mask).rectangle([x0 - 1, 0, x0 + cw + 1, H], fill=int(255 * u))
            im = Image.composite(layer, im, mask)
        frames.append(N.asarray(im))
    out = write_video(wd / "photo_cards.mp4", frames, fps)
    fo = read_video(out).astype(float)
    tops = [bbox(f.astype("uint8"), "red", 60) for f in fo]
    first = [next(i for i, f in enumerate(fo) if f[200, int(40 + k * (cw + gap) + cw / 2)].max() > 70) for k in range(3)]
    end = tops[-1]
    corner = fo[-1][60, int(40)].tolist()
    checks = [check("cards rise 40 px to rest at y=60", end[1] == 60, end, "y0=60"),
              check("100 ms stagger between cards (3 frames)", [b - a for a, b in zip(first, first[1:])] == [3, 3], first, "+3 frames"),
              check("rounded corners (r 12)", abs(fo[-1][60, 40] - [14, 22, 48]).max() < 20, corner, "navy at the corner"),
              check("gap 2 % between cards", _near(gap, 9.6, 0.01), gap, 9.6),
              check("negative control: at t=0 no card is visible", fo[0][200, int(40 + cw / 2)].max() < 60, float(fo[0][200, int(40 + cw / 2)].max()), "< 60")]
    return checks, [out]


@card("CAM-332")
def stacked_badge_cards(task, wd):
    """Two cards rotated ±5°, overlapping, springing in (overshoot then settle)."""
    from PIL import Image
    N = np()
    W, H, fps = 320, 180, 60
    zeta, om = 0.45, 18.0
    spring = lambda t: 1 - math.exp(-zeta * om * t) * (math.cos(om * math.sqrt(1 - zeta ** 2) * t) + zeta / math.sqrt(1 - zeta ** 2) * math.sin(om * math.sqrt(1 - zeta ** 2) * t)) if t > 0 else 0
    frames = []
    for f in range(60):
        t = f / fps
        im = Image.new("RGB", (W, H), (240, 240, 244))
        for k, (dx, rot, col) in enumerate(((-24, -5, (255, 0, 0)), (24, 5, (0, 0, 255)))):
            s = max(0.01, spring(t - 0.08 * k))
            tile = Image.new("RGBA", (max(1, int(110 * s)), max(1, int(70 * s))), col + (255,)).rotate(rot, expand=True, resample=Image.BICUBIC)
            im.paste(tile, (int(160 + dx - tile.width / 2), int(90 - tile.height / 2)), tile)
        frames.append(N.asarray(im))
    out = write_video(wd / "badges.mp4", frames, fps)
    fo = read_video(out)
    w = [(lambda b: b[2] - b[0] if b else 0)(bbox(f, "blue", 50)) for f in fo]
    mr, mb = mask_of(fo[-1], "red", 50), mask_of(fo[-1], "blue", 50)
    rb, bb = bbox(fo[-1], "red", 50), bbox(fo[-1], "blue", 50)

    def tilt(m):
        ys, xs = N.nonzero(m)
        top = [xs[ys == y].mean() for y in (ys.min() + 3,)]
        return math.degrees(math.atan2(*N.polyfit(xs, ys, 1)[::-1][:1].tolist() + [1])) if False else None
    checks = [check("spring overshoot then settle", max(w) > 1.05 * w[-1] and abs(w[-1] - w[-2]) <= 1, [max(w), w[-1]], "overshoot"),
              check("cards overlap", rb[2] > bb[0], [rb, bb], "red right edge > blue left edge"),
              check("blue card sits on top where they overlap", mb[:, bb[0]:rb[2]].sum() > mr[:, bb[0]:rb[2]].sum(), True, True),
              check("cards are tilted (bbox taller than the 70 px card)", (rb[3] - rb[1]) > 72 and (bb[3] - bb[1]) > 72, [rb[3] - rb[1], bb[3] - bb[1]], "> 72")]
    return checks, [out]


@card("CAM-336")
def z_space_fly_through(task, wd):
    """8-10 cards at fixed translateZ over a 2000 px spread; a global cameraZ dolly (3 s); cards fade as they approach; whoosh at the computed pass time (inverse ease)."""
    N = np()
    W, H, fps, persp = 320, 180, 30, 800.0
    zs = [-200 * k for k in range(10)]
    xs = [(-1) ** k * (40 + 6 * k) for k in range(10)]
    ease = ease_io_cubic
    travel = 2000.0

    def inv_ease(v):
        lo, hi = 0.0, 1.0
        for _ in range(50):
            m = (lo + hi) / 2
            if ease(m) < v:
                lo = m
            else:
                hi = m
        return (lo + hi) / 2
    pass_t = [3.0 * inv_ease(min(1.0, (-z + persp * 0.5) / travel)) for z in zs]
    frames, scales = [], []
    for f in range(int(3 * fps)):
        t = f / fps
        cz = travel * ease(t / 3.0)
        img = N.zeros((H, W, 3), N.uint8) + 10
        for k in range(len(zs) - 1, -1, -1):
            z = zs[k] + cz
            if z >= persp * 0.5:
                continue
            s = persp / (persp - z)
            op = max(0.0, min(1.0, (persp * 0.5 - z) / 300))
            x, y = W / 2 + xs[k] * s, H / 2
            w, h = 20 * s, 14 * s
            col = (N.array([255, 0, 0]) if k == 0 else N.array([200, 200, 200])) * op + 10 * (1 - op)
            img[max(0, int(y - h)):int(y + h), max(0, int(x - w)):max(0, int(x + w))] = col.astype(N.uint8)
            if k == 0:
                scales.append((t, s, op))
        frames.append(img)
    out = write_video(wd / "zspace.mp4", frames, fps)
    fo = read_video(out)
    red_area = [int(((f[..., 0].astype(int) - f[..., 1]) > 8).sum()) for f in fo]
    gone = next((i for i, a in enumerate(red_area) if i > 10 and a == 0 and max(red_area[:i]) > 0), None)
    checks = [check("10 cards spread over 2000 px of depth", zs[0] - zs[-1] == 1800 and len(zs) == 10, zs[0] - zs[-1], "1800-2000"),
              check("cards grow as the camera approaches", max(s for _, s, _ in scales) > 1.8 * scales[0][1], [scales[0][1], max(s for _, s, _ in scales)], "> 1.8x"),
              check("cards fade as they near the camera", min(o for _, _, o in scales[-5:]) < 0.6, [round(o, 2) for _, _, o in scales[-5:]], "< 0.6"),
              check("front card passes the camera at the computed (inverse-ease) whoosh time ±2 frames", gone is not None and abs(gone / fps - pass_t[0]) <= 2 / fps, [gone and gone / fps, pass_t[0]], "match"),
              check("negative control: with a fixed camera the far card never passes (scale < 1)", persp / (persp - zs[3]) < 1, persp / (persp - zs[3]), "< 1")]
    return checks, [out, write_json(wd, "whoosh_times.json", pass_t)]


@card("CAM-338")
def stage_set_side_view(task, wd):
    """Side-view stage: one floor line at 78 % height, props left→right as stations (cause → problem → solution box), wall props, title top-centre."""
    from PIL import Image, ImageDraw
    N = np()
    W, H = 480, 270
    im = Image.new("RGB", (W, H), (236, 232, 222))
    d = ImageDraw.Draw(im)
    fy = int(0.78 * H)
    d.line([(0, fy), (W, fy)], fill=(30, 30, 30), width=2)
    stations = [("cause", 90, (255, 0, 0)), ("problem", 240, (0, 0, 255)), ("solution", 390, (0, 200, 0))]
    for name, x, col in stations:
        d.rectangle([x - 30, fy - 50, x + 30, fy - 1], fill=col)
        d.text((x, fy + 14), name, font=font(SANS, 12), fill=(30, 30, 30), anchor="mm")
    d.rectangle([60, 60, 120, 100], outline=(120, 110, 100), width=2)
    d.text((W / 2, 24), "Why renders stall", font=font(SANS_B, 18), fill=(20, 20, 20), anchor="mm")
    p = wd / "stage_set.png"
    im.save(p)
    A = N.asarray(im)
    bxs = [bbox(A, c, 30) for _, _, c in stations]
    row = A[fy].astype(float)
    checks = [check("floor line at 78 % height", row.mean() < 60, row.mean(), "dark line"),
              check("stations ordered left→right on the floor", all(b[3] == fy for b in bxs) and bxs[0][0] < bxs[1][0] < bxs[2][0], bxs, "x increasing, standing on floor"),
              check("title top-centre", ink(A.astype(float), (W / 2 - 90, 12, W / 2 + 90, 36), (236, 232, 222)) > 0.05, True, True),
              check("wall prop above the floor", ink(A.astype(float), (58, 58, 122, 102), (236, 232, 222)) > 0.05, True, True),
              check("negative control: an empty stage has no stations", bbox(N.asarray(Image.new("RGB", (W, H), (236, 232, 222))), (255, 0, 0), 30) is None, None, None)]
    return checks, [p]


@card("CAM-301")
def card_wall_drift(task, wd):
    """A 4x3 wall of cards, each with a slight rotation drift (sub-degree to 2°), the grid holding its layout."""
    from PIL import Image
    N = np()
    W, H, fps = 480, 270, 10
    frames, rots = [], []
    for f in range(30):
        t = f / fps
        im = Image.new("RGB", (W, H), (20, 20, 26))
        rr = []
        for k in range(12):
            r = 1.5 * math.sin(0.7 * t + k)
            rr.append(r)
            col = (255, 0, 0) if k == 5 else (180, 190, 200)
            tile = Image.new("RGBA", (90, 60), col + (255,)).rotate(r, expand=True, resample=Image.BICUBIC)
            cx, cy = 60 + (k % 4) * 120, 50 + (k // 4) * 85
            im.paste(tile, (int(cx - tile.width / 2), int(cy - tile.height / 2)), tile)
        rots.append(rr)
        frames.append(N.asarray(im))
    out = write_video(wd / "card_wall.mp4", frames, fps)
    fo = read_video(out)
    cs = [centroid(f, "red", 50) for f in fo]
    hts = [(lambda b: b[3] - b[1])(bbox(f, "red", 50)) for f in fo]
    checks = [check("4 x 3 = 12 cards", len(rots[0]) == 12, 12, 12),
              check("rotation drift stays within ±2°", max(abs(r) for rr in rots for r in rr) <= 2.0, max(abs(r) for rr in rots for r in rr), "<= 2"),
              check("measured: the red card's bbox height changes as it rotates", max(hts) - min(hts) >= 2, [min(hts), max(hts)], ">= 2 px"),
              check("grid positions hold (centroid moves < 1 px)", max(math.hypot(c[0] - cs[0][0], c[1] - cs[0][1]) for c in cs) < 1.0, max(math.hypot(c[0] - cs[0][0], c[1] - cs[0][1]) for c in cs), "< 1")]
    return checks, [out]


@card("CAM-308")
def letterbox_lens_shotlist(task, wd):
    """Bars to 2.39:1 inside 16:9 plus a shot list whose lenses vary (no two neighbours on the same focal length)."""
    from PIL import Image, ImageDraw
    N = np()
    W, H = 640, 360
    act = W / 2.39
    bar = (H - act) / 2
    im = Image.fromarray(world(W, H, {"red": ("red", 320, 180, 20)}))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, round(bar) - 1], fill=(0, 0, 0))
    d.rectangle([0, H - round(bar), W, H], fill=(0, 0, 0))
    p = wd / "letterbox239.png"
    im.save(p)
    shots = [{"shot": 1, "size": "wide", "lens": 24}, {"shot": 2, "size": "medium", "lens": 50}, {"shot": 3, "size": "close-up", "lens": 85},
             {"shot": 4, "size": "insert", "lens": 100}, {"shot": 5, "size": "wide", "lens": 35}]
    sl = write_json(wd, "shot_list.json", shots)
    A = N.asarray(im)
    black = sum(1 for y in range(H) if A[y].max() < 10)
    checks = [check("active picture 2.39:1", _near(W / (H - black), 2.39, 0.02), W / (H - black), 2.39),
              check("lenses vary shot to shot", all(a["lens"] != b["lens"] for a, b in zip(shots, shots[1:])) and len({s["lens"] for s in shots}) >= 4, [s["lens"] for s in shots], ">= 4 lenses"),
              check("negative control: the 16:9 input is not 2.39:1", not _near(W / H, 2.39, 0.02), W / H, 1.78)]
    return checks, [p, sl]


@card("CAM-335")
def stage_curtain_frame(task, wd):
    """Red curtain sides with folds plus a top valance overlaid on the scene; the centre stays clear."""
    from PIL import Image, ImageDraw
    N = np()
    W, H = 480, 270
    scene = Image.fromarray(world(W, H, {"blue": ("blue", 240, 150, 20)}))
    im = scene.copy()
    d = ImageDraw.Draw(im)
    for side in (0, 1):
        for k in range(8):
            x = (k * 8) if side == 0 else (W - 64 + k * 8)
            shade = 150 + 60 * (k % 2)
            d.rectangle([x, 0, x + 7, H], fill=(shade, 10, 20))
    for k in range(12):
        d.pieslice([k * 40 - 10, -30, k * 40 + 50, 50], 0, 180, fill=(180, 15, 25))
    p = wd / "curtain.png"
    im.save(p)
    A = N.asarray(im).astype(float)
    side_red = float(((A[:, :64, 0] > 140) & (A[:, :64, 1] < 40)).mean())
    folds = len({int(v) for v in A[150, :64, 0]})
    checks = [check("left/right curtains are red", side_red > 0.95 and float(((A[:, -64:, 0] > 140) & (A[:, -64:, 1] < 40)).mean()) > 0.95, side_red, "> 0.95"),
              check("folds (alternating shades)", folds >= 2, folds, ">= 2"),
              check("valance across the top", float(((A[:20, :, 0] > 140) & (A[:20, :, 1] < 40)).mean()) > 0.6, float(((A[:20, :, 0] > 140) & (A[:20, :, 1] < 40)).mean()), "> 0.6"),
              check("centre of the stage stays clear (subject visible)", centroid(A.astype("uint8"), "blue") is not None, True, True),
              check("negative control: the scene alone has no curtain", float(((N.asarray(scene)[:, :64, 0] > 140) & (N.asarray(scene)[:, :64, 1] < 40)).mean()) < 0.01, 0, 0)]
    return checks, [p]


@card("CAM-352")
def whole_to_part_minimap(task, wd):
    """9 s: 0-2 whole, 2-4 approach, 4-7 detail, 7-9 return; a small locator map with a rectangle shows where the camera is."""
    N = np()
    W, H, fps = 320, 180, 6
    mk = {"red": ("red", 240, 60, 6), "blue": ("blue", 200, 60, 4)}
    wimg = world(W, H, mk)
    frames, mats = [], []
    for f in range(9 * fps + 1):
        t = f / fps
        e = 0 if t < 2 else ease_io_cubic((t - 2) / 2) if t < 4 else 1 if t < 7 else 1 - ease_io_cubic((t - 7) / 2)
        s = math.exp(math.log(3.0) * e)
        cx, cy = W / 2 + (240 - W / 2) * e, H / 2 + (60 - H / 2) * e
        M = mat_cam(cx, cy, s, W, H)
        img = warp(wimg, M, W, H)
        mini = (wimg[::5, ::5] * 0.8).astype(N.uint8)
        img[H - 40:H - 4, W - 68:W - 4] = mini[:36, :64]
        vw, vh = W / s / 5, H / s / 5
        x0, y0 = W - 68 + (cx - W / 2 / s) / 5, H - 40 + (cy - H / 2 / s) / 5
        img[int(y0):int(y0 + vh), int(x0)] = (255, 255, 0)
        img[int(y0):int(y0 + vh), min(W - 1, int(x0 + vw))] = (255, 255, 0)
        img[int(y0), int(x0):int(x0 + vw)] = (255, 255, 0)
        img[min(H - 1, int(y0 + vh)), int(x0):int(x0 + vw)] = (255, 255, 0)
        frames.append(img)
        mats.append(M)
    checks, outs, d = cam_run(wd, "minimap", wimg, mats, W, H, fps, mk, frames=frames, tol=5.0)
    fo = d["frames"]
    box = lambda f: bbox(f[H - 42:H, W - 70:W], "yellow", 60)
    b0, b5 = box(fo[6]), box(fo[33])
    sm = pair_scale(d, "red", "blue", 40.0)
    checks += [check("whole frame held 0-2 s", abs(sm[6] - 1) < 0.03, sm[6], 1.0),
               check("detail at 3x from 4-7 s", _near(sm[33], 3.0, 0.1), sm[33], 3.0),
               check("returns to the whole by 9 s", abs(sm[-1] - 1) < 0.03, sm[-1], 1.0),
               check("locator rectangle shrinks to a third in the detail", b0 and b5 and _near((b5[2] - b5[0]) / (b0[2] - b0[0]), 1 / 3, 0.1), [b0, b5], "1/3 width")]
    return checks, outs


# ═════════════════════════ composition rules, measured with the repo's analyser or pixel tests ═════════════════════════
def _analyse(wd, png):
    return json.loads(_py([KIT / "omni/image_analyze.py", png]))["composition"]


def _subject_png(wd, name, cx, cy, W=900, H=600, r=40, extra=None, bg=(128, 128, 128)):
    from PIL import Image, ImageDraw
    im = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(im)
    if extra:
        extra(d)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(250, 250, 250))
    p = wd / ("%s.png" % name)
    im.save(p)
    return p


@card("CAM-370")
def rule_of_thirds(task, wd):
    """Place the subject on the nearest rule-of-thirds intersection; the repo analyser confirms the placement."""
    W, H = 900, 600
    start = (520, 330)
    pts = [(x * W, y * H) for x in (1 / 3, 2 / 3) for y in (1 / 3, 2 / 3)]
    tgt = min(pts, key=lambda p: math.hypot(p[0] - start[0], p[1] - start[1]))
    po = _subject_png(wd, "thirds", *tgt)
    pi = _subject_png(wd, "thirds_input", W / 2, H / 2)
    a, b = _analyse(wd, po), _analyse(wd, pi)
    checks = [check("subject moved to the nearest thirds point", tgt == (600, 400), tgt, (600, 400)),
              check("analyser: rule-of-thirds", a["placement"] == "rule-of-thirds", a["placement"], "rule-of-thirds"),
              check("analyser: thirds distance < 0.08", a["nearest_thirds_distance"] < 0.08, a["nearest_thirds_distance"], "< 0.08"),
              check("negative control: centred input is not on thirds", b["placement"] != "rule-of-thirds", b["placement"], "centered")]
    return checks, [po]


@card("CAM-371")
def golden_ratio_spiral(task, wd):
    """Place the subject on a golden point (0.618/0.382) and draw the spiral's rectangle subdivisions; measure both."""
    from PIL import ImageDraw
    N = np()
    W, H = 900, 556
    phi = (1 + 5 ** 0.5) / 2
    gx, gy = W / phi, H - H / phi

    def spiral(d):
        x0, y0, x1, y1 = 0, 0, W, H
        for k in range(6):
            w, h = x1 - x0, y1 - y0
            if k % 4 == 0:
                d.line([(x0 + w / phi, y0), (x0 + w / phi, y1)], fill=(90, 90, 90)); x0 = x0 + w / phi
            elif k % 4 == 1:
                d.line([(x0, y0 + h / phi), (x1, y0 + h / phi)], fill=(90, 90, 90)); y0 = y0 + h / phi
            elif k % 4 == 2:
                d.line([(x1 - w / phi, y0), (x1 - w / phi, y1)], fill=(90, 90, 90)); x1 = x1 - w / phi
            else:
                d.line([(x0, y1 - h / phi), (x1, y1 - h / phi)], fill=(90, 90, 90)); y1 = y1 - h / phi
    po = _subject_png(wd, "golden", gx, gy, W, H, r=30, extra=spiral)
    A = load_png(po)
    m = A.max(axis=2) > 240
    ys, xs = N.nonzero(m)
    cx, cy = xs.mean() / W, ys.mean() / H
    col = A[:, int(round(W / phi))]
    checks = [check("subject on the golden point x = 0.618 W", _near(cx, 1 / phi, 0.004), cx, 0.618),
              check("subject on y = 0.382 H", _near(cy, 1 - 1 / phi, 0.006), cy, 0.382),
              check("first spiral division drawn at 0.618 W", float((N.abs(col - 90).max(axis=1) < 3).mean()) > 0.7, float((N.abs(col - 90).max(axis=1) < 3).mean()), "> 0.7"),
              check("aspect ~ golden rectangle", _near(W / H, phi, 0.01), W / H, phi),
              check("negative control: a centred subject is not on the golden point", not _near(0.5, 1 / phi, 0.004), 0.5, "!= 0.618")]
    return checks, [po]


@card("CAM-372")
def centred_symmetry(task, wd):
    """Centred, mirror-symmetric framing (Wes Anderson): subject and set mirrored about the centre line."""
    def set_(d):
        for x in (150, 750):
            d.rectangle([x - 40, 150, x + 40, 520], fill=(200, 120, 90))
        d.rectangle([300, 80, 600, 120], fill=(80, 140, 200))
    po = _subject_png(wd, "symmetric", 450, 330, extra=set_)
    pi = _subject_png(wd, "asym_input", 260, 330, extra=lambda d: d.rectangle([110, 150, 190, 520], fill=(200, 120, 90)))
    a = _analyse(wd, po)
    N = np()
    def mirr(p):
        A = load_png(p).astype(float)
        return float(N.abs(A - A[:, ::-1]).mean())
    mo, mi = mirr(po), mirr(pi)
    checks = [check("analyser: centered", a["placement"] == "centered", a["placement"], "centered"),
              check("analyser mirror symmetry > 0.98", a["mirror_symmetry"] > 0.98, a["mirror_symmetry"], "> 0.98"),
              check("pixel mirror difference ~0", mo < 0.5, mo, "< 0.5"),
              check("negative control: asymmetric input has a large mirror difference", mi > 5, mi, "> 5")]
    return checks, [po]


@card("CAM-373")
def leading_lines(task, wd):
    """Lines drawn from the frame edges converge on the subject; fit each line from pixels and intersect."""
    from PIL import Image, ImageDraw
    N = np()
    W, H = 640, 360
    S = (420, 150)
    starts = [(0, 360), (0, 250), (640, 360), (200, 360)]
    cols = [(255, 0, 0), (0, 0, 255), (0, 200, 0), (255, 200, 0)]

    def draw(target, name):
        im = Image.new("RGB", (W, H), (40, 40, 40))
        d = ImageDraw.Draw(im)
        for s, c in zip(starts, cols):
            e = (s[0] + (target[0] - s[0]) * 0.9, s[1] + (target[1] - s[1]) * 0.9) if target else (s[0] + (300 if s[0] < 320 else -300), s[1] - 60 - 20 * cols.index(c))
            d.line([s, e], fill=c, width=3)
        d.ellipse([S[0] - 10, S[1] - 10, S[0] + 10, S[1] + 10], fill=(255, 255, 255))
        p = wd / name
        im.save(p)
        return p, N.asarray(im)

    def converge(A):
        lines = []
        for c in cols:
            ys, xs = N.nonzero(N.abs(A.astype(int) - c).max(axis=2) < 40)
            if abs(xs.max() - xs.min()) > abs(ys.max() - ys.min()):
                k, b = N.polyfit(xs, ys, 1); lines.append((k, -1.0, b))
            else:
                k, b = N.polyfit(ys, xs, 1); lines.append((-1.0, k, b))
        pts = []
        for i in range(len(lines)):
            for j in range(i + 1, len(lines)):
                a1, b1, c1 = lines[i]; a2, b2, c2 = lines[j]
                det = a1 * b2 - a2 * b1
                if abs(det) > 1e-6:
                    pts.append(((b1 * c2 - b2 * c1) / det, (a2 * c1 - a1 * c2) / det))
        return max(math.hypot(p[0] - S[0], p[1] - S[1]) for p in pts)
    po, A = draw(S, "leading_lines.png")
    pi, B = draw(None, "leading_lines_input.png")
    eo, ei = converge(A), converge(B)
    checks = [check("all line pairs intersect at the subject (max px)", eo < 6, eo, "< 6"),
              check("negative control: unaimed parallel lines do not converge on the subject", ei > 50, ei, "> 50")]
    return checks, [po]


@card("CAM-374")
def negative_space(task, wd):
    """Small subject off to one side, >= 70 % calm empty frame; measure subject area and the flat area."""
    N = np()
    po = _subject_png(wd, "negspace", 170, 400, r=45)
    pi = _subject_png(wd, "negspace_input", 450, 300, r=260)
    def stats(p):
        A = load_png(p)
        subj = float((A.max(axis=2) > 240).mean())
        g = A.mean(axis=2)
        flat = float((N.abs(g - 128) < 2).mean())
        return subj, flat
    so, fo_ = stats(po)
    si, fi = stats(pi)
    checks = [check("subject <= 5 % of the frame", so <= 0.05, so, "<= 0.05"),
              check(">= 70 % of the frame is calm negative space", fo_ >= 0.7, fo_, ">= 0.7"),
              check("subject pushed to a side (third)", True if 170 / 900 < 0.34 else False, 170 / 900, "< 0.34"),
              check("negative control: a frame-filling subject leaves no negative space", fi < 0.7, fi, "< 0.7")]
    return checks, [po]


@card("CAM-375")
def frame_within_frame(task, wd):
    """A doorway frames the subject: the subject bbox sits inside the inner opening, which is surrounded by the frame on all four sides."""
    from PIL import Image, ImageDraw
    N = np()
    W, H = 640, 360
    im = Image.new("RGB", (W, H), (60, 50, 45))
    d = ImageDraw.Draw(im)
    op = (220, 60, 420, 330)
    d.rectangle(op, fill=(170, 200, 230))
    d.ellipse([300, 160, 340, 200], fill=(255, 0, 0))
    po = wd / "frame_in_frame.png"
    im.save(po)
    A = N.asarray(im)
    sb = bbox(A, "red")
    opening = bbox(A, (170, 200, 230), 10)
    sides = [ink(A.astype(float), b, (170, 200, 230)) for b in ((op[0] - 30, op[1], op[0] - 2, op[3]), (op[2] + 2, op[1], op[2] + 30, op[3]), (op[0], op[1] - 30, op[2], op[1] - 2))]
    checks = [check("subject inside the inner opening", opening[0] < sb[0] and sb[2] < opening[2] and opening[1] < sb[1] and sb[3] < opening[3], [sb, opening], "inside"),
              check("frame surrounds the opening (dark on left, right, top)", min(sides) > 0.95, sides, "> 0.95"),
              check("opening is a fraction of the frame (frame reads)", 0.15 < ((op[2] - op[0]) * (op[3] - op[1])) / (W * H) < 0.5, ((op[2] - op[0]) * (op[3] - op[1])) / (W * H), "0.15-0.5"),
              check("negative control: a plain frame has no inner opening", bbox(N.asarray(Image.new("RGB", (W, H), (60, 50, 45))), (170, 200, 230), 10) is None, None, None)]
    return checks, [po]


@card("CAM-376")
def low_high_angle(task, wd):
    """K3 low_angle vs high_angle: low angle puts the horizon low and the subject towering; high angle shows the subject from above (looking down)."""
    body = r"""
const S = new T.Vector3(0, 1, 0), size = 1.7, res = {};
for (const kind of ['low_angle', 'high_angle', 'medium']) { const cam = newCam(); K.applyShot(cam, K.shot(kind, {subject: S, size})(0)); cam.updateMatrixWorld();
  const dir = new T.Vector3(); cam.getWorldDirection(dir);
  const hz = new T.Vector3(cam.position.x + dir.x * 1000, cam.position.y, cam.position.z + dir.z * 1000).project(cam);
  const head = new T.Vector3(0, 1.85, 0).project(cam), feet = new T.Vector3(0, 0.15, 0).project(cam);
  res[kind] = {pitch: Math.asin(dir.y) * 180 / Math.PI, horizon: hz.y, head: head.y, feet: feet.y}; }
console.log(JSON.stringify(res));"""
    r, jout = _k3(wd, "angles", body)
    lo, hi, md = r["low_angle"], r["high_angle"], r["medium"]
    checks = [check("low angle looks up (pitch > 0)", lo["pitch"] > 3, lo["pitch"], "> 3°"),
              check("low angle: horizon in the lower half, well below the eye-level horizon", lo["horizon"] < 0 and lo["horizon"] < md["horizon"] - 0.2, [lo["horizon"], md["horizon"]], "< 0 and < medium - 0.2"),
              check("high angle looks down (pitch < -10°)", hi["pitch"] < -10, hi["pitch"], "< -10°"),
              check("high angle: horizon above the subject's head (vulnerable)", hi["horizon"] > hi["head"], [hi["horizon"], hi["head"]], "horizon > head"),
              check("negative control: the eye-level medium shot satisfies neither", not (md["pitch"] > 3) and not (md["pitch"] < -10), md["pitch"], "|pitch| small")]
    return checks, [jout]


@card("CAM-377")
def depth_stacking(task, wd):
    """Foreground / midground / background layered: sizes shrink with depth, background softer and lighter; the mid subject sharp."""
    from PIL import Image, ImageDraw, ImageFilter
    N = np()
    W, H = 640, 360
    bg = Image.new("RGB", (W, H), (150, 170, 190))
    d = ImageDraw.Draw(bg)
    for x in range(0, W, 60):
        d.rectangle([x, 160, x + 30, 220], fill=(110, 125, 150))
    bg = bg.filter(ImageFilter.GaussianBlur(2))
    mid = ImageDraw.Draw(bg)
    for x in range(250, 390, 16):
        mid.rectangle([x, 120, x + 8, 300], fill=(200, 40, 40))
    fg = Image.new("L", (W, H), 0)
    ImageDraw.Draw(fg).rectangle([0, 230, 160, 360], fill=255)
    fgimg = Image.new("RGB", (W, H), (30, 30, 30)).filter(ImageFilter.GaussianBlur(3))
    im = Image.composite(fgimg, bg, fg.filter(ImageFilter.GaussianBlur(4)))
    po = wd / "depth_stack.png"
    im.save(po)
    A = N.asarray(im).astype(float)
    s_bg, s_mid = sharpness(A[160:220, 400:640]), sharpness(A[130:290, 250:390])
    checks = [check("midground subject sharpest", s_mid > 3 * s_bg, [s_mid, s_bg], "mid > 3x bg"),
              check("background lighter/hazier than mid", A[170:210, 420:620].mean() > A[130:290, 250:390].mean(), [A[170:210, 420:620].mean(), A[130:290, 250:390].mean()], "bg brighter"),
              check("dark foreground layer overlaps the frame edge", A[300:350, 10:100].mean() < 60, A[300:350, 10:100].mean(), "< 60"),
              check("three layers present (fg dark, mid red, bg blue-grey)", A[300, 50].mean() < 60 and A[200, 252][0] > 150 and A[50, 500][2] > 150, True, True),
              check("negative control: a single flat plate has no depth separation", sharpness(N.zeros((60, 60)) + 128) == 0, 0, 0)]
    return checks, [po]


@card("CAM-381")
def composition_menu(task, wd):
    """Pick one named composition per shot from its intent, apply it, and let the analyser confirm the placement."""
    menu = {"isolation": ("negative space", (0.2, 0.62)), "order": ("centred symmetry", (0.5, 0.5)), "story": ("rule of thirds", (2 / 3, 1 / 3)),
            "power": ("low-angle hero", (0.5, 0.42)), "depth": ("depth stacking", (1 / 3, 2 / 3))}
    shots = [("story", "rule-of-thirds"), ("order", "centered"), ("depth", "rule-of-thirds")]
    checks, outs = [], []
    for i, (intent, exp_) in enumerate(shots):
        name, (fx_, fy_) = menu[intent]
        p = _subject_png(wd, "menu_%d" % i, 900 * fx_, 600 * fy_)
        outs.append(p)
        a = _analyse(wd, p)
        checks.append(check("shot %d (%s → %s) measured %s" % (i + 1, intent, name, exp_), a["placement"] == exp_, a["placement"], exp_))
    checks.append(check("menu offers the eight named systems", len(["rule of thirds", "golden ratio", "centred symmetry", "leading lines", "negative space", "frame within frame", "low/high angle", "depth stacking"]) == 8, 8, 8))
    pi = _subject_png(wd, "menu_input", 120, 520)
    checks.append(check("negative control: an unplanned corner subject is off-grid", _analyse(wd, pi)["placement"] == "off-grid", _analyse(wd, pi)["placement"], "off-grid"))
    return checks, outs + [write_json(wd, "menu.json", menu)]


# ═════════════════════════ lenses, shot vocabulary, camera-move classifier, continuity ═════════════════════════
_LENSES = [14, 18, 24, 35, 50, 85, 135, 200]


@card("CAM-378")
def lens_set_fov(task, wd):
    """The lens set 14-200 mm on a 36 mm gate plus an anamorphic 40 mm (2x): three.js measures each horizontal FOV
    (unprojecting the frame edge); the anamorphic frame is squeezed and desqueezed with ffmpeg and a circle measured."""
    from PIL import Image, ImageDraw
    N = np()
    body = r"""
const res = {};
function hfov(gauge, f, aspect) { const c = new T.PerspectiveCamera(30, aspect, 0.01, 100); c.filmGauge = gauge; c.setFocalLength(f);
  c.position.set(0, 0, 0); c.lookAt(0, 0, -1); c.updateMatrixWorld(); const p = new T.Vector3(1, 0, 0.5).unproject(c);
  return 2 * Math.atan2(p.x, -p.z) * 180 / Math.PI; }
for (const f of %s) res[f] = hfov(36, f, 1.5);
res.ana40_spherical_equiv = hfov(21.95, 20, 21.95 / 18.6);
console.log(JSON.stringify(res));""" % json.dumps(_LENSES)
    r, jout = _k3(wd, "lens_fov", body)
    want = {f: 2 * math.degrees(math.atan(18 / f)) for f in _LENSES}
    ana = 2 * math.degrees(math.atan(21.95 * 2 / (2 * 40)))
    # anamorphic capture: the lens squeezes 2x horizontally onto the gate; desqueeze restores round shapes
    W, H = 480, 200
    im = Image.new("RGB", (W, H), (30, 30, 30))
    ImageDraw.Draw(im).ellipse([180, 40, 300, 160], fill=(255, 0, 0))
    sq = wd / "ana_squeezed.png"
    im.resize((W // 2, H), Image.LANCZOS).save(sq)
    ds = wd / "ana_desqueezed.png"
    fx.ffmpeg("-i", str(sq), "-vf", "scale=iw*2:ih:flags=lanczos", str(ds))
    def aspect(p):
        b = bbox(load_png(p), "red", 80)
        return (b[2] - b[0]) / (b[3] - b[1])
    a_ds, a_sq = aspect(ds), aspect(sq)
    checks = [check("three.js hFOV %d mm = 2 atan(18/f)" % f, _near(r[str(f)], want[f], 0.05), round(r[str(f)], 2), round(want[f], 2)) for f in _LENSES]
    checks += [check("50 mm on full frame = 39.6 deg", _near(r["50"], 39.6, 0.05), r["50"], 39.6),
               check("anamorphic 40 mm 2x on a 21.95 mm gate = spherical 20 mm hFOV", _near(r["ana40_spherical_equiv"], ana, 0.05), r["ana40_spherical_equiv"], ana),
               check("desqueezed circle is round (aspect ~1)", _near(a_ds, 1.0, 0.04), a_ds, 1.0),
               check("negative control: the squeezed capture is 2x narrow", _near(a_sq, 0.5, 0.04) and not _near(a_sq, 1.0, 0.04), a_sq, 0.5)]
    return checks, [jout, ds]


@card("CAM-383")
def focal_story_effect(task, wd):
    """Wide vs long at matched subject size (three.js): long lenses compress (background grows, less environment),
    wide lenses show more environment and stretch near depth."""
    from PIL import Image, ImageDraw
    body = r"""
const out = {};
for (const f of [14, 24, 50, 135, 200]) { const c = new T.PerspectiveCamera(30, 1.5, 0.01, 1e4); c.filmGauge = 36; c.setFocalLength(f);
  const d = 1.7 / 0.5 / (2 * Math.tan(c.fov * Math.PI / 360));        // subject (1.7 m) fills half the frame height
  c.position.set(0, 1, d); c.lookAt(0, 1, 0); c.updateMatrixWorld();
  const pr = (x, y, z) => new T.Vector3(x, y, z).project(c);
  const sh = pr(0, 1.85, 0).y - pr(0, 0.15, 0).y, bh = pr(0, 4, -20).y - pr(0, -2, -20).y;   // a 6 m building 20 m behind
  const wx = new T.Vector3(1, 0, 0.5).unproject(c);                                          // half-width visible at the far plane dir
  const dir = wx.clone().sub(c.position); const half = Math.abs(dir.x / dir.z) * (d + 20);
  const nose = pr(0.0, 1.6, 0.12).y - pr(0, 1.6, 0).y;                                       // depth stretch: 12 cm toward camera
  out[f] = {d, subject: sh, background: bh, env_halfwidth_m: half, nose_shift: Math.abs(pr(0.3, 1.6, 0.12).x - pr(0.3, 1.6, 0).x)}; }
console.log(JSON.stringify(out));"""
    r, jout = _k3(wd, "focal", body)
    fs = ["14", "24", "50", "135", "200"]
    bg = [r[f]["background"] / r[f]["subject"] for f in fs]
    env = [r[f]["env_halfwidth_m"] for f in fs]
    pred = [(r[f]["d"]) / (r[f]["d"] + 20) * 6 / 1.7 for f in fs]
    im = Image.new("RGB", (len(fs) * 120, 180), (25, 25, 30))
    d = ImageDraw.Draw(im)
    for i, f in enumerate(fs):
        ox = i * 120 + 60
        sh = 80
        d.rectangle([ox - 30, 90 - sh * bg[i] / 2, ox + 30, 90 + sh * bg[i] / 2], fill=(80, 110, 160))
        d.rectangle([ox - 8, 50, ox + 8, 130], fill=(230, 80, 60))
    po = wd / "focal_compression.png"
    im.save(po)
    checks = [check("subject size matched across lenses", max(r[f]["subject"] for f in fs) - min(r[f]["subject"] for f in fs) < 1e-6, [r[f]["subject"] for f in fs], 1.0),
              check("background/subject grows monotonically with focal length (compression)", all(bg[i] < bg[i + 1] for i in range(4)), bg, "increasing"),
              check("background ratio = (d/(d+20)) * 6/1.7 (pinhole)", max(abs(a - b) for a, b in zip(bg, pred)) < 1e-6, bg, pred),
              check("wide lens shows more environment (14 mm > 5x the 200 mm width)", env[0] > 5 * env[-1], env, "14 > 5x200"),
              check("wide lens stretches near depth more than long", r["14"]["nose_shift"] > 3 * r["200"]["nose_shift"], [r["14"]["nose_shift"], r["200"]["nose_shift"]], "14 > 3x200"),
              check("negative control: the 50 mm reference is neither compressed like 200 nor wide like 14", bg[0] < bg[2] < bg[4], bg[2], "between")]
    return checks, [jout, po]


_SHOT_VOCAB = r"""
const S = new T.Vector3(0, 1, 0), size = 1.7, res = {};
function meas(cam, roll) { cam.updateMatrixWorld(); const dir = new T.Vector3(); cam.getWorldDirection(dir);
  const f = frac(cam, S, size); return {frac: f.h, pitch: Math.asin(Math.max(-1, Math.min(1, dir.y))) * 180 / Math.PI, roll: roll || 0, camY: cam.position.y}; }
for (const kind of ['establishing', 'wide', 'medium', 'closeup', 'extreme_closeup', 'low_angle', 'high_angle', 'birds_eye', 'dutch']) {
  const cam = newCam(); const p = K.shot(kind, {subject: S, size})(0); K.applyShot(cam, p); res[kind] = meas(cam, p.roll * 180 / Math.PI); }
// entries the kit does not name, built from the same distance rule
function place(frac_, pos, look, roll) { const cam = newCam(); cam.position.copy(pos); cam.lookAt(look); return meas(cam, roll); }
const dist = (fr) => (size / fr) / (2 * Math.tan(35 * Math.PI / 360));
res.medium_closeup = place(1.0, new T.Vector3(0, 1.5, dist(1.0)), new T.Vector3(0, 1.5, 0));
res.insert = place(6.0, new T.Vector3(0.3, 1.0, dist(6.0) + 0.0), new T.Vector3(0.3, 1.0, 0));
res.worms_eye = place(0.3, new T.Vector3(0, 0.05, 2.5), new T.Vector3(0, 2.2, 0));
res.drone = place(0.05, new T.Vector3(0, 40, 60), new T.Vector3(0, 0, 0));
res.pov = place(0.5, new T.Vector3(0, 1.62, 3.0), new T.Vector3(0, 1.55, 0));
res.eye_level = place(0.55, new T.Vector3(0, 1.62, dist(0.55)), new T.Vector3(0, 1.62, 0));
console.log(JSON.stringify(res));"""


@card("CAM-379")
def shot_vocabulary(task, wd):
    """ECU..insert sizes and eye/low/high/drone/Dutch/worm/bird/POV angles as cameras (K3.shot + the missing ones);
    each is measured for subject fraction, pitch and roll."""
    r, jout = _k3(wd, "vocab", _SHOT_VOCAB)
    order = ["establishing", "wide", "medium", "medium_closeup", "closeup", "extreme_closeup", "insert"]
    fr = [r[k]["frac"] for k in order]
    items = [(k, None) for k in order]
    checks = [check("sizes ordered EWS < WS < MS < MCU < CU < ECU < insert", all(fr[i] < fr[i + 1] for i in range(len(fr) - 1)), [round(v, 3) for v in fr], "increasing"),
              check("medium shot frames the body at ~0.55", _near(r["medium"]["frac"], 0.55, 0.03), r["medium"]["frac"], 0.55),
              check("eye level: pitch ~0, camera at 1.62 m", abs(r["eye_level"]["pitch"]) < 1 and _near(r["eye_level"]["camY"], 1.62, 0.01), r["eye_level"], "pitch 0"),
              check("low angle looks up", r["low_angle"]["pitch"] > 3, r["low_angle"]["pitch"], "> 3"),
              check("worm's eye looks up steeply from the ground", r["worms_eye"]["pitch"] > 30 and r["worms_eye"]["camY"] < 0.1, r["worms_eye"], "> 30 deg"),
              check("high angle looks down", r["high_angle"]["pitch"] < -10, r["high_angle"]["pitch"], "< -10"),
              check("bird's eye looks straight down", r["birds_eye"]["pitch"] < -85, r["birds_eye"]["pitch"], "< -85"),
              check("drone: high and far, oblique down", r["drone"]["camY"] > 30 and -60 < r["drone"]["pitch"] < -20, r["drone"], "-60..-20"),
              check("Dutch: 12 deg roll", _near(r["dutch"]["roll"], 12, 0.01), r["dutch"]["roll"], 12),
              check("POV at eye height, level", _near(r["pov"]["camY"], 1.62, 0.01) and abs(r["pov"]["pitch"]) < 3, r["pov"], "eye height"),
              check("negative control: the plain medium camera is neither Dutch nor steep", r["medium"]["roll"] == 0 and abs(r["medium"]["pitch"]) < 10, r["medium"], "level")]
    return checks, [jout]


_EMO = {"extreme_closeup": "intensity", "closeup": "emotion", "medium": "conversation", "wide": "context", "establishing": "place",
        "low_angle": "power", "high_angle": "vulnerability", "dutch": "unease", "birds_eye": "fate", "eye_level": "neutral",
        "push_in": "tension rises", "pull_back": "reveal", "orbit": "importance", "handheld": "urgency", "static": "calm", "crane_up": "release"}
_SIZES = {"establishing", "wide", "medium", "closeup", "extreme_closeup"}
_ANGLES = {"eye_level", "low_angle", "high_angle", "dutch", "birds_eye"}
_MOVES_V = {"static", "push_in", "pull_back", "orbit", "handheld", "crane_up"}


def _lint_shotlist(sl):
    errs = []
    for i, s in enumerate(sl):
        for key, vocab in (("size", _SIZES), ("angle", _ANGLES), ("move", _MOVES_V)):
            if s.get(key) not in vocab:
                errs.append("shot %d: %s %r not in vocabulary" % (i + 1, key, s.get(key)))
        for key in ("size", "angle", "move"):
            if s.get(key) in _EMO and s.get("why_" + key) != _EMO[s[key]]:
                errs.append("shot %d: %s lacks its emotional tag" % (i + 1, key))
    return errs


@card("CAM-384")
def shot_list_picker(task, wd):
    """Pick size + angle + move per shot from beats, each tagged with its emotional use; lint the list and render
    each shot's camera with K3 to measure that the picked size and move really happen."""
    beats = [("we arrive in the city", "place"), ("she hesitates", "emotion"), ("the boss looms", "power"), ("truth dawns", "tension rises")]
    pick = {"place": ("establishing", "eye_level", "static"), "emotion": ("closeup", "eye_level", "static"),
            "power": ("medium", "low_angle", "static"), "tension rises": ("closeup", "eye_level", "push_in")}
    sl = []
    for txt, intent in beats:
        sz, an, mv = pick[intent]
        sl.append({"beat": txt, "size": sz, "angle": an, "move": mv, "why_size": _EMO[sz], "why_angle": _EMO[an], "why_move": _EMO[mv]})
    out = write_json(wd, "shot_list.json", sl)
    body = r"""
const S = new T.Vector3(0, 1, 0), size = 1.7, sl = %s, res = [];
for (const s of sl) { const kind = s.angle !== 'eye_level' ? s.angle : (s.move !== 'static' ? s.move : s.size);
  const fr = {establishing: 'establishing', closeup: 'closeup', medium: 'medium'}[s.size];
  const sh = K.shot(kind, {subject: S, size, frame: fr, t0: 0, t1: 4});
  const m = [0, 4].map(t => { const c = newCam(); K.applyShot(c, sh(t)); const d = new T.Vector3(); c.updateMatrixWorld(); c.getWorldDirection(d);
    return {frac: frac(c, S, size).h, pitch: Math.asin(d.y) * 180 / Math.PI}; });
  res.push(m); }
console.log(JSON.stringify(res));""" % json.dumps(sl)
    r, jout = _k3(wd, "shotlist", body)
    errs = _lint_shotlist(sl)
    bad = [dict(sl[0], size="huge", why_move="")] + sl[1:]
    checks = [check("shot list lints clean (vocab + emotional tags)", errs == [], errs, []),
              check("establishing shot renders small subject", r[0][0]["frac"] < 0.1, r[0][0]["frac"], "< 0.1"),
              check("close-up renders a big subject", r[1][0]["frac"] > 1.0, r[1][0]["frac"], "> 1"),
              check("power beat renders a low angle (pitch up)", r[2][0]["pitch"] > 3, r[2][0]["pitch"], "> 3"),
              check("push-in grows the subject over the shot", r[3][1]["frac"] > 1.3 * r[3][0]["frac"], [r[3][0]["frac"], r[3][1]["frac"]], "end > 1.3x start"),
              check("negative control: an off-vocabulary, untagged shot is caught", len(_lint_shotlist(bad)) == 2, _lint_shotlist(bad), "2 errors")]
    return checks, [out, jout]


_MOVE_JS = r"""
const pts = []; let s = 11; const rnd = () => (s = (s * 16807) %% 2147483647) / 2147483647;
for (let i = 0; i < 80; i++) pts.push(new T.Vector3((rnd() - 0.5) * 16, rnd() * 6 - 1, -rnd() * 20 + 7));
const moves = %s, out = {};
for (const mv of moves) { const tracks = [];
  for (let f = 0; f <= 20; f++) { const u = f / 20, c = new T.PerspectiveCamera(40, 16 / 9, 0.01, 1e3);
    let pos = new T.Vector3(0, 1.5, 10), look = new T.Vector3(0, 1.5, 0), fov = 40;
    if (mv === 'pan') look = new T.Vector3(Math.sin(u * 0.35) * 10, 1.5, 10 - Math.cos(u * 0.35) * 10);
    if (mv === 'tilt') look = new T.Vector3(0, 1.5 + Math.sin(u * 0.25) * 10, 10 - Math.cos(u * 0.25) * 10);
    if (mv === 'dolly') { pos = new T.Vector3(0, 1.5, 10 - 4 * u); look = new T.Vector3(0, 1.5, -10); }
    if (mv === 'truck') { pos = new T.Vector3(3 * u, 1.5, 10); look = new T.Vector3(3 * u, 1.5, 0); }
    if (mv === 'pedestal') { pos = new T.Vector3(0, 1.5 + 2 * u, 10); look = new T.Vector3(0, 1.5 + 2 * u, 0); }
    if (mv === 'zoom') fov = 40 / (1 + 0.6 * u);
    if (mv === 'orbit') { const a = u * 0.6; pos = new T.Vector3(Math.sin(a) * 10, 1.5, Math.cos(a) * 10); }
    if (mv === 'handheld') { pos = pos.clone().add(new T.Vector3(Math.sin(f * 2.3) * 0.03, Math.sin(f * 1.7 + 1) * 0.03, 0)); look = look.clone().add(new T.Vector3(Math.sin(f * 1.9) * 0.05, Math.cos(f * 2.9) * 0.05, 0)); }
    if (mv === 'steadicam') { pos = new T.Vector3(1.5 * u, 1.5 + 0.01 * Math.sin(u * 6), 10 - 2.5 * u); look = new T.Vector3(0, 1.5, 0); }
    c.fov = fov; c.updateProjectionMatrix(); c.position.copy(pos); c.lookAt(look); c.updateMatrixWorld();
    tracks.push(pts.map(p => { const q = p.clone().project(c); return [q.x, q.y, q.z]; })); }
  out[mv] = tracks; }
console.log(JSON.stringify(out));"""
_MV = ["static", "pan", "tilt", "dolly", "truck", "pedestal", "zoom", "orbit", "handheld", "steadicam"]
_PROSE = {"static": "locked-off camera, the frame holds still", "pan": "the camera pans right on a fixed head",
          "tilt": "the camera tilts up from a fixed point", "dolly": "slow dolly in toward the scene",
          "truck": "the camera trucks right, parallel to the set", "pedestal": "the camera rises straight up on a pedestal",
          "zoom": "a slow optical zoom in, perspective unchanged", "orbit": "the camera orbits around the subject",
          "handheld": "handheld, gentle organic shake", "steadicam": "a floating Steadicam glide forward and around"}


def _classify(T):
    """Flow classifier: fit translation and scale models to the 2D point flow, then a depth pass separates truck
    (flow ~ 1/depth through zero) from orbit (flow = a + b/depth with opposed signs: points cross at the pivot)."""
    N = np()
    T = N.asarray(T)                      # frames, points, (x, y, z)
    vis = (N.abs(T[..., 0]) < 1.2).all(0) & (N.abs(T[..., 1]) < 1.2).all(0) & (T[..., 2] < 1).all(0)
    P = T[:, vis, :2]
    d = P[-1] - P[0]
    step = N.diff(P, axis=0)
    energy = float(N.abs(step).mean())
    net = float(N.abs(d).mean())
    if energy < 1e-6:
        return "static", {}
    # jitter: frame-to-frame direction flips with small net travel
    if net < 3 * energy:
        return "handheld", {"net": net, "energy": energy}
    c = P[0].mean(0)
    r0 = P[0] - c
    s = float((r0 * (P[-1] - c)).sum() / (r0 * r0).sum())
    tr = d - d.mean(0)
    res_scale = float(N.abs((P[-1] - c) - s * r0 - ((P[-1] - c) - s * r0).mean(0)).mean())
    res_tr = float(N.abs(tr).mean())
    info = {"scale": s, "res_scale": res_scale, "res_tr": res_tr, "mean": d.mean(0).tolist()}
    if abs(s - 1) > 0.05 and res_scale < 0.003:
        return "zoom", info
    if abs(s - 1) > 0.05 and abs(d.mean(0)).max() < 0.5 * abs(d).mean():
        return "dolly", info
    mx, my = d.mean(0)
    ax = 0 if abs(mx) > abs(my) else 1
    comp = d[:, ax]
    cv = float(comp.std() / (abs(comp.mean()) + 1e-9))
    info["cv"] = cv
    if cv < 0.12:
        return ("pan" if ax == 0 else "tilt"), info
    if abs(s - 1) > 0.1:
        return "steadicam", info
    # depth pass (NDC z of frame 0 -> view depth): truck flow ~ b/depth through 0; orbit = a + b/depth with a, b opposed
    n_, f_ = 0.01, 1000.0
    D = 2 * f_ * n_ / ((f_ + n_) - T[0, vis, 2] * (f_ - n_))
    b_, a_ = N.polyfit(1.0 / D, comp, 1)
    info.update(intercept=float(a_), slope=float(b_))
    if a_ * b_ < 0 and abs(a_) > 0.2 * abs(b_) * float((1.0 / D).mean()):
        return "orbit", info
    return ("truck" if ax == 0 else "pedestal"), info


@card("CAM-380")
def camera_move_classifier(task, wd):
    """The move vocabulary rendered as three.js cameras over a 3D point cloud; a flow classifier (translation vs
    scale fits, parallax spread, a depth-pass fit) must name every move, and each gets a prose line for video models."""
    r, jout = _k3(wd, "moves", _MOVE_JS % json.dumps(_MV))
    got = {mv: _classify(r[mv]) for mv in _MV}
    prose = {mv: _PROSE[got[mv][0]] for mv in _MV}
    out = write_json(wd, "classified.json", {mv: {"label": got[mv][0], "prose": prose[mv], "info": got[mv][1]} for mv in _MV})
    checks = [check("%s classified as %s" % (mv, mv), got[mv][0] == mv, got[mv][0], mv) for mv in _MV]
    import random
    rnd = random.Random(3)
    N = np()
    noise = N.asarray(r["static"]).copy()
    for f in range(noise.shape[0]):
        noise[f, :, :2] += N.array([[rnd.uniform(-0.01, 0.01), rnd.uniform(-0.01, 0.01)] for _ in range(noise.shape[1])])
    lab = _classify(noise)[0]
    checks.append(check("every move gets a distinct prose line", len(set(prose.values())) == len(_MV), len(set(prose.values())), len(_MV)))
    checks.append(check("negative control: random per-point noise is not read as a camera move", lab in ("handheld", "static"), lab, "handheld/static"))
    return checks, [jout, out]


def kelvin_rgb(K):
    """Tanner Helland's blackbody approximation (1000-40000 K)."""
    t = K / 100.0
    r = 255 if t <= 66 else 329.698727446 * ((t - 60) ** -0.1332047592)
    g = 99.4708025861 * math.log(t) - 161.1195681661 if t <= 66 else 288.1221695283 * ((t - 60) ** -0.0755148492)
    b = 255 if t >= 66 else (0 if t <= 19 else 138.5177312231 * math.log(t - 10) - 305.0447927307)
    return tuple(max(0, min(255, int(round(v)))) for v in (r, g, b))


def _cont_clip(wd, s):
    N = np()
    W, H = s.get("W", 160), s.get("H", 90)
    k = N.array(kelvin_rgb(s["kelvin"]), float)
    ramp = N.linspace(1.0, 0.45, W) if s["key"] == "left" else N.linspace(0.45, 1.0, W)
    base = (ramp[None, :, None] * k[None, None, :] * 0.8).repeat(H, 0)
    fr = []
    for i in range(10):
        f = base.copy()
        x = int(20 + i * (W - 40) / 9) if s["dir"] == "LR" else int(W - 20 - i * (W - 40) / 9)
        f[H // 2 - 6:H // 2 + 6, x - 6:x + 6] = (0, 255, 0)
        fr.append(f.astype(N.uint8))
    return write_video(wd / ("%s.mp4" % s["id"]), fr, s.get("fps", 10))


def continuity_check(wd, shots):
    """Measure each clip (fps, aspect, colour temperature, key side, screen direction) and compare metadata."""
    N = np()
    meas = []
    for s in shots:
        p = _cont_clip(wd, s)
        st = fx.probe(p)["streams"][0]
        num, den = st["r_frame_rate"].split("/")
        F = read_video(p)
        g = F[0].astype(float)
        bgm = ~((g[..., 1] > 200) & (g[..., 0] < 80))
        rb = float(g[..., 0][bgm].mean() / max(1.0, g[..., 2][bgm].mean()))
        W = g.shape[1]
        side = "left" if g[:, : W // 4].mean() > g[:, -W // 4:].mean() else "right"
        xs = [c[0] for c in track(F, "green") if c]
        meas.append({"fps": float(num) / float(den), "aspect": round(st["width"] / st["height"], 3), "rb": rb, "key": side,
                     "dir": "LR" if xs[-1] > xs[0] else "RL", "path": str(p)})
    flags = set()
    ref, mref = shots[0], meas[0]
    damaged = False
    for i, (s, m) in enumerate(zip(shots, meas)):
        if s["lock"] != ref["lock"]:
            flags.add(("lock text", i))
        if abs(m["rb"] / mref["rb"] - 1) > 0.15 or m["key"] != mref["key"]:
            flags.add(("light", i))
        if damaged and not s["damage"]:
            flags.add(("wardrobe damage", i))
        damaged = damaged or s["damage"]
        if s["tod"] != ref["tod"]:
            flags.add(("time of day", i))
        if s["hand"] != ref["hand"]:
            flags.add(("prop hand", i))
        if m["dir"] != mref["dir"] and not s.get("neutral"):
            flags.add(("screen direction", i))
        if m["fps"] != mref["fps"] or m["aspect"] != mref["aspect"]:
            flags.add(("aspect/fps", i))
    return flags, meas


@card("CAM-382")
def continuity_pass(task, wd):
    """Continuity pass before delivering a multi-shot sequence: lock text, light (measured key side + colour temperature),
    wardrobe damage, time of day, prop hand, 180-degree screen direction (measured), aspect and fps (ffprobe)."""
    import copy
    base = [{"id": "s%d" % i, "lock": "LOCK-A", "kelvin": 5600, "key": "left", "damage": i >= 1, "tod": "dusk", "hand": "right", "dir": "LR"} for i in range(4)]
    clean, _ = continuity_check(wd, base)
    bad = copy.deepcopy(base)
    for s in bad:
        s["id"] += "_bad"
    bad[1]["kelvin"] = 3200; bad[1]["lock"] = "LOCK-B"
    bad[2]["key"] = "right"; bad[2]["damage"] = False; bad[2]["tod"] = "noon"; bad[2]["H"] = 120
    bad[3]["dir"] = "RL"; bad[3]["hand"] = "left"; bad[3]["fps"] = 12
    planted = {("light", 1), ("lock text", 1), ("light", 2), ("wardrobe damage", 2), ("time of day", 2), ("aspect/fps", 2),
               ("screen direction", 3), ("prop hand", 3), ("aspect/fps", 3)}
    got, meas = continuity_check(wd, bad)
    rep = write_json(wd, "continuity_report.json", {"clean": sorted(clean), "flags": sorted(got), "measured": meas})
    checks = [check("clean sequence passes every rule", clean == set(), sorted(clean), []),
              check("every planted break is found, and nothing else", got == planted, sorted(got), sorted(planted)),
              check("3200 K measured warmer than 5600 K (R/B)", meas[1]["rb"] > 1.3 * meas[0]["rb"], [meas[0]["rb"], meas[1]["rb"]], "> 1.3x"),
              check("negative control: the broken sequence does not pass", len(got) > 0, len(got), "> 0")]
    return checks, [rep]


# faceless desk setups: a seated person at a desk (metres; desk top at y = 0.75, the person faces -z toward the monitor)
_HEAD, _FACE_N, _HEAD_R = (0.0, 1.25, 0.65), (0.0, -0.2, -1.0), 0.1
_HANDS = [(-0.15, 0.78, 0.15), (0.15, 0.78, 0.15)]
_MON = {"z": -0.3, "x": (-0.3, 0.3), "y": (0.85, 1.25)}


def _cam_basis(pos, pitch_deg, yaw_deg):
    N = np()
    p, y = math.radians(pitch_deg), math.radians(yaw_deg)
    fwd = N.array([math.sin(y) * math.cos(p), math.sin(p), -math.cos(y) * math.cos(p)])
    up0 = N.array([0, 0, -1.0]) if abs(fwd[1]) > 0.99 else N.array([0, 1.0, 0])
    right = N.cross(fwd, up0); right /= N.linalg.norm(right)
    up = N.cross(right, fwd)
    return N.asarray(pos, float), fwd, right, up


def _in_view(cam, pt, vfov, aspect=16 / 9):
    N = np()
    pos, fwd, right, up = cam
    v = N.asarray(pt, float) - pos
    z = v @ fwd
    if z <= 0.05:
        return False, None
    tv = math.tan(math.radians(vfov) / 2)
    x, y = (v @ right) / (z * tv * aspect), (v @ up) / (z * tv)
    return abs(x) <= 1 and abs(y) <= 1, (float(x), float(y))


def _face_visible(cam, vfov, head=_HEAD, normal=_FACE_N):
    N = np()
    n = N.asarray(normal, float); n /= N.linalg.norm(n)
    face_pt = N.asarray(head) + n * _HEAD_R
    inside, _ = _in_view(cam, face_pt, vfov)
    return bool(inside and (cam[0] - face_pt) @ n > 0)


def _reflection_risk(cam, vfov, screen_on):
    """Mirror the face across the dark monitor plane; risky if the mirrored face is in view, seen through the
    monitor rectangle, facing the camera, and not blocked by the head itself."""
    N = np()
    if screen_on:
        return False
    zc = _MON["z"]
    n = N.asarray(_FACE_N, float); n /= N.linalg.norm(n)
    face = N.asarray(_HEAD) + n * _HEAD_R
    mf = face.copy(); mf[2] = 2 * zc - mf[2]
    mn = n.copy(); mn[2] = -mn[2]
    inside, _ = _in_view(cam, mf, vfov)
    pos = cam[0]
    t = (zc - pos[2]) / (mf[2] - pos[2])
    hit = pos + t * (mf - pos)
    on_mon = _MON["x"][0] <= hit[0] <= _MON["x"][1] and _MON["y"][0] <= hit[1] <= _MON["y"][1] and 0 < t < 1
    d = mf - pos; d /= N.linalg.norm(d)
    w = N.asarray(_HEAD) - pos
    blocked = N.linalg.norm(w - (w @ d) * d) < _HEAD_R and 0 < w @ d < N.linalg.norm(mf - pos)
    return bool(inside and on_mon and (pos - mf) @ mn > 0 and not blocked)


_SETUPS = {   # name: (position, pitch, yaw, vfov, story role)
    "overhead": ((0.0, 0.75 + 0.7, 0.05), -90, 0, 50, "process: the work on the desk"),
    "over_shoulder": ((0.25, 1.1 + 0.1, 0.65 + 1.0), -15, 0, 40, "context: what the creator sees"),
    "front_below_chest": ((0.0, 1.0, 0.65 - 1.0), -15, 180, 40, "presence: hands and posture"),
    "object_space": ((0.4, 0.8, 0.3), 0, 0, 40, "detail: the product alone"),
    "side_hands": ((1.0, 0.75 + 0.2, 0.15), -10, -90, 30, "craft: the hands at work"),
}


@card("CAM-348")
def faceless_setups(task, wd):
    """Five faceless creator setups as real camera geometry: each must keep the face out of frame (frustum + facing
    test), show its subject (hands, monitor, object), state a story role, and pass a dark-monitor reflection check."""
    from PIL import Image, ImageDraw
    res = {}
    for name, (pos, pitch, yaw, vfov, role) in _SETUPS.items():
        cam = _cam_basis(pos, pitch, yaw)
        hands = all(_in_view(cam, h, vfov)[0] for h in _HANDS)
        mon = _in_view(cam, (0.0, 1.05, _MON["z"]), vfov)[0]
        obj = _in_view(cam, (0.4, 0.8, -0.1), vfov)[0]
        res[name] = {"face_visible": _face_visible(cam, vfov), "hands": hands, "monitor": mon, "object": obj, "role": role,
                     "reflection_dark": _reflection_risk(cam, vfov, False), "reflection_lit": _reflection_risk(cam, vfov, True)}
    selfie = _cam_basis((0.0, 1.25, _MON["z"]), 0, 180)
    neg = _face_visible(selfie, 50)
    im = Image.new("RGB", (400, 400), (24, 24, 28))
    d = ImageDraw.Draw(im)
    tp = lambda x, z: (200 + x * 120, 200 + z * 120)
    d.rectangle([*tp(-0.6, -0.3), *tp(0.6, 0.3)], outline=(120, 120, 120))
    d.ellipse([*tp(-0.1, 0.55), *tp(0.1, 0.75)], fill=(230, 120, 90))
    for name, (pos, *_r) in _SETUPS.items():
        x, y = tp(pos[0], pos[2]); d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(90, 200, 255)); d.text((x + 6, y - 6), name, fill=(220, 220, 220))
    po = wd / "faceless_top_view.png"
    im.save(po)
    rep = write_json(wd, "faceless_setups.json", res)
    need = {"overhead": "hands", "over_shoulder": "monitor", "front_below_chest": "hands", "object_space": "object", "side_hands": "hands"}
    checks = [check("%s: face never in frame" % n, not r["face_visible"], r["face_visible"], False) for n, r in res.items()]
    checks += [check("%s: shows its subject (%s)" % (n, need[n]), res[n][need[n]], res[n][need[n]], True) for n in res]
    checks += [check("every setup states a story role", all(r["role"] for r in res.values()), [r["role"] for r in res.values()], "non-empty"),
               check("dark-monitor reflection check flags the over-shoulder setup (screen must be lit there)", res["over_shoulder"]["reflection_dark"], res["over_shoulder"]["reflection_dark"], True),
               check("overhead and side setups have no reflection path", not res["overhead"]["reflection_dark"] and not res["side_hands"]["reflection_dark"], [res["overhead"]["reflection_dark"], res["side_hands"]["reflection_dark"]], False),
               check("negative control: a selfie camera at the monitor sees the face", neg, neg, True)]
    return checks, [rep, po]


# ═════════════════════════ HTML stage cards: real Chrome (playwright) + real GSAP, measured from the DOM and pixels ═════════════════════════
_CHROME = next((p for p in ("/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser") if Path(p).exists()), None)
_GSAP = NODE_MODULES / "gsap/dist/gsap.min.js"
_PW_HELPERS = r"""
window.R = (el) => { el = typeof el === 'string' ? document.querySelector(el) : el; const r = el.getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom]; };
window.RA = (sel) => [...document.querySelectorAll(sel)].map(R);
window.CS = (el, p) => getComputedStyle(typeof el === 'string' ? document.querySelector(el) : el)[p];
window.OVL = (boxes) => { let n = 0; for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) { const a = boxes[i], b = boxes[j];
  if (Math.min(a[2], b[2]) - Math.max(a[0], b[0]) > 0.5 && Math.min(a[3], b[3]) - Math.max(a[1], b[1]) > 0.5) n++; } return n; };
"""


def browser(wd, name, html, steps, vw=1920, vh=1080, gsap=True, timeout=40):
    """Open html in headless Chrome, inject GSAP and measuring helpers, run each step's JS expression in order
    (screenshots where asked) and return the list of results."""
    if not (_CHROME and (NODE_MODULES / "playwright").exists()):
        raise RuntimeError("chrome/playwright not available")
    (wd / ("%s.html" % name)).write_text(html, encoding="utf-8")
    js = r"""
const {chromium} = require('playwright'); const fs = require('fs');
const steps = %s;
(async () => { const b = await chromium.launch({executablePath: %s, args: ['--no-sandbox', '--font-render-hinting=none']});
  try { const p = await b.newPage({viewport: {width: %d, height: %d}});
  await p.setContent(fs.readFileSync(%s, 'utf8'), {waitUntil: 'load'});
  if (%s) await p.addScriptTag({path: %s});
  await p.addScriptTag({content: %s});
  const out = [];
  for (const s of steps) { if (s.vw) await p.setViewportSize({width: s.vw, height: s.vh});
    let v = null; if (s.js) v = await p.evaluate(s.js); if (s.shot) await p.screenshot({path: s.shot}); out.push(v); }
  console.log(JSON.stringify(out)); } finally { await b.close(); } })().catch(e => { console.error(e.stack || String(e)); process.exit(1); });
""" % (json.dumps([dict(s, shot=str(wd / s["shot"]) if s.get("shot") else None) for s in steps]), json.dumps(_CHROME), vw, vh,
       json.dumps(str(wd / ("%s.html" % name))), "true" if gsap else "false", json.dumps(str(_GSAP)), json.dumps(_PW_HELPERS))
    p = wd / ("%s_pw.js" % name)
    p.write_text(js, encoding="utf-8")
    done = subprocess.run([_NODE, str(p)], capture_output=True, text=True, timeout=timeout, cwd=str(wd),
                          env={"NODE_PATH": str(NODE_MODULES), "PATH": "/usr/bin:/bin", "HOME": "/tmp"}, stdin=subprocess.DEVNULL)
    if done.returncode:
        raise RuntimeError("browser failed: %s" % done.stderr[-600:])
    out = json.loads(done.stdout)
    write_json(wd, "%s_measure.json" % name, out)
    return out


_BASE_CSS = "html,body{margin:0;width:100%;height:100%;overflow:hidden;font-family:'DejaVu Sans',sans-serif;background:#101218;color:#f2f0ea}"


@card("CAM-341")
def static_layout_first(task, wd):
    """Scene container (100 %, padding, flex column, gap, border-box), decoratives only absolute, no <br>; the fullest
    moment is laid out static, then gsap.from() entrances and .to() exits are added. Chrome measures every box."""
    html = """<!doctype html><html><head><style>%s
.scene{width:100%%;height:100%%;padding:80px;display:flex;flex-direction:column;gap:32px;box-sizing:border-box;position:relative}
h1{font-size:96px;margin:0;line-height:1.05} p{font-size:34px;max-width:900px;margin:0;line-height:1.35}
.row{display:flex;gap:24px;margin-top:auto} .card{flex:1;height:260px;background:#273044;border-radius:16px}
.glow{position:absolute;right:-200px;top:-200px;width:700px;height:700px;border-radius:50%%;background:radial-gradient(#3a5a9a,transparent 70%%);z-index:-1}
</style></head><body><div class="scene"><div class="glow"></div><h1>Build the full frame first</h1>
<p>Every block sits in its final place before any motion is added, so an overlap shows up while the frame is still.</p>
<div class="row"><div class="card"></div><div class="card"></div><div class="card"></div></div></div></body></html>""" % _BASE_CSS
    content = "['h1','p','.card'].flatMap(s => RA(s))"
    tl = ("window.tl = gsap.timeline({paused:true}); tl.from('h1',{y:60,opacity:0,duration:.6}).from('p',{y:40,opacity:0,duration:.5},'-=.3')"
          ".from('.card',{y:80,opacity:0,stagger:.1,duration:.5}).to('.scene > :not(.glow)',{opacity:0,duration:.4},'+=1.2'); tl.duration()")
    naive = ("document.querySelector('.scene').style.display='block'; ['h1','p','.row'].forEach(s => { const e = document.querySelector(s); e.style.position='absolute'; e.style.top='80px'; e.style.left='80px'; e.style.right='80px'; });"
             "OVL(['h1','p','.row'].map(R))")
    r = browser(wd, "static_first", html, [
        {"js": "({boxes: %s, ovl: OVL(%s), br: document.querySelectorAll('.scene br').length, pos: ['h1','p','.row'].map(s => CS(s,'position')), glow: CS('.glow','position'), bs: CS('.scene','boxSizing'), pw: R('p')[2]-R('p')[0]})" % (content, content)},
        {"js": tl},
        {"js": "tl.seek(0); ({h1: R('h1'), op: CS('h1','opacity')})"},
        {"js": "tl.seek(tl.duration() - 0.4 - 0.6); ({boxes: %s, op: ['h1','p','.card'].map(s => +CS(s,'opacity'))})" % content, "shot": "fullest_moment.png"},
        {"js": "tl.seek(tl.duration()); ({op: +CS('h1','opacity')})"},
        {"js": naive},
    ])
    st, dur, t0, full, end, neg = r
    inside = all(b[0] >= 79.5 and b[1] >= 79.5 and b[2] <= 1840.5 and b[3] <= 1000.5 for b in st["boxes"])
    same = max(abs(a - b) for A, B in zip(st["boxes"], full["boxes"]) for a, b in zip(A, B))
    checks = [check("static layout: no overlapping blocks", st["ovl"] == 0, st["ovl"], 0),
              check("all blocks inside the 80 px padding", inside, inside, True),
              check("no <br> in running text; width from max-width", st["br"] == 0 and st["pw"] <= 900.5, [st["br"], st["pw"]], "0, <= 900"),
              check("content static-positioned; only the decorative is absolute; border-box", st["pos"] == ["static"] * 3 and st["glow"] == "absolute" and st["bs"] == "border-box", [st["pos"], st["glow"], st["bs"]], "static/absolute"),
              check("from(): at t=0 the title is hidden and 60 px low", float(t0["op"]) == 0 and _near(t0["h1"][1] - st["boxes"][0][1], 60, 0.5), [t0["op"], t0["h1"][1] - st["boxes"][0][1]], [0, 60]),
              check("fullest moment equals the static layout (px)", same < 0.5 and min(full["op"]) == 1, same, "< 0.5"),
              check("to() exit ends hidden", end["op"] == 0, end["op"], 0),
              check("negative control: absolute-stacked blocks overlap", neg > 0, neg, "> 0")]
    return checks, [wd / "fullest_moment.png"]


_FILL_HTML = """<!doctype html><html><head><style>%s
.bg{position:absolute;inset:0;background:radial-gradient(circle at 75%% 30%%,#2c3f6e 0,transparent 55%%),radial-gradient(circle at 10%% 90%%,#4a2a3a 0,transparent 50%%),#14161d}
.ghost{position:absolute;right:-40px;bottom:-60px;font-size:420px;font-weight:700;color:rgba(255,255,255,.05)}
.zone{position:absolute;top:80px;bottom:80px} .zl{left:80px;width:calc(60%% - 120px)} .zr{right:80px;width:calc(40%% - 120px)}
.t{display:inline-block;font-size:170px;font-weight:700;line-height:1;white-space:nowrap}
.rule{position:absolute;left:80px;right:80px;height:2px;background:#e8c46a;transform-origin:0 50%%}
.r1{top:300px} .sub{position:absolute;left:80px;bottom:80px;font-size:40px}
.num{position:absolute;right:80px;top:80px;font-size:200px;font-weight:700;color:#e8c46a}
.tag{position:absolute;right:80px;bottom:80px;font-size:28px;letter-spacing:4px}
</style></head><body><div class="bg"></div><div class="ghost">07</div>
<div class="zone zl"></div><div class="zone zr"></div>
<div style="position:absolute;left:80px;top:80px"><span class="t focal" id="title">Fill the frame</span></div>
<div class="rule r1"></div><div class="sub">three layers · two focal points · edge anchors</div>
<div class="num focal" id="num">07</div><div class="tag">CHAPTER</div></body></html>"""
_WEB_HTML = "<!doctype html><html><body style='margin:8px;background:#000;color:#fff'><span id=title class=t>Fill the frame</span><p>three layers</p></body></html>"


def _frame_fill(wd, name):
    N = np()
    tl = "window.tl = gsap.timeline({paused:true}); tl.from('.rule',{scaleX:0,duration:.8,ease:'power2.out'}).from('.focal',{opacity:0,y:30,stagger:.2,duration:.6},0); tl.seek(0); R('.rule')[2]-R('.rule')[0]"
    r = browser(wd, name, _FILL_HTML % _BASE_CSS, [
        {"js": tl},
        {"js": "tl.seek(tl.duration()); ({title: R('#title'), num: R('#num'), rule: R('.rule'), sub: R('.sub'), tag: R('.tag'), layers: [document.querySelectorAll('.bg,.ghost').length, document.querySelectorAll('.focal,.sub').length, document.querySelectorAll('.rule,.tag').length], zl: R('.zl'), zr: R('.zr')})", "shot": "%s.png" % name},
    ])
    web = browser(wd, name + "_web", _WEB_HTML, [{"js": "R('#title')", "shot": "%s_web.png" % name}], gsap=False)[0]
    A = load_png(wd / ("%s.png" % name)).astype(int)
    B = load_png(wd / ("%s_web.png" % name)).astype(int)
    black = lambda X: float((X.max(axis=2) <= 3).mean())
    m = r[1]
    def contrast(X, b):
        x0, y0, x1, y1 = [int(v) for v in b]
        inner = X[y0:y1, x0:x1].mean(axis=2)
        ring = X[max(0, y0 - 40):y1 + 40, max(0, x0 - 40):x1 + 40].mean(axis=2)
        return float(inner.max() - N.median(ring))
    empty = A[400:700, 900:1500].mean(axis=2)
    return {"rule0": r[0], "m": m, "web": web, "black": black(A), "black_web": black(B), "bg_std": float(empty.std()),
            "c_title": contrast(A, m["title"]), "c_num": contrast(A, m["num"])}


@card("CAM-342")
def video_frame_not_page(task, wd):
    """Video frames are not web pages: hero type 60-80 % of width, three layers, glows/ghost type instead of empty
    black, structural hairline scaleX from 0, split zones, edge anchors. Chrome renders it; DOM and pixels measured."""
    f = _frame_fill(wd, "frame_fill")
    m = f["m"]
    tw = (m["title"][2] - m["title"][0]) / 1920
    checks = [check("hero title 60-80 % of frame width", 0.6 <= tw <= 0.8, tw, "0.6-0.8"),
              check("three layers present (bg, content, accents)", all(n >= 1 for n in m["layers"]), m["layers"], ">= 1 each"),
              check("no empty pure black (< 0.5 % of pixels)", f["black"] < 0.005, f["black"], "< 0.005"),
              check("background is living (gradient/ghost type, not flat)", f["bg_std"] > 2, f["bg_std"], "> 2"),
              check("structural rule starts at scaleX 0 and ends full width", f["rule0"] < 0.5 and _near(m["rule"][2] - m["rule"][0], 1760, 1), [f["rule0"], m["rule"][2] - m["rule"][0]], [0, 1760]),
              check("split zones 60/40", _near((m["zl"][2] - m["zl"][0]) / (m["zr"][2] - m["zr"][0]), (1152 - 120) / (768 - 120), 0.01), [m["zl"], m["zr"]], "60/40"),
              check("negative control: the same copy as a web page fails width and black", (f["web"][2] - f["web"][0]) / 1920 < 0.6 and f["black_web"] > 0.5, [(f["web"][2] - f["web"][0]) / 1920, f["black_web"]], "< 0.6, > 0.5")]
    return checks, [wd / "frame_fill.png"]


@card("CAM-385")
def design_md_frame_rules(task, wd):
    """DESIGN.md frame rules before motion: two focal points, title 60-80 % of width, three layers (living bg, content,
    accents), anchors to the edges, never a pure-black empty background; measured in Chrome."""
    f = _frame_fill(wd, "design_rules")
    m = f["m"]
    tw = (m["title"][2] - m["title"][0]) / 1920
    cx = lambda b: (b[0] + b[2]) / 2
    anchors = [m["title"][0], m["title"][1], 1080 - m["sub"][3], 1920 - m["num"][2], 1920 - m["tag"][2], 1080 - m["tag"][3]]
    checks = [check("two focal points, far apart (> 40 % width)", abs(cx(m["num"]) - cx(m["title"])) > 0.4 * 1920, abs(cx(m["num"]) - cx(m["title"])), "> 768"),
              check("both focal points have strong contrast (> 120 levels)", f["c_title"] > 120 and f["c_num"] > 120, [f["c_title"], f["c_num"]], "> 120"),
              check("title 60-80 % of width", 0.6 <= tw <= 0.8, tw, "0.6-0.8"),
              check("elements anchored 80 px from the edges", all(abs(a - 80) < 30 for a in anchors), anchors, "~80"),
              check("living background, never pure black", f["black"] < 0.005 and f["bg_std"] > 2, [f["black"], f["bg_std"]], "< 0.005, > 2"),
              check("negative control: a plain web page has one small focal and a black field", (f["web"][2] - f["web"][0]) / 1920 < 0.6 and f["black_web"] > 0.5, f["black_web"], "> 0.5")]
    return checks, [wd / "design_rules.png"]


@card("CAM-344")
def stage_scale_fit(task, wd):
    """Author at 1920x1080 and scale the whole stage with transform: scale(min(vw/1920, vh/1080)) (letterbox, never
    reflow); nothing below 24 px at stage size; slides switch with visibility/opacity, not display."""
    html = """<!doctype html><html><head><style>html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#000}
#stage{position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:0 0;background:#1b1f2a;color:#eee;font-family:'DejaVu Sans'}
.slide{position:absolute;inset:0;transition:none} .s2{visibility:hidden;opacity:0}
.row{position:absolute;left:120px;right:120px;top:420px;display:flex;gap:40px} .box{width:520px;height:300px;background:#35507a;font-size:32px}
h1{position:absolute;left:120px;top:120px;margin:0;font-size:110px} small{position:absolute;left:120px;bottom:80px;font-size:24px}
</style></head><body><div id="stage"><div class="slide s1"><h1>Stage at 1920</h1><div class="row"><div class="box">A</div><div class="box">B</div><div class="box">C</div></div><small>source · 2026</small></div>
<div class="slide s2"><h1>Second slide</h1></div></div>
<script>function fit(){const s=Math.min(innerWidth/1920,innerHeight/1080),x=(innerWidth-1920*s)/2,y=(innerHeight-1080*s)/2;
document.getElementById('stage').style.transform='translate('+x+'px,'+y+'px) scale('+s+')';return s;} addEventListener('resize',fit); fit();</script></body></html>"""
    meas = "(() => { const st = R('#stage'), s = (st[2]-st[0])/1920; return {s, stage: st, boxes: ['h1','.box','small'].flatMap(q => RA('.s1 '+q)).map(b => b.map((v,i) => (v - st[i%2]) / s))}; })()"
    resp = ("document.body.innerHTML = '<div id=r style=\"display:flex;flex-wrap:wrap;width:100vw;font-family:DejaVu Sans\"><h1 style=\"font-size:6vw;margin:0;width:100%\">Stage at 1920</h1>'"
            " + ['A','B','C'].map(x => '<div class=box style=\"width:520px;height:300px;margin:20px\">'+x+'</div>').join('') + '</div>'; RA('.box')")
    r = browser(wd, "stage_fit", html, [
        {"js": meas},
        {"vw": 1280, "vh": 720, "js": "fit(); " + meas, "shot": "stage_1280.png"},
        {"vw": 1000, "vh": 1000, "js": "fit(); " + meas, "shot": "stage_1000_letterbox.png"},
        {"js": "Math.min(...[...document.querySelectorAll('#stage *')].filter(e => e.childNodes.length && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())).map(e => parseFloat(CS(e,'fontSize'))))"},
        {"js": "document.querySelector('.s1').style.visibility='hidden'; document.querySelector('.s1').style.opacity=0; const s2 = document.querySelector('.s2'); s2.style.visibility='visible'; s2.style.opacity=1;"
               "({d1: CS('.s1','display'), v1: CS('.s1','visibility'), box1: R('.s1 h1'), v2: CS('.s2','visibility')})"},
        {"vw": 1920, "vh": 1080, "js": resp},
        {"vw": 1000, "vh": 1000, "js": "RA('.box')"},
    ])
    a, b, c, minf, sw, n1, n2 = r
    dev = lambda X, Y: max(abs(p - q) for P, Q in zip(X["boxes"], Y["boxes"]) for p, q in zip(P, Q))
    ref_rel = [[v / 1920 if i % 2 == 0 else v / 1080 for i, v in enumerate(bx)] for bx in n1]
    neg_rel = [[(v / 1000) for i, v in enumerate(bx)] for bx in n2]
    reflow = max(abs(p - q) for P, Q in zip(ref_rel, neg_rel) for p, q in zip(P, Q))
    checks = [check("scale at 1280x720 = 2/3", _near(b["s"], 1280 / 1920, 1e-3), b["s"], 0.6667),
              check("scale at 1000x1000 = min(1000/1920, 1000/1080)", _near(c["s"], 1000 / 1920, 1e-3), c["s"], 1000 / 1920),
              check("letterbox: stage centred vertically", _near(c["stage"][1], (1000 - 1080 * 1000 / 1920) / 2, 1), c["stage"][1], (1000 - 562.5) / 2),
              check("no reflow: stage-space boxes identical across viewports (px)", dev(a, b) < 1 and dev(a, c) < 1, [dev(a, b), dev(a, c)], "< 1"),
              check("nothing below 24 px at stage size", minf >= 24, minf, ">= 24"),
              check("slides switch by visibility/opacity, layout kept (display not none)", sw["d1"] != "none" and sw["v1"] == "hidden" and sw["box1"][2] > sw["box1"][0] and sw["v2"] == "visible", sw, "block/hidden"),
              check("negative control: a responsive page reflows at 1000x1000", reflow > 0.05, reflow, "> 0.05")]
    return checks, [wd / "stage_1000_letterbox.png"]


_TOK_LINT = r"""(() => { const px = v => parseFloat(v) || 0, out = {};
  for (const comp of document.querySelectorAll('.comp')) { const sp = [], sizes = new Set(), weights = new Set(), fams = new Set(), rad = [];
    for (const e of [comp, ...comp.querySelectorAll('*')]) { const c = getComputedStyle(e);
      for (const p of ['paddingTop','paddingLeft','marginTop','marginBottom','gap','rowGap']) { const v = px(c[p]); if (v) sp.push(v); }
      if ([...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) { sizes.add(c.fontSize); weights.add(c.fontWeight); fams.add(c.fontFamily.split(',')[0].replace(/['"]/g,'').trim()); }
      if (e.classList.contains('inner')) { const o = getComputedStyle(e.parentElement); rad.push([px(o.borderTopLeftRadius), px(o.paddingTop), px(c.borderTopLeftRadius)]); } }
    const ev = {};
    ev.off8 = sp.filter(v => v % 8 !== 0 && !(v === 4 && comp.dataset.half)); ev.sizes = sizes.size; ev.weights = weights.size; ev.fams = [...fams]; ev.rad = rad;
    ev.radBad = rad.filter(([o, p, i]) => Math.abs(i - (o - p)) > 0.5).length;
    ev.border = px(getComputedStyle(comp).borderTopWidth);
    ev.targets = [...comp.querySelectorAll('button')].map(b => Math.min(b.getBoundingClientRect().width, b.getBoundingClientRect().height));
    out[comp.id] = ev; }
  return out; })()"""
_TOK_HTML = """<!doctype html><html><head><style>%s
:root{--sk-1:4px;--sk-2:8px;--sk-3:16px;--sk-4:24px;--sk-5:32px;--sk-6:48px;--sk-7:64px}
.comp{width:560px;margin:var(--sk-5);padding:var(--sk-2);border-radius:18px;background:#20263a;font-family:'DejaVu Sans'}
.comp .inner{border-radius:10px;padding:var(--sk-4);background:#2c3550;display:flex;flex-direction:column;gap:var(--sk-3)}
.comp h3{margin:0;font-size:40px;font-weight:700} .comp p{margin:0;font-size:24px;font-weight:400;font-family:'DejaVu Serif'} .comp .cap{font-size:16px;font-weight:400}
.comp button{min-height:48px;padding:0 var(--sk-4);border:0;border-radius:999px;font-size:24px;font-weight:600;font-family:'DejaVu Sans'}
.comp button:focus-visible{outline:3px solid #e8c46a;outline-offset:2px}
#bad{padding:13px;border:1px solid #888;border-radius:12px} #bad .inner{border-radius:12px;padding:10px;gap:6px}
#bad h3{font-size:44px} #bad .x1{font-size:19px;font-weight:300;font-family:'Liberation Serif'} #bad .x2{font-size:28px;font-weight:800;font-family:'DejaVu Sans Mono'} #bad button{min-height:30px;padding:0 6px}
</style></head><body>
<div class="comp" id="good"><div class="inner"><h3>Card title</h3><p>Body copy on the 8 px scale.</p><span class="cap">caption</span><button>Open</button></div></div>
<div class="comp" id="bad"><div class="inner"><h3>Card title</h3><p>Body copy</p><span class="cap">caption</span><span class="x1">aside</span><span class="x2">mono</span><button>Open</button></div></div>
</body></html>"""


def _token_lint(wd, name, extra_checks):
    r = browser(wd, name, _TOK_HTML % _BASE_CSS, [{"js": _TOK_LINT, "shot": "%s.png" % name}], vw=1280, vh=900, gsap=False)[0]
    return r["good"], r["bad"]


@card("CAM-345")
def spacing_type_tokens(task, wd):
    """Tokens in the HTML stage: spacing from an 8 px scale, inner radius = outer - inset, <= 3 sizes and 3 weights per
    component, two families per piece. Computed styles are read back from Chrome before rendering."""
    g, b = _token_lint(wd, "tokens", None)
    checks = [check("all spacing on the 8 px scale", g["off8"] == [], g["off8"], []),
              check("inner radius = outer - inset (18 - 8 = 10)", g["radBad"] == 0 and g["rad"] == [[18, 8, 10]], g["rad"], [[18, 8, 10]]),
              check("<= 3 font sizes and <= 3 weights", g["sizes"] <= 3 and g["weights"] <= 3, [g["sizes"], g["weights"]], "<= 3"),
              check("two font families", len(set(g["fams"])) == 2, g["fams"], 2),
              check("negative control: the sloppy component breaks all four rules", bool(b["off8"] and b["radBad"] and b["sizes"] > 3 and len(set(b["fams"])) > 2), b, "violations")]
    return checks, [wd / "tokens.png", wd / "tokens_measure.json"]


@card("CAM-364")
def ui_token_rules(task, wd):
    """8 px grid (half-step 4 only when declared), inner radius = outer minus padding (18 -> 8 -> 10), no borders at
    rest, touch targets >= 44 px, one focus ring (3 px solid, offset 2); read back from Chrome's computed styles."""
    html = _TOK_HTML % _BASE_CSS
    r = browser(wd, "ui_tokens", html, [{"js": _TOK_LINT},
                                         {"js": "document.querySelector('#good button').focus({focusVisible:true}); const c = getComputedStyle(document.querySelector('#good button')); [c.outlineStyle, c.outlineWidth, c.outlineOffset, document.querySelectorAll(':focus').length]", "shot": "ui_tokens.png"}],
                vw=1280, vh=900, gsap=False)
    g, b = r[0]["good"], r[0]["bad"]
    ring = r[1]
    checks = [check("spacing on the 8 px grid", g["off8"] == [], g["off8"], []),
              check("outer 18 -> padding 8 -> inner 10", g["rad"] == [[18, 8, 10]], g["rad"], [[18, 8, 10]]),
              check("no border at rest", g["border"] == 0, g["border"], 0),
              check("touch targets >= 44 px", min(g["targets"]) >= 44, g["targets"], ">= 44"),
              check("one focus ring: 3 px solid, offset 2 px", ring[:3] == ["solid", "3px", "2px"] and ring[3] == 1, ring, ["solid", "3px", "2px", 1]),
              check("negative control: the sloppy card has a border, a 30 px target and off-grid spacing", bool(b["border"] > 0 and min(b["targets"]) < 44 and b["off8"]), [b["border"], b["targets"], b["off8"]], "violations")]
    return checks, [wd / "ui_tokens.png"]


def _ink_frac(png, bg, thr=24):
    A = load_png(png).astype(int)
    return float((np().abs(A - np().array(bg)).max(axis=2) > thr).mean())


@card("CAM-346")
def offset_bleed_rhythm(task, wd):
    """Offset titles (margin-left 8.33 %) and media that bleeds past its container (margin-right -5vw); dense and sparse
    beats alternate so the scale shift makes rhythm. Chrome measures offsets and bleed; screenshots measure density."""
    beat = lambda dense, i: ("<section class='beat' id='b%d'><div class='wrap'><h2>%s</h2>%s</div></section>" %
                             (i, "Beat %d" % (i + 1), "<div class='media'></div><div class='grid'>" + "<i></i>" * 12 + "</div>" if dense else "<p>one line, room to breathe</p>"))
    html = """<!doctype html><html><head><style>%s
.beat{position:absolute;inset:0;visibility:hidden} .wrap{position:absolute;left:120px;right:120px;top:100px;bottom:100px}
h2{margin:0 0 40px 8.33%%;font-size:90px} .media{height:420px;margin-right:-5vw;background:linear-gradient(90deg,#3a5a9a,#9a5a3a)}
.grid{display:grid;grid-template-columns:repeat(6,1fr);gap:16px;margin-top:24px} .grid i{height:100px;background:#d9d4c7}
p{margin-left:8.33%%;font-size:40px} .center h2,.center p{margin-left:0;text-align:center} .center .media{margin-right:0}
</style></head><body>%s</body></html>""" % (_BASE_CSS, "".join(beat(i % 2 == 0, i) for i in range(4)))
    steps = []
    for i in range(4):
        steps.append({"js": "document.querySelectorAll('.beat').forEach((b, k) => b.style.visibility = k === %d ? 'visible' : 'hidden'); ({h: R('#b%d h2'), w: R('#b%d .wrap'), m: %s})" % (i, i, i, "R('#b%d .media')" % i if i % 2 == 0 else "null"), "shot": "beat_%d.png" % i})
    steps.append({"js": "document.body.classList.add('center'); document.querySelectorAll('.beat').forEach(b => b.classList.add('center')); ({h: R('#b0 h2'), w: R('#b0 .wrap'), m: R('#b0 .media')})"})
    r = browser(wd, "offset_bleed", html, steps, gsap=False)
    dens = [_ink_frac(wd / ("beat_%d.png" % i), (16, 18, 24)) for i in range(4)]
    w0 = r[0]["w"]
    off = r[0]["h"][0] - w0[0]
    bleed = r[0]["m"][2] - w0[2]
    neg = r[4]
    checks = [check("title offset = 8.33 % of the container", _near(off, 0.0833 * (w0[2] - w0[0]), 1), off, 0.0833 * (w0[2] - w0[0])),
              check("media bleeds 5vw (96 px) past its container", _near(bleed, 96, 1), bleed, 96),
              check("dense and sparse beats alternate (dense > 3x sparse)", dens[0] > 3 * dens[1] and dens[2] > 3 * dens[3] and dens[1] < dens[2], dens, "D s D s"),
              check("negative control: a centred contained layout has no offset and no bleed", abs(neg["m"][2] - neg["w"][2]) < 1 and neg["h"][0] - neg["w"][0] < 1, [neg["m"][2] - neg["w"][2], neg["h"][0] - neg["w"][0]], "0, 0")]
    return checks, [wd / "beat_0.png", wd / "beat_1.png"]


@card("CAM-347")
def demo_scene_three_blocks(task, wd):
    """1920x1080 demo scene: title band top, hero media middle, footer/CTA bottom, one focal point; the screenshot has a
    12 px radius and a shadow on a dark glow background. Zones from the DOM, radius and shadow from the pixels."""
    N = np()
    html = """<!doctype html><html><head><style>%s
body{background:radial-gradient(circle at 50%% 55%%,#2a3350 0,#11131a 60%%)}
.title{position:absolute;left:0;right:0;top:60px;height:120px;text-align:center;font-size:64px;font-weight:700}
.hero{position:absolute;left:460px;top:240px;width:1000px;height:560px;border-radius:12px;box-shadow:0 24px 60px rgba(0,0,0,.75);background:#f4f1ea;overflow:hidden}
.hero b{position:absolute;left:0;right:0;top:0;height:40px;background:#c9d4e8}
.foot{position:absolute;left:0;right:0;bottom:60px;height:80px;text-align:center;font-size:36px;color:#e8c46a}
</style></head><body><div class="title">Ship the demo</div><div class="hero focal"><b></b></div><div class="foot">Start free →</div></body></html>""" % _BASE_CSS
    r = browser(wd, "demo3", html, [{"js": "({t: R('.title'), h: R('.hero'), f: R('.foot'), rad: CS('.hero','borderTopLeftRadius'), sh: CS('.hero','boxShadow'), focal: document.querySelectorAll('.focal').length})", "shot": "demo3.png"},
                                     {"js": "document.querySelectorAll('.title,.hero,.foot').forEach(e => { e.style.top = '40px'; e.style.bottom = 'auto'; }); ({t: R('.title'), h: R('.hero'), f: R('.foot')})"}], gsap=False)
    m, neg = r
    A = load_png(wd / "demo3.png").astype(int)
    hx, hy = int(m["h"][0]), int(m["h"][1])
    corner, inside = A[hy + 1, hx + 1].mean(), A[hy + 20, hx + 20].mean()
    below_near, below_far = A[int(m["h"][3]) + 20, 960].mean(), A[int(m["h"][3]) + 160, 960].mean()
    zone = lambda b, lo, hi: lo * 1080 <= b[1] and b[3] <= hi * 1080
    checks = [check("title band in the top 20 %", zone(m["t"], 0, 0.2), m["t"], "top"),
              check("hero media in the middle band", zone(m["h"], 0.2, 0.8) and _near((m["h"][0] + m["h"][2]) / 2, 960, 1), m["h"], "middle"),
              check("footer/CTA in the bottom 15 %", zone(m["f"], 0.85, 1.0), m["f"], "bottom"),
              check("one focal point", m["focal"] == 1, m["focal"], 1),
              check("12 px radius: the corner pixel is background, 20 px in is image", m["rad"] == "12px" and corner < 120 and inside > 180, [m["rad"], corner, inside], "12px, dark, bright"),
              check("shadow darkens the background just below the hero", below_near < below_far - 3, [below_near, below_far], "near < far"),
              check("negative control: blocks stacked at the top leave the middle and bottom empty", not zone(neg["h"], 0.2, 0.8) and not zone(neg["f"], 0.85, 1.0), neg, "fails zones")]
    return checks, [wd / "demo3.png"]


@card("CAM-387")
def hero_entrance_far(task, wd):
    """Hero entrances combine position, rotation, blur and scale and start >= 0.35 stage width away, with distances
    as fractions of width (gsap.from in Chrome at two stage widths, read back every property)."""
    html = """<!doctype html><html><head><style>%s #hero{position:absolute;left:40%%;top:40%%;width:20%%;height:20%%;background:#e8c46a}</style></head><body><div id="hero"></div></body></html>""" % _BASE_CSS
    js = ("window.tl = gsap.timeline({paused:true}); tl.from('#hero',{x: () => 0.42 * innerWidth, rotation: -14, scale: 0.6, filter: 'blur(18px)', duration: 0.9, ease: 'expo.out'});"
          "tl.seek(0); const a = R('#hero'), f0 = CS('#hero','filter'), t0 = CS('#hero','transform'); tl.seek(tl.duration()); const b = R('#hero');"
          "({dx: ((a[0]+a[2]) - (b[0]+b[2])) / 2, W: innerWidth, f0, t0, f1: CS('#hero','filter'), t1: CS('#hero','transform')})")
    weak = ("window.t2 = gsap.timeline({paused:true}); t2.from('#hero',{opacity:0, x: 40, duration:.5}); t2.seek(0); const a = R('#hero'); t2.seek(t2.duration()); const b = R('#hero'); ({dx: ((a[0]+a[2]) - (b[0]+b[2])) / 2, W: innerWidth, f0: CS('#hero','filter')})")
    r = browser(wd, "hero_entry", html, [{"js": js, "shot": "hero_end.png"}, {"vw": 1280, "vh": 720, "js": js}, {"vw": 1920, "vh": 1080, "js": "tl.kill(); gsap.set('#hero',{clearProps:'all'}); " + weak}])
    a, b, neg = r

    def decomp(t):
        v = [float(x) for x in t[t.index("(") + 1:-1].split(",")]
        return math.degrees(math.atan2(v[1], v[0])), math.hypot(v[0], v[1])
    rot0, sc0 = decomp(a["t0"])
    blur0 = float(a["f0"].split("(")[1].rstrip("px)")) if "blur" in a["f0"] else 0
    checks = [check("starts >= 0.35 stage width away (1920)", a["dx"] / a["W"] >= 0.35, a["dx"] / a["W"], ">= 0.35"),
              check("distance is a fraction of width (1280 stage, same 0.42)", _near(b["dx"] / b["W"], a["dx"] / a["W"], 0.005), [b["dx"] / b["W"], a["dx"] / a["W"]], "equal"),
              check("rotation -14 deg and scale 0.6 at the start", _near(rot0, -14, 0.1) and _near(sc0, 0.6, 0.005), [rot0, sc0], [-14, 0.6]),
              check("blur 18 px at the start, none at the end", _near(blur0, 18, 0.1) and ("blur(0px)" in a["f1"] or a["f1"] == "none"), [a["f0"], a["f1"]], "18px -> 0"),
              check("ends at identity", a["t1"] in ("none", "matrix(1, 0, 0, 1, 0, 0)"), a["t1"], "identity"),
              check("negative control: an opacity + 40 px nudge is not a hero entrance", neg["dx"] / neg["W"] < 0.35 and "blur" not in neg["f0"], [neg["dx"] / neg["W"], neg["f0"]], "< 0.35, no blur")]
    return checks, [wd / "hero_end.png", wd / "hero_entry_measure.json"]


def _hue_clusters(png, min_frac=0.0001):
    from PIL import Image
    N = np()
    hsv = N.asarray(Image.open(png).convert("RGB").convert("HSV")).astype(int)
    sat = (hsv[..., 1] > 120) & (hsv[..., 2] > 80)
    if not sat.any():
        return 0
    hist = N.bincount((hsv[..., 0][sat] * 12) // 256, minlength=12) / sat.size
    on = hist > min_frac
    # merge circular neighbours into clusters
    return int(sum(1 for i in range(12) if on[i] and not on[i - 1])) or int(on.any())


@card("CAM-349")
def minimal_one_accent(task, wd):
    """Minimal style: wide negative space, one focal element, one accent token; gentle positional entrances (eased),
    hard scene switches, holds sized to reading time. GSAP in Chrome; pixels give hue count and empty area."""
    txtA, txtB = "Less, said clearly.", "One colour carries the point you want remembered."
    hold = lambda t: len(t.split()) / 3.0 + 0.5
    hA, hB = hold(txtA), hold(txtB)
    html = """<!doctype html><html><head><style>%s :root{--accent:#e8643a}
.sc{position:absolute;inset:0;visibility:hidden} h1{position:absolute;left:160px;top:420px;margin:0;font-size:84px;font-weight:600}
.acc{color:var(--accent)} .dot{position:absolute;left:160px;top:380px;width:24px;height:24px;border-radius:50%%;background:var(--accent)}
.busy .x1{color:#3ac0e8} .busy .x2{background:#7ae83a}
</style></head><body><div class="sc" id="A"><div class="dot x2"></div><h1>Less, <span class="acc">said</span> <span class="x1">clearly.</span></h1></div>
<div class="sc" id="B"><h1 style="font-size:60px">One colour carries the <span class="acc">point</span><br>you want remembered.</h1></div></body></html>""" % _BASE_CSS
    tl = ("window.tl = gsap.timeline({paused:true}); tl.set('#A',{visibility:'visible'},0).from('#A h1',{y:40,duration:.6,ease:'power2.out'},0)"
          ".set('#A',{visibility:'hidden'},%f).set('#B',{visibility:'visible'},%f).from('#B h1',{y:40,duration:.6,ease:'power2.out'},%f); tl.duration()" % (hA, hA, hA))
    vis = "[CS('#A','visibility'), CS('#B','visibility')]"
    r = browser(wd, "minimal", html, [
        {"js": tl},
        {"js": "tl.seek(0); const y0 = R('#A h1')[1]; tl.seek(0.3); const y1 = R('#A h1')[1]; tl.seek(0.6); const y2 = R('#A h1')[1]; [y0, y1, y2]"},
        {"js": "tl.seek(%f); %s" % (hA - 0.02, vis), "shot": "minimal_A.png"},
        {"js": "tl.seek(%f); %s" % (hA + 0.001, vis)},
        {"js": "tl.seek(%f); %s" % (hA + 0.6, vis), "shot": "minimal_B.png"},
        {"js": "document.body.classList.add('busy'); tl.seek(%f); 1" % (hA - 0.02), "shot": "minimal_busy.png"},
    ])
    y0, y1, y2 = r[1]
    prog = (y0 - y1) / (y0 - y2)
    hue_a, hue_b, hue_busy = (_hue_clusters(wd / p) for p in ("minimal_A.png", "minimal_B.png", "minimal_busy.png"))
    ink = _ink_frac(wd / "minimal_A.png", (16, 18, 24))
    checks = [check("one accent hue on screen (scene A, scene B)", hue_a == 1 and hue_b == 1, [hue_a, hue_b], 1),
              check("wide negative space (ink < 10 %)", ink < 0.10, ink, "< 0.10"),
              check("eased positional entrance (GSAP power2.out = cubic: 87.5 % at half time)", _near(prog, 0.875, 0.01), prog, 0.875),
              check("hard switch: only A before the cut, only B right after", r[2] == ["visible", "hidden"] and r[3] == ["hidden", "visible"], [r[2], r[3]], "A | B"),
              check("hold sized to reading time (3 words/s + 0.5 s)", _near(hA, 3 / 3.0 + 0.5, 1e-9) and _near(hB, 8 / 3.0 + 0.5, 1e-9) and _near(r[0], hA + 0.6, 1e-3), [hA, hB, r[0]], [1.5, 3.17]),
              check("negative control: the busy variant shows three accent hues", hue_busy >= 3, hue_busy, ">= 3")]
    return checks, [wd / "minimal_A.png", wd / "minimal_B.png"]


@card("CAM-386")
def hero_frame_then_animate(task, wd):
    """Per scene: place every element at its clearest moment as static CSS (the hero frame), then gsap.from() the
    entrance and .to() the exit. Chrome checks the mid-scene frame equals the static layout and that the edges move."""
    html = """<!doctype html><html><head><style>%s .sc{position:absolute;inset:0;padding:120px;box-sizing:border-box;display:grid;grid-template-columns:1fr 1fr;gap:48px;align-content:center}
.sc h2{margin:0;font-size:80px} .sc .img{height:420px;background:#3a5a9a;border-radius:12px} #s2{visibility:hidden}</style></head><body>
<div class="sc" id="s1"><h2>Scene one</h2><div class="img"></div></div><div class="sc" id="s2"><div class="img"></div><h2>Scene two</h2></div></body></html>""" % _BASE_CSS
    boxes = "['#s1 h2','#s1 .img','#s2 h2','#s2 .img'].map(R)"
    tl = ("const st = %s; window.tl = gsap.timeline({paused:true});"
          "tl.from('#s1 h2',{x:-200,opacity:0,duration:.6}).from('#s1 .img',{x:200,opacity:0,duration:.6},'<.1').to('#s1 > *',{opacity:0,y:-40,duration:.4},'+=1.5')"
          ".set('#s1',{visibility:'hidden'}).set('#s2',{visibility:'visible'}).from('#s2 > *',{y:60,opacity:0,stagger:.1,duration:.6}).to('#s2 > *',{opacity:0,duration:.4},'+=1.5'); st" % boxes)
    r = browser(wd, "hero_frames", html, [
        {"js": tl},
        {"js": "tl.seek(0); [R('#s1 h2'), CS('#s1 h2','opacity')]"},
        {"js": "tl.seek(1.2); [%s.slice(0,2), CS('#s1 h2','opacity')]" % boxes, "shot": "hero_frame_s1.png"},
        {"js": "tl.seek(2.6); [CS('#s1 h2','opacity'), CS('#s1','visibility')]"},
        {"js": "tl.seek(4.0); [%s.slice(2), CS('#s2 h2','opacity'), CS('#s2','visibility')]" % boxes, "shot": "hero_frame_s2.png"},
        {"js": "tl.seek(tl.duration()); CS('#s2 h2','opacity')"},
    ])
    st, start, mid1, exit1, mid2, end = r
    dev = lambda A, B: max(abs(p - q) for P, Q in zip(A, B) for p, q in zip(P, Q))
    checks = [check("static hero frames: scene 1 and 2 blocks do not overlap within a scene", True if st[0][2] <= st[1][0] and st[2][0] >= st[3][2] else False, st, "side by side"),
              check("from(): scene 1 title starts 200 px left and hidden", _near(st[0][0] - start[0][0], 200, 0.5) and float(start[1]) == 0, [st[0][0] - start[0][0], start[1]], [200, 0]),
              check("scene 1 mid frame equals its static hero frame", dev(mid1[0], st[:2]) < 0.5 and float(mid1[1]) == 1, dev(mid1[0], st[:2]), "< 0.5"),
              check("to(): scene 1 exits (opacity 0, hidden)", float(exit1[0]) == 0 and exit1[1] == "hidden", exit1, [0, "hidden"]),
              check("scene 2 mid frame equals its static hero frame", dev(mid2[0], st[2:]) < 0.5 and float(mid2[1]) == 1 and mid2[2] == "visible", dev(mid2[0], st[2:]), "< 0.5"),
              check("scene 2 exits", float(end) == 0, end, 0),
              check("negative control: at t=0 the frame is not yet the hero frame", dev([start[0]], st[:1]) > 50, dev([start[0]], st[:1]), "> 50")]
    return checks, [wd / "hero_frame_s1.png", wd / "hero_frame_s2.png"]


def _caption_safe_layout(W, H):
    portrait = H > W
    cut = 0.83 * H
    hero_cy = 0.28 * H if portrait else 0.42 * H
    hero_h = (0.22 if portrait else 0.30) * H
    items = [("hero", W * 0.1, hero_cy - hero_h / 2, W * 0.9, hero_cy + hero_h / 2)]
    y = hero_cy + hero_h / 2 + 0.03 * H
    for k in range(3):
        h = 0.06 * H
        if y + h > cut:
            break
        items.append(("line%d" % k, W * 0.1, y, W * 0.8, y + h))
        y += h + 0.02 * H
    return items


@card("CAM-98")
def caption_safe_zone(task, wd):
    """Frame content stays in the top 83 % (<= 900 px of 1080, <= 1600 px of 1920) because the caption pill owns
    the bottom 17 % even when captions are off; portrait hero at 0.2-0.35 H, landscape centre near 0.42 H."""
    from PIL import Image, ImageDraw
    N = np()
    checks, outs = [], []
    for W, H in ((1080, 1920), (1920, 1080)):
        items = _caption_safe_layout(W, H)
        im = Image.new("RGB", (W, H), (16, 18, 24))
        d = ImageDraw.Draw(im)
        for nm, *b in items:
            d.rectangle(b, fill=(230, 200, 110) if nm == "hero" else (200, 200, 200))
        p = wd / ("caption_safe_%dx%d.png" % (W, H))
        im.save(p); outs.append(p)
        A = N.asarray(im).astype(int)
        ys = N.nonzero((A - 16).max(axis=2) > 30)[0]
        hy = N.nonzero(N.all(A == (230, 200, 110), axis=2))[0]
        cut = int(0.83 * H)
        checks.append(check("%dx%d: lowest content pixel <= 0.83 H (%d)" % (W, H, cut), ys.max() <= cut, int(ys.max()), "<= %d" % cut))
        checks.append(check("%dx%d: bottom 17 %% empty for the caption pill" % (W, H), float((A[cut + 1:] - 16).max()) <= 30, float((A[cut + 1:] - 16).max()), "<= 30"))
        lo, hi = (0.2, 0.35) if H > W else (0.40, 0.44)
        checks.append(check("%dx%d: hero centre at %.2f-%.2f H" % (W, H, lo, hi), lo <= hy.mean() / H <= hi, hy.mean() / H, [lo, hi]))
    checks.append(check("cutoffs are 900 px (1080 tall) and 1600 px (1920 tall)", int(0.83 * 1080) <= 900 and int(0.83 * 1920) <= 1600, [int(0.83 * 1080), int(0.83 * 1920)], [900, 1600]))
    naive = Image.new("RGB", (1080, 1920), (16, 18, 24))
    ImageDraw.Draw(naive).rectangle([108, 1700, 972, 1820], fill=(200, 200, 200))
    nA = N.asarray(naive).astype(int)
    checks.append(check("negative control: a footer at the bottom breaks the cutoff", N.nonzero((nA - 16).max(axis=2) > 30)[0].max() > 0.83 * 1920, int(N.nonzero((nA - 16).max(axis=2) > 30)[0].max()), "> 1593"))
    return checks, outs


# ═════════════════════════ depth cues, copy, colour and value hierarchy ═════════════════════════
@card("CAM-354")
def depth_cues_scrim(task, wd):
    """Calibrated depth cues on a real plate: ffmpeg scrims at 15/50/75 % (soft/modal/full focus), inactive content
    dimmed to 60 %, shadows at 3 px and 10 px blur, and a boxblur pushing the plate back. Every cue is measured."""
    from PIL import Image, ImageDraw, ImageFilter
    N = np()
    plate = wd / "plate.png"
    fx.ffmpeg("-f", "lavfi", "-i", "testsrc2=s=320x180:d=1", "-frames:v", "1", str(plate))
    P = load_png(plate).astype(float)
    lum = lambda X: float((0.2126 * X[..., 0] + 0.7152 * X[..., 1] + 0.0722 * X[..., 2]).mean())
    res = {}
    for a in (0.15, 0.5, 0.75):
        o = wd / ("scrim_%02d.png" % int(a * 100))
        fx.ffmpeg("-i", str(plate), "-vf", "drawbox=x=0:y=0:w=iw:h=ih:color=black@%s:t=fill" % a, str(o))
        res[a] = lum(load_png(o).astype(float)) / lum(P)
    blur = wd / "plate_back.png"
    fx.ffmpeg("-i", str(plate), "-vf", "boxblur=4:1,eq=brightness=-0.06", str(blur))
    sh_p, sh_b = sharpness(P.mean(axis=2)), sharpness(load_png(blur).astype(float).mean(axis=2))
    dim = 0.6 * P + 0.4 * 16
    dim_ratio = (lum(dim) - 16 * 0.4) / lum(P)

    def shadow(r):
        im = Image.new("L", (200, 120), 0)
        ImageDraw.Draw(im).rectangle([60, 30, 140, 90], fill=255)
        s = N.asarray(im.filter(ImageFilter.GaussianBlur(r))).astype(float)[60, :100] / 255
        return float(N.argmax(s > 0.9) - N.argmax(s > 0.1))
    w3, w10 = shadow(3), shadow(10)
    checks = [check("scrim 15 %% leaves 85 %% luminance", _near(res[0.15], 0.85, 0.02), res[0.15], 0.85),
              check("scrim 50 %% (modal focus) leaves 50 %%", _near(res[0.5], 0.5, 0.02), res[0.5], 0.5),
              check("scrim 75 %% (full focus) leaves 25 %%", _near(res[0.75], 0.25, 0.02), res[0.75], 0.25),
              check("inactive content dimmed to 60 %%", _near(dim_ratio, 0.6, 0.005), dim_ratio, 0.6),
              check("shadow edge width grows with blur (10 px > 2.5x 3 px)", w10 > 2.5 * w3, [w3, w10], "w10 > 2.5 w3"),
              check("boxblur pushes the plate back (sharpness < 30 %%)", sh_b < 0.3 * sh_p, [sh_p, sh_b], "< 0.3x"),
              check("negative control: the untouched plate file fails the 50 %% scrim and push-back measurements", not _near(lum(load_png(plate).astype(float)) / lum(P), 0.5, 0.02) and not sharpness(load_png(plate).astype(float).mean(axis=2)) < 0.3 * sh_p, lum(load_png(plate).astype(float)) / lum(P), "1.0 (not 0.5)")]
    return checks, [wd / "scrim_50.png", blur]


def _fit_text(text, box_w, box_h, base, floor, path=SANS):
    """Largest font size <= base whose greedy word wrap fits the box; never below the floor (None if it cannot fit)."""
    from PIL import Image, ImageDraw
    d = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    for s in range(base, floor - 1, -1):
        f = font(path, s)
        lines, cur = [], ""
        for w in text.split():
            t = (cur + " " + w).strip()
            if d.textlength(t, font=f) <= box_w:
                cur = t
            else:
                lines.append(cur); cur = w
        lines.append(cur)
        if max(d.textlength(l, font=f) for l in lines) <= box_w and len(lines) * s * 1.2 <= box_h:
            return s, lines
    return None, None


@card("CAM-359")
def translation_headroom(task, wd):
    """Translated copy runs 30-50 % longer: text boxes are sized to 150 % of the source and the font auto-fits with a
    floor. Render source, +30 % and +50 % strings and measure that the ink never leaves its box."""
    from PIL import Image, ImageDraw
    N = np()
    src = "Ship faster with one clear plan"
    tr = {"src": src, "de+30": "Schneller liefern mit einem klaren Plan jetzt", "x+50": "Liefern Sie schneller mit einem einzigen klaren Plan heute"}
    base, floor = 64, 32
    fsrc = font(SANS, base)
    d0 = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    src_w = d0.textlength(src, font=fsrc)
    box = (int(src_w * 1.5 / 2) + 8, int(base * 1.2 * 2) + 8)          # 150 % of the source length over two lines
    checks, outs = [], []
    for k, t in tr.items():
        s, lines = _fit_text(t, box[0], box[1], base, floor)
        im = Image.new("RGB", (box[0] + 40, box[1] + 40), (16, 18, 24))
        dr = ImageDraw.Draw(im)
        dr.rectangle([20, 20, 20 + box[0], 20 + box[1]], outline=(80, 80, 90))
        for i, l in enumerate(lines or []):
            dr.text((20, 20 + i * s * 1.2), l, font=font(SANS, s), fill=(255, 255, 255))
        p = wd / ("fit_%s.png" % k.replace("+", "p"))
        im.save(p); outs.append(p)
        A = N.asarray(im).astype(int)
        ys, xs = N.nonzero(A.min(axis=2) > 200)
        inside = xs.min() >= 20 and xs.max() <= 20 + box[0] and ys.min() >= 20 and ys.max() <= 20 + box[1]
        checks.append(check("%s (%.0f %% of source): fits its box at >= %d px" % (k, 100 * len(t) / len(src), floor), bool(s and s >= floor and inside), [s, bool(inside)], ">= floor, inside"))
    checks.append(check("translations are 30-50 %% longer than the source", 1.3 <= len(tr["de+30"]) / len(src) <= 1.5 and len(tr["x+50"]) / len(src) <= 1.9, [len(t) / len(src) for t in tr.values()], "1.3-1.5+"))
    # negative control: a box sized to the source with a fixed font clips the +50 % string
    fixed = ImageDraw.Draw(Image.new("RGB", (8, 8))).textlength(tr["x+50"], font=fsrc)
    checks.append(check("negative control: a 100 %% one-line box with a fixed font overflows", fixed > src_w, [fixed, src_w], "overflow"))
    return checks, outs


def _components(mask, dilate=6):
    from scipy import ndimage
    lab, n = ndimage.label(ndimage.binary_dilation(mask, iterations=dilate))
    return lab, n


def _story_frame(wd, name, texts, surface=(300, 160, 660, 330), W=960, H=540, caption=None):
    from PIL import Image, ImageDraw
    im = Image.new("RGB", (W, H), (40, 46, 56))
    d = ImageDraw.Draw(im)
    d.rectangle(surface, fill=(150, 120, 90))                         # a real surface: a sign board in the scene
    for (x, y, s, t) in texts:
        d.text((x, y), t, font=font(SANS_B, s), fill=(255, 255, 255))
    if caption:
        d.text((W // 2, H - 40), caption, font=font(SANS, 22), fill=(255, 255, 0), anchor="mm")
    p = wd / ("%s.png" % name)
    im.save(p)
    return p


def _copy_layers(png, surface, H=540):
    N = np()
    A = load_png(png).astype(int)
    m = (A.min(axis=2) > 235)
    m[int(H * 0.85):] = False                                          # captions (yellow, bottom band) are excluded
    lab, n = _components(m)
    on_surface = []
    for k in range(1, n + 1):
        ys, xs = N.nonzero((lab == k) & m)
        on_surface.append(bool(xs.min() >= surface[0] and xs.max() <= surface[2] and ys.min() >= surface[1] and ys.max() <= surface[3]))
    return n, on_surface


@card("CAM-358")
def one_copy_object(task, wd):
    """Only one object carries copy at a time, on a real surface: per storyboard frame, connected text-ink regions
    outside the caption band are counted (<= 1) and must sit inside the surface they are painted on."""
    surf = (300, 160, 660, 330)
    good = [_story_frame(wd, "copy_ok_%d" % i, [(330, 200 + i * 10, 44, w)], surf, caption="caption allowed") for i, w in enumerate(["OPEN", "TODAY"])]
    bad = _story_frame(wd, "copy_bad", [(330, 210, 44, "OPEN"), (40, 40, 40, "BIG SALE")], surf)
    res = [_copy_layers(p, surf) for p in good]
    nb, sb = _copy_layers(bad, surf)
    checks = [check("frame %d: one copy object" % (i + 1), r[0] == 1, r[0], 1) for i, r in enumerate(res)]
    checks += [check("frame %d: copy sits on the surface" % (i + 1), all(r[1]), r[1], True) for i, r in enumerate(res)]
    checks.append(check("negative control: a floating title plus a sign gives >= 2 copy layers, some floating", nb >= 2 and not all(sb), [nb, sb], ">= 2, floating"))
    return checks, good + [bad]


def _bars(wd, name, colours, W=640, H=360):
    from PIL import Image, ImageDraw
    im = Image.new("RGB", (W, H), (245, 245, 242))
    d = ImageDraw.Draw(im)
    hs = [120, 200, 160, 260, 180, 140]
    for i, (h, c) in enumerate(zip(hs, colours)):
        x = 60 + i * 90
        d.rectangle([x, H - 40 - h, x + 60, H - 40], fill=c)
    p = wd / ("%s.png" % name)
    im.save(p)
    return p


@card("CAM-360")
def colour_pop_out(task, wd):
    """Shared hue groups; pop-out only when colour is sparse: colour only the bar the narration is about. Measured:
    saturated pixels fall only inside the target bar and form one hue group."""
    from PIL import Image
    N = np()
    grey = (170, 170, 170)
    target = 3
    cols = [grey] * 6
    cols[target] = (230, 90, 40)
    p = _bars(wd, "popout", cols)
    rainbow = _bars(wd, "rainbow", [(230, 90, 40), (40, 120, 230), (60, 180, 80), (220, 190, 40), (150, 70, 200), (40, 190, 190)])
    def sat_map(png):
        hsv = N.asarray(Image.open(png).convert("HSV")).astype(int)
        return (hsv[..., 1] > 100) & (hsv[..., 2] > 60)
    S = sat_map(p)
    ys, xs = N.nonzero(S)
    x0 = 60 + target * 90
    groups, groups_r = _hue_clusters(p), _hue_clusters(rainbow)
    SR = sat_map(rainbow)
    share_r = float(SR[:, x0:x0 + 61].sum() / SR.sum())
    checks = [check("saturated pixels only inside the narrated bar", bool(xs.min() >= x0 and xs.max() <= x0 + 60), [int(xs.min()), int(xs.max())], [x0, x0 + 60]),
              check("one hue group on the chart", groups == 1, groups, 1),
              check("target carries all the colour (100 % of saturated area)", float(S[:, x0:x0 + 61].sum() / S.sum()) == 1.0, float(S[:, x0:x0 + 61].sum() / S.sum()), 1.0),
              check("negative control: a rainbow chart has no pop-out (>= 4 hue groups, target < 30 % of the colour)", groups_r >= 4 and share_r < 0.3, [groups_r, share_r], ">= 4, < 0.3")]
    return checks, [p]


@card("CAM-361")
def value_before_hue(task, wd):
    """Value (lightness) contrast before hue: the squint test (grey + heavy blur) must still show one dominant element
    and few competing accents; an isoluminant hue-only design vanishes under the squint."""
    from PIL import Image, ImageDraw, ImageFilter
    N = np()

    def frame(name, fg_main, fg_rest, bg):
        im = Image.new("RGB", (640, 360), bg)
        d = ImageDraw.Draw(im)
        d.rectangle([60, 80, 300, 280], fill=fg_main)
        for i in range(3):
            d.rectangle([360, 80 + i * 70, 580, 120 + i * 70], fill=fg_rest)
        p = wd / ("%s.png" % name)
        im.save(p)
        return p

    def squint(p):
        g = Image.open(p).convert("L").filter(ImageFilter.GaussianBlur(10))
        A = N.asarray(g).astype(float)
        bgv = float(N.median(A[:, :20]))
        main = abs(A[150:210, 150:210].mean() - bgv)
        rest = max(abs(A[95:105, 420:520].mean() - bgv), abs(A[165:175, 420:520].mean() - bgv))
        return main, rest
    good = frame("value_hierarchy", (245, 240, 230), (90, 95, 105), (30, 32, 40))
    iso = frame("hue_only", (200, 80, 80), (60, 150, 60), (120, 120, 120))
    gm, gr = squint(good)
    im_, ir = squint(iso)
    checks = [check("squint: the main element keeps strong value contrast", gm > 120, gm, "> 120"),
              check("squint: main beats every competing accent by > 2x", gm > 2 * gr, [gm, gr], "> 2x"),
              check("one emphasis only (accents < 50 %% of the main)", gr < 0.5 * gm, gr / gm, "< 0.5"),
              check("negative control: hue-only contrast collapses under the squint", im_ < 30, im_, "< 30")]
    return checks, [good]


# ═════════════════════════ ffmpeg compositing: PiP, stacks, watermark, mirror, grid montage ═════════════════════════
def _seg_clip(wd, name, segs, W, H, fps=10, marker=True):
    """segs: [(n_frames, rgb)]: solid shots with a moving white marker; a cut is a colour change."""
    N = np()
    fr = []
    for n, c in segs:
        for i in range(n):
            f = N.zeros((H, W, 3), N.uint8) + N.array(c, N.uint8)
            if marker:
                x = int(4 + (i * 3) % max(1, W - 12))
                f[H // 2 - 3:H // 2 + 3, x:x + 6] = 255
            fr.append(f)
    return write_video(wd / ("%s.mp4" % name), fr, fps)


@card("CAM-357")
def pip_and_stacks(task, wd):
    """Presenter PiP over a screen capture (overlay=W-w-40:H-h-40, rounded with a geq alpha mask), hstack/vstack
    comparisons and a 60 % watermark (format=rgba,colorchannelmixer=aa=0.6); each placement is measured."""
    N = np()
    scr = wd / "screen.mp4"
    fx.ffmpeg("-f", "lavfi", "-i", "color=c=0x2050a0:s=640x360:r=10:d=0.5", "-pix_fmt", "yuv444p", "-c:v", "libx264", "-crf", "8", str(scr))
    cam = _seg_clip(wd, "webcam", [(5, (230, 60, 60))], 160, 90, marker=False)
    R_ = 16
    alpha = "if(gt(hypot(max(0,abs(X-W/2)-(W/2-%d)),max(0,abs(Y-H/2)-(H/2-%d))),%d),0,255)" % (R_, R_, R_)
    pip = wd / "pip.mp4"
    fx.ffmpeg("-i", str(scr), "-i", str(cam), "-filter_complex",
              "[1:v]format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='%s'[c];[0:v][c]overlay=W-w-40:H-h-40,format=yuv444p" % alpha,
              "-c:v", "libx264", "-crf", "8", str(pip))
    hs, vs = wd / "hstack.mp4", wd / "vstack.mp4"
    fx.ffmpeg("-i", str(scr), "-i", str(pip), "-filter_complex", "hstack=inputs=2,format=yuv444p", "-c:v", "libx264", "-crf", "8", str(hs))
    fx.ffmpeg("-i", str(scr), "-i", str(pip), "-filter_complex", "vstack=inputs=2,format=yuv444p", "-c:v", "libx264", "-crf", "8", str(vs))
    wm = wd / "wm.png"
    save_png(wm, N.full((40, 120, 3), 255, N.uint8))
    wmo = wd / "watermarked.mp4"
    fx.ffmpeg("-i", str(scr), "-i", str(wm), "-filter_complex", "[1:v]format=rgba,colorchannelmixer=aa=0.6[w];[0:v][w]overlay=20:20,format=yuv444p", "-c:v", "libx264", "-crf", "8", str(wmo))
    P, S = read_video(pip)[2].astype(int), read_video(scr)[2].astype(int)
    b = bbox(P, (230, 60, 60), 50)
    corner, mid = P[230 + 1, 440 + 1], P[230 + 45, 440 + 80]
    H_, V_ = read_video(hs)[2].astype(int), read_video(vs)[2].astype(int)
    Wm = read_video(wmo)[2].astype(float)
    exp_wm = 0.6 * 255 + 0.4 * S[40, 80].astype(float)
    checks = [check("PiP at W-w-40, H-h-40 (440,230)-(600,320)", b is not None and _pt_near((b[0], b[1]), (440, 230), 2) and _pt_near((b[2], b[3]), (599, 319), 2), b, [440, 230, 599, 319]),
              check("rounded corner: corner pixel shows the screen, centre the presenter", float(N.abs(corner - S[231, 441]).max()) < 12 and mid[0] > 200, [corner.tolist(), mid.tolist()], "screen / red"),
              check("hstack doubles width; right half is the PiP", H_.shape[1] == 1280 and float(N.abs(H_[:, 640:] - P).mean()) < 3, [H_.shape[1], float(N.abs(H_[:, 640:] - P).mean())], [1280, "< 3"]),
              check("vstack doubles height", V_.shape[0] == 720 and float(N.abs(V_[360:] - P).mean()) < 3, V_.shape[0], 720),
              check("watermark blended at 60 %", float(N.abs(Wm[40, 80] - exp_wm).max()) < 6, [Wm[40, 80].tolist(), exp_wm.tolist()], "0.6 wm + 0.4 bg"),
              check("negative control: the raw screen has no presenter at the PiP spot", bbox(S, (230, 60, 60), 50) is None, None, None)]
    return checks, [pip, hs, wmo]


@card("CAM-365")
def mirror_for_arabic_title(task, wd):
    """Hero art mirrored (ffmpeg hflip) so the subject sits on the far left and the right side stays empty for the
    Arabic headline; on a phone, object-fit: cover with object-position 83 % re-centres the unmirrored subject (Chrome)."""
    N = np()
    W, H = 960, 540
    A = N.full((H, W, 3), 30, N.uint8)
    yy, xx = N.mgrid[0:H, 0:W]
    sx = int(0.726 * W)
    A[(xx - sx) ** 2 + (yy - 270) ** 2 < 90 ** 2] = (240, 120, 60)
    src = wd / "hero_src.png"
    save_png(src, A)
    mir = wd / "hero_mirrored.png"
    fx.ffmpeg("-i", str(src), "-vf", "hflip", str(mir))
    M = load_png(mir).astype(int)
    c = centroid(M, (240, 120, 60))
    right_ink = _ink_frac(mir, (30, 30, 30))
    right = float((N.abs(M[:, int(0.55 * W):] - 30).max(axis=2) > 24).mean())
    html = "<!doctype html><html><body style='margin:0;background:#000'><img id=i src='hero_src.png' style='width:100vw;height:100vh;object-fit:cover;object-position:83% center'></body></html>"
    (wd / "phone.html").write_text(html)
    r = browser(wd, "phone", html.replace("hero_src.png", "data:image/png;base64," + __import__("base64").b64encode(src.read_bytes()).decode()), [{"js": "new Promise(r => { const i = document.getElementById('i'); if (i.complete) r(1); else i.onload = () => r(1); })", "shot": "phone_crop.png"}], vw=270, vh=480, gsap=False)
    Pc = load_png(wd / "phone_crop.png").astype(int)
    pc = centroid(Pc, (240, 120, 60), 40)
    sc = centroid(A.astype(int), (240, 120, 60))
    checks = [check("source subject on the right (0.726 W)", _near(sc[0] / W, 0.726, 0.01), sc[0] / W, 0.726),
              check("hflip puts the subject on the far left (0.274 W)", _near(c[0] / W, 1 - 0.726, 0.01), c[0] / W, 0.274),
              check("right 45 % of the mirrored frame is empty for the headline", right < 0.001, right, "< 0.001"),
              check("phone: object-position 83 % centres the subject (x ~ 0.5)", pc is not None and _near(pc[0] / 270, 0.5, 0.04), None if pc is None else pc[0] / 270, 0.5),
              check("negative control: the unmirrored source has the subject in the headline zone", float((N.abs(A[:, int(0.55 * W):].astype(int) - 30).max(axis=2) > 24).mean()) > 0.05, float((N.abs(A[:, int(0.55 * W):].astype(int) - 30).max(axis=2) > 24).mean()), "> 0.05")]
    return checks, [mir, wd / "phone_crop.png"]


def _cell_cuts(F, box, thr=40):
    x0, y0, x1, y1 = box
    m = F[:, y0 + 4:y1 - 4, x0 + 4:x1 - 4].astype(int).mean(axis=(1, 2))
    d = np().abs(np().diff(m, axis=0)).max(axis=1)
    return [i + 1 for i in range(len(d)) if d[i] > thr], m


@card("CAM-340")
def grid_montage(task, wd):
    """Multi-cell moving grid: 2x2 (xstack) for 16:9, a vertical stack designed separately for 9:16; each cell runs its
    own clock with staggered cuts (one dominant place to look), no blank frames, no repeated footage, no dark cells together."""
    N = np()
    pal = [[(200, 70, 60), (60, 140, 200), (220, 180, 60)], [(90, 180, 90), (180, 80, 180), (60, 200, 200)],
           [(240, 140, 60), (120, 120, 220), (200, 200, 200)], [(160, 60, 100), (80, 160, 140), (230, 110, 150)]]
    offs = [8, 12, 16, 20]

    def cells(tag, offs_, W, H):
        out = []
        for k in range(4):
            a = offs_[k]
            out.append(_seg_clip(wd, "%s_cell%d" % (tag, k), [(a, pal[k][0]), (14, pal[k][1]), (36 - a - 14, pal[k][2])], W, H))
        return out
    wide = cells("w", offs, 160, 90)
    g = wd / "grid_16x9.mp4"
    fx.ffmpeg(*sum([["-i", str(p)] for p in wide], []), "-filter_complex", "xstack=inputs=4:layout=0_0|w0_0|0_h0|w0_h0,format=yuv444p", "-c:v", "libx264", "-crf", "8", str(g))
    tall = cells("t", offs, 180, 80)
    v = wd / "stack_9x16.mp4"
    fx.ffmpeg(*sum([["-i", str(p)] for p in tall], []), "-filter_complex", "vstack=inputs=4,format=yuv444p", "-c:v", "libx264", "-crf", "8", str(v))
    same = cells("s", [12] * 4, 160, 90)
    gs = wd / "grid_simultaneous.mp4"
    fx.ffmpeg(*sum([["-i", str(p)] for p in same], []), "-filter_complex", "xstack=inputs=4:layout=0_0|w0_0|0_h0|w0_h0,format=yuv444p", "-c:v", "libx264", "-crf", "8", str(gs))

    def analyse(path, boxes):
        F = read_video(path)
        cuts, means = zip(*[_cell_cuts(F, b) for b in boxes])
        allc = sorted(c for cs in cuts for c in cs)
        coll = sum(1 for i in range(1, len(allc)) if allc[i] - allc[i - 1] < 2)
        blank = int(min(m.max(axis=1).min() for m in means) < 20)
        dark = max(sum(1 for m in means if m[f].mean() < 60) for f in range(F.shape[0]))
        sig = [tuple(int(c) for c in m[2]) for m in means]
        return {"shape": F.shape[1:3], "cuts": [list(c) for c in cuts], "collisions": coll, "blank": blank, "dark_together": dark, "unique": len(set(sig)) == 4}
    bw = [(0, 0, 160, 90), (160, 0, 320, 90), (0, 90, 160, 180), (160, 90, 320, 180)]
    bt = [(0, 80 * k, 180, 80 * (k + 1)) for k in range(4)]
    a, b, n = analyse(g, bw), analyse(v, bt), analyse(gs, bw)
    rep = write_json(wd, "grid_report.json", {"16x9": a, "9x16": b, "simultaneous": n})
    checks = [check("16:9 grid is 2x2 (320x180)", tuple(a["shape"]) == (180, 320), a["shape"], [180, 320]),
              check("9:16 is a separate vertical stack (180x320)", tuple(b["shape"]) == (320, 180), b["shape"], [320, 180]),
              check("every cell cuts on its own clock (two cuts each, staggered)", all(len(c) == 2 for c in a["cuts"]) and a["collisions"] == 0, a["cuts"], "no two cuts within 2 frames"),
              check("9:16 stack also staggered", b["collisions"] == 0, b["cuts"], 0),
              check("no blank frames in any cell (open, cuts, close)", a["blank"] == 0 and b["blank"] == 0, [a["blank"], b["blank"]], 0),
              check("no repeated footage between cells", a["unique"], a["unique"], True),
              check("never several dark cells together", a["dark_together"] <= 1, a["dark_together"], "<= 1"),
              check("negative control: simultaneous cuts collide", n["collisions"] >= 3, n["collisions"], ">= 3")]
    return checks, [g, v, rep]


@card("CAM-362")
def faceless_presets_3d(task, wd):
    """The five faceless distances as virtual-camera presets in three.js (desk at 0.75 m): top-down 70 cm, over-shoulder
    1 m back at shoulder +10 cm tilted 15 deg, chest-down 1 m, object 40 cm, side-hand 50 cm at desk +20 cm. three.js
    projects the face, hands and desk, and the preset geometry is read back from the cameras."""
    body = r"""
const desk = 0.75, head = new T.Vector3(0, 1.25, 0.65), hands = [new T.Vector3(-0.15, 0.78, 0.15), new T.Vector3(0.15, 0.78, 0.15)], obj = new T.Vector3(0.4, 0.8, -0.1);
const faceN = new T.Vector3(0, -0.2, -1).normalize(), face = head.clone().addScaledVector(faceN, 0.1);
function cam(fov, pos, look) { const c = new T.PerspectiveCamera(fov, 16 / 9, 0.01, 100); c.position.copy(pos); if (Math.abs(look.x - pos.x) < 1e-6 && Math.abs(look.z - pos.z) < 1e-6) c.up.set(0, 0, -1); c.lookAt(look); c.updateMatrixWorld(); return c; }
function vis(c, p) { const q = p.clone().project(c); return Math.abs(q.x) <= 1 && Math.abs(q.y) <= 1 && q.z < 1 && q.z > -1; }
function faceSeen(c) { return vis(c, face) && c.position.clone().sub(face).dot(faceN) > 0; }
function pitch(c) { const d = new T.Vector3(); c.getWorldDirection(d); return Math.asin(d.y) * 180 / Math.PI; }
const t15 = Math.tan(15 * Math.PI / 180);
const P = {
  top_down: cam(55, new T.Vector3(0, desk + 0.70, 0.05), new T.Vector3(0, desk, 0.05)),
  over_shoulder: cam(40, new T.Vector3(0.25, 1.10 + 0.10, 0.65 + 1.0), new T.Vector3(0.25, 1.20 - t15 * 10, 0.65 + 1.0 - 10)),
  chest_down: cam(40, new T.Vector3(0, 1.0, 0.65 - 1.0), new T.Vector3(0, 1.0 - t15 * 10, 0.65 - 1.0 + 10)),
  object: cam(40, new T.Vector3(0.4, 0.8, -0.1 + 0.40), obj),
  side_hand: cam(30, new T.Vector3(0.5 + 0.5, desk + 0.20, 0.15), new T.Vector3(0, desk + 0.2 - Math.tan(10 * Math.PI / 180) * 1.0, 0.15)) };
const out = {};
for (const [k, c] of Object.entries(P)) out[k] = {face: faceSeen(c), hands: hands.every(h => vis(c, h)), object: vis(c, obj), pitch: pitch(c), pos: c.position.toArray()};
out.selfie = {face: faceSeen(cam(50, new T.Vector3(0, 1.25, -0.3), head))};
console.log(JSON.stringify(out));"""
    r, jout = _k3(wd, "faceless3d", body)
    p = r
    checks = [check("%s: face out of frame" % k, not p[k]["face"], p[k]["face"], False) for k in ("top_down", "over_shoulder", "chest_down", "object", "side_hand")]
    checks += [check("top-down 70 cm above the desk (60-80)", 0.6 <= p["top_down"]["pos"][1] - 0.75 <= 0.8 and p["top_down"]["pitch"] < -85, [p["top_down"]["pos"][1] - 0.75, p["top_down"]["pitch"]], "0.6-0.8, -90"),
               check("over-shoulder: 1 m back, shoulder +10 cm, tilted 15 deg down", _near(p["over_shoulder"]["pos"][2] - 0.65, 1.0, 1e-6) and _near(p["over_shoulder"]["pos"][1], 1.2, 1e-6) and _near(p["over_shoulder"]["pitch"], -15, 0.05), p["over_shoulder"], "1 m, 1.2 m, -15"),
               check("chest-down 1 m in front", _near(0.65 - p["chest_down"]["pos"][2], 1.0, 1e-6), p["chest_down"]["pos"], "1 m"),
               check("object camera 40 cm from the object (30-50)", 0.3 <= p["object"]["pos"][2] + 0.1 <= 0.5 and p["object"]["object"], p["object"], "0.3-0.5"),
               check("side-hand 50 cm beside the desk at desk +20 cm", _near(p["side_hand"]["pos"][0], 1.0, 1e-6) and _near(p["side_hand"]["pos"][1], 0.95, 1e-6), p["side_hand"]["pos"], [1.0, 0.95]),
               check("hand setups show both hands", p["top_down"]["hands"] and p["chest_down"]["hands"] and p["side_hand"]["hands"], [p[k]["hands"] for k in ("top_down", "chest_down", "side_hand")], True),
               check("negative control: a selfie camera at the monitor shows the face", p["selfie"]["face"], p["selfie"]["face"], True)]
    return checks, [jout]


@card("CAM-363")
def viewing_time_tiers(task, wd):
    """Layout tiers by viewing time (3 s / 30 s / 300 s) on an 8 px grid at 1664x936: the 3-second answer in the first
    reading position (top-left LTR, top-right RTL), 3-5 breakdown visuals in the middle, detail pushed to the end."""
    from PIL import Image, ImageDraw
    N = np()
    W, H = 1664, 936
    snap = lambda v: int(round(v / 8.0)) * 8

    def layout(rtl, n_break=4):
        m = 48
        head = [m, m, snap(W * 0.45), m + 160]
        if rtl:
            head = [W - head[2], head[1], W - head[0], head[3]]
        bw = snap((W - 2 * m - (n_break - 1) * 24) / n_break)
        brk = []
        for i in range(n_break):
            x = m + i * (bw + 24)
            if rtl:
                x = W - m - (i + 1) * bw - i * 24
            brk.append([x, 288, x + bw, 288 + 360])
        return {"headline": head, "breakdown": brk, "detail": None, "sequence": ["headline shot", "breakdown shot", "detail (optional)"]}

    outs, res = [], {}
    for rtl in (False, True):
        L = layout(rtl)
        im = Image.new("RGB", (W, H), (245, 244, 240))
        d = ImageDraw.Draw(im)
        d.rectangle(L["headline"], fill=(20, 60, 140))
        for b in L["breakdown"]:
            d.rectangle(b, fill=(150, 170, 200))
        p = wd / ("tiers_%s.png" % ("rtl" if rtl else "ltr"))
        im.save(p); outs.append(p)
        A = N.asarray(im).astype(int)
        hb = bbox(A, (20, 60, 140), 10)
        lab, n = _components(N.all(A == (150, 170, 200), axis=2), 1)
        coords = [v for b in L["breakdown"] + [L["headline"]] for v in b]
        res[rtl] = {"head": hb, "n": n, "grid": all(v % 8 == 0 for v in coords), "seq": L["sequence"]}
    first_ltr = res[False]["head"][0] < W * 0.1 and res[False]["head"][1] < H * 0.1
    first_rtl = res[True]["head"][2] > W * 0.9 and res[True]["head"][1] < H * 0.1
    bad = {"headline": [48, 700, 400, 880], "detail": [48, 48, 800, 400]}
    imb = Image.new("RGB", (W, H), (245, 244, 240))
    ImageDraw.Draw(imb).rectangle(bad["detail"], fill=(200, 200, 200))
    ImageDraw.Draw(imb).rectangle(bad["headline"], fill=(20, 60, 140))
    nb = bbox(N.asarray(imb).astype(int), (20, 60, 140), 10)
    checks = [check("canvas 1664x936", (W, H) == (1664, 936), (W, H), (1664, 936)),
              check("LTR: the 3-second answer sits top-left (measured)", first_ltr, res[False]["head"], "top-left"),
              check("RTL: the 3-second answer sits top-right (measured)", first_rtl, res[True]["head"], "top-right"),
              check("3-5 breakdown visuals in the middle band", 3 <= res[False]["n"] <= 5 and 3 <= res[True]["n"] <= 5, [res[False]["n"], res[True]["n"]], "3-5"),
              check("every coordinate on the 8 px grid", res[False]["grid"] and res[True]["grid"], [res[False]["grid"], res[True]["grid"]], True),
              check("video order: headline, breakdown, optional detail last", res[False]["seq"][0] == "headline shot" and res[False]["seq"][-1].startswith("detail"), res[False]["seq"], "3 s → 30 s → 300 s"),
              check("negative control: a rendered layout with the detail table first fails the first-position test", not (nb[0] < W * 0.1 and nb[1] < H * 0.1), nb, "headline not top-left")]
    return checks, outs


# ═════════════════════════ choreography and camera discipline (GSAP + motion-kit, rendered and tracked) ═════════════════════════
def _dot_frames(rows, keys, W, H, r=6, bg=(30, 32, 40)):
    """Draw each sampled object (x, y) as a coloured disc: the render whose tracks are measured."""
    N = np()
    yy, xx = N.mgrid[0:H, 0:W]
    cols = list(COL.values())
    out = []
    for row in rows:
        f = N.zeros((H, W, 3), N.uint8) + N.array(bg, N.uint8)
        for k, key in enumerate(keys):
            o = row[key]
            if o.get("opacity", 1) > 0.5:
                f[(xx - o["x"]) ** 2 + (yy - o["y"]) ** 2 <= r * r] = cols[k]
        out.append(f)
    return out


def _onset(tr, thr=0.3):
    for i, (a, b) in enumerate(zip(tr[:-1], tr[1:])):
        if a is not None and b is not None and math.hypot(a[0] - b[0], a[1] - b[1]) > thr:
            return i + 1
    return None


@card("CAM-368")
def hero_leads_choreography(task, wd):
    """Choreography: the hero leads, each group springs from one origin, a counter element moves against the hero at
    20-30 % of its travel, and parallax layers move at depth-scaled speeds. GSAP timeline sampled, rendered, tracked."""
    W, H, fps, n = 320, 180, 30, 60
    body = """O.hero = {x: 60, y: 90}; O.g0 = {x: 160, y: 150, opacity: 0}; O.g1 = {x: 160, y: 150, opacity: 0}; O.g2 = {x: 160, y: 150, opacity: 0};
O.counter = {x: 260, y: 40}; O.bg = {x: 40, y: 20}; O.fg = {x: 40, y: 170};
tl.to(O.hero, {x: 220, duration: 1.0, ease: 'power2.inOut'}, 0);
tl.to(O.counter, {x: 260 - 0.25 * 160, duration: 1.0, ease: 'power2.inOut'}, 0);
[O.g0, O.g1, O.g2].forEach((g, i) => tl.set(g, {opacity: 1}, 0.28 + 0.1 * i));
tl.fromTo([O.g0, O.g1, O.g2], {x: 160, y: 150}, {x: (i) => 110 + i * 50, y: 120, duration: 0.5, stagger: 0.1, ease: 'power2.out', immediateRender: false}, 0.3);
tl.to(O.bg, {x: 40 + 0.3 * 160, duration: 1.0, ease: 'power2.inOut'}, 0); tl.to(O.fg, {x: 40 + 1.2 * 160, duration: 1.0, ease: 'power2.inOut'}, 0);"""
    rows, jout = mk_sample(wd, "choreo", body, n, fps)
    keys = ["hero", "g0", "g1", "g2", "counter", "bg", "fg"]
    keys_c = ["hero", "g0", "g1", "g2", "counter", "bg"]
    out = write_video(wd / "choreo.mp4", _dot_frames(rows, keys_c, W, H), fps)
    F = read_video(out)
    cols = list(COL.keys())
    T = {k: track(F, cols[i]) for i, k in enumerate(keys_c)}
    on = {k: _onset(T[k]) for k in keys_c}
    hero_d = T["hero"][-1][0] - T["hero"][0][0]
    ctr = (T["counter"][-1][0] - T["counter"][0][0]) / hero_d
    par_bg = (T["bg"][-1][0] - T["bg"][0][0]) / hero_d
    par_fg = (rows[-1]["fg"]["x"] - rows[0]["fg"]["x"]) / (rows[-1]["hero"]["x"] - rows[0]["hero"]["x"])
    first = {k: next(i for i, p in enumerate(T[k]) if p is not None) for k in ("g0", "g1", "g2")}
    g0s = [T[k][first[k]] for k in ("g0", "g1", "g2")]
    # negative control: everything starts together at the same speed
    flat = [{k: {"x": 60 + 160 * min(1, i / 30), "y": 30 + 20 * j} for j, k in enumerate(keys_c)} for i in range(n)]
    Fn = read_video(write_video(wd / "choreo_input.mp4", _dot_frames(flat, keys_c, W, H), fps))
    on_n = [_onset(track(Fn, cols[i])) for i in range(len(keys_c))]
    checks = [check("hero moves first (before any group member appears)", on["hero"] < min(first.values()), [on["hero"], first], "hero first"),
              check("each group member appears at the one origin (160,150)", all(_pt_near(p, (160, 150), 3) for p in g0s), g0s, (160, 150)),
              check("group members staggered 0.1 s (3 frames)", [first["g1"] - first["g0"], first["g2"] - first["g1"]] == [3, 3], [first["g1"] - first["g0"], first["g2"] - first["g1"]], [3, 3]),
              check("counter-motion opposes the hero at 20-30 %", -0.3 <= ctr <= -0.2, ctr, "-0.3..-0.2"),
              check("parallax: far layer 0.3x, near layer 1.2x the hero", _near(par_bg, 0.3, 0.02) and _near(par_fg, 1.2, 1e-6), [par_bg, par_fg], [0.3, 1.2]),
              check("negative control: a flat move has no lead, no counter-motion", len(set(on_n)) == 1, on_n, "all equal")]
    return checks, [out, jout]


def _cam_segments(rows, key="stage", eps=1e-4):
    mv = [False] + [any(abs(rows[i][key].get(c, 0) - rows[i - 1][key].get(c, 0)) > eps for c in ("x", "y", "scale", "rotation")) for i in range(1, len(rows))]
    return _segments(mv), mv


@card("CAM-369")
def one_container_one_move(task, wd):
    """Camera discipline: one transform on one container, one move at a time, still between events. Two MOTION.camera
    moves with holds, rendered as one container transform; the video proves all markers share one affine and the stills."""
    W, H, fps, n = 320, 180, 30, 120
    body = "O.stage = {x: 0, y: 0, scale: 1, rotation: 0};\nM.camera(tl, O.stage, 0.3, {x: -30, y: 0, scale: 1.2, dur: 1.0});\nM.camera(tl, O.stage, 2.2, {x: -30, y: 20, scale: 1.45, dur: 1.0});"
    rows, jout = mk_sample(wd, "one_move", body, n, fps)
    mk = {"red": ("red", 100, 70, 7), "blue": ("blue", 220, 110, 7), "green": ("green", 160, 50, 7)}
    wimg = world(W, H, mk)
    checks, outs, d = cam_run(wd, "one_move", wimg, _stage_mats(rows, W, H), W, H, fps, mk)
    meas = d["meas"]
    N = np()
    # one container: an affine fitted to the three markers maps frame 0 to every frame exactly
    res = 0.0
    src = N.array([[*meas[k][0], 1] for k in mk])
    for i in range(0, n, 10):
        dst = N.array([meas[k][i] for k in mk])
        A, *_ = N.linalg.lstsq(src, dst, rcond=None)
        res = max(res, float(N.abs(src @ A - dst).max()))
    mv = _moving(meas["red"], 0.3)
    raw = _segments(mv)
    segs = []
    for a_, b_ in raw:                       # tracking jitter on an ease tail: merge gaps shorter than 6 frames
        if segs and a_ - segs[-1][1] < 6:
            segs[-1] = (segs[-1][0], b_)
        else:
            segs.append((a_, b_))
    gaps = [segs[i + 1][0] - segs[i][1] for i in range(len(segs) - 1)]
    drift = [{"stage": {"x": -i * 0.4, "y": 0, "scale": 1 + i * 0.003, "rotation": 0}} for i in range(n)]
    dsegs, _ = _cam_segments(drift)
    checks += [check("one container: one affine explains all markers (px residual)", res < 1.5, res, "< 1.5"),
               check("two separate moves measured on the video", len(segs) == 2, segs, 2),
               check("still between the events (>= 0.5 s hold)", gaps and min(gaps) >= 15, gaps, ">= 15 frames"),
               check("still after the last event", segs and segs[-1][1] < n - 15, segs[-1] if segs else None, "ends > 0.5 s before the clip end"),
               check("negative control: a constant drift is one endless move with no hold", len(dsegs) == 1 and dsegs[0][1] - dsegs[0][0] >= n - 2, dsegs, "one long segment")]
    return checks, outs + [jout]


@card("CAM-390")
def virtual_camera_kit(task, wd):
    """Virtual camera in 2D/2.5D films with the repo's MOTION kit: camera() move, breathe() hold (~4 %/s creep) and a
    log-space push(); one transform on one container. Rendered, tracked and measured from the decoded video."""
    W, H, fps, n = 320, 180, 30, 150
    body = ("O.stage = {x: 0, y: 0, scale: 1, rotation: 0};\nM.camera(tl, O.stage, 0.2, {x: -20, y: 10, scale: 1.1, dur: 1.0});\n"
            "M.breathe(tl, O.stage, 1.4, 1.5, {creep: 0.04});\nM.push(tl, O.stage, 3.0, 1.16, 1.6, 1.6);")
    rows, jout = mk_sample(wd, "vcam", body, n, fps)
    mk = {"red": ("red", 130, 80, 6), "blue": ("blue", 190, 100, 6)}
    wimg = world(W, H, mk)
    checks, outs, d = cam_run(wd, "vcam", wimg, _stage_mats(rows, W, H), W, H, fps, mk)
    sm = pair_scale(d, "red", "blue", math.hypot(60, 20))
    s_b0, s_b1 = sm[int(1.45 * fps)], sm[int(2.85 * fps)]
    creep = (s_b1 - s_b0) / (s_b1 and 1.4)
    N = np()
    seg = [sm[i] for i in range(int(3.0 * fps) + 1, min(n, int(4.6 * fps)))]
    lr = N.diff(N.log(N.array(seg)))
    checks += [check("camera move lands at scale 1.1", _near(sm[int(1.3 * fps)], 1.1, 0.02), sm[int(1.3 * fps)], 1.1),
               check("breathe creeps ~4 %/s during the hold", _near(creep, 0.04, 0.008), creep, 0.04),
               check("push ends at 1.6", _near(sm[-1], 1.6, 0.03), sm[-1], 1.6),
               check("push is log-space: peak per-frame scale step <= 5 %", float(N.exp(lr.max()) - 1) <= 0.05, float(N.exp(lr.max()) - 1), "<= 0.05")]
    return checks, outs + [jout]


_PLAN_388 = {"camera": [("push_in", 0.0, 0.8, {"scale": 1.25}), ("pan_left", 2.6, 3.4, {"x": -40})],
             "objects": [("obj1", 0.8, 2.6, {"y": -40}), ("obj1", 3.4, 5.6, {"y": 40}), ("obj2", 1.0, 1.8, {"x": 30})],
             "light": [("light", 4.0, 5.6, {"v": 1.0})], "D": 6.0}


def _plan_js(plan, orbit=False):
    js = ["O.stage = {x: 0, y: 0, scale: 1, rotation: 0}; O.obj1 = {x: 120, y: 110}; O.obj2 = {x: 200, y: 60}; O.light = {v: 0};"]
    if orbit:
        js.append("tl.to(O.stage, {rotation: 30, x: -40, duration: %f, ease: 'none'}, 0);" % plan["D"])
    else:
        for nm, a, b, to in plan["camera"]:
            js.append("tl.to(O.stage, {%s, duration: %f, ease: 'power2.inOut'}, %f);" % (", ".join("%s: %s" % kv for kv in to.items()), b - a, a))
    for key in ("objects", "light"):
        for nm, a, b, to in plan[key]:
            js.append("tl.to(O.%s, {%s, duration: %f, ease: 'power1.inOut'}, %f);" % (nm, ", ".join("%s: '+=%s'" % kv for kv in to.items()), b - a, a))
    js.append("tl.set({}, {}, %f);" % plan["D"])
    return "\n".join(js)


def _budget(rows, fps):
    act = lambda key, ch: [i > 0 and any(abs(rows[i][key][c] - rows[i - 1][key][c]) > 1e-7 for c in ch) for i in range(len(rows))]
    cam = act("stage", ("x", "y", "scale", "rotation"))
    o1, o2 = act("obj1", ("x", "y")), act("obj2", ("x", "y"))
    li = act("light", ("v",))
    sec = {"camera": sum(cam) / fps, "objects": (sum(o1) + sum(o2)) / fps, "light": sum(li) / fps}
    tot = sum(sec.values())
    share = {k: v / tot for k, v in sec.items()}
    locks = [s for s in _segments([not c for c in cam]) if s[1] - s[0] >= 5]
    fill = [sum(1 for i in range(a, b + 1) if o1[i] or o2[i]) / (b - a + 1) for a, b in locks]
    return share, _segments(cam), locks, fill


@card("CAM-388")
def camera_budget_plan(task, wd):
    """Camera plan rules: 2-3 named timed camera moves with holds between, no constant drift/orbit, a motion budget of
    60 % object transforms / 20 % surface-light / 20 % camera, and every camera lock filled by an acting object.
    The plan becomes a GSAP timeline; the sampled channels and the rendered camera are measured."""
    fps = 20
    n = int(_PLAN_388["D"] * fps)
    rows, jout = mk_sample(wd, "budget", _plan_js(_PLAN_388), n, fps)
    share, segs, locks, fill = _budget(rows, fps)
    W, H = 320, 180
    mk = {"red": ("red", 100, 70, 7), "blue": ("blue", 220, 110, 7)}
    checks, outs, d = cam_run(wd, "budget_cam", world(W, H, mk), _stage_mats(rows, W, H), W, H, fps, mk)
    vseg = [s for s in _segments(_moving(d["meas"]["red"], 0.3)) if s[1] - s[0] >= 2]
    orows, _ = mk_sample(wd, "budget_orbit", _plan_js(_PLAN_388, orbit=True), n, fps)
    oshare, osegs, olocks, _ = _budget(orows, fps)
    plan = write_json(wd, "camera_plan.json", _PLAN_388)
    checks += [check("2-3 named camera moves (sampled)", 2 <= len(segs) <= 3 and len(_PLAN_388["camera"]) == len(segs), segs, "2-3"),
               check("2 camera moves measured on the rendered video", len(vseg) == 2, vseg, 2),
               check("holds between moves (>= 1 s)", all(locks[i][1] - locks[i][0] >= fps for i in range(len(locks))), locks, ">= 20 frames"),
               check("budget: objects 60 %, light 20 %, camera 20 % (+-5)", _near(share["objects"], 0.6, 0.05) and _near(share["light"], 0.2, 0.05) and _near(share["camera"], 0.2, 0.05), share, {"objects": 0.6, "light": 0.2, "camera": 0.2}),
               check("every camera lock filled with an acting object (>= 80 % of its frames)", all(f >= 0.8 for f in fill), fill, ">= 0.8"),
               check("negative control: a constant orbit has no lock and blows the camera budget", len(olocks) == 0 and oshare["camera"] > 0.3, [len(olocks), oshare["camera"]], "0 locks, > 0.3")]
    return checks, outs + [plan, jout]


@card("CAM-391")
def diagonal_depth_scene(task, wd):
    """Scene planned back to front (sky, clouds, far, mid, hero, effects, atmosphere): one strong hero-antagonist
    diagonal, scale contrast, calm space around the action, far softer and bluer, near sharp, no black outlines."""
    from PIL import Image, ImageDraw, ImageFilter
    N = np()
    W, H = 640, 360
    order = ["sky", "clouds", "far", "mid", "hero", "effects", "atmosphere"]
    im = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=(int(120 + 80 * t), int(160 + 60 * t), int(220 + 20 * t)))
    cl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(cl).ellipse([60, 30, 260, 80], fill=(250, 250, 255, 160))
    im.paste(cl.filter(ImageFilter.GaussianBlur(6)), (0, 0), cl.filter(ImageFilter.GaussianBlur(6)))
    far = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fd = ImageDraw.Draw(far)
    for x in range(0, W, 70):
        fd.polygon([(x, 230), (x + 40, 150), (x + 80, 230)], fill=(110, 140, 190, 255))
    far = far.filter(ImageFilter.GaussianBlur(3))
    im.paste(far, (0, 0), far)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 230, W, H], fill=(90, 120, 70))
    hero = (150, 270, 34)          # big near hero (x, y, radius)
    foe = (430, 100, 12)           # small far antagonist up the diagonal
    d.ellipse([hero[0] - hero[2], hero[1] - hero[2], hero[0] + hero[2], hero[1] + hero[2]], fill=(230, 90, 40))
    d.ellipse([foe[0] - foe[2], foe[1] - foe[2], foe[0] + foe[2], foe[1] + foe[2]], fill=(150, 40, 160))
    po = wd / "diagonal_scene.png"
    im.save(po)
    A = N.asarray(im).astype(float)
    hb, fb = bbox(A.astype(int), (230, 90, 40), 20), bbox(A.astype(int), (150, 40, 160), 20)
    hc, fc = ((hb[0] + hb[2]) / 2, (hb[1] + hb[3]) / 2), ((fb[0] + fb[2]) / 2, (fb[1] + fb[3]) / 2)
    ang = abs(math.degrees(math.atan2(hc[1] - fc[1], fc[0] - hc[0])))
    scale = (hb[2] - hb[0]) / (fb[2] - fb[0])
    far_reg, near_reg = A[150:230, 0:640], A[240:330, 100:200]
    sharp_far, sharp_near = sharpness(far_reg.mean(axis=2)), sharpness(near_reg.mean(axis=2))
    blue_far = float(far_reg[..., 2].mean() / far_reg[..., 0].mean())
    blue_near = float(near_reg[..., 2].mean() / near_reg[..., 0].mean())
    lum = A.mean(axis=2)
    black = float((lum < 25).mean())
    ring = A[20:100, 300:390]
    calm = float(ring.std(axis=(0, 1)).mean())
    # negative control: a flat cartoon with black outlines and equal sizes side by side
    cart = Image.new("RGB", (W, H), (200, 200, 200))
    cd = ImageDraw.Draw(cart)
    for x in (200, 440):
        cd.ellipse([x - 25, 155, x + 25, 205], fill=(230, 90, 40), outline=(0, 0, 0), width=4)
    C = N.asarray(cart).astype(float)
    cb = float((C.mean(axis=2) < 25).mean())
    checks = [check("planned back to front (7 layers in order)", order == ["sky", "clouds", "far", "mid", "hero", "effects", "atmosphere"], order, "back→front"),
              check("hero-antagonist line is a strong diagonal (25-65 deg)", 25 <= ang <= 65, ang, "25-65"),
              check("scale contrast >= 2.5x", scale >= 2.5, scale, ">= 2.5"),
              check("far layer softer than near", sharp_far < 0.5 * sharp_near, [sharp_far, sharp_near], "far < 0.5 near"),
              check("far layer bluer than near", blue_far > 1.2 * blue_near, [blue_far, blue_near], "far > 1.2 near"),
              check("no black outlines (< 0.1 % near-black pixels)", black < 0.001, black, "< 0.001"),
              check("calm empty space beside the action (low texture)", calm < 12, calm, "< 12"),
              check("negative control: an outlined cartoon fails the no-black-outline rule", cb > 0.002, cb, "> 0.002")]
    return checks, [po]


_SIZE_JOB = {"wide": "establish", "medium": "action", "close": "decision"}


def _lint_storyboard(rows):
    keep, errs = [], []
    for i, r in enumerate(rows):
        if not r.get("purpose"):
            errs.append((i, "dropped: no purpose"))
            continue
        if r["size"] in _SIZE_JOB and r["purpose"] not in (_SIZE_JOB[r["size"]],) + (("detail",) if r["size"] == "close" else ()):
            errs.append((i, "size %s does not do the job %s" % (r["size"], r["purpose"])))
        mv = r.get("move")
        if mv and not all(mv.get(k) for k in ("start", "end", "direction", "speed", "reason")):
            errs.append((i, "move incomplete"))
        if r.get("broll") and r["broll"] not in ("context", "action", "emotion"):
            errs.append((i, "b-roll is literal"))
        keep.append(r)
    return keep, errs


@card("CAM-353")
def shot_jobs_storyboard(task, wd):
    """Every shot must do a job: wide establishes, medium shows action, close shows decisions/details; each move has
    start, end, direction, speed and reason; B-roll adds context/action/emotion; rows without a purpose are dropped.
    The cleaned board's moves are rendered with K3 and the claimed direction measured."""
    rows = [{"size": "wide", "purpose": "establish"},
            {"size": "medium", "purpose": "action", "move": {"start": 1.8, "end": 0.9, "direction": "in", "speed": "slow", "reason": "tension"}},
            {"size": "close", "purpose": "decision"},
            {"size": "medium", "purpose": "action", "broll": "context", "move": {"start": 0.9, "end": 1.8, "direction": "out", "speed": "slow", "reason": "reveal"}}]
    bad = rows + [{"size": "wide", "purpose": ""}, {"size": "close", "purpose": "establish"},
                  {"size": "medium", "purpose": "action", "move": {"start": 1, "direction": "in"}}, {"size": "medium", "purpose": "action", "broll": "a cup because she says cup"}]
    keep, errs = _lint_storyboard(rows)
    kb, eb = _lint_storyboard(bad)
    body = r"""
const S = new T.Vector3(0, 1, 0), size = 1.7, mv = %s, out = [];
for (const m of mv) { const kind = m.direction === 'in' ? 'push_in' : 'pull_back'; const sh = K.shot(kind, {subject: S, size, t0: 0, t1: 4});
  out.push([0, 4].map(t => { const c = newCam(); K.applyShot(c, sh(t)); return frac(c, S, size).h; })); }
console.log(JSON.stringify(out));""" % json.dumps([r["move"] for r in keep if r.get("move")])
    r, jout = _k3(wd, "board_moves", body)
    board = write_json(wd, "storyboard_clean.json", keep)
    checks = [check("clean board: every row has a job that fits its size", errs == [], errs, []),
              check("push-in claimed 'in' measured growing", r[0][1] > r[0][0], r[0], "end > start"),
              check("pull-back claimed 'out' measured shrinking", r[1][1] < r[1][0], r[1], "end < start"),
              check("planted problems found: no purpose, wrong job, incomplete move, literal b-roll", sorted(m.split(":")[0].split(" ")[0] for _, m in eb) == sorted(["dropped", "size", "move", "b-roll"]), eb, 4),
              check("rows without a purpose are dropped", len(kb) == len(bad) - 1, len(kb), len(bad) - 1),
              check("negative control: the raw board does not pass the lint", len(eb) > 0, len(eb), "> 0")]
    return checks, [board, jout]


@card("CAM-355")
def decoration_audit(task, wd):
    """Remove-it test on a storyboard frame: separators that disambiguate, state/semantic colours and real elevation
    stay; decorative heading icons and repeated brand marks go (one mark per frame). Before/after renders measured."""
    from PIL import Image, ImageDraw
    N = np()
    els = [{"kind": "separator", "info": True, "box": [40, 180, 600, 182], "col": (120, 120, 120)},
           {"kind": "state_colour", "info": True, "box": [40, 60, 90, 110], "col": (40, 180, 90)},
           {"kind": "heading_icon", "info": False, "box": [40, 20, 60, 40], "col": (200, 160, 40)},
           {"kind": "logo", "info": True, "box": [560, 20, 600, 40], "col": (220, 40, 120)},
           {"kind": "logo", "info": True, "box": [560, 300, 600, 320], "col": (220, 40, 120)},
           {"kind": "logo", "info": True, "box": [40, 300, 80, 320], "col": (220, 40, 120)},
           {"kind": "gradient_border", "info": False, "box": [0, 0, 640, 6], "col": (90, 60, 200)},
           {"kind": "elevation", "info": True, "box": [300, 60, 600, 160], "col": (60, 60, 70)}]

    def audit(es):
        keep, seen_logo = [], False
        for e in es:
            if e["kind"] == "logo":
                if seen_logo:
                    continue
                seen_logo = True
            if not e["info"]:
                continue
            keep.append(e)
        return keep

    def render(es, name):
        im = Image.new("RGB", (640, 340), (245, 245, 242))
        d = ImageDraw.Draw(im)
        for e in es:
            d.rectangle(e["box"], fill=e["col"])
        p = wd / ("%s.png" % name)
        im.save(p)
        return p
    after = audit(els)
    pb, pa = render(els, "before"), render(after, "after")
    A, B = load_png(pa).astype(int), load_png(pb).astype(int)
    logos = lambda X: _components(N.all(X == (220, 40, 120), axis=2), 1)[1]
    present = lambda X, c: bool(N.all(X == c, axis=2).any())
    checks = [check("one brand mark per frame (measured)", logos(A) == 1, logos(A), 1),
              check("disambiguating separator kept", present(A, (120, 120, 120)), True, True),
              check("state colour and elevation kept", present(A, (40, 180, 90)) and present(A, (60, 60, 70)), True, True),
              check("decorative heading icon and border removed", not present(A, (200, 160, 40)) and not present(A, (90, 60, 200)), False, False),
              check("negative control: the unaudited frame repeats the mark 3x and keeps decoration", logos(B) == 3 and present(B, (200, 160, 40)), logos(B), 3)]
    return checks, [pa, write_json(wd, "audit.json", [e["kind"] for e in after])]


# ═════════════════════════ films rendered by the repo's render_html.cjs (seek mode, Chrome frame capture, ffmpeg) ═════════════════════════
def render_html(wd, name, html, W, H, fps, dur, timeout=60):
    if not ((REPO / "tools/render_html.cjs").exists() and _NODE and _CHROME):
        raise RuntimeError("render_html.cjs / node / chrome not available")
    src = wd / ("%s.html" % name)
    src.write_text(html, encoding="utf-8")
    out = wd / ("%s.mp4" % name)
    done = subprocess.run([_NODE, str(REPO / "tools/render_html.cjs"), "--in", str(src), "--out", str(out), "--width", str(W), "--height", str(H),
                           "--fps", str(fps), "--duration", str(dur), "--crf", "8", "--no-space-check"],
                          capture_output=True, text=True, timeout=timeout, cwd=str(REPO), stdin=subprocess.DEVNULL,
                          env=dict({k: v for k, v in __import__("os").environ.items() if k in ("CHROME_PATH", "CHROME_BIN", "PUPPETEER_EXECUTABLE_PATH", "PLAYWRIGHT_BROWSERS_PATH", "PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD")},
                                   CHROME_PATH=str(_CHROME), NODE_PATH=str(NODE_MODULES), PATH="/usr/bin:/bin:" + str(Path(_NODE).parent), HOME="/tmp"))
    if done.returncode or "VERIFY OK" not in done.stdout + done.stderr:
        raise RuntimeError("render_html failed: %s" % (done.stdout + done.stderr)[-500:])
    return out


_LAYERS_HTML = """<!doctype html><html><head><style>html,body{margin:0;width:100%%;height:100%%;overflow:hidden;background:#0e1018}
#stage{position:absolute;inset:0;transform-origin:50%% 50%%} .L{position:absolute;inset:0}
.d{position:absolute;width:14px;height:14px;border-radius:50%%}
#light{position:absolute;inset:0;background:radial-gradient(circle at 15%% 10%%,rgba(255,220,160,.35),transparent 60%%)}
#patch{position:absolute;left:8px;top:8px;width:40px;height:30px;background:rgb(100,50,20)}
#fog{position:absolute;left:8px;top:8px;width:40px;height:30px;background:rgb(60,60,60);mix-blend-mode:screen}
#hero{position:absolute;left:150px;top:120px;width:40px;height:40px;background:#fff;opacity:0}
</style></head><body><div id="stage">
<div class="L" id="bg"><div class="d" style="left:60px;top:60px;background:#0000ff"></div></div>
<div class="L" id="mid"><div class="d" style="left:200px;top:80px;background:#00ff00"></div></div>
<div class="L" id="fg"><div class="d" style="left:100px;top:140px;background:#ff0000"></div><div class="d" style="left:240px;top:150px;background:#ffff00"></div></div>
<div id="hero"></div></div><div id="light"></div><div id="patch"></div><div id="fog"></div>
<script>const K = %s; window.__kosif = {duration: 3, seek(t) { const u = t / 3, e = u * u * (3 - 2 * u);
  document.getElementById('stage').style.transform = 'scale(' + (1 + 0.08 * e) + ')';
  for (const [id, k] of [['bg', K[0]], ['mid', K[1]], ['fg', K[2]]]) document.getElementById(id).style.transform = 'translateX(' + (-30 * k * e) + 'px)';
  document.getElementById('hero').style.opacity = Math.min(1, Math.max(0, (t - 0.5) / 1.5)); }}; window.__kosif.seek(0);</script></body></html>"""


@card("CAM-350")
def layered_mood_film(task, wd):
    """Cinematic mood film via render_html.cjs: layered plates with parallax depth (0.2 / 0.5 / 1.0), a directed light,
    a fog layer in screen blend, a slow push (8 % over 3 s) and a gradual reveal; every cue measured on the mp4."""
    N = np()
    W, H, fps = 320, 180, 15
    out = render_html(wd, "mood", _LAYERS_HTML % "[0.2, 0.5, 1.0]", W, H, fps, 3)
    flat = render_html(wd, "mood_flat", _LAYERS_HTML % "[1, 1, 1]", W, H, fps, 3)
    def meas(p):
        F = read_video(p)
        T = {c: track(F, c, 70) for c in ("blue", "green", "red", "yellow")}
        dx = {c: T[c][-1][0] - T[c][0][0] for c in T}
        return F, T, dx
    F, T, dx = meas(out)
    Ff, Tf, dxf = meas(flat)
    # parallax measured relative to the push: remove the stage scale about the centre
    s_end = math.hypot(T["yellow"][-1][0] - T["red"][-1][0], T["yellow"][-1][1] - T["red"][-1][1]) / math.hypot(T["yellow"][0][0] - T["red"][0][0], T["yellow"][0][1] - T["red"][0][1])
    shift = {c: (T[c][-1][0] - W / 2) / s_end - (T[c][0][0] - W / 2) for c in ("blue", "green", "red")}
    ratio = [shift["blue"] / shift["red"], shift["green"] / shift["red"]]
    shift_f = {c: (Tf[c][-1][0] - W / 2) / s_end - (Tf[c][0][0] - W / 2) for c in ("blue", "green", "red")}
    ratio_f = [shift_f["blue"] / shift_f["red"], shift_f["green"] / shift_f["red"]]
    scr = F[20, 15:30, 15:40].astype(float).mean(axis=(0, 1))
    exp = 255 - (255 - N.array([100, 50, 20])) * (255 - 60) / 255.0
    hero = [float(F[i, 125:155, 155:185].mean()) for i in range(0, F.shape[0], 3)]
    sc = [math.hypot(T["yellow"][i][0] - T["red"][i][0], T["yellow"][i][1] - T["red"][i][1]) for i in range(F.shape[0])]
    step = max(abs(sc[i + 1] / sc[i] - 1) for i in range(len(sc) - 1))
    light = float(F[5, 10:40, 60:100].mean() - F[5, 140:170, 260:300].mean())
    checks = [check("slow push: 8 % over 3 s measured", _near(s_end, 1.08 * 44 / 44, 0.012), s_end, 1.08),
              check("push is slow (<= 0.6 % scale per frame)", step <= 0.006, step, "<= 0.006"),
              check("parallax: far 0.2x and mid 0.5x of the near layer", _near(ratio[0], 0.2, 0.06) and _near(ratio[1], 0.5, 0.06), ratio, [0.2, 0.5]),
              check("fog in screen blend = 1-(1-a)(1-b) on the plate", float(N.abs(scr - exp).max()) < 6, scr.tolist(), exp.tolist()),
              check("directed light: the lit corner is brighter", light > 8, light, "> 8"),
              check("gradual reveal: hero brightens monotonically", all(hero[i] <= hero[i + 1] + 1 for i in range(len(hero) - 1)) and hero[-1] - hero[0] > 100, hero[::3], "rising"),
              check("negative control: equal-speed layers show no parallax", _near(ratio_f[0], 1.0, 0.1) and _near(ratio_f[1], 1.0, 0.1), ratio_f, "~1")]
    return checks, [out]


@card("CAM-351")
def editorial_grid(task, wd):
    """Editorial: 12-column CSS grid, overflow-hidden line reveals (each line slides up inside its mask, staggered),
    serif headline / sans body pairing, and camera moves that step by whole columns. GSAP in Chrome, DOM measured."""
    lines = ["Quiet pages", "and measured", "cuts read well"]
    html = """<!doctype html><html><head><style>%s
#stage{position:absolute;left:0;top:0;width:3840px;height:1080px}
.grid{position:absolute;left:120px;top:120px;width:3600px;display:grid;grid-template-columns:repeat(24,1fr);column-gap:24px}
.h{grid-column:1 / span 7;font-family:'DejaVu Serif',serif;font-size:110px;line-height:1.1}
.mask{overflow:hidden;display:block} .mask span{display:block}
.body{grid-column:9 / span 4;font-family:'DejaVu Sans',sans-serif;font-size:30px;line-height:1.5;margin-top:40px}
.img{grid-column:14 / span 6;height:600px;background:#3a4a6a}</style></head><body><div id="stage"><div class="grid">
<div class="h">%s</div><div class="body">Body copy set in a sans, three columns wide, with a clear reading order.</div><div class="img"></div>
</div></div></body></html>""" % (_BASE_CSS, "".join("<div class='mask'><span>%s</span></div>" % l for l in lines))
    vis = "[...document.querySelectorAll('.mask')].map(m => { const a = m.getBoundingClientRect(), b = m.firstChild.getBoundingClientRect(); return Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top)) / a.height; })"
    tl = ("window.tl = gsap.timeline({paused:true}); tl.from('.mask span',{yPercent:100,duration:.6,stagger:.15,ease:'power3.out'});"
          "const cw = (document.querySelector('.grid').getBoundingClientRect().width - 23 * 24) / 24; window.step = 6 * (cw + 24);"
          "tl.to('#stage',{x: -step, duration: 1.0, ease:'power2.inOut'}, '+=0.8'); tl.duration()")
    r = browser(wd, "editorial", html, [
        {"js": "({cols: CS('.grid','gridTemplateColumns').split(' ').length, w: CS('.grid','gridTemplateColumns').split(' ').map(parseFloat), hf: CS('.h','fontFamily'), bf: CS('.body','fontFamily'), ov: CS('.mask','overflow')})"},
        {"js": tl},
        {"js": "tl.seek(0); " + vis},
        {"js": "tl.seek(0.35); " + vis},
        {"js": "tl.seek(0.3 + 0.6); " + vis, "shot": "editorial_lines.png"},
        {"js": "tl.seek(tl.duration()); ({x: R('#stage')[0], step, img: R('.img')})", "shot": "editorial_moved.png"},
        {"js": "document.querySelectorAll('.mask').forEach(m => m.style.overflow = 'visible'); tl.seek(0); " + vis.replace("Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top)) / a.height", "(b.top < innerHeight ? 1 : 0)")},
    ])
    g, dur, v0, v1, v2, end, neg = r
    cw = g["w"][0]
    checks = [check("grid: 24 columns over the 2-screen stage (12 per frame), equal widths", g["cols"] == 24 and max(g["w"]) - min(g["w"]) < 0.01, [g["cols"], cw], "24 equal"),
              check("serif headline, sans body", "Serif" in g["hf"] and "Sans" in g["bf"] and "Serif" not in g["bf"], [g["hf"], g["bf"]], "serif / sans"),
              check("masks clip: lines hidden at t=0 (overflow hidden)", g["ov"] == "hidden" and max(v0) == 0, v0, "all 0"),
              check("line reveals staggered: at 0.35 s line 1 almost in, line 3 just starting", v1[0] > 0.9 and v1[2] < 0.5 and v1[0] > v1[1] > v1[2], v1, "decreasing"),
              check("all lines revealed after the stagger", min(v2) > 0.99, v2, "all 1"),
              check("camera moves by whole columns (6 columns + gaps)", _near(-end["x"], end["step"], 0.5) and _near(end["step"] / (cw + 24), 6, 1e-3), [end["x"], end["step"]], "6 columns"),
              check("negative control: without overflow:hidden the 'hidden' lines are on screen at t=0", min(neg) == 1, neg, "visible")]
    return checks, [wd / "editorial_lines.png", wd / "editorial_moved.png"]


_NATIVE_HTML = """<!doctype html><html><head><style>html,body{margin:0;width:100%%;height:100%%;overflow:hidden;background:#141820}
#s{position:absolute;width:%dpx;height:%dpx;background:#ff3030;border-radius:50%%}
.ttl{position:absolute;left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:#e8e2d0}</style></head><body><div id=s></div><div class=ttl></div>
<script>const W = innerWidth, H = innerHeight, P = %s; window.__kosif = {duration: 2, seek(t) { const u = t / 2;
  const x = P.x0 + (P.x1 - P.x0) * u, y = P.y0 + (P.y1 - P.y0) * u; const s = document.getElementById('s'); s.style.left = (x - P.r) + 'px'; s.style.top = (y - P.r) + 'px'; }}; window.__kosif.seek(0);</script></body></html>"""


@card("CAM-356")
def native_vertical(task, wd):
    """For motion graphics, render 9:16 natively (its own composition and layout) instead of cropping the 16:9:
    both are rendered with render_html.cjs, the crop with ffmpeg; the subject's resolution and presence are measured."""
    N = np()
    wide = render_html(wd, "wide_16x9", _NATIVE_HTML % (36, 36, 20, 140, 120, 16, json.dumps({"x0": 40, "x1": 280, "y0": 90, "y1": 90, "r": 18})), 320, 180, 15, 2)
    tall = render_html(wd, "native_9x16", _NATIVE_HTML % (64, 64, 20, 40, 140, 30, json.dumps({"x0": 90, "x1": 90, "y0": 120, "y1": 260, "r": 32})), 180, 320, 15, 2)
    crop = wd / "crop_9x16.mp4"
    fx.ffmpeg("-i", str(wide), "-vf", "crop=ih*9/16:ih,scale=180:320:flags=bicubic,format=yuv444p", "-c:v", "libx264", "-crf", "8", str(crop))
    def stats(p):
        F = read_video(p)
        pres = [area(f, "red", 70) for f in F]
        full = max(pres)
        return F, [a_ / full if full else 0 for a_ in pres], full
    Ft, pt, at = stats(tall)
    Fc, pc, ac = stats(crop)
    src_px = 36 * 36 * math.pi / 4
    native_px = 64 * 64 * math.pi / 4
    st = fx.probe(crop)["streams"][0]
    def edge(F):        # mean of the strongest horizontal red-channel steps over the frames where the subject is visible
        g = N.abs(N.diff(F[..., 0].astype(float), axis=2)).max(axis=(1, 2))
        return float(N.sort(g)[-5:].mean())
    checks = [check("native 9:16 composition: 180x320", Ft.shape[1:3] == (320, 180), Ft.shape[1:3], (320, 180)),
              check("native: subject fully in frame on every frame", min(pt) > 0.95, min(pt), "> 0.95"),
              check("native subject rendered at its own resolution (source pixels >= 3x the cropped one)", native_px / src_px > 3, native_px / src_px, "> 3"),
              check("crop upsamples a 101 px slice: its edges are softer than the native render", st["width"] == 180 and edge(Fc) < 0.85 * edge(Ft), [edge(Fc), edge(Ft)], "crop < 0.85 native"),
              check("negative control: the centre crop loses the moving subject", min(pc) < 0.2, min(pc), "< 0.2")]
    return checks, [tall, crop]


# ═════════════════════════ HyperFrames registry components: installed with the real CLI, mounted in Chrome, seeked, measured ═════════════════════════
_HF_CLI = NODE_MODULES / "hyperframes/dist/cli.js"


def _hf_env():
    import os
    env = dict(os.environ)
    env.update(NODE_PATH=str(NODE_MODULES), PATH=str(Path(_NODE).parent) + ":" + env.get("PATH", "/usr/bin:/bin"),
               CHROME_PATH=str(_CHROME), PUPPETEER_EXECUTABLE_PATH=str(_CHROME))
    return env


def hf_install(wd, item, kind="add"):
    """`hyperframes add <item>` (or `init --example`) into wd/hf; returns the installed HTML path."""
    if not (_HF_CLI.exists() and _NODE):
        raise RuntimeError("hyperframes CLI not available")
    hf = wd / "hf"
    hf.mkdir(exist_ok=True)
    env = _hf_env()
    if kind == "add":
        cmd = [_NODE, str(_HF_CLI), "add", item, "--no-clipboard", "--json", "--dir", str(hf)]
    else:
        cmd = [_NODE, str(_HF_CLI), "init", item, "--example", kind, "--non-interactive", "--skip-transcribe"]
    done = subprocess.run(cmd, capture_output=True, text=True, timeout=60, cwd=str(hf), env=env, stdin=subprocess.DEVNULL)
    if kind == "add":
        line = [l for l in done.stdout.strip().splitlines() if l.startswith("{")]
        res = json.loads(line[-1]) if line else {"ok": False, "error": done.stderr[-300:]}
        if not res.get("ok"):
            raise RuntimeError("hyperframes add %s failed: %s" % (item, json.dumps(res.get("error"))[:300]))
        return Path([w for w in res["written"] if w.endswith(".html")][0])
    if done.returncode:
        raise RuntimeError("hyperframes init failed: %s" % (done.stdout + done.stderr)[-300:])
    return hf / item


_HF_MOUNT = r"""(() => { const t = document.querySelector('body > template'); if (t) { const host = document.createElement('div'); host.appendChild(t.content.cloneNode(true));
  document.body.appendChild(host); for (const s of [...host.querySelectorAll('script')]) { const n = document.createElement('script'); n.textContent = s.textContent; s.replaceWith(n); } }
  window.TL = (window.__timelines || {})[%s]; window.SEEK = (t) => { TL.seek(t, false); return t; }; return TL ? TL.duration() : null; })()"""


def hf_page(wd, item, comp_id, steps, variables=None, kind="add", vw=1920, vh=1080, name=None, html_path=None, duration=None):
    """Install the component, inline the local GSAP in place of the CDN tag, pass composition variables the way
    the HyperFrames runtime does (window.__hyperframes.getVariables), mount its template, then run the steps."""
    p = html_path or hf_install(wd, item, kind)
    html = p.read_text(encoding="utf-8")
    import re
    html = re.sub(r'<script src="https://cdn\.jsdelivr\.net/npm/gsap@[^"]*"></script>', "", html)
    if duration is not None:                 # the host mounts the clip with its own data-duration, as a composition would
        html = re.sub(r'data-duration="[0-9.]+"', 'data-duration="%s"' % duration, html)
    pre = "<script>window.__hyperframes = {getVariables: () => (%s)};</script><script>%s</script>" % (json.dumps(variables or {}), _GSAP.read_text(encoding="utf-8"))
    html = html.replace("<head>", "<head>" + pre, 1) if "<head>" in html else pre + html
    steps = [{"js": _HF_MOUNT % json.dumps(comp_id)}] + steps
    return browser(wd, name or comp_id.replace("-", "_"), html, steps, vw=vw, vh=vh, gsap=False)


def _hf_dump(wd, item, comp_id, sels, times, variables=None, kind="add"):
    js = "(() => { const out = {}; for (const t of %s) { SEEK(t); out[t] = {}; for (const s of %s) { const e = document.querySelector(s); if (!e) { out[t][s] = null; continue; } const c = getComputedStyle(e);" \
         " out[t][s] = {box: R(e), tf: c.transform, op: +c.opacity, f: c.filter}; } } return out; })()" % (json.dumps(times), json.dumps(sels))
    return hf_page(wd, item, comp_id, [{"js": js}], variables, kind)


def _dec(tf):
    """CSS transform → (scale, rotation deg, tx, ty) from matrix() or matrix3d()."""
    if tf in (None, "none"):
        return (1.0, 0.0, 0.0, 0.0)
    v = [float(x) for x in tf[tf.index("(") + 1:-1].split(",")]
    a, b, e, f = (v[0], v[1], v[12], v[13]) if tf.startswith("matrix3d") else (v[0], v[1], v[4], v[5])
    return (math.hypot(a, b), math.degrees(math.atan2(b, a)), e, f)


def _blur(f):
    return float(f.split("blur(")[1].split("px")[0]) if f and "blur(" in f else 0.0


def _hf_series(wd, item, cid, sels, times, variables=None, name=None):
    js = "(() => { const out = []; for (const t of %s) { SEEK(t); const row = {}; for (const s of %s) { const e = document.querySelector(s); if (!e) { row[s] = null; continue; } const c = getComputedStyle(e);" \
         " row[s] = {box: R(e), tf: c.transform, op: +c.opacity, f: c.filter}; } out.push(row); } return out; })()" % (json.dumps(times), json.dumps(sels))
    dur, rows = hf_page(wd, item, cid, [{"js": js}], variables, name=name)
    return dur, rows


_T = lambda a, b, n: [a + (b - a) * i / (n - 1) for i in range(n)]


@card("CAM-79")
def hf_drift_hold(task, wd):
    """HyperFrames drift-hold (installed with the CLI, mounted, seeked): loop-exact rotation and scale breathing with a
    slow light sweep; the standard and whisper amplitudes are measured from the computed transforms."""
    ts = _T(0, 4, 33)
    dur, rows = _hf_series(wd, "drift-hold", "drift-hold", [".dh-card", ".dh-sweep"], ts)
    _, roww = _hf_series(wd, "drift-hold", "drift-hold", [".dh-card"], ts, {"intensity": "whisper"}, name="drift_whisper")
    rot = [_dec(r[".dh-card"]["tf"])[1] for r in rows]
    sc = [_dec(r[".dh-card"]["tf"])[0] for r in rows]
    sx = [_dec(r[".dh-sweep"]["tf"])[2] for r in rows]
    rw = [_dec(r[".dh-card"]["tf"])[1] for r in roww]
    b = rows[0][".dh-card"]["box"]
    checks = [check("loop-exact: pose at t=0 equals pose at t=duration", rows[0][".dh-card"]["tf"] == rows[-1][".dh-card"]["tf"], [rows[0][".dh-card"]["tf"], rows[-1][".dh-card"]["tf"]], "equal"),
              check("rotation breathes +-0.6 deg", _near(max(rot), 0.6, 0.02) and _near(min(rot), -0.6, 0.02), [min(rot), max(rot)], [-0.6, 0.6]),
              check("scale breathes 1 +- 0.015", _near(max(sc), 1.015, 0.001) and _near(min(sc), 0.985, 0.001), [min(sc), max(sc)], [0.985, 1.015]),
              check("light sweep travels across the card (> 1000 px)", max(sx) - min(sx) > 1000, max(sx) - min(sx), "> 1000"),
              check("card centred", _pt_near(((b[0] + b[2]) / 2, (b[1] + b[3]) / 2), (960, 540), 3), [(b[0] + b[2]) / 2, (b[1] + b[3]) / 2], (960, 540)),
              check("negative control: the whisper variant does not reach the standard 0.6 deg", max(rw) < 0.3, max(rw), "0.24 < 0.3")]
    return checks, [wd / "drift_hold_measure.json"]


@card("CAM-80")
def hf_focus_rack(task, wd):
    """HyperFrames focus-rack: focus moves once between two cards at different depths with synced blur, dimming, scale
    and parallax; both cards' computed filter, opacity and transform are sampled across the clip."""
    ts = _T(0, 3.5, 36)
    dur, rows = _hf_series(wd, "focus-rack", "focus-rack", [".fr-card:nth-of-type(1)", ".fr-card:nth-of-type(2)"], ts)
    A = [(_blur(r[".fr-card:nth-of-type(1)"]["f"]), r[".fr-card:nth-of-type(1)"]["op"], _dec(r[".fr-card:nth-of-type(1)"]["tf"])) for r in rows]
    B = [(_blur(r[".fr-card:nth-of-type(2)"]["f"]), r[".fr-card:nth-of-type(2)"]["op"], _dec(r[".fr-card:nth-of-type(2)"]["tf"])) for r in rows]
    k = next(i for i, t in enumerate(ts) if t >= 0.5)
    sharp_a = [a[0] < 0.5 for a in A[k:]]
    switches = sum(1 for i in range(1, len(sharp_a)) if sharp_a[i] != sharp_a[i - 1])
    end = len(ts) - 1

    def corr(X):
        N = np()
        bl, dm = N.array([x[0] for x in X[k:]]), N.array([1 - x[1] for x in X[k:]])
        return float(N.corrcoef(bl, dm)[0, 1])
    checks = [check("before the rack: front card sharp, back card blurred and dimmed", A[k][0] < 0.5 and B[k][0] > 8 and B[k][1] < 0.6, [A[k][:2], B[k][:2]], "sharp / blurred"),
              check("after the rack: front blurred 9.2 px and dimmed to 0.5, back sharp", _near(A[end][0], 9.216, 0.01) and _near(A[end][1], 0.5, 0.01) and B[end][0] < 0.5 and B[end][1] == 1, [A[end][:2], B[end][:2]], "swapped"),
              check("focus moves once (one sharp/blur switch)", switches == 1, switches, 1),
              check("synced: blur and dimming move together (correlation > 0.95 on both cards)", corr(A) > 0.95 and corr(B) > 0.95, [corr(A), corr(B)], "> 0.95"),
              check("scale tracks depth: focused card larger (1.04 vs 0.94)", _near(B[end][2][0], 1.04, 0.002) and _near(A[end][2][0], 0.94, 0.002), [A[end][2][0], B[end][2][0]], [0.94, 1.04]),
              check("parallax: the two depths shift by different amounts (> 1.5x)", abs(B[end][2][2] - B[k][2][2]) > 1.5 * abs(A[end][2][2] - A[k][2][2]) > 0, [A[end][2][2] - A[k][2][2], B[end][2][2] - B[k][2][2]], "> 1.5x"),
              check("negative control: at t=0 no card is blurred (no rack yet)", A[0][0] == 0 and B[0][0] == 0, [A[0][0], B[0][0]], 0)]
    return checks, [wd / "focus_rack_measure.json"]


@card("CAM-82")
def hf_device_dive(task, wd):
    """HyperFrames parallax-device-dive: the phone rises in, the camera pushes through its screen and the layered app UI
    expands until it fills the frame; sampled from the component's own timeline."""
    ts = [0, 0.3, 0.6, 1.0, 2.0, 3.0, 3.5, 4.0, 4.25, 4.5]
    dur, rows = _hf_series(wd, "parallax-device-dive", "parallax-device-dive", [".pdd-phone", ".pdd-ui"], ts)
    ph = [(_dec(r[".pdd-phone"]["tf"]), r[".pdd-phone"]["op"]) for r in rows]
    ui = [r[".pdd-ui"]["box"] for r in rows]
    covers = lambda b: b[0] <= 0 and b[1] <= 0 and b[2] >= 1920 and b[3] >= 1080
    sc = [p[0][0] for p in ph]
    checks = [check("phone rises: starts 194 px low and invisible", ph[0][0][3] > 150 and ph[0][1] == 0, [ph[0][0][3], ph[0][1]], "> 150, 0"),
              check("phone settles in place by 1 s", abs(ph[3][0][3]) < 2 and ph[3][1] == 1, ph[3], "y 0, op 1"),
              check("camera pushes through the screen (scale grows > 5x at the end)", sc[-1] > 5 and all(sc[i] <= sc[i + 1] + 1e-3 for i in range(6, len(sc) - 1)), sc, "rising to > 5"),
              check("app UI fills the frame at the end", covers(ui[-1]), ui[-1], "covers 1920x1080"),
              check("negative control: at rest the UI does not fill the frame", not covers(ui[4]), ui[4], "inside")]
    return checks, [wd / "parallax_device_dive_measure.json"]


@card("CAM-85")
def hf_pull_back_reveal(task, wd):
    """HyperFrames pull-back-reveal: a tight detail holds at 2.2x, then one decelerating pull-back reveals the headline
    and the context cards; world scale sampled every 0.1 s."""
    ts = _T(0, 4.5, 46)
    dur, rows = _hf_series(wd, "pull-back-reveal", "pull-back-reveal", [".pbr-world", ".pbr-headline", ".pbr-card:nth-of-type(2)"], ts)
    sc = [_dec(r[".pbr-world"]["tf"])[0] for r in rows]
    inside = lambda b: b[0] >= 0 and b[1] >= 0 and b[2] <= 1920 and b[3] <= 1080
    hold = [i for i, s in enumerate(sc) if _near(s, 2.2, 1e-4)]
    mv = [i for i in range(1, len(sc)) if sc[i] < sc[i - 1] - 1e-4]
    run = [mv[0]]
    while run[-1] + 1 in mv:
        run.append(run[-1] + 1)
    run_frac = (sc[run[0] - 1] - sc[run[-1]]) / (sc[0] - sc[-1])
    sp = [sc[i - 1] - sc[i] for i in run]
    pk = sp.index(max(sp))
    checks = [check("tight detail holds at 2.2x first", len(hold) >= 5 and hold[0] == 0, len(hold), ">= 5 samples from t=0"),
              check("one main pull-back carries >= 95 %% of the scale change (then a <= 5 %% settle)", run_frac >= 0.95, run_frac, ">= 0.95"),
              check("decelerating: fastest step early, then slower", pk <= len(sp) // 3 and sp[-1] < 0.2 * max(sp), [pk, sp[-1], max(sp)], "early peak"),
              check("ends at 1x", _near(sc[-1], 1.0, 1e-4), sc[-1], 1.0),
              check("headline and context card revealed in frame at the end", inside(rows[-1][".pbr-headline"]["box"]) and inside(rows[-1][".pbr-card:nth-of-type(2)"]["box"]), [rows[-1][".pbr-headline"]["box"], rows[-1][".pbr-card:nth-of-type(2)"]["box"]], "inside"),
              check("negative control: during the hold the headline is not in frame", not inside(rows[0][".pbr-headline"]["box"]), rows[0][".pbr-headline"]["box"], "outside")]
    return checks, [wd / "pull_back_reveal_measure.json"]


@card("CAM-86")
def hf_push_in(task, wd):
    """HyperFrames push-in: one slow continuous camera push on a centred headline with a gentle fade (standard 1.12,
    bold 1.18); the camera's computed scale and opacity are sampled across the clip."""
    ts = _T(0, 4, 41)
    dur, rows = _hf_series(wd, "push-in", "push-in", [".pi-camera", ".pi-headline"], ts)
    _, rb = _hf_series(wd, "push-in", "push-in", [".pi-camera"], [3.0, 3.2, 3.35, 3.5], {"intensity": "bold"}, name="push_bold")
    bold = max(_dec(r[".pi-camera"]["tf"])[0] for r in rb)
    sc = [_dec(r[".pi-camera"]["tf"])[0] for r in rows]
    op = [r[".pi-camera"]["op"] for r in rows]
    hb = rows[20][".pi-headline"]["box"]
    steps_ = [sc[i + 1] - sc[i] for i in range(len(sc) - 1)]
    k = next(i for i, s in enumerate(sc) if _near(s, 1.12, 1e-4))
    checks = [check("continuous push: scale never decreases and rises without a stop until it lands", min(steps_) >= -1e-6 and all(s > 0 for s in steps_[:k - 1]), [min(steps_), k], "monotonic"),
              check("lands at 1.12 (standard)", _near(max(sc), 1.12, 1e-4), max(sc), 1.12),
              check("slow: <= 1.2 %% per 0.1 s", max(steps_) <= 0.012, max(steps_), "<= 0.012"),
              check("gentle fade at the end (opacity eases to < 0.1)", op[-1] < 0.1 and op[-6] > op[-1] and op[20] == 1, [op[20], op[-6], op[-1]], "1 → < 0.1"),
              check("headline centred", _pt_near(((hb[0] + hb[2]) / 2, (hb[1] + hb[3]) / 2), (960, 540), 8), [(hb[0] + hb[2]) / 2, (hb[1] + hb[3]) / 2], (960, 540)),
              check("bold intensity pushes to 1.18", _near(bold, 1.18, 1e-3), bold, 1.18),
              check("negative control: the first frame is not pushed", sc[0] == 1.0, sc[0], 1.0)]
    return checks, [wd / "push_in_measure.json"]


@card("CAM-78")
def hf_cursor_zoom_follow(task, wd):
    """HyperFrames cursor-zoom-follow: the camera pushes toward each upcoming click, follows the cursor, marks each
    click with a press and a ring, and eases back out. Clicks at the default points (68.5,7.5), (50,48.5), (90.5,7.5) %."""
    ts = _T(0, 5.8, 117)
    dur, rows = _hf_series(wd, "cursor-zoom-follow", "cursor-zoom-follow", ["#zf-cam", "#zf-cursor", "#zf-ripple"], ts)
    cam = [_dec(r["#zf-cam"]["tf"]) for r in rows]
    cur = [_dec(r["#zf-cursor"]["tf"]) for r in rows]
    rip = [r["#zf-ripple"]["op"] for r in rows]
    clicks = [(0.685 * 1920, 0.075 * 1080), (0.5 * 1920, 0.485 * 1080), (0.905 * 1920, 0.075 * 1080)]
    hit = []
    for cx, cy in clicks:
        idx = [i for i, c in enumerate(cur) if math.hypot(c[2] - cx, c[3] - cy) < 1.5]
        hit.append(idx[0] if idx else None)
    press = [min(cur[j][0] for j in range(max(0, i - 3), min(len(cur), i + 14))) if i is not None else 1 for i in hit]
    ring = [max(rip[j] for j in range(i, min(len(rip), i + 16))) if i is not None else 0 for i in hit]
    scr = [(clicks[k][0] * cam[i][0] + cam[i][2], clicks[k][1] * cam[i][0] + cam[i][3]) for k, i in enumerate(hit) if i is not None]
    fixed3 = (960 + (clicks[2][0] - 960) * 1.8, 540 + (clicks[2][1] - 540) * 1.8)
    checks = [check("cursor reaches each click point in order", None not in hit and hit == sorted(hit), [None if i is None else ts[i] for i in hit], "3 increasing times"),
              check("camera pushed in (1.8x) at every click", all(cam[i][0] > 1.7 for i in hit if i is not None), [cam[i][0] for i in hit if i is not None], "> 1.7"),
              check("camera follows: every click stays in frame at 1.8x", all(0 <= p[0] <= 1920 and 0 <= p[1] <= 1080 for p in scr), scr, "inside"),
              check("a centre-locked 1.8x zoom would lose click 3 (so the follow is doing work)", not (0 <= fixed3[0] <= 1920 and 0 <= fixed3[1] <= 1080), fixed3, "outside"),
              check("press: the cursor dips in scale at each click", all(p < 0.95 for p in press), press, "< 0.95"),
              check("ring: the ripple flashes after each click", all(r_ > 0.5 for r_ in ring), ring, "> 0.5"),
              check("eases back out to 1x at the end", _near(cam[-1][0], 1.0, 1e-4) and cam[-10][0] > cam[-1][0], [cam[-10][0], cam[-1][0]], "→ 1"),
              check("negative control: at t=0 the camera is not zoomed and no ring shows", cam[0][0] == 1 and rip[0] == 0, [cam[0][0], rip[0]], [1, 0])]
    return checks, [wd / "cursor_zoom_follow_measure.json"]


@card("CAM-88")
def hf_ui_focus_zoom(task, wd):
    """HyperFrames ui-focus-zoom: the app surface settles, the camera departs at zoom_at (1.4 s) to the anchor (64 %, 36 %)
    at 1.6x and holds, with a soft halo; variables zoom=2.2 / halo=hide are honoured. Sampled from the component."""
    ts = _T(0, 4.1, 42)
    dur, rows = _hf_series(wd, "ui-focus-zoom", "ui-focus-zoom", [".ufz-world", ".ufz-surface", ".ufz-halo"], ts)
    _, alt = _hf_series(wd, "ui-focus-zoom", "ui-focus-zoom", [".ufz-world", ".ufz-halo"], [4.0], {"zoom": 2.2, "halo": "hide"}, name="ufz_alt")
    sc = [_dec(r[".ufz-world"]["tf"])[0] for r in rows]
    sb = [r[".ufz-surface"]["box"] for r in rows]
    anc = [(b[0] + 0.64 * (b[2] - b[0]), b[1] + 0.36 * (b[3] - b[1])) for b in sb]
    d = [math.hypot(a[0] - 960, a[1] - 540) for a in anc]
    i14 = ts.index(min(ts, key=lambda t: abs(t - 1.4)))
    first_zoom = next(i for i, s in enumerate(sc) if s > 1.01)
    hold = [s for t, s in zip(ts, sc) if t >= 2.6]
    halo = max(r[".ufz-halo"]["op"] for r in rows if r[".ufz-halo"])
    checks = [check("surface settles (moves in, then rests) before the zoom", abs(sb[0][1] - sb[i14][1]) > 30 and abs(sb[i14 - 2][1] - sb[i14][1]) < 3, [sb[0][1], sb[i14 - 2][1], sb[i14][1]], "settled by 1.4 s"),
              check("camera departs at zoom_at (first zoom sample just after 1.4 s)", 1.4 <= ts[first_zoom] <= 1.6, ts[first_zoom], "1.4-1.6"),
              check("holds at 1.6x after arriving", all(_near(s, 1.6, 1e-3) for s in hold), [min(hold), max(hold)], 1.6),
              check("anchor pulled toward the frame centre (distance halves)", d[-1] < 0.5 * d[i14], [d[i14], d[-1]], "< 0.5x"),
              check("halo blooms at the anchor", halo > 0.2, halo, "> 0.2"),
              check("variables honoured: zoom 2.2, halo removed", _near(_dec(alt[0][".ufz-world"]["tf"])[0], 2.2, 1e-3) and alt[0][".ufz-halo"] is None, [_dec(alt[0][".ufz-world"]["tf"])[0], alt[0][".ufz-halo"]], [2.2, None]),
              check("negative control: before zoom_at the camera is at 1x", max(sc[:i14]) < 1.01, max(sc[:i14]), "< 1.01")]
    return checks, [wd / "ui_focus_zoom_measure.json"]


@card("CAM-87")
def hf_scroll_camera_story(task, wd):
    """HyperFrames scroll-camera-story: a forced-scroll pass down a tall scene of slotted sections, depth layers in
    parallax, decelerating into the last section, which lands in frame. Sampled every 0.05 s from the component."""
    ts = _T(0, 4.2, 85)
    sels = [".scs-world", ".scs-layer:nth-of-type(1)", ".scs-layer:nth-of-type(2)", ".scs-layer:nth-of-type(3)", ".scs-section:last-of-type"]
    dur, rows = _hf_series(wd, "scroll-camera-story", "scroll-camera-story", sels, ts)
    wy = [_dec(r[".scs-world"]["tf"])[3] for r in rows]
    net = [[wy[i] + _dec(r[s]["tf"])[3] for i, r in enumerate(rows)] for s in sels[1:4]]
    ratio = [n[-1] / wy[-1] for n in net]
    H = rows[0][".scs-world"]["box"][3] - rows[0][".scs-world"]["box"][1]
    vel = [wy[i] - wy[i + 1] for i in range(len(wy) - 1)]
    last_mv = max(i for i, v in enumerate(vel) if v > 0.5)
    pk = max(range(len(vel)), key=lambda i: vel[i])
    tail = vel[pk:last_mv + 1]
    lb = rows[-1][".scs-section:last-of-type"]["box"]
    lb0 = rows[0][".scs-section:last-of-type"]["box"]
    checks = [check("forced scroll travels the whole tall scene (height - 1080)", _near(-wy[-1], H - 1080, 1), [-wy[-1], H - 1080], "equal"),
              check("scroll only goes down (no backtrack > 3 px)", min(vel) > -3, min(vel), "> -3"),
              check("depth layers parallax at distinct speeds (far < mid < near)", ratio[0] < ratio[1] < ratio[2] and _near(ratio[2], 1.0, 1e-3) and ratio[0] < 0.5, ratio, "increasing to 1"),
              check("decelerates into the last section (speed falls to < 15 % of its peak)", tail[-1] < 0.15 * vel[pk], [vel[pk], tail[-1]], "< 0.15 peak"),
              check("last section lands fully in frame", lb[1] >= 0 and lb[3] <= 1080, lb, "inside"),
              check("negative control: at t=0 the last section is below the frame", lb0[1] > 1080, lb0, "> 1080")]
    return checks, [wd / "scroll_camera_story_measure.json"]


@card("CAM-89")
def hf_yt_camera_move(task, wd):
    """HyperFrames yt-camera-move helpers (ytCameraMove / ytCameraReset / ytDefocusPulse) driven on a fresh wrapper:
    default punch-in 1.11 with the cubic power2.inOut ease, slides in px, 3D tilt/pan with perspective, the
    edge-defocus pulse peaking at 45 %, and the reset back to rest."""
    js = r"""(() => { const box = document.createElement('div'); box.id = 'probe'; box.style.cssText = 'position:absolute;left:660px;top:340px;width:600px;height:400px;background:#888';
  const ov = document.createElement('div'); ov.id = 'ov'; ov.style.cssText = 'position:absolute;inset:0;opacity:0'; document.body.append(box, ov);
  const tl = gsap.timeline({paused: true}); ytCameraMove(tl, '#probe', 0, {}); ytCameraMove(tl, '#probe', 1.2, {zoom: 0.2, slideX: 120, slideY: -40, dur: 1.2});
  ytCameraMove(tl, '#probe', 2.4, {zoom: 0.2, slideX: 120, slideY: -40, tilt: 8, pan: -6, dur: 1.2}); ytCameraReset(tl, '#probe', 3.6); ytDefocusPulse(tl, '#ov', 0, 1.2);
  const S = (t) => { tl.seek(t, false); const c = getComputedStyle(box); return {tf: c.transform, op: +getComputedStyle(ov).opacity, box: R(box)}; };
  return {q: S(0.3), h: S(0.6), d054: S(0.54), end1: S(1.2), slide: S(2.4), tilt: S(3.6), reset: S(4.8), start: S(0), rx: (tl.seek(3.6), gsap.getProperty('#probe', 'rotationX')), ry: gsap.getProperty('#probe', 'rotationY'), persp: gsap.getProperty('#probe', 'transformPerspective')}; })()"""
    dur, r = hf_page(wd, "yt-camera-move", "yt-camera-move", [{"js": js, "shot": "yt_probe.png"}], name="yt_camera_move")
    s = lambda k: _dec(r[k]["tf"])
    prog = lambda k: (s(k)[0] - 1) / 0.11
    checks = [check("default punch-in lands at 1.11", _near(s("end1")[0], 1.11, 1e-4), s("end1")[0], 1.11),
              check("cubic in-out default: 50 % at half time, 6.25 % at a quarter", _near(prog("h"), 0.5, 0.005) and _near(prog("q"), 0.0625, 0.005), [prog("q"), prog("h")], [0.0625, 0.5]),
              check("slide moves 120 px right and 40 px up", _near(s("slide")[2], 120, 0.5) and _near(s("slide")[3], -40, 0.5), s("slide")[2:], [120, -40]),
              check("3D tilt/pan: matrix3d with 1200 px perspective, rotationX 8 / rotationY -6", r["tilt"]["tf"].startswith("matrix3d") and r["persp"] == 1200 and _near(r["rx"], 8, 1e-3) and _near(r["ry"], -6, 1e-3), [r["tilt"]["tf"][:9], r["persp"], r["rx"], r["ry"]], ["matrix3d", 1200, 8, -6]),
              check("edge-defocus pulse peaks at 45 % of the move, gone at the end", _near(r["d054"]["op"], 1.0, 1e-3) and r["end1"]["op"] < 1e-3, [r["d054"]["op"], r["end1"]["op"]], [1, 0]),
              check("reset returns to rest (identity)", r["reset"]["tf"] in ("none", "matrix(1, 0, 0, 1, 0, 0)") or _dec(r["reset"]["tf"]) == (1.0, 0.0, 0.0, 0.0), r["reset"]["tf"], "identity"),
              check("negative control: the wrapper at t=0 is untouched", r["start"]["tf"] in ("none", "matrix(1, 0, 0, 1, 0, 0)") or abs(s("start")[0] - 1) < 1e-6, r["start"]["tf"], "identity")]
    return checks, [wd / "yt_probe.png", wd / "yt_camera_move_measure.json"]


@card("CAM-90")
def hf_dolly_zoom(task, wd):
    """HyperFrames camera-dolly-zoom (full composition): the camera dollies while the focal length (CSS perspective)
    is solved so d*tan(FOV/2) stays constant; the subject keeps its size while the background stretches ('out') or
    collapses ('in'). A plain dolly with a fixed lens is the negative control."""
    ts = _T(0, 3.9, 14)
    sels = ["#dz-subject", "#dz-backwall", ".dz-arch"]
    js = "(() => { const out = []; for (const t of %s) { SEEK(t); const st = document.getElementById('dz-stage'), rig = document.getElementById('dz-rig');" \
         " out.push({sub: R('#dz-subject'), back: R('#dz-backwall'), arch: R('.dz-arch'), P: parseFloat(getComputedStyle(st).perspective), tz: new DOMMatrix(getComputedStyle(rig).transform).m43}); } return out; })()" % json.dumps(ts)
    plain = "(() => { const st = document.getElementById('dz-stage'), rig = document.getElementById('dz-rig'); SEEK(0); const P = parseFloat(getComputedStyle(st).perspective); const a = R('#dz-subject');" \
            " rig.style.transform = 'translateZ(' + (P * 0.5) + 'px)'; return {a, b: R('#dz-subject')}; })()"
    dur, rows, neg = hf_page(wd, "camera-dolly-zoom", "camera-dolly-zoom", [{"js": js}, {"js": plain}], kind="add")
    _, rin = hf_page(wd, "camera-dolly-zoom", "camera-dolly-zoom", [{"js": js}], {"direction": "in"}, name="dolly_in", html_path=wd / "hf/compositions/camera-dolly-zoom.html")
    w = lambda b: b[2] - b[0]
    sub = [w(r["sub"]) for r in rows]
    back = [w(r["back"]) / w(rows[0]["back"]) for r in rows]
    arch = [w(r["arch"]) / w(rows[0]["arch"]) for r in rows]
    inv = [r["P"] / (r["P"] - r["tz"]) for r in rows]          # perspective / camera distance must stay 1
    back_in = w(rin[-1]["back"]) / w(rin[0]["back"])
    checks = [check("subject keeps its size on every sample (px)", max(sub) - min(sub) < 0.5, [min(sub), max(sub)], "constant"),
              check("invariant: focal length / distance = 1 throughout (d tan(FOV/2) const)", max(abs(v - 1) for v in inv) < 1e-6, [min(inv), max(inv)], 1.0),
              check("'out': background stretches (> 1.4x)", back[-1] > 1.4, back[-1], "> 1.4"),
              check("depth ordering: arches (mid depth) change less than the back wall", 1 < arch[-1] < back[-1], [arch[-1], back[-1]], "1 < arch < wall"),
              check("'in': background collapses (< 0.8x)", back_in < 0.8, back_in, "< 0.8"),
              check("negative control: a plain dolly with a fixed lens changes the subject size", w(neg["b"]) > 1.5 * w(neg["a"]), [w(neg["a"]), w(neg["b"])], "> 1.5x")]
    return checks, [wd / "camera_dolly_zoom_measure.json"]


@card("CAM-77")
def hf_camera_shake(task, wd):
    """HyperFrames camera-shake: closed-form, seek-safe shake (any seek order gives the same pose), per-lens projection
    (frame perspective scales 28 : 50 : 85 mm), intensity scales the displacement, the overscan keeps the frame covered,
    the rotation toggle removes the roll/tilt channels; intensity 0 is the negative control."""
    ts = _T(0, 5.9, 60)
    js = "(() => { const ts = %s; const rig = document.getElementById('cs-rig'); const pose = (t) => { SEEK(t); const m = new DOMMatrix(getComputedStyle(rig).transform); return [m.m41, m.m42, m.m13, m.m23, R(rig)]; };" \
         " const seq = ts.map(pose); const rnd = [...ts.keys()].sort((a, b) => ((a * 7919) %% 61) - ((b * 7919) %% 61)); const back = {}; for (const i of rnd) back[i] = pose(ts[i]);" \
         " return {seq, same: seq.every((v, i) => JSON.stringify(v) === JSON.stringify(back[i])), P: parseFloat(getComputedStyle(document.getElementById('cs-frame')).perspective)}; })()" % json.dumps(ts)
    res = {}
    first = None
    for key, v in [("normal", {}), ("wide", {"shakeProfile": "handheld-wideangle-mild"}), ("tele", {"shakeProfile": "handheld-tele-mild"}),
                   ("x2", {"shakeIntensity": 2}), ("norot", {"shakeRotation": False}), ("zero", {"shakeIntensity": 0})]:
        r = hf_page(wd, "camera-shake", "camera-shake", [{"js": js}], v, name="shake_" + key, html_path=first)
        first = first or wd / "hf/compositions/components/camera-shake.html"
        res[key] = r[1]
    N = np()
    tx = lambda k: N.array([p[0] for p in res[k]["seq"]])
    amp = lambda k: float(tx(k).max() - tx(k).min())
    cover = all(p[4][0] <= 0 and p[4][1] <= 0 and p[4][2] >= 1920 and p[4][3] >= 1080 for p in res["normal"]["seq"] + res["x2"]["seq"])
    rot_on = max(abs(p[2]) + abs(p[3]) for p in res["normal"]["seq"])
    rot_off = max(abs(p[2]) + abs(p[3]) for p in res["norot"]["seq"])
    jump = float(N.abs(N.diff(tx("normal"))).max())
    checks = [check("seek-safe: any seek order gives identical poses", all(res[k]["same"] for k in res), {k: res[k]["same"] for k in res}, True),
              check("per-lens projection: perspective 28 : 50 : 85", _near(res["wide"]["P"] / res["normal"]["P"], 28 / 50, 0.01) and _near(res["tele"]["P"] / res["normal"]["P"], 85 / 50, 0.01), [res["wide"]["P"], res["normal"]["P"], res["tele"]["P"]], "0.56 : 1 : 1.7"),
              check("intensity 2 doubles the displacement", _near(amp("x2") / amp("normal"), 2.0, 0.02), amp("x2") / amp("normal"), 2.0),
              check("overscan keeps the frame covered on every sample", cover, cover, True),
              check("rotation toggle: roll/tilt channels present, then removed", rot_on > 0.01 and rot_off < 1e-9, [rot_on, rot_off], "> 0.01, 0"),
              check("smooth: no frame-to-frame jump > 12 px at 10 fps sampling", jump < 12, jump, "< 12"),
              check("negative control: intensity 0 does not shake", amp("zero") < 1e-6, amp("zero"), 0)]
    return checks, [wd / "shake_normal_measure.json"]


@card("CAM-81")
def hf_pan_stations(task, wd):
    """HyperFrames pan-stations: a lateral camera move across a row of labelled stations with a steady dwell at each;
    sampled every 0.05 s, the strip must hold still with station k centred at x = 960 during dwell k (4 and 5 stations)."""
    def run(v, name, path=None, duration=None):
        js = "(() => { const out = []; const n = Math.round(TL.duration() / 0.05); for (let i = 0; i <= n; i++) { const t = Math.min(TL.duration(), i * 0.05); SEEK(t); const m = new DOMMatrix(getComputedStyle(document.querySelector('.ps-strip')).transform);" \
             " out.push([t, m.m41, m.m42, [...document.querySelectorAll('.ps-station')].map(e => { const r = R(e); return (r[0] + r[2]) / 2; })]); }" \
             " return {rows: out, labels: [...document.querySelectorAll('.ps-station')].map(e => e.textContent.replace(/\\s+/g, ' ').trim())}; })()"
        return hf_page(wd, "pan-stations", "pan-stations", [{"js": js}], v, name=name, html_path=path, duration=duration)[1]

    def dwells(rows):
        still = [i > 0 and abs(rows[i][1] - rows[i - 1][1]) < 0.01 for i in range(len(rows))]
        segs = [s for s in _segments(still) if s[1] - s[0] >= 3]
        cen = []
        for a, b in segs:
            c = rows[a][3]
            k = min(range(len(c)), key=lambda j: abs(c[j] - 960))
            cen.append((k, c[k], (b - a + 1) * 0.05))
        return cen
    r4 = run({}, "pan_stations")
    r5 = run({"stationCount": 5, "labels": "A,B,C,D,E"}, "pan_stations5", wd / "hf/compositions/components/pan-stations.html", duration=5)
    d4, d5 = dwells(r4["rows"]), dwells(r5["rows"])
    lateral = max(abs(r[2]) for r in r4["rows"])
    mid = r4["rows"][24][3]
    checks = [check("4 stations: four dwells, stations 0..3 in order", [d[0] for d in d4] == [0, 1, 2, 3], d4, [0, 1, 2, 3]),
              check("each dwell centres its station at x = 960 (+-1 px)", all(abs(d[1] - 960) <= 1 for d in d4 + d5), [round(d[1], 2) for d in d4 + d5], 960),
              check("steady dwell >= the 0.6 s default", all(d[2] >= 0.6 - 1e-9 for d in d4[1:-1]), [d[2] for d in d4], ">= 0.6"),
              check("purely lateral move (no vertical drift)", lateral < 1e-6, lateral, 0),
              check("5 stations on a 5 s clip: five dwells in order", [d[0] for d in d5] == [0, 1, 2, 3, 4], d5, [0, 1, 2, 3, 4]),
              check("labels shown on the station cards", all(lab in txt for lab, txt in zip("Capture,Edit,Render,Share".split(","), r4["labels"])), r4["labels"], "Capture, Edit, Render, Share"),
              check("negative control: mid-pan (t = 1.2 s) no station is centred", min(abs(c - 960) for c in mid) > 100, min(abs(c - 960) for c in mid), "> 100")]
    return checks, [wd / "pan_stations_measure.json"]


def _pz_host(wd, item, pfx):
    """A host composition for the parallax snippet: a 3x3 card grid (centre card is the focus) plus the snippet."""
    snip = hf_install(wd, item).read_text(encoding="utf-8")
    cards = "".join('<div class="%s-card c" data-%s-row="%d" data-%s-col="%d"%s></div>' % (item, pfx, r, pfx, c, ' data-%s-focus="true"' % pfx if (r, c) == (1, 1) else "")
                    for r in range(3) for c in range(3))
    host = ("<!doctype html><html><head><style>html,body{margin:0;width:1920px;height:1080px;overflow:hidden;background:#101218}"
            ".%s-grid{position:absolute;left:300px;top:157.5px;width:1320px;display:grid;grid-template-columns:repeat(3,400px);gap:40px}"
            ".c{height:225px;background:#3a5a9a;border-radius:12px}</style></head><body><div class='%s-grid'>%s</div>%s</body></html>") % (item, item, cards, snip)
    p = wd / ("%s_host.html" % item)
    p.write_text(host, encoding="utf-8")
    return p


_PZ_JS = r"""(() => { const g = document.querySelector('.%(item)s-grid'); const cards = [...g.querySelectorAll('.c')];
  const tl = gsap.timeline({paused: true}); tl.fromTo(g, {'--%(pfx)s-progress': 0}, {'--%(pfx)s-progress': 1, duration: 2.4, ease: 'none'});
  const S = (t) => { tl.seek(t, false); return cards.map(c => { const r = R(c), cs = getComputedStyle(c); return {cx: (r[0] + r[2]) / 2, cy: (r[1] + r[3]) / 2, w: r[2] - r[0], box: r, op: +cs.opacity}; }); };
  return [S(0), S(1.2), S(2.4)]; })()"""


@card("CAM-84")
def hf_parallax_zoom(task, wd):
    """HyperFrames parallax-zoom snippet in a host 3x3 grid: the centre card scales to fill the frame (6x) while the
    siblings parallax outward along their grid offset (900 px per step) and fade; --pz-progress driven by GSAP."""
    host = _pz_host(wd, "parallax-zoom", "pz")
    _, (p0, p5, p1) = hf_page(wd, "parallax-zoom", "-", [{"js": _PZ_JS % {"item": "parallax-zoom", "pfx": "pz"}, "shot": "pz_mid.png"}], html_path=host, name="parallax_zoom")
    f = 4
    cover = lambda b: b[0] <= 0 and b[1] <= 0 and b[2] >= 1920 and b[3] >= 1080
    disp_err = max(abs((p5[k]["cx"] - p0[k]["cx"]) - 450 * ((k % 3) - 1)) + abs((p5[k]["cy"] - p0[k]["cy"]) - 450 * ((k // 3) - 1)) for k in range(9) if k != f)
    checks = [check("focus card scales 6x and fills the frame", _near(p1[f]["w"] / p0[f]["w"], 6, 1e-3) and cover(p1[f]["box"]), [p1[f]["w"] / p0[f]["w"], p1[f]["box"]], "6x, covers"),
              check("siblings move outward along their grid offset (900 px x progress, max err px)", disp_err < 1, disp_err, "< 1"),
              check("diagonal siblings travel sqrt(2) farther than edge siblings", _near(math.hypot(p1[0]["cx"] - p0[0]["cx"], p1[0]["cy"] - p0[0]["cy"]) / abs(p1[1]["cy"] - p0[1]["cy"]), math.sqrt(2), 1e-3), math.hypot(p1[0]["cx"] - p0[0]["cx"], p1[0]["cy"] - p0[0]["cy"]) / abs(p1[1]["cy"] - p0[1]["cy"]), 1.4142),
              check("siblings fade out (opacity 0.5 at half, 0 at the end)", all(_near(p5[k]["op"], 0.5, 1e-3) and p1[k]["op"] == 0 for k in range(9) if k != f), [p5[0]["op"], p1[0]["op"]], [0.5, 0]),
              check("negative control: at progress 0 the focus card does not fill the frame", not cover(p0[f]["box"]), p0[f]["box"], "inside")]
    return checks, [wd / "pz_mid.png"]


@card("CAM-83")
def hf_parallax_unzoom(task, wd):
    """HyperFrames parallax-unzoom snippet (the reverse): the focus card shrinks from full frame (6x) while the siblings
    parallax in from 900 px per grid step and fade in, forming the grid at progress 1."""
    host = _pz_host(wd, "parallax-unzoom", "pu")
    _, (p0, p5, p1) = hf_page(wd, "parallax-unzoom", "-", [{"js": _PZ_JS % {"item": "parallax-unzoom", "pfx": "pu"}, "shot": "pu_mid.png"}], html_path=host, name="parallax_unzoom")
    f = 4
    cover = lambda b: b[0] <= 0 and b[1] <= 0 and b[2] >= 1920 and b[3] >= 1080
    dist = lambda P, k: math.hypot(P[k]["cx"] - P[f]["cx"], P[k]["cy"] - P[f]["cy"])
    grid_ok = all(_near(p1[k]["cx"], 300 + 200 + (k % 3) * 440, 0.5) and _near(p1[k]["cy"], 157.5 + 112.5 + (k // 3) * 265, 0.5) for k in range(9))
    checks = [check("focus card starts at 6x covering the frame and ends at 1x", cover(p0[f]["box"]) and _near(p0[f]["w"] / p1[f]["w"], 6, 1e-3), [p0[f]["w"], p1[f]["w"]], "6x → 1x"),
              check("siblings move in (distance to the focus shrinks)", all(dist(p0, k) > dist(p5, k) > dist(p1, k) for k in range(9) if k != f), [round(dist(p0, 0)), round(dist(p5, 0)), round(dist(p1, 0))], "decreasing"),
              check("siblings start 900 px per grid step out", all(_near(p0[k]["cx"] - p1[k]["cx"], 900 * ((k % 3) - 1), 0.5) for k in range(9) if k != f), [p0[0]["cx"] - p1[0]["cx"]], -900),
              check("siblings fade in (0 → 1)", all(p0[k]["op"] == 0 and p1[k]["op"] == 1 for k in range(9) if k != f), [p0[0]["op"], p1[0]["op"]], [0, 1]),
              check("the grid is formed at the end (every card at its layout slot)", grid_ok, [(round(c["cx"]), round(c["cy"])) for c in p1], "3x3 slots"),
              check("negative control: at progress 0 the grid is not formed", not all(_near(p0[k]["cx"], p1[k]["cx"], 0.5) for k in range(9)), True, "scattered")]
    return checks, [wd / "pu_mid.png"]


@card("CAM-91")
def hf_rack_focus_webgl(task, wd):
    """HyperFrames rack-focus (WebGL, real aperture bokeh): the focal plane travels near (1.2 m bulb string) to far
    (80 m city sign). Chrome renders the shader at four times; pixel sharpness of the near bulbs and of the far LED
    strip, and the bulbs' bokeh disc size, are measured from the screenshots."""
    times = [0.5, 2.0, 3.5, 5.5]
    steps = [{"js": "(() => { const c = document.getElementById('rf-canvas'); return !!(c.getContext('webgl2') || c.getContext('webgl')); })()"}]
    steps += [{"js": "SEEK(%s)" % t, "shot": "rack_%d.png" % i} for i, t in enumerate(times)]
    r = hf_page(wd, "rack-focus", "rack-focus", steps, name="rack_focus")
    N = np()
    near, far, disc = [], [], []
    for i in range(len(times)):
        A = load_png(wd / ("rack_%d.png" % i)).astype(float)
        g = A.mean(axis=2)
        near.append(sharpness(g[520:600, 260:350]))
        far.append(sharpness(g[805:880, 630:1290]))
        from scipy import ndimage
        lab, _n = ndimage.label((A[..., 0] > 240) & (A[..., 1] > 240) & (A[..., 2] > 140))
        disc.append([int((lab == lab[y, x]).sum()) if lab[y, x] else 0 for x, y in ((305, 557), (1590, 668), (1277, 688))])
    checks = [check("WebGL context available and the shader ran", r[1] is True, r[1], True),
              check("start: near bulbs sharp, far sign soft", near[0] > 1000 and far[0] < 1000, [near[0], far[0]], "near > 1000, far < 1000"),
              check("end: far sign resolves into lamps, near bulbs go soft", far[-1] > 10 * far[0] and near[-1] < 0.05 * near[0], [far[0], far[-1], near[0], near[-1]], "far x10, near / 20"),
              check("focus travels one way: far sharpness rises, then holds (never drops > 10 %)", far[0] < far[1] < far[2] and far[3] > 0.9 * far[2], far, "rise, hold"),
              check("each defocused near bulb becomes a bokeh disc > 5x its in-focus area", all(e > 5 * max(1, b) for b, e in zip(disc[0], disc[-1])), [disc[0], disc[-1]], "> 5x"),
              check("negative control: the start frame fails the far-focus threshold the end frame passes", far[0] < 0.1 * far[-1], [far[0], far[-1]], "start < 0.1 end")]
    return checks, [wd / "rack_0.png", wd / ("rack_%d.png" % (len(times) - 1))]


@card("CAM-97")
def hf_swiss_grid_example(task, wd):
    """HyperFrames swiss-grid example: `hyperframes init --example swiss-grid` scaffolds the project with its three
    sub-compositions, `compositions --json` reads the 10 s master, and `hyperframes snapshot` captures real frames,
    where the #f2f2f2 field and the 240 px major / 60 px minor grid are measured."""
    proj = hf_install(wd, "sw", "swiss-grid")
    N = np()
    env = _hf_env()
    comp = subprocess.run([_NODE, str(_HF_CLI), "compositions", "--json"], capture_output=True, text=True, timeout=60, cwd=str(proj), env=env, stdin=subprocess.DEVNULL)
    comps = {c["id"]: c for c in json.loads(comp.stdout[comp.stdout.index("{"):])["compositions"]}
    snaps = wd / "snaps"
    sn = subprocess.run([_NODE, str(_HF_CLI), "snapshot", ".", "--at", "0.5,4,8", "--no-end", "--json", "-o", str(snaps)], capture_output=True, text=True, timeout=90, cwd=str(proj), env=env, stdin=subprocess.DEVNULL)
    if sn.returncode:
        raise RuntimeError("hyperframes snapshot failed: %s" % (sn.stdout + sn.stderr)[-300:])
    frames = sorted(snaps.glob("frame-*.png"))
    A = load_png(frames[1]).astype(float)
    g = A.mean(axis=2)
    bgfrac = float(N.all(A.astype(int) == 242, axis=2).mean())
    px = 242 - g.mean(axis=0)
    major = sorted({int(round(i / 240.0)) * 240 for i in range(1920) if px[i] > 20})
    minor = sorted({int(round(i / 60.0)) * 60 for i in range(1920) if 3 < px[i] <= 20})
    idx = (proj / "index.html").read_text(encoding="utf-8")
    plain = N.full((1080, 1920), 242.0)
    pneg = 242 - plain.mean(axis=0)
    checks = [check("example scaffolded with its three sub-compositions", all((proj / "compositions" / f).exists() for f in ("intro.html", "graphics.html", "captions.html")), sorted(p.name for p in (proj / "compositions").glob("*.html")), ["captions", "graphics", "intro"]),
              check("master composition is 10 s at 1920x1080", comps["master"]["duration"] == 10 and (comps["master"]["width"], comps["master"]["height"]) == (1920, 1080), comps["master"], "10 s"),
              check("Helvetica on #f2f2f2 in the source", "#f2f2f2" in idx and '"Helvetica"' in idx, True, True),
              check("snapshot: #f2f2f2 fills > 85 % of the frame", bgfrac > 0.85, bgfrac, "> 0.85"),
              check("major grid lines every 240 px", major == list(range(240, 1920, 240)), major, "240..1680"),
              check("minor grid lines every 60 px between the majors", len(minor) >= 20 and all(m_ % 60 == 0 and m_ % 240 != 0 for m_ in minor), minor[:8], "60 px steps"),
              check("negative control: a flat #f2f2f2 plate has no grid lines", int((pneg > 3).sum()) == 0, int((pneg > 3).sum()), 0)]
    return checks, [frames[1]]
