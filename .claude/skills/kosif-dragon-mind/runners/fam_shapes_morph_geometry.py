"""shapes-morph-geometry: method cards as real programs with known-answer checks.

Engines: the repo motion kit (motion-kit.js) and shape kit (shape-kit.js, SDF sculpting) with GSAP / three in node
or headless Chrome (real SVG geometry), HyperFrames registry components, numpy/PIL/scikit-image for measuring.
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


def area(pts):
    return 0.5 * abs(sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts))))


def centroid(pts):
    a = 0.0
    cx = cy = 0.0
    for i in range(len(pts)):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % len(pts)]
        c = x0 * y1 - x1 * y0
        a += c
        cx += (x0 + x1) * c
        cy += (y0 + y1) * c
    a *= 0.5
    return cx / (6 * a), cy / (6 * a)


def star_d(cx, cy, R, r, n=5):
    pts = []
    for k in range(2 * n):
        ang = -math.pi / 2 + k * math.pi / n
        rad = R if k % 2 == 0 else r
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    return "M " + " L ".join("%.3f %.3f" % p for p in pts) + " Z", pts


def poly_png(path, polys, size=(200, 200), fill=(240, 200, 90)):
    from PIL import Image, ImageDraw
    im = Image.new("RGB", size, (12, 14, 20))
    d = ImageDraw.Draw(im)
    for p in polys:
        d.polygon([tuple(q) for q in p], outline=fill)
    im.save(path)
    return Path(path)


@card("SHAPE-01")
def seek_safe_path_morph(task, wd):
    circ = "M 100 20 A 80 80 0 1 1 99.99 20 Z"
    star, _ = star_d(100, 100, 80, 34)
    js = """const p=$('#p'); const tl=gsap.timeline({paused:true}); M.morphPath(tl,p,%s,%s,0.2,{points:120});
const ref=(d)=>{const q=document.createElementNS('http://www.w3.org/2000/svg','path'); q.setAttribute('d',d); $('svg').appendChild(q);
 const L=q.getTotalLength(); const o=[]; for(let i=0;i<=120;i++){const z=q.getPointAtLength(L*i/120); o.push([z.x,z.y]);} q.remove(); return o;};
const at=(t)=>{tl.seek(t); return ptsOf(p.getAttribute('d'));}; tl.seek(1);
R({a:at(0.2+1e-6), m:at(0.53), b:at(0.86), b2:at(1.3), A:ref(%s), B:ref(%s), closed:p.getAttribute('d').trim().endsWith('Z')});""" % (
        json.dumps(circ), json.dumps(star), json.dumps(circ), json.dumps(star))
    r = kit_page(wd, "morph", '<svg width=200 height=200><path id=p d="%s"/></svg>' % circ, js)
    dist = lambda P, Q: max(math.hypot(a[0] - b[0], a[1] - b[1]) for a, b in zip(P, Q))
    aA, aB, aM = area(r["a"][:-1]), area(r["b"][:-1]), area(r["m"][:-1])
    shift = r["B"][30:] + r["B"][1:31]
    travel = sum(math.hypot(a[0] - b[0], a[1] - b[1]) for a, b in zip(r["A"], r["B"]))
    travel_rot = sum(math.hypot(a[0] - b[0], a[1] - b[1]) for a, b in zip(r["A"], shift))
    path = jw(wd / "morph.json", r)
    poly_png(wd / "morph.png", [r["a"], r["m"], r["b"]])
    checks = [check("first frame == circle (120 samples)", dist(r["a"], r["A"]) < 0.5, dist(r["a"], r["A"]), "<0.5"),
              check("last frame == star", dist(r["b"], r["B"]) < 0.5 and dist(r["b2"], r["B"]) < 0.5, dist(r["b"], r["B"]), "<0.5"),
              check("area at the midpoint lies between A and B", min(aA, aB) < aM < max(aA, aB), [aA, aM, aB], "between"),
              check("both start at top-centre (no twist)", abs(r["A"][0][0] - 100) < 0.1 and abs(r["B"][0][1] - 20) < 0.1 and travel < travel_rot,
                    [travel, travel_rot], "aligned < rotated"),
              check("121 points written, closed with Z", len(r["a"]) == 121 and r["closed"], len(r["a"]), 121),
              check("negative control: the untreated circle is not the star", dist(r["A"], r["B"]) > 20, dist(r["A"], r["B"]), ">20")]
    return checks, [path, wd / "morph.png"]


@card("SHAPE-13")
def morphsvg_plugin(task, wd):
    body = '<svg width=300 height=200><circle id=c cx=80 cy=100 r=50 fill="#e7b65a"/><rect id=r x=160 y=40 width=120 height=120 fill="#5bd1a5"/></svg>'
    js = """gsap.registerPlugin(MorphSVGPlugin); const [c,r]=MorphSVGPlugin.convertToPath('#c,#r');
const tl=gsap.timeline({paused:true}); tl.to(c,{morphSVG:r,duration:1,ease:'none'});
const bb=(t)=>{tl.seek(t); const b=c.getBBox(); return [b.x,b.y,b.width,b.height,c.getTotalLength()];};
const rb=r.getBBox(); R({tag:[c.tagName,r.tagName], s:bb(0), m:bb(0.5), e:bb(1), rect:[rb.x,rb.y,rb.width,rb.height,r.getTotalLength()]});"""
    r = kit_page(wd, "morphsvg", body, js, plugins=("MorphSVGPlugin",))
    path = jw(wd / "morphsvg.json", r)
    e, rect, s0, m = r["e"], r["rect"], r["s"], r["m"]
    checks = [check("primitives converted to paths", r["tag"] == ["path", "path"], r["tag"], ["path", "path"]),
              check("starts as the circle (100x100 at 30,50)", all(abs(a - b) < 1 for a, b in zip(s0[:4], [30, 50, 100, 100])), s0[:4], [30, 50, 100, 100]),
              check("ends as the rect", all(abs(a - b) < 1 for a, b in zip(e[:4], rect[:4])), e[:4], rect[:4]),
              check("ends with the rect's perimeter", abs(e[4] - rect[4]) < 2, e[4], rect[4]),
              check("in-between sits between the two", s0[0] < m[0] < e[0] and m[4] > 0, m[:4], "between"),
              check("negative control: the circle alone is not the rect", abs(s0[0] - rect[0]) > 50, s0[0], rect[0])]
    return checks, [path]


@card("SHAPE-15")
def flip_continuity(task, wd):
    body = """<div id=A style="position:absolute;left:20px;top:20px;width:200px;height:200px"><div id=box style="width:100px;height:100px;background:#e7b65a"></div></div>
<div id=B style="position:absolute;left:400px;top:300px;width:400px;height:100px"></div>"""
    js = """const run=(invert)=>{const el=$('#box'); $('#A').appendChild(el); el.style.cssText='width:100px;height:100px;background:#e7b65a'; gsap.set(el,{clearProps:'transform'});
 const F=el.getBoundingClientRect(); $('#B').appendChild(el); el.style.width='200px'; el.style.height='50px'; const L=el.getBoundingClientRect();
 const tl=gsap.timeline({paused:true});
 if(invert){gsap.set(el,{transformOrigin:'0 0', x:F.left-L.left, y:F.top-L.top, scaleX:F.width/L.width, scaleY:F.height/L.height});
  tl.to(el,{x:0,y:0,scaleX:1,scaleY:1,duration:1,ease:'power2.inOut'});} else tl.to(el,{opacity:1,duration:1});
 const at=(t)=>{tl.seek(t); const b=el.getBoundingClientRect(); return [b.left,b.top,b.width,b.height,+getComputedStyle(el).opacity];};
 return {F:[F.left,F.top,F.width,F.height], L:[L.left,L.top,L.width,L.height], s:at(0), m:at(0.5), e:at(1), n:document.querySelectorAll('#box').length};};
R({flip:run(true), plain:run(false)});"""
    r = kit_page(wd, "flip", body, js)
    f = r["flip"]
    path = jw(wd / "flip.json", r)
    close = lambda a, b: max(abs(x - y) for x, y in zip(a, b)) < 0.6
    checks = [check("First: inverted element sits exactly on its old box", close(f["s"][:4], f["F"]), f["s"][:4], f["F"]),
              check("Play: ends exactly on the new box", close(f["e"][:4], f["L"]), f["e"][:4], f["L"]),
              check("midpoint is the eased in-between (power2.inOut(.5)=.5)", close(f["m"][:4], [(a + b) / 2 for a, b in zip(f["F"], f["L"])]),
                    f["m"][:4], [(a + b) / 2 for a, b in zip(f["F"], f["L"])]),
              check("one element, never crossfaded", f["n"] == 1 and f["s"][4] == 1 and f["m"][4] == 1, [f["n"], f["m"][4]], [1, 1]),
              check("negative control: without the inverse transform it jumps to the new box", close(r["plain"]["s"][:4], r["plain"]["L"]) and
                    not close(r["plain"]["s"][:4], r["plain"]["F"]), r["plain"]["s"][:4], r["plain"]["F"])]
    return checks, [path]


def rrect_frame(W, H, cx, cy, w, h, rad, col, alpha_bg=None):
    import numpy as np
    from PIL import Image, ImageDraw
    im = Image.new("RGB", (W, H), (10, 12, 18))
    d = ImageDraw.Draw(im)
    if w > 1 and h > 1:
        d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=max(0, min(rad, w / 2, h / 2)), fill=col)
    return np.asarray(im)


@card("SHAPE-16")
def card_morph_handoff(task, wd):
    import numpy as np
    js = """const c={scale:1,radius:24,r:30,g:40,b:80,shadow:6,opacity:1}, t={opacity:0}; const tl=gsap.timeline({paused:true});
tl.fromTo(c,{scale:1,radius:24,r:30,g:40,b:80,shadow:6},{scale:2.5,radius:4,r:231,g:182,b:90,shadow:24,duration:.6,ease:'power2.inOut'},0);
tl.to(t,{opacity:1,duration:.2,ease:'power1.out'},.6); tl.to(c,{opacity:0,duration:.2,ease:'power1.in'},.6);
const S=[]; for(let f=0;f<=24;f++){tl.seek(f/30); S.push([c.scale,c.radius,c.r,c.g,c.b,c.shadow,c.opacity,t.opacity]);} out(S);"""
    S = node(wd, "cardmorph", js)
    frames = [rrect_frame(240, 200, 120, 100, 60 * s[0], 40 * s[0], s[1], tuple(int(v * s[6]) for v in s[2:5])) for s in S]
    mp4 = write_mp4(wd / "card_morph.mp4", frames, 30)
    fr = read_mp4(mp4, 240, 200)
    widths = [(blob_x(q, thr=40) or {"x1": 0, "x0": 1})["x1"] - (blob_x(q, thr=40) or {"x1": 0, "x0": 1})["x0"] + 1 for q in fr]
    path = jw(wd / "card_morph.json", {"samples": S, "widths": widths})
    checks = [check("starts as card A (scale 1, radius 24)", S[0][:2] == [1, 24], S[0][:2], [1, 24]),
              check("lands on target (scale 2.5, radius 4, accent colour)", S[18][:5] == [2.5, 4, 231, 182, 90], S[18][:5], [2.5, 4, 231, 182, 90]),
              check("midpoint is power2.inOut(.5) = halfway", abs(S[9][0] - 1.75) < 1e-3, S[9][0], 1.75),
              check("real target fades in only after the morph", S[17][7] == 0 and S[24][7] == 1, [S[17][7], S[24][7]], [0, 1]),
              check("rendered width follows uniform scale (60 -> 150 px)", abs(widths[0] - 61) <= 2 and abs(widths[18] - 151) <= 2, [widths[0], widths[18]], [61, 151]),
              check("negative control: unmorphed card keeps its first size", abs(widths[0] - 151) > 50, widths[0], 151)]
    return checks, [mp4, path]


@card("SHAPE-17")
def morph_chain(task, wd):
    js = """const p={y:-300,sx:44/400,sy:.44,fill:0,count:0,bar:0}; const tl=gsap.timeline({paused:true}); const B=M.beats(120);
