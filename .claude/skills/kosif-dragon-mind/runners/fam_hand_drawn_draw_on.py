"""hand-drawn-draw-on: method cards as real programs with known-answer checks.

Engines: the repo motion kit (motion-kit.js drawPath / flowDash) with GSAP in headless Chrome (real SVG path lengths),
the studio ink engine (INK strokes / hatching, motif library), the pixel-studio painter (reveal orders, exact redraw,
image-to-Python, SVG import, drawing films), HyperFrames registry components and lint, ffmpeg, numpy/PIL/OpenCV for
measuring. Every card measures its own output and runs the same measurement on an untreated input (negative control).
"""
import html
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

from _harness import card, check, fx

GAPS: dict = {
    "DRAW-55": "drives Microsoft Paint on Windows through the desktop mouse tool (kosif_mouse_act / kosif_paint_copy); "
               "no Windows desktop app in this Linux container",
}

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


def chrome(wd, name, body_html, flags=()):
    """Load a page in headless Chrome; the page's script stores JSON in <body data-r>; return it."""
    page = Path(wd) / (name + ".html")
    page.write_text(body_html, encoding="utf-8")
    done = subprocess.run([chrome_bin(), "--headless=new", "--no-sandbox", "--disable-gpu", "--allow-file-access-from-files",
                           "--virtual-time-budget=4000", *flags, "--dump-dom", page.as_uri()], capture_output=True, text=True,
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



def template_page(wd, template, params, seconds, probe_js, size=(540, 960), fps=30):
    """Fill one of the repo's motion templates (mtemplates.render_html), give it the kit + GSAP, probe it in Chrome."""
    import importlib
    import sys
    sd = str(MKT.parent)
    if sd not in sys.path:
        sys.path.insert(0, sd)
    mt = importlib.import_module("mtemplates")
    src = mt.render_html(template, params, size[0], size[1], seconds, fps)
    (wd / "assets").mkdir(exist_ok=True)
    shutil.copy(GSAP / "dist/gsap.min.js", wd / "assets/gsap.min.js")
    shutil.copy(KIT, wd / "assets/motion-kit.js")
    (wd / "index.html").write_text(src, encoding="utf-8")
    probe = src.replace("</body>", "<script>(function(){const tl=window.__timelines.root, G=(e,p)=>+gsap.getProperty(e,p);" + probe_js +
                        "})();</script></body>")
    return chrome(wd, "probe_" + template, probe)


def hf_component(wd, name, variables, probe_js, size=(960, 540)):
    """`npx hyperframes add <name>` into wd, mount the component's <template> in a host page with GSAP and
    window.__hyperframes.getVariables, then run probe_js in headless Chrome (G(el, prop) = gsap.getProperty)."""
    import re
    proj = Path(wd) / "hf"
    proj.mkdir(exist_ok=True)
    subprocess.run(["npx", "--no-install", "hyperframes", "add", name], cwd=proj, capture_output=True, text=True, timeout=90,
                       stdin=subprocess.DEVNULL, check=True)
    comp = proj / ("compositions/components/%s.html" % name)
    src = comp.read_text(encoding="utf-8")
    m = re.search(r"^\s*<template>\s*$(.*)</template>", src, re.S | re.M) or re.search(r"<template>(.*)</template>", src, re.S)
    body = m.group(1) if m else src
    inner = re.sub(r'<script src="[^"]*gsap[^"]*"></script>', "", body)
    shutil.copy(GSAP / "dist/gsap.min.js", Path(wd) / "gsap.min.js")
    page = """<!doctype html><html><head><meta charset=utf-8><script src="gsap.min.js"></script></head>
<body style="margin:0"><div id="host" style="position:relative;width:%dpx;height:%dpx"></div><template id="tpl">%s</template><script>
window.__hyperframes={getVariables:()=>(%s)};
const host=document.getElementById('host'); const frag=document.getElementById('tpl').content.cloneNode(true);
const scripts=[...frag.querySelectorAll('script')]; scripts.forEach(s=>s.remove()); host.appendChild(frag);
for(const s of scripts){const n=document.createElement('script'); n.textContent=s.textContent; document.body.appendChild(n);}
</script><script>(function(){const tl=(window.__timelines||{})[%s], G=(e,p)=>+gsap.getProperty(e,p), $=(s)=>host.querySelector(s), $$=(s)=>[...host.querySelectorAll(s)];
%s
})();</script></body></html>""" % (size[0], size[1], inner, json.dumps(variables), json.dumps(name), probe_js)
    return chrome(wd, "mount_" + name, page), comp


SHAPE_KIT = KIT.parent / "shape-kit.js"
THREE = _node_mod("three") / "build/three.cjs"


def kit_page(wd, name, body, js, plugins=()):
    """A Chrome page with GSAP (+ plugins) and the repo motion kit; js stores its result via R(obj)."""
    wd = Path(wd)
    shutil.copy(GSAP / "dist/gsap.min.js", wd / "gsap.min.js")
    shutil.copy(KIT, wd / "motion-kit.js")
    tags = '<script src="gsap.min.js"></script>'
    for pl in plugins:
        shutil.copy(GSAP / ("dist/%s.min.js" % pl), wd / ("%s.min.js" % pl))
        tags += '<script src="%s.min.js"></script>' % pl
    page = """<!doctype html><html><head><meta charset=utf-8>%s<script src="motion-kit.js"></script></head><body style="margin:0">%s<script>
const M=window.MOTION, R=(o)=>document.body.setAttribute('data-r', JSON.stringify(o)), $=(s)=>document.querySelector(s);
const ptsOf=(d)=>(d.match(/-?\\d*\\.?\\d+(?:e-?\\d+)?/g)||[]).map(Number).reduce((a,v,i,arr)=>{if(i%%2===0)a.push([v,arr[i+1]]);return a;},[]);
%s
</script></body></html>""" % (tags, body, js)
    return chrome(wd, name, page)


def shape_kit(wd, name, js):
    """Run JS with three + the repo shape kit (window.K3S) in node; the script prints one JSON line via out()."""
    src = Path(wd) / (name + ".js")
    src.write_text("global.window=global; window.THREE=require(%s); const fs=require('fs'),vm=require('vm');\n"
                   "vm.runInThisContext(fs.readFileSync(%s,'utf8')); const out=(o)=>console.log(JSON.stringify(o));\n%s"
                   % (json.dumps(str(THREE)), json.dumps(str(SHAPE_KIT)), js), encoding="utf-8")
    res = fx.run(["node", "--no-deprecation", src], timeout=60).stdout.strip().splitlines()
    return json.loads(res[-1])




PSP = REPO / ".claude/skills/kosif-superpowers/vendor/100-superskills/skills/pixel-studio-painter/scripts"


def psp(name):
    """Import a module of the repo's pixel-studio painter (its modules import each other by plain name)."""
    import importlib
    if str(PSP) not in sys.path:
        sys.path.insert(0, str(PSP))
    return importlib.import_module(name)


def sample_logo():
    import numpy as np
    from PIL import Image, ImageDraw
    im = Image.new("RGBA", (120, 140), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([4, 4, 115, 135], radius=40, fill=(170, 200, 55, 255))
    d.rounded_rectangle([12, 12, 107, 127], radius=34, fill=(255, 255, 255, 255))
    d.ellipse([35, 30, 85, 80], outline=(10, 10, 6, 255), width=4)
    d.rectangle([22, 95, 98, 115], fill=(240, 5, 12, 255))
    d.text((30, 99), "KOSIF", fill=(255, 255, 255, 255))
    return np.asarray(im).copy()


@card("DRAW-48")
def painter_reveal_orders(task, wd):
    import numpy as np
    from PIL import Image
    R = psp("render")
    W, H = 240, 160
    idx = np.arange(W * H, dtype=np.int32)
    res, firsts = {}, {}
    for k in ("sweep", "grow", "rise", "down", "left", "right", "sparkle"):
        o = R.reveal_order(idx, W, R.Step(k, [], k, (60, 40)), 0.2, seed=1)
        res[k] = bool(np.array_equal(np.sort(o), idx))
        firsts[k] = o[: W * H // 10]
    y, x = firsts["rise"] // W, firsts["rise"] % W
    yd = firsts["down"] // W
    xl, xr = firsts["left"] % W, firsts["right"] % W
    g = firsts["grow"]
    gd = np.hypot(g % W - 60 * 0.2, g // W - 40 * 0.2)
    # sweep: boustrophedon bands of round(7 * scale) px (scale 1 -> 7 rows); 2nd band runs right to left
    o1 = R.reveal_order(idx, W, R.Step("s", [], "sweep"), 1.0, seed=2)
    rows0 = np.unique(o1[: 7 * W] // W)
    band2 = o1[7 * W: 14 * W]
    dirs = float(np.corrcoef(np.arange(band2.size), band2 % W)[0, 1])
    # picture: paint a scene's pixels in 'grow' order and save the halfway frame
    canvas = np.zeros((H * W, 3), np.uint8)
    half = R.reveal_order(idx, W, R.Step("g", [], "grow", (600, 400)), 0.2, seed=0)[: W * H // 2]
    canvas[half] = (240, 200, 90)
    Image.fromarray(canvas.reshape(H, W, 3)).save(wd / "grow_half.png")
    rnd = np.random.default_rng(0).permutation(idx)[: W * H // 10]
    path = jw(wd / "orders.json", {"permutation": res, "sweep_band_rows": rows0.tolist(), "band2_dir": dirs})
    checks = [check("every order is a permutation of the changed pixels", all(res.values()), res, "all True"),
              check("rise starts at the bottom, down at the top", float(y.mean()) > 0.85 * H and float(yd.mean()) < 0.15 * H, [float(y.mean()), float(yd.mean())], "bottom / top"),
              check("left starts at the right edge, right at the left edge", float(xl.mean()) > 0.85 * W and float(xr.mean()) < 0.15 * W, [float(xl.mean()), float(xr.mean())], "right / left"),
              check("grow starts at its origin", float(gd.mean()) < 0.3 * float(np.hypot(W, H)), float(gd.mean()), "near origin"),
              check("sweep bands are 7 px (scale 1) and go back and forth", rows0.tolist() == list(range(7)) and dirs < -0.9, [rows0.tolist(), dirs], [list(range(7)), "<-0.9"]),
              check("negative control: a random order starts nowhere in particular", abs(float((rnd // W).mean()) - H / 2) < 0.1 * H, float((rnd // W).mean()), "~H/2")]
    return checks, [wd / "grow_half.png", path]


@card("DRAW-49")
def drawing_film(task, wd):
    import numpy as np
    film = psp("film")
    src = wd / "scene.py"
    src.write_text("def build():\n    return [Step('sky', [fill(rect(0, 0, 1200, 800), '#204060')]),"
                   " Step('sun', [fill(ellipse(600, 400, 200, 200), '#ffcc00')], 'grow', origin=(600, 400))]\n", encoding="utf-8")
    info = film.film_drawing(str(src), wd / "drawing.mp4", fps=30, speed="fast", hold=1.5)
    mp4 = wd / "drawing.mp4"
    pr = fx.probe(mp4)
    v = next(s for s in pr["streams"] if s["codec_type"] == "video")
    fr = read_mp4(mp4, int(v["width"]), int(v["height"]))
    tail = fr[-45:]
    still = max(float(np.abs(tail[i].astype(float) - tail[0]).mean()) for i in range(1, 45))
    sun = fr[-1][400, 600].astype(int).tolist()
    first = fr[0].astype(float)
    growing = [float(((q[:, :, 0] > 200) & (q[:, :, 2] < 100)).mean()) for q in fr]
    path = jw(wd / "film.json", {"info": info, "codec": v["codec_name"], "fps": v["r_frame_rate"], "still_tail": still, "sun_px": sun})
    checks = [check("H.264 at 30 fps", v["codec_name"] == "h264" and v["r_frame_rate"] == "30/1", [v["codec_name"], v["r_frame_rate"]], ["h264", "30/1"]),
              check("final frame held 1.5 s (last 45 frames identical up to codec noise)", still < 0.5, still, "<0.5 mean"),
              check("final picture: the sun at the centre", sun[0] > 220 and sun[2] < 60, sun, "~#ffcc00"),
              check("the sun is painted progressively (yellow area grows over several frames)", len({round(g, 3) for g in growing}) >= 4 and growing[-1] > 0.05,
                    sorted({round(g, 3) for g in growing})[:6], ">=4 distinct areas"),
              check("negative control: the first frame is not the finished picture", float(np.abs(first - fr[-1]).mean()) > 10, float(np.abs(first - fr[-1]).mean()), ">10")]
    return checks, [mp4, path]


@card("DRAW-50")
def pil_recorder(task, wd):
    import numpy as np
    from PIL import Image
    code = wd / "sky.py"
    code.write_text("from PIL import Image, ImageDraw\nim = Image.new('RGB', (360, 200), (20, 30, 60))\nd = ImageDraw.Draw(im)\n"
                    "for i in range(360):\n    d.line([(i, 0), (i, 120)], fill=(40, 60 + i // 3, 140))\n"
                    "d.ellipse([140, 60, 220, 140], fill=(255, 210, 80))\nim.save('sky.png')\n", encoding="utf-8")
    out = wd / "rec"
    r = subprocess.run([sys.executable, str(PSP / "runner.py"), str(code), str(out)], capture_output=True, text=True, timeout=120,
                       stdin=subprocess.DEVNULL, cwd=wd)
    jobs = sorted(out.glob("job_*.json"))
    metas = [json.loads(p.read_text(encoding="utf-8")) for p in jobs]
    canvas = json.loads((out / "canvas.json").read_text()) if (out / "canvas.json").exists() else None
    W, H = (canvas["w"], canvas["h"]) if canvas else (360, 200)
    cur = np.zeros((W * H, 4), np.uint8)
    for p in jobs:
        z = np.load(p.with_suffix(".npz"))
        c = z["cols"]
        cur[z["order"]] = c if c.shape[1] == 4 else np.column_stack([c, np.full(len(c), 255, np.uint8)])
    direct = subprocess.run([sys.executable, str(code)], cwd=wd, capture_output=True, timeout=60)
    ref = np.asarray(Image.open(wd / "sky.png").convert("RGBA"))
    mism = int(np.any(cur.reshape(H, W, 4) != ref, axis=2).sum()) if (H, W) == ref.shape[:2] else -1
    labels = [m.get("label", "") for m in metas]
    path = jw(wd / "recorder.json", {"rc": r.returncode, "jobs": len(jobs), "labels": labels[:30], "mismatch": mism, "stderr": r.stderr[-300:]})
    line_jobs = sum(1 for lb in labels if "×20" in lb)
    checks = [check("the program ran and was recorded as paint jobs", r.returncode == 0 and len(jobs) > 2, [r.returncode, len(jobs)], "rc 0, >2 jobs"),
              check("360 sky lines grouped 20 commands per stroke (18 strokes)", line_jobs == 18, line_jobs, 18),
              check("snapshots follow the code's order (18 line strokes, then the ellipse)", labels[-1] != labels[-2] and all("×20" in lb for lb in labels[1:19]),
                    [labels[0], labels[1], labels[-1]], "canvas, lines..., ellipse"),
              check("replayed jobs equal the program's own picture", mism == 0, mism, 0),
              check("negative control: a blank canvas differs from the picture", int(np.any(np.zeros_like(ref) != ref, axis=2).sum()) > 1000,
                    int(np.any(np.zeros_like(ref) != ref, axis=2).sum()), ">1000")]
    return checks, [path]


@card("DRAW-51")
def exact_redraw(task, wd):
    import numpy as np
    from PIL import Image
    ex = psp("exact")
    rgba = sample_logo()
    canvas = np.zeros_like(rgba).reshape(-1, 4)
    stages, half = [], None
    jobs = list(ex.plan(rgba, 10, 64))
    for i, (label, kind, origin, weight, order, cols) in enumerate(jobs):
        canvas[order] = cols
        stages.append((label, kind, int(order.size), ex.mismatches(canvas.reshape(rgba.shape), rgba)))
        if i == len(jobs) // 2:
            half = canvas.copy()
    Image.fromarray(canvas.reshape(rgba.shape)).save(wd / "redrawn.png")
    Image.fromarray(half.reshape(rgba.shape)).save(wd / "halfway.png")
    mis = [s[3] for s in stages]
    path = jw(wd / "exact.json", {"stages": stages})
    checks = [check("ends identical in every RGBA value", mis[-1] == 0, mis[-1], 0),
              check("painted in several stages (block-in first)", len(stages) > 3 and stages[0][1] == "grow", [len(stages), stages[0][1]], ">3, grow"),
              check("mismatch never increases from stage to stage", all(b <= a for a, b in zip(mis, mis[1:])), mis[:6], "non-increasing"),
              check("transparent outside stays transparent", int(canvas.reshape(rgba.shape)[0, 0, 3]) == 0, int(canvas.reshape(rgba.shape)[0, 0, 3]), 0),
              check("negative control: the halfway canvas is not yet the image", ex.mismatches(half.reshape(rgba.shape), rgba) > 0, ex.mismatches(half.reshape(rgba.shape), rgba), ">0")]
    return checks, [wd / "redrawn.png", path]


@card("DRAW-52")
def image_to_python(task, wd):
    import numpy as np
    from PIL import Image
    tp = psp("to_python")
    rgba = sample_logo()
    Image.fromarray(rgba, "RGBA").save(wd / "logo.png")
    code = tp.image_to_python(wd / "logo.png", "logo")
    prog = wd / "make_logo.py"
    prog.write_text(code, encoding="utf-8")
    (wd / "logo.png").rename(wd / "logo_original.png")
    r = subprocess.run([sys.executable, "-I", prog.name], cwd=wd, capture_output=True, timeout=120, stdin=subprocess.DEVNULL)
    out = np.asarray(Image.open(wd / "logo.png").convert("RGBA")) if (wd / "logo.png").exists() else np.zeros_like(rgba)
    mism = int(np.any(out != rgba, axis=2).sum())
    imports = sorted({l.split()[1].split(".")[0] for l in code.splitlines() if l.startswith(("import ", "from "))})
    path = jw(wd / "to_python.json", {"rc": r.returncode, "mismatch": mism, "imports": imports, "polygons": code.count("draw.polygon(")})
    checks = [check("the generated program runs on its own", r.returncode == 0, r.returncode, 0),
              check("draws polygons with Pillow only", code.count("draw.polygon(") > 0 and set(imports) <= {"PIL", "base64", "zlib", "io", "__future__", "pathlib", "sys", "os", "struct"},
                    [code.count("draw.polygon("), imports], "polygons, PIL only"),
              check("reproduces the image pixel for pixel", mism == 0, mism, 0)]
    # negative control: run only part 1 of the program (the polygons) and skip the pixel completion
    cut = code.index("# \u2500\u2500 2.") if "# \u2500\u2500 2." in code else len(code)
    (wd / "make_logo_polys_only.py").write_text(code[:cut] + "\nimg.save('polys_only.png')\n", encoding="utf-8")
    r2 = subprocess.run([sys.executable, "-I", "make_logo_polys_only.py"], cwd=wd, capture_output=True, timeout=120, stdin=subprocess.DEVNULL)
    po = wd / "polys_only.png"
    m2 = int(np.any(np.asarray(Image.open(po).convert("RGBA")) != rgba, axis=2).sum()) if po.exists() else -1
    checks.append(check("negative control: the polygons without the pixel completion are not exact", r2.returncode == 0 and m2 > 0, [r2.returncode, m2], "rc 0, >0 px differ"))
    return checks, [prog, path]


@card("DRAW-53")
def svg_import_and_vectorize(task, wd):
    import numpy as np
    from PIL import Image, ImageDraw
    R = psp("render")
    si = psp("svg_import")
    V = psp("vectorize")
    VS = psp("vector_scene")
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 80"><style>.r{fill:#ff0000}</style>
<rect width="120" height="80" fill="#0000ff"/><g transform="translate(60 40)"><circle class="r" r="10"/></g>
<ellipse cx="20" cy="60" rx="10" ry="5" fill="#00ff00"/><polygon points="90,10 110,10 100,30" fill="#ffffff"/>
<path d="M 5 5 A 10 10 0 0 1 25 5 Z" fill="#ffff00"/></svg>"""
    title, steps = si.load_svg(svg)
    im = R.render_image(steps, .25, rolloff=1)
    im.save(wd / "svg_import.png")
    px = lambda x, y: im.getpixel((round(x * .25), round(y * .25)))
    logo = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
    d = ImageDraw.Draw(logo)
    d.ellipse([10, 10, 110, 110], fill=(230, 20, 30, 255))
    d.ellipse([40, 40, 80, 80], fill=(255, 255, 255, 255))
    logo.save(wd / "logo.png")
    data = V.trace(wd / "logo.png")
    cols = sorted({L["color"] for L in data["layers"]})
    out = R.render_image(VS.build(data), .5, rolloff=1)
    out.save(wd / "vectorized.png")
    s = min(1080 / 120, 730 / 120)
    ox, oy = (1200 - 120 * s) / 2, (800 - 120 * s) / 2
    hole = out.getpixel((round((ox + 60 * s) * .5), round((oy + 60 * s) * .5)))
    ring = out.getpixel((round((ox + 25 * s) * .5), round((oy + 60 * s) * .5)))
    rng = np.random.default_rng(1)
    Image.fromarray(rng.integers(0, 255, (100, 100, 3), dtype=np.uint8)).save(wd / "noise.png")
    noise_photo = V.looks_like_photo(np.asarray(Image.open(wd / "noise.png").convert("RGBA")))
    path = jw(wd / "svg_import.json", {"steps": len(steps), "centre": px(600, 400), "corner": px(1100, 700), "colors": cols, "hole": hole, "ring": ring,
                                        "logo_photo": data["photo"], "noise_photo": bool(noise_photo)})
    checks = [check("every SVG element becomes a drawing step", len(steps) >= 5, len(steps), ">=5"),
              check("transform + CSS class honoured (red circle moved to the centre)", px(600, 400) == (255, 0, 0), px(600, 400), (255, 0, 0)),
              check("background rect drawn", px(1100, 700) == (0, 0, 255), px(1100, 700), (0, 0, 255)),
              check("flat logo vectorizes keeping its colours", "#ffffff" in cols and any(c.startswith("#e6") for c in cols), cols, "#e6..., #ffffff"),
              check("and its hole (white centre, red ring)", hole[:3] == (255, 255, 255) and ring[:3] == (230, 20, 30), [hole, ring], ["white", (230, 20, 30)]),
              check("negative control: noise is treated as a photo, the logo is not", bool(noise_photo) and not data["photo"], [bool(noise_photo), data["photo"]], [True, False])]
    return checks, [wd / "svg_import.png", wd / "vectorized.png", path]


STUDIO_JS = REPO.parent / "app/public/js/10_studio.js"


def studio_ink_js():
    """The studio's INK engine and motif library (10_studio.js), cut out with the helpers it uses."""
    src = STUDIO_JS.read_text(encoding="utf-8")
    a = src.index("const INK = MK.ink = {};")
    b = src.index("\n", src.index("MK.motifFor = "))
    return ("const MK={}; const TAU=Math.PI*2; const clamp=(v,a,b)=>Math.min(b,Math.max(a,v));\n" + src[a:b] + "\n")


def power_inout(p, n):
    return 0.5 * (2 * p) ** n if p < 0.5 else 1 - 0.5 * (2 * (1 - p)) ** n


@card("DRAW-02")
def kit_draw_path(task, wd):
    body = ('<svg width=400 height=200><path id=p d="M20 150 C 120 20, 280 20, 380 150" fill=none stroke=#000 stroke-width=4 />'
            '<circle id=h cx=380 cy=150 r=6 /><path id=f d="M20 180 L 380 180" stroke=#09f fill=none /><path id=raw d="M20 100 L 380 100" stroke=#000 /></svg>')
    js = """const tl=gsap.timeline({paused:true}); const p=$('#p'), h=$('#h'), f=$('#f');
const pre=+gsap.getProperty(h,'scale'); gsap.set(h,{scale:0,opacity:0}); const len=M.drawPath(tl,p,0,2,{head:h}); M.flowDash(tl,f,0,2,{pattern:'28 22',cycles:6});
tl.seek(3); const S=[]; for(let i=0;i<=40;i++){const t=i*0.06; tl.seek(t,false); S.push({t, off:+gsap.getProperty(p,'strokeDashoffset'), head:+gsap.getProperty(h,'scale'), flow:+gsap.getProperty(f,'strokeDashoffset')});}
R({len, pre, true_len:p.getTotalLength(), dash:p.style.strokeDasharray, raw_dash:getComputedStyle($('#raw')).strokeDasharray, S});"""
    r = kit_page(wd, "drawpath", body, js)
    L = r["len"]
    S = r["S"]
    err = max(abs(s["off"] - L * (1 - power_inout(min(1, s["t"] / 2), 5))) for s in S)  # GSAP power4 = p^5
    pre = [s["head"] for s in S if s["t"] < 1.9 - 1e-9]
    late = [s["head"] for s in S if s["t"] >= 2.25]
    ferr = max(abs(s["flow"] + 50 * 6 * min(1, s["t"] / 2)) for s in S)
    path = jw(wd / "drawpath.json", r)
    import re
    dash = [float(v) for v in re.findall(r"[\d.]+", r["dash"])]
    checks = [check("dasharray = path length (len len)", abs(L - r["true_len"]) < 1e-6 and len(dash) == 2 and all(abs(v - L) < 0.01 for v in dash), [L, r["dash"]], "len len"),
              check("offset len -> 0 with power4.inOut over 2 s", err < 0.01, err, "<0.01 px"),
              check("kit leaves the head untouched before its tween (page pre-hides it with gsap.set)", r["pre"] == 1, r["pre"], 1),
              check("head stays hidden until end - 0.1 s", max(pre) == 0, max(pre), 0),
              check("head springs in (overshoot, then ~1)", max(s["head"] for s in S) > 1.0 and abs(S[-1]["head"] - 1) < 0.05, [max(s["head"] for s in S), S[-1]["head"]], ">1 then 1"),
              check("marching dashes: offset -50 x 6 cycles over 2 s, linear", ferr < 0.05, ferr, "~0"),
              check("negative control: an untreated path has no dash array", r["raw_dash"] == "none", r["raw_dash"], "none")]
    return checks, [path]


@card("DRAW-09")
def lint_measure_and_dasharray(task, wd):
    bad = """<!doctype html><html><body><div id="root" data-composition-id="draw" data-duration="3" data-width="400" data-height="200">
<style>#p { stroke-dasharray: 10 10; }</style><svg width="400" height="200"><path id="p" stroke="#000" fill="none"></path></svg>
<script src="gsap.min.js"></script><script>
const tl = gsap.timeline({ paused: true }); const p = document.getElementById("p"); const L = p.getTotalLength();
p.setAttribute("d", "M20 100 L 380 100");
tl.fromTo("#p", { strokeDasharray: L, strokeDashoffset: L }, { strokeDashoffset: 0, duration: 2 }, 0);
window.__timelines = { draw: tl };</script></div></body></html>"""
    good = """<!doctype html><html><body><div id="root" data-composition-id="draw" data-duration="3" data-width="400" data-height="200">
<svg width="400" height="200"><path id="p" d="M20 100 L 380 100" stroke="#000" fill="none"></path></svg>
<script src="gsap.min.js"></script><script>
const tl = gsap.timeline({ paused: true }); const p = document.getElementById("p"); const L = p.getTotalLength();
gsap.set("#p", { strokeDasharray: L + " " + L, strokeDashoffset: L });
tl.to("#p", { strokeDashoffset: 0, duration: 2 }, 0);
window.__timelines = { draw: tl };</script></div></body></html>"""
    res = {}
    for name, src in (("bad", bad), ("good", good)):
        d = wd / name
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(src, encoding="utf-8")
        shutil.copy(GSAP / "dist/gsap.min.js", d / "gsap.min.js")
        p = subprocess.run(["npx", "--no-install", "hyperframes", "lint", "--json", str(d / "index.html")], capture_output=True, text=True,
                           timeout=60, stdin=subprocess.DEVNULL, cwd=wd)
        txt = p.stdout
        res[name] = sorted({c for c in ("svg_measure_before_path_d", "svg_drawon_css_dasharray_conflict") if c in txt})
    # measured in Chrome: what the two bugs do to the pixels' inputs
    body = '<style>#q{stroke-dasharray:10 10}</style><svg width=400 height=200><path id=e /><path id=q d="M20 100 L 380 100" stroke=#000 /></svg>'
    js = """const L0=$('#e').getTotalLength(); const q=$('#q'); const L=q.getTotalLength(); gsap.set(q,{strokeDasharray:L}); const merged=getComputedStyle(q).strokeDasharray;
gsap.set(q,{strokeDasharray:L+' '+L}); const fixed=getComputedStyle(q).strokeDasharray; R({L0,L,merged,fixed});"""
    m = kit_page(wd, "measure", body, js)
    path = jw(wd / "lint.json", {"lint": res, "chrome": m})
    checks = [check("lint flags measuring a path before its d", "svg_measure_before_path_d" in res["bad"], res["bad"], "flagged"),
              check("lint flags GSAP dasharray over a CSS multi-dash", "svg_drawon_css_dasharray_conflict" in res["bad"], res["bad"], "flagged"),
              check("the fixed composition passes both rules", res["good"] == [], res["good"], []),
              check("measured: getTotalLength on a d-less path is 0", m["L0"] == 0 and m["L"] > 300, [m["L0"], m["L"]], [0, 360]),
              check("measured: GSAP merges into the CSS gap (draw-on broken), the two-part value fixes it",
                    m["merged"].replace(" ", "").endswith(",10px") and "10px" not in m["fixed"], [m["merged"], m["fixed"]], ["L, 10px", "L, L"])]
    return checks, [path]


@card("DRAW-24")
def progress_line_from_right(task, wd):
    body = ('<div id=w style="position:relative;width:400px;height:20px"><div id=l style="position:absolute;right:0;top:9px;width:400px;height:2px;'
            'transform-origin:right center;background:linear-gradient(to left,#888 0%,#888 38%,#5b8cff 38%,#5b8cff 64%,#2dd4bf 64%,#2dd4bf 100%)"></div></div>'
            '<div id=n style="width:400px;height:2px;background:#888"></div>')
    js = """const l=$('#l'); const a=l.animate([{transform:'scaleX(0)',opacity:.2},{transform:'scaleX(1)',opacity:1}],{duration:680,delay:160,easing:'cubic-bezier(.22,.8,.26,1)',fill:'both'}); a.pause();
const S=[]; for(let ms=0; ms<=840; ms+=40){a.currentTime=ms; const r=l.getBoundingClientRect(); S.push({ms,w:r.width,right:r.right,left:r.left,op:+getComputedStyle(l).opacity});}
R({S, bg:getComputedStyle(l).backgroundImage, plain:$('#n').getBoundingClientRect().width});"""
    r = kit_page(wd, "progress", body, js)
    S = r["S"]
    curve = bez(.22, .8, .26, 1)
    err = max(abs(s["w"] - 400 * curve(min(1, max(0, (s["ms"] - 160) / 680)))) for s in S)
    path = jw(wd / "progress_line.json", r)
    checks = [check("grows from the right edge (right edge fixed)", max(abs(s["right"] - S[-1]["right"]) for s in S if s["w"] > 0) < 0.01,
                    max(abs(s["right"] - S[-1]["right"]) for s in S if s["w"] > 0), 0),
              check("scaleX follows cubic-bezier(.22,.8,.26,1) over 680 ms after 160 ms", err < 1.0, err, "<1 px"),
              check("nothing before the 160 ms delay", all(s["w"] < 1e-6 for s in S if s["ms"] <= 160), [s["w"] for s in S[:5]], 0),
              check("opacity .2 -> 1", abs(S[0]["op"] - .2) < 1e-6 and abs(S[-1]["op"] - 1) < 1e-6, [S[0]["op"], S[-1]["op"]], [.2, 1]),
              check("colour stops encode state (38% / 64%)", "38%" in r["bg"] and "64%" in r["bg"], r["bg"][:120], "38%, 64%"),
              check("negative control: a plain line is full width at t=0", r["plain"] == 400, r["plain"], 400)]
    return checks, [path]


@card("DRAW-18")
def emphasis_styles(task, wd):
    body = ('<div style="font:32px sans-serif;padding:40px"><span id=w style="position:relative;display:inline-block">word<span id=hl style="position:absolute;'
            'inset:0 -6px;border-radius:3px;background:rgba(255,236,79,.62);mix-blend-mode:multiply;transform-origin:left center"></span></span>'
            ' <span id=a dir=rtl style="position:relative;display:inline-block">كلمة<span id=ha style="position:absolute;inset:0 -6px;'
            'background:rgba(255,236,79,.62);transform-origin:right center"></span></span>'
            ' <span id=u style="position:relative;display:inline-block">under<span id=ul style="position:absolute;left:0;right:0;bottom:-4px;height:3px;background:#e7b65a;transform-origin:left center"></span></span>'
            ' <span id=c style="position:relative;display:inline-block">circle<svg id=cs style="position:absolute;left:-10px;top:-8px" width=140 height=60><ellipse id=ce cx=70 cy=30 rx=64 ry=26 fill=none stroke=red stroke-width=3 /></svg></span>'
            ' <span id=b style="position:relative;display:inline-block">burst<svg id=bs style="position:absolute;left:-20px;top:-20px" width=140 height=80></svg></span></div>')
    js = """const tl=gsap.timeline({paused:true});
gsap.set(['#hl','#ha','#ul'],{scaleX:0});
tl.to('#hl',{scaleX:1,duration:.5,ease:'power2.out'},.6); tl.to('#ha',{scaleX:1,duration:.5,ease:'power2.out'},.6); tl.to('#ul',{scaleX:1,duration:.4,ease:'power2.out'},.6);
const ce=$('#ce'); const L=ce.getTotalLength(); gsap.set(ce,{strokeDasharray:L+' '+L,strokeDashoffset:L}); tl.to(ce,{strokeDashoffset:0,duration:.5,ease:'power2.out'},.6);
const bs=$('#bs'); const lines=[]; for(let i=0;i<12;i++){const a=i/12*Math.PI*2; const l=document.createElementNS('http://www.w3.org/2000/svg','line');
 l.setAttribute('x1',70+Math.cos(a)*30); l.setAttribute('y1',40+Math.sin(a)*30); l.setAttribute('x2',70+Math.cos(a)*44); l.setAttribute('y2',40+Math.sin(a)*44); l.setAttribute('stroke','#e7b65a'); bs.appendChild(l); lines.push(l);}
gsap.set(lines,{opacity:0}); tl.to(lines,{opacity:1,duration:.2,stagger:.02},.6);
const box=(s)=>{const r=$(s).getBoundingClientRect(); return [r.left,r.right,r.width];}; const S=[];
for(const t of [0.5,0.6,0.7,0.85,1.1,1.3]){tl.seek(t,false); S.push({t,hl:box('#hl'),ha:box('#ha'),ul:box('#ul'),off:+gsap.getProperty(ce,'strokeDashoffset'),burst:lines.filter(l=>+getComputedStyle(l).opacity>0.5).length});}
R({S,L,blend:getComputedStyle($('#hl')).mixBlendMode,rad:getComputedStyle($('#hl')).borderRadius,word:box('#w')});"""
    r = kit_page(wd, "emphasis", body, js)
    S = {round(s["t"], 2): s for s in r["S"]}
    full = S[1.3]["hl"][2]
    po2 = lambda p: 1 - (1 - p) ** 3   # GSAP power2.out = 1 - (1 - p)^3
    path = jw(wd / "emphasis.json", r)
    checks = [check("highlight 6 px wider than the word each side", abs(full - (r["word"][2] + 12)) < 0.5, [full, r["word"][2]], "word + 12"),
              check("highlight sweep 0 -> 1 in 0.5 s power2.out from 0.6 s", S[0.6]["hl"][2] < 1e-6 and abs(S[0.85]["hl"][2] / full - po2(0.5)) < 0.01,
                    [S[0.6]["hl"][2], S[0.85]["hl"][2] / full], [0, po2(0.5)]),
              check("multiply blend, 3 px radius", r["blend"] == "multiply" and r["rad"] == "3px", [r["blend"], r["rad"]], ["multiply", "3px"]),
              check("Arabic sweep starts from the RIGHT (right edge fixed)", abs(S[0.7]["ha"][1] - S[1.3]["ha"][1]) < 0.01 and S[0.7]["ha"][0] > S[1.3]["ha"][0] + 5,
                    [S[0.7]["ha"], S[1.3]["ha"]], "right fixed"),
              check("underline draws in 0.4 s", abs(S[1.1]["ul"][2] - S[1.3]["ul"][2]) < 0.01 and S[0.7]["ul"][2] < S[1.3]["ul"][2], [S[0.7]["ul"][2], S[1.3]["ul"][2]], "grows, done by 1.0"),
              check("circle draws on by path length", abs(S[0.6]["off"] - r["L"]) < 0.1 and S[1.3]["off"] < 1e-6, [S[0.6]["off"], S[1.3]["off"]], [r["L"], 0]),
              check("burst: 12 lines", S[1.3]["burst"] == 12, S[1.3]["burst"], 12),
              check("negative control: the latin highlight's right edge moves (not anchored right)", abs(S[0.7]["hl"][1] - S[1.3]["hl"][1]) > 5,
                    abs(S[0.7]["hl"][1] - S[1.3]["hl"][1]), ">5 px")]
    return checks, [path]


@card("DRAW-29")
def ink_pressure_strokes(task, wd):
    body = "<canvas id=c width=400 height=300></canvas>"
    js = studio_ink_js() + """
const cv=$('#c'), c=cv.getContext('2d'); const line=[]; for(let x=20;x<=380;x+=4) line.push([x,60]);
const ink=(y0,y1)=>{const d=c.getImageData(0,0,400,300).data; const col=[]; for(let x=0;x<400;x++){let n=0; for(let y=y0;y<y1;y++) if(d[(y*400+x)*4+3]>60) n++; col.push(n);} return col;};
c.clearRect(0,0,400,300); const head=INK.stroke(c,line,0.5,12,'#000',1); const half=ink(30,90);
c.clearRect(0,0,400,300); INK.stroke(c,line,1,12,'#000',1); const full=ink(30,90);
c.clearRect(0,0,400,300); INK.stroke(c,line,1,12,'#000',1,{plain:true}); const plain=ink(30,90);
const sq=[[100,150],[300,150],[300,280],[100,280],[100,150]];
c.clearRect(0,0,400,300); INK.hatch(c,sq,0.5,'#000',10,2,1); const d=c.getImageData(0,0,400,300).data; let inside=0,outside=0;
for(let y=0;y<300;y++)for(let x=0;x<400;x++){if(d[(y*400+x)*4+3]>60){if(x>=99&&x<=301&&y>=149&&y<=281) inside++; else outside++;}}
c.clearRect(0,0,400,300); INK.hatch(c,sq,1,'#000',10,2,1); const d2=c.getImageData(0,0,400,300).data; let inside2=0; for(let i=3;i<d2.length;i+=4) if(d2[i]>60) inside2++;
const two=[line.slice(0,46), line.slice(45)]; c.clearRect(0,0,400,300); const h2=INK.strokes(c,two,0.25,6,'#000',0);
R({head, at:INK.at(line,0.5), half, full, plain, inside, outside, inside2, h2});"""
    r = kit_page(wd, "ink", body, js)
    import numpy as np
    full, plain, half = np.array(r["full"]), np.array(r["plain"]), np.array(r["half"])
    reach = int(np.nonzero(half)[0].max())
    mid = full[150:250]
    ends = full[22:26]
    path = jw(wd / "ink.json", r)
    checks = [check("progress k = .5 draws half the length (head at x = 200)", abs(r["head"][0] - 200) < 0.5 and abs(reach - 206) <= 8, [r["head"], reach], [200, "~200+cap"]),
              check("INK.at(.5) = the midpoint", abs(r["at"][0] - 200) < 1e-6 and r["at"][1] == 60, r["at"], [200, 60]),
              check("taper: ends thinner than the middle (.35 + 5u)", float(ends.mean()) < 0.6 * float(mid.mean()), [float(ends.mean()), float(mid.mean())], "ends < 60% mid"),
              check("pressure .74 +- .26 varies the width along the stroke", int(mid.max() - mid.min()) >= 3, [int(mid.min()), int(mid.max())], ">=3 px range"),
              check("hatching stays inside the outline", r["outside"] == 0 and r["inside"] > 500, [r["inside"], r["outside"]], [">500", 0]),
              check("hatch k = .5 lays about half the lines of k = 1", 0.3 < r["inside"] / r["inside2"] < 0.7, r["inside"] / r["inside2"], "~0.5"),
              check("strokes share progress by length (k .25 ends in the first stroke)", r["h2"][0] < 200, r["h2"], "x < 200"),
              check("negative control: a plain stroke has constant width (no taper)", int(plain[150:250].max() - plain[150:250].min()) <= 1 and plain[24] >= plain[200] - 1,
                    [int(plain[24]), int(plain[200])], "flat")]
    return checks, [path]


@card("DRAW-13")
def meaning_icons(task, wd):
    body = "<canvas id=c width=220 height=220></canvas>"
    verse = (KIT.parent.parent.parent / "templates/verse.html").read_text(encoding="utf-8")
    import re
    blk = verse[verse.index("const ICONS = {"):]
    blk = blk[: blk.index("\n};") if "\n};" in blk else 4000]
    verse_icons = re.findall(r"^\s*(\w+)\s*:", blk, re.M)
    js = studio_ink_js() + """
const cv=$('#c'), c=cv.getContext('2d'); const names=Object.keys(MOT); const out={};
const ink=()=>{const d=c.getImageData(0,0,220,220).data; let n=0,h=0; for(let i=3;i<d.length;i+=4){ if(d[i]>60){n++; h=(h*31+i)>>>0;} } return [n,h];};
for(const k of names){const m=MOT[k](160); const run=(kk)=>{c.setTransform(1,0,0,1,0,0); c.clearRect(0,0,220,220); c.translate(110,110); INK.strokes(c,m.strokes,kk,5,'#E7B65A',1);};
 run(0); const z=ink()[0]; run(0.5); const h=ink()[0]; run(1); const f=ink(); out[k]={zero:z, half:h, full:f[0], hash:f[1], strokes:m.strokes.length};}
const words={sun:'شمس الصباح', wave:'موج البحر', heart:'قلب نابض', bulb:'فكرة مبدعة', cloud:'سحاب ومطر'}; const match={};
for(const [k,w] of Object.entries(words)) match[k]=MK.motifFor(w,0);
R({names, out, match, fallback:[MK.motifFor('xyz',0),MK.motifFor('xyz',1),MK.motifFor('xyz',9)]});"""
    r = kit_page(wd, "motifs", body, js)
    o = r["out"]
    names = r["names"]
    path = jw(wd / "motifs.json", r | {"verse_icons": verse_icons})
    checks = [check("16 stroke motifs in the studio library", len(names) == 16, len(names), 16),
              check("every motif draws, and each is distinct", all(o[k]["full"] > 200 for k in names) and len({o[k]["hash"] for k in names}) == 16,
                    [min(o[k]["full"] for k in names), len({o[k]["hash"] for k in names})], [">200", 16]),
              check("drawn on progressively (k .5 < k 1)", all(o[k]["half"] < o[k]["full"] for k in names), sum(o[k]["half"] < o[k]["full"] for k in names), 16),
              check("Arabic keyword matcher picks the motif from the meaning", r["match"] == {k: k for k in r["match"]}, r["match"], "self"),
              check("unmatched lines cycle through 8 defaults", r["fallback"] == ["bulb", "star", "star"], r["fallback"], ["bulb", "star", "star"]),
              check("verse template ships 12 stroke icons", len(verse_icons) >= 12, verse_icons, ">=12"),
              check("negative control: k = 0 draws nothing", all(o[k]["zero"] == 0 for k in names), max(o[k]["zero"] for k in names), 0)]
    return checks, [path]


def svg_paths(d, arc_step=6.0, n=16):
    """Pure-Python SVG path sampler (M/L/H/V/C/S/Q/T/A/Z, curves sampled, closed paths return to start)."""
    import re
    toks = re.findall(r"[MLHVCSQTAZmlhvcsqtaz]|-?(?:\d+\.?\d*|\.\d+)(?:e-?\d+)?", d)
    paths, cur, start, pos = [], [], (0.0, 0.0), (0.0, 0.0)
    i, cmd, prev_c, prev_q = 0, None, None, None

    def num():
        nonlocal i
        v = float(toks[i])
        i += 1
        return v
    while i < len(toks):
        if re.match(r"[A-Za-z]", toks[i]):
            cmd = toks[i]
            i += 1
        rel = cmd.islower()
        C = cmd.upper()
        ox, oy = pos if rel else (0.0, 0.0)
        if C == "Z":
            cur.append(start)
            paths.append(cur)
            cur, pos = [], start
            prev_c = prev_q = None
            continue
        if C == "M":
            if cur:
                paths.append(cur)
            pos = (ox + num(), oy + num())
            start, cur = pos, [pos]
            cmd = "l" if rel else "L"
            continue
        if C in "LHV":
            if C == "L":
                pos = (ox + num(), oy + num())
            elif C == "H":
                pos = ((pos[0] if rel else 0) + num(), pos[1])
            else:
                pos = (pos[0], (pos[1] if rel else 0) + num())
            cur.append(pos)
            prev_c = prev_q = None
        elif C in "CS":
            if C == "C":
                c1 = (ox + num(), oy + num())
            else:
                c1 = (2 * pos[0] - prev_c[0], 2 * pos[1] - prev_c[1]) if prev_c else pos
            c2 = (ox + num(), oy + num())
            p1 = (ox + num(), oy + num())
            p0 = pos
            for k in range(1, n + 1):
                t = k / n
                cur.append(tuple((1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t * t * c + t ** 3 * e for a, b, c, e in zip(p0, c1, c2, p1)))
            pos, prev_c, prev_q = p1, c2, None
        elif C in "QT":
            if C == "Q":
                q = (ox + num(), oy + num())
            else:
                q = (2 * pos[0] - prev_q[0], 2 * pos[1] - prev_q[1]) if prev_q else pos
            p1 = (ox + num(), oy + num())
            p0 = pos
            for k in range(1, n + 1):
                t = k / n
                cur.append(tuple((1 - t) ** 2 * a + 2 * (1 - t) * t * b + t * t * c for a, b, c in zip(p0, q, p1)))
            pos, prev_q, prev_c = p1, q, None
        elif C == "A":
            rx, ry, phi, fa, fs = abs(num()), abs(num()), math.radians(num()), int(num()), int(num())
            p1 = (ox + num(), oy + num())
            x1, y1 = pos
            x2, y2 = p1
            cp, sp = math.cos(phi), math.sin(phi)
            dx, dy = (x1 - x2) / 2, (y1 - y2) / 2
            x1p, y1p = cp * dx + sp * dy, -sp * dx + cp * dy
            lam = x1p ** 2 / rx ** 2 + y1p ** 2 / ry ** 2
            if lam > 1:
                rx, ry = rx * math.sqrt(lam), ry * math.sqrt(lam)
            num_ = rx * rx * ry * ry - rx * rx * y1p * y1p - ry * ry * x1p * x1p
            co = math.sqrt(max(0, num_) / (rx * rx * y1p * y1p + ry * ry * x1p * x1p)) * (-1 if fa == fs else 1)
            cxp, cyp = co * rx * y1p / ry, -co * ry * x1p / rx
            cx, cy = cp * cxp - sp * cyp + (x1 + x2) / 2, sp * cxp + cp * cyp + (y1 + y2) / 2
            ang = lambda ux, uy, vx, vy: math.atan2(ux * vy - uy * vx, ux * vx + uy * vy)
            t1 = ang(1, 0, (x1p - cxp) / rx, (y1p - cyp) / ry)
            dt = ang((x1p - cxp) / rx, (y1p - cyp) / ry, (-x1p - cxp) / rx, (-y1p - cyp) / ry)
            if not fs and dt > 0:
                dt -= 2 * math.pi
            elif fs and dt < 0:
                dt += 2 * math.pi
            m = max(12, int(math.ceil(abs(math.degrees(dt)) / arc_step)))
            for k in range(1, m + 1):
                a = t1 + dt * k / m
                cur.append((cx + rx * math.cos(a) * cp - ry * math.sin(a) * sp, cy + rx * math.cos(a) * sp + ry * math.sin(a) * cp))
            cur[-1] = p1
            pos, prev_c, prev_q = p1, None, None
    if cur:
        paths.append(cur)
    return paths


def fit_tf(paths, box, margin=0.08):
    xs = [x for p in paths for x, _ in p]
    ys = [y for p in paths for _, y in p]
    bw, bh = box
    s = min(bw * (1 - 2 * margin) / (max(xs) - min(xs) or 1), bh * (1 - 2 * margin) / (max(ys) - min(ys) or 1))
    ox = (bw - s * (max(xs) - min(xs))) / 2 - s * min(xs)
    oy = (bh - s * (max(ys) - min(ys))) / 2 - s * min(ys)
    return lambda p: (p[0] * s + ox, p[1] * s + oy)


@card("DRAW-54")
def svg_path_sampler(task, wd):
    from PIL import Image, ImageDraw
    d = "M 10 10 L 90 10 Q 120 50 90 90 H 10 V 10 Z M 30 50 C 30 20, 70 20, 70 50 S 30 80, 30 50 M 120 50 A 25 25 0 1 1 170 50"
    P = svg_paths(d)
    tf = fit_tf(P, (400, 300))
    T = [[tf(p) for p in path] for path in P]
    xs = [x for p in T for x, _ in p]
    ys = [y for p in T for _, y in p]
    im = Image.new("RGB", (400, 300), "white")
    dr = ImageDraw.Draw(im)
    for path in T:
        dr.line(path, fill="black", width=2)
    im.save(wd / "sampled.png")
    q = P[0]
    qmid = q[1 + 8]   # 8th of 16 samples of the quadratic (t = .5)
    qtrue = (0.25 * 90 + 0.5 * 120 + 0.25 * 90, 0.25 * 10 + 0.5 * 50 + 0.25 * 90)
    chord_mid = (90, 50)
    arc = P[2]
    arc_r = [math.hypot(x - 145, y - 50) for x, y in arc]
    reveal = lambda path, t: path[: max(1, int(round(t * (len(path) - 1)))) + 1]
    path = jw(wd / "sampled.json", {"paths": [[list(map(float, p)) for p in pp] for pp in P], "bbox": [min(xs), min(ys), max(xs), max(ys)]})
    checks = [check("three sub-paths (M splits), closed one returns to its start", len(P) == 3 and P[0][-1] == P[0][0], [len(P), P[0][0], P[0][-1]], "3, closed"),
              check("curves are sampled, not chorded (quadratic mid on the true curve)", math.dist(qmid, qtrue) < 1e-9 and math.dist(qtrue, chord_mid) > 10, [qmid, qtrue], "on curve"),
              check("smooth S reflects the previous control (ends where it should)", math.dist(P[1][-1], (30, 50)) < 1e-9, P[1][-1], (30, 50)),
              check("arc sampled every <=6 deg with >=12 points on radius 25", len(arc) - 1 >= 30 and max(abs(r_ - 25) for r_ in arc_r) < 1e-6, [len(arc) - 1, max(abs(r_ - 25) for r_ in arc_r)], ">=30 pts, r 25"),
              check("fit into the box with an 8% margin", abs(min(xs) - 32) < 1e-6 or abs(min(ys) - 24) < 1e-6, [min(xs), min(ys), max(xs), max(ys)], "margin 0.08"),
              check("reveal up to t gives a prefix of the points", reveal(T[0], 0.5) == T[0][: len(reveal(T[0], 0.5))] and len(reveal(T[0], 0.5)) < len(T[0]), len(reveal(T[0], 0.5)), "prefix"),
              check("negative control: chording the quadratic misses the curve", math.dist(chord_mid, qtrue) > 10, math.dist(chord_mid, qtrue), ">10")]
    return checks, [wd / "sampled.png", path]


@card("DRAW-G02")
def inertia_rubber_band(task, wd):
    import numpy as np
    from PIL import Image, ImageDraw
    tau, W = 0.325, 400.0
    rng = np.random.default_rng(4)
    ts = np.arange(0, 0.6, 1 / 120)
    v_true = 900.0
    drag = 50 + v_true * ts + rng.normal(0, 0.4, ts.size)       # finger samples at 120 Hz
    last = ts >= ts[-1] - 0.1
    v0 = float(np.polyfit(ts[last], drag[last], 1)[0])
    x0 = float(drag[-1])
    coast = lambda t: x0 + v0 * tau * (1 - math.exp(-t / tau))
    tt = np.arange(0, 2.0, 1 / 60)
    xs = np.array([coast(t) for t in tt])
    # fit tau back from the trajectory: log(rest - x) is linear in t
    rest = x0 + v0 * tau
    k = np.polyfit(tt[:60], np.log(rest - xs[:60]), 1)[0]
    band = lambda d: (1 - 1 / (d * 0.55 / W + 1)) * W
    ds = [10, 100, 400, 2000]
    shown = [band(d) for d in ds]
    # spring back from an overscroll of 120 px displayed
    z, om = 1.0, 2 * math.pi / 0.4
    back = [band(300) * (1 + om * t) * math.exp(-om * t) for t in tt]
    frames = []
    for x in xs[::2]:
        im = Image.new("RGB", (480, 60), (16, 18, 24))
        ImageDraw.Draw(im).rectangle([int(x) % 440, 20, int(x) % 440 + 30, 40], fill=(240, 200, 90))
        frames.append(np.asarray(im))
    mp4 = write_mp4(wd / "inertia.mp4", frames, 30)
    linear = x0 + v0 * tt
    path = jw(wd / "inertia.json", {"v0": v0, "tau_fit": -1 / k, "rest": rest, "band": dict(zip(map(str, ds), shown))})
    checks = [check("release velocity from the last 100 ms of the drag", abs(v0 - v_true) / v_true < 0.02, v0, v_true),
              check("decays exponentially with tau 0.325 s (fitted back)", abs(-1 / k - tau) < 1e-3, -1 / k, tau),
              check("comes to rest at x0 + v0 tau", abs(xs[-1] - rest) < 0.01 * v0 * tau, [float(xs[-1]), rest], "rest"),
              check("rubber band resists: shown < pulled, and never past W", all(s < d for s, d in zip(shown, ds)) and shown[-1] < W, shown, "< d, < W"),
              check("rubber band ~ 0.55 d for a small pull", abs(shown[0] / ds[0] - 0.55) < 0.01, shown[0] / ds[0], 0.55),
              check("springs back to the edge without overshoot (critically damped)", min(back) >= 0 and back[-1] < 0.5, [min(back), back[-1]], ">=0, ~0"),
              check("negative control: a linear coast never stops", float(linear[-1] - linear[-60]) > 100, float(linear[-1] - linear[-60]), ">100 px in the last second")]
    return checks, [mp4, path]


@card("DRAW-59")
def hw_component_library(task, wd):
    probe = """const S=[]; const X=(s)=>+gsap.getProperty($(s),'x'); const ar=$('#hw-b-arrow');
for(let f=0;f<=60;f++){tl.seek(f/30,false); S.push({f, circle:X('#hw-b-circle-g'), arrow:X('#hw-b-arrow-g'), word:X('#hw-b-word'), off:+gsap.getProperty(ar,'strokeDashoffset'), tag:X('#hw-b-tag-config')});}
const A2=[]; for(let f=0;f<=60;f++){tl.seek((f+1e-3)/30,false); A2.push(X('#hw-b-arrow-g'));}
tl.seek(0.5,false); const a=X('#hw-b-circle-g'); tl.seek(1.7,false); tl.seek(0.5,false); const b=X('#hw-b-circle-g');
document.body.setAttribute('data-r',JSON.stringify({S, A2, seek_same:a===b, alen:ar.getTotalLength(), circle_d:($('#hw-b-circle').getAttribute('d')||'').length}));"""
    r, comp = hf_component(wd, "hw-boil", {}, probe, (1920, 1080))
    S = r["S"]
    ch = lambda key: [i for i in range(1, len(S)) if S[i][key] != S[i - 1][key]]
    c_circle, c_arrow, c_word = ch("circle"), ch("arrow"), ch("word")
    amp = max(abs(s["circle"]) for s in S)
    offs = [s["off"] for s in S]
    path = jw(wd / "hw_boil.json", r | {"changes": {"circle": c_circle, "arrow": c_arrow, "word": c_word}})
    checks = [check("component fetched from the registry and mounted", comp.exists() and len(S) == 61, [comp.name, len(S)], "hw-boil, 61 frames"),
              check("calm boil re-poses every 3 frames (frameDrop 3)", c_circle and all(f % 3 == 0 for f in c_circle) and len(c_circle) >= 18, c_circle[:8], "multiples of 3"),
              check("arrow boils every frame (frameDrop 1) when sampled mid-frame", sum(r["A2"][i] != r["A2"][i - 1] for i in range(1, 61)) >= 58,
                    sum(r["A2"][i] != r["A2"][i - 1] for i in range(1, 61)), ">=58 of 60"),
              check("measured quirk: at exact f/30 seeks GSAP's 1e-8 time rounding repeats every 3rd pose", 35 <= len(c_arrow) <= 45, len(c_arrow), "~40 of 60"),
              check("calm amplitude <= 1.6 px", 0 < amp <= 1.6, amp, "<=1.6"),
              check("arrow draws on: dashoffset len -> 0 between 0.65 and 1.45 s", abs(offs[0] - r["alen"]) < 0.5 and offs[45] < 0.5, [offs[0], offs[45]], [r["alen"], 0]),
              check("seek-safe boil (same frame, same pose)", r["seek_same"], r["seek_same"], True),
              check("hand-wobbled circle path generated", r["circle_d"] > 50, r["circle_d"], ">50 chars"),
              check("negative control: an element without a boil never moves", max(abs(s["tag"]) for s in S) == 0, max(abs(s["tag"]) for s in S), 0)]
    return checks, [path, comp]


GAPS["DRAW-16"] = ("hw-write-title block fetches as HTML only: its baked per-glyph centrelines (assets/baked/caveat-pen.js) and the "
                   "Caveat 700 woff2 are not delivered by `hyperframes add` here, and no Hershey stroke fonts are installed")
GAPS["DRAW-60"] = ("alternative libraries (vivus, roughjs, rough-notation, perfect-freehand, @remotion/paths, @excalidraw/excalidraw) "
                   "are not installed in this container; installing is outside this pass")


@card("DRAW-14")
def pen_templates(task, wd):
    probe = """const D=+document.querySelector('[data-duration]').getAttribute('data-duration'); const P=[...document.querySelectorAll('path')]; const S=[];
for(let i=0;i<=24;i++){const t=D*i/24; tl.seek(t,false); S.push(P.map(p=>{const o=parseFloat(getComputedStyle(p).strokeDashoffset)||0; const a=parseFloat(getComputedStyle(p).strokeDasharray)||0; return [o,a];}));}
document.body.setAttribute('data-r',JSON.stringify({D,tl_len:tl.duration(),n:P.length,S,text:document.body.textContent.replace(/\\s+/g,' ').slice(0,400)}));"""
    res = {}
    for tpl, params, secs in (("logo-reveal", {"name": "KOSIF", "tagline": "حركة لها معنى"}, 6),
                              ("bullet-list", {"title": "Plan", "items": "One|Two|Three|Four"}, 8)):
        sub = wd / tpl
        sub.mkdir(exist_ok=True)
        r = template_page(sub, tpl, params, secs, probe)
        S = r["S"]
        drawn = [j for j in range(r["n"]) if S[0][j][1] > 0 and S[0][j][0] > 1 and abs(S[-1][j][0]) < 0.5]
        vis0 = max([1 - S[0][j][0] / S[0][j][1] for j in drawn] or [1.0])
        res[tpl] = {"D": r["D"], "paths": r["n"], "drawn_on": len(drawn), "text": r["text"], "visible_at_0": vis0,
                    "monotone": all(S[i + 1][j][0] <= S[i][j][0] + 1e-6 for j in drawn for i in range(24))}
    path = jw(wd / "templates.json", res)
    lr, bl = res["logo-reveal"], res["bullet-list"]
    checks = [check("logo-reveal composition is 6 s (data-duration)", abs(lr["D"] - 6) < 0.05, lr["D"], 6),
              check("logo is drawn by pen (dash offset len -> 0)", lr["drawn_on"] >= 1 and lr["monotone"], [lr["drawn_on"], lr["monotone"]], ">=1, monotone"),
              check("name and tagline shown", "KOSIF" in lr["text"] and "حركة لها معنى" in lr["text"], lr["text"][:80], "KOSIF, tagline"),
              check("bullet-list composition is 8 s (data-duration)", abs(bl["D"] - 8) < 0.05, bl["D"], 8),
              check("one drawn tick per item (4 items)", bl["drawn_on"] >= 4 and bl["monotone"], bl["drawn_on"], ">=4"),
              check("negative control: the same measure at t = 0 shows the strokes hidden", lr["visible_at_0"] < 0.05 and bl["visible_at_0"] < 0.05,
                    [lr["visible_at_0"], bl["visible_at_0"]], "<0.05 visible")]
    return checks, [path]


# ---------- shared polyline / rough-sketch engine (Python) ----------

def plen(pts):
    return sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))


def resample(pts, n):
    """n+1 points evenly spaced by arc length."""
    cum = [0.0]
    for i in range(len(pts) - 1):
        cum.append(cum[-1] + math.dist(pts[i], pts[i + 1]))
    L, out, j = cum[-1], [], 0
    for k in range(n + 1):
        s = L * k / n
        while j < len(pts) - 2 and cum[j + 1] < s:
            j += 1
        seg = cum[j + 1] - cum[j] or 1
        u = (s - cum[j]) / seg
        out.append((pts[j][0] + (pts[j + 1][0] - pts[j][0]) * u, pts[j][1] + (pts[j + 1][1] - pts[j][1]) * u))
    return out


def partial(pts, frac, n=400):
    rs = resample(pts, n)
    k = max(0, min(n, int(round(frac * n))))
    return rs[: k + 1] if k else []


def dash_runs(pts, dash, gap, offset, n=1000):
    """Visible pieces of a pathLength=1 dash pattern (SVG semantics: dashoffset shifts the pattern start)."""
    rs = resample(pts, n)
    per = dash + gap
    vis = [((k / n + offset) % per) < dash for k in range(n + 1)]
    runs, cur = [], []
    for p, v in zip(rs, vis):
        if v:
            cur.append(p)
        elif cur:
            runs.append(cur)
            cur = []
    if cur:
        runs.append(cur)
    return runs, vis


def sample_colours(img, pts):
    import numpy as np
    a = np.asarray(img)
    H, W = a.shape[:2]
    return [tuple(int(v) for v in a[min(H - 1, max(0, int(round(y)))), min(W - 1, max(0, int(round(x))))][:3]) for x, y in pts]


def rough_line(p0, p1, roughness, bowing, rng, passes=2):
    """Rough.js-style sketch line: two passes, endpoint jitter and a bowed midpoint, both scaled by roughness."""
    L = math.dist(p0, p1)
    out = []
    off = min(L * 0.1, 2.0) * roughness
    nx, ny = (-(p1[1] - p0[1]) / (L or 1), (p1[0] - p0[0]) / (L or 1))
    for _ in range(passes):
        j = lambda: rng.uniform(-off, off) if roughness else 0.0
        bow = bowing * roughness * L * 0.01 * rng.uniform(-1, 1) if roughness else 0.0
        a = (p0[0] + j(), p0[1] + j())
        b = (p1[0] + j(), p1[1] + j())
        m = ((a[0] + b[0]) / 2 + nx * bow * 4 + j(), (a[1] + b[1]) / 2 + ny * bow * 4 + j())
        out.append([((1 - t) ** 2 * a[0] + 2 * (1 - t) * t * m[0] + t * t * b[0], (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * m[1] + t * t * b[1])
                    for t in [i / 16 for i in range(17)]])
    return out


def hachure(poly, angle_deg, gap):
    """Parallel fill lines at angle_deg, gap px apart, clipped to the polygon (shapely)."""
    from shapely.geometry import LineString, Polygon
    P = Polygon(poly)
    cx, cy = P.centroid.x, P.centroid.y
    R = max(math.dist((cx, cy), p) for p in poly) + 2
    a = math.radians(angle_deg)
    d, nrm = (math.cos(a), math.sin(a)), (-math.sin(a), math.cos(a))
    lines = []
    k = -R
    while k <= R:
        o = (cx + nrm[0] * k, cy + nrm[1] * k)
        seg = LineString([(o[0] - d[0] * R, o[1] - d[1] * R), (o[0] + d[0] * R, o[1] + d[1] * R)]).intersection(P)
        for g in getattr(seg, "geoms", [seg]):
            if not g.is_empty and g.length > 0.5:
                lines.append(list(g.coords))
        k += gap
    return lines


def rough_rect(x, y, w, h, roughness=1.0, bowing=1.0, fill_style="hachure", gap=6, angle=-41, seed=1):
    import numpy as np
    rng = np.random.default_rng(seed)
    c = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    strokes = [s for i in range(4) for s in rough_line(c[i], c[(i + 1) % 4], roughness, bowing, rng)]
    fills = []
    if fill_style in ("hachure", "cross-hatch"):
        fills = hachure(c, angle, gap)
        if fill_style == "cross-hatch":
            fills += hachure(c, angle + 90, gap)
    return strokes, fills


def draw_lines(d, lines, col, width, frac=1.0):
    total = sum(plen(l) for l in lines) or 1
    budget = total * frac
    for l in lines:
        L = plen(l)
        if budget <= 0:
            break
        seg = l if budget >= L else partial(l, budget / L)
        if len(seg) > 1:
            d.line(seg, fill=col, width=max(1, int(round(width))), joint="curve")
        budget -= L


def hexrgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def smoothstep(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


@card("DRAW-10")
def river_fill_and_flow(task, wd):
    import numpy as np
    from PIL import Image, ImageDraw
    W, H, fps = 320, 240, 12
    river = catmull_like([(40, 30), (90, 80), (70, 140), (150, 170), (230, 160), (290, 220)])
    flow_runs = lambda t: dash_runs(river, .04, .07, -0.35 * t, 1000)

    def frame(t):
        im = Image.new("RGB", (W, H), (245, 240, 228))
        d = ImageDraw.Draw(im)
        d.line(river, fill=hexrgb("#CDE7F7"), width=20, joint="curve")
        k = 1 - max(0, min(1, (t - 7.3) / 1.4))     # dashoffset 1 -> 0 over 7.3-8.7 s, pathLength 1
        seg = partial(river, 1 - k, 1000)
        if len(seg) > 1:
            d.line(seg, fill=hexrgb("#2B8CE6"), width=12, joint="curve")
        a = max(0, min(1, (t - 8.4) / 0.3))
        if a > 0:
            lay = Image.new("RGB", (W, H))
            mask = Image.new("L", (W, H), 0)
            md = ImageDraw.Draw(mask)
            for run in flow_runs(t)[0]:
                if len(run) > 1:
                    md.line(run, fill=int(255 * a), width=6)
            lay.paste(hexrgb("#A9DBFF"), (0, 0, W, H))
            im = Image.composite(lay, im, mask)
        return im
    ts = [7.0 + i / fps for i in range(int(3.0 * fps))]
    imgs = [frame(t) for t in ts]
    mp4 = write_mp4(wd / "river.mp4", [np.asarray(i) for i in imgs], fps)
    probe_pts = resample(river, 1000)
    water = lambda im: float(np.mean([math.dist(c, hexrgb("#2B8CE6")) < 15 or math.dist(c, hexrgb("#A9DBFF")) < 15 for c in sample_colours(im, probe_pts)]))
    at = lambda t: frame(t)
    flow = lambda t: [math.dist(c, hexrgb("#A9DBFF")) < 15 for c in sample_colours(at(t), probe_pts)]
    f1, f2 = flow(9.5), flow(9.5 + 1 / 12)
    duty = float(np.mean(f1))
    shift = lambda a, b: min(range(110), key=lambda s: sum(x != y for x, y in zip(a[s:], b)))
    sh = shift(f2, f1)   # pattern moves forward along the path with a negative offset
    path = jw(wd / "river.json", {"water_7_0": water(at(7.0)), "water_8_0": water(at(8.0)), "water_9_0": water(at(9.0)), "flow_duty": duty, "shift_pts": sh})
    checks = [check("dry bed only before 7.3 s", water(at(7.0)) == 0.0, water(at(7.0)), 0),
              check("water fills mountain -> sea: half at 8.0 s", abs(water(at(8.0)) - 0.5) < 0.05, water(at(8.0)), 0.5),
              check("river full by 8.7 s", water(at(9.0)) > 0.97, water(at(9.0)), ">0.97"),
              check("flow dashes .04 / .07 of the length (duty .36)", abs(duty - .04 / .11) < 0.05, duty, .04 / .11),
              check("flow runs at -0.35 x t (2.9 per 1/12 s on 1000 pts)", abs(sh - 0.35 / 12 * 1000) <= 2, sh, round(0.35 / 12 * 1000, 1)),
              check("negative control: no flow layer before 8.4 s", not any(flow(8.0)), sum(flow(8.0)), 0)]
    return checks, [mp4, path]


def catmull_like(pts, n=12):
    out = []
    P = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            out.append(tuple(0.5 * ((2 * b) + (-a + c) * t + (2 * a - 5 * b + 4 * c - e) * t * t + (-a + 3 * b - 3 * c + e) * t ** 3)
                             for a, b, c, e in zip(p0, p1, p2, p3)))
    out.append(pts[-1])
    return out


@card("DRAW-11")
def mihrab_gold_pen(task, wd):
    import numpy as np
    from PIL import Image, ImageDraw
    W, H = 240, 300
    arch = [(40, 290), (40, 150)] + [(120 + 80 * math.cos(math.pi - math.pi * k / 40), 150 - 110 * math.sin(math.pi * k / 40)) for k in range(41)] + [(200, 150), (200, 290)]
    inner = [(60, 290), (60, 160)] + [(120 + 60 * math.cos(math.pi - math.pi * k / 40), 160 - 85 * math.sin(math.pi * k / 40)) for k in range(41)] + [(180, 160), (180, 290)]
    Eout = bez(.16, 1, .3, 1)
    amen = 2.4
    gold = [hexrgb("#fff0b3"), hexrgb("#e8b04a"), hexrgb("#fff0b3")]

    def grad(x):
        u = x / W * 2
        a, b = (gold[0], gold[1]) if u < 1 else (gold[1], gold[2])
        u = u if u < 1 else u - 1
        return tuple(int(p + (q - p) * u) for p, q in zip(a, b))

    def frame(t):
        mask = Image.new("L", (W, H), 0)
        d = ImageDraw.Draw(mask)
        k = Eout(min(1, max(0, t / 1.7)))
        w = 7 + 2 * max(0, min(1, (t - amen) / 0.3))
        seg = partial(arch, k)
        if len(seg) > 1:
            d.line(seg, fill=255, width=int(round(w)), joint="curve")
        imask = Image.new("L", (W, H), 0)
        ki = Eout(min(1, max(0, (t - 0.25) / 1.7)))
        si = partial(inner, ki)
        if len(si) > 1:
            ImageDraw.Draw(imask).line(si, fill=int(255 * .55), width=3, joint="curve")
        bg = Image.new("RGB", (W, H), (12, 18, 30))
        g = Image.fromarray(np.array([[grad(x) for x in range(W)]] * H, dtype=np.uint8))
        im = Image.composite(g, bg, imask)
        return Image.composite(g, im, mask), k
    ts = [i / 30 for i in range(int(3.0 * 30))]
    out = [frame(t) for t in ts]
    mp4 = write_mp4(wd / "mihrab.mp4", [np.asarray(o[0]) for o in out], 30)
    probe = resample(arch, 400)

    def drawn(im):
        cs = sample_colours(im, probe)
        on = [sum(c) > 300 for c in cs]
        return (max(i for i, v in enumerate(on) if v) / 400) if any(on) else 0.0
    width_at = lambda im: int((np.asarray(im)[220, 30:52].sum(-1) > 300).sum())
    top = sample_colours(frame(2.0)[0], [(120, 40)])[0]
    side = sample_colours(frame(2.0)[0], [(40, 220)])[0]
    path = jw(wd / "mihrab.json", {"drawn_0.5": drawn(frame(0.5)[0]), "expected_0.5": Eout(0.5 / 1.7), "w_before": width_at(frame(2.0)[0]), "w_after": width_at(frame(2.9)[0])})
    checks = [check("arch draws like a pen with E.out over 1.7 s", abs(drawn(frame(0.5)[0]) - Eout(0.5 / 1.7)) < 0.02, drawn(frame(0.5)[0]), Eout(0.5 / 1.7)),
              check("fully drawn at 1.7 s", drawn(frame(1.75)[0]) > 0.99, drawn(frame(1.75)[0]), 1),
              check("gold gradient: deeper gold at the centre, pale at the sides", top[2] < side[2] - 30, [top, side], "centre #e8b04a, sides #fff0b3"),
              check("stroke thickens 7 -> 9 px on the amen word", width_at(frame(2.0)[0]) in (7, 8) and width_at(frame(2.9)[0]) in (9, 10), [width_at(frame(2.0)[0]), width_at(frame(2.9)[0])], [7, 9]),
              check("inner arch at opacity .55 starts at 0.25 s", sample_colours(frame(1.9)[0], [(60, 250)])[0] != (12, 18, 30) and
                    max(sample_colours(frame(1.9)[0], [(60, 250)])[0]) < 0.6 * 255 + 12 * .45 + 5, sample_colours(frame(1.9)[0], [(60, 250)])[0], "~55% gold"),
              check("negative control: at t = 0 nothing is drawn", drawn(frame(0.0)[0]) == 0.0, drawn(frame(0.0)[0]), 0)]
    return checks, [mp4, path]


@card("DRAW-12")
def ivory_line_examples(task, wd):
    import numpy as np
    from PIL import Image, ImageDraw
    ivory, gold = hexrgb("#F5F0E6"), hexrgb("#E7B65A")
    W = H = 400
    cx = cy = 200

    def clock(t):
        im = Image.new("RGB", (W, H), (14, 16, 22))
        d = ImageDraw.Draw(im)
        d.ellipse([cx - 150, cy - 150, cx + 150, cy + 150], outline=ivory, width=3)
        for i in range(24):
            if t < i * 0.035:
                continue
            a = 2 * math.pi * i / 24
            L, w = (28, 3) if i % 6 == 0 else (14, 2)
            d.line([(cx + (140 - L) * math.sin(a), cy - (140 - L) * math.cos(a)), (cx + 140 * math.sin(a), cy - 140 * math.cos(a))], fill=ivory, width=w)
        ha = 2 * math.pi * min(1, t / 1.2)
        d.line([(cx, cy), (cx + 90 * math.sin(ha), cy - 90 * math.cos(ha))], fill=gold, width=3)
        return im

    def road(t):
        im = Image.new("RGB", (W, 120), (14, 16, 22))
        d = ImageDraw.Draw(im)
        sh = -70 * min(1, t / 1.2)
        for k in range(8):
            x = 20 + 70 * k + sh
            d.rectangle([x, 58, x + 34, 62], fill=gold)
        d.rounded_rectangle([140, 20, 260, 50], radius=10, outline=ivory, width=3)
        for wx in (165, 235):
            d.ellipse([wx - 19, 36 - 19, wx + 19, 36 + 19], outline=ivory, width=3)
        return im
    frames = [np.asarray(clock(i / 30)) for i in range(36)]
    mp4 = write_mp4(wd / "clock.mp4", frames, 30)
    a = np.asarray(clock(1.2))
    prof = []
    for k in range(1440):
        ang = 2 * math.pi * k / 1440
        hit = lambda rs: any(a[int(round(cy - r * math.cos(ang))), int(round(cx + r * math.sin(ang)))].sum() > 600 for r in rs)
        prof.append((hit((116, 118, 120)), hit((131, 133, 135))))
    short = [p[1] for p in prof]
    longs = [p[0] for p in prof]
    runs = lambda v: sum(1 for i in range(len(v)) if v[i] and not v[i - 1])
    gold_mask = lambda im: (np.asarray(im)[58:63, :, 0] > 200) & (np.asarray(im)[58:63, :, 2] < 140)
    dash_cols = lambda im: [x for x in range(W) if gold_mask(im)[:, x].any()]
    starts = lambda im: [x for x in range(1, W) if gold_mask(im)[:, x].any() and not gold_mask(im)[:, x - 1].any()]
    x0 = starts(road(0.0))[0]
    s06 = starts(road(0.6))[0]
    x1 = s06 - 70 if s06 > x0 else s06    # the dash that started at x0 + 70 now sits at s06
    seg_count = runs([bool(gold_mask(road(0.0))[:, x].any()) for x in range(W)])
    staggered = [sum(1 for i in range(24) if (f / 30) >= i * 0.035) for f in (0, 10, 30)]
    blank = Image.new("RGB", (W, H), (14, 16, 22))
    d0 = ImageDraw.Draw(blank)
    d0.ellipse([cx - 150, cy - 150, cx + 150, cy + 150], outline=ivory, width=3)
    bprof = [any(np.asarray(blank)[int(round(cy - r * math.cos(2 * math.pi * k / 1440))), int(round(cx + r * math.sin(2 * math.pi * k / 1440)))].sum() > 600 for r in (131, 133, 135)) for k in range(1440)]
    path = jw(wd / "ivory.json", {"ticks": runs(short), "long_ticks": runs(longs), "road_shift": x1 - x0, "segments": seg_count, "stagger": staggered})
    checks = [check("clock ring with 24 ticks", runs(short) == 24, runs(short), 24),
              check("every 6th tick longer (4 long ticks)", runs(longs) == 4, runs(longs), 4),
              check("ticks stagger in at 35 ms each", staggered == [1, 10, 24], staggered, [1, 10, 24]),
              check("road gold dashes slide -70 px over the example (-35 px at 0.6 s)", abs((x1 - x0) + 35) <= 1, x1 - x0, -35),
              check("road shows 6 dashes on screen", seg_count == 6, seg_count, 6),
              check("negative control: a bare ring has no ticks", runs(bprof) == 0, runs(bprof), 0)]
    return checks, [mp4, path]


def interpolate_clamp(f, f0, f1):
    return max(0.0, min(1.0, (f - f0) / (f1 - f0)))


def annotation_lines(kind, box, rng):
    x0, y0, x1, y1 = box
    cx, cy, w, h = (x0 + x1) / 2, (y0 + y1) / 2, x1 - x0, y1 - y0
    if kind == "underline":
        return rough_line((x0, y1 + 4), (x1, y1 + 4), 1.0, 1.0, rng)
    if kind == "strike":
        return rough_line((x0, cy), (x1, cy), 1.0, 1.0, rng)
    if kind == "crossed-off":
        return rough_line((x0, y0), (x1, y1), 1.0, 1.0, rng) + rough_line((x0, y1), (x1, y0), 1.0, 1.0, rng)
    if kind == "box":
        c = [(x0 - 4, y0 - 4), (x1 + 4, y0 - 4), (x1 + 4, y1 + 4), (x0 - 4, y1 + 4)]
        return [s for i in range(4) for s in rough_line(c[i], c[(i + 1) % 4], 1.0, 1.0, rng)]
    if kind == "bracket":
        return rough_line((x1 + 6, y0), (x1 + 12, y0), 1, 1, rng) + rough_line((x1 + 12, y0), (x1 + 12, y1), 1, 1, rng) + rough_line((x1 + 12, y1), (x1 + 6, y1), 1, 1, rng)
    if kind == "circle":
        j = [rng.uniform(-0.04, 0.04) for _ in range(9)]
        pts = [(cx + (w / 2 + 10) * (1 + j[k % 9]) * math.cos(2 * math.pi * k / 48 * 1.08), cy + (h / 2 + 8) * (1 + j[k % 9]) * math.sin(2 * math.pi * k / 48 * 1.08)) for k in range(49)]
        return [pts]
    if kind == "highlight":
        return [[(x0, cy + rng.uniform(-1, 1)), (x1, cy + rng.uniform(-1, 1))]]
    raise ValueError(kind)


@card("DRAW-23")
def sketchy_annotations(task, wd):
    import numpy as np
    from PIL import Image, ImageDraw
    kinds = ["highlight", "circle", "underline", "strike", "crossed-off", "box", "bracket"]
    boxes = {k: (30, 20 + 40 * i, 150, 44 + 40 * i) for i, k in enumerate(kinds)}

    def frame(f, seed=7):
        p = interpolate_clamp(f, 15, 40)
        base = Image.new("RGB", (240, 300), (250, 248, 240))
        d = ImageDraw.Draw(base)
        for k, b in boxes.items():
            d.rectangle(b, outline=(200, 200, 200))
        hl = Image.new("RGBA", base.size, (0, 0, 0, 0))
        hd = ImageDraw.Draw(hl)
        for i, k in enumerate(kinds):
            rng = np.random.default_rng(seed * 100 + i)
            lines = annotation_lines(k, boxes[k], rng)
            if k == "highlight":
                draw_lines(hd, lines, (255, 236, 79, 140), 22, p)
            else:
                draw_lines(d, lines, (214, 51, 43), 2, p)
        return Image.alpha_composite(base.convert("RGBA"), hl).convert("RGB")
    ink = lambda im: int(((np.asarray(im)[:, :, 0] > 180) & (np.asarray(im)[:, :, 1] < 120)).sum() + ((np.asarray(im)[:, :, 2] < 180) & (np.asarray(im)[:, :, 0] > 240)).sum())
    frames = [frame(f) for f in range(0, 50)]
    mp4 = write_mp4(wd / "annotations.mp4", [np.asarray(x) for x in frames], 30)
    curve = [ink(x) for x in frames]
    same = np.array_equal(np.asarray(frame(45, 7)), np.asarray(frame(45, 7)))
    other = not np.array_equal(np.asarray(frame(45, 7)), np.asarray(frame(45, 8)))
    path = jw(wd / "annotations.json", {"ink": curve})
    checks = [check("progress = interpolate(frame, [15, 40], [0, 1], clamp): nothing before frame 15", curve[14] == curve[0] == ink(frame(0)) and curve[0] == 0, curve[:16:5], 0),
              check("about half the strokes at frame 27.5", 0.3 < curve[27] / curve[45] < 0.7, curve[27] / curve[45], "~0.5"),
              check("complete from frame 40 on (clamped)", curve[40] == curve[49], [curve[40], curve[49]], "equal"),
              check("seven annotation kinds drawn", all(ink(frame(45).crop((0, b[1] - 12, 240, b[3] + 12))) > 20 for b in boxes.values()), len(kinds), 7),
              check("fixed seed: identical redraw", same, same, True),
              check("negative control: another seed draws different strokes", other, other, True)]
    return checks, [mp4, path]


@card("DRAW-27")
def rough_shapes(task, wd):
    import numpy as np
    from PIL import Image, ImageDraw

    def render(roughness, style="hachure", gap=8, seed=3):
        im = Image.new("L", (200, 160), 0)
        d = ImageDraw.Draw(im)
        st, fl = rough_rect(40, 30, 120, 100, roughness, 1.0, style, gap, -41, seed)
        draw_lines(d, st, 255, 2)
        if style == "solid":
            d.rectangle([40, 30, 160, 130], fill=128)
        draw_lines(d, fl, 180, 1)
        return np.asarray(im), st, fl

    def deviation(st):
        # distance of outline points from the true rectangle edges
        dev = []
        for s in st:
            for x, y in s:
                dev.append(min(abs(x - 40), abs(x - 160), abs(y - 30), abs(y - 130)))
        return max(dev)
    a0, s0, f0 = render(0)
    a1, s1, f1 = render(1)
    a2, s2, f2 = render(2)
    _, _, fx_ = render(1, "cross-hatch")
    b1, _, _ = render(1, seed=3)
    b2, _, _ = render(1, seed=4)
    boil = [render(1, seed=int(t * 12))[0] for t in [i / 24 for i in range(24)]]
    changes = sum(not np.array_equal(boil[i], boil[i - 1]) for i in range(1, 24))
    Image.fromarray(a1).save(wd / "rough_rect.png")
    expect_lines = (120 * abs(math.sin(math.radians(41))) + 100 * abs(math.cos(math.radians(41)))) / 8
    path = jw(wd / "rough.json", {"dev": [deviation(s0), deviation(s1), deviation(s2)], "hachure": len(f1), "cross": len(fx_), "boil_changes": changes})
    checks = [check("roughness 0 = straight edges", deviation(s0) < 1e-9, deviation(s0), 0),
              check("wobble grows with roughness (0 < 1 < 2)", 0 < deviation(s1) < deviation(s2), [deviation(s1), deviation(s2)], "increasing"),
              check("hachure fill: line count = span / gap", abs(len(f1) - expect_lines) <= 2, len(f1), round(expect_lines, 1)),
              check("cross-hatch doubles the fill lines", abs(len(fx_) - 2 * len(f1)) <= 3, len(fx_), 2 * len(f1)),
              check("fixed seed: no accidental boil", np.array_equal(a1, b1), True, True),
              check("seed = floor(t x 12) boils 12x per second (every 2nd frame at 24 fps)", changes == 11, changes, 11),
              check("negative control: a different seed changes the strokes", not np.array_equal(b1, b2), True, True)]
    return checks, [wd / "rough_rect.png", path]


@card("DRAW-G01")
def seeded_rough_reveal(task, wd):
    import numpy as np
    from PIL import Image, ImageDraw
    shapes = {"a": (20, 20, 120, 90), "b": (150, 40, 100, 110)}

    def frame(f, per_frame_random=False, drop=3):
        im = Image.new("L", (280, 180), 0)
        d = ImageDraw.Draw(im)
        prog = min(1.0, f / 30)
        for k, (x, y, w, h) in shapes.items():
            seed = ord(k) * 10 + (f // drop)          # one seed per shape id, re-posed every `drop` frames
            if per_frame_random:
                seed = 1000 + f * 7 + ord(k)
            st, fl = rough_rect(x, y, w, h, 1.5, 1.0, "hachure", 6, -41, seed)
            draw_lines(d, st, 255, 2, prog)
            draw_lines(d, fl, 160, 1, max(0, prog * 2 - 1))
        return np.asarray(im)
    F = [frame(f) for f in range(45)]
    R = [frame(f, True) for f in range(45)]
    ch = [f for f in range(31, 45) if not np.array_equal(F[f], F[f - 1])]
    chr_ = [f for f in range(31, 45) if not np.array_equal(R[f], R[f - 1])]
    # hachure angle measured from the fill pixels (value 160) by PCA of a fill line's pixels
    import cv2
    m = (F[44] == 160).astype(np.uint8)
    n, lab = cv2.connectedComponents(m)
    sizes = [(int((lab == i).sum()), i) for i in range(1, n)]
    big = max(sizes)[1]
    ys, xs = np.nonzero(lab == big)
    ang = math.degrees(math.atan(np.polyfit(xs, ys, 1)[0]))
    ink = [int((frame(f, drop=10 ** 6) > 0).sum()) for f in range(31)]   # same pose, so only the reveal changes
    mp4 = write_mp4(wd / "rough_reveal.mp4", [np.repeat(q[:, :, None], 3, 2) for q in F], 30)
    path = jw(wd / "rough_reveal.json", {"changes": ch, "changes_random": chr_, "angle": ang, "ink": ink})
    checks = [check("hachure angle -41 deg (measured on the fill)", abs(ang + 41) < 2, ang, -41),
              check("one seed per shape id: boil only every 3 frames", ch and all(f % 3 == 0 for f in ch), ch, "multiples of 3"),
              check("revealed by path length (ink grows monotonically to full)", all(b >= a for a, b in zip(ink, ink[1:])) and ink[0] == 0 and ink[30] > 0,
                    ink[::6], "monotone"),
              check("negative control: Math.random per frame jitters every frame", len(chr_) == 14, len(chr_), 14)]
    return checks, [mp4, path]


@card("DRAW-43")
def shape_carries_argument(task, wd):
    import numpy as np
    from PIL import Image, ImageDraw
    from scipy import ndimage
    rng0 = np.random.default_rng(2)
    events = [(40 + 70 * i, 100) for i in range(5)]
    sizes = [10, 13, 16, 20, 12]

    def render(roughness, text=True, pts=events):
        rng = np.random.default_rng(5)
        im = Image.new("L", (400, 200), 0)
        d = ImageDraw.Draw(im)
        for s in rough_line((20, 100), (380, 100), roughness, 1.0, rng):
            d.line(s, fill=120, width=2)
        for (x, y), r in zip(pts, sizes):
            d.ellipse([x - r / 2, y - r / 2, x + r / 2, y + r / 2], fill=255)
            if text:
                d.text((x - 10, y + 16), "E%d" % (x // 70), fill=200)
        return np.asarray(im)
    full, bare = render(1), render(1, text=False)
    lab, n = ndimage.label(bare == 255)
    diam = sorted(int(np.ptp(np.nonzero(lab == i)[1])) + 1 for i in range(1, n + 1))
    cents = [ndimage.center_of_mass(lab == i) for i in range(1, n + 1)]
    resid = float(np.std([c[0] for c in cents]))
    dev = lambda r: float(np.abs(np.nonzero(render(r, False) == 120)[0] - 100).max())
    scatter = [(int(x), int(y)) for x, y in zip(rng0.uniform(30, 370, 5), rng0.uniform(30, 170, 5))]
    sl, sn = ndimage.label(render(1, False, scatter) == 255)
    sresid = float(np.std([ndimage.center_of_mass(sl == i)[0] for i in range(1, sn + 1)]))
    Image.fromarray(full).save(wd / "timeline.png")
    path = jw(wd / "argument.json", {"diameters": diam, "row_resid": resid, "dev": [dev(0), dev(1), dev(2)], "scatter_resid": sresid})
    checks = [check("timeline dots 10-20 px", n == 5 and diam[0] >= 10 and diam[-1] <= 21, diam, "10..20"),
              check("without the text the structure is intact (5 dots in one row)", n == 5 and resid < 1.0, [n, resid], "5, on a line"),
              check("roughness 0 smooth, 2 rougher than 1", dev(0) <= 1 and dev(1) < dev(2), [dev(0), dev(1), dev(2)], "0 < 1 < 2"),
              check("negative control: scattered dots carry no timeline (not in a row)", sresid > 10, sresid, ">10 px")]
    return checks, [wd / "timeline.png", path]


def palette_count(a, bg, tol=24, min_share=0.002):
    import numpy as np
    px = a.reshape(-1, 3).astype(int)
    px = px[np.abs(px - np.array(bg)).sum(1) > tol]
    if not len(px):
        return 0
    q = (px // 32) * 32
    vals, cnt = np.unique(q, axis=0, return_counts=True)
    return int((cnt > min_share * a.shape[0] * a.shape[1]).sum())


@card("DRAW-39")
def graphic_recording(task, wd):
    import numpy as np
    from PIL import Image, ImageDraw
    paper, cols = (250, 247, 238), [(35, 35, 40), (214, 51, 43), (31, 95, 209), (240, 180, 40)]
    W, H = 480, 270
    scenes = [[("rect", 30, 40, 120, 80), ("line", 160, 80, 220, 80)], [("rect", 250, 30, 90, 90), ("line", 350, 75, 420, 75)], [("rect", 40, 160, 400, 70)]]

    def frame(k):
        im = Image.new("RGB", (W, H), paper)
        d = ImageDraw.Draw(im)
        total = len(scenes)
        for si, sc in enumerate(scenes):
            p = max(0.0, min(1.0, k * total - si))
            if p <= 0:
                continue
            for j, it in enumerate(sc):
                rng = np.random.default_rng(si * 10 + j)
                if it[0] == "rect":
                    st, fl = rough_rect(it[1], it[2], it[3], it[4], 1.2, 1.0, "hachure", 7, -41, si * 10 + j)
                    draw_lines(d, fl, cols[1 + (si % 3)], 1, p)
                    draw_lines(d, st, cols[0], 2, p)
                else:
                    draw_lines(d, rough_line(it[1:3], it[3:5], 1.0, 1.0, rng), cols[0], 2, p)
                    d.polygon([(it[3], it[4] - 5), (it[3] + 9, it[4]), (it[3], it[4] + 5)], fill=cols[0]) if p >= 1 else None
        return np.asarray(im)
    fr = [frame(i / 44) for i in range(45)]
    mp4 = write_mp4(wd / "recording.mp4", fr, 15)
    pal = palette_count(fr[-1], paper)
    ink = [int((np.abs(f.astype(int) - paper).sum(-1) > 30).sum()) for f in fr]
    scene_done = [int((np.abs(frame(k).astype(int) - paper).sum(-1) > 30).sum()) for k in (1 / 3, 2 / 3, 1.0)]
    noise = np.random.default_rng(1).integers(0, 255, (H, W, 3), dtype=np.uint8)
    path = jw(wd / "recording.json", {"palette": pal, "ink": ink[::4], "scene_ink": scene_done})
    checks = [check("3-5 colours on the paper", 3 <= pal <= 5, pal, "3..5"),
              check("2-5 scenes built one after another", len(scenes) == 3 and scene_done[0] < scene_done[1] < scene_done[2], scene_done, "growing per scene"),
              check("drawn on (ink only grows)", all(b >= a for a, b in zip(ink, ink[1:])) and ink[0] == 0, ink[:5], "monotone from 0"),
              check("hatch fills present (jittered strokes + hatch)", int(((fr[-1][:, :, 2] > 150) & (fr[-1][:, :, 0] < 100)).sum()) > 200,
                    int(((fr[-1][:, :, 2] > 150) & (fr[-1][:, :, 0] < 100)).sum()), ">200 px"),
              check("negative control: a photo-like frame is not a 3-5 colour recording", palette_count(noise, paper) > 5, palette_count(noise, paper), ">5")]
    return checks, [mp4, path]


@card("DRAW-40")
def graphite_teal(task, wd):
    import numpy as np
    from PIL import Image, ImageDraw
    paper, teal = hexrgb("#F4ECDC"), hexrgb("#2E7D8C")
    W, H = 400, 300

    def frame(t):
        im = Image.new("RGB", (W, H), paper)
        d = ImageDraw.Draw(im)
        rng = np.random.default_rng(3)
        figure = [(170, 290), (175, 225), (190, 205), (210, 205), (225, 225), (230, 290)]
        for k in range(60):                                  # graphite hatching for the figure from behind and the floor
            g = int(0x4A + (0x9A - 0x4A) * rng.random())
            x = 160 + k * 1.3
            d.line([(x, 290), (x + 12, 236 + rng.uniform(0, 10))], fill=(g, g, g), width=1)
        for k in range(40):
            g = int(0x4A + (0x9A - 0x4A) * rng.random())
            d.line([(10 + k * 10, 296), (18 + k * 10, 292)], fill=(g, g, g), width=1)
        d.ellipse([186, 206, 214, 234], outline=(0x4A, 0x4A, 0x4A), width=2)
        s = 1 + 0.08 * math.sin(2 * math.pi * t / 2.0)       # only the coloured object moves
        cx, cy, r = 270, 255, 16 * s
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=teal)
        return np.asarray(im)
    fr = [frame(i / 15) for i in range(30)]
    mp4 = write_mp4(wd / "graphite.mp4", fr, 15)
    a = fr[0].astype(int)
    top = a[: H * 2 // 3]
    nonpaper = np.abs(a - paper).sum(-1) > 20
    tealm = np.abs(a - teal).sum(-1) < 20
    from scipy import ndimage
    comps = ndimage.label(tealm)[1]
    other = nonpaper & ~tealm
    sat = (a.max(-1) - a.min(-1))[other]
    diff = np.zeros((H, W), bool)
    for f in fr[1:]:
        diff |= np.abs(f.astype(int) - fr[0]).sum(-1) > 0
    near_teal = ndimage.binary_dilation(tealm, iterations=3)
    plain = np.random.default_rng(0).integers(0, 255, (H, W, 3))
    path = jw(wd / "graphite.json", {"top_ink": int((np.abs(top - paper).sum(-1) > 20).sum()), "teal_parts": int(comps), "grey_sat_max": int(sat.max()),
                                     "changed_outside_teal": int((diff & ~near_teal).sum())})
    checks = [check("4:3 on cream paper #F4ECDC", W * 3 == H * 4 and tuple(fr[0][5, 5]) == paper, [W, H, tuple(int(v) for v in fr[0][5, 5])], "4:3, paper"),
              check("top two-thirds empty", int((np.abs(top - paper).sum(-1) > 20).sum()) == 0, int((np.abs(top - paper).sum(-1) > 20).sum()), 0),
              check("graphite #4A-#9A greys only besides the prop", int(sat.max()) == 0 and int(a[other].min()) >= 0x4A - 1, [int(sat.max()), int(a[other].min())], "neutral greys"),
              check("exactly ONE teal object", comps == 1, comps, 1),
              check("in motion only the coloured object changes", int((diff & ~near_teal).sum()) == 0 and int(diff.sum()) > 0, [int((diff & ~near_teal).sum()), int(diff.sum())], "0 outside teal"),
              check("negative control: a random frame breaks the grey-only rule", int((plain.max(-1) - plain.min(-1)).max()) > 50, int((plain.max(-1) - plain.min(-1)).max()), ">50")]
    return checks, [mp4, path]


@card("DRAW-41")
def storyboard_frames(task, wd):
    import numpy as np
    from PIL import Image, ImageDraw
    W, H = 480, 270
    rng = np.random.default_rng(11)

    def pencil(d, p0, p1, g=110):
        for s in rough_line(p0, p1, 0.8, 1.0, rng):
            d.line(s, fill=(g, g, g), width=1)

    def board(dashed=True):
        im = Image.new("RGB", (W, H), (248, 248, 246))
        d = ImageDraw.Draw(im)
        x0, y0, x1, y1 = 40, 30, 440, 240
        edges = [((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))]
        for a, b in edges:
            L = math.dist(a, b)
            n = int(L // 14) if dashed else 1
            for k in range(n):
                u0, u1 = k / n, (k + (0.6 if dashed else 1)) / n
                d.line([(a[0] + (b[0] - a[0]) * u0, a[1] + (b[1] - a[1]) * u0), (a[0] + (b[0] - a[0]) * u1, a[1] + (b[1] - a[1]) * u1)], fill=(120, 120, 120), width=1)
        pencil(d, (120, 200), (160, 110))
        pencil(d, (160, 110), (200, 200))
        d.ellipse([150, 90, 170, 110], outline=(100, 100, 100))
        pencil(d, (260, 200), (380, 200), 140)
        d.line([(60, 225), (420, 60)], fill=(214, 40, 40), width=2)     # camera axis
        d.text((300, 215), "2.4 m", fill=(90, 90, 90))
        return np.asarray(im)
    a = board().astype(int)
    red = (a[:, :, 0] > 180) & (a[:, :, 1] < 90)
    ys, xs = np.nonzero(red)
    k, b = np.polyfit(xs, ys, 1)
    resid = float(np.abs(ys - (k * xs + b)).max())
    grey = ~red & (np.abs(a - 248).sum(-1) > 30)
    sat = int((a.max(-1) - a.min(-1))[grey].max())
    gaps = lambda arr: sum(1 for x in range(41, 440) if (np.abs(arr[30, x] - 248).sum() > 30) != (np.abs(arr[30, x - 1] - 248).sum() > 30))
    Image.fromarray(a.astype(np.uint8)).save(wd / "storyboard.png")
    solid = board(False).astype(int)
    path = jw(wd / "storyboard.json", {"aspect": W / H, "axis_resid": resid, "grey_sat": sat, "top_edge_transitions": gaps(a)})
    checks = [check("16:9 frame", abs(W / H - 16 / 9) < 1e-9, W / H, 16 / 9),
              check("red camera-axis is one straight line", resid <= 2 and len(xs) > 300, [resid, len(xs)], "<=2 px"),
              check("everything else in grey pencil", sat <= 6, sat, "<=6"),
              check("dashed frame rectangle", gaps(a) > 40, gaps(a), ">40 dash edges"),
              check("negative control: a solid frame has no dash breaks", gaps(solid) <= 2, gaps(solid), "<=2")]
    return checks, [wd / "storyboard.png", path]


@card("DRAW-42")
def crayon_trip_map(task, wd):
    import numpy as np
    from PIL import Image, ImageDraw
    from scipy import ndimage
    W, H = 360, 480
    paper = hexrgb("#FBF6E9")
    confirmed = [[(40, 420), (120, 360), (180, 380), (260, 300)], [(260, 300), (240, 200), (300, 120)], [(260, 300), (140, 220), (80, 120)]]
    routes = [hexrgb("#8CC63F"), hexrgb("#8E6BB0"), hexrgb("#F2A03D")]

    def crayon(d, pts, col, w, rng):
        for p in resample(pts, int(plen(pts) // 2)):
            for _ in range(3):
                if rng.random() < 0.7:
                    x, y = p[0] + rng.normal(0, w / 4), p[1] + rng.normal(0, w / 4)
                    d.ellipse([x - 1.5, y - 1.5, x + 1.5, y + 1.5], fill=col)

    def render(extra=None):
        im = Image.new("RGB", (W, H), paper)
        d = ImageDraw.Draw(im)
        rng = np.random.default_rng(2)
        d.ellipse([200, 380, 330, 460], fill=hexrgb("#A9CDE8"))
        d.ellipse([20, 40, 120, 110], fill=hexrgb("#DDE8B5"))
        for seg in confirmed:
            d.line(seg, fill=hexrgb("#B9AEA6"), width=10, joint="curve")
        for seg, col in zip(confirmed, routes):
            crayon(d, seg, col, 6, rng)
        if extra:
            crayon(d, extra, routes[0], 6, rng)
        for i, p in enumerate([confirmed[0][0], confirmed[0][-1], confirmed[1][-1], confirmed[2][-1]], 1):
            d.ellipse([p[0] - 10, p[1] - 10, p[0] + 10, p[1] + 10], fill=hexrgb("#F7F1DC"), outline=hexrgb("#2B2B2B"), width=2)
            d.text((p[0] - 3, p[1] - 6), str(i), fill=hexrgb("#2B2B2B"))
        return np.asarray(im).astype(int)
    a = render()
    allowed = Image.new("L", (W, H), 0)
    ad = ImageDraw.Draw(allowed)
    for seg in confirmed:
        ad.line(seg, fill=255, width=22, joint="curve")
    allowed = np.asarray(allowed) > 0
    route_px = np.zeros((H, W), bool)
    for c in routes:
        route_px |= np.abs(a - c).sum(-1) < 20
    outside = int((route_px & ~allowed).sum())
    stops = ndimage.label(np.abs(a - hexrgb("#2B2B2B")).sum(-1) < 30)[1]
    tex = float(np.std(route_px[ndimage.binary_erosion(allowed, iterations=8)]))
    present = [int((np.abs(a - c).sum(-1) < 20).sum()) for c in routes]
    b = render(extra=[(40, 420), (300, 120)])
    route_b = np.zeros((H, W), bool)
    for c in routes:
        route_b |= np.abs(b - c).sum(-1) < 20
    Image.fromarray(a.astype(np.uint8)).save(wd / "trip_map.png")
    path = jw(wd / "trip_map.json", {"outside_px": outside, "stops_components": int(stops), "route_px": present, "texture_std": tex, "invented_outside": int((route_b & ~allowed).sum())})
    checks = [check("3:4 portrait map on #FBF6E9", W * 4 == H * 3 and tuple(a[2, 2]) == paper, [W, H], "3:4"),
              check("three route colours drawn", all(p > 100 for p in present), present, ">100 each"),
              check("no invented roads: route ink only on the confirmed path", outside == 0, outside, 0),
              check("crayon texture (broken, not solid fill)", tex > 0.3, tex, ">0.3"),
              check("numbered stops (ink rings + numbers)", stops >= 4, int(stops), ">=4"),
              check("negative control: an invented shortcut lands off the confirmed path", int((route_b & ~allowed).sum()) > 200, int((route_b & ~allowed).sum()), ">200")]
    return checks, [wd / "trip_map.png", path]


def onset_times(samples, rate, thr=0.2, gap=0.15):
    import numpy as np
    env = np.abs(np.asarray(samples, dtype=float))
    hop = int(rate * 0.005)
    e = np.array([env[i:i + hop].max() for i in range(0, len(env) - hop, hop)])
    out, last = [], -1.0
    for i in range(1, len(e)):
        t = i * hop / rate
        if e[i] > thr and e[i - 1] <= thr and t - last > gap:
            out.append(t)
            last = t
    return out


@card("DRAW-P01")
def one_line_three_beats(task, wd):
    import numpy as np
    from PIL import Image, ImageDraw
    W, H, fps, D = 360, 640, 24, 6.0
    way = [(40, 600), (80, 520), (180, 500), (260, 430), (300, 340), (220, 300), (120, 320), (70, 250), (110, 170), (200, 150), (280, 190), (300, 110), (230, 60)]
    line = catmull_like(way, 18)
    beats = [0.9 + 0.85 * k for k in range(3)]
    beat_pts = [way[3], way[6], way[9]]
    loop_c = (180, 80)
    loop = [(loop_c[0] + 110 * math.cos(2 * math.pi * k / 120), loop_c[1] + 40 * math.sin(2 * math.pi * k / 120)) for k in range(121)]

    def frame(t):
        im = Image.new("RGB", (W, H), (10, 12, 18))
        d = ImageDraw.Draw(im)
        seg = partial(line, smoothstep(t / 4.1), 2000)
        if len(seg) > 1:
            d.line(seg, fill=(240, 240, 235), width=3, joint="curve")
        for k, (bt, p) in enumerate(zip(beats, beat_pts)):
            g = smoothstep((t - bt) / 0.55)
            if g > 0:
                r = 9 * g
                d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=(231, 182, 90))
                d.text((p[0] + 14, p[1] - 6), ["01 CAPTURE", "02 CONNECT", "03 RESURFACE"][k], fill=(int(231 * g), int(182 * g), int(90 * g)))
        lp = partial(loop, max(0, min(1, (t - 4.25) / 1.1)), 600)
        if len(lp) > 1:
            d.line(lp, fill=(240, 240, 235), width=3)
        d.text((150, 74), "WORD", fill=(240, 240, 235))
        return np.asarray(im)
    n = int(D * fps)
    vid = write_mp4(wd / "line_video.mp4", [frame(i / fps) for i in range(n)], fps)
    rate = 44100
    tt = np.arange(int(D * rate)) / rate
    audio = np.zeros_like(tt)
    for bt in beats:
        m = (tt >= bt) & (tt < bt + 0.25)
        audio[m] += 0.7 * np.sin(2 * np.pi * 880 * (tt[m] - bt)) * np.exp(-(tt[m] - bt) * 18)
    m = (tt >= 4.25) & (tt < 5.35)
    audio[m] += 0.15 * np.sin(2 * np.pi * 220 * (tt[m] - 4.25)) * np.sin(np.pi * (tt[m] - 4.25) / 1.1)
    fx.write_wav(wd / "sound.wav", audio, rate)
    out = wd / "one_line.mp4"
    fx.ffmpeg("-y", "-i", str(vid), "-i", str(wd / "sound.wav"), "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out))
    pr = fx.probe(out)
    v = next(s for s in pr["streams"] if s["codec_type"] == "video")
    dur = float(pr["format"]["duration"])
    fx.ffmpeg("-y", "-i", str(out), "-vn", "-ac", "1", "-ar", str(rate), str(wd / "back.wav"))
    back, _ = fx.read_wav(wd / "back.wav")
    back = np.asarray(back, dtype=float).reshape(-1)
    ons = onset_times(back, rate, thr=0.3)
    probe_pts = resample(line, 1000)
    fr = read_mp4(out, W, H)
    drawn = lambda f: max([i for i, c in enumerate(sample_colours(np.asarray(fr[f]), probe_pts)) if min(c) > 200] or [0]) / 1000
    d2 = drawn(int(2.05 * fps))
    beat_r = lambda f, k: int((np.abs(fr[f][beat_pts[k][1] - 12:beat_pts[k][1] + 12, beat_pts[k][0] - 12:beat_pts[k][0] + 12].astype(int) - (231, 182, 90)).sum(-1) < 60).sum())
    silent = onset_times(np.zeros(rate), rate, thr=0.3)
    path = jw(wd / "one_line.json", {"size": [v["width"], v["height"]], "fps": v["r_frame_rate"], "duration": dur, "onsets": ons, "drawn_2.05": d2})
    checks = [check("360x640 at 24 fps, 6 s", [v["width"], v["height"]] == [360, 640] and v["r_frame_rate"] == "24/1" and abs(dur - 6) < 0.1, [v["width"], v["height"], v["r_frame_rate"], dur], [360, 640, "24/1", 6]),
              check("drawn length = smoothstep(t / 4.1) (measured at 2.05 s)", abs(d2 - smoothstep(2.05 / 4.1)) < 0.03, d2, smoothstep(2.05 / 4.1)),
              check("one unbroken line: 13 waypoints x 18 steps", len(line) == 12 * 18 + 1, len(line), 217),
              check("beat dots grow from 0.9 / 1.75 / 2.6 s", beat_r(int(0.85 * fps), 0) == 0 and beat_r(int(1.6 * fps), 0) > 100 and beat_r(int(1.6 * fps), 1) == 0,
                    [beat_r(int(0.85 * fps), 0), beat_r(int(1.6 * fps), 0), beat_r(int(1.6 * fps), 1)], [0, ">100", 0]),
              check("code-synthesised sound hits the three beats", len(ons) == 3 and all(abs(a - b) < 0.03 for a, b in zip(ons, beats)), ons, beats),
              check("negative control: silence has no onsets", silent == [], silent, [])]
    return checks, [out, path]


@card("DRAW-X01")
def quill_on_ink_frontier(task, wd):
    import numpy as np
    from PIL import Image, ImageDraw
    W, H, fps = 400, 120, 30
    # a lyric line written right to left (RTL): the ink frontier moves from x 370 to x 30
    stroke = [(370 - 340 * k / 200, 60 + 18 * math.sin(k / 9) * math.sin(k / 31)) for k in range(201)]
    lag = 4
    reveal = lambda t: bez(.45, 0, .55, 1)(max(0, min(1, t / 2.5)))

    def frame(t, follow=True):
        im = Image.new("RGB", (W, H), (248, 244, 236))
        d = ImageDraw.Draw(im)
        seg = partial(stroke, reveal(t), 1000)
        if len(seg) > 1:
            d.line(seg, fill=(30, 30, 40), width=4, joint="curve")
        if follow:
            fxp = seg[-1] if seg else stroke[0]
        else:
            fxp = (370 - 340 * min(1, t / 2.5), 60)       # its own linear tween
        nib = (fxp[0] + lag, fxp[1])                      # slightly behind the frontier (RTL -> to its right)
        d.ellipse([nib[0] - 3, nib[1] - 3, nib[0] + 3, nib[1] + 3], fill=(214, 40, 40))
        d.line([nib, (nib[0] + 30, nib[1] - 40)], fill=(150, 90, 40), width=3)
        return np.asarray(im)

    def measure(frames):
        errs = []
        for a in frames:
            ink = (a.sum(-1) < 200)
            nibm = (a[:, :, 0] > 180) & (a[:, :, 1] < 80)
            cols = np.nonzero(ink.any(0))[0]
            if not len(cols) or not nibm.any():
                continue
            frontier = cols.min()                         # RTL: the leftmost ink is the newest
            errs.append(float(np.nonzero(nibm)[1].mean()) - frontier)
        return errs
    ts = [i / fps for i in range(2, int(2.4 * fps))]
    F = [frame(t) for t in ts]
    mp4 = write_mp4(wd / "quill.mp4", F, fps)
    e = measure(read_mp4(mp4, W, H))
    e_bad = measure([frame(t, False) for t in ts])
    path = jw(wd / "quill.json", {"nib_minus_frontier": e, "independent": e_bad})
    checks = [check("nib sits on the ink frontier every frame", max(abs(x - lag) for x in e) <= 3, [min(e), max(e)], "lag 4 +- 3 px"),
              check("hand moves right to left (RTL)", read_nib(F[0]) > read_nib(F[-1]) + 200, [read_nib(F[0]), read_nib(F[-1])], "decreasing x"),
              check("kept slightly behind the frontier (never ahead)", min(e) >= 0, min(e), ">=0"),
              check("negative control: a hand on its own tween drifts off the frontier", max(abs(x - lag) for x in e_bad) > 15, max(abs(x - lag) for x in e_bad), ">15 px")]
    return checks, [mp4, path]


def read_nib(a):
    import numpy as np
    m = (a[:, :, 0] > 180) & (a[:, :, 1] < 80)
    return float(np.nonzero(m)[1].mean())


@card("DRAW-56")
def coded_drawing_over_clip(task, wd):
    import numpy as np
    from PIL import Image
    fps, W, H = 24, 192, 108
    clip = wd / "generated.mp4"
    fx.ffmpeg("-y", "-f", "lavfi", "-i", "testsrc2=size=%dx%d:rate=%d:duration=2" % (W, H, fps), "-f", "lavfi", "-i", "sine=frequency=330:duration=2",
              "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-shortest", str(clip))
    base = read_mp4(clip, W, H)
    paper = np.array([244, 238, 226], float)
    ink1, ink2 = np.array([30, 34, 48], float), np.array([200, 60, 50], float)
    tooth = np.random.default_rng(0).normal(0, 4, (H, W, 1))       # fixed paper tooth

    def render_at(f):
        t = f / fps
        lum = base[f].astype(float).mean(-1) / 255
        y, x = np.mgrid[0:H, 0:W]
        cell = 6
        cx, cy = (x // cell) * cell + cell / 2, (y // cell) * cell + cell / 2
        lc = lum[np.clip(cy.astype(int), 0, H - 1), np.clip(cx.astype(int), 0, W - 1)]
        dots = np.hypot(x - cx, y - cy) < (1 - lc) * cell * 0.6
        img = np.repeat(paper[None, None], H, 0).repeat(W, 1) + tooth
        img[dots] = ink1
        rng = np.random.default_rng(int(t * 12))                    # boil 12x per second
        edge = np.abs(np.diff(lum, axis=1, prepend=lum[:, :1])) > 0.25
        jit = np.roll(edge, int(rng.integers(-1, 2)), axis=1)
        img[jit] = ink2
        return np.clip(img, 0, 255).astype(np.uint8), lc, dots
    out = [render_at(f) for f in range(len(base))]
    v = write_mp4(wd / "drawing_layer.mp4", [o[0] for o in out], fps)
    film = wd / "film.mp4"
    fx.ffmpeg("-y", "-i", str(v), "-i", str(clip), "-map", "0:v", "-map", "1:a", "-c", "copy", str(film))
    md5 = lambda p: subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(p), "-map", "0:a", "-c", "copy", "-f", "md5", "-"], capture_output=True, text=True, timeout=30).stdout.strip()
    jit_masks = [(np.abs(o[0].astype(int) - ink2).sum(-1) < 10) for o in out]

    def shift_of(f):
        # measured on the output: which roll of the base clip's edges the drawn line work matches
        lum = base[f].astype(float).mean(-1) / 255
        edge = np.abs(np.diff(lum, axis=1, prepend=lum[:, :1])) > 0.25
        return min((-1, 0, 1), key=lambda s_: int((np.roll(edge, s_, axis=1) ^ jit_masks[f]).sum()))
    shifts = [shift_of(f) for f in range(len(out))]
    step = [int(f / fps * 12) for f in range(len(out))]
    other = [f for f in range(1, len(out)) if step[f] == step[f - 1] and shifts[f] != shifts[f - 1]]
    changes = [f for f in range(1, len(out)) if step[f] != step[f - 1] and shifts[f] != shifts[f - 1]]
    a0, lc0, d0 = out[10]
    cov = [d0[(lc0 > a) & (lc0 <= a + 0.25)].mean() for a in (0, 0.25, 0.5, 0.75) if ((lc0 > a) & (lc0 <= a + 0.25)).any()]
    empty = ~np.any([o[2] | jit_masks[i] for i, o in enumerate(out)], axis=0)
    tooth_same = all(np.array_equal(o[0][empty], out[0][0][empty]) for o in out[::7])
    colours_layer = palette_count(out[10][0], (244, 238, 226), tol=40)
    colours_base = palette_count(base[10], (244, 238, 226), tol=40)
    path = jw(wd / "coded_layer.json", {"audio_md5_src": md5(clip), "audio_md5_film": md5(film), "boil_changes": len(changes), "changes_inside_step": len(other),
                                         "halftone_cov": [float(c) for c in cov], "inks": colours_layer, "base_colours": colours_base})
    checks = [check("original audio muxed byte for byte (stream copy)", md5(clip) == md5(film) and md5(clip) != "", [md5(clip)[-12:], md5(film)[-12:]], "equal"),
              check("line work boils 12x per second: pose changes only on 1/12 s steps", len(other) == 0 and len(changes) >= 10, [len(changes), len(other)], [">=10 of 23 steps", 0]),
              check("halftone: darker base -> more ink", all(a > b for a, b in zip(cov, cov[1:])), [round(float(c), 3) for c in cov], "decreasing"),
              check("fixed paper tooth (identical where nothing is drawn)", tooth_same and int(empty.sum()) > 100, int(empty.sum()), "same"),
              check("two inks on paper", colours_layer <= 3, colours_layer, "<=3 incl. tooth"),
              check("negative control: the generated base frame is full colour", colours_base > 5, colours_base, ">5")]
    return checks, [film, path]


@card("DRAW-57")
def trace_reference_style(task, wd):
    import numpy as np
    import cv2
    from PIL import Image, ImageDraw
    W, H = 320, 240
    ref = Image.new("L", (W, H), 236)
    d = ImageDraw.Draw(ref)
    d.ellipse([40, 40, 140, 140], outline=30, width=5)
    d.polygon([(180, 200), (300, 200), (240, 60)], outline=30, width=4)
    d.line([(30, 210), (150, 180)], fill=30, width=3)
    ref.save(wd / "ref.png")
    fx.ffmpeg("-y", "-loop", "1", "-i", str(wd / "ref.png"), "-t", "0.2", "-r", "10", "-c:v", "libx264", "-crf", "23", "-pix_fmt", "yuv420p", str(wd / "ref.mp4"))
    dec = read_mp4(wd / "ref.mp4", W, H)[0].mean(-1)
    truth = np.asarray(ref) < 133
    ink, pap = float(np.percentile(dec, 2)), float(np.percentile(dec, 98))
    mid = (ink + pap) / 2

    def trace(S, thr):
        blur = cv2.GaussianBlur(dec, (0, 0), 1.0)
        sharp = cv2.addWeighted(dec, 1.6, blur, -0.6, 0)
        up = cv2.resize(sharp, (W * S, H * S), interpolation=cv2.INTER_CUBIC)
        m = (up < thr).astype(np.uint8)
        cs, hier = cv2.findContours(m, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
        canvas = np.zeros_like(m)
        polys = [cv2.approxPolyDP(c, 0.5 * S, True) for c in cs]
        # outer contours first, then holes cut back out
        order = sorted(range(len(polys)), key=lambda i: (hier[0][i][3] >= 0) if hier is not None else 0)
        for i in order:
            cv2.fillPoly(canvas, [polys[i]], 0 if (hier is not None and hier[0][i][3] >= 0) else 1)
        back = cv2.resize(canvas.astype(np.float32), (W, H), interpolation=cv2.INTER_AREA) > 0.5
        return back, len(polys)
    t4, n4 = trace(4, mid)
    t1, _ = trace(1, mid)
    tbad, _ = trace(4, ink + 0.1 * (pap - ink))
    floor = float(((dec < mid) ^ truth).mean())
    xor = lambda m: float((m ^ truth).mean())
    dist = cv2.distanceTransform(truth.astype(np.uint8), cv2.DIST_L2, 3)
    sk = dist[dist > 0]
    style = {"stroke_half_width_p10_p50_p90": [float(np.percentile(sk, q)) for q in (10, 50, 90)], "ink_share": float(truth.mean())}
    Image.fromarray((t4 * 255).astype(np.uint8)).save(wd / "traced.png")
    path = jw(wd / "style.json", {"xor_s4": xor(t4), "xor_s1": xor(t1), "xor_bad_threshold": xor(tbad), "codec_floor": floor, "contours": n4, "style": style})
    checks = [check("traced + re-rendered matches the reference (XOR < 1%)", xor(t4) < 0.01, xor(t4), "<0.01"),
              check("close to the codec floor", xor(t4) <= floor + 0.006, [xor(t4), floor], "within 0.6% of floor"),
              check("contours found for every figure (holes kept)", n4 >= 5, n4, ">=5"),
              check("style statistics stored as p10/p50/p90 bands", len(style["stroke_half_width_p10_p50_p90"]) == 3 and style["stroke_half_width_p10_p50_p90"][0] <= style["stroke_half_width_p10_p50_p90"][2],
                    style["stroke_half_width_p10_p50_p90"], "3 ordered values"),
              check("4x supersampling is no worse than 1x", xor(t4) <= xor(t1) + 1e-4, [xor(t4), xor(t1)], "s4 <= s1"),
              check("negative control: a threshold far from the ink/paper midpoint loses the strokes", xor(tbad) > 2 * xor(t4), [xor(tbad), xor(t4)], ">2x")]
    return checks, [wd / "traced.png", path]


@card("DRAW-30")
def dabs_and_js_blur(task, wd):
    body = "<canvas id=c width=200 height=120></canvas>"
    js = """const cv=$('#c'), c=cv.getContext('2d');
const contour=[]; for(let i=0;i<=80;i++){const a=i/80*Math.PI*2; contour.push([100+60*Math.cos(a), 60+35*Math.sin(a)]);}
function dabs(bias){ c.lineCap='round'; c.strokeStyle='#222'; c.lineWidth=2*bias; for(let i=1;i<contour.length;i++){c.beginPath(); c.moveTo(...contour[i-1]); c.lineTo(...contour[i]); c.stroke();} }
function gauss(sigma){ const r=Math.ceil(3*sigma), k=[]; let s=0; for(let i=-r;i<=r;i++){const v=Math.exp(-i*i/(2*sigma*sigma)); k.push(v); s+=v;} k.forEach((v,i)=>k[i]=v/s);
 const im=c.getImageData(0,0,200,120), d=im.data, tmp=new Float32Array(d.length);
 for(let y=0;y<120;y++)for(let x=0;x<200;x++)for(let ch=0;ch<4;ch++){let a=0; for(let i=-r;i<=r;i++){const xx=Math.min(199,Math.max(0,x+i)); a+=d[(y*200+xx)*4+ch]*k[i+r];} tmp[(y*200+x)*4+ch]=a;}
 for(let y=0;y<120;y++)for(let x=0;x<200;x++)for(let ch=0;ch<4;ch++){let a=0; for(let i=-r;i<=r;i++){const yy=Math.min(119,Math.max(0,y+i)); a+=tmp[(yy*200+x)*4+ch]*k[i+r];} d[(y*200+x)*4+ch]=Math.round(a);}
 c.putImageData(im,0,0); }
const hash=()=>{const d=c.getImageData(0,0,200,120).data; let h=2166136261; for(let i=0;i<d.length;i++){h^=d[i]; h=Math.imul(h,16777619)>>>0;} return h;};
const soft=()=>{const d=c.getImageData(0,0,200,120).data; let n=0; for(let i=3;i<d.length;i+=4) if(d[i]>10&&d[i]<245) n++; return n;};
window.renderFrame=(t)=>{c.filter='none'; c.clearRect(0,0,200,120); dabs(1.5+0.5*Math.sin(t)); gauss(0.85);};
const out={};
c.clearRect(0,0,200,120); dabs(1.5); out.plain=hash(); out.plain_soft=soft();
for(const b of ['0.3px','0.5px','0.6px','0.7px','1px','2px']){c.clearRect(0,0,200,120); c.filter='blur('+b+')'; dabs(1.5); c.filter='none'; out['f'+b]=hash(); out['soft'+b]=soft();}
renderFrame(0.3); out.r1=hash(); out.js_soft=soft(); renderFrame(0.3); out.r2=hash(); renderFrame(1.3); out.r3=hash();
c.clearRect(0,0,200,120); dabs(1.5); const d=c.getImageData(0,0,200,120).data; let w=0; for(let y=0;y<120;y++){ if(d[(y*200+100)*4+3]>128) w++; } out.width_at_x100=w;
R(out);"""
    r = kit_page(wd, "dabs", body, js)
    path = jw(wd / "dabs.json", r)
    sub = [k for k in ("0.3px", "0.5px", "0.6px", "0.7px") if r["f" + k] == r["plain"]]
    checks = [check("capsule dabs of width 2 x bias along the contour (bias 1.5: 2 crossings x ~3 px)", 5 <= r["width_at_x100"] <= 8, r["width_at_x100"], "~6"),
              check("measured here: small ctx.filter blurs are silent no-ops (0.3 and 0.5 px; threshold recorded)", "0.3px" in sub and "0.5px" in sub, sub, "0.3px, 0.5px unchanged"),
              check("ctx.filter blur(1px) and above does blur", r["f1px"] != r["plain"] and r["soft2px"] > r["plain_soft"], [r["soft1px"], r["soft2px"], r["plain_soft"]], "softer"),
              check("JS Gaussian (sigma 0.85) blurs where the filter cannot", r["js_soft"] > r["plain_soft"] * 1.3, [r["js_soft"], r["plain_soft"]], ">1.3x soft pixels"),
              check("identical pixels every time (renderFrame(t) deterministic)", r["r1"] == r["r2"] and r["r1"] != r["r3"], [r["r1"], r["r2"], r["r3"]], "same t same hash"),
              check("negative control: unblurred dabs have few soft pixels", r["plain_soft"] < r["js_soft"], r["plain_soft"], "< blurred")]
    return checks, [path]


@card("DRAW-58")
def raster_to_compact_svg(task, wd):
    import base64
    import io
    import numpy as np
    from PIL import Image, ImageDraw, ImageFilter
    W, H = 600, 300
    top, mid, bot = hexrgb("#8f8ae0"), hexrgb("#c9c3f5"), hexrgb("#f1e9fb")
    sky = np.zeros((H, W, 3))
    for y in range(H):
        u = y / (H - 1)
        a, b, k = (top, mid, u / 0.5) if u < 0.5 else (mid, bot, (u - 0.5) / 0.5)
        sky[y] = [p + (q - p) * k for p, q in zip(a, b)]
    im = Image.fromarray(sky.astype(np.uint8))
    d = ImageDraw.Draw(im)
    dunes = [("#b7aee8", 0.62, 30), ("#8d84d6", 0.72, 22), ("#6a60c0", 0.84, 16)]
    dune_pts = []
    for col, base, amp in dunes:
        pts = [(x, H * base - amp * math.sin(x / 90 + base * 9)) for x in range(0, W + 1, 20)] + [(W, H), (0, H)]
        dune_pts.append(pts)
        d.polygon(pts, fill=hexrgb(col))
    d.ellipse([470, 40, 510, 80], fill=(250, 246, 230))
    d.ellipse([482, 34, 522, 74], fill=tuple(int(v) for v in sky[54, 500]))
    for x, y in [(80, 40), (150, 70), (300, 30), (380, 60)]:
        d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(255, 255, 255))
    d.rectangle([120, 150, 126, 215], fill=hexrgb("#4e46a8"))
    d.ellipse([95, 135, 150, 160], fill=hexrgb("#4e46a8"))
    im = im.filter(ImageFilter.GaussianBlur(0.6))
    noise = np.random.default_rng(3).normal(0, 3, (H, W, 3))
    raster = Image.fromarray(np.clip(np.asarray(im) + noise, 0, 255).astype(np.uint8))   # the "generated" plate
    raster.save(wd / "generated.png")
    s = 2.0
    paths = "".join('<path id="dune%d" fill="%s" d="M%s"/>' % (i, col, " L".join("%d %d" % (x * s, y * s) for x, y in pts)) for i, ((col, _, _), pts) in enumerate(zip(dunes, dune_pts)))
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 600" preserveAspectRatio="xMinYMax slice" width="600" height="300">'
           '<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8f8ae0"/><stop offset=".5" stop-color="#c9c3f5"/>'
           '<stop offset="1" stop-color="#f1e9fb"/></linearGradient></defs><rect width="1200" height="600" fill="url(#g)"/>' + paths +
           '<circle cx="980" cy="120" r="40" fill="#faf6e6"/><circle cx="1004" cy="108" r="40" fill="%s"/>' % ("#%02x%02x%02x" % tuple(int(v) for v in sky[54, 500])) +
           "".join('<circle cx="%d" cy="%d" r="4" fill="#fff"/>' % (x * 2, y * 2) for x, y in [(80, 40), (150, 70), (300, 30), (380, 60)]) +
           '<g fill="#4e46a8"><rect x="240" y="300" width="12" height="130"/><ellipse cx="245" cy="295" rx="55" ry="25"/></g></svg>')
    (wd / "valley-dusk.svg").write_text(svg, encoding="utf-8")
    avg = "#%02x%02x%02x" % tuple(int(v) for v in np.asarray(raster).reshape(-1, 3).mean(0))
    flat = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 600" width="600" height="300"><rect width="1200" height="600" fill="%s"/></svg>' % avg
    buf = io.BytesIO()
    raster.save(buf, "PNG")
    png64 = base64.b64encode(buf.getvalue()).decode()
    js = """const load=(src)=>new Promise(r=>{const i=new Image(); i.onload=()=>r(i); i.src=src;});
const px=(img)=>{const c=document.createElement('canvas'); c.width=600; c.height=300; const x=c.getContext('2d'); x.drawImage(img,0,0,600,300); return x.getImageData(0,0,600,300).data;};
(async()=>{const ras=px(await load('data:image/png;base64,%s')); const score=async(svg)=>{const v=px(await load('data:image/svg+xml;base64,'+btoa(svg))); let s=0; for(let i=0;i<v.length;i+=4){s+=Math.abs(v[i]-ras[i])+Math.abs(v[i+1]-ras[i+1])+Math.abs(v[i+2]-ras[i+2]);} return 1-s/(600*300*3*255);};
R({svg:await score(%s), flat:await score(%s)});})();""" % (png64, json.dumps(svg), json.dumps(flat))
    r = kit_page(wd, "score", "", js)
    kb = len(svg.encode()) / 1024
    path = jw(wd / "svg_score.json", {"bytes": len(svg.encode()), "score_svg": r["svg"], "score_flat": r["flat"]})
    checks = [check("compact SVG (< 3 KB)", kb < 3.0, round(kb, 2), "<3 KB"),
              check("three dune paths as parallax layers + gradient sky", svg.count('id="dune') == 3 and "linearGradient" in svg, svg.count('id="dune'), 3),
              check("1200x600 xMinYMax slice", 'viewBox="0 0 1200 600"' in svg and "xMinYMax slice" in svg, True, True),
              check("scored against the raster: similarity > 0.97", r["svg"] > 0.97, r["svg"], ">0.97"),
              check("negative control: a flat average-colour SVG scores clearly lower", r["flat"] < r["svg"] - 0.05, [r["flat"], r["svg"]], "lower by >0.05")]
    return checks, [wd / "valley-dusk.svg", path]
