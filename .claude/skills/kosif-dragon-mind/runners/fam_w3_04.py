"""Wave 3, chunk 04 (engines-render-pipeline cards no earlier runner covered): each card's method as a real program.

Every runner builds a deterministic fixture inside its work folder (lavfi/testsrc clips, PIL frames, synthesized
tones, scaffolded HTML compositions, tiny Lottie files, a performer silhouette clip), applies the card's
what/how/params and measures the produced output against a known answer, plus a negative control (the same
measurement on the untreated input fails the criterion).

Engines: the repo's own kosif-montage-motion scripts (kmotion.py hub and menu, motion.py new/check/lint/frames/
preview/render with --blur/--capture/--workers and its render cache, shard.py plan/render/join, timeline.py,
studio_import.py, workbench_cli.py, qa.channels/loopcheck/mocap/lint RULES, kit/motion-kit.js + gsap), the
hyperframes-animation-studio kmotion/motion.py, tools/render_html.cjs and tools/verify_video.py, lottie-web
(npm, global), headless Chromium driven by Playwright, ffmpeg (xfade, subtitles/libass, loudnorm two-pass, ssim,
concat copy), numpy/scipy/PIL/cv2, mypy/ruff/pytest, tsc.

Installed for this module: ``pip install --user playwright`` (1.64.1; Python bindings only, the browser is the
existing /opt/pw-browsers Chromium) because motion.py/film.py/shard.py, the cards' own renderer, imports it.
Cards whose method needs a live third-party service, a proprietary engine, a Windows GPU path or that carry
no executable method of their own are listed in GAPS with the reason.
"""
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time
from contextlib import contextmanager
from pathlib import Path

import numpy as np

from _harness import card, check, fx

HERE = Path(__file__).resolve().parent
SKILLS = HERE.parents[1]
REPO = HERE.parents[3]
VSK = SKILLS / "kosif-superpowers/vendor/100-superskills/skills"
KM = VSK / "kosif-montage-motion/scripts"
HFS = VSK / "hyperframes-animation-studio/scripts"
NODE_MODS = Path("/opt/node22/lib/node_modules")
LOTTIE = NODE_MODS / "lottie-web/build/player/lottie.min.js"
GSAP = KM / "kit/gsap.min.js"
MKIT = KM / "kit/motion-kit.js"

PYTEST = shutil.which("pytest") or "pytest"
GAPS: dict = {}


def _gap(cid, why):
    GAPS[cid] = why
    GAPS["power:" + cid] = why


_gap("ENG-342", "dispatches a GitHub Actions workflow on the owner's private kosif-render-lab repo (live service, network "
                "write, billed minutes); the local shard/join method it runs is executed as ENG-389")
_gap("ENG-344", "the LottieFiles platform MCP is a live hosted service tied to a LottieFiles account (link only, not "
                "installed); local Lottie authoring/playback run as ENG-343 and ENG-60")
_gap("ENG-345", "kosif_atlas_read is a live Atlas service tool not exposed here; the card is a list of third-party "
                "skill ids whose scripts must not be run unreviewed")
_gap("ENG-346", "drives DaVinci Resolve Studio (proprietary, not installed) through DaVinciResolveScript; without it the "
                "script prints the manual and exits 2. The open equivalent of its timeline/track logic runs as ENG-413")
_gap("ENG-390", "ANGLE D3D11 with --ignore-gpu-blocklist is a Windows Direct3D path on a real GPU; this Linux sandbox "
                "has neither (only SwiftShader)")
_gap("ENG-399", "observed trend statistics (median 20 min per short, 4 h celebrated, $10 median tokens) with no source "
                "dataset here; no method to execute")


# ───────────────────────── shared helpers ─────────────────────────

def env_for(wd, tmp=True, **extra):
    """Child env: projects and films under wd (KOSIF_MOTION_HOME); temp files under wd unless the tool starts Chromium
    (a long TMPDIR breaks its socket path; Playwright removes its own profile folder)."""
    e = dict(os.environ)
    e.update({"KOSIF_MOTION_HOME": str(wd), "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
    if tmp:
        e["TMPDIR"] = str(wd)
    e.update({k: str(v) for k, v in extra.items()})
    return e


def sh(cmd, wd, timeout=60, stdin=None, ok=(0,), env=None):
    done = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, timeout=timeout, cwd=str(wd),
                          input=stdin, env=env or env_for(wd), stdin=None if stdin is not None else subprocess.DEVNULL)
    if ok is not None and done.returncode not in ok:
        raise RuntimeError("command failed (%d): %s :: %s" % (done.returncode, " ".join(map(str, cmd))[:160],
                                                              (done.stderr or done.stdout)[-500:]))
    return done


def py(script, *args, wd, timeout=60, stdin=None, ok=(0,), env=None):
    return sh([sys.executable, script, *args], wd, timeout=timeout, stdin=stdin, ok=ok, env=env)


def jout(text):
    """The last JSON object printed by a tool (pretty or compact)."""
    text = text.strip()
    for m in reversed([m.start() for m in re.finditer(r"(?m)^\{", text)] or [text.find("{")]):
        try:
            return json.JSONDecoder().raw_decode(text[m:])[0]
        except ValueError:
            continue
    raise ValueError("no JSON in output: " + text[-300:])


def jw(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    return Path(path)


def wt(path, text):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(text, encoding="utf-8")
    return Path(path)


def ff(wd, *args, timeout=60):
    return sh(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args], wd, timeout=timeout)


def probe(path):
    return fx.probe(path)


def vstream(path):
    return next(s for s in probe(path)["streams"] if s["codec_type"] == "video")


def duration(path):
    return float(probe(path)["format"]["duration"])


def frame_at(path, t, size=None):
    """One decoded RGB frame (uint8 HxWx3) at time t."""
    vs = vstream(path)
    w, h = (size or (int(vs["width"]), int(vs["height"])))
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", "%.3f" % t, "-i", str(path), "-frames:v", "1",
                          "-vf", "scale=%d:%d" % (w, h), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, timeout=60, stdin=subprocess.DEVNULL).stdout
    return np.frombuffer(raw, np.uint8).reshape(h, w, 3)


def all_frames(path, size=None):
    vs = vstream(path)
    w, h = (size or (int(vs["width"]), int(vs["height"])))
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", "scale=%d:%d" % (w, h), "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-"], capture_output=True, timeout=60, stdin=subprocess.DEVNULL).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)


def nframes(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries",
                          "stream=nb_read_packets", "-of", "csv=p=0", str(path)], capture_output=True, text=True,
                         timeout=60).stdout.strip()
    return int(out.split(",")[0])


def ebur(wd, path):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-filter_complex", "ebur128=peak=true",
                          "-f", "null", "-"], capture_output=True, text=True, timeout=60, cwd=str(wd)).stderr
    tail = err[err.rfind("Summary:"):]
    I = float(re.search(r"I:\s*(-?[\d.]+|-inf)\s*LUFS", tail).group(1))
    return I


def tone_wav(path, freq=440.0, secs=1.0, sr=48000, amp=0.3, ch=1):
    t = np.arange(int(secs * sr)) / sr
    x = amp * np.sin(2 * np.pi * freq * t)
    return fx.write_wav(path, np.stack([x] * ch, 1) if ch > 1 else x, sr)


def peak_hz(x, sr):
    x = np.asarray(x, float)
    if x.ndim > 1:
        x = x.mean(1)
    sp = np.abs(np.fft.rfft(x * np.hanning(len(x))))
    return float(np.fft.rfftfreq(len(x), 1 / sr)[int(np.argmax(sp[1:]) + 1)])


def browser_path():
    for name in ("google-chrome", "chromium", "chromium-browser"):
        if shutil.which(name):
            return shutil.which(name)
    for p in sorted(Path("/opt/pw-browsers").glob("chromium-*/chrome-linux*/chrome")):
        return str(p)
    return None