tl.to(p,{y:0,duration:.6,ease:M.E.hop},B.at(4)-.6); tl.to(p,{sx:1,sy:1,duration:.42,ease:M.E.inOut},B.at(4));
tl.to(p,{sx:2.0,sy:.24,duration:.34,ease:M.E.inOut},B.at(6)); tl.set(p,{bar:1},B.at(6)+.34);
tl.to(p,{fill:800,count:900,duration:1.1,ease:'none'},B.at(6)+.34);
const at=(t)=>{tl.seek(t); return [p.y,p.sx,p.sy,p.fill,p.count,p.bar];}; out({b4:B.at(4), s:[1.0,2.0,2.42,3.0,3.34,3.89,4.44].map(at)});"""
    r = node(wd, "chain", js)
    import numpy as np
    imgs = []
    for y, sx, sy, fill, cnt, bar in r["s"]:
        im, d = canvas(240, 120)
        w, h = 100 * sx, 25 * sy
        d.rounded_rectangle([120 - w / 2, 60 + y / 4 - h / 2, 120 + w / 2, 60 + y / 4 + h / 2], radius=min(w, h) / 2, fill=(230, 60, 60))
        imgs.append(np.asarray(im))
    mp4 = write_mp4(wd / "chain.mp4", [f for f in imgs for _ in range(6)], 30)
    S = r["s"]
    widths = [(blob_x(f.astype(float), thr=100) or {"x0": 0, "x1": -1}) for f in imgs]
    wpx = [w["x1"] - w["x0"] + 1 for w in widths]
    path = jw(wd / "chain.json", r)
    checks = [check("beat 4 at 120 BPM = 2.0 s", r["b4"] == 2.0, r["b4"], 2.0),
              check("one red dot before the beat (44/400 x .44)", abs(S[0][1] - 0.11) < 1e-3, S[0][1:3], [0.11, 0.44]),
              check("pill full size .42 s after beat 4", S[2][1:3] == [1, 1], S[2][1:3], [1, 1]),
              check("press flattens to a bar (2.0 x .24) in .34 s", S[4][1:3] == [2, 0.24] and S[4][5] == 1, S[4][1:3], [2, 0.24]),
              check("fill runs linearly 0 -> 800 over 1.1 s", abs(S[5][3] - 400) < 1e-6 and S[6][3] == 800, [S[5][3], S[6][3]], [400, 800]),
              check("counter lands on 900", S[6][4] == 900, S[6][4], 900),
              check("rendered widths dot < pill < bar", wpx[0] < wpx[2] < wpx[4], [wpx[0], wpx[2], wpx[4]], "growing"),
              check("negative control: the dot is not yet a pill", abs(S[0][1] - 1) > 0.5, S[0][1], 1)]
    return checks, [mp4, path]


@card("SHAPE-20")
def hamburger_to_close(task, wd):
    import numpy as np
    from PIL import Image, ImageDraw
    fps, n = 30, 6

    def frame(p):
        e = power_inout2(p)
        im = Image.new("L", (120, 120), 0)
        d = ImageDraw.Draw(im)
        for k, (y0, ang) in enumerate([(-18, 45), (0, 0), (18, -45)]):
            if k == 1:
                sc = 1 - e
                if sc > 0.02:
                    d.rectangle([60 - 30 * sc, 57, 60 + 30 * sc, 63], fill=int(255 * (1 - e)))
                continue
            a = math.radians(ang * e)
            yy = y0 * (1 - e)
            dx, dy = 30 * math.cos(a), 30 * math.sin(a)
            d.line([60 - dx, 60 + yy - dy, 60 + dx, 60 + yy + dy], fill=255, width=6)
        return np.stack([np.asarray(im)] * 3, axis=2)
    imgs = [frame(f / n) for f in range(n + 1)]
    mp4 = write_mp4(wd / "burger.mp4", imgs + [imgs[-1]] * 10, fps)
    fr = read_mp4(mp4, 120, 120)
    lit = lambda q, x, y: q[y, x, 0] > 128
    end, start = fr[n], fr[0]
    path = jw(wd / "burger.json", {"frames": n, "seconds": n / fps})
    checks = [check("0.2 s = 6 frames at 30 fps", n / fps == 0.2, n / fps, 0.2),
              check("end: both diagonals cross at the centre (X)", lit(end, 60, 60) and lit(end, 75, 45) and lit(end, 75, 75) and lit(end, 45, 45),
                    True, True),
              check("end: middle bar collapsed", not lit(end, 85, 60) and not lit(end, 35, 60), False, False),
              check("end: top and bottom rotated +-45 deg (no horizontal bars left)", not lit(end, 85, 42) and not lit(end, 85, 78), False, False),
              check("negative control: the untreated menu has three horizontal bars", lit(start, 85, 42) and lit(start, 85, 60) and lit(start, 85, 78),
                    True, True)]
    return checks, [mp4, path]


def power_inout2(p):
    return (2 * p) ** 3 / 2 if p < 0.5 else 1 - (2 * (1 - p)) ** 3 / 2


@card("SHAPE-23")
def ring_iris_flood(task, wd):
    import numpy as np
    from PIL import Image, ImageDraw
    sc = 5  # render 1080x1920 at 1/5
    W, H = 1080 // sc, 1920 // sc
    eIn = bez(.7, 0, .84, 0)
    eIris = bez(.4, 0, .7, .92)
    fps = 30
    frames, radii_plan = [], []
    for f in range(int(4.6 * fps)):
        t = f / fps
        im = Image.new("RGB", (W, H), (8, 10, 20))
        d = ImageDraw.Draw(im)
        if t < 4.05:
            p = min(1, max(0, (t - 3.65) / 0.45))
            s = 1 - (1 - .14) * eIn(p)
            sw = 6 + (60 - 6) * eIn(p)
            R = 300 * s
            d.ellipse([540 / sc - R / sc, 930 / sc - R / sc, 540 / sc + R / sc, 930 / sc + R / sc], outline=(245, 240, 230), width=max(1, int(sw / sc)))
            radii_plan.append(None)
        else:
            p = min(1, (t - 4.05) / 0.5)
            r = math.exp(math.log(60) + (math.log(2300) - math.log(60)) * eIris(p))
            radii_plan.append(r)
            d.ellipse([540 / sc - r / sc, 930 / sc - r / sc, 540 / sc + r / sc, 930 / sc + r / sc], fill=(231, 182, 90))
        frames.append(np.asarray(im))
    mp4 = write_mp4(wd / "iris.mp4", frames, fps)
    fr = read_mp4(mp4, W, H)
    brand = lambda q: ((np.abs(q - np.array([231, 182, 90])) < 30).all(axis=2))
    meas_r = [math.sqrt(brand(q).sum() / math.pi) * sc for q in fr]
    f_mid = next(f for f in range(len(frames)) if radii_plan[f] is not None and radii_plan[f] >= math.sqrt(60 * 2300))
    f_ring = int(4.05 * fps) - 1
    ring_end, ring_start = fr[f_ring], fr[int(3.0 * fps)]
    p_end = (f_ring / fps - 3.65) / 0.45
    planned_d = 2 * 300 * (1 - (1 - .14) * eIn(p_end)) / sc
    path = jw(wd / "iris.json", {"measured_r": meas_r, "planned_r": radii_plan})
    lin_mid = (60 + 2300) / 2
    d_end = blob_x(ring_end, thr=150)["x1"] - blob_x(ring_end, thr=150)["x0"] + 1
    d_start = blob_x(ring_start, thr=150)["x1"] - blob_x(ring_start, thr=150)["x0"] + 1
    checks = [check("ring shrinks on E.in toward scale .14 (measured = planned diameter)", abs(d_end - planned_d) <= 3 and d_end < d_start - 10,
                    [d_start, d_end, planned_d], "shrinking, = plan"),
              check("ring scale formula lands on .14 with stroke 60", abs((1 - (1 - .14) * eIn(1)) - .14) < 1e-12 and 6 + 54 * eIn(1) == 60, .14, .14),
              check("iris opens from r 60 at 4.05 s", abs(meas_r[int(4.05 * fps) + 1] - 60) < 25, meas_r[int(4.05 * fps) + 1], 60),
              check("log-space: geometric mean radius (371) reached before half the linear distance", radii_plan[f_mid] < lin_mid and
                    abs(meas_r[f_mid] - radii_plan[f_mid]) < 0.1 * radii_plan[f_mid], [meas_r[f_mid], radii_plan[f_mid]], "~371"),
              check("frame flooded with the brand colour at the end", brand(fr[-1]).mean() > 0.99, float(brand(fr[-1]).mean()), 1.0),
              check("negative control: before the iris there is no flood", brand(fr[int(3.0 * fps)]).mean() < 0.01, float(brand(fr[int(3.0 * fps)]).mean()), 0)]
    return checks, [mp4, path]


@card("SHAPE-39")
def motion_along_path(task, wd):
    d = "M 40 300 C 140 40, 360 40, 460 300 S 760 520, 860 260"
    body = '<svg width=900 height=560><path id=route d="%s" fill=none stroke=#888 /><g id=plane><rect x=-10 y=-4 width=20 height=8 /></g></svg>' % d
    js = """gsap.registerPlugin(MotionPathPlugin); const path=$('#route'), L=path.getTotalLength(); const pl=$('#plane');
const o={x:0,y:0,rotation:0}; const tl=gsap.timeline({paused:true}); tl.to(o,{motionPath:{path:'#route',autoRotate:true},duration:2,ease:'power1.inOut'});
tl.seek(2); const S=[]; for(let i=0;i<=20;i++){tl.seek(i?2*i/20:1e-6); S.push([o.x,o.y,o.rotation]); pl.setAttribute('transform','translate('+o.x+' '+o.y+') rotate('+o.rotation+')');}
const dense=[]; for(let i=0;i<=2000;i++){const p=path.getPointAtLength(L*i/2000); dense.push([p.x,p.y]);}
const free=[]; for(let i=0;i<=20;i++){const e=gsap.parseEase('power1.inOut')(i/20); const a=path.getPointAtLength(L*e), b=path.getPointAtLength(Math.min(L,L*e+0.5)), c=path.getPointAtLength(Math.max(0,L*e-0.5));
 free.push([a.x,a.y,Math.atan2(b.y-c.y,b.x-c.x)*180/Math.PI]);}
R({S,dense,free,L});"""
    r = kit_page(wd, "motionpath", body, js, plugins=("MotionPathPlugin",))
    dense = r["dense"]
    off = max(min(math.hypot(x - a, y - b) for a, b in dense) for x, y, _ in r["S"])
    dang = max(abs(((a[2] - b[2]) + 180) % 360 - 180) for a, b in zip(r["S"][1:-1], r["free"][1:-1]))
    dpos = max(math.hypot(a[0] - b[0], a[1] - b[1]) for a, b in zip(r["S"], r["free"]))
    lin = [(40 + (860 - 40) * i / 20, 300 + (260 - 300) * i / 20) for i in range(21)]
    loff = max(min(math.hypot(x - a, y - b) for a, b in dense) for x, y in lin)
    path = jw(wd / "motion_path.json", {k: v for k, v in r.items() if k != "dense"})
    checks = [check("plugin keeps the element on the path", off < 1.0, off, "<1 px"),
              check("autoRotate follows the tangent", dang < 2.0, dang, "<2 deg"),
              check("plugin-free sampler (getPointAtLength + atan2) agrees", dpos < 3.0, dpos, "<3 px"),
              check("ends on the path end", math.hypot(r["S"][-1][0] - 860, r["S"][-1][1] - 260) < 1, r["S"][-1][:2], [860, 260]),
              check("negative control: a straight lerp leaves the path", loff > 50, loff, ">50")]
    return checks, [path]


def vnoise3(p, seed=7):
    """Smooth 3-D value noise (quintic-faded trilinear lattice), deterministic, in -1..1."""
    import numpy as np
    p = np.asarray(p, dtype=float)
    i = np.floor(p).astype(np.int64)
    f = p - i
    u = f * f * f * (f * (f * 6 - 15) + 10)

    def h(ix, iy, iz):
        n = (ix * 374761393 + iy * 668265263 + iz * 2147483647 + seed * 144665) & 0xFFFFFFFF
        n = (n ^ (n >> 13)) * 1274126177 & 0xFFFFFFFF
        return ((n ^ (n >> 16)) & 0xFFFF) / 32767.5 - 1.0
    out = 0
    for dx in (0, 1):
        for dy in (0, 1):
            for dz in (0, 1):
                w = (u[..., 0] if dx else 1 - u[..., 0]) * (u[..., 1] if dy else 1 - u[..., 1]) * (u[..., 2] if dz else 1 - u[..., 2])
                out = out + w * h(i[..., 0] + dx, i[..., 1] + dy, i[..., 2] + dz)
    return out


def sphere_mesh(nu=48, nv=24):
    import numpy as np
    th = np.linspace(0, 2 * np.pi, nu, endpoint=False)
    ph = np.linspace(0.05, np.pi - 0.05, nv)
    T, P = np.meshgrid(th, ph)
    return np.stack([np.sin(P) * np.cos(T), np.cos(P), np.sin(P) * np.sin(T)], axis=-1).reshape(-1, 3)


@card("SHAPE-30")
def noise_blob(task, wd):
    import numpy as np
    pos = sphere_mesh()
    nrm = pos / np.linalg.norm(pos, axis=1, keepdims=True)
    inten = 0.2

    def blob(t):
        disp = vnoise3(pos * 1.5 + t * 0.5)
        return pos + nrm * disp[:, None] * inten
    a = blob(1.3)
    _ = blob(0.7)
    b = blob(1.3)
    c = blob(1.3 + 1 / 30)
    r = np.linalg.norm(a, axis=1)
    imgs = []
    for f in range(30):
        q = blob(f / 30)
        im, d = canvas(160, 160)
        light = np.clip((q / np.linalg.norm(q, axis=1, keepdims=True)) @ np.array([-.5, .6, .62]), 0, 1)
        for (x, y, z), l in sorted(zip(q.tolist(), light.tolist()), key=lambda k: k[0][2]):
            d.point((80 + 55 * x, 80 - 55 * y), fill=(int(80 + 170 * l),) * 3)
        imgs.append(np.asarray(im))
    mp4 = write_mp4(wd / "blob.mp4", imgs, 30)
    path = jw(wd / "blob.json", {"r_min": float(r.min()), "r_max": float(r.max()), "r_std": float(r.std())})
    plain = np.linalg.norm(pos, axis=1)
    checks = [check("displacement along normals bounded by intensity .2", float(np.abs(r - 1).max()) <= inten + 1e-9, float(np.abs(r - 1).max()), "<=0.2"),
              check("surface is alive (radius varies)", float(r.std()) > 0.02, float(r.std()), ">0.02"),
              check("pure function of seek time: same t -> identical vertices", float(np.abs(a - b).max()) == 0.0, float(np.abs(a - b).max()), 0),
              check("coherent in time (next frame moves a little)", 0 < float(np.abs(c - a).max()) < 0.05, float(np.abs(c - a).max()), "(0, 0.05)"),
              check("negative control: the undisplaced sphere is not alive", float(plain.std()) < 1e-9, float(plain.std()), ">0.02")]
    return checks, [mp4, path]


def sd_circle(x, y, cx, cy, r):
    import numpy as np
    return np.hypot(x - cx, y - cy) - r


def sd_box(x, y, cx, cy, hx, hy):
    import numpy as np
    qx, qy = np.abs(x - cx) - hx, np.abs(y - cy) - hy
    return np.hypot(np.maximum(qx, 0), np.maximum(qy, 0)) + np.minimum(np.maximum(qx, qy), 0)


def smin(a, b, k):
    import numpy as np
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0, 1)
    return b * (1 - h) + a * h - k * h * (1 - h)


@card("SHAPE-31")
def sdf_2d(task, wd):
    import numpy as np
    from PIL import Image
    n = 256
    y, x = np.mgrid[0:n, 0:n] / n * 2 - 1
    c = sd_circle(x, y, -0.25, 0, 0.35)
    b = sd_box(x, y, 0.3, 0, 0.25, 0.25)
    k = 0.2
    u = smin(c, b, k)
    hard = np.minimum(c, b)
    morph = lambda t: c * (1 - t) + b * t
    w = 0.01
    outline = np.abs(u) < w
    glow = np.exp(-np.maximum(u, 0) * 8)
    img = np.stack([(u < 0) * 200 + outline * 55, glow * 200, outline * 255], axis=2).clip(0, 255).astype(np.uint8)
    Image.fromarray(img).save(wd / "sdf.png")
    seam = (abs(c - b) < 0.01) & (np.abs(y) < 0.05) & (hard < 0.1)
    path = jw(wd / "sdf.json", {"seam_gap": float((hard - u)[seam].max()) if seam.any() else None})
    checks = [check("circle SDF exact: d(centre) = -r, d on rim = 0", abs(float(sd_circle(-0.25, 0, -0.25, 0, 0.35)) + 0.35) < 1e-12 and
                    abs(float(sd_circle(0.1, 0, -0.25, 0, 0.35))) < 1e-12, float(sd_circle(-0.25, 0, -0.25, 0, 0.35)), -0.35),
              check("box SDF exact at a corner distance", abs(float(sd_box(0.65, 0.35, 0.3, 0, 0.25, 0.25)) - math.hypot(0.1, 0.1)) < 1e-12,
                    float(sd_box(0.65, 0.35, 0.3, 0, 0.25, 0.25)), math.hypot(0.1, 0.1)),
              check("smooth union <= hard union everywhere", bool((u <= hard + 1e-12).all()), True, True),
              check("smooth union bulges by k/4 where the fields meet", seam.any() and abs(float((hard - u)[seam].max()) - k / 4) < 0.01,
                    float((hard - u)[seam].max()) if seam.any() else None, k / 4),
              check("morph mix: t=0 is A, t=1 is B", np.abs(morph(0) - c).max() == 0 and np.abs(morph(1) - b).max() == 0, 0, 0),
              check("circle outline band = perimeter x 2w (pixels)", abs((np.abs(c) < w).sum() / (2 * math.pi * 0.35 * 2 * w * (n / 2) ** 2) - 1) < 0.1,
                    int((np.abs(c) < w).sum()), 2 * math.pi * 0.35 * 2 * w * (n / 2) ** 2),
              check("glow decays with distance", float(glow[n // 2, n - 1]) < float(glow[n // 2, int(n * 0.83)]) < 1.0001, [float(glow[n // 2, n - 1]), float(glow[n // 2, int(n * .83)])], "decreasing"),
              check("negative control: hard min has no bulge at the seam", float((hard - hard)[seam].max()) < k / 8, 0.0, k / 4)]
    return checks, [wd / "sdf.png", path]


def mesh_stats(pos, idx):
    import numpy as np
    P = np.asarray(pos, dtype=float).reshape(-1, 3)
    F = np.asarray(idx, dtype=np.int64).reshape(-1, 3)
    a, b, c = P[F[:, 0]], P[F[:, 1]], P[F[:, 2]]
    vol = abs(float(np.einsum("ij,ij->i", a, np.cross(b, c)).sum() / 6))
    ar = float(np.linalg.norm(np.cross(b - a, c - a), axis=1).sum() / 2)
    e = np.sort(np.concatenate([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]), axis=1)
    _, counts = np.unique(e, axis=0, return_counts=True)
    return vol, ar, int((counts == 1).sum()), int((counts > 2).sum())


@card("SHAPE-32")
def sdf_sculpt_mesh(task, wd):
    import numpy as np
    r = shape_kit(wd, "sculpt", """const S=K3S.sculpt().sphere([0,0,0],.1,{color:'#ffffff'}); const g=S.mesh({cells:120});
const T=K3S.sculpt().sphere([-.05,0,0],.06).sphere([.05,0,0],.06,{k:.02}).box([0,-.06,0],[.04,.02,.04],.005,{k:.01}); const h=T.mesh({cells:80});
out({p:Array.from(g.attributes.position.array), i:Array.from(g.index.array), st:g.userData.stats, p2:Array.from(h.attributes.position.array), i2:Array.from(h.index.array)});""")
    vol, ar, open_e, nonman = mesh_stats(r["p"], r["i"])
    v2, a2, o2, n2 = mesh_stats(r["p2"], r["i2"])
    np.savez_compressed(wd / "sphere_mesh.npz", p=np.asarray(r["p"], dtype=np.float32), i=np.asarray(r["i"], dtype=np.int32))
    R = 0.1
    st = r["st"]
    pts = np.asarray(r["p"]).reshape(-1, 3)
    rad_err = float(np.abs(np.linalg.norm(pts, axis=1) - R).max())
    path = jw(wd / "sculpt.json", {"volume": vol, "area": ar, "open_edges": open_e, "stats": st, "blob": [v2, a2, o2, n2]})
    checks = [check("sphere volume within 2%", abs(vol / (4 / 3 * math.pi * R ** 3) - 1) < 0.02, vol / (4 / 3 * math.pi * R ** 3), 1),
              check("sphere area within 3%", abs(ar / (4 * math.pi * R * R) - 1) < 0.03, ar / (4 * math.pi * R * R), 1),
              check("vertices on the true surface (radius error < 1e-3)", rad_err < 1e-3, rad_err, "<1e-3"),
              check("watertight: 0 open edges, manifold", open_e == 0 and nonman == 0, [open_e, nonman], [0, 0]),
              check("coarse-to-fine: evaluations < 60% of the full grid", st["evals"] < 0.6 * st["full"], st["evals"] / st["full"], "<0.6"),
              check("smooth-union sculpt also closed", o2 == 0 and v2 > 0, o2, 0)]
    half = np.asarray(r["i"]).reshape(-1, 3)[: len(r["i"]) // 6]
    _, _, open_half, _ = mesh_stats(r["p"], half.reshape(-1))
    checks.append(check("negative control: a cut-open mesh shows open edges", open_half > 0, open_half, ">0"))
    return checks, [wd / "sphere_mesh.npz", path]


@card("SHAPE-33")
def smooth_csg(task, wd):
    r = shape_kit(wd, "csg", """const k=.02;
