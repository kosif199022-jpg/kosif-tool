"""Wave-2 "remotion" programs for the engines-render-pipeline family (ENG-*).

These cards were skipped in wave 1 because they need Remotion or esbuild, which live only in
the Remotion starter's node_modules (starters/remotion, installed with `npm ci` from its own
lockfile). Each program writes a tiny Remotion project (or esbuild fixture) into `work`, renders
a few small frames with the starter's @remotion/renderer and a local Playwright Chromium
headless shell through `_remotion_helper.cjs`, and measures pixels, metadata or bundle bytes
against answers known in advance.

Offline: no npm install, no browser download (the helper refuses one), and the node child gets
http(s)_proxy pointed at a dead local port with no_proxy=localhost, so the page can reach only
Remotion's own localhost bundle server. Bundling uses the starter's esbuild with the same entry
chain as @remotion/bundler (webpack would take ~10 s per card); the CLI (`npx remotion ...`)
calls the same renderer functions used here.
"""
from __future__ import annotations

import base64
import json
import math
import os
import re
import shutil
import subprocess
import urllib.parse
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parents[5]
STARTER = REPO / "starters" / "remotion"
NM = STARTER / "node_modules"
HELPER = Path(__file__).resolve().with_name("_remotion_helper.cjs")
DEAD = "http://127.0.0.1:9"
OFFLINE_ENV = {"http_proxy": DEAD, "https_proxy": DEAD, "HTTP_PROXY": DEAD, "HTTPS_PROXY": DEAD,
               "all_proxy": DEAD, "ALL_PROXY": DEAD, "no_proxy": "localhost,127.0.0.1",
               "NO_PROXY": "localhost,127.0.0.1"}

# ---------------------------------------------------------------- shared helpers


def need_starter():
    if not (NM / "remotion" / "package.json").is_file() or not (NM / "esbuild").is_dir():
        raise RuntimeError("starters/remotion/node_modules is missing: run `npm ci` in starters/remotion")


def env(extra=None):
    e = dict(os.environ)
    e.update(OFFLINE_ENV)
    e.update(extra or {})
    return e


