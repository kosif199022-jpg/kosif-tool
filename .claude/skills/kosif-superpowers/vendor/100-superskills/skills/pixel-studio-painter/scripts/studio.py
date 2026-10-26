"""KOSIF Studio: a drawing program that paints a picture pixel by pixel.

Three ways to give it a picture:
  * a scene from scenes/ (hand-written picture programs, traced images, SVG files)
  * 📝 code from any AI: SVG, Python that draws with PIL / matplotlib / turtle, or a KOSIF scene (build() -> Steps)
  * 🖼 an image (file, or Ctrl+V of a copied picture): it is traced into vector shapes and redrawn

Whatever it is, the studio lays the changed pixels down one at a time in a painter's order (strokes for skies,
growing shapes, rising figures, sparkling details). Vector pictures (scenes, SVG, traced images) also export at
3840x2560 or any size without losing quality.

    python studio.py                      # open the studio
    python studio.py dragon_girl --speed fast
    python studio.py --code drawing.py    # draw a code file (SVG / PIL / matplotlib / turtle / KOSIF scene)
    python studio.py --image photo.jpg    # trace an image and draw it
    python studio.py dragon_girl --render out.png --scale 3.2   # no window: render a 3840x2560 PNG
"""
from __future__ import annotations

import argparse
import ctypes
import json
import os
import queue
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE / "scenes")]
import render as R  # noqa: E402

OUT, SCENES, SOURCES, CODE = HERE / "out", HERE / "scenes", HERE / "sources", HERE / "code"
PAPER = "#f3eee4"
BACKDROP = (27, 24, 34)
EXACT, VECTOR = "مطابق تماماً", "متجه قابل للتكبير"
# seconds a full-sheet step takes; smaller steps take less (time grows with the square root of their area)
SPEEDS = {"بطيء": 5.0, "عادي": 1.8, "سريع": 0.55, "فوري": 0.0}
CODE_TIMEOUT = 120
IMAGE_TYPES = (".png", ".jpg", ".jpeg", ".bmp", ".webp", ".gif", ".tif", ".tiff")
RISKY = [(r"\bos\.(remove|unlink|rmdir|removedirs|rename|replace|system|popen|kill|startfile)\b", "حذف ملفات أو تشغيل برامج"),
         (r"\bshutil\.", "نقل أو حذف ملفات"), (r"\bsubprocess\b", "تشغيل برامج"),
         (r"\b(socket|requests|urllib|http\.client|ftplib|smtplib|webbrowser)\b", "اتصال بالإنترنت"),
         (r"\b(ctypes|winreg|_winapi)\b", "وصول مباشر للنظام"), (r"\b(eval|exec|__import__|compile)\s*\(", "تنفيذ كود مخفي"),
         (r"open\([^)]*,\s*['\"](w|a|x)", "كتابة ملفات"), (r"\bpip\b|\bsys\.exit\b", "تثبيت حزم أو إنهاء البرنامج")]

AI_PROMPT = """أريد كود صورة لبرنامج رسم اسمه KOSIF Studio. أعطني كوداً واحداً كاملاً فقط، بدون أي شرح، بإحدى الصيغ:

1) الأفضل: ملف SVG كامل، viewBox="0 0 1200 800"، يبدأ بخلفية تغطي اللوحة، ثم العناصر من الخلف إلى الأمام
   (الأبعد ثم الأقرب ثم التفاصيل). استعمل path وcircle وellipse وrect وpolygon وlinearGradient وradialGradient
   والشفافية بحرية. لا تستعمل filter أو mask أو clipPath أو صوراً خارجية.

2) أو كود بايثون بمكتبة PIL فقط: img = Image.new("RGB", (1200, 800)) ثم draw = ImageDraw.Draw(img)، وارسم من
   الخلفية إلى التفاصيل بـ rectangle وellipse وpolygon وline وarc وtext، ثم img.save("out.png").

4) أو للواقعية ثلاثية الأبعاد: صفحة HTML واحدة بـ Three.js (importmap من cdn.jsdelivr.net/npm/three@0.170.0)،
   مواد MeshPhysicalMaterial (clearcoat للمبلّل، transmission للأغشية)، ضوء بارد DirectionalLight وضوء دافئ PointLight،
   FogExp2، جسيمات Points بـ AdditiveBlending للنار والشرر، UnrealBloomPass ثم OutputPass، ACESFilmicToneMapping.
   العقد: ضع window.__ready = true بعد رسم أول إطار، ودالة window.render(t) للحركة مع window.__duration بالثواني.

3) أو للمؤثرات السينمائية (توهج، إضاءة حواف، تدرجات ناعمة) كود KOSIF: دالة build() ترجع قائمة Step:
   Step("اسم الخطوة", [عمليات], "ترتيب", origin=(x, y))   الترتيب: "sweep" أو "grow" أو "rise" أو "down" أو "sparkle"
   أشكال: rect(x,y,w,h) ellipse(cx,cy,rx,ry) path("M .. C .. Z") poly([(x,y),...]) tube([(x,y),...],[r,...]) dots([(x,y,r),...])
   ألوان: "#rrggbb" أو "#rrggbbaa" أو lin((x1,y1),(x2,y2),[(0,"#..."),(1,"#...")]) أو rad((cx,cy),r,[(0,"#..."),(1,"#...")])
   عمليات: fill(shape, paint, alpha=1, blur=0, mode="normal"|"add"|"screen"|"multiply")  glow(shape, colour, radius, alpha)
           rim(shape, (dx,dy), width, colour, alpha)  text("نص", x, y, size, colour, anchor="mm", bold=False)
           shade(shape, (lx,ly), lit, dark)  تظليل حجم   noise(shape, amount, cell, seed, mode)  نسيج جلد/صخر/ماء/سحاب
           relief(shape, [(x,y,z,colour,strength),...], base, bump=..)  جسم مضاء فيزيائياً (الأهم للواقعية)
           water(area, lights, deep, sky)  سطح ماء يلمع   scales(shape, size, colour, alpha)  حراشف
           relief(..., bumps=[(amp,cell),...], sss=5, roughness=.5)  جلد حي بتفاصيل متعددة
           الكاميرا: defocus(2) بعد الخلفية، motion_blur(shape, 6, 104) للمطر، bloom(.72, 26, .5)، flare((x,y), "#ffb070", 110, 380, .45)،
           chroma(1.4)، filmic(1.0, 1.08, 1.02) مع ROLLOFF = 1.0، ثم vignette(.55) وgrain(.018)
   للواقعية: كل جسم كبير relief بأضواء المشهد، والماء water، ثلاثة أضواء (بارد ودافئ ومحيط)، البعيد مموّه وأزرق، لا خطوط خارجية سوداء،
   ثم grade وvignette وgrain. اللوحة 1200×800، والأسماء كلها جاهزة بدون import.

الصورة المطلوبة: [اكتب وصف الصورة هنا]"""


# ── scenes: picture programs on disk ─────────────────────────────────────────────────────────────────────────
def scenes() -> list[str]:
    return sorted({p.stem for p in [*SCENES.glob("*.py"), *SCENES.glob("*.json"), *SCENES.glob("*.svg"), *SCENES.glob("*.html")]
                   if not p.stem.startswith("_")})


def scene_file(name: str) -> Path | None:
    for ext in (".py", ".svg", ".json", ".html"):
        p = SCENES / f"{name}{ext}"
        if p.exists():
            return p
    return None


def load(name: str):
    """(title, steps, rolloff) for a scene drawn inside the studio, or None when it is Python that must run in
    its own process (any AI's PIL / matplotlib / turtle code)."""
    p = scene_file(name)
    if p is None:
        raise FileNotFoundError(name)
    if p.suffix == ".json":
        import vector_scene
        data = json.loads(p.read_text(encoding="utf-8"))
        return data.get("title", name), vector_scene.build(data), 1.0
    if p.suffix == ".html":
        return None                                   # rendered in headless Edge by runner.py
    if p.suffix == ".svg":
        import svg_import
        title, steps = svg_import.load_svg(p.read_text(encoding="utf-8"))
        return title if title != "SVG" else name, steps, 1.0
    src = p.read_text(encoding="utf-8-sig")
    if not re.search(r"^\s*def\s+build\s*\(", src, re.M):
        return None
    ns = {"__name__": f"scene_{name}", "__file__": str(p)}
    exec("from render import *\nimport math, random\n", ns)
    exec(compile(src, str(p), "exec"), ns)                 # read fresh every time, so edits show at once
    return ns.get("TITLE", name), ns["build"](), ns.get("ROLLOFF", 0.82)


def image_code(path: Path, title: str) -> str:
    """Code for an image: the original file's own bytes, embedded. The studio paints it from nothing and ends
    identical to the original; the code needs nothing else, so it works the same on any machine."""
    import base64
    data = Path(path).read_bytes()
    with Image.open(path) as im:
        w, h = im.size
    b64 = base64.b64encode(data).decode("ascii")
    body = "\n".join(f'    "{b64[i:i + 100]}"' for i in range(0, len(b64), 100))
    return (f"# KOSIF Studio: كود الصورة «{title}».\n"
            "# يرسمها البرنامج من ورقة فارغة بيكسلاً ببيكسل (الكتل ثم التدقيق ثم اللمسات الدقيقة)،\n"
            "# وتنتهي مطابقة للأصل تماماً. الصورة الأصلية محفوظة داخل الكود، فهو يعمل وحده على أي جهاز.\n"
            f"TITLE = {title!r}\nSIZE = ({w}, {h})\nIMAGE_B64 = (\n{body}\n)\n")