const A=K3S.sculpt().sphere([0,0,0],.1,{color:'#ffffff'}).sphere([.1,0,0],.06,{op:'sub',k:.01,color:'#ff0000'});
const U=K3S.sculpt().sphere([-.05,0,0],.06).sphere([.05,0,0],.06,{k:k}); const H=K3S.sculpt().sphere([-.05,0,0],.06).sphere([.05,0,0],.06,{k:1e-6});
const I=K3S.sculpt().sphere([-.03,0,0],.06).sphere([.03,0,0],.06,{op:'and',k:1e-6});
const cav=A.hit([.3,0,0],[-1,0,0]); out({cav, ccol:A.colorAt(...cav.point), plain:A.colorAt(-.1,0,0), u0:U.dist(0,0,0), h0:H.dist(0,0,0), i0:I.dist(0,0,0),
 sub_in:A.dist(.08,0,0), mesh:(()=>{const g=A.mesh({cells:70}); return g.index.count;})()});""")
    k = 0.02
    d1 = math.hypot(0.05, 0) - 0.06
    expected_u = d1 - k * 0.25
    path = jw(wd / "csg.json", r)
    checks = [check("smooth union at the seam = min - k/4 (h = .5)", abs(r["u0"] - expected_u) < 1e-4, r["u0"], expected_u),
              check("k -> 0 recovers the hard union", abs(r["h0"] - d1) < 1e-4, r["h0"], d1),
              check("intersection (and) = max of the fields", abs(r["i0"] - (math.hypot(0.03, 0) - 0.06)) < 1e-4, r["i0"], math.hypot(.03, 0) - .06),
              check("subtraction carves (point inside the cut is outside the solid)", r["sub_in"] > 0, r["sub_in"], ">0"),
              check("carved cavity tinted red 1.0", abs(r["ccol"][0] - 1) < 0.05 and r["ccol"][1] < 0.05 and r["ccol"][2] < 0.05, r["ccol"], [1, 0, 0]),
              check("plain side keeps the base colour (no red tint)", abs(r["plain"][1] - 1) < 0.05, r["plain"], [1, 1, 1]),
              check("carved shape meshes", r["mesh"] > 0, r["mesh"], ">0"),
              check("negative control: without the smooth blend there is no k/4 bulge", abs(r["h0"] - expected_u) > k * 0.2, r["h0"], expected_u)]
    return checks, [path]


@card("SHAPE-34")
def field_queries(task, wd):
    r = shape_kit(wd, "field", """const S=K3S.sculpt().ellipsoid([0,0,0],[.07,.08,.065],{color:'#f6efe8'});
const hit=S.hit([0,.02,1],[0,0,-1]); const nd=S.dist(...hit.point); const prr=S.project([.2,.1,.05]); const pr=prr.point||prr; const pd=S.dist(...pr);
const g=S.grad? S.grad(...hit.point):null; out({hit, nd, pr, pd, d0:S.dist(0,.02,1), g});""")
    n = r["hit"]["normal"]
    nl = math.sqrt(sum(v * v for v in n))
    eye = {"position": r["hit"]["point"], "forward": n}
    path = jw(wd / "eye_placement.json", {"eye": eye, "query": r})
    p = r["hit"]["point"]
    checks = [check("frontal ray meets the face on the surface (|d| < 1e-3)", abs(r["nd"]) < 1e-3, r["nd"], 0),
              check("hit point is in front (z ~ .065 at y=.02)", abs(p[2] - 0.065 * math.sqrt(1 - (0.02 / 0.08) ** 2)) < 2e-3, p[2],
                    0.065 * math.sqrt(1 - (0.02 / .08) ** 2)),
              check("normal is unit and faces the ray origin", abs(nl - 1) < 1e-6 and n[2] > 0.9, [nl, n[2]], [1, ">0.9"]),
              check("project() lands a point on the surface", abs(r["pd"]) < 2e-3, r["pd"], 0),
              check("negative control: the ray origin itself is far off the surface", abs(r["d0"]) > 0.5, r["d0"], ">0.5")]
    return checks, [path]


@card("SHAPE-38")
def press_ripple(task, wd):
    import numpy as np
    W = H = 160
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    dots = ((xx % 10 < 2) & (yy % 10 < 2)).astype(float)
    cx = cy = 80.0

    def frame(t, on=True):
        r = 120 * (t / 0.9)
        dist = np.hypot(xx - cx, yy - cy) + 1e-9
        band = np.exp(-((dist - r) / 8) ** 2) if on else 0 * dist
        push = 0.18 * 40 * band  # displacement .18 of the ring band (40 px) outward
        sx = xx - (xx - cx) / dist * push
        sy = yy - (yy - cy) / dist * push
        ix = np.clip(np.round(sx).astype(int), 0, W - 1)
        iy = np.clip(np.round(sy).astype(int), 0, H - 1)
        base = dots[iy, ix] * 200
        heat = 0.55 * band * 255
        return np.stack([np.clip(base + heat, 0, 255), np.clip(base + heat * 0.55, 0, 255), base], axis=2).astype(np.uint8), push
    imgs = [frame(f / 30)[0] for f in range(28)]
    mp4 = write_mp4(wd / "ripple.mp4", imgs, 30)
    fr, push = frame(0.45)
    plain, _ = frame(0.45, False)
    ring_r = 60
    warm = fr[80, 80 + ring_r, 0] - fr[80, 80 + ring_r, 2]
    diff_ring = float(np.abs(fr.astype(float) - plain.astype(float))[:, :, 2][np.abs(np.hypot(xx - cx, yy - cy) - ring_r) < 6].mean())
    far = float(np.abs(fr.astype(float) - plain.astype(float))[:, :, 2][np.hypot(xx - cx, yy - cy) < 20].mean())
    path = jw(wd / "ripple.json", {"max_push_px": float(push.max()), "warm": float(warm)})
    checks = [check("displacement peak = .18 x band", abs(float(push.max()) - 0.18 * 40) < 0.05, float(push.max()), 7.2),
              check("ring radius grows linearly over .9 s (60 px at .45 s)", abs(120 * 0.45 / 0.9 - ring_r) < 1e-9, ring_r, 60),
              check("pixels on the ring are shoved (dot grid moved)", diff_ring > 10, diff_ring, ">10"),
              check("centre untouched", far < 1, far, "<1"),
              check("heat .55 adds a warm bloom on the ring", warm > 100, float(warm), ">100"),
              check("negative control: without the ripple nothing moves", float(np.abs(plain.astype(float) - frame(0.45, False)[0]).max()) == 0 and
                    float(frame(0.45, False)[1].max()) == 0, 0, 7.2)]
    return checks, [mp4, path]


def catmull(points, n=10, closed=False):
    P = list(points)
    if closed:
        P = [P[-1]] + P + [P[0], P[1]]
    else:
        P = [P[0]] + P + [P[-1]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 +
                                    (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in range(2)))
    out.append(tuple(P[-2]))
    return out


def arc_table(samples):
    acc = [0.0]
    for a, b in zip(samples, samples[1:]):
        acc.append(acc[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    return acc


def at_distance(samples, acc, s):
    import bisect
    i = min(len(acc) - 2, max(0, bisect.bisect_right(acc, s) - 1))
    u = (s - acc[i]) / (acc[i + 1] - acc[i]) if acc[i + 1] > acc[i] else 0
    a, b = samples[i], samples[i + 1]
    return (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)


@card("SHAPE-40")
def arc_length_speed(task, wd):
    import numpy as np
    way = [(20, 150), (60, 30), (100, 140), (220, 40), (300, 160)]
    curve = catmull(way, n=1000)
    acc = arc_table(curve)
    L = acc[-1]
    N = 60
    const = [at_distance(curve, acc, L * k / N) for k in range(N + 1)]
    naive = [curve[round(k / N * (len(curve) - 1))] for k in range(N + 1)]
    C = np.asarray(curve)
    A = np.asarray(acc)

    def step(pts):  # distance travelled along the curve, measured by projecting each point back onto the dense curve
        s_ = [float(A[int(np.argmin(np.hypot(C[:, 0] - x, C[:, 1] - y)))]) for x, y in pts]
        return np.diff(s_)
    sc, sn = step(const), step(naive)
    seg = 1000
    def turn(k):
        a = np.subtract(curve[k], curve[k - 1])
        b = np.subtract(curve[k + 1], curve[k])
        return float(np.degrees(np.arccos(np.clip(np.dot(a, b) / np.linalg.norm(a) / np.linalg.norm(b), -1, 1))))
    tang = [turn(i * seg) / max(1e-9, (turn(i * seg - 1) + turn(i * seg + 1)) / 2) for i in range(1, len(way) - 1)]
    path = jw(wd / "arc_length.json", {"L": L, "const_steps_cv": float(sc.std() / sc.mean()), "naive_cv": float(sn.std() / sn.mean())})
    imgs = []
    for k in range(N + 1):
        im, d = canvas(320, 180)
        d.line(curve, fill=(80, 80, 90))
        x, y = const[k]
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(240, 200, 90))
        imgs.append(np.asarray(im))
    mp4 = write_mp4(wd / "constant_speed.mp4", imgs, 30)
    checks = [check("curve passes through every waypoint (C0)", all(min(math.hypot(p[0] - w[0], p[1] - w[1]) for p in curve) < 1e-9 for w in way), 0, 0),
              check("C1: no tangent kink at the waypoints (turn there ~ neighbours)", max(tang) < 1.5, max(tang), "<1.5x"),
              check("arc-length table gives constant speed (cv < 1%)", float(sc.std() / sc.mean()) < 0.01, float(sc.std() / sc.mean()), "<0.01"),
              check("negative control: uniform-t sampling varies in speed", float(sn.std() / sn.mean()) > 0.1, float(sn.std() / sn.mean()), ">0.1")]
    return checks, [mp4, path]


def _tokens(d):
    """SVG path tokenizer that understands glued arc flags (e.g. 'a20 20 0 0110 10')."""
    import re
    out, i, cmd, argi = [], 0, None, 0
    num = re.compile(r"[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?")
    while i < len(d):
        c = d[i]
        if c.isalpha():
            cmd, argi = c, 0
            out.append(c)
            i += 1
            continue
        if c in " ,\t\n":
            i += 1
            continue
        if cmd in "aA" and argi % 7 in (3, 4):
            out.append(float(c))
            argi += 1
            i += 1
            continue
        m = num.match(d, i)
        if not m:
            raise ValueError("bad path data at %d" % i)
        out.append(float(m.group()))
        argi += 1
        i = m.end()
    return out


def _arc(p0, rx, ry, phi, fa, fs, p1):
    """SVG endpoint arc -> centre parameterisation, sampled max(4, |dtheta|/2pi*64) points (excluding p0)."""
    x1, y1 = p0
    x2, y2 = p1
    if rx == 0 or ry == 0:
        return [p1]
    cp, sp = math.cos(math.radians(phi)), math.sin(math.radians(phi))
    dx, dy = (x1 - x2) / 2, (y1 - y2) / 2
    x1p, y1p = cp * dx + sp * dy, -sp * dx + cp * dy
    rx, ry = abs(rx), abs(ry)
    lam = x1p ** 2 / rx ** 2 + y1p ** 2 / ry ** 2
    if lam > 1:
        rx, ry = rx * math.sqrt(lam), ry * math.sqrt(lam)
    num = rx * rx * ry * ry - rx * rx * y1p * y1p - ry * ry * x1p * x1p
    den = rx * rx * y1p * y1p + ry * ry * x1p * x1p
    co = math.sqrt(max(0, num / den)) * (-1 if fa == fs else 1)
    cxp, cyp = co * rx * y1p / ry, -co * ry * x1p / rx
    cx, cy = cp * cxp - sp * cyp + (x1 + x2) / 2, sp * cxp + cp * cyp + (y1 + y2) / 2
    ang = lambda ux, uy, vx, vy: math.atan2(ux * vy - uy * vx, ux * vx + uy * vy)
    t1 = ang(1, 0, (x1p - cxp) / rx, (y1p - cyp) / ry)
    dt = ang((x1p - cxp) / rx, (y1p - cyp) / ry, (-x1p - cxp) / rx, (-y1p - cyp) / ry)
    if not fs and dt > 0:
        dt -= 2 * math.pi
    elif fs and dt < 0:
        dt += 2 * math.pi
    n = max(4, int(abs(dt) / (2 * math.pi) * 64))
    pts = []
    for k in range(1, n + 1):
        t = t1 + dt * k / n
        pts.append((cx + rx * math.cos(t) * cp - ry * math.sin(t) * sp, cy + rx * math.cos(t) * sp + ry * math.sin(t) * cp))
    pts[-1] = p1
    return pts


def parse_path(d, n=14):
    """M L H V C S Q T A Z (absolute/relative, smooth reflections, glued arc flags) -> one polyline per subpath."""
    tk = _tokens(d)
    polys, cur, start = [], None, (0.0, 0.0)
    x = y = 0.0
    lastc = lastq = None
    i, cmd = 0, None
    counts = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "S": 4, "Q": 4, "T": 2, "A": 7, "Z": 0}
    while i < len(tk):
        if isinstance(tk[i], str):
            cmd = tk[i]
            i += 1
            if cmd in "zZ":
                if cur:
                    cur.append(start)
                    polys.append(cur)
                cur, (x, y) = None, start
                lastc = lastq = None
                continue
        C = cmd.upper()
        rel = cmd.islower()
        a = tk[i:i + counts[C]]
        i += counts[C]
        ox, oy = (x, y) if rel else (0.0, 0.0)
        if C == "M":
            if cur:
                polys.append(cur)
            x, y = a[0] + ox, a[1] + oy
            start, cur = (x, y), [(x, y)]
            cmd = "l" if rel else "L"
            lastc = lastq = None
            continue
        if cur is None:
            cur = [(x, y)]
        if C == "L":
            x, y = a[0] + ox, a[1] + oy
            cur.append((x, y))
            lastc = lastq = None
        elif C == "H":
            x = a[0] + (ox if rel else 0)
            cur.append((x, y))
            lastc = lastq = None
        elif C == "V":
            y = a[0] + (oy if rel else 0)
            cur.append((x, y))
            lastc = lastq = None
        elif C in "CS":
            if C == "C":
                c1 = (a[0] + ox, a[1] + oy)
                c2, e = (a[2] + ox, a[3] + oy), (a[4] + ox, a[5] + oy)
            else:
                c1 = (2 * x - lastc[0], 2 * y - lastc[1]) if lastc else (x, y)
                c2, e = (a[0] + ox, a[1] + oy), (a[2] + ox, a[3] + oy)
            p0 = (x, y)
            for k in range(1, n + 1):
                t = k / n
                mt = 1 - t
                cur.append((mt ** 3 * p0[0] + 3 * mt * mt * t * c1[0] + 3 * mt * t * t * c2[0] + t ** 3 * e[0],
                            mt ** 3 * p0[1] + 3 * mt * mt * t * c1[1] + 3 * mt * t * t * c2[1] + t ** 3 * e[1]))
            x, y = e
            lastc, lastq = c2, None
        elif C in "QT":
            if C == "Q":
                q, e = (a[0] + ox, a[1] + oy), (a[2] + ox, a[3] + oy)
            else:
                q = (2 * x - lastq[0], 2 * y - lastq[1]) if lastq else (x, y)
                e = (a[0] + ox, a[1] + oy)
            p0 = (x, y)
            for k in range(1, n + 1):
                t = k / n
                mt = 1 - t
                cur.append((mt * mt * p0[0] + 2 * mt * t * q[0] + t * t * e[0], mt * mt * p0[1] + 2 * mt * t * q[1] + t * t * e[1]))
            x, y = e
            lastq, lastc = q, None
        elif C == "A":
            e = (a[5] + ox, a[6] + oy)
            cur.extend(_arc((x, y), a[0], a[1], a[2], int(a[3]), int(a[4]), e))
            x, y = e
            lastc = lastq = None
    if cur:
        polys.append(cur)
    return polys


@card("SHAPE-41")
def svg_path_parser(task, wd):
    d = ("M10 10 h50 v30 H20 Z m80 -10 c10-20 30-20 40 0 s30 20 40 0 q20-30 40 0 t40 0 "
         "a20 20 0 1 1 20 20 A15 15 0 0110 120 l-10-10z M300 150 Q320 120 340 150 T380 150 C 390 170 410 170 420 150 S 450 130 460 150")
    polys = parse_path(d, n=14)
    polys64 = parse_path(d, n=64)
    r = kit_page(wd, "pathref", '<svg width=500 height=300><path id=p d="%s" fill=none /></svg>' % d,
                 """const p=$('#p'), L=p.getTotalLength(); const D=[]; for(let i=0;i<=6000;i++){const q=p.getPointAtLength(L*i/6000); D.push([q.x,q.y]);}
