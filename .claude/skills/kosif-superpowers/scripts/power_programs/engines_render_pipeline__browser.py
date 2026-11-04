"""Wave-2 browser programs for engines-render-pipeline (ENG-*).

Each program writes a small page, runs it in Playwright Chromium through _browser_helper.cjs
(served at https://kosif.test/, every other http(s) request aborted), drives the card's technique
(the vendored MOTION shim, GSAP, the three-kit bundle, render(t) capture, WebGL, esbuild ...) and
checks known answers: exact element positions at t, pixel colours of sought footage, identical
frame hashes across orders and reloads, ffprobe of the encoded film. Nothing here touches the
network or spends credits.
"""
from __future__ import annotations

import json
import math
import re
import subprocess
import time
from pathlib import Path

import numpy as np
from PIL import Image

from ._browser_common import (CAIRO_LATIN_800, GSAP, K3_BUNDLE, KIT, MOTION_KIT, browser, decode_frames, ff,
                              gsap_page, img, near, page, probe, px, sha, vstream, astream)

SEG_COLOURS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255)]   # 4 x 0.25 s segments of the test clip


def make_clip(work: Path, name="clip.webm", size=(32, 18), seconds=1.0, fps=24) -> Path:
    """A VP8 all-intra clip whose colour changes every 0.25 s: red, green, blue, white."""
    out = work / name
    w, h = size
    parts = "".join(f"color=c=0x{r:02X}{g:02X}{b:02X}:s={w}x{h}:r={fps}:d={seconds / 4}[c{i}];"
                    for i, (r, g, b) in enumerate(SEG_COLOURS))
    ff("-filter_complex", parts + "[c0][c1][c2][c3]concat=n=4:v=1:a=0[v]", "-map", "[v]", "-c:v", "libvpx", "-g", "1",
       "-b:v", "400k", "-pix_fmt", "yuv420p", str(out))
    return out


def seg_colour(local_t: float):
    return SEG_COLOURS[min(3, int(local_t / 0.25))]


# ---------------------------------------------------------------- MOTION shim cards

SHIM_BODY = ('<div id="root" data-composition-id="root" data-width="64" data-height="36">'
             '<div id="box" style="position:absolute;left:0;top:28px;width:8px;height:8px;background:#fff"></div>'
             '<div id="css" style="position:absolute;left:0;top:20px;width:8px;height:8px;background:#f0f;animation:slide 2s linear forwards"></div>'
             '<video id="v" src="/clip.webm" data-start="1" data-duration="1" muted playsinline preload="auto" '
             'style="position:absolute;right:0;top:0;width:32px;height:18px"></video></div>')
SHIM_HEAD = "<style>@keyframes slide{from{left:0px}to{left:40px}}</style>"
SHIM_JS = ("const tl = gsap.timeline({paused:true}); tl.to('#box',{x:40,duration:2,ease:'none'});"
           "window.__timelines = window.__timelines || {}; window.__timelines['root'] = tl; MOTION.shim('root', 2);")

PROBE_JS = """(()=>{const v=document.getElementById('v');const a=document.getElementById('css').getAnimations()[0];
return {x:gsap.getProperty('#box','x'), css:a?a.currentTime:null, cssLeft:getComputedStyle(document.getElementById('css')).left,
vt:v.currentTime, vis:v.style.visibility||'visible', ready:window.__ready, dur:window.__duration, fonts:document.fonts.status}})()"""


def _shim_job(work, times, extra_init=(), shots=True):
    make_clip(work)
    page(work, "index.html", gsap_page(SHIM_BODY, SHIM_JS, head=SHIM_HEAD))
    steps = [{"op": "goto", "url": "/index.html"}, {"op": "wait", "js": "window.__ready===true"},
             {"op": "eval", "js": PROBE_JS, "as": "t0"}]
    for i, t in enumerate(times):
        steps += [{"op": "eval", "js": f"(window.render({t}), window.__ready)", "as": f"flag{i}"},
                  {"op": "wait", "js": "window.__ready===true"},
                  {"op": "eval", "js": PROBE_JS, "as": f"p{i}"}]
        if shots:
            steps.append({"op": "shot", "path": str(work / f"t{i}.png"), "selector": "#root"})
    return browser(work, {"steps": steps, "initScripts": list(extra_init)})


def eng_10(work: Path):
    """Render shim: render(t) seeks the GSAP timeline, CSS animation and <video data-start> clip to t."""
    times = [0.5, 1.6, 1.1]                     # 1.1 after 1.6: a backward seek must work too
    r = _shim_job(work, times)
    checks = [("__ready after fonts at load", r["values"]["t0"]["ready"] is True and r["values"]["t0"]["fonts"] == "loaded",
               str(r["values"]["t0"]))]
    for i, t in enumerate(times):
        p = r["values"][f"p{i}"]
        checks.append((f"GSAP x at t={t} is 20*t", abs(p["x"] - 20 * t) < 1e-6, f"x={p['x']}"))
        checks.append((f"CSS animation currentTime at t={t} is {t * 1000:.0f} ms", abs(p["css"] - t * 1000) < 1e-6, f"{p['css']}"))
        checks.append((f"render({t}) lowers __ready first", r["values"][f"flag{i}"] is False, str(r["values"][f"flag{i}"])))
        on = 1 <= t < 2
        checks.append((f"clip visible only in its span at t={t}", (p["vis"] != "hidden") == on, p["vis"]))
        if on:
            lt = t - 1
            checks.append((f"clip sought to {lt:.2f} s", abs(p["vt"] - lt) < 0.01, f"currentTime={p['vt']:.3f}"))
            c = px(work / f"t{i}.png", 48, 9)
            checks.append((f"footage pixel at t={t} is the segment colour", near(c, seg_colour(lt), 40), f"{c} vs {seg_colour(lt)}"))
        box = img(work / f"t{i}.png")
        cols = np.where(box[31, :, :].min(axis=1) > 200)[0]
        checks.append((f"white box drawn at x={20 * t:.0f}px", len(cols) and abs(int(cols.min()) - 20 * t) <= 1, f"cols={cols.tolist()[:3]}"))
    return checks


def eng_32(work: Path):
    """Dual-engine shim: the same file under HyperFrames (window.__hf: timelines only) and under KOSIF render(t)."""
    make_clip(work)
    page(work, "index.html", gsap_page(SHIM_BODY, SHIM_JS, head=SHIM_HEAD))
    t = 1.35
    kosif = browser(work, {"steps": [{"op": "goto", "url": "/index.html"}, {"op": "wait", "js": "window.__ready===true"},
                                     {"op": "eval", "js": f"window.render({t})"}, {"op": "wait", "js": "window.__ready===true"},
                                     {"op": "eval", "js": PROBE_JS, "as": "p"},
                                     {"op": "eval", "js": "typeof window.render", "as": "render"}]}, name="kosif")
    # HyperFrames' runtime sets window.__hf and seeks window.__timelines itself; the shim must not install render().
    hf = browser(work, {"initScripts": ["window.__hf = {runtime:'stand-in'};"],
                        "steps": [{"op": "goto", "url": "/index.html"}, {"op": "sleepFrames", "n": 3},
                                  {"op": "eval", "js": "typeof window.render", "as": "render"},
                                  {"op": "eval", "js": "Object.keys(window.__timelines||{})", "as": "tls"},
                                  {"op": "eval", "js": f"(window.__timelines.root.pause({t}), window.__kosifSeek({t}), true)"},
                                  {"op": "eval", "js": PROBE_JS, "as": "p"},
                                  {"op": "eval", "js": "!!document.getElementById('mk-player')", "as": "player"}]}, name="hf")
    kp, hp = kosif["values"]["p"], hf["values"]["p"]
    return [("KOSIF path exposes window.render", kosif["values"]["render"] == "function", kosif["values"]["render"]),
            ("HyperFrames path leaves render to the runtime", hf["values"]["render"] == "undefined", hf["values"]["render"]),
            ("timeline registered literally as __timelines['root']", hf["values"]["tls"] == ["root"], str(hf["values"]["tls"])),
            ("both engines put the box at x=20*t", abs(kp["x"] - 27.0) < 1e-6 and abs(hp["x"] - 27.0) < 1e-6, f"{kp['x']} / {hp['x']}"),
            ("both engines seek the CSS animation to t", abs(kp["css"] - 1350) < 1e-6 and abs(hp["css"] - 1350) < 1e-6, f"{kp['css']} / {hp['css']}"),
            ("KOSIF path seeks <video data-start> to t-start", abs(kp["vt"] - 0.35) < 0.01, f"{kp['vt']:.3f}"),
            ("no preview player under either renderer", hf["values"]["player"] is False, str(hf["values"]["player"]))]


READY_SPY = """(()=>{let v=false;window.__log=[];window.__seeked=0;window.__raf=0;
const raf=window.requestAnimationFrame.bind(window);window.requestAnimationFrame=(f)=>raf((ts)=>{window.__raf++;f(ts)});
document.addEventListener('seeked',()=>window.__seeked++,true);
Object.defineProperty(window,'__ready',{configurable:true,get(){return v},set(x){v=x;window.__log.push([x,window.__seeked,window.__raf])}});})();"""


def eng_274(work: Path):
    """Renderer shim + footage seeking: __ready flips only after every clip has sought and two animation frames."""
    make_clip(work)
    body = SHIM_BODY[:-len("</div>")] + ('<video id="v2" src="/clip.webm" data-start="0.5" data-duration="1" muted preload="auto" '
                                          'style="position:absolute;left:0;bottom:0;width:16px;height:9px"></video></div>')
    page(work, "index.html", gsap_page(body, SHIM_JS, head=SHIM_HEAD))
    r = browser(work, {"initScripts": [READY_SPY], "steps": [
        {"op": "goto", "url": "/index.html"}, {"op": "wait", "js": "window.__ready===true"},
        {"op": "eval", "js": "[window.__seeked, window.__raf, window.__log.length]", "as": "before"},
        {"op": "eval", "js": "window.render(1.2)"}, {"op": "wait", "js": "window.__ready===true"},
        {"op": "eval", "js": "window.__log", "as": "log"},
        {"op": "eval", "js": "[document.getElementById('v').currentTime, document.getElementById('v2').currentTime, window.__duration, typeof window.__kosifSeek, typeof window.seek]", "as": "state"}]})
    s0, r0, n0 = r["values"]["before"]
    log = r["values"]["log"][n0:]
    falses = [e for e in log if e[0] is False]
    trues = [e for e in log if e[0] is True]
    vt, vt2, dur, ks, sk = r["values"]["state"]
    return [("render(t) set __ready=false first", bool(falses) and log[0][0] is False, str(log)),
            ("__ready=true came after both clips sought", bool(trues) and trues[0][1] - s0 >= 2, f"seeked events {trues[0][1] - s0 if trues else None}"),
            ("__ready=true came at least two animation frames after render", bool(trues) and trues[0][2] - falses[0][2] >= 2,
             f"rAF ticks {trues[0][2] - falses[0][2] if trues and falses else None}"),
            ("clip 1 (start 1 s) sought to 0.2 s", abs(vt - 0.2) < 0.01, f"{vt:.3f}"),
            ("clip 2 (start 0.5 s) sought to 0.7 s", abs(vt2 - 0.7) < 0.01, f"{vt2:.3f}"),
            ("window.__duration, __kosifSeek and seek exposed", dur == 2 and ks == "function" and sk == "function", f"{dur} {ks} {sk}")]


def eng_284(work: Path):
    """Dual-renderer shim: MOTION.register helper, several timelines, and clip span edges."""
    make_clip(work)
    js = ("const tl = gsap.timeline({paused:true}); tl.to('#box',{x:40,duration:2,ease:'none'});"
          "const ov = gsap.timeline({paused:true}); ov.to('#css',{y:-10,duration:1,ease:'none'});"
          "window.__ret = MOTION.register('root', tl) === tl; MOTION.register('overlay', ov); MOTION.shim('root', 2);")
    page(work, "index.html", gsap_page(SHIM_BODY.replace("animation:slide 2s linear forwards", ""), js))
    steps = [{"op": "goto", "url": "/index.html"}, {"op": "wait", "js": "window.__ready===true"},
             {"op": "eval", "js": "[window.__ret, Object.keys(window.__timelines)]", "as": "reg"}]
    edges = [0.999, 1.0, 1.999, 2.0]
    for i, t in enumerate(edges):
        steps += [{"op": "eval", "js": f"window.render({t})"}, {"op": "wait", "js": "window.__ready===true"},
                  {"op": "eval", "js": "[document.getElementById('v').style.visibility||'visible', gsap.getProperty('#box','x'), gsap.getProperty('#css','y'), document.getElementById('v').currentTime]", "as": f"e{i}"}]
    r = browser(work, {"steps": steps})
    ret, keys = r["values"]["reg"]
    vis = [r["values"][f"e{i}"][0] for i in range(4)]
    e2 = r["values"]["e2"]
    return [("MOTION.register returns the timeline", ret is True, str(ret)),
            ("both timelines registered on window.__timelines", sorted(keys) == ["overlay", "root"], str(keys)),
            ("clip hidden just before data-start", vis[0] == "hidden", vis[0]),
            ("clip visible at data-start", vis[1] != "hidden", vis[1]),
            ("clip visible at the last instant of its span", vis[2] != "hidden", vis[2]),
            ("clip hidden at start+duration", vis[3] == "hidden", vis[3]),
            ("root timeline at 1.999 s: x=39.98", abs(e2[1] - 39.98) < 1e-6, str(e2[1])),
            ("overlay timeline clamps at its own end (y=-10)", abs(e2[2] + 10) < 1e-6, str(e2[2])),
            ("clip clamped to duration-1ms at span end", abs(e2[3] - 0.999) < 0.01, f"{e2[3]:.4f}")]


DET_BODY = '<div id="root"></div>'
DET_JS = ("const root=document.getElementById('root');const r=MOTION.rng(42);const dots=[];"
          "for(let i=0;i<12;i++){const d=document.createElement('div');d.style.cssText='position:absolute;width:3px;height:3px;background:#fff';"
          "root.appendChild(d);dots.push({d,x:r()*60,y:r()*32,vx:(r()-.5)*8,vy:(r()-.5)*6});}"
          "window.render=(t)=>{window.__ready=false;for(const p of dots){p.d.style.left=((p.x+p.vx*t)%64+64)%64+'px';"
          "p.d.style.top=((p.y+p.vy*t)%36+36)%36+'px';}requestAnimationFrame(()=>requestAnimationFrame(()=>{window.__ready=true}))};"
          "window.__duration=10;window.__firstRng=MOTION.rng(1)();window.render(0);")
TRAPS = ("window.__traps=0;const _r=Math.random,_n=Date.now;window.__arm=()=>{Math.random=()=>{window.__traps++;return _r()};"
         "Date.now=()=>{window.__traps++;return _n()};};")


def mulberry32(seed):
    a = seed & 0xFFFFFFFF or 1

    def nxt():
        nonlocal a
        a = (a + 0x6D2B79F5) & 0xFFFFFFFF
        t = a
        t = ((t ^ (t >> 15)) * (1 | t)) & 0xFFFFFFFF
        t = (t + (((t ^ (t >> 7)) * (61 | t)) & 0xFFFFFFFF)) & 0xFFFFFFFF ^ t
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return nxt


def _frame150(work, name, order):
    steps = [{"op": "goto", "url": "/index.html"}, {"op": "eval", "js": "window.__arm()"}]
    for t in order:
        steps += [{"op": "eval", "js": f"window.render({t})"}, {"op": "wait", "js": "window.__ready===true"}]
    steps += [{"op": "shot", "path": str(work / f"{name}.png"), "selector": "#root"},
              {"op": "eval", "js": "[window.__traps, window.__firstRng]", "as": "s"}]
    return browser(work, {"initScripts": [TRAPS], "steps": steps}, name=name)


def eng_388(work: Path):
    """Deterministic render(t): frame 150 at 5.00 s is identical whatever was rendered before, with MOTION.rng(seed)."""
    page(work, "index.html", gsap_page(DET_BODY, DET_JS))
    a = _frame150(work, "after_2s", [2.0, 150 / 30])
    b = _frame150(work, "after_9s", [9.0, 7.5, 150 / 30])
    c = _frame150(work, "cold", [150 / 30])
    h = {k: sha(work / f"{k}.png") for k in ("after_2s", "after_9s", "cold")}
    expect = mulberry32(1)()
    return [("frame 150 identical after t=2 and after t=9", h["after_2s"] == h["after_9s"], h["after_2s"][:12] + " " + h["after_9s"][:12]),
            ("frame 150 identical on a fresh page", h["cold"] == h["after_2s"], h["cold"][:12]),
            ("render(t) never read Math.random or Date.now", a["values"]["s"][0] == 0 and b["values"]["s"][0] == 0, str(a["values"]["s"][0])),
            ("MOTION.rng is mulberry32 (seed 1 first draw)", abs(a["values"]["s"][1] - expect) < 1e-12, f"{a['values']['s'][1]} vs {expect}"),
            ("frame has the 12 seeded dots", int((img(work / 'cold.png').max(axis=2) > 200).sum()) >= 9 * 6, "white px")]