def enlarge(im: Image.Image, target: int = 3840) -> tuple[Image.Image, int]:
    """A high-resolution copy of a raster picture with its own colours: a whole-number Lanczos enlargement (the
    pixel grid stays regular) and a gentle unsharp mask to keep edges crisp. Colours are not simplified."""
    import cv2
    rgba = np.ascontiguousarray(np.asarray(im.convert("RGBA")))
    h, w = rgba.shape[:2]
    k = max(1, round(target / max(w, h)))
    if k == 1:
        return Image.fromarray(rgba, "RGBA"), 1
    big = cv2.resize(rgba, (w * k, h * k), interpolation=cv2.INTER_LANCZOS4)
    rgb = big[..., :3]
    big[..., :3] = cv2.addWeighted(rgb, 1.35, cv2.GaussianBlur(rgb, (0, 0), .6 * k), -.35, 0)
    return Image.fromarray(big, "RGBA"), k


def extract_code(text: str) -> str:
    """The code in whatever was pasted: an AI reply with explanations around a ``` block, the whole 🧩 package
    (its program is the block), or bare code with or without fences."""
    text = text.strip()
    blocks = re.findall(r"```[\w+-]*[ \t]*\r?\n(.*?)\r?\n[ \t]*```", text, re.S)
    if blocks:
        return next((b for b in blocks if "IMAGE_B64" in b or re.search(r"^\s*(import|from)\s", b, re.M)
                     or b.lstrip().startswith("<")), blocks[-1]).strip()
    return re.sub(r"^```[\w+-]*\s*\n|\n```\s*$", "", text).strip()


def risky(code: str) -> list[str]:
    if code.lstrip().startswith("<"):
        return []                                         # SVG is data, not code
    return sorted({why for pat, why in RISKY if re.search(pat, code)})


# ── paint jobs: one per step, the changed pixels in painting order ───────────────────────────────────────────
class Job:
    __slots__ = ("i", "step", "order", "cols", "pos", "t0", "dur")

    def __init__(self, i, step, order, cols):
        self.i, self.step, self.order, self.cols = i, step, order, cols
        self.pos, self.t0, self.dur = 0, 0.0, 0.0


def produce(steps, scale: float, out: queue.Queue, stop: threading.Event, rolloff: float = 0.82):
    """Render a picture program inside the studio and turn each step into the pixels to lay down."""
    prev = None
    try:
        for i, st, img in R.render(steps, scale, ss=3, paper=PAPER, rolloff=rolloff):
            if stop.is_set():
                return
            flat = img.reshape(-1, 3)
            if prev is None:
                prev = np.empty_like(flat)
                prev[:] = (R.rgb(PAPER) * 255 + .5).astype(np.uint8)
            idx = np.flatnonzero(np.any(flat != prev, axis=1)).astype(np.int32)
            order = R.reveal_order(idx, img.shape[1], st, scale, seed=i)
            out.put(Job(i, st, order, flat[order].copy()))
            prev = flat.copy()
    except Exception as e:
        out.put(("error", f"{type(e).__name__}: {e}"))
    finally:
        out.put(None)


def produce_exact(rgba: np.ndarray, out: queue.Queue, stop: threading.Event):
    """Paint an image from nothing at its own resolution; the last job leaves it identical to the original."""
    import exact
    i = -1
    try:
        out.put(("status", "🧠 يقيس خطط الرسم الممكنة ويسأل Jev عن أفضلها..."))
        block_k, fine_k, info = exact.choose_plan(rgba)          # photos: Jev chooses; logos keep their colours
        if info:
            out.put(("plan", info))
        for i, (label, kind, origin, weight, order, cols) in enumerate(exact.plan(rgba, block_k, fine_k)):
            if stop.is_set():
                return
            out.put(Job(i, R.Step(label, [], kind, origin, weight), order, cols))
        out.put(("done", {"jobs": i + 1}))
    except Exception as e:
        out.put(("error", f"{type(e).__name__}: {e}"))
    finally:
        out.put(None)