R({L, D, end:D[D.length-1]});""")
    import numpy as np
    D = np.asarray(r["D"])
    allv = np.asarray([p for poly in polys for p in poly])
    off = float(np.min(np.hypot(D[None, :, 0] - allv[:, None, 0], D[None, :, 1] - allv[:, None, 1]), axis=1).max())
    length = lambda ps: sum(math.hypot(b[0] - a[0], b[1] - a[1]) for poly in ps for a, b in zip(poly, poly[1:]))
    L64 = length(polys64)
    closed = [abs(p[0][0] - p[-1][0]) < 1e-9 and abs(p[0][1] - p[-1][1]) < 1e-9 for p in polys]
    path = jw(wd / "parsed.json", {"subpaths": [len(p) for p in polys], "chrome_length": r["L"], "parsed_length_n64": L64})
    poly_png(wd / "parsed.png", [[(x, y) for x, y in p] for p in polys], size=(500, 300))
    naive = parse_path(d.replace("m80", "M80").replace("c10", "C10").replace("s30", "S30"), n=14)
    nv = np.asarray([p for poly in naive for p in poly])
    noff = float(np.min(np.hypot(D[None, :, 0] - nv[:, None, 0], D[None, :, 1] - nv[:, None, 1]), axis=1).max())
    checks = [check("3 subpaths (two closed with Z)", len(polys) == 3 and closed[:2] == [True, True], [len(polys), closed], [3, "closed"]),
              check("every parsed vertex lies on Chrome's own path", off < 0.6, off, "<0.6 px"),
              check("total length matches Chrome getTotalLength (n=64)", abs(L64 - r["L"]) / r["L"] < 0.003, [L64, r["L"]], "within 0.3%"),
              check("ends where Chrome ends", math.hypot(polys[-1][-1][0] - r["end"][0], polys[-1][-1][1] - r["end"][1]) < 0.01, polys[-1][-1], r["end"]),
              check("glued arc flags parsed ('0110' = 0,1,10)", _tokens("a15 15 0 0110 120")[1:] == [15, 15, 0, 0, 1, 10, 120], _tokens("a15 15 0 0110 120")[1:],
                    [15, 15, 0, 0, 1, 10, 120]),
              check("negative control: treating relative commands as absolute leaves the path", noff > 20, noff, ">20")]
    return checks, [path, wd / "parsed.png"]


def circle_pts(cx, cy, r, n=96, rev=False):
    pts = [(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n)) for k in range(n)]
    return pts[::-1] if rev else pts


def bridge(outer, inner):
    """One polygon: outer ring, a zero-width bridge to the inner ring (reversed) and back, so even-odd fill cancels the bridge."""
    return outer + [outer[0]] + inner + [inner[0], outer[0]]


@card("SHAPE-42")
def even_odd_holes(task, wd):
    import numpy as np
    from PIL import Image, ImageDraw
    W = 200
    outer, inner = circle_pts(100, 100, 60, 192), circle_pts(100, 100, 30, 192, rev=True)
    im = Image.new("L", (W, W), 0)
    ImageDraw.Draw(im).polygon(bridge(outer, inner), fill=255)
    im2 = Image.new("L", (W, W), 0)
    d2 = ImageDraw.Draw(im2)
    d2.polygon(outer, fill=255)
    d2.polygon(inner, fill=0)  # a Hole polygon drawn after the shape it cuts
    naive = Image.new("L", (W, W), 0)
    dn = ImageDraw.Draw(naive)
    dn.polygon(outer, fill=255)
    dn.polygon(inner, fill=255)
    Image.merge("RGB", [im, im2, naive]).save(wd / "holes.png")
    a, a2, an = (np.asarray(x) > 127 for x in (im, im2, naive))
    exp = math.pi * (60 ** 2 - 30 ** 2)
    path = jw(wd / "holes.json", {"bridged_area": int(a.sum()), "hole_area": int(a2.sum()), "expected": exp})
    checks = [check("bridged compound: counter is empty", not a[100, 100] and a[100, 145], [bool(a[100, 100]), bool(a[100, 145])], [False, True]),
              check("ring area = pi (R^2 - r^2) within 2%", abs(a.sum() / exp - 1) < 0.02, int(a.sum()), exp),
              check("the bridge leaves no seam (row through the bridge stays a ring)", int(a[100, 100:160].sum()) <= 31 and int(a[100, 130:160].sum()) >= 29,
                    int(a[100, 130:160].sum()), "~30"),
              check("Hole polygon drawn after the shape erases the same area", abs(int(a2.sum()) - int(a.sum())) / exp < 0.02, int(a2.sum()), int(a.sum())),
              check("negative control: filling both subpaths loses the hole", bool(an[100, 100]) and abs(an.sum() / (math.pi * 3600) - 1) < 0.02,
                    bool(an[100, 100]), False)]
    return checks, [wd / "holes.png", path]


class Step:
    def __init__(self, name, ops, order="sweep", origin=(0, 0), weight=1.0):
        self.name, self.ops, self.order, self.origin, self.weight = name, ops, order, origin, weight


def render_steps(steps, W=1200, H=800, ss=3, upto=None):
    import numpy as np
    from PIL import Image, ImageDraw
    big = Image.new("RGB", (W * ss, H * ss), (244, 236, 220))
    d = ImageDraw.Draw(big)
    sx, sy = W * ss / 1200, H * ss / 800
    for st in steps[:upto]:
        for op in st.ops:
            kind = op[0]
            if kind == "ellipse":
                _, cx, cy, rx, ry, col = op
                pts = [(sx * (cx + rx * math.cos(2 * math.pi * k / 48)), sy * (cy + ry * math.sin(2 * math.pi * k / 48))) for k in range(48)]
                d.polygon(pts, fill=col)
            elif kind == "rect":
                _, x0, y0, x1, y1, col = op
                d.rectangle([sx * x0, sy * y0, sx * x1, sy * y1], fill=col)
            elif kind == "vgrad":
                _, y0, y1, c0, c1 = op
                for yy in range(int(sy * y0), int(sy * y1)):
                    u = (yy - sy * y0) / max(1, sy * (y1 - y0))
                    d.line([0, yy, W * ss, yy], fill=tuple(int(a + (b - a) * u) for a, b in zip(c0, c1)))
    return np.asarray(big.resize((W, H), Image.BOX))


def reveal_order(idx, W, step, scale=1.0, seed=1):
    import numpy as np
    rng = np.random.default_rng(seed)
    ys, xs = idx // W, idx % W
    o = step.order
    if o == "sweep":
        band = max(1, round(7 * scale))
        key = (ys // band) * 1e6 + np.where((ys // band) % 2 == 0, xs, -xs) + rng.random(len(idx)) * 26 * scale
    elif o == "grow":
        key = np.hypot(xs - step.origin[0], ys - step.origin[1]) + rng.random(len(idx)) * 9 * scale
    elif o in ("rise", "down", "left", "right"):
        base = {"rise": -ys, "down": ys, "left": -xs, "right": xs}[o]
        key = base + rng.random(len(idx)) * 7 * scale
    else:
        key = rng.random(len(idx))
    return idx[np.argsort(key, kind="stable")]


@card("SHAPE-43")
def step_scene_language(task, wd):
    import numpy as np
    from PIL import Image
    def build():
        return [Step("sky", [("vgrad", 0, 500, (120, 170, 230), (250, 220, 190))], "down"),
                Step("sun", [("ellipse", 900, 220, 90, 90, (255, 210, 90))], "grow", origin=(900, 220)),
                Step("ground", [("rect", 0, 500, 1200, 800, (90, 140, 80))], "rise"),
                Step("tree", [("ellipse", 300, 430, 110, 130, (40, 100, 60)), ("rect", 290, 520, 310, 640, (90, 60, 40))], "sparkle")]
    steps = build()
    full = render_steps(steps, 1200, 800, 3)
    half = render_steps(steps, 600, 400, 3)
    Image.fromarray(full).save(wd / "sheet_1200x800.png")
    down = np.asarray(Image.fromarray(full).resize((600, 400), Image.BOX), dtype=float)
    diff = float(np.abs(down - half).mean())
    edge = full[220, 980:1000, 0].astype(int)
    aa = int(((edge > 0) & (edge < 255) & (edge != edge[0]) & (edge != edge[-1])).sum())
    hard = render_steps(steps, 1200, 800, 1)[220, 980:1000, 0].astype(int)
    hard_aa = int(((hard != hard[0]) & (hard != hard[-1])).sum())
    perms = {}
    prev = render_steps(steps, 300, 200, 1, upto=1)
    for o in ("sweep", "grow", "rise", "down", "left", "right", "sparkle"):
        st = Step("x", [], o, origin=(150, 100))
        idx = np.arange(300 * 200)
        perm = reveal_order(idx, 300, st, 0.25)
        perms[o] = bool(np.array_equal(np.sort(perm), idx))
    path = jw(wd / "steps.json", {"steps": [s.name for s in steps], "resize_diff": diff, "aa_px": aa, "perms": perms})
    checks = [check("program renders at any size (600x400 == downscaled 1200x800)", diff < 2.0, diff, "<2"),
              check("ss=3 supersampling anti-aliases edges", aa >= 1, aa, ">=1"),
              check("every reveal order is a permutation of the step's pixels", all(perms.values()), perms, "all True"),
              check("steps draw in order (ground covers the sky below y=500)", tuple(full[700, 600]) == (90, 140, 80), tuple(int(v) for v in full[700, 600]), (90, 140, 80)),
              check("negative control: ss=1 leaves hard edges", hard_aa == 0, hard_aa, 0)]
    return checks, [wd / "sheet_1200x800.png", path]


@card("SHAPE-44")
def catmull_rom_curves(task, wd):
    from PIL import Image, ImageDraw
    pts = [(20, 100), (80, 20), (160, 120), (240, 40), (300, 110)]
    op = catmull(pts, n=10)
    cl = catmull(pts, n=10, closed=True)
    im = Image.new("RGB", (320, 140), (12, 14, 20))
    d = ImageDraw.Draw(im)
    d.line(op, fill=(240, 200, 90), width=2)
    d.line(cl, fill=(90, 200, 160), width=1)
    im.save(wd / "catmull.png")
    tan = [(op[10 * i + 1][0] - op[10 * i - 1][0], op[10 * i + 1][1] - op[10 * i - 1][1]) for i in range(1, 4)]
    exp = [(pts[i + 1][0] - pts[i - 1][0], pts[i + 1][1] - pts[i - 1][1]) for i in range(1, 4)]
    ang = lambda v: math.atan2(v[1], v[0])
    poly_turn = [abs(math.degrees(ang((pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])) - ang((pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]))))
                 for i in range(1, 4)]
    path = jw(wd / "catmull.json", {"open": op, "closed": cl})
    checks = [check("n=10 samples per segment (open: 4 x 10 + 1)", len(op) == 41, len(op), 41),
              check("passes through every control point", all(op[10 * i] == tuple(map(float, pts[i])) for i in range(5)), True, True),
              check("tangent at a point = (p[i+1] - p[i-1]) / 2", max(abs(ang(a) - ang(b)) for a, b in zip(tan, exp)) < 0.05,
                    max(abs(ang(a) - ang(b)) for a, b in zip(tan, exp)), "<0.05 rad"),
              check("closed curve returns to its start", len(cl) == 51 and cl[-1] == cl[0], len(cl), 51),
              check("negative control: the polyline kinks at the points", min(poly_turn) > 20, min(poly_turn), ">20 deg")]
    return checks, [wd / "catmull.png", path]


def tube_mask(spine, radii, W, H, discs=True, n=8):
    import numpy as np
    from PIL import Image, ImageDraw
    im = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(im)
    nrm = []
    for i in range(len(spine)):  # one normal per spine point (central difference), shared by both neighbouring quads
        (xa, ya), (xb, yb) = spine[max(0, i - 1)], spine[min(len(spine) - 1, i + 1)]
        L = math.hypot(xb - xa, yb - ya) or 1
        nrm.append((-(yb - ya) / L, (xb - xa) / L))
    for i in range(len(spine) - 1):
        (x0, y0), (x1, y1) = spine[i], spine[i + 1]
        (n0x, n0y), (n1x, n1y) = nrm[i], nrm[i + 1]
        r0, r1 = radii[i], radii[i + 1]
        d.polygon([(x0 + n0x * r0, y0 + n0y * r0), (x1 + n1x * r1, y1 + n1y * r1), (x1 - n1x * r1, y1 - n1y * r1), (x0 - n0x * r0, y0 - n0y * r0)], fill=255)
    if discs:
        for i in list(range(0, len(spine), max(1, n // 2))) + [len(spine) - 1]:
            r = radii[i]
            if r > 0.6:
                x, y = spine[i]
                d.ellipse([x - r, y - r, x + r, y + r], fill=255)
    return np.asarray(im) > 127


@card("SHAPE-45")
def variable_radius_tube(task, wd):
    import numpy as np
    from PIL import Image
    spine_ctrl = [(20, 160), (90, 40), (170, 160), (280, 50)]
    spine = catmull(spine_ctrl, n=8)
    radii = [6 + 10 * math.sin(math.pi * i / (len(spine) - 1)) for i in range(len(spine))]
    W, H = 300, 200
    m = tube_mask(spine, radii, W, H, True)
    q = tube_mask(spine, radii, W, H, False)
    Image.fromarray((np.stack([m, q, m], axis=2) * 255).astype(np.uint8)).save(wd / "tube.png")
    yy, xx = np.mgrid[0:H, 0:W]

    def coverage(mask):
        worst = 1.0
        for (x, y), r in zip(spine, radii):
            disk = np.hypot(xx - x, yy - y) <= 0.85 * r
            worst = min(worst, float(mask[disk].mean()))
        return worst
    cov, covq = coverage(m), coverage(q)
    wid = []
    for i in range(4, len(spine) - 4, 5):
        (x0, y0), (x1, y1) = spine[i - 1], spine[i + 1]
        L = math.hypot(x1 - x0, y1 - y0)
        nx, ny = -(y1 - y0) / L, (x1 - x0) / L
        x, y = spine[i]
        t = 0.0
        while t < 3 * radii[i] and m[int(round(y + ny * t)), int(round(x + nx * t))]:
            t += 0.25
        wid.append((t, radii[i]))
    path = jw(wd / "tube.json", {"coverage_with_discs": cov, "coverage_quads_only": covq})
    checks = [check("tight bends never punch holes (coverage 100% around every spine sample)", cov == 1.0, cov, 1.0),
              check("per-point radius respected (edge distance ~ r)", sorted(abs(dm - r) for dm, r in wid)[len(wid) // 2] <= 1.5, wid[:4], "~r"),
              check("negative control: quads alone leave gaps at the bends", covq < 1.0, covq, "<1")]
    return checks, [wd / "tube.png", path]


def ridge(seed, base, amp, rough=0.55, rounds=7, width=1.0, peaks=()):
    import numpy as np
    rng = np.random.default_rng(seed)
    ys = [base, base]
    offsets = []
    a = amp
    for _ in range(rounds):
        new, offs = [ys[0]], []
        for y0, y1 in zip(ys, ys[1:]):
            o = a * (rng.random() * 2 - 1)
            new += [(y0 + y1) / 2 + o, y1]
            offs.append(o)
        ys = new
        offsets.append(offs)
        a *= rough
    xs = [width * i / (len(ys) - 1) for i in range(len(ys))]
    ys = [y + sum(h * math.exp(-((x - px) / pw) ** 2) for px, h, pw in peaks) for x, y in zip(xs, ys)]
    return xs, ys, offsets


@card("SHAPE-46")
def mountain_ridges(task, wd):
    import numpy as np
    from PIL import Image, ImageDraw
    W, H = 320, 180
    layers = []
    for k in range(4):
        xs, ys, offs = ridge(10 + k, 0.45 + 0.1 * k, 0.18, 0.55, peaks=[(0.3, -0.12, 0.05)] if k == 0 else [])
        layers.append((xs, ys, offs))
    sky = np.array([230, 236, 245])
    ink = np.array([40, 50, 70])
    im = Image.new("RGB", (W, H), tuple(sky))
    d = ImageDraw.Draw(im)
    cols = []
    for k, (xs, ys, _) in enumerate(layers):  # far layers first, lighter with distance
        far = 3 - k
        col = tuple(int(v) for v in ink + (sky - ink) * far / 4.5)
        cols.append(col)
        d.polygon([(x * W, y * H) for x, y in zip(xs, ys)] + [(W, H), (0, H)], fill=col)
    im.save(wd / "ridges.png")
    xs, ys, offs = layers[0]
    ratios = [np.mean(np.abs(offs[r + 1])) / np.mean(np.abs(offs[r])) for r in range(3, 6)]
    again = ridge(10, 0.45, 0.18, 0.55, peaks=[(0.3, -0.12, 0.05)])[1]
    other = ridge(11, 0.45, 0.18, 0.55, peaks=[(0.3, -0.12, 0.05)])[1]
    lum = [sum(c) for c in cols]
    path = jw(wd / "ridges.json", {"points": len(xs), "amp_ratios": ratios, "layer_lum": lum})
    flat = [0.45] * len(xs)
    checks = [check("7 rounds -> 129 points", len(xs) == 129, len(xs), 129),
              check("amplitude x rough(.55) per round (measured)", all(abs(r - 0.55) < 0.12 for r in ratios), ratios, 0.55),
              check("seeded: same seed same ridge, new seed new ridge", again == ys and other != ys, True, True),
              check("carved peak raises the ridge at x=.3", min(ys[35:42]) < min(ys[60:]) , min(ys[35:42]), "< rest"),
              check("layers lighter with distance", lum[0] > lum[1] > lum[2] > lum[3], lum, "decreasing"),
              check("negative control: the undisplaced line is flat", max(flat) - min(flat) == 0 and max(ys) - min(ys) > 0.05, max(flat) - min(flat), ">0")]
    return checks, [wd / "ridges.png", path]


def quad_curve(p0, c, p1, n=40):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t * t * p1[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t * t * p1[1])
            for t in [k / n for k in range(n + 1)]]


@card("SHAPE-51")
def two_diagonal_lines(task, wd):
    import numpy as np
    from PIL import Image, ImageDraw
    from scipy import ndimage
    W, H = 320, 180

    def frame(phase, count=2):
        im = Image.new("L", (W, H), 0)
        d = ImageDraw.Draw(im)
        for k in ([0, 1] if count == 2 else [j / (count - 1) for j in range(count)]):
            ox = math.sin(.20 * phase + 2.3 * k) * .035 * W
            oy = math.cos(.16 * phase + k) * .02 * H
            pts = quad_curve((-.2 * W + .63 * W * k + ox, .93 * H + oy), (.30 * W + .41 * W * k + ox, .43 * H + oy),
                             (.65 * W + .5 * W * k + ox, -.10 * H + oy))
            d.line(pts, fill=128, width=3, joint="curve")
        return np.asarray(im)
    imgs = [np.stack([frame(f / 3)] * 3, axis=2) for f in range(60)]
    mp4 = write_mp4(wd / "two_lines.mp4", imgs, 30)
    fr = read_mp4(mp4, W, H)
    eight = np.ones((3, 3))
    counts = [ndimage.label(q[:, :, 0] > 40, structure=eight)[1] for q in fr]
    mids = [blob_x(frame(f / 3)[:, :160, None].repeat(3, 2).astype(float), thr=40)["cx"] for f in range(60)]
    three = ndimage.label(frame(0, 3) > 40, structure=eight)[1]
    path = jw(wd / "two_lines.json", {"components": counts, "drift_px": max(mids) - min(mids)})
    checks = [check("exactly two lines in every frame", set(counts) == {2}, sorted(set(counts)), [2]),
              check("lines drift (alive) within +-3.5% of width", 0.5 < max(mids) - min(mids) <= 2 * .035 * W + 1, max(mids) - min(mids), "<=22.4"),
              check("50% alpha stroke", int(frame(0).max()) == 128, int(frame(0).max()), 128),
              check("negative control: a three-line background fails the count", three == 3 and three != 2, three, 2)]
    return checks, [mp4, path]


@card("SHAPE-55")
def tile_flips_strip_loop(task, wd):
    import numpy as np
    W, H, fps = 240, 120, 30
    unit_w, gap, N = 40, 20, 5
    unit = unit_w + gap
    S = N * unit  # the repeat unit: the whole strip with its gaps
    cols = [(220, 120, 60), (90, 160, 220), (120, 200, 110), (230, 200, 80), (190, 90, 200)]

    def strip(t, span=S, T=10.0):
        a = np.zeros((40, W, 3), dtype=np.uint8)
        off = (t / T) * span  # exactly one repeat unit in 10 s, linear, two identical copies
        for copy in range(2):
            for k in range(N):
                x = int(round(k * unit - off + copy * span))
                if -unit_w < x < W:
                    a[5:35, max(0, x):max(0, min(W, x + unit_w))] = cols[k]
        return a

    def tiles(t):
        a = np.zeros((80, W, 3), dtype=np.uint8)
        for row in range(4):
            p = min(1, max(0, (t - row * 0.5) / 2)) if t < 4 else 1 - min(1, max(0, (t - 4 - row * 0.5) / 2))
            col = np.array([60, 90, 200]) * (1 - p) + np.array([230, 180, 70]) * p
            a[row * 20 + 2:row * 20 + 18, :] = col
        return a
    frames = [np.concatenate([strip(f / fps), tiles(f / fps * 0.8)], axis=0) for f in range(int(10 * fps))]
    mp4 = write_mp4(wd / "loops.mp4", frames[::3], 10)
    seam = float(np.abs(strip(10.0).astype(float) - strip(0.0)).mean())
    bad = float(np.abs(strip(10.0, span=N * unit_w).astype(float) - strip(0.0, span=N * unit_w)).mean())
    t2 = tiles(2.25)
    rows = [tuple(int(v) for v in t2[r * 20 + 10, 5]) for r in range(4)]
    back = tiles(8.0)
    path = jw(wd / "loops.json", {"strip_seam": seam, "miscounted_seam": bad, "rows_at_2_25s": rows})
    checks = [check("strip loop: frame at 10 s == frame at 0 (one unit incl. gap)", seam == 0.0, seam, 0),
              check("tile rows flip with a row delay (row 0 ahead of row 3)", rows[0][0] > rows[3][0], [rows[0][0], rows[3][0]], "row0 > row3"),
              check("tiles return to the first colour by 8 s", tuple(int(v) for v in back[10, 5]) == (60, 90, 200), tuple(int(v) for v in back[10, 5]), (60, 90, 200)),
              check("negative control: moving the tile width without its gap jumps at the seam", bad > 5, bad, ">5")]
    return checks, [mp4, path]


@card("SHAPE-62")
def integer_ratio_loops(task, wd):
    import numpy as np
    from PIL import Image, ImageDraw
    T, fps = 6.0, 30

    def frame(t, ratio=(1, 2)):
        im = Image.new("RGB", (160, 160), (10, 12, 18))
        d = ImageDraw.Draw(im)
        for k, (turns, r, col) in enumerate([(ratio[0], 60, (231, 182, 90)), (ratio[1], 40, (91, 209, 165))]):
            a = (360 * turns * t / T) % 360
            d.arc([80 - r, 80 - r, 80 + r, 80 + r], a, a + 120, fill=col, width=6)
        for j in range(12):  # MG-112: evenly spaced ticks, one turn in 6 s
            a = 2 * math.pi * (j / 12 + (t / T) % 1)
            d.line([80 + 70 * math.cos(a), 80 + 70 * math.sin(a), 80 + 76 * math.cos(a), 80 + 76 * math.sin(a)], fill=(200, 200, 200), width=2)
        return np.asarray(im, dtype=float)
    n = int(T * fps)
    imgs = [frame(f / fps).astype(np.uint8) for f in range(n)]  # t in [0, T): the seam frame is not exported twice
    mp4 = write_mp4(wd / "loop.mp4", imgs, fps)
    seam = float(np.abs(frame(T) - frame(0)).mean())
    dup = float(np.abs(frame((n - 1) / fps) - frame(0)).mean())
    bad = float(np.abs(frame(T, (1, 1.5)) - frame(0, (1, 1.5))).mean())
    nfr = len(read_mp4(mp4, 160, 160))
    path = jw(wd / "loop.json", {"seam": seam, "last_vs_first": dup, "ratio_1_1.5_seam": bad, "frames": nfr})
    checks = [check("1:2 turns per 6 s: frame(T) == frame(0)", seam < 1e-9, seam, 0),
              check("render t in [0, T): last frame is not a copy of the first", dup > 0.5 and nfr == n, [dup, nfr], [">0.5", n]),
              check("negative control: a 1:1.5 ratio does not loop", bad > 0.5, bad, ">0.5")]
    return checks, [mp4, path]


@card("SHAPE-64")
def orbiting_arcs_core(task, wd):
    import numpy as np
    from PIL import Image, ImageDraw
    W = 320

    def frame(phase):
        im = Image.new("RGB", (W, W), (10, 23, 36))
        d = ImageDraw.Draw(im)
        c = W / 2
        for k in range(6):
            ang = .5 * phase + k * math.pi / 3
            dist = W * (.15 + .055 * math.sin(phase + k))
            rad = W * (.04 + .016 * math.sin(1.3 * phase + k))
            alpha = .24 + .25 * math.sin(phase + k) ** 2
            col = (0x89, 0xd6, 0xce) if k % 2 == 0 else (0xd5, 0xf3, 0x75)
            col = tuple(int(10 + (v - 10) * alpha) for v in col)
            x, y = c + dist * math.cos(ang), c + dist * math.sin(ang)
            d.arc([x - rad, y - rad, x + rad, y + rad], math.degrees(ang), math.degrees(ang) + 270, fill=col, width=3)
        r = W * (.12 + .025 * math.sin(1.25 * phase))
        d.ellipse([c - r, c - r, c + r, c + r], fill=(0xc9, 0xf9, 0x6d))
        d.ellipse([c - .58 * r, c - .58 * r, c + .58 * r, c + .58 * r], fill=(0x0a, 0x17, 0x24))
        return np.asarray(im)
    phases = [i * 0.1 for i in range(64)]
    imgs = [frame(p) for p in phases]
    mp4 = write_mp4(wd / "orbit.mp4", imgs, 30)
    fr = read_mp4(mp4, W, W)
    lime = lambda q: ((np.abs(q - np.array([0xc9, 0xf9, 0x6d])) < 25).all(axis=2))
    core_r = [blob_x((lime(q)[:, :, None] * 255).repeat(3, 2).astype(float), thr=128) for q in fr]
    rr = [(b["x1"] - b["x0"] + 1) / 2 / W for b in core_r]
    static = [rr[0]] * len(rr)
    path = jw(wd / "orbit.json", {"core_r_frac": rr})
    checks = [check("core radius 12% +- 2.5% of width (measured)", abs(max(rr) - .145) < 0.006 and abs(min(rr) - .095) < 0.006, [min(rr), max(rr)], [.095, .145]),
              check("donut hole at .58 r", not lime(fr[0])[160, 160] and lime(fr[0])[160, 160 + int(.85 * W * .12)], True, True),
              check("six 270-degree arcs in teal/lime", int(((np.abs(fr[0] - np.array([10, 23, 36])) > 20).any(axis=2)).sum()) > 500, True, True),
              check("negative control: a static core has no breathing", max(static) - min(static) == 0, max(static) - min(static), ">0")]
    return checks, [mp4, path]


def square_pts(cx, cy, half, rot):
    return [(cx + half * math.sqrt(2) * math.cos(rot + math.pi / 4 + k * math.pi / 2), cy + half * math.sqrt(2) * math.sin(rot + math.pi / 4 + k * math.pi / 2)) for k in range(4)]


def star8(cx, cy, R, r, rot=0.0):
    return [(cx + (R if k % 2 == 0 else r) * math.cos(rot - math.pi / 2 + k * math.pi / 8), cy + (R if k % 2 == 0 else r) * math.sin(rot - math.pi / 2 + k * math.pi / 8)) for k in range(16)]


def draw_partial(d, pts, frac, col, width, closed=True):
    P = pts + [pts[0]] if closed else pts
    segs = list(zip(P, P[1:]))
    L = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs)
    left = L * frac
    for a, b in segs:
        s = math.hypot(b[0] - a[0], b[1] - a[1])
        if left <= 0:
            break
        u = min(1, left / s)
        d.line([a, (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)], fill=col, width=width)
        left -= s


@card("SHAPE-73")
def islamic_rosette(task, wd):
    import numpy as np
    from PIL import Image, ImageDraw
    W, fps, T = 300, 30, 3.0
    col = (0xf6, 0xd2, 0x7a)

    def frame(t, full=False, only_square=False):
        im = Image.new("RGB", (W, W), (12, 14, 20))
        d = ImageDraw.Draw(im)
        rot = math.radians(45 * t / T)
        c = W / 2
        parts = [square_pts(c, c, 78, rot), square_pts(c, c, 78, rot + math.pi / 4), star8(c, c, 120, 92, rot),
                 circle_pts(c, c, 48, 96), star8(c, c, 30, 14, rot)]
        if only_square:
            parts = parts[:1]
        for i, pts in enumerate(parts):
            p = 1.0 if full else min(1, max(0, (t - (.4 + .18 * i)) / 1.3))
            if p > 0:
                draw_partial(d, pts, p, col, 3)
        return np.asarray(im)
    imgs = [frame(f / fps) for f in range(int(T * fps))]
    mp4 = write_mp4(wd / "rosette.mp4", imgs, fps)
    from PIL import ImageFilter

    def sym_ratio(img):
        im0 = Image.fromarray(img.astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))
        a = np.asarray(im0, dtype=float)
        e = lambda deg: float(np.abs(np.asarray(im0.rotate(deg, resample=Image.BILINEAR), dtype=float) - a)[40:260, 40:260].mean())
        return e(45) / e(22.5)
    sym = sym_ratio(frame(0, full=True))
    sym_sq = sym_ratio(frame(0, full=True, only_square=True))
    lit = lambda q: int((q[:, :, 0] > 120).sum())
    fr = read_mp4(mp4, W, W)
    path = jw(wd / "rosette.json", {"sym_err_rosette": sym, "sym_err_square": sym_sq, "lit": [lit(q) for q in fr]})
    checks = [check("nothing drawn before 0.4 s", lit(fr[int(.35 * fps)]) == 0, lit(fr[int(.35 * fps)]), 0),
              check("first square draws over 1.3 s (more ink at 1.0 s than at 0.6 s)", lit(fr[int(1.0 * fps)]) > lit(fr[int(.6 * fps)]) > 0,
                    [lit(fr[int(.6 * fps)]), lit(fr[int(1.0 * fps)])], "growing"),
              check("two squares at 0/45 deg give eight-fold symmetry (err45 / err22.5 small)", sym < 0.5, sym, "<0.5"),
              check("negative control: one square alone is not 45-degree symmetric", sym_sq > 0.8, sym_sq, ">0.8")]
    return checks, [mp4, path]





@card("SHAPE-74")
def interlude_rosette(task, wd):
    import importlib
    import sys
    import numpy as np
    from PIL import Image, ImageDraw
    sd = str(KIT.parent.parent)
    if sd not in sys.path:
        sys.path.insert(0, sd)
    verse = importlib.import_module("verse")
    lines = [[{"text": "a", "start": 0.5, "end": 1.0}, {"text": "b", "start": 1.1, "end": 1.6}], [{"text": "c", "start": 8.0, "end": 8.6}],
             [{"text": "d", "start": 9.6, "end": 10.0}], [{"text": "e", "start": 14.2, "end": 14.6}]]
    pl = verse.plan(lines, [0.5] * 5, 16.0, 1080, 1920, None)
    inter = pl["interludes"]
    jw(wd / "verse_plan.json", {"interludes": inter})
    fps, W, bpm = 30, 200, 120
    imgs, active, angles = [], [], []
    for f in range(int(16 * fps)):
        t = f / fps
        im = Image.new("RGB", (W, W), (10, 10, 16))
        d = ImageDraw.Draw(im)
        on = [x for x in inter if x["t"] <= t < x["end"]]
        if on:
            k = t - on[0]["t"]
            beat = max(0.0, math.cos(2 * math.pi * t * bpm / 60)) ** 8
            R = 60 * (1 + 0.07 * beat)
            rot = math.radians(9 * k)
            for i, pts in enumerate([square_pts(100, 100, R / math.sqrt(2), rot), square_pts(100, 100, R / math.sqrt(2), rot + math.pi / 4)]):
                draw_partial(d, pts, min(1, max(0, (k - .12 * i) / 1.1)), (240, 200, 110), 2)
            angles.append((t, math.degrees(rot)))
        active.append(bool(on))
        imgs.append(np.asarray(im))
    mp4 = write_mp4(wd / "interlude.mp4", imgs[::2], 15)
    fr = read_mp4(mp4, W, W)
    lit = [int((q[:, :, 0] > 120).sum()) for q in fr]
    t_on = [i * 2 / fps for i, v in enumerate(lit) if v > 0]
    path = jw(wd / "interlude.json", {"interludes": inter, "lit_window": [min(t_on), max(t_on)] if t_on else None})
    checks = [check("verse.plan: only the >= 4.5 s pause gets an interlude", len(inter) == 1, inter, "one"),
              check("interlude starts .8 s after the line, ends .5 s before the next", inter and inter[0] == {"t": 2.4, "end": 7.5}, inter, {"t": 2.4, "end": 7.5}),
              check("rosette drawn only inside the interlude", t_on and min(t_on) >= 2.4 - 1e-9 and max(t_on) < 7.5, [min(t_on), max(t_on)] if t_on else None, [2.4, 7.5]),
              check("turns 9 deg/s", abs(angles[-1][1] - 9 * (angles[-1][0] - 2.4)) < 1e-6, angles[-1], "9 deg/s"),
              check("negative control: the 1.6 s and 4.2 s pauses get none", all(not (1.6 <= x["t"] < 8.0 and x["t"] != 2.4) for x in inter) and
                    not any(x["t"] > 10 for x in inter), [x["t"] for x in inter], [2.4])]
    return checks, [mp4, path]


def mulberry32(seed):
    a = seed & 0xFFFFFFFF

    def r():
        nonlocal a
        a = (a + 0x6D2B79F5) & 0xFFFFFFFF
        t = a
        t = ((t ^ (t >> 15)) * (t | 1)) & 0xFFFFFFFF
        t ^= (t + (((t ^ (t >> 7)) * (t | 61)) & 0xFFFFFFFF)) & 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return r


@card("SHAPE-75")
def lanterns_mosque(task, wd):
    import numpy as np
    from PIL import Image, ImageDraw
    fps, W, H = 30, 240, 200
    sine = lambda p: -(math.cos(math.pi * p) - 1) / 2

    def yoyo(t, period):
        k, u = divmod(t / period, 1)
        return sine(u) if int(k) % 2 == 0 else 1 - sine(u)

    def windows(seed):
        r = mulberry32(seed)
        return [(0.9 + 0.8 * r(), r() * 2) for _ in range(8)]

    def frame(t, seed=7):
        im = Image.new("RGB", (W, H), (0x14, 0x09, 0x20))
        d = ImageDraw.Draw(im)
        d.ellipse([70, 80, 170, 180], fill=(0x1d, 0x0f, 0x2c))
        d.rectangle([60, 130, 180, 200], fill=(0x1d, 0x0f, 0x2c))
        for k, (dur, off) in enumerate(windows(seed)):
            v = .55 + .45 * yoyo(t + off, dur)
            d.rectangle([66 + 14 * k, 150, 72 + 14 * k, 165], fill=(int(0xff * v), int(0xc7 * v), int(0x68 * v)))
        ang = math.radians(-3.5 + 7 * yoyo(t, 2.2))
        px, py, L = 40, 0, 80
        x, y = px + L * math.sin(ang), py + L * math.cos(ang)
        d.line([px, py, x, y], fill=(150, 120, 80), width=1)
        hexa = [(x + 12 * math.cos(math.pi / 3 * j + ang), y + 16 + 12 * math.sin(math.pi / 3 * j + ang)) for j in range(6)]
        d.polygon(hexa, fill=(0xff, 0xcf, 0x72), outline=(0xc4, 0x8a, 0x2c))
        return np.asarray(im), math.degrees(ang)
    out = [frame(f / fps) for f in range(int(4.4 * fps))]
    mp4 = write_mp4(wd / "lanterns.mp4", [o[0] for o in out], fps)
    fr = read_mp4(mp4, W, H)
    xs = [blob_x(q[:, :60] * ((q[:, :60, 0] > 200) & (q[:, :60, 2] < 150))[:, :, None], thr=100)["cx"] for q in fr]
    angs = [math.degrees(math.asin((x - 40) / 96)) for x in xs]  # hexagon centre radius ~ L + 16
    a1, _ = frame(1.3, 7)
    a2, _ = frame(1.3, 7)
    b, _ = frame(1.3, 8)
    win = lambda img: [int(img[157, 69 + 14 * k, 0]) for k in range(8)]
    path = jw(wd / "lanterns.json", {"angle_planned": [o[1] for o in out], "angle_measured": angs})
    checks = [check("lantern swings +-3.5 deg (planned)", abs(max(o[1] for o in out) - 3.5) < 0.05 and abs(min(o[1] for o in out) + 3.5) < 0.05,
                    [min(o[1] for o in out), max(o[1] for o in out)], [-3.5, 3.5]),
              check("rendered swing measured from the frames ~ +-3.5 deg", abs((max(angs) - min(angs)) / 2 - 3.5) < 0.8, (max(angs) - min(angs)) / 2, 3.5),
              check("pendulum half period 2.2 s (extreme at 0 and 2.2 s)", abs(out[0][1] + 3.5) < 1e-6 and abs(out[66][1] - 3.5) < 1e-6, [out[0][1], out[66][1]], [-3.5, 3.5]),
              check("windows flicker within .55..1", min(win(a1)) >= int(0xff * .55) - 2, min(win(a1)), ">= 140"),
              check("seeded: same seed same windows", win(a1) == win(a2), True, True),
              check("negative control: another seed gives different window phases", win(a1) != win(b), [win(a1)[:3], win(b)[:3]], "differ")]
    return checks, [mp4, path]


@card("SHAPE-76")
def cloud_cluster(task, wd):
    import numpy as np
    from PIL import Image, ImageDraw
    circles = [(0, 0, 62), (-75, 18, 46), (78, 18, 50), (-32, -34, 52), (38, -40, 58)]
    fps, W, H = 15, 400, 260
    lerp = lambda a, b, u: tuple(int(x + (y - x) * u) for x, y in zip(a, b))
    hx = lambda s: tuple(int(s[i:i + 2], 16) for i in (1, 3, 5))

    def frame(t):
        im = Image.new("RGB", (W, H), (40, 60, 90))
        d = ImageDraw.Draw(im)
        sc = .2 + .8 * power_out_c(min(1, max(0, (t - 3.8) / 1.2)))
        dx = 30 * min(1, max(0, (t - 4.9) / 1.3))
        dark = min(1, max(0, (t - 6.0) / 0.5)) * (1 - min(1, max(0, (t - 8.3) / 0.5)))
        top = lerp(hx("#FFFFFF"), hx("#A6B9CC"), dark)
        base = lerp(hx("#DCE8F2"), hx("#8FA3B8"), dark)
        cx, cy = 200 + dx, 140
        d.rounded_rectangle([cx - 124 * sc, cy + 10 * sc, cx + 124 * sc, cy + 68 * sc], radius=29 * sc, fill=base)
        for x, y, r in circles:
            d.ellipse([cx + (x - r) * sc, cy + (y - r) * sc, cx + (x + r) * sc, cy + (y + r) * sc], fill=top)
        return np.asarray(im)
    ts = [f / fps for f in range(int(9.5 * fps))]
    mp4 = write_mp4(wd / "cloud.mp4", [frame(t) for t in ts], fps)
    fr = read_mp4(mp4, W, H)
    wid = lambda q: (lambda b: b["x1"] - b["x0"] + 1)(blob_x(q, thr=150))
    at = lambda t: fr[int(round(t * fps))]
    top_col = lambda q: tuple(int(v) for v in q[140, 200 + 30 if q is not None else 0])
    path = jw(wd / "cloud.json", {"w_small": wid(at(3.0)), "w_full": wid(at(5.2)), "col_6_6": top_col(at(6.6)), "col_9_3": top_col(at(9.3))})
    full_w = 2 * 128 + 1
    checks = [check("cloud of five circles + base at full scale ~256 px wide", abs(wid(at(5.2)) - 249) <= 10, wid(at(5.2)), "~249"),
              check("grows from scale .2 (3.8-5.0 s)", abs(wid(at(3.0)) / wid(at(5.2)) - 0.2) < 0.05, wid(at(3.0)) / wid(at(5.2)), 0.2),
              check("darkens to #A6B9CC by 6.5 s", max(abs(a - b) for a, b in zip(top_col(at(6.6)), hx("#A6B9CC"))) <= 6, top_col(at(6.6)), hx("#A6B9CC")),
              check("lightens again after 8.3 s", min(top_col(at(9.3))) >= 245, top_col(at(9.3)), "white"),
              check("negative control: before 3.8 s the cloud is not at full size", wid(at(3.0)) < 0.5 * full_w, wid(at(3.0)), "< half")]
    return checks, [mp4, path]


def power_out_c(p):
    return 1 - (1 - p) ** 3


EDITORIAL = REPO.parent / "fastify-motion-bro/web/editorial.js"


@card("SHAPE-77")
def icon_library(task, wd):
    import re
    src = EDITORIAL.read_text(encoding="utf-8")
    m = re.search(r"function icon\(c,name,r,accent,ink\)\{.*?\n\}\n", src, re.S)
    helpers = src[:src.index("function icon(")]
    names = ["eye", "brain", "wallet", "money", "screen", "hourglass", "lightbulb", "rocket", "clock", "cursor", "chart", "stairs",
             "domino", "book", "people", "chess", "star"]
    body = "<canvas id=c width=120 height=120></canvas>"
    js = helpers + m.group(0) + """