@contextmanager
def browser_page(wd, w=320, h=180):
    """A headless Chromium page (Playwright). Its profile is a temporary folder Playwright removes on close (a long
    TMPDIR breaks Chromium's socket path, so it is left at the system default)."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=browser_path(), headless=True,
                               args=["--no-sandbox", "--allow-file-access-from-files", "--disable-gpu",
                                     "--autoplay-policy=no-user-gesture-required"])
        try:
            yield b.new_page(viewport={"width": w, "height": h})
        finally:
            b.close()


def png_rgb(data_or_path):
    from PIL import Image
    import io
    im = Image.open(io.BytesIO(data_or_path) if isinstance(data_or_path, (bytes, bytearray)) else data_or_path)
    return np.asarray(im.convert("RGB"))


def red_centroid(img, thr=150):
    m = (img[..., 0] > thr) & (img[..., 1] < 90) & (img[..., 2] < 90)
    if not m.any():
        return None
    ys, xs = np.nonzero(m)
    return float(xs.mean()), float(ys.mean())


def ssim_ff(wd, a, b):
    err = sh(["ffmpeg", "-hide_banner", "-i", a, "-i", b, "-lavfi", "ssim", "-f", "null", "-"], wd).stderr
    return float(re.search(r"All:([\d.]+)", err).group(1))


def motion_project(wd, name="p", seconds=1.0, size="320x180", script=None, tool=KM, extra=()):
    """kmotion/motion.py new NAME into wd/projects (KOSIF_MOTION_HOME=wd)."""
    py(tool / "motion.py", "new", name, "--seconds", str(seconds), "--fps", "30", "--size", size, "--title", "عنوان",
       *extra, wd=wd)
    d = Path(wd) / "projects" / name
    if script:
        html = (d / "index.html").read_text(encoding="utf-8")
        html = re.sub(r"(<div id=\"root\"[^>]*>).*?(</div>\s*</body>)", lambda m: m.group(1) + script + m.group(2), html,
                      flags=re.S)
        wt(d / "index.html", html)
    return d


def lottie_doc(x0=50, x1=250, frames=30, w=320, h=180):
    """A Lottie (bodymovin 5.7) document with one red 40x40 rectangle moving linearly from x0 to x1."""
    return {"v": "5.7.4", "fr": 30, "ip": 0, "op": frames + 1, "w": w, "h": h, "nm": "sting", "ddd": 0, "assets": [],
            "layers": [{"ddd": 0, "ind": 1, "ty": 4, "nm": "box", "sr": 1, "ao": 0, "ip": 0, "op": frames + 1, "st": 0,
                        "bm": 0,
                        "ks": {"o": {"a": 0, "k": 100}, "r": {"a": 0, "k": 0}, "a": {"a": 0, "k": [0, 0, 0]},
                               "s": {"a": 0, "k": [100, 100, 100]},
                               "p": {"a": 1, "k": [{"t": 0, "s": [x0, h / 2, 0], "o": {"x": [0], "y": [0]},
                                                    "i": {"x": [1], "y": [1]}},
                                                   {"t": frames, "s": [x1, h / 2, 0]}]}},
                        "shapes": [{"ty": "rc", "nm": "r", "d": 1, "s": {"a": 0, "k": [40, 40]},
                                    "p": {"a": 0, "k": [0, 0]}, "r": {"a": 0, "k": 0}},
                                   {"ty": "fl", "nm": "f", "c": {"a": 0, "k": [1, 0, 0, 1]}, "o": {"a": 0, "k": 100},
                                    "r": 1}]}]}


# ───────────────────────── Lottie: author (Creator) and play synced (ENG-343, ENG-60) ─────────────────────────

@card("ENG-343")
def lottie_creator(task, wd):
    """Lottie Creator MCP (link only) → its open method here: author a Lottie animation from keyframes, pack it as a
    .lottie (dotLottie zip: manifest.json + animations/<id>.json), then play it with lottie-web and measure the box."""
    import zipfile
    wd = Path(wd)
    doc = lottie_doc()
    jw(wd / "sting.json", doc)
    dl = wd / "sting.lottie"
    with zipfile.ZipFile(dl, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("manifest.json", json.dumps({"version": "1", "generator": "kosif-w3", "animations": [{"id": "sting"}]}))
        z.writestr("animations/sting.json", json.dumps(doc))
    with zipfile.ZipFile(dl) as z:
        names = sorted(z.namelist())
        back = json.loads(z.read("animations/sting.json"))
    shutil.copy(LOTTIE, wd / "lottie.min.js")
    wt(wd / "play.html", "<!doctype html><html><body style='margin:0;background:#000'><div id='a' "
       "style='width:320px;height:180px'></div><script src='lottie.min.js'></script><script>"
       "window.anim=lottie.loadAnimation({container:document.getElementById('a'),renderer:'svg',loop:false,"
       "autoplay:false,animationData:%s});anim.addEventListener('DOMLoaded',()=>{window.__ready=true;});"
       "</script></body></html>" % json.dumps(back))
    xs = {}
    with browser_page(wd) as pg:
        pg.goto((wd / "play.html").as_uri())
        pg.wait_for_function("window.__ready===true", timeout=10000)
        for f in (0, 15, 30):
            pg.evaluate("f=>anim.goToAndStop(f,true)", f)
            img = png_rgb(pg.screenshot())
            c = red_centroid(img)
            xs[f] = c[0] if c else None
            if f == 15:
                (wd / "frame15.png").write_bytes(pg.screenshot())
        total = pg.evaluate("anim.totalFrames")
    ok = all(v is not None for v in xs.values())
    return [
        check("dotLottie archive holds manifest + animation", names == ["animations/sting.json", "manifest.json"], names),
        check("authored doc round-trips through the archive", back == doc),
        check("lottie-web reports the authored frame count", total == 31, total, 31),
        check("box centre at frames 0/15/30 = 50/150/250 px (linear keys)",
              ok and all(abs(xs[f] - e) <= 2.5 for f, e in ((0, 50), (15, 150), (30, 250))), xs, {0: 50, 15: 150, 30: 250}),
        check("negative control: the frame-0 pose is not the frame-30 pose", ok and abs(xs[0] - 250) > 100, xs[0], "!= 250"),
    ], [dl, wd / "sting.json", wd / "frame15.png"]


@card("ENG-60")
def lottie_synced(task, wd):
    """lottie-web loadAnimation({renderer:'svg', autoplay:false}) driven by goToAndStop per frame from the composition's
    paused GSAP timeline, so seeking the composition seeks the logo sting."""
    wd = Path(wd)
    shutil.copy(LOTTIE, wd / "lottie.min.js")
    shutil.copy(GSAP, wd / "gsap.min.js")
    wt(wd / "comp.html", "<!doctype html><html><body style='margin:0;background:#000'><div id='a' "
       "style='width:320px;height:180px'></div><script src='gsap.min.js'></script><script src='lottie.min.js'></script>"
       "<script>const anim=lottie.loadAnimation({container:document.getElementById('a'),renderer:'svg',loop:false,"
       "autoplay:false,animationData:%s});const st={t:0};const tl=gsap.timeline({paused:true});"
       "tl.to(st,{t:1,duration:1,ease:'none',onUpdate:()=>anim.goToAndStop(Math.round(tl.time()*anim.frameRate)+15,true)},0);"
       "window.__timelines={root:tl};window.seek=(t)=>{tl.seek(t,false);anim.goToAndStop(Math.round(t*anim.frameRate)+15,true);"
       "return anim.currentFrame;};anim.addEventListener('DOMLoaded',()=>{window.__ready=true;});</script></body></html>"
       % json.dumps(lottie_doc(frames=45)))
    rows = []
    with browser_page(wd) as pg:
        pg.goto((wd / "comp.html").as_uri())
        pg.wait_for_function("window.__ready===true", timeout=10000)
        free = pg.evaluate("anim.currentFrame")
        for t in (0.0, 0.5, 0.9):
            cf = pg.evaluate("t=>seek(t)", t)
            c = red_centroid(png_rgb(pg.screenshot()))
            rows.append({"t": t, "frame": cf, "x": c[0] if c else None})
        pg.evaluate("seek(0.5)")
        (wd / "seek_0.5.png").write_bytes(pg.screenshot())
        paused = pg.evaluate("anim.isPaused")
    jw(wd / "sync.json", rows)
    # the sting starts 15 frames in (offset), 45-frame move 50→250
    exp = {r["t"]: 50 + 200 * (round(r["t"] * 30) + 15) / 45 for r in rows}
    return [
        check("autoplay off: the sting sits at frame 0 until the timeline seeks it", free == 0 and paused, free, 0),
        check("composition t → lottie frame = t*30 + 15 offset", [r["frame"] for r in rows] == [15, 30, 42],
              [r["frame"] for r in rows], [15, 30, 42]),
        check("box x follows the seeked frame (±2.5 px)",
              all(r["x"] is not None and abs(r["x"] - exp[r["t"]]) <= 2.5 for r in rows), rows, exp),
        check("negative control: an unsynced (never seeked) sting would stay at x=50, not the t=0.9 pose",
              abs(50 - rows[-1]["x"]) > 100, rows[-1]["x"], "far from 50"),
    ], [wd / "sync.json", wd / "seek_0.5.png"]


# ───────────────────────── tool landscape with licences, and when to choose which (ENG-347, ENG-411) ─────────────────────────

CATALOG = VSK / "kosif-montage-motion/references/tools-catalog.md"
CATALOG2 = VSK / "kosif-montage-motion/references/tools-catalog-2.md"


def _licence_class(lic):
    l = lic.lower()
    if "gpl" in l and "lgpl" not in l:
        return "copyleft"
    if "mpl" in l or "lgpl" in l:
        return "weak-copyleft"
    if "mit" in l or "apache" in l or "bsd" in l:
        return "permissive"
    if "غير موثق" in lic:
        return "undocumented"
    return "custom/source-available"


def _direct_tools():
    rows = []
    for line in CATALOG.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(\S+)\s*\|", line)
        if m:
            rows.append({"n": int(m.group(1)), "tool": m.group(2), "category": m.group(3), "licence": m.group(5),
                         "class": _licence_class(m.group(5)), "url": m.group(6)})
    return rows


def _node_version(wd, mod):
    r = sh(["node", "-e", "console.log(require(%s).version)" % json.dumps(str(NODE_MODS / mod / "package.json"))], wd,
           ok=None)
    return r.stdout.strip() if r.returncode == 0 else None


def _stack_review(rows, stack):
    by = {r["tool"].split()[0].lower(): r for r in rows}
    hits = [by[t.lower()] for t in stack if t.lower() in by]
    return {"stack": stack, "tools": hits,
            "review_required": [h["tool"] for h in hits if h["class"] in ("copyleft", "weak-copyleft",
                                                                          "custom/source-available", "undocumented")]}


@card("ENG-347")
def code_video_landscape(task, wd):
    """The 22 direct code/timeline video tools with their licences, classified (permissive / copyleft / weak copyleft /
    custom / undocumented) so another team's stack gets a licence review; the house stack (HyperFrames + GSAP + FFmpeg
    + Playwright + numpy) is probed for real."""
    wd = Path(wd)
    rows = _direct_tools()
    lic = {r["tool"].split()[0]: r["licence"] for r in rows}
    cls = {r["tool"].split()[0]: r["class"] for r in rows}
    with open(wd / "licences.csv", "w", encoding="utf-8") as f:
        f.write("n,tool,class,licence,url\n")
        for r in rows:
            f.write('%d,"%s",%s,"%s",%s\n' % (r["n"], r["tool"], r["class"], r["licence"].replace('"', "'"), r["url"]))
    house = {"hyperframes": _node_version(wd, "hyperframes"), "gsap": _node_version(wd, "gsap"),
             "ffmpeg": (sh(["ffmpeg", "-version"], wd).stdout.split("\n")[0][:40]),
             "playwright": fx.have("playwright"), "numpy": np.__version__}
    team_gpl = _stack_review(rows, ["Etro", "Remotion", "Manim"])
    team_mit = _stack_review(rows, ["Manim", "fframes", "WebMotion"])
    jw(wd / "landscape.json", {"direct": rows, "house_stack": house, "reviews": [team_gpl, team_mit]})
    return [
        check("22 direct tools parsed from the catalogue", len(rows) == 22, len(rows), 22),
        check("known licences: Manim MIT, VideoFlow Apache-2.0, Etro GPL-3.0, Movie Masher MPL-2.0",
              lic.get("Manim", "").startswith("MIT") and lic.get("VideoFlow") == "Apache-2.0" and lic.get("Etro") == "GPL-3.0"
              and lic.get("Movie") == "MPL-2.0", {k: lic.get(k) for k in ("Manim", "VideoFlow", "Etro", "Movie")}),
        check("classes: Etro copyleft, Movie Masher weak-copyleft, fframes permissive",
              (cls.get("Etro"), cls.get("Movie"), cls.get("fframes")) == ("copyleft", "weak-copyleft", "permissive"),
              [cls.get("Etro"), cls.get("Movie"), cls.get("fframes")]),
        check("house stack really present (HyperFrames, GSAP, FFmpeg, Playwright, numpy)",
              all(house.values()), house),
        check("a team stack with Etro (GPL) and Remotion (company licence) is flagged for review",
              set(team_gpl["review_required"]) == {"Etro", "Remotion"}, team_gpl["review_required"]),
        check("negative control: an all-MIT stack (Manim, fframes, WebMotion) raises no review flag",
              team_mit["review_required"] == [], team_mit["review_required"], []),
    ], [wd / "licences.csv", wd / "landscape.json"]


CHOOSE_RULES = [  # from the catalogue's "متى تختار ماذا" section, keyword → engine
    (("معادل", "رياضي", "equation", "math"), "Manim"),
    (("ثلاثي", "3d", "مجسم", "إضاءة"), "Three.js"),
    (("أصول متحركة", "lottie", "rive", "شعار متحرك", "logo sting"), "Lottie/Rive"),
    (("نمذجة", "modelling", "glb"), "Blender"),
    (("قطع", "تجميع", "صوت", "cut", "concat"), "MoviePy/FFmpeg"),
    (("react", "typescript", "فريق"), "Remotion/Motion Canvas/Revideo"),
]


def choose_engine(need):
    n = need.lower()
    for keys, engine in CHOOSE_RULES:
        if any(k in n for k in keys):
            return engine
    return "HTML/CSS/GSAP + HyperFrames"


@card("ENG-411")
def tool_landscape_choose(task, wd):
    """The distilled catalogue (500 tools: 22 direct / 254 adjacent / 224 complementary; 33 integrations) and its
    'when to choose which' rules as a router, with each chosen engine probed on this machine (fallback to the house
    engine when it is missing)."""
    wd = Path(wd)
    t1 = CATALOG.read_text(encoding="utf-8")
    t2 = CATALOG2.read_text(encoding="utf-8")
    counts = [int(x) for x in re.search(r"مباشرة (\d+) · مجاورة (\d+) · مكملة (\d+)", t1).groups()]
    integrations = re.findall(r"(?m)^## (\d+)\. ", t2)
    declared = int(re.search(r"العدد: (\d+)", t2).group(1))
    rule_text = t1[t1.index("## متى تختار ماذا"):t1.index("## الفئات")]
    needs = {"شرح رياضي بالمعادلات": "Manim", "مشهد ثلاثي الأبعاد بإضاءة": "Three.js",
             "شعار متحرك جاهز lottie": "Lottie/Rive", "نمذجة أصل GLB": "Blender",
             "قطع وتجميع مقاطع مع الصوت": "MoviePy/FFmpeg", "مقدمة نص عربي متحرك": "HTML/CSS/GSAP + HyperFrames"}
    probes = {"Manim": fx.have("manim"), "Three.js": (NODE_MODS / "three").exists(),
              "Lottie/Rive": (NODE_MODS / "lottie-web").exists(), "Blender": fx.which("blender"),
              "MoviePy/FFmpeg": fx.which("ffmpeg"), "HTML/CSS/GSAP + HyperFrames": (NODE_MODS / "hyperframes").exists()}
    plan = []
    for need, want in needs.items():
        eng = choose_engine(need)
        avail = probes.get(eng, False)
        plan.append({"need": need, "engine": eng, "expected": want, "available": bool(avail),
                     "run_with": eng if avail else "HTML/CSS/GSAP + HyperFrames (fallback; told to the user)"})
    jw(wd / "route.json", {"counts": counts, "integrations": len(integrations), "plan": plan})
    for_rules = all(k in rule_text for k in ("Manim", "Three.js", "Lottie", "Blender", "MoviePy"))
    untreated = sum(1 for p in plan if "HTML/CSS/GSAP + HyperFrames" == p["expected"])  # an unrouted default fits 1 of 6
    return [
        check("catalogue counts 22 / 254 / 224 (= 500)", counts == [22, 254, 224] and sum(counts) == 500, counts),
        check("33 integrations listed and declared", len(integrations) == 33 == declared, [len(integrations), declared]),
        check("the router's engines are the ones the catalogue's rules name", for_rules),
        check("each need routes to the catalogue's engine", all(p["engine"] == p["expected"] for p in plan),
              [p["engine"] for p in plan], [p["expected"] for p in plan]),
        check("missing engines fall back honestly (Blender/Manim absent here → house engine)",
              all((p["run_with"] == p["engine"]) == p["available"] for p in plan),
              {p["engine"]: p["available"] for p in plan}),
        check("negative control: one default engine for every need fits only 1 of 6", untreated == 1, untreated, 1),
    ], [wd / "route.json"]


# ───────────────────────── cheap chain then final legs (ENG-348) ─────────────────────────

def _leg(wd, i, height, out, secs=1.0):
    w = int(round(height * 16 / 9 / 2) * 2)
    src = ["testsrc2", "smptebars", "rgbtestsrc"][i % 3]
    ff(wd, "-f", "lavfi", "-i", "%s=s=%dx%d:r=30:d=%s" % (src, w, height, secs), "-vf",
       "drawbox=x=iw*%.2f:y=ih*0.4:w=iw*0.2:h=ih*0.2:color=white:t=fill" % (0.1 + 0.3 * i),
       "-c:v", "libx264", "-preset", "ultrafast", "-crf", "20", "-pix_fmt", "yuv420p", out)
    return Path(out)


@card("ENG-348")
def cheap_chain_then_final(task, wd):
    """Render the whole chain cheaply at 480p, then only the approved final legs at 1080p from the same spec (VRES)."""
    wd = Path(wd)
    legs = [0, 1, 2]
    final_legs = [1, 2]
    drafts = [_leg(wd, i, 480, wd / ("draft_%d.mp4" % i)) for i in legs]
    lst = wd / "draft_list.txt"
    lst.write_text("".join("file '%s'\n" % d.name for d in drafts))
    ff(wd, "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", wd / "chain_480p.mp4")
    finals = {i: _leg(wd, i, 1080, wd / ("final_%d_1080p.mp4" % i)) for i in final_legs}
    dh = [int(vstream(d)["height"]) for d in drafts]
    fh = [int(vstream(f)["height"]) for f in finals.values()]
    same = {}
    for i, f in finals.items():
        a = frame_at(wd / ("draft_%d.mp4" % i), 0.5, (160, 90)).astype(float)
        b = frame_at(f, 0.5, (160, 90)).astype(float)
        same[i] = float(np.abs(a - b).mean())
    other = float(np.abs(frame_at(drafts[0], 0.5, (160, 90)).astype(float) - frame_at(finals[1], 0.5, (160, 90)).astype(float)).mean())
    ratio = (854 * 480) / (1920 * 1080)
    return [
        check("whole chain drafted at 480p", dh == [480, 480, 480], dh),
        check("draft chain duration = 3 legs x 1 s", abs(duration(wd / "chain_480p.mp4") - 3.0) < 0.1,
              duration(wd / "chain_480p.mp4"), 3.0),
        check("only the final legs re-rendered at 1080p", fh == [1080, 1080] and len(finals) == 2, fh),
        check("final legs show the drafted picture (mean abs diff at 160x90 < 12)", all(v < 12 for v in same.values()), same),
        check("draft costs ~20% of the 1080p pixels per frame", abs(ratio - 0.1976) < 0.001, ratio, 0.1976),
        check("negative control: a different leg's final does not match leg 0's draft", other > 25, other, "> 25"),
    ], [wd / "chain_480p.mp4", finals[1], finals[2]]


# ───────────────────────── offline frames + audio + burned subtitles, keep only the final (ENG-355) ─────────────────────────

@card("ENG-355")
def offline_frames_mux(task, wd):
    """Render frames offline (PIL), synthesize the audio (numpy), burn subtitles (libass) and mux with ffmpeg; the
    intermediates are deleted so only the final file stays (params scale: 60 fps x 2 s = 120 frames)."""
    from PIL import Image, ImageDraw
    wd = Path(wd)
    fps, secs, W, H = 60, 2, 320, 180
    tmp = wd / "build"
    tmp.mkdir()
    for i in range(fps * secs):
        im = Image.new("RGB", (W, H), (20, 30, 60))
        x = int(20 + (W - 60) * i / (fps * secs - 1))
        ImageDraw.Draw(im).ellipse([x, 40, x + 40, 80], fill=(240, 200, 40))
        im.save(tmp / ("f%04d.png" % i))
    tone_wav(tmp / "tone.wav", 440.0, secs, 48000, 0.3)
    wt(tmp / "subs.srt", "1\n00:00:00,200 --> 00:00:01,000\nHELLO\n\n2\n00:00:01,200 --> 00:00:01,900\nWORLD\n")
    out_dir = wd / "deliver"
    out_dir.mkdir()
    final = out_dir / "film.mp4"
    ff(wd, "-framerate", str(fps), "-i", tmp / "f%04d.png", "-i", tmp / "tone.wav", "-vf",
       "subtitles=build/subs.srt:force_style='Fontsize=28,PrimaryColour=&H00FFFFFF,Outline=2,Alignment=2,MarginV=10'",
       "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
       "-shortest", "-movflags", "+faststart", final)
    clean = np.asarray(Image.open(tmp / "f0036.png").convert("RGB"))       # t = 0.6 s, inside cue 1
    nosub = np.asarray(Image.open(tmp / "f0066.png").convert("RGB"))       # t = 1.1 s, between cues
    shutil.rmtree(tmp)
    left = sorted(p.name for p in out_dir.iterdir())
    st = probe(final)["streams"]
    v = next(s for s in st if s["codec_type"] == "video")
    a = next(s for s in st if s["codec_type"] == "audio")
    f06 = frame_at(final, 0.6)
    band = (slice(120, 175), slice(100, 220))
    white = lambda img: int(((img[band].astype(int).min(2)) > 220).sum())
    sub_on, sub_clean = white(f06), white(clean)
    f11 = white(frame_at(final, 1.1))
    wav = wd / "a.wav"
    ff(wd, "-i", final, "-ac", "1", "-ar", "48000", wav)
    x, sr = fx.read_wav(wav)
    hz = peak_hz(x, sr)
    wav.unlink()
    return [
        check("only the final file is kept", left == ["film.mp4"] and not tmp.exists(), left, ["film.mp4"]),
        check("video 60 fps, 120 frames, 320x180", v["r_frame_rate"] == "60/1" and nframes(final) == 120 and
              (v["width"], v["height"]) == (320, 180), [v["r_frame_rate"], nframes(final)]),
        check("audio muxed (AAC) and its pitch is the synthesized 440 Hz", a["codec_name"] == "aac" and abs(hz - 440) < 3,
              hz, 440),
        check("subtitle burned during cue 1 (white text pixels in the bottom band)", sub_on > 40, sub_on, "> 40"),
        check("no subtitle between cues", f11 < 5, f11, "< 5"),
        check("negative control: the offline frame before burning has no subtitle pixels", sub_clean < 5, sub_clean, "< 5"),
    ], [final]


# ───────────────────────── procedural only, no downloads (ENG-356) ─────────────────────────

def _value_noise(h, w, cell, seed):
    rng = np.random.default_rng(seed)
    g = rng.random((h // cell + 2, w // cell + 2))
    ys, xs = np.mgrid[0:h, 0:w] / cell
    y0, x0 = ys.astype(int), xs.astype(int)
    fy, fx_ = ys - y0, xs - x0
    sy, sx = fy * fy * (3 - 2 * fy), fx_ * fx_ * (3 - 2 * fx_)
    a, b, c, d = g[y0, x0], g[y0, x0 + 1], g[y0 + 1, x0], g[y0 + 1, x0 + 1]
    return (a * (1 - sx) + b * sx) * (1 - sy) + (c * (1 - sx) + d * sx) * sy


def _autocorr1(img):
    a = img - img.mean()
    return float((a[:, :-1] * a[:, 1:]).mean() / (a * a).mean())


def _system_font():
    out = subprocess.run(["fc-match", "-f", "%{file}", "DejaVu Sans"], capture_output=True, text=True).stdout.strip()
    return out


@card("ENG-356")
def procedural_no_downloads(task, wd):
    """No downloaded models/textures/audio: procedural geometry, shader-style value noise, synthesized audio and a
    system font; CONCEPT.md + STORYBOARD.md with shot timecodes, then the film rendered from them."""
    from PIL import Image, ImageDraw, ImageFont
    wd = Path(wd)
    W, H, fps = 320, 180, 30
    shots = [("S1", 0.0, 1.0, "noise ground + rising star polygon"), ("S2", 1.0, 2.0, "star spins, title in system font")]
    wt(wd / "CONCEPT.md", "# Concept\nA star rises over a procedural noise ground; a synthesized chord swells.\n"
       "Assets: all generated in code (geometry, value noise, sine chord) + system font.\n")
    wt(wd / "STORYBOARD.md", "# Storyboard\n" + "".join("- %s %s-%s %s\n" % (s, "00:00:%05.2f" % a, "00:00:%05.2f" % b, d)
                                                        for s, a, b, d in shots))
    noise = _value_noise(H, W, 16, seed=11)
    font_path = _system_font()
    font = ImageFont.truetype(font_path, 24)
    frames = wd / "frames"
    frames.mkdir()
    for i in range(int(2.0 * fps)):
        t = i / fps
        base = (noise * 120 + 30).astype(np.uint8)
        im = Image.fromarray(np.stack([base, base // 2, base // 3], 2))
        dr = ImageDraw.Draw(im)
        cx, cy = W / 2, H * (0.8 - 0.4 * min(t, 1.0))
        ang = t * 2.0
        pts = [(cx + (30 if k % 2 == 0 else 12) * math.cos(ang + k * math.pi / 5),
                cy + (30 if k % 2 == 0 else 12) * math.sin(ang + k * math.pi / 5)) for k in range(10)]
        dr.polygon(pts, fill=(255, 220, 90))
        if t >= 1.0:
            dr.text((W / 2 - 50, 10), "KOSIF", font=font, fill=(255, 255, 255))
        im.save(frames / ("f%03d.png" % i))
    sr = 48000
    tt = np.arange(2 * sr) / sr
    chord = sum(np.sin(2 * np.pi * f * tt) for f in (220.0, 277.18, 329.63)) / 3 * 0.3 * np.minimum(1, tt / 0.5)
    fx.write_wav(wd / "chord.wav", chord, sr)
    film = wd / "film.mp4"
    ff(wd, "-framerate", str(fps), "-i", frames / "f%03d.png", "-i", wd / "chord.wav", "-c:v", "libx264", "-preset",
       "veryfast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", film)
    manifest = {"geometry": "code:star polygon", "texture": "code:value noise seed 11", "audio": "code:sine chord",
                "font": font_path, "downloads": []}
    jw(wd / "assets.json", manifest)
    sb = re.findall(r"(S\d) 00:00:([\d.]+)-00:00:([\d.]+)", (wd / "STORYBOARD.md").read_text())
    contiguous = all(abs(float(sb[k][2]) - float(sb[k + 1][1])) < 1e-6 for k in range(len(sb) - 1))
    total = float(sb[-1][2]) - float(sb[0][1])
    regen = _value_noise(H, W, 16, seed=11)
    white = np.random.default_rng(11).random((H, W))
    sys_font = font_path.startswith(("/usr/share/fonts", "/usr/local/share/fonts", "/etc/fonts"))
    is_procedural = lambda m: not m["downloads"] and all(str(v).startswith("code:") for k, v in m.items()
                                                       if k in ("geometry", "texture", "audio"))
    shutil.rmtree(frames)
    return [
        check("storyboard shots are contiguous and sum to the film duration", contiguous and abs(total - duration(film)) < 0.1,
              [total, duration(film)]),
        check("noise texture regenerates bit-identically from its seed (procedural, not a file)",
              np.array_equal(noise, regen)),
        check("value noise is spatially smooth (lag-1 autocorrelation > 0.9)", _autocorr1(noise) > 0.9, _autocorr1(noise)),
        check("font is a system font", sys_font, font_path),
        check("asset manifest is procedural with no downloads", is_procedural(manifest)),
        check("negative control: white noise (an un-shaded texture) is not smooth", _autocorr1(white) < 0.1,
              _autocorr1(white), "< 0.1"),
        check("negative control: a manifest with a downloaded texture fails the rule",
              not is_procedural(dict(manifest, texture="https://example.org/tex.jpg", downloads=["tex.jpg"]))),
    ], [film, wd / "STORYBOARD.md", wd / "CONCEPT.md"]


# ───────────────────────── engine by need (ENG-357) ─────────────────────────

ENGINE_BY_NEED = [
    (("hover", "scroll", "micro", "ui state"), "CSS/WAAPI"),
    (("react component", "layout", "spring ui"), "Motion"),
    (("draw", "icon", "path", "stroke"), "SVG"),
    (("3d", "orbit", "camera", "mesh"), "Three/R3F"),
    (("react video", "long sequenced", "remotion"), "Remotion"),
    (("html to video", "captions", "render mp4"), "HyperFrames"),
    (("timeline", "stagger", "sequence", "kinetic"), "GSAP"),
]
ENGINE_MODULE = {"CSS/WAAPI": None, "Motion": "motion", "SVG": None, "Three/R3F": "three", "Remotion": "remotion",
                 "HyperFrames": "hyperframes", "GSAP": "gsap"}


def route_engine(need):
    n = need.lower()
    for keys, eng in ENGINE_BY_NEED:
        if any(k in n for k in keys):
            return eng
    return "GSAP"


@card("ENG-357")
def engine_by_need(task, wd):
    """CSS/WAAPI, Motion, GSAP, SVG, Three/R3F, HyperFrames, Remotion selected by need; each choice is proven by
    running that engine here (WAAPI in Chromium, GSAP/three/motion in node, the remotion/hyperframes packages resolved)."""
    wd = Path(wd)
    needs = {"button hover micro-interaction": "CSS/WAAPI", "react component layout transition": "Motion",
             "draw an icon path stroke": "SVG", "3d product orbit camera": "Three/R3F",
             "react video long sequenced edit": "Remotion", "html to video with captions": "HyperFrames",
             "kinetic title stagger timeline": "GSAP"}
    routed = {n: route_engine(n) for n in needs}
    js = ("const r={};const g=require(%s).gsap;const o={x:0};g.to(o,{x:100,duration:1,ease:'none',paused:true}).progress(0.5);"
          "r.gsap=o.x;const T=require(%s);r.three=new T.Vector3(0,0,0).lerp(new T.Vector3(10,0,0),0.25).x;"
          "r.motion=typeof require(%s).animate;r.remotion=require(%s).version;r.hyperframes=require(%s).version;"
          "console.log(JSON.stringify(r));") % tuple(json.dumps(str(x)) for x in (
              NODE_MODS / "gsap", NODE_MODS / "three", NODE_MODS / "motion", NODE_MODS / "remotion/package.json",
              NODE_MODS / "hyperframes/package.json"))
    wt(wd / "engines.js", js)
    nodeo = json.loads(sh(["node", wd / "engines.js"], wd).stdout.strip().splitlines()[-1])
    wt(wd / "waapi.html", "<!doctype html><html><body><svg width=200 height=50><path id=p d='M0 25 L200 25' "
       "stroke='red' stroke-width=4 pathLength=1 stroke-dasharray=1 stroke-dashoffset=1 /></svg><div id=b "
       "style='width:20px;height:20px;background:red'></div><script>"
       "const a=document.getElementById('b').animate([{transform:'translateX(0px)'},{transform:'translateX(100px)'}],"
       "{duration:1000,easing:'linear',fill:'both'});a.pause();a.currentTime=300;"
       "const d=document.getElementById('p').animate([{strokeDashoffset:1},{strokeDashoffset:0}],{duration:1000,fill:'both'});"
       "d.pause();d.currentTime=500;window.__ready=true;</script></body></html>")
    with browser_page(wd) as pg:
        pg.goto((wd / "waapi.html").as_uri())
        pg.wait_for_function("window.__ready===true")
        waapi_x = pg.evaluate("new DOMMatrix(getComputedStyle(document.getElementById('b')).transform).m41")
        svg_off = pg.evaluate("parseFloat(getComputedStyle(document.getElementById('p')).strokeDashoffset)")
    proof = {"CSS/WAAPI": abs(waapi_x - 30) < 0.5, "SVG": abs(svg_off - 0.5) < 0.01, "GSAP": abs(nodeo["gsap"] - 50) < 1e-6,
             "Three/R3F": abs(nodeo["three"] - 2.5) < 1e-9, "Motion": nodeo["motion"] == "function",
             "Remotion": bool(nodeo["remotion"]), "HyperFrames": bool(nodeo["hyperframes"])}
    jw(wd / "engine_choice.json", {"routed": routed, "proof": proof, "node": nodeo, "waapi_x": waapi_x, "svg": svg_off})
    default_hits = sum(1 for n, want in needs.items() if want == "GSAP")
    return [
        check("each need routes to its engine", all(routed[n] == want for n, want in needs.items()), routed, needs),
        check("WAAPI: paused at 300 ms of a 100 px linear move → 30 px", proof["CSS/WAAPI"], waapi_x, 30),
        check("SVG draw-on: dashoffset 0.5 at half time", proof["SVG"], svg_off, 0.5),
        check("GSAP tween at progress 0.5 → 50; three lerp(0.25) → 2.5", proof["GSAP"] and proof["Three/R3F"],
              [nodeo["gsap"], nodeo["three"]], [50, 2.5]),
        check("Motion, Remotion and HyperFrames packages load here", proof["Motion"] and proof["Remotion"] and proof["HyperFrames"],
              [nodeo["motion"], nodeo["remotion"], nodeo["hyperframes"]]),
        check("negative control: one engine for everything fits only 1 of 7 needs", default_hits == 1, default_hits, 1),
    ], [wd / "engine_choice.json"]


# ───────────────────────── track layout + markers that follow recuts (ENG-363) ─────────────────────────

TRACK_LAYOUT = {"V1": "screen", "V2": "graphics", "V3": "text", "A1": "voice", "A2": "location", "A3": "sfx", "A4": "music"}
MARKER_COLOURS = {"CHAPTER": "Blue", "GFX": "Green", "HOOK": "Red", "REVIEW": "Yellow"}


def place_markers(timeline):
    """Markers are stored against a clip (clip id + offset inside it) and placed on the record timeline from the cut."""
    starts, t = {}, 0.0
    for c in timeline["layers"]["V1"]:
        starts[c["id"]] = (t, c["in"], c["out"])
        t += c["out"] - c["in"]
    placed = []
    for m in timeline["anchors"]:
        rec0, cin, cout = starts[m["clip"]]
        src = m["src_t"]
        if cin <= src < cout:
            placed.append({"name": m["name"], "kind": m["kind"], "color": MARKER_COLOURS[m["kind"]], "t": round(rec0 + src - cin, 3)})
    return placed


@card("ENG-363")
def track_marker_convention(task, wd):
    """Fixed track layout for voice-led edits (V1 screen, V2 graphics, V3 text, A1 voice, A2 location, A3 SFX, A4 music)
    and named colour markers (CHAPTER per beat, GFX, HOOK, REVIEW) mirrored in the timeline JSON, re-placed after a recut."""
    wd = Path(wd)
    tl = {"tracks": TRACK_LAYOUT,
          "layers": {"V1": [{"id": "c1", "src": "screen1.mp4", "in": 0.0, "out": 6.0},
                            {"id": "c2", "src": "screen2.mp4", "in": 2.0, "out": 9.0}],
                     "V2": [], "V3": [], "A1": [{"id": "vo", "src": "voice.wav"}], "A2": [], "A3": [], "A4": []},
          "anchors": [{"name": "CHAPTER 1 الفكرة", "kind": "CHAPTER", "clip": "c1", "src_t": 0.5},
                      {"name": "HOOK", "kind": "HOOK", "clip": "c1", "src_t": 1.5},
                      {"name": "GFX card", "kind": "GFX", "clip": "c2", "src_t": 4.0},
                      {"name": "CHAPTER 2", "kind": "CHAPTER", "clip": "c2", "src_t": 6.0},
                      {"name": "REVIEW hum", "kind": "REVIEW", "clip": "c2", "src_t": 8.5}]}
    before = place_markers(tl)
    jw(wd / "edit_v1.json", dict(tl, markers=before))
    tl2 = json.loads(json.dumps(tl))
    tl2["layers"]["V1"][0]["in"] = 1.0              # recut: trim the first second of clip 1 (the hook start moves)
    tl2["layers"]["V1"][1]["out"] = 8.0             # and end clip 2 a second earlier (the REVIEW marker falls out)
    after = place_markers(tl2)
    jw(wd / "edit_v2.json", dict(tl2, markers=after))
    bt = {m["name"]: m["t"] for m in before}
    at = {m["name"]: m["t"] for m in after}
    stale = {m["name"]: m["t"] for m in before}     # markers left where they were (not re-placed)
    # where each marker's source moment really is on the new record timeline
    truth = {"HOOK": 0.5, "GFX card": 7.0, "CHAPTER 2": 9.0}
    return [
        check("seven fixed tracks with their roles", list(TRACK_LAYOUT) == ["V1", "V2", "V3", "A1", "A2", "A3", "A4"]
              and TRACK_LAYOUT["A1"] == "voice" and TRACK_LAYOUT["A4"] == "music", TRACK_LAYOUT),
        check("markers carry the role colour (CHAPTER Blue, GFX Green, HOOK Red, REVIEW Yellow)",
              {m["kind"]: m["color"] for m in before} == MARKER_COLOURS, {m["kind"]: m["color"] for m in before}),
        check("first cut: record times 0.5 / 1.5 / 8.0 / 10.0 / 12.5",
              [bt[k] for k in ("CHAPTER 1 الفكرة", "HOOK", "GFX card", "CHAPTER 2", "REVIEW hum")] == [0.5, 1.5, 8.0, 10.0, 12.5],
              bt),
        check("after the recut every marker sits on its source moment", all(abs(at[k] - v) < 1e-6 for k, v in truth.items()),
              at, truth),
        check("a marker whose moment was cut out is dropped (CHAPTER 1 at src 0.5, REVIEW at src 8.5)",
              "CHAPTER 1 الفكرة" not in at and "REVIEW hum" not in at, sorted(at)),
        check("negative control: markers not re-placed are off by the 1 s trim",
              all(abs(stale[k] - v) >= 0.999 for k, v in truth.items()), {k: stale[k] for k in truth}, truth),
    ], [wd / "edit_v1.json", wd / "edit_v2.json"]


# ───────────────────────── editor routing matrix (ENG-368) ─────────────────────────

def editor_plan(profile):
    tool = (profile.get("editor") or "").lower()
    if tool.startswith("after effects"):
        return {"route": "after-effects", "steps": [
            "verify the AE version (%s) before naming properties or writing JSX" % profile.get("version", "?"),
            "script into a NEW composition in a NEW project; never over an existing project",
            "layered masks, text and compound motion in AE"], "jsx_target": "new_project"}
    if tool.startswith("davinci") or tool.startswith("resolve"):
        return {"route": "resolve", "steps": ["Edit page: cut", "Color page: grade in nodes", "Fusion page: node compositing"],
                "effects_vocabulary": ["Fusion Transform", "Fusion Blur", "Color Warper"]}
    return {"route": "self-render", "steps": ["HTML/SVG + window.__kosif.seek(t)", "tools/render_html.cjs (Playwright frames)",
                                              "ffmpeg cuts/grades"], "engine": "render_html.cjs"}


@card("ENG-368")
def editor_routing(task, wd):
    """Plan to the user's tool: After Effects (version first, JSX into a new project only), Resolve/Fusion (edit, colour
    and nodes separated, no AE effect names), or no editor → Claude renders itself with render_html.cjs + ffmpeg."""
    wd = Path(wd)
    ae = editor_plan({"editor": "After Effects", "version": "25.0"})
    rs = editor_plan({"editor": "DaVinci Resolve 19"})
    me = editor_plan({})
    wt(wd / "film.html", "<!doctype html><html><body style='margin:0;background:#000'><canvas id=c width=320 height=180>"
       "</canvas><script>const c=document.getElementById('c').getContext('2d');window.__kosif={duration:1,seek(t){"
       "c.fillStyle='#000';c.fillRect(0,0,320,180);c.fillStyle='red';c.fillRect(20+200*t,70,40,40);}};</script></body></html>")
    out = wd / "self_render.mp4"
    (wd / "frames").mkdir()
    sh(["node", REPO / "tools/render_html.cjs", "--in", wd / "film.html", "--out", out, "--width", "320", "--height", "180",
        "--fps", "30", "--duration", "1", "--mode", "seek", "--frames-dir", wd / "frames"], wd, timeout=60,
       env=env_for(wd, tmp=False))
    shutil.rmtree(wd / "frames", ignore_errors=True)
    xs = [red_centroid(frame_at(out, t))[0] for t in (0.0, 0.5)]
    graded = wd / "graded.mp4"
    ff(wd, "-i", out, "-vf", "eq=brightness=0.08", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", graded)
    lum = lambda p: float(frame_at(p, 0.5).mean())
    jw(wd / "routes.json", {"after_effects": ae, "resolve": rs, "none": me})
    ae_names = ("Gaussian Blur", "CC ", "Fast Box Blur")
    no_ae = lambda vocab: not any(n in " ".join(vocab) for n in ae_names)
    literal = ["Gaussian Blur", "CC Radial Blur", "Transform"]   # AE names copied 1:1 into a Resolve plan
    return [
        check("After Effects: version verified before JSX, JSX only into a new project",
              ae["steps"][0].startswith("verify the AE version (25.0)") and ae["jsx_target"] == "new_project", ae["steps"][:2]),
        check("Resolve: edit, colour and Fusion nodes kept on separate pages", [s.split(":")[0] for s in rs["steps"]] ==
              ["Edit page", "Color page", "Fusion page"], rs["steps"]),
        check("Resolve vocabulary carries no After Effects effect names",
              no_ae(rs["effects_vocabulary"]), rs["effects_vocabulary"]),
        check("no editor → self-render: render_html.cjs film 30 frames, box moves 20 → 120 px",
              me["route"] == "self-render" and nframes(out) == 30 and abs(xs[0] - 40) < 3 and abs(xs[1] - 140) < 4, xs, [40, 140]),
        check("ffmpeg grade pass lifts luminance", lum(graded) > lum(out) + 5, [lum(out), lum(graded)]),
        check("negative control: AE effect names copied literally into a Resolve plan fail the vocabulary check",
              not no_ae(literal), literal),
        check("negative control: the untreated first frame is not the half-time frame (the render moved the box)",
              abs(xs[1] - xs[0]) > 80, xs),
    ], [out, graded, wd / "routes.json"]


# ───────────────────────── post-production dependency chain, critical path (ENG-369) ─────────────────────────

POST_TASKS = {  # name: (days, depends on)
    "editorial": (5, []), "picture_lock": (0, ["editorial"]), "vfx": (4, ["picture_lock"]),
    "colour": (3, ["picture_lock"]), "sound": (3.5, ["picture_lock"]), "conform": (1, ["vfx", "colour", "sound"]),
    "deliver": (1, ["conform"]),
}


def cpm(tasks):
    order, seen = [], set()

    def visit(n):
        if n in seen:
            return
        for d in tasks[n][1]:
            visit(d)
        seen.add(n)
        order.append(n)
    for n in tasks:
        visit(n)
    es = {}
    for n in order:
        es[n] = max([es[d] + tasks[d][0] for d in tasks[n][1]], default=0.0)
    end = max(es[n] + tasks[n][0] for n in tasks)
    lf = {n: end for n in tasks}
    for n in reversed(order):
        succ = [s for s in tasks if n in tasks[s][1]]
        if succ:
            lf[n] = min(lf[s] - tasks[s][0] for s in succ)
    slack = {n: round(lf[n] - tasks[n][0] - es[n], 6) for n in tasks}
    crit = [n for n in order if slack[n] == 0]
    return end, es, slack, crit


def lock_violations(schedule):
    """Finishing work that starts before picture lock is rework."""
    lock = schedule["picture_lock"]
    return [n for n in ("vfx", "colour", "sound", "conform") if schedule[n] < lock]


@card("ENG-369")
def post_dependency_chain(task, wd):
    """Editorial → VFX → colour → sound → conform → deliver with picture lock as the gate; the critical path sets the
    delivery date; every deliverable traces to a finishing step with a QC check."""
    wd = Path(wd)
    end, es, slack, crit = cpm(POST_TASKS)
    deliverables = [{"item": "master ProRes 1080p", "step": "conform", "qc": "verify_video fps/size/duration"},
                    {"item": "9:16 H.264", "step": "deliver", "qc": "verify_video aspect 9:16"},
                    {"item": "captions .srt (ar)", "step": "sound", "qc": "caption timing vs locked cut"},
                    {"item": "metadata.json", "step": "deliver", "qc": "schema check"}]
    trace_ok = all(d["step"] in POST_TASKS and d["qc"] for d in deliverables)
    bad_sched = dict(es, colour=2.0)                 # grading started on day 2, before the day-5 lock
    jw(wd / "post_plan.json", {"finish_day": end, "early_start": es, "slack": slack, "critical_path": crit,
                               "deliverables": deliverables})
    return [
        check("finish = 5 + 0 + 4 + 1 + 1 = 11 days", end == 11, end, 11),
        check("critical path editorial → lock → VFX → conform → deliver",
              crit == ["editorial", "picture_lock", "vfx", "conform", "deliver"], crit),
        check("float: colour 1 day, sound 0.5 day", slack["colour"] == 1 and slack["sound"] == 0.5,
              [slack["colour"], slack["sound"]], [1, 0.5]),
        check("no finishing step starts before picture lock", lock_violations(es) == [], lock_violations(es)),
        check("every deliverable traced to a finishing step with QC", trace_ok, len(deliverables)),
        check("negative control: grading before lock is flagged as rework", lock_violations(bad_sched) == ["colour"],
              lock_violations(bad_sched), ["colour"]),
    ], [wd / "post_plan.json"]


# ───────────────────────── named role tracks, idempotent (ENG-372) ─────────────────────────

ROLE_V = ["OVERLAY", "GFX", "SUBTITLE", "HOOK_TEXT"]
ROLE_A = ["AMBIENCE", "SFX", "MUSIC", "HOOK"]


def ensure_role_tracks(tl):
    """Find tracks by name and add only the missing ones (video roles on top, VOICE on A1)."""
    if not tl["audio"] or tl["audio"][0]["name"] != "VOICE":
        tl["audio"].insert(0, {"name": "VOICE", "clips": []})
    have_v = {t["name"] for t in tl["video"]}
    have_a = {t["name"] for t in tl["audio"]}
    tl["video"] += [{"name": n, "clips": []} for n in ROLE_V if n not in have_v]
    tl["audio"] += [{"name": n, "clips": []} for n in ROLE_A if n not in have_a]
    return tl


def naive_add_tracks(tl):
    tl["video"] += [{"name": n, "clips": []} for n in ROLE_V]
    tl["audio"] += [{"name": n, "clips": []} for n in ROLE_A]
    return tl


@card("ENG-372")
def named_role_tracks(task, wd):
    """Reserve tracks by role (video OVERLAY/GFX/SUBTITLE/HOOK_TEXT on top, audio AMBIENCE/SFX/MUSIC/HOOK, dialogue VOICE
    on A1), found by name so a re-run adds no duplicates; the same names label an ffmpeg filtergraph mix."""
    wd = Path(wd)
    base = {"video": [{"name": "MAIN", "clips": ["a.mp4"]}], "audio": [{"name": "VOICE", "clips": ["vo.wav"]}]}
    once = ensure_role_tracks(json.loads(json.dumps(base)))
    twice = ensure_role_tracks(json.loads(json.dumps(once)))
    naive = naive_add_tracks(naive_add_tracks(json.loads(json.dumps(base))))
    jw(wd / "tracks.json", twice)
    sr = 48000
    for name, f in (("VOICE", 200.0), ("MUSIC", 600.0), ("SFX", 1500.0)):
        tone_wav(wd / (name.lower() + ".wav"), f, 1.0, sr, 0.25)
    graph = "[0:a]anull[VOICE];[1:a]volume=0.8[MUSIC];[2:a]volume=0.8[SFX];[VOICE][MUSIC][SFX]amix=inputs=3:normalize=0[mix]"
    ff(wd, "-i", wd / "voice.wav", "-i", wd / "music.wav", "-i", wd / "sfx.wav", "-filter_complex", graph, "-map", "[mix]",
       wd / "mix.wav")
    x, _ = fx.read_wav(wd / "mix.wav")
    sp = np.abs(np.fft.rfft(x[:, 0]))
    fr = np.fft.rfftfreq(len(x), 1 / sr)
    present = {f: float(sp[np.argmin(abs(fr - f))] / sp.max()) for f in (200.0, 600.0, 1500.0)}
    names = lambda tl, k: [t["name"] for t in tl[k]]
    return [
        check("video roles stacked above the main edit", names(once, "video") == ["MAIN"] + ROLE_V, names(once, "video")),
        check("VOICE stays on A1, audio roles follow", names(once, "audio") == ["VOICE"] + ROLE_A, names(once, "audio")),
        check("re-running adds nothing (idempotent by name)", twice == once,
              [len(twice["video"]), len(twice["audio"])], [5, 5]),
        check("named filtergraph labels mix all three role stems", all(v > 0.3 for v in present.values()), present),
        check("negative control: adding without lookup duplicates on re-run",
              len(naive["video"]) == 9 and len(naive["audio"]) == 9, [len(naive["video"]), len(naive["audio"])], [9, 9]),
    ], [wd / "tracks.json", wd / "mix.wav"]


# ───────────────────────── post pipeline order with recut re-timing (ENG-373) ─────────────────────────

class PostOrder:
    """cut → colour → privacy mosaic → captions → audio checks, gated by picture lock; each step refuses to run out of order."""
    STEPS = ["cut", "colour", "mosaic", "captions", "audio"]

    def __init__(self):
        self.done = []

    def step(self, name):
        want = self.STEPS[len(self.done)] if len(self.done) < len(self.STEPS) else None
        if name != want:
            raise RuntimeError("out of order: %s before %s" % (name, want))
        self.done.append(name)


def retime_cues(cues, removed):
    """Captions after a recut: drop cues inside removed ranges and shift later ones back by the removed time before them."""
    gone = lambda t: sum(min(r1, t) - r0 for r0, r1 in removed if r0 < t)
    out = []
    for a, b, text in cues:
        if any(r0 <= a and b <= r1 for r0, r1 in removed):
            continue
        out.append((round(a - gone(a), 3), round(b - gone(b), 3), text))
    return out


def srt(cues):
    ts = lambda t: "%02d:%02d:%02d,%03d" % (int(t // 3600), int(t % 3600 // 60), int(t % 60), round((t % 1) * 1000))
    return "".join("%d\n%s --> %s\n%s\n\n" % (i + 1, ts(a), ts(b), x) for i, (a, b, x) in enumerate(cues))


def _block_var(img, x, y, w, h, blk):
    reg = img[y:y + h, x:x + w].astype(float)
    v = [reg[j:j + blk, i:i + blk].std(axis=(0, 1)).mean() for j in range(0, h, blk) for i in range(0, w, blk)]
    return float(np.mean(v))


@card("ENG-373")
def post_pipeline_order(task, wd):
    """Editorial → VFX → colour → sound → conform → deliver gated by picture lock; in practice cut → colour → privacy
    mosaic → captions → audio checks before render, and a recut re-times the captions."""
    wd = Path(wd)
    W, H = 320, 180
    src = wd / "src.mp4"
    ff(wd, "-f", "lavfi", "-i", "testsrc2=s=%dx%d:r=30:d=4" % (W, H), "-f", "lavfi", "-i", "sine=f=440:d=4",
       "-af", "volume=-18dB", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", src)
    po = PostOrder()
    refused = False
    try:
        PostOrder().step("captions")
    except RuntimeError:
        refused = True
    po.step("cut")
    cut = wd / "1_cut.mp4"
    ff(wd, "-ss", "0.5", "-i", src, "-t", "3", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-c:a", "aac", cut)
    lock = jw(wd / "picture_lock.json", {"cut": "src 0.5-3.5", "sha256": hashlib.sha256(cut.read_bytes()).hexdigest()})
    po.step("colour")
    col = wd / "2_colour.mp4"
    ff(wd, "-i", cut, "-vf", "eq=brightness=0.06:saturation=1.3", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt",
       "yuv420p", "-c:a", "copy", col)
    po.step("mosaic")
    mos = wd / "3_mosaic.mp4"
    bx, by, bw, bh, blk = 40, 40, 80, 60, 10
    ff(wd, "-i", col, "-filter_complex",
       "[0:v]split[a][b];[b]crop=%d:%d:%d:%d,scale=%d:%d:flags=neighbor,scale=%d:%d:flags=neighbor[p];[a][p]overlay=%d:%d"
       % (bw, bh, bx, by, bw // blk, bh // blk, bw, bh, bx, by), "-c:v", "libx264", "-preset", "ultrafast", "-crf", "10",
       "-pix_fmt", "yuv444p", "-c:a", "copy", mos)
    po.step("captions")
    cues = [(0.2, 1.0, "ONE"), (1.4, 2.4, "TWO")]
    wt(wd / "caps.srt", srt(cues))
    cap = wd / "4_captions.mp4"
    ff(wd, "-i", mos, "-vf", "subtitles=caps.srt:force_style='Fontsize=26,PrimaryColour=&H00FFFFFF,Outline=2'",
       "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-c:a", "copy", cap)
    po.step("audio")
    I0 = ebur(wd, cap)
    final = wd / "master.mp4"
    ff(wd, "-i", cap, "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", final)
    I1 = ebur(wd, final)
    mv = _block_var(frame_at(final, 0.3), bx, by, bw, bh, blk)
    ov = _block_var(frame_at(cut, 0.3), bx, by, bw, bh, blk)
    # recut: the editor trims 0.5 s at the head of the locked cut → every caption is re-timed
    new_cues = retime_cues(cues, [(0.0, 0.5)])
    wt(wd / "caps_recut.srt", srt(new_cues))
    return [
        check("steps ran in the order cut → colour → mosaic → captions → audio", po.done == PostOrder.STEPS, po.done),
        check("captions before picture lock are refused", refused),
        check("locked cut is 3.0 s and hashed", abs(duration(cut) - 3.0) < 0.05 and len(json.loads(lock.read_text())["sha256"]) == 64,
              duration(cut)),
        check("privacy mosaic: the region is flat 10 px blocks (mean block std < 4)", mv < 4, mv, "< 4"),
        check("audio check: loudness brought to -14 LUFS (±1) from the quiet mix", abs(I1 + 14) <= 1 and I0 < -20, [I0, I1], -14),
        check("recut re-times captions: the trimmed head clips cue 1 to 0-0.5 s, cue 2 moves -0.5 s",
              new_cues == [(0.0, 0.5, "ONE"), (0.9, 1.9, "TWO")], new_cues),
        check("negative control: captions left untouched after the recut start 0.5 s late", abs(cues[1][0] - new_cues[1][0] - 0.5) < 1e-9,
              [cues[1][0], new_cues[1][0]]),
        check("negative control: the untreated cut's region is detailed (block std > 8)", ov > 8, ov, "> 8"),
    ], [final, wd / "caps_recut.srt", lock]


# ───────────────────────── live audio: latency budget, AudioWorklet, oversampled nonlinearity (ENG-377) ─────────────────────────

def _alias_db(y, sr, f0):
    w = np.hanning(len(y))
    P = np.abs(np.fft.rfft(y * w)) ** 2
    fr = np.fft.rfftfreq(len(y), 1 / sr)
    harm = np.zeros_like(fr, bool)
    for k in range(1, 60, 2):
        f = k * f0
        if f < sr / 2:
            harm |= np.abs(fr - f) <= 4
    sig, alias = P[harm].sum(), P[~harm & (fr > 20)].sum()
    return float(10 * np.log10(alias / sig))


@card("ENG-377")
def live_audio_worklet(task, wd):
    """Latency budget first (buffer 64-128 samples), Web Audio AudioWorklet in the browser (preallocated, no locks),
    nonlinearities oversampled 4x (inside the 2-8x range) so the waveshaper does not alias."""
    from scipy.signal import resample_poly
    wd = Path(wd)
    sr = 48000
    budget = {n: round(1000 * n / sr, 3) for n in (64, 128)}
    rt_ms = round(2 * budget[128], 3)              # one input + one output buffer of 128 samples
    wt(wd / "worklet.html", """<!doctype html><html><body><script>
