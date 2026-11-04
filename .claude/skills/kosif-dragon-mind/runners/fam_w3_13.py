"""Wave 3, chunk 13: real runners for build, media, Arabic-language, brand, character, colour, explainer, format,
knowledge-graph, misc, UI and web-research cards.

Engines used (all already installed here; nothing was pip/npm installed for this module):
- python: numpy, PIL (raqm), cv2, cryptography (Ed25519), networkx (AST knowledge graph, Louvain), sqlite3 FTS5,
  trafilatura + bs4/lxml, spacy (blank "ar"), httpx, jsonschema, zipfile, http.server (local fixtures only)
- binaries: ffmpeg/ffprobe, tesseract (ara), pdftotext/pdftoppm, ImageMagick convert, pandoc, curl, mmdc, gcc
- node: playwright (driving /usr/bin/google-chrome), gsap + ScrollTrigger, lottie-web, three via the repo's
  three-kit.bundle.js / shape-kit.js / lab-kit.js, the HyperFrames CLI registry (`hyperframes add`), the
  fastify-motion-bro planner, and the vendored kosif-montage-motion scripts (mtemplates, launch, social,
  build_studio_cloud)

Every runner builds its own deterministic fixture inside the work folder, does the card's method, measures the
produced file against known answers, and runs a negative control on the untreated input. Local HTTP servers bind
127.0.0.1 only and are shut down before the runner returns; nothing is written outside the work folder.
Cards whose engine is a paid service, an account, a GPU, a proprietary app, or a library this session was not allowed
to install are listed in GAPS with the reason.
"""
from __future__ import annotations

import ast
import hashlib
import html as _html
import importlib
import importlib.util
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
import zipfile
from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from _harness import card, check, fx, sha

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
SKILLS = REPO / ".claude/skills"
VSK = SKILLS / "kosif-superpowers/vendor/100-superskills/skills"
MM = VSK / "kosif-montage-motion/scripts"
KIT = MM / "kit"
FASTIFY = REPO.parent / "fastify-motion-bro"
CHROME = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
NODE = shutil.which("node")
NODE_MODULES = (Path(NODE).resolve().parents[1] / "lib/node_modules") if NODE else Path("/nonexistent")
GSAP = NODE_MODULES / "gsap/dist/gsap.min.js"
SCROLLTRIGGER = NODE_MODULES / "gsap/dist/ScrollTrigger.min.js"
LOTTIE = NODE_MODULES / "lottie-web/build/player/lottie.min.js"
HF_CLI = NODE_MODULES / "hyperframes/dist/cli.js"
FREESERIF = Path("/usr/share/fonts/truetype/freefont/FreeSerif.ttf")
DEJAVU = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
DEJAVU_B = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
MONO = Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")

_INSTALL_DENIED = "this session may not install packages (pip/npm install was refused by the permission check)"
GAPS: dict = {
    "power:ABUILD-11": "inspects live App Store / Google Play product state and adds RevenueCat Customer Center: needs store "
                       "accounts and a RevenueCat API key (live paid service)",
    "power:ABUILD-13": "assembles a Wix Headless site: needs a Wix account access token and the live Wix REST/SDK service",
    "power:ABUILD-27": "provisions Render / Vercel / Sealos storage: needs accounts on those live hosting services",
    "power:AMEDIA-01": "ElevenLabs TTS / voice cloning: paid API key and network service",
    "power:AMEDIA-04": "hosted speech-to-text API (batch/streaming/realtime): paid API key and network service",
    "power:AMEDIA-06": "local whisper transcription: no whisper model is on disk (faster-whisper is installed but the model "
                       "download from Hugging Face is a network model fetch) and no yt-dlp/streamlink live source here",
    "power:AMEDIA-08": "PipeWire + WirePlumber + pipewire-pulse are not installed in this container; " + _INSTALL_DENIED,
    "power:AMEDIA-24": "After Effects scripting: proprietary Adobe app (macOS/Windows) not available",
    "power:AMEDIA-27": "Godot engine binary is not installed (headless export needs godot + export templates); " + _INSTALL_DENIED,
    "power:AMEDIA-29": "Houdini / ZBrush / CATIA / Fusion / Rhino / SOLIDWORKS: proprietary, mostly Windows-only DCC/CAD apps",
    "power:ARL-10": "camel-tools is not installed and `pip install --no-deps camel-tools emoji` was refused here; " + _INSTALL_DENIED,
    "power:ARL-11": "full camel-tools needs transformers + torch (~769 MB) and downloaded data packages",
    "power:ARL-12": "pyarabic is not installed; " + _INSTALL_DENIED,
    "power:ARL-13": "farasapy is not installed and downloads the Farasa Java jars from its host at first use; " + _INSTALL_DENIED,
    "power:ARL-20": "camel-tools plus `camel_data -i light` data download; camel-tools is not installed; " + _INSTALL_DENIED,
    "power:ARL-22": "Argos Translate needs its package (torch/stanza stack) plus a ~100 MB ar<->en model download",
    "power:BRAND-10": "fetches official marks from theSVG.org / GitHub / domain icons: live network providers, and third-party "
                      "logos may not be used without permission",
    "power:BRAND-11": "Figma assets/tokens/components/motion via scoped Figma REST and MCP credentials (account + live service)",
    "power:BRAND-16": "Recraft vector generation with an uploaded brand style: paid API key and network service",
    "power:CHAR-06": "multi-reference character generation / IP-Adapter: needs Gemini/OpenAI image keys or a GPU ComfyUI host",
    "power:CHAR-07": "one-request animation strip from an image-edit model: needs an image-edit model API key",
    "power:CHAR-08": "HeyGen / Synthesia lip-synced presenters: paid account key and network service",
    "power:CHAR-50": "panel art from an image model (needs a key); the card's art is the deliverable",
    "power:COLOR-81": "the shader plates need a WebGPU-capable Chromium; headless WebGPU is not available here",
    "power:EXPL-12": "the d2 binary is not installed and its installer host is unverified; " + _INSTALL_DENIED,
    "power:EXPL-41": "PR explainer pipeline needs `gh` network fetches of a real PR plus a voice engine (Kokoro model / HeyGen key)",
    "power:EXPL-45": "Manim (MathTex, TransformMatchingTex) is not installed (needs pip + cairo/pango + LaTeX); " + _INSTALL_DENIED,
    "power:EXPL-X01": "the method's smoke render is `manim -ql`; Manim is not installed; " + _INSTALL_DENIED,
    "power:FMT-25": "h264_nvenc needs an NVIDIA GPU; this container has none",
    "power:FMT-40": "WhatsApp sender needs the owner's personal account linked by scanning a QR code (live service)",
    "power:FMT-69": "instruction-only owner skills (e-commerce, newsletter, SEO): no program to execute",
    "power:GRAPH-01": "installing graphifyy into a venv (~240 MB) is the card itself; " + _INSTALL_DENIED,
    "power:GRAPH-07": "graphify-mcp (the graphifyy[mcp] extra) is not installed; " + _INSTALL_DENIED,
    "power:GRAPH-09": "`graphify install --project` needs the graphify CLI, which is not installed; " + _INSTALL_DENIED,
    "power:GRAPH-10": "doc/image extraction into the graph needs a model backend (subagents or a paid API key)",
    "power:GRAPH-11": "Graphify hosted service over MCP: OAuth account and live service",
    "power:GRAPH-12": "queries the Graphify hosted graph service: OAuth account and live service",
    "power:GRAPH-13": "impact/risk tools of the Graphify hosted service: OAuth account and live service",
    "power:GRAPH-14": "remember/recall writes shared state to the Graphify hosted workspace: account and live service",
    "power:MISC-02": "the KOSIF Atlas pack is not in this checkout; it needs KOSIF_ATLAS_SOURCE=external or the hosted edge API",
    "power:MISC-09": "Windows UIA/OCR desktop automation: Windows-only, not usable in this Linux container",
    "power:MISC-21": "instruction-only owner playbooks: no program to execute",
    "power:UI-55": "GLTF device models from a CDN plus the experimental HTML-in-Canvas Chromium API (not available headless here)",
    "power:UI-78": "video-guide-creator runs in Docker with Edge TTS; Docker is absent and edge-tts is blocked from here",
    "power:WEB-01": "WebSearch is a session tool of the assistant, not callable from a program run",
    "power:WEB-02": "WebFetch is a session tool of the assistant, not callable from a program run",
    "power:WEB-03": "server-side web_search/web_fetch tools need an Anthropic API key and the live API",
    "power:WEB-08": "downloads from huggingface.co through the proxy: a live third-party host, not a deterministic fixture",
    "power:WEB-09": "gh search / release / license calls query the live GitHub API",
    "power:WEB-20": "needs the host's scheduling feature (scheduled tasks / send-later) to re-run a search",
    "power:WEB-21": "Scrapy is not installed; " + _INSTALL_DENIED,
    "power:WEB-22": "Crawl4AI (and its playwright-python + browser setup) is not installed; " + _INSTALL_DENIED,
    "power:WEB-24": "browser-use needs an LLM API key to plan the steps (and is not installed)",
}


# ═════════════════════════════════════════════ helpers ═════════════════════════════════════════════
def _np():
    import numpy as np
    return np


def write_json(wd, name, obj):
    p = Path(wd) / name
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
    return p


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def hexc(c):
    return "#%02x%02x%02x" % tuple(int(round(max(0, min(255, v)))) for v in c[:3])


def rel_lum(c):
    def ch(v):
        v = v / 255.0
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(v) for v in (rgb(c) if isinstance(c, str) else c))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((rel_lum(a), rel_lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def save_png(arr, path):
    from PIL import Image
    Image.fromarray(_np().clip(arr, 0, 255).round().astype("uint8")).save(path)
    return Path(path)


def load_png(path, mode="RGB"):
    from PIL import Image
    return _np().asarray(Image.open(path).convert(mode)).astype(float)


def write_video(path, frames, fps=30):
    """Encode numpy frames losslessly (libx264rgb qp 0) so pixel measurements read back exactly."""
    np = _np()
    frames = list(frames)
    h, w = frames[0].shape[:2]
    p = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", "%dx%d" % (w, h), "-r", str(fps), "-i", "-", "-c:v", "libx264rgb", "-qp", "0",
                          "-preset", "ultrafast", str(path)], stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    for f in frames:
        p.stdin.write(np.clip(f, 0, 255).round().astype("uint8").tobytes())
    p.stdin.close()
    if p.wait():
        raise RuntimeError("ffmpeg encode failed: %s" % p.stderr.read().decode(errors="replace")[-300:])
    return Path(path)


def read_video(path):
    np = _np()
    st = [s for s in fx.probe(path)["streams"] if s.get("codec_type") == "video"][0]
    w, h = int(st["width"]), int(st["height"])
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, timeout=120, stdin=subprocess.DEVNULL).stdout
    return np.frombuffer(out, dtype=np.uint8).reshape(-1, h, w, 3).astype(float)


def chrome_page(wd, name, html, size=(800, 600), budget=3000, screenshot=False):
    """Run a page in headless Chrome and return the JSON its script wrote into <pre id=OUT>."""
    if not CHROME:
        raise RuntimeError("google-chrome not found")
    page = Path(wd) / ("%s.html" % name)
    page.write_text(html, encoding="utf-8")
    base = [CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
            "--disable-extensions", "--allow-file-access-from-files", "--window-size=%d,%d" % size,
            "--virtual-time-budget=%d" % budget]
    done = subprocess.run(base + ["--dump-dom", page.as_uri()], capture_output=True, text=True, timeout=40,
                          stdin=subprocess.DEVNULL)
    m = re.search(r'<pre id="OUT"[^>]*>(.*?)</pre>', done.stdout, re.S)
    if not m or not m.group(1).strip():
        raise RuntimeError("page produced no #OUT: " + done.stderr[-300:])
    out = json.loads(_html.unescape(m.group(1)))
    if isinstance(out, dict) and out.get("__error"):
        raise RuntimeError("page error: " + out["__error"][:300])
    shot = None
    if screenshot:
        shot = Path(wd) / ("%s.png" % name)
        subprocess.run(base + ["--screenshot=%s" % shot, page.as_uri()], capture_output=True, timeout=40,
                       stdin=subprocess.DEVNULL)
        if not shot.exists():
            raise RuntimeError("screenshot failed")
    return out, page, shot


def html_doc(body, js, scripts=(), css="", onload=True):
    tags = "".join("<script>%s</script>" % Path(s).read_text(encoding="utf-8") for s in scripts)
    run = ("window.addEventListener('load',()=>{try{const __r=(()=>{%s})();document.getElementById('OUT').textContent=JSON.stringify(__r)}"
           "catch(e){document.getElementById('OUT').textContent=JSON.stringify({__error:String(e)+' '+(e.stack||'')})}});") % js
    if not onload:
        run = run.replace("window.addEventListener('load',()=>{", "(()=>{").replace("}});", "}})();")
    return ("<!doctype html><html><head><meta charset=utf-8><style>html,body{margin:0;padding:0}%s</style>%s</head>"
            "<body>%s<pre id=\"OUT\" style=\"display:none\"></pre><script>%s</script></body></html>") % (css, tags, body, run)


def node_json(wd, name, js, timeout=40):
    if not NODE:
        raise RuntimeError("node not available")
    p = Path(wd) / ("%s.js" % name)
    p.write_text(js, encoding="utf-8")
    env = {"NODE_PATH": str(NODE_MODULES), "PATH": str(Path(NODE).parent) + ":/usr/bin:/bin", "HOME": str(wd)}
    if os.environ.get("PLAYWRIGHT_BROWSERS_PATH"):
        env["PLAYWRIGHT_BROWSERS_PATH"] = os.environ["PLAYWRIGHT_BROWSERS_PATH"]
    done = subprocess.run([NODE, str(p)], capture_output=True, text=True, timeout=timeout, cwd=str(wd), env=env,
                          stdin=subprocess.DEVNULL)
    if done.returncode:
        raise RuntimeError("node failed: %s" % done.stderr[-500:])
    lines = [l for l in done.stdout.strip().splitlines() if l.strip()]
    out = Path(wd) / ("%s.json" % name)
    out.write_text(lines[-1] if lines else "", encoding="utf-8")
    return json.loads(lines[-1]), out


def font(path=DEJAVU, size=24):
    from PIL import ImageFont
    return ImageFont.truetype(str(path), size, layout_engine=ImageFont.Layout.RAQM)


class _Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def serve_dir(root, handler=None):
    """Serve a folder (or a custom handler) on 127.0.0.1 on a free port; returns (server, base_url)."""
    if handler is None:
        root = str(root)

        class H(_Quiet):
            def __init__(self, *a, **k):
                super().__init__(*a, directory=root, **k)
        handler = H
    srv = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, "http://127.0.0.1:%d" % srv.server_address[1]


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def pw_script(body):
    """A node Playwright script driving the system Chrome; `body` runs with `browser` open and prints JSON."""
    return ("const { chromium } = require('playwright');\n(async () => {\n"
            "const browser = await chromium.launch({ executablePath: %s, args: ['--no-sandbox', '--disable-gpu'] });\n"
            "try {\n%s\n} finally { await browser.close(); }\n})().catch(e => { console.error(String(e.stack || e)); process.exit(1); });\n"
            % (json.dumps(CHROME), body))


def load_py(path, name):
    if name in sys.modules:
        return sys.modules[name]
    sys.path.insert(0, str(Path(path).parent))
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    try:
        spec.loader.exec_module(mod)
    except Exception:
        sys.modules.pop(name, None)
        raise
    return mod


# ═════════════════════════════════════════════ atlas-build ═════════════════════════════════════════════
def _canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def _vt(v):
    return tuple(int(x) for x in v.split("."))


@card("ABUILD-05")
def signed_staged_updater(task, wd):
    """Signed update manifest + an updater that verifies the signature, honours channels, a staged rollout bucket,
    a version floor and a signed-only rollback; the signing key lives outside the app repo (gitignored)."""
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives import serialization
    from cryptography.exceptions import InvalidSignature
    import fnmatch
    repo = wd / "app-repo"
    (repo / "secrets").mkdir(parents=True, exist_ok=True)
    (repo / ".gitignore").write_text("secrets/\n*.jks\n*.p12\n", encoding="utf-8")
    key = Ed25519PrivateKey.from_private_bytes(hashlib.sha256(b"kosif-ci-secret-fixture").digest())
    (repo / "secrets/update-key.pem").write_bytes(key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
                                                                    serialization.NoEncryption()))
    pub = key.public_key()
    payload = wd / "app-2.4.0.bin"
    payload.write_bytes(b"APP" * 4096)

    def manifest(version, rollout, floor, channel="stable", rollback=False, data=payload):
        m = {"version": version, "channel": channel, "rollout_percent": rollout, "min_version": floor, "rollback": rollback,
             "sha256": hashlib.sha256(data.read_bytes()).hexdigest(), "url": "file://" + data.name}
        return {"manifest": m, "sig": key.sign(_canon(m)).hex()}

    def updater(signed, current, device, channel="stable"):
        m = signed.get("manifest")
        try:
            pub.verify(bytes.fromhex(signed.get("sig", "")), _canon(m))
        except (InvalidSignature, ValueError):
            return "reject:signature"
        if hashlib.sha256(payload.read_bytes()).hexdigest() != m["sha256"]:
            return "reject:payload-hash"
        if m["channel"] != channel:
            return "skip:channel"
        if _vt(m["version"]) <= _vt(current) and not m["rollback"]:
            return "skip:not-newer"
        if _vt(current) < _vt(m["min_version"]):
            return "update:forced-floor"
        bucket = int(hashlib.sha256(device.encode()).hexdigest()[:8], 16) % 100
        return "update:staged" if bucket < m["rollout_percent"] else "wait:staged"

    s10 = manifest("2.4.0", 10, "2.0.0")
    devices = ["device-%04d" % i for i in range(2000)]
    got = [updater(s10, "2.3.1", d) for d in devices]
    share = got.count("update:staged") / len(devices)
    tampered = json.loads(json.dumps(s10))
    tampered["manifest"]["rollout_percent"] = 100
    floor = updater(s10, "1.9.0", devices[0]) if updater(s10, "2.3.1", devices[0]) == "wait:staged" else updater(s10, "1.9.0", devices[1])
    downgrade_unsigned = json.loads(json.dumps(s10))
    downgrade_unsigned["manifest"].update(version="2.3.0", rollback=True)
    rollback_signed = manifest("2.3.0", 100, "2.0.0", rollback=True)
    unsigned = {"manifest": s10["manifest"], "sig": ""}
    ignored = any(fnmatch.fnmatch("secrets/update-key.pem", pat.rstrip("/") + ("/*" if pat.endswith("/") else ""))
                  for pat in (repo / ".gitignore").read_text().split())
    out = write_json(wd, "update-feed.json", {"stable": s10, "rollback": rollback_signed,
                                              "staged_share": share, "decisions_sample": got[:20]})
    return [check("staged rollout reaches ~10% of 2000 devices", abs(share - 0.10) < 0.025, share, "0.10 +- 0.025"),
            check("a tampered manifest is rejected", updater(tampered, "2.3.1", "x") == "reject:signature",
                  updater(tampered, "2.3.1", "x"), "reject:signature"),
            check("a client below the version floor is forced to update", floor == "update:forced-floor", floor, "update:forced-floor"),
            check("an unsigned rollback edit is rejected, a signed rollback is accepted",
                  updater(downgrade_unsigned, "2.4.0", "x") == "reject:signature" and updater(rollback_signed, "2.4.0", "x") == "update:staged",
                  [updater(downgrade_unsigned, "2.4.0", "x"), updater(rollback_signed, "2.4.0", "x")], ["reject:signature", "update:staged"]),
            check("beta channel clients skip a stable manifest", updater(s10, "2.3.1", "x", "beta") == "skip:channel"),
            check("the signing key path is gitignored (kept out of the repo)", ignored, ignored, True),
            check("negative control: the unsigned manifest is not accepted", updater(unsigned, "2.3.1", devices[0]) == "reject:signature",
                  updater(unsigned, "2.3.1", devices[0]), "reject:signature")], [out]


_DOC_APP = """<!doctype html><html><head><meta charset=utf-8><style>body{margin:0;font:16px/1.4 DejaVu Sans,sans-serif;background:#f6f7fb}
#hero{width:600px;height:180px;margin:20px;background:%s;color:#fff;display:flex;align-items:center;justify-content:center}
#pricing{width:600px;height:120px;margin:20px;background:#1f7a4f;color:#fff}</style></head><body>
<div id=app></div><script>setTimeout(()=>{document.getElementById('app').innerHTML=
'<div id=hero>KOSIF docs</div><div id=pricing>Plans</div><i id=ready></i>'},250)</script></body></html>"""


@card("ABUILD-17")
def reproducible_doc_screenshots(task, wd):
    """Playwright (system Chrome; Docker is not present here) starts the app, waits on a ready selector, captures each
    target at a fixed viewport into out/ with a manifest, compares with baselines, and only moves stray shots to trash
    on approval."""
    site = wd / "site"
    site.mkdir(exist_ok=True)
    (site / "index.html").write_text(_DOC_APP % "#2f5bff", encoding="utf-8")
    srv, base = serve_dir(site)
    js = pw_script("""
const fs = require('fs'), crypto = require('crypto');
const out = process.argv[2] || 'shots'; const res = {};
for (const run of ['%s/shots_a', '%s/shots_b']) {
  fs.mkdirSync(run, {recursive: true});
  const ctx = await browser.newContext({viewport: {width: 800, height: 600}, deviceScaleFactor: 1});
  const page = await ctx.newPage(); await page.goto('%s/index.html'); await page.waitForSelector('#ready', {state: 'attached', timeout: 5000});
  const man = [];
  for (const t of ['#hero', '#pricing']) { const p = run + '/' + t.slice(1) + '.png'; await page.locator(t).screenshot({path: p});
    man.push({target: t, file: p, sha256: crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex')}); }
  fs.writeFileSync(run + '/manifest.json', JSON.stringify({viewport: [800, 600], shots: man}, null, 1)); res[run] = man; await ctx.close();
}
console.log(JSON.stringify(res));""" % (wd, wd, base))
    try:
        res, _ = node_json(wd, "capture", js)
        (site / "index.html").write_text(_DOC_APP % "#e8333f", encoding="utf-8")       # a UI change after the baseline
        js2 = pw_script("""const ctx = await browser.newContext({viewport: {width: 800, height: 600}}); const page = await ctx.newPage();
await page.goto('%s/index.html'); await page.waitForSelector('#ready', {state: 'attached'});
await page.locator('#hero').screenshot({path: '%s/hero_changed.png'}); console.log(JSON.stringify({ok: 1}));""" % (base, wd))
        node_json(wd, "capture_changed", js2)
    finally:
        srv.shutdown()
    np = _np()
    a, b = res[str(wd / "shots_a")], res[str(wd / "shots_b")]
    base_img, again, changed = load_png(wd / "shots_a/hero.png"), load_png(wd / "shots_b/hero.png"), load_png(wd / "hero_changed.png")
    diff_same = float(np.abs(base_img - again).mean())
    diff_changed = float(np.abs(base_img - changed).mean()) if base_img.shape == changed.shape else 255.0
    size = base_img.shape[1], base_img.shape[0]
    # stray session screenshots: moved to trash only when approved
    stray = wd / "session"
    stray.mkdir(exist_ok=True)
    for n in ("Screenshot 1.png", "Screenshot 2.png"):
        (stray / n).write_bytes(b"\x89PNG stray")

    def cleanup(approved):
        if not approved:
            return 0
        (wd / "trash").mkdir(exist_ok=True)
        moved = 0
        for p in stray.glob("Screenshot*.png"):
            shutil.move(str(p), str(wd / "trash" / p.name))
            moved += 1
        return moved
    kept = cleanup(False)
    moved = cleanup(True)
    return [check("two clean runs give byte-identical shots (reproducible)", [x["sha256"] for x in a] == [x["sha256"] for x in b],
                  [x["sha256"][:12] for x in a], [x["sha256"][:12] for x in b]),
            check("hero captured at the element size inside the 800x600 viewport", size == (600, 180), size, (600, 180)),
            check("visual regression vs baseline: unchanged = 0, changed hero > 20", diff_same == 0 and diff_changed > 20,
                  [diff_same, diff_changed], [0, ">20"]),
            check("stray shots untouched without approval, moved to trash with it", kept == 0 and moved == 2, [kept, moved], [0, 2]),
            check("negative control: the changed UI does not match the baseline", not diff_changed == 0, diff_changed, "!= 0")], \
        [wd / "shots_a/manifest.json", wd / "shots_a/hero.png"]


def _figma_file():
    """A fixture shaped like GET /v1/files/:key (document tree + styles map)."""
    def frame(i, name, color, x, spacing):
        return {"id": "1:%d" % i, "name": name, "type": "FRAME", "absoluteBoundingBox": {"x": x, "y": 0, "width": 360, "height": 640},
                "layoutMode": "VERTICAL", "itemSpacing": spacing, "paddingLeft": 24, "paddingTop": 32,
                "fills": [{"type": "SOLID", "color": color}], "styles": {"fill": "S:bg%d" % i},
                "children": [{"id": "1:%d0" % i, "name": "Title", "type": "TEXT", "characters": "Hello",
                              "style": {"fontFamily": "Cairo", "fontSize": 32, "fontWeight": 800, "lineHeightPx": 40},
                              "styles": {"text": "S:h1"}, "fills": [{"type": "SOLID", "color": {"r": 1, "g": 1, "b": 1, "a": 1}}]}]}
    return {"name": "KOSIF UI", "version": "42",
            "document": {"id": "0:0", "type": "DOCUMENT", "children": [
                {"id": "0:1", "name": "Mobile", "type": "CANVAS", "children": [
                    frame(1, "Home", {"r": 0.043, "g": 0.063, "b": 0.125, "a": 1}, 0, 16),
                    frame(2, "Offer", {"r": 0.906, "g": 0.714, "b": 0.353, "a": 1}, 400, 24)]},
                {"id": "0:2", "name": "Icons", "type": "CANVAS", "children": [
                    {"id": "2:%d" % i, "name": "icon-%02d" % i, "type": "COMPONENT", "absoluteBoundingBox": {"x": i * 30, "y": 0, "width": 24, "height": 24}}
                    for i in range(23)]}]},
            "styles": {"S:bg1": {"name": "color/bg", "styleType": "FILL"}, "S:bg2": {"name": "color/accent", "styleType": "FILL"},
                       "S:h1": {"name": "type/h1", "styleType": "TEXT"}}}


def _walk(node):
    yield node
    for c in node.get("children", []) or []:
        yield from _walk(c)


def figma_tokens(doc):
    styles = doc["styles"]
    tok = {"color": {}, "type": {}, "spacing": {}}
    for n in _walk(doc["document"]):
        for kind, sid in (n.get("styles") or {}).items():
            st = styles.get(sid, {})
            if st.get("styleType") == "FILL" and n.get("fills"):
                c = n["fills"][0]["color"]
                tok["color"][st["name"]] = hexc((c["r"] * 255, c["g"] * 255, c["b"] * 255))
            if st.get("styleType") == "TEXT" and n.get("style"):
                s = n["style"]
                tok["type"][st["name"]] = {"family": s["fontFamily"], "size": s["fontSize"], "weight": s["fontWeight"], "line": s["lineHeightPx"]}
        if n.get("layoutMode"):
            tok["spacing"]["%s/gap" % n["name"].lower()] = n["itemSpacing"]
            tok["spacing"]["%s/pad" % n["name"].lower()] = [n["paddingTop"], n["paddingLeft"]]
    return tok


@card("ABUILD-40")
def figma_rest_tokens_export(task, wd):
    """Walk a GET-file response for colour/type/spacing tokens, batch image exports by node id, and fetch through a
    local mock of the REST API that answers 429 twice: exponential backoff + a response cache."""
    import urllib.request
    import urllib.error
    doc = _figma_file()
    tok = figma_tokens(doc)
    css = ":root{" + "".join("--%s:%s;" % (k.replace("/", "-"), v) for k, v in tok["color"].items()) + "}"
    (wd / "tokens.css").write_text(css, encoding="utf-8")
    write_json(wd, "tokens.json", tok)
    ids = [n["id"] for n in _walk(doc["document"]) if n.get("type") == "COMPONENT"]
    batches = [ids[i:i + 10] for i in range(0, len(ids), 10)]
    hits = {"n": 0, "429": 0}

    class Api(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_GET(self):
            hits["n"] += 1
            if hits["n"] <= 2:
                hits["429"] += 1
                self.send_response(429)
                self.send_header("Retry-After", "0")
                self.end_headers()
                return
            q = self.path.split("ids=")[1].split("&")[0].split(",")
            body = json.dumps({"images": {i: "https://figma-alpha-api.s3/%s.svg" % i for i in q}}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body)
    srv, base = serve_dir(None, Api)
    cache, delays = {}, []

    def get(url, backoff=True):
        if url in cache:
            return cache[url]
        for attempt in range(5):
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers={"X-Figma-Token": "fixture"}), timeout=5) as r:
                    cache[url] = json.loads(r.read())
                    return cache[url]
            except urllib.error.HTTPError as e:
                if e.code != 429 or not backoff:
                    raise
                d = 0.02 * (2 ** attempt)
                delays.append(d)
                time.sleep(d)
        raise RuntimeError("gave up")
    try:
        naive_err = None
        hits["n"] = 0
        try:
            get(base + "/v1/images/KEY?ids=%s&format=svg" % ",".join(batches[0]), backoff=False)
        except Exception as e:
            naive_err = getattr(e, "code", str(e))
        hits["n"], hits["429"] = 0, 0
        images = {}
        for b in batches:
            images.update(get(base + "/v1/images/KEY?ids=%s&format=svg" % ",".join(b))["images"])
        before = hits["n"]
        for b in batches:                                     # a second sync is served from the cache
            get(base + "/v1/images/KEY?ids=%s&format=svg" % ",".join(b))
        after = hits["n"]
    finally:
        srv.shutdown()
    out = write_json(wd, "export-map.json", images)
    return [check("colour tokens converted to exact hex", tok["color"] == {"color/bg": "#0b1020", "color/accent": "#e7b65a"}, tok["color"]),
            check("type token carries family/size/weight", tok["type"]["type/h1"] == {"family": "Cairo", "size": 32, "weight": 800, "line": 40}, tok["type"]),
            check("spacing tokens from auto-layout", tok["spacing"]["offer/gap"] == 24 and tok["spacing"]["home/pad"] == [32, 24], tok["spacing"]),
            check("23 component ids exported in 3 batches of <=10", [len(b) for b in batches] == [10, 10, 3] and len(images) == 23,
                  [len(b) for b in batches], [10, 10, 3]),
            check("two 429s absorbed by exponential backoff", hits["429"] == 2 and delays == [0.02, 0.04], [hits["429"], delays], [2, [0.02, 0.04]]),
            check("cache: re-sync makes no new requests", after == before, [before, after]),
            check("negative control: without backoff the first export call fails with 429", naive_err == 429, naive_err, 429)], \
        [wd / "tokens.css", out, wd / "tokens.json"]


def parse_figma_url(url):
    m = re.match(r"https://(?:www\.)?figma\.com/(?:file|design|proto)/([A-Za-z0-9]+)/[^?]*(?:\?(.*))?$", url)
    if not m:
        raise ValueError("not a figma url")
    q = dict(kv.split("=", 1) for kv in (m.group(2) or "").split("&") if "=" in kv)
    node = q.get("node-id")
    return m.group(1), (node.replace("-", ":") if node else None)


@card("ABUILD-41")
def figma_url_pull(task, wd):
    """Parse file key and node-id (- to :), try MCP then REST with FIGMA_PAT and stop if it is missing; with a
    replayed file response, discover pages/frames and write the export list for downstream skills."""
    url = "https://www.figma.com/design/AbC123xyz/KOSIF-UI?node-id=12-34&t=Qx9"
    key, node = parse_figma_url(url)

    def pull(env, mcp_available, replay=None):
        if mcp_available:
            return {"route": "mcp"}
        if not env.get("FIGMA_PAT"):
            return {"route": "stop", "reason": "FIGMA_PAT (file_content:read) missing: authenticate before pulling"}
        doc = replay
        pages = [{"page": c["name"], "frames": [f["name"] for f in c.get("children", []) if f["type"] in ("FRAME", "COMPONENT")][:5]}
                 for c in doc["document"]["children"]]
        return {"route": "rest", "pages": pages, "export": [f["id"] for c in doc["document"]["children"] for f in c.get("children", [])
                                                           if f["type"] == "FRAME"]}
    stopped = pull({}, False)
    pat = "figd" + "_" + "x" * 20
    pulled = pull({"FIGMA_PAT": pat}, False, _figma_file())
    out = write_json(wd, "figma-pull.json", {"file_key": key, "node_id": node, "no_token": stopped, "pulled": pulled})
    naive_node = url.split("node-id=")[1].split("&")[0]
    return [check("file key parsed", key == "AbC123xyz", key, "AbC123xyz"),
            check("node-id converted 12-34 -> 12:34", node == "12:34", node, "12:34"),
            check("no MCP and no FIGMA_PAT: stops with the reason", stopped["route"] == "stop", stopped["route"], "stop"),
            check("REST route discovers both pages and the frames", pulled["pages"][0] == {"page": "Mobile", "frames": ["Home", "Offer"]}
                  and pulled["export"] == ["1:1", "1:2"], pulled["pages"][0]),
            check("the token never lands in the written output", pat not in out.read_text()),
            check("negative control: the raw URL node id is not an API node id", not re.fullmatch(r"\d+:\d+", naive_node), naive_node, "not N:N")], [out]