const cv=document.getElementById('c'), c=cv.getContext('2d'); const N=%s; const out={};
for(const n of N){c.setTransform(1,0,0,1,0,0); c.fillStyle='#000'; c.fillRect(0,0,120,120); c.translate(60,60); icon(c,n,40,'#E7B65A','#24212A');
 const d=c.getImageData(0,0,120,120).data; let ink=0,acc=0,h=0; for(let i=0;i<d.length;i+=4){ if(d[i]||d[i+1]||d[i+2]) ink++; if(d[i]>200&&d[i+1]>150&&d[i+1]<200&&d[i+2]<120) acc++; h=(h*31+d[i]+d[i+1]*7+d[i+2]*13)>>>0;}
 out[n]={ink,acc,h};}
const blank={}; c.setTransform(1,0,0,1,0,0); c.fillStyle='#000'; c.fillRect(0,0,120,120); const d0=c.getImageData(0,0,120,120).data; let z=0; for(let i=0;i<d0.length;i+=4) if(d0[i]) z++;
document.body.setAttribute('data-r', JSON.stringify({out, blank:z, lw:(()=>{c.setTransform(1,0,0,1,0,0); icon(c,'clock',50,'#fff','#000'); return c.lineWidth;})()}));""" % json.dumps(names)
    page = "<!doctype html><html><body>%s<script>%s</script></body></html>" % (body, js)
    r = chrome(wd, "icons", page)
    path = jw(wd / "icons.json", r)
    o = r["out"]
    hashes = [o[n]["h"] for n in names]
    checks = [check("16 named icons + default all draw", all(o[n]["ink"] > 300 for n in names), min(o[n]["ink"] for n in names), ">300 px"),
              check("every icon is distinct", len(set(hashes)) == len(names), len(set(hashes)), len(names)),
              check("accent colour used by the icons", sum(1 for n in names if o[n]["acc"] > 50) >= 14, sum(1 for n in names if o[n]["acc"] > 50), ">=14"),
              check("stroke width = .08 r", abs(r["lw"] - 4.0) < 1e-9, r["lw"], 4.0),
              check("negative control: an empty canvas has no ink", r["blank"] == 0, r["blank"], 0)]
    return checks, [path]


@card("SHAPE-78")
def living_svg_icons(task, wd):
    body = '<svg width=200 height=200><circle cx=100 cy=100 r=80 fill=none stroke=#ccc /><line id=h x1=100 y1=100 x2=100 y2=40 stroke=#000 stroke-width=4 /><line id=g x1=100 y1=100 x2=100 y2=40 /></svg>'
    js = """const h=$('#h'), g=$('#g'), o={d:0}; const tl=gsap.timeline({paused:true}); tl.to(o,{d:360,duration:4,ease:'none'});
