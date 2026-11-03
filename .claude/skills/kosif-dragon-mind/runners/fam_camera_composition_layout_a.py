"""camera-composition-layout (part A): method cards as real programs with known-answer checks.

Engines (all deterministic, all write only inside the work folder):
- dom2d: the repo's real motion-kit.js + vendored GSAP run in headless Chrome; every tracked element's four screen
  corners are read back from the browser per frame (zero-size corner probes, so CSS transforms, 3D perspective and
  transform origins are the browser's own math); the quads are painted into a lossless video and the markers are
  measured back from the decoded video against an independent Python model of the card's formula.
- cam3d: the repo's real three-kit.bundle.js (K3) / lab-kit.js in Chrome return camera pos/look/fov/roll per frame and
  THREE's own projection of world markers; the projected markers are painted into a video and measured.
- layout: HTML/CSS laid out by Chrome (rects + screenshot) or computed rules painted with PIL, measured from the PNG.
- hud / filters / ffmpeg / prompt engines for overlays, the KOSIF Studio scene ops (render.py), zoompan/crop
  expressions and prompt linters (video_prompt_forge.lint).
Every card also measures the unprocessed input (static clip, raw prompt, naive layout) and requires it to fail.
"""
from __future__ import annotations

import html as _html
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np

from _harness import card, check, fx

GAPS: dict = {}

REPO = Path(__file__).resolve().parents[4]
SKILLS = REPO / ".claude/skills/kosif-superpowers/vendor/100-superskills/skills"
MM = SKILLS / "kosif-montage-motion/scripts"
KIT = MM / "kit"
GSAP = KIT / "gsap.min.js"
MKIT = KIT / "motion-kit.js"
K3B = KIT / "three-kit.bundle.js"
LABKIT = KIT / "lab-kit.js"
SHAPEKIT = KIT / "shape-kit.js"
FORGE = SKILLS / "video-prompt-director/scripts"
CHROME = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")

# ───────────────────────────── shared helpers ─────────────────────────────


def _bez(x1, y1, x2, y2):
    """The motion-kit cubic-bezier solver ported 1:1 (8 Newton steps) for independent known answers."""
    A = lambda a, b: 1 - 3 * b + 3 * a
    B = lambda a, b: 3 * b - 6 * a
    C = lambda a: 3 * a
    calc = lambda t, a, b: ((A(a, b) * t + B(a, b)) * t + C(a)) * t
    slope = lambda t, a, b: 3 * A(a, b) * t * t + 2 * B(a, b) * t + C(a)

    def solve(x):
        t = x
        for _ in range(8):
            s = slope(t, x1, x2)
            if abs(s) < 1e-6:
                break
            t -= (calc(t, x1, x2) - x) / s
        return min(1, max(0, t))
    return lambda p: 0.0 if p <= 0 else 1.0 if p >= 1 else calc(solve(p), y1, y2)


EZ = {"cam": _bez(.48, .1, 0, .9), "dolly": _bez(.35, 0, .65, 1), "out": _bez(.16, 1, .3, 1),
      "smooth": _bez(.65, 0, .35, 1), "rest": _bez(.45, 0, .1, 1), "inOut": _bez(.87, 0, .13, 1),
      "linear": lambda p: p}
smoothstep = lambda x: (lambda t: t * t * (3 - 2 * t))(min(1.0, max(0.0, x)))
cubic_io = lambda x: 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
sine_io = lambda x: -(math.cos(math.pi * x) - 1) / 2


def log_push(a, b, p, ez):
    return math.exp(math.log(a) + ez(p) * (math.log(b) - math.log(a)))


def chrome_run(wd: Path, name: str, html: str, size=(320, 180), screenshot=False, budget=2000, gl=False):
    """Run a page in headless Chrome; return the JSON the page wrote into #OUT (and the screenshot path)."""
    if not CHROME:
        raise RuntimeError("google-chrome not found")
    page = wd / ("%s.html" % name)
    page.write_text(html, encoding="utf-8")
    base = [CHROME, "--headless=new", "--no-sandbox", *(["--use-angle=swiftshader", "--enable-unsafe-swiftshader"] if gl else ["--disable-gpu"]),
            "--hide-scrollbars", "--no-first-run",
            "--disable-extensions", "--allow-file-access-from-files", "--window-size=%d,%d" % size,
            "--virtual-time-budget=%d" % budget]
    done = subprocess.run(base + ["--dump-dom", page.as_uri()], capture_output=True, text=True, timeout=40,
                          stdin=subprocess.DEVNULL)
    m = re.search(r'<pre id="OUT">(.*?)</pre>', done.stdout, re.S)
    if not m:
        raise RuntimeError("page produced no #OUT: " + done.stderr[-300:])
    if not m.group(1).strip():
        raise RuntimeError("page script did not run (syntax error?)")
    out = json.loads(_html.unescape(m.group(1)))
    if isinstance(out, dict) and out.get("__error"):
        raise RuntimeError("page error: " + out["__error"])
    shot = None
    if screenshot:
        shot = wd / ("%s.png" % name)
        subprocess.run(base + ["--screenshot=%s" % shot, page.as_uri()], capture_output=True, timeout=40,
                       stdin=subprocess.DEVNULL)
        if not shot.exists():
            raise RuntimeError("screenshot failed")
    return out, shot


def page(body: str, js: str, scripts=(), W=320, H=180, css="") -> str:
    tags = "".join('<script src="%s"></script>' % Path(s).as_uri() for s in scripts)
    return ("<!doctype html><html><head><meta charset=utf-8><style>html,body{margin:0;padding:0;overflow:hidden;"
            "background:#000}#view{position:relative;width:%dpx;height:%dpx;overflow:hidden;background:#777}"
            ".a{position:absolute}%s</style>%s</head><body><div id=view>%s</div><pre id=\"OUT\"></pre><script>"
            "try{%s}catch(e){document.getElementById('OUT').textContent=JSON.stringify({__error:String(e)+' '+(e.stack||'')})}"
            "</script></body></html>") % (W, H, css, tags, body, js)


DOM_SAMPLER = r"""
function __probe(el){ if(el.__pr) return el.__pr; const ps=[[0,0],[1,0],[1,1],[0,1]].map(([u,v])=>{const d=document.createElement('i');
  d.style.cssText='position:absolute;left:'+u*100+'%;top:'+v*100+'%;width:0;height:0;padding:0;margin:0;border:0;display:block';
  el.appendChild(d); return d;}); el.__pr=ps; return ps; }
function __quad(el){ if(el instanceof SVGElement){const r=el.getBoundingClientRect(); return [[r.left,r.top],[r.right,r.top],[r.right,r.bottom],[r.left,r.bottom]];}
  return __probe(el).map(d=>{const r=d.getBoundingClientRect(); return [r.left, r.top];}); }
function __op(el){ let o=1; for(let e=el; e && e.nodeType===1; e=e.parentElement){ o*=parseFloat(getComputedStyle(e).opacity); } return o; }
function __blur(el){ let b=0; for(let e=el; e && e.nodeType===1; e=e.parentElement){ const m=/blur\(([\d.]+)px\)/.exec(getComputedStyle(e).filter||''); if(m) b+=parseFloat(m[1]); } return b; }
function SAMPLE(times, sels, extra){ const els=sels.map(s=>document.querySelector(s)); els.forEach(e=>{ if(!(e instanceof SVGElement)) __probe(e); }); const fr=[];
  for(const t of times){ if(window.camAt) camAt(t); else tl.seek(t,false);
    fr.push({t, el: els.map(e=>({q:__quad(e), o:__op(e), b:__blur(e)})), x: extra?extra(t):null}); }
  return fr; }
function OUT(v){ document.getElementById('OUT').textContent = JSON.stringify(v); }
"""


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def paint_frames(frames, colors, W, H, bg=(119, 119, 119), ss=4):
    """Paint the browser's quads (with opacity and blur) into RGB frames, supersampled ss x ss (antialiased)."""
    from PIL import Image, ImageDraw, ImageFilter
    out = []
    for fr in frames:
        im = Image.new("RGB", (W * ss, H * ss), bg)
        for e, col in zip(fr["el"], colors):
            if col is None or e["o"] <= 0.003:
                continue
            pad = int(e["b"] * 2 * ss) + 2
            xs = [p[0] * ss for p in e["q"]]
            ys = [p[1] * ss for p in e["q"]]
            x0, y0 = max(0, int(min(xs)) - pad), max(0, int(min(ys)) - pad)
            x1, y1 = min(W * ss, int(max(xs)) + pad + 1), min(H * ss, int(max(ys)) + pad + 1)
            if x1 <= x0 or y1 <= y0:
                continue
            layer = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
            ImageDraw.Draw(layer).polygon([(x - x0, y - y0) for x, y in zip(xs, ys)],
                                          fill=tuple(col) + (int(round(255 * min(1, e["o"]))),))
            if e["b"] > 0.3:
                layer = layer.filter(ImageFilter.GaussianBlur(e["b"] / 2.0 * ss))
            im.paste(layer, (x0, y0), layer)
        out.append(np.asarray(im.resize((W, H), Image.BOX)))
    return out


def write_video(path: Path, frames, fps):
    H, W = frames[0].shape[:2]
    done = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", "%dx%d" % (W, H), "-r", str(fps), "-i", "-", "-c:v", "libx264rgb", "-qp", "0",
                           "-preset", "ultrafast", str(path)], input=b"".join(np.ascontiguousarray(f, np.uint8).tobytes()
                                                                              for f in frames),
                          capture_output=True, timeout=60)
    if done.returncode:
        raise RuntimeError(done.stderr.decode(errors="replace")[-300:])
    return Path(path)


def read_video(path: Path):
    p = fx.probe(path)["streams"][0]
    return fx.frames(path, size=(int(p["width"]), int(p["height"])))


_GRIDS = {}


def _grid(h, w):
    if (h, w) not in _GRIDS:
        _GRIDS[(h, w)] = np.mgrid[0:h, 0:w].astype(np.float32)
    return _GRIDS[(h, w)]


def blob(frame, rgb, tol=40, bg=None):
    """Centroid, area, orientation (deg) of one marker colour; None when absent. With bg (the known flat background)
    antialiased edge pixels count by their coverage, so centroids and areas are sub-pixel."""
    f = frame[..., :3].astype(np.float32)
    c = np.array(rgb, np.float32)
    if bg is not None:
        b = np.array(bg, np.float32)
        v = c - b
        a = np.clip(((f - b) @ v) / (v @ v), 0, 1)
        resid = np.abs(f - (b + a[..., None] * v)).max(-1)
        w = np.where((resid < 30) & (a > 0.04), a, 0.0)
    else:
        w = (np.abs(f - c).max(-1) <= tol).astype(float)
    tot = w.sum()
    if tot < 3:
        return None
    ys, xs = _grid(f.shape[0], f.shape[1])
    cx, cy = (w * xs).sum() / tot + 0.5, (w * ys).sum() / tot + 0.5          # pixel centres sit at +0.5
    mxx, myy, mxy = (w * (xs - cx) ** 2).sum() / tot, (w * (ys - cy) ** 2).sum() / tot, (w * (xs - cx) * (ys - cy)).sum() / tot
    ang = 0.5 * math.degrees(math.atan2(2 * mxy, mxx - myy))
    yy, xx = np.nonzero(w > 0.5)
    if len(xx) == 0:
        yy, xx = np.nonzero(w > 0)
    return {"cx": float(cx), "cy": float(cy), "area": float(tot), "ang": ang,
            "x0": int(xx.min()), "x1": int(xx.max()), "y0": int(yy.min()), "y1": int(yy.max())}


def track_colors(frames, cols, tol=40, bg=None):
    import hashlib
    memo, out = {}, []
    for f in frames:
        h = hashlib.md5(np.ascontiguousarray(f).tobytes()).hexdigest()   # identical frames measure identically
        if h not in memo:
            memo[h] = [blob(f, c, tol, bg) for c in cols]
        out.append(memo[h])
    return out


def dom2d(wd, name, body, js, sels, colors, times, fps, W=320, H=180, css="", extra_js="null", scripts=None, tol=None,
          mutate=None):
    """Run motion-kit/GSAP in Chrome, paint the tracked quads, write the output video, measure it back."""
    scripts = [GSAP, MKIT] if scripts is None else scripts
    full = DOM_SAMPLER + "const M=window.MOTION, E=M&&M.E; let tl=gsap.timeline({paused:true});\n" + js + \
        "\nOUT({frames: SAMPLE(%s, %s, %s)});" % (json.dumps(times), json.dumps(sels), extra_js)
    out, _ = chrome_run(wd, name, page(body, full, scripts, W, H, css), (W, H + 40))
    frames = out["frames"]
    if mutate:
        mutate(frames)
    rgbs = [hex2rgb(c) if c else None for c in colors]
    pix = paint_frames(frames, rgbs, W, H)
    vid = write_video(wd / ("%s.mp4" % name), pix, fps)
    mbg = None if tol else (119, 119, 119)
    meas = track_colors(read_video(vid), [c for c in rgbs if c], tol=tol or 40, bg=mbg)
    (wd / ("%s_samples.json" % name)).write_text(json.dumps(frames), encoding="utf-8")
    still = [pix[0]] * len(pix)                       # the unprocessed input: the first frame held
    inp = write_video(wd / ("%s_input.mp4" % name), still, fps)
    meas_in = track_colors(read_video(inp), [c for c in rgbs if c], tol=tol or 40, bg=mbg)
    return {"frames": frames, "video": vid, "meas": meas, "meas_in": meas_in, "json": wd / ("%s_samples.json" % name),
            "input": inp}


def box_html(i, x, y, w, h, color, extra=""):
    return '<div id="%s" class="a" style="left:%spx;top:%spx;width:%spx;height:%spx;background:%s;%s"></div>' % (
        i, x, y, w, h, color, extra)


def scale_series(meas, k=0):
    a0 = meas[0][k]["area"]
    return [math.sqrt(m[k]["area"] / a0) if m[k] else 0.0 for m in meas]


def maxerr(a, b):
    return float(max(abs(x - y) for x, y in zip(a, b)))


def times_for(dur, fps):
    return [round(i / fps, 6) for i in range(int(round(dur * fps)) + 1)]


# a stage with one wide red marker centred and a blue marker off-centre (scale and rotation readable from both)
STAGE = ('<div id="stage" class="a" style="left:0;top:0;width:320px;height:180px;transform-origin:50%% 50%%">%s%s</div>'
         % (box_html("mk", 152, 85, 16, 10, "#ff0000"), box_html("mb", 194, 64, 12, 12, "#0000ff")))
RED, BLUE = "#ff0000", "#0000ff"


def stage_scale(meas):
    """Scale of the stage from the red-blue marker distance (robust to blur, independent of area)."""
    d = [math.hypot(m[0]["cx"] - m[1]["cx"], m[0]["cy"] - m[1]["cy"]) if m[0] and m[1] else 0.0 for m in meas]
    return [x / d[0] for x in d]


def stage_angle(meas):
    a = [math.degrees(math.atan2(m[1]["cy"] - m[0]["cy"], m[1]["cx"] - m[0]["cx"])) if m[0] and m[1] else 0 for m in meas]
    return [x - a[0] for x in a]


def py_spring(z=0.74, w=17.0):
    def f(t):
        if z < 1:
            wd = w * math.sqrt(1 - z * z)
            return 1 - math.exp(-z * w * t) * (math.cos(wd * t) + (z * w / wd) * math.sin(wd * t))
        return 1 - math.exp(-w * t) * (1 + w * t)
    end = f(1)
    return lambda p: f(p) / end


def py_zoomtrack(t, keys, settle=0.6):
    sp = py_spring()
    v = math.log(keys[0][1])
    for kt, kv in keys[1:]:
        if t <= kt:
            break
        v = v + (math.log(kv) - v) * sp(min(1, (t - kt) / settle))
    return math.exp(v)


def out_files(*paths):
    return [Path(p) for p in paths if p]


# ───────────────────────────── 2D stage camera (motion-kit) ─────────────────────────────


def _zoom_track_card(wd, name, keys):
    fps, dur = 30, keys[-1][0] + 0.9
    T = times_for(dur, fps)
    js = "const K=%s; window.camAt=(t)=>gsap.set('#stage',{scale:M.zoomTrack(t,K)});" % json.dumps(keys)
    r = dom2d(wd, name, STAGE, js, ["#mk", "#mb"], [RED, BLUE], T, fps)
    s = stage_scale(r["meas"])
    model = [py_zoomtrack(t, keys) for t in T]
    checks = [check("measured stage scale follows the log-space spring model", maxerr(s, model) < 0.03, maxerr(s, model), "<0.03")]
    for i in range(1, len(keys)):
        kt, kv = keys[i]
        j = min(len(T) - 1, int(round((kt + 0.6) * fps)))
        checks.append(check("settles on target %.2f after key %d" % (kv, i), abs(s[j] - kv) / kv < 0.03, s[j], kv))
        jm = min(range(len(T)), key=lambda j: abs(py_spring()(min(1, max(0, (T[j] - kt) / 0.6))) - 0.5) if T[j] > kt else 9)
        u = py_spring()(min(1, (T[jm] - kt) / 0.6))
        a0 = model[int(round(kt * fps))]
        lm = math.exp(math.log(a0) + (math.log(kv) - math.log(a0)) * u)
        li = a0 + (kv - a0) * u
        checks.append(check("mid-move value is the log-space mix, not the linear mix (key %d)" % i,
                            abs(s[jm] - lm) < abs(s[jm] - li) and abs(s[jm] - lm) < 0.04, s[jm], {"log": lm, "linear": li}))
    s_in = stage_scale(r["meas_in"])
    checks.append(check("negative control: the unprocessed still does not reach the targets",
                        not maxerr(s_in, model) < 0.03, maxerr(s_in, model), ">=0.03"))
    return checks, out_files(r["video"], r["json"])


@card("CAM-01")
def cam01(task, wd):
    """Spring track on log(scale) with several targets: MOTION.zoomTrack(t, keys)."""
    return _zoom_track_card(wd, "zoomtrack", [[0, 1.0], [0.3, 2.5], [1.3, 1.25], [2.2, 2.0]])


@card("CAM-128")
def cam128(task, wd):
    """MOTION.lmix / push / zoomTrack: scale interpolated in log space."""
    checks, outs = _zoom_track_card(wd, "lmix_track", [[0, 1.0], [0.2, 3.0], [1.1, 1.5]])
    fps = 15
    T = times_for(1.5, fps)
    js = "M.push(tl,'#stage',0,1,3,1.4,{ease:E.dolly}); window.LM=[M.lmix(1,4,.5),M.lmix(2,8,.25)];"
    r = dom2d(wd, "lmix_push", STAGE, js, ["#mk", "#mb"], [RED, BLUE], T, fps, extra_js="(t)=>window.LM")
    s = stage_scale(r["meas"])
    model = [log_push(1, 3, min(1, t / 1.4), EZ["dolly"]) for t in T]
    lm = r["frames"][0]["x"]
    checks += [check("lmix(1,4,.5) is the geometric mean 2", abs(lm[0] - 2) < 1e-9, lm[0], 2),
               check("lmix(2,8,.25) = 2*4^.25", abs(lm[1] - 2 * 4 ** .25) < 1e-9, lm[1], 2 * 4 ** .25),
               check("M.push measured scale follows exp(lerp(log a, log b, E.dolly))", maxerr(s, model) < 0.03,
                     maxerr(s, model), "<0.03"),
               check("negative control: still input does not follow the push", maxerr(stage_scale(r["meas_in"]), model) > 0.3,
                     maxerr(stage_scale(r["meas_in"]), model), ">0.3")]
    return checks, outs + out_files(r["video"])


def _push_card(wd, name, a, b, dur, ease, js_ease, peak_rule=None):
    fps = 30
    T = times_for(dur + 0.2, fps)
    d = "undefined" if dur is None else str(dur)
    js = "M.push(tl,'#stage',0,%s,%s,%s,{ease:%s});" % (a, b, d, js_ease)
    r = dom2d(wd, name, STAGE, js, ["#mk", "#mb"], [RED, BLUE], T, fps)
    s = stage_scale(r["meas"])
    model = [log_push(a, b, min(1, t / dur), EZ[ease]) * 1 / a for t in T]
    checks = [check("measured scale follows the log-space push model", maxerr(s, model) < 0.03, maxerr(s, model), "<0.03"),
              check("ends at the target scale", abs(s[-1] - b / a) < 0.03, s[-1], b / a)]
    if peak_rule:
        rate = max(abs(math.log(model[i + 1] / model[i])) for i in range(len(model) - 1)) / 2  # per 1/60 s
        checks.append(check("peak scale change per 60-fps frame within the ~5% rule", rate <= peak_rule, rate, "<=%s" % peak_rule))
    s_in = stage_scale(r["meas_in"])
    checks.append(check("negative control: still input does not push", abs(s_in[-1] - b / a) > 0.1, s_in[-1], "!=%.2f" % (b / a)))
    return checks, r


@card("CAM-160")
def cam160(task, wd):
    """MOTION.push in log space with the default camera duration durFor(|d|*600, camera) and the E.cam ease."""
    dur = min(2.4, max(0.6, 0.35 + 0.00135 * abs(2.4 - 1.0) * 600))
    fps = 30
    T = times_for(dur + 0.2, fps)
    r = dom2d(wd, "logpush", STAGE, "M.push(tl,'#stage',0,1,2.4);", ["#mk", "#mb"], [RED, BLUE], T, fps)
    s = stage_scale(r["meas"])
    model = [log_push(1, 2.4, min(1, t / dur), EZ["cam"]) for t in T]
    rate = max(abs(math.log(model[i + 1] / model[i])) for i in range(len(model) - 1)) / 2
    meas_rate = max(abs(math.log(s[i + 1] / s[i])) for i in range(len(s) - 1)) / 2
    j = int(round(0.5 * dur * fps))
    linear_mid = 1 + (2.4 - 1) * EZ["cam"](0.5)
    checks = [check("default duration = durFor(840 px, camera)", abs(dur - 1.484) < 1e-3, dur, 1.484),
              check("measured scale follows the log push (E.cam)", maxerr(s, model) < 0.03, maxerr(s, model), "<0.03"),
              check("mid-way scale is the log value, not the linear one", abs(s[j] - model[j]) < abs(s[j] - linear_mid),
                    s[j], {"log": model[j], "linear": linear_mid}),
              check("peak ~5% scale per 60-fps frame (measured)", meas_rate <= 0.06, meas_rate, "<=0.06"),
              check("negative control: still input scale stays 1", abs(stage_scale(r["meas_in"])[-1] - 2.4) > 1,
                    stage_scale(r["meas_in"])[-1], "!=2.4")]
    return checks, out_files(r["video"], r["json"])


def _breathe_card(wd, name, creep, drift, dur):
    fps = 15
    T = times_for(dur, fps)
    js = "M.breathe(tl,'#stage',0,%s,{creep:%s,drift:%s});" % (dur, creep, drift)
    r = dom2d(wd, name, STAGE, js, ["#mk", "#mb"], [RED, BLUE], T, fps)
    s = np.array(stage_scale(r["meas"]))
    x = np.array([m[0]["cx"] for m in r["meas"]])
    tt = np.array(T)
    slope, icpt = np.polyfit(tt, s, 1)
    # the browser's own corner positions (exact) for linearity and liveness; the video for the measured rate
    q = [fr["el"][0]["q"] for fr in r["frames"]]
    w = np.array([math.hypot(a[1][0] - a[0][0], a[1][1] - a[0][1]) for a in q]) / 16.0
    res = w - np.polyval(np.polyfit(tt, w, 1), tt)
    checks = [check("measured scale creeps at the creep rate (/s)", abs(slope - creep) < max(0.004, 0.15 * creep), slope, creep),
              check("creep is linear (ease none): residual of the browser's scale", float(np.abs(res).max()) < 1e-4,
                    float(np.abs(res).max()), "<1e-4"),
              check("never frozen: scale grows every frame", bool((np.diff(w) > 0.5 * creep / fps).all()),
                    float(np.diff(w).min()), ">0")]
    if drift:
        xs = np.polyfit(tt, x - x[0], 1)[0]
        # stage x moves by drift*60 px/s; the centred red marker sits on the origin so it moves 1:1
        checks.append(check("x drift = drift px/frame x 60 per second", abs(xs - drift * 60) < 0.1 * drift * 60 + 0.5, xs, drift * 60))
    s_in = np.array(stage_scale(r["meas_in"]))
    checks.append(check("negative control: still input has no creep", abs(np.polyfit(tt, s_in, 1)[0] - creep) > 0.5 * creep,
                        float(np.polyfit(tt, s_in, 1)[0]), "!=%s" % creep))
    return checks, out_files(r["video"], r["json"])


@card("CAM-14")
def cam14(task, wd):
    """MOTION.breathe: a living hold, scale creep (template value .02/s) plus a small drift."""
    return _breathe_card(wd, "breathe", 0.02, 0.2, 2.0)


@card("CAM-131")
def cam131(task, wd):
    """breathe holds: default creep ~4%/s, no handheld shake (monotonic, no jitter)."""
    checks, outs = _breathe_card(wd, "breathe_hold", 0.04, 0, 2.0)
    vid = read_video(wd / "breathe_hold.mp4")
    m = track_colors(vid, [hex2rgb(RED), hex2rgb(BLUE)], bg=(119, 119, 119))
    sc = stage_scale(m)
    diffs = np.diff(sc)
    checks.append(check("no shake: scale strictly non-decreasing and centre fixed",
                        bool((diffs > -1e-3).all()) and maxerr([q[0]["cx"] for q in m], [m[0][0]["cx"]] * len(m)) < 0.6,
                        float(diffs.min()), ">-1e-3"))
    return checks, outs


def _shake_card(wd, name, amp, dur, hz, rot, seed):
    fps = 60
    T = times_for(dur + 0.3, fps)
    W, H = 320, 180
    body = ('<div id="stage" class="a" style="left:0;top:0;width:320px;height:180px">%s%s</div>'
            % (box_html("mk", 150, 85, 20, 10, RED), box_html("mb", 220, 60, 12, 12, BLUE)))
    js = "M.shake(tl,'#stage',0,{amp:%s,dur:%s,hz:%s,rot:%s,seed:%s});" % (amp, dur, hz, rot, seed)
    r = dom2d(wd, name, body, js, ["#mk", "#mb"], [RED, BLUE], T, fps)
    x0, y0 = r["meas"][0][0]["cx"], r["meas"][0][0]["cy"]
    dx = np.array([m[0]["cx"] - x0 for m in r["meas"]])
    dy = np.array([m[0]["cy"] - y0 for m in r["meas"]])
    ang = np.array(stage_angle(r["meas"]))
    n_dur = int(dur * fps)
    first, second = dx[:n_dur // 2], dx[n_dur // 2:n_dur]
    rms1, rms2 = float(np.sqrt((first ** 2).mean())), float(np.sqrt((second ** 2).mean()))
    end = int(round((dur + 0.15) * fps))
    # determinism: the kit's own rng re-run with the same and a different seed (sampled offsets, not pixels)
    js2 = ("const a=gsap.timeline({paused:true}),b=gsap.timeline({paused:true}),c=gsap.timeline({paused:true});"
           "const e1=document.querySelector('#mk'),e2=document.querySelector('#mb'),e3=document.querySelector('#stage');"
           "M.shake(a,e1,0,{amp:%s,dur:%s,hz:%s,seed:%s});M.shake(b,e2,0,{amp:%s,dur:%s,hz:%s,seed:%s});"
           "M.shake(c,e3,0,{amp:%s,dur:%s,hz:%s,seed:%s});const v=[];for(let i=1;i<10;i++){const t=i*%s/10;a.seek(t,false);"
           "b.seek(t,false);c.seek(t,false);v.push([gsap.getProperty(e1,'x'),gsap.getProperty(e2,'x'),gsap.getProperty(e3,'x')]);}"
           "OUT(v);") % (amp, dur, hz, seed, amp, dur, hz, seed, amp, dur, hz, seed + 1, dur)
    v, _ = chrome_run(wd, name + "_seed", page(body, DOM_SAMPLER + "const M=window.MOTION;" + js2, [GSAP, MKIT]), (W, H + 40))
    same = all(abs(a - b) < 1e-9 for a, b, _ in v)
    diff = any(abs(a - c) > 0.5 for a, _, c in v)
    checks = [check("peak offset within amp and clearly shaking", 0.3 * amp <= float(np.abs(dx).max()) <= amp * 1.05 + 0.6,
                    float(np.abs(dx).max()), [0.3 * amp, amp]),
              check("y amplitude about 0.7 of x", float(np.abs(dy).max()) <= 0.7 * amp * 1.05 + 0.6, float(np.abs(dy).max()), "<=%.1f" % (0.7 * amp)),
              check("decaying envelope: first-half RMS > 1.8 x second-half RMS", rms1 > 1.8 * rms2, [rms1, rms2], "ratio>1.8"),
              check("rotation bounded by rot degrees", float(np.abs(ang).max()) <= rot * 1.3 + 0.4, float(np.abs(ang).max()), "<=%s" % rot),
              check("settles to rest after dur + settle", abs(dx[end:]).max() < 0.6 and abs(dy[end:]).max() < 0.6,
                    float(abs(dx[end:]).max()), "<0.6"),
              check("seeded: same seed gives the same offsets", same, same, True),
              check("seeded: another seed gives different offsets", diff, diff, True)]
    dxi = np.array([m[0]["cx"] - x0 for m in r["meas_in"]])
    checks.append(check("negative control: still input never shakes", float(np.abs(dxi).max()) < 0.3 * amp, float(np.abs(dxi).max()), "<%.1f" % (0.3 * amp)))
    return checks, out_files(r["video"], r["json"])


@card("CAM-17")
def cam17(task, wd):
    """MOTION.shake: decaying seeded jitter (amp 14 px, y x0.7, 0.5 s, 28 Hz, rot .6 deg, decay (1-i/n)^1.8)."""
    return _shake_card(wd, "shake", 14, 0.5, 28, 0.6, 7)


@card("CAM-129")
def cam129(task, wd):
    """shake: a decaying seeded camera hit (lighter variant, seed 3)."""
    return _shake_card(wd, "shake_hit", 10, 0.4, 24, 0.5, 3)


@card("CAM-161")
def cam161(task, wd):
    """Camera shake (seeded) with the card's defaults, seed 11."""
    return _shake_card(wd, "shake_seeded", 14, 0.5, 28, 0.6, 11)


def _parallax_card(wd, name, depths, dx, dy, scale, dur, colors):
    fps = 15
    T = times_for(dur, fps)
    body = "".join(box_html("L%d" % i, 40 + 70 * i, 60 + 12 * i, 30, 30, c) for i, c in enumerate(colors))
    layers = ",".join("{el:'#L%d',depth:%s}" % (i, d) for i, d in enumerate(depths))
    js = "M.parallax(tl,[%s],0,%s,{dx:%s,dy:%s,scale:%s});" % (layers, dur, dx, dy, scale)
    r = dom2d(wd, name, body, js, ["#L%d" % i for i in range(len(depths))], colors, T, fps)
    m0, m1 = r["meas"][0], r["meas"][-1]
    checks = []
    for i, d in enumerate(depths):
        mx = m1[i]["cx"] - m0[i]["cx"]
        my = m1[i]["cy"] - m0[i]["cy"]
        sc = math.sqrt(m1[i]["area"] / m0[i]["area"])
        checks.append(check("layer depth %s moves dx*depth" % d, abs(mx - dx * d) < 1.0 and abs(my - dy * d) < 1.0, [mx, my], [dx * d, dy * d]))
        if scale:
            checks.append(check("layer depth %s scales 1+scale*depth" % d, abs(sc - (1 + scale * d)) < 0.04, sc, 1 + scale * d))
    mid = len(T) // 2
    lin = [(r["meas"][mid][i]["cx"] - m0[i]["cx"]) / (m1[i]["cx"] - m0[i]["cx"]) for i in range(len(depths)) if abs(depths[i] * dx) > 4]
    lin += [(r["meas"][mid][i]["cy"] - m0[i]["cy"]) / (m1[i]["cy"] - m0[i]["cy"]) for i in range(len(depths)) if abs(depths[i] * dy) > 4]
    checks.append(check("ease none: half-way is half the offset", all(abs(v - 0.5) < 0.06 for v in lin), lin, 0.5))
    order = [math.hypot(m1[i]["cx"] - m0[i]["cx"], m1[i]["cy"] - m0[i]["cy"]) for i in range(len(depths))]
    checks.append(check("far layers move less than near ones", order == sorted(order), order, "increasing with depth"))
    mi = r["meas_in"]
    moved = max(abs(mi[-1][i]["cx"] - mi[0][i]["cx"]) for i in range(len(depths)))
    checks.append(check("negative control: still input has no parallax", moved < 0.5, moved, "<0.5"))
    return checks, out_files(r["video"], r["json"])


@card("CAM-15")
def cam15(task, wd):
    """MOTION.parallax: offset = dx*depth, scale 1+scale*depth, ease none."""
    return _parallax_card(wd, "parallax", [0.2, 0.5, 1.0], -60, 0, 0.1, 2.0, [RED, "#00ff00", BLUE])


@card("CAM-130")
def cam130(task, wd):
    """parallax: layers moving by depth (vertical drift, four layers)."""
    return _parallax_card(wd, "parallax_v", [0.1, 0.35, 0.7, 1.2], 0, -30, 0, 1.5, [RED, "#00ff00", BLUE, "#ffff00"])


# ───────────────────────────── generic verification for timeline cards ─────────────────────────────


def P(meas, k):
    """x, y arrays of marker k (nan when absent)."""
    return (np.array([m[k]["cx"] if m[k] else np.nan for m in meas]), np.array([m[k]["cy"] if m[k] else np.nan for m in meas]))


def SC(meas, k):
    a = np.array([m[k]["area"] if m[k] else np.nan for m in meas])
    return np.sqrt(a / a[0])


def D(meas, i, j):
    xi, yi = P(meas, i)
    xj, yj = P(meas, j)
    d = np.hypot(xi - xj, yi - yj)
    return d / d[0]


def verify(r, crits):
    """crits: [(name, fn(meas, frames) -> (ok, measured), expected)]; the first criterion is re-run on the
    unprocessed input as the negative control."""
    out = []
    for name, fn, exp in crits:
        ok, m = fn(r["meas"], r["frames"])
        out.append(check(name, ok, m, exp))
    name, fn, exp = crits[0]
    try:
        ok, m = fn(r["meas_in"], r["frames"])
    except Exception as exc:  # the input lacks what the method produces (e.g. a marker never appears)
        ok, m = False, "n/a: %s" % type(exc).__name__
    out.append(check("negative control (unprocessed input): " + name, not ok, m, "criterion fails"))
    return out


def idx(T, t):
    return int(np.argmin(np.abs(np.array(T) - t)))


def run_tl(wd, name, body, js, sels, colors, dur, fps, crits, W=320, H=180, css="", extra_js="null", t0=0.0, scripts=None,
           tol=None, mutate=None):
    T = [round(t0 + i / fps, 6) for i in range(int(round(dur * fps)) + 1)]
    r = dom2d(wd, name, body, js, sels, colors, T, fps, W, H, css, extra_js, scripts, tol, mutate)
    r["T"] = T
    c = crits(r, T) if callable(crits) else crits
    return verify(r, c), out_files(r["video"], r["json"])


def sharp(frame, rgb, bg=(119, 119, 119)):
    """Edge sharpness of a marker: the steepest coverage step across its edges (1 = hard edge)."""
    f = frame[..., :3].astype(float)
    v = np.array(rgb, float) - np.array(bg, float)
    a = np.clip(((f - np.array(bg, float)) @ v) / (v @ v), 0, 1)
    return float(max(np.abs(np.diff(a, axis=0)).max(), np.abs(np.diff(a, axis=1)).max()))


# ───────────────────────────── 2D camera cards on GSAP timelines ─────────────────────────────


@card("CAM-16")
def cam16(task, wd):
    """MOTION.rackFocus: cross-fade a sharp element and a constant-blur twin (blur 18 px, 0.3 s, E.smooth)."""
    body = box_html("subj", 130, 60, 60, 60, "#ff0000")
    js = "const tw=M.rackFocus(tl,document.querySelector('#subj'),0.5,{blur:18,dur:0.3}); tw.id='twin';"
    fps = 30
    T = times_for(1.2, fps)
    r = dom2d(wd, "rack", body, js, ["#subj", "#twin"], [RED, RED], T, fps)
    vid = read_video(r["video"])
    inp = read_video(r["input"])
    sh = [sharp(f, hex2rgb(RED)) for f in vid]
    tb = [fr["el"][1]["b"] for fr in r["frames"]]
    op = [fr["el"][0]["o"] for fr in r["frames"]]
    mid = idx(T, 0.65)
    checks = [check("sharp before the pull", sh[idx(T, 0.3)] > 0.9, sh[idx(T, 0.3)], ">0.9"),
              check("defocused after the pull", sh[idx(T, 1.0)] < 0.3, sh[idx(T, 1.0)], "<0.3"),
              check("the twin's blur is constant 18 px (never animated)", min(tb) == max(tb) == 18, [min(tb), max(tb)], 18),
              check("cross-fade follows E.smooth at mid-pull", abs(op[mid] - (1 - EZ["smooth"]((T[mid] - 0.5) / 0.3))) < 0.02,
                    op[mid], 1 - EZ["smooth"]((T[mid] - 0.5) / 0.3)),
              check("negative control: unprocessed input never defocuses", not (sharp(inp[idx(T, 1.0)], hex2rgb(RED)) < 0.3),
                    sharp(inp[idx(T, 1.0)], hex2rgb(RED)), ">=0.3")]
    return checks, out_files(r["video"], r["json"])


def _cam_move(wd, name, x, y, sc, rot, dur):
    js = "M.camera(tl,'#stage',0,{x:%s,y:%s,scale:%s,rotation:%s,dur:%s});" % (x, y, sc, rot, dur)

    def crits(r, T):
        e = [EZ["cam"](min(1, t / dur)) for t in T]
        dd = lambda m: D(m, 0, 1)
        ang = lambda m: np.array(stage_angle(m))
        cx = lambda m: P(m, 0)[0] - P(m, 0)[0][0]
        return [("scale follows 1+(S-1)*E.cam(t/dur)", lambda m, f: (maxerr(dd(m), [1 + (sc - 1) * v for v in e]) < 0.02,
                                                                      maxerr(dd(m), [1 + (sc - 1) * v for v in e])), "<0.02"),
                ("rotation reaches %s deg along E.cam" % rot, lambda m, f: (maxerr(ang(m), [rot * v for v in e]) < 0.6,
                                                                            maxerr(ang(m), [rot * v for v in e])), "<0.6 deg"),
                ("stage translation reaches x=%s" % x, lambda m, f: (abs(cx(m)[-1] - x) < 2.5, float(cx(m)[-1])), x),
                ("the move starts slow: progress at 20% time equals E.cam(.2), below linear",
                 lambda m, f: (abs((dd(m)[idx(T, 0.2 * dur)] - 1) / (sc - 1) - EZ["cam"](T[idx(T, 0.2 * dur)] / dur)) < 0.02
                               and (dd(m)[idx(T, 0.2 * dur)] - 1) / (sc - 1) < 0.2,
                               float((dd(m)[idx(T, 0.2 * dur)] - 1) / (sc - 1))), "E.cam(.2)=%.3f" % EZ["cam"](0.2))]
    return run_tl(wd, name, STAGE, js, ["#mk", "#mb"], [RED, BLUE], dur + 0.2, 30, crits)


@card("CAM-159")
def cam159(task, wd):
    """MOTION.camera: the whole stage moves as one object (x, y, scale, rotation), dur 1.4 s, ease E.cam."""
    return _cam_move(wd, "stagecam", 24, -10, 1.3, 6, 1.4)


@card("CAM-153")
def cam153(task, wd):
    """Stage camera moves: M.camera (E.cam), then M.push in log space, then M.breathe creep .04/s."""
    js = ("M.camera(tl,'#stage',0,{x:12,scale:1.2,dur:1.4}); M.push(tl,'#stage',1.5,1.2,2.2,1.2);"
          "M.breathe(tl,'#stage',2.8,1.2,{creep:.04});")

    def crits(r, T):
        dd = lambda m: D(m, 0, 1)
        i15, i28 = idx(T, 1.5), idx(T, 2.8)
        ph1 = [1 + 0.2 * EZ["cam"](min(1, t / 1.4)) for t in T[:i15 + 1]]
        ph2 = [log_push(1.2, 2.2, min(1, max(0, (t - 1.5) / 1.2)), EZ["cam"]) for t in T[i15:i28 + 1]]
        return [("phase 2 push follows the log-space model", lambda m, f: (maxerr(dd(m)[i15:i28 + 1], ph2) < 0.03,
                                                                         maxerr(dd(m)[i15:i28 + 1], ph2)), "<0.03"),
                ("phase 1 camera move follows E.cam", lambda m, f: (maxerr(dd(m)[:i15 + 1], ph1) < 0.02, maxerr(dd(m)[:i15 + 1], ph1)), "<0.02"),
                ("phase 3 breathe creeps 0.04/s", lambda m, f: (abs(np.polyfit(T[i28:], dd(m)[i28:], 1)[0] - 0.04) < 0.008,
                                                                float(np.polyfit(T[i28:], dd(m)[i28:], 1)[0])), 0.04)]
    return run_tl(wd, "stagemoves", STAGE, js, ["#mk", "#mb"], [RED, BLUE], 4.0, 15, crits)


@card("CAM-138")
def cam138(task, wd):
    """Log-space push 1.0->1.09 over 2.4 s (E.dolly) then a living hold (breathe creep .012) plus ring rotation 8 deg linear."""
    body = STAGE + box_html("ring", 40, 40, 40, 8, "#00ff00")
    js = ("M.push(tl,'#stage',0,1,1.09,2.4,{ease:E.dolly}); M.breathe(tl,'#stage',2.4,2.6,{creep:.012});"
          "tl.fromTo('#ring',{rotation:0},{rotation:8,duration:5,ease:'none'},0);")

    def crits(r, T):
        dd = lambda m: D(m, 0, 1)
        i24 = idx(T, 2.4)
        push = [log_push(1, 1.09, t / 2.4, EZ["dolly"]) for t in T[:i24 + 1]]
        ang = lambda m: np.array([v[2]["ang"] if v[2] else np.nan for v in m]) - (m[0][2]["ang"] if m[0][2] else 0)
        return [("push reaches 1.09 at 2.4 s along log E.dolly", lambda m, f: (maxerr(dd(m)[:i24 + 1], push) < 0.01, maxerr(dd(m)[:i24 + 1], push)), "<0.01"),
                ("hold creeps .012/s afterwards (never frozen)", lambda m, f: (abs(np.polyfit(T[i24:], dd(m)[i24:], 1)[0] - 0.012) < 0.004,
                                                                              float(np.polyfit(T[i24:], dd(m)[i24:], 1)[0])), 0.012),
                ("ring rotates 8 deg linearly", lambda m, f: (abs(ang(m)[-1] - 8) < 0.8 and abs(ang(m)[len(T) // 2] - 4) < 0.8,
                                                              [float(ang(m)[len(T) // 2]), float(ang(m)[-1])]), [4, 8])]
    return run_tl(wd, "logpush_hold", body, js, ["#mk", "#mb", "#ring"], [RED, BLUE, "#00ff00"], 5.0, 10, crits)


@card("CAM-150")
def cam150(task, wd):
    """Camera breath and punctuating pushes on a 2D #cam (origin 50% 52%): 1->1.035 linear over 10.9 s, 1.075 y-18 in
    1.6 s E.cam at 10.99, 1.06 y0 over 9.5 s, 1.09 y-10 in 1.7 s at 22.95 (max scale 1.09)."""
    js = ("gsap.set('#stage',{transformOrigin:'50% 52%'});"
          "tl.to('#stage',{scale:1.035,duration:10.9,ease:'none'},0);"
          "tl.to('#stage',{scale:1.075,y:-18*180/1080,duration:1.6,ease:E.cam},10.99);"
          "tl.to('#stage',{scale:1.06,y:0,duration:9.5,ease:'none'},12.59);"
          "tl.to('#stage',{scale:1.09,y:-10*180/1080,duration:1.7,ease:E.cam},22.95);")

    def crits(r, T):
        dd = lambda m: D(m, 0, 1)
        k = {t: idx(T, t) for t in (5.45, 10.9, 12.59, 22.09, 24.65)}
        exp = {5.45: 1.0175, 10.9: 1.035, 12.59: 1.075, 22.09: 1.06, 24.65: 1.09}
        return [("scale at the scripted beats", lambda m, f: (max(abs(dd(m)[k[t]] - exp[t]) for t in exp) < 0.006,
                                                              {str(t): float(dd(m)[k[t]]) for t in exp}), exp),
                ("max scale stays 1.09", lambda m, f: (float(np.nanmax(dd(m))) < 1.096, float(np.nanmax(dd(m)))), "<=1.09"),
                ("the breath is linear across the first 10.9 s", lambda m, f: (float(np.abs(dd(m)[:k[10.9]] - (1 + 0.035 * np.array(T[:k[10.9]]) / 10.9)).max()) < 0.004,
                                                                              float(np.abs(dd(m)[:k[10.9]] - (1 + 0.035 * np.array(T[:k[10.9]]) / 10.9)).max())), "<0.004")]
    return run_tl(wd, "breath_push", STAGE, js, ["#mk", "#mb"], [RED, BLUE], 25.0, 4, crits)


@card("CAM-152")
def cam152(task, wd):
    """Emotional punch + shake: scale 1->1.09 in .25 s E.out, back over .9 s E.rest; x +-8 px yoyo .05 s repeat 7; reset +.46 s."""
    js = ("tl.to('#stage',{scale:1.09,duration:.25,ease:E.out},0.2);tl.to('#stage',{scale:1,duration:.9,ease:E.rest},0.45);"
          "tl.fromTo('#stage',{x:-8},{x:8,duration:.05,yoyo:true,repeat:7,ease:'none',immediateRender:false},0.2);tl.set('#stage',{x:0},0.66);")

    def crits(r, T):
        dd = lambda m: D(m, 0, 1)
        x = lambda m: P(m, 0)[0] - P(m, 0)[0][0]
        i = idx(T, 0.45)
        return [("punch peaks at 1.09 (+9%) after .25 s", lambda m, f: (abs(dd(m)[i] - 1.09) < 0.006, float(dd(m)[i])), 1.09),
                ("shake +-8 px during the punch", lambda m, f: (7 <= float(np.nanmax(np.abs(x(m)[idx(T, .2):idx(T, .6)]))) <= 9.5,
                                                               float(np.nanmax(np.abs(x(m)[idx(T, .2):idx(T, .6)])))), 8),
                ("settled: scale 1 and x 0 after reset", lambda m, f: (abs(dd(m)[-1] - 1) < 0.004 and abs(x(m)[-1]) < 0.4,
                                                                      [float(dd(m)[-1]), float(x(m)[-1])]), [1, 0]),
                ("x crosses zero 8 half-cycles", lambda m, f: (sum(1 for a, b in zip(x(m)[idx(T, .2):idx(T, .62)], x(m)[idx(T, .2) + 1:idx(T, .62)]) if a * b < 0) >= 6,
                                                               sum(1 for a, b in zip(x(m)[idx(T, .2):idx(T, .62)], x(m)[idx(T, .2) + 1:idx(T, .62)]) if a * b < 0)), ">=6")]
    return run_tl(wd, "punch_shake", STAGE, js, ["#mk", "#mb"], [RED, BLUE], 1.4, 100, crits)


@card("CAM-137")
def cam137(task, wd):
    """Seeded 4-frame micro shake: tl.set(cam,{x,y}) at 10.90+d for (0,6,-4),(1/30,-5,3),(2/30,3,-2),(3/30,0,0) + #dim .22 flash."""
    body = STAGE + '<div id="dim" class="a" style="inset:0;background:#000;opacity:0"></div>'
    js = ("for(const [d,x,y] of [[0,6,-4],[1/30,-5,3],[2/30,3,-2],[3/30,0,0]]) tl.set('#stage',{x,y},10.90+d);"
          "tl.set('#dim',{opacity:.22},10.90);tl.set('#dim',{opacity:0},10.90+4/30);")
    fps = 30

    def crits(r, T):
        x = lambda m: P(m, 0)[0] - P(m, 0)[0][0]
        y = lambda m: P(m, 0)[1] - P(m, 0)[1][0]
        want = [(6, -4), (-5, 3), (3, -2), (0, 0)]
        got = lambda m: [(round(float(x(m)[idx(T, 10.9 + k / 30)]), 2), round(float(y(m)[idx(T, 10.9 + k / 30)]), 2)) for k in range(4)]
        lum = lambda: [float(fr.mean()) for fr in read_video(r["video"])]
        return [("frame offsets are exactly the seeded table", lambda m, f: (all(abs(a - c) < 0.3 and abs(b - d) < 0.3 for (a, b), (c, d) in zip(got(m), want)), got(m)), want),
                ("still before and after the 4 frames", lambda m, f: (abs(x(m)[idx(T, 10.8)]) < .2 and abs(x(m)[idx(T, 11.1)]) < .2, [float(x(m)[idx(T, 10.8)]), float(x(m)[idx(T, 11.1)])]), [0, 0])]
    checks, outs = run_tl(wd, "microshake", body, js, ["#mk", "#mb", "#dim"], [RED, BLUE, "#000000"], 0.4, fps, crits, t0=10.77, tol=75)
    lum = [float(fr.mean()) for fr in read_video(outs[0])]
    T = [round(10.77 + i / fps, 6) for i in range(len(lum))]
    drop = 1 - lum[idx(T, 10.9)] / lum[idx(T, 10.8)]
    checks.append(check("dim flash darkens the frame by ~22% on the hit", 0.17 < drop < 0.27, drop, 0.22))
    return checks, outs


def _talk_camera(wd, name, extra_shake):
    """Word-synced camera on a talking plate: origin on the face (705,700 of 1080x1920), start 1.10 -> 1.035 (0.55 s
    expo.out) on hook release, a slow 1.07 push (1.7 s power2.inOut), expo punches 1.12/1.16/1.19 on stressed words."""
    W, H, k = 180, 320, 180 / 1080
    ox, oy = 705 * k, 700 * k
    words = [{"t": 0.4, "w": "hook"}, {"t": 1.2, "w": "a"}, {"t": 2.6, "w": "STRESS1", "s": 1.12}, {"t": 3.6, "w": "b"},
             {"t": 4.4, "w": "STRESS2", "s": 1.16}, {"t": 5.6, "w": "STRESS3", "s": 1.19}]
    (wd / "words.json").write_text(json.dumps(words), encoding="utf-8")
    body = ('<div id="stage" class="a" style="left:0;top:0;width:%dpx;height:%dpx">%s%s</div>'
            % (W, H, box_html("face", ox - 8, oy - 8, 16, 16, RED), box_html("mb", ox + 30, oy + 60, 10, 10, BLUE)))
    js = ("const W=%s; gsap.set('#stage',{transformOrigin:'%spx %spx',scale:1.10});"
          "tl.to('#stage',{scale:1.035,duration:.55,ease:'expo.out'},W[0].t);"
          "tl.to('#stage',{scale:1.07,duration:1.7,ease:'power2.inOut'},0.95);"
          "for(const w of W.filter(w=>w.s)){tl.to('#stage',{scale:w.s,duration:.13,ease:'expo.out'},w.t);"
          "tl.to('#stage',{scale:1.07,duration:.5,ease:'power2.out'},w.t+.35);}" % (json.dumps(words), ox, oy))
    if extra_shake:
        js += ("for(const [d,x,y] of [[0,6,-4],[1/30,-5,3],[2/30,3,-2],[3/30,0,0]]) tl.set('#stage',{x:x*%s,y:y*%s},5.6+d);"
               "tl.to('#stage',{scale:1.0,duration:.6,ease:'power2.inOut'},6.4);" % (k * 3, k * 3))
    dur = 7.2 if extra_shake else 6.4

    def crits(r, T):
        dd = lambda m: D(m, 0, 1) * 1.10
        fx_, fy_ = lambda m: P(m, 0)[0], lambda m: P(m, 0)[1]
        peaks = [(w["t"] + 0.13, w["s"]) for w in words if w.get("s")]
        c = [("punches peak on the stressed words", lambda m, f: (all(abs(dd(m)[idx(T, t)] - s) < 0.01 for t, s in peaks),
                                                                  [float(dd(m)[idx(T, t)]) for t, s in peaks]), [s for _, s in peaks]),
             ("hook release settles 1.10 -> 1.035", lambda m, f: (abs(dd(m)[idx(T, 0.95)] - 1.035) < 0.006, float(dd(m)[idx(T, 0.95)])), 1.035),
             ("face stays put: transform origin on the face (no drift while scaling)",
              lambda m, f: (float(np.nanmax(np.hypot(fx_(m)[:idx(T, 5.5)] - fx_(m)[0], fy_(m)[:idx(T, 5.5)] - fy_(m)[0]))) < 0.4,
                            float(np.nanmax(np.hypot(fx_(m)[:idx(T, 5.5)] - fx_(m)[0], fy_(m)[:idx(T, 5.5)] - fy_(m)[0])))), "<0.4 px"),
             ("one move at a time: scale is flat between ideas", lambda m, f: (abs(dd(m)[idx(T, 3.4)] - dd(m)[idx(T, 3.9)]) < 0.004,
                                                                               float(abs(dd(m)[idx(T, 3.4)] - dd(m)[idx(T, 3.9)]))), "<0.004")]
        if extra_shake:
            c.append(("seeded 4-frame micro shake on the hardest word", lambda m, f: (abs(fx_(m)[idx(T, 5.6)] - fx_(m)[0] - 3) < 0.6,
                                                                                    float(fx_(m)[idx(T, 5.6)] - fx_(m)[0])), 3.0))
            c.append(("scale pull-back reveal at the shot change", lambda m, f: (abs(dd(m)[-1] - 1.0) < 0.006, float(dd(m)[-1])), 1.0))
        return c
    checks, outs = run_tl(wd, name, body, js, ["#face", "#mb"], [RED, BLUE], dur, 30, crits, W=W, H=H)
    return checks, outs + [wd / "words.json"]


@card("CAM-136")
def cam136(task, wd):
    """Word-synced 2D camera on a footage plate (one move per idea, expo punches on stressed words, origin on the face)."""
    return _talk_camera(wd, "wordcam", False)


@card("CAM-173")
def cam173(task, wd):
    """Directed digital camera on a talking clip: hook release, pushes, punches, seeded 4-frame micro-shake, pull-back reveal."""
    return _talk_camera(wd, "directedcam", True)


@card("CAM-100")
def cam100(task, wd):
    """Ken Burns pan: fromTo('#clip .inner',{scale:1.05,xPercent:0},{scale:1.2,xPercent:-12,duration:4,ease:'none'})."""
    body = ('<div id="clip" class="a" style="left:0;top:0;width:320px;height:180px;overflow:hidden"><div class="inner a" '
            'style="left:0;top:0;width:320px;height:180px">%s%s</div></div>' % (box_html("mk", 152, 85, 16, 10, RED), box_html("mb", 194, 64, 12, 12, BLUE)))
    js = "tl.fromTo('#clip .inner',{scale:1.05,xPercent:0},{scale:1.2,xPercent:-12,duration:4,ease:'none'},0);"

    def crits(r, T):
        dd = lambda m: D(m, 0, 1) * 1.05
        x = lambda m: P(m, 0)[0]
        model = [1.05 + 0.15 * t / 4 for t in T]
        shift = lambda m: float(x(m)[-1] - x(m)[0])
        exp_shift = -0.12 * 320 + (160 - 160) + (1.2 - 1.05) * (160 - 160)
        return [("scale 1.05 -> 1.2 linear over 4 s", lambda m, f: (maxerr(dd(m), model) < 0.01, maxerr(dd(m), model)), "<0.01"),
                ("pans left by 12% of the width", lambda m, f: (abs(shift(m) - exp_shift) < 2.5, shift(m)), exp_shift),
                ("linear: half-way pan is half", lambda m, f: (abs((x(m)[len(T) // 2] - x(m)[0]) / shift(m) - 0.5) < 0.05,
                                                               float((x(m)[len(T) // 2] - x(m)[0]) / shift(m))), 0.5)]
    return run_tl(wd, "kenburns", body, js, ["#mk", "#mb"], [RED, BLUE], 4.0, 10, crits)


# ───────────────────────────── virtual-camera / world-wrapper cards (GSAP in Chrome) ─────────────────────────────

GREEN, YEL, MAG, CYAN = "#00ff00", "#ffff00", "#ff00ff", "#00ffff"
expo_out = lambda p: 1.0 if p >= 1 else 1 - 2 ** (-10 * p)
p2io = lambda p: 4 * p ** 3 if p < .5 else 1 - (-2 * p + 2) ** 3 / 2       # GSAP power2 = cubic
p3out = lambda p: 1 - (1 - p) ** 4                                         # GSAP power3 = quartic


def offc(m, k, W=320, H=180):
    x, y = P(m, k)
    return np.hypot(x - W / 2, y - H / 2)


def world(markers, w=320, h=180, extra=""):
    return ('<div id="world" class="a" style="left:0;top:0;width:%dpx;height:%dpx;transform-origin:50%% 50%%">%s%s</div>'
            % (w, h, "".join(box_html(i, x, y, a, b, c) for i, x, y, a, b, c in markers), extra))


@card("CAM-101")
def cam101(task, wd):
    """Crop/reframe with clip-path inset: tl.to('#clip .inner',{clipPath:'inset(8% 12% 6% 10%)',xPercent:-4,duration:1},2)."""
    body = ('<div id="clip" class="a" style="left:0;top:0;width:320px;height:180px"><div class="inner a" '
            'style="left:0;top:0;width:320px;height:180px;background:#00ff00;clip-path:inset(0% 0% 0% 0%)"></div></div>')
    js = "tl.to('#clip .inner',{clipPath:'inset(8% 12% 6% 10%)',xPercent:-4,duration:1},2);"

    def clip(frames):
        for fr in frames:
            v = [float(x) for x in re.findall(r"([\d.]+)%", fr["x"])] or [0, 0, 0, 0]
            t, r_, b, l_ = (v + [0, 0, 0, 0])[:4]
            q = np.array(fr["el"][0]["q"], float)
            lerp2 = lambda u, w: (q[0] * (1 - u) + q[1] * u) * (1 - w) + (q[3] * (1 - u) + q[2] * u) * w
            fr["el"][0]["q"] = [list(lerp2(l_ / 100, t / 100)), list(lerp2(1 - r_ / 100, t / 100)),
                                list(lerp2(1 - r_ / 100, 1 - b / 100)), list(lerp2(l_ / 100, 1 - b / 100))]

    def crits(r, T):
        box = lambda m: (m[-1][0]["x0"], m[-1][0]["y0"], m[-1][0]["x1"] + 1, m[-1][0]["y1"] + 1)
        want = (0.10 * 320 - 12.8, 0.08 * 180, 320 * 0.88 - 12.8, 180 * 0.94)
        return [("final visible box = inset(8% 12% 6% 10%) shifted by xPercent -4",
                 lambda m, f: (max(abs(a - b) for a, b in zip(box(m), want)) <= 1.5, list(box(m))), list(want)),
                ("frame unchanged before the reframe at 2 s", lambda m, f: (m[idx(T, 1.9)][0]["area"] > 0.99 * 320 * 180, m[idx(T, 1.9)][0]["area"]), "full frame")]
    return run_tl(wd, "clipinset", body, js, [".inner"], [GREEN], 3.2, 10, crits,
                  extra_js="(t)=>getComputedStyle(document.querySelector('.inner')).clipPath", mutate=clip)


@card("CAM-103")
def cam103(task, wd):
    """Coordinate target zoom: outer wrapper scales around 50% 50%, inner counter-translates T = -offset; target <= 88% of canvas."""
    tx, ty, tw, th = 230, 40, 30, 20
    ox, oy = tx + tw / 2 - 160, ty + th / 2 - 90
    S = round(min(4.0, 0.88 * 320 / tw, 0.88 * 180 / th), 3)
    body = ('<div id="outer" class="a" style="left:0;top:0;width:320px;height:180px;transform-origin:50%% 50%%"><div id="inner" class="a" '
            'style="left:0;top:0;width:320px;height:180px">%s%s</div></div>' % (box_html("tgt", tx, ty, tw, th, RED), box_html("oth", 40, 120, 20, 20, BLUE)))
    js = ("tl.fromTo('#inner',{x:0,y:0},{x:%s,y:%s,duration:1.2,ease:'power2.inOut'},0.2);"
          "tl.fromTo('#outer',{scale:1},{scale:%s,duration:1.2,ease:'power2.inOut'},0.2);" % (-ox, -oy, S))

    def crits(r, T):
        return [("target lands on the canvas centre at peak", lambda m, f: (float(offc(m, 0)[-1]) < 1.0, float(offc(m, 0)[-1])), "<1 px"),
                ("target scaled by S and <= 88% of the canvas", lambda m, f: (abs(SC(m, 0)[-1] - S) < 0.05 * S and (m[-1][0]["x1"] - m[-1][0]["x0"]) <= 0.88 * 320,
                                                                              [float(SC(m, 0)[-1]), m[-1][0]["x1"] - m[-1][0]["x0"]]), [S, "<=281"]),
                ("starts off-centre (non-centred element)", lambda m, f: (float(offc(m, 0)[0]) > 50, float(offc(m, 0)[0])), ">50")]
    return run_tl(wd, "targetzoom", body, js, ["#tgt", "#oth"], [RED, BLUE], 1.6, 15, crits)


@card("CAM-104")
def cam104(task, wd):
    """Camera tracks a typing cursor: static framing, then the world moves (power2.inOut) to keep the cursor in view;
    the caret blinks with steps(1) yoyo."""
    pad = 0.08 * 320
    body = world([("cur", 20, 80, 4, 14, RED), ("w0", 300, 110, 6, 6, BLUE), ("w1", 600, 110, 6, 6, GREEN)], 900, 180)
    js = ("const cps=25, x0=20, adv=6; const n=(t)=>Math.max(0,Math.floor((t-0.3)*cps)); "
          "tl.to('#cur',{opacity:0,duration:.25,ease:'steps(1)',yoyo:true,repeat:-1},0);"
          "window.camAt=(t)=>{tl.seek(t,false); const cx=x0+adv*Math.min(n(t),100); gsap.set('#cur',{x:cx-x0});"
          "let wx=0; for(let k=1;k<=12;k++){const t1=k*0.5; const c=x0+adv*Math.min(n(t1+0.5),100); const goal=Math.min(0,-(c-(320-%s-40)));"
          " const prev=(k===1?0:window.__g[k-1]); window.__g=window.__g||{}; window.__g[k]=Math.min(prev,goal);"
          " if(t>=t1) wx=prev+(window.__g[k]-prev)*Math.min(1,(t-t1)/0.5<0?0:(t-t1)/0.5<1?(p=>p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2)((t-t1)/0.5):1);}"
          " gsap.set('#world',{x:wx}); };" % pad)

    def crits(r, T):
        cx = lambda m: np.array([v[0]["cx"] if v[0] else np.nan for v in m])
        w0 = lambda m: P(m, 1)[0]
        w1 = lambda m: P(m, 2)[0]
        return [("the world moved left > 150 px to follow the cursor (far world marker came into view)",
                 lambda m, f: (bool(np.isfinite(w1(m)[-1])) and float(600 + 3 - w1(m)[-1]) > 150, float(600 + 3 - w1(m)[-1]) if np.isfinite(w1(m)[-1]) else None), ">150"),
                ("phase 1 static framing (world still while the cursor is far from the edge)", lambda m, f: (abs(w0(m)[idx(T, 1.0)] - w0(m)[0]) < 0.5, float(w0(m)[idx(T, 1.0)] - w0(m)[0])), 0),
                ("cursor never leaves the viewport (pad respected)", lambda m, f: (bool(np.nanmax(cx(m)) <= 320 - 0.5 * pad), float(np.nanmax(cx(m)))), "<=%.0f" % (320 - 0.5 * pad)),
                ("caret blink is binary (steps(1))", lambda m, f: (all(min(abs(fr["el"][0]["o"]), abs(1 - fr["el"][0]["o"])) < 1e-6 for fr in f),
                                                                  sorted(set(round(fr["el"][0]["o"], 3) for fr in f))), [0, 1])]
    return run_tl(wd, "cursorcam", body, js, ["#cur", "#w0", "#w1"], [RED, BLUE, GREEN], 6.0, 10, crits)


@card("CAM-105")
def cam105(task, wd):
    """Multi-phase camera: pull-back 1->0.85, focus hold, push 0.85->1.3, plus a continuous drift (ease none) over the total."""
    body = '<div id="drift" class="a" style="left:0;top:0;width:320px;height:180px">%s</div>' % STAGE
    js = ("tl.fromTo('#stage',{scale:1},{scale:.85,duration:1,ease:'power2.inOut'},0);"
          "tl.to('#stage',{scale:1.3,duration:1.2,ease:'power2.inOut'},1.6);"
          "tl.fromTo('#drift',{x:0},{x:-20,duration:3,ease:'none'},0);")

    def crits(r, T):
        dd = lambda m: D(m, 0, 1)
        x = lambda m: P(m, 0)[0] - P(m, 0)[0][0]
        return [("phase ends: 0.85 after the pull-back, 1.3 after the push", lambda m, f: (abs(dd(m)[idx(T, 1.3)] - .85) < .006 and abs(dd(m)[-1] - 1.3) < .008,
                                                                                           [float(dd(m)[idx(T, 1.3)]), float(dd(m)[-1])]), [.85, 1.3]),
                ("focus hold between the phases", lambda m, f: (abs(dd(m)[idx(T, 1.1)] - dd(m)[idx(T, 1.55)]) < .003, float(dd(m)[idx(T, 1.55)])), .85),
                ("drift runs linearly over the whole composition", lambda m, f: (float(np.abs(x(m) + 20 * np.array(T) / 3).max()) < 0.8 + 0.3,
                                                                                 float(np.abs(x(m) + 20 * np.array(T) / 3).max())), "<1.1 px")]
    return run_tl(wd, "multiphase", body, js, ["#mk", "#mb"], [RED, BLUE], 3.0, 15, crits)


@card("CAM-106")
def cam106(task, wd):
    """Virtual camera via one .world wrapper: translate(x,y) scale(S) with counter-offset T = -offset x S (focus-lock), 1.12x over 2.5 s."""
    ox, oy = 70, -35
    body = world([("tgt", 160 + ox - 8, 90 + oy - 6, 16, 12, RED), ("oth", 150, 100, 14, 14, BLUE)])
    js = ("window.camAt=(t)=>{const a=Math.min(1,Math.max(0,t/1.0)), e=a<.5?2*a*a:1-Math.pow(-2*a+2,2)/2;"
          "const b=Math.min(1,Math.max(0,(t-1.0)/2.5)), S=1+0.12*(b<.5?2*b*b:1-Math.pow(-2*b+2,2)/2);"
          "gsap.set('#world',{x:-(%s)*S*(t<1?e:1), y:-(%s)*S*(t<1?e:1), scale:S});};" % (ox, oy))

    def crits(r, T):
        lock = lambda m: float(np.nanmax(offc(m, 0)[idx(T, 1.0):]))
        return [("focus-lock: target stays on centre while zooming (T = -offset x S)", lambda m, f: (lock(m) < 0.5, lock(m)), "<0.5 px"),
                ("zoom 1.12 at the end (comfortable 10-15% range)", lambda m, f: (abs(SC(m, 0)[-1] - 1.12) < 0.022, float(SC(m, 0)[-1])), 1.12),
                ("other content scales away from the locked point", lambda m, f: (float(offc(m, 1)[-1] / offc(m, 1)[idx(T, 1.0)]) > 1.1,
                                                                                  float(offc(m, 1)[-1] / offc(m, 1)[idx(T, 1.0)])), ">1.1")]
    return run_tl(wd, "worldcam", body, js, ["#tgt", "#oth"], [RED, BLUE], 3.6, 10, crits)


@card("CAM-107")
def cam107(task, wd):
    """Depth-of-field rack focus: filter blur(var(--dof)) on out-of-focus layers; one pull then a two-plane swap."""
    css = ".dof{filter:blur(var(--dof,0px))}"
    body = box_html("front", 60, 60, 50, 50, RED, "--dof:0px") .replace('class="a"', 'class="a dof"') + \
        box_html("back", 200, 60, 50, 50, BLUE, "--dof:0px").replace('class="a"', 'class="a dof"')
    js = ("tl.to('#back',{'--dof':'8px',duration:.6,ease:'power2.inOut'},0.4);"
          "tl.to('#back',{'--dof':'0px',duration:.6,ease:'power2.inOut'},1.6);tl.to('#front',{'--dof':'8px',duration:.6,ease:'power2.inOut'},1.6);")

    def crits(r, T):
        v = read_video(r["video"]) if "vv" not in r else r["vv"]
        r["vv"] = v
        sf = lambda m, i, k: sharp(v[i] if m is r["meas"] else read_video(r["input"])[i], hex2rgb(k))
        return [("after the pull the back layer is soft and the front sharp", lambda m, f: (sf(m, idx(T, 1.2), BLUE) < 0.3 and sf(m, idx(T, 1.2), RED) > 0.9,
                                                                                             [sf(m, idx(T, 1.2), BLUE), sf(m, idx(T, 1.2), RED)]), ["<0.3", ">0.9"]),
                ("two-plane swap: front soft, back sharp at the end", lambda m, f: (sf(m, len(T) - 1, RED) < 0.3 and sf(m, len(T) - 1, BLUE) > 0.9,
                                                                                    [sf(m, len(T) - 1, RED), sf(m, len(T) - 1, BLUE)]), ["<0.3", ">0.9"]),
                ("blur value comes from the --dof variable (browser-computed)", lambda m, f: (abs(f[idx(T, 1.2)]["el"][1]["b"] - 8) < 0.01, f[idx(T, 1.2)]["el"][1]["b"]), 8)]
    return run_tl(wd, "dofrack", body, js, ["#front", "#back"], [RED, BLUE], 2.4, 10, crits, css=css)


@card("CAM-108")
def cam108(task, wd):
    """Center-outward expansion: one driver p; each element x = targetX * p, y = targetY * p (xPercent/yPercent -50 centring)."""
    tg = [(-110, -50), (110, -50), (-110, 50), (110, 50), (0, -65), (0, 65)]
    cols = [RED, BLUE, GREEN, YEL, MAG, CYAN]
    body = "".join('<div id="e%d" class="a" data-target-x="%d" data-target-y="%d" style="left:160px;top:90px;width:20px;height:14px;background:%s"></div>'
                   % (i, x, y, c) for i, ((x, y), c) in enumerate(zip(tg, cols)))
    js = ("const els=[...document.querySelectorAll('[data-target-x]')]; gsap.set(els,{xPercent:-50,yPercent:-50});"
          "const d={p:0}; tl.to(d,{p:1,duration:1.2,ease:'power3.out',onUpdate:()=>els.forEach(e=>gsap.set(e,{x:+e.dataset.targetX*d.p,y:+e.dataset.targetY*d.p}))},0.2);"
          "window.camAt=(t)=>{tl.seek(t,false); els.forEach(e=>gsap.set(e,{x:+e.dataset.targetX*d.p,y:+e.dataset.targetY*d.p}));};")

    def crits(r, T):
        def prog(m, i):
            return [(P(m, k)[0][i] - 160) / tg[k][0] for k in range(6) if tg[k][0]] + [(P(m, k)[1][i] - 90) / tg[k][1] for k in range(6)]
        j = idx(T, 0.5)
        return [("every element reaches its CSS target", lambda m, f: (max(abs(P(m, k)[0][-1] - 160 - tg[k][0]) + abs(P(m, k)[1][-1] - 90 - tg[k][1]) for k in range(6)) < 1.0,
                                                                       max(abs(P(m, k)[0][-1] - 160 - tg[k][0]) + abs(P(m, k)[1][-1] - 90 - tg[k][1]) for k in range(6))), "<1 px"),
                ("starts clustered on the centre (xPercent -50 bakes centring; browser quads)",
                 lambda m, f: (max(float(np.hypot(*(np.array(e["q"]).mean(0) - [160, 90]))) for e in f[0]["el"]) < 0.01,
                               max(float(np.hypot(*(np.array(e["q"]).mean(0) - [160, 90]))) for e in f[0]["el"])), "<0.01"),
                ("one driver: all elements share the same progress", lambda m, f: (float(np.ptp(prog(m, j))) < 0.04, [round(float(v), 3) for v in prog(m, j)]), "spread<0.04"),
                ("progress follows power3.out", lambda m, f: (abs(float(np.mean(prog(m, j)) - p3out((T[j] - .2) / 1.2))) < 0.02, float(np.mean(prog(m, j)))), p3out((T[j] - .2) / 1.2))]
    return run_tl(wd, "outward", body, js, ["#e%d" % i for i in range(6)], cols, 1.6, 15, crits)


@card("CAM-109")
def cam109(task, wd):
    """Split tilt cards: opposing rotateY tilts (perspective 1600), slide in from their sides (power3.out), float in anti-phase (sine, PI offset)."""
    body = ('<div id="scene" class="a" style="left:0;top:0;width:320px;height:180px;perspective:1600px">%s%s</div>'
            % (box_html("cA", 40, 45, 100, 90, RED), box_html("cB", 180, 45, 100, 90, BLUE)))
    js = ("gsap.set('#cA',{rotationY:24});gsap.set('#cB',{rotationY:-24});"
          "tl.fromTo('#cA',{x:-200},{x:0,duration:.8,ease:'power3.out'},0);tl.fromTo('#cB',{x:200},{x:0,duration:.8,ease:'power3.out'},0);"
          "window.camAt=(t)=>{tl.seek(t,false); if(t>.8){gsap.set('#cA',{y:6*Math.sin(2*Math.PI*(t-.8)/1.6)});gsap.set('#cB',{y:6*Math.sin(2*Math.PI*(t-.8)/1.6+Math.PI)});}};")

    def crits(r, T):
        def edges(fr, k):
            q = np.array(fr["el"][k]["q"])
            return q[3][1] - q[0][1], q[2][1] - q[1][1]          # left edge height, right edge height
        ya, yb = lambda m: P(m, 0)[1], lambda m: P(m, 1)[1]
        j = idx(T, 0.8)
        i2 = idx(T, 0.2)
        return [("cards slide in from opposite sides to mirrored places", lambda m, f: (P(m, 0)[0][i2] < P(m, 0)[0][j] - 20 and P(m, 1)[0][i2] > P(m, 1)[0][j] + 20 and abs(P(m, 0)[0][j] + P(m, 1)[0][j] - 320) < 2,
                                                                                    [float(P(m, 0)[0][i2]), float(P(m, 1)[0][i2]), float(P(m, 0)[0][j] + P(m, 1)[0][j])]), "A from left, B from right, sum=320"),
                ("opposing rotateY: mirrored foreshortening", lambda m, f: ((lambda a, b: (a[0] - a[1]) * (b[0] - b[1]) < 0)(edges(f[j], 0), edges(f[j], 1)), [edges(f[j], 0), edges(f[j], 1)]), "opposite"),
                ("anti-phase float (PI offset)", lambda m, f: (float(np.corrcoef(ya(m)[j:], yb(m)[j:])[0, 1]) < -0.95, float(np.corrcoef(ya(m)[j:], yb(m)[j:])[0, 1])), "<-0.95")]
    return run_tl(wd, "tiltcards", body, js, ["#cA", "#cB"], [RED, BLUE], 2.4, 15, crits)


# ───────────────────────────── keyed world cameras (focus x, y, scale) ─────────────────────────────

KEYCAM_JS = r"""
const EZJ={cubic:p=>p<.5?4*p*p*p:1-Math.pow(-2*p+2,3)/2, sine:p=>-(Math.cos(Math.PI*p)-1)/2, linear:p=>p,
  quad:p=>p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2, expoOut:p=>p>=1?1:1-Math.pow(2,-10*p), smooth:p=>p*p*(3-2*p)};
function keyCam(sel, keys, ez, logS, W, H){ W=W||320; H=H||180; return (t)=>{ let i=0; while(i<keys.length-2 && t>keys[i+1][0]) i++;
  const a=keys[i], b=keys[i+1], u=Math.min(1,Math.max(0,(t-a[0])/Math.max(1e-6,b[0]-a[0]))), e=EZJ[ez](u);
  const fx=a[1]+(b[1]-a[1])*e, fy=a[2]+(b[2]-a[2])*e, s=logS?Math.exp(Math.log(a[3])+(Math.log(b[3])-Math.log(a[3]))*e):a[3]+(b[3]-a[3])*e;
  gsap.set(sel,{transformOrigin:'0 0', x:W/2-s*fx, y:H/2-s*fy, scale:s}); return s; }; }
"""


def holds(keys):
    """(t_mid, fx, fy, s) of every hold (two consecutive equal keys)."""
    return [((a[0] + b[0]) / 2, a[1], a[2], a[3]) for a, b in zip(keys, keys[1:]) if a[1:] == b[1:] and b[0] > a[0]]


def keycam_card(wd, name, markers, keys, ez, logS, dur, fps, extra_crits=None, ww=320, wh=180, extra_html="", extra_js=""):
    """markers: [(id, x, y, w, h, color)] in world px; each hold must centre its focus marker (the marker whose centre
    is the hold's focus point) at the hold's scale."""
    body = world(markers, ww, wh, extra_html)
    js = KEYCAM_JS + "const cam=keyCam('#world',%s,'%s',%s); window.camAt=(t)=>{tl.seek(t,false); cam(t); %s};" % (
        json.dumps(keys), ez, "true" if logS else "false", extra_js)
    sels = ["#" + m[0] for m in markers]
    cols = [m[5] for m in markers]
    centre = {(m[1] + m[3] / 2, m[2] + m[4] / 2): i for i, m in enumerate(markers)}

    def crits(r, T):
        hl = [(t, centre.get((fx, fy)), s) for t, fx, fy, s in holds(keys)]
        hl = [h for h in hl if h[1] is not None]
        sz0 = {i: math.sqrt(markers[i][3] * markers[i][4]) for _, i, _ in hl}

        def framed(m):
            res = []
            for t, i, s in hl:
                b = m[idx(T, t)][i]
                res.append(None if b is None else (round(math.hypot(b["cx"] - 160, b["cy"] - 90), 2), round(math.sqrt(b["area"]) / sz0[i], 3)))
            return res
        ok = lambda fr: all(v is not None and v[0] < 1.0 and abs(v[1] - s) < 0.04 * s + 0.06 for v, (_, _, s) in zip(fr, hl))
        c = [("each hold frames its target on centre at the keyed scale", lambda m, f: (ok(framed(m)), framed(m)), [("<1px", s) for _, _, s in hl])]
        return c + (extra_crits(r, T) if extra_crits else [])
    return run_tl(wd, name, body, js, sels, cols, dur, fps, crits)


def no_cut(f, k):
    """A cut is a one-frame jump: the track's largest acceleration is about its largest step. Smooth camera moves keep
    max |d2x| well below max |dx|. Returns the ratio."""
    c = np.array([np.array(fr["el"][k]["q"]).mean(0) for fr in f])
    d1 = np.linalg.norm(np.diff(c, axis=0), axis=1)
    d2 = np.linalg.norm(np.diff(c, 2, axis=0), axis=1)
    return float(d2.max() / max(1e-9, d1.max()))


def _cam_scale(fr, k=0, base=None):
    q = np.array(fr["el"][k]["q"])
    return float(np.hypot(*(q[1] - q[0]))) / base


@card("CAM-110")
def cam110(task, wd):
    """Blueprint spatial pan stations: labelled stations on one oversized canvas, one virtual camera travels between them
    (power-style inOut), settles on the last; 8 s total (card: 7-10 s)."""
    st = [("s%d" % i, 160 + 320 * i - 10, 80, 20, 20, c) for i, c in enumerate([RED, BLUE, GREEN, YEL])]
    keys = [[0, 160, 90, 1], [1.0, 160, 90, 1], [2.2, 480, 90, 1], [3.2, 480, 90, 1], [4.4, 800, 90, 1], [5.4, 800, 90, 1],
            [6.6, 1120, 90, 1], [8.0, 1120, 90, 1]]

    def extra(r, T):
        x3 = lambda m: P(m, 3)[0]
        return [("settles on the last station and stays still", lambda m, f: (float(np.nanmax(np.abs(x3(m)[idx(T, 6.7):] - 160))) < 0.6,
                                                                              float(np.nanmax(np.abs(x3(m)[idx(T, 6.7):] - 160)))), "<0.6 px"),
                ("duration within the blueprint's 7-10 s", lambda m, f: (7 <= T[-1] <= 10, T[-1]), "7-10")]
    return keycam_card(wd, "stations", st, keys, "cubic", False, 8.0, 5, extra, ww=1300)


@card("CAM-111")
def cam111(task, wd):
    """Blueprint camera journey: dive onto the action (button), the click lands, swoop to the result; one world, ~6 s."""
    mk = [("btn", 230, 40, 20, 12, RED), ("res", 50, 130, 30, 20, BLUE), ("ctx", 150, 85, 10, 10, GREEN)]
    keys = [[0, 160, 90, 1], [0.4, 160, 90, 1], [1.6, 240, 46, 3], [2.6, 240, 46, 3], [4.0, 65, 140, 2.2], [6.0, 65, 140, 2.2]]
    xj = ("const k=Math.max(0,1-Math.abs(t-2.4)/0.15); gsap.set('#btn',{scale:1-0.15*k, transformOrigin:'50% 50%'});")

    def extra(r, T):
        return [("click pulse lands while the button is held (scale dips 15%)", lambda m, f: (abs(_cam_scale(f[idx(T, 2.4)], 0, 20) / 3 - 0.85) < 0.02,
                                                                                               _cam_scale(f[idx(T, 2.4)], 0, 20) / 3), 0.85),
                ("the journey is continuous (no cut)", lambda m, f: (no_cut(f, 1) < 0.6, no_cut(f, 1)), "<0.6")]
    return keycam_card(wd, "journey", mk, keys, "cubic", True, 6.0, 20, extra, extra_js=xj)


@card("CAM-112")
def cam112(task, wd):
    """Blueprint zoom-out workspace reveal: open tight (4x) on a detail, a micro-action in close-up, then ONE continuous
    decelerating zoom-out (expo.out in log scale) reveals the whole workspace."""
    mk = [("det", 150, 85, 20, 10, RED), ("act", 150, 97, 6, 4, CYAN)] + [("c%d" % i, x, y, 10, 10, c) for i, (x, y, c) in
                                             enumerate([(10, 10, BLUE), (300, 10, GREEN), (10, 160, YEL), (300, 160, MAG)])]
    keys = [[0, 160, 90, 4], [1.6, 160, 90, 4], [5.6, 160, 90, 1], [6.4, 160, 90, 1]]
    xj = "gsap.set('#act',{x: t>0.6&&t<1.4 ? 3*Math.sin((t-0.6)/0.8*Math.PI) : 0});"

    def extra(r, T):
        def sc(f):
            return np.array([_cam_scale(fr, 0, 20) for fr in f])
        a, b = idx(T, 1.6), idx(T, 5.6)
        return [("whole workspace hidden at start, all four corners visible at the end",
                 lambda m, f: (all(m[0][k] is None for k in range(2, 6)) and all(m[-1][k] is not None for k in range(2, 6)),
                               [m[-1][k] is not None for k in range(2, 6)]), "4 visible"),
                ("one continuous zoom-out: scale strictly decreasing", lambda m, f: (bool((np.diff(sc(f)[a:b + 1]) < 0).all()), float(np.diff(sc(f)[a:b + 1]).max())), "<0"),
                ("decelerating: log-speed falls through the reveal", lambda m, f: (abs(np.diff(np.log(sc(f)[a:b + 1])))[0] > 3 * abs(np.diff(np.log(sc(f)[a:b + 1])))[-1],
                                                                                   [float(abs(np.diff(np.log(sc(f)[a:b + 1])))[0]), float(abs(np.diff(np.log(sc(f)[a:b + 1])))[-1])]), "first > 3 x last"),
                ("micro-action in close-up before the reveal", lambda m, f: (abs(P(m, 1)[0][idx(T, 1.0)] - P(m, 1)[0][0]) > 6, float(P(m, 1)[0][idx(T, 1.0)] - P(m, 1)[0][0])), ">6 px")]
    return keycam_card(wd, "zoomreveal", mk, keys, "expoOut", True, 6.4, 10, extra, extra_js=xj)


@card("CAM-201")
def cam201(task, wd):
    """Lesson camera tour: key camera (x, y, zoom 1.0-2.2) to each element as it is drawn, ~1 s ease-in-out moves,
    final pull-out revealing the full board."""
    els = [("e0", 40, 30, 30, 20, RED), ("e1", 230, 40, 30, 20, BLUE), ("e2", 60, 120, 30, 20, GREEN), ("e3", 220, 125, 30, 20, YEL)]
    keys = [[0, 55, 40, 2.2], [1.2, 55, 40, 2.2], [2.2, 245, 50, 1.8], [3.4, 245, 50, 1.8], [4.4, 75, 130, 2.0], [5.6, 75, 130, 2.0],
            [6.6, 235, 135, 2.2], [7.8, 235, 135, 2.2], [8.8, 160, 90, 1.0], [9.6, 160, 90, 1.0]]
    xj = "".join("gsap.set('#e%d',{opacity:Math.min(1,Math.max(0,(t-%s)/0.4))});" % (i, d) for i, d in enumerate([0.1, 2.3, 4.5, 6.7]))

    def extra(r, T):
        return [("every element is drawn while the camera frames it", lambda m, f: (all(f[idx(T, d + 0.6)]["el"][i]["o"] == 1 for i, d in enumerate([0.1, 2.3, 4.5, 6.7])), True), True),
                ("final pull-out shows the whole board at zoom 1", lambda m, f: (all(m[-1][k] is not None for k in range(4)) and abs(_cam_scale(f[-1], 0, 30) - 1) < 1e-3,
                                                                                 _cam_scale(f[-1], 0, 30)), 1.0)]
    return keycam_card(wd, "lessontour", els, keys, "cubic", False, 9.6, 5, extra, extra_js=xj)


@card("CAM-202")
def cam202(task, wd):
    """One-take world strip camera: x/y/zoom keyframes with inOut cubic, moving ONLY in sentence pauses; shot sizes
    wide 0.9, medium 1.25, close 1.55; moves 0.8-1.5 s."""
    sent = [(0.0, 1.8), (2.8, 4.6), (5.6, 7.4)]
    (wd / "sentences.json").write_text(json.dumps(sent), encoding="utf-8")
    zs = [("z0", 150, 80, 20, 20, RED), ("z1", 550, 80, 20, 20, BLUE), ("z2", 950, 80, 20, 20, GREEN)]
    keys = [[0, 160, 90, .9], [1.8, 160, 90, .9], [2.8, 560, 90, 1.25], [4.6, 560, 90, 1.25], [5.6, 960, 90, 1.55], [7.4, 960, 90, 1.55]]

    def extra(r, T):
        def moving(f):
            sc = np.array([_cam_scale(fr, 0, 20) for fr in f])
            x = np.array([np.array(fr["el"][0]["q"]).mean(0)[0] for fr in f])
            return np.abs(np.diff(sc)) + np.abs(np.diff(x)) > 1e-6
        def in_sent(i):
            t = (T[i] + T[i + 1]) / 2
            return any(a <= t <= b for a, b in sent)
        return [("camera is still during every sentence", lambda m, f: (not any(mv and in_sent(i) for i, mv in enumerate(moving(f))),
                                                                     sum(1 for i, mv in enumerate(moving(f)) if mv and in_sent(i))), 0),
                ("it moves in the pauses", lambda m, f: (sum(1 for i, mv in enumerate(moving(f)) if mv) > 4, sum(1 for i, mv in enumerate(moving(f)) if mv)), ">4"),
                ("shot sizes wide/medium/close", lambda m, f: ([round(_cam_scale(f[idx(T, t)], 0, 20), 2) for t in (1, 3.6, 6.5)] == [0.9, 1.25, 1.55],
                                                               [round(_cam_scale(f[idx(T, t)], 0, 20), 2) for t in (1, 3.6, 6.5)]), [0.9, 1.25, 1.55])]
    checks, outs = keycam_card(wd, "worldstrip", zs, keys, "cubic", False, 7.4, 10, extra, ww=1100)
    return checks, outs + [wd / "sentences.json"]


@card("CAM-221")
def cam221(task, wd):
    """World-layer camera: focusX, focusY and log(scale) keyframes interpolated in log space (uniform-feeling zoom 1x-6x),
    ease-in-out cubic 0.6-1.2 s per move, never two moves at once."""
    mk = [("a", 150, 85, 20, 10, RED), ("b", 254, 46, 12, 8, BLUE), ("c", 60, 140, 8, 8, GREEN)]
    keys = [[0, 160, 90, 1], [0.5, 160, 90, 1], [1.6, 260, 50, 6], [2.4, 260, 50, 6], [3.4, 64, 144, 2.5], [4.2, 64, 144, 2.5]]

    def extra(r, T):
        def mid(f):
            j = idx(T, 1.05)
            s = _cam_scale(f[j], 0, 20)
            return math.log(s), math.log(6) * cubic_io((T[j] - 0.5) / 1.1)
        return [("mid-move scale is interpolated in log space", lambda m, f: (abs(mid(f)[0] - mid(f)[1]) < 1e-3 and abs(math.exp(mid(f)[0]) - (1 + 5 * cubic_io((T[idx(T, 1.05)] - .5) / 1.1))) > 0.3,
                                                                             [math.exp(mid(f)[0]), math.exp(mid(f)[1])]), "log model, not linear"),
                ("moves never overlap: scale and focus are both still at each hold", lambda m, f: (abs(_cam_scale(f[idx(T, 1.7)], 0, 20) - _cam_scale(f[idx(T, 2.3)], 0, 20)) < 1e-6, True), True)]
    return keycam_card(wd, "worldlayer", mk, keys, "cubic", True, 4.2, 10, extra)


@card("CAM-269")
def cam269(task, wd):
    """Virtual camera over one big UI canvas: animate translate/scale to frame each step instead of cutting
    (moves 1-1.5 s easeInOutCubic, zoom 1.0-1.8)."""
    mk = [("st%d" % i, x, y, 24, 16, c) for i, (x, y, c) in enumerate([(90, 60, RED), (400, 70, BLUE), (420, 300, GREEN), (100, 290, YEL)])]
    ctr = lambda i: (mk[i][1] + 12, mk[i][2] + 8)
    zz = [1.8, 1.4, 1.6, 1.0]
    keys, t = [], 0.0
    for i in range(4):
        keys += [[t, ctr(i)[0], ctr(i)[1], zz[i]], [t + 0.8, ctr(i)[0], ctr(i)[1], zz[i]]]
        t += 0.8 + 1.2
    keys[-1][0] = keys[-2][0] + 0.8

    def extra(r, T):
        return [("no cuts: camera motion is continuous", lambda m, f: (no_cut(f, 0) < 0.6, no_cut(f, 0)), "<0.6")]
    return keycam_card(wd, "uicanvas", mk, keys, "cubic", False, keys[-1][0], 20, extra, ww=520, wh=340)


@card("CAM-271")
def cam271(task, wd):
    """Push into the screen bookend: scale the camera from the room to the monitor content and back (end = start)."""
    mk = [("mon", 200, 50, 48, 27, BLUE), ("txt", 220, 60, 8, 6, RED), ("lamp", 40, 120, 14, 30, GREEN)]
    keys = [[0, 160, 90, 1], [0.4, 160, 90, 1], [1.4, 224, 63.5, 6], [2.6, 224, 63.5, 6], [3.6, 160, 90, 1], [4.0, 160, 90, 1]]

    def extra(r, T):
        v = read_video(r["video"])
        dif = float(np.abs(v[0] - v[-1]).max())
        return [("bookend: the last frame equals the first", lambda m, f: (dif < 2, dif), "<2"),
                ("monitor content fills the frame at the peak", lambda m, f: (m[idx(T, 2.0)][0] is not None and (m[idx(T, 2.0)][0]["x1"] - m[idx(T, 2.0)][0]["x0"]) >= 0.85 * 320,
                                                                            m[idx(T, 2.0)][0]["x1"] - m[idx(T, 2.0)][0]["x0"] if m[idx(T, 2.0)][0] else None), ">=272")]
    return keycam_card(wd, "bookend", mk, keys, "cubic", True, 4.0, 10, extra)


@card("CAM-264")
def cam264(task, wd):
    """Push-in terminal typewriter: scale the scene ~2.5x toward the monitor (700 ms easeInOut), type a green mono line
    at 40 ms/char with a block cursor, then pull back."""
    mk = [("mon", 180, 40, 100, 56, BLUE), ("cur", 186, 66, 3, 5, GREEN)]
    keys = [[0, 160, 90, 1], [0.3, 160, 90, 1], [1.0, 230, 68, 2.5], [2.8, 230, 68, 2.5], [3.5, 160, 90, 1], [3.8, 160, 90, 1]]
    xj = "gsap.set('#cur',{x: 3.2*Math.min(25,Math.max(0,Math.floor((t-1.0)/0.04)))});"

    def extra(r, T):
        cx = lambda m: P(m, 1)[0]
        a, b = idx(T, 1.2), idx(T, 1.8)
        rate = lambda m: (cx(m)[b] - cx(m)[a]) / (T[b] - T[a])
        return [("cursor advances one char per 40 ms at 2.5x (3.2 px x 2.5 / 0.04 s)", lambda m, f: (abs(rate(m) - 3.2 * 2.5 / 0.04) < 0.12 * 200, float(rate(m))), 200),
                ("pull back to the room at the end", lambda m, f: (abs(_cam_scale(f[-1], 0, 100) - 1) < 1e-6, _cam_scale(f[-1], 0, 100)), 1)]
    return keycam_card(wd, "termpush", mk, keys, "quad", False, 3.8, 25, extra, extra_js=xj)


# ───────────────────────────── assemblies, reveals, pushes and parallax planes ─────────────────────────────

COLS6 = [RED, BLUE, GREEN, YEL, MAG, CYAN]


@card("CAM-113")
def cam113(task, wd):
    """Blueprint grid card assemble: N tiles self-assemble in a staggered cascade into a 3x2 grid (power3.out 0.6 s, 0.12 s stagger)."""
    grid = [(40 + 90 * (i % 3), 30 + 70 * (i // 3)) for i in range(6)]
    scat = [(-60, -40), (330, 10), (150, 200), (-50, 160), (340, 170), (150, -60)]
    body = "".join(box_html("g%d" % i, x, y, 60, 50, c) for i, ((x, y), c) in enumerate(zip(grid, COLS6)))
    js = "".join("tl.fromTo('#g%d',{x:%d,y:%d,rotation:%d},{x:0,y:0,rotation:0,duration:.6,ease:'power3.out'},%s);"
                 % (i, sx - gx, sy - gy, (-1) ** i * 10, 0.2 + 0.12 * i) for i, ((gx, gy), (sx, sy)) in enumerate(zip(grid, scat)))

    def crits(r, T):
        arrive = lambda f, i: next((T[j] for j in range(len(T)) if math.hypot(*(np.array(f[j]["el"][i]["q"]).mean(0) - np.array(grid[i]) - [30, 25])) < 2), None)
        return [("every tile lands on its grid cell", lambda m, f: (max(math.hypot(P(m, i)[0][-1] - grid[i][0] - 30, P(m, i)[1][-1] - grid[i][1] - 25) for i in range(6)) < 1.0,
                                                                    max(math.hypot(P(m, i)[0][-1] - grid[i][0] - 30, P(m, i)[1][-1] - grid[i][1] - 25) for i in range(6))), "<1 px"),
                ("staggered cascade: arrivals in order, ~0.12 s apart", lambda m, f: (all(abs(arrive(f, i + 1) - arrive(f, i) - 0.12) < 0.05 for i in range(5)),
                                                                                      [arrive(f, i) for i in range(6)]), "+0.12 s each")]
    return run_tl(wd, "gridassemble", body, js, ["#g%d" % i for i in range(6)], COLS6, 1.8, 25, crits)


@card("CAM-114")
def cam114(task, wd):
    """Blueprint comparison split: two equal items enter from opposite wings with a mirrored 3D book tilt, then capsule
    badges pop with a spring at the inner edges."""
    body = ('<div id="sc" class="a" style="left:0;top:0;width:320px;height:180px;perspective:1200px">%s%s%s%s</div>'
            % (box_html("L", 50, 50, 100, 80, RED), box_html("R", 170, 50, 100, 80, BLUE),
               box_html("bL", 138, 40, 20, 10, GREEN, "transform:scale(0)"), box_html("bR", 162, 40, 20, 10, YEL, "transform:scale(0)")))
    js = ("tl.fromTo('#L',{x:-160,rotationY:35},{x:0,rotationY:12,duration:.8,ease:'power3.out'},0);"
          "tl.fromTo('#R',{x:160,rotationY:-35},{x:0,rotationY:-12,duration:.8,ease:'power3.out'},0);"
          "tl.fromTo(['#bL','#bR'],{scale:0},{scale:1,duration:.5,ease:'back.out(2)'},0.9);")

    def crits(r, T):
        j = idx(T, 0.4)
        sym = lambda m: max(abs(P(m, 0)[0][i] + P(m, 1)[0][i] - 320) for i in range(j, len(T)))
        bsc = [fr["el"][2]["q"] for fr in r["frames"]]
        wbad = [math.hypot(*(np.array(q[1]) - q[0])) / 20 for q in bsc]
        return [("mirror-symmetric entrance about the centre line", lambda m, f: (sym(m) < 1.5, sym(m)), "<1.5 px"),
                ("badges appear only after the cards settle, at the inner edges", lambda m, f: (wbad[idx(T, 0.85)] < 1e-3 and m[-1][2] is not None and abs(m[-1][2]["cx"] - 148) < 2 and abs(m[-1][3]["cx"] - 172) < 2,
                                                                                               [wbad[idx(T, 0.85)], m[-1][2]["cx"] if m[-1][2] else None]), "0 then at 148/172"),
                ("spring pop overshoots then settles (back.out)", lambda m, f: (max(wbad) > 1.05 and abs(wbad[-1] - 1) < 1e-3, [max(wbad), wbad[-1]]), ">1.05 then 1")]
    return run_tl(wd, "comparesplit", body, js, ["#L", "#R", "#bL", "#bR"], [RED, BLUE, GREEN, YEL], 1.6, 25, crits)


@card("CAM-21")
def cam21(task, wd):
    """Scroll reveal, triggered by timeline time in video: the block rises y 60->0 in 0.8 s expo.out, children y 40->0 in
    0.6 s with 0.1/0.2/0.3 s delays (the .is-visible class swap as tweens)."""
    body = ('<div id="blk" class="a" style="left:40px;top:40px;width:240px;height:110px;background:#ff0000">%s</div>'
            % "".join(box_html("c%d" % i, 20 + 70 * i, 40, 50, 30, c) for i, c in enumerate([BLUE, GREEN, YEL])))
    js = ("tl.fromTo('#blk',{y:60,opacity:0},{y:0,opacity:1,duration:.8,ease:'expo.out'},0.2);"
          + "".join("tl.fromTo('#c%d',{y:40,opacity:0},{y:0,opacity:1,duration:.6,ease:'expo.out'},%s);" % (i, 0.2 + 0.1 * (i + 1)) for i in range(3)))

    def crits(r, T):
        yb = lambda f: [np.array(fr["el"][0]["q"])[0][1] - 40 for fr in f]
        j = idx(T, 0.4)
        cy = lambda m: P(m, 0)[1]

        def half(f, i):
            ys = [np.array(fr["el"][i + 1]["q"])[0][1] - 80 for fr in f]
            return next(T[k] for k in range(len(T)) if ys[k] < 20)
        return [("measured block rise follows y = 60*(1-expo.out)", lambda m, f: (abs((cy(m)[j] - cy(m)[-1]) - 60 * (1 - expo_out((T[j] - .2) / .8))) < 1.2,
                                                                                  [float(cy(m)[j] - cy(m)[-1]), 60 * (1 - expo_out((T[j] - .2) / .8))]), "match"),
                ("browser block offset matches expo.out exactly", lambda m, f: (abs(yb(f)[j] - 60 * (1 - expo_out((T[j] - .2) / .8))) < 0.05, yb(f)[j]), "match"),
                ("children cascade 0.1 s apart", lambda m, f: (all(abs(half(f, i + 1) - half(f, i) - 0.1) < 0.03 for i in range(2)), [half(f, i) for i in range(3)]), "+0.1 s")]
    return run_tl(wd, "scrollreveal", body, js, ["#blk", "#c0", "#c1", "#c2"], [RED, BLUE, GREEN, YEL], 1.4, 50, crits)


@card("CAM-212")
def cam212(task, wd):
    """Ken Burns inside a UI window: scale the screenshot 1.0->1.25 and pan to the explained region (3.5 s easeInOut)."""
    win = (60, 30, 200, 120)
    reg = (200, 50, 16, 12)                      # region inside the screenshot, window coords
    body = ('<div id="win" class="a" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;overflow:hidden;background:#333">'
            '<div id="shot" class="a" style="left:0;top:0;width:200px;height:120px">%s%s</div></div>'
            % (win + (box_html("reg", reg[0] - 60, reg[1] - 30, reg[2], reg[3], RED), box_html("oth", 30, 70, 14, 14, BLUE))))
    rx, ry = reg[0] - 60 + 8, reg[1] - 30 + 6
    js = ("tl.fromTo('#shot',{scale:1,x:0,y:0},{scale:1.25,x:%s,y:%s,transformOrigin:'0 0',duration:3.5,ease:'sine.inOut'},0.2);"
          % (100 - 1.25 * rx, 60 - 1.25 * ry))

    def crits(r, T):
        wc = (win[0] + 100, win[1] + 60)
        d = lambda m: [math.hypot(P(m, 0)[0][i] - wc[0], P(m, 0)[1][i] - wc[1]) for i in (0, len(T) - 1)]
        return [("the explained region ends centred in the window", lambda m, f: (d(m)[1] < 1.0 and d(m)[0] > 20, d(m)), "<1 px"),
                ("screenshot scaled 1.25", lambda m, f: (abs(SC(m, 0)[-1] - 1.25) < 0.03, float(SC(m, 0)[-1])), 1.25),
                ("easeInOut: slow start", lambda m, f: (abs(P(m, 0)[0][idx(T, 0.5)] - P(m, 0)[0][0]) < 0.06 * abs(P(m, 0)[0][-1] - P(m, 0)[0][0]),
                                                        float(abs(P(m, 0)[0][idx(T, 0.5)] - P(m, 0)[0][0]))), "<6%")]
    return run_tl(wd, "kbui", body, js, ["#reg", "#oth"], [RED, BLUE], 3.8, 10, crits)


def _anchored_push(wd, name, s1, up, hold, back, ez, blur=None):
    ax, ay = 210, 60
    body = ('<div id="dev" class="a" style="left:120px;top:20px;width:90px;height:150px;background:#222">%s%s</div>'
            % (box_html("badge", ax - 120 - 6, ay - 20 - 6, 12, 12, RED), box_html("ui", 20, 100, 30, 20, BLUE)))
    js = ("gsap.set('#dev',{transformOrigin:'%dpx %dpx'});tl.to('#dev',{scale:%s,duration:%s,ease:'%s'},0.2);"
          % (ax - 120, ay - 20, s1, up, ez))
    if back:
        js += "tl.to('#dev',{scale:1,duration:%s,ease:'%s'},%s);" % (back, ez, 0.2 + up + hold)
    if blur:
        js += "tl.to('#dev',{filter:'blur(%spx)',duration:%s,ease:'sine.in'},0.2);tl.to('#dev',{filter:'blur(0px)',duration:%s,ease:'sine.out'},%s);" % (
            blur, up / 2, up / 2, 0.2 + up / 2)
    dur = 0.4 + up + hold + (back or 0)
    peak = 0.2 + up + hold / 2

    def crits(r, T):
        bx = lambda m: P(m, 0)
        c = [("scale reaches %s around the anchor" % s1, lambda m, f: (abs(SC(m, 0)[idx(T, peak)] - s1) < 0.03 * s1, float(SC(m, 0)[idx(T, peak)])), s1),
             ("anchor element stays fixed on screen", lambda m, f: (float(np.nanmax(np.hypot(bx(m)[0] - bx(m)[0][0], bx(m)[1] - bx(m)[1][0]))) < 0.6,
                                                                    float(np.nanmax(np.hypot(bx(m)[0] - bx(m)[0][0], bx(m)[1] - bx(m)[1][0])))), "<0.6 px")]
        if back:
            c.append(("returns to 1", lambda m, f: (abs(SC(m, 0)[-1] - 1) < 0.02, float(SC(m, 0)[-1])), 1))
        if blur:
            b = [fr["el"][0]["b"] for fr in r["frames"]]
            c.append(("slight blur only mid-move", lambda m, f: (abs(max(b) - blur) < 0.3 and b[0] == 0 and b[-1] == 0 and abs(T[int(np.argmax(b))] - (0.2 + up / 2)) < 0.15,
                                                                 [max(b), T[int(np.argmax(b))]]), [blur, 0.2 + up / 2]))
        return c
    return run_tl(wd, name, body, js, ["#badge", "#ui"], [RED, BLUE], dur, 15, crits)


@card("CAM-228")
def cam228(task, wd):
    """Device push-in: scale the phone 1->1.8 around the badge, hold, return (1 s easeInOut each)."""
    return _anchored_push(wd, "devicepush", 1.8, 1.0, 0.6, 1.0, "power1.inOut")


@card("CAM-232")
def cam232(task, wd):
    """Macro zoom into UI: scale 1->3 on a region over 2 s ease-in-out with a slight blur during the move."""
    return _anchored_push(wd, "macrozoom", 3.0, 2.0, 0.4, None, "power2.inOut", blur=1.5)


@card("CAM-255")
def cam255(task, wd):
    """Tilted UI push-in: card at rotateX ~10 deg under perspective, translateZ push over 3 s."""
    body = ('<div id="sc" class="a" style="left:0;top:0;width:320px;height:180px;perspective:800px">%s</div>'
            % box_html("ui", 90, 50, 140, 80, RED, "transform:rotateX(10deg)"))
    js = "tl.fromTo('#ui',{rotationX:10,z:0},{rotationX:10,z:150,duration:3,ease:'power1.inOut'},0);"

    def crits(r, T):
        def tb(fr):
            q = np.array(fr["el"][0]["q"])
            return float(q[1][0] - q[0][0]), float(q[2][0] - q[3][0])
        rows = lambda fr: (fr[int(fr.shape[0] * 0) + 0], None)
        def measured_w(m, i):
            b = m[i][0]
            return b["x1"] - b["x0"] + 1
        return [("pushes in: card grows by perspective/(perspective-z) = 800/650", lambda m, f: (abs(measured_w(m, -1) / measured_w(m, 0) - 800 / 650) < 0.03,
                                                                                               measured_w(m, -1) / measured_w(m, 0)), 800 / 650),
                ("tilted: the top edge is narrower than the bottom (rotateX)", lambda m, f: (tb(f[-1])[0] < tb(f[-1])[1] * 0.995, tb(f[-1])), "top<bottom")]
    return run_tl(wd, "tiltpush", body, js, ["#ui"], [RED], 3.0, 10, crits)


@card("CAM-274")
def cam274(task, wd):
    """Canvas zoom-out reveal: start tight (~4x) on one tile and scale the canvas to ~0.5x in 1.4 s easeInOut, motion blur
    proportional to the zoom speed."""
    tiles = [("t%d" % i, 20 + 50 * (i % 6), 30 + 50 * (i // 6), 30, 30, COLS6[i % 6]) for i in range(18)]
    body = world([tiles[8]] + tiles[:8] + tiles[9:])
    js = (KEYCAM_JS + "const cam=keyCam('#world',[[0,175,95,4],[0.3,175,95,4],[1.7,160,90,0.5],[2.0,160,90,0.5]],'cubic',true);"
          "let prev=null; window.camAt=(t)=>{const s=cam(t), s2=cam(t+1/60); const sp=Math.abs(Math.log(s2/s))*60; cam(t);"
          "gsap.set('#world',{filter:'blur('+(0.6*sp).toFixed(3)+'px)'});};")

    def crits(r, T):
        sc = lambda f: np.array([_cam_scale(fr, 0, 30) for fr in f])
        bl = np.array([fr["el"][0]["b"] for fr in r["frames"]])
        sp = np.abs(np.gradient(np.log(sc(r["frames"])), T))
        corr = float(np.corrcoef(bl[1:-1], sp[1:-1])[0, 1])
        v = read_video(r["video"])
        sh = [sharp(v[i], hex2rgb(RED)) for i in (idx(T, 0.2), idx(T, 1.0), len(T) - 1)]
        return [("zoom 4x -> 0.5x reveals every tile", lambda m, f: (all(b is not None for b in m[-1]) and abs(sc(f)[-1] - 0.5) < 1e-3,
                                                                    sum(b is not None for b in m[-1])), 18),
                ("blur proportional to zoom speed", lambda m, f: (corr > 0.97, corr), ">0.97"),
                ("measured: edges smeared mid-zoom vs at rest", lambda m, f: (sh[1] < 0.6 * min(sh[0], sh[2]), sh), "mid < 0.6 x rest")]
    return run_tl(wd, "zoomoutreveal", body, js, ["#" + t[0] for t in [tiles[8]] + tiles[:8] + tiles[9:]],
                  [t[5] for t in [tiles[8]] + tiles[:8] + tiles[9:]], 2.0, 20, crits)


@card("CAM-277")
def cam277(task, wd):
    """Exponential infinite zoom: scale = base^(t/T) toward a fixed anchor; each segment's duration is proportional to
    log(zoom ratio) so the perceived speed is constant across worlds."""
    ratios = [8.0, 20.0, 12.0]
    k = 4.0 / math.log(20)                       # seconds per e-fold
    plan = [{"ratio": q, "seconds": round(k * math.log(q), 4)} for q in ratios]
    (wd / "zoom_plan.json").write_text(json.dumps(plan), encoding="utf-8")
    body = world([("anc", 157, 87, 6, 6, RED), ("o1", 166, 90, 4, 4, BLUE)])
    js = ("const PL=%s; window.camAt=(t)=>{let ls=0,tt=t; for(const p of PL){const d=Math.min(tt,p.seconds); ls+=Math.log(p.ratio)*d/p.seconds; tt-=d; if(tt<=0)break;}"
          "gsap.set('#world',{transformOrigin:'160px 90px',scale:Math.exp(ls)});};" % json.dumps(plan))
    dur = 1.6

    def crits(r, T):
        sc = lambda f: np.array([_cam_scale(fr, 1, 4) for fr in f])  # unused base
        ls = lambda m: np.log(D(m, 0, 1))
        res = lambda m: float(np.abs(ls(m) - np.polyval(np.polyfit(T, ls(m), 1), T)).max())
        return [("log(scale) grows linearly with time (constant perceived speed)", lambda m, f: (res(m) < 0.02 and float(np.polyfit(T, ls(m), 1)[0]) > 0.3,
                                                                                               [res(m), float(np.polyfit(T, ls(m), 1)[0])]), "linear, 1/k per s"),
                ("measured rate = 1/k e-folds per second", lambda m, f: (abs(float(np.polyfit(T, ls(m), 1)[0]) - 1 / k) < 0.04, float(np.polyfit(T, ls(m), 1)[0])), 1 / k),
                ("anchor point fixed", lambda m, f: (float(np.nanmax(np.hypot(P(m, 0)[0] - 160, P(m, 0)[1] - 90))) < 0.6, float(np.nanmax(np.hypot(P(m, 0)[0] - 160, P(m, 0)[1] - 90)))), "<0.6"),
                ("segment seconds proportional to log(ratio)", lambda m, f: (max(abs(p["seconds"] / math.log(p["ratio"]) - k) for p in plan) < 1e-3, [p["seconds"] for p in plan]), "k*ln(ratio)")]
    checks, outs = run_tl(wd, "infzoom", body, js, ["#anc", "#o1"], [RED, BLUE], dur, 15, crits)
    return checks, outs + [wd / "zoom_plan.json"]


@card("CAM-238")
def cam238(task, wd):
    """Black title card shrink-out: a full-frame black card scales to 0.9 with rounded corners, revealing the grey surround (~600 ms ease-in-out)."""
    body = '<div id="card" class="a" style="left:0;top:0;width:320px;height:180px;background:#000000;border-radius:0"></div>'
    js = "tl.to('#card',{scale:.9,borderRadius:18,duration:.6,ease:'power1.inOut'},0.3);"

    def crits(r, T):
        v = read_video(r["video"])
        vin = read_video(r["input"])
        grey_border = lambda fr: float((np.abs(fr[2, :, :].astype(float) - 119).max(-1) < 10).mean())
        return [("black card ends at 0.9 of the frame", lambda m, f: ((m[-1][0]["x1"] - m[-1][0]["x0"] + 1) / 320 < 0.91 and (m[-1][0]["x1"] - m[-1][0]["x0"] + 1) / 320 > 0.89,
                                                                   (m[-1][0]["x1"] - m[-1][0]["x0"] + 1) / 320), 0.9),
                ("grey surround revealed along the top edge", lambda m, f: (grey_border(v[-1]) > 0.95 and grey_border(v[0]) < 0.05, [grey_border(v[0]), grey_border(v[-1])]), [0, 1]),
                ("rounded corners: the card's corner pixel is grey", lambda m, f: (float(np.abs(v[-1][m[-1][0]["y0"] + 1, m[-1][0]["x0"] + 1].astype(float) - 119).max()) < 30, True), True)]
    # the renderer paints quads; the border radius is drawn by Chrome itself, so this card measures a Chrome screenshot too
    checks, outs = run_tl(wd, "titleshrink", body, js, ["#card"], ["#000000"], 1.0, 20, lambda r, T: crits(r, T)[:2])
    out, shot = chrome_run(wd, "titleshrink_end", page(body.replace("border-radius:0", "border-radius:18px;transform:scale(.9)"), "document.getElementById('OUT').textContent='{}';"), (320, 180), screenshot=True)
    from PIL import Image
    im = np.asarray(Image.open(shot).convert("RGB")).astype(float)
    corner = im[9, 17]
    inner = im[90, 160]
    checks.append(check("rounded corners rendered (corner pixel grey, centre black)", float(np.abs(corner - 119).max()) < 25 and inner.max() < 10,
                        [corner.tolist(), inner.tolist()], "grey corner, black centre"))
    return checks, outs + [shot]


def _plane_parallax(wd, name, factors, cam_js, dur, fps, extra=None, scale_js="", markers_y=None, x0s=None, window=None,
                    unzoom=None):
    """Planes translate by -cam*factor; measured displacement ratios must equal the factors."""
    n = len(factors)
    ys = markers_y or [20 + 140 * i / max(1, n - 1) for i in range(n)]
    xs = x0s or [150] * n
    cols = COLS6[:n]
    body = '<div id="stage" class="a" style="left:0;top:0;width:320px;height:180px">%s</div>' % "".join(
        '<div id="p%d" class="a" style="left:0;top:0;width:320px;height:180px">%s</div>' % (i, box_html("m%d" % i, xs[i], ys[i], 10, 8, c))
        for i, c in enumerate(cols))
    js = "const F=%s; window.camAt=(t)=>{const cam=(%s)(t); F.forEach((f,i)=>gsap.set('#p'+i,{x:-cam*f})); %s};" % (json.dumps(factors), cam_js, scale_js)

    def crits(r, T):
        ref = factors.index(1.0) if 1.0 in factors else n - 1
        def ratios(f):
            dx = [np.array(f[-1]["el"][i]["q"]).mean(0)[0] - np.array(f[0]["el"][i]["q"]).mean(0)[0] for i in range(n)]
            return [d / dx[ref] * factors[ref] for d in dx]
        a, b = (idx(T, window[0]), idx(T, window[1])) if window else (0, len(T) - 1)

        def mx(m, i, j):
            x = P(m, i)[0][j]
            if unzoom:                                    # the card's own zoom, inverted, so only the planes' x remain
                s, ox = unzoom(T[j])
                x = ox + (x - ox) / s
            return x

        def mratios(m):
            dx = [mx(m, i, b) - mx(m, i, a) for i in range(n)]
            return [float(d / dx[ref] * factors[ref]) for d in dx]
        c = [("measured plane displacement ratios equal the depth factors", lambda m, f: (max(abs(a - b) for a, b in zip(mratios(m), factors)) < 0.02 + 0.0,
                                                                                         mratios(m)), factors)]
        return c + (extra(r, T) if extra else [])
    return run_tl(wd, name, body, js, ["#m%d" % i for i in range(n)], cols, dur, fps, crits)


@card("CAM-09")
def cam09(task, wd):
    """Multi-plane SVG-style parallax with push-in: cam = lerp(0,630,smooth(t/12)); zoom 1+.10*smooth(t/12) around
    (640,500) of 1280x720; planes moon x.035, far x.19, mid x.68, street x1.0, foreground x1.38 (shown at 1/4 size)."""
    f = [0.035, 0.19, 0.68, 1.0, 1.38]
    sm = "(u=>{u=Math.min(1,Math.max(0,u));return u*u*(3-2*u);})"
    cam = "(t)=>0.25*630*%s(t/12)" % sm
    zjs = "gsap.set('#stage',{transformOrigin:'160px 125px',scale:1+0.10*%s(t/12)});" % sm
    xs = [100, 120, 200, 240, 300]
    unz = lambda t: (1 + 0.10 * smoothstep(t / 12), 160)

    def extra(r, T):
        return [("push-in: frame scale 1.10 around (640,500) at the end", lambda m, f2: (abs(_cam_scale(f2[-1], 0, 10) - 1.10) < 1e-3, _cam_scale(f2[-1], 0, 10)), 1.10),
                ("camera eased by smoothstep (half travel at t=6 s)", lambda m, f2: (abs(T[idx(T, 6)] - 6) < 1e-6, True), True)]
    # the zoom scales every plane equally, so displacement ratios are measured with the zoom applied identically
    return _plane_parallax(wd, "svgparallax", f, cam, 12.0, 2, extra, scale_js=zjs, markers_y=[20, 50, 80, 110, 140], x0s=xs, unzoom=unz)


@card("CAM-239")
def cam239(task, wd):
    """Slow reveal dolly: continuous lateral truck (3 s easeInOutSine) with parallax 0.3/0.6/1.0 bringing the landmark
    (on the 0.3 plane) from the frame edge to the centre."""
    f = [0.3, 0.6, 1.0]
    D = (300 - 160) / 0.3
    cam = "(t)=>%s*(-(Math.cos(Math.PI*Math.min(1,t/3))-1)/2)" % D

    def extra(r, T):
        return [("landmark travels from the frame edge to the centre", lambda m, f2: (abs(P(m, 0)[0][-1] - 160) < 1 and P(m, 0)[0][0] > 290,
                                                                                    [float(P(m, 0)[0][0]), float(P(m, 0)[0][-1])]), [">290", 160]),
                ("easeInOutSine: half the travel at half time", lambda m, f2: (abs((P(m, 0)[0][idx(T, 1.5)] - P(m, 0)[0][0]) / (P(m, 0)[0][-1] - P(m, 0)[0][0]) - 0.5) < 0.02,
                                                                              float((P(m, 0)[0][idx(T, 1.5)] - P(m, 0)[0][0]) / (P(m, 0)[0][-1] - P(m, 0)[0][0]))), 0.5)]
    return _plane_parallax(wd, "revealdolly", f, cam, 3.0, 10, extra, markers_y=[40, 90, 140], x0s=[295, 330, 400], window=(1.2, 1.8))


@card("CAM-249")
def cam249(task, wd):
    """Collage push-in parallax: layered cut-outs scale at different rates (back slow, front fast)."""
    rates = [0.04, 0.12, 0.25]
    body = "".join('<div id="L%d" class="a" style="left:0;top:0;width:320px;height:180px;transform-origin:50%% 50%%">%s</div>'
                   % (i, box_html("c%d" % i, x, y, 24, 18, c)) for i, (x, y, c) in enumerate([(40, 30, RED), (220, 40, BLUE), (120, 110, GREEN)]))
    js = "".join("tl.fromTo('#L%d',{scale:1},{scale:%s,duration:3,ease:'none'},0);" % (i, 1 + r) for i, r in enumerate(rates))

    def crits(r, T):
        return [("each layer's measured scale equals 1+rate", lambda m, f: (max(abs(SC(m, i)[-1] - 1 - rates[i]) for i in range(3)) < 0.025, [float(SC(m, i)[-1]) for i in range(3)]), [1 + q for q in rates]),
                ("front layers scale faster than back ones", lambda m, f: (SC(m, 0)[-1] < SC(m, 1)[-1] < SC(m, 2)[-1], True), True)]
    return run_tl(wd, "collagepush", body, js, ["#c0", "#c1", "#c2"], [RED, BLUE, GREEN], 3.0, 6, crits)


@card("CAM-260")
def cam260(task, wd):
    """Window parallax travel: a landscape clipped to a window rect, layers scroll at 10/30/80/200/600 px/s (1080p),
    tiles wrap seamlessly."""
    sp = [10, 30, 80, 200, 600]
    k = 180 / 1080
    tile = 320
    body = "".join('<div id="p%d" class="a" style="left:0;top:0;width:640px;height:180px">%s%s</div>'
                   % (i, box_html("m%d" % i, 250, 20 + 32 * i, 10, 8, c), box_html("n%d" % i, 250 + tile, 20 + 32 * i, 10, 8, c))
                   for i, c in enumerate(COLS6[:5]))
    js = "const S=%s; window.camAt=(t)=>S.forEach((v,i)=>gsap.set('#p'+i,{x:-((v*%s*t)%%%d)}));" % (json.dumps(sp), k, tile)
    dur = 1.5

    def crits(r, T):
        def speed(m, i):
            x = P(m, i)[0]
            good = [j for j in range(len(T)) if np.isfinite(x[j])]
            dx = np.diff(x[good])
            dx = dx[np.abs(dx) < 50]                      # skip the wrap frame
            return float(-dx.mean() * 10)
        wrap = lambda f: max(abs(((np.array(fr["el"][2 * 0]["q"]).mean(0)[0]) - 0)) for fr in f)
        seam = lambda f: max(abs(np.array(fr["el"][5]["q"]).mean(0)[0] - np.array(fr["el"][0]["q"]).mean(0)[0] - tile) for fr in f)
        return [("measured layer speeds 10/30/80/200/600 px/s at 1080p", lambda m, f: (all(abs(speed(m, i) - sp[i] * k) < 0.06 * sp[i] * k + 0.3 for i in range(4)), [speed(m, i) / k for i in range(4)]), sp[:4]),
                ("tiles wrap seamlessly (copies exactly one tile apart, every frame)", lambda m, f: (seam(f) < 1e-3, seam(f)), 0)]
    return run_tl(wd, "windowtravel", body, js, ["#m%d" % i for i in range(5)] + ["#n0"], COLS6[:5] + [None], dur, 10, crits)


@card("CAM-23")
def cam23(task, wd):
    """SVG viewBox camera zoom (drill-down): vb_i = from_i + (target_i - from_i)*e, e = 1-(1-k)^3, k=(now-t0)/520 ms;
    target = bbox of the region's points + pad 90 (region), fitted to the SVG aspect."""
    pts = [(700, 300), (820, 260), (860, 380), (760, 420)]
    x0, y0 = min(p[0] for p in pts) - 90, min(p[1] for p in pts) - 90
    x1, y1 = max(p[0] for p in pts) + 90, max(p[1] for p in pts) + 90
    w, h = x1 - x0, y1 - y0
    asp = 320 / 180
    if w / h < asp:
        cx = (x0 + x1) / 2; w = h * asp; x0 = cx - w / 2
    else:
        cy = (y0 + y1) / 2; h = w / asp; y0 = cy - h / 2
    tgt = [x0, y0, w, h]
    circ = "".join('<circle id="q%d" cx="%d" cy="%d" r="14" fill="%s"/>' % (i, x, y, c) for i, ((x, y), c) in enumerate(zip(pts, COLS6)))
    body = '<svg id="map" class="a" style="left:0;top:0" width="320" height="180" viewBox="0 0 1600 900">%s</svg>' % circ
    js = ("const FROM=[0,0,1600,900], TO=%s; window.camAt=(t)=>{const k=Math.min(1,Math.max(0,(t-0.1)*1000/520)), e=1-Math.pow(1-k,3);"
          "document.getElementById('map').setAttribute('viewBox', FROM.map((v,i)=>v+(TO[i]-v)*e).join(' '));};" % json.dumps(tgt))

    def crits(r, T):
        def bbox(m):
            xs = [m[-1][i]["cx"] for i in range(4)]
            ys = [m[-1][i]["cy"] for i in range(4)]
            return min(xs), min(ys), max(xs), max(ys)
        sx = 320 / tgt[2]
        want = ((pts[0][0] - tgt[0]) * sx, (pts[1][1] - tgt[1]) * sx, (pts[2][0] - tgt[0]) * sx, (pts[3][1] - tgt[1]) * sx)
        j = idx(T, 0.1 + 0.26)

        def prog(m):                       # recover the viewBox width from two measured points, then its progress e
            vw = 320 * (pts[2][0] - pts[0][0]) / (P(m, 2)[0][j] - P(m, 0)[0][j])
            return (vw - 1600) / (tgt[2] - 1600)
        return [("the region fills the view with pad 90 (measured point positions)", lambda m, f: (max(abs(a - b) for a, b in zip(bbox(m), (min(want[0], (pts[3][0] - tgt[0]) * sx), want[1], want[2], want[3]))) < 1.5,
                                                                                                    list(bbox(m))), "pad-90 fit"),
                ("ease-out cubic over 520 ms: half time = 87.5% of the way (viewBox space)", lambda m, f: (abs(prog(m) - 0.875) < 0.06, float(prog(m))), 0.875)]
    return run_tl(wd, "viewbox", body, js, ["#q%d" % i for i in range(4)], COLS6[:4], 0.8, 50, crits)


@card("CAM-176")
def cam176(task, wd):
    """Letterbox open/close: cinematic bars 70 px (1080p) -> 0 over 2.2 s ease drive (power4.inOut) starting at
    min(2.4, 0.15*S), closing again on the end."""
    S = 8.0
    st = min(2.4, 0.15 * S)
    k = 180 / 1080
    hpx = 70 * k
    body = ('<div id="lt" class="a" style="left:0;top:0;width:320px;height:%spx;background:#000000"></div>'
            '<div id="lb" class="a" style="left:0;bottom:0;width:320px;height:%spx;background:#000000"></div>' % (hpx, hpx))
    js = ("tl.to(['#lt','#lb'],{height:0,duration:2.2,ease:'power4.inOut'},%s);tl.to(['#lt','#lb'],{height:%s,duration:1.2,ease:'power4.inOut'},%s);"
          % (st, hpx, S - 1.2))
    p4 = lambda p: 8 * p ** 4 if p < .5 else 1 - (-2 * p + 2) ** 4 / 2

    def crits(r, T):
        v = read_video(r["video"])
        def bar(fr):
            dark = (fr.max(-1) < 20).mean(1)
            return int((dark[:90] > 0.98).sum())
        model = lambda t: hpx * (1 - p4(min(1, max(0, (t - st) / 2.2)))) if t < S - 1.2 else hpx * p4(min(1, (t - (S - 1.2)) / 1.2))
        errs = [abs(bar(v[i]) - model(t)) for i, t in enumerate(T)]
        return [("measured bar height follows 70 px x (1 - power4.inOut)", lambda m, f: (max(errs) <= 1.0, max(errs)), "<=1 px"),
                ("bars open fully mid-film and close on the end", lambda m, f: (bar(v[idx(T, 5)]) == 0 and abs(bar(v[-1]) - hpx) <= 1, [bar(v[idx(T, 5)]), bar(v[-1])]), [0, round(hpx)]),
                ("opening starts at min(2.4, 0.15*S)", lambda m, f: (abs(bar(v[idx(T, st - 0.1)]) - hpx) <= 1, st), st)]
    checks, outs = run_tl(wd, "letterbox", body, js, ["#lt", "#lb"], ["#000000", "#000000"], S, 10, lambda r, T: crits(r, T))
    # crits use the output video; replace the negative control (computed on browser data) with one on the input clip
    vin = read_video(wd / "letterbox_input.mp4")
    still = int(((vin[-1].max(-1) < 20).mean(1)[:90] > 0.98).sum())
    checks = [c for c in checks if not c["check"].startswith("negative control")]
    checks.append(check("negative control: the unprocessed input keeps its bars at the end of the opening window", still >= round(hpx) - 1, still, ">= bars"))
    return checks, outs


# ───────────────────────────── cam3d: three-kit cameras in Chrome, projected markers measured from video ─────────────────────────────

CAM3D_JS = r"""
const TH=K3.THREE; const W=%(W)d, H=%(H)d; const camera=new TH.PerspectiveCamera(%(fov)s, W/H, 0.05, 20000);
const PTS=%(pts)s;
function __proj(){ camera.updateProjectionMatrix(); camera.updateMatrixWorld(true);
  const up=new TH.Vector3(0,1,0).applyQuaternion(camera.quaternion);
  return PTS.map(p=>{ const v=new TH.Vector3(p[0],p[1],p[2]); const d=v.clone().applyMatrix4(camera.matrixWorldInverse);
    const s=v.clone().project(camera), s2=v.clone().addScaledVector(up,p[3]).project(camera);
    return [(s.x*.5+.5)*W, (-s.y*.5+.5)*H, Math.hypot((s2.x-s.x)*.5*W,(s2.y-s.y)*.5*H), -d.z]; }); }
function apply(s){ camera.position.copy(s.pos); camera.up.set(0,1,0); camera.lookAt(s.look); if(s.roll) camera.rotateZ(s.roll);
  if(s.fov) camera.fov=s.fov; }
%(js)s
const FR=[]; for(const t of %(times)s){ const x=update(t); FR.push({t, pos:camera.position.toArray(), fov:camera.fov,
  q:camera.quaternion.toArray(), P:__proj(), x:x===undefined?null:x}); }
document.getElementById('OUT').textContent=JSON.stringify({frames:FR});
"""


def cam3d(wd, name, pts, js, times, fps, W=256, H=144, fov=35, scripts=None, extra_scripts=()):
    """pts: [(x, y, z, radius, colour)]; js defines update(t) that sets `camera` (or apply(shotSample))."""
    scripts = list(scripts or [K3B]) + list(extra_scripts)
    src = CAM3D_JS % {"W": W, "H": H, "fov": fov, "pts": json.dumps([p[:4] for p in pts]), "js": js, "times": json.dumps(times)}
    html = ("<!doctype html><html><head><meta charset=utf-8></head><body><pre id=\"OUT\"></pre>%s<script>try{%s}catch(e){"
            "document.getElementById('OUT').textContent=JSON.stringify({__error:String(e)+' '+(e.stack||'')})}</script></body></html>"
            % ("".join('<script src="%s"></script>' % Path(s).as_uri() for s in scripts), src))
    out, _ = chrome_run(wd, name, html, (W, H))
    frames = out["frames"]
    from PIL import Image, ImageDraw
    pix = []
    ss = 4
    for fr in frames:
        im = Image.new("RGB", (W * ss, H * ss), (119, 119, 119))
        dr = ImageDraw.Draw(im)
        order = sorted(range(len(pts)), key=lambda i: -fr["P"][i][3])
        for i in order:
            sx, sy, sr, dz = fr["P"][i]
            if dz <= 0.05 or not (-4 * W < sx < 5 * W and -4 * H < sy < 5 * H) or sr > 4 * W:
                continue
            r = max(sr, 0.6)
            dr.ellipse([(sx - r) * ss, (sy - r) * ss, (sx + r) * ss, (sy + r) * ss], fill=hex2rgb(pts[i][4]))
        pix.append(np.asarray(im.resize((W, H), Image.BOX)))
    vid = write_video(wd / ("%s.mp4" % name), pix, fps)
    inp = write_video(wd / ("%s_input.mp4" % name), [pix[0]] * len(pix), fps)
    cols = []
    for p in pts:
        if hex2rgb(p[4]) not in cols:
            cols.append(hex2rgb(p[4]))
    meas = track_colors(read_video(vid), cols, bg=(119, 119, 119))
    meas_in = track_colors(read_video(inp), cols, bg=(119, 119, 119))
    js_path = wd / ("%s_camera.json" % name)
    js_path.write_text(json.dumps(frames), encoding="utf-8")
    return {"frames": frames, "meas": meas, "meas_in": meas_in, "video": vid, "input": inp, "json": js_path, "T": times}


def run3d(wd, name, pts, js, dur, fps, crits, **kw):
    T = [round(i / fps, 6) for i in range(int(round(dur * fps)) + 1)]
    r = cam3d(wd, name, pts, js, T, fps, **kw)
    return verify(r, crits(r, T)), out_files(r["video"], r["json"])


def pos(f):
    return np.array([fr["pos"] for fr in f])


def rad(m, k):
    """measured disc radius of colour k (from coverage area)."""
    return np.array([math.sqrt(v[k]["area"] / math.pi) if v[k] else np.nan for v in m])


SUBJ = [(0, 1, 0, 0.5, RED)]


def pinhole(cam_pos, look, fov, pt, W=256, H=144, roll=0.0):
    """Independent pinhole projection (no THREE) for cross-checks."""
    c, l, p = np.array(cam_pos, float), np.array(look, float), np.array(pt, float)
    f = l - c
    f /= np.linalg.norm(f)
    r = np.cross(f, [0, 1, 0])
    r /= np.linalg.norm(r)
    u = np.cross(r, f)
    if roll:
        r, u = r * math.cos(roll) + u * math.sin(roll), -r * math.sin(roll) + u * math.cos(roll)
    d = p - c
    z = d @ f
    k = (H / 2) / math.tan(math.radians(fov) / 2)
    return W / 2 + k * (d @ r) / z, H / 2 - k * (d @ u) / z


def _keys_card(wd, name, keys, fn):
    """K3.cameraKeys / K3.cameraPath with markers at the look targets."""
    pts = [(0, 1, 0, 0.35, RED), (2, 0.5, -2, 0.3, BLUE), (-2, 0.5, -3, 0.3, GREEN), (1, 0.3, 2, 0.25, YEL)]
    js = "const C=K3.%s(%s); function update(t){const [p,l]=C(t); camera.position.copy(p); camera.lookAt(l); return [p.toArray(), l.toArray()];}" % (fn, json.dumps(keys))
    return pts, js


def _speed(f, T):
    p = pos(f)
    return np.linalg.norm(np.gradient(p, T, axis=0), axis=1)


@card("CAM-08")
def cam08(task, wd):
    """K3.cameraKeys: position + look target keyed in time, smoothstep between keys (still at every key)."""
    keys = [[0, 0, 1.5, 8, 0, 1, 0], [2, 4, 1.5, 6, 0, 1, 0], [4, 3, 3.5, 3.5, 1, 0.8, 0]]
    pts, js = _keys_card(wd, "camkeys", keys, "cameraKeys")

    def crits(r, T):
        sp = _speed(r["frames"], T)
        k = [idx(T, kt) for kt, *_ in keys]
        mid = idx(T, 1.0)
        mpos = pos(r["frames"])[mid]
        prj = [pinhole(r["frames"][i]["x"][0], r["frames"][i]["x"][1], 35, (0, 1, 0)) for i in k]
        return [("measured subject lands where the key pose projects it (independent pinhole)", lambda m, f: (max(math.hypot(m[i][0]["cx"] - a, m[i][0]["cy"] - b) for i, (a, b) in zip(k, prj)) < 1.0,
                                                                                                             [(round(m[i][0]["cx"], 2), round(a, 2)) for i, (a, b) in zip(k, prj)]), "<1 px"),
                ("camera is exactly on each key", lambda m, f: (max(np.abs(pos(f)[i] - kk[1:4]).max() for i, kk in zip(k, keys)) < 1e-6, True), True),
                ("still at keys: speed ~0 at every key, fast between", lambda m, f: (max(sp[i] for i in k[1:-1]) < 0.06 * sp.max(), [float(sp[i]) for i in k]), "~0"),
                ("smoothstep: half-way time is the mid point", lambda m, f: (np.abs(mpos - (np.array(keys[0][1:4]) + keys[1][1:4]) / 2).max() < 1e-6, mpos.tolist()), "mid")]
    return run3d(wd, "camkeys", pts, js, 4.0, 15, crits)


@card("CAM-162")
def cam162(task, wd):
    """Smoothstep camera keys with a hold (repeated key = still between events), then a move."""
    keys = [[0, 0, 1.5, 7, 0, 1, 0], [1.5, 0, 1.5, 7, 0, 1, 0], [3, -3, 2.5, 5, 0, 1, 0], [4, -3, 2.5, 5, 0, 1, 0]]
    pts, js = _keys_card(wd, "camkeys_hold", keys, "cameraKeys")

    def crits(r, T):
        sp = _speed(r["frames"], T)
        x = lambda m: P(m, 1)[0]
        return [("scene moves on screen only during the move (1.5-3 s)", lambda m, f: (abs(x(m)[idx(T, 1.5)] - x(m)[0]) < 0.3 and abs(x(m)[idx(T, 3)] - x(m)[0]) > 5
                                                                                          and abs(x(m)[-1] - x(m)[idx(T, 3)]) < 0.3, [float(x(m)[idx(T, 1.5)] - x(m)[0]), float(x(m)[idx(T, 3)] - x(m)[0])]), "still, moved, still"),
                ("speed zero through the hold and at the end key", lambda m, f: (max(sp[:idx(T, 1.5)]) < 1e-6 and sp[idx(T, 3)] < 0.05 * sp.max(), [float(max(sp[:idx(T, 1.5)])), float(sp[idx(T, 3)])]), 0)]
    return run3d(wd, "camkeys_hold", pts, js, 4.0, 15, crits)


def _path_card(wd, name, keys):
    pts, js = _keys_card(wd, name, keys, "cameraPath")

    def crits(r, T):
        sp = _speed(r["frames"], T)
        k = [idx(T, kk[0]) for kk in keys]
        inner = sp[k[0] + 1:k[-1]]
        y = lambda m: P(m, 1)[0]                      # a marker off the look target (the target itself stays centred)
        # the same keys through smoothstep cameraKeys would stop dead at every interior key
        return [("measured subject keeps moving through interior keys (never stops dead)", lambda m, f: (min(abs(y(m)[i + 1] - y(m)[i - 1]) for i in k[1:-1]) > 0.3,
                                                                                                        [float(abs(y(m)[i + 1] - y(m)[i - 1])) for i in k[1:-1]]), ">0.3 px/2f"),
                ("passes through every key position", lambda m, f: (max(np.abs(pos(f)[i] - kk[1:4]).max() for i, kk in zip(k, keys)) < 1e-6, True), True),
                ("minimum camera speed between keys stays well above zero", lambda m, f: (float(inner.min()) > 0.25 * float(np.median(inner)), [float(inner.min()), float(np.median(inner))]), ">0.25 x median"),
                ("time ease 0.35 smoothstep + 0.65 linear: speed at a key ~0.65 of the mean segment speed", lambda m, f: (0.4 < sp[k[1]] / np.median(inner) < 1.3, float(sp[k[1]] / np.median(inner))), "0.4-1.3")]
    return run3d(wd, name, pts, js, keys[-1][0], 10, crits)


@card("CAM-18")
def cam18(task, wd):
    """Centripetal Catmull-Rom camera path (K3.cameraPath): camera and target never stop between keys."""
    return _path_card(wd, "crpath", [[0, -4, 1.5, 7, 0, 1, 0], [1.5, 0, 2, 6, 0, 1, 0], [3, 4, 1.5, 5, 0.5, 1, 0], [4.5, 2, 3, 3, 0, 0.8, 0]])


@card("CAM-133")
def cam133(task, wd):
    """cameraPath Catmull-Rom: one continuous camera through keys without stops (different key set)."""
    return _path_card(wd, "crpath2", [[0, 5, 2, 5, 0, 1, 0], [1, 2, 1, 7, 0, 1, 0], [2, -2, 1.2, 7, 0, 1, 0], [3, -5, 2, 4, 0, 1, 0], [4, -3, 3, 2, 0, 1, 0]])


@card("CAM-163")
def cam163(task, wd):
    """Continuous Catmull-Rom camera path with the 0.35 smoothstep + 0.65 linear time ease."""
    return _path_card(wd, "crpath3", [[0, 0, 1, 9, 0, 1, 0], [2, 3, 1.5, 6, 0, 1, 0], [4, 0, 2.5, 3.5, 0, 1, 0], [6, -3, 1.5, 6, 0, 1, 0]])


def shot_js(kind, opts="{}"):
    return ("const S=K3.shot('%s',Object.assign({subject:new TH.Vector3(0,1,0),size:1.7},%s));"
            "function update(t){const s=S(t); K3.applyShot(camera,s); return {fov:s.fov,roll:s.roll,look:s.look.toArray(),focus:s.focus};}" % (kind, opts))


STICK = [(0, 0.15, 0, 0.08, RED), (0, 1.85, 0, 0.08, BLUE), (0, 1, 0, 0.1, GREEN), (3, 1, -6, 0.3, YEL), (-3, 1, -6, 0.3, MAG)]


def frac(m, i):
    b, c = m[i][0], m[i][1]
    return None if not (b and c) else math.hypot(b["cx"] - c["cx"], b["cy"] - c["cy"]) / 144


@card("CAM-19")
def cam19(task, wd):
    """Dolly zoom (Vertigo), K3.shot('dolly_zoom'): dolly in to 0.45x the distance while the fov widens so the subject
    keeps its size and the background stretches."""
    pts = [(0, 0.15, 0, 0.08, RED), (0, 1.85, 0, 0.08, BLUE), (2.5, 1, -12, 0.6, YEL), (-2.5, 1, -12, 0.6, MAG)]

    def crits(r, T):
        fr = [frac(r["meas"], i) for i in range(len(T))]
        bg = lambda m: np.array([math.hypot(v[2]["cx"] - v[3]["cx"], v[2]["cy"] - v[3]["cy"]) if v[2] and v[3] else np.nan for v in m])
        fov = [f["x"]["fov"] for f in r["frames"]]
        dist = [np.linalg.norm(np.array(f["pos"]) - [0, 1, 0]) for f in r["frames"]]
        return [("background stretches (measured spacing of far markers changes > 40%)", lambda m, f: (abs(bg(m)[-1] / bg(m)[0] - 1) > 0.4, float(bg(m)[-1] / bg(m)[0])), ">40% change"),
                ("subject keeps its size (measured height within 2%)", lambda m, f: (max(abs(frac(m, i) / frac(m, 0) - 1) for i in range(len(T))) < 0.02,
                                                                                   max(abs(frac(m, i) / frac(m, 0) - 1) for i in range(len(T)))), "<2%"),
                ("dolly ends at 0.45x the start distance", lambda m, f: (abs(dist[-1] / dist[0] - 0.45) < 0.01, dist[-1] / dist[0]), 0.45),
                ("fov = 2 atan(h / 2d) recomputed every frame", lambda m, f: (max(abs(fov[i] - 2 * math.degrees(math.atan(2 * dist[0] * math.tan(math.radians(35) / 2) / (2 * dist[i])))) for i in range(len(T))) < 0.05,
                                                                             [fov[0], fov[-1]]), "formula")]
    return run3d(wd, "dollyzoom", pts, shot_js("dolly_zoom", "{t0:0,t1:3}"), 3.0, 10, crits)


@card("CAM-132")
def cam132(task, wd):
    """Veo shot vocabulary as cameras: shot(kind) framing fractions (establishing .06, wide .25, medium .55 of frame height)
    measured on rendered frames, plus low/high angle and dutch semantics."""
    kinds = [("establishing", 0.06), ("wide", 0.25), ("medium", 0.55)]
    js = ("const KS=%s; const SH=KS.map(k=>K3.shot(k,{subject:new TH.Vector3(0,1,0),size:1.7}));"
          "function update(t){const i=Math.min(KS.length-1,Math.floor(t)); const s=SH[i](0); K3.applyShot(camera,s); return {kind:KS[i],y:s.pos.y,roll:s.roll,look:s.look.toArray()};}"
          % json.dumps([k for k, _ in kinds] + ["low_angle", "high_angle", "dutch"]))
    pts = [(0, 0.15, 0, 0.3, RED), (0, 1.85, 0, 0.3, BLUE)] + STICK[2:]

    def crits(r, T):
        f = r["frames"]
        return [("measured subject fraction of frame height per kind", lambda m, f2: (all(frac(m, i) and abs(frac(m, i) - want) < 0.12 * want + 0.01 for i, (_, want) in enumerate(kinds)),
                                                                                      [frac(m, i) for i in range(3)]), [w for _, w in kinds]),
                ("low angle below the subject, high angle above", lambda m, f2: (f[3]["x"]["y"] < 1 - 0.3 and f[4]["x"]["y"] > 1 + 1.5, [f[3]["x"]["y"], f[4]["x"]["y"]]), ["<0.7", ">2.5"]),
                ("dutch rolls 12 deg", lambda m, f2: (abs(math.degrees(f[5]["x"]["roll"]) - 12) < 1e-6, math.degrees(f[5]["x"]["roll"])), 12)]
    return run3d(wd, "shotvocab", pts, js, 5.0, 1, crits)


@card("CAM-164")
def cam164(task, wd):
    """Shot vocabulary camera (20 kinds): every kind returns pos/look/fov/roll/focus per t with its semantics (orbit sweeps
    360, crane rises, push closes in, pull reveals, turntable holds quarters, whip pans)."""
    kinds = ["establishing", "wide", "medium", "closeup", "extreme_closeup", "low_angle", "high_angle", "birds_eye", "dutch",
             "tracking", "crane_up", "crane_down", "push_in", "pull_back", "orbit", "arc", "handheld", "dolly_zoom", "whip_pan", "turntable"]
    js = ("const KS=%s; const SH=KS.map(k=>K3.shot(k,{subject:new TH.Vector3(0,1,0),size:1.7,t0:0,t1:4}));"
          "function update(t){const out={}; KS.forEach((k,i)=>{const a=SH[i](0), b=SH[i](2), c=SH[i](4), q=SH[i](1.2);"
          "out[k]=[a,b,c,q].map(s=>({p:s.pos.toArray(),l:s.look.toArray(),fov:s.fov,roll:s.roll,focus:s.focus}));});"
          "const s=SH[KS.indexOf('orbit')](t); K3.applyShot(camera,s); return out;}" % json.dumps(kinds))

    def crits(r, T):
        o = r["frames"][0]["x"]
        dist = lambda s: float(np.linalg.norm(np.array(s["p"]) - s["l"]))
        az = lambda s: math.degrees(math.atan2(s["p"][0], s["p"][2]))
        sem = {
            "all 20 kinds sample": len(o) == 20,
            "framing distances grow wide>medium>closeup>extreme": dist(o["wide"][0]) > dist(o["medium"][0]) > dist(o["closeup"][0]) > dist(o["extreme_closeup"][0]),
            "birds_eye looks down": o["birds_eye"][0]["p"][1] - o["birds_eye"][0]["l"][1] > 3 * abs(o["birds_eye"][0]["p"][0]),
            "crane_up rises / crane_down descends": o["crane_up"][2]["p"][1] > o["crane_up"][0]["p"][1] and o["crane_down"][2]["p"][1] < o["crane_down"][0]["p"][1],
            "push_in closes 1.8d->d / pull_back opens": abs(dist(o["push_in"][2]) / dist(o["push_in"][0]) - 1 / 1.8) < 0.02 and dist(o["pull_back"][2]) > 2 * dist(o["pull_back"][0]),
            "orbit half-way is 180 deg round": abs(((az(o["orbit"][1]) - az(o["orbit"][0])) % 360) - 180) < 1,
            "arc sweeps 60 deg": abs(((az(o["arc"][2]) - az(o["arc"][0])) % 360) - 60) < 1,
            "dolly_zoom widens fov": o["dolly_zoom"][2]["fov"] > o["dolly_zoom"][0]["fov"] + 10,
            "tracking follows a moving subject": o["tracking"][2]["l"][0] - o["tracking"][0]["l"][0] > 4,
            "turntable holds a quarter (front still at 1.2 s? no: quarter 1 hold)": abs(((az(o["turntable"][3]) - az(o["turntable"][0])) % 360) - 90) < 1,
            "whip pan swings the look 90 deg": abs(o["whip_pan"][2]["l"][0] - o["whip_pan"][0]["l"][0]) > 1,
            "focus = |pos - look|": all(abs(s["focus"] - dist(s)) < 1e-6 for k in kinds for s in o[k]),
        }

        def az_meas(m):     # the orbit render: background markers swing across the frame
            x = P(m, 3)[0]
            return float(np.nanmax(x) - np.nanmin(x))
        return [("measured orbit render sweeps the scene across the frame", lambda m, f: (az_meas(m) > 60, az_meas(m)), ">60 px")] + \
               [(k, (lambda v: lambda m, f: (v, v))(v), True) for k, v in sem.items()]
    return run3d(wd, "shot20", STICK, js, 4.0, 5, crits)


@card("CAM-165")
def cam165(task, wd):
    """Seeded handheld sway: three octaves of smooth sine noise around a ~1.3 (rad/s) sway, amplitude .012 x distance."""
    js = ("const A=K3.shot('medium',{subject:new TH.Vector3(0,1,0),size:1.7,handheld:true,seed:7}),"
          "B=K3.shot('medium',{subject:new TH.Vector3(0,1,0),size:1.7,handheld:true,seed:7}),C=K3.shot('medium',{subject:new TH.Vector3(0,1,0),size:1.7,handheld:true,seed:8}),"
          "Z=K3.shot('medium',{subject:new TH.Vector3(0,1,0),size:1.7});"
          "function update(t){const a=A(t); K3.applyShot(camera,a); return {a:a.pos.toArray(),b:B(t).pos.toArray(),c:C(t).pos.toArray(),z:Z(t).pos.toArray()};}")
    dur, fps = 30.0, 4

    def crits(r, T):
        x = np.array([fr["x"]["a"][0] - fr["x"]["z"][0] for fr in r["frames"]])
        d = np.linalg.norm(np.array(r["frames"][0]["x"]["z"]) - [0, 1, 0])
        spec = np.abs(np.fft.rfft(x - x.mean()))
        fr = np.fft.rfftfreq(len(x), 1 / fps) * 2 * math.pi
        peak = float(fr[1 + int(np.argmax(spec[1:]))])
        same = max(abs(a["x"]["a"][0] - a["x"]["b"][0]) for a in r["frames"])
        diff = max(abs(a["x"]["a"][0] - a["x"]["c"][0]) for a in r["frames"])
        mx = lambda m: P(m, 3)[0]
        return [("measured frame sways (background marker wanders > 1 px)", lambda m, f: (float(np.nanmax(mx(m)) - np.nanmin(mx(m))) > 1, float(np.nanmax(mx(m)) - np.nanmin(mx(m)))), ">1 px"),
                ("dominant sway frequency ~1.3 rad/s", lambda m, f: (abs(peak - 1.3) < 0.25, peak), 1.3),
                ("amplitude scales with .012 x distance (<= 1.0 of it)", lambda m, f: (0.3 * 0.012 * d < float(np.abs(x).max()) <= 0.012 * d * 1.01, [float(np.abs(x).max()), 0.012 * d]), "<=.012d"),
                ("seeded: same seed identical, another seed differs", lambda m, f: (same < 1e-12 and diff > 1e-3, [same, diff]), "0 / >0")]
    return run3d(wd, "handheld", STICK, js, dur, fps, crits)


@card("CAM-166")
def cam166(task, wd):
    """Shot from words: K3.shotFromWords parses a phrase into a camera, combining modifiers (low angle tracking, vertigo, handheld)."""
    ph = ["low angle tracking shot", "tracking shot", "slow push-in", "vertigo", "handheld close up", "a calm frame"]
    js = ("const PH=%s; const SS=PH.map(p=>K3.shotFromWords(p,{subject:new TH.Vector3(0,1,0),size:1.7,t0:0,t1:2}));"
          "function update(t){const i=Math.min(PH.length-1,Math.floor(t/2)); const s=SS[i](t-2*i); K3.applyShot(camera,s);"
          "return PH.map((p,j)=>{const a=SS[j](0),b=SS[j](2); return {p:a.pos.toArray(),p2:b.pos.toArray(),fov:a.fov,fov2:b.fov,l:a.look.toArray()};});}" % json.dumps(ph))

    def crits(r, T):
        o = r["frames"][0]["x"]
        d = lambda s, k: float(np.linalg.norm(np.array(s[k]) - [0, 1, 0]))
        sem = {"'low angle tracking shot' = tracking, lower than plain tracking": o[0]["p"][1] < o[1]["p"][1] - 0.5 and o[0]["p2"][0] - o[0]["p"][0] > 1,
               "'slow push-in' closes in": d(o[2], "p2") < d(o[2], "p") * 0.6,
               "'vertigo' = dolly zoom (fov widens)": o[3]["fov2"] > o[3]["fov"] + 10,
               "'handheld close up' = closeup distance": d(o[4], "p") < d(o[5], "p") * 0.5,
               "unknown words fall back to medium": abs(d(o[5], "p") - (1.7 / 0.55) / (2 * math.tan(math.radians(35) / 2))) < 0.1}
        return [("measured renders differ per phrase (subject size changes across shots)", lambda m, f: (np.nanmax(SC(m, 2)) / np.nanmin(SC(m, 2)) > 1.5, float(np.nanmax(SC(m, 2)) / np.nanmin(SC(m, 2)))), ">1.5")] + \
               [(k, (lambda v: lambda m, f: (v, v))(v), True) for k, v in sem.items()]
    return run3d(wd, "fromwords", STICK, js, 12.0, 2, crits)


SM_JS = "const sm=(a,b,x)=>K3.smooth(a,b,x), lerp=K3.lerp;"


@card("CAM-142")
def cam142(task, wd):
    """Keyed camera paths: cameraPath through keys for one smooth move, fov storm 38 - 4 smooth(9.5,12.8) + 4 smooth(12.8,15.2),
    focus distance = |p - l| x 0.9."""
    keys = [[0, 4.5, .42, 2.3, -2.6, -.12, -1.6], [5, 2.5, .8, 4.5, -1, 0.2, -1], [10, 0, 1.2, 6, 0, 0.5, 0], [17, -3, 2, 5, 0.5, 0.6, 0]]
    js = SM_JS + ("const C=K3.cameraPath(%s); function update(t){const [p,l]=C(t); camera.position.copy(p); camera.lookAt(l);"
                  "camera.fov=38-4*sm(9.5,12.8,t)+4*sm(12.8,15.2,t); return {focus:p.distanceTo(l)*0.9, d:p.distanceTo(l)};}" % json.dumps(keys))
    pts = [(-1, 0.3, -1, 0.3, RED), (2, 0.5, -4, 0.4, BLUE), (-3, 0.6, -5, 0.4, GREEN)]
    sm = lambda a, b, x: smoothstep((x - a) / (b - a))

    def crits(r, T):
        fov = [f["fov"] for f in r["frames"]]
        model = [38 - 4 * sm(9.5, 12.8, t) + 4 * sm(12.8, 15.2, t) for t in T]
        j1, j2 = idx(T, 12.8), idx(T, 17)
        return [("measured scene grows as the storm narrows the fov (12.8 s vs 9.5 s, camera nearly still)", lambda m, f: (P(m, 1)[0][j1] is not None and True, True), True),
                ("fov follows the storm curve (34 deg at 12.8 s, back to 38)", lambda m, f: (maxerr(fov, model) < 1e-6 and abs(fov[j1] - 34) < 1e-6 and abs(fov[j2] - 38) < 1e-6, [fov[j1], fov[j2]]), [34, 38]),
                ("focus = 0.9 x |p - l| every frame", lambda m, f: (max(abs(fr["x"]["focus"] - 0.9 * fr["x"]["d"]) for fr in f) < 1e-9, True), True),
                ("one smooth move: camera never stops between keys", lambda m, f: (float(_speed(f, T)[1:-1].min()) > 0.05, float(_speed(f, T)[1:-1].min())), ">0.05")]
    checks, outs = run3d(wd, "keyedpaths", pts, js, 17.0, 5, crits)
    # replace the placeholder first criterion with a real measured one: the far marker's apparent size tracks 1/tan(fov/2)
    fr = json.loads((wd / "keyedpaths_camera.json").read_text())
    T = [f["t"] for f in fr]
    m = track_colors(read_video(outs[0]), [hex2rgb(RED), hex2rgb(BLUE), hex2rgb(GREEN)], bg=(119, 119, 119))
    pr = np.array([f["P"][1][2] for f in fr])
    inside = np.array([f["P"][1][0] - f["P"][1][2] > 1 and f["P"][1][0] + f["P"][1][2] < 255 and f["P"][1][1] - f["P"][1][2] > 1
                       and f["P"][1][1] + f["P"][1][2] < 143 for f in fr])
    rr = rad(m, 1)
    good = (pr > 3) & np.isfinite(rr) & inside
    err = float(np.nanmax(np.abs(rr[good] / pr[good] - 1))) if good.any() else 9.0
    ok = err < 0.08 and good.sum() > 0.5 * len(T)
    checks[0] = check("measured marker radius matches THREE's projection through the storm", bool(ok), [err, int(good.sum())], "<8%")
    checks = [c for c in checks if not c["check"].startswith("negative control")]
    still = track_colors(read_video(wd / "keyedpaths_input.mp4"), [hex2rgb(RED), hex2rgb(BLUE), hex2rgb(GREEN)], bg=(119, 119, 119))
    ri = rad(still, 1)
    e_in = np.abs(ri[good] / pr[good] - 1)
    err_in = float(np.max(np.where(np.isfinite(e_in), e_in, 9.0)))
    checks.append(check("negative control: the unprocessed still does not match the projection", err_in > 0.08, err_in, ">0.08"))
    return checks, outs


@card("CAM-143")
def cam143(task, wd):
    """Veo shot words as explicit camera math: blue_hour 'slow push-in, low angle, road-level' = position (6.4-1.0e,
    1.5+0.2e, 16-7e), look (-8, 26, -420), e = smooth(0,8,t), fov 32; night_boat 'orbit 12 deg': angle 132-12e,
    radius 19-5.5e, height 1.55+.35e, fov 30."""
    js = SM_JS + ("let mode=0; function update(t){const e=sm(0,8,t<8?t:t-8); if(t<8){camera.fov=32; camera.position.set(6.4-1.0*e,1.5+0.2*e,16-7*e);"
                  " camera.lookAt(-8,26,-420);} else {const a=(132-12*e)*Math.PI/180, R=19-5.5*e; camera.fov=30;"
                  " camera.position.set(Math.sin(a)*R,1.55+.35*e,Math.cos(a)*R); camera.lookAt(0,1,0);} return {e};}")
    pts = [(4, 0.4, 0, 0.5, RED), (0, 1, 0, 0.6, BLUE), (-6, 1, -30, 2, GREEN)]

    def crits(r, T):
        p = pos(r["frames"])
        a = [math.degrees(math.atan2(q[0], q[2])) for q in p[idx(T, 8):]]
        return [("push-in: the road-level marker grows on screen", lambda m, f: (rad(m, 0)[idx(T, 7.5)] > 1.4 * rad(m, 0)[0], [float(rad(m, 0)[0]), float(rad(m, 0)[idx(T, 7.5)])]), ">1.4x"),
                ("road-level low camera (1.5-1.7 m) pitched upward to the far look point", lambda m, f: (1.5 <= p[:idx(T, 7.9), 1].min() and p[:idx(T, 7.9), 1].max() <= 1.7, [float(p[:idx(T, 7.9), 1].min()), float(p[:idx(T, 7.9), 1].max())]), [1.5, 1.7]),
                ("night_boat orbit sweeps 12 deg and closes 19 -> 13.5", lambda m, f: (abs((a[0] - a[-1]) - 12) < 0.2 and abs(np.hypot(p[-1][0], p[-1][2]) - 13.5) < 0.05, [a[0] - a[-1], float(np.hypot(p[-1][0], p[-1][2]))]), [12, 13.5])]
    return run3d(wd, "veomath", pts, js, 16.0, 2, crits)


@card("CAM-144")
def cam144(task, wd):
    """Project a 3D point to screen for a HUD callout: proj = mid.project(camera); sx = (x*.5+.5)W, sy = (-y*.5+.5)H; the 2D
    label (leader 150 px at -45 deg at 1080p) follows the 3D member exactly while the camera orbits."""
    js = ("function update(t){const a=t*0.6; camera.position.set(Math.sin(a)*6,2+0.5*Math.sin(t),Math.cos(a)*6); camera.lookAt(0,1,0);"
          "camera.updateMatrixWorld(true); const v=new TH.Vector3(0.8,1.4,0.3).project(camera); return [(v.x*.5+.5)*W,(-v.y*.5+.5)*H];}")
    pts = [(0.8, 1.4, 0.3, 0.12, RED), (0, 1, 0, 0.3, BLUE)]

    def crits(r, T):
        tag = [fr["x"] for fr in r["frames"]]
        lead = 150 * 144 / 1080
        # paint the callout (leader + box) at the projected point onto the output frames and re-measure both
        from PIL import Image, ImageDraw
        frames = read_video(r["video"])
        outf = []
        for fr, (sx, sy) in zip(frames, tag):
            im = Image.fromarray(fr.astype(np.uint8))
            d = ImageDraw.Draw(im)
            ex, ey = sx + lead * math.cos(math.radians(-45)), sy + lead * math.sin(math.radians(-45))
            d.line([(sx, sy), (ex, ey)], fill=(255, 255, 0), width=1)
            d.rectangle([ex, ey - 6, ex + 30, ey], outline=(0, 255, 255))
            outf.append(np.asarray(im))
        write_video(wd / "callout.mp4", outf, 10)
        cb = read_video(wd / "callout.mp4")

        def start_err(m):
            errs = []
            for i, v in enumerate(m):
                if not v[0]:
                    continue
                yy, xx = np.nonzero((np.abs(cb[i].astype(float) - [255, 255, 0]).max(-1) < 60))
                if len(xx) == 0:
                    return 99
                j = int(np.argmin(np.hypot(xx - v[0]["cx"], yy - v[0]["cy"])))
                errs.append(math.hypot(xx[j] + 0.5 - v[0]["cx"], yy[j] + 0.5 - v[0]["cy"]))
            return max(errs)
        indep = max(math.hypot(*(np.array(pinhole(fr["pos"], (0, 1, 0), 35, (0.8, 1.4, 0.3))) - fr["x"])) for fr in r["frames"])
        return [("the callout's leader starts on the measured 3D member every frame", lambda m, f: (start_err(m) < 1.6, start_err(m)), "<1.6 px"),
                ("THREE's projection equals an independent pinhole projection", lambda m, f: (indep < 0.05, indep), "<0.05 px"),
                ("the member actually travels across the frame (orbit)", lambda m, f: (float(np.nanmax(P(m, 0)[0]) - np.nanmin(P(m, 0)[0])) > 30, float(np.nanmax(P(m, 0)[0]) - np.nanmin(P(m, 0)[0]))), ">30")]
    checks, outs = run3d(wd, "hudproject", pts, js, 4.0, 10, crits)
    return checks, outs + [wd / "callout.mp4"]


@card("CAM-146")
def cam146(task, wd):
    """Dolly-in arc: n=t/DUR; angle = n*PI*0.5+0.3; dist = 9.5-2.2n; x=sin(angle)dist, z=cos(angle)dist, y=sin(n PI)*1.5+.5;
    lookAt(0,0,0); FOV 45."""
    DUR = 4.0
    js = ("function update(t){const n=t/%s, a=n*Math.PI*0.5+0.3, d=9.5-2.2*n; camera.fov=45; camera.position.set(Math.sin(a)*d,Math.sin(n*Math.PI)*1.5+0.5,Math.cos(a)*d);"
          "camera.lookAt(0,0,0);}" % DUR)
    pts = [(0, 0, 0, 0.6, RED), (3, 0, -3, 0.4, BLUE)]

    def crits(r, T):
        p = pos(r["frames"])
        ang = [math.degrees(math.atan2(q[0], q[2])) for q in p]
        dist = np.hypot(p[:, 0], p[:, 2])
        return [("subject always centred (lookAt) and grows by 9.5/7.3 (measured)", lambda m, f: (float(np.nanmax(offc(m, 0, 256, 144))) < 0.8 and abs(rad(m, 0)[-1] / rad(m, 0)[0] - np.linalg.norm(p[0]) / np.linalg.norm(p[-1])) < 0.04,
                                                                                               [float(np.nanmax(offc(m, 0, 256, 144))), float(rad(m, 0)[-1] / rad(m, 0)[0])]), ["<0.8", float(np.linalg.norm(p[0]) / np.linalg.norm(p[-1]))]),
                ("orbit a quarter turn", lambda m, f: (abs(ang[-1] - ang[0] - 90) < 0.1, ang[-1] - ang[0]), 90),
                ("distance 9.5 -> 7.3", lambda m, f: (abs(dist[0] - 9.5) < 1e-6 and abs(dist[-1] - 7.3) < 1e-6, [float(dist[0]), float(dist[-1])]), [9.5, 7.3]),
                ("height bob peaks 2.0 mid-clip", lambda m, f: (abs(p[idx(T, DUR / 2), 1] - 2.0) < 1e-6, float(p[idx(T, DUR / 2), 1])), 2.0)]
    return run3d(wd, "arcdolly", pts, js, DUR, 10, crits)


@card("CAM-148")
def cam148(task, wd):
    """Spline camera flights and eased dollies: CatmullRomCurve3 flythrough rising to the tower with roll .12 -> -.08, a
    dive with roll .25 -> 0; one readable move per shot."""
    js = ("const C=new TH.CatmullRomCurve3([[0,2,20],[4,3,10],[2,6,2],[0,12,-4]].map(a=>new TH.Vector3(...a)));"
          "function update(t){ if(t<=4){const u=t/4; camera.position.copy(C.getPoint(u)); camera.up.set(0,1,0); camera.lookAt(0,10,-20); camera.rotateZ(lerp(.12,-.08,u)); return {roll:lerp(.12,-.08,u)};}"
          " const u=(t-4)/2, e=u*u*(3-2*u); camera.position.set(0,lerp(30,8,e),lerp(-30,-10,e)); camera.up.set(0,1,0); camera.lookAt(0,0,0); camera.rotateZ(lerp(.25,0,u)); return {roll:lerp(.25,0,u)};}"
          ).replace("lerp(", "K3.lerp(")
    pts = [(-4, 4, -20, 0.6, RED), (4, 4, -20, 0.6, BLUE), (0, 10, -20, 1.0, GREEN)]

    def crits(r, T):
        def tilt(m, i):                         # a camera roll turns the horizon the other way on screen
            a, b = m[i][0], m[i][1]
            return None if not (a and b) else -math.degrees(math.atan2(-(b["cy"] - a["cy"]), b["cx"] - a["cx"]))
        rolls = [math.degrees(fr["x"]["roll"]) for fr in r["frames"]]
        i0, i1 = 0, idx(T, 3.0)
        return [("measured horizon tilt follows the roll (.12 -> -.08 rad)", lambda m, f: (tilt(m, i0) is not None and tilt(m, i1) is not None and abs(tilt(m, i0) - rolls[i0]) < 2.5 and abs(tilt(m, i1) - rolls[i1]) < 2.5,
                                                                                          [tilt(m, i0), tilt(m, i1)]), [rolls[i0], rolls[i1]]),
                ("flythrough rises to the tower", lambda m, f: (pos(f)[i1][1] > pos(f)[0][1] + 4, [pos(f)[0][1], pos(f)[i1][1]]), "rising"),
                ("dive roll settles .25 -> 0", lambda m, f: (abs(rolls[idx(T, 4.1)] - math.degrees(.25 * (1 - 0.05))) < 0.05 and abs(rolls[-1]) < 1e-6, [rolls[idx(T, 4.1)], rolls[-1]]), [13.6, 0])]
    return run3d(wd, "splineflight", pts, js, 6.0, 10, crits)


@card("CAM-139")
def cam139(task, wd):
    """3D orbit with push-in, break shake and pull-back: ang = lerp(.42,-.3,easeInOut(t/5)) + .06 sin(.9t); push =
    smooth(load, brk+.1)(1-smooth(swap+.3, rank+.4)); dist 1.95 -> 1.8 (+.14 end pull); shake = exp(-9(t-T_BREAK))*.006."""
    LOAD, BRK, SWAP, RANK = 0.8, 2.0, 3.0, 4.0
    js = SM_JS + ("const L=%s,B=%s,S=%s,R=%s; const eio=x=>x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2;"
                  "function update(t){const ang=K3.lerp(.42,-.3,eio(Math.min(1,t/5)))+.06*Math.sin(.9*t); const push=sm(L,B+.1,t)*(1-sm(S+.3,R+.4,t));"
                  " const dist=1.95-0.15*push+0.14*sm(R+.4,5,t); const sh=t>B?Math.exp(-9*(t-B))*.006:0;"
                  " camera.position.set(Math.sin(ang)*dist+sh*Math.sin(97*t),0.6+sh*Math.cos(83*t),Math.cos(ang)*dist); camera.lookAt(0,0.4,0); return {dist,sh,push};}"
                  % (LOAD, BRK, SWAP, RANK))
    pts = [(0, 0.4, 0, 0.12, RED), (0.5, 0.2, -0.6, 0.06, BLUE)]

    def crits(r, T):
        sh = np.array([fr["x"]["sh"] for fr in r["frames"]])
        d = np.array([fr["x"]["dist"] for fr in r["frames"]])
        jb = idx(T, BRK + 0.04)
        return [("measured subject grows during the push and shrinks on the pull-back", lambda m, f: (rad(m, 0)[idx(T, 3.0)] > 1.05 * rad(m, 0)[0] and rad(m, 0)[-1] < rad(m, 0)[idx(T, 3.0)] / 1.1,
                                                                                                      [float(rad(m, 0)[0]), float(rad(m, 0)[idx(T, 3.0)]), float(rad(m, 0)[-1])]), "grow then shrink"),
                ("break shake decays exp(-9 dt)", lambda m, f: (abs(sh[idx(T, BRK + 0.3)] / sh[jb] - math.exp(-9 * (T[idx(T, BRK + 0.3)] - T[jb]))) < 1e-6, float(sh[idx(T, BRK + 0.3)] / sh[jb])), math.exp(-9 * 0.28)),
                ("dist 1.95 -> 1.8 at the push, +.14 pull at the end", lambda m, f: (abs(d[idx(T, 2.5)] - 1.8) < 1e-6 and abs(d[-1] - 2.09) < 1e-3, [float(d[idx(T, 2.5)]), float(d[-1])]), [1.8, 2.09])]
    return run3d(wd, "breakorbit", pts, js, 5.0, 25, crits)


@card("CAM-141")
def cam141(task, wd):
    """Hermite camera keys with bullet time: velocity-continuous keys (tangents (k2-k0)/(t2-t0)*h); between STOP 6.0 and
    START 7.2 the world freezes while the camera keeps orbiting; fov = 36 + 3.5 kick - 2.5 smooth(STOP,FREEZE)(1-smooth(START,HOME))."""
    keys = [[0, 0, 6, 1.5, 0, 1], [2, 40, 5.5, 1.6, 0, 1], [4, 90, 5, 2, 0, 1], [6, 150, 4.5, 1.8, 0, 1], [8, 220, 5, 1.5, 0, 1], [10, 270, 6, 1.4, 0, 1]]
    js = SM_JS + ("const K=%s, STOP=6.0, FREEZE=6.75, START=7.2, HOME=7.85;"
                  "function herm(t){let i=0; while(i<K.length-2&&t>K[i+1][0]) i++; const a=K[i],b=K[i+1],h=b[0]-a[0],u=(t-a[0])/h;"
                  " const tan=(j,c)=>{const p=K[Math.max(0,j-1)],n=K[Math.min(K.length-1,j+1)]; return (n[c]-p[c])/(n[0]-p[0])*h;};"
                  " const h00=2*u*u*u-3*u*u+1,h10=u*u*u-2*u*u+u,h01=-2*u*u*u+3*u*u,h11=u*u*u-u*u;"
                  " return [1,2,3,4,5].map(c=>h00*a[c]+h10*tan(i,c)+h01*b[c]+h11*tan(i+1,c));}"
                  "function tape(t){ if(t<STOP) return t; if(t<START) return STOP; return STOP+(t-START); }"
                  "function update(t){const [ang,d,hh,lx,ly]=herm(t); const A=ang*Math.PI/180; camera.position.set(Math.sin(A)*d,hh,Math.cos(A)*d); camera.lookAt(lx,ly,0);"
                  " camera.fov=36-2.5*sm(STOP,FREEZE,t)*(1-sm(START,HOME,t)); const w=tape(t); PTS[1][0]=Math.sin(w*1.2)*2; return {w, ball:PTS[1][0]};}"
                  % json.dumps(keys))
    pts = [(0, 1, 0, 0.3, RED), (0, 0.5, 1.5, 0.25, BLUE), (1.2, 1.3, -1.0, 0.2, GREEN)]

    def crits(r, T):
        p = pos(r["frames"])
        v = np.gradient(p, T, axis=0)
        kk = [idx(T, k[0]) for k in keys[1:-1]]
        jump = max(float(np.linalg.norm(v[i + 1] - v[i - 1])) for i in kk)
        typ = float(np.median(np.linalg.norm(np.diff(v, axis=0), axis=1))) * 2
        ball = np.array([fr["x"]["ball"] for fr in r["frames"]])
        a, b = idx(T, 6.1), idx(T, 7.1)
        return [("measured: the world (ball) freezes in bullet time while the frame keeps moving", lambda m, f: (abs(ball[b] - ball[a]) < 1e-9 and abs(P(m, 2)[0][b] - P(m, 2)[0][a]) > 3,
                                                                                                                [float(ball[b] - ball[a]), float(P(m, 2)[0][b] - P(m, 2)[0][a])]), ["0", ">3 px"]),
                ("velocity-continuous through every key (Hermite C1)", lambda m, f: (jump < 3 * typ + 1e-3, [jump, typ]), "no kink"),
                ("fov dips 2.5 deg in the freeze and returns", lambda m, f: (abs(f[idx(T, 7.0)]["fov"] - 33.5) < 1e-6 and abs(f[-1]["fov"] - 36) < 1e-6, [f[idx(T, 7.0)]["fov"], f[-1]["fov"]]), [33.5, 36])]
    return run3d(wd, "bullettime", pts, js, 10.0, 10, crits)


def _orbit_walk(wd, name, stops, drift, extra=None, fps=8):
    """lab-kit K3.orbitWalk(camera, stops, {drift}): ease between stops, hold at each with micro drift, shorter way round."""
    js = ("const OW=K3.orbitWalk(camera,%s,{drift:%s}); function update(t){OW(t); return {look:OW.lookPoint.toArray(), fov:OW.fov};}"
          % (json.dumps(stops), drift))
    fixed_look = all(s["look"] == [0, 1, 0] for s in stops)
    pts = [(0, 1, 0, 0.15, RED), (2, 1.2, 1.0, 0.08, BLUE), (-2, 0.3, -2, 0.3, GREEN)]
    dur = stops[-1]["t"] + (stops[-1].get("hold") or 0) + 0.5

    def crits(r, T):
        f = r["frames"]
        p = pos(f)
        lk = np.array([fr["x"]["look"] for fr in f])
        az = np.degrees(np.arctan2(p[:, 0] - lk[:, 0], p[:, 2] - lk[:, 2]))
        res = []
        for s in stops:
            a = min(j for j in range(len(T)) if T[j] >= s["t"] - 1e-9)
            b = max([j for j in range(len(T)) if T[j] <= s["t"] + (s.get("hold") or 0) + 1e-9] or [a])
            dev = float(np.abs(p[a:b + 1] - p[a]).max()) if b > a else 0.0
            res.append((round(float(az[a]), 2), round(float(np.hypot(p[a, 0] - lk[a, 0], p[a, 2] - lk[a, 2])), 3), round(dev, 4)))
        steps = [((b["angle"] - a["angle"] + 540) % 360) - 180 for a, b in zip(stops, stops[1:])]
        walked = [float(((az[idx(T, b["t"])] - az[idx(T, a["t"])] + 540) % 360) - 180) for a, b in zip(stops, stops[1:])]
        def clear(i):                          # frames where no other marker overlaps the subject's disc on screen
            P0 = r["frames"][i]["P"]
            return all(math.hypot(P0[k][0] - P0[0][0], P0[k][1] - P0[0][1]) > P0[k][2] + P0[0][2] + 1 for k in range(1, len(P0)))
        okf = [i for i in range(len(T)) if clear(i)]
        cen = (lambda m: float(np.nanmax(offc(m, 0, 256, 144)[okf]))) if fixed_look else (lambda m: 0.0)
        c = [("measured: the frame walks round the subject (scene sweeps, fixed look stays centred)", lambda m, f2: (cen(m) < 1.2 and float(np.nanmax(P(m, 2)[0]) - np.nanmin(P(m, 2)[0])) > 20,
                                                                                                  [cen(m), float(np.nanmax(P(m, 2)[0]) - np.nanmin(P(m, 2)[0]))]), ["<1.2", ">20 px sweep"]),
             ("camera on each stop's angle and distance (within the micro drift)", lambda m, f2: (all(abs(((a - s["angle"] + 540) % 360) - 180) < 0.2 + math.degrees(math.atan(2 * drift / s["dist"])) and abs(d - s["dist"]) < 0.05 for (a, d, _), s in zip(res, stops)),
                                                                          [(a, d) for a, d, _ in res]), [(s["angle"], s["dist"]) for s in stops]),
             ("holds: only micro drift (<= 2 x drift) during each hold", lambda m, f2: (all(dv <= 2 * drift + 1e-6 for _, _, dv in res), [dv for _, _, dv in res]), "<=%.3f" % (2 * drift)),
             ("walks the shorter way round", lambda m, f2: (all(abs(w - s) < 1.5 for w, s in zip(walked, steps)), walked), steps)]
        return c + (extra(r, T) if extra else [])
    return run3d(wd, name, pts, js, dur, fps, crits, extra_scripts=[LABKIT])


@card("CAM-20")
def cam20(task, wd):
    """Orbit walk with stops: a lens walks the circle round the hero object and holds at parts with micro drift (.012)."""
    return _orbit_walk(wd, "orbitwalk", [{"t": 0, "angle": 20, "dist": 5, "height": 1.6, "look": [0, 1, 0], "hold": 0.8},
                                          {"t": 2.5, "angle": 110, "dist": 4, "height": 1.4, "look": [0, 1, 0], "hold": 1.0},
                                          {"t": 5, "angle": -150, "dist": 4.5, "height": 2.0, "look": [0, 1, 0], "hold": 0.8}], 0.012)


@card("CAM-134")
def cam134(task, wd):
    """orbitWalk camera: walks around the target holding at each stop (four stops, wrap-around shorter path)."""
    return _orbit_walk(wd, "orbitwalk4", [{"t": 0, "angle": 170, "dist": 6, "height": 1.8, "look": [0, 1, 0], "hold": 0.5},
                                           {"t": 2, "angle": -160, "dist": 5, "height": 1.5, "look": [0, 1, 0], "hold": 0.5},
                                           {"t": 4, "angle": -90, "dist": 4, "height": 1.2, "look": [0, 1, 0], "hold": 0.5},
                                           {"t": 6, "angle": 0, "dist": 5, "height": 2.2, "look": [0, 1, 0], "hold": 0.5}], 0.012)


def _lab_tour(wd, name):
    st = [{"t": 0, "angle": 28, "dist": 6.4, "height": 2.1, "look": [0, 1, 0], "fov": 30},
          {"t": 3, "angle": -35, "dist": 2.3, "height": 1.75, "look": [0, 1.3, 0], "hold": 1.2, "fov": 32},
          {"t": 6.5, "angle": -5, "dist": 1.0, "height": 1.45, "look": [0, 1.4, 0.1], "hold": 0.8, "fov": 26},
          {"t": 9.5, "angle": 60, "dist": 3.0, "height": 1.8, "look": [0, 1, 0], "hold": 0.8, "fov": 32},
          {"t": 13, "angle": 28, "dist": 6.4, "height": 2.1, "look": [0, 1, 0], "fov": 30}]

    def extra(r, T):
        fov = [fr["x"]["fov"] for fr in r["frames"]]
        p = pos(r["frames"])
        return [("eye extreme close-up narrows the fov to 26", lambda m, f: (abs(fov[idx(T, 6.9)] - 26) < 1e-6, fov[idx(T, 6.9)]), 26),
                ("returns to the opening wide frame", lambda m, f: (float(np.abs(p[-1] - p[0]).max()) < 0.03, float(np.abs(p[-1] - p[0]).max())), "<0.03")]
    return _orbit_walk(wd, name, st, 0.012, extra, fps=5)


@card("CAM-140")
def cam140(task, wd):
    """Orbit walk with stops and holds (head hold 1.2, eye extreme close-up fov 26, back to the opening wide)."""
    return _lab_tour(wd, "labtour")


@card("CAM-177")
def cam177(task, wd):
    """Orbit-walk lens with holds (lab/HUD documentary move: t0 28/6.4, t3 -35/2.3 hold 1.2, t6.5 eye dist 1.0 fov 26)."""
    return _lab_tour(wd, "labtour177")


@card("CAM-250")
def cam250(task, wd):
    """Chase camera with lag: camera.position lerps toward ball + offset(2,3,5) by 0.06 per frame, lookAt a smoothed
    target, the offset rotating slowly."""
    js = ("const cp=new TH.Vector3(2,3,5), lt=new TH.Vector3(0,0.5,0); let fr=0;"
          "function ball(t){return new TH.Vector3(t<3?4*t:12, 0.5, 0);}"
          "function update(t){const b=ball(t); const a=0.05*t; const off=new TH.Vector3(2*Math.cos(a)-5*Math.sin(a),3,2*Math.sin(a)+5*Math.cos(a));"
          " cp.lerp(b.clone().add(off),0.06); lt.lerp(b,0.12); camera.position.copy(cp); camera.lookAt(lt); PTS[0][0]=b.x;"
          " return {gap:cp.distanceTo(b.clone().add(off)), tg:b.clone().add(off).toArray(), bx:b.x};}")
    pts = [(0, 0.5, 0, 0.4, RED), (6, 0.2, -3, 0.3, BLUE), (12, 0.2, 3, 0.3, GREEN)]
    fps = 30

    def crits(r, T):
        p = pos(r["frames"])
        tg = np.array([fr["x"]["tg"] for fr in r["frames"]])
        i3 = idx(T, 3.0)
        rec = float(max(np.abs(p[n] - (p[n - 1] + 0.06 * (tg[n] - p[n - 1]))).max() for n in range(1, len(T))))
        off = offc(r["meas"], 0, 256, 144)
        return [("measured: the ball drifts off centre while chasing, then the lagging camera re-centres it", lambda m, f: (float(np.nanmax(offc(m, 0, 256, 144)[:i3])) > 8 and float(offc(m, 0, 256, 144)[-1]) < 2.5,
                                                                                                                     [float(np.nanmax(offc(m, 0, 256, 144)[:i3])), float(offc(m, 0, 256, 144)[-1])]), [">8", "<2.5"]),
                ("every frame: position = lerp(previous, ball + rotating offset, 0.06)", lambda m, f: (rec < 1e-5, rec), "<1e-5")]
    return run3d(wd, "chasecam", pts, js, 5.0, fps, crits)


@card("CAM-263")
def cam263(task, wd):
    """Chase camera with bank: lerp the camera behind the target (0.1/frame); roll proportional to lateral velocity,
    clamped to 25 deg."""
    js = ("const cp=new TH.Vector3(0,2,6); let prev=null; function tgt(t){return new TH.Vector3(6*Math.sin(t*1.2), 0.5, -4*t);}"
          "function update(t){const b=tgt(t), b2=tgt(t+1/30); const vx=(b2.x-b.x)*30; cp.lerp(b.clone().add(new TH.Vector3(0,2,6)),0.1);"
          " camera.position.copy(cp); camera.up.set(0,1,0); camera.lookAt(b); const roll=Math.max(-25,Math.min(25,-4.2*vx))*Math.PI/180; camera.rotateZ(roll);"
          " PTS.forEach((p,i)=>{ if(i<2){ p[2]=b.z-20; } }); return {roll, vx};}")
    pts = [(-6, 0.5, -20, 0.6, RED), (6, 0.5, -20, 0.6, BLUE), (0, 0.5, 0, 0.3, GREEN)]
    fps = 30

    def crits(r, T):
        rolls = np.degrees([fr["x"]["roll"] for fr in r["frames"]])
        vx = np.array([fr["x"]["vx"] for fr in r["frames"]])

        def tilt(m):
            out = []
            for v in m:
                a, b = v[0], v[1]
                out.append(-math.degrees(math.atan2(-(b["cy"] - a["cy"]), b["cx"] - a["cx"])) if a and b else np.nan)
            return np.array(out)
        ok = lambda m: np.isfinite(tilt(m))
        corr = lambda m: float(np.corrcoef(tilt(m)[ok(m)], rolls[ok(m)])[0, 1]) if ok(m).sum() > 10 and np.std(tilt(m)[ok(m)]) > 0.5 else 0.0
        return [("measured horizon banks with the roll (correlation)", lambda m, f: (corr(m) > 0.9, corr(m)), ">0.9"),
                ("roll proportional to lateral velocity, clamped at 25 deg", lambda m, f: (float(np.abs(rolls).max()) <= 25 + 1e-9 and abs(float(np.abs(rolls).max()) - 25) < 1e-6
                                                                                          and float(np.corrcoef(rolls[np.abs(rolls) < 24.9], vx[np.abs(rolls) < 24.9])[0, 1]) < -0.999,
                                                                                          float(np.abs(rolls).max())), 25)]
    return run3d(wd, "chasebank", pts, js, 5.0, fps, crits)


GROUND_SQ = [(-1, 0, -1, 0.12, RED), (1, 0, -1, 0.12, BLUE), (1, 0, 1, 0.12, GREEN), (-1, 0, 1, 0.12, YEL)]


def quad_aspect(m, i):
    v = m[i]
    if not all(v[:4]):
        return None
    pts = np.array([[v[k]["cx"], v[k]["cy"]] for k in range(4)])
    w = (np.linalg.norm(pts[1] - pts[0]) + np.linalg.norm(pts[2] - pts[3])) / 2
    h = (np.linalg.norm(pts[3] - pts[0]) + np.linalg.norm(pts[2] - pts[1])) / 2
    return float(h / w)


@card("CAM-219")
def cam219(task, wd):
    """Crane to top-down hero end card: lerp the camera from a low 3/4 view to overhead over 2 s easeInOutCubic (final FOV
    35); the tagline/logo overlay fades in over 500 ms after."""
    js = ("const A=new TH.Vector3(0,1.2,5), B=new TH.Vector3(0,7,0.001); const e=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;"
          "function update(t){const u=Math.min(1,t/2); camera.position.lerpVectors(A,B,e(u)); camera.fov=K3.lerp(45,35,e(u)); camera.lookAt(0,0,0);"
          " return {logo:Math.min(1,Math.max(0,(t-2)/0.5))};}")

    def crits(r, T):
        logo = [fr["x"]["logo"] for fr in r["frames"]]
        return [("measured ground square: foreshortened at the start, a true square from overhead", lambda m, f: (quad_aspect(m, 0) is not None and quad_aspect(m, 0) < 0.75 and abs(quad_aspect(m, -1) - 1) < 0.03,
                                                                                                                 [quad_aspect(m, 0), quad_aspect(m, -1)]), ["<0.75", 1.0]),
                ("final fov 35 and overhead", lambda m, f: (abs(f[-1]["fov"] - 35) < 1e-6 and pos(f)[-1][1] > 6.9, [f[-1]["fov"], pos(f)[-1][1]]), [35, 7]),
                ("overlay fades in over 500 ms after the crane", lambda m, f: (logo[idx(T, 2.0)] == 0 and abs(logo[idx(T, 2.25)] - 0.5) < 0.05 and logo[-1] == 1, [logo[idx(T, 2.0)], logo[idx(T, 2.25)], logo[-1]]), [0, 0.5, 1])]
    return run3d(wd, "cranetop", GROUND_SQ, js, 2.6, 20, crits)


@card("CAM-230")
def cam230(task, wd):
    """Turntable orbit showcase: the camera orbits 30-60 deg/s around the model (45 deg/s here) at constant radius."""
    js = "function update(t){const a=(45*t+10)*Math.PI/180; camera.position.set(Math.sin(a)*5,1.6,Math.cos(a)*5); camera.lookAt(0,0.6,0);}"
    pts = [(0, 0.6, 0, 0.4, RED), (1.2, 0.6, 0, 0.15, BLUE), (0, 0.6, 1.2, 0.15, GREEN)]

    def crits(r, T):
        p = pos(r["frames"])
        az = np.unwrap(np.arctan2(p[:, 0], p[:, 2]))
        rate = float(np.degrees(np.polyfit(T, az, 1)[0]))
        x = P(r["meas"], 1)[0]
        return [("measured: model features swing across the frame", lambda m, f: (float(np.nanmax(P(m, 1)[0]) - np.nanmin(P(m, 1)[0])) > 30, float(np.nanmax(P(m, 1)[0]) - np.nanmin(P(m, 1)[0]))), ">30 px"),
                ("orbit rate within 30-60 deg/s and constant", lambda m, f: (30 <= rate <= 60 and float(np.abs(np.degrees(np.diff(az)) * 10 - rate).max()) < 1e-3, rate), 45),
                ("constant radius", lambda m, f: (float(np.ptp(np.hypot(p[:, 0], p[:, 2]))) < 1e-6, True), True)]
    return run3d(wd, "turntable", pts, js, 4.0, 10, crits)


@card("CAM-278")
def cam278(task, wd):
    """Orbit push-in: tween the OrbitControls target and distance over 4 s ease (spherical coordinates kept)."""
    js = ("const T0=new TH.Vector3(0,1,0), T1=new TH.Vector3(0.6,1.3,0.2); const e=x=>x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2;"
          "const sph=new TH.Spherical(8, 1.2, 0.6); function update(t){const u=e(Math.min(1,t/4)); const tg=T0.clone().lerp(T1,u); const s=sph.clone(); s.radius=K3.lerp(8,3,u);"
          " camera.position.setFromSpherical(s).add(tg); camera.lookAt(tg); return {tg:tg.toArray(), r:s.radius};}")
    pts = [(0.6, 1.3, 0.2, 0.15, RED), (0, 1, 0, 0.3, BLUE), (-1.5, 0.5, -1, 0.3, GREEN)]

    def crits(r, T):
        rr = [fr["x"]["r"] for fr in r["frames"]]
        tg = np.array([fr["x"]["tg"] for fr in r["frames"]])
        dirs = (pos(r["frames"]) - tg) / np.array(rr)[:, None]
        return [("measured: the new target ends centred and 8/3 larger", lambda m, f: (float(offc(m, 0, 256, 144)[-1]) < 0.8 and abs(rad(m, 0)[-1] / rad(m, 0)[0] - 8 / 3 * 1.0) < 0.35,
                                                                                    [float(offc(m, 0, 256, 144)[-1]), float(rad(m, 0)[-1] / rad(m, 0)[0])]), ["<0.8", "~2.7"]),
                ("distance 8 -> 3 with an inOut ease", lambda m, f: (abs(rr[-1] - 3) < 1e-9 and abs(rr[idx(T, 2)] - 5.5) < 1e-6, [rr[idx(T, 2)], rr[-1]]), [5.5, 3]),
                ("orbit angles kept (same spherical direction)", lambda m, f: (float(np.abs(dirs - dirs[0]).max()) < 1e-6, True), True)]
    return run3d(wd, "orbitpush", pts, js, 4.0, 10, crits)


@card("CAM-217")
def cam217(task, wd):
    """Push-in camera dolly: from wide to a mascot close-up over 3 s ease-in-out, with depth-of-field on the background
    (blur grows with distance from the focus plane)."""
    js = ("const e=x=>x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2; function update(t){const u=e(Math.min(1,t/3)); camera.position.set(0,1.2,K3.lerp(11,2.2,u)); camera.lookAt(0,1,0);"
          " return {focus:camera.position.distanceTo(new TH.Vector3(0,1,0))};}")
    pts = [(0, 1, 0, 0.45, RED), (2.0, 1.2, -6, 0.5, BLUE), (-2.2, 1.0, -8, 0.5, GREEN)]
    T = [round(i / 10, 6) for i in range(31)]
    r = cam3d(wd, "pushdof", pts, js, T, 10)
    # depth of field applied per marker: blur radius proportional to |depth - focus| / depth (thin-lens circle of confusion)
    from PIL import Image, ImageDraw, ImageFilter
    frames = []
    for fr in r["frames"]:
        im = Image.new("RGB", (256 * 4, 144 * 4), (119, 119, 119))
        for i in sorted(range(len(pts)), key=lambda i: -fr["P"][i][3]):
            sx, sy, sr, dz = fr["P"][i]
            coc = 6.0 * abs(dz - fr["x"]["focus"]) / max(dz, 1e-3)
            layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
            ImageDraw.Draw(layer).ellipse([(sx - sr) * 4, (sy - sr) * 4, (sx + sr) * 4, (sy + sr) * 4], fill=hex2rgb(pts[i][4]) + (255,))
            if coc > 0.2:
                layer = layer.filter(ImageFilter.GaussianBlur(coc * 4))
            im.paste(layer, (0, 0), layer)
        frames.append(np.asarray(im.resize((256, 144), Image.BOX)))
    vid = write_video(wd / "pushdof_dof.mp4", frames, 10)
    v = read_video(vid)
    vin = read_video(r["input"])
    m = track_colors(v, [hex2rgb(RED)], bg=(119, 119, 119))
    frac_ = [(b[0]["y1"] - b[0]["y0"] + 1) / 144 if b[0] else 0 for b in m]
    sb = [sharp(v[i], hex2rgb(BLUE)) for i in (0, len(T) - 1)]
    sr = [sharp(v[i], hex2rgb(RED)) for i in (0, len(T) - 1)]
    coc_b = [6.0 * abs(fr["P"][1][3] - fr["x"]["focus"]) / fr["P"][1][3] for fr in (r["frames"][0], r["frames"][-1])]
    checks = [check("wide to close-up: mascot grows from <15% to >45% of frame height", frac_[0] < 0.15 and frac_[-1] > 0.45, [frac_[0], frac_[-1]], ["<0.15", ">0.45"]),
              check("measured: mascot sharp, background soft at the close-up", sr[-1] > 0.8 and sb[-1] < 0.6 * sr[-1], [sr[-1], sb[-1]], "red sharp, blue < 0.6x"),
              check("background circle of confusion grows as focus pulls in", coc_b[1] > coc_b[0], coc_b, "growing"),
              check("ease-in-out: slow start", r["frames"][3]["pos"][2] > 11 - 0.05 * 8.8, r["frames"][3]["pos"][2], ">10.56"),
              check("negative control: the unprocessed still never pushes in", not ((blob(vin[-1], hex2rgb(RED), bg=(119, 119, 119))["y1"] - blob(vin[-1], hex2rgb(RED), bg=(119, 119, 119))["y0"] + 1) / 144 > 0.45),
                    (blob(vin[-1], hex2rgb(RED), bg=(119, 119, 119))["y1"] - blob(vin[-1], hex2rgb(RED), bg=(119, 119, 119))["y0"] + 1) / 144, "<=0.45")]
    return checks, [vid, r["json"]]


@card("CAM-214")
def cam214(task, wd):
    """Glowing card field fly-over: hundreds (300-600) of small cards on a curved ground, the camera dollies forward and
    tilts; cards stream outward from the vanishing point (4-5 s)."""
    rng = np.random.default_rng(5)
    n = 420
    xs, zs = rng.uniform(-12, 12, n), rng.uniform(-40, 4, n)
    cards = [(float(x), float(-0.004 * x * x - 0.002 * z * z), float(z), 0.12, "#ffd27a") for x, z in zip(xs, zs)]
    pts = [(0, 3, -60, 1.5, RED)] + cards
    js = "function update(t){const u=t/4.5; camera.position.set(0,2.2-0.6*u,6-18*u); camera.lookAt(0,1.4-1.4*u,-60); return {pitch:Math.atan2((1.4-1.4*u)-(2.2-0.6*u),-60-(6-18*u))};}"

    def crits(r, T):
        f = r["frames"]

        def outflow(a, b):
            out = 0
            tot = 0
            for i in range(1, len(pts)):
                pa, pb = f[a]["P"][i], f[b]["P"][i]
                if pa[3] > 0.5 and pb[3] > 0.5 and 0 < pa[0] < 256 and 0 < pa[1] < 144:
                    tot += 1
                    out += math.hypot(pb[0] - 128, pb[1] - 72) > math.hypot(pa[0] - 128, pa[1] - 72)
            return out / max(1, tot)
        vids = {}

        def spread(m):
            v = vids.setdefault(id(m), read_video(r["video"] if m is r["meas"] else r["input"]))
            def rd(fr):                         # glowing card pixels in the near band of the frame
                yy, xx = np.nonzero(np.abs(fr.astype(float) - [255, 210, 122]).max(-1) < 50)
                return int((yy > 100).sum())
            return rd(v[0]), rd(v[idx(T, 3.0)])
        pitch = [fr["x"]["pitch"] for fr in f]
        return [("measured: the near band fills with glowing cards as the camera flies in", lambda m, f2: (spread(m)[1] > 1.4 * spread(m)[0], spread(m)), ">1.4x"),
                ("card count 300-600 on a curved ground", lambda m, f2: (300 <= n <= 600 and len({round(c[1], 3) for c in cards}) > 100, n), "300-600"),
                ("cards stream outward from the vanishing point", lambda m, f2: (outflow(0, idx(T, 1.0)) > 0.9, outflow(0, idx(T, 1.0))), ">0.9"),
                ("camera tilts during the dolly", lambda m, f2: (abs(pitch[-1] - pitch[0]) > 0.005, [pitch[0], pitch[-1]]), "changes")]
    return run3d(wd, "cardfield", pts, js, 4.5, 6, crits)


@card("CAM-24")
def cam24(task, wd):
    """Pointer / scroll parallax camera: eye = (px*1.6 + sin(t*.11)*.6, .4 + py + cos(t*.09)*.4, 6.5 - scroll*4), lookAt
    (px*.4, py*.3 - scroll*1.5, -8); the pointer is followed with lerp .06 per frame; scroll dollies 4 units."""
    js = ("let px=0,py=0; function input(t){return t<1?[0,0,0]:t<3?[1,0.5,0]:[1,0.5,Math.min(1,(t-3)/1.5)];}"
          "function update(t){const [tx,ty,sc]=input(t); px+=(tx-px)*.06; py+=(ty-py)*.06;"
          " camera.position.set(px*1.6+Math.sin(t*.11)*.6,.4+py+Math.cos(t*.09)*.4,6.5-sc*4); camera.lookAt(px*.4,py*.3-sc*1.5,-8); return {px,sc};}")
    pts = [(0, 0, -8, 0.6, RED), (-2, 0.5, -2, 0.3, BLUE), (2, -0.5, -4, 0.3, GREEN)]
    fps = 60

    def crits(r, T):
        px = np.array([fr["x"]["px"] for fr in r["frames"]])
        a = idx(T, 1.0)
        gap = 1 - px[a + 60]
        z = pos(r["frames"])[:, 2]
        return [("measured: near layers shift more than far ones when the pointer moves", lambda m, f: (abs(P(m, 1)[0][idx(T, 2.9)] - P(m, 1)[0][a]) > 2 * abs(P(m, 0)[0][idx(T, 2.9)] - P(m, 0)[0][a]) and abs(P(m, 1)[0][idx(T, 2.9)] - P(m, 1)[0][a]) > 3,
                                                                                                      [float(P(m, 1)[0][idx(T, 2.9)] - P(m, 1)[0][a]), float(P(m, 0)[0][idx(T, 2.9)] - P(m, 0)[0][a])]), "near > 2x far"),
                ("pointer followed with lerp .06 per frame (gap (1-.06)^n)", lambda m, f: (abs(gap - 0.94 ** 60) < 0.02, float(gap)), 0.94 ** 60),
                ("scroll dollies 4 units (eye z 6.5 -> 2.5)", lambda m, f: (abs(z[-1] - 2.5) < 1e-9, float(z[-1])), 2.5)]
    return run3d(wd, "pointercam", pts, js, 4.6, fps // 4 * 4 // 4 * 4 and 60, crits, W=192, H=108)


@card("CAM-223")
def cam223(task, wd):
    """Rail parallax for speed: railing posts every 2 m along the pier, the camera tracks at rider speed 4 m/s, so
    near posts sweep past faster than far ones (screen speed ~ 1/depth)."""
    near = [(float(x), 0.8, -2.0, 0.08, RED) for x in np.arange(-20, 30, 2.0)]
    far = [(float(x), 0.8, -8.0, 0.25, BLUE) for x in np.arange(-20, 40, 2.0)]
    js = "function update(t){camera.position.set(4*t,1.2,0); camera.lookAt(4*t,1.0,-10);}"
    pts = [near[10]] + [far[10]] + [p for i, p in enumerate(near) if i != 10] + [p for i, p in enumerate(far) if i != 10]

    def crits(r, T):
        f = r["frames"]
        def sp(i):
            return (f[3]["P"][i][0] - f[0]["P"][i][0]) / (T[3] - T[0])
        sp_n, sp_f = sp(0), sp(1)
        k = (144 / 2) / math.tan(math.radians(35) / 2)
        pos_n = np.array([fr["P"][0][0] for fr in f])

        def meas_speed(m):
            xs = [v[0]["cx"] for v in m[:4] if v[0]]
            return (xs[-1] - xs[0]) / (T[len(xs) - 1]) if len(xs) > 1 else 0.0
        return [("measured: post field slides left at rider speed (near rail)", lambda m, f2: (meas_speed(m) < -0.5 * abs(4 * k / 2.0), meas_speed(m)), "~ -4k/2 px/s"),
                ("near posts sweep faster than far posts by the depth ratio", lambda m, f2: (abs(sp_n / sp_f - 8.0 / 2.0) < 0.05, sp_n / sp_f), 4.0),
                ("rider speed 4 m/s, posts 2 m apart (one post every 0.5 s)", lambda m, f2: (abs(near[1][0] - near[0][0] - 2) < 1e-9 and abs(pos(f)[-1][0] - 4 * T[-1]) < 1e-9, True), True)]
    return run3d(wd, "railparallax", pts, js, 2.0, 15, crits)


# ───────────────────────────── HUD overlays: drawn per frame over footage, measured back from the video ─────────────────────────────

MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
HW, HH, HFPS = 640, 360, 30


def _font(size):
    from PIL import ImageFont
    try:
        return ImageFont.truetype(MONO, int(size))
    except OSError:
        return ImageFont.load_default()


def tc(frame, fps=HFPS):
    s, ff = divmod(frame, fps)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d:%02d" % (h, m, s, ff)


def base_clip(n, W=HW, H=HH, ground=None):
    """Footage stand-in: a slowly drifting dark gradient (or a flat ground colour)."""
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    out = []
    for i in range(n):
        if ground:
            fr = np.zeros((H, W, 3), np.float32) + np.array(hex2rgb(ground), np.float32)
        else:
            g = 40 + 30 * np.sin(xs / 90 + i * 0.05) + 20 * np.cos(ys / 70 - i * 0.03)
            fr = np.stack([g * 0.6, g * 0.8, g + 15], -1)
        out.append(np.clip(fr, 0, 255).astype(np.uint8))
    return out


class Hud:
    """A HUD spec: components drawn on an RGBA overlay per frame; each component also measures itself back."""

    def __init__(self, dur=1.0, fps=HFPS, ground=None):
        self.c, self.dur, self.fps, self.ground = [], dur, fps, ground

    def add(self, kind, **kw):
        kw["kind"] = kind
        self.c.append(kw)
        return self

    def overlay(self, i, only=None, text_override=None):
        from PIL import Image, ImageDraw
        t = i / self.fps
        ov = Image.new("RGBA", (HW, HH), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for k, c in enumerate(self.c):
            if only is not None and k != only:
                continue
            col = hex2rgb(c.get("color", "#ffffff")) + (int(255 * c.get("alpha", 1.0)),)
            if c["kind"] == "brackets":
                m, a, w = c["inset"], c["arm"], c["lw"]
                for cx, cy, sx, sy in ((m, m, 1, 1), (HW - 1 - m, m, -1, 1), (m, HH - 1 - m, 1, -1), (HW - 1 - m, HH - 1 - m, -1, -1)):
                    d.rectangle([min(cx, cx + sx * (a - 1)), min(cy, cy + sy * (w - 1)), max(cx, cx + sx * (a - 1)), max(cy, cy + sy * (w - 1))], fill=col)
                    d.rectangle([min(cx, cx + sx * (w - 1)), min(cy, cy + sy * (a - 1)), max(cx, cx + sx * (w - 1)), max(cy, cy + sy * (a - 1))], fill=col)
            elif c["kind"] == "text":
                s = text_override if (text_override is not None and only == k) else c["fn"](t, i)
                d.text(c["xy"], s, font=_font(c.get("size", 12)), fill=col, anchor=c.get("anchor", "la"))
            elif c["kind"] == "bar":
                frac_ = max(0.0, min(1.0, c["fn"](t, i)))
                x0, y, x1, h = c["x0"], c["y"], c["x1"], c.get("h", 2)
                if c.get("track"):
                    d.rectangle([x0, y, x1 - 1, y + h - 1], fill=hex2rgb(c["track"]) + (int(255 * c.get("alpha", 1.0)),))
                L = int(round((x1 - x0) * frac_))
                if L > 0:
                    d.rectangle([x0, y, x0 + L - 1, y + h - 1], fill=col)
            elif c["kind"] == "dot":
                if c["fn"](t, i):
                    x, y, r = c["xy"][0], c["xy"][1], c.get("r", 4)
                    d.ellipse([x - r, y - r, x + r, y + r], fill=col)
            elif c["kind"] == "squares":
                k_on = c["fn"](t, i)
                for j in range(c["n"]):
                    x = c["xy"][0] + j * (c["size"] + c["gap"])
                    box = [x, c["xy"][1], x + c["size"] - 1, c["xy"][1] + c["size"] - 1]
                    if j < k_on:
                        d.rectangle(box, fill=col)
                    else:
                        d.rectangle(box, outline=col)
            elif c["kind"] == "marker":           # a vertical playhead/marker line moving along x
                x = int(round(c["x0"] + (c["x1"] - c["x0"]) * max(0, min(1, c["fn"](t, i)))))
                d.rectangle([x, c["y"], x + c.get("w", 1) - 1, c["y"] + c["h"] - 1], fill=col)
                for tx in c.get("ticks", []):
                    xx = int(round(c["x0"] + (c["x1"] - c["x0"]) * tx))
                    d.polygon([(xx, c["y"] - 4), (xx + 3, c["y"] - 1), (xx, c["y"] + 2), (xx - 3, c["y"] - 1)], fill=hex2rgb(c.get("tick_color", "#ffffff")) + (255,))
        return ov

    def render(self, wd, name):
        from PIL import Image
        n = int(round(self.dur * self.fps))
        base = base_clip(n, ground=self.ground)
        outs = []
        for i in range(n):
            im = Image.fromarray(base[i]).convert("RGBA")
            im.alpha_composite(self.overlay(i))
            outs.append(np.asarray(im.convert("RGB")))
        vid = write_video(wd / ("%s.mp4" % name), outs, self.fps)
        inp = write_video(wd / ("%s_input.mp4" % name), base, self.fps)
        return vid, inp, base


def _text_box(hud, k, strings):
    from PIL import Image, ImageDraw
    c = hud.c[k]
    d = ImageDraw.Draw(Image.new("RGB", (4, 4)))
    boxes = [d.textbbox(c["xy"], s, font=_font(c.get("size", 12)), anchor=c.get("anchor", "la")) for s in strings]
    x0, y0 = max(0, min(b[0] for b in boxes) - 1), max(0, min(b[1] for b in boxes) - 1)
    x1, y1 = min(HW, max(b[2] for b in boxes) + 1), min(HH, max(b[3] for b in boxes) + 1)
    return x0, y0, x1, y1


def hud_measure(hud, vid_frames, base, samples=(0, 7, 18, 29)):
    """Measure every component of a HUD on decoded frames; returns {name: (ok, measured, expected)}."""
    from PIL import Image
    res = {}
    n = len(vid_frames)
    samples = [s for s in samples if s < n] or [0]
    diff = [np.abs(vid_frames[i].astype(float) - base[i].astype(float)).max(-1) > 6 for i in range(n)]
    for k, c in enumerate(hud.c):
        name = c.get("name", "%s#%d" % (c["kind"], k))
        if c["kind"] == "brackets":
            m, a, w = c["inset"], c["arm"], c["lw"]
            meas = []
            for i in samples:
                D = diff[i]
                arms = []
                for cy, cx, sx, sy in ((m, m, 1, 1), (m, HW - 1 - m, -1, 1), (HH - 1 - m, m, 1, -1), (HH - 1 - m, HW - 1 - m, -1, -1)):
                    L = 0
                    while 0 <= cx + sx * L < HW and D[cy, cx + sx * L]:
                        L += 1
                    V = 0
                    while 0 <= cy + sy * V < HH and D[cy + sy * V, cx]:
                        V += 1
                    arms.append((L, V, bool(D[cy - sy, cx]) if 0 <= cy - sy < HH else False))
                meas.append(arms)
            ok = all(L == a and V == a and not outside for arms in meas for L, V, outside in arms)
            res[name + ": 4 L-brackets at inset %d px, arms %d px, every frame" % (m, a)] = (ok, meas[0], [(a, a, False)] * 4)
        elif c["kind"] == "text":
            good = []
            for i in samples:
                t = i / hud.fps
                exp = c["fn"](t, i)
                alts = [c["fn"]((j) / hud.fps, j) for j in (max(0, i - 1), min(n - 1, i + 1), (i + n // 2) % n)]
                alts = [s for s in dict.fromkeys(alts) if s != exp] + c.get("alts", [])
                cands = [exp] + alts
                box = _text_box(hud, k, cands)
                errs = []
                for s in cands:
                    im = Image.fromarray(base[i]).convert("RGBA")
                    im.alpha_composite(hud.overlay(i, only=k, text_override=s))
                    a_ = np.asarray(im.convert("RGB"))[box[1]:box[3], box[0]:box[2]].astype(float)
                    b_ = vid_frames[i][box[1]:box[3], box[0]:box[2]].astype(float)
                    errs.append(float(np.abs(a_ - b_).mean()))
                best = int(np.argmin(errs))
                good.append((best == 0 and errs[0] < 1.0, exp, round(errs[0], 3), round(min(errs[1:]) if len(errs) > 1 else 99, 3)))
            res[name + ": reads the expected text in the frame (vs neighbours)"] = (all(g[0] for g in good), [g[1:] for g in good], "best match = expected")
        elif c["kind"] == "bar":
            meas, want = [], []
            for i in samples:
                row = diff[i][c["y"] + c.get("h", 2) // 2, c["x0"]:c["x1"]]
                if c.get("track"):
                    col = np.array(hex2rgb(c.get("color", "#ffffff")), float)
                    px = vid_frames[i][c["y"] + c.get("h", 2) // 2, c["x0"]:c["x1"]].astype(float)
                    tr = np.array(hex2rgb(c["track"]), float)
                    row = np.abs(px - col).max(-1) < np.abs(px - tr).max(-1)
                L = int(np.argmin(row)) if not row.all() else len(row)
                meas.append(L)
                want.append(int(round((c["x1"] - c["x0"]) * max(0, min(1, c["fn"](i / hud.fps, i))))))
            res[name + ": bar length follows its value per frame"] = (all(abs(a - b) <= 1 for a, b in zip(meas, want)), meas, want)
        elif c["kind"] == "dot":
            x, y = c["xy"]
            got = [bool(diff[i][y, x]) for i in range(n)]
            want = [bool(c["fn"](i / hud.fps, i)) for i in range(n)]
            res[name + ": dot on/off pattern"] = (got == want and any(want), "".join("1" if g else "0" for g in got), "".join("1" if w else "0" for w in want))
        elif c["kind"] == "squares":
            got, want = [], []
            for i in samples:
                k_on = 0
                for j in range(c["n"]):
                    x = c["xy"][0] + j * (c["size"] + c["gap"]) + c["size"] // 2
                    y = c["xy"][1] + c["size"] // 2
                    k_on += bool(diff[i][y, x])
                got.append(k_on)
                want.append(c["fn"](i / hud.fps, i))
            res[name + ": filled squares count"] = (got == want, got, want)
        elif c["kind"] == "marker":
            got, want = [], []
            yy = c["y"] + c["h"] // 2
            for i in samples:
                cols = np.nonzero(np.abs(vid_frames[i][yy].astype(float) - hex2rgb(c["color"])).max(-1) < 40)[0]
                cols = cols[(cols >= c["x0"] - 2) & (cols <= c["x1"] + 2)]
                got.append(int(cols.min()) if len(cols) else -1)
                want.append(int(round(c["x0"] + (c["x1"] - c["x0"]) * max(0, min(1, c["fn"](i / hud.fps, i))))))
            res[name + ": marker x follows its value"] = (all(abs(a - b) <= 1 for a, b in zip(got, want)), got, want)
    return res


def hud_card(wd, name, hud, extra=None, samples=(0, 7, 18, 29)):
    vid, inp, base = hud.render(wd, name)
    v = read_video(vid)
    vi = read_video(inp)
    res = hud_measure(hud, v, base, samples)
    checks = [check(k, ok, m, e) for k, (ok, m, e) in res.items()]
    res_in = hud_measure(hud, vi, base, samples)
    neg = [k for k, (ok, _, _) in res_in.items() if ok]
    checks.append(check("negative control: no HUD component measures on the unprocessed footage", not neg, neg, []))
    if extra:
        checks += extra(v, base)
    spec = wd / ("%s_hud.json" % name)
    spec.write_text(json.dumps([{k: (v_ if not callable(v_) else "fn") for k, v_ in c.items()} for c in hud.c]), encoding="utf-8")
    return checks, [vid, spec]


def chapter_of(t, cuts):
    return sum(1 for c in cuts if t >= c)


def hz_on(t, hz=1.0):
    return (t * hz) % 1.0 < 0.5


S3 = lambda px: max(1, int(round(px / 3)))         # 1080p design px -> this 640x360 render
F3 = lambda px: max(9, int(round(px * 0.9)))        # mono label size kept legible at this size


def _std_hud(inset, arm, lw=1, alpha=0.6, color="#ffffff", dur=1.0, ground=None):
    return Hud(dur, ground=ground).add("brackets", inset=inset, arm=arm, lw=lw, color=color, alpha=alpha, name="brackets")


NAMES7 = ["INTRO", "TYPE", "MOTION", "CAMERA", "COLOR", "SOUND", "END"]


@card("CAM-195")
def cam195(task, wd):
    """Showreel HUD frame: 4 L brackets (~40 px arms, 1.5 px white 60%), top-left title/subtitle + REC dot, top-right running
    timecode HH:MM:SS:FF + spec line, bottom-left scene label updated at each scene start."""
    cuts = [0.0, 0.7, 1.4]
    h = _std_hud(S3(60), S3(120), 1, 0.6, dur=2.0)
    h.add("text", name="title", xy=(30, 26), fn=lambda t, i: "KOSIF REEL", size=F3(13), alts=["KOSIF RELL"])
    h.add("dot", name="rec", xy=(24, 50), r=3, color="#ff3030", fn=lambda t, i: hz_on(t))
    h.add("text", name="timecode", xy=(HW - 30, 26), anchor="ra", fn=lambda t, i: tc(i), size=F3(13))
    h.add("text", name="spec", xy=(HW - 30, 42), anchor="ra", fn=lambda t, i: "1080x1920 30P", size=F3(12), alts=["1080x1920 24P"])
    h.add("text", name="scene label", xy=(30, HH - 30), anchor="ld", fn=lambda t, i: "%02d %s" % (chapter_of(t, cuts), NAMES7[chapter_of(t, cuts)]), size=F3(13))
    return hud_card(wd, "showreel", h, samples=(0, 15, 25, 45, 59))


@card("CAM-196")
def cam196(task, wd):
    """HUD frame overlay: corner brackets, mono timecode TC and a frame counter F 0263/0900."""
    h = _std_hud(16, 22, 1, 0.8)
    h.add("text", name="TC", xy=(26, HH - 26), anchor="ld", fn=lambda t, i: "TC " + tc(i + 263), size=10)
    h.add("text", name="frame counter", xy=(HW - 26, HH - 26), anchor="rd", fn=lambda t, i: "F %04d/0900" % (i + 263), size=10)
    return hud_card(wd, "hudframe", h)


@card("CAM-197")
def cam197(task, wd):
    """Persistent HUD reel frame: brackets 24 px, mono 13 px, 4% safe margin, live TC hh:mm:ss:ff, chapter 'NN/07 NAME',
    and 4 beat squares filling per beat (120 bpm)."""
    m = int(0.04 * HH)
    cuts = [0.0, 1.0]
    h = _std_hud(m, S3(72), 1, 0.7, dur=2.0)
    h.add("text", name="TC", xy=(HW - m - 8, m + 8), anchor="ra", fn=lambda t, i: "TC " + tc(i), size=F3(13))
    h.add("text", name="chapter", xy=(m + 8, m + 8), fn=lambda t, i: "%02d/07 %s" % (chapter_of(t, cuts), NAMES7[chapter_of(t, cuts)]), size=F3(13))
    h.add("squares", name="beat squares", n=4, xy=(m + 8, HH - m - 18), size=8, gap=4, fn=lambda t, i: int(t * 2) % 4 + 1)
    return hud_card(wd, "reelframe", h, samples=(0, 14, 16, 31, 46, 59))


@card("CAM-198")
def cam198(task, wd):
    """HUD frame chrome: corner tick marks, timecode, bottom progress line (1 px, 40% opacity)."""
    h = _std_hud(12, 10, 1, 0.4)
    h.add("text", name="TC", xy=(HW - 20, 20), anchor="ra", fn=lambda t, i: tc(i), size=10, alpha=0.8)
    h.add("bar", name="progress line", x0=0, x1=HW, y=HH - 3, h=1, alpha=0.4, fn=lambda t, i: (i + 1) / 30)
    return hud_card(wd, "chrome", h)


@card("CAM-199")
def cam199(task, wd):
    """Viewfinder HUD frame: corner L-brackets at 3% inset; mono labels in all four corners; TC from the frame number;
    bottom progress line width = t/duration; blue square bullet #0645e2."""
    m = int(0.03 * HH)
    h = _std_hud(m, 18, 1, 0.9)
    for nm, xy, an, s in (("label TL", (m + 22, m + 6), "la", "CAM A"), ("label TR", (HW - m - 6, m + 6), "ra", "ISO 800"),
                          ("label BL", (m + 6, HH - m - 8), "ld", "F2.8")):
        h.add("text", name=nm, xy=xy, anchor=an, fn=(lambda s_: lambda t, i: s_)(s), size=10, alts=[s[::-1]])
    h.add("text", name="TC label BR", xy=(HW - m - 6, HH - m - 8), anchor="rd", fn=lambda t, i: "TC " + tc(i), size=10)
    h.add("dot", name="blue bullet", xy=(m + 13, m + 11), r=3, color="#0645e2", fn=lambda t, i: True)
    h.add("bar", name="progress", x0=0, x1=HW, y=HH - 2, h=2, color="#0645e2", fn=lambda t, i: i / 30)
    return hud_card(wd, "viewfinder", h)


@card("CAM-200")
def cam200(task, wd):
    """HUD showreel frame: corner brackets, mono chapter label 'NN NAME', timecode, progress bar persistent over all scenes."""
    cuts = [0.0, 0.5]
    h = _std_hud(14, 20, 1, 0.7)
    h.add("text", name="chapter", xy=(24, 22), fn=lambda t, i: "%02d %s" % (chapter_of(t, cuts), NAMES7[chapter_of(t, cuts)]), size=11)
    h.add("text", name="TC", xy=(HW - 24, 22), anchor="ra", fn=lambda t, i: tc(i), size=11)
    h.add("bar", name="progress", x0=24, x1=HW - 24, y=HH - 24, h=3, fn=lambda t, i: i / 29)
    return hud_card(wd, "showreel200", h, samples=(0, 14, 15, 29))


@card("CAM-208")
def cam208(task, wd):
    """HUD corner frame: corner brackets + a mono timecode at 9 px."""
    h = _std_hud(10, 14, 1, 0.8)
    h.add("text", name="TC 9px", xy=(18, HH - 16), anchor="ld", fn=lambda t, i: tc(i), size=9)
    return hud_card(wd, "cornerframe", h)


@card("CAM-210")
def cam210(task, wd):
    """Numbered HUD reel frame: brackets, top-left project label, top-right '0N / 06 - SECTION', bottom timecode,
    resolution tag and a progress line (mono 11 px uppercase, 40 px margins)."""
    m = S3(40) * 3 // 3 + 6
    cuts = [0.0, 0.5]
    secs = ["INTRO", "TYPE", "MOTION"]
    h = _std_hud(m - 6, 16, 1, 0.8)
    h.add("text", name="project", xy=(m + 6, m + 4), fn=lambda t, i: "PROJECT KOSIF", size=10, alts=["PROJECT KOSIP"])
    h.add("text", name="section", xy=(HW - m - 6, m + 4), anchor="ra", fn=lambda t, i: "0%d / 06 - %s" % (chapter_of(t, cuts), secs[chapter_of(t, cuts)]), size=10)
    h.add("text", name="TC", xy=(m + 6, HH - m - 8), anchor="ld", fn=lambda t, i: tc(i), size=10)
    h.add("text", name="resolution", xy=(HW - m - 6, HH - m - 8), anchor="rd", fn=lambda t, i: "1920X1080", size=10, alts=["1080X1920"])
    h.add("bar", name="progress", x0=m, x1=HW - m, y=HH - m, h=1, fn=lambda t, i: i / 29)
    return hud_card(wd, "numbered", h, samples=(0, 14, 15, 29))


@card("CAM-215")
def cam215(task, wd):
    """Film HUD overlay: corner crop marks, a BPM/bar counter and a timecode (120 bpm, 4/4)."""
    h = _std_hud(8, 12, 1, 0.8, dur=2.4)
    h.add("text", name="bpm bar counter", xy=(20, HH - 20), anchor="ld", fn=lambda t, i: "120 BPM  BAR %02d.%d" % (int(t * 2) // 4 + 1, int(t * 2) % 4 + 1), size=10)
    h.add("text", name="TC", xy=(HW - 20, HH - 20), anchor="rd", fn=lambda t, i: tc(i), size=10)
    return hud_card(wd, "filmhud", h, samples=(0, 14, 15, 45, 61, 71))


@card("CAM-218")
def cam218(task, wd):
    """Geo HUD brackets: corner brackets + live coordinates of the tracked point + section labels."""
    lat = lambda t: 30.0444 + 0.0012 * t
    lon = lambda t: 31.2357 - 0.0008 * t
    h = _std_hud(12, 18, 1, 0.8)
    h.add("text", name="coordinates", xy=(22, HH - 20), anchor="ld", fn=lambda t, i: "%.4fN %.4fE" % (lat(t * 10), lon(t * 10)), size=10)
    h.add("text", name="section", xy=(22, 20), fn=lambda t, i: "02 / CAIRO", size=10, alts=["03 / CAIRO"])
    return hud_card(wd, "geohud", h)


@card("CAM-226")
def cam226(task, wd):
    """Corner crop marks frame: four thin L ticks framing a UI panel like print registration marks (1 px, 16 px arms, 30% opacity)."""
    h = Hud(1.0, ground="#e8e6e0").add("brackets", inset=40, arm=S3(48) + 0, lw=1, color="#000000", alpha=0.3, name="crop marks")
    return hud_card(wd, "cropmarks", h)


@card("CAM-229")
def cam229(task, wd):
    """Poster HUD micro-labels: mono 10 px plate number, chapter code, colour-key dots at the left edge."""
    h = Hud(1.0, ground="#f2efe6")
    h.add("text", name="plate number", xy=(14, 14), fn=lambda t, i: "PL. 07", size=10, color="#222222", alts=["PL. 01"])
    h.add("text", name="chapter code", xy=(HW - 14, 14), anchor="ra", fn=lambda t, i: "CH-B2", size=10, color="#222222", alts=["CH-B3"])
    for j, col in enumerate(["#e4342f", "#2f6be4", "#e4b62f"]):
        h.add("dot", name="colour key %d" % j, xy=(10, 120 + 16 * j), r=4, color=col, fn=lambda t, i: True)
    return hud_card(wd, "posterhud", h)


@card("CAM-234")
def cam234(task, wd):
    """Chapter tag system: mono 'NN/06 SECTION' bottom-left + progress line, spec text bottom-right."""
    cuts = [0.0, 0.5]
    h = Hud(1.0)
    h.add("text", name="chapter tag", xy=(20, HH - 24), anchor="ld", fn=lambda t, i: "%02d/06 %s" % (chapter_of(t, cuts), NAMES7[chapter_of(t, cuts)]), size=10)
    h.add("bar", name="progress line", x0=20, x1=200, y=HH - 18, h=1, fn=lambda t, i: i / 29)
    h.add("text", name="spec", xy=(HW - 20, HH - 20), anchor="rd", fn=lambda t, i: "4K / 24 FPS", size=10, alts=["4K / 25 FPS"])
    return hud_card(wd, "chaptertag", h, samples=(0, 14, 15, 29))


@card("CAM-242")
def cam242(task, wd):
    """Frame-counter meta HUD: 'frame / total' and 'chapter / total' counters ticking every frame (total 900 frames at 60 fps)."""
    h = Hud(0.5, fps=60)
    h.add("text", name="frame counter", xy=(HW - 16, 16), anchor="ra", fn=lambda t, i: "%03d / 900" % (i + 1), size=11)
    h.add("text", name="chapter counter", xy=(16, 16), fn=lambda t, i: "%02d / 06" % (1 + (i // 15)), size=11)
    return hud_card(wd, "framecounter", h, samples=(0, 1, 14, 15, 29))


def _camcorder(wd, name, inset_frac, alpha):
    m = int(inset_frac * HH)
    h = _std_hud(m, 20, 2, alpha, dur=2.0)
    h.add("text", name="title/reel", xy=(m + 10, m + 8), fn=lambda t, i: "REEL 01", size=10, alpha=alpha, alts=["REEL 02"])
    h.add("text", name="TC", xy=(HW - m - 10, m + 8), anchor="ra", fn=lambda t, i: "TC " + tc(i), size=10, alpha=alpha)
    h.add("text", name="counter", xy=(m + 10, HH - m - 10), anchor="ld", fn=lambda t, i: "%05d" % i, size=10, alpha=alpha)
    h.add("dot", name="REC 1 Hz", xy=(HW - m - 16, HH - m - 16), r=4, color="#ff2020", fn=lambda t, i: hz_on(t))
    return hud_card(wd, name, h, samples=(0, 14, 15, 44, 59))


@card("CAM-247")
def cam247(task, wd):
    """Camcorder HUD frame: corner brackets, mono labels top (title/reel, TC) and bottom (counter, red REC dot blinking
    1 Hz); inset 5%, 70% opacity."""
    return _camcorder(wd, "camcorder", 0.05, 0.7)


@card("CAM-248")
def cam248(task, wd):
    """Viewfinder HUD: corner marks, TC counter, REC dot (blinking)."""
    return _camcorder(wd, "viewfinder248", 0.04, 0.9)


@card("CAM-251")
def cam251(task, wd):
    """Self-annotating HUD: a mono code comment naming the current technique on top, 'NN / SECTION' on the right; scene id,
    BPM and bar number at the bottom; red #e93e24 progress."""
    beats = [(0.0, "// per-letter rise + rotate . stagger 22ms . circ.out", "01 / TYPE"), (0.5, "// camera push . log space . E.cam", "02 / CAMERA")]
    cur = lambda t: [b for b in beats if t >= b[0]][-1]
    h = Hud(1.0)
    h.add("text", name="technique comment", xy=(16, 14), fn=lambda t, i: cur(t)[1], size=10)
    h.add("text", name="section", xy=(HW - 16, 14), anchor="ra", fn=lambda t, i: cur(t)[2], size=10)
    h.add("text", name="scene/bpm/bar", xy=(16, HH - 18), anchor="ld", fn=lambda t, i: "S%02d  120 BPM  BAR %d" % (1 + (t >= 0.5), int(t * 2) // 4 + 1), size=10)
    h.add("bar", name="red progress", x0=0, x1=HW, y=HH - 4, h=3, color="#e93e24", fn=lambda t, i: i / 29)
    return hud_card(wd, "selfannot", h, samples=(0, 14, 15, 29))


@card("CAM-253")
def cam253(task, wd):
    """Mono corner counters: '04/10' index top-right, labels uppercase mono."""
    h = Hud(1.0)
    h.add("text", name="index", xy=(HW - 16, 16), anchor="ra", fn=lambda t, i: "%02d/10" % (4 + (i >= 15)), size=12)
    h.add("text", name="label", xy=(16, 16), fn=lambda t, i: "KINETIC TYPE", size=12, alts=["Kinetic Type"])
    return hud_card(wd, "monocounters", h, samples=(0, 14, 15, 29))


@card("CAM-254")
def cam254(task, wd):
    """Editor timeline HUD: bottom bar with 6 diamond keyframes, a playhead moving with real time, section label at the
    playhead; timecode top-right HH:MM:SS:FF."""
    h = Hud(1.0)
    h.add("bar", name="timeline line", x0=40, x1=HW - 40, y=HH - 30, h=1, fn=lambda t, i: 1.0, alpha=0.5)
    h.add("marker", name="playhead", x0=40, x1=HW - 40, y=HH - 44, h=24, w=1, color="#ff4040", fn=lambda t, i: i / 29,
          ticks=[k / 5 for k in range(6)], tick_color="#ffd040")
    h.add("text", name="TC", xy=(HW - 20, 16), anchor="ra", fn=lambda t, i: tc(i), size=11)

    def extra(v, base):
        d = [np.abs(v[0][HH - 45, int(round(40 + (HW - 80) * k / 5)) + (2 if k == 0 else 0)].astype(float) - [255, 208, 64]).max() < 40 for k in range(6)]
        return [check("6 diamond keyframes on the timeline", all(d), d, [True] * 6)]
    return hud_card(wd, "editortl", h, extra)


@card("CAM-256")
def cam256(task, wd):
    """Paper HUD frame: corner brackets + tiny mono timecode labels on a cream ground."""
    h = _std_hud(14, 18, 1, 0.8, color="#3a3530", ground="#f1ead8")
    h.add("text", name="TC", xy=(24, HH - 22), anchor="ld", fn=lambda t, i: tc(i), size=9, color="#3a3530")
    return hud_card(wd, "paperhud", h)


@card("CAM-258")
def cam258(task, wd):
    """Persistent game HUD frame: player name, 7-digit zero-padded score counter, hearts and level on top; section label,
    countdown TIME in 0.1 s steps and a 4 px lime progress bar growing across the full duration at the bottom."""
    dur = 1.0
    h = Hud(dur)
    h.add("text", name="player", xy=(14, 12), fn=lambda t, i: "P1 KOSIF", size=11, alts=["P2 KOSIF"])
    h.add("text", name="score 7 digits", xy=(HW // 2, 12), anchor="ma", fn=lambda t, i: "%07d" % (i * 137), size=11)
    h.add("squares", name="hearts", n=3, xy=(HW - 60, 12), size=10, gap=4, color="#ff4060", fn=lambda t, i: 3 - (i >= 20))
    h.add("text", name="countdown TIME", xy=(HW - 14, HH - 16), anchor="rd", fn=lambda t, i: "TIME %04.1f" % (math.floor((60 - t) * 10) / 10), size=11)
    h.add("bar", name="lime progress 4px", x0=0, x1=HW, y=HH - 4, h=4, color="#a8ff3c", fn=lambda t, i: i / 29)
    return hud_card(wd, "gamehud", h, samples=(0, 3, 19, 20, 29))


@card("CAM-262")
def cam262(task, wd):
    """Scene index HUD: '03/08 KINETIC TYPE' label + its progress segment."""
    h = Hud(1.0)
    h.add("text", name="scene index", xy=(16, HH - 20), anchor="ld", fn=lambda t, i: "03/08 KINETIC TYPE", size=10, alts=["04/08 KINETIC TYPE"])
    h.add("bar", name="segment progress", x0=16 + 2 * 40, x1=16 + 3 * 40, y=HH - 12, h=2, track="#555555", fn=lambda t, i: i / 29)
    return hud_card(wd, "sceneindex", h)


@card("CAM-265")
def cam265(task, wd):
    """Showreel HUD overlay: 4 corner brackets (20 px arms), mono title top-left, timecode top-right, chapter bottom-left,
    'frame / total' with a thin progress line bottom-right, ~12 px mono at 60% opacity, margin 32 px, updated every frame."""
    m = S3(32 * 3) // 3 + 10
    cuts = [0.0, 0.5]
    h = _std_hud(m, 20, 1, 0.6)
    h.add("text", name="title", xy=(m + 8, m + 6), fn=lambda t, i: "KOSIF", size=11, alpha=0.6, alts=["KOSIP"])
    h.add("text", name="TC", xy=(HW - m - 8, m + 6), anchor="ra", fn=lambda t, i: tc(i), size=11, alpha=0.6)
    h.add("text", name="chapter", xy=(m + 8, HH - m - 8), anchor="ld", fn=lambda t, i: "%02d %s" % (chapter_of(t, cuts), NAMES7[chapter_of(t, cuts)]), size=11, alpha=0.6)
    h.add("text", name="frame/total", xy=(HW - m - 8, HH - m - 14), anchor="rd", fn=lambda t, i: "%03d / 030" % (i + 1), size=11, alpha=0.6)
    h.add("bar", name="progress line", x0=HW - m - 108, x1=HW - m - 8, y=HH - m - 10, h=1, alpha=0.6, fn=lambda t, i: (i + 1) / 30)
    return hud_card(wd, "showreel265", h, samples=(0, 14, 15, 29))


@card("CAM-266")
def cam266(task, wd):
    """Crop-mark frame: four L corners + brand tag + footer date, 40 px safe margin."""
    h = _std_hud(S3(40 * 3) // 3 + 10, 16, 1, 0.8)
    h.add("text", name="brand tag", xy=(HW // 2, 30), anchor="ma", fn=lambda t, i: "KOSIF STUDIO", size=11, alts=["KOSIF STUDI0"])
    h.add("text", name="footer date", xy=(HW // 2, HH - 30), anchor="md", fn=lambda t, i: "2026.11.03", size=10, alts=["2026.11.08"])
    return hud_card(wd, "cropframe", h)


@card("CAM-275")
def cam275(task, wd):
    """Chapter HUD + timeline marker: '05 / ELIZA' top-left, a tick ruler top-right with an orange marker moving along it."""
    h = Hud(1.0)
    h.add("text", name="chapter", xy=(16, 14), fn=lambda t, i: "05 / ELIZA", size=12, alts=["06 / ELIZA"])
    h.add("marker", name="orange marker on tick ruler", x0=HW - 200, x1=HW - 20, y=10, h=14, w=2, color="#ff8a1e", fn=lambda t, i: i / 29,
          ticks=[k / 10 for k in range(11)], tick_color="#dddddd")
    return hud_card(wd, "chapterruler", h)


# ───────────────────────────── the repo's own Python implementations (direct.py, verse.py, render.py, prompt forge) ─────────────────────────────

_MODS = {}


def repo_mod(path: Path, name: str):
    """Import a vendored repo script by path (no side effects beyond its own imports)."""
    if name not in _MODS:
        import importlib.util
        spec = importlib.util.spec_from_file_location("kosif_" + name, path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = mod                   # @dataclass in render.py looks its module up here
        old = (sys.stdout, sys.stderr)
        try:
            spec.loader.exec_module(mod)
        finally:
            sys.stdout, sys.stderr = old
        _MODS[name] = mod
    return _MODS[name]


def _talk_fixture():
    """A spoken-clip transcript fixture (two sentences, a stressed word each) and two shots with known face boxes."""
    segs = [{"start": 0.0, "end": 2.4, "words": [{"start": 0.0, "end": 0.4, "text": "النجاح"}, {"start": 0.45, "end": 0.9, "text": "يحتاج"},
                                                    {"start": 0.95, "end": 1.6, "text": "صبراً"}, {"start": 1.65, "end": 2.3, "text": "طويلاً"}]},
            {"start": 2.6, "end": 5.4, "words": [{"start": 2.6, "end": 3.0, "text": "كافح"}, {"start": 3.05, "end": 3.6, "text": "كل"},
                                                    {"start": 3.65, "end": 4.4, "text": "يوم"}, {"start": 4.5, "end": 5.3, "text": "بإصرار"}]}]
    shots = [{"start": 0.0, "end": 2.5, "box": (0.30, 0.28, 0.40, 0.30)}, {"start": 2.5, "end": 6.0, "box": (0.35, 0.30, 0.30, 0.30)}]
    stress = [0.2, -0.5, 1.4, 0.3, 0.9, -1.0, 0.1, 1.2]
    return segs, shots, stress


@card("CAM-10")
def cam10(task, wd):
    """Safe-area and face-aware text placement (direct.plan): every keyword timed in a face shot sits below the face box,
    captions stay at y <= 0.80 x 1920 inside the 9:16 safe area. Runs the repo's direct.plan and renders the layout."""
    D = repo_mod(MM / "direct.py", "direct")
    segs, shots, stress = _talk_fixture()
    W, H = 1080, 1920
    plan = D.plan(segs, [dict(s) for s in shots], stress, W, H, 6.0)
    (wd / "plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8")
    shot_of = lambda t: next((s for s in shots if s["start"] <= t < s["end"]), shots[-1])
    # render each keyword frame: face box + keyword + caption lines, then measure them back from the PNGs
    from PIL import Image, ImageDraw
    frames, meas = [], []
    for k in plan["keys"]:
        sh = shot_of(k["t"])
        im = Image.new("RGB", (W // 4, H // 4), (40, 40, 48))
        d = ImageDraw.Draw(im)
        bx = sh["box"]
        d.rectangle([bx[0] * W / 4, bx[1] * H / 4, (bx[0] + bx[2]) * W / 4, (bx[1] + bx[3]) * H / 4], fill=(230, 170, 140))
        d.rectangle([W / 8 - 60, k["y"] / 4, W / 8 + 60, k["y"] / 4 + 190 / 4 * 0.8], fill=(255, 0, 0))
        cap = [c for c in plan["captions"] if c["words"][0]["t"] <= k["t"] <= c["end"]]
        for c in cap:
            d.rectangle([20, c["y"] / 4, W / 4 - 20, c["y"] / 4 + 54 / 4], fill=(0, 0, 255))
        p = wd / ("key_%d.png" % len(frames))
        im.save(p)
        frames.append(p)
        a = np.asarray(Image.open(p).convert("RGB"))
        face = blob(a, (230, 170, 140), 20)
        key = blob(a, (255, 0, 0), 20)
        capb = blob(a, (0, 0, 255), 20)
        meas.append({"face_bottom": face["y1"] * 4, "key_top": key["y0"] * 4, "cap_top": capb["y0"] * 4 if capb else None,
                     "cap_bottom": capb["y1"] * 4 if capb else None})
    caps_ok = all(c["y"] <= 0.80 * H for c in plan["captions"])
    keys_below = all(m["key_top"] > m["face_bottom"] for m in meas)
    # the unprocessed input: the keyword at the default centre (190 px tall band around y = H/2), same measurement
    naive = [{"face_bottom": (shot_of(k["t"])["box"][1] + shot_of(k["t"])["box"][3]) * H, "key_top": H / 2 - 95} for k in plan["keys"]]
    naive_ok = all(m["key_top"] > m["face_bottom"] for m in naive)
    checks = [check("direct.plan produced keywords and captions", len(plan["keys"]) >= 1 and len(plan["captions"]) >= 1, [len(plan["keys"]), len(plan["captions"])], ">=1, >=1"),
              check("measured: every keyword sits below the face box of its shot", keys_below and bool(meas), meas, "key_top > face_bottom"),
              check("captions y <= 0.80 x 1920 (safe area)", caps_ok, [c["y"] for c in plan["captions"]], "<=1536"),
              check("negative control: centred text would overlap a face", not naive_ok, naive, "key_top > face_bottom fails")]
    return checks, [wd / "plan.json"] + frames


@card("CAM-12")
def cam12(task, wd):
    """Text-safe layout stack (direct.plan): keyY = clip(face bottom + 1.5% H, .50H, .66H); capY = clip(keyY + 13.5% H,
    .64H, .80H); motifs on the free side; text never over eyes or mouth."""
    D = repo_mod(MM / "direct.py", "direct")
    W, H = 1080, 1920
    boxes = [(0.3, 0.10, 0.4, 0.20), (0.3, 0.30, 0.4, 0.30), (0.55, 0.20, 0.3, 0.25), (0.1, 0.05, 0.3, 0.12), (0.3, 0.40, 0.4, 0.25)]
    shots = [{"start": i * 2.0, "end": i * 2.0 + 2.0, "box": b} for i, b in enumerate(boxes)]
    segs = [{"start": 0.0, "end": 8.0, "words": [{"start": i * 0.5, "end": i * 0.5 + 0.4, "text": "كلمة%d" % i} for i in range(16)]}]
    D.plan(segs, shots, [0.0] * 16, W, H, 8.0)
    rows = []
    for s in shots:
        fb = (s["box"][1] + s["box"][3]) * H
        ky = float(np.clip(fb + 0.015 * H, 0.50 * H, 0.66 * H))
        cy = float(np.clip(ky + 0.135 * H, 0.64 * H, 0.80 * H))
        mouth = (s["box"][1] + s["box"][3] * 0.8) * H
        rows.append({"keyY": s["keyY"], "capY": s["capY"], "side": s["side"], "want": (ky, cy), "mouth": mouth, "cx": (s["box"][0] + s["box"][2] / 2) * W})
    (wd / "stack.json").write_text(json.dumps(rows, indent=1), encoding="utf-8")
    checks = [check("keyY / capY follow the clip formulas for every shot", all(abs(r["keyY"] - r["want"][0]) < 1e-6 and abs(r["capY"] - r["want"][1]) < 1e-6 for r in rows),
                    [(round(r["keyY"]), round(r["capY"])) for r in rows], [(round(r["want"][0]), round(r["want"][1])) for r in rows]),
              check("never over the eyes or mouth: keyword below the mouth line", all(r["keyY"] > r["mouth"] for r in rows), [(round(r["keyY"]), round(r["mouth"])) for r in rows], "keyY > mouth"),
              check("stack order face -> keyword -> caption", all(r["capY"] > r["keyY"] for r in rows), True, True),
              check("motifs go to the free side", all((r["side"] < W / 2) == (r["cx"] > W / 2) for r in rows), [r["side"] for r in rows], "opposite the face"),
              check("negative control: a fixed lower-third y (0.55 H) lands on a low face", not all(0.55 * H > (b[1] + b[3] * 0.8) * H for b in boxes), 0.55 * H, "fails")]
    return checks, [wd / "stack.json"]


def _skin_clip(path, box, n=12, size=(160, 284), move=0.0, fps=10):
    """A synthetic talking plate: a skin-coloured face ellipse (YCrCb inside the direct.py skin range) on a cool background."""
    from PIL import Image, ImageDraw
    W, H = size
    frames = []
    for i in range(n):
        im = Image.new("RGB", (W, H), (40, 60, 90))
        d = ImageDraw.Draw(im)
        x0, y0, w, h = box[0] * W + move * i, box[1] * H, box[2] * W, box[3] * H
        d.ellipse([x0, y0, x0 + w, y0 + h], fill=(224, 172, 140))
        frames.append(np.asarray(im))
    return write_video(path, frames, fps), frames


@card("CAM-174")
def cam174(task, wd):
    """Auto camera from subject boxes: direct.subject_box finds the largest skin region in the upper 78% (else the moving
    region) and the camera pushes on it, 1.03 -> 1.09, or 1.12 -> 1.22 when the subject is small (< 20% H)."""
    D = repo_mod(MM / "direct.py", "direct")
    big, _ = _skin_clip(wd / "big.mp4", (0.30, 0.15, 0.40, 0.30))
    small, _ = _skin_clip(wd / "small.mp4", (0.50, 0.30, 0.18, 0.15))
    plain = write_video(wd / "plain.mp4", [np.zeros((284, 160, 3), np.uint8) + 60] * 12, 10)
    out = {}
    for nm, clip in (("big", big), ("small", small), ("plain", plain)):
        bx = D.subject_box(clip, 0, 12, 10.0)
        sh = {"from": 1.03, "to": 1.09}
        if bx and bx[3] < 0.2:
            sh["from"], sh["to"] = 1.12, 1.22
        out[nm] = {"box": bx, **sh}
    # render the push on the big plate around the found box centre, then measure the face growth
    bx = out["big"]["box"]
    cx, cy = (bx[0] + bx[2] / 2) * 160, (bx[1] + bx[3] * 0.4) * 284
    clip_frames = read_video(big)
    from PIL import Image
    pushed = []
    for i, fr in enumerate(clip_frames):
        s = out["big"]["from"] + (out["big"]["to"] - out["big"]["from"]) * i / (len(clip_frames) - 1)
        im = Image.fromarray(fr.astype(np.uint8)).transform((160, 284), Image.AFFINE, (1 / s, 0, cx - cx / s, 0, 1 / s, cy - cy / s), Image.BILINEAR)
        pushed.append(np.asarray(im))
    pv = write_video(wd / "pushed.mp4", pushed, 10)
    pm = read_video(pv)
    a0 = blob(pm[0], (224, 172, 140), 30)["area"]
    a1 = blob(pm[-1], (224, 172, 140), 30)["area"]
    (wd / "camera.json").write_text(json.dumps(out), encoding="utf-8")
    checks = [check("subject_box finds the face box (fractions of the frame)", bx is not None and abs(bx[0] - 0.30) < 0.03 and abs(bx[2] - 0.40) < 0.03 and abs(bx[3] - 0.30) < 0.03, bx, (0.30, 0.15, 0.40, 0.30)),
              check("big subject: push 1.03 -> 1.09", (out["big"]["from"], out["big"]["to"]) == (1.03, 1.09), (out["big"]["from"], out["big"]["to"]), (1.03, 1.09)),
              check("small subject (<20% H): start wider and push more 1.12 -> 1.22", (out["small"]["from"], out["small"]["to"]) == (1.12, 1.22), out["small"], (1.12, 1.22)),
              check("measured: the face grows by (1.09/1.03)^2 in area on the rendered push", abs(a1 / a0 - (1.09 / 1.03) ** 2) < 0.03, a1 / a0, (1.09 / 1.03) ** 2),
              check("negative control: a plate without a subject gives no box", out["plain"]["box"] is None, out["plain"]["box"], None)]
    return checks, [wd / "camera.json", pv]


@card("CAM-175")
def cam175(task, wd):
    """Type off the face over pictures (verse.text_band): after fill-crop, a face in the middle band moves the line to the
    lower (0.70 H) or upper (0.26 H) third; a free middle returns None."""
    V = repo_mod(MM / "verse.py", "verse")
    from PIL import Image, ImageDraw
    W, H = 1080, 1920
    cases = {"face_high_mid": (0.40, 0.33), "face_low_mid": (0.40, 0.50), "no_face": None}
    res, paths = {}, []
    for nm, pos_ in cases.items():
        im = Image.new("RGB", (800, 1000), (50, 70, 110))
        if pos_:
            d = ImageDraw.Draw(im)
            d.ellipse([pos_[0] * 800, pos_[1] * 1000, pos_[0] * 800 + 160, pos_[1] * 1000 + 200], fill=(224, 172, 140))
        p = wd / ("%s.png" % nm)
        im.save(p)
        paths.append(p)
        res[nm] = V.text_band(p, W, H)
    # render a line over the fill-cropped picture and measure whether it is off the face
    def off_face(nm, yline, tag):
        im = Image.open(wd / ("%s.png" % nm)).convert("RGB")
        sc = max(W / im.width, H / im.height)
        im = im.resize((int(im.width * sc + .5), int(im.height * sc + .5)))
        x0, y0 = (im.width - W) // 2, (im.height - H) // 2
        im = im.crop((x0, y0, x0 + W, y0 + H)).resize((W // 4, H // 4))
        face = blob(np.asarray(im), (224, 172, 140), 25)
        d = ImageDraw.Draw(im)
        y = yline / 4
        d.rectangle([30, y - 15, W // 4 - 30, y + 15], fill=(255, 0, 0))
        im.save(wd / ("%s_%s.png" % (nm, tag)))
        line = blob(np.asarray(im), (255, 0, 0), 25)
        return face is None or line["y0"] > face["y1"] or line["y1"] < face["y0"]
    lay = [off_face(nm, res[nm], "layout") for nm in ("face_high_mid", "face_low_mid")]
    lay_in = [off_face(nm, 0.47 * H, "centred") for nm in ("face_high_mid", "face_low_mid")]
    (wd / "bands.json").write_text(json.dumps(res), encoding="utf-8")
    checks = [check("face high in the middle band -> line in the lower third (0.70 H)", res["face_high_mid"] == round(0.70 * H), res["face_high_mid"], round(0.70 * H)),
              check("face low in the middle band -> line in the upper third (0.26 H)", res["face_low_mid"] == round(0.26 * H), res["face_low_mid"], round(0.26 * H)),
              check("free middle -> None (centre is fine)", res["no_face"] is None, res["no_face"], None),
              check("measured: the placed line never overlaps the face", all(lay), lay, [True, True]),
              check("negative control: the unprocessed centred line (0.47 H) overlaps the face", not all(lay_in), lay_in, "not all off-face")]
    return checks, [wd / "bands.json"] + paths


@card("CAM-11")
def cam11(task, wd):
    """Camera-move vocabulary + one-move rule: video_prompt_forge.lint flags multi_camera when a shot names two moves
    (push-in, dolly, orbit, crane, pan, tilt, rack focus, dolly-zoom ...); static/locked-off do not count."""
    F = repo_mod(FORGE / "video_prompt_forge.py", "forge")
    doc = {"locks": {"character": "Layla, 28", "style": "warm editorial"},
           "shots": [{"n": 1, "duration": 5, "action": "pours latte", "camera": "slow push-in"},
                     {"n": 2, "duration": 5, "action": "slides cup", "camera": "dolly left then orbit around the cup"},
                     {"n": 3, "duration": 4, "action": "smiles", "camera": "static, locked-off"},
                     {"n": 4, "duration": 4, "action": "walks", "camera": "crane up with a whip pan"}]}
    issues = F.lint(doc)
    flagged = sorted(int(re.search(r"(\d+)", i["msg"]).group(1)) for i in issues if i["code"] == "multi_camera")
    fixed = json.loads(json.dumps(doc))
    for s in fixed["shots"]:                           # the rule applied: keep the first named move only
        cams = re.findall(F.CAMERA_WORDS, s["camera"].lower())
        cams = [c for c in cams if c not in ("static", "locked-off", "locked off")]
        if len(cams) > 1:
            s["camera"] = cams[0]
    after = [i for i in F.lint(fixed) if i["code"] == "multi_camera"]
    vocab = [w for w in ["push-in", "pull-out", "dolly", "tracking", "orbit", "arc", "crane", "handheld", "whip pan", "pan", "tilt", "rack focus", "dolly-zoom", "drone", "flyover"]
             if re.search(F.CAMERA_WORDS, w)]
    (wd / "lint.json").write_text(json.dumps({"before": issues, "after": after, "fixed": fixed}, ensure_ascii=False, indent=1), encoding="utf-8")
    checks = [check("lint flags exactly the two-move shots (2 and 4)", flagged == [2, 4], flagged, [2, 4]),
              check("static / locked-off is not a move", 3 not in flagged, flagged, "no 3"),
              check("after applying one move per shot the lint is clean", not after, len(after), 0),
              check("the recognised vocabulary covers the card's moves", len(vocab) == 15, len(vocab), 15),
              check("negative control: the unprocessed prompt doc fails the one-move rule", bool(flagged), flagged, "issues")]
    return checks, [wd / "lint.json"]


def _studio_scene(R):
    """A KOSIF Studio picture program: background stripes, a far shape, then a hero (left in focus)."""
    steps = [R.Step("bg", [R.fill(R.rect(0, 0, 1200, 800), "#20304a")]),
             R.Step("stripes", [R.fill(R.rect(x, 0, 30, 800), "#d0d8e8") for x in range(0, 1200, 120)]),
             R.Step("far", [R.fill(R.ellipse(900, 300, 120, 120), "#e0b040")])]
    hero = R.Step("hero", [R.fill(R.rect(150, 300, 220, 300), "#ff3020")])
    return steps, hero


def _hf(a):
    """High-frequency energy of a picture (mean |Laplacian|)."""
    g = a.astype(float).mean(-1)
    return float(np.abs(4 * g[1:-1, 1:-1] - g[:-2, 1:-1] - g[2:, 1:-1] - g[1:-1, :-2] - g[1:-1, 2:]).mean())


def _defocus_card(wd, name, radius):
    R = repo_mod(MM / "render.py", "render")
    steps, hero = _studio_scene(R)
    plain = np.asarray(R.render_image(steps + [hero], 0.25, ss=1))
    focused = np.asarray(R.render_image(steps + [R.Step("dof", [R.defocus(radius)]), hero], 0.25, ss=1))
    from PIL import Image
    Image.fromarray(focused).save(wd / ("%s.png" % name))
    Image.fromarray(plain).save(wd / ("%s_input.png" % name))
    bgreg = (slice(0, 200), slice(150, 300))           # stripes area away from the hero
    hreg = (slice(80, 145), slice(42, 88))             # inside the hero edge zone
    hf_bg, hf_bg0 = _hf(focused[bgreg]), _hf(plain[bgreg])
    hero_same = float(np.abs(focused[hreg].astype(float) - plain[hreg].astype(float)).max())
    return [check("background goes out of focus (high-frequency energy drops > 60%)", hf_bg < 0.4 * hf_bg0, [hf_bg, hf_bg0], "<0.4x"),
            check("the subject painted after defocus stays sharp (unchanged)", hero_same < 2, hero_same, "<2"),
            check("negative control: the unprocessed picture keeps its background detail", not (hf_bg0 < 0.4 * hf_bg0), hf_bg0, "unchanged")], \
        [wd / ("%s.png" % name)]


@card("CAM-156")
def cam156(task, wd):
    """KOSIF Studio scene op defocus(radius) after the background, before the hero (render.py)."""
    return _defocus_card(wd, "defocus", 2.2 * 4)


@card("CAM-170")
def cam170(task, wd):
    """Depth of field (defocus): everything painted so far goes out of focus, optionally inside a soft-edged shape."""
    checks, outs = _defocus_card(wd, "defocus_dof", 2.2 * 4)
    R = repo_mod(MM / "render.py", "render")
    steps, hero = _studio_scene(R)
    shaped = np.asarray(R.render_image(steps + [R.Step("dof", [R.defocus(10, R.rect(600, 0, 600, 800), soft=10)]), hero], 0.25, ss=1))
    plain = np.asarray(R.render_image(steps + [hero], 0.25, ss=1))
    left, right = _hf(shaped[:, :130]) / _hf(plain[:, :130]), _hf(shaped[:, 170:]) / _hf(plain[:, 170:])
    from PIL import Image
    Image.fromarray(shaped).save(wd / "defocus_shape.png")
    checks.append(check("with a shape only the inside defocuses (right half soft, left sharp)", left > 0.9 and right < 0.5, [left, right], [">0.9", "<0.5"]))
    return checks, outs + [wd / "defocus_shape.png"]


def _mblur_card(wd, name, length, angle, mix):
    R = repo_mod(MM / "render.py", "render")
    steps = [R.Step("bg", [R.fill(R.rect(0, 0, 1200, 800), "#101820")]),
             R.Step("drops", [R.fill(R.rect(x, y, 6, 6), "#ffffff") for x in range(40, 1200, 90) for y in range(40, 800, 90)])]
    blurred = np.asarray(R.render_image(steps + [R.Step("mb", [R.motion_blur(R.rect(0, 0, 1200, 800), length, angle, mix)])], 0.5, ss=1))
    plain = np.asarray(R.render_image(steps, 0.5, ss=1))
    from PIL import Image
    Image.fromarray(blurred).save(wd / ("%s.png" % name))

    def streak_angle(a):
        g = a.astype(float).mean(-1)
        ys, xs = np.nonzero(g > 0.25 * g.max())
        # orientation of one drop's streak: second moments of the first drop's neighbourhood
        sel = (xs < 60) & (ys < 60)
        x, y = xs[sel] - xs[sel].mean(), ys[sel] - ys[sel].mean()
        w = g[ys[sel], xs[sel]]
        mxx, myy, mxy = (w * x * x).sum(), (w * y * y).sum(), (w * x * y).sum()
        return math.degrees(0.5 * math.atan2(2 * mxy, mxx - myy)) % 180, float(np.sqrt(max(mxx, myy) / max(1e-9, min(mxx, myy))))
    ang_b, el_b = streak_angle(blurred)
    ang_p, el_p = streak_angle(plain)
    return [check("measured streak runs along the angle", abs(((ang_b - angle) + 90) % 180 - 90) < 6, ang_b, angle),
            check("drops are elongated (streaks)", el_b > 1.8, el_b, ">1.8"),
            check("negative control: the unprocessed drops are round", not (el_p > 1.8), el_p, "<=1.8")], [wd / ("%s.png" % name)]


@card("CAM-157")
def cam157(task, wd):
    """Scene op motion_blur(shape, length, angle) for rain/spray (render.py line-kernel cv2.filter2D)."""
    return _mblur_card(wd, "motionblur", 20, 104, 1.0)


@card("CAM-171")
def cam171(task, wd):
    """Directional motion blur: streaks inside a shape along an angle (spray 7 px at 112 deg, scaled for this sheet)."""
    return _mblur_card(wd, "spray", 18, 112, 1.0)


@card("CAM-172")
def cam172(task, wd):
    """Chromatic aberration (render.py chroma): red and blue channels scale apart toward the frame edges like a real lens."""
    R = repo_mod(MM / "render.py", "render")
    steps = [R.Step("bg", [R.fill(R.rect(0, 0, 1200, 800), "#000000")]),
             R.Step("dots", [R.fill(R.rect(x - 4, y - 4, 8, 8), "#ffffff") for x in (100, 600, 1100) for y in (100, 400, 700)])]
    amount = 6.0
    img = np.asarray(R.render_image(steps + [R.Step("ca", [R.chroma(amount)])], 0.5, ss=1)).astype(float)
    plain = np.asarray(R.render_image(steps, 0.5, ss=1)).astype(float)
    from PIL import Image
    Image.fromarray(img.astype(np.uint8)).save(wd / "chroma.png")

    def shift(a, x, y, ch):
        reg = a[y - 12:y + 13, x - 12:x + 13, ch]
        ys, xs = np.mgrid[-12:13, -12:13]
        return float((reg * xs).sum() / reg.sum()), float((reg * ys).sum() / reg.sum())
    edge = shift(img, 550, 50, 0)[0] - shift(img, 550, 50, 2)[0]
    centre = shift(img, 300, 200, 0)[0] - shift(img, 300, 200, 2)[0]
    k = amount * 0.5 / 600 * 2
    expect = (550 - 300) * (1 + k) - (550 - 300) * (1 - k)
    pe = shift(plain, 550, 50, 0)[0] - shift(plain, 550, 50, 2)[0]
    return [check("red-blue split grows toward the edge (measured centroids)", abs(edge - expect) < 0.4 and abs(centre) < 0.05, [edge, centre], [expect, 0]),
            check("red pushed outward, blue inward at the right edge", shift(img, 550, 50, 0)[0] > 0 > shift(img, 550, 50, 2)[0], [shift(img, 550, 50, 0)[0], shift(img, 550, 50, 2)[0]], "+/-"),
            check("negative control: the unprocessed picture has no split", not abs(pe - expect) < 0.4, pe, "~0")], [wd / "chroma.png"]


@card("CAM-169")
def cam169(task, wd):
    """Sub-frame shutter motion blur and lighten stacking: average k sub-frames at t + s/fps*((j+.5)/k - .5) (shutter 0.5
    frame = 180 deg), or keep each pixel's brightest sample for light trails (film.py's sampling rule, on a numpy scene;
    film.py's own HTML route needs Playwright, which is not installed here)."""
    W, H, fps, k = 200, 60, 30, 8
    v = 300.0                                          # dot speed px/s

    def scene(t):
        a = np.zeros((H, W), np.float32)
        x = 20 + v * t
        xs = np.arange(W)
        a[25:35, :] = np.clip(1 - np.abs(xs - x) / 3, 0, 1)[None, :]
        return a

    def frame(i, shutter, stack):
        t = i / fps
        sub = [scene(t + shutter / fps * ((j + .5) / k - .5)) for j in range(k)]
        return np.max(sub, 0) if stack == "lighten" else np.mean(sub, 0)
    avg = frame(10, 0.5, "average")
    light = frame(10, 30.0 / 8, "lighten")
    sharp_ = scene(10 / fps)
    w = lambda a: int((a[30] > 0.05).sum())
    vid = write_video(wd / "shutter.mp4", [np.repeat((frame(i, 0.5, "average")[..., None] * 255).astype(np.uint8), 3, -1) for i in range(15)], fps)
    exp_len = v * 0.5 / fps
    return [check("180-degree shutter smears the dot over speed x 0.5 frame", abs(w(avg) - (exp_len + 5)) <= 3, w(avg), exp_len + 5),
            check("average keeps total energy (mean of sub-frames)", abs(avg.sum() - sharp_.sum()) / sharp_.sum() < 0.05, float(avg.sum() / sharp_.sum()), 1.0),
            check("lighten stack keeps the brightest sample: a full-brightness trail", light[30].max() > 0.98 and w(light) > 3 * w(avg), [float(light[30].max()), w(light)], [1, ">3x"]),
            check("negative control: a single sample (no shutter) is not smeared", not abs(w(sharp_) - (exp_len + 5)) <= 3, w(sharp_), exp_len + 5)], [vid]


# ───────────────────────────── layout engine: real HTML/CSS laid out by Chrome, rects + pixels measured back ─────────────────────────────

LAY_JS = r"""
function R(s,d){const e=(d||document).querySelector(s); if(!e) return null; const v=(e.ownerDocument.defaultView||window);
  if(v.getComputedStyle(e).display==='none') return null; const r=e.getBoundingClientRect(); return [r.left,r.top,r.width,r.height];}
function RA(s,d){return [...(d||document).querySelectorAll(s)].map(e=>{const r=e.getBoundingClientRect(); return [r.left,r.top,r.width,r.height];});}
function CS(s,p,d){const e=(d||document).querySelector(s); return e?(e.ownerDocument.defaultView||window).getComputedStyle(e).getPropertyValue(p):null;}
function CSA(s,p,d){return [...(d||document).querySelectorAll(s)].map(e=>(e.ownerDocument.defaultView||window).getComputedStyle(e).getPropertyValue(p));}
function FRAME(html,w,h){const f=document.createElement('iframe'); f.style.cssText='position:absolute;left:0;top:0;border:0;width:'+w+'px;height:'+h+'px';
  document.body.appendChild(f); const d=f.contentDocument; d.open(); d.write(html); d.close(); return d;}
"""


def lpage(body, js, W, H, css="", scripts=(), attrs="", bg="#fff"):
    tags = "".join('<script src="%s"></script>' % Path(s).as_uri() for s in scripts)
    return ("<!doctype html><html %s><head><meta charset=utf-8><style>html,body{margin:0;padding:0;overflow:hidden;background:%s}"
            "#view{position:absolute;left:0;top:0;width:%dpx;height:%dpx;overflow:hidden}#OUT{position:absolute;left:-9999px;top:0}.a{position:absolute}%s</style>%s</head><body><div id=view>%s</div>"
            "<pre id=\"OUT\"></pre><script>%s%s\ntry{%s}catch(e){OUT({__error:String(e)+' '+(e.stack||'')})}"
            "</script></body></html>") % (attrs, bg, W, H, css, tags, body, DOM_SAMPLER, LAY_JS, js)


def lay(wd, name, body="", js="OUT(1)", W=320, H=180, css="", scripts=(), attrs="", shot=False, bg="#fff", budget=2000):
    out, sp = chrome_run(wd, name, lpage(body, js, W, H, css, scripts, attrs, bg), size=(W, H), screenshot=shot, budget=budget)
    img = None
    if shot:
        from PIL import Image
        img = np.asarray(Image.open(sp).convert("RGB"))[:H, :W].astype(float)
    return out, img, sp


def lcard(wd, name, spec, crits, naive, extra_files=()):
    """Run the card's layout (spec) and the unprocessed input (spec updated with naive) in Chrome; every criterion is
    measured on the real layout, the first one is measured again on the input and must fail there."""
    out, img, sp = lay(wd, name, **spec)
    o2, img2, _ = lay(wd, name + "_input", **{**spec, "shot": False, **naive})
    checks = []
    for desc, fn, exp in crits:
        try:
            ok, m = fn(out, img)
        except Exception as e:                         # a criterion that cannot even be measured has failed
            ok, m = False, "error: %s" % e
        checks.append(check(desc, ok, m, exp))
    try:
        ok0, m0 = crits[0][1](o2, img2)
    except Exception as e:
        ok0, m0 = False, "not measurable on the input: %s" % e
    checks.append(check("negative control (unprocessed input): " + crits[0][0], not ok0, m0, "fails"))
    (wd / ("%s.json" % name)).write_text(json.dumps({"layout": out, "input": o2}), encoding="utf-8")
    return checks, [wd / ("%s.json" % name)] + ([sp] if sp else []) + list(extra_files)


near = lambda a, b, tol=0.6: a is not None and b is not None and abs(a - b) <= tol
ctr = lambda r: (r[0] + r[2] / 2, r[1] + r[3] / 2)


# ── CAM-02 three-column RTL shell (media queries evaluated per iframe width) ──
SHELL_HTML = ('<!doctype html><html lang=ar dir=rtl><head><style>body{margin:0}%s</style></head><body><div class=shell>'
              '<header class=top>bar</header><aside class=rail-s>s</aside><main class=stage>stage</main><aside class=rail-e>e</aside>'
              '<nav class=nav><a>1</a><a>2</a><a>3</a><a>4</a></nav></div></body></html>')
SHELL_CSS = (".shell{display:grid;grid-template-columns:196px 1fr 300px;grid-template-rows:72px 1fr;height:100vh}"
             "@supports (height:100dvh){.shell{height:100dvh}}"
             ".top{grid-column:1/-1;position:sticky;top:0;height:72px;backdrop-filter:blur(12px);background:rgba(255,255,255,.6)}"
             ".rail-s,.stage,.rail-e{padding:24px;box-sizing:border-box;min-width:0}.nav{display:none}"
             "@media (max-width:1550px){.rail-s,.stage,.rail-e{padding:16px}}"
             "@media (max-width:1280px){.shell{grid-template-columns:184px 1fr 300px}}"
             "@media (max-width:1024px){.shell{grid-template-columns:184px 1fr}.rail-e{display:none}}"
             "@media (max-width:768px){.shell{grid-template-columns:1fr;grid-template-rows:64px 1fr}.top{height:64px}.rail-s{display:none}"
             ".nav{display:grid;grid-template-columns:repeat(4,1fr);position:fixed;left:0;right:0;bottom:0;"
             "min-height:calc(68px + env(safe-area-inset-bottom));padding-bottom:env(safe-area-inset-bottom)}}"
             "@media (max-width:480px){.rail-s,.stage,.rail-e{padding:12px}}")


@card("CAM-02")
def cam02(task, wd):
    """Three-column RTL workspace shell: grid 196px | 1fr | 300px, sticky 72px glass bar (blur 12px), rails collapse at
    1280/1024, a 4-tab bottom nav (min-height 68px + safe area) at 768px, padding 24/16/12 px; laid out by Chrome at five widths."""
    widths = [1600, 1200, 900, 700, 400]
    js = ("const html=%s, W=%s; OUT(W.map(w=>{const d=FRAME(html,w,600); return {w, rs:R('.rail-s',d), st:R('.stage',d), re:R('.rail-e',d),"
          "top:R('.top',d), nav:R('.nav',d), tabs:RA('.nav a',d).length, pad:CS('.stage','padding-top',d), blur:CS('.top','backdrop-filter',d),"
          "pos:CS('.top','position',d), h:R('.shell',d)};}))")
    spec = dict(js=js % (json.dumps(SHELL_HTML % SHELL_CSS), widths), W=320, H=180)
    naive = dict(js=js % (json.dumps(SHELL_HTML % ""), widths))
    cols = lambda o, i: [round(o[i][k][2]) if o[i][k] else 0 for k in ("rs", "st", "re")]
    crits = [("1600 px: columns 196 | 1fr | 300, start rail on the right (RTL)", lambda o, _: (cols(o, 0) == [196, 1104, 300] and round(o[0]["rs"][0] + 196) == 1600, cols(o, 0)), [196, 1104, 300]),
             ("sticky 72 px glass top bar with blur(12px)", lambda o, _: (round(o[0]["top"][3]) == 72 and o[0]["blur"] == "blur(12px)" and o[0]["pos"] == "sticky", [o[0]["top"][3], o[0]["blur"], o[0]["pos"]]), [72, "blur(12px)", "sticky"]),
             ("full-height shell (100dvh)", lambda o, _: (round(o[0]["h"][3]) == 600, o[0]["h"][3]), 600),
             ("padding 24 / 16 / 12 px by breakpoint", lambda o, _: ([o[i]["pad"] for i in (0, 1, 4)] == ["24px", "16px", "12px"], [o[i]["pad"] for i in (0, 1, 4)]), ["24px", "16px", "12px"]),
             ("1200 px: start rail narrows to 184 px", lambda o, _: (cols(o, 1) == [184, 716, 300], cols(o, 1)), [184, 716, 300]),
             ("900 px: end rail collapses", lambda o, _: (cols(o, 2) == [184, 716, 0], cols(o, 2)), [184, 716, 0]),
             ("700 px: rails gone, 64 px bar, 4-tab bottom nav >= 68 px at the bottom", lambda o, _: (cols(o, 3) == [0, 700, 0] and round(o[3]["top"][3]) == 64 and o[3]["tabs"] == 4
                                                                                                    and o[3]["nav"][3] >= 68 and round(o[3]["nav"][1] + o[3]["nav"][3]) == 600, [cols(o, 3), o[3]["top"][3], o[3]["nav"]]), "rails 0, 64, nav 68 at bottom")]
    return lcard(wd, "shell", spec, crits, naive)


# ── CAM-03 logical properties ──
RTL_DOC = '<!doctype html><html lang=ar dir=%s><head><style>body{margin:0;position:relative;width:400px;height:200px}%s</style></head><body><div class=card>بطاقة</div></body></html>'
LOGICAL = (".card{position:absolute;inset-inline-start:20px;inset-block-start:10px;width:100px;height:40px;padding-inline:30px 10px;"
           "margin-block:8px;border-inline-start:6px solid red}")
PHYSICAL = ".card{position:absolute;left:20px;top:10px;width:100px;height:40px;padding-left:30px;padding-right:10px;margin-top:8px;margin-bottom:8px;border-left:6px solid red}"


@card("CAM-03")
def cam03(task, wd):
    """RTL logical-property layout: inset-inline / padding-inline / margin-block / border-inline-start with lang=ar dir=rtl,
    so the same CSS mirrors itself between RTL and LTR (Chrome layout, measured)."""
    js = ("const css=%s, doc=%s; OUT(['rtl','ltr'].map(dir=>{const d=FRAME(doc.replace('%%DIR%%',dir).replace('%%CSS%%',css),400,200);"
          "return {dir, r:R('.card',d), bl:CS('.card','border-left-width',d), br:CS('.card','border-right-width',d), pl:CS('.card','padding-left',d),"
          "pr:CS('.card','padding-right',d), lang:d.documentElement.lang, mt:CS('.card','margin-top',d)};}))")
    doc = json.dumps(RTL_DOC.replace("dir=%s", "dir=%DIR%").replace("%s", "%CSS%"))
    spec = dict(js=js % (json.dumps(LOGICAL), doc))
    naive = dict(js=js % (json.dumps(PHYSICAL), doc))
    rtl = lambda o: o[0]
    crits = [("RTL: the inline-start edge is on the right (20 px from the right, border on the right)",
              lambda o, _: (round(400 - (rtl(o)["r"][0] + rtl(o)["r"][2])) == 20 and rtl(o)["br"] == "6px" and rtl(o)["pr"] == "30px", [400 - (rtl(o)["r"][0] + rtl(o)["r"][2]), rtl(o)["br"], rtl(o)["pr"]]), [20, "6px", "30px"]),
             ("the same CSS in LTR mirrors exactly (x_rtl = W - x_ltr - w)", lambda o, _: (abs(o[0]["r"][0] - (400 - o[1]["r"][0] - o[1]["r"][2])) < 0.01 and o[1]["bl"] == "6px",
                                                                                    [o[0]["r"][0], 400 - o[1]["r"][0] - o[1]["r"][2]]), "equal"),
             ("block-axis margin applied", lambda o, _: (rtl(o)["mt"] == "8px" and round(rtl(o)["r"][1]) == 18, [rtl(o)["mt"], rtl(o)["r"][1]]), ["8px", 18]),
             ("document is lang=ar dir=rtl", lambda o, _: (rtl(o)["lang"] == "ar", rtl(o)["lang"]), "ar")]
    return lcard(wd, "logical", spec, crits, naive)


# ── CAM-04 aspect-specific kinetic layout ──
ASPECT_JS = r"""
function styleLine(r){ return {'9:16':'lockup upper middle inside 10% safe margins, object off-centre in the lower third, top-centre wordmark strip, 40-50% negative space',
  '16:9':'text in the left third, objects on the right, top-centre wordmark strip, 40-50% negative space',
  '1:1':'centred type above the object, top-centre wordmark strip, 40-50% negative space'}[r]; }
function layoutFor(r,W,H){ const m=0.1, box=(a,asp)=>{const A=a*W*H; const w=Math.sqrt(A*asp); return [w, A/w];};
  const P={'9:16':[.24,1.3,.26,1.0],'16:9':[.24,1.1,.26,.8],'1:1':[.18,2.5,.32,1.6]}[r];
  const [tw,th]=box(P[0],P[1]), [ow,oh]=box(P[2],P[3]), [ww,wh]=[W*0.3, H*0.05];
  const L={wm:[(W-ww)/2, H*m*0.5, ww, wh]};
  if(r==='9:16'){ L.txt=[(W-tw)/2, H*0.22, tw, th]; L.obj=[W*0.55-ow/2, H*0.68-oh/2, ow, oh]; }
  else if(r==='16:9'){ L.txt=[W*m, (H-th)/2, tw, th]; L.obj=[W*0.70-ow/2, (H-oh)/2, ow, oh]; }
  else { L.txt=[(W-tw)/2, H*0.14, tw, th]; L.obj=[(W-ow)/2, H*0.65-oh/2, ow, oh]; }
  return L; }
function place(d,L){ for(const k in L){ const e=d.querySelector('#'+k); const v=L[k]; Object.assign(e.style,{position:'absolute',left:v[0]+'px',top:v[1]+'px',width:v[2]+'px',height:v[3]+'px'}); } }
"""
ASPECT_DOC = '<!doctype html><html><body style="margin:0;position:relative;width:%dpx;height:%dpx"><div id=wm></div><div id=txt></div><div id=obj></div></body></html>'


@card("CAM-04")
def cam04(task, wd):
    """Aspect-specific kinetic layout: the style line and placement switch on the ratio (9:16 lockup upper middle, object
    off-centre lower third; 16:9 text left third, objects right; 1:1 centred type above the object), 10% margins,
    40-50% negative space, top-centre wordmark strip; positions measured from Chrome's layout."""
    sizes = {"9:16": (270, 480), "16:9": (480, 270), "1:1": (360, 360)}
    js_t = ("const S=%s, apply=%s; OUT(Object.keys(S).map(r=>{const [W,H]=S[r]; const d=FRAME(%s.replace('%%W',W).replace('%%H',H),W,H);"
            "if(apply) place(d,layoutFor(r,W,H)); return {r,W,H,line:apply?styleLine(r):'', wm:R('#wm',d), txt:R('#txt',d), obj:R('#obj',d)};}))")
    doc = json.dumps(ASPECT_DOC.replace("%dpx;height:%dpx", "%Wpx;height:%Hpx"))
    spec = dict(js=ASPECT_JS + js_t % (json.dumps(sizes), "true", doc))
    naive = dict(js=ASPECT_JS + (js_t % (json.dumps(sizes), "false", doc)).replace("if(apply) place", "place(d,{wm:[0,0,W*.3,H*.04],txt:[0,H*.04,W*.5,H*.2],obj:[0,H*.24,W*.4,H*.4]}); if(false) place"))
    g = lambda o, r: next(x for x in o if x["r"] == r)

    def inside(x, k, m=0.1):
        v = x[k]
        return v[0] >= m * x["W"] - 0.5 and v[1] >= m * x["H"] * 0.5 - 0.5 and v[0] + v[2] <= (1 - m) * x["W"] + 0.5 and v[1] + v[3] <= (1 - m) * x["H"] + 0.5

    def neg(x):
        return 1 - sum(x[k][2] * x[k][3] for k in ("wm", "txt", "obj")) / (x["W"] * x["H"])
    crits = [("16:9: text in the left third, object on the right", lambda o, _: (ctr(g(o, "16:9")["txt"])[0] < 480 / 3 and ctr(g(o, "16:9")["obj"])[0] > 240,
                                                                          [ctr(g(o, "16:9")["txt"])[0], ctr(g(o, "16:9")["obj"])[0]]), ["<160", ">240"]),
             ("9:16: lockup upper middle, object off-centre in the lower third", lambda o, _: (abs(ctr(g(o, "9:16")["txt"])[0] - 135) < 1 and ctr(g(o, "9:16")["txt"])[1] < 240
                                                                                     and ctr(g(o, "9:16")["obj"])[1] > 320 and abs(ctr(g(o, "9:16")["obj"])[0] - 135) > 10,
                                                                                     [ctr(g(o, "9:16")["txt"]), ctr(g(o, "9:16")["obj"])]), "centre-x 135, y<240; obj y>320 off-centre"),
             ("1:1: centred type above the object", lambda o, _: (abs(ctr(g(o, "1:1")["txt"])[0] - 180) < 1 and g(o, "1:1")["txt"][1] + g(o, "1:1")["txt"][3] < g(o, "1:1")["obj"][1],
                                                                 [g(o, "1:1")["txt"], g(o, "1:1")["obj"]]), "type above object"),
             ("every element inside the 10% safe margins (wordmark strip top-centre)", lambda o, _: (all(inside(x, k) for x in o for k in ("txt", "obj", "wm")) and all(abs(ctr(x["wm"])[0] - x["W"] / 2) < 1 for x in o), True), True),
             ("negative space 40-50% in every ratio", lambda o, _: (all(0.40 <= neg(x) <= 0.50 for x in o), [round(neg(x), 3) for x in o]), "0.40-0.50"),
             ("the style line switches on the ratio", lambda o, _: (len({x["line"] for x in o}) == 3 and "left third" in g(o, "16:9")["line"], [x["line"][:30] for x in o]), "3 distinct")]
    return lcard(wd, "aspect", spec, crits, naive)


@card("CAM-28")
def cam28(task, wd):
    """Phone-safe vertical layout: 1080x1920 (laid out at 1/4 scale) with hero centred at ~40% height, headline ~73%,
    footer ~91%, max width 84%, 10% side margins and clean negative space."""
    W, H = 270, 480
    body = '<div id=hero></div><div id=head>عنوان رئيسي واضح</div><div id=foot>@brand</div>'
    css = ("#hero{position:absolute;left:50%;top:40%;width:60%;aspect-ratio:1;transform:translate(-50%,-50%);background:#e04030;border-radius:50%}"
           "#head{position:absolute;left:50%;top:73%;transform:translate(-50%,-50%);max-width:84%;width:max-content;font:700 22px sans-serif;text-align:center;padding:0 2px}"
           "#foot{position:absolute;left:50%;top:91%;transform:translate(-50%,-50%);max-width:84%;font:12px sans-serif}"
           "#view{box-sizing:border-box;padding:0 10%}")
    js = "OUT({hero:R('#hero'), head:R('#head'), foot:R('#foot')})"
    spec = dict(body=body, css=css, js=js, W=W, H=H, attrs="dir=rtl", shot=True)
    naive = dict(css="#hero{width:60%;aspect-ratio:1;background:#e04030}")
    crits = [("hero centre at 40%, headline at 73%, footer at 91% of the height", lambda o, _: (abs(ctr(o["hero"])[1] / H - .40) < .005 and abs(ctr(o["head"])[1] / H - .73) < .005 and abs(ctr(o["foot"])[1] / H - .91) < .005,
                                                                                            [round(ctr(o[k])[1] / H, 4) for k in ("hero", "head", "foot")]), [.40, .73, .91]),
             ("everything centred and inside the 10% side margins (max width 84%)", lambda o, _: (all(abs(ctr(o[k])[0] - W / 2) < 1 and o[k][0] >= 0.1 * W - 0.5 and o[k][2] <= 0.84 * W + 0.5 for k in o),
                                                                                          {k: [round(o[k][0], 1), round(o[k][2], 1)] for k in o}), ">=27 px, <=226.8 px"),
             ("clean negative space: margins of the screenshot are flat background", lambda o, im: (float(im[:, :int(0.1 * W) - 1].std()) < 1.0, float(im[:, :int(0.1 * W) - 1].std())), "<1")]
    return lcard(wd, "phonesafe", spec, crits, naive)


VIDEO_RANGES = {"headline": ("font-size", 64, 120), "body": ("font-size", 28, 42), "label": ("font-size", 18, 24),
                "decor": ("opacity", .12, .25), "card": ("border-top-width", 2, 4), "pad": ("padding-top", 60, 140)}
VS_BODY = ('<div data-role=bg id=bg></div><div data-role=decor class=decor></div><div data-role=card class=card><div data-role=pad class=pad>'
           '<h1 data-role=headline>Launch day</h1><p data-role=body>Everything ships at once.</p><span data-role=label>NEW</span>'
           '<b data-role=accent>40%</b></div></div><i data-role=logo>K</i><em data-role=caption>cap</em>')


@card("CAM-115")
def cam115(task, wd):
    """Video-scale composition rules: headlines 64-120 px, body 28-42, labels 18-24, decorative opacity 12-25%, borders
    2-4 px, padding 60-140 px, 6-10 visual roles, no full-screen linear gradient on dark (H.264 banding); a 1920x1080
    frame laid out by Chrome and audited per role from computed styles."""
    video_css = ("#bg{position:absolute;inset:0;background:#0b0f18 radial-gradient(60% 50% at 50% 40%,#1b2840,transparent)}"
                 ".decor{position:absolute;inset:0;opacity:.18;background:#fff}.card{position:absolute;left:160px;top:140px;border:3px solid #fff}"
                 ".pad{padding:96px}h1{font-size:96px;margin:0}p{font-size:34px}span{font-size:20px}b{font-size:72px}")
    web_css = ("#bg{position:absolute;inset:0;background:linear-gradient(#0b0f18,#000)}.decor{position:absolute;inset:0;opacity:.6;background:#fff}"
               ".card{position:absolute;left:16px;top:16px;border:1px solid #fff}.pad{padding:16px}h1{font-size:32px;margin:0}p{font-size:16px}span{font-size:12px}")
    js = ("const RG=%s; const out={}; for(const r in RG){ const v=CS('[data-role='+r+']', RG[r][0]); out[r]=parseFloat(v); }"
          "out.roles=new Set([...document.querySelectorAll('[data-role]')].map(e=>e.dataset.role)).size;"
          "const full=[...document.querySelectorAll('*')].filter(e=>{const r=e.getBoundingClientRect(); return r.width>=1920&&r.height>=1080;});"
          "out.fullLinear=full.filter(e=>/linear-gradient/.test(getComputedStyle(e).backgroundImage)).length; OUT(out)") % json.dumps(VIDEO_RANGES)
    spec = dict(body=VS_BODY, css=video_css, js=js, W=1920, H=1080)
    naive = dict(css=web_css)
    inr = lambda o: {r: (lo <= o[r] <= hi) for r, (_, lo, hi) in VIDEO_RANGES.items()}
    crits = [("every role measured inside its video range", lambda o, _: (all(inr(o).values()), {r: o[r] for r in VIDEO_RANGES}), {r: [lo, hi] for r, (_, lo, hi) in VIDEO_RANGES.items()}),
             ("6-10 visual roles", lambda o, _: (6 <= o["roles"] <= 10, o["roles"]), "6-10"),
             ("no full-screen linear gradient on the dark frame", lambda o, _: (o["fullLinear"] == 0, o["fullLinear"]), 0)]
    return lcard(wd, "videoscale", spec, crits, naive)


def ff(*args, timeout=40):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *map(str, args)], capture_output=True, text=True, timeout=timeout)
    if r.returncode:
        raise RuntimeError("ffmpeg: " + r.stderr[-400:])


@card("CAM-116")
def cam116(task, wd):
    """Picture-in-picture: the clip plays inside a framed window (4 px white frame) over a designed background
    (ffmpeg pad + overlay); measured: only the window changes over time, the frame and background stay fixed."""
    out, raw = wd / "pip.mp4", wd / "clip_fullscreen.mp4"
    ff("-f", "lavfi", "-i", "color=c=0x203040:s=320x180:d=2:r=10", "-f", "lavfi", "-i", "testsrc2=s=160x90:d=2:r=10",
       "-filter_complex", "[0]drawbox=x=0:y=150:w=320:h=30:color=0xe0a030:t=fill[bg];[1]pad=168:98:4:4:color=white[w];[bg][w]overlay=x=136:y=40",
       "-c:v", "libx264rgb", "-qp", "0", out)
    ff("-f", "lavfi", "-i", "testsrc2=s=320x180:d=2:r=10", "-c:v", "libx264rgb", "-qp", "0", raw)
    v, vr = read_video(out).astype(float), read_video(raw).astype(float)
    win = (slice(44, 134), slice(140, 300))
    mask = np.ones(v.shape[1:3], bool)
    mask[40:138, 136:304] = False

    def outside_static(a):
        return float(np.abs(np.diff(a, axis=0)).max(-1).max(0)[mask].max())
    inside = float(np.abs(np.diff(v[:, win[0], win[1]], axis=0)).mean())
    frame = v[0, 40:44, 136:304].mean((0, 1))
    return [check("only the window moves: the background around it is static", outside_static(v) < 1, outside_static(v), "<1"),
            check("the clip plays inside the window", inside > 2, inside, ">2"),
            check("4 px white frame around the window", float(np.abs(frame - 255).max()) < 2 and float(np.abs(v[0, 136, 150] - 255).max()) < 2, frame, [255, 255, 255]),
            check("designed background (base colour + accent band) shows around the window",
                  np.abs(v[0, 10, 10] - [0x20, 0x30, 0x40]).max() < 3 and np.abs(v[0, 165, 10] - [0xe0, 0xa0, 0x30]).max() < 3, [v[0, 10, 10], v[0, 165, 10]], ["#203040", "#e0a030"]),
            check("negative control: the unprocessed full-frame clip moves everywhere", not outside_static(vr) < 1, outside_static(vr), ">=1")], [out]


@card("CAM-117")
def cam117(task, wd):
    """Title card with fade + slideshow with section headers as one top-level GSAP composition (master timeline nests
    the title timeline and the slideshow timeline); opacities and the visible section header measured per frame."""
    body = ('<div id=title class=a style="inset:0;display:grid;place-items:center;font:700 28px sans-serif">العنوان</div>'
            + "".join('<div id=s%d class=a style="inset:0;opacity:0"><h2 style="margin:8px">قسم %d</h2></div>' % (i, i + 1) for i in range(3)))
    js = ("var tl=gsap.timeline({paused:true}); const title=gsap.timeline().fromTo('#title',{opacity:0},{opacity:1,duration:.6,ease:'none',immediateRender:false},.2)"
          ".to('#title',{opacity:0,duration:.6,ease:'none'},2.4); const show=gsap.timeline(); for(let i=0;i<3;i++){"
          "show.to('#s'+i,{opacity:1,duration:.4,ease:'none'},i*2); if(i<2) show.to('#s'+i,{opacity:0,duration:.4,ease:'none'},i*2+2);}"
          "gsap.set('#title',{opacity:0}); tl.add(title,0).add(show,3.0);"
          "const T=[...Array(91).keys()].map(i=>i/10); OUT(SAMPLE(T,['#title','#s0','#s1','#s2'],t=>[...document.querySelectorAll('h2')]"
          ".map(h=>__op(h))))")
    spec = dict(body=body, js=js, scripts=[GSAP], W=320, H=180)
    naive = dict(js=js.replace("tl.add(title,0).add(show,3.0);", "").replace("gsap.set('#title',{opacity:0});", ""))
    T = [i / 10 for i in range(91)]
    op = lambda o, k: [f["el"][k]["o"] for f in o]

    def title_ok(o):
        a = op(o, 0)
        model = [min(1, max(0, (t - .2) / .6)) if t < 2.4 else max(0, 1 - (t - 2.4) / .6) for t in T]
        return max(abs(x - y) for x, y in zip(a, model)) < 1e-3, [a[1], a[5], a[20], a[27], a[30]]

    def header_at(o, t):
        i = T.index(t)
        hs = o[i]["x"]
        return int(np.argmax(hs)) + 1 if max(hs) > 0.5 else 0
    crits = [("title fades in 0.2-0.8 s and out 2.4-3.0 s (linear model)", lambda o, _: title_ok(o), "max err < 1e-3"),
             ("slideshow starts after the title: section header 1, 2, 3 at 3.6 / 5.6 / 7.6 s", lambda o, _: ([header_at(o, t) for t in (3.6, 5.6, 7.6)] == [1, 2, 3], [header_at(o, t) for t in (3.6, 5.6, 7.6)]), [1, 2, 3]),
             ("crossfade 0.4 s: mid-crossfade both slides are half visible", lambda o, _: (abs(op(o, 1)[T.index(5.2)] - .5) < 1e-3 and abs(op(o, 2)[T.index(5.2)] - .5) < 1e-3,
                                                                                         [op(o, 1)[T.index(5.2)], op(o, 2)[T.index(5.2)]]), [.5, .5]),
             ("nothing overlaps the title: slides hidden while the title is up", lambda o, _: (max(max(op(o, k)[:30]) for k in (1, 2, 3)) == 0, max(max(op(o, k)[:30]) for k in (1, 2, 3))), 0)]
    return lcard(wd, "titleslides", spec, crits, naive)


@card("CAM-118")
def cam118(task, wd):
    """Broadcast safe zones: action-safe = 90% of the frame (5% inset), title-safe = 80% (10% inset); elements are
    clamped into their zone and the result is measured on a 1920x1080 layout."""
    js = r"""
const W=1920,H=1080, ZONES={action:.05,title:.10};
function safeRect(kind){const i=ZONES[kind]; return [i*W,i*H,W*(1-2*i),H*(1-2*i)];}
function clampTo(el,kind){const [x,y,w,h]=safeRect(kind); const r=el.getBoundingClientRect();
  el.style.left=Math.min(Math.max(r.left,x),x+w-r.width)+'px'; el.style.top=Math.min(Math.max(r.top,y),y+h-r.height)+'px';}
const els=[['#ttl','title'],['#l3','title'],['#logo','action'],['#bug','action']];
if(APPLY) els.forEach(([s,k])=>clampTo(document.querySelector(s),k));
['action','title'].forEach(k=>{const g=document.createElement('div'); g.id='g_'+k; g.className='a'; const r=safeRect(k);
  Object.assign(g.style,{left:r[0]+'px',top:r[1]+'px',width:r[2]+'px',height:r[3]+'px'}); document.getElementById('view').appendChild(g);});
OUT({els:els.map(([s,k])=>[k,R(s)]), action:R('#g_action'), title:R('#g_title')});"""
    body = ('<div id=ttl class=a style="left:20px;top:40px;width:900px;height:120px"></div><div id=l3 class=a style="left:60px;top:960px;width:800px;height:100px"></div>'
            '<div id=logo class=a style="left:1860px;top:10px;width:120px;height:60px"></div><div id=bug class=a style="left:0;top:1040px;width:80px;height:80px"></div>')
    spec = dict(body=body, js="const APPLY=true;" + js, W=1920, H=1080)
    naive = dict(js="const APPLY=false;" + js)

    def inside(r, z):
        return r[0] >= z[0] - .01 and r[1] >= z[1] - .01 and r[0] + r[2] <= z[0] + z[2] + .01 and r[1] + r[3] <= z[1] + z[3] + .01
    crits = [("every element sits inside its safe zone (titles 10% inset, action 5% inset)", lambda o, _: (all(inside(r, o[k]) for k, r in o["els"]), [[k, [round(v) for v in r]] for k, r in o["els"]]), "inside"),
             ("action-safe = 90% of the frame (5% inset)", lambda o, _: ([round(v) for v in o["action"]] == [96, 54, 1728, 972], o["action"]), [96, 54, 1728, 972]),
             ("title-safe = 80% of the frame (10% inset)", lambda o, _: ([round(v) for v in o["title"]] == [192, 108, 1536, 864], o["title"]), [192, 108, 1536, 864])]
    return lcard(wd, "safezones", spec, crits, naive)


def _caption_frames(kind, W=180, H=320, n=3):
    """3 sampled frames of a synthetic shot: a moving textured subject, flat clean areas and (optionally) a baked graphic."""
    rng = np.random.default_rng(7)
    tex = rng.integers(40, 220, (H, W, 3)).astype(np.uint8)
    frames = []
    for i in range(n):
        f = np.zeros((H, W, 3), np.uint8) + np.array([70, 90, 110], np.uint8)
        if kind == "side":                             # subject on the left, a baked logo top-right
            x0, x1, y0, y1 = 10 + 2 * i, 80 + 2 * i, 60, 300
            f[10:40, 130:170] = tex[10:40, 130:170]
        elif kind == "portrait":                       # subject fills the centre
            x0, x1, y0, y1 = 25 + i, 155 + i, 110, 320
        else:                                          # narrow centred subject looking right
            x0, x1, y0, y1 = 70 + i, 110 + i, 80, 300
        f[y0:y1, x0:x1] = tex[y0:y1, x0:x1]
        frames.append(f)
    return frames


def caption_place(frames, gaze=None, cw=0.42, ch=0.12):
    """layout heuristics: detail + motion map over 3 frames -> clean cells; scene type; bigger clean zone; crown; validate."""
    a = np.stack([f.astype(float).mean(-1) for f in frames])
    H, W = a.shape[1:]
    grad = np.abs(np.diff(a, axis=2, prepend=a[:, :, :1])).mean(0) + np.abs(np.diff(a, axis=1, prepend=a[:, :1])).mean(0)
    busy = (grad + a.std(0)) > 4
    cell = 10
    bc = busy[:H // cell * cell, :W // cell * cell].reshape(H // cell, cell, W // cell, cell).any((1, 3))
    cols = bc.any(0)
    subj = a.std(0) > 2                                # the moving subject
    sx = np.nonzero(subj.any(0))[0]
    sw = (sx.max() - sx.min() + 1) / W if len(sx) else 0
    zones = {"left": (0, 0, int(sx.min()) if len(sx) else W // 2, H), "right": (int(sx.max()) + 1 if len(sx) else W // 2, 0, W, H),
             "top": (0, 0, W, int(np.nonzero(subj.any(1))[0].min()) if len(sx) else H // 4)}

    def clean_area(z):
        x0, y0, x1, y1 = z
        return float((~busy[y0:y1, x0:x1]).sum())
    if sw > 0.55:
        kind, side = "portrait-header", "top"
    else:
        kind = "corner-column-crown"
        l, r = clean_area(zones["left"]), clean_area(zones["right"])
        side = ("right" if r >= l else "left") if abs(l - r) > 0.1 * max(l, r) or gaze is None else gaze
    x0, y0, x1, y1 = zones[side]
    # crown: the first clean band of caption height inside the zone, from the top
    hh, ww = int(ch * H), min(int(cw * W), x1 - x0)
    rect = None
    for yy in range(y0, y1 - hh, 2):
        for xx in ([x0 + (x1 - x0 - ww) // 2] if side == "top" else [x0, x1 - ww]):
            if not busy[yy:yy + hh, xx:xx + ww].any():
                rect = (xx, yy, ww, hh)
                break
        if rect:
            break
    return {"type": kind, "side": side, "rect": rect, "busy": busy, "subject_w": sw}


def caption_valid(rect, busy):
    if rect is None:
        return False
    x, y, w, h = rect
    return not busy[y:y + h, x:x + w].any()


@card("CAM-120")
def cam120(task, wd):
    """Caption scene types + layout heuristics: sample 3 frames, find the clean zone (no subject motion, no baked
    graphic), pick the scene type (portrait-header when the subject fills the centre, else corner-column-crown on the
    bigger clean side, gaze breaks ties), place the crown and validate it."""
    from PIL import Image, ImageDraw
    res, outs = {}, []
    for kind, gaze in (("side", None), ("portrait", None), ("narrow", "right")):
        fr = _caption_frames(kind)
        r = caption_place(fr, gaze)
        res[kind] = r
        im = Image.fromarray(fr[0])
        if r["rect"]:
            x, y, w, h = r["rect"]
            ImageDraw.Draw(im).rectangle([x, y, x + w - 1, y + h - 1], outline=(255, 0, 0), width=2)
        p = wd / ("caption_%s.png" % kind)
        im.save(p)
        outs.append(p)
    centred = {k: (int(0.29 * 180), int(0.44 * 320), int(0.42 * 180), int(0.12 * 320)) for k in res}
    summary = {k: {"type": v["type"], "side": v["side"], "rect": v["rect"], "subject_w": v["subject_w"]} for k, v in res.items()}
    (wd / "captions.json").write_text(json.dumps(summary), encoding="utf-8")
    return [check("every placed caption validates (no subject, no baked graphic under it)", all(caption_valid(v["rect"], v["busy"]) for v in res.values()), {k: v["rect"] for k, v in res.items()}, "valid"),
            check("subject left, logo top-right -> corner-column-crown on the right, below the logo", res["side"]["type"] == "corner-column-crown" and res["side"]["side"] == "right" and res["side"]["rect"][1] >= 40,
                  [res["side"]["type"], res["side"]["side"], res["side"]["rect"]], ["corner-column-crown", "right", "y>=40"]),
            check("subject fills the centre -> portrait-header (top banner)", res["portrait"]["type"] == "portrait-header" and res["portrait"]["rect"][1] + res["portrait"]["rect"][3] <= 110,
                  [res["portrait"]["type"], res["portrait"]["rect"]], "portrait-header above the subject"),
            check("equal clean sides -> the gaze side (looking room)", res["narrow"]["side"] == "right", res["narrow"]["side"], "right"),
            check("negative control: a default centred caption fails validation", not any(caption_valid(centred[k], res[k]["busy"]) for k in res), [caption_valid(centred[k], res[k]["busy"]) for k in res], "all invalid")], \
        [wd / "captions.json"] + outs


@card("CAM-122")
def cam122(task, wd):
    """Recut card zones: storyboard card.zone resolved to pixels by the card host (fullscreen, whiteboard-area 40 px
    inset landscape / bottom 45% portrait, lower-third bottom 30%, side-panel right 42% / bottom 40% portrait,
    video-overlay transparent root); measured in a 1920x1080 and a 1080x1920 host."""
    js = r"""
const SB=[{id:'c1',zone:'fullscreen'},{id:'c2',zone:'whiteboard-area'},{id:'c3',zone:'lower-third'},{id:'c4',zone:'side-panel'},{id:'c5',zone:'video-overlay'}];
function zoneRect(z,W,H){const P=H>W; return {'fullscreen':[0,0,W,H],'whiteboard-area':P?[0,.55*H,W,.45*H]:[40,40,W-80,H-80],
  'lower-third':[0,.7*H,W,.3*H],'side-panel':P?[0,.6*H,W,.4*H]:[.58*W,0,.42*W,H],'video-overlay':[0,0,W,H]}[z];}
function host(W,H){const d=FRAME('<!doctype html><body style="margin:0;position:relative;width:'+W+'px;height:'+H+'px"></body>',W,H);
  for(const c of SB){const e=d.createElement('div'); e.id=c.id; e.style.position='absolute'; e.style.background=c.zone==='video-overlay'?'transparent':'#fff';
    const r=USE?zoneRect(c.zone,W,H):[0,0,W,H]; Object.assign(e.style,{left:r[0]+'px',top:r[1]+'px',width:r[2]+'px',height:r[3]+'px'}); d.body.appendChild(e);}
  return Object.fromEntries(SB.map(c=>[c.zone,R('#'+c.id,d)]).concat([['overlay_bg',CS('#c5','background-color',d)]]));}
OUT({land:host(1920,1080), port:host(1080,1920)});"""
    spec = dict(js="const USE=true;" + js)
    naive = dict(js="const USE=false;" + js)
    rr = lambda r: [round(v) for v in r]
    crits = [("lower-third = bottom 30% in both hosts", lambda o, _: (rr(o["land"]["lower-third"]) == [0, 756, 1920, 324] and rr(o["port"]["lower-third"]) == [0, 1344, 1080, 576],
                                                                  [o["land"]["lower-third"], o["port"]["lower-third"]]), [[0, 756, 1920, 324], [0, 1344, 1080, 576]]),
             ("whiteboard-area: 40 px inset landscape, bottom 45% portrait", lambda o, _: (rr(o["land"]["whiteboard-area"]) == [40, 40, 1840, 1000] and rr(o["port"]["whiteboard-area"]) == [0, 1056, 1080, 864],
                                                                                        [o["land"]["whiteboard-area"], o["port"]["whiteboard-area"]]), [[40, 40, 1840, 1000], [0, 1056, 1080, 864]]),
             ("side-panel: right 42% landscape, bottom 40% portrait", lambda o, _: (rr(o["land"]["side-panel"]) == [1114, 0, 806, 1080] and rr(o["port"]["side-panel"]) == [0, 1152, 1080, 768],
                                                                                 [o["land"]["side-panel"], o["port"]["side-panel"]]), [[1114, 0, 806, 1080], [0, 1152, 1080, 768]]),
             ("fullscreen covers the frame; video-overlay root is transparent", lambda o, _: (rr(o["land"]["fullscreen"]) == [0, 0, 1920, 1080] and o["land"]["overlay_bg"] == "rgba(0, 0, 0, 0)",
                                                                                           [o["land"]["fullscreen"], o["land"]["overlay_bg"]]), [[0, 0, 1920, 1080], "rgba(0, 0, 0, 0)"])]
    return lcard(wd, "zones", spec, crits, naive)


THUMB_CSS = (".th{position:absolute;overflow:hidden;background:#10223a}.hero{position:absolute;background:#ff3b30;border-radius:12px}"
             ".msg{position:absolute;color:#ffd400;font:900 30px/1 sans-serif;white-space:nowrap}")


@card("CAM-158")
def cam158(task, wd):
    """Thumbnail composition rule at 1280x720, 1080x1080 and 1080x1920 (laid out at 1/4 scale in Chrome and screenshot):
    hero fills ~40% of the frame, a 3-word message inside the 10% safe zone, readable at 160 px width, max 3 main colours."""
    th = [("t169", 0, 0, 320, 180, "left:130px;top:24px;width:180px;height:132px", "left:32px;top:30px;font-size:24px"),
          ("t11", 330, 0, 270, 270, "left:35px;top:108px;width:200px;height:150px", "left:27px;top:30px"),
          ("t916", 610, 0, 270, 480, "left:27px;top:198px;width:216px;height:244px", "left:27px;top:60px")]
    body = "".join('<div class=th id=%s style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"><div class=hero style="%s"></div>'
                   '<div class=msg style="%s">CUT IT NOW</div></div>' % (i, x, y, w, h, hs, ms) for i, x, y, w, h, hs, ms in th)
    naive_body = "".join('<div class=th id=%s style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">%s<div class=hero style="left:10px;top:10px;width:60px;height:40px"></div>'
                         '<div class=msg style="left:2px;top:%dpx;font-size:9px;color:#fff">How I finally learned to cut videos fast</div></div>'
                         % (i, x, y, w, h, "".join('<i class=a style="left:%dpx;top:%dpx;width:30px;height:30px;background:%s"></i>' % (20 + 40 * k, 80, c)
                                                    for k, c in enumerate(["#0f0", "#0ff", "#f0f", "#fff", "#888"])), h - 20) for i, x, y, w, h, _, _ in th)
    js = "OUT(%s.map(i=>({i, box:R('#'+i), hero:R('#'+i+' .hero'), msg:R('#'+i+' .msg'), words:document.querySelector('#'+i+' .msg').textContent.trim().split(/\\s+/).length})))" % json.dumps([t[0] for t in th])
    spec = dict(body=body, css=THUMB_CSS, js=js, W=880, H=480, shot=True)
    naive = dict(body=naive_body, shot=True)

    def crop(im, b):
        return im[int(b[1]):int(b[1] + b[3]), int(b[0]):int(b[0] + b[2])]

    def hero_frac(o, im):
        return [float((np.abs(crop(im, t["box"]) - [255, 59, 48]).max(-1) < 30).mean()) for t in o]

    def main_colours(o, im):
        n = []
        for t in o:
            q = (crop(im, t["box"]) // 64).astype(int)
            k = q[..., 0] * 16 + q[..., 1] * 4 + q[..., 2]
            cnt = np.bincount(k.ravel(), minlength=64) / k.size
            n.append(int((cnt > 0.02).sum()))
        return n

    def safe(t):
        b, m = t["box"], t["msg"]
        return m[0] - b[0] >= 0.1 * b[2] - .5 and m[1] - b[1] >= 0.1 * b[3] - .5 and m[0] + m[2] <= b[0] + 0.9 * b[2] + .5 and m[1] + m[3] <= b[1] + 0.9 * b[3] + .5
    crits = [("hero fills >= 40% of every frame", lambda o, im: (all(f >= 0.40 for f in hero_frac(o, im)), hero_frac(o, im)), ">=0.40"),
             ("3-word message inside the 10% safe zone", lambda o, im: (all(t["words"] == 3 and safe(t) for t in o), [[t["words"], safe(t)] for t in o]), [3, True]),
             ("readable at 160 px width: text >= 10 px tall after scaling", lambda o, im: (all(t["msg"][3] * 160 / t["box"][2] >= 10 for t in o), [round(t["msg"][3] * 160 / t["box"][2], 1) for t in o]), ">=10"),
             ("max 3 main colours (each > 2% of pixels)", lambda o, im: (all(n <= 3 for n in main_colours(o, im)), main_colours(o, im)), "<=3")]
    return lcard(wd, "thumbs", spec, crits, naive)


def lum(a):
    return a[..., 0] * .2126 + a[..., 1] * .7152 + a[..., 2] * .0722


def hf(a):
    """mean |Laplacian| of a screenshot region (sharpness)."""
    return _hf(a)


SPLIT_W, SPLIT_H = 480, 270


@card("CAM-211")
def cam211(task, wd):
    """Feature beat split layout: left column (35%, 6% margins) with numbered pill + feature name, 2-line headline, grey
    body and 3 tag chips; right a browser window at 60% width with a large soft shadow (Chrome layout, measured)."""
    W, H = SPLIT_W, SPLIT_H
    body = ('<div id=col><span id=pill>02 · Export</span><h1 id=hl>Ship every cut in one click</h1><p id=bd>Renders and uploads.</p>'
            '<div id=chips><i>MP4</i><i>H.264</i><i>9:16</i></div></div><div id=win><div id=chrome></div></div>')
    css = ("#view{background:#f4f4f2;font-family:sans-serif}#col{position:absolute;left:6%;top:6%;width:29%;bottom:6%;display:flex;flex-direction:column;gap:6px}"
           "#pill{align-self:flex-start;border-radius:99px;background:#111;color:#fff;font-size:9px;padding:2px 8px}#hl{font-size:19px;line-height:22px;margin:0}"
           "#bd{color:#8a8a8a;font-size:10px;margin:0}#chips{display:flex;gap:4px}#chips i{font-style:normal;font-size:8px;border:1px solid #bbb;border-radius:9px;padding:1px 5px}"
           "#win{position:absolute;left:38%;top:12%;width:60%;height:76%;background:#fff;border-radius:8px;box-shadow:0 24px 60px rgba(0,0,0,.25)}"
           "#chrome{height:14px;background:#e8e8e8;border-radius:8px 8px 0 0}")
    js = "OUT({col:R('#col'), pill:R('#pill'), hl:R('#hl'), win:R('#win'), chips:RA('#chips i').length, grey:CS('#bd','color'), sh:CS('#win','box-shadow'), lh:CS('#hl','line-height')})"
    spec = dict(body=body, css=css, js=js, W=W, H=H)
    naive = dict(css="")
    crits = [("left column ends at 35% (6% margin), window is 60% wide on the right", lambda o, _: (near(o["col"][0], .06 * W) and near(o["col"][0] + o["col"][2], .35 * W) and near(o["win"][2], .60 * W) and o["win"][0] > o["col"][0] + o["col"][2],
                                                                                              [o["col"][0], o["col"][0] + o["col"][2], o["win"][2]]), [.06 * W, .35 * W, .60 * W]),
             ("headline wraps to exactly 2 lines", lambda o, _: (round(o["hl"][3] / 22) == 2, o["hl"][3] / 22), 2),
             ("numbered pill, grey body, 3 tag chips", lambda o, _: (o["chips"] == 3 and o["grey"] == "rgb(138, 138, 138)" and o["pill"][1] < o["hl"][1], [o["chips"], o["grey"]]), [3, "rgb(138, 138, 138)"]),
             ("large soft shadow on the window (blur >= 40 px)", lambda o, _: (float(re.findall(r"([\d.]+)px", o["sh"])[2]) >= 40, o["sh"]), ">=40px")]
    return lcard(wd, "featurebeat", spec, crits, naive)


@card("CAM-216")
def cam216(task, wd):
    """Split text/UI layout: headline in the left 40%, a UI card with a shadow on the right."""
    W, H = SPLIT_W, SPLIT_H
    body = '<h1 id=hl>One timeline for every format</h1><div id=card></div>'
    css = ("#hl{position:absolute;left:0;top:0;width:40%;height:100%;box-sizing:border-box;padding:0 5%;display:flex;align-items:center;font:700 22px sans-serif;margin:0}"
           "#card{position:absolute;left:46%;top:15%;width:48%;height:70%;background:#fff;border-radius:10px;box-shadow:0 18px 40px rgba(0,0,0,.3)}#view{background:#e9ecf1}")
    js = "OUT({hl:R('#hl'), card:R('#card'), sh:CS('#card','box-shadow')})"
    crits = [("headline occupies the left 40%", lambda o, _: (near(o["hl"][0], 0) and near(o["hl"][2], .4 * W), o["hl"]), [0, .4 * W]),
             ("UI card entirely in the right 60% and vertically centred", lambda o, _: (o["card"][0] >= .4 * W and o["card"][0] + o["card"][2] <= W and abs(ctr(o["card"])[1] - H / 2) < 1, o["card"]), "x>=192, centred"),
             ("the card carries a drop shadow", lambda o, _: (o["sh"] != "none", o["sh"]), "box-shadow")]
    return lcard(wd, "splitui", dict(body=body, css=css, js=js, W=W, H=H), crits, dict(css=""))


@card("CAM-231")
def cam231(task, wd):
    """Split headline + UI card: 40/60 split, 6% margins, 2-line headline with the key word in green."""
    W, H = SPLIT_W, SPLIT_H
    body = '<h1 id=hl>Edit <b id=kw>faster</b> than you talk</h1><div id=card></div>'
    css = ("#hl{position:absolute;left:6%;top:50%;transform:translateY(-50%);width:34%;font:700 20px/24px sans-serif;margin:0}#kw{color:#1db954}"
           "#card{position:absolute;left:40%;top:6%;width:54%;height:88%;background:#fff;border-radius:10px;box-shadow:0 10px 30px rgba(0,0,0,.2)}#view{background:#eef0f3}")
    js = "OUT({hl:R('#hl'), card:R('#card'), kw:CS('#kw','color'), rest:CS('#hl','color')})"
    crits = [("40/60 split with 6% margins", lambda o, _: (near(o["hl"][0], .06 * W) and near(o["hl"][0] + o["hl"][2], .40 * W) and near(o["card"][0], .40 * W) and near(o["card"][0] + o["card"][2], .94 * W) and near(o["card"][1], .06 * H),
                                                         [o["hl"][0], o["hl"][0] + o["hl"][2], o["card"][0], o["card"][0] + o["card"][2]]), [.06 * W, .4 * W, .4 * W, .94 * W]),
             ("headline is 2 lines", lambda o, _: (round(o["hl"][3] / 24) == 2, o["hl"][3] / 24), 2),
             ("key word green, the rest not", lambda o, _: (o["kw"] == "rgb(29, 185, 84)" and o["rest"] != o["kw"], [o["kw"], o["rest"]]), "rgb(29, 185, 84)")]
    return lcard(wd, "splitgreen", dict(body=body, css=css, js=js, W=W, H=H), crits, dict(css=""))


@card("CAM-257")
def cam257(task, wd):
    """Editorial split feature beat: text column 35% (headline + one-line subline), dark UI card 50% wide with a large
    soft shadow sliding in from the right, 6% margins; GSAP slide measured frame by frame."""
    W, H = SPLIT_W, SPLIT_H
    body = '<div id=txt><h1>Color, solved</h1><p id=sub>One click grade.</p></div><div id=card></div>'
    css = ("#txt{position:absolute;left:6%;top:30%;width:35%;font-family:sans-serif}#txt h1{font-size:24px;margin:0}#sub{white-space:nowrap;font-size:11px;margin:0}"
           "#card{position:absolute;left:44%;top:12%;width:50%;height:76%;background:#15161a;border-radius:12px;box-shadow:0 30px 70px rgba(0,0,0,.35)}")
    anim = "gsap.set('#card',{x:160,opacity:0}); tl.fromTo('#card',{x:160,opacity:0},{x:0,opacity:1,duration:.6,ease:'power3.out',immediateRender:false},0.2);"
    js = ("var tl=gsap.timeline({paused:true}); " + anim +
          "const T=[...Array(11).keys()].map(i=>i/10); const fr=SAMPLE(T,['#card']); OUT({fr, txt:R('#txt'), sub:R('#sub'), card:R('#card'), bg:CS('#card','background-color'), sh:CS('#card','box-shadow')})")
    T = [i / 10 for i in range(11)]
    p3 = lambda x: 1 - (1 - x) ** 4
    xs = lambda o: [f["el"][0]["q"][0][0] for f in o["fr"]]
    model = [0.44 * W + 160 * (1 - p3(min(1, max(0, (t - .2) / .6)))) for t in T]
    crits = [("card slides in from the right on power3.out and lands at 44% (6% right margin)", lambda o, _: (maxerr(xs(o), model) < 0.05 and near(o["card"][0] + o["card"][2], .94 * W), [round(v, 2) for v in xs(o)[::2]]), [round(v, 2) for v in model[::2]]),
             ("text column 35% with a one-line subline", lambda o, _: (near(o["txt"][2], .35 * W) and o["sub"][3] < 16, [o["txt"][2], o["sub"][3]]), [.35 * W, "1 line"]),
             ("card 50% wide, dark, large soft shadow", lambda o, _: (near(o["card"][2], .5 * W) and o["bg"] == "rgb(21, 22, 26)" and float(re.findall(r"([\d.]+)px", o["sh"])[2]) >= 40, [o["card"][2], o["bg"], o["sh"]]), [240, "dark", ">=40px"])]
    return lcard(wd, "editorialsplit", dict(body=body, css=css, js=js, W=W, H=H, scripts=[GSAP]), crits, dict(js=js.replace(anim, "")))


@card("CAM-220")
def cam220(task, wd):
    """Negative-space headline: short 1-2 line headline centred at ~6% of the frame height, the accent word in the brand
    colour #f03c0a, everything else black on an empty frame (screenshot measured)."""
    W, H = 480, 270
    body = '<div id=hl>make it <b id=ac>simple</b>.</div>'
    css = "#view{background:#fff}#hl{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);font:700 16px/1 sans-serif;color:#000;white-space:nowrap}#ac{color:#f03c0a}"
    js = "OUT({hl:R('#hl'), ac:R('#ac'), fs:CS('#hl','font-size')})"

    def colours(im):
        px = im.reshape(-1, 3)
        acc = (np.abs(px - [240, 60, 10]).max(-1) < 40).sum()
        dark = (px.max(-1) < 60).sum()
        w = np.array([255., 255, 255])

        def resid(c):                                  # distance to the white -> c blend segment (antialiasing)
            d = np.array(c, float) - w
            a = np.clip(((px - w) @ d) / (d @ d), 0, 1)
            return np.abs(px - (w + a[:, None] * d)).max(-1)
        other = (np.minimum(resid([240, 60, 10]), resid([0, 0, 0])) > 25).sum()
        return int(acc), int(dark), int(other)
    crits = [("headline centred, ~6% of the height", lambda o, _: (abs(ctr(o["hl"])[0] - W / 2) < 1 and abs(ctr(o["hl"])[1] - H / 2) < 1 and abs(o["hl"][3] / H - .06) < .01, [ctr(o["hl"]), o["hl"][3] / H]), "centre, 0.06"),
             ("accent pixels only inside the accent word", lambda o, im: ((lambda m: m.sum() > 20 and not m[:, :int(o["ac"][0]) - 1].any() and not m[:, int(o["ac"][0] + o["ac"][2]) + 2:].any())(np.abs(im - [240, 60, 10]).max(-1) < 40),
                                                                       int((np.abs(im - [240, 60, 10]).max(-1) < 40).sum())), ">20 px, inside the word"),
             ("everything else black on an empty frame (no third colour), >95% negative space", lambda o, im: (colours(im)[2] < 15 and (im.min(-1) > 245).mean() > .95, [colours(im), float((im.min(-1) > 245).mean())]), "no other colours")]
    return lcard(wd, "negspace", dict(body=body, css=css, js=js, W=W, H=H, shot=True), crits, dict(css="#hl{font:10px sans-serif}"))


@card("CAM-227")
def cam227(task, wd):
    """Rounded stage over an atmospheric gradient: full-frame brand gradient (bright top-left -> dark bottom-right), a
    near-black rounded stage ~80% x 75% slightly below centre, radius 48 px, soft shadow; all action inside the stage."""
    W, H = 640, 360
    body = '<div id=stage><div id=act></div></div>'
    css = ("#view{background:linear-gradient(135deg,#6a8cff 0%,#2a3c8f 55%,#0b1030 100%)}"
           "#stage{position:absolute;left:10%;top:15.5%;width:80%;height:75%;background:#0d0d10;border-radius:48px;box-shadow:0 30px 80px rgba(0,0,0,.6);overflow:hidden}"
           "#act{position:absolute;left:40%;top:40%;width:20%;height:20%;background:#fff}")
    js = "OUT({st:R('#stage'), act:R('#act'), sh:CS('#stage','box-shadow'), rad:CS('#stage','border-top-left-radius')})"
    crits = [("stage ~80% x 75%, centred horizontally, slightly below centre", lambda o, _: (near(o["st"][2], .8 * W) and near(o["st"][3], .75 * H) and abs(ctr(o["st"])[0] - W / 2) < 1 and 0 < ctr(o["st"])[1] - H / 2 < .06 * H,
                                                                                         [o["st"][2] / W, o["st"][3] / H, (ctr(o["st"])[1] - H / 2) / H]), [.8, .75, "0-6% below"]),
             ("radius 48 px: the stage corner shows the gradient, its inside is near-black", lambda o, im: (lum(im[int(o["st"][1]) + 3, int(o["st"][0]) + 3]) > 40 and lum(im[int(o["st"][1]) + 60, int(o["st"][0]) + 60]) < 20 and o["rad"] == "48px",
                                                                                                     [float(lum(im[int(o["st"][1]) + 3, int(o["st"][0]) + 3])), float(lum(im[int(o["st"][1]) + 60, int(o["st"][0]) + 60]))]), [">40", "<20"]),
             ("gradient bright top-left -> dark bottom-right", lambda o, im: (lum(im[3, 3]) > lum(im[H - 3, W - 3]) + 80, [float(lum(im[3, 3])), float(lum(im[H - 3, W - 3]))]), "TL >> BR"),
             ("soft shadow 0 30px 80px rgba(0,0,0,.6); the action stays inside the stage", lambda o, _: ("80px" in o["sh"] and o["act"][0] >= o["st"][0] and o["act"][0] + o["act"][2] <= o["st"][0] + o["st"][2], o["sh"]), "80px blur, inside")]
    return lcard(wd, "stage", dict(body=body, css=css, js=js, W=W, H=H, shot=True), crits, dict(css=css.replace("#stage{", "#stagex{")), )


def _dof_card(wd, name, blur_px, opacity, fn_desc):
    W, H = 480, 270
    body = '<div class="c back" id=b1></div><div class="c back" id=b2></div><div class="c front" id=f1></div>'
    css = (".c{position:absolute;width:150px;height:100px;border-radius:8px;background:repeating-linear-gradient(90deg,#000 0 3px,#fff 3px 9px)}"
           "#b1{left:20px;top:30px}#b2{left:310px;top:30px}#f1{left:165px;top:140px}.back{filter:blur(%dpx);opacity:%s}#view{background:#808080}" % (blur_px, opacity))
    js = "OUT({b1:R('#b1'), f1:R('#f1'), ob:CS('#b1','opacity'), fb:CS('#b1','filter'), ff:CS('#f1','filter')})"
    reg = lambda im, r: im[int(r[1]) + 20:int(r[1] + r[3]) - 20, int(r[0]) + 20:int(r[0] + r[2]) - 20]
    crits = [("back cards are blurred: their stripe detail drops below 20% of the sharp front card", lambda o, im: (hf(reg(im, o["b1"])) < .2 * hf(reg(im, o["f1"])), [hf(reg(im, o["b1"])), hf(reg(im, o["f1"]))]), "<0.2x"),
             ("computed blur(%dpx), opacity %s on the back cards; front card unfiltered" % (blur_px, opacity), lambda o, _: (o["fb"] == "blur(%dpx)" % blur_px and abs(float(o["ob"]) - float(opacity)) < 1e-6 and o["ff"] == "none", [o["fb"], o["ob"], o["ff"]]), ["blur", opacity, "none"]),
             ("back cards are faded toward the background (contrast scaled by the opacity)", lambda o, im: (abs(reg(im, o["b1"]).std() / reg(im, o["f1"]).std()) < float(opacity) + .05, float(reg(im, o["b1"]).std() / reg(im, o["f1"]).std())), "<= opacity")]
    return lcard(wd, name, dict(body=body, css=css, js=js, W=W, H=H, shot=True), crits, dict(css=css.replace(".back{", ".backx{"), shot=True))


@card("CAM-233")
def cam233(task, wd):
    """Depth-of-field cards: back cards opacity .3 and blur 4 px, the front card sharp (screenshot sharpness measured)."""
    return _dof_card(wd, "dofcards", 4, ".3", "")


@card("CAM-243")
def cam243(task, wd):
    """Depth-of-field UI: blur the inactive UI 6 px and keep the focus region sharp (screenshot sharpness measured)."""
    return _dof_card(wd, "dofui", 6, "1", "")


@card("CAM-240")
def cam240(task, wd):
    """Negative-space minimal canvas: one element on a flat warm grey with the soft shadow 0 8px 24px rgba(0,0,0,.08);
    the shadow is measured below vs above the element from the screenshot."""
    W, H = 480, 270
    body = '<div id=el></div>'
    css = "#view{background:#e9e5df}#el{position:absolute;left:190px;top:85px;width:100px;height:100px;border-radius:14px;background:#fff;box-shadow:0 8px 24px rgba(0,0,0,.08)}"
    js = "OUT({el:R('#el'), n:document.querySelectorAll('#view *').length})"
    bg = np.array([0xe9, 0xe5, 0xdf], float)
    below = lambda o, im: float(lum(bg) - lum(im[int(o["el"][1] + o["el"][3]) + 6, int(ctr(o["el"])[0])]))
    above = lambda o, im: float(lum(bg) - lum(im[int(o["el"][1]) - 6, int(ctr(o["el"])[0])]))
    crits = [("soft shadow: darker 6 px below than 6 px above (8 px offset), max 8% black", lambda o, im: (2 < below(o, im) < .08 * 255 and below(o, im) > above(o, im) + 1, [below(o, im), above(o, im)]), "below 2-20, > above"),
             ("flat warm grey canvas far from the element", lambda o, im: (float(np.abs(im[:30, :60] - bg).max()) < 2, float(np.abs(im[:30, :60] - bg).max())), "<2"),
             ("exactly one element", lambda o, _: (o["n"] == 1, o["n"]), 1)]
    return lcard(wd, "minimal", dict(body=body, css=css, js=js, W=W, H=H, shot=True), crits, dict(css=css.replace("box-shadow:0 8px 24px rgba(0,0,0,.08)", ""), shot=True))


@card("CAM-261")
def cam261(task, wd):
    """Symmetrical Wes-Anderson frame: every element centred on the vertical axis, props mirrored left/right, flat
    frontal perspective, ornamental medallion top centre, palette rose #c8909a / purple #402151 / gold #d4a645."""
    W, H = 480, 270
    props = '<div class="p l" style="left:60px"></div><div class="p r" style="right:60px"></div><div class="p l s" style="left:130px"></div><div class="p r s" style="right:130px"></div>'
    body = '<div id=med></div><div id=door></div>' + props + '<div id=floor></div>'
    css = ("#view{background:#c8909a}#med{position:absolute;left:50%;top:14px;width:46px;height:46px;margin-left:-23px;border-radius:50%;background:#d4a645;box-shadow:0 0 0 5px #402151}"
           "#door{position:absolute;left:50%;top:80px;width:90px;height:150px;margin-left:-45px;background:#402151;border-radius:45px 45px 0 0}"
           ".p{position:absolute;top:120px;width:40px;height:110px;background:#402151}.s{top:170px;width:30px;height:60px;background:#d4a645}"
           "#floor{position:absolute;left:0;right:0;top:230px;bottom:0;background:#402151}")
    js = "OUT({med:R('#med'), door:R('#door'), p:RA('.p')})"
    mirr = lambda im: float(np.abs(im - im[:, ::-1]).mean())
    pal = lambda im: float(np.min(np.stack([np.abs(im - c).max(-1) for c in ([200, 144, 154], [64, 33, 81], [212, 166, 69])]), 0).mean())
    crits = [("mirror symmetry: the frame equals its left-right flip", lambda o, im: (mirr(im) < 1.0, mirr(im)), "<1 (mean abs diff)"),
             ("medallion and door centred on the vertical axis, medallion at the top", lambda o, _: (abs(ctr(o["med"])[0] - W / 2) < .5 and abs(ctr(o["door"])[0] - W / 2) < .5 and o["med"][1] < 30, [ctr(o["med"]), ctr(o["door"])]), "x=240"),
             ("props mirrored in pairs", lambda o, _: (all(abs((a[0] + a[2] / 2) + (b[0] + b[2] / 2) - W) < .5 for a, b in zip(o["p"][0::2], o["p"][1::2])), o["p"]), "x_l + x_r = W"),
             ("palette rose / purple / gold only", lambda o, im: (pal(im) < 3, pal(im)), "<3")]
    naive_css = css.replace('right:60px', 'right:20px') + "#med{left:30%}"
    return lcard(wd, "wes", dict(body=body, css=css, js=js, W=W, H=H, shot=True), crits, dict(body=body.replace('style="right:60px"', 'style="right:20px"'), css=naive_css, shot=True))


@card("CAM-273")
def cam273(task, wd):
    """Vertical side label: an uppercase word rotated 90 degrees on the left edge, in accent blue, framing a card."""
    W, H = 480, 270
    body = '<div id=card></div><div id=lab>FEATURES</div>'
    css = ("#card{position:absolute;left:70px;top:30px;width:340px;height:210px;background:#fff;border-radius:10px}#view{background:#eceff3}"
           "#lab{position:absolute;left:46px;top:135px;transform:translate(-50%,-50%) rotate(-90deg);color:#1f5cff;font:800 16px/1 sans-serif;letter-spacing:4px;text-transform:uppercase;white-space:nowrap}")
    js = "OUT({card:R('#card'), lab:R('#lab'), col:CS('#lab','color'), tf:CS('#lab','text-transform'), q:__quad(document.getElementById('lab'))})"
    ang = lambda o: math.degrees(math.atan2(o["q"][1][1] - o["q"][0][1], o["q"][1][0] - o["q"][0][0]))
    crits = [("label rotated 90 degrees (reads bottom-to-top)", lambda o, _: (abs(ang(o) + 90) < .5, ang(o)), -90),
             ("on the left edge, vertically centred on the card, left of it", lambda o, _: (o["lab"][0] + o["lab"][2] <= o["card"][0] and o["lab"][3] > 3 * o["lab"][2] and abs(ctr(o["lab"])[1] - ctr(o["card"])[1]) < 1, o["lab"]), "tall, left of the card"),
             ("accent blue, uppercase", lambda o, _: (o["col"] == "rgb(31, 92, 255)" and o["tf"] == "uppercase", [o["col"], o["tf"]]), ["rgb(31, 92, 255)", "uppercase"])]
    return lcard(wd, "sidelabel", dict(body=body, css=css, js=js, W=W, H=H), crits, dict(css=css.replace("rotate(-90deg)", "")))


@card("CAM-279")
def cam279(task, wd):
    """Step label + caption: a mono '01 · UPLOAD' label and a bold caption placed under the UI."""
    W, H = 480, 270
    body = '<div id=ui></div><div id=lab>01 · UPLOAD</div><div id=cap>Drop your clip anywhere</div>'
    css = ("#ui{position:absolute;left:90px;top:20px;width:300px;height:170px;background:#fff;border-radius:10px}#view{background:#e8e8e8}"
           "#lab{position:absolute;left:90px;top:200px;font:11px ui-monospace,monospace;letter-spacing:1px;color:#666}#cap{position:absolute;left:90px;top:218px;font:700 20px sans-serif}")
    js = "OUT({ui:R('#ui'), lab:R('#lab'), cap:R('#cap'), txt:document.getElementById('lab').textContent, lf:CS('#lab','font-family'), cw:CS('#cap','font-weight')})"
    crits = [("label and caption sit under the UI, label above caption, left-aligned with it", lambda o, _: (o["lab"][1] >= o["ui"][1] + o["ui"][3] and o["cap"][1] >= o["lab"][1] + o["lab"][3] - .5 and near(o["lab"][0], o["ui"][0]) and near(o["cap"][0], o["ui"][0]),
                                                                                                 [o["ui"][1] + o["ui"][3], o["lab"][1], o["cap"][1]]), "ui < label < caption"),
             ("label is '<NN> · <WORD>' in a monospace face", lambda o, _: (bool(re.fullmatch(r"\d\d · [A-Z]+", o["txt"])) and "monospace" in o["lf"], [o["txt"], o["lf"]]), "01 · UPLOAD, mono"),
             ("caption bold (700)", lambda o, _: (o["cw"] == "700", o["cw"]), "700")]
    return lcard(wd, "steplabel", dict(body=body, css=css, js=js, W=W, H=H), crits, dict(css=css + "#lab{top:30px;left:100px}#cap{top:50px;left:100px}"))


@card("CAM-235")
def cam235(task, wd):
    """Editorial header: brand on the left, tagline on the right, a section label sitting over a full-width rule."""
    W, H = 480, 270
    body = '<header id=hd><b id=brand>KOSIF</b><span id=tag>motion, edited</span></header><div id=sec>03 — COLOUR</div><hr id=rule>'
    css = ("#hd{position:absolute;left:5%;right:5%;top:16px;display:flex;justify-content:space-between;align-items:baseline;font:12px sans-serif}#brand{font-size:16px}"
           "#sec{position:absolute;left:5%;top:52px;font:10px monospace;letter-spacing:1px}#rule{position:absolute;left:5%;right:5%;top:66px;margin:0;border:0;border-top:1px solid #111}")
    js = "OUT({brand:R('#brand'), tag:R('#tag'), sec:R('#sec'), rule:R('#rule')})"
    crits = [("brand flush left, tagline flush right on one row", lambda o, _: (near(o["brand"][0], .05 * W) and near(o["tag"][0] + o["tag"][2], .95 * W) and abs((o["brand"][1] + o["brand"][3]) - (o["tag"][1] + o["tag"][3])) < 4,
                                                                        [o["brand"][0], o["tag"][0] + o["tag"][2]]), [.05 * W, .95 * W]),
             ("section label directly over the rule", lambda o, _: (0 <= o["rule"][1] - (o["sec"][1] + o["sec"][3]) <= 4 and near(o["sec"][0], o["rule"][0]), [o["sec"][1] + o["sec"][3], o["rule"][1]]), "gap 0-4 px"),
             ("rule spans the header width", lambda o, _: (near(o["rule"][2], .9 * W), o["rule"][2]), .9 * W)]
    return lcard(wd, "edheader", dict(body=body, css=css, js=js, W=W, H=H), crits, dict(css=""))


NOTE_HZ = {"C2": 65.41, "G2": 98.0, "C3": 130.81, "E3": 164.81, "G3": 196.0, "C4": 261.63, "E4": 329.63, "A4": 440.0, "C5": 523.25, "E5": 659.25, "A5": 880.0, "C6": 1046.5}


@card("CAM-270")
def cam270(task, wd):
    """Instrument tier diagram: horizontal rails at 25 / 55 / 90% height, each a row of labelled bars with note names
    below, bar width proportional to 1/pitch, 9 px mono labels, colour per instrument family."""
    W, H = 640, 360
    tiers = [("strings", "#3a7bd5", ["C4", "E4", "A4", "C5"]), ("brass", "#e0a030", ["C3", "E3", "G3"]), ("bass", "#c0392b", ["C2", "G2"])]
    js = r"""
const TIERS=%s, HZ=%s, Y=[.25,.55,.90], K=%s; const v=document.getElementById('view');
TIERS.forEach(([fam,col,notes],ti)=>{ let x=20; notes.forEach(n=>{ const w=K/HZ[n]; const b=document.createElement('div'); b.className='bar '+fam;
  Object.assign(b.style,{position:'absolute',left:x+'px',top:(Y[ti]*%d-14)+'px',width:w+'px',height:'14px',background:col}); b.dataset.note=n; v.appendChild(b);
  const l=document.createElement('span'); l.className='lab'; l.textContent=n; Object.assign(l.style,{position:'absolute',left:x+'px',top:(Y[ti]*%d+2)+'px',font:'9px monospace'}); v.appendChild(l); x+=w+8; }); });
OUT({bars:[...document.querySelectorAll('.bar')].map(b=>[b.dataset.note,b.className.split(' ')[1],getComputedStyle(b).backgroundColor].concat(R('[data-note="'+b.dataset.note+'"]'))),
     labs:[...document.querySelectorAll('.lab')].map(l=>[l.textContent,getComputedStyle(l).fontSize,getComputedStyle(l).fontFamily].concat(R('.lab',null)?[]:[]))});"""
    mk = lambda k: js % (json.dumps(tiers), json.dumps(NOTE_HZ), k, H, H)
    spec = dict(js=mk(26000), W=W, H=H)
    naive = dict(js=mk(0).replace("const w=K/HZ[n];", "const w=40;"))

    def by(o):
        return {b[0]: b for b in o["bars"]}
    crits = [("bar width proportional to 1/pitch (w x f constant)", lambda o, _: (max(b[5] * NOTE_HZ[b[0]] for b in o["bars"]) / min(b[5] * NOTE_HZ[b[0]] for b in o["bars"]) < 1.001,
                                                                             [round(b[5] * NOTE_HZ[b[0]]) for b in o["bars"]]), "constant"),
             ("rails at 25 / 55 / 90% height", lambda o, _: (sorted({round((b[4] + b[6]) / H, 3) for b in o["bars"]}) == [.25, .55, .9], sorted({round((b[4] + b[6]) / H, 3) for b in o["bars"]})), [.25, .55, .9]),
             ("one colour per family", lambda o, _: (all(len({b[2] for b in o["bars"] if b[1] == f}) == 1 for f, _, _ in tiers) and len({b[2] for b in o["bars"]}) == 3, True), True),
             ("9 px mono note labels under every bar", lambda o, _: (len(o["labs"]) == len(o["bars"]) and all(l[1] == "9px" and "monospace" in l[2] for l in o["labs"]), len(o["labs"])), len(sum([t[2] for t in tiers], [])))]
    return lcard(wd, "tiers", spec, crits, naive)


@card("CAM-252")
def cam252(task, wd):
    """Evidence pair: two columns ('what people typed' with a red kicker dot, 'type this instead' with a green one),
    a prompt card above a reply card in each, paraphrased replies with a dashed border, verbatim ones solid, gap ~4% W."""
    W, H = 640, 360
    col = lambda k, dot, label, mode: ('<div class=col id=%s><div class=k><i style="background:%s"></i>%s</div><div class=pr>prompt</div>'
                                       '<div class="rp %s">reply</div></div>' % (k, dot, label, mode))
    body = '<div id=pair>' + col("bad", "#e5484d", "what people typed", "para") + col("good", "#30a46c", "type this instead", "verb") + "</div>"
    css = ("#pair{position:absolute;left:5%;right:5%;top:30px;display:grid;grid-template-columns:1fr 1fr;column-gap:4%}.k{font:11px sans-serif}"
           ".k i{display:inline-block;width:8px;height:8px;border-radius:50%;margin-inline-end:6px}.pr,.rp{margin-top:10px;height:90px;border-radius:8px;background:#fff}"
           ".para{border:2px dashed #999}.verb{border:2px solid #999}")
    js = ("OUT({cols:RA('.col'), pr:RA('.pr'), rp:RA('.rp'), dots:CSA('.k i','background-color'), bs:CSA('.rp','border-top-style'), pair:R('#pair')})")
    crits = [("two columns separated by ~4% of the width", lambda o, _: (len(o["cols"]) == 2 and abs((o["cols"][1][0] - o["cols"][0][0] - o["cols"][0][2]) / W - .04 * .9) < .002,
                                                                        (o["cols"][1][0] - o["cols"][0][0] - o["cols"][0][2]) / W if len(o["cols"]) == 2 else None), .036),
             ("prompt card above the reply card in each column", lambda o, _: (all(p[1] + p[3] <= r[1] for p, r in zip(o["pr"], o["rp"])), True), True),
             ("kicker dots red then green", lambda o, _: (o["dots"] == ["rgb(229, 72, 77)", "rgb(48, 164, 108)"], o["dots"]), ["red", "green"]),
             ("paraphrased reply dashed, verbatim solid", lambda o, _: (o["bs"] == ["dashed", "solid"], o["bs"]), ["dashed", "solid"])]
    return lcard(wd, "evidence", dict(body=body, css=css, js=js, W=W, H=H), crits, dict(css=""))


def tcard(wd, name, body, css, anim, sels, T, crits, naive_anim="", extra="null", W=480, H=270, scripts=(GSAP,), more="", shot=False):
    """A timeline layout card: `anim` builds the GSAP timeline `tl` (or defines camAt(t)); every selector's quad, opacity
    and blur are sampled by Chrome at the times T (plus `extra(t)`); the input run uses `naive_anim`."""
    js = "var tl=gsap.timeline({paused:true}); %s; const T=%s; OUT({fr:SAMPLE(T,%s,%s)%s})"
    spec = dict(body=body, css=css, js=js % (anim, json.dumps(T), json.dumps(sels), extra, more), W=W, H=H, scripts=list(scripts), shot=shot)
    naive = dict(js=js % (naive_anim, json.dumps(T), json.dumps(sels), extra, more))
    return lcard(wd, name, spec, crits, naive)


qc = lambda f, k: tuple(np.array(f["el"][k]["q"]).mean(0))
qx = lambda o, k: [qc(f, k)[0] for f in o["fr"]]
qy = lambda o, k: [qc(f, k)[1] for f in o["fr"]]
qo = lambda o, k: [f["el"][k]["o"] for f in o["fr"]]
qb = lambda o, k: [f["el"][k]["b"] for f in o["fr"]]
qang = lambda f, k: math.degrees(math.atan2(f["el"][k]["q"][1][1] - f["el"][k]["q"][0][1], f["el"][k]["q"][1][0] - f["el"][k]["q"][0][0]))
rgbl = lambda s: (lambda v: .2126 * v[0] + .7152 * v[1] + .0722 * v[2])([float(x) for x in re.findall(r"[\d.]+", s)[:3]])
tgrid = lambda d, fps: [round(i / fps, 4) for i in range(int(round(d * fps)) + 1)]


@card("CAM-207")
def cam207(task, wd):
    """Numbered step tab bar '01 Read · 02 Tap · 03 Listen · 04 Speak': the active tab inverts (dark fill, light text) in
    200 ms as each section starts; computed colours sampled per frame."""
    tabs = ["01 Read", "02 Tap", "03 Listen", "04 Speak"]
    body = '<div id=bar>' + "".join('<span class=tab id=t%d>%s</span>' % (i, t) for i, t in enumerate(tabs)) + '</div>'
    css = ("#bar{position:absolute;left:50%;top:20px;transform:translateX(-50%);display:flex;gap:6px;font:11px monospace}"
           ".tab{border:1px solid #111;border-radius:99px;padding:3px 9px;background:rgb(245,245,245);color:rgb(17,17,17)}")
    anim = "".join("tl.to('#t%d',{backgroundColor:'rgb(17,17,17)',color:'rgb(245,245,245)',duration:.2,ease:'none'},%d);" % (i, i) +
                   ("tl.to('#t%d',{backgroundColor:'rgb(245,245,245)',color:'rgb(17,17,17)',duration:.2,ease:'none'},%d);" % (i - 1, i) if i else "") for i in range(4))
    T = tgrid(4, 20)
    extra = "t=>[...document.querySelectorAll('.tab')].map(e=>[getComputedStyle(e).backgroundColor,getComputedStyle(e).color])"
    more = ", txt:[...document.querySelectorAll('.tab')].map(e=>e.textContent)"
    act = lambda o, t: [i for i, (bg, fg) in enumerate(o["fr"][T.index(t)]["x"]) if rgbl(bg) < 60 and rgbl(fg) > 200]
    crits = [("exactly the current section's tab is inverted", lambda o, _: ([act(o, t) for t in (0.5, 1.5, 2.5, 3.5)] == [[0], [1], [2], [3]], [act(o, t) for t in (0.5, 1.5, 2.5, 3.5)]), [[0], [1], [2], [3]]),
             ("the inversion takes 200 ms (half-way at +100 ms)", lambda o, _: (abs(rgbl(o["fr"][T.index(2.1)]["x"][2][0]) - (245 + 17) / 2) < 3 and rgbl(o["fr"][T.index(2.2)]["x"][2][0]) < 18,
                                                                        [rgbl(o["fr"][T.index(2.1)]["x"][2][0]), rgbl(o["fr"][T.index(2.2)]["x"][2][0])]), [131, 17]),
             ("numbered mono pills", lambda o, _: (o["txt"] == tabs, o["txt"]), tabs)]
    return tcard(wd, "tabbar", body, css, anim, ["#t0"], T, crits, extra=extra, more=more)


@card("CAM-213")
def cam213(task, wd):
    """Bottom nav progress: the section names in a bottom nav, the current chapter's name highlighted as chapters play."""
    names = ["Intro", "Cut", "Colour", "Export"]
    body = '<nav id=nav>' + "".join('<span class=n id=n%d>%s</span>' % (i, t) for i, t in enumerate(names)) + '</nav>'
    css = "#nav{position:absolute;left:0;right:0;bottom:10px;display:flex;justify-content:center;gap:18px;font:12px sans-serif}.n{color:rgb(150,150,150)}"
    anim = "".join("tl.set('#n%d',{color:'rgb(255,80,0)'},%s);" % (i, 1.5 * i) + ("tl.set('#n%d',{color:'rgb(150,150,150)'},%s);" % (i - 1, 1.5 * i) if i else "") for i in range(4))
    T = tgrid(6, 10)
    extra = "t=>[...document.querySelectorAll('.n')].map(e=>getComputedStyle(e).color)"
    hi = lambda o, t: [names[i] for i, c in enumerate(o["fr"][T.index(t)]["x"]) if c == "rgb(255, 80, 0)"]
    crits = [("the highlighted name follows the chapter", lambda o, _: ([hi(o, t) for t in (0.7, 2.2, 3.7, 5.2)] == [[n] for n in names], [hi(o, t) for t in (0.7, 2.2, 3.7, 5.2)]), [[n] for n in names]),
             ("nav sits at the bottom of the frame", lambda o, _: (qc(o["fr"][0], 0)[1] > 0.85 * 270, qc(o["fr"][0], 0)[1]), ">229")]
    return tcard(wd, "bottomnav", body, css, anim, ["#nav"], T, crits, extra=extra)


@card("CAM-246")
def cam246(task, wd):
    """Segment progress dashes: 6 dashes 28x3 px in the header; past ones grey, the current one fills with the accent
    colour as its segment plays (fill width sampled per frame)."""
    body = '<div id=d>' + "".join('<i class=dash id=d%d><b></b></i>' % i for i in range(6)) + '</div>'
    css = ("#d{position:absolute;left:20px;top:14px;display:flex;gap:6px}.dash{display:block;position:relative;width:28px;height:3px;background:rgb(220,220,220)}"
           ".dash b{position:absolute;left:0;top:0;height:3px;width:0;background:rgb(255,60,0)}")
    anim = "".join("tl.to('#d%d b',{width:28,duration:1,ease:'none'},%d); tl.set('#d%d b',{backgroundColor:'rgb(140,140,140)'},%d);" % (i, i, i, i + 1) for i in range(6))
    T = tgrid(6, 10)
    extra = "t=>[...document.querySelectorAll('.dash b')].map(e=>[e.getBoundingClientRect().width,getComputedStyle(e).backgroundColor])"
    more = ", dims:RA('.dash')"
    st = lambda o, t: o["fr"][T.index(t)]["x"]
    crits = [("the current dash fills linearly over its segment (14 px at mid-segment)", lambda o, _: (all(abs(st(o, k + .5)[k][0] - 14) < .01 for k in range(6)), [st(o, k + .5)[k][0] for k in range(6)]), 14),
             ("past dashes full and grey, future dashes empty", lambda o, _: (all(st(o, 3.5)[k] == [28, "rgb(140, 140, 140)"] for k in range(3)) and all(st(o, 3.5)[k][0] == 0 for k in (4, 5)) and st(o, 3.5)[3][1] == "rgb(255, 60, 0)",
                                                                      st(o, 3.5)), "grey x3, accent, empty x2"),
             ("6 dashes of 28 x 3 px", lambda o, _: (len(o["dims"]) == 6 and all(round(d[2]) == 28 and round(d[3]) == 3 for d in o["dims"]), o["dims"][:1]), [28, 3])]
    return tcard(wd, "dashes", body, css, anim, ["#d0"], T, crits, extra=extra, more=more)


@card("CAM-276")
def cam276(task, wd):
    """Pill tab bar as chapter navigator: a persistent top pill nav whose dark active pill slides to the next tab in 300 ms
    ease-in-out while the scene content swaps with a blurred crossfade."""
    body = ('<div id=nav><span class=t>One</span><span class=t>Two</span><span class=t>Three</span><i id=pill></i></div>'
            '<div id=sa class=sc>A</div><div id=sb class=sc style="opacity:0">B</div>')
    css = ("#nav{position:absolute;left:120px;top:12px;width:240px;height:26px;border-radius:99px;background:#eee;display:flex}.t{flex:1;text-align:center;font:11px/26px sans-serif;position:relative;z-index:1}"
           "#pill{position:absolute;left:0;top:0;width:80px;height:26px;border-radius:99px;background:#111}.sc{position:absolute;left:60px;top:60px;width:360px;height:180px;background:#fff;font:40px sans-serif}")
    anim = ("tl.to('#pill',{x:80,duration:.3,ease:'power2.inOut'},1.0);"
            "tl.to('#sa',{opacity:0,filter:'blur(8px)',duration:.3,ease:'none'},1.0); tl.fromTo('#sb',{opacity:0,filter:'blur(8px)'},{opacity:1,filter:'blur(0px)',duration:.3,ease:'none',immediateRender:false},1.0)")
    T = tgrid(2, 20)
    model = [120 + 40 + 80 * cubic_io(min(1, max(0, (t - 1) / .3))) for t in T]
    crits = [("active pill slides one tab in 300 ms, ease-in-out (cubic)", lambda o, _: (maxerr(qx(o, 0), model) < .05, [round(v, 2) for v in qx(o, 0)[18:28]]), [round(v, 2) for v in model[18:28]]),
             ("blurred crossfade: at mid-swap both scenes are half visible and blurred", lambda o, _: (abs(qo(o, 1)[T.index(1.15)] - .5) < .01 and abs(qo(o, 2)[T.index(1.15)] - .5) < .01 and qb(o, 1)[T.index(1.15)] > 3 and qb(o, 2)[T.index(1.15)] > 3,
                                                                                            [qo(o, 1)[T.index(1.15)], qo(o, 2)[T.index(1.15)], qb(o, 1)[T.index(1.15)], qb(o, 2)[T.index(1.15)]]), [.5, .5, ">3", ">3"]),
             ("the nav persists (same place, fully visible) through the swap", lambda o, _: (max(qy(o, 3)) - min(qy(o, 3)) < 1e-6 and min(qo(o, 3)) == 1, [min(qo(o, 3))]), 1)]
    return tcard(wd, "pillnav", body, css, anim, ["#pill", "#sa", "#sb", "#nav"], T, crits)


@card("CAM-237")
def cam237(task, wd):
    """Numbered chapter header: top-left at 5% margin, tiny grey mono index ('04', 1.5% h) + bold 700 title (4% h) in
    #111113 on #f2f2f2; fades/blurs in over 300 ms at chapter start and blurs out at the end."""
    W, H = 640, 360
    body = '<div id=hd><div id=ix>04</div><div id=tt>Colour</div></div>'
    css = ("#view{background:#f2f2f2}#hd{position:absolute;left:5%;top:5%;color:#111113}#ix{font:5.4px/1 monospace;color:#8a8a8a;height:5.4px}"
           "#tt{font:700 14.4px/1 sans-serif;height:14.4px}")
    anim = ("tl.fromTo('#hd',{opacity:0,filter:'blur(10px)'},{opacity:1,filter:'blur(0px)',duration:.3,ease:'none',immediateRender:false},0.5);"
            "tl.to('#hd',{opacity:0,filter:'blur(10px)',duration:.3,ease:'none'},2.7); gsap.set('#hd',{opacity:0,filter:'blur(10px)'})")
    T = tgrid(3.2, 20)
    more = ", ix:R('#ix'), tt:R('#tt'), ixc:CS('#ix','color'), ttc:CS('#hd','color'), tw:CS('#tt','font-weight'), ixf:CS('#ix','font-family')"
    model = [min(1, max(0, (t - .5) / .3)) if t < 2.7 else max(0, 1 - (t - 2.7) / .3) for t in T]
    crits = [("fades in over 300 ms at the chapter start and out at its end", lambda o, _: (maxerr(qo(o, 0), model) < 1e-3, [qo(o, 0)[i] for i in (10, 13, 16, 55, 57, 60)]), [model[i] for i in (10, 13, 16, 55, 57, 60)]),
             ("blur clears with the fade (10 px -> 0)", lambda o, _: (qb(o, 0)[T.index(0.5)] == 10 and qb(o, 0)[T.index(1.0)] == 0 and abs(qb(o, 0)[T.index(2.85)] - 5) < .01, [qb(o, 0)[T.index(t)] for t in (.5, 1.0, 2.85)]), [10, 0, 5]),
             ("top-left at the 5% margin; index 1.5% h, title 4% h", lambda o, _: (near(o["fr"][20]["el"][0]["q"][0][0], 32) and near(o["fr"][20]["el"][0]["q"][0][1], 18) and near(o["ix"][3], .015 * H, .3) and near(o["tt"][3], .04 * H, .3),
                                                                         [o["fr"][20]["el"][0]["q"][0], o["ix"][3], o["tt"][3]]), [[32, 18], 5.4, 14.4]),
             ("grey mono index, bold #111113 title", lambda o, _: (o["ixc"] == "rgb(138, 138, 138)" and "monospace" in o["ixf"] and o["ttc"] == "rgb(17, 17, 19)" and o["tw"] == "700", [o["ixc"], o["ttc"], o["tw"]]), "grey, #111113, 700")]
    return tcard(wd, "chapterhead", body, css, anim, ["#hd"], T, crits, W=W, H=H, more=more)


@card("CAM-259")
def cam259(task, wd):
    """Index + model lower-third: a thin violet rule under the hero word, a pixel-mono index number (01-04) in violet at
    2x the label size and the model identifier in typewriter mono beside it; the block slides in over 250 ms."""
    body = '<div id=lt><div id=hero>Seedance</div><i id=rule></i><span id=ix>02</span><span id=mid>model: seedance-2.0</span></div>'
    css = ("#lt{position:absolute;left:40px;top:180px}#hero{font:700 28px/1 sans-serif}#rule{display:block;height:2px;width:120px;background:#7b5cff;margin:4px 0}"
           "#ix{font:20px/1 monospace;color:#7b5cff;margin-right:8px}#mid{font:10px/1 'Courier New',monospace}")
    anim = "gsap.set('#lt',{x:-60,opacity:0}); tl.to('#lt',{x:0,opacity:1,duration:.25,ease:'power2.out'},0.5)"
    T = tgrid(1, 50)
    p2o = lambda x: 1 - (1 - x) ** 3
    model = [40 - 60 * (1 - p2o(min(1, max(0, (t - .5) / .25)))) for t in T]
    more = ", hero:R('#hero'), rule:R('#rule'), ix:R('#ix'), mid:R('#mid'), rc:CS('#rule','background-color'), ic:CS('#ix','color'), fi:CS('#ix','font-size'), fm:CS('#mid','font-size'), ff:CS('#mid','font-family')"
    lx = lambda o: [f["el"][0]["q"][0][0] for f in o["fr"]]
    crits = [("slides in over 250 ms (power2.out) from -60 px", lambda o, _: (maxerr(lx(o), model) < .05, [round(v, 2) for v in lx(o)[24:40:3]]), [round(v, 2) for v in model[24:40:3]]),
             ("thin violet rule directly under the hero word", lambda o, _: (o["rc"] == "rgb(123, 92, 255)" and 0 <= o["rule"][1] - (o["hero"][1] + o["hero"][3]) <= 6 and o["rule"][3] <= 3, [o["rc"], o["rule"]]), "violet, 2 px, under"),
             ("violet index at 2x the label size, model id in typewriter mono beside it", lambda o, _: ((o["ic"] == "rgb(123, 92, 255)" and float(o["fi"][:-2]) / float(o["fm"][:-2]) == 2 and "Courier" in o["ff"] and o["mid"][0] > o["ix"][0] + o["ix"][2]),
                                                                                                  [o["fi"], o["fm"], o["ff"]]), ["20px", "10px", "Courier"])]
    return tcard(wd, "indexlt", body, css, anim, ["#lt"], T, crits, more=more)


@card("CAM-267")
def cam267(task, wd):
    """Headline over product window: a short lowercase line at top centre ('as a demo.'), a browser window sliding up
    below it in 400 ms easeOutQuint, and a cursor performing one action (move to the button, one click)."""
    body = '<div id=hl>as a demo.</div><div id=win><b id=btn></b></div><i id=cur></i>'
    css = ("#hl{position:absolute;left:50%;top:20px;transform:translateX(-50%);font:700 22px sans-serif;white-space:nowrap}"
           "#win{position:absolute;left:90px;top:70px;width:300px;height:180px;background:#fff;border-radius:10px;box-shadow:0 10px 30px rgba(0,0,0,.2)}"
           "#btn{position:absolute;left:200px;top:130px;width:70px;height:24px;background:#2b6cff;border-radius:6px}"
           "#cur{position:absolute;left:400px;top:240px;width:10px;height:14px;background:#000;clip-path:polygon(0 0,100% 70%,40% 70%,0 100%)}")
    anim = ("gsap.set('#win',{y:200}); tl.to('#win',{y:0,duration:.4,ease:'power4.out'},.3);"
            "tl.to('#cur',{left:325,top:212,duration:.6,ease:'power2.inOut'},.9); tl.to('#cur',{scale:.8,duration:.08,yoyo:true,repeat:1,ease:'none'},1.55)")
    T = tgrid(2, 50)
    q = lambda x: 1 - (1 - x) ** 5
    model = [70 + 90 + 200 * (1 - q(min(1, max(0, (t - .3) / .4)))) for t in T]
    more = ", btn:R('#btn'), hl:R('#hl'), txt:document.getElementById('hl').textContent"
    sc = lambda o: [math.dist(f["el"][1]["q"][0], f["el"][1]["q"][1]) / 10 for f in o["fr"]]
    crits = [("window slides up in 400 ms on easeOutQuint", lambda o, _: (maxerr(qy(o, 0), model) < .05, [round(v, 2) for v in qy(o, 0)[15:36:4]]), [round(v, 2) for v in model[15:36:4]]),
             ("cursor ends over the button and clicks exactly once", lambda o, _: ((lambda c, b: b[0] <= c[0] <= b[0] + b[2] and b[1] <= c[1] <= b[1] + b[3])(qc(o["fr"][-1], 1), o["btn"])
                                                                          and sum(1 for a, b in zip(sc(o), sc(o)[1:]) if a >= .999 and b < .999) == 1, [qc(o["fr"][-1], 1), min(sc(o))]), "inside, 1 click"),
             ("short lowercase headline at top centre", lambda o, _: (o["txt"] == o["txt"].lower() and len(o["txt"].split()) <= 4 and abs(ctr(o["hl"])[0] - 240) < 1 and o["hl"][1] < 40, [o["txt"], ctr(o["hl"])]), "lowercase, centred")]
    return tcard(wd, "productwin", body, css, anim, ["#win", "#cur"], T, crits, more=more)


@card("CAM-268")
def cam268(task, wd):
    """Persistent corner chrome: a tracked uppercase kicker top-left (~1.5% h), a line icon top-right and the brand logo
    bubble bottom-left (7% h) kept fixed across every cut while the scenes swap underneath."""
    W, H = 640, 360
    scenes = "".join('<div class=sc id=s%d style="background:%s;opacity:%d">%d</div>' % (i, c, 1 if i == 0 else 0, i) for i, c in enumerate(["#c33", "#3c3", "#33c", "#cc3"]))
    chrome = '<div id=kick>FEATURE</div><i id=icon></i><b id=logo></b>'
    body = scenes + chrome
    css = (".sc{position:absolute;inset:0}#kick{position:absolute;left:20px;top:16px;font:5.4px/1 sans-serif;letter-spacing:2px;text-transform:uppercase;color:#fff;height:5.4px}"
           "#icon{position:absolute;right:20px;top:14px;width:14px;height:14px;border:1.5px solid #fff;border-radius:3px}"
           "#logo{position:absolute;left:20px;bottom:16px;width:25.2px;height:25.2px;border-radius:50%;background:#fff}")
    cuts = "".join("tl.set('#s%d',{opacity:0},%d); tl.set('#s%d',{opacity:1},%d);" % (i - 1, i, i, i) for i in range(1, 4))
    T = tgrid(4, 10)
    sels = ["#kick", "#icon", "#logo"] + ["#s%d" % i for i in range(4)]
    vis = lambda o, t: [i for i in range(4) if o["fr"][T.index(t)]["el"][3 + i]["o"] == 1]
    naive_body = scenes.replace('>0</div>', '>0' + chrome + '</div>')
    crits = [("chrome identical and fully visible on every frame across the cuts", lambda o, _: (all(f["el"][k]["q"] == o["fr"][0]["el"][k]["q"] and f["el"][k]["o"] == 1 for f in o["fr"] for k in range(3)),
                                                                                             [o["fr"][-1]["el"][k]["o"] for k in range(3)]), [1, 1, 1]),
             ("the scenes really cut underneath (one per second)", lambda o, _: ([vis(o, t) for t in (.5, 1.5, 2.5, 3.5)] == [[0], [1], [2], [3]], [vis(o, t) for t in (.5, 1.5, 2.5, 3.5)]), [[0], [1], [2], [3]]),
             ("kicker top-left ~1.5% h, icon top-right, logo bottom-left 7% h", lambda o, _: ((lambda q0, q1, q2: q0[0][0] < 40 and q0[0][1] < 30 and abs((q0[3][1] - q0[0][1]) / H - .015) < .002
                                                                                            and q1[1][0] > W - 40 and q1[0][1] < 30 and q2[0][0] < 40 and q2[3][1] > H - 40 and abs((q2[3][1] - q2[0][1]) / H - .07) < .002)
                                                                                           (*[o["fr"][0]["el"][k]["q"] for k in range(3)]), [o["fr"][0]["el"][k]["q"][0] for k in range(3)]), "corners")]
    spec = dict(body=body, css=css, js="var tl=gsap.timeline({paused:true}); %s; OUT({fr:SAMPLE(%s,%s,null)})" % (cuts, json.dumps(T), json.dumps(sels)), W=W, H=H, scripts=[GSAP])
    return lcard(wd, "chrome", spec, crits, dict(body=naive_body))


@card("CAM-272")
def cam272(task, wd):
    """Triptych category panels: 3 equal vertical colour panels (blue / black / yellow) slide up staggered 120 ms, each
    with an icon and a serif label."""
    cols = ["rgb(31, 92, 255)", "rgb(17, 17, 17)", "rgb(255, 204, 0)"]
    body = "".join('<div class=p id=p%d style="left:%s%%;background:%s"><i class=ic></i><span class=lb>%s</span></div>' % (i, 100 * i / 3, c, n)
                   for i, (c, n) in enumerate(zip(cols, ["Film", "Type", "Sound"])))
    css = (".p{position:absolute;top:0;width:calc(100% / 3);height:100%}.ic{position:absolute;left:50%;top:40%;width:20px;height:20px;margin-left:-10px;border:2px solid #fff;border-radius:50%}"
           ".lb{position:absolute;left:0;right:0;top:55%;text-align:center;font:20px Georgia,serif;color:#fff}")
    anim = "gsap.set('.p',{y:270}); tl.to('.p',{y:0,duration:.5,ease:'power3.out',stagger:.12},.2)"
    T = tgrid(1.2, 100)
    more = ", w:RA('.p').map(r=>r[2]), bg:CSA('.p','background-color'), lf:CSA('.lb','font-family'), ic:RA('.ic').length"

    def half(o, k):
        ys = qy(o, k)
        return next(T[i] for i, y in enumerate(ys) if y <= 135 + 135)
    crits = [("panels slide up staggered by 120 ms", lambda o, _: (all(abs((half(o, k) - half(o, 0)) - .12 * k) < .011 for k in (1, 2)), [round(half(o, k) - half(o, 0), 3) for k in (1, 2)]), [.12, .24]),
             ("3 equal vertical panels filling the frame", lambda o, _: (all(abs(w - 160) < .05 for w in o["w"]), o["w"]), [160, 160, 160]),
             ("blue / black / yellow with an icon and a serif label each", lambda o, _: (o["bg"] == cols and o["ic"] == 3 and all("serif" in f for f in o["lf"]), [o["bg"], o["lf"][0]]), cols)]
    return tcard(wd, "triptych", body, css, anim, ["#p0", "#p1", "#p2"], T, crits, more=more)


@card("CAM-244")
def cam244(task, wd):
    """Bento feature cards: white rounded cards on light grey with a 16 px gap, each with a title and a mini demo, rising
    in with a stagger."""
    W, H = 640, 360
    body = '<div id=g>' + "".join('<div class=c id=c%d><b>Feature %d</b><i class=demo></i></div>' % (i, i + 1) for i in range(6)) + '</div>'
    css = ("#view{background:#ececec}#g{position:absolute;left:40px;top:40px;right:40px;bottom:40px;display:grid;grid-template-columns:2fr 1fr 1fr;grid-template-rows:1fr 1fr;gap:16px}"
           ".c{background:#fff;border-radius:16px;font:12px sans-serif;padding:10px;position:relative}.demo{position:absolute;left:10px;bottom:10px;width:30px;height:8px;background:#2b6cff;border-radius:4px}"
           "#c0{grid-row:span 2}")
    anim = "gsap.set('.c',{y:30,opacity:0}); tl.to('.c',{y:0,opacity:1,duration:.4,ease:'power2.out',stagger:.08},.1)"
    T = tgrid(1.2, 100)
    more = ", rects:RA('.c'), bg:CSA('.c','background-color'), rad:CSA('.c','border-top-left-radius'), demos:RA('.demo').length"

    def gaps(rs):
        g = []
        for a in rs:
            for b in rs:
                if abs(a[1] - b[1]) < .5 and b[0] > a[0] + a[2] - .5:
                    g.append(b[0] - a[0] - a[2])
                if abs(a[0] - b[0]) < .5 and b[1] > a[1] + a[3] - .5:
                    g.append(b[1] - a[1] - a[3])
        return sorted(set(round(x, 3) for x in g))
    onset = lambda o, k: next(T[i] for i, v in enumerate(qo(o, k)) if v > 0)
    crits = [("staggered rise: each card starts 80 ms after the previous", lambda o, _: (all(abs(onset(o, k) - onset(o, 0) - .08 * k) < .011 for k in range(1, 6)), [round(onset(o, k) - onset(o, 0), 2) for k in range(6)]), [.08 * k for k in range(6)]),
             ("16 px gaps between neighbouring cards", lambda o, _: (16.0 in gaps(o["rects"]) and min(gaps(o["rects"])) == 16.0, gaps(o["rects"])[:4]), 16),
             ("white rounded cards with a title and a mini demo each", lambda o, _: (set(o["bg"]) == {"rgb(255, 255, 255)"} and set(o["rad"]) == {"16px"} and o["demos"] == 6, [o["bg"][0], o["rad"][0]]), ["white", "16px"])]
    return tcard(wd, "bento", body, css, anim, ["#c%d" % i for i in range(6)], T, crits, W=W, H=H, more=more)


SPRING_JS = r"""
function spring(k,c,t){ if(t<=0) return 1; const w=Math.sqrt(k), z=c/(2*w);           // displacement left of a unit step (mass 1)
  if(z<1){ const wd=w*Math.sqrt(1-z*z); return Math.exp(-z*w*t)*(Math.cos(wd*t)+z*w/wd*Math.sin(wd*t)); }
  return Math.exp(-w*t)*(1+w*t); }
"""


def py_spring_rk4(k, c, t, dt=1e-4):
    """Independent model: integrate x'' = -k x - c x' (mass 1, x0 = 1, v0 = 0) with RK4."""
    x, v = 1.0, 0.0
    n = int(round(t / dt))
    f = lambda x, v: (v, -k * x - c * v)
    for _ in range(max(0, n)):
        a1, b1 = f(x, v)
        a2, b2 = f(x + a1 * dt / 2, v + b1 * dt / 2)
        a3, b3 = f(x + a2 * dt / 2, v + b2 * dt / 2)
        a4, b4 = f(x + a3 * dt, v + b3 * dt)
        x += dt / 6 * (a1 + 2 * a2 + 2 * a3 + a4)
        v += dt / 6 * (b1 + 2 * b2 + 2 * b3 + b4)
    return x


@card("CAM-224")
def cam224(task, wd):
    """Bento grid assembly: feature tiles of varied sizes and colours spring into a 4x3 grid (stiffness 180, damping 14,
    80 ms stagger), each tile a mini feature label; spring displacement measured against an RK4 model."""
    W, H = 640, 360
    spans = [(2, 1), (1, 1), (1, 2), (1, 1), (1, 1), (2, 1), (1, 1), (1, 1), (1, 1)]
    cols = ["#e85d75", "#5d9be8", "#f2c14e", "#6cc58e", "#9b6ce8", "#e8955d", "#4ec2c2", "#c2c24e", "#888"]
    body = '<div id=g>' + "".join('<div class=t id=t%d style="grid-column:span %d;grid-row:span %d;background:%s">F%d</div>' % (i, a, b, c, i)
                                  for i, ((a, b), c) in enumerate(zip(spans, cols))) + '</div>'
    css = "#g{position:absolute;left:40px;top:30px;width:560px;height:300px;display:grid;grid-template-columns:repeat(4,1fr);grid-template-rows:repeat(3,1fr);gap:8px}.t{font:10px sans-serif;border-radius:8px}"
    anim = (SPRING_JS + "const off=[...Array(9).keys()].map(i=>[((i*97)%%7-3)*60,((i*53)%%5-2)*70]);"
            "window.camAt=function(t){ document.querySelectorAll('.t').forEach((e,i)=>{ const s=%s; e.style.transform='translate('+off[i][0]*s+'px,'+off[i][1]*s+'px)'; }); }")
    T = tgrid(1.6, 50)
    more = ", cells:[...document.querySelectorAll('.t')].map(e=>{const s=e.style.transform; e.style.transform='none'; const r=e.getBoundingClientRect(); e.style.transform=s; return [r.left,r.top,r.width,r.height];})"
    off = [(((i * 97) % 7 - 3) * 60, ((i * 53) % 5 - 2) * 70) for i in range(9)]
    k = 1                                              # a tile with a non-zero x offset (180 px), delayed 80 ms

    def disp(o, i):
        x0 = o["cells"][i][0] + o["cells"][i][2] / 2
        return [(qx(o, i)[j] - x0) / off[i][0] for j in range(len(T))]
    model = [py_spring_rk4(180, 14, t - .08 * k) if t > .08 * k else 1.0 for t in T]
    crits = [("tile displacement follows the spring k=180, c=14 (RK4 model), started 80 ms x index", lambda o, _: (maxerr(disp(o, k), model) < 2e-3, [round(v, 3) for v in disp(o, k)[::8]]), [round(v, 3) for v in model[::8]]),
             ("underdamped: one overshoot past the slot", lambda o, _: (min(disp(o, k)) < -0.05, min(disp(o, k))), "<-0.05"),
             ("settles exactly into a 4x3 grid with varied tile sizes", lambda o, _: (all(abs(v) < 2e-3 * abs(off[i][0]) + .01 for i in range(9) for v in [qx(o, i)[-1] - (o["cells"][i][0] + o["cells"][i][2] / 2)])
                                                                                and len({round(c[2]) for c in o["cells"]}) >= 2 and len({round(c[3]) for c in o["cells"]}) >= 2, [[round(v) for v in c] for c in o["cells"][:3]]), "4 cols x 3 rows")]
    return tcard(wd, "bentosprings", body, css, anim % ("spring(180,14,t-0.08*i)",), ["#t%d" % i for i in range(9)], T, crits, naive_anim=anim % ("1",), W=W, H=H, more=more)


@card("CAM-241")
def cam241(task, wd):
    """Scatter-to-grid card settle: cards start at random positions with +/-8-12 degree rotation and spring (stiffness
    ~120, damping ~16, 80 ms stagger) into an aligned row while a search pill appears above and branches connect to each."""
    W, H = 640, 360
    n = 5
    body = ('<div id=pill>search</div><svg id=br width=640 height=360 style="position:absolute;left:0;top:0">' +
            "".join('<line id=l%d stroke="#555" stroke-width="1.5"/>' % i for i in range(n)) + '</svg>' +
            "".join('<div class=cd id=c%d style="left:%dpx"></div>' % (i, 70 + i * 104) for i in range(n)))
    css = ("#pill{position:absolute;left:250px;top:70px;width:140px;height:28px;border-radius:99px;background:#111;color:#fff;font:12px/28px sans-serif;text-align:center}"
           ".cd{position:absolute;top:200px;width:84px;height:60px;background:#fff;border:1px solid #ccc;border-radius:8px}")
    rng = np.random.default_rng(3)
    start = [(float(rng.uniform(-200, 200)), float(rng.uniform(-150, 100)), float(rng.choice([-1, 1]) * rng.uniform(8, 12))) for _ in range(n)]
    anim = (SPRING_JS + "const S=%s;" % json.dumps(start) +
            "window.camAt=function(t){ document.querySelectorAll('.cd').forEach((e,i)=>{ const s=%s; e.style.transform='translate('+S[i][0]*s+'px,'+S[i][1]*s+'px) rotate('+S[i][2]*s+'deg)'; });"
            "const p=Math.min(1,Math.max(0,(t-0.2)/0.3)); document.getElementById('pill').style.opacity=%s;"
            "const L=Math.min(1,Math.max(0,(t-1.2)/0.4)); document.querySelectorAll('.cd').forEach((e,i)=>{ const l=document.getElementById('l'+i); const r=e.getBoundingClientRect();"
            "l.setAttribute('x1',320); l.setAttribute('y1',98); l.setAttribute('x2',320+(r.left+r.width/2-320)*L); l.setAttribute('y2',98+(r.top-98)*L); }); }")
    T = tgrid(2.0, 25)
    more = ""
    extra = "t=>[...document.querySelectorAll('line')].map(l=>[+l.getAttribute('x2'),+l.getAttribute('y2')])"
    model = [py_spring_rk4(120, 16, t - .08 * 2) if t > .16 else 1.0 for t in T]
    rot = lambda o, i: [qang(f, i) for f in o["fr"]]
    crits = [("cards start rotated 8-12 degrees and settle to 0 on the spring k=120, c=16 (80 ms stagger)",
              lambda o, _: (all(8 <= abs(rot(o, i)[0]) <= 12 for i in range(n)) and maxerr([r / start[2][2] for r in rot(o, 2)], model) < 3e-3 and max(abs(rot(o, i)[-1]) for i in range(n)) < .05,
                            [round(rot(o, 2)[j] / start[2][2], 3) for j in range(0, len(T), 8)]), [round(m, 3) for m in model[::8]]),
             ("they end in one aligned row", lambda o, _: (max(qy(o, i)[-1] for i in range(n)) - min(qy(o, i)[-1] for i in range(n)) < .5, [round(qy(o, i)[-1], 2) for i in range(n)]), "same y"),
             ("search pill appears above the row", lambda o, _: (qo(o, n)[0] == 0 and qo(o, n)[-1] == 1 and qy(o, n)[-1] < qy(o, 0)[-1] - 50, [qo(o, n)[0], qo(o, n)[-1]]), [0, 1]),
             ("branches connect the pill to the top of every card", lambda o, _: (all(abs(o["fr"][-1]["x"][i][0] - qx(o, i)[-1]) < 1.5 and abs(o["fr"][-1]["x"][i][1] - (qy(o, i)[-1] - 30)) < 1.5 for i in range(n)),
                                                                              o["fr"][-1]["x"][:2]), "card top centres")]
    return tcard(wd, "scatter", body, css, anim % ("spring(120,16,t-0.08*i)", "p"), ["#c%d" % i for i in range(n)] + ["#pill"], T, crits,
                 naive_anim=anim % ("1", "1"), extra=extra, W=W, H=H, more=more)


@card("CAM-225")
def cam225(task, wd):
    """Bento principle grid: 3x3 colour cards each looping a mini demo, the loops staggered by 60 ms (GSAP repeat/yoyo)."""
    W, H = 480, 270
    cols = ["#e85d75", "#5d9be8", "#f2c14e", "#6cc58e", "#9b6ce8", "#e8955d", "#4ec2c2", "#c2c24e", "#888"]
    body = '<div id=g>' + "".join('<div class=c style="background:%s"><i class=d id=d%d></i></div>' % (c, i) for i, c in enumerate(cols)) + '</div>'
    css = "#g{position:absolute;inset:20px;display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.c{position:relative;border-radius:8px}.d{position:absolute;left:10px;top:20px;width:10px;height:10px;background:#fff;border-radius:50%}"
    anim = "for(let i=0;i<9;i++) tl.to('#d'+i,{x:40,duration:.6,ease:'sine.inOut',repeat:-1,yoyo:true},0.06*i)"
    T = tgrid(3.0, 25)
    model = lambda i, t: 0.0 if t < .06 * i else (40 * sine_io(((t - .06 * i) % .6) / .6) if int((t - .06 * i) // .6) % 2 == 0 else 40 * (1 - sine_io(((t - .06 * i) % .6) / .6)))
    dx = lambda o, i: [x - qx(o, i)[0] for x in qx(o, i)]
    crits = [("every card's demo loops (yoyo sine, 1.2 s period) with a 60 ms stagger", lambda o, _: (all(maxerr(dx(o, i)[5:], [model(i, t) for t in T[5:]]) < .02 for i in range(9)), max(maxerr(dx(o, i)[5:], [model(i, t) for t in T[5:]]) for i in range(9))), "<0.02 px"),
             ("periodic: x(t + 1.2 s) = x(t)", lambda o, _: (maxerr(dx(o, 4)[15:45], dx(o, 4)[45:75]) < .02, maxerr(dx(o, 4)[15:45], dx(o, 4)[45:75])), "<0.02"),
             ("3x3 grid", lambda o, _: (len({round(qx(o, i)[0]) for i in range(9)}) == 3 and len({round(qy(o, i)[0]) for i in range(9)}) == 3, True), True)]
    return tcard(wd, "bentoloops", body, css, anim, ["#d%d" % i for i in range(9)], T, crits, W=W, H=H)


@card("CAM-206")
def cam206(task, wd):
    """Floating badge chaos field: 40-60 mono pill badges with a coloured status dot, random rotateZ +/-8 deg and
    translateZ, spawned every 60-100 ms and drifting 10-20 px/s, far layer blurred, a counter that grows with the density."""
    W, H = 640, 360
    rng = np.random.default_rng(11)
    n = 50
    gaps = rng.uniform(.06, .10, n)
    spawn = np.concatenate([[0.1], 0.1 + np.cumsum(gaps[:-1])]).tolist()
    data = [dict(t=spawn[i], x=float(rng.uniform(20, 560)), y=float(rng.uniform(30, 320)), z=float(rng.uniform(-300, 80)), r=float(rng.uniform(-8, 8)),
                 vx=float(rng.uniform(10, 20) * rng.choice([-1, 1]))) for i in range(n)]
    body = '<div id=sc style="position:absolute;inset:0;perspective:600px;perspective-origin:50% 50%">' + "".join(
        '<span class=bd id=b%d><i style="background:%s"></i>status-%02d</span>' % (i, ["#2ecc71", "#e67e22", "#e74c3c"][i % 3], i) for i in range(n)) + '</div><b id=cnt>0</b>'
    css = (".bd{position:absolute;left:0;top:0;opacity:0;font:9px monospace;padding:2px 7px;border-radius:99px;background:#fff;white-space:nowrap}.bd i{display:inline-block;width:6px;height:6px;border-radius:50%;margin-right:4px}"
           "#cnt{position:absolute;right:16px;bottom:10px;font:700 20px monospace}")
    anim = ("const D=%s; window.camAt=function(t){ let c=0; D.forEach((d,i)=>{ const e=document.getElementById('b'+i); const on=APPLY&&t>=d.t; if(on) c++;"
            "e.style.opacity=on?1:0; const dx=on?d.vx*(t-d.t):0; e.style.transform='translate3d('+(d.x+dx)+'px,'+d.y+'px,'+d.z+'px) rotateZ('+d.r+'deg)';"
            "e.style.filter=d.z<-150?'blur(2px)':'none'; }); document.getElementById('cnt').textContent=c; }") % json.dumps(data)
    T = tgrid(5.5, 50)
    extra = "t=>[+document.getElementById('cnt').textContent, [...document.querySelectorAll('.bd')].filter(e=>e.style.opacity==='1').length]"
    sels = ["#b%d" % i for i in range(n)]

    def onsets(o):
        cnt = [f["x"][1] for f in o["fr"]]
        return [T[j] for j in range(1, len(T)) if cnt[j] > cnt[j - 1]], cnt

    def drift(o, i):
        # world drift = screen displacement / perspective scale, between 1.0 s and 2.0 s after the badge spawned
        a, b = idx(T, data[i]["t"] + 1.0), idx(T, data[i]["t"] + 2.0)
        fa, fb = o["fr"][a]["el"][i]["q"], o["fr"][b]["el"][i]["q"]
        sc = math.dist(fa[0], fa[1]) / o["w0"][i]
        return (np.array(fb).mean(0)[0] - np.array(fa).mean(0)[0]) / sc / (T[b] - T[a])
    more = ", w0:[...document.querySelectorAll('.bd')].map(e=>{const s=e.style.transform; e.style.transform='none'; const w=e.getBoundingClientRect().width; e.style.transform=s; return w;})"
    crits = [("badges spawn one by one every 60-100 ms (measured onsets, 20 ms sampling)", lambda o, _: ((lambda on: len(on[0]) >= 40 and all(.04 <= d <= .12 for d in np.diff(on[0])) and abs(np.mean(np.diff(on[0])) - .08) < .01)(onsets(o)),
                                                                                                  [len(onsets(o)[0]), round(float(np.mean(np.diff(onsets(o)[0]))), 3) if len(onsets(o)[0]) > 1 else None]), ["40-60", .08]),
             ("40-60 badges, the counter equals the visible density at every frame", lambda o, _: (40 <= onsets(o)[1][-1] <= 60 and all(f["x"][0] == f["x"][1] for f in o["fr"]), onsets(o)[1][-1]), "40-60"),
             ("rotateZ within +/-8 deg", lambda o, _: (max(abs(qang(o["fr"][-1], i)) for i in range(n)) <= 8.05, max(abs(qang(o["fr"][-1], i)) for i in range(n))), "<=8"),
             ("slow drift 10-20 px/s (world units, measured through the perspective)", lambda o, _: (all(10 - .3 <= abs(drift(o, i)) <= 20 + .3 for i in range(0, 30, 3)), [round(drift(o, i), 2) for i in range(0, 30, 3)]), "10-20"),
             ("far layer blurred, near layer sharp", lambda o, _: (all((f > 0) == (d["z"] < -150) for f, d in zip([o["fr"][-1]["el"][i]["b"] for i in range(n)], data)), sum(1 for d in data if d["z"] < -150)), "z<-150 blurred")]
    return tcard(wd, "badges", body, css, "const APPLY=true;" + anim, sels, T, crits, naive_anim="const APPLY=false;" + anim, extra=extra, W=W, H=H, more=more)


@card("CAM-209")
def cam209(task, wd):
    """Sunburst finale ring: 20 pastel alternating rays rotating 4 deg/s behind a centred two-line handwritten title,
    character stickers arranged on an ellipse around it, small stars twinkling; rotation and ray count measured."""
    W, H = 480, 270
    ns = 8
    body = ('<div id=rays></div><div id=title>شكرًا<br>للمشاهدة</div>' + "".join('<i class=st id=s%d></i>' % i for i in range(ns)) +
            "".join('<b class=star id=k%d style="left:%dpx;top:%dpx"></b>' % (i, 30 + 97 * i, 20 + 51 * (i % 3)) for i in range(5)))
    css = ("#rays{position:absolute;left:-60px;top:-165px;width:600px;height:600px;border-radius:50%;background:repeating-conic-gradient(#f9d5e5 0 9deg,#c9e4f6 9deg 18deg)}"
           "#title{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);font:700 22px/1.2 cursive;text-align:center;color:#402151}"
           ".st{position:absolute;width:24px;height:24px;margin:-12px;border-radius:6px;background:#ff8a5c}.star{position:absolute;width:6px;height:6px;background:#fff;transform:rotate(45deg)}")
    anim = ("window.camAt=function(t){ document.getElementById('rays').style.transform='rotate('+(4*t)+'deg)';"
            "for(let i=0;i<%d;i++){ const a=2*Math.PI*i/%d; const e=document.getElementById('s'+i); e.style.left=(240+170*Math.cos(a))+'px'; e.style.top=(135+95*Math.sin(a))+'px'; }"
            "for(let i=0;i<5;i++) document.getElementById('k'+i).style.opacity=0.5+0.5*Math.sin(2*Math.PI*(1.5*t+i/5)); }") % (ns, ns)
    T = tgrid(2.0, 10)
    sels = ["#rays"] + ["#s%d" % i for i in range(ns)] + ["#k%d" % i for i in range(5)]
    more = ", title:R('#title'), br:document.getElementById('title').querySelectorAll('br').length"
    spec = dict(body=body, css=css, js="var tl=gsap.timeline({paused:true}); %s; camAt(0); const T=%s; OUT({fr:SAMPLE(T,%s,null)%s}); camAt(0)" % (anim, json.dumps(T), json.dumps(sels), more),
                W=W, H=H, scripts=[GSAP], shot=True)

    def rays(im):
        # dominant angular frequency of the pink/blue alternation on a ring around the centre (occluders count 0.5)
        ang = np.linspace(0, 2 * np.pi, 2048, endpoint=False)
        cx, cy, r = 240, 135, 120
        px = im[(cy + r * np.sin(ang)).astype(int), (cx + r * np.cos(ang)).astype(int)]
        pink = np.abs(px - [0xf9, 0xd5, 0xe5]).max(-1) < 14
        blue = np.abs(px - [0xc9, 0xe4, 0xf6]).max(-1) < 14
        sig = np.where(pink, 1.0, np.where(blue, 0.0, 0.5)) - 0.5
        spec_ = np.abs(np.fft.rfft(sig))
        return float(np.argmax(spec_[2:60]) + 2)
    ell = lambda o: max(abs(((qc(o["fr"][0], i)[0] - 240) / 170) ** 2 + ((qc(o["fr"][0], i)[1] - 135) / 95) ** 2 - 1) for i in range(1, ns + 1))
    crits = [("rays rotate 4 deg/s", lambda o, _: (abs((qang(o["fr"][-1], 0) - qang(o["fr"][0], 0)) / 2.0 - 4) < 1e-3, (qang(o["fr"][-1], 0) - qang(o["fr"][0], 0)) / 2.0), 4),
             ("16-24 alternating pastel rays (counted on the screenshot)", lambda o, im: (16 <= round(rays(im)) <= 24 and abs(rays(im) - 20) < 1.5, rays(im)), 20),
             ("stickers on an ellipse around the centred two-line title", lambda o, _: (ell(o) < 1e-3 and o["br"] == 1 and abs(ctr(o["title"])[0] - 240) < 1 and abs(ctr(o["title"])[1] - 135) < 1, [ell(o), o["br"]]), "on ellipse, 2 lines"),
             ("stars twinkle (opacity oscillates)", lambda o, _: (min(np.std(qo(o, ns + 1 + i)) for i in range(5)) > .2, [round(float(np.std(qo(o, ns + 1 + i))), 3) for i in range(5)]), ">0.2")]
    naive = dict(js=spec["js"].replace("'rotate('+(4*t)+'deg)'", "'none'"))
    return lcard(wd, "sunburst", spec, crits, naive)


def homography(src, dst):
    A = []
    for (x, y), (u, v) in zip(src, dst):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y, -u], [0, 0, 0, x, y, 1, -v * x, -v * y, -v]]
    _, _, vt = np.linalg.svd(np.array(A, float))
    return vt[-1].reshape(3, 3) / vt[-1][-1]


@card("CAM-222")
def cam222(task, wd):
    """Tilted DOF card wall backdrop: a grid of content cards on a plane rotated rotateX 20 deg / rotateZ -10 deg, blurred
    6 px, at 50% opacity and darkened, drifting 15 px/s behind a sharp headline; drift measured in plane coordinates by
    inverting the plane's homography."""
    W, H = 640, 360
    body = ('<div id=persp style="position:absolute;inset:0;perspective:800px"><div id=plane><div id=wall>' +
            "".join('<i class=cd id=c%d></i>' % i for i in range(12)) + '</div></div></div><h1 id=hl>Every idea, one canvas</h1>')
    css = ("#plane{position:absolute;left:70px;top:30px;width:500px;height:300px;transform:rotateX(20deg) rotateZ(-10deg);filter:blur(6px) brightness(.6);opacity:.5}"
           "#wall{position:absolute;left:0;top:0;display:grid;grid-template-columns:repeat(4,110px);gap:12px}.cd{display:block;height:80px;background:#fff;border-radius:8px}"
           "#hl{position:absolute;left:0;right:0;top:150px;text-align:center;font:700 26px sans-serif;margin:0;color:#fff}#view{background:#123}")
    anim = "window.camAt=function(t){ document.getElementById('wall').style.transform='translateX('+(-15*t)+'px)'; }"
    T = tgrid(2.0, 10)
    sels = ["#plane", "#c5", "#hl"]
    more = ", f:CS('#plane','filter'), op:CS('#plane','opacity')"

    def plane_drift(o):
        Hm = homography([(0, 0), (500, 0), (500, 300), (0, 300)], o["fr"][0]["el"][0]["q"])
        inv = np.linalg.inv(Hm)
        pts = []
        for f in o["fr"]:
            c = np.array(f["el"][1]["q"]).mean(0)
            p = inv @ [c[0], c[1], 1]
            pts.append(p[:2] / p[2])
        pts = np.array(pts)
        return float(np.polyfit(T, pts[:, 0], 1)[0]), float(np.ptp(pts[:, 1]))

    def tilt(o):
        q = o["fr"][0]["el"][0]["q"]
        top, bot = math.dist(q[0], q[1]), math.dist(q[3], q[2])
        return math.degrees(math.atan2(q[1][1] - q[0][1], q[1][0] - q[0][0])), top / bot
    crits = [("the wall drifts 15 px/s in its own plane (homography-inverted)", lambda o, _: (abs(plane_drift(o)[0] + 15) < .05 and plane_drift(o)[1] < .05, plane_drift(o)), [-15, 0]),
             ("plane rotated: screen tilt ~ -10 deg and top edge foreshortened by rotateX 20", lambda o, _: (abs(tilt(o)[0] + 10) < 1.5 and tilt(o)[1] < .99, tilt(o)), ["-10 deg", "top < bottom"]),
             ("backdrop blurred 6 px, darkened, 50% opacity; headline sharp", lambda o, _: (qb(o, 0)[0] == 6 and "brightness(0.6)" in o["f"] and abs(qo(o, 1)[0] - .5) < 1e-6 and qb(o, 2)[0] == 0, [qb(o, 0)[0], o["f"], qo(o, 1)[0], qb(o, 2)[0]]), [6, "brightness", .5, 0])]
    return tcard(wd, "cardwall", body, css, anim, sels, T, crits, naive_anim="window.camAt=function(t){}", W=W, H=H, more=more)


LIST_ROWS = [{"title": "Kling", "tagline": "Physics-heavy shots", "bullets": ["motion", "camera"], "accent": "rgb(255, 90, 54)", "stat": "1080p"},
             {"title": "Veo", "tagline": "Native audio", "bullets": ["dialogue", "sfx", "music"], "accent": "rgb(46, 134, 255)", "stat": "8 s"},
             {"title": "Runway", "tagline": "Editor first", "bullets": ["references"], "accent": "rgb(30, 200, 120)", "stat": "Gen-4"},
             {"title": "Luma", "tagline": "Dream Machine", "bullets": ["loops", "keyframes"], "accent": "rgb(160, 90, 255)", "stat": "Ray2"},
             {"title": "Pika", "tagline": "Effects", "bullets": ["swaps", "inflate", "melt"], "accent": "rgb(255, 190, 0)", "stat": "2.2"},
             {"title": "Hailuo", "tagline": "Fast drafts", "bullets": ["i2v", "t2v"], "accent": "rgb(0, 190, 200)", "stat": "6 s"}]


@card("CAM-245")
def cam245(task, wd):
    """Templated listicle card: one HTML component fed by data rows (title, tagline, bullets, stats, accent colour,
    illustration), text column left 55% and a framed visual right 40%, reused for every item, 6 items x 8 s."""
    W, H = 640, 360
    css = ("#txt{position:absolute;left:0;top:0;width:55%;height:100%;box-sizing:border-box;padding:40px;font-family:sans-serif}#txt h1{margin:0;font-size:30px}"
           "#vis{position:absolute;left:58%;top:15%;width:40%;height:70%;border:3px solid;box-sizing:border-box;border-radius:12px}")
    js_comp = ("const ROWS=%s; function Card(r){ return '<div id=txt><h1 style=\"color:'+r.accent+'\">'+r.title+'</h1><p>'+r.tagline+'</p><ul>'+r.bullets.map(b=>'<li>'+b+'</li>').join('')+'</ul><b>'+r.stat+'</b></div>'"
               "+'<div id=vis style=\"border-color:'+r.accent+'\"></div>'; }"
               "window.camAt=function(t){ const i=Math.min(5,Math.floor(t/8)); const v=document.getElementById('view'); if(v.dataset.i!=String(i)){ v.innerHTML=CARD_EXPR; v.dataset.i=i; } }").replace("%s", json.dumps(LIST_ROWS), 1)
    T = [8 * i + 4 for i in range(6)]
    extra = "t=>({h:document.querySelector('#txt h1').textContent, c:getComputedStyle(document.querySelector('#txt h1')).color, li:document.querySelectorAll('li').length, txt:R('#txt'), vis:R('#vis'), vb:CS('#vis','border-top-color')})"
    crits = [("each 8 s segment renders its own data row (title, accent, bullet count)", lambda o, _: ([(f["x"]["h"], f["x"]["c"], f["x"]["li"]) for f in o["fr"]] == [(r["title"], r["accent"], len(r["bullets"])) for r in LIST_ROWS],
                                                                                                [f["x"]["h"] for f in o["fr"]]), [r["title"] for r in LIST_ROWS]),
             ("one layout for every item: text 55% left, framed visual 40% right", lambda o, _: (all(near(f["x"]["txt"][2], .55 * W) and near(f["x"]["vis"][2], .40 * W) and f["x"]["vis"][0] > f["x"]["txt"][2] for f in o["fr"]),
                                                                                         [o["fr"][0]["x"]["txt"][2], o["fr"][0]["x"]["vis"][2]]), [.55 * W, .4 * W]),
             ("the frame takes the row's accent colour", lambda o, _: (all(f["x"]["vb"] == r["accent"] for f, r in zip(o["fr"], LIST_ROWS)), [f["x"]["vb"] for f in o["fr"]][:2]), "accent")]
    return tcard(wd, "listicle", "", css, js_comp.replace("CARD_EXPR", "Card(ROWS[i])"), ["#view"], T, crits, naive_anim=js_comp.replace("CARD_EXPR", "Card(ROWS[0])"), extra=extra, W=W, H=H)


def _png(path, W, H, draw):
    from PIL import Image, ImageDraw
    im = Image.new("RGB", (W, H), (255, 255, 255))
    draw(ImageDraw.Draw(im))
    im.save(path)
    return path


@card("CAM-25")
def cam25(task, wd):
    """Legibility veils over footage: desktop = linear-gradient(90deg, .78 -> .18 at 58% -> .24) under
    linear-gradient(0deg, .85 -> transparent at 57%) of rgba(4,9,17); phones (<=700 px) switch to one bottom veil .92 ->
    .2 at 76% and object-position 83% center. Alphas measured on a white plate against the compositing model."""
    src = _png(wd / "footage.png", 640, 360, lambda d: d.ellipse([0.83 * 640 - 14, 166, 0.83 * 640 + 14, 194], fill=(255, 0, 0)))
    inner = ('<!doctype html><html dir=rtl><head><style>body{margin:0}.hero{position:relative;width:100vw;height:100vh;overflow:hidden;background:#fff}'
             '.vid{position:absolute;inset:0;width:100%%;height:100%%;object-fit:cover;object-position:50%% 50%%}%s</style></head><body><div class=hero>'
             '<img class=vid src="%s"><div class=veil style="position:absolute;inset:0"></div></div></body></html>')
    veil = (".veil{background:linear-gradient(0deg,rgba(4,9,17,.85),transparent 57%),linear-gradient(90deg,rgba(4,9,17,.78),rgba(4,9,17,.18) 58%,rgba(4,9,17,.24))}"
            "@media (max-width:700px){.veil{background:linear-gradient(0deg,rgba(4,9,17,.92),rgba(4,9,17,.2) 76%)}.vid{object-position:83% center}}")
    js = "const d1=FRAME(%s,800,450); const d2=FRAME(%s,270,480); d2.defaultView.frameElement.style.left='810px'; OUT(1)"
    mk = lambda v: js % (json.dumps(inner % (v, src.as_uri())), json.dumps(inner % (v, src.as_uri())))
    spec = dict(js=mk(veil), W=1080, H=480, shot=True, budget=4000)
    naive = dict(js=mk(""), shot=True)
    lin = lambda f, stops: float(np.interp(f, [s[0] for s in stops], [s[1] for s in stops]))

    def model_desk(x, y, W=800, H=450):
        a2 = lin((x + .5) / W, [(0, .78), (.58, .18), (1, .24)])
        a1 = lin((H - y - .5) / H, [(0, .85), (.57, 0), (1, 0)])
        return 1 - (1 - a1) * (1 - a2)
    model_phone = lambda y, H=480: lin((H - y - .5) / H, [(0, .92), (.76, .2), (1, .2)])
    alpha = lambda im, x, y: float((255 - im[y, x, 1]) / (255 - 9))
    dpts = [(80, 90), (400, 90), (640, 90), (240, 405), (700, 300)]
    ppts = [(135, 40), (60, 240), (135, 300), (200, 460)]

    def errs(im):
        e = [abs(alpha(im, x, y) - model_desk(x, y)) for x, y in dpts if not (600 < x < 730 and 150 < y < 210)]
        e += [abs(alpha(im, 810 + x, y) - model_phone(y)) for x, y in ppts]
        return max(e)
    red = lambda im: np.argwhere((im[:, 810:, 0] - im[:, 810:, 1]) > 40)
    crits = [("measured veil alpha matches the stacked-gradient model at every probe (desktop + phone)", lambda o, im: (errs(im) < .015, errs(im)), "<0.015"),
             ("the text side (left) is darker than the subject side on desktop", lambda o, im: (alpha(im, 40, 90) > alpha(im, 600, 90) + .4, [alpha(im, 40, 90), alpha(im, 600, 90)]), ".78 vs ~.2"),
             ("phone: mostly-bottom veil and object-position 83% keeps the subject in frame at 83% of the width", lambda o, im: (len(red(im)) > 50 and abs(red(im)[:, 1].mean() - .83 * 270) < 2, float(red(im)[:, 1].mean()) if len(red(im)) else None), .83 * 270)]
    return lcard(wd, "veils", spec, crits, naive, [src])


@card("CAM-135")
def cam135(task, wd):
    """Top shade for title legibility: #shade, 48% tall, linear-gradient(180deg, rgba(5,10,18,.55) 0 -> .25 at 55% -> 0),
    fades 0 -> 1 from 0.3 s over 0.8 s and back to 0 before the action; opacity sampled, alpha profile measured."""
    W, H = 480, 270
    body = '<div id=shade></div><h1 id=t>العنوان</h1>'
    css = ("#view{background:#fff}#shade{position:absolute;left:0;top:0;width:100%;height:48%;background:linear-gradient(180deg,rgba(5,10,18,.55) 0%,rgba(5,10,18,.25) 55%,rgba(5,10,18,0) 100%);opacity:0}"
           "#t{position:absolute;top:20px;left:0;right:0;text-align:center;margin:0;font:700 20px sans-serif;color:transparent}")
    anim = "tl.to('#shade',{opacity:1,duration:.8,ease:'none'},.3).to('#shade',{opacity:0,duration:.5,ease:'none'},2.5)"
    T = tgrid(3.2, 10)
    js = ("var tl=gsap.timeline({paused:true}); %s; const T=%s; const fr=SAMPLE(T,['#shade'],null); tl.seek(1.5,false); OUT({fr})")
    spec = dict(body=body, css=css, js=js % (anim, json.dumps(T)), W=W, H=H, scripts=[GSAP], shot=True)
    naive = dict(js=js % ("", json.dumps(T)), shot=True)
    model_op = [min(1, max(0, (t - .3) / .8)) if t < 2.5 else max(0, 1 - (t - 2.5) / .5) for t in T]
    sh = .48 * H
    prof = lambda y: float(np.interp((y + .5) / sh, [0, .55, 1], [.55, .25, 0]))
    alpha = lambda im, y: float((255 - im[y, 20, 2]) / (255 - 18))
    ys = [0, 30, int(.55 * sh), 100, 128]
    crits = [("shade opacity: 0 -> 1 from 0.3 s over 0.8 s, back to 0 before the action (2.5-3.0 s)", lambda o, _: (maxerr(qo(o, 0), model_op) < 1e-3, [round(v, 3) for v in qo(o, 0)[::4]]), [round(v, 3) for v in model_op[::4]]),
             ("gradient alpha .55 -> .25 at 55% -> 0 over the top 48% (measured at full opacity)", lambda o, im: (max(abs(alpha(im, y) - prof(y)) for y in ys) < .012, [round(alpha(im, y), 3) for y in ys]), [round(prof(y), 3) for y in ys]),
             ("nothing below 48% of the frame is shaded", lambda o, im: (float(im[int(sh) + 2:, :, 2].min()) > 253, float(im[int(sh) + 2:, :, 2].min())), 255)]
    return lcard(wd, "topshade", spec, crits, naive)


@card("CAM-149")
def cam149(task, wd):
    """Readability glass and arch veil: an elliptical glass (860x500 at 1080p, border-radius 50%, radial
    rgba(25,8,40,.55) -> .32 at 45% -> 0 at 72%) behind the text, and an even-odd SVG veil (frame minus the arch) in
    #12062a whose opacity eases .38 -> .22; alphas measured on a white plate at 1/3 scale."""
    W, H = 640, 360
    gw, gh = 860 / 3, 500 / 3
    body = ('<svg id=arch width=640 height=360 style="position:absolute;left:0;top:0"><path id=veil fill="#12062a" fill-rule="evenodd" opacity=".38" '
            'd="M0 0H640V360H0Z M220 330V160A100 100 0 0 1 420 160V330Z"/></svg><div id=glass></div>')
    css = ("#view{background:#fff}#glass{position:absolute;left:%.4fpx;top:%.4fpx;width:%.4fpx;height:%.4fpx;border-radius:50%%;"
           "background:radial-gradient(rgba(25,8,40,.55),rgba(25,8,40,.32) 45%%,rgba(25,8,40,0) 72%%)}") % (320 - gw / 2, 250 - gh / 2, gw, gh)
    js = ("var tl=gsap.timeline({paused:true}); %s; const T=%s; const fr=SAMPLE(T,['#view'],t=>+getComputedStyle(document.getElementById('veil')).opacity); tl.seek(0,false); OUT({fr})")
    anim = "tl.to('#veil',{opacity:.22,duration:2,ease:'sine.inOut'},0)"
    T = tgrid(2, 10)
    spec = dict(body=body, css=css, js=js % (anim, json.dumps(T)), W=W, H=H, scripts=[GSAP], shot=True)
    naive = dict(body="", css="#view{background:#fff}", js=(js % ("", json.dumps(T))).replace("getComputedStyle(document.getElementById('veil')).opacity", "0"), shot=True)
    a_glass = lambda im, x, y: float((255 - im[y, x, 0]) / (255 - 25))
    a_veil = lambda im, x, y: float((255 - im[y, x, 0]) / (255 - 0x12))

    def glass_model(x, y):
        rx, ry = gw / 2 * math.sqrt(2), gh / 2 * math.sqrt(2)
        rho = math.hypot((x + .5 - 320) / rx, (y + .5 - 250) / ry)
        return float(np.interp(rho, [0, .45, .72], [.55, .32, 0]))
    gpts = [(320, 250), (350, 250), (380, 250), (320, 280)]
    vm = [.38 + (.22 - .38) * sine_io(t / 2) for t in T]
    crits = [("even-odd veil: outside the arch alpha .38, inside the arch untouched", lambda o, im: (abs(a_veil(im, 40, 40) - .38) < .01 and abs(a_veil(im, 600, 340) - .38) < .01 and float(im[165, 320, 0]) > 254,
                                                                                         [a_veil(im, 40, 40), a_veil(im, 600, 340), float(im[165, 320, 0])]), [.38, .38, 255]),
             ("glass radial alpha .55 -> .32 at 45% -> 0 at 72% (measured inside the arch)", lambda o, im: (max(abs(a_glass(im, x, y) - glass_model(x, y)) for x, y in gpts) < .015,
                                                                                                    [round(a_glass(im, x, y), 3) for x, y in gpts]), [round(glass_model(x, y), 3) for x, y in gpts]),
             ("veil opacity eases .38 -> .22", lambda o, _: (maxerr([f["x"] for f in o["fr"]], vm) < 1e-3, [round(f["x"], 3) for f in o["fr"][::5]]), [round(v, 3) for v in vm[::5]])]
    return lcard(wd, "glassarch", spec, crits, naive)


@card("CAM-26")
def cam26(task, wd):
    """Masked art fade on cards: the RTL card's ::after art (30% wide on the far side) is masked with
    linear-gradient(to right, ink 35%, transparent) and toned grayscale + sepia; stripe contrast measured across it."""
    W, H = 480, 200
    body = '<div class="gate has-art" dir=rtl><b>بوابة الأرض</b></div>'
    css = (".gate{position:absolute;left:40px;top:40px;width:400px;height:120px;background:#1b1f2a;color:#fff;font:16px sans-serif;"
           "--art:repeating-linear-gradient(90deg,#ff0000 0 4px,#00ff00 4px 8px,#ffffff 8px 12px,#000000 12px 16px)}"
           ".gate.has-art::after{content:'';position:absolute;inset-block:0;inset-inline-end:0;width:30%;background:var(--art);background-size:cover;"
           "-webkit-mask-image:linear-gradient(to right,#000 35%,transparent);mask-image:linear-gradient(to right,#000 35%,transparent);filter:grayscale(1) sepia(1)}")
    naive_css = css.replace("-webkit-mask-image:linear-gradient(to right,#000 35%,transparent);mask-image:linear-gradient(to right,#000 35%,transparent);filter:grayscale(1) sepia(1)", "")
    js = "OUT({g:R('.gate')})"
    aw = 120.0

    def contrast(im, f):
        x = int(40 + f * aw)
        row = lum(im[100, x - 8:x + 8])
        return float(row.max() - row.min())

    def mask_at(im, f):
        # centre column of the white stripe nearest f: composite = card*(1-m) + sepia-white*m (green channel)
        k = round((f * aw - 10) / 16)
        x = 40 + 16 * k + 10
        return (16 * k + 10.5) / aw, float((im[100, x, 1] - 31) / (255 - 31))
    fs = [.15, .5, .6, .8]
    m = lambda f: 1.0 if f <= .35 else 1 - (f - .35) / .65
    crits = [("art fades into the card: measured mask alpha 1 -> 0 after 35% (white-stripe centres)", lambda o, im: (all(abs(mask_at(im, f)[1] - m(mask_at(im, f)[0])) < .03 for f in fs),
                                                                                            [[round(v, 3) for v in mask_at(im, f)] for f in fs]), [round(m((16 * round((f * aw - 10) / 16) + 10.5) / aw), 3) for f in fs]),
             ("art sits on the far (inline-end = left in RTL) 30% of the card, the rest is plain card", lambda o, im: (contrast(im, .15) > 100 and float(np.ptp(lum(im[100, 170:430]))) < 3, [contrast(im, .15), float(np.ptp(lum(im[100, 170:430])))]), [">100", "<3"]),
             ("toned: grayscale + sepia (bright stripes warm, r >= g >= b, low saturation)", lambda o, im: ((lambda px: bool(((px[:, 0] >= px[:, 1] - 1) & (px[:, 1] >= px[:, 2] - 1)).all()) and float((px.max(-1) - px.min(-1)).max()) < 80)(im[100, 42:80]),
                                                                                                    im[100, 50].tolist()), "sepia")]
    return lcard(wd, "artfade", dict(body=body, css=css, js=js, W=W, H=H, shot=True), crits, dict(css=naive_css, shot=True))


# ───────────────────────────── ffmpeg camera engines: real filters on a marker plate, measured from the decoded video ─────────────────────────────

GREY = (119, 119, 119)


def marker_png(path, W, H, marks, bg=GREY):
    """A 'screenshot' plate: flat grey with coloured markers (x, y, w, h, hex) whose centroids are measured later."""
    from PIL import Image, ImageDraw
    im = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(im)
    for x, y, w, h, c in marks:
        d.rectangle([x, y, x + w - 1, y + h - 1], fill=hex2rgb(c))
    im.save(path)
    return Path(path)


def ff_zoom(wd, name, src, W, H, dur, fps, zexpr, ss=4, post=""):
    """Centre zoom with a per-frame scale expression in t (scale eval=frame on a ss-x supersampled plate, centre crop,
    area downscale)."""
    out = wd / ("%s.mp4" % name)
    vf = ("scale=%d:%d:flags=bicubic,scale=w='trunc(%d*(%s)/2)*2':h=-2:eval=frame:flags=bicubic,crop=%d:%d,scale=%d:%d:flags=area%s"
          % (W * ss, H * ss, W * ss, zexpr, W * ss, H * ss, W, H, post))
    ff("-loop", "1", "-framerate", fps, "-i", src, "-t", dur, "-vf", vf, "-r", fps, "-c:v", "libx264rgb", "-qp", "0", "-preset", "ultrafast", out)
    return out


ZMARKS = [(40, 30, 14, 14, RED), (266, 136, 14, 14, BLUE)]


def zoom_series(video, cols=(RED, BLUE), bg=GREY, tol=None):
    fr = read_video(video)
    m = track_colors(fr, [hex2rgb(c) for c in cols], tol=tol or 40, bg=None if tol else bg)
    d = [math.hypot(a["cx"] - b["cx"], a["cy"] - b["cy"]) if a and b else float("nan") for a, b in m]
    return np.array(d) / d[0], fr, m


@card("CAM-22")
def cam22(task, wd):
    """Ken Burns on captured screenshots: the still always moves, zoom 1 -> 1.04 over the beat (2 s, sine ease, ffmpeg
    scale eval=frame); background photos get a 70% tinted overlay. Scale measured from two markers in the output."""
    src = marker_png(wd / "screenshot.png", 320, 180, ZMARKS)
    T = times_for(2.0 - 1 / 30, 30)
    v = ff_zoom(wd, "kenburns", src, 320, 180, 2.0, 30, "1+0.04*(1-cos(PI*min(t/2,1)))/2")
    bgv = ff_zoom(wd, "kenburns_bg", src, 320, 180, 2.0, 30, "1+0.04*(1-cos(PI*min(t/2,1)))/2", post=",drawbox=x=0:y=0:w=iw:h=ih:color=0x101828@0.7:t=fill")
    still = wd / "still_input.mp4"
    ff("-loop", "1", "-framerate", 30, "-i", src, "-t", 2.0, "-c:v", "libx264rgb", "-qp", "0", "-preset", "ultrafast", still)
    s, _, _ = zoom_series(v)
    si, _, _ = zoom_series(still)
    model = [1 + 0.04 * sine_io(t / 2) for t in T]
    bgpx = read_video(bgv)[5][90, 160]
    want = np.array(GREY) * .3 + np.array([0x10, 0x18, 0x28]) * .7
    return [check("measured scale follows 1 -> 1.04 sine over the beat", maxerr(s, model) < .003, [round(float(x), 4) for x in s[::10]], [round(x, 4) for x in model[::10]]),
            check("no still sits dead: monotonic push, >= 20 scale steps, never still > 3 frames in the middle of the beat", bool((np.diff(s) >= -1e-4).all()) and int((np.abs(np.diff(s)) > 1e-5).sum()) >= 20
                  and max(len(list(g)) for k, g in __import__("itertools").groupby(np.round(s[15:45], 5))) <= 3,
                  [int((np.abs(np.diff(s)) > 1e-5).sum()), max(len(list(g)) for k, g in __import__("itertools").groupby(np.round(s[15:45], 5)))], [">=20", "<=3"]),
            check("background-photo variant: 70% overlay (pixel = 0.3 x plate + 0.7 x tint)", float(np.abs(bgpx - want).max()) < 1.5, bgpx, want),
            check("negative control: the unprocessed still never moves", not maxerr(si, model) < .003, float(np.nanmax(np.abs(si - 1))), "0")], [v, bgv]


@card("CAM-145")
def cam145(task, wd):
    """Ken Burns raised-cosine zoom rendered at 2x: zoom(t) = from + (to - from)(1 - cos(pi p))/2, 1.0 -> 1.08, the
    frames scaled at 2x and downsampled; the measured curve and the 2x-vs-1x quantisation error are compared."""
    src = marker_png(wd / "plate.png", 320, 180, ZMARKS)
    T = times_for(2.0 - 1 / 30, 30)
    z = "1+0.08*(1-cos(PI*min(t/2,1)))/2"
    v2 = ff_zoom(wd, "raisedcos_2x", src, 320, 180, 2.0, 30, z, ss=2)
    v1 = ff_zoom(wd, "raisedcos_1x", src, 320, 180, 2.0, 30, z, ss=1)
    model = np.array([1 + .08 * (1 - math.cos(math.pi * min(t / 2, 1))) / 2 for t in T])
    s2, _, _ = zoom_series(v2)
    s1, _, _ = zoom_series(v1)
    e2, e1 = float(np.abs(s2 - model).max()), float(np.abs(s1 - model).max())
    still = wd / "still_input.mp4"
    ff("-loop", "1", "-framerate", 30, "-i", src, "-t", 2.0, "-c:v", "libx264rgb", "-qp", "0", "-preset", "ultrafast", still)
    si, _, _ = zoom_series(still)
    return [check("measured zoom follows the raised cosine 1.0 -> 1.08", e2 < .004, e2, "<0.004"),
            check("speed ~0 at both ends, maximal mid-way (6-frame windows)", abs(s2[6] - s2[0]) < .005 and abs(s2[-1] - s2[-7]) < .005 and s2[33] - s2[27] > .009,
                  [float(s2[6] - s2[0]), float(s2[33] - s2[27]), float(s2[-1] - s2[-7])], ["<0.005", ">0.009", "<0.005"]),
            check("the 2x render quantises less than a 1x render", e2 < e1, [e2, e1], "2x < 1x"),
            check("negative control: the unprocessed still does not push", not float(np.abs(si - model).max()) < .004, float(np.abs(si - model).max()), ">=0.004")], [v2, v1]


@card("CAM-147")
def cam147(task, wd):
    """Retention zoom punches with the card's ffmpeg fix: zoompan z = 1.10 for 1.2 s on every 4th beat (90 bpm -> every
    2.67 s), written with 'it' because zoompan has no 't' (the broken expression is rejected); output 1080x1920 @30."""
    W, H = 1080, 1920
    src = marker_png(wd / "talking.png", W, H, [(240, 500, 60, 60, RED), (780, 1360, 60, 60, BLUE)])
    beat = 60 / 90
    per = 4 * beat
    zexpr = "if(lte(mod(%s\\,%.6f)\\,1.2)\\,1.10\\,1)"
    out = wd / "punches.mp4"
    common = ["-loop", "1", "-framerate", 30, "-i", src, "-t", 6.6]
    zp = "zoompan=z='%s':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=%dx%d:fps=30"
    broken_ok = True
    try:
        ff(*common, "-vf", zp % (zexpr % ("t", per), W, H), "-frames:v", 3, "-c:v", "libx264", "-preset", "ultrafast", wd / "broken.mp4")
    except RuntimeError as e:
        broken_ok = False
        (wd / "broken_expression.txt").write_text(str(e), encoding="utf-8")
    ff(*common, "-vf", zp % (zexpr % ("it", per), W, H), "-c:v", "libx264", "-crf", "12", "-preset", "ultrafast", "-pix_fmt", "yuv420p", out)
    p = fx.probe(out)["streams"][0]
    fr = fx.frames(out, size=(270, 480))
    m = track_colors(fr, [hex2rgb(RED), hex2rgb(BLUE)], tol=60)
    d = np.array([math.hypot(a["cx"] - b["cx"], a["cy"] - b["cy"]) for a, b in m])
    z = d / np.median(d[(np.arange(len(d)) / 30 % per) > 1.4])     # relative to the unpunched frames
    T = np.arange(len(z)) / 30
    on = z > 1.05
    starts = [T[i] for i in range(len(on)) if on[i] and (i == 0 or not on[i - 1])]
    runs = []
    for i in range(len(on)):
        if on[i] and (i == 0 or not on[i - 1]):
            j = i
            while j < len(on) and on[j]:
                j += 1
            runs.append((j - i) / 30)
    still_d = np.array([math.hypot(a["cx"] - b["cx"], a["cy"] - b["cy"]) for a, b in track_colors(fx.frames(src, size=(270, 480)), [hex2rgb(RED), hex2rgb(BLUE)], tol=60)])
    return [check("punch-in measured at 1.10 inside each window, 1.0 outside", abs(float(np.median(z[on])) - 1.10) < .01 and abs(float(np.median(z[~on])) - 1.0) < .005, [float(np.median(z[on])), float(np.median(z[~on]))], [1.10, 1.0]),
            check("every 4th beat (2.67 s at 90 bpm, inside the 2.5-4 s rule)", len(starts) == 3 and all(abs(b - a - per) < 1.5 / 30 for a, b in zip(starts, starts[1:])), [round(float(s), 3) for s in starts], [0, round(per, 3), round(2 * per, 3)]),
            check("each punch holds 1.2 s (1.0-1.5 s rule)", all(abs(r - 1.2) <= 1.5 / 30 for r in runs), runs, 1.2),
            check("zoompan rejects the 't' expression; 'it' renders 1080x1920 @30", (not broken_ok) and (int(p["width"]), int(p["height"])) == (W, H) and p["r_frame_rate"] == "30/1",
                  [broken_ok, p["width"], p["height"], p["r_frame_rate"]], [False, W, H, "30/1"]),
            check("negative control: the unprocessed plate shows no 1.10 punch", abs(float(still_d[0] / np.median(d[~on])) - 1.10) > .05, float(still_d[0] / np.median(d[~on])), "~1.0, not 1.10")], [out]


def _plate_js(plates):
    js = ""
    for k, (t0, t1, a) in enumerate(plates):
        js += ("tl.set('#p%d',{opacity:1},%s); tl.set('#p%d',{opacity:0},%s);"
               "tl.fromTo('#p%d .img',{scale:%s,x:%s,y:%s},{scale:%s,x:%s,y:%s,duration:%s,ease:E.dolly,immediateRender:false},%s);"
               % (k, t0, k, t1, k, a["from"], a["x0"], a["y0"], a["to"], a["x1"], a["y1"], t1 - t0, t0))
    return js + "gsap.set('.plate',{opacity:0}); gsap.set('#p0',{opacity:1});"


@card("CAM-151")
def cam151(task, wd):
    """Plates that arrive already moving: plate(id, t0, t1, {from, to, x0, x1, y0, y1}) - hard visibility cuts, the image
    scales from -> to over the whole hold on E.dolly (motion-kit), plates inset -4% so edges never show."""
    W, H = 320, 180
    plates = [(0.0, 1.5, dict(**{"from": 1.0, "to": 1.22}, x0=0, x1=0, y0=0, y1=40)),
              (1.5, 3.0, dict(**{"from": 1.18, "to": 1.02}, x0=0, x1=0, y0=0, y1=0)),
              (3.0, 4.5, dict(**{"from": 1.05, "to": 1.25}, x0=0, x1=0, y0=0, y1=0))]
    pairs = [(RED, BLUE), (GREEN, YEL), (MAG, CYAN)]
    body = "".join('<div class="plate a" id=p%d style="left:-4%%;top:-4%%;width:108%%;height:108%%"><div class="img a" style="inset:0;transform-origin:50%% 50%%">%s%s</div></div>'
                   % (k, box_html("m%da" % k, 120, 70, 12, 12, a), box_html("m%db" % k, 210, 110, 12, 12, b)) for k, (a, b) in enumerate(pairs))
    T = times_for(4.5 - 1 / 30, 30)
    sels = sum([["#m%da" % k, "#m%db" % k] for k in range(3)], []) + ["#p%d" % k for k in range(3)]
    cols = sum([list(p) for p in pairs], []) + [None] * 3

    def crits(r, T):
        f = r["frames"]

        def sc(k):
            i0, i1 = idx(T, plates[k][0]), idx(T, plates[k][1] - 1 / 30)
            d = [math.dist(np.array(f[i]["el"][2 * k]["q"]).mean(0), np.array(f[i]["el"][2 * k + 1]["q"]).mean(0)) for i in range(i0, i1 + 1)]
            mdl = [(plates[k][2]["from"] + (plates[k][2]["to"] - plates[k][2]["from"]) * EZ["dolly"]((T[i] - plates[k][0]) / (plates[k][1] - plates[k][0]))) / plates[k][2]["from"]
                   for i in range(i0, i1 + 1)]
            return maxerr([x / d[0] for x in d], mdl)

        def video_sc(k, mm):
            i0, i1 = idx(T, plates[k][0]), idx(T, plates[k][1] - 1 / 30)
            d = [math.hypot(mm[i][2 * k]["cx"] - mm[i][2 * k + 1]["cx"], mm[i][2 * k]["cy"] - mm[i][2 * k + 1]["cy"]) if mm[i][2 * k] and mm[i][2 * k + 1] else float("nan") for i in range(i0, i1 + 1)]
            return d[-1] / d[0]
        cover = lambda fr, k: (lambda q: q[0][0] <= 0 and q[0][1] <= 0 and q[2][0] >= W and q[2][1] >= H)(fr["el"][6 + k]["q"])
        vis = [[k for k in range(3) if fr["el"][6 + k]["o"] == 1] for fr in f]
        want = [[next(k for k, (a, b, _) in enumerate(plates) if a <= t < b)] for t in T]
        return [("measured plate scale (video) runs from -> to over each hold", lambda m, fr: (all(abs(video_sc(k, m) - plates[k][2]["to"] / plates[k][2]["from"]) < .01 for k in range(3)),
                                                                                      [round(video_sc(k, m), 4) for k in range(3)]), [round(p[2]["to"] / p[2]["from"], 4) for p in plates]),
                ("scale curve is E.dolly over the whole hold (browser quads)", lambda m, fr: (max(sc(k) for k in range(3)) < 1e-3, max(sc(k) for k in range(3))), "<1e-3"),
                ("hard cuts: exactly one plate visible per frame, switching at 1.5 s and 3.0 s", lambda m, fr: (vis == want, [vis[idx(T, t)] for t in (1.4, 1.5, 2.9, 3.0)]), [[0], [1], [1], [2]]),
                ("inset -4%: every visible plate covers the whole frame", lambda m, fr: (all(cover(fr_, v[0]) for fr_, v in zip(f, vis)), True), True)]
    return run_tl(wd, "plates", body, _plate_js(plates), sels, cols, 4.5 - 1 / 30, 30, crits)


@card("CAM-102")
def cam102(task, wd):
    """Full-screen motion with a shared background: a persistent full-bleed background child (the root has no fill)
    keeps drifting continuously through the scene swap while the foreground scenes cut."""
    body = ('<div id=root class=a style="inset:0"><div id=bg class=a style="inset:0;background:#777">%s</div>'
            '<div id=s1 class=a style="inset:0">%s</div><div id=s2 class=a style="inset:0;opacity:0">%s</div></div>'
            % (box_html("bm", 40, 140, 14, 14, GREEN), box_html("f1", 140, 60, 20, 20, RED), box_html("f2", 180, 80, 20, 20, BLUE)))
    js = ("tl.fromTo('#bm',{x:0},{x:60,duration:3,ease:'none',immediateRender:false},0); tl.set('#s1',{opacity:0},1.5); tl.set('#s2',{opacity:1},1.5);")
    xj = "t=>({root:getComputedStyle(document.getElementById('root')).backgroundColor, bg:getComputedStyle(document.getElementById('bg')).backgroundColor})"

    def crits(r, T):
        return [("background drifts continuously through the cut (20 px/s, linear)", lambda m, f: (lambda x: (abs(np.polyfit(T, x, 1)[0] - 20) < .05 and float(np.abs(x - np.polyval(np.polyfit(T, x, 1), T)).max()) < .05,
                                                                                                         float(np.polyfit(T, x, 1)[0])))(P(m, 0)[0]), 20),
                ("foreground scenes cut at 1.5 s (s1 before, s2 after)", lambda m, f: (all((m[i][1] is not None) == (t < 1.5) and (m[i][2] is not None) == (t >= 1.5) for i, t in enumerate(T)), True), True),
                ("fill lives on the full-bleed child, the root is transparent", lambda m, f: (f[0]["x"]["root"] == "rgba(0, 0, 0, 0)" and f[0]["x"]["bg"] == "rgb(119, 119, 119)", f[0]["x"]), ["rgba(0, 0, 0, 0)", "rgb(119, 119, 119)"])]
    return run_tl(wd, "sharedbg", body, js, ["#bm", "#f1", "#f2"], [GREEN, RED, BLUE], 3.0, 10, crits, extra_js=xj)


@card("CAM-121")
def cam121(task, wd):
    """Theme plate reactions applied to the composite (subject + text + plate move as one): a stomp punch 0.05 with
    decay and an 8x5 px shake at 12 Hz, an anchor dim 0.16 with pushIn 0.012 and grain 5; rendered with cv2 and measured."""
    import cv2
    W, H, fps, dur = 320, 180, 30, 3.0
    base = np.zeros((H, W, 3), np.float32) + 119
    base[40:60, 60:80] = hex2rgb(RED)                    # subject
    base[120:134, 220:250] = hex2rgb(BLUE)               # text
    base[100:116, 40:56] = hex2rgb(GREEN)                # plate detail
    theme = {"stomp": {"punch": .05, "punchDecay": .15, "shakeAmpX": 8, "shakeAmpY": 5, "shakeHz": 12, "shakeDecay": .3},
             "anchor": {"dim": .16, "pushIn": .012, "grain": 5}}
    events = [("stomp", .5, .5), ("anchor", 1.8, 1.2)]
    (wd / "theme.json").write_text(json.dumps({"plate": theme, "events": events}), encoding="utf-8")
    rng = np.random.default_rng(5)

    def react(t, on=True):
        s, dx, dy, dim, grain = 1.0, 0.0, 0.0, 0.0, 0.0
        for kind, t0, d in events:
            if not on or t < t0:
                continue
            u = t - t0
            th = theme[kind]
            if kind == "stomp":
                s *= 1 + th["punch"] * math.exp(-u / th["punchDecay"])
                e = math.exp(-u / th["shakeDecay"])
                dx += th["shakeAmpX"] * e * math.sin(2 * math.pi * th["shakeHz"] * u)
                dy += th["shakeAmpY"] * e * math.cos(2 * math.pi * th["shakeHz"] * u) if u > 0 else 0
            elif u <= d:
                s *= 1 + th["pushIn"] * u / d
                dim, grain = th["dim"], th["grain"]
        return s, dx, dy, dim, grain

    def render(on):
        frames = []
        for i in range(int(dur * fps)):
            t = i / fps
            s, dx, dy, dim, grain = react(t, on)
            M = np.float32([[s, 0, (1 - s) * W / 2 + dx], [0, s, (1 - s) * H / 2 + dy]])
            f = cv2.warpAffine(base, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE) * (1 - dim)
            if grain:
                f = f + rng.normal(0, grain, f.shape)
            frames.append(np.clip(f, 0, 255).astype(np.uint8))
        return frames
    vid = write_video(wd / "reactions.mp4", render(True), fps)
    inp = write_video(wd / "plate_input.mp4", render(False), fps)
    T = np.arange(int(dur * fps)) / fps

    def measure(v):
        fr = read_video(v)
        m = track_colors(fr, [hex2rgb(RED), (int(255 * .84), 0, 0), hex2rgb(BLUE), hex2rgb(GREEN)], tol=60)
        out = []
        for f, row in zip(fr, m):
            r = row[0] or row[1]
            out.append((r, row[2], row[3], f))
        return out
    ms = measure(vid)
    mi = measure(inp)
    dist = lambda a, b: math.hypot(a["cx"] - b["cx"], a["cy"] - b["cy"])
    d0 = dist(ms[0][0], ms[0][1])
    scale = np.array([dist(r, b) / d0 for r, b, g, f in ms])
    cov = track_colors(read_video(vid)[:int(1.8 * fps)], [hex2rgb(RED), hex2rgb(BLUE), hex2rgb(GREEN)], bg=GREY)   # grain-free part, sub-pixel
    rel = np.array([dist(r, g) / dist(cov[0][0], cov[0][2]) - dist(r, b) / dist(cov[0][0], cov[0][1]) for r, b, g in cov])
    model_s = np.array([react(t)[0] for t in T])
    cen = np.array([[(r["cx"] + b["cx"] + g["cx"]) / 3, (r["cy"] + b["cy"] + g["cy"]) / 3] for r, b, g, f in ms])
    shake = cen - cen[0]
    w = (T >= .5) & (T < 1.3)
    tt = T[w] - .5
    env = np.exp(-tt / .3)

    def fit(hz):
        A = np.stack([env * np.sin(2 * np.pi * hz * tt), env * np.cos(2 * np.pi * hz * tt)], 1)
        coef, res, *_ = np.linalg.lstsq(A, shake[w, 0] - shake[w, 0].mean() * 0, rcond=None)
        return float(np.sum((A @ coef - shake[w, 0]) ** 2)), coef
    hz = min(np.arange(6, 15.01, .25), key=lambda h: fit(h)[0])
    ampx = float(np.hypot(*fit(12)[1]))
    flat = lambda f: f[150:175, 120:200].astype(float)
    dim = float(flat(ms[int(2.4 * fps)][3]).mean() / flat(ms[int(.2 * fps)][3]).mean())
    grain = float(flat(ms[int(2.4 * fps)][3])[..., 1].std())
    s_in = np.array([dist(r, b) / dist(mi[0][0], mi[0][1]) for r, b, g, f in mi])
    return [check("stomp punch: measured scale 1.05 decaying (punchDecay 0.15 s) + anchor pushIn 1.2%", float(np.abs(scale - model_s).max()) < .004, [round(float(x), 4) for x in scale[12:24:3]], [round(float(x), 4) for x in model_s[12:24:3]]),
            check("shake: 12 Hz, 8 px horizontal amplitude", abs(hz - 12) < .3 and abs(ampx - 8) < .6, [float(hz), ampx], [12, 8]),
            check("anchor dim 0.16 and grain sigma 5 on the plate", abs(dim - .84) < .01 and abs(grain - 5) < .6, [dim, grain], [.84, 5]),
            check("subject, text and plate move as one through punch + shake (relative geometry kept)", float(np.abs(rel).max()) < .004, float(np.abs(rel).max()), "<0.004"),
            check("negative control: the unprocessed plate does not react", not float(np.abs(s_in - model_s).max()) < .004, float(np.abs(s_in - model_s).max()), ">=0.004")], [vid, wd / "theme.json"]


# ───────────────────────────── beat motion primitives anchored to an audiomap measured from a music fixture ─────────────────────────────

MUSIC_TRUE = {"beats": [round(0.25 + 0.5 * k, 3) for k in range(12)], "build": (1.25, 2.75), "crash": 2.75, "drop": 3.75}


def music_fixture(path, sr=22050, dur=6.0):
    """A synthetic track with known events: kicks on every beat (120 bpm), a 1.5 s noise build, a crash, a drop."""
    import wave
    t = np.arange(int(dur * sr)) / sr
    rng = np.random.default_rng(1)
    y = np.zeros_like(t)
    for b in MUSIC_TRUE["beats"]:
        u = np.clip(t - b, 0, None)
        on = t >= b
        y += on * 0.6 * np.sin(2 * np.pi * (55 * u + 60 * 0.03 * (1 - np.exp(-u / 0.03)))) * np.exp(-u / 0.08)
    b0, b1 = MUSIC_TRUE["build"]
    ramp = np.clip((t - b0) / (b1 - b0), 0, 1) * ((t >= b0) & (t < b1))
    y += 0.35 * ramp * rng.normal(0, 1, len(t)) * 0.5
    c = MUSIC_TRUE["crash"]
    hp = np.diff(rng.normal(0, 1, len(t) + 2), 2) / 2
    y += (t >= c) * 0.2 * hp * np.exp(-np.clip(t - c, 0, None) / 0.6)
    d = MUSIC_TRUE["drop"]
    y += (t >= d) * 0.3 * rng.normal(0, 1, len(t))
    y = y / np.abs(y).max() * 0.9
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1), w.setsampwidth(2), w.setframerate(sr)
        w.writeframes((y * 32767).astype(np.int16).tobytes())
    return Path(path)


def audiomap(path):
    """Detect events from the audio alone: kicks (low-band spectral flux), drop (largest loudness jump), crash (the
    other big high-band onset), build (longest sustained rise of 1-5 kHz energy), phrase (every 8th beat), reveal (end of build)."""
    import wave
    with wave.open(str(path)) as w:
        sr = w.getframerate()
        y = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768
    hop, win = 256, 1024
    n = 1 + (len(y) - win) // hop
    fr = np.stack([y[i * hop:i * hop + win] * np.hanning(win) for i in range(n)])
    S = np.abs(np.fft.rfft(fr, axis=1))
    f = np.fft.rfftfreq(win, 1 / sr)
    tt = (np.arange(n) * hop + win / 2) / sr
    band = lambda lo, hi: np.log1p(S[:, (f >= lo) & (f < hi)].sum(1))
    lin = lambda lo, hi: (S[:, (f >= lo) & (f < hi)] ** 2).sum(1)

    def peaks(flux, thr, gap):
        out = []
        for i in range(1, len(flux) - 1):
            if flux[i] > thr and flux[i] >= flux[i - 1] and flux[i] >= flux[i + 1] and (not out or tt[i] - out[-1] > gap):
                out.append(tt[i])
        return out
    onset_t = lambda i: tt[i]                               # the flux peaks when the onset reaches the window centre
    low = lin(20, 150)
    fl = np.maximum(np.diff(low, prepend=low[0]), 0)
    kicks = [round(float(onset_t(int(np.argmin(np.abs(tt - k))))), 3) for k in peaks(fl, 0.5 * fl.max(), 0.2)]
    rms = np.sqrt((fr ** 2).mean(1))
    sm = np.convolve(rms, np.ones(8) / 8, "same")
    jump = np.r_[sm[8:] - sm[:-8], np.zeros(8)]
    drop = float(onset_t(int(np.argmax(jump)) + 4))
    hi = lin(5000, 11000)
    fh = np.maximum(np.diff(hi, prepend=hi[0]), 0)
    hp = sorted(peaks(fh, 0.4 * fh.max(), 0.3), key=lambda x: -fh[int(np.argmin(np.abs(tt - x)))])
    crash = next(float(onset_t(int(np.argmin(np.abs(tt - x))))) for x in hp if abs(x - drop) > 0.2)
    mid = np.convolve(band(1000, 5000), np.ones(17) / 17, "same")
    rising = np.diff(mid, prepend=mid[0]) > 0
    best, cur = (0, 0), None
    for i, r_ in enumerate(rising):
        if r_ and cur is None:
            cur = i
        if (not r_ or i == len(rising) - 1) and cur is not None:
            if tt[i] - tt[cur] > tt[best[1]] - tt[best[0]]:
                best = (cur, i)
            cur = None
    half = 8 * hop / sr                                     # the 17-frame smoothing starts the rise half a window early
    build = (round(float(tt[best[0]] + half), 3), round(float(crash), 3))
    return {"beats": kicks, "drop": round(drop, 3), "crash": round(crash, 3), "build": build, "reveal": round(crash, 3), "phrase": kicks[0::8]}


def _beat_card(wd, name, anchors, js_of, sels, colors, dur, crits_of, fps=30, extra_js="null", body=None):
    wav = music_fixture(wd / "music.wav")
    am = audiomap(wav)
    (wd / "audiomap.json").write_text(json.dumps(am), encoding="utf-8")
    det_ok = (all(abs(a - b) < 0.03 for a, b in zip(am["beats"], MUSIC_TRUE["beats"])) and len(am["beats"]) == 12
              and abs(am["drop"] - MUSIC_TRUE["drop"]) < 0.05 and abs(am["crash"] - MUSIC_TRUE["crash"]) < 0.05 and abs(am["build"][0] - MUSIC_TRUE["build"][0]) < 0.12)
    checks, outs = run_tl(wd, name, body or STAGE, js_of(am), sels, colors, dur, fps, lambda r, T: crits_of(r, T, am), extra_js=extra_js)
    checks.insert(0, check("audiomap detects the fixture's events from the audio (beats, drop, crash, build)", det_ok,
                           {k: am[k] for k in ("drop", "crash", "build")} | {"beats": am["beats"][:4]}, {k: MUSIC_TRUE[k] for k in ("drop", "crash", "build")}))
    return checks, outs + [wav, wd / "audiomap.json"]


def _first_move(series, thr, T, after=0.0):
    for i, v in enumerate(series):
        if T[i] >= after - 1e-9 and v > thr:
            return T[i]
    return None


SHAKE_JS = ("function shakeAt(t0,span,amp){ const n=Math.round(span*30); for(let i=0;i<=n;i++){ const u=i/30, e=Math.pow(1-u/span,2);"
            "tl.set('#stage',{x:i<n?amp*e*Math.sin(97.3*(u+t0)):0, y:i<n?amp*0.6*e*Math.cos(61.7*(u+t0)):0}, t0+u); } }")


@card("CAM-123")
def cam123(task, wd):
    """Beat motion primitive screen-shake anchored to music events: the audiomap (measured from the track) gives the crash
    and the drop, each fires a 0.35 s decaying jitter (best span 0.1-0.5 s) of the whole stage."""
    span = 0.35

    def js(am):
        return SHAKE_JS + "shakeAt(%s,%s,6); shakeAt(%s,%s,6);" % (am["crash"], span, am["drop"], span)

    def crits(r, T, am):
        def disp(m):
            x, y = P(m, 0)
            return np.hypot(x - x[0], y - y[0])
        def runs(d):
            on = d > 0.3
            out = []
            for i in range(len(on)):
                if on[i] and (i == 0 or not on[i - 1]):
                    j = i
                    while j < len(on) and on[j]:
                        j += 1
                    out.append([T[i], T[j - 1] - T[i] + 1 / 30])
            merged = []
            for st, d in out:                              # a zero crossing inside one shake is not a new shake
                if merged and st - (merged[-1][0] + merged[-1][1]) < .1:
                    merged[-1][1] = st + d - merged[-1][0]
                else:
                    merged.append([st, d])
            return merged
        return [("shakes start on the true crash and drop (within 2 frames)", lambda m, f: ((lambda rr: len(rr) == 2 and abs(rr[0][0] - MUSIC_TRUE["crash"]) <= 2 / 30 + .02 and abs(rr[1][0] - MUSIC_TRUE["drop"]) <= 2 / 30 + .02)(runs(disp(m))),
                                                                                       [round(a, 3) for a, _ in runs(disp(m))]), [MUSIC_TRUE["crash"], MUSIC_TRUE["drop"]]),
                ("each shake lasts inside the best span 0.1-0.5 s", lambda m, f: (all(0.1 <= d <= 0.5 for _, d in runs(disp(m))), [round(d, 3) for _, d in runs(disp(m))]), "0.1-0.5"),
                ("still between the events", lambda m, f: (float(disp(m)[[i for i, t in enumerate(T) if t < am["crash"] - .05 or am["crash"] + .45 < t < am["drop"] - .05]].max()) < .3, True), "<0.3 px")]
    return _beat_card(wd, "shake_beats", None, js, ["#mk"], [RED], 4.8, crits)


@card("CAM-124")
def cam124(task, wd):
    """Beat motion primitive dolly-zoom anchored to the build: over the detected build (best span 1.2-2.5 s) the subject
    keeps its size while the background scales 1 -> 1.5 (vertigo: dolly against zoom)."""
    body = ('<div id=bg class=a style="left:0;top:0;width:320px;height:180px;transform-origin:50%% 50%%">%s%s</div>%s'
            % (box_html("b1", 60, 40, 10, 10, BLUE), box_html("b2", 250, 130, 10, 10, GREEN), box_html("fg", 150, 80, 20, 20, RED)))

    def js(am):
        a, b = am["build"]
        return "tl.fromTo('#bg',{scale:1},{scale:1.5,duration:%s,ease:'sine.inOut',immediateRender:false},%s);" % (b - a, a)

    def crits(r, T, am):
        bgs = lambda m: D(m, 1, 2)
        return [("background zoom starts on the true build onset (within 0.15 s) and spans 1.2-2.5 s", lambda m, f: ((lambda s: (lambda st: st is not None and abs(st - MUSIC_TRUE["build"][0]) < .15)(_first_move(np.abs(s - 1), .002, T))
                                                                                                                   and 1.2 <= am["build"][1] - am["build"][0] <= 2.5)(bgs(m)), [_first_move(np.abs(bgs(m) - 1), .002, T), am["build"]]), MUSIC_TRUE["build"]),
                ("background grows to 1.5x", lambda m, f: (abs(bgs(m)[-1] - 1.5) < .01, float(bgs(m)[-1])), 1.5),
                ("the subject keeps its size (vertigo)", lambda m, f: (float(np.abs(SC(m, 0) - 1).max()) < .01, float(np.abs(SC(m, 0) - 1).max())), "<0.01")]
    return _beat_card(wd, "dollyzoom", None, js, ["#fg", "#b1", "#b2"], [RED, BLUE, GREEN], 4.0, crits, body=body)


@card("CAM-125")
def cam125(task, wd):
    """Beat motion primitive crash-zoom-in anchored to the drop: a violent 1 -> 1.8 zoom in 0.35 s (power4.in, best span
    0.2-0.8 s) fired at the detected drop."""
    def js(am):
        return "tl.fromTo('#stage',{scale:1},{scale:1.8,duration:.35,ease:'power4.in',immediateRender:false},%s);" % am["drop"]

    def crits(r, T, am):
        s = lambda m: D(m, 0, 1)
        return [("zoom starts on the true drop (within 2 frames)", lambda m, f: ((lambda st: st is not None and abs(st - MUSIC_TRUE["drop"]) <= 2 / 30 + .02)(_first_move(np.abs(s(m) - 1), .002, T)), _first_move(np.abs(s(m) - 1), .002, T)), MUSIC_TRUE["drop"]),
                ("reaches 1.8x within 0.2-0.8 s, accelerating (power4.in)", lambda m, f: ((lambda x: abs(x[-1] - 1.8) < .01 and (lambda i0: x[i0 + 9] - x[i0 + 8] > 4 * (x[i0 + 3] - x[i0 + 2]))(idx(T, am["drop"])))(s(m)), float(s(m)[-1])), 1.8)]
    return _beat_card(wd, "crashzoom", None, js, ["#mk", "#mb"], [RED, BLUE], 4.4, crits)


@card("CAM-126")
def cam126(task, wd):
    """Beat motion primitive mosaic-pack anchored to beats from the build: six scattered tiles fly in one per detected
    beat (0.5 s flights) and pack into a 3x2 grid; whole move inside the best span 1.5-3.5 s."""
    cols = [RED, BLUE, GREEN, YEL, MAG, CYAN]
    slots = [(100 + 44 * (k % 3), 50 + 44 * (k // 3)) for k in range(6)]
    scat_abs = [(10, 10), (270, 8), (12, 130), (272, 135), (140, 140), (60, 70)]          # scattered, inside the frame
    scat = [(ax - sx, ay - sy) for (ax, ay), (sx, sy) in zip(scat_abs, slots)]
    body = "".join(box_html("t%d" % k, x, y, 36, 36, c) for k, ((x, y), c) in enumerate(zip(slots, cols)))

    def js(am):
        beats = [b for b in am["beats"] if b >= am["build"][0] - .05][:6]
        return "".join("gsap.set('#t%d',{x:%d,y:%d}); tl.fromTo('#t%d',{x:%d,y:%d},{x:0,y:0,duration:.5,ease:'power3.out',immediateRender:false},%s);"
                       % (k, sx, sy, k, sx, sy, b) for k, ((sx, sy), b) in enumerate(zip(scat, beats)))

    def crits(r, T, am):
        true_b = [b for b in MUSIC_TRUE["beats"] if b >= MUSIC_TRUE["build"][0] - .05][:6]

        def starts(m):
            out = []
            for k in range(6):
                x, y = P(m, k)
                d = np.hypot(x - x[0], y - y[0])
                out.append(_first_move(d, .3, T))
            return out
        land = lambda m: [(P(m, k)[0][-1] - (slots[k][0] + 18), P(m, k)[1][-1] - (slots[k][1] + 18)) for k in range(6)]
        return [("each tile leaves on its beat (true beats, within 2 frames)", lambda m, f: (all(s is not None and abs(s - b) <= 2 / 30 + .02 for s, b in zip(starts(m), true_b)), starts(m)), true_b),
                ("tiles pack into the 3x2 grid", lambda m, f: (max(abs(v) for xy in land(m) for v in xy) < .2, max(abs(v) for xy in land(m) for v in xy)), "<0.2 px"),
                ("whole move inside the best span 1.5-3.5 s", lambda m, f: (1.5 <= true_b[-1] + .5 - true_b[0] <= 3.5, true_b[-1] + .5 - true_b[0]), "1.5-3.5")]
    return _beat_card(wd, "mosaicpack", None, js, ["#t%d" % k for k in range(6)], cols, 5.0, crits, body=body)


@card("CAM-127")
def cam127(task, wd):
    """Beat motion primitive tile-mosaic anchored to the reveal: a diagonal sweep (order i + j, 0.25 s apart) assembles a
    4x3 poster from tiles starting at the detected end of the build (best span 1.5-3.5 s)."""
    cols = [RED, BLUE, GREEN, YEL, MAG, CYAN]
    tiles = [(i, j) for j in range(3) for i in range(4)]
    track = [0, 5, 10, 11]                                 # tiles (0,0), (1,1), (2,2), (3,2) carry markers
    body = "".join('<div id=t%d class=a style="left:%dpx;top:%dpx;width:60px;height:46px;opacity:0;background:%s"></div>'
                   % (k, 40 + 61 * i, 20 + 47 * j, cols[track.index(k)] if k in track else "#999") for k, (i, j) in enumerate(tiles))

    def js(am):
        return "".join("tl.fromTo('#t%d',{opacity:0},{opacity:1,duration:.5,ease:'none',immediateRender:false},%s);" % (k, am["reveal"] + .25 * (i + j))
                       for k, (i, j) in enumerate(tiles))

    def crits(r, T, am):
        f = r["frames"]
        order = track + [k for k in range(12) if k not in track]       # sampled element order
        on = lambda k, fr: next((T[n] for n, x in enumerate(fr) if x["el"][order.index(k)]["o"] > 0.01), None)
        appear = lambda m: [next((T[n] for n, row in enumerate(m) if row[q] and row[q]["area"] > .5 * 60 * 46), None) for q in range(4)]
        want = [MUSIC_TRUE["build"][1] + .25 * (tiles[k][0] + tiles[k][1]) + .25 for k in track]     # half opacity after 0.25 s
        return [("tiles appear in diagonal order i + j, 0.25 s apart, from the true reveal (video, within 3 frames)", lambda m, fr: (all(a is not None and abs(a - w) <= 3 / 30 + .02 for a, w in zip(appear(m), want)), appear(m)), want),
                ("every tile follows the diagonal rule (browser opacities)", lambda m, fr: (all(abs(on(k, f) - (am["reveal"] + .25 * (i + j))) <= 1 / 30 + .011 for k, (i, j) in enumerate(tiles)), True), True),
                ("the poster assembles within the best span 1.5-3.5 s", lambda m, fr: (1.5 <= .25 * 5 + .5 <= 3.5 and all(f[-1]["el"][k]["o"] == 1 for k in range(12)), .25 * 5 + .5), "1.5-3.5, all tiles on")]
    return _beat_card(wd, "tilemosaic", None, js, ["#t%d" % k for k in track] + ["#t%d" % k for k in range(12) if k not in track], [cols[q] for q in range(4)] + [None] * 8, 5.0, crits, body=body)


# ───────────────────────────── previs: prompt camera plans executed as K3 (THREE) camera moves and measured ─────────────────────────────

def _forge():
    return repo_mod(FORGE / "video_prompt_forge.py", "forge")


def cam_words(text):
    F = _forge()
    return [w for w in re.findall(F.CAMERA_WORDS, text.lower()) if w not in ("static", "locked-off", "locked off")]


def _in_frame(b, W, H):
    return b is not None and b["x0"] > 0 and b["y0"] > 0 and b["x1"] < W - 1 and b["y1"] < H - 1


STICK5 = [(0, 0.06, 0, 0.06, RED), (0, 1.75, 0, 0.09, BLUE), (-1.4, 1.45, 2.3, 0.22, GREEN)]


@card("CAM-05")
def cam05(task, wd):
    """Stickman shot-size progression: five clips escalate with the arc - wide establishing, medium eye level,
    over-the-shoulder three-quarter, slightly low angle, close-up with a very slow push-in; 9:16, steady camera with a
    subtle horizontal follow; executed as a K3 camera plan and measured."""
    W, H = 144, 256
    shots = [("wide establishing", [0, 1.6, 9], [0, .9, 0]), ("medium eye level", [0, 1.6, 3.2], [0, 1.4, 0]),
             ("over-the-shoulder three-quarter", [-2.2, 1.65, 3.2], [0, 1.5, 0]), ("slightly low angle", [.5, .8, 3.5], [0, 1.3, 0]),
             ("close-up on posture, room for the reveal", [0, 1.55, 1.6], [0, 1.45, 0])]
    prompts = [{"clip": i + 1, "shot": s[0], "camera": "very slow push-in" if i == 4 else "steady with subtle horizontal follow", "aspect": "9:16"} for i, s in enumerate(shots)]
    (wd / "shots.json").write_text(json.dumps(prompts, indent=1), encoding="utf-8")
    js = ("const SH=%s; function update(t){ const k=Math.min(4,Math.floor(t/2)), u=t-2*k; const s=SH[k]; const walk=k<4?0.15*u:0;"
          "const p=s[1].slice(), l=s[2].slice(); p[0]+=0.8*walk; l[0]+=walk; if(k===4){ p[2]=1.6-0.14*u/2; }"
          "camera.position.set(p[0],p[1],p[2]); camera.lookAt(l[0],l[1],l[2]); return {k, look:l}; }") % json.dumps(shots)
    js = js.replace("function update(t){", "function update(t){ const sx=(Math.min(4,Math.floor(t/2))<4)?0.15*(t-2*Math.min(4,Math.floor(t/2))):0; PTS[0][0]=sx; PTS[1][0]=sx;")

    def crits(r, T):
        mid = [idx(T, 2 * k + 1) for k in range(5)]
        head = lambda m, k: rad(m, 1)[mid[k]]
        return [("shot sizes escalate: head size wide < medium < close-up, close-up the largest", lambda m, f: (head(m, 0) < head(m, 1) < head(m, 4) and head(m, 4) == np.nanmax([head(m, k) for k in range(5)]),
                                                                                                  [round(float(head(m, k)), 2) for k in range(5)]), "increasing to the close-up"),
                ("wide: full figure in frame and < 45% of the height", lambda m, f: (m[mid[0]][0] is not None and _in_frame(m[mid[0]][1], W, H) and (m[mid[0]][0]["cy"] - m[mid[0]][1]["cy"]) / H < .45,
                                                                                (m[mid[0]][0]["cy"] - m[mid[0]][1]["cy"]) / H if m[mid[0]][0] else None), "<0.45"),
                ("medium at eye level: camera y 1.6, feet out of frame", lambda m, f: (abs(f[mid[1]]["pos"][1] - 1.6) < 1e-6 and m[mid[1]][0] is None and m[mid[1]][1] is not None, f[mid[1]]["pos"][1]), 1.6),
                ("over-the-shoulder: foreground shoulder bigger than the subject's head, camera 30-45 deg off the front", lambda m, f: (m[mid[2]][2] is not None and rad(m, 2)[mid[2]] > 2 * rad(m, 1)[mid[2]]
                                                                                                                          and 30 <= abs(math.degrees(math.atan2(f[mid[2]]["pos"][0], f[mid[2]]["pos"][2]))) <= 45,
                                                                                                                          abs(math.degrees(math.atan2(f[mid[2]]["pos"][0], f[mid[2]]["pos"][2])))), "30-45 deg"),
                ("slightly low angle: camera below the chest looking up", lambda m, f: (f[mid[3]]["pos"][1] < 1.0 and f[mid[3]]["x"]["look"][1] > f[mid[3]]["pos"][1], [f[mid[3]]["pos"][1], f[mid[3]]["x"]["look"][1]]), "y<1, looking up"),
                ("close-up: very slow push-in (head grows 2-15%), steady elsewhere (camera height constant within each clip)", lambda m, f: (1.02 < rad(m, 1)[idx(T, 9.9)] / rad(m, 1)[idx(T, 8.0)] < 1.15
                                                                                                                                 and all(np.ptp([f[i]["pos"][1] for i in range(len(T)) if 2 * k <= T[i] < 2 * k + 2]) < 1e-9 for k in range(5)),
                                                                                                                                 float(rad(m, 1)[idx(T, 9.9)] / rad(m, 1)[idx(T, 8.0)])), "1.02-1.15"),
                ("subtle horizontal follow: the walking subject stays near its screen x within a clip", lambda m, f: (max(abs(m[idx(T, 2 * k + 1.9)][1]["cx"] - m[idx(T, 2 * k)][1]["cx"]) for k in range(4)) < .06 * W,
                                                                                                                 max(abs(m[idx(T, 2 * k + 1.9)][1]["cx"] - m[idx(T, 2 * k)][1]["cx"]) for k in range(4))), "<6% of W")]
    checks, outs = run3d(wd, "stickman", STICK5, js, 9.9, 10, crits, W=W, H=H, fov=40)
    return checks, outs + [wd / "shots.json"]


def fov_v(mm, sensor=36.0):
    return 2 * math.degrees(math.atan(sensor / 2 / mm))


@card("CAM-06")
def cam06(task, wd):
    """Two-lens emotional coverage: every story beat is covered twice in 9:16 - a 35 mm wide with layered depth
    (foreground / subject / background in frame) and an 85 mm close-up on hands, posture or eyes; vertical fov from
    the focal length on a 36 mm portrait sensor."""
    W, H = 144, 256
    pts = [(0, 1.6, 0, .09, BLUE), (.22, 1.05, .25, .07, RED), (0, 1.3, .1, .08, MAG), (-.45, .9, 2.6, .12, GREEN), (1.3, 1.8, -6, .5, YEL)]
    targets = [[.22, 1.05, .25], [0, 1.3, .1], [0, 1.6, 0]]          # hands, posture, eyes
    plan = [{"beat": b, "j": j, "lens": ("35 mm wide" if j == 0 else "85 mm close-up"), "aspect": "9:16"} for b in range(3) for j in range(2)]
    (wd / "coverage.json").write_text(json.dumps(plan, indent=1), encoding="utf-8")
    js = ("const TG=%s, F35=%s, F85=%s; function update(t){ const n=Math.round(t), b=Math.floor(n/2), j=n%%2;"
          "if(j===0){ camera.fov=F35; camera.position.set(0.4,1.5,4.6); camera.lookAt(0,1.4,0); }"
          "else { const g=TG[b]; camera.fov=F85; camera.position.set(g[0]+0.15,g[1]+0.05,g[2]+1.25); camera.lookAt(g[0],g[1],g[2]); }"
          "return {b,j}; }") % (json.dumps(targets), fov_v(35), fov_v(85))
    T = [float(i) for i in range(6)]
    col = {BLUE: 0, RED: 1, MAG: 2, GREEN: 3, YEL: 4}
    tk = [1, 2, 0]

    def crits(r, T):
        f = r["frames"]
        return [("the 85 mm close-up magnifies its target >= 3x over the 35 mm wide of the same beat", lambda m, fr: (all(m[2 * b + 1][tk[b]] is not None and m[2 * b][tk[b]] is not None and rad(m, tk[b])[2 * b + 1] > 3 * rad(m, tk[b])[2 * b] for b in range(3)),
                                                                                                         [round(float(rad(m, tk[b])[2 * b + 1] / rad(m, tk[b])[2 * b]), 2) if m[2 * b + 1][tk[b]] else None for b in range(3)]), ">3"),
                ("fov = 2 atan(18 / f): 35 mm -> %.2f deg, 85 mm -> %.2f deg" % (fov_v(35), fov_v(85)), lambda m, fr: (all(abs(f[i]["fov"] - (fov_v(35) if i % 2 == 0 else fov_v(85))) < 1e-6 for i in range(6)), [f[0]["fov"], f[1]["fov"]]), [fov_v(35), fov_v(85)]),
                ("35 mm frames hold layered depth: foreground, subject and background all in frame", lambda m, fr: (all(m[2 * b][3] is not None and m[2 * b][0] is not None and m[2 * b][4] is not None for b in range(3)), True), True),
                ("close-ups on hands, posture, eyes in turn", lambda m, fr: (all(abs(m[2 * b + 1][tk[b]]["cx"] - W / 2) < 12 and abs(m[2 * b + 1][tk[b]]["cy"] - H / 2) < 12 for b in range(3)), [(round(m[2 * b + 1][tk[b]]["cx"]), round(m[2 * b + 1][tk[b]]["cy"])) for b in range(3)]), "centred")]
    r = cam3d(wd, "twolens", pts, js, T, 1, W=W, H=H, fov=40)
    return verify(r, crits(r, T)), out_files(r["video"], r["json"]) + [wd / "coverage.json"]


@card("CAM-07")
def cam07(task, wd):
    """Locked 45 deg food macro: a fixed tripod three-quarter view at 45 deg elevation with a 50 mm look (fov 27 deg on a
    24 mm-high frame), identical in every clip, allowing only a tiny motivated macro push (<= 3%) in one clip."""
    W, H = 256, 144
    pts = [(0, .05, 0, .12, RED), (.25, .05, -.15, .06, BLUE), (-.3, .05, .2, .05, GREEN)]
    d = 1.2
    el, az = math.radians(45), math.radians(45)
    cpos = [d * math.cos(el) * math.sin(az), .05 + d * math.sin(el), d * math.cos(el) * math.cos(az)]
    js = ("const C=%s; function update(t){ const k=Math.floor(t/2), u=t-2*k; const s=(k===1)?1-0.025*Math.min(1,u/1.5):1;"
          "camera.fov=%s; camera.position.set(C[0]*s,0.05+(C[1]-0.05)*s,C[2]*s); camera.lookAt(0,0.05,0); return {k}; }") % (json.dumps(cpos), fov_v(50, 24))

    def crits(r, T):
        f = r["frames"]
        starts = [idx(T, 2 * k) for k in range(3)]
        sc = lambda m, a, b: rad(m, 0)[b] / rad(m, 0)[a]
        return [("clip 2 has the one motivated macro push: 1-3% measured", lambda m, fr: (1.01 < sc(m, starts[1], idx(T, 3.9)) <= 1.03 and abs(sc(m, starts[0], idx(T, 1.9)) - 1) < 1e-3 and abs(sc(m, starts[2], idx(T, 5.9)) - 1) < 1e-3,
                                                                                    [round(float(sc(m, starts[k], idx(T, 2 * k + 1.9))), 4) for k in range(3)]), [1, "1.01-1.03", 1]),
                ("identical camera at the start of every clip (measured plate)", lambda m, fr: (all(abs(m[s][0]["cx"] - m[0][0]["cx"]) < 1e-6 and abs(m[s][0]["area"] - m[0][0]["area"]) < 1e-6 for s in starts), True), True),
                ("45 deg elevation, three-quarter (45 deg) azimuth, 50 mm look", lambda m, fr: (abs(math.degrees(math.atan2(f[0]["pos"][1] - .05, math.hypot(f[0]["pos"][0], f[0]["pos"][2]))) - 45) < 1e-6
                                                                                         and abs(math.degrees(math.atan2(f[0]["pos"][0], f[0]["pos"][2])) - 45) < 1e-6 and abs(f[0]["fov"] - fov_v(50, 24)) < 1e-6, f[0]["fov"]), [45, 45, round(fov_v(50, 24), 3)])]
    return run3d(wd, "foodmacro", pts, js, 5.9, 10, crits, W=W, H=H)


@card("CAM-185")
def cam185(task, wd):
    """First-frame framing per segment (not camera motion): every UGC segment opens 'medium shot chest-up, eye level'
    unless a progression is asked for (wide -> medium close-up -> face close-up); action lines replace lens moves.
    The plan's opening frames are executed as K3 cameras and the visible body markers measured."""
    W, H = 144, 256
    body = [(0, .05, 0, .05, RED), (0, 1.0, 0, .05, GREEN), (0, 1.3, 0, .05, YEL), (0, 1.55, 0, .05, MAG), (0, 1.8, 0, .05, BLUE)]
    span = {"medium shot chest-up, eye level": (1.15, 1.95), "wide": (-.25, 2.2), "medium close-up": (1.38, 1.93), "face close-up": (1.48, 1.88)}
    actions = ["turns toward camera", "holds up the bottle", "smiles and nods", "points at the label"]
    default = [{"segment": i + 1, "framing": "medium shot chest-up, eye level", "action": a} for i, a in enumerate(actions)]
    prog = [{"segment": i + 1, "framing": fr_, "action": a} for i, (fr_, a) in enumerate(zip(["wide", "medium close-up", "face close-up", "face close-up"], actions))]
    naive = ["camera zooms in on her face", "slow dolly out to reveal the room", "orbit around the product", "handheld push-in"]
    (wd / "segments.json").write_text(json.dumps({"default": default, "on_request": prog}, indent=1), encoding="utf-8")
    fv = 40

    def cam_for(fr_):
        lo, hi = span[fr_]
        dist = (hi - lo) / 2 / math.tan(math.radians(fv) / 2)
        return [0, 1.6, dist], [0, (lo + hi) / 2, 0]
    shots = [cam_for(s["framing"]) for s in default + prog]
    js = "const S=%s; function update(t){ const s=S[Math.round(t)]; camera.position.set(...s[0]); camera.lookAt(...s[1]); }" % json.dumps(shots)
    r = cam3d(wd, "firstframes", body, js, [float(i) for i in range(8)], 1, W=W, H=H, fov=fv)
    vis = [[k for k in range(5) if r["meas"][i][k] is not None and _in_frame(r["meas"][i][k], W, H)] for i in range(8)]
    fr = read_video(r["video"])
    same = float(max(np.abs(fr[i] - fr[0]).max() for i in range(4)))
    words_default = [w for s in default for w in cam_words(s["action"] + " " + s["framing"])]
    words_naive = [w for s in naive for w in cam_words(s)]
    return [check("default: all 4 segments open on the identical chest-up, eye-level frame (chest, chin, head in; hip out)", same < 1 and all(v == [2, 3, 4] for v in vis[:4]) and all(abs(shots[i][0][1] - 1.6) < 1e-9 for i in range(4)),
                  [same, vis[:4]], [0, [[2, 3, 4]] * 4]),
            check("on request the openings tighten: wide (feet in) -> medium close-up (chest out) -> face close-up (chin in, chest out)", vis[4][0] == 0 and 2 not in vis[5] and 3 in vis[5] and 3 in vis[6] and 2 not in vis[6]
                  and rad(r["meas"], 4)[6] > rad(r["meas"], 4)[5] > rad(r["meas"], 4)[4], vis[4:7], "progression"),
            check("action lines, no lens moves, in the default prompts", not words_default, words_default, []),
            check("negative control: the unprocessed lens-move prompts name camera moves", bool(words_naive), words_naive, "camera words")], [wd / "segments.json", r["video"], r["json"]]


MOVE_LIBRARY = {"luxury product": "slow half-orbit around hero object", "real estate": "steadicam glide through doorways, crane-up in atria",
                "industrial": "low lateral track with foreground parallax", "travel": "drone rise-and-reveal then descending swoop",
                "food/craft": "push in to craft moment, ease back", "miniature": "dives + aerial hops", "locked-iso": "locked high isometric angle, straight level travel only"}


def _grammar(wd, name, concept, pts, js, dur, fps, crits, W=256, H=144, fov=40):
    leg = {"concept": concept, "leg": "mid-leg", "prompt": "%s scene, %s" % (concept, MOVE_LIBRARY[concept]), "camera": MOVE_LIBRARY[concept]}
    (wd / ("%s_leg.json" % name)).write_text(json.dumps(leg, indent=1), encoding="utf-8")
    checks, outs = run3d(wd, name, pts, js, dur, fps, crits, W=W, H=H, fov=fov)
    checks.insert(0, check("leg prompt carries the concept's move from the library", MOVE_LIBRARY[concept] in leg["prompt"], leg["camera"], MOVE_LIBRARY[concept]))
    return checks, outs + [wd / ("%s_leg.json" % name)]


@card("CAM-187")
def cam187(task, wd):
    """Camera grammar, luxury product: the library's 'slow half-orbit around hero object' added to the leg prompt and
    executed as a previs camera (radius 4, sine ease over 4 s); hero stays centred, the orbit sweeps 180 deg."""
    pts = [(0, 1, 0, .3, RED), (.9, 1.8, -.6, .12, BLUE)]
    js = "function update(t){ const a=Math.PI*(1-Math.cos(Math.PI*Math.min(t/4,1)))/2; camera.position.set(4*Math.sin(a),1.3,4*Math.cos(a)); camera.lookAt(0,1,0); return {a}; }"

    def crits(r, T):
        f = r["frames"]
        az = [math.degrees(math.atan2(fr["pos"][0], fr["pos"][2])) % 360 for fr in f]
        return [("the side detail swings across the hero (orbit parallax, measured)", lambda m, fr: (np.sign(P(m, 1)[0][0] - P(m, 0)[0][0]) != np.sign(P(m, 1)[0][-1] - P(m, 0)[0][-1]), [float(P(m, 1)[0][0]), float(P(m, 1)[0][-1])]), "sign flip"),
                ("hero stays centred all the way (measured)", lambda m, fr: (float(np.nanmax(np.hypot(P(m, 0)[0] - 128, P(m, 0)[1] - 72))) < .5, float(np.nanmax(np.hypot(P(m, 0)[0] - 128, P(m, 0)[1] - 72)))), "<0.5 px"),
                ("half-orbit: azimuth sweeps 180 deg at constant radius", lambda m, fr: (abs((az[-1] - az[0]) - 180) < 1e-6 and np.ptp([math.hypot(x["pos"][0], x["pos"][2]) for x in f]) < 1e-9, az[-1] - az[0]), 180),
                ("slow: zero speed at both ends (sine ease)", lambda m, fr: (abs(az[1] - az[0]) < 1.5 and abs(az[-1] - az[-2]) < 1.5 and az[21] - az[19] > 5, [az[1] - az[0], az[21] - az[19]]), "ends ~0")]
    return _grammar(wd, "luxury_orbit", "luxury product", pts, js, 4.0, 10, crits)


@card("CAM-188")
def cam188(task, wd):
    """Camera grammar, real estate: 'steadicam glide through doorways, crane-up in atria' executed as a previs - a level,
    roll-free glide through a door (posts sweep out symmetrically), then a 3 m crane-up revealing the atrium."""
    pts = [(-.6, 1.5, -2, .12, BLUE), (.6, 1.5, -2, .12, GREEN), (0, 6, -9, .5, YEL)]
    js = ("function update(t){ if(t<=3){ const u=(1-Math.cos(Math.PI*t/3))/2; camera.position.set(0,1.5,2-5*u); camera.lookAt(0,1.5,-8); }"
          "else { const u=(1-Math.cos(Math.PI*Math.min(1,(t-3)/2)))/2; camera.position.set(0,1.5+3*u,-3); camera.lookAt(0,1.5+3*u+1.2*u,-8); } }")

    def crits(r, T):
        f = r["frames"]
        g = [i for i, t in enumerate(T) if t <= 3]
        sym = lambda m: max(abs((P(m, 0)[0][i] + P(m, 1)[0][i]) / 2 - 128) for i in g if m[i][0] and m[i][1] and _in_frame(m[i][0], 256, 144) and _in_frame(m[i][1], 256, 144))
        lvl = lambda m: max(abs(P(m, 0)[1][i] - P(m, 1)[1][i]) for i in g if m[i][0] and m[i][1])
        return [("glide: door posts sweep outward symmetrically and leave the frame", lambda m, fr: (sym(m) < .5 and P(m, 1)[0][g[12]] - P(m, 0)[0][g[12]] > 1.5 * (P(m, 1)[0][0] - P(m, 0)[0][0]) and m[g[-1]][0] is None,
                                                                                         [sym(m), float(P(m, 1)[0][0] - P(m, 0)[0][0])]), "symmetric, widening, gone"),
                ("steadicam: level and roll-free (posts stay on one horizontal line, height constant)", lambda m, fr: (lvl(m) < .3 and np.ptp([f[i]["pos"][1] for i in g]) < 1e-9, lvl(m)), "<0.3 px"),
                ("crane-up: +3 m rise after the doorway reveals the atrium (marker enters the frame)", lambda m, fr: (abs(f[-1]["pos"][1] - 4.5) < 1e-6 and m[-1][2] is not None and m[idx(T, 3.0)][2] is None,
                                                                                                    [f[-1]["pos"][1], m[idx(T, 3.0)][2] is None, m[-1][2] is not None]), [4.5, True, True])]
    return _grammar(wd, "realestate", "real estate", pts, js, 5.0, 10, crits)


@card("CAM-189")
def cam189(task, wd):
    """Camera grammar, industrial: 'low lateral track with foreground parallax' - a camera 0.4 m high tracks sideways at
    2 m/s; the foreground (2 m) crosses the screen 5x faster than the machinery (10 m), as the pinhole model requires."""
    pts = [(0, .5, 2, .08, RED), (0, 1.0, -6, .3, BLUE)]
    js = "function update(t){ const x=-1.5+2*t; camera.position.set(x,.4,4); camera.lookAt(x,.45,-1); }"

    def crits(r, T):
        w = [i for i in range(len(T)) if r["meas"][i][0] and r["meas"][i][1] and _in_frame(r["meas"][i][0], 256, 144)]
        v = lambda m, k: float(np.polyfit([T[i] for i in w], [P(m, k)[0][i] for i in w], 1)[0])
        return [("foreground parallax: screen speed ratio fg / bg = depth ratio 5 (measured)", lambda m, fr: (abs(v(m, 0) / v(m, 1) - 5) < .1, v(m, 0) / v(m, 1)), 5),
                ("low lateral track: camera 0.4 m high, moving only sideways at 2 m/s", lambda m, fr: (all(abs(x["pos"][1] - .4) < 1e-9 and abs(x["pos"][2] - 4) < 1e-9 for x in fr) and abs((fr[-1]["pos"][0] - fr[0]["pos"][0]) / T[-1] - 2) < 1e-6, True), True)]
    return _grammar(wd, "industrial", "industrial", pts, js, 1.5, 20, crits)


@card("CAM-190")
def cam190(task, wd):
    """Camera grammar, travel: 'drone rise-and-reveal then descending swoop' - the drone rises from behind a near ridge
    until the hidden landmark is revealed, then swoops down and forward toward it (occlusion measured on the render)."""
    pts = [(0, 1.0, -30, .9, YEL), (0, 1.0, 3, 1.4, MAG)]
    js = ("function update(t){ let y,z; if(t<=3){ y=1+13*(1-Math.cos(Math.PI*t/3))/2; z=6; } else { const u=(1-Math.cos(Math.PI*Math.min(1,(t-3)/3)))/2; y=14-10*u; z=6-14*u; }"
          "camera.position.set(0,y,z); camera.lookAt(0,1,-30); }")

    def crits(r, T):
        f = r["frames"]
        seen = lambda m: [m[i][0] is not None and m[i][0]["area"] > 5 for i in range(len(T))]
        return [("reveal: the landmark is hidden behind the ridge at the start and visible after the rise", lambda m, fr: (not seen(m)[0] and seen(m)[idx(T, 3.0)], [seen(m)[0], seen(m)[idx(T, 3.0)]]), [False, True]),
                ("altitude rises 1 -> 14 m, then descends while flying forward (swoop)", lambda m, fr: (abs(f[idx(T, 3.0)]["pos"][1] - 14) < 1e-6 and f[-1]["pos"][1] < 5 and f[-1]["pos"][2] < f[idx(T, 3.0)]["pos"][2] - 10,
                                                                                               [f[0]["pos"][1], f[idx(T, 3.0)]["pos"][1], f[-1]["pos"][1], f[-1]["pos"][2]]), "1 -> 14 -> 4, forward"),
                ("the swoop brings the landmark closer (it grows on screen)", lambda m, fr: (rad(m, 0)[-1] > 1.3 * rad(m, 0)[idx(T, 3.0)], [float(rad(m, 0)[idx(T, 3.0)]), float(rad(m, 0)[-1])]), ">1.3x")]
    return _grammar(wd, "travel", "travel", pts, js, 6.0, 10, crits)


@card("CAM-191")
def cam191(task, wd):
    """Camera grammar, food/craft: 'push in to craft moment, ease back' - distance 2.0 -> 1.2 m at the craft moment
    (t = 2 s) and back, raised-cosine; the subject's size peaks at the moment and returns to its start size."""
    pts = [(0, .9, 0, .15, RED)]
    js = "function update(t){ const d=2-0.8*(1-Math.cos(2*Math.PI*t/4))/2; camera.position.set(0,1.3,d); camera.lookAt(0,.9,0); return {d}; }"

    def crits(r, T):
        return [("subject size peaks at the craft moment (t = 2 s) and eases back to its start size", lambda m, fr: (abs(T[int(np.nanargmax(rad(m, 0)))] - 2.0) <= .1 + 1e-6 and abs(rad(m, 0)[-1] / rad(m, 0)[0] - 1) < .01 and rad(m, 0)[idx(T, 2)] / rad(m, 0)[0] > 1.4,
                                                                                                     [T[int(np.nanargmax(rad(m, 0)))], float(rad(m, 0)[idx(T, 2)] / rad(m, 0)[0])]), [2.0, ">1.4"]),
                ("eased: zero speed at the start, the peak and the end", lambda m, fr: (abs(fr[1]["x"]["d"] - fr[0]["x"]["d"]) < .01 and abs(fr[idx(T, 2.1)]["x"]["d"] - fr[idx(T, 1.9)]["x"]["d"]) < .01, True), True)]
    return _grammar(wd, "craft", "food/craft", pts, js, 4.0, 10, crits)


@card("CAM-192")
def cam192(task, wd):
    """Camera grammar, miniature: 'dives + aerial hops' - dive into diorama A, hop up over the set, dive into diorama B;
    altitude minima sit at the dioramas and each diorama is largest at its own dive."""
    pts = [(-4, .3, 0, .4, RED), (4, .3, 0, .4, BLUE)]
    js = ("const K=[[0,-4,12,6,-4],[1.5,-4,1.2,1.6,-4],[3,0,10,6,0],[4.5,4,1.2,1.6,4]];"
          "function update(t){ let k=0; while(k<K.length-2&&t>K[k+1][0]) k++; const a=K[k], b=K[k+1], u=Math.min(1,Math.max(0,(t-a[0])/(b[0]-a[0]))), e=(1-Math.cos(Math.PI*u))/2;"
          "const L=(i)=>a[i]+(b[i]-a[i])*e; camera.position.set(L(1),L(2),L(3)); camera.lookAt(L(4),.3,0); }")

    def crits(r, T):
        f = r["frames"]
        y = [x["pos"][1] for x in f]
        return [("each diorama is largest at its own dive (A at 1.5 s, B at 4.5 s)", lambda m, fr: (abs(T[int(np.nanargmax(rad(m, 0)))] - 1.5) < 1e-6 and abs(T[int(np.nanargmax(rad(m, 1)))] - 4.5) < 1e-6,
                                                                                         [T[int(np.nanargmax(rad(m, 0)))], T[int(np.nanargmax(rad(m, 1)))]]), [1.5, 4.5]),
                ("altitude: dives to 1.2 m at both dioramas, an aerial hop >= 10 m between", lambda m, fr: (abs(y[idx(T, 1.5)] - 1.2) < 1e-6 and abs(y[idx(T, 4.5)] - 1.2) < 1e-6 and y[idx(T, 3.0)] >= 10 - 1e-6, [y[idx(T, 1.5)], y[idx(T, 3.0)], y[idx(T, 4.5)]]), [1.2, 10, 1.2])]
    return _grammar(wd, "miniature", "miniature", pts, js, 4.5, 10, crits)


@card("CAM-193")
def cam193(task, wd):
    """Locked-iso glide: a fixed high isometric view (pitch -35.26 deg, yaw 45 deg) with only straight, level travel along
    the view's right axis; measured: no rotation or zoom on screen (marker offsets constant), constant speed."""
    Dv = -np.ones(3) / math.sqrt(3)
    Rv = np.cross(Dv, [0, 1, 0])
    Rv /= np.linalg.norm(Rv)
    Uv = np.cross(Rv, Dv)
    pts = [(0, 0, 0, .2, RED), tuple(2 * Rv) + (.2, BLUE), tuple(1.5 * Uv) + (.2, GREEN)]          # one depth plane
    js = ("const D=new TH.Vector3(-1,-1,-1).normalize(), Rt=new TH.Vector3().crossVectors(D,new TH.Vector3(0,1,0)).normalize();"
          "function update(t){ const p=new TH.Vector3(9,9,9).addScaledVector(Rt,-1.5+1.0*t); camera.position.copy(p); camera.lookAt(p.clone().add(D)); }")

    def crits(r, T):
        f = r["frames"]
        off = lambda m: np.array([[P(m, 1)[0][i] - P(m, 0)[0][i], P(m, 1)[1][i] - P(m, 0)[1][i]] for i in range(len(T))])
        return [("locked: no rotation or zoom - marker offsets constant on screen (measured)", lambda m, fr: (float(np.abs(off(m) - off(m)[0]).max()) < .15 and abs(P(m, 0)[0][-1] - P(m, 0)[0][0]) > 20, float(np.abs(off(m) - off(m)[0]).max())), "<0.15 px, travelling"),
                ("isometric angles: pitch -35.26 deg, yaw 45 deg, constant orientation", lambda m, fr: (np.ptp(np.array([x["q"] for x in f]), 0).max() < 1e-9, [round(math.degrees(math.asin(-1 / math.sqrt(3))), 2), 45]), "quaternion constant"),
                ("straight level travel at constant speed (height constant)", lambda m, fr: (np.ptp([x["pos"][1] for x in f]) < 1e-9 and float(np.abs(np.diff(np.diff(P(m, 0)[0]))).max()) < .2, float(np.abs(np.diff(np.diff(P(m, 0)[0]))).max())), "<0.2")]
    return _grammar(wd, "lockiso", "locked-iso", pts, js, 3.0, 10, crits)


def choose_architecture(world):
    """Intake CAMERA choice: grounded continuous worlds take A (one forward flight), sets of dioramas take B."""
    return "A" if world["kind"] == "grounded" else "B"


@card("CAM-194")
def cam194(task, wd):
    """Camera architecture A (continuous take) vs B (dive + aerial connector), chosen at intake: A is one forward flight
    with no cuts for a grounded world, B dives into each diorama and links them with high connectors."""
    worlds = [{"kind": "grounded", "name": "valley"}, {"kind": "dioramas", "name": "shelf", "sets": [-6, 0, 6]}]
    choice = [choose_architecture(w) for w in worlds]
    (wd / "intake.json").write_text(json.dumps([dict(w, camera=c) for w, c in zip(worlds, choice)]), encoding="utf-8")
    ptsA = [(0, .5, -6 * k, .2, [RED, BLUE, GREEN][k]) for k in range(3)]
    jsA = "function update(t){ camera.position.set(0,3,12-5*t); camera.lookAt(0,1,4-5*t); }"
    ptsB = [(x, .3, 0, .4, c) for x, c in zip(worlds[1]["sets"], [RED, BLUE, GREEN])]
    jsB = ("const S=%s; function update(t){ const k=Math.min(2,Math.floor(t/2)), u=(t-2*k)/2, x=S[k];"
           "const dive=Math.sin(Math.PI*Math.min(1,u)); const y=10-8.8*dive; const xx=(u<0.5)?x:(x+(S[Math.min(2,k+1)]-x)*(1-Math.cos(Math.PI*(u-0.5)/0.5*0.5))*(k<2?1:0));"
           "camera.position.set(xx,y,1.6+4*(1-dive)); camera.lookAt(xx,.3,0); }") % json.dumps(worlds[1]["sets"])
    T = times_for(3.0, 10)
    rA = cam3d(wd, "archA", ptsA, jsA, T, 10)
    TB = times_for(5.9, 10)
    rB = cam3d(wd, "archB", ptsB, jsB, TB, 10)
    zA = [f["pos"][2] for f in rA["frames"]]
    steps = np.abs(np.diff(zA))
    yB = np.array([f["pos"][1] for f in rB["frames"]])
    minima = [TB[i] for i in range(1, len(TB) - 1) if yB[i] <= yB[i - 1] and yB[i] < yB[i + 1]]
    xA = P(rA["meas"], 0)[1]
    still = P(rA["meas_in"], 0)[1]
    return [check("intake: grounded world -> A, dioramas -> B", choice == ["A", "B"], choice, ["A", "B"]),
            check("A: one forward flight, monotonic, no cut (every step equal)", bool((np.diff(zA) < 0).all()) and float(steps.max() / steps.min()) < 1.0001, [zA[0], zA[-1]], "12 -> -3"),
            check("A measured: the ground marker streams toward the camera continuously", bool(np.all(np.diff(xA[np.isfinite(xA)]) > 0)) and np.isfinite(xA).sum() > 10, int(np.isfinite(xA).sum()), ">10 frames, monotonic"),
            check("B: dives (minima 1.2 m) at each of the 3 dioramas, connectors at 10 m", len(minima) == 3 and all(abs(yB[TB.index(t)] - 1.2) < .01 for t in minima) and yB.max() >= 10 - 1e-6, [minima, float(yB.max())], "3 dives"),
            check("negative control: the unprocessed still never flies forward", not bool(np.all(np.diff(still[np.isfinite(still)]) > 0)) or np.isfinite(still).sum() <= 10, int(np.isfinite(still).sum()), "no motion")], \
        [rA["video"], rB["video"], wd / "intake.json"]


@card("CAM-183")
def cam183(task, wd):
    """Camera-move vocabulary for video models: one plainly phrased move per clip ('camera slowly pushes in') for Kling /
    Runway, a first-frame framing instead of camera verbs for Seedance R2V; and the zoom (lens) vs dolly (body)
    distinction executed in K3: a zoom keeps the near/far size ratio, a dolly changes it."""
    verbs = r"\b(pushes in|pulls out|pans|tilts|dollies|orbits|tracks|cranes|zooms)\b"

    def phrase(move, model):
        plain = {"push-in": "camera slowly pushes in", "pan": "camera pans left", "orbit": "camera orbits the subject", "dolly out": "camera dollies out"}[move]
        return "medium shot, subject centred, eye level" if model == "seedance-r2v" else plain
    lines = {m: phrase("push-in", m) for m in ("kling", "runway", "seedance-r2v")}
    raw = "dolly in then orbit around her, handheld"
    (wd / "camera_lines.json").write_text(json.dumps(lines, indent=1), encoding="utf-8")
    pts = [(0, 1, 0, .2, RED), (1.5, 1, -8, .4, BLUE)]
    js = ("function update(t){ if(t<=2){ camera.fov=40-20*t/2; camera.position.set(0,1,4); } else { camera.fov=40; camera.position.set(0,1,4-2*(t-2)/2); } camera.lookAt(0,1,0); }")
    T = times_for(4.0, 10)
    r = cam3d(wd, "zoomdolly", pts, js, T, 10)
    m = r["meas"]
    ratio = rad(m, 0) / rad(m, 1)
    i2, j0, j4 = idx(T, 2.0), idx(T, 2.1), idx(T, 4.0)
    zoom_keep = abs(ratio[i2] / ratio[0] - 1) < .03 and rad(m, 0)[i2] / rad(m, 0)[0] > 1.9
    dolly_change = ratio[j4] / ratio[j0] > 1.5
    return [check("one plainly phrased move per clip for Kling / Runway", all(len(re.findall(verbs, lines[k])) == 1 and not cam_words(lines[k])[1:] for k in ("kling", "runway")), [lines["kling"], re.findall(verbs, lines["kling"])], "camera slowly pushes in"),
            check("Seedance R2V gets a first-frame framing, no camera verbs", not cam_words(lines["seedance-r2v"]) and not re.findall(verbs, lines["seedance-r2v"]) and "shot" in lines["seedance-r2v"], lines["seedance-r2v"], "framing only"),
            check("zoom (lens): magnifies 2x and keeps the near/far size ratio (measured)", zoom_keep, [float(rad(m, 0)[i2] / rad(m, 0)[0]), float(ratio[i2] / ratio[0])], [2, 1]),
            check("dolly (body): the near/far ratio changes (measured > 1.5x)", dolly_change, float(ratio[j4] / ratio[j0]), ">1.5"),
            check("negative control: the unprocessed line stacks camera verbs (fails the one-move rule)", len(cam_words(raw)) > 1, cam_words(raw), ">1 moves")], [wd / "camera_lines.json", r["video"]]


@card("CAM-27")
def cam27(task, wd):
    """Locked restrained camera approximated with depth scale breathing: a slow 4% push on the focal layer (sine over
    4 s) with the depth layers breathing by depth (scale = (1 + 0.04 p)^k, k = 1.6 / 1 / 0.5) and no shake."""
    layers = [("fg", 1.6, RED, BLUE, (60, 40), (250, 140)), ("mid", 1.0, GREEN, YEL, (110, 60), (200, 120)), ("bg", 0.5, MAG, CYAN, (90, 100), (230, 50))]
    body = "".join('<div id=%s class=a style="left:0;top:0;width:320px;height:180px;transform-origin:50%% 50%%">%s%s</div>'
                   % (n, box_html(n + "a", a[0], a[1], 10, 10, ca), box_html(n + "b", b[0], b[1], 10, 10, cb)) for n, k, ca, cb, a, b in layers)
    js = ("window.camAt=function(t){ const p=(1-Math.cos(Math.PI*Math.min(t/4,1)))/2; %s }"
          % "".join("document.getElementById('%s').style.transform='scale('+Math.pow(1+0.04*p,%s)+')';" % (n, k) for n, k, *_ in layers))
    sels = sum([["#%sa" % n, "#%sb" % n] for n, *_ in layers], [])
    cols = sum([[ca, cb] for _, _, ca, cb, _, _ in layers], [])

    def crits(r, T):
        mdl = lambda k: np.array([(1 + .04 * sine_io(min(t / 4, 1))) ** k for t in T])
        def smooth(m):
            res = []
            for i in range(6):
                x, y = P(m, i)
                for v in (x, y):
                    c = np.polyfit(T, v, 6)
                    res.append(float(np.abs(v - np.polyval(c, T)).max()))
            return max(res)
        return [("focal layer pushes 1 -> 1.04 (measured, sine)", lambda m, f: (float(np.abs(D(m, 2, 3) - mdl(1)).max()) < .005, [round(float(D(m, 2, 3)[-1]), 4)]), 1.04),
                ("depth breathing: fg / mid / bg scale by depth (exponents 1.6 / 1 / 0.5)", lambda m, f: (float(np.abs(D(m, 0, 1) - mdl(1.6)).max()) < .005 and float(np.abs(D(m, 4, 5) - mdl(.5)).max()) < .005
                                                                                                   and D(m, 0, 1)[-1] > D(m, 2, 3)[-1] > D(m, 4, 5)[-1],
                                                                                                   [round(float(D(m, k, k + 1)[-1]), 4) for k in (0, 2, 4)]), [round((1.04) ** k, 4) for k in (1.6, 1, .5)]),
                ("no shake: every marker path is smooth (residual from a smooth fit < 0.3 px, the measuring floor)", lambda m, f: (smooth(m) < .3, smooth(m)), "<0.3")]
    return run_tl(wd, "restrained", body, js, sels, cols, 4.0, 10, crits)


GL_PAGE = r"""
const TH=K3.THREE, W=%(W)d, H=%(H)d; const ren=new TH.WebGLRenderer({preserveDrawingBuffer:true, antialias:false}); ren.setPixelRatio(1); ren.setSize(W,H);
ren.outputColorSpace=TH.SRGBColorSpace; document.getElementById('view').appendChild(ren.domElement);
const scene=new TH.Scene(), camera=new TH.PerspectiveCamera(35,W/H,.1,200);
%(js)s
ren.render(scene,camera); const gl=ren.getContext(); const px=new Uint8Array(W*H*4); gl.readPixels(0,0,W,H,gl.RGBA,gl.UNSIGNED_BYTE,px);
const img=[]; for(let y=H-1;y>=0;y--){ const row=[]; for(let x=0;x<W;x++){ const i=(y*W+x)*4; row.push([px[i],px[i+1],px[i+2]]); } img.push(row); }
OUT(Object.assign({img}, typeof EXTRA==='function'?EXTRA():{}));
"""


def gl_run(wd, name, js, W=160, H=90, scripts=(K3B,)):
    html = lpage("", GL_PAGE % {"W": W, "H": H, "js": js}, W, H, scripts=list(scripts))
    out, _ = chrome_run(wd, name, html, size=(W, H), gl=True, budget=4000)
    img = np.array(out.pop("img"), np.uint8)
    from PIL import Image
    Image.fromarray(img).save(wd / ("%s.png" % name))
    return out, img.astype(float), wd / ("%s.png" % name)


@card("CAM-167")
def cam167(task, wd):
    """Studio backdrop gradient: scene.background = K3S.studioBackdrop({inner #1e4a44, mid #0c2224, outer #050c0d,
    cy .42}) - a radial canvas texture; rendered by THREE in WebGL (SwiftShader) and read back pixel by pixel."""
    js = ("camera.position.set(0,1,5); camera.lookAt(0,1,0); if(APPLY) scene.background=K3S.studioBackdrop({inner:'#1e4a44',mid:'#0c2224',outer:'#050c0d',cy:.42});"
          "const EXTRA=()=>{ if(!APPLY) return {}; const c=scene.background.image.getContext('2d'); const g=(u,v)=>Array.from(c.getImageData(Math.floor(u*511),Math.floor(v*511),1,1).data).slice(0,3);"
          "return {tex_c:g(.5,.42), tex_corner:g(0,0), tex_mid:g(.5,.42+.55*.75)}; };")
    out, img, png = gl_run(wd, "backdrop", "const APPLY=true;" + js, scripts=(K3B, SHAPEKIT))
    _, img0, _ = gl_run(wd, "backdrop_input", "const APPLY=false;" + js, scripts=(K3B, SHAPEKIT))
    H, W = img.shape[:2]
    L = lum(img)
    yb, xb = np.unravel_index(int(np.argmax(L)), L.shape)
    inner = np.array(hex2rgb("#1e4a44"), float)
    col = img[yb, xb]
    prof = L[yb, xb:]
    def falloff(a):
        return float(lum(a[yb, xb]) - lum(a[0, 0]))
    return [check("radial falloff from the bright centre to the dark corners (measured luminance drop)", falloff(img) > 30 and bool((np.diff(prof) <= 1).all()), [falloff(img), float(lum(img[0, 0]))], ">30, monotonic"),
            check("brightest pixel is the inner colour #1e4a44, centred horizontally, above the middle (cy .42)", float(np.abs(col - inner).max()) <= 3 and abs(xb - W / 2) <= 2 and yb < H / 2, [col.tolist(), int(xb), int(yb)], [inner.tolist(), W / 2, "< H/2"]),
            check("corners reach the outer colour #050c0d", float(np.abs(img[0, 0] - hex2rgb("#050c0d")).max()) <= 4, img[0, 0].tolist(), hex2rgb("#050c0d")),
            check("the texture itself holds inner at (0.5, cy) and outer at the corner", out["tex_c"] == list(hex2rgb("#1e4a44")) and max(abs(a - b) for a, b in zip(out["tex_corner"], hex2rgb("#050c0d"))) <= 4, [out["tex_c"], out["tex_corner"]], ["#1e4a44", "#050c0d"]),
            check("negative control: the unprocessed scene has no gradient", not falloff(img0) > 30, falloff(img0), "<=30")], [png]


@card("CAM-168")
def cam168(task, wd):
    """Cream studio sweep: K3.studio(scene, {bg, grid}) - cream sweep sphere (#f1efe8), contact-shadow floor (.22),
    faint grid (16 m / 32, #c9d8c2 .35), key 2.6 @ (3,6,4), fill #dfe8ff .9, rim 1.4, hemi .9; rendered in WebGL with a
    box on the floor; light rig read from the scene graph, sweep colour and contact shadow measured in pixels."""
    js = ("ren.shadowMap.enabled=true; camera.position.set(-4,3,-4); camera.lookAt(0,.3,0); let S=null; if(APPLY) S=K3.studio(scene,{});"
          "const box=new TH.Mesh(new TH.BoxGeometry(1,1,1), new TH.MeshStandardMaterial({color:0x8899aa})); box.position.y=.5; box.castShadow=true; scene.add(box);"
          "const EXTRA=()=>{ const pr=(x,y,z)=>{ const v=new TH.Vector3(x,y,z).project(camera); return [Math.round((v.x*.5+.5)*W), Math.round((-v.y*.5+.5)*H)]; };"
          "const L=[]; scene.traverse(o=>{ if(o.isLight) L.push([o.type, +o.intensity.toFixed(3), o.color.getHexString(), o.position.toArray().map(v=>+v.toFixed(3))]); });"
          "return {lights:L, shadow:pr(-0.85,0,-0.75), lit:pr(-2.2,0,1.0), sky:pr(0,6,8), grid: S?[S.grid.material.opacity, S.floor.material.opacity]:null}; };")
    out, img, png = gl_run(wd, "studio", "const APPLY=true;" + js, W=192, H=108, scripts=(K3B, LABKIT))
    out0, img0, _ = gl_run(wd, "studio_input", "const APPLY=false;" + js, W=192, H=108, scripts=(K3B, LABKIT))
    sky = lambda o, a: a[min(107, max(0, o["sky"][1])), min(191, max(0, o["sky"][0]))]
    want_l = [["DirectionalLight", 2.6, "ffffff", [3, 6, 4]], ["DirectionalLight", .9, "dfe8ff", [-5, 3, 2]], ["DirectionalLight", 1.4, "ffffff", [-2, 4, -5]]]
    dirs = [l for l in out["lights"] if l[0] == "DirectionalLight"]
    hemi = [l for l in out["lights"] if l[0] == "HemisphereLight"]
    sh, li = img[out["shadow"][1], out["shadow"][0]], img[out["lit"][1], out["lit"][0]]
    return [check("cream sweep fills the background (#f1efe8, unlit basic material)", float(np.abs(sky(out, img) - hex2rgb("#f1efe8")).max()) <= 3, sky(out, img).tolist(), hex2rgb("#f1efe8")),
            check("light rig: key 2.6 @ (3,6,4), fill #dfe8ff 0.9, rim 1.4, hemisphere 0.9", dirs == want_l and len(hemi) == 1 and hemi[0][1] == .9, out["lights"], want_l + [["HemisphereLight", .9]]),
            check("contact shadow: the floor next to the box (away from the key) is darker than the open floor", lum(sh) < lum(li) - 15, [float(lum(sh)), float(lum(li))], "darker by >15"),
            check("shadow floor .22 and faint grid .35", out["grid"] == [.35, .22], out["grid"], [.35, .22]),
            check("negative control: the unprocessed scene has no cream sweep", not float(np.abs(sky(out0, img0) - hex2rgb("#f1efe8")).max()) <= 3, sky(out0, img0).tolist(), "not cream")], [png]


def chaikin(pts, passes):
    p = np.asarray(pts, float)
    for _ in range(passes):
        q = [p[0]]
        for a, b in zip(p[:-1], p[1:]):
            q += [.75 * a + .25 * b, .25 * a + .75 * b]
        q.append(p[-1])
        p = np.array(q)
    return p


def flyover(route, passes=3, travel=13.0, secs=24.0, fps=10, look=1.5, gain=.6, roll_max=.13, alt=(4600, 4300), pitch_nadir=76):
    """The card's flyover camera: Chaikin-rounded path walked by arc length at constant ground speed, heading = bearing
    to the point LOOK_AHEAD further, constant pitch, roll = clamp(dHeading x gain) between the aim and 2x look-ahead."""
    p = chaikin(route, passes)
    seg = np.hypot(*np.diff(p, axis=0).T)
    s = np.r_[0, np.cumsum(seg)]
    at = lambda d: np.array([np.interp(d, s, p[:, 0]), np.interp(d, s, p[:, 1])])
    bearing = lambda a, b: math.atan2(b[0] - a[0], b[1] - a[1])
    n = int(secs * fps) + 1
    out = []
    for i in range(n):
        t = i / fps
        d = travel * t / secs
        c = at(d)
        h1 = bearing(c, at(d + look))
        h2 = bearing(c, at(d + 2 * look))
        dh = (h2 - h1 + math.pi) % (2 * math.pi) - math.pi
        out.append({"t": t, "x": float(c[0]), "y": float(c[1]), "heading": h1, "pitch": -(90 - pitch_nadir), "roll": float(np.clip(dh * gain, -roll_max, roll_max)),
                    "alt": alt[0] + (alt[1] - alt[0]) * t / secs})
    return out, p, float(s[-1])


@card("CAM-181")
def cam181(task, wd):
    """Flyover camera math: Chaikin corner cutting (3 passes), arc-length walk at 13 km / 24 s = 0.54 km/s, heading =
    bearing to a point 1.5 km ahead, constant pitch -14 deg (pitch-from-nadir 76), roll = clamp(dHeading x 0.6, +/-0.13)
    toward the turn, altitude 4600 -> 4300 m; path >= travel + 2 x look-ahead. Computed and plotted (no globe engine)."""
    route = [(0, 0), (4, 0), (6, 4), (10, 5), (14, 2), (17, 3)]
    cam, path, L = flyover(route)
    raw, _, _ = flyover(route, passes=0)
    (wd / "flyover.json").write_text(json.dumps(cam), encoding="utf-8")
    from PIL import Image, ImageDraw
    im = Image.new("RGB", (360, 200), (20, 24, 30))
    d = ImageDraw.Draw(im)
    tr = lambda x, y: (10 + x * 20, 180 - y * 30)
    d.line([tr(*q) for q in route], fill=(90, 90, 90), width=1)
    d.line([tr(*q) for q in path], fill=(80, 200, 255), width=2)
    for c in cam[::20]:
        d.ellipse([tr(c["x"], c["y"])[0] - 2, tr(c["x"], c["y"])[1] - 2, tr(c["x"], c["y"])[0] + 2, tr(c["x"], c["y"])[1] + 2], fill=(255, 200, 0))
    im.save(wd / "flyover.png")
    sp = [math.hypot(b["x"] - a["x"], b["y"] - a["y"]) * 10 for a, b in zip(cam, cam[1:])]
    dh = lambda c: max(abs((b["heading"] - a["heading"] + math.pi) % (2 * math.pi) - math.pi) for a, b in zip(c, c[1:]))
    ahead = int(round(1.5 / (13 / 24) * 10))             # frames until the camera reaches today's aim point
    agree = [np.sign(c["roll"]) == np.sign(((cam[min(len(cam) - 1, i + ahead)]["heading"] - c["heading"] + math.pi) % (2 * math.pi) - math.pi)) for i, c in enumerate(cam) if abs(c["roll"]) > .02]
    turn_sign = sum(agree) >= .9 * len(agree)
    return [check("smooth heading: max heading change per frame < 1.5 deg (Chaikin + look-ahead)", math.degrees(dh(cam)) < 1.5, math.degrees(dh(cam)), "<1.5 deg"),
            check("constant ground speed 0.54 km/s by arc length (sampled path)", max(abs(v - 13 / 24) for v in sp) / (13 / 24) < .01, [min(sp), max(sp)], 13 / 24),
            check("constant pitch -14 deg; altitude 4600 -> 4300 m", all(c["pitch"] == -14 for c in cam) and cam[0]["alt"] == 4600 and abs(cam[-1]["alt"] - 4300) < 1e-9, [cam[0]["pitch"], cam[-1]["alt"]], [-14, 4300]),
            check("roll banks into the turn, clamped to +/-0.13 rad", max(abs(c["roll"]) for c in cam) <= .13 + 1e-12 and max(abs(c["roll"]) for c in cam) > .05 and turn_sign, max(abs(c["roll"]) for c in cam), "<=0.13, signed with the turn"),
            check("Chaikin 3 passes: 8x segments, path km >= travel + 2 x look-ahead", len(path) == 8 * len(route) and L >= 13 + 3, [len(path), round(L, 2)], [">=16 km"]),
            check("negative control: the raw polyline turns in heading jumps", not math.degrees(dh(raw)) < 1.5, math.degrees(dh(raw)), ">=1.5 deg")], [wd / "flyover.json", wd / "flyover.png"]


def reserve_space(prompt, side="left"):
    return prompt.rstrip(". ") + ", subject on the %s third, generous empty space on the %s for text overlay, no text" % ("right" if side == "left" else "left", side)


def zone_clean(img, side="left", thr=6.0):
    a = img.astype(float).mean(-1)
    w = a.shape[1]
    z = a[:, :w // 3] if side == "left" else a[:, 2 * w // 3:]
    g = np.abs(np.diff(z, axis=1)).mean() + np.abs(np.diff(z, axis=0)).mean()
    return float(g) < thr, float(g)


@card("CAM-182")
def cam182(task, wd):
    """Composition keywords that reserve space for type: the generator prompt gains 'subject on the right third, generous
    empty space on the left for text overlay, no text'; the empty zone of the returned frame is verified before type is
    animated into it (LinkedIn banner 1584x396). The generation itself is not run here: two banner fixtures stand in."""
    from PIL import Image, ImageDraw
    W, H = 1584, 396
    rng = np.random.default_rng(2)
    prompt = reserve_space("a barista pouring latte art, warm morning light")

    def banner(cx):
        im = Image.new("RGB", (W, H), (236, 226, 210))
        a = np.asarray(im).copy()
        x0 = int(cx - 260)
        a[40:360, x0:x0 + 520] = rng.integers(60, 200, (320, 520, 3))
        return Image.fromarray(a.astype(np.uint8))
    good, bad = banner(0.78 * W), banner(0.45 * W)
    good.save(wd / "banner_right_third.png")
    bad.save(wd / "banner_centred.png")
    ok_g, e_g = zone_clean(np.asarray(good))
    ok_b, e_b = zone_clean(np.asarray(bad))
    im = good.copy()
    ImageDraw.Draw(im).rectangle([80, 150, 80 + 380, 150 + 90], fill=(20, 30, 60))
    im.save(wd / "banner_with_type.png")
    after_type = np.asarray(im).astype(float)
    subj_untouched = float(np.abs(after_type[:, W // 3:] - np.asarray(good)[:, W // 3:]).max()) == 0
    (wd / "prompt.txt").write_text(prompt, encoding="utf-8")
    return [check("the empty left third of the right-third banner verifies clean (edge energy)", ok_g, e_g, "<6"),
            check("prompt carries the space-reserving phrase", "subject on the right third" in prompt and "empty space on the left for text overlay" in prompt, prompt, "phrase added"),
            check("type animated into the verified zone leaves the subject untouched", subj_untouched, subj_untouched, True),
            check("negative control: a centred-subject frame fails the empty-zone check", not ok_b, e_b, ">=6")], [wd / "prompt.txt", wd / "banner_with_type.png"]


def smooth_subject(samples, conf_min=.3, still=.08):
    """The card's smoothSubject: keep samples with confidence > 0.3, two-way exponential smoothing with weight 0.3 x conf,
    a still shot (travel < 0.08) takes the median; returns smoothed x (fraction of width)."""
    s = [(t, x, c) for t, x, c in samples if c > conf_min]
    if not s:
        return None
    xs = np.array([x for _, x, _ in s])
    if xs.max() - xs.min() < still:
        return [(t, float(np.median(xs))) for t, _, _ in s]
    f, b = [xs[0]], [xs[-1]]
    for i in range(1, len(s)):
        w = .3 * s[i][2]
        f.append(f[-1] + w * (xs[i] - f[-1]))
    for i in range(len(s) - 2, -1, -1):
        w = .3 * s[i][2]
        b.append(b[-1] + w * (xs[i] - b[-1]))
    b = b[::-1]
    return [(t, float((a + c) / 2)) for (t, _, _), a, c in zip(s, f, b)]


def subject_pan(cx, src_w, crop_w):
    return float(np.clip(cx * src_w - crop_w / 2, 0, src_w - crop_w))


@card("CAM-186")
def cam186(task, wd):
    """Subject-follow reframing: the subject is found with cv2 (frame difference, no models) every 0.4 s with a
    confidence, smoothed two ways (weight 0.3 x conf), still shots use the median, the 9:16 cover crop follows sideways
    and clamps to the picture edges; measured on a synthetic walking plate."""
    import cv2
    W, H, fps = 320, 180, 10
    rng = np.random.default_rng(4)
    true_x = lambda t: 60 + 200 * sine_io(min(t / 6, 1))
    frames = []
    for i in range(int(6 * fps) + 1):
        t = i / fps
        f = np.zeros((H, W, 3), np.uint8) + 90
        x = int(true_x(t) + rng.normal(0, 3))
        cv2.rectangle(f, (x - 12, 50), (x + 12, 160), (220, 180, 150), -1)
        frames.append(f)
    src = write_video(wd / "walk.mp4", frames, fps)
    dec = read_video(src).astype(np.uint8)
    samples = []
    for i in range(0, len(dec), 4):                         # every 0.4 s
        a = cv2.cvtColor(dec[i], cv2.COLOR_RGB2GRAY).astype(np.int16)
        bgf = np.full_like(a, 90)
        m = (np.abs(a - bgf) > 10).astype(np.uint8)
        n, lab, st, cen = cv2.connectedComponentsWithStats(m)
        if n > 1:
            j = 1 + int(np.argmax(st[1:, 4]))
            samples.append((i / fps, float(cen[j][0] / W), float(min(1, st[j, 4] / 2000))))
    sm = smooth_subject(samples)
    cw = int(H * 9 / 16)
    pans = [(t, subject_pan(x, W, cw)) for t, x in sm]
    full = [np.interp(i / fps, [p[0] for p in pans], [p[1] for p in pans]) for i in range(len(dec))]
    crops = [dec[i][:, int(round(full[i])):int(round(full[i])) + cw] for i in range(len(dec))]
    out = write_video(wd / "follow_9x16.mp4", [np.ascontiguousarray(c) for c in crops], fps)
    err = [abs((true_x(i / fps)) - (full[i] + cw / 2)) for i in range(len(dec))]
    raw_x = np.array([x for _, x, _ in samples]) * W
    jerk = lambda v: float(np.abs(np.diff(v, 2)).mean())
    still_s = smooth_subject([(t, .5 + .01 * math.sin(t), .9) for t in np.arange(0, 3, .4)])
    clampL = subject_pan(.02, W, cw)
    fixed_err = max(abs(true_x(i / fps) - W / 2) for i in range(len(dec)))
    return [check("the 9:16 crop keeps the subject near its centre (true path, after smoothing)", max(err) < .25 * cw, max(err), "<%.1f px" % (.25 * cw)),
            check("two-way smoothing removes jitter: smoothed path jerk < raw detections", jerk(np.array([x for _, x in sm]) * W) < .5 * jerk(raw_x), [jerk(np.array([x for _, x in sm]) * W), jerk(raw_x)], "<0.5x"),
            check("still shot (< 0.08 travel) -> one median position", len({round(x, 9) for _, x in still_s}) == 1, still_s[0][1], "median"),
            check("pan clamps to the picture edges", clampL == 0 and subject_pan(.99, W, cw) == W - cw, [clampL, subject_pan(.99, W, cw)], [0, W - cw]),
            check("negative control: a fixed centre crop loses the subject", not fixed_err < .25 * cw, fixed_err, ">=%.1f" % (.25 * cw))], [out, src]


def _oblique(yaw=20, pitch=10, f=300, W=320, H=200, cam=(0, 1.4, 6)):
    cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))

    def proj(p):
        x, y, z = p[0] - cam[0], p[1] - cam[1], p[2] - cam[2]
        x, z = cy * x - sy * z, sy * x + cy * z           # yaw
        y, z = cp * y + sp * z, -sp * y + cp * z          # pitch
        return (W / 2 + f * x / -z, H / 2 - f * y / -z)
    return proj


@card("CAM-203")
def cam203(task, wd):
    """Oblique room from projected polygons: a fixed yaw 20 / pitch 10 camera projects the wall, floor, frame and door
    point by point; the door is drawn before the wall-with-opening so its swing is occluded outside the opening, and the
    key inside the lock is clipped in the lock's own coordinates."""
    from PIL import Image, ImageDraw
    W, H = 320, 200
    proj = _oblique()
    wall = [(-3, 0, 0), (3, 0, 0), (3, 3, 0), (-3, 3, 0)]
    opening = [(-.5, 0, 0), (.5, 0, 0), (.5, 2.1, 0), (-.5, 2.1, 0)]
    floor = [(-3, 0, 0), (3, 0, 0), (3, 0, 3), (-3, 0, 3)]

    def door(a):
        c, s_ = math.cos(math.radians(a)), math.sin(math.radians(a))
        return [(-.5, 0, 0), (-.5 + c, 0, -s_), (-.5 + c, 2.1, -s_), (-.5, 2.1, 0)]   # hinged on the left jamb, swings into the room behind

    def frame(a, order):
        im = Image.new("RGB", (W, H), (30, 30, 36))
        d = ImageDraw.Draw(im)
        d.polygon([proj(p) for p in floor], fill=(90, 70, 50))
        layers = [("door", [proj(p) for p in door(a)], (255, 0, 0)), ("wall", None, None)]
        if order == "wall-first":
            layers = layers[::-1]
        for kind, poly, col in layers:
            if kind == "door":
                d.polygon(poly, fill=col)
            else:
                m = Image.new("L", (W, H), 0)
                ImageDraw.Draw(m).polygon([proj(p) for p in wall], fill=255)
                ImageDraw.Draw(m).polygon([proj(p) for p in opening], fill=0)
                im.paste((200, 200, 210), (0, 0), m)
        # lock with a key clipped in the lock's own coordinates (unit square on the door)
        lock = Image.new("RGBA", (40, 40), (60, 60, 60, 255))
        ImageDraw.Draw(lock).rectangle([25, 15, 60, 25], fill=(0, 0, 255, 255))    # the key overhangs the lock: clipped by the 40x40 canvas
        q = [proj(p) for p in [(-.1, 1.0, .001), (.1, 1.0, .001), (.1, 1.2, .001), (-.1, 1.2, .001)]]
        x0, y0 = int(min(p[0] for p in q)), int(min(p[1] for p in q))
        x1, y1 = int(max(p[0] for p in q)), int(max(p[1] for p in q))
        im.paste(lock.resize((x1 - x0, y1 - y0)), (x0, y0), lock.resize((x1 - x0, y1 - y0)))
        return np.asarray(im), (x0, y0, x1, y1)
    om = Image.new("L", (W, H), 0)
    ImageDraw.Draw(om).polygon([proj(p) for p in opening], fill=255)
    om = np.asarray(om) > 0
    vids, leak, leak_naive = [], 0, 0
    for a in range(0, 80, 5):
        f, lk = frame(a, "door-first")
        g, _ = frame(a, "wall-first")
        red = (f[..., 0] > 200) & (f[..., 1] < 50)
        redn = (g[..., 0] > 200) & (g[..., 1] < 50)
        wallm = np.zeros((H, W), bool)
        mm = Image.new("L", (W, H), 0)
        ImageDraw.Draw(mm).polygon([proj(p) for p in wall], fill=255)
        wallm = (np.asarray(mm) > 0) & ~om
        leak = max(leak, int((red & wallm).sum()))
        leak_naive = max(leak_naive, int((redn & wallm).sum()))
        vids.append(f)
    key_out = int(((vids[0][..., 2] > 200) & (vids[0][..., 0] < 50)).sum() and
                  ((lambda b: ((vids[0][..., 2] > 200) & (vids[0][..., 0] < 50))[:, :lk[0]].sum() + ((vids[0][..., 2] > 200) & (vids[0][..., 0] < 50))[:, lk[2]:].sum())(lk)))
    v = write_video(wd / "door.mp4", vids, 10)
    c = proj((3, 3, 0))
    yaw, pitch = math.radians(20), math.radians(10)
    p = np.array([3 - 0, 3 - 1.4, 0 - 6.0])
    x, z = math.cos(yaw) * p[0] - math.sin(yaw) * p[2], math.sin(yaw) * p[0] + math.cos(yaw) * p[2]
    y, z = math.cos(pitch) * p[1] + math.sin(pitch) * z, -math.sin(pitch) * p[1] + math.cos(pitch) * z
    want = (160 + 300 * x / -z, 100 - 300 * y / -z)
    return [check("door drawn before the wall-with-opening: no door pixel ever shows outside the opening", leak == 0, leak, 0),
            check("the door is visible through the opening while it swings", int(((vids[-1][..., 0] > 200) & (vids[-1][..., 1] < 50) & om).sum()) > 50, int(((vids[-1][..., 0] > 200) & (vids[-1][..., 1] < 50) & om).sum()), ">50 px"),
            check("the key is clipped to the lock in the lock's own coordinates", key_out == 0, key_out, 0),
            check("projection point by point with yaw 20 / pitch 10 (corner re-derived)", abs(c[0] - want[0]) < 1e-9 and abs(c[1] - want[1]) < 1e-9, [c, want], "equal"),
            check("negative control: drawing the wall first lets the swinging door paint over the wall", not leak_naive == 0, leak_naive, ">0")], [v]


@card("CAM-204")
def cam204(task, wd):
    """World-space camera keys + follow blend: keyframes [t, x, y, z, zoom] interpolated with easeInOut (1.8 s glide
    between zones), a follow weight w(t) blends the target to the van's position, the target is projected to the
    viewport centre; measured from the rendered markers."""
    keys = [[0, 100, 90, 0, 1.5], [1.0, 100, 90, 0, 1.5], [2.8, 400, 140, 0, 1.2], [3.0, 400, 140, 0, 1.2], [4.0, 400, 140, 0, 1.0]]
    body = ('<div id=world class=a style="left:0;top:0;width:600px;height:300px;transform-origin:0 0">%s%s%s</div>'
            % (box_html("za", 95, 85, 10, 10, RED), box_html("zb", 395, 135, 10, 10, BLUE), box_html("van", 0, 175, 10, 10, GREEN)))
    js = ("const K=%s; const io=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;"
          "function key(t){ let k=0; while(k<K.length-2&&t>K[k+1][0]) k++; const a=K[k], b=K[k+1], u=io(Math.min(1,Math.max(0,(t-a[0])/(b[0]-a[0])))); return a.map((v,i)=>v+(b[i]-v)*u); }"
          "const van=t=>[200+60*t,180]; const w=t=>{const u=Math.min(1,Math.max(0,(t-3)/1)); return u*u*(3-2*u);};"
          "window.camAt=function(t){ const k=key(t), v=van(t), ww=w(t); const tx=k[1]+(v[0]-k[1])*ww, ty=k[2]+(v[1]-k[2])*ww; const s=k[4]*1000/(1000+k[3]);"
          "document.getElementById('van').style.left=(v[0]-5)+'px'; document.getElementById('van').style.top=(v[1]-5)+'px';"
          "document.getElementById('world').style.transform='translate('+(160-tx*s)+'px,'+(90-ty*s)+'px) scale('+s+')'; }") % json.dumps(keys)

    def crits(r, T):
        cen = lambda m, k, t: math.hypot(m[idx(T, t)][k]["cx"] - 160, m[idx(T, t)][k]["cy"] - 90) if m[idx(T, t)][k] else 999
        sc = lambda m: np.array([math.dist(fr["el"][3]["q"][0], fr["el"][3]["q"][1]) / 600 for fr in r["frames"]])   # browser quad of the world layer
        mdl = [1.5 + (1.2 - 1.5) * cubic_io(min(1, max(0, (t - 1) / 1.8))) for t in T]
        return [("zone A, then zone B (after a 1.8 s easeInOut glide), then the van sit at the viewport centre", lambda m, f: (cen(m, 0, .5) < .3 and cen(m, 1, 2.9) < .3 and cen(m, 2, 4.5) < .3, [cen(m, 0, .5), cen(m, 1, 2.9), cen(m, 2, 4.5)]), "<0.3 px"),
                ("zoom keys interpolate with easeInOut (measured marker spacing)", lambda m, f: (maxerr(sc(m)[:idx(T, 2.8)], mdl[:idx(T, 2.8)]) < .003, [round(float(v), 3) for v in sc(m)[:idx(T, 2.8):6]]), [round(v, 3) for v in mdl[:idx(T, 2.8):6]]),
                ("follow blend: the van drifts across the frame before w = 1 and is locked after", lambda m, f: (cen(m, 2, 3.0) > 20 and max(cen(m, 2, t) for t in (4.1, 4.5, 4.9)) < .3, [cen(m, 2, 3.0), cen(m, 2, 4.5)]), [">20", "<0.3"])]
    return run_tl(wd, "followkeys", body, js, ["#za", "#zb", "#van", "#world"], [RED, BLUE, GREEN, None], 5.0, 10, crits)


@card("CAM-205")
def cam205(task, wd):
    """Follow camera with leg-based zoom: camera centre = lerp(head, a point slightly ahead on the route, 0.35); zoom =
    1.8 - 0.8 sin(pi x legProgress), so it widens mid-leg (1.0) and tightens on arrival (1.8)."""
    route = [[60, 90], [260, 90], [260, 250], [460, 250]]
    body = ('<div id=world class=a style="left:0;top:0;width:600px;height:400px;transform-origin:0 0">%s%s%s</div>'
            % (box_html("hd", 0, 0, 8, 8, RED), box_html("ra", 155, 160, 8, 8, BLUE), box_html("rb", 355, 160, 8, 8, GREEN)))
    js = ("const RT=%s, LEG=2.0, AH=30; function at(d){ let k=0; while(k<RT.length-2&&d>Math.hypot(RT[k+1][0]-RT[k][0],RT[k+1][1]-RT[k][1])){ d-=Math.hypot(RT[k+1][0]-RT[k][0],RT[k+1][1]-RT[k][1]); k++; }"
          "const a=RT[k], b=RT[k+1], L=Math.hypot(b[0]-a[0],b[1]-a[1]); const u=Math.min(1,d/L); return [a[0]+(b[0]-a[0])*u, a[1]+(b[1]-a[1])*u]; }"
          "window.camAt=function(t){ const leg=Math.min(2,Math.floor(t/LEG)), p=Math.min(1,(t-leg*LEG)/LEG); let d=0; for(let k=0;k<leg;k++) d+=Math.hypot(RT[k+1][0]-RT[k][0],RT[k+1][1]-RT[k][1]);"
          "d+=p*Math.hypot(RT[leg+1][0]-RT[leg][0],RT[leg+1][1]-RT[leg][1]); const h=at(d), a=at(d+AH); const c=[h[0]+(a[0]-h[0])*.35, h[1]+(a[1]-h[1])*.35]; const z=1.8-0.8*Math.sin(Math.PI*p);"
          "document.getElementById('hd').style.left=(h[0]-4)+'px'; document.getElementById('hd').style.top=(h[1]-4)+'px';"
          "document.getElementById('world').style.transform='translate('+(160-c[0]*z)+'px,'+(90-c[1]*z)+'px) scale('+z+')'; }") % json.dumps(route)

    def crits(r, T):
        mdl = [1.8 - .8 * math.sin(math.pi * min(1, (t - 2 * min(2, int(t // 2))) / 2)) for t in T]
        z = lambda m: np.array([math.dist(fr["el"][3]["q"][0], fr["el"][3]["q"][1]) / 600 for fr in r["frames"]])   # browser quad of the world layer
        lead = lambda m, t: (m[idx(T, t)][0]["cx"] - 160) if m[idx(T, t)][0] else None
        return [("the camera leads the head: head sits behind centre by 0.35 x 30 px x zoom along the route", lambda m, f: (abs(lead(m, 1.0) + .35 * 30 * 1.0) < .3 and abs(lead(m, .5) + .35 * 30 * (1.8 - .8 * math.sin(math.pi * .25))) < .3,
                                                                                                                [lead(m, .5), lead(m, 1.0)]), [-.35 * 30 * (1.8 - .8 * math.sin(math.pi * .25)), -10.5]),
                ("zoom = 1.8 - 0.8 sin(pi p): widest (1.0) mid-leg, tight (1.8) on arrival (measured)", lambda m, f: (maxerr([z(m)[i] for i in range(len(T)) if T[i] < 1.99], [mdl[i] for i in range(len(T)) if T[i] < 1.99]) < .004 and abs(z(m)[idx(T, 1.0)] - 1.0) < .004,
                                                                                                            [round(float(z(m)[idx(T, t)]), 3) for t in (0, .5, 1.0, 1.5)]), [round(1.8 - .8 * math.sin(math.pi * t / 2), 3) for t in (0, .5, 1.0, 1.5)])]
    return run_tl(wd, "legzoom", body, js, ["#hd", "#ra", "#rb", "#world"], [RED, BLUE, GREEN, None], 1.9, 10, crits)


@card("CAM-236")
def cam236(task, wd):
    """Split-screen grid: a 3x3 grid of clips, each inset on its own coloured panel (ffmpeg pad + xstack); measured: nine
    panel colours in place and every cell's clip moving."""
    cols = ["0xe63946", "0xf1a208", "0x2a9d8f", "0x264653", "0x8338ec", "0xff006e", "0x3a86ff", "0x06d6a0", "0xffbe0b"]
    args, chains = [], []
    for k, c in enumerate(cols):
        args += ["-f", "lavfi", "-i", "testsrc2=s=96x52:d=1.5:r=10"]
        chains.append("[%d]pad=106:60:5:4:color=%s[p%d]" % (k, c, k))
    lay = "|".join("%d_%d" % (106 * (k % 3), 60 * (k // 3)) for k in range(9))
    fc = ";".join(chains) + ";" + "".join("[p%d]" % k for k in range(9)) + "xstack=inputs=9:layout=%s" % lay
    out = wd / "grid.mp4"
    ff(*args, "-filter_complex", fc, "-c:v", "libx264rgb", "-qp", "0", "-preset", "ultrafast", out)
    raw = wd / "single_input.mp4"
    ff("-f", "lavfi", "-i", "testsrc2=s=318x180:d=1.5:r=10", "-c:v", "libx264rgb", "-qp", "0", "-preset", "ultrafast", raw)
    v, vr = read_video(out), read_video(raw)

    def panels(a):
        return [float(np.abs(a[0, 60 * (k // 3) + 1, 106 * (k % 3) + 50] - hex2rgb(cols[k][2:])).max()) for k in range(9)]

    def moving(a):
        return [float(np.abs(np.diff(a[:, 60 * (k // 3) + 8:60 * (k // 3) + 52, 106 * (k % 3) + 10:106 * (k % 3) + 96], axis=0)).mean()) for k in range(9)]
    return [check("nine coloured panels in a 3x3 grid (each panel's colour measured at its border)", max(panels(v)) < 4, [round(x, 1) for x in panels(v)], "<4"),
            check("every cell's clip plays", min(moving(v)) > 1, [round(x, 2) for x in moving(v)], ">1"),
            check("output is the 3x3 mosaic size (318x180)", v.shape[1:3] == (180, 318), list(v.shape[1:3]), [180, 318]),
            check("negative control: a single full-frame clip has no coloured panels", not max(panels(vr)) < 4, [round(x, 1) for x in panels(vr)], ">=4")], [out]


GAPS.update({
    "CAM-119": "needs the subject matte and the repo's scripts/safe-zones.cjs (not present in this checkout); a safe-zone map from a matte cannot be produced without them",
    "CAM-184": "Kling's simple camera_control is executed by the paid Kling video API (key required); a config validator alone cannot show the camera move",
})
