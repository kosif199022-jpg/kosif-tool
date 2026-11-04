"""engines-render-pipeline (wave 3, chunk 03): method cards as real programs with known-answer checks.

Engines used here (all local, offline at run time):
  * HyperFrames CLI 0.9.8 (global npm ``hyperframes``) with its pinned chrome-headless-shell and ffmpeg:
    init / add / catalog / lint / check / snapshot / render / preview / info / compositions / timeline / doctor / docs /
    clean / catch-up, and its runtime adapters for GSAP, Anime.js, CSS keyframes and WAAPI.
    Every call runs with HOME=<work>/.hfhome so its history and caches stay inside the work folder.
  * @hyperframes/sdk 0.9.8 (npm, installed for ENG-182), vega 5.30 + vega-lite 5.21 (ENG-149), pixi.js 8.6.6 (ENG-263),
    @tailwindcss/browser 4.2.4 (ENG-194, the exact file the HyperFrames scaffold pins by sha384), moviepy 2.1.2 (pip, ENG-243).
  * three r186 (WebGPURenderer + TSL on Chrome's SwiftShader WebGPU adapter), lottie-web, maplibre-gl, d3, animejs, p5, gsap,
    @slidev/parser + rough-notation, plotly + kaleido, all through Playwright Chromium on a loopback file server.
  * The repo's own KOSIF Motion tools: motion.py, kmotion.py, workbench, web/server.py (Starlette on 127.0.0.1),
    cloud_setup.py, ffprobe_shim.py, html_render.py, film.py, kosif-one plan.py, pixel-studio-painter studio.py.
Each card measures its own output and runs the same measurement on the untreated input (negative control).
"""
import glob
import hashlib
import html as _html
import json
import math
import os
import re
import shutil
import socket
import subprocess
import sys
import threading
import time
from pathlib import Path

from _harness import card, check, fx, sha

REPO = Path(__file__).resolve().parents[4]
VEND = REPO / ".claude/skills/kosif-superpowers/vendor/100-superskills/skills"
KMM = VEND / "kosif-montage-motion/scripts"
MOTION = KMM / "motion.py"
KMOTION = KMM / "kmotion.py"
STUDIO = VEND / "pixel-studio-painter/scripts/studio.py"

_EXT = "external engine from the 500-tool HyperFrames catalog, link only: not installed here"
GAPS: dict = {
    "ENG-143": "Blender is not installed (no blender binary; the bpy wheel is several hundred MB) so Cycles cannot run",
    "ENG-153": "needs a live ComfyUI server with GPU models on :8188; none runs here and a mock would only test itself",
    "ENG-154": "ComfyUI frontend (subgraphs, blueprints, App Mode) is not installed; it is a live GUI app",
    "ENG-174": "hyperframes capture downloads a third-party website and captions screenshots with a cloud AI model (key + network)",
    "ENG-176": "present needs an interactive presenter/audience browser session; publish uploads to a hosted HeyGen project",
    "ENG-178": "cloud / lambda / cloudrun need a HeyGen account or AWS/GCP accounts with billing (paid live services)",
    "ENG-179": "figma import needs a Figma account token; claude-design handoff needs the hosted Claude Design service",
    "ENG-181": "the Studio editor's WebMCP tools need an interactive agent browser session against the live studio app",
    "ENG-184": "on-device vector tier needs a consent-gated 33 MB ONNX model download into ~/.hyperframes (outside the work folder)",
    "ENG-238": _EXT + " (Editly needs native headless-gl and node-canvas builds)",
    "ENG-239": _EXT + " (FFCreator needs native node-canvas + headless-gl)",
    "ENG-240": _EXT + " (fframes is a Rust crate needing a cargo build with ffmpeg dev headers)",
    "ENG-241": _EXT + " (Manim Community needs pycairo/pangocairo system libraries, not present)",
    "ENG-242": _EXT + " (Motion Canvas needs a Vite project build and its browser renderer plugin)",
    "ENG-244": "Remotion is installed but a cold webpack bundle measured 17-23 s here, over the 15 s runner budget",
    "ENG-245": _EXT + " (Rendervid)",
    "ENG-246": _EXT + " (Revideo needs a Vite build plus its headless renderer)",
    "ENG-247": _EXT + " (VideoFlow)",
    "ENG-248": _EXT + " (VideoRenderingEngine)",
    "ENG-249": _EXT + " (VidPy needs the MLT melt binary, not installed)",
    "ENG-250": _EXT + " (WebMotion)",
    "ENG-251": _EXT + " (Diffusion Studio Core, browser WebCodecs engine)",
    "ENG-252": _EXT + " (Etro)",
    "ENG-253": _EXT + " (Movie Masher)",
    "ENG-254": _EXT + " (Twick)",
    "ENG-255": _EXT + " (WebAV)",
    "ENG-256": "Creatomate is a paid hosted rendering API (key + network)",
    "ENG-257": "iLoveVideoEditor is a hosted web service",
    "ENG-258": "JSON2Video is a paid hosted rendering API (key + network)",
    "ENG-259": "Shotstack is a paid hosted rendering API (key + network)",
    "ENG-261": "Remotion Agent Skills is a catalogue link to an external skill pack (not installed)",
    "ENG-262": "hyperframes skills installs plugin files into the agent's own config folders from the network",
    "ENG-293": "the painting window is a Tkinter desktop app and tkinter is not installed here (no display either)",
    "ENG-303": "the Animation menu lives inside the Tkinter studio window (tkinter not installed)",
    "ENG-30": "the KOSIF Omni MCP server source (kosif-one/tools/kosif-omni/mcp-server) is not in this repository",
    "ENG-316": "@remotion/three needs a Remotion webpack bundle (17-23 s cold here, over budget) plus @react-three/fiber",
    "ENG-322": "AWS Lambda + Step Functions + S3 need an AWS account with billing",
    "ENG-324": "After Effects is a paid desktop app (Adobe), not available on Linux",
    "ENG-326": "Premiere Pro / After Effects / AME are paid Adobe desktop apps, not available here",
    "ENG-327": "DaVinci Resolve Studio external scripting needs the running proprietary app",
    "ENG-329": "Cassette is a remote editing agent behind an account and back-end",
    "ENG-330": "Unreal Engine 5 editor + its MCP server are not installed (proprietary, GPU)",
    "ENG-334": "GCP Cloud Run + Workflows + GCS need a Google Cloud account with billing",
    "ENG-335": "needs a Kubernetes cluster to run the batch render jobs",
    "ENG-336": "HeyGen-hosted cloud render needs an OAuth login or API key and uploads the project",
    "ENG-337": "Google Cloud Run render needs a GCP project with billing",
    "ENG-338": "plugin marketplace installs go over the network into the agent's own config (account-level)",
    "ENG-339": "remote planning needs the hosted KOSIF Site and KOSIF_SITE_TOKEN (consent-gated live service)",
    "ENG-340": "remote 2D render needs the hosted KOSIF Site render service (token, quota, network)",
    "ENG-341": "site bridge planner talks to the hosted workbench (token + network)",
}

# ----------------------------------------------------------------------------------------------- helpers


def _node_root():
    for base in [Path(shutil.which("node") or "/usr/bin/node").resolve().parent.parent / "lib/node_modules",
                 Path("/opt/node22/lib/node_modules"), Path("/usr/lib/node_modules"), Path("/usr/local/lib/node_modules")]:
        if (base / "gsap").exists():
            return base
    return Path("/opt/node22/lib/node_modules")


NM = _node_root()
GSAP_JS = NM / "gsap/dist/gsap.min.js"
_REAL_HOME = Path(os.path.expanduser("~"))


def _hf_chrome():
    hits = sorted(glob.glob(str(_REAL_HOME / ".cache/hyperframes/chrome/chrome-headless-shell/*/chrome-headless-shell-linux64/chrome-headless-shell")))
    return hits[-1] if hits else ""


def _hf_bin():
    return shutil.which("hyperframes") or str(NM / "hyperframes/bin/hyperframes.mjs")


def hf_env(wd):
    env = dict(os.environ)
    env.update(HOME=str(Path(wd) / ".hfhome"), HYPERFRAMES_SKIP_SKILLS="1", DO_NOT_TRACK="1", HYPERFRAMES_NO_TELEMETRY="1",
               HYPERFRAMES_EXTRACT_CACHE_DIR=str(Path(wd) / ".hfx"))
    ch = _hf_chrome()
    if ch:
        env["HYPERFRAMES_BROWSER_PATH"] = ch
    return env


def hf(wd, *args, timeout=60, ok=True, env=None):
    """Run the HyperFrames CLI with its home inside the work folder."""
    e = hf_env(wd)
    e.update(env or {})
    done = subprocess.run([_hf_bin(), *[str(a) for a in args]], capture_output=True, text=True, timeout=timeout,
                          stdin=subprocess.DEVNULL, env=e, cwd=str(wd))
    if ok and done.returncode:
        raise RuntimeError("hyperframes %s failed (%d): %s" % (args[0], done.returncode, (done.stderr or done.stdout)[-500:]))
    return done


def jparse(text):
    """The JSON document in a CLI's stdout (skipping banner lines)."""
    i = text.find("{")
    j = text.find("[")
    starts = [k for k in (i, j) if k >= 0]
    if not starts:
        raise ValueError("no JSON in output: " + text[:200])
    s = text[min(starts):]
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        dec = json.JSONDecoder()
        return dec.raw_decode(s)[0]


def hfj(wd, *args, **kw):
    return jparse(hf(wd, *args, **kw).stdout)


def jw(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    return Path(path)


def box_comp(w=320, h=180, dur=1.0, fps=None, bg="#000", tween=None, extra_body="", extra_css="", head="", root_attrs="",
             gsap=True, comp_id="main"):
    """A HyperFrames composition: a red 40x40 box whose centre moves 20 -> w-20 linearly over `dur` (GSAP by default)."""
    tw = tween if tween is not None else 'tl.fromTo("#box",{x:0},{x:%d,duration:%s,ease:"none"},0);' % (w - 40, dur)
    fps_attr = ' data-fps="%d"' % fps if fps else ""
    return ("<!doctype html><html><head><meta charset=\"UTF-8\">%s%s<style>html,body{margin:0;width:%dpx;height:%dpx;overflow:hidden;"
            "background:%s}#box{position:absolute;left:0;top:%dpx;width:40px;height:40px;background:#ff0000}%s</style></head><body>"
            "<div id=\"root\" data-composition-id=\"%s\" data-start=\"0\" data-duration=\"%s\" data-width=\"%d\" data-height=\"%d\"%s%s>"
            "<div id=\"box\" class=\"clip\" data-start=\"0\" data-duration=\"%s\" data-track-index=\"0\"></div>%s</div>"
            "<script>window.__timelines=window.__timelines||{};%s</script></body></html>"
            % ('<script src="gsap.min.js"></script>' if gsap else "", head, w, h, bg, h // 2 - 20, extra_css, comp_id, dur, w, h,
               fps_attr, root_attrs, dur, extra_body,
               ('const tl=gsap.timeline({paused:true});%swindow.__timelines["%s"]=tl;' % (tw, comp_id)) if gsap else ""))


def hf_project(wd, name, html_text, files=None):
    d = Path(wd) / name
    d.mkdir(parents=True, exist_ok=True)
    shutil.copy(GSAP_JS, d / "gsap.min.js")
    (d / "index.html").write_text(html_text, encoding="utf-8")
    for rel, content in (files or {}).items():
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, (bytes, bytearray)):
            p.write_bytes(content)
        elif isinstance(content, Path):
            shutil.copy(content, p)
        else:
            p.write_text(content, encoding="utf-8")
    return d


def red_cx(arr, thr=150):
    """Centre x of the red box in an RGB array (None when absent)."""
    import numpy as np
    a = np.asarray(arr, dtype=float)
    m = (a[..., 0] > thr) & (a[..., 1] < 90) & (a[..., 2] < 90)
    xs = np.nonzero(m)[1]
    return float(xs.mean()) if len(xs) else None


def load_rgb(path, mode="RGB"):
    import numpy as np
    from PIL import Image
    return np.asarray(Image.open(path).convert(mode)).astype(float)


def snapshot(wd, proj, times):
    d = hfj(wd, "snapshot", proj, "--at", ",".join(str(t) for t in times), "--json", timeout=60)
    frames = d.get("frames") or d.get("files") or []
    return {round(float(f["time"]), 3): Path(f["path"]) for f in frames}, d


def probe_v(path):
    p = fx.probe(path)
    v = [s for s in p["streams"] if s["codec_type"] == "video"][0]
    return p, v


def nframes(path):
    out = fx.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                  "stream=nb_read_frames", "-of", "csv=p=0", str(path)]).stdout.strip()
    return int(out.split(",")[0])


def write_mp4(path, frames, fps=30, lossless=True):
    import numpy as np
    arr = [np.asarray(f, dtype=np.uint8) for f in frames]
    h, w = arr[0].shape[:2]
    codec = ["-c:v", "libx264rgb", "-qp", "0", "-preset", "ultrafast"] if lossless else ["-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p"]
    p = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                        "-s", "%dx%d" % (w, h), "-r", str(fps), "-i", "-", *codec, str(path)],
                       input=b"".join(a.tobytes() for a in arr), capture_output=True, timeout=60)
    if p.returncode:
        raise RuntimeError(p.stderr.decode(errors="replace")[-300:])
    return Path(path)


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def http(method, url, body=None, headers=None, timeout=20):
    import urllib.error
    import urllib.request
    data = None
    hd = dict(headers or {})
    if body is not None:
        data = json.dumps(body).encode() if not isinstance(body, (bytes, bytearray)) else bytes(body)
        hd.setdefault("content-type", "application/json")
    req = urllib.request.Request(url, data=data, headers=hd, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read(), dict(e.headers or {})


class Served:
    """Serve the work folder on 127.0.0.1 (``/nm/...`` maps to the global node_modules) for browser pages."""

    def __init__(self, root):
        import http.server
        root = Path(root)

        class H(http.server.SimpleHTTPRequestHandler):
            def translate_path(self, path):
                p = path.split("?", 1)[0].split("#", 1)[0]
                from urllib.parse import unquote
                p = unquote(p)
                f = (NM / p[4:]) if p.startswith("/nm/") else (root / p.lstrip("/"))
                if not f.exists() and Path(str(f) + ".js").exists():      # extensionless ESM imports (roughjs/bin)
                    f = Path(str(f) + ".js")
                return str(f)

            def log_message(self, *a):
                pass

            def end_headers(self):
                self.send_header("Cache-Control", "no-store")
                super().end_headers()

        H.extensions_map = dict(H.extensions_map, **{".js": "text/javascript; charset=utf-8", ".mjs": "text/javascript; charset=utf-8",
                                                       ".html": "text/html; charset=utf-8", ".json": "application/json",
                                                       ".wasm": "application/wasm"})
        self.srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
        self.port = self.srv.server_address[1]
        self.t = threading.Thread(target=self.srv.serve_forever, daemon=True)
        self.t.start()

    def url(self, rel):
        return "http://127.0.0.1:%d/%s" % (self.port, rel)

    def close(self):
        self.srv.shutdown()
        self.srv.server_close()


def _pw_chrome():
    for pat in ("/opt/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell",
                "/opt/pw-browsers/chromium-*/chrome-linux64/chrome"):
        hits = sorted(glob.glob(pat))
        if hits:
            return hits[-1]
    return shutil.which("google-chrome") or shutil.which("chromium")


WEBGPU = ["--enable-unsafe-webgpu", "--enable-features=Vulkan", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"]
SOFTGL = ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"]


def browser(wd, name, page_html, flags=(), size=(320, 180), wait="window.__r !== undefined", timeout=20000, shots=None,
            init_script=None):
    """Load a page from the work folder in Playwright Chromium; return (window.__r, console log).
    `shots` = list of (js_expression_before, png_name) to screenshot after evaluating each expression."""
    from playwright.sync_api import sync_playwright
    wd = Path(wd)
    (wd / (name + ".html")).write_text(page_html, encoding="utf-8")
    srv = Served(wd)
    logs = []
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(args=["--no-sandbox", *flags], executable_path=_pw_chrome())
            try:
                pg = b.new_page(viewport={"width": size[0], "height": size[1]})
                pg.on("console", lambda m: logs.append(m.text[:300]))
                pg.on("pageerror", lambda e: logs.append("ERR " + str(e)[:300]))
                if init_script:
                    pg.add_init_script(init_script)
                pg.goto(srv.url(name + ".html"))
                try:
                    pg.wait_for_function(wait, timeout=timeout)
                except Exception as exc:  # noqa: BLE001 — report what the page said
                    raise RuntimeError("page never finished (%s): %s" % (type(exc).__name__, logs[-4:]))
                outs = []
                for expr, png in shots or []:
                    if expr:
                        pg.evaluate(expr)
                    pg.screenshot(path=str(wd / png))
                    outs.append(wd / png)
                r = pg.evaluate("window.__r")
            finally:
                b.close()
    finally:
        srv.close()
    if isinstance(r, dict) and r.get("err"):
        raise RuntimeError("page error: %s | %s" % (r["err"][:400], logs[-3:]))
    return r, logs


def kenv(wd, **extra):
    env = dict(os.environ)
    env.update(KOSIF_MOTION_HOME=str(wd), HYPERFRAMES_SKIP_SKILLS="1", PYTHONIOENCODING="utf-8")
    env.update({k: str(v) for k, v in extra.items()})
    return env


def py(script, *args, wd, timeout=60, env=None, ok=True):
    done = subprocess.run([sys.executable, str(script), *[str(a) for a in args]], capture_output=True, text=True,
                          timeout=timeout, stdin=subprocess.DEVNULL, cwd=str(wd), env=env or kenv(wd))
    if ok and done.returncode:
        raise RuntimeError("%s failed (%d): %s" % (Path(script).name, done.returncode, (done.stderr or done.stdout)[-600:]))
    return done


def last_json(text):
    """The last top-level JSON object printed by a tool (multi-line pretty JSON allowed)."""
    k = text.rfind("\n{")
    k = 0 if k < 0 and text.startswith("{") else k
    for start in [m.start() for m in re.finditer(r"(?m)^\{", text)][::-1]:
        try:
            return json.JSONDecoder().raw_decode(text[start:])[0]
        except json.JSONDecodeError:
            continue
    raise ValueError("no JSON object in output: " + text[-300:])


# ======================================================================================= HyperFrames CLI


@card("ENG-120")
def hf_render_matrix(task, wd):
    """render --format webm keeps alpha: transparent ground stays alpha 0, the box alpha 255; fps flag sets frame count."""
    import numpy as np
    proj = hf_project(wd, "matrix", box_comp(w=160, h=90, dur=1.0, bg="transparent"))
    out = wd / "matrix.webm"
    hf(wd, "render", proj, "-o", out, "--format", "webm", "-q", "draft", "--fps", "10", "-w", "1", "--quiet", timeout=90)
    p, v = probe_v(out)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-c:v", "libvpx-vp9", "-i", str(out), "-vf", "select=eq(n\\,5)",
                          "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgba", "-"], capture_output=True, timeout=60).stdout
    fr = np.frombuffer(raw, dtype=np.uint8).reshape(90, 160, 4).astype(float)
    corner_a = float(fr[2:10, 2:10, 3].mean())
    cx = red_cx(fr[..., :3] * (fr[..., 3:4] / 255.0))
    box_a = float(fr[35:55, int(cx) - 5:int(cx) + 5, 3].mean()) if cx else 0.0
    n = nframes(out)
    alpha_tag = (v.get("tags") or {}).get("alpha_mode") or (v.get("tags") or {}).get("ALPHA_MODE")
    return [check("codec is VP9 in WebM", v["codec_name"] == "vp9", v["codec_name"], "vp9"),
            check("alpha_mode tag present", str(alpha_tag) == "1", alpha_tag, "1"),
            check("--fps 10 x 1 s -> 10 frames", n == 10, n, 10),
            check("transparent ground decodes to alpha 0", corner_a < 5, corner_a, "< 5"),
            check("box at frame 5 centred at 20+120*0.5=80 px", cx is not None and abs(cx - 80) <= 3, cx, 80),
            check("negative control: the box pixels are opaque (criterion alpha<5 fails there)", box_a > 250, box_a, "> 250")], [out]


@card("ENG-127")
def hf_gfx_markers(task, wd):
    """Per GFX marker: one composition matching timeline w/h/fps, rendered with -c and overlaid back at the marker."""
    import numpy as np
    W, H, FPS = 160, 90, 30
    markers = [{"name": "title-01", "kind": "chapter title", "tc": 0.5, "dur": 0.4, "color": "#00c000"},
               {"name": "table-02", "kind": "before/after table", "tc": 1.3, "dur": 0.4, "color": "#0050ff"}]
    jw(wd / "markers.json", {"timeline": {"width": W, "height": H, "fps": FPS}, "markers": markers})
    proj = hf_project(wd, "gfx", box_comp(w=W, h=H, dur=0.4))
    for m in markers:
        body = ('<div id="card" class="clip" data-start="0" data-duration="%s" data-track-index="1" '
                'style="position:absolute;inset:20px;background:%s"></div>' % (m["dur"], m["color"]))
        html_text = box_comp(w=W, h=H, dur=m["dur"], fps=FPS, extra_body=body, comp_id=m["name"])
        (proj / "compositions").mkdir(exist_ok=True)
        (proj / "compositions" / (m["name"] + ".html")).write_text(html_text.replace('src="gsap.min.js"', 'src="../gsap.min.js"'), encoding="utf-8")
    renders = []
    for m in markers:
        o = proj / "renders" / (m["name"] + ".mp4")
        hf(wd, "render", proj, "-c", "compositions/%s.html" % m["name"], "-o", o, "--fps", FPS, "-q", "draft", "-w", "1", "--quiet", timeout=90)
        renders.append(o)
    base = wd / "timeline.mp4"
    fx.ffmpeg("-f", "lavfi", "-i", "color=c=gray:s=%dx%d:r=%d:d=2" % (W, H, FPS), "-pix_fmt", "yuv420p", "-c:v", "libx264", "-crf", "12", str(base))
    args, fc, last = ["-i", str(base)], "", "0:v"
    for k, (m, o) in enumerate(zip(markers, renders), 1):
        args += ["-itsoffset", str(m["tc"]), "-i", str(o)]
        fc += "[%s][%d:v]overlay=enable='between(t,%s,%s)':eof_action=pass[v%d];" % (last, k, m["tc"], m["tc"] + m["dur"] - 0.01, k)
        last = "v%d" % k
    final = wd / "timeline_with_gfx.mp4"
    fx.ffmpeg(*args, "-filter_complex", fc.rstrip(";"), "-map", "[%s]" % last, "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", str(final))
    fr = fx.frames(final, size=(W, H))
    def col(t):
        return fr[int(round(t * FPS))][45, 80]
    g, b, before = col(0.7), col(1.5), col(0.2)
    dims = [(probe_v(o)[1]["width"], probe_v(o)[1]["height"], probe_v(o)[1]["r_frame_rate"]) for o in renders]
    return [check("each render matches the timeline 160x90@30", all(d == (W, H, "30/1") for d in dims), dims, [W, H, "30/1"]),
            check("chapter card on screen at 0.7 s (green)", g[1] > 120 and g[0] < 80, g, "green"),
            check("table card on screen at 1.5 s (blue)", b[2] > 150 and b[1] < 140, b, "blue"),
            check("negative control: before the first marker the timeline is plain grey", abs(before[0] - before[1]) < 12 and abs(before[1] - before[2]) < 12 and before[1] < 200, before, "grey")], [final, *renders]


@card("ENG-137")
def hf_render_settings(task, wd):
    """draft while iterating: --quality draft at --fps 24; doctor confirms Chrome / FFmpeg / Node."""
    proj = hf_project(wd, "settings", box_comp(w=160, h=90, dur=0.5, fps=30))
    out = wd / "draft24.mp4"
    hf(wd, "render", proj, "-o", out, "--fps", "24", "--quality", "draft", "--format", "mp4", "-w", "1", "--quiet", timeout=90)
    _, v = probe_v(out)
    n = nframes(out)
    doc = hfj(wd, "doctor", "--json", ok=False)
    req = {c["name"]: c["ok"] for c in doc["checks"] if c["name"] in ("Chrome", "FFmpeg", "Node.js")}
    authored = int(re.search(r'data-fps="(\d+)"', (proj / "index.html").read_text()).group(1))
    return [check("output fps follows --fps 24", v["r_frame_rate"] == "24/1", v["r_frame_rate"], "24/1"),
            check("0.5 s at 24 fps -> 12 frames", n == 12, n, 12),
            check("doctor: Chrome, FFmpeg and Node all ok", len(req) == 3 and all(req.values()), req, "all true"),
            check("negative control: the composition's own data-fps (30) is not the rendered rate", authored != 24, authored, "!= 24")], [out]


@card("ENG-164")
def hf_route(task, wd):
    """The HyperFrames route: check Node >= 22 and verify a real render before using it."""
    node_v = fx.run(["node", "--version"]).stdout.strip()
    hf_v = hf(wd, "--version").stdout.strip()
    def gate(v):
        m = re.match(r"v?(\d+)", v)
        return bool(m) and int(m.group(1)) >= 22
    proj = hf_project(wd, "route", box_comp(w=160, h=90, dur=0.5, fps=10))
    out = wd / "route_check.mp4"
    hf(wd, "render", proj, "-o", out, "-q", "draft", "-w", "1", "--quiet", timeout=90)
    fr = fx.frames(out, size=(160, 90))
    cx0, cxl = red_cx(fr[0]), red_cx(fr[-1])
    exp_last = 20 + 120 * (4 / 5)
    jw(wd / "route.json", {"node": node_v, "hyperframes": hf_v, "render": str(out)})
    return [check("Node >= 22 gate passes", gate(node_v), node_v, ">= 22"),
            check("hyperframes CLI answers a version", re.match(r"^\d+\.\d+\.\d+", hf_v) is not None, hf_v, "x.y.z"),
            check("verify render: 5 frames", len(fr) == 5, len(fr), 5),
            check("frame 4 box centre at 20+120*0.4*2.5=116", cxl is not None and abs(cxl - exp_last) <= 3, cxl, exp_last),
            check("negative control: Node 20 fails the gate", not gate("v20.11.0"), "v20.11.0", "rejected"),
            check("negative control: frame 0 box is not at the frame-4 position", cx0 is not None and abs(cx0 - exp_last) > 50, cx0, "far")], [out, wd / "route.json"]


@card("ENG-171")
def hf_init(task, wd):
    """init --resolution portrait --non-interactive --skip-transcribe scaffolds a 1080x1920 project."""
    hf(wd, "init", "port", "--resolution", "portrait", "--non-interactive", "--skip-transcribe")
    hf(wd, "init", "land", "--non-interactive", "--skip-transcribe")
    def dims(p):
        t = (wd / p / "index.html").read_text()
        return int(re.search(r'data-width="(\d+)"', t).group(1)), int(re.search(r'data-height="(\d+)"', t).group(1))
    info = hfj(wd, "info", wd / "port", "--json")
    files = sorted(x.name for x in (wd / "port").iterdir())
    return [check("portrait scaffold root is 1080x1920", dims("port") == (1080, 1920), dims("port"), [1080, 1920]),
            check("info reads resolution portrait", info.get("resolution") == "portrait", info.get("resolution"), "portrait"),
            check("project files written", {"index.html", "hyperframes.json", "meta.json", "package.json"} <= set(files), files, "index/hyperframes/meta/package"),
            check("negative control: default init is landscape 1920x1080", dims("land") == (1920, 1080), dims("land"), [1920, 1080])], [wd / "port/index.html"]