def render(work: Path, name: str, files: dict, composition: str, extra_env=None, **job) -> dict:
    """Write a Remotion project (files: relative path -> text/bytes), bundle and render it."""
    need_starter()
    proj = work / name
    for rel, data in files.items():
        p = proj / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data) if isinstance(data, bytes) else p.write_text(data, encoding="utf-8")
    job.setdefault("entry", str(proj / "index.jsx"))
    job.setdefault("outDir", str(proj / "out"))
    job["composition"] = composition
    jf = proj / "job.json"
    jf.parent.mkdir(parents=True, exist_ok=True)
    jf.write_text(json.dumps(job, ensure_ascii=False), encoding="utf-8")
    r = subprocess.run(["node", str(HELPER), str(jf)], capture_output=True, text=True, timeout=90,
                       env=env(extra_env))
    lines = [ln for ln in r.stdout.splitlines() if ln.startswith("{")]
    res = json.loads(lines[-1]) if lines else {"error": (r.stderr or r.stdout)[-800:]}
    if r.returncode != 0 or "error" in res:
        raise RuntimeError(f"remotion render failed: {res.get('error')}")
    (proj / "render-result.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    return res


def try_render(*a, **k):
    try:
        return render(*a, **k), ""
    except RuntimeError as e:
        return None, str(e)


def node(code: str, cwd: Path, extra_env=None) -> str:
    """Run a node script that can require the starter's packages (NODE_PATH)."""
    need_starter()
    e = env({"NODE_PATH": str(NM)})
    e.update(extra_env or {})
    r = subprocess.run(["node", "-e", code], capture_output=True, text=True, cwd=cwd, env=e, timeout=60)
    if r.returncode != 0:
        raise RuntimeError(f"node failed: {r.stderr[-800:]}")
    return r.stdout


def esbuild_cli(args, cwd: Path) -> str:
    need_starter()
    r = subprocess.run([str(NM / ".bin" / "esbuild"), *args], capture_output=True, text=True, cwd=cwd,
                       env=env(), timeout=60)
    if r.returncode != 0:
        raise RuntimeError(f"esbuild failed: {r.stderr[-800:]}")
    return r.stderr


def img(path) -> np.ndarray:
    return np.asarray(Image.open(path).convert("RGB")).astype(int)


def hexrgb(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def mask(a, rgb, tol=40):
    return (np.abs(a - np.array(rgb)).max(axis=2) <= tol)


def bbox(a, rgb, tol=40):
    ys, xs = np.nonzero(mask(a, rgb, tol))
    if not len(xs):
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def centroid_x(a, channel=0, thresh=30):
    w = a[..., channel].astype(float) * (a[..., channel] > thresh)
    s = w.sum()
    return float((w.sum(axis=0) * np.arange(a.shape[1])).sum() / s) if s else float("nan")


def psnr(a, b) -> float:
    mse = float(((a.astype(float) - b.astype(float)) ** 2).mean())
    return 99.0 if mse == 0 else 10 * math.log10(255 ** 2 / mse)


def ffprobe(path) -> dict:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def vstream(path) -> dict:
    return next(s for s in ffprobe(path)["streams"] if s["codec_type"] == "video")


def pkg_version(name) -> str:
    return json.loads((NM / name / "package.json").read_text())["version"]


PRE = ('import React from "react";\n'
       'import {registerRoot, Composition, AbsoluteFill, Sequence, Series, useCurrentFrame, useVideoConfig,'
       ' interpolate, Easing, random, spring, staticFile, OffthreadVideo, Interactive} from "remotion";\n')


def root(cid, comp, w, h, fps, dur, extra=""):
    return (f'registerRoot(() => <Composition id="{cid}" component={{{comp}}} width={{{w}}} height={{{h}}}'
            f' fps={{{fps}}} durationInFrames={{{dur}}} {extra}/>);\n')


# ---------------------------------------------------------------- ENG-312 KosifFilm composition

def eng_312(work: Path):
    """Render the starter's own KosifFilm (src/index.ts, props.example.json) at 1/4 size, jpeg frames."""
    props = json.loads((STARTER / "props.example.json").read_text(encoding="utf-8"))
    res = render(work, "kosif-film", {}, "KosifFilm", entry=str(STARTER / "src" / "index.ts"),
                 publicDir=str(STARTER / "public"), props=props, scale=0.25, imageFormat="jpeg",
                 stills=[60], variants=[{"name": "default-props", "props": {}, "frame": 60}],
                 media={"out": str(work / "kosif-film" / "out" / "film-58-62.mp4"), "frameRange": [58, 62],
                        "imageFormat": "jpeg"})
    c = res["composition"]
    out = work / "kosif-film" / "out"
    with_props = img(out / "still-0060.jpeg")
    default = img(out / "variant-default-props.jpeg")
    green, orange = hexrgb(props["accent"]), hexrgb("#ff7a1a")
    g1, o1 = int(mask(with_props, green, 30).sum()), int(mask(with_props, orange, 30).sum())
    g2, o2 = int(mask(default, green, 30).sum()), int(mask(default, orange, 30).sum())
    v = vstream(out / "film-58-62.mp4")
    return [
        ("composition 1080x1920 @30 fps, 12 s = 360 frames",
         (c["width"], c["height"], c["fps"], c["durationInFrames"]) == (1080, 1920, 30, 360), str(c)[:200]),
        ("props.example.json reach the composition", c["props"]["title"] == props["title"], c["props"]["title"]),
        ("pinned remotion 4.0.535 and react 19.3.1 installed",
         (pkg_version("remotion"), pkg_version("react")) == ("4.0.535", "19.3.1"),
         f"{pkg_version('remotion')} / {pkg_version('react')}"),
        ("frame 60 at scale 0.25 is 270x480", with_props.shape[:2] == (480, 270), str(with_props.shape)),
        ("props accent #19c37d drawn, default #ff7a1a absent", g1 > 60 and o1 < 5, f"green={g1} orange={o1}"),
        ("default props draw the #ff7a1a accent instead", o2 > 60 and g2 < 5, f"green={g2} orange={o2}"),
        ("jpeg-frame mp4 of frames 58-62 has 5 frames at 270x480",
         (int(v["nb_frames"]), v["width"], v["height"], v["codec_name"]) == (5, 270, 480, "h264"),
         f"{v['nb_frames']} {v['width']}x{v['height']} {v['codec_name']}"),
    ]


# ---------------------------------------------------------------- ENG-317 delivery path (still + render)

def eng_317(work: Path):
    """still KosifFilm --frame=60, then render with --props=props.json; the render's frame 60 equals the still."""
    props = {"title": "عرض التسليم", "words": ["أ", "ب"], "accent": "#3b82f6", "lang": "ar"}
    pj = work / "props.json"
    pj.write_text(json.dumps(props, ensure_ascii=False), encoding="utf-8")
    out = work / "delivery" / "out"
    res = render(work, "delivery", {}, "KosifFilm", entry=str(STARTER / "src" / "index.ts"),
                 publicDir=str(STARTER / "public"), props=json.loads(pj.read_text(encoding="utf-8")),
                 scale=0.25, stills=[60],
                 media={"out": str(out / "film.mp4"), "frameRange": [58, 62], "crf": 12})
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(out / "film.mp4"), "-vf", r"select=eq(n\,2)",
                    "-frames:v", "1", str(out / "film-frame60.png")], check=True)
    still, frame = img(out / "still-0060.png"), img(out / "film-frame60.png")
    p = psnr(still, frame)
    other = psnr(still, img_frame(out / "film.mp4", 0, out / "film-frame58.png"))
    v = vstream(out / "film.mp4")
    blue = int(mask(still, hexrgb("#3b82f6"), 30).sum())
    return [
        ("still is a PNG of frame 60", (out / "still-0060.png").read_bytes()[:8] == b"\x89PNG\r\n\x1a\n", "png magic"),
        ("render honours props.json (accent #3b82f6 in the still)", blue > 60, f"accent pixels={blue}"),
        ("render frame 60 matches the still (PSNR > 30 dB)", p > 30, f"{p:.1f} dB"),
        ("frame 60 matches better than frame 58", p > other, f"60: {p:.1f} dB vs 58: {other:.1f} dB"),
        ("film.mp4 holds frames 58-62: 5 frames, 30 fps, h264",
         (int(v["nb_frames"]), v["r_frame_rate"], v["codec_name"]) == (5, "30/1", "h264"),
         f"{v['nb_frames']} {v['r_frame_rate']} {v['codec_name']}"),
        ("composition resolved from the starter", res["composition"]["id"] == "KosifFilm", res["composition"]["id"]),
    ]


def img_frame(video, n, out_png):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-vf", f"select=eq(n\\,{n})",
                    "-frames:v", "1", str(out_png)], check=True)
    return img(out_png)


# ---------------------------------------------------------------- tiny box composition used by 313/430/163

BOX = PRE + """const C = () => { const f = useCurrentFrame();
  return <AbsoluteFill style={{background: "#000"}}>
    <div style={{position: "absolute", left: 10 + f * 4, top: 10, width: 12, height: 12, background: "#ff0000"}}/>
  </AbsoluteFill>; };
""" + root("Box", "C", 96, 40, 30, 10)


def box_ok(png, frame):
    b = bbox(img(png), (255, 0, 0), 40)
    return b == (10 + 4 * frame, 10, 21 + 4 * frame, 21), b


# ---------------------------------------------------------------- ENG-313 local Chromium reuse

CONFIG_STUB = """const calls = (globalThis.__calls = globalThis.__calls || []);
exports.Config = new Proxy({}, { get: (t, k) => (...a) => { calls.push([k, ...a]); } });
"""


def eval_config(work: Path, env_extra: dict) -> str | None:
    """Evaluate starters/remotion/remotion.config.ts with a recording Config stub; return the browser set."""
    stub = work / "config-stub.cjs"
    stub.write_text(CONFIG_STUB)
    code = f"""
const esbuild = require({json.dumps(str(NM / 'esbuild'))});
const r = esbuild.buildSync({{ entryPoints: [{json.dumps(str(STARTER / 'remotion.config.ts'))}], bundle: true,
  platform: 'node', format: 'cjs', write: false, logLevel: 'silent',
  alias: {{ '@remotion/cli/config': {json.dumps(str(stub))} }} }});
const m = {{ exports: {{}} }};
new Function('require', 'module', 'exports', r.outputFiles[0].text)(require, m, m.exports);
const set = (globalThis.__calls || []).filter((c) => c[0] === 'setBrowserExecutable');
console.log(JSON.stringify({{ browser: set.length ? set[0][1] : null, calls: globalThis.__calls.map((c) => c[0]) }}));
"""
    e = {"KOSIF_BROWSER": "", "PLAYWRIGHT_BROWSERS_PATH": ""}
    e.update(env_extra)
    out = node(code, work, e)
    return json.loads(out.strip().splitlines()[-1])["browser"]