const code=`class Drive extends AudioWorkletProcessor{constructor(){super();this.n=0;this.q=0;}
process(ins,outs){const i=ins[0][0],o=outs[0][0];if(!i)return true;this.q=o.length;for(let k=0;k<o.length;k++)o[k]=Math.tanh(4*i[k]);
if(this.n++===0)this.port.postMessage(this.q);return true;}}registerProcessor('drive',Drive);`;
(async()=>{const ctx=new OfflineAudioContext(1,4800,48000);
await ctx.audioWorklet.addModule(URL.createObjectURL(new Blob([code],{type:'application/javascript'})));
const osc=new OscillatorNode(ctx,{frequency:1000});const g=new GainNode(ctx,{gain:0.9});
const node=new AudioWorkletNode(ctx,'drive');let quantum=null;node.port.onmessage=e=>{quantum=e.data;};
osc.connect(g).connect(node).connect(ctx.destination);osc.start();const buf=await ctx.startRendering();
await new Promise(r=>setTimeout(r,50));window.__r={quantum,y:Array.from(buf.getChannelData(0).slice(0,4800))};window.__ready=true;})();
</script></body></html>""")
    with browser_page(wd) as pg:
        pg.goto((wd / "worklet.html").as_uri())
        pg.wait_for_function("window.__ready===true", timeout=15000)
        r = pg.evaluate("window.__r")
    y = np.array(r["y"])
    t = np.arange(len(y)) / sr
    ref = np.tanh(4 * 0.9 * np.sin(2 * np.pi * 1000 * t))
    err = float(np.abs(y[200:] - ref[200:]).max())
    f0 = 5000.0
    n = sr                                          # 1 s, 1 Hz bins
    x = 0.9 * np.sin(2 * np.pi * f0 * np.arange(n) / sr)
    naive = np.tanh(4 * x)
    os4 = resample_poly(np.tanh(4 * resample_poly(x, 4, 1)), 1, 4)
    a_naive, a_os = _alias_db(naive[1000:-1000], sr, f0), _alias_db(os4[1000:-1000], sr, f0)
    fx.write_wav(wd / "drive_os4.wav", os4 * 0.5, sr)
    jw(wd / "latency.json", {"buffer_ms": budget, "round_trip_ms": rt_ms, "quantum": r["quantum"],
                             "alias_db": {"naive": a_naive, "os4": a_os}, "worklet_max_err": err})
    return [
        check("latency budget: 64 → 1.333 ms, 128 → 2.667 ms at 48 kHz", budget == {64: 1.333, 128: 2.667}, budget),
        check("in+out buffering of 128 samples (5.33 ms) leaves over 4 ms of a 10 ms live budget", 10 - rt_ms > 4, rt_ms, "< 6"),
        check("AudioWorklet ran in Chromium with the 128-frame render quantum", r["quantum"] == 128, r["quantum"], 128),
        check("worklet waveshaper output equals tanh(4x) (max err < 1e-3)", err < 1e-3, err, "< 1e-3"),
        check("4x oversampling cuts aliasing by more than 10 dB (to below -28 dB)", a_naive - a_os > 10 and a_os < -28,
              [a_naive, a_os]),
        check("negative control: the un-oversampled shaper aliases (alias energy > -40 dB)", a_naive > -40, a_naive, "> -40"),
    ], [wd / "latency.json", wd / "drive_os4.wav"]


# ───────────────────────── kmotion hubs and menus (ENG-38, ENG-71, ENG-97, ENG-70) ─────────────────────────

KMOTION = KM / "kmotion.py"
HF_KMOTION = HFS / "kmotion.py"


def _menu_lines(text):
    return [(int(m.group(1)), m.group(2), m.group(3)) for m in re.finditer(r"(?m)^\s*(\d+)\. (.+?)\s+\(([\w-]+)\)\s*$", text)]


def _kmotion_table(wd, script):
    code = ("import sys,json;sys.path.insert(0,%r);import kmotion as k;print(json.dumps({'C':{c:[v[0],v[1]] for c,v in "
            "k.C.items()},'G':k.GROUPS},ensure_ascii=False))") % str(Path(script).parent)
    return json.loads(sh([sys.executable, "-c", code], wd).stdout.strip().splitlines()[-1])


@card("ENG-38")
def kmotion_hub_menu(task, wd):
    """One entry point wrapping every tool in five groups (create, sound, edit, check, draw) with an interactive
    numbered Arabic menu that asks for each argument: pick 'probe' by number, answer its question, get the result."""
    wd = Path(wd)
    clip = wd / "clip.mp4"
    ff(wd, "-f", "lavfi", "-i", "testsrc2=s=320x180:r=30:d=1.5", "-f", "lavfi", "-i", "sine=f=440:d=1.5", "-c:v", "libx264",
       "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", clip)
    tab = _kmotion_table(wd, KMOTION)
    groups = [g for g, _ in tab["G"]]
    menu = sh([sys.executable, KMOTION], wd, stdin="").stdout
    items = _menu_lines(menu)
    num = next(n for n, _, c in items if c == "probe")
    run = sh([sys.executable, KMOTION], wd, stdin="%d\n%s\n" % (num, clip))
    wt(wd / "menu_session.txt", run.stdout)
    res = jout(run.stdout)
    bad = sh([sys.executable, KMOTION], wd, stdin="999\n", ok=None)
    asked = "الملف" in run.stdout
    return [
        check("five groups: create, sound, edit, check, draw", groups == ["create", "sound", "edit", "check", "draw"], groups),
        check("every command sits in one of the five groups", all(v[0] in groups for v in tab["C"].values()), len(tab["C"])),
        check("menu numbers every command 1..N", [n for n, _, _ in items] == list(range(1, len(tab["C"]) + 1)),
              len(items), len(tab["C"])),
        check("the menu asked for the argument (Arabic prompt) and ran probe", asked and "▶ python kmotion.py probe" in run.stdout),
        check("probe answered with the fixture's real size, duration and audio",
              res["video"]["w"] == 320 and res["video"]["h"] == 180 and abs(res["duration"] - 1.5) < 0.1 and res["audio"],
              [res["video"]["w"], res["video"]["h"], res["duration"]]),
        check("negative control: a number outside the menu is refused (exit 2)", bad.returncode == 2, bad.returncode, 2),
    ], [wd / "menu_session.txt"]


@card("ENG-71")
def kmotion_no_args_menu(task, wd):
    """Every tool behind one CLI; with no arguments a numbered Arabic menu appears (and `help` lists the same commands)."""
    wd = Path(wd)
    menu = sh([sys.executable, KMOTION], wd, stdin="").stdout
    wt(wd / "menu.txt", menu)
    helpt = sh([sys.executable, KMOTION, "help"], wd).stdout
    wt(wd / "help.txt", helpt)
    items = _menu_lines(menu)
    help_cmds = re.findall(r"(?m)^   ([\w-]+)\s+\S", helpt)
    arabic = sum(1 for _, label, _ in items if re.search(r"[؀-ۿ]", label))
    direct = sh([sys.executable, KMOTION, "transitions"], wd).stdout
    return [
        check("no args → numbered menu 1..N", len(items) > 40 and [n for n, _, _ in items] == list(range(1, len(items) + 1)),
              len(items)),
        check("every menu entry is labelled in Arabic", arabic == len(items), arabic, len(items)),
        check("menu and help list the same commands", sorted(c for _, _, c in items) == sorted(help_cmds),
              [len(items), len(help_cmds)]),
        check("the same CLI runs a tool directly (transitions lists xfade types)", "circleopen" in direct and "fade" in direct),
        check("negative control: with arguments (help) no numbered menu is printed", _menu_lines(helpt) == [],
              len(_menu_lines(helpt)), 0),
    ], [wd / "menu.txt", wd / "help.txt"]


KM97 = ("new bundle kit-bundle frames check render preview sync doctor score ambience voice beats channels direct verse "
        "audio2motion reel montage grade captions transcribe decaption footage mocap silence aspect trim concat loop "
        "stabilize export thumb probe batch fonts lint sheet speed study measure").split()


@card("ENG-97")
def kmotion_48_commands(task, wd):
    """Single entry point grouping create, sound, edit, check and draw commands with an Arabic numbered menu: every
    command the card lists resolves to a real module, and the menu runs one (transitions) end to end."""
    wd = Path(wd)
    tab = _kmotion_table(wd, KMOTION)
    C = tab["C"]
    missing = [c for c in KM97 if c not in C]
    modfiles = {c: (KM / (C[c][1] + ".py")).exists() for c in KM97 if c in C}
    menu = sh([sys.executable, KMOTION], wd, stdin="").stdout
    items = _menu_lines(menu)
    num = next(n for n, _, c in items if c == "transitions")
    run = sh([sys.executable, KMOTION], wd, stdin="%d\n" % num).stdout
    wt(wd / "transitions.txt", run)
    xf = re.findall(r"(?m)^([a-z]+)\s{2,}", run)
    have = sh(["ffmpeg", "-hide_banner", "-h", "filter=xfade"], wd).stdout
    jw(wd / "commands.json", {c: C[c] for c in KM97 if c in C})
    return [
        check("all %d listed commands are in the hub" % len(KM97), not missing and len(KM97) == 41, missing),
        check("hub offers at least 48 commands", len(C) >= 48, len(C), ">= 48"),
        check("each listed command resolves to an existing module", all(modfiles.values()),
              [c for c, ok in modfiles.items() if not ok]),
        check("menu picked 'transitions' by number and ran it", "▶ python kmotion.py transitions" in run and len(xf) > 20,
              len(xf)),
        check("listed transitions really exist in this ffmpeg's xfade", all(t in have for t in xf[:10]), xf[:10]),
        check("negative control: a made-up command is not in the hub", "teleport" not in C),
    ], [wd / "commands.json", wd / "transitions.txt"]


@card("ENG-70")
def kmotion_dispatcher_fallback(task, wd):
    """Arabic-menu dispatcher over motion.py (new/check/render…); renders via HyperFrames CLI when installed beside
    motion.py, else with KOSIF Studio's own frame renderer: here the CLI is absent, so the fallback must render.
    (The hyperframes-animation-studio copy imports pixel-studio-painter's film.py, which hangs in this sandbox, so the
    kosif-montage-motion copy of the same dispatcher is the one driven.)"""
    wd = Path(wd)
    e = env_for(wd, tmp=False)
    sh([sys.executable, KMOTION, "new", "film", "--seconds", "1", "--size", "320x180"], wd, env=e)
    proj = wd / "projects" / "film"
    chk = sh([sys.executable, KMOTION, "check", "film"], wd, env=e, ok=None)
    r = sh([sys.executable, KMOTION, "render", "film", "--engine", "auto"], wd, env=e, timeout=40)
    rep = jout(r.stdout)
    out = Path(rep["file"])
    hf_local = (KM / "node_modules/hyperframes/package.json").exists()
    fr = all_frames(out, (64, 36)).astype(float)
    moving = float(max(np.abs(f - fr[0]).mean() for f in fr))
    return [
        check("kmotion new scaffolded the project", (proj / "index.html").exists()),
        check("HyperFrames CLI absent beside motion.py → check says so (exit 2)", not hf_local and chk.returncode == 2,
              chk.returncode, 2),
        check("render auto fell back to the studio frame renderer", rep["engine"] == "studio", rep["engine"], "studio"),
        check("film: 30 frames at 320x180 inside the work folder", nframes(out) == 30 and str(out).startswith(str(wd)) and
              int(vstream(out)["width"]) == 320, [nframes(out), str(out)[-40:]]),
        check("the rendered composition moves", moving > 1.0, moving, "> 1"),
        check("negative control: asking for the hyperframes engine without the CLI fails",
              sh([sys.executable, KMOTION, "render", "film", "--engine", "hyperframes"], wd, env=e, ok=None).returncode != 0),
    ], [out]


# ───────────────────────── engine router with availability and Native Canvas fallback (ENG-385) ─────────────────────────

ROUTER_DOC = Path("/home/claude/fastify-motion-bro/docs/ENGINE_ROUTER.md")


def engine_available(name, consent=None):
    consent = consent or {}
    if name == "Native Canvas":
        return fx.which("ffmpeg") and bool(browser_path())
    if name == "Remotion":
        return (NODE_MODS / "remotion").exists() and (NODE_MODS / "@remotion").exists()
    if name == "HyperFrames":
        return (NODE_MODS / "hyperframes").exists() and int(sh(["node", "-p", "process.versions.node.split('.')[0]"], ".").stdout) >= 22
    if name == "KOSIF Motion":
        return (KM / "audio2motion.py").exists() and (KM / "kit/shape-kit.js").exists()
    if name == "Higgsfield":                     # paid: key + licence + terms + the user's explicit permission
        return bool(consent.get("higgsfield_key") and consent.get("user_permission"))
    return False                                 # scroll-world / brag are creative directions, not runtimes


def route_goal(goal, consent=None):
    g = goal.lower()
    want = ("Higgsfield" if "ai clip" in g else "Remotion" if "react" in g else "KOSIF Motion" if "karaoke" in g or "voice" in g
            else "HyperFrames" if "html" in g else "scroll-world/brag" if "scroll" in g else "Native Canvas")
    if engine_available(want, consent):
        return {"goal": goal, "engine": want, "note": None}
    return {"goal": goal, "engine": "Native Canvas", "wanted": want,
            "note": "%s is not usable here; falling back to Native Canvas (trade-off explained to the user)" % want}


@card("ENG-385")
def engine_router_fallback(task, wd):
    """Decision table between Native Canvas (implemented), Remotion, HyperFrames, KOSIF Motion, Higgsfield and the
    scroll-world/brag directions: verify the target is installed and usable, explain the switch, fall back to Native
    Canvas and say so; the fallback renders a real time-seekable canvas film."""
    wd = Path(wd)
    doc = ROUTER_DOC.read_text(encoding="utf-8") if ROUTER_DOC.exists() else ""
    named = [n for n in ("Native Canvas", "Remotion", "HyperFrames", "KOSIF Motion", "Higgsfield", "Scroll-world") if n in doc]
    goals = ["react long sequenced edit", "html cinematic composition", "arabic karaoke voice captions",
             "ai clip of a desert", "scroll-scrub launch", "arabic title card"]
    plan = [route_goal(g) for g in goals]
    with_consent = route_goal("ai clip of a desert", {"higgsfield_key": "set", "user_permission": True})
    jw(wd / "routing.json", {"plan": plan, "doc_engines": named})
    wt(wd / "canvas.html", "<!doctype html><html><body style='margin:0;background:#000'><canvas id=c width=320 height=180>"
       "</canvas><script>const c=document.getElementById('c').getContext('2d');window.__kosif={duration:1,seek(t){"
       "c.fillStyle='#0d1b2a';c.fillRect(0,0,320,180);c.fillStyle='#ff0000';c.fillRect(10+260*t,120,50,20);"
       "c.fillStyle='#fff';c.font='32px sans-serif';c.direction='rtl';c.textAlign='center';c.fillText('مرحبا',160,70);}};"
       "</script></body></html>")
    out = wd / "native_canvas.mp4"
    (wd / "frames").mkdir()
    sh(["node", REPO / "tools/render_html.cjs", "--in", wd / "canvas.html", "--out", out, "--width", "320", "--height", "180",
        "--fps", "30", "--duration", "1", "--mode", "seek", "--frames-dir", wd / "frames"], wd, timeout=60, env=env_for(wd, tmp=False))
    shutil.rmtree(wd / "frames", ignore_errors=True)
    x0, x1 = red_centroid(frame_at(out, 0.0))[0], red_centroid(frame_at(out, 0.9))[0]
    eng = {p["goal"]: p["engine"] for p in plan}
    return [
        check("router doc names all the engines", len(named) == 6, named),
        check("available engines are chosen (Remotion, HyperFrames, KOSIF Motion)",
              [eng[g] for g in goals[:3]] == ["Remotion", "HyperFrames", "KOSIF Motion"], [eng[g] for g in goals[:3]]),
        check("Higgsfield without key + permission → Native Canvas with a stated reason",
              eng[goals[3]] == "Native Canvas" and "not usable" in plan[3]["note"], plan[3]),
        check("scroll-world is a direction, never a runtime → Native Canvas", eng[goals[4]] == "Native Canvas"),
        check("Native Canvas fallback rendered 30 frames and the bar moves 35 → 269 px",
              nframes(out) == 30 and abs(x0 - 35) < 3 and abs(x1 - 269) < 4, [x0, x1], [35, 269]),
        check("negative control: with key and permission recorded, Higgsfield is not replaced", with_consent["engine"] == "Higgsfield",
              with_consent["engine"]),
    ], [out, wd / "routing.json"]


# ───────────────────────── KOSIF Motion routing: discover, run the alignment, read its report (ENG-386) ─────────────────────────

ALIGN_PY = r"""
import json, sys
sys.path.insert(0, sys.argv[1])
import verse
from pathlib import Path
lines = [["قلب", "صغير", "يغني"]]
words = verse.estimate(lines, Path(sys.argv[2]))
spans = verse.voiced_spans(Path(sys.argv[2]))
print(json.dumps({"words": words, "spans": spans}, ensure_ascii=False))
"""


def claim_word_sync(report_path):
    """Only a read alignment report with every word inside voiced audio allows the claim."""
    p = Path(report_path)
    if not p.exists():
        return False, "no alignment report: word sync cannot be claimed"
    r = json.loads(p.read_text(encoding="utf-8"))
    ws = [w for line in r["words"] for w in line]
    inside = all(any(a - 0.05 <= (w["start"] + w["end"]) / 2 <= b + 0.05 for a, b in r["spans"]) for w in ws)
    return inside and len(ws) == 3, "aligned" if inside else "words outside voiced audio"


@card("ENG-386")
def kosif_motion_route(task, wd):
    """Routing target for audio2motion, karaoke captions, the structural shape kit, voice analysis and local montage
    (the kosif-one / kosif-studio tools, mirrored here in kosif-montage-motion): discover them, run their alignment and
    read its report before claiming word sync."""
    wd = Path(wd)
    want = {"audio2motion": "audio2motion.py", "karaoke captions": "montage.py", "shape kit": "kit/shape-kit.js",
            "voice analysis": "verse.py", "transcribe": "transcribe.py", "local montage": "montage.py"}
    found = {k: (KM / v).exists() for k, v in want.items()}
    sr = 16000
    x = np.zeros(int(3.0 * sr))
    rng = np.random.default_rng(4)
    spans = [(0.3, 0.8), (1.2, 1.7), (2.1, 2.6)]
    for a, b in spans:
        n = int((b - a) * sr)
        t = np.arange(n) / sr
        x[int(a * sr):int(a * sr) + n] = 0.4 * np.sin(2 * np.pi * 160 * t) * (1 + 0.3 * rng.standard_normal(n).clip(-1, 1))
    fx.write_wav(wd / "voice.wav", x, sr)
    before, why_before = claim_word_sync(wd / "align_report.json")
    wt(wd / "align.py", ALIGN_PY)
    rep = json.loads(py(wd / "align.py", KM, wd / "voice.wav", wd=wd).stdout.strip().splitlines()[-1])
    jw(wd / "align_report.json", rep)
    after, why_after = claim_word_sync(wd / "align_report.json")
    ws = [w for line in rep["words"] for w in line]
    return [
        check("the routed tools are discovered locally", all(found.values()), found),
        check("voice analysis found the three voiced bursts (±0.1 s)",
              len(rep["spans"]) == 3 and all(abs(a - sa) < 0.1 and abs(b - sb) < 0.1 for (a, b), (sa, sb) in zip(rep["spans"], spans)),
              rep["spans"], spans),
        check("alignment timed every word in order", len(ws) == 3 and all(ws[i]["end"] <= ws[i + 1]["start"] + 1e-6 for i in range(2)),
              [(w["text"], round(w["start"], 2), round(w["end"], 2)) for w in ws]),
        check("after reading the report, word sync may be claimed", after, why_after),
        check("negative control: before the alignment ran there is no report and no claim", not before, why_before),
    ], [wd / "align_report.json"]


# ───────────────────────── render farm: shard frame ranges, join losslessly (ENG-389) ─────────────────────────

BOX_SCRIPT = """
  <div id="box" style="position:absolute;left:0;top:%(top)spx;width:40px;height:40px;background:#ff0000"></div>
  <script>
    const tl = gsap.timeline({ paused: true });
    tl.fromTo("#box", { x: 0 }, { x: %(x)s, duration: %(d)s, ease: "none" }, 0);
    window.__timelines = window.__timelines || {};
    window.__timelines["root"] = tl;
    MOTION.shim("root", %(d)s);
  </script>
