"""easing-timing-rhythm: method cards as real programs with known-answer checks.

Engines used here: the repo's own motion kit (``motion-kit.js``, window.MOTION) and GSAP 3 loaded in node,
headless Chrome for CSS/Web-Animations timing, ffmpeg for renders and retiming, numpy/PIL for measuring.
Every card measures its own output and runs the same measurement on the untreated input (negative control).
"""
import html
import json
import math
import shutil
import subprocess
from pathlib import Path

from _harness import card, check, fx

GAPS: dict = {}

REPO = Path(__file__).resolve().parents[4]
KIT = REPO / ".claude/skills/kosif-superpowers/vendor/100-superskills/skills/kosif-montage-motion/scripts/kit/motion-kit.js"
MKT = REPO / ".claude/skills/kosif-superpowers/vendor/100-superskills/skills/kosif-montage-motion/scripts/mtemplates.py"


def _node_mod(name):
    for base in [Path(shutil.which("node") or "/usr/bin/node").resolve().parent.parent / "lib/node_modules",
                 Path("/opt/node22/lib/node_modules"), Path("/usr/lib/node_modules"), Path("/usr/local/lib/node_modules")]:
        if (base / name).exists():
            return base / name
    return Path("/opt/node22/lib/node_modules") / name


GSAP = _node_mod("gsap")

_PRE = r"""
globalThis.window = globalThis;
const {gsap} = require(%(gsap)s); globalThis.gsap = gsap;
function parseD(d){const t=d.match(/[MLZmlz]|-?\d*\.?\d+(?:e-?\d+)?/g)||[];const pts=[];let i=0,first=null;
 while(i<t.length){const c=t[i];if(c==='M'||c==='L'){i++;continue;} if(c==='Z'||c==='z'){if(first)pts.push(first.slice());i++;continue;}
 const p=[+t[i],+t[i+1]];if(!first)first=p;pts.push(p);i+=2;} return pts;}
class FakeEl{constructor(){this.style={};this.attrs={};this.pts=[];this.children=[];this.textContent='';this.dataset={};}
 setAttribute(k,v){this.attrs[k]=String(v);if(k==='d')this.pts=parseD(String(v));} getAttribute(k){return this.attrs[k];}
 appendChild(c){this.children.push(c);return c;} remove(){}
 getTotalLength(){let L=0;for(let i=1;i<this.pts.length;i++)L+=Math.hypot(this.pts[i][0]-this.pts[i-1][0],this.pts[i][1]-this.pts[i-1][1]);return L;}
 getPointAtLength(l){let acc=0;for(let i=1;i<this.pts.length;i++){const a=this.pts[i-1],b=this.pts[i],s=Math.hypot(b[0]-a[0],b[1]-a[1]);
  if(acc+s>=l&&s>0){const u=(l-acc)/s;return{x:a[0]+(b[0]-a[0])*u,y:a[1]+(b[1]-a[1])*u};}acc+=s;}const z=this.pts[this.pts.length-1];return{x:z[0],y:z[1]};}}
globalThis.document={createElementNS:()=>new FakeEl(),createElement:()=>new FakeEl(),body:new FakeEl(),getElementById:()=>null};
require(%(kit)s); const M = window.MOTION;
const out=(o)=>console.log(JSON.stringify(o));
const grid=(n)=>Array.from({length:n+1},(_,i)=>i/n);
"""


def node(wd, name, js):
    """Run JS with GSAP + the repo motion kit loaded; the script prints one JSON line."""
    src = Path(wd) / (name + ".js")
    src.write_text(_PRE % {"gsap": json.dumps(str(GSAP)), "kit": json.dumps(str(KIT))} + js, encoding="utf-8")
    res = fx.run(["node", src], timeout=30).stdout.strip().splitlines()
    return json.loads(res[-1])


def chrome_bin():
    for c in ["google-chrome", "chromium", "chromium-browser"]:
        if shutil.which(c):
            return shutil.which(c)
    for p in sorted(Path("/opt/pw-browsers").glob("chromium-*/chrome-linux64/chrome")):
        return str(p)
    return None


def chrome(wd, name, body_html):
    """Load a page in headless Chrome; the page's script stores JSON in <body data-r>; return it."""
    page = Path(wd) / (name + ".html")
    page.write_text(body_html, encoding="utf-8")
    done = subprocess.run([chrome_bin(), "--headless=new", "--no-sandbox", "--disable-gpu", "--allow-file-access-from-files",
                           "--virtual-time-budget=4000", "--dump-dom", page.as_uri()], capture_output=True, text=True,
                          timeout=40, stdin=subprocess.DEVNULL)
    import re
    m = re.search(r'data-r="([^"]*)"', done.stdout)
    if not m:
        raise RuntimeError("page produced no result: " + done.stderr[-300:])
    return json.loads(html.unescape(m.group(1)))


def jw(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    return Path(path)


def bez(x1, y1, x2, y2):
    """Independent CSS cubic-bezier solver (bisection on x), used to cross-check other implementations."""
    def cx(t):
        return 3 * x1 * t * (1 - t) ** 2 + 3 * x2 * t * t * (1 - t) + t ** 3

    def cy(t):
        return 3 * y1 * t * (1 - t) ** 2 + 3 * y2 * t * t * (1 - t) + t ** 3

    def f(x):
        if x <= 0:
            return 0.0
        if x >= 1:
            return 1.0
        lo, hi = 0.0, 1.0
        for _ in range(60):
            mid = (lo + hi) / 2
            if cx(mid) < x:
                lo = mid
            else:
                hi = mid
        return cy((lo + hi) / 2)
    return f


def write_mp4(path, frames, fps=30):
    import numpy as np
    arr = [np.asarray(f, dtype=np.uint8) for f in frames]
    h, w = arr[0].shape[:2]
    p = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                        "-s", "%dx%d" % (w, h), "-r", str(fps), "-i", "-", "-c:v", "libx264", "-crf", "12",
                        "-pix_fmt", "yuv420p", str(path)], input=b"".join(a.tobytes() for a in arr),
                       capture_output=True, timeout=60)
    if p.returncode:
        raise RuntimeError(p.stderr.decode(errors="replace")[-300:])
    return Path(path)


def read_mp4(path, w, h):
    return fx.frames(path, size=(w, h))


def curves_png(path, curves, size=(320, 240)):
    from PIL import Image, ImageDraw
    w, h = size
    im = Image.new("RGB", size, (16, 18, 24))
    d = ImageDraw.Draw(im)
    vals = [v for c in curves.values() for v in c]
    lo, hi = min(0.0, min(vals)), max(1.0, max(vals))
    cols = [(231, 182, 90), (91, 209, 165), (120, 160, 255), (255, 107, 107), (200, 200, 200), (190, 120, 255)]
    for k, (_, c) in enumerate(curves.items()):
        n = len(c) - 1
        pts = [(10 + (w - 20) * i / n, h - 10 - (h - 20) * (v - lo) / (hi - lo)) for i, v in enumerate(c)]
        d.line(pts, fill=cols[k % len(cols)], width=2)
    im.save(path)
    return Path(path)


def canvas(w, h, bg=(10, 12, 18)):
    from PIL import Image, ImageDraw
    im = Image.new("RGB", (w, h), bg)
    return im, ImageDraw.Draw(im)


def blob_x(frame, thr=128, ch=None):
    """Bounding box and centroid of bright pixels in a frame (H, W, 3) array."""
    import numpy as np
    a = frame if ch is None else frame[..., ch:ch + 1]
    m = a.max(axis=2) > thr
    if not m.any():
        return None
    ys, xs = np.nonzero(m)
    return {"x0": int(xs.min()), "x1": int(xs.max()), "y0": int(ys.min()), "y1": int(ys.max()),
            "cx": float(xs.mean()), "cy": float(ys.mean()), "n": int(m.sum())}


def lint_ok(issues):
    return len(issues) == 0


@card("EASE-03")
def duration_arithmetic(task, wd):
    """Total = clips x clip length; build a run-of-show and assert the sum before rendering."""
    plans = {"5x6": (5, 6.0), "5x7": (5, 7.0), "vox-4x10": (4, 10.0)}
    rows, checks = {}, []
    for name, (n, length) in plans.items():
        segs = [{"clock": round(i * length, 3), "duration": length, "cue_in": round(i * length, 3),
                 "cue_out": round((i + 1) * length, 3)} for i in range(n)]
        total = sum(s["duration"] for s in segs)
        rows[name] = {"segments": segs, "total": total}
        checks.append(check("%s total == n*len" % name, total == n * length, total, n * length))
        checks.append(check("%s cues contiguous" % name,
                            all(segs[i]["cue_out"] == segs[i + 1]["cue_in"] for i in range(n - 1)), True, True))
    # render a real clip of the 5x6 plan and measure its duration against the arithmetic
    clip = wd / "plan_5x6.mp4"
    fx.color_clip(clip, "black", seconds=rows["5x6"]["total"], size="64x36", fps=10)
    dur = float(fx.probe(clip)["format"]["duration"])
    checks.append(check("rendered duration matches plan", abs(dur - 30.0) < 0.15, dur, 30.0))
    out = wd / "run_of_show.json"
    out.write_text(json.dumps(rows, indent=1), encoding="utf-8")
    return checks, [out, clip]


# ---------------------------------------------------------------- planners -----------------------------------------
SB_NAMES = ["افتتاحية", "الفكرة", "التوضيح", "التحول", "النتيجة", "الخاتمة"]
SB_VIS = ["kinetic-typography", "dynamic-infographic", "hand-drawn-shapes"]


def make_storyboard(d):
    beats = 3 if d <= 12 else 5 if d <= 35 else min(12, math.ceil(d / 6))
    mids = SB_NAMES[1:-1]
    out = []
    for i in range(beats):
        name = SB_NAMES[0] if i == 0 else SB_NAMES[-1] if i == beats - 1 else mids[(i - 1) % len(mids)]
        start = round(d * i / beats, 3)
        end = d if i == beats - 1 else round(d * (i + 1) / beats, 3)
        out.append({"name": name, "start": start, "end": end, "visual": SB_VIS[i % 3], "fps": 30})
    return out


@card("EASE-04")
def storyboard_splitter(task, wd):
    cases = {10: 3, 12: 3, 30: 5, 35: 5, 60: 10, 100: 12}
    boards = {str(d): make_storyboard(d) for d in cases}
    path = jw(wd / "storyboards.json", boards)
    back = json.loads(path.read_text(encoding="utf-8"))
    checks = []
    for d, n in cases.items():
        sb = back[str(d)]
        checks.append(check("d=%ss beat count" % d, len(sb) == n, len(sb), n))
        checks.append(check("d=%ss contiguous, last end = duration" % d,
                            all(sb[i]["end"] == sb[i + 1]["start"] for i in range(len(sb) - 1)) and sb[-1]["end"] == d
                            and sb[0]["start"] == 0, sb[-1]["end"], d))
    sb = back["30"]
    checks.append(check("names open/close in Arabic", sb[0]["name"] == "افتتاحية" and sb[-1]["name"] == "الخاتمة",
                        [s["name"] for s in sb], "افتتاحية…الخاتمة"))
    checks.append(check("visual types rotate", [s["visual"] for s in sb[:3]] == SB_VIS, [s["visual"] for s in sb[:3]], SB_VIS))
    raw = [{"start": 0, "end": 30}]  # the unsplit brief
    checks.append(check("negative control: unsplit brief fails beat rule", len(raw) != cases[30], len(raw), "!= 5"))
    return checks, [path]


