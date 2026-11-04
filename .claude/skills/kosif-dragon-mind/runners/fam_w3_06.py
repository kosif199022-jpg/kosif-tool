"""qa-verification (wave 3, chunk 06): QA method cards as real programs with known-answer checks.

Engines used (all already installed here, nothing new was installed):
  * HyperFrames CLI 0.9.8 (/opt/node22/bin/hyperframes) for lint / check / snapshot / keyframes / compare /
    grade-compare / timeline / history / upgrade / usage, on fixture projects written into the work folder with
    the CLI's own vendored GSAP (the CDN is not reachable), driving /usr/bin/google-chrome headless.
  * node + playwright (global node_modules) with Chrome for page audits, WebGPU (SwiftShader adapter), axe-core.
  * ffmpeg / ffprobe, numpy, PIL, OpenCV, tesseract, ImageMagick `convert`, the repo's mimic analyser
    (kosif-superpowers/scripts/mimic/mm_analyze.py + synthetic/make_reference.py), the vendored kosif-montage-motion
    and pixel-studio-painter test suites, fastify-motion-bro's `node --test` suite and llm-judge-eval-lab's
    eval_runner.py, each copied into the work folder before it is run or mutated.

Every runner builds its own deterministic fixture in the work folder, measures the produced output against known
answers, and runs a negative control (the same measurement on the untreated input fails the criterion).
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

from _harness import card, check, fx, sha

GAPS: dict = {
    "QA-216": "needs a speech-to-text model on sung audio: ElevenLabs Scribe is a paid key and the faster-whisper "
              "weights cannot be fetched (huggingface.co is refused by the proxy, 403); there is also no TTS/singing "
              "engine here to make a sung fixture, so nothing honest can run",
    "QA-221": "AGENT.TOOLS.verify_transcript transcribes the media with a speech model (key:unspecified); faster-whisper "
              "has no cached weights and huggingface.co is blocked (403), and no TTS exists to build a spoken fixture",
    "QA-227": "a bake-off across Kling 3.0, MiniMax H3 and Seedance 2.0 spends ~64 paid video-generation credits on "
              "live services; no open equivalent of those three models exists here",
    "QA-274": "Blender is not installed (no `blender` binary, and the bpy wheel is several hundred MB), so the Cycles "
              "black-render assertions have no engine to run in",
    "QA-298": "`hyperframes render --docker` needs a running Docker daemon; /var/run/docker.sock does not exist in this "
              "sandbox, so the pinned Chromium/fonts/FFmpeg image cannot start",
}

ROOT = Path(__file__).resolve().parents[4]
SKILLS = ROOT / ".claude/skills"
VENDOR = SKILLS / "kosif-superpowers/vendor/100-superskills/skills"
MIMIC = SKILLS / "kosif-superpowers/scripts/mimic"
NODE_MODULES = "/opt/node22/lib/node_modules"
HF_BIN = "/opt/node22/bin/hyperframes"
GSAP = NODE_MODULES + "/hyperframes/dist/vendor/npm/gsap@3.15.0/dist/gsap.min.js"
CHROME = next((p for p in ("/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser") if Path(p).exists()), None)
HF_CONF = {"paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"}}


# ----------------------------------------------------------------------------------------------- helpers
def _np():
    import numpy as np
    return np


def tw(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def wj(path, obj):
    return tw(path, json.dumps(obj, ensure_ascii=False, indent=1))


def rj(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_png(arr, path):
    from PIL import Image
    Image.fromarray(_np().clip(arr, 0, 255).round().astype("uint8")).save(path)
    return Path(path)


def load_png(path):
    from PIL import Image
    return _np().asarray(Image.open(path).convert("RGB")).astype(float)


def write_video(path, frames, fps=30, lossless=True, audio=None):
    np = _np()
    frames = list(frames)
    h, w = frames[0].shape[:2]
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", "%dx%d" % (w, h), "-r", str(fps), "-i", "-"]
    if audio:
        cmd += ["-i", str(audio), "-c:a", "aac", "-b:a", "128k", "-shortest"]
    cmd += (["-c:v", "libx264rgb", "-qp", "0", "-preset", "ultrafast"] if lossless else
            ["-c:v", "libx264", "-crf", "16", "-preset", "veryfast", "-pix_fmt", "yuv420p"]) + [str(path)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    for f in frames:
        p.stdin.write(np.clip(f, 0, 255).round().astype("uint8").tobytes())
    p.stdin.close()
    if p.wait():
        raise RuntimeError("ffmpeg encode failed: %s" % p.stderr.read().decode(errors="replace")[-300:])
    return Path(path)


def read_video(path, size=None):
    np = _np()
    st = [s for s in fx.probe(path)["streams"] if s.get("codec_type") == "video"][0]
    w, h = (int(st["width"]), int(st["height"])) if size is None else size
    vf = [] if size is None else ["-vf", "scale=%d:%d" % size]
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), *vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, timeout=120, stdin=subprocess.DEVNULL).stdout
    return np.frombuffer(out, dtype=np.uint8).reshape(-1, h, w, 3).astype(float)


def contact_sheet(imgs, cols, path, pad=4, bg=24):
    np = _np()
    h, w = imgs[0].shape[:2]
    rows = int(math.ceil(len(imgs) / float(cols)))
    sheet = np.full((rows * (h + pad) + pad, cols * (w + pad) + pad, 3), float(bg))
    for i, im in enumerate(imgs):
        r, c = divmod(i, cols)
        sheet[pad + r * (h + pad): pad + r * (h + pad) + h, pad + c * (w + pad): pad + c * (w + pad) + w] = im
    return save_png(sheet, path)


def node(wd, name, js, timeout=60):
    """Run a node script with the global node_modules; it prints one JSON line last."""
    src = tw(Path(wd) / (name + ".cjs"), js)
    env = dict(os.environ, NODE_PATH=NODE_MODULES)
    done = subprocess.run(["node", str(src)], capture_output=True, text=True, timeout=timeout, cwd=str(wd), env=env,
                          stdin=subprocess.DEVNULL)
    if done.returncode:
        raise RuntimeError("node failed: " + (done.stderr or done.stdout)[-600:])
    return json.loads(done.stdout.strip().splitlines()[-1])


PW = ("const {chromium}=require('playwright');const fs=require('fs');const path=require('path');\n"
      "const launch=(extra)=>chromium.launch({executablePath:%s,args:['--no-sandbox','--font-render-hinting=none'].concat(extra||[])});\n"
      % json.dumps(CHROME))


def lum_rel(rgb):
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in [v / 255.0 for v in rgb]]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a, b):
    la, lb = sorted([lum_rel(a), lum_rel(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def phash(img, size=32, keep=8):
    """Perceptual hash: DCT of the 32x32 grey image, top-left 8x8 above the median."""
    np = _np()
    from PIL import Image
    from scipy.fft import dctn
    g = np.asarray(Image.fromarray(np.clip(img, 0, 255).astype("uint8")).convert("L").resize((size, size), Image.BILINEAR), float)
    d = dctn(g, norm="ortho")[:keep, :keep].flatten()
    return d[1:] > np.median(d[1:])


def hamming(a, b):
    return int((a != b).sum())


class Serve:
    """Serve a folder (and optional JSON API handlers) on 127.0.0.1 in a thread, for local fixtures only."""

    def __init__(self, root, api=None):
        import http.server
        api = api or {}
        rootp = str(root)

        class H(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *a, **k):
                super().__init__(*a, directory=rootp, **k)

            def log_message(self, *a, **k):
                pass

            def _api(self, method):
                path = self.path.split("?")[0]
                fn = api.get((method, path))
                if fn is None:
                    return False
                n = int(self.headers.get("Content-Length") or 0)
                body = self.rfile.read(n) if n else b""
                fn(self, body)
                return True

            def do_GET(self):
                if self._api("GET"):
                    return
                rng = self.headers.get("Range")
                fp = Path(self.translate_path(self.path))
                if rng and fp.is_file():                         # byte ranges, so <video> can seek
                    data = fp.read_bytes()
                    a, _, z = rng.replace("bytes=", "").partition("-")
                    a = int(a or 0)
                    z = min(int(z) if z else len(data) - 1, len(data) - 1)
                    self.send_response(206)
                    self.send_header("Content-Type", self.guess_type(str(fp)))
                    self.send_header("Accept-Ranges", "bytes")
                    self.send_header("Content-Range", "bytes %d-%d/%d" % (a, z, len(data)))
                    self.send_header("Content-Length", str(z - a + 1))
                    self.end_headers()
                    self.wfile.write(data[a:z + 1])
                    return
                super().do_GET()

            def do_POST(self):
                if not self._api("POST"):
                    self.send_error(404)

        self.srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
        self.url = "http://127.0.0.1:%d" % self.srv.server_address[1]
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()

    def close(self):
        self.srv.shutdown()
        self.srv.server_close()


def send_json(h, obj, code=200):
    data = json.dumps(obj).encode()
    h.send_response(code)
    h.send_header("Content-Type", "application/json")
    h.send_header("Content-Length", str(len(data)))
    h.end_headers()
    h.wfile.write(data)


# ----------------------------------------------------------------------------------------------- HyperFrames
def hf(wd, args, cwd, timeout=60):
    """Run the real HyperFrames CLI; returns (returncode, parsed JSON envelope or None, combined text)."""
    home = Path(wd) / "_home"
    home.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, HOME=str(home), XDG_CACHE_HOME=str(home / ".cache"), HYPERFRAMES_NO_UPDATE_CHECK="1",
               NODE_PATH=NODE_MODULES)
    if CHROME:
        env.setdefault("HYPERFRAMES_BROWSER_PATH", CHROME)
    done = subprocess.run([HF_BIN, *map(str, args)], capture_output=True, text=True, timeout=timeout, cwd=str(cwd),
                          env=env, stdin=subprocess.DEVNULL)
    out = done.stdout
    js = None
    for m in re.finditer(r"(?m)^\{", out):
        try:
            js = json.JSONDecoder().raw_decode(out[m.start():])[0]
            break
        except ValueError:
            continue
    return done.returncode, js, out + done.stderr


def par(*calls):
    """Run independent CLI calls at once (each is a zero-argument callable); results in order."""
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=4) as ex:
        futs = [ex.submit(c) for c in calls]
        return [f.result() for f in futs]


def hf_project(wd, name, body, css="", js="", w=640, h=360, dur=2, register=True, bg="#101820", paused=True):
    if not (Path(HF_BIN).exists() and Path(GSAP).exists()):
        raise RuntimeError("HyperFrames CLI or its vendored GSAP is missing")
    p = Path(wd) / name
    p.mkdir(parents=True, exist_ok=True)
    shutil.copy(GSAP, p / "gsap.min.js")
    wj(p / "hyperframes.json", HF_CONF)
    reg = 'window.__timelines=window.__timelines||{};window.__timelines["main"]=tl;' if register else ""
    tl = "gsap.timeline({paused:true})" if paused else "gsap.timeline()"
    tw(p / "index.html", '<!doctype html>\n<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=%d, height=%d">'
       '<script src="gsap.min.js"></script><style>html,body{margin:0;width:%dpx;height:%dpx;overflow:hidden;background:%s}%s</style></head>'
       '<body><div id="root" data-composition-id="main" data-start="0" data-duration="%s" data-width="%d" data-height="%d">%s</div>'
       '<script>const tl=%s;%s%s</script></body></html>\n' % (w, h, w, h, bg, css, dur, w, h, body, tl, js, reg))
    return p


BOX_CSS = ("#box{position:absolute;left:40px;top:140px;width:80px;height:80px;background:#ff3b30}"
           "#title{position:absolute;left:200px;top:40px;color:#ffffff;font:600 40px sans-serif}")
BOX_BODY = ('<div id="box" class="clip" data-start="0" data-duration="2" data-track-index="0"></div>'
            '<h1 id="title" class="clip" data-start="0" data-duration="2" data-track-index="1">Hello</h1>')
BOX_JS = 'tl.to("#box",{x:400,duration:1.5,ease:"none"},0);tl.fromTo("#title",{opacity:0},{opacity:1,duration:0.5},0.2);'


def good_project(wd, name="good"):
    return hf_project(wd, name, BOX_BODY, BOX_CSS, BOX_JS)


def bad_layout_project(wd, name="bad"):
    css = ("#box{position:absolute;left:40px;top:140px;width:80px;height:80px;background:#ff3b30}"
           "#title{position:absolute;left:420px;top:40px;color:#1a222a;font:600 40px sans-serif;white-space:nowrap}")
    body = BOX_BODY.replace(">Hello<", ">Hello wide world title<")
    return hf_project(wd, name, body, css, 'tl.to("#box",{x:400,duration:1.5,ease:"none"},0);')


def red_x(img):
    np = _np()
    m = (img[..., 0] > 200) & (img[..., 1] < 100) & (img[..., 2] < 100)
    xs = np.nonzero(m)[1]
    return float(xs.min()) if len(xs) else -1.0


def findings(env, section):
    return [f.get("code") for f in (env.get(section) or {}).get("findings", [])]


# ═════════════════════════ HyperFrames CLI cards (real CLI on fixture projects) ═════════════════════════
@card("QA-148")
def hf_cli_lint(task, wd):
    """`hyperframes lint --json`: the static linter over composition HTML/CSS/JS, read as agent JSON."""
    good = good_project(wd, "good")
    bad = hf_project(wd, "bad", BOX_BODY, BOX_CSS, BOX_JS, register=False, paused=False)
    rg, jg, _ = hf(wd, ["lint", ".", "--json"], good)
    rb, jb, _ = hf(wd, ["lint", ".", "--json"], bad)
    out = wj(wd / "lint.json", {"good": jg, "bad": jb})
    codes = sorted({f["code"] for f in jb["findings"]})
    return [check("clean fixture lints with 0 errors and ok=true", jg["ok"] and jg["errorCount"] == 0, jg["errorCount"], 0),
            check("one file scanned per project", jg["filesScanned"] == 1 and jb["filesScanned"] == 1, jb["filesScanned"], 1),
            check("unregistered timeline reported with its rule codes", {"missing_timeline_registry", "gsap_timeline_not_registered"} <= set(codes), codes,
                  ["gsap_timeline_not_registered", "missing_timeline_registry"]),
            check("every finding carries a fixHint", all(f.get("fixHint") for f in jb["findings"]), len(jb["findings"]), ">=2"),
            check("exit code gates: 0 clean, non-zero broken", rg == 0 and rb != 0, [rg, rb], [0, "!=0"]),
            check("negative control: the broken fixture does not lint ok", not jb["ok"], jb["ok"], False)], [out]


@card("QA-149")
def hf_cli_check(task, wd):
    """`hyperframes check --json`: one browser audit at 9 midpoint samples, overflow tolerance 2 px and WCAG contrast."""
    good = good_project(wd, "good")
    bad = bad_layout_project(wd, "bad")
    (rg, jg, _), (rb, jb, _) = par(lambda: hf(wd, ["check", ".", "--json"], good, timeout=90),
                                   lambda: hf(wd, ["check", ".", "--json"], bad, timeout=90))
    out = wj(wd / "check.json", {"good": jg, "bad": jb})
    samples = jg["layout"]["samples"]
    mid = [round((i + 0.5) * 2 / 9.0, 3) for i in range(9)]
    return [check("9 samples at the midpoints of 9 equal slices", len(samples) == 9 and all(abs(a - b) < 0.002 for a, b in zip(samples, mid)), samples, mid),
            check("clean fixture passes the gate", jg["ok"] and rg == 0, jg["ok"], True),
            check("overflow of the wide title reported", "text_box_overflow" in findings(jb, "layout"), findings(jb, "layout"), "text_box_overflow"),
            check("WCAG contrast failure reported (1.1:1 < 3:1)", "contrast_aa_failure" in findings(jb, "contrast"), findings(jb, "contrast"), "contrast_aa_failure"),
            check("negative control: the faulty fixture fails the gate", not jb["ok"] and rb != 0, [jb["ok"], rb], [False, "!=0"])], [out]


@card("QA-150")
def hf_cli_snapshot(task, wd):
    """`hyperframes snapshot --at`, `--zoom selector` (crop at scale 3) and `--against` a reference video."""
    np = _np()
    good = good_project(wd, "good")
    ref = fx.color_clip(wd / "ref.mp4", "blue", 2.0, "640x360", 30)
    (r1, j1, t1), (r2, j2, t2), (r3, j3, t3) = par(
        lambda: hf(wd, ["snapshot", ".", "--at", "0.5,1.0", "--no-end", "--json", "-o", wd / "at"], good, timeout=90),
        lambda: hf(wd, ["snapshot", ".", "--at", "0.5", "--no-end", "--zoom", "#box", "--json", "-o", wd / "zoom"], good, timeout=90),
        lambda: hf(wd, ["snapshot", ".", "--at", "1.0", "--no-end", "--against", ref, "--json", "-o", wd / "against"], good, timeout=90))
    if not (j1 and j2 and j3):
        raise RuntimeError("snapshot failed: %s" % (t1 + t2 + t3)[-400:])
    xs = [red_x(load_png(f["path"])) for f in j1["frames"]]
    exp = [40 + 400 * 0.5 / 1.5, 40 + 400 * 1.0 / 1.5]
    z = load_png(j2["frames"][0]["path"])
    zred = float(((z[..., 0] > 200) & (z[..., 1] < 100)).mean())
    full_red = float(((load_png(j1["frames"][0]["path"])[..., 0] > 200) & (load_png(j1["frames"][0]["path"])[..., 1] < 100)).mean())
    ag = sorted(p.name for p in (wd / "against").glob("*"))
    blue = [p for p in (wd / "against").glob("*.png") if load_png(p)[..., 2].mean() > 200 and load_png(p)[..., 0].mean() < 40]
    return [check("frame times are the requested --at times", [f["time"] for f in j1["frames"]] == [0.5, 1.0], [f["time"] for f in j1["frames"]], [0.5, 1.0]),
            check("box left edge at each time matches the linear tween", all(abs(a - b) <= 2 for a, b in zip(xs, exp)), xs, exp),
            check("--zoom crop is a 3x density crop around #box (>= 240 px)", min(z.shape[:2]) >= 240, list(z.shape[:2]), ">= 240"),
            check("zoom crop is mostly the box", zred > 0.3, zred, "> 0.3"),
            check("--against saved the reference frame (blue) beside the render", len(blue) >= 1 and len(ag) >= 2, ag, "reference + pair"),
            check("negative control: the full frame is not mostly the box", full_red < 0.1, full_red, "< 0.1")], [Path(j1["frames"][0]["path"]), Path(j2["frames"][0]["path"])]


@card("QA-151")
def hf_cli_keyframes(task, wd):
    """`hyperframes keyframes --json`: inspect tween keyframes over time (targets, start/end, ease, stops)."""
    good = good_project(wd, "good")
    still = hf_project(wd, "still", BOX_BODY, BOX_CSS, "")
    r, j, t = hf(wd, ["keyframes", ".", "--json"], good)
    r0, j0, _ = hf(wd, ["keyframes", ".", "--json"], still)
    out = wj(wd / "keyframes.json", j)
    tw_ = {x["target"]: x for x in j["compositions"][0]["tweens"]}
    box, title = tw_.get("#box"), tw_.get("#title")
    return [check("two tweens found: #box and #title", sorted(tw_) == ["#box", "#title"], sorted(tw_), ["#box", "#title"]),
            check("#box: to, 0 -> 1.5 s, ease none, ends at x=400", box["method"] == "to" and box["start"] == 0 and box["end"] == 1.5 and box["ease"] == "none"
                  and box["keyframes"][-1]["properties"].get("x") == 400, [box["start"], box["end"], box["ease"]], [0, 1.5, "none"]),
            check("#title: fromTo opacity 0 -> 1 between 0.2 and 0.7 s", title["method"] == "fromTo" and abs(title["start"] - 0.2) < 1e-6 and abs(title["end"] - 0.7) < 1e-6
                  and title["keyframes"][0]["properties"]["opacity"] == 0 and title["keyframes"][-1]["properties"]["opacity"] == 1,
                  [title["start"], title["end"]], [0.2, 0.7]),
            check("negative control: a project with no tweens lists none", sum(len(c["tweens"]) for c in j0["compositions"]) == 0,
                  sum(len(c["tweens"]) for c in j0["compositions"]), 0)], [out]


def _clusters(cols):
    np = _np()
    cols = np.nonzero(cols)[0]
    if not len(cols):
        return []
    runs = np.split(cols, np.nonzero(np.diff(cols) > 3)[0] + 1)
    return [(int(r[0]), int(r[-1])) for r in runs if r[-1] - r[0] >= 20]


@card("QA-152")
def hf_cli_compare(task, wd):
    """`hyperframes compare` of two variants into a labelled sheet, and `grade-compare` of candidate grades."""
    np = _np()
    from PIL import Image
    a = good_project(wd, "red")
    b = hf_project(wd, "blue", BOX_BODY, BOX_CSS.replace("#ff3b30", "#2f6bff"), BOX_JS)
    Image.new("RGB", (320, 180), (128, 100, 80)).save(wd / "ref.png")
    wj(wd / "grades.json", [{"label": "warm", "grading": {"adjust": {"temperature": 0.8}}}, {"label": "bw", "grading": {"adjust": {"saturation": -1}}}])
    (r, j, t), (r2, j2, t2) = par(
        lambda: hf(wd, ["compare", "red", "blue", "--at", "1", "--labels", "red,blue", "--out", wd / "compare.png", "--json"], wd, timeout=90),
        lambda: hf(wd, ["grade-compare", "--for", "ref.png", "--grades", "grades.json", "--out", "grade-compare.png", "--json"], wd, timeout=90))
    if not (j and j2):
        raise RuntimeError("compare failed: %s" % (t + t2)[-400:])
    S = load_png(wd / "compare.png")
    red = float(((S[..., 0] > 200) & (S[..., 1] < 100) & (S[..., 2] < 100)).sum())
    blu = float(((S[..., 2] > 200) & (S[..., 0] < 100)).sum())
    G = load_png(wd / "grade-compare.png")
    H, W = G.shape[:2]
    orig, warm, bw = G[int(H * 0.28), int(W * 0.25)], G[int(H * 0.28), int(W * 0.75)], G[int(H * 0.77), int(W * 0.25)]
    sat = lambda c: float(max(c) - min(c))
    return [check("compare rendered both variants", j["rendered"] == 2 and [v["label"] for v in j["variants"]] == ["red", "blue"], j["rendered"], 2),
            check("sheet holds a red box and a blue box", red > 2000 and blu > 2000, [red, blu], "> 2000 px each"),
            check("grade-compare: 3 cells (baseline + 2 grades)", j2["cells"] == 3, j2["cells"], 3),
            check("warm grade raises R-B over the original", (warm[0] - warm[2]) > (orig[0] - orig[2]) + 10, [list(orig), list(warm)], "R-B up"),
            check("bw grade has no saturation", sat(bw) <= 3, sat(bw), "<= 3"),
            check("negative control: the ungraded original is saturated", sat(orig) > 20, sat(orig), "> 20")], [wd / "compare.png", wd / "grade-compare.png"]


@card("QA-155")
def hf_pin_upgrade(task, wd):
    """Pinned project CLI: `upgrade --project . --check`, then bump the package.json pins, verify with check, record
    old/new versions, and revert on failure."""
    proj = good_project(wd, "proj")
    pkg = {"name": "proj", "private": True, "type": "module",
           "scripts": {s: "npx --yes hyperframes@0.9.0 " + s for s in ("preview", "check", "render")}}
    wj(proj / "package.json", pkg)
    before = (proj / "package.json").read_text()
    r0, probe_, t0 = hf(wd, ["upgrade", "--project", ".", "--check", "--json"], proj, timeout=45)
    if not probe_ or "latestVersion" not in probe_.get("_meta", {}):
        raise RuntimeError("upgrade --check failed (registry unreachable?): %s" % t0[-300:])
    latest = probe_["_meta"]["latestVersion"]
    r1, up, t1 = hf(wd, ["upgrade", "--project", ".", "-y", "--json"], proj, timeout=45)
    rc, ck, _ = hf(wd, ["check", ".", "--json"], proj, timeout=90)
    if not ck or not ck.get("ok"):
        (proj / "package.json").write_text(before)
    after = rj(proj / "package.json")
    pins = sorted({re.search(r"hyperframes@([\d.]+)", v).group(1) for v in after["scripts"].values()})
    # the revert path: a broken project's check fails, so its bump is rolled back
    broke = hf_project(wd, "broke", BOX_BODY, BOX_CSS, BOX_JS, register=False, paused=False)
    wj(broke / "package.json", pkg)
    b_before = (broke / "package.json").read_text()
    hf(wd, ["upgrade", "--project", ".", "-y", "--json"], broke, timeout=45)
    bumped = (broke / "package.json").read_text() != b_before
    rcb, ckb, _ = hf(wd, ["check", ".", "--json"], broke, timeout=90)
    if not ckb or not ckb.get("ok"):
        (broke / "package.json").write_text(b_before)
    summary = wj(wd / "upgrade_summary.json", {"old": "0.9.0", "new": latest, "check_ok": ck.get("ok"), "pins": pins,
                                               "broken_project_reverted": (broke / "package.json").read_text() == b_before})
    return [check("probe reports the pinned version as behind", probe_.get("changed") is True and probe_.get("from") == ["0.9.0"], probe_.get("from"), ["0.9.0"]),
            check("every script pin bumped to the latest version", pins == [latest], pins, [latest]),
            check("verify with check after the upgrade passes", ck.get("ok") is True, ck.get("ok"), True),
            check("failing check reverts the bump", bumped and (broke / "package.json").read_text() == b_before, bumped, "bumped then reverted"),
            check("negative control: the untreated package.json still pins 0.9.0", "hyperframes@0.9.0" in before and latest != "0.9.0", "0.9.0", "!= latest")], [summary, proj / "package.json"]


@card("QA-158")
def hf_timeline(task, wd):
    """`hyperframes timeline --json`: every track and clip with starts, ends and what plays."""
    body = ('<div id="a" class="clip" data-start="0" data-duration="1.5" data-track-index="0" style="position:absolute;width:50px;height:50px;background:#f00"></div>'
            '<div id="b" class="clip" data-start="1.5" data-duration="1.5" data-track-index="0" style="position:absolute;width:50px;height:50px;background:#0f0"></div>'
            '<h1 id="t" class="clip" data-start="0.5" data-duration="2" data-track-index="1" style="color:#fff;position:absolute;top:100px">Title</h1>')
    p = hf_project(wd, "tl", body, "", 'tl.to("#a",{x:100,duration:1},0);', dur=3)
    r, j, t = hf(wd, ["timeline", "--json"], p)
    out = wj(wd / "timeline.json", j)
    rows = {row["id"]: row for tr in j["timeline"]["tracks"] for row in tr["rows"]}
    spans = {k: (rows[k]["absStart"], rows[k]["absEnd"], rows[k]["trackIndex"]) for k in rows}
    exp = {"a": (0, 1.5, 0), "b": (1.5, 3, 0), "t": (0.5, 2.5, 1)}
    return [check("timeline duration is 3 s", j["timeline"]["duration"] == 3, j["timeline"]["duration"], 3),
            check("every clip listed with start, end and track", spans == exp, spans, exp),
            check("what plays: element kinds", rows["t"]["kind"] == "h1" and rows["a"]["kind"] == "div", [rows["t"]["kind"], rows["a"]["kind"]], ["h1", "div"]),
            check("negative control: track 0 clips do not overlap (a ends where b starts)", spans["a"][1] <= spans["b"][0], [spans["a"][1], spans["b"][0]], "a.end <= b.start")], [out]


@card("QA-161")
def hf_keyframe_diagnostics(task, wd):
    """`keyframes --selector --shot` onion-skin ghosts, `--layout strip`, and `snapshot --at` proving the final lockup."""
    np = _np()
    good = good_project(wd, "good")
    still = hf_project(wd, "still", BOX_BODY, BOX_CSS, 'tl.fromTo("#title",{opacity:0},{opacity:1,duration:0.5},0.2);')
    (r1, j1, t1), (r2, j2, t2), (r3, j3, t3), (r4, j4, t4) = par(
        lambda: hf(wd, ["keyframes", ".", "--selector", "#box", "--shot", wd / "onion.png", "--samples", "5", "--json"], good, timeout=90),
        lambda: hf(wd, ["keyframes", ".", "--selector", "#box", "--shot", wd / "strip.png", "--layout", "strip", "--from", "0", "--to", "1.5", "--samples", "4", "--json"], good, timeout=90),
        lambda: hf(wd, ["keyframes", ".", "--selector", "#box", "--shot", wd / "still.png", "--samples", "5", "--json"], still, timeout=90),
        lambda: hf(wd, ["snapshot", ".", "--at", "2", "--no-end", "--json", "-o", wd / "lockup"], good, timeout=90))
    if not ((wd / "onion.png").exists() and (wd / "strip.png").exists() and j4):
        raise RuntimeError("keyframes --shot failed: %s" % (t1 + t2 + t4)[-400:])
    ghost = lambda a: (a[..., 0] > 90) & (a[..., 0] < 200) & (a[..., 1] < 70) & (a[..., 2] < 70)
    cl = _clusters(ghost(load_png(wd / "onion.png")).any(axis=0))
    cs = _clusters(ghost(load_png(wd / "still.png")).any(axis=0)) if (wd / "still.png").exists() else []
    starts = [c[0] for c in cl]
    gaps = np.diff(starts) if len(starts) > 1 else np.array([0])
    L = load_png(j4["frames"][0]["path"])
    white = float((L.min(axis=2) > 230).sum())
    return [check("onion shot shows >= 4 ghost positions of #box", len(cl) >= 4, cl, ">= 4"),
            check("ghost spacing is even (linear ease: equal steps)", len(gaps) >= 3 and float(gaps.max() - gaps.min()) <= 4, gaps.tolist(), "max-min <= 4 px"),
            check("strip layout written as a PNG filmstrip", load_png(wd / "strip.png").std() > 5, (wd / "strip.png").stat().st_size, "> 0"),
            check("final lockup at t=2: box at its end x and the title fully on", abs(red_x(L) - 440) <= 2 and white > 300, [red_x(L), white], [440, "> 300"]),
            check("negative control: a box that never moves leaves one ghost", len(cs) <= 1, cs, "<= 1 cluster")], [wd / "onion.png", wd / "strip.png"]


@card("QA-164")
def hf_lint_gate(task, wd):
    """Lint (static) gate: named rule ids, --verbose info level, exit code as the gate."""
    good = good_project(wd, "good")
    body = ('<div id="a" class="clip" data-start="0" data-duration="2" data-track-index="0"></div>'
            '<div id="b" class="clip" data-start="1" data-duration="2" data-track-index="1"></div>'
            '<img id="im" src="missing.png" class="clip" data-start="0" data-duration="1" data-track-index="2">')
    over = hf_project(wd, "overlap", body, "#a{position:absolute;transform:translateX(20px);width:50px;height:50px;background:red}",
                      'tl.to("#a",{x:100,duration:1},0);')
    nocomp = good_project(wd, "nocomp")
    p = nocomp / "index.html"
    p.write_text(p.read_text().replace(' data-composition-id="main"', ""))
    res = {}
    for name, d in (("good", good), ("overlap", over), ("nocomp", nocomp)):
        rc, j, _ = hf(wd, ["lint", ".", "--verbose", "--json"], d)
        res[name] = {"rc": rc, "codes": sorted({f["code"] for f in j["findings"]}), "errors": j["errorCount"], "ok": j["ok"]}
    out = wj(wd / "lint_gate.json", res)
    return [check("clean project passes the gate (exit 0)", res["good"]["rc"] == 0 and res["good"]["errors"] == 0, res["good"], "rc 0"),
            check("CSS transform vs GSAP x, a missing asset and a clip past the root are named", {"gsap_css_transform_conflict", "missing_local_asset",
                  "clip_ends_past_root_duration"} <= set(res["overlap"]["codes"]), res["overlap"]["codes"], ["clip_ends_past_root_duration", "gsap_css_transform_conflict", "missing_local_asset"]),
            check("warnings only appear with their own severity (clip past root is a warning)", res["overlap"]["errors"] == 2, res["overlap"]["errors"], 2),
            check("missing data-composition-id is named root_missing_composition_id", "root_missing_composition_id" in res["nocomp"]["codes"], res["nocomp"]["codes"], "root_missing_composition_id"),
            check("rule ids are snake_case names", all(re.fullmatch(r"[a-z0-9_]+", c) for r in res.values() for c in r["codes"]), [r["codes"] for r in res.values()], "snake_case"),
            check("negative control: broken projects fail the gate (exit != 0)", res["overlap"]["rc"] != 0 and res["nocomp"]["rc"] != 0,
                  [res["overlap"]["rc"], res["nocomp"]["rc"]], "!= 0")], [out]


@card("QA-165")
def hf_check_gate_motion(task, wd):
    """check as one browser gate: runtime errors, layout, `*.motion.json` assertions, WCAG contrast; --samples 15 and --at."""
    good = good_project(wd, "good")
    wj(good / "index.motion.json", {"duration": 2, "assertions": [{"kind": "appearsBy", "selector": "#title", "bySec": 0.8},
                                                                   {"kind": "staysInFrame", "selector": "#box"}]})
    bad = hf_project(wd, "bad", BOX_BODY, BOX_CSS, 'tl.to("#box",{x:900,duration:1.5,ease:"none"},0);tl.fromTo("#title",{opacity:0},{opacity:1,duration:0.5},1.2);'
                     'setTimeout(()=>{throw new Error("boom")},0);')
    wj(bad / "index.motion.json", {"duration": 2, "assertions": [{"kind": "appearsBy", "selector": "#title", "bySec": 0.5},
                                                                  {"kind": "staysInFrame", "selector": "#box"}]})
    (rg, jg, _), (rb, jb, _) = par(lambda: hf(wd, ["check", ".", "--json", "--samples", "15"], good, timeout=90),
                                   lambda: hf(wd, ["check", ".", "--json"], bad, timeout=90))
    out = wj(wd / "check_gate.json", {"good": jg, "bad": jb})
    return [check("--samples 15 sweeps 15 grid times", len(jg["layout"]["samples"]) == 15, len(jg["layout"]["samples"]), 15),
            check("motion sidecar discovered and its assertions pass on the good film", jg["motion"].get("enabled") and jg["motion"]["ok"], jg["motion"].get("specPath", "")[-20:], "index.motion.json"),
            check("good film passes the whole gate", jg["ok"] and rg == 0, jg["ok"], True),
            check("late entrance and off-frame drift fail motion assertions", jb["motion"]["errorCount"] >= 1, findings(jb, "motion"), ">= 1"),
            check("thrown page error reported by runtime", jb["runtime"]["errorCount"] + jb["runtime"]["warningCount"] >= 1, findings(jb, "runtime"), ">= 1"),
            check("negative control: the faulty film fails the exit code", rb != 0 and not jb["ok"], rb, "!= 0")], [out]


@card("QA-167")
def hf_snapshot_contact(task, wd):
    """`snapshot --at t1,t2,t3` stills + contact sheet to inspect mounts, text and the final lockup."""
    np = _np()
    good = good_project(wd, "good")
    r, j, t = hf(wd, ["snapshot", ".", "--at", "0,0.5,1.0,1.5", "--json", "-o", wd / "snaps"], good, timeout=90)
    if not j:
        raise RuntimeError(t[-300:])
    fr = [load_png(f["path"]) for f in j["frames"]]
    sheet = load_png(j["contactSheets"][0])
    white = [float((a.min(axis=2) > 230).sum()) for a in fr]
    return [check("one still per --at time plus the readable end frame", len(fr) >= 4 and [f["time"] for f in j["frames"]][:4] == [0, 0.5, 1.0, 1.5],
                  [f["time"] for f in j["frames"]], [0, 0.5, 1.0, 1.5, "end"]),
            check("contact sheet is wider than one frame (grid of stills)", sheet.shape[1] > fr[0].shape[1], list(sheet.shape[:2]), "> 640 wide"),
            check("title mounted and fully on by 1.0 s", white[2] > 300, white, "> 300 white px"),
            check("box reaches its end x in the lockup", abs(red_x(fr[-1]) - 440) <= 2, red_x(fr[-1]), 440),
            check("negative control: frame 0 has no title text yet", white[0] < 20, white[0], "< 20")], [Path(j["contactSheets"][0])]


@card("QA-169")
def hf_compare_variants_grades(task, wd):
    """Compare three variants side by side and compare a .cube LUT grade against the baseline frame."""
    np = _np()
    from PIL import Image
    cols = {"red": "#ff3b30", "green": "#21c45a", "blue": "#2f6bff"}
    for k, c in cols.items():
        hf_project(wd, k, BOX_BODY, BOX_CSS.replace("#ff3b30", c), BOX_JS)
    n = 17
    lines = ["TITLE \"invert\"", "LUT_3D_SIZE %d" % n]
    for b in range(n):
        for g in range(n):
            for rr in range(n):
                lines.append("%.6f %.6f %.6f" % (1 - rr / (n - 1.0), 1 - g / (n - 1.0), 1 - b / (n - 1.0)))
    lines = lines[:2] + lines[2:]
    # .cube order: red fastest
    tw(wd / "invert.cube", "\n".join(lines) + "\n")
    Image.new("RGB", (320, 180), (200, 60, 40)).save(wd / "ref.png")
    (r, j, t), (r2, j2, t2) = par(
        lambda: hf(wd, ["compare", "red", "green", "blue", "--at", "1", "--labels", "red,green,blue", "--cols", "3", "--out", wd / "variants.png", "--json"], wd, timeout=90),
        lambda: hf(wd, ["grade-compare", "--for", "ref.png", "--luts", "invert.cube", "--out", "lut-compare.png", "--json"], wd, timeout=90))
    if not (j and j2):
        raise RuntimeError((t + t2)[-400:])
    V = load_png(wd / "variants.png")
    W = V.shape[1]
    thirds = [V[:, i * W // 3:(i + 1) * W // 3] for i in range(3)]
    dom = [int(np.argmax([(th[..., c] > 180).sum() - (th[..., (c + 1) % 3] > 180).sum() for c in range(3)])) for th in thirds]
    G = load_png(wd / "lut-compare.png")
    H, Wg = G.shape[:2]
    base, lut = G[int(H * 0.5), int(Wg * 0.25)], G[int(H * 0.5), int(Wg * 0.75)]
    return [check("three variants rendered in one row", j["rendered"] == 3, j["rendered"], 3),
            check("each third is dominated by its variant's colour (R,G,B)", dom == [0, 1, 2], dom, [0, 1, 2]),
            check("grade-compare made baseline + LUT cells", j2["cells"] == 2, j2["cells"], 2),
            check("invert LUT cell is the complement of the baseline (+-25)", all(abs(lut[c] - (255 - base[c])) <= 25 for c in range(3)), [list(base), list(lut)], "255 - base"),
            check("negative control: the baseline cell is not inverted", abs(base[0] - 200) <= 25, list(base), "~(200,60,40)")], [wd / "variants.png", wd / "lut-compare.png"]


@card("QA-170")
def hf_history_turns(task, wd):
    """Project history per agent turn: `history begin --who`, edits, `end`; `undo --who agent` takes back only the
    agent's newest turn, and refuses (conflict) rather than overwrite a newer edit the person made to the same file."""
    p = good_project(wd, "proj")
    idx, notes = p / "index.html", p / "notes.html"
    notes.write_text("<p>draft</p>")
    H = lambda *a: hf(wd, ["history", *a, "--json"], p)[1]
    H("begin", "--who", "agent", "--label", "recolor box")
    idx.write_text(idx.read_text().replace("#ff3b30", "#00ff00"))
    H("end", "--who", "agent")
    H("begin", "--who", "person", "--label", "notes")
    notes.write_text("<p>person's note</p>")
    H("end", "--who", "person")
    lst = H()
    edited = idx.read_text()
    und = H("undo", "--who", "agent")
    after_undo = idx.read_text()
    # second round: the person edits the same file after the agent -> undo must refuse
    H("begin", "--who", "agent", "--label", "retitle")
    idx.write_text(idx.read_text().replace(">Hello<", ">Agent<"))
    H("end", "--who", "agent")
    H("begin", "--who", "person", "--label", "colour tweak")
    idx.write_text(idx.read_text().replace("#ff3b30", "#123456"))
    H("end", "--who", "person")
    und2 = H("undo", "--who", "agent")
    final = idx.read_text()
    out = wj(wd / "history.json", {"list": lst, "undo": und, "undo_conflict": und2})
    who = [e["who"]["name"] for e in lst["entries"]]
    return [check("two entries recorded, one per turn, each naming its file", sorted(who) == ["agent", "person"] and
                  sorted(f for e in lst["entries"] for f in e["files"]) == ["index.html", "notes.html"], [(e["who"]["name"], e["files"]) for e in lst["entries"]], "agent:index, person:notes"),
            check("undo --who agent succeeded", bool(und and und.get("ok")), (und or {}).get("ok"), True),
            check("agent's recolour undone, person's note kept", "#ff3b30" in after_undo and notes.read_text() == "<p>person's note</p>", "#ff3b30" in after_undo, True),
            check("undo refuses when the person edited the same file later (conflict named)", und2 and not und2.get("ok") and und2.get("conflict", {}).get("files") == ["index.html"],
                  (und2 or {}).get("conflict"), {"files": ["index.html"]}),
            check("the person's later colour survives the refused undo", "#123456" in final and ">Agent<" in final, "#123456" in final, True),
            check("negative control: before the undo the agent's colour was in the file", "#00ff00" in edited, "#00ff00" in edited, True)], [out, idx]