def tree_state(d: Path):
    """Files under d with size and mtime (empty when d is absent)."""
    return sorted((str(p), p.stat().st_size, p.stat().st_mtime_ns) for p in d.rglob("*")) if d.exists() else []


def fake_exe(p: Path):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("#!/bin/sh\nexit 3\n")
    p.chmod(0o755)
    return str(p)


def eng_313(work: Path):
    """Config.setBrowserExecutable(found) from remotion.config.ts; --browser-executable wins; no download."""
    home = work / "home"
    home.mkdir()
    kosif = fake_exe(work / "kosif-browser" / "chrome")
    both = work / "pw-both"
    shell = fake_exe(both / "chromium_headless_shell-1200" / "chrome-headless-shell-linux64" / "chrome-headless-shell")
    fake_exe(both / "chromium-1200" / "chrome-linux64" / "chrome")
    only_full = work / "pw-full"
    full = fake_exe(only_full / "chromium-1200" / "chrome-linux64" / "chrome")
    r_env = eval_config(work, {"KOSIF_BROWSER": kosif, "HOME": str(home)})
    r_shell = eval_config(work, {"PLAYWRIGHT_BROWSERS_PATH": str(both), "HOME": str(home)})
    r_full = eval_config(work, {"PLAYWRIGHT_BROWSERS_PATH": str(only_full), "HOME": str(home)})
    r_missing = eval_config(work, {"KOSIF_BROWSER": str(work / "nope"), "PLAYWRIGHT_BROWSERS_PATH": str(both),
                                   "HOME": str(home)})
    real = eval_config(work, {})
    remotion_dl = NM / ".remotion"
    before = tree_state(remotion_dl)
    ok_res, ok_err = try_render(work, "real", {"index.jsx": BOX}, "Box", browser=real, stills=[2])
    bad_res, bad_err = try_render(work, "fake", {"index.jsx": BOX}, "Box",
                                  browser=fake_exe(work / "broken" / "chrome"), stills=[2])
    good, b = box_ok(work / "real" / "out" / "still-0002.png", 2) if ok_res else (False, ok_err)
    return [
        ("KOSIF_BROWSER wins", r_env == kosif, str(r_env)),
        ("headless shell preferred over full chromium", r_shell == shell, str(r_shell)),
        ("full chromium used when no headless shell", r_full == full, str(r_full)),
        ("missing KOSIF_BROWSER falls through to playwright root", r_missing == shell, str(r_missing)),
        ("this machine resolves an existing Chromium", bool(real) and Path(real).is_file(), str(real)),
        ("render with the reused Chromium draws the known box", good and ok_res["browser"] == real, f"{b}"),
        ("no Remotion browser download happened", tree_state(remotion_dl) == before,
         f"node_modules/.remotion files unchanged: {len(before)}"),
        ("a broken --browser-executable really is used (render fails)", bad_res is None, bad_err[:160]),
    ]


# ---------------------------------------------------------------- ENG-430 cloud machine browser paths

def cloud_paths(node_roots, browser_roots):
    """The card's two locations: <root>/node_modules/playwright and chromium_headless_shell-*/.../headless_shell."""
    pw = next((str(Path(r) / "node_modules" / "playwright") for r in node_roots
               if (Path(r) / "node_modules" / "playwright" / "package.json").is_file()), None)
    shells = []
    for r in browser_roots:
        for d in Path(r).glob("chromium_headless_shell-*") if Path(r).is_dir() else []:
            m = re.fullmatch(r"chromium_headless_shell-(\d+)", d.name)
            for exe in (d / "chrome-linux" / "headless_shell", d / "chrome-headless-shell-linux64" / "chrome-headless-shell"):
                if m and exe.is_file():
                    shells.append((int(m.group(1)), str(exe)))
    shells.sort(reverse=True)
    return pw, (shells[0][1] if shells else None)


def eng_430(work: Path):
    fx = work / "fixture"
    (fx / "opt/node-tools/node_modules/playwright").mkdir(parents=True)
    (fx / "opt/node-tools/node_modules/playwright/package.json").write_text('{"name":"playwright","version":"1.0.0"}')
    old = fake_exe(fx / "opt/pw-browsers/chromium_headless_shell-1100/chrome-linux/headless_shell")
    new = fake_exe(fx / "opt/pw-browsers/chromium_headless_shell-1200/chrome-linux/headless_shell")
    fake_exe(fx / "opt/pw-browsers/chromium-1300/chrome-linux/chrome")  # a full build is not a headless shell
    fpw, fshell = cloud_paths([fx / "opt/node-tools"], [fx / "opt/pw-browsers"])
    groot = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    node_roots = ["/opt/node-tools", str(Path(groot).parent) if groot else "/nonexistent"]
    if os.environ.get("KOSIF_PLAYWRIGHT"):  # the repo's documented override: <root>/node_modules/playwright
        node_roots.append(str(Path(os.environ["KOSIF_PLAYWRIGHT"]).parents[1]))
    broots = [p for p in [os.environ.get("PLAYWRIGHT_BROWSERS_PATH"), "/opt/pw-browsers",
                          str(Path.home() / ".cache" / "ms-playwright")] if p]
    pw, shell = cloud_paths(node_roots, broots)
    listing_before = sorted(str(p) for r in broots if Path(r).is_dir() for p in Path(r).iterdir())
    ver = subprocess.run([shell, "--version"], capture_output=True, text=True).stdout.strip() if shell else ""
    res, err = try_render(work, "cloud", {"index.jsx": BOX}, "Box", browser=shell, stills=[3]) if shell else (None, "no shell")
    good, b = box_ok(work / "cloud" / "out" / "still-0003.png", 3) if res else (False, err)
    listing_after = sorted(str(p) for r in broots if Path(r).is_dir() for p in Path(r).iterdir())
    return [
        ("fixture: playwright module found under node-tools", fpw == str(fx / "opt/node-tools/node_modules/playwright"), str(fpw)),
        ("fixture: newest chromium_headless_shell-*/chrome-linux/headless_shell picked", fshell == new and fshell != old, str(fshell)),
        ("machine: preinstalled playwright module found", bool(pw), str(pw)),
        ("machine: headless shell found and reports a Chrome version", bool(shell) and "Chrome" in ver, f"{shell} | {ver}"),
        ("Remotion renders with that headless_shell (known box)", good, str(b)),
        ("no playwright install: browser roots unchanged", listing_before == listing_after, f"{len(listing_after)} entries"),
    ]


