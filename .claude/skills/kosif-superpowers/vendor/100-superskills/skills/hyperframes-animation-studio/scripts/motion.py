"""KOSIF Motion — professional animations as HTML compositions (HyperFrames format + GSAP + the motion kit),
rendered by HyperFrames' CLI when it is installed here, or by KOSIF Studio's own frame renderer.

    python motion.py new NAME [--seconds 8] [--fps 30] [--size 1920x1080] [--title "..."]   a project in projects/NAME
    python motion.py frames PROJECT [--times 0.5,2,4,8] [--out DIR]                           key frames (the 8-second gate)
    python motion.py check PROJECT                                                             HyperFrames lint + runtime validation
    python motion.py render PROJECT [--engine auto|hyperframes|studio] [--quality looks] [--fps 30] [--out X.mp4]
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
    p = Path(name)
    return p if p.is_dir() else PROJECTS / name


def duration_of(index: Path) -> float:
    import re
    m = re.search(r'data-composition-id="[^"]+"[^>]*data-duration="([\d.]+)"', index.read_text(encoding="utf-8"))
    return float(m.group(1)) if m else 10.0


def new(name: str, seconds: float, fps: int, size: str, title: str, three_d: bool = False, canvas: bool = False) -> Path:
    """A project from the flat template, or (three_d) from the cinematic 3D template: src/main.js on the three-kit,
    bundled by `motion.py bundle` before rendering."""
    d = PROJECTS / name
    (d / "assets").mkdir(parents=True, exist_ok=True)
    w, h = (int(v) for v in size.lower().split("x"))
    fill = lambda s: (s.replace("{{TITLE}}", title or name).replace("{{W}}", str(w)).replace("{{H}}", str(h))
                       .replace("{{SECONDS}}", str(seconds)).replace("{{FPS}}", str(fps)))
    if three_d:
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
            html = (d / "index.html").read_text(encoding="utf-8").replace('<script src="assets/main.bundle.js"></script>',
                                                                            '<script src="assets/three-kit.bundle.js"></script>\n<script src="src/main.js"></script>')
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
    r = subprocess.run([node, str(esb), str(d / entry), "--bundle", "--format=iife", "--minify", "--target=es2020", *loaders,
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
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=html_render.browser_path(), headless=True, args=html_render.GPU_FLAGS[2:])
        pg = browser.new_context(viewport={"width": w, "height": h}).new_page()
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)[:200]))
        pg.on("console", lambda m: errors.append("console." + m.type + ": " + m.text[:200]) if m.type in ("error", "warning") else None)
        pg.goto((d / "index.html").resolve().as_uri(), wait_until="load", timeout=timeout * 1000)
        pg.wait_for_function("window.__ready === true || typeof window.seek === 'function'", timeout=timeout * 1000)
        for t in times:
            pg.evaluate(film.SEEK_JS, t)
            pg.wait_for_function("window.__ready === true", timeout=timeout * 1000)
            f = out / f"t{t:05.2f}.png"
            f.write_bytes(pg.screenshot(type="png"))
            files.append(f)
            print(f)
        browser.close()
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


def render(name: str, engine: str, quality: str, fps: int | None, out: Path | None, blur: int = 1, shutter: float = 0.5,
           stack: str = "average") -> Path:
    d = project_dir(name)
    index = d / "index.html"
    out = out or OUT_DIR / f"{d.name}.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = hf_cmd()
    use_hf = engine == "hyperframes" or (engine == "auto" and cmd is not None)
    t0 = time.perf_counter()
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
        film.film_animate(str(index), out, fps=fps or _fps(index), seconds=duration_of(index), size=_size(index), blur=blur,
                          shutter=shutter, stack=stack)
        mux_audio(index, out)
    print(json.dumps({"file": str(out), "engine": "hyperframes" if use_hf else "studio", "blur": blur, "seconds": round(time.perf_counter() - t0, 1),
                      "mb": round(out.stat().st_size / 1e6, 2)}, ensure_ascii=False))
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
    args = ["ffmpeg", "-y", "-v", "error", "-i", str(video)]
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
    mix += ";[mix]loudnorm=I=-14:TP=-1:LRA=11[aout]"
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
    from PIL import Image
    tmp = Path(tempfile.mkdtemp(prefix="kosif_me_"))
    subprocess.run(["ffmpeg", "-v", "error", "-i", str(film_path), "-vf", f"fps={fps},scale=320:-2", str(tmp / "f_%05d.png")], check=True)
    files = sorted(tmp.glob("f_*.png"))
    prev, energy = None, []
    for f in files:
        a = np.asarray(Image.open(f).convert("L")).astype(np.float32)
        if prev is not None:
            energy.append(float(np.abs(a - prev).mean()))
        prev = a
    shutil.rmtree(tmp, ignore_errors=True)
    e = np.array(energy)
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
    p = sub.add_parser("frames"); p.add_argument("project"); p.add_argument("--times", default="0.5,2,4,6,8"); p.add_argument("--out")
    p = sub.add_parser("check"); p.add_argument("project")
    p = sub.add_parser("render"); p.add_argument("project"); p.add_argument("--engine", default="auto", choices=["auto", "hyperframes", "studio"])
    p.add_argument("--quality", default="looks"); p.add_argument("--fps", type=int); p.add_argument("--out")
    p.add_argument("--blur", type=int, default=1, help="sub-frames per frame for pages that implement window.__blur (studio engine)")
    p.add_argument("--shutter", type=float, default=0.5, help="exposure in frames: 0.5 = 180° shutter; 30 at 30 fps = a 1 s long exposure")
    p.add_argument("--stack", default="average", choices=["average", "lighten"], help="lighten = star trails / light painting")
    p = sub.add_parser("measure"); p.add_argument("film"); p.add_argument("--fps", type=int, default=15)
    sub.add_parser("doctor")
    p = sub.add_parser("sync"); p.add_argument("project")
    p = sub.add_parser("bundle"); p.add_argument("project"); p.add_argument("--entry", default="src/main.js"); p.add_argument("--out", default="assets/main.bundle.js")
    p = sub.add_parser("lint"); p.add_argument("project")
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
    if a.cmd == "bundle":
        bundle(a.project, a.entry, a.out)
    elif a.cmd == "new":
        new(a.name, a.seconds, a.fps, a.size, a.title, a.three_d, a.canvas)
    elif a.cmd == "frames":
        frames(a.project, [float(v) for v in a.times.split(",")], Path(a.out) if a.out else None)
    elif a.cmd == "check":
        sys.exit(check(a.project))
    elif a.cmd == "render":
        render(a.project, a.engine, a.quality, a.fps, Path(a.out) if a.out else None, a.blur, a.shutter, a.stack)
    elif a.cmd == "measure":
        measure(Path(a.film), a.fps)
    elif a.cmd == "doctor":
        doctor()
    elif a.cmd == "sync":
        sync_assets(project_dir(a.project))


if __name__ == "__main__":
    main()
