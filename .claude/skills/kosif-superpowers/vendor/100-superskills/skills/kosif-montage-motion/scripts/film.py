"""Film: the studio's drawing as a video, and time-based pictures as video. Frames go straight to FFmpeg.

    python film.py drawing <scene|code file> --out out/x.mp4 [--fps 30] [--speed normal]   the picture forming pixel by pixel
    python film.py animate <page.html|scene.py> --out out/x.mp4 [--fps 30] [--seconds 6]    render(t) / build(t) frames

Idea from HyperFrames (heygen-com/hyperframes): deterministic frames from a seekable source, encoded by FFmpeg.
"""
from __future__ import annotations

import argparse
import os
import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE / "scenes")]
import render as R  # noqa: E402

PAPER = "#f3eee4"
SPEEDS = {"slow": 5.0, "normal": 1.8, "fast": 0.55}


def ffmpeg() -> str:
    f = shutil.which("ffmpeg")
    if not f:
        raise RuntimeError("ffmpeg is not on PATH")
    return f


class Encoder:
    """Raw RGB frames piped into libx264. `preset`/`crf` trade time for size (draft: ultrafast/23, delivery: medium/18)."""

    def __init__(self, out: Path, w: int, h: int, fps: int, preset: str = "medium", crf: int = 18):
        out.parent.mkdir(parents=True, exist_ok=True)
        self.p = subprocess.Popen([ffmpeg(), "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}",
                                   "-r", str(fps), "-i", "-", "-c:v", "libx264", "-preset", preset, "-pix_fmt", "yuv420p",
                                   "-crf", str(crf), "-g", str(fps * 2), "-movflags", "+faststart", str(out)],
                                  stdin=subprocess.PIPE, bufsize=w * h * 3 * 4)
        self.n = 0

    def frame(self, rgb: np.ndarray):
        self.p.stdin.write(np.ascontiguousarray(rgb).tobytes())
        self.n += 1

    def close(self):
        self.p.stdin.close()
        rc = self.p.wait()
        if rc != 0:
            raise RuntimeError(f"ffmpeg encoder exited with {rc} after {self.n} frames")


def drawing_jobs(source: str):
    """Paint jobs for a scene name or a code file, exactly as the studio plays them."""
    try:
        import studio
    except ImportError:
        raise SystemExit("film drawing needs KOSIF Studio (studio.py) next to film.py — the skill package has only the animate mode")
    src = Path(source)
    if src.suffix.lower() in studio.IMAGE_TYPES and src.exists():         # an image: its own code, drawn exactly
        work = Path(tempfile.mkdtemp(prefix="kosif_film_img_"))
        src = work / f"{src.stem}_code.py"
        src.write_text(studio.image_code(Path(source), Path(source).stem), encoding="utf-8")
    if src.suffix.lower() in (".py", ".svg", ".html", ".htm", ".txt") and src.exists():
        work = Path(tempfile.mkdtemp(prefix="kosif_film_"))
        subprocess.run([sys.executable, str(HERE / "runner.py"), str(src), str(work)], capture_output=True, timeout=900)
        if (work / "error.txt").exists():
            raise RuntimeError((work / "error.txt").read_text(encoding="utf-8")[-800:])
        canvas = json.loads((work / "canvas.json").read_text(encoding="utf-8")) if (work / "canvas.json").exists() else None
        jobs = []
        for i in range(10000):
            f = work / f"job_{i:04d}.npz"
            if not f.exists():
                break
            meta = json.loads((work / f"job_{i:04d}.json").read_text(encoding="utf-8"))
            with np.load(f) as z:
                jobs.append((meta, z["order"], z["cols"]))
        shutil.rmtree(work, ignore_errors=True)
        return canvas, jobs
    title, steps, rolloff = studio.load(source)
    jobs, prev = [], None
    for i, st, img in R.render(steps, 1.0, ss=3, paper=PAPER, rolloff=rolloff):
        flat = img.reshape(-1, 3)
        if prev is None:
            prev = np.empty_like(flat)
            prev[:] = (R.rgb(PAPER) * 255 + .5).astype(np.uint8)
        idx = np.flatnonzero(np.any(flat != prev, axis=1)).astype(np.int32)
        order = R.reveal_order(idx, img.shape[1], st, 1.0, seed=i)
        jobs.append(({"label": st.label, "weight": st.weight}, order, flat[order].copy()))
        prev = flat.copy()
    return None, jobs


