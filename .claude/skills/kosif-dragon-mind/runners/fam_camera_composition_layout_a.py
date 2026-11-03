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


def chrome_run(wd: Path, name: str, html: str, size=(320, 180), screenshot=False, budget=2000):
    """Run a page in headless Chrome; return the JSON the page wrote into #OUT (and the screenshot path)."""
    if not CHROME:
        raise RuntimeError("google-chrome not found")
    page = wd / ("%s.html" % name)
    page.write_text(html, encoding="utf-8")
    base = [CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
            "--disable-extensions", "--allow-file-access-from-files", "--window-size=%d,%d" % size,
            "--virtual-time-budget=%d" % budget]
    done = subprocess.run(base + ["--dump-dom", page.as_uri()], capture_output=True, text=True, timeout=40,
                          stdin=subprocess.DEVNULL)
    m = re.search(r'<pre id="OUT">(.*?)</pre>', done.stdout, re.S)
    if not m:
        raise RuntimeError("page produced no #OUT: " + done.stderr[-300:])
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
function __quad(el){ return __probe(el).map(d=>{const r=d.getBoundingClientRect(); return [r.left, r.top];}); }
function __op(el){ let o=1; for(let e=el; e && e.nodeType===1; e=e.parentElement){ o*=parseFloat(getComputedStyle(e).opacity); } return o; }
function __blur(el){ let b=0; for(let e=el; e && e.nodeType===1; e=e.parentElement){ const m=/blur\(([\d.]+)px\)/.exec(getComputedStyle(e).filter||''); if(m) b+=parseFloat(m[1]); } return b; }
function SAMPLE(times, sels, extra){ const els=sels.map(s=>document.querySelector(s)); els.forEach(__probe); const fr=[];
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


def blob(frame, rgb, tol=40, bg=None):
    """Centroid, area, orientation (deg) of one marker colour; None when absent. With bg (the known flat background)
    antialiased edge pixels count by their coverage, so centroids and areas are sub-pixel."""
    f = frame[..., :3].astype(float)
    c = np.array(rgb, float)
    if bg is not None:
        b = np.array(bg, float)
        v = c - b
        a = np.clip(((f - b) @ v) / (v @ v), 0, 1)
        resid = np.abs(f - (b + a[..., None] * v)).max(-1)
        w = np.where((resid < 30) & (a > 0.04), a, 0.0)
    else:
        w = (np.abs(f - c).max(-1) <= tol).astype(float)
    tot = w.sum()
    if tot < 3:
        return None
    ys, xs = np.mgrid[0:f.shape[0], 0:f.shape[1]]
    cx, cy = (w * xs).sum() / tot, (w * ys).sum() / tot
    mxx, myy, mxy = (w * (xs - cx) ** 2).sum() / tot, (w * (ys - cy) ** 2).sum() / tot, (w * (xs - cx) * (ys - cy)).sum() / tot
    ang = 0.5 * math.degrees(math.atan2(2 * mxy, mxx - myy))
    yy, xx = np.nonzero(w > 0.5)
    if len(xx) == 0:
        yy, xx = np.nonzero(w > 0)
    return {"cx": float(cx), "cy": float(cy), "area": float(tot), "ang": ang,
            "x0": int(xx.min()), "x1": int(xx.max()), "y0": int(yy.min()), "y1": int(yy.max())}


def track_colors(frames, cols, tol=40, bg=None):
    return [[blob(f, c, tol, bg) for c in cols] for f in frames]


def dom2d(wd, name, body, js, sels, colors, times, fps, W=320, H=180, css="", extra_js="null", scripts=None):
    """Run motion-kit/GSAP in Chrome, paint the tracked quads, write the output video, measure it back."""
    scripts = [GSAP, MKIT] if scripts is None else scripts
    full = DOM_SAMPLER + "const M=window.MOTION, E=M&&M.E; let tl=gsap.timeline({paused:true});\n" + js + \
        "\nOUT({frames: SAMPLE(%s, %s, %s)});" % (json.dumps(times), json.dumps(sels), extra_js)
    out, _ = chrome_run(wd, name, page(body, full, scripts, W, H, css), (W, H + 40))
    frames = out["frames"]
    rgbs = [hex2rgb(c) if c else None for c in colors]
    pix = paint_frames(frames, rgbs, W, H)
    vid = write_video(wd / ("%s.mp4" % name), pix, fps)
    meas = track_colors(read_video(vid), [c for c in rgbs if c], bg=(119, 119, 119))
    (wd / ("%s_samples.json" % name)).write_text(json.dumps(frames), encoding="utf-8")
    still = [pix[0]] * len(pix)                       # the unprocessed input: the first frame held
    inp = write_video(wd / ("%s_input.mp4" % name), still, fps)
    meas_in = track_colors(read_video(inp), [c for c in rgbs if c], bg=(119, 119, 119))
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


def run_tl(wd, name, body, js, sels, colors, dur, fps, crits, W=320, H=180, css="", extra_js="null", t0=0.0, scripts=None):
    T = [round(t0 + i / fps, 6) for i in range(int(round(dur * fps)) + 1)]
    r = dom2d(wd, name, body, js, sels, colors, T, fps, W, H, css, extra_js, scripts)
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
    js = "const tw=M.rackFocus(tl,'#subj',0.5,{blur:18,dur:0.3}); tw.id='twin';"
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
                ("the move starts slow (E.cam: <12%% at 20%% time)", lambda m, f: ((dd(m)[idx(T, 0.2 * dur)] - 1) / (sc - 1) < 0.12,
                                                                                    float((dd(m)[idx(T, 0.2 * dur)] - 1) / (sc - 1))), "<0.12")]
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
        ph1 = [1 + 0.2 * EZ["cam"](min(1, t / 1.4)) for t in T if t <= 1.5]
        ph2 = [log_push(1.2, 2.2, min(1, (t - 1.5) / 1.2), EZ["cam"]) for t in T if 1.5 <= t <= 2.8]
        i15, i28 = idx(T, 1.5), idx(T, 2.8)
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
          "tl.fromTo('#stage',{x:-8},{x:8,duration:.05,yoyo:true,repeat:7,ease:'none'},0.2);tl.set('#stage',{x:0},0.66);")

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
    return run_tl(wd, "punch_shake", STAGE, js, ["#mk", "#mb"], [RED, BLUE], 1.6, 120, crits)


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
    checks, outs = run_tl(wd, "microshake", body, js, ["#mk", "#mb", "#dim"], [RED, BLUE, "#000000"], 0.4, fps, crits, t0=10.77)
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