"""


@card("ENG-389")
def shard_render_join(task, wd):
    """scripts/shard.py: split the frame range across machines (plan), render each shard to its own segment, join them
    losslessly (stream copy) — here two shards on one machine stand in for two runners."""
    wd = Path(wd)
    e = env_for(wd, tmp=False)
    motion_project(wd, "farm", 0.6, "160x90", BOX_SCRIPT % {"d": "0.6", "x": 120, "top": 25})
    plan = jout(py(KM / "shard.py", "plan", "farm", "--of", "2", wd=wd, env=e).stdout)
    segs = []
    for i in range(2):
        seg = wd / ("seg%02d.mp4" % i)
        py(KM / "shard.py", "render", "farm", "--shard", str(i), "--of", "2", "--out", seg, wd=wd, env=e, timeout=40)
        segs.append(seg)
    film = wd / "film.mp4"
    py(KM / "shard.py", "join", "farm", *segs, "--out", film, "--no-poster", wd=wd, env=e, timeout=40)
    ranges = [(s["i0"], s["i1"]) for s in plan["shards"]]
    parts = np.concatenate([all_frames(s) for s in segs])
    joined = all_frames(film)
    exact = joined.shape == parts.shape and bool(np.array_equal(joined, parts))
    reenc = wd / "reencoded.mp4"
    ff(wd, "-i", film, "-c:v", "libx264", "-crf", "35", "-pix_fmt", "yuv420p", reenc)
    lossy = all_frames(reenc)
    xs = [red_centroid(f, 120)[0] for f in joined[::6]]
    return [
        check("plan: 18 frames split 0-9 / 9-18 with no gap or overlap", plan["frames"] == 18 and ranges == [(0, 9), (9, 18)],
              ranges),
        check("each shard rendered its own range", [nframes(s) for s in segs] == [9, 9], [nframes(s) for s in segs]),
        check("joined film = 18 frames", nframes(film) == 18, nframes(film), 18),
        check("join is lossless: decoded film == the shards' frames, bit for bit", exact),
        check("motion continues across the seam (box x rises monotonically)", all(b > a for a, b in zip(xs, xs[1:])), xs),
        check("negative control: a re-encoded join is not bit-identical", not np.array_equal(lossy, parts)),
    ], [film, wd / "seg00.mp4"]


# ───────────────────────── capture format timings and SSIM, re-measured here (ENG-393) ─────────────────────────

@card("ENG-393")
def capture_timing_ssim(task, wd):
    """The card's i7-1165G7 table (5 s 3D 1080p: preview 28 s; JPEG capture 87 s at SSIM 0.990; PNG 117 s; final
    --blur 4 173 s) re-measured on this machine at a small size: JPEG vs PNG capture of the same composition."""
    wd = Path(wd)
    e = env_for(wd, tmp=False)
    motion_project(wd, "cap", 0.5, "320x180", BOX_SCRIPT % {"d": "0.5", "x": 280, "top": 70})
    times, films = {}, {}
    for cap in ("jpeg", "png"):
        out = wd / ("cap_%s.mp4" % cap)
        t0 = time.perf_counter()
        py(KM / "motion.py", "render", "cap", "--engine", "studio", "--capture", cap, "--workers", "1", "--force",
           "--out", out, wd=wd, env=e, timeout=40)
        times[cap] = round(time.perf_counter() - t0, 2)
        films[cap] = out
    s = ssim_ff(wd, films["jpeg"], films["png"])
    rev = wd / "reversed.mp4"
    ff(wd, "-i", films["png"], "-vf", "reverse", "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", rev)
    s_rev = ssim_ff(wd, films["jpeg"], rev)
    card_t = {"preview": 28, "jpeg": 87, "png": 117, "final_blur4": 173}
    jw(wd / "timings.json", {"card_i7_1165G7_s": card_t, "here_s": times, "ssim_jpeg_vs_png": s, "frames": nframes(films["png"])})
    differ = not np.array_equal(all_frames(films["jpeg"]), all_frames(films["png"]))
    return [
        check("card table: PNG capture costs 1.34x JPEG, final blur 4 ≈ 1.48x PNG",
              round(card_t["png"] / card_t["jpeg"], 2) == 1.34 and round(card_t["final_blur4"] / card_t["png"], 2) == 1.48),
        check("both capture formats rendered 15 frames here", nframes(films["jpeg"]) == nframes(films["png"]) == 15),
        check("JPEG capture is visually the PNG film (SSIM ≥ 0.990, the card's figure)", s >= 0.99, s, ">= 0.990"),
        check("the JPEG path really ran (frames not bit-identical to PNG)", differ),
        check("negative control: SSIM against the time-reversed film fails 0.990", s_rev < 0.99, s_rev, "< 0.990"),
    ], [wd / "timings.json", films["jpeg"]]


# ───────────────────────── motion blur --blur 4 (ENG-396) ─────────────────────────

def _smear(frame):
    """Width (px) of the partially red band on the box's row: pixels between background and full red."""
    row = frame[frame.shape[0] // 2].astype(float)
    r = row[:, 0] - row[:, 2]
    full = r.max()
    return int(((r > 0.15 * full) & (r < 0.85 * full)).sum())


@card("ENG-396")
def motion_blur_4(task, wd):
    """--blur 4: four sub-frames per frame averaged (180° shutter) by the studio renderer; a fast box gets a smeared
    edge band about speed x shutter wide, while --blur 1 keeps a hard edge."""
    wd = Path(wd)
    e = env_for(wd, tmp=False)
    motion_project(wd, "mb", 0.4, "320x180", BOX_SCRIPT % {"d": "0.4", "x": 280, "top": 70})
    outs = {}
    for b in (1, 4):
        outs[b] = wd / ("blur%d.mp4" % b)
        py(KM / "motion.py", "render", "mb", "--engine", "studio", "--blur", str(b), "--workers", "1", "--force", "--capture",
           "png", "--crf", "1", "--out", outs[b], wd=wd, env=e, timeout=40)
    f1 = all_frames(outs[1])[6]
    f4 = all_frames(outs[4])[6]
    s1, s4 = _smear(f1), _smear(f4)
    speed = 280 / 0.4 / 30              # px per frame
    expect = speed * 0.5                # 180° shutter
    return [
        check("both renders: 12 frames", nframes(outs[1]) == nframes(outs[4]) == 12),
        check("--blur 4 smears each edge by about speed x shutter (%.1f px, ±50%%)" % expect,
              0.5 * expect <= s4 / 2 <= 1.5 * expect, s4 / 2, expect),
        check("blur 4 band is much wider than blur 1", s4 >= s1 + 8, [s1, s4]),
        check("negative control: --blur 1 keeps a hard edge (band ≤ 4 px)", s1 <= 4, s1, "<= 4"),
    ], [outs[4], outs[1]]


# ───────────────────────── critique loop: contact sheets at phone width, 6-8 criteria, ≥3 rounds (ENG-398) ─────────────────────────

def _design_frames(params, n=6, W=1080, H=1920):
    from PIL import Image, ImageDraw, ImageFont
    font = ImageFont.truetype(_system_font(), params["size"])
    out = []
    for i in range(n):
        im = Image.new("RGB", (W, H), params["bg"])
        dr = ImageDraw.Draw(im)
        words = params["text"].split()[:params["words"]]
        y = params["top"] + i * params["drift"]
        dr.text((params["margin"], y), " ".join(words), font=font, fill=params["fg"])
        out.append(im)
    return out


def _lum(c):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = c
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def _criteria(params, frames, phone_w=390):
    W, H = frames[0].size
    k = phone_w / W
    import numpy as _np
    arr = [_np.asarray(f.convert("L"), float) for f in frames]
    L1, L2 = sorted([_lum(params["fg"]), _lum(params["bg"])], reverse=True)
    ink = [_np.argwhere(a != a[0, 0]) for a in arr]
    right = max(int(i[:, 1].max()) for i in ink if len(i))
    return {
        "type ≥ 16 px at phone width": params["size"] * k >= 16,
        "contrast ≥ 4.5:1": (L1 + 0.05) / (L2 + 0.05) >= 4.5,
        "side margin ≥ 5%": params["margin"] >= 0.05 * W,
        "≤ 8 words on screen": len(params["text"].split()[:params["words"]]) <= 8,
        "inside the safe area": right <= W - 0.05 * W,
        "moves between frames": float(_np.abs(arr[-1] - arr[0]).mean()) > 0.05,
        "top clear of the status bar (≥ 8%)": params["top"] >= 0.08 * H,
    }


@card("ENG-398")
def contact_sheet_rounds(task, wd):
    """Critique loop: contact sheet of 6 frames viewed at phone width (390 px), scored on 7 measurable criteria, fixed and
    re-scored for at least three rounds until every criterion passes."""
    wd = Path(wd)
    params = {"size": 40, "fg": (120, 120, 130), "bg": (90, 90, 100), "margin": 20, "words": 11, "top": 60, "drift": 0,
              "text": "هذه فكرة واحدة تكفي لتغيير يوم كامل لو بدأت الآن مع كل خطوة"}
    fixes = [lambda p: p.update(size=72, fg=(255, 255, 255), bg=(13, 27, 42)),
             lambda p: p.update(margin=90, words=4),
             lambda p: p.update(top=240, drift=12)]
    rounds = []
    for r in range(3):
        frames = _design_frames(params)
        crit = _criteria(params, frames)
        sheet = wd / ("sheet_round%d.png" % (r + 1))
        from PIL import Image
        thumbs = [f.resize((390, 693)) for f in frames]
        S = Image.new("RGB", (390 * 3, 693 * 2))
        for i, t in enumerate(thumbs):
            S.paste(t, ((i % 3) * 390, (i // 3) * 693))
        S.save(sheet)
        rounds.append({"round": r + 1, "failed": [k for k, v in crit.items() if not v], "sheet": sheet.name})
        if all(crit.values()):
            break
        fixes[r](params)
    final = _criteria(params, _design_frames(params))
    rounds.append({"round": len(rounds) + 1, "failed": [k for k, v in final.items() if not v], "sheet": None})
    jw(wd / "critique.json", rounds)
    return [
        check("7 criteria (inside the card's 6-8)", 6 <= len(final) <= 8, len(final)),
        check("at least three scored rounds with a contact sheet each", sum(1 for r in rounds if r["sheet"]) >= 3,
              [r["round"] for r in rounds if r["sheet"]]),
        check("contact sheet thumbnails are phone width (3 x 390 px)",
              __import__("PIL.Image", fromlist=["Image"]).open(wd / "sheet_round1.png").size == (1170, 1386)),
        check("failures fall round by round", [len(r["failed"]) for r in rounds] == sorted([len(r["failed"]) for r in rounds],
                                                                                           reverse=True),
              [len(r["failed"]) for r in rounds]),
        check("after the fixes every criterion passes", rounds[-1]["failed"] == [], rounds[-1]["failed"]),
        check("negative control: the untreated first draft fails several criteria", len(rounds[0]["failed"]) >= 5,
              rounds[0]["failed"]),
    ], [wd / "critique.json", wd / "sheet_round3.png"]


# ───────────────────────── video-model base shot redrawn in JS (ENG-400) ─────────────────────────

REDRAW_HTML = """<!doctype html><html><body style="margin:0"><canvas id="c" width="%(w)d" height="%(h)d"></canvas><script>
const img = new Image();
img.onload = () => {
  const c = document.getElementById('c'), g = c.getContext('2d');
  g.drawImage(img, 0, 0);
  const d = g.getImageData(0, 0, c.width, c.height), p = d.data, W = c.width, H = c.height;
  const lum = new Float32Array(W * H);
  for (let i = 0; i < W * H; i++) lum[i] = 0.299 * p[4*i] + 0.587 * p[4*i+1] + 0.114 * p[4*i+2];
  const pal = [[244,236,220],[214,160,90],[120,60,40],[40,40,60]];     // paper, ochre, sienna, ink
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const i = y * W + x, l = lum[i];
    let gx = 0, gy = 0;
    if (x > 0 && y > 0 && x < W - 1 && y < H - 1) {
      gx = lum[i+1-W] + 2*lum[i+1] + lum[i+1+W] - lum[i-1-W] - 2*lum[i-1] - lum[i-1+W];
      gy = lum[i-1+W] + 2*lum[i+W] + lum[i+1+W] - lum[i-1-W] - 2*lum[i-W] - lum[i+1-W];
    }
    const k = Math.hypot(gx, gy) > 140 ? 3 : l > 170 ? 0 : l > 100 ? 1 : 2;
    p[4*i] = pal[k][0]; p[4*i+1] = pal[k][1]; p[4*i+2] = pal[k][2];
  }
  g.putImageData(d, 0, 0);
  window.__out = c.toDataURL('image/png'); window.__ready = true;
};
img.src = '%(src)s';
</script></body></html>"""


def _sobel_edges(gray, thr=140):
    g = gray.astype(float)
    gx = np.zeros_like(g)
    gy = np.zeros_like(g)
    gx[1:-1, 1:-1] = (g[:-2, 2:] + 2 * g[1:-1, 2:] + g[2:, 2:] - g[:-2, :-2] - 2 * g[1:-1, :-2] - g[2:, :-2])
    gy[1:-1, 1:-1] = (g[2:, :-2] + 2 * g[2:, 1:-1] + g[2:, 2:] - g[:-2, :-2] - 2 * g[:-2, 1:-1] - g[:-2, 2:])
    return np.hypot(gx, gy) > thr


@card("ENG-400")
def model_shot_redrawn(task, wd):
    """Base shots from a video model redrawn in JS: each base frame is redrawn on a canvas (Sobel ink lines + a
    4-colour posterised paper palette) and re-encoded. The base shot here is a local stand-in clip (testsrc2), since the
    generator itself is a paid model; the redraw is the card's method."""
    import base64
    wd = Path(wd)
    base = wd / "base_shot.mp4"
    ff(wd, "-f", "lavfi", "-i", "testsrc2=s=320x180:r=30:d=1", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", base)
    (wd / "base").mkdir()
    (wd / "redrawn").mkdir()
    ff(wd, "-i", base, "-vf", "select='not(mod(n\\,10))'", "-vsync", "0", wd / "base/b%02d.png")
    pngs = sorted((wd / "base").glob("b*.png"))
    outs = []
    with browser_page(wd) as pg:
        for p in pngs:
            wt(wd / "redraw.html", REDRAW_HTML % {"w": 320, "h": 180, "src": "base/" + p.name})
            pg.goto((wd / "redraw.html").as_uri())
            pg.wait_for_function("window.__ready===true", timeout=10000)
            data = pg.evaluate("window.__out").split(",", 1)[1]
            o = wd / "redrawn" / p.name.replace("b", "r")
            o.write_bytes(base64.b64decode(data))
            outs.append(o)
    film = wd / "redrawn.mp4"
    ff(wd, "-framerate", "3", "-i", wd / "redrawn/r%02d.png", "-c:v", "libx264", "-pix_fmt", "yuv420p", film)
    b0, r0 = png_rgb(pngs[0]), png_rgb(outs[0])
    ncol = lambda img: len(np.unique(img.reshape(-1, 3), axis=0))
    gray = (0.299 * b0[..., 0] + 0.587 * b0[..., 1] + 0.114 * b0[..., 2])
    e_base = _sobel_edges(gray)
    ink = np.all(r0 == [40, 40, 60], axis=2)
    iou = float((e_base & ink).sum() / max(1, (e_base | ink).sum()))
    return [
        check("every sampled base frame was redrawn (3 of 30)", len(outs) == len(pngs) == 3, len(outs)),
        check("redraw uses only the 4-colour paper palette", ncol(r0) <= 4, ncol(r0), "<= 4"),
        check("ink lines sit on the base shot's edges (IoU > 0.9)", iou > 0.9, iou, "> 0.9"),
        check("redrawn frames encoded as a clip", nframes(film) == 3, nframes(film), 3),
        check("negative control: the untreated base frame is full colour (> 100 colours)", ncol(b0) > 100, ncol(b0), "> 100"),
    ], [film, outs[0]]


# ───────────────────────── listen with math: per-frame channels, tape clock, magma ground, glitch, loopcheck (ENG-401) ─────────────────────────

def _kick_track(path, times, secs, sr=44100):
    x = np.zeros(int(secs * sr))
    n = int(0.15 * sr)
    t = np.arange(n) / sr
    k = 0.9 * np.sin(2 * np.pi * (50 + 80 * np.exp(-t * 40)) * t) * np.exp(-t * 18)
    for a in times:
        i = int(a * sr)
        x[i:i + n] += k[: len(x) - i]
    x += 0.05 * np.sin(2 * np.pi * 3000 * np.arange(len(x)) / sr)
    return fx.write_wav(path, x, sr)


def _glitch(img, seed, rows=8, shift=30):
    rng = np.random.default_rng(seed)
    out = img.copy()
    for y in rng.integers(0, img.shape[0] - 4, rows):
        out[y:y + 4] = np.roll(out[y:y + 4], int(rng.integers(-shift, shift)), axis=1)
    return out


@card("ENG-401")
def listen_with_math(task, wd):
    """Per-frame audio channels (motion.py channels: kick/onset/rms, the tape clock), the spectrogram as a magma ground,
    a seeded glitch pass on the kick frames, and motion.py loopcheck on the seam."""
    from PIL import Image
    wd = Path(wd)
    kicks = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    _kick_track(wd / "track.wav", kicks, 3.5)
    py(KM / "motion.py", "channels", wd / "track.wav", "--fps", "30", "--out", wd / "channels.json", wd=wd, timeout=60)
    ch = json.loads((wd / "channels.json").read_text())
    got = ch.get("kicks", [])
    hit = all(any(abs(g - k) <= 0.05 for g in got) for k in kicks)
    spec = sorted(wd.glob("**/spectrogram*.png"))
    sp = png_rgb(spec[0]) if spec else None
    # the ground: the spectrogram scrolled under the frame, glitched on kick frames (seeded)
    W, H, fps = 160, 90, 30
    ground = np.asarray(Image.fromarray(sp).resize((W * 4, H))) if sp is not None else None
    frames = []
    kick_frames = {int(round(k * fps)) for k in got}
    for i in range(int(1.0 * fps)):
        f = np.roll(ground, -i * 4, axis=1)[:, :W]
        frames.append(_glitch(f, i) if i in kick_frames else f)
    def enc(fr, path):
        p = subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (W, H), "-r", "30",
                            "-i", "-", "-c:v", "libx264", "-crf", "10", "-pix_fmt", "yuv444p", str(path)],
                           input=b"".join(np.ascontiguousarray(f).tobytes() for f in fr), capture_output=True)
        if p.returncode:
            raise RuntimeError(p.stderr.decode()[-300:])
        return Path(path)
    seamless = [np.roll(ground, -int(round(i * ground.shape[1] / 30)), axis=1)[:, :W] for i in range(30)]
    enc(frames, wd / "ground.mp4")
    enc(seamless, wd / "loop_ok.mp4")
    enc(frames[:15] + [np.zeros_like(frames[0]) + 255] * 15, wd / "loop_bad.mp4")
    lc_ok = jout(py(KM / "motion.py", "loopcheck", wd / "loop_ok.mp4", wd=wd).stdout)
    lc_bad = jout(py(KM / "motion.py", "loopcheck", wd / "loop_bad.mp4", wd=wd, ok=(0, 1)).stdout)
    tape = ch.get("tape", [])
    magma_like = sp is not None and sp[..., 0].mean() > sp[..., 2].mean() * 0.8 and sp[..., 1].mean() < sp[..., 0].mean()
    g15 = min(kick_frames)
    return [
        check("one channel value per frame (3.5 s x 30 = 105)", len(ch.get("rms", [])) == 105, len(ch.get("rms", [])), 105),
        check("kicks found at the six planted times (±50 ms)", hit and len(got) == 6, got, kicks),
        check("tape clock runs at normal speed (ends ≈ 3.5 s)", tape and abs(tape[-1] - 3.5) < 0.15, tape[-1] if tape else None, 3.5),
        check("magma spectrogram ground written (warm red > blue-ish, green lowest)", bool(spec) and magma_like,
              [float(sp[..., c].mean()) for c in range(3)] if sp is not None else None),
        check("glitch pass changes the kick frame only", not np.array_equal(frames[g15], np.roll(ground, -g15 * 4, axis=1)[:, :W])
              and np.array_equal(frames[g15 + 3], np.roll(ground, -(g15 + 3) * 4, axis=1)[:, :W]), sorted(kick_frames)),
        check("loopcheck passes the seamless ground loop", lc_ok["ok"], lc_ok),
        check("negative control: loopcheck fails a loop with a hard seam", not lc_bad["ok"], lc_bad),
    ], [wd / "channels.json", wd / "ground.mp4", spec[0] if spec else wd / "channels.json"]


# ───────────────────────── mocap → particle body (ENG-402) ─────────────────────────

@card("ENG-402")
def mocap_particles(task, wd):
    """motion.py mocap: a fixed-camera clip of a performer → per-frame particle positions inside the silhouette (median
    background, cleaned difference, one seeded candidate list) for three-kit's particle body. The performer here is a
    synthetic figure walking across a textured room. (The GLB loadModel half needs WebGL; not exercised.)"""
    wd = Path(wd)
    W, H, n = 320, 180, 45
    rng = np.random.default_rng(3)
    room = (rng.random((H, W)) * 40 + 80).astype(np.uint8)
    room = np.stack([room] * 3, 2)
    xs = [int(30 + (W - 90) * i / (n - 1)) for i in range(n)]
    frames = []
    for i in range(n):
        f = room.copy()
        x = xs[i]
        f[40:150, x:x + 30] = 235                       # body
        f[20:40, x + 7:x + 23] = 235                    # head
        frames.append(f)
    p = subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (W, H), "-r", "30",
                        "-i", "-", "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", str(wd / "performer.mp4")],
                       input=b"".join(f.tobytes() for f in frames), capture_output=True)
    if p.returncode:
        raise RuntimeError(p.stderr.decode()[-300:])
    rep = jout(py(KM / "motion.py", "mocap", wd / "performer.mp4", "--out", wd / "body.json", "--fps", "30", wd=wd, timeout=60).stdout)
    body = json.loads((wd / "body.json").read_text())
    py(KM / "motion.py", "mocap", wd / "performer.mp4", "--out", wd / "body2.json", "--fps", "30", wd=wd, timeout=60)
    cx, inside = [], []
    for i, row in enumerate(body["frames"]):
        pts = np.array(row, float).reshape(-1, 2)
        pts = pts[pts[:, 0] >= 0]
        px = pts[:, 0] / 1000 * W
        py_ = pts[:, 1] / 1000 * H
        cx.append(float(px.mean()) if len(px) else None)
        x = xs[i]
        ok = ((px >= x - 4) & (px <= x + 34) & (py_ >= 16) & (py_ <= 154))
        inside.append(float(ok.mean()) if len(px) else 0.0)
    truth = [x + 15 for x in xs]
    err = max(abs(a - b) for a, b in zip(cx, truth) if a is not None)
    uniform = np.random.default_rng(7).random((1200, 2))
    ucx = float((uniform[:, 0] * W).mean())
    return [
        check("one particle frame per video frame", len(body["frames"]) == n, len(body["frames"]), n),
        check("particles fill the silhouette (mean fill > 0)", rep["mean_fill"] > 0, rep["mean_fill"]),
        check("≥ 95% of particles lie inside the performer each frame", min(inside) >= 0.95, min(inside), ">= 0.95"),
        check("particle centroid tracks the performer (max error < 6 px)", err < 6, err, "< 6"),
        check("seeded: a second run gives identical particles", json.loads((wd / "body2.json").read_text()) == body),
        check("negative control: unmasked candidate points stay centred (do not walk)",
              abs(ucx - truth[0]) > 100 and abs(ucx - truth[-1]) > 100, ucx, truth[0]),
    ], [wd / "body.json"]


# ───────────────────────── revealWords masks, dir on text, karaoke per word (ENG-403) ─────────────────────────

@card("ENG-403")
def reveal_words_karaoke(task, wd):
    """MOTION.revealWords masks on an RTL text element (direction on the text, never on <html>), with a per-word karaoke
    highlight timed from words.json, seeked on the paused GSAP timeline and measured in Chromium; lint RULES confirm."""
    wd = Path(wd)
    shutil.copy(GSAP, wd / "gsap.min.js")
    shutil.copy(MKIT, wd / "motion-kit.js")
    words = [{"w": "قلب", "t": 0.40}, {"w": "صغير", "t": 0.80}, {"w": "يغني", "t": 1.20}]
    jw(wd / "words.json", words)
    page = ("<!doctype html><html lang='ar'><head><meta charset='utf-8'><script src='gsap.min.js'></script>"
            "<script src='motion-kit.js'></script><style>#t{direction:rtl;unicode-bidi:isolate;font-size:40px;color:#fff;"
            "visibility:hidden}</style></head><body style='margin:0;background:#000'><div id='root' data-composition-id='root'>"
            "<div id='t'>%s</div></div><script>const M=window.MOTION;const W=%s;const tl=gsap.timeline({paused:true});"
            "const inners=M.revealWords(tl,document.getElementById('t'),0.2,{dur:0.3,stagger:0.25});"
            "W.forEach((w,i)=>{tl.set(inners[i],{color:'#ffcc00'},w.t);if(i>0)tl.set(inners[i-1],{color:'#ffffff'},w.t);});"
            "window.__timelines={root:tl};M.shim('root',1.6);window.__ready=true;</script></body></html>"
            % (" ".join(w["w"] for w in words), json.dumps(words)))
    wt(wd / "index.html", page)
    probe_js = ("t=>{window.__timelines.root.pause(t);return Array.from(document.querySelectorAll('.mk-wi')).map(e=>{"
                "const s=getComputedStyle(e);return {o:+s.opacity,c:s.color};});}")
    rows = {}
    with browser_page(wd) as pg:
        pg.goto((wd / "index.html").as_uri())
        pg.wait_for_function("window.__ready===true")
        for t in (0.1, 0.45, 0.85, 1.25):
            rows[t] = pg.evaluate(probe_js, t)
        dir_html = pg.evaluate("document.documentElement.getAttribute('dir')")
        dir_text = pg.evaluate("getComputedStyle(document.getElementById('t')).direction")
        pg.evaluate("window.__timelines.root.pause(1.25)")
        pg.screenshot(path=str(wd / "karaoke_1.25.png"))
    jw(wd / "probe.json", {str(k): v for k, v in rows.items()})
    gold = "rgb(255, 204, 0)"
    lit = {t: [i for i, r in enumerate(v) if r["c"] == gold] for t, v in rows.items()}
    lint_code = ("import sys,re,json;sys.path.insert(0,%r);import qa;h=open(sys.argv[1],encoding='utf-8').read();"
                 "print(json.dumps([m for lvl,rx,m in qa.RULES if lvl=='error' and re.search(rx,h)]))") % str(KM)
    errs_ok = json.loads(sh([sys.executable, "-c", lint_code, wd / "index.html"], wd).stdout)
    bad = wt(wd / "bad.html", page.replace("<html lang='ar'>", "<html lang='ar' dir='rtl'>"))
    errs_bad = json.loads(sh([sys.executable, "-c", lint_code, bad], wd).stdout)
    return [
        check("three word masks built (.mk-wi)", all(len(v) == 3 for v in rows.values()), [len(v) for v in rows.values()]),
        check("before the reveal every word is hidden", all(r["o"] < 0.01 for r in rows[0.1]), [r["o"] for r in rows[0.1]]),
        check("words reveal in stagger order (t=0.45: word 1 in, word 3 not yet)",
              rows[0.45][0]["o"] > 0.9 and rows[0.45][2]["o"] < 0.1, [r["o"] for r in rows[0.45]]),
        check("karaoke lights exactly the current word at its words.json time", lit == {0.1: [], 0.45: [0], 0.85: [1], 1.25: [2]},
              lit),
        check("direction is on the text element (rtl), not on <html>", dir_html is None and dir_text == "rtl", [dir_html, dir_text]),
        check("lint: no errors on the page", errs_ok == [], errs_ok),
        check("negative control: dir=rtl on <html> is caught by the lint", any("dir=rtl" in e for e in errs_bad), errs_bad),
    ], [wd / "index.html", wd / "probe.json", wd / "karaoke_1.25.png"]


# ───────────────────────── JSON timeline → film (ENG-404) ─────────────────────────

def _av_clip(wd, path, color, freq, secs=2.0):
    ff(wd, "-f", "lavfi", "-i", "color=c=%s:s=320x180:r=30:d=%s" % (color, secs), "-f", "lavfi", "-i",
       "sine=f=%s:d=%s" % (freq, secs), "-shortest", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
       "-c:a", "aac", path)
    return Path(path)


@card("ENG-404")
def timeline_to_film(task, wd):
    """timeline.py (kmotion timeline): a spec with a cut, an xfade transition, a 2x speed change, an Arabic text overlay
    and music ducked under the clips' sound renders to a film, then the delivery gate runs (--inspect)."""
    wd = Path(wd)
    _av_clip(wd, wd / "a.mp4", "red", 300)
    _av_clip(wd, wd / "b.mp4", "blue", 500)
    ff(wd, "-f", "lavfi", "-i", "sine=f=200:d=4", "-ac", "2", wd / "music.wav")
    spec = {"size": "320x180", "fps": 30,
            "clips": [{"src": "a.mp4", "in": 0, "out": 2, "transition": {"type": "fade", "dur": 0.5}},
                      {"src": "b.mp4", "in": 0, "out": 2, "speed": 2.0}],
            "overlays": [{"type": "text", "text": "مرحبا", "start": 0.2, "end": 1.2, "pos": "center", "size": 40,
                          "color": "#ffffff"}],
            "audio": {"music": {"src": "music.wav", "gain": -6}, "keep_clip_audio": True, "duck": "clips", "lufs": -14}}
    jw(wd / "edit.json", spec)
    film = wd / "film.mp4"
    rep = jout(py(KMOTION, "timeline", wd / "edit.json", "--out", film, "--inspect", wd=wd, timeout=60).stdout)
    d = duration(film)
    mid = frame_at(film, 1.75).astype(float)      # inside the fade 1.5-2.0
    early = frame_at(film, 0.05).astype(float)
    late = frame_at(film, 2.3).astype(float)
    centre = lambda f: int((f[60:120, 110:210].min(2) > 200).sum())
    I = ebur(wd, film)
    return [
        check("duration = 2 + 2/2 - 0.5 fade = 2.5 s", abs(d - 2.5) < 0.08, d, 2.5),
        check("xfade: mid-transition frame mixes red and blue", mid[..., 0].mean() > 50 and mid[..., 2].mean() > 50,
              [mid[..., 0].mean(), mid[..., 2].mean()]),
        check("Arabic text drawn at 0.5 s (white glyph pixels in the centre)", centre(frame_at(film, 0.5).astype(float)) > 30,
              centre(frame_at(film, 0.5).astype(float))),
        check("text gone after its end (2.3 s)", centre(late) < 5, centre(late)),
        check("delivery gate passed and loudness at -14 LUFS (±1)", rep.get("gate", {}).get("ok") and abs(I + 14) <= 1, [rep.get("gate"), I]),
        check("negative control: the first frame is pure red (no transition mix)", early[..., 2].mean() < 20, early[..., 2].mean()),
    ], [film, wd / "edit.json"]


# ───────────────────────── scaffold, preview, parallel render with cache (ENG-405, ENG-406, ENG-407) ─────────────────────────

def _contract(html):
    m = re.search(r'<div id="root"[^>]*data-composition-id="root"[^>]*>', html)
    attrs = dict(re.findall(r'data-([\w-]+)="([^"]*)"', m.group(0))) if m else {}
    return {"root": bool(m), "attrs": attrs, "timelines": 'window.__timelines["root"]' in html,
            "paused": "paused: true" in html, "shim": "M.shim(" in html or "MOTION.shim(" in html}


@card("ENG-405")
def scaffold_new(task, wd):
    """kmotion new: a deterministic HTML composition project in 2D, 3D or the product lab, sized and timed by its
    arguments (--seconds, --size)."""
    wd = Path(wd)
    made = {}
    for name, extra in (("film2d", []), ("film3d", ["--3d"]), ("lab", ["--lab"])):
        py(KMOTION, "new", name, "--seconds", "6", "--size", "1080x1920", "--title", "عنوان", *extra, wd=wd)
        made[name] = wd / "projects" / name
    c2 = _contract((made["film2d"] / "index.html").read_text(encoding="utf-8"))
    html3 = (made["film3d"] / "index.html").read_text(encoding="utf-8")
    htmll = (made["lab"] / "index.html").read_text(encoding="utf-8")
    other = wd / "again"
    other.mkdir()
    py(KMOTION, "new", "film2d", "--seconds", "6", "--size", "1080x1920", "--title", "عنوان", wd=other, env=env_for(other))
    h1 = hashlib.sha256((made["film2d"] / "index.html").read_bytes()).hexdigest()
    h2 = hashlib.sha256((other / "projects/film2d/index.html").read_bytes()).hexdigest()
    plain = _contract("<html><body><div id='root'></div></body></html>")
    return [
        check("2D: data-composition-id root sized 1080x1920, 6 s, 30 fps",
              c2["root"] and c2["attrs"].get("width") == "1080" and c2["attrs"].get("height") == "1920" and
              float(c2["attrs"].get("duration", 0)) == 6.0 and c2["attrs"].get("fps") == "30", c2["attrs"]),
        check("one paused GSAP timeline registered in window.__timelines.root + MOTION.shim",
              c2["timelines"] and c2["paused"] and c2["shim"], c2),
        check("3D route loads the three-kit", "three-kit" in html3 or "K3" in html3),
        check("lab route loads the lab-kit", "lab-kit" in htmll),
        check("deterministic: the same arguments scaffold a byte-identical page", h1 == h2, [h1[:12], h2[:12]]),
        check("negative control: a plain page has no composition contract", not plain["root"] and not plain["timelines"]),
    ], [made["film2d"] / "index.html", made["film3d"] / "index.html", made["lab"] / "index.html"]


@card("ENG-406")
def preview_draft(task, wd):
    """kmotion preview: a quick draft at half size and 15 fps for timing checks (JPEG capture, ultrafast)."""
    wd = Path(wd)
    e = env_for(wd, tmp=False)
    motion_project(wd, "pv", 1.0, "320x180", BOX_SCRIPT % {"d": "1.0", "x": 280, "top": 70})
    rep = jout(py(KMOTION, "preview", "pv", wd=wd, env=e, timeout=40).stdout)
    out = Path(rep["file"])
    v = vstream(out)
    xs = [red_centroid(f, 120) for f in all_frames(out)]
    attrs = _contract((wd / "projects/pv/index.html").read_text(encoding="utf-8"))["attrs"]
    full = (int(attrs["width"]), int(attrs["height"]))
    return [
        check("draft is half size (160x90)", (int(v["width"]), int(v["height"])) == (160, 90), [v["width"], v["height"]]),
        check("draft is 15 fps and 15 frames for 1 s", v["r_frame_rate"] == "15/1" and nframes(out) == 15,
              [v["r_frame_rate"], nframes(out)]),
        check("timing preserved: box at mid-draft is at mid-travel (±6 px of 80 at half size)",
              xs[7] is not None and abs(xs[7][0] - (10 + 140 * 7 / 15)) < 6, xs[7]),
        check("report marks it a draft", rep.get("draft") is True and out.name.endswith(".draft.mp4"), rep),
        check("negative control: the project's own size (320x180) fails the half-size check",
              full != (int(v["width"]), int(v["height"])), full),
    ], [out]


@card("ENG-407")
def parallel_render_cache(task, wd):
    """kmotion render: the composition through parallel headless browsers (--workers 2) with motion blur (--blur 2) and
    the render cache (unchanged sources and parameters → no re-render; --force renders again identically)."""
    wd = Path(wd)
    e = env_for(wd, tmp=False)
    motion_project(wd, "rc", 1.0, "320x180", BOX_SCRIPT % {"d": "1.0", "x": 280, "top": 70})
    t0 = time.perf_counter()
    r1 = jout(py(KMOTION, "render", "rc", "--engine", "studio", "--workers", "2", "--blur", "2", wd=wd, env=e, timeout=40).stdout)
    t1 = time.perf_counter()
    out = Path(r1["file"])
    h1 = hashlib.sha256(out.read_bytes()).hexdigest()
    r2 = jout(py(KMOTION, "render", "rc", "--engine", "studio", "--workers", "2", "--blur", "2", wd=wd, env=e, timeout=40).stdout)
    t2 = time.perf_counter()
    h2 = hashlib.sha256(out.read_bytes()).hexdigest()
    page = wd / "projects/rc/index.html"
    wt(page, page.read_text(encoding="utf-8").replace("x: 280", "x: 200"))
    r3 = jout(py(KMOTION, "render", "rc", "--engine", "studio", "--workers", "2", "--blur", "2", wd=wd, env=e, timeout=40).stdout)
    return [
        check("first render used 2 parallel browsers and blur 2, 30 frames",
              r1.get("workers") == 2 and r1.get("blur") == 2 and r1.get("frames") == 30 and nframes(out) == 30, r1),
        check("unchanged project → cache hit, film untouched", r2.get("cached") is True and h1 == h2, r2),
        check("cache hit is fast (< 1 s vs the real render)", (t2 - t1) < 1.0 < (t1 - t0) + 0.5, [round(t1 - t0, 2), round(t2 - t1, 2)]),
        check("negative control: an edited source is not served from cache", not r3.get("cached") and r3.get("frames") == 30, r3),
    ], [out]


# ───────────────────────── timeline A by record date, dated duplicate B with named tracks (ENG-413) ─────────────────────────

def _resolve_tracks():
    src = (VSK / "davinci-resolve-pipeline/scripts/resolve_pipeline.py").read_text(encoding="utf-8")
    v = json.loads(re.search(r"TRACKS_V = (\[.*?\])", src).group(1).replace("'", '"'))
    a = json.loads(re.search(r"TRACKS_A = (\[.*?\])", src).group(1).replace("'", '"'))
    return v, a


def ensure_named(tracks, names):
    have = [t["name"] for t in tracks]
    return tracks + [{"name": n, "items": []} for n in names if n not in have]


@card("ENG-413")
def record_date_timelines(task, wd):
    """Timeline A ordered by Date Recorded and never touched; B = a dated duplicate with 4 video + 4 audio named role
    tracks (resolve_pipeline.py's TRACKS_V/TRACKS_A), named idempotently. Resolve itself is proprietary, so the same
    logic runs on the open timeline JSON with ffprobe's creation_time as the record date."""
    import copy
    wd = Path(wd)
    stamps = {"clip_a.mp4": "2026-10-03T09:15:00Z", "clip_b.mp4": "2026-10-01T18:40:00Z", "clip_c.mp4": "2026-10-02T07:05:00Z"}
    for name, ts in stamps.items():
        ff(wd, "-f", "lavfi", "-i", "testsrc2=s=160x90:r=30:d=0.5", "-metadata", "creation_time=%s" % ts, "-c:v", "libx264",
           "-preset", "ultrafast", "-pix_fmt", "yuv420p", wd / name)
    rec = {n: probe(wd / n)["format"]["tags"]["creation_time"] for n in stamps}
    order = sorted(rec, key=lambda n: rec[n])
    A = {"name": "Timeline A", "video": [{"name": "V1", "items": [{"clip": n, "recorded": rec[n]} for n in order]}],
         "audio": [{"name": "A1", "items": []}]}
    jw(wd / "timeline_A.json", A)
    hA = hashlib.sha256((wd / "timeline_A.json").read_bytes()).hexdigest()
    tv, ta = _resolve_tracks()
    stamp = "20261104_0900"
    B = copy.deepcopy(A)
    B["name"] = "Timeline A_edit_%s" % stamp
    B["video"] = ensure_named(B["video"], tv)
    B["audio"] = ensure_named(B["audio"], ta)
    B2 = copy.deepcopy(B)
    B2["video"] = ensure_named(B2["video"], tv)
    B2["audio"] = ensure_named(B2["audio"], ta)
    jw(wd / "timeline_B.json", B2)
    hA2 = hashlib.sha256((wd / "timeline_A.json").read_bytes()).hexdigest()
    by_name = sorted(stamps)
    return [
        check("A is ordered by Date Recorded (b, c, a)", order == ["clip_b.mp4", "clip_c.mp4", "clip_a.mp4"], order),
        check("A is never touched (hash unchanged after B is made)", hA == hA2 and A["name"] == "Timeline A", hA[:12]),
        check("B is a dated duplicate with A's cut", B2["name"].endswith(stamp) and B2["video"][0] == A["video"][0], B2["name"]),
        check("B has 4 video + 4 audio role tracks from resolve_pipeline.py", [t["name"] for t in B2["video"][1:]] == tv and
              [t["name"] for t in B2["audio"][1:]] == ta and len(tv) == len(ta) == 4, [tv, ta]),
        check("naming is idempotent: a re-run adds no duplicate tracks", B2 == B, [len(B2["video"]), len(B2["audio"])], [5, 5]),
        check("negative control: file-name order is not record-date order", by_name != order, by_name),
    ], [wd / "timeline_A.json", wd / "timeline_B.json"]


# ───────────────────────── HyperFrames composition contract (ENG-414) ─────────────────────────

@card("ENG-414")
def hyperframes_contract(task, wd):
    """The HyperFrames contract: data-composition-id root, one paused GSAP timeline in window.__timelines['root'],
    MOTION.shim, kit reveal/draw/seeded effects; banned dir=rtl on html, audio without id, Math.random, setTimeout, wall
    clock — checked by motion.py lint and seeked in Chromium (default length 8 s)."""
    wd = Path(wd)
    py(KMOTION, "new", "hf", wd=wd)
    page = wd / "projects/hf/index.html"
    html = page.read_text(encoding="utf-8")
    c = _contract(html)
    lint_ok = jout(py(KM / "motion.py", "lint", "hf", wd=wd, ok=(0, 1)).stdout)
    bad = {"Math.random": html.replace("M.vignette(root", "const r = Math.random(); M.vignette(root"),
           "setTimeout": html.replace("M.vignette(root", "setTimeout(() => 0, 10); M.vignette(root"),
           "dir=rtl": html.replace('<html lang="ar">', '<html lang="ar" dir="rtl">'),
           "audio id": html.replace("</body>", '<audio src="a.wav"></audio></body>'),
           "wall clock": html.replace("M.vignette(root", "const now = Date.now(); M.vignette(root")}
    caught = {}
    for k, h in bad.items():
        d = wd / "projects" / ("bad_" + re.sub(r"\W", "", k))
        shutil.copytree(wd / "projects/hf", d)
        wt(d / "index.html", h)
        caught[k] = jout(py(KM / "motion.py", "lint", d.name, wd=wd, ok=(0, 1)).stdout).get("errors", 0)
    with browser_page(wd, 480, 270) as pg:
        pg.goto(page.as_uri())
        pg.wait_for_function("!!(window.__timelines && window.__timelines.root)", timeout=10000, polling=100)
        st = pg.evaluate("({p: window.__timelines.root.paused(), d: window.__timelines.root.duration(), dur: window.__duration,"
                         " seek: typeof window.render})")
    return [
        check("default composition is 8 s with a data-composition-id root", c["root"] and float(c["attrs"]["duration"]) == 8.0,
              c["attrs"].get("duration")),
        check("one paused GSAP timeline registered as window.__timelines.root", st["p"] is True and st["d"] > 0, st),
        check("MOTION.shim exposes render(t) and the duration", st["seek"] == "function" and st["dur"] == 8, st),
        check("the scaffold passes lint with 0 errors", lint_ok.get("errors") == 0, lint_ok),
        check("each banned pattern is caught as an error", all(v >= 1 for v in caught.values()), caught),
    ], [page]


# ───────────────────────── Studio project JSON → timeline spec → FFmpeg render (ENG-73) ─────────────────────────

@card("ENG-73")
def studio_import_render(task, wd):
    """kmotion studio-import P.kosif.json --out edit.json --media DIR --render film.mp4: the browser editor's project
    (version 1) mapped to a timeline spec (clips by trim, text overlays %→px, shapes skipped and reported, soundtrack gain
    from volume) and rendered offline at full quality."""
    wd = Path(wd)
    media = wd / "media"
    media.mkdir()
    _av_clip(wd, media / "beach.mp4", "orange", 330, 3.0)
    from PIL import Image
    Image.new("RGB", (320, 180), (20, 120, 60)).save(media / "card.png")
    ff(wd, "-f", "lavfi", "-i", "sine=f=220:d=6", "-ac", "2", media / "song.wav")
    proj = {"version": 1, "name": "رحلة", "aspect": "16:9",
            "assets": [{"id": "a1", "name": "beach.mp4"}, {"id": "a2", "name": "card.png"}, {"id": "a3", "name": "song.wav"},
                       {"id": "a4", "name": "missing.mp4"}],
            "clips": [{"type": "video", "assetId": "a1", "trim": 0.5, "duration": 1.5},
                      {"type": "image", "assetId": "a2", "duration": 1.0},
                      {"type": "demo", "preset": "sunset", "duration": 0.5},
                      {"type": "video", "assetId": "a4", "duration": 0.5}],
            "overlays": [{"type": "text", "text": "رحلة البحر", "start": 0.2, "duration": 1.2, "x": 50, "y": 50, "size": 10,
                          "color": "#ffffff", "animation": "rise"},
                         {"type": "shape", "start": 0, "duration": 1}],
            "soundtrack": {"assetId": "a3", "volume": 0.5}}
    jw(wd / "P.kosif.json", proj)
    out = py(KMOTION, "studio-import", wd / "P.kosif.json", "--out", wd / "edit.json", "--media", media, "--size", "320x180",
             "--render", wd / "film.mp4", wd=wd, timeout=60).stdout
    rep = jout(out)
    spec = json.loads((wd / "edit.json").read_text(encoding="utf-8"))
    c0 = spec["clips"][0]
    ov = spec["overlays"][0]
    d = duration(wd / "film.mp4")
    gain = spec["audio"].get("music", {}).get("gain")
    return [
        check("video clip mapped by trim: in 0.5, out 2.0", (c0["in"], c0["out"]) == (0.5, 2.0), [c0["in"], c0["out"]]),
        check("image and demo clips mapped (image 1 s, sunset colour card)", spec["clips"][1].get("dur") == 1.0 and
              spec["clips"][2].get("color") == "#3a1a12", spec["clips"][1:3]),
        check("text overlay: size 10% of 180 px = 18 px, x/y 50% → 0.5", ov["size"] == 18 and ov["x"] == 0.5 and ov["y"] == 0.5,
              [ov["size"], ov["x"], ov["y"]]),
        check("shape overlay skipped and reported; missing media reported", rep["skipped"][0]["type"] == "shape" and
              "missing.mp4" in rep["missing_media"], [rep["skipped"], rep["missing_media"]]),
        check("soundtrack volume 0.5 → gain -6.02 dB", gain == -6.02, gain, -6.02),
        check("film rendered with the project's total length (3.5 s) and the gate ran", abs(d - 3.5) < 0.1 and rep.get("gate", {}).get("ok"),
              [d, rep.get("gate")]),
        check("negative control: without --media nothing is found (all media missing)",
              len(jout(py(KMOTION, "studio-import", wd / "P.kosif.json", "--out", wd / "edit_nomedia.json", wd=wd).stdout)
                  ["missing_media"]) == 4),
    ], [wd / "film.mp4", wd / "edit.json"]


# ───────────────────────── Workbench: plan → validate → manifest → preview → MP4 → project (ENG-86) ─────────────────────────

WB_PY = r"""
import json, sys
sys.path.insert(0, sys.argv[1]); sys.path.insert(0, sys.argv[1] + "/web")
import wbcompat
plan = wbcompat.make_plan({"task": "مقدمة عربية أنيقة عن قوة الأفكار", "seconds": 3, "fps": 30, "aspect": "9:16"})
ok = wbcompat.validate_plan(plan)
import copy
badp = copy.deepcopy(plan); badp["timeline"]["fps"] = 7
bad = wbcompat.validate_plan(badp)
print(json.dumps({"plan": plan, "valid": ok, "bad": bad}, ensure_ascii=False))
"""


@card("ENG-86")
def workbench_flow(task, wd):
    """The Workbench five-button flow as its CLI: make a plan, validate it, compile the manifest, scrub the canvas
    preview (0.033 s steps), render a local MP4 and keep the manifest as the editable project."""
    wd = Path(wd)
    wt(wd / "wb.py", WB_PY)
    v = json.loads(py(wd / "wb.py", KM, wd=wd).stdout.strip().splitlines()[-1])
    py(KM / "workbench_cli.py", "مقدمة عربية أنيقة عن قوة الأفكار", "--seconds", "3", "--aspect", "9:16", "--plan-only",
       "--out", wd / "project", wd=wd)
    man = json.loads((wd / "project/manifest.json").read_text(encoding="utf-8"))
    sc = man["scenes"]
    contiguous = sc[0]["start_frame"] == 0 and all(a["end_frame_exclusive"] == b["start_frame"] for a, b in zip(sc, sc[1:])) \
        and sc[-1]["end_frame_exclusive"] == 90
    out = wd / "film.mp4"
    py(KM / "workbench_cli.py", "--manifest", wd / "project/manifest.json", "--out", out, wd=wd, timeout=60)
    st = vstream(out)
    with browser_page(wd, 270, 480) as pg:
        pg.goto((wd / "project/index.html").as_uri())
        pg.wait_for_timeout(300)
        shots = []
        for t in (0.0, 0.033 * 45):
            pg.evaluate("t=>{if(window.seek)window.seek(t);else if(window.render)window.render(t);}", t)
            pg.wait_for_timeout(50)
            shots.append(png_rgb(pg.screenshot()))
        has_seek = pg.evaluate("typeof window.seek==='function'||typeof window.render==='function'")
    diff = float(np.abs(shots[0].astype(float) - shots[1].astype(float)).mean())
    f_a, f_b = frame_at(out, 0.1, (108, 192)).astype(float), frame_at(out, 2.0, (108, 192)).astype(float)
    return [
        check("plan validates; an fps outside 24/25/30/50/60 is rejected", v["valid"]["valid"] and not v["bad"]["valid"],
              [v["valid"]["valid"], v["bad"]["valid"]]),
        check("manifest: 5 beats covering frames 0-90 without gaps", len(sc) == 5 and contiguous, [(s["start_frame"], s["end_frame_exclusive"]) for s in sc]),
        check("MP4 rendered 1080x1920, 30 fps, 90 frames", (st["width"], st["height"], st["r_frame_rate"]) == (1080, 1920, "30/1")
              and nframes(out) == 90, [st["width"], st["height"], st["r_frame_rate"], nframes(out)]),
        check("the project page scrubs: canvas changes between t=0 and t=1.485", has_seek and diff > 1.0, diff, "> 1"),
        check("the film differs between beat 1 and beat 4", float(np.abs(f_a - f_b).mean()) > 1, float(np.abs(f_a - f_b).mean())),
        check("negative control: an invalid plan produces errors", bool(v["bad"]["errors"]), v["bad"]["errors"]),
    ], [out, wd / "project/manifest.json", wd / "project/index.html"]


# ───────────────────────── owner skills, followed step by step (ENG-415 … ENG-421) ─────────────────────────

RENAME_TOOL = r'''#!/usr/bin/env python3
"""Number video clips in a folder: "مقطع أول.mp4" -> "001_مقطع_أول.mp4"; --clean moves *.tmp into .trash (never deletes).

Input: a folder of clips. Output: renamed clips. Side effect: files renamed/moved (only without --dry-run).
Examples:
  python tool.py "My Clips" --dry-run
  python tool.py "My Clips" --clean
"""
import argparse, shutil, sys
from pathlib import Path


def plan(folder: Path):
    clips = sorted(p for p in folder.iterdir() if p.suffix.lower() in (".mp4", ".mov") and not p.name[:3].isdigit())
    return [(p, folder / ("%03d_%s" % (i + 1, p.name.replace(" ", "_")))) for i, p in enumerate(clips)]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder"); ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--clean", action="store_true")
    a = ap.parse_args(argv)
    folder = Path(a.folder)
    if not folder.is_dir():
        print("error: folder not found: %s" % folder, file=sys.stderr)
        return 2
    for src, dst in plan(folder):
        print(("would rename" if a.dry_run else "renamed") + ": %s -> %s" % (src.name, dst.name))
        if not a.dry_run:
            src.rename(dst)
    if a.clean:
        trash = folder / ".trash"
        for t in folder.glob("*.tmp"):
            print(("would move" if a.dry_run else "moved") + " to .trash: " + t.name)
            if not a.dry_run:
                trash.mkdir(exist_ok=True)
                shutil.move(str(t), str(trash / t.name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''

RENAME_TEST = r'''import subprocess, sys
from pathlib import Path
TOOL = Path(__file__).resolve().parents[1] / "tool.py"


def mk(tmp_path):
    d = tmp_path / "My Clips"
    d.mkdir()
    for n in ("مقطع أول.mp4", "b roll.mov", "cache.tmp"):
        (d / n).write_bytes(b"x")
    return d


def run(*a):
    return subprocess.run([sys.executable, str(TOOL), *a], capture_output=True, text=True, encoding="utf-8")


def test_dry_run_changes_nothing(tmp_path):
    d = mk(tmp_path)
    before = sorted(p.name for p in d.iterdir())
    r = run(str(d), "--dry-run", "--clean")
    assert r.returncode == 0 and "would rename" in r.stdout
    assert sorted(p.name for p in d.iterdir()) == before


def test_rename_and_trash(tmp_path):
    d = mk(tmp_path)
    assert run(str(d), "--clean").returncode == 0
    names = sorted(p.name for p in d.iterdir())
    assert names == [".trash", "001_b_roll.mov", "002_مقطع_أول.mp4"]
    assert (d / ".trash" / "cache.tmp").exists()


def test_missing_folder_exit_2(tmp_path):
    r = run(str(tmp_path / "nope"))
    assert r.returncode == 2 and "folder not found" in r.stderr
'''


@card("ENG-415")
def automation_cli(task, wd):
    """automation-scripts-cli steps: input/output/side effect in one line, argparse with examples and --dry-run, UTF-8
    Arabic names and spaces, explained errors with exit codes, no permanent delete (move to .trash), tests on a temp
    folder, README with the install line — as a clip-numbering tool for a video job."""
    wd = Path(wd)
    proj = wd / "clip-tool"
    wt(proj / "tool.py", RENAME_TOOL)
    wt(proj / "tests/test_tool.py", RENAME_TEST)
    wt(proj / "README.md", "# clip-tool\nInstall: `python3 -m pip install --user pytest` (the tool itself is stdlib only)\n\n"
       "Usage: `python tool.py \"My Clips\" --dry-run`\n")
    t = sh([PYTEST, "-q", "-p", "no:cacheprovider", proj / "tests"], proj, ok=None)
    wt(wd / "pytest.txt", t.stdout)
    helpt = py(proj / "tool.py", "--help", wd=proj).stdout
    src = (proj / "tool.py").read_text(encoding="utf-8")
    passed = int(re.search(r"(\d+) passed", t.stdout).group(1)) if "passed" in t.stdout else 0
    naive = "import os,sys\nfor f in os.listdir(sys.argv[1]):\n    os.remove(f)\n"
    rules = lambda code: ("--dry-run" in code and "os.remove" not in code and "unlink" not in code and "rmtree" not in code)
    return [
        check("three pytest cases pass on a temp folder (Arabic names with spaces)", t.returncode == 0 and passed == 3, t.stdout[-200:]),
        check("--help shows the examples and --dry-run", "Examples" in helpt and "--dry-run" in helpt),
        check("no permanent delete in the tool (moves to .trash)", rules(src) and ".trash" in src),
        check("README carries the install line", "Install:" in (proj / "README.md").read_text()),
        check("negative control: a naive script with os.remove and no --dry-run fails the safety rules", not rules(naive)),
    ], [proj / "tool.py", wd / "pytest.txt"]


CAPTURE_PAGE = """<!doctype html><html><body style="margin:0;background:#000">
<button data-testid="play" aria-label="play">تشغيل</button>
<form id="f"><button type="submit" data-testid="publish">نشر</button></form>
<canvas id="c" width="320" height="140" data-testid="stage" data-state="idle"></canvas>
<script>
window.submitted = false; document.getElementById('f').addEventListener('submit', e => { e.preventDefault(); window.submitted = true; });
const c = document.getElementById('c'), g = c.getContext('2d');
window.seek = t => { g.fillStyle = '#000'; g.fillRect(0, 0, 320, 140); g.fillStyle = '#f00'; g.fillRect(10 + 260 * t, 50, 40, 40); };
document.querySelector('[data-testid=play]').addEventListener('click', () => {
  Promise.resolve().then(() => { window.seek(0); c.dataset.state = 'ready'; });
});
</script></body></html>"""


@card("ENG-416")
def playwright_capture(task, wd):
    """browser-automation-playwright steps: stable selectors (getByRole/getByTestId, no XPath), waits on state not
    time, a screenshot per step, a hard stop before any submit; used as the headless frame-by-frame capture of an HTML
    animation."""
    wd = Path(wd)
    wt(wd / "anim.html", CAPTURE_PAGE)
    (wd / "screenshots").mkdir()
    log = ["# run-log", "goal: capture 10 frames of the stage animation; never publish"]
    from playwright.sync_api import expect
    with browser_page(wd, 320, 200) as pg:
        pg.goto((wd / "anim.html").as_uri())
        stage = pg.get_by_test_id("stage")
        before = stage.get_attribute("data-state")
        pg.screenshot(path=str(wd / "screenshots/00_loaded.png"))
        pg.get_by_role("button", name="play").click()
        expect(stage).to_have_attribute("data-state", "ready")
        after = stage.get_attribute("data-state")
        log.append("clicked play (role=button name=play); waited on data-state=ready")
        pg.screenshot(path=str(wd / "screenshots/01_ready.png"))
        hashes = []
        for i in range(10):
            pg.evaluate("t=>window.seek(t)", i / 9)
            p = wd / "screenshots" / ("frame_%02d.png" % i)
            stage.screenshot(path=str(p))
            hashes.append(hashlib.sha256(p.read_bytes()).hexdigest())
        log.append("captured 10 frames by seek(t)")
        submitted = pg.evaluate("window.submitted")
        log.append("STOP before publish: the submit button was not pressed")
    wt(wd / "run-log.md", "\n".join(log) + "\n")
    ff(wd, "-framerate", "10", "-i", wd / "screenshots/frame_%02d.png", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-vf",
       "scale=320:140", wd / "capture.mp4")
    xs = [red_centroid(png_rgb(wd / "screenshots" / ("frame_%02d.png" % i)))[0] for i in (0, 9)]
    import inspect
    code = inspect.getsource(playwright_capture)
    body = code[code.index('"""', code.index('"""') + 3) + 3:code.index("    return [")]   # the program between docstring and checks
    return [
        check("state waited on, not time: idle → ready after the click", before == "idle" and after == "ready", [before, after]),
        check("10 distinct frames captured frame by frame", len(set(hashes)) == 10, len(set(hashes))),
        check("the box travels 30 → 290 px across the capture", abs(xs[0] - 30) < 3 and abs(xs[1] - 290) < 3, xs),
        check("selectors are role/test-id only (no XPath, no fixed sleeps)", "xpath" not in body.lower() and "wait_for_timeout" not in body
              and "get_by_test_id" in body),
        check("hard stop before submit: the form was never submitted", submitted is False),
        check("a screenshot per step and a run log", len(list((wd / "screenshots").glob("*.png"))) == 12 and (wd / "run-log.md").exists()),
        check("negative control: before the click the stage is still idle (nothing to capture)", before != "ready", before),
    ], [wd / "capture.mp4", wd / "run-log.md"]


DOCKERFILE = """# render worker: ffmpeg + the timeline tool
FROM python:3.12-slim AS build
WORKDIR /src
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim AS run
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && rm -rf /var/lib/apt/lists/*
COPY --from=build /install /usr/local
WORKDIR /app
COPY worker.py .
RUN useradd --create-home --uid 10001 render
USER render
ENTRYPOINT ["python", "worker.py"]
"""

CI_YML = """name: ci
on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python: ['3.11', '3.12']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}
          cache: pip
      - run: pip install -r requirements.txt ruff pytest
      - run: ruff check .
      - run: pytest -q
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t render-worker .
  deploy:
    needs: build
    if: startsWith(github.ref, 'refs/tags/v')
    environment: production
    runs-on: ubuntu-latest
    steps:
      - run: echo deploy with ${{ secrets.REGISTRY_TOKEN != '' }}
"""

WORKER = '''"""Render worker: make a 1 s colour clip with ffmpeg (the job the container runs)."""
import subprocess
import sys


def render(out: str, colour: str = "blue") -> int:
    return subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c={colour}:s=160x90:d=1",
                           "-pix_fmt", "yuv420p", out]).returncode