# ---------------------------------------------------------------- ENG-314 stack option remotion

def eng_314(work: Path):
    kosif = REPO / "tools" / "kosif.py"
    run = lambda *a: subprocess.run([sys.executable, str(kosif), *a], capture_output=True, text=True, timeout=60)
    p_rem = run("prompt", "kinetic-arabic", "--stack", "remotion")
    p_can = run("prompt", "kinetic-arabic", "--stack", "canvas")
    (work / "prompt-remotion.txt").write_text(p_rem.stdout, encoding="utf-8")
    dest = work / "project"
    sc = run("scaffold", "kinetic-arabic", str(dest), "--starter", "remotion", "--stack", "remotion")
    copy = dest / "remotion"
    res = render(work, "from-scaffold", {}, "KosifFilm", entry=str(copy / "src" / "index.ts"),
                 publicDir=str(copy / "public"), scale=0.1, stills=[60])
    still = img(work / "from-scaffold" / "out" / "still-0060.png")
    return [
        ("--stack remotion names Remotion/React and starters/remotion",
         p_rem.returncode == 0 and "Remotion/React (مشروع starters/remotion في المستودع)" in p_rem.stdout,
         f"rc={p_rem.returncode} names Remotion={'Remotion/React' in p_rem.stdout}"),
        ("--stack canvas does not", "Remotion/React" not in p_can.stdout, str("Remotion/React" in p_can.stdout)),
        ("scaffold --starter remotion copies the starter", sc.returncode == 0 and (copy / "src" / "Film.tsx").is_file()
         and (copy / "package.json").is_file(), sc.stdout[-160:]),
        ("the copy has no node_modules", not (copy / "node_modules").exists(), str((copy / "node_modules").exists())),
        ("scaffolded project renders KosifFilm 1080x1920 (frame 60 at 0.1 = 108x192)",
         res["composition"]["width"] == 1080 and still.shape[:2] == (192, 108), str(still.shape)),
    ]


# ---------------------------------------------------------------- ENG-130 parameterized launch video

RANDOM_EXPR = 'random("launch-seed")'
LAUNCH = PRE + """const STAGE = ({color, bx}) => <div style={{position: "absolute", left: bx, top: 100, width: 200, height: 80, background: color}}/>;
const Launch = ({stages}) => { const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const bx = Math.floor(__RANDOM__ * 1500);
  return <AbsoluteFill style={{background: "#000"}}>
    <Series>{stages.map((s, i) => <Series.Sequence key={i} durationInFrames={fps} premountFor={10}><STAGE color={s.color} bx={bx}/></Series.Sequence>)}</Series>
    <div style={{position: "absolute", right: 40, top: 40, color: "#888", fontSize: 40}}>{(f / fps).toFixed(1)}s</div>
    <Sequence from={45} premountFor={15} name="LowerThird"><div style={{position: "absolute", left: 0, bottom: 0, width: "100%", height: 120, background: "#ffffff"}}/></Sequence>
  </AbsoluteFill>; };
registerRoot(() => <Composition id="Launch" component={Launch} fps={30} width={1920} height={1080} durationInFrames={1}
  defaultProps={{aspect: "16:9", stages: []}}
  calculateMetadata={({props}) => ({durationInFrames: props.stages.length * 30,
    width: props.aspect === "9:16" ? 1080 : 1920, height: props.aspect === "9:16" ? 1920 : 1080})}/>);
"""


def eng_130(work: Path):
    stages = [{"color": "#ff0000"}, {"color": "#00ff00"}, {"color": "#0000ff"}]
    props = {"aspect": "16:9", "stages": stages}
    src = LAUNCH.replace("__RANDOM__", RANDOM_EXPR)
    res = render(work, "launch", {"index.jsx": src}, "Launch", props=props, scale=0.1, stills=[40, 45, 50, 70],
                 frames=[50, 50], variants=[{"name": "vertical", "props": {"aspect": "9:16", "stages": stages}}])
    out = work / "launch" / "out"
    expected = float(node(f"console.log(require('remotion').random('launch-seed'))", work).strip())
    exp_left = math.floor(expected * 1500) / 10
    s40, s45, s50, s70 = (img(out / f"still-{n:04d}.png") for n in (40, 45, 50, 70))
    green = bbox(s40, (0, 255, 0), 60)
    blue = bbox(s70, (0, 0, 255), 60)
    lower40, lower45 = int(mask(s40, (255, 255, 255), 20)[-10:].sum()), int(mask(s45, (255, 255, 255), 20)[-10:].sum())
    again = img(out / "element-50.png") if (out / "element-50.png").exists() else img(sorted(out.glob("element-*.png"))[0])
    versions = {p.parent.name: json.loads(p.read_text())["version"] for p in (NM / "@remotion").glob("*/package.json")}
    versions["remotion"] = pkg_version("remotion")
    pinned = json.loads((STARTER / "package.json").read_text())["dependencies"]
    c, v = res["composition"], res["variants"]["vertical"]
    return [
        ("calculateMetadata: 3 stages -> 90 frames, 1920x1080 @30", (c["durationInFrames"], c["width"], c["height"], c["fps"]) == (90, 1920, 1080, 30), str(c)[:120]),
        ("same logic gives 1080x1920 for 9:16", (v["width"], v["height"]) == (1080, 1920), f"{v['width']}x{v['height']}"),
        ("all remotion packages on one exact version", len(set(versions.values())) == 1, str(sorted(set(versions.values())))),
        ("package.json pins exact versions (no ^ or ~)", all(re.fullmatch(r"\d+\.\d+\.\d+", x) for k, x in pinned.items() if "remotion" in k), str(pinned)),
        ("Series: frame 40 shows stage 2 colour, frame 70 stage 3", green is not None and blue is not None, f"{green} {blue}"),
        ("random(seed) places the badge where random('launch-seed') says",
         green is not None and abs(green[0] - exp_left) <= 1.0, f"left={green and green[0]} expected={exp_left:.1f}"),
        ("premounted lower third hidden at frame 40, shown at 45", lower40 == 0 and lower45 > 100, f"{lower40} -> {lower45}"),
        ("deterministic: two renders of frame 50 identical", np.array_equal(s50, again), f"diff={int(np.abs(s50 - again).sum())}"),
    ]