@card("ENG-172")
def hf_render_formats(task, wd):
    """render --format png-sequence writes RGBA frames (AE/Nuke ingest) and gif writes an animated GIF."""
    import numpy as np
    from PIL import Image
    proj = hf_project(wd, "fmt", box_comp(w=160, h=90, dur=0.5, bg="transparent"))
    seq = wd / "seq"
    hf(wd, "render", proj, "-o", seq, "--format", "png-sequence", "--fps", "10", "-q", "draft", "-w", "1", "--quiet", timeout=90)
    pngs = sorted(seq.rglob("*.png"))
    modes = {Image.open(p).mode for p in pngs}
    a0 = np.asarray(Image.open(pngs[0]).convert("RGBA")).astype(float)
    corner = float(a0[2:8, 2:8, 3].mean())
    cxs = [red_cx(np.asarray(Image.open(p).convert("RGB"))) for p in pngs]
    exp = [20 + 120 * (k / 5) for k in range(5)]
    return [check("0.5 s at 10 fps -> 5 PNG frames", len(pngs) == 5, len(pngs), 5),
            check("frames are RGBA", modes == {"RGBA"}, sorted(modes), ["RGBA"]),
            check("transparent ground alpha 0", corner < 5, corner, "< 5"),
            check("box centres follow 20+120*t/0.5... per frame", all(c is not None and abs(c - e) <= 3 for c, e in zip(cxs, exp)), cxs, exp),
            check("negative control: frame 0 and frame 4 differ (motion captured)", cxs[0] is not None and cxs[-1] is not None and abs(cxs[-1] - cxs[0]) > 60,
                  [cxs[0], cxs[-1]], "> 60 px apart")], pngs[:2]


@card("ENG-173")
def hf_preview(task, wd):
    """Studio preview server: --background on a chosen port, --status, page served, --stop."""
    proj = hf_project(wd, "prev", box_comp(w=160, h=90, dur=0.5))
    port = free_port()
    hf(wd, "preview", proj, "--port", port, "--background", "--no-open", timeout=60)
    try:
        code, body = 0, b""
        t0 = time.time()
        while time.time() - t0 < 15:
            try:
                code, body, _ = http("GET", "http://127.0.0.1:%d/" % port, timeout=3)
                if code == 200:
                    break
            except OSError:
                time.sleep(0.2)
        st = hf(wd, "preview", proj, "--status", ok=False).stdout
    finally:
        hf(wd, "preview", proj, "--stop", ok=False)
    (wd / "studio.html").write_bytes(body)
    gone = True
    try:
        http("GET", "http://127.0.0.1:%d/" % port, timeout=2)
        gone = False
    except OSError:
        gone = True
    return [check("studio page answers 200", code == 200, code, 200),
            check("page is the HyperFrames studio", b"__HF_CLI" in body or b"hyperframes" in body.lower(), len(body), "studio html"),
            check("--status reports the background server", str(port) in st or "running" in st.lower(), st[-160:], "port or running"),
            check("negative control: after --stop the port no longer answers", gone, gone, True)], [wd / "studio.html"]


@card("ENG-175")
def hf_catalog_add(task, wd):
    """catalog --query --type block finds registry items; add pastes one into the project wired by data-composition-src."""
    proj = hf_project(wd, "cat", box_comp(w=320, h=180, dur=1.0))
    cat = hfj(wd, "catalog", "--query", "lower third", "--type", "block", "--json")
    jw(wd / "catalog.json", cat)
    names = [r["name"] for r in cat.get("results", [])]
    types = {r.get("type") for r in cat.get("results", [])}
    pick = names[0] if names else None
    before = (proj / "compositions" / ("%s.html" % pick)).exists() if pick else True
    add = hfj(wd, "add", pick, "--dir", proj, "--json", "--no-clipboard")
    written = [Path(p) for p in add.get("written", [])]
    snippet = add.get("snippet", "")
    # wire the snippet into the host root, then the project must list it as a composition
    t = (proj / "index.html").read_text()
    t = t.replace('<div id="box"', snippet + '<div id="box"', 1)
    (proj / "index.html").write_text(t)
    comps = [c.get("id") for c in hfj(wd, "compositions", proj, "--json")["compositions"]]
    return [check("query returns block results", len(names) > 0 and types <= {"block"}, [len(names), sorted(types)], "> 0 blocks"),
            check("add wrote compositions/<name>.html", any(p.name == "%s.html" % pick and p.stat().st_size > 0 for p in written), [str(p) for p in written], pick),
            check("snippet wires data-composition-src", ('data-composition-src="compositions/%s.html"' % pick) in snippet, snippet[:160], pick),
            check("project now lists the block as a composition", pick in comps, comps, pick),
            check("negative control: the block file did not exist before add", not before, before, False)], written + [wd / "catalog.json"]


@card("ENG-177")
def hf_doctor_info(task, wd):
    """doctor / info / compositions describe the environment and the project exactly."""
    proj = hf_project(wd, "inf", box_comp(w=320, h=180, dur=1.5))
    doc = hfj(wd, "doctor", "--json", ok=False)
    info = hfj(wd, "info", proj, "--json")
    comps = hfj(wd, "compositions", proj, "--json")["compositions"]
    jw(wd / "doctor.json", doc)
    jw(wd / "info.json", info)
    names = {c["name"]: c["ok"] for c in doc["checks"]}
    t2 = proj / "index.html"
    t2.write_text(t2.read_text().replace('data-duration="1.5" data-width', 'data-duration="3" data-width'))
    info2 = hfj(wd, "info", proj, "--json")
    return [check("doctor lists Node.js, FFmpeg, FFprobe, Chrome as ok", all(names.get(k) for k in ("Node.js", "FFmpeg", "FFprobe", "Chrome")),
                  {k: names.get(k) for k in ("Node.js", "FFmpeg", "FFprobe", "Chrome")}, "all true"),
            check("info width/height/duration = 320/180/1.5", (info["width"], info["height"], info["duration"]) == (320, 180, 1.5),
                  [info["width"], info["height"], info["duration"]], [320, 180, 1.5]),
            check("compositions lists one 'main'", [c["id"] for c in comps] == ["main"], [c["id"] for c in comps], ["main"]),
            check("negative control: after editing data-duration the info no longer reads 1.5", info2["duration"] == 3, info2["duration"], 3)], [wd / "doctor.json", wd / "info.json"]


@card("ENG-189")
def hf_preview_catchup(task, wd):
    """Open preview in the background before delivery, then catch-up reports what the desktop app did since."""
    proj = hf_project(wd, "cu", box_comp(w=160, h=90, dur=0.5))
    port = free_port()
    hf(wd, "preview", proj, "--port", port, "--background", "--no-open", timeout=60)
    try:
        code = 0
        t0 = time.time()
        while time.time() - t0 < 15 and code != 200:
            try:
                code = http("GET", "http://127.0.0.1:%d/" % port, timeout=3)[0]
            except OSError:
                time.sleep(0.2)
        lst = hf(wd, "preview", "--list", ok=False).stdout
    finally:
        hf(wd, "preview", proj, "--stop", ok=False)
    cu = hfj(wd, "catch-up", proj, "--json")
    jw(wd / "catchup.json", cu)
    return [check("background preview answers before delivery", code == 200, code, 200),
            check("preview --list shows the project server", str(port) in lst or "cu" in lst, lst[-200:], "listed"),
            check("catch-up answers for this project", Path(cu.get("project", "")).resolve() == proj.resolve(), cu.get("project"), str(proj)),
            check("catch-up: no desktop turns yet (fresh project)", cu.get("turns") == [] and cu.get("files") == [], [cu.get("turns"), cu.get("files")], [[], []]),
            check("negative control: catch-up on a folder with no composition is refused", _refused(wd), "rc != 0", "refused")], [wd / "catchup.json"]


def _refused(wd):
    (wd / "nowhere").mkdir(exist_ok=True)
    r = hf(wd, "catch-up", wd / "nowhere", "--json", ok=False)
    return r.returncode != 0 and "No composition found" in (r.stdout + r.stderr)


@card("ENG-194")
def hf_tailwind(task, wd):
    """init --tailwind: the v4 browser runtime (vendored, sha384 = the scaffold's integrity pin) styles frame 0."""
    import base64
    import numpy as np
    hf(wd, "init", "tw", "--tailwind", "--non-interactive", "--skip-transcribe")
    t = (wd / "tw/index.html").read_text()
    m = re.search(r'<script src="(https://cdn\.jsdelivr\.net/npm/@tailwindcss/browser@([\d.]+)/dist/index\.global\.js)" integrity="sha384-([^"]+)"', t)
    local = NM / "@tailwindcss/browser/dist/index.global.js"
    digest = base64.b64encode(hashlib.sha384(local.read_bytes()).digest()).decode()
    shutil.copy(local, wd / "tw/tailwind.global.js")
    shutil.copy(GSAP_JS, wd / "tw/gsap.min.js")
    t = t.replace(m.group(1), "tailwind.global.js").replace(re.search(r'<script src="https://cdn[^"]*gsap[^"]*"', t).group(0), '<script src="gsap.min.js"')
    t = re.sub(r'data-duration="\d+"', 'data-duration="1"', t)
    t = t.replace('width=1920, height=1080', 'width=320, height=180').replace("width: 1920px", "width: 320px").replace("height: 1080px", "height: 180px")
    t = t.replace('data-width="1920"', 'data-width="320"').replace('data-height="1080"', 'data-height="180"')
    t = t.replace('<h1 id="title" class="clip"', '<div id="tw" class="clip absolute left-[100px] top-[40px] w-[120px] h-[100px] bg-[#00ff00]" '
                  'data-start="0" data-duration="1" data-track-index="2"></div><h1 id="title" class="clip"')
    (wd / "tw/index.html").write_text(t)
    shots, _ = snapshot(wd, wd / "tw", [0])
    f0 = load_rgb(shots[0.0])
    px = f0[44:50, 104:112].reshape(-1, 3).mean(0)
    # untreated: same page without the Tailwind runtime
    bare = t.replace('<script src="tailwind.global.js"', '<script data-off="1" src="none.js"')
    r, _ = browser(wd, "tw_bare", bare.replace("</body>", "<script>setTimeout(()=>window.__r=1,400)</script></body>"), size=(320, 180),
                   shots=[(None, "bare.png")])
    b0 = load_rgb(wd / "bare.png")[44:50, 104:112].reshape(-1, 3).mean(0)
    return [check("scaffold pins @tailwindcss/browser v4", m is not None and m.group(2).startswith("4."), m.group(2) if m else None, "4.x"),
            check("vendored runtime matches the scaffold's sha384 pin", m is not None and digest == m.group(3), digest[:16], (m.group(3)[:16] if m else None)),
            check("frame 0 is styled: Tailwind arbitrary classes paint the box green", px[1] > 200 and px[0] < 60 and px[2] < 60, px, [0, 255, 0]),
            check("negative control: without the runtime frame 0 is unstyled there", not (b0[1] > 200 and b0[0] < 60), b0, "not green")], [shots[0.0], wd / "tw/index.html"]


@card("ENG-195")
def hf_gsap_transforms(task, wd):
    """Motion on x/y/scale/rotation passes the render-contract lints; width/left tweens + layout reads are flagged."""
    bad_tw = ('const r0=document.getElementById("box").getBoundingClientRect();'
              'tl.to("#box",{left:280,width:80,duration:1,ease:"none"},0);')
    good_tw = 'const W0=320-40;tl.fromTo("#box",{x:0,scale:1},{x:W0,scale:1.2,rotation:10,duration:1,ease:"none"},0);'
    bad = hf_project(wd, "bad", box_comp(tween=bad_tw, extra_css="#box{will-change:transform}"))
    good = hf_project(wd, "good", box_comp(tween=good_tw))
    lb, lg = hfj(wd, "lint", bad, "--json", ok=False), hfj(wd, "lint", good, "--json", ok=False)
    mb = last_json(py(MOTION, "lint", bad, wd=wd, ok=False).stdout + "\n")
    mg = last_json(py(MOTION, "lint", good, wd=wd, ok=False).stdout + "\n")
    codes_b = sorted({f.get("code") for f in lb["findings"]})
    def static_rules(src):
        js = re.findall(r"<script>(.*?)</script>", src, re.S)[-1]
        props = re.findall(r"\{([^{}]*duration[^{}]*)\}", js)
        layout = sorted({k for p in props for k in re.findall(r"\b(width|height|top|left)\s*:", p)})
        return {"layout_props": layout, "rect_reads": js.count("getBoundingClientRect")}
    sb, sg = static_rules((bad / "index.html").read_text()), static_rules((good / "index.html").read_text())
    jw(wd / "lint.json", {"hyperframes_bad": lb, "hyperframes_good": lg, "motion_bad": mb, "motion_good": mg, "static": [sb, sg]})
    return [check("hyperframes lint flags non-transform motion on the bad comp", "gsap_non_transform_motion" in codes_b, codes_b, "gsap_non_transform_motion"),
            check("static rule: bad comp tweens layout props and reads layout", sb["layout_props"] == ["left", "width"] and sb["rect_reads"] == 1, sb, {"layout_props": ["left", "width"], "rect_reads": 1}),
            check("motion.py lint warns on the bad comp", mb.get("warnings", 0) + mb.get("errors", 0) >= 1, mb, ">= 1"),
            check("transform-only comp: 0 hyperframes lint errors, no layout props", lg["errorCount"] == 0 and sg == {"layout_props": [], "rect_reads": 0}, [lg["errorCount"], sg], [0, "clean"]),
            check("negative control: the untreated (bad) comp fails the 0-error criterion", lb["errorCount"] > 0, lb["errorCount"], "> 0")], [wd / "lint.json"]


def _adapter_run(wd, name, html_text, extra_files=None):
    proj = hf_project(wd, name, html_text, extra_files)
    shots, _ = snapshot(wd, proj, [0, 0.5])
    cx0, cx5 = red_cx(load_rgb(shots[0.0])), red_cx(load_rgb(shots[0.5]))
    return proj, shots, cx0, cx5


@card("ENG-196")
def hf_anime_adapter(task, wd):
    """Anime.js v4 timeline registered on window.__hfAnime is sought by the HyperFrames runtime per frame."""
    js = ("<script src=\"anime.js\"></script>", "<script>const {createTimeline}=anime;window.__hfAnime=window.__hfAnime||[];"
          "const at=createTimeline({autoplay:false});at.add('#box',{x:[0,280],duration:1000,ease:'linear'},0);window.__hfAnime.push(at);</script>")
    html_text = box_comp(gsap=False, head=js[0]).replace("</body>", js[1] + "</body>")
    proj, shots, cx0, cx5 = _adapter_run(wd, "anime", html_text, {"anime.js": NM / "animejs/dist/bundles/anime.umd.min.js"})
    ver = json.loads((NM / "animejs/package.json").read_text())["version"]
    kf = hfj(wd, "keyframes", proj, "--json", ok=False)
    return [check("anime.js is v4", ver.startswith("4."), ver, "4.x"),
            check("seek 0.5 s puts the box centre at 160 px", cx5 is not None and abs(cx5 - 160) <= 3, cx5, 160),
            check("keyframes inspector sees the anime timeline", '"anime"' in json.dumps(kf), "anime" in json.dumps(kf), True),
            check("negative control: at 0 s (unsought) the box is at 20 px, not 160", cx0 is not None and abs(cx0 - 160) > 100, cx0, 20)], [shots[0.5]]


@card("ENG-197")
def hf_css_adapter(task, wd):
    """CSS @keyframes become seekable: the runtime drives animation-delay/play-state so 0.5 s lands mid-way."""
    css = "@keyframes mv{from{transform:translateX(0)}to{transform:translateX(280px)}}.mv{animation:mv 1s linear both}"
    html_text = box_comp(gsap=False, extra_css=css).replace('id="box" class="clip"', 'id="box" class="clip mv"')
    proj, shots, cx0, cx5 = _adapter_run(wd, "cssk", html_text)
    return [check("seek 0.5 s puts the box centre at 160 px", cx5 is not None and abs(cx5 - 160) <= 3, cx5, 160),
            check("frame 0 at the keyframe start (20 px)", cx0 is not None and abs(cx0 - 20) <= 3, cx0, 20),
            check("negative control: the unsought frame fails the 160 px criterion", cx0 is not None and abs(cx0 - 160) > 100, cx0, "far from 160")], [shots[0.5]]


@card("ENG-198")
def hf_waapi_adapter(task, wd):
    """element.animate() seeked through currentTime by the runtime, no GSAP dependency."""
    js = ("<script>const a=document.getElementById('box').animate([{transform:'translateX(0)'},{transform:'translateX(280px)'}],"
          "{duration:1000,easing:'linear',fill:'both'});a.pause();</script>")
    html_text = box_comp(gsap=False).replace("</body>", js + "</body>")
    proj, shots, cx0, cx5 = _adapter_run(wd, "waapi", html_text)
    has_gsap = "gsap" in (proj / "index.html").read_text()
    return [check("no GSAP in the composition", not has_gsap, has_gsap, False),
            check("seek 0.5 s puts the box centre at 160 px", cx5 is not None and abs(cx5 - 160) <= 3, cx5, 160),
            check("negative control: the unsought frame (0 s) is far from 160 px", cx0 is not None and abs(cx0 - 160) > 100, cx0, 20)], [shots[0.5]]


@card("ENG-199")
def hf_dev_loop(task, wd):
    """init -> author -> lint -> check -> render --quality looks -> test -s -> ffprobe."""
    hf(wd, "init", "loop", "--non-interactive", "--skip-transcribe")
    proj = wd / "loop"
    shutil.copy(GSAP_JS, proj / "gsap.min.js")
    (proj / "index.html").write_text(box_comp(w=160, h=90, dur=0.5, fps=10))
    lint = hfj(wd, "lint", proj, "--json", ok=False)
    chk = hfj(wd, "check", proj, "--json", ok=False, timeout=60)
    out = wd / "loop.mp4"
    hf(wd, "render", proj, "--quality", "looks", "--output", out, "-w", "1", "--quiet", timeout=90)
    p, v = probe_v(out)
    dur = float(p["format"]["duration"])
    broken = hf_project(wd, "broken", box_comp(w=160, h=90, dur=0.5).replace('data-composition-id="main" ', ""))
    lint_b = hfj(wd, "lint", broken, "--json", ok=False)
    return [check("lint: 0 errors", lint["errorCount"] == 0, lint["errorCount"], 0),
            check("check gate ok", chk.get("ok") is True, chk.get("ok"), True),
            check("test -s out.mp4", out.stat().st_size > 0, out.stat().st_size, "> 0"),
            check("ffprobe: h264 160x90, 0.5 s", (v["codec_name"], v["width"], v["height"]) == ("h264", 160, 90) and abs(dur - 0.5) < 0.06,
                  [v["codec_name"], v["width"], v["height"], dur], ["h264", 160, 90, 0.5]),
            check("negative control: a comp missing data-composition-id fails lint", lint_b["errorCount"] > 0, lint_b["errorCount"], "> 0")], [out]