def produce_code(code_file: Path, scale: float, out: queue.Queue, stop: threading.Event):
    """Run code in its own process (runner.py) and stream its paint jobs as they are written."""
    work = Path(tempfile.mkdtemp(prefix="kosif_run_"))
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    proc = subprocess.Popen([sys.executable, str(HERE / "runner.py"), str(code_file), str(work), "--scale", str(scale)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, creationflags=flags)
    n, t0, canvas_sent = 0, time.time(), False
    try:
        while not stop.is_set():
            if not canvas_sent and (work / "canvas.json").exists():
                c = json.loads((work / "canvas.json").read_text(encoding="utf-8"))
                out.put(("canvas", (c["w"], c["h"])))
                canvas_sent = True
            job = work / f"job_{n:04d}.npz"
            if job.exists():
                meta = json.loads((work / f"job_{n:04d}.json").read_text(encoding="utf-8"))
                with np.load(job) as z:
                    order, cols = z["order"], z["cols"]
                st = R.Step(meta["label"], [], meta["order"], tuple(meta["origin"]) if meta["origin"] else None,
                            meta["weight"])
                out.put(Job(n, st, order, cols))
                n += 1
                continue
            if (work / "error.txt").exists():
                out.put(("error", (work / "error.txt").read_text(encoding="utf-8")))
                return
            if (work / "done.json").exists():
                if not (work / f"job_{n:04d}.npz").exists():
                    if (work / "final.png").exists():
                        out.put(("reference", np.asarray(Image.open(work / "final.png").convert("RGBA")).copy()))
                    out.put(("done", json.loads((work / "done.json").read_text(encoding="utf-8"))))
                    return
                continue
            if proc.poll() is not None:
                time.sleep(.1)
                if not any((work / f).exists() for f in ("done.json", "error.txt")) and \
                        not (work / f"job_{n:04d}.npz").exists():
                    err = proc.stderr.read().decode("utf-8", "replace") if proc.stderr else ""
                    out.put(("error", err or f"the code process ended (exit code {proc.returncode})"))
                    return
            if time.time() - t0 > CODE_TIMEOUT:
                proc.kill()
                out.put(("error", f"الكود تجاوز {CODE_TIMEOUT} ثانية فأُوقف."))
                return
            time.sleep(.03)
    finally:
        if proc.poll() is None:
            proc.kill()
        out.put(None)
        shutil.rmtree(work, ignore_errors=True)


# ── the window ─────────────────────────────────────────────────────────────────────────────────────────────
class Studio:
    def __init__(self, scene: str, speed: str, scale: float = 1.0):
        import tkinter as tk
        from tkinter import ttk
        from PIL import ImageTk
        self.tk, self.ttk = tk, ttk
        self.scale = scale
        self.W, self.H = round(R.W0 * scale), round(R.H0 * scale)
        self.root = tk.Tk()
        self.root.title("KOSIF Studio — رسم بالبيكسل")
        self.root.configure(bg="#16141c")
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TButton", padding=(10, 4))

        self.scene = tk.StringVar(value=scene)
        self.speed = tk.StringVar(value=speed)
        self.image_mode = tk.StringVar(value=EXACT)
        self._build_menu()
        self._build_bar()

        self.cv = tk.Canvas(self.root, width=self.W, height=self.H, bg=PAPER, highlightthickness=0)
        self.cv.pack(padx=8, pady=(2, 0))
        self.disp = np.empty((self.H, self.W, 3), np.uint8)
        self.photo = ImageTk.PhotoImage(Image.new("RGB", (self.W, self.H), PAPER))
        self.cv.create_image(0, 0, image=self.photo, anchor="nw")
        self.brush = self.cv.create_oval(-20, -20, -10, -10, outline="#ffffff", width=2)
        self.brush_in = self.cv.create_oval(-20, -20, -10, -10, outline="#1a1420", width=1)

        self.info = tk.StringVar(value="")
        tk.Label(self.root, textvariable=self.info, fg="#9fe0b5", bg="#16141c", anchor="e",
                 font=("Segoe UI", 11, "bold")).pack(fill="x", padx=10, pady=(2, 0))
        self.status = tk.StringVar(value="")
        tk.Label(self.root, textvariable=self.status, fg="#e9e2f5", bg="#16141c", anchor="e",
                 font=("Segoe UI", 11)).pack(fill="x", padx=10, pady=(0, 4))
        for keys, fn in (("<Control-v>", self.paste_any), ("<Control-V>", self.paste_any), ("<Control-o>", self.open_image),
                         ("<Control-s>", self.save_png), ("<F5>", self.redraw), ("<Control-e>", self.edit_with_ai),
                         ("<Control-g>", self.picture_from_prompt), ("<Control-z>", self.undo), ("<Control-k>", self.open_code)):
            self.root.bind(keys, lambda e, fn=fn: fn())

        self.q: queue.Queue = queue.Queue(maxsize=6)
        self.stop = threading.Event()
        self.job = None
        self.paused = False
        self.drawn, self.t_start, self.steps_total = 0, 0.0, 0
        self.source = ("scene", scene)                     # what is being drawn: a scene, a code file, an image
        self.native = None                                 # an image painted at its own resolution
        self.reference = None                              # what that image must end up identical to
        self.code_win = None
        self.original = None                               # the image file behind the current picture, if any
        self.history: list[Path] = []                      # pictures before each 🧩 edit, for ↩
        self.busy = False                                  # something is being drawn right now
        self.pending_note = ""                             # shown with the next "finished" message
        self.last_info: dict = {}
        if scene:
            self.root.after(300, self.start)

    def _build_menu(self):
        tk = self.tk
        m = tk.Menu(self.root)
        f = tk.Menu(m, tearoff=0)
        f.add_command(label="فتح صورة…", accelerator="Ctrl+O", command=self.open_image)
        f.add_command(label="لصق صورة أو كود من الحافظة", accelerator="Ctrl+V", command=self.paste_any)
        f.add_command(label="فتح ملف كود…", command=lambda: (self.open_code(), self.open_code_file()))
        f.add_separator()
        f.add_command(label="حفظ PNG", accelerator="Ctrl+S", command=self.save_png)
        f.add_command(label="تصدير عالي الدقة (3840×2560)", command=self.export_big)
        f.add_command(label="كود الصورة (برنامج بايثون مستقل)", command=self.export_image_code)
        f.add_command(label="فيلم الرسم (MP4)", command=self.make_film)
        f.add_separator()
        f.add_command(label="خروج", command=self.root.destroy)
        m.add_cascade(label="ملف", menu=f)
        d = tk.Menu(m, tearoff=0)
        d.add_command(label="ارسم", accelerator="F5", command=self.redraw)
        d.add_command(label="إيقاف / متابعة", command=self.toggle_pause)
        sp = tk.Menu(d, tearoff=0)
        for name in SPEEDS:
            sp.add_radiobutton(label=name, variable=self.speed, value=name)
        d.add_cascade(label="السرعة", menu=sp)
        md = tk.Menu(d, tearoff=0)
        for name in (EXACT, VECTOR):
            md.add_radiobutton(label=name, variable=self.image_mode, value=name)
        d.add_cascade(label="طريقة رسم الصور", menu=md)
        m.add_cascade(label="رسم", menu=d)
        ai = tk.Menu(m, tearoff=0)
        ai.add_command(label="🧩 عدّل الصورة…", accelerator="Ctrl+E", command=self.edit_with_ai)
        ai.add_command(label="🤖 صورة من وصف…", accelerator="Ctrl+G", command=self.picture_from_prompt)
        ai.add_command(label="↩ تراجع عن آخر تعديل", accelerator="Ctrl+Z", command=self.undo)
        ai.add_separator()
        ai.add_command(label="📝 لوحة الكود", accelerator="Ctrl+K", command=self.open_code)
        ai.add_command(label="انسخ تعليمات لأي ذكاء اصطناعي", command=self.copy_ai_prompt)
        ai.add_command(label="⚙ إعداد الذكاء الاصطناعي…", command=self.ai_settings)
        m.add_cascade(label="ذكاء اصطناعي", menu=ai)
        mo = tk.Menu(m, tearoff=0)
        mo.add_command(label="🎬 مشروع أنيميشن جديد (مسطّح)…", command=lambda: self.motion_new(False))
        mo.add_command(label="🎬 مشروع أنيميشن جديد (ثلاثي الأبعاد)…", command=lambda: self.motion_new(True))
        mo.add_separator()
        mo.add_command(label="🖼 إطار مفتاحي من مشروع… (يُرسم هنا)", command=self.motion_frame)
        mo.add_command(label="🎞 تصيير فيلم المشروع…", command=self.motion_render)
        mo.add_separator()
        mo.add_command(label="🧪 فحص المشروع (حتمية وعقد وذوق)…", command=self.motion_lint)
        mo.add_command(label="🔍 لوحة نقد لفيلم (اتصال + هاتف + review.md)…", command=lambda: self.motion_film_tool("sheet"))
        mo.add_command(label="📏 قياس السرعة بالبكسل/إطار لفيلم…", command=lambda: self.motion_film_tool("speed"))
        mo.add_command(label="🎼 شبكة إيقاع من مقطوعة…", command=lambda: self.motion_film_tool("beats"))
        mo.add_command(label="🎓 دراسة فيلم مرجعي (قطعات، لقطات، لوحة)…", command=lambda: self.motion_film_tool("study"))
        mo.add_command(label="📂 فتح مجلد المشاريع", command=lambda: os.startfile(str(HERE / "motion" / "projects")) if (HERE / "motion" / "projects").exists() else None)
        m.add_cascade(label="أنيميشن", menu=mo)
        h = tk.Menu(m, tearoff=0)
        h.add_command(label="دليل سريع", accelerator="F1", command=self.show_help)
        m.add_cascade(label="مساعدة", menu=h)
        self.root.config(menu=m)
        self.root.bind("<F1>", lambda e: self.show_help())

    def _build_bar(self):
        """Two rows of groups: source · drawing, then AI · export — the window stays as wide as the canvas."""
        tk, ttk = self.tk, self.ttk
        rows = [tk.Frame(self.root, bg="#16141c") for _ in range(2)]
        rows[0].pack(fill="x", padx=8, pady=(4, 0))
        rows[1].pack(fill="x", padx=8, pady=(2, 2))

        def group(row, title):
            g = tk.Frame(row, bg="#16141c")
            g.pack(side="left", padx=(0, 10))
            tk.Label(g, text=title, fg="#7d7592", bg="#16141c", font=("Segoe UI", 8)).pack(side="right", padx=(6, 0))
            return g
        g = group(rows[0], "المصدر")
        self.scene_box = ttk.Combobox(g, textvariable=self.scene, values=scenes(), width=14, state="readonly")
        self.scene_box.pack(side="left")
        self.scene_box.bind("<<ComboboxSelected>>", lambda e: self.start())
        ttk.Button(g, text="🖼  صورة", command=self.open_image).pack(side="left", padx=2)
        ttk.Button(g, text="📝  كود", command=self.open_code).pack(side="left", padx=2)
        ttk.Combobox(g, textvariable=self.image_mode, values=[EXACT, VECTOR], width=13, state="readonly").pack(side="left", padx=2)
        g = group(rows[0], "الرسم")
        ttk.Button(g, text="▶  ارسم", command=self.redraw).pack(side="left", padx=2)
        self.pause_btn = ttk.Button(g, text="⏸", width=3, command=self.toggle_pause)
        self.pause_btn.pack(side="left", padx=2)
        ttk.Combobox(g, textvariable=self.speed, values=list(SPEEDS), width=6, state="readonly").pack(side="left", padx=2)
        ttk.Button(rows[0], text="❓", width=3, command=self.show_help).pack(side="right", padx=2)
        g = group(rows[1], "الذكاء الاصطناعي")
        ttk.Button(g, text="🧩  عدّل الصورة", command=self.edit_with_ai).pack(side="left", padx=2)
        ttk.Button(g, text="🤖  صورة من وصف", command=self.picture_from_prompt).pack(side="left", padx=2)
        self.undo_btn = ttk.Button(g, text="↩  تراجع", command=self.undo, state="disabled")
        self.undo_btn.pack(side="left", padx=2)
        ttk.Button(g, text="⚙", width=3, command=self.ai_settings).pack(side="left", padx=2)
        g = group(rows[1], "التصدير")
        ttk.Button(g, text="💾  PNG", command=self.save_png).pack(side="left", padx=2)
        ttk.Button(g, text="⤢  دقة عالية", command=self.export_big).pack(side="left", padx=2)
        ttk.Button(g, text="📤  كود الصورة", command=self.export_image_code).pack(side="left", padx=2)
        ttk.Button(g, text="🎬  فيلم", command=self.make_film).pack(side="left", padx=2)

    # ── drawing ──────────────────────────────────────────────────────────────────────────────────────────────
    def redraw(self):
        if self.source[0] == "code":
            self.start_code(self.source[1])
        elif self.source[0] == "image":
            self.start_exact(*self.source[1:])
        else:
            self.start()

    def _reset(self, title: str, total: int, canvas: tuple[int, int] | None = None):
        self.stop.set()
        self.stop = threading.Event()
        self.q = queue.Queue(maxsize=6)
        self.title, self.steps_total = title, total
        self.disp[:] = (R.rgb(PAPER) * 255 + .5).astype(np.uint8)
        self.flat = self.disp.reshape(-1, 3)
        self.photo.paste(Image.fromarray(self.disp))
        self.job, self.paused, self.drawn = None, False, 0
        self.pause_btn.configure(text="⏸  إيقاف")
        self.t_start = time.perf_counter()
        self.last_info = {}
        self.native, self.reference = None, None
        self.busy = True
        self.info.set("")
        if canvas:
            self.set_native(*canvas)

    def set_native(self, w: int, h: int):
        """Paint on a w x h canvas at its own resolution (nothing resampled), shown fitted into the window."""
        f = min(self.W / w, self.H / h)
        f = float(int(f)) if f >= 2 else f                 # small images: a whole-number zoom keeps pixels square
        dw, dh = max(1, round(w * f)), max(1, round(h * f))
        ox, oy = (self.W - dw) // 2, (self.H - dh) // 2
        xs = np.minimum((np.arange(dw) / f).astype(np.int64), w - 1)
        ys = np.minimum((np.arange(dh) / f).astype(np.int64), h - 1)
        self.native = {"w": w, "h": h, "f": f, "ox": ox, "oy": oy, "dw": dw, "dh": dh,
                       "map": (ys[:, None] * w + xs[None, :]).reshape(-1), "canvas": np.zeros((w * h, 4), np.uint8)}
        self.disp[:] = BACKDROP
        self.refresh_native()

    def refresh_native(self, final: bool = False):
        """Show the native canvas fitted to the window the way image viewers do: shrinking averages the pixels
        (no jagged edges), small pictures zoom by whole numbers (crisp pixels). Very large pictures use the fast
        nearest-pixel view while drawing and the smooth one at the end."""
        import cv2
        nv = self.native
        if nv["w"] * nv["h"] <= 4_000_000 or final:
            can = nv["canvas"].reshape(nv["h"], nv["w"], 4).astype(np.float32)
            a = can[..., 3:4] / 255
            rgb = can[..., :3] * a + R.rgb(PAPER) * 255 * (1 - a)       # see-through pixels show the paper
            if (nv["dw"], nv["dh"]) != (nv["w"], nv["h"]):
                interp = cv2.INTER_AREA if nv["f"] < 1 else cv2.INTER_NEAREST if nv["f"] >= 2 else cv2.INTER_CUBIC
                rgb = cv2.resize(rgb, (nv["dw"], nv["dh"]), interpolation=interp)
            view = np.clip(rgb + .5, 0, 255).astype(np.uint8)
        else:
            sub = nv["canvas"][nv["map"]].astype(np.float32)
            a = sub[:, 3:4] / 255
            view = (sub[:, :3] * a + R.rgb(PAPER) * 255 * (1 - a) + .5).astype(np.uint8).reshape(nv["dh"], nv["dw"], 3)
        self.disp[nv["oy"]:nv["oy"] + nv["dh"], nv["ox"]:nv["ox"] + nv["dw"]] = view
        self.photo.paste(Image.fromarray(self.disp))

    def start_exact(self, src: Path, name: str):
        import exact
        self.source = ("image", src, name)
        rgba = exact.load_rgba(src)
        h, w = rgba.shape[:2]
        self._reset(f"{name} ({w}×{h})", 0, canvas=(w, h))
        self.reference = rgba
        self.status.set("يرسم الصورة من الصفر ليطابق الأصل تماماً...")
        threading.Thread(target=produce_exact, args=(rgba, self.q, self.stop), daemon=True).start()
        self.root.after(1, self.tick)

    def start(self):
        name = self.scene.get()
        self.source = ("scene", name)
        try:
            loaded = load(name)
        except Exception as e:
            self.status.set(f"تعذّر فتح المشهد {name}: {e}")
            return
        if loaded is None:                                  # plain Python from an AI: run it in its own process
            self.start_code(scene_file(name), keep_source=False)
            self.source = ("scene", name)
            return
        title, steps, rolloff = loaded
        self._reset(title, len(steps))
        threading.Thread(target=produce, args=(steps, self.scale, self.q, self.stop, rolloff), daemon=True).start()
        self.root.after(1, self.tick)

    def start_code(self, code_file: Path, keep_source: bool = True):
        if keep_source:
            self.source = ("code", code_file)
        self._reset("كود", 0)
        self.status.set("يشغّل الكود...")
        threading.Thread(target=produce_code, args=(Path(code_file), self.scale, self.q, self.stop),
                         daemon=True).start()
        self.root.after(1, self.tick)

    def toggle_pause(self):
        self.paused = not self.paused
        self.pause_btn.configure(text="▶  متابعة" if self.paused else "⏸  إيقاف")
        if not self.paused and self.job:
            self.job.t0 = time.perf_counter() - self.job.dur * self.job.pos / max(1, len(self.job.order))

    def tick(self):
        if self.paused:
            self.root.after(50, self.tick)
            return
        now = time.perf_counter()
        if self.job is None:
            try:
                item = self.q.get_nowait()
            except queue.Empty:
                self.root.after(10, self.tick)
                return
            if item is None:                                # the picture is finished
                self.finish()
                return
            if isinstance(item, tuple):
                kind, val = item
                if kind == "done":
                    self.last_info = val
                    p = val.get("plan")
                    if p and p.get("candidate"):
                        c = p["candidate"]
                        who = (f"ثقة Jev {round(p['probabilities'][p['choice']] * 100)}٪"
                               if p["by"] == "jev" else "بالقاعدة: Jev غير متاح")
                        self.info.set(f"🧠 الخطة: {c['block_colours']} لوناً ثم {c['refine_tones']} درجة ({who})")
                    self.title, self.steps_total = val.get("title", self.title), val.get("jobs", self.steps_total)
                elif kind == "canvas":
                    self.set_native(*val)
                elif kind == "reference":
                    self.reference = val
                elif kind == "status":
                    self.status.set(val)
                elif kind == "plan":
                    c = val["candidates"][val["choice"]]
                    who = (f"ثقة Jev {round(val['probabilities'][val['choice']] * 100)}٪"
                           if val["by"] == "jev" else "بالقاعدة: Jev غير متاح")
                    self.info.set(f"🧠 الخطة: {c['block_colours']} لوناً ثم {c['refine_tones']} درجة ({who})")
                else:
                    self.show_error(val)
                self.root.after(1, self.tick)
                return
            self.job = item
            n = len(self.job.order)
            k = SPEEDS.get(self.speed.get(), 1.8)
            area = self.native["w"] * self.native["h"] if self.native else self.W * self.H
            self.job.dur = k * self.job.step.weight * (n / area) ** .5
            self.job.t0 = now
        j = self.job
        n = len(j.order)
        target = n if j.dur <= 0 else min(n, int(n * (now - j.t0) / j.dur))
        if target > j.pos:
            sel = j.order[j.pos:target]
            last = int(sel[-1])
            if self.native is None:
                self.flat[sel] = j.cols[j.pos:target]
                x, y = last % self.W, last // self.W
                self.photo.paste(Image.fromarray(self.disp))
            else:
                nv = self.native
                cols = j.cols[j.pos:target]
                nv["canvas"][sel] = cols if cols.shape[1] == 4 else np.column_stack([cols, np.full(len(cols), 255,
                                                                                                    np.uint8)])
                x = nv["ox"] + (last % nv["w"] + .5) * nv["f"]
                y = nv["oy"] + (last // nv["w"] + .5) * nv["f"]
                self.refresh_native()
            self.drawn += target - j.pos
            j.pos = target
            self.cv.coords(self.brush, x - 7, y - 7, x + 7, y + 7)
            self.cv.coords(self.brush_in, x - 5, y - 5, x + 5, y + 5)
        total = f"/{self.steps_total}" if self.steps_total else ""
        self.status.set(f"{self.title}   ·   الخطوة {j.i + 1}{total}: {j.step.label}   ·   "
                        f"{self.drawn:,} بيكسل مرسوم   ·   {now - self.t_start:.1f} ث")
        if j.pos >= n:
            self.job = None
            self.root.after(1, self.tick)
        else:
            self.root.after(12, self.tick)

    def finish(self):
        self.cv.coords(self.brush, -20, -20, -10, -10)
        self.cv.coords(self.brush_in, -20, -20, -10, -10)
        self.photo.paste(Image.fromarray(self.disp))
        self.busy = False
        if getattr(self, "error_shown", False):
            self.error_shown = False
            return
        secs = time.perf_counter() - self.t_start
        steps = self.steps_total or (self.job.i + 1 if self.job else 0)
        note, self.pending_note = self.pending_note, ""
        msg = ((note + "   ·   ") if note else "") + (f"{self.title}   ·   اكتملت الرسمة: {self.drawn:,} بيكسل في {secs:.1f} ثانية"
               + (f"   ·   {steps} خطوة" if steps else ""))
        OUT.mkdir(exist_ok=True)
        if self.native is None:
            Image.fromarray(self.disp).save(OUT / f"{self.out_name()}_{self.W}x{self.H}.png")
        else:
            nv = self.native
            self.refresh_native(final=True)
            img = nv["canvas"].reshape(nv["h"], nv["w"], 4)
            Image.fromarray(img, "RGBA").save(OUT / f"{self.out_name()}_exact.png")
            if self.reference is not None and self.reference.shape == img.shape:
                import exact
                bad = exact.mismatches(img, self.reference)
                total = nv["w"] * nv["h"]
                plan = self.info.get()
                self.info.set((f"✅ مطابقة للأصل تماماً ({total:,} بيكسل)" if bad == 0 else
                               f"⚠ {bad:,} بيكسل يختلف عن الأصل") + (f"   ·   {plan[2:]}" if plan else ""))
        self.status.set(msg)

    def out_name(self) -> str:
        return {"code": "code", "image": self.source[-1]}.get(self.source[0], self.scene.get())

    def show_error(self, msg: str):
        self.error_shown = True
        self.busy = False
        self.pending_note = ""
        last = [ln for ln in msg.strip().splitlines() if ln.strip()][-1:] or [msg]
        self.status.set(f"⚠ الكود فيه خطأ: {last[0][:150]}")
        if self.code_win is not None and self.code_win.winfo_exists():
            self.err_box.configure(state="normal")
            self.err_box.delete("1.0", "end")
            self.err_box.insert("1.0", msg)
            self.err_box.configure(state="disabled")

    # ── code from any AI ───────────────────────────────────────────────────────────────────────────────────
    def open_code(self, text: str | None = None, run: bool = False):
        tk, ttk = self.tk, self.ttk
        if self.code_win is None or not self.code_win.winfo_exists():
            w = self.code_win = tk.Toplevel(self.root)
            w.title("📝 كود الصورة — الصق كود أي ذكاء اصطناعي")
            w.configure(bg="#16141c")
            tk.Label(w, text="الصق كود الصورة من أي ذكاء اصطناعي، ثم اضغط «ارسم الكود»", fg="#e9e2f5",
                     bg="#16141c", font=("Segoe UI", 11), anchor="e").pack(fill="x", padx=10, pady=(8, 0))
            tk.Label(w, text="SVG   ·   Python: PIL / matplotlib / turtle   ·   KOSIF scene: build()   ·   Ctrl+Enter",
                     fg="#9f97b3", bg="#16141c", font=("Segoe UI", 9), anchor="e").pack(fill="x", padx=10, pady=(0, 4))
            row = tk.Frame(w, bg="#16141c")
            row.pack(fill="x", padx=8, pady=4)
            ttk.Button(row, text="▶  ارسم الكود", command=self.run_code).pack(side="right", padx=2)
            ttk.Button(row, text="📋  لصق", command=self.paste_code).pack(side="right", padx=2)
            ttk.Button(row, text="📄  نسخ الكود", command=self.copy_code).pack(side="right", padx=2)
            ttk.Button(row, text="💾  حفظ ملفاً", command=self.save_code_file).pack(side="right", padx=2)
            ttk.Button(row, text="📂  فتح ملف", command=self.open_code_file).pack(side="right", padx=2)
            ttk.Button(row, text="💾  حفظ كمشهد", command=self.save_code_as_scene).pack(side="right", padx=2)
            ttk.Button(row, text="🧹  مسح", command=lambda: self.code_text.delete("1.0", "end")).pack(side="right", padx=2)
            ttk.Button(row, text="🤖  انسخ تعليمات للذكاء الاصطناعي", command=self.copy_ai_prompt).pack(side="left", padx=2)
            ttk.Button(row, text="🧩  عدّل الصورة", command=self.edit_with_ai).pack(side="left", padx=2)
            ex = sorted(p.name for p in (HERE / "examples").glob("*") if p.suffix in (".py", ".svg"))
            if ex:
                self.example = tk.StringVar(value="أمثلة…")
                cb = ttk.Combobox(row, textvariable=self.example, values=ex, width=22, state="readonly")
                cb.pack(side="left", padx=6)
                cb.bind("<<ComboboxSelected>>", lambda e: self.load_code_text(
                    (HERE / "examples" / self.example.get()).read_text(encoding="utf-8")))
            body = tk.Frame(w, bg="#16141c")
            body.pack(fill="both", expand=True, padx=8)
            self.code_text = tk.Text(body, width=100, height=30, wrap="none", undo=True, font=("Consolas", 11),
                                     bg="#100e15", fg="#e8e3f2", insertbackground="#ffffff", relief="flat")
            ys = ttk.Scrollbar(body, orient="vertical", command=self.code_text.yview)
            xs = ttk.Scrollbar(body, orient="horizontal", command=self.code_text.xview)
            self.code_text.configure(yscrollcommand=ys.set, xscrollcommand=xs.set)
            ys.pack(side="right", fill="y")
            xs.pack(side="bottom", fill="x")
            self.code_text.pack(side="left", fill="both", expand=True)
            self.err_box = tk.Text(w, height=6, wrap="word", font=("Consolas", 10), bg="#1d1218", fg="#ff9a9a",
                                   relief="flat", state="disabled")
            self.err_box.pack(fill="x", padx=8, pady=(4, 8))
            self.code_text.bind("<Control-Return>", lambda e: (self.run_code(), "break")[1])
            self.code_text.bind("<Control-a>", lambda e: (self.code_text.tag_add("sel", "1.0", "end-1c"), "break")[1])
            self.code_text.bind("<Control-A>", lambda e: (self.code_text.tag_add("sel", "1.0", "end-1c"), "break")[1])
            w.geometry("+%d+%d" % (self.root.winfo_rootx() + 60, self.root.winfo_rooty() + 80))
        self.code_win.deiconify()
        self.code_win.lift()
        if text is not None:
            self.load_code_text(text)
        if run:
            self.run_code()

    def load_code_text(self, text: str):
        self.code_text.delete("1.0", "end")
        self.code_text.insert("1.0", text)

    def copy_code(self):
        """📄: the whole code to the clipboard (the file stays on disk too)."""
        code = self.code_text.get("1.0", "end-1c")
        if not code.strip():
            self.status.set("لا يوجد كود لنسخه.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(code)
        self.root.update()                                  # hand the clipboard over before anything else runs
        self.status.set(f"📄 نُسخ الكود إلى الحافظة ({len(code):,} حرفاً، {len(code) // 1024:,} ك.ب).")

    def save_code_file(self):
        from tkinter import filedialog
        code = self.code_text.get("1.0", "end-1c")
        if not code.strip():
            return
        low = code.lstrip()[:4000].lower()
        ext = ".html" if low.startswith("<") and ("<!doctype html" in low or "<html" in low) else ".svg" if low.startswith("<") else ".py"
        p = filedialog.asksaveasfilename(defaultextension=ext, initialdir=OUT, initialfile=f"code{ext}",
                                         filetypes=[("كود", f"*{ext}"), ("الكل", "*.*")], parent=self.code_win)
        if p:
            Path(p).write_text(code, encoding="utf-8")
            self.status.set(f"💾 حُفظ الكود: {p}")

    def paste_code(self):
        try:
            self.load_code_text(self.root.clipboard_get())
        except self.tk.TclError:
            self.status.set("الحافظة لا تحتوي نصاً.")

    def open_code_file(self):
        from tkinter import filedialog
        p = filedialog.askopenfilename(filetypes=[("كود صورة", "*.py *.svg *.html *.txt"), ("الكل", "*.*")])
        if p:
            self.load_code_text(Path(p).read_text(encoding="utf-8-sig", errors="replace"))

    def copy_ai_prompt(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(AI_PROMPT)
        self.status.set("نُسخت التعليمات: الصقها في أي ذكاء اصطناعي، واكتب وصف صورتك مكان [اكتب وصف الصورة هنا]، "
                        "ثم الصق الكود الذي يعطيك إياه هنا.")

    def _clean_code(self, code: str) -> str | None:
        """Strip the ``` fences AIs add, and put the original image back in place of an edit-program key."""
        import edit_pack
        code = extract_code(code)
        try:
            code, restored = edit_pack.restore(code)
        except FileNotFoundError as e:
            self.status.set(f"⚠ {e}")
            return None
        if restored:
            self.status.set("🧩 أُعيدت الصورة الأصلية إلى برنامج التعديل.")
        return code

    def current_picture(self) -> Path | None:
        """The picture on the canvas as a file at its own resolution: the opened image, the result of a code run
        (the native canvas, pixel for pixel), or a drawn scene. None while drawing or when nothing is drawn."""
        if self.busy:
            return None
        if self.source[0] == "image" and self.original and Path(self.original).exists():
            return Path(self.original)
        SOURCES.mkdir(exist_ok=True)
        if self.native is not None:
            nv = self.native
            src = SOURCES / time.strftime("edit_%Y%m%d_%H%M%S.png")
            Image.fromarray(nv["canvas"].reshape(nv["h"], nv["w"], 4), "RGBA").convert("RGB").save(src)
            return src
        if self.drawn > 0:                                 # a scene is drawn at the window's size, which is its size
            src = SOURCES / f"{self.out_name()}_canvas.png"
            Image.fromarray(self.disp, "RGB").save(src)
            return src
        return None

    def _manual_ai(self, text: str, program: str | None, title: str, steps: str):
        """No AI is connected: the text goes to the clipboard, the panel opens, and the steps are shown."""
        from tkinter import messagebox
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()
        self.open_code(program)
        self.status.set(f"نُسخ النص ({len(text):,} حرفاً). الصقه في Claude أو أي ذكاء اصطناعي، ثم الصق ردّه في اللوحة واضغط «ارسم الكود».")
        messagebox.showinfo(title, steps + "\n\nليتم ذلك تلقائياً: افتح طرفية واكتب  claude  ثم  /login  مرة واحدة "
                            "(أو ضع مفتاح API في ⚙)، ثم أعد فتح الاستوديو.", parent=self.root)

    def edit_with_ai(self):
        """🧩: say what should change. The studio describes the picture and writes the edit program; colour changes
        are done locally at once, anything else is asked of Claude (CLI or API); without either, the package is
        copied for the user to paste into any AI. The result is drawn: the original first, then the edit."""
        from tkinter import filedialog, simpledialog
        import ai_bridge
        import edit_pack
        if self.busy:
            self.status.set("انتظر حتى تكتمل الرسمة الحالية.")
            return
        src = self.current_picture()
        if src is None:
            p = filedialog.askopenfilename(title="اختر الصورة التي تريد تعديلها",
                                           filetypes=[("صور", " ".join("*" + e for e in IMAGE_TYPES)), ("الكل", "*.*")])
            if not p:
                return
            src = Path(p)
        req = simpledialog.askstring("🧩 عدّل الصورة", "ما التعديل الذي تريده؟\nمثلاً: غيّر لون القميص إلى الأحمر، أو: اجعل الخلفية أفتح",
                                     parent=self.root)
        if not req or not req.strip():
            return
        req = req.strip()
        name = re.sub(r"[^\w-]+", "_", Path(src).stem) or "image"
        self.status.set("🧩 يصف الصورة ويحضّر برنامج التعديل...")

        def work():
            try:
                program, _ = edit_pack.edit_program(src, name)
                local = edit_pack.local_edit(src, req)
                if local:
                    code, how = edit_pack.with_edits(program, local[0]), f"محلياً ({local[1]})"
                elif ai_bridge.backend():
                    self.root.after(0, lambda: self.status.set("🧩 يسأل Claude عن التعديل... (قد يستغرق نحو دقيقة)"))
                    reply = ai_bridge.ask(edit_pack.package(src, name, req))
                    code = extract_code(reply)
                    if "IMAGE_B64" not in code or "# EDITS START" not in code:
                        raise RuntimeError("ردّ الذكاء الاصطناعي لم يحتوِ برنامج التعديل")
                    how = "بواسطة Claude"
                else:
                    pack = edit_pack.package(src, name, req)
                    self.root.after(0, lambda: self._manual_ai(
                        pack, program, "🧩 التعديل بالذكاء الاصطناعي",
                        "لا يوجد ذكاء اصطناعي متصل بالاستوديو، فالخطوات يدوية:\n"
                        "1) نُسخت حزمة التعديل إلى الحافظة.\n2) الصقها في Claude (أو أي ذكاء اصطناعي).\n"
                        "3) انسخ ردّه كله.\n4) اضغط «📋 لصق» في لوحة الكود ثم «▶ ارسم الكود»."))
                    return
            except Exception as e:
                self.root.after(0, lambda e=e: self.status.set(f"تعذّر التعديل: {e}"))
                return

            def go():
                self.history.append(Path(src))
                self.undo_btn.configure(state="normal")
                self.run_code_text(code, f"🧩 {req[:40]} — {how}")
            self.root.after(0, go)
        threading.Thread(target=work, daemon=True).start()

    def picture_from_prompt(self):
        """🤖: describe a picture; Claude writes its code (SVG / PIL / scene) and the studio draws it."""
        from tkinter import simpledialog
        import ai_bridge
        if self.busy:
            self.status.set("انتظر حتى تكتمل الرسمة الحالية.")
            return
        desc = simpledialog.askstring("🤖 صورة من وصف", "صف الصورة التي تريدها (بالعربية أو الإنجليزية):", parent=self.root)
        if not desc or not desc.strip():
            return
        prompt = AI_PROMPT.replace("[اكتب وصف الصورة هنا]", desc.strip())
        if not ai_bridge.backend():
            self._manual_ai(prompt, None, "🤖 صورة من وصف",
                            "لا يوجد ذكاء اصطناعي متصل بالاستوديو، فالخطوات يدوية:\n1) نُسخ الطلب إلى الحافظة.\n"
                            "2) الصقه في Claude (أو أي ذكاء اصطناعي).\n3) انسخ ردّه كله.\n4) «📋 لصق» ثم «▶ ارسم الكود».")
            return
        self.status.set("🤖 يطلب من Claude كود الصورة... (قد يستغرق نحو دقيقة)")

        def work():
            try:
                code = extract_code(ai_bridge.ask(prompt))
            except Exception as e:
                self.root.after(0, lambda e=e: self.status.set(f"تعذّر طلب الصورة: {e}"))
                return
            self.root.after(0, lambda: self.run_code_text(code, f"🤖 {desc.strip()[:40]} — بواسطة Claude"))
        threading.Thread(target=work, daemon=True).start()

    def undo(self):
        """↩: back to the picture before the last 🧩 edit."""
        if self.busy or not self.history:
            return
        src = self.history.pop()
        self.undo_btn.configure(state="normal" if self.history else "disabled")
        self.open_image(path=str(src))

    def make_film(self):
        """🎬: the current picture forming pixel by pixel, as an MP4 in out/."""
        if self.busy:
            self.status.set("انتظر حتى تكتمل الرسمة الحالية.")
            return
        import film
        src = self.scene.get() if self.source[0] == "scene" else str(self.source[1])
        if not src:
            return
        out = OUT / f"{self.out_name()}_drawing.mp4"
        OUT.mkdir(exist_ok=True)
        speed = {"بطيء": "slow", "عادي": "normal", "سريع": "fast", "فوري": "fast"}.get(self.speed.get(), "normal")
        self.status.set("🎬 يصنع فيلم الرسم بـ ffmpeg... قد يستغرق دقيقة أو أكثر")

        def work():
            try:
                info = film.film_drawing(src, out, fps=30, speed=speed)
            except Exception as e:
                self.root.after(0, lambda e=e: self.status.set(f"تعذّر صنع الفيلم: {e}"))
                return
            self.root.after(0, lambda: self.status.set(f"🎬 الفيلم جاهز: out/{out.name} ({info['seconds']} ث، {info['frames']} إطار)"))
        threading.Thread(target=work, daemon=True).start()

    def ai_settings(self):
        """⚙: which AI the studio can reach, and how to connect one."""
        import ai_bridge
        tk, ttk = self.tk, self.ttk
        w = tk.Toplevel(self.root)
        w.title("⚙ الذكاء الاصطناعي")
        w.configure(bg="#16141c")
        w.transient(self.root)
        body = tk.Frame(w, bg="#16141c", padx=14, pady=10)
        body.pack(fill="both", expand=True)
        state = tk.StringVar(value="يفحص...")
        tk.Label(body, textvariable=state, fg="#9fe0b5", bg="#16141c", justify="right", anchor="e", wraplength=620,
                 font=("Segoe UI", 11, "bold")).pack(fill="x", pady=(0, 6))
        tk.Label(body, text="ليعمل 🧩 و🤖 تلقائياً يحتاج الاستوديو ذكاءً اصطناعياً متصلاً:\n"
                            "• Claude Code: افتح طرفية واكتب  claude  ثم  /login  مرة واحدة (لا يحتاج مفتاحاً).\n"
                            "• أو مفتاح Anthropic API أدناه.\n"
                            "بدونهما: تغييرات الألوان تتم محلياً، وبقية الطلبات تُنسخ لتلصقها في أي ذكاء اصطناعي.",
                 fg="#e9e2f5", bg="#16141c", justify="right", anchor="e", wraplength=620, font=("Segoe UI", 10)).pack(fill="x")
        st = ai_bridge.load_settings()
        row = tk.Frame(body, bg="#16141c")
        row.pack(fill="x", pady=(10, 2))
        key = tk.StringVar(value=st.get("anthropic_api_key", ""))
        ttk.Entry(row, textvariable=key, show="•", width=52).pack(side="left")
        tk.Label(row, text="مفتاح Anthropic API (اختياري)", fg="#cfc8dc", bg="#16141c").pack(side="right", padx=6)
        row = tk.Frame(body, bg="#16141c")
        row.pack(fill="x", pady=2)
        model = tk.StringVar(value=st.get("model", ""))
        ttk.Entry(row, textvariable=model, width=28).pack(side="left")
        tk.Label(row, text="النموذج (للمفتاح)", fg="#cfc8dc", bg="#16141c").pack(side="right", padx=6)
        row = tk.Frame(body, bg="#16141c")
        row.pack(fill="x", pady=(10, 0))

        def refresh():
            ai_bridge._cache.clear()

            def work():
                info = ai_bridge.status()
                now = {"cli": "متصل عبر Claude Code ✅", "api": "متصل عبر مفتاح API ✅"}.get(info["backend"],
                       "غير متصل — الألوان محلياً، والباقي بالنسخ واللصق")
                self.root.after(0, lambda: state.set(f"الحالة: {now}\n{info['cli_msg']}"))
            threading.Thread(target=work, daemon=True).start()

        def save():
            ai_bridge.save_settings({"anthropic_api_key": key.get().strip(), "model": model.get().strip() or ai_bridge.DEFAULTS["model"]})
            refresh()
        ttk.Button(row, text="حفظ", command=save).pack(side="right", padx=2)
        ttk.Button(row, text="إعادة الفحص", command=refresh).pack(side="right", padx=2)
        ttk.Button(row, text="إغلاق", command=w.destroy).pack(side="left", padx=2)
        refresh()

    # ── animation (KOSIF Motion): the film pipeline from the window ──────────────────────────────────────
    def _motion(self, *args, done=None, note=""):
        """Run motion/motion.py with these arguments in a thread; the last output line goes to the status bar."""
        motion = HERE / "motion" / "motion.py"
        if not motion.exists():
            self.status.set("مجلد motion غير موجود بجوار الاستوديو.")
            return
        self.status.set(note or "🎬 يعمل...")

        def work():
            env = dict(os.environ, PYTHONIOENCODING="utf-8")
            r = subprocess.run([sys.executable, str(motion), *map(str, args)], capture_output=True, text=True, encoding="utf-8",
                               errors="replace", cwd=str(motion.parent), env=env)
            out = (r.stdout or "").strip().splitlines()
            err = (r.stderr or "").strip().splitlines()
            last = (out[-1] if out else (err[-1] if err else "")).strip()
            ok = r.returncode == 0

            def show():
                self.status.set(("✅ " if ok else "⚠ ") + last[:160])
                if ok and done:
                    done(out)
            self.root.after(0, show)
        threading.Thread(target=work, daemon=True).start()

    def _motion_project(self, title: str) -> str | None:
        from tkinter import simpledialog
        projects = HERE / "motion" / "projects"
        names = sorted(p.name for p in projects.glob("*") if (p / "index.html").exists()) if projects.exists() else []
        hint = "المشاريع: " + "، ".join(names) if names else "لا مشاريع بعد"
        name = simpledialog.askstring(title, f"اسم المشروع:\n{hint}", parent=self.root)
        return name.strip() if name and name.strip() else None

    def motion_new(self, three_d: bool):
        from tkinter import simpledialog
        name = simpledialog.askstring("مشروع أنيميشن جديد", "اسم المشروع (بالإنجليزية بلا مسافات):", parent=self.root)
        if not name or not name.strip():
            return
        secs = simpledialog.askfloat("المدة", "كم ثانية؟", initialvalue=8.0, minvalue=1, maxvalue=600, parent=self.root)
        if not secs:
            return
        title = simpledialog.askstring("العنوان", "عنوان الفيلم (يظهر في الإطار الأول):", initialvalue=name, parent=self.root) or name
        args = ["new", name.strip(), "--seconds", secs, "--title", title]
        if three_d:
            args.append("--3d")

        def done(out):
            d = HERE / "motion" / "projects" / name.strip()
            if three_d:
                self._motion("bundle", name.strip(), note="📦 يحزم مشهد Three.js...", done=lambda o: self.open_code((d / "index.html").read_text(encoding="utf-8")))
            else:
                self.open_code((d / "index.html").read_text(encoding="utf-8"))
        self._motion(*args, note="🎬 ينشئ المشروع...", done=done)

    def motion_frame(self):
        """A key frame of a project rendered by the film engine, then drawn here pixel by pixel."""
        from tkinter import simpledialog
        name = self._motion_project("إطار مفتاحي")
        if not name:
            return
        t = simpledialog.askfloat("الزمن", "الثانية المطلوبة:", initialvalue=1.0, minvalue=0, parent=self.root)
        if t is None:
            return
        out = HERE / "motion" / "projects" / name / "frames"

        def done(o):
            f = out / f"t{t:05.2f}.png"
            if f.exists():
                self.open_image(path=str(f))
        self._motion("frames", name, "--times", f"{t}", note=f"🖼 يرسم إطار {t} ث من {name}...", done=done)

    def motion_render(self):
        from tkinter import simpledialog
        name = self._motion_project("تصيير الفيلم")
        if not name:
            return
        blur = simpledialog.askinteger("ضبابية الحركة", "إطارات فرعية لكل إطار (1 = بلا ضبابية، 4 = سينمائي):", initialvalue=1, minvalue=1, maxvalue=8, parent=self.root)
        if not blur:
            return
        out = OUT / f"{name}.mp4"
        OUT.mkdir(exist_ok=True)
        self._motion("render", name, "--engine", "studio", "--blur", blur, "--out", str(out),
                     note=f"🎞 يصيّر {name} (قد يستغرق دقائق؛ الحالة هنا عند الانتهاء)...",
                     done=lambda o: self.status.set(f"✅ الفيلم جاهز: out/{out.name}"))

    def motion_lint(self):
        name = self._motion_project("فحص المشروع")
        if name:
            self._motion("lint", name, note=f"🧪 يفحص {name}...")

    def motion_film_tool(self, cmd: str):
        """sheet / speed / beats / study on a file the user picks; the result opens (sheet, study) or shows in the status bar."""
        from tkinter import filedialog
        kinds = [("صوت", "*.wav *.mp3 *.m4a *.flac")] if cmd == "beats" else [("فيديو", "*.mp4 *.mov *.webm *.mkv")]
        path = filedialog.askopenfilename(title={"sheet": "فيلم للنقد", "speed": "فيلم لقياس السرعة", "beats": "مقطوعة موسيقية", "study": "فيلم مرجعي"}[cmd],
                                          initialdir=str(OUT), filetypes=kinds + [("الكل", "*.*")])
        if not path:
            return
        p = Path(path)
        if cmd == "sheet":
            out = p.parent / (p.stem + "_qa")
            self._motion("sheet", str(p), "--out", str(out), note="🔍 يصنع لوحة النقد...", done=lambda o: self.open_image(path=str(out / "contact.png")))
        elif cmd == "study":
            out = p.parent / (p.stem + "_study")
            self._motion("study", str(p), "--out", str(out), note="🎓 يدرس الفيلم المرجعي...", done=lambda o: os.startfile(str(out)))
        else:
            self._motion(cmd, str(p), note={"speed": "📏 يقيس السرعة بالتدفق البصري...", "beats": "🎼 يستخرج شبكة الإيقاع..."}[cmd])

    def show_help(self):
        from tkinter import messagebox
        messagebox.showinfo("دليل سريع", (
            "المصدر: اختر مشهداً من القائمة، أو 🖼 صورة (تُرسم من الصفر وتنتهي مطابقة للأصل)، أو 📝 كود من أي ذكاء اصطناعي.\n\n"
            "الرسم: ▶ يعيد الرسم، ⏸ يوقف، والسرعة من القائمة.\n\n"
            "🧩 عدّل الصورة: اكتب ما تريد تغييره («غيّر الذهبي إلى الأزرق»، «اجعل القميص أحمر»)؛ الألوان تتغيّر فوراً، "
            "وبقية الطلبات يكتبها Claude ويرسمها الاستوديو. ↩ يرجع خطوة.\n\n"
            "🤖 صورة من وصف: صف الصورة ويكتب Claude كودها ويرسمها.\n\n"
            "التصدير: 💾 PNG، ⤢ دقة عالية، 📤 كود الصورة (برنامج بايثون يعيد رسمها بأي مكان)، 🎬 فيلم الرسم.\n\n"
            "اختصارات: Ctrl+O صورة · Ctrl+V لصق · F5 ارسم · Ctrl+E تعديل · Ctrl+G من وصف · Ctrl+Z تراجع · Ctrl+K الكود · Ctrl+S حفظ"),
            parent=self.root)

    def run_code_text(self, code: str, note: str = ""):
        """Run code as if it were pasted and ▶ pressed (the panel, if open, shows it)."""
        code = self._clean_code(code)
        if not code:
            return
        if self.code_win is not None and self.code_win.winfo_exists():
            self.load_code_text(code)
        if self._launch_code(code):
            self.pending_note = note

    def run_code(self):
        code = self._clean_code(self.code_text.get("1.0", "end"))
        if code is None:
            return
        if not code:
            self.status.set("الصق كوداً أولاً.")
            return
        if self._launch_code(code):
            self.err_box.configure(state="normal")
            self.err_box.delete("1.0", "end")
            self.err_box.configure(state="disabled")

    def _launch_code(self, code: str) -> bool:
        """The risk check, then the code is written to code/last.* and drawn. False when the user declined."""
        from tkinter import messagebox
        why = risky(code)
        parent = self.code_win if self.code_win is not None and self.code_win.winfo_exists() else self.root
        if why and not messagebox.askyesno("تنبيه قبل التشغيل",
                                           "هذا الكود يحتوي أوامر تتجاوز الرسم:\n• " + "\n• ".join(why) +
                                           "\n\nسيعمل على جهازك بصلاحياتك. هل تثق بمصدره وتريد تشغيله؟",
                                           icon="warning", default="no", parent=parent):
            return False
        CODE.mkdir(exist_ok=True)
        low = code.lstrip()[:4000].lower()
        ext = ".html" if low.startswith("<") and ("<!doctype html" in low or "<html" in low or "<script" in low) else \
            ".svg" if low.startswith("<") else ".py"
        f = CODE / f"last{ext}"
        f.write_text(code, encoding="utf-8")
        self.start_code(f)
        return True

    def save_code_as_scene(self):
        from tkinter import simpledialog
        code = self._clean_code(self.code_text.get("1.0", "end"))
        if not code:
            return
        name = simpledialog.askstring("حفظ كمشهد", "اسم المشهد (بالإنجليزية، بدون مسافات):", parent=self.code_win)
        if not name:
            return
        name = re.sub(r"[^\w-]+", "_", name.strip())
        low = code.lstrip()[:4000].lower()
        ext = ".html" if low.startswith("<") and ("<!doctype html" in low or "<html" in low or "<script" in low) else \
            ".svg" if low.startswith("<") else ".py"
        (SCENES / f"{name}{ext}").write_text(code, encoding="utf-8")
        self.scene_box.configure(values=scenes())
        self.status.set(f"حُفظ المشهد {name}، وصار في قائمة المشاهد.")

    # ── pictures: trace and redraw ─────────────────────────────────────────────────────────────────────────
    def open_image(self, path: str | None = None, image: Image.Image | None = None):
        from tkinter import filedialog
        if path is None and image is None:
            path = filedialog.askopenfilename(filetypes=[("صور", " ".join("*" + e for e in IMAGE_TYPES)),
                                                         ("الكل", "*.*")])
            if not path:
                return
        SOURCES.mkdir(exist_ok=True)
        self.original = None
        if image is not None:
            name = time.strftime("clip_%Y%m%d_%H%M%S")
            src = SOURCES / f"{name}.png"
            image.save(src)
            self.original = src
        else:
            name = re.sub(r"[^\w-]+", "_", Path(path).stem) or "image"
            src = SOURCES / f"{name}.png"
            Image.open(path).save(src)                  # decoded pixels kept losslessly: the reference to match
            self.original = Path(path)                  # the file itself, for 📤 image code
        if self.image_mode.get() == EXACT:
            self.start_exact(src, name)
            return
        self.status.set("يُعيد رسم الصورة: يتعرّف على ألوانها ويحوّلها إلى أشكال متجهة...")

        def work():
            import vectorize as V
            t = time.perf_counter()
            try:
                data = V.trace(src)
            except Exception as e:
                self.root.after(0, lambda: self.status.set(f"تعذّر تحليل الصورة: {e}"))
                return
            data["title"] = name
            V.save(data, SCENES / f"{name}.json")
            OUT.mkdir(exist_ok=True)
            V.to_svg(data, OUT / f"{name}.svg", scale=2)
            secs = time.perf_counter() - t

            def go():
                self.scene_box.configure(values=scenes())
                self.scene.set(name)
                self.start()
                self.title = f"{name} ({len(data['layers'])} لون، حُلّلت في {secs:.1f} ث)"
            self.root.after(0, go)
        threading.Thread(target=work, daemon=True).start()

    def paste_any(self):
        """Ctrl+V: a copied picture is traced and redrawn; copied code or SVG goes to the code panel and runs."""
        from PIL import ImageGrab
        try:
            clip = ImageGrab.grabclipboard()
        except Exception:
            clip = None
        if isinstance(clip, Image.Image):
            self.open_image(image=clip.convert("RGBA"))
            return
        if isinstance(clip, list) and clip:
            p = Path(clip[0])
            if p.suffix.lower() in IMAGE_TYPES:
                self.open_image(path=str(p))
            elif p.suffix.lower() in (".py", ".svg", ".html", ".htm", ".txt"):
                self.open_code(p.read_text(encoding="utf-8-sig", errors="replace"), run=True)
            return
        try:
            text = self.root.clipboard_get()
        except self.tk.TclError:
            return
        if "<svg" in text or "<html" in text.lower() or re.search(r"\b(import|from|def|ImageDraw|turtle|plt)\b", text):
            self.open_code(text, run=True)

    def export_image_code(self, path: str | None = None):
        """📤: the code of an image (the open one, or one you pick). Pasted into any KOSIF Studio it paints the
        picture from nothing and ends identical to the original."""
        from tkinter import filedialog
        src = Path(path) if path else getattr(self, "original", None) if self.source[0] == "image" else None
        if src is None or not src.exists():
            p = filedialog.askopenfilename(title="اختر الصورة التي تريد كودها",
                                           filetypes=[("صور", " ".join("*" + e for e in IMAGE_TYPES)), ("الكل", "*.*")])
            if not p:
                return
            src = Path(p)
        name = re.sub(r"[^\w-]+", "_", src.stem) or "image"
        OUT.mkdir(exist_ok=True)
        self.status.set("📤 يحوّل الصورة إلى برنامج بايثون: يتتبّع أشكالها ثم يضمّن تفاصيلها...")

        def work():
            import to_python
            t = time.perf_counter()
            code = to_python.image_to_python(src, name)
            f = OUT / f"{name}.py"
            f.write_text(code, encoding="utf-8")

            def show():
                self.open_code(code)
                self.status.set(f"📤 برنامج الصورة جاهز في {time.perf_counter() - t:.0f} ث ({len(code) // 1024:,} ك.ب): {f}   ·   "
                                f"شغّله بـ python {f.name} في أي مكان، أو اضغط «ارسم الكود» هنا.")
            self.root.after(0, show)
        threading.Thread(target=work, daemon=True).start()

    # ── files ────────────────────────────────────────────────────────────────────────────────────────────
    def save_png(self):
        from tkinter import filedialog
        p = filedialog.asksaveasfilename(defaultextension=".png", initialdir=OUT,
                                         initialfile=f"{self.out_name()}.png", filetypes=[("PNG", "*.png")])
        if p:
            if self.native is not None:
                nv = self.native
                Image.fromarray(nv["canvas"].reshape(nv["h"], nv["w"], 4), "RGBA").save(p)
            else:
                Image.fromarray(self.disp).save(p)
            self.status.set(f"حُفظت: {p}")

    def export_big(self):
        name = self.out_name()
        OUT.mkdir(exist_ok=True)
        p = OUT / f"{name}_3840x2560.png"
        self.status.set("يُصدَّر بدقة 3840×2560 من نفس البرنامج...")

        def work():
            t = time.perf_counter()
            try:
                if self.source[0] == "image":
                    import vectorize as V
                    src = self.source[1]
                    im = Image.open(src)
                    im.load()
                    if V.looks_like_photo(np.asarray(im.convert("RGBA"))):
                        big, k = enlarge(im)                 # photos: the exact image itself, enlarged, true colours
                        pk = OUT / f"{name}_x{k}.png"
                        big.save(pk)
                        msg = (f"✅ تكبير ×{k} من الصورة المطابقة نفسها بألوانها الأصلية ({big.width}×{big.height}): "
                               f"out/{pk.name}   ·   والأصل المطابق: out/{name}_exact.png")
                    else:                                    # logos and flat art: vector stays sharp at any size
                        import vector_scene
                        data = V.trace(src)
                        V.to_svg(data, OUT / f"{name}.svg", scale=2)
                        R.render_image(vector_scene.build(data), scale=3.2, ss=2, rolloff=1.0).save(p)
                        msg = (f"✅ نسخة متجهة حادة بأي حجم: out/{name}.svg و {p.name}   ·   "
                               f"والأصل المطابق: out/{name}_exact.png")
                elif self.source[0] == "code" or load(name) is None:
                    code = self.source[1] if self.source[0] == "code" else scene_file(name)
                    tmp = Path(tempfile.mkdtemp(prefix="kosif_exp_"))
                    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
                    subprocess.run([sys.executable, str(HERE / "runner.py"), str(code), str(tmp), "--scale", "3.2",
                                    "--export", str(p)], timeout=CODE_TIMEOUT * 2, creationflags=flags,
                                   capture_output=True)
                    info = json.loads((tmp / "done.json").read_text(encoding="utf-8"))
                    shutil.rmtree(tmp, ignore_errors=True)
                    if info.get("raster"):                  # raster result: keep it exact, and enlarge it faithfully
                        exact_p = OUT / f"{name}_original.png"
                        Path(p).replace(exact_p)
                        big, k = enlarge(Image.open(exact_p))
                        pk = OUT / f"{name}_x{k}.png"
                        big.save(pk)
                        msg = (f"✅ ناتج الكود بدقته الأصلية: out/{exact_p.name}   ·   وتكبير ×{k} بألوانه الأصلية "
                               f"({big.width}×{big.height}): out/{pk.name}")
                    else:
                        msg = f"تم التصدير 3840×2560 بلا فقد في الجودة في {time.perf_counter() - t:.0f} ث: {p}"
                else:
                    _, steps, rolloff = load(name)
                    R.render_image(steps, scale=3.2, ss=2, rolloff=rolloff).save(p)
                    msg = f"تم التصدير 3840×2560 بلا فقد في الجودة في {time.perf_counter() - t:.0f} ث: {p}"
            except Exception as e:
                msg = f"تعذّر التصدير: {e}"
            self.root.after(0, lambda: self.status.set(msg))
        threading.Thread(target=work, daemon=True).start()

    def run(self):
        self.root.update_idletasks()                        # the window is as tall as the screen allows: open it at the top
        x = max(0, (self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) // 2)
        self.root.geometry(f"+{x}+0")
        self.root.mainloop()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("scene", nargs="?", default="dragon_girl" if scene_file("dragon_girl") else (scenes() or [""])[0])
    ap.add_argument("--speed", default="عادي", help="بطيء / عادي / سريع / فوري  (or slow/normal/fast/instant)")
    ap.add_argument("--render", metavar="PNG", help="no window: render the picture program to this file")
    ap.add_argument("--scale", type=float, default=1.0, help="1.0 = 1200x800, 3.2 = 3840x2560")
    ap.add_argument("--trace", metavar="IMAGE", help="vectorize an image into scenes/<name>.json (+ out/<name>.svg)")
    ap.add_argument("--image", metavar="IMAGE", help="open the studio and redraw this image")
    ap.add_argument("--image-code", metavar="IMAGE", help="no window: write a standalone Python program for this image to out/<name>.py")
    ap.add_argument("--data-only", action="store_true", help="with --image-code: the pure-data form (TITLE/SIZE/IMAGE_B64), read by the studio without running")
    ap.add_argument("--code", metavar="FILE", help="open the studio and draw this code file (SVG/PIL/matplotlib/turtle/scene)")
    ap.add_argument("--name", help="scene name for --trace (default: the image's file name)")
    ap.add_argument("--title", help="title shown while drawing a traced scene")
    a = ap.parse_args()
    if a.trace:
        import vectorize as V
        name = a.name or Path(a.trace).stem
        t = time.perf_counter()
        data = V.trace(a.trace)
        data["title"] = a.title or name
        V.save(data, SCENES / f"{name}.json")
        OUT.mkdir(exist_ok=True)
        V.to_svg(data, OUT / f"{name}.svg", scale=4)
        pts = sum(len(p["pts"]) for L in data["layers"] for p in L["polys"])
        print(f"traced {a.trace} -> scenes/{name}.json + out/{name}.svg: {len(data['layers'])} colours, "
              f"{pts} points, {time.perf_counter() - t:.1f}s")
        a.scene = name
    if a.image_code:
        name = re.sub(r"[^\w-]+", "_", Path(a.image_code).stem) or "image"
        OUT.mkdir(exist_ok=True)
        if a.data_only:
            f = OUT / f"{name}_code.py"
            f.write_text(image_code(Path(a.image_code), name), encoding="utf-8")
        else:
            import to_python
            f = OUT / f"{name}.py"
            f.write_text(to_python.image_to_python(Path(a.image_code), name), encoding="utf-8")
        print(f"{f}: {f.stat().st_size // 1024:,} KB")
        return
    speed = {"slow": "بطيء", "normal": "عادي", "fast": "سريع", "instant": "فوري"}.get(a.speed, a.speed)
    if a.render:
        t = time.perf_counter()
        loaded = load(a.scene)
        if loaded is None:
            raise SystemExit("this scene is plain Python: draw it in the studio, or run runner.py with --export")
        _, steps, rolloff = loaded
        R.render_image(steps, scale=a.scale, ss=2 if a.scale > 2 else 3, rolloff=rolloff).save(a.render)
        print(f"{a.render}: {round(R.W0 * a.scale)}x{round(R.H0 * a.scale)} in {time.perf_counter() - t:.1f}s")
        return
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)      # real pixels, not Windows' blurry upscaling
    except Exception:
        pass
    st = Studio("" if (a.code or a.image) else a.scene, speed, a.scale)
    if a.code:
        st.root.after(300, lambda: st.open_code(Path(a.code).read_text(encoding="utf-8-sig"), run=True))
    elif a.image:
        st.root.after(300, lambda: st.open_image(path=a.image))
    st.run()


if __name__ == "__main__":
    main()
