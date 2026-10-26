"""Run picture code from any AI in its own process and turn it into paint jobs the studio plays pixel by pixel.

    python runner.py CODE_FILE OUT_DIR [--scale 1.0] [--export PNG]

The code can be any of:
  * an SVG document (or Python that prints/returns/saves one)
  * a KOSIF scene: Python that defines build() returning Steps (render's names are preloaded, imports optional)
  * any Python that draws a picture with PIL, matplotlib or turtle. With PIL every drawing command is recorded,
    so the studio paints the picture in the very order the code drew it.

Output, written as it becomes ready so drawing starts before the code has finished:
  OUT_DIR/job_0000.npz + job_0000.json ...   changed pixels in painting order + what was drawn
  OUT_DIR/done.json                          {"title", "kind", "jobs", "raster"} when finished
  OUT_DIR/error.txt                          if the code failed (the traceback, for the code panel)
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import re
import sys
import tempfile
import time
import traceback
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE)]
import render as R  # noqa: E402

PAPER = "#f3eee4"
BACKDROP = (27, 24, 34)
CALLS_AR = {"rectangle": "مستطيل", "rounded_rectangle": "مستطيل مستدير", "ellipse": "شكل بيضاوي",
            "circle": "دائرة", "polygon": "مضلع", "regular_polygon": "مضلع منتظم", "line": "خط", "arc": "قوس",
            "chord": "وتر", "pieslice": "قطاع", "point": "نقاط", "text": "نص", "multiline_text": "نص",
            "bitmap": "صورة صغيرة", "paste": "لصق صورة", "alpha_composite": "دمج طبقة", "blank": "اللوحة"}


def kind_of(code: str) -> str:
    if re.search(r"^IMAGE_B64\s*=", code, re.M) and not re.search(r"^\s*(def |draw\.|img\.|for |while )", code, re.M):
        return "image"                                    # data only: TITLE / SIZE / IMAGE_B64
    s = code.lstrip("\ufeff \t\r\n")
    low = s[:4000].lower()
    if s.startswith("<") and ("<!doctype html" in low or "<html" in low or "<canvas" in low or "<script" in low):
        return "html"
    if s.startswith("<") and "<svg" in low:
        return "svg"
    if re.search(r"^\s*def\s+build\s*\(", code, re.M):
        return "scene"
    return "python"


# ── writing paint jobs ──────────────────────────────────────────────────────────────────────────────────────
class Jobs:
    def __init__(self, out: Path, scale: float):
        self.out, self.scale = out, scale
        self.W, self.H = round(R.W0 * scale), round(R.H0 * scale)
        self.prev = np.empty((self.W * self.H, 3), np.uint8)
        self.prev[:] = (R.rgb(PAPER) * 255 + .5).astype(np.uint8)
        self.n = 0

    def add(self, img: np.ndarray, label: str, order: str = "grow", origin=None, weight: float = .5):
        flat = img.reshape(-1, 3)
        idx = np.flatnonzero(np.any(flat != self.prev, axis=1)).astype(np.int32)
        if idx.size == 0:
            return
        st = R.Step(label, [], order, origin, weight)
        o = R.reveal_order(idx, self.W, st, self.scale, seed=self.n)
        base = self.out / f"job_{self.n:04d}"
        np.savez(str(base) + ".tmp.npz", order=o, cols=flat[o])
        Path(str(base) + ".json").write_text(json.dumps({"label": label, "order": order, "origin": origin,
                                                         "weight": weight}, ensure_ascii=False), encoding="utf-8")
        os.replace(str(base) + ".tmp.npz", str(base) + ".npz")       # the studio only sees finished jobs
        self.prev = flat.copy()
        self.n += 1


class NativeJobs(Jobs):
    """Paint jobs on a canvas the size of the picture itself (RGBA), so the result equals it pixel for pixel."""

    def __init__(self, out: Path, w: int, h: int, start: int = 0):
        self.out, self.scale, self.W, self.H, self.n = out, 1.0, w, h, start
        self.prev = np.zeros((w * h, 4), np.uint8)
        (out / "canvas.json").write_text(json.dumps({"w": w, "h": h}), encoding="utf-8")

    def add(self, img: np.ndarray, label: str, order: str = "grow", origin=None, weight: float = .5):
        flat = img.reshape(-1, 4)
        idx = np.flatnonzero(np.any(flat != self.prev, axis=1)).astype(np.int32)
        if idx.size == 0:
            return
        o = R.reveal_order(idx, self.W, R.Step(label, [], order, origin, weight), 1.0, seed=self.n)
        base = self.out / f"job_{self.n:04d}"
        np.savez(str(base) + ".tmp.npz", order=o, cols=flat[o])
        Path(str(base) + ".json").write_text(json.dumps({"label": label, "order": order, "origin": origin,
                                                         "weight": weight}, ensure_ascii=False), encoding="utf-8")
        os.replace(str(base) + ".tmp.npz", str(base) + ".npz")
        self.prev = flat.copy()
        self.n += 1

    def add_raw(self, label: str, order: str, origin, weight: float, idx: np.ndarray, cols: np.ndarray):
        """A job already in painting order (exact redraw)."""
        base = self.out / f"job_{self.n:04d}"
        np.savez(str(base) + ".tmp.npz", order=idx.astype(np.int32), cols=cols)
        Path(str(base) + ".json").write_text(json.dumps({"label": label, "order": order, "origin": origin,
                                                         "weight": weight}, ensure_ascii=False), encoding="utf-8")
        os.replace(str(base) + ".tmp.npz", str(base) + ".npz")
        self.n += 1


def read_image_code(code: str) -> tuple[str, bytes]:
    """The title and the picture embedded in image code. Only literal assignments are read (ast.literal_eval):
    nothing in the file is executed."""
    import ast
    import base64
    vals = {}
    for node in ast.parse(code).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) \
                and node.targets[0].id in ("TITLE", "IMAGE_B64"):
            vals[node.targets[0].id] = ast.literal_eval(node.value)
    if "IMAGE_B64" not in vals:
        raise ValueError("IMAGE_B64 must be a plain string")
    return str(vals.get("TITLE", "صورة")), base64.b64decode("".join(str(vals["IMAGE_B64"]).split()))


def run_html(code_file: Path, out: Path, width: int = 1200, height: int = 800, t: float | None = None) -> dict:
    """An HTML page (Three.js, WebGL, CSS): rendered once in headless Edge at the studio's sheet size, saved as the
    reference, then painted from a blank canvas (plan chosen by Jev) and finished to the exact frame."""
    import exact
    import html_render
    frame = out / "frame.png"
    info = html_render.render_html(code_file, frame, width, height, t)
    im = Image.open(frame)
    im.load()
    rgba = np.ascontiguousarray(np.asarray(im.convert("RGBA")))
    Image.fromarray(rgba, "RGBA").save(out / "final.png")
    h, w = rgba.shape[:2]
    nj = NativeJobs(out, w, h)
    block_k, fine_k, plan = exact.choose_plan(rgba)
    for label, kind, origin, weight, order, cols in exact.plan(rgba, block_k, fine_k):
        nj.add_raw(label, kind, origin, weight, order, cols)
    p = {k: plan[k] for k in ("by", "choice", "probabilities")} if plan else None
    if plan:
        p["candidate"] = plan["candidates"][plan["choice"]]
    return {"title": info.get("title") or "HTML", "kind": "html", "raster": False, "jobs": nj.n, "plan": p,
            "render": {k: v for k, v in info.items() if k != "file"}, "final": im}


def run_html(code_file: Path, out: Path, width: int = 1200, height: int = 800, t: float | None = None) -> dict:
    """An HTML page (Three.js, WebGL, CSS): rendered once in headless Edge at the studio's sheet size, saved as the
    reference, then painted from a blank canvas (plan chosen by Jev) and finished to the exact frame."""
    import exact
    import html_render
    frame = out / "frame.png"
    info = html_render.render_html(code_file, frame, width, height, t)
    im = Image.open(frame)
    im.load()
    rgba = np.ascontiguousarray(np.asarray(im.convert("RGBA")))
    Image.fromarray(rgba, "RGBA").save(out / "final.png")
    h, w = rgba.shape[:2]
    nj = NativeJobs(out, w, h)
    block_k, fine_k, plan = exact.choose_plan(rgba)
    for label, kind, origin, weight, order, cols in exact.plan(rgba, block_k, fine_k):
        nj.add_raw(label, kind, origin, weight, order, cols)
    p = {k: plan[k] for k in ("by", "choice", "probabilities")} if plan else None
    if plan:
        p["candidate"] = plan["candidates"][plan["choice"]]
    return {"title": info.get("title") or "HTML", "kind": "html", "raster": False, "jobs": nj.n, "plan": p,
            "render": {k: v for k, v in info.items() if k != "file"}, "final": im}


def run_image_code(code: str, out: Path) -> dict:
    """Image code: paint the embedded picture from a blank sheet (Jev picks the plan for photos) and end
    identical to it; final.png is the reference the studio checks against."""
    import exact
    title, data = read_image_code(code)
    im = Image.open(io.BytesIO(data))
    im.load()
    rgba = np.ascontiguousarray(np.asarray(im.convert("RGBA")))
    Image.fromarray(rgba, "RGBA").save(out / "final.png")
    h, w = rgba.shape[:2]
    nj = NativeJobs(out, w, h)
    block_k, fine_k, info = exact.choose_plan(rgba)
    for label, kind, origin, weight, order, cols in exact.plan(rgba, block_k, fine_k):
        nj.add_raw(label, kind, origin, weight, order, cols)
    plan = {k: info[k] for k in ("by", "choice", "probabilities")} if info else None
    if info:
        plan["candidate"] = info["candidates"][info["choice"]]
    return {"title": title, "kind": "image", "raster": True, "jobs": nj.n, "plan": plan, "final": im}


def play_steps(steps, jobs: Jobs, rolloff: float):
    for _, st, img in R.render(steps, jobs.scale, ss=3, paper=PAPER, rolloff=rolloff):
        jobs.add(img, st.label, st.order, st.origin, st.weight)


# ── raster pictures (PIL, matplotlib, turtle) on the 1200 x 800 sheet ───────────────────────────────────────
class Sheet:
    """Where a picture of w x h pixels sits on the studio sheet: pixel art is enlarged by whole numbers (crisp),
    big pictures are reduced to fit, the rest is shown 1:1."""

    def __init__(self, w: int, h: int, scale: float):
        W, H = round(R.W0 * scale), round(R.H0 * scale)
        f = min(W / w, H / h)
        self.f = float(int(f)) if f >= 2 else f              # pixel art: whole-number zoom; the rest: fill the sheet
        self.nearest = f >= 2
        self.w, self.h = max(1, round(w * self.f)), max(1, round(h * self.f))
        self.x, self.y = (W - self.w) // 2, (H - self.h) // 2
        self.W, self.H, self.scale = W, H, scale

    def place(self, im: Image.Image) -> np.ndarray:
        rgba = im.convert("RGBA")
        if rgba.size != (self.w, self.h):
            rgba = rgba.resize((self.w, self.h), Image.NEAREST if self.nearest else Image.LANCZOS)
        sheet = Image.new("RGBA", (self.W, self.H), BACKDROP + (255,))
        sheet.alpha_composite(rgba, (self.x, self.y))
        return np.asarray(sheet.convert("RGB"))

    def origin(self, box):
        if not box:
            return None
        x0, y0, x1, y1 = box
        return ((self.x + (x0 + x1) / 2 * self.f) / self.scale, (self.y + (y0 + y1) / 2 * self.f) / self.scale)


def _bbox(xy):
    vals = []

    def flat(v):
        if isinstance(v, (int, float)):
            vals.append(float(v))
        elif isinstance(v, (list, tuple)):
            for t in v:
                flat(t)
    flat(xy)
    if len(vals) < 2:
        return None
    xs, ys = vals[0::2], vals[1::2]
    return (min(xs), min(ys), max(xs), max(ys))


class Recorder:
    """Watches every PIL drawing command. Commands of one kind in a row (360 sky lines) are gathered into strokes of
    up to 20; a new kind of command closes the stroke before it draws, so every step shows one kind of thing."""
    RUN = 20

    def __init__(self):
        self.streams: dict[int, list] = {}     # image id -> [(png bytes, label, bbox)]
        self.images: dict[int, Image.Image] = {}
        self.pending: dict[int, list] = {}
        self.final: Image.Image | None = None
        self.depth = 0

    def before(self, im: Image.Image, label: str):
        pend = self.pending.get(id(im))
        if pend and pend[-1][0] != label:
            self.commit(im)

    def after(self, im: Image.Image, label: str, box, now: bool = False):
        self.images[id(im)] = im
        pend = self.pending.setdefault(id(im), [])
        pend.append((label, box))
        if now or len(pend) >= self.RUN:
            self.commit(im)

    def commit(self, im: Image.Image):
        key = id(im)
        pend = self.pending.get(key) or [("blank", None)]
        buf = io.BytesIO()
        im.convert("RGBA").save(buf, "PNG", compress_level=1)
        boxes = [p[1] for p in pend if p[1]]
        box = (min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes),
               max(b[3] for b in boxes)) if boxes else None
        names: dict[str, int] = {}
        for lb, _ in pend:
            names[lb] = names.get(lb, 0) + 1
        text = "، ".join(f"{CALLS_AR.get(k, k)}{' ×' + str(v) if v > 1 else ''}" for k, v in names.items())
        stream = self.streams.setdefault(key, [])
        stream.append((buf.getvalue(), text, box))
        self.pending[key] = []
        if len(stream) > 300:                                 # keep it bounded: thin out, keep the order
            self.streams[key] = stream[:1] + stream[1::2]

    def flush(self):
        for key, pend in list(self.pending.items()):
            if pend:
                self.commit(self.images[key])

    def install(self):
        from PIL import ImageDraw
        rec = self

        def wrap(name, orig):
            def inner(self, *a, **k):
                im = getattr(self, "_image", None)
                top = rec.depth == 0 and im is not None
                if top:
                    rec.before(im, name)
                rec.depth += 1
                try:
                    return orig(self, *a, **k)
                finally:
                    rec.depth -= 1
                    if top:
                        rec.after(im, name, _bbox(a[0] if a else k.get("xy")))
            return inner
        for name in CALLS_AR:
            orig = getattr(ImageDraw.ImageDraw, name, None)
            if callable(orig):
                setattr(ImageDraw.ImageDraw, name, wrap(name, orig))
        draw_init = ImageDraw.ImageDraw.__init__

        def init(self, im, *a, **k):                            # the blank canvas is the first snapshot
            draw_init(self, im, *a, **k)
            if id(im) not in rec.streams:
                rec.images[id(im)] = im
                rec.commit(im)
        ImageDraw.ImageDraw.__init__ = init
        for name in ("paste", "alpha_composite"):
            orig = getattr(Image.Image, name)

            def make(name=name, orig=orig):
                def inner(self, *a, **k):
                    tracked = rec.depth == 0 and id(self) in rec.streams
                    if tracked:
                        rec.before(self, name)
                    r = orig(self, *a, **k)
                    if tracked:
                        rec.after(self, name, None, now=True)
                    return r
                return inner
            setattr(Image.Image, name, make())
        save, show = Image.Image.save, Image.Image.show

        def save_(self, fp, *a, **k):
            rec.final, rec.final_of = self.copy(), id(self)
            if isinstance(fp, (str, Path)) and str(fp).lower().endswith(".svg"):
                return None
            return save(self, fp, *a, **k)

        def show_(self, *a, **k):
            rec.final, rec.final_of = self.copy(), id(self)
        Image.Image.save, Image.Image.show = save_, show_

    def stream_for(self, final: Image.Image):
        """The recorded snapshots that lead to the final picture: its own, or those of a same-size layer."""
        key = getattr(self, "final_of", None) if final is self.final else id(final)
        if key in self.streams:
            return self.streams[key]
        same = [k for k, im in self.images.items() if im.size == final.size and len(self.streams.get(k, [])) > 1]
        return self.streams[same[-1]] if same else []


def run_python(code: str, jobs: Jobs, workdir: Path) -> dict:
    rec = Recorder()
    rec.install()
    figs, plt = [], None
    if re.search(r"matplotlib|pyplot|pylab|seaborn", code):     # only then: it costs seconds to load
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        plt.show = lambda *a, **k: figs.extend(plt.figure(n) for n in plt.get_fignums() if plt.figure(n) not in figs)
    turtle_used = "turtle" in code
    if turtle_used:
        _prepare_turtle()
    ns = {"__name__": "__main__"}
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        exec(compile(code, "<الكود>", "exec"), ns)
    printed = out.getvalue()
    rec.flush()

    final = rec.final
    if final is None:                                           # the last picture the code made
        drawn = [rec.images[k] for k in rec.streams]
        if drawn:
            final = max(drawn, key=lambda im: im.size[0] * im.size[1])
    if final is None and plt is not None:
        for n in plt.get_fignums():
            if plt.figure(n) not in figs:
                figs.append(plt.figure(n))
        if figs:
            buf = io.BytesIO()
            figs[-1].savefig(buf, format="png", dpi=110, bbox_inches="tight")
            final = Image.open(io.BytesIO(buf.getvalue()))
            final.load()
    if final is None and turtle_used:
        final = _grab_turtle()
    if final is None:                                           # SVG produced as text, or a file on disk
        svg = next((v for v in [printed, *[x for x in ns.values() if isinstance(x, str)]] if "<svg" in v), None)
        files = sorted(workdir.glob("*.svg")) + sorted(workdir.glob("*.png")) + sorted(workdir.glob("*.jpg"))
        if svg is None and files and files[0].suffix == ".svg":
            svg = files[0].read_text(encoding="utf-8", errors="ignore")
        if svg:
            import svg_import
            title, steps = svg_import.load_svg(svg[svg.index("<"):])
            play_steps(steps, jobs, 1.0)
            return {"title": title, "kind": "svg", "raster": False}
        if files:
            final = Image.open(files[0])
            final.load()
    if final is None:
        raise RuntimeError("the code ran but made no picture (no PIL image, matplotlib figure, turtle drawing or SVG)")

    final = final.convert("RGBA")
    final.save(jobs.out / "final.png")                          # what the code really made: the reference
    nj = NativeJobs(jobs.out, *final.size, start=jobs.n)
    stream = rec.stream_for(final)
    for png, label, box in stream:
        snap = Image.open(io.BytesIO(png)).convert("RGBA")
        if snap.size == final.size:
            centre = ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2) if box else None
            nj.add(np.asarray(snap), label, "grow" if box else "sweep", centre, .35)
    nj.add(np.asarray(final), "اللمسات الأخيرة" if stream else "الصورة", "sweep", None, .6 if stream else 1.2)
    jobs.n = nj.n
    kind = "pil" if stream else "matplotlib" if figs else "turtle" if turtle_used else "python"
    return {"title": ns.get("TITLE", "كود بايثون"), "kind": kind, "raster": True, "final": final}


def _prepare_turtle():
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        pass
    import turtle
    for name in ("done", "mainloop", "exitonclick", "bye"):
        setattr(turtle, name, lambda *a, **k: None)
    turtle.TurtleScreen.mainloop = lambda *a, **k: None
    turtle.TurtleScreen.exitonclick = lambda *a, **k: None
    turtle.tracer(0, 0)


def _grab_turtle():
    import turtle
    from PIL import ImageGrab
    sc = turtle.Screen()
    sc.update()
    cv = sc.getcanvas()
    cv.update()
    time.sleep(.2)
    x, y = cv.winfo_rootx(), cv.winfo_rooty()
    return ImageGrab.grab((x, y, x + cv.winfo_width(), y + cv.winfo_height()), all_screens=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("code")
    ap.add_argument("out")
    ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--export", help="render the final picture to this PNG at --scale (vector code stays sharp)")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    code_path = Path(a.code).resolve()
    code = code_path.read_text(encoding="utf-8-sig")
    workdir = Path(tempfile.mkdtemp(prefix="kosif_code_"))
    os.chdir(workdir)                     # files the code writes land in a scratch folder, not next to the studio
    jobs = Jobs(out, a.scale)
    try:
        kind = kind_of(code)
        if kind == "image":
            steps, rolloff = None, 1.0
            info = run_image_code(code, out)
            jobs.n = info["jobs"]
        elif kind == "html":
            steps, rolloff = None, 1.0
            info = run_html(code_path, out, round(R.W0 * (a.scale if a.export else 1.0)),
                            round(R.H0 * (a.scale if a.export else 1.0)))
            jobs.n = info["jobs"]
        elif kind == "html":
            steps, rolloff = None, 1.0
            info = run_html(code_path, out, round(R.W0 * (a.scale if a.export else 1.0)),
                            round(R.H0 * (a.scale if a.export else 1.0)))
            jobs.n = info["jobs"]
        elif kind == "svg":
            import svg_import
            title, steps = svg_import.load_svg(code)
            info = {"title": title, "kind": "svg", "raster": False}
            rolloff = 1.0
        elif kind == "scene":
            ns = {"__name__": "kosif_scene"}
            exec("from render import *\nimport math, random\n", ns)
            exec(compile(code, "<الكود>", "exec"), ns)
            steps = ns["build"]()
            info = {"title": ns.get("TITLE", "مشهد"), "kind": "scene", "raster": False}
            rolloff = ns.get("ROLLOFF", 0.82)
        else:
            steps, rolloff = None, 1.0
            info = run_python(code, jobs, workdir)
        if a.export:
            if steps is not None:
                R.render_image(steps, a.scale, ss=2 if a.scale > 2 else 3, rolloff=rolloff).save(a.export)
            elif kind == "html":
                info["final"].convert("RGB").save(a.export)      # HTML is resolution independent: re-rendered at --scale
            elif kind == "html":
                info["final"].convert("RGB").save(a.export)      # HTML is resolution independent: re-rendered at --scale
            else:
                info["final"].save(a.export)                     # raster code: its own resolution, exactly
        elif steps is not None:
            play_steps(steps, jobs, rolloff)
        info.pop("final", None)
        info["jobs"] = jobs.n
        (out / "done.json").write_text(json.dumps(info, ensure_ascii=False), encoding="utf-8")
    except BaseException:
        (out / "error.txt").write_text(traceback.format_exc(limit=6), encoding="utf-8")
        sys.exit(1)


if __name__ == "__main__":
    main()