def film_drawing(source: str, out: Path, fps: int = 30, speed: str = "normal", hold: float = 1.5) -> dict:
    canvas, jobs = drawing_jobs(source)
    if canvas:
        w, h = canvas["w"], canvas["h"]
        # fit the native canvas into a 16:9 frame the way the studio shows it
        fw, fh = 1280, 720
        f = min(fw / w, fh / h)
        dw, dh = max(2, round(w * f) // 2 * 2), max(2, round(h * f) // 2 * 2)
        native = np.zeros((w * h, 4), np.uint8)
    else:
        w, h = R.W0, R.H0
        fw, fh, dw, dh = 1200, 800, 1200, 800
        flat = np.empty((w * h, 3), np.uint8)
        flat[:] = (R.rgb(PAPER) * 255 + .5).astype(np.uint8)
    enc = Encoder(out, fw, fh, fps)
    k = SPEEDS.get(speed, 1.8)
    t = time.perf_counter()
    import cv2

    def frame():
        if canvas:
            a = native[:, 3:4].astype(np.float32) / 255
            rgb = (native[:, :3] * a + (R.rgb(PAPER) * 255) * (1 - a) + .5).astype(np.uint8).reshape(h, w, 3)
            view = cv2.resize(rgb, (dw, dh), interpolation=cv2.INTER_AREA if f < 1 else cv2.INTER_NEAREST)
            fr = np.full((fh, fw, 3), 27, np.uint8)
            fr[(fh - dh) // 2:(fh - dh) // 2 + dh, (fw - dw) // 2:(fw - dw) // 2 + dw] = view
            return fr
        return flat.reshape(h, w, 3)
    for meta, order, cols in jobs:
        n = len(order)
        dur = k * float(meta.get("weight", .5)) * (n / (w * h)) ** .5
        frames = max(1, int(round(dur * fps)))
        for j in range(1, frames + 1):
            a, b = int(n * (j - 1) / frames), int(n * j / frames)
            sel = order[a:b]
            if canvas:
                c = cols[a:b]
                native[sel] = c if c.shape[1] == 4 else np.column_stack([c, np.full(len(c), 255, np.uint8)])
            else:
                flat[sel] = cols[a:b]
            enc.frame(frame())
    last = frame()
    for _ in range(int(hold * fps)):
        enc.frame(last)
    enc.close()
    return {"file": str(out), "frames": enc.n, "fps": fps, "seconds": round(enc.n / fps, 1), "encode_s": round(time.perf_counter() - t, 1)}


SEEK_JS = """t => { window.__ready = false;
  if (window.render) { window.render(t); }
  else if (window.seek) { window.seek(t); requestAnimationFrame(() => requestAnimationFrame(() => { window.__ready = true; })); }
  else { window.__ready = true; } }"""


def _decode(buf: bytes) -> np.ndarray:
    """PNG/JPEG bytes → RGB uint8 through OpenCV (2-3× faster than PIL for 1080p frames)."""
    try:
        import cv2
        a = cv2.imdecode(np.frombuffer(buf, np.uint8), cv2.IMREAD_COLOR)
        if a is not None:
            return a[..., ::-1]
    except ImportError:
        pass
    import io
    return np.asarray(Image.open(io.BytesIO(buf)).convert("RGB"))


def _grabber(pg, capture: str = "png"):
    """The fastest way to read the page's pixels: Chrome DevTools' captureScreenshot with optimizeForSpeed (a fast
    zlib level for PNG — lossless, about half the time of the default encoder; JPEG q95 for drafts). Falls back to
    Playwright's screenshot on browsers without the flag."""
    import base64
    fmt = "jpeg" if capture == "jpeg" else "png"
    extra = {"quality": 95} if fmt == "jpeg" else {}
    try:
        cdp = pg.context.new_cdp_session(pg)
        cdp.send("Page.captureScreenshot", {"format": fmt, "fromSurface": True, "optimizeForSpeed": True, **extra})

        def grab() -> bytes:
            return base64.b64decode(cdp.send("Page.captureScreenshot", {"format": fmt, "fromSurface": True, "optimizeForSpeed": True, **extra})["data"])
        return grab
    except Exception:                                      # noqa: BLE001 — an older Chromium: the plain screenshot path
        kw = {"type": "jpeg", "quality": 95} if fmt == "jpeg" else {"type": "png"}
        return lambda: pg.screenshot(timeout=90000, **kw)


def _avail_gb() -> float | None:
    """Memory new work can still allocate (GB). A malloc fails when the COMMIT limit is reached, not when RAM is full
    (Windows compresses and pages), so: Windows → commit headroom (GlobalMemoryStatusEx.ullAvailPageFile); Linux →
    MemAvailable + half the free swap; else psutil's available RAM."""
    try:
        if os.name == "nt":
            import ctypes

            class MS(ctypes.Structure):
                _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong), ("ullTotalPhys", ctypes.c_ulonglong),
                            ("ullAvailPhys", ctypes.c_ulonglong), ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                            ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong), ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
            m = MS(); m.dwLength = ctypes.sizeof(MS)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m)):
                return m.ullAvailPageFile / 2 ** 30
        else:
            info = {ln.split(":")[0]: int(ln.split()[1]) for ln in open("/proc/meminfo", encoding="ascii") if ln.split()[1:2]}
            if "MemAvailable" in info:
                return (info["MemAvailable"] + 0.5 * info.get("SwapFree", 0)) / 2 ** 20
    except Exception:  # noqa: BLE001
        pass
    try:
        import psutil
        return psutil.virtual_memory().available / 2 ** 30
    except Exception:  # noqa: BLE001
        return None