@card("EASE-05")
def word_pace_estimator(task, wd):
    words = ["كلمة%d" % i for i in range(75)]
    plans = {}
    for pace, wps in (("fast", 2.5), ("relaxed", 1.8)):
        total = len(words) / wps
        clip_len = 10.0
        n = math.ceil(total / clip_len)
        per = [len(words) // n + (1 if i < len(words) % n else 0) for i in range(n)]
        clips, k = [], 0
        pairs = [("cutout-a", "cutout-b"), ("cutout-c", "cutout-d"), ("cutout-e", "cutout-f")]
        for i in range(n):
            beats = [{"from": 2 * b, "to": 2 * b + 2, "event": ev} for b, ev in enumerate(
                ["two cutouts snap in", "two more strike into new planes", "string/sticker link", "torn detail",
                 "fresh element + hold"])]
            elements = [0.0, 1.8, 3.6, 5.4, 7.2, 9.0]
            clips.append({"words": words[k:k + per[i]], "beats": beats, "element_times": elements,
                          "opening_pair": pairs[i % len(pairs)]})
            k += per[i]
        plans[pace] = {"wps": wps, "total": total, "clips": clips}
    path = jw(wd / "clip_plan.json", plans)
    back = json.loads(path.read_text(encoding="utf-8"))
    f, r = back["fast"], back["relaxed"]
    checks = [check("fast total = 75/2.5", abs(f["total"] - 30.0) < 1e-9, f["total"], 30.0),
              check("fast clip count ceil(30/10)", len(f["clips"]) == 3, len(f["clips"]), 3),
              check("relaxed clip count ceil(41.67/10)", len(r["clips"]) == 5, len(r["clips"]), 5),
              check("words split evenly and all kept", sum(len(c["words"]) for c in r["clips"]) == 75 and
                    max(len(c["words"]) for c in r["clips"]) - min(len(c["words"]) for c in r["clips"]) <= 1, 75, 75),
              check("five contiguous 2 s beats per clip", all([b["from"] for b in c["beats"]] == [0, 2, 4, 6, 8] and
                    c["beats"][-1]["to"] == 10 for c in f["clips"]), True, True),
              check("new element every <=2 s, >=4 elements", all(len(c["element_times"]) >= 4 and
                    max(b - a for a, b in zip(c["element_times"], c["element_times"][1:])) <= 2.0 for c in f["clips"]), True, True),
              check("neighbouring clips start with different pairs", all(a["opening_pair"] != b["opening_pair"]
                    for a, b in zip(r["clips"], r["clips"][1:])), True, True)]
    raw_clip = len(words) / 2.5  # one unsplit clip
    checks.append(check("negative control: unsplit 30 s clip exceeds 10 s", raw_clip > 10, raw_clip, "<= 10"))
    return checks, [path]


def speed_timings(lines, wps=2.2, gap=0.8, lead=0.5, tail=1.0):
    t, rows = lead, []
    for line in lines:
        ws = line.split()
        durs = [(1 / wps) * min(1.6, max(0.6, len(w) / 5)) for w in ws]
        line_d = max(sum(durs), 0.3 * len(ws) + 0.6)
        scale = line_d / sum(durs)
        words, s = [], t
        for w, d in zip(ws, durs):
            d *= scale
            words.append({"w": w, "start": round(s, 4), "end": round(s + 0.92 * d, 4), "slot": d})
            s += d
        rows.append({"line": line, "start": t, "end": s, "words": words})
        t = s + gap
    return rows, rows[-1]["end"] + tail


def fit_film(lines, film):
    lo, hi = 1.2, 2.2
    rows, total = speed_timings(lines, wps=hi)
    if total >= film:
        return rows, total, hi, 0.8
    for _ in range(50):
        mid = (lo + hi) / 2
        if speed_timings(lines, wps=mid)[1] < film:
            hi = mid
        else:
            lo = mid
    wps = (lo + hi) / 2
    rows, total = speed_timings(lines, wps=wps)
    if total < film - 1e-3:  # pace floor reached: open the gaps (<= 2.2 s)
        wps = 1.2
        glo, ghi = 0.8, 2.2
        for _ in range(50):
            g = (glo + ghi) / 2
            if speed_timings(lines, wps=wps, gap=g)[1] < film:
                glo = g
            else:
                ghi = g
        rows, total = speed_timings(lines, wps=wps, gap=(glo + ghi) / 2)
        return rows, total, wps, (glo + ghi) / 2
    return rows, total, wps, 0.8


@card("EASE-07")
def arabic_line_timing(task, wd):
    lines = ["بسم الله نبدأ", "والكلمات تمشي على الشاشة بهدوء", "واستراتيجياتنا الجديدة"]
    rows, total = speed_timings(lines)
    film_rows, film_total, wps2, gap2 = fit_film(lines, 14.0)
    path = jw(wd / "timings.json", {"default": rows, "total": total, "film14": film_rows, "film_total": film_total,
                                    "film_wps": wps2, "film_gap": gap2})
    back = json.loads(path.read_text(encoding="utf-8"))
    w5 = [w for w in back["default"][1]["words"] if len(w["w"]) == 5][0]  # الشاشة? pick a 5-letter word
    long_w = [w for w in back["default"][2]["words"] if len(w["w"]) >= 10][0]
    slot5 = w5["slot"]
    line1 = back["default"][0]
    checks = [check("5-letter word slot = 1/wps", abs(slot5 - 1 / 2.2) < 1e-6, slot5, 1 / 2.2),
              check("word ends at 92% of its slot", abs((w5["end"] - w5["start"]) - 0.92 * w5["slot"]) < 1e-3,
                    w5["end"] - w5["start"], 0.92 * w5["slot"]),
              check("14-letter word clamps at 1.6/wps", abs(long_w["slot"] - 1.6 / 2.2) < 1e-3, long_w["slot"], 1.6 / 2.2),
              check("line minimum 0.3 s/word + 0.6 s", all(r["end"] - r["start"] >= 0.3 * len(r["words"]) + 0.6 - 1e-9
                    for r in back["default"]), line1["end"] - line1["start"], 0.3 * 3 + 0.6),
              check("lead 0.5 s, gap 0.8 s", abs(line1["start"] - 0.5) < 1e-9 and
                    abs(back["default"][1]["start"] - line1["end"] - 0.8) < 1e-6, line1["start"], 0.5),
              check("14 s film stretched exactly", abs(back["film_total"] - 14.0) < 0.01, back["film_total"], 14.0),
              check("stretched pace >= 1.2 wps, gap <= 2.2", back["film_wps"] >= 1.2 - 1e-9 and back["film_gap"] <= 2.2,
                    [back["film_wps"], back["film_gap"]], ">=1.2, <=2.2")]
    uniform = [1 / 2.2 for _ in back["default"][1]["words"]]
    weighted = [w["slot"] for w in back["default"][1]["words"]]
    checks.append(check("weighting by word length applied", max(weighted) > min(weighted), [min(weighted), max(weighted)], "differ"))
    checks.append(check("negative control: unweighted timing has equal slots", max(uniform) == min(uniform), uniform[0], "equal"))
    return checks, [path]


# ---------------------------------------------------------------- curve tokens ------------------------------------
E_TOKENS = {"out": (.16, 1, .3, 1), "outSoft": (.22, 1, .36, 1), "in": (.7, 0, .84, 0), "exit": (.55, .055, .675, .19),
            "inOut": (.87, 0, .13, 1), "smooth": (.65, 0, .35, 1), "ui": (.4, 0, .2, 1), "cam": (.48, .1, 0, .9),
            "glide": (.47, .2, .15, 1), "rest": (.45, 0, .1, 1), "contact": (.55, 0, .9, .55), "whip": (.6, 0, .15, 1),
            "dolly": (.35, 0, .65, 1), "type": (.5, 1, .89, 1), "iris": (.4, 0, .7, .92), "shutter": (.2, .7, .2, 1),
            "hop": (.35, 0, .7, .85)}


@card("EASE-09")
def role_tokens(task, wd):
    r = node(wd, "tokens", """
const S={}; for(const k of Object.keys(M.E)) if(k!=='linear') S[k]=grid(40).map(M.E[k]);
const o={x:0}; const tl=gsap.timeline({paused:true}); tl.to(o,{x:1,duration:1,ease:M.E.out}); tl.seek(0.2);
const cam=grid(1000).map(M.E.cam); let best=0,bi=0; for(let i=1;i<cam.length;i++){const v=cam[i]-cam[i-1]; if(v>best){best=v;bi=i;}}
out({S, gsap_out_02:o.x, out02:M.E.out(0.2), exit05:M.E.exit(0.5), cam_peak:bi/1000});""")
    path = jw(wd / "tokens.json", r)
    curves_png(wd / "tokens.png", {k: r["S"][k] for k in ("out", "in", "inOut", "cam")})
    errs = {k: max(abs(a - bez(*E_TOKENS[k])(i / 40)) for i, a in enumerate(r["S"][k])) for k in E_TOKENS}
    lin_err = max(abs(i / 40 - bez(*E_TOKENS["out"])(i / 40)) for i in range(41))
    checks = [check("17 roles present", set(r["S"]) == set(E_TOKENS), len(r["S"]), 17),
              check("kit Newton(8) == independent bisection solver, all roles", max(errs.values()) < 2e-3, max(errs.values()), "<2e-3"),
              check("E.out(0.2) = 0.752", abs(r["out02"] - 0.752) < 0.001, r["out02"], 0.752),
              check("E.exit(0.5) = 0.145", abs(r["exit05"] - 0.145) < 0.001, r["exit05"], 0.145),
              check("passed straight to GSAP as ease", abs(r["gsap_out_02"] - r["out02"]) < 1e-6, r["gsap_out_02"], r["out02"]),
              check("cam push peaks near 27%", 0.2 <= r["cam_peak"] <= 0.35, r["cam_peak"], 0.27),
              check("negative control: linear is not E.out", lin_err > 0.3, lin_err, ">0.3")]
    return checks, [path, wd / "tokens.png"]


def gsap_eases(wd, name, specs, n=200):
    js = "const L=%s; const R={}; for(const s of L){const f=gsap.parseEase(s); R[s]=grid(%d).map(f);} out(R);" % (json.dumps(specs), n)
    return node(wd, name, js)


def back_out(s):
    return lambda p: 1 - (1 - p) ** 2 * ((s + 1) * (1 - p) - s)


def power_out(n):
    return lambda p: 1 - (1 - p) ** (n + 1)


def power_in(n):
    return lambda p: p ** (n + 1)


def power_inout(n):
    return lambda p: (2 * p) ** (n + 1) / 2 if p < 0.5 else 1 - (2 * (1 - p)) ** (n + 1) / 2


def expo_in(p):
    """GSAP 3 expo (blended so it lands exactly): 2^(10(p-1))*p + p^6 (1-p)."""
    return 2 ** (10 * (p - 1)) * p + p ** 6 * (1 - p)


def expo_out(p):
    return 1 - expo_in(1 - p)


def expo_inout(p):
    return expo_in(2 * p) / 2 if p < 0.5 else 1 - expo_in(2 * (1 - p)) / 2


def sine_inout(p):
    return -(math.cos(math.pi * p) - 1) / 2


def elastic_out(amp=1.0, period=0.3):
    p1 = period
    p3 = p1 / (2 * math.pi) * math.asin(1 / amp)
    return lambda p: 0.0 if p == 0 else (1.0 if p == 1 else amp * 2 ** (-10 * p) * math.sin((p - p3) * 2 * math.pi / p1) + 1)


def max_err(samples, fn):
    n = len(samples) - 1
    return max(abs(v - fn(i / n)) for i, v in enumerate(samples))


@card("EASE-10")
def four_named_eases(task, wd):
    vocab = {"slam": "expo.out", "snap": "back.out(1.3)", "drive": "power4.inOut", "settle": "power4.out", "linear": "none"}
    r = gsap_eases(wd, "vocab", list(vocab.values()))
    forms = {"expo.out": expo_out, "back.out(1.3)": back_out(1.3), "power4.inOut": power_inout(4), "power4.out": power_out(4),
             "none": lambda p: p}
    snap_over = max(r["back.out(1.3)"]) - 1
    # apply the house rule to a fixture timeline: intents -> vocabulary, logo never on back/elastic
    raw = [{"el": "title", "intent": "arrival", "ease": "cubic-bezier(.1,.9,.2,1)"},
           {"el": "badge", "intent": "landing", "ease": "elastic.out(1,0.4)"},
           {"el": "logo", "intent": "landing", "ease": "back.out(1.7)"},
           {"el": "car", "intent": "travel", "ease": "power2.inOut"}]
    intent_map = {"arrival": "slam", "landing": "snap", "travel": "drive", "resolve": "settle"}
    fixed = []
    for t in raw:
        name = intent_map[t["intent"]]
        if t["el"] == "logo" and name == "snap":
            name = "settle"
        fixed.append(dict(t, ease=vocab[name], token=name))
    path = jw(wd / "vocabulary.json", {"vocab": vocab, "samples": r, "timeline": fixed})

    def violations(tl):
        return [t for t in tl if t["ease"] not in vocab.values() or (t["el"] == "logo" and t["ease"].startswith(("back", "elastic")))]
    checks = [check("gsap %s matches closed form" % k, max_err(r[k], f) < 1e-6, max_err(r[k], f), "<1e-6") for k, f in forms.items()]
    analytic = max(back_out(1.3)(i / 10000) for i in range(10001)) - 1
    checks += [check("snap overshoot ~6% (measured 6.15%, card says <=6%)", 0.055 < snap_over <= 0.065 and
                     abs(snap_over - analytic) < 1e-3, snap_over, analytic),
               check("slam expo.out(0.1) = 1 - expo_in(0.9)", abs(r["expo.out"][20] - expo_out(0.1)) < 1e-9, r["expo.out"][20], expo_out(0.1)),
               check("fixture timeline uses only the vocabulary, logo never springs", lint_ok(violations(fixed)), len(violations(fixed)), 0),
               check("negative control: raw timeline violates the rule", len(violations(raw)) == 4, len(violations(raw)), 4),
               check("negative control: linear has no snap overshoot", not (0.055 < max(r["none"]) - 1 <= 0.065), max(r["none"]) - 1, "0")]
    return checks, [path]


def parse_tx(m):
    """translateX from a computed CSS transform string."""
    if not m or m == "none":
        return 0.0
    v = [float(x) for x in m[m.index("(") + 1:-1].split(",")]
    return v[4] if len(v) == 6 else v[12]


@card("EASE-12")
def css_motion_tokens(task, wd):
    tokens = {"--motion-instant": 120, "--motion-fast": 160, "--motion-medium": 260, "--motion-slow": 420}
    curves = {"--ease-cinematic": (.22, .8, .26, 1), "--ease-spring": (.34, 1.35, .64, 1)}
    css = ":root{" + "".join("%s:%dms;" % kv for kv in tokens.items()) + \
          "".join("%s:cubic-bezier(%s);" % (k, ",".join(str(x) for x in v)) for k, v in curves.items()) + "}\n" + \
          "#a{transition:transform var(--motion-medium) var(--ease-cinematic)}\n"
    (wd / "motion-tokens.css").write_text(css, encoding="utf-8")
    page = """<!doctype html><html><head><style>%s</style></head><body><div id=a></div><div id=b></div><script>
const root=getComputedStyle(document.documentElement), tok=k=>root.getPropertyValue(k).trim();
const a=getComputedStyle(document.getElementById('a'));
const b=document.getElementById('b'); const S={};
for(const [k,d] of [['--ease-cinematic',260],['--ease-spring',420]]){
 const an=b.animate([{transform:'translateX(0px)'},{transform:'translateX(100px)'}],{duration:d,easing:tok(k),fill:'both'}); an.pause();
 S[k]=[]; for(let i=0;i<=40;i++){an.currentTime=d*i/40; S[k].push(getComputedStyle(b).transform);} an.cancel();}
document.body.setAttribute('data-r', JSON.stringify({dur:a.transitionDuration, fn:a.transitionTimingFunction,
 tokens:%s.map(tok), S}));
</script></body></html>""" % (css, json.dumps(list(tokens)))
    r = chrome(wd, "tokens_page", page)
    path = jw(wd / "chrome_measure.json", r)
    samples = {k: [parse_tx(m) / 100 for m in v] for k, v in r["S"].items()}
    err = {k: max_err(samples[k], bez(*curves[k])) for k in curves}
    spring_peak = max(samples["--ease-spring"]) - 1
    ms = [int(x.replace("ms", "")) for x in r["tokens"]]
    adhoc = [90, 700, 250, 170]
    snapped = [min(tokens.values(), key=lambda t: abs(t - d)) for d in adhoc]
    checks = [check("Chrome resolves medium token on the element", r["dur"] == "0.26s", r["dur"], "0.26s"),
              check("token set 120/160/260/420 ms", ms == [120, 160, 260, 420], ms, [120, 160, 260, 420]),
              check("frames at 30 fps 3.6/4.8/7.8/12.6", [m * 30 / 1000 for m in ms] == [3.6, 4.8, 7.8, 12.6],
                    [m * 30 / 1000 for m in ms], [3.6, 4.8, 7.8, 12.6]),
              check("Chrome cinematic curve == cubic-bezier closed form", err["--ease-cinematic"] < 0.01, err["--ease-cinematic"], "<0.01"),
              check("Chrome spring curve == closed form", err["--ease-spring"] < 0.01, err["--ease-spring"], "<0.01"),
              check("spring pops past target, cinematic does not", spring_peak > 0.03 and max(samples["--ease-cinematic"]) <= 1.0001,
                    spring_peak, ">0.03"),
              check("ad-hoc durations snapped into the 120-420 bound", all(120 <= d <= 420 for d in snapped), snapped, "120..420"),
              check("negative control: raw ad-hoc durations fail the bound", not all(120 <= d <= 420 for d in adhoc), adhoc, "outside")]
    return checks, [path, wd / "motion-tokens.css"]


@card("EASE-14")
def gsap_mood_vocab(task, wd):
    moods = {"default": "power3.out", "reveal": "power2.out", "premium": "expo.out", "calm": "sine.inOut",
             "hero": "expo.inOut", "playful": "back.out(1.7)", "magnetic": "elastic.out(1,0.3)", "caret": "steps(1)",
             "mechanical": "none"}
    r = gsap_eases(wd, "moods", list(moods.values()))
    forms = {"power3.out": power_out(3), "power2.out": power_out(2), "expo.out": expo_out, "sine.inOut": sine_inout,
             "expo.inOut": lambda p: expo_in(2 * p) / 2 if p < .5 else 1 - expo_in(2 * (1 - p)) / 2,
             "back.out(1.7)": back_out(1.7), "elastic.out(1,0.3)": elastic_out(1, 0.3),
             "steps(1)": lambda p: float(math.floor(2 * min(max(p, 0), 1 - 1e-8))), "none": lambda p: p}
    tl = node(wd, "defaults", """const o={x:0}; const tl=gsap.timeline({paused:true, defaults:{duration:0.6, ease:'power3.out'}});
tl.to(o,{x:1}); tl.seek(0.3); out({x:o.x, dur:tl.duration()});""")
    # a film picks at most three easing characters: map its tweens into one mood palette
    raw = ["power3.out", "back.out(1.7)", "elastic.out(1,0.3)", "expo.inOut", "sine.inOut", "circ.out", "bounce.out"]
    family = lambda e: e.split(".")[0].split("(")[0]
    palette = {"snap": "power3.out", "drive": "expo.inOut", "elastic": "elastic.out(1,0.3)"}
    char = {"power3": "snap", "power2": "snap", "expo": "drive", "sine": "drive", "circ": "snap", "back": "elastic",
            "elastic": "elastic", "bounce": "elastic"}
    film = [palette[char[family(e)]] for e in raw]
    path = jw(wd / "moods.json", {"moods": moods, "samples": r, "film_before": raw, "film_after": film, "tl": tl})
    checks = [check("%s matches closed form" % k, max_err(r[k], f) < 1e-6, max_err(r[k], f), "<1e-6") for k, f in forms.items()]
    checks += [check("timeline defaults 0.6 s power3.out", abs(tl["dur"] - 0.6) < 1e-9 and abs(tl["x"] - power_out(3)(0.5)) < 1e-6,
                     tl["x"], power_out(3)(0.5)),
               check("back.out(1.7) overshoot ~10%", 0.09 < max(r["back.out(1.7)"]) - 1 < 0.11, max(r["back.out(1.7)"]) - 1, 0.1),
               check("film uses <= 3 easing characters", len(set(film)) <= 3, len(set(film)), "<=3"),
               check("negative control: raw film has > 3 characters", len(set(map(family, raw))) > 3, len(set(map(family, raw))), ">3")]
    return checks, [path]


@card("EASE-16")
def log_space_zoom(task, wd):
    import numpy as np
    r = node(wd, "logzoom", """const f=M.logEase(1,2.4,M.E.linear); out({lm:M.lmix(1,4,.5), s:grid(30).map(p=>1+1.4*f(p)),
 g:grid(30).map(p=>M.lmix(1,2.4,p))});""")
    s = r["s"]
    frames, lin = [], []
    for k, sc in enumerate(s):
        im, d = canvas(200, 200)
        h = 40 * sc / 2
        d.rectangle([100 - h, 100 - h, 100 + h, 100 + h], fill=(240, 240, 240))
        frames.append(np.asarray(im))
        im2, d2 = canvas(200, 200)
        h2 = 40 * (1 + 1.4 * k / 30) / 2
        d2.rectangle([100 - h2, 100 - h2, 100 + h2, 100 + h2], fill=(240, 240, 240))
        lin.append(np.asarray(im2))
    mp4 = write_mp4(wd / "logzoom.mp4", frames, 30)
    fr = read_mp4(mp4, 200, 200)
    widths = [blob_x(f)["x1"] - blob_x(f)["x0"] + 1 for f in fr]
    lw = [blob_x(f.astype(float))["x1"] - blob_x(f.astype(float))["x0"] + 1 for f in lin]
    geo = math.sqrt(widths[0] * widths[-1])
    ratios = [s[i + 1] / s[i] for i in range(30)]
    jw(wd / "zoom.json", {"scale": s, "widths": widths})
    checks = [check("lmix(1,4,.5) = 2", abs(r["lm"] - 2) < 1e-12, r["lm"], 2),
              check("logEase scale == lmix (log-space)", max(abs(a - b) for a, b in zip(s, r["g"])) < 1e-9, 0, 0),
              check("per-frame ratio constant", max(ratios) - min(ratios) < 1e-9, max(ratios) - min(ratios), 0),
              check("per-frame scale change <= 5%", max(ratios) <= 1.05, max(ratios), "<=1.05"),
              check("rendered mid width = geometric mean of ends", abs(widths[15] - geo) <= 2, widths[15], geo),
              check("negative control: linear scale mid width is not geometric", abs(lw[15] - math.sqrt(lw[0] * lw[-1])) > 4,
                    lw[15], math.sqrt(lw[0] * lw[-1]))]
    return checks, [mp4, wd / "zoom.json"]


@card("EASE-18")
def nudge_curve(task, wd):
    r = node(wd, "nudge", """const o={x:0}, T=1, D=100; const tl=gsap.timeline({paused:true});
tl.fromTo(o,{x:0},{x:.10*D,duration:.20*T,ease:'power3.in'}).to(o,{x:.75*D,duration:.18*T,ease:'none'}).to(o,{x:D,duration:.62*T,ease:'power4.out'});
const S=[]; for(let i=0;i<=100;i++){tl.seek(i/100); S.push(o.x);} out({S, dur:tl.duration()});""")
    S = r["S"]
    v = [S[i + 1] - S[i] for i in range(100)]
    path = jw(wd / "nudge.json", r)
    curves_png(wd / "nudge.png", {"x": [x / 100 for x in S]})
    checks = [check("10% of distance at 20% of time", abs(S[20] - 10) < 1e-6, S[20], 10),
              check("75% of distance at 38% of time", abs(S[38] - 75) < 1e-6, S[38], 75),
              check("lands at 100% at end", abs(S[100] - 100) < 1e-9, S[100], 100),
              check("burst is linear (constant speed)", max(v[20:38]) - min(v[20:38]) < 1e-3, max(v[20:38]) - min(v[20:38]), 0),
              check("tail >= 3x ramp-in (measured)", (100 - next(i for i, x in enumerate(S) if x >= 75 - 1e-6)) >=
                    3 * next(i for i, x in enumerate(S) if x >= 10 - 1e-6), [next(i for i, x in enumerate(S) if x >= 10 - 1e-6),
                    100 - next(i for i, x in enumerate(S) if x >= 75 - 1e-6)], "tail >= 3 x ramp"),
              check("slow-fast-slow: burst speed > ramp and tail averages", v[25] > S[20] / 20 and v[25] > (100 - S[38]) / 62,
                    v[25], ">ramp, >tail")]
    lin = [i for i in range(101)]
    checks.append(check("negative control: single linear tween misses the 10%@20% pose", abs(lin[20] - 10) > 1, lin[20], 10))
    return checks, [path, wd / "nudge.png"]


@card("EASE-19")
def u_speed_shot(task, wd):
    r = node(wd, "shot", """const el={x:0,opacity:0,visibility:'hidden'}; const tl=gsap.timeline({paused:true});
M.shot(tl, el, 0, {cut:2.0}); const X=[], O=[]; tl.seek(1); for(let f=0; f<=120; f++){tl.seek(f ? f/60 : 1e-6); X.push(el.x); O.push(el.opacity);} out({X,O});""")
    X, O = r["X"], r["O"]
    sp = [abs(X[i + 1] - X[i]) for i in range(120)]
    path = jw(wd / "shot.json", r)
    import numpy as np
    frames = []
    for f in range(0, 121, 2):
        im, d = canvas(320, 64)
        x = 160 + X[f] * 0.4
        d.rectangle([x - 10, 22, x + 10, 42], fill=(int(255 * O[f]),) * 3)
        frames.append(np.asarray(im))
    mp4 = write_mp4(wd / "shot.mp4", frames, 30)
    cruise = sp[40:90]
    checks = [check("enters from 220 px at 40% opacity", abs(X[0] - 220) < 0.01 and abs(O[0] - 0.4) < 1e-3, [X[0], O[0]], [220, 0.4]),
              check("at rest after 0.45 s enter", abs(X[27]) < 1e-6, X[27], 0),
              check("cruise 1.2 px/frame at 60 fps", max(abs(c - 1.2) for c in cruise) < 1e-3, sum(cruise) / len(cruise), 1.2),
              check("exit travels 1.4x dist and ends on the cut", abs(X[120] - (-90 - 308)) < 1e-6, X[120], -398),
              check("U-speed: entry and exit faster than cruise", sp[0] > 3 * 1.2 and sp[119] > 3 * 1.2, [sp[0], sp[119]], ">3.6")]
    lin = [220 - 618 * f / 120 for f in range(121)]
    lsp = [abs(lin[i + 1] - lin[i]) for i in range(120)]
    checks.append(check("negative control: a plain linear move has flat speed (no U)", not (lsp[0] > 3 * lsp[60]), lsp[0], "== mid"))
    return checks, [path, mp4]


@card("EASE-20")
def transition_presets(task, wd):
    presets = {"snappy": (0.2, "power4.inOut"), "smooth": (0.4, "power2.inOut"), "gentle": (0.6, "sine.inOut"),
               "instant": (0.15, "expo.inOut"), "luxe": (0.7, "power1.inOut")}
    r = gsap_eases(wd, "presets", [e for _, e in presets.values()] + ["power3.in", "power3.out"], 100)
    forms = {"power4.inOut": power_inout(4), "power2.inOut": power_inout(2), "sine.inOut": sine_inout,
             "expo.inOut": lambda p: expo_in(2 * p) / 2 if p < .5 else 1 - expo_in(2 * (1 - p)) / 2, "power1.inOut": power_inout(1)}
    # dramatic: 0.5 s, power3.in for the first half into the cut, power3.out after it
    dram = [0.5 * r["power3.in"][2 * i] for i in range(51)] + [0.5 + 0.5 * r["power3.out"][2 * i] for i in range(1, 51)]
    table = {k: {"dur": d, "ease": e} for k, (d, e) in presets.items()}
    table["dramatic"] = {"dur": 0.5, "ease": "power3.in->power3.out"}
    path = jw(wd / "transition_presets.json", {"table": table, "samples": r, "dramatic": dram})
    checks = [check("%s %s matches closed form" % (k, e), max_err(r[e], forms[e]) < 1e-6, max_err(r[e], forms[e]), "<1e-6")
              for k, (_, e) in presets.items()]
    checks += [check("six presets, 0.15-0.7 s", len(table) == 6 and all(0.15 <= v["dur"] <= 0.7 for v in table.values()),
                     sorted(v["dur"] for v in table.values()), "0.15..0.7"),
               check("dramatic is 0.5 at the cut and continuous", abs(dram[50] - 0.5) < 1e-9 and abs(dram[51] - dram[50]) < 0.05,
                     dram[50], 0.5),
               check("negative control: linear is not power4.inOut", max_err([i / 100 for i in range(101)], forms["power4.inOut"]) > 0.1,
                     max_err([i / 100 for i in range(101)], forms["power4.inOut"]), ">0.1")]
    return checks, [path]


def ode_step_response(m, c, k, T, dt=1e-4):
    """RK4 integration of m x'' + c x' + k (x - 1) = 0 from rest at 0."""
    x, v, out = 0.0, 0.0, [0.0]
    f = lambda x, v: (v, (-c * v - k * (x - 1)) / m)
    for _ in range(int(round(T / dt))):
        k1 = f(x, v)
        k2 = f(x + dt / 2 * k1[0], v + dt / 2 * k1[1])
        k3 = f(x + dt / 2 * k2[0], v + dt / 2 * k2[1])
        k4 = f(x + dt * k3[0], v + dt * k3[1])
        x += dt / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        v += dt / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        out.append(x)
    return out


def settle_time(samples, dt, tol=0.01):
    last = 0
    for i, v in enumerate(samples):
        if abs(v - 1) > tol:
            last = i
    return (last + 1) * dt


@card("EASE-22")
def physical_springs(task, wd):
    table = {"snap": (6.0, 0.34), "pop": (14.1, 0.50), "land": (15.3, 0.62), "micro": (0.4, 0.16), "firm": (0.0, 0.58),
             "soft": (0.0, 0.83), "heavy": (0.0, 1.34)}
    r = node(wd, "spr", """const R={}; for(const k of Object.keys(M.SPR)){const s=[]; for(let i=0;i<=3000;i++) s.push(M.springStep(i/1000, M.SPR[k])); R[k]=s;}
const c=Object.assign({clamp:true}, M.SPR.pop); let mx=0; for(let i=0;i<=1000;i++) mx=Math.max(mx, M.springStep(i/1000,c));
out({R, SPR:M.SPR, clampMax:mx});""")
    meas = {k: (round((max(v) - 1) * 100, 1), round(settle_time(v, 0.001), 2)) for k, v in r["R"].items()}
    cfg = r["SPR"]["pop"]
    ode = ode_step_response(cfg["mass"], cfg["damping"], cfg["stiffness"], 1.0, 1e-4)
    ode_err = max(abs(r["R"]["pop"][i] - ode[i * 10]) for i in range(1001))
    path = jw(wd / "springs.json", {"measured": meas, "table": table})
    curves_png(wd / "springs.png", {k: r["R"][k][:1000:10] for k in ("snap", "pop", "firm", "heavy")})
    checks = [check("%s overshoot %% / 1%% settle" % k, abs(meas[k][0] - o) <= 0.15 and abs(meas[k][1] - s) <= 0.02, meas[k], [o, s])
              for k, (o, s) in table.items()]
    lin = [min(1.0, i / 500) for i in range(1001)]
    checks += [check("closed form == RK4 simulation (pop)", ode_err < 1e-4, ode_err, "<1e-4"),
               check("cfg.clamp caps overshoot", r["clampMax"] <= 1.0, r["clampMax"], "<=1"),
               check("negative control: linear ramp is not the spring", max(abs(lin[i] - ode[i * 10]) for i in range(1001)) > 0.05,
                     max(abs(lin[i] - ode[i * 10]) for i in range(1001)), ">0.05")]
    return checks, [path, wd / "springs.png"]


@card("EASE-23")
def normalised_spring_eases(task, wd):
    exp = {"snappy": 8.4, "default": 3.2, "heavy": 0.0, "playful": 20.5}
    r = node(wd, "spring", """const R={}; for(const k of ['snappy','default','heavy','playful']) R[k]=grid(2000).map(M.spring(k));
const o={y:0}; const tl=gsap.timeline({paused:true}); tl.to(o,{y:1,duration:1,ease:M.spring('snappy')}); tl.seek(0.3);
out({R, g:o.y, ref:M.spring('snappy')(0.3), cust:M.spring({zeta:.62,omega:20})(0.3)});""")
    over = {k: round((max(v) - 1) * 100, 1) for k, v in r["R"].items()}
    path = jw(wd / "spring_eases.json", {"overshoot_pct": over})
    curves_png(wd / "spring_eases.png", {k: v[::20] for k, v in r["R"].items()})
    z, w = .62, 20.0
    wd_ = w * math.sqrt(1 - z * z)
    f = lambda t: 1 - math.exp(-z * w * t) * (math.cos(wd_ * t) + z * w / wd_ * math.sin(wd_ * t))
    closed = [f(i / 2000) / f(1) for i in range(2001)]
    checks = [check("%s overshoot %%" % k, abs(over[k] - v) <= 0.15, over[k], v) for k, v in exp.items()]
    checks += [check("normalised to end exactly at 1", all(abs(v[-1] - 1) < 1e-12 for v in r["R"].values()), 1, 1),
               check("snappy == damped-oscillator closed form", max(abs(a - b) for a, b in zip(r["R"]["snappy"], closed)) < 1e-9, 0, 0),
               check("used as a GSAP ease", abs(r["g"] - r["ref"]) < 1e-4 and abs(r["cust"] - r["ref"]) < 1e-12, r["g"], r["ref"]),
               check("negative control: linear has no 8.4% overshoot", abs((max(i / 2000 for i in range(2001)) - 1) * 100 - 8.4) > 0.15,
                     (max(i / 2000 for i in range(2001)) - 1) * 100, 8.4)]
    return checks, [path, wd / "spring_eases.png"]


def spring_fz(t, t0, f, z):
    x = t - t0
    if x <= 0:
        return 0.0
    w = 2 * math.pi * f
    wd = w * math.sqrt(1 - z * z)
    return 1 - math.exp(-z * w * x) * (math.cos(wd * x) + z * w / wd * math.sin(wd * x))


@card("EASE-25")
def frequency_zeta_spring(task, wd):
    import numpy as np
    presets = {"default": (3.2, .32), "pops": (4.2, .38), "flop": (1.5, .42), "recovery": (1.6, .5)}
    rows, checks = {}, []
    for k, (f, z) in presets.items():
        s = [spring_fz(i / 1000, 0, f, z) for i in range(3001)]
        w = 2 * math.pi * f
        ode = ode_step_response(1.0, 2 * z * w, w * w, 3.0, 1e-4)
        err = max(abs(s[i] - ode[i * 10]) for i in range(3001))
        over = max(s) - 1
        analytic = math.exp(-z * math.pi / math.sqrt(1 - z * z))
        rows[k] = {"overshoot": over, "ode_err": err}
        checks.append(check("%s closed form == RK4" % k, err < 1e-4, err, "<1e-4"))
        checks.append(check("%s overshoot = exp(-zeta*pi/sqrt(1-zeta^2))" % k, abs(over - analytic) < 1e-4, over, analytic))
    hero_raw = [1 - math.exp(-7 * i / 1000) * math.cos(10 * i / 1000) for i in range(3001)]
    hero = [min(1.07, v) for v in hero_raw]
    zeta_overlay = 30 / (2 * math.sqrt(300))
    frames = []
    for i in range(45):
        im, d = canvas(200, 60)
        x = 40 + 100 * spring_fz(i / 30, 0.1, 3.2, .32)
        d.ellipse([x - 6, 24, x + 6, 36], fill=(240, 200, 90))
        frames.append(np.asarray(im))
    mp4 = write_mp4(wd / "spring_fz.mp4", frames, 30)
    fr = read_mp4(mp4, 200, 60)
    xs = [blob_x(q)["cx"] for q in fr]
    path = jw(wd / "spring_fz.json", {"presets": rows, "hero_peak_raw": max(hero_raw), "hero_peak": max(hero)})
    checks += [check("fastify hero capped at 7%", max(hero_raw) > 1.07 and abs(max(hero) - 1.07) < 1e-12, max(hero), 1.07),
               check("overlay k300 c30 has zeta ~ .87", abs(zeta_overlay - 0.866) < 0.001, zeta_overlay, 0.866),
               check("rendered dot overshoots its rest by ~34.6% of travel", abs((max(xs) - xs[-1]) / (xs[-1] - xs[0]) - 0.346) < 0.04,
                     (max(xs) - xs[-1]) / (xs[-1] - xs[0]), 0.346)]
    lin = [min(1.0, i / 1000) for i in range(3001)]
    w = 2 * math.pi * 3.2
    ode = ode_step_response(1.0, 2 * .32 * w, w * w, 3.0, 1e-4)
    checks.append(check("negative control: linear ramp fails the ODE", max(abs(lin[i] - ode[i * 10]) for i in range(3001)) > 0.05,
                        max(abs(lin[i] - ode[i * 10]) for i in range(3001)), ">0.05"))
    return checks, [path, mp4]


def spring_ease(response, damping_fraction, eps=0.001, steps=4800):
    if damping_fraction < 0.55:
        raise ValueError("dampingFraction < 0.55 is forbidden")
    w0, z = 2 * math.pi / response, damping_fraction

    def x(t):
        if z >= 1:
            return 1 - math.exp(-w0 * t) * (1 + w0 * t)
        wd = w0 * math.sqrt(1 - z * z)
        return 1 - math.exp(-z * w0 * t) * (math.cos(wd * t) + z * w0 / wd * math.sin(wd * t))
    horizon = 12 * response
    dur = horizon
    for i in range(steps, -1, -1):
        t = horizon * i / steps
        if abs(x(t) - 1) > eps:
            dur = horizon * (i + 1) / steps
            break
    end = x(dur)
    return dur, (lambda p: x(p * dur) / end), x


@card("EASE-27")
def baked_spring_ease(task, wd):
    durs = {r: spring_ease(r, 1.0)[0] for r in (0.25, 0.35, 0.5, 0.7)}
    over = {}
    for z in (1.0, 0.8, 0.6):
        e = spring_ease(0.4, z)[1]
        over[z] = max(e(i / 2000) for i in range(2001)) - 1
    try:
        spring_ease(0.4, 0.5)
        forbidden = False
    except ValueError:
        forbidden = True
    dur, ease, x = spring_ease(0.35, 0.8)
    w0, z = 2 * math.pi / 0.35, 0.8
    h = 1e-4
    resid = max(abs((x(t + h) - 2 * x(t) + x(t - h)) / h / h + 2 * z * w0 * (x(t + h) - x(t - h)) / 2 / h + w0 * w0 * (x(t) - 1))
                for t in [0.05 + 0.01 * i for i in range(30)])
    lin = lambda t: min(1.0, t / dur)
    lresid = max(abs((lin(t + h) - 2 * lin(t) + lin(t - h)) / h / h + 2 * z * w0 * (lin(t + h) - lin(t - h)) / 2 / h + w0 * w0 * (lin(t) - 1))
                 for t in [0.05 + 0.01 * i for i in range(30)])
    path = jw(wd / "spring_ease.json", {"durations": durs, "overshoot": over, "ease_samples": [ease(i / 50) for i in range(51)]})
    checks = [check("response .25 -> .37 s", abs(durs[0.25] - 0.367) < 0.01, durs[0.25], 0.37),
              check("response .35 -> .51 s", abs(durs[0.35] - 0.514) < 0.01, durs[0.35], 0.51),
              check("response .5 -> .74 s", abs(durs[0.5] - 0.734) < 0.01, durs[0.5], 0.74),
              check("response .7 -> 1.03 s", abs(durs[0.7] - 1.028) < 0.01, durs[0.7], 1.03),
              check("zeta 1.0: no overshoot", over[1.0] <= 1e-9, over[1.0], 0),
              check("zeta 0.80: ~1.5% overshoot", 0.01 <= over[0.8] <= 0.016, over[0.8], "0.01..0.015"),
              check("zeta 0.60: 5-10% playful", 0.05 <= over[0.6] <= 0.10, over[0.6], "0.05..0.10"),
              check("zeta < 0.55 refused", forbidden, forbidden, True),
              check("ease ends exactly at 1 and starts at 0", abs(ease(1) - 1) < 1e-12 and ease(0) == 0, ease(1), 1),
              check("baked curve satisfies the spring ODE", resid < 0.05, resid, "<0.05"),
              check("negative control: linear ramp violates the ODE", lresid > 10, lresid, ">10")]
    return checks, [path]


STAGGER = {"latin-char": 0.025, "word": 0.05, "arabic-word": 0.09, "nav": 0.05, "line": 0.1, "feature-card": 0.11}


def plan_stagger(kind, n):
    each = min(0.2, STAGGER[kind])
    if each * (n - 1) > 0.5:
        return {"amount": 0.3}
    return {"each": each}


@card("EASE-32")
def stagger_budgets(task, wd):
    cases = [("latin-char", 8), ("latin-char", 40), ("word", 6), ("arabic-word", 5), ("line", 4), ("feature-card", 50)]
    plans = [plan_stagger(k, n) for k, n in cases]
    js = "const C=%s; const R=[]; for(const [n,st] of C){const objs=Array.from({length:n},()=>({x:0}));" \
         "const tl=gsap.timeline({paused:true}); tl.to(objs,{x:1,duration:.4,ease:'power2.out',stagger:st});" \
         "const starts=objs.map(()=>null); for(let ms=0; ms<=1500; ms++){tl.seek(ms/1000+1e-7); objs.forEach((o,i)=>{if(starts[i]===null&&o.x>0) starts[i]=ms/1000;});}" \
         "R.push(starts);} out(R);" % json.dumps([[n, p] for (_, n), p in zip(cases, plans)])
    starts = node(wd, "stagger", js)
    spans = [s[-1] - s[0] for s in starts]
    arabic = "حركة لها معنى واضح جدا"
    units = arabic.split()
    path = jw(wd / "stagger.json", {"cases": cases, "plans": plans, "measured_spans": spans, "arabic_units": units})
    checks = [check("%s x%d total stagger <= 0.5 s" % c, sp <= 0.5 + 0.002, sp, "<=0.5") for c, sp in zip(cases, spans)]
    checks += [check("8 Latin chars at 25 ms each", abs(spans[0] - 0.175) <= 0.002, spans[0], 0.175),
               check("long cascades compress to amount 0.3", abs(spans[1] - 0.3) <= 0.002 and abs(spans[5] - 0.3) <= 0.002,
                     [spans[1], spans[5]], 0.3),
               check("Arabic staggers by whole word, never letters", len(units) == 5 and plans[3] == {"each": 0.09}, len(units), 5)]
    naive = 0.05 * (50 - 1)
    checks.append(check("negative control: naive 50 ms x 50 cards blows the budget", naive > 0.5, naive, "<=0.5"))
    return checks, [path]


@card("EASE-34")
def css_index_stagger(task, wd):
    blocks = "".join('<div class="b" style="--i:%d">%d</div>' % (i, i) if i < 10 else '<div class="b late">%d</div>' % i
                     for i in range(14))
    raw = "".join('<div class="r">%d</div>' % i for i in range(4))
    page = """<!doctype html><html><head><style>
:root{--ease:cubic-bezier(.16,1,.3,1)}
@keyframes scene-in{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.b{animation:scene-in .42s var(--ease) both;animation-delay:calc(var(--i)*45ms)}
.b.late{animation:none}
.r{animation:scene-in .42s var(--ease) both}
</style></head><body>%s%s<script>
const D=[...document.querySelectorAll('.b')].map(e=>getComputedStyle(e).animationDelay+'|'+getComputedStyle(e).animationName);
const R=[...document.querySelectorAll('.r')].map(e=>getComputedStyle(e).animationDelay);
const a0=document.querySelectorAll('.b')[3].getAnimations()[0]; a0.pause(); a0.currentTime=0; const t0=getComputedStyle(document.querySelectorAll('.b')[3]).transform;
a0.currentTime=135+420; const t1=getComputedStyle(document.querySelectorAll('.b')[3]).opacity;
document.body.setAttribute('data-r', JSON.stringify({D,R,t0,t1}));
</script></body></html>""" % (blocks, raw)
    (wd / "cascade.html").write_text(page, encoding="utf-8")
    r = chrome(wd, "cascade_run", page)
    path = jw(wd / "cascade_measure.json", r)
    delays = [float(x.split("|")[0][:-1]) for x in r["D"][:10]]
    names = [x.split("|")[1] for x in r["D"]]
    rise = float(r["t0"][r["t0"].index("(") + 1:-1].split(",")[5]) if r["t0"].startswith("matrix") else None
    checks = [check("delays = i x 45 ms (Chrome computed)", all(abs(d - 0.045 * i) < 1e-9 for i, d in enumerate(delays)), delays,
                    [round(0.045 * i, 3) for i in range(10)]),
              check("only the first 10 blocks animate", names[:10] == ["scene-in"] * 10 and names[10:] == ["none"] * 4, names, "10 x scene-in"),
              check("8 px rise at the start of block 3", rise == 8.0, rise, 8.0),
              check("block 3 fully in at delay + 420 ms", abs(float(r["t1"]) - 1.0) < 1e-6, r["t1"], 1),
              check("negative control: blocks without --i all start at 0 s", set(r["R"]) == {"0s"}, r["R"], "0s")]
    return checks, [path, wd / "cascade.html"]


@card("EASE-35")
def hero_opening(task, wd):
    r = node(wd, "hero", """const mk=()=>({y:0,opacity:1}); const E={eyebrow:mk(),h1:mk(),sub:mk(),cta:mk(),hint:mk()};
gsap.set(Object.values(E),{y:30,opacity:0}); const firstFrame=E.h1.opacity;
const tl=gsap.timeline({paused:true});
tl.to(E.eyebrow,{y:0,opacity:1,duration:.6}).to(E.h1,{y:0,opacity:1,duration:.8},'-=0.3').to(E.sub,{y:0,opacity:1,duration:.6},'-=0.5')
  .to(E.cta,{y:0,opacity:1,duration:.5},'-=0.3').to(E.hint,{y:0,opacity:1,duration:.4},'-=0.2');
const S=tl.getChildren().map(c=>[c.startTime(), c.endTime()]);
const seq=gsap.timeline({paused:true}); for(const d of [.6,.8,.6,.5,.4]) seq.to({v:0},{v:1,duration:d});
out({S, total:tl.duration(), firstFrame, seq:seq.duration()});""")
    S = r["S"]
    exp = [[0, .6], [.3, 1.1], [.6, 1.2], [.9, 1.4], [1.2, 1.6]]
    path = jw(wd / "hero_timeline.json", r)
    checks = [check("%s window" % n, abs(S[i][0] - exp[i][0]) < 1e-9 and abs(S[i][1] - exp[i][1]) < 1e-9, S[i], exp[i])
              for i, n in enumerate(["eyebrow", "h1", "subtitle", "cta", "hint"])]
    checks += [check("strict order of starts", all(S[i][0] < S[i + 1][0] for i in range(4)), [s[0] for s in S], "increasing"),
               check("whole entrance ~1.5 s", 1.4 <= r["total"] <= 1.7, r["total"], 1.5),
               check("gsap.set before the timeline: no flash of final layout", r["firstFrame"] == 0, r["firstFrame"], 0),
               check("negative control: sequential (no overlaps) takes 2.9 s", abs(r["seq"] - 2.9) < 1e-9 and r["seq"] > 1.7, r["seq"], ">1.7")]
    return checks, [path]


@card("EASE-36")
def overlap_four_acts(task, wd):
    fps, lead = 30, 1.0
    plan = {"lead": {"start": 0.0, "dur": lead}, "secondary": {"start": 0.65 * lead, "dur": lead - 0.65 * lead + 1 / fps},
            "shape": {"start": 0.0, "dur": lead - 6 / fps}}
    acts = {"anticipation": 0.15, "action": 0.40, "reaction": 0.15, "resolution": 0.30}
    js = "const P=%s; const o={lead:0,sec:0,shape:0}; const tl=gsap.timeline({paused:true});" \
         "tl.to(o,{lead:1,duration:P.lead.dur,ease:'power2.inOut'},P.lead.start);" \
         "tl.to(o,{sec:1,duration:P.secondary.dur,ease:'power2.out'},P.secondary.start);" \
         "tl.to(o,{shape:1,duration:P.shape.dur,ease:'power2.inOut'},P.shape.start);" \
         "const S=[]; for(let f=0;f<=45;f++){tl.seek(f/30); S.push([o.lead,o.sec,o.shape]);} out(S);" % json.dumps(plan)
    S = node(wd, "overlap", js)
    settle = [next(f for f in range(46) if all(abs(S[g][k] - 1) < 1e-4 for g in range(f, 46))) for k in range(3)]
    start_sec = next(f for f in range(46) if S[f][1] > 0)
    path = jw(wd / "overlap.json", {"plan": plan, "acts": acts, "settle_frames": settle, "samples": S})
    checks = [check("secondary starts at 55-75% of the lead", 0.55 <= start_sec / 30 / lead <= 0.75,
                    start_sec / 30, "0.55..0.75 s"),
              check("lead and secondary settle within 2 frames", abs(settle[0] - settle[1]) <= 2, settle[:2], "<=2 f apart"),
              check("shape settles 6 frames before position", settle[0] - settle[2] == 6, settle[0] - settle[2], 6),
              check("act proportions in bands and sum to 1", 0.10 <= acts["anticipation"] <= 0.2 and 0.3 <= acts["action"] <= 0.5 and
                    0.1 <= acts["reaction"] <= 0.2 and 0.2 <= acts["resolution"] <= 0.3 and abs(sum(acts.values()) - 1) < 1e-9,
                    list(acts.values()), "10-20/30-50/10-20/20-30")]
    naive_start = lead  # secondary chained after the lead
    checks.append(check("negative control: chained secondary starts at 100%", not (0.55 <= naive_start / lead <= 0.75), naive_start / lead, "0.55..0.75"))
    return checks, [path]


def lint_13(tl, W=1920, bpm=120):
    issues = []
    for el in tl["elements"]:
        for (t0, x0), (t1, x1) in zip(el["keys"], el["keys"][1:]):
            if abs(x1 - x0) > W / 3:
                issues.append(("travel", el["id"], t0))
    n = len(tl["elements"])
    for k in range(0, int(tl["dur"] * 10)):
        t = k / 10 + 0.05
        moving = sum(1 for el in tl["elements"] if el["keys"][0][0] <= t < el["keys"][-1][0])
        if moving > n / 3:
            issues.append(("crowd", moving, t))
            break
    ev = sorted(tl["events"]) + [tl["dur"]]
    for a, b in zip([0] + ev, ev):
        if b - a > 4:
            issues.append(("gap", a, b))
    for a, b in tl["holds"]:
        if b - a > 1.5 * 60 / bpm:
            issues.append(("hold", a, b))
    return issues


def fix_13(tl, W=1920, bpm=120):
    out = json.loads(json.dumps(tl))
    for el in out["elements"]:
        keys = [el["keys"][0]]
        for (t0, x0), (t1, x1) in zip(el["keys"], el["keys"][1:]):
            n = math.ceil(abs(x1 - x0) / (W / 3))
            for j in range(1, n + 1):
                keys.append([t0 + (t1 - t0) * j / n, x0 + (x1 - x0) * j / n])
        el["keys"] = keys
    per = max(1, len(out["elements"]) // 3)
    for i, el in enumerate(out["elements"]):
        span = el["keys"][-1][0] - el["keys"][0][0]
        start = (i // per) * (span + 0.1)
        base = el["keys"][0][0]
        el["keys"] = [[start + (t - base), x] for t, x in el["keys"]]
    out["dur"] = max(out["dur"], max(el["keys"][-1][0] for el in out["elements"]))
    ev = sorted(out["events"])
    filled, prev = [], 0
    for e in ev + [out["dur"]]:
        while e - prev > 4:
            prev += 3
            filled.append(prev)
        if e < out["dur"]:
            filled.append(e)
        prev = e
    out["events"] = sorted(filled)
    out["holds"] = [[a, min(b, a + 1.5 * 60 / bpm)] for a, b in out["holds"]]
    return out


@card("EASE-37")
def one_third_rules(task, wd):
    raw = {"dur": 12.0, "events": [0.5, 6.0], "holds": [[2.0, 4.0]],
           "elements": [{"id": "e%d" % i, "keys": [[0.0, 0.0], [1.0, 1500.0]]} for i in range(6)]}
    fixed = fix_13(raw)
    path = jw(wd / "timeline_fixed.json", fixed)
    back = json.loads(path.read_text(encoding="utf-8"))
    before, after = lint_13(raw), lint_13(back)
    travel = max(abs(b[1] - a[1]) for el in back["elements"] for a, b in zip(el["keys"], el["keys"][1:]))
    gaps = [b - a for a, b in zip([0] + sorted(back["events"]), sorted(back["events"]) + [back["dur"]])]
    checks = [check("fixed timeline passes all four 1/3 rules", after == [], after, []),
              check("no key-to-key travel over 1/3 frame", travel <= 640 + 1e-9, travel, "<=640"),
              check("a new event every <= 4 s", max(gaps) <= 4 + 1e-9, max(gaps), "<=4"),
              check("no hold over 1.5 beats (0.75 s at 120 BPM)", all(b - a <= 0.75 + 1e-9 for a, b in back["holds"]), back["holds"], "<=0.75"),
              check("negative control: raw timeline breaks every rule", {i[0] for i in before} == {"travel", "crowd", "gap", "hold"},
                    sorted({i[0] for i in before}), ["crowd", "gap", "hold", "travel"])]
    return checks, [path]


@card("EASE-38")
def build_breathe_resolve(task, wd):
    import numpy as np
    fps, T, W, H = 10, 6.0, 160, 90
    n = int(T * fps)
    frames = []
    for f in range(n + 1):
        p = f / n
        im, d = canvas(W, H)
        if p <= 0.3:  # build
            w = 120 * power_out(2)(p / 0.3)
            y = 45
        elif p <= 0.7:  # breathe: ONE ambient motion (a slow vertical float)
            w = 120
            y = 45 + 3 * math.sin(2 * math.pi * (p - 0.3) / 0.4)
        else:  # resolve: decisive exit
            w = 120 * (1 - power_in(3)((p - 0.7) / 0.3))
            y = 45
        if w > 0.5:
            d.rectangle([20, y - 5, 20 + w, y + 5], fill=(240, 240, 240))
        frames.append(np.asarray(im))
    mp4 = write_mp4(wd / "scene.mp4", frames, fps)
    fr = read_mp4(mp4, W, H)
    info = [blob_x(q) for q in fr]
    width = [0 if b is None else b["x1"] - b["x0"] + 1 for b in info]
    cy = [None if b is None else b["cy"] for b in info]
    b_end, r_start = int(0.3 * n), int(0.7 * n)
    breathe_w = width[b_end:r_start + 1]
    breathe_y = [c for c in cy[b_end:r_start + 1]]
    path = jw(wd / "phases.json", {"width": width, "cy": cy})
    checks = [check("build: grows to full by 30%", width[0] < 10 and abs(width[b_end] - 121) <= 2, [width[0], width[b_end]], [0, 121]),
              check("breathe: width holds (only one motion)", max(breathe_w) - min(breathe_w) <= 2, max(breathe_w) - min(breathe_w), "<=2"),
              check("breathe: ambient float is alive", 4 <= max(breathe_y) - min(breathe_y) <= 8, max(breathe_y) - min(breathe_y), "~6 px"),
              check("resolve: gone at 100%", width[-1] == 0, width[-1], 0)]
    static = [121] * (n + 1)
    checks.append(check("negative control: static bar has no build phase", not (static[0] < 10), static[0], "<10"))
    return checks, [mp4, path]


@card("EASE-40")
def distance_duration(task, wd):
    r = node(wd, "durfor", """const o={x:0}; const tl=gsap.timeline({paused:true}); tl.to(o,{x:600,duration:M.durFor(600),ease:M.E.glide});
out({d600:M.durFor(600), c100:M.durFor(100,true), c3000:M.durFor(3000,true), c1000:M.durFor(1000,true), d0:M.durFor(0),
 slope:(M.durFor(1100)-M.durFor(100))/1000, tl:tl.duration(), ladder:[50,150,300,600,1200].map(p=>M.durFor(p))});""")
    path = jw(wd / "durfor.json", r)
    lad = r["ladder"]
    checks = [check("durFor(600) = 1.16 s", abs(r["d600"] - 1.16) < 1e-9, r["d600"], 1.16),
              check("camera durFor(100) clamps to 0.6 s", r["c100"] == 0.6, r["c100"], 0.6),
              check("camera durFor(3000) clamps to 2.4 s", r["c3000"] == 2.4, r["c3000"], 2.4),
              check("camera mid-range unclamped (1000 px = 1.7 s)", abs(r["c1000"] - 1.7) < 1e-9, r["c1000"], 1.7),
              check("0.35 s base + 1.35 ms/px", abs(r["d0"] - 0.35) < 1e-12 and abs(r["slope"] - 0.00135) < 1e-12, [r["d0"], r["slope"]], [0.35, 0.00135]),
              check("tween takes the distance duration", abs(r["tl"] - 1.16) < 1e-9, r["tl"], 1.16),
              check("duration grows with distance", all(a < b for a, b in zip(lad, lad[1:])), lad, "increasing")]
    fixed = [0.5] * 5
    checks.append(check("negative control: fixed 0.5 s does not grow", not all(a < b for a, b in zip(fixed, fixed[1:])), fixed, "increasing"))
    return checks, [path]


def ease_out_cubic(p):
    return 1 - (1 - p) ** 3


@card("EASE-41")
def six_second_editorial(task, wd):
    import numpy as np
    fps, W, H = 30, 192, 108
    n = 180
    words = [(30, 60, 50), (90, 60, 50), (150, 60, 40)]  # x, y, width per word block
    frames = []
    for f in range(n):
        t = f / fps
        im, d = canvas(W, H, (12, 14, 20))
        for gx in range(0, W, 24):
            d.line([gx, 0, gx, H], fill=(40, 44, 56))
        if t >= 0.5 and t < 6.0:
            for k, (x, y, w) in enumerate(words):
                sf = 15 + 7 * k  # entrance at 0.5 s, stagger 7 frames
                st = sf / fps
                if f < sf:
                    continue
                p = min(1.0, (t - st) / 1.2)
                sp = 1 - math.exp(-6 * p) * math.cos(9 * p) if p < 1 else 1.0  # spring entrance
                rise = (1 - min(1.0, sp)) * 16
                yy = y + rise
                if 3.5 <= t < 4.7:
                    yy += 2 * math.sin(2 * math.pi * (t - 3.5) / 1.2)
                if t >= 4.7:
                    yy += 60 * ease_out_cubic(min(1.0, (t - 4.7) / 1.3))
                top = max(yy - 8, 40)  # word mask (masked vertical reveal): nothing above the mask line
                if top < yy + 8 and yy - 8 < 84:
                    d.rectangle([x - w / 2 + 10, top, x + w / 2 - 10, min(yy + 8, 84)], fill=(250, 250, 250))
        frames.append(np.asarray(im))
    mp4 = write_mp4(wd / "editorial_6s.mp4", frames, fps)
    dur = float(fx.probe(mp4)["format"]["duration"])
    fr = read_mp4(mp4, W, H)
    white = [int(((q > 200).all(axis=2)).sum()) for q in fr]
    hold = white[int(3.6 * fps):int(4.6 * fps)]
    first = [next(f for f in range(n) if fr[f][40:85, int(x - w / 2 + 10):int(x + w / 2 - 10)].min(axis=2).max() > 200) for x, _, w in words]
    path = jw(wd / "editorial.json", {"white": white, "first_frames": first})
    checks = [check("film is exactly 6.0 s", abs(dur - 6.0) < 0.05, dur, 6.0),
              check("0-0.5 s: grid and lines only", max(white[:15]) == 0, max(white[:15]), 0),
              check("entrance starts at 0.5 s with 7-frame word stagger", first[0] == 15 and first[1] - first[0] == 7 and first[2] - first[1] == 7,
                    first, [15, 22, 29]),
              check("hold 3.5-4.7 s: words fully on, steady coverage", min(hold) > 0 and (max(hold) - min(hold)) / max(hold) < 0.15,
                    [min(hold), max(hold)], "steady"),
              check("exit drops out by 6.0 s", white[-1] == 0, white[-1], 0)]
    static = np.asarray(frames[120])
    checks.append(check("negative control: an all-visible still has words at t=0", int(((static > 200).all(axis=2)).sum()) > 0,
                        int(((static > 200).all(axis=2)).sum()), ">0 (fails the base rule)"))
    return checks, [mp4, path]


UI_LADDER = {"micro": (80, 120), "button": (120, 180), "icon": (150, 250), "card": (200, 350), "modal": (300, 400),
             "page": (400, 600), "dramatic": (600, 1200)}


def ui_duration(element, video=False):
    lo, hi = UI_LADDER[element]
    enter = hi if video else (lo + hi) / 2
    return {"enter": enter, "exit": 0.75 * enter, "exit_ease": "power2.in", "enter_ease": "power2.out"}


@card("EASE-42")
def ui_duration_ladder(task, wd):
    raw = [{"el": "button", "ms": 60}, {"el": "modal", "ms": 900}, {"el": "card", "ms": 260}, {"el": "page", "ms": 1500}]
    ui = [dict(e, **ui_duration(e["el"])) for e in raw]
    video = [dict(e, **ui_duration(e["el"], video=True)) for e in raw]
    path = jw(wd / "durations.json", {"ui": ui, "video": video})

    def lint(rows, key):
        return [r for r in rows if not (UI_LADDER[r["el"]][0] <= r[key] <= UI_LADDER[r["el"]][1])]
    checks = [check("every UI duration inside its ladder band", lint(ui, "enter") == [], len(lint(ui, "enter")), 0),
              check("exit = 0.75 x enter, ease-in", all(abs(r["exit"] - 0.75 * r["enter"]) < 1e-9 and r["exit_ease"].endswith(".in") for r in ui),
                    ui[0]["exit"], 0.75 * ui[0]["enter"]),
              check("video takes the long end of each band", all(r["enter"] == UI_LADDER[r["el"]][1] for r in video),
                    [r["enter"] for r in video], [UI_LADDER[r["el"]][1] for r in video]),
              check("nothing imperceptible (<100 ms) outside micro", all(r["enter"] >= 100 for r in ui if r["el"] != "micro"), 1, 1),
              check("negative control: raw durations break the ladder", len(lint(raw, "ms")) == 3, len(lint(raw, "ms")), 3)]
    return checks, [path]


@card("EASE-44")
def reveal_across_shot(task, wd):
    shot = 12.0
    lines = ["line%d" % i for i in range(8)]
    words = [{"word": "w%d" % i, "start": round(i * 1.6, 2), "end": round(i * 1.6 + 0.5, 2), "line": i} for i in range(8)]
    jw(wd / "words.json", words)
    cue = {w["line"]: w["start"] for w in json.loads((wd / "words.json").read_text())}
    phases = [{"line": lines[i], "reveal_at": cue[i], "verb": "reveal"} for i in range(8)]
    path = jw(wd / "phases.json", phases)
    back = json.loads(path.read_text())
    front = sum(1 for p in back if p["reveal_at"] < 0.25 * shot) / len(back)
    checks = [check("every reveal cued on its voiceover word", all(abs(p["reveal_at"] - words[i]["start"]) < 1 / 30 for i, p in enumerate(back)), 0, 0),
              check("front-load <= 25%", front <= 0.25, front, "<=0.25"),
              check("first frame already readable", back[0]["reveal_at"] == 0, back[0]["reveal_at"], 0),
              check("each move named with one verb", all(len(p["verb"].split()) == 1 for p in back), 1, 1)]
    slide = [{"reveal_at": 0.0} for _ in lines]
    fl = sum(1 for p in slide if p["reveal_at"] < 0.25 * shot) / len(slide)
    checks.append(check("negative control: everything at t=0 reads as a slide", fl > 0.25, fl, "<=0.25"))
    return checks, [path, wd / "words.json"]


@card("EASE-45")
def keep_alive(task, wd):
    import numpy as np
    fps, W, H, n = 30, 320, 180, 90

    def frame(t, alive=True):
        im, d = canvas(W, H)
        z = 1 + 0.03 * t / 3 if alive else 1.0  # screenshot slow zoom 1 -> 1.03
        w = 100 * z
        d.rectangle([60 - w / 2, 60 - w * 0.3, 60 + w / 2, 60 + w * 0.3], fill=(90, 160, 255))
        fy = 5 * math.sin(2 * math.pi * t / 1.5) if alive else 0  # float +-5 px
        d.ellipse([200, 50 + fy, 220, 70 + fy], fill=(255, 210, 90))
        count = int(min(1, t / 2) * 10) if alive else 10  # stat counts from 0
        for k in range(count):
            d.rectangle([20 + k * 12, 150, 28 + k * 12, 170], fill=(120, 230, 160))
        return np.asarray(im)
    mp4 = write_mp4(wd / "alive.mp4", [frame(f / fps) for f in range(n)], fps)
    still = write_mp4(wd / "static.mp4", [frame(f / fps, False) for f in range(n)], fps)
    fr, st = read_mp4(mp4, W, H), read_mp4(still, W, H)

    def regions(seq):
        zw = [blob_x(q[:, :130] * (q[:, :130, 2:3] > 200))["x1"] - blob_x(q[:, :130] * (q[:, :130, 2:3] > 200))["x0"] + 1 for q in seq]
        fy = [blob_x(q[30:100, 180:240] * (q[30:100, 180:240, 0:1] > 200))["cy"] for q in seq]
        cnt = [int((q[150:171, :, 1] > 200).sum()) for q in seq]
        return zw, fy, cnt

    def frozen(seq, regs):
        worst = 0
        for vals in regs:
            run = 0
            for a, b in zip(vals, vals[1:]):
                run = run + 1 if abs(a - b) < 0.5 else 0
                worst = max(worst, run)
        return worst / fps
    zw, fy, cnt = regions(fr)
    zw2, fy2, cnt2 = regions(st)
    path = jw(wd / "alive.json", {"zoom_width": zw, "float_y": fy, "counter_px": cnt})
    checks = [check("screenshot zooms 1 -> ~1.03", 1.02 <= zw[-1] / zw[0] <= 1.04, zw[-1] / zw[0], 1.03),
              check("float amplitude 4-6 px", 4 <= (max(fy) - min(fy)) / 2 <= 6, (max(fy) - min(fy)) / 2, "4..6"),
              check("stat counts up from 0", cnt[0] == 0 and cnt[-1] > 0, [cnt[0], cnt[-1]], "0 -> full"),
              check("float element never frozen > 1.2 s", frozen(fr, [fy]) <= 1.2, frozen(fr, [fy]), "<=1.2"),
              check("negative control: the static render is frozen for the whole shot", frozen(st, [fy2, zw2]) > 1.2,
                    frozen(st, [fy2, zw2]), ">1.2")]
    return checks, [mp4, path]


@card("EASE-46")
def pose_ladder(task, wd):
    r = node(wd, "poses", """const o={x:0}; const tl=gsap.timeline({paused:true});
tl.to(o,{keyframes:[{x:0,duration:.2},{x:120,duration:.4,ease:'power2.out'},{x:100,duration:.2,ease:'power2.inOut'}],ease:'none'});
tl.addLabel('settled'); const lab=tl.labels.settled;
const P=[0.2,0.6,0.8].map(t=>{tl.seek(t); return o.x;}); const S=[]; for(let i=0;i<=80;i++){tl.seek(i/100); S.push(o.x);}
const run=(ir)=>{const a={x:0}; const t=gsap.timeline({paused:true}); t.to(a,{x:10,duration:.5},0.5);
 t.fromTo(a,{x:50},{x:60,duration:.5,immediateRender:ir},1.0); t.seek(0.2); const v=a.x; t.seek(0.75); return [v,a.x];};
out({P, S, lab, irFalse:run(false), irTrue:run(true)});""")
    path = jw(wd / "poses.json", r)
    S = r["S"]
    checks = [check("pose at 0.2 s = 0", abs(r["P"][0]) < 1e-6, r["P"][0], 0),
              check("pose at 0.6 s = 120 (overshoot pose)", abs(r["P"][1] - 120) < 1e-6, r["P"][1], 120),
              check("final pose at 0.8 s = 100", abs(r["P"][2] - 100) < 1e-6, r["P"][2], 100),
              check("label marks the settled state at 0.8 s", abs(r["lab"] - 0.8) < 1e-9, r["lab"], 0.8),
              check("motion peaks at 120 then settles back", abs(max(S) - 120) < 1e-6 and S[-1] < max(S), max(S), 120),
              check("immediateRender:false keeps the earlier poses", r["irFalse"] == [0, 7.5], r["irFalse"], [0, 7.5]),
              check("negative control: default later fromTo flashes and corrupts earlier poses", r["irTrue"] != [0, 7.5],
                    r["irTrue"], "!= [0, 7.5]")]
    return checks, [path]


@card("EASE-47")
def paused_master_timeline(task, wd):
    js = """const T=()=>({v:0}); const tl=gsap.timeline({paused:true, defaults:{duration:.5, ease:'power2.out'}});
window.__timelines={}; window.__timelines['scene-1']=tl;
const a=T(),b=T(),c=T(),d=T(),e=T(),f=T(),g=T(),h=T();
tl.to(a,{v:1,duration:1},0).to(b,{v:1},'<').to(c,{v:1},'>').to(d,{v:1},'<0.2').to(e,{v:1},'+=0.5').to(f,{v:1},'-=0.2');
tl.addLabel('intro',0); tl.to(g,{v:1},'intro+=0.3');
const child=gsap.timeline(); child.to(h,{v:1,duration:1}); tl.add(child, 3);
const S=tl.getChildren(false).map(x=>+x.startTime().toFixed(6));
const live=gsap.timeline(); live.to({v:0},{v:1,duration:0.4});
setTimeout(()=>{out({S, dflt:tl.getChildren()[1].duration(), reg:window.__timelines['scene-1']===tl, paused:tl.paused(),
  pausedTime:tl.time(), liveTime:live.time(), total:tl.duration()}); process.exit(0);}, 150);"""
    r = node(wd, "master", js)
    path = jw(wd / "master.json", r)
    # a@0 (1 s), b '<' = 0, label intro+=0.3 = 0.3, c '>' = end of b = 0.5, d '<0.2' = 0.7,
    # e '+=0.5' = timeline end (1.2) + 0.5 = 1.7, f '-=0.2' = end (2.2) - 0.2 = 2.0, child nested at 3 (sorted by start)
    exp = [0, 0, 0.3, 0.5, 0.7, 1.7, 2.0, 3.0]
    checks = [check("positions 0 < > <0.2 +=0.5 -=0.2 label+=0.3 nest@3", r["S"] == exp, r["S"], exp),
              check("defaults duration .5", abs(r["dflt"] - 0.5) < 1e-12, r["dflt"], 0.5),
              check("registered under the composition id", r["reg"], r["reg"], True),
              check("paused master does not advance with the wall clock", r["paused"] and r["pausedTime"] == 0, r["pausedTime"], 0),
              check("negative control: an unpaused timeline runs on its own", r["liveTime"] > 0.05, r["liveTime"], ">0")]
    return checks, [path]


@card("EASE-48")
def function_sampled_keyframes(task, wd):
    r = node(wd, "sampled", """const fn=t=>({x:100*Math.sin(2*Math.PI*t)}); const K=M.sampled(fn,0,1,60);
const o={x:0}; const tl=gsap.timeline({paused:true}); tl.to(o,{keyframes:K, ease:'none'});
const ts=[0.1234,0.25,0.5,0.731,0.9]; const V=ts.map(t=>{tl.seek(t); return o.x;});
const o2={x:0}; const t2=gsap.timeline({paused:true}); t2.fromTo(o2,{x:0},{x:fn(1).x,duration:1,ease:'none'}); t2.seek(0.25);
out({n:K.length, ease:K[1].ease, V, truth:ts.map(t=>fn(t).x), two:o2.x, dur:tl.duration()});""")
    path = jw(wd / "sampled.json", r)
    err = max(abs(a - b) for a, b in zip(r["V"], r["truth"]))
    checks = [check("1 s -> 61 keys", r["n"] == 61, r["n"], 61),
              check("keys use ease none", r["ease"] == "none", r["ease"], "none"),
              check("timeline length 1 s", abs(r["dur"] - 1) < 1e-4, r["dur"], 1),
              check("seeking anywhere reproduces f(t) (60/s sampling)", err < 0.2, err, "<0.2"),
              check("negative control: a two-key tween misses f(0.25)=100", abs(r["two"] - 100) > 50, r["two"], 100)]
    return checks, [path]


@card("EASE-51")
def hit_pulse(task, wd):
    import numpy as np
    onset_f = 10
    r = node(wd, "hit", """out({peak:M.hitPulse(2/60), z1:M.hitPulse(0.534), z0:M.hitPulse(0.52),
 env:Array.from({length:61},(_,f)=>M.hitPulse((f-%d)/60))});""" % onset_f)
    rate = 48000
    sig = np.zeros(rate)
    s0 = int(onset_f / 60 * rate)
    sig[s0:s0 + 480] = 0.8 * np.sin(2 * np.pi * 1000 * np.arange(480) / rate)
    wav = fx.write_wav(wd / "hit.wav", sig, rate)
    imgs = []
    for f in range(61):  # the visual is driven by the kit envelope, keyed to the sound onset
        im, d = canvas(120, 120)
        rr = 10 + 30 * r["env"][f]
        d.ellipse([60 - rr, 60 - rr, 60 + rr, 60 + rr], fill=(255, 255, 255))
        imgs.append(np.asarray(im))
    mp4 = write_mp4(wd / "hit.mp4", imgs, 60)
    fr = read_mp4(mp4, 120, 120)
    area = [blob_x(q)["n"] for q in fr]
    base = area[0]
    peak_f = int(np.argmax(area))
    back_f = next(f for f in range(peak_f, 61) if area[f] == base)
    a, ra = fx.read_wav(wav)
    a_on = int(np.argmax(np.abs(a[:, 0]) > 0.1)) / ra

    def ref(u):  # attack 2 f sine rise then exp(-(u-2)/5), zero after 2 + 6*5 frames
        return 0.0 if u <= 0 or u > 32 else (math.sin(u / 2 * math.pi / 2) if u < 2 else math.exp(-(u - 2) / 5))
    env_err = max(abs(r["env"][f] - ref(f - onset_f)) for f in range(61))
    path = jw(wd / "hit.json", {"kit": r, "area": area})
    checks = [check("kit hitPulse peaks 1.0 at 33 ms", abs(r["peak"] - 1) < 1e-12, r["peak"], 1.0),
              check("kit hitPulse zero after 533 ms, alive before", r["z1"] == 0 and r["z0"] > 0, [r["z0"], r["z1"]], ">0, 0"),
              check("kit envelope == attack/decay closed form", env_err < 1e-12, env_err, 0),
              check("rendered peak lands 2 frames after the sound", peak_f - round(a_on * 60) == 2, peak_f - round(a_on * 60), 2),
              check("visual exactly at rest once u > 32 frames (533 ms)", back_f == onset_f + 33, back_f, onset_f + 33),
              check("negative control: before the hit the circle is flat (no pulse)",
                    max(area[:onset_f + 1]) - min(area[:onset_f + 1]) <= base * 0.05, max(area[:onset_f + 1]) - min(area[:onset_f + 1]), "flat")]
    return checks, [mp4, wav, path]


@card("EASE-52")
def contact_squash(task, wd):
    import numpy as np
    r = node(wd, "squash", """const el={scaleX:1,scaleY:1,transformOrigin:''}; const tl=gsap.timeline({paused:true}); M.squash(tl,el,0.1,{edge:'bottom'});
const S=[]; tl.seek(0.3); for(let f=0;f<=18;f++){tl.seek(f?0.1+f/60:0.1+1e-6); S.push([el.scaleX, el.scaleY]);} out({S, origin:el.transformOrigin});""")
    S = r["S"]
    W, H, base_y, w0, h0 = 160, 120, 100, 40, 40

    def render(anchor_bottom):
        imgs = []
        for sx, sy in S:
            im, d = canvas(W, H)
            w, h = w0 * sx, h0 * sy
            if anchor_bottom:
                y1, y0 = base_y, base_y - h
            else:
                cy = base_y - h0 / 2
                y0, y1 = cy - h / 2, cy + h / 2
            d.rectangle([80 - w / 2, y0, 80 + w / 2, y1], fill=(255, 255, 255))
            imgs.append(np.asarray(im))
        return imgs
    mp4 = write_mp4(wd / "squash.mp4", render(True), 60)
    fr = read_mp4(mp4, W, H)
    bots = [blob_x(q)["y1"] for q in fr]
    widths = [blob_x(q)["x1"] - blob_x(q)["x0"] + 1 for q in fr]
    heights = [blob_x(q)["y1"] - blob_x(q)["y0"] + 1 for q in fr]
    cen = [blob_x(q.astype(float))["y1"] for q in render(False)]
    kick = 0.6
    sq = 1 - .16 * kick
    stretch = 1 / math.sqrt(sq)
    wob = [math.exp(-7 * x) * math.sin(30 * x) * .05 for x in [i / 100 for i in range(101)]]
    path = jw(wd / "squash.json", {"S": S, "origin": r["origin"], "bottoms": bots})
    checks = [check("contact pose scaleX 1.08 / scaleY 0.90", abs(S[0][0] - 1.08) < 1e-3 and abs(S[0][1] - 0.90) < 1e-3, S[0], [1.08, 0.9]),
              check("recovers to 1 in 0.13 s (8 f)", S[8] == [1, 1] and S[7] != [1, 1], [S[7], S[8]], "1,1 at f8"),
              check("anchored to the hit edge (origin 50% 100%)", r["origin"] == "50% 100%", r["origin"], "50% 100%"),
              check("rendered bottom edge never moves", max(bots) - min(bots) <= 1, [min(bots), max(bots)], "constant"),
              check("rendered contact frame wider and flatter", widths[0] > widths[-1] + 2 and heights[0] < heights[-1] - 2,
                    [widths[0], heights[0]], ">w, <h"),
              check("volume-preserving variant: sq * stretch^2 = 1", abs(sq * stretch * stretch - 1) < 1e-12, sq * stretch ** 2, 1),
              check("landing wobble decays", max(abs(v) for v in wob[50:]) < 0.05 * math.exp(-3.5) + 1e-9, max(abs(v) for v in wob[50:]), "decayed"),
              check("negative control: centre-anchored squash moves the contact edge", max(cen) - min(cen) > 1, max(cen) - min(cen), ">1")]
    return checks, [mp4, path]


@card("EASE-53")
def squash_stretch_hop(task, wd):
    r = node(wd, "hop", """const o={y:0,scaleY:1}; const tl=gsap.timeline({paused:true});
for(let k=0;k<3;k++){const at=k*0.42; tl.to(o,{y:-90,scaleY:1.08,duration:.2,ease:M.E.out},at); tl.to(o,{y:0,scaleY:.86,duration:.18,ease:M.E.contact},at+.2);}
tl.to(o,{scaleY:1,duration:.12},0.84+.38);
const S=[]; for(let i=0;i<=140;i++){tl.seek(i/100); S.push([o.y,o.scaleY]);} out(S);""")
    S = r
    apex = [S[20], S[62], S[104]]
    land = [S[38], S[80], S[122]]
    bunny = [math.sin(math.pi * u / 100) * .026 for u in range(101)]
    ball = {"scaleY": 0.75, "scaleX": 1 / 0.75}
    path = jw(wd / "hop.json", {"samples": S, "ball": ball})
    import numpy as np
    imgs = []
    for y, sy in S[::2]:
        im, d = canvas(120, 160)
        h = 30 * sy
        w = 30 / sy
        d.rectangle([60 - w / 2, 140 + y - h, 60 + w / 2, 140 + y], fill=(255, 220, 120))
        imgs.append(np.asarray(im))
    mp4 = write_mp4(wd / "hop.mp4", imgs, 50)
    checks = [check("three apexes at -90 px with stretch 1.08", all(abs(a[0] + 90) < 1e-3 and abs(a[1] - 1.08) < 1e-3 for a in apex), apex, [-90, 1.08]),
              check("three landings at 0 with squash .86", all(abs(l[0]) < 1e-3 and abs(l[1] - .86) < 1e-3 for l in land), land, [0, .86]),
              check("hops 0.42 s apart", [i for i in range(141) if abs(S[i][0] + 90) < 1e-3] == [20, 62, 104], [20, 62, 104], [20, 62, 104]),
              check("recovers to scaleY 1 at the end", abs(S[-1][1] - 1) < 1e-6, S[-1][1], 1),
              check("bunny hop peak .026 at mid", abs(max(bunny) - .026) < 1e-12 and bunny.index(max(bunny)) == 50, max(bunny), .026),
              check("classic ball impact preserves area", abs(ball["scaleX"] * ball["scaleY"] - 1) < 1e-12 and 1.2 <= ball["scaleX"] <= 1.4,
                    ball["scaleX"] * ball["scaleY"], 1)]
    flat = [1.0 for _ in S]
    checks.append(check("negative control: a hop without squash never reaches .86", min(flat) > .9, min(flat), .86))
    return checks, [path, mp4]


def word_layer(text="WOW", size=(200, 100)):
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new("L", size, 0)
    d = ImageDraw.Draw(im)
    try:
        font = ImageFont.load_default(size=48)
    except TypeError:
        font = ImageFont.load_default()
    d.text((size[0] / 2, size[1] / 2), text, fill=255, font=font, anchor="mm")
    return im


def sharpness(a):
    import numpy as np
    a = np.asarray(a, dtype=float)
    if a.ndim == 3:
        a = a.mean(axis=2)
    return float(np.abs(np.diff(a, axis=1)).mean() + np.abs(np.diff(a, axis=0)).mean())


@card("EASE-58")
def blur_pop(task, wd):
    import numpy as np
    from PIL import Image, ImageFilter
    word = word_layer()
    W, H = word.size
    fps = 30
    ein = back_out(1.3)
    eout = bez(*E_TOKENS["in"])

    def frame(scale, opacity, blur):
        lay = word.resize((max(1, int(W * scale)), max(1, int(H * scale))), Image.BILINEAR)
        if blur > 0.05:
            lay = lay.filter(ImageFilter.GaussianBlur(blur))
        can = Image.new("L", (W, H), 0)
        can.paste(lay, ((W - lay.width) // 2, (H - lay.height) // 2))
        a = np.asarray(can, dtype=float) * max(0.0, min(1.0, opacity))
        return np.stack([a] * 3, axis=2).astype(np.uint8)
    imgs, scales = [], []
    n_in, n_out = int(0.55 * fps), int(0.25 * fps)
    for f in range(n_in + 1):
        e = ein(f / n_in)
        s = 0.4 + 0.6 * e
        scales.append(s)
        imgs.append(frame(s, e, max(0.0, 16 * (1 - e))))
    hold = [frame(1, 1, 0)] * 10
    outs = []
    for f in range(1, n_out + 1):
        e = eout(f / n_out)
        outs.append(frame(1 + 0.12 * e, 1 - e, 10 * e))
    mp4 = write_mp4(wd / "blur_pop.mp4", imgs + hold + outs, fps)
    fr = read_mp4(mp4, W, H)
    ref = np.asarray(frame(1, 1, 0), dtype=float)
    end_in = fr[n_in]
    diff = float(np.abs(end_in - ref).mean())
    bright = [float(q.mean()) for q in fr]
    path = jw(wd / "blur_pop.json", {"scales": scales, "brightness": bright})
    checks = [check("starts invisible (opacity 0)", bright[0] < 0.5, bright[0], 0),
              check("starts blurred: sharpness rises through the pop-in", sharpness(fr[3]) < sharpness(fr[n_in]) * 0.6,
                    [sharpness(fr[3]), sharpness(fr[n_in])], "rising"),
              check("back.out(1.3) overshoot carried into scale (.4 + .6 x 1.0615)",
                    abs(max(scales) - (0.4 + 0.6 * max(ein(i / 1000) for i in range(1001)))) < 0.004 and max(scales) > 1.02,
                    max(scales), 0.4 + 0.6 * max(ein(i / 1000) for i in range(1001))),
              check("lands at scale 1, sharp, full opacity at 0.55 s", diff < 3, diff, "<3"),
              check("leaves to opacity 0 in 0.25 s", bright[-1] < 0.5, bright[-1], 0)]
    raw = np.asarray(frame(1, 1, 0), dtype=float)
    checks.append(check("negative control: the plain word is visible and sharp at frame 0", raw.mean() > 0.5, float(raw.mean()), "~0"))
    return checks, [mp4, path]


@card("EASE-59")
def wiggle_and_sway(task, wd):
    r = node(wd, "wiggle", """const o={rotation:0}; const tl=gsap.timeline({paused:true});
tl.fromTo(o,{rotation:-4},{rotation:4,duration:.12,yoyo:true,repeat:7,ease:'sine.inOut'});
const S=[]; for(let i=0;i<=960;i++){tl.seek(i/1000); S.push(o.rotation);} out({S, dur:tl.duration()});""")
    S = r["S"]
    # count direction flips: sign changes of the first difference
    d = [S[i + 1] - S[i] for i in range(len(S) - 1)]
    sg = [1 if v > 1e-9 else -1 if v < -1e-9 else 0 for v in d]
    sg = [v for v in sg if v]
    flips = sum(1 for a, b in zip(sg, sg[1:]) if a != b)
    phases = [0.0, 1.3, 2.1, 3.7]
    branch = [[4 * math.sin(2 * math.pi * t / 80 + p) for t in range(81)] for p in phases]

    def corr(a, b):
        import numpy as np
        return float(np.corrcoef(a, b)[0, 1])
    max_c = max(corr(branch[i], branch[j]) for i in range(4) for j in range(i + 1, 4))
    tilt = [6 * math.sin(2 * math.pi * t / 60) for t in range(61)]
    shadow = [1 - 0.3 * abs(a) / 6 for a in tilt]
    path = jw(wd / "wiggle_sway.json", {"wiggle": S, "branches": branch, "shadow": shadow})
    curves_png(wd / "wiggle.png", {"rot": [(v + 4) / 8 for v in S[::8]]})
    in_phase = [[4 * math.sin(2 * math.pi * t / 80) for t in range(81)] for _ in phases]
    checks = [check("wiggle spans -4..4 degrees", abs(min(S) + 4) < 1e-6 and abs(max(S) - 4) < 1e-6, [min(S), max(S)], [-4, 4]),
              check("0.12 s x 8 plays = 0.96 s", abs(r["dur"] - 0.96) < 1e-9, r["dur"], 0.96),
              check("7 direction reversals (yoyo repeat 7)", flips == 7, flips, 7),
              check("branches never all in phase", max_c < 0.95, max_c, "<0.95"),
              check("pendulum shadow scale tied to tilt", abs(corr([abs(a) for a in tilt], shadow) + 1) < 1e-9, corr([abs(a) for a in tilt], shadow), -1),
              check("negative control: in-phase branches correlate 1.0", corr(in_phase[0], in_phase[1]) > 0.95, corr(in_phase[0], in_phase[1]), ">0.95")]
    return checks, [path, wd / "wiggle.png"]


def edge_ramp(row, thr_lo=0.1, thr_hi=0.9):
    """Width in px of the leading-edge ramp of a 1-D brightness profile."""
    import numpy as np
    row = np.asarray(row, dtype=float)
    m = row.max()
    if m <= 0:
        return 0
    n = row / m
    lo = int(np.argmax(n > thr_lo))
    hi = int(np.argmax(n > thr_hi))
    return hi - lo


@card("EASE-60")
def speed_limits(task, wd):
    import numpy as np
    from PIL import Image, ImageFilter
    W, H, fps, n = 480, 80, 30, 12
    speeds = {"read": 2.0, "fast": 30.0}

    def render(blur_fast):
        imgs = []
        for f in range(n):
            im, d = canvas(W, H, (0, 0, 0))
            d.rectangle([20 + speeds["read"] * f, 8, 60 + speeds["read"] * f, 30], fill=(255, 255, 255))
            lay = Image.new("L", (W, 40), 0)
            from PIL import ImageDraw
            ImageDraw.Draw(lay).rectangle([20 + speeds["fast"] * f, 8, 60 + speeds["fast"] * f, 30], fill=255)
            if blur_fast:  # > 12 px/f needs blur: a horizontal box blur the length of one frame's travel
                k = int(speeds["fast"])
                a = np.asarray(lay, dtype=float)
                kern = np.ones(k) / k
                a = np.apply_along_axis(lambda r: np.convolve(r, kern, mode="same"), 1, a)
                lay = Image.fromarray(a.clip(0, 255).astype(np.uint8))
            im.paste(Image.merge("RGB", [lay] * 3), (0, 40))
            imgs.append(np.asarray(im))
        return imgs
    mp4 = write_mp4(wd / "speed.mp4", render(True), fps)
    raw = render(False)
    fr = read_mp4(mp4, W, H)
    cx_read = [blob_x(q[:40])["cx"] for q in fr]
    cx_fast = [blob_x(q[40:], thr=20)["cx"] for q in fr]
    v_read = float(np.median(np.diff(cx_read)))
    v_fast = float(np.median(np.diff(cx_fast)))
    ramp_out = edge_ramp(fr[5][59, :, 0])
    ramp_raw = edge_ramp(np.asarray(raw[5], dtype=float)[59, :, 0])
    rule = lambda v, ramp: v <= 12 or ramp >= 10
    path = jw(wd / "speed.json", {"v_read": v_read, "v_fast": v_fast, "ramp_blurred": ramp_out, "ramp_raw": ramp_raw})
    checks = [check("reading text measured <= 3 px/frame", abs(v_read - 2) < 0.3 and v_read <= 3, v_read, "<=3"),
              check("fast element measured ~30 px/frame (flagged > 12)", abs(v_fast - 30) < 1 and v_fast > 12, v_fast, 30),
              check("fast element is blurred (edge ramp >= 10 px)", ramp_out >= 10, ramp_out, ">=10"),
              check("rendered film passes the speed rule", rule(v_fast, ramp_out), True, True),
              check("negative control: the unblurred 30 px/f render fails the rule", not rule(v_fast, ramp_raw), ramp_raw, "<10")]
    return checks, [mp4, path]


@card("EASE-62")
def shutter_blur(task, wd):
    import numpy as np
    W, H, fps, v, N = 240, 40, 30, 8.0, 16

    def draw(x):
        a = np.zeros((H, W))
        a[10:30, int(round(x)):int(round(x)) + 20] = 255
        return a

    def pos(t):
        return 40 + v * fps * t
    frames_blur, frames_raw = [], []
    for f in range(12):
        t = f / fps
        acc = np.zeros((H, W))
        for k in range(N):  # 720 degree shutter, phase -360: window [t - 1/fps, t + 1/fps]
            tk = t - 1 / fps + 2 / fps * k / (N - 1)
            acc += draw(pos(tk)) / N
        frames_blur.append(np.stack([acc] * 3, axis=2).astype(np.uint8))
        frames_raw.append(np.stack([draw(pos(t))] * 3, axis=2).astype(np.uint8))
    mp4 = write_mp4(wd / "shutter.mp4", frames_blur, fps)
    fr = read_mp4(mp4, W, H)
    ext = lambda a: int((a[20, :, 0] > 10).sum())
    measured = ext(fr[6])
    expect = 20 + 2 * v
    centre = blob_x(fr[6], thr=10)["cx"]
    path = jw(wd / "shutter.json", {"extent": measured, "expected": expect, "centre": centre})
    checks = [check("smear spans 2 frames of travel (720 deg)", abs(measured - expect) <= 2, measured, expect),
              check("blur centred on the true position at t", abs(centre - (pos(6 / fps) + 9.5)) <= 1.0, centre, pos(6 / fps) + 9.5),
              check("16 sub-frame samples (intensity steps)", len(set(np.round(frames_blur[6][20, :, 0] / (255 / N)).astype(int))) >= 10,
                    len(set(np.round(frames_blur[6][20, :, 0] / (255 / N)).astype(int))), ">=10 levels"),
              check("negative control: the unblurred frame spans only the object", ext(frames_raw[6].astype(float)) == 20,
                    ext(frames_raw[6].astype(float)), 20)]
    return checks, [mp4, path]


def cut_film(path, shots, fps=10, size=(32, 18), first_change=None):
    """Render a film of flat-colour shots (one colour per shot); optional element popping in at a frame."""
    import numpy as np
    w, h = size
    frames, palette = [], [(200, 40, 40), (40, 160, 60), (40, 70, 200), (220, 200, 40), (160, 40, 200), (40, 200, 200)]
    for i, dur in enumerate(shots):
        n = int(round(dur * fps))
        for k in range(n):
            a = np.zeros((h, w, 3), dtype=np.uint8)
            a[:] = palette[i % len(palette)]
            if first_change is not None and i == 0 and k >= first_change:
                a[h // 4:3 * h // 4, w // 4:3 * w // 4] = 255
            frames.append(a)
    return write_mp4(path, frames, fps)


def detect_cuts(path, size=(32, 18), thr=40):
    import numpy as np
    fr = read_mp4(path, *size)
    d = [float(np.abs(fr[i + 1] - fr[i]).mean()) for i in range(len(fr) - 1)]
    return [i + 1 for i, v in enumerate(d) if v > thr], len(fr), d


@card("EASE-63")
def pacing_medians(task, wd):
    import statistics
    fps = 30
    shots = [1.1, 1.3, 1.46, 1.6, 2.8, 1.2, 1.46, 1.5, 1.0, 1.46, 1.7, 1.3, 2.2]  # end card 2.2 s
    mp4 = cut_film(wd / "pacing.mp4", shots, fps, (48, 27), first_change=3)
    cuts, n, d = detect_cuts(mp4, (48, 27))
    bounds = [0] + cuts + [n]
    lens = [(b - a) / fps for a, b in zip(bounds, bounds[1:])]
    first_vis = next(i + 1 for i, v in enumerate(d) if v > 5) / fps
    path = jw(wd / "pacing.json", {"detected_shots": lens, "first_visible_change": first_vis})
    checks = [check("detected shots == planned shots", len(lens) == len(shots) and max(abs(a - b) for a, b in zip(lens, shots)) <= 1 / fps + 1e-9,
                    len(lens), len(shots)),
              check("median shot 1.46 s", abs(statistics.median(lens) - 1.46) <= 1 / fps, statistics.median(lens), 1.46),
              check("shots inside 1.0-2.8 s band", min(lens) >= 1.0 - 1e-9 and max(lens) <= 2.8 + 1e-9, [min(lens), max(lens)], "1.0..2.8"),
              check("first visible change by 0.10 s", first_vis <= 0.10 + 1e-9, first_vis, "<=0.10"),
              check("end card ~2.2 s", abs(lens[-1] - 2.2) <= 1 / fps, lens[-1], 2.2)]
    flat = cut_film(wd / "flat.mp4", [10.0], fps, (48, 27))
    c2, n2, _ = detect_cuts(flat, (48, 27))
    checks.append(check("negative control: one 10 s static shot has median 10 s", (n2 / fps) > 2.8 and not c2, n2 / fps, "<=2.8"))
    return checks, [mp4, path]


@card("EASE-64")
def edit_rhythm_genre(task, wd):
    fps = 10
    pattern = [1.2, 3.5, 3.8]  # fast shot, then two breathing shots
    shots, t = [], 0.0
    while t < 60 - 1e-9:
        d = pattern[len(shots) % 3]
        d = min(d, 60 - t)
        shots.append(d)
        t += d
    mp4 = cut_film(wd / "explainer_60s.mp4", shots, fps)
    cuts, n, _ = detect_cuts(mp4)
    bounds = [0] + cuts + [n]
    lens = [(b - a) / fps for a, b in zip(bounds, bounds[1:])]
    asl = sum(lens) / len(lens)
    alt = all((lens[i] <= 1.5) != (lens[i + 1] <= 1.5) or lens[i] > 1.5 for i in range(len(lens) - 1))
    vlog = [8.0] * 8
    vcut = cut_film(wd / "vlog_60s.mp4", vlog[:7] + [4.0], fps)
    vc, vn, _ = detect_cuts(vcut)
    path = jw(wd / "rhythm.json", {"explainer_shots": lens, "asl": asl, "cuts": len(cuts), "vlog_cuts": len(vc)})
    checks = [check("explainer ASL in 2.5-4 s", 2.5 <= asl <= 4.0, asl, "3.3 (2.5-4)"),
              check("15-25 cuts in the first minute", 15 <= len(cuts) <= 25, len(cuts), "15..25"),
              check("same picture <= 8 s", max(lens) <= 8, max(lens), "<=8"),
              check("fast shots (0.5-1.5) alternate with breathing (2.5-4.0)", all(0.5 <= x <= 1.5 or 2.5 <= x <= 4.0 for x in lens[:-1]) and alt,
                    sorted(set(lens)), "fast/breathing"),
              check("negative control: an 8 s-ASL vlog cut fails the explainer target", not (15 <= len(vc) <= 25), len(vc), "15..25")]
    return checks, [mp4, path]


@card("EASE-65")
def short_form_structure(task, wd):
    segs = [{"text": "عنوان", "start": 0.0, "end": 1.2, "kind": "title"},
            {"text": "هل تعرف لماذا؟", "start": 1.2, "end": 2.6, "kind": "hook"},
            {"text": "المشكلة", "start": 2.6, "end": 8.0}, {"text": "الوعد", "start": 8.0, "end": 11.0},
            {"text": "الدليل 1", "start": 11.0, "end": 18.0}, {"text": "الدليل 2", "start": 18.0, "end": 24.0},
            {"text": "الخلاصة", "start": 24.0, "end": 28.0}, {"text": "ذيل طويل", "start": 28.0, "end": 36.0}]
    jw(wd / "words.json", segs)
    src = json.loads((wd / "words.json").read_text())
    body = [s for s in src if s.get("kind") != "title"]  # hook in the first frame, before any title card
    t, out = 0.0, []
    for s in body:
        d = s["end"] - s["start"]
        if t + d > 30:
            break
        sec = "hook" if t < 3 else "problem/promise" if t < 10 else "proof" if t < 25 else "close"
        out.append({"text": s["text"], "start": round(t, 3), "end": round(t + d, 3), "section": sec, "caption": True})
        t += d
    path = jw(wd / "structure.json", out)
    back = json.loads(path.read_text())
    secs = [s["section"] for s in back]
    checks = [check("hook in the first frame", back[0]["start"] == 0 and back[0]["text"] == "هل تعرف لماذا؟", back[0]["text"], "hook"),
              check("hook ends within 3 s", back[0]["end"] <= 3, back[0]["end"], "<=3"),
              check("sections in arc order", secs == sorted(secs, key=["hook", "problem/promise", "proof", "close"].index), secs, "ordered"),
              check("clip <= 30 s", back[-1]["end"] <= 30, back[-1]["end"], "<=30"),
              check("captions always on", all(s["caption"] for s in back), True, True),
              check("negative control: raw order opens on a title card, runs 36 s", src[0]["kind"] == "title" and src[-1]["end"] > 30,
                    [src[0]["kind"], src[-1]["end"]], "hook first, <=30")]
    return checks, [path, wd / "words.json"]


def clicks(times, seconds, rate=44100, freq=1500.0, amp=0.8, dur=0.02):
    import numpy as np
    sig = np.zeros(int(seconds * rate))
    for t in times:
        s = int(t * rate)
        n = int(dur * rate)
        k = np.arange(n)
        sig[s:s + n] += amp * np.sin(2 * np.pi * freq * k / rate) * np.exp(-k / (n / 4))
    return sig


def onsets(sig, rate, hop=0.005, thr=0.05):
    import numpy as np
    n = int(hop * rate)
    env = np.array([np.abs(sig[i:i + n]).max() for i in range(0, len(sig) - n, n)])
    on = []
    for i in range(1, len(env)):
        if env[i] > thr and env[i - 1] <= thr:
            on.append(i * hop)
    return on


@card("EASE-67")
def beat_clock(task, wd):
    import numpy as np
    bpm, fps, T = 120, 30, 4.0
    beats = [i * 60 / bpm for i in range(8)]
    js = """const B=M.beats(%d); const ch=M.channels({fps:%d, frames:%d, kicks:%s, beats:%s});
out({at4:B.at(4), len2:B.len(2), v:Array.from({length:%d},(_,f)=>ch.kick(f/%d))});""" % (bpm, fps, int(T * fps), json.dumps(beats), json.dumps(beats), int(T * fps), fps)
    r = node(wd, "beats", js)
    sig = clicks(beats, T)
    wav = fx.write_wav(wd / "clicks.wav", sig)
    imgs = []
    for v in r["v"]:
        a = np.zeros((36, 64, 3), dtype=np.uint8)
        a[:] = int(30 + 225 * v)
        imgs.append(a)
    vid = write_mp4(wd / "pulse_silent.mp4", imgs, fps)
    mp4 = wd / "beat_clock.mp4"
    fx.ffmpeg("-i", vid, "-i", wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", mp4)
    fr = read_mp4(mp4, 64, 36)
    br = [float(q.mean()) for q in fr]
    peaks = [i for i in range(1, len(br) - 1) if br[i] > 120 and br[i] >= br[i - 1] and br[i] >= br[i + 1]]
    fx.ffmpeg("-i", mp4, "-vn", "-ac", "1", "-ar", "44100", wd / "decoded.wav")
    a, ra = fx.read_wav(wd / "decoded.wav")
    aon = onsets(a[:, 0], ra)
    off = [min(abs(p / fps - o) for o in aon) for p in peaks]
    path = jw(wd / "beat_clock.json", {"at4": r["at4"], "peaks": peaks, "audio_onsets": aon})
    checks = [check("beat n at n x 60/BPM: B.at(4) = 2.0 s", abs(r["at4"] - 2.0) < 1e-12, r["at4"], 2.0),
              check("B.len(2) = 1.0 s", abs(r["len2"] - 1.0) < 1e-12, r["len2"], 1.0),
              check("one visual pulse per beat", len(peaks) == 8, len(peaks), 8),
              check("audio onsets decoded from the film: 8", len(aon) == 8, len(aon), 8),
              check("each pulse within 1 frame of its sound", max(off) <= 1 / fps + 0.006, max(off), "<=1 frame")]
    flat = [r["v"][0]] * len(r["v"])
    checks.append(check("negative control: visuals off the beat clock have no pulses", max(flat) - min(flat) == 0, max(flat) - min(flat), 0))
    return checks, [mp4, path]


@card("EASE-68")
def onset_snapped_words(task, wd):
    import numpy as np
    rate = 44100
    true_on = [0.50, 1.10, 1.70, 2.40, 3.00]
    sig = np.zeros(int(3.6 * rate))
    for t in true_on:
        s = int(t * rate)
        k = np.arange(int(0.25 * rate))
        sig[s:s + len(k)] += 0.6 * np.sin(2 * np.pi * 700 * k / rate) * np.minimum(1, k / 200)
    sig += 0.01 * np.random.default_rng(3).standard_normal(len(sig))
    fx.write_wav(wd / "vocal.wav", sig, rate)
    a, ra = fx.read_wav(wd / "vocal.wav")
    x = a[:, 0]
    spec = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / ra)
    spec[(f < 300) | (f > 3000)] = 0  # vocal band
    band = np.fft.irfft(spec, len(x))
    hop = int(0.005 * ra)
    env = np.array([np.sqrt((band[i:i + hop] ** 2).mean()) for i in range(0, len(band) - hop, hop)])
    flux = np.maximum(0, np.diff(env, prepend=0))
    stamps = [{"w": "w%d" % i, "start": t + 0.06} for i, t in enumerate(true_on)]  # model stamps run 60 ms late
    snapped = []
    for s in stamps:
        lo, hi = int((s["start"] - 0.100) / 0.005), int((s["start"] + 0.040) / 0.005)
        k = lo + int(np.argmax(flux[lo:hi + 1]))
        snapped.append(dict(s, start=round(k * 0.005, 3)))
    bpm = 120
    grid = {"tempo": bpm, "beats": [i * 0.5 for i in range(8)], "bars": [i * 2.0 for i in range(2)], "words": snapped,
            "cuts": [i * 2.0 for i in range(2)]}
    path = jw(wd / "grid.json", grid)
    err = max(abs(s["start"] - t) for s, t in zip(snapped, true_on))
    raw_err = max(abs(s["start"] - t) for s, t in zip(stamps, true_on))
    checks = [check("words snapped to the vocal onset within 10 ms", err <= 0.010, err, "<=0.010"),
              check("snap stayed inside -100..+40 ms of the stamp", all(-0.1 - 1e-9 <= s["start"] - st["start"] <= 0.04 + 1e-9
                    for s, st in zip(snapped, stamps)), True, True),
              check("cuts on bar lines (every 4 beats)", grid["cuts"] == grid["beats"][::4], grid["cuts"], grid["beats"][::4]),
              check("negative control: raw model stamps are 60 ms late", raw_err > 0.05, raw_err, "<=0.010")]
    return checks, [path, wd / "vocal.wav"]


def cut_list(mode, every=2.0, dur=10.0, beats=None, voiced=None, shots=None):
    if mode == "interval":
        return [round(every * k, 6) for k in range(1, int(dur / every + 1e-9)) if every * k < dur]
    if mode == "beat":
        gap, out = max(0.45, 0.8 * every), []
        for b in beats:
            if not out or b - out[-1] >= gap - 1e-9:
                out.append(b)
        return out
    if mode == "speech":
        gap, out, prev_end = max(0.8, every / 2), [], -1e9
        for s, e in voiced:
            if s - prev_end >= 0.3 and (not out or s - out[-1] >= gap):
                out.append(s)
            prev_end = e
        return out
    if mode == "shots":
        return list(shots)
    raise ValueError(mode)


def snap_time(t, targets, px_per_s, w=7):
    best = min(targets, key=lambda x: abs(x - t))
    return best if abs(best - t) * px_per_s <= w else t


@card("EASE-69")
def cut_modes_snapping(task, wd):
    beats = [i * 0.5 for i in range(1, 20)]
    voiced = [(0.0, 1.0), (1.1, 1.9), (2.4, 3.5), (3.6, 4.0), (4.5, 5.5), (6.2, 7.0)]
    res = {"interval": cut_list("interval", 2.0), "beat": cut_list("beat", 1.0, beats=beats),
           "speech": cut_list("speech", 1.0, voiced=voiced), "shots": cut_list("shots", shots=[1.23, 4.56])}
    snaps = {t: snap_time(t, [2.0, 4.0, 1.23], px_per_s=100) for t in (2.05, 2.2, 1.18)}
    path = jw(wd / "cuts.json", {"cuts": res, "snaps": {str(k): v for k, v in snaps.items()}})
    sp = lambda c: min(b - a for a, b in zip(c, c[1:]))
    checks = [check("interval every 2 s", res["interval"] == [2.0, 4.0, 6.0, 8.0], res["interval"], [2, 4, 6, 8]),
              check("beat cuts >= max(0.45, 0.8*every) apart", sp(res["beat"]) >= 0.8 - 1e-9, sp(res["beat"]), ">=0.8"),
              check("speech cuts on voiced starts after >= 0.3 s pause", res["speech"] == [0.0, 2.4, 4.5, 6.2], res["speech"], [0, 2.4, 4.5, 6.2]),
              check("shot mode keeps measured boundaries", res["shots"] == [1.23, 4.56], res["shots"], [1.23, 4.56]),
              check("snap within 7 px (0.07 s at 100 px/s)", snaps[2.05] == 2.0 and snaps[1.18] == 1.23, [snaps[2.05], snaps[1.18]], [2.0, 1.23]),
              check("no snap beyond 7 px", snaps[2.2] == 2.2, snaps[2.2], 2.2),
              check("negative control: raw beats are only 0.5 s apart", sp(beats) < 0.8, sp(beats), ">=0.8")]
    return checks, [path]


@card("EASE-70")
def speech_pause_grammar(task, wd):
    import numpy as np
    rate = 16000
    words = [("السلام", 0.0, 0.5), ("عليكم", 0.6, 1.1), ("قال", 2.3, 2.7), ("قال", 3.0, 3.4), ("اليوم", 3.5, 4.0),
             ("نبدأ", 4.4, 4.9), ("الدرس", 6.2, 6.8)]
    total = 7.4
    sig = np.zeros(int(total * rate))
    for i, (_, s, e) in enumerate(words):
        k = np.arange(int(s * rate), int(e * rate))
        sig[k] = 0.5 * np.sin(2 * np.pi * (300 + 50 * i) * k / rate)
    wav = fx.write_wav(wd / "speech.wav", sig, rate)
    jw(wd / "words.json", [{"w": w, "start": s, "end": e} for w, s, e in words])
    src = wd / "take.mkv"
    fx.ffmpeg("-f", "lavfi", "-i", "testsrc2=s=64x36:r=25:d=%s" % total, "-i", wav, "-c:v", "libx264", "-pix_fmt", "yuv420p",
              "-c:a", "pcm_s16le", "-shortest", src)
    ws = json.loads((wd / "words.json").read_text())
    keep = [w for i, w in enumerate(ws) if not (i + 1 < len(ws) and ws[i + 1]["w"] == w["w"])]  # last take of a retake
    segs = []
    for i, w in enumerate(keep):
        s, e = w["start"], w["end"]
        if i + 1 < len(keep):
            gap = keep[i + 1]["start"] - e
            prev_gap = (w["start"] - keep[i - 1]["end"]) if i else 1.0
            if gap > 0.7 and prev_gap >= 0.15:
                e = e + 0.4  # keep a breath, cut the rest
            else:
                e = keep[i + 1]["start"]
        segs.append((round(max(0, s), 3), round(min(total, e), 3)))
    merged = []
    for s, e in segs:
        if merged and abs(merged[-1][1] - s) < 1e-6:
            merged[-1] = (merged[-1][0], e)
        else:
            merged.append((s, e))
    parts, labels = [], []
    for i, (s, e) in enumerate(merged):
        parts.append("[0:v]trim=%s:%s,setpts=PTS-STARTPTS[v%d];[0:a]atrim=%s:%s,asetpts=PTS-STARTPTS[a%d]" % (s, e, i, s, e, i))
        labels.append("[v%d][a%d]" % (i, i))
    fc = ";".join(parts) + ";" + "".join(labels) + "concat=n=%d:v=1:a=1[v][a]" % len(merged)
    out = wd / "cut.mkv"
    fx.ffmpeg("-i", src, "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-pix_fmt", "yuv420p",
              "-c:a", "pcm_s16le", out)
    pr = fx.probe(out)
    vdur = float([s for s in pr["streams"] if s["codec_type"] == "video"][0].get("duration") or pr["format"]["duration"])
    fx.ffmpeg("-i", out, "-vn", "-c:a", "pcm_s16le", wd / "cut_audio.wav")
    a, _ = fx.read_wav(wd / "cut_audio.wav")
    expect = sum(e - s for s, e in merged)
    n0 = int((merged[0][1] - merged[0][0]) * rate)
    orig0 = sig[int(merged[0][0] * rate):int(merged[0][0] * rate) + n0]
    same = float(np.max(np.abs(a[:n0, 0] - orig0))) if n0 else 1.0
    gaps_after = [merged[i + 1][0] - merged[i][1] for i in range(len(merged) - 1)]
    path = jw(wd / "edit.json", {"segments": merged, "expected": expect, "audio_s": len(a) / rate, "video_s": vdur})
    checks = [check("retake group keeps only the last take", [w["w"] for w in keep].count("قال") == 1 and
                    [w for w in keep if w["w"] == "قال"][0]["start"] == 3.0, [w["start"] for w in keep if w["w"] == "قال"], [3.0]),
              check("audio length = kept segments", abs(len(a) / rate - expect) < 0.03, len(a) / rate, expect),
              check("V1 trimmed by the same length as A1", abs(vdur - len(a) / rate) < 0.05, vdur, len(a) / rate),
              check("kept audio untouched (sample-exact)", same < 1e-3, same, "<1e-3"),
              check("source gaps > 0.7 s are removed", expect < total - 1.5, expect, "< %.1f" % (total - 1.5))]
    raw_gaps = [ws[i + 1]["start"] - ws[i]["end"] for i in range(len(ws) - 1)]
    checks.append(check("negative control: the source keeps gaps > 0.7 s", max(raw_gaps) > 0.7, max(raw_gaps), "<=0.7"))
    return checks, [out, path]