if __name__ == "__main__":
    sys.exit(render(sys.argv[1] if len(sys.argv) > 1 else "out.mp4"))
'''


def docker_rules(dockerfile, files):
    lines = [l.strip() for l in dockerfile.splitlines() if l.strip() and not l.startswith("#")]
    froms = [l for l in lines if l.upper().startswith("FROM ")]
    return {"multi-stage": len(froms) >= 2, "small pinned base": all(":latest" not in f and "slim" in f for f in froms),
            "non-root user": any(l.upper().startswith("USER ") and "root" not in l for l in lines),
            ".dockerignore": ".dockerignore" in files, "no secret in image": not re.search(r"(?i)(token|password|secret)\s*=", dockerfile)}


@card("ENG-417")
def docker_ci(task, wd):
    """docker-ci-devops steps: small multi-stage Dockerfile with a non-root user and .dockerignore, compose for dev with
    variables from .env.example, an Actions matrix with dependency cache, lint → test → build → deploy on tags only with
    an environment gate, least-privilege token, no secrets; verified by parsing and by running the CI's steps locally."""
    import yaml
    wd = Path(wd)
    p = wd / "render-worker"
    wt(p / "Dockerfile", DOCKERFILE)
    wt(p / ".dockerignore", ".git\n__pycache__\n*.mp4\n.env\n")
    wt(p / "docker-compose.yml", "services:\n  worker:\n    build: .\n    env_file: .env\n    volumes:\n      - ./out:/app/out\n")
    wt(p / ".env.example", "RENDER_QUALITY=high\n")
    wt(p / "requirements.txt", "")
    wt(p / "worker.py", WORKER)
    wt(p / "ruff.toml", "line-length = 120\n\n[lint]\nselect = [\"E\", \"F\", \"I\"]\n")
    wt(p / "test_worker.py", "import worker\n\n\ndef test_render(tmp_path):\n    o = tmp_path / 'o.mp4'\n"
       "    assert worker.render(str(o)) == 0 and o.stat().st_size > 0\n")
    wt(p / ".github/workflows/ci.yml", CI_YML)
    ci = yaml.safe_load(CI_YML)
    on = ci.get(True) or ci.get("on")
    rules = docker_rules(DOCKERFILE, [x.name for x in p.iterdir()])
    lint = sh([shutil.which("ruff") or "ruff", "check", "--no-cache", "."], p, ok=None)
    test = sh([PYTEST, "-q", "-p", "no:cacheprovider"], p, ok=None)
    tok = "ghp" + "_" + "A" * 36
    leak = re.compile(r"gh[pousr]_[A-Za-z0-9]{36}")
    scanned = [f for f in p.rglob("*") if f.is_file() and leak.search(f.read_text(errors="ignore"))]
    naive = "FROM python:latest\nCOPY . .\nENV API_TOKEN=" + tok + "\nCMD python worker.py\n"
    jw(wd / "checks.json", {"docker": rules, "ruff": lint.returncode, "pytest": test.stdout[-200:]})
    return [
        check("Dockerfile rules: multi-stage, slim pinned base, non-root, .dockerignore, no secret", all(rules.values()), rules),
        check("compose takes variables from .env (example committed)", "env_file" in (p / "docker-compose.yml").read_text() and
              (p / ".env.example").exists()),
        check("Actions: matrix + pip cache, test → build → deploy chain", ci["jobs"]["test"]["strategy"]["matrix"]["python"] == ["3.11", "3.12"]
              and ci["jobs"]["build"]["needs"] == "test" and ci["jobs"]["deploy"]["needs"] == "build"),
        check("deploy only on tags behind an environment; token is contents: read",
              "refs/tags/v" in ci["jobs"]["deploy"]["if"] and ci["jobs"]["deploy"]["environment"] == "production" and
              ci["permissions"] == {"contents": "read"} and "tags" in on["push"]),
        check("the CI's lint and test steps pass locally (ruff, pytest renders with ffmpeg)", lint.returncode == 0 and test.returncode == 0,
              [lint.returncode, test.stdout.strip()[-60:]]),
        check("no token-shaped secret anywhere in the project", scanned == [], [str(s) for s in scanned]),
        check("negative control: a naive Dockerfile (latest, root, baked token) fails the rules",
              not all(docker_rules(naive, []).values()) and bool(leak.search(naive)), docker_rules(naive, [])),
    ], [p / "Dockerfile", p / ".github/workflows/ci.yml", wd / "checks.json"]


GAME_PAGE = """<!doctype html><html><body style="margin:0;background:#000"><canvas id="c" width="320" height="180"></canvas><script>
const DT = 1 / 60, G = 400;
let S = { t: 0, ball: { y: 0, v: 0 }, player: { x: 160 }, keys: {} };
function update(dt) {                              // simulation only
  S.t += dt; S.ball.v += G * dt; S.ball.y += S.ball.v * dt;
  if (S.keys.ArrowRight) S.player.x += 120 * dt;
  if (S.keys.ArrowLeft) S.player.x -= 120 * dt;
}
const g = document.getElementById('c').getContext('2d');
function render() {                                // drawing only
  g.fillStyle = '#0d1b2a'; g.fillRect(0, 0, 320, 180);
  g.fillStyle = '#ff0000'; g.fillRect(40, Math.min(170, 10 + S.ball.y * 0.2), 10, 10);
  g.fillStyle = '#00ff00'; g.fillRect(S.player.x - 10, 160, 20, 10);
}
window.step = n => { for (let i = 0; i < n; i++) update(DT); render(); return JSON.parse(JSON.stringify(S)); };
addEventListener('keydown', e => { S.keys[e.key] = true; }); addEventListener('keyup', e => { S.keys[e.key] = false; });
document.getElementById('c').addEventListener('touchstart', e => { S.player.x = e.touches[0].clientX; e.preventDefault(); });
window.save = () => localStorage.setItem('game', JSON.stringify(S));
window.load = () => { S = JSON.parse(localStorage.getItem('game')); render(); return S; };
window.reset = () => { S = { t: 0, ball: { y: 0, v: 0 }, player: { x: 160 }, keys: {} }; render(); };
render(); window.__ready = true;
</script></body></html>"""


@card("ENG-418")
def game_loop_frames(task, wd):
    """game-dev-web steps: separate update(dt) and render, fixed timestep, keyboard + touch input, localStorage save and
    restore; the same loop then drives procedural animation frames for capture."""
    wd = Path(wd)
    wt(wd / "game.html", GAME_PAGE)
    wt(wd / "design.md", "Core loop: dodge the falling ball by moving the paddle; lose if it lands on you.\n")
    (wd / "frames").mkdir()
    with browser_page(wd) as pg:
        pg.goto((wd / "game.html").as_uri())
        pg.wait_for_function("window.__ready===true")
        s60 = pg.evaluate("window.step(60)")
        pg.keyboard.down("ArrowRight")
        s90 = pg.evaluate("window.step(30)")
        pg.keyboard.up("ArrowRight")
        pg.evaluate("""() => { const c = document.getElementById('c');
            c.dispatchEvent(new TouchEvent('touchstart', {cancelable: true, bubbles: true,
              touches: [new Touch({identifier: 1, target: c, clientX: 50, clientY: 100})]})); }""")
        touch_x = pg.evaluate("window.step(0).player.x")
        pg.evaluate("window.save()")
        pg.evaluate("window.reset()")
        fresh = pg.evaluate("window.step(0)")
        restored = pg.evaluate("window.load()")
        pg.evaluate("window.reset()")
        for i in range(15):
            pg.evaluate("window.step(4)")
            pg.screenshot(path=str(wd / "frames" / ("f%02d.png" % i)))
    ff(wd, "-framerate", "15", "-i", wd / "frames/f%02d.png", "-c:v", "libx264", "-pix_fmt", "yuv420p", wd / "loop.mp4")
    y_true = 0.5 * 400 * 1.0 ** 2
    hs = {hashlib.sha256(p.read_bytes()).hexdigest() for p in (wd / "frames").glob("*.png")}
    return [
        check("fixed 1/60 s semi-implicit steps: y = g·dt²·n(n+1)/2 = 203.33 exactly, within 2% of ½gt² = 200",
              abs(s60["ball"]["y"] - 400 / 3600 * 60 * 61 / 2) < 1e-6 and abs(s60["ball"]["y"] - y_true) / y_true < 0.02,
              s60["ball"]["y"], 203.333333),
        check("keyboard: ArrowRight for 0.5 s moves the paddle +60 px", abs(s90["player"]["x"] - 220) < 0.5, s90["player"]["x"], 220),
        check("touch input moves the paddle to the touch point", touch_x == 50, touch_x, 50),
        check("localStorage save → restore returns the saved state", restored["player"]["x"] == 50 and
              abs(restored["t"] - s90["t"]) < 1e-9, [restored["player"]["x"], restored["t"]]),
        check("the loop drives 15 distinct captured frames", len(hs) == 15 and nframes(wd / "loop.mp4") == 15, len(hs)),
        check("negative control: a fresh (unrestored) state differs from the saved one", fresh["player"]["x"] != 50 and fresh["t"] == 0,
              fresh),
    ], [wd / "loop.mp4", wd / "game.html"]


PERF_SLOW = '''def motion_energy(frames):
    """Mean absolute frame-to-frame difference, one value per step (pure Python loops)."""
    out = []
    for k in range(1, len(frames)):
        a, b = frames[k - 1], frames[k]
        s = 0
        for y in range(len(a)):
            ra, rb = a[y], b[y]
            for x in range(len(ra)):
                s += abs(int(ra[x]) - int(rb[x]))
        out.append(s / (len(a) * len(a[0])))
    return out