const map=(el,x,y)=>{const m=el.getCTM(); return [m.a*x+m.c*y+m.e, m.b*x+m.d*y+m.f];}; const S=[];
for(let i=0;i<=16;i++){tl.seek(4*i/16); h.setAttribute('transform','rotate('+o.d+' 100 100)'); g.setAttribute('transform','rotate('+o.d+')');
 S.push({d:o.d, tip:map(h,100,40), hub:map(h,100,100), bad_hub:map(g,100,100)});}
R({S});"""
    r = kit_page(wd, "living", body, js)
    S = r["S"]
    path = jw(wd / "living_icon.json", r)
    rad = [math.hypot(s["tip"][0] - 100, s["tip"][1] - 100) for s in S]
    angs = [math.degrees(math.atan2(s["tip"][0] - 100, -(s["tip"][1] - 100))) % 360 for s in S]
    checks = [check("hand turns about its exact centre (hub fixed)", max(math.hypot(s["hub"][0] - 100, s["hub"][1] - 100) for s in S) < 1e-6, 0, 0),
              check("tip stays on its radius (60)", max(abs(x - 60) for x in rad) < 1e-6, max(abs(x - 60) for x in rad), 0),
              check("linear rotation with ease none (22.5 deg per 0.25 s)", all(abs(((a - 22.5 * i) + 180) % 360 - 180) < 1e-6 for i, a in enumerate(angs[:-1])),
                    angs[:3], [0, 22.5, 45]),
              check("negative control: rotate(deg) without cx cy moves the hub", max(math.hypot(s["bad_hub"][0] - 100, s["bad_hub"][1] - 100) for s in S) > 50,
                    max(math.hypot(s["bad_hub"][0] - 100, s["bad_hub"][1] - 100) for s in S), ">50")]
    return checks, [path]


@card("SHAPE-79")
def icon_grid_rules(task, wd):
    import numpy as np
    from PIL import Image, ImageDraw
    # a 24 px icon on the keyline grid: 2 px strokes centred on whole pixels -> edges on the pixel grid
    icon = [("rect", 4, 5, 20, 19), ("line", 8, 10, 16, 10), ("line", 8, 14, 13, 14)]

    def render(scale, offset=0.0):
        S = 24 * scale
        im = Image.new("L", (S * 4, S * 4), 0)
        d = ImageDraw.Draw(im)
        k = 4 * scale
        for op in icon:
            if op[0] == "rect":
                _, x0, y0, x1, y1 = op
                d.rectangle([(x0 + offset) * k - k, (y0 + offset) * k - k, (x1 + offset) * k + k - 1, (y1 + offset) * k + k - 1], outline=255, width=2 * k)
            else:
                _, x0, y0, x1, y1 = op
                d.rectangle([(x0 + offset) * k, (y0 + offset) * k - k, (x1 + offset) * k - 1, (y1 + offset) * k + k - 1], fill=255)
        return np.asarray(im.resize((S, S), Image.BOX), dtype=float)
    shots = {s: render(s // 24 if s >= 24 else 1) for s in (24, 48, 192)}
    small = np.asarray(Image.fromarray(render(1).astype(np.uint8)).resize((16, 16), Image.BOX), dtype=float)
    Image.fromarray(shots[48].astype(np.uint8)).save(wd / "icon_48.png")
    crisp = lambda a: float(((a > 10) & (a < 245)).mean())
    from scipy import ndimage
    lab, nreg = ndimage.label(shots[24] < 128)
    closed = nreg >= 2 and lab[12, 12] != lab[0, 0]
    off = render(1, 0.25)
    path = jw(wd / "icon_rules.json", {"half_tone_share_24": crisp(shots[24]), "half_tone_share_offgrid": crisp(off), "ink_16": float((small > 60).mean())})
    checks = [check("on-grid 24 px icon: crisp 2 px strokes (no half-tone pixels)", crisp(shots[24]) == 0.0, crisp(shots[24]), 0),
              check("scales cleanly to 48 and 192 px", crisp(shots[48]) == 0.0 and crisp(shots[192]) == 0.0, [crisp(shots[48]), crisp(shots[192])], [0, 0]),
              check("still legible at 16 px (ink present, frame intact)", 0.15 < float((small > 60).mean()) < 0.7, float((small > 60).mean()), "0.15..0.7"),
              check("outer shape is closed: interior is a separate region from the outside (measured)", bool(closed), int(nreg), ">=2 regions"),
              check("negative control: an off-grid icon blurs into half-tones", crisp(off) > 0.05, crisp(off), ">0.05")]
    return checks, [wd / "icon_48.png", path]


@card("SHAPE-80")
def sticker_popups(task, wd):
    import numpy as np
    from PIL import Image, ImageDraw
    z, w = .4, 17.0
    wd_ = w * math.sqrt(1 - z * z)
    spring = lambda l: 0 if l <= 0 else 1 - math.exp(-z * w * l) * (math.cos(wd_ * l) + z * w / wd_ * math.sin(wd_ * l))
    fps, W, H = 60, 240, 400
    size = 0.16 * H
    pos = {"top": .30, "centre": .47, "bottom": .64}
    frames, scales, rots = [], [], []

    def draw(sc, fade=1.0):
        im = Image.new("RGB", (W, H), (10, 12, 18))
        d = ImageDraw.Draw(im)
        for yf in pos.values():
            r = size / 2 * sc
            c = tuple(int(v * fade) for v in (0x52, 0xdb, 0xc6))
            d.ellipse([W / 2 - r, yf * H - r, W / 2 + r, yf * H + r], fill=c)
        return np.asarray(im)
    for f in range(int(1.2 * fps)):
        l = f / fps
        sc = spring(l)
        scales.append(sc)
        rots.append(math.sin(3 * l) * .03)
        frames.append(draw(sc, 1 - min(1, max(0, (l - 1.0) / 0.2))))
    mp4 = write_mp4(wd / "stickers.mp4", frames, fps)
    fr = read_mp4(mp4, W, H)

    def width(q, yf):
        row = q[int(yf * H), :, 1] > 100
        return int(row.sum())

    def overshoot(seq):
        ws = [width(q, .47) for q in seq]
        return max(ws) / ws[int(0.8 * fps)] - 1
    col = fr[int(0.8 * fps)][:, W // 2, 1] > 100
    ys = np.nonzero(col)[0]
    runs = np.split(ys, np.nonzero(np.diff(ys) > 1)[0] + 1)
    centres = [float(r.mean()) / H for r in runs]
    linear = [draw(min(1.0, (f / fps) / 0.3)) for f in range(int(1.2 * fps))]
    ov, ov_lin = overshoot(fr), overshoot(linear)
    pred = math.exp(-z * math.pi / math.sqrt(1 - z * z))
    path = jw(wd / "stickers.json", {"scale": scales, "overshoot_measured": ov, "centres": centres})
    checks = [check("spring z .4 w 17 overshoot = exp(-z pi / sqrt(1 - z^2)) (measured on frames)", abs(ov - pred) < 0.04, ov, pred),
              check("default circle size 16% (measured at rest)", abs(width(fr[int(0.8 * fps)], .47) / H - 0.16) < 0.01, width(fr[int(0.8 * fps)], .47) / H, 0.16),
              check("positions top 30% / centre 47% / bottom 64%", len(centres) == 3 and all(abs(a - b) < 0.01 for a, b in zip(centres, pos.values())), centres, list(pos.values())),
              check("wobble rotation sin(3l) x .03 bounded", max(abs(r) for r in rots) <= 0.03 and max(abs(r) for r in rots) > 0.02, max(abs(r) for r in rots), "<=0.03"),
              check(".2 s fade-out at the end", float(fr[-1].max()) < 20, float(fr[-1].max()), "~0"),
              check("negative control: an unsprung linear pop shows no overshoot", abs(ov_lin - pred) >= 0.04, ov_lin, "!= %.3f" % pred)]
    return checks, [mp4, path]


def _fill_poly(pts, W, H, ss=1):
    import numpy as np
    from PIL import Image, ImageDraw
    im = Image.new("L", (W, H), 0)
    ImageDraw.Draw(im).polygon([(float(x), float(y)) for x, y in pts], fill=255)
    return np.asarray(im, dtype=float)


@card("SHAPE-X01")
def shape_chain_same_points(task, wd):
    import numpy as np
    from scipy import ndimage
    N, W, H, cx, cy = 160, 200, 200, 100, 100
    th = np.linspace(0, 2 * np.pi, N, endpoint=False)
    circle = np.c_[cx + 60 * np.cos(th), cy + 60 * np.sin(th)]
    ellipse = np.c_[cx + 80 * np.cos(th), cy + 35 * np.sin(th)]
    sq = np.c_[cx + 60 * np.clip(1.42 * np.cos(th), -1, 1), cy + 60 * np.clip(1.42 * np.sin(th), -1, 1)]
    rr = 40 + 25 * (np.cos(5 * th) > 0)
    star = np.c_[cx + (45 + 22 * np.cos(5 * th)) * np.cos(th), cy + (45 + 22 * np.cos(5 * th)) * np.sin(th)]
    chain = [circle, ellipse, sq, star]
    fps, seg = 30, 20
    frames, counts, steps = [], [], []
    prev = None
    for k in range(len(chain) - 1):
        for f in range(seg):
            u = f / seg
            u = u * u * (3 - 2 * u)
            pts = (1 - u) * chain[k] + u * chain[k + 1]
            counts.append(len(pts))
            if prev is not None:
                steps.append(float(np.abs(pts - prev).max()))
            prev = pts
            frames.append(_fill_poly(pts, W, H))
    mp4 = write_mp4(wd / "chain.mp4", [np.repeat(f[:, :, None], 3, 2).astype(np.uint8) for f in frames], fps)
    mid = frames[seg + seg // 2]
    fade = 0.5 * _fill_poly(chain[1], W, H) + 0.5 * _fill_poly(chain[2], W, H)
    half = lambda a: float(((a > 40) & (a < 215)).mean())
    comps = ndimage.label(mid > 128)[1]
    path = jw(wd / "chain.json", {"counts": sorted(set(counts)), "max_step": max(steps), "half_tone_mid": half(mid), "half_tone_crossfade": half(fade)})
    checks = [check("same point count carried through every shape of the chain", set(counts) == {N}, sorted(set(counts)), [N]),
              check("motion is continuous (no jump between frames)", max(steps) < 12, max(steps), "<12 px"),
              check("mid-morph frame is one solid shape (no ghost)", comps == 1 and half(mid) < 0.002, [comps, half(mid)], [1, "~0"]),
              check("chain reaches every shape (end = star)", float(np.abs(prev - star).max()) < 4, float(np.abs(prev - star).max()), "<4"),
              check("negative control: crossfading two images leaves half-tone ghosts", half(fade) > 0.02, half(fade), ">0.02")]
    return checks, [mp4, path]


def _crossings(a, b):
    def inter(p1, p2, p3, p4):
        d = lambda a, b, c: (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
        return (d(p1, p2, p3) * d(p1, p2, p4) < 0) and (d(p3, p4, p1) * d(p3, p4, p2) < 0)
    n = len(a)
    return int(sum(bool(inter(a[i], b[i], a[j], b[j])) for i in range(n) for j in range(i + 1, n)))


@card("SHAPE-X02")
def formations_no_cut(task, wd):
    import numpy as np
    from scipy.optimize import linear_sum_assignment
    from scipy import ndimage
    from PIL import Image, ImageDraw
    n, W, H = 28, 320, 240
    k = np.arange(n)
    fan = np.c_[160 + 110 * np.cos(np.pi * (0.1 + 0.8 * k / (n - 1))), 220 - 110 * np.sin(np.pi * (0.1 + 0.8 * k / (n - 1)))]
    graph = np.c_[20 + 280 * k / (n - 1), 200 - 150 * (0.5 + 0.5 * np.sin(k / 4.0)) * (k / (n - 1))]
    ring = np.c_[160 + 90 * np.cos(2 * np.pi * k / n), 120 + 90 * np.sin(2 * np.pi * k / n)]
    forms = [fan, graph, ring]

    def assign(a, b):
        cost = ((a[:, None, :] - b[None, :, :]) ** 2).sum(-1) ** 0.5
        r, c = linear_sum_assignment(cost)
        return b[c]
    seq = [forms[0]]
    for f in forms[1:]:
        seq.append(assign(seq[-1], f))
    rng = np.random.default_rng(3)
    rand = [forms[0]] + [f[rng.permutation(n)] for f in forms[1:]]
    cross = [_crossings(seq[i], seq[i + 1]) for i in range(2)]
    cross_r = [_crossings(rand[i], rand[i + 1]) for i in range(2)]
    travel = sum(float(np.linalg.norm(seq[i + 1] - seq[i], axis=1).sum()) for i in range(2))
    travel_r = sum(float(np.linalg.norm(rand[i + 1] - rand[i], axis=1).sum()) for i in range(2))
    fps, seg = 30, 40
    frames = []
    for i in range(2):
        for f in range(seg + 1 if i == 1 else seg):
            u = f / seg
            u = u * u * (3 - 2 * u)
            p = (1 - u) * seq[i] + u * seq[i + 1]
            im = Image.new("RGB", (W, H), (12, 12, 20))
            d = ImageDraw.Draw(im)
            for x, y in p:
                d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(240, 200, 90))
            frames.append(np.asarray(im))
    mp4 = write_mp4(wd / "formations.mp4", frames, fps)
    fr = read_mp4(mp4, W, H)
    def cents(img):
        lab, m = ndimage.label(img[:, :, 1] > 100)
        return np.array(ndimage.center_of_mass(lab > 0, lab, range(1, m + 1))) if m else np.zeros((0, 2))

    def max_move(a, b):
        c = ((a[:, None, :] - b[None, :, :]) ** 2).sum(-1) ** 0.5
        r, cc = linear_sum_assignment(c)
        return float(c[r, cc].max())
    C = [cents(q) for q in fr]
    ok = [i for i in range(len(C) - 1) if len(C[i]) == n and len(C[i + 1]) == n]
    diffs = [max_move(C[i], C[i + 1]) for i in ok]
    hard_cut = max_move(C[0], C[-1])
    counts = [ndimage.label(fr[j][:, :, 1] > 100)[1] for j in (0, seg, 2 * seg)]
    path = jw(wd / "formations.json", {"crossings": cross, "crossings_random": cross_r, "travel": travel, "travel_random": travel_r, "counts": counts})
    checks = [check("same 28 elements in fan, graph and ring", counts == [n, n, n], counts, [n] * 3),
              check("optimal assignment: no crossing paths", sum(cross) == 0, cross, [0, 0]),
              check("no cuts: tracked dots move <= 12 px per frame (measured on %d frame pairs)" % len(ok), len(ok) > 20 and max(diffs) <= 12 and hard_cut > 3 * max(diffs), [len(ok), max(diffs), hard_cut], "<=12 px, cut jump >3x"),
              check("optimal travel shorter than random pairing", travel < 0.6 * travel_r, [travel, travel_r], "<60%"),
              check("negative control: random pairing crosses paths", sum(cross_r) > 20, cross_r, ">20")]
    return checks, [mp4, path]


@card("SHAPE-G01")
def tracker_redraw(task, wd):
    import numpy as np
    from PIL import Image, ImageDraw
    W, H, fps = 320, 200, 30
    X = lambda t: 40 + 240 * t
    Y = lambda x: 100 - 60 * math.sin((x - 40) / 240 * 2 * math.pi)
    dY = lambda x: -60 * math.cos((x - 40) / 240 * 2 * math.pi) * 2 * math.pi / 240

    def draw(dot_t, tan_t):
        im = Image.new("RGB", (W, H), (0, 0, 0))
        d = ImageDraw.Draw(im)
        d.line([(x, Y(x)) for x in range(40, 281)], fill=(70, 70, 70), width=1)
        x0 = X(tan_t)
        s = dY(x0)
        d.line([(x0 - 50, Y(x0) - 50 * s), (x0 + 50, Y(x0) + 50 * s)], fill=(0, 255, 0), width=3)
        x = X(dot_t)
        d.ellipse([x - 6, Y(x) - 6, x + 6, Y(x) + 6], fill=(255, 0, 0))
        return np.asarray(im)
    ts = [f / 59 for f in range(60)]
    tracker = [draw(t, t) for t in ts]
    separate = [draw(t, t ** 2) for t in ts]   # tangent animated by its own (eased) tween

    def gap(img):
        rm = (img[:, :, 0] > 150) & (img[:, :, 1] < 110)
        gm = (img[:, :, 1] > 150) & (img[:, :, 0] < 110)
        ry, rx = np.nonzero(rm)
        gy, gx = np.nonzero(gm)
        px, py = rx.mean(), ry.mean()
        a, b = np.polyfit(gx, gy, 1)
        return abs(a * px - py + b) / math.hypot(a, 1), (px, py)
    mp4 = write_mp4(wd / "tracker.mp4", tracker, fps)
    fr = read_mp4(mp4, W, H)
    g_tr = [gap(f)[0] for f in fr[3:-3]]
    g_sep = [gap(f)[0] for f in separate[3:-3]]
    dots = [gap(f)[1] for f in fr[3:-3]]
    on_curve = max(abs(py - Y(px)) for px, py in dots)
    path = jw(wd / "tracker.json", {"gap_tracker_max": max(g_tr), "gap_separate_max": max(g_sep), "dot_curve_err": on_curve})
    checks = [check("tangent passes through the dot in every frame (one tracker)", max(g_tr) < 2.0, max(g_tr), "<2 px"),
              check("dot measured on the curve y = f(x) in every frame", on_curve < 3.0, on_curve, "<3 px (dot r 6)"),
              check("dot moves monotonically with the tracker", all(dots[i + 1][0] > dots[i][0] for i in range(len(dots) - 1)), True, True),
              check("negative control: separately tweened tangent drifts off the dot", max(g_sep) > 10, max(g_sep), ">10 px")]
    return checks, [mp4, path]


@card("SHAPE-G02")
def keyed_part_matching(task, wd):
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
    font = ImageFont.load_default(size=28) if hasattr(ImageFont, "load_default") else None
    A = ["x", "+", "2", "=", "5"]
    B = ["x", "=", "5", "-", "2"]
    adv = 26
    posA = {i: 30 + adv * i for i in range(len(A))}
    posB = {i: 30 + adv * i for i in range(len(B))}

    def keyed():
        pairs, usedB = [], set()
        for i, g in enumerate(A):
            j = next((j for j, h in enumerate(B) if h == g and j not in usedB), None)
            if j is not None:
                usedB.add(j)
                pairs.append((i, j, "move"))
        restA = [i for i in range(len(A)) if i not in {p[0] for p in pairs}]
        restB = [j for j in range(len(B)) if j not in usedB]
        pairs += [(i, j, "morph") for i, j in zip(restA, restB)]
        return pairs
    index = [(i, i, "move" if A[i] == B[i] else "morph") for i in range(len(A))]

    def frame(pairs, u):
        im = Image.new("L", (200, 50), 0)
        layers = []
        for i, j, kind in pairs:
            x = posA[i] + (posB[j] - posA[i]) * u
            if kind == "move":
                layers.append((A[i], x, 1.0))
            else:
                layers.append((A[i], x, 1 - u))
                layers.append((B[j], x, u))
        acc = np.zeros((50, 200))
        for g, x, a in layers:
            l = Image.new("L", (200, 50), 0)
            ImageDraw.Draw(l).text((x, 8), g, fill=255, font=font)
            acc = np.maximum(acc, a * np.asarray(l, dtype=float))
        return acc
    kp, ip = keyed(), index
    travel = lambda P: sum(abs(posB[j] - posA[i]) for i, j, _ in P)
    morphs = lambda P: sum(k == "morph" for *_, k in P)
    half = lambda a: float(((a > 60) & (a < 200)).sum())
    mids_k = frame(kp, 0.5)
    mids_i = frame(ip, 0.5)
    frames = [np.repeat(frame(kp, f / 29)[:, :, None], 3, 2).astype(np.uint8) for f in range(30)]
    mp4 = write_mp4(wd / "keyed.mp4", frames, 30)
    path = jw(wd / "keyed.json", {"keyed": kp, "index": ip, "travel_keyed": travel(kp), "travel_index": travel(ip),
                                   "morphs_keyed": morphs(kp), "morphs_index": morphs(ip), "half_keyed": half(mids_k), "half_index": half(mids_i)})
    checks = [check("matching parts keep their identity (x, =, 5, 2 move)", morphs(kp) == 1, morphs(kp), 1),
              check("only the differing part morphs (+ -> -)", [(A[i], B[j]) for i, j, k in kp if k == "morph"] == [("+", "-")],
                    [(A[i], B[j]) for i, j, k in kp if k == "morph"], [["+", "-"]]),
              check("mid-frame has fewer melting (half-tone) pixels than index pairing", half(mids_k) < 0.5 * half(mids_i), [half(mids_k), half(mids_i)], "<50%"),
              check("negative control: index pairing morphs every differing slot", morphs(ip) >= 4, morphs(ip), ">=4")]
    return checks, [mp4, path]


def _poly_pts(s):
    return [tuple(map(float, q.split(","))) for q in s.split()]


@card("SHAPE-12")
def facet_morph(task, wd):
    import re
    import numpy as np
    probe = """const D=tl.duration(); const S=[]; for(let i=0;i<=40;i++){tl.seek(D*i/40,false); S.push($$('polygon').map(p=>[p.getAttribute('points'),p.getAttribute('fill'),p.getAttribute('stroke')]));}