# ---------------------------------------------------------------- preview player cards

PREVIEW_INIT = "Object.defineProperty(Navigator.prototype,'webdriver',{get:()=>false});"


def _preview_page(work, audio=True):
    sr = 16000
    t = np.arange(int(sr * 2)) / sr
    data = (0.2 * np.sin(2 * np.pi * 440 * t) * 32767).astype("<i2")
    import wave
    with wave.open(str(work / "tone.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(data.tobytes())
    body = SHIM_BODY.replace('<video id="v"', ('<audio id="a" src="/tone.wav" data-start="0" preload="auto"></audio>' if audio else "")
                             + '<video id="v"')
    make_clip(work)
    page(work, "index.html", gsap_page(body, SHIM_JS, head=SHIM_HEAD))


def eng_72(work: Path):
    """Self-playing preview: opened in an ordinary browser the composition plays, pauses and scrubs with audio in sync."""
    _preview_page(work)
    state = "[gsap.getProperty('#box','x'), document.getElementById('mk-t').textContent, document.getElementById('a').currentTime, document.getElementById('a').paused]"
    r = browser(work, {"initScripts": [PREVIEW_INIT], "launch": {"args": ["--autoplay-policy=no-user-gesture-required"]},
                       "context": {"viewport": {"width": 320, "height": 240}}, "steps": [
        {"op": "goto", "url": "/index.html"}, {"op": "wait", "js": "!!document.getElementById('mk-player')"},
        {"op": "eval", "js": state, "as": "s0"},
        {"op": "click", "selector": "#mk-pp"},
        {"op": "wait", "js": "parseFloat(document.getElementById('mk-t').textContent)>=0.6", "timeout": 5000},
        {"op": "click", "selector": "#mk-pp"}, {"op": "eval", "js": state, "as": "paused"},
        {"op": "eval", "js": "new Promise(r=>setTimeout(r,300))"}, {"op": "eval", "js": state, "as": "later"},
        {"op": "eval", "js": "(()=>{const s=document.getElementById('mk-scrub');s.value=750;s.dispatchEvent(new Event('input'));return true})()"},
        {"op": "eval", "js": state, "as": "scrub"},
        {"op": "shot", "path": str(work / "preview.png")}]})
    v = r["values"]
    x_p, lab_p, at_p, apaused = v["paused"]
    tp = float(lab_p.split("/")[0])
    return [("player starts at 0.00", v["s0"][1].startswith("0.00") and v["s0"][0] == 0, v["s0"][1]),
            ("play advanced the film in real time", tp >= 0.6, lab_p),
            ("composition follows the clock (x = 20*t)", abs(x_p - 20 * tp) < 0.6, f"x={x_p} t={tp}"),
            ("audio element played in sync (|audio - t| < 0.15 s)", abs(at_p - tp) < 0.15, f"audio={at_p:.3f} t={tp:.3f}"),
            ("pause stops the clock", v["later"][1] == lab_p and apaused is True, f"{lab_p} -> {v['later'][1]}"),
            ("scrub to 750/1000 shows t=1.50", v["scrub"][1].startswith("1.50") and abs(v["scrub"][0] - 30) < 1e-6, f"{v['scrub'][1]} x={v['scrub'][0]}"),
            ("scrub seeks the audio too", abs(v["scrub"][2] - 1.5) < 0.05, f"{v['scrub'][2]:.3f}")]


def eng_93(work: Path):
    """Preview player details: 48 px bar, #E7B65A play button, window-fit scale, space bar, hidden under renderers."""
    _preview_page(work, audio=False)
    vp = {"width": 400, "height": 300}
    q = ("(()=>{const b=document.getElementById('mk-player');const pp=document.getElementById('mk-pp');"
         "return {h:b.getBoundingClientRect().height,bg:getComputedStyle(pp).backgroundColor,tr:document.getElementById('root').style.transform}})()")
    r = browser(work, {"initScripts": [PREVIEW_INIT], "context": {"viewport": vp}, "steps": [
        {"op": "goto", "url": "/index.html"}, {"op": "wait", "js": "!!document.getElementById('mk-player')"},
        {"op": "eval", "js": q, "as": "bar"},
        {"op": "press", "key": "Space"}, {"op": "eval", "js": "document.getElementById('mk-pp').textContent", "as": "after1"},
        {"op": "press", "key": "Space"}, {"op": "eval", "js": "document.getElementById('mk-pp').textContent", "as": "after2"},
        {"op": "shot", "path": str(work / "bar.png")}]}, name="human")
    rend = browser(work, {"steps": [{"op": "goto", "url": "/index.html"}, {"op": "wait", "js": "window.__ready===true"},
                                    {"op": "eval", "js": "!!document.getElementById('mk-player')", "as": "p"}]}, name="webdriver")
    qs = browser(work, {"initScripts": [PREVIEW_INIT], "steps": [{"op": "goto", "url": "/index.html?render=1"},
                                                                 {"op": "wait", "js": "window.__ready===true"},
                                                                 {"op": "eval", "js": "!!document.getElementById('mk-player')", "as": "p"}]}, name="query")
    bar = r["values"]["bar"]
    s = min(vp["width"] / 64, (vp["height"] - 56) / 36)
    m = re.search(r"scale\(([\d.]+)\)", bar["tr"])
    c = px(work / "bar.png", 3, vp["height"] - 24)
    return [("bar is 48 px tall", bar["h"] == 48, str(bar["h"])),
            ("play button colour #E7B65A", bar["bg"] == "rgb(231, 182, 90)", bar["bg"]),
            ("composition scaled to the window (min(W, H-56) fit)", m is not None and abs(float(m.group(1)) - s) < 1e-6, f"{bar['tr']} expect {s}"),
            ("space bar plays then pauses", r["values"]["after1"] == "❚❚" and r["values"]["after2"] == "▶", f"{r['values']['after1']} {r['values']['after2']}"),
            ("bar background #14161a drawn", near(c, (0x14, 0x16, 0x1a), 6), str(c)),
            ("no player under navigator.webdriver", rend["values"]["p"] is False, str(rend["values"]["p"])),
            ("no player with ?render", qs["values"]["p"] is False, str(qs["values"]["p"]))]


def eng_116(work: Path):
    """GSAP quickTo (duration 0.4, power3) and matchMedia (desktop width, reduced motion)."""
    js = ("window.xTo = gsap.quickTo('#dot','x',{duration:0.4,ease:'power3'});"
          "window.cond = null; gsap.matchMedia().add({isDesktop:'(min-width:800px)', reduceMotion:'(prefers-reduced-motion: reduce)'},"
          " ctx => { const c = ctx.conditions; window.cond = {isDesktop:c.isDesktop, reduceMotion:c.reduceMotion};"
          " window.tw = gsap.to('#bar',{x:50, duration: c.reduceMotion ? 0 : 2}); });")
    page(work, "index.html", gsap_page('<div id="root"><div id="dot" style="width:4px;height:4px;background:#fff"></div>'
                                       '<div id="bar" style="width:4px;height:4px;background:#0f0"></div></div>', js, libs=("gsap",)))
    q = ("(()=>{xTo(100); const tw=gsap.getTweensOf('#dot')[0]; tw.pause(); tw.progress(0.5); const mid=gsap.getProperty('#dot','x');"
         "tw.progress(1); const end=gsap.getProperty('#dot','x'); return {dur:tw.duration(), mid, end, cond:window.cond, twd:window.tw?window.tw.duration():null}})()")
    a = browser(work, {"context": {"viewport": {"width": 1024, "height": 600}, "reducedMotion": "reduce"},
                       "steps": [{"op": "goto", "url": "/index.html"}, {"op": "eval", "js": q, "as": "q"}]}, name="desk_reduce")
    b = browser(work, {"context": {"viewport": {"width": 600, "height": 600}, "reducedMotion": "no-preference"},
                       "steps": [{"op": "goto", "url": "/index.html"}, {"op": "eval", "js": q, "as": "q"},
                                 {"op": "shot", "path": str(work / "mobile.png")}]}, name="mobile")
    c = browser(work, {"context": {"viewport": {"width": 1280, "height": 600}, "reducedMotion": "no-preference"},
                       "steps": [{"op": "goto", "url": "/index.html"}, {"op": "eval", "js": q, "as": "q"}]}, name="desk_full")
    qa, qb, qc = a["values"]["q"], b["values"]["q"], c["values"]["q"]
    power3_out_half = 1 - (1 - 0.5) ** 4
    return [("quickTo tween lasts 0.4 s", abs(qa["dur"] - 0.4) < 1e-9, str(qa["dur"])),
            ("power3 (out) at half time = 93.75 px of 100", abs(qa["mid"] - 100 * power3_out_half) < 1e-6, str(qa["mid"])),
            ("quickTo reaches its target", qa["end"] == 100, str(qa["end"])),
            ("1024 px + reduce: isDesktop and reduceMotion true", qa["cond"] == {"isDesktop": True, "reduceMotion": True}, str(qa["cond"])),
            ("reduced motion gives a 0 s tween", qa["twd"] == 0, str(qa["twd"])),
            ("600 px + no-preference: no condition matches, setup never runs", qb["cond"] is None and qb["twd"] is None, str(qb["cond"])),
            ("1280 px + no-preference: isDesktop only", qc["cond"] == {"isDesktop": True, "reduceMotion": False}, str(qc["cond"])),
            ("full motion keeps the 2 s tween", qc["twd"] == 2, str(qc["twd"]))]


# ---------------------------------------------------------------- three-kit bundle cards

K3_SCENE = """(()=>{const T=K3.THREE;const c=document.createElement('canvas');document.body.appendChild(c);
const r=K3.makeRenderer(c,64,36,{tone:'neutral',exposure:1});const s=new T.Scene();s.background=new T.Color(0x000000);
const cam=new T.OrthographicCamera(-32,32,18,-18,0.1,10);cam.position.z=5;
const m=new T.Mesh(new T.PlaneGeometry(20,20),new T.MeshBasicMaterial({color:0xff0000,toneMapped:false}));s.add(m);r.render(s,cam);
const gl=r.getContext();const p=new Uint8Array(4);gl.readPixels(32,18,1,1,gl.RGBA,gl.UNSIGNED_BYTE,p);const q=new Uint8Array(4);gl.readPixels(2,2,1,1,gl.RGBA,gl.UNSIGNED_BYTE,q);
return {centre:Array.from(p),corner:Array.from(q),exports:Object.keys(K3).length,rev:T.REVISION,post:Object.keys(K3.POST).sort(),buf:[gl.drawingBufferWidth,gl.drawingBufferHeight]}})()"""


def _file_page(work, name, scripts, js_after=""):
    tags = "".join(f'<script src="{Path(s).resolve().as_uri()}"></script>' for s in scripts)
    (work / name).write_text(f"<!doctype html><html><head><meta charset=utf-8></head><body style='margin:0'>{tags}"
                             f"<script>{js_after}</script></body></html>", encoding="utf-8")
    return (work / name).resolve().as_uri()


def eng_12(work: Path):
    """Pre-bundled 3D kit: one classic script gives window.K3 with 69 exports and three r186, from file:// with no npm."""
    url = _file_page(work, "k3.html", [K3_BUNDLE])
    r = browser(work, {"launch": {"args": ["--allow-file-access-from-files"]},
                       "steps": [{"op": "goto", "url": url}, {"op": "eval", "js": K3_SCENE, "as": "k"},
                                 {"op": "eval", "js": "location.protocol", "as": "proto"}]})
    k = r["values"]["k"]
    size = K3_BUNDLE.stat().st_size
    (work / "k3_report.json").write_text(json.dumps({"bytes": size, **k}, indent=1))
    return [("bundle is 904,567 bytes", size == 904567, str(size)),
            ("page loaded from file://", r["values"]["proto"] == "file:", r["values"]["proto"]),
            ("window.K3 has 69 exports", k["exports"] == 69, str(k["exports"])),
            ("three REVISION 186", k["rev"] == "186", k["rev"]),
            ("K3.makeRenderer drew the red plane at the centre", near(k["centre"][:3], (255, 0, 0), 3), str(k["centre"])),
            ("background stays black outside the plane", near(k["corner"][:3], (0, 0, 0), 3), str(k["corner"])),
            ("no page errors and no network", not r["pageErrors"] and not r["blocked"], str(r["pageErrors"][:1]))]


def eng_286(work: Path):
    """Prebuilt bundle + kits loaded after it: lab-kit extends window.K3; loaded alone it refuses."""
    lab = KIT / "lab-kit.js"
    ok_url = _file_page(work, "with_bundle.html", [K3_BUNDLE, lab])
    bad_url = _file_page(work, "lab_only.html", [lab])
    q = ("({lab:K3.LAB_VERSION, rabbit:typeof K3.makeRabbit, post:Object.keys(K3.POST).sort(), "
         "composer: new K3.POST.EffectComposer(new K3.THREE.WebGLRenderer({canvas:document.createElement('canvas')})).passes.length})")
    a = browser(work, {"steps": [{"op": "goto", "url": ok_url}, {"op": "eval", "js": q, "as": "k"}]}, name="ok")
    b = browser(work, {"steps": [{"op": "goto", "url": bad_url}, {"op": "eval", "js": "typeof window.K3", "as": "k3"}]}, name="bad")
    k = a["values"]["k"]
    return [("bundle size 904,567 bytes", K3_BUNDLE.stat().st_size == 904567, str(K3_BUNDLE.stat().st_size)),
            ("lab-kit extended K3 (LAB_VERSION 1, makeRabbit)", k["lab"] == 1 and k["rabbit"] == "function", str(k)),
            ("K3.POST carries the post classes", k["post"] == sorted(["BokehPass", "EffectComposer", "FilmPass", "OutputPass", "RenderPass", "ShaderPass", "UnrealBloomPass"]), str(k["post"])),
            ("an EffectComposer can be built from K3.POST", k["composer"] == 0, str(k["composer"])),
            ("lab-kit without the bundle throws its guard error", any("needs three-kit.bundle.js" in e for e in b["pageErrors"]), str(b["pageErrors"][:1])),
            ("no window.K3 without the bundle", b["values"]["k3"] == "undefined", b["values"]["k3"])]


def eng_287(work: Path):
    """Draft scale: with window.__draftScale the GL drawing buffer shrinks by that factor."""
    lab = KIT / "lab-kit.js"
    q = ("(()=>{const c=document.createElement('canvas');const r=K3.makeRenderer(c,320,180,{});const gl=r.getContext();"
         "const T=K3.THREE,s=new T.Scene(),cam=new T.PerspectiveCamera(50,16/9,.1,10);s.add(new T.Mesh(new T.TorusKnotGeometry(1,.3,200,32),new T.MeshNormalMaterial()));cam.position.z=4;"
         "const t0=performance.now();for(let i=0;i<20;i++)r.render(s,cam);gl.finish();"
         "return [gl.drawingBufferWidth, gl.drawingBufferHeight, c.width, c.height, performance.now()-t0]})()")
    res = {}
    for ds in (1, 0.5, 0.25):
        init = [] if ds == 1 else [f"window.__draftScale={ds};"]
        url = _file_page(work, f"draft_{ds}.html", [K3_BUNDLE, lab])
        res[ds] = browser(work, {"initScripts": init, "steps": [{"op": "goto", "url": url}, {"op": "eval", "js": q, "as": "b"}]},
                          name=f"draft_{ds}")["values"]["b"]
    (work / "draft.json").write_text(json.dumps({str(k): v for k, v in res.items()}))
    return [("full scale buffer 320x180", res[1][:2] == [320, 180], str(res[1][:2])),
            ("draft 0.5 buffer 160x90", res[0.5][:2] == [160, 90], str(res[0.5][:2])),
            ("draft 0.25 buffer 80x45", res[0.25][:2] == [80, 45], str(res[0.25][:2])),
            ("pixel count falls 16x at 0.25", res[1][0] * res[1][1] == 16 * res[0.25][0] * res[0.25][1], "")]


BLUR_JS = """(()=>{const T=K3.THREE;const W=64,H=16;const c=document.createElement('canvas');document.body.appendChild(c);
const r=new T.WebGLRenderer({canvas:c,preserveDrawingBuffer:true});r.setPixelRatio(1);r.setSize(W,H,false);
const s=new T.Scene();s.background=new T.Color(0);const cam=new T.OrthographicCamera(0,W,H,0,-1,1);
const sq=new T.Mesh(new T.PlaneGeometry(8,8),new T.MeshBasicMaterial({color:0xffffff}));sq.position.y=8;s.add(sq);
const composer=new K3.POST.EffectComposer(r);composer.addPass(new K3.POST.RenderPass(s,cam));composer.addPass(new K3.POST.OutputPass());
const post={composer,film:{uniforms:{time:{value:0}}}};
const render=K3.makeFrameLoop(r,post,W,H,(t)=>{sq.position.x=12+t*SPEED;});
const gl=r.getContext();const row=()=>{const p=new Uint8Array(W*4);gl.readPixels(0,8,W,1,gl.RGBA,gl.UNSIGNED_BYTE,p);return Array.from({length:W},(_,i)=>p[i*4]);};
const out={};window.__fps=30;window.__shutter=0.5;
window.__blur=1;render(0.1);out.sharp=row();
window.__blur=4;window.__stack=undefined;render(0.1);out.avg=row();
window.__stack='lighten';render(0.1);out.lighten=row();
out.native=window.__nativeBlur;return out;})()"""


def blur_profile(row, thr=8):
    a = np.array(row)
    on = np.where(a > thr)[0]
    return a, (int(on.min()), int(on.max())) if len(on) else (None, None)


def eng_285(work: Path):
    """GPU motion-blur / long-exposure loop: k=4 sub-frames over shutter 0.5 at 30 fps, average vs MaxEquation lighten."""
    speed = 240.0                    # px/s: sub-frame step = 0.5/30 * 1/4 * 240 = 1 px
    url = _file_page(work, "blur.html", [K3_BUNDLE])
    r = browser(work, {"steps": [{"op": "goto", "url": url}, {"op": "eval", "js": BLUR_JS.replace("SPEED", str(speed)), "as": "b"}]})
    b = r["values"]["b"]
    (work / "blur_rows.json").write_text(json.dumps(b))
    sharp, (s0, s1) = blur_profile(b["sharp"])
    avg, (a0, a1) = blur_profile(b["avg"])
    lig, (l0, l1) = blur_profile(b["lighten"])
    step = 0.5 / 30 / 4 * speed      # 1 px between sub-frames
    full = sharp.max()
    partial = [v for v in avg[a0:a1 + 1] if 0.1 * full < v < 0.9 * full]
    return [("sharp frame: square 8 px wide", s1 - s0 + 1 == 8, f"{s0}..{s1}"),
            ("page flagged native blur (__nativeBlur)", b["native"] is True, str(b["native"])),
            ("average stack smears 3 px wider (k-1 sub-frame steps)", (a1 - a0 + 1) - (s1 - s0 + 1) == round(3 * step), f"{a0}..{a1}"),
            ("average stack has partial-coverage ramps", len(partial) >= 4, f"ramp values {partial[:6]}"),
            ("lighten stack covers the same span", (l0, l1) == (a0, a1), f"{l0}..{l1}"),
            ("lighten keeps full brightness across the trail", int(lig[l0:l1 + 1].min()) >= full - 3, f"min {int(lig[l0:l1 + 1].min())} full {int(full)}")]


ONE_CLOCK_JS = """
window.build=(canvas,W,H)=>{const T=K3.THREE;const r=new T.WebGLRenderer({canvas,preserveDrawingBuffer:true});r.setPixelRatio(1);r.setSize(W,H,false);
const s=new T.Scene();s.background=new T.Color(0);const cam=new T.OrthographicCamera(0,W,H,0,-1,1);
const cube=new T.Mesh(new T.PlaneGeometry(6,6),new T.MeshBasicMaterial({color:0x00ff00}));cube.position.y=28;s.add(cube);
const tex=new T.Mesh(new T.PlaneGeometry(8,8),new T.MeshBasicMaterial({color:0xffffff}));tex.position.set(56,8,0);s.add(tex);
const ready=new Promise(res=>setTimeout(()=>{const c=document.createElement('canvas');c.width=c.height=4;const g=c.getContext('2d');g.fillStyle='#0000ff';g.fillRect(0,0,4,4);
 createImageBitmap(c).then(bm=>{const t=new T.Texture(bm);t.needsUpdate=true;tex.material.map=t;tex.material.needsUpdate=true;window.__texAt=performance.now();res();});},300));
return {render(t){cube.position.x=4+t*10;r.render(s,cam);},ready};};
const W=64,H=36,canvas=document.getElementById('gl');const three=build(canvas,W,H);
const tl=gsap.timeline({paused:true});tl.to('#cap',{x:40,duration:4,ease:'none'});
window.render=(t)=>{window.__ready=false;tl.seek(t);three.render(t);requestAnimationFrame(()=>requestAnimationFrame(()=>{window.__ready=true}));};
window.__t0=performance.now();
Promise.all([document.fonts.ready,three.ready]).then(()=>{window.render(0);});
"""


def eng_222(work: Path):
    """Three.js scene + DOM overlay on one clock: overlay sought first, then the 3D frame; frame 0 waits for textures."""
    body = ('<div id="root"><canvas id="gl" width="64" height="36" style="position:absolute;left:0;top:0"></canvas>'
            '<div id="cap" style="position:absolute;left:0;top:0;width:4px;height:4px;background:#f00"></div></div>')
    page(work, "index.html", gsap_page(body, ONE_CLOCK_JS, libs=("gsap", "k3")))
    steps = [{"op": "goto", "url": "/index.html"}, {"op": "wait", "js": "window.__ready===true"},
             {"op": "eval", "js": "[window.__texAt-window.__t0]", "as": "tex"},
             {"op": "shot", "path": str(work / "f0.png"), "selector": "#root"}]
    for t in (1.0, 2.5):
        steps += [{"op": "eval", "js": f"window.render({t})"}, {"op": "wait", "js": "window.__ready===true"},
                  {"op": "shot", "path": str(work / f"f{t}.png"), "selector": "#root"}]
    r = browser(work, {"steps": steps})
    checks = [("frame 0 waited for the async texture (>=300 ms)", r["values"]["tex"][0] >= 290, f"{r['values']['tex'][0]:.0f} ms"),
              ("textured quad shows the texture on frame 0", near(px(work / "f0.png", 56, 27), (0, 0, 255), 20), str(px(work / "f0.png", 56, 27)))]
    for t in (1.0, 2.5):
        im = img(work / f"f{t}.png")
        red = np.where((im[1, :, 0] > 200) & (im[1, :, 1] < 60))[0]
        green = np.where((im[8, :, 1] > 200) & (im[8, :, 0] < 60))[0]
        checks.append((f"overlay at x=10*t at t={t}", len(red) and abs(int(red.min()) - 10 * t) <= 1, f"{red.min() if len(red) else None}"))
        checks.append((f"3D quad centred at 4+10*t at t={t}", len(green) and abs((green.min() + green.max() + 1) / 2 - (4 + 10 * t)) <= 1,
                       f"{green.min() if len(green) else None}..{green.max() if len(green) else None}"))
    return checks



# ---------------------------------------------------------------- render(t) capture pipeline cards

def encode(frames_dir: Path, out: Path, fps, crf=18, preset="slow", pattern="f_%04d.png", extra=()):
    ff("-framerate", str(fps), "-i", str(frames_dir / pattern), "-c:v", "libx264", "-preset", preset, "-crf", str(crf),
       "-pix_fmt", "yuv420p", "-movflags", "+faststart", *extra, str(out))
    return out


def moov_first(path: Path) -> bool:
    data = path.read_bytes()[:4096]
    return 0 <= data.find(b"moov") < max(data.find(b"mdat"), 0) or (data.find(b"moov") >= 0 and data.find(b"mdat") < 0)


SQUARE_PAGE = """<!doctype html><html><head><meta charset=utf-8><style>html,body{margin:0;background:#000}
#stage{position:relative;width:WWpx;height:HHpx;background:#101010;overflow:hidden}
#sq{position:absolute;top:4px;left:0;width:6px;height:6px;background:#fff}</style></head><body><div id="stage"><div id="sq"></div></div>
<script>window.__duration=DUR;window.render=(t)=>{document.getElementById('sq').style.left=(t*SPEED).toFixed(3)+'px';
window.__ready=true;EXTRA};window.render(0);</script></body></html>"""


def square_page(work, name="index.html", w=96, h=54, dur=1.0, speed=60, extra="", dur_js=None):
    html = (SQUARE_PAGE.replace("WW", str(w)).replace("HH", str(h)).replace("SPEED", str(speed)).replace("EXTRA", extra)
            .replace("DUR", str(dur) if dur_js is None else dur_js))
    return page(work, name, html)


def square_x(png) -> int | None:
    a = img(png)
    cols = np.where(a[6, :, :].min(axis=1) > 200)[0]
    return int(cols.min()) if len(cols) else None


def eng_267(work: Path):
    """Headless frame capture: render(t) per frame time, exact viewport screenshots f_%04d.png, frames=round(dur*fps), --limit."""
    proj = {"width": 96, "height": 54, "duration": 1.0, "fps": 30}
    (work / "project.json").write_text(json.dumps(proj))
    square_page(work, extra="if(Math.abs(t-0.5)<1e-9) setTimeout(()=>{throw new Error('planted page error at t=0.5')});")
    n = round(proj["duration"] * proj["fps"])
    job = {"launch": {"args": ["--ignore-gpu-blocklist"]}, "context": {"viewport": {"width": proj["width"], "height": proj["height"]}, "deviceScaleFactor": 1},
           "steps": [{"op": "goto", "url": "/index.html"}, {"op": "wait", "js": "window.__ready===true"},
                     {"op": "frames", "count": n, "fps": proj["fps"], "dir": str(work / "frames"), "fast": True,
                      "waitJs": "window.__ready===true", "progressEvery": 30},
                     {"op": "eval", "js": "new Promise(r=>setTimeout(r,50))"}]}
    r = browser(work, job)
    lim = browser(work, dict(job, steps=[job["steps"][0], job["steps"][1], dict(job["steps"][2], count=min(n, 5), dir=str(work / "limit"))]), name="limit")
    files = sorted((work / "frames").glob("f_*.png"))
    sizes = {Image.open(f).size for f in files}
    xs = [square_x(f) for f in files]
    return [(f"frames = round(1.0 s * 30) = {n}", len(files) == n, str(len(files))),
            ("numbered f_0000.png .. f_0029.png", files[0].name == "f_0000.png" and files[-1].name == f"f_{n - 1:04d}.png", f"{files[0].name}..{files[-1].name}"),
            ("every PNG is exactly the project viewport (DSF 1)", sizes == {(96, 54)}, str(sizes)),
            ("frame i shows the square at 60*i/30 px", all(x == round(2 * i) for i, x in enumerate(xs)), str(xs[:6])),
            ("--limit 5 keeps 5 frames", len(list((work / "limit").glob("f_*.png"))) == 5, str(len(list((work / "limit").glob('*.png'))))),
            ("page errors logged", any("planted page error" in e for e in r["pageErrors"]), str(r["pageErrors"][:1])),
            ("progress logged every 30 frames", sum(1 for c in r["console"] if c["type"] == "progress") == n // 30, str([c["text"] for c in r["console"] if c["type"] == "progress"]))]


CAPTURE_PAGE = """<!doctype html><html><head><meta charset=utf-8><style>html,body{margin:0;background:#000}canvas{display:block}</style></head>
<body><canvas id="c" width="64" height="36"></canvas><script>
const capture=/[?&]capture=1/.test(location.search);const c=document.getElementById('c');
const gl=c.getContext('webgl',{preserveDrawingBuffer:true});window.__loopTicks=0;
window.render=(t)=>{const r=(t%1);gl.clearColor(r,0.25,1-r,1);gl.clear(gl.COLOR_BUFFER_BIT);
gl.enable(gl.SCISSOR_TEST);gl.scissor(Math.round(t*12)%64,10,6,6);gl.clearColor(1,1,1,1);gl.clear(gl.COLOR_BUFFER_BIT);gl.disable(gl.SCISSOR_TEST);};
if(!capture){c.style.width='100vw';const loop=(ts)=>{window.__loopTicks++;window.render(ts/1000);requestAnimationFrame(loop)};requestAnimationFrame(loop);}
document.fonts.ready.then(()=>{window.render(0);window.__ready=true;});</script></body></html>"""


def eng_268(work: Path):
    """Deterministic render(t) WebGL capture: ?capture=1 stops the rAF loop and scaling, --only stills, ffmpeg at 30 fps."""
    page(work, "index.html", CAPTURE_PAGE)
    fps = 30
    job = {"context": {"viewport": {"width": 64, "height": 36}, "deviceScaleFactor": 1},
           "steps": [{"op": "goto", "url": "/index.html?capture=1"}, {"op": "wait", "js": "window.__ready===true"},
                     {"op": "eval", "js": "new Promise(r=>setTimeout(()=>r([window.__loopTicks, getComputedStyle(document.getElementById('c')).width]),120))", "as": "cap"},
                     {"op": "frames", "count": fps, "fps": fps, "dir": str(work / "frames"), "fast": True, "readyFlag": False},
                     {"op": "frames", "times": [0.5, 3.5], "fps": fps, "indexFromTime": True, "pattern": "only_%04d.png", "dir": str(work / "only"), "fast": True, "readyFlag": False},
                     {"op": "eval", "js": "document.getElementById('c').toDataURL().length", "as": "data"}]}
    r = browser(work, job)
    live = browser(work, {"context": {"viewport": {"width": 128, "height": 72}}, "steps": [
        {"op": "goto", "url": "/index.html"}, {"op": "wait", "js": "window.__loopTicks>3"},
        {"op": "eval", "js": "getComputedStyle(document.getElementById('c')).width", "as": "w"}]}, name="live")
    mp4 = encode(work / "frames", work / "film.mp4", fps, crf=17)
    frames = decode_frames(mp4, 64, 36)
    still = img(work / "only" / "only_0015.png")
    f15 = frames[15].astype(np.int16)
    ticks, width = r["values"]["cap"]
    expect_r = round(0.5 * 255)
    return [("?capture=1: no rAF loop ran", ticks == 0, str(ticks)),
            ("?capture=1: canvas not scaled (64px)", width == "64px", width),
            ("without capture the loop runs and scales", live["values"]["w"] != "64px", live["values"]["w"]),
            ("--only 0.5,3.5 wrote frames 15 and 105", sorted(p.name for p in (work / "only").glob("*.png")) == ["only_0015.png", "only_0105.png"], str(sorted(p.name for p in (work / 'only').glob('*.png')))),
            ("still at 0.5 s: red channel = 0.5*255", abs(int(still[2, 2, 0]) - expect_r) <= 2, str(still[2, 2].tolist())),
            ("film frame 15 matches the 0.5 s still", float(np.abs(f15 - still).mean()) < 6, f"mean abs diff {float(np.abs(f15 - still).mean()):.2f}"),
            ("preserveDrawingBuffer keeps the frame readable", r["values"]["data"] > 200, str(r["values"]["data"])),
            ("film is 30 frames at 30 fps", len(frames) == 30 and vstream(mp4)["r_frame_rate"] == "30/1", f"{len(frames)} {vstream(mp4)['r_frame_rate']}")]


SVG_FONT_PAGE = """<!doctype html><html><head><meta charset=utf-8><style>
@font-face{font-family:Cairo;src:url(/lib/cairo-latin-800.woff2) format('woff2');font-weight:700;font-display:block}
html,body{margin:0;background:#000}</style></head><body>
<svg id="stage" width="96" height="54" viewBox="0 0 96 54"><rect width="96" height="54" fill="#0b1d3a"/>
<circle id="drop" cx="10" cy="27" r="5" fill="#4fc3f7"/><text id="cap" x="4" y="50" font-family="Cairo" font-weight="700" font-size="10" fill="#fff">Rain</text></svg>
<script>window.render=(t)=>{document.getElementById('drop').setAttribute('cx',(10+t*7).toFixed(3));window.__ready=true;};
document.fonts.load('700 54px Cairo').then(()=>{window.render(0);window.__ready=true;});</script></body></html>"""


def eng_272(work: Path):
    """SVG stage capture to MP4: wait for __ready, fonts.check('700 54px Cairo'), render(i/30) + #stage screenshots, 300 frames, CRF 18 slow."""
    page(work, "index.html", SVG_FONT_PAGE)
    n = 300
    r = browser(work, {"context": {"viewport": {"width": 96, "height": 54}}, "steps": [
        {"op": "goto", "url": "/index.html"}, {"op": "wait", "js": "window.__ready===true"},
        {"op": "eval", "js": "document.fonts.check('700 54px Cairo')", "as": "font"},
        {"op": "eval", "js": "document.fonts.check('700 54px NoSuchFontKosif')", "as": "nofont_check"},
        {"op": "frames", "count": n, "fps": 30, "dir": str(work / "frames"), "selector": "#stage", "fast": True, "waitJs": "window.__ready===true"}]}, timeout=90)
    mp4 = encode(work / "frames", work / "water.mp4", 30, crf=18, preset="slow")
    v = vstream(mp4)
    frames = decode_frames(mp4, 96, 54)
    def drop_x(f):
        blue = np.where((f[27, :, 2] > 180) & (f[27, :, 0] < 140))[0]
        return (blue.min() + blue.max()) / 2 if len(blue) else None
    x0, x299 = drop_x(frames[0]), drop_x(frames[299])
    return [("web font Cairo 700 really loaded", r["values"]["font"] is True, str(r["values"]["font"])),
            ("300 frames captured", len(list((work / "frames").glob("f_*.png"))) == n, str(len(list((work / 'frames').glob('*.png'))))),
            ("H.264 yuv420p, 300 frames, 10.0 s", v["codec_name"] == "h264" and v["pix_fmt"] == "yuv420p" and int(v["nb_frames"]) == n
             and abs(float(v["duration"]) - 10.0) < 0.05, f"{v['codec_name']} {v['pix_fmt']} {v['nb_frames']} {v['duration']}"),
            ("faststart: moov before mdat", moov_first(mp4), ""),
            ("drop at frame 0 at cx=10", x0 is not None and abs(x0 - 10) <= 1, str(x0)),
            ("drop at frame 299 at cx=10+7*299/30", x299 is not None and abs(x299 - (10 + 7 * 299 / 30)) <= 1.5, str(x299))]


def eng_280(work: Path):
    """capture --html --w --h --fps --dur --only 1,4,7 --selector #stage: true pixel size, spot times, element crop."""
    square_page(work, w=80, h=40, dur=8, speed=6)
    w, h, fps = 120, 90, 2
    r = browser(work, {"context": {"viewport": {"width": w, "height": h}, "deviceScaleFactor": 1}, "steps": [
        {"op": "goto", "url": "/index.html"}, {"op": "wait", "js": "window.__ready===true"},
        {"op": "frames", "times": [1, 4, 7], "fps": fps, "indexFromTime": True, "dir": str(work / "only"), "fast": True},
        {"op": "frames", "times": [1], "fps": fps, "indexFromTime": True, "dir": str(work / "stage"), "selector": "#stage", "fast": True},
        {"op": "frames", "count": 16, "fps": fps, "dir": str(work / "all"), "fast": True}]})
    only = sorted(p.name for p in (work / "only").glob("*.png"))
    xs = [square_x(work / "only" / n) for n in only]
    return [("--only 1,4,7 at 2 fps writes frames 2, 8, 14", only == ["f_0002.png", "f_0008.png", "f_0014.png"], str(only)),
            ("spot frames show the square at 6*t px", xs == [6, 24, 42], str(xs)),
            ("full-page frames are true pixel size 120x90", Image.open(work / "only" / only[0]).size == (w, h), str(Image.open(work / 'only' / only[0]).size)),
            ("--selector #stage crops to the element 80x40", Image.open(work / "stage" / "f_0002.png").size == (80, 40), str(Image.open(work / 'stage' / 'f_0002.png').size)),
            ("--fps 2 --dur 8 gives 16 frames", len(list((work / "all").glob("*.png"))) == 16, str(len(list((work / 'all').glob('*.png')))))]


def chromium_binary(work: Path) -> str:
    r = browser(work, {"steps": []}, name="exe")
    return r.get("executable") or ""


def eng_297(work: Path):
    """Page to one deterministic frame: wait for __ready, optional render(t), screenshot; fallback --screenshot --virtual-time-budget."""
    page(work, "index.html", CAPTURE_PAGE)
    r = browser(work, {"context": {"viewport": {"width": 64, "height": 36}}, "steps": [
        {"op": "goto", "url": "/index.html?capture=1"}, {"op": "wait", "js": "window.__ready===true"},
        {"op": "eval", "js": "window.__ready=false; window.render(2.5); window.__ready=true"},
        {"op": "shot", "path": str(work / "t2_5.png")},
        {"op": "eval", "js": "window.__ready=false; window.render(2.5); window.__ready=true"},
        {"op": "shot", "path": str(work / "t2_5_again.png")},
        {"op": "eval", "js": "window.render(0)"}, {"op": "shot", "path": str(work / "t0.png")}]})
    a, b = img(work / "t2_5.png"), img(work / "t0.png")
    exe = r.get("executable", "")
    checks = [("render(2.5) frame: red = 0.5*255", abs(int(a[2, 2, 0]) - 128) <= 2, str(a[2, 2].tolist())),
              ("render(2.5) square at x=round(2.5*12)%64=30", int(a[23, 30:36].min()) > 240 and int(a[23, 29, 1]) < 100 and int(a[23, 36, 1]) < 100, str(a[23, 28:38, 1].tolist())),
              ("same t gives a byte-identical PNG", sha(work / "t2_5.png") == sha(work / "t2_5_again.png"), ""),
              ("t=0 differs from t=2.5", sha(work / "t0.png") != sha(work / "t2_5.png"), "")]
    # fallback path: the browser's own --screenshot with a virtual-time budget (no seek)
    if exe and Path(exe).exists():
        (work / "plain.html").write_text("<html><body style='margin:0;background:#00ff00'></body></html>")
        out = work / "fallback.png"
        subprocess.run([exe, "--headless", "--no-sandbox", "--hide-scrollbars", "--window-size=64,36", "--virtual-time-budget=30000",
                        f"--screenshot={out}", (work / "plain.html").resolve().as_uri()], capture_output=True, timeout=30)
        ok = out.exists() and near(px(out, 5, 5), (0, 255, 0), 3)
        checks.append(("fallback --screenshot --virtual-time-budget=30000 made the frame", ok, str(px(out, 5, 5)) if out.exists() else "no file"))
    else:
        checks.append(("chromium executable located for the fallback path", False, exe))
    return checks


def capture_film(work: Path, url: str, fps: int, size, seconds=None, name="film", crf=17, preset="medium", init=()):
    """film.py animate: duration from window.__duration (fallback 4 s), render(t) or seek(t) per frame, ffmpeg encode."""
    w, h = size
    dur_js = f"{seconds}" if seconds else "(window.__duration||4)"
    rjs = "(t)=>(window.render?window.render(t):window.seek(t))"
    r = browser(work, {"initScripts": list(init), "context": {"viewport": {"width": w, "height": h}}, "steps": [
        {"op": "goto", "url": url}, {"op": "wait", "js": "window.__ready===true"},
        {"op": "eval", "js": "[window.__duration||null, typeof window.render, typeof window.seek]", "as": "c"},
        {"op": "frames", "durationJs": dur_js, "fps": fps, "dir": str(work / name), "fast": True, "renderJs": rjs,
         "waitJs": "window.__ready===true", "as": "f"}]}, name=name)
    mp4 = encode(work / name, work / f"{name}.mp4", fps, crf=crf, preset=preset)
    _, has_render, has_seek = r["values"]["c"]
    used = "render" if has_render == "function" else ("seek" if has_seek == "function" else "none")
    return mp4, r["values"]["f_seconds"], used, r


def eng_298(work: Path):
    """Seekable page renderer: __duration sets the length (fallback 4 s), render(t) or seek(t), default 1280x720 / 30 fps."""
    square_page(work, "with_dur.html", w=1280, h=720, dur=1.0, speed=300)
    square_page(work, "no_dur.html", w=1280, h=720, dur_js="undefined", speed=30)
    a, sa, ra, _ = capture_film(work, "/with_dur.html", 30, (1280, 720), name="with_dur")
    b, sb, rb, _ = capture_film(work, "/no_dur.html", 2, (1280, 720), name="no_dur")
    va, vb = vstream(a), vstream(b)
    fa = decode_frames(a, 1280, 720)
    sq = np.where(fa[15, 6, :, :].min(axis=1) > 200)[0]
    return [("__duration 1.0 s gives a 1.0 s film", abs(float(va["duration"]) - 1.0) < 0.05 and sa == 1.0, va["duration"]),
            ("no __duration falls back to 4 s", sb == 4.0 and abs(float(vb["duration"]) - 4.0) < 0.05, vb["duration"]),
            ("1280x720 at 30 fps", (va["width"], va["height"], va["r_frame_rate"]) == (1280, 720, "30/1"), f"{va['width']}x{va['height']} {va['r_frame_rate']}"),
            ("30 frames for 1 s", int(va["nb_frames"]) == 30, va["nb_frames"]),
            ("frame 15 shows render(0.5): square at 150 px", len(sq) and abs(int(sq.min()) - 150) <= 2, str(sq[:2].tolist())),
            ("drove render(t) on this page", ra == "render", ra)]


CONTRACT_PAGES = {
    "good.html": "window.__duration=2;window.render=(t)=>{document.body.dataset.x=(t*10).toFixed(4);window.__ready=true};window.render(0);",
    "wallclock.html": "window.__duration=2;const t0=performance.now();window.render=(t)=>{document.body.dataset.x=((performance.now()-t0)/100).toFixed(4);window.__ready=true};window.render(0);",
    "no_duration.html": "window.render=(t)=>{document.body.dataset.x=(t*10).toFixed(4);window.__ready=true};window.render(0);",
    "never_ready.html": "window.__duration=2;window.render=(t)=>{document.body.dataset.x=(t*10).toFixed(4)};",
    "seek_only.html": "window.__duration=2;window.seek=(t)=>{document.body.dataset.x=(t*10).toFixed(4);window.__ready=true};window.seek(0);",
}


def check_contracts(work: Path, names) -> dict:
    """The studio's page contract: __ready, render(t) or seek(t), __duration in seconds, frame = f(t) only."""
    steps = []
    for i, name in enumerate(names):
        steps += [{"op": "goto", "url": f"/{name}"},
                  {"op": "eval", "js": "new Promise(r=>{const t0=performance.now();const f=()=>window.__ready===true||performance.now()-t0>400?r(window.__ready===true):requestAnimationFrame(f);f()})", "as": f"ready{i}"},
                  {"op": "eval", "js": "[typeof window.render, typeof window.seek, window.__duration]", "as": f"api{i}"},
                  {"op": "eval", "js": "(async()=>{const go=window.render||window.seek;if(!go)return null;go(1);const a=document.body.dataset.x;await new Promise(r=>setTimeout(r,120));go(1);return [a,document.body.dataset.x]})()", "as": f"twice{i}"}]
    v = browser(work, {"steps": steps}, name="contracts")["values"]
    out = {}
    for i, name in enumerate(names):
        problems = []
        if not v[f"ready{i}"]:
            problems.append("never sets window.__ready")
        api = v[f"api{i}"]
        if api[0] != "function" and api[1] != "function":
            problems.append("no render(t)/seek(t)")
        if not isinstance(api[2], (int, float)) or api[2] <= 0:
            problems.append("no __duration")
        tw = v[f"twice{i}"]
        if tw is None or tw[0] != tw[1]:
            problems.append("frame depends on the wall clock")
        out[name] = problems
    return out


def eng_304(work: Path):
    """Seekable HTML page contract validator on five pages with known verdicts."""
    for n, js in CONTRACT_PAGES.items():
        page(work, n, f"<!doctype html><html><body><script>{js}</script></body></html>")
    got = check_contracts(work, list(CONTRACT_PAGES))
    (work / "contract_report.json").write_text(json.dumps(got, indent=1))
    return [("conforming page passes", got["good.html"] == [], str(got["good.html"])),
            ("seek(t)-only page passes", got["seek_only.html"] == [], str(got["seek_only.html"])),
            ("wall-clock animation caught", got["wallclock.html"] == ["frame depends on the wall clock"], str(got["wallclock.html"])),
            ("missing __duration caught", got["no_duration.html"] == ["no __duration"], str(got["no_duration.html"])),
            ("page that never sets __ready caught", "never sets window.__ready" in got["never_ready.html"], str(got["never_ready.html"]))]


SEEK_PAGE = """<!doctype html><html><head><meta charset=utf-8><style>html,body{margin:0;background:#000}#bar{position:absolute;left:0;top:0;height:8px;background:#fff}</style></head>
<body><div id="bar"></div><script>window.__duration=1;window.seek=(t)=>{document.getElementById('bar').style.width=Math.round(t*64)+'px';window.__ready=true;};window.seek(0);</script></body></html>"""


def eng_394(work: Path):
    """Route A: the program is the film. index.html window.seek(t), Playwright per frame, FFmpeg."""
    page(work, "index.html", SEEK_PAGE)
    mp4, secs, rjs, _ = capture_film(work, "/index.html", 24, (64, 36), name="routeA")
    fr = decode_frames(mp4, 64, 36)
    widths = [int((f[3, :, :].min(axis=1) > 180).sum()) for f in fr]
    expect = [round(i / 24 * 64) for i in range(24)]
    return [("driven through window.seek(t) (no render)", rjs == "seek", rjs),
            ("24 frames for __duration 1 s at 24 fps", len(fr) == 24, str(len(fr))),
            ("each frame's bar width = round(t*64)", max(abs(a - b) for a, b in zip(widths, expect)) <= 1, f"{widths[:6]} vs {expect[:6]}"),
            ("H.264 MP4", vstream(mp4)["codec_name"] == "h264", vstream(mp4)["codec_name"])]


RAND_PAGE = """<!doctype html><html><head><meta charset=utf-8><style>html,body{margin:0;background:#000}</style></head><body>
<canvas id="c" width="64" height="36"></canvas><script>
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
const R=mulberry32(SEED);const stars=Array.from({length:30},()=>({x:R()*64,y:R()*36,v:R()*20}));
const g=document.getElementById('c').getContext('2d');
window.render=(t)=>{g.fillStyle='#000';g.fillRect(0,0,64,36);g.fillStyle='#fff';for(const s of stars){g.fillRect(Math.floor((s.x+s.v*t)%64),Math.floor(s.y),1,1);}window.__ready=true;};
window.__duration=1;window.render(0);</script></body></html>"""


def eng_435(work: Path):
    """Pure function of time + seeded random: shuffled-order capture decodes identical to in-order capture; no rAF/CSS transitions."""
    page(work, "index.html", RAND_PAGE.replace("SEED", "7"))
    page(work, "other_seed.html", RAND_PAGE.replace("SEED", "8"))
    fps, n = 20, 20
    order = list(range(n))
    shuffled = order[::-1][:10] + order[:10]
    shuffled = sorted(set(shuffled), key=lambda i: (i * 7) % n)
    traps = "window.__rafCalls=0;const _raf=window.requestAnimationFrame;window.requestAnimationFrame=(f)=>{window.__rafCalls++;return _raf(f)};"
    r = browser(work, {"initScripts": [traps], "context": {"viewport": {"width": 64, "height": 36}}, "steps": [
        {"op": "goto", "url": "/index.html"}, {"op": "wait", "js": "window.__ready===true"},
        {"op": "frames", "times": [i / fps for i in order], "fps": fps, "indexFromTime": True, "dir": str(work / "inorder"), "fast": True},
        {"op": "frames", "times": [i / fps for i in shuffled], "fps": fps, "indexFromTime": True, "dir": str(work / "shuffled"), "fast": True},
        {"op": "eval", "js": "[window.__rafCalls, document.getAnimations().length]", "as": "s"}]})
    o = browser(work, {"context": {"viewport": {"width": 64, "height": 36}}, "steps": [
        {"op": "goto", "url": "/other_seed.html"}, {"op": "wait", "js": "window.__ready===true"},
        {"op": "frames", "times": [0.0], "fps": fps, "indexFromTime": True, "dir": str(work / "seed8"), "fast": True}]}, name="seed8")
    a = encode(work / "inorder", work / "inorder.mp4", fps, crf=17, preset="medium")
    b = encode(work / "shuffled", work / "shuffled.mp4", fps, crf=17, preset="medium")
    fa, fb = decode_frames(a, 64, 36), decode_frames(b, 64, 36)
    same_png = all(sha(work / "inorder" / f"f_{i:04d}.png") == sha(work / "shuffled" / f"f_{i:04d}.png") for i in order)
    return [("every frame PNG identical in shuffled order", same_png, ""),
            ("muxed films decode identical", fa.shape == fb.shape and bool((fa == fb).all()), f"{fa.shape} {fb.shape}"),
            ("no rAF used and no CSS/Web animations", r["values"]["s"] == [0, 0], str(r["values"]["s"])),
            ("a different seed gives a different frame 0", sha(work / "seed8" / "f_0000.png") != sha(work / "inorder" / "f_0000.png"), "")]


SHADER_PAGE = """<!doctype html><html><head><meta charset=utf-8><style>html,body{margin:0;background:#000}</style></head><body>
<canvas id="c" width="64" height="36"></canvas><script>
const c=document.getElementById('c');const gl=c.getContext('webgl',{preserveDrawingBuffer:true});
const vs=`attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}`;
const fs=`precision highp float;uniform float uTime;uniform vec2 uBall;void main(){vec2 q=gl_FragCoord.xy;float r=fract(uTime);
float d=length(q-uBall);gl_FragColor=d<3.0?vec4(1.,1.,1.,1.):vec4(r,0.2,0.4,1.);}`;
function sh(t,s){const o=gl.createShader(t);gl.shaderSource(o,s);gl.compileShader(o);return o}
const pr=gl.createProgram();gl.attachShader(pr,sh(gl.VERTEX_SHADER,vs));gl.attachShader(pr,sh(gl.FRAGMENT_SHADER,fs));gl.linkProgram(pr);gl.useProgram(pr);
const b=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,b);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,1,1]),gl.STATIC_DRAW);
const loc=gl.getAttribLocation(pr,'p');gl.enableVertexAttribArray(loc);gl.vertexAttribPointer(loc,2,gl.FLOAT,false,0,0);
const FPS=30;const uT=gl.getUniformLocation(pr,'uTime'),uB=gl.getUniformLocation(pr,'uBall');
function physics(frame){let y=33,v=0;const dt=1/FPS;for(let i=0;i<frame;i++){v-=60*dt;y+=v*dt;if(y<3){y=3;v=-v*0.6;}}return y;}
window.renderFrame=(frame)=>{const y=physics(frame);gl.uniform1f(uT,frame/FPS);gl.uniform2f(uB,32,y);gl.drawArrays(gl.TRIANGLE_STRIP,0,4);window.__ballY=y;window.__ready=true;};
window.render=(t)=>window.renderFrame(Math.round(t*FPS));window.renderFrame(0);</script></body></html>"""


def ball_y_expected(frame, fps=30):
    y, v, dt = 33.0, 0.0, 1 / fps
    for _ in range(frame):
        v -= 60 * dt
        y += v * dt
        if y < 3:
            y, v = 3.0, -v * 0.6
    return y


def eng_378(work: Path):
    """Deterministic time for offline render: uTime = frame/fps and fixed-dt physics, PNG sequence -> libx264 yuv420p."""
    page(work, "index.html", SHADER_PAGE)
    r = browser(work, {"context": {"viewport": {"width": 64, "height": 36}}, "steps": [
        {"op": "goto", "url": "/index.html"}, {"op": "wait", "js": "window.__ready===true"},
        {"op": "frames", "count": 30, "fps": 30, "dir": str(work / "frames"), "fast": True},
        {"op": "frames", "times": [15 / 30, 15 / 30], "fps": 30, "dir": str(work / "again"), "pattern": "a_%04d.png", "fast": True},
        {"op": "eval", "js": "(window.renderFrame(20), window.__ballY)", "as": "y20"}]})
    mp4 = encode(work / "frames", work / "film.mp4", 30, crf=17, preset="medium")
    f15 = img(work / "frames" / "f_0015.png")
    return [("uTime = 15/30 -> red = fract(0.5)*255", abs(int(f15[1, 1, 0]) - 128) <= 2, str(f15[1, 1].tolist())),
            ("re-rendering frame 15 is byte-identical", sha(work / "again" / "a_0000.png") == sha(work / "frames" / "f_0015.png")
             == sha(work / "again" / "a_0001.png"), ""),
            ("fixed-dt physics: ball y at frame 20 matches the reference integrator", abs(r["values"]["y20"] - ball_y_expected(20)) < 1e-9,
             f"{r['values']['y20']} vs {ball_y_expected(20)}"),
            ("ball drawn at the integrated height on frame 15",
             int(f15[36 - 1 - int(round(ball_y_expected(15))), 32, 1]) > 240, str(f15[36 - 1 - int(round(ball_y_expected(15))), 32].tolist())),
            ("libx264 yuv420p, 30 frames", vstream(mp4)["codec_name"] == "h264" and vstream(mp4)["pix_fmt"] == "yuv420p" and int(vstream(mp4)["nb_frames"]) == 30,
             f"{vstream(mp4)['pix_fmt']} {vstream(mp4)['nb_frames']}")]


FONT_PAGE = """<!doctype html><html><head><meta charset=utf-8>
<link rel="preload" href="/fonts/cairo.woff2" as="font" type="font/woff2" crossorigin>
<style>@import url('https://fonts.googleapis.com/css2?family=Cairo');
@font-face{font-family:KCairo;src:url(/fonts/cairo.woff2) format('woff2');font-weight:800;font-display:DISPLAY}
html,body{margin:0;background:#000;color:#fff}#t{font:800 40px KCairo, monospace;display:inline-block;white-space:nowrap}</style></head>
<body><span id="t">Wide Mmm</span><script>window.__w0=document.getElementById('t').getBoundingClientRect().width;
WAIT</script></body></html>"""


def eng_379(work: Path):
    """Web font loading for headless render: self-hosted woff2, font-display:block, preload, await document.fonts.ready."""
    (work / "fonts").mkdir()
    (work / "fonts" / "cairo.woff2").write_bytes(CAIRO_LATIN_800.read_bytes())
    ready = FONT_PAGE.replace("DISPLAY", "block").replace("WAIT", "document.fonts.ready.then(()=>{window.__w=document.getElementById('t').getBoundingClientRect().width;window.__ready=true;});")
    nowait = FONT_PAGE.replace("DISPLAY", "swap").replace("WAIT", "window.__w=document.getElementById('t').getBoundingClientRect().width;window.__ready=true;")
    page(work, "ready.html", ready)
    page(work, "nowait.html", nowait)
    q = "[window.__w, document.fonts.check('800 40px KCairo'), getComputedStyle(document.getElementById('t')).fontFamily]"
    delay = {"/fonts/cairo.woff2": 700}
    a = browser(work, {"delay": delay, "steps": [{"op": "goto", "url": "/ready.html", "waitUntil": "commit"}, {"op": "wait", "js": "window.__ready===true"},
                                                 {"op": "eval", "js": q, "as": "q"}, {"op": "shot", "path": str(work / "ready.png"), "selector": "#t"}]}, name="ready")
    b = browser(work, {"delay": delay, "steps": [{"op": "goto", "url": "/nowait.html", "waitUntil": "commit"}, {"op": "wait", "js": "window.__ready===true"},
                                                 {"op": "eval", "js": q, "as": "q"},
                                                 {"op": "eval", "js": "document.fonts.ready.then(()=>document.getElementById('t').getBoundingClientRect().width)", "as": "final"}]}, name="nowait")
    wa, fa, _ = a["values"]["q"]
    wb, _, _ = b["values"]["q"]
    final = b["values"]["final"]
    return [("after fonts.ready the face is loaded", fa is True, str(fa)),
            ("measured width after fonts.ready = final Cairo width", abs(wa - final) < 0.01, f"{wa:.2f} vs {final:.2f}"),
            ("capturing before the font arrives measures fallback glyphs", abs(wb - final) > 1, f"{wb:.2f} vs {final:.2f}"),
            ("Google Fonts @import was blocked (never relied on)", any("fonts.googleapis.com" in u for u in a["blocked"]), str(a["blocked"][:1])),
            ("self-hosted woff2 was served locally", any(q["url"].endswith("/fonts/cairo.woff2") and q["status"] == 200 for q in a["requests"]), "")]


CHART_PAGE = """<!doctype html><html><head><meta charset=utf-8><style>html,body{margin:0;background:#000}.b{position:absolute;bottom:0;width:10px;background:#fff}</style></head>
<body><div id="b0" class="b" style="left:2px"></div><div id="b1" class="b" style="left:20px"></div><div id="b2" class="b" style="left:38px"></div>
<script>const V=[30,12,24];const clamp=(x)=>Math.max(0,Math.min(1,x));const ease=(x)=>x*x*(3-2*x);
function interpolate(t,[t0,t1],[a,b]){return a+(b-a)*ease(clamp((t-t0)/(t1-t0)));}
window.seek=(t)=>{V.forEach((v,i)=>{document.getElementById('b'+i).style.height=interpolate(t,[i*0.5,i*0.5+1],[0,v]).toFixed(3)+'px';});window.__ready=true;};
window.seek(0);</script></body></html>"""


def chart_heights(t):
    out = []
    for i, v in enumerate([30, 12, 24]):
        x = max(0.0, min(1.0, (t - i * 0.5) / 1.0))
        out.append(round(v * x * x * (3 - 2 * x), 3))
    return out


def eng_382(work: Path):
    """Frame-driven chart clock: heights = interpolate(t) with clamp + easing; any order, no timers, nothing runs alone."""
    page(work, "index.html", CHART_PAGE)
    traps = "window.__timers=0;for(const k of ['setTimeout','setInterval','requestAnimationFrame']){const f=window[k].bind(window);window[k]=(...a)=>{window.__timers++;return f(...a)}};"
    hq = "[0,1,2].map(i=>parseFloat(document.getElementById('b'+i).style.height))"
    steps = [{"op": "goto", "url": "/index.html"}]
    for t in (2.5, 0.8, 1.25, 0.8, 9.0):
        steps += [{"op": "eval", "js": f"window.seek({t})"}, {"op": "eval", "js": hq, "as": f"h{t}"}]
    steps += [{"op": "eval", "js": "[window.__timers, document.getAnimations().length]", "as": "s"}]
    r = browser(work, {"initScripts": [traps], "steps": steps})
    v = r["values"]
    (work / "chart.json").write_text(json.dumps(v))
    return [("t=0.8 heights match interpolate+easing", v["h0.8"] == chart_heights(0.8), f"{v['h0.8']} vs {chart_heights(0.8)}"),
            ("t=1.25 heights match", v["h1.25"] == chart_heights(1.25), f"{v['h1.25']} vs {chart_heights(1.25)}"),
            ("seeking back to 0.8 after 1.25 gives the same frame", v["h0.8"] == chart_heights(0.8), ""),
            ("clamp: t=9 holds final values", v["h9.0"] == [30, 12, 24], str(v["h9.0"])),
            ("t=2.5 already complete", v["h2.5"] == [30, 12, 24], str(v["h2.5"])),
            ("no timers, rAF or animations used", v["s"] == [0, 0], str(v["s"]))]


OVERLAY_PAGE = """<!doctype html><html><head><meta charset=utf-8><script src="/lib/gsap.min.js"></script><script src="/lib/motion-kit.js"></script><style>html,body{margin:0;background:#000}
#root{position:relative;width:64px;height:36px;overflow:hidden}video{position:absolute;inset:0;width:64px;height:36px}
#title{position:absolute;left:4px;top:4px;width:30px;height:8px;background:#ffcc00;opacity:0;font:6px monospace;text-indent:14px;color:#000;overflow:hidden}
#logo{position:absolute;right:2px;bottom:2px;width:6px;height:6px;background:#000}</style></head><body>
<div id="root"><video id="v" src="/broll.webm" data-start="0" data-duration="1" muted preload="auto"></video><div id="title" aria-label="Brand title">BRAND</div><div id="logo"></div></div>
<script>const tl=gsap.timeline({paused:true});tl.to('#title',{opacity:1,duration:0.25,ease:'none'},0.25);
window.__timelines={root:tl};MOTION.shim('root',1);</script></body></html>"""


def eng_383(work: Path):
    """Programmatic overlays over AI-style footage: the clip is B-roll, title and logo are rendered in code on top."""
    make_clip(work, "broll.webm", size=(64, 36))
    page(work, "index.html", OVERLAY_PAGE)
    steps = [{"op": "goto", "url": "/index.html"}, {"op": "wait", "js": "window.__ready===true"}]
    for t in (0.1, 0.6):
        steps += [{"op": "eval", "js": f"window.render({t})"}, {"op": "wait", "js": "window.__ready===true"},
                  {"op": "shot", "path": str(work / f"c{t}.png"), "selector": "#root"}]
    steps.append({"op": "eval", "js": "document.getElementById('title').textContent", "as": "txt"})
    r = browser(work, {"context": {"viewport": {"width": 64, "height": 36}}, "steps": steps})
    a, b = img(work / "c0.1.png"), img(work / "c0.6.png")
    return [("at 0.1 s footage (red segment) shows under a hidden title", near(a[6, 6], (255, 0, 0), 40), str(a[6, 6].tolist())),
            ("at 0.6 s the code title (#ffcc00) covers the footage", near(b[6, 6], (255, 204, 0), 8), str(b[6, 6].tolist())),
            ("at 0.6 s footage is the blue segment around the title", near(b[25, 30], (0, 0, 255), 40), str(b[25, 30].tolist())),
            ("logo drawn in code on every frame", near(a[31, 59], (0, 0, 0), 10) and near(b[31, 59], (0, 0, 0), 10), f"{a[31, 59].tolist()} {b[31, 59].tolist()}"),
            ("title is live text in the DOM, not burnt into the clip", r["values"]["txt"] == "BRAND", r["values"]["txt"])]


DRAW_PAGE = """<!doctype html><html><head><meta charset=utf-8><script src="/lib/gsap.min.js"></script><style>html,body{margin:0;background:#000}</style></head><body>
<canvas id="c" width="64" height="36"></canvas><script>
const g=document.getElementById('c').getContext('2d');window.frames_=Array.from({length:30},(_,f)=>({x:f*2,c:f%2?'#ff0000':'#00ff00'}));
window.__drawn=[];function draw(fr){return ()=>{g.fillStyle='#000';g.fillRect(0,0,64,36);g.fillStyle=fr.c;g.fillRect(fr.x,10,4,4);window.__drawn.push(fr.x);};}
const fps=30;const tl=gsap.timeline({paused:true});for(let f=0;f<30;f++)tl.call(draw(window.frames_[f]),[],f/fps);
window.__traps=0;const _r=Math.random,_n=Date.now;window.render=(t)=>{Math.random=()=>{window.__traps++;return _r()};Date.now=()=>{window.__traps++;return _n()};
tl.seek(t,false);Math.random=_r;Date.now=_n;window.__ready=true;};window.__ac=typeof AudioContext;tl.seek(0,false);window.__ready=true;</script></body></html>"""


def eng_375(work: Path):
    """Deterministic sampling: for f<totalFrames tl.call(draw(frames[f]),[],f/fps); no Web Audio, Math.random or Date.now at render."""
    page(work, "index.html", DRAW_PAGE)
    r = browser(work, {"context": {"viewport": {"width": 64, "height": 36}}, "steps": [
        {"op": "goto", "url": "/index.html"}, {"op": "wait", "js": "window.__ready===true"},
        {"op": "frames", "times": [10 / 30, 17 / 30], "fps": 30, "indexFromTime": True, "dir": str(work / "frames"), "fast": True},
        {"op": "eval", "js": "[window.__traps, window.__drawn.slice(-1)[0], window.__drawn.length]", "as": "s"}]})
    f10, f17 = img(work / "frames" / "f_0010.png"), img(work / "frames" / "f_0017.png")
    traps, last, n = r["values"]["s"]
    return [("frame 10 draws frames[10] (green at x=20)", near(f10[11, 21], (0, 255, 0), 3) and int(f10[11, 18].max()) == 0, str(f10[11, 21].tolist())),
            ("frame 17 draws frames[17] (red at x=34)", near(f17[11, 35], (255, 0, 0), 3), str(f17[11, 35].tolist())),
            ("render never touched Math.random or Date.now", traps == 0, str(traps)),
            ("last sampled call is the frame asked for", last == 34, str(last))]

# ---------------------------------------------------------------- footage, HTML-in-canvas, stage, storage, adapters

def eng_112(work: Path):
    """Blob-URL seekable video: a host without byte ranges breaks seeking; fetch -> createObjectURL -> video.src restores it."""
    make_clip(work, "norange.webm", size=(32, 18))
    js = """(async(src)=>{const seekTo=(v,t)=>new Promise(r=>{const done=()=>r(v.currentTime);v.addEventListener('seeked',done,{once:true});v.currentTime=t;setTimeout(()=>r(v.currentTime),1500)});
const load=(v,s)=>new Promise(r=>{v.addEventListener('loadeddata',r,{once:true});v.src=s;v.load();});
const a=document.createElement('video');a.muted=true;document.body.appendChild(a);await load(a,src);
const aRanges=a.seekable.length?a.seekable.end(0):0;const aT=await seekTo(a,0.6);
const blob=await (await fetch(src)).blob();const url=URL.createObjectURL(blob);
const b=document.createElement('video');b.muted=true;document.body.appendChild(b);await load(b,url);
const bRanges=b.seekable.length?b.seekable.end(0):0;const bT=await seekTo(b,0.6);
await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(()=>setTimeout(r,60))));const cv=document.createElement('canvas');cv.width=32;cv.height=18;const g=cv.getContext('2d');g.drawImage(b,0,0);
return {aRanges,aT,bRanges,bT,url:url.slice(0,5),px:Array.from(g.getImageData(16,9,1,1).data),type:blob.type}})('/norange.webm')"""
    page(work, "index.html", "<!doctype html><html><body></body></html>")
    r = browser(work, {"noRange": ["/norange.webm"], "steps": [{"op": "goto", "url": "/index.html"}, {"op": "eval", "js": js, "as": "v"}]})
    v = r["values"]["v"]
    (work / "seek_report.json").write_text(json.dumps(v))
    return [("host without byte ranges: clip not seekable (seekable end 0)", v["aRanges"] == 0, str(v["aRanges"])),
            ("host without byte ranges: seek to 0.6 s fails", abs(v["aT"] - 0.6) > 0.05, f"{v['aT']:.3f}"),
            ("Blob URL clip is seekable to its 1 s end", abs(v["bRanges"] - 1.0) < 0.05, f"{v['bRanges']:.3f}"),
            ("Blob URL seek lands on 0.6 s", abs(v["bT"] - 0.6) < 0.02, f"{v['bT']:.3f}"),
            ("frame at 0.6 s is the blue segment", near(v["px"][:3], (0, 0, 255), 40), str(v["px"])),
            ("src is a blob: URL", v["url"] == "blob:", v["url"])]


HIC_FLAGS = ["--enable-features=CanvasDrawElement"]
HIC_PAGE = """<!doctype html><html><body style="margin:0;background:#000">
<canvas id="c" width="64" height="36" layoutsubtree><div id="ui" style="width:64px;height:36px;background:#ff0000;color:#fff;font:10px monospace">UI</div></canvas>
<canvas id="out" width="64" height="36"></canvas><script>
const c=document.getElementById('c'),g=c.getContext('2d'),o=document.getElementById('out').getContext('2d');
window.paint=(effect)=>{g.clearRect(0,0,64,36);g.drawElementImage(document.getElementById('ui'),0,0,64,36);
o.clearRect(0,0,64,36);o.filter=effect||'none';o.drawImage(c,0,0);o.filter='none';
return {src:Array.from(g.getImageData(40,30,1,1).data),out:Array.from(o.getImageData(40,30,1,1).data)}};
window.__api=typeof g.drawElementImage;requestAnimationFrame(()=>requestAnimationFrame(()=>{window.__ready=true}));</script></body></html>"""


def eng_125(work: Path):
    """HtmlInCanvas post-processing: DOM drawn into a canvas (drawElementImage, Chrome 149+ flag), then a Canvas2D effect."""
    page(work, "index.html", HIC_PAGE)
    r = browser(work, {"launch": {"args": HIC_FLAGS}, "steps": [
        {"op": "goto", "url": "/index.html"}, {"op": "wait", "js": "window.__ready===true"},
        {"op": "eval", "js": "window.paint('invert(1)')", "as": "inv"},
        {"op": "eval", "js": "(document.getElementById('ui').style.background='#0000ff', new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))))"},
        {"op": "eval", "js": "window.paint('grayscale(1)')", "as": "gray"}]}, name="flag")
    plain = browser(work, {"steps": [{"op": "goto", "url": "/index.html"}, {"op": "eval", "js": "window.__api", "as": "api"}]}, name="noflag")
    major = int(re.search(r"Chrome/(\d+)", r["userAgent"]).group(1))
    inv, gray = r["values"]["inv"], r["values"]["gray"]
    lum = round(0.2126 * 0 + 0.7152 * 0 + 0.0722 * 255)
    return [("Chromium is 149 or newer", major >= 149, str(major)),
            ("drawElementImage needs the flag (absent without it)", plain["values"]["api"] == "undefined", plain["values"]["api"]),
            ("live red DOM layer painted into the canvas", near(inv["src"][:3], (255, 0, 0), 2), str(inv["src"])),
            ("invert effect turns it cyan", near(inv["out"][:3], (0, 255, 255), 2), str(inv["out"])),
            ("an edited DOM layer repaints (now blue)", near(gray["src"][:3], (0, 0, 255), 2), str(gray["src"])),
            ("grayscale effect = Rec.709 luma of blue", near(gray["out"][:3], (lum, lum, lum), 3), f"{gray['out']} vs {lum}")]


SCREEN_PAGE = """<!doctype html><html><body style="margin:0;background:#000">
<canvas id="src" width="390" height="844" layoutsubtree><div id="ui" style="width:390px;height:844px;background:#00ff00"><h1 id="h">Hello</h1></div></canvas>
<canvas id="gl" width="64" height="64"></canvas><script src="/lib/three-kit.bundle.js"></script><script>
const T=K3.THREE,src=document.getElementById('src'),g=src.getContext('2d');
const r=new T.WebGLRenderer({canvas:document.getElementById('gl'),preserveDrawingBuffer:true});r.setPixelRatio(1);r.setSize(64,64,false);
const s=new T.Scene();s.background=new T.Color(0);const cam=new T.OrthographicCamera(-1,1,1,-1,0,2);cam.position.z=1;
const tex=new T.CanvasTexture(src);tex.colorSpace=T.SRGBColorSpace;
const screen=new T.Mesh(new T.PlaneGeometry(1,1.6),new T.MeshBasicMaterial({map:tex,toneMapped:false}));s.add(screen);
window.frame=()=>{if(typeof g.drawElementImage!=='function')return 'no-api';g.clearRect(0,0,390,844);g.drawElementImage(document.getElementById('ui'),0,0,390,844);tex.needsUpdate=true;r.render(s,cam);
const gl=r.getContext(),p=new Uint8Array(4);gl.readPixels(32,32,1,1,gl.RGBA,gl.UNSIGNED_BYTE,p);const q=new Uint8Array(4);gl.readPixels(2,32,1,1,gl.RGBA,gl.UNSIGNED_BYTE,q);return {mid:Array.from(p),edge:Array.from(q)}};
requestAnimationFrame(()=>requestAnimationFrame(()=>{window.__ready=true}));</script></body></html>"""


def eng_185(work: Path):
    """HTML-in-Canvas live screens: a 390x844 phone UI drawn into a canvas each frame and uploaded as a three.js texture."""
    page(work, "index.html", SCREEN_PAGE)
    r = browser(work, {"launch": {"args": HIC_FLAGS}, "steps": [
        {"op": "goto", "url": "/index.html"}, {"op": "wait", "js": "window.__ready===true"},
        {"op": "eval", "js": "window.frame()", "as": "f1"},
        {"op": "eval", "js": "(document.getElementById('ui').style.background='#ff00ff', new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))))"},
        {"op": "eval", "js": "window.frame()", "as": "f2"},
        {"op": "eval", "js": "[document.getElementById('src').width, document.getElementById('src').height]", "as": "buf"}]})
    no = browser(work, {"steps": [{"op": "goto", "url": "/index.html"}, {"op": "wait", "js": "window.__ready===true"},
                                  {"op": "eval", "js": "window.frame()", "as": "f"}]}, name="noflag")
    f1, f2 = r["values"]["f1"], r["values"]["f2"]
    return [("phone screen buffer 390x844", r["values"]["buf"] == [390, 844], str(r["values"]["buf"])),
            ("3D screen shows the live green UI", near(f1["mid"][:3], (0, 255, 0), 3), str(f1["mid"])),
            ("outside the screen mesh stays black", near(f1["edge"][:3], (0, 0, 0), 3), str(f1["edge"])),
            ("editing the HTML changes the next frame (magenta)", near(f2["mid"][:3], (255, 0, 255), 3), str(f2["mid"])),
            ("feature check: without the experimental API the page reports it", no["values"]["f"] == "no-api", str(no["values"]["f"]))]


STAGE_PAGE = """<!doctype html><html><head><meta charset=utf-8><style>html,body{margin:0;background:#000}
.stage{position:relative;isolation:isolate;overflow:hidden;width:64px;height:36px;background:#202060}
.shader{position:absolute;inset:0;z-index:0;pointer-events:none;width:64px;height:36px}
.ui{position:relative;z-index:1;margin:10px 0 0 10px;width:20px;height:10px;background:#fff}</style></head><body>
<div class="stage"><canvas class="shader" id="sh"></canvas><button class="ui" id="btn"></button></div><script>
const cv=document.getElementById('sh');const DPR=Math.min(window.devicePixelRatio||1,2);cv.width=64*DPR;cv.height=36*DPR;window.__dpr=DPR;
const gl=NOGL?null:cv.getContext('webgl');
if(gl){gl.clearColor(1,0.5,0,1);gl.clear(gl.COLOR_BUFFER_BIT);}else{cv.style.display='none';}
window.__ready=true;</script></body></html>"""


def eng_128(work: Path):
    """Shader-backed stage: GPU layer under crisp DOM UI, static CSS fallback beneath, DPR capped at 2, shader ignores pointer."""
    page(work, "gpu.html", STAGE_PAGE.replace("NOGL", "false"))
    page(work, "fallback.html", STAGE_PAGE.replace("NOGL", "true"))
    q = "[document.elementFromPoint(15,12).id, window.__dpr, document.getElementById('sh').width]"
    a = browser(work, {"context": {"viewport": {"width": 64, "height": 36}, "deviceScaleFactor": 3}, "steps": [
        {"op": "goto", "url": "/gpu.html"}, {"op": "eval", "js": q, "as": "q"},
        {"op": "eval", "js": "document.elementFromPoint(50,30).tagName", "as": "under"},
        {"op": "shot", "path": str(work / "gpu.png")}]}, name="gpu")
    b = browser(work, {"context": {"viewport": {"width": 64, "height": 36}}, "steps": [
        {"op": "goto", "url": "/fallback.html"}, {"op": "shot", "path": str(work / "fallback.png")}]}, name="fb")
    g = np.asarray(Image.open(work / "gpu.png").convert("RGB").resize((64, 36), Image.NEAREST)).astype(int)
    f = img(work / "fallback.png")
    return [("UI button sits above the shader layer", a["values"]["q"][0] == "btn", str(a["values"]["q"][0])),
            ("shader takes no pointer events (stage receives them)", a["values"]["under"] == "DIV", a["values"]["under"]),
            ("DPR 3 is capped at 2 (canvas 128 px wide)", a["values"]["q"][1] == 2 and a["values"]["q"][2] == 128, str(a["values"]["q"][1:])),
            ("GPU layer visible around the UI (orange)", near(g[30, 50], (255, 128, 0), 6), str(g[30, 50].tolist())),
            ("UI drawn crisp on top (white)", near(g[14, 15], (255, 255, 255), 30), str(g[14, 15].tolist())),
            ("without WebGL the static CSS background shows", near(f[30, 50], (0x20, 0x20, 0x60), 4), str(f[30, 50].tolist()))]


VLIB_PAGE = """<!doctype html><html><body><a id="dl"></a><script>
const VLIB={db:null,open(){return new Promise((res,rej)=>{const q=indexedDB.open('basma-videos',1);q.onupgradeneeded=()=>q.result.createObjectStore('videos',{keyPath:'id',autoIncrement:true});q.onsuccess=()=>{this.db=q.result;res()};q.onerror=rej;})},
 tx(m){return this.db.transaction('videos',m).objectStore('videos')},
 async add(blob,meta){const c=document.createElement('canvas');c.width=16;c.height=9;const g=c.getContext('2d');g.fillStyle=meta.colour||'#888';g.fillRect(0,0,16,9);
  const ext=blob.type.includes('webm')?'.webm':'.mp4';const rec={title:meta.title,size:blob.size,cost:meta.cost,thumb:c.toDataURL(),name:meta.title+ext,blob,at:meta.at};
  await new Promise(r=>{const q=this.tx('readwrite').add(rec);q.onsuccess=r});const all=await this.list();
  for(const old of all.slice(30)) await new Promise(r=>{const q=this.tx('readwrite').delete(old.id);q.onsuccess=r});},
 list(){return new Promise(r=>{const q=this.tx('readonly').getAll();q.onsuccess=()=>r(q.result.sort((a,b)=>b.at-a.at))})},
 async download(id){const rec=(await this.list()).find(x=>x.id===id);const a=document.getElementById('dl');a.href=URL.createObjectURL(rec.blob);a.download=rec.name;a.textContent='dl';}};
window.VLIB=VLIB;VLIB.open().then(()=>{window.__ready=true});</script></body></html>"""


def eng_161(work: Path):
    """Local video library in IndexedDB 'basma-videos': title, size, cost, thumbnail; last 30 kept; WebM keeps .webm."""
    page(work, "index.html", VLIB_PAGE)
    add = ("(async()=>{for(let i=1;i<=32;i++){const type=i%2?'video/webm':'video/mp4';"
           "await VLIB.add(new Blob([new Uint8Array(100+i)],{type}),{title:'film'+i,cost:i*0.5,at:i});}return true})()")
    q = "(async()=>{const l=await VLIB.list();return l.map(x=>[x.title,x.size,x.cost,x.name,x.thumb.slice(0,22)])})()"
    dl = work / "dl"
    dl.mkdir()
    r = browser(work, {"steps": [
        {"op": "goto", "url": "/index.html"}, {"op": "wait", "js": "window.__ready===true"}, {"op": "eval", "js": add},
        {"op": "reload"}, {"op": "wait", "js": "window.__ready===true"}, {"op": "eval", "js": q, "as": "lib"},
        {"op": "eval", "js": "(async()=>{const l=await VLIB.list();await VLIB.download(l[0].id);return l[0].name})()", "as": "first"},
        {"op": "download", "selector": "#dl", "dir": str(dl), "as": "file"}]})
    lib = r["values"]["lib"]
    titles = [x[0] for x in lib]
    return [("only the last 30 renders kept", len(lib) == 30, str(len(lib))),
            ("newest first: film32 .. film3", titles[0] == "film32" and titles[-1] == "film3", f"{titles[0]}..{titles[-1]}"),
            ("survives a reload (IndexedDB)", len(lib) == 30, ""),
            ("size and cost recorded", lib[0][1] == 132 and lib[0][2] == 16.0, str(lib[0][1:3])),
            ("thumbnail stored as PNG data URL", all(x[4] == "data:image/png;base64," for x in lib), lib[0][4]),
            ("WebM keeps .webm, MP4 keeps .mp4", lib[1][3] == "film31.webm" and lib[0][3] == "film32.mp4", f"{lib[0][3]} {lib[1][3]}"),
            ("download saves the stored blob under its name", r["values"]["file"]["name"] == "film32.mp4" and r["values"]["file"]["bytes"] == 132,
             str(r["values"]["file"]))]


ADAPTER_PAGE = """<!doctype html><html><head><script src="/lib/gsap.min.js"></script>
<style>@keyframes mv{from{left:0px}to{left:60px}}#c{position:absolute;left:0;animation:mv 2s linear paused both}</style></head><body>
<div id="g"></div><div id="c"></div><div id="w"></div><canvas id="k" width="8" height="8"></canvas><script>
const fps=30;const adapters={
gsap:{init(){this.tl=gsap.timeline({paused:true}).to('#g',{x:60,duration:2,ease:'none'})},seekFrame(f){this.tl.seek(f/fps,false)},read(){return gsap.getProperty('#g','x')},destroy(){this.tl.kill();this.tl=null}},
css:{init(){this.a=document.getElementById('c').getAnimations()[0];this.a.pause()},seekFrame(f){this.a.currentTime=f/fps*1000},read(){return parseFloat(getComputedStyle(document.getElementById('c')).left)},destroy(){this.a.cancel()}},
waapi:{init(){this.a=document.getElementById('w').animate([{opacity:0},{opacity:1}],{duration:2000,fill:'both'});this.a.pause()},seekFrame(f){this.a.currentTime=f/fps*1000},read(){return parseFloat(getComputedStyle(document.getElementById('w')).opacity)*60},destroy(){this.a.cancel()}},
custom:{init(){this.g=document.getElementById('k').getContext('2d')},seekFrame(f){this.v=f/fps*30;this.g.fillStyle='rgb('+Math.round(this.v*4)+',0,0)';this.g.fillRect(0,0,8,8)},read(){return this.g.getImageData(1,1,1,1).data[0]/4},destroy(){this.g=null}}};
window.run=(order)=>{const out={};for(const[k,a]of Object.entries(adapters)){a.init();out[k]=order.map(f=>{a.seekFrame(f);return Math.round(a.read()*1000)/1000});a.destroy();}return out};
window.__ready=true;</script></body></html>"""


def eng_170(work: Path):
    """Frame adapters (GSAP, CSS, WAAPI, custom canvas host) with init/seekFrame/destroy; random and backward seeks."""
    page(work, "index.html", ADAPTER_PAGE)
    order = [45, 3, 29, 3, 60, 0, 59]
    r = browser(work, {"steps": [{"op": "goto", "url": "/index.html"}, {"op": "wait", "js": "window.__ready===true"},
                                 {"op": "eval", "js": f"window.run({order})", "as": "o"},
                                 {"op": "eval", "js": "[document.getElementById('c').getAnimations().length, document.getElementById('w').getAnimations().length]", "as": "left"}]})
    o = r["values"]["o"]
    exp = [round(60 * min(f, 60) / 60, 3) for f in order]
    exp_custom = [round(round(f / 30 * 30 * 4) / 4, 3) for f in order]
    return [("GSAP adapter: x(frame) = frame px in any order", o["gsap"] == exp, f"{o['gsap']} vs {exp}"),
            ("CSS adapter matches after backward seeks", o["css"] == exp, str(o["css"])),
            ("WAAPI adapter matches", max(abs(a - b) for a, b in zip(o["waapi"], exp)) < 0.01, str(o["waapi"])),
            ("custom host adapter (canvas) matches", o["custom"] == exp_custom, f"{o['custom']} vs {exp_custom}"),
            ("frame 3 identical both times it was sought", all(v[1] == v[3] for v in o.values()), ""),
            ("destroy() released the CSS/WAAPI animations", r["values"]["left"] == [0, 0], str(r["values"]["left"]))]


PERF_LINT_JS = """(()=>{const LAYOUT=['left','top','right','bottom','width','height','margin','padding','margin-left','margin-top','padding-left','font-size'];const issues=[];
for(const sh of document.styleSheets){for(const r of sh.cssRules){
 if(r.type===CSSRule.KEYFRAMES_RULE){for(const k of r.cssRules){for(let i=0;i<k.style.length;i++){const p=k.style[i];if(LAYOUT.some(l=>p===l||p.startsWith(l+'-')))issues.push('layout:'+r.name+':'+p);}}}
 if(r.type===CSSRule.STYLE_RULE){const tp=r.style.transitionProperty;if(tp&&tp.split(',').map(s=>s.trim()).includes('all'))issues.push('transition-all:'+r.selectorText);
  if(r.style.willChange&&r.style.willChange!=='auto')issues.push('will-change:'+r.selectorText);}}}
const blurAnims=document.getAnimations().filter(a=>a.effect&&a.effect.getKeyframes().some(k=>k.filter&&/blur/.test(k.filter)));
if(blurAnims.length>3)issues.push('animated-blur-nodes:'+blurAnims.length);
const engines={};for(const a of document.getAnimations()){const t=a.effect.target;for(const k of a.effect.getKeyframes())for(const p of Object.keys(k)){if(['offset','easing','composite','computedOffset'].includes(p))continue;const key=(t.id||t.className)+'.'+p;engines[key]=(engines[key]||0)+1;}}
for(const[k,n]of Object.entries(engines))if(n>2)issues.push('one-engine-per-property:'+k);
const dpr=(full)=>Math.min(window.devicePixelRatio,full?1.25:2);return {issues:issues.sort(),dpr:dpr(false),dprShader:dpr(true)}})()"""


def eng_361(work: Path):
    """Web-motion performance rules as a lint run on the live page; DPR caps 2 and 1.25 for full-bleed shaders."""
    bad = ("<style>@keyframes slideL{from{left:0}to{left:100px}}@keyframes ok{from{transform:translateX(0);opacity:0}to{transform:translateX(9px);opacity:1}}"
           "@keyframes fog{from{filter:blur(0px)}to{filter:blur(8px)}}.card{transition:all .3s}.hero{will-change:transform}"
           ".b{animation:fog 1s infinite}.m{animation:slideL 1s infinite}</style>"
           "<div class='m'></div>" + "".join("<div class='b'></div>" for _ in range(5)) + "<div class='card'></div><div class='hero'></div>")
    good = ("<style>@keyframes ok{from{transform:translateX(0);opacity:0}to{transform:translateX(9px);opacity:1}}"
            ".card{transition:transform .3s, opacity .3s}.x{animation:ok 1s infinite}</style><div class='x'></div><div class='card'></div>")
    page(work, "bad.html", f"<!doctype html><html><head></head><body>{bad}</body></html>")
    page(work, "good.html", f"<!doctype html><html><head></head><body>{good}</body></html>")
    a = browser(work, {"context": {"deviceScaleFactor": 3}, "steps": [{"op": "goto", "url": "/bad.html"}, {"op": "eval", "js": PERF_LINT_JS, "as": "l"}]}, name="bad")
    b = browser(work, {"steps": [{"op": "goto", "url": "/good.html"}, {"op": "eval", "js": PERF_LINT_JS, "as": "l"}]}, name="good")
    la, lb = a["values"]["l"], b["values"]["l"]
    (work / "lint.json").write_text(json.dumps({"bad": la, "good": lb}, indent=1))
    return [("layout property animation flagged", "layout:slideL:left" in la["issues"], str(la["issues"])),
            ("transition: all flagged", "transition-all:.card" in la["issues"], ""),
            ("lingering will-change flagged", "will-change:.hero" in la["issues"], ""),
            ("blur animated on many nodes flagged", "animated-blur-nodes:5" in la["issues"], ""),
            ("transform/opacity page has no issues", lb["issues"] == [], str(lb["issues"])),
            ("DPR 3 capped at 2", la["dpr"] == 2, str(la["dpr"])),
            ("full-bleed shader DPR capped at 1.25", la["dprShader"] == 1.25, str(la["dprShader"]))]


X03_PAGE = """<!doctype html><html><head><meta charset=utf-8><style>
@font-face{font-family:Used;src:url(/f/used.woff2)}@font-face{font-family:Unused;src:url(/f/unused.woff2)}
#u{font-family:Used}#hid{display:none;width:20px}#vis{width:20px;height:5px}
.clip0{clip-path:inset(0);font:40px/10px monospace;color:#fff;background:#000;display:inline-block;padding:0}
.clipneg{clip-path:inset(-40% -40% -40% -40%);font:40px/10px monospace;color:#fff;background:#000;display:inline-block}</style></head>
<body style="margin:0;background:#000"><span id="u">x</span><div id="hid"></div><div id="vis"></div>
<div style="position:absolute;top:60px;left:0"><span class="clip0" id="c0">H</span></div><div style="position:absolute;top:60px;left:60px"><span class="clipneg" id="c1">H</span></div>
<canvas id="cv" width="4" height="4"></canvas></body></html>"""


def eng_x03(work: Path):
    """Render bugs already paid for: hidden-element measure, unused font faces after fonts.ready, globalAlpha, clip-path insets, file:// taint."""
    (work / "f").mkdir()
    for n in ("used", "unused"):
        (work / "f" / f"{n}.woff2").write_bytes(CAIRO_LATIN_800.read_bytes())
    page(work, "index.html", X03_PAGE)
    js = """(async()=>{await document.fonts.ready;const faces=[...document.fonts].map(f=>[f.family,f.status]);
await document.fonts.load('16px Unused');const after=[...document.fonts].map(f=>[f.family,f.status]);
const g=document.getElementById('cv').getContext('2d');g.fillStyle='#000';g.fillRect(0,0,4,4);
const group=0.5;g.globalAlpha=group;g.globalAlpha=0.5;g.fillStyle='#fff';g.fillRect(0,0,2,4);
g.globalAlpha=group*0.5;g.fillRect(2,0,2,4);g.globalAlpha=1;const p=g.getImageData(0,0,4,1).data;
return {hid:document.getElementById('hid').getBoundingClientRect().width,vis:document.getElementById('vis').getBoundingClientRect().width,faces,after,assign:p[0],mult:p[8]}})()"""
    r = browser(work, {"context": {"viewport": {"width": 140, "height": 120}}, "steps": [
        {"op": "goto", "url": "/index.html"}, {"op": "eval", "js": js, "as": "v"},
        {"op": "shot", "path": str(work / "clip.png")}]})
    v = r["values"]["v"]
    a = img(work / "clip.png")
    ink0 = int((a[30:110, 0:50].max(axis=2) > 128).sum())
    ink1 = int((a[30:110, 60:110].max(axis=2) > 128).sum())
    # file:// taints canvas unless --allow-file-access-from-files
    Image.new("RGB", (2, 2), (255, 0, 0)).save(work / "dot.png")
    (work / "taint.html").write_text("<html><body><script>const i=new Image();i.onload=()=>{const c=document.createElement('canvas');c.width=c.height=2;"
                                     "const g=c.getContext('2d');g.drawImage(i,0,0);try{c.toDataURL();window.__r='ok'}catch(e){window.__r=e.name}};i.src='dot.png';</script></body></html>")
    u = (work / "taint.html").as_uri()
    t1 = browser(work, {"steps": [{"op": "goto", "url": u}, {"op": "wait", "js": "!!window.__r"}, {"op": "eval", "js": "window.__r", "as": "r"}]}, name="taint")
    t2 = browser(work, {"launch": {"args": ["--allow-file-access-from-files"]},
                        "steps": [{"op": "goto", "url": u}, {"op": "wait", "js": "!!window.__r"}, {"op": "eval", "js": "window.__r", "as": "r"}]}, name="notaint")
    faces = dict(map(tuple, v["faces"]))
    after = dict(map(tuple, v["after"]))
    return [("measuring a display:none element returns 0", v["hid"] == 0 and v["vis"] == 20, f"{v['hid']} / {v['vis']}"),
            ("fonts.ready resolved with the unused face still unloaded", faces.get("Unused") == "unloaded" and faces.get("Used") == "loaded", str(faces)),
            ("document.fonts.load force-loads it", after.get("Unused") == "loaded", str(after)),
            ("assigning globalAlpha drops the group alpha (128)", abs(v["assign"] - 128) <= 1, str(v["assign"])),
            ("multiplying globalAlpha keeps it (64)", abs(v["mult"] - 64) <= 1, str(v["mult"])),
            ("clip-path inset(0) cuts glyph ink; -40% insets keep it", ink1 > ink0 * 1.3, f"{ink0} vs {ink1} ink px"),
            ("file:// image taints the canvas (SecurityError)", t1["values"]["r"] == "SecurityError", t1["values"]["r"]),
            ("--allow-file-access-from-files lifts it", t2["values"]["r"] == "ok", t2["values"]["r"])]


SPRITE_PAGE = """<!doctype html><html><body style="margin:0;background:#000"><canvas id="c" width="128" height="72"></canvas><script>
const atlas=document.createElement('canvas');atlas.width=16;atlas.height=16;const ag=atlas.getContext('2d');
const COLS=['#ff0000','#00ff00','#0000ff','#ffffff'];COLS.forEach((c,i)=>{ag.fillStyle=c;ag.fillRect((i%2)*8,Math.floor(i/2)*8,8,8)});
const g=document.getElementById('c').getContext('2d');let created=0;const pool=[];
function get(){if(pool.length)return pool.pop();created++;return {x:0,y:0,vx:0,vy:0,f:0}}
const MAX=2000;const sprites=[];for(let i=0;i<MAX;i++){const s=get();s.x=(i*13)%120;s.y=(i*7)%64;s.vx=((i%5)-2)*10;s.vy=((i%3)-1)*10;s.f=i%4;sprites.push(s)}
let draws=0;const origDraw=g.drawImage.bind(g);const srcs=new Set();g.drawImage=(img,...a)=>{draws++;srcs.add(img);return origDraw(img,...a)};
window.tick=(dt)=>{const c0=created;g.fillStyle='#000';g.fillRect(0,0,128,72);draws=0;
for(const s of sprites){s.x+=s.vx*dt;s.y+=s.vy*dt;g.drawImage(atlas,(s.f%2)*8,Math.floor(s.f/2)*8,8,8,Math.round(s.x),Math.round(s.y),2,2)}
return {draws,newObjects:created-c0}};
window.recycle=()=>{const s=sprites.pop();pool.push(s);const t=get();sprites.push(t);return pool.length};
window.info=()=>({created,count:sprites.length,textures:srcs.size,first:[sprites[0].x,sprites[0].y],f:sprites[0].f});window.__ready=true;</script></body></html>"""


def eng_g02(work: Path):
    """2D scene with thousands of sprites: one 16x16 atlas, 2,000 sprites moved by delta time, pooled objects, capped count."""
    page(work, "index.html", SPRITE_PAGE)
    r = browser(work, {"context": {"viewport": {"width": 128, "height": 72}}, "steps": [
        {"op": "goto", "url": "/index.html"}, {"op": "wait", "js": "window.__ready===true"},
        {"op": "eval", "js": "[tick(0.5),tick(0.5)]", "as": "t"}, {"op": "eval", "js": "window.info()", "as": "i"},
        {"op": "eval", "js": "window.recycle()", "as": "pool"}, {"op": "eval", "js": "window.info()", "as": "i2"},
        {"op": "eval", "js": "(()=>{for(let k=0;k<10;k++)tick(1/60);const b=[];for(let r=0;r<7;r++){const t0=performance.now();for(let k=0;k<10;k++)tick(1/60);b.push((performance.now()-t0)/10)}return Math.min(...b)})()", "as": "ms"},
        {"op": "shot", "path": str(work / "sprites.png")}]})
    t, i, i2 = r["values"]["t"], r["values"]["i"], r["values"]["i2"]
    # sprite 0: x=0, vx=-20, y=0, vy=-10 -> after 1 s of dt: (-20, -10)
    return [("2,000 sprites drawn per frame", t[1]["draws"] == 2000 and i["count"] == 2000, str(t[1]["draws"])),
            ("all draws come from one atlas texture", i["textures"] == 1, str(i["textures"])),
            ("no new objects allocated per frame", t[0]["newObjects"] == 0 and t[1]["newObjects"] == 0, str([x["newObjects"] for x in t])),
            ("delta-time motion: sprite 0 at (-20,-10) after 2 x 0.5 s", i["first"] == [-20, -10], str(i["first"])),
            ("recycling reuses the pooled object (created stays 2000)", i2["created"] == 2000 and i2["count"] == 2000, str(i2["created"])),
            ("frame time (best of 7 batches after warm-up) for 2,000 sprites under 16.7 ms", 0 < r["values"]["ms"] < 16.7, f"{r['values']['ms']:.2f} ms")]


def eng_292(work: Path):
    """KOSIF picture program: ordered Step objects of vector ops on a 1200x800 float sheet; re-rendered at any scale, still sharp."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("kosif_studio_render", KIT.parents[2] / "pixel-studio-painter" / "scripts" / "render.py")
    import sys as _sys
    R = _sys.modules.get("kosif_studio_render")
    if R is None:
        R = importlib.util.module_from_spec(spec)      # the vendored KOSIF Studio renderer, read-only
        _sys.modules["kosif_studio_render"] = R
        spec.loader.exec_module(R)
    steps = [R.Step("sky", [R.fill(R.rect(0, 0, 1200, 400), "#2040a0")]),
             R.Step("box", [R.fill(R.rect(300, 200, 600, 400), "#ff0000")], order="grow", origin=(600, 400))]
    out = {}
    for scale in (0.1, 0.32):
        im = R.render_image(steps, scale, ss=3 if scale <= 2 else 2, rolloff=1.0)
        im.save(work / f"pic_{scale}.png")
        out[scale] = np.asarray(im).astype(int)
    a, b = out[0.1], out[0.32]
    def edge(arr, scale):
        row = arr[int(500 * scale)]
        red = np.where((row[:, 0] > 200) & (row[:, 2] < 60))[0]
        return int(red.min()), int(red.max())
    e1, e2 = edge(a, 0.1), edge(b, 0.32)
    steps_seen = [s.label for s in steps]
    return [("scale 1.0 sheet -> 0.1 gives 120x80", a.shape[:2] == (80, 120), str(a.shape)),
            ("scale 0.32 gives 384x256", b.shape[:2] == (256, 384), str(b.shape)),
            ("default paper #000000 below the sky", a[-1, 2].tolist() == [0, 0, 0], str(a[-1, 2].tolist())),
            ("box edges at 300..900 units scale to 30..89 px", e1 == (30, 89), str(e1)),
            ("box edges at scale 0.32 are 96..287 px (re-drawn, not resampled)", e2 == (96, 287), str(e2)),
            ("rolloff=1 keeps the logo red exact", a[50, 60].tolist() == [255, 0, 0], str(a[50, 60].tolist())),
            ("steps drawn in order (box over sky)", steps_seen == ["sky", "box"] and a[30, 60].tolist() == [255, 0, 0], str(a[30, 60].tolist()))]


# ---------------------------------------------------------------- HTML scenes -> narrated MP4

def tone_wav(path: Path, seconds: float, freq: float, sr=16000):
    import wave
    t = np.arange(int(sr * seconds)) / sr
    data = (0.3 * np.sin(2 * np.pi * freq * t) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(data.tobytes())
    return path


SCENE_HTML = """<!doctype html><html><head><meta charset=utf-8><style>html,body{margin:0;background:BG;width:1920px;height:1080px;overflow:hidden}
#t{position:absolute;left:200px;top:400px;width:300px;height:200px;background:#fff}</style></head><body><div id="t"></div>EXTRA<script>
window.render=(t)=>{document.getElementById('t').style.transform='translateX('+(t*400).toFixed(1)+'px)';window.__ready=true};window.render(0);</script></body></html>"""


def build_scenes(work: Path, scenes, fps, xfade):
    """scenes.json -> per-scene motion frames (render(t)) -> clip per scene -> xfade concat -> narration mixed in."""
    manifest = []
    clips = []
    for i, sc in enumerate(scenes):
        html = SCENE_HTML.replace("BG", sc["bg"]).replace("EXTRA", sc.get("extra", ""))
        page(work, f"scene{i}.html", html)
        tone_wav(work / f"narration{i}.wav", sc["narration_s"], 300 + 100 * i)
        dur = round(sc["narration_s"] + 1.5, 3)               # auto duration = TTS + 1.5 s
        manifest.append({"order": i, "html": f"scene{i}.html", "narration": f"narration{i}.wav", "duration": dur, "text": sc["text"]})
    (work / "scenes.json").write_text(json.dumps(manifest, indent=1))
    steps = []
    for m in manifest:
        steps += [{"op": "goto", "url": "/" + m["html"]}, {"op": "wait", "js": "window.__ready===true"},
                  {"op": "frames", "count": int(round(m["duration"] * fps)), "fps": fps, "dir": str(work / f"f{m['order']}"), "fast": True},
                  {"op": "eval", "js": "(document.getElementById('end')||{}).textContent||''", "as": f"end{m['order']}"}]
    rr = browser(work, {"context": {"viewport": {"width": 1920, "height": 1080}}, "steps": steps}, name="scenes")
    (work / "end_card.txt").write_text(rr["values"][f"end{manifest[-1]['order']}"])
    for m in manifest:
        clip = work / f"clip{m['order']}.mp4"
        ff("-framerate", str(fps), "-i", str(work / f"f{m['order']}" / "f_%04d.png"), "-i", str(work / m["narration"]),
           "-af", "apad", "-t", str(m["duration"]), "-c:v", "libx264", "-preset", "ultrafast", "-crf", "20", "-pix_fmt", "yuv420p",
           "-r", str(fps), "-c:a", "aac", "-ar", "48000", str(clip))
        clips.append(clip)
    d0 = manifest[0]["duration"]
    out = work / "demo.mp4"
    ff("-i", str(clips[0]), "-i", str(clips[1]), "-filter_complex",
       f"[0:v][1:v]xfade=transition=fade:duration={xfade}:offset={d0 - xfade}[v];[0:a][1:a]acrossfade=d={xfade}[a]",
       "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "20", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-movflags", "+faststart", str(out))
    return out, manifest


def black_frames(video) -> list:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(video), "-vf", "blackdetect=d=0.03:pix_th=0.05", "-an", "-f", "null", "-"],
                       capture_output=True, text=True)
    return re.findall(r"black_start:([\d.]+)", r.stderr)


END_CARD = '<div id="end" style="position:absolute;left:100px;top:100px;color:#fff;font:48px sans-serif">kosif.example/try — Start free</div>'


def end_card_ok(work: Path) -> bool:
    t = (work / "end_card.txt").read_text()
    return bool(re.search(r"[a-z0-9-]+\.[a-z]{2,}/?\S*", t)) and bool(re.search(r"\b(start|try|get|book|join)\b", t, re.I))


def eng_360(work: Path):
    """Single-prompt demo pipeline: HTML scene per 1920x1080 page + narration, scenes.json, motion render, crossfade concat; checklist."""
    xf, fps = 0.4, 6
    scenes = [{"bg": "#203060", "narration_s": 1.0, "text": "hook"}, {"bg": "#602030", "narration_s": 0.5, "text": "cta", "extra": END_CARD}]
    out, man = build_scenes(work, scenes, fps, xf)
    v, a = vstream(out), astream(out)
    total = man[0]["duration"] + man[1]["duration"] - xf
    fr = decode_frames(out, 1920, 1080)
    first, last = fr[0].astype(int), fr[-1].astype(int)
    moving = int(np.abs(fr[0].astype(int) - fr[3].astype(int)).sum()) > 0
    return [("auto duration = narration + 1.5 s (2.5 s, 2.0 s)", [m["duration"] for m in man] == [2.5, 2.0], str([m["duration"] for m in man])),
            ("crossfade 0.4 s: total = 2.5 + 2.0 - 0.4", abs(float(probe(out)["format"]["duration"]) - total) < 0.2, probe(out)["format"]["duration"]),
            ("audio stream present", a is not None, str(a and a["codec_name"])),
            ("1920x1080", (v["width"], v["height"]) == (1920, 1080), f"{v['width']}x{v['height']}"),
            ("no black frames", black_frames(out) == [], str(black_frames(out))),
            ("scenes are motion, not stills", moving, ""),
            ("opens on scene 1, ends on scene 2", near(first[5, 5], (0x20, 0x30, 0x60), 8) and near(last[1070, 1900], (0x60, 0x20, 0x30), 8),
             f"{first[5, 5].tolist()} {last[1070, 1900].tolist()}"),
            ("end card carries a URL and a CTA", end_card_ok(work), "")]


def eng_365(work: Path):
    """HTML scenes to MP4: manifest order and durations, crossfade blend at the seam, audio stream, no black gap, end card."""
    xf, fps = 0.3, 6
    scenes = [{"bg": "#00a000", "narration_s": 0.5, "text": "one"}, {"bg": "#a000a0", "narration_s": 0.5, "text": "two", "extra": END_CARD}]
    out, man = build_scenes(work, scenes, fps, xf)
    fr = decode_frames(out, 1920, 1080)
    seam = int(round((man[0]["duration"] - xf / 2) * fps))
    mid = fr[seam][5, 5].astype(int)
    m = json.loads((work / "scenes.json").read_text())
    # planted failure for the checker: a hard cut through black must be flagged
    ff("-f", "lavfi", "-i", "color=c=0x00a000:s=320x180:r=6:d=1", "-f", "lavfi", "-i", "color=c=black:s=320x180:r=6:d=0.5",
       "-f", "lavfi", "-i", "color=c=0xa000a0:s=320x180:r=6:d=1", "-filter_complex", "[0][1][2]concat=n=3:v=1:a=0", "-c:v", "libx264",
       "-preset", "ultrafast", "-pix_fmt", "yuv420p", str(work / "planted_black.mp4"))
    return [("manifest lists scenes in order with html + narration", [x["html"] for x in m] == ["scene0.html", "scene1.html"] and all(x["narration"] for x in m), ""),
            ("seam frame is a blend of both scene colours", 30 < mid[0] < 150 and 30 < mid[1] < 150 and mid[2] < 120, str(mid.tolist())),
            ("audio stream exists", astream(out) is not None, ""),
            ("1920x1080", (vstream(out)["width"], vstream(out)["height"]) == (1920, 1080), ""),
            ("no black frames between scenes", black_frames(out) == [], str(black_frames(out))),
            ("the black-frame check catches a planted black gap", len(black_frames(work / "planted_black.mp4")) == 1, str(black_frames(work / "planted_black.mp4"))),
            ("end card has URL and CTA", end_card_ok(work), "")]


VIRTUAL_PAGE = """<!doctype html><html><head><style>@keyframes mv{from{left:0px}to{left:100px}}
#css{position:absolute;left:0;top:0;width:4px;height:4px;background:#fff;animation:mv 2s linear both}</style></head><body>
<div id="css"></div><div id="w" style="position:absolute;top:10px;width:4px;height:4px;background:#0f0"></div><script>
document.getElementById('w').animate([{transform:'translateX(0px)'},{transform:'translateX(50px)'}],{duration:1000,fill:'both'});
window.__ticks=0;window.__t0=Date.now();setInterval(()=>window.__ticks++,100);</script></body></html>"""
VSEEK = "((t)=>{document.getAnimations().forEach(a=>{a.pause();a.currentTime=t*1000});return [parseFloat(getComputedStyle(document.getElementById('css')).left), new DOMMatrix(getComputedStyle(document.getElementById('w')).transform).m41]})"


def eng_110(work: Path):
    """Virtual-time mode for pages with no seek hook: pause document.getAnimations() at t*1000, or advance Chromium's virtual clock."""
    page(work, "index.html", VIRTUAL_PAGE)
    r = browser(work, {"cdp": True, "steps": [
        {"op": "goto", "url": "/index.html"},
        {"op": "eval", "js": VSEEK + "(1.5)", "as": "a"}, {"op": "eval", "js": VSEEK + "(0.25)", "as": "b"},
        {"op": "cdpSend", "method": "Emulation.setVirtualTimePolicy", "params": {"policy": "pause"}},
        {"op": "eval", "js": "[window.__ticks, Date.now()]", "as": "v0"},
        {"op": "cdpSend", "method": "Emulation.setVirtualTimePolicy", "params": {"policy": "advance", "budget": 1000},
         "waitEvent": "Emulation.virtualTimeBudgetExpired"},
        {"op": "eval", "js": "[window.__ticks, Date.now()]", "as": "v1"},
        {"op": "cdpSend", "method": "Emulation.setVirtualTimePolicy", "params": {"policy": "pauseIfNetworkFetchesPending"}}]})
    a, b, (k0, d0), (k1, d1) = r["values"]["a"], r["values"]["b"], r["values"]["v0"], r["values"]["v1"]
    return [("CSS animation at t=1.5 s: left = 75 px", abs(a[0] - 75) < 1e-6, str(a[0])),
            ("WAAPI animation at t=1.5 s clamps at 50 px (fill)", abs(a[1] - 50) < 1e-6, str(a[1])),
            ("seeking back to 0.25 s: 12.5 px and 12.5 px", abs(b[0] - 12.5) < 1e-6 and abs(b[1] - 12.5) < 1e-6, str(b)),
            ("virtual clock: a 1000 ms budget advances Date.now by about 1000 ms", 990 <= d1 - d0 <= 1100, f"{d1 - d0} ms"),
            ("virtual clock fires the 100 ms timer about 10 times", 9 <= k1 - k0 <= 11, str(k1 - k0))]


BUILD_CJS = r"""const fs=require('fs');const path=require('path');const out=process.argv[2];fs.mkdirSync(path.join(out,'svg'),{recursive:true});
const N=288;const frames=[];for(let i=0;i<N;i++){const t=i/24;const x=(4+t*4).toFixed(2);
const svg=`<svg xmlns="http://www.w3.org/2000/svg" width="64" height="36" viewBox="0 0 64 36"><rect width="64" height="36" fill="#1b1030"/><circle cx="${x}" cy="18" r="4" fill="#ffd400"/></svg>`;
fs.writeFileSync(path.join(out,'svg',String(i).padStart(4,'0')+'.svg'),svg);frames.push(svg);}
fs.writeFileSync(path.join(out,'player.html'),'<html><body><img id=f><script>const F='+JSON.stringify(frames)+';let i=0;setInterval(()=>{document.getElementById("f").src="data:image/svg+xml,"+encodeURIComponent(F[i++%F.length])},1000/24)</script></body></html>');
console.log(N);"""
RASTER_JS = """(async()=>{const out=[];const c=document.createElement('canvas');c.width=64;c.height=36;const g=c.getContext('2d');
for(let i=0;i<288;i++){const n=String(i).padStart(4,'0');const im=new Image();im.src='/svg/'+n+'.svg';await im.decode();g.clearRect(0,0,64,36);g.drawImage(im,0,0);
out.push(c.toDataURL('image/png').split(',')[1]);}return out})()"""


def eng_223(work: Path):
    """SVG frame export + ffmpeg: Node writes 288 SVG frames and a self-contained HTML player, Chromium rasterises, H.264 crf 18."""
    import base64
    (work / "build.cjs").write_text(BUILD_CJS)
    n = int(subprocess.run(["node", str(work / "build.cjs"), str(work)], capture_output=True, text=True, check=True).stdout.strip())
    page(work, "raster.html", "<!doctype html><html><body></body></html>")
    r = browser(work, {"steps": [{"op": "goto", "url": "/raster.html"}, {"op": "eval", "js": RASTER_JS, "as": "png"}]}, timeout=90)
    (work / "frames").mkdir()
    for i, b in enumerate(r["values"]["png"]):
        (work / "frames" / f"{i:04d}.png").write_bytes(base64.b64decode(b))
    mp4 = work / "film.mp4"
    ff("-framerate", "24", "-i", str(work / "frames" / "%04d.png"), "-c:v", "libx264", "-preset", "slow", "-crf", "18",
       "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(mp4))
    v = vstream(mp4)
    fr = decode_frames(mp4, 64, 36)
    def cx(f):
        cols = np.where((f[18, :, 0] > 180) & (f[18, :, 1] > 150) & (f[18, :, 2] < 120))[0]
        return (cols.min() + cols.max() + 1) / 2 if len(cols) else None
    svgs = sorted((work / "svg").glob("*.svg"))
    return [("Node wrote 288 SVG frames 0000..0287", n == 288 and len(svgs) == 288 and svgs[-1].name == "0287.svg", f"{len(svgs)} {svgs[-1].name}"),
            ("self-contained HTML player embeds all frames", (work / "player.html").read_text().count("<svg") == 288, ""),
            ("rasteriser produced 288 PNGs", len(list((work / "frames").glob("*.png"))) == 288, ""),
            ("H.264 yuv420p, 288 frames = 12.0 s at 24 fps", v["codec_name"] == "h264" and v["pix_fmt"] == "yuv420p" and int(v["nb_frames"]) == 288
             and abs(float(v["duration"]) - 12.0) < 0.05, f"{v['nb_frames']} {v['duration']}"),
            ("faststart (moov first)", moov_first(mp4), ""),
            ("frame 120 shows the circle at 4 + 5*4 = 24 px", cx(fr[120]) is not None and abs(cx(fr[120]) - 24) <= 1, str(cx(fr[120])))]


PROGRAMS = {
    "ENG-10": eng_10, "ENG-32": eng_32, "ENG-274": eng_274, "ENG-284": eng_284, "ENG-388": eng_388,
    "ENG-72": eng_72, "ENG-93": eng_93, "ENG-116": eng_116,
    "ENG-12": eng_12, "ENG-286": eng_286, "ENG-285": eng_285, "ENG-222": eng_222,
    "ENG-267": eng_267, "ENG-268": eng_268, "ENG-272": eng_272, "ENG-280": eng_280, "ENG-297": eng_297, "ENG-298": eng_298,
    "ENG-304": eng_304, "ENG-394": eng_394, "ENG-435": eng_435, "ENG-378": eng_378, "ENG-379": eng_379, "ENG-382": eng_382,
    "ENG-383": eng_383, "ENG-375": eng_375,
    "ENG-112": eng_112, "ENG-125": eng_125, "ENG-185": eng_185, "ENG-128": eng_128, "ENG-161": eng_161, "ENG-170": eng_170,
    "ENG-361": eng_361, "ENG-X03": eng_x03, "ENG-G02": eng_g02,
    "ENG-292": eng_292, "ENG-360": eng_360, "ENG-365": eng_365, "ENG-110": eng_110, "ENG-223": eng_223,
}