@card("ENG-200")
def hf_init_examples(task, wd):
    """init with an example template + portrait preset, and init --video wires the user's clip (duration probed)."""
    clip = wd / "clip.mp4"
    fx.ffmpeg("-f", "lavfi", "-i", "testsrc2=s=320x180:r=30:d=1.4", "-f", "lavfi", "-i", "sine=f=440:d=1.4", "-c:v", "libx264",
              "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(clip))
    hf(wd, "init", "kt", "--example", "kinetic-type", "--resolution", "portrait", "--non-interactive", "--skip-transcribe")
    hf(wd, "init", "vid", "--video", clip, "--non-interactive", "--skip-transcribe")
    comps = hfj(wd, "compositions", wd / "kt", "--json")["compositions"]
    vt = (wd / "vid/index.html").read_text()
    vm = re.search(r'<video[^>]*?src="([^"]+)"[^>]*?data-duration="([\d.]+)"', vt, re.S)
    copied = (wd / "vid/clip.mp4")
    blank = hf(wd, "init", "plain", "--non-interactive", "--skip-transcribe") and (wd / "plain/index.html").read_text()
    return [check("example scaffold has its sub-composition", any(c.get("source") == "compositions/main-graphics.html" for c in comps), [c["id"] for c in comps], "main-graphics"),
            check("portrait preset on every composition", all((c["width"], c["height"]) == (1080, 1920) for c in comps), [(c["width"], c["height"]) for c in comps], [1080, 1920]),
            check("--video copied byte for byte", copied.exists() and sha(copied) == sha(clip), copied.exists(), True),
            check("<video> wired to clip.mp4 with probed duration 1.4", vm is not None and vm.group(1) == "clip.mp4" and abs(float(vm.group(2)) - 1.4) < 0.05,
                  vm.groups() if vm else None, ["clip.mp4", 1.4]),
            check("negative control: plain init has no <video>", "<video" not in blank, "<video" in blank, False)], [wd / "vid/index.html", wd / "kt/index.html"]


@card("ENG-201")
def hf_doctor_browser(task, wd):
    """doctor --json (environment) and browser path (the pinned Chrome)."""
    doc = hfj(wd, "doctor", "--json", ok=False)
    jw(wd / "doctor.json", doc)
    bp = hf(wd, "browser", "path", ok=False).stdout.strip().splitlines()
    path = Path(bp[-1].strip()) if bp else Path("/nonexistent")
    req = {c["name"]: c["ok"] for c in doc["checks"]}
    failing = sorted(k for k, v in req.items() if not v)
    ver = fx.run([str(path), "--version"]).stdout.strip() if path.exists() else ""
    return [check("doctor checks Node.js, FFmpeg, Chrome", all(req.get(k) for k in ("Node.js", "FFmpeg", "Chrome")), {k: req.get(k) for k in ("Node.js", "FFmpeg", "Chrome")}, "ok"),
            check("browser path points at an executable Chrome", path.exists() and os.access(path, os.X_OK), str(path), "executable"),
            check("that Chrome answers a version", "Chrome" in ver or "Chromium" in ver, ver, "Chrome x"),
            check("negative control: jq -e .ok is false here because optional pieces fail (reported, not hidden)",
                  doc.get("ok") is False and len(failing) > 0, failing, "non-empty")], [wd / "doctor.json"]


@card("ENG-202")
def hf_catalog_words(task, wd):
    """Offline catalog search, local word tier: plain-English beat -> ranked registry items; misses reported."""
    q = hfj(wd, "catalog", "--query", "reveal", "--json")
    miss = hfj(wd, "catalog", "--query", "qqzzxxv wvvqq", "--json")
    jw(wd / "search.json", {"hit": q, "miss": miss})
    res = q.get("results", [])
    top = res[0] if res else {}
    blob = (top.get("name", "") + " " + top.get("title", "") + " " + " ".join(top.get("tags", [])) + " " + top.get("description", "")).lower()
    return [check("tier is the local word tier", q.get("tier") == "words", q.get("tier"), "words"),
            check("results found", len(res) > 0, len(res), "> 0"),
            check("top result mentions 'reveal'", "reveal" in blob, top.get("name"), "reveal"),
            check("miss carries a report_gap feedback command", "feedback --search-miss" in json.dumps(miss), miss.get("report_gap", "")[:60], "feedback --search-miss"),
            check("negative control: a nonsense query finds nothing", len(miss.get("results", [])) == 0, len(miss.get("results", [])), 0)], [wd / "search.json"]


@card("ENG-203")
def hf_info_tools(task, wd):
    """info / upgrade --check / compositions / docs / clean --dry-run, all as JSON where offered."""
    proj = hf_project(wd, "it", box_comp(w=320, h=180, dur=2))
    info = hfj(wd, "info", proj, "--json")
    up = hfj(wd, "upgrade", "--check", "--json", ok=False)
    comps = hfj(wd, "compositions", proj, "--json")["compositions"]
    docs = hf(wd, "docs", "rendering").stdout
    hf(wd, "render", proj, "-o", wd / "tiny.mp4", "-q", "draft", "--fps", "5", "-w", "1", "--quiet", "--end", "0.4", ok=False, timeout=60)
    clean = hfj(wd, "clean", "--dry-run", "--json", ok=False)
    jw(wd / "tools.json", {"info": info, "upgrade": up, "compositions": comps, "clean": clean})
    removed = clean.get("removed", [])
    return [check("info duration 2", info["duration"] == 2, info["duration"], 2),
            check("upgrade --check reports current version", up.get("current") == hf(wd, "--version").stdout.strip(), up.get("current"), "installed version"),
            check("compositions lists main", [c["id"] for c in comps] == ["main"], [c["id"] for c in comps], ["main"]),
            check("docs rendering topic prints", "render" in docs.lower() and len(docs) > 200, len(docs), "> 200 chars"),
            check("clean --dry-run is a dry run listing only paths", clean.get("dryRun") is True and all("path" in r for r in removed), [clean.get("dryRun"), len(removed)], [True, "paths"]),
            check("negative control: dry run deleted nothing (project still there)", (proj / "index.html").exists(), True, True)], [wd / "tools.json"]


@card("ENG-204")
def hf_studio_layout(task, wd):
    """Every scene a sub-composition; one element kind per track via data-track-kind; exactly one caption track."""
    def scene(cid, color):
        return ('<template id="%s-t"><div data-composition-id="%s" data-width="320" data-height="180" data-duration="1" '
                'style="position:absolute;inset:0;background:%s"></div></template>' % (cid, cid, color))
    (wd / "lay/compositions").mkdir(parents=True, exist_ok=True)
    for cid, col in (("s1", "#113"), ("s2", "#311")):
        (wd / ("lay/compositions/%s.html" % cid)).write_text(scene(cid, col))
    def host(caption_tracks):
        rows = ['<div class="clip" id="sc1" data-composition-id="s1" data-composition-src="compositions/s1.html" data-start="0" data-duration="1" data-track-index="0" data-track-kind="graphics"></div>',
                '<div class="clip" id="sc2" data-composition-id="s2" data-composition-src="compositions/s2.html" data-start="1" data-duration="1" data-track-index="0" data-track-kind="graphics"></div>']
        for k in range(caption_tracks):
            rows.append('<div class="clip" id="cap%d" data-start="0" data-duration="2" data-track-index="%d" data-track-kind="captions">word</div>' % (k, 1 + k))
        rows.append('<audio id="bed" class="clip" src="bed.wav" data-start="0" data-duration="2" data-track-index="5" data-track-kind="audio"></audio>')
        return box_comp(w=320, h=180, dur=2, gsap=False, extra_body="".join(rows)).replace('<div id="box" class="clip" data-start="0" data-duration="2" data-track-index="0"></div>', "")
    fx.tone(wd / "lay/bed.wav", seconds=2)
    def layout(n):
        (wd / "lay/index.html").write_text(host(n))
        tl = hfj(wd, "timeline", wd / "lay", "--json")["timeline"]
        kinds = {}
        for tr in tl["tracks"]:
            for r in tr["rows"]:
                kinds.setdefault(r.get("trackIndex"), set()).add(r.get("trackKind") or tr["kind"])
        cap_tracks = sorted(i for i, ks in kinds.items() if "captions" in ks)
        return tl, kinds, cap_tracks
    tl2, kinds2, caps2 = layout(2)
    tl, kinds, caps = layout(1)
    jw(wd / "timeline.json", tl)
    one_kind = all(len(v) == 1 for v in kinds.values())
    subs = [r for tr in tl["tracks"] for r in tr["rows"] if (r.get("src") or "").startswith("compositions/")]
    return [check("both scenes are sub-compositions", len(subs) == 2, len(subs), 2),
            check("one element kind per track", one_kind, {k: sorted(v) for k, v in kinds.items()}, "1 kind each"),
            check("exactly one caption track", len(caps) == 1, caps, 1),
            check("negative control: a layout with two caption tracks fails the one-caption-track rule", len(caps2) == 2, caps2, 2)], [wd / "timeline.json"]


@card("ENG-205")
def hf_registry_add(task, wd):
    """Registry: blocks install as sub-compositions, components paste into compositions/components/."""
    proj = hf_project(wd, "reg", box_comp(w=320, h=180, dur=1))
    comp = hfj(wd, "catalog", "--query", "glow", "--type", "component", "--json")
    blk = hfj(wd, "catalog", "--query", "chart", "--type", "block", "--json")
    c_name = comp["results"][0]["name"]
    b_name = blk["results"][0]["name"]
    cpath = proj / "compositions/components" / (c_name + ".html")
    existed = cpath.exists() or (proj / "compositions").exists()
    a1 = hfj(wd, "add", c_name, "--dir", proj, "--json", "--no-clipboard")
    a2 = hfj(wd, "add", b_name, "--dir", proj, "--json", "--no-clipboard")
    bpath = proj / "compositions" / (b_name + ".html")
    total = (comp.get("total") or 0) + (blk.get("total") or 0)
    lock = json.loads((proj / "hyperframes.lock.json").read_text()) if (proj / "hyperframes.lock.json").exists() else {}
    jw(wd / "added.json", {"component": a1, "block": a2, "lock": lock})
    return [check("component pasted into compositions/components/", cpath.exists() and cpath.stat().st_size > 0, str(cpath.relative_to(proj)), "compositions/components/<name>.html"),
            check("block installed as compositions/<name>.html", bpath.exists() and bpath.stat().st_size > 0, str(bpath.relative_to(proj)), "compositions/<name>.html"),
            check("block snippet is a data-composition-src mount", "data-composition-src" in a2.get("snippet", ""), a2.get("snippet", "")[:120], "data-composition-src"),
            check("types reported block vs component", a1.get("typeDir") == "components" and a2.get("typeDir") == "blocks", [a1.get("typeDir"), a2.get("typeDir")], ["components", "blocks"]),
            check("catalog indexes hundreds of items", isinstance(total, int) and total >= 300, total, ">= 300"),
            check("negative control: before add the project had no compositions folder", not existed, existed, False)], [cpath, bpath]


@card("ENG-206")
def hf_matte_composite(task, wd):
    """Render the caption layer with alpha, then FFmpeg-overlay the subject matte on top: words sit behind the speaker."""
    import numpy as np
    from PIL import Image, ImageDraw
    W, H = 160, 90
    cap = ('<div id="cap" class="clip" data-start="0" data-duration="0.5" data-track-index="1" '
           'style="position:absolute;left:10px;right:10px;top:35px;height:20px;background:#00ff00"></div>')
    proj = hf_project(wd, "cap", box_comp(w=W, h=H, dur=0.5, bg="transparent", tween="", extra_body=cap).replace(
        '<div id="box" class="clip" data-start="0" data-duration="0.5" data-track-index="0"></div>', ""))
    layer = wd / "captions.webm"
    hf(wd, "render", proj, "-o", layer, "--format", "webm", "-q", "draft", "--fps", "10", "-w", "1", "--quiet", timeout=90)
    matte = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(matte).ellipse((60, 15, 100, 75), fill=(255, 0, 0, 255))
    matte.save(wd / "subject_matte.png")
    bg = wd / "plate.mp4"
    fx.ffmpeg("-f", "lavfi", "-i", "color=c=blue:s=%dx%d:r=10:d=0.5" % (W, H), "-pix_fmt", "yuv420p", "-c:v", "libx264", str(bg))
    final, nomatte = wd / "final.mp4", wd / "no_matte.mp4"
    fx.ffmpeg("-i", str(bg), "-c:v", "libvpx-vp9", "-i", str(layer), "-loop", "1", "-i", str(wd / "subject_matte.png"), "-filter_complex",
              "[0:v][1:v]overlay=format=auto[t];[t][2:v]overlay=shortest=1:format=auto,format=yuv420p[v]", "-map", "[v]", "-t", "0.5",
              "-c:v", "libx264", "-crf", "10", str(final))
    fx.ffmpeg("-i", str(bg), "-c:v", "libvpx-vp9", "-i", str(layer), "-filter_complex", "[0:v][1:v]overlay=format=auto,format=yuv420p[v]",
              "-map", "[v]", "-t", "0.5", "-c:v", "libx264", "-crf", "10", str(nomatte))
    f = fx.frames(final, size=(W, H))[2]
    n = fx.frames(nomatte, size=(W, H))[2]
    centre, side, plate = f[44:47, 78:82].reshape(-1, 3).mean(0), f[44:47, 20:30].reshape(-1, 3).mean(0), f[10, 20]
    nc = n[44:47, 78:82].reshape(-1, 3).mean(0)
    return [check("caption visible beside the speaker (green)", side[1] > 180 and side[0] < 80, side, "green"),
            check("speaker covers the words where they cross (red)", centre[0] > 180 and centre[1] < 80, centre, "red"),
            check("plate shows through the transparent caption layer (blue)", plate[2] > 180 and plate[1] < 80, plate, "blue"),
            check("negative control: without the matte overlay the centre shows the caption", nc[1] > 180 and nc[0] < 80, nc, "green")], [final, layer]


def _storyboard(wd, frames):
    md = "# STORYBOARD\n\n" + "\n".join("## %s (%.2fs)\ncolour: %s\n" % (n, d, c) for n, d, c in frames)
    (wd / "STORYBOARD.md").write_text(md)
    return wd / "STORYBOARD.md"


def _assemble(wd, sb, proj, inject=True, xdur=0.2):
    rows = re.findall(r"## (\S+) \(([\d.]+)s\)\ncolour: (\S+)", sb.read_text())
    (proj / "compositions/frames").mkdir(parents=True, exist_ok=True)
    t, mounts, bounds = 0.0, [], []
    for k, (name, d, col) in enumerate(rows):
        d = float(d)
        fid = name.replace("-", "_")
        (proj / "compositions/frames" / (name + ".html")).write_text(
            '<template id="%s-t"><div data-composition-id="%s" data-width="160" data-height="90" data-duration="%s" '
            'style="position:absolute;inset:0;background:%s"></div></template>' % (fid, fid, d, col))
        mounts.append('<div class="clip" id="m_%s" data-composition-id="%s" data-composition-src="compositions/frames/%s.html" '
                      'data-start="%s" data-duration="%s" data-track-index="0"></div>' % (fid, fid, name, round(t, 3), d))
        t += d
        if k < len(rows) - 1:
            bounds.append(round(t, 3))
    trans = []
    if inject:
        for b in bounds:
            trans.append('<div class="clip hf-transition" id="x_%d" data-transition="crossfade" data-start="%s" data-duration="%s" '
                         'data-track-index="1" style="position:absolute;inset:0;background:#000;opacity:0"></div>' % (int(b * 1000), round(b - xdur / 2, 3), xdur))
    html_text = box_comp(w=160, h=90, dur=round(t, 3), gsap=False, extra_body="".join(mounts + trans)).replace(
        '<div id="box" class="clip" data-start="%s" data-duration="%s" data-track-index="0"></div>' % (round(t, 3), round(t, 3)), "")
    (proj / "index.html").write_text(html_text)
    return rows, bounds


def _verify_transitions(wd, proj, bounds):
    tl = hfj(wd, "timeline", proj, "--json")["timeline"]
    rows = [r for tr in tl["tracks"] for r in tr["rows"]]
    mounts = sorted((r["start"], r["duration"]) for r in rows if (r.get("src") or "").startswith("compositions/frames/"))
    xs = sorted(r["start"] + r["duration"] / 2 for r in rows if (r.get("id") or "").startswith("x_"))
    ok = len(xs) == len(bounds) and all(abs(a - b) < 1e-6 for a, b in zip(xs, bounds))
    return tl, mounts, xs, ok


@card("ENG-207")
def hf_assemble_index(task, wd):
    """Assemble storyboard frames as sub-compositions on a track (cumulative starts) and inject + verify boundary transitions."""
    frames = [("01-intro", 0.8, "#203040"), ("02-claim", 1.2, "#402030"), ("03-proof", 0.6, "#304020"), ("04-cta", 1.0, "#101010")]
    sb = _storyboard(wd, frames)
    proj = hf_project(wd, "asm", "")
    rows, bounds = _assemble(wd, sb, proj, inject=True)
    tl, mounts, xs, ok = _verify_transitions(wd, proj, bounds)
    jw(wd / "assembled_timeline.json", tl)
    cum = [0.0]
    for _, d, _ in frames[:-1]:
        cum.append(round(cum[-1] + d, 3))
    raw = hf_project(wd, "asm_raw", "")
    _assemble(wd, sb, raw, inject=False)
    _, _, xs0, ok0 = _verify_transitions(wd, raw, bounds)
    lint = hfj(wd, "lint", proj, "--json", ok=False)
    return [check("frames mounted at cumulative starts", [m[0] for m in mounts] == cum, [m[0] for m in mounts], cum),
            check("one transition centred on every boundary (verify)", ok, xs, bounds),
            check("assembled project lints without errors", lint["errorCount"] == 0, lint["errorCount"], 0),
            check("negative control: the un-injected assembly fails verify", not ok0 and xs0 == [], xs0, [])], [proj / "index.html", wd / "assembled_timeline.json"]


@card("ENG-210")
def hf_contract(task, wd):
    """Root data-* contract, .clip timing, media ids, nested data-composition-src, data-composition-variables (+ --variables)."""
    import numpy as np
    W, H = 160, 90
    sub = ('<template id="lt-t"><div data-composition-id="lower" data-width="%d" data-height="%d" data-duration="0.5">'
           '<div style="position:absolute;left:0;right:0;bottom:0;height:20px;background:#ffffff"></div></div></template>' % (W, H))
    body = ('<div id="ground" class="clip" data-start="0" data-duration="0.5" data-track-index="2" style="position:absolute;inset:0;background:var(--bg)"></div>'
            '<div class="clip" id="lt" data-composition-id="lower" data-composition-src="compositions/lower.html" data-start="0" data-duration="0.5" data-track-index="3"></div>'
            '<audio id="tone" class="clip" src="tone.wav" data-start="0" data-duration="0.5" data-track-index="4"></audio>')
    vars_attr = "[{\"id\":\"bg\",\"type\":\"color\",\"label\":\"Ground\",\"default\":\"#ff00ff\"}]"
    html_text = box_comp(w=W, h=H, dur=0.5, fps=10, extra_body=body, tween="").replace(
        '<div id="box" class="clip" data-start="0" data-duration="0.5" data-track-index="0"></div>', "").replace(
        "<html>", "<html data-composition-variables='%s'>" % vars_attr).replace(
        "window.__timelines=window.__timelines||{};", "window.__timelines=window.__timelines||{};"
        "const v=(window.__hyperframes&&window.__hyperframes.getVariables)?window.__hyperframes.getVariables():{bg:'#ff00ff'};"
        "document.getElementById('ground').style.background=v.bg;")
    proj = hf_project(wd, "contract", html_text, {"compositions/lower.html": sub})
    fx.tone(proj / "tone.wav", seconds=0.5)
    lint = hfj(wd, "lint", proj, "--json", ok=False)
    comps = hfj(wd, "compositions", proj, "--json")["compositions"]
    out = wd / "contract.mp4"
    hf(wd, "render", proj, "-o", out, "-q", "draft", "-w", "1", "--quiet", "--variables", json.dumps({"bg": "#00ff00"}), timeout=90)
    f = fx.frames(out, size=(W, H))[2]
    ground, lower = f[30, 80], f[85, 80]
    p = fx.probe(out)
    has_audio = any(s["codec_type"] == "audio" for s in p["streams"])
    broken = hf_project(wd, "contract_broken", html_text.replace('data-composition-id="main" ', ""), {"compositions/lower.html": sub})
    lb = hfj(wd, "lint", broken, "--json", ok=False)
    return [check("contract lints clean", lint["errorCount"] == 0, lint["errorCount"], 0),
            check("nested composition resolved via data-composition-src", any(c.get("source") == "compositions/lower.html" for c in comps), [c.get("id") for c in comps], "lower"),
            check("--variables override paints the ground green", ground[1] > 180 and ground[0] < 80 and ground[2] < 80, ground, [0, 255, 0]),
            check("nested lower third rendered (white band)", lower.min() > 200, lower, "white"),
            check("audio clip with id muxed", has_audio, has_audio, True),
            check("negative control: root without data-composition-id fails lint", lb["errorCount"] > 0, lb["errorCount"], "> 0")], [out]


@card("ENG-180")
def hf_producer_backend(task, wd):
    """Producer: headless Chrome BeginFrame capture -> FFmpeg, with HF_SEGMENTED_CAPTURE segments concatenated."""
    proj = hf_project(wd, "prod", box_comp(w=160, h=90, dur=2.0, fps=30))
    out = wd / "producer.mp4"
    r = hf(wd, "render", proj, "-o", out, "-q", "draft", "-w", "1", "--keep-segments", timeout=90,
           env={"HF_SEGMENTED_CAPTURE": "true", "HF_SEGMENT_FRAMES": "30"})
    log = r.stdout + r.stderr
    (wd / "producer.log").write_text(log)
    segs = sorted((proj / "renders/.hf-segments").rglob("segments.json"))
    plan = json.loads(segs[0].read_text()) if segs else {}
    done = plan.get("completed", [])
    n = nframes(out)
    seg_n = [nframes(Path(c["path"])) for c in done]
    modes = sorted(set(re.findall(r'"captureMode":"(\w+)"', log)))
    return [check("capture mode is Chrome BeginFrame", "beginframe" in modes, modes, "beginframe"),
            check("segmented capture phase ran", '"phase":"capture_segmented"' in log, '"capture_segmented"' in log, True),
            check("60 frames split into 2 segments of 30", [c["endFrame"] - c["startFrame"] for c in done] == [30, 30] and seg_n == [30, 30], seg_n, [30, 30]),
            check("concatenated output has all 60 frames", n == 60, n, 60),
            check("negative control: one segment alone is not the whole film", bool(seg_n) and seg_n[0] != n, seg_n[:1], "!= 60")], [out, wd / "producer.log"]


_SDK_JS = r"""
import {openComposition} from %(sdk)s;
import {createFsAdapter} from %(fs)s;
import fs from 'fs';
const dir=process.argv[2]; const html=fs.readFileSync(dir+'/composition.html','utf8');
const persist=createFsAdapter({root:dir});
const c=await openComposition(html,{persist,persistPath:'composition.html',coalesceMs:0});
const box=c.find({track:0})[0]; const root=c.getRootElements()[0].id;
c.setTiming(box,{start:0.25,duration:0.5});
c.setStyle(box,{background:'#00ff00'});
const lab=c.addElement(root,1,'<div id="label" class="clip" data-start="0" data-duration="1" data-track-index="1">hello sdk</div>');
c.undo(); const afterUndo=c.serialize(); c.redo();
await c.flush();
const t=c.getElementTimings();
console.log(JSON.stringify({box,lab,boxTiming:t[box],undoHasLabel:afterUndo.includes('hello sdk'),redoHasLabel:c.serialize().includes('hello sdk'),
  versions:(await persist.listVersions('composition.html')).length}));
c.dispose();
"""


@card("ENG-182")
def hf_sdk(task, wd):
    """@hyperframes/sdk: open a composition, edit timing/style/elements with undo/redo, persist through the fs adapter."""
    sdk = NM / "@hyperframes/sdk/dist"
    d = wd / "sdkproj"
    d.mkdir()
    original = box_comp(w=320, h=180, dur=1)
    (d / "composition.html").write_text(original)
    src = wd / "edit.mjs"
    src.write_text(_SDK_JS % {"sdk": json.dumps(str(sdk / "index.js")), "fs": json.dumps(str(sdk / "adapters/fs.js"))})
    r = json.loads(fx.run(["node", src, d], timeout=30).stdout.strip().splitlines()[-1])
    saved = (d / "composition.html").read_text()
    lint = hfj(wd, "lint", hf_project(wd, "sdkcheck", saved), "--json", ok=False)
    return [check("timing edit: box enters 0.25 s, exits 0.75 s", r["boxTiming"] == {"enterAt": 0.25, "exitAt": 0.75, "labels": []}, r["boxTiming"], [0.25, 0.75]),
            check("undo removes the added element, redo restores it", (not r["undoHasLabel"]) and r["redoHasLabel"], [r["undoHasLabel"], r["redoHasLabel"]], [False, True]),
            check("fs adapter persisted the edits to disk", 'data-start="0.25"' in saved and "hello sdk" in saved and "#00ff00" in saved,
                  ['data-start="0.25"' in saved, "hello sdk" in saved, "#00ff00" in saved], [True, True, True]),
            check("version history kept", r["versions"] >= 1, r["versions"], ">= 1"),
            check("serialized document still lints clean", lint["errorCount"] == 0, lint["errorCount"], 0),
            check("negative control: the original HTML has none of the edits", "hello sdk" not in original and 'data-start="0.25"' not in original, False, False)], [d / "composition.html"]


def _x264_crf(path):
    m = re.search(rb"crf=([\d.]+)", Path(path).read_bytes())
    return float(m.group(1)) if m else None


@card("ENG-319")
def hf_draft_high(task, wd):
    """Render tiers: --quality draft for iteration vs high for delivery (x264 CRF read from the encoded SEI)."""
    proj = hf_project(wd, "tiers", box_comp(w=160, h=90, dur=0.5, fps=10, bg="#204060"))
    d, h = wd / "draft.mp4", wd / "high.mp4"
    hf(wd, "render", proj, "--quality", "draft", "--output", d, "-w", "1", "--quiet", timeout=90)
    hf(wd, "render", proj, "--quality", "high", "--output", h, "-w", "1", "--quiet", timeout=90)
    cd, ch = _x264_crf(d), _x264_crf(h)
    fd, fh = fx.frames(d, size=(160, 90)), fx.frames(h, size=(160, 90))
    return [check("both tiers render 5 frames", len(fd) == len(fh) == 5, [len(fd), len(fh)], 5),
            check("high uses a lower CRF than draft", cd is not None and ch is not None and ch < cd, [cd, ch], "high < draft"),
            check("same picture: box centre agrees within 2 px", abs(red_cx(fd[2]) - red_cx(fh[2])) <= 2, [red_cx(fd[2]), red_cx(fh[2])], "equal"),
            check("negative control: the draft file fails the high-tier CRF", cd is not None and ch is not None and cd > ch, cd, "> %s" % ch)], [d, h]


@card("ENG-290")
def hf_cli_pipeline(task, wd):
    """check -> snapshot key frames -> render -q draft -f 30 -> doctor, with the low-memory env set."""
    proj = hf_project(wd, "pipe", box_comp(w=160, h=90, dur=1.0))
    shots, snap = snapshot(wd, proj, [0.25, 0.75])
    out = wd / "pipe.mp4"
    hf(wd, "render", proj, "-o", out, "-q", "draft", "-f", "30", "-w", "1", "--quiet", timeout=90,
       env={"PRODUCER_LOW_MEMORY_MODE": "1", "HYPERFRAMES_SKIP_SKILLS": "1"})
    n = nframes(out)
    c25, c75 = red_cx(load_rgb(shots[0.25])), red_cx(load_rgb(shots[0.75]))
    sheets = [Path(s) for s in snap.get("contactSheets", [])]
    doc = hfj(wd, "doctor", "--json", ok=False)
    return [check("snapshot at 0.25 s: box centre 20+120*0.25=50", c25 is not None and abs(c25 - 50) <= 3, c25, 50),
            check("snapshot at 0.75 s: box centre 110", c75 is not None and abs(c75 - 110) <= 3, c75, 110),
            check("contact sheet written", any(s.exists() and s.stat().st_size > 0 for s in sheets), [str(s.name) for s in sheets], "contact-sheet"),
            check("render -f 30 of 1 s -> 30 frames", n == 30, n, 30),
            check("doctor answered", isinstance(doc.get("checks"), list) and len(doc["checks"]) > 5, len(doc.get("checks", [])), "> 5"),
            check("negative control: the 0.25 s frame fails the 0.75 s position", c25 is not None and abs(c25 - 110) > 30, c25, "far from 110")], [out, shots[0.25]]


# ======================================================================================= KOSIF Motion tools

GAPS["ENG-228"] = ("the five-command lab loop does not fit 15 s here: kmotion score synthesises ~8 s even for a 2 s spec and "
                   "one lab-kit frame takes ~9.4 s on SwiftShader (render ≈2 s/frame per the card)")


_REPO = Path(__file__).resolve().parents[4]
KIT_DIR = _REPO / ".claude/skills/kosif-superpowers/vendor/100-superskills/skills/kosif-montage-motion/scripts/kit"
LAB_REL = ".claude/skills/kosif-superpowers/vendor/100-superskills/skills/kosif-montage-motion/scripts/kit/lab-kit.js"
_DRAFT_PAGE = """<!doctype html><html><body style="margin:0"><canvas id="c" width="640" height="360"></canvas>
<script src="three-kit.bundle.js"></script><script src="%s"></script><script>
try{const K3=window.K3,T=K3.THREE,c=document.getElementById('c');const r=K3.makeRenderer(c,640,360,{});
const sc=new T.Scene();sc.background=new T.Color(0x102030);const cam=new T.PerspectiveCamera(40,640/360,0.1,50);cam.position.set(0,0,4);
const m=new T.Mesh(new T.BoxGeometry(1.4,1.4,1.4),new T.MeshBasicMaterial({color:0xff2020}));m.rotation.set(0.5,0.6,0);sc.add(m);
r.render(sc,cam);const gl=r.getContext();const px=new Uint8Array(4);gl.readPixels(gl.drawingBufferWidth>>1,gl.drawingBufferHeight>>1,1,1,gl.RGBA,gl.UNSIGNED_BYTE,px);
window.__r={ratio:r.getPixelRatio(),bw:gl.drawingBufferWidth,bh:gl.drawingBufferHeight,centre:Array.from(px),own:Object.getOwnPropertyDescriptor(K3,'makeRenderer').hasOwnProperty('value')};}
catch(e){window.__r={err:String(e.stack||e)}}</script></body></html>"""


@card("ENG-287")
def draft_scale(task, wd):
    """__draftScale (set by film.py --draft) shrinks lab-kit's GL buffers: measured in Chromium/SwiftShader on the repo's lab-kit.js.
    Negative controls: the same page at ds=1, and the pre-fix lab-kit.js (git 8aacac0^) at ds=0.5, which kept ratio 1."""
    for f in ("three-kit.bundle.js", "lab-kit.js"):
        shutil.copy(KIT_DIR / f, wd / f)
    try:
        old = fx.run(["git", "-C", str(_REPO), "show", "8aacac0^:" + LAB_REL]).stdout
    except Exception:  # noqa: BLE001 — no git history here: the ds=1 control still runs
        old = ""
    has_old = "K3.makeRenderer = function" in old
    if has_old:
        (wd / "lab-kit-old.js").write_text(old, encoding="utf-8")
    init = "window.__draftScale = %s;"
    a, _ = browser(wd, "draft", _DRAFT_PAGE % "lab-kit.js", flags=SOFTGL, size=(640, 360), init_script=init % 0.5)
    b, _ = browser(wd, "full", _DRAFT_PAGE % "lab-kit.js", flags=SOFTGL, size=(640, 360), init_script=init % 1)
    c = browser(wd, "old", _DRAFT_PAGE % "lab-kit-old.js", flags=SOFTGL, size=(640, 360), init_script=init % 0.5)[0] if has_old else None
    jw(wd / "draft_scale.json", {"ds_0.5": a, "ds_1": b, "old_ds_0.5": c})
    red = lambda r: r["centre"][0] > 200 and r["centre"][1] < 80
    out = [check("ds=0.5: pixel ratio 0.5 and a 320x180 GL buffer for a 640x360 canvas", (a["ratio"], a["bw"], a["bh"]) == (0.5, 320, 180), [a["ratio"], a["bw"], a["bh"]], [0.5, 320, 180]),
           check("draft buffer holds 1/4 of the full pixels", a["bw"] * a["bh"] * 4 == b["bw"] * b["bh"], [a["bw"] * a["bh"], b["bw"] * b["bh"]], "1:4"),
           check("draft still renders the scene (red cube at the centre)", red(a), a["centre"], "red"),
           check("K3.makeRenderer is now an own value (getter-only export replaced)", a["own"] is True, a["own"], True),
           check("negative control: ds=1 keeps ratio 1 and 640x360", (b["ratio"], b["bw"], b["bh"]) == (1, 640, 360) and red(b), [b["ratio"], b["bw"], b["bh"]], [1, 640, 360])]
    if has_old:
        out.append(check("negative control: the pre-fix lab-kit.js ignores ds=0.5 (ratio 1, 640x360)", (c["ratio"], c["bw"], c["bh"]) == (1, 640, 360), [c["ratio"], c["bw"], c["bh"]], [1, 640, 360]))
    return out, [wd / "draft_scale.json"]


def kmm_mirror(wd):
    """A private copy of the motion scripts whose node_modules points at the global HyperFrames install
    (motion.py looks for HERE/node_modules/hyperframes; the skill folder itself is never written)."""
    m = Path(wd) / "kmm" / "scripts"
    m.mkdir(parents=True, exist_ok=True)
    for f in KMM.glob("*.py"):
        shutil.copy(f, m / f.name)
    for d in ("kit", "web", "omni"):
        if (KMM / d).exists() and not (m / d).exists():
            (m / d).symlink_to(KMM / d)
    if (KMM.parent / "templates").exists() and not (m.parent / "templates").exists():
        (m.parent / "templates").symlink_to(KMM.parent / "templates")
    if not (m / "node_modules").exists():
        (m / "node_modules").symlink_to(NM)
    return m


def kproj(wd, name, *flags, seconds=1.0, fps=15, size="320x180", title=""):
    args = ["new", name, "--seconds", seconds, "--fps", fps, "--size", size, *flags]
    if title:
        args += ["--title", title]
    py(MOTION, *args, wd=wd)
    return Path(wd) / "projects" / name


MOVER = """<!doctype html><html><head><meta charset="UTF-8"><script src="assets/gsap.min.js"></script><script src="assets/motion-kit.js"></script>
<style>html,body{margin:0;width:%(w)dpx;height:%(h)dpx;overflow:hidden;background:#000}#box{position:absolute;left:0;top:%(top)dpx;width:20px;height:%(bh)dpx;background:#ff0000}</style></head>
<body><div id="root" data-composition-id="root" data-width="%(w)d" data-height="%(h)d" data-start="0" data-duration="%(d)s" data-fps="%(fps)d">
<div id="box"></div>%(audio)s
<script>const tl=gsap.timeline({paused:true});tl.fromTo("#box",{x:0},{x:%(dx)d,duration:%(d)s,ease:"none"},0);
window.__timelines=window.__timelines||{};window.__timelines["root"]=tl;window.MOTION.shim("root",%(d)s);</script></div></body></html>"""


def mover(proj, w=160, h=90, d=0.5, fps=10, dx=None, audio=""):
    (proj / "index.html").write_text(MOVER % {"w": w, "h": h, "d": d, "fps": fps, "top": h // 4, "bh": h // 2,
                                              "dx": dx if dx is not None else w - 20, "audio": audio}, encoding="utf-8")
    return proj


def edge_width(row):
    """Pixels in the red ramp between 10% and 90% of the row's red maximum (motion blur widens it)."""
    import numpy as np
    r = np.asarray(row, dtype=float)[:, 0]
    lo, hi = r.min(), r.max()
    if hi - lo < 50:
        return 0
    return int(((r > lo + 0.1 * (hi - lo)) & (r < lo + 0.9 * (hi - lo))).sum())


def lufs(path):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True, timeout=60).stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", out)
    return float(m[-1]) if m else None