# ---------------------------------------------------------------- ENG-163 Remotion route with fallback

def validate_remotion(work: Path, starter: Path) -> tuple[bool, str]:
    pkg = starter / "node_modules" / "remotion" / "package.json"
    if not pkg.is_file():
        return False, f"remotion not installed in {starter}"
    res, err = try_render(work, f"validate-{starter.name}", {"index.jsx": BOX}, "Box", stills=[1],
                          extra_env={"KOSIF_REMOTION_STARTER": str(starter)})
    if not res:
        return False, err
    ok, b = box_ok(work / f"validate-{starter.name}" / "out" / "still-0001.png", 1)
    return ok, f"known-answer still {'ok' if ok else 'wrong'}: {b}"


def native_canvas_box(path: Path, frame: int):
    im = Image.new("RGB", (96, 40), (0, 0, 0))
    ImageDraw.Draw(im).rectangle([10 + 4 * frame, 10, 21 + 4 * frame, 21], fill=(255, 0, 0))
    im.save(path)


def route(work: Path, starter: Path):
    ok, why = validate_remotion(work, starter)
    if ok:
        return "remotion", why
    native_canvas_box(work / f"native-{starter.name}.png", 1)
    return "native-canvas", why


def eng_163(work: Path):
    broken = work / "starter-not-installed"
    (broken / "src").mkdir(parents=True)
    r_real, why_real = route(work, STARTER)
    r_broken, why_broken = route(work, broken)
    nat_ok, b = box_ok(work / f"native-{broken.name}.png", 1) if r_broken == "native-canvas" else (False, None)
    return [
        ("installed + validated starter routes to remotion", r_real == "remotion", f"{r_real}: {why_real}"),
        ("uninstalled starter routes to native canvas", r_broken == "native-canvas", f"{r_broken}: {why_broken}"),
        ("the reason names the missing install", "not installed" in why_broken, why_broken[:120]),
        ("native fallback renders the same known frame", nat_ok, str(b)),
    ]


# ---------------------------------------------------------------- ENG-124 studio-editable Interactive markup

INTERACTIVE = PRE + """const C = () => { const frame = useCurrentFrame();
  return <AbsoluteFill style={{background: "#000"}}>
    <Interactive.Div name="Title" style={{position: "absolute", left: 20, top: 20, width: 20, height: 20, background: "#ff0000",
      scale: interpolate(frame, [0, 100], [1, 2]), translate: interpolate(frame, [0, 100], ["0px 0px", "__END__"]), rotate: "0deg"}}/>
    <Interactive.Div name="Badge" style={{position: "absolute", left: 250, top: 10, width: 10, height: 10, background: "#00ff00"}}/>
  </AbsoluteFill>; };
""" + root("Edit", "C", 300, 200, 30, 101)
TRANSLATE_END = "100px 100px"


def lint_editable(src: str) -> list:
    issues = []
    if re.search(r"\btransform\s*:", src):
        issues.append("transform string (use scale/translate/rotate props)")
    if re.search(r"\.map\(.*?=>\s*<Interactive\.", src):
        issues.append("Interactive clips generated by .map()")
    names = re.findall(r"<Interactive\.\w+\s+name=\"([^\"]+)\"", src)
    if len(names) != len(re.findall(r"<Interactive\.\w+", src)):
        issues.append("Interactive element without a name")
    return issues


def eng_124(work: Path):
    src = INTERACTIVE.replace("__END__", TRANSLATE_END)
    render(work, "edit", {"index.jsx": src}, "Edit", stills=[0, 50, 100])
    out = work / "edit" / "out"
    got = {f: bbox(img(out / f"still-{f:04d}.png"), (255, 0, 0), 60) for f in (0, 50, 100)}
    # translate t*100 px and scale 1+t about the 20x20 box centre (30, 30)
    exp = {}
    for f in (0, 50, 100):
        t = f / 100
        cx = cy = 30 + 100 * t
        half = 10 * (1 + t)
        exp[f] = (round(cx - half), round(cy - half), round(cx + half) - 1, round(cy + half) - 1)
    close = {f: got[f] is not None and max(abs(a - b) for a, b in zip(got[f], exp[f])) <= 1 for f in got}
    bad_src = src.replace('<Interactive.Div name="Badge"', '{[1, 2].map((i) => <Interactive.Div key={i}').replace(
        'background: "#00ff00"}}/>', 'background: "#00ff00"}}/>)}', 1)
    bad_src2 = src.replace('scale: interpolate(frame, [0, 100], [1, 2]),', 'transform: `scale(${1 + frame / 100})`,')
    return [
        ("frame 0: box at its authored 20..39", close[0], f"{got[0]} vs {exp[0]}"),
        ("frame 50: translate 50px + scale 1.5", close[50], f"{got[50]} vs {exp[50]}"),
        ("frame 100: translate 100px 100px + scale 2", close[100], f"{got[100]} vs {exp[100]}"),
        ("source uses individual transform props and named nodes", lint_editable(src) == [], str(lint_editable(src))),
        ("lint catches .map()-generated clips", "Interactive clips generated by .map()" in lint_editable(bad_src), str(lint_editable(bad_src))),
        ("lint catches a transform string", any("transform string" in i for i in lint_editable(bad_src2)), str(lint_editable(bad_src2))),
    ]


# ---------------------------------------------------------------- ENG-350 real component reuse

PRODUCT_BUTTON = """import React from "react";
export const TONES = {primary: "#2563eb", danger: "#dc2626"};
export const Button = ({label, tone = "primary", style}) => (
  <button data-tone={tone} style={{background: TONES[tone], color: "#ffffff", border: 0, width: 60, height: 24, fontSize: 1, ...style}}>{label}</button>
);
"""
SCENE_IMPORT = "./product/Button.jsx"
REUSE_SCENE = PRE + """import {Button} from "__IMPORT__";
const C = () => <AbsoluteFill style={{background: "#000"}}>
  <Button label="Buy" tone="primary" style={{position: "absolute", left: 10, top: 10}}/>
  <Button label="Delete" tone="danger" style={{position: "absolute", left: 90, top: 10}}/>
</AbsoluteFill>;
""" + root("Reuse", "C", 160, 44, 30, 1)
MOCK_BUTTON = PRODUCT_BUTTON.replace("#2563eb", "#22c55e").replace("#dc2626", "#a855f7")