tl.seek(D*0.5,false); const a=$$('polygon').map(p=>p.getAttribute('points')).join('|'); tl.seek(D*0.9,false); tl.seek(D*0.5,false); const b=$$('polygon').map(p=>p.getAttribute('points')).join('|');
document.body.setAttribute('data-r',JSON.stringify({D,n:$$('polygon').length,S,seek_same:a===b}));"""
    r, comp = hf_component(wd, "facet-morph", {"forms": "blob,mark,badge"}, probe, (540, 540))
    S = r["S"]
    allpts = [[_poly_pts(p) for p, _, _ in fr] for fr in S]
    sil = [sum(area(tri) for tri in fr) for fr in allpts]
    rgb = lambda s: tuple(int(x) for x in re.findall(r"\d+", s)[:3])

    def light_corr(fr, lx, ly):
        pts = [_poly_pts(p) for p, _, _ in fr]
        cx = sum(x for tri in pts for x, _ in tri) / (3 * len(pts))
        cy = sum(y for tri in pts for _, y in tri) / (3 * len(pts))
        dots, lum = [], []
        for (p, f, _), tri in zip(fr, pts):
            mx, my = sum(x for x, _ in tri) / 3 - cx, sum(y for _, y in tri) / 3 - cy
            ln = math.hypot(mx, my) or 1
            dots.append(mx / ln * lx + my / ln * ly)
            c = rgb(f)
            lum.append(0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2])
        return float(np.corrcoef(dots, lum)[0, 1])
    mid = S[20]
    c_ul, c_lr = light_corr(mid, -0.62, -0.78), light_corr(mid, 0.62, 0.78)
    disp = lambda A, B: max(math.hypot(a[0] - b[0], a[1] - b[1]) for ta, tb in zip(A, B) for a, b in zip(ta, tb))
    changes = [disp(allpts[i], allpts[i + 1]) for i in range(40)]
    flat = all(f == s and f.startswith("rgb") for _, f, s in mid)
    path = jw(wd / "facet_morph.json", {"D": r["D"], "n": r["n"], "seek_same": r["seek_same"], "area": sil, "corr_ul": c_ul,
                                         "corr_lr": c_lr, "changes": changes})
    checks = [check("36 triangular facets", r["n"] == 36 and all(len(_poly_pts(p)) == 3 for p, _, _ in mid), r["n"], 36),
              check("mass morphs between silhouettes (area changes over the timeline)", (max(sil) - min(sil)) / max(sil) > 0.1, [min(sil), max(sil)], ">10% range"),
              check("one flat colour per facet (fill = stroke rgb)", flat, flat, True),
              check("lit from the upper left: facet brightness correlates with the UL direction", c_ul > 0.3, c_ul, ">0.3"),
              check("seek-safe: same time gives identical vertices after seeking away", r["seek_same"], r["seek_same"], True),
              check("hold: final frames still (hold_last)", changes[-1] < 1e-6, changes[-1], 0),
              check("negative control: light from the lower right does not match the shading", c_lr < 0, c_lr, "<0")]
    return checks, [path, comp]


def metaball_field(W, H, centres, r):
    import numpy as np
    y, x = np.mgrid[0:H, 0:W].astype(float)
    f = np.zeros((H, W))
    for cx, cy in centres:
        f += r * r / ((x - cx) ** 2 + (y - cy) ** 2 + 1e-6)
    return f


@card("SHAPE-28")
def gooey_split_and_blob(task, wd):
    import numpy as np
    from scipy import ndimage
    # part 1: a dot splits into a three-dot menu through a metaball neck, spins, then re-merges (iso-surface f >= 1)
    W, H, r, fps = 240, 120, 14, 30
    def centres(t):
        if t < 0.8:
            spread = 46 * (1 - (1 - t / 0.8) ** 3)
        elif t < 1.4:
            spread = 46.0
        else:
            spread = 46 * max(0.0, 1 - (t - 1.4) / 0.6) ** 2
        spin = math.radians(180 * max(0.0, min(1.0, (t - 0.8) / 0.4)))
        return [(120 + k * spread * math.cos(spin), 60 + k * spread * math.sin(spin)) for k in (-1, 0, 1)]
    ts = [f / fps for f in range(int(2.2 * fps))]
    masks = [(metaball_field(W, H, centres(t), r) >= 1.0) for t in ts]
    comps = [ndimage.label(m)[1] for m in masks]
    sep = [math.dist(centres(t)[0], centres(t)[1]) for t in ts]
    # neck: still one body while centres are farther apart than 2r (plain circles would already be apart)
    neck = [i for i in range(len(ts)) if comps[i] == 1 and 2 * r < sep[i] < 3.2 * r]
    circles = lambda t: np.any([((np.mgrid[0:H, 0:W][1] - cx) ** 2 + (np.mgrid[0:H, 0:W][0] - cy) ** 2) <= r * r for cx, cy in centres(t)], 0)
    t_neck = ts[neck[0]] if neck else 0.0
    comps_plain = ndimage.label(circles(t_neck))[1]
    mp4 = write_mp4(wd / "gooey.mp4", [np.repeat((m * 255).astype(np.uint8)[:, :, None], 3, 2) for m in masks], fps)
    # part 2: hyperframes soft-blob-touch: the blob bulges toward the touch and recovers on a velocity-preserving spring
    probe = """const D=tl.duration(); const cv=$('canvas'); const ctx=cv.getContext('2d'); const S=[];