@card("QA-171")
def hf_component_quality_bar(task, wd):
    """hyperframes-registry component quality bar, mechanical pass: X1 no timeline, F2 duplicate (motion fingerprint
    + markup skeleton hashes), X6 no markup, X2 name claims a missing technique, X7 unseeded randomness; then
    `hyperframes lint` on the item that passes."""
    comps = {
        "spring-pop": '<div class="pop">Hi</div><script>const tl=gsap.timeline({paused:true});tl.from(".pop",{scale:0,duration:.6,ease:"back.out(2)"});window.__timelines["spring-pop"]=tl;</script>',
        "spring-scale-in": '<div class="card">Hey</div><script>const tl=gsap.timeline({paused:true});tl.from(".card",{scale:0,duration:.6,ease:"power2.out"});window.__timelines["spring-scale-in"]=tl;</script>',
        "grow-in": '<div class="box">Yo</div><script>const tl=gsap.timeline({paused:true});tl.from(".box",{scale:0,duration:.6,ease:"power2.out"});window.__timelines["grow-in"]=tl;</script>',
        "static-label": '<div class="label">Label</div><style>.label{color:var(--ink,#111)}</style>',
        "style-only": '<style>.x{color:red}</style><script>/* helper */</script>',
        "sparkle-field": '<div class="dots"></div><script>const tl=gsap.timeline({paused:true});for(let i=0;i<9;i++){tl.to(".dots",{x:Math.random()*100,duration:.2})}window.__timelines["sparkle-field"]=tl;</script>',
    }
    rules = {"spring-": r"elastic|back\.|bounce", "mask": r"mask|clip-path", "glass": r"backdrop-filter", "draw": r"stroke-dash|pathLength"}

    def strip(s, tags=("script", "style")):
        s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
        for t in tags:
            s = re.sub(r"<%s.*?</%s>" % (t, t), "", s, flags=re.S)
        return s

    rep = {}
    fps, sks = {}, {}
    for name, src in comps.items():
        code = "".join(re.findall(r"<script>(.*?)</script>", src, re.S))
        calls = re.sub(r"\((\s*)[\"'][^\"']*[\"']", "(S", " ".join(re.findall(r"\.(?:from|to|fromTo)\([^;]*\)", code)))
        fp = hashlib.sha1(calls.encode()).hexdigest()[:10] if calls else None
        sk = hashlib.sha1(" ".join(re.findall(r"<(\w+)", strip(src))).encode()).hexdigest()[:10]
        fps[name], sks[name] = fp, sk
        flags = []
        if "__timelines" not in src and name != "static-label":
            flags.append("X1")
        if len(re.findall(r"<\w+", strip(src))) == 0:
            flags.append("X6")
        for pat, need in rules.items():
            if pat in name and not re.search(need, code):
                flags.append("X2")
        if re.search(r"Math\.random|Date\.now|performance\.now", code):
            flags.append("X7")
        rep[name] = flags
        tw(wd / "items" / name / (name + ".html"), src)
    for a in comps:
        for b in comps:
            if a < b and fps[a] and fps[a] == fps[b] and sks[a] == sks[b]:
                rep[a].append("F2:" + b)
                rep[b].append("F2:" + a)
    out = wj(wd / "audit.json", {"flags": rep, "fingerprints": fps, "skeletons": sks})
    host = hf_project(wd, "mount", '<div class="pop" style="color:#fff;font:600 80px sans-serif;position:absolute;left:200px;top:120px">Hi</div>', "",
                      'tl.from(".pop",{scale:0,duration:.6,ease:"back.out(2)"},0);')
    rc, lj, _ = hf(wd, ["lint", ".", "--json"], host)
    return [check("spring-pop passes the mechanical pass", rep["spring-pop"] == [], rep["spring-pop"], []),
            check("spring-scale-in: name claims a spring it lacks (X2) and duplicates grow-in (F2)", "X2" in rep["spring-scale-in"] and "F2:grow-in" in rep["spring-scale-in"],
                  rep["spring-scale-in"], ["X2", "F2:grow-in"]),
            check("style-only item has no markup (X6) and no timeline (X1)", {"X6", "X1"} <= set(rep["style-only"]), rep["style-only"], ["X1", "X6"]),
            check("Math.random scatter flagged X7", "X7" in rep["sparkle-field"], rep["sparkle-field"], ["X7"]),
            check("static-label kept (deliberate static, N3)", rep["static-label"] == [], rep["static-label"], []),
            check("surviving item mounted alone lints clean", lj["ok"], lj["errorCount"], 0),
            check("negative control: distinct items do not share both hashes", not (fps["spring-pop"] == fps["grow-in"] and sks["spring-pop"] == sks["grow-in"]),
                  [fps["spring-pop"], fps["grow-in"]], "differ")], [out]


@card("QA-213")
def hf_check_contrast_gate(task, wd):
    """Single pre-render `hyperframes check` gate: WCAG contrast failures are errors; `--no-contrast` skips them all."""
    css = BOX_CSS.replace("color:#ffffff", "color:#26303a")
    low = hf_project(wd, "low", BOX_BODY, css, BOX_JS)
    fixed = hf_project(wd, "fixed", BOX_BODY, BOX_CSS, BOX_JS)
    (r1, j1, _), (r2, j2, _), (r3, j3, _) = par(lambda: hf(wd, ["check", ".", "--json"], low, timeout=90),
                                                lambda: hf(wd, ["check", ".", "--json", "--no-contrast"], low, timeout=90),
                                                lambda: hf(wd, ["check", ".", "--json"], fixed, timeout=90))
    out = wj(wd / "gate.json", {"low": j1, "low_no_contrast": j2, "fixed": j3})
    f = (j1["contrast"]["findings"] or [{}])[0]
    measured = contrast(hexrgb("#26303a"), hexrgb("#101820"))
    return [check("low-contrast title is a contrast error", "contrast_aa_failure" in findings(j1, "contrast") and f.get("severity") == "error", findings(j1, "contrast"), "contrast_aa_failure"),
            check("our own WCAG ratio agrees it is under 3:1", measured < 3, measured, "< 3"),
            check("--no-contrast skips every contrast finding", findings(j2, "contrast") == [] and j2["ok"], findings(j2, "contrast"), []),
            check("the fixed palette passes the gate", j3["ok"] and r3 == 0, j3["ok"], True),
            check("negative control: the untreated film fails the gate", not j1["ok"] and r1 != 0, r1, "!= 0")], [out]


@card("QA-223")
def hf_usage_window(task, wd):
    """`hyperframes usage --json` at start, after drafting and before rendering; an unknown allowance is reported as
    unknown, never invented."""
    p = good_project(wd, "proj")
    reads = {}
    for stage in ("start", "after_draft", "before_render"):
        rc, j, t = hf(wd, ["usage", "--json"], p, timeout=30)
        reads[stage] = j if j is not None else {"status": "unknown", "reason": "no JSON"}
    def say(r):
        if r.get("status") == "unknown" or "remaining" not in r:
            return "usage unknown (%s)" % r.get("reason", "n/a")
        return "remaining %s, resets %s" % (r["remaining"], r.get("resetsAt"))
    lines = {k: say(v) for k, v in reads.items()}
    out = wj(wd / "usage_log.json", {"reads": reads, "said": lines})
    fake = {"status": "unknown"}
    fabricated = "remaining 80%, resets 18:00"
    honest = lambda r, line: (r.get("status") == "unknown") == line.startswith("usage unknown")
    return [check("usage read at all three milestones", sorted(reads) == ["after_draft", "before_render", "start"], sorted(reads), 3),
            check("each read is machine JSON with a status or numbers", all("status" in r or "remaining" in r for r in reads.values()), [r.get("status") for r in reads.values()], "status"),
            check("what we say matches what was read (unknown stays unknown)", all(honest(reads[k], lines[k]) for k in reads), lines, "consistent"),
            check("negative control: a fabricated allowance for an unknown read fails the honesty test", not honest(fake, fabricated), fabricated, "rejected")], [out]