def eng_350(work: Path):
    files = {"product/Button.jsx": PRODUCT_BUTTON, "mock/Button.jsx": MOCK_BUTTON,
             "index.jsx": REUSE_SCENE.replace("__IMPORT__", SCENE_IMPORT)}
    render(work, "reuse", files, "Reuse", stills=[0])
    a = img(work / "reuse" / "out" / "still-0000.png")
    # the product app's own server render of the same component file
    code = f"""require('esbuild').buildSync({{ entryPoints: [{json.dumps(str(work / 'reuse' / 'product' / 'Button.jsx'))}],
  bundle: true, platform: 'node', format: 'cjs', outfile: {json.dumps(str(work / 'button.cjs'))}, jsx: 'automatic',
  external: ['react'], logLevel: 'silent' }});
const React = require('react'); const {{renderToStaticMarkup}} = require('react-dom/server');
const {{Button}} = require({json.dumps(str(work / 'button.cjs'))});
console.log(renderToStaticMarkup(React.createElement('div', null, React.createElement(Button, {{label: 'Buy'}}),
  React.createElement(Button, {{label: 'Delete', tone: 'danger'}}))));"""
    html = node(code, work).strip()
    (work / "product-markup.html").write_text(html, encoding="utf-8")
    tones = re.findall(r"background:(#[0-9a-f]{6})", html)
    left = a[10:34, 10:70].reshape(-1, 3).mean(axis=0)
    right = a[10:34, 90:150].reshape(-1, 3).mean(axis=0)
    near = lambda m, h: float(np.abs(m - np.array(hexrgb(h))).max())
    return [
        ("product markup renders both buttons", ">Buy<" in html and ">Delete<" in html, html[:120]),
        ("product tones are #2563eb and #dc2626", tones[:2] == ["#2563eb", "#dc2626"], str(tones)),
        ("scene primary button pixels = product primary tone", near(left, tones[0]) <= 3, f"{left.round(1)} vs {tones[0]}"),
        ("scene danger button pixels = product danger tone", near(right, tones[1]) <= 3, f"{right.round(1)} vs {tones[1]}"),
        ("buttons are 60x24 as the component defines", bbox(a, hexrgb(tones[0]), 10) == (10, 10, 69, 33), str(bbox(a, hexrgb(tones[0]), 10))),
    ]


# ---------------------------------------------------------------- ENG-323 SSR with golden frames

GOLDEN = PRE + """const C = ({value}) => <AbsoluteFill style={{background: "#000"}}>
  {Array.from({length: value}, (_, i) => <div key={i} style={{position: "absolute", left: 8 + i * 20, top: 10, width: 12, height: 30, background: "#ffffff"}}/>)}
</AbsoluteFill>;
""" + root("Report", "C", 120, 50, 30, 30, 'defaultProps={{value: 1}}')


def runs(row):
    r = np.concatenate([[0], row.astype(int), [0]])
    return int((np.diff(r) == 1).sum())


def eng_323(work: Path):
    out = work / "ssr" / "out"
    render(work, "ssr", {"index.jsx": GOLDEN}, "Report", props={"value": 3},
           variants=[{"name": "golden", "props": {"value": 3}, "frame": 12},
                     {"name": "again", "props": {"value": 3}, "frame": 12},
                     {"name": "changed", "props": {"value": 4}, "frame": 12}],
           media={"out": str(out / "report.mp4"), "frameRange": [0, 9]})
    g, a, c = (img(out / f"variant-{n}.png") for n in ("golden", "again", "changed"))
    shutil.copy(out / "variant-golden.png", work / "golden.png")
    v = vstream(out / "report.mp4")
    return [
        ("golden frame shows value=3 bars", runs(mask(g, (255, 255, 255), 30)[25]) == 3, str(runs(mask(g, (255, 255, 255), 30)[25]))),
        ("re-render with same props matches the golden exactly", np.array_equal(g, a), "pixel-identical"),
        ("changed props (value=4) fail the golden", not np.array_equal(g, c) and runs(mask(c, (255, 255, 255), 30)[25]) == 4,
         f"bars={runs(mask(c, (255, 255, 255), 30)[25])}"),
        ("renderMedia SSR: 10 frames h264 at 30 fps",
         (int(v["nb_frames"]), v["codec_name"], v["r_frame_rate"]) == (10, "h264", "30/1"),
         f"{v['nb_frames']} {v['codec_name']} {v['r_frame_rate']} (local SSR only; Lambda not exercised)"),
    ]


# ---------------------------------------------------------------- ENG-X05 rule checklist (runnable topics)

RULES = PRE + """const C = ({seconds}) => { const frame = useCurrentFrame(); const {fps} = useVideoConfig();
  const s = spring({frame, fps, config: {damping: 200}});
  return <AbsoluteFill style={{background: "#000"}}>
    <div style={{position: "absolute", left: 0, top: 5, width: 10, height: 10, background: "#ff0000", translate: `${s * 100}px 0px`}}/>
    <Sequence from={10} durationInFrames={10}><div style={{position: "absolute", left: 0, top: 30, width: 20, height: 10, background: "#00ff00"}}/></Sequence>
  </AbsoluteFill>; };
""" + root("Rules", "C", 130, 45, 30, 1, 'defaultProps={{seconds: 1}} calculateMetadata={({props}) => ({durationInFrames: props.seconds * 30})}')

SRT = "1\n00:00:00,000 --> 00:00:01,500\nمرحبا بكم\n\n2\n00:00:01,500 --> 00:00:03,000\nفي كوسيف\n"


def tiktok_pages_reference(tokens, combine_ms):
    pages = []
    for t in tokens:
        if not pages or t["startMs"] - pages[-1][0]["startMs"] > combine_ms:
            pages.append([t])
        else:
            pages[-1].append(t)
    return [[x["text"].strip() for x in p] for p in pages]