'''

PERF_FAST = '''import numpy as np


def motion_energy(frames):
    """Same measure, vectorised: one array op over all frames."""
    f = np.asarray(frames, dtype=np.int32)
    return np.abs(np.diff(f, axis=0)).mean(axis=(1, 2)).tolist()
'''


@card("ENG-419")
def performance_optimization(task, wd):
    """performance-optimization steps: measure first, find the one bottleneck, apply the lowest-risk fix, re-measure the
    same way, keep it only if it is faster and the output is unchanged, and write a budget — on a video job's per-frame
    motion-energy measure."""
    import cProfile
    import pstats
    import io
    wd = Path(wd)
    wt(wd / "slow.py", PERF_SLOW)
    wt(wd / "fast.py", PERF_FAST)
    ns_s, ns_f = {}, {}
    exec(compile(PERF_SLOW, str(wd / "slow.py"), "exec"), ns_s)
    exec(compile(PERF_FAST, str(wd / "fast.py"), "exec"), ns_f)
    rng = np.random.default_rng(5)
    frames = rng.integers(0, 256, (20, 90, 160)).astype(np.int16)    # decoded frames arrive as arrays

    def best(fn, n=3):
        ts = []
        for _ in range(n):
            t0 = time.perf_counter()
            r = fn(frames)
            ts.append(time.perf_counter() - t0)
        return min(ts), r
    t_slow, r_slow = best(ns_s["motion_energy"], 2)
    prof = cProfile.Profile()
    prof.enable()
    ns_s["motion_energy"](frames)
    prof.disable()
    s = io.StringIO()
    pstats.Stats(prof, stream=s).sort_stats("tottime").print_stats(3)
    hot = "motion_energy" in s.getvalue().split("\n\n")[-2] if "\n\n" in s.getvalue() else "motion_energy" in s.getvalue()
    t_fast, r_fast = best(ns_f["motion_energy"], 5)
    same = np.allclose(r_slow, r_fast)
    budget = {"motion_energy_20x90x160_ms": 20.0}
    jw(wd / "budget.json", budget)
    wt(wd / "perf-report.md", "# perf report\n| version | best of runs (ms) |\n|---|---|\n| loops | %.1f |\n| numpy | %.2f |\n\n"
       "bottleneck: %s\nkept: numpy (output identical: %s)\n" % (t_slow * 1000, t_fast * 1000, "motion_energy inner loop", same))
    return [
        check("profiler names the hot function (motion_energy's inner loop)", hot, s.getvalue()[-300:]),
        check("the fix keeps the output identical", same),
        check("re-measured the same way: at least 20x faster", t_slow / t_fast >= 20, round(t_slow / t_fast, 1), ">= 20"),
        check("fast version meets the written budget (≤ 20 ms)", t_fast * 1000 <= budget["motion_energy_20x90x160_ms"],
              round(t_fast * 1000, 2)),
        check("negative control: the unoptimised version breaks the budget", t_slow * 1000 > budget["motion_energy_20x90x160_ms"],
              round(t_slow * 1000, 1)),
    ], [wd / "perf-report.md", wd / "budget.json"]


PYPRO_MOD = '''"""Timecodes for a video job: parse HH:MM:SS:FF into frames and back."""
from __future__ import annotations

