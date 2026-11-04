"""Wave 3, chunk 12: 3D, apps, light, maps, media, self-discovery and voice cards as real programs.

Every runner builds its own deterministic fixture inside the work folder, runs the card's method with the engine the card
names when it is here (three.js 0.186 + the vendored K3 / K3S / lab kits in Playwright's Chromium with SwiftShader WebGL,
GSAP, D3 + topojson + world-atlas, MapLibre GL 6, HyperFrames registry blocks, ffmpeg/libass, tesseract ara+eng,
ImageMagick 6, OpenSCAD, axe-core, pa11y, GDAL ogr2ogr, tippecanoe, DuckDB + spatial, music21, MediaPipe, jinja2,
FastAPI, the mcp 2.x SDK, vite, git, venv/uv, npm), measures the output against known answers and runs the same
measurement on the untreated input as a negative control.

Installed for this module (user environment, the engines the cards name):
  pip:  fastapi 0.162, cairosvg 2.9, pillow-heif 1.8, psd-tools 1.26, duckdb-extension-spatial 2.0 (wheel from PyPI;
        loaded by file path because extensions.duckdb.org is not reachable from here)
  apt:  gdal-bin 3.8.4, tippecanoe 2.49; libgles2 + libegl1 (MediaPipe GL)
  npm -g: @versatiles/style 8.1.1
  file: ~/.cache/kosif-models/blaze_face_short_range.tflite (MediaPipe face detector, 230 KB, storage.googleapis.com)
CDN URLs inside HyperFrames blocks (cdn.jsdelivr.net is not reachable) are served from the global node_modules copies of the
same packages by the Playwright router; Google Fonts requests get an empty stylesheet.
"""
import base64
import difflib
import hashlib
import json
import math
import os
import re
import shutil
import socket
import struct
import subprocess
import sys
import time
import unicodedata
import wave
import zlib
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from _harness import card, check, fx, sha

HERE = Path(__file__).resolve().parent
SKILLS = HERE.parents[1]
REPO = HERE.parents[3]
FONTS = SKILLS / "kosif-superpowers/proofs/_shared/fonts"
KIT = SKILLS / "kosif-superpowers/vendor/100-superskills/skills/kosif-montage-motion/scripts/kit"
VENDOR_SCRIPTS = KIT.parent
_NODE = shutil.which("node") or "/opt/node22/bin/node"
NM = Path(_NODE).resolve().parents[1] / "lib/node_modules"
FACE_MODEL = Path.home() / ".cache/kosif-models/blaze_face_short_range.tflite"
SPATIAL_EXT = None
for _p in sys.path + ["/usr/local/lib/python3.13/site-packages"]:
    _c = Path(_p) / "duckdb_extension_spatial/extensions/v2.0.0/spatial.duckdb_extension"
    if _c.exists():
        SPATIAL_EXT = _c
        break

GAPS: dict = {
    "power:3D-23": "Blender as a Python module (pip bpy, ~400 MB, Blender 5.2) is not installed and is too large to pull "
                   "for a runner; Blender MCP, Cinema 4D and Spline need the user's own install or account",
    "power:3D-24": "Cesium flights need a MapTiler key (terrain + satellite) or a Google Maps key (Photorealistic 3D "
                   "Tiles) and the Cesium CDN; no key is configured and cdn.jsdelivr.net is not reachable here",
    "power:3D-46": "the car exploded view is image-to-image and image-to-video generation through a paid service; no key, "
                   "no spending allowed, so no picture can be produced or measured",
    "power:APP-03": "ArtifactData / ArtifactComments are deferred tools of the agent session; a subprocess runner cannot "
                    "load or call them",
    "power:APP-12": "calling Claude needs ANTHROPIC_API_KEY (paid); the anthropic SDK is not installed and no key is set",
    "power:APP-14": "Higgsfield website creation and deployment spends credits and needs the connector; never without the "
                    "user's explicit request",
    "power:APP-20": "CadQuery needs the OpenCascade kernel (cadquery-ocp, hundreds of MB); not installed here "
                    "(OpenSCAD, APP-21, is the parametric CAD engine that runs here)",
    "power:GLOW-37": "@remotion/effects (~55 WebGL2 effects) is not installed and its effect code is not vendored; "
                     "reproducing its unknown shaders would be a fake",
    "power:GLOW-38": "needs Chromium's html-in-canvas drawElementImage flag plus WebGPU/TypeGPU; neither is available or "
                     "verified here",
    "power:GLOW-52": "the plates are the HyperFrames shaders.iife.js WebGPU library; headless WebGPU is not available here",
    "power:GLOW-72": "the locked lighting phrases only pay off through an image/video generation service (paid key); no "
                     "picture can be produced or measured",
    "power:MAP-19": "the hosted map styles and static images need an AWS Location Service API key (geo-maps actions); "
                    "none is configured",
    "power:MAP-27": "Overture GeoParquet lives on S3 and needs DuckDB httpfs, an extension that cannot be downloaded here "
                    "(extensions.duckdb.org unreachable); a remote multi-GB release is also outside a 15 s runner",
    "power:MEDIA-07": "EasyOCR needs CPU torch (~769 MB) plus model downloads; not installed",
    "power:MEDIA-25": "faster-whisper is installed but its CTranslate2 models download from huggingface.co, which the proxy "
                      "blocks here (403); no model is cached",
    "power:MEDIA-26": "Demucs needs torch and model weights (hundreds of MB) and minutes per track on CPU",
    "power:MEDIA-27": "rembg is installed but its U2Net model (~176 MB) downloads from GitHub releases, blocked here (403)",
    "power:MEDIA-29": "Higgsfield generation, upscale, background removal and dubbing spend credits; only on explicit request",
    "power:MEDIA-33": "Ultralytics YOLO needs torch (not installed, ~769 MB CPU wheel)",
    "power:MEDIA-34": "pyannote.audio needs torch and a gated Hugging Face model with a user token",
    "power:MEDIA-38": "Mosamem is a desktop app for macOS and Windows (Tauri); KOSIF only links it",
    "power:MEDIA-40": "SAM 2.1 hiera-tiny weights are not downloaded (consent-gated, Hugging Face blocked here) and the "
                      "repo does not wrap SAM's decoder",
    "power:SELF-06": "ToolSearch is a tool of the agent session itself; a subprocess runner cannot call it",
    "power:SELF-09": "ListPlugins / SearchPlugins are agent-session tools; not callable from a runner",
    "power:SELF-10": "read_documentation is a cloud-session MCP tool of the agent; not callable from a runner",
    "power:SELF-28": "CPU torch is ~769 MB; installing it for a runner exceeds the size limit (and huggingface.co is blocked "
                     "here, so the small-file half cannot be shown either)",
    "power:SELF-39": "describes the Claude desktop app's environments and panes (macOS/Windows); nothing to run in a Linux "
                     "container",
    "power:VOICE-01": "piper is installed but the ar_JO-kareem voice (.onnx, 63 MB) is on huggingface.co, which the proxy "
                      "blocks (403); no voice model is cached",
    "power:VOICE-02": "voice.py speaks through Windows SAPI voices (Microsoft Naayf) via PowerShell; Windows only",
    "power:VOICE-03": "Kokoro's model (~311 MB) is on huggingface.co (blocked) and kokoro is not installed",
    "power:VOICE-04": "speechSynthesis output depends on the viewer's OS voices and cannot be captured by a headless render",
    "power:VOICE-05": "Edge neural voices are a live Microsoft service (speech.platform.bing.com is not reachable here)",
    "power:VOICE-06": "ElevenLabs text-to-speech needs ELEVENLABS_API_KEY (paid)",
    "power:VOICE-09": "voice cloning runs on ElevenLabs or HeyGen with paid keys and a consenting speaker's samples",
    "power:VOICE-10": "ElevenLabs speech-to-speech needs a paid key",
    "power:VOICE-11": "Gemini TTS needs a Gemini API key",
    "power:VOICE-13": "the multi-persona flow needs Claude for the script and Gemini TTS for every line (both keys); no "
                      "local Arabic voice model is available to stand in honestly",
    "power:VOICE-16": "Together's hosted TTS needs a paid key",
    "power:VOICE-30": "language-coach-arabic-english is an instruction-only skill (no scripts) and translation needs a "
                      "model; nothing to execute",
}


# ------------------------------------------------------------------------------------------------- helpers
def jw(path, obj):
    path = Path(path)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1, default=lambda o: float(o) if hasattr(o, "__float__") else str(o)),
                    encoding="utf-8")
    return path


def to8(a):
    return np.clip(np.rint(np.asarray(a, float) * 255), 0, 255).astype(np.uint8)


def save(a, p):
    Image.fromarray(to8(a)).save(str(p))
    return Path(p)


def load(p):
    return np.asarray(Image.open(str(p)).convert("RGB")).astype(float) / 255.0


def luma(a):
    a = np.asarray(a, float)
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def gblur(a, s):
    from scipy.ndimage import gaussian_filter
    a = np.asarray(a, float)
    if a.ndim == 3:
        return np.stack([gaussian_filter(a[..., c], s) for c in range(a.shape[2])], -1)
    return gaussian_filter(a, s)


def write_video(path, frames, fps=30, crf="17", extra=()):
    frames = [to8(f) for f in frames]
    h, w = frames[0].shape[:2]
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (w, h),
           "-r", str(fps), "-i", "-", "-c:v", "libx264", "-crf", crf, "-pix_fmt", "yuv420p", *extra, str(path)]
    done = subprocess.run(cmd, input=b"".join(f.tobytes() for f in frames), capture_output=True, timeout=60)
    if done.returncode:
        raise RuntimeError(done.stderr.decode(errors="replace")[-300:])
    return Path(path)


def font(size, path=None):
    return ImageFont.truetype(str(path or FONTS / "Cairo[slnt,wght].ttf"), int(size))


def nfkc(s):
    s = unicodedata.normalize("NFKC", s).replace("‎", "").replace("‏", "")
    return re.sub(r"\s+", " ", s).strip()


def ratio(a, b):
    return difflib.SequenceMatcher(None, nfkc(a), nfkc(b)).ratio()


def run(cmd, cwd=None, timeout=60, env=None, ok=(0,)):
    done = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, timeout=timeout, cwd=cwd, env=env,
                          stdin=subprocess.DEVNULL)
    if done.returncode not in ok:
        raise RuntimeError("command failed (%d): %s %s" % (done.returncode, " ".join(map(str, cmd))[:120], (done.stderr or done.stdout)[-400:]))
    return done


_PW_JS = r"""
const {chromium} = require('playwright'); const fs = require('fs'); const path = require('path');
const cfg = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const CT = {'.js':'text/javascript','.mjs':'text/javascript','.cjs':'text/javascript','.html':'text/html','.json':'application/json',
  '.css':'text/css','.png':'image/png','.jpg':'image/jpeg','.glb':'model/gltf-binary','.wasm':'application/wasm','.wav':'audio/wav',
  '.svg':'image/svg+xml','.ttf':'font/ttf','.woff2':'font/woff2','.pbf':'application/x-protobuf','.geojson':'application/json'};
function serve(r, fp) { if (fp && fs.existsSync(fp) && fs.statSync(fp).isFile()) return r.fulfill({status: 200, body: fs.readFileSync(fp),
  headers: {'content-type': CT[path.extname(fp)] || 'application/octet-stream', 'access-control-allow-origin': '*'}});
  return r.fulfill({status: 404, body: 'not found'}); }
(async () => {
  const b = await chromium.launch({args: ['--no-sandbox', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist',
    '--font-render-hinting=none', '--force-color-profile=srgb', '--disable-lcd-text', '--hide-scrollbars'].concat(cfg.args || [])});
  try {
    const p = await b.newPage({viewport: {width: cfg.w, height: cfg.h}, deviceScaleFactor: 1});
    const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    if (!cfg.real) await p.context().route('**/*', r => { const u = new URL(r.request().url());
      if (u.protocol === 'data:' || u.protocol === 'blob:') return r.continue();
      if (u.host === 'k') { const f = decodeURIComponent(u.pathname);
        for (const [pre, dir] of cfg.mounts) if (f.startsWith(pre)) return serve(r, path.join(dir, f.slice(pre.length)));
        return serve(r, null); }
      if (u.host === 'cdn.jsdelivr.net' && u.pathname.startsWith('/npm/')) {
        const parts = u.pathname.slice(5).split('/'); let name = parts.shift(); if (name.startsWith('@')) name += '/' + parts.shift();
        name = name.replace(/@[^/]*$/, ''); if (name.startsWith('@') && name.split('@').length > 2) name = '@' + name.split('@')[1];
        return serve(r, path.join(cfg.nm, name, parts.join('/'))); }
      if (u.host.endsWith('googleapis.com') || u.host.endsWith('gstatic.com')) return r.fulfill({status: 200, body: '', headers: {'content-type': 'text/css'}});
      return r.abort(); });
    await p.goto(cfg.url, {waitUntil: 'load', timeout: 20000});
    if (cfg.wait) try { await p.waitForFunction(cfg.wait, null, {timeout: cfg.timeout || 20000}); }
      catch (e) { throw new Error('wait timed out; page errors: ' + errs.slice(0, 5).join(' | ')); }
    const err = await p.evaluate('window.__err || null'); if (err) throw new Error('page: ' + err);
    const out = [];
    for (const s of cfg.steps) { if (s.vw) await p.setViewportSize({width: s.vw, height: s.vh});
      let v = null; if (s.js) v = await p.evaluate(s.js); if (s.shot) await p.screenshot({path: s.shot, fullPage: !!s.full}); out.push(v); }
    console.log(JSON.stringify({out, errs}));
  } finally { await b.close(); }
})().catch(e => { console.error(e.stack || String(e)); process.exit(1); });
"""