def eng_x05(work: Path):
    res = render(work, "rules", {"index.jsx": RULES}, "Rules", props={"seconds": 2}, frames=[0, 30])
    out = work / "rules" / "out"
    fr = {int(re.findall(r"\d+", p.name)[0]): img(p) for p in out.glob("element-*.png")}
    clip = work / "clip.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=s=160x90:r=30:d=1",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(clip)], check=True)
    tokens = [{"text": (" " if i else "") + f"w{i}", "startMs": i * 400, "endMs": i * 400 + 400,
               "timestampMs": i * 400 + 200, "confidence": 1} for i in range(6)]
    code = f"""const c = require('@remotion/captions'); const r = require('remotion');
const R = require('@remotion/renderer');
(async () => {{
  const md = await R.getVideoMetadata({json.dumps(str(clip))}, {{logLevel: 'error'}});
  console.log(JSON.stringify({{ srt: c.parseSrt({{input: {json.dumps(SRT)}}}).captions,
    pages: c.createTikTokStyleCaptions({{captions: {json.dumps(tokens)}, combineTokensWithinMilliseconds: 1200}}).pages,
    spring8: r.spring({{frame: 8, fps: 30, config: {{damping: 200}}}}),
    meta: {{w: md.width, h: md.height, fps: md.fps, d: md.durationInSeconds}} }}));
}})().catch((e) => {{ console.error(e); process.exit(1); }});"""
    j = json.loads(node(code, work).strip().splitlines()[-1])
    (work / "checklist.json").write_text(json.dumps(j, ensure_ascii=False, indent=1), encoding="utf-8")
    seq_vis = {f: int(mask(fr[f], (0, 255, 0), 40).sum()) for f in (9, 10, 19, 20)}
    sx = {f: centroid_x(fr[f]) - 4.5 for f in (0, 8, 30)}
    pages = [[t["text"].strip() for t in p["tokens"]] for p in j["pages"]]
    lic = (NM / "remotion" / "LICENSE.md").read_text(encoding="utf-8")
    covered = ["compositions", "calculate-metadata", "sequencing", "trimming", "timing (spring)", "media helpers",
               "import SRT", "display captions", "licence"]
    return [
        ("calculate-metadata: seconds=2 -> 60 frames", res["composition"]["durationInFrames"] == 60, str(res["composition"]["durationInFrames"])),
        ("sequencing/trimming: Sequence from 10 for 10 frames visible only on 10..19",
         seq_vis[9] == 0 and seq_vis[10] > 0 and seq_vis[19] > 0 and seq_vis[20] == 0, str(seq_vis)),
        ("timing: spring(damping 200) starts at 0, settles at 1 by frame 30",
         abs(sx[0]) <= 0.2 and abs(sx[30] - 100) <= 0.5, f"{sx[0]:.2f} .. {sx[30]:.2f}"),
        ("timing: frame 8 position = spring() value", abs(sx[8] - 100 * j["spring8"]) <= 0.35, f"{sx[8]:.2f} vs {100 * j['spring8']:.2f}"),
        ("media helpers: getVideoMetadata reads 160x90 @30 fps, 1 s",
         (j["meta"]["w"], j["meta"]["h"], round(j["meta"]["fps"]), round(j["meta"]["d"], 2)) == (160, 90, 30, 1.0), str(j["meta"])),
        ("import SRT: 2 cues at 0-1500 and 1500-3000 ms",
         [(c["startMs"], c["endMs"]) for c in j["srt"]] == [(0, 1500), (1500, 3000)] and j["srt"][1]["text"] == "في كوسيف", str(j["srt"])[:160]),
        ("display captions: 1200 ms pages match the reference grouping",
         pages == tiktok_pages_reference(tokens, 1200), f"{pages}"),
        ("licence: company licence clause present", "Company License" in lic, "remotion/LICENSE.md"),
        ("checklist covers the runnable topics", len(covered) == 9,
         "covered: " + ", ".join(covered) + "; not run here: fonts, gifs, lottie, 3D, tailwind, measuring text, transcribe (packages not in the starter)"),
    ]


# ---------------------------------------------------------------- esbuild cards (ENG-309 / 276 / 225)

ES_TARGET = "es2020"
LOADERS = [".glb", ".gltf", ".hdr", ".png", ".jpg", ".jpeg", ".webp", ".wav", ".bin"]


def asset_bytes(ext: str) -> bytes:
    return (f"KOSIF-{ext}-".encode() + bytes(range(256)))[: 64 + len(ext)]


def data_url_bytes(u: str) -> bytes:
    """Decode a data: URL in either form esbuild emits (base64, or percent-encoded text)."""
    head, body = u.split(",", 1)
    return base64.b64decode(body) if head.endswith(";base64") else urllib.parse.unquote_to_bytes(body)


def run_classic(bundle: Path, cwd: Path, expr: str):
    """Run the bundle as a classic (non-module) script with a window object; return JSON of expr."""
    code = f"""const vm = require('vm'); const fs = require('fs');
const ctx = {{ window: {{}} }}; ctx.globalThis = ctx;
new vm.Script(fs.readFileSync({json.dumps(str(bundle))}, 'utf8')).runInNewContext(ctx);
console.log(JSON.stringify({expr}));"""
    return json.loads(node(code, cwd).strip().splitlines()[-1])


def scene_fixture(root: Path, with_assets=True):
    src = root / "src"
    src.mkdir(parents=True, exist_ok=True)
    imports, fields = [], []
    if with_assets:
        for i, ext in enumerate(LOADERS):
            (src / f"asset{i}{ext}").write_bytes(asset_bytes(ext))
            imports.append(f'import a{i} from "./asset{i}{ext}";')
            fields.append(f'"{ext}": a{i}')
    (src / "data.json").write_text(json.dumps({"fish": 7, "name": "koi"}))
    (src / "main.js").write_text("\n".join(imports) + """
import data from "./data.json";
const opts = {};
opts.speed ||= 1;
const cfg = { deep: { v: 3 } };
window.SCENE = { assets: {""" + ", ".join(fields) + """}, data, speed: opts.speed, deep: cfg?.deep?.v ?? 0 };
""")


