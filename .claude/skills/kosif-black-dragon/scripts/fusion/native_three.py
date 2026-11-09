#!/usr/bin/env python3
"""native_three.py - Black Dragon helper for deterministic three.js / TSL frame rendering.
Original code. Ideas observed in mrdoob/three.js (MIT): NodeFrame reads performance.now()
(src/nodes/core/NodeFrame.js:310-316) so TSL `time`/`deltaTime` are wall-clock driven;
the fix is a virtual clock injected before any module loads.
Subcommands: catalog | clock-shim | harness | self-test   (--json before the subcommand)
"""
import argparse, json, re, subprocess, sys, tempfile, shutil
from pathlib import Path

SHIM = r"""(() => {
  // virtual clock: performance.now / Date.now / rAF are driven only by __dragon.step(frame)
  const fps = %(fps)s; let frame = 0; const cbs = [];
  const now = () => frame * 1000 / fps;
  const base = 1700000000000;
  performance.now = now; Date.now = () => base + now();
  window.requestAnimationFrame = (cb) => { cbs.push(cb); return cbs.length; };
  window.cancelAnimationFrame = () => {};
  window.__dragon = {
    fps, get frame() { return frame; },
    // advance to absolute frame index n, firing queued rAF callbacks once at that time
    step(n) { frame = n; const q = cbs.splice(0); q.forEach(cb => cb(now())); return now(); }
  };
})();"""

HTML = """<!doctype html><meta charset=utf-8><style>html,body{margin:0;background:#000}canvas{display:block}</style>
<script>%(shim)s</script>
<script type="importmap">{"imports":{"three":"%(three)s","three/webgpu":"%(webgpu)s","three/tsl":"%(tsl)s"}}</script>
<canvas id=c width=%(w)s height=%(h)s></canvas>
<script type="module">
import * as THREE from 'three/webgpu';
// Rule: never use THREE.Clock/Date; read time only via window.__dragon.frame / fps.
const renderer = new THREE.WebGPURenderer({canvas: document.getElementById('c'), antialias:true, forceWebGL: %(fw)s});
await renderer.init();
const scene = new THREE.Scene(), camera = new THREE.PerspectiveCamera(50, %(w)s/%(h)s, .1, 100);
camera.position.z = 3; scene.add(new THREE.Mesh(new THREE.TorusKnotGeometry(.6,.2,128,16), new THREE.MeshNormalMaterial()));
window.renderFrame = async (n) => {
  window.__dragon.step(n);                      // updates performance.now -> TSL time/deltaTime
  const t = n / window.__dragon.fps;
  scene.children[0].rotation.y = t * Math.PI;   // pure function of t
  await renderer.render(scene, camera);
  return true;
};
window.ready = true;
</script>"""

DRIVER = """# Playwright driver: serve the folder (python -m http.server) then: python drive.py http://localhost:8000/index.html
import sys; from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    pg = b.new_page(viewport={'width':%(w)s,'height':%(h)s}); pg.goto(sys.argv[1]); pg.wait_for_function('window.ready')
    for n in range(%(frames)s):
        pg.evaluate('n => renderFrame(n)', n)
        pg.locator('#c').screenshot(path=f'frame_{n:05d}.png')
    b.close()
"""


def catalog(root: Path):
    out = {"tsl_display": [], "tsl_math": [], "tsl_utils": [], "tsl_lighting": [], "core_nodes": {}}
    for sub in ("display", "math", "utils", "lighting"):
        d = root / "examples" / "jsm" / "tsl" / sub
        for f in (sorted(d.glob("*.js")) if d.exists() else []):
            txt = f.read_text("utf-8", "replace")
            names = re.findall(r"^export (?:const|function|class) (\w+)", txt, re.M)
            out["tsl_" + sub].append({"file": f.name, "exports": names})
    nd = root / "src" / "nodes"
    for sub in ("display", "utils", "procedural", "gpgpu"):
        d = nd / sub
        names = []
        for f in (sorted(d.glob("*.js")) if d.exists() else []):
            names += re.findall(r"^export const (\w+)", f.read_text("utf-8", "replace"), re.M)
        out["core_nodes"][sub] = names
    return out