const cen=()=>{const d=ctx.getImageData(0,0,cv.width,cv.height).data; let sx=0,sy=0,s=0; for(let y=0;y<cv.height;y+=2)for(let x=0;x<cv.width;x+=2){const a=d[(y*cv.width+x)*4+3]; sx+=a*x; sy+=a*y; s+=a;} return [sx/s/cv.width, sy/s/cv.height, s];};
for(let i=0;i<=80;i++){tl.seek(D*i/80,false); S.push(cen());}
tl.seek(2.0,false); const a=cen(); tl.seek(3.9,false); tl.seek(0.3,false); tl.seek(2.0,false); const b=cen();
document.body.setAttribute('data-r',JSON.stringify({D,S,seek_same:JSON.stringify(a)===JSON.stringify(b),w:cv.width,h:cv.height}));"""
    rr, comp = hf_component(wd, "soft-blob-touch", {"touch_x": 66, "touch_y": 38, "touch_at": 1.6}, probe, (400, 400))
    S = rr["S"]
    D = rr["D"]
    tt = [D * i / 80 for i in range(81)]
    rest = S[0]
    tx, ty = 0.66, 0.38
    toward = [((p[0] - rest[0]) * (tx - rest[0]) + (p[1] - rest[1]) * (ty - rest[1])) / math.hypot(tx - rest[0], ty - rest[1]) for p in S]
    i_peak = max(range(81), key=lambda i: toward[i])
    after = toward[i_peak:]
    vel = [(toward[i + 1] - toward[i]) / (tt[1] - tt[0]) for i in range(80)]
    acc = [abs(vel[i + 1] - vel[i]) for i in range(i_peak - 3, min(79, i_peak + 4))]
    path = jw(wd / "gooey_blob.json", {"components": comps, "neck_frames": len(neck), "neck_t": t_neck, "plain_circles_components": comps_plain,
                                        "blob_toward": toward, "peak_t": tt[i_peak], "seek_same": rr["seek_same"]})
    checks = [check("one dot at the start, three dots in the menu", comps[0] == 1 and max(comps) == 3, [comps[0], max(comps)], [1, 3]),
              check("metaball neck: still one body with centres > 2r apart", len(neck) >= 1, len(neck), ">=1 frame"),
              check("re-merges into one dot at the end", comps[-1] == 1, comps[-1], 1),
              check("blob bulges toward the touch point after contact (1.6 s)", toward[i_peak] > 0.01 and tt[i_peak] > 1.6, [toward[i_peak], tt[i_peak]], ">1% toward, after 1.6 s"),
              check("recovers on a spring: overshoots past rest then settles", min(after) < -0.0005 and abs(toward[-1]) < 0.002, [min(after), toward[-1]], "overshoot <0, end ~0"),
              check("seek-safe repaint (same time, same canvas after seeking away)", rr["seek_same"], rr["seek_same"], True),
              check("negative control: plain circles at the neck frame are already separate bodies", comps_plain > 1, comps_plain, ">1"),
              check("negative control: before contact the blob does not lean toward the touch", abs(toward[int(80 * 0.5 / D)]) < 0.3 * toward[i_peak],
                    toward[int(80 * 0.5 / D)], "small")]
    return checks, [mp4, path, comp]


@card("SHAPE-88")
def separator_reveal(task, wd):
    probe = """const root=$('.hf-ui-separator'), span=root.querySelector('span');
const T=gsap.timeline({paused:true}); T.fromTo(root,{'--hf-separator-progress':0},{'--hf-separator-progress':1,duration:0.42,ease:'power3.out'},0);
const w=()=>span.getBoundingClientRect().width; const S=[]; for(let i=0;i<=14;i++){T.seek(0.42*i/14,false); S.push(w());}
T.seek(0.21,false); const a=w(); T.seek(0.42,false); T.seek(0.05,false); T.seek(0.21,false); const b=w();
root.style.removeProperty('--hf-separator-progress'); const untimed=w();
document.body.setAttribute('data-r',JSON.stringify({S,a,b,full:root.getBoundingClientRect().width,thick:root.getBoundingClientRect().height,untimed}));"""
    r, comp = hf_component(wd, "separator", {"orientation": "horizontal", "thickness": "bold", "tone": "accent"}, probe, (480, 120))
    S = r["S"]
    exp = [r["full"] * (1 - (1 - i / 14) ** 4) for i in range(15)]  # GSAP power3.out = 1 - (1 - p)^4
    err = max(abs(a - b) for a, b in zip(S, exp))
    path = jw(wd / "separator.json", r | {"expected": exp, "max_err": err})
    checks = [check("rule is 360 px wide and 4 px thick (bold)", abs(r["full"] - 360) < 0.5 and abs(r["thick"] - 4) < 0.01, [r["full"], r["thick"]], [360, 4]),
              check("progressive reveal follows power3.out 0.42 s", err < 0.6, err, "<0.6 px"),
              check("starts hidden, ends full", S[0] == 0 and abs(S[-1] - r["full"]) < 0.5, [S[0], S[-1]], [0, r["full"]]),
              check("seek-safe: same time gives same width after seeking away", abs(r["a"] - r["b"]) < 1e-9, [r["a"], r["b"]], "equal"),
              check("negative control: without the timeline the rule is drawn full at t=0", r["untimed"] > 0.9 * r["full"], r["untimed"], "full width")]
    return checks, [path, comp]


@card("SHAPE-61")
def pattern_fields_grid(task, wd):
    import numpy as np
    from scipy.spatial import cKDTree
    from PIL import Image
    # (a) hyperframes dynamic-grid: CSS-variable density / weight and the scroll recipe, measured on computed styles
    probe = """const g=$('.hf-dynamic-grid'); const cs=()=>getComputedStyle(g);
const T=gsap.timeline({paused:true}); T.to(g,{'--hf-grid-x':'72px','--hf-grid-y':'-72px',duration:6,ease:'none'},0);
const P=[]; for(const t of [0,1.5,3,6]){T.seek(t,false); P.push(cs().backgroundPosition);}
document.body.setAttribute('data-r',JSON.stringify({size:cs().backgroundSize,line:g.style.getPropertyValue('--hf-grid-line'),P}));"""
    r, comp = hf_component(wd, "dynamic-grid", {"density": "fine", "weight": "bold"}, probe, (400, 300))
    nums = lambda s: [float(v) for v in __import__("re").findall(r"-?\d+\.?\d*", s)]
    pos = [nums(p)[:2] for p in r["P"]]
    # (b) fragment-shader equivalents on the CPU: ripples, op-art spiral, sliding stripes, Voronoi cells
    H = W = 160
    y, x = np.mgrid[0:H, 0:W].astype(float)
    cx = cy = 80
    rad = np.hypot(x - cx, y - cy)
    ang = np.arctan2(y - cy, x - cx)
    t = 0.25
    ripples = 0.5 + 0.5 * np.cos(2 * np.pi * (rad / 16 - t))
    spiral = (np.mod(ang / (2 * np.pi) * 6 + rad / 20, 1) > 0.5).astype(float)
    stripes = (np.mod((x + y) / 20 + t, 1) > 0.5).astype(float)
    rng = np.random.default_rng(5)
    seeds = rng.uniform(0, W, (24, 2))
    d = ((x[..., None] - seeds[:, 0]) ** 2 + (y[..., None] - seeds[:, 1]) ** 2)
    cells = d.argmin(-1)
    ref = cKDTree(seeds).query(np.c_[x.ravel(), y.ravel()])[1].reshape(H, W)
    tile = np.concatenate([np.concatenate([ripples, spiral], 1), np.concatenate([stripes, cells / 23.0], 1)], 0)
    Image.fromarray((tile * 255).astype(np.uint8)).save(wd / "patterns.png")
    prof = ripples[80, 80:]
    peaks = [i for i in range(1, len(prof) - 1) if prof[i] >= prof[i - 1] and prof[i] > prof[i + 1]]
    period = float(np.diff(peaks).mean())
    # stripes slide: phase shift between t and t+0.5 equals half a period (pixels invert)
    stripes2 = (np.mod((x + y) / 20 + t + 0.5, 1) > 0.5).astype(float)
    inv = float((stripes2 != stripes).mean())
    path = jw(wd / "patterns.json", {"grid": r, "ripple_period": period, "voronoi_agree": float((cells == ref).mean()), "stripe_invert": inv})
    checks = [check("grid density fine = 44 px cells, weight bold = 3 px lines (CSS vars)", r["size"].startswith("44px") and r["line"] == "3px", [r["size"], r["line"]], ["44px", "3px"]),
              check("grid scrolls linearly: x 0 -> 72 px, y 0 -> -72 px over 6 s", pos[0] == [0, 0] and abs(pos[2][0] - 36) < 0.1 and abs(pos[3][1] + 72) < 0.1, pos, [[0, 0], "..", [36, -36], [72, -72]]),
              check("ripples: radial period 16 px", abs(period - 16) < 0.6, period, 16),
              check("Voronoi: every pixel belongs to its nearest seed (vs k-d tree)", float((cells == ref).mean()) == 1.0, float((cells == ref).mean()), 1.0),
              check("sliding stripes: half-cycle shift inverts the pattern", inv > 0.85, inv, ">0.85"),
              check("op-art spiral covers half the area", abs(float(spiral.mean()) - 0.5) < 0.03, float(spiral.mean()), 0.5),
              check("negative control: farthest-seed labelling disagrees with the k-d tree", float((d.argmax(-1) == ref).mean()) < 0.1, float((d.argmax(-1) == ref).mean()), "<0.1")]
    return checks, [wd / "patterns.png", path, comp]