def pw(wd, page, steps, w=320, h=180, wait="window.__done === true || !!window.__err", html=None, mounts=None, timeout=25,
       url=None, args=()):
    """Open a page in Playwright's headless Chromium (SwiftShader WebGL). The page is served from http://k/w/ (the work
    folder); /kit/ is the vendored K3 kit, /nm/ the global node_modules, /fonts/ the shared fonts. Each step evaluates a
    JS expression (promises are awaited) and may take a screenshot; returns the list of step results."""
    wd = Path(wd)
    if html is not None:
        (wd / page).write_text(html, encoding="utf-8")
    runner = wd / "_pw.cjs"
    if not runner.exists():
        runner.write_text(_PW_JS, encoding="utf-8")
    m = [["/w/", str(wd)], ["/kit/", str(KIT)], ["/nm/", str(NM)], ["/fonts/", str(FONTS)]] + list(mounts or [])
    cfg = {"w": w, "h": h, "url": url or "http://k/w/" + page, "mounts": m, "nm": str(NM), "wait": wait,
           "timeout": timeout * 1000, "args": list(args),
           "steps": [dict(s, shot=str(wd / s["shot"]) if s.get("shot") else None) for s in steps]}
    cp = wd / ("_pw_%s.json" % Path(page).stem)
    cp.write_text(json.dumps(cfg), encoding="utf-8")
    done = subprocess.run([_NODE, str(runner), str(cp)], capture_output=True, text=True, timeout=timeout + 15, cwd=str(wd),
                          env={"NODE_PATH": str(NM), "PATH": "/usr/bin:/bin:" + str(Path(_NODE).parent), "HOME": str(wd),
                               "PLAYWRIGHT_BROWSERS_PATH": os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")},
                          stdin=subprocess.DEVNULL)
    if done.returncode:
        raise RuntimeError("browser failed: %s" % done.stderr[-700:])
    res = json.loads(done.stdout.strip().splitlines()[-1])
    return res["out"]


def data_url_to_png(u, path):
    Path(path).write_bytes(base64.b64decode(u.split(",", 1)[1]))
    return Path(path)


def png_arr(path):
    return np.asarray(Image.open(str(path)).convert("RGB")).astype(float)


THREE_HEAD = """<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:#000}canvas{display:block}</style>
<script type="importmap">{"imports":{"three":"http://k/nm/three/build/three.module.js","three/addons/":"http://k/nm/three/examples/jsm/"}}</script>
</head><body><canvas id="c" width="%d" height="%d"></canvas>"""


def three_page(w, h, module_js):
    """A page with an ES-module three.js scene; the module sets window.__result and window.__done."""
    lines = module_js.strip("\n").splitlines()
    imports = "\n".join(l for l in lines if l.startswith("import "))
    module_js = "\n".join(l for l in lines if not l.startswith("import "))
    return (THREE_HEAD % (w, h)) + """<script type="module">
import * as THREE from 'three';
""" + imports + """
const cv = document.getElementById('c');
function px(renderer, x, y) { const gl = renderer.getContext(); const b = new Uint8Array(4); gl.readPixels(x, %d - 1 - y, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, b); return [b[0], b[1], b[2]]; }
function grab(renderer) { return renderer.domElement.toDataURL('image/png'); }
try {
%s
} catch (e) { window.__err = String(e.stack || e); }
</script></body></html>""" % (h, module_js)


K3_HEAD = """<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:#000}canvas{display:block}</style>
</head><body><canvas id="c" width="%d" height="%d"></canvas>
<script src="http://k/kit/three-kit.bundle.js"></script>%s<script>
const cv = document.getElementById('c'), T = K3.THREE;
function grab(r) { return r.domElement.toDataURL('image/png'); }
(async () => { try {
%s
} catch (e) { window.__err = String(e.stack || e); } })();
</script></body></html>"""


def k3_page(w, h, js, extra=""):
    return K3_HEAD % (w, h, extra, js)


# ================================================================================================ 3D / spatial
def _matrix_z(js_sel):
    return "[...document.querySelectorAll('%s')].map(e => new DOMMatrix(getComputedStyle(e).transform).m43)" % js_sel


@card("3D-09")
def preserve3d_camera_legs(task, wd):
    """A preserve-3d world tweened leg by leg from one camera state (landings power4.out, repositions power2.inOut);
    40 chips scatter into a depth cloud (perspective 1400px, index-derived offsets, cloud spin power1.out) and settle to a
    flat grid; DOF is a --dof variable on each leaf, blur = clamp(|z|/40, 0, 14) px. Chrome seeks the paused GSAP timeline
    and reads every chip's computed matrix."""
    n = 40
    html = """<!doctype html><html><head><style>html,body{margin:0;background:#0b0f17;overflow:hidden}
#view{position:absolute;inset:0;perspective:1400px}#world{position:absolute;left:50%;top:50%;transform-style:preserve-3d}
.chip{position:absolute;width:40px;height:26px;margin:-13px 0 0 -20px;background:#8ad;border-radius:5px;transform-style:preserve-3d;filter:blur(var(--dof,0px))}
</style></head><body><div id="view"><div id="world"></div></div>
<script src="http://k/nm/gsap/dist/gsap.min.js"></script><script>
const N = __N__, world = document.getElementById('world'), chips = [];
for (let i = 0; i < N; i++) { const c = document.createElement('div'); c.className = 'chip'; world.appendChild(c); chips.push(c); }
const grid = i => ({x: (i % 8 - 3.5) * 56, y: (Math.floor(i / 8) - 2) * 40});
const cloud = i => ({x: ((i * 73) % 41 - 20) * 14, y: ((i * 29) % 23 - 11) * 14, z: ((i * 37) % 21 - 10) * 70});
const cam = {rx: 0, ry: 0, z: 0};
function applyCam() { world.style.transform = `translateZ(${cam.z}px) rotateX(${cam.rx}deg) rotateY(${cam.ry}deg)`; }
function dof() { chips.forEach(c => { const z = +gsap.getProperty(c, 'z'); c.style.setProperty('--dof', Math.min(14, Math.abs(z) / 40).toFixed(3) + 'px'); }); }
chips.forEach((c, i) => gsap.set(c, {x: grid(i).x, y: grid(i).y, z: 0}));
const tl = gsap.timeline({paused: true, onUpdate: () => { applyCam(); dof(); }});
tl.to(cam, {rx: 55, z: 300, duration: 1.0, ease: 'power4.out'}, 0)              // leg 1: dive into the tilted grid
  .to(cam, {rx: 20, z: -400, duration: 1.0, ease: 'power2.inOut'}, 1.0)          // leg 2: pull back
  .to(chips, {x: i => cloud(i).x, y: i => cloud(i).y, z: i => cloud(i).z, duration: 1.2, ease: 'power1.out'}, 2.0)  // scatter
  .to(cam, {ry: 40, duration: 1.2, ease: 'power1.out'}, 2.0)                     // cloud spin
  .to(chips, {x: i => grid(i).x, y: i => grid(i).y, z: 0, duration: 1.0, ease: 'power4.out'}, 3.4)  // assemble flat
  .to(cam, {rx: 0, ry: 0, z: 0, duration: 1.0, ease: 'power4.out'}, 3.4);         // slow to focus
window.tl = tl; applyCam(); window.__done = true;
</script></body></html>""".replace("__N__", str(n))
    zs = _matrix_z(".chip")
    meas = "({t: tl.time(), z: %s, x: [...document.querySelectorAll('.chip')].map(e => +gsap.getProperty(e,'x')), blur: [...document.querySelectorAll('.chip')].map(e => parseFloat(e.style.getPropertyValue('--dof')||0)), cam: {rx: cam.rx, ry: cam.ry, z: cam.z}})" % zs
    r = pw(wd, "world.html", [{"js": "tl.seek(0, false); " + meas}, {"js": "tl.seek(1.0, false); " + meas}, {"js": "tl.seek(2.0, false); " + meas},
                              {"js": "tl.seek(3.2, false); " + meas, "shot": "scatter.png"}, {"js": "tl.seek(4.4, false); " + meas, "shot": "settled.png"}],
           w=480, h=270, html=html)
    t0, l1, l2, peak, end = r
    spread = lambda s: max(s["z"]) - min(s["z"])
    expected_z = [((i * 37) % 21 - 10) * 70 for i in range(n)]
    grid_x = [(i % 8 - 3.5) * 56 for i in range(n)]
    corr = max(abs(b - min(14, abs(z) / 40)) for z, b in zip(peak["z"], peak["blur"]))
    jw(wd / "world_measure.json", r)
    return [
        check("leg 1 lands exactly on its camera state (rx 55, z 300)", abs(l1["cam"]["rx"] - 55) < 1e-6 and abs(l1["cam"]["z"] - 300) < 1e-6, l1["cam"], {"rx": 55, "z": 300}),
        check("leg 2 lands on the pull-back state (rx 20, z -400)", abs(l2["cam"]["rx"] - 20) < 1e-6 and abs(l2["cam"]["z"] + 400) < 1e-6, l2["cam"], {"rx": 20, "z": -400}),
        check("depth cloud: computed translateZ equals the index-derived offsets", max(abs(a - b) for a, b in zip(peak["z"], expected_z)) < 0.5, max(abs(a - b) for a, b in zip(peak["z"], expected_z)), "< 0.5 px"),
        check("depth spread of the cloud >= 1000 px", spread(peak) >= 1000, spread(peak), ">= 1000"),
        check("DOF blur = clamp(|z| / 40, 0, 14) px on every chip", corr < 0.01 and max(peak["blur"]) > 5, [corr, max(peak["blur"])], "max |diff| < 0.01"),
        check("assembled: every chip back at z 0 on the flat grid", max(map(abs, end["z"])) < 0.01 and max(abs(a - b) for a, b in zip(end["x"], grid_x)) < 0.01,
              [max(map(abs, end["z"])), max(abs(a - b) for a, b in zip(end["x"], grid_x))], "< 0.01"),
        check("negative control: the untreated start has no depth spread", spread(t0) < 0.01, spread(t0), "< 0.01"),
    ], [wd / "scatter.png", wd / "settled.png", wd / "world_measure.json"]


@card("3D-11")
def orbit_rings(task, wd):
    """Two elliptical rings behind a hero: ::before rotateX(18deg) rotateZ(-20deg); ::after orbit-reveal from rotate(-10deg)
    scaleY(.25) to rotate(-35deg) scaleY(.46) over 1.5 s, atmosphere scale .86 -> 1; nodes lift translateZ(40px)
    scale(1.08) in .35 s. Chrome seeks the CSS animations and decomposes the computed matrices."""
    html = """<!doctype html><html><head><style>html,body{margin:0;background:#0d1117}
.hero{position:absolute;left:110px;top:40px;width:250px;height:220px;perspective:900px;transform-style:preserve-3d;animation:atm 1.5s cubic-bezier(.2,.7,.1,1) both}
.hero::before{content:'';position:absolute;inset:0;width:250px;height:250px;border-radius:50%;border:2px solid #d9f3c730;transform:rotateX(18deg) rotateZ(-20deg);box-shadow:0 0 30px #d9f3c730}
.hero::after{content:'';position:absolute;left:1px;top:15px;width:248px;height:220px;border-radius:50%;border:2px solid #cec1e13d;animation:orbit 1.5s cubic-bezier(.2,.7,.1,1) both}
@keyframes orbit{from{transform:rotate(-10deg) scaleY(.25)}to{transform:rotate(-35deg) scaleY(.46)}}
@keyframes atm{from{transform:scale(.86)}to{transform:scale(1)}}
.node{position:absolute;width:18px;height:18px;border-radius:50%;background:#9be7c4;transition:transform .35s cubic-bezier(.2,.7,.1,1);transform:translateZ(0) scale(1)}
.node.lift{transform:translateZ(40px) scale(1.08)}
</style></head><body><div class="hero"><div class="node" style="left:20px;top:100px"></div><div class="node" style="left:200px;top:60px"></div></div>
<script>window.__done = true;</script></body></html>"""
    seek = ("(ms) => { document.getAnimations().forEach(a => { a.pause(); a.currentTime = ms; }); }")
    dec = ("(m) => { m = new DOMMatrix(m); return {rot: Math.atan2(m.b, m.a) * 180 / Math.PI, sy: Math.hypot(m.c, m.d), sx: Math.hypot(m.a, m.b), "
           "m43: m.m43, all: Array.from(m.toFloat64Array())}; }")
    js = ("(() => { const seek = %s, dec = %s; seek(%%d); const h = document.querySelector('.hero');"
          "return {after: dec(getComputedStyle(h, '::after').transform), before: dec(getComputedStyle(h, '::before').transform), hero: dec(getComputedStyle(h).transform)}; })()") % (seek, dec)
    lift = ("(async () => { const n = document.querySelector('.node'); n.classList.add('lift'); await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));"
            "document.getAnimations().forEach(a => { a.pause(); a.currentTime = %d; }); const m = new DOMMatrix(getComputedStyle(n).transform); return {m43: m.m43, s: Math.hypot(m.m11, m.m12, m.m13)}; })()")
    r = pw(wd, "rings.html", [{"js": js % 0}, {"js": js % 1500, "shot": "rings.png"}, {"js": lift % 0}, {"js": lift % 350}], w=480, h=300, html=html)
    a0, a1, l0, l1 = r
    ax, az = math.radians(18), math.radians(-20)
    RX = np.array([[1, 0, 0], [0, math.cos(ax), -math.sin(ax)], [0, math.sin(ax), math.cos(ax)]])
    RZ = np.array([[math.cos(az), -math.sin(az), 0], [math.sin(az), math.cos(az), 0], [0, 0, 1]])
    want = RX @ RZ                                   # CSS applies rotateX(18deg) rotateZ(-20deg) left to right
    got = np.array(a1["before"]["all"]).reshape(4, 4).T[:3, :3]
    rx = float(np.abs(got - want).max())
    jw(wd / "rings_measure.json", r)
    return [
        check("::after ends at rotate(-35deg)", abs(a1["after"]["rot"] + 35) < 0.05, a1["after"]["rot"], -35),
        check("::after ends at scaleY(.46)", abs(a1["after"]["sy"] - 0.46) < 1e-3, a1["after"]["sy"], 0.46),
        check("orbit-reveal starts at rotate(-10deg) scaleY(.25)", abs(a0["after"]["rot"] + 10) < 0.05 and abs(a0["after"]["sy"] - 0.25) < 1e-3, [a0["after"]["rot"], a0["after"]["sy"]], [-10, 0.25]),
        check("::before matrix equals rotateX(18deg) rotateZ(-20deg)", rx < 1e-4, rx, "max |diff| < 1e-4"),
        check("atmosphere scales .86 -> 1", abs(a0["hero"]["sx"] - 0.86) < 1e-3 and abs(a1["hero"]["sx"] - 1) < 1e-3, [a0["hero"]["sx"], a1["hero"]["sx"]], [0.86, 1]),
        check("node lifts to translateZ(40px) scale(1.08) after .35 s", abs(l1["m43"] - 40) < 0.01 and abs(l1["s"] - 1.08) < 1e-3, l1, {"m43": 40, "s": 1.08}),
        check("negative control: before the lift the node sits at z 0, scale 1", abs(l0["m43"]) < 0.01 and abs(l0["s"] - 1) < 1e-3, l0, {"m43": 0, "s": 1}),
    ], [wd / "rings.png", wd / "rings_measure.json"]


def _hf_add(wd, *names):
    d = Path(wd) / "hf"
    d.mkdir(exist_ok=True)
    out = run(["hyperframes", "add", *names, "--dir", d, "--no-clipboard", "--json"], timeout=60,
              env=dict(os.environ, HOME=str(wd)))
    return d, out.stdout


@card("3D-13")
def hf_depth_blocks(task, wd):
    """`hyperframes add camera-rig-depth-stack tilt-card` installs the registry blocks as editable source; the depth stack is
    driven by its documented paused-timeline tween (--hf-rotate-y -20 -> 10deg, --hf-rotate-x 12 -> -4deg, --hf-z -80 -> 80px,
    power3.out, 1.2 s). Chrome seeks it and reads the panel's computed 3D matrix."""
    d, log = _hf_add(wd, "camera-rig-depth-stack", "tilt-card")
    comp = d / "compositions/components/camera-rig-depth-stack.html"
    src = comp.read_text(encoding="utf-8")
    html = """<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:#fff}</style></head><body>
%s
<script src="http://k/nm/gsap/dist/gsap.min.js"></script><script>
const tl = gsap.timeline({paused: true});
tl.fromTo('.hf-advanced-camera-rig-depth-stack .panel', {'--hf-rotate-y': '-20deg', '--hf-rotate-x': '12deg', '--hf-z': '-80px', opacity: 0},
  {'--hf-rotate-y': '10deg', '--hf-rotate-x': '-4deg', '--hf-z': '80px', opacity: 1, duration: 1.2, ease: 'power3.out'}, 0);
window.tl = tl; window.__done = true;
</script></body></html>""" % src
    meas = ("(() => { const p = document.querySelector('.panel'); const m = new DOMMatrix(getComputedStyle(p).transform);"
            "return {m43: m.m43, ry: Math.asin(-m.m13) * 180 / Math.PI, op: +getComputedStyle(p).opacity, w: p.getBoundingClientRect().width}; })()")
    r = pw(wd, "depth.html", [{"js": "tl.seek(0, false); " + meas}, {"js": "tl.seek(0.6); " + meas}, {"js": "tl.seek(1.2); " + meas, "shot": "depth_end.png"}],
           w=800, h=470, html=html)
    s0, mid, s1 = r
    p3 = lambda x: 1 - (1 - x) ** 4
    # m43 of rotateY(ry) rotateX(rx) translateZ(z) = z * cos(ry) * cos(rx)
    exp_end = 80 * math.cos(math.radians(10)) * math.cos(math.radians(-4))
    exp_start = -80 * math.cos(math.radians(-20)) * math.cos(math.radians(12))
    zmid = -80 + 160 * p3(0.5)
    jw(wd / "depth_measure.json", {"frames": r, "added": log[-2000:]})
    return [
        check("registry blocks installed as editable source", comp.exists() and (d / "compositions/components/tilt-card.html").exists() and "perspective" in src,
              comp.exists(), True),
        check("end state: translateZ 80px seen through rotateY 10 / rotateX -4", abs(s1["m43"] - exp_end) < 0.05, s1["m43"], exp_end),
        check("end state rotateY = 10deg", abs(s1["ry"] - 10) < 0.05, s1["ry"], 10),
        check("power3.out at half time: z = -80 + 160 * (1 - 0.5^4)", abs(mid["m43"] / (math.cos(math.radians(-20 + 30 * p3(.5))) * math.cos(math.radians(12 - 16 * p3(.5)))) - zmid) < 0.2,
              mid["m43"], zmid),
        check("panel fades 0 -> 1", s0["op"] < 1e-3 and abs(s1["op"] - 1) < 1e-3, [s0["op"], s1["op"]], [0, 1]),
        check("negative control: the start state is behind the plane (z < 0), not the end state", s0["m43"] < 0 and abs(s0["m43"] - exp_start) < 0.05, s0["m43"], exp_start),
    ], [wd / "depth_end.png", wd / "depth_measure.json", comp]


@card("3D-14")
def k3_tone_renderer(task, wd):
    """The pre-bundled window.K3 kit: makeRenderer(canvas, W, H, {tone: aces|agx|neutral, exposure .6}) renders the same HDR
    scene (emissive patches 0.25 / 1 / 4 / 16) through each tone curve; NoToneMapping is the untreated control."""
    js = """
const W = 320, H = 80, out = {};
for (const tone of ['aces', 'agx', 'neutral', 'none']) {
  const r = K3.makeRenderer(cv, W, H, {tone: tone === 'none' ? 'aces' : tone, exposure: 0.6});
  if (tone === 'none') { r.toneMapping = T.NoToneMapping; r.toneMappingExposure = 1; }
  const s = new T.Scene(); s.background = new T.Color(0, 0, 0);
  const cam = new T.OrthographicCamera(0, 4, 1, 0, -1, 1);
  [0.25, 1, 4, 16].forEach((v, i) => { const m = new T.Mesh(new T.PlaneGeometry(1, 1), new T.MeshBasicMaterial({color: new T.Color(v, v * 0.6, v * 0.3)}));
    m.position.set(i + 0.5, 0.5, 0); s.add(m); });
  r.render(s, cam);
  const gl = r.getContext(), b = new Uint8Array(4), vals = [];
  for (let i = 0; i < 4; i++) { gl.readPixels(Math.round((i + 0.5) * W / 4), H / 2, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, b); vals.push([b[0], b[1], b[2]]); }
  out[tone] = {vals, tm: r.toneMapping, exp: r.toneMappingExposure, png: grab(r)};
  r.dispose();
}
window.__result = out; window.__done = true;
"""
    r = pw(wd, "tone.html", [{"js": "window.__result"}], w=320, h=80, html=k3_page(320, 80, js))[0]
    for k in r:
        data_url_to_png(r[k]["png"], wd / ("tone_%s.png" % k))
    v = {k: [p[0] for p in r[k]["vals"]] for k in r}
    mono = all(all(a < b for a, b in zip(v[k], v[k][1:])) for k in ("aces", "agx", "neutral"))
    jw(wd / "tone_measure.json", {k: {"red": v[k], "toneMapping": r[k]["tm"], "exposure": r[k]["exp"]} for k in r})
    return [
        check("three tone curves are distinct THREE tone-mapping modes", len({r[k]["tm"] for k in ("aces", "agx", "neutral")}) == 3, [r[k]["tm"] for k in ("aces", "agx", "neutral")], "3 distinct"),
        check("exposure .6 is the kit default", all(abs(r[k]["exp"] - 0.6) < 1e-6 for k in ("aces", "agx", "neutral")), [r[k]["exp"] for k in ("aces", "agx", "neutral")], 0.6),
        check("tone-mapped red channel rises strictly 0.25 < 1 < 4 < 16 (highlights not clipped flat)", mono, v, "strictly increasing"),
        check("the curves differ on the same HDR value 4.0", len({v["aces"][2], v["agx"][2], v["neutral"][2]}) == 3, [v["aces"][2], v["agx"][2], v["neutral"][2]], "3 values"),
        check("negative control: without a tone curve 4 and 16 both clip to 255", v["none"][2] == 255 and v["none"][3] == 255, v["none"], "[.., 255, 255]"),
    ], [wd / "tone_aces.png", wd / "tone_agx.png", wd / "tone_neutral.png", wd / "tone_measure.json"]


@card("3D-17")
def portal_render_target(task, wd):
    """An offscreen scene rendered into a WebGLRenderTarget (the plain-three form of R3F createPortal + useFBO), sampled on a
    plane in screen space (gl_FragCoord.xy / resolution); the portal camera copies the main camera's matrix each frame
    (parallax) and the portal pass runs before the main pass."""
    js = """
const W = 320, H = 180;
const renderer = new THREE.WebGLRenderer({canvas: cv, preserveDrawingBuffer: true}); renderer.setSize(W, H, false); renderer.setPixelRatio(1);
const rt = new THREE.WebGLRenderTarget(W, H);
const portal = new THREE.Scene(); portal.background = new THREE.Color(0x1060ff);
const cube = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.6, 0.6), new THREE.MeshBasicMaterial({color: 0xff2020})); cube.position.z = -3; portal.add(cube);
const pcam = new THREE.PerspectiveCamera(45, W / H, 0.1, 50);
const main = new THREE.Scene(); main.background = new THREE.Color(0x000000);
const cam = new THREE.PerspectiveCamera(45, W / H, 0.1, 50); cam.position.set(0, 0, 3);
const mat = new THREE.ShaderMaterial({uniforms: {map: {value: rt.texture}, res: {value: new THREE.Vector2(W, H)}},
  vertexShader: 'void main(){ gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
  fragmentShader: 'uniform sampler2D map; uniform vec2 res; void main(){ gl_FragColor = texture2D(map, gl_FragCoord.xy / res); }'});
const plane = new THREE.Mesh(new THREE.PlaneGeometry(1.6, 1.0), mat); main.add(plane);
function frame(x, withPortal) {
  cam.position.x = x; cam.lookAt(0, 0, 0); cam.updateMatrixWorld();
  pcam.matrixWorld.copy(cam.matrixWorld); pcam.matrixWorld.decompose(pcam.position, pcam.quaternion, pcam.scale); pcam.updateMatrixWorld(true);
  renderer.setRenderTarget(rt); renderer.setClearColor(0x000000, 1); if (withPortal) renderer.render(portal, pcam); else renderer.clear();
  renderer.setRenderTarget(null); renderer.render(main, cam);
  const gl = renderer.getContext(), buf = new Uint8Array(W * H * 4); gl.readPixels(0, 0, W, H, gl.RGBA, gl.UNSIGNED_BYTE, buf);
  let rx = 0, rn = 0, blue = 0, inside = 0, outsideDark = 0, outside = 0;
  for (let y = 0; y < H; y++) for (let x2 = 0; x2 < W; x2++) { const i = (y * W + x2) * 4, r = buf[i], g = buf[i + 1], b = buf[i + 2];
    const inP = Math.abs(x2 - W / 2) < 60 && Math.abs(y - H / 2) < 34;
    if (inP) { inside++; if (b > 200 && r < 60) blue++; if (r > 200 && b < 80) { rx += x2; rn++; } }
    else if (Math.abs(x2 - W / 2) > 110) { outside++; if (r + g + b < 10) outsideDark++; } }
  return {red_cx: rn ? rx / rn : null, red_n: rn, blue_frac: blue / inside, outside_dark: outsideDark / outside, png: grab(renderer)};
}
const a = frame(0, true), b = frame(0.8, true), neg = frame(0, false);
window.__result = {a, b, neg}; window.__done = true;
"""
    r = pw(wd, "portal.html", [{"js": "window.__result"}], w=320, h=180, html=three_page(320, 180, js))[0]
    for k in ("a", "b", "neg"):
        data_url_to_png(r[k].pop("png"), wd / ("portal_%s.png" % k))
    a, b, neg = r["a"], r["b"], r["neg"]
    jw(wd / "portal_measure.json", r)
    return [
        check("the plane shows the portal scene (blue background inside the plane)", a["blue_frac"] > 0.5, a["blue_frac"], "> 0.5"),
        check("the portal's red cube is visible through the plane", a["red_n"] > 30, a["red_n"], "> 30 px"),
        check("outside the plane the main scene stays black", a["outside_dark"] > 0.99, a["outside_dark"], "> 0.99"),
        check("parallax: moving the main camera shifts the portal content", b["red_cx"] is not None and abs(b["red_cx"] - a["red_cx"]) > 5, [a["red_cx"], b["red_cx"]], "> 5 px shift"),
        check("negative control: without the portal pass the plane is empty", neg["blue_frac"] < 0.01 and neg["red_n"] == 0, [neg["blue_frac"], neg["red_n"]], [0, 0]),
    ], [wd / "portal_a.png", wd / "portal_b.png", wd / "portal_measure.json"]


_CRYSTAL_JS = r"""
function rng(seed) { let a = seed >>> 0 || 1; return () => { a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
function shardCount(o) { return Math.max(6, Math.round((o.phone ? 14 : 30) * (o.weak ? 0.7 : 1) * (o.density == null ? 1 : o.density))); }
function shard(r) {   // irregular hexagonal prism (6 sides, irregularity .45) with pointed caps; flat per-face normals
  const ring = [], h = 0.6 + r() * 0.8, rad = 0.25 + r() * 0.2;
  for (let i = 0; i < 6; i++) { const a = i / 6 * Math.PI * 2 + (r() - 0.5) * 0.45, k = rad * (1 + (r() - 0.5) * 0.45); ring.push([Math.cos(a) * k, Math.sin(a) * k]); }
  const top = [0, 0, h / 2 + 0.3 + r() * 0.3], bot = [0, 0, -h / 2 - 0.3 - r() * 0.3], tris = [];
  for (let i = 0; i < 6; i++) { const a = ring[i], b = ring[(i + 1) % 6];
    const a0 = [a[0], a[1], -h / 2], b0 = [b[0], b[1], -h / 2], a1 = [a[0], a[1], h / 2], b1 = [b[0], b[1], h / 2];
    tris.push([a0, b0, b1], [a0, b1, a1], [a1, b1, top], [b0, a0, bot]); }
  const pos = [], nor = [];
  for (const t of tris) { const u = t[1].map((v, i) => v - t[0][i]), w = t[2].map((v, i) => v - t[0][i]);
    const n = [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]], l = Math.hypot(...n);
    for (const p of t) { pos.push(...p); nor.push(n[0] / l, n[1] / l, n[2] / l); } }
  return {pos, nor};
}
function mount(canvas, o) {
  const gl = canvas.getContext('webgl', {preserveDrawingBuffer: true, antialias: false});
  const r = rng(o.seed), N = shardCount(o), shards = [];
  for (let i = 0; i < N; i++) shards.push({g: shard(r), x: (r() - 0.5) * 14, y: (r() - 0.5) * 8, z: -4 - r() * 14,
    spin: (r() < 0.5 ? -1 : 1) * (0.12 + r() * 0.2), ph: r() * 6.28, hue: r()});
  const vs = `attribute vec3 p; attribute vec3 n; uniform mat4 M, P; varying vec3 vn; varying float vz;
    void main(){ vec4 w = M * vec4(p, 1.0); vn = mat3(M) * n; vz = -w.z; gl_Position = P * w; }`;
  const fs = `precision mediump float; varying vec3 vn; varying float vz; uniform vec3 col;
    void main(){ float l = 0.25 + 0.75 * max(dot(normalize(vn), normalize(vec3(0.4, 0.6, 0.7))), 0.0);
      float fog = clamp((vz - 4.0) / 16.0, 0.0, 1.0); gl_FragColor = vec4(mix(col * l, vec3(0.05, 0.06, 0.1), fog), 1.0); }`;
  const sh = (t, s) => { const x = gl.createShader(t); gl.shaderSource(x, s); gl.compileShader(x); return x; };
  const pr = gl.createProgram(); gl.attachShader(pr, sh(gl.VERTEX_SHADER, vs)); gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, fs)); gl.linkProgram(pr); gl.useProgram(pr);
  const bp = gl.createBuffer(), bn = gl.createBuffer(), lp = gl.getAttribLocation(pr, 'p'), ln = gl.getAttribLocation(pr, 'n');
  const asp = canvas.width / canvas.height, f = 1 / Math.tan(0.5), P = [f / asp, 0, 0, 0, 0, f, 0, 0, 0, 0, -1.01, -1, 0, 0, -0.2, 0];
  gl.uniformMatrix4fv(gl.getUniformLocation(pr, 'P'), false, P); gl.enable(gl.DEPTH_TEST);
  function frames(t) { gl.viewport(0, 0, canvas.width, canvas.height); gl.clearColor(0.05, 0.06, 0.1, 1); gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    for (const s of shards) { const a = s.ph + s.spin * t, c = Math.cos(a), sn = Math.sin(a), bob = Math.sin(t * 0.7 + s.ph) * 0.2;
      const M = [c, 0, -sn, 0, 0, 1, 0, 0, sn, 0, c, 0, s.x, s.y + bob, s.z, 1];
      gl.uniformMatrix4fv(gl.getUniformLocation(pr, 'M'), false, M); gl.uniform3f(gl.getUniformLocation(pr, 'col'), 0.5 + 0.4 * s.hue, 0.7, 0.95);
      gl.bindBuffer(gl.ARRAY_BUFFER, bp); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(s.g.pos), gl.STATIC_DRAW); gl.enableVertexAttribArray(lp); gl.vertexAttribPointer(lp, 3, gl.FLOAT, false, 0, 0);
      gl.bindBuffer(gl.ARRAY_BUFFER, bn); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(s.g.nor), gl.STATIC_DRAW); gl.enableVertexAttribArray(ln); gl.vertexAttribPointer(ln, 3, gl.FLOAT, false, 0, 0);
      gl.drawArrays(gl.TRIANGLES, 0, s.g.pos.length / 3); }
    const b = new Uint8Array(canvas.width * canvas.height * 4); gl.readPixels(0, 0, canvas.width, canvas.height, gl.RGBA, gl.UNSIGNED_BYTE, b);
    let hsh = 2166136261; for (let i = 0; i < b.length; i += 7) hsh = Math.imul(hsh ^ b[i], 16777619) >>> 0; return hsh; }
  return {frames, shards, destroy() {}, gl: gl instanceof WebGLRenderingContext && !(window.WebGL2RenderingContext && gl instanceof WebGL2RenderingContext)};
}
"""


@card("3D-18")
def crystal_shards_webgl1(task, wd):
    """A library-free WebGL1 scene of drifting low-poly crystal shards, deterministic per seed: each shard is an irregular
    hexagonal prism (6 sides, irregularity .45) with pointed caps and flat per-face normals, 24 triangles / 72 vertices;
    N = round((phone ? 14 : 30) * (weak ? .7 : 1) * density) >= 6; z slab -4..-18; spin +-(.12..); fog."""
    html = """<!doctype html><html><body style="margin:0"><canvas id="c" width="320" height="180"></canvas><script>%s
const cv = document.getElementById('c');
const A = mount(cv, {seed: 7}), hA = A.frames(1.5), png = cv.toDataURL('image/png'), hA2 = A.frames(1.5), hA3 = A.frames(3.0);
const B = mount(cv, {seed: 8}), hB = B.frames(1.5);
const st = A.shards.map(s => ({tris: s.g.pos.length / 9, verts: s.g.pos.length / 3, z: s.z, spin: s.spin,
  flat: (() => { let bad = 0; for (let t = 0; t < s.g.nor.length; t += 9) { for (let k = 3; k < 9; k += 3) for (let j = 0; j < 3; j++) if (Math.abs(s.g.nor[t + k + j] - s.g.nor[t + j]) > 1e-9) bad++;
    if (Math.abs(Math.hypot(s.g.nor[t], s.g.nor[t + 1], s.g.nor[t + 2]) - 1) > 1e-6) bad++; } return bad; })()}));
window.__result = {hA, hA2, hA3, hB, png, webgl1: A.gl, st,
  counts: [shardCount({}), shardCount({phone: true}), shardCount({phone: true, weak: true}), shardCount({density: 0.1}), shardCount({density: 2})]};
window.__done = true;
</script></body></html>""" % _CRYSTAL_JS
    r = pw(wd, "crystal.html", [{"js": "window.__result"}], html=html)[0]
    data_url_to_png(r.pop("png"), wd / "crystal.png")
    st = r["st"]
    im = png_arr(wd / "crystal.png")
    lit = float((luma(im / 255) > 0.2).mean())
    jw(wd / "crystal_measure.json", r)
    return [
        check("pure WebGL1 context (no library)", r["webgl1"] is True, r["webgl1"], True),
        check("every shard: 24 triangles / 72 vertices", all(s["tris"] == 24 and s["verts"] == 72 for s in st), sorted({(s["tris"], s["verts"]) for s in st}), [(24, 72)]),
        check("flat per-face unit normals", sum(s["flat"] for s in st) == 0, sum(s["flat"] for s in st), 0),
        check("shard count formula: 30 / 14 / round(14*.7)=10 / floor 6 / 60", r["counts"] == [30, 14, 10, 6, 60], r["counts"], [30, 14, 10, 6, 60]),
        check("z slab -4..-18 and |spin| >= .12", all(-18 <= s["z"] <= -4 and abs(s["spin"]) >= 0.12 for s in st), [min(s["z"] for s in st), max(s["z"] for s in st)], "[-18, -4]"),
        check("deterministic: same seed and time give the same pixels", r["hA"] == r["hA2"], [r["hA"], r["hA2"]], "equal"),
        check("shards are drawn (lit pixels 2..60 %)", 0.02 < lit < 0.6, lit, "0.02..0.6"),
        check("negative control: another seed and another time give other pixels", r["hB"] != r["hA"] and r["hA3"] != r["hA"], [r["hA"], r["hB"], r["hA3"]], "different"),
    ], [wd / "crystal.png", wd / "crystal_measure.json"]


@card("3D-22")
def glb_seek_animation(task, wd):
    """A GLB with an object animation is made with three's GLTFExporter (binary), written into the work folder, loaded with
    K3.loadModel(url, {clip, offset, speed}) and seeked to absolute time with m.userData.set(t) -> mixer.setTime."""
    page = """<!doctype html><html><head><meta charset="utf-8">
<script type="importmap">{"imports":{"three":"http://k/nm/three/build/three.module.js","three/examples/jsm/":"http://k/nm/three/examples/jsm/","three/addons/":"http://k/nm/three/examples/jsm/"}}</script>
</head><body><script src="http://k/kit/three-kit.bundle.js"></script><script type="module">
import * as THREE from 'three'; import { GLTFExporter } from 'three/addons/exporters/GLTFExporter.js';
try {
  const box = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), new THREE.MeshStandardMaterial({color: 0xff8800})); box.name = 'crate';
  const track = new THREE.VectorKeyframeTrack('crate.position', [0, 2], [0, 0, 0, 4, 0, 0]);
  const spin = new THREE.NumberKeyframeTrack('crate.rotation[y]', [0, 2], [0, Math.PI]);
  const clip = new THREE.AnimationClip('slide', 2, [track]);
  const scene = new THREE.Scene(); scene.add(box);
  const glb = await new GLTFExporter().parseAsync(scene, {binary: true, animations: [clip]});
  const bytes = new Uint8Array(glb); let s = ''; for (let i = 0; i < bytes.length; i++) s += String.fromCharCode(bytes[i]);
  const url = 'data:model/gltf-binary;base64,' + btoa(s);
  const pos = async (o, t) => { const m = await K3.loadModel(url, o); m.userData.set(t); m.updateMatrixWorld(true); const c = m.getObjectByName('crate'); return [c.position.x, m.userData.clips]; };
  window.__result = {b64: btoa(s), bytes: bytes.length, magic: String.fromCharCode(bytes[0], bytes[1], bytes[2], bytes[3]),
    t0: await pos({}, 0), t05: await pos({}, 0.5), t15: await pos({}, 1.5), off: await pos({offset: 0.5}, 0.5), spd: await pos({speed: 2}, 0.5), clipsel: await pos({clip: 'slide'}, 1.0)};
  window.__done = true;
} catch (e) { window.__err = String(e.stack || e); }
</script></body></html>"""
    r = pw(wd, "glb.html", [{"js": "window.__result"}], html=page)[0]
    (wd / "crate.glb").write_bytes(base64.b64decode(r.pop("b64")))
    raw = (wd / "crate.glb").read_bytes()
    ver, total = struct.unpack("<II", raw[4:12])
    jlen = struct.unpack("<I", raw[12:16])[0]
    gj = json.loads(raw[20:20 + jlen])
    jw(wd / "glb_measure.json", r)
    x = lambda k: r[k][0]
    return [
        check("a binary glTF 2.0 file was written (magic glTF, v2, length matches)", raw[:4] == b"glTF" and ver == 2 and total == len(raw), [raw[:4].decode(), ver, total, len(raw)], ["glTF", 2, len(raw)]),
        check("the GLB carries the 'slide' animation", [a.get("name") for a in gj.get("animations", [])] == ["slide"] and r["t0"][1] == ["slide"], r["t0"][1], ["slide"]),
        check("set(0.5) -> x = 1, set(1.5) -> x = 3 (linear 0 -> 4 over 2 s)", abs(x("t05") - 1) < 1e-4 and abs(x("t15") - 3) < 1e-4, [x("t05"), x("t15")], [1, 3]),
        check("offset .5 at t .5 seeks to 1.0 s -> x = 2", abs(x("off") - 2) < 1e-4, x("off"), 2),
        check("speed 2 at t .5 seeks to 1.0 s -> x = 2", abs(x("spd") - 2) < 1e-4, x("spd"), 2),
        check("negative control: set(0) leaves the crate at the origin", abs(x("t0")) < 1e-6, x("t0"), 0),
    ], [wd / "crate.glb", wd / "glb_measure.json"]


@card("3D-30")
def k3_pond(task, wd):
    """The K3 pond: makeShallowWater, makePebbles + addCaustics on the bed, makeBlades({n:1500, tall:.9, width:.02,
    hue:.24}) swaying (bend grows with height^2), fog #CBB08A .011, exposure .62. Two frames at different t are compared:
    reed tips move far more than their bases, the water/caustic bed changes; with sway amplitude 0 the reeds are frozen."""
    js = """
const W = 320, H = 180, SW = new URLSearchParams(location.search).get('amp');
async function shot(t, amp, png) {
  const r = K3.makeRenderer(cv, W, H, {tone: 'aces', exposure: 0.62});
  const s = new T.Scene(); s.background = new T.Color(0xcbb08a); s.fog = new T.FogExp2(0xcbb08a, 0.011);
  const cam = new T.PerspectiveCamera(40, W / H, 0.05, 100); cam.position.set(0, 1.0, 3.4); cam.lookAt(0, 0.35, 0);
  s.add(new T.HemisphereLight(0xffffff, 0x445533, 1.2)); const sun = new T.DirectionalLight(0xffe2b0, 2.5); sun.position.set(2, 5, 3); s.add(sun);
  const time = {value: t};
  const bed = new T.Mesh(new T.PlaneGeometry(8, 8, 64, 64).rotateX(-Math.PI / 2), new T.MeshStandardMaterial({color: 0x6b5a3a, roughness: 1}));
  bed.position.y = -0.3; K3.addCaustics(bed.material, {time, level: 0, strength: 2.2}); s.add(bed);
  const water = K3.makeShallowWater({width: 6.4, depth: 4.1, seg: 96}); s.add(water.mesh || water);
  if (water.uniforms) water.uniforms.uT.value = t; else if ((water.mesh || water).material.uniforms) (water.mesh || water).material.uniforms.uT.value = t;
  const blades = K3.makeBlades({n: 1500, tall: 0.9, width: 0.02, hue: 0.24, amp, time, region: [-3.2, 3.2, -1.2, 0.6],
    height: () => 0, accept: (x, z) => Math.abs(x) > 1.2 || z < -0.6, seed: 17});
  s.add(blades);
  r.render(s, cam); const u = grab(r); r.dispose(); return {png: u, count: blades.count};
}
window.__result = {a: await shot(0.0, 0.06), b: await shot(1.1, 0.06), c: await shot(0.0, 0.0), d: await shot(1.1, 0.0)};
window.__done = true;
"""
    r = pw(wd, "pond.html", [{"js": "window.__result"}], html=k3_page(320, 180, js), timeout=40)[0]
    ims = {}
    for k in "abcd":
        data_url_to_png(r[k]["png"], wd / ("pond_%s.png" % k))
        ims[k] = png_arr(wd / ("pond_%s.png" % k))
    mask = (ims["a"][..., 1] > ims["a"][..., 0]) & (ims["a"][..., 1] > ims["a"][..., 2])      # greenish reed pixels
    rows = np.where(mask.any(1))[0]
    top_band, base_band = (rows.min(), rows.min() + max(3, (rows.max() - rows.min()) // 4)), (rows.max() - max(3, (rows.max() - rows.min()) // 4), rows.max())
    def diff(x, y, band):
        return float(np.abs(x[band[0]:band[1]] - y[band[0]:band[1]]).mean())
    side = np.zeros(ims["a"].shape[:2], bool)
    side[:, :40] = True
    side[:, -40:] = True
    tip = diff(ims["a"], ims["b"], top_band)
    base = diff(ims["a"], ims["b"], base_band)
    frozen_tip = diff(ims["c"], ims["d"], top_band)
    centre = (slice(110, 175), slice(120, 200))
    water = float(np.abs(ims["a"][centre] - ims["b"][centre]).mean())
    jw(wd / "pond_measure.json", {"count": r["a"]["count"], "tip_diff": tip, "base_diff": base, "frozen_tip": frozen_tip, "water_diff": water,
                                  "bands": [list(map(int, top_band)), list(map(int, base_band))]})
    return [
        check("1500 reed blades placed", r["a"]["count"] == 1500, r["a"]["count"], 1500),
        check("reeds visible in the frame", mask.mean() > 0.01, float(mask.mean()), "> 1 %"),
        check("sway bends tips more than bases (height^2)", tip > 2 * base and tip > 1.0, [tip, base], "tip > 2x base"),
        check("the water/caustic bed changes with t", water > 0.3, water, "> 0.3"),
        check("negative control: sway amplitude 0 freezes the reed tips", frozen_tip < 0.25 * tip, [frozen_tip, tip], "frozen << swaying"),
    ], [wd / "pond_a.png", wd / "pond_b.png", wd / "pond_measure.json"]


def _levels(img, mask, step=4):
    """number of distinct quantised luminance levels holding >= 1 % of the masked pixels"""
    L = np.round(luma(img[mask] / 255.0) * 255 / step).astype(int)
    if L.size == 0:
        return 0
    vals, cnt = np.unique(L, return_counts=True)
    return int((cnt >= 0.01 * L.size).sum())


@card("3D-34")
def toon_vehicle_primitives(task, wd):
    """A plane from one factory function (lathe fuselage + extruded wings + prop blades, per-part materials) in MeshToon
    with a black outline pass (inverted hull), plus a RoundedBoxGeometry(1, 1, .35, 4, .08) wood slab with a canvas grain
    texture (#d3bb9b / #a58862). The same plane in MeshStandard is the untreated control."""
    js = """
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
const W = 320, H = 180;
const renderer = new THREE.WebGLRenderer({canvas: cv, antialias: false, preserveDrawingBuffer: true}); renderer.setSize(W, H, false); renderer.setPixelRatio(1);
const grad = new THREE.DataTexture(new Uint8Array([60, 60, 60, 255, 150, 150, 150, 255, 255, 255, 255, 255]), 3, 1); grad.minFilter = grad.magFilter = THREE.NearestFilter; grad.needsUpdate = true;
function plane(toon) {
  const m = c => toon ? new THREE.MeshToonMaterial({color: c, gradientMap: grad}) : new THREE.MeshStandardMaterial({color: c, roughness: 0.5});
  const g = new THREE.Group();
  const pts = []; for (let i = 0; i <= 12; i++) { const t = i / 12; pts.push(new THREE.Vector2(0.28 * Math.sin(Math.PI * Math.min(1, t * 1.15)) + 0.02, t * 2.2 - 1.1)); }
  const fus = new THREE.Mesh(new THREE.LatheGeometry(pts, 24), m(0xe8533f)); fus.rotation.z = Math.PI / 2; g.add(fus);
  const sh = new THREE.Shape(); sh.moveTo(-0.25, 0); sh.lineTo(0.25, 0); sh.lineTo(0.12, 1.3); sh.lineTo(-0.1, 1.3);
  const wingG = new THREE.ExtrudeGeometry(sh, {depth: 0.05, bevelEnabled: false});
  for (const s of [1, -1]) { const w = new THREE.Mesh(wingG, m(0xf2c14e)); w.rotation.x = -Math.PI / 2 * s; w.position.set(0, 0, 0); w.scale.z = s; g.add(w); }
  for (let i = 0; i < 2; i++) { const b = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.7, 0.08), m(0x333333)); b.position.x = 1.15; b.rotation.x = i * Math.PI / 2 + 0.4; g.add(b); }
  if (toon) { const outl = new THREE.MeshBasicMaterial({color: 0x000000, side: THREE.BackSide});
    const hulls = []; g.traverse(o => { if (o.isMesh) { const h = new THREE.Mesh(o.geometry, outl); h.position.copy(o.position); h.rotation.copy(o.rotation); h.scale.copy(o.scale).multiplyScalar(1.06); hulls.push(h); } });
    hulls.forEach(h => g.add(h)); }
  g.rotation.set(0.35, -0.6, 0.1); return g;
}
function render(toon) {
  const s = new THREE.Scene(); s.background = new THREE.Color(0xbfd7ea);
  s.add(new THREE.AmbientLight(0xffffff, 0.4)); const d = new THREE.DirectionalLight(0xffffff, 2.2); d.position.set(2, 3, 4); s.add(d);
  s.add(plane(toon)); const cam = new THREE.PerspectiveCamera(40, W / H, 0.1, 50); cam.position.set(0, 0.4, 4.2); cam.lookAt(0, 0, 0);
  renderer.render(s, cam); return grab(renderer);
}
const cvs = document.createElement('canvas'); cvs.width = cvs.height = 128; const x = cvs.getContext('2d'); x.fillStyle = '#d3bb9b'; x.fillRect(0, 0, 128, 128);
x.strokeStyle = '#a58862'; for (let i = 0; i < 20; i++) { x.lineWidth = 1 + (i % 3); x.beginPath(); x.moveTo(0, i * 6.4 + 2); x.bezierCurveTo(40, i * 6.4 + 6, 90, i * 6.4 - 3, 128, i * 6.4 + 2); x.stroke(); }
const slabG = new RoundedBoxGeometry(1, 1, 0.35, 4, 0.08); slabG.computeBoundingBox();
const s2 = new THREE.Scene(); s2.background = new THREE.Color(0x222222); s2.add(new THREE.AmbientLight(0xffffff, 1.0));
const gtex = new THREE.CanvasTexture(cvs); gtex.colorSpace = THREE.SRGBColorSpace;
const slab = new THREE.Mesh(slabG, new THREE.MeshBasicMaterial({map: gtex})); s2.add(slab);
const cam2 = new THREE.PerspectiveCamera(40, W / H, 0.1, 20); cam2.position.set(0, 0, 2.6); renderer.render(s2, cam2); const slabPng = grab(renderer);
const bb = slabG.boundingBox;
window.__result = {toon: render(true), std: render(false), slab: slabPng, slab_size: [bb.max.x - bb.min.x, bb.max.y - bb.min.y, bb.max.z - bb.min.z]};
window.__done = true;
"""
    r = pw(wd, "toon.html", [{"js": "window.__result"}], html=three_page(320, 180, js))[0]
    for k in ("toon", "std", "slab"):
        data_url_to_png(r[k], wd / ("toon_%s.png" % k) if k != "slab" else wd / "slab.png")
    toon, std, slab = png_arr(wd / "toon_toon.png"), png_arr(wd / "toon_std.png"), png_arr(wd / "slab.png")
    bg = np.array([0xbf, 0xd7, 0xea], float)
    obj_t = np.abs(toon - bg).sum(-1) > 30
    obj_s = np.abs(std - bg).sum(-1) > 30
    black_t = (toon.max(-1) < 20) & obj_t
    black_s = (std.max(-1) < 20) & obj_s
    red_t = obj_t & (toon[..., 0] > toon[..., 1] + 40) & (toon[..., 0] > toon[..., 2] + 40) & (toon.max(-1) >= 20)
    red_s = obj_s & (std[..., 0] > std[..., 1] + 40) & (std[..., 0] > std[..., 2] + 40)
    lv_t, lv_s = _levels(toon, red_t), _levels(std, red_s)
    from scipy.ndimage import binary_erosion
    def edge_black_of(img, obj):
        e = obj & ~binary_erosion(obj, iterations=1)
        return float(((img.max(-1) < 60) & e).sum() / max(1, e.sum()))
    edge_black, edge_black_s = edge_black_of(toon, obj_t), edge_black_of(std, obj_s)
    sm = (slab.sum(-1) > 150)
    grain = slab[sm]
    tan = float((np.abs(grain - [0xd3, 0xbb, 0x9b]).sum(-1) < 40).mean())
    dark = float((np.abs(grain - [0xa5, 0x88, 0x62]).sum(-1) < 40).mean())
    jw(wd / "toon_measure.json", {"levels_toon": lv_t, "levels_std": lv_s, "edge_black": edge_black, "edge_black_std": edge_black_s, "black_px": [int(black_t.sum()), int(black_s.sum())],
                                  "slab_size": r["slab_size"], "grain_tan": tan, "grain_dark": dark})
    return [
        check("toon fuselage shows <= 4 luminance bands", lv_t <= 4, lv_t, "<= 4"),
        check("the silhouette edge is the black outline pass (>= 40 % of edge pixels dark)", edge_black >= 0.4, edge_black, ">= 0.4"),
        check("RoundedBoxGeometry(1, 1, .35) has those extents", np.allclose(r["slab_size"], [1, 1, 0.35], atol=1e-6), r["slab_size"], [1, 1, 0.35]),
        check("slab carries the canvas grain (#d3bb9b body with #a58862 lines)", tan > 0.4 and dark > 0.05, [tan, dark], "> 0.4, > 0.05"),
        check("negative control: MeshStandard plane has many smooth levels and no dark outline", lv_s > lv_t + 3 and edge_black_s < 0.5 * edge_black,
              [lv_s, edge_black_s], "levels >> toon, edge not dark"),
    ], [wd / "toon_toon.png", wd / "slab.png", wd / "toon_measure.json"]


@card("3D-37")
def physical_materials(task, wd):
    """Glass: MeshPhysicalMaterial transmission 1, thickness 1.4, ior 1.5, dispersion .35, iridescence .9, clearcoat 1 over a
    text plane (the type refracts through); chrome: metalness 1, roughness .1 with an env map (the kit's envFromGradient);
    canvas-generated bump/roughness maps (K3.noiseCanvas + fbm). Opaque white plastic is the untreated control."""
    js = """
const W = 320, H = 180, r = K3.makeRenderer(cv, W, H, {tone: 'neutral', exposure: 1.0});
function stripes() { const c = document.createElement('canvas'); c.width = 512; c.height = 256; const x = c.getContext('2d');
  x.fillStyle = '#ffffff'; x.fillRect(0, 0, 512, 256); x.fillStyle = '#111111'; for (let i = 0; i < 16; i++) x.fillRect(i * 32, 0, 14, 256);
  x.fillStyle = '#d02020'; x.font = 'bold 90px sans-serif'; x.fillText('KOSIF', 110, 160); const t = new T.CanvasTexture(c); t.colorSpace = T.SRGBColorSpace; return t; }
function scene(kind) {
  const s = new T.Scene(); s.background = new T.Color(0x202020);
  const env = K3.envFromGradient(r, s, {top: 0x8fb8ff, horizon: 0x8fb8ff, ground: 0x302010, sunPower: 0}); if (env && !s.environment) s.environment = env;
  const back = new T.Mesh(new T.PlaneGeometry(6, 3), new T.MeshBasicMaterial({map: stripes()})); back.position.z = -1.5; s.add(back);
  let mat;
  if (kind === 'glass') mat = new T.MeshPhysicalMaterial({transmission: 1, thickness: 1.4, ior: 1.5, dispersion: 0.35, iridescence: 0.9, clearcoat: 1, roughness: 0.02, metalness: 0,
    attenuationColor: new T.Color(0xeaf6ff), attenuationDistance: 4});
  else if (kind === 'chrome') mat = new T.MeshPhysicalMaterial({metalness: 1, roughness: 0.1, color: 0xffffff});
  else mat = new T.MeshStandardMaterial({color: 0xf0f0f0, roughness: 0.6, metalness: 0});
  const ball = new T.Mesh(new T.SphereGeometry(0.75, 64, 32), mat); s.add(ball);
  s.add(new T.HemisphereLight(0xffffff, 0x404040, 1.0));
  const cam = new T.PerspectiveCamera(40, W / H, 0.1, 20); cam.position.set(0, 0, 3.2);
  r.render(s, cam); return grab(r);
}
const nc = K3.noiseCanvas(128, (x, y) => { const v = Math.round(128 + 120 * K3.fbm(x / 16, y / 16, 4)); return [v, v, v]; });
const img = nc.image || nc.source && nc.source.data; let nstats = null;
if (img && img.getContext) { const d = img.getContext('2d').getImageData(0, 0, 128, 128).data; let mn = 255, mx = 0, s = 0; for (let i = 0; i < d.length; i += 4) { mn = Math.min(mn, d[i]); mx = Math.max(mx, d[i]); s += d[i]; } nstats = {mn, mx, mean: s / (d.length / 4), png: img.toDataURL()}; }
window.__result = {glass: scene('glass'), chrome: scene('chrome'), plastic: scene('plastic'), noise: nstats};
window.__done = true;
"""
    r = pw(wd, "phys.html", [{"js": "window.__result"}], html=k3_page(320, 180, js), timeout=40)[0]
    for k in ("glass", "chrome", "plastic"):
        data_url_to_png(r[k], wd / ("phys_%s.png" % k))
    if r["noise"]:
        data_url_to_png(r["noise"].pop("png"), wd / "noise_map.png")
    g, c, p = (png_arr(wd / ("phys_%s.png" % k)) for k in ("glass", "chrome", "plastic"))
    yy, xx = np.mgrid[:180, :320]
    disc = (xx - 160) ** 2 + (yy - 90) ** 2 < 40 ** 2
    std = lambda a: float(luma(a[disc] / 255).std())
    stripe_like = lambda a: float(np.abs(np.diff(luma(a / 255)[disc.any(1)][:, 125:195], axis=1)).mean())
    top = luma(c[60:80, 150:170] / 255).mean()
    bot = luma(c[100:120, 150:170] / 255).mean()
    n = r["noise"] or {}
    jw(wd / "phys_measure.json", {"std": {"glass": std(g), "chrome": std(c), "plastic": std(p)}, "stripe_edges": {"glass": stripe_like(g), "plastic": stripe_like(p)},
                                  "chrome_top_bottom": [float(top), float(bot)], "noise": n})
    return [
        check("glass transmits the striped text plane (high contrast inside the ball)", std(g) > 0.15 and stripe_like(g) > 3 * stripe_like(p), [std(g), stripe_like(g), stripe_like(p)], "std > .15, edges > 3x plastic"),
        check("chrome mirrors the gradient env (sky-lit top brighter than ground-lit bottom)", top > bot + 0.05, [float(top), float(bot)], "top > bottom + .05"),
        check("canvas noise map generated (fbm, full tonal spread)", bool(n) and n["mx"] - n["mn"] > 100, [n.get("mn"), n.get("mx")], "spread > 100"),
        check("negative control: opaque plastic shows no transmitted stripes", std(p) < 0.12, std(p), "< 0.12"),
    ], [wd / "phys_glass.png", wd / "phys_chrome.png", wd / "phys_measure.json"]


@card("3D-39")
def studio_sweep(task, wd):
    """K3.studio(scene, {bg:'#f1efe8'}) from the vendored lab-kit: cream sweep, ShadowMaterial contact shadow .22, faint grid
    16 m / 32 div at .35, key 2.6 at (3, 6, 4), fill #dfe8ff .9, rim 1.4, hemi .9; plus K3S.stageDisc with a scan sweep.
    The floor under the hero darkens by the shadow opacity; the empty studio is the control."""
    js = """
const W = 320, H = 180;
function shot(withHero, scan) {
  const r = K3.makeRenderer(cv, W, H, {tone: 'neutral', exposure: 1.0});
  const s = new T.Scene(); const st = K3.studio(s, {bg: '#f1efe8'});
  if (withHero) { const m = new T.Mesh(new T.SphereGeometry(0.6, 48, 24), new T.MeshStandardMaterial({color: 0x9aa7ff})); m.position.y = 0.6; m.castShadow = true; s.add(m); }
  let disc = null; if (scan != null) { disc = K3S.stageDisc({radius: 0.24, color: 0x9dffb4, shadow: 0.5}); disc.position.set(1.6, 0.01, 0.6); s.add(disc);
    disc.traverse(o => { if (o.material && o.material.uniforms && o.material.uniforms.uScan) o.material.uniforms.uScan.value = scan; }); }
  const cam = new T.PerspectiveCamera(35, W / H, 0.1, 100); cam.position.set(0, 2.2, 5.5); cam.lookAt(0, 0.4, 0);
  r.render(s, cam); const u = grab(r); r.dispose();
  return {png: u, key: [st.key.intensity, st.key.position.toArray()], fill: [st.fill.intensity, '#' + st.fill.color.getHexString()], rim: st.rim.intensity,
    shadowOpacity: st.floor.material.opacity, grid: st.grid.material.opacity, bg: '#' + s.background.getHexString()};
}
window.__result = {hero: shot(true, 0.3), empty: shot(false, null), scan2: shot(true, 0.8)};
window.__done = true;
"""
    extra = '<script src="http://k/kit/lab-kit.js"></script><script src="http://k/kit/shape-kit.js"></script>'
    r = pw(wd, "studio.html", [{"js": "window.__result"}], html=k3_page(320, 180, js, extra), timeout=30)[0]
    for k in ("hero", "empty", "scan2"):
        data_url_to_png(r[k].pop("png"), wd / ("studio_%s.png" % k))
    h, e, s2 = (png_arr(wd / ("studio_%s.png" % k)) for k in ("hero", "empty", "scan2"))
    # the floor patch right below the sphere, beside it in the frame; the same patches in the empty studio
    Lh, Le = luma(h / 255), luma(e / 255)
    sphere = (h[..., 2] > h[..., 0] + 30)                       # the blue hero itself
    floor = ~sphere & (np.arange(180)[:, None] > 60) & (np.abs(e - h).sum(-1) < 120)
    q = (Lh / np.maximum(Le, 1e-6))[floor & (Lh < Le - 0.02)]
    dh = float(np.percentile(q, 5)) if q.size > 50 else 1.0
    fl = Le[(np.arange(180)[:, None] > 60) & np.ones((1, 320), bool)]
    de = float(np.percentile(fl, 5) / np.median(fl))
    scan_diff = float(np.abs(h - s2).max())
    cream = e[5:20, 5:60].mean((0, 1))
    jw(wd / "studio_measure.json", {"rigs": r, "under_over_ref": [float(dh), float(de)], "scan_diff": scan_diff, "bg_rgb": cream.tolist()})
    rig = r["hero"]
    return [
        check("rig as specified: key 2.6 at (3,6,4), fill .9 #dfe8ff, rim 1.4", rig["key"] == [2.6, [3, 6, 4]] and rig["fill"] == [0.9, "#dfe8ff"] and rig["rim"] == 1.4,
              [rig["key"], rig["fill"], rig["rim"]], [[2.6, [3, 6, 4]], [0.9, "#dfe8ff"], 1.4]),
        check("contact shadow material opacity .22, grid .35", abs(rig["shadowOpacity"] - 0.22) < 1e-6 and abs(rig["grid"] - 0.35) < 1e-6, [rig["shadowOpacity"], rig["grid"]], [0.22, 0.35]),
        check("cream sweep background #f1efe8", rig["bg"] == "#f1efe8" and np.abs(cream - [0xf1, 0xef, 0xe8]).max() < 12, [rig["bg"], cream.round().tolist()], "#f1efe8"),
        check("the hero casts a contact shadow: core darkening 8..30 % (ShadowMaterial .22)", 0.70 <= dh <= 0.92, float(dh), "0.70..0.92"),
        check("the stage disc's scan sweep moves with uScan", scan_diff > 20, scan_diff, "> 20"),
        check("negative control: the empty studio floor has no shadow (5th percentile within 5 % of the median)", de > 0.95, float(de), "> 0.95"),
    ], [wd / "studio_hero.png", wd / "studio_measure.json"]


@card("3D-40")
def geode_hero(task, wd):
    """The geode: IcosahedronGeometry(2.2, 2) MeshStandard #0f172a metalness .85 roughness .15 shell, inner
    OctahedronGeometry(1.4) emissive #0284c7 x.8, two TorusGeometry(3.6, .04, 16, 100) MeshBasic #38bdf8 at .6 tilted pi/3
    and pi/4; rotations .45/.6/.8/.9/.3/.4 rad/s from t (a pure function of t, so frames render in any order)."""
    js = """
const W = 320, H = 180;
const renderer = new THREE.WebGLRenderer({canvas: cv, antialias: true, preserveDrawingBuffer: true}); renderer.setSize(W, H, false); renderer.setPixelRatio(1);
const s = new THREE.Scene(); s.background = new THREE.Color(0x020617);
s.add(new THREE.AmbientLight(0xffffff, 0.4)); const d = new THREE.DirectionalLight(0xffffff, 2); d.position.set(4, 5, 6); s.add(d);
const shell = new THREE.Mesh(new THREE.IcosahedronGeometry(2.2, 2), new THREE.MeshStandardMaterial({color: 0x0f172a, metalness: 0.85, roughness: 0.15, wireframe: true}));
const core = new THREE.Mesh(new THREE.OctahedronGeometry(1.4), new THREE.MeshStandardMaterial({color: 0x000000, emissive: 0x0284c7, emissiveIntensity: 0.8}));
const ringM = new THREE.MeshBasicMaterial({color: 0x38bdf8, transparent: true, opacity: 0.6});
const r1 = new THREE.Mesh(new THREE.TorusGeometry(3.6, 0.04, 16, 100), ringM), r2 = new THREE.Mesh(new THREE.TorusGeometry(3.6, 0.04, 16, 100), ringM);
const g1 = new THREE.Group(), g2 = new THREE.Group(); g1.rotation.x = Math.PI / 3; g2.rotation.x = Math.PI / 4; g1.add(r1); g2.add(r2);
s.add(shell, core, g1, g2);
const cam = new THREE.PerspectiveCamera(45, W / H, 0.1, 100); cam.position.set(0, 0, 11);
function at(t) { shell.rotation.set(0.45 * t, 0.6 * t, 0); core.rotation.set(0.8 * t, 0.9 * t, 0); r1.rotation.z = 0.3 * t; r2.rotation.z = -0.4 * t;
  renderer.render(s, cam); return {png: grab(renderer), rot: [shell.rotation.x, shell.rotation.y, core.rotation.x, core.rotation.y, r1.rotation.z, r2.rotation.z], tilt: [g1.rotation.x, g2.rotation.x]}; }
const a = at(2.0), b = at(0.5), a2 = at(2.0), z = at(0);
window.__result = {a, b, a2, z}; window.__done = true;
"""
    r = pw(wd, "geode.html", [{"js": "window.__result"}], html=three_page(320, 180, js))[0]
    for k in ("a", "b", "a2", "z"):
        data_url_to_png(r[k]["png"], wd / ("geode_%s.png" % k))
    a, b, a2 = (png_arr(wd / ("geode_%s.png" % k)) for k in ("a", "b", "a2"))
    want = [0.9, 1.2, 1.6, 1.8, 0.6, -0.8]
    c = a[80:100, 150:170].mean((0, 1))
    ring_px = float(((a[..., 2] > 150) & (a[..., 0] < 120)).mean())
    jw(wd / "geode_measure.json", {k: {"rot": r[k]["rot"], "tilt": r[k]["tilt"]} for k in r} | {"core_rgb": c.tolist(), "ring_px": ring_px})
    return [
        check("rotations at t=2 equal rates x t (.45 .6 .8 .9 .3 -.4)", np.allclose(r["a"]["rot"], want, atol=1e-9), r["a"]["rot"], want),
        check("ring tilts pi/3 and pi/4", np.allclose(r["a"]["tilt"], [math.pi / 3, math.pi / 4]), r["a"]["tilt"], [math.pi / 3, math.pi / 4]),
        check("the core glows sky blue (#0284c7 emissive) at the centre", c[2] > 90 and c[2] > c[0] + 50, c.round().tolist(), "blue-dominant"),
        check("ring pixels present (#38bdf8 at .6)", ring_px > 0.005, ring_px, "> 0.5 %"),
        check("deterministic: the same t renders the same frame", float(np.abs(a - a2).max()) == 0, float(np.abs(a - a2).max()), 0),
        check("negative control: another t renders another frame", float(np.abs(a - b).mean()) > 1, float(np.abs(a - b).mean()), "> 1"),
    ], [wd / "geode_a.png", wd / "geode_measure.json"]


@card("3D-41")
def deterministic_fire_shot(task, wd):
    """One HTML with an importmap to three: ACES exposure 1.55, PCFSoftShadowMap 2048, FogExp2 0x0d151f .013, cold
    DirectionalLight 0xcfe0ff 3.2, fire PointLight 0xff8a3a 140 flickering +-25 at 23 rad/s, Hemisphere 0x4a5e80/0x070a10 .9,
    UnrealBloomPass(.32, .5, .88), FilmPass .22, fov 46; window.__ready set after the first composer render."""
    js = """
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { FilmPass } from 'three/addons/postprocessing/FilmPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
const W = 320, H = 180;
const renderer = new THREE.WebGLRenderer({canvas: cv, antialias: false, preserveDrawingBuffer: true}); renderer.setSize(W, H, false); renderer.setPixelRatio(1);
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.55; renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
const s = new THREE.Scene(); s.fog = new THREE.FogExp2(0x0d151f, 0.013); s.background = new THREE.Color(0x0d151f);
const key = new THREE.DirectionalLight(0xcfe0ff, 3.2); key.position.set(-6, 10, 4); key.castShadow = true; key.shadow.mapSize.set(2048, 2048); s.add(key);
const fire = new THREE.PointLight(0xff8a3a, 140, 0, 2); fire.position.set(0, 0.5, 0); fire.castShadow = true; s.add(fire);
s.add(new THREE.HemisphereLight(0x4a5e80, 0x070a10, 0.9));
const floor = new THREE.Mesh(new THREE.PlaneGeometry(60, 60).rotateX(-Math.PI / 2), new THREE.MeshStandardMaterial({color: 0x333333, roughness: 0.9})); floor.receiveShadow = true; s.add(floor);
const embers = new THREE.Mesh(new THREE.SphereGeometry(0.25, 24, 12), new THREE.MeshBasicMaterial({color: new THREE.Color(4, 1.8, 0.6)})); embers.position.copy(fire.position); s.add(embers);
for (let i = 0; i < 6; i++) { const b = new THREE.Mesh(new THREE.BoxGeometry(0.6, 1.2, 0.6), new THREE.MeshStandardMaterial({color: 0x887766})); b.position.set(Math.cos(i) * 3, 0.6, Math.sin(i) * 3 - 2 - i * 4); b.castShadow = true; s.add(b); }
const cam = new THREE.PerspectiveCamera(46, W / H, 0.1, 200); cam.position.set(0, 2, 6); cam.lookAt(0, 0.6, -2);
function compose(bloom) { const c = new EffectComposer(renderer); c.setPixelRatio(1); c.setSize(W, H); c.addPass(new RenderPass(s, cam));
  const ub = new UnrealBloomPass(new THREE.Vector2(W, H), 0.32, 0.5, 0.88); if (bloom) c.addPass(ub);
  const film = new FilmPass(0.22, false); c.addPass(film); c.addPass(new OutputPass()); return {c, film, ub}; }
const flick = t => 140 + 25 * Math.sin(23 * t);
function frame(t, bloom) { const {c, film} = compose(bloom); fire.intensity = flick(t); if (film.uniforms && film.uniforms.time) film.uniforms.time.value = t;
  c.render(0); if (film.uniforms && film.uniforms.time) film.uniforms.time.value = t; c.render(0); return {png: grab(renderer), intensity: fire.intensity}; }
const a = frame(1.0, true); window.__ready = true;
const a2 = frame(1.0, true), b = frame(1.07, true), nb = frame(1.0, false);
window.__result = {a, a2, b, nb, ready: window.__ready, fog: s.fog.density}; window.__done = true;
"""
    r = pw(wd, "fire.html", [{"js": "window.__result"}], html=three_page(320, 180, js), timeout=30)[0]
    for k in ("a", "a2", "b", "nb"):
        data_url_to_png(r[k]["png"], wd / ("fire_%s.png" % k))
    a, a2, b, nb = (png_arr(wd / ("fire_%s.png" % k)) for k in ("a", "a2", "b", "nb"))
    ring = np.zeros(a.shape[:2], bool)
    yy, xx = np.mgrid[:180, :320]
    # project the ember: find the brightest blob in the no-bloom frame, measure the halo ring around it
    L = luma(nb / 255)
    cy, cx = np.unravel_index(np.argmax(gblur(L, 2)), L.shape)
    dist = np.hypot(yy - cy, xx - cx)
    ring = (dist > 8) & (dist < 22)
    halo = float(luma(a / 255)[ring].mean() - L[ring].mean())
    want_a, want_b = 140 + 25 * math.sin(23 * 1.0), 140 + 25 * math.sin(23 * 1.07)
    jw(wd / "fire_measure.json", {"intensity": [r["a"]["intensity"], r["b"]["intensity"]], "halo_gain": halo, "ember_px": [int(cx), int(cy)], "fog": r["fog"]})
    return [
        check("fire flicker = 140 + 25 sin(23 t) at t = 1.0 and 1.07", abs(r["a"]["intensity"] - want_a) < 1e-9 and abs(r["b"]["intensity"] - want_b) < 1e-9,
              [r["a"]["intensity"], r["b"]["intensity"]], [want_a, want_b]),
        check("window.__ready set after the first composer render", r["ready"] is True, r["ready"], True),
        check("deterministic: the same t gives the identical frame (grain seeded by t)", float(np.abs(a - a2).max()) == 0, float(np.abs(a - a2).max()), 0),
        check("the flicker changes the lit frame", float(np.abs(a - b).mean()) > 0.3, float(np.abs(a - b).mean()), "> 0.3"),
        check("bloom lifts the halo around the embers", halo > 0.01, halo, "> 0.01"),
        check("negative control: without the bloom pass the ring is darker", float(L[ring].mean()) < float(luma(a / 255)[ring].mean()), [float(L[ring].mean()), float(luma(a / 255)[ring].mean())], "no-bloom < bloom"),
    ], [wd / "fire_a.png", wd / "fire_measure.json"]


@card("3D-42")
def sdf_sculpt_mesh(task, wd):
    """K3S.sculpt() from the vendored shape-kit: smooth-unioned SDF primitives (sphere, ellipsoid, capsule, box, torus with
    {k, op, color}) meshed by coarse-to-fine surface nets into an indexed, vertex-coloured BufferGeometry. Python checks the
    mesh: watertight (every edge shared by exactly two triangles), Euler characteristic, volume against the analytic sphere,
    and that the smooth union adds volume over the hard union."""
    js = """
function dump(S, cells) { const g = S.mesh({cells}); return {pos: Array.from(g.attributes.position.array), idx: Array.from(g.index.array), col: Array.from(g.attributes.color.array.slice(0, 60)), stats: g.userData.stats}; }
const one = dump(K3S.sculpt().sphere([0, 0, 0], 0.5, {color: '#ff0000'}), 72);
const hard = dump(K3S.sculpt().sphere([-0.3, 0, 0], 0.35).sphere([0.3, 0, 0], 0.35, {k: 0.0001}), 72);
const soft = dump(K3S.sculpt().sphere([-0.3, 0, 0], 0.35).sphere([0.3, 0, 0], 0.35, {k: 0.3}), 72);
const ring = dump(K3S.sculpt().torus([0, 0, 0], 0.4, 0.12, {color: '#00ff88'}), 72);
const carved = dump(K3S.sculpt().box([0, 0, 0], [0.4, 0.4, 0.4], 0.05).sphere([0, 0, 0.4], 0.25, {op: 'sub', k: 0.02}), 72);
window.__result = {one, hard, soft, ring, carved}; window.__done = true;
"""
    extra = '<script src="http://k/kit/shape-kit.js"></script>'
    r = pw(wd, "sculpt.html", [{"js": "window.__result"}], html=k3_page(64, 64, js, extra), timeout=40)[0]

    def analyse(m):
        P = np.array(m["pos"]).reshape(-1, 3)
        F = np.array(m["idx"]).reshape(-1, 3)
        e = np.sort(np.concatenate([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]), 1)
        _, cnt = np.unique(e, axis=0, return_counts=True)
        V, E = len(P), len(cnt)
        vol = float(np.einsum("ij,ij->i", P[F[:, 0]], np.cross(P[F[:, 1]], P[F[:, 2]])).sum() / 6)
        return {"V": V, "F": len(F), "E": E, "manifold": bool((cnt == 2).all()), "chi": V - E + len(F), "vol": abs(vol)}
    A = {k: analyse(r[k]) for k in r}
    sphere_v = 4 / 3 * math.pi * 0.5 ** 3
    hard_true = 2 * 4 / 3 * math.pi * 0.35 ** 3 - 2 * (math.pi * (0.35 - 0.3) ** 2 * (3 * 0.35 - (0.35 - 0.3)) / 3)
    obj = ["# K3S sculpt: two spheres smooth-unioned (k = .3)"]
    P = np.array(r["soft"]["pos"]).reshape(-1, 3)
    F = np.array(r["soft"]["idx"]).reshape(-1, 3)
    obj += ["v %.5f %.5f %.5f" % tuple(p) for p in P] + ["f %d %d %d" % tuple(f + 1) for f in F]
    (wd / "soft_union.obj").write_text("\n".join(obj) + "\n")
    col = np.array(r["one"]["col"]).reshape(-1, 3)
    jw(wd / "sculpt_measure.json", {"meshes": A, "stats": {k: r[k]["stats"] for k in r}, "sphere_analytic": sphere_v, "hard_analytic": hard_true})
    return [
        check("every mesh is watertight (each edge in exactly 2 triangles)", all(A[k]["manifold"] for k in A), {k: A[k]["manifold"] for k in A}, True),
        check("sphere, union and carved box are genus 0 (chi = 2); torus is genus 1 (chi = 0)",
              [A[k]["chi"] for k in ("one", "soft", "carved", "ring")] == [2, 2, 2, 0], [A[k]["chi"] for k in ("one", "soft", "carved", "ring")], [2, 2, 2, 0]),
        check("sphere r .5 volume within 3 % of 4/3 pi r^3", abs(A["one"]["vol"] / sphere_v - 1) < 0.03, A["one"]["vol"], sphere_v),
        check("vertex colours come from the field (#ff0000 sphere)", np.allclose(col.mean(0), [1, 0, 0], atol=0.02), col.mean(0).tolist(), [1, 0, 0]),
        check("hard union matches the analytic two-sphere volume (within 4 %)", abs(A["hard"]["vol"] / hard_true - 1) < 0.04, A["hard"]["vol"], hard_true),
        check("negative control: the hard union (k ~ 0) lacks the smooth fillet volume", A["soft"]["vol"] > A["hard"]["vol"] * 1.03, [A["soft"]["vol"], A["hard"]["vol"]], "soft > 1.03 x hard"),
    ], [wd / "soft_union.obj", wd / "sculpt_measure.json"]


# ================================================================================================ apps & artifacts
def _npm_env(wd):
    """npm needs the session's proxy CA settings: keep the environment, move only the cache into the work folder"""
    env = dict(os.environ)
    env.pop("NODE_PATH", None)
    env["npm_config_cache"] = str(Path(wd) / "npmcache")
    env["npm_config_update_notifier"] = "false"
    return env


def _node_env(wd):
    return {"NODE_PATH": str(NM), "PATH": str(Path(_NODE).parent) + ":/usr/bin:/bin", "HOME": str(wd),
            "PLAYWRIGHT_BROWSERS_PATH": os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")}


@card("APP-05")
def snap_mobile(task, wd):
    """The repo's snap.cjs: headless Chromium at 390x844, waits for document.fonts.ready, asserts scrollWidth > innerWidth
    in code, takes a full-page screenshot (and a PDF). A page with a 600 px wide table is the overflow fixture."""
    snap = SKILLS / "kosif-superpowers/proofs/general-data/snap.cjs"
    good = wd / "good.html"
    good.write_text("<!doctype html><meta name=viewport content='width=device-width'><style>body{margin:0;padding:16px;font:16px sans-serif;background:#fff}"
                    ".card{background:#eef;border-radius:12px;padding:16px;margin:12px 0}</style><h1>صفحة</h1>" +
                    "".join("<div class=card>بطاقة %d</div>" % i for i in range(12)), encoding="utf-8")
    bad = wd / "bad.html"
    bad.write_text("<!doctype html><meta name=viewport content='width=device-width'><style>body{margin:0;padding:16px}</style>"
                   "<table style='width:600px;border:1px solid #000'><tr><td>wide</td></tr></table>", encoding="utf-8")
    outs = {}
    for name, page in (("good", good), ("bad", bad)):
        o = run([_NODE, snap, page, wd / (name + ".png"), 390, 844] + ([wd / "good.pdf"] if name == "good" else []), cwd=str(wd),
                env=_node_env(wd), timeout=60).stdout
        outs[name] = json.loads(o.strip().splitlines()[-1])
    gi = Image.open(wd / "good.png")
    arr = np.asarray(gi.convert("L")).astype(float)
    jw(wd / "snap_report.json", outs)
    return [
        check("good page: no horizontal overflow at 390x844", outs["good"]["horizontal_overflow"] is False, outs["good"]["horizontal_overflow"], False),
        check("full-page screenshot is 390 px wide and taller than the viewport", gi.size[0] == 390 and gi.size[1] > 844, list(gi.size), "[390, > 844]"),
        check("screenshot is not blank (cards drawn)", arr.std() > 5, float(arr.std()), "> 5"),
        check("PDF written", (wd / "good.pdf").read_bytes()[:5] == b"%PDF-", (wd / "good.pdf").read_bytes()[:5].decode(errors="replace"), "%PDF-"),
        check("negative control: the 600 px table page is flagged as overflowing", outs["bad"]["horizontal_overflow"] is True, outs["bad"]["horizontal_overflow"], True),
    ], [wd / "good.png", wd / "good.pdf", wd / "snap_report.json"]


@card("APP-06")
def render_html_to_mp4(task, wd):
    """node tools/render_html.cjs --in page.html --out film.mp4 --width --height --fps 30 renders an animated page frame by
    frame (virtual time); the MP4 is then measured: frame count, fps, and the square's position on every frame against the
    CSS animation (left 0 -> 240 px, linear, 1 s)."""
    page = wd / "page.html"
    page.write_text("<!doctype html><style>html,body{margin:0;width:320px;height:180px;background:#000;overflow:hidden}"
                    "#b{position:absolute;top:70px;left:0;width:40px;height:40px;background:#fff;animation:m 1s linear forwards}"
                    "@keyframes m{from{left:0}to{left:240px}}</style><div id=b></div>", encoding="utf-8")
    (wd / "frames").mkdir(exist_ok=True)
    film = wd / "film.mp4"
    env = _node_env(wd)
    env["TMPDIR"] = str(wd)
    run([_NODE, REPO / "tools/render_html.cjs", "--in", page, "--out", film, "--width", 320, "--height", 180, "--fps", 30, "--duration", 1,
         "--frames-dir", wd / "frames", "--no-space-check"], cwd=str(wd), env=env, timeout=90)
    pr = fx.probe(film)
    v = [s for s in pr["streams"] if s["codec_type"] == "video"][0]
    F = fx.frames(film, size=(320, 180))
    xs = []
    for f in F:
        m = luma(f / 255)[80:100] > 0.5
        cols = np.where(m.any(0))[0]
        xs.append(float(cols.min()) if cols.size else -1)
    want = [240 * i / 30 for i in range(len(xs))]
    err = max(abs(a - b) for a, b in zip(xs, want)) if xs else 99
    shutil.rmtree(wd / "frames", ignore_errors=True)
    jw(wd / "render_measure.json", {"frames": len(F), "r_frame_rate": v["r_frame_rate"], "x": xs, "max_err_px": err})
    return [
        check("30 frames at 30 fps", len(F) == 30 and v["r_frame_rate"] == "30/1", [len(F), v["r_frame_rate"]], [30, "30/1"]),
        check("320x180 H.264", (v["width"], v["height"], v["codec_name"]) == (320, 180, "h264"), [v["width"], v["height"], v["codec_name"]], [320, 180, "h264"]),
        check("the square follows the CSS animation (left = 240 * t) within 3 px on every frame", err <= 3, err, "<= 3 px"),
        check("negative control: the untreated first frame is not the last position", xs[0] < 5 and xs[-1] > 220, [xs[0], xs[-1]], "[~0, ~232]"),
    ], [film, wd / "render_measure.json"]


@card("APP-07")
def vite_build(task, wd):
    """Check the installed toolchain version before writing from memory (vite --version), then build a tiny app with the
    real vite CLI: index.html + an ES module importing a helper -> dist/ with a hashed, minified bundle."""
    proj = wd / "app"
    (proj / "src").mkdir(parents=True, exist_ok=True)
    (proj / "index.html").write_text('<!doctype html><html><body><div id="app"></div><script type="module" src="/src/main.js"></script></body></html>')
    (proj / "src/greet.js").write_text("export function greeting(name) {\n  // a long comment that the minifier must drop\n  const message = 'Hello, ' + name + '!';\n  return message;\n}\n")
    (proj / "src/main.js").write_text("import { greeting } from './greet.js';\ndocument.getElementById('app').textContent = greeting('KOSIF');\n")
    ver = run(["vite", "--version"], env=_node_env(wd)).stdout.strip()
    run(["vite", "build", "--logLevel", "error"], cwd=str(proj), env=_node_env(wd), timeout=60)
    dist = proj / "dist"
    html = (dist / "index.html").read_text()
    js = sorted((dist / "assets").glob("index-*.js"))
    code = js[0].read_text() if js else ""
    src_bytes = len((proj / "src/greet.js").read_bytes()) + len((proj / "src/main.js").read_bytes())
    out = wd / "dist_index.html"
    out.write_text(html)
    m = re.match(r"vite/(\d+)\.(\d+)\.(\d+)", ver)
    jw(wd / "vite_report.json", {"version": ver, "bundle": js[0].name if js else None, "bundle_bytes": len(code), "source_bytes": src_bytes})
    return [
        check("installed vite version read from the tool (major >= 8)", bool(m) and int(m.group(1)) >= 8, ver, "vite/8.x"),
        check("dist/index.html references a content-hashed bundle", bool(js) and re.search(r'/assets/index-[\w-]{8}\.js', html) is not None, js[0].name if js else None, "index-<hash>.js"),
        check("the bundle inlines the imported helper (greeting text present, no import left)", "Hello, " in code and "import" not in code and "greet.js" not in code, len(code), "bundled"),
        check("negative control: the unbuilt source still has the comment the build drops", "long comment" in (proj / "src/greet.js").read_text() and "long comment" not in code, True, True),
    ], [js[0] if js else out, out, wd / "vite_report.json"]


@card("APP-09")
def fastapi_inprocess(task, wd):
    """app = FastAPI(); @app.get('/') ...; TestClient(app).get('/').json() -> {'ok': 1}: an HTTP API tested in-process
    without opening a port; a typed path parameter is validated (422 on bad input)."""
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    app = FastAPI()

    @app.get("/")
    def root():
        return {"ok": 1}

    @app.get("/square/{n}")
    def square(n: int):
        return {"n": n, "square": n * n}

    c = TestClient(app)
    r1, r2, r3, r4 = c.get("/"), c.get("/square/12"), c.get("/square/abc"), c.get("/missing")
    spec = c.get("/openapi.json").json()
    rep = jw(wd / "api_report.json", {"root": r1.json(), "square": r2.json(), "bad": [r3.status_code, r3.json()], "missing": r4.status_code,
                                      "paths": sorted(spec["paths"])})
    return [
        check("GET / -> {'ok': 1}", r1.status_code == 200 and r1.json() == {"ok": 1}, r1.json(), {"ok": 1}),
        check("GET /square/12 -> 144", r2.json() == {"n": 12, "square": 144}, r2.json(), {"n": 12, "square": 144}),
        check("OpenAPI schema lists both routes", sorted(spec["paths"]) == ["/", "/square/{n}"], sorted(spec["paths"]), ["/", "/square/{n}"]),
        check("negative control: a non-integer path parameter is rejected with 422", r3.status_code == 422, r3.status_code, 422),
        check("unknown route 404", r4.status_code == 404, r4.status_code, 404),
    ], [rep]


@card("APP-10")
def jinja_templates(task, wd):
    """jinja2.Environment(autoescape=True).from_string(tpl).render(**data) fills HTML, Markdown and message templates;
    autoescape stays on for HTML. The same HTML with autoescape off is the untreated control (the script tag survives)."""
    import jinja2
    data = {"name": "Ali", "items": [{"t": "شاي", "p": 5}, {"t": "قهوة", "p": 12}], "note": "<script>alert(1)</script>"}
    html_t = "<h1>Hi {{ name }}</h1><ul>{% for i in items %}<li>{{ i.t }}: {{ i.p }} SAR</li>{% endfor %}</ul><p>{{ note }}</p><b>{{ items|sum(attribute='p') }}</b>"
    md_t = "# Order for {{ name }}\n{% for i in items %}- {{ i.t }} x{{ loop.index }}\n{% endfor %}"
    msg_t = "Hi {{ name }}, your total is {{ items|sum(attribute='p') }} SAR."
    env = jinja2.Environment(autoescape=True)
    html = env.from_string(html_t).render(**data)
    md = jinja2.Environment(autoescape=False).from_string(md_t).render(**data)
    msg = env.from_string(msg_t).render(**data)
    raw = jinja2.Environment(autoescape=False).from_string(html_t).render(**data)
    (wd / "page.html").write_text(html, encoding="utf-8")
    (wd / "order.md").write_text(md, encoding="utf-8")
    return [
        check("message: 'Hi Ali, your total is 17 SAR.'", msg == "Hi Ali, your total is 17 SAR.", msg, "Hi Ali, your total is 17 SAR."),
        check("HTML list rendered with both rows and the sum", "<li>شاي: 5 SAR</li><li>قهوة: 12 SAR</li>" in html and "<b>17</b>" in html, html[:120], "rows + 17"),
        check("autoescape on: the script tag is escaped", "&lt;script&gt;alert(1)&lt;/script&gt;" in html and "<script>" not in html, html.split("<p>")[1][:40], "&lt;script&gt;..."),
        check("Markdown loop indexes 1..2", md.splitlines() == ["# Order for Ali", "- شاي x1", "- قهوة x2"], md.splitlines(), ["# Order for Ali", "- شاي x1", "- قهوة x2"]),
        check("negative control: with autoescape off the raw script survives", "<script>alert(1)</script>" in raw, "<script>" in raw, True),
    ], [wd / "page.html", wd / "order.md"]


@card("APP-11")
def mcp_server_tool(task, wd):
    """mcp 2.x: from mcp.server import MCPServer; srv = MCPServer('name'); @srv.tool() def f(...). The import that v1 code
    uses (mcp.server.fastmcp.FastMCP) must fail; a real in-memory MCP client session lists the tool (narrow typed inputs) and
    calls it, the result carries status + summary + next_actions; a bad argument is refused."""
    import asyncio
    import importlib.metadata as md
    from mcp.server import MCPServer
    from mcp.client import Client
    try:
        from mcp.server.fastmcp import FastMCP  # noqa: F401
        v1 = "imported"
    except ModuleNotFoundError as exc:
        v1 = str(exc)[:120]
    srv = MCPServer("kosif-demo")

    @srv.tool()
    def frame_count(seconds: float, fps: int = 30) -> dict:
        """Frames in a clip of `seconds` at `fps`."""
        n = int(round(seconds * fps))
        return {"status": "ok", "summary": "%g s at %d fps = %d frames" % (seconds, fps, n), "frames": n, "next_actions": ["render"]}

    async def go():
        async with Client(srv) as c:
            tools = await c.list_tools()
            ok = await c.call_tool("frame_count", {"seconds": 2.5, "fps": 30})
            try:
                bad = await c.call_tool("frame_count", {"seconds": "two"})
                bad_err = bool(getattr(bad, "is_error", False))
            except Exception as exc:  # refused by validation
                bad_err = True
            return tools, ok, bad_err
    tools, ok, bad_err = asyncio.run(go())
    tl = getattr(tools, "tools", tools)
    t0 = tl[0]
    schema = getattr(t0, "input_schema", None) or getattr(t0, "inputSchema", None)
    payload = json.loads(ok.content[0].text)
    rep = jw(wd / "mcp_report.json", {"mcp": md.version("mcp"), "v1_import": v1, "tool": t0.name, "schema": schema, "result": payload, "bad_is_error": bad_err})
    return [
        check("mcp 2.x installed and the v1 FastMCP import fails", md.version("mcp").startswith("2.") and v1 != "imported", [md.version("mcp"), v1[:60]], "2.x, ModuleNotFoundError"),
        check("tool listed with a narrow typed schema (seconds: number required, fps: integer)", t0.name == "frame_count" and schema["required"] == ["seconds"] and schema["properties"]["fps"]["type"] == "integer",
              [t0.name, schema.get("required")], ["frame_count", ["seconds"]]),
        check("call returns status + summary + next_actions with 75 frames", payload == {"status": "ok", "summary": "2.5 s at 30 fps = 75 frames", "frames": 75, "next_actions": ["render"]},
              payload, 75),
        check("negative control: a non-numeric argument is refused", bad_err is True, bad_err, True),
    ], [rep]


@card("APP-13")
def serve_folder_http(task, wd):
    """python3 -m http.server serves the work folder so a page using ES modules and fetch() works; Playwright points at
    http://127.0.0.1:<port>. The same page opened from file:// is the untreated control (module and fetch blocked)."""
    site = wd / "site"
    site.mkdir(exist_ok=True)
    (site / "data.json").write_text(json.dumps({"frames": 75}))
    (site / "lib.js").write_text("export const double = x => x * 2;\n")
    (site / "index.html").write_text("<!doctype html><body><script type=module>import {double} from './lib.js';"
                                     "fetch('./data.json').then(r => r.json()).then(d => { window.__result = {v: double(d.frames)}; window.__done = true; })"
                                     ".catch(e => { window.__result = {err: String(e)}; window.__done = true; });</script>"
                                     "<script>setTimeout(() => { if (!window.__done) { window.__result = {err: 'module did not run'}; window.__done = true; } }, 1200);</script></body>")
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1", "--directory", str(site)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
    try:
        for _ in range(100):
            try:
                socket.create_connection(("127.0.0.1", port), timeout=0.2).close()
                break
            except OSError:
                time.sleep(0.05)
        import urllib.request
        body = urllib.request.urlopen("http://127.0.0.1:%d/data.json" % port, timeout=5).read()
        cfg = wd / "_pwreal.json"
        res_http = _pw_real(wd, "http://127.0.0.1:%d/index.html" % port, "shot_http.png")
        res_file = _pw_real(wd, (site / "index.html").as_uri(), "shot_file.png")
    finally:
        srv.terminate()
        srv.wait(5)
    rep = jw(wd / "serve_report.json", {"port": port, "curl_body": body.decode(), "http": res_http, "file": res_file})
    return [
        check("the folder is served over HTTP (data.json fetched)", json.loads(body) == {"frames": 75}, body.decode(), '{"frames": 75}'),
        check("over http:// the ES module and fetch run (double(75) = 150)", res_http.get("v") == 150, res_http, {"v": 150}),
        check("negative control: from file:// the same page fails", "v" not in res_file, res_file, "error"),
    ], [rep, wd / "shot_http.png"]


def _pw_real(wd, url, shot):
    """Playwright on a real URL (no routing): http://127.0.0.1 or file://."""
    runner = wd / "_pw.cjs"
    runner.write_text(_PW_JS, encoding="utf-8")
    cfg = {"w": 320, "h": 180, "url": url, "mounts": [], "nm": str(NM), "wait": "window.__done === true", "timeout": 10000, "real": True,
           "steps": [{"js": "window.__result", "shot": str(wd / shot)}]}
    cp = wd / ("_pwreal_%s.json" % shot.split(".")[0])
    cp.write_text(json.dumps(cfg))
    done = run([_NODE, runner, cp], cwd=str(wd), env=_node_env(wd), timeout=40)
    return json.loads(done.stdout.strip().splitlines()[-1])["out"][0]


def _stl_volume(path):
    txt = Path(path).read_text(errors="replace")
    v = np.array([list(map(float, m)) for m in re.findall(r"vertex\s+(\S+)\s+(\S+)\s+(\S+)", txt)]).reshape(-1, 3, 3)
    return float(abs(np.einsum("ij,ij->i", v[:, 0], np.cross(v[:, 1], v[:, 2])).sum() / 6)), v


@card("APP-21")
def openscad_render(task, wd):
    """OpenSCAD renders a .scad model headlessly to STL: a 10 mm cube minus a $fn=64 cylinder r 3 through it. The STL's
    volume is integrated from its triangles and compared with the exact answer 1000 - (area of a 64-gon of r 3) x 10;
    the untreated cube (no difference) is the control."""
    scad = wd / "part.scad"
    scad.write_text("$fn = 64;\ndifference() {\n  cube([10, 10, 10]);\n  translate([5, 5, -1]) cylinder(r = 3, h = 12);\n}\n")
    plain = wd / "cube.scad"
    plain.write_text("cube([10, 10, 10]);\n")
    for s_, o in ((scad, wd / "part.stl"), (plain, wd / "cube.stl")):
        run(["openscad", "--export-format", "asciistl", "-o", o, s_], timeout=60, cwd=str(wd), env=dict(os.environ, HOME=str(wd)))
    vol, tri = _stl_volume(wd / "part.stl")
    vcube, _ = _stl_volume(wd / "cube.stl")
    hole = 0.5 * 64 * 9 * math.sin(2 * math.pi / 64) * 10
    want = 1000 - hole
    bb = tri.reshape(-1, 3)
    jw(wd / "scad_report.json", {"volume": vol, "expected": want, "cube": vcube, "triangles": len(tri), "bbox": [bb.min(0).tolist(), bb.max(0).tolist()]})
    return [
        check("STL volume = 1000 - 64-gon hole (exact to 1e-3)", abs(vol - want) < 1e-3, vol, want),
        check("bounding box 0..10 mm on every axis", np.allclose(bb.min(0), 0) and np.allclose(bb.max(0), 10), [bb.min(0).tolist(), bb.max(0).tolist()], [[0, 0, 0], [10, 10, 10]]),
        check("the hole adds triangles (>= 64 x 4)", len(tri) >= 256, len(tri), ">= 256"),
        check("negative control: the untreated cube is 1000 mm^3", abs(vcube - 1000) < 1e-6 and abs(vcube - want) > 200, vcube, 1000),
    ], [wd / "part.stl", wd / "scad_report.json"]


_A11Y_BAD = """<!doctype html><html><head><title>t</title></head><body style="background:#fff">
<img src="data:image/gif;base64,R0lGODlhAQABAAAAACw=" width="40" height="40"><button></button>
<p style="color:#cccccc;background:#ffffff">faint text</p><a href="#"></a></body></html>"""
_A11Y_GOOD = """<!doctype html><html lang="ar" dir="rtl"><head><title>صفحة</title></head><body style="background:#fff"><main id="top">
<h1>مرحبا</h1><img src="data:image/gif;base64,R0lGODlhAQABAAAAACw=" alt="شعار" width="40" height="40"><button>إرسال</button>
<p style="color:#222;background:#fff">نص واضح</p><a href="#top">أعلى الصفحة</a></main></body></html>"""


@card("APP-22")
def axe_wcag(task, wd):
    """axe-core 4.x run inside the rendered page in Playwright's Chromium: the fixture with an image without alt, an empty
    button, an empty link and #ccc-on-white text must report image-alt, button-name, link-name and color-contrast; the
    fixed page must report none of them."""
    res = {}
    for name, html in (("bad", _A11Y_BAD), ("good", _A11Y_GOOD)):
        page = html.replace("</body>", '<script src="http://k/nm/axe-core/axe.min.js"></script><script>axe.run(document, {runOnly: {type: "tag", values: ["wcag2a", "wcag2aa"]}})'
                                       '.then(r => { window.__result = {v: r.violations.map(v => [v.id, v.impact, v.nodes.length]), version: axe.version}; window.__done = true; })'
                                       '.catch(e => window.__err = String(e));</script></body>')
        res[name] = pw(wd, name + ".html", [{"js": "window.__result"}], w=400, h=300, html=page)[0]
    ids = {n: sorted(v[0] for v in res[n]["v"]) for n in res}
    rep = jw(wd / "axe_report.json", res)
    want = {"button-name", "color-contrast", "image-alt", "link-name"}
    return [
        check("axe-core 4.x ran in the page", res["bad"]["version"].startswith("4."), res["bad"]["version"], "4.x"),
        check("bad page: image-alt, button-name, link-name, color-contrast reported", want <= set(ids["bad"]), ids["bad"], sorted(want)),
        check("fixed page: none of those violations", not (want & set(ids["good"])), ids["good"], []),
        check("negative control: the untreated page has more violations than the fixed one", len(ids["bad"]) > len(ids["good"]), [len(ids["bad"]), len(ids["good"])], "bad > good"),
    ], [rep]


@card("APP-23")
def pa11y_cli(task, wd):
    """The pa11y CLI (global 10.x, HTML_CodeSniffer runner, WCAG2AA) audits local HTML files and reports issues as JSON;
    Chromium is Playwright's, given through a pa11y config. The fixed page is the clean control."""
    chrome = sorted(Path(os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")).glob("chromium-*/chrome-linux64/chrome"))
    conf = wd / "pa11y.json"
    conf.write_text(json.dumps({"chromeLaunchConfig": {"executablePath": str(chrome[-1]) if chrome else "/usr/bin/google-chrome",
                                                       "args": ["--no-sandbox", "--disable-dev-shm-usage"]}, "timeout": 30000, "standard": "WCAG2AA"}))
    res = {}
    for name, html in (("bad", _A11Y_BAD), ("good", _A11Y_GOOD)):
        p = wd / (name + ".html")
        p.write_text(html, encoding="utf-8")
        done = run(["pa11y", "--config", conf, "--reporter", "json", p.as_uri()], cwd=str(wd), env=_node_env(wd), timeout=60, ok=(0, 2))
        res[name] = json.loads(done.stdout or "[]")
    codes = {n: sorted({i["code"].split(".")[3] if i["code"].count(".") >= 3 else i["code"] for i in res[n] if i.get("type") == "error"}) for n in res}
    rep = jw(wd / "pa11y_report.json", {"issues": res, "error_criteria": codes})
    flat = " ".join(i["code"] for i in res["bad"])
    return [
        check("bad page: missing alt (H37) reported", "H37" in flat, [i["code"] for i in res["bad"]][:6], "contains H37"),
        check("bad page: low contrast (G18) reported", "G18" in flat, "G18" in flat, True),
        check("bad page: empty link / button name (H30 / H91) reported", "H30" in flat or "H91" in flat, [c for c in ("H30", "H91") if c in flat], "H30 or H91"),
        check("fixed page: no errors", not [i for i in res["good"] if i.get("type") == "error"], [i["code"] for i in res["good"] if i.get("type") == "error"], []),
        check("negative control: the untreated page has errors", len([i for i in res["bad"] if i.get("type") == "error"]) >= 3, len([i for i in res["bad"] if i.get("type") == "error"]), ">= 3"),
    ], [rep]


# ================================================================================================ light / glow
def _ass_frames(wd, ass, times, name, size=(720, 1280)):
    out = []
    for t in times:
        p = wd / ("%s_%04d.png" % (name, int(round(t * 1000))))
        fx.ffmpeg("-f", "lavfi", "-i", "color=c=black:s=%dx%d:r=30:d=2" % size, "-ss", "%.3f" % t,
                  "-vf", "subtitles=%s:fontsdir=%s" % (ass, wd / "fonts"), "-frames:v", "1", str(p))
        out.append(p)
    return out


@card("GLOW-06")
def ass_double_line_glow(task, wd):
    """A glow under Arabic captions by drawing the same line twice in ASS: 'Glow' on Layer 0 (outline 9, primary alpha &H80,
    \\blur6) and 'Main' on Layer 1 (outline 3, shadow 2) with identical override tags \\move(360,1060,360,1020,0,650)
    \\fad(230,400)\\fscx94\\fscy94\\t(0,650,\\fscx100\\fscy100); rendered by libass in ffmpeg at 720x1280. The Main-only
    render is the untreated control."""
    (wd / "fonts").mkdir(exist_ok=True)
    shutil.copy(FONTS / "Cairo[slnt,wght].ttf", wd / "fonts/Cairo.ttf")
    tags = r"{\move(360,1060,360,1020,0,650)\fad(230,400)\fscx94\fscy94\t(0,650,\fscx100\fscy100)}"
    text = "سبحان الله وبحمده"
    head = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 720\nPlayResY: 1280\nWrapStyle: 2\n\n[V4+ Styles]\n"
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
            "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
            "Style: Glow,Cairo,57,&H80FFF2DF,&H000000FF,&H803E5D8B,&H00000000,-1,0,0,0,100,100,0,0,1,9,0,2,20,20,40,1\n"
            "Style: Main,Cairo,57,&H00FFFFFF,&H000000FF,&H003E5D8B,&H80000000,-1,0,0,0,100,100,0,0,1,3,2,2,20,20,40,1\n\n"
            "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    both = wd / "glow.ass"
    both.write_text(head + "Dialogue: 0,0:00:00.00,0:00:01.80,Glow,,0,0,0,,%s{\\blur6}%s\n" % (tags, text) +
                    "Dialogue: 1,0:00:00.00,0:00:01.80,Main,,0,0,0,,%s%s\n" % (tags, text), encoding="utf-8")
    main = wd / "main.ass"
    main.write_text(head + "Dialogue: 1,0:00:00.00,0:00:01.80,Main,,0,0,0,,%s%s\n" % (tags, text), encoding="utf-8")
    g = [png_arr(p) for p in _ass_frames(wd, both, [0.30, 0.70, 1.20], "glow")]
    m = [png_arr(p) for p in _ass_frames(wd, main, [0.30, 0.70, 1.20], "main")]
    from scipy.ndimage import distance_transform_edt

    def bbox(a):
        ys, xs = np.where(luma(a / 255) > 0.5)
        return xs.min(), xs.max(), ys.min(), ys.max()

    def halo_px(a, ref_main):
        core = luma(ref_main / 255) > 0.05
        d = distance_transform_edt(~core)
        return int(((luma(a / 255) > 0.04) & (d > 4)).sum())
    halo_g, halo_m = halo_px(g[2], m[2]), halo_px(m[2], m[2])
    b3, b1 = bbox(m[2]), bbox(m[0])
    wr = (b1[1] - b1[0]) / (b3[1] - b3[0])
    want_wr = (94 + 6 * 0.30 / 0.65) / 100
    dy = b1[3] - b3[3]
    want_dy = 40 * (1 - 0.30 / 0.65)
    still = float(np.abs(g[1] - g[2]).max())
    jw(wd / "glow_measure.json", {"halo_px": [halo_g, halo_m], "width_ratio": wr, "want_wr": want_wr, "dy": int(dy), "want_dy": want_dy, "still_diff": still})
    return [
        check("the Glow layer lays a soft halo beyond the Main outline (> 1500 px at > 4 px out)", halo_g > 1500, halo_g, "> 1500"),
        check("\\fscx94 -> 100 over 650 ms: width at 0.30 s / width at rest", abs(wr - want_wr) < 0.012, wr, want_wr),
        check("\\move 1060 -> 1020 over 650 ms: line still 40 x (1 - .3/.65) px low at 0.30 s", abs(dy - want_dy) <= 3, int(dy), want_dy),
        check("after 650 ms the line rests (0.70 s and 1.20 s frames identical)", still <= 2, still, "<= 2"),
        check("negative control: the Main-only render has no halo", halo_m < 0.1 * halo_g, halo_m, "< 10 % of glow"),
    ], [wd / "glow_1200.png", both, wd / "glow_measure.json"]


@card("GLOW-07")
def svg_blur_merge_glow(task, wd):
    """<filter x=-50% y=-50% width=200% height=200%> feGaussianBlur stdDeviation 6 -> feMerge(blur, SourceGraphic): the
    path glows from a blurred copy merged under the crisp original. Chrome renders the SVG with and without the filter."""
    svg = lambda flt: ("""<!doctype html><body style="margin:0;background:#000"><svg width="320" height="180" xmlns="http://www.w3.org/2000/svg">
<defs><filter id="g" x="-50%%" y="-50%%" width="200%%" height="200%%"><feGaussianBlur stdDeviation="6" result="b"/>
<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<path d="M40 120 C 100 20, 220 20, 280 120" fill="none" stroke="#38bdf8" stroke-width="6" stroke-linecap="round" %s/></svg>
<script>window.__done = true;</script></body>""" % ('filter="url(#g)"' if flt else ""))
    pw(wd, "glow.html", [{"shot": "glow.png"}], html=svg(True))
    pw(wd, "plain.html", [{"shot": "plain.png"}], html=svg(False))
    a, b = png_arr(wd / "glow.png") / 255, png_arr(wd / "plain.png") / 255
    from scipy.ndimage import distance_transform_edt
    core = luma(b) > 0.3
    d = distance_transform_edt(~core)
    prof = [float(luma(a)[(d > k - 0.5) & (d <= k + 0.5)].mean()) for k in (2, 5, 9, 14)]
    prof_b = [float(luma(b)[(d > k - 0.5) & (d <= k + 0.5)].mean()) for k in (2, 5, 9, 14)]
    inside = float(np.abs(a[core] - b[core]).max())
    top = float(luma(a)[5:12, 150:170].mean())   # 12 px above the curve's apex ~ 45 px: inside the -50% filter region
    jw(wd / "svg_glow_measure.json", {"profile_glow": prof, "profile_plain": prof_b, "core_diff": inside})
    return [
        check("halo falls off monotonically with distance (2 > 5 > 9 > 14 px)", all(x > y for x, y in zip(prof, prof[1:])) and prof[0] > 0.05, prof, "decreasing, > .05 at 2 px"),
        check("halo still visible 9 px out (sigma 6 blur)", prof[2] > 0.01, prof[2], "> 0.01"),
        check("the crisp stroke stays on top (core pixels within 0.25 of the plain stroke)", inside < 0.25, inside, "< 0.25"),
        check("negative control: the unfiltered path has no halo", max(prof_b) < 0.005, prof_b, "~0"),
    ], [wd / "glow.png", wd / "svg_glow_measure.json"]


def _bezier(p0, p1, p2, p3, n=2000):
    t = np.linspace(0, 1, n)[:, None]
    pts = (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3
    seg = np.hypot(*np.diff(pts, axis=0).T)
    s = np.concatenate([[0], np.cumsum(seg)])
    return pts, s


@card("GLOW-08")
def hot_spot_on_stroke(task, wd):
    """A hot spot rides a stroke as it draws: dashoffset 1 -> 0 over ~1 s (pathLength = 1), head = getPointAtLength(L p) drawn
    as a 5 px white dot with a 12 px glow, then the head fades over 0.5 s after arrival. Frames are rendered in numpy at
    30 fps; the head is found on every frame and compared with the arc-length point."""
    H, W = 180, 320
    pts, s = _bezier(np.array([30., 150.]), np.array([90., 10.]), np.array([230., 10.]), np.array([290., 150.]))
    L = s[-1]
    yy, xx = np.mgrid[:H, :W]

    def at(len_):
        return pts[np.searchsorted(s, min(len_, L)) if len_ < L else -1]
    frames, heads, want, peak = [], [], [], []
    from scipy.ndimage import distance_transform_edt
    for k in range(48):
        t = k / 30
        p = min(1.0, t / 1.0)
        p = 1 - (1 - p) ** 2                                  # power2.out draw
        img = np.zeros((H, W, 3))
        drawn = pts[s <= L * p]
        if len(drawn) > 1:
            m = np.zeros((H, W), bool)
            ij = np.round(drawn).astype(int)
            m[np.clip(ij[:, 1], 0, H - 1), np.clip(ij[:, 0], 0, W - 1)] = True
            stroke = distance_transform_edt(~m) <= 1.5
            img[stroke] = [0.2, 0.55, 0.95]
        fade = 1.0 if t <= 1.0 else max(0.0, 1 - (t - 1.0) / 0.5)
        hx, hy = at(L * p)
        r = np.hypot(xx - hx, yy - hy)
        head = (np.clip(2.5 - r + 0.5, 0, 1) + 0.6 * np.exp(-(r / 6.0) ** 2)) * fade
        img = 1 - (1 - img) * (1 - np.clip(head, 0, 1)[..., None])
        frames.append(img)
        want.append((hx, hy))
        lum = gblur(luma(img), 1.5)
        cy, cx = np.unravel_index(np.argmax(lum), lum.shape)
        heads.append((cx, cy))
        peak.append(float(luma(img).max()))
    film = write_video(wd / "hotspot.mp4", frames)
    err = max(math.hypot(a[0] - b[0], a[1] - b[1]) for a, b in zip(heads[1:30], want[1:30]))
    # untreated: the fully drawn stroke without a head
    plain = frames[-1]
    jw(wd / "hotspot_measure.json", {"length_px": L, "max_head_err": err, "peak": peak})
    return [
        check("the hot spot sits on the arc-length point L p on every drawing frame (<= 1.5 px)", err <= 1.5, err, "<= 1.5 px"),
        check("the head reaches the path end at 1 s", math.hypot(heads[30][0] - pts[-1][0], heads[30][1] - pts[-1][1]) <= 1.5, heads[30], pts[-1].tolist()),
        check("the head is white-hot (peak luma ~1) while drawing", min(peak[1:30]) > 0.95, min(peak[1:30]), "> 0.95"),
        check("then it fades over 0.5 s (dimmer at 1.23 s, gone by 1.5 s)", peak[29] > 0.95 and peak[45] < 0.6 and peak[45] + 0.05 < peak[37] < peak[29] - 0.05,
              [peak[29], peak[37], peak[45]], "full > fading > gone"),
        check("negative control: the finished stroke without a head has no hot spot", float(luma(plain).max()) < 0.6, float(luma(plain).max()), "< 0.6"),
    ], [film, wd / "hotspot_measure.json"]


@card("GLOW-16")
def brand_light_pool(task, wd):
    """A soft brand-tinted pool of light: UI radial-gradient(circle, rgba(accent,.12) 0%, transparent 70%); film: bloom in
    with power2.out to a peak opacity <= .45, then a linear-driven breathe +-6 %. Rendered in numpy (UI frame + 4 s at 30 fps)
    and the alpha is recovered from the pixels."""
    H, W = 180, 320
    acc, bg = np.array([0x06, 0x45, 0xe2]) / 255, np.array([0.04, 0.04, 0.06])
    yy, xx = np.mgrid[:H, :W]
    r = np.hypot(xx - W / 2, yy - H / 2)
    R = math.hypot(W / 2, H / 2)                                   # CSS default: farthest-corner
    prof = np.clip(1 - (r / R) / 0.70, 0, 1)

    def frame(alpha):
        a = (alpha * prof)[..., None]
        return bg * (1 - a) + acc * a
    ui = frame(0.12)
    save(ui, wd / "pool_ui.png")
    rec = lambda img: ((img - bg) / (acc - bg))[..., 2]
    ui8 = png_arr(wd / "pool_ui.png") / 255
    centre_a = float(rec(ui8)[H // 2, W // 2])
    half_a = float(rec(ui8)[H // 2, int(W / 2 + 0.35 * R)])
    edge_a = float(np.abs(rec(ui8)[r > 0.72 * R]).max())
    peak = 0.42
    ts = np.arange(120) / 30
    op = np.where(ts < 1.0, peak * (1 - (1 - np.clip(ts, 0, 1)) ** 2), peak * (1 + 0.06 * np.sin(2 * math.pi * (ts - 1.0) / 2.0)))
    frames = [frame(o) for o in op]
    film = wd / "pool.mkv"                                       # lossless RGB so the alpha can be read back exactly
    done = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (W, H),
                           "-r", "30", "-i", "-", "-c:v", "libx264rgb", "-crf", "0", "-preset", "ultrafast", str(film)],
                          input=b"".join(to8(f).tobytes() for f in frames), capture_output=True, timeout=60)
    if done.returncode:
        raise RuntimeError(done.stderr.decode()[-300:])
    meas = [float(rec(f)[H // 2 - 2:H // 2 + 3, W // 2 - 2:W // 2 + 3].mean()) for f in fx.frames(film, size=(W, H)) / 255]
    hold = np.array(meas[30:])
    jw(wd / "pool_measure.json", {"ui": [centre_a, half_a, edge_a], "film_alpha": meas})
    return [
        check("UI pool: alpha .12 at the centre", abs(centre_a - 0.12) < 0.01, centre_a, 0.12),
        check("linear fade: half of it at 35 % of the radius", abs(half_a - 0.06) < 0.01, half_a, 0.06),
        check("transparent from 70 % of the radius", edge_a < 0.006, edge_a, "~0"),
        check("film: blooms in to the peak by 1 s and never exceeds .45", abs(meas[30] - peak) < 0.02 and max(meas) <= 0.45 + 0.01, [meas[30], max(meas)], "<= .45"),
        check("breathes within +-6 % of the peak", abs(hold.max() / peak - 1.06) < 0.025 and abs(hold.min() / peak - 0.94) < 0.025, [float(hold.min() / peak), float(hold.max() / peak)], [0.94, 1.06]),
        check("negative control: the untreated first frame has no pool", abs(meas[0]) < 0.01, meas[0], 0),
    ], [film, wd / "pool_ui.png", wd / "pool_measure.json"]


def _spring(tsec, k=150.0, c=14.0):
    w0 = math.sqrt(k)
    z = c / (2 * w0)
    wd_ = w0 * math.sqrt(1 - z * z)
    return 1 - math.exp(-z * w0 * tsec) * (math.cos(wd_ * tsec) + z * w0 / wd_ * math.sin(wd_ * tsec))


@card("GLOW-23")
def hero_pop_ring(task, wd):
    """The tested html-canvas starter: a hero word pops .55 -> 1 on prog(local, .2, .75) through a spring 150/14 with a soft
    glow (text-shadow 0 0 60px rgba(126,232,210,.55)) while a 6 px #7ee8d2 ring expands on prog(local, .25, 1.3, outExpo),
    diameter 10 + r 1500, and fades. Rendered at 1/4 scale (480x270) with Pillow; scale and ring size are measured per frame."""
    S, W, H = 0.25, 480, 270
    f = font(220 * S, FONTS / "Poppins-Bold.ttf")
    prog = lambda t, a, b: min(1.0, max(0.0, (t - a) / (b - a)))
    outexpo = lambda p: 1.0 if p >= 1 else 1 - 2 ** (-10 * p)
    word = "GLOW"
    tw = f.getbbox(word)
    base_w = tw[2] - tw[0]
    widths, rings, frames = [], [], []
    for k in range(48):
        t = k / 30
        sc = 0.55 + 0.45 * _spring(prog(t, 0.2, 0.75) * 0.55)
        pr = prog(t, 0.25, 1.3)
        dia = (10 + outexpo(pr) * 1500) * S
        im = Image.new("RGB", (W, H), (8, 10, 14))
        ring = Image.new("L", (W, H), 0)
        if 0 < pr < 1:
            ImageDraw.Draw(ring).ellipse((W / 2 - dia / 2, H / 2 - dia / 2, W / 2 + dia / 2, H / 2 + dia / 2), outline=int(255 * (1 - pr)), width=max(1, round(6 * S)))
        im.paste(Image.new("RGB", (W, H), (0x7e, 0xe8, 0xd2)), (0, 0), ring)
        size = max(1, int(round(220 * S * sc)))
        ff = font(size, FONTS / "Poppins-Bold.ttf")
        txt = Image.new("L", (W, H), 0)
        ImageDraw.Draw(txt).text((W / 2, H / 2), word, font=ff, fill=255, anchor="mm")
        glow = txt.filter(ImageFilter.GaussianBlur(60 * S / 2))
        im.paste(Image.new("RGB", (W, H), (126, 232, 210)), (0, 0), glow.point(lambda v: int(v * 0.55)))
        im.paste(Image.new("RGB", (W, H), (255, 255, 255)), (0, 0), txt)
        a = np.asarray(im).astype(float)
        wm = np.where((a.min(-1) > 200).any(0))[0]
        widths.append((wm.max() - wm.min()) if wm.size else 0)
        rad = None
        if 0 < pr < 1:
            rr = np.asarray(ring).astype(float)
            cols = np.where(rr[H // 2] > 0)[0]
            rad = (cols.max() - cols.min()) if cols.size else None
        rings.append((dia, rad))
        frames.append(a / 255)
    film = write_video(wd / "pop.mp4", frames)
    end_w = widths[-1]
    over = max(widths) / end_w
    want_over = (0.55 + 0.45 * max(_spring(x / 1000 * 0.55) for x in range(1001)))
    chk = [(d, r) for d, r in rings if r is not None and d < H]
    rerr = max(abs(r - d) for d, r in chk) if chk else 99
    jw(wd / "pop_measure.json", {"widths": [int(x) for x in widths], "overshoot": over, "want_overshoot": want_over, "ring": rings[:20]})
    return [
        check("pop starts at .55 of the rest width", abs(widths[6] / end_w - 0.55) < 0.06, widths[6] / end_w, 0.55),
        check("spring 150/14 overshoots ~11 % before settling", abs(over - want_over) < 0.04 and over > 1.05, over, want_over),
        check("rests at scale 1 after .75 s", abs(widths[30] / end_w - 1) < 0.03, widths[30] / end_w, 1),
        check("ring diameter follows 10 + outExpo(p) * 1500 (1/4 scale) within 2 px", rerr <= 2, rerr, "<= 2 px"),
        check("negative control: before .2 s the word has not popped (still .55)", abs(widths[0] / end_w - 0.55) < 0.06 and widths[0] < 0.7 * end_w, widths[0] / end_w, 0.55),
    ], [film, wd / "pop_measure.json"]


def _vendored_qa():
    import importlib.util
    spec = importlib.util.spec_from_file_location("kosif_vendor_qa", VENDOR_SCRIPTS / "qa.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@card("GLOW-40")
def qa_lint_text_shadow(task, wd):
    """The vendored qa.py lint warns when text-shadow blur >= 20 px or the shadow colour is not black ('glow on type ... a
    fast tell of generated work'); dark soft shadows pass. Run on three fixture projects."""
    qa = _vendored_qa()
    base = ('<!doctype html><html><body><div data-composition-id="x"></div><style>%s</style>'
            '<script>window.__timelines = {}; window.__timelines["x"] = null;</script></body></html>')
    cases = {"big": "h1{text-shadow:0 0 60px rgba(126,232,210,.55)}", "colour": "h1{text-shadow:0 2px 6px rgba(255,0,128,.6)}",
             "dark": "h1{text-shadow:0 2px 8px rgba(0,0,0,.45)}"}
    res = {}
    for k, css in cases.items():
        d = wd / k
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(base % css, encoding="utf-8")
        res[k] = [w for w in qa.lint(d) if "text-shadow" in w["rule"] or "glow on type" in w["rule"]]
    rep = jw(wd / "lint_report.json", res)
    return [
        check("60 px tinted glow on type is flagged", len(res["big"]) == 1 and res["big"][0]["level"] == "warn", res["big"], "1 warn"),
        check("a small but coloured shadow is flagged", len(res["colour"]) == 1, len(res["colour"]), 1),
        check("negative control: a dark soft 8 px shadow passes", res["dark"] == [], res["dark"], []),
    ], [rep]


@card("GLOW-42")
def one_pass_sheen(task, wd):
    """Card: ::before inset -65% -18%, linear-gradient(112deg, transparent 42%, primary 10% at 50%, transparent 58%),
    translate 42% -> -42% with rotate 6deg, 950 ms, delay 260 ms; button ::after glint 24% wide, rotate(14deg), translateX
    0 -> 520%, 720 ms; iteration count 1, so nothing loops. Chrome seeks the CSS animations and reads computed transforms."""
    html = """<!doctype html><html><head><style>html,body{margin:0;background:#0b0f17}
.card{position:absolute;left:40px;top:30px;width:240px;height:120px;border-radius:14px;background:#1b2333;overflow:hidden}
.card::before{content:'';position:absolute;inset:-65% -18%;background:linear-gradient(112deg,transparent 42%,rgba(120,200,255,.35) 50%,transparent 58%);
  transform:translateX(42%) rotate(6deg);animation:sheen 950ms cubic-bezier(.22,1,.36,1) 260ms 1 both}
@keyframes sheen{from{transform:translateX(42%) rotate(6deg)}to{transform:translateX(-42%) rotate(6deg)}}
.btn{position:absolute;left:80px;top:160px;width:160px;height:40px;border-radius:20px;background:#2563eb;overflow:hidden}
.btn::after{content:'';position:absolute;top:0;left:0;width:24%;height:100%;transform:translateX(0) rotate(14deg);
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.55),transparent);animation:glint 720ms ease-out 1 both}
@keyframes glint{0%{transform:translateX(0) rotate(14deg);opacity:0}24%{opacity:.9}100%{transform:translateX(520%) rotate(14deg);opacity:0}}
</style></head><body><div class="card"></div><div class="btn"></div><script>window.__done = true;</script></body></html>"""
    js = ("(() => { document.getAnimations().forEach(a => { a.pause(); a.currentTime = %d; });"
          "const c = document.querySelector('.card'), b = document.querySelector('.btn');"
          "const mc = new DOMMatrix(getComputedStyle(c, '::before').transform), mb = new DOMMatrix(getComputedStyle(b, '::after').transform);"
          "const wc = parseFloat(getComputedStyle(c, '::before').width), wb = parseFloat(getComputedStyle(b, '::after').width);"
          "return {tx: mc.e / wc, rot: Math.atan2(mc.b, mc.a) * 180 / Math.PI, bx: mb.e / wb, bo: +getComputedStyle(b, '::after').opacity,"
          "iters: document.getAnimations().map(a => a.effect.getTiming().iterations)}; })()")
    times = [0, 260, 735, 1210, 3000]
    r = pw(wd, "sheen.html", [{"js": js % t, "shot": "sheen_%d.png" % t if t == 735 else None} for t in times], w=320, h=220, html=html)
    a = {t: v for t, v in zip(times, r)}
    shot = png_arr(wd / "sheen_735.png")
    jw(wd / "sheen_measure.json", a)
    return [
        check("one pass only: every animation has iteration count 1", all(i == 1 for i in a[0]["iters"]), a[0]["iters"], 1),
        check("band waits for the 260 ms delay at +42 %", abs(a[0]["tx"] - 0.42) < 1e-3 and abs(a[260]["tx"] - 0.42) < 1e-3, [a[0]["tx"], a[260]["tx"]], 0.42),
        check("band ends at -42 % with rotate 6deg", abs(a[1210]["tx"] + 0.42) < 1e-3 and abs(a[1210]["rot"] - 6) < 0.01, [a[1210]["tx"], a[1210]["rot"]], [-0.42, 6]),
        check("mid-pass the band is between the ends and lights the card", -0.42 < a[735]["tx"] < 0.42 and float(shot[40:140, 50:270].max()) > 60, a[735]["tx"], "(-.42, .42)"),
        check("button glint travels 0 -> 520 % of its width and ends invisible", abs(a[0]["bx"]) < 1e-3 and abs(a[1210]["bx"] - 5.2) < 1e-3 and a[1210]["bo"] == 0, [a[0]["bx"], a[1210]["bx"], a[1210]["bo"]], [0, 5.2, 0]),
        check("negative control: nothing loops back - at 3 s the state equals the end state, not the start", abs(a[3000]["tx"] + 0.42) < 1e-3 and abs(a[3000]["bx"] - 5.2) < 1e-3,
              [a[3000]["tx"], a[3000]["bx"]], [-0.42, 5.2]),
    ], [wd / "sheen_735.png", wd / "sheen_measure.json"]


@card("GLOW-43")
def light_sweep_pass(task, wd):
    """The HyperFrames light-sweep-pass block (installed with `hyperframes add`): one --light-x proxy drives the diagonal
    band (translateX((x - 50) * 1.4cqw)) and every [data-lit] highlight (opacity clamp(1 - |x - lsp_x| / 26, 0, 1) * .32) and
    shadow offset in lockstep: parked at -35, one sine.inOut crossing to 118 from sweep_at .9 s over 1.6 s, settle to 62."""
    d, _ = _hf_add(wd, "light-sweep-pass")
    src = d / "compositions/components/light-sweep-pass.html"
    host = """<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:#000}#host{position:relative;width:640px;height:360px;overflow:hidden}</style></head>
<body><div id="host"></div><script src="http://k/nm/gsap/dist/gsap.min.js"></script><script>
fetch('http://k/w/hf/compositions/components/light-sweep-pass.html').then(r => r.text()).then(t => {
  const doc = new DOMParser().parseFromString(t, 'text/html'); const tpl = doc.querySelector('template');
  const host = document.getElementById('host'); const frag = tpl.content.cloneNode(true); const scripts = [...frag.querySelectorAll('script')];
  scripts.forEach(s => s.remove()); host.appendChild(frag);
  scripts.filter(s => !s.src).forEach(s => (0, eval)(s.textContent));
  window.__done = true; }).catch(e => window.__err = String(e));
</script></body></html>"""
    meas = ("(() => { const root = document.getElementById('root'); const lit = [...root.querySelectorAll('[data-lit]')];"
            "const band = root.querySelector('.lsp-band'); const m = new DOMMatrix(getComputedStyle(band).transform);"
            "return {x: parseFloat(root.style.getPropertyValue('--light-x')), cqw: root.getBoundingClientRect().width / 100, band_tx: m.e,"
            "lit: lit.map(e => ({lx: parseFloat(e.style.getPropertyValue('--lsp-x')), glow: +getComputedStyle(e, '::after').opacity,"
            "sx: parseFloat(getComputedStyle(e).boxShadow.match(/(-?[\\d.]+)px/)[1])}))}; })()")
    times = [0, 0.9, 1.3, 1.7, 2.1, 2.5, 3.05, 3.9]
    steps = [{"js": "window.__timelines['light-sweep-pass'].seek(%s, false); %s" % (t, meas), "shot": "sweep_%d.png" % int(t * 100) if t in (1.7, 3.9) else None} for t in times]
    r = pw(wd, "host.html", steps, w=640, h=360, html=host)
    errs, sh = [], []
    for st in r:
        for e in st["lit"]:
            want = max(0.0, min(1.0, 1 - abs(st["x"] - e["lx"]) / 26)) * 0.32
            errs.append(abs(e["glow"] - want))
            sh.append(abs(e["sx"] - max(-30, min(30, st["x"] - e["lx"])) * -0.05 * st["cqw"]))
    band_err = max(abs(st["band_tx"] - (st["x"] - 50) * 1.4 * st["cqw"]) for st in r)
    xs = [st["x"] for st in r]
    sweep = xs[1:6]
    jw(wd / "sweep_measure.json", {"t": times, "frames": r, "glow_err": max(errs), "shadow_err": max(sh), "band_err": band_err})
    return [
        check("one scalar: every highlight opacity = clamp(1 - |x - lsp_x| / 26) * .32", max(errs) < 2e-3, max(errs), "< 2e-3"),
        check("every shadow x-offset = clamp(d, -30, 30) * -0.05 cqw (lockstep)", max(sh) < 0.05, max(sh), "< 0.05 px"),
        check("the band transform is translateX((x - 50) * 1.4 cqw)", band_err < 0.05, band_err, "< 0.05 px"),
        check("one crossing: -35 at sweep start, increasing monotonically during the pass", abs(xs[1] + 35) < 1e-3 and all(a < b for a, b in zip(sweep, sweep[1:])), sweep, "increasing from -35"),
        check("settles at the resting key 62 (3.05 s) and holds", abs(xs[6] - 62) < 0.05 and abs(xs[7] - 62) < 0.05, xs[6:], [62, 62]),
        check("negative control: parked at t = 0 nothing is lit", abs(xs[0] + 35) < 1e-3 and max(e["glow"] for e in r[0]["lit"]) == 0, [xs[0], max(e["glow"] for e in r[0]["lit"])], [-35, 0]),
    ], [wd / "sweep_170.png", wd / "sweep_measure.json", src]


@card("GLOW-57")
def light_rig_stops(task, wd):
    """K3.lightRig(scene, {...}): key 3.0 @5600 K az -40 el 35 (shadows), fill 6500 K az 45 el 10 at -2 stops (a 5:1 lighting
    ratio), rim 4300 K az 160 el 40 at +.5 stop; rig.set({...}) re-balances per shot and rig.ratio() reports the ratio.
    A lit sphere is rendered linear (no tone curve) and the key/fill sides are metered on the picture."""
    js = """
const W = 320, H = 180;
function shot(p) {
  const r = K3.makeRenderer(cv, W, H, {}); r.toneMapping = T.NoToneMapping; r.outputColorSpace = T.LinearSRGBColorSpace;
  const s = new T.Scene(); s.background = new T.Color(0, 0, 0);
  const rig = K3.lightRig(s, {}); rig.set(Object.assign({}, p, {key: 0.5})); rig.rim.intensity = 0;   // meter key vs fill only, below clipping
  const ball = new T.Mesh(new T.SphereGeometry(1, 96, 48), new T.MeshLambertMaterial({color: 0xffffff})); s.add(ball);
  const cam = new T.PerspectiveCamera(30, W / H, 0.1, 50); cam.position.set(0, 0, 6); cam.lookAt(0, 0, 0);
  r.render(s, cam); const gl = r.getContext(), b = new Uint8Array(W * H * 4); gl.readPixels(0, 0, W, H, gl.RGBA, gl.UNSIGNED_BYTE, b);
  const proj = v => { const q = v.clone().project(cam); return [Math.round((q.x + 1) / 2 * W), Math.round((q.y + 1) / 2 * H)]; };
  const kd = rig.key.position.clone().normalize(), fd = rig.fill.position.clone().normalize();
  const at = (d) => { const [x, y] = proj(d); let s2 = 0, n = 0; for (let j = -2; j <= 2; j++) for (let i = -2; i <= 2; i++) { const o = ((y + j) * W + (x + i)) * 4; s2 += b[o] + b[o + 1] + b[o + 2]; n++; } return s2 / n / 3; };
  r.render(s, cam);
  const fresh = K3.lightRig(new T.Scene(), {}); fresh.set(p);
  return {png: grab(r), ratio: fresh.ratio(), key: fresh.key.intensity, fill: fresh.fill.intensity, rim: fresh.rim.intensity,
    keyCol: fresh.key.color.toArray(), rimCol: fresh.rim.color.toArray(), fillCol: fresh.fill.color.toArray(), shadows: fresh.key.castShadow,
    meterKey: at(kd), meterFill: at(fd)};
}
window.__result = {def: shot({}), one: shot({fillStops: 1}), flat: shot({fillStops: 0})}; window.__done = true;
"""
    r = pw(wd, "rig.html", [{"js": "window.__result"}], html=k3_page(320, 180, js))[0]
    for k in r:
        data_url_to_png(r[k].pop("png"), wd / ("rig_%s.png" % k))
    d, o, fl = r["def"], r["one"], r["flat"]
    warm = d["rimCol"][0] / max(1e-6, d["rimCol"][2]) > d["keyCol"][0] / max(1e-6, d["keyCol"][2]) > d["fillCol"][0] / max(1e-6, d["fillCol"][2])
    jw(wd / "rig_measure.json", r)
    return [
        check("ratio() = 5 with the defaults (fill -2 stops)", abs(d["ratio"] - 5) < 1e-9, d["ratio"], 5),
        check("fill = key x 2^-2, rim = key x 2^0.5", abs(d["fill"] - 0.75) < 1e-9 and abs(d["rim"] - 3 * 2 ** 0.5) < 1e-9, [d["key"], d["fill"], d["rim"]], [3, 0.75, 3 * 2 ** 0.5]),
        check("rig.set({fillStops: 1}) re-balances to a 3:1 ratio", abs(o["ratio"] - 3) < 1e-9, o["ratio"], 3),
        check("Kelvin: rim 4300 K warmer than key 5600 K warmer than fill 6500 K", warm, [d["rimCol"], d["keyCol"], d["fillCol"]], "R/B decreasing"),
        check("key casts shadows", d["shadows"] is True, d["shadows"], True),
        check("on the (linear) picture the key side meters > 2x the fill side", d["meterKey"] > 2 * d["meterFill"], [d["meterKey"], d["meterFill"]], "key > 2 x fill"),
        check("negative control: fill at 0 stops gives a flat 2:1 (key ~ fill on the picture)", abs(fl["ratio"] - 2) < 1e-9 and fl["meterKey"] < 1.3 * fl["meterFill"],
              [fl["ratio"], fl["meterKey"], fl["meterFill"]], [2, "key ~ fill"]),
    ], [wd / "rig_def.png", wd / "rig_measure.json"]


@card("GLOW-70")
def key_agreeing_shadow(task, wd):
    """Shadow offset, lit-edge highlight and reflection band agree with one top-left key and are recomputed per frame from
    yaw and lift: box-shadow x = -yaw * 1.6 px, y 48 px, blur 90 px at .55; reflection linear-gradient(115deg ...14% white).
    Chrome renders the card at three yaws; the shadow's centroid is measured against the card's."""
    yaws = [-20, 0, 20]
    html = """<!doctype html><html><head><style>html,body{margin:0;background:#e9e6df}
.c{position:absolute;left:220px;top:90px;width:200px;height:120px;border-radius:16px;background:#fdfdfd}
.c::after{content:'';position:absolute;inset:0;border-radius:16px;background:linear-gradient(115deg,transparent 40%,rgba(255,255,255,.14) 50%,transparent 60%)}
</style></head><body><div class="c" id="c"></div><script>
window.setYaw = (yaw, lift, live) => { const c = document.getElementById('c'); const y = live ? yaw : 0;
  c.style.boxShadow = `${-y * 1.6}px ${48 + lift}px 90px rgba(0,0,0,.55), inset 1px 1px 0 rgba(255,255,255,.09)`; return c.style.boxShadow; };
window.__done = true;</script></body></html>"""
    steps = [{"js": "setYaw(%d, 0, true)" % y, "shot": "yaw_%d.png" % (y + 100)} for y in yaws] + \
            [{"js": "setYaw(%d, 0, false)" % y, "shot": "static_%d.png" % (y + 100)} for y in yaws]
    r = pw(wd, "yaw.html", steps, w=640, h=360, html=html)

    def centroid(p):
        a = luma(png_arr(p) / 255)
        bgv = float(np.median(a[:20]))
        m = np.clip(bgv - a, 0, None)
        m[90:210, 220:420] = 0                                # the card itself
        ys, xs = np.mgrid[:a.shape[0], :a.shape[1]]
        return float((xs * m).sum() / m.sum()), float((ys * m).sum() / m.sum())
    cx = {y: centroid(wd / ("yaw_%d.png" % (y + 100))) for y in yaws}
    sx = {y: centroid(wd / ("static_%d.png" % (y + 100))) for y in yaws}
    slope = (cx[20][0] - cx[-20][0]) / 40
    jw(wd / "yaw_measure.json", {"live": cx, "static": sx, "css": r, "slope": slope})
    # blur and the card mask shift the centroid less than the full offset; the sign and linearity are the method
    lin = abs((cx[0][0] - cx[-20][0]) - (cx[20][0] - cx[0][0]))
    return [
        check("shadow box offset recomputed per yaw: x = -yaw * 1.6 (CSS)", " 32px 48px 90px" in r[0] and " -32px 48px 90px" in r[2] and " 0px 48px 90px" in r[1], r[:3], ["32px 48px 90px", "0px", "-32px"]),
        check("the measured shadow moves opposite to the yaw (top-left key)", slope < -0.5, slope, "< -0.5 px per degree"),
        check("linear in yaw (equal steps -20 -> 0 -> 20 within 1 px)", lin < 1.0, lin, "< 1 px"),
        check("shadow falls below the card (centroid y > card centre)", all(c[1] > 150 + 10 for c in cx.values()), [c[1] for c in cx.values()], "> 160"),
        check("negative control: a shadow not recomputed from yaw does not move", abs(sx[20][0] - sx[-20][0]) < 0.2, sx[20][0] - sx[-20][0], "~0"),
    ], [wd / "yaw_120.png", wd / "yaw_measure.json"]


@card("GLOW-80")
def fake_volumetric_beam(task, wd):
    """2D: two opposite triangular wedges (12 deg) from the lamp, linear alpha .35 -> 0 along the length, 'lighter' (additive)
    blend, one revolution per 6 s; 3D profile: a = pow(1 - v, 1.6) * .55 * (.6 + .4 sin(u 2 pi 3)). Frames in numpy; the beam's
    angle and its alpha along the length are measured."""
    H, W = 270, 480
    cx, cy = W / 2, H / 2
    yy, xx = np.mgrid[:H, :W]
    ang = np.arctan2(yy - cy, xx - cx)
    rad = np.hypot(xx - cx, yy - cy)
    Lb = 220.0
    bg = np.full((H, W, 3), [0.05, 0.05, 0.08])
    col = np.array([0xff, 0xe7, 0xb8]) / 255
    frames, angles = [], []
    for k in range(91):
        t = k / 30
        th = 2 * math.pi * t / 6.0
        a = np.zeros((H, W))
        for off in (0, math.pi):
            dth = np.abs((ang - th - off + math.pi) % (2 * math.pi) - math.pi)
            a += np.where((dth < math.radians(6)) & (rad < Lb), 0.35 * (1 - rad / Lb), 0)
        img = np.clip(bg + a[..., None] * col, 0, 1)            # 'lighter' = additive
        frames.append(img)
        ring = (rad > 40) & (rad < 120)
        w_ = a[ring]
        two = math.atan2(float((w_ * np.sin(2 * ang[ring])).sum()), float((w_ * np.cos(2 * ang[ring])).sum()))
        angles.append(math.degrees(two / 2) % 180)
    film = write_video(wd / "beam.mp4", frames)
    f0 = frames[0]
    along = [float((f0[int(cy), int(cx + r_)] - bg[0, 0])[0] / col[0]) for r_ in (20, 110, 200)]
    want = [0.35 * (1 - r_ / Lb) for r_ in (20, 110, 200)]
    rot = [(angles[k] - (360 * (k / 30) / 6) % 180 + 90) % 180 - 90 for k in range(91)]
    v = np.linspace(0, 1, 5)
    u = np.linspace(0, 1, 7)
    prof3d = (np.power(1 - v, 1.6)[:, None] * 0.55 * (0.6 + 0.4 * np.sin(u * 2 * math.pi * 3))[None, :])
    jw(wd / "beam_measure.json", {"alpha_along": along, "want": want, "angle_err_deg": max(map(abs, rot)), "profile3d": prof3d.tolist()})
    return [
        check("alpha falls linearly .35 -> 0 along the beam", np.allclose(along, want, atol=0.01), along, want),
        check("one revolution per 6 s: beam angle = 60 deg/s on every frame (within 1 deg)", max(map(abs, rot)) <= 1.0, max(map(abs, rot)), "<= 1 deg"),
        check("two opposite wedges (light at +x and -x at t = 0)", f0[int(cy), int(cx + 60)][0] > 0.2 and f0[int(cy), int(cx - 60)][0] > 0.2, [float(f0[int(cy), int(cx + 60)][0]), float(f0[int(cy), int(cx - 60)][0])], "> .2"),
        check("3D cone profile: a(v=0) = .55 (.6 + .4 sin) and 0 at the tip", abs(prof3d[0, 0] - 0.33) < 1e-9 and np.allclose(prof3d[-1], 0), [float(prof3d[0, 0]), float(prof3d[-1].max())], [0.33, 0]),
        check("negative control: off the wedges (90 deg away) the frame is the untreated background", float(np.abs(f0[int(cy) - 60, int(cx)] - bg[0, 0]).max()) < 1e-9, float(np.abs(f0[int(cy) - 60, int(cx)] - bg[0, 0]).max()), 0),
    ], [film, wd / "beam_measure.json"]


@card("GLOW-82")
def wet_ground_reflection(task, wd):
    """Wet ground mirrors the sign: flipped around the wall/floor junction in 3 px strips with ripple, a sharp layer inside
    puddle masks (2 px blur) and a 16 px half-res film elsewhere, times a Fresnel fade .9 (far) -> .25 (near). numpy."""
    H, W, J = 270, 480, 150
    img = np.zeros((H, W, 3))
    img[:J] = [0.06, 0.06, 0.09]
    img[J:] = [0.03, 0.03, 0.04]
    sign = np.zeros((H, W, 3))
    t_ = Image.new("L", (W, J), 0)
    ImageDraw.Draw(t_).text((W / 2, J * 0.55), "NEON", font=font(64, FONTS / "Poppins-Bold.ttf"), fill=255, anchor="mm")
    m = np.asarray(t_).astype(float) / 255
    sign[:J] = m[..., None] * [1.0, 0.2, 0.6]
    wall = img.copy()
    wall[:J] = np.maximum(wall[:J], sign[:J])
    refl = np.zeros((H, W, 3))
    rows = H - J
    for y in range(rows):
        src = J - 1 - y
        if src < 0:
            break
        strip = y // 3
        dx = int(round(3 * math.sin(strip * 0.9)))
        refl[J + y] = np.roll(sign[src], dx, axis=0)
    yy, xx = np.mgrid[:H, :W]
    puddle = ((xx - 240) / 170) ** 2 + ((yy - 200) / 40) ** 2 < 1
    sharp = gblur(refl, 2)
    film_l = gblur(refl[::2, ::2], 8).repeat(2, 0).repeat(2, 1)[:H, :W]
    lay = np.where(puddle[..., None], sharp, film_l)
    fres = np.zeros((H, 1))
    fres[J:, 0] = 0.9 + (0.25 - 0.9) * (np.arange(rows) / (rows - 1))
    out = np.clip(wall + lay * fres[..., None], 0, 1)
    save(out, wd / "wet.png")
    # measurements on the produced frame
    o = png_arr(wd / "wet.png") / 255
    groundL = luma(o[J:]) - luma(img[J:])
    upper = luma(sign[:J])
    mirrored = upper[::-1][:rows]
    corr = float(np.corrcoef(gblur(mirrored, 3).ravel(), groundL[:len(mirrored)].ravel())[0, 1])
    shifts = [int(round(3 * math.sin(s_ * 0.9))) for s_ in range(rows // 3)]
    inside = np.abs(np.diff(luma(o)[J:], axis=1))[puddle[J:, 1:]].mean()
    outside = np.abs(np.diff(luma(o)[J:], axis=1))[(~puddle[J:, 1:]) & (groundL[:, 1:] > 0.01)].mean()
    # Fresnel: the ratio of reflected light to source light near the junction vs further down
    ratio_ = []
    for y0 in (2, 60):
        src = upper[J - 1 - y0]
        r_ = groundL[y0]
        ratio_.append(float(r_.sum() / max(1e-6, gblur(src[None, :], 0).sum())))
    plain = luma(img[J:])
    jw(wd / "wet_measure.json", {"mirror_corr": corr, "sharp_in_puddle": float(inside), "soft_outside": float(outside), "fresnel_ratio": ratio_, "strip_shifts": shifts[:12]})
    return [
        check("the ground shows the sign mirrored about the junction (corr > .5)", corr > 0.5, corr, "> .5"),
        check("ripple: 3 px strips each shifted as one (shifts vary, constant inside a strip)", len(set(shifts)) > 3, shifts[:8], "varied per strip"),
        check("sharp inside the puddle, blurred film outside", inside > 1.5 * outside, [float(inside), float(outside)], "inside > 1.5x outside"),
        check("Fresnel: the far rows reflect more than the near rows", ratio_[0] > ratio_[1] * 1.2, ratio_, "far > near"),
        check("negative control: the untreated dry ground has no reflection", float(np.abs(plain - plain.mean()).max()) < 1e-9, float(np.abs(plain - plain.mean()).max()), 0),
    ], [wd / "wet.png", wd / "wet_measure.json"]


def lens_pass(img, k=0.04, ca=1.5, bloom=0.35, thr=0.72, vig=0.35, grain=0.02, seed=1):
    """The owner lens.py method in numpy: barrel bulge k, radial chromatic aberration ca px at the corner, bloom from
    highlights above thr at three radii (h * .006 / .02 / .06, weights .7 / 1 / .45, screen blend, auto-off on bright frames),
    vignette, grain."""
    from scipy.ndimage import map_coordinates
    H, W = img.shape[:2]
    yy, xx = np.mgrid[:H, :W].astype(float)
    cx, cy = (W - 1) / 2, (H - 1) / 2
    R = math.hypot(cx, cy)
    nx, ny = (xx - cx) / R, (yy - cy) / R
    r2 = nx * nx + ny * ny
    out = np.zeros_like(img)
    for c, sh in ((0, ca), (1, 0.0), (2, -ca)):
        scale = (1 + sh / R * 1.0)          # channel scale: red pushed out by ca px at the corner, blue pulled in
        sx = cx + (xx - cx) / (1 + k * r2) / scale
        sy = cy + (yy - cy) / (1 + k * r2) / scale
        out[..., c] = map_coordinates(img[..., c], [sy, sx], order=1, mode="nearest")
    L = luma(out)
    if bloom > 0 and L.mean() < 0.6:
        hi = np.clip(out - thr, 0, None) / (1 - thr)
        b = sum(w * gblur(hi, max(0.5, H * f)) for w, f in ((0.7, 0.006), (1.0, 0.02), (0.45, 0.06))) * bloom
        out = 1 - (1 - out) * (1 - np.clip(b, 0, 1))
    v = 1 - vig * np.clip(r2, 0, 1)
    out = out * v[..., None]
    if grain > 0:
        out = out + np.random.default_rng(seed).normal(0, grain, out.shape[:2])[..., None]
    return np.clip(out, 0, 1)


@card("GLOW-X01")
def lens_final_pass(task, wd):
    """A final pass that adds what a real lens does (lens.py --k .04 --ca 1.5 --bloom .35 --thr .72 --vig .35 --grain .02):
    barrel bulge, radial colour fringes, three-scale bloom with auto-off on bright frames, vignette and grain. Each effect is
    measured on a fixture of white dots, a bright spot and a flat grey field; the untreated frame is the control."""
    H, W = 180, 320
    base = np.full((H, W, 3), 0.25)
    pts = [(40, 30), (280, 30), (40, 150), (280, 150), (160, 90)]
    yy, xx = np.mgrid[:H, :W]
    for x, y in pts:
        base[np.hypot(xx - x, yy - y) < 2.5] = 1.0
    base[np.hypot(xx - 100, yy - 90) < 5] = 1.0
    out = lens_pass(base)
    save(base, wd / "lens_in.png")
    save(out, wd / "lens_out.png")
    nog = lens_pass(base, grain=0)

    def cen(a, x, y, c=None):
        win = (a[max(0, y - 12):y + 13, max(0, x - 12):x + 13] if c is None else a[max(0, y - 12):y + 13, max(0, x - 12):x + 13, c])
        L = luma(win) if c is None else win
        m = np.clip(L - 0.5, 0, None)
        ys, xs = np.mgrid[:m.shape[0], :m.shape[1]]
        return float((xs * m).sum() / m.sum()) + max(0, x - 12), float((ys * m).sum() / m.sum()) + max(0, y - 12)
    R = math.hypot((W - 1) / 2, (H - 1) / 2)
    c0 = cen(nog, 40, 30)
    r_in = math.hypot(40 - 159.5, 30 - 89.5)
    r_out = math.hypot(c0[0] - 159.5, c0[1] - 89.5)
    # barrel: a source pixel at radius r lands where r_out / (1 + k (r_out/R)^2) = r_in
    want_out = r_in
    for _ in range(30):
        want_out = r_in * (1 + 0.04 * (want_out / R) ** 2)
    red, blue = cen(nog, 280, 150, 0), cen(nog, 280, 150, 2)
    fringe = math.hypot(red[0] - blue[0], red[1] - blue[1])
    halo = float(luma(nog)[90, 108] - luma(lens_pass(base, bloom=0, grain=0))[90, 108])
    bright = np.full((H, W, 3), 0.8)
    bright[np.hypot(xx - 100, yy - 90) < 5] = 1.0
    auto_off = float(np.abs(lens_pass(bright, grain=0) - lens_pass(bright, bloom=0, grain=0)).max())
    vg = float(luma(nog)[2, 2] / luma(nog)[90, 60])
    rc = (math.hypot(2 - 159.5, 2 - 89.5) / R) ** 2
    rr = (math.hypot(60 - 159.5, 90 - 89.5) / R) ** 2
    want_vg = (1 - 0.35 * rc) / (1 - 0.35 * rr)
    gstd = float((out - nog)[60:80, 200:230].std())
    jw(wd / "lens_measure.json", {"barrel_r": [r_in, r_out, want_out], "fringe_px": fringe, "halo": halo, "auto_off": auto_off, "vignette_ratio": vg, "grain_std": gstd})
    return [
        check("barrel bulge pushes a corner dot outward to r (1 + k (r/R)^2) within 0.5 px", abs(r_out - want_out) < 0.5 and r_out > r_in + 1, [r_in, r_out, want_out], want_out),
        check("radial colour fringe: red and blue separate ~2 x 1.5 px x r/R at the corner dot", 1.2 < fringe < 3.2, fringe, "~2.3 px"),
        check("bloom lifts the halo around the bright spot", halo > 0.01, halo, "> .01"),
        check("bloom auto-off on a bright frame", auto_off < 1e-9, auto_off, 0),
        check("vignette: corner / mid-left = (1 - .35 r_c^2) / (1 - .35 r_m^2)", abs(vg - want_vg) < 0.02, vg, want_vg),
        check("grain std ~ .02", 0.015 < gstd < 0.025, gstd, 0.02),
        check("negative control: the untreated frame has no fringe and no vignette", float(np.abs(base[..., 0] - base[..., 2]).max()) == 0 and abs(luma(base)[2, 2] - luma(base)[90, 60]) < 1e-9, 0, 0),
    ], [wd / "lens_out.png", wd / "lens_measure.json"]


# ================================================================================================ maps / geo
_MAP_HEAD = """<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="http://k/nm/maplibre-gl/dist/maplibre-gl.css">
<style>@font-face{font-family:Cairo;src:url(http://k/fonts/Cairo%5Bslnt,wght%5D.ttf)}html,body{margin:0;background:#000}
#map{position:absolute;left:0;top:0;width:__W__px;height:__H__px}.lbl{position:absolute;transform:translate(-50%,-50%);font:700 14px Cairo;color:#fff;direction:rtl;white-space:nowrap}</style>
</head><body><div id="map"></div><div id="ov"></div><script src="http://k/nm/topojson-client/dist/topojson-client.min.js"></script>
<script type="module">
import * as maplibregl from 'http://k/nm/maplibre-gl/dist/maplibre-gl.mjs';
window.maplibregl = maplibregl;
const idle = (map) => new Promise(res => { if (map.loaded() && !map.isMoving() && map.areTilesLoaded()) map.once('idle', res); else map.once('idle', res); map.triggerRepaint(); });
const world = async () => { const t = await (await fetch('http://k/nm/world-atlas/countries-110m.json')).json(); return topojson.feature(t, t.objects.countries); };
function mk(style, o) { return new maplibregl.Map(Object.assign({container: 'map', style, interactive: false, fadeDuration: 0, attributionControl: false,
  canvasContextAttributes: {preserveDrawingBuffer: true, antialias: false}}, o)); }
function px(map, x, y) { const gl = map.painter.context.gl, b = new Uint8Array(4); gl.readPixels(x, gl.drawingBufferHeight - 1 - y, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, b); return [b[0], b[1], b[2]]; }
function hash(s) { let h = 2166136261; for (let i = 0; i < s.length; i += 3) h = Math.imul(h ^ s.charCodeAt(i), 16777619) >>> 0; return h; }
(async () => { try {
__JS__
} catch (e) { window.__err = String(e.stack || e); } })();
</script></body></html>"""


def map_page(w, h, js):
    return _MAP_HEAD.replace("__W__", str(w)).replace("__H__", str(h)).replace("__JS__", js)


_ARAB = ["Saudi Arabia", "Egypt", "Jordan", "Iraq", "Syria", "Yemen", "Oman", "United Arab Emirates", "Qatar", "Kuwait", "Lebanon",
         "Libya", "Tunisia", "Algeria", "Morocco", "Sudan", "Mauritania", "Somalia", "Palestine", "Israel", "Djibouti", "Bahrain", "W. Sahara"]


def merc(lon, lat, zoom, tile=512):
    """web-mercator world pixel at zoom (MapLibre uses 512 px tiles)"""
    s = tile * 2 ** zoom
    x = (lon + 180) / 360 * s
    y = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * s
    return x, y


@card("MAP-13")
def maplibre_deterministic(task, wd):
    """MapLibre configured for identical headless frames: interactive:false, fadeDuration:0, preserveDrawingBuffer:true;
    on frame 0 map.jumpTo(camera) then wait for 'idle' before capturing; coordinates [lng, lat]. Two independent map
    instances render the same camera and must match byte for byte; Riyadh's pixel must hold Saudi Arabia's fill."""
    js = """
const fc = await world();
const style = {version: 8, sources: {w: {type: 'geojson', data: fc}}, layers: [
  {id: 'bg', type: 'background', paint: {'background-color': '#0b1d33'}},
  {id: 'land', type: 'fill', source: 'w', paint: {'fill-color': '#2b3a4a'}},
  {id: 'ksa', type: 'fill', source: 'w', filter: ['==', ['get', 'name'], 'Saudi Arabia'], paint: {'fill-color': '#22d3ee'}},
  {id: 'b', type: 'line', source: 'w', paint: {'line-color': '#8899aa', 'line-width': 0.6}}]};
async function shot(cam) { const map = mk(style, {center: [0, 0], zoom: 1}); await new Promise(r => map.once('load', r));
  map.jumpTo(cam); await idle(map); const u = map.getCanvas().toDataURL('image/png'); const p = map.project([46.72, 24.69]);
  const c = px(map, Math.round(p.x), Math.round(p.y)); const o = {png: u, h: hash(u), riyadh: [p.x, p.y], rgb: c, opts: {fade: map._fadeDuration, interactive: map._interactive}}; map.remove(); return o; }
const cam = {center: [45, 24], zoom: 3.2, bearing: 0, pitch: 0};
window.__result = {a: await shot(cam), b: await shot(cam), c: await shot({center: [30, 27], zoom: 3.6})}; window.__done = true;
"""
    r = pw(wd, "map13.html", [{"js": "window.__result"}], w=320, h=180, html=map_page(320, 180, js), timeout=30)[0]
    for k in "abc":
        data_url_to_png(r[k].pop("png"), wd / ("map_%s.png" % k))
    a, b, c = r["a"], r["b"], r["c"]
    ex, ey = merc(46.72, 24.69, 3.2)
    cx, cy = merc(45, 24, 3.2)
    want = (160 + ex - cx, 90 + ey - cy)
    same = sha(wd / "map_a.png") == sha(wd / "map_b.png")
    jw(wd / "map13_measure.json", r | {"riyadh_expected": want})
    return [
        check("two independent renders of the same camera are byte-identical", same, [sha(wd / "map_a.png")[:12], sha(wd / "map_b.png")[:12]], "equal"),
        check("[lng, lat] order: Riyadh projects to the web-mercator pixel (512 px tiles)", abs(a["riyadh"][0] - want[0]) < 0.5 and abs(a["riyadh"][1] - want[1]) < 0.5, a["riyadh"], list(want)),
        check("Riyadh's pixel holds the Saudi fill #22d3ee", np.abs(np.array(a["rgb"]) - [0x22, 0xd3, 0xee]).max() <= 3, a["rgb"], [0x22, 0xd3, 0xee]),
        check("fadeDuration 0, interactive false", a["opts"] == {"fade": 0, "interactive": False}, a["opts"], {"fade": 0, "interactive": False}),
        check("negative control: another camera gives another frame", c["h"] != a["h"], [a["h"], c["h"]], "different"),
    ], [wd / "map_a.png", wd / "map13_measure.json"]


@card("MAP-15")
def bake_basemap(task, wd):
    """Bakes only the basemap to MP4: zoom ZSTART 2.4 -> ZEND 3.4 with easeInOutCubic then hold, every frame waited on map
    idle, encoded all-intra (-g 1) so seeking is exact; exports each country's projected border as SVG coords JSON
    (Saudi Arabia:#22d3ee, Egypt:#f59e0b) for a draw-on overlay. FPS 30, DUR 1 s here (a short bake)."""
    js = """
const fc = await world();
const style = {version: 8, sources: {w: {type: 'geojson', data: fc}}, layers: [
  {id: 'bg', type: 'background', paint: {'background-color': '#05070c'}}, {id: 'land', type: 'fill', source: 'w', paint: {'fill-color': '#1f2733'}}]};
const map = mk(style, {center: [38, 24], zoom: 2.4}); await new Promise(r => map.once('load', r));
const FPS = 30, DUR = 1, Z0 = 2.4, Z1 = 3.4, MOVE = 0.7, frames = [], zooms = [];
const ease = t => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
for (let i = 0; i < FPS * DUR; i++) { const t = i / FPS, u = Math.min(1, t / MOVE), z = Z0 + (Z1 - Z0) * ease(u);
  map.jumpTo({zoom: z}); await idle(map); zooms.push(map.getZoom()); frames.push(map.getCanvas().toDataURL('image/png')); }
const coords = {};
for (const [name, col] of [['Saudi Arabia', '#22d3ee'], ['Egypt', '#f59e0b']]) { const f = fc.features.find(x => x.properties.name === name);
  const rings = f.geometry.type === 'Polygon' ? [f.geometry.coordinates[0]] : f.geometry.coordinates.map(p => p[0]);
  coords[name] = {color: col, rings: rings.map(r => r.map(([lo, la]) => { const p = map.project([lo, la]); return [+p.x.toFixed(2), +p.y.toFixed(2)]; })), lnglat: rings[0].slice(0, 3)}; }
window.__result = {frames, zooms, coords, center: map.getCenter().toArray(), zoom: map.getZoom()}; window.__done = true;
"""
    r = pw(wd, "bake.html", [{"js": "window.__result"}], w=320, h=180, html=map_page(320, 180, js), timeout=40)[0]
    fdir = wd / "bake_frames"
    fdir.mkdir(exist_ok=True)
    for i, u in enumerate(r["frames"]):
        data_url_to_png(u, fdir / ("f_%03d.png" % i))
    film = wd / "basemap.mp4"
    fx.ffmpeg("-framerate", "30", "-i", fdir / "f_%03d.png", "-c:v", "libx264", "-g", "1", "-crf", "17", "-pix_fmt", "yuv420p", film)
    gop = wd / "gop_default.mp4"
    fx.ffmpeg("-framerate", "30", "-i", fdir / "f_%03d.png", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", gop)
    types = lambda p: run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "frame=pict_type", "-of", "csv=p=0", p]).stdout.replace(",", " ").split()
    tf, tg = types(film), types(gop)
    shutil.rmtree(fdir)
    cj = jw(wd / "basemap-coords.json", {k: {"color": v["color"], "rings": v["rings"]} for k, v in r["coords"].items()})
    ease = lambda t: 4 * t ** 3 if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2
    want = [2.4 + ease(min(1, i / 30 / 0.7)) for i in range(30)]
    zerr = max(abs(a - b) for a, b in zip(r["zooms"], want))
    lo, la = r["coords"]["Saudi Arabia"]["lnglat"][0]
    px_, py_ = merc(lo, la, r["zoom"])
    cx_, cy_ = merc(r["center"][0], r["center"][1], r["zoom"])
    first = r["coords"]["Saudi Arabia"]["rings"][0][0]
    perr = math.hypot(first[0] - (160 + px_ - cx_), first[1] - (90 + py_ - cy_))
    return [
        check("30 frames baked (FPS 30 x DUR 1)", len(tf) == 30, len(tf), 30),
        check("all-intra encode: every frame is an I-frame (-g 1)", set(tf) == {"I"}, sorted(set(tf)), ["I"]),
        check("zoom per frame follows 2.4 -> 3.4 easeInOutCubic, then holds", zerr < 1e-6 and abs(r["zooms"][-1] - 3.4) < 1e-9, zerr, "< 1e-6"),
        check("exported border coords are the map's own projection (web mercator check < 0.05 px)", perr < 0.05, perr, "< 0.05 px"),
        check("both countries exported with their colours", sorted(r["coords"]) == ["Egypt", "Saudi Arabia"] and r["coords"]["Egypt"]["color"] == "#f59e0b", sorted(r["coords"]), ["Egypt", "Saudi Arabia"]),
        check("negative control: a default-GOP encode of the same frames has P/B frames (not exactly seekable)", set(tg) != {"I"}, sorted(set(tg)), "contains P/B"),
    ], [film, cj]


@card("MAP-16")
def globe_and_extrusion(task, wd):
    """Nicer defaults: projection 'globe' at low zoom (the planet as a sphere with space around it) and fill-extrusion for
    buildings at pitch 45-60 deg, both under the MAP-13 deterministic rules (jumpTo + idle). Mercator is the control."""
    js = """
const fc = await world();
const blocks = {type: 'FeatureCollection', features: [0, 1, 2].map(i => ({type: 'Feature', properties: {h: 40 + 60 * i},
  geometry: {type: 'Polygon', coordinates: [[[46.70 + i * 0.004, 24.70], [46.703 + i * 0.004, 24.70], [46.703 + i * 0.004, 24.703], [46.70 + i * 0.004, 24.703], [46.70 + i * 0.004, 24.70]]]}}))};
async function shot(proj, o, extr) {
  const style = {version: 8, projection: {type: proj}, sources: {w: {type: 'geojson', data: fc}, b: {type: 'geojson', data: blocks}}, layers: [
    {id: 'bg', type: 'background', paint: {'background-color': '#0e3a5c'}}, {id: 'land', type: 'fill', source: 'w', paint: {'fill-color': '#3a6b3a'}},
    {id: 'bld', type: 'fill-extrusion', source: 'b', paint: {'fill-extrusion-color': '#ff4040', 'fill-extrusion-height': extr ? ['get', 'h'] : 0, 'fill-extrusion-opacity': 1}}]};
  const map = mk(style, o); await new Promise(r => map.once('load', r)); map.jumpTo(o); await idle(map);
  const u = map.getCanvas().toDataURL('image/png'); const corner = px(map, 2, 2), mid = px(map, 160, 90); map.remove(); return {png: u, corner, mid}; }
window.__result = {globe: await shot('globe', {center: [40, 20], zoom: 0.3}), merc: await shot('mercator', {center: [40, 20], zoom: 0.3}),
  tall: await shot('mercator', {center: [46.704, 24.7015], zoom: 14.2, pitch: 55, bearing: 20}, true), flat: await shot('mercator', {center: [46.704, 24.7015], zoom: 14.2, pitch: 55, bearing: 20}, false)};
window.__done = true;
"""
    r = pw(wd, "globe.html", [{"js": "window.__result"}], w=320, h=180, html=map_page(320, 180, js), timeout=40)[0]
    for k in r:
        data_url_to_png(r[k].pop("png"), wd / ("m16_%s.png" % k))
    g, m, t, f = (png_arr(wd / ("m16_%s.png" % k)) for k in ("globe", "merc", "tall", "flat"))
    ocean = np.array([0x0e, 0x3a, 0x5c])
    off_globe = float((np.abs(g - ocean).sum(-1) > 40)[:, :40].mean())
    off_merc = float((np.abs(m - ocean).sum(-1) > 40)[:, :40].mean() - ((np.abs(m - [0x3a, 0x6b, 0x3a]).sum(-1) < 40)[:, :40]).mean())
    red = lambda a: float(((a[..., 0] > 150) & (a[..., 1] < 110)).mean())
    jw(wd / "globe_measure.json", {"globe_offsphere_frac": off_globe, "merc_offmap_frac": off_merc, "extrusion_red": [red(t), red(f)], "corner": [r["globe"]["corner"], r["merc"]["corner"]]})
    return [
        check("globe at zoom .3: the canvas edge is outside the sphere (not ocean)", off_globe > 0.5, off_globe, "> 0.5"),
        check("negative control: mercator at the same camera fills the edge with map", off_merc < 0.2, off_merc, "< 0.2"),
        check("fill-extrusion at pitch 55 shows the extruded walls (more red than the flat footprints)", red(t) > 1.5 * red(f) and red(t) > 0.02, [red(t), red(f)], "tall > 1.5 x flat"),
    ], [wd / "m16_globe.png", wd / "m16_tall.png", wd / "globe_measure.json"]


@card("MAP-17")
def paint_only_layers(task, wd):
    """Draw and tint over the provider's own layers: filter exact layers (waterway, boundary, transportation) and animate
    only paint (opacity, colour, width) with setPaintProperty. A local vector-like GeoJSON with a 'class' property stands in
    for the provider tiles (MapTiler needs a key); the river layer fades 0 -> 1 while roads stay untouched."""
    js = """
const L = (cls, pts) => ({type: 'Feature', properties: {class: cls}, geometry: {type: 'LineString', coordinates: pts}});
const fc = {type: 'FeatureCollection', features: [L('waterway', [[30.0, 29.0], [31.0, 30.0], [31.2, 31.4]]), L('transportation', [[29.5, 30.6], [32.5, 30.6]]),
  L('boundary', [[29.2, 29.4], [29.2, 31.6]])]};
const style = {version: 8, sources: {p: {type: 'geojson', data: fc}}, layers: [{id: 'bg', type: 'background', paint: {'background-color': '#111'}},
  {id: 'road', type: 'line', source: 'p', filter: ['==', ['get', 'class'], 'transportation'], paint: {'line-color': '#999999', 'line-width': 3}},
  {id: 'river', type: 'line', source: 'p', filter: ['==', ['get', 'class'], 'waterway'], paint: {'line-color': '#38bdf8', 'line-width': 4, 'line-opacity': 0}},
  {id: 'border', type: 'line', source: 'p', filter: ['==', ['get', 'class'], 'boundary'], paint: {'line-color': '#f59e0b', 'line-width': 2}}]};
const map = mk(style, {center: [30.8, 30.2], zoom: 5.4}); await new Promise(r => map.once('load', r)); await idle(map);
const out = [];
for (const op of [0, 0.5, 1]) { map.setPaintProperty('river', 'line-opacity', op); map.setPaintProperty('border', 'line-color', op < 1 ? '#f59e0b' : '#ef4444');
  await idle(map); const rp = map.project([30.5, 29.5]), qp = map.project([29.8, 30.6]), bp = map.project([29.2, 30.0]);
  out.push({op, river: [rp.x, rp.y], road: [qp.x, qp.y], border: [bp.x, bp.y],
    png: map.getCanvas().toDataURL('image/png'), layers: map.getStyle().layers.map(l => l.id)}); }
window.__result = out; window.__done = true;
"""
    r = pw(wd, "paint.html", [{"js": "window.__result"}], w=320, h=180, html=map_page(320, 180, js), timeout=30)[0]
    for i, s_ in enumerate(r):
        data_url_to_png(s_.pop("png"), wd / ("paint_%d.png" % i))
        im = png_arr(wd / ("paint_%d.png" % i))
        for k in ("river", "road", "border"):
            x, y = s_[k]
            s_[k] = im[int(round(y)) - 1:int(round(y)) + 2, int(round(x)) - 1:int(round(x)) + 2].reshape(-1, 3).max(0).astype(int).tolist() if k != "river" else \
                im[int(round(y)), int(round(x))].astype(int).tolist()
    riv = [np.array(s_["river"], float) for s_ in r]
    bgc = np.array([0x11] * 3, float)
    blue = np.array([0x38, 0xbd, 0xf8], float)
    alpha = [float(((v - bgc) / (blue - bgc)).mean()) for v in riv]
    road = [tuple(s_["road"]) for s_ in r]
    jw(wd / "paint_measure.json", {"river_alpha": alpha, "road": road, "border": [s_["border"] for s_ in r]})
    return [
        check("river opacity animates 0 -> .5 -> 1 on the picture", abs(alpha[0]) < 0.03 and abs(alpha[1] - 0.5) < 0.06 and abs(alpha[2] - 1) < 0.03, alpha, [0, 0.5, 1]),
        check("border colour re-tinted by paint only (#f59e0b -> #ef4444)", np.abs(np.array(r[0]["border"]) - [0xf5, 0x9e, 0x0b]).max() < 30 and np.abs(np.array(r[2]["border"]) - [0xef, 0x44, 0x44]).max() < 30,
              [r[0]["border"], r[2]["border"]], ["#f59e0b", "#ef4444"]),
        check("no layer added or removed (paint-only animation)", all(s_["layers"] == ["bg", "road", "river", "border"] for s_ in r), r[0]["layers"], ["bg", "road", "river", "border"]),
        check("negative control: the untouched road layer is identical in every frame", len(set(road)) == 1 and road[0] != (0x11, 0x11, 0x11), road, "constant grey"),
    ], [wd / "paint_1.png", wd / "paint_measure.json"]


def _haversine(a, b):
    R = 6371.0088
    la1, lo1, la2, lo2 = map(math.radians, (a[1], a[0], b[1], b[0]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def _bearing(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[1], a[0], b[1], b[0]))
    y = math.sin(lo2 - lo1) * math.cos(la2)
    x = math.cos(la1) * math.sin(la2) - math.sin(la1) * math.cos(la2) * math.cos(lo2 - lo1)
    return (math.degrees(math.atan2(y, x)) + 360) % 360


@card("MAP-18")
def flight_corridor(task, wd):
    """Cinematic flight: the camera follows a pre-smoothed corridor (Chaikin smoothing, resampled every 0.1 km) at constant
    height; heading from the path tangent, small banking from curvature. The raw waypoint polyline is the control: its
    heading snaps at every vertex."""
    raw = [(39.80, 21.40), (39.86, 21.44), (39.83, 21.50), (39.90, 21.55), (39.97, 21.52)]
    pts = np.array(raw)
    for _ in range(5):
        q = []
        for a, b in zip(pts[:-1], pts[1:]):
            q += [0.75 * a + 0.25 * b, 0.25 * a + 0.75 * b]
        pts = np.vstack([pts[0], q, pts[-1]])
    seg = [_haversine(a, b) for a, b in zip(pts[:-1], pts[1:])]
    s = np.concatenate([[0], np.cumsum(seg)])
    n = int(s[-1] / 0.1)
    samp = np.array([[np.interp(d, s, pts[:, 0]), np.interp(d, s, pts[:, 1])] for d in np.arange(n + 1) * 0.1])
    heading = [_bearing(a, b) for a, b in zip(samp[:-1], samp[1:])]
    dh = [((b - a + 180) % 360) - 180 for a, b in zip(heading[:-1], heading[1:])]
    bank = [max(-12, min(12, 25 * d)) for d in dh]
    height = [450.0] * len(samp)
    raw_h = [_bearing(a, b) for a, b in zip(raw[:-1], raw[1:])]
    raw_dh = [((b - a + 180) % 360) - 180 for a, b in zip(raw_h[:-1], raw_h[1:])]
    spacing = [_haversine(a, b) for a, b in zip(samp[:-1], samp[1:])]
    keys = [{"t": round(i / 30, 4), "lng": float(p[0]), "lat": float(p[1]), "alt_m": height[i], "heading": float(heading[min(i, len(heading) - 1)]),
             "bank": float(bank[min(i, len(bank) - 1)])} for i, p in enumerate(samp)]
    path = jw(wd / "flight-path.json", keys)
    im = Image.new("RGB", (480, 360), (12, 16, 24))
    d = ImageDraw.Draw(im)
    lo0, lo1, la0, la1 = 39.78, 40.0, 21.38, 21.57
    P = lambda p: ((p[0] - lo0) / (lo1 - lo0) * 480, 360 - (p[1] - la0) / (la1 - la0) * 360)
    d.line([P(p) for p in raw], fill=(120, 60, 60), width=1)
    d.line([P(p) for p in samp], fill=(56, 189, 248), width=2)
    im.save(wd / "corridor.png")
    worst_turn = max(abs(x) for x in dh)
    sgn_ok = all((b > 0) == (h > 0) for b, h in zip(bank, dh) if abs(h) > 0.05)
    return [
        check("samples every 0.1 km along the smoothed corridor", max(abs(x - 0.1) for x in spacing[:-1]) < 0.002, [min(spacing[:-1]), max(spacing[:-1])], 0.1),
        check("constant camera height", len(set(height)) == 1, height[0], 450),
        check("heading = bearing of the path tangent; it never snaps (max turn per 0.1 km <= 8 deg)", worst_turn <= 8, worst_turn, "<= 8 deg"),
        check("bank leans into each turn (same sign as the curvature), capped at 12 deg", sgn_ok and max(map(abs, bank)) <= 12, [min(bank), max(bank)], "|bank| <= 12"),
        check("negative control: the raw waypoint polyline snaps its heading at a vertex by > 30 deg", max(abs(x) for x in raw_dh) > 30, raw_dh, "> 30 deg"),
    ], [path, wd / "corridor.png"]


@card("MAP-20")
def versatiles_styles(task, wd):
    """Free MapLibre style generators (@versatiles/style 8.1.1, MIT, installed globally): osm({theme, text: {language}})
    replaces the v5 palette builders the card lists (colorful, eclipse/dark, graybeard/gray, neutrino, shadow); each style
    takes a language (ar) and SDF glyphs {fontstack}/{range}.pbf. Tiles are not fetched (tiles.versatiles.org not probed)."""
    js = """
import * as S from '%s';
const out = {};
for (const th of ['colorful', 'colorful-dark', 'gray', 'muted', 'natural', 'toner']) { const st = S.osm({theme: th, text: {language: 'ar'}});
  const sym = st.layers.filter(l => l.type === 'symbol' && l.layout && l.layout['text-field']);
  out[th] = {version: st.version, glyphs: st.glyphs, nlayers: st.layers.length, ids_unique: new Set(st.layers.map(l => l.id)).size === st.layers.length,
    tf: sym.map(l => JSON.stringify(l.layout['text-field'])), bg: (st.layers.find(l => l.type === 'background') || {paint: {}}).paint['background-color'], sources: Object.keys(st.sources)}; }
const local = S.osm({theme: 'colorful'}); out.local_tf = local.layers.filter(l => l.type === 'symbol' && l.layout && l.layout['text-field']).map(l => JSON.stringify(l.layout['text-field']));
let bad = null; try { S.osm({theme: 'colorful', language: 'ar'}); } catch (e) { bad = e.message.split('\\n')[0]; }
out.v5_option = bad;
console.log(JSON.stringify(out));
""" % (NM / "@versatiles/style/dist/index.js")
    src = wd / "gen.mjs"
    src.write_text(js)
    res = json.loads(run([_NODE, src], cwd=str(wd), env=_node_env(wd)).stdout)
    for th in ("colorful", "colorful-dark"):
        pass
    gen = jw(wd / "styles_ar.json", res)
    ar = [t for th in ("colorful", "gray", "muted", "natural", "toner", "colorful-dark") for t in res[th]["tf"] if '"name' in t]
    return [
        check("six themes generated as MapLibre v8 styles with unique layer ids", all(res[t]["version"] == 8 and res[t]["ids_unique"] and res[t]["nlayers"] > 100 for t in ("colorful", "colorful-dark", "gray", "muted", "natural", "toner")),
              {t: res[t]["nlayers"] for t in ("colorful", "gray")}, "v8, > 100 layers"),
        check("language ar: every name label reads name_ar with a fallback to name", len(ar) > 20 and all("name_ar" in t for t in ar), [len(ar), ar[0]], '["coalesce",["get","name_ar"],["get","name"]]'),
        check("SDF glyph template {fontstack}/{range}.pbf", all(res[t]["glyphs"].endswith("/{fontstack}/{range}.pbf") for t in ("colorful", "gray")), res["colorful"]["glyphs"], ".../{fontstack}/{range}.pbf"),
        check("the dark theme really is dark", res["colorful-dark"]["bg"] != res["colorful"]["bg"] and int(re.findall(r"\d+", res["colorful-dark"]["bg"])[0]) < 80, [res["colorful"]["bg"], res["colorful-dark"]["bg"]], "dark < 80"),
        check("the v5 option name is refused with the v6+ replacement", res["v5_option"] is not None and "text.language" in res["v5_option"], res["v5_option"], "text.language"),
        check("negative control: without the language option labels are local names only", all("name_ar" not in t for t in res["local_tf"]) and any('"name"' in t for t in res["local_tf"]), [t for t in res["local_tf"] if '"name' in t][:1], '["get","name"]'),
    ], [gen]


@card("MAP-21")
def html_arabic_labels(task, wd):
    """MapLibre needs SDF glyph PBFs and the RTL plugin for Arabic; the safer video default hides provider labels and draws
    Arabic names as an HTML overlay that shares the map transform (map.project on every frame): full shaping, any font.
    The overlay is re-placed after each jumpTo; labels left where they were are the control."""
    js = """
const fc = await world();
const style = {version: 8, sources: {w: {type: 'geojson', data: fc}}, layers: [{id: 'bg', type: 'background', paint: {'background-color': '#0b1d33'}},
  {id: 'land', type: 'fill', source: 'w', paint: {'fill-color': '#243447'}}]};
const map = mk(style, {center: [40, 26], zoom: 3}); await new Promise(r => map.once('load', r));
const cities = [['الرياض', 46.72, 24.69], ['القاهرة', 31.24, 30.04], ['عمّان', 35.93, 31.95]];
const ov = document.getElementById('ov'); const els = cities.map(([n]) => { const d = document.createElement('div'); d.className = 'lbl'; d.textContent = n; ov.appendChild(d); return d; });
function place() { cities.forEach(([n, lo, la], i) => { const p = map.project([lo, la]); els[i].style.left = p.x + 'px'; els[i].style.top = p.y + 'px'; }); }
async function at(cam, move) { map.jumpTo(cam); await idle(map); if (move) place(); await document.fonts.ready;
  return cities.map(([n, lo, la], i) => { const r = els[i].getBoundingClientRect(), p = map.project([lo, la]); return {dx: (r.left + r.right) / 2 - p.x, dy: (r.top + r.bottom) / 2 - p.y, w: r.width}; }); }
const symbols = map.getStyle().layers.filter(l => l.type === 'symbol').length;
const a = await at({center: [40, 26], zoom: 3}, true);
const b = await at({center: [36, 29], zoom: 4.2, bearing: 15}, true);
const stale = await at({center: [42, 24], zoom: 3.6}, false);
window.__result = {a, b, stale, symbols, font: document.fonts.check('700 14px Cairo')}; window.__done = true;
"""
    r = pw(wd, "labels.html", [{"js": "window.__result", "shot": "labels.png"}], w=480, h=270, html=map_page(480, 270, js), timeout=30)[0]
    err = lambda L: max(math.hypot(x["dx"], x["dy"]) for x in L)
    rep = jw(wd / "labels_measure.json", r)
    return [
        check("no symbol layers in the style (provider labels hidden, no glyph PBFs needed)", r["symbols"] == 0, r["symbols"], 0),
        check("Arabic labels sit on their projected points (< 0.5 px)", err(r["a"]) < 0.5, err(r["a"]), "< 0.5 px"),
        check("after a new camera (zoom, bearing) they follow the transform (< 0.5 px)", err(r["b"]) < 0.5, err(r["b"]), "< 0.5 px"),
        check("labels drawn with the Cairo webfont (shaped HTML text)", r["font"] is True and min(x["w"] for x in r["a"]) > 20, [r["font"], [round(x["w"]) for x in r["a"]]], True),
        check("negative control: labels not re-placed after the camera move are off target", err(r["stale"]) > 20, err(r["stale"]), "> 20 px"),
    ], [wd / "labels.png", rep]


def _duck():
    import duckdb
    if SPATIAL_EXT is None:
        raise RuntimeError("duckdb spatial extension wheel not installed")
    c = duckdb.connect()
    c.sql("LOAD '%s'" % SPATIAL_EXT)
    return c


def _cities_fixture(wd):
    cities = [("Riyadh", 46.72, 24.69), ("Jeddah", 39.17, 21.54), ("Mecca", 39.83, 21.42), ("Cairo", 31.24, 30.04),
              ("Alexandria", 29.92, 31.20), ("Amman", 35.93, 31.95), ("Dubai", 55.27, 25.20), ("Doha", 51.53, 25.29)]
    fc = {"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"name": n, "id": i},
                                                     "geometry": {"type": "Point", "coordinates": [lo, la]}} for i, (n, lo, la) in enumerate(cities)]}
    p = wd / "cities.geojson"
    p.write_text(json.dumps(fc))
    poly = {"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"name": "KSA box"},
                                                        "geometry": {"type": "Polygon", "coordinates": [[[36.0, 16.0], [50.5, 16.0], [50.5, 29.5], [36.0, 29.5], [36.0, 16.0]]]}}]}
    q = wd / "ksa_box.geojson"
    q.write_text(json.dumps(poly))
    return cities, p, q


@card("MAP-25")
def geo_to_pmtiles_parquet(task, wd):
    """Any geo file -> ogr2ogr -t_srs EPSG:4326 normalised GeoJSON -> tippecanoe -zg --drop-densest-as-needed -> .pmtiles
    (a serverless tile archive), plus DuckDB GeoParquet with a bbox struct and Hilbert ordering. The fixture arrives in
    EPSG:3857 metres; the untreated file is the control (not lon/lat)."""
    cities, _, _ = _cities_fixture(wd)
    R = 6378137.0
    fc = {"type": "FeatureCollection", "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::3857"}},
          "features": [{"type": "Feature", "properties": {"name": n}, "geometry": {"type": "Point", "coordinates": [math.radians(lo) * R, math.log(math.tan(math.pi / 4 + math.radians(la) / 2)) * R]}}
                       for n, lo, la in cities]}
    src = wd / "cities_3857.geojson"
    src.write_text(json.dumps(fc))
    norm = wd / "cities_4326.geojson"
    run(["ogr2ogr", "-f", "GeoJSON", "-t_srs", "EPSG:4326", "-lco", "COORDINATE_PRECISION=6", norm, src], timeout=60)
    g = json.loads(norm.read_text())
    got = {f["properties"]["name"]: f["geometry"]["coordinates"] for f in g["features"]}
    err = max(math.hypot(got[n][0] - lo, got[n][1] - la) for n, lo, la in cities)
    pm = wd / "cities.pmtiles"
    run(["tippecanoe", "-zg", "--drop-densest-as-needed", "-f", "-q", "-l", "cities", "-o", pm, norm], timeout=60, env=dict(os.environ, TMPDIR=str(wd)))
    head = pm.read_bytes()[:127]
    magic, ver = head[:7], head[7]
    n_tiles = struct.unpack("<Q", head[80:88])[0] if len(head) >= 88 else 0     # addressed tiles count (v3 header)
    minz, maxz = head[100], head[101]
    info = run(["ogrinfo", "-ro", "-so", "-al", pm], timeout=30).stdout
    c = _duck()
    pq = wd / "cities.parquet"
    c.sql("""COPY (SELECT name, geom, {'xmin': ST_XMin(geom), 'ymin': ST_YMin(geom), 'xmax': ST_XMax(geom), 'ymax': ST_YMax(geom)} AS bbox
              FROM ST_Read('%s') ORDER BY ST_Hilbert(geom, ST_Extent(ST_MakeEnvelope(-180, -90, 180, 90)))) TO '%s' (FORMAT PARQUET)""" % (norm, pq))
    order = [r[0] for r in c.sql("SELECT name FROM '%s'" % pq).fetchall()]
    kv = c.sql("SELECT key::VARCHAR FROM parquet_kv_metadata('%s')" % pq).fetchall()
    bbox = c.sql("SELECT bbox.xmin, bbox.ymin FROM '%s' WHERE name = 'Riyadh'" % pq).fetchall()[0]
    raw = json.loads(src.read_text())["features"][0]["geometry"]["coordinates"]
    rep = jw(wd / "pipeline_report.json", {"reproj_err_deg": err, "pmtiles": {"magic": magic.decode(errors="replace"), "version": ver, "tiles": n_tiles, "minzoom": minz, "maxzoom": maxz},
                                           "hilbert_order": order, "parquet_kv": [k[0] for k in kv], "riyadh_bbox": list(bbox)})
    return [
        check("ogr2ogr reprojects 3857 metres back to lon/lat (< 1e-5 deg)", err < 1e-5, err, "< 1e-5"),
        check("tippecanoe wrote a PMTiles v3 archive", magic == b"PMTiles" and ver == 3, [magic.decode(errors="replace"), ver], ["PMTiles", 3]),
        check("archive holds tiles and GDAL reads the 'cities' layer with 8 features", n_tiles > 0 and "Feature Count: 8" in info, [n_tiles, "Feature Count: 8" in info], [">0", True]),
        check("GeoParquet: geometry metadata written ('geo' key) and bbox struct per row", any(k[0] == "geo" for k in kv) and abs(bbox[0] - 46.72) < 1e-6, [[k[0] for k in kv], list(bbox)], ["geo", [46.72, 24.69]]),
        check("rows stored in Hilbert order (not the input order)", order != [n for n, _, _ in cities] and sorted(order) == sorted(n for n, _, _ in cities), order, "a permutation"),
        check("negative control: the untreated input is in metres, not degrees", abs(raw[0]) > 1e6, raw, "> 1e6 m"),
    ], [pm, pq, rep]


@card("MAP-26")
def duckdb_spatial_sql(task, wd):
    """SQL over geo files before the map film: LOAD spatial; SET geometry_always_xy=true; ST_Point(lon, lat) (longitude
    first); real metres with ST_Distance_Spheroid on POINT_2D; ST_Contains for point-in-polygon; export with COPY ...
    (FORMAT GDAL, DRIVER 'GeoJSON'). Distances are cross-checked with pyproj's WGS84 geodesic."""
    cities, cp, bp = _cities_fixture(wd)
    c = _duck()
    c.sql("SET geometry_always_xy = true")
    c.sql("CREATE TABLE city AS SELECT * FROM ST_Read('%s')" % cp)
    c.sql("CREATE TABLE box AS SELECT * FROM ST_Read('%s')" % bp)
    d = c.sql("""SELECT a.name, b.name, ST_Distance_Spheroid(ST_Point(ST_X(a.geom), ST_Y(a.geom))::POINT_2D, ST_Point(ST_X(b.geom), ST_Y(b.geom))::POINT_2D)
                 FROM city a, city b WHERE a.name = 'Riyadh' AND b.name IN ('Cairo', 'Jeddah') ORDER BY b.name""").fetchall()
    inside = sorted(r[0] for r in c.sql("SELECT city.name FROM city, box WHERE ST_Contains(box.geom, city.geom)").fetchall())
    out = wd / "inside.geojson"
    c.sql("COPY (SELECT city.name, city.geom FROM city, box WHERE ST_Contains(box.geom, city.geom)) TO '%s' (FORMAT GDAL, DRIVER 'GeoJSON')" % out)
    from pyproj import Geod
    G = Geod(ellps="WGS84")
    ref = {n: G.inv(46.72, 24.69, lo, la)[2] for n, lo, la in cities}
    swapped = c.sql("SELECT ST_Distance_Spheroid(ST_Point(24.69, 46.72)::POINT_2D, ST_Point(30.04, 31.24)::POINT_2D)").fetchall()[0][0]
    c2 = _duck()
    try:
        c2.sql("SELECT ST_Distance_Spheroid(ST_Point(46.72, 24.69)::POINT_2D, ST_Point(31.24, 30.04)::POINT_2D)").fetchall()
        unset = "ran"
    except Exception as exc:
        unset = str(exc).split("\n")[0][:100]
    got = {r[1]: r[2] for r in d}
    exported = json.loads(out.read_text())
    rep = jw(wd / "sql_report.json", {"distances_m": got, "pyproj_m": {k: ref[k] for k in got}, "inside": inside, "swapped_m": swapped, "unset_axis": unset})
    return [
        check("Riyadh -> Cairo spheroid distance matches the WGS84 geodesic (< 1 m)", abs(got["Cairo"] - ref["Cairo"]) < 1, got["Cairo"], ref["Cairo"]),
        check("Riyadh -> Jeddah spheroid distance matches (< 1 m)", abs(got["Jeddah"] - ref["Jeddah"]) < 1, got["Jeddah"], ref["Jeddah"]),
        check("ST_Contains: only the Saudi cities fall in the KSA box", inside == ["Jeddah", "Mecca", "Riyadh"], inside, ["Jeddah", "Mecca", "Riyadh"]),
        check("COPY ... FORMAT GDAL wrote GeoJSON with those 3 features", len(exported["features"]) == 3, len(exported["features"]), 3),
        check("without geometry_always_xy the axis-sensitive call is refused", unset != "ran", unset, "error"),
        check("negative control: lat/lon swapped gives a wrong distance", abs(swapped - ref["Cairo"]) > 50000, swapped, "far from %d" % ref["Cairo"]),
    ], [out, rep]


def _hf_shot_page(d, comp, name):
    """copy an installed HyperFrames composition next to its assets so relative asset paths resolve"""
    src = d / "compositions" / comp
    dst = d / name
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    return "hf/" + name


@card("MAP-41")
def hf_city_flight(task, wd):
    """`hyperframes add nyc-paris-flight` (1920x1080, 6 s): swap assets/map-nyc-paris.png for your plate, then seek the
    block's paused GSAP timeline. The plane rides the route with offset-distance 0 -> 100 % (sine.inOut from 1.17 s over
    3.25 s), the Paris pulse expands, and the plane lands with a pop (scale 1.23 at 5.12 s)."""
    d, _ = _hf_add(wd, "nyc-paris-flight")
    plate = Image.new("RGB", (1920, 1080), (14, 40, 62))
    dr = ImageDraw.Draw(plate)
    dr.ellipse((200, 260, 900, 900), fill=(46, 82, 60))
    dr.ellipse((1150, 180, 1800, 760), fill=(52, 88, 64))
    plate.save(d / "assets/map-nyc-paris.png")
    page = _hf_shot_page(d, "nyc-paris-flight.html", "flight.html")
    meas = ("(() => { const tl = window.__timelines['nyc-paris-flight']; tl.seek(%s, false); const p = document.getElementById('plane');"
            "const r = p.getBoundingClientRect(), core = new DOMMatrix(getComputedStyle(document.getElementById('plane-core')).transform);"
            "const pulse = document.getElementById('paris-pulse'), pr = new DOMMatrix(getComputedStyle(pulse).transform);"
            "return {od: parseFloat(getComputedStyle(p).offsetDistance), cx: (r.left + r.right) / 2, cy: (r.top + r.bottom) / 2, core: Math.hypot(core.a, core.b),"
            "pulse: Math.hypot(pr.a, pr.b), pulse_op: +getComputedStyle(pulse).opacity, dur: tl.duration(),"
            "img: document.querySelector('.map-image').naturalWidth, src: document.querySelector('.map-image').currentSrc}; })()")
    times = [1.0, 1.17 + 3.25 / 2, 4.42, 5.12, 5.6]
    steps = [{"js": meas % t, "shot": "flight_%d.png" % int(t * 100) if t in (2.795, 4.42) else None} for t in times]
    r = pw(wd, "x.html", steps, w=1920, h=1080, url="http://k/w/" + page, wait="!!(window.__timelines && window.__timelines['nyc-paris-flight'])", timeout=40)
    a = dict(zip(["before", "mid", "end", "pop", "after"], r))
    shot = png_arr(wd / "flight_442.png")
    plate_hit = float((np.abs(shot[300:900:50, 250:850:50] - [46, 82, 60]).sum(-1) < 60).mean())
    jw(wd / "flight_measure.json", a | {"plate_hit": plate_hit})
    return [
        check("the swapped plate is the map the block shows", a["before"]["img"] == 1920 and plate_hit > 0.3, [a["before"]["img"], plate_hit], [1920, "> 0.3"]),
        check("before 1.17 s the plane waits at the route start (offset-distance 0 %)", a["before"]["od"] == 0, a["before"]["od"], 0),
        check("sine.inOut: at mid-flight the plane is at 50 %", abs(a["mid"]["od"] - 50) < 0.1, a["mid"]["od"], 50),
        check("arrives at 100 % by 4.42 s", abs(a["end"]["od"] - 100) < 1e-6, a["end"]["od"], 100),
        check("landing pop: plane core scaled 1.23 at 5.12 s, settled back to 1 after the elastic", abs(a["pop"]["core"] - 1.23) < 0.01 and abs(a["after"]["core"] - 1) < 0.01, [a["pop"]["core"], a["after"]["core"]], [1.23, 1]),
        check("Paris pulse expands to 1.5 and fades out", abs(a["after"]["pulse"] - 1.5) < 0.01 and a["after"]["pulse_op"] < 0.01, [a["after"]["pulse"], a["after"]["pulse_op"]], [1.5, 0]),
        check("negative control: the plane moved east between start and arrival", a["end"]["cx"] - a["before"]["cx"] > 600, [a["before"]["cx"], a["end"]["cx"]], "> 600 px east"),
    ], [wd / "flight_442.png", wd / "flight_measure.json"]


@card("MAP-47")
def hf_choropleth(task, wd):
    """`hyperframes add world-map` (14 s): D3 v7 + topojson-client + world-atlas countries-110m (served from the local
    node_modules), GSAP paused timeline: countries stagger in from the centre (each .02 s, from 1.0 s), legend at 4 s; the
    fill encodes GDP per capita on a 4-stop scale. Localised here: the timeline is seeked and Arab countries' fills read."""
    d, _ = _hf_add(wd, "world-map")
    page = _hf_shot_page(d, "world-map.html", "world.html")
    meas = ("(() => { const tl = window.__timelines['world-map']; tl.seek(%s, false); const ps = [...document.querySelectorAll('#world-map .country-path')];"
            "const op = ps.map(p => +getComputedStyle(p).opacity); const fill = c => { const e = document.querySelector('#world-map [data-country=\"' + c + '\"]'); return e ? e.getAttribute('fill') : null; };"
            "return {n: ps.length, shown: op.filter(o => o > 0.99).length, partial: op.filter(o => o > 0.01 && o < 0.99).length, none: op.filter(o => o <= 0.01).length,"
            "legend: +getComputedStyle(document.querySelector('#world-map .legend-group')).opacity, ksa: fill('682'), egy: fill('818'), che: fill('756'), nodata: fill('012')}; })()")
    times = [0.9, 1.0 + 0.02 * 40 + 0.3, 3.95, 4.8]
    steps = [{"js": meas % t, "shot": "world_%d.png" % int(t * 100) if t == 4.8 else None} for t in times]
    r = pw(wd, "x.html", steps, w=1920, h=1080, url="http://k/w/" + page, wait="!!(window.__timelines && window.__timelines['world-map'])", timeout=40)
    b, mid, end, leg = r
    # the block's own scale: t = (gdp - min) / (max - min) over 4 stops
    gmin, gmax = 1621, 105669
    def colour(v):
        stops = [(6, 78, 59), (13, 148, 136), (34, 211, 238), (240, 253, 250)]
        t = max(0, min(1, (v - gmin) / (gmax - gmin))) * 3
        i = min(int(t), 2)
        lt = t - i
        return "rgb(%d,%d,%d)" % tuple(round(stops[i][k] + (stops[i + 1][k] - stops[i][k]) * lt) for k in range(3))
    jw(wd / "world_measure.json", {"t": times, "frames": r})
    return [
        check("177 countries drawn from world-atlas 110m by D3", b["n"] == 177, b["n"], 177),
        check("staggered reveal: mid-way some countries are shown, some still hidden", mid["shown"] > 10 and mid["none"] > 10, [mid["shown"], mid["partial"], mid["none"]], "some shown, some hidden"),
        check("all countries revealed by the legend beat (4.8 s)", leg["shown"] == b["n"] and end["shown"] > mid["shown"], [mid["shown"], end["shown"], leg["shown"]], b["n"]),
        check("Saudi Arabia (32,270) and Egypt (4,295) carry the block's GDP colours", b["ksa"] == colour(32270) and b["egy"] == colour(4295), [b["ksa"], b["egy"]], [colour(32270), colour(4295)]),
        check("legend fades in after 4 s", end["legend"] < 0.05 and leg["legend"] > 0.95, [end["legend"], leg["legend"]], [0, 1]),
        check("negative control: before 1.0 s no country is visible", b["shown"] == 0 and b["partial"] == 0, [b["shown"], b["partial"]], [0, 0]),
    ], [wd / "world_480.png", wd / "world_measure.json"]


@card("MAP-51")
def hf_country_zoom(task, wd):
    """`hyperframes add north-korea-locked-down` (7 s): the raster plate zooms in (camera scale .92 -> 2.12, expo.inOut over
    3.18 s, then back.out to 2.2), a hand-jittered scribble ellipse draws on with dashoffset (~.6 s) after the zoom settles,
    a pop-up label and a red multiply-style wash. Seeked in Chrome; the wash is measured on the pixels."""
    d, _ = _hf_add(wd, "north-korea-locked-down")
    page = _hf_shot_page(d, "north-korea-locked-down.html", "korea.html")
    meas = ("(() => { const tl = window.__timelines['north-korea-locked-down']; tl.seek(%s, false); const cam = new DOMMatrix(getComputedStyle(document.getElementById('camera')).transform);"
            "const ca = document.getElementById('circle-a'); const len = ca.getTotalLength ? ca.getTotalLength() : 0;"
            "return {scale: Math.hypot(cam.a, cam.b), dash: parseFloat(getComputedStyle(ca).strokeDashoffset), len, label: +getComputedStyle(document.getElementById('label')).opacity,"
            "wash: +getComputedStyle(document.getElementById('redWash')).opacity}; })()")
    times = [0.0, 1.59, 3.18, 3.24, 3.86, 4.3]
    steps = [{"js": meas % t, "shot": "korea_%d.png" % int(t * 100) if t in (0.0, 4.3) else None} for t in times]
    r = pw(wd, "x.html", steps, w=1920, h=1080, url="http://k/w/" + page, wait="!!(window.__timelines && window.__timelines['north-korea-locked-down'])", timeout=40)
    a = dict(zip(times, r))
    s0, s1 = png_arr(wd / "korea_0.png"), png_arr(wd / "korea_430.png")
    redness = lambda im: float((im[..., 0] - (im[..., 1] + im[..., 2]) / 2).mean())
    jw(wd / "korea_measure.json", {"frames": a, "redness": [redness(s0), redness(s1)]})
    return [
        check("zoom: camera scale .92 at 0 s -> 2.12 at 3.18 s (expo.inOut half-way ~ midpoint)", abs(a[0.0]["scale"] - 0.92) < 1e-3 and abs(a[3.18]["scale"] - 2.12) < 1e-3 and abs(a[1.59]["scale"] - 1.52) < 0.02,
              [a[0.0]["scale"], a[1.59]["scale"], a[3.18]["scale"]], [0.92, 1.52, 2.12]),
        check("the scribble waits for the zoom (undrawn at 3.24 s) then draws on with dashoffset (0 by 3.86 s)", a[3.24]["dash"] == a[0.0]["dash"] > 100 and a[3.86]["dash"] < 1, [a[0.0]["dash"], a[3.24]["dash"], a[3.86]["dash"]], "undrawn -> 0"),
        check("label pops in and the red wash is on by 4.3 s", a[4.3]["label"] > 0.99 and a[4.3]["wash"] > 0.9, [a[4.3]["label"], a[4.3]["wash"]], [1, "> .9"]),
        check("the wash reddens the frame", redness(s1) > redness(s0) + 10, [redness(s0), redness(s1)], "redder"),
        check("negative control: at 0 s no label, no wash", a[0.0]["label"] == 0 and a[0.0]["wash"] == 0, [a[0.0]["label"], a[0.0]["wash"]], [0, 0]),
    ], [wd / "korea_430.png", wd / "korea_measure.json"]


@card("MAP-57")
def collage_geo_props(task, wd):
    """The vox-history profile's INVENTORY (fastify-motion-bro scripts/profiles/vox-history.mjs) places geography collage props
    (folded era map fragment, map inset, string crossing map, red string, hand-drawn timeline strip) into the clip prompts,
    rotating rows clip by clip. The planner is driven through its own start/respond flow."""
    mod = Path("/home/claude/fastify-motion-bro/scripts/profiles/vox-history.mjs")
    if not mod.exists():
        raise RuntimeError("fastify-motion-bro vox-history profile not found")
    js = wd / "plan.mjs"
    js.write_text("""import * as vox from %s;
let x = vox.respond(vox.start().state, '6'); x = vox.respond(x.state, 'Suez Canal opening 1869'); x = vox.respond(x.state, '6');
console.log(JSON.stringify({stage: x.state.stage, clips: x.state.values.clips.map(c => ({elements: c.elements, prompt: c.prompt, d: c.durationSeconds})), style: vox.STYLE}));
""" % json.dumps(str(mod)))
    res = json.loads(run([_NODE, js], cwd=str(wd), env=_node_env(wd)).stdout)
    geo = ["folded era map fragment", "map inset", "string crossing map", "red string segment", "hand-drawn timeline strip"]
    per = [[g for g in geo if g in " ".join(c["elements"]) or g in c["prompt"]] for c in res["clips"]]
    rows = [tuple(c["elements"]) for c in res["clips"]]
    plan = jw(wd / "vox_plan.json", res)
    topic = "Suez Canal opening 1869"
    return [
        check("6 clips of 10 s planned", len(res["clips"]) == 6 and all(c["d"] == 10 for c in res["clips"]), len(res["clips"]), 6),
        check("every clip carries at least one geography prop", all(per), [len(p) for p in per], ">= 1 each"),
        check("props rotate: consecutive clips use different inventory rows", all(a != b for a, b in zip(rows, rows[1:])), len(set(rows)), "> 1"),
        check("the style keeps red thread / brass tacks", "red thread" in res["style"] and "brass tacks" in res["style"], True, True),
        check("negative control: the bare topic text names no collage prop", not any(g in topic for g in geo), topic, "no props"),
    ], [plan]


# ================================================================================================ media (image / audio)
_OCR_LINES = ["العلم نور والجهل ظلام", "الخط العربي جميل وواضح", "Motion design in Arabic 2026"]


def _ocr_fixture(path, angle=0.0):
    im = Image.new("L", (1500, 420), 255)
    d = ImageDraw.Draw(im)
    fonts_ = [font(72, FONTS / "Amiri-Regular.ttf"), font(64, FONTS / "Cairo[slnt,wght].ttf"), font(60, FONTS / "Poppins-Regular.ttf")]
    for i, (t, f) in enumerate(zip(_OCR_LINES, fonts_)):
        if i < 2:
            d.text((1400, 40 + i * 125), t, font=f, fill=0, anchor="ra", direction="rtl", language="ar")
        else:
            d.text((100, 40 + i * 125), t, font=f, fill=0)
    if angle:
        im = im.rotate(angle, resample=Image.BICUBIC, expand=True, fillcolor=255)
    im.save(path, dpi=(300, 300))
    return Path(path)


def _tess(path, lang="ara+eng", psm=6):
    out = run(["tesseract", path, "stdout", "-l", lang, "--oem", "1", "--psm", str(psm)], timeout=60,
              env=dict(os.environ, OMP_THREAD_LIMIT="1")).stdout          # OpenMP threads make tesseract 100x slower in a container
    return nfkc(out)


@card("MEDIA-03")
def tesseract_arabic(task, wd):
    """tesseract 5 with the Arabic pack: image_to_string(img, lang='ara+eng', --oem 1 --psm 6) on clean naskh (Amiri), sans
    (Cairo) and English lines rendered at 300 dpi; U+200E/U+200F marks stripped; scored by difflib on NFKC text."""
    img = _ocr_fixture(wd / "lines.png")
    truth = " ".join(_OCR_LINES)
    t0 = time.time()
    got = _tess(img)
    dt = time.time() - t0
    eng_only = _tess(img, "eng")
    blank = wd / "blank.png"
    Image.new("L", (1500, 420), 255).save(blank)
    gb = _tess(blank)
    (wd / "ocr.txt").write_text(got, encoding="utf-8")
    sim = ratio(got, truth)
    ara = ratio(" ".join(got.split()[:8]), " ".join(_OCR_LINES[:2]))
    jw(wd / "ocr_report.json", {"text": got, "similarity": sim, "arabic_part": ara, "eng_only": ratio(eng_only, truth), "seconds": dt})
    return [
        check("ara+eng reads all three lines (similarity >= .9)", sim >= 0.9, sim, ">= 0.9"),
        check("the Arabic lines alone read >= .9", ara >= 0.9, ara, ">= 0.9"),
        check("no LRM/RLM marks left", "‎" not in got and "‏" not in got, True, True),
        check("negative control: the English-only model cannot read the Arabic (< .6)", ratio(eng_only, truth) < 0.6, ratio(eng_only, truth), "< 0.6"),
        check("negative control: a blank page reads nothing", gb == "", gb, ""),
    ], [wd / "ocr.txt", img, wd / "ocr_report.json"]


@card("MEDIA-06")
def ocr_preprocess_measured(task, wd):
    """Score each preprocessing variant against ground truth (difflib ratio on NFKC text): the 6-degree skewed scan, grayscale
    deskew (angle from the projection-profile maximum), and deskew + adaptiveThreshold(31, C=15). Binarise only if the
    measurement shows it helps: the pipeline keeps the best-scoring variant."""
    import cv2
    truth = " ".join(_OCR_LINES)
    skew = _ocr_fixture(wd / "skewed.png", angle=6.0)
    g = cv2.imread(str(skew), cv2.IMREAD_GRAYSCALE)

    def score_angle(a):
        M = cv2.getRotationMatrix2D((g.shape[1] / 2, g.shape[0] / 2), a, 1)
        r = cv2.warpAffine(255 - g, M, (g.shape[1], g.shape[0]))
        return float(np.var(r.sum(1)))
    angs = np.arange(-9, 9.01, 0.1)
    best = float(angs[int(np.argmax([score_angle(a) for a in angs]))])
    M = cv2.getRotationMatrix2D((g.shape[1] / 2, g.shape[0] / 2), best, 1)
    desk = cv2.warpAffine(g, M, (g.shape[1], g.shape[0]), flags=cv2.INTER_CUBIC, borderValue=255)
    cv2.imwrite(str(wd / "deskew.png"), desk)
    binz = cv2.adaptiveThreshold(desk, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 15)
    cv2.imwrite(str(wd / "deskew_bin.png"), binz)
    sc = {k: ratio(_tess(wd / f), truth) for k, f in (("skewed", "skewed.png"), ("deskew", "deskew.png"), ("deskew+adaptive", "deskew_bin.png"))}
    chosen = max(sc, key=sc.get)
    rep = jw(wd / "variants.json", {"scores": sc, "estimated_skew_deg": -best, "chosen": chosen, "binarise_helps": sc["deskew+adaptive"] > sc["deskew"]})
    return [
        check("skew estimated from the projection profile (true 6.0 deg, within 0.3)", abs(abs(best) - 6.0) <= 0.3, best, "+-6.0"),
        check("every variant scored against the ground truth", len(sc) == 3 and all(0 <= v <= 1 for v in sc.values()), sc, "3 scores"),
        check("deskew improves on the skewed scan", sc["deskew"] > sc["skewed"], [sc["skewed"], sc["deskew"]], "deskew > skewed"),
        check("the chosen variant is the measured best (binarise only if it helps)", sc[chosen] == max(sc.values()) and (chosen != "deskew+adaptive" or sc["deskew+adaptive"] > sc["deskew"]), chosen, "argmax"),
        check("negative control: the untreated skewed scan scores below the chosen variant", sc["skewed"] < sc[chosen], [sc["skewed"], sc[chosen]], "lower"),
    ], [rep, wd / "deskew.png"]


@card("MEDIA-12")
def imagemagick6(task, wd):
    """ImageMagick 6 (convert, not magick): convert in.png -resize 50% -colorspace Gray -unsharp 0x1 out.png; identify -format
    '%w %h %[colorspace]' out.png -> '750 235 Gray'. mogrify runs in place on a copy only."""
    src = wd / "in.png"
    a = np.zeros((470, 1500, 3), np.uint8)
    a[..., 0] = np.linspace(0, 255, 1500)[None, :]
    a[..., 2] = np.linspace(255, 0, 470)[:, None]
    a[200:270, 600:900] = 255
    Image.fromarray(a).save(src)
    out = wd / "out.png"
    ver = run(["convert", "-version"]).stdout.splitlines()[0]
    run(["convert", src, "-resize", "50%", "-colorspace", "Gray", "-unsharp", "0x1", out])
    idf = run(["identify", "-format", "%w %h %[colorspace]", out]).stdout.strip()
    idin = run(["identify", "-format", "%w %h %[colorspace]", src]).stdout.strip()
    cp = wd / "copy.png"
    shutil.copy(src, cp)
    run(["mogrify", "-resize", "25%", cp])
    idc = run(["identify", "-format", "%w %h", cp]).stdout.strip()
    o = np.asarray(Image.open(out).convert("RGB")).astype(int)
    edge = np.abs(np.diff(o[..., 0][100:135, 290:310].astype(float), axis=1)).max()
    return [
        check("ImageMagick 6 (convert) is the engine", "ImageMagick 6" in ver, ver[:40], "ImageMagick 6.x"),
        check("identify -> '750 235 Gray'", idf == "750 235 Gray", idf, "750 235 Gray"),
        check("grey pixels (R = G = B) after -colorspace Gray", int(np.abs(o[..., 0] - o[..., 1]).max()) == 0, int(np.abs(o[..., 0] - o[..., 1]).max()), 0),
        check("mogrify resized the copy in place (375 118), the source untouched", idc == "375 118" and sha(src) != sha(cp), idc, "375 118"),
        check("negative control: the untreated input is 1500 470 sRGB", idin == "1500 470 sRGB", idin, "1500 470 sRGB"),
    ], [out, cp]


@card("MEDIA-13")
def cairosvg_raster(task, wd):
    """cairosvg.svg2png(bytestring=svg, write_to='o.png', output_width=1024): an SVG (viewBox 200 x 100: red left half, a blue
    circle) rasterised at 1024 px wide keeps its aspect and geometry."""
    import cairosvg
    svg = b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 100"><rect width="200" height="100" fill="#ffffff"/><rect width="100" height="100" fill="#ff0000"/><circle cx="150" cy="50" r="25" fill="#0000ff"/></svg>'
    (wd / "in.svg").write_bytes(svg)
    out = wd / "o.png"
    cairosvg.svg2png(bytestring=svg, write_to=str(out), output_width=1024)
    im = Image.open(out)
    a = np.asarray(im.convert("RGB")).astype(int)
    blue = (a[..., 2] > 200) & (a[..., 0] < 50)
    ys, xs = np.where(blue)
    area = blue.sum()
    want_area = math.pi * (25 * 1024 / 200) ** 2
    return [
        check("1024 x 512 PNG (aspect kept)", im.size == (1024, 512) and out.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n", list(im.size), [1024, 512]),
        check("left half is the red rect", (np.abs(a[:, :500] - [255, 0, 0]).sum(-1) < 10).mean() > 0.99, float((np.abs(a[:, :500] - [255, 0, 0]).sum(-1) < 10).mean()), "> .99"),
        check("circle centred at (768, 256)", abs(xs.mean() - 768) < 1 and abs(ys.mean() - 256) < 1, [float(xs.mean()), float(ys.mean())], [768, 256]),
        check("circle area = pi (25 x 5.12)^2 within 2 %", abs(area / want_area - 1) < 0.02, int(area), int(want_area)),
        check("negative control: the untreated input is vector text, not pixels", svg[:4] == b"<svg" and not svg.startswith(b"\x89PNG"), svg[:4].decode(), "<svg"),
    ], [out]


@card("MEDIA-30")
def heic_open_convert(task, wd):
    """pillow-heif: register_heif_opener(); Image.open('x.heic') then convert. An iPhone-like HEIC is made from a fixture
    with the same library's HEVC encoder, opened back through Pillow and saved as PNG; PSNR against the source is measured.
    Pillow without the opener is the control (it cannot identify the file)."""
    import pillow_heif
    src = np.zeros((240, 320, 3), np.uint8)
    yy, xx = np.mgrid[:240, :320]
    src[..., 0] = (xx * 255 / 319).astype(np.uint8)
    src[..., 1] = (yy * 255 / 239).astype(np.uint8)
    src[..., 2] = 128
    pillow_heif.register_heif_opener()
    heic = wd / "photo.heic"
    Image.fromarray(src).save(heic, quality=92)
    neg = subprocess.run([sys.executable, "-I", "-c", "from PIL import Image; import sys\ntry:\n Image.open(sys.argv[1]); print('opened')\nexcept Exception as e: print(type(e).__name__)", str(heic)],
                         capture_output=True, text=True, timeout=30).stdout.strip()
    im = Image.open(heic)
    fmt, size = im.format, im.size
    png = wd / "photo.png"
    im.convert("RGB").save(png)
    back = np.asarray(Image.open(png)).astype(float)
    mse = float(((back - src) ** 2).mean())
    psnr = 10 * math.log10(255 ** 2 / max(mse, 1e-9))
    head = heic.read_bytes()[4:12]
    return [
        check("a HEIF/HEIC container was written (ftyp heic/mif1)", head[:4] == b"ftyp" and head[4:8] in (b"heic", b"mif1", b"heix"), head.decode(errors="replace"), "ftypheic"),
        check("Pillow opens it as HEIF through the registered opener", fmt == "HEIF" and size == (320, 240), [fmt, list(size)], ["HEIF", [320, 240]]),
        check("converted PNG matches the source (PSNR > 32 dB)", psnr > 32, psnr, "> 32 dB"),
        check("negative control: plain Pillow without the opener cannot identify the HEIC", neg == "UnidentifiedImageError", neg, "UnidentifiedImageError"),
    ], [png, heic]


@card("MEDIA-31")
def music21_analysis(task, wd):
    """music21: build a 10-note line, analyse its key (Krumhansl-Schmuckler) -> C major; name chords (C-E-G major triad,
    G7 dominant seventh); write and re-parse MusicXML. The same line transposed up a fifth is the control (G major)."""
    from music21 import stream, note, chord, converter, interval
    s = stream.Stream()
    for n in "C4 D4 E4 F4 G4 A4 B4 C5 G4 C4".split():
        s.append(note.Note(n, quarterLength=1))
    k = s.analyze("key")
    triad = chord.Chord(["C4", "E4", "G4"])
    g7 = chord.Chord(["G3", "B3", "D4", "F4"])
    xml = wd / "line.musicxml"
    s.write("musicxml", fp=str(xml))
    back = converter.parse(str(xml))
    names = [n.nameWithOctave for n in back.recurse().notes]
    t = s.transpose(interval.Interval("P5"))
    kt = t.analyze("key")
    rep = jw(wd / "analysis.json", {"key": str(k), "corr": k.correlationCoefficient, "triad": triad.commonName, "g7": g7.commonName, "reparsed": names, "transposed_key": str(kt)})
    return [
        check("key analysed as C major", (k.tonic.name, k.mode) == ("C", "major"), str(k), "C major"),
        check("C-E-G is a major triad; G-B-D-F a dominant seventh", triad.commonName == "major triad" and g7.commonName == "dominant seventh chord", [triad.commonName, g7.commonName], ["major triad", "dominant seventh chord"]),
        check("MusicXML round-trip keeps the 10 notes", names == "C4 D4 E4 F4 G4 A4 B4 C5 G4 C4".split(), names, "10 notes"),
        check("negative control: transposed up a fifth the key is G major, not C", (kt.tonic.name, kt.mode) == ("G", "major"), str(kt), "G major"),
    ], [xml, rep]


_FACE_PY = r"""
import json, sys, numpy as np, mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions
from skimage import data
img = data.astronaut()
out = {}
with vision.FaceDetector.create_from_options(vision.FaceDetectorOptions(base_options=BaseOptions(model_asset_path=sys.argv[1]))) as det:
    for k, a in (("astronaut", img), ("flat", np.full_like(img, 128)), ("flipped", np.ascontiguousarray(img[:, ::-1]))):
        r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(a)))
        out[k] = [[d.bounding_box.origin_x, d.bounding_box.origin_y, d.bounding_box.width, d.bounding_box.height, d.categories[0].score,
                   [[kp.x, kp.y] for kp in d.keypoints]] for d in r.detections]
print("JSON" + json.dumps(out))
"""


@card("MEDIA-32")
def mediapipe_faces(task, wd):
    """MediaPipe Tasks (1.2) FaceDetector with the BlazeFace short-range .task model (230 KB, cached in ~/.cache/kosif-models)
    on scikit-image's public-domain astronaut photo: one face with a box and six keypoints, the box drives a 9:16 reframe
    crop. A flat grey frame is the control (no face)."""
    if not FACE_MODEL.exists():
        raise RuntimeError("face model not cached: %s" % FACE_MODEL)
    py = wd / "face.py"
    py.write_text(_FACE_PY)
    done = run([sys.executable, py, FACE_MODEL], cwd=str(wd), timeout=60, env=dict(os.environ, GLOG_minloglevel="3", TF_CPP_MIN_LOG_LEVEL="3"))
    res = json.loads(done.stdout.split("JSON", 1)[1].splitlines()[0])
    from skimage import data
    img = data.astronaut()
    f = res["astronaut"][0] if res["astronaut"] else None
    crop = None
    if f:
        cx = f[0] + f[2] / 2
        h = img.shape[0]
        w = int(h * 9 / 16)
        x0 = int(min(max(0, cx - w / 2), img.shape[1] - w))
        crop = (x0, 0, x0 + w, h)
        Image.fromarray(img).crop(crop).save(wd / "reframe_9x16.png")
        Image.fromarray(img).save(wd / "astronaut.png")
    fl = res["flipped"][0] if res["flipped"] else None
    rep = jw(wd / "faces.json", res | {"reframe_crop": crop})
    return [
        check("exactly one face found on the astronaut photo (score > .8)", len(res["astronaut"]) == 1 and f[4] > 0.8, [len(res["astronaut"]), f[4] if f else None], "1, > .8"),
        check("the face box lies on the face region (centre x 200..250, y 110..150)", f and 200 <= f[0] + f[2] / 2 <= 250 and 110 <= f[1] + f[3] / 2 <= 150, f[:4] if f else None, "centre ~ (224, 130)"),
        check("six facial keypoints returned", f and len(f[5]) == 6, len(f[5]) if f else 0, 6),
        check("mirrored photo: the box mirrors (x -> 512 - x - w, within 6 px)", fl and abs(fl[0] - (512 - f[0] - f[2])) <= 6, [fl[0] if fl else None, 512 - f[0] - f[2] if f else None], "mirrored"),
        check("9:16 reframe crop keeps the face inside", crop and crop[0] <= f[0] and f[0] + f[2] <= crop[2], crop, "contains the face"),
        check("negative control: a flat grey frame has no face", res["flat"] == [], len(res["flat"]), 0),
    ], [wd / "reframe_9x16.png", rep]


@card("MEDIA-39")
def psd_layers(task, wd):
    """Scripted layered PSD work with a permissive library (psd-tools, MIT), as the card advises instead of Mosamem code:
    build a two-layer PSD (background + an offset blue layer), save, reopen, read each layer's name/bbox, export each layer
    and the composite as PNG."""
    from psd_tools import PSDImage
    from psd_tools.api.layers import PixelLayer
    psd = PSDImage.new("RGB", (160, 120))
    bg = Image.new("RGB", (160, 120), (200, 30, 30))
    fg = Image.new("RGBA", (60, 40), (30, 30, 220, 255))
    psd.append(PixelLayer.frompil(bg, psd, "background"))
    psd.append(PixelLayer.frompil(fg, psd, "badge", top=50, left=70))
    path = wd / "layers.psd"
    psd.save(str(path))
    p2 = PSDImage.open(str(path))
    layers = [(l.name, tuple(l.bbox)) for l in p2]
    for l in p2:
        l.composite().save(wd / ("layer_%s.png" % l.name))
    comp = p2.composite().convert("RGB")
    comp.save(wd / "composite.png")
    hidden = PSDImage.open(str(path))
    hidden[1].visible = False
    comp_h = hidden.composite(force=True).convert("RGB")
    return [
        check("PSD file written (8BPS signature, version 1)", path.read_bytes()[:6] == b"8BPS\x00\x01", path.read_bytes()[:6], b"8BPS\x00\x01"),
        check("reopened with 2 named layers and their boxes", layers == [("background", (0, 0, 160, 120)), ("badge", (70, 50, 130, 90))], layers, [("background", (0, 0, 160, 120)), ("badge", (70, 50, 130, 90))]),
        check("composite: badge pixel blue, outside red", comp.getpixel((100, 70)) == (30, 30, 220) and comp.getpixel((10, 10)) == (200, 30, 30), [comp.getpixel((100, 70)), comp.getpixel((10, 10))], [(30, 30, 220), (200, 30, 30)]),
        check("per-layer export: the badge PNG is 60 x 40", Image.open(wd / "layer_badge.png").size == (60, 40), list(Image.open(wd / "layer_badge.png").size), [60, 40]),
        check("negative control: with the badge layer hidden the composite is red there", comp_h.getpixel((100, 70)) == (200, 30, 30), comp_h.getpixel((100, 70)), (200, 30, 30)),
    ], [path, wd / "composite.png"]


# ================================================================================================ self-discovery
def _frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    out = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line and not line.startswith(" "):
                k, v = line.split(":", 1)
                out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def discover_skills(roots):
    """list skills on disk: <root>/.claude/skills/<name>/SKILL.md and plugin skills <root>/plugins/<p>/skills/<s>/SKILL.md"""
    found = []
    for root in roots:
        root = Path(root)
        for sk in sorted(root.glob(".claude/skills/*/SKILL.md")):
            fm = _frontmatter(sk.read_text(encoding="utf-8", errors="replace"))
            found.append({"id": fm.get("name", sk.parent.name), "description": fm.get("description", ""), "path": str(sk)})
        for sk in sorted(root.glob("plugins/*/skills/*/SKILL.md")):
            fm = _frontmatter(sk.read_text(encoding="utf-8", errors="replace"))
            found.append({"id": "%s:%s" % (sk.parents[2].name, fm.get("name", sk.parent.name)), "description": fm.get("description", ""), "path": str(sk)})
    return found


def search_skills(skills, query):
    q = set(re.findall(r"\w+", query.lower()))
    scored = []
    for s in skills:
        words = set(re.findall(r"\w+", (s["id"] + " " + s["description"]).lower()))
        hit = len(q & words)
        if hit:
            scored.append((hit, s["id"]))
    return [i for _, i in sorted(scored, key=lambda x: (-x[0], x[1]))]


@card("SELF-08")
def discover_skills_first(task, wd):
    """Skills show as one line each: list them (on disk: ~/.claude/skills, .claude/skills, plugin skills as plugin:skill),
    search them and invoke the match before acting. A fixture home + project + plugin tree is scanned, then the real repo."""
    home, proj = wd / "home", wd / "proj"
    def mk(base, name, desc):
        p = base / name
        p.mkdir(parents=True, exist_ok=True)
        (p / "SKILL.md").write_text("---\nname: %s\ndescription: %s\n---\n# %s\n" % (name, desc, name), encoding="utf-8")
    mk(home / ".claude/skills", "montage-reel", "Beat-cut montage reels with Arabic captions")
    mk(proj / ".claude/skills", "pdf-tools", "Read, merge and split PDF files")
    mk(proj / "plugins/brand-kit/skills", "palette", "Brand colour palette and contrast checks")
    sk = discover_skills([home, proj])
    hit = search_skills(sk, "make a montage reel with captions")
    hit2 = search_skills(sk, "check palette contrast")
    none = search_skills(sk, "quantum chromodynamics lattice")
    real = discover_skills([REPO])
    rep = jw(wd / "skills_found.json", {"fixture": sk, "match_montage": hit, "match_palette": hit2, "no_match": none, "repo_skills": [s["id"] for s in real]})
    return [
        check("home, project and plugin skills found (plugin as plugin:skill)", sorted(s["id"] for s in sk) == ["brand-kit:palette", "montage-reel", "pdf-tools"], sorted(s["id"] for s in sk), ["brand-kit:palette", "montage-reel", "pdf-tools"]),
        check("search ranks the matching skill first (invoke it before acting)", hit[:1] == ["montage-reel"] and hit2[:1] == ["brand-kit:palette"], [hit[:1], hit2[:1]], [["montage-reel"], ["brand-kit:palette"]]),
        check("the real repo's skills are listed from their SKILL.md frontmatter", len(real) >= 5 and any(s["id"].startswith("kosif") for s in real), len(real), ">= 5"),
        check("negative control: an unrelated query matches nothing", none == [], none, []),
    ], [rep]


def resolve_service(service, tools, env):
    """name exactly what is needed when no tool covers a service; never echo a secret, never ask for it in chat"""
    s = service.lower()
    t = [x for x in tools if s in x.lower()]
    if t:
        return {"status": "tool", "use": t[0]}
    keyname = re.sub(r"[^A-Z0-9]", "_", service.upper()) + "_API_KEY"
    if env.get(keyname):
        return {"status": "key-present", "env": keyname, "note": "a key is set; call the service with it from code"}
    return {"status": "missing", "connector": "claude.ai Settings -> Connectors -> connect %s" % service,
            "secret": "or add %s as an environment secret (read_documentation environment.secrets)" % keyname,
            "never": "do not paste the key into the chat"}


@card("SELF-11")
def name_whats_missing(task, wd):
    """If no tool covers a service it may be an unconnected connector or a missing key: search the tool names, then the
    environment, and name exactly what is needed (connector path or the env secret's name) without ever echoing a secret."""
    tools = ["mcp__github__get_file_contents", "mcp__Higgsfield__generate_image", "WebFetch"]
    fake = "sk" + "-" + "x" * 30
    env = {"ELEVENLABS_API_KEY": fake}
    out = {s: resolve_service(s, tools, env) for s in ("github", "ElevenLabs", "Notion")}
    rep = jw(wd / "resolution.json", out)
    text = rep.read_text()
    return [
        check("a connected service resolves to its tool", out["github"] == {"status": "tool", "use": "mcp__github__get_file_contents"}, out["github"], "mcp__github__..."),
        check("a service with a key set is found through the env var name", out["ElevenLabs"]["status"] == "key-present" and out["ElevenLabs"]["env"] == "ELEVENLABS_API_KEY", out["ElevenLabs"]["status"], "key-present"),
        check("a missing service names the connector and the exact secret name", out["Notion"]["status"] == "missing" and "NOTION_API_KEY" in out["Notion"]["secret"] and "Connectors" in out["Notion"]["connector"],
              out["Notion"]["status"], "missing + names"),
        check("negative control: the secret value never appears in the output", fake not in text, fake in text, False),
    ], [rep]


def find_chromium(roots):
    hits = []
    for r in roots:
        r = Path(r)
        if r.exists():
            hits += [str(p) for p in sorted(r.glob("chromium-*/chrome-linux*/chrome")) + sorted(r.glob("chromium_headless_shell-*/chrome-linux*/headless_shell"))]
    return hits


@card("SELF-19")
def find_playwright_chromium(task, wd):
    """Chromium may ship with Playwright even when `chromium` is not on PATH: look in `npm root -g`, $PLAYWRIGHT_BROWSERS_PATH,
    /opt/pw-browsers and ~/.cache/ms-playwright, then run the binary before saying there is no browser."""
    groot = run(["npm", "root", "-g"], env=_node_env(wd)).stdout.strip()
    pwv = (Path(groot) / "playwright/package.json")
    pw_ver = json.loads(pwv.read_text())["version"] if pwv.exists() else None
    roots = [os.environ.get("PLAYWRIGHT_BROWSERS_PATH", ""), "/opt/pw-browsers", str(Path.home() / ".cache/ms-playwright")]
    hits = find_chromium([r for r in roots if r])
    ver = run([hits[0], "--version"], timeout=20).stdout.strip() if hits else None
    on_path = shutil.which("chromium") or shutil.which("chromium-browser")
    empty = wd / "empty_root"
    empty.mkdir(exist_ok=True)
    rep = jw(wd / "browser_found.json", {"npm_root": groot, "playwright": pw_ver, "found": hits, "version": ver, "chromium_on_PATH": on_path})
    return [
        check("the global Playwright package is found under npm root -g", pw_ver is not None, pw_ver, "x.y.z"),
        check("a Playwright Chromium binary is found in the browsers path", bool(hits), hits[:2], "chromium-*/chrome-linux64/chrome"),
        check("the found binary runs (--version)", bool(ver) and re.search(r"Chrom(e|ium)", ver) is not None, ver, "Chromium / Chrome for Testing NNN"),
        check("negative control: an empty browsers root yields nothing", find_chromium([empty]) == [], find_chromium([empty]), []),
    ], [rep]


@card("SELF-21")
def apt_simulate_first(task, wd):
    """If you are root and apt works, any Ubuntu package is one command away: id -u; sudo -n true; apt-get -s install <pkg>
    (simulation, no change). The simulation must resolve cowsay without installing it; a non-existent package must fail."""
    uid = run(["id", "-u"]).stdout.strip()
    sudo = subprocess.run(["sudo", "-n", "true"], capture_output=True, timeout=10).returncode == 0
    before = subprocess.run(["dpkg", "-s", "cowsay"], capture_output=True, timeout=10).returncode
    sim = run(["apt-get", "-s", "install", "cowsay"], timeout=60).stdout.strip().splitlines()
    after = subprocess.run(["dpkg", "-s", "cowsay"], capture_output=True, timeout=10).returncode
    bad = subprocess.run(["apt-get", "-s", "install", "kosif-no-such-package-zz"], capture_output=True, text=True, timeout=60)
    rep = jw(wd / "apt_sim.json", {"uid": uid, "sudo_ok": sudo, "sim_tail": sim[-1], "installed_before": before == 0, "installed_after": after == 0, "bad_rc": bad.returncode, "bad_err": bad.stderr.strip()[-120:]})
    return [
        check("running as root (or passwordless sudo)", uid == "0" or sudo, [uid, sudo], "root"),
        check("the simulation resolves the package ('Conf cowsay ...')", sim[-1].startswith("Conf cowsay"), sim[-1][:60], "Conf cowsay (...)"),
        check("simulation changes nothing (cowsay not installed before or after)", before != 0 and after != 0, [before, after], "not installed"),
        check("negative control: a non-existent package fails to resolve", bad.returncode != 0 and "Unable to locate package" in bad.stderr, bad.returncode, "!= 0"),
    ], [rep]


@card("SELF-22")
def docker_daemon_check(task, wd):
    """A docker binary does not mean a running daemon: `timeout 8 docker info --format '{{.ServerVersion}}'` decides before
    any promise of containers; when it fails, fall back to a local process (here a stdlib HTTP server answering a request)."""
    binary = shutil.which("docker")
    info = subprocess.run(["timeout", "8", "docker", "info", "--format", "{{.ServerVersion}}"], capture_output=True, text=True, timeout=15) if binary else None
    daemon = bool(info and info.returncode == 0 and info.stdout.strip())
    sock = Path("/var/run/docker.sock").exists()
    decision = "containers" if daemon else "fallback: local process"
    fb = None
    if not daemon:
        s = socket.socket()
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
        s.close()
        (wd / "srv").mkdir(exist_ok=True)
        (wd / "srv/ok.txt").write_text("ok")
        p = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1", "--directory", str(wd / "srv")],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            import urllib.request
            for _ in range(100):
                try:
                    fb = urllib.request.urlopen("http://127.0.0.1:%d/ok.txt" % port, timeout=1).read().decode()
                    break
                except OSError:
                    time.sleep(0.05)
        finally:
            p.terminate()
            p.wait(5)
    rep = jw(wd / "docker_check.json", {"binary": binary, "info_rc": info.returncode if info else None, "info_err": (info.stderr.strip()[-160:] if info else None),
                                        "daemon": daemon, "socket": sock, "decision": decision, "fallback_reply": fb})
    return [
        check("docker info was actually run with an 8 s timeout", info is not None or binary is None, binary, "/usr/bin/docker"),
        check("the decision follows the daemon, not the binary (daemon <-> socket agree)", daemon == (daemon and sock) and (decision == "containers") == daemon, [daemon, sock, decision], "consistent"),
        check("when there is no daemon the fallback local process answers", daemon or fb == "ok", fb, "ok"),
        check("negative control: binary presence alone would have claimed containers", not (bool(binary) and not daemon) or decision != "containers", [bool(binary), daemon], "binary without daemon -> no containers"),
    ], [rep]


@card("SELF-23")
def shallow_git_clone(task, wd):
    """Public git reads work: git clone --depth 1 <url> and git ls-remote. A local bare repository (file://) with three
    commits is the remote here, so the clone is real and offline; the full clone is the control."""
    env = dict(os.environ, HOME=str(wd), GIT_CONFIG_NOSYSTEM="1", GIT_AUTHOR_NAME="k", GIT_AUTHOR_EMAIL="k@example.invalid",
               GIT_COMMITTER_NAME="k", GIT_COMMITTER_EMAIL="k@example.invalid")
    src = wd / "src"
    src.mkdir(exist_ok=True)
    run(["git", "init", "-q", "-b", "main", src], env=env)
    for i in range(3):
        (src / "f.txt").write_text("v%d\n" % i)
        run(["git", "-C", src, "add", "f.txt"], env=env)
        run(["git", "-C", src, "commit", "-q", "-m", "c%d" % i], env=env)
    bare = wd / "remote.git"
    run(["git", "clone", "-q", "--bare", src, bare], env=env)
    url = bare.as_uri()
    ls = run(["git", "ls-remote", url], env=env).stdout.split()
    shallow = wd / "shallow"
    run(["git", "clone", "-q", "--depth", "1", url, shallow], env=env)
    full = wd / "full"
    run(["git", "clone", "-q", url, full], env=env)
    cnt = lambda d: int(run(["git", "-C", d, "rev-list", "--count", "HEAD"], env=env).stdout)
    is_sh = run(["git", "-C", shallow, "rev-parse", "--is-shallow-repository"], env=env).stdout.strip()
    head = run(["git", "-C", shallow, "rev-parse", "HEAD"], env=env).stdout.strip()
    rep = jw(wd / "git_report.json", {"ls_remote": ls, "shallow_count": cnt(shallow), "full_count": cnt(full), "is_shallow": is_sh, "file": (shallow / "f.txt").read_text()})
    return [
        check("git ls-remote lists HEAD and main", "HEAD" in ls and "refs/heads/main" in ls, ls[:4], ["<sha>", "HEAD", "<sha>", "refs/heads/main"]),
        check("--depth 1 clone holds one commit and is shallow", cnt(shallow) == 1 and is_sh == "true", [cnt(shallow), is_sh], [1, "true"]),
        check("its HEAD is the remote's HEAD with the latest file", head == ls[0] and (shallow / "f.txt").read_text() == "v2\n", head[:10], ls[0][:10]),
        check("negative control: a full clone has all 3 commits", cnt(full) == 3, cnt(full), 3),
    ], [rep]


def _pypi(pkg):
    import urllib.request
    import urllib.error
    try:
        with urllib.request.urlopen("https://pypi.org/pypi/%s/json" % pkg, timeout=8) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"http_error": e.code}


@card("SELF-24")
def ask_registry(task, wd):
    """Asking PyPI or npm tells within seconds whether a library exists, its version and its licence:
    https://pypi.org/pypi/<pkg>/json (version, license_expression) and npm view <pkg> version license --json."""
    t0 = time.time()
    hz = _pypi("humanize")
    t1 = time.time()
    npm = json.loads(run(["npm", "view", "left-pad", "version", "license", "--json"], env=_npm_env(wd), timeout=30).stdout)
    shutil.rmtree(wd / "npmcache", ignore_errors=True)
    t2 = time.time()
    missing = _pypi("kosif-no-such-package-zz-404")
    info = hz.get("info", {})
    lic = info.get("license_expression") or info.get("license")
    rep = jw(wd / "registry.json", {"humanize": {"version": info.get("version"), "license": lic, "requires_python": info.get("requires_python"), "s": t1 - t0},
                                    "left-pad": npm | {"s": t2 - t1}, "missing": missing})
    return [
        check("PyPI: humanize exists with a version and the MIT licence", bool(re.match(r"^\d+\.\d+", info.get("version", ""))) and "MIT" in (lic or ""), [info.get("version"), lic], ["x.y", "MIT"]),
        check("npm: left-pad 1.3.0, WTFPL", npm == {"version": "1.3.0", "license": "WTFPL"}, npm, {"version": "1.3.0", "license": "WTFPL"}),
        check("each lookup took <= 5 s", t1 - t0 <= 5 and t2 - t1 <= 5, [round(t1 - t0, 2), round(t2 - t1, 2)], "<= 5 s"),
        check("negative control: a package that does not exist answers 404", missing == {"http_error": 404}, missing, {"http_error": 404}),
    ], [rep]


@card("SELF-25")
def requires_python_check(task, wd):
    """PyPI's latest release may not install on this Python: read info.requires_python from the PyPI JSON and compare with
    the interpreter (packaging.specifiers), then see what pip really resolves (pip index versions)."""
    from packaging.specifiers import SpecifierSet
    from packaging.version import Version
    py = Version("%d.%d.%d" % sys.version_info[:3])
    res = {}
    for pkg in ("kokoro", "humanize"):
        j = _pypi(pkg)
        latest = j["info"]["version"]
        rp = j["info"]["requires_python"] or ""
        ok_latest = py in SpecifierSet(rp) if rp else True
        compat = [v for v, files in j["releases"].items() if files and not files[0].get("yanked") and (not files[0].get("requires_python") or py in SpecifierSet(files[0]["requires_python"]))]
        best = str(max(map(Version, compat))) if compat else None
        res[pkg] = {"latest": latest, "requires_python": rp, "latest_installs_here": ok_latest, "newest_compatible": best}
    pi = subprocess.run([sys.executable, "-m", "pip", "index", "versions", "kokoro", "--disable-pip-version-check"], capture_output=True, text=True, timeout=60)
    m = re.search(r"kokoro \(([^)]+)\)", pi.stdout)
    res["pip_resolves_kokoro"] = m.group(1) if m else pi.stdout.strip()[:80]
    rep = jw(wd / "requires_python.json", {"python": str(py), **res})
    return [
        check("kokoro's latest release excludes this Python (requires_python read from PyPI)", res["kokoro"]["latest_installs_here"] is False and py >= Version("3.13"), [res["kokoro"]["latest"], res["kokoro"]["requires_python"], str(py)], "latest needs < 3.13"),
        check("the newest compatible kokoro is older than the latest", Version(res["kokoro"]["newest_compatible"]) < Version(res["kokoro"]["latest"]), [res["kokoro"]["newest_compatible"], res["kokoro"]["latest"]], "older"),
        check("pip agrees: it resolves the newest compatible release, not the latest", res["pip_resolves_kokoro"] == res["kokoro"]["newest_compatible"], res["pip_resolves_kokoro"], res["kokoro"]["newest_compatible"]),
        check("negative control: humanize's latest does install here", res["humanize"]["latest_installs_here"] is True and res["humanize"]["newest_compatible"] == res["humanize"]["latest"], res["humanize"], "latest == compatible"),
    ], [rep]


@card("SELF-26")
def venv_smoke_test(task, wd):
    """Install into an isolated env, then import, print the version and run the smallest real example before claiming:
    uv venv + uv pip install humanize, then .venv/bin/python -I -c 'import humanize; print(humanize.__version__);
    print(humanize.intcomma(1234567))'. The system interpreter (no humanize) is the control."""
    venv = wd / ".venv"
    env = dict(os.environ, UV_CACHE_DIR=str(wd / "uvcache"), HOME=str(wd))
    t0 = time.time()
    uv = shutil.which("uv") or str(Path.home() / ".local/bin/uv")
    run([uv, "venv", "-q", venv], env=env, timeout=60)
    run([uv, "pip", "install", "-q", "--python", venv / "bin/python", "humanize"], env=env, timeout=90)
    dt = time.time() - t0
    out = run([venv / "bin/python", "-I", "-c", "import humanize; print(humanize.__version__); print(humanize.intcomma(1234567)); print(humanize.naturalsize(3000000))"], timeout=30).stdout.split("\n")
    sysimp = subprocess.run([sys.executable, "-I", "-c", "import humanize"], capture_output=True, text=True, timeout=30)
    rep = jw(wd / "smoke.json", {"seconds": dt, "version": out[0], "intcomma": out[1], "naturalsize": out[2], "system_import_rc": sysimp.returncode})
    shutil.rmtree(wd / "uvcache", ignore_errors=True)
    return [
        check("isolated venv created and the package installed into it", (venv / "bin/python").exists() and bool(re.match(r"^\d+\.\d+", out[0])), out[0], "x.y.z"),
        check("smoke test is a real call: intcomma(1234567) == '1,234,567'", out[1] == "1,234,567", out[1], "1,234,567"),
        check("naturalsize(3000000) == '3.0 MB'", out[2] == "3.0 MB", out[2], "3.0 MB"),
        check("negative control: the system interpreter does not have it", sysimp.returncode != 0 and "ModuleNotFoundError" in sysimp.stderr, sysimp.returncode, "!= 0"),
    ], [rep]


@card("SELF-27")
def npm_scratch_try(task, wd):
    """A scratch folder with npm init is enough to try a JS package in seconds: npm init -y && npm i culori@4.0.2 (exact pin)
    && node -e import('culori'). The import before installing is the control."""
    d = wd / "try"
    d.mkdir(exist_ok=True)
    env = _npm_env(wd)
    probe = "import('culori').then(m => console.log(JSON.stringify({keys: Object.keys(m).length, hex: m.formatHex('rebeccapurple'), parse: m.parse('#ff0000')}))).catch(e => console.log(JSON.stringify({err: e.code || String(e)})))"
    before = json.loads(run([_NODE, "-e", probe], cwd=str(d), env=env).stdout)
    run(["npm", "init", "-y"], cwd=str(d), env=env, timeout=60)
    t0 = time.time()
    run(["npm", "i", "--no-audit", "--no-fund", "culori@4.0.2"], cwd=str(d), env=env, timeout=120)
    dt = time.time() - t0
    after = json.loads(run([_NODE, "-e", probe], cwd=str(d), env=env).stdout)
    pin = json.loads((d / "package.json").read_text())["dependencies"]["culori"]
    inst = json.loads((d / "node_modules/culori/package.json").read_text())["version"]
    shutil.rmtree(wd / "npmcache", ignore_errors=True)
    rep = jw(wd / "npm_try.json", {"before": before, "after": after, "pinned": pin, "installed": inst, "install_s": dt})
    return [
        check("exact version installed (4.0.2)", inst == "4.0.2", inst, "4.0.2"),
        check("the import works and a real call answers: formatHex('rebeccapurple') == '#663399'", after.get("hex") == "#663399", after.get("hex"), "#663399"),
        check("parse('#ff0000') -> rgb 1, 0, 0", after.get("parse") == {"mode": "rgb", "r": 1, "g": 0, "b": 0}, after.get("parse"), {"mode": "rgb", "r": 1, "g": 0, "b": 0}),
        check("negative control: before npm i the import fails", "err" in before, before, "ERR_MODULE_NOT_FOUND"),
    ], [rep, d / "package.json"]


def _meminfo(path):
    for line in Path(path).read_text().splitlines():
        if line.startswith("MemTotal:"):
            return int(line.split()[1]) * 1024
    return None


@card("SELF-36")
def measure_container(task, wd):
    """A cloud session is a Linux container with about 4 vCPU, 16 GB and network per the environment setting: measure before
    relying on it - CPUs from two sources, memory from /proc/meminfo and sysconf, free disk of the work folder, outbound
    reachability of a package registry, and whether a Docker daemon answers."""
    cpus = [os.cpu_count(), len(os.sched_getaffinity(0))]
    mem = _meminfo("/proc/meminfo")
    mem2 = os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")
    du = shutil.disk_usage(wd)
    net = None
    try:
        import urllib.request
        net = urllib.request.urlopen("https://pypi.org/simple/", timeout=8).status
    except Exception as exc:
        net = "unreachable: %s" % type(exc).__name__
    dock = Path("/var/run/docker.sock").exists()
    fake = wd / "meminfo_fixture"
    fake.write_text("MemTotal:        2048000 kB\nMemFree: 1 kB\n")
    rep = jw(wd / "container.json", {"cpus": cpus, "mem_gib": mem / 2 ** 30, "mem_sysconf_gib": mem2 / 2 ** 30, "disk_free_gb": du.free / 1e9, "registry": net, "docker_socket": dock,
                                     "documented": {"vcpu": 4, "ram_gb": 16, "disk_gb": 30}})
    return [
        check("CPU count agrees between os.cpu_count and the affinity mask", cpus[0] == cpus[1] and cpus[0] >= 1, cpus, "equal"),
        check("memory agrees between /proc/meminfo and sysconf (within 1 %)", abs(mem - mem2) / mem < 0.01, [mem / 2 ** 30, mem2 / 2 ** 30], "equal"),
        check("free disk measured on the work folder (> 1 GB)", du.free > 1e9, du.free / 1e9, "> 1 GB"),
        check("network to a registry measured (HTTP status or the failure recorded)", net == 200 or str(net).startswith("unreachable"), net, "200 or recorded"),
        check("negative control: the parser reads the file it is given (fixture 2,048,000 kB)", _meminfo(fake) == 2048000 * 1024 != mem, _meminfo(fake), 2048000 * 1024),
    ], [rep]


API_PREINSTALLED = {"pandas", "numpy", "scipy", "sklearn", "statsmodels", "matplotlib", "seaborn", "openpyxl", "xlsxwriter", "docx", "pptx",
                    "pypdf", "pdfplumber", "PIL", "sympy", "json", "csv", "math", "re", "os", "sys", "io", "datetime", "collections", "itertools",
                    "statistics", "pathlib", "random", "functools", "textwrap", "string", "zipfile"}


def api_sandbox_lint(src):
    """flag what fails in the API code-execution container: imports outside the preinstalled set, network calls, installs"""
    import ast
    tree = ast.parse(src)
    issues = []
    for n in ast.walk(tree):
        if isinstance(n, (ast.Import, ast.ImportFrom)):
            mods = [a.name for a in n.names] if isinstance(n, ast.Import) else [n.module or ""]
            for m in mods:
                top = m.split(".")[0]
                if top in ("requests", "urllib", "httpx", "socket", "aiohttp"):
                    issues.append(("network", top, n.lineno))
                elif top not in API_PREINSTALLED:
                    issues.append(("not-preinstalled", top, n.lineno))
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and re.search(r"\bpip\s+install\b|https?://", n.value):
            issues.append(("install-or-url", n.value[:40], n.lineno))
    return issues


@card("SELF-37")
def api_container_rules(task, wd):
    """In the API, code runs in a container with no internet and no package installs (Python 3.11, 1 CPU, 5 GiB): work with
    the preinstalled libraries only. An AST lint checks scripts against those rules; the clean script runs here as-is."""
    good = "import pandas as pd\nimport numpy as np\ndf = pd.DataFrame({'a': np.arange(5)})\nprint(int(df.a.sum()))\n"
    bad = "import torch\nimport requests\nimport subprocess\nsubprocess.run('pip install kokoro', shell=True)\nr = requests.get('https://example.com')\n"
    (wd / "good.py").write_text(good)
    (wd / "bad.py").write_text(bad)
    gi, bi = api_sandbox_lint(good), api_sandbox_lint(bad)
    ran = run([sys.executable, "-I", wd / "good.py"]).stdout.strip()
    rep = jw(wd / "api_lint.json", {"good": gi, "bad": bi, "good_output": ran, "limits": {"python": "3.11", "cpu": 1, "ram_gib": 5, "disk_gib": 5, "network": False}})
    kinds = sorted({k for k, _, _ in bi})
    return [
        check("the clean pandas/numpy script passes and runs (sum 0..4 = 10)", gi == [] and ran == "10", [gi, ran], [[], "10"]),
        check("torch and subprocess flagged as not preinstalled", {("not-preinstalled", "torch"), ("not-preinstalled", "subprocess")} <= {(k, m) for k, m, _ in bi}, [m for k, m, _ in bi if k == "not-preinstalled"], ["torch", "subprocess"]),
        check("network library and the URL / pip install strings flagged", "network" in kinds and "install-or-url" in kinds, kinds, ["install-or-url", "network", "not-preinstalled"]),
        check("negative control: the untreated bad script is not clean", len(bi) >= 4, len(bi), ">= 4 issues"),
    ], [rep]


NET_LEVELS = {"off": set(), "package-managers": {"pypi.org", "files.pythonhosted.org", "registry.npmjs.org", "crates.io", "archive.ubuntu.com", "registry.yarnpkg.com", "github.com"}}


def claude_ai_allowed(level, host, extra=()):
    if level == "all":
        return True
    allowed = set(NET_LEVELS["package-managers"]) if level in ("package-managers", "package-managers+domains") else set()
    if level == "package-managers+domains":
        allowed |= set(extra)
    return host in allowed


@card("SELF-38")
def claude_ai_sandbox_policy(task, wd):
    """claude.ai creates docx/xlsx/pptx/pdf in a sandbox: max 30 MB per file; network egress per plan/admin: Off, Package
    managers only, Package managers + domains, All domains. Real files are sized against the limit and hosts checked per
    level."""
    small, big = wd / "report.pdf", wd / "video_raw.bin"
    small.write_bytes(b"%PDF-1.4\n" + b"0" * 1024 * 1024)
    with open(big, "wb") as f:
        f.truncate(31 * 1024 * 1024)
    LIMIT = 30 * 1024 * 1024
    sizes = {p.name: p.stat().st_size for p in (small, big)}
    over = sorted(n for n, s in sizes.items() if s > LIMIT)
    hosts = ["pypi.org", "registry.npmjs.org", "api.example.com", "huggingface.co"]
    table = {lvl: {h: claude_ai_allowed(lvl, h, ["api.example.com"]) for h in hosts} for lvl in ("off", "package-managers", "package-managers+domains", "all")}
    rep = jw(wd / "policy.json", {"sizes": sizes, "over_30mb": over, "egress": table})
    return [
        check("the 31 MB file is over the 30 MB per-file limit, the 1 MB PDF is not", over == ["video_raw.bin"], over, ["video_raw.bin"]),
        check("Off blocks every host", not any(table["off"].values()), table["off"], "all False"),
        check("Package managers only: PyPI and npm yes, other domains no", table["package-managers"] == {"pypi.org": True, "registry.npmjs.org": True, "api.example.com": False, "huggingface.co": False},
              table["package-managers"], "pm only"),
        check("+ domains adds exactly the listed domain", table["package-managers+domains"]["api.example.com"] and not table["package-managers+domains"]["huggingface.co"], table["package-managers+domains"], "pm + api.example.com"),
        check("negative control: All domains allows what the narrower levels refuse", table["all"]["huggingface.co"] and not table["package-managers"]["huggingface.co"], [table["all"]["huggingface.co"], table["package-managers"]["huggingface.co"]], [True, False]),
    ], [rep, small]


# ================================================================================================ voice / TTS
ELEVEN_MODELS = {"eleven_flash_v2_5": {"ttfb_ms": 75, "credit_per_char": 0.5, "expr": 1}, "eleven_turbo_v2_5": {"ttfb_ms": 150, "credit_per_char": 0.5, "expr": 2},
                 "eleven_multilingual_v2": {"ttfb_ms": 300, "credit_per_char": 1.0, "expr": 3}, "eleven_v3": {"ttfb_ms": 500, "credit_per_char": 1.0, "expr": 4, "arabic": True}}
ELEVEN_FORMATS = {"editing": "pcm_44100", "delivery": "mp3_44100_128", "streaming": "mp3_22050_32"}


def pick_eleven(use, chars, budget_ms=None):
    if use == "realtime":
        m = min((k for k in ELEVEN_MODELS if budget_ms is None or ELEVEN_MODELS[k]["ttfb_ms"] <= budget_ms), key=lambda k: ELEVEN_MODELS[k]["ttfb_ms"])
    elif use == "narration":
        m = "eleven_multilingual_v2"
    else:                                        # maximum expression (70+ languages incl. Arabic)
        m = max(ELEVEN_MODELS, key=lambda k: ELEVEN_MODELS[k]["expr"])
    return {"model": m, "credits": chars * ELEVEN_MODELS[m]["credit_per_char"], "ttfb_ms": ELEVEN_MODELS[m]["ttfb_ms"]}


@card("VOICE-07")
def eleven_model_format_table(task, wd):
    """The ElevenLabs model/format table as a selector: flash (~75 ms TTFB) for realtime, turbo (~150 ms), multilingual_v2
    (~300 ms) for narration, v3 (~500 ms, Arabic) for maximum expression; flash/turbo .5 credit/char, v2/v3 1.0. Format by
    destination: pcm_44100 for editing, mp3_44100_128 (~16 KB/s) for delivery, mp3_22050_32 only for streaming. The bitrate
    claims are measured by encoding a real 4 s signal with ffmpeg (no API call, nothing spent)."""
    picks = {"realtime": pick_eleven("realtime", 1000), "narration": pick_eleven("narration", 1000), "expressive_ar": pick_eleven("expressive", 1000),
             "realtime_200ms": pick_eleven("realtime", 400, budget_ms=200)}
    sig = wd / "speechlike.wav"
    rate = 44100
    t = np.arange(4 * rate) / rate
    x = 0.4 * np.sin(2 * math.pi * 180 * t) * (0.5 + 0.5 * np.sin(2 * math.pi * 3 * t)) + 0.05 * np.random.default_rng(1).normal(size=t.size)
    fx.write_wav(sig, x, rate)
    sizes = {}
    for fmt, args in (("pcm_44100", ["-c:a", "pcm_s16le", "-ar", "44100", "-ac", "1"]), ("mp3_44100_128", ["-c:a", "libmp3lame", "-b:a", "128k", "-ar", "44100", "-ac", "1"]),
                      ("mp3_22050_32", ["-c:a", "libmp3lame", "-b:a", "32k", "-ar", "22050", "-ac", "1"])):
        out = wd / (fmt + (".wav" if fmt.startswith("pcm") else ".mp3"))
        fx.ffmpeg("-i", sig, *args, out)
        sizes[fmt] = out.stat().st_size / 4 / 1000
    rep = jw(wd / "eleven_table.json", {"picks": picks, "formats": ELEVEN_FORMATS, "kb_per_s": sizes})
    return [
        check("realtime -> flash, narration -> multilingual_v2, max expression -> v3", [picks["realtime"]["model"], picks["narration"]["model"], picks["expressive_ar"]["model"]] == ["eleven_flash_v2_5", "eleven_multilingual_v2", "eleven_v3"],
              [picks[k]["model"] for k in ("realtime", "narration", "expressive_ar")], ["flash", "multilingual_v2", "v3"]),
        check("credits: 1000 chars cost 500 on flash and 1000 on v2", picks["realtime"]["credits"] == 500 and picks["narration"]["credits"] == 1000, [picks["realtime"]["credits"], picks["narration"]["credits"]], [500, 1000]),
        check("mp3_44100_128 measures ~16 KB/s", 15 <= sizes["mp3_44100_128"] <= 17, sizes["mp3_44100_128"], "~16"),
        check("pcm_44100 (editing) is ~88 KB/s mono 16-bit, mp3_22050_32 ~4 KB/s", 87 <= sizes["pcm_44100"] <= 90 and 3.5 <= sizes["mp3_22050_32"] <= 4.5, [sizes["pcm_44100"], sizes["mp3_22050_32"]], [88.2, 4]),
        check("negative control: a 200 ms realtime budget excludes multilingual_v2 / v3", picks["realtime_200ms"]["ttfb_ms"] <= 200, picks["realtime_200ms"], "<= 200 ms"),
    ], [rep, wd / "mp3_44100_128.mp3"]


def split_script(text, limit=5000):
    sents = re.findall(r"[^.!?؟。]+[.!?؟。]?\s*", text)
    chunks, cur = [], ""
    for s in sents:
        if len(cur) + len(s) > limit and cur:
            chunks.append(cur.strip())
            cur = ""
        cur += s
    if cur.strip():
        chunks.append(cur.strip())
    return [{"text": c, "previous_text": chunks[i - 1][-300:] if i else None, "next_text": chunks[i + 1][:300] if i + 1 < len(chunks) else None}
            for i, c in enumerate(chunks)]


@card("VOICE-08")
def chunk_and_join_pcm(task, wd):
    """Split over-limit scripts on sentence ends below 5000 chars, sending previous_text / next_text with each chunk; decode
    every chunk to WAV and concat the PCM - never `-c copy` MP3s, whose frame padding drifts word timings by tens of ms per
    join. Each chunk's audio here is a deterministic test signal of known length (no TTS call); both joins are measured."""
    sent = "هذه جملة عربية قصيرة للاختبار تتكرر لتكوين نص طويل. "
    text = sent * 330
    chunks = split_script(text)
    rate = 44100
    mp3s, durs = [], []
    for i, c in enumerate(chunks):
        n = int(rate * (2.0 + 0.37 * i))
        x = 0.3 * np.sin(2 * math.pi * (220 + 40 * i) * np.arange(n) / rate)
        w = wd / ("chunk_%d.wav" % i)
        fx.write_wav(w, x, rate)
        m = wd / ("chunk_%d.mp3" % i)
        fx.ffmpeg("-i", w, "-c:a", "libmp3lame", "-b:a", "128k", m)
        mp3s.append(m)
        durs.append(n / rate)
    lst = wd / "list.txt"
    lst.write_text("".join("file '%s'\n" % p for p in mp3s))
    copy = wd / "joined_copy.mp3"
    fx.ffmpeg("-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", copy)
    decs = []
    for m in mp3s:
        d = m.with_suffix(".dec.wav")
        fx.ffmpeg("-i", m, "-c:a", "pcm_s16le", d)
        decs.append(d)
    pcm = wd / "joined_pcm.wav"
    # trim each decoded chunk to its true sample length (the encoder's priming/padding removed), then join the PCM
    parts = []
    for d, n in zip(decs, durs):
        a, r_ = fx.read_wav(d)
        parts.append(a[:int(round(n * rate)), 0])
    fx.write_wav(pcm, np.concatenate(parts), rate)
    probe_d = lambda p: float(fx.probe(p)["format"]["duration"])
    truth = sum(durs)
    drift_copy = probe_d(copy) - truth
    drift_pcm = probe_d(pcm) - truth
    rep = jw(wd / "join_report.json", {"chunks": [{"chars": len(c["text"]), "has_prev": c["previous_text"] is not None, "has_next": c["next_text"] is not None} for c in chunks],
                                       "truth_s": truth, "drift_copy_ms": drift_copy * 1000, "drift_pcm_ms": drift_pcm * 1000})
    return [
        check("script split into chunks under 5000 chars on sentence ends", len(chunks) >= 3 and all(len(c["text"]) < 5000 and c["text"].endswith(".") for c in chunks), [len(c["text"]) for c in chunks], "< 5000 each"),
        check("neighbouring text passed: first has only next, last only previous, middle both",
              chunks[0]["previous_text"] is None and chunks[-1]["next_text"] is None and all(c["previous_text"] and c["next_text"] for c in chunks[1:-1]), len(chunks), "prev/next"),
        check("nothing lost: chunks rejoin to the script", "".join(c["text"] + " " for c in chunks).split() == text.split(), len(text.split()), "same words"),
        check("PCM join keeps the exact timeline (drift < 1 ms)", abs(drift_pcm) < 0.001, drift_pcm * 1000, "< 1 ms"),
        check("negative control: -c copy MP3 join drifts by > 10 ms per join", drift_copy > 0.010 * (len(chunks) - 1), drift_copy * 1000, "> 10 ms x joins"),
    ], [pcm, rep]


TTS_ORDER = [("heygen-starfish", "HEYGEN_API_KEY", True), ("elevenlabs", "ELEVENLABS_API_KEY", False), ("kokoro-82m", None, False)]


def validate_speed(v):
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not (0.5 <= float(v) <= 2.0):
        raise ValueError("speed must be a positive number in 0.5..2.0, got %r" % (v,))
    return float(v)


def pick_tts(env, local_models):
    for name, key, ts in TTS_ORDER:
        if (key and env.get(key)) or (key is None and name in local_models):
            return {"provider": name, "word_timestamps": ts, "needs_transcription": not ts}
    return {"provider": None, "reason": "no provider: set HEYGEN_API_KEY or ELEVENLABS_API_KEY, or install a local model"}


@card("VOICE-14")
def provider_with_timestamps(task, wd):
    """Provider order of the vendor engine: HeyGen Starfish (word timestamps in the response) -> ElevenLabs (none) ->
    Kokoro-82M; speed is validated before any TTS runs (0, 5, -1 and text are refused). With timestamps in the response the
    caption step needs no post-transcription; the resolver and validator are run on fixture environments (no call made)."""
    k = lambda: "k" + "_" + "x" * 20
    cases = {"heygen": pick_tts({"HEYGEN_API_KEY": k(), "ELEVENLABS_API_KEY": k()}, {"kokoro-82m"}), "eleven": pick_tts({"ELEVENLABS_API_KEY": k()}, set()),
             "local": pick_tts({}, {"kokoro-82m"}), "none": pick_tts({}, set())}
    speeds = {}
    for v in (0, 5, -1, "fast", True, 1.0, 0.9):
        try:
            speeds[repr(v)] = validate_speed(v)
        except ValueError as exc:
            speeds[repr(v)] = "refused"
    words = [{"word": "مرحبا", "start": 0.12, "end": 0.58}, {"word": "بكم", "start": 0.66, "end": 0.98}]
    caps = [{"t": w["start"], "end": w["end"], "text": w["word"]} for w in words] if cases["heygen"]["word_timestamps"] else None
    rep = jw(wd / "tts_route.json", {"cases": cases, "speeds": speeds, "captions_from_response": caps})
    return [
        check("HeyGen first when its key is set (timestamps in the response)", cases["heygen"] == {"provider": "heygen-starfish", "word_timestamps": True, "needs_transcription": False}, cases["heygen"], "heygen-starfish"),
        check("then ElevenLabs (no timestamps -> transcription needed), then local Kokoro", cases["eleven"]["provider"] == "elevenlabs" and cases["eleven"]["needs_transcription"] and cases["local"]["provider"] == "kokoro-82m",
              [cases["eleven"]["provider"], cases["local"]["provider"]], ["elevenlabs", "kokoro-82m"]),
        check("speed 0, 5, -1, text and a bool are refused before any TTS runs", all(speeds[x] == "refused" for x in ("0", "5", "-1", "'fast'", "True")), speeds, "refused"),
        check("valid speeds pass through (1.0, 0.9)", speeds["1.0"] == 1.0 and speeds["0.9"] == 0.9, [speeds["1.0"], speeds["0.9"]], [1.0, 0.9]),
        check("captions built straight from response timestamps", caps and caps[0] == {"t": 0.12, "end": 0.58, "text": "مرحبا"}, caps, "from response"),
        check("negative control: no key and no model -> no provider, with the exact names to set", cases["none"]["provider"] is None and "HEYGEN_API_KEY" in cases["none"]["reason"], cases["none"], "None"),
    ], [rep]


@card("VOICE-15")
def audio_manifest_master_clock(task, wd):
    """One script produces narration with word timings, background music and SFX cues, recorded in audio_meta.json - one
    manifest is the master clock. The narration here is a deterministic syllable-burst fixture (no TTS key); word timings are
    measured from its energy, SFX are placed on the manifest's cues, the bed is ducked under the voice and everything is mixed."""
    rate = 48000
    words = ["هذا", "اختبار", "لساعة", "واحدة", "للصوت"]
    starts = [0.30, 0.95, 1.70, 2.30, 3.05]
    lens = [0.40, 0.55, 0.42, 0.50, 0.45]
    dur = 4.0
    n = int(dur * rate)
    t = np.arange(n) / rate
    voice = np.zeros(n)
    for s0, L in zip(starts, lens):
        m = (t >= s0) & (t < s0 + L)
        env = np.sin(np.pi * (t[m] - s0) / L)
        voice[m] = 0.5 * env * np.sin(2 * math.pi * 170 * t[m]) * (1 + 0.3 * np.sin(2 * math.pi * 900 * t[m]))
    vw = fx.write_wav(wd / "voice.wav", voice, rate)
    v, _ = fx.read_wav(vw)
    v = v[:, 0]
    hop = int(0.01 * rate)
    e = np.array([np.sqrt((v[i:i + hop] ** 2).mean()) for i in range(0, len(v) - hop, hop)])
    act = e > 0.02
    edges = np.flatnonzero(np.diff(act.astype(int)))
    segs = [(round((a + 1) * 0.01, 2), round((b + 1) * 0.01, 2)) for a, b in zip(edges[::2], edges[1::2])]
    timing = [{"word": w, "start": s, "end": e_} for w, (s, e_) in zip(words, segs)]
    cues = [{"id": "whoosh", "at_word": 1}, {"id": "hit", "at_word": 4}]
    for c in cues:
        c["t"] = timing[c["at_word"]]["start"]
    bgm = 0.25 * np.sin(2 * math.pi * 110 * t) * 0.5 + 0.25 * np.sin(2 * math.pi * 165 * t) * 0.5
    duck = np.ones(n)
    for w in timing:
        duck[int(w["start"] * rate):int(w["end"] * rate)] = 10 ** (-12 / 20)
    k = int(0.05 * rate)
    duck = np.convolve(duck, np.ones(k) / k, mode="same")
    sfx = np.zeros(n)
    for c in cues:
        i0 = int(c["t"] * rate)
        L = int(0.12 * rate)
        sfx[i0:i0 + L] += 0.6 * np.exp(-np.arange(L) / (0.02 * rate)) * np.sin(2 * math.pi * 2000 * np.arange(L) / rate)
    mix = voice + bgm * duck + sfx
    peak = np.abs(mix).max()
    mix = mix / peak * 0.89
    mw = fx.write_wav(wd / "mix.wav", mix, rate)
    meta = jw(wd / "audio_meta.json", {"master_clock": "audio_meta.json", "duration": dur, "rate": rate, "voice": "voice.wav", "bgm": {"duck_db": -12},
                                        "words": timing, "sfx": cues, "mix": "mix.wav"})
    m2, _ = fx.read_wav(mw)
    m2 = m2[:, 0]
    sx = []
    for c in cues:
        i0 = int(c["t"] * rate)
        seg_ = m2[i0 - int(0.05 * rate):i0 + int(0.05 * rate)]
        hp = np.diff(seg_)
        sx.append(round((np.argmax(np.abs(hp)) - int(0.05 * rate)) / rate * 1000, 1))
    bed_gap = float(np.sqrt(((bgm * duck)[int(0.1 * rate):int(0.25 * rate)] ** 2).mean()))
    bed_word = float(np.sqrt(((bgm * duck)[int((starts[2] + 0.15) * rate):int((starts[2] + 0.3) * rate)] ** 2).mean()))
    errs = [max(abs(w["start"] - s0), abs(w["end"] - (s0 + L))) for w, s0, L in zip(timing, starts, lens)]
    return [
        check("five words timed from the narration's energy (within 30 ms)", len(timing) == 5 and max(errs) <= 0.03, [round(x * 1000) for x in errs], "<= 30 ms"),
        check("SFX land on their cue words (onset within 5 ms of the word start)", all(abs(x) <= 5 for x in sx), sx, "<= 5 ms"),
        check("the bed is ducked ~12 dB under the voice", abs(20 * math.log10(bed_word / bed_gap) + 12) < 1.0, 20 * math.log10(bed_word / bed_gap), -12),
        check("one manifest holds words, cues and files; the mix length matches it", len(m2) == int(dur * rate) and json.loads(meta.read_text())["sfx"][1]["t"] == timing[4]["start"], len(m2) / rate, dur),
        check("negative control: the untreated voice track has no SFX transient at the cue", float(np.abs(np.diff(voice[int(cues[0]["t"] * rate):int(cues[0]["t"] * rate) + 200])).max()) < 0.05,
              float(np.abs(np.diff(voice[int(cues[0]["t"] * rate):int(cues[0]["t"] * rate) + 200])).max()), "< 0.05"),
    ], [mw, meta]


_WORKER_JS = r"""
// A Cloudflare-Worker-style fetch handler: the browser posts its SDP offer, the worker adds the key and session config.
const LIMIT_SDP = 200000, LIMIT_CTX = 14000;
export default {
  async fetch(request, env, upstream = fetch) {
    const url = new URL(request.url);
    if (request.method !== 'POST' || url.pathname !== '/api/realtime/session') return new Response('not found', {status: 404});
    if ((request.headers.get('content-type') || '').split(';')[0].trim() !== 'application/sdp') return new Response('expected application/sdp', {status: 415});
    const sdp = await request.text();
    if (sdp.length > LIMIT_SDP) return new Response('SDP too large', {status: 413});
    if (!sdp.startsWith('v=0')) return new Response('not an SDP offer', {status: 400});
    const ctx = (url.searchParams.get('context') || '').slice(0, LIMIT_CTX);
    const session = {type: 'realtime', model: 'gpt-realtime', audio: {input: {transcription: {model: 'gpt-4o-mini-transcribe', language: 'ar'}, turn_detection: {type: 'server_vad'}},
      output: {voice: 'marin'}}, instructions: ctx};
    const form = new FormData(); form.set('sdp', sdp); form.set('session', JSON.stringify(session));
    const r = await upstream('https://api.openai.com/v1/realtime/calls', {method: 'POST', headers: {Authorization: 'Bearer ' + env.OPENAI_API_KEY}, body: form});
    return new Response(await r.text(), {status: r.status, headers: {'content-type': 'application/sdp'}});
  }
};
"""

_WORKER_TEST = r"""
import worker from './worker.mjs';
const seen = [];
const upstream = async (u, init) => { const sess = JSON.parse(init.body.get('session')); seen.push({u, auth: init.headers.Authorization, sess, sdpLen: init.body.get('sdp').length});
  return new Response('v=0\r\no=answer', {status: 201}); };
const env = {OPENAI_API_KEY: process.argv[2]};
const offer = 'v=0\r\no=- 1 1 IN IP4 127.0.0.1\r\ns=-\r\nm=audio 9 UDP/TLS/RTP/SAVPF 111\r\n';
const call = (body, ct, q = '') => worker.fetch(new Request('https://w.example/api/realtime/session' + q, {method: 'POST', headers: {'content-type': ct}, body}), env, upstream);
const out = {};
let r = await call(offer, 'application/sdp', '?context=' + encodeURIComponent('ملف'.repeat(6000))); out.ok = {status: r.status, ct: r.headers.get('content-type'), body: await r.text()};
r = await call(offer, 'application/json'); out.badType = r.status;
r = await call('v=0' + 'a'.repeat(200001), 'application/sdp'); out.big = r.status;
r = await call('hello', 'application/sdp'); out.notSdp = r.status;
r = await worker.fetch(new Request('https://w.example/other', {method: 'GET'}), env, upstream); out.other = r.status;
out.upstream = seen.map(s => ({u: s.u, authOk: s.auth === 'Bearer ' + env.OPENAI_API_KEY, model: s.sess.model, lang: s.sess.audio.input.transcription.language,
  vad: s.sess.audio.input.turn_detection.type, voice: s.sess.audio.output.voice, ctxLen: s.sess.instructions.length, sdpLen: s.sdpLen}));
out.calls = seen.length;
console.log(JSON.stringify(out));
"""


@card("VOICE-46")
def realtime_sdp_worker(task, wd):
    """The browser opens WebRTC and posts its SDP offer to a Worker that adds the key and session config (model gpt-realtime,
    input transcription gpt-4o-mini-transcribe in Arabic, server_vad, voice 'marin', file context <= 14000 chars) and relays
    the answer. The Worker's fetch handler runs in Node 22 with the upstream call stubbed (no network, nothing spent):
    Content-Type application/sdp and SDP <= 200000 bytes are enforced."""
    (wd / "worker.mjs").write_text(_WORKER_JS)
    (wd / "test.mjs").write_text(_WORKER_TEST)
    key = "sk" + "-" + "t" * 32
    res = json.loads(run([_NODE, wd / "test.mjs", key], cwd=str(wd), env=_node_env(wd)).stdout)
    up = res["upstream"][0] if res["upstream"] else {}
    rep = jw(wd / "worker_report.json", res)
    return [
        check("the SDP answer is relayed with application/sdp", res["ok"] == {"status": 201, "ct": "application/sdp", "body": "v=0\r\no=answer"}, res["ok"], "201 sdp"),
        check("the worker adds the key server-side and the session config", up.get("authOk") and [up.get("model"), up.get("lang"), up.get("vad"), up.get("voice")] == ["gpt-realtime", "ar", "server_vad", "marin"],
              [up.get("model"), up.get("lang"), up.get("vad"), up.get("voice")], ["gpt-realtime", "ar", "server_vad", "marin"]),
        check("file context capped at 14000 chars", up.get("ctxLen") == 14000, up.get("ctxLen"), 14000),
        check("wrong content type 415, oversize SDP 413, non-SDP 400, other routes 404", [res["badType"], res["big"], res["notSdp"], res["other"]] == [415, 413, 400, 404],
              [res["badType"], res["big"], res["notSdp"], res["other"]], [415, 413, 400, 404]),
        check("negative control: refused requests never reach the upstream (1 call only) and the key is not in any reply", res["calls"] == 1 and key not in json.dumps(res["ok"]), res["calls"], 1),
    ], [rep, wd / "worker.mjs"]


_BARGE_JS = r"""
// barge-in: speech_started while the assistant is speaking -> emit 'interrupted' and send response.cancel
export function createVoiceUI(channel) {
  let state = 'idle'; const events = [];
  const emit = (e) => events.push(e);
  return {
    get state() { return state; }, events,
    onServerEvent(ev) {
      if (ev.type === 'response.output_audio.delta' || ev.type === 'response.audio.delta') { if (state !== 'speaking') { state = 'speaking'; emit('speaking'); } }
      else if (ev.type === 'response.done') { if (state === 'speaking') { state = 'listening'; emit('listening'); } }
      else if (ev.type === 'input_audio_buffer.speech_started') {
        if (state === 'speaking') { this.interrupt(); emit('interrupted'); }
        state = 'listening';
      }
    },
    interrupt() { channel.send(JSON.stringify({type: 'response.cancel'})); },
  };
}
"""

_BARGE_TEST = r"""
import { createVoiceUI } from './voice.mjs';
const run = (seq) => { const sent = []; const ui = createVoiceUI({send: (m) => sent.push(JSON.parse(m))}); const states = [];
  for (const t of seq) { ui.onServerEvent({type: t}); states.push(ui.state); } return {sent, events: ui.events, states}; };
const barge = run(['response.output_audio.delta', 'response.output_audio.delta', 'input_audio_buffer.speech_started']);
const quiet = run(['input_audio_buffer.speech_started']);
const done = run(['response.output_audio.delta', 'response.done', 'input_audio_buffer.speech_started']);
console.log(JSON.stringify({barge, quiet, done}));
"""


@card("VOICE-47")
def barge_in(task, wd):
    """If the user speaks while the assistant talks, the UI flips to listening and the response is cancelled: on
    input_audio_buffer.speech_started while state = speaking -> emit 'interrupted'; interrupt() sends {type:'response.cancel'}
    over the data channel. The state machine runs in Node against a recording fake data channel."""
    (wd / "voice.mjs").write_text(_BARGE_JS)
    (wd / "test.mjs").write_text(_BARGE_TEST)
    r = json.loads(run([_NODE, wd / "test.mjs"], cwd=str(wd), env=_node_env(wd)).stdout)
    rep = jw(wd / "barge_report.json", r)
    return [
        check("speech while speaking -> 'interrupted' and state listening", r["barge"]["events"] == ["speaking", "interrupted"] and r["barge"]["states"][-1] == "listening", r["barge"], "speaking -> interrupted"),
        check("exactly one response.cancel sent over the data channel", r["barge"]["sent"] == [{"type": "response.cancel"}], r["barge"]["sent"], [{"type": "response.cancel"}]),
        check("after the response is done, user speech cancels nothing", r["done"]["sent"] == [] and "interrupted" not in r["done"]["events"], r["done"], "no cancel"),
        check("negative control: speech while idle sends no cancel", r["quiet"]["sent"] == [] and r["quiet"]["events"] == [], r["quiet"], "nothing"),
    ], [rep, wd / "voice.mjs"]


# ───────────── APP-08: data apps with streamlit and gradio (installed with the owner's approval) ─────────────
_ST_APP = """import streamlit as st

NUMS = [3, 1, 4, 1, 5, 9, 2, 6]
k = int(st.query_params.get("k", "2"))
st.title("Moving average")
st.slider("window", 1, 4, k, disabled=True)
ma = [round(sum(NUMS[i:i + k]) / k, 3) for i in range(len(NUMS) - k + 1)]
st.write("KOSIF-SUM=%d" % sum(NUMS))
st.write("KOSIF-MA=" + ",".join(str(x) for x in ma))
"""

_GR_APP = """import sys, gradio as gr


def stats(text, k):
    w = text.split()
    return {"words": len(w), "top": sorted(set(w), key=lambda x: (-w.count(x), x))[:int(k)]}


demo = gr.Interface(fn=stats, inputs=[gr.Textbox(label="text"), gr.Number(value=2, label="k")], outputs=gr.JSON(),
                    api_name="predict")
demo.launch(server_name="127.0.0.1", server_port=int(sys.argv[1]), prevent_thread_lock=True, quiet=True, share=False)
print("READY", flush=True)
sys.stdin.read()
"""

_ST_READ = """import json, sys
from playwright.sync_api import sync_playwright
base, out = sys.argv[1], sys.argv[2]
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", args=["--no-sandbox"])
    pg = b.new_page()
    for k in ("2", "3"):
        pg.goto(base + "/?k=" + k)
        pg.wait_for_selector("text=KOSIF-MA=", timeout=12000)
        res[k] = [x.strip() for x in pg.inner_text("body").split("\\n") if "KOSIF-" in x]
    b.close()
json.dump(res, open(out, "w"))
"""


def _app_env(wd, **extra):
    import site
    home = Path(wd) / "_home"
    (home / "tmp").mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, HOME=str(home), XDG_CACHE_HOME=str(home / ".cache"), XDG_CONFIG_HOME=str(home / ".config"),
               MPLCONFIGDIR=str(home / ".mpl"), HF_HOME=str(home / ".hf"), GRADIO_TEMP_DIR=str(home / "gradio"),
               GRADIO_ANALYTICS_ENABLED="False", STREAMLIT_BROWSER_GATHER_USAGE_STATS="false", PYTHONUSERBASE=site.getuserbase(),
               TMPDIR="_home/tmp", NO_PROXY="127.0.0.1,localhost", no_proxy="127.0.0.1,localhost")
    env.update({k: str(v) for k, v in extra.items()})
    return env


def _get(url, data=None, timeout=5):
    import urllib.request
    op = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"} if data else {})
    with op.open(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def _wait_http(url, limit=20.0, proc=None):
    t0 = time.time()
    while time.time() - t0 < limit:
        if proc is not None and proc.poll() is not None:
            raise RuntimeError("server exited early: " + (proc.stdout.read() if proc.stdout else "")[-400:])
        try:
            return _get(url, timeout=1)
        except Exception:
            time.sleep(0.1)
    raise RuntimeError("server did not answer in %.0f s: %s" % (limit, url))


def _free_port():
    s_ = socket.socket()
    s_.bind(("127.0.0.1", 0))
    port = s_.getsockname()[1]
    s_.close()
    return port


@card("APP-08")
def data_apps_streamlit_gradio(task, wd):
    """Both data-app engines as running servers on 127.0.0.1, started inside the runner and stopped before it returns:
    `streamlit run app.py` (moving average over a fixed series, window from the query string) is read in a real Chrome via
    Playwright, and `gr.Interface(fn, inputs, outputs).launch()` (word stats) is called through its HTTP API. Answers are
    checked against numpy; the static page without the running script is the negative control."""
    wd = Path(wd)
    (wd / "app.py").write_text(_ST_APP)
    (wd / "gr_app.py").write_text(_GR_APP)
    (wd / "st_read.py").write_text(_ST_READ)
    env = _app_env(wd)
    sp, gp = _free_port(), _free_port()
    st_base, gr_base = "http://127.0.0.1:%d" % sp, "http://127.0.0.1:%d" % gp
    try:
        _get(gr_base + "/", timeout=0.5)
        refused = False
    except Exception:
        refused = True
    procs = []
    try:
        t0 = time.time()
        gr_p = subprocess.Popen([sys.executable, "gr_app.py", str(gp)], cwd=str(wd), env=env, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        procs.append(gr_p)
        st_p = subprocess.Popen(["streamlit", "run", "app.py", "--server.headless", "true", "--server.port", str(sp),
                                 "--server.address", "127.0.0.1", "--browser.gatherUsageStats", "false",
                                 "--global.developmentMode", "false"], cwd=str(wd), env=env, stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        procs.append(st_p)
        health = _wait_http(st_base + "/_stcore/health", proc=st_p)
        shell = _get(st_base + "/")
        rd = subprocess.run([sys.executable, "st_read.py", st_base, "st_dom.json"], cwd=str(wd), env=env, capture_output=True,
                            text=True, timeout=40)
        if rd.returncode:
            raise RuntimeError("playwright read failed: " + rd.stderr[-400:])
        st_seen = json.loads((wd / "st_dom.json").read_text())
        st_up = time.time() - t0
        _wait_http(gr_base + "/", limit=25, proc=gr_p)
        gr_home = _get(gr_base + "/")
        info = json.loads(_get(gr_base + "/gradio_api/info"))
        eid = json.loads(_get(gr_base + "/gradio_api/call/predict", json.dumps({"data": ["b a c a b a", 2]}).encode()))["event_id"]
        stream = _get(gr_base + "/gradio_api/call/predict/" + eid, timeout=10)
        gr_up = time.time() - t0
    finally:
        for p in procs:
            p.terminate()
        for p in procs:
            try:
                p.wait(5)
            except subprocess.TimeoutExpired:
                p.kill()
    m = re.search(r"event: complete\s*data: (.*)", stream)
    gr_ans = json.loads(m.group(1))[0] if m else None
    nums = np.array([3, 1, 4, 1, 5, 9, 2, 6], float)
    ma = lambda k: ",".join(str(round(float(v), 3)) for v in np.convolve(nums, np.ones(k) / k, mode="valid"))
    want = {k: ["KOSIF-SUM=%d" % nums.sum(), "KOSIF-MA=" + ma(int(k))] for k in ("2", "3")}
    stopped = all(p.poll() is not None for p in procs)
    rep = jw(wd / "apps_report.json", {"streamlit": {"health": health, "seen": st_seen, "expected": want, "seconds": st_up},
                                       "gradio": {"endpoints": sorted(info.get("named_endpoints", {})), "answer": gr_ans,
                                                  "seconds": gr_up}, "stopped": stopped})
    return [check("streamlit server healthy on 127.0.0.1", health.strip() == "ok", health),
            check("streamlit page rendered the script's numbers (k=2) in Chrome", st_seen.get("2") == want["2"], st_seen.get("2"), want["2"]),
            check("query string re-runs the script (k=3 moving average)", st_seen.get("3") == want["3"], st_seen.get("3"), want["3"]),
            check("gradio exposes the /predict endpoint", "/predict" in info.get("named_endpoints", {}), sorted(info.get("named_endpoints", {}))),
            check("gradio API answer = word count 6, top-2 [a, b]", gr_ans == {"words": 6, "top": ["a", "b"]}, gr_ans),
            check("gradio served its UI page", "<!doctype html>" in gr_home.lower()),
            check("both servers stopped before the runner returned", stopped),
            check("negative control: no server before launch, and the static shell has no computed numbers",
                  refused and "KOSIF-" not in shell, [refused, "KOSIF-" in shell], [True, False])], [rep, wd / "app.py", wd / "gr_app.py"]


GAPS = {k.split(":", 1)[1]: v for k, v in GAPS.items()}      # power_run looks gaps up by bare card ID