_PLAN_NODES = {"frame": {"w": 360, "h": 300, "fill": "#0b1020"},
               "nodes": [{"id": "title", "x": 24, "y": 32, "w": 312, "h": 40, "fill": "#e7b65a"},
                         {"id": "body", "x": 24, "y": 88, "w": 312, "h": 120, "fill": "#1f2a44"},
                         {"id": "cta", "x": 24, "y": 224, "w": 160, "h": 48, "fill": "#2f5bff", "radius": 12}]}


def _build_from_plan(plan, bugs=None):
    bugs = bugs or {}
    f = plan["frame"]
    els = []
    for n in plan["nodes"]:
        x = n["x"] + bugs.get(n["id"], {}).get("dx", 0)
        w = n["w"] + bugs.get(n["id"], {}).get("dw", 0)
        els.append('<div id="%s" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;height:%dpx;background:var(--%s);border-radius:%dpx"></div>'
                   % (n["id"], x, n["y"], w, n["h"], n["id"], n.get("radius", 0)))
    css = ":root{%s}" % "".join("--%s:%s;" % (n["id"], n["fill"]) for n in plan["nodes"])
    return '<style>%s</style><div id=frame style="position:relative;width:%dpx;height:%dpx;background:%s">%s</div>' % (css, f["w"], f["h"], f["fill"], "".join(els))


@card("ABUILD-42")
def figma_plan_build_diff(task, wd):
    """Measured plan from Figma nodes -> build -> measure the built screen in Chrome -> diff against the plan -> fix ->
    re-measure; plus a version diff of two node sets into a code-update checklist."""
    plan = _PLAN_NODES
    write_json(wd, "plan.json", plan)
    js = ("const f=document.getElementById('frame').getBoundingClientRect();const o={};"
          "for(const id of %s){const r=document.getElementById(id).getBoundingClientRect();o[id]=[r.left-f.left,r.top-f.top,r.width,r.height,getComputedStyle(document.getElementById(id)).backgroundColor]}return o;"
          % json.dumps([n["id"] for n in plan["nodes"]]))

    def measure(name, body):
        out, _, _ = chrome_page(wd, name, html_doc(body, js), (400, 340))
        dev = {}
        for n in plan["nodes"]:
            x, y, w, h, bg = out[n["id"]]
            d = max(abs(x - n["x"]), abs(y - n["y"]), abs(w - n["w"]), abs(h - n["h"]))
            col = "#%02x%02x%02x" % tuple(int(v) for v in re.findall(r"\d+", bg)[:3])
            dev[n["id"]] = {"px": d, "colour_ok": col == n["fill"]}
        return dev
    first = measure("build_v1", _build_from_plan(plan, {"cta": {"dx": 8, "dw": -16}, "body": {"dw": 6}}))
    bad = [k for k, v in first.items() if v["px"] > 1]
    second = measure("build_v2", _build_from_plan(plan))
    v2 = json.loads(json.dumps(plan))
    v2["nodes"][2]["w"], v2["nodes"][0]["fill"] = 200, "#ffb020"
    checklist = ["%s.%s: %s -> %s" % (a["id"], k, a[k], b[k]) for a, b in zip(plan["nodes"], v2["nodes"]) for k in a if a[k] != b[k]]
    out = write_json(wd, "diff-report.json", {"first_build": first, "after_fix": second, "version_checklist": checklist})
    return [check("first build deviations found on body and cta", sorted(bad) == ["body", "cta"], bad, ["body", "cta"]),
            check("after the fix every node is within 1 px", all(v["px"] <= 1 for v in second.values()), {k: v["px"] for k, v in second.items()}),
            check("colours map to tokens and render exactly", all(v["colour_ok"] for v in second.values())),
            check("version diff yields the exact 2-item checklist", checklist == ["title.fill: #e7b65a -> #ffb020", "cta.w: 160 -> 200"], checklist),
            check("negative control: the unfixed build fails the 1 px tolerance", not all(v["px"] <= 1 for v in first.values()),
                  {k: v["px"] for k, v in first.items()})], [out, wd / "build_v2.html"]


@card("ABUILD-45")
def brand_landing_scroll3d(task, wd):
    """Brand interview -> one HTML landing page with CSS 3D and a scrubbed GSAP ScrollTrigger card; scroll positions
    are driven in Chrome and the six conversion checks are audited on the live DOM."""
    brand = {"name": "KOSIF", "primary": "#0b1020", "accent": "#e7b65a", "font": "DejaVu Sans", "audience": "creators"}
    body = ("<header id=hero style='height:560px;background:%(primary)s;color:#fff;padding:40px'><h1 id=h1>%(name)s motion studio</h1>"
            "<a id=cta href='#form' style='display:inline-block;padding:14px 28px;background:%(accent)s;color:#0b1020'>Start free</a></header>"
            "<section id=stage style='box-sizing:border-box;height:900px;perspective:900px;padding-top:200px'><div id=card style='width:300px;height:200px;margin:auto;"
            "background:%(accent)s;transform-style:preserve-3d'></div></section>"
            "<section id=trust><p class=quote>“Fastest edits we shipped.” — Studio A</p><p class=quote>“Arabic type done right.” — Studio B</p></section>"
            "<form id=form><label for=email>Email</label><input id=email type=email required><button type=submit>Join</button></form>"
            "<div style='height:600px'></div>") % brand
    measure = ("gsap.registerPlugin(ScrollTrigger);const tl=gsap.to('#card',{rotationY:180,ease:'none',scrollTrigger:{trigger:'#stage',start:'top top',end:'bottom top',scrub:true}});"
               "const o={rot:[]};const T0=document.getElementById('stage').offsetTop;for(const y of [0,T0,T0+450,T0+900]){window.scrollTo(0,y);ScrollTrigger.update();tl.scrollTrigger&&tl.scrollTrigger.update();o.rot.push(+gsap.getProperty('#card','rotationY').toFixed(2));}"
               "window.scrollTo(0,0);ScrollTrigger.update();const cta=document.getElementById('cta').getBoundingClientRect();"
               "o.audit={above_fold_cta:cta.bottom<=innerHeight,headline:!!document.querySelector('#hero h1'),trust:document.querySelectorAll('.quote').length,"
               "form_labelled:!!document.querySelector('label[for=email]')&&document.getElementById('email').type==='email',"
               "persp:getComputedStyle(document.getElementById('stage')).perspective,external_scripts:[...document.scripts].filter(s=>s.src).length,"
               "cta_contrast_bg:getComputedStyle(document.getElementById('cta')).backgroundColor};return o;")
    out, page, _ = chrome_page(wd, "landing", html_doc(body, measure, [GSAP, SCROLLTRIGGER]), (1000, 600), budget=2500)
    bare = "<header><h1>Untitled</h1></header><section id=stage style='height:900px'><div id=card></div></section><div style='height:600px'></div>"
    neg, _, _ = chrome_page(wd, "landing_bare", html_doc(bare, "const o={rot:[]};for(const y of [0,560,1010]){window.scrollTo(0,y);o.rot.push(+gsap.getProperty('#card','rotationY'))}"
                                                     "o.cta=!!document.getElementById('cta');o.trust=document.querySelectorAll('.quote').length;return o;", [GSAP]), (1000, 600))
    rot, a = out["rot"], out["audit"]
    six = [a["above_fold_cta"], a["headline"], a["trust"] >= 2, a["form_labelled"], a["persp"] == "900px", a["external_scripts"] == 0]
    return [check("scroll scrubs the 3D card 0 -> 180 deg monotonically", rot[0] == 0 and abs(rot[-1] - 180) < 1 and rot == sorted(rot), rot, [0, "...", 180]),
            check("mid-scroll is mid-rotation", 30 < rot[1] < 150 or 30 < rot[2] < 150, rot[1:3]),
            check("conversion audit: all six dimensions pass", all(six), six, [True] * 6),
            check("CTA painted in the brand accent", a["cta_contrast_bg"] == "rgb(231, 182, 90)", a["cta_contrast_bg"]),
            check("negative control: a page without the trigger never rotates and fails the audit",
                  not (neg["rot"][-1] > 1) and not neg["cta"] and neg["trust"] == 0, neg)], [page]


def _probe_curl(url, timeout=3):
    env = {k: v for k, v in os.environ.items() if k.lower() not in ("http_proxy", "https_proxy", "all_proxy")}
    done = subprocess.run(["curl", "-sS", "--noproxy", "*", "-o", "/dev/null", "-m", str(timeout), "--connect-timeout", "2", "-w",
                           '{"dns":%{time_namelookup},"connect":%{time_connect},"ttfb":%{time_starttransfer},"total":%{time_total},"code":"%{http_code}"}',
                           url], capture_output=True, text=True, env=env, timeout=timeout + 5, stdin=subprocess.DEVNULL)
    t = json.loads(done.stdout) if done.stdout.strip().startswith("{") else {}
    if "code" in t:
        t["code"] = int(t["code"])
    return done.returncode, t


def fault_domain(probes):
    """Observed / Inferred / Unknown lines and one fault domain from bounded read-only probes."""
    lines, domain, conf = [], "unknown", "low"
    if not probes:
        return {"domain": "unknown", "confidence": "low", "lines": ["Unknown: no probe evidence"]}
    lan = probes.get("local")
    if lan and lan[0] != 0:
        lines.append("Observed: the known local target fails too (curl exit %d)" % lan[0])
        return {"domain": "lan", "confidence": "medium", "lines": lines + ["Inferred: local network or host stack"]}
    rc, t = probes["target"]
    lines.append("Observed: local target answered" if lan else "Unknown: no local comparison")
    if rc == 6:
        domain, conf = "dns", "high"
        lines += ["Observed: curl exit 6 (name did not resolve)", "Inferred: resolver/DNS for this name"]
    elif rc == 7:
        domain, conf = "remote-service", "high"
        lines += ["Observed: name resolved, TCP connect refused (exit 7)", "Inferred: the service is not listening"]
    elif rc == 28:
        domain, conf = ("remote-service", "medium") if t.get("connect", 0) > 0 else ("upstream-path", "low")
        lines += ["Observed: timed out after connect=%.3fs (exit 28)" % t.get("connect", 0), "Inferred: service accepted but did not answer"]
    elif rc == 0 and t.get("code", 0) < 500:
        domain, conf = "none", "high"
        lines.append("Observed: HTTP %s in %.3fs" % (t.get("code"), t.get("total", 0)))
    else:
        domain = "remote-service"
        lines.append("Observed: HTTP %s" % t.get("code"))
    return {"domain": domain, "confidence": conf, "lines": lines}


@card("ABUILD-52")
def network_fault_localise(task, wd):
    """Bounded read-only probes (curl -w dns/connect/ttfb/total with timeouts) against local fixtures: a healthy
    server, an unresolvable name, a refused port and a server that accepts but never answers."""
    site = wd / "site"
    site.mkdir(exist_ok=True)
    (site / "index.html").write_text("ok", encoding="utf-8")
    srv, base = serve_dir(site)
    hang = socket.socket()
    hang.bind(("127.0.0.1", 0))
    hang.listen(1)
    closed = free_port()
    try:
        local = _probe_curl(base + "/index.html")
        cases = {"healthy": base + "/index.html", "dns": "http://kosif-probe.invalid/", "refused": "http://127.0.0.1:%d/" % closed,
                 "hang": "http://127.0.0.1:%d/" % hang.getsockname()[1]}
        res = {k: fault_domain({"local": local, "target": _probe_curl(u, timeout=2)}) for k, u in cases.items()}
    finally:
        srv.shutdown()
        hang.close()
    out = write_json(wd, "fault-report.json", res)
    got = {k: v["domain"] for k, v in res.items()}
    exp = {"healthy": "none", "dns": "dns", "refused": "remote-service", "hang": "remote-service"}
    labelled = all(l.split(":")[0] in ("Observed", "Inferred", "Unknown") for v in res.values() for l in v["lines"])
    none = fault_domain({})
    return [check("each fixture localised to its fault domain", got == exp, got, exp),
            check("every line labelled Observed / Inferred / Unknown", labelled),
            check("DNS and refused verdicts carry high confidence", res["dns"]["confidence"] == "high" and res["refused"]["confidence"] == "high"),
            check("negative control: with no probe evidence the domain stays unknown", none["domain"] == "unknown", none["domain"], "unknown")], [out]


# ═════════════════════════════════════════════ arabic-language ═════════════════════════════════════════════
def render_ar_lines(path, lines, size=56, fnt=FREESERIF, width=1100):
    from PIL import Image, ImageDraw
    f = font(fnt, size)
    im = Image.new("L", (width, 40 + int(size * 1.8) * len(lines)), 255)
    d = ImageDraw.Draw(im)
    for i, ln in enumerate(lines):
        d.text((width - 30, 20 + i * int(size * 1.8)), ln, font=f, fill=0, direction="rtl", language="ar", anchor="ra")
    im.save(path)
    return Path(path)


_BIDI = "‎‏؜‪‫‬‭‮"
_AR_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")


def tesseract(img, lang="ara", psm=6):
    env = dict(os.environ, OMP_THREAD_LIMIT="1")
    done = subprocess.run(["tesseract", str(img), "-", "-l", lang, "--psm", str(psm)], capture_output=True, text=True,
                          timeout=30, env=env, stdin=subprocess.DEVNULL)
    if done.returncode:
        raise RuntimeError("tesseract failed: " + done.stderr[-300:])
    return done.stdout


@card("ARL-14")
def tesseract_arabic_ocr(task, wd):
    """tesseract -l ara --psm 6 on rendered Arabic lines; strip LRM/RLM marks, compare words with the source, and
    verify every number token separately (the card: words read well, digits and % must always be re-checked)."""
    words = "ارتفعت المبيعات في شهر مارس"
    nums = "نمو ٢٥٪ في عام ٢٠٢٤"
    img = render_ar_lines(wd / "lines.png", [words, nums])
    raw = tesseract(img)
    text = "".join(ch for ch in raw if ch not in _BIDI)
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    marks = sum(raw.count(c) for c in _BIDI)
    src_nums = re.findall(r"\d+", nums.translate(_AR_DIGITS))
    ocr_nums = re.findall(r"\d+", " ".join(lines[1:]).translate(_AR_DIGITS))
    report = {"ocr": lines, "bidi_marks_removed": marks,
              "numbers": [{"source": s, "ocr": ocr_nums[i] if i < len(ocr_nums) else None,
                           "ok": i < len(ocr_nums) and ocr_nums[i] == s} for i, s in enumerate(src_nums)],
              "rule": "never trust OCR digits or %: verify every number against the image/source (ARL-15)"}
    out = write_json(wd, "ocr-report.json", report)
    (wd / "ocr.txt").write_text(text, encoding="utf-8")
    blank = render_ar_lines(wd / "blank.png", [""])
    neg = "".join(ch for ch in tesseract(blank) if ch not in _BIDI).strip()
    word_hits = sum(w in (lines[0] if lines else "") for w in words.split())
    return [check("Arabic words line read exactly", lines and lines[0] == words, lines[:1], words),
            check("every source word recovered", word_hits == 5, word_hits, 5),
            check("each source number gets its own verification row", len(report["numbers"]) == 2 and [r["source"] for r in report["numbers"]] == ["25", "2024"],
                  [r["source"] for r in report["numbers"]], ["25", "2024"]),
            check("output has no bidi control marks left", not any(c in text for c in _BIDI)),
            check("negative control: a blank page yields no Arabic words", not re.search(r"[؀-ۿ]{2,}", neg), neg, "")], [out, img]


_BW_PAIRS = [("ء", "'"), ("آ", "|"), ("أ", ">"), ("ؤ", "&"), ("إ", "<"), ("ئ", "}"), ("ا", "A"), ("ب", "b"), ("ة", "p"),
             ("ت", "t"), ("ث", "v"), ("ج", "j"), ("ح", "H"), ("خ", "x"), ("د", "d"), ("ذ", "*"), ("ر", "r"), ("ز", "z"),
             ("س", "s"), ("ش", "$"), ("ص", "S"), ("ض", "D"), ("ط", "T"), ("ظ", "Z"), ("ع", "E"), ("غ", "g"), ("ـ", "_"),
             ("ف", "f"), ("ق", "q"), ("ك", "k"), ("ل", "l"), ("م", "m"), ("ن", "n"), ("ه", "h"), ("و", "w"), ("ى", "Y"),
             ("ي", "y"), ("\u064b", "F"), ("\u064c", "N"), ("\u064d", "K"), ("\u064e", "a"), ("\u064f", "u"), ("\u0650", "i"),
             ("\u0651", "~"), ("\u0652", "o"), ("\u0670", "`"), ("\u0671", "{")]
_BW = dict(_BW_PAIRS)
_BW_INV = {v: k for k, v in _BW.items()}


def ar2bw(s):
    return "".join(_BW.get(c, c) for c in s)


def bw2ar(s):
    return "".join(_BW_INV.get(c, c) for c in s)


@card("ARL-18")
def buckwalter_names_policy(task, wd):
    """Lossless Buckwalter for machine transliteration (exact round trip), while people's names in the keep list keep
    the Latin spelling they use; Arabizi is detected and left for the user to confirm, never auto-converted."""
    s = "مُحَمَّدٌ يَقْرَأُ القُرْآنَ"
    bw = ar2bw(s)
    back = bw2ar(bw)
    keep = {"محمد صلاح": "Mohamed Salah", "كوزيف": "KOSIF"}

    def for_readers(text):
        for ar, latin in keep.items():
            text = text.replace(ar, "\u0000%s\u0000" % latin)
        parts = text.split("\u0000")
        return "".join(p if i % 2 else ar2bw(p) for i, p in enumerate(parts))
    reader = for_readers("سجل محمد صلاح هدفا مع كوزيف")

    def arabizi(text):
        return bool(re.search(r"[A-Za-z]+[2357][A-Za-z]*", text))
    lossy = "".join({"ُ": "", "َ": "", "ّ": "", "ٌ": "", "ْ": "", "ِ": ""}.get(c, c) for c in s)
    out = write_json(wd, "translit.json", {"source": s, "buckwalter": bw, "round_trip": back, "reader": reader,
                                           "arabizi_needs_confirmation": arabizi("ana 3ayez a7ki m3ak")})
    return [check("Buckwalter output matches the card's known answer", bw == "muHama~dN yaqora>u Alquro|na", bw, "muHama~dN yaqora>u Alquro|na"),
            check("round trip is exact", back == s, back, s),
            check("names keep their own Latin spelling", "Mohamed Salah" in reader and "KOSIF" in reader and "mHmd" not in reader, reader),
            check("Arabizi chat is flagged for confirmation, a name is not", arabizi("ana 3ayez a7ki m3ak") and not arabizi("Mohamed Salah")),
            check("negative control: a diacritic-dropping romanizer does not round-trip", bw2ar(ar2bw(lossy)) != s, ar2bw(lossy), "!= source")], [out]


@card("ARL-21")
def spacy_arabic_rules(task, wd):
    """spaCy blank('ar') tokenisation and a PhraseMatcher rule for 'يوم الجمعة' (NER models are a download, not used)."""
    import spacy
    from spacy.matcher import PhraseMatcher
    nlp = spacy.blank("ar")
    doc = nlp("سنلتقي يوم الجمعة في القاهرة بعد الصلاة.")
    pm = PhraseMatcher(nlp.vocab)
    pm.add("FRIDAY", [nlp.make_doc("يوم الجمعة")])
    hits = [(doc[a:b].text, a, b) for _, a, b in pm(doc)]
    neg = nlp("سنلتقي يوم السبت في القاهرة.")
    out = write_json(wd, "spacy.json", {"version": spacy.__version__, "tokens": [t.text for t in doc], "matches": hits})
    return [check("8 tokens with the full stop split off", len(doc) == 8 and doc[-1].text == ".", [t.text for t in doc], 8),
            check("rule matched 'يوم الجمعة' at tokens 1-3", hits == [("يوم الجمعة", 1, 3)], hits),
            check("negative control: a sentence about Saturday has no match", pm(neg) == [], len(pm(neg)), 0)], [out]


# ═════════════════════════════════════════════ HyperFrames registry (real CLI, mounted in Chrome) ═════════════════════════════════════════════
def hf_add(wd, item):
    """`hyperframes add <item>` into wd/hf with the real CLI; returns the installed HTML path."""
    if not (HF_CLI.exists() and NODE):
        raise RuntimeError("hyperframes CLI not available")
    hf = Path(wd) / "hf"
    hf.mkdir(exist_ok=True)
    env = dict(os.environ, NODE_PATH=str(NODE_MODULES), CHROME_PATH=str(CHROME), PUPPETEER_EXECUTABLE_PATH=str(CHROME),
               HOME=str(hf), PATH=str(Path(NODE).parent) + ":" + os.environ.get("PATH", "/usr/bin:/bin"))
    done = subprocess.run([NODE, str(HF_CLI), "add", item, "--no-clipboard", "--json", "--dir", str(hf)], capture_output=True,
                          text=True, timeout=60, cwd=str(hf), env=env, stdin=subprocess.DEVNULL)
    line = [l for l in done.stdout.strip().splitlines() if l.startswith("{")]
    res = json.loads(line[-1]) if line else {"ok": False, "error": done.stderr[-300:]}
    if not res.get("ok"):
        raise RuntimeError("hyperframes add %s failed: %s" % (item, json.dumps(res.get("error"))[:300]))
    return Path([w for w in res["written"] if w.endswith(".html")][0])


_HF_MOUNT = r"""const __t=document.querySelector('body > template'); if(__t){const host=document.getElementById('HOST');
host.appendChild(__t.content.cloneNode(true)); for(const s of [...host.querySelectorAll('script')]){const n=document.createElement('script');
n.textContent=s.textContent; s.replaceWith(n);} }"""


def hf_run(wd, path, comp_id, measure_js, variables=None, duration=None, size=(1920, 1080), name=None):
    """Mount an installed registry item with the local GSAP (the CDN tag removed), pass composition variables the way
    the runtime does, then run `measure_js` with TL = window.__timelines[comp_id]."""
    src = Path(path).read_text(encoding="utf-8")
    src = re.sub(r'<script src="https://cdn\.jsdelivr\.net/npm/gsap@[^"]*"></script>', "", src)
    if duration is not None:
        src = re.sub(r'data-duration="[0-9.]+"', 'data-duration="%s"' % duration, src)
    pre = ("<script>window.__hyperframes={getVariables:()=>(%s)};</script><script>%s</script>"
           % (json.dumps(variables or {}, ensure_ascii=False), GSAP.read_text(encoding="utf-8")))
    src = src.replace("<head>", "<head>" + pre, 1) if "<head>" in src else pre + src
    run = ("<div id=HOST style='position:relative;width:%dpx;height:%dpx;overflow:hidden'></div><pre id=\"OUT\" style=\"display:none\"></pre><script>"
           "window.addEventListener('load',()=>{try{%s}catch(e){};let __n=0;const tick=()=>{try{const TL=(window.__timelines||{})[%s];"
           "if(!TL&&__n++<100){return setTimeout(tick,20)};const SEEK=t=>{TL.seek(t,false);return t};"
           "const R=e=>{const r=e.getBoundingClientRect();return [r.left,r.top,r.width,r.height]};const __r=(()=>{%s})();"
           "document.getElementById('OUT').textContent=JSON.stringify(__r)}catch(e){document.getElementById('OUT').textContent="
           "JSON.stringify({__error:String(e)+' '+(e.stack||'')})}};tick();});</script>") % (size[0], size[1], _HF_MOUNT, json.dumps(comp_id), measure_js)
    src = src.replace("</body>", run + "</body>", 1)
    out, page, _ = chrome_page(wd, name or comp_id.replace("-", "_"), src, size, budget=3000)
    return out, page


@card("BRAND-25")
def hf_logo_sting_tiles(task, wd):
    """`hyperframes add logo-sting` and `wordmark-tiles`: the sting lands from scale 1.15 at the impact, fires one
    ring and exactly one white frame, then holds dead still; the tile wordmark builds its grid from `columns`."""
    p = hf_add(wd, "logo-sting")
    js = ("const w=document.querySelector('.ls-wordmark'),ring=document.querySelector('.ls-ring'),fl=document.querySelector('.ls-flash');"
          "const st=t=>{SEEK(t);return {s:+gsap.getProperty(w,'scale').toFixed(4),ring:+getComputedStyle(ring).opacity,flash:+getComputedStyle(fl).opacity,text:w.textContent}};"
          "return {dur:TL.labels.end,root:+document.getElementById('root').dataset.duration,t0:st(0),t54:st(0.54),t56:st(0.56),t60:st(0.6),t12:st(1.2),t21:st(2.1)};")
    o, page = hf_run(wd, p, "logo-sting", js, {"wordmark": "KOSIF", "accent": "blue"})
    t = hf_add(wd, "wordmark-tiles")
    js2 = "return {n:document.querySelectorAll('.wt-tile').length,cols:getComputedStyle(document.querySelector('.wt-grid')).getPropertyValue('--wt-columns').trim(),dur:TL.duration()};"
    a, _ = hf_run(wd, t, "wordmark-tiles", js2, {"text": "KOSIF", "columns": 12}, name="tiles12")
    b, _ = hf_run(wd, t, "wordmark-tiles", js2, {"text": "KOSIF", "columns": 10}, name="tiles10")
    out = write_json(wd, "sting.json", {"sting": o, "tiles12": a, "tiles10": b})
    return [check("sting is 2.2 s (inside the 2-4 s band): end label == root data-duration", abs(o["dur"] - 2.2) < 1e-6 and o["root"] == 2.2 and 2 <= o["dur"] <= 4, [o["dur"], o["root"]], 2.2),
            check("wordmark lands from scale 1.15 to 1 by the 0.55 s impact", o["t0"]["s"] == 1.15 and o["t56"]["s"] == 1.0, [o["t0"]["s"], o["t56"]["s"]], [1.15, 1.0]),
            check("exactly one white frame at impact", o["t54"]["flash"] == 0 and o["t56"]["flash"] == 1 and o["t60"]["flash"] == 0,
                  [o["t54"]["flash"], o["t56"]["flash"], o["t60"]["flash"]], [0, 1, 0]),
            check("ring fires after impact and is gone in the hold", o["t60"]["ring"] > 0.2 and o["t12"]["ring"] == 0, [o["t60"]["ring"], o["t12"]["ring"]]),
            check("hold is dead still (1.2 s == 2.1 s)", o["t12"] == o["t21"]),
            check("variables applied: wordmark text", o["t21"]["text"] == "KOSIF"),
            check("tiles: 12 columns -> 60 tiles, 10 columns -> 40 tiles", a["n"] == 60 and b["n"] == 40 and a["cols"] == "12", [a["n"], b["n"]], [60, 40]),
            check("negative control: before the impact the lockup is not settled", o["t0"]["s"] != o["t21"]["s"], o["t0"]["s"], "!= 1")], [out, page]


@card("EXPL-40")
def hf_code_blocks(task, wd):
    """`hyperframes add code-typing` (5 s, caret tracks the frontier) and `code-diff` (6 s, 2 states): seeked in
    Chrome, the caret position and typed-character count are measured per time."""
    p = hf_add(wd, "code-typing")
    js = ("const c=document.querySelector('.caret');const vis=()=>[...document.querySelectorAll('#surface .line span, #surface .line')].filter(e=>e.children.length===0&&e.textContent.trim()&&+getComputedStyle(e).opacity>0.5).reduce((n,e)=>n+e.textContent.length,0);"
          "const o=[];for(const t of [0,1,2,3,4.5]){SEEK(t);const r=c.getBoundingClientRect();o.push({t,x:Math.round(r.left),y:Math.round(r.top),n:vis()})}return {dur:TL.duration(),s:o};")
    a, page = hf_run(wd, p, "code-typing", js)
    q = hf_add(wd, "code-diff")
    b, _ = hf_run(wd, q, "code-diff", "return {dur:TL.duration(),labels:Object.keys(TL.labels||{})};", name="diff")
    out = write_json(wd, "code-blocks.json", {"typing": a, "diff": b})
    s = a["s"]
    moved = len({(x["x"], x["y"]) for x in s}) >= 4
    return [check("code-typing is a 5 s block", abs(a["dur"] - 5) < 0.05, a["dur"], 5),
            check("code-diff is a 6 s block", abs(b["dur"] - 6) < 0.05, b["dur"], 6),
            check("caret travels with the typing frontier (>=4 distinct positions)", moved, [(x["x"], x["y"]) for x in s]),
            check("negative control: at t=0 the caret has not reached its final position", (s[0]["x"], s[0]["y"]) != (s[-1]["x"], s[-1]["y"]),
                  (s[0]["x"], s[0]["y"]), "!= end")], [out, page]


@card("FMT-65")
def hf_platform_cards(task, wd):
    """`hyperframes add tiktok-follow | x-post | yt-lower-third`: sizes and durations per the card, a fictional handle
    swapped in, the lower third using elastic.out(1,0.4)."""
    res = {}
    for item, size in (("tiktok-follow", (1080, 1920)), ("x-post", (1920, 1080)), ("yt-lower-third", (1920, 1080))):
        p = hf_add(wd, item)
        src = p.read_text(encoding="utf-8")
        o, page = hf_run(wd, p, item, "SEEK(TL.duration());return {tl:TL.duration(),dur:+document.querySelector('[data-composition-id]').getAttribute('data-duration'),w:document.querySelector('[data-composition-id]').getAttribute('data-width'),"
                                      "h:document.querySelector('[data-composition-id]').getAttribute('data-height'),txt:document.body.innerText.slice(0,400)};",
                         size=size, name=item.replace("-", "_"))
        o["elastic"] = "elastic.out(1, 0.4)" in src or "elastic.out(1,0.4)" in src
        res[item] = o
    out = write_json(wd, "platform-cards.json", res)
    return [check("follow card 1080x1920 at 4.5 s", (res["tiktok-follow"]["w"], res["tiktok-follow"]["h"]) == ("1080", "1920") and abs(res["tiktok-follow"]["dur"] - 4.5) < 0.05,
                  [res["tiktok-follow"]["w"], res["tiktok-follow"]["h"], res["tiktok-follow"]["dur"]]),
            check("x-post 1920x1080 at 5 s", (res["x-post"]["w"], res["x-post"]["h"]) == ("1920", "1080") and abs(res["x-post"]["dur"] - 5) < 0.05,
                  [res["x-post"]["w"], res["x-post"]["h"], res["x-post"]["dur"]]),
            check("lower third 4.5 s with elastic.out(1,0.4)", abs(res["yt-lower-third"]["dur"] - 4.5) < 0.05 and res["yt-lower-third"]["elastic"],
                  [res["yt-lower-third"]["dur"], res["yt-lower-third"]["elastic"]]),
            check("every animation fits inside its composition duration", all(r["tl"] <= r["dur"] + 1e-6 for r in res.values()), {k: [r["tl"], r["dur"]] for k, r in res.items()}),
            check("negative control: x-post is not a vertical follow-card canvas", (res["x-post"]["w"], res["x-post"]["h"]) != ("1080", "1920"))], \
        [out, wd / "x_post.html"]


@card("UI-84")
def hf_component_hold(task, wd):
    """`hyperframes add chat-message`, mounted with variable overrides; a longer host duration only adds hold, it
    never time-stretches the entrance."""
    p = hf_add(wd, "chat-message")
    js = ("const els=[...document.querySelectorAll('#HOST *')].filter(e=>e.tagName!=='SCRIPT'&&e.tagName!=='STYLE').slice(0,60);"
          "const snap=t=>{SEEK(t);return els.map(e=>{const c=getComputedStyle(e);return c.opacity+'|'+c.transform}).join(';')};"
          "return {dur:TL.duration(),a:snap(0.3),b:snap(0.8),c:snap(1.2),sa:snap(0.15),sb:snap(0.4),sc:snap(0.6)};")
    short, page = hf_run(wd, p, "chat-message", js, duration=4, size=(1080, 1920), name="chat4")
    long_, _ = hf_run(wd, p, "chat-message", js, duration=8, size=(1080, 1920), name="chat8")
    out = write_json(wd, "hold.json", {"short_dur": short["dur"], "long_dur": long_["dur"]})
    same = short["a"] == long_["a"] and short["b"] == long_["b"] and short["c"] == long_["c"]
    return [check("host duration 4 s vs 8 s: timeline covers the host (hold grows)", long_["dur"] >= short["dur"], [short["dur"], long_["dur"]]),
            check("entrance states identical at 0.3/0.8/1.2 s (no time-stretch)", same),
            check("entrance actually animates (0.3 s state != 1.2 s state)", short["a"] != short["c"]),
            check("negative control: a time-stretched entrance differs from the reference",
                  not (long_["sa"] == short["a"] and long_["sb"] == short["b"] and long_["sc"] == short["c"]))], [out, page]


# ═════════════════════════════════════════════ brand-logo-identity ═════════════════════════════════════════════
def _sat(r, g, b):
    mx, mn = max(r, g, b) / 255.0, min(r, g, b) / 255.0
    return 0.0 if mx == 0 else (mx - mn) / mx