def run_shim_in_node(fps=30):
    node = shutil.which("node")
    if not node:
        return None
    js = ("globalThis.window=globalThis;globalThis.performance={now:()=>0};" + (SHIM % {"fps": fps}) +
          ";let hits=[];window.requestAnimationFrame(t=>hits.push(t));const a=__dragon.step(15);"
          "const b=performance.now();console.log(JSON.stringify({a,b,hits,d:Date.now()}))")
    r = subprocess.run([node, "-e", js], capture_output=True, text=True, timeout=30)
    return json.loads(r.stdout) if r.returncode == 0 else {"error": r.stderr}


def emit(a, obj):
    print(json.dumps(obj, ensure_ascii=False, indent=1 if a.json else None))


def params(a):
    p = {"fps": a.fps, "w": a.w, "h": a.h, "frames": a.frames, "fw": str(a.force_webgl).lower(),
         "three": a.three_url, "webgpu": a.three_url.replace("module", "webgpu"),
         "tsl": a.three_url.replace("module", "tsl")}
    p["shim"] = SHIM % p
    return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    sp = ap.add_subparsers(dest="cmd", required=True)
    c = sp.add_parser("catalog"); c.add_argument("repo")
    s = sp.add_parser("clock-shim"); s.add_argument("--fps", type=int, default=30)
    h = sp.add_parser("harness"); h.add_argument("outdir")
    h.add_argument("--fps", type=int, default=30); h.add_argument("--w", type=int, default=1080)
    h.add_argument("--h", type=int, default=1920); h.add_argument("--frames", type=int, default=90)
    h.add_argument("--three-url", default="/build/three.module.js"); h.add_argument("--force-webgl", action="store_true")
    sp.add_parser("self-test")
    a = ap.parse_args()
    if a.cmd == "catalog":
        emit(a, catalog(Path(a.repo)))
    elif a.cmd == "clock-shim":
        print(SHIM % {"fps": a.fps})
    elif a.cmd == "harness":
        o = Path(a.outdir); o.mkdir(parents=True, exist_ok=True)
        p = params(a)
        (o / "index.html").write_text(HTML % p, "utf-8"); (o / "drive.py").write_text(DRIVER % p, "utf-8")
        emit(a, {"written": [str(o / "index.html"), str(o / "drive.py")], "fps": a.fps})
    else:
        with tempfile.TemporaryDirectory() as td:
            t = Path(td) / "r"
            (t / "examples/jsm/tsl/display").mkdir(parents=True); (t / "src/nodes/utils").mkdir(parents=True)
            (t / "examples/jsm/tsl/display/BloomNode.js").write_text("export const bloom = 1;\nexport default class BloomNode {}\nexport class X{}\n")
            (t / "src/nodes/utils/Timer.js").write_text("export const time = 1;\nexport const frameId = 2;\n")
            cat = catalog(t)
            assert cat["tsl_display"][0]["exports"] == ["bloom", "X"], cat
            assert cat["core_nodes"]["utils"] == ["time", "frameId"], cat
            hd = Path(td) / "h"
            sys.argv = [sys.argv[0], "harness", str(hd), "--frames", "3"]
            main()
            html = (hd / "index.html").read_text("utf-8")
            assert "__dragon" in html and "forceWebGL: false" in html and (hd / "drive.py").exists()
            r = run_shim_in_node(30)
            if r is None:
                print("node missing, shim JS check skipped")
            else:
                assert "error" not in r, r
                assert abs(r["a"] - 500.0) < 1e-9 and r["b"] == r["a"], r
                assert r["hits"] == [500.0] and r["d"] == 1700000000500, r
        print("self-test OK: catalog parse, harness html+driver, virtual clock frame15@30fps=500ms")


if __name__ == "__main__":
    main()