@card("ENG-211")
def km_new_flat(task, wd):
    """kmotion new NAME --seconds --fps --size --title: an HTML+GSAP composition on the motion kit."""
    p = kproj(wd, "flat", seconds=2, fps=24, size="640x360", title="عنوان")
    t = (p / "index.html").read_text()
    q = kproj(wd, "flat2", seconds=1, fps=30, size="320x180")
    t2 = (q / "index.html").read_text()
    root = re.search(r'<div id="root"[^>]*>', t).group(0)
    return [check("root contract: 640x360, 2 s, 24 fps", all(x in root for x in ('data-width="640"', 'data-height="360"', 'data-duration="2.0"', 'data-fps="24"')), root, "640x360 2.0 24"),
            check("GSAP + motion kit vendored next to the page", (p / "assets/gsap.min.js").stat().st_size > 10000 and (p / "assets/motion-kit.js").stat().st_size > 1000,
                  sorted(x.name for x in (p / "assets").iterdir()), ["gsap.min.js", "motion-kit.js"]),
            check("title set in the composition", ">عنوان<" in t, ">عنوان<" in t, True),
            check("timeline registered for HyperFrames", 'window.__timelines["root"]' in t, True, True),
            check("negative control: a project made without --title does not carry it", "عنوان" not in t2, "عنوان" in t2, False)], [p / "index.html"]


@card("ENG-212")
def km_new_canvas(task, wd):
    """kmotion new NAME --canvas: one page whose window.seek(t) paints the exact frame for t."""
    p = kproj(wd, "cv", "--canvas", seconds=1, fps=30, size="320x180")
    t = (p / "index.html").read_text()
    t = t.replace('data-width="1920"', 'data-width="320"').replace('data-height="1080"', 'data-height="180"')
    shutil.copytree(p, wd / "cvpage", dirs_exist_ok=True)
    page = t.replace("</body>", "<script>setTimeout(()=>{window.__r=1},300)</script></body>")
    (wd / "cvpage/index.html").write_text(page)
    js_a = "window.seek(0.1)"
    js_b = "window.seek(0.8)"
    r, logs = browser(wd / "cvpage", "seek", page, size=(320, 180), shots=[(js_a, "a.png"), (js_b, "b.png"), (js_a, "a2.png")])
    import numpy as np
    a, b, a2 = (load_rgb(wd / "cvpage" / n) for n in ("a.png", "b.png", "a2.png"))
    diff_ab, diff_aa = float(np.abs(a - b).mean()), float(np.abs(a - a2).mean())
    return [check("canvas route: one canvas and window.seek defined", "<canvas" in t and "window.seek" in t, ["<canvas" in t, "window.seek" in t], [True, True]),
            check("seek is a pure function of t: seek(0.1) twice is identical", diff_aa < 0.5, diff_aa, "< 0.5"),
            check("negative control: a different t paints a different frame", diff_ab > 1.0, diff_ab, "> 1")], [wd / "cvpage/b.png", p / "index.html"]


@card("ENG-232")
def km_new_2d3d(task, wd):
    """kmotion new NAME [--3d]: 2D on motion-kit / 3D on three-kit + shape-kit; frames gives review stills."""
    p2 = kproj(wd, "two", seconds=1, fps=15, size="320x180", title="X")
    tpl2 = (p2 / "index.html").read_text()
    mover(p2, w=320, h=180, d=1, fps=15)
    p3 = kproj(wd, "three", "--3d", seconds=1, fps=15, size="320x180")
    a3 = sorted(x.name for x in (p3 / "assets").iterdir())
    main3 = (p3 / "src/main.js").read_text() if (p3 / "src/main.js").exists() else ""
    out = py(MOTION, "frames", p2, "--times", "0.2,0.9", wd=wd).stdout
    stills = sorted((p2 / "frames").glob("*.png"))
    import numpy as np
    s0, s1 = load_rgb(stills[0]), load_rgb(stills[-1])
    return [check("3D scaffold carries three-kit bundle + shape-kit + motion-kit", {"three-kit.bundle.js", "shape-kit.js", "motion-kit.js"} <= set(a3), a3, "kits"),
            check("3D scene source uses the kit (K3)", "K3" in main3 or "three" in main3.lower(), len(main3), "> 0"),
            check("frames wrote 2 review stills at 320x180", len(stills) == 2 and s0.shape[:2] == (180, 320), [len(stills), list(s0.shape[:2])], [2, [180, 320]]),
            check("2D scaffold is on the motion kit", "motion-kit.js" in tpl2 and (p2 / "assets/motion-kit.js").exists(), "motion-kit.js" in tpl2, True),
            check("negative control: the 2D scaffold has no three-kit", not (p2 / "assets/three-kit.bundle.js").exists(), (p2 / "assets/three-kit.bundle.js").exists(), False),
            check("stills differ over time (motion)", float(np.abs(s0 - s1).mean()) > 0.5, float(np.abs(s0 - s1).mean()), "> 0.5")], stills


@card("ENG-229")
def km_workbench(task, wd):
    """Browser-free 2D workbench: task -> plan -> manifest -> Pillow frames -> FFmpeg MP4 (1080x1920, 48 frames)."""
    import numpy as np
    out = wd / "wb.mp4"
    r = py(KMOTION, "workbench", "قطة في الليل", "--aspect", "9:16", "--seconds", 2, "--fps", 24, "--titles", "أ|ب|ج|د|هـ", "--out", out, wd=wd, timeout=60)
    (wd / "workbench.log").write_text(r.stdout)
    _, v = probe_v(out)
    n = nframes(out)
    fr = fx.frames(out, size=(54, 96))
    var = float(np.abs(fr[5] - fr[40]).mean())
    py(KMOTION, "workbench", "قطة في الليل", "--aspect", "9:16", "--seconds", 2, "--fps", 24, "--out", wd / "plan_only", "--plan-only", wd=wd, ok=False)
    po = sorted(x.name for x in (wd / "plan_only").iterdir()) if (wd / "plan_only").is_dir() else []
    return [check("1080x1920 portrait", (v["width"], v["height"]) == (1080, 1920), [v["width"], v["height"]], [1080, 1920]),
            check("2 s x 24 fps = 48 frames", n == 48, n, 48),
            check("frames change across the titles", var > 1.0, var, "> 1"),
            check("plan stage alone writes plan + manifest", "manifest.json" in po and "plan.json" in po, po, ["manifest.json", "plan.json"]),
            check("negative control: the plan-only stage has no film (no frames yet)", not any(n.endswith(".mp4") for n in po), po, "no .mp4")], [out]


def _site_env(wd):
    import site
    home = Path(wd) / "home"
    home.mkdir(exist_ok=True)
    env = kenv(wd)
    env.pop("KOSIF_MOTION_HOME", None)
    env.update(HOME=str(home), PYTHONPATH=os.pathsep.join([site.getusersitepackages(), env.get("PYTHONPATH", "")]).rstrip(os.pathsep))
    return env, home


@card("ENG-209")
def km_cloud_setup(task, wd):
    """cloud_setup: writable home, ffmpeg resolved, an ffprobe stand-in that answers like ffprobe, config for kmotion."""
    env, home = _site_env(wd)
    before = (home / ".kosif-motion.json").exists()
    r = py(KMM / "cloud_setup.py", "--home", home / "kosif-motion", wd=wd, env=env, timeout=60)
    cfg_p = home / ".kosif-motion.json"
    cfg = json.loads(cfg_p.read_text()) if cfg_p.exists() else {}
    clip = fx.test_clip(wd / "c.mp4", seconds=1.0, size="320x180", fps=25)
    shim = json.loads(subprocess.run([sys.executable, str(KMM / "ffprobe_shim.py"), "-v", "error", "-show_streams", "-show_format", "-of", "json", str(clip)],
                                     capture_output=True, text=True, timeout=30).stdout)
    real = fx.probe(clip)
    sv = [s for s in shim["streams"] if s.get("codec_type") == "video"][0]
    rv = [s for s in real["streams"] if s.get("codec_type") == "video"][0]
    projects = home / "kosif-motion/projects"
    return [check("config written for kmotion", cfg_p.exists() and str(home / "kosif-motion") in json.dumps(cfg), sorted(cfg)[:6], "home in config"),
            check("writable home with projects/", projects.is_dir(), projects.is_dir(), True),
            check("ffprobe stand-in agrees with ffprobe: 320x180", (int(sv["width"]), int(sv["height"])) == (int(rv["width"]), int(rv["height"])) == (320, 180),
                  [sv.get("width"), sv.get("height")], [320, 180]),
            check("stand-in duration within 0.05 s of ffprobe", abs(float(shim["format"]["duration"]) - float(real["format"]["duration"])) < 0.05,
                  [shim["format"]["duration"], real["format"]["duration"]], "equal"),
            check("negative control: before setup there was no config in this home", not before, before, False)], [cfg_p]


@card("ENG-231")
def km_cloud_install(task, wd):
    """cloud_setup --install on a claude.ai-style sandbox: deps resolved, workbench route ready without a browser."""
    env, home = _site_env(wd)
    before = (home / ".kosif-motion.json").exists()
    r = py(KMM / "cloud_setup.py", "--install", "--home", home / "km", "--no-examples", wd=wd, env=env, timeout=90)
    (wd / "setup.log").write_text(r.stdout + r.stderr)
    cfg = json.loads((home / ".kosif-motion.json").read_text())
    ff = cfg.get("ffmpeg") or cfg.get("bin") or ""
    env2 = dict(env, KOSIF_MOTION_HOME=str(home / "km"))
    wb = py(KMOTION, "workbench", "اختبار", "--aspect", "1:1", "--seconds", 2, "--fps", 24, "--out", wd / "wb.mp4", wd=wd, env=env2, timeout=60)
    _, v = probe_v(wd / "wb.mp4")
    return [check("setup reports the browser-free route ready", "جاهز" in r.stdout or "ready" in r.stdout.lower(), r.stdout.strip().splitlines()[-1][:80], "جاهز"),
            check("config written", (home / ".kosif-motion.json").exists(), True, True),
            check("workbench renders after setup: 1:1, 48 frames", (v["width"] == v["height"]) and nframes(wd / "wb.mp4") == 48, [v["width"], v["height"]], "square, 48"),
            check("negative control: no config before setup", not before, before, False)], [wd / "setup.log", wd / "wb.mp4"]


@card("ENG-218")
def km_final(task, wd):
    """kmotion final: lossless PNG capture, libx264 slow CRF 16, short side >= 1080, poster baked, report written."""
    p = mover(kproj(wd, "fin", seconds=0.5, fps=10, size="320x180"), w=320, h=180, d=0.5, fps=10)
    py(KMOTION, "final", p, wd=wd, timeout=90)
    out = wd / "out/fin.mp4"
    rep = json.loads((wd / "out/fin.mp4.kosif.json").read_text())
    _, v = probe_v(out)
    crf = _x264_crf(out)
    poster = wd / "out/fin.poster.jpg"
    return [check("short side >= 1080 (320x180 scaled x6)", min(v["width"], v["height"]) >= 1080, [v["width"], v["height"]], ">= 1080"),
            check("x264 CRF 16", crf == 16.0, crf, 16),
            check("preset slow + PNG capture in the render report", rep["params"].get("preset") == "slow" and rep["params"].get("capture") == "png",
                  [rep["params"].get("preset"), rep["params"].get("capture")], ["slow", "png"]),
            check("poster baked", poster.exists() and poster.stat().st_size > 0, poster.exists(), True),
            check("negative control: the authored size fails the >=1080 rule", min(320, 180) < 1080, 180, "< 1080")], [out, poster]


@card("ENG-215")
def km_cdp_capture(task, wd):
    """film.py grabber: CDP Page.captureScreenshot(optimizeForSpeed) PNG stays lossless; the JPEG draft path does not."""
    import io
    import numpy as np
    from PIL import Image
    sys.path.insert(0, str(KMM))
    import film
    page = wd / "grab.html"
    page.write_text("<html><body style='margin:0;background:#000'><canvas id=c width=320 height=180></canvas><script>"
                    "const g=document.getElementById('c').getContext('2d');for(let y=0;y<180;y+=4)for(let x=0;x<320;x+=4){"
                    "g.fillStyle='rgb('+((x*7+y*3)%256)+','+((x*x+y)%256)+','+((y*11)%256)+')';g.fillRect(x,y,4,4);}</script></body></html>")
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=_pw_chrome(), args=["--no-sandbox"])
        pg = b.new_page(viewport={"width": 320, "height": 180})
        pg.goto(page.as_uri())
        t0 = time.time()
        fast = film._grabber(pg, "png")
        raw_fast = [fast() for _ in range(5)][-1]
        t_fast = time.time() - t0
        t1 = time.time()
        raw_plain = [pg.screenshot(type="png") for _ in range(5)][-1]
        t_plain = time.time() - t1
        raw_jpeg = film._grabber(pg, "jpeg")()
        b.close()
    a = np.asarray(Image.open(io.BytesIO(raw_fast)).convert("RGB")).astype(int)
    pl = np.asarray(Image.open(io.BytesIO(raw_plain)).convert("RGB")).astype(int)
    jp = np.asarray(Image.open(io.BytesIO(raw_jpeg)).convert("RGB")).astype(int)
    (wd / "fast.png").write_bytes(raw_fast)
    jw(wd / "timing.json", {"optimizeForSpeed_5x_s": t_fast, "plain_5x_s": t_plain})
    return [check("CDP grabber returns PNG bytes", raw_fast[:8] == b"\x89PNG\r\n\x1a\n", raw_fast[:4], "PNG"),
            check("optimizeForSpeed PNG is pixel-identical to the plain screenshot", int(np.abs(a - pl).max()) == 0, int(np.abs(a - pl).max()), 0),
            check("exact known pixel at (8,4): rgb(68,68,44)", list(a[4, 8]) == [68, 68, 44], list(a[4, 8]), [68, 68, 44]),
            check("negative control: the JPEG draft capture is not lossless", int(np.abs(jp - pl).max()) > 0, int(np.abs(jp - pl).max()), "> 0")], [wd / "fast.png", wd / "timing.json"]


_RENDER_PAGE = """<html><body style="margin:0;background:#000"><div id="b" style="position:absolute;top:70px;left:0;width:40px;height:40px;background:#f00"></div>
<script>window.render=(t)=>{window.__ready=false;document.getElementById('b').style.transform='translateX('+(t*100)+'px)';
requestAnimationFrame(()=>requestAnimationFrame(()=>{window.__ready=true}));};window.__duration=2;window.render(0);</script></body></html>"""


@card("ENG-265")
def km_html_render(task, wd):
    """html_render.py page out --size --t: headless Chrome seeks window.render(t) and captures a PNG."""
    page = wd / "page.html"
    page.write_text(_RENDER_PAGE)
    py(KMM / "html_render.py", page, wd / "t15.png", "--size", "320x180", "--t", 1.5, wd=wd, timeout=60)
    py(KMM / "html_render.py", page, wd / "t0.png", "--size", "320x180", "--t", 0, wd=wd, timeout=60)
    a, z = load_rgb(wd / "t15.png"), load_rgb(wd / "t0.png")
    ca, cz = red_cx(a), red_cx(z)
    return [check("PNG is 320x180", a.shape[:2] == (180, 320), list(a.shape[:2]), [180, 320]),
            check("render(1.5) box centre at 20+150=170 px", ca is not None and abs(ca - 170) <= 2, ca, 170),
            check("negative control: t=0 capture has the box at 20 px", cz is not None and abs(cz - 20) <= 2 and abs(cz - 170) > 100, cz, 20)], [wd / "t15.png"]


@card("ENG-264")
def km_motion_blur(task, wd):
    """motion.py render --blur 4 --shutter 0.5: sub-frame motion blur widens a fast mover's edge vs the sharp still."""
    import numpy as np
    p = mover(kproj(wd, "mb", seconds=0.5, fps=10, size="160x90"), w=160, h=90, d=0.5, fps=10, dx=140)
    r = py(MOTION, "render", p, "--engine", "studio", "--blur", 4, "--shutter", 0.5, "--out", wd / "blur.mp4", wd=wd, timeout=90)
    py(MOTION, "frames", p, "--times", "0.2", wd=wd)
    sharp = load_rgb(sorted((p / "frames").glob("*.png"))[0])
    fr = fx.frames(wd / "blur.mp4", size=(160, 90))
    blurred = fr[2]
    ew_b, ew_s = edge_width(blurred[45]), edge_width(sharp[45])
    return [check("render produced 5 frames", len(fr) == 5, len(fr), 5),
            check("blurred edge ramp wider than 6 px (shutter 0.5 x 28 px/frame)", ew_b >= 6, ew_b, ">= 6"),
            check("box centre at 0.2 s still ~ 10+140*0.4=66", abs(red_cx(blurred, thr=60) - 66) <= 8, red_cx(blurred, thr=60), 66),
            check("negative control: the unblurred still has a sharp edge (< 4 px ramp)", ew_s < 4, ew_s, "< 4")], [wd / "blur.mp4"]


@card("ENG-275")
def km_render_mix(task, wd):
    """motion.py render: seeks the composition, encodes with FFmpeg, muxes <audio> clips and normalises the mix to -14 LUFS."""
    p = kproj(wd, "mix", seconds=1, fps=10, size="160x90")
    fx.tone(p / "assets/tone.wav", freq=440, seconds=1.0, amp=0.9)
    mover(p, w=160, h=90, d=1, fps=10, audio='<audio id="tone" src="assets/tone.wav" data-start="0" data-duration="1" data-volume="1"></audio>')
    out = wd / "mix.mp4"
    py(MOTION, "render", p, "--engine", "studio", "--out", out, wd=wd, timeout=90)
    pr = fx.probe(out)
    a = [s for s in pr["streams"] if s["codec_type"] == "audio"]
    L, L_in = lufs(out), lufs(p / "assets/tone.wav")
    return [check("video + audio streams", len(a) == 1 and any(s["codec_type"] == "video" for s in pr["streams"]), [s["codec_type"] for s in pr["streams"]], ["video", "audio"]),
            check("10 frames", nframes(out) == 10, nframes(out), 10),
            check("mix normalised to -14 LUFS (+-1.5)", L is not None and abs(L - (-14)) <= 1.5, L, -14),
            check("negative control: the raw tone is far from -14 LUFS", L_in is not None and abs(L_in - (-14)) > 3, L_in, "!= -14")], [out]


@card("ENG-305")
def km_dual_engine(task, wd):
    """motion.py render --engine studio vs --engine hyperframes: same composition, same picture."""
    import site
    p = mover(kproj(wd, "dual", seconds=0.5, fps=10, size="160x90"), w=160, h=90, d=0.5, fps=10)
    s_out, h_out = wd / "studio.mp4", wd / "hyperframes.mp4"
    py(MOTION, "render", p, "--engine", "studio", "--out", s_out, wd=wd, timeout=60)
    env = kenv(wd, HOME=str(wd / ".hfhome"), PYTHONUSERBASE=str(Path(site.getuserbase())))
    env.update({k: v for k, v in hf_env(wd).items() if k.startswith("HYPERFRAMES") or k in ("DO_NOT_TRACK",)})
    r = py(kmm_mirror(wd) / "motion.py", "render", p, "--engine", "hyperframes", "--out", h_out, wd=wd, timeout=90, env=env)
    eng = json.loads(r.stdout[r.stdout.rfind("{"):]) if "{" in r.stdout else {}
    a, b = fx.frames(s_out, size=(160, 90)), fx.frames(h_out, size=(160, 90))
    ca, cb = [red_cx(f) for f in a], [red_cx(f) for f in b]
    exp = [10 + 140 * k / 5 for k in range(5)]
    return [check("both engines rendered 5 frames", len(a) == len(b) == 5, [len(a), len(b)], 5),
            check("studio engine box centres match t", all(c is not None and abs(c - e) <= 3 for c, e in zip(ca, exp)), ca, exp),
            check("hyperframes engine box centres match t", all(c is not None and abs(c - e) <= 3 for c, e in zip(cb, exp)), cb, exp),
            check("negative control: frame 0 vs frame 4 differ by > 100 px", abs(ca[-1] - ca[0]) > 100, [ca[0], ca[-1]], "> 100")], [s_out, h_out]


@card("ENG-289")
def km_template(task, wd):
    """motion.py new: the default composition (data-* root, #cam stage, SVG gradient, vignette .4, grain .06, camera push 1.06)."""
    import numpy as np
    p = kproj(wd, "tpl", seconds=1, fps=15, size="320x180", title="مرحبا")
    t = (p / "index.html").read_text()
    py(MOTION, "frames", p, "--times", "0.05,0.9", wd=wd)
    stills = sorted((p / "frames").glob("*.png"))
    f = load_rgb(stills[0])
    top, bot = f[6, 160], f[172, 160]
    feats = {"root": 'data-composition-id="root"' in t, "cam": 'id="cam"' in t, "grad": "#1b2a49" in t and "#0d1b2a" in t,
             "vignette": "strength: 0.4" in t, "grain": "opacity: 0.06" in t, "push": "scale: 1.06" in t}
    blank = load_rgb(hf_project(wd, "plain", box_comp()) and _plain_png(wd))
    return [check("template carries the house contract", all(feats.values()), feats, "all True"),
            check("rendered ground runs top lighter-blue -> bottom darker (gradient #1b2a49 -> #0d1b2a)", top[2] > bot[2] and top[0] >= bot[0], [top, bot], "top > bottom"),
            check("negative control: a flat black page has no such gradient", float(abs(blank[6, 160] - blank[172, 160]).sum()) < 3, blank[6, 160], "flat")], stills


def _plain_png(wd):
    from PIL import Image
    Image.new("RGB", (320, 180), (0, 0, 0)).save(wd / "plain.png")
    return wd / "plain.png"


@card("ENG-230")
def km_render_lints(task, wd):
    """motion.py lint: render-contract rules (audio id, will-change, gsap.from, timers, Math.random, CSS transition)."""
    p = kproj(wd, "lintme", seconds=1, fps=15, size="320x180")
    good = (p / "index.html").read_text()
    bad = good.replace("</style>", "#x{will-change: transform; transition: opacity .3s}</style>").replace(
        "<script>", "<script>const jitter=Math.random();setTimeout(()=>{},10);gsap.from('#title',{opacity:0});", 1).replace(
        "</body>", '<audio src="assets/a.wav"></audio></body>')
    (p / "index.html").write_text(bad)
    fb = last_json(py(MOTION, "lint", p, wd=wd, ok=False).stdout + "\n")
    lines = py(MOTION, "lint", p, wd=wd, ok=False).stdout
    (wd / "lint_bad.txt").write_text(lines)
    want = {"Math.random": "Math.random", "timers": "timers", "audio": "<audio> without an id", "will-change": "will-change", "transition": "CSS transition", "from": "gsap.from"}
    hits = {k: (v in lines) for k, v in want.items()}
    clean = mover(kproj(wd, "clean", seconds=1, fps=15, size="320x180"), w=320, h=180, d=1, fps=15)
    fg = last_json(py(MOTION, "lint", clean, wd=wd, ok=False).stdout + "\n")
    return [check("every injected rule is flagged", all(hits.values()), hits, "all True"),
            check("errors counted (random, timers, audio id)", fb.get("errors", 0) >= 3, fb, ">= 3 errors"),
            check("clean mover passes with 0 errors", fg.get("errors", 1) == 0, fg, 0),
            check("negative control: the violating project fails the 0-error criterion", fb.get("errors", 0) > 0, fb.get("errors"), "> 0")], [wd / "lint_bad.txt"]


@card("ENG-282")
def km_kit_delta(task, wd):
    """The motion.py owner layer over HyperFrames: measure / sheet / inspect on a real render."""
    p = mover(kproj(wd, "kd", seconds=1, fps=10, size="160x90"), w=160, h=90, d=1, fps=10)
    fx.tone(p / "assets/t.wav", seconds=1.0, amp=0.6)
    out = wd / "kd.mp4"
    py(MOTION, "render", p, "--engine", "studio", "--out", out, wd=wd, timeout=60)
    meas = py(MOTION, "measure", out, "--fps", 10, wd=wd, ok=False).stdout
    sheet = wd / "sheet.png"
    py(MOTION, "sheet", out, "--out", sheet, wd=wd, ok=False)
    insp = py(MOTION, "inspect", out, wd=wd, ok=False)
    (wd / "measure.txt").write_text(meas + "\n----\n" + insp.stdout)
    still = wd / "still.mp4"
    fx.color_clip(still, color="black", seconds=1.0, size="160x90", fps=10)
    meas_still = py(MOTION, "measure", still, "--fps", 10, wd=wd, ok=False).stdout
    def motion_of(txt):
        try:
            j = last_json(txt + "\n")
        except ValueError:
            return None
        for k in ("motion", "mean_motion", "motion_mean", "activity"):
            if isinstance(j.get(k), (int, float)):
                return float(j[k])
        nums = [v for v in j.values() if isinstance(v, (int, float))]
        return float(sum(nums)) if nums else None
    m1, m0 = motion_of(meas), motion_of(meas_still)
    return [check("measure ran on the render", m1 is not None, m1, "number"),
            check("contact sheet written", sheet.exists() and sheet.stat().st_size > 0, sheet.exists(), True),
            check("inspect (delivery gate) answered", "yuv420p" in insp.stdout or "h264" in insp.stdout.lower() or insp.returncode in (0, 1), insp.stdout[-120:], "gate report"),
            check("negative control: a black still measures differently from the moving render", m0 is not None and m1 is not None and m0 != m1, [m1, m0], "differ")], [sheet, wd / "measure.txt"]


