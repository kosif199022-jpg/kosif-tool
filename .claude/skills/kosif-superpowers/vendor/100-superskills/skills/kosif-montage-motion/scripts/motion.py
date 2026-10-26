"""KOSIF Motion — professional animations as HTML compositions (HyperFrames format + GSAP + the motion kit),
rendered by HyperFrames' CLI when it is installed here, or by KOSIF Studio's own frame renderer.

    python motion.py new NAME [--seconds 8] [--fps 30] [--size 1920x1080] [--title "..."] [--3d|--canvas|--lab]   a project in projects/NAME
    python motion.py frames PROJECT [--times 0.5,2,4,8] [--out DIR]                           key frames (the 8-second gate)
    python motion.py check PROJECT                                                             HyperFrames lint + runtime validation
    python motion.py render PROJECT [--engine auto|hyperframes|studio] [--workers 0] [--draft] [--force] [--out X.mp4]
    python motion.py preview PROJECT                                                              a draft cut in a fraction of the time
    python motion.py measure FILM.mp4 [--fps 15]                                               motion energy: still share, peak, mean
    python motion.py lint PROJECT                                                               determinism, contract and taste checks
    python motion.py sheet FILM.mp4 [--at 4.2] [--out DIR]                                      contact sheet, phone test, strip, review.md
    python motion.py speed FILM.mp4                                                             px/frame from optical flow: blur or redesign
    python motion.py beats TRACK.wav [--out beats.json]                                         a beat grid (bpm, beats, downbeats, hits)
    python motion.py study REFERENCE.mp4 [--out DIR]                                            measure a reference film → style_guide.md
    python motion.py footage CLIP.mp4 --out projects/X/assets/clip.mp4 [--from 0 --dur 5]       an all-intra clip a composition can seek
    python motion.py doctor                                                                     what is available on this machine

A composition is index.html with a root <div data-composition-id data-width data-height data-duration>, GSAP
timelines registered in window.__timelines (seconds), assets/motion-kit.js for text masks, pen strokes, rain,
vapour, camera moves, grain and vignette, and the kit's shim so the same file renders through either engine.
"""
from __future__ import annotations
import sys as _sys
for _s in (_sys.stdout, _sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")   # Windows consoles default to a legacy code page

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _writable(d: Path) -> bool:
    try:
        d.mkdir(parents=True, exist_ok=True)
        probe = d / ".kosif_write_probe"
        probe.write_text("x"); probe.unlink()
        return True
    except OSError:
        return False


# where projects and films go: KOSIF_MOTION_HOME if set, next to the tool when writable, else the working directory
# (a skill folder on claude.ai is read-only)
_HOME = Path(os.environ["KOSIF_MOTION_HOME"]) if os.environ.get("KOSIF_MOTION_HOME") else None
PROJECTS = (_HOME / "projects") if _HOME else (HERE / "projects" if _writable(HERE / "projects") else Path.cwd() / "projects")
KIT = HERE / "kit" / "motion-kit.js"
TEMPLATE = next((p for p in (HERE / "templates" / "composition.html", HERE.parent / "templates" / "composition.html") if p.exists()),
                HERE / "templates" / "composition.html")
GSAP = next((p for p in (HERE / "node_modules" / "gsap" / "dist" / "gsap.min.js", HERE / "kit" / "gsap.min.js") if p.exists()),
            HERE / "node_modules" / "gsap" / "dist" / "gsap.min.js")
K3_BUNDLE = HERE / "kit" / "three-kit.bundle.js"                  # the 3D kit + three.js as one global script (window.K3)
# KOSIF Studio's renderer (html_render.py, film.py): next to motion/ in the studio, or in skill 109 next to this skill
STUDIO = next((p for p in (HERE.parent, HERE, HERE.parent.parent / "pixel-studio-painter" / "scripts") if (p / "html_render.py").exists()), HERE.parent)
OUT_DIR = (_HOME / "out") if _HOME else (STUDIO / "out" if _writable(STUDIO / "out") else Path.cwd() / "out")
sys.path.insert(0, str(STUDIO))


def hf_cmd() -> list[str] | None:
    """How to run HyperFrames' CLI here: node + its bin script (the .cmd wrapper breaks on non-ASCII paths)."""
    pkg = HERE / "node_modules" / "hyperframes" / "package.json"
    if not pkg.exists():
        return None
    meta = json.loads(pkg.read_text(encoding="utf-8"))
    b = meta.get("bin")
    rel = b if isinstance(b, str) else (b or {}).get("hyperframes") or next(iter((b or {}).values()), None)
    if not rel:
        return None
    node = shutil.which("node")
    return [node, str(pkg.parent / rel)] if node else None


def _env() -> dict:
    env = dict(os.environ)
    env.setdefault("HYPERFRAMES_SKIP_SKILLS", "1")
    env.setdefault("PRODUCER_LOW_MEMORY_MODE", "1")
    return env


def project_dir(name: str) -> Path:
    """A project by path, by `projects/NAME`, or by bare NAME — wherever projects live (KOSIF_MOTION_HOME, the tool, cwd)."""
    p = Path(name)
    for cand in (p, PROJECTS / p.name, PROJECTS.parent / p, Path.cwd() / p, HERE / p):
        if (cand / "index.html").exists():
            return cand
    return p if p.is_dir() else PROJECTS / p.name


def safe_name(name: str) -> str:
    """A project name that stays inside PROJECTS: the last path part, letters/digits/Arabic/_/- only, never empty or dotted."""
    base = Path(str(name).replace("\\", "/")).name
    slug = re.sub(r"[^\w\-\u0600-\u06FF]+", "_", base, flags=re.UNICODE).strip("._-")
    if not slug or slug in (".", ".."):
        raise SystemExit(f"invalid project name: {name!r}")
    return slug


def html_text(s) -> str:
    """Text for an HTML template: escaped, so a title can never become markup or script."""
    import html as _h
    return _h.escape(str(s), quote=True)


def json_for_script(obj) -> str:
    """JSON safe inside a <script> element: '</' cannot close the tag."""
    import json as _j
    return _j.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


def final(name: str, out: Path | None = None, blur: int = 1, fps: int | None = None, min_short: int = 1080, workers: int = 0,
          poster_at: float | None = None, bake: bool = True) -> dict:
    """The delivery render, quality first: lossless PNG capture, libx264 slow / CRF 16, the short side never under
    min_short (a smaller page is drawn larger, not upscaled afterwards), then the poster baked as frame 0 and the gate.
    Use `preview` (draft) for every review round and this once at the end — that, not a lower final quality, is where
    the time is saved."""
    d = project_dir(name)
    w, h = _size(d / "index.html")
    scale = max(1.0, min_short / min(w, h))
    rep: dict = {}
    t_poster = None
    if bake:                                                   # the poster moment, picked on a quick draft, is DRAWN as frame 0 of the
        import poster                                          # final render: one encode, no generation loss afterwards
        t0 = time.perf_counter()
        if poster_at is None:
            draft = Path(tempfile.mkdtemp(prefix="kosif_poster_")) / "draft.mp4"
            render(name, "studio", "looks", None, draft, draft=True, force=True)
            poster_at = poster.pick(draft)["t"]
        t_poster = float(poster_at)
        rep["poster_pick_s"] = round(time.perf_counter() - t0, 1)
    t0 = time.perf_counter()
    path = render(name, "studio", "looks", fps, out, blur, workers=workers, force=True, capture="png", preset="slow", crf=16,
                  scale_override=scale if scale > 1.0 else None, frame0_t=t_poster)
    rep.update({"file": str(path), "size": f"{round(w * scale) // 2 * 2}x{round(h * scale) // 2 * 2}", "render_s": round(time.perf_counter() - t0, 1),
                "blur": blur, "capture": "png", "crf": 16})
    if bake:
        jpg = poster.extract(path, 0.0, path.with_suffix(".poster.jpg"))
        rep["poster"] = {"t": t_poster, "jpg": str(jpg), "method": "drawn as frame 0 (no re-encode)"}
    import qa
    g = qa.inspect(path)
    rep["gate"] = {k: g.get(k) for k in ("ok", "issues", "lufs", "true_peak", "size", "fps")}
    return rep


def duration_of(index: Path) -> float:
    import re
    m = re.search(r'data-composition-id="[^"]+"[^>]*data-duration="([\d.]+)"', index.read_text(encoding="utf-8"))
    return float(m.group(1)) if m else 10.0


LAB_KIT = HERE / "kit" / "lab-kit.js"
SHAPE_KIT = HERE / "kit" / "shape-kit.js"                          # the product-lab look (fur, eyes, characters, HUD, orbit walk)


def new(name: str, seconds: float, fps: int, size: str, title: str, three_d: bool = False, canvas: bool = False, lab: bool = False) -> Path:
    """A project from the flat template, or (three_d) from the cinematic 3D template: src/main.js on the three-kit,
    bundled by `motion.py bundle` before rendering."""
    import html as _html
    name = safe_name(name)
    d = PROJECTS / name
    (d / "assets").mkdir(parents=True, exist_ok=True)
    w, h = (int(v) for v in size.lower().split("x"))
    if not (16 <= w <= 7680 and 16 <= h <= 7680) or not (0.1 <= float(seconds) <= 3600) or not (1 <= int(fps) <= 120):
        raise SystemExit(f"out of range: size {w}x{h}, seconds {seconds}, fps {fps}")
    fill = lambda s: (s.replace("{{TITLE}}", _html.escape(title or name, quote=True)).replace("{{W}}", str(w)).replace("{{H}}", str(h))
                       .replace("{{SECONDS}}", str(seconds)).replace("{{FPS}}", str(fps)))
    if lab:                                                    # the lab route: three-kit bundle + lab-kit, HUD, orbit walk, two plush characters
        tdir = TEMPLATE.parent / "lab"
        (d / "src").mkdir(exist_ok=True)
        (d / "index.html").write_text(fill((tdir / "index.html").read_text(encoding="utf-8")), encoding="utf-8")
        (d / "src" / "main.js").write_text(fill((tdir / "main.js").read_text(encoding="utf-8")), encoding="utf-8")
        shutil.copy2(K3_BUNDLE, d / "assets" / "three-kit.bundle.js"); shutil.copy2(LAB_KIT, d / "assets" / "lab-kit.js")
    elif three_d:
        tdir = TEMPLATE.parent / "scene3d"
        (d / "src").mkdir(exist_ok=True)
        (d / "index.html").write_text(fill((tdir / "index.html").read_text(encoding="utf-8")), encoding="utf-8")
        js = fill((tdir / "src" / "main.js").read_text(encoding="utf-8"))
        if (HERE / "node_modules" / "three").exists() or not K3_BUNDLE.exists():
            kit_rel = Path(os.path.relpath(HERE / "kit" / "three-kit.js", d / "src")).as_posix()   # the kit, from wherever the project is
            (d / "src" / "main.js").write_text(js.replace("../../../kit/three-kit.js", kit_rel), encoding="utf-8")
        else:                                                  # no npm here: the scene runs on the pre-bundled kit, no bundling step
            js = re.sub(r"import\s*\{([^}]*)\}\s*from\s*\"[^\"]*three-kit\.js\";", lambda m: "const {" + m.group(1) + "} = window.K3;", js, flags=re.S)
            js = js.replace("export function build", "function build").replace("export ", "")
            (d / "src" / "main.js").write_text(js, encoding="utf-8")
            shutil.copy2(K3_BUNDLE, d / "assets" / "three-kit.bundle.js")
            shutil.copy2(SHAPE_KIT, d / "assets" / "shape-kit.js")          # window.K3S: SDF sculpting, plush, characters
            html = (d / "index.html").read_text(encoding="utf-8").replace('<script src="assets/main.bundle.js"></script>',
                                                                            '<script src="assets/three-kit.bundle.js"></script>\n<script src="assets/shape-kit.js"></script>\n<script src="src/main.js"></script>')
            (d / "index.html").write_text(html, encoding="utf-8")
    elif canvas:                                               # the canvas route: one file, window.seek(t)
        (d / "index.html").write_text(fill((TEMPLATE.parent / "canvas.html").read_text(encoding="utf-8")), encoding="utf-8")
    else:
        (d / "index.html").write_text(fill(TEMPLATE.read_text(encoding="utf-8")), encoding="utf-8")
    sync_assets(d)
    print(d)
    return d


def sync_assets(d: Path):
    (d / "assets").mkdir(exist_ok=True)
    shutil.copy2(KIT, d / "assets" / "motion-kit.js")
    if GSAP.exists():
        shutil.copy2(GSAP, d / "assets" / "gsap.min.js")
    index = d / "index.html"
    html = index.read_text(encoding="utf-8") if index.exists() else ""
    for name, src in (("lab-kit.js", LAB_KIT), ("three-kit.bundle.js", K3_BUNDLE), ("shape-kit.js", SHAPE_KIT)):
        # refresh the kits a project uses — present already, or named by its page (examples ship without the copies)
        if src.exists() and ((d / "assets" / name).exists() or f"assets/{name}" in html):
            shutil.copy2(src, d / "assets" / name)
    fonts = HERE / "kit" / "fonts"
    for fname in sorted(set(re.findall(r"assets/fonts/([\w.-]+\.woff2)", html))):  # the kit's fonts a page names (examples ship without them)
        if (fonts / fname).exists() and not (d / "assets" / "fonts" / fname).exists():
            (d / "assets" / "fonts").mkdir(parents=True, exist_ok=True)
            shutil.copy2(fonts / fname, d / "assets" / "fonts" / fname)


def _esbuild_cmd(esb: Path) -> list[str]:
    """esbuild's bin/esbuild is a JS shim on Windows/macOS installs but the native binary itself on Linux."""
    head = esb.read_bytes()[:4]
    return [str(esb)] if head[:4] == b"\x7fELF" or head[:2] == b"MZ" or head[:4] in (b"\xcf\xfa\xed\xfe", b"\xca\xfe\xba\xbe") else [shutil.which("node") or "node", str(esb)]


def kit_bundle() -> Path:
    """Rebuild kit/three-kit.bundle.js (three.js + three-kit as window.K3) with esbuild — after editing three-kit.js.
    Needs `npm install three@0.186.1 esbuild` in scripts/ (or NODE_PATH pointing at such a node_modules)."""
    roots = [HERE / "node_modules"] + [Path(p) for p in os.environ.get("NODE_PATH", "").split(os.pathsep) if p]
    esb = next((r / "esbuild" / "bin" / "esbuild" for r in roots if (r / "esbuild" / "bin" / "esbuild").exists()), None)
    node = shutil.which("node")
    if not esb or not node:
        raise SystemExit("esbuild/node not found: npm install three@0.186.1 esbuild  (in scripts/)")
    env = {**os.environ, "NODE_PATH": os.pathsep.join(str(r) for r in roots)}
    r = subprocess.run([*_esbuild_cmd(esb), str(HERE / "kit" / "k3-entry.js"), "--bundle", "--format=iife", "--minify", "--target=es2020",
                        f"--outfile={K3_BUNDLE}"], cwd=HERE, env=env, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(r.stderr[-1500:])
    print(K3_BUNDLE, f"{K3_BUNDLE.stat().st_size // 1024} KB")
    return K3_BUNDLE
    if GSAP.exists():
        shutil.copy2(GSAP, d / "assets" / "gsap.min.js")


def bundle(name: str, entry: str = "src/main.js", out: str = "assets/main.bundle.js") -> Path:
    """Three.js (or any ES-module) scene → one classic script with esbuild, so the composition loads from file://
    in both renderers without CORS or a dev server."""
    d = project_dir(name)
    esb = HERE / "node_modules" / "esbuild" / "bin" / "esbuild"
    if (d / "assets" / "three-kit.bundle.js").exists() and not esb.exists():
        print("this project runs on the pre-bundled kit (window.K3): nothing to bundle")
        return d / "src" / "main.js"
    if not esb.exists():
        raise SystemExit("esbuild is not installed here: npm install esbuild three  (in motion/)")
    node = shutil.which("node")
    target = d / out
    # assets imported by the scene are inlined (GLB/HDR/PNG/JPG/WAV as data URLs, JSON as data), so file:// renders need no server
    loaders = [f"--loader:{ext}=dataurl" for ext in (".glb", ".gltf", ".hdr", ".png", ".jpg", ".jpeg", ".webp", ".wav", ".bin")] + ["--loader:.json=json"]
    r = subprocess.run([*_esbuild_cmd(esb), str(d / entry), "--bundle", "--format=iife", "--minify", "--target=es2020", *loaders,
                        f"--outfile={target}"], cwd=HERE, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise SystemExit(r.stderr[-1500:])
    print(target, f"{target.stat().st_size // 1024} KB")
    return target


def frames(name: str, times: list[float], out: Path | None, timeout: float = 300.0) -> list[Path]:
    """Key frames through the studio's renderer: the page is built once (3D scenes take a while to generate their
    textures), then sought to each time; window.render(t) or window.seek(t)."""
    import io
    import re
    import html_render
    from playwright.sync_api import sync_playwright
    import film
    d = project_dir(name)
    out = out or d / "frames"
    out.mkdir(parents=True, exist_ok=True)
    html = (d / "index.html").read_text(encoding="utf-8")
    m = re.search(r'data-width="(\d+)"[^>]*data-height="(\d+)"', html)
    w, h = (int(m.group(1)), int(m.group(2))) if m else (1920, 1080)
    files = []
    p, browser, pg, _ = film._open_page(d / "index.html", w, h, timeout * 1000)
    errors: list[str] = []
    pg.on("pageerror", lambda e: errors.append(str(e)[:200]))
    pg.on("console", lambda m: errors.append("console." + m.type + ": " + m.text[:200]) if m.type in ("error", "warning") else None)
    try:
        grab = film._grabber(pg, "png")
        for t in times:
            f = out / f"t{t:05.2f}.png"
            for attempt in range(4):                           # a busy machine can stall one grab: seek again and retry
                try:
                    pg.evaluate(film.SEEK_JS, t)
                    pg.wait_for_function("window.__ready === true", timeout=timeout * 1000)
                    f.write_bytes(grab())
                    break
                except Exception as e:                         # noqa: BLE001 — playwright TimeoutError and friends
                    if attempt == 3:
                        raise
                    print(f"t={t}: {type(e).__name__}, retry {attempt + 1}", file=sys.stderr)
                    pg.wait_for_timeout(1500 * (attempt + 1))
            files.append(f)
            print(f)
    finally:
        browser.close(); p.stop()
    if errors:
        print("page errors:", *errors[:5], sep="\n  ")
    return files


def check(name: str) -> int:
    cmd = hf_cmd()
    if not cmd:
        print("HyperFrames is not installed here: npm install hyperframes gsap  (in motion/)")
        return 2
    r = subprocess.run([*cmd, "check", str(project_dir(name))], env=_env(), cwd=HERE)
    return r.returncode


def _fingerprint(d: Path, params: dict) -> str:
    """What the render depends on: every text source in the project (html/js/css/json) by content, every binary asset
    by name + size + mtime, plus the render parameters. Same fingerprint → the same film, so it need not be rendered twice."""
    import hashlib
    h = hashlib.sha1(json.dumps(params, sort_keys=True).encode())
    for f in sorted(p for p in d.rglob("*") if p.is_file() and "frames" not in p.parts and not p.name.startswith(".")):
        rel = f.relative_to(d).as_posix().encode()
        if f.suffix.lower() in (".html", ".htm", ".js", ".css", ".json", ".svg", ".txt"):
            h.update(rel); h.update(f.read_bytes())
        else:
            st = f.stat(); h.update(rel); h.update(f"{st.st_size}:{int(st.st_mtime)}".encode())
    return h.hexdigest()


def render(name: str, engine: str, quality: str, fps: int | None, out: Path | None, blur: int = 1, shutter: float = 0.5,
           stack: str = "average", workers: int = 0, draft: bool = False, force: bool = False, capture: str | None = None,
           preset: str | None = None, crf: int | None = None, scale_override: float | None = None, frame0_t: float | None = None) -> Path:
    """draft: half size, 15 fps, ultrafast/crf 23, JPEG capture, no sub-frame blur — a review cut in a fraction of the
    time (the same page, the same t → the same composition). workers: browsers in parallel (0 = by core count).
    A finished film whose fingerprint (sources + parameters) is unchanged is not rendered again unless force."""
    d = project_dir(name)
    index = d / "index.html"
    out = out or OUT_DIR / (f"{d.name}.draft.mp4" if draft else f"{d.name}.mp4")
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = hf_cmd()
    use_hf = engine == "hyperframes" or (engine == "auto" and cmd is not None)
    if draft:
        use_hf = False
    size = _size(index)
    scale = 1.0
    if draft:                                                  # the page keeps its own layout; the browser draws it at half the pixels
        scale, fps, blur = 0.5, fps or 15, 1
    elif scale_override:
        scale = float(scale_override)
    capture = capture or ("jpeg" if draft else "png")
    preset = preset or ("ultrafast" if draft else "medium")
    crf = crf if crf is not None else (23 if draft else 18)
    params = {"engine": "hyperframes" if use_hf else "studio", "fps": fps or _fps(index), "size": size, "scale": scale, "blur": blur, "shutter": shutter,
              "stack": stack, "capture": capture, "preset": preset, "crf": crf, "quality": quality, "v": 4, "frame0_t": frame0_t}
    fp = _fingerprint(d, params)
    stamp = out.with_suffix(out.suffix + ".kosif.json")
    if not force and out.exists() and stamp.exists():
        try:
            if json.loads(stamp.read_text(encoding="utf-8")).get("fingerprint") == fp:
                print(json.dumps({"file": str(out), "cached": True, "mb": round(out.stat().st_size / 1e6, 2)}, ensure_ascii=False))
                return out
        except (OSError, ValueError):
            pass
    t0 = time.perf_counter()
    rep = {}
    if use_hf:
        if not cmd:
            raise SystemExit("HyperFrames is not installed here")
        args = [*cmd, "render", str(d), "-o", str(out), "-q", quality, "--quiet"]
        if fps:
            args += ["-f", str(fps)]
        r = subprocess.run(args, env=_env(), cwd=HERE)
        if r.returncode != 0 or not out.exists():
            raise SystemExit(f"hyperframes render failed ({r.returncode})")
    else:
        import film
        rep = film.film_animate(str(index), out, fps=fps or _fps(index), seconds=duration_of(index), size=size, blur=blur,
                                shutter=shutter, stack=stack, workers=workers, capture=capture, preset=preset, crf=crf, scale=scale,
                                frame0_t=frame0_t)
        mux_audio(index, out)
    info = {"file": str(out), "engine": "hyperframes" if use_hf else "studio", "draft": draft, "blur": blur, "workers": rep.get("workers"),
            "frames": rep.get("frames"), "seconds": round(time.perf_counter() - t0, 1), "mb": round(out.stat().st_size / 1e6, 2)}
    stamp.write_text(json.dumps({"fingerprint": fp, **info, "params": params}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(info, ensure_ascii=False))
    return out


def mux_audio(index: Path, video: Path):
    """The composition's <audio> clips (src, data-start, data-volume, data-fade-out) mixed into the studio-rendered video,
    the way HyperFrames does it for its own renders."""
    import re
    html = index.read_text(encoding="utf-8")
    clips = []
    for m in re.finditer(r"<audio\b[^>]*>", html):
        tag = m.group(0)
        src = re.search(r'src="([^"]+)"', tag)
        if not src:
            continue
        f = (index.parent / src.group(1)).resolve()
        if not f.exists():
            continue
        g = lambda k, d: float(re.search(rf'data-{k}="([\d.]+)"', tag).group(1)) if re.search(rf'data-{k}="([\d.]+)"', tag) else d
        role = re.search(r'data-role="([^"]+)"', tag)
        clips.append((f, g("start", 0.0), g("duration", 0.0), g("volume", 1.0), g("fade-out", 0.0), g("fade-in", 0.0), role.group(1) if role else ""))
    if not clips or not shutil.which("ffmpeg"):
        return
    dur = duration_of(index)
    args = ["ffmpeg", "-y", "-v", "info", "-hide_banner", "-nostats", "-i", str(video)]
    filters, labels = [], []
    for i, (f, start, d, vol, fo, fi, _role) in enumerate(clips):
        args += ["-i", str(f)]
        fl = f"[{i + 1}:a]volume={vol}"
        if fi:
            fl += f",afade=t=in:st=0:d={fi}"
        if fo and d:
            fl += f",afade=t=out:st={max(0.0, d - fo)}:d={fo}"
        fl += f",adelay={int(start * 1000)}|{int(start * 1000)}[a{i}]"
        filters.append(fl)
        labels.append(f"[a{i}]")
    # narration (data-role="voice") ducks everything else through a sidechain compressor so the words stay on top;
    # then the mix is normalised to what the platforms normalise to: -14 LUFS integrated, true peak -1 dB
    vo = [labels[i] for i, c in enumerate(clips) if c[6] == "voice"]
    bed = [labels[i] for i, c in enumerate(clips) if c[6] != "voice"]
    if vo and bed:
        mix = ((f"{''.join(bed)}amix=inputs={len(bed)}:normalize=0[bed];" if len(bed) > 1 else f"{bed[0]}anull[bed];")
               + (f"{''.join(vo)}amix=inputs={len(vo)}:normalize=0[vo];" if len(vo) > 1 else f"{vo[0]}anull[vo];")
               + "[vo]asplit=2[vk][vm];[bed][vk]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=380[duck];"
               + "[duck][vm]amix=inputs=2:normalize=0[mix]")
    else:
        mix = f"{''.join(labels)}amix=inputs={len(clips)}:normalize=0[mix]" if len(clips) > 1 else f"{labels[0]}anull[mix]"
    # two-pass loudness: measure the mix first, then normalise linearly with the measured values. One-pass loudnorm
    # (dynamic mode) overshoots on short films — a 5 s clip came out at -12.1 LUFS instead of -14.
    norm = "loudnorm=I=-14:TP=-1:LRA=11"
    meas = subprocess.run([*args, "-filter_complex", ";".join(filters + [mix + f";[mix]{norm}:print_format=json[aout]"]), "-map", "[aout]",
                           "-t", str(dur), "-f", "null", "-"], capture_output=True, text=True)
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", meas.stderr or "")
    if m:
        v = json.loads(m.group(0))
        norm += (f":measured_I={v['input_i']}:measured_TP={v['input_tp']}:measured_LRA={v['input_lra']}"
                 f":measured_thresh={v['input_thresh']}:offset={v['target_offset']}:linear=true")
    mix += f";[mix]{norm}[aout]"
    tmp = video.with_suffix(".tmp.mp4")
    args += ["-filter_complex", ";".join(filters + [mix]), "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
             "-t", str(dur), "-movflags", "+faststart", str(tmp)]
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode == 0 and tmp.exists():
        tmp.replace(video)
    else:
        print("audio mux skipped:", (r.stderr or "")[-300:])


def _fps(index: Path) -> int:
    import re
    m = re.search(r'data-fps="(\d+)"', index.read_text(encoding="utf-8"))
    return int(m.group(1)) if m else 30


def _size(index: Path) -> tuple[int, int]:
    import re
    m = re.search(r'data-width="(\d+)"[^>]*data-height="(\d+)"', index.read_text(encoding="utf-8"))
    return (int(m.group(1)), int(m.group(2))) if m else (1920, 1080)


def measure(film_path: Path, fps: int = 15) -> dict:
    """Motion energy frame by frame (mean |difference| between consecutive frames at 320 px): the share of
    near-still frames, the peak, the mean, and the longest freeze. The motion-director floor: little stillness,
    no single huge jump, something always moving."""
    import numpy as np
    import qa
    prev, energy, nframes = None, [], 0
    for g in qa._frames(film_path, fps, 320):                 # streamed grey frames: no temp files, no PNG round-trip
        a = g.astype(np.float32)
        nframes += 1
        if prev is not None:
            energy.append(float(np.abs(a - prev).mean()))
        prev = a
    files = range(nframes)
    e = np.array(energy if energy else [0.0])
    still = e < 0.6
    longest, run = 0, 0
    for s in still:
        run = run + 1 if s else 0
        longest = max(longest, run)
    rep = {"frames": len(files), "fps": fps, "mean": round(float(e.mean()), 2), "peak": round(float(e.max()), 2),
           "near_still_share": round(float(still.mean()), 3), "longest_freeze_s": round(longest / fps, 2),
           "above_2_share": round(float((e > 2).mean()), 3)}
    print(json.dumps(rep, ensure_ascii=False))
    return rep


def doctor():
    cmd = hf_cmd()
    print("hyperframes:", " ".join(cmd) if cmd else "not installed (npm install hyperframes gsap in motion/)")
    print("gsap:", GSAP if GSAP.exists() else "missing")
    print("ffmpeg:", shutil.which("ffmpeg") or "missing")
    try:
        import html_render
        print("browser:", html_render.browser_path())
    except Exception as e:
        print("browser:", e)
    if cmd:
        subprocess.run([*cmd, "doctor"], env=_env(), cwd=HERE)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("new"); p.add_argument("name"); p.add_argument("--seconds", type=float, default=8); p.add_argument("--fps", type=int, default=30)
    p.add_argument("--size", default="1920x1080"); p.add_argument("--title", default="")
    p.add_argument("--3d", dest="three_d", action="store_true", help="a cinematic Three.js project on the three-kit (bundle it before rendering)")
    p.add_argument("--canvas", action="store_true", help="the canvas route: one index.html, one canvas, window.seek(t)")
    p.add_argument("--lab", action="store_true", help="the product-lab route: plush 3D characters, HUD callouts, a lens that walks the circle (lab-kit)")
    p = sub.add_parser("frames"); p.add_argument("project"); p.add_argument("--times", default="0.5,2,4,6,8"); p.add_argument("--out")
    p = sub.add_parser("check"); p.add_argument("project")
    p = sub.add_parser("render"); p.add_argument("project"); p.add_argument("--engine", default="auto", choices=["auto", "hyperframes", "studio"])
    p.add_argument("--quality", default="looks"); p.add_argument("--fps", type=int); p.add_argument("--out")
    p.add_argument("--blur", type=int, default=1, help="sub-frames per frame for pages that implement window.__blur (studio engine)")
    p.add_argument("--shutter", type=float, default=0.5, help="exposure in frames: 0.5 = 180° shutter; 30 at 30 fps = a 1 s long exposure")
    p.add_argument("--stack", default="average", choices=["average", "lighten"], help="lighten = star trails / light painting")
    p.add_argument("--workers", type=int, default=0, help="browsers rendering in parallel (0 = one per core, up to 4)")
    p.add_argument("--draft", action="store_true", help="review cut: half size, 15 fps, ultrafast, JPEG capture")
    p.add_argument("--force", action="store_true", help="render even when sources and parameters are unchanged")
    p.add_argument("--capture", choices=["png", "jpeg"], help="frame grab format (jpeg ≈ 2× faster)")
    p.add_argument("--preset", help="libx264 preset"); p.add_argument("--crf", type=int)
    p = sub.add_parser("preview", help="= render --draft: a quick review cut (NAME.draft.mp4)")
    p.add_argument("project"); p.add_argument("--out"); p.add_argument("--workers", type=int, default=0); p.add_argument("--fps", type=int); p.add_argument("--force", action="store_true")
    p = sub.add_parser("measure"); p.add_argument("film"); p.add_argument("--fps", type=int, default=15)
    sub.add_parser("doctor")
    p = sub.add_parser("sync"); p.add_argument("project")
    sub.add_parser("kit-bundle", help="rebuild kit/three-kit.bundle.js with esbuild after editing three-kit.js")
    p = sub.add_parser("bundle"); p.add_argument("project"); p.add_argument("--entry", default="src/main.js"); p.add_argument("--out", default="assets/main.bundle.js")
    p = sub.add_parser("lint"); p.add_argument("project")
    p = sub.add_parser("final"); p.add_argument("project"); p.add_argument("--out"); p.add_argument("--blur", type=int, default=1)
    p.add_argument("--fps", type=int); p.add_argument("--min-short", type=int, default=1080); p.add_argument("--workers", type=int, default=0)
    p.add_argument("--poster-at", type=float); p.add_argument("--no-poster", action="store_true")
    p = sub.add_parser("sheet"); p.add_argument("film"); p.add_argument("--at", type=float); p.add_argument("--out")
    p = sub.add_parser("speed"); p.add_argument("film"); p.add_argument("--fps", type=float)
    p = sub.add_parser("beats"); p.add_argument("audio"); p.add_argument("--out")
    p = sub.add_parser("study"); p.add_argument("reference"); p.add_argument("--out")
    p = sub.add_parser("footage"); p.add_argument("video"); p.add_argument("--out", required=True); p.add_argument("--from", dest="start", type=float, default=0.0)
    p.add_argument("--dur", type=float); p.add_argument("--width", type=int, default=1280); p.add_argument("--fps", type=int, default=30)
    p = sub.add_parser("channels"); p.add_argument("audio"); p.add_argument("--fps", type=int, default=30); p.add_argument("--out"); p.add_argument("--bpm", type=float)
    p = sub.add_parser("loopcheck"); p.add_argument("film")
    p = sub.add_parser("inspect", help="the delivery gate: yuv420p/H.264, black + frozen stretches, LUFS + true peak, exposure")
    p.add_argument("film"); p.add_argument("--lufs", type=float, default=-14.0); p.add_argument("--allow", action="append", default=[], help="an expected hold, e.g. 6.6-7.3 (repeatable)")
    p = sub.add_parser("montage", help="edit footage to a beat (montage.py cut): clips, music, grade, punches, ducking, captions")
    p.add_argument("clips", nargs="+"); p.add_argument("--music", required=True); p.add_argument("--out", required=True); p.add_argument("--seconds", type=float)
    p.add_argument("--ratio", default="9:16"); p.add_argument("--grade", default="teal_orange"); p.add_argument("--voice"); p.add_argument("--captions")
    p.add_argument("--no-punch", action="store_true"); p.add_argument("--keep-audio", action="store_true"); p.add_argument("--style", default="reels")
    p = sub.add_parser("mocap"); p.add_argument("video"); p.add_argument("--out", required=True); p.add_argument("--fps", type=int, default=30)
    p.add_argument("--points", type=int, default=1200); p.add_argument("--from", dest="start", type=float, default=0.0); p.add_argument("--dur", type=float)
    a = ap.parse_args()
    if a.cmd == "inspect":
        import qa
        allow = [tuple(float(x) for x in v.split("-", 1)) for v in a.allow]
        rep = qa.inspect(Path(a.film), a.lufs, expect=allow)
        print(json.dumps(rep, ensure_ascii=False, indent=1))
        sys.exit(0 if rep["ok"] else 1)
    if a.cmd == "montage":
        import montage
        rep = montage.cut(a.clips, Path(a.music), Path(a.out), a.seconds, a.ratio, 30, a.grade, not a.no_punch,
                          Path(a.voice) if a.voice else None, Path(a.captions) if a.captions else None, a.keep_audio, a.style)
        rep.pop("plan"); print(json.dumps(rep, ensure_ascii=False, indent=1))
        return
    if a.cmd in ("channels", "loopcheck", "mocap"):
        import qa
        if a.cmd == "mocap":
            print(json.dumps(qa.mocap(Path(a.video), Path(a.out), a.fps, a.points, start=a.start, dur=a.dur), ensure_ascii=False, indent=1))
            return
        if a.cmd == "channels":
            print(json.dumps(qa.channels(Path(a.audio), a.fps, Path(a.out) if a.out else None, a.bpm), ensure_ascii=False, indent=1))
        else:
            rep = qa.loopcheck(Path(a.film))
            print(json.dumps(rep))
            sys.exit(0 if rep.get("ok") else 1)
        return
    if a.cmd in ("lint", "sheet", "speed", "beats", "study", "footage"):
        import qa
        if a.cmd == "lint":
            found = qa.lint(project_dir(a.project))
            for f in found:
                print(f"{f['level']:5s} {f['file']}:{f['line']}  {f['rule']}  ‹{f['text']}›")
            errs = sum(1 for f in found if f["level"] == "error")
            print(json.dumps({"errors": errs, "warnings": sum(1 for f in found if f["level"] == "warn")}))
            sys.exit(1 if errs else 0)
        if a.cmd == "sheet":
            film_p = Path(a.film)
            print(json.dumps(qa.sheet(film_p, Path(a.out) if a.out else film_p.parent / (film_p.stem + "_qa"), a.at), ensure_ascii=False, indent=1))
        elif a.cmd == "speed":
            print(json.dumps(qa.speed(Path(a.film), a.fps), ensure_ascii=False, indent=1))
        elif a.cmd == "beats":
            rep = qa.beats(Path(a.audio))
            out = Path(a.out) if a.out else Path(a.audio).with_suffix(".beats.json")
            out.write_text(json.dumps(rep, indent=1), encoding="utf-8")
            print(json.dumps({"bpm": rep["bpm"], "beats": len(rep["beats"]), "hits": len(rep["hits"]), "file": str(out)}))
        elif a.cmd == "study":
            ref = Path(a.reference)
            rep = qa.study(ref, Path(a.out) if a.out else ref.parent / (ref.stem + "_study"))
            print(json.dumps({k: v for k, v in rep.items() if k not in ("cut_times", "sheet")}, ensure_ascii=False, indent=1))
        elif a.cmd == "footage":
            print(json.dumps(qa.footage(Path(a.video), Path(a.out), a.start, a.dur, a.width, a.fps), ensure_ascii=False, indent=1))
        return
    if a.cmd == "kit-bundle":
        kit_bundle()
    elif a.cmd == "bundle":
        bundle(a.project, a.entry, a.out)
    elif a.cmd == "new":
        new(a.name, a.seconds, a.fps, a.size, a.title, a.three_d, a.canvas, a.lab)
    elif a.cmd == "frames":
        frames(a.project, [float(v) for v in a.times.split(",")], Path(a.out) if a.out else None)
    elif a.cmd == "check":
        sys.exit(check(a.project))
    elif a.cmd == "render":
        render(a.project, a.engine, a.quality, a.fps, Path(a.out) if a.out else None, a.blur, a.shutter, a.stack,
               a.workers, a.draft, a.force, a.capture, a.preset, a.crf)
    elif a.cmd == "final":
        print(json.dumps(final(a.project, Path(a.out) if a.out else None, a.blur, a.fps, a.min_short, a.workers, a.poster_at, not a.no_poster), ensure_ascii=False, indent=1))
    elif a.cmd == "preview":
        render(a.project, "studio", "looks", a.fps, Path(a.out) if a.out else None, workers=a.workers, draft=True, force=a.force)
    elif a.cmd == "measure":
        measure(Path(a.film), a.fps)
    elif a.cmd == "doctor":
        doctor()
    elif a.cmd == "sync":
        sync_assets(project_dir(a.project))


if __name__ == "__main__":
    main()