def colors_from_image(path):
    """Port of the studio's BRAND.colorsFromImage: 64x64 sample, alpha<128 skipped, near-black / near-white-grey
    skipped, 4096 buckets weighted 1+2*saturation, distinct colours by L1 > 90, accent fallback = primary +45% white."""
    from PIL import Image
    im = Image.open(path).convert("RGBA").resize((64, 64), Image.BILINEAR)
    h, dark, light = {}, 0, 0
    for r, g, b, a in im.getdata():
        if a < 128:
            continue
        l, s = 0.299 * r + 0.587 * g + 0.114 * b, _sat(r, g, b)
        if l < 40:
            dark += 1
            continue
        if l > 228 and s < 0.12:
            light += 1
            continue
        k = (r >> 4) << 8 | (g >> 4) << 4 | (b >> 4)
        e = h.setdefault(k, [0.0, 0, 0, 0, 0])
        e[0] += 1 + s * 2
        e[1] += r
        e[2] += g
        e[3] += b
        e[4] += 1
    buckets = sorted(([e[0], e[1] / e[4], e[2] / e[4], e[3] / e[4]] for e in h.values()), key=lambda x: -x[0])
    out = []
    for bk in buckets:
        if all(abs(o[1] - bk[1]) + abs(o[2] - bk[2]) + abs(o[3] - bk[3]) > 90 for o in out):
            out.append(bk)
        if len(out) >= 4:
            break
    if not out:
        return {"primary": "#2a2a2e", "accent": "#ffd23f", "text": "#ffffff", "bg": "#0d0d10"} if dark > light else None
    P = out[0][1:]
    A = out[1][1:] if len(out) > 1 else [v + (255 - v) * 0.45 for v in P]
    return {"primary": hexc(P), "accent": hexc(A), "text": "#ffffff",
            "bg": "#0d0d10" if dark > light * 1.5 else hexc([v * 0.15 for v in P])}


_KNOWN_FONTS = ["Cairo", "Tajawal", "Almarai", "IBM Plex Sans Arabic", "Readex Pro", "Inter", "Roboto", "Montserrat"]


def brand_from_text(txt):
    hexes = list(dict.fromkeys(m.lower() for m in re.findall(r"#[0-9a-fA-F]{6}\b", txt)))

    def named(words):
        m = re.search(r"(?:%s)[^#\n]{0,40}(#[0-9a-fA-F]{6})" % words, txt, re.I)
        return m.group(1).lower() if m else None
    pal = {"primary": named("primary|أساسي|رئيسي|main") or (hexes[0] if hexes else None),
           "accent": named("accent|secondary|ثانوي|إبراز|ابراز|highlight") or (hexes[1] if len(hexes) > 1 else None),
           "bg": named("background|bg|خلفية|dark"), "text": named("text|نص|foreground")}
    return pal, [f for f in _KNOWN_FONTS if re.search(r"\b%s\b" % re.escape(f), txt, re.I)]


def font_weight(name):
    n = name.lower()
    if re.search(r"variable|vf", n):
        return "100 900"
    for pat, w in (("black|heavy", "900"), ("extrabold", "800"), ("semibold|demibold", "600"), ("bold", "700"), ("medium", "500"), ("light|thin", "300")):
        if re.search(pat, n):
            return w
    return "400"


def import_brand(zpath):
    files = {}
    with zipfile.ZipFile(zpath) as z:
        for n in z.namelist():
            if n.endswith("/") or "__MACOSX" in n or "/." in n:
                continue
            files[n.split("/")[-1]] = z.read(n)
    imgs = [n for n in files if re.search(r"\.(png|jpe?g|svg|webp|gif)$", n, re.I)]
    logo = next((n for n in imgs if re.search(r"logo|لوجو|شعار|mark|icon|brand", n, re.I)), None) or next((n for n in imgs if n.endswith(".svg")), None) \
        or (imgs[0] if len(imgs) == 1 else None)
    fonts = {n: font_weight(n) for n in files if re.search(r"\.(ttf|otf|woff2?)$", n, re.I)}
    pal, named_fonts = {}, []
    for n, data in files.items():
        if re.search(r"\.(json|css|txt|md)$", n, re.I):
            p, f = brand_from_text(data.decode("utf-8", "replace"))
            pal.update({k: v for k, v in p.items() if v})
            named_fonts += f
    return files, logo, fonts, pal, named_fonts


@card("BRAND-09")
def brand_folder_apply(task, wd):
    """Read a brand zip: logo by name, font weights from file names, palette from a CSS guide (hex near keywords) and
    from the logo pixels; then apply: watermark at opacity 0.88 on every frame and a 2.6 s end card on the last 2.6 s."""
    from PIL import Image, ImageDraw
    np = _np()
    logo = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    d = ImageDraw.Draw(logo)
    d.ellipse((8, 8, 120, 120), fill=(231, 182, 90, 255))
    d.rectangle((44, 44, 84, 84), fill=(47, 91, 255, 255))
    logo.save(wd / "brand-logo.png")
    zp = wd / "brand.zip"
    with zipfile.ZipFile(zp, "w") as z:
        z.write(wd / "brand-logo.png", "KOSIF/brand-logo.png")
        z.writestr("KOSIF/photo.jpg", b"\xff\xd8 not a logo")
        z.writestr("KOSIF/guide.css", "/* KOSIF */ :root{ --primary: #0B1020; --accent: #E7B65A; --background-dark: #05060a; }\nbody{font-family:Cairo}")
        for f in ("Cairo-ExtraBold.ttf", "Cairo-Light.ttf", "Inter-Variable.ttf", "Inter-SemiBold.otf"):
            z.writestr("KOSIF/fonts/" + f, b"\x00\x01\x00\x00")
        z.writestr("__MACOSX/._guide.css", b"junk")
    files, logo_name, fonts, pal, named = import_brand(zp)
    img_pal = colors_from_image(wd / "brand-logo.png")
    # apply to a 8 s 9:16 film (small canvas for measuring): watermark 0.88, end card on the last 2.6 s
    W, H, fps, dur = 108, 192, 10, 8.0
    lg = np.asarray(Image.open(wd / "brand-logo.png").convert("RGBA").resize((18, 18), Image.NEAREST)).astype(float)
    frames = []
    for i in range(int(dur * fps)):
        t = i / fps
        endcard = t >= dur - 2.6
        f = np.zeros((H, W, 3))
        f[:] = rgb(pal["primary"]) if endcard else (90, 90, 90)
        x0, y0 = int(W * 0.84) - 9, int(H * 0.07)
        a = lg[..., 3:4] / 255.0 * 0.88
        f[y0:y0 + 18, x0:x0 + 18] = f[y0:y0 + 18, x0:x0 + 18] * (1 - a) + lg[..., :3] * a
        frames.append(f)
    film = write_video(wd / "branded.mp4", frames, fps)
    fr = read_video(film)
    end_start = next(i for i in range(len(fr)) if np.abs(fr[i][100, 10] - rgb(pal["primary"])).max() < 3)
    px = fr[0][int(H * 0.07) + 9, int(W * 0.84)]           # inside the blue square of the logo, over grey
    expect = 0.12 * 90 + 0.88 * np.array([47, 91, 255])
    out = write_json(wd, "brand.json", {"logo": logo_name, "fonts": fonts, "palette_css": pal, "palette_logo": img_pal, "fonts_named": named,
                                        "end_card_from_s": end_start / fps})
    return [check("logo chosen by name (not the photo)", logo_name == "brand-logo.png", logo_name),
            check("font weights guessed from file names", fonts == {"Cairo-ExtraBold.ttf": "800", "Cairo-Light.ttf": "300", "Inter-Variable.ttf": "100 900",
                                                                   "Inter-SemiBold.otf": "600"}, fonts),
            check("palette from the guide: hex next to primary/accent/background", pal == {"primary": "#0b1020", "accent": "#e7b65a", "bg": "#05060a"}, pal),
            check("logo pixels: primary = the dominant saturated gold, accent = the blue", img_pal["primary"] == "#e7b65a" and img_pal["accent"] == "#2f5bff", img_pal),
            check("named font Cairo found in the CSS", named == ["Cairo"], named),
            check("watermark blended at opacity 0.88", float(np.abs(px - expect).max()) < 4, px, expect),
            check("end card starts at 8 - 2.6 = 5.4 s", abs(end_start / fps - 5.4) < 0.11, end_start / fps, 5.4),
            check("negative control: an all-grey logo yields no palette", colors_from_image(_grey_png(wd)) is None)], [out, film]


def _grey_png(wd):
    from PIL import Image
    Image.new("RGBA", (64, 64), (240, 240, 240, 255)).save(wd / "grey.png")
    return wd / "grey.png"


@card("BRAND-27")
def smear_text_texture(task, wd):
    """The thermal-finger-trail smear with the blob replaced by a shaped Arabic word texture: fuv = uv - disp, where
    disp follows the finger's velocity with a gaussian falloff around the trail (numpy port of the shader)."""
    from PIL import Image, ImageDraw
    np = _np()
    W, H = 360, 160
    tex = Image.new("L", (W, H), 0)
    ImageDraw.Draw(tex).text((W - 20, 30), "كوزيف", font=font(FREESERIF, 96), fill=255, direction="rtl", language="ar", anchor="ra")
    tex = np.asarray(tex).astype(float)
    trail = [(60 + 12 * i, 80) for i in range(20)]               # finger moving right along y = 80
    vel = (12.0, 0.0)
    ys, xs = np.mgrid[0:H, 0:W].astype(float)
    dist = np.min([np.hypot(xs - x, ys - y) for x, y in trail], axis=0)
    fall = np.exp(-(dist / 18.0) ** 2)
    k = 1.5
    sx, sy = xs - k * vel[0] * fall, ys - k * vel[1] * fall
    import cv2
    out_img = cv2.remap(tex.astype("float32"), sx.astype("float32"), sy.astype("float32"), cv2.INTER_LINEAR)
    save_png(np.repeat(out_img[..., None], 3, axis=2), wd / "smear.png")
    save_png(np.repeat(tex[..., None], 3, axis=2), wd / "text_texture.png")

    def row_shift(a, b, y):
        best, bs = 0, 1e18
        for s in range(0, 30):
            e = float(np.sum((np.roll(a[y], s) - b[y]) ** 2))
            if e < bs:
                best, bs = s, e
        return best
    shift_trail = row_shift(tex, out_img, 80)
    far_diff = float(np.abs(out_img[:20] - tex[:20]).max())
    ink = float((tex > 127).mean())
    return [check("shaped Arabic word rendered into the texture", ink > 0.05, ink, ">0.05"),
            check("pixels on the trail are smeared along the finger direction by ~k*v = 18 px", 15 <= shift_trail <= 20, shift_trail, 18),
            check("pixels far from the trail are untouched", far_diff < 1e-3, far_diff, 0),
            check("negative control: the untreated texture has no shift", row_shift(tex, tex, 80) == 0, row_shift(tex, tex, 80), 0)], \
        [wd / "smear.png", wd / "text_texture.png"]


_THEME_ENDCARDS = {"charcoal": ("#141414", "#f2f2f2"), "sky": ("#0c2a4a", "#9fe0ff"), "gold": ("#120d05", "#e7b65a"),
                   "red": ("#d92332", "#ffffff"), "chrome": ("#0b0c0e", "#d8dde3")}


@card("BRAND-33")
def last_clip_endcard(task, wd):
    """theme.endcard appended only when i == n-1 and a user-owned brand is set; otherwise every prompt states
    'no logos/watermarks'. Clips are encoded and the last one gets a white-on-red wordmark card."""
    from PIL import Image, ImageDraw
    np = _np()

    def plan(n, brand, theme="red"):
        clips = []
        for i in range(n):
            prompt = "scene %d of the story" % (i + 1)
            if not brand:
                prompt += ", no logos/watermarks"
            clips.append({"i": i, "prompt": prompt, "endcard": bool(brand) and i == n - 1, "theme": theme})
        return clips
    p = plan(4, {"wordmark": "KOSIF", "owned": True})
    bg, ink = _THEME_ENDCARDS["red"]
    paths = []
    for c in p:
        frames = [np.full((96, 160, 3), 60.0 + 30 * c["i"]) for _ in range(10)]
        if c["endcard"]:
            card_im = Image.new("RGB", (160, 96), bg)
            ImageDraw.Draw(card_im).text((80, 48), "KOSIF", font=font(DEJAVU_B, 30), fill=ink, anchor="mm")
            frames += [np.asarray(card_im).astype(float)] * 10
        paths.append(write_video(wd / ("clip%d.mp4" % c["i"]), frames, 10))
    durs = [float(fx.probe(x)["format"]["duration"]) for x in paths]
    last = read_video(paths[-1])[-1]
    red = float((np.abs(last - rgb(bg)).max(axis=-1) < 20).mean())
    white = float((last.min(axis=-1) > 230).mean())
    nobrand = plan(4, None)
    out = write_json(wd, "plan.json", {"branded": p, "unbranded": nobrand, "durations": durs})
    return [check("only the last clip carries the end card", [c["endcard"] for c in p] == [False, False, False, True]),
            check("last clip is 1 s longer (the card), others 1 s", [round(d, 1) for d in durs] == [1.0, 1.0, 1.0, 2.0], durs, [1, 1, 1, 2]),
            check("end card is white wordmark on red", red > 0.7 and 0.01 < white < 0.3, [red, white]),
            check("without a brand: no end card, every prompt says no logos/watermarks",
                  not any(c["endcard"] for c in nobrand) and all("no logos/watermarks" in c["prompt"] for c in nobrand)),
            check("negative control: a middle clip has no red card frame", float((np.abs(read_video(paths[1])[-1] - rgb(bg)).max(axis=-1) < 20).mean()) < 0.01)], [out, paths[-1]]


@card("BRAND-37")
def eight_templates_one_palette(task, wd):
    """The eight Arabic-first motion templates (mtemplates.render_html) filled with one brand token set so all share
    one palette; each output has no unfilled placeholder and embeds the Cairo face."""
    accent = "#19C37D"
    code = ("import sys,json;sys.path.insert(0,%r);import mtemplates as mt;from pathlib import Path;wd=Path(%r);res={}\n"
            "for n,t in mt.TEMPLATES.items():\n"
            " h=mt.render_html(n,{'accent':%r,'bg1':'#0b1020','bg2':'#05060a'},1080,1920,t['seconds'] or 6.6,30);(wd/(n+'.html')).write_text(h,encoding='utf-8')\n"
            " res[n]=t['params']['accent'][0]\n"
            "print(json.dumps(res))") % (str(MM), str(wd), accent)
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=60, cwd=str(wd), stdin=subprocess.DEVNULL,
                       env=dict(os.environ, KOSIF_MOTION_HOME=str(wd / "home")))
    if r.returncode:
        raise RuntimeError("mtemplates failed: " + r.stderr[-300:])
    default_accents = {k: v.lower() for k, v in json.loads(r.stdout.strip().splitlines()[-1]).items()}
    names = list(default_accents)
    shared = {}
    for n in names:
        h = (wd / ("%s.html" % n)).read_text(encoding="utf-8")
        shared[n] = {"accent": accent.lower() in h.lower(), "bg": "#0b1020" in h.lower(), "placeholders": len(re.findall(r"\{\{[A-Z_0-9]+\}\}", h)),
                     "cairo": "Cairo" in h, "comp": "data-composition-id" in h}
    out = write_json(wd, "templates.json", shared)
    return [check("all 8 templates generated", len(names) == 8 and all((wd / ("%s.html" % n)).stat().st_size > 1000 for n in names), len(names), 8),
            check("every template carries the brand accent and ground", all(v["accent"] and v["bg"] for v in shared.values())),
            check("no unfilled placeholders, Cairo embedded, composition id present",
                  all(v["placeholders"] == 0 and v["cairo"] and v["comp"] for v in shared.values())),
            check("negative control: the untouched defaults do not share one accent", len(set(default_accents.values())) > 1,
                  sorted(set(default_accents.values())))], [out, wd / "logo-reveal.html"]


# ═════════════════════════════════════════════ characters-rigs (the repo's three-kit / shape-kit / lab-kit) ═════════════════════════════════════════════
K3_BUNDLE, SHAPE_KIT, LAB_KIT = KIT / "three-kit.bundle.js", KIT / "shape-kit.js", KIT / "lab-kit.js"


def k3_page(wd, name, js, kits=(), budget=8000):
    """Run the repo's kit in headless Chrome (canvas 2D available; no WebGL renderer is created) and return #OUT."""
    pre = "const K=window.K3,T=K.THREE;const bb=o=>{const b=new T.Box3().setFromObject(o);return [b.min.x,b.min.y,b.min.z,b.max.x,b.max.y,b.max.z]};"
    out, page, _ = chrome_page(wd, name, html_doc("", pre + js, [K3_BUNDLE, *kits]), (320, 200), budget=budget)
    return out, page


@card("CHAR-39")
def k3_flock(task, wd):
    """K3.makeFlock: 18 instanced V birds following a keyed path, flap sin(uT*9 + phase) in the vertex shader,
    visible only inside [t0, t1]."""
    js = """const path=[[0,0,50,0],[4,400,50,-100],[8,800,120,-100]];
const m=K.makeFlock({n:18,path,t0:1,t1:7,spread:120,size:9,color:'#1a1d22',seed:5});
const cen=t=>{m.userData.set(t);const p=new T.Vector3(),q=new T.Quaternion(),s=new T.Vector3(),M=new T.Matrix4();let c=[0,0,0],sc=[];
 for(let i=0;i<m.count;i++){m.getMatrixAt(i,M);M.decompose(p,q,s);c[0]+=p.x/m.count;c[1]+=p.y/m.count;c[2]+=p.z/m.count;sc.push(s.x)}return {c,sc,on:m.material.uniforms.uOn.value,uT:m.material.uniforms.uT.value}};
const a=cen(2),b=cen(3),off=cen(0.5);
return {count:m.count,a,b,off,vs:m.material.vertexShader,phase:Array.from(m.geometry.attributes.phase.array).slice(0,18)};"""
    o, page = k3_page(wd, "flock", js)
    dx = o["b"]["c"][0] - o["a"]["c"][0]
    dz = o["b"]["c"][2] - o["a"]["c"][2]
    flap = lambda t, ph: math.sin(t * 9 + ph * 2 * math.pi) * 0.8
    period = 2 * math.pi / 9
    out = write_json(wd, "flock.json", {k: o[k] for k in ("count", "a", "b")})
    return [check("18 instances", o["count"] == 18, o["count"], 18),
            check("flock centroid advances with the keyed path (+100 x, -25 z per second)", abs(dx - 100) < 8 and abs(dz + 25) < 8, [dx, dz], [100, -25]),
            check("bird scale = size 9 x (0.8..1.2)", all(7.2 - 1e-6 <= s <= 10.8 + 1e-6 for s in o["a"]["sc"]), [min(o["a"]["sc"]), max(o["a"]["sc"])], [7.2, 10.8]),
            check("shader flaps with sin(uT * 9.0 + phase); uT follows t", "sin(uT * 9.0 + phase * 6.2832)" in o["vs"] and o["a"]["uT"] == 2,
                  o["a"]["uT"], 2),
            check("flap period is 2*pi/9 s for every phase", all(abs(flap(1.0, p) - flap(1.0 + period, p)) < 1e-9 for p in o["phase"])),
            check("negative control: before t0 the flock is switched off", o["off"]["on"] == 0 and o["a"]["on"] == 1, [o["off"]["on"], o["a"]["on"]], [0, 1])], [out, page]


@card("CHAR-40")
def k3s_bunny(task, wd):
    """K3S.bunny: a procedurally sculpted plush bunny with named rig parts on pivots (neck [0,.152,.004], ears from the
    skull), eyes placed by ray hits; part rotations move only their own subtree."""
    js = """const b=K3S.bunny({fur:'#f2e4d8',belly:'#fbf3ea',pink:'#ff9fb8',nose:'#ff7c9c',scarf:'#7fe7b4',cells:96});
let tris=0;b.group.traverse(m=>{if(m.isMesh){const g=m.geometry;tris+=(g.index?g.index.count:g.attributes.position.count)/3}});
const eL=b.parts.earL,eR=b.parts.earR,ep=eL.parent;ep.remove(eL);ep.remove(eR);const box=bb(b.group);const boxE=(ep.add(eL),ep.add(eR),bb(b.group));const ear=new T.Vector3();b.parts.earL.getWorldPosition(ear);const tail0=new T.Vector3();b.parts.tail.getWorldPosition(tail0);
const tipBefore=bb(b.parts.earL);b.parts.head.rotation.z=0.4;b.group.updateMatrixWorld(true);const tipAfter=bb(b.parts.earL);const tail1=new T.Vector3();b.parts.tail.getWorldPosition(tail1);
let eyes=0;b.parts.head.traverse(m=>{if(m.userData&&m.userData.ball)eyes++});
return {parts:Object.keys(b.parts).sort(),neck:b.parts.head.position.toArray(),pivots:b.pivots,tris,h:box[4]-box[1],hE:boxE[4]-boxE[1],eyes,earMoved:Math.abs(tipAfter[0]-tipBefore[0])+Math.abs(tipAfter[1]-tipBefore[1]),tailMoved:tail1.distanceTo(tail0)};"""
    o, page = k3_page(wd, "bunny", js, [SHAPE_KIT], budget=20000)
    out = write_json(wd, "bunny.json", o)
    need = {"body", "head", "earL", "earR", "tail", "mouth", "scarf"}
    return [check("named rig parts present", need <= set(o["parts"]), o["parts"], sorted(need)),
            check("head sits on the neck pivot [0, .152, .004]", all(abs(a - b) < 1e-9 for a, b in zip(o["neck"], [0, 0.152, 0.004])), o["neck"]),
            check("about 0.33 m tall without the ears (ears add height)", 0.29 <= o["h"] <= 0.37 and o["hE"] > o["h"], [o["h"], o["hE"]], 0.33),
            check("sculpt at 96 cells exceeds 50,000 triangles", o["tris"] > 50000, o["tris"], ">50000"),
            check("two eyes placed on the face", o["eyes"] == 2, o["eyes"], 2),
            check("rotating the head carries the ears (child of the head pivot)", o["earMoved"] > 0.01, o["earMoved"]),
            check("negative control: the tail (not under the head) does not move", o["tailMoved"] < 1e-9, o["tailMoved"], 0)], [out, page]


@card("CHAR-41")
def k3_eyes(task, wd):
    """K3S.eye (glossy ball, iris ring at 55%, catch-lights .3r / .14r, clearcoat 1, ior 1.5, env 1.6) and K3.makeEye
    (sclera / emissive iris / pupil / cornea .22) with blink scaling y by 1 - .92k."""
    js = """const r=.012,e=K3S.eye({r,tall:1.12,iris:'#5a3a2c'});const ball=e.userData.ball,mat=ball.material;
const kids=e.children.map(c=>({geo:c.geometry.type,p:c.geometry.parameters,pos:c.position.toArray()}));
const L=K.makeEye(0.1,{iris:0x8fe02a});const blink=k=>{L.userData.blink(k);return L.scale.y};
const parts=L.children.map(c=>({color:c.material.color.getHexString(),op:c.material.opacity,em:c.material.emissive?c.material.emissive.getHexString():null}));
return {rough:mat.roughness,cc:mat.clearcoat,ior:mat.ior,env:mat.envMapIntensity,tall:ball.scale.y,kids,parts,b0:blink(0),b5:blink(0.5),b1:blink(1)};"""
    o, page = k3_page(wd, "eyes", js, [SHAPE_KIT, LAB_KIT])
    r = 0.012
    iris, s1, s2 = o["kids"][1], o["kids"][2], o["kids"][3]
    out = write_json(wd, "eyes.json", o)
    return [check("gloss: roughness .08, clearcoat 1, ior 1.5, env 1.6", [o["rough"], o["cc"], o["ior"], o["env"]] == [0.08, 1, 1.5, 1.6],
                  [o["rough"], o["cc"], o["ior"], o["env"]]),
            check("iris ring radius 55% of r", abs(iris["p"]["radius"] - 0.55 * r) < 1e-9, iris["p"]["radius"], 0.55 * r),
            check("catch-lights .3r and .14r, both upper/lower-outer on the front", abs(s1["p"]["radius"] - 0.3 * r) < 1e-9 and abs(s2["p"]["radius"] - 0.14 * r) < 1e-9
                  and s1["pos"][2] > 0 and s2["pos"][2] > 0, [s1["p"]["radius"], s2["p"]["radius"]]),
            check("layered eye: sclera f4f6f2, iris 8fe02a (emissive), pupil 05070a, cornea opacity .22",
                  [p["color"] for p in o["parts"]] == ["f4f6f2", "8fe02a", "05070a", "ffffff"] and abs(o["parts"][3]["op"] - 0.22) < 1e-9 and o["parts"][1]["em"] != "000000"),
            check("blink scales y by 1 - .92k", [round(o["b0"], 6), round(o["b5"], 6), round(o["b1"], 6)] == [1.0, 0.54, 0.08], [o["b0"], o["b5"], o["b1"]], [1, 0.54, 0.08]),
            check("negative control: an open eye is not a closed one", abs(o["b0"] - o["b1"]) > 0.5)], [out, page]


@card("CHAR-42")
def lab_rabbit_lion(task, wd):
    """K3.makeRabbit / makeLion: named joints, shell fur (7 / 8 layers, mane x2.6 with gravity .5); the part swap
    lerps the rabbit tail to 0x8a4a1c and scales it 1 + .45*sw over 16.4-17.2 s; six HUD beats in order."""
    js = """const R=K.makeRabbit({color:0xf1f0ea,inner:0xf3b6c0,iris:0x3a7bd5,furLength:.09,layers:7});
const Lc=K.makeLion({color:0xe3b05a,mane:0x8a4a1c,iris:0xd9a21b,muzzle:0xf5e2b8,furLength:.07,layers:8});
const shells=(root,name)=>{let g=null;root.traverse(o=>{if(o.name===name)g=o});if(!g)return null;const top=g.children[g.children.length-1].material;const sh={uniforms:{},vertexShader:'#include <begin_vertex>'};top.onBeforeCompile(sh);return {n:g.children.length,shell:sh.uniforms.uShell.value,grav:sh.uniforms.uGrav.value}};
const tail=R.userData.joints.tail.children[0];const c0=new T.Color(0xffffff);const c1=new T.Color(0x8a4a1c);
const sw=t=>Math.min(1,Math.max(0,(t-16.4)/0.8));const at=t=>{const k=sw(t);tail.material.color.copy(c0).lerp(c1,k);tail.scale.setScalar(1+.45*k);return [tail.material.color.getHexString(),+tail.scale.x.toFixed(4)]};
return {rj:Object.keys(R.userData.joints).sort(),lj:Object.keys(Lc.userData.joints).sort(),rb:shells(R,'body_fur'),lm:shells(Lc,'mane_fur'),lb:shells(Lc,'body_fur'),
 s0:at(16.0),s1:at(16.8),s2:at(17.2)};"""
    o, page = k3_page(wd, "lab", js, [LAB_KIT], budget=15000)
    beats = ["SHAPE", "JOINT", "LOAD", "BREAK", "SWAP", "RANK"]
    cuts = [0, 3.0, 6.5, 10.0, 14.0, 17.5, 20.0]
    sched = [{"beat": b, "t0": cuts[i], "t1": cuts[i + 1]} for i, b in enumerate(beats)]
    swap_in = next(s for s in sched if s["beat"] == "SWAP")
    out = write_json(wd, "lab.json", {**o, "hud": sched})
    return [check("rabbit joints named", {"head", "earL", "earR", "armL", "armR", "footL", "footR", "tail"} <= set(o["rj"]), o["rj"]),
            check("lion joints named", {"head", "legFL", "legBR", "tail", "earL"} <= set(o["lj"]), o["lj"]),
            check("rabbit fur: 7 shells, outer shell at .09", o["rb"]["n"] == 7 and abs(o["rb"]["shell"] - 0.09) < 1e-9, o["rb"]),
            check("lion mane: 8 shells... (layers 8 -> mane 8), length .07 x 2.6 with gravity .5", o["lm"]["n"] == 8 and abs(o["lm"]["shell"] - 0.182) < 1e-9
                  and abs(o["lm"]["grav"] - 0.5 * 0.182) < 1e-9, o["lm"]),
            check("lion body fur uses max(5, layers-3) = 5 shells", o["lb"]["n"] == 5, o["lb"]["n"], 5),
            check("swap: tail colour/scale 16.0 s untouched, mid at 16.8 s, done (8a4a1c, 1.45) at 17.2 s",
                  o["s0"] == ["ffffff", 1.0] and o["s2"] == ["8a4a1c", 1.45] and o["s1"][1] == 1.225, [o["s0"], o["s1"], o["s2"]]),
            check("SWAP beat window holds the 16.4-17.2 s swap", swap_in["t0"] <= 16.4 and 17.2 <= swap_in["t1"], swap_in),
            check("negative control: before the swap the tail is not the mane colour", o["s0"][0] != "8a4a1c")], [out, page]


@card("CHAR-43")
def k3_koi(task, wd):
    """K3.makeKoi: lofted 28x18 body with fins, seeded 256 px skin in four varieties, swim phase 2*pi*1.6*t and a
    bend that leans into turns (uTurn) along a path."""
    js = """const kinds=['kohaku','sanke','showa','ogon'],o={};
for(const kind of kinds){const k=K.makeKoi({length:.62,seed:7,kind,amp:.11});const cv=k.material.map.image;const g=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data;
 const near=(c,t)=>{let n=0;for(let i=0;i<g.length;i+=4){if(Math.abs(g[i]-c[0])<40&&Math.abs(g[i+1]-c[1])<40&&Math.abs(g[i+2]-c[2])<40)n++}return n/(g.length/4)};
 o[kind]={size:cv.width,red:near([226,86,32]),showaRed:near([196,52,28]),black:near([24,22,24]),gold:near([232,190,90]),cc:k.material.clearcoat,kindTag:k.userData.kind};}
const k=K.makeKoi({length:.62,seed:7,kind:'kohaku'});const straight=(t,out)=>out.set(t*0.3,0,0);const circle=(t,out)=>out.set(Math.cos(t),0,Math.sin(t));
k.userData.set(2.0,straight,1.6);const s={ph:k.userData.swim.uPh.value,turn:k.userData.swim.uTurn.value,amp:k.userData.swim.uAmpK.value,len:k.userData.swim.uLen.value,ry:k.rotation.y};
k.userData.set(2.0,circle,1.6);const c={turn:k.userData.swim.uTurn.value};const box=bb(k);return {o,s,c,len:box[3]-box[0]};"""
    o, page = k3_page(wd, "koi", js, budget=15000)
    v = o["o"]
    out = write_json(wd, "koi.json", o)
    return [check("skins are 256 px and tagged by variety", all(v[k]["size"] == 256 and v[k]["kindTag"] == k for k in v)),
            check("kohaku has red patches (#e25620), ogon has none", v["kohaku"]["red"] > 0.05 and v["ogon"]["red"] < 0.01, [v["kohaku"]["red"], v["ogon"]["red"]]),
            check("ogon is gold #e8be5a", v["ogon"]["gold"] > 0.3, v["ogon"]["gold"]),
            check("sanke and showa carry black (#181618); showa red is #c4341c", v["sanke"]["black"] > 0.01 and v["showa"]["black"] > 0.01 and v["showa"]["showaRed"] > 0.02,
                  [v["sanke"]["black"], v["showa"]["black"], v["showa"]["showaRed"]]),
            check("clearcoat .6, amp .11, length .62 (body + tail fin ~ .62-.75 m)", v["kohaku"]["cc"] == 0.6 and abs(o["s"]["amp"] - 0.11) < 1e-9 and 0.6 <= o["len"] <= 0.8, o["len"]),
            check("swim phase = 2*pi*1.6*t at t=2", abs(o["s"]["ph"] - 2 * math.pi * 1.6 * 2) < 1e-6, o["s"]["ph"], 2 * math.pi * 3.2),
            check("heading follows a straight +x path (rotation.y = 0)", abs(o["s"]["ry"]) < 1e-6, o["s"]["ry"], 0),
            check("on a circular path the bend leans into the turn", abs(o["c"]["turn"]) > 0.05, o["c"]["turn"]),
            check("negative control: a straight path has no turn lean", abs(o["s"]["turn"]) < 1e-9, o["s"]["turn"], 0)], [out, page]