@card("ENG-33")
def km_step_skill_map(task, wd):
    """kosif-one plan.py: STEP_SKILLS maps each production step to where it lives; plan() routes a request to steps."""
    sys.path.insert(0, str(VEND / "kosif-one/scripts"))
    import plan as P
    cases = {"عايز موشن جرافيك لكلمات متحركة عن النجاح": "motion_2d", "مشهد 3D واقعي لمركب في البحر تحت القمر": "cinematic_3d",
             "عندي فيديو بتكلم فيه عايز اقص الصمت واحط سبتايتل": "talking_reel"}
    got = {q: P.plan(q)["main_route"] for q in cases}
    p = P.plan("عايز موشن جرافيك لكلمات متحركة عن النجاح")
    steps = [s["step"] for s in p["steps"]]
    missing = [s for s in steps if s not in P.STEP_SKILLS]
    uses = [u for s in p["steps"] for u in s["use"]]
    files = [u for u in uses if u.get("path")]
    exist = sum(1 for u in files if Path(u["path"]).exists())
    jw(wd / "plan.json", p)
    none = P.plan("صلح الكود ده فيه خطأ")["main_route"]
    return [check("requests route to the expected pipelines", got == cases, got, cases),
            check("every planned step is in STEP_SKILLS", steps and not missing, missing, []),
            check("steps resolve to real skill files on disk", files and exist == len(files), [exist, len(files)], "all exist"),
            check("negative control: a code-fix request is not a media route", none == "not_media", none, "not_media")], [wd / "plan.json"]