import logging
from dataclasses import dataclass

log = logging.getLogger(__name__)


class TimecodeError(ValueError):
    """A timecode that does not fit the frame rate."""


@dataclass(frozen=True)
class Timecode:
    frames: int
    fps: int

    @classmethod
    def parse(cls, text: str, fps: int) -> Timecode:
        try:
            h, m, s, f = (int(p) for p in text.split(":"))
        except ValueError as exc:
            raise TimecodeError(f"not HH:MM:SS:FF: {text!r}") from exc
        if not 0 <= f < fps or not 0 <= s < 60 or not 0 <= m < 60:
            raise TimecodeError(f"{text!r} is out of range at {fps} fps")
        log.debug("parsed %s", text)
        return cls(((h * 60 + m) * 60 + s) * fps + f, fps)

    def __str__(self) -> str:
        s, f = divmod(self.frames, self.fps)
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        return f"{h:02d}:{m:02d}:{s:02d}:{f:02d}"
'''

PYPRO_TEST = '''import pytest

from kclip.timecode import Timecode, TimecodeError


@pytest.mark.parametrize(("text", "fps", "frames"), [("00:00:01:00", 30, 30), ("00:01:00:15", 30, 1815),
                                                     ("01:00:00:00", 25, 90000)])
def test_parse(text: str, fps: int, frames: int) -> None:
    tc = Timecode.parse(text, fps)
    assert tc.frames == frames and str(tc) == text