@card("CHAR-44")
def toon_fisherman(task, wd):
    """Spheres and capsules on hierarchical joints: torso Capsule(.2,.42) rotated -.18, head sphere .13 + half-sphere cap
    0xcfc6b2, legs, and a rod cylinder (.008 -> .02) oriented by a quaternion from base to tip with a line to the water."""
    js = """const g=new T.Group(),hip=new T.Group();hip.position.set(0,.5,0);g.add(hip);
const torso=new T.Mesh(new T.CapsuleGeometry(.2,.42,6,12),new T.MeshToonMaterial({color:0x34495e}));torso.position.y=.35;torso.rotation.x=-.18;hip.add(torso);
const neck=new T.Group();neck.position.set(0,.72,0);hip.add(neck);const head=new T.Mesh(new T.SphereGeometry(.13,24,16),new T.MeshToonMaterial({color:0xe0b896}));neck.add(head);
const cap=new T.Mesh(new T.SphereGeometry(.135,24,12,0,Math.PI*2,0,Math.PI/2),new T.MeshToonMaterial({color:0xcfc6b2}));cap.position.y=.02;neck.add(cap);
for(const sx of [-1,1]){const leg=new T.Mesh(new T.CapsuleGeometry(.07,.38,4,8),new T.MeshToonMaterial({color:0x22313f}));leg.position.set(sx*.09,-.25,0);hip.add(leg)}
const base=new T.Vector3(.2,.8,.2),tip=new T.Vector3(1.4,1.6,.2),dir=tip.clone().sub(base),len=dir.length();
const rod=new T.Mesh(new T.CylinderGeometry(.008,.02,len,8),new T.MeshToonMaterial({color:0x5b3b22}));rod.position.copy(base).addScaledVector(dir,.5);
rod.quaternion.setFromUnitVectors(new T.Vector3(0,1,0),dir.clone().normalize());g.add(rod);
const line=new T.Line(new T.BufferGeometry().setFromPoints([tip,new T.Vector3(tip.x,0,tip.z)]),new T.LineBasicMaterial({color:0xffffff}));g.add(line);
g.updateMatrixWorld(true);const axis=new T.Vector3(0,1,0).applyQuaternion(rod.quaternion);const topEnd=new T.Vector3(0,len/2,0).applyMatrix4(rod.matrixWorld);
const hw0=new T.Vector3();head.getWorldPosition(hw0);hip.rotation.z=.3;g.updateMatrixWorld(true);const hw1=new T.Vector3();head.getWorldPosition(hw1);
const raw=new T.Vector3(0,1,0);return {torsoRot:torso.rotation.x,capColor:cap.material.color.getHexString(),capTheta:cap.geometry.parameters.thetaLength,
 r:[rod.geometry.parameters.radiusTop,rod.geometry.parameters.radiusBottom],align:axis.dot(dir.clone().normalize()),tipErr:topEnd.distanceTo(tip),
 rawAlign:raw.dot(dir.clone().normalize()),lineEnd:line.geometry.attributes.position.array[4],headMoved:hw1.distanceTo(hw0),pivotAtJoint:neck.position.toArray()};"""
    o, page = k3_page(wd, "fisherman", js)
    out = write_json(wd, "fisherman.json", o)
    return [check("torso capsule rotated -.18 rad", abs(o["torsoRot"] + 0.18) < 1e-9, o["torsoRot"], -0.18),
            check("half-sphere cap in 0xcfc6b2", o["capColor"] == "cfc6b2" and abs(o["capTheta"] - math.pi / 2) < 1e-9),
            check("rod tapers .008 -> .02", o["r"] == [0.008, 0.02], o["r"]),
            check("quaternion points the rod from base to tip (tip within 1 mm)", o["align"] > 0.9999 and o["tipErr"] < 1e-3, [o["align"], o["tipErr"]]),
            check("fishing line drops to the water (y = 0)", o["lineEnd"] == 0, o["lineEnd"], 0),
            check("hip joint rotation carries the head (hierarchy)", o["headMoved"] > 0.1, o["headMoved"]),
            check("negative control: an un-oriented cylinder does not follow the rod direction", o["rawAlign"] < 0.9, o["rawAlign"], "<0.9")], [out, page]


def _lottie_walk():
    """A tiny Lottie: a 'character' rectangle stepping up and down once per second (loop), with acting markers."""
    fr = 30
    return {"v": "5.7.4", "fr": fr, "ip": 0, "op": 225, "w": 200, "h": 200, "nm": "walker", "ddd": 0, "assets": [],
            "markers": [{"tm": 0, "cm": "walk", "dr": 90}, {"tm": 90, "cm": "stop", "dr": 30}, {"tm": 120, "cm": "point", "dr": 60}, {"tm": 180, "cm": "idle", "dr": 45}],
            "layers": [{"ddd": 0, "ind": 1, "ty": 4, "nm": "body", "sr": 1, "ip": 0, "op": 225, "st": 0, "bm": 0,
                        "ks": {"o": {"a": 0, "k": 100}, "r": {"a": 0, "k": 0}, "a": {"a": 0, "k": [0, 0, 0]}, "s": {"a": 0, "k": [100, 100, 100]},
                               "p": {"a": 1, "k": [{"t": 0, "s": [100, 120, 0], "i": {"x": [1], "y": [1]}, "o": {"x": [0], "y": [0]}},
                                                   {"t": 15, "s": [100, 100, 0], "i": {"x": [1], "y": [1]}, "o": {"x": [0], "y": [0]}},
                                                   {"t": 30, "s": [100, 120, 0], "i": {"x": [1], "y": [1]}, "o": {"x": [0], "y": [0]}},
                                                   {"t": 45, "s": [100, 100, 0], "i": {"x": [1], "y": [1]}, "o": {"x": [0], "y": [0]}},
                                                   {"t": 60, "s": [100, 120, 0], "i": {"x": [1], "y": [1]}, "o": {"x": [0], "y": [0]}},
                                                   {"t": 75, "s": [100, 100, 0], "i": {"x": [1], "y": [1]}, "o": {"x": [0], "y": [0]}},
                                                   {"t": 90, "s": [100, 120, 0]}]}},
                        "shapes": [{"ty": "rc", "d": 1, "s": {"a": 0, "k": [40, 80]}, "p": {"a": 0, "k": [0, 0]}, "r": {"a": 0, "k": 6}, "nm": "r"},
                                   {"ty": "fl", "c": {"a": 0, "k": [0.9, 0.7, 0.35, 1]}, "o": {"a": 0, "k": 100}, "r": 1, "bm": 0, "nm": "f"}]}]}


@card("CHAR-47")
def lottie_markers_gsap(task, wd):
    """The acting lives in one Lottie: lottie-web registered for seeking (goToAndStop(frame, true) from seek(t)); beat
    times come from the file's markers (tm / fr); GSAP owns the card and the camera, placed at those marker times."""
    data = _lottie_walk()
    write_json(wd, "walker.json", data)
    body = "<div id=lot style='width:200px;height:200px'></div><div id=card style='position:absolute;left:0;top:0;width:50px;height:30px;opacity:0'></div><div id=cam></div>"
    js = """const anim=lottie.loadAnimation({container:document.getElementById('lot'),renderer:'svg',loop:false,autoplay:false,animationData:%s});
const fr=anim.frameRate,beats={};for(const m of anim.animationData.markers)beats[m.cm]=m.tm/fr;
const tl=gsap.timeline({paused:true});tl.to('#card',{opacity:1,x:120,duration:.4},beats.point);tl.to('#cam',{x:-80,duration:3,ease:'none'},beats.walk);
const seek=t=>{tl.seek(t,false);anim.goToAndStop(Math.min(t*fr,anim.totalFrames-1),true)};
const yAt=t=>{seek(t);const g=document.querySelector('#lot svg g g');return g.getAttribute('transform')};
const s=[];for(const t of [0,0.5,1.0,2.0,3.9,4.1,4.4]){seek(t);s.push({t,frame:Math.round(anim.currentFrame),card:+gsap.getProperty('#card','opacity'),cam:+gsap.getProperty('#cam','x'),tf:yAt(t)})}
return {fr,beats,total:anim.totalFrames,s};""" % json.dumps(data)
    o, page, _ = chrome_page(wd, "lottie", html_doc(body, js, [LOTTIE, GSAP]), (300, 300))
    s = {round(x["t"], 1): x for x in o["s"]}
    out = write_json(wd, "lottie-beats.json", o)
    return [check("beat times read from markers (tm / fr)", o["beats"] == {"walk": 0, "stop": 3, "point": 4, "idle": 6}, o["beats"]),
            check("seek(t) drives the Lottie frame exactly (t * 30)", [s[k]["frame"] for k in (0.0, 0.5, 1.0, 2.0)] == [0, 15, 30, 60]),
            check("1 s walk cycle: pose at 0 s == pose at 1 s == 2 s, different at 0.5 s",
                  s[0.0]["tf"] == s[1.0]["tf"] == s[2.0]["tf"] and s[0.5]["tf"] != s[0.0]["tf"], [s[0.0]["tf"], s[0.5]["tf"]]),
            check("GSAP card waits for the 'point' marker (4 s) then appears", s[3.9]["card"] == 0 and 0 < s[4.1]["card"] < 1 and s[4.4]["card"] == 1,
                  [s[3.9]["card"], s[4.1]["card"], s[4.4]["card"]]),
            check("camera moves with the walk beat", s[2.0]["cam"] < s[0.0]["cam"], [s[0.0]["cam"], s[2.0]["cam"]]),
            check("negative control: before the marker the card is hidden", s[3.9]["card"] == 0)], [out, page]


# ═════════════════════════════════════════════ color-palette-grading ═════════════════════════════════════════════
def srgb_to_oklab(c):
    def lin(v):
        v = v / 255.0
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(v) for v in c)
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l, m, s = (math.copysign(abs(x) ** (1 / 3), x) for x in (l, m, s))
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)


def oklch_to_srgb(L, C, H):
    a, b = C * math.cos(math.radians(H)), C * math.sin(math.radians(H))
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    bb = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s

    def enc(v):
        v = max(0.0, min(1.0, v))
        return 255 * (12.92 * v if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055)
    return tuple(int(round(enc(v))) for v in (r, g, bb))


def oklch(c):
    L, a, b = srgb_to_oklab(c)
    return L, math.hypot(a, b), (math.degrees(math.atan2(b, a)) + 360) % 360


def uniformity(Ls):
    d = [abs(Ls[i + 1] - Ls[i]) for i in range(len(Ls) - 1)]
    return 1 - (max(d) - min(d)) / (sum(d) / len(d))


@card("COLOR-41")
def starter_tokens(task, wd):
    """The tested canvas starter opens on 'midnight teal' (tokens on :root, radial backdrop #182446 -> #0b1020 55%,
    90 px grid at .045 x .6); STYLE.md §4.1 carries five colour slots; the Remotion starter's withAlpha() appends a hex
    byte or falls back to color-mix — all read from the repo and measured."""
    st = REPO / "starters/html-canvas"
    dst = wd / "starter"
    shutil.copytree(st, dst)
    js = ("const r=getComputedStyle(document.documentElement),b=getComputedStyle(document.body),g=getComputedStyle(document.getElementById('grid'));"
          "return {bg:r.getPropertyValue('--bg').trim(),ink:r.getPropertyValue('--ink').trim(),muted:r.getPropertyValue('--muted').trim(),accent:r.getPropertyValue('--accent').trim(),"
          "accent2:r.getPropertyValue('--accent-2').trim(),backdrop:b.backgroundImage,grid:g.backgroundImage,size:g.backgroundSize,op:g.opacity};")
    src = (dst / "index.html").read_text(encoding="utf-8")
    probe = src.replace("</body>", "<pre id=\"OUT\" style=\"display:none\"></pre><script>window.addEventListener('load',()=>{try{const __r=(()=>{%s})();"
                        "document.getElementById('OUT').textContent=JSON.stringify(__r)}catch(e){document.getElementById('OUT').textContent=JSON.stringify({__error:String(e)})}})"
                        "</script></body>" % js, 1)
    (dst / "probe.html").write_text(probe, encoding="utf-8")
    done = subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--allow-file-access-from-files", "--window-size=540,960",
                           "--virtual-time-budget=1500", "--dump-dom", (dst / "probe.html").as_uri()], capture_output=True, text=True, timeout=40, stdin=subprocess.DEVNULL)
    o = json.loads(_html.unescape(re.search(r'<pre id="OUT"[^>]*>(.*?)</pre>', done.stdout, re.S).group(1)))
    style = (REPO / "templates/STYLE.md").read_text(encoding="utf-8")
    slots = dict(re.findall(r"^\| (bg|fg|accent|muted|line) \| (#[0-9A-Fa-f]{6}) \|", style, re.M))
    fa = (REPO / "starters/remotion/src/Film.tsx").read_text(encoding="utf-8")
    fn = re.search(r"export const withAlpha = \(color: string, alpha: number\): string => \{.*?\n\};", fa, re.S).group(0)
    fn = fn.replace("export const withAlpha = (color: string, alpha: number): string =>", "const withAlpha = (color, alpha) =>")
    wa, _ = node_json(wd, "withalpha", fn + "\nconsole.log(JSON.stringify([withAlpha('#19c37d', 0.3), withAlpha('#ff7a1a', 1), withAlpha('rgb(1,2,3)', 0.5)]));")
    out = write_json(wd, "tokens.json", {"starter": o, "style_md": slots, "withAlpha": wa})
    return [check("starter tokens are midnight teal", [o["bg"], o["ink"], o["muted"], o["accent"], o["accent2"]] == ["#0b1020", "#f3f7ff", "#9fb0cc", "#7ee8d2", "#ffb86b"],
                  [o["bg"], o["accent"]]),
            check("radial backdrop #182446 -> --bg at 55%", "rgb(24, 36, 70)" in o["backdrop"] and "55%" in o["backdrop"] and "rgb(11, 16, 32)" in o["backdrop"], o["backdrop"]),
            check("90 px grid of rgba(255,255,255,.045) at opacity .6", o["size"].startswith("90px 90px") and o["op"] == "0.6"
                  and all(abs(float(a) - 0.045) < 0.003 for a in re.findall(r"rgba\(255, 255, 255, ([\d.]+)\)", o["grid"])) and "rgba(255, 255, 255" in o["grid"],
                  [o["size"], o["op"], o["grid"][:60]]),
            check("STYLE.md carries the five slots", slots == {"bg": "#0B0F19", "fg": "#F5F7FA", "accent": "#FFB020", "muted": "#8A93A6", "line": "#2A3346"}, slots),
            check("withAlpha appends the alpha byte, else color-mix", wa == ["#19c37d4d", "#ff7a1aff", "color-mix(in srgb, rgb(1,2,3) 50%, transparent)"], wa),
            check("negative control: the Remotion paper colour is not the canvas starter's ground", "#f4f1ea" not in json.dumps(o))], [out]


@card("COLOR-47")
def colormap_by_meaning(task, wd):
    """Pick the colormap by what the data means (sequential = monotonic lightness, diverging around a centred norm,
    cyclic for angles), then a chart with one accent on <=2 marks, context grey at 40%, <=4 hues; all measured."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import TwoSlopeNorm
    np = _np()

    def choose(kind):
        return {"ordered": "viridis", "signed": "RdBu_r", "angle": "twilight", "category": "tab10"}[kind]

    def L_of(name, n=32):
        cm = matplotlib.colormaps[name]
        return [srgb_to_oklab([v * 255 for v in cm(i / (n - 1))[:3]])[0] for i in range(n)]
    mono = lambda Ls: all(b > a for a, b in zip(Ls, Ls[1:])) or all(b < a for a, b in zip(Ls, Ls[1:]))
    seq = L_of(choose("ordered"))
    norm = TwoSlopeNorm(vmin=-2, vcenter=0, vmax=5)
    cyc = matplotlib.colormaps[choose("angle")]
    cyc_gap = max(abs(a - b) for a, b in zip(cyc(0.0), cyc(1.0)))
    ledger = {"accent": "#e8333f", "context": "#8a93a6", "chrome": "#3a4252", "bg": "#ffffff"}
    vals = [12, 18, 31, 15, 9]
    fig, ax = plt.subplots(figsize=(4, 3), dpi=80)
    for i, v in enumerate(vals):
        hi = v == max(vals)
        ax.bar(i, v, color=ledger["accent"] if hi else ledger["context"], alpha=1.0 if hi else 0.4)
    for s in ax.spines.values():
        s.set_color(ledger["chrome"])
    fig.savefig(wd / "chart.png", facecolor="white")
    plt.close(fig)
    img = load_png(wd / "chart.png")
    sat = img.max(axis=-1) - img.min(axis=-1)
    hues = set()
    for px in img[sat > 40][::7]:
        hues.add(int(oklch(px)[2] // 30))
    accent_mask = (np.abs(img - rgb(ledger["accent"])).max(axis=-1) < 10)
    cols = np.where(accent_mask.any(axis=0))[0]
    marks = 1 + int(np.sum(np.diff(cols) > 1)) if len(cols) else 0
    ctx = img[(np.abs(img - (np.array(rgb(ledger["context"])) * 0.4 + 255 * 0.6)).max(axis=-1) < 6)]
    out = write_json(wd, "colour-roles.json", {"choice": {k: choose(k) for k in ("ordered", "signed", "angle", "category")}, "ledger": ledger,
                                               "viridis_L": seq, "accent_marks": marks})
    return [check("ordered data -> viridis with monotonic OKLab lightness", mono(seq), [round(seq[0], 3), round(seq[-1], 3)]),
            check("diverging norm centred: -2 -> 0, 0 -> .5, 5 -> 1", [float(norm(-2)), float(norm(0)), float(norm(5))] == [0.0, 0.5, 1.0]),
            check("cyclic map closes on itself (angles/hours)", cyc_gap < 0.05, cyc_gap),
            check("accent on exactly one mark, context bars at 40%", marks == 1 and len(ctx) > 500, [marks, len(ctx)]),
            check("chart uses <= 4 hue families", len(hues) <= 4, sorted(hues)),
            check("negative control: a rainbow (jet) is not monotonic in lightness", not mono(L_of("jet")))], [out, wd / "chart.png"]


@card("COLOR-51")
def oklch_ramps(task, wd):
    """Build ramps in OKLCH (Ottosson): a neutral ramp with even L steps (uniformity >= 0.7, hue drift <= 10 deg) and a
    material ramp that rotates hue 10-20 deg per step, cooler in the shadows, warmer in the lights, more chroma in darks."""
    from PIL import Image, ImageDraw
    neutral = [oklch_to_srgb(L, 0.02, 255) for L in [0.22 + i * 0.12 for i in range(7)]]
    Ln = [oklch(c)[0] for c in neutral]
    drift = max(oklch(c)[2] for c in neutral) - min(oklch(c)[2] for c in neutral)
    mat = [oklch_to_srgb(L, C, H) for L, C, H in [(0.32, 0.12, 265), (0.45, 0.11, 250), (0.58, 0.10, 235), (0.71, 0.09, 220), (0.84, 0.08, 205)]]
    mh = [oklch(c)[2] for c in mat]
    mc = [oklch(c)[1] for c in mat]
    steps = [abs(mh[i] - mh[i + 1]) for i in range(4)]
    linear = []
    for i in range(7):                                    # the untreated ramp: equal steps in linear light
        v = 0.02 + i * (0.9 - 0.02) / 6
        e = 255 * (1.055 * v ** (1 / 2.4) - 0.055)
        linear.append((e, e, e))
    Ll = [oklch(c)[0] for c in linear]
    im = Image.new("RGB", (70 * 7, 140))
    d = ImageDraw.Draw(im)
    for i, c in enumerate(neutral):
        d.rectangle((i * 70, 0, i * 70 + 69, 69), fill=c)
    for i, c in enumerate(mat):
        d.rectangle((i * 98, 70, i * 98 + 97, 139), fill=c)
    im.save(wd / "ramps.png")
    out = write_json(wd, "ramps.json", {"neutral": [hexc(c) for c in neutral], "material": [hexc(c) for c in mat], "neutral_L": Ln})
    return [check("neutral ramp uniformity >= 0.7", uniformity(Ln) >= 0.7, uniformity(Ln), ">=0.7"),
            check("neutral hue drift <= 10 deg", drift <= 10, drift, "<=10"),
            check("material ramp rotates 10-20 deg per step", all(10 <= s <= 20 for s in steps), steps),
            check("shadows cooler (bluer) than highlights, darks more saturated", mh[0] > mh[-1] and mc[0] > mc[-1], [mh[0], mh[-1], mc[0], mc[-1]]),
            check("negative control: a linear-light grey ramp fails the uniformity test", uniformity(Ll) < 0.7, uniformity(Ll), "<0.7")], [out, wd / "ramps.png"]


def pick_ink(ground, inks=("#ffffff", "#0b0b10")):
    return max(inks, key=lambda i: contrast(i, ground))


@card("COLOR-67")
def chapter_grounds(task, wd):
    """Each beat owns one flat saturated ground from a 4-colour brand set; the cut is the colour change (hard, 0 ms, on
    the bar), at most one flip per bar, and the text ink inverts so it stays >= 4.5:1."""
    from PIL import Image, ImageDraw
    np = _np()
    grounds = ["#2f5bff", "#ffd23f", "#e8333f", "#1fb36b"]
    bpm, fps, bars = 120, 30, 4
    bar_f = int(fps * 4 * 60 / bpm)
    fnt = font(DEJAVU_B, 28)
    frames, inks = [], []
    for i in range(bar_f * bars):
        g = grounds[(i // bar_f) % 4]
        ink = pick_ink(g)
        im = Image.new("RGB", (160, 90), g)
        ImageDraw.Draw(im).text((80, 45), "KOSIF", font=fnt, fill=ink, anchor="mm")
        frames.append(np.asarray(im).astype(float))
        inks.append(ink)
    film = write_video(wd / "grounds.mp4", frames, fps)
    fr = read_video(film)
    corner = [hexc(f[2, 2]) for f in fr]
    changes = [i for i in range(1, len(corner)) if corner[i] != corner[i - 1]]
    in_between = [c for c in corner if c not in grounds]
    worst = min(contrast(inks[i], grounds[(i // bar_f) % 4]) for i in range(len(inks)))
    fixed_white = min(contrast("#ffffff", g) for g in grounds)
    out = write_json(wd, "grounds.json", {"cuts_at_frames": changes, "bar_frames": bar_f, "inks": sorted(set(inks))})
    return [check("ground changes exactly on each bar (frames 60, 120, 180)", changes == [bar_f, 2 * bar_f, 3 * bar_f], changes),
            check("hard cuts: no tweened in-between colours", not in_between, len(in_between), 0),
            check("<= 1 flip per bar", len(changes) <= bars - 1),
            check("text ink inverts and stays >= 4.5:1 on every ground", worst >= 4.5 and len(set(inks)) == 2, worst, ">=4.5"),
            check("negative control: constant white ink fails on the yellow ground", fixed_white < 4.5, fixed_white, "<4.5")], [out, film]


@card("COLOR-69")
def sky_stop_drift(task, wd):
    """GSAP tweens the SVG sky's stop-color attributes: night -> dawn over 11 s (sine.inOut), dawn -> morning over a
    13.7 s second leg; the veil fades .38 -> .22 linearly and the stars fade out from 2 s over 9 s."""
    night, dawn, morn = ["#0b1033", "#3b1f5e", "#b9507a"], ["#2b3d86", "#c4677a", "#ffb066"], ["#34509a", "#f2a079", "#ffd890"]
    body = ("<svg width=200 height=200><defs><linearGradient id=g x1=0 y1=0 x2=0 y2=1>" +
            "".join("<stop id=s%d offset='%s' stop-color='%s'/>" % (i, o, c) for i, (o, c) in enumerate(zip((0, 0.6, 1), night))) +
            "</linearGradient></defs><rect width=200 height=200 fill='url(#g)'/><rect id=veil width=200 height=200 fill='#1d0f2c' opacity='.38'/>"
            "<g id=stars opacity='1'><circle cx=20 cy=20 r=1 fill='#fff'/></g></svg>")
    js = """const tl=gsap.timeline({paused:true});%s