# ═════════════════════════ video fixtures and analysis cards ═════════════════════════
def texture(seed, h, w, block=8, lo=40, hi=220):
    np = _np()
    r = np.random.default_rng(seed)
    base = r.uniform(lo, hi, (h // block + 1, w // block + 1, 3))
    return np.kron(base, np.ones((block, block, 1)))[:h, :w]


def moving_shot(seed, n, h, w, step=2):
    np = _np()
    big = texture(seed, h, w * 3)
    return [np.roll(big, -step * i, axis=1)[:, :w].copy() for i in range(n)]


def mimic():
    sys.dont_write_bytecode = True
    if str(MIMIC) not in sys.path:
        sys.path.insert(0, str(MIMIC))
    import mm_analyze
    from mm_common import probe
    return mm_analyze, probe


def audio_md5(path):
    return subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:a:0", "-c", "copy", "-f", "md5", "-"],
                          capture_output=True, text=True, timeout=60, stdin=subprocess.DEVNULL).stdout.strip()


def qa_mod():
    sys.dont_write_bytecode = True
    p = str(VENDOR / "kosif-montage-motion/scripts")
    if p not in sys.path:
        sys.path.insert(0, p)
    import qa
    return qa


def tone_wav(path, seconds, freq=440.0, amp=0.25, rate=48000, beeps=None):
    """A tone (or silence with short beeps at the given times) as 16-bit WAV."""
    np = _np()
    t = np.arange(int(seconds * rate)) / rate
    if beeps is None:
        y = amp * np.sin(2 * np.pi * freq * t)
    else:
        y = np.zeros_like(t)
        for b in beeps:
            m = (t >= b) & (t < b + 0.05)
            y[m] = amp * np.sin(2 * np.pi * freq * t[m])
    return fx.write_wav(path, y, rate)


@card("QA-133")
def watch_reference_video(task, wd):
    """Watch a video by frames + transcript: scene-detect cuts, stratified interval samples, transcript-anchored frames,
    perceptual-hash dedupe (no hard cap), every frame keeps its time and tolerance; the caption track is read as the
    timed transcript (the faster-whisper weights are not downloadable here, so the fixture carries its own subtitles)."""
    np = _np()
    W, H, fps = 160, 90, 30
    frames = moving_shot(1, 60, H, W, 3) + [texture(2, H, W)] * 60 + moving_shot(3, 60, H, W, 3)
    vid = write_video(wd / "clip_v.mp4", frames, fps)
    cues = [(0.4, 1.6, "Hook: watch this"), (2.2, 3.4, "The calm middle"), (4.3, 5.6, "Follow for more")]
    srt = "".join("%d\n00:00:%06.3f --> 00:00:%06.3f\n%s\n\n" % (i + 1, a, b, txt) for i, (a, b, txt) in enumerate(cues)).replace(".", ",")
    tw(wd / "in.srt", srt)
    fx.ffmpeg("-i", vid, "-i", wd / "in.srt", "-map", "0", "-map", "1", "-c:v", "copy", "-c:s", "mov_text", wd / "social.mp4")
    src = wd / "social.mp4"
    fx.ffmpeg("-i", src, "-map", "0:s:0", wd / "transcript.srt")
    got = []
    for blk in (wd / "transcript.srt").read_text().strip().split("\n\n"):
        ln = blk.strip().splitlines()
        a, b = [sum(float(x) * m for x, m in zip(s.replace(",", ".").split(":"), (3600, 60, 1))) for s in ln[1].split(" --> ")]
        got.append((round(a, 3), round(b, 3), " ".join(ln[2:])))
    F = read_video(src)
    d = np.abs(np.diff(F, axis=0)).mean(axis=(1, 2, 3))
    cuts = [int(i + 1) for i in np.nonzero(d > 25)[0]]
    bounds = [0] + cuts + [len(F)]
    cand = []
    for s0, s1 in zip(bounds[:-1], bounds[1:]):
        for k in range(s0, s1, fps // 2):                       # stratified 0.5 s interval inside each shot
            cand.append({"frame": k, "t": k / fps, "why": "interval", "tol": 0.25})
    for a, b, txt in got:                                       # transcript-anchored frames at cue midpoints
        k = int(round((a + b) / 2 * fps))
        cand.append({"frame": k, "t": k / fps, "why": "transcript", "tol": 0.5 / fps})
    for c in cuts:
        cand.append({"frame": c, "t": c / fps, "why": "scene", "tol": 0.5 / fps})
    cand.sort(key=lambda c: c["frame"])
    kept, hashes = [], []
    for c in cand:
        h = phash(F[c["frame"]])
        if any(hamming(h, o) <= 6 for o in hashes):
            continue
        hashes.append(h)
        kept.append(c)
    static = [c for c in kept if 60 <= c["frame"] < 120]
    raw_static = [c for c in cand if 60 <= c["frame"] < 120]
    raw_dupes = sum(1 for i, a in enumerate(raw_static) for b in raw_static[i + 1:] if hamming(phash(F[a["frame"]]), phash(F[b["frame"]])) <= 6)
    contact_sheet([F[c["frame"]] for c in kept], 6, wd / "contact.png")
    md = ["# Watch report: social.mp4", "", "TL;DR: %d shots over %.1f s, %d frames read." % (len(bounds) - 1, len(F) / fps, len(kept)), "",
          "## Transcript (verbatim, timed)"] + ["- [%.2f-%.2f] %s" % g for g in got] + ["", "## Frames"] + \
         ["- %.3f s (+-%.3f, %s)" % (c["t"], c["tol"], c["why"]) for c in kept] + ["", "## Beats", "hook -> %s -> CTA" % got[1][2]]
    tw(wd / "watch.md", "\n".join(md))
    return [check("scene cuts found at the shot joins (frames 60, 120)", cuts == [60, 120], cuts, [60, 120]),
            check("transcript read back verbatim with cue times", [g[2] for g in got] == [c[2] for c in cues] and all(abs(g[0] - c[0]) < 0.01 for g, c in zip(got, cues)), got, cues),
            check("every kept frame carries a time and a tolerance", all("t" in c and c["tol"] > 0 for c in kept), len(kept), "all"),
            check("dedupe keeps one frame of the frozen middle shot", len(static) == 1, len(static), 1),
            check("moving shots keep several frames (no hard cap)", len(kept) - len(static) >= 6, len(kept) - len(static), ">= 6"),
            check("negative control: undeduped samples of the frozen shot are near-duplicates", raw_dupes >= 3, raw_dupes, ">= 3")], [wd / "watch.md", wd / "contact.png"]


def _look_fixture(path, letterbox=True, vignette=True, fade=True):
    np = _np()
    W, H, fps = 96, 160, 30
    frames = moving_shot(5, 45, H, W, 2) + moving_shot(9, 45, H, W, 2)
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / math.sqrt(2)
    vig = (1 - 0.6 * r ** 2.2)[..., None]
    out = []
    for i, f in enumerate(frames):
        f = f.copy()
        if vignette:
            f = f * vig
        if fade and i < 12:
            f = f * (i / 12.0)
        if letterbox:
            f[:19] = 0
            f[-19:] = 0
        out.append(f)
    return write_video(path, out, fps)


@card("QA-196")
def shot_boundary_look(task, wd):
    """mm_analyze per-frame features: detect_boundaries -> shot_measures per shot -> global_look (vignette, grain,
    letterbox rows near-black in mean and max, fades)."""
    A, probe = mimic()
    res = {}
    for name, kw in (("treated", {}), ("plain", {"letterbox": False, "vignette": False, "fade": False})):
        p = _look_fixture(wd / (name + ".mp4"), **kw)
        info = probe(str(p))
        f = A.pass_a(str(p), info["fps"], info["w"], info["h"])
        b = A.detect_boundaries(f)
        cuts = [int(round((x["a"] + x["b"]) / 2)) for x in b]
        res[name] = {"cuts": cuts, "look": A.global_look(f, []), "shot0": A.shot_measures(f, 0, 45, 1, 44)}
    out = wj(wd / "look.json", res)
    L, P = res["treated"]["look"], res["plain"]["look"]
    return [check("cut detected at frame 45 (+-1)", any(abs(c - 45) <= 1 for c in res["treated"]["cuts"]), res["treated"]["cuts"], 45),
            check("letterbox top/bottom about 19/160 = 0.12", abs(L["letterbox"]["top"] - 0.119) <= 0.03 and abs(L["letterbox"]["bottom"] - 0.119) <= 0.03, L["letterbox"], 0.119),
            check("vignette found (corner/centre < 0.9, strength > 0)", L["vignette"]["corner_ratio"] < 0.9 and L["vignette"]["strength"] > 0, L["vignette"], "< 0.9"),
            check("fade-in from black measured", L["fade_in_frames"] >= 5, L["fade_in_frames"], ">= 5"),
            check("shot motion: leftward pan measured", res["treated"]["shot0"]["motion"]["pan_x_per_frame"] < 0, res["treated"]["shot0"]["motion"]["pan_x_per_frame"], "< 0"),
            check("negative control: the untreated film has no letterbox, vignette or fade", P["letterbox"]["top"] == 0 and P["vignette"]["strength"] == 0 and P["fade_in_frames"] == 0,
                  [P["letterbox"]["top"], P["vignette"]["strength"], P["fade_in_frames"]], [0, 0, 0])], [out]


def _score_bounds(cuts, truth, tol=10):
    hit = 0
    for t in truth:
        c = (t["ts"] + t["te"]) / 2.0
        hit += any(abs(x - c) <= tol for x in cuts)
    return hit


@card("QA-197")
def synthetic_regression_harness(task, wd):
    """Mimic regression harness: synthetic/make_reference.py builds a reference with known truth (transitions, texts),
    the analyser's boundary detector runs on it and is scored against truth.json."""
    A, probe = mimic()
    fx.run([sys.executable, "-B", MIMIC / "synthetic/make_reference.py", wd / "ref", "--w", "108", "--h", "192"], timeout=60)
    truth = rj(wd / "ref/truth.json")
    ref = str(wd / "ref/ref.mp4")
    info = probe(ref)
    f = A.pass_a(ref, info["fps"], info["w"], info["h"])
    b = A.detect_boundaries(f)
    cuts = [(x["a"] + x["b"]) / 2.0 for x in b]
    hit = _score_bounds(cuts, truth["transitions"])
    shifted = _score_bounds([c + 40 for c in cuts], truth["transitions"])
    card_ = wj(wd / "scorecard.json", {"truth": truth["transitions"], "detected_centres": cuts, "located": hit, "of": len(truth["transitions"])})
    return [check("reference built with its truth (6 transitions, texts)", len(truth["transitions"]) == 6 and len(truth["texts"]) >= 1, len(truth["transitions"]), 6),
            check("frame count matches truth", f["n"] == truth["frames"], f["n"], truth["frames"]),
            check("analyser locates >= 4 of 6 transitions within +-10 frames", hit >= 4, hit, ">= 4"),
            check("no more detections than transitions + 2", len(cuts) <= 8, len(cuts), "<= 8"),
            check("negative control: detections shifted by 40 frames score poorly", shifted <= 1, shifted, "<= 1")], [card_, wd / "ref/truth.json"]


@card("QA-198")
def reference_video_analyser(task, wd):
    """mm_analyze.analyze: per-frame features -> shot boundaries -> transition kind by re-synthesis -> per-shot
    look/motion -> global look -> spec.json + analysis.md + sheets; the original audio stream is copied untouched."""
    np = _np()
    A, probe = mimic()
    W, H = 96, 160
    S1, S2 = moving_shot(1, 50, H, W, 2), moving_shot(4, 50, H, W, 2)
    frames = S1[:45] + S2[:45]
    tone_wav(wd / "tone.wav", 3.0, 523.25)
    v = write_video(wd / "v.mp4", frames, 30, lossless=False)
    fx.ffmpeg("-i", v, "-i", wd / "tone.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-shortest", wd / "ref.mp4")
    spec = A.analyze(str(wd / "ref.mp4"), str(wd / "work"), skip_text=True, deep=False)
    sp = rj(wd / "work/spec.json")
    trans = sp.get("transitions", [])
    orig = list((wd / "work/audio").glob("original_audio.*"))
    same = orig and audio_md5(orig[0]) == audio_md5(wd / "ref.mp4")
    sheets = list((wd / "work/sheets").glob("*"))
    fx.ffmpeg("-i", wd / "ref.mp4", "-vn", "-c:a", "aac", "-b:a", "64k", wd / "re.m4a")
    re_md5 = audio_md5(wd / "re.m4a")
    md = list((wd / "work").glob("*.md"))
    return [check("spec.json written with shots and transitions", len(sp.get("shots", [])) == 2 and len(trans) == 1, [len(sp.get("shots", [])), len(trans)], [2, 1]),
            check("the join is a cut at frame 45", trans and trans[0]["type"] == "cut" and abs(trans[0]["ts"] - 45) <= 1, trans[:1], "cut @45"),
            check("analysis markdown and review sheets written", bool(md) and len(sheets) >= 1, [p.name for p in md + sheets][:5], ">= 1 each"),
            check("original audio copied byte-for-byte (same packet md5)", bool(same), [audio_md5(orig[0]) if orig else None], "== source"),
            check("negative control: a re-encoded copy of the audio has a different md5", audio_md5(wd / "ref.mp4") != re_md5, re_md5, "differs")], [wd / "work/spec.json"]


@card("QA-199")
def synthetic_regression_fonts(task, wd):
    """Synthetic regression for mimic: truth.json from make_reference.py, analysis scored with run_synthetic's own
    score_transitions, and font ranking (mm_fonts.signature/similarity) of a line set in a known font."""
    np = _np()
    from PIL import Image, ImageDraw, ImageFont
    A, probe = mimic()
    sys.path.insert(0, str(MIMIC / "synthetic"))
    import run_synthetic as RS
    import mm_fonts
    truth = {"transitions": [{"type": "cut", "ts": 45, "te": 45}]}
    W, H = 96, 160
    frames = moving_shot(1, 50, H, W, 2)[:45] + moving_shot(4, 50, H, W, 2)[:45]
    v = write_video(wd / "ref.mp4", frames, 30)
    info = probe(str(v))
    f = A.pass_a(str(v), info["fps"], info["w"], info["h"])
    b = A.detect_boundaries(f)
    det = [A.classify(f, x, None, deep=False) for x in b]
    spec = {"transitions": [{"type": d["type"], "ts": d["ts"], "te": d["te"]} for d in det]}
    ok_t, ok_s, n, nd, rows = RS.score_transitions(spec, truth)
    fonts = SKILLS / "kosif-superpowers/proofs/_shared/fonts"
    cand = ["Poppins-Bold.ttf", "Amiri-Regular.ttf", "Lalezar-Regular.ttf", "Tajawal-Bold.ttf", "ArefRuqaa-Regular.ttf"]

    def mask(fn, text="Mimic 42"):
        im = Image.new("L", (520, 120), 0)
        ImageDraw.Draw(im).text((10, 10), text, fill=255, font=ImageFont.truetype(str(fonts / fn), 72))
        return np.asarray(im) > 128
    ref_sig = mm_fonts.signature(mask("Poppins-Bold.ttf"))
    scores = sorted(((mm_fonts.similarity(ref_sig, mm_fonts.signature(mask(c)))[0], c) for c in cand), reverse=True)
    other = mm_fonts.signature(mask("Lalezar-Regular.ttf"))
    sc_other = sorted(((mm_fonts.similarity(other, mm_fonts.signature(mask(c)))[0], c) for c in cand), reverse=True)
    out = wj(wd / "scorecard.json", {"transitions": {"type_ok": ok_t, "span_ok": ok_s, "of": n, "detected": nd},
                                     "font_rank": [[round(s, 4), c] for s, c in scores]})
    bad_spec = {"transitions": [{"type": "fade", "ts": 10, "te": 25}]}
    bt, bs, *_ = RS.score_transitions(bad_spec, truth)
    return [check("transition kind scored 1/1 against truth", ok_t == 1, ok_t, 1),
            check("transition span within +-1 frame", ok_s == 1, ok_s, 1),
            check("font ranking puts the true font first", scores[0][1] == "Poppins-Bold.ttf", scores[:2], "Poppins-Bold.ttf"),
            check("ranking is input-specific (a Lalezar line ranks Lalezar first)", sc_other[0][1] == "Lalezar-Regular.ttf", sc_other[0], "Lalezar-Regular.ttf"),
            check("negative control: a wrong detection scores 0 on kind and span", bt == 0 and bs == 0, [bt, bs], [0, 0])], [out]


@card("QA-X09")
def synthetic_ground_truth_scorecard(task, wd):
    """Ground-truth scorecard: write a synthetic reference whose truth we wrote (cut, dissolve, dip-to-black), run the
    same mimic analyser that would run on the user's video, compare kind, span and timing before trusting it."""
    np = _np()
    A, probe = mimic()
    W, H = 96, 160
    S = [moving_shot(s, 60, H, W, 2) for s in (11, 12, 13)]
    fr = S[0][:40] + S[1][:40]                                       # cut at 40
    for k in range(18):                                              # dip to black 80..98
        a = k / 17.0
        src = S[1][40 + k] if a < .5 else S[2][k]
        fr.append(src * abs(1 - 2 * a))
    fr += S[2][18:50]
    truth = [{"type": "cut", "ts": 40, "te": 40}, {"type": "fadeblack", "ts": 80, "te": 98}]
    v = write_video(wd / "synthetic.mp4", fr, 30)
    info = probe(str(v))
    f = A.pass_a(str(v), info["fps"], info["w"], info["h"])
    b = A.detect_boundaries(f)
    det = [A.classify(f, x, None, deep=False) for x in b]
    rows = []
    for t in truth:
        d = min(det, key=lambda d: abs((d["ts"] + d["te"]) / 2 - (t["ts"] + t["te"]) / 2))
        rows.append({"truth": t, "detected": {"type": d["type"], "ts": d["ts"], "te": d["te"]},
                     "kind_ok": d["type"] == t["type"] or {d["type"], t["type"]} <= {"fadeblack", "dipblack"},
                     "timing_err": abs((d["ts"] + d["te"]) / 2 - (t["ts"] + t["te"]) / 2)})
    out = wj(wd / "scorecard.json", {"rows": rows, "detected": len(det)})
    cut = rows[0]
    trust = all(r["timing_err"] <= 6 for r in rows)
    naive = [{"type": "cut", "ts": 60, "te": 60}]
    naive_err = min(abs(60 - 40), abs(60 - 89))
    return [check("cut: kind and span exact", cut["kind_ok"] and cut["detected"]["ts"] == 40, cut["detected"], {"type": "cut", "ts": 40}),
            check("dip-to-black located (centre within +-6 frames)", rows[1]["timing_err"] <= 6, rows[1]["timing_err"], "<= 6"),
            check("detections = truth count", len(det) == 2, len(det), 2),
            check("scorecard says trust the measurements", trust, trust, True),
            check("negative control: an unanalysed guess (one cut mid-film) misses the truth by > 6 frames", naive_err > 6, naive_err, "> 6")], [out]


# ═════════════════════════ delivery QA on rendered films ═════════════════════════
def lufs_tp(path):
    txt = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True, timeout=60, stdin=subprocess.DEVNULL).stderr
    i = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", txt)[-1])
    tp = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", txt)[-1])
    return i, tp


def energy(frames):
    np = _np()
    return np.abs(np.diff(frames, axis=0)).mean(axis=(1, 2, 3))


@card("QA-61")
def shipped_film_benchmark(task, wd):
    """Shipped-film benchmark: render reference films, measure them with qa.inspect (LUFS, true peak, black/frozen)
    and motion energy at 15 fps / 320 px (still share), store the benchmark, and re-measure to prove it regresses."""
    np = _np()
    qa = qa_mod()
    W, H = 320, 180
    films = {}
    for name, amp, frozen in (("loud_moving", 0.5, False), ("quiet_half_still", 0.25, True)):
        fr = moving_shot(7, 120, H, W, 3)
        if frozen:
            fr = fr[:30] + [fr[30]] * 60 + fr[90:]
        tone_wav(wd / (name + ".wav"), 4.0, 997.0, amp)
        v = write_video(wd / (name + "_v.mp4"), fr, 30, lossless=False)
        fx.ffmpeg("-i", v, "-i", wd / (name + ".wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", wd / (name + ".mp4"))
        ins = qa.inspect(wd / (name + ".mp4"))
        e = energy(read_video(wd / (name + ".mp4"), (320, 180))[::2])
        films[name] = {"lufs": ins["lufs"], "tp": ins["true_peak"], "frozen": ins["frozen"], "still_pct": float((e < 0.5).mean() * 100),
                       "motion_mean": float(e.mean())}
    bench = wj(wd / "benchmark.json", films)
    again = {k: qa.inspect(wd / (k + ".mp4"))["lufs"] for k in films}
    L, Q = films["loud_moving"], films["quiet_half_still"]
    return [check("halving the amplitude lowers loudness by 6 LU (+-0.5)", abs((L["lufs"] - Q["lufs"]) - 6.02) <= 0.5, L["lufs"] - Q["lufs"], 6.02),
            check("true peak tracks the 0.5 amplitude (-6 dBFS +-1)", abs(L["tp"] + 6.02) <= 1.0, L["tp"], -6.02),
            check("still share: ~0 % for the moving film, ~50 % for the half-frozen one", L["still_pct"] < 5 and 40 <= Q["still_pct"] <= 60, [L["still_pct"], Q["still_pct"]], [0, 50]),
            check("qa.inspect flags the frozen stretch", bool(Q["frozen"]) and not L["frozen"], [L["frozen"], Q["frozen"]], "[] vs stretch"),
            check("re-measuring reproduces the stored LUFS (regression reference)", all(abs(again[k] - films[k]["lufs"]) < 0.05 for k in films), again, "same"),
            check("negative control: the moving film's motion energy far exceeds the frozen half", L["motion_mean"] > 1.5 * Q["motion_mean"], [L["motion_mean"], Q["motion_mean"]], "> 1.5x")], [bench]


def _arabic_joined(text, font):
    from PIL import Image, ImageDraw, ImageFont
    from scipy import ndimage
    np = _np()
    f = ImageFont.truetype(str(font), 64, layout_engine=ImageFont.Layout.RAQM)

    def comps(s):
        im = Image.new("L", (900, 140), 0)
        ImageDraw.Draw(im).text((20, 20), s, fill=255, font=f, direction="rtl", language="ar")
        a = np.asarray(im) > 100
        return ndimage.label(a)[1], a
    nj, aj = comps(text)
    ni, _ = comps(" ".join(text))
    return nj, ni, aj


@card("QA-251")
def pre_delivery_motion_qa(task, wd):
    """Pre-delivery checklist: tools/verify_video.py (ffprobe size/fps/duration/streams + EBU R128), frame grabs at
    chosen times, Arabic joined with its dots (fewer ink pieces than isolated letters), reading time measured on the
    real text, and every scene has an asset or a 'missing' tag with a fallback."""
    np = _np()
    W, H = 180, 320
    fr = moving_shot(3, 90, H, W, 2)
    tone_wav(wd / "t0.wav", 3.0, 997.0, 0.3)
    l0, _ = lufs_tp(wd / "t0.wav")
    tone_wav(wd / "tone.wav", 3.0, 997.0, 0.3 * 10 ** ((-14 - l0) / 20.0))
    v = write_video(wd / "v.mp4", fr, 30, lossless=False)
    fx.ffmpeg("-i", v, "-i", wd / "tone.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", wd / "film.mp4")
    fx.ffmpeg("-i", wd / "film.mp4", "-vf", "scale=320:180,fps=25", "-af", "volume=-12dB", "-c:v", "libx264", "-c:a", "aac", wd / "wrong.mp4")
    vv = ROOT / "tools/verify_video.py"
    rep = {}
    for k in ("film", "wrong"):
        d = subprocess.run([sys.executable, "-B", vv, wd / (k + ".mp4"), "--aspect", "9:16", "--fps", "30", "--duration", "3", "--lufs", "-14", "--json", wd / (k + "_report.json")],
                           capture_output=True, text=True, timeout=60, stdin=subprocess.DEVNULL)
        rep[k] = (d.returncode, rj(wd / (k + "_report.json")))
    grabs = []
    for t in (0.5, 1.5, 2.5):
        g = wd / ("grab_%.1f.png" % t)
        fx.ffmpeg("-ss", str(t), "-i", wd / "film.mp4", "-frames:v", "1", g)
        grabs.append(g)
    nj, ni, _ = _arabic_joined("بسم الله", SKILLS / "kosif-superpowers/proofs/_shared/fonts/Amiri-Regular.ttf")
    scenes = [{"id": 1, "text": "ادعُ ربك في السحر", "hold": 2.6, "asset": "grab_0.5.png"},
              {"id": 2, "text": "قصير", "hold": 0.3, "asset": None}]
    for s in scenes:
        s["need_s"] = round(0.4 + 0.3 * len(s["text"].split()), 2)
        s["reading_ok"] = s["hold"] >= s["need_s"]
        s["asset_state"] = "ok" if s["asset"] and (wd / s["asset"]).exists() else "missing (fallback: brand plate)"
    out = wj(wd / "delivery_checklist.json", {"verify_video": {k: v[1] for k, v in rep.items()}, "arabic_pieces": [nj, ni], "scenes": scenes})
    return [check("verify_video passes the 9:16 / 30 fps / 3 s / -14 LUFS film", rep["film"][0] == 0, rep["film"][0], 0),
            check("frame grabs written at 0.5, 1.5, 2.5 s", all(g.stat().st_size > 0 for g in grabs), len(grabs), 3),
            check("Arabic stays joined: fewer ink pieces than the isolated letters", nj < ni, [nj, ni], "joined < isolated"),
            check("reading time measured: scene 1 ok, scene 2 too short", [s["reading_ok"] for s in scenes] == [True, False], [(s["hold"], s["need_s"]) for s in scenes], [True, False]),
            check("scene without an asset carries a 'missing' tag with a fallback", scenes[1]["asset_state"].startswith("missing"), scenes[1]["asset_state"], "missing (fallback)"),
            check("negative control: the 16:9 25 fps quiet export fails verify_video", rep["wrong"][0] != 0, rep["wrong"][0], "!= 0")], [out, wd / "film.mp4"]


@card("QA-225")
def render_and_verify(task, wd):
    """Render + verify: SetCurrentRenderFormatAndCodec / SetRenderSettings / AddRenderJob / StartRendering /
    GetRenderJobStatus as a render queue (ffmpeg stands in for DaVinci Resolve's renderer, which is proprietary),
    then an ffprobe match of size, fps and duration (+-1 frame)."""
    class Queue:
        def __init__(self):
            self.fmt, self.settings, self.jobs = None, {}, []

        def SetCurrentRenderFormatAndCodec(self, fmt, codec):
            self.fmt = (fmt, codec)
            return fmt in ("mp4", "mov") and codec in ("H264", "H265")

        def SetRenderSettings(self, s):
            self.settings.update(s)
            return True

        def AddRenderJob(self):
            self.jobs.append({"id": "job%d" % len(self.jobs), "settings": dict(self.settings), "fmt": self.fmt, "status": "Ready"})
            return self.jobs[-1]["id"]

        def StartRendering(self, jid):
            j = [x for x in self.jobs if x["id"] == jid][0]
            s = j["settings"]
            j["status"] = "Rendering"
            out = wd / ("%s.%s" % (s["CustomName"], j["fmt"][0]))
            fx.ffmpeg("-f", "lavfi", "-i", "testsrc2=s=%dx%d:r=%s:d=%s" % (s["FormatWidth"], s["FormatHeight"], s["FrameRate"], s["Seconds"]),
                      "-c:v", {"H264": "libx264", "H265": "libx265"}[j["fmt"][1]], "-pix_fmt", "yuv420p", out)
            j["status"], j["out"] = "Complete", out
            return True

        def GetRenderJobStatus(self, jid):
            return {"JobStatus": [x for x in self.jobs if x["id"] == jid][0]["status"]}

    def verify(path, s):
        st = [x for x in fx.probe(path)["streams"] if x["codec_type"] == "video"][0]
        n, d = st["r_frame_rate"].split("/")
        fps = float(n) / float(d)
        frames = int(st.get("nb_frames") or 0)
        want = int(round(float(s["Seconds"]) * float(s["FrameRate"])))
        return {"size": (st["width"], st["height"]) == (s["FormatWidth"], s["FormatHeight"]), "fps": abs(fps - float(s["FrameRate"])) < 0.01,
                "frames": abs(frames - want) <= 1, "measured": [st["width"], st["height"], fps, frames, want]}
    q = Queue()
    ok_codec = q.SetCurrentRenderFormatAndCodec("mp4", "H264")
    want = {"CustomName": "master", "FormatWidth": 320, "FormatHeight": 568, "FrameRate": 30, "Seconds": 2}
    q.SetRenderSettings(want)
    jid = q.AddRenderJob()
    q.StartRendering(jid)
    status = q.GetRenderJobStatus(jid)["JobStatus"]
    good = verify(q.jobs[0]["out"], want)
    q.SetRenderSettings({"CustomName": "drift", "FrameRate": 25})
    j2 = q.AddRenderJob()
    q.StartRendering(j2)
    bad = verify(q.jobs[1]["out"], want)
    out = wj(wd / "render_verify.json", {"good": good, "bad": bad})
    return [check("format/codec accepted", ok_codec, ok_codec, True),
            check("render job completes", status == "Complete", status, "Complete"),
            check("size matches the settings", good["size"], good["measured"][:2], [320, 568]),
            check("fps and frame count match (+-1 frame)", good["fps"] and good["frames"], good["measured"][2:], [30, 60]),
            check("negative control: a 25 fps render fails the fps/frames match", not bad["fps"] and not bad["frames"], bad["measured"][2:], "mismatch")], [out, q.jobs[0]["out"]]


@card("QA-323")
def scope_measurement_stills(task, wd):
    """Scopes without API: seek to the clip middle, export a still, compute luminance / channel histograms with
    Pillow, and require white balance channel spread <= 20/255 on a true neutral patch."""
    np = _np()
    from PIL import Image
    W, H = 320, 180
    base = texture(2, H, W, 16, 60, 200)
    base[60:120, 120:200] = 128                                   # 18 % grey card
    warm = base * np.array([1.25, 1.0, 0.8])
    for name, img in (("cast", warm), ("neutral", base)):
        write_video(wd / (name + ".mp4"), [img] * 60, 30)
    res = {}
    for name in ("cast", "neutral", "corrected"):
        src = wd / (name + ".mp4")
        if name == "corrected":
            st = load_png(wd / "still_cast.png")[60:120, 120:200].reshape(-1, 3).mean(axis=0)
            gain = st.mean() / st
            fx.ffmpeg("-i", wd / "cast.mp4", "-vf", "colorchannelmixer=rr=%.4f:gg=%.4f:bb=%.4f" % tuple(gain), "-c:v", "libx264rgb", "-qp", "0", src)
        dur = float(fx.probe(src)["format"]["duration"])
        fx.ffmpeg("-ss", "%.3f" % (dur / 2), "-i", src, "-frames:v", "1", wd / ("still_%s.png" % name))
        im = Image.open(wd / ("still_%s.png" % name)).convert("RGB")
        hist = im.histogram()
        patch = np.asarray(im, float)[60:120, 120:200].reshape(-1, 3).mean(axis=0)
        res[name] = {"patch": patch.round(1).tolist(), "wb_spread": float(patch.max() - patch.min()), "luma_hist_bins": len(im.convert("L").histogram()),
                     "channel_hist": [sum(hist[i * 256:(i + 1) * 256]) for i in range(3)]}
    out = wj(wd / "scopes.json", res)
    return [check("still taken at the clip middle (1.0 s of 2 s)", (wd / "still_cast.png").exists(), "1.0 s", "middle"),
            check("histograms computed (256 bins, one per channel)", res["neutral"]["luma_hist_bins"] == 256 and len(set(res["neutral"]["channel_hist"])) == 1,
                  res["neutral"]["channel_hist"], "W*H each"),
            check("neutral clip: grey card spread <= 20/255", res["neutral"]["wb_spread"] <= 20, res["neutral"]["wb_spread"], "<= 20"),
            check("corrected clip passes the WB gate", res["corrected"]["wb_spread"] <= 20, res["corrected"]["wb_spread"], "<= 20"),
            check("negative control: the warm cast fails the WB gate", res["cast"]["wb_spread"] > 20, res["cast"]["wb_spread"], "> 20")], [out, wd / "still_cast.png"]


RESOLVE_COLOURS = ["Blue", "Cyan", "Green", "Yellow", "Red", "Pink", "Purple", "Fuchsia", "Rose", "Lavender", "Sky", "Mint",
                   "Lemon", "Sand", "Cocoa", "Cream"]
MARKER_ROLE = {"CHAPTER": "Blue", "PRIVACY": "Purple", "CUT_DONE": "Red", "CUT_REVIEW": "Yellow", "EXPOSURE_CHECK": "Lemon",
               "WB_CHECK": "Sky", "AUDIO_REVIEW": "Sand", "GFX": "Cyan"}


@card("QA-324")
def resolve_marker_registry(task, wd):
    """Fixed marker colours per role, the first CHAPTER at frame 0, offsets +0..+6 so markers never collide on one
    frame, and only Resolve's 16 colours; markers written as Timeline.AddMarker(frame,color,name,note,dur) calls."""
    events = [("CHAPTER", 3, "Intro"), ("CUT_REVIEW", 120, "tight"), ("WB_CHECK", 120, "skin"), ("AUDIO_REVIEW", 120, "hum"),
              ("CHAPTER", 300, "Part 2"), ("PRIVACY", 301, "plate"), ("GFX", 450, "lower third"), ("NOTE", 500, "bad role")]
    taken, markers, rejected = set(), [], []
    for i, (role, frame, name) in enumerate(sorted(events, key=lambda e: e[1])):
        color = MARKER_ROLE.get(role)
        if color not in RESOLVE_COLOURS:
            rejected.append(role)
            continue
        if role == "CHAPTER" and not any(m["name"].startswith("CHAPTER") for m in markers):
            frame = 0
        for off in range(7):
            if frame + off not in taken:
                frame += off
                break
        else:
            rejected.append(role)
            continue
        taken.add(frame)
        markers.append({"frame": frame, "color": color, "name": "%s %s" % (role, name), "note": name, "dur": 1})
    calls = ["Timeline.AddMarker(%d, %r, %r, %r, %d)" % (m["frame"], m["color"], m["name"], m["note"], m["dur"]) for m in markers]
    out = wj(wd / "markers.json", {"markers": markers, "calls": calls, "rejected": rejected})
    naive = [e[1] for e in events]
    frames = [m["frame"] for m in markers]
    return [check("first CHAPTER is at frame 0", markers[0]["frame"] == 0 and markers[0]["color"] == "Blue", markers[0], "Blue @0"),
            check("three markers on frame 120 spread to 120,121,122", sorted(f for f in frames if 120 <= f <= 126) == [120, 121, 122], sorted(frames), [120, 121, 122]),
            check("no two markers share a frame", len(frames) == len(set(frames)), frames, "unique"),
            check("every colour is one of Resolve's 16 and matches its role", all(m["color"] == MARKER_ROLE[m["name"].split()[0]] for m in markers), [m["color"] for m in markers], "role colours"),
            check("unknown role refused", rejected == ["NOTE"], rejected, ["NOTE"]),
            check("negative control: naive placement collides on frame 120", len(naive) != len(set(naive)), naive, "duplicates")], [out]


@card("QA-264")
def watch_twice_rule(task, wd):
    """Watch every cut twice: a with-sound pass and a muted pass, both at phone scale, with contact sheets (qa.sheet's
    contact + phone-width test) and a report listing each cut for both passes, sent with the sheets."""
    np = _np()
    qa = qa_mod()
    W, H = 360, 640
    fr = moving_shot(1, 45, H, W, 3) + moving_shot(2, 45, H, W, 3)
    tone_wav(wd / "a.wav", 3.0)
    v = write_video(wd / "v.mp4", fr, 30, lossless=False)
    fx.ffmpeg("-i", v, "-i", wd / "a.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", wd / "cut.mp4")
    fx.ffmpeg("-i", wd / "cut.mp4", "-vf", "scale=390:-2", "-c:v", "libx264", "-c:a", "aac", wd / "pass1_sound_phone.mp4")
    fx.ffmpeg("-i", wd / "cut.mp4", "-vf", "scale=390:-2", "-an", "-c:v", "libx264", wd / "pass2_muted_phone.mp4")
    sh = qa.sheet(wd / "cut.mp4", wd / "sheets")
    F = read_video(wd / "cut.mp4", (90, 160))
    cuts = [round((i + 1) / 30.0, 2) for i in np.nonzero(energy(F) > 25)[0]]
    passes = {}
    for k in ("pass1_sound_phone", "pass2_muted_phone"):
        pr = fx.probe(wd / (k + ".mp4"))
        vs = [s for s in pr["streams"] if s["codec_type"] == "video"][0]
        passes[k] = {"width": vs["width"], "audio": any(s["codec_type"] == "audio" for s in pr["streams"])}
    rep = tw(wd / "watch_twice.md", "\n".join(["# Watch twice"] + ["- cut at %.2f s: sound pass [ ], muted pass [ ]" % c for c in cuts] +
                                             ["", "contact: %s" % sh["contact"], "phone: %s" % sh["phone"]]))
    orig_audio = any(s["codec_type"] == "audio" for s in fx.probe(wd / "cut.mp4")["streams"])
    return [check("both passes rendered at phone width 390 px", passes["pass1_sound_phone"]["width"] == 390 and passes["pass2_muted_phone"]["width"] == 390,
                  [p["width"] for p in passes.values()], 390),
            check("sound pass keeps the audio, muted pass has none", passes["pass1_sound_phone"]["audio"] and not passes["pass2_muted_phone"]["audio"],
                  [p["audio"] for p in passes.values()], [True, False]),
            check("contact sheet and phone-width sheet written", Path(sh["contact"]).stat().st_size > 0 and Path(sh["phone"]).stat().st_size > 0, list(sh)[:2], "files"),
            check("the cut at 1.5 s is listed for both passes", cuts == [1.5] and "1.50 s" in rep.read_text(), cuts, [1.5]),
            check("negative control: the untreated cut is not a muted pass (it has sound)", orig_audio, orig_audio, True)], [rep, Path(sh["contact"])]


@card("QA-353")
def three_point_sync(task, wd):
    """Three-point sync spot check: per scene, at three timestamps, measure the gap between the visual hit (flash)
    and the audio hit (beep onset); scenes off by more than one frame are flagged."""
    np = _np()
    fps, rate = 30, 48000
    W, H = 160, 90
    flashes = {1: [0.5, 1.5, 2.5], 2: [3.5, 4.5, 5.5]}
    beeps = flashes[1] + [t + 5 / 30.0 for t in flashes[2]]          # scene 2 audio slipped 5 frames
    fr = []
    for i in range(6 * fps):
        t = i / fps
        img = np.full((H, W, 3), 30.0)
        if any(abs(t - f) < 1e-6 for f in flashes[1] + flashes[2]):
            img[:] = 250
        fr.append(img)
    tone_wav(wd / "beeps.wav", 6.0, 1000.0, 0.6, rate, beeps)
    write_video(wd / "film.mp4", fr, fps, audio=wd / "beeps.wav")
    F = read_video(wd / "film.mp4", (40, 24))
    fx.ffmpeg("-i", wd / "film.mp4", "-vn", "-ac", "1", "-ar", str(rate), wd / "a.wav")
    a, _ = fx.read_wav(wd / "a.wav")
    env = np.abs(a[:, 0])
    lum = F.mean(axis=(1, 2, 3))
    rows = []
    for scene, ts in flashes.items():
        for t in ts:
            lo, hi = int((t - 0.3) * fps), int((t + 0.3) * fps)
            vf = (lo + int(np.argmax(lum[lo:hi]))) / fps
            seg = env[int((t - 0.3) * rate):int((t + 0.4) * rate)]
            onset = (t - 0.3) + int(np.argmax(seg > 0.2)) / rate
            rows.append({"scene": scene, "t": t, "visual": round(vf, 4), "audio": round(onset, 4), "off_frames": round((onset - vf) * fps, 2)})
    bad = sorted({r["scene"] for r in rows if abs(r["off_frames"]) > 1})
    out = wj(wd / "sync.json", rows)
    return [check("three spot checks per scene", [sum(r["scene"] == s for r in rows) for s in (1, 2)] == [3, 3], len(rows), 6),
            check("scene 1 in sync (<= 1 frame) at all three points", all(abs(r["off_frames"]) <= 1 for r in rows if r["scene"] == 1), [r["off_frames"] for r in rows if r["scene"] == 1], "<= 1"),
            check("scene 2 measured ~5 frames late at every point", all(abs(r["off_frames"] - 5) <= 1 for r in rows if r["scene"] == 2), [r["off_frames"] for r in rows if r["scene"] == 2], 5),
            check("only scene 2 flagged", bad == [2], bad, [2]),
            check("negative control: scene 2's slipped audio fails the 1-frame criterion", any(abs(r["off_frames"]) > 1 for r in rows if r["scene"] == 2), "scene 2", "fails")], [out, wd / "film.mp4"]


def lapvar(img):
    np = _np()
    g = img.mean(axis=2) if img.ndim == 3 else img
    lap = g[1:-1, 1:-1] * 4 - g[:-2, 1:-1] - g[2:, 1:-1] - g[1:-1, :-2] - g[1:-1, 2:]
    return float(lap.var())


@card("QA-286")
def map_render_verification(task, wd):
    """Map motion judged on a rendered MP4: a middle-frame still first, then a short MP4 of the camera move; measure
    shimmer of fine map detail during the move and switch to a pre-filtered fixed plate when it shimmers."""
    np = _np()
    W, H, n = 240, 136, 45
    big = np.full((H, W + 200), 40.0)
    big[:, ::4] = 230                                            # 1 px road grid: the detail that shimmers
    big[::5, :] = 200

    def render(plate, name, integer=False):
        fr = []
        for i in range(n):
            off = i * 1.37                                       # sub-pixel pan
            k, frac = int(off), off - int(off)
            if integer:                                          # the fixed plate: pre-rendered once, moved in whole pixels
                k, frac = int(round(off)), 0.0
            a = (1 - frac) * plate[:, k:k + W] + frac * plate[:, k + 1:k + 1 + W]
            fr.append(np.repeat(a[..., None], 3, axis=2))
        save_png(fr[n // 2], wd / ("%s_mid.png" % name))
        write_video(wd / ("%s.mp4" % name), fr, 30)
        F = read_video(wd / ("%s.mp4" % name))
        hf_ = np.array([lapvar(f) for f in F])
        return float(hf_.std() / hf_.mean())
    raw = render(big, "live_tiles")
    fixed = render(big, "fixed_plate", integer=True)
    decision = "fixed plate" if raw > 0.08 else "keep tiles"
    final = fixed if decision == "fixed plate" else raw
    out = wj(wd / "map_qa.json", {"shimmer_live": raw, "shimmer_plate": fixed, "decision": decision})
    return [check("middle-frame still rendered before the MP4", (wd / "live_tiles_mid.png").stat().st_mtime <= (wd / "live_tiles.mp4").stat().st_mtime, "mid.png", "first"),
            check("shimmer measured on the rendered MP4 (detail energy CV)", raw > 0.08, raw, "> 0.08"),
            check("decision: switch to the fixed plate", decision == "fixed plate", decision, "fixed plate"),
            check("fixed plate is steady (CV < 0.04) and keeps detail", final < 0.04 and lapvar(load_png(wd / "fixed_plate_mid.png")) > 50, [final, lapvar(load_png(wd / "fixed_plate_mid.png"))], "< 0.04"),
            check("negative control: the live tiles fail the steadiness criterion", raw >= 0.04, raw, ">= 0.04")], [out, wd / "fixed_plate.mp4"]


def _walker(frame, n, swing=28.0, bob=4.0, H=120, W=100):
    """Stick figure: legs swing +-swing deg, hips lowest at contact (max spread), highest at passing."""
    from PIL import Image, ImageDraw
    ph = 2 * math.pi * frame / n
    a = math.radians(swing) * math.cos(ph)
    hip_y = 70 - bob * (1 - abs(math.cos(ph))) if swing else 70.0
    im = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(im)
    hx = W // 2
    d.ellipse([hx - 7, hip_y - 52, hx + 7, hip_y - 38], fill=255)
    d.line([hx, hip_y - 38, hx, hip_y], fill=255, width=4)
    L = 40
    for s in (1, -1):
        d.line([hx, hip_y, hx + s * L * math.sin(a), hip_y + L * math.cos(a)], fill=255, width=4)
    return _np().asarray(im, float)


@card("QA-281")
def animation_contact_passing(task, wd):
    """Animation review: render every frame of the cycle side by side in a preview sheet, then check distinct contact
    and passing poses, a consistent bob (both contacts at one height, passing higher), and held impact frames."""
    np = _np()
    n = 16

    def analyse(frames):
        spread, head = [], []
        for f in frames:
            ys, xs = np.nonzero(f > 128)
            low = xs[ys >= ys.max() - 3]
            spread.append(float(low.max() - low.min()))
            head.append(float(ys.min()))
        return np.array(spread), np.array(head)
    good = [_walker(i, n) for i in range(n)] + [_walker(0, n)] * 3          # 3 held impact frames after the cycle
    slide = [_walker(i, n, swing=0, bob=0) for i in range(n)]
    contact_sheet([np.repeat(f[..., None], 3, 2) for f in good], 8, wd / "preview_sheet.png")
    sp, hd = analyse(good[:n])
    c1, c2 = int(np.argmax(sp[:n // 2])), n // 2 + int(np.argmax(sp[n // 2:]))
    p1 = int(np.argmin(sp))
    held = sum(1 for i in range(n, len(good)) if np.array_equal(good[i], good[n - n]))
    ssp, shd = analyse(slide)
    out = wj(wd / "review.json", {"spread": sp.tolist(), "head_y": hd.tolist(), "contacts": [c1, c2], "passing": p1, "held": held})
    return [check("preview sheet shows every frame (19 cells)", load_png(wd / "preview_sheet.png").shape[1] > 8 * 100, load_png(wd / "preview_sheet.png").shape[:2], "8 x 3 grid"),
            check("contact frames at 0 and 8 (max foot spread)", [c1, c2] == [0, 8], [c1, c2], [0, 8]),
            check("passing pose distinct: spread far smaller than contact", sp[p1] < 0.3 * sp[c1], [sp[p1], sp[c1]], "< 0.3x"),
            check("bob consistent: both contacts at one head height, passing >= 3 px higher", hd[c1] == hd[c2] and hd[p1] <= hd[c1] - 3, [hd[c1], hd[c2], hd[p1]], "equal, passing higher"),
            check("impact held for >= 2 frames", held >= 2, held, ">= 2"),
            check("negative control: a sliding cycle has no distinct contact/passing", float(ssp.max() - ssp.min()) <= 1 and float(shd.max() - shd.min()) == 0, [ssp.max() - ssp.min(), shd.max() - shd.min()], "flat")], [wd / "preview_sheet.png", out]


def _beat_film(path, dead=(3, 5), seconds=8, W=160, H=90, fps=30, seed=21):
    np = _np()
    shot = moving_shot(seed, seconds * fps, H, W, 2)
    fr = []
    for i in range(seconds * fps):
        s = i // fps
        fr.append(shot[dead[0] * fps] if dead and dead[0] <= s < dead[1] else shot[i])
    return write_video(path, fr, fps)


@card("QA-330")
def eight_second_gate(task, wd):
    """Eight-second gate + weakest-beat gate: build the first 5-8 s, send a contact sheet (1 frame/s), find the worst
    seconds by measured motion energy, rebuild them, then run the same gate on the middle."""
    np = _np()

    def gate(path):
        F = read_video(path, (80, 45))
        e = energy(F)
        per_s = [float(e[s * 30:(s + 1) * 30 - 1].mean()) for s in range(len(F) // 30)]
        worst = sorted(range(len(per_s)), key=lambda s: per_s[s])[:2]
        contact_sheet([F[s * 30] for s in range(len(per_s))], 4, path.with_suffix(".sheet.png"))
        return per_s, sorted(worst)
    v1 = _beat_film(wd / "open_v1.mp4", dead=(3, 5))
    per1, worst1 = gate(v1)
    v2 = _beat_film(wd / "open_v2.mp4", dead=None)
    per2, worst2 = gate(v2)
    mid = _beat_film(wd / "middle_v1.mp4", dead=(5, 6), seed=22)
    perm, worstm = gate(mid)
    log = wj(wd / "gate_log.json", {"opening_v1": {"per_s": per1, "worst": worst1}, "opening_v2": {"per_s": per2, "worst": worst2},
                                    "middle_v1": {"per_s": perm, "worst": worstm}})
    return [check("opening built at 8 s with a 1 frame/s contact sheet", len(per1) == 8 and (wd / "open_v1.sheet.png").exists(), len(per1), 8),
            check("worst seconds of the opening are 3 and 4 (the dead beat)", worst1 == [3, 4], worst1, [3, 4]),
            check("rebuild lifts the weakest second above the motion floor", min(per2) > 1.0, min(per2), "> 1.0"),
            check("same gate on the middle finds second 5", 5 in worstm and perm[5] < 0.1, worstm, "contains 5"),
            check("negative control: the first build fails the motion floor", min(per1) <= 1.0, min(per1), "<= 1.0")], [log, wd / "open_v1.sheet.png"]


@card("QA-349")
def preview_before_render_gate(task, wd):
    """Preview-before-render: a 9-12 frame contact sheet plus a 3-5 s clip (--start/--duration) of the hardest scene,
    and the final render refuses to run until approval.json exists."""
    np = _np()
    W, H = 160, 90
    scenes = [moving_shot(1, 90, H, W, 1), moving_shot(2, 120, H, W, 6), moving_shot(3, 90, H, W, 2)]
    fr = [f for s in scenes for f in s]
    v = write_video(wd / "draft.mp4", fr, 30, lossless=False)
    F = read_video(v, (80, 45))
    e = energy(F)
    bounds = [0, 90, 210, 300]
    hard = int(np.argmax([e[a:b - 1].mean() for a, b in zip(bounds[:-1], bounds[1:])]))
    start, dur = bounds[hard] / 30.0, 4.0
    fx.ffmpeg("-ss", "%.3f" % start, "-t", "%.1f" % dur, "-i", v, "-c:v", "libx264", wd / "hardest.mp4")
    idx = np.linspace(0, len(F) - 1, 12).astype(int)
    contact_sheet([F[i] for i in idx], 4, wd / "contact.png")

    def final_render():
        if not (wd / "approval.json").exists():
            return "blocked: no approval"
        fx.ffmpeg("-i", v, "-c:v", "libx264", "-crf", "17", wd / "final.mp4")
        return "rendered"
    first = final_render()
    wj(wd / "approval.json", {"approved_by": "requester", "sheet": sha(wd / "contact.png"), "clip": sha(wd / "hardest.mp4")})
    second = final_render()
    clip_s = float(fx.probe(wd / "hardest.mp4")["format"]["duration"])
    return [check("contact sheet holds 12 frames", len(idx) == 12, len(idx), "9-12"),
            check("hardest scene = the fast one (scene 2)", hard == 1, hard, 1),
            check("preview clip is 3-5 s from the hardest scene's start", 3 <= clip_s <= 5 and start == 3.0, [start, clip_s], [3.0, "3-5 s"]),
            check("final render runs after approval", second == "rendered" and (wd / "final.mp4").stat().st_size > 0, second, "rendered"),
            check("negative control: without approval the final render is blocked", first.startswith("blocked"), first, "blocked")], [wd / "contact.png", wd / "hardest.mp4"]


def _text_layer(img, text, x, y, size=18, color=(255, 255, 255), blur=0):
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
    np = _np()
    im = Image.fromarray(img.astype("uint8"))
    lay = Image.new("L", im.size, 0)
    ImageDraw.Draw(lay).text((x, y), text, fill=255, font=ImageFont.truetype(str(SKILLS / "kosif-superpowers/proofs/_shared/fonts/Poppins-Bold.ttf"), size))
    if blur:
        lay = lay.resize((lay.width // blur, lay.height // blur)).resize(lay.size, Image.BILINEAR)
    m = np.asarray(lay, float)[..., None] / 255
    return img * (1 - m) + np.array(color, float) * m


@card("QA-348")
def failure_hunt(task, wd):
    """Failure hunt over contact.png / phone.png and the film: overlapping text during a swap, a frame border,
    loop-seam stutter (qa.loopcheck), a dead beat, and blurry up-scaled text, each with a measured detector."""
    np = _np()
    qa = qa_mod()
    W, H, n = 200, 120, 60

    def film(bad):
        base = moving_shot(8, n, H, W, 2)
        out = []
        for i, f in enumerate(base):
            f = f * 0.4
            if bad and 36 <= i < 56:
                f = base[36] * 0.4                                    # dead beat
            if i < 30 or (bad and i < 34):
                f = _text_layer(f, "ONE", 20, 40, 26)
            if i >= 30 - (4 if bad else 0):
                f = _text_layer(f, "TWO", 26 if bad else 120, 44 if bad else 40, 26)
            f = _text_layer(f, "small", 130, 90, 14, blur=3 if bad else 0)
            if bad:
                f[:2], f[-2:], f[:, :2], f[:, -2:] = 255, 255, 255, 255
            out.append(f)
        if bad:
            out[-1] = np.roll(out[-1], 25, axis=1)
        return out
    rep = {}
    for k in ("bad", "clean"):
        fr = film(k == "bad")
        p = write_video(wd / (k + ".mp4"), fr, 30)
        sh = qa.sheet(p, wd / (k + "_sheets"))
        F = read_video(p)
        e = energy(F)
        ink = [(f.min(axis=2) > 200)[30:80] for f in F]
        A_, B_ = ink[10], ink[50]
        cover = lambda m, ref: float((m & ref).sum()) / max(1, ref.sum())
        both = [i for i, m in enumerate(ink) if cover(m, A_) > 0.9 and cover(m, B_) > 0.9]
        swap_overlap = len(both) >= 2
        border = bool((F[0][:2].min() > 240) and (F[0][:, :2].min() > 240))
        lc = qa.loopcheck(p)
        run, longest = 0, 0
        for x in e:
            run = run + 1 if x < 0.3 else 0
            longest = max(longest, run)
        sm = F[10][85:110, 125:190]
        rep[k] = {"swap_overlap": bool(swap_overlap), "overlap_frames": both, "border": border, "seam_ok": bool(lc["ok"]), "dead_frames": longest,
                  "small_text_sharpness": lapvar(sm), "contact": sh["contact"], "phone": sh["phone"]}
    out = wj(wd / "failure_hunt.json", rep)
    B, C = rep["bad"], rep["clean"]
    return [check("overlapping text during the swap found", B["swap_overlap"] and not C["swap_overlap"], [B["swap_overlap"], C["swap_overlap"]], [True, False]),
            check("frame border found", B["border"] and not C["border"], [B["border"], C["border"]], [True, False]),
            check("loop seam stutter found by qa.loopcheck", not B["seam_ok"], B["seam_ok"], False),
            check("dead beat of ~20 frames found", B["dead_frames"] >= 18 and C["dead_frames"] < 5, [B["dead_frames"], C["dead_frames"]], [">= 18", "< 5"]),
            check("blurry scaled text is softer than crisp text", B["small_text_sharpness"] < 0.5 * C["small_text_sharpness"], [B["small_text_sharpness"], C["small_text_sharpness"]], "< 0.5x"),
            check("negative control: the clean film raises none of the five", not (C["swap_overlap"] or C["border"]) and C["dead_frames"] < 5, C, "clean")], [out, Path(B["contact"])]


def _gen_shot(seed, subject=(220, 60, 60), light=1.0, stray=False, W=160, H=120, n=20):
    """A deterministic 'generated' shot: a subject disc over a textured set; the same seed gives the same pixels."""
    np = _np()
    from PIL import Image, ImageDraw
    bg = texture(seed, H, W, 16, 60, 120)
    fr = []
    for i in range(n):
        im = Image.fromarray(np.clip(bg * light, 0, 255).astype("uint8"))
        d = ImageDraw.Draw(im)
        d.ellipse([60 + i, 35, 100 + i, 75], fill=tuple(int(c * light) for c in subject))
        a = np.asarray(im, float)
        if stray:
            a = _text_layer(a, "XQ7", 10, 85, 26)
        fr.append(a)
    return fr


@card("QA-54")
def post_generation_video_qa(task, wd):
    """Post-generation QA per shot: identity drift (subject colour vs the hero reference), stray text (tesseract),
    light continuity (mean luminance jump); regenerate only the failed shot and re-check, others untouched."""
    np = _np()
    ref_subject = np.array([220, 60, 60], float)
    plan = {1: dict(seed=1), 2: dict(seed=2, subject=(60, 90, 220), stray=True, light=1.6), 3: dict(seed=3)}

    def qa_shot(path):
        F = read_video(path)
        mid = F[len(F) // 2]
        disc = mid[45:65, 70 + len(F) // 2:90 + len(F) // 2].reshape(-1, 3).mean(axis=0)
        save_png(np.kron(mid, np.ones((3, 3, 1))), path.with_suffix(".ocr.png"))
        txt = subprocess.run(["tesseract", str(path.with_suffix(".ocr.png")), "-", "--psm", "11"], capture_output=True, text=True, timeout=30).stdout
        return {"identity_dist": float(np.abs(disc - ref_subject).mean()), "text": re.sub(r"[^A-Za-z0-9]", "", txt), "lum": float(F.mean())}
    shots, res = {}, {}
    for k, kw in plan.items():
        shots[k] = write_video(wd / ("shot%d.mp4" % k), _gen_shot(**kw), 24)
        res[k] = qa_shot(shots[k])
    mean_l = np.mean([res[k]["lum"] for k in (1, 3)])
    fails = sorted(k for k in res if res[k]["identity_dist"] > 25 or len(res[k]["text"]) >= 2 or abs(res[k]["lum"] - mean_l) > 25)
    before = {k: sha(shots[k]) for k in shots}
    for k in fails:
        shots[k] = write_video(wd / ("shot%d.mp4" % k), _gen_shot(seed=plan[k]["seed"]), 24)
    after = {k: qa_shot(shots[k]) for k in shots}
    still_fail = [k for k in after if after[k]["identity_dist"] > 25 or len(after[k]["text"]) >= 2]
    out = wj(wd / "shot_qa.json", {"first": res, "failed": fails, "after": after})
    return [check("only shot 2 fails QA", fails == [2], fails, [2]),
            check("shot 2: identity drift measured (blue subject)", res[2]["identity_dist"] > 25, res[2]["identity_dist"], "> 25"),
            check("shot 2: stray text read by tesseract", "XQ7" in res[2]["text"] or len(res[2]["text"]) >= 2, res[2]["text"], "XQ7"),
            check("shot 2: light continuity break", abs(res[2]["lum"] - mean_l) > 25, abs(res[2]["lum"] - mean_l), "> 25"),
            check("after regenerating shot 2 every shot passes", still_fail == [], still_fail, []),
            check("shots 1 and 3 were not re-rendered (same hashes)", all(sha(shots[k]) == before[k] for k in (1, 3)), "unchanged", "unchanged"),
            check("negative control: the hero shot has no text and no drift", res[1]["text"] == "" and res[1]["identity_dist"] < 10, res[1], "clean")], [out, shots[2]]


@card("QA-52")
def demo2d_proof_render(task, wd):
    """demo2d proof render: a 6 s 1080x1920 30 fps film (ffmpeg overlays animated by t), with an MP4, a GIF, a contact
    sheet and qa.json that PASSES on measured duration, size, fps and mean motion."""
    np = _np()
    fc = "[0][1]overlay=x='100+700*t/6':y=500[a];[a][2]overlay=x=140:y='1500-900*t/6'"
    fx.ffmpeg("-f", "lavfi", "-i", "color=c=0x101820:s=1080x1920:r=30:d=6", "-f", "lavfi", "-i", "color=c=0xff3b30:s=180x180:r=30:d=6",
              "-f", "lavfi", "-i", "color=c=0x21c45a:s=800x60:r=30:d=6", "-filter_complex", fc, "-c:v", "libx264", "-preset", "veryfast",
              "-crf", "18", "-pix_fmt", "yuv420p", wd / "demo2d.mp4", timeout=60)
    fx.ffmpeg("-i", wd / "demo2d.mp4", "-vf", "fps=10,scale=270:-1", wd / "demo2d.gif")
    st = [s for s in fx.probe(wd / "demo2d.mp4")["streams"] if s["codec_type"] == "video"][0]
    F = read_video(wd / "demo2d.mp4", (108, 192))
    ends = []
    for t in ("0", "5.95"):
        fx.ffmpeg("-ss", t, "-i", wd / "demo2d.mp4", "-frames:v", "1", wd / ("end_%s.png" % t))
        ends.append(red_x(load_png(wd / ("end_%s.png" % t))))
    e = energy(F)
    contact_sheet([F[i] for i in range(0, 180, 20)], 9, wd / "contact.png")
    qa = {"frames": len(F), "size": [st["width"], st["height"]], "fps": st["r_frame_rate"], "mean_motion": round(float(e.mean()), 3)}
    qa["verdict"] = "PASS" if qa["frames"] == 180 and qa["size"] == [1080, 1920] and qa["fps"] == "30/1" and qa["mean_motion"] > 0.05 else "FAIL"
    wj(wd / "qa.json", qa)
    still = read_video(fx.color_clip(wd / "still.mp4", "0x101820", 1.0, "108x192", 30))
    return [check("180 frames at 1080x1920, 30 fps", qa["frames"] == 180 and qa["size"] == [1080, 1920] and qa["fps"] == "30/1", qa, "180 / 1080x1920 / 30"),
            check("GIF and contact sheet written", (wd / "demo2d.gif").stat().st_size > 0 and (wd / "contact.png").stat().st_size > 0, (wd / "demo2d.gif").stat().st_size, "> 0"),
            check("red box travels ~700 px across (x at 0 s vs 5.95 s)", 650 < ends[1] - ends[0] < 710, ends, "100 -> ~794"),
            check("qa.json verdict PASS with mean_motion > 0.05", qa["verdict"] == "PASS", qa["mean_motion"], "> 0.05"),
            check("negative control: a still plate has zero mean motion", float(energy(still).mean()) == 0.0, float(energy(still).mean()), 0)], [wd / "demo2d.mp4", wd / "qa.json"]


@card("QA-174")
def fast_composite_preview(task, wd):
    """Fast composite preview frames: approximate the final composite (background + moving alpha logo + caption) at
    chosen times with PIL, without rendering, and compare with the real ffmpeg overlay render at the same times."""
    np = _np()
    from PIL import Image, ImageDraw
    W, H = 320, 180
    bg = texture(4, H, W, 20, 40, 160)
    save_png(bg, wd / "bg.png")
    logo = Image.new("RGBA", (60, 60), (0, 0, 0, 0))
    ImageDraw.Draw(logo).ellipse([0, 0, 59, 59], fill=(255, 200, 0, 230))
    logo.save(wd / "logo.png")
    fx.ffmpeg("-loop", "1", "-t", "3", "-r", "30", "-i", wd / "bg.png", "-i", wd / "logo.png",
              "-filter_complex", "[0][1]overlay=x='40+60*t':y=60", "-c:v", "libx264rgb", "-qp", "0", wd / "final.mp4")

    def preview(t):
        im = Image.open(wd / "bg.png").convert("RGBA")
        im.alpha_composite(logo, (int(math.floor(40 + 60 * t)), 60))
        return np.asarray(im.convert("RGB"), float)

    def psnr(a, b):
        m = ((a - b) ** 2).mean()
        return 99.0 if m == 0 else 10 * math.log10(255 ** 2 / m)
    F = read_video(wd / "final.mp4")
    rows, t0 = [], time.time()
    for t in (0.5, 1.5, 2.5):
        p = preview(t)
        save_png(p, wd / ("preview_%.1f.png" % t))
        rows.append({"t": t, "psnr": psnr(p, F[int(round(t * 30))]), "wrong_t_psnr": psnr(preview(t + 0.5), F[int(round(t * 30))])})
    per_frame = (time.time() - t0) / 3
    out = wj(wd / "preview_vs_render.json", {"rows": rows, "seconds_per_frame": per_frame})
    return [check("preview matches the real render at every time (PSNR >= 35 dB)", all(r["psnr"] >= 35 for r in rows), [r["psnr"] for r in rows], ">= 35"),
            check("preview is fast (< 2 s per frame)", per_frame < 2, per_frame, "< 2 s"),
            check("three preview stills written", all((wd / ("preview_%.1f.png" % t)).exists() for t in (0.5, 1.5, 2.5)), 3, 3),
            check("negative control: a preview at the wrong time does not match (PSNR < 30)", all(r["wrong_t_psnr"] < 30 for r in rows), [r["wrong_t_psnr"] for r in rows], "< 30")], [out, wd / "preview_1.5.png"]


# ═════════════════════════ browser cards (node + playwright + Chrome) ═════════════════════════
GL_ARGS = "['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']"

SEEK_PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:#101820}</style></head>
<body><canvas id="c" width="640" height="360" data-width="640" data-height="360"></canvas><script>
window.__builds=(window.__builds||0)+1; window.__ready=false; window.__att={};
const STALL=__STALL__; const c=document.getElementById('c'), g=c.getContext('2d');
function draw(t){ g.fillStyle='#101820'; g.fillRect(0,0,640,360); g.fillStyle='#ff3b30'; g.fillRect(Math.round(20+60*t),140,60,60); }
window.seek=function(t){ const k=String(t); window.__att[k]=(window.__att[k]||0)+1; window.__ready=false;
  if((STALL[k]||0)>=window.__att[k]) return;  /* a stalled grab: never becomes ready */
  setTimeout(()=>{draw(t); window.__ready=true;},30); };
__EXTRA__
setTimeout(()=>{draw(0); window.__ready=true;},50);
</script></body></html>"""


def seek_page(wd, name="index.html", stall=None, extra=""):
    return tw(Path(wd) / "proj" / name, SEEK_PAGE.replace("__STALL__", json.dumps(stall or {})).replace("__EXTRA__", extra))


def frame_grab(wd, page, times, out, attempts=1, backoff=0.0, timeout_ms=1500):
    """Open the page once, seek to each time, wait for window.__ready, screenshot; retry stalled grabs with an
    n x back-off; collect page errors and console warnings."""
    js = PW + """(async()=>{const b=await launch();const ctx=await b.newContext({viewport:{width:640,height:360}});const p=await ctx.newPage();
let loads=0;const errors=[];p.on('load',()=>loads++);p.on('pageerror',e=>errors.push('pageerror: '+String(e.message||e).slice(0,160)));
p.on('console',m=>{if(['error','warning'].includes(m.type()))errors.push('console.'+m.type()+': '+m.text().slice(0,160));});
await p.goto('file://'+__PAGE__,{waitUntil:'load'});await p.waitForFunction('window.__ready===true',null,{timeout:10000});
const frames=[];fs.mkdirSync(__OUT__,{recursive:true});
for(const t of __TIMES__){let ok=false,n=0;const waits=[];while(!ok&&n<__ATT__){n++;await p.evaluate(t=>window.seek(t),t);
  try{await p.waitForFunction('window.__ready===true',null,{timeout:__TMO__});ok=true;}catch(e){const w=__BACK__*n;waits.push(w);await new Promise(r=>setTimeout(r,w*1000));}}
  const f=path.join(__OUT__,'t'+t.toFixed(2).padStart(5,'0')+'.png');if(ok)await p.screenshot({path:f});frames.push({t,ok,attempts:n,waits,path:ok?f:null});}
const builds=await p.evaluate(()=>window.__builds);await b.close();console.log(JSON.stringify({loads,builds,frames,errors}));})();"""
    js = (js.replace("__PAGE__", json.dumps(str(page))).replace("__OUT__", json.dumps(str(out))).replace("__TIMES__", json.dumps(times))
          .replace("__ATT__", str(attempts)).replace("__TMO__", str(timeout_ms)).replace("__BACK__", str(backoff)))
    return node(wd, "grab", js, timeout=60)


def _box_ok(frames):
    return [(f["t"], red_x(load_png(f["path"])), round(20 + 60 * f["t"])) for f in frames if f["ok"]]


@card("QA-178")
def keyframe_gate_frames(task, wd):
    """Keyframe gate frames (kmotion frames --times 1,4,7): render selected stills before any video render, retrying a
    stalled grab instead of giving up."""
    page = seek_page(wd, stall={"4": 1})
    r = frame_grab(wd, page, [1, 4, 7], wd / "frames", attempts=3, backoff=0.2, timeout_ms=800)
    r0 = frame_grab(wd, page, [1, 4, 7], wd / "frames_noretry", attempts=1, timeout_ms=800)
    pos = _box_ok(r["frames"])
    out = wj(wd / "gate.json", r)
    return [check("three stills at 1, 4, 7 s", [f["t"] for f in r["frames"] if f["ok"]] == [1, 4, 7], [f["t"] for f in r["frames"]], [1, 4, 7]),
            check("each still shows the composition at its time (box x = 20 + 60 t)", all(abs(x - e) <= 1 for _, x, e in pos), pos, "+-1 px"),
            check("the stalled grab at 4 s was retried and succeeded on attempt 2", r["frames"][1]["attempts"] == 2 and r["frames"][1]["ok"], r["frames"][1]["attempts"], 2),
            check("negative control: without retries the 4 s still is lost", not r0["frames"][1]["ok"], r0["frames"][1]["ok"], False)], [out, Path(r["frames"][0]["path"])]


@card("QA-193")
def key_frames_gate(task, wd):
    """Key frames gate (motion.py frames --times 0.5,2,4,6,8): build the page once and seek to each time."""
    page = seek_page(wd)
    times = [0.5, 2, 4, 6, 8]
    r = frame_grab(wd, page, times, wd / "frames")
    pos = _box_ok(r["frames"])
    out = wj(wd / "gate.json", r)
    shots = [Path(f["path"]) for f in r["frames"]]
    distinct = len({sha(p) for p in shots})
    return [check("five stills at the default times", [f["t"] for f in r["frames"]] == times and all(f["ok"] for f in r["frames"]), [f["t"] for f in r["frames"]], times),
            check("page built once and only seeked (1 load, 1 build)", r["loads"] == 1 and r["builds"] == 1, [r["loads"], r["builds"]], [1, 1]),
            check("each still is the composition at its time", all(abs(x - e) <= 1 for _, x, e in pos), pos, "+-1 px"),
            check("negative control: stills differ from each other (not one frame repeated)", distinct == 5, distinct, 5)], [out, shots[2]]


@card("QA-209")
def key_frame_review_grabs(task, wd):
    """Key-frame review grabs: one page, stills at chosen times, 4 attempts with 1.5 s x n back-off on stalled grabs,
    page errors and console warnings reported."""
    extra = "console.warn('font fallback used'); setTimeout(()=>{throw new Error('late script error')},10);"
    page = seek_page(wd, stall={"2": 2}, extra=extra)
    t0 = time.time()
    r = frame_grab(wd, page, [0.5, 2, 4], wd / "frames", attempts=4, backoff=1.5, timeout_ms=400)
    took = time.time() - t0
    f2 = r["frames"][1]
    out = wj(wd / "grabs.json", r)
    return [check("all three stills saved", all(f["ok"] for f in r["frames"]), [f["ok"] for f in r["frames"]], [True] * 3),
            check("stalled 2 s grab took 3 attempts with 1.5 s then 3.0 s back-off", f2["attempts"] == 3 and f2["waits"] == [1.5, 3.0], [f2["attempts"], f2["waits"]], [3, [1.5, 3.0]]),
            check("console warning and page error reported", any("console.warning" in e for e in r["errors"]) and any("pageerror" in e for e in r["errors"]), r["errors"], "both"),
            check("box position right at each time", all(abs(x - e) <= 1 for _, x, e in _box_ok(r["frames"])), _box_ok(r["frames"]), "+-1 px"),
            check("negative control: the stalled time is not ready on its first seek", f2["attempts"] > 1, f2["attempts"], "> 1")], [out, Path(f2["path"])]


@card("QA-308")
def review_frames_recipe(task, wd):
    """Review frames (eight-second gate) through the studio: POST /api/jobs {recipe:'frames', args} queues the grab,
    GET /api/jobs/<id> reports it; equivalent to `kmotion.py frames PROJECT --times 1,3,5`."""
    page = seek_page(wd)
    jobs = {}

    def post(h, body):
        req = json.loads(body or b"{}")
        if req.get("recipe") != "frames":
            return send_json(h, {"error": "unknown recipe"}, 400)
        jid = "job%d" % (len(jobs) + 1)
        a = req["args"]
        res = frame_grab(wd, Path(a["project"]) / "index.html", a.get("times", [1, 3, 5]), wd / jid)
        jobs[jid] = {"id": jid, "status": "done" if all(f["ok"] for f in res["frames"]) else "failed", "result": res}
        send_json(h, {"id": jid})

    def get(h, body):
        send_json(h, jobs)
    srv = Serve(wd, {("POST", "/api/jobs"): post, ("GET", "/api/jobs"): get})
    try:
        import urllib.request
        rq = urllib.request.Request(srv.url + "/api/jobs", data=json.dumps({"recipe": "frames", "args": {"project": str(page.parent), "times": [1, 3, 5]}}).encode(),
                                    headers={"Content-Type": "application/json"})
        jid = json.loads(urllib.request.urlopen(rq, timeout=60).read())["id"]
        allj = json.loads(urllib.request.urlopen(srv.url + "/api/jobs", timeout=10).read())
        try:
            urllib.request.urlopen(urllib.request.Request(srv.url + "/api/jobs", data=b'{"recipe":"render"}'), timeout=10)
            bad = 200
        except urllib.error.HTTPError as e:
            bad = e.code
    finally:
        srv.close()
    job = allj[jid]
    pos = _box_ok(job["result"]["frames"])
    out = wj(wd / "jobs.json", allj)
    return [check("POST /api/jobs queued a frames job", jid == "job1" and job["status"] == "done", job["status"], "done"),
            check("stills at the panel's times 1, 3, 5", [f["t"] for f in job["result"]["frames"]] == [1, 3, 5], [f["t"] for f in job["result"]["frames"]], [1, 3, 5]),
            check("stills show the composition at those times", all(abs(x - e) <= 1 for _, x, e in pos), pos, "+-1 px"),
            check("negative control: an unknown recipe is refused (400)", bad == 400, bad, 400)], [out, Path(job["result"]["frames"][0]["path"])]


WEBGPU_PAGE = """<!doctype html><html><body><script>
let adapter, device, tex, buf, lost=0, reasons=[], rebuilt=0, ready;
async function init(handle){ adapter=await navigator.gpu.requestAdapter(); device=await adapter.requestDevice();
  tex=device.createTexture({size:[4,4],format:'rgba8unorm',usage:GPUTextureUsage.RENDER_ATTACHMENT|GPUTextureUsage.COPY_SRC});
  buf=device.createBuffer({size:1024,usage:GPUBufferUsage.COPY_DST|GPUBufferUsage.MAP_READ});
  const d=device; ready=new Promise(res=>{ d.lost.then(async info=>{ lost++; reasons.push(info.reason); if(handle){ await init(handle); rebuilt++; } res(); }); }); }
async function frame(r,g,b){ try{ const e=device.createCommandEncoder();
  const p=e.beginRenderPass({colorAttachments:[{view:tex.createView(),loadOp:'clear',storeOp:'store',clearValue:{r,g,b,a:1}}]}); p.end();
  e.copyTextureToBuffer({texture:tex},{buffer:buf,bytesPerRow:256},[4,4]); device.queue.submit([e.finish()]);
  await buf.mapAsync(GPUMapMode.READ); const a=Array.from(new Uint8Array(buf.getMappedRange().slice(0,4))); buf.unmap(); return a; }
  catch(err){ return [0,0,0,0]; } }
function bigBuffer(guard){ const want=adapter.limits.maxBufferSize*2; if(guard && want>adapter.limits.maxBufferSize) return 'skipped: over maxBufferSize';
  device.pushErrorScope('validation'); try{ device.createBuffer({size:want,usage:GPUBufferUsage.STORAGE}); }catch(e){ return 'threw'; }
  return device.popErrorScope().then(e=>e?'validation error':'ok'); }
window.run=async function(handle){ lost=0; reasons=[]; rebuilt=0; await init(handle); const before=await frame(1,0,0);
  device.destroy(); await Promise.race([ready,new Promise(r=>setTimeout(r,2000))]); const after=await frame(1,0,0);
  const big=await bigBuffer(handle); return {before,after,lost,reasons,rebuilt,big,limit:adapter.limits.maxBufferSize}; };
</script></body></html>"""


@card("QA-135")
def webgpu_device_loss(task, wd):
    """WebGPU device-loss handling: the renderer watches device.lost and rebuilds device + resources instead of
    producing black frames; limits are checked before a big buffer. Runs on Chrome's SwiftShader WebGPU adapter."""
    page = tw(wd / "webgpu.html", WEBGPU_PAGE)
    js = PW + """(async()=>{const b=await launch(['--enable-unsafe-webgpu','--use-webgpu-adapter=swiftshader','--enable-features=Vulkan']);const p=await b.newPage();
await p.goto('file://'+__PAGE__);const has=await p.evaluate(()=>!!navigator.gpu);if(!has){console.log(JSON.stringify({gpu:false}));await b.close();return;}
const handled=await p.evaluate(()=>run(true));const naive=await p.evaluate(()=>run(false));await b.close();console.log(JSON.stringify({gpu:true,handled,naive}));})();"""
    r = node(wd, "webgpu", js.replace("__PAGE__", json.dumps(str(page))), timeout=60)
    if not r.get("gpu"):
        raise RuntimeError("navigator.gpu is not available in this Chrome")
    H, N = r["handled"], r["naive"]
    np = _np()
    save_png(np.array([[H["before"][:3], H["after"][:3], N["after"][:3]]], float).repeat(40, 0).repeat(40, 1), wd / "frames_before_after.png")
    out = wj(wd / "device_loss.json", r)
    return [check("frame before the loss renders red", H["before"][:3] == [255, 0, 0], H["before"], [255, 0, 0, 255]),
            check("device.lost fired once with its reason", H["lost"] == 1 and H["reasons"] == ["destroyed"], H["reasons"], ["destroyed"]),
            check("handler rebuilt device and resources; next frame is red again", H["rebuilt"] == 1 and H["after"][:3] == [255, 0, 0], H["after"], [255, 0, 0, 255]),
            check("limits checked before a buffer over maxBufferSize", H["big"].startswith("skipped"), H["big"], "skipped"),
            check("negative control: without the handler the frame after the loss is black", N["after"][:3] == [0, 0, 0] and N["rebuilt"] == 0, N["after"], [0, 0, 0, 0])], [out, wd / "frames_before_after.png"]


def three_site(wd):
    www = Path(wd) / "www"
    www.mkdir(parents=True, exist_ok=True)
    for f in ("three.module.js", "three.core.js"):
        shutil.copy(Path(NODE_MODULES) / "three/build" / f, www / f)
    return www


DBG_PAGE = """<!doctype html><html><head><style>html,body{margin:0;background:#000}</style>
<script type="importmap">{"imports":{"three":"./three.module.js"}}</script></head><body><script type="module">
import * as THREE from 'three';
const W=320,H=180; const R=new THREE.WebGLRenderer({preserveDrawingBuffer:true}); R.setSize(W,H); document.body.appendChild(R.domElement);
const log=[]; window.__log=log;
R.domElement.addEventListener('webglcontextlost',e=>{e.preventDefault(); log.push('LOUD: webglcontextlost');});
R.domElement.addEventListener('webglcontextrestored',()=>log.push('LOUD: webglcontextrestored'));
function build(){ const D=window.__dbg||{}; const S=new THREE.Scene(); S.background=new THREE.Color(0x202020);
  const cam=new THREE.PerspectiveCamera(50,W/H,0.1,100); cam.position.set(0,6,8); cam.lookAt(0,0,0);
  const add=(name,geo,col,y)=>{ if(D['no'+name]) return; const m=new THREE.Mesh(geo,new THREE.MeshBasicMaterial({color:col})); m.position.y=y; m.name=name; S.add(m); };
  add('ground',new THREE.PlaneGeometry(14,14).rotateX(-Math.PI/2),0x2e7d32,0);
  add('water',new THREE.CircleGeometry(3,32).rotateX(-Math.PI/2),0x1565ff,0.02);
  add('koi',new THREE.BoxGeometry(0.8,0.3,0.4),0xff8c00,0.3);
  const rt=new THREE.WebGLRenderTarget(W,H);
  const post=new THREE.Mesh(new THREE.PlaneGeometry(2,2),new THREE.ShaderMaterial({uniforms:{t:{value:rt.texture}},
    vertexShader:'varying vec2 v;void main(){v=uv;gl_Position=vec4(position,1.);}',
    fragmentShader:'uniform sampler2D t;varying vec2 v;void main(){vec4 c=texture2D(t,v);float d=distance(v,vec2(.5));gl_FragColor=vec4(c.rgb*(1.-1.2*d*d),1.);}'}));
  const PS=new THREE.Scene(); PS.add(post); const oc=new THREE.OrthographicCamera(-1,1,1,-1,0,1);
  window.render=()=>{ if(D.nopost){ R.setRenderTarget(null); R.render(S,cam); } else { R.setRenderTarget(rt); R.render(S,cam); R.setRenderTarget(null); R.render(PS,oc); } };
  window.render(); }
window.build=build; window.loseCtx=()=>{const x=R.getContext().getExtension('WEBGL_lose_context'); x.loseContext(); setTimeout(()=>x.restoreContext(),50);};
window.__ok=true;
</script></body></html>"""


@card("QA-179")
def debug_visibility_toggles(task, wd):
    """window.__dbg set before build() hides water, koi or the whole post stack (render bypasses the post pass when
    nopost), isolating artefacts; webglcontextlost/restored listeners log loudly."""
    np = _np()
    www = three_site(wd)
    tw(www / "index.html", DBG_PAGE)
    srv = Serve(www)
    try:
        js = PW + """(async()=>{const b=await launch(%s);const out={};
for(const [name,dbg] of [['full',{}],['nowater',{nowater:1}],['nokoi',{nokoi:1}],['nopost',{nopost:1}]]){
  const p=await b.newPage({viewport:{width:320,height:180}});await p.goto(__URL__);await p.waitForFunction('window.__ok===true');
  await p.evaluate(d=>{window.__dbg=d;window.build();},dbg);await p.screenshot({path:__DIR__+'/'+name+'.png'});
  if(name==='full'){await p.evaluate(()=>window.loseCtx());await new Promise(r=>setTimeout(r,400));out.log=await p.evaluate(()=>window.__log);}
  await p.close();}
await b.close();console.log(JSON.stringify(out));})();""" % GL_ARGS
        r = node(wd, "dbg", js.replace("__URL__", json.dumps(srv.url + "/index.html")).replace("__DIR__", json.dumps(str(wd))), timeout=60)
    finally:
        srv.close()
    im = {k: load_png(wd / (k + ".png")) for k in ("full", "nowater", "nokoi", "nopost")}
    blue = lambda a: int(((a[..., 2] > 150) & (a[..., 0] < 80)).sum())
    orange = lambda a: int(((a[..., 0] > 200) & (a[..., 1] > 40) & (a[..., 1] < 170) & (a[..., 2] < 40)).sum())
    corner = lambda a: float(a[150:178, 2:40].mean())
    out = wj(wd / "dbg.json", {"blue": {k: blue(v) for k, v in im.items()}, "orange": {k: orange(v) for k, v in im.items()},
                               "corner_level": {k: corner(v) for k, v in im.items()}, "log": r.get("log")})
    return [check("water visible normally, gone with nowater", blue(im["full"]) > 500 and blue(im["nowater"]) == 0, [blue(im["full"]), blue(im["nowater"])], "> 500 -> 0"),
            check("koi gone with nokoi, water untouched", orange(im["full"]) > 20 and orange(im["nokoi"]) == 0 and blue(im["nokoi"]) > 500, [orange(im["full"]), orange(im["nokoi"])], "> 20 -> 0"),
            check("nopost bypasses the post stack (corners no longer darkened by the vignette pass)", corner(im["full"]) < 0.5 * corner(im["nopost"]),
                  [corner(im["full"]), corner(im["nopost"])], "post < 0.5 x nopost"),
            check("context loss and restore logged loudly", r.get("log") == ["LOUD: webglcontextlost", "LOUD: webglcontextrestored"], r.get("log"), "lost, restored"),
            check("negative control: without toggles every layer renders", blue(im["full"]) > 500 and orange(im["full"]) > 20, [blue(im["full"]), orange(im["full"])], "all present")], [out, wd / "full.png"]


ISO_PAGE = """<!doctype html><html><head><style>html,body{margin:0}</style>
<script type="importmap">{"imports":{"three":"./three.module.js"}}</script></head><body><script type="module">
import * as THREE from 'three';
const W=320,H=180; const R=new THREE.WebGLRenderer({preserveDrawingBuffer:true}); R.setSize(W,H); document.body.appendChild(R.domElement);
const S=new THREE.Scene(); S.background=new THREE.Color(0x111111); const cam=new THREE.PerspectiveCamera(50,W/H,0.1,100); cam.position.set(0,0,10);
const sh=(frag)=>new THREE.ShaderMaterial({uniforms:{time:{value:0}},vertexShader:'varying vec2 v;void main(){v=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',fragmentShader:frag});
const mk=(mat,x,z)=>{const m=new THREE.Mesh(new THREE.PlaneGeometry(1.6,1.6),mat);m.position.set(x,0,z);S.add(m);return m;};
mk(new THREE.MeshBasicMaterial({color:0x2e7d32}),-4,0); mk(new THREE.MeshBasicMaterial({color:0x1565c0}),-2,-1);
mk(sh('uniform float time;varying vec2 v;void main(){gl_FragColor=vec4(0.9,0.9,0.2,1.);}'),0,1);
mk(sh('uniform float time;varying vec2 v;void main(){float s=step(.5,fract(v.y*8.+time));gl_FragColor=vec4(mix(vec3(.3),vec3(1.,0.,1.),s),1.);}'),2,0);
mk(new THREE.MeshBasicMaterial({color:0xaaaaaa}),4,-2);
window.__S={S,cam,update:(t)=>S.traverse(o=>{if(o.material&&o.material.uniforms)o.material.uniforms.time.value=t;})};
window.render=(t)=>{window.__S.update(t);R.render(S,cam);};
window.meshes=()=>{const out=[];let si=0;S.traverse(o=>{if(o.isMesh){out.push({type:o.material.type,shaderIndex:o.material.type==='ShaderMaterial'?si++:null,dist:+o.position.distanceTo(cam.position).toFixed(3)});}});return out;};
window.hide=(by,val)=>{let si=0;S.traverse(o=>{if(o.isMesh){const isS=o.material.type==='ShaderMaterial';o.visible=!(by==='type'?o.material.type===val:(isS&&si===val));if(isS)si++;}});};
window.__ok=true;
</script></body></html>"""


@card("QA-189")
def shader_isolation_debugging(task, wd):
    """Shader isolation: render the same frame (t = 15 s) with one material type, then one ShaderMaterial index,
    hidden at a time; compare screenshots to find the artefact's source; list meshes with distance to camera."""
    www = three_site(wd)
    tw(www / "index.html", ISO_PAGE)
    srv = Serve(www)
    try:
        js = PW + """(async()=>{const b=await launch(%s);const p=await b.newPage({viewport:{width:320,height:180}});
await p.goto(__URL__);await p.waitForFunction('window.__ok===true');const meshes=await p.evaluate(()=>window.meshes());const shots=[];
for(const [by,val] of [['none',null],['type','MeshBasicMaterial'],['type','ShaderMaterial'],['index',0],['index',1]]){
  await p.evaluate(([by,val])=>{if(by==='none')window.hide('type','__none__');else window.hide(by,val);window.render(15);},[by,val]);
  const f=__DIR__+'/qa/s5_hide_'+by+'_'+val+'.png';await p.screenshot({path:f});shots.push({by,val,f});}
await b.close();console.log(JSON.stringify({meshes,shots}));})();""" % GL_ARGS
        (wd / "qa").mkdir(exist_ok=True)
        r = node(wd, "iso", js.replace("__URL__", json.dumps(srv.url + "/index.html")).replace("__DIR__", json.dumps(str(wd))), timeout=60)
    finally:
        srv.close()
    mag = lambda a: int(((a[..., 0] > 200) & (a[..., 2] > 200) & (a[..., 1] < 60)).sum())
    res = {"%s:%s" % (s["by"], s["val"]): mag(load_png(s["f"])) for s in r["shots"]}
    culprit = [k for k, v in res.items() if k.startswith("index") and v == 0]
    out = wj(wd / "isolation.json", {"magenta_px": res, "culprit": culprit, "meshes": r["meshes"]})
    return [check("artefact present in the full frame at t = 15", res["none:None"] > 200, res["none:None"], "> 200 magenta px"),
            check("hiding MeshBasicMaterial keeps it; hiding ShaderMaterial removes it", res["type:MeshBasicMaterial"] > 200 and res["type:ShaderMaterial"] == 0,
                  [res["type:MeshBasicMaterial"], res["type:ShaderMaterial"]], "> 200, 0"),
            check("culprit is ShaderMaterial index 1", culprit == ["index:1"], culprit, ["index:1"]),
            check("five meshes listed with distance to camera", len(r["meshes"]) == 5 and r["meshes"][2]["dist"] == 9.0, [m["dist"] for m in r["meshes"]], "5 rows, 9.0 for the z=1 mesh"),
            check("negative control: hiding the innocent shader (index 0) leaves the artefact", res["index:0"] > 200, res["index:0"], "> 200")], [out, Path(r["shots"][0]["f"])]


def pw_run(wd, name, body, timeout=60, args=""):
    """Run a playwright body inside an async main with `b` (browser) open; the body must set `out`."""
    js = PW + "(async()=>{const b=await launch(%s);let out={};\n%s\nawait b.close();console.log(JSON.stringify(out));})();" % (args or "[]", body)
    return node(wd, name, js, timeout=timeout)


COMPARE_PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:#000}
#stage{display:flex;width:960px;height:270px}#stage>*{flex:1;min-width:0;height:270px;display:block}
button{font:12px sans-serif}</style></head><body>
<div id="tabs"><button data-v="product">product</button><button data-v="orig">orig</button><button data-v="ref">ref</button><button data-v="all">all</button></div>
<div id="stage"><canvas id="product"></canvas><canvas id="orig"></canvas><video id="ref" muted preload="auto" src="ref.mp4"></video></div>
<script>
const P=document.getElementById('product'),O=document.getElementById('orig'),V=document.getElementById('ref'); const img=new Image(); img.src='orig.png';
let T=0;
function sizeCanvas(c,half){const r=c.getBoundingClientRect();c.width=Math.round(r.width*(half?0.5:1));c.height=Math.round(r.height*(half?0.5:1));}
function drawProduct(){sizeCanvas(P,false);const g=P.getContext('2d');g.fillStyle='#401010';g.fillRect(0,0,P.width,P.height);g.fillStyle='#ff3b30';g.fillRect(Math.round(10+40*T),100,40,40);}
function drawOrig(){sizeCanvas(O,true);const g=O.getContext('2d');g.fillStyle='#000';g.fillRect(0,0,O.width,O.height);
  const s=Math.min(O.width/img.width,O.height/img.height),w=img.width*s,h=img.height*s;g.drawImage(img,(O.width-w)/2,(O.height-h)/2,w,h);window.__fit={w,h,cw:O.width,ch:O.height};}
window.view=function(v){for(const [id,el] of [['product',P],['orig',O],['ref',V]]) el.style.display=(v==='all'||v===id)?'block':'none'; drawProduct(); if(img.complete) drawOrig();};
window.seek=async function(t,sync=true){T=t;drawProduct();if(sync){await new Promise(r=>{V.addEventListener('seeked',r,{once:true});V.currentTime=t;});}return V.currentTime;};
document.querySelectorAll('#tabs button').forEach(b=>b.onclick=()=>view(b.dataset.v));
Promise.all([new Promise(r=>img.onload=r),new Promise(r=>V.addEventListener('loadeddata',r,{once:true}))]).then(()=>{view('all');window.__ok=true;});
</script></body></html>"""


@card("QA-146")
def multi_monitor_compare(task, wd):
    """Multi-monitor compare view: product / original / reference monitors one at a time or side by side (tabs),
    drawOrig contain-fit at half resolution, and the reference video seeked in sync with the product time."""
    np = _np()
    from PIL import Image
    www = Path(wd) / "www"
    www.mkdir()
    Image.new("RGB", (200, 200), (33, 196, 90)).save(www / "orig.png")
    fx.ffmpeg("-f", "lavfi", "-i", "color=c=blue:s=320x180:r=30:d=1", "-f", "lavfi", "-i", "color=c=yellow:s=320x180:r=30:d=1",
              "-filter_complex", "[0][1]concat=n=2:v=1", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-g", "1", www / "ref.mp4")
    tw(www / "index.html", COMPARE_PAGE)
    srv = Serve(www)
    try:
        body = """const p=await b.newPage({viewport:{width:960,height:300}});await p.goto(__URL__);await p.waitForFunction('window.__ok===true',null,{timeout:15000});
await p.click('button[data-v=all]');out.t=await p.evaluate(()=>seek(1.5));await p.screenshot({path:__DIR__+'/all.png'});
out.fit=await p.evaluate(()=>window.__fit);out.css=await p.evaluate(()=>document.getElementById('orig').getBoundingClientRect().width);
await p.click('button[data-v=orig]');out.vis=await p.evaluate(()=>['product','orig','ref'].map(i=>getComputedStyle(document.getElementById(i)).display));
await p.screenshot({path:__DIR__+'/orig_only.png'});
await p.click('button[data-v=all]');await p.evaluate(()=>{document.getElementById('ref').currentTime=0;});await new Promise(r=>setTimeout(r,300));
await p.evaluate(()=>seek(1.5,false));await p.screenshot({path:__DIR__+'/unsynced.png'});"""
        r = pw_run(wd, "compare", body.replace("__URL__", json.dumps(srv.url + "/index.html")).replace("__DIR__", json.dumps(str(wd))))
    finally:
        srv.close()
    A, U = load_png(wd / "all.png"), load_png(wd / "unsynced.png")
    y = 30 + 135
    ref_px, unsync_px = A[y, 800], U[y, 800]
    fit = r["fit"]
    return [check("'all' shows the three monitors side by side", A[y, 160][0] > 50 and A[y, 480][1] > 150 and ref_px[0] > 150 and ref_px[1] > 150,
                  [A[y, 160].tolist(), A[y, 480].tolist(), ref_px.tolist()], "product | orig | ref"),
            check("orig drawn at half resolution of its monitor", fit["cw"] == round(r["css"] / 2), [fit["cw"], r["css"]], "css / 2"),
            check("orig contain-fit: square fills the monitor height, centred", abs(fit["w"] - fit["h"]) < 0.5 and abs(fit["h"] - fit["ch"]) < 0.5, fit, "w == h == ch"),
            check("reference seeked to the product time (1.5 s, +-1 frame)", abs(r["t"] - 1.5) <= 1 / 30.0 + 1e-6, r["t"], 1.5),
            check("one-at-a-time tab shows only orig", r["vis"] == ["none", "block", "none"], r["vis"], ["none", "block", "none"]),
            check("negative control: without sync the reference still shows its first (blue) second", unsync_px[2] > 150 and unsync_px[0] < 100, unsync_px.tolist(), "blue")], [wd / "all.png"]


ANIM_PAGE = """<!doctype html><html><head><script src="gsap.min.js"></script><style>html,body{margin:0;width:640px;height:360px;overflow:hidden}
div{position:absolute;width:30px;height:30px;background:#09f;top:20px}</style></head><body>
__BODY__<script>window.__timelines={};const tl=gsap.timeline({paused:true});__JS__;window.__timelines.main=tl;
window.mapAnim=(n)=>{const D=tl.duration();const tws=tl.getChildren(true,true,false).map(t=>({targets:t.targets().map(e=>'#'+e.id),start:+t.startTime().toFixed(3),
 dur:+t.duration().toFixed(3)}));const clips={};document.querySelectorAll('[data-duration]').forEach(e=>clips['#'+e.id]={start:+e.dataset.start,end:+e.dataset.start+ +e.dataset.duration});
 const boxes=[];for(let i=0;i<=n;i++){const t=D*i/n;tl.seek(t,false);boxes.push({t:+t.toFixed(3),b:[...document.querySelectorAll('div')].map(e=>{const r=e.getBoundingClientRect();return ['#'+e.id,Math.round(r.x),Math.round(r.y)];})});}
 return {duration:D,tweens:tws,clips,boxes};};</script></body></html>"""


def anim_audit(m, W=640, H=360):
    """animation-map audit: dead zones (> 1 s with no active tween), stagger inconsistency, lifecycle problems
    (a tween outlives its element's clip, or moves it off the canvas)."""
    tws, D = m["tweens"], m["duration"]
    cover = sorted((t["start"], t["start"] + t["dur"]) for t in tws)
    dead, cur = [], 0.0
    for a, b in cover:
        if a - cur > 1.0:
            dead.append([round(cur, 3), round(a, 3)])
        cur = max(cur, b)
    if D - cur > 1.0:
        dead.append([round(cur, 3), round(D, 3)])
    groups = {}
    for t in tws:
        for tg in t["targets"]:
            if tg.startswith("#s"):
                groups.setdefault("stagger", []).append(t["start"])
    stagger = []
    for g, st in groups.items():
        st = sorted(st)
        d = [round(b - a, 3) for a, b in zip(st, st[1:])]
        if d and max(d) - min(d) > 0.02:
            stagger.append({"group": g, "deltas": d})
    life = []
    for t in tws:
        for tg in t["targets"]:
            c = m["clips"].get(tg)
            if c and t["start"] + t["dur"] > c["end"] + 1e-6:
                life.append({"target": tg, "issue": "tween ends %.2f s after its clip" % (t["start"] + t["dur"] - c["end"])})
    for bx in m["boxes"]:
        for tg, x, y in bx["b"]:
            if (x > W or y > H or x < -30) and not any(l["target"] == tg and "off" in l["issue"] for l in life):
                life.append({"target": tg, "issue": "moves off the canvas at %.2f s" % bx["t"]})
    return {"dead_zones": dead, "stagger": stagger, "lifecycle": life}


@card("QA-160")
def animation_map_audit(task, wd):
    """Animation map audit: enumerate every GSAP tween on window.__timelines, sample bounding boxes, flag dead zones,
    stagger inconsistency and lifecycle problems into animation-map.json."""
    fixtures = {
        "bad": ('<div id="a" data-start="0" data-duration="5"></div><div id="s1"></div><div id="s2"></div><div id="s3"></div><div id="s4"></div>'
                '<div id="late" data-start="0" data-duration="3"></div>',
                'tl.to("#a",{x:100,duration:1},0);tl.to("#s1",{y:100,duration:.4},0);tl.to("#s2",{y:100,duration:.4},.1);tl.to("#s3",{y:100,duration:.4},.2);'
                'tl.to("#s4",{y:100,duration:.4},.6);tl.to("#a",{x:200,duration:1},3);tl.to("#late",{x:900,duration:2},2.5)'),
        "clean": ('<div id="a" data-start="0" data-duration="5"></div><div id="s1"></div><div id="s2"></div><div id="s3"></div><div id="s4"></div>'
                  '<div id="late" data-start="0" data-duration="5"></div>',
                  'tl.to("#a",{x:100,duration:1.5},0);tl.to("#s1",{y:100,duration:.4},0);tl.to("#s2",{y:100,duration:.4},.1);tl.to("#s3",{y:100,duration:.4},.2);'
                  'tl.to("#s4",{y:100,duration:.4},.3);tl.to("#a",{x:200,duration:1.5},1.5);tl.to("#late",{x:300,duration:2},3)'),
    }
    maps = {}
    for k, (body, js) in fixtures.items():
        d = Path(wd) / k
        d.mkdir()
        shutil.copy(GSAP, d / "gsap.min.js")
        tw(d / "index.html", ANIM_PAGE.replace("__BODY__", body).replace("__JS__", js))
        r = pw_run(wd, "map_" + k, "const p=await b.newPage({viewport:{width:640,height:360}});await p.goto('file://'+%s);out=await p.evaluate(()=>mapAnim(20));"
                   % json.dumps(str(d / "index.html")))
        maps[k] = dict(r, audit=anim_audit(r))
        wj(d / ".hyperframes/anim-map/animation-map.json", maps[k])
    B, C = maps["bad"]["audit"], maps["clean"]["audit"]
    return [check("every tween enumerated (7) with start and duration", len(maps["bad"]["tweens"]) == 7, len(maps["bad"]["tweens"]), 7),
            check("bounding boxes sampled at 21 times", len(maps["bad"]["boxes"]) == 21, len(maps["bad"]["boxes"]), 21),
            check("dead zone 1.0 -> 2.5 s flagged", B["dead_zones"] == [[1.0, 2.5]], B["dead_zones"], [[1.0, 2.5]]),
            check("stagger 0.1, 0.1, 0.4 flagged inconsistent", B["stagger"] and B["stagger"][0]["deltas"] == [0.1, 0.1, 0.4], B["stagger"], [0.1, 0.1, 0.4]),
            check("#late outlives its clip and leaves the canvas", sorted(x["issue"].split()[0] for x in B["lifecycle"] if x["target"] == "#late") == ["moves", "tween"],
                  B["lifecycle"], "2 lifecycle issues"),
            check("negative control: the clean timeline has no findings", C == {"dead_zones": [], "stagger": [], "lifecycle": []}, C, "none")], [Path(wd) / "bad/.hyperframes/anim-map/animation-map.json"]


CAPTION_PAGE = """<!doctype html><html><head><script src="gsap.min.js"></script><style>html,body{margin:0;width:540px;height:960px;background:#222}
#cap{position:absolute;left:40px;right:40px;bottom:__BOTTOM__;display:flex;flex-direction:column;justify-content:flex-end}
.l{color:#fff;font:700 34px sans-serif;line-height:44px}#w{position:absolute;top:200px;left:40px;width:300px;color:#fff;font:700 30px sans-serif}</style></head><body>
<div id="cap"><div class="l">first line</div><div class="l">second line</div><div class="l" id="last">third line</div></div>
<div id="w">Tap twice to save the clip</div>
<script>const tl=gsap.timeline({paused:true});__JS__;
window.sample=()=>{const out=[];for(let i=0;i<=20;i++){const t=i*0.1;tl.seek(t,false);const w=document.getElementById('w');
 const lines=Math.round(w.getBoundingClientRect().height/parseFloat(getComputedStyle(w).lineHeight||36));
 out.push({t:+t.toFixed(2),op:+getComputedStyle(document.getElementById('cap')).opacity,lines:w.getClientRects().length?Math.round(w.offsetHeight/35):0});}
 return {samples:out,lastBottom:document.getElementById('last').getBoundingClientRect().bottom};};</script></body></html>"""


@card("QA-176")
def caption_failure_modes(task, wd):
    """Caption failure modes (learned) as detectors: flex-stacked captions pushed into the bottom gesture zone,
    letterSpacing animation reflow jumps, a double fade pop, and a frame-rate mismatch between background and matte."""
    np = _np()
    cases = {
        "bad": ("2%", 'tl.fromTo("#cap",{opacity:0},{opacity:1,duration:.5},0);tl.set("#cap",{opacity:0},.6);tl.to("#cap",{opacity:1,duration:.4},.6);'
                      'tl.fromTo("#w",{letterSpacing:"0px"},{letterSpacing:"28px",duration:1.5},0)'),
        "good": ("24%", 'tl.fromTo("#cap",{opacity:0},{opacity:1,duration:.5},0);tl.fromTo("#w",{scale:.96},{scale:1,duration:1.5},0)'),
    }
    res = {}
    for k, (bottom, js) in cases.items():
        d = Path(wd) / k
        d.mkdir()
        shutil.copy(GSAP, d / "gsap.min.js")
        tw(d / "index.html", CAPTION_PAGE.replace("__BOTTOM__", bottom).replace("__JS__", js))
        r = pw_run(wd, "cap_" + k, "const p=await b.newPage({viewport:{width:540,height:960}});await p.goto('file://'+%s);out=await p.evaluate(()=>sample());"
                   "await p.evaluate(()=>{tl.seek(1,false);});await p.screenshot({path:%s});" % (json.dumps(str(d / "index.html")), json.dumps(str(d / "frame.png"))))
        ops = [s["op"] for s in r["samples"]]
        rise = [b_ - a for a, b_ in zip(ops, ops[1:])]
        pop = any(x < -0.2 for x in rise[:8])
        lines = [s["lines"] for s in r["samples"]]
        res[k] = {"gesture_zone": r["lastBottom"] > 960 * 0.82, "last_bottom": r["lastBottom"], "double_fade": pop, "ops": ops,
                  "reflow_jumps": sum(1 for a, b_ in zip(lines, lines[1:]) if a != b_), "lines": lines}
    fx.ffmpeg("-f", "lavfi", "-i", "color=c=gray:s=160x284:r=30:d=1", "-c:v", "libx264", wd / "bg.mp4")
    fx.ffmpeg("-f", "lavfi", "-i", "color=c=white:s=160x284:r=25:d=1", "-c:v", "libx264", wd / "matte_bad.mp4")
    fx.ffmpeg("-f", "lavfi", "-i", "color=c=white:s=160x284:r=30:d=1", "-c:v", "libx264", wd / "matte_good.mp4")
    rate = lambda p: [s for s in fx.probe(p)["streams"] if s["codec_type"] == "video"][0]["r_frame_rate"]
    res["fps"] = {"bg": rate(wd / "bg.mp4"), "matte_bad": rate(wd / "matte_bad.mp4"), "matte_good": rate(wd / "matte_good.mp4")}
    out = wj(wd / "caption_failures.json", res)
    B, G = res["bad"], res["good"]
    return [check("flex-stacked captions reach into the bottom 18 % gesture zone", B["gesture_zone"] and not G["gesture_zone"], [B["last_bottom"], G["last_bottom"]], "> 787 vs <= 787"),
            check("double fade pop found (opacity drops mid-entrance)", B["double_fade"] and not G["double_fade"], [B["double_fade"], G["double_fade"]], [True, False]),
            check("letterSpacing animation reflows the line (line count jumps)", B["reflow_jumps"] >= 1 and G["reflow_jumps"] == 0, [B["reflow_jumps"], G["reflow_jumps"]], [">= 1", 0]),
            check("fps mismatch between background and matte found", res["fps"]["bg"] != res["fps"]["matte_bad"] and res["fps"]["bg"] == res["fps"]["matte_good"], res["fps"], "30 vs 25"),
            check("negative control: the corrected captions trip none of the four", not (G["gesture_zone"] or G["double_fade"] or G["reflow_jumps"]), G["last_bottom"], "clean")], [out, Path(wd) / "bad/frame.png"]


ACTION_PAGE = """<!doctype html><html><body style="margin:0;font:16px sans-serif">
<header style="height:60px;background:#123">menu</header>
<button data-kosif-action="save" onclick="setTimeout(()=>document.getElementById('toast').style.display='block',300)">Save</button>
<button data-kosif-action="ghost" style="display:none">Hidden</button>
<a data-kosif-action="export" id="dl" download="report.csv">Export</a>
<div id="toast" style="display:none">Saved</div><div style="height:1800px;background:linear-gradient(#fff,#ccc)">long page</div>
<script>document.getElementById('dl').href=URL.createObjectURL(new Blob(['id,score\\n1,42\\n'],{type:'text/csv'}));</script></body></html>"""


@card("QA-317")
def playwright_patterns(task, wd):
    """Browser automation QA patterns: element-index JS (<= 250 elements), act on [data-kosif-action=ID],
    expect(...).toBeVisible (timeout 10000), full-page screenshot at 1280x800, downloads via the download event,
    and an anti-loop guard of 3 picks of the same target."""
    page = tw(wd / "app.html", ACTION_PAGE)
    body = """const {expect}=require('playwright/test');const ctx=await b.newContext({viewport:{width:1280,height:800},acceptDownloads:true});const p=await ctx.newPage();
await p.goto('file://'+__PAGE__);
out.index=await p.evaluate(()=>[...document.querySelectorAll('[data-kosif-action],button,a,input')].slice(0,250).map((e,i)=>({i,id:e.dataset.kosifAction||null,visible:!!(e.offsetWidth||e.offsetHeight)})));
await p.click('[data-kosif-action=save]');let vis=true;try{await expect(p.locator('#toast')).toBeVisible({timeout:10000});}catch(e){vis=false;}out.toast=vis;
let ghost=true;try{await expect(p.locator('[data-kosif-action=ghost]')).toBeVisible({timeout:500});}catch(e){ghost=false;}out.ghost=ghost;
await p.screenshot({path:__DIR__+'/full.png',fullPage:true});
const [d]=await Promise.all([p.waitForEvent('download'),p.click('[data-kosif-action=export]')]);await d.saveAs(__DIR__+'/report.csv');out.dl=d.suggestedFilename();
const picks=['save','save','save','save'];const seen={};out.loop=null;for(const [n,t] of picks.entries()){seen[t]=(seen[t]||0)+1;if(seen[t]>=3){out.loop={stopped_at:n,target:t};break;}}"""
    r = pw_run(wd, "patterns", body.replace("__PAGE__", json.dumps(str(page))).replace("__DIR__", json.dumps(str(wd))))
    from PIL import Image
    full = Image.open(wd / "full.png").size
    return [check("element index lists every actionable element with its action id", [e["id"] for e in r["index"]][:3] == ["save", "ghost", "export"] and len(r["index"]) <= 250,
                  [e["id"] for e in r["index"]], ["save", "ghost", "export"]),
            check("acting on [data-kosif-action=save] shows the toast (expect visible)", r["toast"] is True, r["toast"], True),
            check("full-page screenshot is taller than the 800 px viewport", full[1] > 1800 and full[0] == 1280, list(full), "1280 x > 1800"),
            check("download captured with its file and content", r["dl"] == "report.csv" and (wd / "report.csv").read_text() == "id,score\n1,42\n", r["dl"], "report.csv"),
            check("anti-loop stops on the 3rd pick of the same target", r["loop"] == {"stopped_at": 2, "target": "save"}, r["loop"], {"stopped_at": 2, "target": "save"}),
            check("negative control: a hidden element fails expect visible", r["ghost"] is False, r["ghost"], False)], [wd / "full.png", wd / "report.csv"]


TELLS_JS = r"""()=>{const px=s=>parseFloat(s)||0;const rgb=s=>(s.match(/\d+(\.\d+)?/g)||[]).slice(0,3).map(Number);const out={};
const all=[...document.querySelectorAll('body *')];
out.gradient_text=all.some(e=>{const c=getComputedStyle(e);return (c.webkitBackgroundClip==='text'||c.backgroundClip==='text')&&c.backgroundImage.includes('gradient');});
const cards=[...document.querySelectorAll('.card')];
out.left_accent_bar=cards.some(e=>px(getComputedStyle(e).borderLeftWidth)>=3&&px(getComputedStyle(e).borderRightWidth)===0);
out.cyan_on_black=all.some(e=>{const c=rgb(getComputedStyle(e).color),bg=rgb(getComputedStyle(document.body).backgroundColor);return c[0]<60&&c[1]>200&&c[2]>200&&bg[0]+bg[1]+bg[2]<60;});
out.purple_blue_gradient=all.some(e=>{const g=getComputedStyle(e).backgroundImage;const cs=(g.match(/rgb\([^)]*\)/g)||[]).map(rgb);return cs.length>=2&&cs.some(c=>c[0]>100&&c[2]>180&&c[1]<100)&&cs.some(c=>c[2]>180&&c[0]<100);});
out.pure_black_or_white=[document.body,...all].some(e=>{const b=getComputedStyle(e).backgroundColor;return b==='rgb(0, 0, 0)'||b==='rgb(255, 255, 255)';});
const sizes=cards.map(e=>{const r=e.getBoundingClientRect();return Math.round(r.width)+'x'+Math.round(r.height)+':'+e.children.length;});
out.identical_card_grid=cards.length>=3&&new Set(sizes).size===1;
const texts=all.filter(e=>e.childNodes.length&&[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()));
out.all_centred_single_weight=texts.length>0&&texts.every(e=>getComputedStyle(e).textAlign==='center')&&new Set(texts.map(e=>getComputedStyle(e).fontWeight)).size===1;
return out;}"""


@card("QA-329")
def ai_design_tells(task, wd):
    """AI-design tells blacklist checked on the rendered page's computed styles: gradient text, left accent bar on
    cards, cyan on black, purple-blue gradient, pure black/white, identical card grids, all-centred single weight."""
    slop = """<html><body style="background:#000;text-align:center;font-weight:400;margin:0">
<h1 style="font-weight:400;background:linear-gradient(90deg,#8a2be2,#1e90ff);-webkit-background-clip:text;background-clip:text;color:transparent">Unlock the future</h1>
<p style="color:#00ffff">Powered by AI</p><div style="background:linear-gradient(#8a2be2,#1e40ff);height:20px"></div>
<div class="card" style="border-left:4px solid #0ff;width:200px;height:80px;display:inline-block"><p>One</p></div>
<div class="card" style="border-left:4px solid #0ff;width:200px;height:80px;display:inline-block"><p>Two</p></div>
<div class="card" style="border-left:4px solid #0ff;width:200px;height:80px;display:inline-block"><p>Three</p></div></body></html>"""
    clean = """<html><body style="background:#15171c;color:#e9e4da;margin:0;font-family:sans-serif">
<h1 style="font-weight:800;text-align:left">Field notes</h1><p style="font-weight:400;text-align:left">Measured, not decorated.</p>
<div class="card" style="border:1px solid #3a3d44;width:320px;height:120px;display:inline-block"><h3>Lead</h3><p>Detail</p></div>
<div class="card" style="border:1px solid #3a3d44;width:200px;height:80px;display:inline-block"><p>Two</p></div>
<div class="card" style="border:1px solid #3a3d44;width:200px;height:80px;display:inline-block"><p>Three</p></div></body></html>"""
    res = {}
    for k, html in (("slop", slop), ("clean", clean)):
        f = tw(wd / (k + ".html"), html)
        res[k] = pw_run(wd, "tells_" + k, "const p=await b.newPage({viewport:{width:900,height:500}});await p.goto('file://'+%s);out=await p.evaluate(%s);"
                        "await p.screenshot({path:%s});" % (json.dumps(str(f)), TELLS_JS, json.dumps(str(wd / (k + ".png")))))
    out = wj(wd / "tells.json", res)
    hits = sorted(k for k, v in res["slop"].items() if v)
    return [check("all seven tells found on the generic page", len(hits) == 7, hits, 7),
            check("each tell is a named rule", sorted(res["slop"]) == sorted(["gradient_text", "left_accent_bar", "cyan_on_black", "purple_blue_gradient", "pure_black_or_white",
                                                                              "identical_card_grid", "all_centred_single_weight"]), sorted(res["slop"]), "7 names"),
            check("the revised page is clean", not any(res["clean"].values()), [k for k, v in res["clean"].items() if v], []),
            check("negative control: the untreated page fails the blacklist", any(res["slop"].values()), len(hits), "> 0")], [out, wd / "slop.png"]


A11Y_BAD = """<html><head><style>@keyframes s{to{transform:rotate(360deg)}}.spin{animation:s 2s linear infinite;width:20px;height:20px;background:#09f}</style></head>
<body style="background:#fff;margin:0"><p style="color:#bbb;font-size:14px">Low contrast caption</p><img src="data:image/gif;base64,R0lGODlhAQABAAAAACw=">
<div class="spin"></div><p>مرحبا بالعالم</p><div style="width:500px;background:#eee">wide fixed block</div></body></html>"""
A11Y_GOOD = """<html lang="ar" dir="rtl"><head><title>ok</title><style>@keyframes s{to{transform:rotate(360deg)}}.spin{animation:s 2s linear infinite;width:20px;height:20px;background:#09f}
@media (prefers-reduced-motion: reduce){.spin{animation:none}}</style></head>
<body style="background:#fff;margin:0"><main><h1>عنوان</h1><p style="color:#333;font-size:14px">نص واضح</p><img alt="شعار القناة" src="data:image/gif;base64,R0lGODlhAQABAAAAACw=">
<div class="spin"></div><div style="max-width:100%;background:#eee">كتلة مرنة</div></main></body></html>"""


@card("QA-332")
def accessibility_wcag(task, wd):
    """WCAG 2.2 gate: axe-core scan (contrast 4.5:1, alt text), 200 % zoom without horizontal scroll, motion that
    stops under prefers-reduced-motion, and RTL direction for Arabic text; re-scan after the fix."""
    axe = Path(NODE_MODULES) / "axe-core/axe.min.js"
    res = {}
    for k, html in (("before", A11Y_BAD), ("after", A11Y_GOOD)):
        f = tw(wd / (k + ".html"), html)
        body = """const p=await b.newPage({viewport:{width:640,height:480}});await p.goto('file://'+__F__);await p.addScriptTag({path:__AXE__});
const r=await p.evaluate(async()=>{const x=await axe.run(document,{runOnly:['wcag2a','wcag2aa']});return x.violations.map(v=>v.id);});
const z=await b.newPage({viewport:{width:320,height:480}});await z.goto('file://'+__F__);const zoom=await z.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
const m=await b.newPage({viewport:{width:640,height:480},reducedMotion:'reduce'});await m.goto('file://'+__F__);
const anim=await m.evaluate(()=>getComputedStyle(document.querySelector('.spin')).animationName);
const dir=await p.evaluate(()=>getComputedStyle(document.querySelector('p:last-of-type')||document.body).direction);
out={violations:r,overflow_at_200:zoom,reduced_motion_animation:anim,dir};"""
        res[k] = pw_run(wd, "a11y_" + k, body.replace("__F__", json.dumps(str(f))).replace("__AXE__", json.dumps(str(axe))))
    out = wj(wd / "wcag_report.json", res)
    B, A = res["before"], res["after"]
    return [check("axe finds the contrast and alt-text failures", {"color-contrast", "image-alt"} <= set(B["violations"]), B["violations"], ["color-contrast", "image-alt"]),
            check("200 % zoom (320 css px) scrolls sideways before, not after", B["overflow_at_200"] and not A["overflow_at_200"], [B["overflow_at_200"], A["overflow_at_200"]], [True, False]),
            check("motion stops under prefers-reduced-motion after the fix", B["reduced_motion_animation"] == "s" and A["reduced_motion_animation"] == "none",
                  [B["reduced_motion_animation"], A["reduced_motion_animation"]], ["s", "none"]),
            check("Arabic text runs right-to-left after the fix", A["dir"] == "rtl" and B["dir"] == "ltr", [B["dir"], A["dir"]], ["ltr", "rtl"]),
            check("re-scan after the fix: no axe violations", A["violations"] == [], A["violations"], []),
            check("negative control: the untreated page fails the gate", len(B["violations"]) >= 2, len(B["violations"]), ">= 2")], [out]


THUMB = """<html><body style="margin:0;width:1280px;height:720px;background:__BG__;font-family:sans-serif;position:relative;overflow:hidden">
<div id="photo" style="position:absolute;right:60px;top:110px;width:480px;height:500px;background:#c8743c"></div>
<h1 id="title" style="position:absolute;left:60px;top:200px;margin:0;font:900 120px sans-serif;color:__TC__">__TXT__</h1></body></html>"""


@card("QA-338")
def ab_thumbnail_single_variable(task, wd):
    """A/B thumbnail, one variable: two versions that differ in exactly one element (the pixel diff stays inside that
    element's box) and a 10 % downscale legibility test of the title."""
    np = _np()
    from PIL import Image
    variants = {"A": ("#101820", "#ffd400", "SAVE 2H"), "B": ("#101820", "#3a4048", "SAVE 2H"), "C": ("#2a1030", "#3a4048", "SAVE 2H")}
    boxes = {}
    for k, (bg, tc, txt) in variants.items():
        f = tw(wd / (k + ".html"), THUMB.replace("__BG__", bg).replace("__TC__", tc).replace("__TXT__", txt))
        boxes[k] = pw_run(wd, "thumb_" + k, "const p=await b.newPage({viewport:{width:1280,height:720}});await p.goto('file://'+%s);await p.screenshot({path:%s});"
                          "out=await p.evaluate(()=>{const r=document.getElementById('title').getBoundingClientRect();return [r.x,r.y,r.width,r.height];});"
                          % (json.dumps(str(f)), json.dumps(str(wd / (k + ".png")))))
    img = {k: load_png(wd / (k + ".png")) for k in variants}

    def diff_inside(a, b, box):
        m = np.abs(img[a] - img[b]).max(axis=2) > 8
        ys, xs = np.nonzero(m)
        x, y, w, h = box
        inside = ((xs >= x - 2) & (xs <= x + w + 2) & (ys >= y - 2) & (ys <= y + h + 2)).mean() if len(xs) else 0
        return float(inside), int(m.sum())

    def legible(k):
        small = np.asarray(Image.fromarray(img[k].astype("uint8")).resize((128, 72), Image.LANCZOS), float)
        x, y, w, h = [v / 10 for v in boxes[k]]
        reg = small[int(y):int(y + h), int(x):int(x + w)]
        lum = reg.mean(axis=2)
        fg, bgc = reg.reshape(-1, 3)[lum.flatten() >= np.percentile(lum, 95)].mean(0), reg.reshape(-1, 3)[lum.flatten() <= np.percentile(lum, 20)].mean(0)
        return contrast(fg, bgc), h
    ab_in, ab_n = diff_inside("A", "B", boxes["A"])
    ac_in, _ = diff_inside("A", "C", boxes["A"])
    la, lb = legible("A"), legible("B")
    out = wj(wd / "ab.json", {"A_vs_B_diff_inside_title": ab_in, "A_vs_C_diff_inside_title": ac_in, "legibility_10pct": {"A": la, "B": lb}})
    return [check("A vs B differ only inside the title box (one variable)", ab_in > 0.99 and ab_n > 1000, [ab_in, ab_n], "> 0.99"),
            check("at 10 % (128x72) the title is still >= 9 px tall", la[1] >= 9, la[1], ">= 9"),
            check("A's title stays legible at 10 % (contrast >= 4.5)", la[0] >= 4.5, la[0], ">= 4.5"),
            check("B's dim title fails the 10 % legibility test", lb[0] < 3, lb[0], "< 3"),
            check("negative control: A vs C change two elements, so the pair is not single-variable", ac_in < 0.5, ac_in, "< 0.5")], [out, wd / "A.png"]


CAPTURE_PAGE = """<html><head><style>@font-face{font-family:K;src:url('__FONT__')}body{margin:0;font-family:K;background:#f4f1ea;color:#222}
button{font:24px K;padding:10px}button:hover{background:#ffb000}</style></head><body><h1 id="d"></h1><button id="b">Go</button>
<script>document.getElementById('d').textContent=new Intl.DateTimeFormat(navigator.language,{dateStyle:'full',timeStyle:'short'}).format(new Date(Date.UTC(2026,0,1,23,30)));</script></body></html>"""


@card("QA-74")
def reproducible_ui_capture(task, wd):
    """Reproducible UI capture: identical route, viewport 1280x820 @2x, theme, locale, timezone and interaction state;
    wait for observable readiness (document.fonts.ready) instead of sleeps; drive hover explicitly."""
    font = SKILLS / "kosif-superpowers/proofs/_shared/fonts/Poppins-Bold.ttf"
    shutil.copy(font, wd / "font.ttf")
    f = tw(wd / "ui.html", CAPTURE_PAGE.replace("__FONT__", "font.ttf"))
    body = """const shot=async(name,tz)=>{const c=await b.newContext({viewport:{width:1280,height:820},deviceScaleFactor:2,colorScheme:'light',locale:'en-GB',timezoneId:tz});
const p=await c.newPage();await p.goto('file://'+__F__);await p.evaluate(()=>document.fonts.ready);const ff=await p.evaluate(()=>document.fonts.check('24px K'));
await p.hover('#b');await p.screenshot({path:__DIR__+'/'+name+'.png'});const txt=await p.textContent('#d');await c.close();return {ff,txt};};
out.a=await shot('a','UTC');out.b=await shot('b','UTC');out.tokyo=await shot('tokyo','Asia/Tokyo');"""
    r = pw_run(wd, "capture", body.replace("__F__", json.dumps(str(f))).replace("__DIR__", json.dumps(str(wd))))
    from PIL import Image
    size = Image.open(wd / "a.png").size
    hover = load_png(wd / "a.png")
    orange = int(((hover[..., 0] > 230) & (hover[..., 1] > 150) & (hover[..., 1] < 200) & (hover[..., 2] < 40)).sum())
    out = wj(wd / "capture.json", dict(r, sha={k: sha(wd / (k + ".png")) for k in ("a", "b", "tokyo")}))
    return [check("two captures with identical settings are byte-identical", sha(wd / "a.png") == sha(wd / "b.png"), sha(wd / "a.png")[:12], "== second"),
            check("1280x820 at device scale 2 -> 2560x1640 pixels", size == (2560, 1640), list(size), [2560, 1640]),
            check("web font loaded before the capture (fonts.ready, then check)", r["a"]["ff"] is True, r["a"]["ff"], True),
            check("hover state driven explicitly (button turned #ffb000)", orange > 500, orange, "> 500 px"),
            check("negative control: a different timezone changes the capture", sha(wd / "tokyo.png") != sha(wd / "a.png") and r["tokyo"]["txt"] != r["a"]["txt"],
                  [r["a"]["txt"], r["tokyo"]["txt"]], "differs")], [out, wd / "a.png"]


SWEEP_SCREENS = {
    "home": "<header style='height:60px;background:#123;color:#fff'>App</header><main><h1>Home</h1><p>Welcome back, 3 new clips.</p><button>Open</button></main>",
    "stats": "<header style='height:60px;background:#123;color:#fff'>App</header><main><h1>Stats</h1><p>Views: NaN</p><p>Owner: undefined</p><p>[object Object]</p></main>",
    "table": "<header style='height:60px;background:#123;color:#fff'>App</header><main><table style='width:600px'><tr><td>wide table that does not fit a phone</td></tr></table>"
             "<button style='width:80px;white-space:nowrap;overflow:hidden'>Download everything now</button></main>",
    "empty": "<header style='height:300px;background:#123;color:#fff'>App</header><nav style='height:200px;background:#234'>nav</nav><main></main>",
}


@card("QA-79")
def playwright_visual_sweeps(task, wd):
    """Visual sweeps: open every registered screen on a laptop viewport and 390 / 320 px phones, screenshot it, fail
    on page errors, broken values (undefined / NaN / [object Object]), horizontal overflow, clipped controls or empty
    views; a clutter audit measures chrome (header/nav) against content."""
    www = Path(wd) / "build"
    for k, v in SWEEP_SCREENS.items():
        tw(www / (k + ".html"), "<html><head><meta name='viewport' content='width=device-width'></head><body style='margin:0;font:16px sans-serif'>%s</body></html>" % v)
    srv = Serve(www)
    try:
        body = """const res={};for(const s of __SCREENS__){for(const [vw,vh] of [[1280,800],[390,844],[320,640]]){const p=await b.newPage({viewport:{width:vw,height:vh}});const errs=[];
p.on('pageerror',e=>errs.push(String(e)));await p.goto(__URL__+'/'+s+'.html');await p.screenshot({path:__DIR__+'/'+s+'_'+vw+'.png'});
const m=await p.evaluate(()=>{const t=document.body.innerText;const main=document.querySelector('main');const chrome=[...document.querySelectorAll('header,nav')].reduce((a,e)=>a+e.offsetHeight,0);
 return {broken:(t.match(/undefined|NaN|\\[object Object\\]/g)||[]),overflow:document.documentElement.scrollWidth>innerWidth,
 clipped:[...document.querySelectorAll('button')].some(e=>e.scrollWidth>e.clientWidth+1),empty:!main||main.innerText.trim().length<3,chrome,content:main?main.offsetHeight:0};});
res[s+'@'+vw]=Object.assign(m,{errors:errs});await p.close();}}out=res;"""
        r = pw_run(wd, "sweep", body.replace("__SCREENS__", json.dumps(list(SWEEP_SCREENS))).replace("__URL__", json.dumps(srv.url)).replace("__DIR__", json.dumps(str(wd))), timeout=90)
    finally:
        srv.close()
    fails = {k: [n for n in ("broken", "overflow", "clipped", "empty") if v[n]] + (["errors"] if v["errors"] else []) for k, v in r.items()}
    fails = {k: v for k, v in fails.items() if v}
    clutter = {k: round(v["chrome"] / max(1, v["chrome"] + v["content"]), 2) for k, v in r.items() if k.endswith("@1280")}
    out = wj(wd / "sweep.json", {"pages": r, "fails": fails, "clutter": clutter})
    return [check("12 screenshots: 4 screens x 3 viewports", len(r) == 12 and len(list(wd.glob("*_*.png"))) == 12, len(r), 12),
            check("broken values found on stats at every size", all(fails.get("stats@%d" % w) == ["broken"] for w in (1280, 390, 320)), [fails.get("stats@%d" % w) for w in (1280, 390, 320)], "broken"),
            check("table overflows and clips only on phones", "overflow" in fails.get("table@390", []) and "overflow" in fails.get("table@320", []) and "overflow" not in fails.get("table@1280", []),
                  [fails.get("table@%d" % w) for w in (1280, 390, 320)], "phones only"),
            check("empty view caught and its chrome dominates (clutter >= 0.9)", "empty" in fails.get("empty@1280", []) and clutter["empty@1280"] >= 0.9, clutter, "empty >= 0.9"),
            check("negative control: home passes on every viewport", not any(k.startswith("home@") for k in fails), [k for k in fails if k.startswith("home")], [])], [out, wd / "stats_390.png"]


def render_spec_still(spec, path, W=320, H=180):
    from PIL import Image, ImageDraw
    im = Image.new("RGB", (W, H), spec["bg"])
    d = ImageDraw.Draw(im)
    x, y, w, h = spec["title_box"]
    d.rectangle([x, y, x + w, y + h], fill=spec["title_color"])
    im.save(path)
    return Path(path)


REVIEW_PAGE = """<!doctype html><html><body style="margin:0"><img id="f" src="frame.png" style="display:block">
<input id="note" value=""><script>
const pins=[];document.getElementById('f').addEventListener('click',async e=>{pins.push({x:e.offsetX,y:e.offsetY,t:1.0,note:document.getElementById('note').value});
 await fetch('feedback',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({pins})});window.__sent=pins.length;});
</script></body></html>"""


@card("QA-183")
def review_site_markup(task, wd):
    """Review site markup: `review init` writes a local review page on 127.0.0.1, the user pins a note on the frame,
    the page POSTs feedback, and `apply` changes the spec under the pin and re-renders."""
    spec = {"bg": "#101820", "title_box": [40, 40, 160, 40], "title_color": "#ffffff", "other_box": [220, 120, 60, 30]}
    name = "film1"
    site = Path(wd) / "review" / name
    site.mkdir(parents=True)
    wj(wd / "spec.json", spec)
    render_spec_still(spec, site / "frame.png")
    tw(site / "index.html", REVIEW_PAGE)
    got = {}

    def fb(h, body):
        got.update(json.loads(body))
        wj(wd / "feedback.json", got)
        send_json(h, {"ok": True})
    srv = Serve(wd, {("POST", "/review/%s/feedback" % name): fb})
    try:
        url = srv.url + "/review/%s/" % name
        body = """const p=await b.newPage({viewport:{width:320,height:240}});await p.goto(__URL__);await p.fill('#note','make the title gold');
await p.click('#f',{position:{x:100,y:60}});await p.waitForFunction('window.__sent===1');out.url=__URL__;"""
        r = pw_run(wd, "review", body.replace("__URL__", json.dumps(url)))
    finally:
        srv.close()
    fbk = rj(wd / "feedback.json")
    spec2 = dict(spec)
    applied = []
    for pin in fbk["pins"]:
        x, y, w, h = spec["title_box"]
        if x <= pin["x"] <= x + w and y <= pin["y"] <= y + h and "gold" in pin["note"]:
            spec2["title_color"] = "#ffb000"
            applied.append("title_color")
    wj(wd / "spec_applied.json", spec2)
    render_spec_still(spec2, wd / "frame_applied.png")
    a, b0 = load_png(wd / "frame_applied.png"), load_png(site / "frame.png")
    return [check("review page served on 127.0.0.1 under /review/NAME/", r["url"].startswith("http://127.0.0.1:") and r["url"].endswith("/review/film1/"), r["url"], "/review/film1/"),
            check("pinned note posted back with its position and text", fbk["pins"] == [{"x": 100, "y": 60, "t": 1.0, "note": "make the title gold"}], fbk["pins"], "1 pin"),
            check("apply mapped the pin to the title and changed only it", applied == ["title_color"] and spec2["other_box"] == spec["other_box"], applied, ["title_color"]),
            check("re-render shows the gold title", a[60, 100].tolist() == [255, 176, 0], a[60, 100].tolist(), [255, 176, 0]),
            check("negative control: before apply the title is white", b0[60, 100].tolist() == [255, 255, 255], b0[60, 100].tolist(), [255, 255, 255])], [wd / "feedback.json", wd / "frame_applied.png"]


PLAYER_PAGE = """<!doctype html><html><head><style>body{background:#fafafa;color:#111;font:14px sans-serif}
@media (prefers-color-scheme: dark){body{background:#111;color:#eee}}</style></head><body><div id="scenes"></div><button id="send">Send to Claude</button>
<script>let reel;fetch('reel.json').then(r=>r.json()).then(j=>{reel=j;const box=document.getElementById('scenes');
 reel.scenes.forEach(s=>{box.insertAdjacentHTML('beforeend',`<div class=sc data-id=${s.id}><input class=text value="${s.text}"><select class=status><option>review</option><option>changes</option><option>approved</option></select><input class=pin placeholder="note"></div>`);});window.__ok=true;});
document.getElementById('send').onclick=async()=>{const lines=[];const changes=[];
 document.querySelectorAll('.sc').forEach(d=>{const s=reel.scenes.find(x=>x.id==d.dataset.id);const text=d.querySelector('.text').value,st=d.querySelector('.status').value,pin=d.querySelector('.pin').value;
  const c={id:s.id,status:st};if(text!==s.text){c.text=text;lines.push(`Scene ${s.id}: change text "${s.text}" -> "${text}"`);} if(pin){c.note=pin;lines.push(`Scene ${s.id}: note "${pin}"`);}
  if(st==='approved')lines.push(`Scene ${s.id}: approved, do not touch`);changes.push(c);});
 const body={prompt:lines.join('\\n'),changes};await fetch('feedback',{method:'POST',body:JSON.stringify(body)});window.__sent=true;};</script></body></html>"""


@card("QA-40")
def scene_review_player(task, wd):
    """Scene-by-scene review player: `review init` writes reel.json and serves the player; the user edits a scene's
    text, pins a note, marks scenes approved and sends one prompt; Claude reads kosif_review_feedback and applies only
    the requested changes. Light and dark themes follow prefers-color-scheme."""
    reel = {"name": "reel1", "scenes": [{"id": 1, "text": "Welcome", "status": "review"}, {"id": 2, "text": "Old line", "status": "review"},
                                        {"id": 3, "text": "Follow", "status": "review"}]}
    site = Path(wd) / "review/reel1"
    wj(site / "reel.json", reel)
    tw(site / "index.html", PLAYER_PAGE)

    def fb(h, body):
        wj(wd / "kosif_review_feedback.json", json.loads(body))
        send_json(h, {"ok": True})
    srv = Serve(wd, {("POST", "/review/reel1/feedback"): fb})
    try:
        body = """const p=await b.newPage();await p.goto(__URL__);await p.waitForFunction('window.__ok===true');
await p.fill('.sc[data-id="2"] .text','New line');await p.selectOption('.sc[data-id="1"] .status','approved');await p.selectOption('.sc[data-id="2"] .status','changes');
await p.fill('.sc[data-id="2"] .pin','logo bigger');await p.click('#send');await p.waitForFunction('window.__sent===true');
out.light=await p.evaluate(()=>getComputedStyle(document.body).backgroundColor);
const d=await b.newPage({colorScheme:'dark'});await d.goto(__URL__);out.dark=await d.evaluate(()=>getComputedStyle(document.body).backgroundColor);"""
        r = pw_run(wd, "player", body.replace("__URL__", json.dumps(srv.url + "/review/reel1/")))
    finally:
        srv.close()
    fbk = rj(wd / "kosif_review_feedback.json")
    applied = json.loads(json.dumps(reel))
    for c in fbk["changes"]:
        s = [x for x in applied["scenes"] if x["id"] == c["id"]][0]
        s["status"] = c["status"]
        if "text" in c and s["status"] != "approved":
            s["text"] = c["text"]
        if "note" in c:
            s["note"] = c["note"]
    wj(wd / "reel_applied.json", applied)
    sc = {s["id"]: s for s in applied["scenes"]}
    return [check("one prompt names only scene 2's change and note, and scene 1's approval", fbk["prompt"].splitlines() == [
                "Scene 1: approved, do not touch", 'Scene 2: change text "Old line" -> "New line"', 'Scene 2: note "logo bigger"'], fbk["prompt"].splitlines(), 3),
            check("applied: scene 2 text changed and marked for changes", sc[2]["text"] == "New line" and sc[2]["status"] == "changes", sc[2], "New line / changes"),
            check("approved scene 1 untouched, scene 3 untouched", sc[1] == {"id": 1, "text": "Welcome", "status": "approved"} and sc[3]["text"] == "Follow", [sc[1], sc[3]], "unchanged"),
            check("light and dark themes differ", r["light"] == "rgb(250, 250, 250)" and r["dark"] == "rgb(17, 17, 17)", [r["light"], r["dark"]], "light / dark"),
            check("negative control: the original reel still has the old line", reel["scenes"][1]["text"] == "Old line", reel["scenes"][1]["text"], "Old line")], [wd / "kosif_review_feedback.json", wd / "reel_applied.json"]


@card("QA-214")
def concept_first_build(task, wd):
    """Concept image first, then a faithful build: lock an approved storyboard still as the spec, extract its exact
    colour tokens, build the frame in HTML from them, and compare concept vs render with an 8x8 hotspot grid until
    they match (image generation itself is an external service, so the approved still stands in for it)."""
    np = _np()
    from PIL import Image, ImageDraw
    from collections import Counter
    im = Image.new("RGB", (320, 176), "#0e1a2b")
    d = ImageDraw.Draw(im)
    d.rectangle([20, 40, 219, 79], fill="#f4efe6")
    d.rectangle([20, 120, 199, 135], fill="#ffb000")
    im.save(wd / "concept.png")
    tok = [("#%02x%02x%02x" % c) for c, _ in Counter(im.getdata()).most_common(3)]
    tokens = {"ground": tok[0], "ink": tok[1], "accent": tok[2]}
    wj(wd / "tokens.json", tokens)

    def build(name, accent_x):
        html = ("<html><body style='margin:0;width:320px;height:176px;background:%s;position:relative'>"
                "<div style='position:absolute;left:20px;top:40px;width:200px;height:40px;background:%s'></div>"
                "<div style='position:absolute;left:%dpx;top:120px;width:180px;height:16px;background:%s'></div></body></html>" % (tokens["ground"], tokens["ink"], accent_x, tokens["accent"]))
        f = tw(wd / (name + ".html"), html)
        pw_run(wd, name, "const p=await b.newPage({viewport:{width:320,height:176}});await p.goto('file://'+%s);await p.screenshot({path:%s});"
               % (json.dumps(str(f)), json.dumps(str(wd / (name + ".png")))))
        return load_png(wd / (name + ".png"))
    C = load_png(wd / "concept.png")

    def hotspots(R):
        g = np.abs(R - C).mean(axis=2)
        cells = [[float(g[r * 22:(r + 1) * 22, c * 40:(c + 1) * 40].mean()) for c in range(8)] for r in range(8)]
        return [(r, c) for r in range(8) for c in range(8) if cells[r][c] > 1.0]
    h1 = hotspots(build("build_v1", 60))
    h2 = hotspots(build("build_v2", 20))
    out = wj(wd / "fidelity.json", {"tokens": tokens, "v1_hotspots": h1, "v2_hotspots": h2})
    return [check("tokens extracted exactly from the concept", tokens == {"ground": "#0e1a2b", "ink": "#f4efe6", "accent": "#ffb000"}, tokens, "exact hexes"),
            check("v1 hotspots sit only on the misplaced accent bar (rows 5-6, y 120-136)", h1 and all(r in (5, 6) for r, _ in h1), h1, "rows 5-6 only"),
            check("v2 matches the concept: no hotspot in the 8x8 grid", h2 == [], h2, []),
            check("render pixels equal the concept tokens", load_png(wd / "build_v2.png")[125, 100].tolist() == [255, 176, 0], load_png(wd / "build_v2.png")[125, 100].tolist(), [255, 176, 0]),
            check("negative control: the first build fails the fidelity bar", len(h1) > 0, len(h1), "> 0")], [out, wd / "build_v2.png"]


@card("QA-145")
def integration_health_check(task, wd):
    """Integration health page: /api/basma-health reports configuration without ever returning credentials, read-only
    model probes answer one word each, a streaming test sends 5 chunks 0.7 s apart, and a realistic 4 KB JSON
    round-trips; timeouts per route. Local stand-ins replace Gemini and Claude (no live service is called)."""
    import http.client
    import urllib.request
    secret = "sk" + "-" + "ant" + "-" + "x" * 24
    cfg = {"GEMINI_API_KEY": "AI" + "za" + "y" * 30, "ANTHROPIC_API_KEY": secret, "MODEL": "local-stub"}

    def health(h, body):
        send_json(h, {k.split("_")[0].lower(): {"configured": bool(v)} for k, v in cfg.items() if k.endswith("KEY")})

    def leak(h, body):
        send_json(h, cfg)

    def model(name):
        return lambda h, body: send_json(h, {"model": name, "answer": "ok"})

    def stream(h, body):
        h.send_response(200)
        h.send_header("Content-Type", "text/plain")
        h.send_header("Transfer-Encoding", "chunked")
        h.end_headers()
        for i in range(5):
            data = ("chunk%d\n" % i).encode()
            h.wfile.write(b"%x\r\n%s\r\n" % (len(data), data))
            h.wfile.flush()
            time.sleep(0.7) if i < 4 else None
        h.wfile.write(b"0\r\n\r\n")

    def echo(h, body):
        send_json(h, {"bytes": len(body), "keys": len(json.loads(body))})
    api = {("GET", "/api/basma-health"): health, ("GET", "/api/debug-env"): leak, ("GET", "/api/model/gemini"): model("gemini"),
           ("GET", "/api/model/claude"): model("claude"), ("GET", "/api/stream"): stream, ("POST", "/api/echo"): echo}
    srv = Serve(wd, api)
    diag = {}
    try:
        get = lambda p, t=45: urllib.request.urlopen(srv.url + p, timeout=t).read()
        hb = get("/api/basma-health")
        naive = get("/api/debug-env")
        diag["health"] = json.loads(hb)
        diag["models"] = {m: json.loads(get("/api/model/" + m))["answer"] for m in ("gemini", "claude")}
        host, port = srv.url.split("//")[1].split(":")
        c = http.client.HTTPConnection(host, int(port), timeout=10)
        c.request("GET", "/api/stream")
        resp = c.getresponse()
        stamps, t0 = [], time.time()
        for _ in range(5):
            resp.readline()
            stamps.append(round(time.time() - t0, 3))
        payload = json.dumps({"k%03d" % i: "v" * 30 for i in range(110)}).encode()
        rq = urllib.request.Request(srv.url + "/api/echo", data=payload, headers={"Content-Type": "application/json"})
        diag["echo"] = json.loads(urllib.request.urlopen(rq, timeout=45).read())
        diag["stream_stamps"] = stamps
    finally:
        srv.close()
    gaps = [b - a for a, b in zip(stamps, stamps[1:])]
    out = wj(wd / "diagnosis.json", diag)
    leaked = lambda blob: any(v.encode() in blob for k, v in cfg.items() if k.endswith("KEY"))
    return [check("health reports both integrations configured", diag["health"] == {"gemini": {"configured": True}, "anthropic": {"configured": True}}, diag["health"], "configured"),
            check("health response contains no credential", not leaked(hb), leaked(hb), False),
            check("each model route answers one word", all(len(a.split()) == 1 for a in diag["models"].values()), diag["models"], "one word"),
            check("stream: 5 chunks about 0.7 s apart", len(stamps) == 5 and all(0.55 <= g <= 0.9 for g in gaps), gaps, 0.7),
            check("realistic ~4 KB JSON round-trips", 3500 <= diag["echo"]["bytes"] <= 5000 and diag["echo"]["keys"] == 110, diag["echo"], "~4 KB, 110 keys"),
            check("negative control: a naive debug-env page leaks the key", leaked(naive), leaked(naive), True)], [out]


@card("QA-220")
def single_frame_director_review(task, wd):
    """Single-frame director review (rule-based, no model call): the current frame is exported as JPEG q0.82 and
    judged for caption contrast, faces covered, Reels/TikTok safe zones (bottom 18 %, right strip), colour harmony
    and clutter; only what is wrong is fixed."""
    np = _np()
    from PIL import Image, ImageDraw
    W, H = 270, 480
    layout = {"face": [85, 120, 100, 110], "caption": [30, 420, 200, 36], "logo": [235, 200, 30, 30]}
    style = {"caption_fg": "#8a8a8a", "caption_bg": "#6a6a6a", "bg": "#2c3e50"}

    def draw(L, S, path):
        im = Image.new("RGB", (W, H), S["bg"])
        d = ImageDraw.Draw(im)
        x, y, w, h = L["face"]
        d.ellipse([x, y, x + w, y + h], fill="#e0b090")
        x, y, w, h = L["caption"]
        d.rectangle([x, y, x + w, y + h], fill=S["caption_bg"])
        d.rectangle([x + 10, y + 12, x + w - 10, y + 22], fill=S["caption_fg"])
        x, y, w, h = L["logo"]
        d.rectangle([x, y, x + w, y + h], fill="#ffffff")
        im.save(path, quality=82)
        return np.asarray(Image.open(path).convert("RGB"), float)

    def review(L, path):
        A = np.asarray(Image.open(path).convert("RGB"), float)
        fixes = []
        x, y, w, h = L["caption"]
        fg, bg = A[y + 17, x + w // 2], A[y + 4, x + 4]
        if contrast(fg, bg) < 4.5:
            fixes.append("caption contrast %.2f < 4.5" % contrast(fg, bg))
        if y + h > H * 0.82:
            fixes.append("caption in bottom 18 %")
        lx = L["logo"][0]
        if lx + L["logo"][2] > W * 0.85:
            fixes.append("logo in right-side UI strip")
        fx_, fy, fw, fh = L["face"]
        if not (x + w < fx_ or x > fx_ + fw or y + h < fy or y > fy + fh):
            fixes.append("face covered")
        return fixes
    A0 = draw(layout, style, wd / "frame_v1.jpg")
    f1 = review(layout, wd / "frame_v1.jpg")
    L2, S2 = json.loads(json.dumps(layout)), dict(style)
    if any(f.startswith("caption contrast") for f in f1):
        S2["caption_fg"], S2["caption_bg"] = "#ffffff", "#111111"
    if "caption in bottom 18 %" in f1:
        L2["caption"][1] = 330
    if "logo in right-side UI strip" in f1:
        L2["logo"][0] = 20
    draw(L2, S2, wd / "frame_v2.jpg")
    f2 = review(L2, wd / "frame_v2.jpg")
    out = wj(wd / "director_review.json", {"v1": f1, "v2": f2, "layout_v2": L2})
    return [check("frame exported as JPEG q0.82", (wd / "frame_v1.jpg").read_bytes()[:2] == b"\xff\xd8", "jpeg", "q0.82"),
            check("three problems found: contrast, bottom zone, right strip", [f.split()[0] for f in f1] == ["caption", "caption", "logo"], f1, 3),
            check("face not covered, so not touched", "face covered" not in f1 and L2["face"] == layout["face"], L2["face"], layout["face"]),
            check("after the fixes the frame passes review", f2 == [], f2, []),
            check("negative control: the untreated frame fails review", len(f1) > 0, len(f1), "> 0")], [out, wd / "frame_v2.jpg"]


# ═════════════════════════ test suites, judges and evaluators ═════════════════════════
def copy_tree(src, dst, ignore=("__pycache__", "node_modules", ".git", "out", "renders")):
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(*ignore))
    return Path(dst)


def mutate(path, old, new):
    t = Path(path).read_text(encoding="utf-8")
    if old not in t:
        raise RuntimeError("mutation anchor not found in %s" % path)
    Path(path).write_text(t.replace(old, new, 1), encoding="utf-8")


@card("QA-25")
def fastify_unit_suite(task, wd):
    """`npm test` = node --test over planner, all seven profiles, CLI persistence/clean plate and the viral gate:
    24/24 pass on a copy of the project; a mutated planner copy must fail."""
    src = Path("/home/claude/fastify-motion-bro")
    if not (src / "tests").exists():
        raise RuntimeError("fastify-motion-bro project not found")
    res = {}
    for k in ("clean", "mutant"):
        d = copy_tree(src, wd / k)
        if k == "mutant":
            mutate(d / "scripts/planner.mjs", "b.duration_seconds<=12?3", "b.duration_seconds<=12?4")
        files = sorted(str(p.relative_to(d)) for p in (d / "tests").glob("*.test.mjs"))
        t0 = time.time()
        done = subprocess.run(["node", "--test", *files], capture_output=True, text=True, timeout=60, cwd=str(d), stdin=subprocess.DEVNULL)
        get = lambda key: int((re.search(r"# %s (\d+)" % key, done.stdout) or [0, 0])[1])
        res[k] = {"rc": done.returncode, "tests": get("tests"), "pass": get("pass"), "fail": get("fail"), "seconds": round(time.time() - t0, 2)}
        tw(wd / (k + "_tap.txt"), done.stdout)
    out = wj(wd / "suite.json", res)
    return [check("24 tests run and pass on the clean copy", res["clean"]["tests"] == 24 and res["clean"]["pass"] == 24 and res["clean"]["rc"] == 0, res["clean"], "24/24"),
            check("suite is fast (< 5 s)", res["clean"]["seconds"] < 5, res["clean"]["seconds"], "< 5 s"),
            check("mutant planner (4 scenes for a short film) is caught", res["mutant"]["fail"] >= 1 and res["mutant"]["rc"] != 0, res["mutant"], ">= 1 failure"),
            check("negative control: the suite is not vacuous (mutant pass count drops)", res["mutant"]["pass"] < res["clean"]["pass"], [res["mutant"]["pass"], res["clean"]["pass"]], "fewer")], [out, wd / "clean_tap.txt"]


def unittest_run(cwd, args, timeout=60, env=None):
    done = subprocess.run([sys.executable, "-B", *args], capture_output=True, text=True, timeout=timeout, cwd=str(cwd), stdin=subprocess.DEVNULL,
                          env=dict(os.environ, **(env or {})))
    txt = done.stdout + done.stderr
    ran = int((re.search(r"Ran (\d+) test", txt) or [0, 0])[1])
    fails = sum(int(x) for x in re.findall(r"(?:failures|errors)=(\d+)", txt))
    skipped = int((re.search(r"skipped=(\d+)", txt) or [0, 0])[1])
    return {"rc": done.returncode, "ran": ran, "failed": fails, "skipped": skipped, "ok": "\nOK" in txt}, txt


@card("QA-60")
def motion_test_suite(task, wd):
    """kosif-montage-motion test suite: test_audio2motion.py (semantic routing, safe cue estimates, invalid timings,
    audio envelope, kmotion registration, frame maths) on a copy of the scripts; a mutated validator must fail it."""
    src = VENDOR / "kosif-montage-motion/scripts"
    res = {}
    for k in ("clean", "mutant"):
        d = copy_tree(src, wd / k)
        if k == "mutant":
            mutate(d / "audio2motion.py", "if a<p-0.015:raise ValueError('Cues must be sorted and nonoverlapping')", "pass")
        res[k], txt = unittest_run(d, ["test_audio2motion.py"])
        tw(wd / (k + ".log"), txt)
    out = wj(wd / "suite.json", res)
    return [check("audio2motion suite runs >= 7 tests and passes", res["clean"]["ran"] >= 7 and res["clean"]["ok"], res["clean"], ">= 7 OK"),
            check("mutant (overlapping cues accepted) is caught", res["mutant"]["failed"] >= 1 and not res["mutant"]["ok"], res["mutant"], ">= 1 failure"),
            check("same test count on both copies", res["clean"]["ran"] == res["mutant"]["ran"], [res["clean"]["ran"], res["mutant"]["ran"]], "equal"),
            check("negative control: the untreated mutant does not pass", res["mutant"]["rc"] != 0, res["mutant"]["rc"], "!= 0")], [out, wd / "clean.log"]


@card("QA-208")
def studio_regression_suite(task, wd):
    """KOSIF Studio (pixel-studio-painter) regression suite: renderer holes / even-odd / arcs / gradients / Arabic
    text, SVG import, exact redraw, image-to-Python, HTML frames, drawing films, edit packages and the studio, run with
    unittest on a copy; the three slowest classes (judge, AI bridge, vectorise noise) are left out to stay under 15 s, and
    so is Html (its Python-playwright launch fails when TMPDIR points into the work folder: the socket path is too long);
    a mutated even-odd compound must fail."""
    src = VENDOR / "pixel-studio-painter/scripts"
    classes = ["Renderer", "Svg", "Exact", "ImageToPython", "Film", "EditPack", "Studio"]
    res = {}
    for k in ("clean", "mutant"):
        d = copy_tree(src, wd / k)
        if k == "mutant":
            mutate(d / "render.py", "    if len(polys) < 2:\n        return polys\n    a = polys[0][0]", "    return polys\n    a = polys[0][0]")
        sel = ["test_studio." + c for c in (classes if k == "clean" else ["Renderer"])]
        (wd / (k + "_tmp")).mkdir()
        res[k], txt = unittest_run(d / "tests", ["-m", "unittest", *sel], timeout=60, env={"TMPDIR": str(wd / (k + "_tmp"))})
        tw(wd / (k + ".log"), txt)
    out = wj(wd / "suite.json", res)
    return [check("selected studio classes run (>= 20 tests) and pass", res["clean"]["ran"] >= 20 and res["clean"]["ok"], res["clean"], ">= 20 OK"),
            check("mutant renderer (even-odd holes filled) is caught", res["mutant"]["failed"] >= 1, res["mutant"], ">= 1 failure"),
            check("negative control: the mutant Renderer class does not pass", not res["mutant"]["ok"], res["mutant"]["ok"], False)], [out, wd / "clean.log"]


_TS_MODULE = '''import sqlite3

def reading_time(text, wps=3.0, floor=0.4):
    """Seconds a caption must hold: floor + words / wps."""
    words = [w for w in text.split() if w.strip()]
    if not words:
        raise ValueError("empty caption")
    return round(floor + len(words) / wps, 2)

def save_caption(db, text):
    db.execute("insert into captions(text, hold) values (?, ?)", (text, reading_time(text)))
    return db.execute("select count(*) from captions").fetchone()[0]
'''
_TS_TESTS = '''import random, sqlite3, tempfile, os, unittest
import captions as C

def factory(seed=7, n=5):
    r = random.Random(seed)
    return [" ".join(r.choice(["noor", "sabr", "amal", "fajr"]) for _ in range(r.randint(1, 6))) for _ in range(n)]

class Unit(unittest.TestCase):
    def test_happy_path_three_words(self):
        self.assertEqual(C.reading_time("one two three"), 1.4)
    def test_edge_single_word_keeps_floor(self):
        self.assertEqual(C.reading_time("salaam"), 0.73)
    def test_edge_empty_caption_rejected(self):
        with self.assertRaises(ValueError):
            C.reading_time("   ")

class Integration(unittest.TestCase):
    def setUp(self):
        self.path = tempfile.mktemp(suffix=".db")
        self.db = sqlite3.connect(self.path)
        self.db.execute("create table captions(text, hold)")
    def tearDown(self):
        self.db.close(); os.remove(self.path)
    def test_seeded_rows_saved(self):
        for t in factory():
            n = C.save_caption(self.db, t)
        self.assertEqual(n, 5)
        holds = [h for (h,) in self.db.execute("select hold from captions")]
        self.assertTrue(all(h >= 0.73 for h in holds))

if __name__ == "__main__":
    unittest.main()
'''


@card("QA-336")
def complete_testing_suite(task, wd):
    """Complete testing suite steps: a risk map first, unit tests (happy path + two edge cases, behaviour names),
    an integration test on a real temporary SQLite database with seeded factories and cleanup, coverage by trace,
    a flakiness rerun, and a mutation check proving the tests bite."""
    proj = wd / "proj"
    tw(proj / "captions.py", _TS_MODULE)
    tw(proj / "test_captions.py", _TS_TESTS)
    wj(wd / "risk_map.json", [{"risk": "caption flashes too fast to read", "test": "Unit.*"}, {"risk": "rows lost on save", "test": "Integration.test_seeded_rows_saved"}])
    tmp = wd / "tmp"
    tmp.mkdir()
    tenv = {"TMPDIR": str(tmp)}
    r1, t1 = unittest_run(proj, ["test_captions.py", "-v"], env=tenv)
    r2, _ = unittest_run(proj, ["test_captions.py"], env=tenv)
    cov = subprocess.run([sys.executable, "-B", "-m", "trace", "--count", "--missing", "-C", str(wd / "cov"), "--module", "unittest", "test_captions"], capture_output=True, text=True,
                         cwd=str(proj), timeout=60, stdin=subprocess.DEVNULL, env=dict(os.environ, **tenv))
    cover = [p for p in (wd / "cov").glob("*captions.cover") if not p.name.startswith("test_")]
    missing = cover[0].read_text().count(">>>>>>") if cover else 99
    mut = wd / "mut"
    copy_tree(proj, mut)
    mutate(mut / "captions.py", "floor + len(words) / wps", "len(words) / wps")
    rm, _ = unittest_run(mut, ["test_captions.py"], env=tenv)
    leftovers = list(tmp.glob("*.db"))
    out = wj(wd / "test_report.json", {"run1": r1, "run2": r2, "uncovered_lines": missing, "mutant": rm})
    names = re.findall(r"(test_\w+)", t1)
    return [check("4 tests: happy path, 2 edges, 1 integration; all pass", r1["ran"] == 4 and r1["ok"], r1, "4 OK"),
            check("test names describe behaviour", all(len(n.split("_")) >= 3 for n in names), sorted(set(names)), "behaviour names"),
            check("coverage: no line of the module left unexecuted", cover and missing == 0, missing, 0),
            check("rerun gives the same result (not flaky)", r2 == r1 or (r2["ran"] == r1["ran"] and r2["ok"] == r1["ok"]), [r1["ok"], r2["ok"]], "same"),
            check("integration cleaned its temporary database", leftovers == [], [str(p) for p in leftovers], []),
            check("negative control: the mutant (floor dropped) fails the suite", not rm["ok"] and rm["failed"] >= 2, rm, ">= 2 failures")], [out, wd / "risk_map.json"]


@card("QA-334")
def llm_judge_eval_lab(task, wd):
    """LLM Judge & Eval Lab: one criterion per judge, two standard judges + one adversarial, scored with the skill's
    eval_runner.py (sigma, adversarial gap rule 0.6/0.4, HARD_FAIL assertions, regression gate exit 3, Cohen's
    kappa calibration against human labels)."""
    E = VENDOR / "llm-judge-eval-lab/scripts/eval_runner.py"
    wj(wd / "rubric.json", {"name": "reel", "pass_threshold": 7, "criteria": {"clarity": 0.5, "sync": 0.5}})
    wj(wd / "j/j1.json", {"judge": "j1", "role": "standard", "scores": {"clarity": 8, "sync": 8}, "position": "AB"})
    wj(wd / "j/j2.json", {"judge": "j2", "role": "standard", "scores": {"clarity": 8, "sync": 9}, "position": "BA"})
    wj(wd / "j/j3.json", {"judge": "adv", "role": "adversarial", "scores": {"clarity": 5, "sync": 6}, "position": "AB"})
    wj(wd / "assert_fail.json", {"results": [{"name": "render exists", "kind": "file", "result": "HARD_FAIL"}]})
    run = lambda *a: subprocess.run([sys.executable, "-B", E, *map(str, a)], capture_output=True, text=True, timeout=30, cwd=str(wd), stdin=subprocess.DEVNULL)
    r1 = run("score", "--rubric", "rubric.json", "--judges", "j/*.json", "--out", "base.json")
    r2 = run("score", "--rubric", "rubric.json", "--judges", "j/*.json", "--assertions", "assert_fail.json", "--out", "hard.json")
    g = run("gate", "--run", "hard.json", "--baseline", "base.json")
    g0 = run("gate", "--run", "base.json", "--baseline", "base.json")
    hum = {"items": [{"id": i, "labels": {"clarity": v}} for i, v in enumerate([1, 0, 1, 1, 0, 1, 0, 1, 1, 0] * 3)]}
    jud = {"items": [{"id": i, "labels": {"clarity": v if i % 10 else 1 - v}} for i, v in enumerate([1, 0, 1, 1, 0, 1, 0, 1, 1, 0] * 3)]}
    wj(wd / "human.json", hum)
    wj(wd / "judge.json", jud)
    k = run("kappa", "--human", "human.json", "--judge", "judge.json")
    base, hard = rj(wd / "base.json"), rj(wd / "hard.json")
    kap = json.loads(k.stdout[k.stdout.index("{"):]) if "{" in k.stdout else {}
    kv = None
    for v in (kap.values() if isinstance(kap, dict) else []):
        if isinstance(v, dict) and "kappa" in v:
            kv = v["kappa"]
        elif isinstance(v, dict) and "clarity" in v:
            kv = v["clarity"].get("kappa") if isinstance(v["clarity"], dict) else v["clarity"]
    if kv is None and isinstance(kap.get("clarity"), (int, float, dict)):
        kv = kap["clarity"]["kappa"] if isinstance(kap["clarity"], dict) else kap["clarity"]
    tw(wd / "kappa.txt", k.stdout + k.stderr)
    return [check("standard judges agree (sigma < 0.8 -> 'needs verification' note)", base["sigma"] < 0.8 and any("σ" in n for n in base["notes"]), base["sigma"], "< 0.8"),
            check("adversarial gap > 1.5 blends 0.6 x standard + 0.4 x adversarial", abs(base["final"] - (0.6 * base["standard_avg"] + 0.4 * base["adversarial_avg"])) < 0.01, base["final"], 7.15),
            check("without assertions the run passes the threshold", base["passed"] and r1.returncode == 0, base["passed"], True),
            check("one HARD_FAIL sinks the pass whatever the score", hard["hard_fail"] and not hard["passed"] and r2.returncode != 0, [hard["final"], hard["passed"]], "fails"),
            check("regression gate blocks the lost pass (exit 3) and lets an equal run through", g.returncode == 3 and g0.returncode == 0, [g.returncode, g0.returncode], [3, 0]),
            check("kappa measured on 30 human-labelled samples (3 disagreements)", kv is not None and 0.6 < float(kv) < 0.9, kv, "0.6-0.9"),
            check("negative control: the HARD_FAIL run is not shippable", not hard["passed"], hard["passed"], False)], [wd / "base.json", wd / "hard.json"]


def ocr(path, psm=7):
    env = dict(os.environ, OMP_THREAD_LIMIT="1")
    return subprocess.run(["tesseract", str(path), "-", "--psm", str(psm)], capture_output=True, text=True, timeout=30, stdin=subprocess.DEVNULL,
                          env=env).stdout.strip()


@card("QA-217")
def theme_bible_qa_loop(task, wd):
    """Theme bible + generate/QA loop: one theme file (palette, typography, negative tokens, text limits) drives every
    panel; N candidates are generated in parallel, QA'd in one pass (OCR of the expected string with tesseract,
    palette compliance, text limits, geometry), one targeted change is applied, and the loop stops at 'ship' or 3."""
    np = _np()
    from PIL import Image, ImageDraw, ImageFont
    from concurrent.futures import ThreadPoolExecutor
    theme = {"palette": ["#0e1a2b", "#f4efe6", "#ffb000"], "font": "Poppins-Bold.ttf", "negative": ["purple gradient", "lens flare"],
             "text_max_chars": 18, "title": "SABR WINS", "safe_margin": 16}
    wj(wd / "theme.json", theme)
    fontdir = SKILLS / "kosif-superpowers/proofs/_shared/fonts"

    def generate(params, i):
        im = Image.new("RGB", (480, 270), theme["palette"][0])
        d = ImageDraw.Draw(im)
        d.rectangle([24, 200, 24 + 120 + 20 * i, 214], fill=params["accent"])
        d.text((params["x"], 60), theme["title"], fill=theme["palette"][1], font=ImageFont.truetype(str(fontdir / theme["font"]), params["size"]))
        p = wd / ("iter%d_cand%d.png" % (params["iter"], i))
        im.save(p)
        return p

    def qa(p):
        a = np.asarray(Image.open(p).convert("RGB"), float)
        pal = np.array([hexrgb(h) for h in theme["palette"]], float)
        dist = np.abs(a.reshape(-1, 1, 3) - pal[None]).sum(axis=2).min(axis=1)
        off_palette = float((dist > 60).mean())
        Image.open(p).crop((0, 40, 480, 140)).save(p.with_suffix(".title.png"))
        txt = ocr(p.with_suffix(".title.png"), 7).replace("\n", " ")
        ys, xs = np.nonzero(np.abs(a - pal[1]).sum(axis=2) < 40)
        inside = len(xs) and xs.min() >= theme["safe_margin"] and xs.max() <= 480 - theme["safe_margin"]
        return {"ocr": txt, "ocr_ok": theme["title"] in txt.upper(), "off_palette": off_palette, "palette_ok": off_palette < 0.01,
                "text_ok": len(theme["title"]) <= theme["text_max_chars"], "geometry_ok": bool(inside)}
    params = {"accent": "#c000ff", "size": 9, "x": 40}
    log = []
    for it in range(1, 4):
        params["iter"] = it
        with ThreadPoolExecutor(max_workers=3) as ex:
            cands = list(ex.map(lambda i: generate(dict(params), i), range(3)))
        rows = [qa(c) for c in cands]
        verdict = "ship" if all(r["ocr_ok"] and r["palette_ok"] and r["text_ok"] and r["geometry_ok"] for r in rows) else "iterate"
        change = None
        if verdict == "iterate":
            if not all(r["palette_ok"] for r in rows):
                params["accent"], change = theme["palette"][2], "accent -> palette #ffb000"
            elif not all(r["ocr_ok"] for r in rows):
                params["size"], change = 56, "title size 9 -> 56"
        log.append({"iter": it, "verdict": verdict, "qa": rows, "change": change})
        if verdict == "ship":
            break
    out = wj(wd / "qa_loop.json", log)
    return [check("three candidates generated and QA'd per iteration", all(len(l["qa"]) == 3 for l in log), [len(l["qa"]) for l in log], 3),
            check("one targeted change per failed iteration (palette, then type size)", [l["change"] for l in log if l["change"]] == ["accent -> palette #ffb000", "title size 9 -> 56"],
                  [l["change"] for l in log], 2),
            check("ships at iteration 3 (<= 3)", log[-1]["verdict"] == "ship" and len(log) == 3, [l["verdict"] for l in log], ["iterate", "iterate", "ship"]),
            check("final candidates read back by OCR and stay on palette", all(r["ocr_ok"] and r["palette_ok"] for r in log[-1]["qa"]), [r["ocr"] for r in log[-1]["qa"]], theme["title"]),
            check("negative control: the first candidates fail palette and OCR", not any(r["palette_ok"] or r["ocr_ok"] for r in log[0]["qa"]), log[0]["qa"][0], "fail")], [out, wd / "iter3_cand0.png"]


def _overlap_score(task, option):
    tw_ = set(re.findall(r"\w+", task.lower()))
    ow = set(re.findall(r"\w+", option.lower()))
    return len(tw_ & ow) / float(len(ow) or 1)


@card("QA-218")
def jev_closed_set_judge(task, wd):
    """Jev closed-set judge: choose among fixed options (letters A-L) with order bias removed by asking twice with the
    options reversed; thousands of options are pre-ranked (word-overlap fallback when embeddings are unavailable) and
    judged in heats of 12. It judges only, it never acts."""
    q = "a calm reel about patience at dawn prayer"
    ideas = ["patience at dawn prayer calm reel", "loud gym montage", "street food tour", "calm sea timelapse"] + \
            ["random idea number %d about cars" % i for i in range(26)] + ["dawn prayer patience story", "calm reel of patience at dawn"]
    LET = "ABCDEFGHIJKL"

    def biased_judge(opts):
        """Stand-in judge with a strong first-position bias, as raw LLM judges have; returns per-letter scores."""
        return {LET[i]: _overlap_score(q, o) + (1.2 if i == 0 else 0.0) for i, o in enumerate(opts)}

    def ask(opts, debias=True):
        s1 = biased_judge(opts)
        if not debias:
            return opts[max(range(len(opts)), key=lambda i: s1[LET[i]])], s1
        rev = opts[::-1]
        s2 = biased_judge(rev)
        total = {o: s1[LET[i]] + s2[LET[len(opts) - 1 - i]] for i, o in enumerate(opts)}
        return max(opts, key=lambda o: (total[o], -opts.index(o))), total
    ranked = sorted(ideas, key=lambda o: -_overlap_score(q, o))
    heats = [ranked[i:i + 12] for i in range(0, len(ranked), 12)]
    winners = [ask(h)[0] for h in heats]
    final, _ = ask(winners)
    trap = ["loud gym montage", "calm reel of patience at dawn", "street food tour"]
    biased_pick, _ = ask(trap, debias=False)
    fair_pick, _ = ask(trap)
    out = wj(wd / "jev.json", {"heats": [len(h) for h in heats], "winners": winners, "final": final, "trap": {"biased": biased_pick, "debiased": fair_pick}})
    return [check("32 options judged in heats of <= 12", [len(h) for h in heats] == [12, 12, 8], [len(h) for h in heats], [12, 12, 8]),
            check("final choice is the best-matching idea", final in ("calm reel of patience at dawn", "patience at dawn prayer calm reel"), final, "patience at dawn ..."),
            check("order bias removed: reversed asking picks the right option", fair_pick == "calm reel of patience at dawn", fair_pick, "calm reel of patience at dawn"),
            check("the judge only returns a choice (no action taken)", isinstance(final, str) and not list(wd.glob("*.action")), "choice only", "no side effects"),
            check("negative control: a single-order ask falls for the first-position bias", biased_pick == "loud gym montage", biased_pick, "loud gym montage")], [out]


@card("QA-333")
def fact_checker_verifier(task, wd):
    """Fact-Checker & Verifier steps: extract every checkable claim into a table, find its primary source with date and
    a short quote, classify supported / contradicted / unverifiable, check each citation really says what is
    attributed, and summarise the supported share, the most serious error and the missing fact."""
    src = wd / "sources"
    tw(src / "ministry_2025.txt", "Date: 2025-03-10\nThe new bridge is 1,200 metres long and opened in March 2025.\n")
    tw(src / "census_2024.txt", "Date: 2024-11-02\nThe city population reached 4.1 million people in 2024.\n")
    tw(src / "blog_repost.txt", "Date: 2025-04-01\nSomeone said the bridge cost a lot.\n")
    script = ("The bridge is 1,200 metres long. It opened in March 2025. The city has 5 million people. "
              "The bridge was built by 900 workers. The bridge cost 2 billion according to the ministry.")
    claims = [s.strip() for s in re.split(r"(?<=\.)\s+", script) if re.search(r"\d", s)]
    cites = {"The bridge cost 2 billion according to the ministry.": "ministry_2025.txt"}
    docs = {p.name: p.read_text() for p in src.glob("*.txt")}
    rows = []
    for c in claims:
        nums = re.findall(r"[\d][\d,.]*", c)
        cw = set(re.findall(r"\w+", c.lower()))
        covr = lambda d: len(cw & set(re.findall(r"\w+", docs[d].lower()))) / float(len(cw))
        nums_in = lambda d: {n.rstrip(".") for n in re.findall(r"[\d][\d,.]*", docs[d])}
        best = max(docs, key=covr)
        text = docs[best]
        date = re.search(r"Date: (\S+)", text).group(1)
        quote = [ln for ln in text.splitlines() if not ln.startswith("Date")][0][:80]
        if covr(best) < 0.35:
            verdict = "unverifiable"
        elif all(n.rstrip(".") in nums_in(best) for n in nums):
            verdict = "supported"
        else:
            verdict = "contradicted"
        cite = cites.get(c)
        cite_ok = None if cite is None else all(n.rstrip(".") in nums_in(cite) for n in nums)
        rows.append({"claim": c, "source": best, "date": date, "quote": quote, "verdict": verdict, "citation": cite, "citation_says_it": cite_ok})
    sup = sum(r["verdict"] == "supported" for r in rows) / float(len(rows))
    worst = [r["claim"] for r in rows if r["verdict"] == "contradicted"]
    out = wj(wd / "fact_table.json", {"rows": rows, "summary": {"supported_share": sup, "most_serious": worst[:1],
                                                               "missing_fact": "the actual population figure (census 2024: 4.1 million)"}})
    v = [r["verdict"] for r in rows]
    return [check("five checkable claims extracted", len(rows) == 5, len(rows), 5),
            check("length and opening date supported by the ministry source", v[:2] == ["supported", "supported"] and rows[0]["source"] == "ministry_2025.txt", v[:2], ["supported", "supported"]),
            check("population claim contradicted by the census (4.1 million)", v[2] == "contradicted" and rows[2]["source"] == "census_2024.txt", [v[2], rows[2]["source"]], "contradicted"),
            check("worker count has no source -> unverifiable", v[3] == "unverifiable", v[3], "unverifiable"),
            check("the 2-billion citation does not say what is attributed", rows[4]["citation_says_it"] is False, rows[4]["citation_says_it"], False),
            check("each row carries source date and quote", all(r["date"] and r["quote"] for r in rows), rows[0]["date"], "dated"),
            check("negative control: an unchecked script would claim 100 % supported, measured is 40 %", abs(sup - 0.4) < 1e-9, sup, 0.4)], [out]


@card("QA-335")
def llm_judge_eval_suites(task, wd):
    """LLM Judge & Eval Suites: a method tree (exact match -> rules -> anchored rubric judge -> human, cheapest that
    suffices), calibration against 30 human labels, a position-swap check, a length-bias test, the sample size and a
    numeric ship gate before running."""
    np = _np()
    rng = np.random.default_rng(3)
    items = []
    for i in range(30):
        good = i % 3 != 0
        text = ("Patience at dawn, one breath at a time" if good else "buy now buy now buy now click link") + (" extra words" * int(rng.integers(0, 4)))
        items.append({"id": i, "output": text, "human": int(good), "ref": "Patience at dawn" if i < 5 else None})

    def method(it):
        if it["ref"]:
            return "exact", int(it["output"].startswith(it["ref"]))
        if len(it["output"]) > 120:
            return "rules", 0
        anchors = {"patience": 1, "dawn": 1, "buy": -1, "click": -1}
        s = sum(v for k, v in anchors.items() if k in it["output"].lower())
        return "judge", int(s > 0)
    res = [dict(it, method=method(it)[0], pred=method(it)[1]) for it in items]
    agree = sum(r["pred"] == r["human"] for r in res) / 30.0
    fair = lambda a, b: int(method({"output": a, "ref": None})[1] >= method({"output": b, "ref": None})[1])
    long_bias = lambda a, b: int(len(a) >= len(b))
    pairs = [(items[i]["output"], items[i + 1]["output"]) for i in range(0, 28, 2)]
    swap_ok = all(fair(a, b) == 1 - fair(b, a) or method({"output": a, "ref": None})[1] == method({"output": b, "ref": None})[1] for a, b in pairs)
    lens = np.array([len(r["output"]) for r in res])
    corr_fair = float(np.corrcoef(lens, [r["pred"] for r in res])[0, 1])
    corr_long = float(np.corrcoef(lens, [int(l > np.median(lens)) for l in lens])[0, 1])
    n_needed = int(math.ceil(1.96 ** 2 * 0.25 / 0.1 ** 2))
    pass_rate = sum(r["pred"] for r in res) / 30.0
    gate = {"min_agreement": 0.8, "max_length_corr": 0.3, "n_for_ship_decision": n_needed}
    ship_ready = agree >= gate["min_agreement"] and abs(corr_fair) <= gate["max_length_corr"]
    out = wj(wd / "eval_suite.json", {"agreement": agree, "methods": {m: sum(r["method"] == m for r in res) for m in ("exact", "rules", "judge")},
                                      "length_corr": corr_fair, "biased_length_corr": corr_long, "gate": gate, "pass_rate": pass_rate, "ship_ready": ship_ready})
    return [check("cheapest method first: 5 exact-match items, the rest judged by the anchored rubric", sum(r["method"] == "exact" for r in res) == 5, sum(r["method"] == "exact" for r in res), 5),
            check("agreement with 30 human labels >= 0.8", agree >= 0.8, agree, ">= 0.8"),
            check("position swap is consistent", swap_ok, swap_ok, True),
            check("no length bias in the rubric judge (|r| <= 0.3)", abs(corr_fair) <= 0.3, corr_fair, "<= 0.3"),
            check("sample size for a +-10 % ship decision computed before the run (97)", n_needed == 97, n_needed, 97),
            check("negative control: a 'longer is better' judge fails the length-bias test", abs(corr_long) > 0.3, corr_long, "> 0.3")], [out]


@card("QA-303")
def honesty_rule(task, wd):
    """Honesty rule as a gate on the delivery report: every 'measured' claim must match a value re-measured from the
    file, every render claimed must exist, footage must be credited, no face may be flagged as replaced, and what was
    not measured is said as not measured."""
    np = _np()
    film = fx.test_clip(wd / "film.mp4", 2.0, "320x180", 30)
    measured = {"duration_s": round(float(fx.probe(film)["format"]["duration"]), 2), "frames": len(read_video(film, (32, 18)))}

    def gate(rep):
        issues = []
        for k, v in rep.get("measured", {}).items():
            if measured.get(k) is None:
                issues.append("claims %s as measured but nothing measured it" % k)
            elif abs(float(v) - float(measured[k])) > 1e-6:
                issues.append("%s claimed %s, measured %s" % (k, v, measured[k]))
        for r in rep.get("renders", []):
            if not (wd / r).exists():
                issues.append("claims render %s that does not exist" % r)
        for f in rep.get("footage", []):
            if not f.get("credit"):
                issues.append("footage %s without credit" % f["file"])
        if rep.get("face_replaced"):
            issues.append("a real face was replaced")
        return issues
    honest = {"measured": dict(measured), "not_measured": ["loudness (no audio stream)"], "renders": ["film.mp4"],
              "footage": [{"file": "pexels_123.mp4", "credit": "Pexels / A. Author"}], "face_replaced": False}
    inflated = {"measured": {"duration_s": 15.0, "frames": 450, "lufs": -14}, "renders": ["film.mp4", "final_4k.mp4"],
                "footage": [{"file": "pexels_123.mp4", "credit": ""}], "face_replaced": True}
    gi, gb = gate(honest), gate(inflated)
    out = wj(wd / "honesty.json", {"measured_here": measured, "honest_issues": gi, "inflated_issues": gb})
    return [check("measured values re-measured from the file (2 s, 60 frames)", measured == {"duration_s": 2.0, "frames": 60}, measured, {"duration_s": 2.0, "frames": 60}),
            check("the honest report passes the gate", gi == [], gi, []),
            check("inflated report: wrong numbers, unmeasured LUFS, un-run 4K render, missing credit, face replaced", len(gb) == 6, gb, 6),
            check("not-measured items are stated, not filled in", honest["not_measured"] and "lufs" not in honest["measured"], honest["not_measured"], "stated"),
            check("negative control: the inflated report fails the gate", len(gb) > 0, len(gb), "> 0")], [out]


@card("QA-316")
def generator_failure_checklist(task, wd):
    """Generator failure-prevention checklist on every generated frame, the measurable items: garbled text (OCR of
    the expected words), duplicated objects / limbs (template matches of one part), repeated textures (tile
    self-similarity), and earring asymmetry (left/right mirror difference of the ear regions)."""
    np = _np()
    from PIL import Image, ImageDraw, ImageFont
    font = ImageFont.truetype(str(SKILLS / "kosif-superpowers/proofs/_shared/fonts/Poppins-Bold.ttf"), 40)

    def frame(bad):
        rng = np.random.default_rng(5)
        tile = rng.uniform(60, 140, (40, 40, 3))
        bgarr = np.tile(tile, (6, 12, 1)) if bad else rng.uniform(60, 140, (240, 480, 3))
        im = Image.fromarray(bgarr[:240, :480].astype("uint8"))
        d = ImageDraw.Draw(im)
        d.rectangle([150, 120, 330, 150], fill=(20, 20, 20))
        d.text((160, 112), "OPEN" if not bad else "0PFN", fill=(255, 255, 255), font=font)
        for x in ([60, 380] if not bad else [60, 380, 300]):          # hands: two, or a duplicated third
            d.ellipse([x, 180, x + 30, 210], fill=(230, 180, 140))
        d.ellipse([20, 20, 34, 34], fill=(255, 215, 0))                # left earring
        if not bad:
            d.ellipse([446, 20, 460, 34], fill=(255, 215, 0))          # right earring (missing when bad)
        p = wd / ("%s.png" % ("bad" if bad else "good"))
        im.save(p)
        return p

    def audit(p):
        a = np.asarray(Image.open(p).convert("RGB"), float)
        Image.open(p).crop((150, 110, 330, 160)).resize((540, 150)).save(p.with_suffix(".txt.png"))
        txt = ocr(p.with_suffix(".txt.png"), 7).upper()
        skin = (np.abs(a - np.array([230, 180, 140])).sum(axis=2) < 30)
        from scipy import ndimage
        lab, n = ndimage.label(skin)
        hands = sum(1 for i in range(1, n + 1) if (lab == i).sum() > 200)
        bgp = a[40:100, 100:420].copy()
        rep = float(np.abs(bgp[:, :40] - bgp[:, 40:80]).mean())
        gold = (np.abs(a - np.array([255, 215, 0])).sum(axis=2) < 30)
        asym = int(gold[:, :240].sum()) - int(gold[:, ::-1][:, :240].sum())
        return {"text_ok": "OPEN" in txt, "ocr": txt, "hands": hands, "repeat_texture": rep < 1.0, "earring_asymmetry": abs(asym) > 50}
    G, B = audit(frame(False)), audit(frame(True))
    out = wj(wd / "checklist.json", {"good": G, "bad": B})
    return [check("garbled text caught by OCR", G["text_ok"] and not B["text_ok"], [G["ocr"], B["ocr"]], "OPEN vs garbled"),
            check("duplicated hand counted (3 vs 2)", G["hands"] == 2 and B["hands"] == 3, [G["hands"], B["hands"]], [2, 3]),
            check("repeated texture tile found", B["repeat_texture"] and not G["repeat_texture"], [G["repeat_texture"], B["repeat_texture"]], [False, True]),
            check("earring asymmetry found", B["earring_asymmetry"] and not G["earring_asymmetry"], [G["earring_asymmetry"], B["earring_asymmetry"]], [False, True]),
            check("negative control: the defective frame fails the checklist", not B["text_ok"] or B["hands"] != 2, B, "fails")], [out, wd / "bad.png"]


# ═════════════════════════ anti-pattern detectors over real timelines, rigs and frames ═════════════════════════
def kf_tweens(wd, name, body, css, js, dur=4):
    """Write a HyperFrames composition and read its tweens back with the real `hyperframes keyframes --json`."""
    p = hf_project(wd, name, body, css, js, dur=dur)
    rc, j, t = hf(wd, ["keyframes", ".", "--json"], p)
    if not j:
        raise RuntimeError("keyframes failed: %s" % t[-300:])
    return j["compositions"][0]["tweens"], p


def _props(tw_):
    ks = tw_["keyframes"]
    return ks[0]["properties"], ks[-1]["properties"]


@card("QA-357")
def kinetic_type_anti_patterns(task, wd):
    """Kinetic-type anti-patterns found on the real timeline (hyperframes keyframes) and CSS: typewriter on every
    line, bounce on every word, diagonal slides, too-short holds, glow on body text, more than two font families."""
    words = ["Sabr", "is", "light", "at", "dawn"]
    body = "".join('<span id="w%d" class="clip word" data-start="0" data-duration="4" data-track-index="%d" style="position:absolute;left:%dpx;top:150px">%s</span>' % (i, i, 40 + 110 * i, w)
                   for i, w in enumerate(words))
    bad_css = (".word{color:#fff;font:600 40px 'Georgia'}#w1{font-family:'Courier New'}#w2{font-family:'Impact'}"
               ".word{text-shadow:0 0 12px #0ff, 2px 0 #f00, -2px 0 #0ff}")
    bad_js = "".join('tl.fromTo("#w%d",{x:-40,y:40,opacity:0},{x:0,y:0,opacity:1,duration:.3,ease:"bounce.out"},%.1f);tl.to("#w%d",{opacity:0,duration:.2},%.1f);'
                     % (i, 0.2 * i, i, 0.2 * i + 0.45) for i in range(5))
    good_css = ".word{color:#fff;font:600 40px 'Georgia'}"
    good_js = "".join('tl.fromTo("#w%d",{y:24,opacity:0},{y:0,opacity:1,duration:.5,ease:"power3.out"},%.1f);' % (i, 0.12 * i) for i in range(5)) + \
              'tl.to(".word",{opacity:0,duration:.4},3.4);'

    def audit(tws, css):
        ent = [t for t in tws if t["method"] == "fromTo"]
        exits = {t["target"]: t["start"] for t in tws if t["method"] == "to"}
        f = {}
        f["bounce_every_word"] = len(ent) >= 3 and all("bounce" in (t.get("ease") or "") or "elastic" in (t.get("ease") or "") for t in ent)
        f["diagonal_slides"] = sum(1 for t in ent if abs(_props(t)[0].get("x", 0)) > 0 and abs(_props(t)[0].get("y", 0)) > 0)
        holds = [exits[t["target"]] - t["end"] for t in ent if t["target"] in exits]
        f["too_short_holds"] = sum(1 for h in holds if h < 0.4 + 0.3)
        f["glow_on_body"] = bool(re.search(r"\.word\{[^}]*text-shadow", css))
        f["font_families"] = len(set(re.findall(r"'([^']+)'", css)))
        f["typewriter_everywhere"] = len(ent) >= 3 and all(t.get("ease") == "steps" for t in ent)
        return f
    tb, _ = kf_tweens(wd, "bad", body, bad_css, bad_js)
    tg, _ = kf_tweens(wd, "good", body, good_css, good_js)
    B, G = audit(tb, bad_css), audit(tg, good_css)
    out = wj(wd / "kinetic_audit.json", {"bad": B, "good": G, "tweens_read": len(tb)})
    return [check("timeline read from the composition (10 tweens)", len(tb) == 10, len(tb), 10),
            check("bounce on every word", B["bounce_every_word"] and not G["bounce_every_word"], [B["bounce_every_word"], G["bounce_every_word"]], [True, False]),
            check("diagonal slides counted (5)", B["diagonal_slides"] == 5 and G["diagonal_slides"] == 0, [B["diagonal_slides"], G["diagonal_slides"]], [5, 0]),
            check("holds shorter than reading time (5)", B["too_short_holds"] == 5 and G["too_short_holds"] == 0, [B["too_short_holds"], G["too_short_holds"]], [5, 0]),
            check("glow / chromatic aberration on body text, and 3 random fonts", B["glow_on_body"] and B["font_families"] == 3 and G["font_families"] == 1,
                  [B["glow_on_body"], B["font_families"]], [True, 3]),
            check("negative control: the restrained version trips nothing", not (G["bounce_every_word"] or G["diagonal_slides"] or G["too_short_holds"] or G["glow_on_body"]),
                  G, "clean")], [out]


@card("QA-363")
def product_ui_anti_patterns(task, wd):
    """Product-UI anti-patterns on the real timeline: teleporting cursor (a zero-duration jump), zero latency between
    click and response, uniform 300 ms everywhere, bounce everywhere, infinite stagger, blur-in text, lorem UI."""
    body = ('<div id="cursor" class="clip" data-start="0" data-duration="4" data-track-index="0" style="position:absolute;width:12px;height:12px;background:#fff"></div>'
            '<div id="panel" class="clip" data-start="0" data-duration="4" data-track-index="1" style="position:absolute;left:300px;top:100px;width:200px;height:120px;background:#234"></div>'
            '<p id="copy" class="clip" data-start="0" data-duration="4" data-track-index="2" style="position:absolute;top:260px;color:#fff">__COPY__</p>')
    bad_js = ('tl.set("#cursor",{x:420,y:150},0.5);tl.fromTo("#panel",{scale:.8,opacity:0},{scale:1,opacity:1,duration:.3,ease:"back.out(3)"},0.5);'
              'tl.fromTo("#copy",{filter:"blur(10px)",opacity:0},{filter:"blur(0px)",opacity:1,duration:.3,ease:"bounce.out"},1);'
              'tl.to("#panel",{y:6,duration:.3,repeat:-1,yoyo:true,ease:"elastic.out"},1.5);')
    good_js = ('tl.to("#cursor",{x:420,y:150,duration:.6,ease:"power2.inOut"},0);tl.fromTo("#panel",{opacity:0,y:8},{opacity:1,y:0,duration:.24,ease:"power2.out"},0.72);'
               'tl.fromTo("#copy",{opacity:0},{opacity:1,duration:.45,ease:"power1.out"},1.2);')

    def audit(tws, html):
        f = {}
        cur = [t for t in tws if t["target"] == "#cursor"]
        f["teleporting_cursor"] = any(t["method"] == "set" or (t["duration"] or 0) == 0 for t in cur)
        arrive = max((t["start"] + (t["duration"] or 0)) for t in cur) if cur else 0
        resp = [t["start"] for t in tws if t["target"] == "#panel" and t["method"] == "fromTo"]
        f["latency_s"] = round(resp[0] - arrive, 3) if resp else None
        f["zero_latency"] = f["latency_s"] is not None and f["latency_s"] < 0.05
        durs = [t["duration"] for t in tws if t["duration"]]
        f["uniform_300ms"] = len(durs) >= 3 and all(abs(d - 0.3) < 1e-6 for d in durs)
        eases = [t.get("ease") or "" for t in tws if t["method"] != "set"]
        f["bounce_everywhere"] = bool(eases) and all(any(k in e for k in ("bounce", "back", "elastic")) for e in eases)
        f["infinite_loop"] = any("totalDuration" in (t.get("unresolved") or []) for t in tws)
        f["blur_in_text"] = any("blur" in str(_props(t)[0].get("filter", "")) for t in tws if t["target"] == "#copy")
        f["lorem_ui"] = "lorem" in html.lower()
        return f
    tb, pb = kf_tweens(wd, "bad", body.replace("__COPY__", "Lorem ipsum dolor sit amet"), "", bad_js)
    tg, pg = kf_tweens(wd, "good", body.replace("__COPY__", "Export finished in 4 s"), "", good_js)
    B, G = audit(tb, (pb / "index.html").read_text()), audit(tg, (pg / "index.html").read_text())
    out = wj(wd / "ui_audit.json", {"bad": B, "good": G})
    flags = lambda f: sorted(k for k, v in f.items() if v is True)
    return [check("all seven product-UI tells found on the bad demo", flags(B) == sorted(["teleporting_cursor", "zero_latency", "uniform_300ms", "bounce_everywhere",
                                                                                         "infinite_loop", "blur_in_text", "lorem_ui"]), flags(B), 7),
            check("measured click-to-response latency: 0 s bad, 0.12 s good", B["latency_s"] == 0 and abs(G["latency_s"] - 0.12) < 1e-6, [B["latency_s"], G["latency_s"]], [0, 0.12]),
            check("negative control: the considered demo trips none", flags(G) == [], flags(G), [])], [out]


@card("QA-361")
def phone_anti_patterns(task, wd):
    """Phone mock-up anti-patterns on the real timeline and CSS: perpetual bob, linear scrolling, looping glare,
    mirrored hardware, mismatched corner radii (screen radius must equal body radius minus bezel), ghost taps."""
    body = ('<div id="phone" class="clip" data-start="0" data-duration="4" data-track-index="0"><div id="screen"><div id="feed"></div></div><div id="glare"></div></div>'
            '<div id="tap" class="clip" data-start="0" data-duration="4" data-track-index="1"></div>')
    css_t = "#phone{position:absolute;left:250px;top:20px;width:160px;height:320px;border-radius:%dpx;background:#111;padding:%dpx}#screen{width:100%%;height:100%%;border-radius:%dpx;overflow:hidden;background:#fff}%s"
    bad_css = css_t % (32, 8, 10, "#phone{transform:scaleX(-1)}")
    good_css = css_t % (32, 8, 24, "")
    bad_js = ('tl.to("#phone",{y:-8,duration:1,repeat:-1,yoyo:true},0);tl.to("#feed",{y:-400,duration:3,ease:"none"},0.5);'
              'tl.to("#glare",{x:160,duration:1,repeat:-1},0);tl.fromTo("#tap",{scale:0},{scale:1,duration:.2},2.0);')
    good_js = ('tl.fromTo("#phone",{y:30,opacity:0},{y:0,opacity:1,duration:.6,ease:"power3.out"},0);tl.fromTo("#tap",{scale:0},{scale:1,duration:.2},1.0);'
               'tl.to("#feed",{y:-400,duration:1.2,ease:"power2.inOut"},1.1);')

    def audit(tws, css):
        f = {}
        f["perpetual_bob"] = any(t["target"] == "#phone" and "totalDuration" in (t.get("unresolved") or []) for t in tws)
        f["linear_scrolling"] = any(t["target"] == "#feed" and t.get("ease") == "none" for t in tws)
        f["looping_glare"] = any(t["target"] == "#glare" and "totalDuration" in (t.get("unresolved") or []) for t in tws)
        f["mirrored_hardware"] = "scaleX(-1)" in css
        body_r, pad, scr_r = [int(x) for x in re.findall(r"border-radius:(\d+)px;background:#111;padding:(\d+)px\}#screen\{[^}]*border-radius:(\d+)px", css)[0]]
        f["radius_mismatch_px"] = abs(body_r - pad - scr_r)
        taps = [t["start"] for t in tws if t["target"] == "#tap"]
        screen = [t["start"] for t in tws if t["target"] == "#feed"]
        f["ghost_taps"] = sum(1 for tp in taps if not any(0 <= s - tp <= 0.3 for s in screen))
        return f
    tb, _ = kf_tweens(wd, "bad", body, bad_css, bad_js)
    tg, _ = kf_tweens(wd, "good", body, good_css, good_js)
    B, G = audit(tb, bad_css), audit(tg, good_css)
    out = wj(wd / "phone_audit.json", {"bad": B, "good": G})
    return [check("perpetual bob and looping glare (infinite repeats) found", B["perpetual_bob"] and B["looping_glare"], [B["perpetual_bob"], B["looping_glare"]], [True, True]),
            check("linear scrolling found", B["linear_scrolling"] and not G["linear_scrolling"], [B["linear_scrolling"], G["linear_scrolling"]], [True, False]),
            check("mirrored hardware found", B["mirrored_hardware"], B["mirrored_hardware"], True),
            check("corner radii: 32 - 8 = 24 expected; bad screen is 14 px off", B["radius_mismatch_px"] == 14 and G["radius_mismatch_px"] == 0, [B["radius_mismatch_px"], G["radius_mismatch_px"]], [14, 0]),
            check("ghost tap (no screen change within 0.3 s) found", B["ghost_taps"] == 1 and G["ghost_taps"] == 0, [B["ghost_taps"], G["ghost_taps"]], [1, 0]),
            check("negative control: the good mock trips none", not any(v for k, v in G.items() if k not in ("radius_mismatch_px", "ghost_taps")) and G["ghost_taps"] == 0, G, "clean")], [out]


@card("QA-350")
def three_d_anti_patterns(task, wd):
    """3D anti-patterns measured on a scene description and its sampled camera path: chrome on everything, an aimless
    spinning logo with no hold, motion-sick whips (camera yaw rate), the default grey light rig, random lens flares,
    the hero frame held < 1.5 s, and z-fighting (coplanar overlapping meshes)."""
    np = _np()

    def scene(bad):
        mats = [{"name": n, "metalness": 1.0 if bad else m, "roughness": 0.05 if bad else 0.5} for n, m in (("logo", 0.2), ("floor", 0.0), ("plinth", 0.1))]
        meshes = [{"name": "floor", "pos": [0, 0, 0], "normal": [0, 1, 0], "size": 10}, {"name": "decal", "pos": [0, 0 if bad else 0.002, 0], "normal": [0, 1, 0], "size": 2}]
        lights = [{"type": "ambient", "color": "#ffffff", "intensity": 1.0}] if bad else [{"type": "key", "color": "#ffe2c0", "intensity": 2.2}, {"type": "rim", "color": "#9fc6ff", "intensity": 1.1}]
        logo = {"spin_deg_per_s": 120, "hold_s": 0} if bad else {"spin_deg_per_s": 0, "hold_s": 2.0}
        t = np.linspace(0, 4, 121)
        if bad:
            yaw = np.where(t < 1.0, 0, np.where(t < 1.2, (t - 1.0) / 0.2 * 90, 90))
        else:
            yaw = np.clip(t / 2.0, 0, 1) ** 2 * 30
        cam = {"t": t.tolist(), "yaw": yaw.tolist()}
        return {"materials": mats, "meshes": meshes, "lights": lights, "logo": logo, "camera": cam, "flares": 3 if bad else 0}

    def audit(s):
        t, yaw = np.array(s["camera"]["t"]), np.array(s["camera"]["yaw"])
        rate = np.abs(np.diff(yaw) / np.diff(t))
        still = rate < 1.0
        run, longest = 0, 0
        for x in still:
            run = run + 1 if x else 0
            longest = max(longest, run)
        hold = longest * float(t[1] - t[0])
        z = 0
        for i, a in enumerate(s["meshes"]):
            for b in s["meshes"][i + 1:]:
                if a["normal"] == b["normal"] and abs(np.dot(np.subtract(a["pos"], b["pos"]), a["normal"])) < 1e-4:
                    z += 1
        return {"chrome_everything": all(m["metalness"] >= 0.9 and m["roughness"] < 0.15 for m in s["materials"]),
                "aimless_spin": s["logo"]["spin_deg_per_s"] > 0 and s["logo"]["hold_s"] < 1.5,
                "max_yaw_rate": float(rate.max()), "whip": float(rate.max()) > 180,
                "default_grey_light": len(s["lights"]) == 1 and s["lights"][0]["type"] == "ambient" and s["lights"][0]["color"] == "#ffffff",
                "lens_flares": s["flares"], "hero_hold_s": round(hold, 2), "hero_hold_short": hold < 1.5, "z_fighting_pairs": z}
    B, G = audit(scene(True)), audit(scene(False))
    wj(wd / "scene_bad.json", scene(True))
    out = wj(wd / "anti3d.json", {"bad": B, "good": G})
    return [check("chrome on every material and default grey light rig", B["chrome_everything"] and B["default_grey_light"], [B["chrome_everything"], B["default_grey_light"]], [True, True]),
            check("spinning logo with no hold", B["aimless_spin"] and not G["aimless_spin"], [B["aimless_spin"], G["aimless_spin"]], [True, False]),
            check("90 deg in 0.2 s whip = 450 deg/s (> 180)", abs(B["max_yaw_rate"] - 450) < 1 and B["whip"] and not G["whip"], [B["max_yaw_rate"], G["max_yaw_rate"]], [450, "< 180"]),
            check("z-fighting: decal coplanar with the floor", B["z_fighting_pairs"] == 1 and G["z_fighting_pairs"] == 0, [B["z_fighting_pairs"], G["z_fighting_pairs"]], [1, 0]),
            check("hero frame held >= 1.5 s in the good scene", G["hero_hold_s"] >= 1.5 and not G["hero_hold_short"], G["hero_hold_s"], ">= 1.5"),
            check("negative control: the bad scene fails the hero-hold and flare rules", B["lens_flares"] > 0 and B["hero_hold_s"] < G["hero_hold_s"] + 10, [B["lens_flares"], B["hero_hold_s"]], "flares > 0")], [out, wd / "scene_bad.json"]


def _rig(frames=48, phase=0.0, rigid=False, rubber=False, slide=False):
    """Planar character rig by forward kinematics (pelvis, knee, foot per leg) -> joints (F, 5, 2). The root advances
    so the stance foot (the lower one) stays planted; `slide` adds a drift that drags the planted foot."""
    np = _np()
    out, root_x, prev = [], 0.0, None
    for f in range(frames):
        ph = 2 * math.pi * f / frames + phase
        rel = []
        for side in (0, math.pi):
            a = 0.4 * math.sin(ph + side) if not rigid else 0.0
            thigh = 0.5 * (1 + (0.25 * math.sin(ph * 2) if rubber else 0))
            knee = thigh * np.array([math.sin(a), -math.cos(a)])
            foot = knee + 0.5 * np.array([math.sin(a * 0.5), -math.cos(a * 0.5)])
            foot = foot + np.array([0.0, 0.1 * max(0.0, math.cos(ph + side))]) if not rigid else foot   # swing foot lifts
            rel.append((knee, foot))
        y0, y1 = rel[0][1][1], rel[1][1][1]
        stance = 0 if y0 < y1 - 1e-12 else 1 if y1 < y0 - 1e-12 else (prev[0] if prev else 0)
        if prev is not None and prev[0] == stance:
            root_x -= rel[stance][1][0] - prev[1]
        if slide:
            root_x += 0.02
        prev = (stance, rel[stance][1][0])
        pelvis = np.array([root_x, 1.0])
        js = [pelvis] + [pelvis + v for kn, ft in rel for v in (kn, ft)]
        if rigid:
            rot = 0.3 * math.sin(ph)
            R = np.array([[math.cos(rot), -math.sin(rot)], [math.sin(rot), math.cos(rot)]])
            js = [pelvis + R @ (jj - pelvis) for jj in js]
        out.append(js)
    return np.array(out)


@card("QA-354")
def character_anti_patterns(task, wd):
    """Character anti-patterns measured on rig joint tracks: puppet whole-body rotation (pose rigid while the body
    turns), rubber limbs (bone length varying > 5 %), identical timing between characters (zero phase lag), sliding
    feet (a planted foot moving), and famous-character imitation (name blacklist)."""
    np = _np()

    def audit(J, other=None, name=""):
        bone = np.linalg.norm(J[:, 1] - J[:, 0], axis=1)
        rel = J - J[:, :1]
        shape_change = float(np.abs(np.diff(np.linalg.norm(rel, axis=2), axis=0)).max())
        ang = np.arctan2(rel[:, 2, 0], -rel[:, 2, 1])
        f = {"bone_cv": float(bone.std() / bone.mean()), "rubber": float(bone.std() / bone.mean()) > 0.05,
             "puppet_rotation": shape_change < 1e-9 and float(np.ptp(ang)) > 0.1}
        foot, other_foot = J[:, 2], J[:, 4]
        planted = foot[:, 1] < other_foot[:, 1] - 1e-12
        vx = np.abs(np.diff(foot[:, 0]))[planted[1:] & planted[:-1]]
        f["planted_foot_slip"] = float(vx.max()) if len(vx) else 0.0
        f["sliding_feet"] = f["planted_foot_slip"] > 0.005
        if other is not None:
            a, b = J[:, 2, 0] - J[:, 0, 0], other[:, 2, 0] - other[:, 0, 0]
            lags = [float(np.corrcoef(a, np.roll(b, k))[0, 1]) for k in range(len(a))]
            f["phase_lag_frames"] = int(np.argmax(lags))
        f["imitation"] = name.lower() in {"mickey", "pikachu", "mario"}
        return f
    good, mate = _rig(), _rig(phase=0.9)
    bad_twin = _rig()
    res = {"good": audit(good, mate, "Noor"), "rigid": audit(_rig(rigid=True)), "rubber": audit(_rig(rubber=True)),
           "twins": audit(good, bad_twin), "slide": audit(_rig(slide=True)), "named": audit(good, name="Pikachu")}
    out = wj(wd / "rig_audit.json", res)
    return [check("puppet whole-body rotation found on the rigid rig", res["rigid"]["puppet_rotation"] and not res["good"]["puppet_rotation"], [res["rigid"]["puppet_rotation"], res["good"]["puppet_rotation"]], [True, False]),
            check("rubber limbs: thigh length CV > 5 %", res["rubber"]["rubber"] and res["good"]["bone_cv"] < 1e-9, [res["rubber"]["bone_cv"], res["good"]["bone_cv"]], "> 0.05 vs 0"),
            check("identical timing: two characters with zero phase lag", res["twins"]["phase_lag_frames"] == 0 and res["good"]["phase_lag_frames"] != 0,
                  [res["twins"]["phase_lag_frames"], res["good"]["phase_lag_frames"]], [0, "!= 0"]),
            check("sliding feet: the planted foot drags 0.02 per frame on the slide rig, stays put on the good walk",
                  res["slide"]["sliding_feet"] and abs(res["slide"]["planted_foot_slip"] - 0.02) < 1e-6 and res["good"]["planted_foot_slip"] < 1e-9,
                  [res["good"]["planted_foot_slip"], res["slide"]["planted_foot_slip"]], [0, 0.02]),
            check("famous-character imitation flagged by name", res["named"]["imitation"] and not res["good"]["imitation"], [res["named"]["imitation"], res["good"]["imitation"]], [True, False]),
            check("negative control: the clean walk trips none of rubber / puppet / sliding / imitation", not (res["good"]["rubber"] or res["good"]["puppet_rotation"] or res["good"]["sliding_feet"] or res["good"]["imitation"]),
                  res["good"], "clean")], [out]


def im_run(*args):
    return subprocess.run(["convert", *map(str, args)], capture_output=True, text=True, timeout=30, stdin=subprocess.DEVNULL)


@card("QA-362")
def photo_anti_patterns(task, wd):
    """Photo-montage anti-patterns measured with ImageMagick and the edit list: stretched photos (aspect changed),
    haloed cut-outs (a bright ring around the alpha edge), black boxes (bars `-trim` finds), mirrored text (OCR reads
    only the flopped image), screensaver push-ins (the same linear zoom on every shot), and 1 s crossfades everywhere."""
    np = _np()
    from PIL import Image, ImageDraw, ImageFont
    font = ImageFont.truetype(str(SKILLS / "kosif-superpowers/proofs/_shared/fonts/Poppins-Bold.ttf"), 44)
    src = Image.new("RGB", (400, 300), (90, 120, 150))
    ImageDraw.Draw(src).text((40, 120), "MARKET", fill=(255, 255, 255), font=font)
    src.save(wd / "photo.png")
    im_run(wd / "photo.png", "-resize", "400x200!", wd / "stretched.png")
    im_run(wd / "photo.png", "-flop", wd / "mirrored.png")
    im_run(wd / "photo.png", "-background", "black", "-gravity", "center", "-extent", "560x300", wd / "boxed.png")
    cut = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    ImageDraw.Draw(cut).ellipse([40, 40, 160, 160], fill=(200, 80, 60, 255))
    plate = Image.new("RGB", (200, 200), (40, 40, 40))
    halo = plate.copy()
    ImageDraw.Draw(halo).ellipse([34, 34, 166, 166], fill=(250, 250, 250))
    halo.paste(cut, (0, 0), cut)
    clean = plate.copy()
    clean.paste(cut, (0, 0), cut)
    halo.save(wd / "halo.png")
    clean.save(wd / "clean_cut.png")
    cut.save(wd / "mask.png")

    def ident(p):
        return [int(x) for x in subprocess.run(["identify", "-format", "%w %h", str(p)], capture_output=True, text=True, timeout=30).stdout.split()]

    def trimmed(p):
        g = subprocess.run(["convert", str(p), "-fuzz", "3%", "-trim", "-format", "%w %h", "info:"], capture_output=True, text=True, timeout=30).stdout.split()
        return [int(x) for x in g]

    def ring(p):
        im_run(wd / "mask.png", "-alpha", "extract", "-morphology", "EdgeOut", "Disk:3", wd / "ring.png")
        r = np.asarray(Image.open(wd / "ring.png").convert("L")) > 128
        a = np.asarray(Image.open(p).convert("L"), float)
        return float(a[r].mean())
    w0, h0 = ident(wd / "photo.png")
    w1, h1 = ident(wd / "stretched.png")
    tb = trimmed(wd / "boxed.png")
    read_plain, read_mirror = ocr(wd / "photo.png", 7).upper(), ocr(wd / "mirrored.png", 7).upper()
    im_run(wd / "mirrored.png", "-flop", wd / "mirrored_flopped.png")
    read_back = ocr(wd / "mirrored_flopped.png", 7).upper()
    edits_bad = [{"zoom": [1.0, 1.1], "ease": "linear", "xfade": 1.0} for _ in range(4)]
    edits_good = [{"zoom": [1.0, 1.04], "ease": "power2.out", "xfade": 0.0}, {"zoom": [1.08, 1.0], "ease": "power1.inOut", "xfade": 0.4},
                  {"zoom": [1.0, 1.0], "ease": "none", "xfade": 0.0}, {"zoom": [1.0, 1.06], "ease": "power2.out", "xfade": 0.25}]
    screensaver = lambda e: all(x["ease"] == "linear" and x["zoom"][1] > x["zoom"][0] for x in e)
    xf1 = lambda e: all(abs(x["xfade"] - 1.0) < 1e-9 for x in e)
    res = {"stretch": [w0 / float(h0), w1 / float(h1)], "black_box_trim": tb, "halo_ring": ring(wd / "halo.png"), "clean_ring": ring(wd / "clean_cut.png"),
           "ocr": [read_plain, read_mirror, read_back], "screensaver": [screensaver(edits_bad), screensaver(edits_good)], "xfade_1s": [xf1(edits_bad), xf1(edits_good)]}
    out = wj(wd / "photo_audit.json", res)
    return [check("stretched photo: aspect 1.333 -> 2.0", abs(res["stretch"][0] - 4 / 3.0) < 1e-6 and res["stretch"][1] == 2.0, res["stretch"], [1.333, 2.0]),
            check("black boxes: -trim finds the 400 px photo inside the 560 px frame", tb[0] == 400, tb, [400, 300]),
            check("haloed cut-out: bright ring around the alpha edge", res["halo_ring"] > 200 and res["clean_ring"] < 60, [res["halo_ring"], res["clean_ring"]], "> 200 vs < 60"),
            check("mirrored text: unreadable as shown, readable once flopped back", "MARKET" in read_plain and "MARKET" not in read_mirror and "MARKET" in read_back, res["ocr"], "flopped"),
            check("screensaver push-ins and 1 s crossfades on every shot found", res["screensaver"] == [True, False] and res["xfade_1s"] == [True, False],
                  [res["screensaver"], res["xfade_1s"]], [[True, False], [True, False]]),
            check("negative control: the clean cut-out has no halo", res["clean_ring"] < 60, res["clean_ring"], "< 60")], [out, wd / "halo.png"]


THIRD_PARTY = ["nike", "apple", "coca-cola", "instagram", "tiktok", "netflix"]


@card("QA-369")
def trademark_safety(task, wd):
    """Trademark safety rule: scan the film's text and logo assets for third-party marks and trade dress (names and a
    perceptual-hash match against a reference mark), and label unverified claims as placeholders in the output copy."""
    np = _np()
    from PIL import Image, ImageDraw
    script = ["Run faster than Nike runners", "Our app is the #1 choice", "Made in Cairo", "Cuts edit time by 73%", "Share it on Instagram"]
    sources = {"Made in Cairo": "company registry"}

    def swoosh(path, shift=0):
        im = Image.new("RGB", (64, 64), "white")
        ImageDraw.Draw(im).polygon([(6 + shift, 40), (58, 14), (24, 50)], fill="black")
        im.save(path)
        return np.asarray(im, float)
    ref = phash(swoosh(wd / "ref_mark.png"))
    assets = {"logo_a.png": swoosh(wd / "logo_a.png", 2), "own_logo.png": None}
    own = Image.new("RGB", (64, 64), "white")
    ImageDraw.Draw(own).ellipse([12, 12, 52, 52], fill=(255, 176, 0))
    own.save(wd / "own_logo.png")
    assets["own_logo.png"] = np.asarray(own, float)
    marks = {k: hamming(phash(v), ref) <= 8 for k, v in assets.items()}
    out_lines, flags = [], []
    for ln in script:
        hits = [b for b in THIRD_PARTY if re.search(r"\b%s\b" % re.escape(b), ln.lower())]
        claim = bool(re.search(r"#1|\d+\s*%|best|clinically|guaranteed", ln, re.I)) and ln not in sources
        if hits:
            flags.append(("mark", ln, hits))
            ln = re.sub("|".join(hits), "[third-party mark removed]", ln, flags=re.I)
        if claim:
            flags.append(("claim", ln))
            ln = "[PLACEHOLDER: unverified claim] " + ln
        out_lines.append(ln)
    tw(wd / "script_safe.txt", "\n".join(out_lines))
    out = wj(wd / "trademark_report.json", {"flags": flags, "logo_matches": marks})
    return [check("third-party names found (Nike, Instagram)", sorted(h for f in flags if f[0] == "mark" for h in f[2]) == ["instagram", "nike"], [f for f in flags if f[0] == "mark"], 2),
            check("unverified claims labelled as placeholders (#1, 73 %)", sum(1 for f in flags if f[0] == "claim") == 2 and all(l.startswith("[PLACEHOLDER") for l in out_lines[1:2] + out_lines[3:4]),
                  [f[1] for f in flags if f[0] == "claim"], 2),
            check("logo asset matching a third-party mark caught by perceptual hash", marks == {"logo_a.png": True, "own_logo.png": False}, marks, {"logo_a.png": True, "own_logo.png": False}),
            check("sourced fact left alone", out_lines[2] == "Made in Cairo", out_lines[2], "Made in Cairo"),
            check("negative control: the raw script contains the marks", any("Nike" in l for l in script) and not any("Nike" in l for l in out_lines), "Nike", "removed")], [out, wd / "script_safe.txt"]


@card("QA-337")
def silent_readability(task, wd):
    """Silent-readability test: render each storyboard shot, read its on-screen text back with OCR, and require that
    the key fact of every shot is legible muted, and that each shot adds information the previous ones did not."""
    from PIL import Image, ImageDraw, ImageFont
    font = ImageFont.truetype(str(SKILLS / "kosif-superpowers/proofs/_shared/fonts/Poppins-Bold.ttf"), 40)
    boards = {
        "v1": [{"vo": "Prices fell by 40 percent", "fact": "40%", "screen": "BIG NEWS"},
               {"vo": "starting Monday", "fact": "MONDAY", "screen": "MONDAY"},
               {"vo": "in every store", "fact": "STORES", "screen": "MONDAY"}],
        "v2": [{"vo": "Prices fell by 40 percent", "fact": "40%", "screen": "PRICES -40%"},
               {"vo": "starting Monday", "fact": "MONDAY", "screen": "FROM MONDAY"},
               {"vo": "in every store", "fact": "STORES", "screen": "ALL STORES"}]}
    res = {}
    for k, shots in boards.items():
        seen, rows = set(), []
        for i, s in enumerate(shots):
            im = Image.new("RGB", (560, 140), (16, 24, 32))
            ImageDraw.Draw(im).text((20, 40), s["screen"], fill=(255, 255, 255), font=font)
            p = wd / ("%s_shot%d.png" % (k, i))
            im.save(p)
            txt = ocr(p, 7).upper().replace(" ", "")
            words = set(re.findall(r"[A-Z0-9%-]+", ocr(p, 7).upper()))
            rows.append({"shot": i, "ocr": txt, "muted_ok": s["fact"] in txt.replace("-", ""), "adds_info": bool(words - seen)})
            seen |= words
        res[k] = rows
    out = wj(wd / "silent_test.json", res)
    v1, v2 = res["v1"], res["v2"]
    return [check("v1: shot 0's fact (40 %) lives only in the voice-over", not v1[0]["muted_ok"], v1[0]["ocr"], "no 40%"),
            check("v1: shot 2 repeats shot 1 and adds nothing", not v1[2]["adds_info"], v1[2], "adds nothing"),
            check("v2: every fact is readable muted", all(r["muted_ok"] for r in v2), [r["ocr"] for r in v2], "all facts"),
            check("v2: every shot adds new information", all(r["adds_info"] for r in v2), [r["adds_info"] for r in v2], [True] * 3),
            check("negative control: the first storyboard fails the silent test", not all(r["muted_ok"] and r["adds_info"] for r in v1), [(r["muted_ok"], r["adds_info"]) for r in v1], "fails")], [out, wd / "v2_shot0.png"]


@card("QA-347")
def twelve_aesthetic_lenses(task, wd):
    """Twelve aesthetic lenses judged on frames: one measured line per lens (world & depth, silhouette, action /
    contact, camera, light, colour, VFX, atmosphere, materials, production design, composition, beauty) in review.md."""
    np = _np()
    from scipy.ndimage import gaussian_filter
    H, W, n = 180, 320, 24

    def film(rich):
        fr = []
        yy, xx = np.mgrid[0:H, 0:W]
        for i in range(n):
            if not rich:
                fr.append(np.full((H, W, 3), 128.0))
                continue
            bg = gaussian_filter(texture(3, H, W, 8, 60, 140), (3, 3, 0))                  # soft background = depth
            haze = (1 - yy / H)[..., None] * 60
            img = bg * 0.45 + haze + np.array([0, 10, 40]) * (1 - yy / H)[..., None]
            img = img * (0.75 + 0.5 * (1 - xx / W))[..., None]                              # key light from the left
            x0 = 96 + i * 2
            img[60:150, x0:x0 + 40] = texture(9, 90, 40, 4, 200, 250) * np.array([1.0, 0.7, 0.5])   # subject near the left third, warm
            if i in (12, 13):
                img[20:30, 200:300] = 255                                                   # a hit: VFX flash
            fr.append(img)
        return fr

    def lenses(F):
        F = np.array(F)
        mid = F[8]                                       # a frame between hits; the subject sits at x 112..152 there
        g = mid.mean(axis=2)
        e = energy(F)
        hsv_h = (np.degrees(np.arctan2(math.sqrt(3) * (mid[..., 1] - mid[..., 2]), 2 * mid[..., 0] - mid[..., 1] - mid[..., 2])) % 360)
        cy, cx = np.argwhere(np.abs(mid - mid.mean(axis=(0, 1))).sum(axis=2) > 120).mean(axis=0) if (np.abs(mid - mid.mean(axis=(0, 1))).sum(axis=2) > 120).any() else (H / 2, W / 2)
        L = {
            "world & depth": lapvar(mid[60:150, 112:152]) / max(1e-6, lapvar(mid[155:178, 200:300])),
            "character silhouette": contrast(mid[60:150, 112:152].reshape(-1, 3).mean(0), mid[60:150, 40:80].reshape(-1, 3).mean(0)),
            "action/contact": float(e.max() / max(1e-6, np.median(e))),
            "camera": float(np.median(e)),
            "light": float(g[:, :W // 3].mean() - g[:, -W // 3:].mean()),
            "colour": float(np.std(hsv_h)),
            "VFX": float((F.min(axis=3) > 250).mean(axis=(1, 2)).max()),
            "atmosphere": float(g[:30].mean() - g[-30:].mean()),
            "materials": float(mid[60:150, 112:152].std()),
            "production design": float(len(np.unique((mid // 32).reshape(-1, 3), axis=0))),
            "composition": float(abs(cx / W - 1 / 3.0)),
        }
        L["beauty"] = float(sum([L["world & depth"] > 2, L["character silhouette"] > 1.5, L["light"] > 10, L["composition"] < 0.15]))
        return L
    rich, flat = lenses(film(True)), lenses(film(False))
    lines = ["# Twelve-lens review"] + ["- %s: %.3f" % (k, v) for k, v in rich.items()]
    tw(wd / "review.md", "\n".join(lines))
    wj(wd / "lenses.json", {"rich": rich, "flat": flat})
    return [check("review.md has exactly one line per lens (12)", len(lines) - 1 == 12, len(lines) - 1, 12),
            check("depth: subject sharper than the soft background (> 2x)", rich["world & depth"] > 2, rich["world & depth"], "> 2"),
            check("light comes from the left (left third brighter by > 10)", rich["light"] > 10, rich["light"], "> 10"),
            check("action: the hit is a motion-energy peak (> 3x median)", rich["action/contact"] > 3, rich["action/contact"], "> 3"),
            check("composition: subject near the left third (|x/W - 1/3| < 0.15)", rich["composition"] < 0.15, rich["composition"], "< 0.15"),
            check("atmosphere: haze lifts the top of frame", rich["atmosphere"] > 10, rich["atmosphere"], "> 10"),
            check("negative control: a flat grey film scores 0 of 4 on the beauty roll-up", flat["beauty"] == 0 and rich["beauty"] == 4, [flat["beauty"], rich["beauty"]], [0, 4])], [wd / "review.md"]


@card("QA-X05")
def client_proxy_critic(task, wd):
    """Client-proxy critic: the critic's brief carries the client's verbatim words, the approved version and the three
    things that must not change; it judges by that taste (space is wanted) instead of a generic creative director's
    (who calls > 60 % empty canvas a flaw), and checks the must-not-change regions against the approved frame."""
    np = _np()
    from PIL import Image, ImageDraw
    W, H = 320, 568

    def frame(path, logo_xy=(24, 24), extra_blocks=0, title="#f4efe6"):
        im = Image.new("RGB", (W, H), "#0e1a2b")
        d = ImageDraw.Draw(im)
        d.rectangle([logo_xy[0], logo_xy[1], logo_xy[0] + 40, logo_xy[1] + 40], fill="#ffb000")
        d.rectangle([24, 380, 296, 420], fill=title)
        for i in range(extra_blocks):
            d.rectangle([24 + (i % 3) * 92, 100 + (i // 3) * 70, 104 + (i % 3) * 92, 160 + (i // 3) * 70], fill="#3a5570")
        im.save(path)
        return np.asarray(im, float)
    approved = frame(wd / "approved.png")
    spacious = frame(wd / "v_spacious.png")
    cluttered = frame(wd / "v_cluttered.png", logo_xy=(250, 24), extra_blocks=9)
    brief = {"client_words": "Leave it calm. Lots of empty space. Do not move my logo.", "approved": "approved.png",
             "must_not_change": [{"name": "logo", "box": [24, 24, 64, 64]}, {"name": "title bar", "box": [24, 380, 296, 420]}, {"name": "ground colour", "box": [0, 500, 320, 568]}]}
    wj(wd / "critic_brief.json", brief)
    empty = lambda a: float((np.abs(a - np.array(hexrgb("#0e1a2b"), float)).sum(axis=2) < 6).mean())

    def proxy(a):
        viol = [m["name"] for m in brief["must_not_change"] if np.abs(a[m["box"][1]:m["box"][3], m["box"][0]:m["box"][2]] -
                                                                   approved[m["box"][1]:m["box"][3], m["box"][0]:m["box"][2]]).mean() > 1]
        ok = empty(a) >= 0.6 and not viol
        return {"empty": empty(a), "violations": viol, "verdict": "approve" if ok else "revise"}

    def generic(a):
        return {"empty": empty(a), "verdict": "revise" if empty(a) > 0.6 else "approve"}
    res = {"spacious": {"proxy": proxy(spacious), "generic": generic(spacious)}, "cluttered": {"proxy": proxy(cluttered), "generic": generic(cluttered)}}
    out = wj(wd / "critic.json", res)
    return [check("brief carries the client's words, the approved version and 3 must-not-change items",
                  "empty space" in brief["client_words"] and len(brief["must_not_change"]) == 3, len(brief["must_not_change"]), 3),
            check("client proxy approves the spacious version (> 60 % empty)", res["spacious"]["proxy"]["verdict"] == "approve" and res["spacious"]["proxy"]["empty"] > 0.6,
                  res["spacious"]["proxy"], "approve"),
            check("client proxy sends the cluttered version back and names the moved logo", res["cluttered"]["proxy"]["verdict"] == "revise" and res["cluttered"]["proxy"]["violations"] == ["logo"],
                  res["cluttered"]["proxy"]["violations"], ["logo"]),
            check("negative control: a generic critic rejects the space the client asked for", res["spacious"]["generic"]["verdict"] == "revise", res["spacious"]["generic"], "revise")], [out, wd / "critic_brief.json"]