def _workers_default(n_frames: int, w: int = 1920, h: int = 1080) -> int:
    """How many browsers to run side by side. Parallel pages pay off only when there are enough frames to amortise each
    page's build (3D scenes mesh and compile shaders on load): never more than one page per 20 frames, at most 6.
    Software WebGL (SwiftShader) already rasterises on every core — measured on 4 cores, 2 pages beat 1 and 4 — so it
    gets one page per 2 cores. Memory caps it too: each page with its own x264 encoder needs ≈ 0.45 GB + 0.25 GB per
    megapixel of what can still be allocated (six 1080×1920 workers beside a test run and other jobs ended in
    "x264 malloc failed"). KOSIF_WORKERS overrides."""
    env = os.environ.get("KOSIF_WORKERS")
    if env:
        return max(1, int(env))
    cores = os.cpu_count() or 1
    if n_frames < 40 or cores < 2:
        return 1
    import html_render
    per_page = 2 if getattr(html_render, "_USE_SOFT", False) else 1
    nw = max(1, min(cores // per_page, 6, n_frames // 20))
    free = _avail_gb()
    if free is not None:
        nw = max(1, min(nw, int((free - 2.0) / (0.45 + 0.25 * w * h / 1e6))))   # keep ~2 GB of headroom for the rest
    return nw


auto_workers = _workers_default                                    # the Pro branch's public name for the same policy


def _open_page(src: Path, w: int, h: int, budget_ms: float, scale: float = 1.0):
    """A headless page on the composition, ready to be sought. Returns (playwright, browser, page, native_blur)."""
    import html_render
    from playwright.sync_api import sync_playwright
    p = sync_playwright().start()
    browser = p.chromium.launch(executable_path=html_render.browser_path(), headless=True, args=html_render.page_flags(src))
    vw, vh = (max(2, round(w * scale) // 2 * 2), max(2, round(h * scale) // 2 * 2)) if scale != 1.0 else (w, h)
    pg = browser.new_context(viewport={"width": vw, "height": vh}).new_page()
    if scale != 1.0:                                           # a draft: the page keeps its layout, CSS zoom shrinks it; 3D kits read __draftScale for their buffers
        pg.add_init_script(f"window.__draftScale = {scale}; document.addEventListener('DOMContentLoaded', () => {{ document.documentElement.style.zoom = '{scale}'; }});")
    errors: list[str] = []
    pg.on("pageerror", lambda e: errors.append(str(e)[:300]))
    pg.on("console", lambda m: errors.append("console.error: " + m.text[:300]) if m.type == "error" else None)
    pg.goto(src.resolve().as_uri(), wait_until="load", timeout=budget_ms)
    # pages with the kit's shim report readiness (fonts, footage); bare canvas pages only define seek(t).
    # A page that threw and never reports ready fails here in seconds, not after the whole budget.
    ready = "window.__ready === true || (typeof window.seek === 'function' && typeof window.render !== 'function')"
    waited = 0.0
    while True:
        try:
            pg.wait_for_function(ready, timeout=5000)
            break
        except Exception:                                  # noqa: BLE001 — a wait timeout; decide whether to keep waiting
            waited += 5.0
            if errors and not pg.evaluate(ready):
                browser.close(); p.stop()
                raise RuntimeError("the page threw before it was ready:\n  " + "\n  ".join(errors[:5]))
            if waited * 1000 >= budget_ms:
                browser.close(); p.stop()
                raise RuntimeError(f"the page never set window.__ready within {budget_ms / 1000:.0f} s")
    native = bool(pg.evaluate("!!window.__nativeBlur"))
    return p, browser, pg, native


def _render_chunk(job: dict) -> dict:
    """Frames [i0, i1) of a page into one MP4 segment. Runs in its own process with its own browser; deterministic
    pages make every segment identical to what a single pass would have drawn."""
    src, seg = Path(job["src"]), Path(job["seg"])
    w, h, fps, k = job["w"], job["h"], job["fps"], job["blur"]
    shutter, stack, start, capture = job["shutter"], job["stack"], job["start"], job["capture"]
    frames_dir = Path(job["frames_dir"]) if job.get("frames_dir") else None
    scale = float(job.get("scale") or 1.0)
    ow, oh = max(2, round(w * scale) // 2 * 2), max(2, round(h * scale) // 2 * 2)
    budget = float(os.environ.get("KOSIF_PAGE_TIMEOUT", "600")) * 1000
    p, browser, pg, native = _open_page(src, w, h, budget, scale)
    try:
        pg.evaluate("([k, s, f, st]) => { window.__blur = k; window.__shutter = s; window.__fps = f; window.__stack = st; }",
                    [k if native else 1, float(shutter), int(fps), stack])
        direct = (native or k == 1) and not frames_dir and scale == 1.0 and capture == "png"
        if direct:                                             # PNG bytes piped to FFmpeg undecoded (v1.3): no Python decode per frame
            enc = subprocess.Popen([ffmpeg(), "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(fps), "-c:v", "png", "-i", "-",
                                    "-c:v", "libx264", "-preset", job["preset"], "-crf", str(job["crf"]), "-pix_fmt", "yuv420p",
                                    "-vf", f"scale={ow}:{oh}:flags=neighbor", "-r", str(fps), "-movflags", "+faststart", str(seg)], stdin=subprocess.PIPE)
        else:
            enc = Encoder(seg, ow, oh, fps, job["preset"], job["crf"])
        grab = _grabber(pg, capture)

        def fit(a: np.ndarray) -> np.ndarray:                  # device pixels may round differently from ow×oh by one pixel
            return a if a.shape[0] == oh and a.shape[1] == ow else a[:oh, :ow] if a.shape[0] >= oh and a.shape[1] >= ow else np.pad(a, ((0, oh - a.shape[0]), (0, ow - a.shape[1]), (0, 0)), mode="edge")

        def shot(t: float, raw: bool = False):
            # a busy machine (or a <video> still decoding) can stall the compositor past one screenshot timeout;
            # seek again and retry instead of losing the whole render
            for attempt in range(4):
                try:
                    pg.evaluate(SEEK_JS, max(0.0, t))
                    pg.wait_for_function("window.__ready === true", timeout=180000)
                    return grab() if raw else fit(_decode(grab()))
                except Exception as e:                    # noqa: BLE001 — playwright TimeoutError and friends
                    if attempt == 3:
                        raise
                    print(f"frame t={t:.3f}: {type(e).__name__}, retry {attempt + 1}", file=sys.stderr, flush=True)
                    pg.wait_for_timeout(1500 * (attempt + 1))
        f0 = job.get("frame0_t")
        for i in range(job["i0"], job["i1"]):
            t = start + i / fps if not (i == 0 and f0 is not None) else float(f0)   # frame 0 = the poster moment (no re-encode later)
            if direct:
                enc.stdin.write(shot(t, raw=True))
                continue
            if native or k == 1:
                rgb = shot(t)
            else:                                              # centred shutter: samples at t + s/fps·((j+.5)/k − .5)
                acc = np.zeros((oh, ow, 3), np.float32)
                for j in range(k):
                    sub = shot(t + shutter / fps * ((j + 0.5) / k - 0.5))
                    if stack == "lighten":
                        np.maximum(acc, sub, out=acc)
                    else:
                        acc += sub
                rgb = np.clip(acc if stack == "lighten" else acc / k + 0.5, 0, 255).astype(np.uint8)
            enc.frame(rgb)
            if frames_dir:
                Image.fromarray(rgb).save(frames_dir / f"f{i:05d}.jpg", quality=92)
        if direct:
            enc.stdin.close()
            if enc.wait() != 0:
                raise RuntimeError("ffmpeg failed while encoding the PNG stream")
        else:
            enc.close()
    finally:
        browser.close()
        p.stop()
    return {"seg": str(seg), "frames": job["i1"] - job["i0"], "native_blur": native}


def _concat(segments: list[Path], out: Path):
    lst = out.with_suffix(".segments.txt")
    lst.write_text("".join(f"file '{s.resolve().as_posix()}'\n" for s in segments), encoding="utf-8")
    r = subprocess.run([ffmpeg(), "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy",
                        "-movflags", "+faststart", str(out)], capture_output=True, text=True)
    lst.unlink(missing_ok=True)
    if r.returncode != 0:
        raise RuntimeError("segment concat failed: " + r.stderr[-600:])


def film_animate(source: str, out: Path, fps: int = 30, seconds: float | None = None, size=(1280, 720), blur: int = 1,
                 shutter: float = 0.5, start: float = 0.0, frames_dir: Path | None = None, stack: str = "average",
                 workers: int = 0, capture: str = "png", preset: str = "medium", crf: int = 18, scale: float = 1.0,
                 frame0_t: float | None = None) -> dict:
    """Frames of a seekable page through FFmpeg. blur = sub-frames per output frame: a real shutter, k times the cost.
    Pages that accumulate on the GPU themselves set window.__nativeBlur (the three-kit's makeFrameLoop does, reading
    window.__blur / __shutter / __fps); for every other page (GSAP compositions, canvas seek(t) films) the samples are
    taken here, centred on the frame's time, averaged in float and quantised once — the way film cameras smear motion.
    shutter is in frames: 0.5 = a 180° shutter; 30 at 30 fps = a one-second long exposure (silky water, light trails).
    stack="lighten" keeps each pixel's brightest sample instead of the mean — star trails and light painting.
    workers > 1 splits the timeline across that many browsers (one process each) and concatenates the segments
    losslessly; 0 = pick by core count. capture="jpeg" grabs frames as JPEG q95 (≈2× faster than PNG, invisible in
    the H.264 output). preset/crf go to libx264 (draft: ultrafast/23).
    A page may expose window.render(t) (KOSIF / HyperFrames shim) or window.seek(t) (the canvas route)."""
    src = Path(source)
    t0 = time.perf_counter()
    if src.suffix.lower() in (".html", ".htm"):
        w, h = size
        if frames_dir:
            frames_dir.mkdir(parents=True, exist_ok=True)
        # the duration comes from the page unless given; read it once in a short-lived browser only when needed
        if seconds is None:
            budget = float(os.environ.get("KOSIF_PAGE_TIMEOUT", "600")) * 1000
            p, browser, pg, _ = _open_page(src, w, h, budget)
            seconds = pg.evaluate("window.__duration || 4")
            browser.close(); p.stop()
        n = int(round(seconds * fps))
        k = max(1, int(blur))
        nw = workers or _workers_default(n, int(w * scale), int(h * scale))
        nw = max(1, min(nw, n))
        base = dict(src=str(src), w=w, h=h, fps=fps, blur=k, shutter=shutter, stack=stack, start=start, capture=capture,
                    preset=preset, crf=crf, scale=scale, frames_dir=str(frames_dir) if frames_dir else None, frame0_t=frame0_t)
        if nw == 1:
            rep = _render_chunk({**base, "i0": 0, "i1": n, "seg": str(out)})
            return {"file": str(out), "frames": n, "fps": fps, "seconds": seconds, "blur": k, "native_blur": rep["native_blur"],
                    "workers": 1, "capture": capture, "encode_s": round(time.perf_counter() - t0, 1)}
        bounds = [round(n * i / nw) for i in range(nw + 1)]
        segdir = Path(tempfile.mkdtemp(prefix="kosif_seg_"))
        jobs = [{**base, "i0": bounds[i], "i1": bounds[i + 1], "seg": str(segdir / f"seg{i:02d}.mp4")} for i in range(nw) if bounds[i + 1] > bounds[i]]
        # one plain child process per chunk (v1.3) — not multiprocessing: its spawn start re-imports the caller's
        # __main__, which breaks scripts without a main guard; each child writes its result next to its segment
        procs = []
        for j in jobs:
            jf = Path(j["seg"]).with_suffix(".job.json")
            jf.write_text(json.dumps(j), encoding="utf-8")
            procs.append((subprocess.Popen([sys.executable, str(Path(__file__).resolve()), "_chunk", str(jf)]), jf))
        failed = [jf.name for pr, jf in procs if pr.wait() != 0]
        if failed:
            shutil.rmtree(segdir, ignore_errors=True)
            raise RuntimeError(f"render worker(s) failed: {', '.join(failed)}")
        reps = [json.loads(jf.with_suffix(".out.json").read_text(encoding="utf-8")) for _, jf in procs]
        _concat([Path(j["seg"]) for j in jobs], out)
        shutil.rmtree(segdir, ignore_errors=True)
        return {"file": str(out), "frames": n, "fps": fps, "seconds": seconds, "blur": k, "native_blur": reps[0]["native_blur"],
                "workers": len(jobs), "capture": capture, "encode_s": round(time.perf_counter() - t0, 1)}
    import importlib
    mod = importlib.import_module(src.stem)
    if not hasattr(mod, "build_t"):
        raise RuntimeError("a scene animates when it defines build_t(t) -> steps")
    dur = seconds or getattr(mod, "DURATION", 4.0)
    w, h = R.W0, R.H0
    enc = Encoder(out, w, h, fps, preset, crf)
    n = int(dur * fps)
    for i in range(n):
        enc.frame(np.asarray(R.render_image(mod.build_t(i / fps), 1.0, rolloff=getattr(mod, "ROLLOFF", .82))))
    enc.close()
    return {"file": str(out), "frames": n, "fps": fps, "seconds": dur, "encode_s": round(time.perf_counter() - t0, 1)}


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "_chunk":          # a parallel render worker (see film_animate)
        jf = Path(sys.argv[2])
        rep = _render_chunk(json.loads(jf.read_text(encoding="utf-8")))
        jf.with_suffix(".out.json").write_text(json.dumps(rep), encoding="utf-8")
        return
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["drawing", "animate"])
    ap.add_argument("source")
    ap.add_argument("--out", required=True)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--speed", default="normal")
    ap.add_argument("--seconds", type=float)
    ap.add_argument("--workers", type=int, default=0); ap.add_argument("--capture", default="png", choices=["png", "jpeg"])
    ap.add_argument("--preset", default="medium"); ap.add_argument("--crf", type=int, default=18)
    a = ap.parse_args()
    if a.mode == "drawing":
        print(json.dumps(film_drawing(a.source, Path(a.out), a.fps, a.speed), ensure_ascii=False))
    else:
        print(json.dumps(film_animate(a.source, Path(a.out), a.fps, a.seconds, workers=a.workers, capture=a.capture, preset=a.preset, crf=a.crf), ensure_ascii=False))


if __name__ == "__main__":
    main()
