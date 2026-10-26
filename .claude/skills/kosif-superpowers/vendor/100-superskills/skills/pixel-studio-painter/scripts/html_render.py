"""Render an HTML page (Three.js, WebGL, CSS, canvas) to a PNG deterministically in headless Edge/Chrome.

The idea comes from HyperFrames (heygen-com/hyperframes, Apache-2.0): write HTML, seek it, capture frames.
Contract for the page:
  * it sets `window.__ready = true` when the first frame is fully drawn (fonts, textures, post-processing);
  * for animation it may define `window.render(t)` (seconds) and set `window.__duration` (seconds);
    `frame(t)` calls `render(t)` then waits for `__ready` again.

    python html_render.py page.html out.png [--size 1920x1080] [--t 2.5]
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

EDGES = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
         r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
         r"C:\Program Files\Google\Chrome\Application\chrome.exe"]
# Measured on this machine (Intel Iris Xe): a 64-step 1080p raymarch frame = 142 ms with the real GPU through
# ANGLE/D3D11, 4335 ms on SwiftShader. The GPU is the default; HTML_RENDER_SOFTWARE=1 forces SwiftShader.
_SOFT = ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"]
_HARD = ["--use-angle=d3d11", "--use-gl=angle", "--enable-gpu-rasterization", "--enable-webgl"]
# Direct3D exists only on Windows; elsewhere (Linux sandboxes, macOS) WebGL runs on SwiftShader unless told otherwise
_USE_SOFT = bool(os.environ.get("HTML_RENDER_SOFTWARE")) or os.name != "nt"
GPU_FLAGS = ["--headless=new", "--hide-scrollbars", *(_SOFT if _USE_SOFT else _HARD),
             "--ignore-gpu-blocklist", "--disable-gpu-sandbox", "--autoplay-policy=no-user-gesture-required",
             "--allow-file-access-from-files"]


def browser_path() -> str | None:
    """Edge or Chrome on Windows; chromium / google-chrome / msedge on Linux and macOS; None = Playwright's own Chromium."""
    for p in EDGES + ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"]:
        if os.path.exists(p):
            return p
    for name in ("msedge", "chrome", "google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        found = shutil.which(name)
        if found:
            return found
    if _playwright():
        return None
    raise RuntimeError("no Edge, Chrome or Chromium found for HTML rendering (pip install playwright && playwright install chromium)")


def _playwright():
    try:
        from playwright.sync_api import sync_playwright
        return sync_playwright
    except ImportError:
        return None


def render_html(page: str | Path, out: str | Path, width: int = 1920, height: int = 1080, t: float | None = None,
                timeout: float = 90.0, scale: float = 1.0) -> dict:
    """One frame of the page. With Playwright (preferred) it waits for window.__ready and can seek `t`;
    without it, Edge's own --screenshot with a virtual-time budget is used (no seeking)."""
    page, out = Path(page).resolve(), Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.perf_counter()
    sp = _playwright()
    if sp:
        with sp() as p:
            browser = p.chromium.launch(executable_path=browser_path(), headless=True, args=GPU_FLAGS[2:])  # None → bundled Chromium
            ctx = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=scale)
            pg = ctx.new_page()
            pg.goto(page.as_uri(), wait_until="load", timeout=timeout * 1000)
            pg.wait_for_function("window.__ready === true", timeout=timeout * 1000)
            if t is not None:
                pg.evaluate("t => { window.__ready = false; if (window.render) window.render(t); else window.__ready = true; }", t)
                pg.wait_for_function("window.__ready === true", timeout=timeout * 1000)
            pg.wait_for_timeout(50)
            pg.screenshot(path=str(out), full_page=False)
            info = pg.evaluate("({dur: window.__duration || null, title: document.title || null})")
            browser.close()
        return {"backend": "playwright", "file": str(out), "size": (int(width * scale), int(height * scale)),
                "seconds": round(time.perf_counter() - t0, 1), "duration": info.get("dur"), "title": info.get("title")}
    prof = Path(tempfile.mkdtemp(prefix="kosif_edge_"))
    cmd = [browser_path(), *GPU_FLAGS, f"--user-data-dir={prof}", f"--window-size={width},{height}",
           f"--force-device-scale-factor={scale}", "--virtual-time-budget=30000", f"--screenshot={out}", page.as_uri()]
    subprocess.run(cmd, capture_output=True, timeout=timeout)
    shutil.rmtree(prof, ignore_errors=True)
    if not out.exists():
        raise RuntimeError("the browser produced no screenshot")
    return {"backend": "edge-screenshot", "file": str(out), "size": (int(width * scale), int(height * scale)),
            "seconds": round(time.perf_counter() - t0, 1)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page")
    ap.add_argument("out")
    ap.add_argument("--size", default="1920x1080")
    ap.add_argument("--t", type=float)
    ap.add_argument("--scale", type=float, default=1.0)
    a = ap.parse_args()
    w, h = (int(v) for v in a.size.lower().split("x"))
    print(render_html(a.page, a.out, w, h, a.t, scale=a.scale))


if __name__ == "__main__":
    main()