tl.fromTo('#veil',{attr:{opacity:.38}},{attr:{opacity:.22},duration:24.7,ease:'none'},0);tl.to('#stars',{attr:{opacity:0},duration:9,ease:'none'},2);
const at=t=>{tl.seek(t,false);return {s:[0,1,2].map(i=>document.getElementById('s'+i).getAttribute('stop-color')),veil:+document.getElementById('veil').getAttribute('opacity'),stars:+document.getElementById('stars').getAttribute('opacity')}};
return {dur:tl.duration(),t0:at(0),t55:at(5.5),t11:at(11),t247:at(24.7),t2:at(2),t65:at(6.5)};""" % "".join(
        "tl.to('#s%d',{attr:{'stop-color':'%s'},duration:11,ease:'sine.inOut'},0);tl.to('#s%d',{attr:{'stop-color':'%s'},duration:13.7,ease:'sine.inOut'},11);"
        % (i, dawn[i], i, morn[i]) for i in range(3))
    o, page, _ = chrome_page(wd, "sky", html_doc(body, js, [GSAP]), (240, 240))

    def as_hex(c):
        c = c.strip()
        if c.startswith("#"):
            return c.lower()
        return hexc([float(v) for v in re.findall(r"[\d.]+", c)[:3]])
    s0, s55, s11, s247 = ([as_hex(c) for c in o[k]["s"]] for k in ("t0", "t55", "t11", "t247"))
    mid_expect = [hexc([(a + b) / 2 for a, b in zip(rgb(n), rgb(d))]) for n, d in zip(night, dawn)]
    mid_err = max(abs(a - b) for x, y in zip(s55, mid_expect) for a, b in zip(rgb(x), rgb(y)))
    out = write_json(wd, "sky.json", o)
    return [check("timeline is 11 + 13.7 = 24.7 s", abs(o["dur"] - 24.7) < 1e-6, o["dur"], 24.7),
            check("night at 0 s, dawn at 11 s, morning at 24.7 s", s0 == night and s11 == dawn and s247 == morn, [s0, s11, s247]),
            check("sine.inOut leg is half-way at 5.5 s", mid_err <= 3, s55, mid_expect),
            check("veil .38 -> .22 linear (0.30 at 12.35 s implies .38 at 0, .22 at end)", abs(o["t0"]["veil"] - 0.38) < 1e-6 and abs(o["t247"]["veil"] - 0.22) < 1e-6),
            check("stars start fading at 2 s and are half gone at 6.5 s", o["t2"]["stars"] == 1 and abs(o["t65"]["stars"] - 0.5) < 0.01, [o["t2"]["stars"], o["t65"]["stars"]]),
            check("negative control: the untweened sky (t=0) is not the morning palette", s0 != morn)], [out, page]


@card("COLOR-71")
def act_accent_flip(task, wd):
    """One accent per act: the card's glow and second headline flip red #e8333f -> cyan #1fb3e6 over ~300 ms at the turn;
    orange stays <= 15% of the frame."""
    np = _np()
    fps, W, H = 30, 160, 90
    red, cyan, ground = np.array(rgb("#e8333f")), np.array(rgb("#1fb3e6")), np.array(rgb("#0a1822"))
    turn = 0.5
    frames = []
    for i in range(30):
        t = i / fps
        k = min(1.0, max(0.0, (t - turn) / 0.3))
        c = red * (1 - k) + cyan * k
        f = np.zeros((H, W, 3)) + ground
        f[30:60, 40:120] = c                   # card glow
        f[64:70, 50:110] = c                   # second headline line
        f[80:90, 0:20] = rgb("#ff6a1a")        # a small orange tag
        frames.append(f)
    film = write_video(wd / "flip.mp4", frames, fps)
    fr = read_video(film)
    near = lambda f, c: float((np.abs(f[45, 80] - c).max()) < 6)
    start = next(i for i in range(len(fr)) if np.abs(fr[i][45, 80] - red).max() > 6)
    end = next(i for i in range(len(fr)) if np.abs(fr[i][45, 80] - cyan).max() < 6)
    orange = float((np.abs(fr[0] - rgb("#ff6a1a")).max(axis=-1) < 30).mean())
    heavy = np.zeros((H, W, 3)) + rgb("#ff6a1a")
    heavy[:, :100] = ground
    heavy_share = float((np.abs(heavy - rgb("#ff6a1a")).max(axis=-1) < 30).mean())
    out = write_json(wd, "flip.json", {"flip_start_frame": start, "flip_end_frame": end, "orange_share": orange})
    return [check("problem act shows red, offer act shows cyan", near(fr[10], red) and near(fr[-1], cyan)),
            check("flip lasts ~300 ms (9 frames at 30 fps)", end - start in (8, 9, 10), end - start, 9),
            check("headline line flips with the glow", np.abs(fr[-1][66, 80] - cyan).max() < 6),
            check("orange <= 15% of the frame", orange <= 0.15, orange, "<=0.15"),
            check("negative control: an orange-flooded frame breaks the 15% cap", heavy_share > 0.15, heavy_share)], [out, film]


@card("COLOR-73")
def event_tint(task, wd):
    """Multiply the whole frame with the event colour at 40% while the spell lasts, 3 frames stronger (70%) on impact,
    then release; a UI error state tints amber and is capped at 15%."""
    np = _np()
    ys, xs = np.mgrid[0:90, 0:160]
    base = np.stack([80 + xs, 120 + ys, 200 - xs // 2], axis=-1).astype(float).clip(0, 255)
    blue = np.array(rgb("#3a6bff")) / 255.0
    sched = []
    for i in range(24):
        a = 0.0
        if 4 <= i < 16:
            a = 0.7 if 8 <= i < 11 else 0.4
        sched.append(a)
    frames = [base * (1 - a) + base * blue * a for a in sched]
    film = write_video(wd / "tint.mp4", frames, 24)
    fr = read_video(film)

    def strength(f, col):
        ch = int(np.argmin(col))
        num = (base - f)[..., ch]
        den = (base * (1 - col))[..., ch]
        return float(np.median(num / np.maximum(den, 1e-6)))
    meas = [round(strength(f, blue), 2) for f in fr]
    amber = np.array(rgb("#ffb020")) / 255.0
    err = min(0.15, 0.3)
    err_frame = base * (1 - err) + base * amber * err
    out = write_json(wd, "tint.json", {"schedule": sched, "measured": meas})
    impact = [i for i, a in enumerate(meas) if a >= 0.65]
    return [check("cast frames tinted at 40%", all(abs(meas[i] - 0.4) < 0.03 for i in (4, 6, 12, 15)), [meas[i] for i in (4, 12)], 0.4),
            check("impact: exactly 3 stronger frames (70%)", impact == [8, 9, 10], impact, [8, 9, 10]),
            check("released after the spell", all(abs(m) < 0.02 for m in meas[16:]), meas[16:18], 0),
            check("error tint capped at 15%", abs(strength(err_frame, amber) - 0.15) < 0.01 and err <= 0.15, strength(err_frame, amber)),
            check("negative control: the untinted frames measure no tint", all(abs(m) < 0.02 for m in meas[:4]), meas[:4], 0)], [out, film]


def hsl_hex(h, s, l):
    import colorsys
    r, g, b = colorsys.hls_to_rgb((h % 360) / 360.0, l, s)
    return hexc((r * 255, g * 255, b * 255))


@card("COLOR-74")
def index_hue_rings(task, wd):
    """Ring hue from its index (330 deg inside -> 185 deg outside, HSL S 80% L 65%), the counter takes the innermost
    hue; a background hue-rotating 360 deg / 10 s keeps white text >= 4.5:1 by checking the worst hue."""
    from PIL import Image, ImageDraw
    n = 6
    hues = [330 + (185 - 330) * i / (n - 1) for i in range(n)]
    cols = [hsl_hex(h, 0.8, 0.65) for h in hues]
    im = Image.new("RGB", (240, 240), "#0b0b10")
    d = ImageDraw.Draw(im)
    for i in reversed(range(n)):
        r = 30 + i * 15
        d.ellipse((120 - r, 120 - r, 120 + r, 120 + r), outline=cols[i], width=10)
    d.text((120, 120), "42", font=font(DEJAVU_B, 26), fill=cols[0], anchor="mm")
    im.save(wd / "rings.png")
    px = load_png(wd / "rings.png")
    ring_hues = []
    for i in range(n):
        r = 30 + i * 15 - 5
        ring_hues.append(round(oklch(px[120 - r, 120])[2], 1))
    measured_hsl = []
    import colorsys
    for i in range(n):
        r = 30 + i * 15 - 5
        rr, gg, bb = px[120 - r, 120] / 255.0
        measured_hsl.append(round(colorsys.rgb_to_hls(rr, gg, bb)[0] * 360))

    def worst(L):
        return min(contrast("#ffffff", hsl_hex(h, 0.8, L)) for h in range(0, 360, 2))
    L = max(l / 100 for l in range(5, 60) if worst(l / 100) >= 4.5)
    rot = [(360 * t / 10.0) % 360 for t in (0, 2.5, 5, 10)]
    out = write_json(wd, "rings.json", {"hues": hues, "colours": cols, "bg_lightness_for_text": L, "rotation_deg": rot})
    return [check("ring hues step 330 -> 185 across the index", [round(h) for h in hues] == [330, 301, 272, 243, 214, 185], [round(h) for h in hues]),
            check("rendered rings carry those hues (HSL read-back within 3 deg)", all(abs(a - round(b) % 360) <= 3 for a, b in zip(measured_hsl, hues)), measured_hsl),
            check("counter uses the innermost hue", cols[0] == hsl_hex(330, 0.8, 0.65), cols[0]),
            check("background rotates 360 deg per 10 s", rot == [0, 90, 180, 0], rot),
            check("rotating ground lightness chosen so the worst hue still gives >= 4.5:1", worst(L) >= 4.5, [L, worst(L)]),
            check("negative control: at L 50% the worst hue fails white text", worst(0.5) < 4.5, worst(0.5), "<4.5")], [out, wd / "rings.png"]


@card("COLOR-77")
def sixteen_colour_cap(task, wd):
    """Cap the film at 16 indexed colours (Pillow quantize with a fixed palette); two accent indices swap on odd/even
    frames for 3 frames at each spell; the final flash uses 4 colours."""
    from PIL import Image
    np = _np()
    pal = [(0, 0, 0), (255, 255, 255), (232, 51, 63), (31, 179, 230)] + [(16 * i, 40 + 12 * i, 120 - 6 * i) for i in range(12)]
    pimg = Image.new("P", (1, 1))
    pimg.putpalette([v for c in pal for v in c] + [0] * (768 - 48))
    ys, xs = np.mgrid[0:72, 0:128]
    frames, counts, spells = [], [], {6, 14}
    for i in range(24):
        src = np.stack([(xs * 2 + i * 3) % 256, (ys * 3) % 256, (xs + ys) % 256], axis=-1).astype("uint8")
        q = Image.fromarray(src).quantize(palette=pimg, dither=Image.Dither.NONE)
        a = np.asarray(q).copy()
        a[30:42, 50:78] = 2
        if any(s <= i < s + 3 for s in spells) and i % 2:
            a[a == 2], a[a == 3] = 99, 2
            a[a == 99] = 3
        if i >= 21:
            a = (a % 4)
        q2 = Image.fromarray(a.astype("uint8"), "P")
        q2.putpalette(pimg.getpalette())
        rgbf = np.asarray(q2.convert("RGB")).astype(float)
        frames.append(rgbf)
        counts.append(len({tuple(c) for c in rgbf.reshape(-1, 3)}))
    film = write_video(wd / "indexed.mp4", frames, 12)
    fr = read_video(film)
    allowed = {tuple(c) for c in pal}
    off_palette = sum(1 for f in fr for c in {tuple(x) for x in f.reshape(-1, 3).astype(int)} if c not in allowed)
    centre = [tuple(fr[i][36, 64].astype(int)) for i in range(24)]
    swapped = [i for i in range(24) if centre[i] == pal[3]]
    src0 = np.stack([(xs * 2) % 256, (ys * 3) % 256, (xs + ys) % 256], axis=-1)
    raw_colours = len({tuple(c) for c in src0.reshape(-1, 3)})
    out = write_json(wd, "indexed.json", {"colours_per_frame": counts, "accent_swapped_frames": swapped})
    return [check("every frame uses <= 16 colours", max(counts) <= 16, max(counts), "<=16"),
            check("every pixel is a palette entry (lossless read-back)", off_palette == 0, off_palette, 0),
            check("accent swaps on odd frames within each 3-frame spell window", swapped == [7, 15], swapped, [7, 15]),
            check("final flash frames use exactly 4 colours", all(c <= 4 for c in counts[21:]) and counts[21] == 4, counts[21:]),
            check("negative control: the source frame has far more than 16 colours", raw_colours > 16, raw_colours)], [out, film]


@card("COLOR-78")
def dark_radial_ground(task, wd):
    """Dark ground with a slightly lighter centre: radial #182446 -> #0b1020 at 55% + a 90 px grid at .045; consecutive
    scenes alternate the start stop (#0c1728 even / #132337 odd) so they breathe."""
    np = _np()
    W, H = 540, 360
    ys, xs = np.mgrid[0:H, 0:W].astype(float)
    r = np.hypot((xs - W / 2) / (W / 2), (ys - H * 0.42) / (H / 2)) / math.sqrt(2)
    out_frames = []
    for scene in range(2):
        inner = np.array(rgb("#182446" if scene == 0 else "#132337"))
        k = np.clip(r / 0.55, 0, 1)[..., None]
        f = inner * (1 - k) + np.array(rgb("#0b1020")) * k
        grid = ((xs.astype(int) % 90 == 0) | (ys.astype(int) % 90 == 0))[..., None]
        f = np.where(grid, f * (1 - 0.045) + 255 * 0.045, f)
        save_png(f, wd / ("ground_%d.png" % scene))
        out_frames.append(load_png(wd / ("ground_%d.png" % scene)))
    a = out_frames[0]
    centre, edge = a[int(H * 0.42), W // 2 + 1], a[3, 3]
    near_hex = lambda px, h: float(np.abs(px - rgb(h)).max()) <= 2
    lift = float(a[45, 90][0] - a[45, 91][0])
    flat = np.zeros((H, W, 3)) + rgb("#0b1020")
    out = write_json(wd, "ground.json", {"centre": hexc(centre), "edge": hexc(edge), "grid_lift": lift})
    return [check("centre is the lighter #182446, edge settles on #0b1020", near_hex(centre, "#182446") and near_hex(edge, "#0b1020"), [hexc(centre), hexc(edge)]),
            check("grid lines every 90 px lift by .045 of white", 9 <= lift <= 13, lift, "~11"),
            check("consecutive scenes start from alternating centre stops", near_hex(out_frames[1][int(H * 0.42), W // 2 + 1], "#132337"), hexc(out_frames[1][int(H * 0.42), W // 2 + 1])),
            check("negative control: a flat ground has no lighter centre", hexc(flat[100, 100]) == hexc(flat[0, 0]))], [out, wd / "ground_0.png"]


@card("COLOR-82")
def one_grade_over_stack(task, wd):
    """Grade the final composite (not each layer), 3% grain, a 12% vignette and a 24 px contact shadow at .35 under the
    cut-out, so the layers read as one photograph."""
    import cv2
    np = _np()
    H, W = 240, 320
    bg = np.zeros((H, W, 3)) + (150, 160, 170)
    cut = np.zeros((H, W), bool)
    cut[60:170, 120:200] = True
    shadow = np.zeros((H, W), "float32")
    shadow[168:176, 120:200] = 1.0
    shadow = cv2.GaussianBlur(shadow, (0, 0), 24 / 3)
    shadow = shadow / shadow.max() * 0.35
    comp = bg * (1 - shadow[..., None])
    comp[cut] = (200, 120, 90)
    graded = np.clip((comp - 128) * 1.08 + 128 + np.array([6, 0, -6]), 0, 255)
    ys, xs = np.mgrid[0:H, 0:W].astype(float)
    rr = np.hypot((xs - W / 2) / (W / 2), (ys - H / 2) / (H / 2)) / math.sqrt(2)
    vig = 1 - 0.12 * rr ** 2
    rng = np.random.default_rng(7)
    final = np.clip(graded * vig[..., None] + rng.normal(0, 0.03 * 255, (H, W, 1)), 0, 255)
    save_png(final, wd / "composite.png")
    f = load_png(wd / "composite.png")
    flat_bg = np.clip((np.array([150, 160, 170.0]) - 128) * 1.08 + 128 + np.array([6, 0, -6]), 0, 255)
    corner_ratio = float(f[:6, :6].mean() / (flat_bg.mean() * 1.0))
    centre_patch = f[100:110, 20:30] - (flat_bg * vig[100:110, 20:30, None])
    grain = float(centre_patch.std() / 255)
    under = float(1 - f[172:176, 150:170].mean() / (flat_bg * vig[172:176, 150:170, None]).mean())
    raw = comp
    raw_corner = float(raw[:6, :6].mean() / raw[100:110, 20:30].mean())
    out = write_json(wd, "grade.json", {"corner_ratio": corner_ratio, "grain": grain, "shadow_darkening": under})
    return [check("vignette darkens corners by ~12%", 0.86 <= corner_ratio <= 0.9, corner_ratio, 0.88),
            check("grain within 2-4%", 0.02 <= grain <= 0.04, grain, 0.03),
            check("contact shadow under the cut-out at ~.35", 0.28 <= under <= 0.4, under, 0.35),
            check("grade applied once to the whole stack (warm offset on background and cut-out alike)",
                  abs((f[30:60, 20:60, 0] - f[30:60, 20:60, 2]).mean() - (flat_bg[0] - flat_bg[2])) < 3),
            check("negative control: the ungraded stack has no vignette", abs(raw_corner - 1) < 1e-6, raw_corner, 1)], [out, wd / "composite.png"]


@card("COLOR-83")
def stylisation_steps(task, wd):
    """A photo steps down on beats: full colour -> duotone (300 ms) -> halftone (300 ms) -> flat vector (400 ms); luma
    threshold .5, halftone dot pitch 10 px at 1080 width (4 px at this 432 px canvas)."""
    np = _np()
    W, H, fps = 432, 240, 30
    ys, xs = np.mgrid[0:H, 0:W].astype(float)
    photo = np.stack([128 + 100 * np.sin(xs / 40), 128 + 90 * np.cos(ys / 30), 128 + 80 * np.sin((xs + ys) / 55)], -1)
    luma = (0.2126 * photo[..., 0] + 0.7152 * photo[..., 1] + 0.0722 * photo[..., 2]) / 255
    dark, light = np.array(rgb("#1d1a4a")), np.array(rgb("#ffb020"))
    duo = dark * (1 - luma[..., None]) + light * luma[..., None]
    pitch = round(10 * W / 1080)
    cx, cy = (xs % pitch) - pitch / 2 + 0.5, (ys % pitch) - pitch / 2 + 0.5
    cell_l = luma[(ys // pitch * pitch).astype(int), (xs // pitch * pitch).astype(int)]
    dot = np.hypot(cx, cy) < (1 - cell_l) * pitch * 0.7
    half = np.where(dot[..., None], dark, light)
    flat = np.where((luma > 0.5)[..., None], light, dark)
    beats = [0, 9, 18, 30]                     # frames: duotone at 0, halftone at +300 ms, vector at +600 ms, end +1 s
    frames = []
    for i in range(30 + 6):
        img = photo if i < 3 else duo if i < 3 + 9 else half if i < 3 + 18 else flat
        frames.append(img)
    film = write_video(wd / "steps.mp4", frames, fps)
    fr = read_video(film)

    def on_segment(f):
        v = (f - dark) / (light - dark)
        return float(np.abs(v - v.mean(axis=-1, keepdims=True)).max())
    duo_err, photo_err = on_segment(fr[5]), on_segment(fr[0])
    spec = np.abs(np.fft.rfft((fr[15][..., 0] < 100).astype(float).mean(axis=0) - 0.5))
    period = W / (np.argmax(spec[5:]) + 5)
    two = len({tuple(c) for c in fr[30].reshape(-1, 3).astype(int)})
    starts = [i for i in range(1, len(fr)) if np.abs(fr[i] - fr[i - 1]).mean() > 5]
    out = write_json(wd, "steps.json", {"stage_starts": starts, "dot_period_px": period, "duo_error": duo_err})
    return [check("duotone pixels lie on the two-ink line", duo_err < 0.03, duo_err, "<0.03"),
            check("halftone dot pitch = 4 px (10 px at 1080)", abs(period - pitch) < 0.3, period, pitch),
            check("flat vector = 2 colours by luma > .5", two == 2, two, 2),
            check("stages start 300 ms and 300 ms apart (frames 3, 12, 21)", starts == [3, 12, 21], starts),
            check("negative control: the untreated photo is not on the two-ink line", photo_err > 0.2, photo_err, ">0.2")], [out, film]


# ═════════════════════════════════════════════ diagrams-explainers-code ═════════════════════════════════════════════
@card("EXPL-09")
def flat_alpha_icons(task, wd):
    """Flat icons on a shared palette at 1024 px; the model's opaque white ground is removed by a near-white threshold in
    Pillow so the icon gets a real alpha channel."""
    from PIL import Image, ImageDraw
    np = _np()
    pal = {"ink": (11, 16, 32), "accent": (231, 182, 90), "fill": (47, 91, 255)}
    im = Image.new("RGB", (1024, 1024), (252, 252, 250))         # the opaque "model output"
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((212, 312, 812, 762), 60, fill=pal["fill"])
    d.ellipse((412, 412, 612, 612), fill=pal["accent"], outline=pal["ink"], width=24)
    im.save(wd / "icon_opaque.png")

    def remove_white(img, thr=240):
        a = np.asarray(img.convert("RGB")).astype(int)
        alpha = np.where(a.min(axis=-1) >= thr, 0, 255).astype("uint8")
        return Image.fromarray(np.dstack([a.astype("uint8"), alpha]), "RGBA")
    rgba = remove_white(im)
    rgba.save(wd / "icon.png")
    A = np.asarray(Image.open(wd / "icon.png"))
    transparent = float((A[..., 3] == 0).mean())
    body = A[A[..., 3] == 255][..., :3]
    in_pal = float(np.mean([min(np.abs(px - np.array(c)).max() for c in pal.values()) <= 2 for px in body[::97]]))
    opaque_alpha = np.asarray(im.convert("RGBA"))[..., 3]
    exp_t = 1 - (600 * 450 - (4 - math.pi) * 60 ** 2) / 1024 ** 2
    return [check("1024 px square RGBA", A.shape == (1024, 1024, 4), A.shape),
            check("background removed: transparent share matches the ground area", abs(transparent - exp_t) < 0.01, transparent, exp_t),
            check("corners transparent, icon centre opaque", A[0, 0, 3] == 0 and A[512, 512, 3] == 255),
            check("opaque pixels use only the shared palette", in_pal == 1.0, in_pal, 1.0),
            check("negative control: the model's opaque output has no transparency", int(opaque_alpha.min()) == 255)], [wd / "icon.png"]


@card("EXPL-11")
def mermaid_render_animate(task, wd):
    """mmdc renders flowchart text to SVG (rendering validates the syntax); <=12 nodes, every arrow labelled, RL for
    Arabic; then the SVG nodes are revealed in reading order with a GSAP stagger, seeked in Chrome."""
    cfg = write_json(wd, "puppeteer.json", {"args": ["--no-sandbox"], "executablePath": CHROME})
    good = wd / "flow.mmd"
    good.write_text("flowchart RL\n  A[فكرة] -->|نكتب| B[سيناريو]\n  B -->|نرسم| C[لوحة]\n  C -->|نحرك| D[فيلم]\n", encoding="utf-8")
    bad = wd / "broken.mmd"
    bad.write_text("flowchart TD\n  A[Start] -->|go B[Work\n", encoding="utf-8")
    env = dict(os.environ, PUPPETEER_EXECUTABLE_PATH=str(CHROME), HOME=str(wd))

    def mmdc(src, dst):
        return subprocess.run(["mmdc", "-i", str(src), "-o", str(dst), "-t", "dark", "-b", "transparent", "-p", str(cfg)], capture_output=True,
                              text=True, timeout=60, env=env, stdin=subprocess.DEVNULL)
    r_ok = mmdc(good, wd / "flow.svg")
    r_bad = mmdc(bad, wd / "broken.svg")
    svg = (wd / "flow.svg").read_text(encoding="utf-8")
    nodes = re.findall(r'<g class="node[^"]*" id="[^"]*flowchart-([A-Z])-\d+"[^>]*transform="translate\(([\d.]+), ([\d.]+)\)"', svg)
    labels = re.findall(r'class="edgeLabel"[^>]*>.*?<p>([^<]*)</p>', svg, re.S)
    xs = [float(x) for _, x, _ in nodes]
    js = """const ns=[...document.querySelectorAll('g.node')].sort((a,b)=>b.getBBox().x-a.getBBox().x);
const tl=gsap.timeline({paused:true});tl.from(ns,{opacity:0,duration:.3,stagger:.4});const at=t=>{tl.seek(t,false);return ns.map(n=>+getComputedStyle(n).opacity)};
return {ids:ns.map(n=>n.id.split('-')[3]),o0:at(0),o1:at(0.75),o2:at(1.35),end:at(tl.duration())};"""
    o, page, _ = chrome_page(wd, "animate", html_doc(svg, js, [GSAP]), (900, 300))
    out = write_json(wd, "mermaid.json", {"nodes": nodes, "labels": labels, "reveal": o})
    return [check("mmdc rendered the flowchart (exit 0)", r_ok.returncode == 0 and len(svg) > 2000, r_ok.returncode, 0),
            check("4 nodes (<= 12) and every arrow labelled", len(nodes) == 4 and len([l for l in labels if l.strip()]) == 3, [len(nodes), labels]),
            check("RL direction: A..D placed right to left", xs == sorted(xs, reverse=True), xs),
            check("nodes revealed in reading order (right to left)", o["ids"] == ["A", "B", "C", "D"] and o["o1"][:2] == [1, 1] and o["o1"][2] < 1 and o["end"] == [1, 1, 1, 1],
                  [o["ids"], o["o1"]]),
            check("negative control: broken syntax fails to render", r_bad.returncode != 0 and not (wd / "broken.svg").exists(), r_bad.returncode, "!= 0")], [wd / "flow.svg", out]


def truss_solve(nodes, members, supports, loads):
    """3D direct stiffness: nodes {id: (x,y,z)}, members [(a, b, A, E)], supports {id: (fx,fy,fz) fixed flags},
    loads {id: (Fx,Fy,Fz)} -> member axial forces (N, + tension)."""
    np = _np()
    ids = list(nodes)
    ix = {n: i for i, n in enumerate(ids)}
    K = np.zeros((3 * len(ids), 3 * len(ids)))
    geo = []
    for a, b, A, E in members:
        pa, pb = np.array(nodes[a], float), np.array(nodes[b], float)
        L = np.linalg.norm(pb - pa)
        c = (pb - pa) / L
        k = E * A / L * np.outer(c, c)
        ia, ib = 3 * ix[a], 3 * ix[b]
        for (r, s, sg) in ((ia, ia, 1), (ib, ib, 1), (ia, ib, -1), (ib, ia, -1)):
            K[r:r + 3, s:s + 3] += sg * k
        geo.append((ia, ib, c, L, E, A))
    F = np.zeros(3 * len(ids))
    for n, f in loads.items():
        F[3 * ix[n]:3 * ix[n] + 3] = f
    fixed = [3 * ix[n] + d for n, fl in supports.items() for d in range(3) if fl[d]]
    free = [i for i in range(3 * len(ids)) if i not in fixed]
    U = np.zeros(3 * len(ids))
    U[free] = np.linalg.solve(K[np.ix_(free, free)], F[free])
    return [E * A / L * float(np.dot(c, U[ib:ib + 3] - U[ia:ia + 3])) for ia, ib, c, L, E, A in geo]


def util_colour(u):
    stops = [(0, (0.35, 1, 0.72)), (0.5, (0.75, 1, 0.45)), (0.8, (1, 0.86, 0.35)), (1, (1, 0.36, 0.28))]
    u = max(0.0, min(1.0, u))
    for (u0, c0), (u1, c1) in zip(stops, stops[1:]):
        if u <= u1:
            k = (u - u0) / (u1 - u0)
            return tuple(a + (b - a) * k for a, b in zip(c0, c1))
    return stops[-1][1]


@card("EXPL-51")
def truss_solver_drives_film(task, wd):
    """A truss is solved (direct stiffness), members are coloured by utilisation (.35,1,.72 -> ... -> 1,.36,.28), the
    weakest member is flagged to break, and swapping in a thicker member raises the safety factor."""
    from PIL import Image, ImageDraw
    E, S = 8e6, 2e6                       # plush E 8 MPa, strength 2 MPa
    th = math.radians(40)
    nodes = {"L": (0, 0, 0), "R": (2 * math.cos(th), 0, 0), "T": (math.cos(th), math.sin(th), 0)}
    members = [("L", "T", 1.2e-4, E), ("R", "T", 1.2e-4, E), ("L", "R", 4.0e-5, E)]
    supports = {"L": (1, 1, 1), "R": (0, 1, 1), "T": (0, 0, 1)}        # pinned, roller, and out-of-plane restraint
    P = -1.9
    loads = {"T": (0, P, 0)}
    f = truss_solve(nodes, members, supports, loads)
    util = [abs(fi / m[2]) / S for fi, m in zip(f, members)]
    weak = max(range(len(members)), key=lambda i: util[i])
    sf = 1 / max(util)
    m2 = [list(m) for m in members]
    m2[weak][2] *= 2.0
    f2 = truss_solve(nodes, [tuple(m) for m in m2], supports, loads)
    util2 = [abs(fi / m[2]) / S for fi, m in zip(f2, m2)]
    sf2 = 1 / max(util2)
    # check against the analytic two-bar + tie answer
    f_incl, f_tie = P / (2 * math.sin(th)), -P / (2 * math.tan(th))
    im = Image.new("RGB", (320, 220), "#0d2627")
    d = ImageDraw.Draw(im)
    sx = lambda p: (40 + p[0] * 140, 190 - p[1] * 140)
    for i, (a, b, A, _) in enumerate(members[:3]):
        c = tuple(int(v * 255) for v in util_colour(min(1, util[i] / max(util))))
        d.line([sx(nodes[a]), sx(nodes[b])], fill=c, width=6 if i == weak else 3)
    im.save(wd / "truss.png")
    zero = truss_solve(nodes, members, supports, {"T": (0, 0, 0)})
    out = write_json(wd, "model.json", {"nodes": nodes, "members": members, "forces_N": f, "utilisation": util, "weak": weak,
                                        "safety": sf, "safety_after_swap": sf2})
    return [check("inclined members match the analytic force P/(2 sin th)", abs(f[0] - f_incl) < 1e-6 and abs(f[1] - f_incl) < 1e-6, f[:2], f_incl),
            check("tie member matches -P/(2 tan th) (tension)", abs(f[2] - f_tie) < 1e-6 and f[2] > 0, f[2], f_tie),
            check("the thin tie is the weakest member", weak == 2, weak, 2),
            check("utilisation colour ramp hits its stops", util_colour(0) == (0.35, 1, 0.72) and util_colour(1) == (1, 0.36, 0.28)
                  and all(abs(a - b) < 1e-9 for a, b in zip(util_colour(0.8), (1, 0.86, 0.35)))),
            check("swapping a 2x thicker weak member raises the safety factor", sf2 > sf * 1.2, [sf, sf2]),
            check("negative control: the unloaded truss carries no force", max(abs(x) for x in zero) < 1e-12, max(abs(x) for x in zero), 0)], [out, wd / "truss.png"]


@card("EXPL-58")
def diagram_and_code_films(task, wd):
    """Two film categories: an ordered 3-5 node diagram (nodes appear in order, links draw, a flow dot travels) and a dark
    LTR monospace code editor typing token by token with a result panel."""
    from PIL import Image, ImageDraw
    np = _np()
    fps, W, H = 15, 320, 180
    nodes = [(60, 90), (160, 90), (260, 90)]
    frames = []
    for i in range(45):
        t = i / fps
        im = Image.new("RGB", (W, H), "#0b1020")
        d = ImageDraw.Draw(im)
        for k, (x, y) in enumerate(nodes):
            if t >= 0.4 * k:
                d.ellipse((x - 18, y - 18, x + 18, y + 18), fill="#7ee8d2")
            if k and t >= 0.4 * k:
                d.line((nodes[k - 1][0] + 18, y, x - 18, y), fill="#9fb0cc", width=3)
        if t >= 1.2:
            u = ((t - 1.2) / 1.2) % 1
            px = 78 + u * (242 - 78)
            d.ellipse((px - 4, 86, px + 4, 94), fill="#ffb86b")
        frames.append(np.asarray(im).astype(float))
    dia = write_video(wd / "diagram.mp4", frames, fps)
    toks = ["const", " total", " =", " items", ".reduce", "(", "add", ",", " 0", ")", ";"]
    colours = {"const": "#ff7ab2", ".reduce": "#7ee8d2"}
    code_frames, typed = [], []
    for i in range(len(toks) + 4):
        im = Image.new("RGB", (W, H), "#0d1117")
        d = ImageDraw.Draw(im)
        d.text((8, 20), "1", font=font(MONO, 13), fill="#4b5563")
        x = 26
        for tk in toks[:min(i, len(toks))]:
            d.text((x, 20), tk, font=font(MONO, 13), fill=colours.get(tk, "#e6edf3"))
            x += font(MONO, 13).getlength(tk)
        if i >= len(toks) + 1:
            d.rectangle((8, 120, 312, 170), fill="#132337")
            d.text((16, 136), "> 42", font=font(MONO, 14), fill="#7ee8d2")
        typed.append(x)
        code_frames.append(np.asarray(im).astype(float))
    code = write_video(wd / "code.mp4", code_frames, 4)
    fr = read_video(dia)
    appear = [next(i for i in range(len(fr)) if np.abs(fr[i][y, x] - rgb("#7ee8d2")).max() < 8) for x, y in nodes]
    dot = [int(np.argmax((np.abs(fr[i][90] - rgb("#ffb86b")).max(axis=-1) < 30))) for i in (20, 24, 28)]
    cf = read_video(code)
    panel = [bool(np.abs(f[150, 300] - rgb("#132337")).max() < 6) for f in cf]
    out = write_json(wd, "films.json", {"node_appear_frames": appear, "dot_x": dot, "typed_x": typed})
    return [check("nodes appear in order 0.4 s apart", appear == [0, 6, 12], appear, [0, 6, 12]),
            check("flow dot travels left to right along the links", dot[0] < dot[1] < dot[2], dot),
            check("code typed token by token, LTR (caret x strictly grows)", all(b > a for a, b in zip(typed[:len(toks) + 1], typed[1:len(toks) + 1]))),
            check("result panel only after the last token", panel.index(True) == len(toks) + 1, panel.index(True), len(toks) + 1),
            check("negative control: the first diagram frame shows only one node", np.abs(fr[0][90, 260] - rgb("#7ee8d2")).max() > 8)], [dia, code, out]


# ═════════════════════════════════════════════ formats-platforms ═════════════════════════════════════════════
_CANVAS = {"reels": ("9:16", 1080, 1920), "tiktok": ("9:16", 1080, 1920), "shorts": ("9:16", 1080, 1920), "snapchat": ("9:16", 1080, 1920),
           "whatsapp-status": ("9:16", 1080, 1920), "youtube": ("16:9", 1920, 1080), "site": ("16:9", 1920, 1080), "desktop": ("16:9", 1920, 1080),
           "feed-reach": ("4:5", 1080, 1350), "square-feed": ("1:1", 1080, 1080), "link-preview": ("1.91:1", 1200, 630), "pinterest": ("2:3", 1000, 1500),
           "cinema": ("2.39:1", 2048, 858)}


def derive_canvas(where):
    if where not in _CANVAS:
        return None
    ar, w, h = _CANVAS[where]
    return {"plays_on": where, "aspect": ar, "width": w, "height": h, "why": "derived from where it plays (%s), not from 'which size?'" % where}


def width_for(height, ratio):
    a, b = (float(x) for x in ratio.split(":"))
    return int(round(height * a / b))


@card("FMT-01")
def canvas_from_destination(task, wd):
    """Ask where it plays, derive the canvas from that and record the derivation in the brief; widths come from
    round(h * ratio), so 16:9 must be driven with --height 1080 (1920 gives 3413 x 1920)."""
    brief = {"topic": "قهوة الصباح", "plays_on": ["reels", "youtube", "feed-reach"]}
    brief["canvas"] = [derive_canvas(p) for p in brief["plays_on"]]
    p = write_json(wd, "brief.json", brief)
    exp = {"reels": (1080, 1920), "youtube": (1920, 1080), "feed-reach": (1080, 1350), "square-feed": (1080, 1080),
           "link-preview": (1200, 630), "pinterest": (1000, 1500)}
    got = {k: (derive_canvas(k)["width"], derive_canvas(k)["height"]) for k in exp}
    fx.ffmpeg("-f", "lavfi", "-i", "color=c=#0b1020:s=%dx%d:d=0.2:r=10" % (1080 // 4, 1350 // 4), "-c:v", "libx264", "-pix_fmt", "yuv420p", str(wd / "feed_preview.mp4"))
    pr = [s for s in fx.probe(wd / "feed_preview.mp4")["streams"] if s["codec_type"] == "video"][0]
    return [check("platform table: 9:16 / 16:9 / 4:5 / 1:1 / 1.91:1 / 2:3", got == exp, got, exp),
            check("derivation recorded in the brief", all(c and "derived from where it plays" in c["why"] for c in brief["canvas"]) and p.stat().st_size > 0),
            check("16:9 from --height 1080 gives 1920 wide", width_for(1080, "16:9") == 1920, width_for(1080, "16:9"), 1920),
            check("the pitfall: --height 1920 on 16:9 gives 3413 x 1920", width_for(1920, "16:9") == 3413, width_for(1920, "16:9"), 3413),
            check("a 4:5 preview encodes at the derived ratio", (int(pr["width"]), int(pr["height"])) == (270, 337) or abs(int(pr["width"]) / int(pr["height"]) - 0.8) < 0.01,
                  (pr["width"], pr["height"])),
            check("negative control: 'which size?' without a destination derives nothing", derive_canvas("which size?") is None)], [p, wd / "feed_preview.mp4"]


def round_to(v, m):
    return int(math.floor(v / m + 0.5)) * m


def frames_8k1(seconds, fps):
    return int(round((seconds * fps - 1) / 8)) * 8 + 1


@card("FMT-07")
def diffusion_dims(task, wd):
    """Round W/H to /8 (SD), /16 (Wan, Krea 2), /32 (LTX); LTX frame counts are 8k+1; the generated clip is then
    reframed to the delivery canvas by scale + crop, never stretched."""
    np = _np()
    dims = {m: (round_to(1000, m), round_to(562, m)) for m in (8, 16, 32)}
    ltx = [frames_8k1(s, 24) for s in (5, 6.7, 10.7)]
    n = frames_8k1(0.4, 24)
    src = wd / "ltx_768x512.mp4"
    frames = []
    for i in range(n):
        f = np.zeros((512, 768, 3)) + 40
        f[156:356, 284:484] = 230                         # a 200 x 200 square
        frames.append(f)
    write_video(src, frames, 24)
    dst = wd / "delivery_1080x1920.mp4"
    fx.ffmpeg("-i", str(src), "-vf", "scale=-2:1920:flags=neighbor,crop=1080:1920", "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", str(dst))
    st = [s for s in fx.probe(dst)["streams"] if s["codec_type"] == "video"][0]
    g = read_video(dst)[0].mean(axis=-1) > 135
    ys, xs = np.where(g)
    aspect = (xs.max() - xs.min() + 1) / (ys.max() - ys.min() + 1)
    fx.ffmpeg("-i", str(src), "-vf", "scale=1080:1920", "-frames:v", "1", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(wd / "stretched.mp4"))
    gs = read_video(wd / "stretched.mp4")[0].mean(axis=-1) > 135
    ys2, xs2 = np.where(gs)
    stretched = (xs2.max() - xs2.min() + 1) / (ys2.max() - ys2.min() + 1)
    out = write_json(wd, "dims.json", {"dims": dims, "ltx_frames": ltx, "fixture_frames": n})
    return [check("1000x562 rounds to 1000x560 (/8), 1008x560 (/16), 992x576 (/32)", dims == {8: (1000, 560), 16: (1008, 560), 32: (992, 576)}, dims),
            check("LTX frame counts are 8k+1 (121 / 161 / 257 at 24 fps)", ltx == [121, 161, 257], ltx),
            check("every count satisfies (n - 1) % 8 == 0", all((x - 1) % 8 == 0 for x in ltx + [n])),
            check("delivered at 1080x1920", (st["width"], st["height"]) == (1080, 1920), (st["width"], st["height"])),
            check("reframe keeps the square square (no stretch)", abs(aspect - 1) < 0.03, aspect, 1.0),
            check("negative control: a plain resize stretches the square", abs(stretched - 1) > 0.3, stretched)], [dst, out]


_SAFE = {"top": 250, "bottom": 320, "right": 120, "left": 60}


def safe_zone(w=1080, h=1920, m=_SAFE):
    return (m["left"], m["top"], w - m["right"], h - m["bottom"])


def inside(box, zone):
    return box[0] >= zone[0] and box[1] >= zone[1] and box[2] <= zone[2] and box[3] <= zone[3]


@card("FMT-08")
def vertical_safe_zone(task, wd):
    """On 1080x1920 the platform chrome covers top 250 / bottom 320 / right 120 / left 60 px: draw the guides first,
    then check every critical element sits in the trusted ~900x1350 zone."""
    from PIL import Image, ImageDraw
    np = _np()
    z = safe_zone()
    im = Image.new("RGB", (1080, 1920), "#0b1020")
    d = ImageDraw.Draw(im)
    d.rectangle(z, outline="#ff3b6b", width=6)
    layout = {"title": (120, 320, 900, 520), "face": (300, 640, 780, 1180), "cta": (200, 1420, 880, 1560)}
    for k, b in layout.items():
        d.rectangle(b, fill="#7ee8d2" if k != "face" else "#ffb86b")
    im.save(wd / "safe_guides.png")
    a = np.asarray(im).astype(float)
    red = np.where((np.abs(a - rgb("#ff3b6b")).max(axis=-1) < 10))
    guide = (int(red[1].min()), int(red[0].min()), int(red[1].max()), int(red[0].max()))
    bad = (200, 1700, 880, 1840)
    out = write_json(wd, "safe.json", {"zone": z, "size": [z[2] - z[0], z[3] - z[1]], "layout_ok": {k: inside(b, z) for k, b in layout.items()}})
    return [check("trusted zone is 900 x 1350", (z[2] - z[0], z[3] - z[1]) == (900, 1350), (z[2] - z[0], z[3] - z[1]), (900, 1350)),
            check("zone is nudged upward (top margin < bottom margin)", z[1] < 1920 - z[3]),
            check("guides drawn at the zone edges", guide == (60, 250, 960, 1600), guide),
            check("title, face and CTA all inside the zone", all(inside(b, z) for b in layout.values())),
            check("negative control: a caption at y 1700-1840 sits under the platform chrome", not inside(bad, z))], [wd / "safe_guides.png", out]


def cap_height(img_gray, thr=128):
    np = _np()
    rows = np.where((img_gray < thr).any(axis=1))[0]
    return int(rows.max() - rows.min() + 1) if len(rows) else 0


@card("FMT-11")
def min_text_size(task, wd):
    """Smallest text 36 px at 1080 wide, checked on a 360 px preview, with contrast >= 4.5:1."""
    from PIL import Image, ImageDraw
    np = _np()

    def sample(px, fg, bg):
        im = Image.new("RGB", (1080, 200), bg)
        ImageDraw.Draw(im).text((40, 60), "HEXA", font=font(DEJAVU_B, px), fill=fg)
        prev = im.resize((360, 67), Image.LANCZOS).convert("L")
        return im, cap_height(np.asarray(prev).astype(float) if fg != "#ffffff" else 255 - np.asarray(prev).astype(float))

    def rule(px, fg, bg):
        _, ch = sample(px, fg, bg)
        return px >= 36 and contrast(fg, bg) >= 4.5 and ch >= 8, ch
    im, _ = sample(36, "#0b1020", "#f3f7ff")
    im.save(wd / "text36.png")
    ok36, ch36 = rule(36, "#0b1020", "#f3f7ff")
    ok_grey, _ = rule(40, "#9fb0cc", "#f3f7ff")
    ok24, ch24 = rule(24, "#0b1020", "#f3f7ff")
    out = write_json(wd, "readable.json", {"cap_px_on_360_preview": {"36": ch36, "24": ch24}, "contrast_dark": contrast("#0b1020", "#f3f7ff"),
                                           "contrast_grey": contrast("#9fb0cc", "#f3f7ff")})
    return [check("36 px dark-on-light passes: >= 8 px caps on the 360 preview, contrast >= 4.5", ok36, [ch36, contrast("#0b1020", "#f3f7ff")]),
            check("low-contrast grey text fails at any size", not ok_grey, contrast("#9fb0cc", "#f3f7ff"), "<4.5"),
            check("caps measured at 1/3 scale of the 36 px glyphs (~8.7 px)", 8 <= ch36 <= 10, ch36, "8-10"),
            check("negative control: 24 px text fails the floor", not ok24, [24, ch24], ">=36")], [wd / "text36.png", out]


@card("FMT-19")
def subject_aware_crops(task, wd):
    """Platform crops from one image: find the subject (colour-contrast saliency in Lab, OpenCV), crop 9:16, 1:1 and 4:5
    around it, fill with a blurred copy when the crop is larger than the image, and preview the three crops first."""
    import cv2
    from PIL import Image, ImageFilter
    np = _np()
    W, H = 960, 540
    img = np.zeros((H, W, 3), "uint8")
    img[:] = (90, 110, 100)
    rng = np.random.default_rng(1)
    img = np.clip(img + rng.normal(0, 4, img.shape), 0, 255).astype("uint8")
    cv2.circle(img, (760, 260), 70, (40, 60, 230), -1)              # the subject, far right
    cv2.imwrite(str(wd / "source.png"), img)
    lab = cv2.cvtColor(cv2.GaussianBlur(img, (0, 0), 3), cv2.COLOR_BGR2LAB).astype(float)
    smap = np.linalg.norm(lab - np.median(lab.reshape(-1, 3), axis=0), axis=-1)       # colour-contrast saliency
    smap = (smap / smap.max() * 255).astype("uint8")
    _, th = cv2.threshold(smap, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    ys, xs = np.where(th > 0)
    cx, cy = int(xs.mean()), int(ys.mean())
    crops = {}
    for name, (a, b) in {"9x16": (9, 16), "1x1": (1, 1), "4x5": (4, 5)}.items():
        ch = H
        cw = int(round(ch * a / b))
        x0 = min(max(0, cx - cw // 2), W - cw)
        crop = img[0:ch, x0:x0 + cw]
        crops[name] = (x0, cw)
        cv2.imwrite(str(wd / ("crop_%s.png" % name)), crop)
    tall = Image.fromarray(img[..., ::-1]).resize((W, int(W * 16 / 9)))
    tall = tall.filter(ImageFilter.GaussianBlur(24))
    tall.paste(Image.fromarray(img[..., ::-1]), (0, (tall.height - H) // 2))
    tall.save(wd / "fill_9x16.png")
    sheet = Image.new("RGB", (3 * 320, 400), "#111")
    for i, n in enumerate(crops):
        im = Image.open(wd / ("crop_%s.png" % n))
        im.thumbnail((310, 390))
        sheet.paste(im, (i * 320 + 5, 5))
    sheet.save(wd / "preview_3crops.png")
    has_subject = {n: x0 <= 760 - 70 and 760 + 70 <= x0 + cw for n, (x0, cw) in crops.items()}
    cw = int(round(H * 9 / 16))
    centre_x0 = (W - cw) // 2
    out = write_json(wd, "crops.json", {"subject_centre": [cx, cy], "crops": crops, "subject_inside": has_subject})
    return [check("saliency finds the subject centre", abs(cx - 760) < 25 and abs(cy - 260) < 25, [cx, cy], [760, 260]),
            check("all three crops contain the whole subject", all(has_subject.values()), has_subject),
            check("crop aspects 9:16 / 1:1 / 4:5", [crops["9x16"][1], crops["1x1"][1], crops["4x5"][1]] == [304, 540, 432], [v[1] for v in crops.values()]),
            check("3-crop preview sheet written", (wd / "preview_3crops.png").stat().st_size > 1000),
            check("blurred fill extends to a full 9:16 canvas", Image.open(wd / "fill_9x16.png").size == (960, int(960 * 16 / 9)), Image.open(wd / "fill_9x16.png").size),
            check("negative control: a centre crop cuts the subject out", not (centre_x0 <= 690 and 830 <= centre_x0 + cw), [centre_x0, centre_x0 + cw])], \
        [wd / "preview_3crops.png", out]


@card("FMT-33")
def social_pack_check(task, wd):
    """social.py pack builds the post-pack skeleton from a real file; filled, `social.py check` lints lengths, hashtag
    caps, hook and CTA per platform (exit 0 = ready). Nothing is posted."""
    script = VSK / "kosif-social/scripts/social.py"
    film = wd / "film.mp4"
    fx.ffmpeg("-f", "lavfi", "-i", "color=c=#0b1020:s=1080x1920:d=1:r=10", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", str(film))
    pk = wd / "X.post.json"
    run = lambda *a: subprocess.run([sys.executable, str(script), *map(str, a)], capture_output=True, text=True, timeout=60, cwd=str(wd), stdin=subprocess.DEVNULL)
    r = run("pack", film, "--platforms", "tiktok,reels,shorts", "--topic", "قهوة الصباح", "--out", pk)
    if r.returncode:
        raise RuntimeError("social.py pack failed: " + r.stderr[-300:])
    raw = run("check", pk)
    d = json.loads(pk.read_text(encoding="utf-8"))
    hook = "سر قهوة الصباح في دقيقة"
    for k in ("tiktok", "reels"):
        d["posts"][k].update(caption=hook + "\nجربها بكرة واحكيلنا. احفظ الفيديو وتابعنا", hashtags=["#قهوة", "#صباح", "#وصفات"], cta="احفظ الفيديو وتابعنا",
                             first_comment="الوصفة كاملة في التعليق", alt_text="كوب قهوة على طاولة خشب", cover_text="قهوة الصباح")
    d["posts"]["shorts"].update(title="سر قهوة الصباح في دقيقة", description=hook + " — اشترك للمزيد", hashtags=["#قهوة", "#صباح", "#shorts"],
                                pinned_comment="الوصفة كاملة هنا")
    filled = wd / "filled.post.json"
    filled.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    ok = run("check", filled)
    d["posts"]["shorts"]["title"] = "ق" * 120
    long_t = wd / "long_title.post.json"
    long_t.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    bad = run("check", long_t)
    rep = json.loads(ok.stdout) if ok.stdout.strip().startswith("{") else {"raw": ok.stdout[-300:]}
    return [check("pack skeleton for 3 platforms from the real file", set(json.loads(pk.read_text())["posts"]) == {"tiktok", "reels", "shorts"}),
            check("filled pack passes the lint (exit 0)", ok.returncode == 0, [ok.returncode, rep.get("errors"), (ok.stdout or ok.stderr)[-200:]], 0),
            check("a 120-character YouTube title is rejected (limit 100)", bad.returncode != 0, bad.returncode, "!= 0"),
            check("negative control: the empty skeleton is not ready", raw.returncode != 0, raw.returncode, "!= 0")], [filled, pk]


@card("FMT-39")
def share_sheet_or_upload_pages(task, wd):
    """Share the file through the system share sheet (navigator.share with files, title, text) or fall back to opening
    the upload pages; never posts by itself (no request leaves the page)."""
    page_js = """const LINKS=['https://www.tiktok.com/upload','https://www.youtube.com/upload','https://www.instagram.com/','https://www.facebook.com/reels/create'];
async function share(file,caption,nav){if(nav.share&&nav.canShare&&nav.canShare({files:[file]})){await nav.share({files:[file],title:'KOSIF',text:caption});return {via:'sheet'}}
 return {via:'links',links:LINKS}}
const sent=[];const origFetch=window.fetch;window.fetch=(...a)=>{sent.push(a[0]);return origFetch(...a)};
const f=new File([new Uint8Array([0,0,0,24,102,116,121,112])],'film.mp4',{type:'video/mp4'});let got=null;
const navWith={share:async p=>{got={n:p.files.length,name:p.files[0].name,title:p.title,text:p.text}},canShare:()=>true};
return Promise.all([share(f,'قهوة الصباح #قهوة',navWith),share(f,'x',{})]).then(r=>({a:r[0],b:r[1],got,sent:sent.length,native:typeof navigator.share}));"""
    js = "return null;"
    body = "<script>window.__p=(()=>{%s})();</script>" % page_js
    html = html_doc(body, js).replace(
        "const __r=(()=>{return null;})();document.getElementById('OUT').textContent=JSON.stringify(__r)",
        "window.__p.then(v=>{document.getElementById('OUT').textContent=JSON.stringify(v)})")
    o, page, _ = chrome_page(wd, "share", html, (320, 200))
    out = write_json(wd, "share.json", o)
    return [check("with a share sheet: the file, title and caption are handed over", o["a"]["via"] == "sheet" and o["got"] == {"n": 1, "name": "film.mp4", "title": "KOSIF", "text": "قهوة الصباح #قهوة"},
                  o["got"]),
            check("without one: the four upload pages are offered", o["b"]["via"] == "links" and len(o["b"]["links"]) == 4 and o["b"]["links"][0].endswith("tiktok.com/upload")),
            check("nothing is posted: no request left the page", o["sent"] == 0, o["sent"], 0),
            check("negative control: a navigator without share() does not use the sheet", o["b"]["via"] != "sheet")], [out, page]


def cloudinary_to_ffmpeg(spec, src_h):
    """Cloudinary-style URL transformations (so_/eo_/du_ trim, ac_none, c_limit,h_, fps_) -> local ffmpeg arguments."""
    pre, vf, args = [], [], []
    p = {}
    for comp in spec.split("/"):
        for kv in comp.split(","):
            if "_" in kv:
                k, v = kv.split("_", 1)
                p[k] = v
            else:
                p[kv] = True
    if "so" in p:
        pre += ["-ss", p["so"]]
    if "eo" in p:
        args += ["-t", str(float(p["eo"]) - float(p.get("so", 0)))]
    elif "du" in p:
        args += ["-t", p["du"]]
    if p.get("ac") == "none":
        args += ["-an"]
    if p.get("c") == "limit" and "h" in p and int(p["h"]) < src_h:
        vf.append("scale=-2:%s" % p["h"])
    if "fps" in p:
        vf.append("fps=%s" % p["fps"])
    if vf:
        args += ["-vf", ",".join(vf)]
    return pre, args


@card("FMT-41")
def url_variants_locally(task, wd):
    """Derive video variants the way Cloudinary URL transformations do (so_/eo_ trim, du_, ac_none, c_limit,h_, fps_,
    an animated preview), executed locally with ffmpeg since the hosted services need accounts."""
    src = wd / "master.mp4"
    fx.ffmpeg("-f", "lavfi", "-i", "testsrc2=s=640x360:r=30:d=6", "-f", "lavfi", "-i", "sine=f=440:d=6", "-c:v", "libx264", "-preset", "ultrafast",
              "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(src))

    def make(spec, name):
        pre, args = cloudinary_to_ffmpeg(spec, 360)
        dst = wd / name
        fx.ffmpeg(*pre, "-i", str(src), *args, *(["-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p"] if name.endswith(".mp4") else
                                                  ["-c:v", "libwebp_anim", "-loop", "0", "-q:v", "50"]), str(dst))
        pr = fx.probe(dst)
        v = [s for s in pr["streams"] if s["codec_type"] == "video"][0]
        return {"dur": float(pr["format"].get("duration", 0) or 0), "audio": any(s["codec_type"] == "audio" for s in pr["streams"]),
                "h": int(v["height"]), "fps": v.get("r_frame_rate"), "frames": int(v.get("nb_frames") or 0)}
    a = make("so_1,eo_4/ac_none/c_limit,h_240/fps_15", "trim_mute_240.mp4")
    b = make("du_5/c_limit,h_720", "limit720.mp4")
    c = make("so_0,eo_2/c_limit,h_180/fps_10", "preview.webp")
    m = make("du_6", "master_probe.mp4")
    out = write_json(wd, "variants.json", {"trim_mute_240": a, "limit720": b, "webp": c})
    return [check("so_1,eo_4 trims to 3 s and ac_none removes the audio", abs(a["dur"] - 3) < 0.1 and not a["audio"], [a["dur"], a["audio"]]),
            check("c_limit,h_240 scales down to 240 and fps_15 sets 15 fps", a["h"] == 240 and a["fps"] == "15/1", [a["h"], a["fps"]]),
            check("c_limit,h_720 never upscales a 360p master", b["h"] == 360 and abs(b["dur"] - 5) < 0.1, [b["h"], b["dur"]]),
            check("animated WebP preview written", (wd / "preview.webp").stat().st_size > 1000 and (wd / "preview.webp").read_bytes()[:4] == b"RIFF"),
            check("negative control: the untransformed master still has audio and its 6 s", m["audio"] and abs(m["dur"] - 6) < 0.1, [m["audio"], m["dur"]])], \
        [wd / "trim_mute_240.mp4", wd / "preview.webp", out]


@card("FMT-42")
def studio_cloud_bundle(task, wd):
    """build_studio_cloud.py bundles the Studio editor modules into one self-contained artifact page: modules wrapped in
    scopes with imports rewritten, mp4-muxer@5.2.1 from jsDelivr, saves through window.claude.use('downloads') with the
    four error codes mapped."""
    script = MM / "web/build_studio_cloud.py"
    page = wd / "studio-cloud.html"
    r = subprocess.run([sys.executable, str(script), "--out", str(page), "--home-url", "https://example.org/kosif-home"], capture_output=True, text=True,
                       timeout=60, cwd=str(wd), stdin=subprocess.DEVNULL)
    if r.returncode:
        raise RuntimeError("build failed: " + r.stderr[-300:])
    h = page.read_text(encoding="utf-8")
    srcs = [p for p in (MM / "web/static/studio").glob("*.mjs")]
    src_imports = sum(len(re.findall(r"^import .* from '\./", p.read_text(encoding="utf-8"), re.M)) for p in srcs)
    left = len(re.findall(r"^\s*import .* from ['\"]\./", h, re.M))
    ext = [s for s in re.findall(r'<script[^>]+src="([^"]+)"', h)]
    codes = all(c in h for c in ("declined", "too_large", "rate_limited", "rejected_extension"))
    mods = re.findall(r'<script type="module">(.*?)</script>', h, re.S)
    (wd / "module.mjs").write_text(mods[0] if mods else "", encoding="utf-8")
    syn = subprocess.run([NODE, "--check", str(wd / "module.mjs")], capture_output=True, text=True, timeout=30)
    return [check("one self-contained page of ~78.5 KB", 60000 < len(h.encode()) < 100000, len(h.encode()), "~78.5 KB"),
            check("relative module imports rewritten (none left)", left == 0, left, 0),
            check("only external script: mp4-muxer@5.2.1 from cdn.jsdelivr.net", ext == ["https://cdn.jsdelivr.net/npm/mp4-muxer@5.2.1/build/mp4-muxer.min.js"], ext),
            check("saves go through the downloads capability with all 4 error codes mapped", "window.claude?.use?.('downloads')" in h and codes),
            check("home URL embedded and the bundled module parses (node --check)", "example.org/kosif-home" in h and syn.returncode == 0, syn.stderr[-200:]),
            check("negative control: the unbundled source modules do use relative imports", src_imports > 0, src_imports, ">0")], [page]


@card("FMT-68")
def three_ready_briefs(task, wd):
    """The three ready briefs (doodle 9:16 30 s ar-EG, launch 16:9 20 s en, whiteboard 9:16 45 s ar) copied into a
    project/brief.json and planned with fastify-motion-bro's planner; the deliverable is an H.264 yuv420p +faststart
    CRF 19 MP4 with the storyboard's duration."""
    planner = FASTIFY / "scripts/planner.mjs"
    res = {}
    for name in ("demo-9x16", "launch-16x9", "whiteboard-ar"):
        root = wd / name
        (root / "project").mkdir(parents=True, exist_ok=True)
        shutil.copy(FASTIFY / "examples" / (name + ".json"), root / "project/brief.json")
        js = "import(%s).then(m=>{const s=m.plan(%s);console.log(JSON.stringify({aspect:s.aspect,dur:s.duration_seconds,lang:s.brief.language,n:s.scenes.length,"\
             "contig:s.scenes.every((x,i)=>i===0||x.start===s.scenes[i-1].end),last:s.scenes[s.scenes.length-1].end}))})" % (json.dumps(planner.as_uri()), json.dumps(str(root)))
        o, _ = node_json(wd, "plan_" + name.replace("-", "_"), js)
        o["files"] = sorted(p.name for p in (root / "project").iterdir())
        res[name] = o
    sb = json.loads((wd / "launch-16x9/project/storyboard.json").read_text(encoding="utf-8"))
    mp4 = wd / "launch_deliverable.mp4"
    fx.ffmpeg("-f", "lavfi", "-i", "color=c=#0b1020:s=320x180:r=30:d=%s" % sb["duration_seconds"], "-c:v", "libx264", "-profile:v", "high", "-crf", "19",
              "-preset", "medium", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(mp4))
    pr = fx.probe(mp4)
    v = pr["streams"][0]
    raw = mp4.read_bytes()[:4096]
    bad = wd / "bad"
    (bad / "project").mkdir(parents=True, exist_ok=True)
    (bad / "project/brief.json").write_text(json.dumps({"title": "x", "topic": "y", "aspect": "4:5", "duration_seconds": 20}), encoding="utf-8")
    rej = subprocess.run([NODE, "-e", "import(%s).then(m=>{try{m.plan(%s);console.log('ok')}catch(e){console.log('rejected:'+e.message)}})"
                          % (json.dumps(planner.as_uri()), json.dumps(str(bad)))], capture_output=True, text=True, timeout=30)
    out = write_json(wd, "briefs.json", res)
    want = {"demo-9x16": ("9:16", 30, "ar-EG"), "launch-16x9": ("16:9", 20, "en"), "whiteboard-ar": ("9:16", 45, "ar")}
    return [check("each brief planned with its aspect, length and language", all((res[k]["aspect"], res[k]["dur"], res[k]["lang"]) == w for k, w in want.items()),
                  {k: (v["aspect"], v["dur"], v["lang"]) for k, v in res.items()}),
            check("contiguous scenes that end at the brief duration", all(r["contig"] and r["last"] == r["dur"] for r in res.values())),
            check("planner wrote storyboard.json, STYLE.md and PLAN.md", all({"PLAN.md", "STYLE.md", "storyboard.json"} <= set(r["files"]) for r in res.values())),
            check("deliverable: H.264 High yuv420p, moov before mdat (+faststart), 20 s", v["codec_name"] == "h264" and v["pix_fmt"] == "yuv420p" and v.get("profile") == "High"
                  and raw.find(b"moov") != -1 and (raw.find(b"mdat") == -1 or raw.find(b"moov") < raw.find(b"mdat")) and abs(float(pr["format"]["duration"]) - 20) < 0.1,
                  [v["codec_name"], v["pix_fmt"], v.get("profile")]),
            check("negative control: a 4:5 brief is rejected by the planner", rej.stdout.strip().startswith("rejected"), rej.stdout.strip())], [out, mp4]


# ═════════════════════════════════════════════ knowledge-graph (Graphify's method on Python ast + networkx) ═════════════════════════════════════════════
# graphify (graphifyy) is not installed here and could not be installed; these runners do the same AST method with the
# standard library `ast` and networkx (Louvain communities in place of Leiden), on a fixture code folder.
_CODE = {
    "app/aspects.py": '"""Aspect ratios."""\n\ndef ratio(name):\n    """Width over height for a named aspect."""\n    return {"9:16": 9 / 16}.get(name, 1)\n\n\ndef even(v):\n    return int(v) // 2 * 2\n',
    "app/render.py": "from app.aspects import ratio, even\nfrom app.base import Job\n\n\nclass RenderJob(Job):\n    def size(self, h):\n        return even(h * ratio(self.aspect)), h\n\n\ndef render(job):\n    return job.size(1920)\n",
    "app/base.py": "class Job:\n    aspect = '9:16'\n\n    def run(self):\n        return self.size(1080)\n",
    "app/cli.py": "from app.render import render, RenderJob\nfrom app.aspects import ratio\n\n\ndef build_prompt(x):\n    return 'make %s' % x\n\n\ndef cmd_scaffold():\n    return render(RenderJob()), build_prompt('a'), ratio('9:16')\n",
    "app/cycle_a.py": "import app.cycle_b\n\n\ndef ping():\n    return app.cycle_b.pong()\n",
    "app/cycle_b.py": "import app.cycle_a\n\n\ndef pong():\n    return 1\n",
}


def write_code(root, files=_CODE):
    for rel, src in files.items():
        p = Path(root) / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(src, encoding="utf-8")
    return Path(root)


class CodeGraph:
    """Symbols, calls, imports, inheritance and docstring rationale nodes extracted from Python files by AST."""

    def __init__(self):
        import networkx as nx
        self.G = nx.MultiDiGraph()
        self.hashes = {}
        self.parsed = []

    def _mod(self, rel):
        return rel[:-3].replace("/", ".")

    def extract_file(self, root, rel):
        self.parsed.append(rel)
        G = self.G
        for n in [n for n, d in G.nodes(data=True) if d.get("file") == rel]:
            G.remove_node(n)
        src = (Path(root) / rel).read_text(encoding="utf-8")
        self.hashes[rel] = hashlib.sha256(src.encode()).hexdigest()
        tree = ast.parse(src)
        G.add_node(rel, kind="file", file=rel, line=1, label=rel)
        imports = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                tgt = node.module.replace(".", "/") + ".py"
                G.add_edge(rel, tgt, rel_type="imports_from", line=node.lineno, prov="EXTRACTED")
                for a in node.names:
                    imports[a.asname or a.name] = tgt
            elif isinstance(node, ast.Import):
                for a in node.names:
                    tgt = a.name.replace(".", "/") + ".py"
                    G.add_edge(rel, tgt, rel_type="imports", line=node.lineno, prov="EXTRACTED")
                    imports[a.name] = tgt

        def add_def(fn, owner=None):
            name = ("%s.%s" % (owner, fn.name) if owner else fn.name) + "()"
            nid = "%s::%s" % (rel, name)
            G.add_node(nid, kind="function", file=rel, line=fn.lineno, label=name)
            G.add_edge(rel, nid, rel_type="contains", line=fn.lineno, prov="EXTRACTED")
            doc = ast.get_docstring(fn)
            if doc:
                rid = nid + "#why"
                G.add_node(rid, kind="rationale", file=rel, line=fn.lineno, label=doc[:60])
                G.add_edge(nid, rid, rel_type="rationale", line=fn.lineno, prov="EXTRACTED")
            for c in ast.walk(fn):
                if isinstance(c, ast.Call):
                    f = c.func
                    callee = f.id if isinstance(f, ast.Name) else f.attr if isinstance(f, ast.Attribute) else None
                    if callee:
                        G.add_edge(nid, ("?", callee, imports.get(callee)), rel_type="calls", line=c.lineno, prov="EXTRACTED")
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                add_def(node)
            elif isinstance(node, ast.ClassDef):
                cid = "%s::%s" % (rel, node.name)
                G.add_node(cid, kind="class", file=rel, line=node.lineno, label=node.name)
                G.add_edge(rel, cid, rel_type="contains", line=node.lineno, prov="EXTRACTED")
                for b in node.bases:
                    if isinstance(b, ast.Name):
                        G.add_edge(cid, ("?", b.id, imports.get(b.id)), rel_type="inherits", line=node.lineno, prov="EXTRACTED")
                for f in node.body:
                    if isinstance(f, ast.FunctionDef):
                        add_def(f, node.name)

    def resolve(self):
        G = self.G
        names = {}
        for n, d in G.nodes(data=True):
            if isinstance(n, str) and d.get("kind") in ("function", "class"):
                names.setdefault(d["label"].rstrip("()").split(".")[-1], []).append(n)
        for u, v, k, d in list(G.edges(keys=True, data=True)):
            if isinstance(v, tuple):
                _, name, hint = v
                cands = names.get(name, [])
                if hint:
                    cands = [c for c in cands if c.startswith(hint + "::")] or cands
                G.remove_edge(u, v, k)
                for c in cands[:1] if hint else cands:
                    G.add_edge(u, c, rel_type=d["rel_type"], line=d["line"], prov="EXTRACTED" if hint or len(cands) == 1 else "INFERRED")
        for n in [n for n in G.nodes if isinstance(n, tuple)]:
            G.remove_node(n)
        for n in list(G.nodes):
            if "kind" not in G.nodes[n]:
                G.nodes[n].update(kind="file", file=n, line=1, label=n)

    def extract(self, root, only=None):
        root = Path(root)
        for p in sorted(root.rglob("*.py")):
            rel = p.relative_to(root).as_posix()
            if only is None or rel in only:
                self.extract_file(root, rel)
        self.resolve()
        return self

    def update(self, root):
        root = Path(root)
        changed = [p.relative_to(root).as_posix() for p in sorted(root.rglob("*.py"))
                   if self.hashes.get(p.relative_to(root).as_posix()) != hashlib.sha256(p.read_bytes()).hexdigest()]
        self.parsed = []
        for rel in changed:
            self.extract_file(root, rel)
        self.resolve()
        return changed

    def communities(self, seed=1):
        import networkx as nx
        U = nx.Graph()
        U.add_nodes_from(n for n, d in self.G.nodes(data=True) if d["kind"] != "rationale")
        U.add_edges_from((u, v) for u, v, d in self.G.edges(data=True) if d["rel_type"] != "rationale")
        return [sorted(c) for c in nx.community.louvain_communities(U, seed=seed)]

    def save(self, out):
        out = Path(out)
        out.mkdir(parents=True, exist_ok=True)
        data = {"nodes": [{"id": n, **d} for n, d in self.G.nodes(data=True)],
                "edges": [{"source": u, "target": v, **d} for u, v, d in self.G.edges(data=True)]}
        (out / "graph.json").write_text(json.dumps(data, indent=1), encoding="utf-8")
        return out / "graph.json"

    def report(self, out):
        import networkx as nx
        G = self.G
        deg = sorted(((G.degree(n), n) for n, d in G.nodes(data=True) if d["kind"] in ("function", "class")), reverse=True)
        imp = nx.DiGraph([(u, v) for u, v, d in G.edges(data=True) if d["rel_type"] in ("imports", "imports_from")])
        cycles = sorted(sorted(c) for c in nx.simple_cycles(imp))
        com = self.communities()
        lines = ["# GRAPH_REPORT", "", "%d nodes, %d edges, %d communities" % (G.number_of_nodes(), G.number_of_edges(), len(com)), "",
                 "## God nodes"] + ["- %s (%d)" % (n, d) for d, n in deg[:5]] + ["", "## Import cycles"] + ["- " + " <-> ".join(c) for c in cycles]
        (Path(out) / "GRAPH_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        return {"god": [n for _, n in deg[:5]], "cycles": cycles, "communities": com}

    # queries ──────────────────────────────────────────────
    def match(self, words):
        import math as _m
        labels = {n: d["label"].lower() for n, d in self.G.nodes(data=True) if d["kind"] in ("function", "class")}
        toks = [w.lower() for w in re.split(r"[\s_]+", words) if w]
        df = {t: sum(t in l for l in labels.values()) for t in toks}
        score = {n: sum(_m.log(1 + len(labels) / df[t]) for t in toks if df[t] and t in l) for n, l in labels.items()}
        best = max(score.values()) if score else 0
        if best <= 0:
            return 4, []
        top = [n for n, s in score.items() if abs(s - best) < 1e-9]
        return (0 if len(top) == 1 else 3), sorted(top)

    def explain(self, nid):
        G = self.G
        rows = [("out", d["rel_type"], v, "%s:L%d" % (G.nodes[nid]["file"], d["line"]), d["prov"]) for _, v, d in G.out_edges(nid, data=True)]
        rows += [("in", d["rel_type"], u, "%s:L%d" % (G.nodes[u]["file"], d["line"]), d["prov"]) for u, _, d in G.in_edges(nid, data=True)]
        return sorted(rows)

    def query(self, words, budget=400):
        code, hits = self.match(words)
        if code:
            return code, hits, ""
        seen, frontier, text = {hits[0]}, [hits[0]], []
        while frontier:
            nxt = []
            for n in frontier:
                for _, v, d in list(self.G.out_edges(n, data=True)) + [(u, n, d) for u, _, d in self.G.in_edges(n, data=True)]:
                    m = v if v != n else _
                    line = "%s -%s-> %s (%s:L%d)" % (n, d["rel_type"], v, self.G.nodes[n]["file"], d["line"])
                    text.append(line)
                    if m not in seen:
                        seen.add(m)
                        nxt.append(m)
            frontier = nxt
        out = "\n".join(text)
        return 0, hits, out[:budget] + ("\n[cut %d chars to the budget]" % (len(out) - budget) if len(out) > budget else "")

    def affected(self, target, depth=2):
        rels = {"calls", "imports", "imports_from", "inherits", "references", "uses", "implements"}
        G = self.G
        start = {target} | {n for n in G.nodes if isinstance(n, str) and n.startswith(target + "::")}
        seen, frontier, hits = set(start), set(start), []
        for _ in range(depth):
            nxt = set()
            for n in frontier:
                for u, _, d in G.in_edges(n, data=True):
                    if d["rel_type"] in rels and u not in seen:
                        hits.append((u, d["rel_type"], "%s:L%d" % (G.nodes[u]["file"], d["line"])))
                        seen.add(u)
                        nxt.add(u)
            frontier = nxt
        return sorted(hits)


@card("GRAPH-02")
def code_folder_to_graph(task, wd):
    """Turn a code folder into a knowledge graph by AST (symbols, calls, imports, inheritance, communities) with no
    model, on a COPY of the folder, and write graph.json + GRAPH_REPORT.md (god nodes, import cycles, communities)."""
    src = write_code(wd / "src")
    copy = wd / "copy"
    shutil.copytree(src, copy)
    t0 = time.time()
    g = CodeGraph().extract(copy)
    gj = g.save(wd / "graphify-out")
    rep = g.report(wd / "graphify-out")
    dt = time.time() - t0
    G = g.G
    rel = lambda r: sum(1 for *_, d in G.edges(data=True) if d["rel_type"] == r)
    calls = {(u, v) for u, v, d in G.edges(data=True) if d["rel_type"] == "calls"}
    data_only = CodeGraph()
    (wd / "data").mkdir(exist_ok=True)
    (wd / "data/table.py").write_text("ROWS = [1, 2, 3]\n", encoding="utf-8")
    data_only.extract(wd / "data")
    syms = sum(1 for _, d in data_only.G.nodes(data=True) if d["kind"] in ("function", "class"))
    return [check("symbols extracted (9 functions/methods + 2 classes)", sum(1 for _, d in G.nodes(data=True) if d["kind"] in ("function", "class")) == 11,
                  sum(1 for _, d in G.nodes(data=True) if d["kind"] in ("function", "class")), 11),
            check("call edge cmd_scaffold() -> render() resolved through the import", ("app/cli.py::cmd_scaffold()", "app/render.py::render()") in calls),
            check("inheritance RenderJob -> Job", any(d["rel_type"] == "inherits" and v == "app/base.py::Job" for _, v, d in G.edges(data=True))),
            check("import cycle cycle_a <-> cycle_b reported", rep["cycles"] == [["app/cycle_a.py", "app/cycle_b.py"]], rep["cycles"]),
            check("communities found and the report written", len(rep["communities"]) >= 2 and (wd / "graphify-out/GRAPH_REPORT.md").stat().st_size > 50, len(rep["communities"])),
            check("the source folder is untouched (output beside the copy)", not (src / "graphify-out").exists() and sorted(p.name for p in src.rglob("*")) == sorted(p.name for p in copy.rglob("*"))),
            check("fast: under 2 s", dt < 2, dt),
            check("negative control: a data-only file yields no symbols", syms == 0, syms, 0)], [gj, wd / "graphify-out/GRAPH_REPORT.md"]


@card("GRAPH-03")
def graph_query_explain(task, wd):
    """Ask the graph: query (substring + IDF match, BFS with a soft budget), explain (every edge with direction,
    relation, EXTRACTED/INFERRED and file:line), path A B; exit codes 0 answered, 3 ambiguous, 4 not found."""
    import networkx as nx
    g = CodeGraph().extract(write_code(wd / "src"))
    code, hits, text = g.query("build prompt", budget=300)
    amb_code, amb = g.match("ping pong")
    nf_code, _ = g.match("فيديو")
    ex = g.explain("app/cli.py::build_prompt()")
    U = g.G.to_undirected(as_view=False)
    path = nx.shortest_path(U, "app/cli.py::cmd_scaffold()", "app/aspects.py::even()")
    out = write_json(wd, "answers.json", {"query": {"code": code, "hits": hits, "text": text}, "ambiguous": amb, "explain": ex, "path": path})
    return [check("'build prompt' answers build_prompt() (exit 0)", code == 0 and hits == ["app/cli.py::build_prompt()"], [code, hits]),
            check("explain lists the caller with direction and file:line", ("in", "calls", "app/cli.py::cmd_scaffold()", "app/cli.py:L10", "EXTRACTED") in ex, ex),
            check("an ambiguous word exits 3 with the candidates", amb_code == 3 and len(amb) >= 2, [amb_code, amb]),
            check("the BFS answer respects the soft budget and says what was cut", "[cut" in text or len(text) <= 300, len(text)),
            check("shortest structural path cmd_scaffold -> even", path[0].endswith("cmd_scaffold()") and path[-1].endswith("even()") and len(path) <= 5, path),
            check("negative control: an Arabic sentence matches nothing (exit 4, no translation)", nf_code == 4, nf_code, 4)], [out]


@card("GRAPH-04")
def graph_affected(task, wd):
    """Reverse traversal (calls, imports, inheritance ...) to depth 2: exactly who depends on aspects.py before editing,
    with file:line; an undirected BFS over-reports."""
    import networkx as nx
    g = CodeGraph().extract(write_code(wd / "src"))
    hits = g.affected("app/aspects.py", depth=2)
    who = sorted({h[0] for h in hits})
    U = g.G.to_undirected(as_view=False)
    starts = [n for n in U if isinstance(n, str) and n.startswith("app/aspects.py")]
    und = set()
    for s in starts:
        und |= set(nx.single_source_shortest_path_length(U, s, cutoff=2))
    out = write_json(wd, "affected.json", {"dependents": hits, "undirected_bfs_size": len(und)})
    want = {"app/cli.py", "app/render.py", "app/render.py::RenderJob.size()", "app/cli.py::cmd_scaffold()"}
    return [check("importing files and call sites found", want <= set(who), who),
            check("every hit carries file:line", all(re.match(r"app/\w+\.py:L\d+$", h[2]) for h in hits)),
            check("unrelated cycle files are not reported", not any("cycle" in w for w in who), who),
            check("negative control: an undirected BFS reaches more of the graph than the dependents", len(und) > len(who) + 3, [len(und), len(who)])], [out]


@card("GRAPH-05")
def graph_incremental_update(task, wd):
    """Refresh after an edit: only changed files are re-extracted (by content hash); graph.json and the report are
    rewritten and docstrings become rationale nodes."""
    src = write_code(wd / "src")
    g = CodeGraph().extract(src)
    first = len(g.parsed)
    p = src / "app/aspects.py"
    p.write_text(p.read_text() + '\n\ndef odd(v):\n    """Odd sizes break yuv420p."""\n    return even(v) + 1\n', encoding="utf-8")
    t0 = time.time()
    changed = g.update(src)
    dt = time.time() - t0
    gj = g.save(wd / "graphify-out")
    g.report(wd / "graphify-out")
    G = g.G
    new_call = any(u == "app/aspects.py::odd()" and v == "app/aspects.py::even()" for u, v, d in G.edges(data=True) if d["rel_type"] == "calls")
    rationale = [d["label"] for _, d in G.nodes(data=True) if d["kind"] == "rationale"]
    nothing = g.update(src)
    return [check("first build parsed all 6 files", first == 6, first, 6),
            check("update re-extracted only the edited file", changed == ["app/aspects.py"] and g.parsed == [], changed),
            check("the new function and its call edge are in the graph", new_call),
            check("docstrings became rationale nodes", "Odd sizes break yuv420p." in rationale and "Width over height for a named aspect." in rationale, rationale),
            check("update is fast (< 1.2 s)", dt < 1.2, dt),
            check("negative control: with no edits nothing is re-extracted", nothing == [], nothing, [])], [gj, wd / "graphify-out/GRAPH_REPORT.md"]


@card("GRAPH-06")
def graph_lessons(task, wd):
    """save-result per answer (useful / dead_end / corrected) then reflect: a deterministic LESSONS.md with Tentative
    (fewer than 2 corroborations), Known dead ends, decayed with a 30-day half-life."""
    now = 1_790_000_000
    day = 86400
    results = [{"q": "where is the aspect rule", "nodes": ["ratio()"], "outcome": "useful", "t": now - 2 * day},
               {"q": "aspect width", "nodes": ["ratio()"], "outcome": "useful", "t": now - 40 * day},
               {"q": "who renders", "nodes": ["render()"], "outcome": "useful", "t": now - 1 * day},
               {"q": "font loader", "nodes": ["load_font()"], "outcome": "dead_end", "t": now - 3 * day},
               {"q": "even sizes", "nodes": ["even()"], "outcome": "corrected", "t": now - 5 * day}]
    store = wd / "graphify-out/reflections"
    store.mkdir(parents=True, exist_ok=True)
    for i, r in enumerate(results):
        (store / ("result_%02d.json" % i)).write_text(json.dumps(r), encoding="utf-8")

    def reflect(folder, half_life=30, min_corr=2):
        rows = [json.loads(p.read_text()) for p in sorted(folder.glob("result_*.json"))]
        agg = {}
        for r in rows:
            w = 0.5 ** ((now - r["t"]) / (half_life * day))
            for n in r["nodes"]:
                a = agg.setdefault(n, {"useful": 0, "dead_end": 0, "corrected": 0, "weight": 0.0})
                a[r["outcome"]] += 1
                a["weight"] += w if r["outcome"] == "useful" else -w
        trusted = sorted(n for n, a in agg.items() if a["useful"] >= min_corr)
        tentative = sorted(n for n, a in agg.items() if 0 < a["useful"] < min_corr)
        dead = sorted(n for n, a in agg.items() if a["dead_end"])
        md = ["# LESSONS", "", "## Trusted"] + ["- %s (weight %.3f)" % (n, agg[n]["weight"]) for n in trusted] + \
             ["", "## Tentative"] + ["- " + n for n in tentative] + ["", "## Known dead ends"] + ["- " + n for n in dead]
        return "\n".join(md) + "\n", agg, trusted, tentative, dead
    md, agg, trusted, tentative, dead = reflect(store)
    (store / "LESSONS.md").write_text(md, encoding="utf-8")
    md2 = reflect(store)[0]
    w40 = 0.5 ** (40 / 30)
    empty = wd / "empty"
    empty.mkdir()
    md_e, _, tr_e, te_e, de_e = reflect(empty)
    return [check("ratio() corroborated twice -> trusted", trusted == ["ratio()"], trusted),
            check("render() seen once -> tentative", tentative == ["render()"], tentative),
            check("load_font() listed as a known dead end", dead == ["load_font()"], dead),
            check("30-day half-life weighting (2 d + 40 d answers)", abs(agg["ratio()"]["weight"] - (0.5 ** (2 / 30) + w40)) < 1e-9, agg["ratio()"]["weight"]),
            check("reflect is deterministic", md == md2),
            check("negative control: with no saved results there are no lessons", not (tr_e or te_e or de_e))], [store / "LESSONS.md"]


@card("GRAPH-08")
def graph_exports(task, wd):
    """Export the graph: an agent wiki (index.md + one article per community), Obsidian notes with links, GraphML for
    Gephi/yEd, Neo4j Cypher, and a self-contained HTML page (no third-party CDN)."""
    import networkx as nx
    g = CodeGraph().extract(write_code(wd / "src"))
    com = g.communities()
    wiki = wd / "wiki"
    wiki.mkdir()
    idx = ["# Code wiki", ""]
    for i, c in enumerate(com):
        name = "community-%02d.md" % i
        (wiki / name).write_text("# Community %d\n\n" % i + "\n".join("- `%s` (%s:L%d)" % (n, g.G.nodes[n]["file"], g.G.nodes[n]["line"]) for n in c) + "\n", encoding="utf-8")
        idx.append("- [Community %d](%s) — %d nodes" % (i, name, len(c)))
    (wiki / "index.md").write_text("\n".join(idx) + "\n", encoding="utf-8")
    obs = wd / "obsidian"
    obs.mkdir()
    for n, d in g.G.nodes(data=True):
        if d["kind"] == "file":
            links = sorted({v for _, v, e in g.G.out_edges(n, data=True) if e["rel_type"] in ("imports", "imports_from")})
            (obs / (n.replace("/", "__") + ".md")).write_text("# %s\n\n" % n + "\n".join("[[%s]]" % l.replace("/", "__") for l in links) + "\n", encoding="utf-8")
    S = nx.DiGraph()
    for n, d in g.G.nodes(data=True):
        S.add_node(n, kind=d["kind"], file=d["file"], line=d["line"])
    for u, v, d in g.G.edges(data=True):
        S.add_edge(u, v, rel=d["rel_type"])
    nx.write_graphml(S, wd / "graph.graphml")
    back = nx.read_graphml(wd / "graph.graphml")
    cy = ["CREATE (:Node {id:%s, kind:%s});" % (json.dumps(n), json.dumps(d["kind"])) for n, d in S.nodes(data=True)]
    cy += ["MATCH (a:Node {id:%s}),(b:Node {id:%s}) CREATE (a)-[:%s]->(b);" % (json.dumps(u), json.dumps(v), d["rel"].upper()) for u, v, d in S.edges(data=True)]
    (wd / "cypher.txt").write_text("\n".join(cy) + "\n", encoding="utf-8")
    page = wd / "graph.html"
    page.write_text("<!doctype html><meta charset=utf-8><title>Code graph</title><pre id=g></pre><script>const G=%s;document.getElementById('g').textContent="
                    "G.nodes.length+' nodes'</script>" % json.dumps({"nodes": list(S.nodes), "edges": [[u, v] for u, v in S.edges]}), encoding="utf-8")
    articles = sorted(p.name for p in wiki.glob("community-*.md"))
    linked = re.findall(r"\]\((community-\d+\.md)\)", (wiki / "index.md").read_text())
    cdn = re.findall(r"https?://", page.read_text())
    return [check("wiki: index.md links one article per community", linked == articles and len(articles) == len(com), [len(linked), len(com)]),
            check("GraphML round-trips node and edge counts", (back.number_of_nodes(), back.number_of_edges()) == (S.number_of_nodes(), S.number_of_edges()),
                  (back.number_of_nodes(), back.number_of_edges())),
            check("Cypher has one CREATE per node and one MATCH per edge", len(cy) == S.number_of_nodes() + S.number_of_edges()),
            check("Obsidian note for cli.py links its imports", "[[app__render.py]]" in (obs / "app__cli.py.md").read_text()),
            check("HTML page is self-contained (no CDN)", cdn == []),
            check("negative control: a graph with no nodes yields no articles", CodeGraph().communities() == [])], \
        [wiki / "index.md", wd / "graph.graphml", wd / "cypher.txt", page]


GAPS.update({
    "power:MISC-19": "the Audit Studio / Audit Pro / KOSIF Earth apps (kosif-audit-studio) are not in this checkout",
    "power:MISC-P04": "tools/render_catalog.py and references/CAPABILITIES.csv (the 60 capability cards) are not in this checkout",
})


# ═════════════════════════════════════════════ other (misc) ═════════════════════════════════════════════
@card("MISC-03")
def fts5_skill_search(task, wd):
    """SQLite FTS5 over a folder of third-party SKILL.md files (the deep index method on a fixture mirror): build once,
    query with MATCH, rank by bm25, count indexed words."""
    import sqlite3
    mirror = wd / "atlas"
    docs = {"remotion-captions": "Remotion captions with ffmpeg burn-in and word timing", "ffmpeg-loudnorm": "ffmpeg loudnorm two pass to -14 LUFS",
            "arabic-shaping": "Arabic shaping with HarfBuzz raqm for subtitles", "music-beats": "Detect beats with librosa onset strength",
            "remotion-deploy": "Deploy Remotion Lambda render farm", "pdf-ocr": "OCR scanned PDF pages with tesseract ara"}
    for k, v in docs.items():
        (mirror / k).mkdir(parents=True, exist_ok=True)
        (mirror / k / "SKILL.md").write_text("---\nname: %s\n---\n# %s\n\n%s\n" % (k, k, v), encoding="utf-8")
    db = wd / "deep_index.sqlite"
    con = sqlite3.connect(db)
    con.execute("CREATE VIRTUAL TABLE skills USING fts5(name, body, tokenize='unicode61')")
    words = 0
    for p in sorted(mirror.glob("*/SKILL.md")):
        body = p.read_text(encoding="utf-8")
        words += len(body.split())
        con.execute("INSERT INTO skills VALUES (?, ?)", (p.parent.name, body))
    con.commit()
    q = lambda m: [r[0] for r in con.execute("SELECT name FROM skills WHERE skills MATCH ? ORDER BY bm25(skills)", (m,))]
    both = q("remotion AND ffmpeg")
    rem = q("remotion")
    phrase = q('"word timing"')
    none = q("blender")
    con.close()
    out = write_json(wd, "search.json", {"remotion AND ffmpeg": both, "remotion": rem, "phrase": phrase, "words": words})
    return [check("AND query finds the one skill with both techniques", both == ["remotion-captions"], both),
            check("single-term query finds both Remotion skills", sorted(rem) == ["remotion-captions", "remotion-deploy"], rem),
            check("phrase query works", phrase == ["remotion-captions"], phrase),
            check("word count of the indexed mirror", words == sum(len(("---\nname: %s\n---\n# %s\n\n%s\n" % (k, k, v)).split()) for k, v in docs.items()), words),
            check("negative control: a technique absent from the mirror returns nothing", none == [], none, [])], [db, out]


@card("MISC-05")
def web_mcp_endpoint(task, wd):
    """Start the KOSIF Motion Web server (scripts/web/server.py, home = the work folder) on a loopback port and speak
    JSON-RPC MCP to /mcp: initialize (protocol 2025-03-26), tools/list (22 tools), ping, tools/call; a request from a
    foreign web origin is refused."""
    import urllib.request
    import urllib.error
    port = free_port()
    env = {k: v for k, v in os.environ.items() if k.lower() not in ("http_proxy", "https_proxy")}
    env.update(KOSIF_MOTION_HOME=str(wd / "home"), NO_PROXY="*")
    log = open(wd / "server.log", "w")
    proc = subprocess.Popen([sys.executable, str(MM / "web/server.py"), "--port", str(port), "--workers", "1"], stdout=log, stderr=subprocess.STDOUT,
                            env=env, cwd=str(wd), stdin=subprocess.DEVNULL)
    base = "http://127.0.0.1:%d/mcp" % port
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

    def rpc(method, params=None, headers=None):
        body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params or {}}).encode()
        req = urllib.request.Request(base, data=body, headers={"Content-Type": "application/json", **(headers or {})})
        try:
            with opener.open(req, timeout=10) as r:
                return r.status, json.loads(r.read() or b"{}")
        except urllib.error.HTTPError as e:
            return e.code, {}
    try:
        t0 = time.time()
        while time.time() - t0 < 10:
            try:
                with opener.open(base, timeout=1) as r:
                    if r.status == 200:
                        break
            except Exception:
                time.sleep(0.15)
        init = rpc("initialize")[1]
        tools = rpc("tools/list")[1]
        ping = rpc("ping")[1]
        call = rpc("tools/call", {"name": "motion_templates", "arguments": {}})[1]
        unknown = rpc("no/such")[1]
        foreign = rpc("tools/list", headers={"Origin": "https://evil.example", "Sec-Fetch-Site": "cross-site"})[0]
    finally:
        proc.terminate()
        proc.wait(timeout=10)
        log.close()
    names = [t["name"] for t in tools["result"]["tools"]]
    out = write_json(wd, "mcp-session.json", {"initialize": init, "tools": names, "call": str(call)[:500]})
    return [check("initialize answers protocol 2025-03-26", init["result"]["protocolVersion"] == "2025-03-26", init["result"]["protocolVersion"]),
            check("tools/list exposes 22 tools incl. motion_plan and kosif_render_manifest", len(names) == 22 and "motion_plan" in names and "kosif_render_manifest" in names, len(names), 22),
            check("ping returns an empty result", ping.get("result") == {}),
            check("tools/call motion_templates returns structured content", "content" in call.get("result", {}) and call["result"]["content"][0]["type"] == "text"),
            check("unknown method -> JSON-RPC -32601", unknown.get("error", {}).get("code") == -32601, unknown.get("error")),
            check("negative control: a cross-site page cannot post to the local server", foreign in (403, 400), foreign, 403)], [out, wd / "server.log"]


@card("MISC-08")
def one_contract_many_agents(task, wd):
    """One contract wired for Claude (CLAUDE.md, .claude/skills), Codex/Cursor (AGENTS.md, .agents/skills), Gemini
    (GEMINI.md) and Copilot (.github/copilot-instructions.md): audit the real fastify-motion-bro checkout (read-only)
    for entry files that point at AGENTS.md + an existing SKILL.md and for 9 skills x 3 identical copies."""
    def audit(root):
        root = Path(root)
        entries = {}
        for f in ("CLAUDE.md", "GEMINI.md", ".github/copilot-instructions.md"):
            p = root / f
            t = p.read_text(encoding="utf-8") if p.exists() else ""
            paths = re.findall(r"[\w./-]*SKILL\.md", t)
            entries[f] = {"agents": "AGENTS.md" in t, "skill_paths_ok": bool(paths) and all((root / x).exists() for x in paths) or ("SKILL.md" not in t and "AGENTS.md" in t)}
        trees = [".claude/skills", ".agents/skills", "skills"]
        names = sorted(p.parent.name for p in (root / "skills").glob("*/SKILL.md"))
        copies = {n: len({sha(root / t / n / "SKILL.md") for t in trees if (root / t / n / "SKILL.md").exists()}) for n in names}
        present = {n: sum((root / t / n / "SKILL.md").exists() for t in trees) for n in names}
        return {"entries": entries, "skills": names, "distinct_versions": copies, "copies": present}
    real = audit(FASTIFY)
    tamper = wd / "fixture"
    for f in ("AGENTS.md", "CLAUDE.md", "GEMINI.md", ".github/copilot-instructions.md"):
        (tamper / f).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(FASTIFY / f, tamper / f)
    for t in (".claude/skills", ".agents/skills", "skills"):
        shutil.copytree(FASTIFY / t, tamper / t)
    p = tamper / ".agents/skills/stickman/SKILL.md"
    p.write_text(p.read_text(encoding="utf-8") + "\nlocal drift\n", encoding="utf-8")
    bad = audit(tamper)
    out = write_json(wd, "contract-audit.json", {"fastify": real, "tampered_fixture": bad})
    return [check("9 skills, each in 3 trees", len(real["skills"]) == 9 and set(real["copies"].values()) == {3}, [len(real["skills"]), set(real["copies"].values())]),
            check("the 3 copies are byte-identical for every skill", set(real["distinct_versions"].values()) == {1}, real["distinct_versions"]),
            check("every entry file points at AGENTS.md", all(e["agents"] for e in real["entries"].values()), real["entries"]),
            check("SKILL.md paths named in entry files exist", all(e["skill_paths_ok"] for e in real["entries"].values()), real["entries"]),
            check("negative control: a drifted copy is caught", bad["distinct_versions"]["stickman"] == 2, bad["distinct_versions"]["stickman"], 2)], [out]


_GATE_RULES = [("BLOCK", r"\bpassword|كلمة السر|credit card|card number|\bcvv\b|payment|pay now|ادفع"),
               ("HANDOFF", r"captcha|verification code|\botp\b|رمز التحقق|2fa"),
               ("CONFIRM", r"\bsend\b|\bpost\b|publish|delete|remove|install|submit|ارسل|انشر|احذف")]
_GATE_EXIT = {"RUN": 0, "CONFIRM": 1, "BLOCK": 3, "HANDOFF": 4}


def action_gate(goal, steps, approved=(), allowed_domains=()):
    rows = []
    for i, s in enumerate(steps):
        verdict = "RUN"
        dom = re.search(r"https?://([^/\s]+)", s)
        if dom and allowed_domains and dom.group(1) not in allowed_domains:
            verdict = "BLOCK"
        else:
            for v, pat in _GATE_RULES:
                if re.search(pat, s, re.I):
                    verdict = v
                    break
            if verdict == "CONFIRM" and i in approved:
                verdict = "RUN"
        rows.append({"step": s, "verdict": verdict})
    worst = max((r["verdict"] for r in rows), key=lambda v: [0, 1, 4, 3].index(_GATE_EXIT[v]))
    return {"goal": goal, "steps": rows, "verdict": worst, "exit": _GATE_EXIT[worst]}


@card("MISC-11")
def gui_action_gate(task, wd):
    """Classify planned browser/GUI steps RUN / CONFIRM / HANDOFF / BLOCK (CAPTCHA, verification codes, passwords,
    payment, send, delete, install) with exit 0 / 1 / 4 / 3; approved indices pass, foreign domains block."""
    dom = ["studio.example"]
    a = action_gate("export a reel", ["open https://studio.example/editor", "click Export", "wait for render"], allowed_domains=dom)
    b = action_gate("share", ["open https://studio.example/editor", "post the reel to the channel"], allowed_domains=dom)
    c = action_gate("share", ["open https://studio.example/editor", "post the reel to the channel"], approved=[1], allowed_domains=dom)
    d = action_gate("login", ["open https://studio.example/login", "type the verification code from SMS"], allowed_domains=dom)
    e = action_gate("buy", ["open https://studio.example/cart", "enter credit card number"], allowed_domains=dom)
    f = action_gate("browse", ["open https://unknown.example/"], allowed_domains=dom)
    out = write_json(wd, "gate.json", {"run": a, "confirm": b, "approved": c, "handoff": d, "block": e, "foreign": f})
    return [check("read/click/wait plan runs (exit 0)", a["exit"] == 0, a["exit"], 0),
            check("posting needs confirmation (exit 1)", b["exit"] == 1, b["exit"], 1),
            check("an explicitly approved post step runs", c["exit"] == 0, c["exit"], 0),
            check("verification codes are handed to the human (exit 4)", d["exit"] == 4, d["exit"], 4),
            check("payment details are blocked (exit 3)", e["exit"] == 3, e["exit"], 3),
            check("negative control: a domain outside the allow-list does not run", f["exit"] != 0, f["exit"], 3)], [out]


_LICENCE_SIGS = [("MIT", r"Permission is hereby granted, free of charge"), ("Apache-2.0", r"Apache License,?\s+Version 2\.0"),
                 ("BSD-3-Clause", r"Neither the name of .* nor the names of its\s+contributors"), ("GPL-3.0", r"GNU GENERAL PUBLIC LICENSE\s+Version 3")]
_REUSE_OK = {"MIT", "Apache-2.0", "BSD-3-Clause"}


@card("MISC-12")
def licence_inventory(task, wd):
    """Inventory inspiration repos by their LICENSE text: an allow-list of reusable sources, GPL kept as a tool only,
    and anything unlicensed is read, never copied; THIRD_PARTY_NOTICES lists what may be reused."""
    texts = {"motion-starter-kit": "MIT License\n\nPermission is hereby granted, free of charge, to any person obtaining a copy",
             "hyperframes": "Apache License\n                           Version 2.0, January 2004",
             "scroll-world": "MIT License\nCopyright (c) 2025\n\nPermission is hereby granted, free of charge, to any person",
             "bsd-tool": "Redistribution and use ... Neither the name of the copyright holder nor the names of its\ncontributors may be used",
             "gpl-lib": "GNU GENERAL PUBLIC LICENSE\n                       Version 3, 29 June 2007",
             "landing-unverified": None}
    root = wd / "repos"
    for name, t in texts.items():
        (root / name).mkdir(parents=True, exist_ok=True)
        (root / name / "index.js").write_text("// code\n", encoding="utf-8")
        if t:
            (root / name / "LICENSE").write_text(t, encoding="utf-8")

    def classify(repo):
        lic = repo / "LICENSE"
        if not lic.exists():
            return {"licence": None, "use": "read-only (unlicensed: do not copy)"}
        t = lic.read_text(encoding="utf-8")
        name = next((n for n, pat in _LICENCE_SIGS if re.search(pat, t, re.S)), "unknown")
        return {"licence": name, "use": "reuse with LICENSE + attribution" if name in _REUSE_OK else "tool only, do not bundle" if name.startswith("GPL") else "read-only"}
    inv = {p.name: classify(p) for p in sorted(root.iterdir())}
    allow = sorted(k for k, v in inv.items() if v["licence"] in _REUSE_OK)
    notices = "\n".join("%s — %s" % (k, inv[k]["licence"]) for k in allow) + "\n"
    (wd / "THIRD_PARTY_NOTICES.md").write_text(notices, encoding="utf-8")
    out = write_json(wd, "licences.json", inv)
    return [check("MIT / Apache-2.0 / BSD-3 detected from their texts", [inv[k]["licence"] for k in ("motion-starter-kit", "hyperframes", "bsd-tool")] == ["MIT", "Apache-2.0", "BSD-3-Clause"]),
            check("allow-list holds only permissive sources", allow == ["bsd-tool", "hyperframes", "motion-starter-kit", "scroll-world"], allow),
            check("GPL kept as a tool, never bundled", inv["gpl-lib"]["use"] == "tool only, do not bundle"),
            check("notices list every reusable source", all(k in notices for k in allow) and "gpl-lib" not in notices),
            check("negative control: the unlicensed repo is not reusable", inv["landing-unverified"]["licence"] is None and "landing-unverified" not in allow)], \
        [out, wd / "THIRD_PARTY_NOTICES.md"]


def tiny_text_pdf(path, text):
    """A minimal valid one-page PDF with a real text layer (Helvetica)."""
    stream = ("BT /F1 18 Tf 50 750 Td (%s) Tj ET" % text).encode()
    objs = [b"<< /Type /Catalog /Pages 2 0 R >>", b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
            b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream", b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]
    out, offs = b"%PDF-1.4\n", []
    for i, o in enumerate(objs, 1):
        offs.append(len(out))
        out += b"%d 0 obj\n" % i + o + b"\nendobj\n"
    x = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1) + b"".join(b"%010d 00000 n \n" % o for o in offs)
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, x)
    Path(path).write_bytes(out)
    return Path(path)


@card("MISC-16")
def pdf_text_layer_then_ocr(task, wd):
    """Check for a text layer first (pdftotext bytes per page), then add an invisible OCR layer to the image-only PDF
    with tesseract ara+eng (its PDF renderer), and confirm the text is now extractable."""
    from PIL import Image
    textpdf = tiny_text_pdf(wd / "born_digital.pdf", "Quarterly report 2026")
    img = render_ar_lines(wd / "scan.png", ["ارتفعت المبيعات في شهر مارس"], size=56)
    Image.open(img).convert("RGB").save(wd / "scanned.pdf", resolution=150)

    def layer(pdf):
        out = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True, timeout=30).stdout
        pages = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout).group(1))
        return len(out.strip().encode()) / pages, out
    b_text, t_text = layer(textpdf)
    b_scan, _ = layer(wd / "scanned.pdf")
    fx.run(["pdftoppm", "-r", "150", "-png", "-singlefile", str(wd / "scanned.pdf"), str(wd / "page")])
    env = dict(os.environ, OMP_THREAD_LIMIT="1")
    subprocess.run(["tesseract", str(wd / "page.png"), str(wd / "ocr_layer"), "-l", "ara+eng", "--psm", "6", "pdf"], capture_output=True, timeout=60,
                   env=env, stdin=subprocess.DEVNULL)
    b_ocr, t_ocr = layer(wd / "ocr_layer.pdf")
    t_ocr = "".join(ch for ch in t_ocr if ch not in _BIDI)
    hits = sum(w in t_ocr for w in "ارتفعت المبيعات في شهر مارس".split())
    out = write_json(wd, "pdf-check.json", {"born_digital_bytes_per_page": b_text, "scanned_bytes_per_page": b_scan, "after_ocr_bytes": b_ocr, "ocr_text": t_ocr.strip()})
    return [check("born-digital PDF has a text layer", "Quarterly report 2026" in t_text and b_text > 15, b_text),
            check("scanned PDF: almost no bytes of text per page -> image-only", b_scan < 5, b_scan, "<5"),
            check("after the invisible OCR layer the Arabic words are extractable", hits >= 4, hits, ">=4 of 5"),
            check("the OCR PDF keeps the page image (not a text-only rewrite)", (wd / "ocr_layer.pdf").stat().st_size > 5000, (wd / "ocr_layer.pdf").stat().st_size),
            check("negative control: the untreated scan has no extractable text", b_scan < 5 and b_scan < b_ocr)], [wd / "ocr_layer.pdf", out]


_MISC18 = {"night_boat": (1920, 1080, 30, 5.0), "lab_rabbit_lion": (960, 540, 24, 20.0), "bunny_twin": (1080, 1920, 30, 5.0), "midnight_cat": (1280, 720, 24, 12.0)}


@card("MISC-18")
def composition_sources(task, wd):
    """The ready composition sources: copy one into a work home and `sync` its assets the way kmotion does
    (motion.sync_assets), then read every listed project's declared canvas, fps and duration."""
    names = ["night_boat", "blue_hour", "koi_pond", "lab_rabbit_lion", "bunny_twin", "midnight_cat", "sound_ground", "water_cycle_3d", "showreel", "premium_edit"]
    present = {n: (MM / "projects" / n / "index.html").exists() for n in names}
    specs = {}
    for n in names:
        if present[n]:
            h = (MM / "projects" / n / "index.html").read_text(encoding="utf-8", errors="replace")
            g = lambda k: (re.search(r'data-%s="([\d.]+)"' % k, h) or [None, None])[1]
            specs[n] = [g("width"), g("height"), g("fps"), g("duration")]
    home = wd / "home"
    dst = home / "projects/night_boat"
    shutil.copytree(MM / "projects/night_boat", dst, ignore=shutil.ignore_patterns("assets"))
    before = (dst / "assets").exists()
    env = dict(os.environ, KOSIF_MOTION_HOME=str(home))
    r = subprocess.run([sys.executable, "-c", "import sys;sys.path.insert(0,%r);import motion;from pathlib import Path;motion.sync_assets(Path(%r))" % (str(MM), str(dst))],
                       capture_output=True, text=True, timeout=60, env=env, cwd=str(wd), stdin=subprocess.DEVNULL)
    synced = sorted(p.name for p in (dst / "assets").glob("*")) if (dst / "assets").exists() else []
    same = all(sha(dst / "assets" / f) == sha(KIT / f) for f in synced if (KIT / f).exists() and (KIT / f).is_file())
    out = write_json(wd, "sources.json", {"present": present, "specs": specs, "synced_assets": synced})
    ok_specs = all([float(x) for x in specs[n]] == [float(v) for v in want] for n, want in _MISC18.items())
    return [check("all ten listed projects are present", all(present.values()), present),
            check("declared canvas / fps / duration match the card", ok_specs, {n: specs[n] for n in _MISC18}),
            check("sync copied the kit assets into the remix copy", r.returncode == 0 and "three-kit.bundle.js" in synced, [r.returncode, synced[:6], r.stderr[-200:]]),
            check("synced assets are byte-identical to the kit", same and len(synced) >= 3),
            check("negative control: the copy had no assets before the sync", not before, before, False)], [out]


# ═════════════════════════════════════════════ ui-product-device ═════════════════════════════════════════════
@card("UI-56")
def device_mockup_2x(task, wd):
    """Place an image inside a device frame with CSS shadows and capture with Playwright at deviceScaleFactor 2."""
    np = _np()
    shot = np.zeros((300, 140, 3)) + rgb("#2f5bff")
    shot[20:60, 20:120] = rgb("#ffffff")
    save_png(shot, wd / "screen.png")
    html = ("<!doctype html><body style='margin:0;background:#eef1f6;width:400px;height:420px'><div id=dev style='position:absolute;left:120px;top:40px;"
            "width:160px;height:330px;border-radius:26px;background:#0b0d12;box-shadow:0 30px 40px rgba(0,0,0,.35)'><img id=scr src='screen.png' "
            "style='position:absolute;left:10px;top:15px;width:140px;height:300px;border-radius:16px'></div></body>")
    (wd / "mock.html").write_text(html, encoding="utf-8")
    js = pw_script("""for (const dpr of [2, 1]) { const ctx = await browser.newContext({viewport: {width: 400, height: 420}, deviceScaleFactor: dpr});
const p = await ctx.newPage(); await p.goto(%s); await p.waitForLoadState('load'); await p.screenshot({path: %s + '/mock_' + dpr + 'x.png'}); await ctx.close(); }
console.log(JSON.stringify({ok: 1}));""" % (json.dumps((wd / "mock.html").as_uri()), json.dumps(str(wd))))
    node_json(wd, "capture", js)
    a, b = load_png(wd / "mock_2x.png"), load_png(wd / "mock_1x.png")
    inside = a[2 * 95, 2 * 200]                          # inside the white bar of the screen image
    under = a[2 * 385, 2 * 200].mean()                   # the drop shadow below the device
    bg = a[2 * 410, 2 * 20].mean()
    return [check("captured at 2x DPR (800 x 840)", a.shape[:2] == (840, 800), a.shape[:2], (840, 800)),
            check("screen image placed inside the frame", np.abs(inside - 255).max() < 6 and np.abs(a[2 * 300, 2 * 200] - rgb("#2f5bff")).max() < 8, inside),
            check("device body dark at its bezel", a[2 * 48, 2 * 200].mean() < 30, a[2 * 48, 2 * 200].mean()),
            check("CSS shadow darkens the ground below the device", under < bg - 15, [under, bg]),
            check("negative control: a 1x capture has half the pixels per side", b.shape[:2] == (420, 400), b.shape[:2])], [wd / "mock_2x.png"]


_STEPS_PAGE = """<!doctype html><meta charset=utf-8><body style="margin:0;height:2000px;font:16px DejaVu Sans">
<button id=go style="position:absolute;left:40px;top:40px;width:120px;height:40px">Render</button><span id=count style="position:absolute;left:180px;top:50px">0</span>
<input id=name style="position:absolute;left:40px;top:120px;width:200px;font-size:16px">
<div id=card style="position:absolute;left:40px;top:200px;width:80px;height:60px;background:#7ee8d2"></div><div id=ready style="display:none"></div>
<div id=cursor style="position:fixed;left:0;top:0;width:18px;height:18px;border-radius:9px;background:#e8333f;pointer-events:none;z-index:9"></div>
<script>let n=0;go.onclick=()=>count.textContent=++n;let drag=null;card.onmousedown=e=>drag=[e.clientX-card.offsetLeft,e.clientY-card.offsetTop];
onmousemove=e=>{cursor.style.left=(e.clientX-9)+'px';cursor.style.top=(e.clientY-9)+'px';if(drag){card.style.left=(e.clientX-drag[0])+'px';card.style.top=(e.clientY-drag[1])+'px'}};
onmouseup=()=>drag=null;setTimeout(()=>ready.id='ready-ok',200)</script>"""


@card("UI-72")
def json_steps_drive_page(task, wd):
    """A JSON steps file drives a real page through Playwright: waitFor, click with a gliding cursor (450 ms), drag,
    type (70 ms/key), wheel scroll over time, and a caption per step written to captions.vtt."""
    (wd / "app.html").write_text(_STEPS_PAGE, encoding="utf-8")
    steps = [{"do": "waitFor", "sel": "#ready-ok", "caption": "الصفحة جاهزة"}, {"do": "click", "sel": "#go", "caption": "نضغط زر الرندر"},
             {"do": "type", "sel": "#name", "text": "KOSIF", "caption": "نكتب الاسم"}, {"do": "drag", "sel": "#card", "to": [300, 240], "caption": "نسحب البطاقة"},
             {"do": "wheel", "dy": 600, "ms": 600, "caption": "ننزل في الصفحة"}]
    write_json(wd, "steps.json", steps)
    js = pw_script("""const steps = JSON.parse(require('fs').readFileSync(%s, 'utf8'));
const ctx = await browser.newContext({viewport: {width: 640, height: 400}}); const p = await ctx.newPage(); await p.goto(%s);
let cur = [10, 10]; const t0 = Date.now(); const cues = []; const mid = [];
const glide = async (x, y) => { const n = 15; for (let i = 1; i <= n; i++) { const k = i / n, e = k * k * (3 - 2 * k);
  await p.mouse.move(cur[0] + (x - cur[0]) * e, cur[1] + (y - cur[1]) * e); if (i === 7) mid.push(await p.evaluate(() => [cursor.offsetLeft + 9, cursor.offsetTop + 9]));
  await p.waitForTimeout(30); } cur = [x, y]; };
for (const s of steps) { const a = (Date.now() - t0) / 1000;
  if (s.do === 'waitFor') await p.waitForSelector(s.sel, {state: 'attached', timeout: 20000});
  if (s.do === 'click') { const b = await p.locator(s.sel).boundingBox(); await glide(b.x + b.width / 2, b.y + b.height / 2); await p.mouse.down(); await p.mouse.up(); }
  if (s.do === 'type') { await p.click(s.sel); await p.keyboard.type(s.text, {delay: 70}); }
  if (s.do === 'drag') { const b = await p.locator(s.sel).boundingBox(); await glide(b.x + 10, b.y + 10); await p.mouse.down(); await glide(s.to[0], s.to[1]); await p.mouse.up(); }
  if (s.do === 'wheel') { const k = 6; for (let i = 0; i < k; i++) { await p.mouse.wheel(0, s.dy / k); await p.waitForTimeout(s.ms / k); } }
  const b = (Date.now() - t0) / 1000; cues.push([a, Math.max(b, a + 3), s.caption]); }
const st = await p.evaluate(() => ({count: count.textContent, name: document.getElementById('name').value, card: [card.offsetLeft, card.offsetTop], y: scrollY}));
await ctx.close(); console.log(JSON.stringify({st, cues, mid}));""" % (json.dumps(str(wd / "steps.json")), json.dumps((wd / "app.html").as_uri())))
    o, _ = node_json(wd, "drive", js)
    fmt = lambda t: "%02d:%02d:%06.3f" % (int(t // 3600), int(t % 3600 // 60), t % 60)
    vtt = "WEBVTT\n\n" + "\n".join("%d\n%s --> %s\n%s\n" % (i + 1, fmt(a), fmt(b), c) for i, (a, b, c) in enumerate(o["cues"]))
    (wd / "captions.vtt").write_text(vtt, encoding="utf-8")
    st = o["st"]
    starts = [c[0] for c in o["cues"]]
    return [check("click registered on the button", st["count"] == "1", st["count"], "1"),
            check("text typed into the field", st["name"] == "KOSIF", st["name"]),
            check("card dragged to ~(290, 230) (grab offset 10 px)", abs(st["card"][0] - 290) <= 2 and abs(st["card"][1] - 230) <= 2, st["card"], [290, 230]),
            check("wheel scrolled the page 600 px", st["y"] == 600, st["y"], 600),
            check("cursor glides (mid-glide position strictly between start and target)", all(0 < m[0] < 640 for m in o["mid"]) and len(o["mid"]) == 3, o["mid"]),
            check("one caption per step, in time order, each >= 3 s", len(o["cues"]) == 5 and starts == sorted(starts) and all(b - a >= 3 - 1e-6 for a, b, _ in o["cues"])),
            check("negative control: the untouched page state differs", (st["count"], st["name"], st["y"]) != ("0", "", 0))], [wd / "captions.vtt"]


_SITE = """<!doctype html><html lang=en><head><meta charset=utf-8><title>KOSIF Studio</title><meta name=description content="Arabic-first motion graphics">
<style>body{margin:0;background:#0b1020;color:#f3f7ff;font-family:'DejaVu Sans',sans-serif}h1{color:#e7b65a;font-size:48px}a.cta{background:#2f5bff;color:#fff;padding:12px}</style></head>
<body><h1>Motion that means something</h1><p>Kinetic Arabic type, beat-synced montage and one-click export.</p><a class=cta href="#">Start free</a>
<img src="hero.png" width=200 height=120><div style="height:900px"></div><h2>Pricing</h2></body></html>"""


@card("UI-73")
def site_capture_tokens(task, wd):
    """A headless crawl of a site yields screenshots, brand tokens (colours, fonts), text and assets; a failed capture
    is a hard stop (BLOCKED.md), never an invented page. (`hyperframes capture` itself is answered 403 from this
    sandbox, so the same capture runs on Playwright + Chrome against a local site.)"""
    site = wd / "site"
    site.mkdir(exist_ok=True)
    (site / "index.html").write_text(_SITE, encoding="utf-8")
    np = _np()
    save_png(np.zeros((120, 200, 3)) + rgb("#e7b65a"), site / "hero.png")
    srv, base = serve_dir(site)
    cap = wd / "capture"

    def capture(url):
        js = pw_script("""const fs = require('fs'); const out = %s; fs.mkdirSync(out + '/screenshots', {recursive: true});
const ctx = await browser.newContext({viewport: {width: 1000, height: 600}}); const p = await ctx.newPage();
const r = await p.goto(%s, {timeout: 8000}).catch(e => null);
if (!r || r.status() >= 400) { fs.writeFileSync(out + '/BLOCKED.md', 'capture failed: ' + (r ? r.status() : 'no response')); console.log(JSON.stringify({ok: false})); }
else { const tokens = await p.evaluate(() => { const cs = new Set(), fonts = new Set(); for (const e of document.querySelectorAll('body, body *')) { const s = getComputedStyle(e);
  cs.add(s.color); if (s.backgroundColor !== 'rgba(0, 0, 0, 0)') cs.add(s.backgroundColor); fonts.add(s.fontFamily); }
  return {title: document.title, description: document.querySelector('meta[name=description]').content, colors: [...cs], fonts: [...fonts],
          text: document.body.innerText, assets: [...document.images].map(i => i.src), headings: [...document.querySelectorAll('h1,h2')].map(h => h.textContent)}; });
  let i = 0; for (const y of [0, 600]) { await p.evaluate(y => scrollTo(0, y), y); await p.screenshot({path: out + '/screenshots/' + (i++) + '.png'}); }
  fs.writeFileSync(out + '/tokens.json', JSON.stringify(tokens, null, 1)); console.log(JSON.stringify({ok: true, tokens})); }
await ctx.close();""" % (json.dumps(str(cap)), json.dumps(url)))
        return node_json(wd, "capture", js)[0]
    try:
        good = capture(base + "/index.html")
        blocked_dir = cap / "BLOCKED.md"
        bad = capture(base + "/missing.html")
    finally:
        srv.shutdown()
    t = good["tokens"]
    shots = sorted((cap / "screenshots").glob("*.png"))
    return [check("capture ok with title, description and headings from the page", good["ok"] and t["title"] == "KOSIF Studio" and t["headings"] == ["Motion that means something", "Pricing"]),
            check("brand colours read from computed styles", {"rgb(231, 182, 90)", "rgb(11, 16, 32)", "rgb(47, 91, 255)"} <= set(t["colors"]), t["colors"][:6]),
            check("font family recorded", any("DejaVu Sans" in f for f in t["fonts"]), t["fonts"]),
            check("assets listed and 2 screenshots written", t["assets"][0].endswith("/hero.png") and len(shots) == 2),
            check("negative control: a failing URL stops with BLOCKED.md, no tokens invented", bad["ok"] is False and blocked_dir.exists(), bad)], [cap / "tokens.json", shots[0]]


@card("UI-74")
def launch_film_plan_deliver(task, wd):
    """kmotion brag: `init` reads a product folder into material + a plan (hook -> reveal -> highlights -> outro);
    `deliver` bakes the strongest settled frame as the poster at frame 0, runs the gate and checks the share copy."""
    sys.path.insert(0, str(MM))
    launch = load_py(MM / "launch.py", "launch")
    prod = wd / "product"
    prod.mkdir()
    (prod / "index.html").write_text("<!doctype html><html><head><title>KOSIF Studio</title><meta name=description content='Arabic-first motion graphics in minutes'>"
                                     "<style>:root{--brand:#e7b65a;--bg:#0b1020}body{font-family:Cairo}</style></head><body><h1>Motion that means something</h1>"
                                     "<h2>Kinetic Arabic type</h2><h2>Beat-synced montage</h2><h2>One-click export</h2><a class=cta href='/start'>Start free</a></body></html>", encoding="utf-8")
    env = dict(os.environ, KOSIF_MOTION_HOME=str(wd / "home"))
    run = lambda *a: subprocess.run([sys.executable, str(MM / "launch.py"), *map(str, a)], capture_output=True, text=True, timeout=60, cwd=str(wd), env=env,
                                    stdin=subprocess.DEVNULL)
    r = run("init", prod, "--format", "vertical", "--duration", "20", "--out", wd / "brag")
    if r.returncode:
        raise RuntimeError("brag init failed: " + r.stderr[-300:])
    m = json.loads((wd / "brag/material.json").read_text(encoding="utf-8"))
    plan = (wd / "brag/brag-plan.md").read_text(encoding="utf-8")
    film = wd / "film.mp4"
    fx.ffmpeg("-f", "lavfi", "-i", "testsrc2=s=216x384:r=30:d=3", "-f", "lavfi", "-i", "sine=f=440:d=3", "-c:v", "libx264", "-preset", "ultrafast",
              "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(film))
    (wd / "brag/share-copy.txt").write_text("KOSIF Studio turns a script into Arabic motion in minutes. Try it free.", encoding="utf-8")
    d = run("deliver", wd / "brag", "--film", film)
    if d.returncode not in (0, 1):
        raise RuntimeError("brag deliver failed: " + d.stderr[-300:])
    rep = json.loads(d.stdout[d.stdout.index("{"):])
    np = _np()
    f0 = read_video(wd / "brag/brag.mp4")[0]
    poster = load_png(wd / "brag/brag.jpg")
    orig0 = read_video(film)[0]
    bad_copy = launch.check_copy("One. Two. Three. Four. Five sentences here.")
    return [check("material: title, palette and the four headings from the product's own page",
                  m["title"] == "KOSIF Studio" and m["palette"] == {"brand": "#e7b65a", "bg": "#0b1020"} and len(m["headings"]) == 4, [m["title"], m["palette"]]),
            check("plan is vertical 1080x1920 with the hook -> reveal -> highlights -> outro shape", "1080×1920" in plan and "Hook" in plan and "Reveal" in plan and "outro" in plan),
            check("poster baked as frame 0", float(np.abs(f0 - poster).mean()) < 6 and rep["baked"]["frames"] == 90, [float(np.abs(f0 - poster).mean()), rep["baked"]]),
            check("share copy passes (1-3 sentences, <= 280 chars)", rep["share_copy_issues"] == [], rep["share_copy_issues"]),
            check("the gate measured loudness and reports it", rep["lufs"] is not None and isinstance(rep["gate_issues"], list), [rep["lufs"], rep["gate_issues"]]),
            check("negative control: the original frame 0 is not the poster, and a 5-sentence copy fails",
                  float(np.abs(orig0 - poster).mean()) > 6 and any("sentences" in x for x in bad_copy), [float(np.abs(orig0 - poster).mean()), bad_copy])], \
        [wd / "brag/brag.mp4", wd / "brag/brag-plan.md"]


@card("UI-77")
def record_tab_contact_sheet(task, wd):
    """Record the active page to WebM (Playwright's recorder, since agent-browser is not installed) with an animated
    pointer, transcode to MP4 at 30 fps and build an automatic contact sheet."""
    (wd / "app.html").write_text(_STEPS_PAGE, encoding="utf-8")
    js = pw_script("""const ctx = await browser.newContext({viewport: {width: 640, height: 400}, recordVideo: {dir: %s, size: {width: 640, height: 400}}});
const p = await ctx.newPage(); await p.goto(%s); await p.waitForSelector('#ready-ok', {state: 'attached'});
for (let i = 0; i <= 40; i++) { await p.mouse.move(20 + i * 14, 60 + i * 6); await p.waitForTimeout(40); }
const v = p.video(); await ctx.close(); console.log(JSON.stringify({path: await v.path()}));""" % (json.dumps(str(wd / "rec")), json.dumps((wd / "app.html").as_uri())))
    o, _ = node_json(wd, "record", js)
    webm = Path(o["path"])
    shutil.move(str(webm), str(wd / "demo.webm"))
    fx.ffmpeg("-i", str(wd / "demo.webm"), "-vf", "fps=30,scale=320:200", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", str(wd / "demo.mp4"))
    fx.ffmpeg("-i", str(wd / "demo.mp4"), "-vf", "select='not(mod(n\\,10))',scale=160:100,tile=3x2", "-frames:v", "1", str(wd / "contact.png"))
    np = _np()
    fr = read_video(wd / "demo.mp4")
    red = [np.argwhere(np.abs(f - rgb("#e8333f")).max(axis=-1) < 40) for f in fr]
    xs = [2 * float(r[:, 1].mean()) for r in red if len(r) > 5]
    v = [s for s in fx.probe(wd / "demo.mp4")["streams"] if s["codec_type"] == "video"][0]
    sheet = load_png(wd / "contact.png")
    still = wd / "still.mp4"
    fx.ffmpeg("-i", str(wd / "demo.mp4"), "-vf", "select=eq(n\\,0),loop=60:1:0,setpts=N/30/TB", "-frames:v", "60", "-c:v", "libx264", "-preset", "ultrafast",
              "-pix_fmt", "yuv420p", str(still))
    fx.ffmpeg("-i", str(still), "-vf", "select='not(mod(n\\,10))',scale=160:100,tile=3x2", "-frames:v", "1", str(wd / "contact_still.png"))
    still_sheet = load_png(wd / "contact_still.png")

    def tile_marks(sh):
        out = []
        for i in range(6):
            t = sh[(i // 3) * 100:(i // 3 + 1) * 100, (i % 3) * 160:(i % 3 + 1) * 160]
            pts = np.argwhere(np.abs(t - rgb("#e8333f")).max(axis=-1) < 60)
            out.append(tuple(np.round(pts.mean(axis=0)).astype(int)) if len(pts) else None)
        return out
    marks, still_marks = tile_marks(sheet), tile_marks(still_sheet)
    moving = len({m for m in marks if m}) >= 3
    return [check("WebM recorded and transcoded to 30 fps MP4", (wd / "demo.webm").stat().st_size > 2000 and v["r_frame_rate"] == "30/1", v["r_frame_rate"]),
            check("recording lasts >= 1.5 s", float(fx.probe(wd / "demo.mp4")["format"]["duration"]) >= 1.5),
            check("the pointer moves left to right across the recording", len(xs) > 10 and xs[-1] - xs[0] > 200, [xs[0] if xs else None, xs[-1] if xs else None]),
            check("contact sheet 3x2 tiles of 160 px", sheet.shape[:2] == (200, 480), sheet.shape),
            check("contact-sheet tiles show the pointer at >= 3 different places", moving, [str(m) for m in marks]),
            check("negative control: a sheet from a frozen (unanimated) recording shows one pointer place",
                  len({m for m in still_marks if m}) <= 1, [str(m) for m in still_marks])], \
        [wd / "demo.mp4", wd / "contact.png"]


@card("UI-82")
def launch_kinetic_type(task, wd):
    """Launch-promo kinetic type: a neon prompt box types at ~18 chars/s with a 3 px purple caret while the parent
    scales 2.5 -> 1 from the first character (camera pull-back synced to typing); modes big -> prompt -> orb -> capsule -> end."""
    text = "Make a launch film for KOSIF"
    body = ("<div id=stage style='width:960px;height:540px;background:#05050A;position:relative;overflow:hidden;font-family:DejaVu Sans'>"
            "<div id=box style='position:absolute;left:180px;top:230px;width:600px;height:80px;border:2px solid #A88BFF;border-radius:16px;color:#F5F3FF;font-size:28px;"
            "box-shadow:0 0 30px #6C3BFF;transform-origin:50% 50%'><span id=t></span><i id=caret style='display:inline-block;width:3px;height:30px;background:#A88BFF'></i></div></div>")
    js = """const T=%s,cps=18,dur=T.length/cps;const st={n:0};const tl=gsap.timeline({paused:true});
tl.addLabel('big',0).addLabel('prompt',1).to(st,{n:T.length,duration:dur,ease:'none',onUpdate:()=>{document.getElementById('t').textContent=T.slice(0,Math.floor(st.n))}},'prompt')
 .fromTo('#box',{scale:2.5},{scale:1,duration:dur,ease:'power2.out'},'prompt').addLabel('orb','+=0.4').addLabel('capsule','+=1').addLabel('end','+=1');
const at=t=>{tl.seek(t,false);const c=getComputedStyle(document.getElementById('caret'));return {chars:document.getElementById('t').textContent.length,scale:+gsap.getProperty('#box','scale').toFixed(3),cw:c.width,cc:c.backgroundColor}};
return {dur,labels:Object.entries(tl.labels).sort((a,b)=>a[1]-b[1]).map(x=>x[0]),s:[at(0.5),at(1+0.5),at(1+1.02),at(1+dur)]};""" % json.dumps(text)
    o, page, _ = chrome_page(wd, "promo", html_doc(body, js, [GSAP]), (960, 540))
    s = o["s"]
    out = write_json(wd, "promo.json", o)
    return [check("typing at 18 chars/s: 9 chars at 0.5 s into the prompt, 18 at ~1 s", s[1]["chars"] == 9 and s[2]["chars"] == 18, [s[1]["chars"], s[2]["chars"]]),
            check("pull-back from scale 2.5 to 1 across the typing", s[0]["scale"] == 2.5 and s[3]["scale"] == 1 and 1 < s[2]["scale"] < 2.5, [x["scale"] for x in s]),
            check("caret is 3 px and purple #A88BFF", s[1]["cw"] == "3px" and s[1]["cc"] == "rgb(168, 139, 255)", [s[1]["cw"], s[1]["cc"]]),
            check("modes cycle big -> prompt -> orb -> capsule -> end", o["labels"] == ["big", "prompt", "orb", "capsule", "end"], o["labels"]),
            check("negative control: before the prompt mode nothing is typed and the box is still zoomed", s[0]["chars"] == 0 and s[0]["scale"] == 2.5)], [out, page]


@card("UI-87")
def offline_player_page(task, wd):
    """The film ships as an offline web page (build.cjs): play/pause, restart, a 0.01 s range slider, an MP4 download
    link, reduced-motion support, render(t) clamped, rAF advancing by min(dt, 0.1); validated with its own
    player-test.cjs and test.cjs, plus a Chrome check of the page."""
    src = MM / "projects/midnight_cat"
    dst = wd / "midnight_cat"
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("svg", "frames", "*.mp4"))
    (dst / "svg").mkdir(exist_ok=True)
    env = {"PATH": str(Path(NODE).parent) + ":/usr/bin:/bin", "HOME": str(wd)}
    b = subprocess.run([NODE, "build.cjs"], cwd=str(dst), capture_output=True, text=True, timeout=60, env=env)
    t = subprocess.run([NODE, "test.cjs"], cwd=str(dst), capture_output=True, text=True, timeout=60, env=env)
    p = subprocess.run([NODE, "player-test.cjs"], cwd=str(dst), capture_output=True, text=True, timeout=60, env=env)
    h = (dst / "midnight-cat.original.html").read_text(encoding="utf-8")
    js = "const a=document.getElementById('time');window.render(6.25);const f1=document.getElementById('stage').innerHTML.length;window.render(99);" \
         "return {step:a.step,max:a.max,clamped:+a.value,dl:!!document.querySelector('a[download]'),f1,dur:window.__duration};"
    probe = h.replace("</body>", "<pre id=\"OUT\" style=\"display:none\"></pre><script>window.addEventListener('load',()=>{try{document.getElementById('OUT').textContent="
                      "JSON.stringify((()=>{%s})())}catch(e){document.getElementById('OUT').textContent=JSON.stringify({__error:String(e)})}})</script></body>" % js, 1)
    o, page, _ = chrome_page(wd, "player_probe", probe, (1280, 900))
    bare = dst.parent / "bare"
    shutil.copytree(dst, bare)
    (bare / "midnight-cat.original.html").write_text(re.sub(r"<script>[\s\S]*?</script>", "", h), encoding="utf-8")
    neg = subprocess.run([NODE, "player-test.cjs"], cwd=str(bare), capture_output=True, text=True, timeout=60, env=env)
    svgs = len(list((dst / "svg").glob("*.svg")))
    return [check("build.cjs rebuilt the self-contained page and 288 frames (12 s x 24 fps)", b.returncode == 0 and svgs == 288, [b.returncode, svgs], 288),
            check("player-test.cjs PASS (init, reduced motion, seek, deterministic frame, play/pause, restart, stop, bounds)",
                  p.returncode == 0 and p.stdout.startswith("PASS"), p.stdout.strip()[:120]),
            check("test.cjs passes", t.returncode == 0, (t.stdout + t.stderr).strip()[-120:]),
            check("in Chrome: 0.01 s slider, 12 s max, render(99) clamps to 12, download link present",
                  o["step"] in ("0.01", ".01") and o["max"] == "12" and o["clamped"] == 12 and o["dl"] and o["dur"] == 12, o),
            check("theme tokens #060d17 / #ffb769 / #71e5d2 in the page", all(c in h for c in ("#060d17", "#ffb769", "#71e5d2"))),
            check("negative control: the page without its player script fails player-test", neg.returncode != 0, neg.returncode, "!= 0")], \
        [dst / "midnight-cat.original.html"]


# ═════════════════════════════════════════════ web-research ═════════════════════════════════════════════
@card("WEB-04")
def proxy_ca_requests(task, wd):
    """httpx with a User-Agent, timeout and redirects, reading SSL_CERT_FILE / proxy settings from the environment —
    against a local HTTPS server whose CA bundle is supplied, never with TLS verification disabled."""
    import ssl
    fx.run(["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes", "-keyout", str(wd / "key.pem"), "-out", str(wd / "cert.pem"), "-days", "2",
            "-subj", "/CN=127.0.0.1", "-addext", "subjectAltName=IP:127.0.0.1"])
    seen = {}

    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_GET(self):
            seen.setdefault("ua", self.headers.get("User-Agent"))
            if self.path == "/old":
                self.send_response(301)
                self.send_header("Location", "/new")
                self.end_headers()
                return
            body = "مرحبا من الخادم".encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
    srv = ThreadingHTTPServer(("127.0.0.1", 0), H)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(wd / "cert.pem", wd / "key.pem")
    srv.socket = ctx.wrap_socket(srv.socket, server_side=True)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    url = "https://127.0.0.1:%d/old" % srv.server_address[1]
    code = ("import httpx,json,sys\ntry:\n r=httpx.get(sys.argv[1],headers={'User-Agent':'kosif-research/1.0 (+https://example.org/contact)'},timeout=30,follow_redirects=True)\n"
            " print(json.dumps({'status':r.status_code,'final':str(r.url),'text':r.text,'hops':len(r.history)}))\nexcept Exception as e:\n print(json.dumps({'error':type(e).__name__+': '+str(e)[:120]}))\n")
    (wd / "fetch.py").write_text(code, encoding="utf-8")
    base_env = {k: v for k, v in os.environ.items() if k not in ("SSL_CERT_FILE", "REQUESTS_CA_BUNDLE")}
    base_env["NO_PROXY"] = "127.0.0.1"
    try:
        ok = subprocess.run([sys.executable, "-I", str(wd / "fetch.py"), url], capture_output=True, text=True, timeout=40,
                            env=dict(base_env, SSL_CERT_FILE=str(wd / "cert.pem")))
        no_ca = subprocess.run([sys.executable, "-I", str(wd / "fetch.py"), url], capture_output=True, text=True, timeout=40, env=base_env)
    finally:
        srv.shutdown()
    a, b = json.loads(ok.stdout), json.loads(no_ca.stdout)
    out = write_json(wd, "fetch.json", {"with_ca_bundle": a, "without": b, "server_saw_ua": seen.get("ua")})
    src = (wd / "fetch.py").read_text()
    return [check("HTTPS 200 through the supplied CA bundle (SSL_CERT_FILE from the env)", a.get("status") == 200 and a.get("text") == "مرحبا من الخادم", a),
            check("redirect followed /old -> /new", a.get("final", "").endswith("/new") and a.get("hops") == 1, a.get("final")),
            check("the server saw the identifying User-Agent", seen.get("ua", "").startswith("kosif-research/1.0"), seen.get("ua")),
            check("verification is never disabled in the request code", "verify=False" not in src and "verify" not in src),
            check("negative control: without the CA bundle the TLS check refuses the server", "error" in b and "SSL" in b["error"] or "CERTIFICATE" in b.get("error", "").upper(), b)], [out]


_ARTICLE = """<!doctype html><html lang=ar dir=rtl><head><meta charset=utf-8><title>مهرجان الحركة العربية 2026</title>
<meta name=author content="فريق كوزيف"><meta property="article:published_time" content="2026-10-20"></head><body>
<nav><a href=/>الرئيسية</a> | <a href=/news>الأخبار</a> | <a href=/ads>أعلن معنا</a></nav><div class=ad>إعلان: خصم خمسين بالمئة على الاشتراك</div>
<article><h1>مهرجان الحركة العربية 2026</h1>
<p>انطلقت اليوم في القاهرة فعاليات مهرجان الحركة العربية، بمشاركة أكثر من مئتي مصمم من اثنتي عشرة دولة، وقدّم المشاركون أفلامًا قصيرة تعتمد على الخط العربي المتحرك والموسيقى الحية.</p>
<p>وقالت لجنة التحكيم إن الأعمال هذا العام ركزت على قراءة النص قبل الحركة، وعلى احترام اتجاه الكتابة من اليمين إلى اليسار، مع استخدام أدوات مفتوحة المصدر في الإنتاج.</p>
<p>ويستمر المهرجان أسبوعًا كاملًا، وتُعرض الأفلام الفائزة في ختامه مع ورش عمل مجانية للطلاب حول التحريك والتلوين والتصدير للمنصات.</p></article>
<footer>جميع الحقوق محفوظة — سياسة الخصوصية — اتصل بنا</footer></body></html>"""


@card("WEB-05")
def article_to_markdown(task, wd):
    """trafilatura strips menus and ads and keeps the article as Markdown; the title comes from BeautifulSoup(lxml);
    front matter records the source URL and UTC fetch time; pandoc converts it to .docx keeping the source line."""
    import trafilatura
    from bs4 import BeautifulSoup
    url = "https://news.example/arab-motion-2026"
    md = trafilatura.extract(_ARTICLE, output_format="markdown", include_links=False, url=url)
    title = BeautifulSoup(_ARTICLE, "lxml").title.get_text(strip=True)
    fetched = "2026-11-04T00:00:00Z"
    doc = "---\ntitle: %s\nsource: %s\nfetched: %s\n---\n\n%s\n\nSource: %s\n" % (title, url, fetched, md, url)
    (wd / "article.md").write_text(doc, encoding="utf-8")
    fx.run(["pandoc", str(wd / "article.md"), "-o", str(wd / "article.docx")], timeout=60)
    with zipfile.ZipFile(wd / "article.docx") as z:
        xml = z.read("word/document.xml").decode("utf-8")
    words = len(re.findall(r"[\u0600-\u06ff]+", md or ""))
    raw = BeautifulSoup(_ARTICLE, "lxml").get_text(" ")
    return [check("article body kept (all three paragraphs)", md and "مئتي مصمم" in md and "ورش عمل مجانية" in md and "اليمين إلى اليسار" in md),
            check("menus, ad and footer dropped", not any(x in md for x in ("أعلن معنا", "خصم خمسين", "سياسة الخصوصية")), md[:80]),
            check("title from <title> and front matter with source + UTC time", title == "مهرجان الحركة العربية 2026" and doc.startswith("---\ntitle:") and "source: " + url in doc),
            check("docx written and keeps the source line", url in xml and (wd / "article.docx").stat().st_size > 3000),
            check("Arabic word count of the kept article", words >= 60, words, ">=60"),
            check("negative control: the raw page text still carries the ad and the footer", "خصم خمسين" in raw and "سياسة الخصوصية" in raw)], [wd / "article.md", wd / "article.docx"]


@card("WEB-15")
def check_versions_before_coding(task, wd):
    """Before writing code against a library, read its installed version and API locally (pip metadata, the module's
    __version__, the npm package.json, `<tool> -version`) and adapt to breaking changes."""
    import importlib.metadata as md
    import numpy
    np_meta, np_mod = md.version("numpy"), numpy.__version__
    pip_show = subprocess.run([sys.executable, "-m", "pip", "show", "numpy"], capture_output=True, text=True, timeout=60).stdout
    pip_ver = (re.search(r"^Version:\s*(\S+)", pip_show, re.M) or [None, None])[1]
    gsap_pkg = json.loads((NODE_MODULES / "gsap/package.json").read_text())["version"]
    gsap_js = node_json(wd, "gsapver", "const {gsap}=require('gsap');console.log(JSON.stringify(gsap.version))")[0]
    ffv = fx.run(["ffmpeg", "-hide_banner", "-version"]).stdout.splitlines()[0]
    major = int(np_mod.split(".")[0])
    integ = "numpy.trapezoid" if hasattr(numpy, "trapezoid") else "numpy.trapz"
    api = {"numpy_major": major, "integrate_with": integ, "trapz_present": hasattr(numpy, "trapz")}
    stale = {"numpy": "1.26.4"}
    out = write_json(wd, "versions.json", {"numpy": [np_meta, np_mod, pip_ver], "gsap": [gsap_pkg, gsap_js], "ffmpeg": ffv, "api": api})
    return [check("pip metadata, pip show and numpy.__version__ agree", np_meta == np_mod == pip_ver, [np_meta, np_mod, pip_ver]),
            check("npm package.json version equals the loaded gsap.version", gsap_pkg == gsap_js, [gsap_pkg, gsap_js]),
            check("ffmpeg reports its version line", ffv.startswith("ffmpeg version"), ffv[:40]),
            check("API picked from the installed major (numpy 2 -> trapezoid)", (major >= 2 and integ == "numpy.trapezoid") or (major < 2 and integ == "numpy.trapz"), api),
            check("negative control: a remembered version does not match what is installed", stale["numpy"] != np_mod, [stale["numpy"], np_mod])], [out]


@card("WEB-23")
def trafilatura_arabic_metadata(task, wd):
    """Trafilatura extracts the main Arabic article text and its metadata (title, author, date) from HTML and drops the
    boilerplate (nav, ads, footer)."""
    import trafilatura
    res = trafilatura.bare_extraction(_ARTICLE, with_metadata=True, url="https://news.example/arab-motion-2026")
    d = res.as_dict() if hasattr(res, "as_dict") else dict(res)
    text = d.get("text") or ""
    out = write_json(wd, "extract.json", {k: d.get(k) for k in ("title", "author", "date", "text", "language")})
    full = BeautifulSoup_text(_ARTICLE)
    return [check("main text kept (Arabic, three paragraphs)", "القاهرة" in text and "ورش عمل" in text and len(text) > 300, len(text)),
            check("boilerplate dropped", not any(x in text for x in ("الرئيسية", "خصم خمسين", "جميع الحقوق")), text[:60]),
            check("metadata: title, author, date", d.get("title") == "مهرجان الحركة العربية 2026" and d.get("author") == "فريق كوزيف" and d.get("date") == "2026-10-20",
                  [d.get("title"), d.get("author"), d.get("date")]),
            check("trafilatura version recorded", bool(trafilatura.__version__)),
            check("negative control: the untreated HTML text includes the boilerplate", "خصم خمسين" in full and "جميع الحقوق" in full)], [out]


def BeautifulSoup_text(h):
    from bs4 import BeautifulSoup
    return BeautifulSoup(h, "lxml").get_text(" ")