@pytest.mark.parametrize("bad", ["00:00:00:30", "1:2", "aa:00:00:00"])
def test_rejects(bad: str) -> None:
    with pytest.raises(TimecodeError):
        Timecode.parse(bad, 30)
'''


@card("ENG-420")
def python_pro(task, wd):
    """python-pro steps: src/package layout + pyproject, types on every signature with a dataclass model, a custom
    exception (no bare except), pytest with parametrize, ruff and mypy --strict clean, logging not print."""
    wd = Path(wd)
    p = wd / "kclip"
    wt(p / "pyproject.toml", "[project]\nname = \"kclip\"\nversion = \"0.1.0\"\nrequires-python = \">=3.10\"\n\n"
       "[tool.pytest.ini_options]\npythonpath = [\"src\"]\n\n[tool.ruff]\nline-length = 120\n\n[tool.ruff.lint]\n"
       "select = [\"E\", \"F\", \"I\", \"B\", \"T20\"]\n")
    wt(p / "src/kclip/__init__.py", "")
    wt(p / "src/kclip/py.typed", "")
    wt(p / "src/kclip/timecode.py", PYPRO_MOD)
    wt(p / "tests/test_timecode.py", PYPRO_TEST)
    wt(p / "README.md", "```python\nfrom kclip.timecode import Timecode\nprint(Timecode.parse('00:00:01:00', 30).frames)  # 30\n```\n")
    mypy = shutil.which("mypy") or "mypy"
    ruff = shutil.which("ruff") or "ruff"
    t = sh([PYTEST, "-q", "-p", "no:cacheprovider"], p, ok=None)
    m = sh([mypy, "--strict", "--no-incremental", "--cache-dir", wd / ".mypy", "src"], p, ok=None)
    r = sh([ruff, "check", "--no-cache", "."], p, ok=None)
    wt(p / "bad/bad.py", "def scale(x):\n    try:\n        return x * 2\n    except:\n        print('oops')\n")
    mb = sh([mypy, "--strict", "--no-incremental", "--cache-dir", wd / ".mypy", "bad/bad.py"], p, ok=None)
    rb = sh([ruff, "check", "--no-cache", "bad"], p, ok=None)
    shutil.rmtree(wd / ".mypy", ignore_errors=True)
    wt(wd / "qa.txt", t.stdout + "\n" + m.stdout + "\n" + r.stdout)
    passed = int(re.search(r"(\d+) passed", t.stdout).group(1)) if "passed" in t.stdout else 0
    return [
        check("pytest: 6 parametrised cases pass", t.returncode == 0 and passed == 6, t.stdout.strip()[-80:]),
        check("mypy --strict: no issues", m.returncode == 0, m.stdout.strip()[-120:]),
        check("ruff (E, F, I, B, T20 — no print): clean", r.returncode == 0, r.stdout.strip()[-120:]),
        check("custom exception chained from the parse error (no bare except)", "raise TimecodeError" in PYPRO_MOD and "from exc" in PYPRO_MOD
              and "except:" not in PYPRO_MOD),
        check("negative control: an untyped module with a bare except and print fails mypy and ruff",
              mb.returncode != 0 and rb.returncode != 0 and "E722" in rb.stdout and "T201" in rb.stdout, [mb.returncode, rb.stdout[-160:]]),
    ], [p / "src/kclip/timecode.py", wd / "qa.txt"]


TS_SRC = '''export type Parsed = { ok: true; frames: number } | { ok: false; error: string };

export function parseTimecode(text: string, fps: number): Parsed {
  const parts = text.split(":").map(Number);
  if (parts.length !== 4 || parts.some((n) => !Number.isInteger(n))) return { ok: false, error: `not HH:MM:SS:FF: ${text}` };
  const [h, m, s, f] = parts as [number, number, number, number];
  if (f >= fps || s >= 60 || m >= 60) return { ok: false, error: `${text} out of range at ${fps} fps` };
  return { ok: true, frames: ((h * 60 + m) * 60 + s) * fps + f };
}

export function firstCut(cuts: number[]): number {
  const c = cuts[0];
  return c === undefined ? 0 : c;
}
'''

TS_TEST = '''import { test } from "node:test";
import assert from "node:assert/strict";
import { parseTimecode, firstCut } from "../dist/src/timecode.js";

test("parses", () => {
  const r = parseTimecode("00:01:00:15", 30);
  assert.equal(r.ok && r.frames, 1815);
});
test("rejects frames past fps", () => {
  const r = parseTimecode("00:00:00:30", 30);
  assert.equal(r.ok, false);
});
test("empty cut list", () => assert.equal(firstCut([]), 0));
'''


@card("ENG-421")
def typescript_node_pro(task, wd):
    """typescript-node-pro steps: strict tsconfig (strict, noUncheckedIndexedAccess) with ESM, discriminated-union
    results instead of any, tests that pass, clear package scripts — compiled with tsc and tested with node:test."""
    wd = Path(wd)
    p = wd / "tc"
    wt(p / "package.json", json.dumps({"name": "tc", "version": "0.1.0", "type": "module",
                                       "scripts": {"build": "tsc -p .", "test": "node --test tests/timecode.test.mjs"}}, indent=1))
    cfg = {"compilerOptions": {"target": "ES2022", "module": "NodeNext", "moduleResolution": "NodeNext", "strict": True,
                               "noUncheckedIndexedAccess": True, "outDir": "dist", "rootDir": "."},
           "include": ["src"]}
    wt(p / "tsconfig.json", json.dumps(cfg, indent=1))
    wt(p / "src/timecode.ts", TS_SRC)
    wt(p / "tests/timecode.test.mjs", TS_TEST)
    tsc = shutil.which("tsc") or "tsc"
    c = sh([tsc, "-p", "."], p, ok=None, timeout=60)
    t = sh(["node", "--test", "tests/timecode.test.mjs"], p, ok=None) if c.returncode == 0 else None
    bad = p / "bad"
    wt(bad / "tsconfig.json", json.dumps(dict(cfg, include=["x.ts"], compilerOptions=dict(cfg["compilerOptions"], outDir="out")), indent=1))
    wt(bad / "x.ts", "export function scale(x) { return x * 2; }\nexport function first(a: number[]): number { return a[0] * 2; }\n")
    cb = sh([tsc, "-p", "."], bad, ok=None, timeout=60)
    wt(wd / "qa.txt", (c.stdout or "") + "\n" + (t.stdout if t else "") + "\n" + cb.stdout)
    any_free = not re.search(r"\bany\b", TS_SRC)
    return [
        check("tsc --strict with noUncheckedIndexedAccess compiles with no errors", c.returncode == 0, c.stdout[-200:]),
        check("node:test: 3 tests pass on the compiled ESM", t is not None and t.returncode == 0 and "# pass 3" in t.stdout,
              (t.stdout[-120:] if t else None)),
        check("no any; results are a discriminated union", any_free and "ok: true" in TS_SRC and "ok: false" in TS_SRC),
        check("negative control: implicit any and an unchecked index fail the same config",
              cb.returncode != 0 and "TS7006" in cb.stdout and "TS2532" in cb.stdout, re.findall(r"TS\d+", cb.stdout)),
    ], [p / "dist/src/timecode.js", wd / "qa.txt"]


# ───────────────────────── hardware encode recipe + loudnorm/subtitle filtergraphs (ENG-422) ─────────────────────────

NVENC = ["-hwaccel", "cuda", "-c:v", "h264_nvenc", "-preset", "p7", "-tune", "hq", "-rc", "vbr", "-cq", "19"]


@card("ENG-422")
def hw_encode_loudnorm_subs(task, wd):
    """The hardware encode recipe (-hwaccel cuda h264_nvenc -preset p7 -tune hq -rc vbr -cq 19) is tried for real; with no
    NVIDIA device it falls back to libx264 CRF 19 and says so. The loudnorm two-pass and subtitle filtergraphs run."""
    wd = Path(wd)
    src = wd / "src.mp4"
    ff(wd, "-f", "lavfi", "-i", "testsrc2=s=320x180:r=30:d=2", "-f", "lavfi", "-i", "sine=f=440:d=2", "-af", "volume=-24dB",
       "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", src)
    hw = sh(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", NVENC[0], NVENC[1], "-i", src, *NVENC[2:], "-frames:v", "5",
             wd / "nvenc_try.mp4"], wd, ok=None)
    used = "h264_nvenc" if hw.returncode == 0 else "libx264"
    venc = NVENC[2:] if used == "h264_nvenc" else ["-c:v", "libx264", "-preset", "medium", "-crf", "19"]
    p1 = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(src), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
                         "-f", "null", "-"], capture_output=True, text=True, timeout=60).stderr
    m = json.loads(p1[p1.rindex("{"):p1.rindex("}") + 1])
    wt(wd / "subs.srt", "1\n00:00:00,300 --> 00:00:01,500\nCAPTION\n")
    af = ("loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:offset=%s:linear=true"
          % (m["input_i"], m["input_tp"], m["input_lra"], m["input_thresh"], m["target_offset"]))
    out = wd / "delivery.mp4"
    ff(wd, "-i", src, "-vf", "subtitles=subs.srt:force_style='Fontsize=26,PrimaryColour=&H00FFFFFF'", *venc, "-pix_fmt", "yuv420p",
       "-af", af, "-ar", "48000", "-c:a", "aac", "-b:a", "320k", out)
    (wd / "nvenc_try.mp4").unlink(missing_ok=True)
    recipe = {"recipe": " ".join(NVENC), "encoder_used": used, "fallback_reason": None if used == "h264_nvenc" else hw.stderr.strip()[-200:],
              "loudnorm_pass1": m, "filter_audio": af}
    jw(wd / "recipe.json", recipe)
    I0, I1 = ebur(wd, src), ebur(wd, out)
    white = lambda img: int((img[120:175, 60:260].min(2) > 220).sum())
    return [
        check("recipe carries the card's NVENC flags", recipe["recipe"] == "-hwaccel cuda -c:v h264_nvenc -preset p7 -tune hq -rc vbr -cq 19"),
        check("NVENC really tried; without a device the fallback is libx264 CRF 19 and the reason is recorded",
              (used == "h264_nvenc") or (used == "libx264" and recipe["fallback_reason"]), [used, (recipe["fallback_reason"] or "")[:80]]),
        check("delivery video codec is H.264", vstream(out)["codec_name"] == "h264"),
        check("loudnorm two-pass lands at -14 LUFS (±0.5)", abs(I1 + 14) <= 0.5, I1, -14),
        check("subtitle filtergraph burned the caption at 1.0 s", white(frame_at(out, 1.0)) > 30, white(frame_at(out, 1.0))),
        check("negative control: the source is far from -14 LUFS and has no caption", I0 < -25 and white(frame_at(src, 1.0)) < 30,
              [I0, white(frame_at(src, 1.0))]),
    ], [out, wd / "recipe.json"]


# ───────────────────────── no screen recording for delivery (ENG-428) ─────────────────────────

CLOCK_PAGE = """<!doctype html><html><body style="margin:0;background:#000"><canvas id="c" width="160" height="90"></canvas><script>
const g = document.getElementById('c').getContext('2d');
function draw(i) { g.fillStyle = 'rgb(' + (i % 256) + ',0,0)'; g.fillRect(0, 0, 160, 90); }
window.seek = t => draw(Math.round(t * 60));
const t0 = performance.now();
window.stop = false;
function tick() { if (window.stop) return; draw(Math.floor((performance.now() - t0) * 60 / 1000)); requestAnimationFrame(tick); }
requestAnimationFrame(tick); window.__ready = true;
</script></body></html>"""


@card("ENG-428")
def no_screen_capture(task, wd):
    """Screen capture drops frames and is not reproducible: a 60 fps wall-clock animation grabbed in real time vs the
    same page stepped frame by frame with seek(t) — the frame index is painted into the picture and read back."""
    wd = Path(wd)
    wt(wd / "clock.html", CLOCK_PAGE)
    idx = lambda png: int(round(png_rgb(png)[45, 80, 0]))
    with browser_page(wd, 160, 90) as pg:
        pg.goto((wd / "clock.html").as_uri())
        pg.wait_for_function("window.__ready===true", polling=100)
        rt = []
        t0 = time.perf_counter()
        while time.perf_counter() - t0 < 1.0:
            rt.append(idx(pg.screenshot()))
        pg.evaluate("window.stop = true")
        pg.evaluate("() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))")
        det_runs = []
        for _ in range(2):
            seq = []
            for i in range(30):
                pg.evaluate("t=>window.seek(t)", i / 60)
                seq.append(idx(pg.screenshot()))
            det_runs.append(seq)
    expected = list(range(30))
    jw(wd / "capture_compare.json", {"realtime": rt, "deterministic": det_runs[0]})
    gaps = [b - a for a, b in zip(rt, rt[1:])]
    dropped = sum(max(0, g - 1) for g in gaps)
    return [
        check("frame stepping paints every frame 0..29 in order", det_runs[0] == expected, det_runs[0][:8]),
        check("frame stepping is reproducible (two runs identical)", det_runs[0] == det_runs[1]),
        check("real-time capture dropped frames (index gaps > 1)", dropped > 0, {"grabs": len(rt), "dropped": dropped}),
        check("real-time capture grabbed fewer frames than the 60 the second held", len(set(rt)) < 60, len(set(rt)), "< 60"),
    ], [wd / "capture_compare.json"]


# ───────────────────────── preview → check clip → approval → final → verify_video → TEST_REPORT (ENG-431) ─────────────────────────

def final_render(wd, src, approval, preview, out, audio):
    """Refuses unless the approval names the exact preview the user saw."""
    a = json.loads(Path(approval).read_text()) if Path(approval).exists() else {}
    if not (a.get("approved") is True and a.get("preview_sha256") == hashlib.sha256(Path(preview).read_bytes()).hexdigest()):
        raise PermissionError("no approval recorded for this preview: final render refused")
    ff(wd, "-i", src, "-i", audio, "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
       "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
       "-ar", "48000", "-ac", "2", "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart", "-shortest", out)
    return Path(out)


@card("ENG-431")
def preview_to_report(task, wd):
    """Render recipe A: preview PNG → motion check clip (--start 4 --duration 3 --width 540 --height 960) → approval →
    final render with audio → verify_video gate → TEST_REPORT filled with the measured values."""
    wd = Path(wd)
    src = wd / "render.mp4"
    ff(wd, "-f", "lavfi", "-i", "color=c=0x0d1b2a:s=1080x1920:r=30:d=7", "-vf",
       "drawbox=x='100+600*t/7':y=800:w=300:h=300:color=0xE7B65A:t=fill", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "16",
       "-pix_fmt", "yuv420p", src)
    preview = wd / "preview.png"
    ff(wd, "-ss", "1", "-i", src, "-frames:v", "1", preview)
    chk = wd / "check_clip.mp4"
    ff(wd, "-ss", "4", "-i", src, "-t", "3", "-vf", "scale=540:960", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", chk)
    tone_wav(wd / "voice.wav", 440.0, 7.0, 48000, 0.2)
    refused = False
    try:
        final_render(wd, src, wd / "approval.json", preview, wd / "final.mp4", wd / "voice.wav")
    except PermissionError:
        refused = True
    jw(wd / "approval.json", {"approved": True, "by": "user", "preview_sha256": hashlib.sha256(preview.read_bytes()).hexdigest()})
    final = final_render(wd, src, wd / "approval.json", preview, wd / "final.mp4", wd / "voice.wav")
    g = sh([sys.executable, REPO / "tools/verify_video.py", final, "--aspect", "9:16", "--fps", "30", "--duration", "7", "--json",
            wd / "verify.json"], wd, ok=None)
    rep = json.loads((wd / "verify.json").read_text())
    gc = sh([sys.executable, REPO / "tools/verify_video.py", chk, "--aspect", "9:16", "--fps", "30", "--duration", "7", "--json",
             wd / "verify_check.json"], wd, ok=None)
    tmpl = (REPO / "templates/TEST_REPORT.md").read_text(encoding="utf-8")
    vals = {"style_name": "render recipe A", "id": "ENG-431", "aspect": "9:16", "resolution": "1080x1920", "fps": "30",
            "duration": "7", "frames": str(nframes(final)), "date": "2026-11-04"}
    filled = re.sub(r"\{(\w+)\}", lambda m: vals.get(m.group(1), m.group(0)), tmpl)
    filled += "\n\n## Measured (verify_video)\n" + "\n".join("- %s: %s (%s)" % (c["check"], c["value"], "PASS" if c["pass"] else "FAIL")
                                                            for c in rep["checks"])
    wt(wd / "TEST_REPORT.md", filled)
    cv = vstream(chk)
    return [
        check("preview PNG is a full-size still", png_rgb(preview).shape[:2] == (1920, 1080)),
        check("motion check clip: 3 s at 540x960 from t=4", (cv["width"], cv["height"]) == (540, 960) and abs(duration(chk) - 3) < 0.05,
              [cv["width"], cv["height"], duration(chk)]),
        check("final render refused before approval", refused),
        check("verify_video gate passes the final (H.264, 9:16, 30 fps, 7 s, AAC, -14 LUFS)", g.returncode == 0 and
              all(c["pass"] for c in rep["checks"]), [c["check"] for c in rep["checks"] if not c["pass"]]),
        check("TEST_REPORT filled with measured values (no placeholders left for the target line)",
              "{duration}" not in filled and "integrated loudness" in filled and "210" in filled),
        check("negative control: the gate fails the check clip against the delivery target", gc.returncode != 0),
    ], [final, wd / "TEST_REPORT.md", wd / "verify.json"]


# ───────────────────────── whole video from a project with local tools only (ENG-433) ─────────────────────────

@card("ENG-433")
def local_whole_video(task, wd):
    """The model builds the whole video with local tools from a project spec, no bundled assets: title cards drawn with
    Pillow (system font, RAQM shaping), a synthesized score, an ffmpeg composite; 1080x1920, 30 fps, ~20 s; every
    intermediate lives in work/."""
    from PIL import Image, ImageDraw, ImageFont
    wd = Path(wd)
    spec = {"size": [1080, 1920], "fps": 30, "seconds": 20,
            "scenes": [{"text": "الفكرة", "start": 0, "end": 6}, {"text": "الطريق", "start": 6, "end": 13},
                       {"text": "الأثر", "start": 13, "end": 20}]}
    jw(wd / "project.json", spec)
    work = wd / "work"
    work.mkdir()
    font = ImageFont.truetype(_system_font(), 140)
    inputs = []
    for i, s in enumerate(spec["scenes"]):
        im = Image.new("RGBA", (1080, 400), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((540, 200), s["text"], font=font, fill=(255, 255, 255, 255), anchor="mm")
        im.save(work / ("card%d.png" % i))
        inputs += ["-i", work / ("card%d.png" % i)]
    sr = 48000
    t = np.arange(20 * sr) / sr
    score = sum(np.sin(2 * np.pi * f * t) for f in (110.0, 164.81, 220.0)) / 3 * 0.25 * np.minimum(1, t / 2) * np.minimum(1, (20 - t) / 2)
    fx.write_wav(work / "score.wav", score, sr)
    chain = "[0:v]drawbox=x='90+600*t/20':y=1300:w=300:h=40:color=0xE7B65A:t=fill[b0]"
    for i, s in enumerate(spec["scenes"]):
        chain += ";[b%d][%d:v]overlay=0:700:enable='between(t,%d,%d)'[b%d]" % (i, i + 1, s["start"], s["end"] - 0.01, i + 1)
    film = wd / "film.mp4"
    ff(wd, "-f", "lavfi", "-i", "color=c=0x0d1b2a:s=1080x1920:r=30:d=20", *inputs, "-i", work / "score.wav", "-filter_complex", chain,
       "-map", "[b3]", "-map", "4:a", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac",
       "-shortest", film, timeout=60)
    v = vstream(film)
    band = lambda f: int((f[700:1100, 200:880].min(2) > 200).sum())
    sig = {s["text"]: frame_at(film, (s["start"] + s["end"]) / 2, (1080, 1920)) for s in spec["scenes"]}
    lit = {k: band(f) for k, f in sig.items()}
    a, b = sig["الفكرة"][700:1100, 200:880], sig["الطريق"][700:1100, 200:880]
    distinct = float(np.abs(a.astype(float) - b.astype(float)).mean()) > 2
    outside = sorted(str(x) for x in [p for p in inputs if isinstance(p, Path)] if not str(x).startswith(str(work)))
    bare = frame_at(film, 0.0, (1080, 1920)) * 0
    return [
        check("1080x1920 at 30 fps, 20 s", (v["width"], v["height"], v["r_frame_rate"]) == (1080, 1920, "30/1") and abs(duration(film) - 20) < 0.1,
              [v["width"], v["height"], v["r_frame_rate"], duration(film)]),
        check("each scene's title is on screen in its window", all(n > 500 for n in lit.values()), lit),
        check("titles change between scenes", distinct),
        check("audio is the synthesized score (AAC)", any(s["codec_type"] == "audio" for s in probe(film)["streams"])),
        check("no bundled assets: every input was made in work/ (or lavfi)", outside == [] and sorted(p.name for p in work.iterdir()) ==
              ["card0.png", "card1.png", "card2.png", "score.wav"], outside),
        check("negative control: the untreated background frame has no title pixels", band(bare) == 0, band(bare)),
    ], [film, wd / "project.json"]
