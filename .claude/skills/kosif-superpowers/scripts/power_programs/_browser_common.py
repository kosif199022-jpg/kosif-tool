"""Shared helpers for the wave-2 "browser" modules (<family>__browser.py).

`browser(work, job)` writes the job, runs `_browser_helper.cjs` (Playwright Chromium, every
http(s) request outside https://kosif.test/ aborted) and returns its result dict. Pages are
served from `work` (or job["root"]) at https://kosif.test/, a secure origin, so WebCodecs,
MediaRecorder and fonts behave as on a real https site. Vendored libraries (GSAP, MOTION kit,
three-kit bundle, Cairo fonts) are read-only files under vendor/ and are mapped into the page
with job["extra"].
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
HELPER = HERE / "_browser_helper.cjs"
KIT = REPO / ".claude/skills/kosif-superpowers/vendor/100-superskills/skills/kosif-montage-motion/scripts/kit"
GSAP = KIT / "gsap.min.js"
MOTION_KIT = KIT / "motion-kit.js"
K3_BUNDLE = KIT / "three-kit.bundle.js"
CAIRO_800 = KIT / "fonts/cairo-arabic-800-normal.woff2"
CAIRO_LATIN_800 = KIT / "fonts/cairo-latin-800-normal.woff2"
ESBUILD = REPO / "starters/remotion/node_modules/esbuild/bin/esbuild"
ORIGIN = "https://kosif.test"
LIBS = {"/lib/gsap.min.js": str(GSAP), "/lib/motion-kit.js": str(MOTION_KIT), "/lib/three-kit.bundle.js": str(K3_BUNDLE),
        "/lib/cairo-800.woff2": str(CAIRO_800), "/lib/cairo-latin-800.woff2": str(CAIRO_LATIN_800)}


def browser(work: Path, job: dict, name: str = "browser", timeout: int = 45) -> dict:
    job = dict(job)
    job.setdefault("root", str(work))
    extra = dict(LIBS)
    extra.update(job.get("extra") or {})
    job["extra"] = extra
    jf, rf = work / f"{name}_job.json", work / f"{name}_result.json"
    jf.write_text(json.dumps(job, ensure_ascii=False, indent=1), encoding="utf-8")
    r = subprocess.run(["node", str(HELPER), str(jf), str(rf)], capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError("browser helper failed: " + r.stderr[-1500:])
    return json.loads(rf.read_text(encoding="utf-8"))


def page(work: Path, name: str, html: str) -> str:
    (work / name).write_text(html, encoding="utf-8")
    return f"/{name}"


def sh(cmd, **kw) -> str:
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, **kw)
    if r.returncode != 0:
        raise RuntimeError(f"{cmd[0]} failed: {r.stderr[-800:]}")
    return r.stdout + r.stderr


def ff(*args) -> str:
    return sh(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args])


def probe(path) -> dict:
    return json.loads(sh(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path]))


def vstream(path) -> dict:
    return next(s for s in probe(path)["streams"] if s["codec_type"] == "video")


def astream(path):
    return next((s for s in probe(path)["streams"] if s["codec_type"] == "audio"), None)


def img(path) -> np.ndarray:
    return np.asarray(Image.open(path).convert("RGB")).astype(np.int16)


def px(path, x, y):
    return tuple(int(v) for v in img(path)[y, x])


def near(c, ref, tol=12) -> bool:
    return all(abs(int(a) - int(b)) <= tol for a, b in zip(c, ref))


def sha(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def decode_frames(video, w, h, n=None):
    """Raw RGB frames of a video as an (N, h, w, 3) uint8 array."""
    args = ["ffmpeg", "-v", "error", "-i", str(video)]
    if n:
        args += ["-frames:v", str(n)]
    args += ["-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    raw = subprocess.run(args, capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)


def gsap_page(body: str, script: str, size=(64, 36), head: str = "", libs=("gsap", "motion")) -> str:
    tags = "".join({"gsap": '<script src="/lib/gsap.min.js"></script>', "motion": '<script src="/lib/motion-kit.js"></script>',
                    "k3": '<script src="/lib/three-kit.bundle.js"></script>'}[k] for k in libs)
    w, h = size
    return (f"<!doctype html><html><head><meta charset=utf-8><style>html,body{{margin:0;background:#000}}"
            f"#root{{position:relative;width:{w}px;height:{h}px;overflow:hidden;background:#000}}</style>{head}{tags}</head>"
            f"<body>{body}<script>{script}</script></body></html>")