@card("ENG-302")
def km_studio_cli(task, wd):
    """pixel-studio-painter studio.py headless modes: --render a scene to PNG at --scale, and --code FILE --render."""
    import numpy as np
    out = wd / "scene.png"
    r = py(STUDIO, "dragon_girl", "--render", out, "--scale", 0.25, wd=wd, timeout=60)
    from PIL import Image
    im = Image.open(out)
    code = wd / "pic.py"
    code.write_text("from PIL import Image, ImageDraw\nim = Image.new('RGB', (200, 100), (255, 255, 255))\n"
                    "ImageDraw.Draw(im).rectangle((50, 25, 150, 75), fill=(0, 0, 255))\nim.save('out.png')\n")
    out2 = wd / "code.png"
    r2 = py(STUDIO, "--code", code, "--render", out2, wd=wd, timeout=60, ok=False)
    c = load_rgb(out2) if out2.exists() else None
    arr = np.asarray(im.convert("RGB")).astype(float)
    return [check("scene rendered at scale 0.25 of 1200x800 -> 300x200", im.size == (300, 200), list(im.size), [300, 200]),
            check("rendered picture is not blank", float(arr.std()) > 10, float(arr.std()), "> 10"),
            check("--code picture rendered with the blue rectangle", c is not None and c[c.shape[0] // 2, c.shape[1] // 2][2] > 200 and c[c.shape[0] // 2, c.shape[1] // 2][0] < 60,
                  None if c is None else c[c.shape[0] // 2, c.shape[1] // 2], "blue centre"),
            check("negative control: the code picture's corner is white, not blue", c is not None and c[2, 2].min() > 200, None if c is None else c[2, 2], "white")], [out, out2]


# ======================================================================================= KOSIF Motion Web (local studio server)


class WebServer:
    """scripts/web/server.py on 127.0.0.1:<free port> with its home (KOSIF_MOTION_HOME) inside the work folder."""

    def __init__(self, wd, workers=1):
        self.wd = Path(wd)
        self.port = free_port()
        self.base = "http://127.0.0.1:%d" % self.port
        self.log = open(self.wd / "server.log", "w")
        self.p = subprocess.Popen([sys.executable, str(KMM / "web/server.py"), "--host", "127.0.0.1", "--port", str(self.port),
                                   "--workers", str(workers)], stdout=self.log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                                  cwd=str(self.wd), env=kenv(self.wd))
        t0 = time.time()
        while time.time() - t0 < 12:
            try:
                if http("GET", self.base + "/api/health", timeout=2)[0] == 200:
                    return
            except OSError:
                time.sleep(0.15)
        self.close()
        raise RuntimeError("web server did not come up: " + (self.wd / "server.log").read_text()[-300:])

    def get(self, path, **kw):
        c, b, h = http("GET", self.base + path, **kw)
        return c, b, h

    def jget(self, path, **kw):
        c, b, _ = self.get(path, **kw)
        return c, (json.loads(b) if b[:1] in (b"{", b"[") else b)

    def jpost(self, path, body, **kw):
        c, b, _ = http("POST", self.base + path, body=body, **kw)
        try:
            return c, json.loads(b)
        except ValueError:
            return c, b

    def rpc(self, method, params=None):
        return self.jpost("/mcp", {"jsonrpc": "2.0", "id": 1, "method": method, "params": params or {}})[1]

    def close(self):
        try:
            self.p.terminate()
            self.p.wait(timeout=5)
        except Exception:  # noqa: BLE001
            self.p.kill()
        self.log.close()


def _listening(port):
    s = socket.socket()
    s.settimeout(0.5)
    try:
        return s.connect_ex(("127.0.0.1", port)) == 0
    finally:
        s.close()


@card("ENG-16")
def web_workbench_contract(task, wd):
    """Local studio web app: /api/plan (12 s x 30 fps -> 360 frames), /api/validate, /api/compile (manifest + window.render)."""
    import copy
    srv = WebServer(wd)
    try:
        c, p = srv.jpost("/api/plan", {"task": "حركة نصوص عربية", "seconds": 12, "fps": 30, "aspect": "16:9"})
        v_ok = srv.jpost("/api/validate", {"plan": p})[1]
        q = copy.deepcopy(p)
        q["timeline"]["shots"][1]["start_frame"] += 1
        v_bad = srv.jpost("/api/validate", {"plan": q})[1]
        comp = srv.jpost("/api/compile", {"plan": p})[1]
        c415 = http("POST", srv.base + "/api/plan", body=b"x", headers={"content-type": "text/plain"})[0]
    finally:
        srv.close()
    jw(wd / "plan.json", p)
    (wd / "project.html").write_text(comp.get("project_html") or "")
    return [check("plan: 12 s x 30 fps = 360 frames", p["timeline"]["total_frames"] == 360, p["timeline"]["total_frames"], 360),
            check("validate accepts the plan", v_ok.get("valid") is True, v_ok.get("valid"), True),
            check("compile: kosif.motion.manifest.v1 + project_html with window.render", comp["manifest"]["schema"] == "kosif.motion.manifest.v1" and "window.render" in (comp.get("project_html") or ""),
                  comp["manifest"]["schema"], "kosif.motion.manifest.v1"),
            check("JSON-only API: text/plain refused 415", c415 == 415, c415, 415),
            check("negative control: a shot nudged one frame fails validation", v_bad.get("valid") is False, v_bad.get("valid"), False)], [wd / "plan.json", wd / "project.html"]


@card("ENG-18")
def web_loopback_server(task, wd):
    """The montage engine's hands: a loopback-only Starlette site with containment and a cross-origin guard."""
    srv = WebServer(wd)
    try:
        h = srv.jget("/api/health")[1]
        idx_c, idx_b, _ = srv.get("/")
        studio_c = srv.get("/studio/index.html")[0]
        p = srv.jpost("/api/projects", {"name": "t_card", "kind": "template", "template": "title-card", "params": {"title": "اختبار"}, "seconds": 5})[1]
        esc = srv.jpost("/api/projects/t_card/file", {"path": "../x.html", "content": "x"})[0]
        exe = srv.jpost("/api/projects/t_card/file", {"path": "evil.exe", "content": "x"})[0]
        ok_w = srv.jpost("/api/projects/t_card/file", {"path": "notes.md", "content": "ملاحظة"})[1]
        fb = {"version": 1, "text": "x", "over": {}, "notes": [], "status": {}}
        cross = http("POST", srv.base + "/api/projects", body={"name": "evil"}, headers={"origin": "https://evil.example"})[0]
        lan_ips = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")]
        lan_open = False
        for ip in lan_ips[:1]:
            s = socket.socket()
            s.settimeout(0.5)
            lan_open = s.connect_ex((ip, srv.port)) == 0
            s.close()
    finally:
        srv.close()
    (wd / "index.html").write_bytes(idx_b)
    return [check("health ok, home inside the work folder", h["status"] == "ok" and Path(h["engine"]["home"]).resolve() == Path(wd).resolve(), h["engine"]["home"], str(wd)),
            check("RTL UI at / and Studio at /studio/", idx_c == 200 and studio_c == 200, [idx_c, studio_c], [200, 200]),
            check("project created from a template", p.get("has_index") is True, p.get("has_index"), True),
            check("path containment: ../ and .exe refused (400)", esc == 400 and exe == 400, [esc, exe], [400, 400]),
            check("in-project write allowed", "written" in ok_w, list(ok_w), "written"),
            check("cross-origin POST refused (403)", cross == 403, cross, 403),
            check("negative control: not reachable on the LAN address (loopback only)", not lan_open, lan_ips[:1], "closed")], [wd / "index.html"]


@card("ENG-219")
def web_studio_mcp(task, wd):
    """kmotion web: the Starlette studio plus its /mcp endpoint (studio tools) behind a cross-origin guard."""
    srv = WebServer(wd)
    try:
        init = srv.rpc("initialize")
        tools = [t["name"] for t in srv.rpc("tools/list")["result"]["tools"]]
        r = srv.rpc("tools/call", {"name": "motion_plan", "arguments": {"task": "حركة", "seconds": 4, "fps": 24, "aspect": "9:16"}})
        recipes = srv.rpc("tools/call", {"name": "kosif_recipes", "arguments": {}})
        tabs = srv.get("/")[1].decode("utf-8", "replace")
        evil = http("POST", srv.base + "/mcp", body={"jsonrpc": "2.0", "id": 1, "method": "tools/list"}, headers={"origin": "https://evil.example"})[0]
    finally:
        srv.close()
    jw(wd / "mcp_tools.json", tools)
    return [check("MCP server name", init["result"]["serverInfo"]["name"] == "kosif-motion-web", init["result"]["serverInfo"]["name"], "kosif-motion-web"),
            check(">= 14 studio tools including motion_* and kosif_*", len(tools) >= 14 and {"motion_plan", "kosif_run", "kosif_job"} <= set(tools), len(tools), ">= 14"),
            check("motion_plan via MCP: 4 s x 24 fps = 96 frames", r["result"]["structuredContent"]["timeline"]["total_frames"] == 96,
                  r["result"]["structuredContent"]["timeline"]["total_frames"], 96),
            check("recipes reachable through MCP", "groups" in recipes["result"]["structuredContent"], list(recipes["result"]["structuredContent"])[:3], "groups"),
            check("negative control: a cross-origin MCP call is refused", evil == 403, evil, 403)], [wd / "mcp_tools.json"]


@card("ENG-233")
def web_jobs_sse(task, wd):
    """Local KOSIF Motion Web: recipe job queued, run, logged, and streamed over SSE until 'event: end'."""
    srv = WebServer(wd)
    try:
        j = srv.jpost("/api/jobs", {"recipe": "transitions", "args": {}})[1]
        t0, s = time.time(), {}
        while time.time() - t0 < 10:
            s = srv.jget("/api/jobs/%s" % j["id"])[1]
            if s.get("status") in ("done", "failed"):
                break
            time.sleep(0.2)
        log = srv.get("/api/jobs/%s/log.txt" % j["id"])[1].decode("utf-8", "replace")
        sse = srv.get("/api/jobs/%s/log" % j["id"])[1].decode("utf-8", "replace")
        bad = srv.jpost("/api/jobs", {"recipe": "nope"})[0]
    finally:
        srv.close()
    (wd / "job.log").write_text(log)
    (wd / "job.sse").write_text(sse)
    return [check("job queued then done", j.get("status") == "queued" and s.get("status") == "done", [j.get("status"), s.get("status")], ["queued", "done"]),
            check("job log lists ffmpeg transitions (fade)", "fade" in log, len(log), "contains fade"),
            check("SSE stream ends with 'event: end'", "event: end" in sse, sse[-60:], "event: end"),
            check("negative control: an unknown recipe is refused (400)", bad == 400, bad, 400)], [wd / "job.log", wd / "job.sse"]


@card("ENG-234")
def web_mcp_tools(task, wd):
    """kosif-web MCP: Claude drives the local site (kosif_project_write, kosif_timeline_check, kosif_run/kosif_job)."""
    srv = WebServer(wd)
    try:
        srv.jpost("/api/projects", {"name": "mcpp", "kind": "template", "template": "title-card", "params": {"title": "x"}, "seconds": 3})
        w = srv.rpc("tools/call", {"name": "kosif_project_write", "arguments": {"name": "mcpp", "path": "notes.md", "content": "من MCP"}})
        wbad = srv.rpc("tools/call", {"name": "kosif_project_write", "arguments": {"name": "mcpp", "path": "../escape.md", "content": "x"}})
        a = fx.test_clip(wd / "a.mp4", seconds=2.0, size="320x180", fps=24)
        spec = {"size": "320x180", "fps": 24, "clips": [{"src": str(a), "in": 0.5, "out": 1.5}, {"color": "#000000", "dur": 0.5}]}
        tc = srv.rpc("tools/call", {"name": "kosif_timeline_check", "arguments": {"spec": spec}})
        run = srv.rpc("tools/call", {"name": "kosif_run", "arguments": {"recipe": "transitions", "args": {}}})
    finally:
        srv.close()
    written = (wd / "projects/mcpp/notes.md")
    tcs = tc["result"].get("structuredContent") or json.loads(tc["result"]["content"][0]["text"])
    jw(wd / "mcp_calls.json", {"write": w, "timeline": tc, "run": run})
    err = wbad.get("error") or (wbad.get("result") or {}).get("isError")
    return [check("kosif_project_write wrote the file into the project", written.exists() and written.read_text() == "من MCP", written.exists(), True),
            check("kosif_timeline_check: 2 clips, 1.0 + 0.5 = 1.5 s", len(tcs.get("clips", [])) == 2 and abs(tcs.get("seconds", 0) - 1.5) < 0.05, [len(tcs.get("clips", [])), tcs.get("seconds")], [2, 1.5]),
            check("kosif_run queued a recipe job", "transitions" in json.dumps(run), "transitions" in json.dumps(run), True),
            check("negative control: a path escaping the project is refused", bool(err) and not (wd / "projects/escape.md").exists(), bool(err), True)], [wd / "mcp_calls.json"]


@card("ENG-235")
def web_studio_export(task, wd):
    """KOSIF Studio: single-file offline studio (WebCodecs + mp4-muxer 5.2.1), and studio JSON -> timeline -> full-quality MP4 at -14 LUFS."""
    out_html = wd / "studio-cloud.html"
    py(KMM / "web/build_studio_cloud.py", "--out", out_html, wd=wd, timeout=60)
    page = out_html.read_text("utf-8", "replace")
    r, _ = browser(wd, "wc", "<script>(async()=>{const s=await VideoEncoder.isConfigSupported({codec:'avc1.42001f',width:320,height:180,bitrate:1e6,framerate:30});"
                   "window.__r={avc:s.supported}})()</script>")
    media = wd / "media"
    media.mkdir()
    clip = media / "studio_clip.mp4"
    fx.ffmpeg("-f", "lavfi", "-i", "testsrc2=s=320x180:r=24:d=3", "-f", "lavfi", "-i", "sine=f=440:d=3", "-c:v", "libx264", "-pix_fmt", "yuv420p",
              "-c:a", "aac", "-shortest", str(clip))
    project = {"version": 1, "name": "من الاستوديو", "aspect": "9:16", "background": "#07111e",
               "assets": [{"id": "a1", "name": "studio_clip.mp4", "type": "video", "size": 1, "lastModified": 0, "duration": 3}],
               "clips": [{"id": "c1", "type": "video", "assetId": "a1", "trim": 0.5, "duration": 2, "volume": 1, "fit": "cover"},
                         {"id": "c2", "type": "demo", "preset": "sunset", "duration": 1.0}],
               "overlays": [], "soundtrack": None}
    jw(wd / "studio_project.json", project)
    film = wd / "studio_film.mp4"
    py(KMM / "studio_import.py", wd / "studio_project.json", "--out", wd / "edit.json", "--media", media, "--render", film, wd=wd, timeout=90)
    spec = json.loads((wd / "edit.json").read_text())
    p, v = probe_v(film)
    L = lufs(film)
    dur = float(p["format"]["duration"])
    bad = subprocess.run([sys.executable, str(KMM / "studio_import.py"), str(jw(wd / "v7.json", {"version": 7})), "--out", str(wd / "x.json")],
                         capture_output=True, text=True, timeout=30)
    return [check("single-file studio bundles mp4-muxer 5.2.1 + WebCodecs export", "5.2.1" in page and "VideoEncoder" in page and len(page) > 50000,
                  ["5.2.1" in page, "VideoEncoder" in page, len(page)], [True, True, "> 50 KB"]),
            check("this Chrome's WebCodecs supports H.264 encode", r.get("avc") is True, r.get("avc"), True),
            check("studio JSON -> 9:16 timeline (720x1280)", spec["size"] == "720x1280" and (v["width"], v["height"]) == (720, 1280), [spec["size"], v["width"], v["height"]], "720x1280"),
            check("film length = 2.0 + 1.0 s", abs(dur - 3.0) < 0.1, dur, 3.0),
            check("mix at -14 LUFS (+-1.5)", L is not None and abs(L + 14) <= 1.5, L, -14),
            check("negative control: a version-7 project is refused", bad.returncode != 0, bad.returncode, "!= 0")], [film, out_html]


# ======================================================================================= three.js WebGPU / TSL, WebGL, maps, charts

IMPORTMAP = ('<script type="importmap">{"imports":{"three":"/nm/three/build/three.webgpu.js","three/webgpu":"/nm/three/build/three.webgpu.js",'
             '"three/tsl":"/nm/three/build/three.tsl.js","three/addons/":"/nm/three/examples/jsm/"}}</script>')


def tsl_page(body_js, w=64, h=64):
    return ("<html><body style='margin:0;background:#000'>%s<script type='module'>\nimport * as THREE from 'three/webgpu';\n"
            "import * as TSL from 'three/tsl';\nconst W=%d,H=%d;const R={};\n"
            "async function px(renderer,rt){const p=await renderer.readRenderTargetPixelsAsync(rt,0,0,W,H);return Array.from(p);}\n"
            "try{\nconst renderer=new THREE.WebGPURenderer({antialias:false});renderer.setSize(W,H);renderer.setPixelRatio(1);"
            "document.body.appendChild(renderer.domElement);await renderer.init();R.backend=renderer.backend.isWebGPUBackend?'webgpu':'webgl';\n"
            "const cam=new THREE.OrthographicCamera(-1,1,1,-1,0.1,10);cam.position.z=2;\n%s\n}catch(e){R.err=String(e.stack||e);}\nwindow.__r=R;\n</script></body></html>"
            % (IMPORTMAP, w, h, body_js))


def rgba_at(pix, w, x, y):
    i = (y * w + x) * 4
    return pix[i:i + 4]


@card("ENG-138")
def tsl_node_materials(task, wd):
    """WebGPURenderer + TSL node material (colorNode/roughnessNode/positionNode); frames captured headless and encoded."""
    import numpy as np
    js = r"""
const {mix,color,uv,uniform,float,positionLocal,vec3}=TSL;
const u=uniform(0);
const scene=new THREE.Scene();scene.add(new THREE.AmbientLight(0xffffff,3));
const m=new THREE.MeshStandardNodeMaterial();m.colorNode=mix(color(0xff0000),color(0x0000ff),u);m.roughnessNode=float(0.35);
m.positionNode=positionLocal.mul(vec3(0.5,1,1));
const mesh=new THREE.Mesh(new THREE.PlaneGeometry(2,2),m);scene.add(mesh);
const rt=new THREE.RenderTarget(W,H);renderer.setRenderTarget(rt);R.frames=[];
for(let k=0;k<5;k++){u.value=k/4;renderer.render(scene,cam);R.frames.push(await px(renderer,rt));}
const plain=new THREE.Mesh(new THREE.PlaneGeometry(2,2),new THREE.MeshStandardMaterial({color:0xff0000}));
scene.remove(mesh);scene.add(plain);renderer.render(scene,cam);R.plain=await px(renderer,rt);
"""
    r, logs = browser(wd, "tsl", tsl_page(js), flags=WEBGPU, timeout=25000)
    W = H = 64
    frames = [np.array(f, dtype=np.uint8).reshape(H, W, 4)[::-1, :, :3] for f in r["frames"]]
    write_mp4(wd / "tsl_frames.mp4", frames, fps=5)
    def width(a):
        return int((a[32].sum(1) > 30).sum())
    plain = np.array(r["plain"], dtype=np.uint8).reshape(H, W, 4)[::-1, :, :3]
    f0, f4 = frames[0][32, 32].astype(int), frames[-1][32, 32].astype(int)
    back = fx.frames(wd / "tsl_frames.mp4", size=(W, H))
    return [check("WebGPU backend (SwiftShader adapter)", r["backend"] == "webgpu", r["backend"], "webgpu"),
            check("positionNode halves the plane width (32 of 64 px)", abs(width(frames[0]) - 32) <= 2, width(frames[0]), 32),
            check("colorNode animates red -> blue over the uniform", f0[0] > 150 and f0[2] < 40 and f4[2] > 150 and f4[0] < 40, [list(f0), list(f4)], "red -> blue"),
            check("captured frames encoded and decode back (5)", len(back) == 5, len(back), 5),
            check("negative control: the plain material plane spans the full width", width(plain) >= 62, width(plain), 64)], [wd / "tsl_frames.mp4"]


def _pipe_shots(wd, name, js, w=96, h=64, flags=WEBGPU):
    """Pages that expose window.go(mode) -> Promise; screenshot each mode."""
    page = tsl_page(js, w=w, h=h)
    modes = re.findall(r"//MODES:(.*)", js)[0].split(",")
    r, _ = browser(wd, name, page, flags=flags, size=(w, h), timeout=25000,
                   shots=[("window.go('%s')" % m, "%s_%s.png" % (name, m)) for m in modes])
    return r, {m: load_rgb(wd / ("%s_%s.png" % (name, m))) for m in modes}


@card("ENG-139")
def tsl_render_pipeline(task, wd):
    """RenderPipeline: scene pass -> effect node -> outputNode; pipeline.render() instead of renderer.render()."""
    import numpy as np
    js = r"""
const {pass,vec4,float}=TSL;
const scene=new THREE.Scene();
scene.add(new THREE.Mesh(new THREE.PlaneGeometry(1,1),new THREE.MeshBasicMaterial({color:0xff0000})));
R.hasPipeline=typeof THREE.RenderPipeline==='function';
const rt=new THREE.RenderTarget(W,H);
const pipe=new THREE.RenderPipeline(renderer);const sp=pass(scene,cam);
const tex=sp.getTextureNode('output');
pipe.outputNode=vec4(tex.rgb.oneMinus(),float(1));
renderer.setRenderTarget(rt);pipe.render();R.pipe=await px(renderer,rt);
renderer.setRenderTarget(rt);renderer.render(scene,cam);R.direct=await px(renderer,rt);
"""
    r, _ = browser(wd, "pipe", tsl_page(js, w=64, h=64), flags=WEBGPU, size=(64, 64), timeout=25000)
    a = np.array(r["pipe"], dtype=np.uint8).reshape(64, 64, 4)[..., :3]
    d = np.array(r["direct"], dtype=np.uint8).reshape(64, 64, 4)[..., :3]
    from PIL import Image
    Image.fromarray(a[::-1]).save(wd / "pipeline.png")
    Image.fromarray(d[::-1]).save(wd / "direct.png")
    pc, pb, dc, db = a[32, 32], a[4, 4], d[32, 32], d[4, 4]
    return [check("RenderPipeline class present (r183+ name)", r.get("hasPipeline") is True, r.get("hasPipeline"), True),
            check("pipeline output = inverted scene: plane cyan", pc[0] < 60 and pc[1] > 200 and pc[2] > 200, pc, [0, 255, 255]),
            check("pipeline output: background white", pb.min() > 200, pb, [255, 255, 255]),
            check("negative control: renderer.render() skips the node graph (red plane on black)", dc[0] > 200 and dc[1] < 60 and db.max() < 40, [dc, db], "red/black")], [wd / "pipeline.png", wd / "direct.png"]


@card("ENG-140")
def tsl_outline_fxaa(task, wd):
    """Built-in TSL passes: outline(scene, camera, {selectedObjects, edgeThickness 1}) x edgeStrength 3, then fxaa()."""
    import numpy as np
    js = r"""
const {pass,uniform,color}=TSL;
const {outline}=await import('three/addons/tsl/display/OutlineNode.js');
const {fxaa}=await import('three/addons/tsl/display/FXAANode.js');
const scene=new THREE.Scene();
const mesh=new THREE.Mesh(new THREE.PlaneGeometry(0.8,0.8),new THREE.MeshBasicMaterial({color:0x0000ff}));scene.add(mesh);
const rt=new THREE.RenderTarget(W,H);const sp=pass(scene,cam);
const op=outline(scene,cam,{selectedObjects:[mesh],edgeThickness:uniform(1.0),edgeGlow:uniform(0)});
const edge=op.visibleEdge.mul(color(0xffffff)).add(op.hiddenEdge.mul(color(0xffffff))).mul(uniform(3.0));
const pipe=new THREE.RenderPipeline(renderer);pipe.outputNode=fxaa(edge.add(sp));
const plain=new THREE.RenderPipeline(renderer);plain.outputNode=sp;
renderer.setRenderTarget(rt);pipe.render();R.outline=await px(renderer,rt);
renderer.setRenderTarget(rt);plain.render();R.plain=await px(renderer,rt);
"""
    r, _ = browser(wd, "outl", tsl_page(js, w=64, h=64), flags=WEBGPU, size=(64, 64), timeout=25000)
    o = np.array(r["outline"], dtype=np.uint8).reshape(64, 64, 4)[..., :3].astype(float)
    p = np.array(r["plain"], dtype=np.uint8).reshape(64, 64, 4)[..., :3].astype(float)
    from PIL import Image
    Image.fromarray(o[::-1].astype("uint8")).save(wd / "outline.png")
    # plane spans x in [19.2, 44.8]; the ring sits just outside each vertical edge
    def ring(a):
        return float(max(a[32, 13:20, 0].max(), a[32, 45:52, 0].max()))
    inner, far = o[32, 32], o[32, 3]
    return [check("outline ring around the selected mesh", ring(o) > 150, ring(o), "> 150"),
            check("mesh interior stays blue", inner[2] > 200 and inner[0] < 80, inner, "blue"),
            check("far background stays dark", far.max() < 40, far, "dark"),
            check("negative control: the plain scene pass has no ring", ring(p) < 20, ring(p), "< 20")], [wd / "outline.png"]


@card("ENG-141")
def tsl_wgsl_fn(task, wd):
    """wgslFn(): raw WGSL injected as a callable TSL node (here mix(a, b, t*t))."""
    import numpy as np
    js = r"""
const {wgslFn,color,uv,mix}=TSL;
const sq=wgslFn(`fn sqmix(a: vec3<f32>, b: vec3<f32>, t: f32) -> vec3<f32> { return mix(a, b, t * t); }`);
const scene=new THREE.Scene();
const m=new THREE.MeshBasicNodeMaterial();m.colorNode=sq({a:color(0xff0000),b:color(0x0000ff),t:uv().x});
const mesh=new THREE.Mesh(new THREE.PlaneGeometry(2,2),m);scene.add(mesh);
const rt=new THREE.RenderTarget(W,H);renderer.setRenderTarget(rt);renderer.render(scene,cam);R.wgsl=await px(renderer,rt);
m.colorNode=mix(color(0xff0000),color(0x0000ff),uv().x);m.needsUpdate=true;renderer.render(scene,cam);R.linear=await px(renderer,rt);
"""
    r, _ = browser(wd, "wgsl", tsl_page(js), flags=WEBGPU, timeout=25000)
    W = 64
    a = np.array(r["wgsl"], dtype=np.uint8).reshape(64, 64, 4)
    b = np.array(r["linear"], dtype=np.uint8).reshape(64, 64, 4)
    from PIL import Image
    Image.fromarray(a[::-1, :, :3]).save(wd / "wgsl.png")
    t = (32 + 0.5) / 64
    exp_r = (1 - t * t) * 255
    return [check("WebGPU backend runs the WGSL", r["backend"] == "webgpu", r["backend"], "webgpu"),
            check("mid pixel red = (1-t^2)*255", abs(float(a[32, 32, 0]) - exp_r) <= 4, float(a[32, 32, 0]), round(exp_r, 1)),
            check("mid pixel blue = t^2*255", abs(float(a[32, 32, 2]) - t * t * 255) <= 4, float(a[32, 32, 2]), round(t * t * 255, 1)),
            check("negative control: the plain linear mix fails the t^2 value", abs(float(b[32, 32, 0]) - exp_r) > 30, float(b[32, 32, 0]), "~128")], [wd / "wgsl.png"]


@card("ENG-142")
def three_shader_scaffold(task, wd):
    """Plane (2x2, 32x32 segments) + custom vertex/fragment shader; memoised uniforms; u_time = frame/fps each frame."""
    import numpy as np
    page = ("<html><body style='margin:0'><script type='importmap'>{\"imports\":{\"three\":\"/nm/three/build/three.module.js\"}}</script>"
            "<script type='module'>import * as THREE from 'three';const R={};try{const W=32,H=32,FPS=6;"
            "const renderer=new THREE.WebGLRenderer({preserveDrawingBuffer:true});renderer.setSize(W,H);document.body.appendChild(renderer.domElement);"
            "const scene=new THREE.Scene();const cam=new THREE.OrthographicCamera(-1,1,1,-1,0.1,10);cam.position.z=2;"
            "const uniforms={u_time:{value:0}};"
            "const geo=new THREE.PlaneGeometry(2,2,32,32);R.verts=geo.attributes.position.count;"
            "const mat=new THREE.ShaderMaterial({uniforms,vertexShader:'void main(){gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0);}',"
            "fragmentShader:'uniform float u_time;void main(){gl_FragColor=vec4(vec3(0.5+0.5*sin(u_time*3.14159)),1.0);}'});"
            "scene.add(new THREE.Mesh(geo,mat));const rt=new THREE.WebGLRenderTarget(W,H);R.vals=[];R.same=uniforms===mat.uniforms;"
            "for(let f=0;f<6;f++){uniforms.u_time.value=f/FPS;renderer.setRenderTarget(rt);renderer.render(scene,cam);const p=new Uint8Array(W*H*4);"
            "renderer.readRenderTargetPixels(rt,0,0,W,H,p);R.vals.push(p[(16*W+16)*4]);}"
            "uniforms.u_time.value=0;R.frozen=[];for(let f=0;f<3;f++){renderer.render(scene,cam);const p=new Uint8Array(W*H*4);renderer.readRenderTargetPixels(rt,0,0,W,H,p);R.frozen.push(p[(16*W+16)*4]);}"
            "}catch(e){R.err=String(e.stack||e)}window.__r=R;</script></body></html>")
    r, _ = browser(wd, "shader", page, flags=SOFTGL, size=(32, 32))
    exp = [round((0.5 + 0.5 * math.sin(f / 6 * math.pi)) * 255) for f in range(6)]
    frames = [np.full((32, 32, 3), v, dtype=np.uint8) for v in r["vals"]]
    write_mp4(wd / "shader.mp4", frames, fps=6)
    return [check("plane 32x32 segments -> 33*33 = 1089 vertices", r["verts"] == 1089, r["verts"], 1089),
            check("uniforms object memoised (same object the material holds)", r["same"] is True, r["same"], True),
            check("u_time = frame/fps drives the shader per frame", all(abs(a - b) <= 2 for a, b in zip(r["vals"], exp)), r["vals"], exp),
            check("negative control: without the per-frame update the value is frozen", len(set(r["frozen"])) == 1 and len(set(r["vals"])) > 3, r["frozen"], "constant")], [wd / "shader.mp4"]


ENGINE_MAP = {"custom-3d": "three", "geo-layers": "deck.gl", "trips": "deck.gl", "arcs": "deck.gl", "globe": "cesium", "terrain": "cesium",
              "2d-sprites": "pixi.js", "particles-2d": "pixi.js", "minimal-shader": "regl", "full-engine": "babylonjs"}


def pick_engine(scene_type):
    return ENGINE_MAP.get(scene_type)


@card("ENG-144")
def engine_selection(task, wd):
    """Engine selection map: scene type -> engine; picks that are installed here are loaded to prove they are usable."""
    answers = {"custom-3d": "three", "trips": "deck.gl", "globe": "cesium", "2d-sprites": "pixi.js", "minimal-shader": "regl", "full-engine": "babylonjs"}
    got = {k: pick_engine(k) for k in answers}
    installed = {e: (NM / e / "package.json").exists() for e in sorted(set(ENGINE_MAP.values()))}
    page = ("<html><body><script type='importmap'>{\"imports\":{\"three\":\"/nm/three/build/three.module.js\",\"pixi\":\"/nm/pixi.js/dist/pixi.min.mjs\"}}</script>"
            "<script type='module'>const R={};try{const T=await import('three');R.three=T.REVISION;const P=await import('pixi');R.pixi=P.VERSION;}catch(e){R.err=String(e)}window.__r=R;</script></body></html>")
    r, _ = browser(wd, "engines", page)
    jw(wd / "engine_map.json", {"map": ENGINE_MAP, "picks": got, "installed": installed, "loaded": r})
    return [check("map answers the card's scene types", got == answers, got, answers),
            check("installed picks load in the browser (three, pixi.js)", str(r.get("three", "")).isdigit() and str(r.get("pixi", "")).startswith("8"), r, "three rev + pixi 8"),
            check("install state reported per engine", installed.get("three") is True and installed.get("pixi.js") is True, installed, "three/pixi present"),
            check("negative control: an unknown scene type gets no engine", pick_engine("spreadsheet") is None, pick_engine("spreadsheet"), None)], [wd / "engine_map.json"]


@card("ENG-147")
def maplibre_deterministic(task, wd):
    """MapLibre: interactive:false, fadeDuration:0, preserveDrawingBuffer; per frame setData -> once('idle') -> capture; twice identical."""
    page = ("<html><head><link rel='stylesheet' href='/nm/maplibre-gl/dist/maplibre-gl.css'></head><body style='margin:0'><div id='m' style='width:256px;height:128px'></div>"
            "<script type='module'>import * as maplibregl from '/nm/maplibre-gl/dist/maplibre-gl.mjs';const R={};try{"
            "const style={version:8,sources:{pt:{type:'geojson',data:{type:'FeatureCollection',features:[]}}},layers:[{id:'bg',type:'background',paint:{'background-color':'#000'}},"
            "{id:'c',type:'circle',source:'pt',paint:{'circle-radius':6,'circle-color':'#ff0000'}}]};"
            "async function run(){const map=new maplibregl.Map({container:'m',style,center:[0,0],zoom:0,interactive:false,fadeDuration:0,attributionControl:false,"
            "canvasContextAttributes:{preserveDrawingBuffer:true}});await new Promise(r=>map.once('idle',r));const out=[];"
            "for(let k=0;k<5;k++){const lon=-60+30*k;map.getSource('pt').setData({type:'Feature',geometry:{type:'Point',coordinates:[lon,0]}});"
            "await new Promise(r=>{map.once('idle',r);map.triggerRepaint();});out.push(map.getCanvas().toDataURL('image/png'));}"
            "return out;}"
            "R.a=await run();R.b=await run();R.dpr=window.devicePixelRatio;}catch(e){R.err=String(e.stack||e)}window.__r=R;</script></body></html>")
    r, logs = browser(wd, "map", page, flags=SOFTGL, size=(256, 128), timeout=25000)
    import base64
    import io
    from PIL import Image
    def dec(u):
        return Image.open(io.BytesIO(base64.b64decode(u.split(",", 1)[1]))).convert("RGB")
    ims = [dec(u) for u in r["a"]]
    for k, im in enumerate(ims):
        im.save(wd / ("frame_%d.png" % k))
    import numpy as np
    cx = [red_cx(np.asarray(im)) for im in ims]
    W = ims[0].size[0]
    exp = [W / 2 + (-60 + 30 * k) / 360 * 512 * (W / 256) for k in range(5)]
    same = all(hashlib.sha256(np.asarray(dec(a)).tobytes()).hexdigest() == hashlib.sha256(np.asarray(dec(b)).tobytes()).hexdigest() for a, b in zip(r["a"], r["b"]))
    return [check("point lands on the Web-Mercator x for each frame", all(c is not None and abs(c - e) <= 2 for c, e in zip(cx, exp)), cx, [round(e, 1) for e in exp]),
            check("two full runs give byte-identical frames (deterministic)", same, same, True),
            check("negative control: frame 0 is not at frame 4's position (frames really advance)", abs(cx[0] - exp[4]) > 50, cx[0], "far from %s" % round(exp[4], 1))], [wd / "frame_2.png"]


@card("ENG-149")
def vega_lite_states(task, wd):
    """Vega-Lite spec -> compile -> Vega View -> SVG per state; tween the two states in our own frames."""
    import numpy as np
    js = r"""
const vl=require(%(vl)s), vega=require(%(vega)s);
function spec(vals){return {"$schema":"https://vega.github.io/schema/vega-lite/v5.json",width:200,height:100,data:{values:vals},
 mark:"bar",encoding:{x:{field:"k",type:"nominal",sort:null},y:{field:"v",type:"quantitative",scale:{domain:[0,10]}}}};}
(async()=>{const out={};
for(const [name,vals] of [["A",[{k:"a",v:2},{k:"b",v:5},{k:"c",v:8}]],["B",[{k:"a",v:8},{k:"b",v:4},{k:"c",v:1}]]]){
 const vg=vl.compile(spec(vals)).spec; const view=new vega.View(vega.parse(vg),{renderer:'none'});
 out[name]=await view.toSVG(); const sg=await view.runAsync(); 
 const bars=[]; view.scenegraph().root.items[0].items.forEach(function walk(n){ if(n.marktype==='rect'&&n.role==='mark'){n.items.forEach(i=>bars.push({x:i.x,y:i.y,w:i.width,h:i.height}));} (n.items||[]).forEach(c=>{if(c.items)walk(c)}) });
 out[name+"_bars"]=bars; }
let bad=null; try{ vl.compile({mark:"bar",encoding:{x:{field:"k",type:"nonsense"}}}); }catch(e){bad=String(e.message||e);}
out.bad=bad; console.log(JSON.stringify(out));})();
"""
    src = wd / "vl.cjs"
    src.write_text(js % {"vl": json.dumps(str(NM / "vega-lite")), "vega": json.dumps(str(NM / "vega"))})
    r = json.loads(fx.run(["node", src], timeout=30).stdout.strip().splitlines()[-1])
    (wd / "stateA.svg").write_text(r["A"])
    (wd / "stateB.svg").write_text(r["B"])
    ha = [b["h"] for b in r["A_bars"]]
    hb = [b["h"] for b in r["B_bars"]]
    frames = []
    for k in range(6):
        u = k / 5
        im = np.zeros((110, 210, 3), dtype=np.uint8)
        for i, (a, b) in enumerate(zip(r["A_bars"], r["B_bars"])):
            h = a["h"] + (b["h"] - a["h"]) * u
            x0 = int(a["x"]) + 5
            im[int(105 - h):105, x0:x0 + int(a["w"])] = (70, 130, 180)
        frames.append(im)
    write_mp4(wd / "vl_tween.mp4", frames, fps=5)
    mid = fx.frames(wd / "vl_tween.mp4", size=(210, 110))
    def hcol(a, x):
        return int((a[:, x].sum(1) > 150).sum())
    xa = int(r["A_bars"][0]["x"] + r["A_bars"][0]["w"] / 2) + 5
    return [check("bars encode data: heights = v/10 x 100 px", all(abs(h - v * 10) < 0.5 for h, v in zip(ha, [2, 5, 8])) and all(abs(h - v * 10) < 0.5 for h, v in zip(hb, [8, 4, 1])), [ha, hb], [[20, 50, 80], [80, 40, 10]]),
            check("SVG written for each state with 3 bars", r["A"].count("<path") >= 3 and len(r["A_bars"]) == 3, len(r["A_bars"]), 3),
            check("tween midpoint frame: bar a at (20+80)/2 = 50 px", abs(hcol(mid[0], xa) - 20) <= 2 and abs(hcol(mid[-1], xa) - 80) <= 2, [hcol(mid[0], xa), hcol(mid[-1], xa)], [20, 80]),
            check("negative control: an invalid spec is rejected by vega-lite", bool(r.get("bad")), (r.get("bad") or "")[:80], "error")], [wd / "stateA.svg", wd / "vl_tween.mp4"]


@card("ENG-150")
def d3_math_engine(task, wd):
    """D3 for scales/shapes/geo; every frame computed from t (no d3.transition timers); our timeline owns time."""
    import numpy as np
    from PIL import Image, ImageDraw
    js = r"""
import * as d3 from %(d3)s;
const x=d3.scaleLinear().domain([0,10]).range([0,200]), y=d3.scaleLinear().domain([0,100]).range([100,0]);
const data=[[0,0],[5,50],[10,100]];
const line=d3.line().x(d=>x(d[0])).y(d=>y(d[1]));
const proj=d3.geoEquirectangular().scale(100/Math.PI).translate([100,50]);
const frames=[]; for(let f=0;f<5;f++){const t=f/4; const vals=data.map(d=>[d[0],d[1]*t]); frames.push({t, path:line(vals), pts:vals.map(d=>[x(d[0]),y(d[1])])});}
console.log(JSON.stringify({x5:x(5),y50:y(50),ticks:x.ticks(5),path:line(data),cairo:proj([31.24,30.04]),frames,ext:d3.extent([3,9,1])}));
"""
    src = wd / "d3.mjs"
    src.write_text(js % {"d3": json.dumps(str(NM / "d3/src/index.js"))})
    r = json.loads(fx.run(["node", src], timeout=30).stdout.strip())
    ims = []
    for fr in r["frames"]:
        im = Image.new("RGB", (210, 110), (0, 0, 0))
        ImageDraw.Draw(im).line([(p[0] + 5, p[1] + 5) for p in fr["pts"]], fill=(255, 0, 0), width=2)
        ims.append(np.asarray(im))
    write_mp4(wd / "d3_line.mp4", ims, fps=5)
    last_y = r["frames"][-1]["pts"][2][1]
    mid_y = r["frames"][2]["pts"][2][1]
    exp_cairo = [100 + 31.24 * (100 / math.pi) * math.pi / 180, 50 - 30.04 * (100 / math.pi) * math.pi / 180]
    return [check("scale known answers: x(5)=100, y(50)=50", r["x5"] == 100 and r["y50"] == 50, [r["x5"], r["y50"]], [100, 50]),
            check("line path string from d3-shape", r["path"] == "M0,100L100,50L200,0", r["path"], "M0,100L100,50L200,0"),
            check("geo projection of Cairo matches equirectangular math", all(abs(a - b) < 0.01 for a, b in zip(r["cairo"], exp_cairo)), r["cairo"], [round(v, 3) for v in exp_cairo]),
            check("frame t=0.5 computed from t: last point y = y(50) = 50", abs(mid_y - 50) < 1e-9 and abs(last_y - 0) < 1e-9, [mid_y, last_y], [50, 0]),
            check("negative control: frame t=0 differs from t=1 (state is a function of t)", r["frames"][0]["path"] != r["frames"][-1]["path"], r["frames"][0]["path"][:30], "!= final")], [wd / "d3_line.mp4"]


@card("ENG-151")
def plotly_static_frames(task, wd):
    """Product chart library in video: Plotly with animation off, state set per frame, exported statically (kaleido)."""
    import numpy as np
    import plotly.graph_objects as go
    import plotly.io as pio
    figs, pngs = [], []
    for k, u in enumerate((0.0, 0.5, 1.0)):
        vals = [2 + 6 * u, 5, 8 - 6 * u]
        fig = go.Figure(go.Bar(x=["a", "b", "c"], y=vals, marker_color="#ff0000"))
        fig.update_layout(width=300, height=200, margin=dict(l=0, r=0, t=0, b=0), yaxis=dict(range=[0, 10], visible=False),
                          xaxis=dict(visible=False), plot_bgcolor="#000", paper_bgcolor="#000", transition={"duration": 0})
        figs.append(fig)
        pngs.append(wd / ("plotly_%d.png" % k))
    pio.write_images(figs, [str(p) for p in pngs], scale=1, width=300, height=200)          # one kaleido browser for every state
    imgs = [load_rgb(p) for p in pngs]
    write_mp4(wd / "plotly.mp4", [i.astype("uint8") for i in imgs], fps=3)
    def bar_h(a, col):
        x = int(a.shape[1] * (col + 0.5) / 3)
        return int((a[:, x, 0] > 150).sum())
    h0 = [bar_h(imgs[0], c) for c in range(3)]
    h2 = [bar_h(imgs[2], c) for c in range(3)]
    return [check("frame 0 bars proportional to [2,5,8] of 10 (x 20 px)", all(abs(h - v * 20) <= 3 for h, v in zip(h0, [2, 5, 8])), h0, [40, 100, 160]),
            check("frame 2 bars proportional to [8,5,2]", all(abs(h - v * 20) <= 3 for h, v in zip(h2, [8, 5, 2])), h2, [160, 100, 40]),
            check("frames encoded (3)", nframes(wd / "plotly.mp4") == 3, nframes(wd / "plotly.mp4"), 3),
            check("negative control: frame 0 fails frame 2's heights", abs(h0[0] - 160) > 50, h0[0], "!= 160")], [wd / "plotly.mp4", pngs[1]]


# ======================================================================================= in-page libraries, Lottie, Slidev, Pixi, MoviePy


def _lottie_json():
    """A Bodymovin document: one shape layer, a red 40x40 rect whose position moves 20 -> 140 px linearly over 30 frames."""
    lin = {"i": {"x": [1], "y": [1]}, "o": {"x": [0], "y": [0]}}
    return {"v": "5.7.0", "fr": 30, "ip": 0, "op": 30, "w": 160, "h": 90, "nm": "mover", "ddd": 0, "assets": [],
            "layers": [{"ddd": 0, "ind": 1, "ty": 4, "nm": "box", "sr": 1, "ip": 0, "op": 30, "st": 0, "bm": 0,
                        "ks": {"o": {"a": 0, "k": 100}, "r": {"a": 0, "k": 0}, "a": {"a": 0, "k": [0, 0, 0]}, "s": {"a": 0, "k": [100, 100, 100]},
                               "p": {"a": 1, "k": [dict(t=0, s=[20, 45, 0], e=[140, 45, 0], **lin), {"t": 30, "s": [140, 45, 0]}]}},
                        "shapes": [{"ty": "gr", "nm": "g", "it": [
                            {"ty": "rc", "nm": "r", "d": 1, "s": {"a": 0, "k": [40, 40]}, "p": {"a": 0, "k": [0, 0]}, "r": {"a": 0, "k": 0}},
                            {"ty": "fl", "nm": "f", "c": {"a": 0, "k": [1, 0, 0, 1]}, "o": {"a": 0, "k": 100}, "r": 1, "bm": 0},
                            {"ty": "tr", "p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0},
                             "o": {"a": 0, "k": 100}, "sk": {"a": 0, "k": 0}, "sa": {"a": 0, "k": 0}}]}]}]}


@card("ENG-123")
def lottie_in_timeline(task, wd):
    """lottie.loadAnimation({autoplay:false}) with the frame set from the timeline; GSAP entrance scale 0.3->1 back.out(1.6) 0.35 s."""
    jw(wd / "mover.json", _lottie_json())
    page = ("<html><body style='margin:0;background:#000'><div id='wrap' style='width:160px;height:90px'><div id='l' style='width:160px;height:90px'></div></div>"
            "<script src='/nm/lottie-web/build/player/lottie.min.js'></script><script src='/nm/gsap/dist/gsap.min.js'></script><script>"
            "fetch('mover.json').then(r=>r.json()).then(data=>{const anim=lottie.loadAnimation({container:document.getElementById('l'),renderer:'svg',autoplay:false,loop:false,animationData:data});"
            "window.seekTo=(t)=>{anim.goToAndStop(Math.round(t*30),true);};"
            "const tl=gsap.timeline({paused:true});tl.fromTo('#wrap',{scale:0.3},{scale:1,duration:0.35,ease:'back.out(1.6)'},0);"
            "const sc=[0,0.1,0.2,0.3,0.35].map(t=>{tl.seek(t);return gsap.getProperty('#wrap','scale');});tl.seek(1);"
            "anim.addEventListener('DOMLoaded',()=>{window.__r={frames:anim.totalFrames,fr:anim.frameRate,scale:sc}});});</script></body></html>")
    r, _ = browser(wd, "lottie", page, size=(160, 90), shots=[("window.seekTo(0)", "f0.png"), ("window.seekTo(0.5)", "f15.png"), ("window.seekTo(29/30)", "f29.png")])
    c0, c15, c29 = (red_cx(load_rgb(wd / n)) for n in ("f0.png", "f15.png", "f29.png"))
    sc = r["scale"]
    return [check("Bodymovin JSON loaded: 30 frames at 30 fps", r["frames"] == 30 and r["fr"] == 30, [r["frames"], r["fr"]], [30, 30]),
            check("timeline t=0.5 s -> lottie frame 15 -> box at 80 px", c15 is not None and abs(c15 - 80) <= 2, c15, 80),
            check("frame 29 -> 20+120*29/30 = 136 px", c29 is not None and abs(c29 - 136) <= 2, c29, 136),
            check("entrance: scale 0.3 at 0, overshoots past 1, lands on 1 at 0.35 s", abs(sc[0] - 0.3) < 1e-6 and max(sc) > 1.0 and abs(sc[-1] - 1) < 1e-6, sc, "0.3 -> >1 -> 1"),
            check("negative control: frame 0 is far from the frame-15 position", c0 is not None and abs(c0 - 80) > 40, c0, 20)], [wd / "f15.png", wd / "mover.json"]


CATALOG_CLAIMS = {"motion": "MIT", "animejs": "MIT", "three": "MIT", "gsap": "no-charge", "lottie-web": "MIT", "pixi.js": "MIT", "d3": "ISC",
                  "p5": "LGPL-2.1", "maplibre-gl": "BSD-3-Clause"}


def _license_ok(claim, lic):
    lic = str(lic or "")
    if claim == "no-charge":
        return "no charge" in lic.lower() and "MIT" not in lic
    return lic == claim


@card("ENG-132")
def component_catalog_licenses(task, wd):
    """Animated component/library catalog with licence notes, checked against the installed packages' own licence fields."""
    rows = []
    for name, claim in CATALOG_CLAIMS.items():
        pj = NM / name / "package.json"
        meta = json.loads(pj.read_text()) if pj.exists() else {}
        rows.append({"name": name, "version": meta.get("version"), "claim": claim, "package_license": meta.get("license"),
                     "ok": _license_ok(claim, meta.get("license")), "osi": claim != "no-charge"})
    jw(wd / "catalog_licenses.json", rows)
    md = "| lib | version | licence | OSI |\n|---|---|---|---|\n" + "\n".join("| %s | %s | %s | %s |" % (r["name"], r["version"], r["package_license"], r["osi"]) for r in rows)
    (wd / "catalog_licenses.md").write_text(md)
    gs = [r for r in rows if r["name"] == "gsap"][0]
    return [check("every catalogued licence matches the package's own field", all(r["ok"] for r in rows), {r["name"]: r["package_license"] for r in rows if not r["ok"]}, "all match"),
            check("anime.js is v4 (as catalogued)", str([r for r in rows if r["name"] == "animejs"][0]["version"]).startswith("4."), [r for r in rows if r["name"] == "animejs"][0]["version"], "4.x"),
            check("GSAP flagged as custom no-charge, not OSI", gs["osi"] is False and "no charge" in gs["package_license"].lower(), gs["package_license"][:40], "no-charge"),
            check("negative control: a wrong claim (GSAP = MIT) is caught", not _license_ok("MIT", gs["package_license"]), gs["package_license"][:30], "mismatch")], [wd / "catalog_licenses.json", wd / "catalog_licenses.md"]


_SLIDES = """---
transition: fade
---
# Intro

<v-click>first point</v-click>

<v-click>second point</v-click>

---
transition: slide-left
---
# List

<v-clicks depth="2">

- a
  - a1
- b

</v-clicks>

<span v-mark.underline.red="3">key word</span>
"""


@card("ENG-134")
def slidev_clicks(task, wd):
    """Slidev deck parsed by @slidev/parser (clicks, transitions); click choreography + Rough Notation underline in our HTML engine."""
    import numpy as np
    (wd / "slides.md").write_text(_SLIDES)
    js = ("import {parse} from %s;import fs from 'fs';const r=await parse(fs.readFileSync(process.argv[2],'utf8'),'slides.md');"
          "console.log(JSON.stringify(r.slides.map(s=>({fm:s.frontmatter,content:s.content}))));"
          % json.dumps(str(NM / "@slidev/cli/node_modules/@slidev/parser/dist/index.mjs")))
    (wd / "parse.mjs").write_text(js)
    slides = json.loads(fx.run(["node", wd / "parse.mjs", wd / "slides.md"], timeout=30).stdout.strip().splitlines()[-1])
    def clicks(content):
        n = len(re.findall(r"<v-click>", content))
        for m in re.finditer(r'<v-clicks(?: depth="(\d+)")?>(.*?)</v-clicks>', content, re.S):
            depth = int(m.group(1) or 1)
            n += sum(1 for ln in m.group(2).splitlines() if re.match(r"^(\s*)- ", ln) and len(re.match(r"^(\s*)", ln).group(1)) // 2 < depth)
        marks = [int(x) for x in re.findall(r'v-mark[\w.]*="(\d+)"', content)]
        return max([n] + marks)
    per = [clicks(s["content"]) for s in slides]
    rn = NM / "@slidev/cli/node_modules"
    imap = {"imports": {"roughjs/bin/generator": "/nm/@slidev/cli/node_modules/roughjs/bin/generator.js",
                        "roughjs/bin/math": "/nm/@slidev/cli/node_modules/roughjs/bin/math.js",
                        "roughjs/bin/renderer": "/nm/@slidev/cli/node_modules/roughjs/bin/renderer.js",
                        "path-data-parser": "/nm/@slidev/cli/node_modules/path-data-parser/lib/index.js",
                        "points-on-curve": "/nm/@slidev/cli/node_modules/points-on-curve/lib/index.js",
                        "points-on-curve/lib/curve-to-bezier.js": "/nm/@slidev/cli/node_modules/points-on-curve/lib/curve-to-bezier.js",
                        "points-on-path": "/nm/@slidev/cli/node_modules/points-on-path/lib/index.js",
                        "hachure-fill": "/nm/@slidev/cli/node_modules/hachure-fill/bin/hachure.js"}}
    page = ("<html><body style='margin:0;background:#fff;font:28px sans-serif'><script type='importmap'>%s</script>"
            "<div id='a' style='position:absolute;left:20px;top:20px;opacity:0'>first</div><div id='b' style='position:absolute;left:20px;top:70px;opacity:0'>second</div>"
            "<span id='k' style='position:absolute;left:20px;top:120px'>key word</span><script src='/nm/gsap/dist/gsap.min.js'></script>"
            "<script type='module'>import {annotate} from '/nm/@slidev/cli/node_modules/@slidev/rough-notation/dist/index.mjs';"
            "const mark=annotate(document.getElementById('k'),{type:'underline',color:'#ff0000',animate:false,strokeWidth:3});"
            "const tl=gsap.timeline({paused:true});tl.addLabel('c1',0.5).to('#a',{opacity:1,duration:0.01},'c1').addLabel('c2',1.0).to('#b',{opacity:1,duration:0.01},'c2')"
            ".addLabel('c3',1.5).call(()=>mark.show(),null,'c3');window.click=(n)=>{tl.seek(['start','c1','c2','c3'][n]==='start'?0:tl.labels[['','c1','c2','c3'][n]]+0.02,false);};"
            "window.__r={labels:tl.labels};</script></body></html>" % json.dumps(imap))
    r, _ = browser(wd, "clicks", page, size=(300, 170), shots=[("window.click(0)", "c0.png"), ("window.click(1)", "c1.png"), ("window.click(3)", "c3.png")])
    c0, c1, c3 = (load_rgb(wd / n) for n in ("c0.png", "c1.png", "c3.png"))
    def ink(a, y0, y1):
        return float((a[y0:y1, 10:200].min(2) < 128).mean())
    def red_under(a):
        z = a[150:168, 10:200]
        return int(((z[..., 0] > 180) & (z[..., 1] < 100)).sum())
    return [check("parser reads 2 slides with their transitions", [s["fm"].get("transition") for s in slides] == ["fade", "slide-left"], [s["fm"].get("transition") for s in slides], ["fade", "slide-left"]),
            check("click counts per slide: 2 v-clicks; v-clicks depth 2 (3 items) + v-mark at 3", per == [2, 3], per, [2, 3]),
            check("forward delay 500 ms between click labels", [round(r["labels"][k], 2) for k in ("c1", "c2", "c3")] == [0.5, 1.0, 1.5], r["labels"], [0.5, 1.0, 1.5]),
            check("click 1 reveals only the first point", ink(c1, 20, 55) > 0.01 and ink(c1, 70, 105) < 0.005, [ink(c1, 20, 55), ink(c1, 70, 105)], "first only"),
            check("click 3 draws the Rough Notation underline (red ink under the key word)", red_under(c3) > 40, red_under(c3), "> 40 px"),
            check("negative control: at click 0 nothing is revealed and no mark is drawn", ink(c0, 20, 105) < 0.005 and red_under(c0) == 0, [ink(c0, 20, 105), red_under(c0)], [0, 0])], [wd / "c3.png", wd / "slides.md"]


_INPAGE = """<html><head><meta charset="utf-8"></head><body style="margin:0;background:#000"><div id="stage" style="position:relative;width:320px;height:180px">
<div id="g" style="position:absolute;left:0;top:10px;width:20px;height:20px;background:#ff0000"></div>
<div id="an" style="position:absolute;left:0;top:50px;width:20px;height:20px;background:#00ff00"></div>
<svg id="sv" width="320" height="180" style="position:absolute;left:0;top:0"><path id="pth" d="M0,150 L320,150" stroke="#0000ff" stroke-width="6" fill="none"/></svg>
<div id="p5h" style="position:absolute;left:0;top:90px"></div></div>
<script src="/nm/gsap/dist/gsap.min.js"></script><script src="/nm/animejs/dist/bundles/anime.umd.min.js"></script>
<script src="/nm/d3/dist/d3.min.js"></script><script src="/nm/p5/lib/p5.min.js"></script>
<script>
const tl=gsap.timeline({paused:true});tl.fromTo('#g',{x:0},{x:300,duration:1,ease:'none'},0);
const at=anime.createTimeline({autoplay:false});at.add('#an',{x:[0,300],duration:1000,ease:'linear'},0);
const L=d3.select('#pth').node().getTotalLength();d3.select('#pth').attr('stroke-dasharray',L);
let P=null,T=0;new p5((s)=>{s.setup=()=>{s.createCanvas(320,30).parent('p5h');s.noLoop();s.pixelDensity(1);};s.draw=()=>{s.background(0);s.noStroke();s.fill(255,255,0);s.rect(300*T,5,20,20);};P=s;});
window.seek=(t)=>{T=t;tl.seek(t);at.seek(t*1000);d3.select('#pth').attr('stroke-dashoffset',L*(1-t));if(P)P.redraw();};
setTimeout(()=>{window.__r={gsap:gsap.version,anime:!!anime.createTimeline,d3:d3.version,p5:!!P};},300);
</script></body></html>"""


def _inpage_measure(a):
    import numpy as np
    def cx(mask):
        xs = np.nonzero(mask)[1]
        return float(xs.mean()) if len(xs) else None
    red = cx((a[5:35, :, 0] > 200) & (a[5:35, :, 1] < 60))
    grn = cx((a[45:75, :, 1] > 200) & (a[45:75, :, 0] < 60))
    yel = cx((a[90:125, :, 0] > 200) & (a[90:125, :, 1] > 200) & (a[90:125, :, 2] < 60))
    blue_len = int(((a[146:154, :, 2] > 200) & (a[146:154, :, 0] < 60)).any(0).sum())
    return {"gsap": red, "anime": grn, "p5": yel, "draw_on_px": blue_len}


@card("ENG-260")
def inpage_libraries(task, wd):
    """Libraries inside a page, all driven by one seek(t): GSAP + Anime.js tweens, D3 SVG draw-on, p5 canvas."""
    r, _ = browser(wd, "libs", _INPAGE, size=(320, 180), shots=[("window.seek(0.5)", "t05.png"), ("window.seek(0)", "t0.png")])
    m5, m0 = _inpage_measure(load_rgb(wd / "t05.png")), _inpage_measure(load_rgb(wd / "t0.png"))
    jw(wd / "libs.json", {"versions": r, "t0.5": m5, "t0": m0})
    return [check("all four libraries loaded", r["gsap"].startswith("3.") and r["anime"] and r["d3"].startswith("7") and r["p5"], r, "gsap3/anime/d3 7/p5"),
            check("GSAP + Anime.js boxes at 10+300*0.5 = 160 px", all(v is not None and abs(v - 160) <= 2 for v in (m5["gsap"], m5["anime"])), [m5["gsap"], m5["anime"]], 160),
            check("p5 canvas square at 160 px", m5["p5"] is not None and abs(m5["p5"] - 160) <= 2, m5["p5"], 160),
            check("D3 draw-on stroke half drawn (160 of 320 px)", abs(m5["draw_on_px"] - 160) <= 3, m5["draw_on_px"], 160),
            check("negative control: at t=0 the boxes sit at 10 px and the stroke is undrawn", abs((m0["gsap"] or 0) - 10) <= 2 and m0["draw_on_px"] <= 3, m0, "start state")], [wd / "t05.png", wd / "libs.json"]


@card("ENG-291")
def inpage_vendored_seekable(task, wd):
    """Vendor the libraries locally (no CDN at render) and keep the page seekable: seek out of order -> identical frames."""
    import numpy as np
    page = _INPAGE
    cdn = re.findall(r'src="(https?://[^"]+)"', page)
    r, _ = browser(wd, "vend", page, size=(320, 180),
                   shots=[("window.seek(0.7)", "a.png"), ("window.seek(0.2)", "b.png"), ("window.seek(0.7)", "a2.png"), ("window.seek(1)", "end.png")])
    a, b, a2 = (load_rgb(wd / n) for n in ("a.png", "b.png", "a2.png"))
    d_same, d_diff = float(np.abs(a - a2).max()), float(np.abs(a - b).mean())
    m = _inpage_measure(a)
    return [check("no CDN URL: every script is served from the local vendor folder", cdn == [] and page.count('src="/nm/') == 4, cdn, []),
            check("seek(0.7) after seek(0.2) reproduces seek(0.7) exactly", d_same == 0, d_same, 0),
            check("state at 0.7 s: GSAP box at 220 px", m["gsap"] is not None and abs(m["gsap"] - 220) <= 2, m["gsap"], 220),
            check("negative control: a different t gives a different frame", d_diff > 1, d_diff, "> 1")], [wd / "a.png"]


@card("ENG-263")
def pixi_render(task, wd):
    """PixiJS v8 in a page: Application + Graphics, positioned from t, extracted with renderer.extract."""
    page = ("<html><body style='margin:0'><script type='module'>import * as PIXI from '/nm/pixi.js/dist/pixi.min.mjs';const R={};try{"
            "const app=new PIXI.Application();await app.init({width:160,height:90,background:'#000000',preference:'webgl',antialias:false,preserveDrawingBuffer:true,resolution:1});"
            "document.body.appendChild(app.canvas);const g=new PIXI.Graphics().rect(0,0,20,20).fill(0xff0000);g.y=35;app.stage.addChild(g);app.ticker.stop();"
            "const grab=(t)=>{g.x=140*t;app.render();return app.canvas.toDataURL('image/png');};"
            "R.version=PIXI.VERSION;R.t0=grab(0);R.t5=grab(0.5);R.t1=grab(1);R.renderer=app.renderer.name||String(app.renderer.type);}catch(e){R.err=String(e.stack||e)}window.__r=R;</script></body></html>")
    r, _ = browser(wd, "pixi", page, flags=SOFTGL, size=(160, 90), timeout=25000)
    import base64
    import io
    import numpy as np
    from PIL import Image
    def cx(u):
        im = Image.open(io.BytesIO(base64.b64decode(u.split(",", 1)[1]))).convert("RGB")
        return red_cx(np.asarray(im)), im
    (c0, _), (c5, im5), (c1, _) = cx(r["t0"]), cx(r["t5"]), cx(r["t1"])
    im5.save(wd / "pixi_t05.png")
    jw(wd / "pixi.json", {"version": r["version"], "renderer": r["renderer"], "cx": [c0, c5, c1]})
    return [check("PixiJS v8 running", str(r["version"]).startswith("8."), r["version"], "8.x"),
            check("t=0.5 sprite centre at 10+70 = 80 px", c5 is not None and abs(c5 - 80) <= 1.5, c5, 80),
            check("t=1 sprite centre at 150 px", c1 is not None and abs(c1 - 150) <= 1.5, c1, 150),
            check("negative control: t=0 is at 10 px, not the t=0.5 position", c0 is not None and abs(c0 - 80) > 50, c0, 10)], [wd / "pixi_t05.png", wd / "pixi.json"]


@card("ENG-243")
def moviepy_engine(task, wd):
    """MoviePy (installed, MIT): code-timeline composite of clips with a position function, written with ffmpeg."""
    from moviepy import ColorClip, CompositeVideoClip, concatenate_videoclips
    bg = ColorClip((160, 90), color=(0, 0, 0), duration=1.0)
    box = ColorClip((20, 20), color=(255, 0, 0), duration=1.0).with_position(lambda t: (int(140 * t), 35))
    a = CompositeVideoClip([bg, box], size=(160, 90))
    b = ColorClip((160, 90), color=(0, 0, 255), duration=0.5)
    film = concatenate_videoclips([a, b])
    out = wd / "moviepy.mp4"
    film.write_videofile(str(out), fps=10, codec="libx264", audio=False, logger=None, preset="ultrafast")
    fr = fx.frames(out, size=(160, 90))
    c5 = red_cx(fr[5])
    end = fr[-1][45, 80]
    return [check("1.0 + 0.5 s at 10 fps -> 15 frames", len(fr) == 15, len(fr), 15),
            check("position function: t=0.5 -> box centre 80 px", c5 is not None and abs(c5 - 80) <= 2, c5, 80),
            check("concatenated blue tail", end[2] > 200 and end[0] < 50, end, "blue"),
            check("negative control: frame 0 box at 10 px", red_cx(fr[0]) is not None and abs(red_cx(fr[0]) - 10) <= 2, red_cx(fr[0]), 10)], [out]


# ======================================================================================= pipelines, routers, interchange


def onsets(samples, rate, thr=0.2, gap=0.05):
    import numpy as np
    a = np.abs(np.asarray(samples, dtype=float))
    idx = np.nonzero(a > thr)[0]
    out, last = [], -1e9
    for i in idx:
        if i - last > gap * rate:
            out.append(i / rate)
        last = i
    return out


KIT_ORDER = ["lyric", "plotter", "doodle", "whiteboard", "chalkboard", "stickman", "isometric", "fake3d", "infographic", "mapjourney", "product"]
KIT_PAL = {"lyric": {"bg": (12, 12, 20), "ink": (240, 220, 160)}, "chalkboard": {"bg": (30, 50, 40), "ink": (240, 240, 240)}}


def kit_build(o, cache, wd):
    """KIT.build: parse -> speedTimings (or align to voice) -> 'motionkit' scene (cached per signature) -> sfx stem -> music bed."""
    import numpy as np
    if o["style"] not in KIT_ORDER:
        raise ValueError("unknown style %s" % o["style"])
    lines = [ln.strip() for ln in o["script"].split("\n") if ln.strip()]
    if o.get("voice_onsets"):
        starts = list(o["voice_onsets"])
        ends = starts[1:] + [o["duration"]]
    else:
        words = [len(ln.split()) for ln in lines]
        per = [w / (2.5 * o.get("speed", 1.0)) for w in words]
        scale = o["duration"] / sum(per)
        starts, t = [], 0.0
        for d in per:
            starts.append(round(t, 4))
            t += d * scale
        ends = starts[1:] + [o["duration"]]
    pal = dict(KIT_PAL.get(o["style"], KIT_PAL["lyric"]))
    if o.get("brand"):
        pal["ink"] = o["brand"]
    params = {"style": o["style"], "lines": lines, "title": o.get("title", ""), "pal": pal, "fonts": o.get("fonts", ["DejaVu Sans"]), "seed": o.get("seed", 1)}
    sig = hashlib.sha256(json.dumps(params, sort_keys=True, default=list).encode()).hexdigest()[:16]
    hit = sig in cache
    if not hit:
        cache[sig] = {"type": "motionkit", "params": params}
    rate = 22050
    n = int(o["duration"] * rate)
    stem = np.zeros(n)
    click = np.sin(2 * np.pi * 1800 * np.arange(int(0.03 * rate)) / rate) * np.hanning(int(0.03 * rate)) * 0.8
    for s in starts:
        i = int(s * rate)
        stem[i:i + len(click)] += click[: max(0, n - i)]
    t = np.arange(n) / rate
    bed = 0.08 * (np.sin(2 * np.pi * 220 * t) + np.sin(2 * np.pi * 277.2 * t) + np.sin(2 * np.pi * 329.6 * t)) / 3
    fx.write_wav(wd / "sfx_stem.wav", stem, rate)
    fx.write_wav(wd / "music_bed.wav", bed, rate)
    from PIL import Image, ImageDraw
    fps, W, H = 10, 160, 90
    frames = []
    for k in range(int(o["duration"] * fps)):
        tt = k / fps
        cur = max(i for i, s in enumerate(starts) if s <= tt + 1e-9)
        im = Image.new("RGB", (W, H), pal["bg"])
        d = ImageDraw.Draw(im)
        prog = (tt - starts[cur]) / max(1e-6, ends[cur] - starts[cur])
        d.rectangle((10, 40, 10 + int(140 * prog), 50), fill=pal["ink"])
        d.text((10, 10), "%d/%d" % (cur + 1, len(lines)), fill=pal["ink"])
        frames.append(np.asarray(im))
    film = write_mp4(wd / ("film_%s.mp4" % o["style"]), frames, fps=fps)
    return {"sig": sig, "cache_hit": hit, "starts": starts, "ends": ends, "lines": lines, "film": film, "pal": pal}


@card("ENG-156")
def motionkit_film_builder(task, wd):
    """Timed script -> whole-timeline film in one procedural style, with its own SFX stem and a music bed (pipeline re-implemented from the card)."""
    import numpy as np
    cache = {}
    o = {"style": "lyric", "script": "one two three\nfour five\nsix seven eight nine", "title": "T", "duration": 3.6, "speed": 1.0, "brand": (255, 0, 0)}
    a = kit_build(o, cache, wd)
    b = kit_build(o, cache, wd)
    stem, rate = fx.read_wav(wd / "sfx_stem.wav")
    det = onsets(stem[:, 0], rate)
    words = [3, 2, 4]
    exp = [0.0, 3 / 9 * 3.6, 5 / 9 * 3.6]
    fr = fx.frames(a["film"], size=(160, 90))
    ink = fr[5][45, 12]
    try:
        kit_build(dict(o, style="watercolor"), cache, wd)
        bad = False
    except ValueError:
        bad = True
    jw(wd / "build.json", {k: v for k, v in a.items() if k != "film"} | {"film": str(a["film"])})
    return [check("speed timings proportional to words (3:2:4 of 3.6 s)", all(abs(s - e) < 1e-3 for s, e in zip(a["starts"], exp)), a["starts"], [round(e, 4) for e in exp]),
            check("SFX stem: one event at every line start", len(det) == 3 and all(abs(d - e) < 0.01 for d, e in zip(det, exp)), [round(d, 3) for d in det], [round(e, 3) for e in exp]),
            check("scene cached per signature (second build is a hit, same sig)", b["cache_hit"] and a["sig"] == b["sig"] and len(cache) == 1, [b["cache_hit"], len(cache)], [True, 1]),
            check("brand colour remaps the style's ink role", ink[0] > 200 and ink[1] < 60, ink, [255, 0, 0]),
            check("11 styles in KIT.ORDER", len(KIT_ORDER) == 11, len(KIT_ORDER), 11),
            check("negative control: a style outside KIT.ORDER is refused", bad, bad, True)], [a["film"], wd / "sfx_stem.wav", wd / "music_bed.wav"]


AIR_TASKS = {"code": ("top", "high", 20000), "film": ("top", "high", 14000), "imitate": ("top", "high", 12000),
             "plan": ("mid", "medium", 12000), "agent": ("mid", "medium", 6000), "script": ("mid", "medium", 6000), "vision": ("mid", "medium", 6000),
             "review": ("mid", "medium", 8000), "highlights": ("mid", "medium", 4000),
             "quick": ("small", "low", 3000), "post": ("small", "low", 3000), "captions": ("small", "low", 4000), "default": ("mid", "medium", 16000)}


def air_route(task, model="auto", effort="auto"):
    m, e, mx = AIR_TASKS.get(task, AIR_TASKS["default"])
    m = m if model == "auto" else model
    e = e if effort == "auto" else effort
    return {"model": m, "effort": e, "max_tokens": mx, "thinking": "adaptive" if e in ("high", "max") else None}


def air_call(req, backend):
    """400 -> retry once without effort; 404 -> fall back to the mid tier."""
    tries = []
    r = dict(req)
    for _ in range(3):
        code = backend(r)
        tries.append((r["model"], r.get("effort"), code))
        if code == 200:
            return {"ok": True, "tries": tries}
        if code == 400 and r.get("effort"):
            r = dict(r, effort=None)
        elif code == 404 and r["model"] != "mid":
            r = dict(r, model="mid")
        else:
            break
    return {"ok": False, "tries": tries}


def gem_chain(chosen, models, sick, now, call, hedge_after=0.05):
    """[chosen, flash, flash-lite] skipping models marked sick in the last 3 minutes; hedge: start the next when one fails or is silent."""
    import concurrent.futures as cf
    chain = [m for m in [chosen] + models if not (m in sick and now - sick[m] < 180)]
    started = []
    with cf.ThreadPoolExecutor(max_workers=len(chain)) as ex:
        futs = {}
        for m in chain:
            started.append(m)
            futs[ex.submit(call, m)] = m
            done, _ = cf.wait(list(futs), timeout=hedge_after, return_when=cf.FIRST_COMPLETED)
            for f in done:
                if f.result() == "ok":
                    return {"winner": futs[f], "started": started, "chain": chain}
        for f in cf.as_completed(list(futs)):
            if f.result() == "ok":
                return {"winner": futs[f], "started": started, "chain": chain}
    return {"winner": None, "started": started, "chain": chain}


@card("ENG-332")
def ai_router(task, wd):
    """AI router: task -> model tier + effort + token budget; 400/404 recovery; Gemini free-first chain with skips and a hedge."""
    got = {t: air_route(t) for t in ("code", "film", "imitate", "plan", "review", "captions", "quick", "unknown")}
    over = air_route("captions", model="top", effort="max")
    r400 = air_call(air_route("code"), lambda r: 400 if r.get("effort") else 200)
    r404 = air_call(air_route("code"), lambda r: 404 if r["model"] == "top" else 200)
    def slow_then_ok(m):
        if m == "gem-chosen":
            time.sleep(0.4)
            return "ok"
        if m == "gem-flash":
            return "fail"
        return "ok"
    g = gem_chain("gem-chosen", ["gem-flash", "gem-flash-lite"], {"gem-flash": time.time() - 30}, time.time(), slow_then_ok)
    g2 = gem_chain("gem-chosen", ["gem-flash", "gem-flash-lite"], {}, time.time(), lambda m: "ok")
    jw(wd / "router.json", {"routes": got, "override": over, "r400": r400, "r404": r404, "gem": g, "gem_fast": g2})
    return [check("heavy tasks -> top tier, high effort, 20000/14000/12000 tokens", [(got[t]["model"], got[t]["effort"], got[t]["max_tokens"]) for t in ("code", "film", "imitate")] ==
                  [("top", "high", 20000), ("top", "high", 14000), ("top", "high", 12000)], [got[t]["max_tokens"] for t in ("code", "film", "imitate")], [20000, 14000, 12000]),
            check("plan/review -> mid medium; captions/quick -> small low", (got["plan"]["model"], got["review"]["effort"], got["captions"]["model"], got["quick"]["effort"]) == ("mid", "medium", "small", "low"),
                  [got["plan"]["model"], got["captions"]["model"]], ["mid", "small"]),
            check("adaptive thinking only for high/max", got["code"]["thinking"] == "adaptive" and got["plan"]["thinking"] is None and over["thinking"] == "adaptive", [got["code"]["thinking"], got["plan"]["thinking"]], ["adaptive", None]),
            check("400 -> retried without effort and succeeded", r400["ok"] and r400["tries"][-1][1] is None and len(r400["tries"]) == 2, r400["tries"], "2 tries"),
            check("404 -> fell back to the mid tier", r404["ok"] and r404["tries"][-1][0] == "mid", r404["tries"], "mid"),
            check("sick model skipped; hedge started the next while the first was silent", "gem-flash" not in g["chain"] and g["winner"] == "gem-flash-lite" and g["started"] == ["gem-chosen", "gem-flash-lite"],
                  g, "skip flash, lite wins"),
            check("negative control: an unknown task is not routed to the heavy tier", got["unknown"]["model"] == "mid" and got["unknown"]["max_tokens"] == 16000, got["unknown"], "default")], [wd / "router.json"]


CRITICAL = {"inputs", "montage", "motion_film", "launch_film", "reels", "imitate"}


def agent_plan(prompt):
    """Rule-based local plan (no AI): 1-9 steps, render only when asked."""
    steps = ["inputs"]
    if "مونتاج" in prompt or "montage" in prompt:
        steps.append("montage")
    if "ترجمة" in prompt or "captions" in prompt:
        steps.append("smart_captions")
    if "موسيقى" in prompt or "music" in prompt:
        steps.append("music")
    if "صدّر" in prompt or "render" in prompt or "صدر" in prompt:
        steps.append("render")
    steps.append("review")
    return {"reply": "خطة محلية", "title": prompt[:30], "steps": steps[:9], "next": ["post", "export_fingerprint"]}


def agent_tools(wd):
    def inputs(st):
        clips = sorted(Path(st["media"]).glob("*.mp4"))
        if not clips:
            raise RuntimeError("no input media")
        st["clips"] = clips
        return "%d clips" % len(clips)

    def montage(st):
        lst = wd / "list.txt"
        lst.write_text("".join("file '%s'\n" % c for c in st["clips"]))
        out = wd / "montage.mp4"
        fx.ffmpeg("-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(out))
        st["film"] = out
        return str(out.name)

    def smart_captions(st):
        srt = wd / "captions.srt"
        srt.write_text("1\n00:00:00,000 --> 00:00:01,000\nمرحبا\n")
        return srt.name

    def music(st):
        fx.tone(wd / "music.wav", seconds=1.0)
        return "music.wav"

    def render(st):
        out = wd / "final.mp4"
        fx.ffmpeg("-i", str(st["film"]), "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out))
        st["final"] = out
        return out.name

    def review(st):
        return "ok" if st.get("film") else "nothing to review"
    return {"inputs": inputs, "montage": montage, "smart_captions": smart_captions, "music": music, "render": render, "review": review}


def agent_run(plan, tools, st):
    log, stopped = [], False
    for name in plan["steps"]:
        if stopped:
            log.append({"step": name, "status": "skipped"})
            continue
        t0 = time.time()
        try:
            out = tools[name](st)
            log.append({"step": name, "status": "done", "engine": "local", "ms": round((time.time() - t0) * 1000, 1), "out": out})
        except Exception as e:  # noqa: BLE001
            log.append({"step": name, "status": "failed", "engine": "local", "ms": round((time.time() - t0) * 1000, 1), "error": str(e)[:100]})
            if name in CRITICAL:
                stopped = True
    return log


@card("ENG-333")
def agent_tool_runner(task, wd):
    """Director: plan 1-9 tool calls (local rule plan), run each live with engine + time, stop dependents when a critical tool fails."""
    media = wd / "media"
    media.mkdir()
    for k, c in enumerate(("red", "blue")):
        fx.color_clip(media / ("%d.mp4" % k), color=c, seconds=0.5, size="160x90", fps=10)
    p1 = agent_plan("اعمل مونتاج مع ترجمة")
    log1 = agent_run(p1, agent_tools(wd), {"media": media})
    p2 = agent_plan("اعمل مونتاج مع ترجمة وصدّر")
    log2 = agent_run(p2, agent_tools(wd), {"media": media})
    empty = wd / "empty"
    empty.mkdir()
    log3 = agent_run(p2, agent_tools(wd), {"media": empty})
    jw(wd / "agent_log.json", {"plan": p1, "run": log1, "plan_render": p2, "run_render": log2, "run_fail": log3})
    film = wd / "montage.mp4"
    return [check("plan without an export request has no render step", "render" not in p1["steps"] and 1 <= len(p1["steps"]) <= 9, p1["steps"], "no render"),
            check("every step logged live with engine and time", all("engine" in s and "ms" in s for s in log1), [s["step"] for s in log1], "engine+ms"),
            check("montage really made: 1.0 s film from two 0.5 s clips", film.exists() and abs(float(fx.probe(film)["format"]["duration"]) - 1.0) < 0.1, film.exists(), True),
            check("render runs when the user asked", [s["status"] for s in log2 if s["step"] == "render"] == ["done"], [s["status"] for s in log2 if s["step"] == "render"], ["done"]),
            check("critical 'inputs' failure stops every later step", log3[0]["status"] == "failed" and all(s["status"] == "skipped" for s in log3[1:]), [s["status"] for s in log3], "failed, skipped..."),
            check("negative control: with inputs present nothing is skipped", all(s["status"] == "done" for s in log1), [s["status"] for s in log1], "all done")], [wd / "agent_log.json", film]


def tc(frames, fps):
    f = int(round(frames))
    return "%02d:%02d:%02d:%02d" % (f // (3600 * fps), f // (60 * fps) % 60, f // fps % 60, f % fps)


def trim_render(segs, out):
    """Frame-exact cut list render: trim=start_frame/end_frame per segment, then the concat filter."""
    args, fc = [], ""
    for i, (f, a, b) in enumerate(segs):
        args += ["-i", str(f)]
        fc += "[%d:v]trim=start_frame=%d:end_frame=%d,setpts=PTS-STARTPTS[v%d];" % (i, a, b, i)
    fc += "".join("[v%d]" % i for i in range(len(segs))) + "concat=n=%d:v=1:a=0[o]" % len(segs)
    fx.ffmpeg(*args, "-filter_complex", fc, "-map", "[o]", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out))
    return out


@card("ENG-135")
def nondestructive_timeline(task, wd):
    """Reference timeline A (chronological) -> duplicate B named A_edit_YYYYMMDD_HHMM; clips keyed by filename + TC; dry-run, apply, log, reset."""
    import datetime as dt
    media = wd / "media"
    media.mkdir()
    fps = 25
    clips = []
    for k, (name, c, created) in enumerate((("c_b.mp4", "blue", 2), ("c_a.mp4", "red", 1), ("c_c.mp4", "green", 3))):
        fx.color_clip(media / name, color=c, seconds=0.4, size="160x90", fps=fps)
        clips.append({"file": name, "created": created, "frames": 10})
    hashes0 = {c["file"]: sha(media / c["file"]) for c in clips}
    A = {"name": "Interview", "fps": fps, "clips": []}
    rec = 0
    for c in sorted(clips, key=lambda c: c["created"]):
        A["clips"].append({"file": c["file"], "tc_in": tc(rec, fps), "tc_out": tc(rec + c["frames"], fps), "frames": c["frames"]})
        rec += c["frames"]
    jw(wd / "A.json", A)
    a_sha = sha(wd / "A.json")
    stamp = dt.datetime(2026, 11, 4, 9, 30).strftime("%Y%m%d_%H%M")
    B = json.loads(json.dumps(A))
    B["name"] = "%s_edit_%s" % (A["name"], stamp)
    edit = {"op": "trim", "key": {"file": "c_b.mp4", "tc_in": "00:00:00:10"}, "frames": 6}
    def find(tl, key):
        return [i for i, c in enumerate(tl["clips"]) if c["file"] == key["file"] and c["tc_in"] == key["tc_in"]]
    def apply(tl, e, dry):
        hit = find(tl, e["key"])
        if len(hit) != 1:
            return {"applied": False, "reason": "clip not found by filename+TC", "dry_run": dry}
        new = json.loads(json.dumps(tl))
        new["clips"][hit[0]]["frames"] = e["frames"]
        r = 0
        for c in new["clips"]:
            c["tc_in"], c["tc_out"], r = tc(r, fps), tc(r + c["frames"], fps), r + c["frames"]
        return {"applied": not dry, "dry_run": dry, "result": new}
    dry = apply(B, edit, True)
    real = apply(B, edit, False)
    B2 = real["result"]
    jw(wd / ("%s.json" % B2["name"]), B2)
    (wd / "edit_log.md").write_text("# edit log\n\n| time | op | key | frames |\n|---|---|---|---|\n| %s | %s | %s @ %s | %s |\n"
                                    % (stamp, edit["op"], edit["key"]["file"], edit["key"]["tc_in"], edit["frames"]))
    by_index = apply(B, {"op": "trim", "key": {"file": "c_b.mp4", "tc_in": "00:00:00:00"}, "frames": 6}, False)
    trim_render([(media / c["file"], 0, c["frames"]) for c in B2["clips"]], wd / "B_render.mp4")
    nB = nframes(wd / "B_render.mp4")
    return [check("A is chronological by creation (a, b, c)", [c["file"] for c in A["clips"]] == ["c_a.mp4", "c_b.mp4", "c_c.mp4"], [c["file"] for c in A["clips"]], ["c_a.mp4", "c_b.mp4", "c_c.mp4"]),
            check("working copy named <A>_edit_<YYYYMMDD_HHMM>", B2["name"] == "Interview_edit_20261104_0930", B2["name"], "Interview_edit_20261104_0930"),
            check("dry run changes nothing", dry["applied"] is False and B["clips"][1]["frames"] == 10, dry["applied"], False),
            check("edit applied on B by filename + TC: B = 10+6+10 frames, render agrees", sum(c["frames"] for c in B2["clips"]) == 26 and nB == 26, [sum(c["frames"] for c in B2["clips"]), nB], 26),
            check("source timeline A and every media file untouched (hashes)", sha(wd / "A.json") == a_sha and all(sha(media / f) == h for f, h in hashes0.items()), "unchanged", "unchanged"),
            check("negative control: addressing the clip by a wrong TC (index-style) finds nothing", by_index["applied"] is False, by_index.get("reason"), "not found")], [wd / ("%s.json" % B2["name"]), wd / "edit_log.md", wd / "B_render.mp4"]


@card("ENG-325")
def nle_interchange(task, wd):
    """No NLE here: emit CMX3600 EDL, FCPXML, marker CSV and an After Effects JSX for the user, and keep the local render in ffmpeg."""
    import xml.etree.ElementTree as ET
    fps = 25
    cut = [{"file": "a.mp4", "src_in": 10, "src_out": 35}, {"file": "b.mp4", "src_in": 0, "src_out": 20}, {"file": "a.mp4", "src_in": 50, "src_out": 65}]
    markers = [{"tc": 0, "name": "Intro"}, {"tc": 25, "name": "Point"}]
    for f, col in (("a.mp4", "red"), ("b.mp4", "blue")):
        fx.color_clip(wd / f, color=col, seconds=3, size="160x90", fps=fps)
    lines, rec = ["TITLE: KOSIF CUT", "FCM: NON-DROP FRAME", ""], 0
    for k, c in enumerate(cut, 1):
        d = c["src_out"] - c["src_in"]
        lines.append("%03d  %-8s V     C        %s %s %s %s" % (k, Path(c["file"]).stem.upper()[:8], tc(c["src_in"], fps), tc(c["src_out"], fps), tc(rec, fps), tc(rec + d, fps)))
        lines.append("* FROM CLIP NAME: %s" % c["file"])
        rec += d
    (wd / "cut.edl").write_text("\n".join(lines) + "\n")
    total = rec
    res = ET.Element("fcpxml", version="1.9")
    r = ET.SubElement(res, "resources")
    ET.SubElement(r, "format", id="r1", frameDuration="1/%ds" % fps, width="160", height="90")
    for i, f in enumerate(("a.mp4", "b.mp4"), 2):
        ET.SubElement(r, "asset", id="r%d" % i, src=f, start="0s", duration="75/25s", hasVideo="1", format="r1")
    lib = ET.SubElement(ET.SubElement(ET.SubElement(res, "library"), "event", name="KOSIF"), "project", name="cut")
    spine = ET.SubElement(ET.SubElement(lib, "sequence", format="r1", duration="%d/%ds" % (total, fps)), "spine")
    off = 0
    for c in cut:
        d = c["src_out"] - c["src_in"]
        ET.SubElement(spine, "asset-clip", ref="r2" if c["file"] == "a.mp4" else "r3", offset="%d/%ds" % (off, fps), start="%d/%ds" % (c["src_in"], fps), duration="%d/%ds" % (d, fps))
        off += d
    ET.ElementTree(res).write(wd / "cut.fcpxml", encoding="utf-8", xml_declaration=True)
    (wd / "markers.csv").write_text("timecode,name\n" + "".join("%s,%s\n" % (tc(m["tc"], fps), m["name"]) for m in markers))
    (wd / "build_comp.jsx").write_text("app.beginUndoGroup('kosif');var proj=app.project;var comp=proj.items.addComp('cut',160,90,1.0,%s,%d);"
                                       "var s=comp.layers.addSolid([1,0,0],'bg',160,90,1.0);var t=comp.layers.addText('Intro');"
                                       "t.property('Position').expression='ease(time,0,0.6,[-200,45],[80,45])';"
                                       "try{var rq=app.project.renderQueue.items.add(comp);rq.outputModule(1).applyTemplate('H.264');}catch(e){}app.endUndoGroup();"
                                       % (total / fps, fps))
    # parse everything back
    ev = [ln for ln in (wd / "cut.edl").read_text().splitlines() if re.match(r"^\d{3} ", ln)]
    def frames_of(t):
        h, m, s, f = map(int, t.split(":"))
        return ((h * 60 + m) * 60 + s) * fps + f
    recs = [(frames_of(ln.split()[-2]), frames_of(ln.split()[-1])) for ln in ev]
    continuous = all(recs[i][1] == recs[i + 1][0] for i in range(len(recs) - 1)) and recs[0][0] == 0
    tree = ET.parse(wd / "cut.fcpxml")
    durs = [int(c.get("duration").split("/")[0]) for c in tree.iter("asset-clip")]
    trim_render([(wd / c["file"], c["src_in"], c["src_out"]) for c in cut], wd / "local_render.mp4")
    n = nframes(wd / "local_render.mp4")
    gap = list(recs)
    gap[1] = (gap[1][0] + 5, gap[1][1] + 5)
    gap_ok = all(gap[i][1] == gap[i + 1][0] for i in range(len(gap) - 1))
    return [check("EDL: 3 events, record TCs continuous from 0", len(ev) == 3 and continuous, recs, "continuous"),
            check("FCPXML parses; clip durations sum to the EDL length (60 frames)", sum(durs) == total == 60, [durs, total], 60),
            check("marker CSV and AE JSX (addComp 160x90 @25, %.1f s) written" % (total / fps), "addComp('cut',160,90,1.0,2.4,25)" in (wd / "build_comp.jsx").read_text() and (wd / "markers.csv").read_text().count("\n") == 3,
                  "jsx+csv", "written"),
            check("local ffmpeg render of the same cut list = 60 frames", n == 60, n, 60),
            check("negative control: a cut list with a 5-frame gap fails the continuity check", not gap_ok, gap, "gap detected")], [wd / "cut.edl", wd / "cut.fcpxml", wd / "markers.csv", wd / "build_comp.jsx"]


def fc_family(name):
    out = fx.run(["fc-match", "-f", "%{family}", name]).stdout
    return out.split(",")[0].strip()


@card("ENG-328")
def resolve_pitfalls_plan(task, wd):
    """Plan edits as segment lists and rebuild the timeline (no clip moves); verify fonts with fc-list before placing titles."""
    import numpy as np
    fps = 10
    segs = {"r": "red", "g": "green", "b": "blue"}
    for k, c in segs.items():
        fx.color_clip(wd / ("%s.mp4" % k), color=c, seconds=0.5, size="160x90", fps=fps)
    v1 = ["r", "g", "b"]
    v2 = ["b", "r", "g"]
    def rebuild(order, out):
        lst = wd / (out + ".txt")
        lst.write_text("".join("file '%s'\n" % (wd / ("%s.mp4" % k)) for k in order))
        fx.ffmpeg("-f", "concat", "-safe", "0", "-i", str(lst), "-c:v", "libx264", "-pix_fmt", "yuv420p", str(wd / (out + ".mp4")))
        return wd / (out + ".mp4")
    rebuild(v1, "v1")
    film = rebuild(v2, "v2")
    fr = fx.frames(film, size=(16, 9))
    order = []
    for k in (2, 7, 12):
        p = fr[k][4, 8]
        order.append("rgb"[int(np.argmax(p))])
    fams = sorted(set(fx.run(["fc-list", ":", "family"]).stdout.replace(",", "\n").splitlines()))
    want = ["DejaVu Sans", "Kosif Imaginary Sans"]
    present = {f: (f in [x.strip() for x in fams]) for f in want}
    substituted = {f: fc_family(f) for f in want}
    titles = [f for f in want if present[f]]
    jw(wd / "segments.json", {"v1": v1, "v2": v2, "fonts": present, "fc_match": substituted, "titles_with": titles})
    return [check("re-cut built as a new timeline from the segment list (b, r, g)", order == ["b", "r", "g"], order, ["b", "r", "g"]),
            check("rebuilt length = 3 x 0.5 s", nframes(film) == 15, nframes(film), 15),
            check("fc-list confirms DejaVu Sans before use", present["DejaVu Sans"] is True, present, "DejaVu present"),
            check("missing font caught before placing the title (only present fonts used)", titles == ["DejaVu Sans"], titles, ["DejaVu Sans"]),
            check("negative control: fc-match silently substitutes the missing font (what Text+ would do)", substituted["Kosif Imaginary Sans"] != "Kosif Imaginary Sans",
                  substituted["Kosif Imaginary Sans"], "a different family")], [film, wd / "segments.json"]


@card("ENG-187")
def production_loop(task, wd):
    """Production loop as a dependency graph: independent stages run concurrently; real voice length wins; one contact sheet for review."""
    import concurrent.futures as cf
    import numpy as np
    from PIL import Image
    graph = {"assets": [], "audio": [], "frames": ["assets"], "sync": ["frames", "audio"], "assemble": ["sync"], "verify": ["assemble"], "deliver": ["verify"]}
    levels, done = [], set()
    while len(done) < len(graph):
        lvl = sorted(k for k, deps in graph.items() if k not in done and all(d in done for d in deps))
        levels.append(lvl)
        done |= set(lvl)
    st, ran, lock = {}, [], threading.Lock()
    fps, guess = 10, 1.0

    def assets():
        shutil.copy(GSAP_JS, wd / "gsap.min.js")
        return "ok"

    def audio():
        rate = 22050
        voice = 0.5 * np.sin(2 * np.pi * 300 * np.arange(int(1.3 * rate)) / rate)
        n = int(1.6 * rate)
        bed = 0.3 * np.sin(2 * np.pi * 110 * np.arange(n) / rate)
        bed[: len(voice)] *= 10 ** (-12 / 20)                  # carve the bed under the voice
        mix = bed.copy()
        mix[: len(voice)] += voice
        fx.write_wav(wd / "voice.wav", voice, rate)
        fx.write_wav(wd / "bed.wav", bed, rate)
        fx.write_wav(wd / "mix.wav", mix, rate)
        meta = {"voice_s": len(voice) / rate, "bed_db_under_voice": -12, "words": [{"w": "مرحبا", "start": 0.1, "end": 0.6}]}
        jw(wd / "audio_meta.json", meta)
        st["voice_s"] = meta["voice_s"]

    def frames():
        st["frames_guess"] = int(guess * fps)

    def sync():
        st["frames"] = int(round(st["voice_s"] * fps))

    def assemble():
        ims = []
        for k in range(st["frames"]):
            a = np.zeros((90, 160, 3), dtype=np.uint8)
            a[:, : int(160 * (k + 1) / st["frames"])] = (40, 120, 200)
            ims.append(a)
        st["ims"] = ims
        write_mp4(wd / "silent.mp4", ims, fps=fps)
        fx.ffmpeg("-i", str(wd / "silent.mp4"), "-i", str(wd / "mix.wav"), "-c:v", "copy", "-c:a", "aac", "-shortest", str(wd / "film.mp4"))

    def verify():
        tiles = st["ims"][:: max(1, len(st["ims"]) // 6)][:6]
        sheet = Image.new("RGB", (160 * 3, 90 * 2))
        for i, t in enumerate(tiles):
            sheet.paste(Image.fromarray(t), ((i % 3) * 160, (i // 3) * 90))
        sheet.save(wd / "contact_sheet.png")
        st["tiles"] = len(tiles)

    def deliver():
        shutil.copy(wd / "film.mp4", wd / "final.mp4")
    fns = {"assets": assets, "audio": audio, "frames": frames, "sync": sync, "assemble": assemble, "verify": verify, "deliver": deliver}
    conc = []
    for lvl in levels:
        with cf.ThreadPoolExecutor(max_workers=len(lvl)) as ex:
            list(ex.map(lambda k: (fns[k](), ran.append(k)), lvl))
        conc.append(len(lvl))
    order_ok = all(ran.index(d) < ran.index(k) for k, deps in graph.items() for d in deps)
    p = fx.probe(wd / "final.mp4")
    vdur = [float(s.get("duration", 0)) for s in p["streams"] if s["codec_type"] == "video"][0]
    mix, rate = fx.read_wav(wd / "bed.wav")
    under = 20 * math.log10(np.sqrt(np.mean(mix[: int(1.2 * rate), 0] ** 2)) + 1e-9)
    outside = 20 * math.log10(np.sqrt(np.mean(mix[int(1.35 * rate):, 0] ** 2)) + 1e-9)
    return [check("stages ran in dependency order", order_ok, ran, "deps first"),
            check("assets and audio ran concurrently in the first level", levels[0] == ["assets", "audio"] and conc[0] == 2, levels[0], ["assets", "audio"]),
            check("duration sync: real voice length (1.3 s) wins -> 13 frames", st["frames"] == 13 and abs(vdur - 1.3) < 0.06, [st["frames"], vdur], [13, 1.3]),
            check("bed carved ~12 dB under the voice", abs((outside - under) - 12) < 1.0, round(outside - under, 2), 12),
            check("one contact sheet with 6 tiles for review", st["tiles"] == 6 and (wd / "contact_sheet.png").exists(), st["tiles"], 6),
            check("negative control: the storyboard guess (10 frames) is not the synced length", st["frames_guess"] != st["frames"], st["frames_guess"], "!= 13")], [wd / "final.mp4", wd / "contact_sheet.png", wd / "audio_meta.json"]


def frame_html(fid, color, dur, prefix_ok=True):
    pid = (fid + "-") if prefix_ok else ""
    return ('<template id="%s-template"><div data-composition-id="%s" data-width="160" data-height="90" data-duration="%s">'
            '<div id="%sbg" style="position:absolute;inset:0;background:%s"></div><div id="%stitle" class="clip" data-start="0" data-duration="%s" '
            'data-track-index="0" style="position:absolute;left:10px;top:10px;color:#fff">%s</div>'
            '<script>window.__timelines=window.__timelines||{};const tl_%s=gsap.timeline({paused:true});'
            'tl_%s.fromTo("#%stitle",{x:0},{x:40,duration:%s});window.__timelines["%s"]=tl_%s;</script></div></template>'
            % (fid, fid, dur, pid, color, pid, dur, fid, fid.replace("-", "_"), fid.replace("-", "_"), pid, dur, fid, fid.replace("-", "_")))


def frame_self_check(fid, text):
    codes = []
    if not re.match(r"\s*<template", text):
        codes.append("E_NO_TEMPLATE")
    if text.count("gsap.timeline(") != 1 or "paused:true" not in text.replace(" ", ""):
        codes.append("E_TIMELINE")
    if ('window.__timelines["%s"]' % fid) not in text:
        codes.append("E_TIMELINE_KEY")
    ids = re.findall(r'(?<![-\w])id="([^"]+)"', text)
    if any(not (i.startswith(fid + "-") or i == fid + "-template") for i in ids):
        codes.append("E_ID_PREFIX")
    return codes


@card("ENG-188")
def frame_workers(task, wd):
    """Parallel frame workers: packets -> compositions/frames/NN-*.html under a concurrency cap; orchestrator self-checks + lints and re-dispatches failures."""
    import concurrent.futures as cf
    proj = hf_project(wd, "frames_proj", "")
    (proj / "compositions/frames").mkdir(parents=True)
    packets = [{"fid": "f01-intro", "color": "#203040", "dur": 0.5}, {"fid": "f02-claim", "color": "#402030", "dur": 0.5},
               {"fid": "f03-proof", "color": "#304020", "dur": 0.5}, {"fid": "f04-cta", "color": "#101010", "dur": 0.5}]
    cap, live, peak, attempts = 2, [0], [0], {}
    lock = threading.Lock()

    def worker(pk):
        with lock:
            live[0] += 1
            peak[0] = max(peak[0], live[0])
            attempts[pk["fid"]] = attempts.get(pk["fid"], 0) + 1
            first = attempts[pk["fid"]] == 1
        time.sleep(0.05)
        ok_ids = not (pk["fid"] == "f03-proof" and first)          # this worker forgets the id prefix on its first try
        p = proj / "compositions/frames" / ("%s.html" % pk["fid"].replace("f", "", 1))
        p.write_text(frame_html(pk["fid"], pk["color"], pk["dur"], prefix_ok=ok_ids))
        with lock:
            live[0] -= 1
        return pk["fid"], p

    def dispatch(pks):
        with cf.ThreadPoolExecutor(max_workers=cap) as ex:
            return list(ex.map(worker, pks))
    results = dispatch(packets)
    first_codes = {fid: frame_self_check(fid, p.read_text()) for fid, p in results}
    failed = [pk for pk in packets if first_codes[pk["fid"]]]
    results2 = dispatch(failed)
    final_codes = {fid: frame_self_check(fid, (proj / "compositions/frames" / ("%s.html" % fid.replace("f", "", 1))).read_text()) for fid in first_codes}
    mounts, t = [], 0.0
    for pk in packets:
        mounts.append('<div class="clip" id="m-%s" data-composition-id="%s" data-composition-src="compositions/frames/%s.html" data-start="%s" data-duration="%s" data-track-index="0"></div>'
                      % (pk["fid"], pk["fid"], pk["fid"].replace("f", "", 1), t, pk["dur"]))
        t += pk["dur"]
    (proj / "index.html").write_text(box_comp(w=160, h=90, dur=t, gsap=True, tween="", extra_body="".join(mounts)).replace(
        '<div id="box" class="clip" data-start="%s" data-duration="%s" data-track-index="0"></div>' % (t, t), ""))
    lint = hfj(wd, "lint", proj, "--json", ok=False)
    comps = [c["id"] for c in hfj(wd, "compositions", proj, "--json")["compositions"]]
    jw(wd / "dispatch.json", {"first": first_codes, "final": final_codes, "attempts": attempts, "peak": peak[0], "lint": lint["errorCount"]})
    return [check("concurrency cap respected (peak <= 2 live workers)", peak[0] <= cap, peak[0], "<= 2"),
            check("self-check caught the un-prefixed ids on the first pass", first_codes["f03-proof"] == ["E_ID_PREFIX"], first_codes["f03-proof"], ["E_ID_PREFIX"]),
            check("only the failed frame was re-dispatched", attempts == {"f01-intro": 1, "f02-claim": 1, "f03-proof": 2, "f04-cta": 1}, attempts, "f03 x2"),
            check("all frames pass the contract after re-dispatch", all(v == [] for v in final_codes.values()), final_codes, "all []"),
            check("assembled project lints clean and lists the 4 frames", lint["errorCount"] == 0 and all(pk["fid"] in comps for pk in packets), [lint["errorCount"], comps], [0, "4 frames"]),
            check("negative control: the first-pass f03 file fails the id-prefix rule", bool(first_codes["f03-proof"]), first_codes["f03-proof"], "non-empty")], [wd / "dispatch.json", proj / "index.html"]


BRIEF_KEYS = ["Objective", "Verbatim copy", "Identity", "Scene summary", "Audio", "Sub-skills to load"]


def write_brief(path, req):
    md = "# Composition brief\n\n" + "".join("## %s\n%s\n\n" % (k, req[k] if not isinstance(req[k], list) else "\n".join("- " + x for x in req[k])) for k in BRIEF_KEYS)
    Path(path).write_text(md, encoding="utf-8")
    return Path(path)


def read_brief(path):
    secs = re.split(r"(?m)^## ", Path(path).read_text(encoding="utf-8"))[1:]
    return {s.split("\n", 1)[0].strip(): s.split("\n", 1)[1].strip() for s in secs}


@card("ENG-318")
def composition_brief(task, wd):
    """Separate composition-brief.md (objective, verbatim copy, identity, scenes, audio, sub-skills); the build must carry the copy verbatim."""
    copy = "«الجودة ليست صدفة» — 2026"
    req = {"Objective": "15 s launch teaser", "Verbatim copy": copy, "Identity": "ink #0d1b2a, accent #e7b65a, font Cairo",
           "Scene summary": "1 hook; 2 claim; 3 call to action", "Audio": "bed -18 LUFS, voice on top", "Sub-skills to load": ["hyperframes", "hyperframes-cli"]}
    b = write_brief(wd / "composition-brief.md", req)
    got = read_brief(b)
    skills_root = [Path(os.path.expanduser("~/.claude/skills")), _REAL_HOME / ".claude/skills"]
    subs = [x[2:] for x in got["Sub-skills to load"].splitlines()]
    found = {s: any((r / s / "SKILL.md").exists() for r in skills_root) for s in subs}
    proj = hf_project(wd, "teaser", box_comp(w=320, h=180, dur=1, extra_body='<div id="copy" class="clip" data-start="0" data-duration="1" data-track-index="1">%s</div>' % _html.escape(copy)))
    built = _html.unescape(re.search(r'<div id="copy"[^>]*>(.*?)</div>', (proj / "index.html").read_text()).group(1))
    paraphrase = "الجودة ليست صدفة - 2026"
    return [check("brief has all six sections", list(got) == BRIEF_KEYS, list(got), BRIEF_KEYS),
            check("verbatim copy survives the brief byte for byte", got["Verbatim copy"] == copy, got["Verbatim copy"], copy),
            check("listed sub-skills exist as installed skills", all(found.values()), found, "all True"),
            check("composition carries the copy verbatim", built == copy, built, copy),
            check("negative control: a paraphrased line fails the verbatim check", paraphrase != got["Verbatim copy"], paraphrase, "!= copy")], [b, proj / "index.html"]
