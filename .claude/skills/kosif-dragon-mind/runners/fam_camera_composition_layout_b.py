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

GAPS: dict = {}

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
    inp = write_video(wd / ("%s_input.mp4" % name), [warp(wimg, M, W, H) for M in imats], fps)
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
    sys.path.insert(0, str(Path(path).parent))
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
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
    flags = [False] + [float(np().abs(fo[i] - fo[i - 1]).mean()) > 0.05 for i in range(1, len(fo))]
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


def _push_card(wd, name, W, H, fps, scale_fn, n, tol=2.0, neg_k=2.5):
    mk, d0 = _push_world(W, H)
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
    checks, outs, d, sm, si, _ = _push_card(wd, "punch", 320, 180, 60, fn, 75)
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
    fps = 30
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
    checks, outs, d, mid = _offset_card(wd, "climax", 480, 270, fps, offs, scales, tol=2.0)
    sm = pair_scale(d, "red", "blue", 0.4 * 480)
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