def eng_309(work: Path):
    """esbuild --bundle --format=iife --minify --target=es2020 with dataurl loaders and a json loader."""
    scene_fixture(work)
    flags = ["src/main.js", "--bundle", "--format=iife", "--minify", f"--target={ES_TARGET}",
             *[f"--loader:{e}=dataurl" for e in LOADERS], "--loader:.json=json"]
    esbuild_cli([*flags, "--outfile=assets/main.bundle.js"], work)
    esbuild_cli([f for f in flags if f != "--minify"] + ["--outfile=assets/unminified.js"], work)
    js = (work / "assets" / "main.bundle.js").read_text()
    scene = run_classic(work / "assets" / "main.bundle.js", work, "ctx.window.SCENE")
    decoded_ok = all(data_url_bytes(scene["assets"][e]) == asset_bytes(e) for e in LOADERS)
    return [
        ("all 9 asset types embedded as data: URLs that decode to the source bytes",
         len(scene["assets"]) == 9 and decoded_ok, ", ".join(sorted(scene["assets"]))),
        ("json loader yields the object", scene["data"] == {"fish": 7, "name": "koi"}, str(scene["data"])),
        ("iife: no import/export left, runs as a classic script", not re.search(r"\bimport\s|\bexport\s", js) and js.startswith("(()=>"), js[:30]),
        ("target es2020 lowers ||= (ES2021) and keeps ?. / ??", "||=" not in js and "?." in js and "??" in js, f"||= present={'||=' in js}"),
        ("lowered code still behaves: speed=1, deep=3", (scene["speed"], scene["deep"]) == (1, 3), f"{scene['speed']} {scene['deep']}"),
        ("--minify shrinks the bundle", len(js) < len((work / "assets" / "unminified.js").read_text()),
         f"{len(js)} < {len((work / 'assets' / 'unminified.js').read_text())}"),
    ]


def motion_bundle(project: Path, entry="src/main.js", out="assets/main.bundle.js", global_name=None):
    """motion.py bundle PROJECT [--entry --out]: es2020, minified, iife, dataurl loaders."""
    args = [entry, "--bundle", "--format=iife", "--minify", f"--target={ES_TARGET}",
            *[f"--loader:{e}=dataurl" for e in LOADERS], f"--outfile={out}"]
    if global_name:
        args.append(f"--global-name={global_name}")
    esbuild_cli(args, project)
    return project / out


def eng_276(work: Path):
    proj = work / "projects" / "koi"
    scene_fixture(proj)
    default_out = motion_bundle(proj)
    (proj / "src" / "alt.js").write_text('import d from "./data.json"; window.ALT = d.fish * 2;')
    custom_out = motion_bundle(proj, entry="src/alt.js", out="build/alt.bundle.js")
    kit = work / "kit"
    kit.mkdir()
    (kit / "k3-entry.js").write_text("".join(f"export const e{i} = {i};\n" for i in range(5)) +
                                     "export const POST = { Bloom: class Bloom {} };\n")
    kit_out = motion_bundle(kit, entry="k3-entry.js", out="three-kit.bundle.js", global_name="K3")
    scene = run_classic(default_out, work, "ctx.window.SCENE.assets")
    alt = run_classic(custom_out, work, "ctx.window.ALT")
    k3 = run_classic(kit_out, work, "Object.keys(ctx.K3).sort()")
    js = default_out.read_text()
    return [
        ("default entry src/main.js -> assets/main.bundle.js", default_out.is_file(), str(default_out.relative_to(work))),
        ("--entry/--out honoured", custom_out.is_file() and alt == 14, f"{custom_out.relative_to(work)} ALT={alt}"),
        (".glb .gltf .hdr .png .jpg .jpeg .webp .wav .bin all dataurl-embedded",
         sorted(scene) == sorted(LOADERS) and all(data_url_bytes(scene[e]) == asset_bytes(e) for e in LOADERS),
         str(sorted(scene))),
        ("kit-bundle exposes window.K3 with its 6 exports incl. POST", k3 == ["POST", "e0", "e1", "e2", "e3", "e4"], str(k3)),
        ("es2020 + minified (no ||=, single line)", "||=" not in js and js.count("\n") <= 1, f"lines={js.count(chr(10))}"),
    ]


def eng_225(work: Path):
    proj = work / "projects" / "pond"
    src = proj / "src"
    src.mkdir(parents=True)
    # three@0.186.1 is not in the starter: a local ES-module kit stands in for three-kit.js
    (src / "three-kit.js").write_text("export class Node { constructor(n) { this.name = n; this.children = []; } add(c) { this.children.push(c); return this; } }\n"
                                      "export const makeFish = (i) => new Node('fish' + i);\n")
    (src / "data.json").write_text(json.dumps({"fish": 5}))
    Image.new("RGB", (4, 4), (10, 200, 30)).save(src / "tex.png")
    (src / "main.js").write_text('import { Node, makeFish } from "./three-kit.js";\nimport data from "./data.json";\n'
                                 'import tex from "./tex.png";\nconst scene = new Node("scene");\n'
                                 'for (let i = 0; i < data.fish; i++) scene.add(makeFish(i));\n'
                                 'window.SCENE = { count: scene.children.length, last: scene.children.at(-1).name, tex };\n')
    esbuild_cli(["src/main.js", "--bundle", "--format=iife", f"--target={ES_TARGET}", "--loader:.png=dataurl",
                 "--outfile=assets/main.bundle.js"], proj)
    js = (proj / "assets" / "main.bundle.js").read_text()
    (proj / "index.html").write_text('<!doctype html><script src="assets/main.bundle.js"></script>')
    scene = run_classic(proj / "assets" / "main.bundle.js", work, "ctx.window.SCENE")
    png = data_url_bytes(scene["tex"])
    return [
        ("ES-module imports bundled into one classic assets/main.bundle.js",
         not re.search(r"^\s*(import|export)\b", js, re.M) and "// src/three-kit.js" in js and "var makeFish" in js,
         "kit module inlined: " + str("// src/three-kit.js" in js)),
        ("classic script (no type=module) builds the scene: 5 fish", scene["count"] == 5 and scene["last"] == "fish4", str(scene["count"])),
        ("JSON data imported", scene["count"] == json.loads((src / "data.json").read_text())["fish"], "fish=5"),
        ("PNG data embedded byte-for-byte", png == (src / "tex.png").read_bytes(), f"{len(png)} bytes"),
        ("iife wrapper for file:// loading", js.lstrip().startswith(("(()", '"use strict";\n(()', "(function")), js[:20]),
    ]


PROGRAMS = {
    "ENG-312": eng_312,
    "ENG-317": eng_317,
    "ENG-313": eng_313,
    "ENG-430": eng_430,
    "ENG-314": eng_314,
    "ENG-130": eng_130,
    "ENG-163": eng_163,
    "ENG-124": eng_124,
    "ENG-350": eng_350,
    "ENG-323": eng_323,
    "ENG-X05": eng_x05,
    "ENG-309": eng_309,
    "ENG-276": eng_276,
    "ENG-225": eng_225,
}
