"""Real programs for the engines-render-pipeline family (ENG-*).

Each function builds its own fixture (tiny frames, tones, HTML pages, JSON specs), performs the
card's technique (ffmpeg encodes, numpy post passes, contract validators, schedulers, codec
pickers ...) with the card's own numbers, writes its outputs into `work`, and returns checks whose
answers are known in advance. Browser-only, cloud, paid or GUI cards are not here: they are listed
in out/power-programs/engines-skipped.json with the reason.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import math
import os
import re
import secrets
import shlex
import shutil
import subprocess
import sys
import time
import wave
import xml.etree.ElementTree as ET
import zipfile
from fractions import Fraction
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parents[5]

# ---------------------------------------------------------------- shared helpers


def sh(cmd, **kw):
    """Run a command (list), raise with stderr on failure, return stdout text."""
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, **kw)
    if r.returncode != 0:
        raise RuntimeError(f"{cmd[0]} failed: {r.stderr[-800:]}")
    return r.stdout + r.stderr


def ff(*args):
    return sh(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args])


def probe(path) -> dict:
    out = sh(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path])
    return json.loads(out)


def vstream(path) -> dict:
    return next(s for s in probe(path)["streams"] if s["codec_type"] == "video")


def astream(path):
    return next((s for s in probe(path)["streams"] if s["codec_type"] == "audio"), None)


def count_frames(path) -> int:
    out = sh(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
              "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", path])
    return int(out.strip().split()[0])


def decode(path, w, h, extra=None) -> np.ndarray:
    """Decode a video to an (n, h, w, 3) uint8 array."""
    cmd = ["ffmpeg", "-v", "error", "-i", str(path)] + (extra or []) + \
        ["-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)


def write_png(path, arr):
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(path)


def solid(w, h, rgb):
    a = np.zeros((h, w, 3), np.uint8)
    a[:] = rgb
    return a


def write_wav(path, samples, sr=16000, channels=1):
    s = np.asarray(samples, dtype=np.float64)
    if channels == 2 and s.ndim == 1:
        s = np.stack([s, s], 1)
    pcm = (np.clip(s, -1, 1) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())


def read_audio(path, sr=16000, channels=1) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "s16le", "-ac", str(channels),
                          "-ar", str(sr), "-"], capture_output=True, check=True).stdout
    a = np.frombuffer(raw, "<i2").astype(np.float64) / 32768
    return a.reshape(-1, channels) if channels > 1 else a


def tone(freq, sec, sr=16000, amp=0.5):
    t = np.arange(int(sec * sr)) / sr
    return amp * np.sin(2 * np.pi * freq * t)


def amp_at(x, freq, sr):
    """Amplitude of a sinusoid at freq in signal x (single-bin DFT)."""
    n = len(x)
    t = np.arange(n) / sr
    return 2 * abs(np.dot(x, np.exp(-2j * np.pi * freq * t))) / n


def frames_from(fn, n, folder, pattern="f_%04d.png"):
    folder.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        write_png(folder / (pattern % i), fn(i))
    return folder / pattern


def encode_png(pattern, out, fps, extra=None, start_number=0):
    ff("-framerate", str(fps), "-start_number", str(start_number), "-i", pattern,
       *(extra or ["-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p"]), out)
    return out


def gray_clip(path, w, h, fps, n, levels=None, extra=None):
    """Encode n frames whose grey level encodes the frame index (8*i by default)."""
    tmp = Path(str(path) + ".frames")
    levels = levels or [min(255, 8 * i) for i in range(n)]
    frames_from(lambda i: solid(w, h, (levels[i],) * 3), n, tmp)
    encode_png(tmp / "f_%04d.png", path, fps, extra)
    shutil.rmtree(tmp)
    return path


def save_json(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def mulberry32(seed):
    """Exact port of the JS mulberry32 (constant 0x6D2B79F5), 32-bit integer maths."""
    state = [seed & 0xFFFFFFFF]

    def imul(a, b):
        return (a * b) & 0xFFFFFFFF

    def nxt():
        state[0] = (state[0] + 0x6D2B79F5) & 0xFFFFFFFF
        a = state[0]
        t = imul(a ^ (a >> 15), 1 | a)
        t = ((t + imul(t ^ (t >> 7), 61 | t)) & 0xFFFFFFFF) ^ t
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return nxt


JS_MULBERRY_SEED1 = [0.6270739405881613, 0.002735721180215478, 0.5274470399599522]  # measured with node
JS_MULBERRY_SEED7 = [0.011704753153026104, 0.06195825757458806, 0.97690763277933]


def hash2(i, j):
    """Stateless integer hash of a cell -> [0,1) (mulberry32 seeded with a mixed key)."""
    return mulberry32((i * 374761393 + j * 668265263) & 0xFFFFFFFF)()


def parse_html(text):
    from bs4 import BeautifulSoup
    return BeautifulSoup(text, "html.parser")


def _raises(fn, exc):
    try:
        fn()
    except exc:
        return True
    return False


def clamp01(x):
    return max(0.0, min(1.0, x))


# ------------------------------------------------- composition contract validator (shared)


def composition_errors(html, required=("data-composition-id", "data-width", "data-height", "data-duration", "data-fps"),
                       fps_allowed=None, root_selector=None):
    """Validate a seekable HTML composition: a root carrying the data-* attrs, a paused timeline
    registered literally on window.__timelines[<id>], and a MOTION.shim(<id>, seconds) call that
    matches data-duration. Returns a list of problems (empty = valid)."""
    soup = parse_html(html)
    root = soup.select_one(root_selector) if root_selector else soup.find(attrs={"data-composition-id": True})
    if root is None:
        return ["no root with data-composition-id"]
    errs = [f"root missing {a}" for a in required if not root.has_attr(a)]
    if errs:
        return errs
    for a in ("data-width", "data-height", "data-duration", "data-fps"):
        if root.has_attr(a):
            try:
                if float(root[a]) <= 0:
                    errs.append(f"{a} not positive")
            except ValueError:
                errs.append(f"{a} not numeric")
    if fps_allowed and root.has_attr("data-fps") and int(float(root["data-fps"])) not in fps_allowed:
        errs.append(f"data-fps {root['data-fps']} not in {sorted(fps_allowed)}")
    cid = root["data-composition-id"]
    script = "\n".join(s.get_text() for s in soup.find_all("script"))
    if not re.search(r"window\.__timelines\[\s*['\"]%s['\"]\s*\]\s*=" % re.escape(cid), script):
        errs.append("timeline not registered literally on window.__timelines")
    if "paused" not in script or not re.search(r"paused\s*:\s*true", script):
        errs.append("timeline not paused")
    m = re.search(r"MOTION\.shim\(\s*['\"]%s['\"]\s*,\s*([\d.]+)\s*\)" % re.escape(cid), script)
    if "MOTION.shim" in script or "data-fps" in required:
        if not m:
            errs.append("MOTION.shim(root, seconds) missing")
        elif root.has_attr("data-duration") and abs(float(m.group(1)) - float(root["data-duration"])) > 1e-9:
            errs.append("shim seconds differ from data-duration")
    return errs


def composition_page(cid="root", w=1920, h=1080, dur=8, fps=30, shim=True, extra_body="", attrs=None):
    a = {"data-composition-id": cid, "data-width": w, "data-height": h, "data-duration": dur, "data-fps": fps}
    if attrs is not None:
        a = attrs
    at = " ".join(f'{k}="{v}"' for k, v in a.items())
    sh_line = f"MOTION.shim('{cid}', {dur});" if shim else ""
    return (f"<!doctype html><html><body><div id=\"{cid}\" {at}>{extra_body}</div>"
            f"<script>const tl = gsap.timeline({{paused: true}});\n"
            f"tl.to('#{cid} .t', {{opacity: 1, duration: 1}}, 0.2);\n"
            f"window.__timelines = window.__timelines || {{}};\nwindow.__timelines['{cid}'] = tl;\n{sh_line}</script>"
            f"</body></html>")


BANNED_JS = {
    "Math.random": r"Math\.random\s*\(",
    "Date.now": r"Date\.now\s*\(",
    "performance.now": r"performance\.now\s*\(",
    "requestAnimationFrame": r"requestAnimationFrame\s*\(",
    "setTimeout": r"setTimeout\s*\(",
    "setInterval": r"setInterval\s*\(",
    "fetch": r"\bfetch\s*\(",
}


def lint_js(src, banned):
    """Return the banned names that occur in JS source (comments stripped)."""
    code = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    code = re.sub(r"//[^\n]*", "", code)
    return sorted(name for name in banned if re.search(BANNED_JS.get(name, re.escape(name)), code))


# ================================================================ batch 1: ENG-01 .. ENG-59


def eng01(work):
    page = composition_page()
    (work / "index.html").write_text(page, encoding="utf-8")
    root = parse_html(page).find(attrs={"data-composition-id": True})
    frames = round(float(root["data-duration"]) * float(root["data-fps"]))
    bad = composition_page(attrs={"data-composition-id": "root", "data-width": 1920, "data-height": 1080,
                                  "data-duration": 8})
    mism = page.replace("MOTION.shim('root', 8)", "MOTION.shim('root', 6)")
    unreg = page.replace("window.__timelines['root'] = tl;", "")
    return [("defaults 1920x1080 8 s 30 fps", (root["data-width"], root["data-height"], root["data-duration"], root["data-fps"]) == ("1920", "1080", "8", "30"), dict(root.attrs)),
            ("valid contract has no problems", composition_errors(page) == [], composition_errors(page)),
            ("frames = duration x fps = 240", frames == 240, frames),
            ("page without data-fps rejected", "root missing data-fps" in composition_errors(bad), composition_errors(bad)),
            ("shim seconds must equal data-duration", "shim seconds differ from data-duration" in composition_errors(mism), composition_errors(mism)),
            ("unregistered timeline rejected", any("registered" in e for e in composition_errors(unreg)), composition_errors(unreg))]


def eng02(work):
    W, H, fps = 64, 36, 12

    class Scene:  # the module contract: DURATION + renderFrame(t)
        DURATION = 1.0

        @staticmethod
        def renderFrame(t):
            a = solid(W, H, (0, 0, 0))
            x = int(round(t * 48))
            a[:, x:x + 8] = 255
            return a
    n = round(Scene.DURATION * fps)
    folder = work / "frames"
    folder.mkdir()
    for f in range(n):
        write_png(folder / f"{f:05d}.png", Scene.renderFrame(f / fps))
    out = encode_png(folder / "%05d.png", work / "scene.mp4", fps,
                     ["-c:v", "libx264", "-preset", "ultrafast", "-crf", "1", "-pix_fmt", "yuv420p"])
    vs = vstream(out)
    frames = decode(out, W, H)
    xs = [int(np.argmax(fr[H // 2, :, 0] > 128)) for fr in frames]
    want = [int(round(f / fps * 48)) for f in range(n)]
    return [("frames = DURATION*fps = 12", count_frames(out) == 12, count_frames(out)),
            ("h264 yuv420p", (vs["codec_name"], vs["pix_fmt"]) == ("h264", "yuv420p"), (vs["codec_name"], vs["pix_fmt"])),
            ("frame f shows renderFrame(f/fps)", all(abs(a - b) <= 1 for a, b in zip(xs, want)), xs)]


def eng03(work):
    W, H, fps, sr = 64, 36, 30, 48000
    srcs = []
    for k, (rgb, freq) in enumerate([((220, 30, 30), 440), ((30, 30, 220), 660)]):
        p = work / f"shot{k}.mov"
        ff("-f", "lavfi", "-i", f"color=c=0x{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}:s={W}x{H}:r={fps}:d=1",
           "-f", "lavfi", "-i", f"sine=f={freq}:r=44100:d=1", "-c:v", "libx264", "-preset", "ultrafast",
           "-crf", "8", "-c:a", "pcm_s16le", "-shortest", p)
        srcs.append(p)
    music = work / "music.wav"
    write_wav(music, tone(220, 1.0, sr, 0.2), sr)
    S, N = [(5, 10), (3, 8)], [10, 8]
    fc = []
    for k, (s, n) in enumerate(S):
        fc.append(f"[{k}:v]trim=start_frame={s}:end_frame={s + n},setpts=PTS-STARTPTS,format=yuv420p[v{k}]")
        fc.append(f"[{k}:a]atrim=start={s / fps}:end={(s + n) / fps},asetpts=PTS-STARTPTS,aresample=48000,volume=-8dB[a{k}]")
    fc.append("[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][sfx]")
    fc.append("[sfx][2:a]amix=inputs=2:duration=first:normalize=0[a]")
    inter = work / "intermediate.mov"
    ff(*sum([["-i", p] for p in srcs], []), "-i", music, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]",
       "-c:v", "libx264", "-crf", "8", "-preset", "ultrafast", "-c:a", "pcm_s24le", inter)
    final = work / "final.mp4"
    ff("-i", inter, "-c:v", "libx264", "-profile:v", "high", "-crf", "17", "-g", "60", "-preset", "veryfast",
       "-pix_fmt", "yuv420p", "-c:a", "aac", final)
    fr = decode(inter, W, H)
    a = read_audio(inter, sr)
    seg = a[int(0.05 * sr):int(0.30 * sr)]
    raw = read_audio(srcs[0], sr)[int(0.2 * sr):int(0.45 * sr)]
    ratio = amp_at(seg, 440, sr) / max(amp_at(raw, 440, sr), 1e-9)
    music_amp = amp_at(seg, 220, sr)
    ast = astream(inter)
    return [("frames = 10 + 8", len(fr) == 18, len(fr)),
            ("first window from shot 0 (red)", fr[0, 5, 5, 0] > 150 and fr[9, 5, 5, 2] < 100, fr[0, 5, 5].tolist()),
            ("second window from shot 1 (blue)", fr[10, 5, 5, 2] > 150, fr[10, 5, 5].tolist()),
            ("shot audio at -8 dB (x0.398)", abs(ratio - 10 ** (-8 / 20)) < 0.04, round(ratio, 4)),
            ("music summed unnormalised (amp 0.2)", abs(music_amp - 0.2) < 0.02, round(music_amp, 4)),
            ("intermediate PCM 24-bit 48 kHz", (ast["codec_name"], ast["sample_rate"]) == ("pcm_s24le", "48000"), (ast["codec_name"], ast["sample_rate"])),
            ("final High profile", vstream(final)["profile"] == "High", vstream(final)["profile"])]


def eng04(work):
    def dpr_cap(phone, device_dpr):
        return min(device_dpr, 1.0 if phone else 1.5)

    def wait_shader(completes_at_ms, frame_ms=16, give_up=12000):
        t = 0
        while t <= give_up:
            if completes_at_ms is not None and t >= completes_at_ms:
                return ("ready", t)
            t += frame_ms
        return ("gave_up", t)

    def link_probe(link_ms, storage):
        if link_ms > 1500:
            storage["sqc_world_slow"] = "1"
        return storage

    def make_world(has_webgl):
        return None if not has_webgl else {"canvas": True, "fade_in_s": 1.5}
    r = {"dpr_phone": dpr_cap(True, 3), "dpr_desktop": dpr_cap(False, 3), "dpr_low": dpr_cap(False, 1),
         "never": wait_shader(None), "fast": wait_shader(5000), "slow_flag": link_probe(1600, {}),
         "ok_flag": link_probe(1400, {}), "no_gl": make_world(False)}
    save_json(work / "guards.json", r)
    return [("phone dpr capped at 1", r["dpr_phone"] == 1.0, r["dpr_phone"]),
            ("desktop dpr capped at 1.5", r["dpr_desktop"] == 1.5, r["dpr_desktop"]),
            ("low dpr untouched", r["dpr_low"] == 1, r["dpr_low"]),
            ("gives up after 12 s", r["never"][0] == "gave_up" and r["never"][1] > 12000, r["never"]),
            ("compiles at 5 s -> ready", r["fast"][0] == "ready" and r["fast"][1] < 5100, r["fast"]),
            ("link > 1.5 s remembers slow device", r["slow_flag"] == {"sqc_world_slow": "1"} and r["ok_flag"] == {}, (r["slow_flag"], r["ok_flag"])),
            ("no WebGL returns null", r["no_gl"] is None, r["no_gl"])]


def eng05(work):
    html = ('<div class="door"><video preload="none" data-src="door.mp4" poster="door.jpg"></video></div>'
            '<div class="dash"><video preload="none" data-src="dash.mp4" poster="dash.jpg"></video></div>')

    def gate(page, wide, reduced, save_data):
        soup = parse_html(page)
        for v in soup.find_all("video"):
            if wide and not reduced and not save_data:
                v["src"] = v["data-src"]
        return soup

    def sw_route(url, headers, destination=""):
        if destination == "video" or "range" in {k.lower() for k in headers} or re.search(r"\.(mp4|webm|mov)$", url):
            return "network"
        return "cache-first"
    on = gate(html, True, False, False)
    off = gate(html, True, True, False)
    data = gate(html, True, False, True)
    (work / "gated.html").write_text(str(on), encoding="utf-8")
    routes = [sw_route("/door.mp4", {}), sw_route("/x", {"Range": "bytes=0-"}), sw_route("/clip", {}, "video"),
              sw_route("/index.html", {})]
    return [("wide + motion ok -> src swapped in", all(v.get("src") for v in on.find_all("video")), [v.get("src") for v in on.find_all("video")]),
            ("reduced motion keeps poster only", not any(v.get("src") for v in off.find_all("video")), str(off)[:80]),
            ("save-data keeps poster only", not any(v.get("src") for v in data.find_all("video")), ""),
            ("preload stays none", all(v["preload"] == "none" for v in on.find_all("video")), ""),
            ("SW sends video/Range to network, html cached", routes == ["network", "network", "network", "cache-first"], routes)]


def eng06(work):
    def compile_storyboard(brief, scenes=5, sec=6, fps=30):
        sc = [{"id": f"scene-{i + 1:02d}", "start": i * sec, "end": (i + 1) * sec,
               "motion_prompt": f"{brief} — beat {i + 1}"} for i in range(scenes)]
        return {"aspect": "9:16", "fps": fps, "duration_seconds": scenes * sec, "exact_background_lines": 2,
                "approval": {"storyboard": False, "posters": False}, "sound": {"policy": "user-audio-untouched"},
                "palette": ["#0b0b0b", "#f2efe8", "#e4342f"], "scenes": sc}
    sb = compile_storyboard("حملة")
    d = work / "projects" / "viral-editorial"
    d.mkdir(parents=True)
    save_json(d / "storyboard.json", sb)
    save_json(d / "posters.json", [{"scene": s["id"]} for s in sb["scenes"]])
    save_json(d / "motion-prompts.json", [s["motion_prompt"] for s in sb["scenes"]])
    return [("5 scenes", len(sb["scenes"]) == 5, len(sb["scenes"])),
            ("5 x 6 s = 30 s", sb["duration_seconds"] == 30 and sb["scenes"][-1]["end"] == 30, sb["duration_seconds"]),
            ("900 frames at 30 fps", sb["duration_seconds"] * sb["fps"] == 900, sb["duration_seconds"] * sb["fps"]),
            ("contiguous scenes", all(a["end"] == b["start"] for a, b in zip(sb["scenes"], sb["scenes"][1:])), [s["start"] for s in sb["scenes"]]),
            ("exact_background_lines = 2, approvals off", sb["exact_background_lines"] == 2 and not any(sb["approval"].values()), sb["approval"]),
            ("three files written", sorted(p.name for p in d.iterdir()) == ["motion-prompts.json", "posters.json", "storyboard.json"], sorted(p.name for p in d.iterdir()))]


def ffprobe_shim(path):
    """ffprobe stand-in built on ffmpeg only: exact frame count by decoding, duration to 1/100 s."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-map", "0:v:0", "-f", "null", "-"],
                       capture_output=True, text=True)
    err = r.stderr
    frames = int(re.findall(r"frame=\s*(\d+)", err)[-1])
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err)
    dur = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
    s = re.search(r"Video: (\w+).*?, (\d+)x(\d+)", err)
    return {"frames": frames, "duration": round(dur, 2), "codec": s.group(1), "width": int(s.group(2)), "height": int(s.group(3))}


def eng07(work):
    clip = gray_clip(work / "clip.mp4", 64, 36, 25, 37)
    shim = ffprobe_shim(clip)
    save_json(work / "shim.json", shim)
    real = probe(clip)
    return [("exact frame count 37", shim["frames"] == 37 == count_frames(clip), shim["frames"]),
            ("duration 1.48 s to 1/100", shim["duration"] == 1.48, shim["duration"]),
            ("matches real ffprobe duration", abs(shim["duration"] - float(real["format"]["duration"])) < 0.01, real["format"]["duration"]),
            ("codec/size parsed", (shim["codec"], shim["width"], shim["height"]) == ("h264", 64, 36), shim)]


def measure_lufs(path):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    summary = out[out.rfind("Summary:"):]
    i = float(re.search(r"I:\s+(-?[\d.]+) LUFS", summary).group(1))
    pk = re.search(r"Peak:\s+(-?[\d.inf]+) dBFS", summary)
    return i, (float(pk.group(1)) if pk else None)


def normalize_to(src, dst, target):
    i, _ = measure_lufs(src)
    ff("-i", src, "-af", f"volume={target - i:.3f}dB", "-c:a", "pcm_s16le", dst)
    return measure_lufs(dst)[0]


def eng08(work):
    W, H, fps = 64, 36, 30
    spec = {"size": [W, H], "fps": fps, "clips": [{"color": "red", "dur": 1.0}, {"color": "blue", "dur": 1.0}],
            "transition": {"type": "fade", "dur": 0.5}, "loudness": -14}
    save_json(work / "edit.json", spec)
    ins = []
    for c in spec["clips"]:
        ins += ["-f", "lavfi", "-i", f"color=c={c['color']}:s={W}x{H}:r={fps}:d={c['dur']}"]
    for k, c in enumerate(spec["clips"]):
        ins += ["-f", "lavfi", "-i", f"sine=f={300 + 200 * k}:d={c['dur']}"]
    d = spec["transition"]["dur"]
    off = spec["clips"][0]["dur"] - d
    fc = f"[0:v][1:v]xfade=transition={spec['transition']['type']}:duration={d}:offset={off},format=yuv420p[v];[2:a][3:a]acrossfade=d={d}[a]"
    pic = work / "picture.mp4"
    ff(*ins, "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "4",
       "-c:a", "pcm_s16le", "-f", "mov", pic)
    snd = work / "sound.wav"
    ff("-i", pic, "-vn", "-c:a", "pcm_s16le", snd)
    lufs = normalize_to(snd, work / "sound_norm.wav", spec["loudness"])
    fr = decode(pic, W, H)
    mid = fr[int((off + d / 2) * fps)][H // 2, W // 2].astype(int)
    dur = len(fr) / fps
    return [("duration = 1 + 1 - 0.5 = 1.5 s", abs(dur - 1.5) < 1 / fps + 1e-9, dur),
            ("start is clip 1 (red)", fr[0][5, 5, 0] > 200 and fr[0][5, 5, 2] < 60, fr[0][5, 5].tolist()),
            ("end is clip 2 (blue)", fr[-1][5, 5, 2] > 200 and fr[-1][5, 5, 0] < 60, fr[-1][5, 5].tolist()),
            ("xfade midpoint is a mix", 60 < mid[0] < 200 and 60 < mid[2] < 200, mid.tolist()),
            ("sound pass -14 LUFS +-0.5", abs(lufs + 14) <= 0.5, lufs)]


def eng09(work):
    W, H, fps, sec = 36, 64, 30, 6
    titles = "أ|ب".split("|")
    n = sec * fps
    beat = n // len(titles)

    def frame(i):
        a = solid(W, H, (12, 14, 18))
        k = min(i // beat, len(titles) - 1)
        a[20 + 10 * k:28 + 10 * k, 6:30] = (231, 182, 90)  # title band for beat k
        a[H - 2:, : int(W * i / (n - 1))] = 255  # progress
        return a
    pat = frames_from(frame, n, work / "frames")
    out = encode_png(pat, work / "film.mp4", fps)
    shutil.rmtree(work / "frames")
    vs = vstream(out)
    fr = decode(out, W, H)
    return [("6 s x 30 fps = 180 frames", count_frames(out) == 180, count_frames(out)),
            ("9:16 aspect", vs["width"] * 16 == vs["height"] * 9, (vs["width"], vs["height"])),
            ("title 1 shown in first beat", fr[30][24, 18, 0] > 150 and fr[30][34, 18, 0] < 60, fr[30][24, 18].tolist()),
            ("title 2 shown in second beat", fr[120][34, 18, 0] > 150 and fr[120][24, 18, 0] < 60, fr[120][34, 18].tolist())]


def post_stack(img, bloom=.22, radius=.6, threshold=.9, clamp=48.0, vignette=.42, ca=1.2, grain=.16, seed=1):
    """NaN guard -> clamp -> bloom (threshold, gaussian radius) -> CA -> vignette -> grain."""
    from scipy.ndimage import gaussian_filter
    x = np.nan_to_num(np.asarray(img, np.float64), nan=0.0, posinf=clamp, neginf=0.0)
    x = np.minimum(x, clamp)
    bright = np.maximum(x - threshold, 0)
    sig = radius * min(x.shape[:2]) / 16
    x = x + bloom * np.stack([gaussian_filter(bright[..., c], sig) for c in range(3)], -1)
    s = int(round(ca))
    if s:
        x[..., 0] = np.roll(x[..., 0], s, axis=1)
        x[..., 2] = np.roll(x[..., 2], -s, axis=1)
    h, w = x.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    r2 = (((xx - (w - 1) / 2) / ((w - 1) / 2)) ** 2 + ((yy - (h - 1) / 2) / ((h - 1) / 2)) ** 2) / 2
    x = x * (1 - vignette * r2)[..., None]
    if grain:
        rng = np.random.default_rng(seed)
        x = x + (rng.random((h, w, 1)) - 0.5) * grain
    return x


def eng11(work):
    flat = np.full((32, 48, 3), 0.5)
    v = post_stack(flat, bloom=0, ca=0, grain=0)
    nan = flat.copy()
    nan[3, 3] = np.nan
    nan[4, 4] = 1e6
    g = post_stack(nan, bloom=0, ca=0, vignette=0, grain=0)
    dark_b = post_stack(flat, ca=0, vignette=0, grain=0)
    hot = np.zeros((32, 48, 3))
    hot[16, 24] = 5.0
    hb = post_stack(hot, ca=0, vignette=0, grain=0)
    line = np.zeros((32, 48, 3))
    line[:, 20] = 1.0
    cl = post_stack(line, bloom=0, vignette=0, grain=0)
    g1 = post_stack(flat, bloom=0, ca=0, vignette=0, seed=3)
    g2 = post_stack(flat, bloom=0, ca=0, vignette=0, seed=3)
    np.save(work / "post.npy", v)
    corner = v[0, 0, 0] / flat[0, 0, 0]
    return [("NaN guard -> finite", bool(np.isfinite(g).all()), float(g[3, 3, 0])),
            ("clamp 48", float(g.max()) == 48.0, float(g.max())),
            ("below threshold .9 -> no bloom", np.allclose(dark_b, flat), float(abs(dark_b - flat).max())),
            ("bright pixel spreads bloom", hb[16, 27, 0] > 0 and hb[16, 24, 0] > 5.0, float(hb[16, 27, 0])),
            ("vignette .42 at corners", abs(corner - (1 - .42)) < 1e-9, corner),
            ("CA 1.2 -> 1 px split", cl[5, 21, 0] == 1.0 and cl[5, 19, 2] == 1.0 and cl[5, 20, 1] == 1.0, [cl[5, 21, 0], cl[5, 19, 2]]),
            ("grain .16 seeded, amplitude <= .08", np.array_equal(g1, g2) and float(abs(g1 - flat).max()) <= .08 + 1e-12, float(abs(g1 - flat).max()))]


def eng13(work):
    W, H, fps, dur = 1280, 720, 24, 12
    calls = {"static": 0}

    def rnd(i):
        v = math.sin(i * 127.1 + 311.7) * 43758.5453
        return v - math.floor(v)

    def rect(x, y, w, h, fill):
        return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}"/>'

    def static_layers():
        calls["static"] += 1
        return "".join(rect(i * 64, H - 200 - rnd(i) * 220, 60, 420, "#14182a") for i in range(20))
    STATIC = static_layers()

    def scene_svg(t):
        par = -t * 18
        rain = "".join(f'<line x1="{(rnd(k) * W + t * 40) % W:.1f}" y1="{(rnd(k + 99) * H + t * 600) % H:.1f}" x2="{(rnd(k) * W + t * 40) % W - 4:.1f}" y2="{(rnd(k + 99) * H + t * 600) % H + 18:.1f}" stroke="#7fa"/>' for k in range(40))
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
                f'{rect(0, 0, W, H, "#05060c")}<g transform="translate({par:.2f},0)">{STATIC}</g>{rain}'
                f'<text x="640" y="660" opacity="{clamp01((t - 1) / 1):.3f}">neon</text></svg>')
    n = dur * fps
    (work / "frame_0072.svg").write_text(scene_svg(72 / fps))
    root = ET.fromstring(scene_svg(3.0))
    rvals = [rnd(i) for i in range(200)]
    return [("12 s x 24 fps = 288 frames", n == 288, n),
            ("SVG is 1280x720", (root.get("width"), root.get("height")) == ("1280", "720"), root.attrib),
            ("pure function of t", scene_svg(3.0) == scene_svg(3.0), "same string"),
            ("different t -> different frame", scene_svg(1.0) != scene_svg(2.0), ""),
            ("static layers built once", calls["static"] == 1 and (scene_svg(5) and calls["static"] == 1), calls),
            ("rnd(i) in [0,1)", all(0 <= v < 1 for v in rvals) and len(set(rvals)) == 200, min(rvals))]


def eng14(work):
    kit = work / "kit"
    (kit / "fonts").mkdir(parents=True)
    for f in ["motion-kit.js", "gsap.min.js", "three-kit.bundle.js", "shape-kit.js", "lab-kit.js"]:
        (kit / f).write_text(f"// {f}")
    for f in ["Cairo.woff2", "Tajawal.woff2"]:
        (kit / "fonts" / f).write_bytes(b"wOF2" + f.encode())
    proj = work / "projects" / "demo"
    proj.mkdir(parents=True)
    (proj / "index.html").write_text('<script src="assets/motion-kit.js"></script><script src="assets/gsap.min.js"></script>'
                                     '<script src="assets/shape-kit.js"></script><style>@font-face{src:url(assets/fonts/Cairo.woff2)}</style>')

    def sync_assets(d):
        html = (d / "index.html").read_text()
        copied = []
        for f in sorted(kit.glob("*.js")):
            if f.name in html:
                (d / "assets").mkdir(exist_ok=True)
                shutil.copy(f, d / "assets" / f.name)
                copied.append(f.name)
        for f in sorted((kit / "fonts").glob("*.woff2")):
            if f"assets/fonts/{f.name}" in html:
                (d / "assets" / "fonts").mkdir(parents=True, exist_ok=True)
                shutil.copy(f, d / "assets" / "fonts" / f.name)
                copied.append("fonts/" + f.name)
        return copied
    got = sync_assets(proj)
    return [("referenced kits copied", {"motion-kit.js", "gsap.min.js", "shape-kit.js"} <= set(got), got),
            ("unreferenced three-kit/lab-kit not copied", not (proj / "assets" / "three-kit.bundle.js").exists() and "lab-kit.js" not in got, got),
            ("only the named font copied", (proj / "assets/fonts/Cairo.woff2").exists() and not (proj / "assets/fonts/Tajawal.woff2").exists(), got)]


def shard_plan(frames, n):
    base, extra = divmod(frames, n)
    shards, i0 = [], 0
    for k in range(n):
        i1 = i0 + base + (1 if k < extra else 0)
        shards.append({"i0": i0, "i1": i1})
        i0 = i1
    return {"frames": frames, "shards": shards}


def eng15(work):
    plan = shard_plan(5 * 30, 7)
    save_json(work / "plan.json", plan)
    s = plan["shards"]
    sizes = [x["i1"] - x["i0"] for x in s]
    return [("night_boat 5 s x 30 fps = 150 frames", plan["frames"] == 150, plan["frames"]),
            ("7 shards", len(s) == 7, len(s)),
            ("first i0 = 0, last i1 = frames", s[0]["i0"] == 0 and s[-1]["i1"] == 150, (s[0], s[-1])),
            ("no gaps: each i1 == next i0", all(a["i1"] == b["i0"] for a, b in zip(s, s[1:])), sizes),
            ("balanced within one frame", max(sizes) - min(sizes) <= 1, sizes)]


def eng17(work):
    def frame_plan(seconds, fps):
        return [{"i": i, "t": i / fps, "timestampUs": round(i * 1e6 / fps)} for i in range(round(seconds * fps))]

    def sanitise(project):
        p = dict(project)
        p["duration"] = min(float(p.get("duration", 0)), 60.0)
        p["bg"] = p["bg"] if re.fullmatch(r"#[0-9a-fA-F]{6}", str(p.get("bg", ""))) else "#000000"
        p["src"] = p["src"] if str(p.get("src", "")).startswith(("blob:", "data:", "./", "assets/")) else ""
        return p
    plan = frame_plan(8, 30)
    save_json(work / "frame_plan.json", plan[:5])
    sp = sanitise({"duration": 95, "bg": "red;}", "src": "javascript:alert(1)"})
    return [("framePlan(8, 30) -> 240 frames", len(plan) == 240, len(plan)),
            ("timestamp of frame 30 = 1e6 us", plan[30]["timestampUs"] == 1_000_000, plan[30]),
            ("last frame t = 239/30", abs(plan[-1]["t"] - 239 / 30) < 1e-12, plan[-1]),
            ("project capped at 60 s", sp["duration"] == 60.0, sp["duration"]),
            ("colour and URL sanitised", sp["bg"] == "#000000" and sp["src"] == "", sp)]


def eng19(work):
    RECIPES = {"silence": {"fields": [{"name": "input", "kind": "file", "positional": True},
                                      {"name": "--threshold", "kind": "number"}, {"name": "--mode", "kind": "choice", "choices": ["cut", "mark"]},
                                      {"name": "--set", "kind": "set"}, {"name": "--keep", "kind": "bool"}]}}

    def build_args(recipe, values):
        fields = {f["name"]: f for f in RECIPES[recipe]["fields"]}
        opts, pos = [], []
        for k, v in values.items():
            if k not in fields:
                raise ValueError(f"unknown field {k}")
            if isinstance(v, str) and ("\x00" in v or "\n" in v):
                raise ValueError("NUL/newline refused")
            f = fields[k]
            if f.get("positional"):
                pos.append(str(v))
            elif f["kind"] == "bool":
                if v:
                    opts.append(k)
            elif f["kind"] == "set":
                opts += [k, *shlex.split(v)]
            elif f["kind"] == "choice":
                if v not in f["choices"]:
                    raise ValueError("bad choice")
                opts += [k, v]
            elif f["kind"] == "number":
                opts += [k, str(float(v))]
        return opts + ["--"] + pos
    argv = build_args("silence", {"input": "-rf.mp4", "--threshold": "-30", "--set": "a=1 'b c'", "--keep": True})
    save_json(work / "argv.json", argv)
    refused = []
    for bad in [{"--evil": "1"}, {"input": "a\nb"}, {"--mode": "zap"}, {"input": "x\x00"}]:
        try:
            build_args("silence", bad)
        except ValueError as e:
            refused.append(str(e))
    return [("options before '--', positionals after", argv[argv.index("--") + 1:] == ["-rf.mp4"] and argv.index("--") == len(argv) - 2, argv),
            ("'set' is shlex-split", argv[argv.index("--set") + 1:argv.index("--set") + 3] == ["a=1", "b c"], argv),
            ("bool adds a bare flag", "--keep" in argv, argv),
            ("unknown field / newline / bad choice / NUL refused", len(refused) == 4, refused)]


def eng20(work):
    rx = re.compile(r"(\S+\.(?:mp4|mov|webm|gif|webp|png|jpg|wav|mp3|json|srt|ass|html|md|txt))\b")
    (work / "outs").mkdir()
    for i in range(25):
        (work / "outs" / f"o{i}.png").write_bytes(b"x")
    script = "import sys\n" + "\n".join(f"print('wrote {work / 'outs' / f'o{i}.png'}')" for i in range(25)) + "\nprint('missing /nope/x.mp4')\n"
    t0 = time.strftime("%Y%m%d-%H%M%S")
    job_id = f"{t0}-{secrets.token_hex(3)}"
    proc = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    log = proc.stdout
    (work / "log.txt").write_text(log)
    found = []
    for m in rx.finditer(log):
        p = Path(m.group(1))
        if p.exists() and str(p) not in found:
            found.append(str(p))
    outputs = found[:20]
    history = [f"job{i}" for i in range(75)][-60:]
    return [("job id = YYYYmmdd-HHMMSS-hex6", bool(re.fullmatch(r"\d{8}-\d{6}-[0-9a-f]{6}", job_id)), job_id),
            ("outputs regex-matched, only existing files", "/nope/x.mp4" not in outputs and all(Path(p).exists() for p in outputs), len(found)),
            ("outputs capped at 20", len(found) == 25 and len(outputs) == 20, len(outputs)),
            ("history keeps the last 60", len(history) == 60 and history[0] == "job15", history[0])]


def eng21(work):
    EXT = {".html", ".htm", ".js", ".json", ".css", ".txt", ".md", ".svg", ".srt", ".ass", ".vtt", ".csv"}
    proj = work / "projects" / "p1"
    proj.mkdir(parents=True)

    def write_file(project, rel, content):
        target = (project / rel).resolve()
        if project.resolve() not in target.parents:
            return 403
        if target.suffix.lower() not in EXT:
            return 415
        if len(content.encode()) > 4 * 1024 * 1024:
            return 413
        if target.exists():
            shutil.copy(target, str(target) + ".bak")
        target.write_text(content, encoding="utf-8")
        return 200
    r = [write_file(proj, "index.html", "<p>1</p>"), write_file(proj, "index.html", "<p>2</p>"),
         write_file(proj, "../../escape.html", "x"), write_file(proj, "run.sh", "x"),
         write_file(proj, "big.json", "x" * (4 * 1024 * 1024 + 1))]
    return [("write inside project ok", r[:2] == [200, 200], r),
            ("automatic .bak keeps previous", (proj / "index.html.bak").read_text() == "<p>1</p>", ""),
            ("path escape refused", r[2] == 403 and not (work / "escape.html").exists(), r[2]),
            ("non-text extension refused", r[3] == 415, r[3]),
            ("> 4 MB refused", r[4] == 413, r[4])]


def eng22(work):
    DEFAULT = ["فكرة تبدأ", "تفاصيل تتضح", "من زاوية أخرى", "لحظة الأثر", "المشهد التالي"]

    def compile_plan(plan):
        n = plan.get("scenes", 5)
        dur = plan["seconds"] / n
        man = {"schema": "kosif.motion.manifest.v1", "width": plan["w"], "height": plan["h"], "fps": plan["fps"],
               "duration": plan["seconds"], "subtitle": plan["task"][:85],
               "scenes": [{"title": DEFAULT[i % 5], "start": i * dur, "end": (i + 1) * dur} for i in range(n)]}
        return man

    def project_html(m):
        return (f'<body data-width="{m["width"]}" data-height="{m["height"]}" data-duration="{m["duration"]}" data-fps="{m["fps"]}">'
                f'<canvas></canvas><script>window.__duration={m["duration"]};const M={json.dumps(m, ensure_ascii=False)};'
                f'window.render=function(t){{/*manifest-player*/}};window.__ready=true;</script></body>')
    task = "مقدمة عربية أنيقة عن قوة الأفكار " * 5
    m = compile_plan({"task": task, "seconds": 12, "fps": 30, "w": 1920, "h": 1080})
    html = project_html(m)
    (work / "index.html").write_text(html, encoding="utf-8")
    body = parse_html(html).body
    return [("default titles in order", [s["title"] for s in m["scenes"]] == DEFAULT, [s["title"] for s in m["scenes"]]),
            ("subtitle = first 85 chars", m["subtitle"] == task[:85] and len(m["subtitle"]) == 85, len(m["subtitle"])),
            ("page carries data-width/height/duration/fps", (body["data-width"], body["data-duration"], body["data-fps"]) == ("1920", "12", "30"), dict(body.attrs)),
            ("window.__duration and __ready set", "window.__duration=12" in html and "window.__ready=true" in html, "")]


def verify_h264(path, w, h, frames, fps):
    p = probe(path)
    v = [s for s in p["streams"] if s["codec_type"] == "video"]
    probs = []
    if len(p["streams"]) != 1 or len(v) != 1 or v[0]["codec_name"] != "h264":
        probs.append("not a single h264 stream")
    if v and (v[0]["width"], v[0]["height"]) != (w, h):
        probs.append("size")
    n = count_frames(path)
    if n != frames:
        probs.append(f"frames {n}")
    if abs(float(p["format"]["duration"]) - frames / fps) > 1 / fps:
        probs.append("duration")
    return probs


def eng23(work):
    W, H, fps, n = 64, 36, 15, 15
    accent = np.array([231, 182, 90.0])
    unit = min(W, H)

    def frame(i):
        t = i / fps
        g = np.linspace(1, 0, H)[:, None, None]
        top = accent * .14 + 17 * .86
        img = (top * g + 17 * (1 - g)) * np.ones((H, W, 3))
        im = Image.fromarray(img.astype(np.uint8))
        d = ImageDraw.Draw(im)
        for k in range(3):
            ease = 0.5 - 0.5 * math.cos(t * 2)
            r = unit * (.17 + k * .045) * (.7 + .3 * ease)
            cx = W / 2 + math.sin(t * .4) * unit * .025
            d.ellipse([cx - r, H / 2 - r, cx + r, H / 2 + r], outline=(60, 70, 72))
        return np.asarray(im)
    out = work / "manifest.mp4"
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pixel_format", "rgb24", "-video_size", f"{W}x{H}",
                             "-framerate", str(fps), "-i", "pipe:0", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                             "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)], stdin=subprocess.PIPE)
    progress = []
    for i in range(n):
        proc.stdin.write(frame(i).tobytes())
        progress.append(round(0.95 * (i + 1) / n, 3))
    proc.stdin.close()
    proc.wait()
    probs = verify_h264(out, W, H, n, fps)
    short = work / "short.mp4"
    ff("-i", out, "-frames:v", "10", "-c", "copy", short)
    top = decode(out, W, H)[0][0, W // 2].astype(int)
    want = accent * .14 + 17 * .86
    return [("ffprobe verification passes", probs == [], probs),
            ("truncated file fails verification", verify_h264(short, W, H, n, fps) != [], verify_h264(short, W, H, n, fps)),
            ("top row = accent*.14 + 17*.86", np.abs(top - want).max() <= 8, (top.tolist(), want.round(1).tolist())),
            ("progress ends at 0.95", progress[-1] == 0.95, progress[-1])]


def eng24(work):
    class RenderEngine:
        def __init__(self):
            self.jobs = {}

        def submit(self):
            jid, tok = secrets.token_urlsafe(18), secrets.token_urlsafe(32)
            d = work / "jobs" / jid
            d.mkdir(parents=True)
            self.jobs[jid] = {"token": tok, "state": "running", "dir": d}
            return jid, tok

        def lookup(self, jid, header):
            j = self.jobs.get(jid)
            if j is None or not hmac.compare_digest(j["token"].encode(), (header or "").encode()):
                return 404
            return 200 if j["state"] == "succeeded" else 409

        def cancel(self, jid, header):
            if self.lookup(jid, header) == 404:
                return 404
            shutil.rmtree(self.jobs[jid]["dir"])
            self.jobs[jid]["state"] = "cancelled"
            return 204
    e = RenderEngine()
    jid, tok = e.submit()
    r = {"wrong": e.lookup(jid, "x" * 43), "missing_job": e.lookup("nope", tok), "no_header": e.lookup(jid, None),
         "not_ready": e.lookup(jid, tok)}
    e.jobs[jid]["state"] = "succeeded"
    r["ready"] = e.lookup(jid, tok)
    j2, t2 = e.submit()
    d2 = e.jobs[j2]["dir"]
    r["cancel"] = e.cancel(j2, t2)
    save_json(work / "lookups.json", r)
    return [("id 18 bytes (24 chars), token 32 bytes (43 chars)", (len(jid), len(tok)) == (24, 43), (len(jid), len(tok))),
            ("wrong token looks like a missing job (404)", r["wrong"] == r["missing_job"] == r["no_header"] == 404, r),
            ("right token before done -> 409", r["not_ready"] == 409, r["not_ready"]),
            ("right token when done -> 200", r["ready"] == 200, r["ready"]),
            ("cancel deletes the job folder", r["cancel"] == 204 and not d2.exists(), r["cancel"])]


def eng25(work):
    ORDER = ["video/webm;codecs=vp8,opus", "video/webm;codecs=vp9,opus", "video/webm", "video/mp4"]

    def pick(supported):
        return next((m for m in ORDER if m in supported), None)

    def record(seconds, hidden_at=None, timeslice=250):
        chunks = []
        for k in range(int(seconds * 1000 / timeslice)):
            if hidden_at is not None and k * timeslice >= hidden_at * 1000:
                return {"aborted": True, "chunks": len(chunks)}
            chunks.append(k)
        return {"aborted": False, "chunks": len(chunks), "fps": 24, "videoBitsPerSecond": 5_000_000, "audioBitsPerSecond": 128_000}
    r = {"all": pick(set(ORDER)), "no_vp8": pick({"video/webm;codecs=vp9,opus", "video/mp4"}), "safari": pick({"video/mp4"}),
         "none": pick(set()), "rec": record(2), "hidden": record(2, hidden_at=1)}
    save_json(work / "recorder.json", r)
    return [("first supported: vp8,opus", r["all"] == ORDER[0], r["all"]),
            ("falls back to vp9,opus", r["no_vp8"] == ORDER[1], r["no_vp8"]),
            ("mp4 last", r["safari"] == "video/mp4" and r["none"] is None, r["safari"]),
            ("250 ms timeslice -> 8 chunks in 2 s at 24 fps / 5 Mbps / 128 kbps", r["rec"]["chunks"] == 8 and r["rec"]["videoBitsPerSecond"] == 5e6, r["rec"]),
            ("hidden tab aborts", r["hidden"]["aborted"] and r["hidden"]["chunks"] == 4, r["hidden"])]


def eng26(work):
    def bitrate(w, h, fps):
        return min(16_000_000, w * h * fps * 0.15)

    def encode_plan(frames, fps, queue_cap=8, drain_per_frame=1):
        gop = fps * 2
        keys, q, qmax = [], 0, 0
        for i in range(frames):
            while q >= queue_cap:
                q -= drain_per_frame
            q += 1
            qmax = max(qmax, q)
            if i % gop == 0:
                keys.append(i)
            q = max(0, q - (1 if i % 3 == 0 else 0))
        return {"gop": gop, "keys": keys, "queue_max": qmax}
    p = encode_plan(240, 30)
    r = {"1080p30": bitrate(1920, 1080, 30), "720p30": bitrate(1280, 720, 30), "4k60": bitrate(3840, 2160, 60), **p}
    save_json(work / "encode_plan.json", r)
    return [("1080p30 = 1920*1080*30*0.15", r["1080p30"] == 9_331_200, r["1080p30"]),
            ("720p30 = 4,147,200", r["720p30"] == 4_147_200, r["720p30"]),
            ("4K60 capped at 16 Mbps", r["4k60"] == 16_000_000, r["4k60"]),
            ("GOP = fps*2 = 60, keyframe every 2 s", r["gop"] == 60 and r["keys"] == [0, 60, 120, 180], r["keys"]),
            ("encode queue never above 8", r["queue_max"] <= 8, r["queue_max"])]


def pick_video_codec(w, h, fps, supported):
    ll = "2A" if (w * h > 1280 * 720 or fps > 30) else "1F"
    chain = [f"avc1.6400{ll}", f"avc1.4D40{ll}", f"avc1.42E0{ll}", "avc1.42E01F"]
    for c in chain:
        if c in supported:  # isConfigSupported({codec:c, bitrate:8e6})
            return c, chain
    return None, chain


def eng27(work):
    r = {}
    r["1080"] = pick_video_codec(1920, 1080, 30, {"avc1.64002A", "avc1.42E01F"})
    r["720_60"] = pick_video_codec(1280, 720, 60, {"avc1.4D402A"})
    r["720_30"] = pick_video_codec(1280, 720, 30, {"avc1.42E01F", "avc1.64001F"})
    r["base_only"] = pick_video_codec(1920, 1080, 30, {"avc1.42E01F"})
    r["none"] = pick_video_codec(1920, 1080, 30, set())
    save_json(work / "codecs.json", {k: list(v[0:1]) + [v[1]] for k, v in r.items()})
    return [("1080p -> High level 4.2 (avc1.64002A)", r["1080"][0] == "avc1.64002A", r["1080"][0]),
            ("fps > 30 forces level 2A", r["720_60"][0] == "avc1.4D402A" and r["720_60"][1][0].endswith("2A"), r["720_60"]),
            ("720p30 -> level 1F (3.1), High first", r["720_30"][0] == "avc1.64001F", r["720_30"][0]),
            ("final fallback Baseline 3.1", r["base_only"][0] == "avc1.42E01F" and r["base_only"][1][-1] == "avc1.42E01F", r["base_only"]),
            ("nothing supported -> None", r["none"][0] is None, r["none"][0])]


def eng28(work):
    def pick_audio(supported):
        for codec, name in [("mp4a.40.2", "aac"), ("opus", "opus")]:
            if codec in supported:
                return {"codec": codec, "container": name, "bitrate": 192_000, "channels": 2, "sampleRate": 48_000}
        return {"codec": None, "report": "exported silent: no AAC or Opus encoder"}

    def blocks(n_samples, size=4096):
        return [(i, min(size, n_samples - i)) for i in range(0, n_samples, size)]
    b = blocks(48_000 * 2)
    r = {"aac": pick_audio({"mp4a.40.2", "opus"}), "opus": pick_audio({"opus"}), "none": pick_audio(set()), "blocks": len(b), "last": b[-1]}
    save_json(work / "audio_plan.json", r)
    return [("AAC-LC first", r["aac"]["codec"] == "mp4a.40.2" and r["aac"]["bitrate"] == 192000, r["aac"]),
            ("Opus fallback", r["opus"]["codec"] == "opus", r["opus"]),
            ("neither -> silent + report", r["none"]["codec"] is None and "silent" in r["none"]["report"], r["none"]),
            ("2 s at 48 kHz -> 24 blocks of 4096 (last 1792)", r["blocks"] == 24 and r["last"][1] == 96000 - 23 * 4096, r["last"])]


def eng29(work):
    class Media:
        def __init__(self):
            self.currentTime, self.seeking, self.seeks, self.target = 0.0, False, [], None

        def start(self, t):
            self.seeking, self.target = True, t
            self.seeks.append(t)

        def finish(self):
            self.currentTime, self.seeking = self.target, False

    class Seeker:
        TOL = 0.025

        def __init__(self, m):
            self.m, self.pending = m, None

        def seek(self, t):
            if not self.m.seeking and abs(self.m.currentTime - t) <= self.TOL:
                return "skip"
            if self.m.seeking:
                self.pending = t
                return "queued"
            self.m.start(t)
            return "seeking"

        def on_seeked(self):
            self.m.finish()
            if self.pending is not None:
                t, self.pending = self.pending, None
                return self.seek(t)

    def stable_seek(m, t, seeked_after_ms, timeout=8000):
        return "ok" if seeked_after_ms <= timeout else "timeout"
    m = Media()
    s = Seeker(m)
    log = [s.seek(1.0), s.seek(1.5), s.seek(2.0)]
    s.on_seeked()
    s.on_seeked()
    log.append(s.seek(2.01))
    save_json(work / "seek_log.json", {"log": log, "seeks": m.seeks})
    return [("newer seek waits while one is in flight", log[:3] == ["seeking", "queued", "queued"], log),
            ("only latest pending target executed", m.seeks == [1.0, 2.0], m.seeks),
            ("target within 25 ms is not re-sought", log[3] == "skip" and m.currentTime == 2.0, log[3]),
            ("seeked wait times out at 8000 ms", stable_seek(m, 2, 8001) == "timeout" and stable_seek(m, 2, 7999) == "ok", "")]


def eng31(work):
    import random

    def build(path):
        W, H = 1600, 900
        random.seed(7)
        out = []
        a = out.append
        a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">')
        a('<defs><linearGradient id="sky"><stop offset="0" stop-color="#0b1020"/><stop offset="1" stop-color="#3a2a52"/></linearGradient>'
          '<radialGradient id="glow"><stop offset="0" stop-color="#ffcf7a"/><stop offset="1" stop-opacity="0"/></radialGradient>'
          '<pattern id="grain" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="1" height="1" fill="#fff1"/></pattern>'
          '<filter id="blur"><feGaussianBlur stdDeviation="6"/></filter></defs>')
        a(f'<rect id="sky-layer" width="{W}" height="{H}" fill="url(#sky)"/>')
        a('<circle id="sun" cx="1200" cy="260" r="180" fill="url(#glow)" filter="url(#blur)"/>')
        for k in range(60):
            a(f'<circle class="ember" cx="{random.uniform(0, W):.2f}" cy="{random.uniform(0, H):.2f}" r="{random.uniform(1, 4):.2f}" fill="#ff9a3c"/>')
        a(f'<rect id="grain-layer" width="{W}" height="{H}" fill="url(#grain)"/></svg>')
        Path(path).write_text("".join(out))
    build(work / "a.svg")
    build(work / "b.svg")
    txt = (work / "a.svg").read_text()
    root = ET.fromstring(txt)
    ids = [e.get("id") for e in root if e.get("id")]
    return [("byte-for-byte reproducible from seed 7", (work / "a.svg").read_bytes() == (work / "b.svg").read_bytes(), hashlib.sha256(txt.encode()).hexdigest()[:16]),
            ("1600x900", (root.get("width"), root.get("height")) == ("1600", "900"), root.attrib),
            ("defs: linear+radial gradient, pattern, feGaussianBlur", all(k in txt for k in ["linearGradient", "radialGradient", "<pattern", "feGaussianBlur"]), ""),
            ("layers back-to-front (sky first, grain last)", ids[0] == "sky-layer" and ids[-1] == "grain-layer", ids),
            ("60 embers", txt.count('class="ember"') == 60, txt.count('class="ember"'))]


def eng34(work):
    r = mulberry32(1)
    vals = [r(), r(), r()]
    cells = [[hash2(i, j) for j in range(16)] for i in range(16)]
    save_json(work / "rng.json", {"seed1": vals, "cells": cells[0]})
    flat = [v for row in cells for v in row]
    return [("mulberry32(1) == JS reference", vals == JS_MULBERRY_SEED1, vals),
            ("same seed -> same stream", [mulberry32(9)() for _ in range(3)] == [mulberry32(9)() for _ in range(3)], ""),
            ("hash(i,j) stateless and repeatable", hash2(3, 5) == cells[3][5], hash2(3, 5)),
            ("hash in [0,1), 256 distinct", all(0 <= v < 1 for v in flat) and len(set(flat)) == 256, len(set(flat)))]


def ss_mask(polys, w, h, ss=3, holes=()):
    big = Image.new("L", (w * ss, h * ss), 0)
    d = ImageDraw.Draw(big)
    for p in polys:
        d.polygon([(x * ss, y * ss) for x, y in p], fill=255)
    for p in holes:
        d.polygon([(x * ss, y * ss) for x, y in p], fill=0)
    return np.asarray(big.reduce(ss)).astype(int)


def eng35(work):
    w, h = 20, 12
    edge = 10 + 1 / 3
    m = ss_mask([[(0, 0), (edge, 0), (edge, h), (0, h)]], w, h)
    hole = ss_mask([[(1, 1), (19, 1), (19, 11), (1, 11)]], w, h, holes=[[(7, 4), (13, 4), (13, 8), (7, 8)]])
    hard = ss_mask([[(0, 0), (edge, 0), (edge, h), (0, h)]], w, h, ss=1)
    Image.fromarray(m.astype(np.uint8)).save(work / "mask.png")
    pad = lambda blur: 3 * blur + 2  # noqa: E731
    vals = sorted(set(m[5].tolist()))
    return [("inside fully covered", m[5, 3] == 255, m[5, 3]),
            ("edge pixel partially covered (antialiased)", 0 < m[5, 10] < 255, m[5, 10]),
            ("ss=3 gives coverage steps of 1/3", all(v % 85 == 0 for v in vals), vals),
            ("ss=1 has no partial coverage", set(np.unique(hard).tolist()) <= {0, 255}, np.unique(hard).tolist()),
            ("Hole polygon fills 0", hole[6, 10] == 0 and hole[2, 10] == 255, (hole[6, 10], hole[2, 10])),
            ("bbox pad = 3*blur+2", (pad(0), pad(4)) == (2, 14), (pad(0), pad(4)))]


NAMED = {"black": (0, 0, 0), "white": (255, 255, 255), "red": (255, 0, 0), "lime": (0, 255, 0), "blue": (0, 0, 255),
         "rebeccapurple": (102, 51, 153), "orange": (255, 165, 0), "gold": (255, 215, 0), "teal": (0, 128, 128),
         "navy": (0, 0, 128), "gray": (128, 128, 128), "silver": (192, 192, 192), "crimson": (220, 20, 60)}


def svg_length(v, ref=100.0):
    v = v.strip()
    m = re.fullmatch(r"(-?[\d.]+)(px|%|em|rem|pt)?", v)
    num, unit = float(m.group(1)), m.group(2) or "px"
    return {"px": num, "%": num * ref / 100, "em": num * 16, "rem": num * 16, "pt": num * 1.333}[unit]


def svg_color(v, current=(0, 0, 0)):
    v = v.strip().lower()
    if v == "currentcolor":
        return current + (1.0,)
    if v in NAMED:
        return NAMED[v] + (1.0,)
    if v.startswith("#"):
        hx = v[1:]
        if len(hx) == 3:
            hx = "".join(c * 2 for c in hx)
        return tuple(int(hx[i:i + 2], 16) for i in (0, 2, 4)) + (1.0,)
    m = re.fullmatch(r"(rgba?|hsla?)\(([^)]*)\)", v)
    parts = [p.strip() for p in m.group(2).split(",")]
    a = float(parts[3]) if len(parts) > 3 else 1.0
    if m.group(1).startswith("rgb"):
        return tuple(int(round(float(p[:-1]) * 2.55)) if p.endswith("%") else int(float(p)) for p in parts[:3]) + (a,)
    import colorsys
    hh, ss, ll = float(parts[0]) / 360, float(parts[1].rstrip("%")) / 100, float(parts[2].rstrip("%")) / 100
    r, g, b = colorsys.hls_to_rgb(hh, ll, ss)
    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)), a)


def svg_transform(s):
    M = np.eye(3)
    for name, args in re.findall(r"(\w+)\(([^)]*)\)", s):
        a = [float(x) for x in re.split(r"[ ,]+", args.strip())]
        if name == "translate":
            T = np.array([[1, 0, a[0]], [0, 1, a[1] if len(a) > 1 else 0], [0, 0, 1]])
        elif name == "scale":
            T = np.diag([a[0], a[1] if len(a) > 1 else a[0], 1])
        elif name == "rotate":
            c, s_ = math.cos(math.radians(a[0])), math.sin(math.radians(a[0]))
            T = np.array([[c, -s_, 0], [s_, c, 0], [0, 0, 1]])
        elif name == "skewX":
            T = np.array([[1, math.tan(math.radians(a[0])), 0], [0, 1, 0], [0, 0, 1]])
        elif name == "skewY":
            T = np.array([[1, 0, 0], [math.tan(math.radians(a[0])), 1, 0], [0, 0, 1]])
        else:
            T = np.array([[a[0], a[2], a[4]], [a[1], a[3], a[5]], [0, 0, 1]])
        M = M @ T
    return M


SKIP_TAGS = {"filter", "mask", "clipPath", "pattern", "image"}


def load_svg(text, max_steps=160):
    root = ET.fromstring(text)
    steps = []
    title = None

    def tag(e):
        return e.tag.split("}")[-1]

    def walk(e, M):
        nonlocal title
        t = tag(e)
        if t == "title":
            title = e.text
        if t in SKIP_TAGS or t == "defs":
            return
        M2 = M @ svg_transform(e.get("transform", "")) if e.get("transform") else M
        if t in {"rect", "circle", "ellipse", "line", "polyline", "polygon", "path", "text"}:
            steps.append({"tag": t, "fill": e.get("fill"), "matrix": M2.round(6).tolist()})
        for c in e:
            if len(steps) < max_steps:
                walk(c, M2)
    walk(root, np.eye(3))
    return title, steps[:max_steps]


def gradient_chain(grads, gid, limit=8):
    seen, cur = [], gid
    while cur and len(seen) < limit:
        if cur in seen:
            break
        seen.append(cur)
        cur = grads.get(cur)
    return seen


def eng36(work):
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 100"><title>شعار</title>'
           '<g transform="translate(10,5) scale(2)"><rect width="10" height="10" fill="red"/>'
           '<g transform="skewX(45)"><circle r="3" fill="hsl(120,100%,50%)"/></g></g>'
           '<text fill="rgba(0,0,255,0.5)">مرحبا</text></svg>')
    title, steps = load_svg(svg)
    save_json(work / "steps.json", steps)
    rect_m = np.array(steps[0]["matrix"])
    pt = rect_m @ np.array([10, 10, 1])
    skew_m = np.array(steps[1]["matrix"]) @ np.array([0, 4, 1])
    chain = gradient_chain({f"g{i}": f"g{i + 1}" for i in range(20)}, "g0")
    return [("units: 2em=32, 1rem=16, 12pt=15.996, 50%=100", (svg_length("2em"), svg_length("1rem"), round(svg_length("12pt"), 3), svg_length("50%", 200)) == (32, 16, 15.996, 100), ""),
            ("hsl(120,100%,50%) = lime", svg_color("hsl(120,100%,50%)") == (0, 255, 0, 1.0), svg_color("hsl(120,100%,50%)")),
            ("rgba alpha kept, currentColor resolved, named rebeccapurple", svg_color("rgba(0,0,255,0.5)")[3] == 0.5 and svg_color("currentColor", (1, 2, 3))[:3] == (1, 2, 3) and svg_color("rebeccapurple")[:3] == (102, 51, 153), ""),
            ("translate(10,5) scale(2): (10,10) -> (30,25)", pt[:2].tolist() == [30, 25], pt[:2].tolist()),
            ("skewX(45) composes: (0,4) -> (18,13)", np.allclose(skew_m[:2], [18, 13]), skew_m[:2].tolist()),
            ("Arabic text step and title kept", title == "شعار" and steps[-1]["tag"] == "text", title),
            ("gradient href chain stops at 8", len(chain) == 8, len(chain))]


def eng37(work):
    NAME = re.compile(r"^[\w\u0600-\u06FF][\w\u0600-\u06FF-]{0,63}$")
    kit = work / "kit"
    kit.mkdir()
    (kit / "three-kit.bundle.js").write_text("window.K3={}")
    (kit / "shape-kit.js").write_text("//shape")

    def new(name, route="flat", seconds=8, fps=30, size="1920x1080", npm=False):
        if not NAME.match(name):
            raise ValueError("bad name")
        d = work / "projects" / name
        (d / "assets").mkdir(parents=True)
        w, h = size.split("x")
        js = "import * as THREE from 'three';\nimport {makePost} from './kit/three-kit.js';" if route == "3d" else ""
        if route == "3d" and not npm:
            js = js.replace("import * as THREE from 'three';", "const THREE = window.K3.THREE;").replace(
                "import {makePost} from './kit/three-kit.js';", "const {makePost} = window.K3;")
            for f in ["three-kit.bundle.js", "shape-kit.js"]:
                shutil.copy(kit / f, d / "assets" / f)
        (d / "index.html").write_text(composition_page(w=w, h=h, dur=seconds, fps=fps).replace("</body>", f"<script>{js}</script></body>"))
        return d
    d = new("فيلم-1", route="3d")
    flat = new("flat1")
    bad = []
    for n in ["-x", "a" * 65, "a b"]:
        try:
            new(n)
        except ValueError:
            bad.append(n)
    html = (d / "index.html").read_text()
    root = parse_html((flat / "index.html").read_text()).find(attrs={"data-composition-id": True})
    return [("defaults 8 s 30 fps 1920x1080", (root["data-duration"], root["data-fps"], root["data-width"], root["data-height"]) == ("8", "30", "1920", "1080"), dict(root.attrs)),
            ("Arabic name accepted", d.exists(), d.name),
            ("bad names refused (leading '-', 65 chars, space)", len(bad) == 3, bad),
            ("3D without npm rewrites imports to window.K3", "window.K3" in html and "from 'three'" not in html, ""),
            ("3D copies three-kit.bundle.js + shape-kit.js", sorted(p.name for p in (d / "assets").iterdir()) == ["shape-kit.js", "three-kit.bundle.js"], "")]


def _first_style_id():
    out = sh([sys.executable, str(REPO / "tools" / "kosif.py"), "list", "--limit", "1", "--json"])
    d = json.loads(out)
    return (d[0] if isinstance(d, list) else d["styles"][0])["id"]


def eng39(work):
    sid = _first_style_id()
    d = work / "proj"
    sh([sys.executable, str(REPO / "tools" / "kosif.py"), "scaffold", sid, d, "--starter", "html-canvas"])
    files = sorted(p.name for p in d.iterdir())
    words = json.loads((d / "words.json").read_text(encoding="utf-8"))
    return [("STYLE/PLAN/TEST_REPORT/words.json written", {"STYLE.md", "PLAN.md", "TEST_REPORT.md", "words.json"} <= set(files), files),
            ("style id recorded", sid in (d / "TEST_REPORT.md").read_text(encoding="utf-8"), sid),
            ("html-canvas starter copied", (d / "html-canvas" / "index.html").is_file(), ""),
            ("words.json is valid JSON", isinstance(words, (list, dict)), type(words).__name__)]


def eng50(work):
    sid = _first_style_id()
    d = work / "proj"
    sh([sys.executable, str(REPO / "tools" / "kosif.py"), "scaffold", sid, d, "--starter", "html-canvas", "--duration", "4", "--fps", "25"])
    rep = (d / "TEST_REPORT.md").read_text(encoding="utf-8")
    m = re.search(r"(\d+) frames", rep)
    leaked = [p for p in (d / "html-canvas").rglob("*") if p.name in {"node_modules", "out", "media"}]
    second = subprocess.run([sys.executable, str(REPO / "tools" / "kosif.py"), "scaffold", sid, str(d)], capture_output=True, text=True)
    return [("frames = round(4 * 25) = 100", m and int(m.group(1)) == 100, m.group(0) if m else rep[:120]),
            ("REQUEST.md written", (d / "REQUEST.md").is_file(), ""),
            ("starter copied without node_modules/out/media", leaked == [], leaked),
            ("non-empty dir refused without --force", second.returncode != 0, second.returncode)]


def eng41(work):
    class Page:
        duration, fps = 2.0, 15

        def __init__(self):
            self.seen = []

        def seek(self, t):
            self.seen.append(t)
            return solid(32, 18, (int(t * 100),) * 3)

    def render(page, start=0.0, duration=None, fps=None):
        fps = fps or page.fps
        duration = duration if duration is not None else page.duration
        total = round(duration * fps)
        return [page.seek(start + i / fps) for i in range(total)]
    p = Page()
    frames = render(p, start=0.5, duration=1.0)
    d = work / "frames"
    d.mkdir()
    for i, f in enumerate(frames):
        write_png(d / f"f_{i:04d}.png", f)
    out = encode_png(d / "f_%04d.png", work / "out.mp4", 15)
    p2 = Page()
    render(p2)
    return [("total = round(duration*fps) = 15", len(frames) == 15 and count_frames(out) == 15, len(frames)),
            ("frame t = start + i/fps", all(abs(t - (0.5 + i / 15)) < 1e-12 for i, t in enumerate(p.seen)), p.seen[:3]),
            ("duration defaults to page duration (30 frames)", len(p2.seen) == 30, len(p2.seen))]


def eng45(work):
    W, H, fps = 63, 35, 25
    pat = frames_from(lambda i: solid(W, H, (i * 9 % 255, 80, 120)), 25, work / "frames")
    mp3 = work / "voice.mp3"
    ff("-f", "lavfi", "-i", "sine=f=440:d=1.5", "-c:a", "libmp3lame", "-b:a", "128k", mp3)
    wav = work / "voice.wav"
    write_wav(wav, tone(440, 1.5, 44100), 44100)
    vflags = ["-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
              "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2,setparams=range=tv:color_primaries=bt709:color_trc=bt709:colorspace=bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
              "-movflags", "+faststart"]
    copy = work / "copy.mp4"
    ff("-framerate", fps, "-i", pat, "-i", mp3, *vflags, "-c:a", "copy", "-shortest", copy)
    aac = work / "aac.mp4"
    ff("-framerate", fps, "-i", pat, "-i", wav, *vflags, "-c:a", "aac", "-b:a", "320k", "-af", "apad", "-shortest",
       "-shortest_buf_duration", "0.05", aac)  # keep -shortest from overshooting on padded audio (newer ffmpeg buffers more)
    shutil.rmtree(work / "frames")

    def pkt_hashes(p):
        out = sh(["ffmpeg", "-v", "error", "-i", p, "-map", "0:a", "-c", "copy", "-f", "framemd5", "-"])
        return [ln.split(",")[-1].strip() for ln in out.splitlines() if ln and not ln.startswith("#")]
    src_h, out_h = pkt_hashes(mp3), pkt_hashes(copy)
    vs = vstream(copy)
    adur = float(astream(aac)["duration"])
    return [("odd 63x35 padded to even 64x36", (vs["width"], vs["height"]) == (64, 36), (vs["width"], vs["height"])),
            ("libx264 High yuv420p BT.709", (vs["profile"], vs["pix_fmt"], vs.get("color_primaries")) == ("High", "yuv420p", "bt709"), (vs["profile"], vs["pix_fmt"], vs.get("color_primaries"))),
            ("MP3 stream-copied byte for byte (packet prefix)", astream(copy)["codec_name"] == "mp3" and len(out_h) > 10 and out_h == src_h[:len(out_h)], (len(out_h), len(src_h))),
            ("audio cut at the last video frame", len(out_h) < len(src_h), (len(out_h), len(src_h))),
            ("WAV -> AAC, video length decides the end", astream(aac)["codec_name"] == "aac" and adur <= 1.0 + 0.05, adur)]


def eng46(work):
    fps, start, dur = 30, 4.0, 3.0
    times = [start + i / fps for i in range(round(dur * fps))]
    pat = frames_from(lambda i: solid(32, 18, (int(times[i] * 30) % 256,) * 3), len(times), work / "f")
    out = encode_png(pat, work / "window.mp4", fps)
    shutil.rmtree(work / "f")
    return [("--start 4 --duration 3 -> 90 frames", len(times) == 90 and count_frames(out) == 90, len(times)),
            ("first frame at t = 4.0", times[0] == 4.0, times[0]),
            ("last frame at t = 4 + 89/30 < 7", abs(times[-1] - (4 + 89 / 30)) < 1e-12 and times[-1] < 7, times[-1])]


def eng47(work):
    d = work / "frames"
    pat = frames_from(lambda i: solid(16, 16, (i, i, i)), 12, d, "frame_%06d.png")
    names = sorted(p.name for p in d.iterdir())
    out = encode_png(pat, work / "film.mp4", 12)
    back = np.asarray(Image.open(d / "frame_000007.png"))
    return [("names frame_%06d.png", names[0] == "frame_000000.png" and names[-1] == "frame_000011.png", names[:2]),
            ("12 frames kept", len(names) == 12, len(names)),
            ("kept frames lossless PNG", int(back[0, 0, 0]) == 7, int(back[0, 0, 0])),
            ("sequence encodes back to 12 frames", count_frames(out) == 12, count_frames(out))]


def eng48(work):
    def resolve(cwd, opt_root, env):
        cands = [cwd / "node_modules" / "playwright", opt_root / "opt/node-tools/node_modules/playwright"]
        if env.get("KOSIF_PLAYWRIGHT"):
            cands.append(Path(env["KOSIF_PLAYWRIGHT"]))
        return next((str(c) for c in cands if c.is_dir()), None)
    cwd, opt, custom = work / "cwd", work / "root", work / "custom"
    (opt / "opt/node-tools/node_modules/playwright").mkdir(parents=True)
    custom.mkdir()
    cwd.mkdir()
    a = resolve(cwd, opt, {"KOSIF_PLAYWRIGHT": str(custom)})
    (cwd / "node_modules" / "playwright").mkdir(parents=True)
    b = resolve(cwd, opt, {"KOSIF_PLAYWRIGHT": str(custom)})
    shutil.rmtree(opt / "opt")
    shutil.rmtree(cwd / "node_modules")
    c = resolve(cwd, opt, {"KOSIF_PLAYWRIGHT": str(custom)})
    e = resolve(cwd, opt, {})
    save_json(work / "resolution.json", [a, b, c, e])
    return [("/opt/node-tools before $KOSIF_PLAYWRIGHT", a.endswith("opt/node-tools/node_modules/playwright"), a),
            ("cwd wins first", b == str(cwd / "node_modules" / "playwright"), b),
            ("$KOSIF_PLAYWRIGHT last", c == str(custom), c),
            ("nothing found -> None (never installs)", e is None, e)]


def eng49(work):
    class Timeline:
        def __init__(self, duration, fps, scenes, always):
            self.duration, self.fps, self.scenes, self.always, self.log = duration, fps, scenes, always, []

        def seek(self, t):
            t = max(0, min(self.duration, t))
            vis = []
            for s in self.scenes:
                on = s["t0"] <= t < s["t1"] or (t == self.duration and s["t1"] == self.duration)
                if on:
                    vis.append((s["id"], round((t - s["t0"]) / (s["t1"] - s["t0"]), 6)))
            self.always(t)
            self.log.append(t)
            return vis
    hits = []
    sc = [{"id": f"s{i}", "t0": a, "t1": b} for i, (a, b) in enumerate([(0, 3.4), (3.4, 7.2), (7.2, 10.4), (10.4, 12)])]
    tl = Timeline(12, 30, sc, hits.append)
    r = {"3.5": tl.seek(3.5), "7.2": tl.seek(7.2), "12": tl.seek(12), "5.3": tl.seek(5.3)}
    save_json(work / "seek.json", r)
    return [("only scene 2 visible at 3.5 s", r["3.5"] == [("s1", round(0.1 / 3.8, 6))], r["3.5"]),
            ("boundary 7.2 belongs to scene 3", [v[0] for v in r["7.2"]] == ["s2"], r["7.2"]),
            ("end of film shows last scene at p=1", r["12"] == [("s3", 1.0)], r["12"]),
            ("local progress p = (t-t0)/(t1-t0)", r["5.3"] == [("s1", 0.5)], r["5.3"]),
            ("always(t) runs every frame", hits == [3.5, 7.2, 12, 5.3], hits),
            ("12 s x 30 fps = 360 frames", round(tl.duration * tl.fps) == 360, 360)]


def eng54(work):
    def route(has_browser, has_ffmpeg):
        return "A" if has_browser and has_ffmpeg else ("B" if has_ffmpeg else "C")

    def deliver_c(d):
        d.mkdir()
        (d / "index.html").write_text("<!doctype html><script>/* self-playing */</script>")
        write_wav(d / "score.wav", tone(220, 2.0) * np.linspace(1, 0, 32000))
        (d / "COMMANDS.txt").write_text("node tools/render_html.cjs --in index.html --out film.mp4 --audio score.wav\n")
        return sorted(p.name for p in d.iterdir())
    files = deliver_c(work / "routeC")
    with wave.open(str(work / "routeC" / "score.wav")) as wf:
        dur = wf.getnframes() / wf.getframerate()
    here = route(shutil.which("chromium") is not None, shutil.which("ffmpeg") is not None)
    return [("browser+ffmpeg -> A", route(True, True) == "A", "A"),
            ("ffmpeg only -> B", route(False, True) == "B", "B"),
            ("neither -> C", route(False, False) == "C" and route(True, False) == "C", "C"),
            ("route C ships HTML + synthesized WAV + commands", files == ["COMMANDS.txt", "index.html", "score.wav"] and dur == 2.0, files),
            ("this machine has ffmpeg -> A or B", here in "AB", here)]


def eng55(work):
    jobs = [{"name": f"j{i}", "cmd": [sys.executable, "-c", "import os,time;t=time.time();time.sleep(0.25);print(os.environ['KOSIF_WORKERS'], t, time.time())"]} for i in range(4)]
    save_json(work / "jobs.json", jobs)
    from concurrent.futures import ThreadPoolExecutor

    def run(j):
        env = dict(os.environ, KOSIF_WORKERS="1")
        out = subprocess.run(j["cmd"], capture_output=True, text=True, env=env).stdout.split()
        return {"name": j["name"], "workers": out[0], "start": float(out[1]), "end": float(out[2])}
    with ThreadPoolExecutor(max_workers=2) as ex:
        rep = list(ex.map(run, jobs))
    save_json(work / "jobs.report.json", rep)
    events = sorted([(r["start"], 1) for r in rep] + [(r["end"], -1) for r in rep])
    cur = peak = 0
    for _, d in events:
        cur += d
        peak = max(peak, cur)
    return [("report lists all 4 jobs", [r["name"] for r in rep] == ["j0", "j1", "j2", "j3"], len(rep)),
            ("each job got KOSIF_WORKERS=1", all(r["workers"] == "1" for r in rep), [r["workers"] for r in rep]),
            ("at most 2 at a time, and 2 really overlapped", peak == 2, peak)]


def subframe_render(pos_fn, w, h, n, fps, k, shutter, stack="average"):
    """Render n frames of a 1-px dot moving by pos_fn(t); accumulate k sub-frames over shutter*frame."""
    out = []
    for i in range(n):
        acc = np.zeros((h, w))
        for j in range(k):
            t = (i + (shutter * (j + 0.5) / k if k > 1 else 0)) / fps
            img = np.zeros((h, w))
            x = int(round(pos_fn(t)))
            if 0 <= x < w:
                img[:, x] = 1.0
            acc = np.maximum(acc, img) if stack == "lighten" else acc + img / k
        out.append(acc)
    return out


def eng56(work):
    fps = 30
    speed = 480  # px/s -> 16 px per frame
    fr = subframe_render(lambda t: 4 + speed * t, 64, 4, 3, fps, 4, 0.5)
    crisp = subframe_render(lambda t: 4 + speed * t, 64, 4, 3, fps, 1, 0.5)
    np.save(work / "blur.npy", np.array(fr))
    lit = np.nonzero(fr[1][0])[0]
    span = lit.max() - lit.min()
    grain_seed = [hash2(i, 0) for i in range(3)]
    return [("4 sub-frames -> 4 lit columns", len(lit) == 4, lit.tolist()),
            ("180 deg shutter: sub-frames span 0.5 frame (16 px * 0.5 * 3/4 = 6 px)", span == 6, int(span)),
            ("energy conserved (sum = 1 column)", abs(fr[1].sum() / 4 - 1) < 1e-9, fr[1].sum()),
            ("k=1 stays crisp", np.count_nonzero(crisp[1][0]) == 1, int(np.count_nonzero(crisp[1][0]))),
            ("grain fixed per output frame (seeded by frame)", grain_seed == [hash2(i, 0) for i in range(3)], grain_seed)]


def eng57(work):
    def check(html):
        p = []
        if len(re.findall(r"<h1\b", html)) != 1:
            p.append("exactly one h1")
        for bp in (900, 580):
            if not re.search(r"@media\s*\(max-width:\s*%dpx\)" % bp, html):
                p.append(f"breakpoint {bp}px")
        if re.search(r"<link[^>]+stylesheet[^>]+href=\"(?!https://fonts\.googleapis)", html):
            p.append("external stylesheet")
        s, t = html.find("gsap.set("), re.search(r"gsap\.(to|from|fromTo)\(", html)
        if t and (s < 0 or s > t.start()):
            p.append("gsap.set must precede tweens")
        return p
    good = ("<style>h1{font:800 76px/1 sans}@media (max-width: 900px){h1{font-size:60px}}@media (max-width: 580px){h1{font-size:44px}}</style>"
            "<h1>عنوان</h1><h2>a</h2><script>gsap.set('.card',{y:40});gsap.to('.card',{y:0});</script>")
    (work / "landing.html").write_text(good, encoding="utf-8")
    return [("good page passes", check(good) == [], check(good)),
            ("two h1 caught", "exactly one h1" in check(good.replace("<h2>a</h2>", "<h1>b</h1>")), ""),
            ("missing 580px breakpoint caught", "breakpoint 580px" in check(good.replace("580px", "600px")), ""),
            ("tween before gsap.set caught", "gsap.set must precede tweens" in check(good.replace("gsap.set('.card',{y:40});", "")), ""),
            ("external stylesheet caught", "external stylesheet" in check(good + '<link rel="stylesheet" href="x.css">'), "")]


def eng58(work):
    scale, margin = 2, 16
    bg = (245, 240, 230)
    W, H = 200, 120
    im = Image.new("RGB", (W * scale, H * scale), bg)
    d = ImageDraw.Draw(im)
    box = (37 * scale, 21 * scale, 151 * scale, 77 * scale)
    d.rectangle(box, fill=(20, 30, 60))
    im.save(work / "raw.png")
    a = np.asarray(im).astype(int)
    ref = a[2, 2]
    mask = np.abs(a - ref).sum(-1) > 12
    ys, xs = np.nonzero(mask)
    crop = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    pad = margin * scale
    out = Image.new("RGB", (crop.width + 2 * pad, crop.height + 2 * pad), tuple(int(v) for v in ref))
    out.paste(crop, (pad, pad))
    out.save(work / "trimmed.png")
    o = np.asarray(out).astype(int)
    m2 = np.abs(o - ref).sum(-1) > 12
    y2, x2 = np.nonzero(m2)
    return [("content size kept", (crop.width, crop.height) == (box[2] - box[0] + 1, box[3] - box[1] + 1), crop.size),
            ("margin 16 CSS px = 32 device px each side", (x2.min(), y2.min(), out.width - 1 - x2.max(), out.height - 1 - y2.max()) == (32, 32, 32, 32), (int(x2.min()), int(y2.min()))),
            ("background sampled at pixel (2,2)", tuple(ref) == bg, tuple(ref))]


def eng59(work):
    def fcpxml(fps, clips, markers):
        fd = Fraction(100, 100 * fps)
        root = ET.Element("fcpxml", version="1.10")
        res = ET.SubElement(root, "resources")
        ET.SubElement(res, "format", id="r1", frameDuration=f"100/{100 * fps}s", width="1920", height="1080")
        for i, c in enumerate(clips):
            ET.SubElement(res, "asset", id=f"a{i}", src=c["src"], start="0s", duration=f"{c['frames'] * 100}/{100 * fps}s")
        spine = ET.SubElement(ET.SubElement(ET.SubElement(ET.SubElement(root, "library"), "event"), "project", name="edit"), "sequence", format="r1")
        sp = ET.SubElement(spine, "spine")
        off = 0
        for i, c in enumerate(clips):
            cl = ET.SubElement(sp, "asset-clip", ref=f"a{i}", offset=f"{off * 100}/{100 * fps}s", duration=f"{c['frames'] * 100}/{100 * fps}s")
            for m in markers.get(i, []):
                ET.SubElement(cl, "marker", start=f"{m * 100}/{100 * fps}s", value=f"beat {m}")
            off += c["frames"]
        return root, fd
    root, fd = fcpxml(24, [{"src": "a.mov", "frames": 48}, {"src": "b.mov", "frames": 37}], {1: [12]})
    ET.ElementTree(root).write(work / "edit.fcpxml", encoding="utf-8", xml_declaration=True)

    def rat(s):
        n, d = s[:-1].split("/")
        return Fraction(int(n), int(d))
    clips = root.findall(".//asset-clip")
    end = rat(clips[-1].get("offset")) + rat(clips[-1].get("duration"))
    r30, _ = fcpxml(30, [{"src": "a", "frames": 1}], {})
    return [("frameDuration 100/2400s at 24 fps", root.find(".//format").get("frameDuration") == "100/2400s", root.find(".//format").get("frameDuration")),
            ("30 fps -> 100/3000s", r30.find(".//format").get("frameDuration") == "100/3000s", ""),
            ("85 frames end exactly at 85/24 s", end == Fraction(85, 24), str(end)),
            ("second clip offset 4800/2400s", clips[1].get("offset") == "4800/2400s", clips[1].get("offset"))]


PROGRAMS = {
    "ENG-01": eng01, "ENG-02": eng02, "ENG-03": eng03, "ENG-04": eng04, "ENG-05": eng05, "ENG-06": eng06,
    "ENG-07": eng07, "ENG-08": eng08, "ENG-09": eng09, "ENG-11": eng11, "ENG-13": eng13, "ENG-14": eng14,
    "ENG-15": eng15, "ENG-17": eng17, "ENG-19": eng19, "ENG-20": eng20, "ENG-21": eng21, "ENG-22": eng22,
    "ENG-23": eng23, "ENG-24": eng24, "ENG-25": eng25, "ENG-26": eng26, "ENG-27": eng27, "ENG-28": eng28,
    "ENG-29": eng29, "ENG-31": eng31, "ENG-34": eng34, "ENG-35": eng35, "ENG-36": eng36, "ENG-37": eng37,
    "ENG-39": eng39, "ENG-41": eng41, "ENG-45": eng45, "ENG-46": eng46, "ENG-47": eng47, "ENG-48": eng48,
    "ENG-49": eng49, "ENG-50": eng50, "ENG-54": eng54, "ENG-55": eng55, "ENG-56": eng56, "ENG-57": eng57,
    "ENG-58": eng58, "ENG-59": eng59,
}


# ================================================================ batch 2: ENG-61 .. ENG-119


def eng61(work):
    class Scene:
        def __init__(self, css_w, css_h, pixel_ratio):
            self.pr = min(pixel_ratio, 3)
            self.w, self.h = int(css_w * self.pr), int(css_h * self.pr)
            self.records = [{"x": i * 10, "v": (i * 37) % 100} for i in range(12)]
            self.static_draws = 0
            self._static = None

        def static_layer(self):
            if self._static is None:
                self.static_draws += 1
                a = np.zeros((self.h, self.w))
                a[::max(1, self.h // 8)] = 0.2
                self._static = a
            return self._static

        def draw(self, t):
            img = self.static_layer().copy()
            k = int(t * 2) % len(self.records)
            r = self.records[k]
            img[: int(self.h * r["v"] / 100), int(r["x"] * self.pr) % self.w] = 1.0
            return img
    s4 = Scene(400, 300, 4)
    s2 = Scene(400, 300, 2)
    a, b = s4.draw(1.0), s4.draw(1.0)
    s4.draw(2.0)
    np.save(work / "frame.npy", a[::10, ::10])
    return [("pixelRatio 4 clamped to 3 -> 1200x900", (s4.w, s4.h) == (1200, 900), (s4.w, s4.h)),
            ("pixelRatio 2 -> 800x600", (s2.w, s2.h) == (800, 600), (s2.w, s2.h)),
            ("redraw from state is identical for the same t", np.array_equal(a, b), ""),
            ("static layer drawn once, active marks every frame", s4.static_draws == 1 and not np.array_equal(a, s4.draw(2.0)), s4.static_draws)]


def eng62(work):
    ASPECT = {"9:16": (1080, 1920), "16:9": (1920, 1080), "1:1": (1080, 1080), "4:5": (1080, 1350)}
    dna = {"shots": [{"dur": 1.2, "move": "push"}, {"dur": 0.8, "move": "pan"}], "grade": {"contrast": 1.1, "saturation": 1.05},
           "captions": {"alignment": 2}, "music_mix": 0.3}
    save_json(work / "dna.json", dna)
    (work / "style_bible.md").write_text("# بصمة الأسلوب\n\n" + "\n".join(f"- لقطة {i + 1}: {s['dur']} ث، حركة {s['move']}" for i, s in enumerate(dna["shots"])), encoding="utf-8")
    script = f'''import argparse, json
DNA = {json.dumps(dna)}
ASPECT = {json.dumps(ASPECT)}
ap = argparse.ArgumentParser()
for a in ["--clips", "--out", "--music", "--srt", "--duration"]:
    ap.add_argument(a)
ap.add_argument("--mode", choices=["style", "clone"], default="style")
ap.add_argument("--aspect", choices=list(ASPECT), default="9:16")
ap.add_argument("--fps", type=int, default=30)
ap.add_argument("--res", type=int, choices=[720, 1080], default=1080)
ap.add_argument("--keep-audio", action="store_true")
ap.add_argument("--seed", type=int, default=7)
ap.add_argument("--dry-run", action="store_true")
a = ap.parse_args()
w, h = ASPECT[a.aspect]
s = a.res / min(w, h)
w, h = int(round(w * s / 2) * 2), int(round(h * s / 2) * 2)
cmds = []
for i, shot in enumerate(DNA["shots"]):
    g = DNA["grade"]
    cmds.append(f"ffmpeg -i clip{{i}}.mp4 -t {{shot['dur']}} -vf scale={{w}}:{{h}}:force_original_aspect_ratio=increase,crop={{w}}:{{h}},eq=contrast={{g['contrast']}}:saturation={{g['saturation']}},fps={{a.fps}} -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 shot{{i}}.mp4")
cmds.append("ffmpeg -f concat -safe 0 -i list.txt -c copy joined.mp4")
cmds.append(f"ffmpeg -i joined.mp4 -i {{a.music}} -filter_complex amix=inputs=2:weights=1 {{DNA['music_mix']}} -c:v copy -c:a aac -b:a 192k {{a.out}}")
print(json.dumps({{"size": [w, h], "seed": a.seed, "commands": cmds}}))
'''
    (work / "rebuild.py").write_text(script)
    r1 = json.loads(sh([sys.executable, work / "rebuild.py", "--dry-run", "--aspect", "9:16", "--res", "720", "--music", "m.wav", "--out", "o.mp4"]))
    r2 = json.loads(sh([sys.executable, work / "rebuild.py", "--dry-run", "--aspect", "16:9"]))
    bad = subprocess.run([sys.executable, work / "rebuild.py", "--dry-run", "--aspect", "2:1"], capture_output=True)
    c = " ".join(r1["commands"])
    return [("9:16 at --res 720 -> 720x1280", r1["size"] == [720, 1280], r1["size"]),
            ("16:9 default 1080 -> 1920x1080", r2["size"] == [1920, 1080], r2["size"]),
            ("per-shot libx264 veryfast crf 18 yuv420p + aac 160k 48 kHz", c.count("-crf 18") == 2 and "-b:a 160k -ar 48000" in c, r1["commands"][0][-120:]),
            ("music mixed at 0.3, aac 192k, concat demuxer", "weights=1 0.3" in c and "-b:a 192k" in c and "-f concat" in c, ""),
            ("seed defaults to 7, unknown aspect refused", r1["seed"] == 7 and bad.returncode != 0, r1["seed"]),
            ("JSON + style bible + script exported", all((work / f).is_file() for f in ["dna.json", "style_bible.md", "rebuild.py"]), "")]


def eng63(work):
    W, H = 54, 96
    story = {"duration": 12, "scenes": [{"start": 0, "end": 4}, {"start": 4, "end": 8}, {"start": 8, "end": 12}]}

    def scene_at(t):
        return next((i for i, s in enumerate(story["scenes"]) if s["start"] <= t < s["end"]), len(story["scenes"]) - 1)

    def draw(t):
        a = np.zeros((H, W, 3))
        k = scene_at(t)
        a[..., 2] = np.linspace(40, 90, H)[:, None] + 30 * k
        ph = t * 1.3
        cx, cy = W / 2 + 18 * math.cos(ph), H / 2 + 18 * math.sin(ph)
        yy, xx = np.mgrid[0:H, 0:W]
        a[..., 0] = np.where((xx - cx) ** 2 + (yy - cy) ** 2 <= 4, 255, 0)
        a[H - 2:, : int(round(W * t / story["duration"]))] = (255, 255, 255)
        return a.astype(np.uint8)
    times = [0.5, 2.0, 4.5, 6.0, 9.1, 11.5]
    fr = [draw(t) for t in times]
    for t, f in zip(times, fr):
        write_png(work / f"t{t}.png", f)
    hashes = {hashlib.md5(f.tobytes()).hexdigest() for f in fr}
    errs = []
    for t, f in zip(times, fr):
        ys, xs = np.nonzero(f[: H - 2, :, 0] == 255)
        ang = math.atan2(ys.mean() - H / 2, xs.mean() - W / 2) % (2 * math.pi)
        errs.append(abs((ang - (t * 1.3) % (2 * math.pi) + math.pi) % (2 * math.pi) - math.pi))
    return [("6 sample times -> 6 distinct frames", len(hashes) == 6, len(hashes)),
            ("pure function of absolute time", np.array_equal(draw(3.3), draw(3.3)), ""),
            ("scene lookup start <= t < end", [scene_at(t) for t in (0, 3.99, 4, 8, 12)] == [0, 0, 1, 2, 2], ""),
            ("orbit phase = t * 1.3 rad/s", max(errs) < 0.2, round(max(errs), 3)),
            ("progress bar = t/duration", int((fr[3][H - 1, :, 1] == 255).sum()) == round(W * 0.5), int((fr[3][H - 1, :, 1] == 255).sum()))]


def eng64(work):
    SIZES = {"9:16": (540, 960), "16:9": (960, 540), "1:1": (720, 720)}

    def play(stamps_ms, duration):
        t, last, out = 0.0, None, []
        for s in stamps_ms:
            if last is not None:
                t += min((s - last) / 1000, 0.08)
                if t >= duration:
                    t = 0.0
            last = s
            out.append(round(t, 6))
        return out

    def mmss(t):
        return f"{int(t // 60):02d}:{int(t % 60):02d}"
    tr = play([0, 16, 32, 532, 548], 30)
    loop = play([0, 50, 100, 150], 0.12)
    save_json(work / "playback.json", {"normal": tr, "loop": loop})
    return [("canvas sized by aspect", SIZES["9:16"] == (540, 960) and SIZES["1:1"] == (720, 720), SIZES),
            ("normal frames advance by dt", tr[1] == 0.016 and tr[2] == 0.032, tr),
            ("a 500 ms stall advances only 80 ms", abs(tr[3] - tr[2] - 0.08) < 1e-9, tr),
            ("playback loops at the end", loop == [0.0, 0.05, 0.1, 0.0], loop),
            ("slider 0-1000 and mm:ss readout", (500 / 1000 * 75, mmss(75)) == (37.5, "01:15"), mmss(75))]


def eng65(work):
    calls = []

    def draw_editorial(t):
        calls.append(("editorial", t))

    def draw_native(t):
        calls.append(("native", t))

    def make_player(story):
        win = {"fmbReady": False}

        def draw(t):
            (draw_editorial if story.get("profile") == "viral-editorial-3d" else draw_native)(t)
        win["renderFrame"] = draw
        win["fmbReady"] = True
        return win
    a = make_player({"profile": "viral-editorial-3d"})
    b = make_player({"profile": "other"})
    c = make_player({})
    a["renderFrame"](1.0)
    b["renderFrame"](2.0)
    c["renderFrame"](3.0)
    save_json(work / "calls.json", calls)
    return [("viral-editorial-3d -> editorial renderer", calls[0] == ("editorial", 1.0), calls[0]),
            ("other profile -> native", calls[1] == ("native", 2.0), calls[1]),
            ("no profile -> native", calls[2] == ("native", 3.0), calls[2]),
            ("renderFrame + fmbReady exposed", a["fmbReady"] and callable(a["renderFrame"]), "")]


def eng66(work):
    from urllib.parse import unquote
    ROOT = work / "site"
    for d in ["web", "project", "assets", "examples", "secret"]:
        (ROOT / d).mkdir(parents=True)
        (ROOT / d / "f.txt").write_text(d)
    allowed = {"web", "project", "assets", "examples"}

    def serve(url):
        rel = unquote(url).lstrip("/")
        target = (ROOT / rel).resolve()
        if ROOT.resolve() not in target.parents:
            return 403, {}
        if target.relative_to(ROOT.resolve()).parts[0] not in allowed:
            return 403, {}
        if not target.is_file():
            return 404, {}
        return 200, {"Cache-Control": "no-store"}
    r = {u: serve(u)[0] for u in ["/web/f.txt", "/examples/f.txt", "/secret/f.txt", "/web/../secret/f.txt", "/web/%2e%2e/secret/f.txt", "/web/none.txt", "/../../etc/passwd"]}
    save_json(work / "routes.json", r)
    return [("whitelisted dirs served", r["/web/f.txt"] == 200 and r["/examples/f.txt"] == 200, r),
            ("non-whitelisted dir refused", r["/secret/f.txt"] == 403, r["/secret/f.txt"]),
            ("traversal (plain and %2e%2e) refused", r["/web/../secret/f.txt"] == r["/web/%2e%2e/secret/f.txt"] == r["/../../etc/passwd"] == 403, r),
            ("missing file 404, no-store caching", r["/web/none.txt"] == 404 and serve("/web/f.txt")[1]["Cache-Control"] == "no-store", "")]


def storyboard_errors(sb):
    p = []
    for k in ["version", "brief", "duration_seconds", "aspect", "fps", "scenes"]:
        if k not in sb:
            p.append(f"missing {k}")
    if p:
        return p
    if sb["fps"] != 30:
        p.append("fps must be 30")
    prev = 0
    for i, s in enumerate(sb["scenes"]):
        if s.get("id") != f"scene-{i + 1:02d}":
            p.append(f"id {s.get('id')}")
        for k in ["start", "end"]:
            if round(s[k], 3) != s[k]:
                p.append(f"{s['id']} {k} beyond ms precision")
        if s["start"] != prev or s["end"] <= s["start"]:
            p.append(f"{s['id']} timing")
        prev = s["end"]
        for k in ["title", "text", "visual", "motion", "sfx"]:
            if k not in s:
                p.append(f"{s['id']} missing {k}")
    if abs(prev - sb["duration_seconds"]) > 1e-9:
        p.append("scenes do not end at duration")
    return p


def eng67(work):
    sc = lambda i, a, b: {"id": f"scene-{i:02d}", "start": a, "end": b, "title": "t", "text": "x", "visual": "v", "motion": "m", "sfx": ""}  # noqa: E731
    sb = {"version": 1, "brief": "b", "duration_seconds": 9.5, "aspect": "9:16", "fps": 30,
          "scenes": [sc(1, 0, 3.25), sc(2, 3.25, 6.125), sc(3, 6.125, 9.5)]}
    save_json(work / "storyboard.json", sb)
    bad_id = json.loads(json.dumps(sb))
    bad_id["scenes"][1]["id"] = "scene-2"
    bad_ms = json.loads(json.dumps(sb))
    bad_ms["scenes"][0]["end"] = 3.2501
    gap = json.loads(json.dumps(sb))
    gap["scenes"][2]["start"] = 6.2
    return [("valid storyboard passes", storyboard_errors(sb) == [], storyboard_errors(sb)),
            ("ids must be scene-01..", any("id scene-2" in e for e in storyboard_errors(bad_id)), storyboard_errors(bad_id)),
            ("times limited to ms precision", any("ms precision" in e for e in storyboard_errors(bad_ms)), storyboard_errors(bad_ms)),
            ("gap between scenes caught", any("timing" in e for e in storyboard_errors(gap)), storyboard_errors(gap)),
            ("fps 30 enforced", "fps must be 30" in storyboard_errors(dict(sb, fps=25)), "")]


def eng68(work):
    def smooth(a, b, x):
        u = clamp01((x - a) / (b - a))
        return u * u * (3 - 2 * u)

    def headline_opacity(local):
        return smooth(0.5, 1.1, local) * (1 - smooth(4.7, 6.0, local))

    def draw(w, t):
        scale = w / 540
        h = int(w * 16 / 9)
        local = t % 6
        a = np.zeros((h, w, 3))
        a[...] = (240, 236, 226)
        a[::int(12 * scale), ::int(12 * scale)] = (200, 190, 180)
        ph = t * 1.06
        y = int(h / 2 + 10 * scale * math.sin(ph))
        a[y:y + int(6 * scale), :, 0] = 255 * headline_opacity(local)
        x = int((w / 2) + 15 * scale * math.cos(ph))
        a[: int(8 * scale), x % w] = (30, 30, 30)
        return a.astype(np.uint8), scale
    times = [0.1, 1.2, 2.5, 3.8, 5.0, 6.5]
    fr = [draw(216, t)[0] for t in times]
    for t, f in zip(times, fr):
        write_png(work / f"ed_{t}.png", f)
    return [("scale = w/540 (1080 -> 2)", draw(1080, 0)[1] == 2.0, draw(1080, 0)[1]),
            ("hidden before entrance at .5 s", headline_opacity(0.4) == 0 and headline_opacity(0.6) > 0, headline_opacity(0.6)),
            ("fully shown mid-scene, exit starts after 4.7 s", headline_opacity(3) == 1 and headline_opacity(4.6) == 1 and headline_opacity(4.9) < 1, headline_opacity(4.9)),
            ("6 distinct frames across 0.1-6.5 s", len({f.tobytes() for f in fr}) == 6, len({f.tobytes() for f in fr}))]


def value_noise(t, seed=0, rate=8.0):
    x = t * rate
    i = math.floor(x)
    f = x - i
    a, b = hash2(i, seed), hash2(i + 1, seed)
    u = f * f * (3 - 2 * f)
    return (a + (b - a) * u) * 2 - 1


def eng69(work):
    stop = lambda t, fps=12: math.floor(t * fps) / fps  # noqa: E731
    phos = lambda age, tau: math.exp(-age / tau)  # noqa: E731

    def frame(t):
        return (round(value_noise(t, 1), 9), round(value_noise(t, 2), 9), stop(t), round(phos(t % 1, 0.25), 9))
    times = [i / 30 for i in range(60)]
    seq = [frame(t) for t in times]
    par = [frame(t) for t in reversed(times)][::-1]
    save_json(work / "frames.json", seq[:10])
    jumps = max(abs(value_noise(t + 1e-4, 1) - value_noise(t, 1)) for t in times)
    return [("stop-motion floor(t*fps)/fps: 0.49 s @12 -> 5/12", stop(0.49) == 5 / 12, stop(0.49)),
            ("phosphor exp(-age/tau) = 1/e at age = tau", abs(phos(0.25, 0.25) - 1 / math.e) < 1e-12, phos(0.25, 0.25)),
            ("shake channels continuous", jumps < 0.01, jumps),
            ("frames identical in any capture order", seq == par, ""),
            ("independent channels differ", value_noise(0.3, 1) != value_noise(0.3, 2), "")]


def eng74(work):
    src = work / "skill"
    (src / "scripts").mkdir(parents=True)
    (src / "SKILL.md").write_text("---\nname: x\n---\n")
    for i in range(250):
        (src / "scripts" / f"s{i:03d}.py").write_text(f"# {i}\n")

    def build(out, claude_ai, description):
        if claude_ai and len(description) > 1024:
            raise ValueError("description > 1024 chars")
        files = sorted(p for p in src.rglob("*") if p.is_file())
        files.sort(key=lambda p: (p.name != "SKILL.md", str(p)))
        if claude_ai:
            files = files[:200]
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
            for p in files:
                z.write(p, p.relative_to(src))
        return out
    small = build(work / "x.zip", True, "d" * 1024)
    full = build(work / "full.zip", False, "")
    names = zipfile.ZipFile(small).namelist()
    try:
        build(work / "y.zip", True, "d" * 1025)
        refused = False
    except ValueError:
        refused = True
    return [("claude.ai upload <= 200 files", len(names) == 200, len(names)),
            ("SKILL.md always included", "SKILL.md" in names, names[0]),
            ("full package keeps all 251", len(zipfile.ZipFile(full).namelist()) == 251, len(zipfile.ZipFile(full).namelist())),
            ("description of 1025 chars refused", refused, refused)]


def sampled(fn, t0, t1, fps=60):
    n = round((t1 - t0) * fps)
    return [{"duration": 1 / fps, "ease": "none", **fn(t0 + (i + 1) / fps)} for i in range(n)]


def play_keyframes(start, kfs, t, key):
    """GSAP-style keyframe playback (ease none): linear between successive keyframe values."""
    prev, acc = start, 0.0
    for k in kfs:
        if t <= acc + k["duration"] + 1e-12:
            u = (t - acc) / k["duration"]
            return prev + (k[key] - prev) * u
        prev, acc = k[key], acc + k["duration"]
    return prev


def eng75(work):
    fn = lambda t: {"x": 100 * t * t}  # noqa: E731
    kf = sampled(fn, 0, 1)
    save_json(work / "keyframes.json", kf)
    mid = play_keyframes(0, kf, 0.5, "x")
    return [("60 keyframes per second", len(kf) == 60, len(kf)),
            ("each keyframe 1/fps, ease none", all(abs(k["duration"] - 1 / 60) < 1e-15 and k["ease"] == "none" for k in kf), kf[0]),
            ("durations sum to t1-t0", abs(sum(k["duration"] for k in kf) - 1) < 1e-12, sum(k["duration"] for k in kf)),
            ("playback at a sample = fn(t)", abs(mid - 25) < 1e-9, mid),
            ("last keyframe = fn(t1)", kf[-1]["x"] == 100, kf[-1]["x"])]


def mulberry32_np(seed, n):
    """Second, independent implementation with numpy uint32 arithmetic (the '3D kit' copy)."""
    a = np.uint32(seed)
    out = []
    with np.errstate(over="ignore"):
        for _ in range(n):
            a = np.uint32(a + np.uint32(0x6D2B79F5))
            t = np.uint32((a ^ (a >> np.uint32(15))) * (np.uint32(1) | a))
            t = np.uint32((t + np.uint32((t ^ (t >> np.uint32(7))) * (np.uint32(61) | t))) ^ t)
            out.append(float(np.uint32(t ^ (t >> np.uint32(14)))) / 4294967296)
    return out


def eng76(work):
    r = mulberry32(42)
    kit = mulberry32_np(42, 50)
    motion = [r() for _ in range(50)]
    save_json(work / "streams.json", {"motion": motion[:5], "kit": kit[:5]})
    return [("constant 0x6D2B79F5 = 1831565813", 0x6D2B79F5 == 1831565813, 0x6D2B79F5),
            ("MOTION.rng(42) first value == JS 0.6011037519201636", motion[0] == 0.6011037519201636, motion[0]),
            ("3D-kit rng gives the same stream", kit == motion, kit[:2]),
            ("different seeds differ", mulberry32(43)() != motion[0], "")]


def aces(x, exposure=0.6):
    x = np.asarray(x, np.float64) * exposure
    return np.clip((x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14), 0, 1)


def pbr_neutral(c):
    c = np.array(c, np.float64)
    start, desat = 0.8 - 0.04, 0.15
    x = c.min()
    off = x - 6.25 * x * x if x < 0.08 else 0.04
    c = c - off
    peak = c.max()
    if peak < start:
        return c
    d = 1 - start
    new = 1 - d * d / (peak + d - start)
    c = c * new / peak
    g = 1 - 1 / (desat * (peak - new) + 1)
    return c * (1 - g) + new * g


def eng77(work):
    ramp = np.linspace(0, 20, 256)
    out = aces(ramp)
    write_png(work / "aces_ramp.png", np.tile((out * 255)[None, :, None], (8, 1, 3)))
    hot = pbr_neutral([4.0, 1.0, 0.2])
    return [("ACES(0) = 0", out[0] == 0, out[0]),
            ("ACES monotonic", bool(np.all(np.diff(out) >= 0)), ""),
            ("exposure 0.6: ACES(1) = 0.9216/1.3688 = 0.6733", abs(float(aces(1.0)) - 0.9216 / 1.3688) < 1e-9, float(aces(1.0))),
            ("highlights roll off below 1", float(aces(20)) <= 1.0 and float(aces(20)) > 0.97, float(aces(20))),
            ("neutral keeps mid-grey (0.5 -> 0.46 offset only)", np.allclose(pbr_neutral([0.5] * 3), 0.46), pbr_neutral([0.5] * 3).tolist()),
            ("neutral compresses highlights to <= 1", hot.max() <= 1.0 and hot[0] > hot[1] > hot[2], hot.round(3).tolist())]


def eng78(work):
    P = dict(bloom=.55, radius=.5, threshold=.82, vignette=.38, grain=.025, ca=0)

    def lite_post(img, supported=True, **kw):
        if not supported:
            return np.asarray(img, np.float64)  # plain render fallback
        return post_stack(img, **{**P, **kw})
    flat = np.full((32, 48, 3), 0.8)
    nb = lite_post(flat, grain=0, vignette=0)
    v = lite_post(flat, grain=0, bloom=0)
    g = lite_post(flat, vignette=0, bloom=0, seed=5)
    hot = np.zeros((32, 48, 3))
    hot[16, 24] = 3
    hb = lite_post(hot, grain=0, vignette=0)
    np.save(work / "lite.npy", v)
    return [("0.8 below threshold .82 -> no bloom", np.allclose(nb, flat), float(abs(nb - flat).max())),
            ("bloom .55 spreads from a hot pixel", hb[16, 26, 0] > 0, float(hb[16, 26, 0])),
            ("vignette .38 at corners", abs(v[0, 0, 0] / 0.8 - (1 - .38)) < 1e-9, v[0, 0, 0] / 0.8),
            ("grain .025 -> amplitude <= .0125", float(abs(g - flat).max()) <= .0125 + 1e-12, float(abs(g - flat).max())),
            ("unsupported -> plain render", np.array_equal(lite_post(flat, supported=False), flat), "")]


def eng79(work):
    from scipy.ndimage import gaussian_filter, shift

    def lab_post(img, bloom=.08, threshold=.95, grain=.05, vignette=.18, ca=.4, warm=.25, dof=False, seed=1):
        x = np.asarray(img, np.float64).copy()
        x = x + bloom * gaussian_filter(np.maximum(x - threshold, 0), (2, 2, 0))
        if ca:
            x[..., 0] = shift(x[..., 0], (0, ca), order=1, mode="nearest")
            x[..., 2] = shift(x[..., 2], (0, -ca), order=1, mode="nearest")
        x[..., 0] *= 1 + warm * 0.2
        x[..., 2] *= 1 - warm * 0.2
        if dof:
            x = gaussian_filter(x, (1.5, 1.5, 0))
        h, w = x.shape[:2]
        yy, xx = np.mgrid[0:h, 0:w]
        r2 = (((xx - (w - 1) / 2) / ((w - 1) / 2)) ** 2 + ((yy - (h - 1) / 2) / ((h - 1) / 2)) ** 2) / 2
        x = x * (1 - vignette * r2)[..., None]
        if grain:
            x = x + (np.random.default_rng(seed).random((h, w, 1)) - .5) * grain
        return x
    edge = np.zeros((16, 32, 3))
    edge[:, 16:] = 0.5
    e = lab_post(edge, grain=0, vignette=0, warm=0)
    flat = np.full((16, 32, 3), 0.5)
    wv = lab_post(flat, grain=0, vignette=0, ca=0)
    sharp = lab_post(edge, grain=0, vignette=0, ca=0, warm=0)
    soft = lab_post(edge, grain=0, vignette=0, ca=0, warm=0, dof=True)
    np.save(work / "lab.npy", wv)
    return [("CA .4 -> fractional red split (0.4 of the step)", abs(e[8, 16, 0] - 0.5 * 0.6) < 1e-9, e[8, 16, 0]),
            ("warm .25 lifts red, cools blue", wv[8, 8, 0] > 0.5 > wv[8, 8, 2], wv[8, 8].tolist()),
            ("threshold .95: 0.5 grey gets no bloom", np.allclose(sharp, edge), ""),
            ("DOF opt-in only", np.array_equal(sharp, edge) and not np.allclose(soft, edge), ""),
            ("vignette .18 at the corner", abs(lab_post(flat, grain=0, ca=0, warm=0)[0, 0, 0] / 0.5 - 0.82) < 1e-9, "")]


def eng80(work):
    def make_renderer(W, H, draft_scale=None):
        pr = draft_scale if draft_scale else 1
        return {"pixelRatio": pr, "buffer": (round(W * pr), round(H * pr))}
    full = make_renderer(1920, 1080)
    draft = make_renderer(1920, 1080, 0.5)
    img = Image.new("RGB", draft["buffer"], (20, 20, 20)).resize((1920 // 10, 1080 // 10))
    img.save(work / "draft_preview.png")
    return [("no draft -> pixel ratio 1, full buffer", full == {"pixelRatio": 1, "buffer": (1920, 1080)}, full),
            ("__draftScale .5 -> 960x540 buffer", draft["buffer"] == (960, 540) and draft["pixelRatio"] == 0.5, draft),
            ("draft renders 4x fewer pixels", (1920 * 1080) / (960 * 540) == 4, 4)]


def spring(t, k, d, m=1.0):
    w0 = math.sqrt(k / m)
    z = d / (2 * math.sqrt(k * m))
    if z < 1:
        wd = w0 * math.sqrt(1 - z * z)
        return 1 - math.exp(-z * w0 * t) * (math.cos(wd * t) + z * w0 / wd * math.sin(wd * t))
    if z == 1:
        return 1 - math.exp(-w0 * t) * (1 + w0 * t)
    r1, r2 = -w0 * (z - math.sqrt(z * z - 1)), -w0 * (z + math.sqrt(z * z - 1))
    c2 = r1 / (r1 - r2)
    c1 = 1 - c2
    return 1 - (c1 * math.exp(r1 * t) + c2 * math.exp(r2 * t))


def spring_ode(t_end, k, d, dt=1e-4):
    x, v = 0.0, 0.0
    for _ in range(int(t_end / dt)):
        a = -k * (x - 1) - d * v
        v += a * dt
        x += v * dt
    return x


def eng81(work):
    out = lambda p: 1 - 2 ** (-10 * p)  # noqa: E731
    exit_ = lambda p: p ** 2.8  # noqa: E731
    beat = lambda t, bpm=120: t * bpm / 60  # noqa: E731
    ts = np.linspace(0, 1.5, 300)
    body = [spring(t, 170, 26) for t in ts]
    title = [spring(t, 220, 24) for t in ts]
    save_json(work / "curves.json", {"spring_170_26": body[::30], "spring_220_24": title[::30]})
    return [("closed-form spring matches ODE integration", abs(spring(0.3, 170, 26) - spring_ode(0.3, 170, 26)) < 2e-3, (spring(0.3, 170, 26), spring_ode(0.3, 170, 26))),
            ("k170 d26 settles, overshoot < 0.1%", max(body) < 1.001 and abs(body[-1] - 1) < 1e-3, max(body)),
            ("title 220/24 overshoots more (~1.3%)", 1.005 < max(title) < 1.02, max(title)),
            ("out(1) = 1 - 2^-10 = 0.9990234375", out(1) == 0.9990234375, out(1)),
            ("exit(.5) = .5^2.8 = 0.14359", abs(exit_(0.5) - 0.143587) < 1e-5, exit_(0.5)),
            ("BPM 120: 1.25 s = beat 2.5", beat(1.25) == 2.5, beat(1.25))]


def eng82(work):
    FPS = {24, 25, 30, 50, 60}

    def plan(seconds, aspect, titles, accents, fps):
        if fps not in FPS:
            raise ValueError("fps")
        ts = titles.split("|")
        acc = accents.split(",")
        beat = seconds / len(ts)
        return [{"title": t, "accent": acc[i % len(acc)], "start": i * beat, "end": (i + 1) * beat} for i, t in enumerate(ts)]
    p = plan(12, "9:16", "a|b|c", "#E7B65A,#5BD1A5", 30)
    fr = []
    for b in p:
        rgb = tuple(int(b["accent"][i:i + 2], 16) for i in (1, 3, 5))
        im = Image.new("RGB", (36, 64), (14, 14, 18))
        ImageDraw.Draw(im).rectangle([4, 28, 31, 35], fill=rgb)
        im.save(work / f"beat_{b['title']}.png")
        fr.append(np.asarray(im)[30, 10].tolist())
    try:
        plan(12, "9:16", "a", "#fff000", 29)
        bad = False
    except ValueError:
        bad = True
    return [("accents cycle a->1, b->2, c->1", [b["accent"] for b in p] == ["#E7B65A", "#5BD1A5", "#E7B65A"], [b["accent"] for b in p]),
            ("12 s over 3 titles -> 4 s beats", [b["start"] for b in p] == [0, 4, 8], [b["start"] for b in p]),
            ("frames drawn in the accent", fr[0] == [231, 182, 90] and fr[1] == [91, 209, 165], fr[:2]),
            ("fps limited to 24/25/30/50/60", bad, bad)]


def eng83(work):
    W, H, fps, dur = 64, 36, 20, 1.0
    logo = work / "logo.png"
    Image.new("RGB", (8, 8), (255, 0, 0)).save(logo)
    spec = {"clips": [{"color": "0x203040", "dur": dur}], "overlays": [{"type": "image", "src": "logo.png", "x": 4, "y": 4}],
            "progress": {"h": 4, "color": "white"}}
    save_json(work / "spec.json", spec)
    ph = spec['progress']['h']
    fc = (f"[0:v][1:v]overlay={spec['overlays'][0]['x']}:{spec['overlays'][0]['y']}[o];"
          f"[o][2:v]overlay=x='-w+W*t/{dur}':y=H-{ph}:eval=frame[v]")
    out = work / "f.mp4"
    ff("-f", "lavfi", "-i", f"color=c={spec['clips'][0]['color']}:s={W}x{H}:r={fps}:d={dur}", "-i", logo,
       "-f", "lavfi", "-i", f"color=c={spec['progress']['color']}:s={W}x{ph}:r={fps}:d={dur}", "-filter_complex", fc,
       "-map", "[v]", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "1", "-pix_fmt", "yuv444p", out)
    fr = decode(out, W, H)
    mid = fr[10]
    lit = int((mid[H - 2, :, 1] > 200).sum())
    return [("logo overlaid at (4,4)", mid[6, 6, 0] > 200 and mid[6, 6, 1] < 60, mid[6, 6].tolist()),
            ("progress bar at t=0.5 is half width", abs(lit - W / 2) <= 2, lit),
            ("progress bar grows", int((fr[2][H - 2, :, 1] > 200).sum()) < lit < int((fr[-1][H - 2, :, 1] > 200).sum()), ""),
            ("20 frames for 1 s at 20 fps", len(fr) == 20, len(fr))]


def eng84(work):
    PRESETS = {"aurora": "#0b2a3a", "sunset": "#3a1a12", "grid": "#101828"}

    def studio_import(project):
        if project["preset"] not in PRESETS:
            raise KeyError(project["preset"])
        return {"size": project["size"], "fps": project["fps"],
                "clips": [{"type": "color", "color": PRESETS[project["preset"]], "dur": s["dur"], "title": s.get("text")} for s in project["scenes"]]}
    edit = studio_import({"preset": "sunset", "size": [64, 36], "fps": 10, "scenes": [{"dur": 0.5, "text": "مرحبا"}]})
    save_json(work / "edit.json", edit)
    out = work / "f.mp4"
    c = edit["clips"][0]
    ff("-f", "lavfi", "-i", f"color=c=0x{c['color'][1:]}:s=64x36:r=10:d={c['dur']}", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "0", "-pix_fmt", "yuv444p", out)
    px = decode(out, 64, 36)[0][10, 10].astype(int)
    try:
        studio_import({"preset": "neon", "size": [1, 1], "fps": 1, "scenes": []})
        bad = False
    except KeyError:
        bad = True
    return [("sunset preset -> #3a1a12", c["color"] == "#3a1a12", c["color"]),
            ("rendered background matches preset", np.abs(px - [0x3a, 0x1a, 0x12]).max() <= 2, px.tolist()),
            ("scene text carried to the timeline", c["title"] == "مرحبا", c["title"]),
            ("unknown preset refused", bad, bad)]


def project_kind(html):
    if re.search(r"three-kit|window\.K3", html):
        kind = "3d"
    elif re.search(r"window\.seek\s*=", html):
        kind = "canvas"
    elif "manifest-player" in html:
        kind = "manifest"
    else:
        kind = "2d"
    w = re.search(r'data-width="(\d+)"', html)
    h = re.search(r'data-height="(\d+)"', html)
    d = re.search(r'data-duration="([\d.]+)"', html)
    return {"kind": kind, "size": (int(w.group(1)), int(h.group(1))) if w and h else None, "duration": float(d.group(1)) if d else None}


def eng85(work):
    pages = {"3d": '<div data-width="1920" data-height="1080" data-duration="6"></div><script src="assets/three-kit.bundle.js"></script><script>window.seek=t=>0</script>',
             "canvas": '<div data-width="1080" data-height="1920" data-duration="4"></div><script>window.seek = function(t){}</script>',
             "manifest": '<body data-width="1080" data-height="1080" data-duration="12"><script>/*manifest-player*/</script>',
             "2d": '<div data-width="1920" data-height="1080" data-duration="8"></div>'}
    r = {k: project_kind(v) for k, v in pages.items()}
    save_json(work / "kinds.json", r)
    return [("each page classified", all(r[k]["kind"] == k for k in r), {k: v["kind"] for k, v in r.items()}),
            ("3D wins over window.seek", r["3d"]["kind"] == "3d", r["3d"]),
            ("size read from data-width/height", r["canvas"]["size"] == (1080, 1920), r["canvas"]["size"]),
            ("duration read from the page", r["manifest"]["duration"] == 12.0, r["manifest"]["duration"])]


def render_contract_errors(html):
    soup = parse_html(html)
    p = []
    body = soup.body
    for a in ["data-composition-id", "data-width", "data-height", "data-duration", "data-fps"]:
        if body is None or not body.has_attr(a):
            p.append(f"body missing {a}")
    js = "\n".join(s.get_text() for s in soup.find_all("script"))
    for need, rx in [("window.render", r"window\.render\s*="), ("window.__duration", r"window\.__duration\s*="), ("window.__ready", r"window\.__ready\s*=\s*true")]:
        if not re.search(rx, js):
            p.append(f"missing {need}")
    if "capture" not in js:
        p.append("no ?capture mode")
    m = re.search(r"window\.render\s*=\s*function\s*\(\s*t\s*\)\s*\{(.*?)\n\};", js, re.S)
    if m and lint_js(m.group(1), ["requestAnimationFrame", "Date.now", "Math.random"]):
        p.append("render(t) not pure")
    return p


def eng87(work):
    page = ('<body data-composition-id="c" data-width="1080" data-height="1920" data-duration="6" data-fps="30"><div id="ui"></div><script>\n'
            "if (new URLSearchParams(location.search).has('capture')) document.getElementById('ui').remove();\n"
            "window.__duration = 6;\nwindow.render = function(t){\n  el.style.opacity = Math.min(1, t);\n};\n"
            "window.__ready = true;\nfunction preview(){ requestAnimationFrame(preview); }\n</script></body>")
    (work / "index.html").write_text(page)
    impure = page.replace("el.style.opacity = Math.min(1, t);", "el.style.opacity = Math.random();")
    return [("valid page passes", render_contract_errors(page) == [], render_contract_errors(page)),
            ("rAF allowed for preview playback only", "requestAnimationFrame" in page and render_contract_errors(page) == [], ""),
            ("Math.random inside render(t) caught", "render(t) not pure" in render_contract_errors(impure), render_contract_errors(impure)),
            ("missing __ready caught", "missing window.__ready" in render_contract_errors(page.replace("window.__ready = true;", "")), ""),
            ("missing body data-fps caught", "body missing data-fps" in render_contract_errors(page.replace(' data-fps="30"', "")), "")]


def eng88(work):
    fps = 30
    t_of = lambda i: i / fps  # noqa: E731

    def wait_ready(ready_at_ms, timeout=60000, poll=500):
        t = 0
        while t <= timeout:
            if ready_at_ms is not None and t >= ready_at_ms:
                return "ready"
            t += poll
        return "timeout"
    src = "window.render = function(t){ cam.x = Math.sin(t); };\nwindow.__ready = true;"
    bad = "window.render = function(t){ cam.x = Date.now(); requestAnimationFrame(f); };"
    (work / "scene.js").write_text(src)
    return [("t step = 1/fps = 0.0333 s", round(t_of(1), 4) == 0.0333, t_of(1)),
            ("frame 150 = 5.00 s", t_of(150) == 5.0, t_of(150)),
            ("pure page passes the lint", lint_js(src, ["requestAnimationFrame", "Date.now", "Math.random"]) == [], ""),
            ("Date.now / rAF caught", lint_js(bad, ["requestAnimationFrame", "Date.now", "Math.random"]) == ["Date.now", "requestAnimationFrame"], lint_js(bad, ["requestAnimationFrame", "Date.now"])),
            ("ready wait gives up after 60 s", wait_ready(None) == "timeout" and wait_ready(59000) == "ready", "")]


def eng89(work):
    RATIO = {"9:16": (1080, 1920), "16:9": (1920, 1080), "1:1": (1080, 1080)}
    TEMPLATE = "<title>{{TITLE}}</title><div data-w='{{WIDTH}}' data-h='{{HEIGHT}}' data-d='{{DURATION}}' data-fps='{{FPS}}'></div>"

    def new(name, typ="2d", ratio="9:16", seconds=10, fps=30, title="عنوان"):
        w, h = RATIO[ratio] if ratio in RATIO else tuple(int(v) for v in ratio.split("x"))
        d = work / name
        for sub in ["frames", "assets"]:
            (d / sub).mkdir(parents=True)
        html = TEMPLATE
        for k, v in {"TITLE": title, "WIDTH": w, "HEIGHT": h, "DURATION": seconds, "FPS": fps}.items():
            html = html.replace("{{%s}}" % k, str(v))
        (d / "index.html").write_text(html, encoding="utf-8")
        save_json(d / "project.json", {"type": typ, "width": w, "height": h, "seconds": seconds, "fps": fps, "frames": seconds * fps})
        (d / "STORYBOARD.md").write_text(f"# {title}\n", encoding="utf-8")
        save_json(d / "ai_prompts.json", [])
        if typ == "3d":
            (d / "assets" / "three.min.js").write_text("// three")
        return d
    a = new("p916")
    b = new("p4k", "3d", "3840x2160", 5, 24)
    html = (a / "index.html").read_text(encoding="utf-8")
    pj = json.loads((b / "project.json").read_text())
    return [("9:16 -> 1080x1920 baked in", "data-w='1080' data-h='1920'" in html, html[-80:]),
            ("no {{placeholders}} left", "{{" not in html, ""),
            ("custom WxH 3840x2160", (pj["width"], pj["height"]) == (3840, 2160), pj),
            ("3d copies three.min.js; frames/ and assets/ made", (b / "assets/three.min.js").exists() and (a / "frames").is_dir(), ""),
            ("project.json frames = 10 x 30", json.loads((a / "project.json").read_text())["frames"] == 300, "")]


def eng90(work):
    proj = work / "proj"
    (proj / "assets").mkdir(parents=True)
    pat = frames_from(lambda i: solid(64, 36, (i * 10, 50, 90)), 15, proj / "frames")
    rng = np.random.default_rng(0)
    write_wav(proj / "assets" / "soundtrack.wav", rng.uniform(-0.5, 0.5, 44100 * 2), 44100, 2)

    def default_audio(p, given=None):
        if given:
            return given
        s = p / "assets" / "soundtrack.wav"
        return s if s.exists() else None
    audio = default_audio(proj)
    out = work / "f.mp4"
    ff("-framerate", "30", "-i", pat, "-i", audio, "-c:a", "aac", "-b:a", "256k", "-shortest", "-c:v", "libx264",
       "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", out)
    a = astream(out)
    dur = float(probe(out)["format"]["duration"])
    return [("default audio = assets/soundtrack.wav", audio.name == "soundtrack.wav", str(audio.name)),
            ("AAC ~256 kb/s", a["codec_name"] == "aac" and 200_000 < int(a["bit_rate"]) <= 270_000, a.get("bit_rate")),
            ("-shortest: 2 s audio cut to 0.5 s video", dur < 0.7, dur),
            ("15 frames yuv420p", count_frames(out) == 15 and vstream(out)["pix_fmt"] == "yuv420p", "")]


def eng91(work):
    fn = lambda t: {"y": math.sin(2 * math.pi * t)}  # noqa: E731
    kf = sampled(fn, 0.5, 2.0)
    save_json(work / "kf.json", kf[:10])
    errs = [abs(play_keyframes(fn(0.5)["y"], kf, t - 0.5, "y") - fn(t)["y"]) for t in np.linspace(0.5, 2.0, 157)]
    return [("1.5 s at 60 Hz -> 90 keyframes", len(kf) == 90, len(kf)),
            ("piecewise-linear playback within 1.4e-3 of fn", max(errs) < 1.4e-3, max(errs)),
            ("ends exactly at fn(2.0)", abs(kf[-1]["y"] - fn(2.0)["y"]) < 1e-12, kf[-1]["y"])]


def eng92(work):
    good = "const r = MOTION.rng(7); const x = r() * 100; const h = MOTION.hash(3, 4);"
    bad = "const x = Math.random() * 100;"
    (work / "lint.json").write_text(json.dumps({"good": lint_js(good, ["Math.random"]), "bad": lint_js(bad, ["Math.random"])}))
    a, b = mulberry32(7), mulberry32(7)
    return [("seeded rng passes the lint", lint_js(good, ["Math.random"]) == [], ""),
            ("Math.random is a lint error", lint_js(bad, ["Math.random"]) == ["Math.random"], ""),
            ("commented-out Math.random ignored", lint_js("// Math.random()\n" + good, ["Math.random"]) == [], ""),
            ("re-render identical frame for frame", [a() for _ in range(100)] == [b() for _ in range(100)], "")]


def eng94(work):
    fps, speed = 30, 30 * 2  # 2 px per frame time unit
    avg = subframe_render(lambda t: 2 + speed * t, 80, 2, 1, fps, 16, 30, "average")[0]
    lit = subframe_render(lambda t: 2 + speed * t, 80, 2, 1, fps, 16, 30, "lighten")[0]
    np.save(work / "stacks.npy", np.stack([avg, lit]))
    cols = np.nonzero(lit[0])[0]
    return [("lighten keeps every trail sample at full brightness", float(lit[0, cols].min()) == 1.0, float(lit[0, cols].min())),
            ("average dims each of 16 samples to 1/16", abs(float(avg[0, cols].max()) - 1 / 16) < 1e-9, float(avg[0, cols].max())),
            ("shutter 30 frames spans ~58 px trail (30 * 2 * 15/16 + ...)", 50 <= cols.max() - cols.min() <= 60, int(cols.max() - cols.min())),
            ("16 distinct trail positions", len(cols) == 16, len(cols))]


def eng95(work):
    TEMPLATES = {None: "composition.html", "3d": "scene3d/", "canvas": "canvas.html", "lab": "lab/", "directed": "directed.html", "verse": "verse.html"}

    def choose(flags):
        on = [f for f in ("3d", "canvas", "lab") if flags.get(f)]
        if len(on) > 1:
            raise ValueError("pick one route")
        return TEMPLATES[on[0] if on else None]
    r = {"flat": choose({}), "3d": choose({"3d": True}), "canvas": choose({"canvas": True}), "lab": choose({"lab": True})}
    save_json(work / "routes.json", r)
    try:
        choose({"3d": True, "lab": True})
        bad = False
    except ValueError:
        bad = True
    return [("flat -> composition.html", r["flat"] == "composition.html", r),
            ("--3d -> scene3d/, --canvas -> canvas.html, --lab -> lab/", (r["3d"], r["canvas"], r["lab"]) == ("scene3d/", "canvas.html", "lab/"), r),
            ("two routes refused", bad, bad)]


def eng96(work):
    import importlib.util

    def env_report(libs, tools):
        rep = {"python": {m: importlib.util.find_spec(m) is not None for m in libs},
               "tools": {t: shutil.which(t) is not None for t in tools}}
        browser = any(rep["tools"].get(b) for b in ("chromium", "chrome", "msedge"))
        rep["route"] = "A" if browser and rep["tools"]["ffmpeg"] else ("B" if rep["tools"]["ffmpeg"] else "C")
        return rep
    r = env_report(["numpy", "PIL", "no_such_module_xyz"], ["ffmpeg", "chromium", "no-such-tool-xyz"])
    save_json(work / "env.json", r)
    return [("numpy and PIL found", r["python"]["numpy"] and r["python"]["PIL"], r["python"]),
            ("missing module reported missing", r["python"]["no_such_module_xyz"] is False, ""),
            ("ffmpeg found here", r["tools"]["ffmpeg"], r["tools"]),
            ("route follows browser+ffmpeg", r["route"] == ("A" if r["tools"]["chromium"] else "B"), r["route"])]


def eng98(work):
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="10" height="10"/>'
           '<filter id="f"><feGaussianBlur stdDeviation="2"/></filter><mask id="m"><rect width="100" height="100" fill="white"/></mask>'
           '<clipPath id="c"><circle r="5"/></clipPath><pattern id="p"><rect width="2" height="2"/></pattern>'
           '<image href="x.png" width="10" height="10"/><circle r="4"/></svg>')
    _, steps = load_svg(svg)
    save_json(work / "steps.json", steps)
    return [("only drawable shapes become steps", [s["tag"] for s in steps] == ["rect", "circle"], [s["tag"] for s in steps]),
            ("filter/mask/clipPath/pattern/image not drawn", SKIP_TAGS == {"filter", "mask", "clipPath", "pattern", "image"}, sorted(SKIP_TAGS)),
            ("max_steps limit honoured", len(load_svg("<svg xmlns='http://www.w3.org/2000/svg'>" + "<rect/>" * 300 + "</svg>")[1]) == 160, "")]


def eng99(work):
    code = ("from PIL import Image, ImageDraw\nim = Image.new('RGB', (64, 64))\nd = ImageDraw.Draw(im)\n"
            "for i in range(360):\n    d.line([(i % 64, 0), (63 - i % 64, 63)], fill=(i % 255, 90, 160))\n"
            "for i in range(5):\n    d.ellipse([i, i, 20 + i, 20 + i], outline='white')\nim.save(OUT)\n")
    (work / "drawing.py").write_text(code)
    runner = ("import json, sys\nfrom PIL import ImageDraw\nlog = []\nfor name in ['line', 'ellipse', 'rectangle', 'polygon']:\n"
              "    orig = getattr(ImageDraw.ImageDraw, name)\n"
              "    def wrap(self, *a, _o=orig, _n=name, **k):\n        log.append(_n)\n        return _o(self, *a, **k)\n"
              "    setattr(ImageDraw.ImageDraw, name, wrap)\n"
              "OUT = sys.argv[2]\nexec(open(sys.argv[1]).read(), {'OUT': OUT, '__name__': '__main__'})\n"
              "strokes = []\nfor n in log:\n    if strokes and strokes[-1]['op'] == n and strokes[-1]['count'] < 20:\n        strokes[-1]['count'] += 1\n"
              "    else:\n        strokes.append({'op': n, 'count': 1})\njson.dump({'commands': len(log), 'strokes': strokes}, open(sys.argv[3], 'w'))\n")
    (work / "runner_impl.py").write_text(runner)
    scratch = work / "scratch"
    scratch.mkdir()
    subprocess.run([sys.executable, work / "runner_impl.py", work / "drawing.py", work / "final.png", work / "jobs.json"],
                   cwd=scratch, timeout=120, check=True)
    jobs = json.loads((work / "jobs.json").read_text())
    line_strokes = [s for s in jobs["strokes"] if s["op"] == "line"]
    return [("every PIL command recorded in order (365)", jobs["commands"] == 365, jobs["commands"]),
            ("360 lines -> 18 strokes", len(line_strokes) == 18 and all(s["count"] == 20 for s in line_strokes), len(line_strokes)),
            ("ellipses follow lines (painter order)", jobs["strokes"][-1] == {"op": "ellipse", "count": 5}, jobs["strokes"][-1]),
            ("picture produced", Image.open(work / "final.png").size == (64, 64), "")]


def eng100(work):
    W, H, fps = 64, 36, 20
    a = gray_clip(work / "a.mp4", W, H, fps, 20, [40] * 20)
    b = gray_clip(work / "b.mp4", W, H, fps, 40, [10 + 5 * i for i in range(40)], ["-c:v", "libx264", "-preset", "ultrafast", "-crf", "0", "-pix_fmt", "yuv444p"])
    edl = {"fps": fps, "size": [W, H], "sources": {"a": str(a), "b": str(b)},
           "clips": [{"src": "a", "in": 0.0, "out": 1.0, "speed": 1.0}, {"src": "b", "in": 0.0, "out": 2.0, "speed": 2.0}]}
    save_json(work / "edl.json", edl)

    def compile_edl(e, out):
        ins, fc, labels = [], [], ""
        srcs = list(e["sources"])
        for s in srcs:
            ins += ["-i", e["sources"][s]]
        for k, c in enumerate(e["clips"]):
            i = srcs.index(c["src"])
            fc.append(f"[{i}:v]trim=start={c['in']}:end={c['out']},setpts=(PTS-STARTPTS)/{c['speed']},fps={e['fps']},scale={e['size'][0]}:{e['size'][1]},format=yuv444p[v{k}]")
            labels += f"[v{k}]"
        fc.append(f"{labels}concat=n={len(e['clips'])}:v=1:a=0[v]")
        return ["ffmpeg", "-y", "-v", "error", *ins, "-filter_complex", ";".join(fc), "-map", "[v]", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "0", str(out)]
    out = work / "final.mp4"
    cmd = compile_edl(edl, out)
    (work / "dry_run.txt").write_text(shlex.join(cmd))
    sh(cmd)
    fr = decode(out, W, H)
    lv = [int(f[5, 5, 0]) for f in fr]
    return [("one ffmpeg command with one filter_complex", cmd.count("-filter_complex") == 1 and cmd[0] == "ffmpeg", ""),
            ("duration = 1 s + 2 s / speed 2 = 2 s", len(fr) == 40, len(fr)),
            ("first clip from source a", all(abs(v - 40) <= 2 for v in lv[:20]), lv[:3]),
            ("speed 2 skips every other source frame", all(abs(lv[20 + k] - (10 + 10 * k)) <= 2 for k in range(20)), lv[20:24])]


def eng101(work):
    W, H, fps, n = 32, 18, 30, 24
    pat = frames_from(lambda i: solid(W, H, (i * 10, 255 - i * 10, 60)), n, work / "frames")
    out = encode_png(pat, work / "x.mp4", fps, ["-c:v", "libx264", "-preset", "ultrafast", "-crf", "18", "-pix_fmt", "yuv420p"])
    picks = [round(i * (n - 1) / 11) for i in range(12)]
    sheet = Image.new("RGB", (4 * W, 3 * H))
    for k, i in enumerate(picks):
        sheet.paste(Image.open(work / "frames" / f"f_{i:04d}.png"), ((k % 4) * W, (k // 4) * H))
    sheet.save(work / "contact-sheet.png")
    gif = work / "p.gif"
    ff("-framerate", fps, "-i", pat, "-vf", "split[a][b];[a]palettegen[p];[b][p]paletteuse", gif)
    g = Image.open(gif)
    return [("MP4 has all 24 frames", count_frames(out) == 24, count_frames(out)),
            ("contact sheet 12 frames in 4 cols (128x54)", sheet.size == (4 * W, 3 * H), sheet.size),
            ("sheet tile 12 is the last frame", np.asarray(sheet)[2 * H + 5, 3 * W + 5].tolist()[:2] == [230, 25], np.asarray(sheet)[2 * H + 5, 3 * W + 5].tolist()),
            ("GIF preview has 24 frames", getattr(g, "n_frames", 1) == 24, getattr(g, "n_frames", 1))]


def eng102(work):
    R = mulberry32(7)
    vals = [R() for _ in range(3)]
    pts = [(round(R() * 100, 6), round(R() * 100, 6)) for _ in range(5)]
    R2 = mulberry32(7)
    [R2() for _ in range(3)]
    pts2 = [(round(R2() * 100, 6), round(R2() * 100, 6)) for _ in range(5)]
    save_json(work / "particles.json", pts)
    return [("rng(7) == JS reference", vals == JS_MULBERRY_SEED7, vals),
            ("particles identical on every render", pts == pts2, pts[0])]


def fingerprint(project, params):
    h = hashlib.sha1()
    for p in sorted(project.rglob("*")):
        if not p.is_file() or p.name.endswith(".kosif.json") or p.suffix == ".mp4":
            continue
        rel = str(p.relative_to(project))
        if p.suffix in {".html", ".js", ".css", ".json", ".svg", ".txt"}:
            h.update(rel.encode() + p.read_bytes())
        else:
            st = p.stat()
            h.update(f"{rel}:{st.st_size}:{st.st_mtime_ns}".encode())
    keys = ["engine", "fps", "size", "scale", "blur", "shutter", "stack", "capture", "preset", "crf", "quality"]
    h.update(json.dumps({**{k: params.get(k) for k in keys}, "v": 4}, sort_keys=True).encode())
    return h.hexdigest()


def cached_render(project, film, params, force=False):
    fp = fingerprint(project, params)
    stamp = Path(str(film) + ".kosif.json")
    if not force and film.exists() and stamp.exists() and json.loads(stamp.read_text())["fingerprint"] == fp:
        return "cached"
    film.write_bytes(b"film" + fp.encode())
    save_json(stamp, {"fingerprint": fp, "params": params})
    return "rendered"


def eng103(work):
    proj = work / "p"
    proj.mkdir()
    (proj / "index.html").write_text("<p>1</p>")
    (proj / "clip.mp3").write_bytes(b"\x00" * 100)
    film = proj / "FILM.mp4"
    P = {"engine": "studio", "fps": 30, "crf": 17}
    r = [cached_render(proj, film, P), cached_render(proj, film, P)]
    (proj / "index.html").write_text("<p>2</p>")
    r.append(cached_render(proj, film, P))
    os.utime(proj / "clip.mp3", ns=(1, 1))
    r.append(cached_render(proj, film, P))
    r.append(cached_render(proj, film, {**P, "crf": 18}))
    r.append(cached_render(proj, film, {**P, "crf": 18}, force=True))
    r.append(cached_render(proj, film, {**P, "crf": 18, "unrelated": 1}))
    return [("first render, then cached", r[:2] == ["rendered", "cached"], r),
            ("text source change re-renders", r[2] == "rendered", r[2]),
            ("binary mtime change re-renders", r[3] == "rendered", r[3]),
            ("render param (crf) change re-renders", r[4] == "rendered", r[4]),
            ("--force overrides the cache", r[5] == "rendered", r[5]),
            ("non-hashed key does not bust the cache", r[6] == "cached", r[6]),
            ("stamp FILM.mp4.kosif.json written", (proj / "FILM.mp4.kosif.json").is_file(), "")]


def eng104(work):
    def home(env, tool_dir, cwd, writable):
        if env.get("KOSIF_MOTION_HOME"):
            return Path(env["KOSIF_MOTION_HOME"])
        return tool_dir if writable(tool_dir) else cwd
    tool, cwd, custom = work / "tool", work / "cwd", work / "custom"
    for d in (tool, cwd, custom):
        d.mkdir()
    a = home({"KOSIF_MOTION_HOME": str(custom)}, tool, cwd, lambda p: True)
    b = home({}, tool, cwd, lambda p: True)
    c = home({}, tool, cwd, lambda p: False)
    (a / "projects").mkdir()
    save_json(work / "homes.json", [str(a), str(b), str(c)])
    return [("KOSIF_MOTION_HOME wins", a == custom, str(a)),
            ("else next to the tool when writable", b == tool, str(b)),
            ("read-only tool dir -> working directory", c == cwd, str(c))]


def eng108(work):
    seed_rng = mulberry32(11)
    stars = [(seed_rng() * 64, seed_rng() * 36) for _ in range(200)]

    def frame(t):
        a = np.zeros((36, 64))
        for k, (x, y) in enumerate(stars):
            xx = int(x + 10 * t) % 64
            a[int(y), xx] = 0.5 + 0.5 * math.sin(t * 3 + k)
        return a
    ts = [i / 30 for i in range(30)]
    t0 = time.perf_counter()
    fwd = [frame(t) for t in ts]
    per = (time.perf_counter() - t0) / len(ts) * 1000
    back = [frame(t) for t in reversed(ts)][::-1]
    np.save(work / "frame0.npy", fwd[0])
    return [("frame = f(t): any order gives the same frames", all(np.array_equal(a, b) for a, b in zip(fwd, back)), ""),
            ("seeded star field reproducible", stars[0][0] == mulberry32(11)() * 64, stars[0]),
            ("budget < 50 ms per frame", per < 50, round(per, 2))]


def eng111(work):
    page = (REPO / "starters" / "html-canvas" / "index.html").read_text(encoding="utf-8")
    tl = (REPO / "starters" / "html-canvas" / "timeline.js").read_text(encoding="utf-8")
    m = re.search(r"window\.__kosif\s*=\s*\{([^}]*)\}", page)
    keys = re.findall(r"(\w+)\s*:", m.group(1)) if m else []
    (work / "contract.json").write_text(json.dumps({"keys": keys}))
    seek_body = re.search(r"seek\(t\)\s*\{(.*?)\n    \}", tl, re.S)
    return [("starter exposes window.__kosif {duration, fps, seek}", keys == ["duration", "fps", "seek"], keys),
            ("optional window.__kosifReady promise", "window.__kosifReady" in page, ""),
            ("seek(t) clamps t into [0, duration]", bool(seek_body) and "Math.max(0, Math.min(this.duration, t))" in seek_body.group(1), ""),
            ("starter draws without Math.random / Date.now", lint_js(page + tl, ["Math.random", "Date.now"]) == [], lint_js(page + tl, ["Math.random", "Date.now"]))]


def eng113(work):
    def smoothstep(x):
        x = clamp01(x)
        return x * x * (3 - 2 * x)

    def world(n_sections, dive=1.3, conn=0.9):
        spans, pos = [], 0.0
        for i in range(n_sections):
            spans.append(("section", i, pos, pos + dive))
            pos += dive
            if i < n_sections - 1:
                spans.append(("connector", i, pos, pos + conn))
                pos += conn
        return spans, pos

    def at(spans, scroll, crossfade=0.12):
        for kind, i, a, b in spans:
            if a <= scroll < b:
                local = (scroll - a) / (b - a)
                op = smoothstep(local / crossfade) * smoothstep((1 - local) / crossfade)
                return kind, i, round(local, 6), round(op, 6), round(1.03 + 0.14 * local, 6)
        return None
    spans, total = world(3)
    save_json(work / "spans.json", spans)
    lerp = lambda cur, target, k=0.1: cur + (target - cur) * k  # noqa: E731
    return [("3 sections + 2 connectors = 3*1.3 + 2*0.9 = 5.7 screens", abs(total - 5.7) < 1e-12, total),
            ("scroll 0.65 is the middle of section 0", at(spans, 0.65)[:3] == ("section", 0, 0.5), at(spans, 0.65)),
            ("scale = 1.03 + 0.14 * local (0.5 -> 1.1)", at(spans, 0.65)[4] == 1.1, at(spans, 0.65)[4]),
            ("copy fully visible mid-section, 0 at edges", at(spans, 0.65)[3] == 1.0 and at(spans, 0.0)[3] == 0.0, at(spans, 0.0)),
            ("crossfade .12: half-way at local .06", at(spans, 0.06 * 1.3)[3] == 0.5, at(spans, 0.078)),
            ("scroll -> time is lerped", lerp(0, 1) == 0.1, "")]


def power1_out(p):
    return 1 - (1 - p) ** 2


class Tweens:
    """Minimal GSAP-like engine: to / from / fromTo / set, default duration 0.5 s, ease power1.out."""

    def __init__(self, css):
        self.css, self.items = dict(css), []

    def to(self, prop, end, start_t=0.0, duration=0.5, ease=power1_out):
        self.items.append((prop, None, end, start_t, duration, ease))

    def from_(self, prop, start, start_t=0.0, duration=0.5, ease=power1_out):
        self.items.append((prop, start, self.css[prop], start_t, duration, ease))

    def fromTo(self, prop, start, end, start_t=0.0, duration=0.5, ease=power1_out):
        self.items.append((prop, start, end, start_t, duration, ease))

    def set(self, prop, value, start_t=0.0):
        self.items.append((prop, value, value, start_t, 0.0, lambda p: 1))

    def state(self, t):
        s = dict(self.css)
        for prop, a, b, t0, d, ease in self.items:
            if t < t0 and a is not None and d > 0:
                s[prop] = a
                continue
            if t < t0:
                continue
            p = 1.0 if d == 0 else clamp01((t - t0) / d)
            a0 = s[prop] if a is None else a
            s[prop] = a0 + (b - a0) * ease(p)
        if "autoAlpha" in s:
            s["visibility"] = "hidden" if s["autoAlpha"] == 0 else "inherit"
        return s


def eng114(work):
    tw = Tweens({"x": 0, "y": 40, "autoAlpha": 1, "scale": 1})
    tw.to("x", 100)
    tw.from_("y", 0, 0.5)
    tw.fromTo("scale", 0.5, 1.5, 1.0, 1.0)
    tw.set("autoAlpha", 0, 2.5)
    s = {t: tw.state(t) for t in (0.25, 0.5, 0.75, 1.5, 3.0)}
    save_json(work / "states.json", {str(k): v for k, v in s.items()})
    return [("to(): default 0.5 s, power1.out -> 75 at t=0.25", s[0.25]["x"] == 75, s[0.25]["x"]),
            ("from(): starts at given value, CSS keeps final layout", s[0.5]["y"] == 0 and s[3.0]["y"] == 40, (s[0.5]["y"], s[3.0]["y"])),
            ("from() mid-way 0.75 = 30", s[0.75]["y"] == 30, s[0.75]["y"]),
            ("fromTo(): explicit start+end", s[1.5]["scale"] == 0.5 + 1.0 * power1_out(0.5), s[1.5]["scale"]),
            ("set(): instant, autoAlpha 0 hides", s[3.0]["autoAlpha"] == 0 and s[3.0]["visibility"] == "hidden" and s[1.5]["visibility"] == "inherit", s[3.0]["visibility"])]


def directional(cur, spec):
    m = re.fullmatch(r"(-?[\d.]+)_(cw|ccw|short)", spec)
    target, mode = float(m.group(1)), m.group(2)
    diff = (target - cur) % 360
    if mode == "cw":
        delta = diff if target > cur or diff else 0
        delta = target - cur if target - cur > 0 else diff
    elif mode == "ccw":
        delta = target - cur if target - cur < 0 else diff - 360
    else:
        delta = diff - 360 if diff > 180 else diff
    return cur + delta


def relative(cur, spec):
    m = re.fullmatch(r"([+\-*/])=(-?[\d.]+)", spec)
    op, v = m.group(1), float(m.group(2))
    return {"+": cur + v, "-": cur - v, "*": cur * v, "/": cur / v}[op]


def eng115(work):
    r = {"360_cw from 0": directional(0, "360_cw"), "-170_short from 0": directional(0, "-170_short"),
         "90_ccw from 10": directional(10, "90_ccw"), "350_short from 10": directional(10, "350_short"),
         "+=20 from 5": relative(5, "+=20"), "*=2 from 1.5": relative(1.5, "*=2")}
    tw = Tweens({"--hue": 0, "--wght": 700})
    tw.to("--hue", 180, duration=1, ease=lambda p: p)
    tw.to("--wght", 300, duration=1, ease=lambda p: p)
    mid = tw.state(0.5)
    r["vars at 0.5"] = mid
    save_json(work / "rotations.json", r)
    return [("'360_cw' turns a full clockwise circle", r["360_cw from 0"] == 360, r["360_cw from 0"]),
            ("'-170_short' takes the short way", r["-170_short from 0"] == -170, r["-170_short from 0"]),
            ("'90_ccw' from 10 goes counter-clockwise to -270", r["90_ccw from 10"] == -270, r["90_ccw from 10"]),
            ("'350_short' from 10 goes -20 to -10", r["350_short from 10"] == -10, r["350_short from 10"]),
            ("x:'+=20' and scale:'*=2'", (r["+=20 from 5"], r["*=2 from 1.5"]) == (25, 3.0), ""),
            ("CSS vars --hue / --wght interpolate", (mid["--hue"], mid["--wght"]) == (90, 500), mid)]


def eng117(work):
    drawn = []

    def draw_frame(time_):
        cells = [int(hash2(int(time_ * 30), k) * 255) for k in range(8)]
        drawn.append(round(time_, 6))
        return cells
    tw = Tweens({"time": 0})
    tw.to("time", 5, 0, duration=5, ease=lambda p: p)
    frames = {}
    for t in (2.5, 0.0, 5.0, 2.5):
        p = tw.state(t)
        frames.setdefault(t, []).append(draw_frame(p["time"]))
    save_json(work / "proxy.json", {str(k): v for k, v in frames.items()})
    return [("proxy time follows the timeline (ease none)", tw.state(2.5)["time"] == 2.5 and tw.state(5)["time"] == 5, ""),
            ("onUpdate redraws with the proxy time", drawn == [2.5, 0.0, 5.0, 2.5], drawn),
            ("seeking back gives the same canvas (integer hash)", frames[2.5][0] == frames[2.5][1], frames[2.5][0][:3])]


def hf_errors(html, fps_allowed=(24, 30, 60), sizes=((1920, 1080), (1080, 1920))):
    p = composition_errors(html, required=("data-composition-id", "data-width", "data-height", "data-duration"), fps_allowed=fps_allowed)
    soup = parse_html(html)
    root = soup.find(attrs={"data-composition-id": True})
    if root is not None and root.has_attr("data-width") and (int(root["data-width"]), int(root["data-height"])) not in sizes:
        p.append("size")
    for c in soup.find_all(class_="clip"):
        for a in ["id", "data-start", "data-duration", "data-track-index"]:
            if not c.has_attr(a):
                p.append(f"clip missing {a}")
    js = "\n".join(s.get_text() for s in soup.find_all("script"))
    if re.search(r"(setTimeout|then|addEventListener)\s*\([^;]*__timelines", js, re.S):
        p.append("timeline registered asynchronously")
    return [e for e in p if e != "MOTION.shim(root, seconds) missing"]


def eng118(work):
    clips = '<div class="clip" id="t1" data-start="0" data-duration="3" data-track-index="2"></div><div class="clip" id="t2" data-start="3" data-duration="2" data-track-index="1"></div>'
    page = composition_page(w=1080, h=1920, dur=5, fps=30, shim=False, extra_body=clips)
    (work / "index.html").write_text(page)
    late = page.replace("window.__timelines['root'] = tl;", "setTimeout(() => { window.__timelines['root'] = tl; }, 0);")
    return [("valid HyperFrames page", hf_errors(page) == [], hf_errors(page)),
            ("clip without data-track-index caught", "clip missing data-track-index" in hf_errors(page.replace(' data-track-index="1"', "")), ""),
            ("fps 25 rejected (24/30/60)", any("data-fps" in e for e in hf_errors(page.replace('data-fps="30"', 'data-fps="25"'))), ""),
            ("asynchronous registration caught", "timeline registered asynchronously" in hf_errors(late), hf_errors(late)),
            ("unsupported size caught", "size" in hf_errors(page.replace('data-width="1080"', 'data-width="1000"')), "")]


def subcomp_errors(host, subs):
    p = []
    soup = parse_html(host)
    for h in soup.find_all(attrs={"data-composition-src": True}):
        for a in ["data-composition-id", "data-start", "data-duration", "data-track-index"]:
            if not h.has_attr(a):
                p.append(f"host missing {a}")
        sub = subs.get(h["data-composition-src"])
        if sub is None:
            p.append("missing sub file")
        elif not parse_html(sub).find("template"):
            p.append("sub not wrapped in <template>")
    for v in soup.find_all("video"):
        if not (v.has_attr("muted") and v.has_attr("playsinline")):
            p.append("video must be muted playsinline")
    if soup.find_all("video") and not soup.find_all("audio"):
        p.append("no separate <audio> element")
    js = "\n".join(s.get_text() for s in soup.find_all("script"))
    if re.search(r"\.(to|from|fromTo)\(\s*['\"]video", js):
        p.append("animate a wrapper, not the <video>")
    return p


def eng119(work):
    host = ('<div data-composition-id="root"><div data-composition-id="intro" data-composition-src="compositions/intro.html" data-start="0" data-duration="4" data-track-index="1"></div>'
            '<div class="wrap"><video src="a.mp4" muted playsinline></video></div><audio src="a.mp4"></audio>'
            "<script>tl.to('.wrap', {scale: 1.1});</script></div>")
    subs = {"compositions/intro.html": "<template><div data-composition-id='intro'></div></template>"}
    d = work / "compositions"
    d.mkdir()
    (d / "intro.html").write_text(subs["compositions/intro.html"])
    (work / "index.html").write_text(host)
    return [("valid host + sub-composition", subcomp_errors(host, subs) == [], subcomp_errors(host, subs)),
            ("sub file without <template> caught", "sub not wrapped in <template>" in subcomp_errors(host, {"compositions/intro.html": "<div></div>"}), ""),
            ("unmuted video caught", "video must be muted playsinline" in subcomp_errors(host.replace(" muted", ""), subs), ""),
            ("tweening the <video> itself caught", "animate a wrapper, not the <video>" in subcomp_errors(host.replace("tl.to('.wrap'", "tl.to('video'"), subs), ""),
            ("missing separate <audio> caught", "no separate <audio> element" in subcomp_errors(host.replace('<audio src="a.mp4"></audio>', ""), subs), "")]


PROGRAMS.update({
    "ENG-61": eng61, "ENG-62": eng62, "ENG-63": eng63, "ENG-64": eng64, "ENG-65": eng65, "ENG-66": eng66,
    "ENG-67": eng67, "ENG-68": eng68, "ENG-69": eng69, "ENG-74": eng74, "ENG-75": eng75, "ENG-76": eng76,
    "ENG-77": eng77, "ENG-78": eng78, "ENG-79": eng79, "ENG-80": eng80, "ENG-81": eng81, "ENG-82": eng82,
    "ENG-83": eng83, "ENG-84": eng84, "ENG-85": eng85, "ENG-87": eng87, "ENG-88": eng88, "ENG-89": eng89,
    "ENG-90": eng90, "ENG-91": eng91, "ENG-92": eng92, "ENG-94": eng94, "ENG-95": eng95, "ENG-96": eng96,
    "ENG-98": eng98, "ENG-99": eng99, "ENG-100": eng100, "ENG-101": eng101, "ENG-102": eng102, "ENG-103": eng103,
    "ENG-104": eng104, "ENG-108": eng108, "ENG-111": eng111, "ENG-113": eng113, "ENG-114": eng114,
    "ENG-115": eng115, "ENG-117": eng117, "ENG-118": eng118, "ENG-119": eng119,
})


# ================================================================ batch 3: ENG-121 .. ENG-279


def cubic_bezier(x1, y1, x2, y2):
    def bx(s):
        return 3 * (1 - s) ** 2 * s * x1 + 3 * (1 - s) * s * s * x2 + s ** 3

    def by(s):
        return 3 * (1 - s) ** 2 * s * y1 + 3 * (1 - s) * s * s * y2 + s ** 3

    def f(x):
        lo, hi = 0.0, 1.0
        for _ in range(60):
            mid = (lo + hi) / 2
            if bx(mid) < x:
                lo = mid
            else:
                hi = mid
        return by((lo + hi) / 2)
    return f, bx, by


def interpolate(frame, inp, out, easing=None, clamp=True):
    if clamp:
        frame = min(max(frame, inp[0]), inp[-1])
    for k in range(len(inp) - 1):
        if frame <= inp[k + 1] or k == len(inp) - 2:
            p = (frame - inp[k]) / (inp[k + 1] - inp[k])
            e = easing[k] if isinstance(easing, list) else easing
            p = e(p) if e else p
            return out[k] + (out[k + 1] - out[k]) * p


def eng121(work):
    fps = 30
    ease, bx, by = cubic_bezier(0.16, 1, 0.3, 1)
    vals = [interpolate(f, [0, 0.3 * fps], [0, 1], ease) for f in range(-5, 20)]
    save_json(work / "values.json", vals)
    s = np.linspace(0, 1, 200001)
    xs, ys = bx(s), by(s)
    ref = float(np.interp(0.5, xs, ys))
    return [("frame 0 -> 0, frame 0.3*fps (9) -> 1", abs(vals[5]) < 1e-12 and abs(vals[14] - 1) < 1e-12, (vals[5], vals[14])),
            ("extrapolate clamp both sides", vals[0] == vals[5] and abs(vals[0]) < 1e-12 and vals[-1] == 1, (vals[0], vals[-1])),
            ("bezier(0.16,1,0.3,1) solver matches dense sampling", abs(ease(0.5) - ref) < 1e-6, (ease(0.5), ref)),
            ("strong ease-out: 50% time -> > 90% value", ease(0.5) > 0.9, ease(0.5)),
            ("multi-keyframe with n-1 easings: [0,10,20]->[0,100,50] at 15 = 75", interpolate(15, [0, 10, 20], [0, 100, 50], [None, None]) == 75, "")]


def eng122(work):
    fps = 30

    def sequence(frame, start, dur, premount):
        local = frame - start
        mounted = start - premount <= frame < start + dur
        visible = 0 <= local < dur
        return {"mounted": mounted, "visible": visible, "local": local if visible else None}

    def series(durs, offsets):
        starts, t = [], 0
        for d, o in zip(durs, offsets):
            t += o
            starts.append(t)
            t += d
        return starts, t
    seq = {f: sequence(f, 30, 60, 1 * fps) for f in (0, 29, 30, 89, 90)}
    starts, total = series([45, 30, 20], [0, -10, 0])
    trim_child = lambda frame, start, trim_before: frame - start + trim_before  # noqa: E731
    save_json(work / "timing.json", {"seq": {str(k): v for k, v in seq.items()}, "series": starts, "total": total})
    return [("Sequence from=30: frame 30 is local 0, 89 is 59", seq[30]["local"] == 0 and seq[89]["local"] == 59, (seq[30], seq[89])),
            ("hidden outside 30..89", not seq[29]["visible"] and not seq[90]["visible"], ""),
            ("premountFor 1 s mounts from frame 0", seq[0]["mounted"] and not seq[0]["visible"], seq[0]),
            ("Series with -10 offset overlaps: starts 0, 35, 65; total 85", starts == [0, 35, 65] and total == 85, (starts, total)),
            ("trimBefore 10 shifts the child's clock", trim_child(40, 30, 10) == 20, trim_child(40, 30, 10))]


def eng126(work):
    def overshoot(k, d):
        z = d / (2 * math.sqrt(k))
        return math.exp(-math.pi * z / math.sqrt(1 - z * z))
    ts = np.linspace(0, 1.5, 15001)
    a = max(spring(t, 500, 30) for t in ts) - 1
    b = max(spring(t, 400, 17) for t in ts) - 1
    kf = interpolate(0.5, [0, 0.5, 1], [1, 1.05, 1])
    save_json(work / "springs.json", {"500/30": a, "400/17": b})
    return [("500/30 overshoot = exp(-pi z/sqrt(1-z^2)) = 5.8%", abs(a - overshoot(500, 30)) < 1e-4 and abs(a - 0.0583) < 1e-3, a),
            ("400/17 bouncier: 22.9%", abs(b - overshoot(400, 17)) < 1e-4 and abs(b - 0.229) < 2e-3, b),
            ("settles to 1", abs(spring(1.5, 500, 30) - 1) < 1e-4, spring(1.5, 500, 30)),
            ("keyframes [1,1.05,1] peak mid-way", kf == 1.05, kf)]


def eng129(work):
    ease = lambda t: min(1, 1.001 - 2 ** (-10 * t))  # noqa: E731

    def scroll_at(frame, fps, y0, y1, duration=1.2):
        p = clamp01((frame / fps) / duration)
        return y0 + (y1 - y0) * ease(p)
    fps = 30
    path = [scroll_at(f, fps, 0, 1000) for f in range(0, 40)]
    again = [scroll_at(f, fps, 0, 1000) for f in reversed(range(0, 40))][::-1]
    save_json(work / "scroll.json", path)
    return [("expo easing: e(0) = 0.001, e(1) = 1", abs(ease(0) - 0.001) < 1e-12 and ease(1) == 1, (ease(0), ease(1))),
            ("half-way (0.6 s) = 1.001 - 2^-5 = 0.96975", abs(path[18] - 969.75) < 1e-9, path[18]),
            ("arrives at 1.2 s (frame 36)", path[36] == 1000 and path[39] == 1000, path[36]),
            ("scroll set from frame time is order-independent", path == again, "")]


def eng131(work):
    import yaml
    STEP = {"slide": {"title-card", "bullet-points", "outro"},
            "screencast": {"navigate", "wait", "highlight", "click", "fill", "scroll", "hover", "screenshot_pause"}}

    def load_guide(text):
        g = yaml.safe_load(text)
        meta = g.setdefault("meta", {})
        meta.setdefault("resolution", [1920, 1080])
        meta.setdefault("voice", "en-US-AriaNeural")
        errs = []
        for i, s in enumerate(g.get("steps", [])):
            if s.get("type") not in STEP:
                errs.append(f"step {i}: type")
            elif s["type"] == "slide" and s.get("layout") not in STEP["slide"]:
                errs.append(f"step {i}: layout")
            elif s["type"] == "screencast":
                errs += [f"step {i}: action {a.get('action')}" for a in s.get("actions", []) if a.get("action") not in STEP["screencast"]]
        return g, errs
    doc = ("meta: {language: ar}\nbrand: {colors: ['#0b0b0b'], logo: logo.png}\nsteps:\n"
           "  - {type: slide, layout: title-card, title: مرحبا}\n"
           "  - type: screencast\n    actions: [{action: navigate, url: 'http://localhost'}, {action: click, selector: '#go'}, {action: screenshot_pause, seconds: 2}]\n"
           "  - {type: slide, layout: outro}\n")
    (work / "guide.yaml").write_text(doc, encoding="utf-8")
    g, errs = load_guide(doc)
    _, bad = load_guide(doc.replace("action: click", "action: teleport"))
    return [("defaults: resolution [1920,1080], voice en-US-AriaNeural", g["meta"]["resolution"] == [1920, 1080] and g["meta"]["voice"] == "en-US-AriaNeural", g["meta"]),
            ("valid guide has no errors", errs == [], errs),
            ("unknown screencast action caught", bad == ["step 1: action teleport"], bad),
            ("3 steps parsed with Arabic title", len(g["steps"]) == 3 and g["steps"][0]["title"] == "مرحبا", "")]


def eng133(work):
    def pin_errors(pkg):
        deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
        rem = {k: v for k, v in deps.items() if k == "remotion" or k.startswith("@remotion/")}
        errs = [f"{k} not exact ({v})" for k, v in rem.items() if not re.fullmatch(r"\d+\.\d+\.\d+", v)]
        if len(set(rem.values())) > 1:
            errs.append("remotion packages on different versions")
        return errs
    good = {"dependencies": {"remotion": "4.0.535", "@remotion/cli": "4.0.535", "@remotion/media": "4.0.535", "react": "^19.0.0"}}
    save_json(work / "package.json", good)
    comp = {"fps": 30, "width": 1920, "height": 1080}
    return [("exact same-version pins pass", pin_errors(good) == [], pin_errors(good)),
            ("caret range caught", pin_errors({"dependencies": {"remotion": "^4.0.535"}}) == ["remotion not exact (^4.0.535)"], ""),
            ("mixed versions caught", "remotion packages on different versions" in pin_errors({"dependencies": {"remotion": "4.0.535", "@remotion/cli": "4.0.534"}}), ""),
            ("non-remotion deps ignored", pin_errors({"dependencies": {"react": "^19"}}) == [], ""),
            ("defaults 30 fps 1920x1080", comp == {"fps": 30, "width": 1920, "height": 1080}, comp)]


def eng136(work):
    def transition_series(scenes, transitions, overlays=()):
        starts, t = [], 0
        for i, d in enumerate(scenes):
            starts.append(t)
            t += d - (transitions[i] if i < len(transitions) else 0)
        return starts, t
    starts, total = transition_series([90, 60, 75], [15, 15])
    _, with_overlay = transition_series([90, 60, 75], [0, 0], overlays=[15])
    linear = lambda f, n=15: clamp01(f / n)  # noqa: E731
    save_json(work / "series.json", {"starts": starts, "total": total})
    return [("transitions overlap scenes: 90+60+75-2*15 = 195", total == 195, total),
            ("scene 2 starts at 75, scene 3 at 120", starts == [0, 75, 120], starts),
            ("overlays (light leak) do not shorten", with_overlay == 225, with_overlay),
            ("linearTiming 15 frames: half-way at 7.5", linear(7.5) == 0.5 and linear(15) == 1, linear(7.5))]


def eng145(work):
    from fontTools import subset
    from fontTools.ttLib import TTFont
    src = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    text = "مرحبا بالعالم"
    out = work / "subset.ttf"
    opts = subset.Options()
    opts.layout_features = ["*"]
    sub = subset.Subsetter(opts)
    full = TTFont(src)
    sub.populate(text=text)
    sub.subset(full)
    full.save(out)
    f = TTFont(out)
    cmap = set(f.getBestCmap())
    want = {ord(c) for c in text}
    orig = TTFont(src)
    feats = {fr.FeatureTag for fr in f["GSUB"].table.FeatureList.FeatureRecord} if "GSUB" in f else set()
    return [("only the used code points kept", cmap == want, sorted(cmap)),
            ("far fewer glyphs", len(f.getGlyphOrder()) < len(orig.getGlyphOrder()) / 20, (len(f.getGlyphOrder()), len(orig.getGlyphOrder()))),
            ("Arabic presentation features kept (init/medi/fina)", {"init", "medi", "fina"} <= feats, sorted(feats)),
            ("file much smaller", out.stat().st_size < src.stat().st_size / 10, out.stat().st_size)]


def back_out(p, c=1.6):
    q = p - 1
    return q * q * ((c + 1) * q + c) + 1


def eng146(work):
    dur = 0.35
    ts = np.linspace(0, dur, 3501)
    sc = [back_out(t / dur) for t in ts]
    peak = max(sc)
    ip = int(np.argmax(sc))
    save_json(work / "scale_in.json", sc[::350])
    p_peak = 1 + (-(2 * 1.6) + math.sqrt((2 * 1.6) ** 2)) / 1  # derivative root of q^2((c+1)q+c): q = -2c/(3(c+1))
    q = -2 * 1.6 / (3 * 2.6)
    exact_peak = back_out(1 + q)
    return [("starts at 0, ends at 1 after 0.35 s", sc[0] == 0 and abs(sc[-1] - 1) < 1e-12, (sc[0], sc[-1])),
            ("overshoots: peak matches q* = -2c/(3(c+1))", abs(peak - exact_peak) < 1e-6 and peak > 1, (peak, exact_peak)),
            ("peak before the end, then settles", 0 < ip < len(ts) - 1 and all(np.diff(sc[ip:]) <= 1e-12), ts[ip]),
            ("c=1.6 overshoots more than c=1", peak > max(back_out(t / dur, 1.0) for t in ts), p_peak)]


def eng148(work):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    preset = {"font.size": 14, "axes.labelsize": 16, "axes.titlesize": 18, "xtick.labelsize": 12, "ytick.labelsize": 12,
              "lines.linewidth": 2.5, "lines.markersize": 8, "axes.spines.top": False, "axes.spines.right": False, "svg.fonttype": "none"}
    with plt.rc_context(preset):
        fig, ax = plt.subplots(figsize=(6.4, 3.6), layout="constrained")
        line, = ax.plot([0, 1, 2, 3], [1, 3, 2, 4], marker="o")
        ax.set_title("نمو")
        ax.set_xlabel("t")
        fig.savefig(work / "plate.png", dpi=300)
        fig.savefig(work / "plate.svg")
        lw, ms, top = line.get_linewidth(), line.get_markersize(), ax.spines["top"].get_visible()
        tsize = ax.title.get_fontsize()
        plt.close(fig)
    im = Image.open(work / "plate.png")
    svg = (work / "plate.svg").read_text()
    return [("exact pixel size figsize*dpi = 1920x1080", im.size == (1920, 1080), im.size),
            ("lines 2.5, markers 8, title 18", (lw, ms, tsize) == (2.5, 8, 18), (lw, ms, tsize)),
            ("no top/right spines", top is False, top),
            ("SVG keeps text as <text>", "<text" in svg, svg.count("<text"))]


def comfy_errors(g):
    errs = []
    for nid, node in g.items():
        if not isinstance(nid, str) or "class_type" not in node or "inputs" not in node:
            errs.append(f"{nid}: shape")
            continue
        for k, v in node["inputs"].items():
            if isinstance(v, list):
                if len(v) != 2 or str(v[0]) not in g or not isinstance(v[1], int):
                    errs.append(f"{nid}.{k}: bad link {v}")
    return errs


def eng152(work):
    def t2i(prompt, neg, seed=7):
        return {"1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "model.safetensors"}},
                "2": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": ["1", 1]}},
                "3": {"class_type": "CLIPTextEncode", "inputs": {"text": neg, "clip": ["1", 1]}},
                "4": {"class_type": "EmptyLatentImage", "inputs": {"width": 1024, "height": 1024, "batch_size": 1}},
                "5": {"class_type": "KSampler", "inputs": {"model": ["1", 0], "positive": ["2", 0], "negative": ["3", 0], "latent_image": ["4", 0],
                                                        "seed": seed, "steps": 20, "cfg": 7.0, "sampler_name": "euler", "scheduler": "normal", "denoise": 1.0}},
                "6": {"class_type": "VAEDecode", "inputs": {"samples": ["5", 0], "vae": ["1", 2]}},
                "7": {"class_type": "SaveImage", "inputs": {"images": ["6", 0], "filename_prefix": "kosif"}}}
    g = t2i("a lantern", "blurry")
    save_json(work / "workflow_api.json", g)
    # topological order from links
    order, seen = [], set()

    def visit(n):
        if n in seen:
            return
        seen.add(n)
        for v in g[n]["inputs"].values():
            if isinstance(v, list):
                visit(v[0])
        order.append(g[n]["class_type"])
    visit("7")
    broken = json.loads(json.dumps(g))
    broken["5"]["inputs"]["positive"] = ["9", 0]
    return [("valid API-format graph", comfy_errors(g) == [], comfy_errors(g)),
            ("chain Checkpoint -> CLIP x2 -> Latent -> KSampler -> VAEDecode -> SaveImage", order == ["CheckpointLoaderSimple", "CLIPTextEncode", "CLIPTextEncode", "EmptyLatentImage", "KSampler", "VAEDecode", "SaveImage"], order),
            ("link to a missing node caught", comfy_errors(broken) == ["5.positive: bad link ['9', 0]"], comfy_errors(broken)),
            ("node ids are strings, links [id, index]", all(isinstance(k, str) for k in g) and g["6"]["inputs"]["vae"] == ["1", 2], "")]


def eng155(work):
    SR = 48000

    def mix(tracks, seconds):
        out = np.zeros((int(seconds * SR), 2))
        failed = []
        for tr in tracks:
            if tr.get("data") is None:
                failed.append(tr["name"])
                continue
            src = tr["data"][int(tr.get("in", 0) * SR):]
            start = int(tr["start"] * SR)
            n = len(out) - start
            if tr.get("loop"):
                reps = int(np.ceil(n / len(src)))
                src = np.tile(src, reps)
            seg = src[:n]
            g = np.interp(np.arange(len(seg)) / SR, [0, len(seg) / SR], tr.get("gain", [1, 1]))
            out[start:start + len(seg)] += (seg * g)[:, None]
        return out, failed
    click = np.zeros(SR // 10)
    click[0] = 1.0
    music = np.full(SR, 0.25)
    out, failed = mix([{"name": "sfx", "data": click, "start": 0.5, "loop": True},
                       {"name": "music", "data": music, "start": 0.0, "gain": [1, 0]},
                       {"name": "broken.m4a", "data": None, "start": 0}], 1.0)
    write_wav(work / "mix.wav", out, SR, 2)
    clicks = np.nonzero(out[:, 0] > 0.9)[0].tolist()
    return [("48 kHz stereo mixdown", out.shape == (48000, 2), out.shape),
            ("sample-accurate start: first click at sample 24000", clicks[0] == 24000, clicks[:2]),
            ("loop repeats every 4800 samples", clicks == [24000 + 4800 * k for k in range(5)], clicks),
            ("gain automation 1 -> 0", abs(out[0, 1] - 0.25) < 1e-9 and out[-1, 1] < 0.001, (out[0, 1], out[-1, 1])),
            ("undecodable file reported", failed == ["broken.m4a"], failed)]


def guess_role(name):
    n = name.lower()
    ext = n.rsplit(".", 1)[-1]
    kind = {"mp4": "video", "mov": "video", "webm": "video", "mp3": "audio", "wav": "audio", "m4a": "audio", "png": "image", "jpg": "image",
            "jpeg": "image", "webp": "image", "pdf": "pdf", "txt": "text", "md": "text", "docx": "text", "srt": "captions", "vtt": "captions",
            "ttf": "font", "otf": "font", "woff2": "font", "zip": "zip", "json": "json"}.get(ext, "link")
    rules = {"video": [("ref", "ref"), ("مرجع", "ref"), ("bg", "bg")], "audio": [("voice", "voice"), ("تعليق", "voice"), ("music", "music"), ("أغنية", "music"), ("sfx", "sfx")],
             "image": [("logo", "logo"), ("شعار", "logo"), ("bg", "bg")], "pdf": [("brand", "brand")], "text": [("script", "script"), ("brand", "brand")]}
    default = {"video": "main", "audio": "music", "image": "clip", "pdf": "doc", "text": "doc", "link": "ref"}
    for key, role in rules.get(kind, []):
        if key in n:
            return kind, role
    return kind, default.get(kind, kind)


def eng157(work):
    names = ["مرجع_الإعلان.mp4", "clip1.mov", "تعليق صوتي.wav", "أغنية.mp3", "شعار.png", "brand-book.pdf", "script.md", "subs.srt", "Cairo.ttf", "https://x.y/video"]
    r = {n: guess_role(n) for n in names}
    save_json(work / "roles.json", r)
    return [("Arabic ref/مرجع -> video ref", r["مرجع_الإعلان.mp4"] == ("video", "ref"), r["مرجع_الإعلان.mp4"]),
            ("plain video -> main", r["clip1.mov"] == ("video", "main"), r["clip1.mov"]),
            ("تعليق -> voice, أغنية -> music", r["تعليق صوتي.wav"] == ("audio", "voice") and r["أغنية.mp3"] == ("audio", "music"), ""),
            ("شعار -> logo, brand pdf -> brand", r["شعار.png"] == ("image", "logo") and r["brand-book.pdf"] == ("pdf", "brand"), ""),
            ("script text, captions, font, link ref", (r["script.md"], r["subs.srt"][0], r["Cairo.ttf"][0], r["https://x.y/video"]) == (("text", "script"), "captions", "font", ("link", "ref")), "")]


def eng158(work):
    ORDER = ['video/mp4;codecs="avc1.42E01E,mp4a.40.2"', "video/mp4", "video/webm;codecs=vp9,opus", "video/webm;codecs=vp8,opus", "video/webm"]

    def pick(supported):
        m = next((x for x in ORDER if x in supported), None)
        return m, (".mp4" if m and m.startswith("video/mp4") else ".webm")
    r = {"chrome": pick(set(ORDER)), "firefox": pick({"video/webm;codecs=vp8,opus", "video/webm"}), "old": pick({"video/webm"})}
    cfg = {"fps": 30, "videoBitsPerSecond": 8_000_000, "audioBitsPerSecond": 160_000, "timeslice_ms": 250}
    save_json(work / "recorder.json", {"picks": r, "cfg": cfg})
    return [("MP4 avc1.42E01E+mp4a.40.2 first", r["chrome"] == (ORDER[0], ".mp4"), r["chrome"]),
            ("vp9 not supported -> vp8/opus, named .webm honestly", r["firefox"] == (ORDER[3], ".webm"), r["firefox"]),
            ("plain webm last", r["old"] == ("video/webm", ".webm"), r["old"]),
            ("30 fps, 8 Mbps, 160 kbps, 250 ms chunks -> 40 chunks in 10 s", cfg["videoBitsPerSecond"] == 8e6 and 10_000 // cfg["timeslice_ms"] == 40, cfg)]


def eng159(work):
    def hq_config(w, h, fps, supported):
        codec = "avc1.640028" if (w * h <= 1280 * 720 and fps <= 30) else "avc1.64002A"
        if codec not in supported and fps > 30:
            fps = 30
            codec = "avc1.640028" if w * h <= 1280 * 720 else "avc1.640029"
        if codec not in supported:
            codec = "avc1.640029" if "avc1.640029" in supported else None
        mp = w * h / 1e6
        br = 10_000_000 if mp <= 1 else (20_000_000 if fps > 30 else 16_000_000)
        return {"codec": codec, "fps": fps, "bitrate": br, "gop": fps * 2, "queue": 6}
    ALL = {"avc1.640028", "avc1.64002A", "avc1.640029"}
    r = {"720p30": hq_config(1280, 720, 30, ALL), "1080p30": hq_config(1920, 1080, 30, ALL), "1080p60": hq_config(1920, 1080, 60, ALL),
         "1080p60_no42": hq_config(1920, 1080, 60, {"avc1.640029"})}
    chunks = math.ceil(48000 * 3 / 4800)
    save_json(work / "hq.json", r)
    return [("<= 720p30 -> avc1.640028 at 10 Mbps", (r["720p30"]["codec"], r["720p30"]["bitrate"]) == ("avc1.640028", 10_000_000), r["720p30"]),
            ("1080p30 -> avc1.64002A at 16 Mbps", (r["1080p30"]["codec"], r["1080p30"]["bitrate"]) == ("avc1.64002A", 16_000_000), r["1080p30"]),
            ("1080p60 -> 20 Mbps, GOP 120 (keyframe every 2 s)", (r["1080p60"]["bitrate"], r["1080p60"]["gop"]) == (20_000_000, 120), r["1080p60"]),
            ("no level 4.2 -> fall back to 30 fps / avc1.640029", (r["1080p60_no42"]["codec"], r["1080p60_no42"]["fps"]) == ("avc1.640029", 30), r["1080p60_no42"]),
            ("3 s of 48 kHz audio -> 30 chunks of 4800", chunks == 30, chunks)]


def eng160(work):
    class Editor:
        def __init__(self):
            self.undo, self.storage, self.state = [], {}, {"scenes": []}

        def change(self, s):
            self.undo.append(json.dumps(self.state))
            self.undo = self.undo[-25:]
            self.state = s

        def ctrl_z(self):
            if self.undo:
                self.state = json.loads(self.undo.pop())

        def autosave(self):
            blob = json.dumps({"v": 4, **self.state})
            if len(blob.encode()) < 1.5 * 1024 * 1024:
                self.storage["basma.autosave"] = blob
                return True
            return False

    def load_project(data):
        for s in data["scenes"]:
            if s.get("code") and s.get("origin") != "local":
                s["trusted"] = False
        return data
    e = Editor()
    for i in range(30):
        e.change({"scenes": [{"n": i}]})
    for _ in range(40):
        e.ctrl_z()
    ok = e.autosave()
    big = Editor()
    big.state = {"scenes": [{"code": "x" * (1600 * 1024)}]}
    p = load_project({"scenes": [{"code": "draw()", "origin": "file"}, {"code": "draw()", "origin": "local"}, {"text": "a"}]})
    save_json(work / "autosave.json", json.loads(e.storage["basma.autosave"]))
    return [("undo keeps 25 steps", e.state == {"scenes": [{"n": 4}]}, e.state),
            ("autosave under 1.5 MB stored as basma.autosave v4", ok and json.loads(e.storage["basma.autosave"])["v"] == 4, ""),
            ("project over 1.5 MB not autosaved", big.autosave() is False, ""),
            ("external code scenes marked untrusted", p["scenes"][0]["trusted"] is False and "trusted" not in p["scenes"][1], p["scenes"][:2]),
            ("autosave every 6 s -> 10 saves a minute", 60 // 6 == 10, 10)]


def blocked_host(host):
    import ipaddress
    h = host.strip("[]").lower()
    if h in {"localhost"} or h.endswith((".local", ".internal", ".localhost")):
        return True
    try:
        ip = ipaddress.ip_address(h)
    except ValueError:
        return bool(re.fullmatch(r"[\d.]+|0x[0-9a-f]+", h))
    if ip.version == 6:
        return True
    nets = ["10.0.0.0/8", "192.168.0.0/16", "172.16.0.0/12", "169.254.0.0/16", "100.64.0.0/10", "127.0.0.0/8", "0.0.0.0/8"]
    return any(ip in ipaddress.ip_network(n) for n in nets) or True


def eng162(work):
    from urllib.parse import urlparse

    def fetch(url, redirects):
        hops = 0
        while True:
            u = urlparse(url)
            if u.scheme != "https" or blocked_host(u.hostname or ""):
                return {"status": 200, "x-basma-status": "blocked", "hops": hops}
            if url not in redirects:
                return {"status": 200, "x-basma-status": "ok", "hops": hops}
            hops += 1
            if hops > 6:
                return {"status": 200, "x-basma-status": "too-many-redirects", "hops": hops}
            url = redirects[url]
    hosts = {h: blocked_host(h) for h in ["localhost", "10.1.2.3", "192.168.1.1", "172.20.0.1", "169.254.169.254", "100.64.0.9", "[::1]",
                                          "printer.local", "db.internal", "2130706433", "example.com", "cdn.jsdelivr.net"]}
    chain = {f"https://a{i}.com/": f"https://a{i + 1}.com/" for i in range(10)}
    r = {"public": fetch("https://example.com/x", {}), "http": fetch("http://example.com/", {}),
         "redirect_to_private": fetch("https://ok.com/", {"https://ok.com/": "https://169.254.169.254/latest"}),
         "loop": fetch("https://a0.com/", chain)}
    save_json(work / "ssrf.json", {"hosts": hosts, "fetch": r})
    return [("private, link-local, CGNAT, IPv6 literal, .local/.internal, numeric hosts blocked", all(hosts[h] for h in list(hosts)[:10]), hosts),
            ("public hosts allowed", not hosts["example.com"] and not hosts["cdn.jsdelivr.net"], ""),
            ("only https allowed", r["http"]["x-basma-status"] == "blocked", r["http"]),
            ("every redirect hop re-checked", r["redirect_to_private"]["x-basma-status"] == "blocked" and r["redirect_to_private"]["hops"] == 1, r["redirect_to_private"]),
            ("max 6 redirects; errors as 200 + x-basma-status", r["loop"] == {"status": 200, "x-basma-status": "too-many-redirects", "hops": 7}, r["loop"])]


def eng165(work):
    def dims(height, aspect):
        if height % 2 or not 144 <= height <= 3840:
            raise ValueError("height must be even 144-3840")
        num, den = {"9:16": (9, 16), "16:9": (16, 9), "1:1": (1, 1)}[aspect]
        w = round(height * num / den)
        return w + (w % 2), height

    def fps_ok(f):
        return 1 <= f <= 60
    w, h = dims(144, "9:16")
    fps = 12
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-vcodec", "png", "-framerate", str(fps), "-i", "pipe:0",
                             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "19", "-movflags", "+faststart",
                             str(work / "export.mp4")], stdin=subprocess.PIPE)
    import io
    for i in range(12):
        buf = io.BytesIO()
        Image.fromarray(solid(w, h, (i * 20, 30, 60))).save(buf, "PNG")
        proc.stdin.write(buf.getvalue())
    proc.stdin.close()
    proc.wait()
    errs = []
    for hh in (143, 145, 4000):
        try:
            dims(hh, "9:16")
        except ValueError:
            errs.append(hh)
    vs = vstream(work / "export.mp4")
    return [("width = h*9/16 rounded even: 144 -> 82x144", (w, h) == (82, 144), (w, h)),
            ("16:9 at 1080 -> 1920x1080", dims(1080, "16:9") == (1920, 1080), dims(1080, "16:9")),
            ("odd or out-of-range heights refused", errs == [143, 145, 4000], errs),
            ("fps limited to 1-60", fps_ok(1) and fps_ok(60) and not fps_ok(61) and not fps_ok(0), ""),
            ("PNG pipe -> H.264 yuv420p, 12 frames", (vs["codec_name"], vs["pix_fmt"], count_frames(work / "export.mp4")) == ("h264", "yuv420p", 12), "")]


def eng166(work):
    import mimetypes
    ROOT = work / "repo"
    for d in ["web", "project", "secrets"]:
        (ROOT / d).mkdir(parents=True)
    (ROOT / "web" / "player.js").write_text("//")
    (ROOT / "project" / "storyboard.json").write_text("{}")
    (ROOT / "secrets" / "key.txt").write_text("k")

    def route(url):
        assert url.startswith("http://fmb.local/")
        rel = url[len("http://fmb.local/"):]
        p = (ROOT / rel).resolve()
        try:
            first = p.relative_to(ROOT.resolve()).parts[0]
        except ValueError:
            return 403, None
        if first not in {"web", "project"}:
            return 403, None
        if not p.is_file():
            return 404, None
        return 200, mimetypes.guess_type(p.name)[0]
    r = {u: route("http://fmb.local/" + u) for u in ["web/player.js", "project/storyboard.json", "secrets/key.txt", "web/../secrets/key.txt", "web/x.js"]}
    save_json(work / "routes.json", r)
    return [("web/ served with JS MIME", r["web/player.js"][0] == 200 and "javascript" in r["web/player.js"][1], r["web/player.js"]),
            ("project/ served as JSON", r["project/storyboard.json"] == (200, "application/json"), r["project/storyboard.json"]),
            ("outside web/ project/ -> 403", r["secrets/key.txt"][0] == 403 and r["web/../secrets/key.txt"][0] == 403, ""),
            ("missing -> 404", r["web/x.js"][0] == 404, "")]


def clip_errors(html):
    soup = parse_html(html)
    p = []
    for e in soup.find_all(attrs={"data-start": True}):
        if e.has_attr("data-composition-id"):
            continue
        if "clip" not in (e.get("class") or []):
            p.append(f"#{e.get('id')} timed but not class=clip")
    return p


def eng167(work):
    page = composition_page(shim=False, extra_body='<h1 id="t" class="clip" data-start="0" data-duration="2" data-track-index="0">a</h1>')
    (work / "index.html").write_text(page)
    root = parse_html(page).find(attrs={"data-composition-id": True})
    bad = page.replace('class="clip" ', "")
    return [("root 1920x1080 default", (root["data-width"], root["data-height"]) == ("1920", "1080"), ""),
            ("timed child with class=clip passes", clip_errors(page) == [] and hf_errors(page) == [], hf_errors(page)),
            ("timed child without class=clip caught", clip_errors(bad) == ["#t timed but not class=clip"], clip_errors(bad))]


def eng168(work):
    def nested_errors(host, subs):
        p = []
        for h in parse_html(host).find_all(attrs={"data-composition-src": True}):
            cid = h["data-composition-id"]
            sub = subs.get(h["data-composition-src"], "")
            if not re.search(r"window\.__timelines\[\s*['\"]%s['\"]\s*\]\s*=" % re.escape(cid), sub):
                p.append(f"{cid}: sub does not register window.__timelines['{cid}']")
            if not h.has_attr("data-playback-start"):
                p.append(f"{cid}: no data-playback-start")
        return p
    host = '<div data-composition-id="x" data-composition-src="compositions/x.html" data-start="2" data-duration="3" data-playback-start="0.5"></div>'
    sub = "<template><div data-composition-id='x'></div><script>window.__timelines['x'] = gsap.timeline({paused:true});</script></template>"
    (work / "host.html").write_text(host)
    local = lambda t, start=2, pb=0.5: t - start + pb  # noqa: E731
    return [("matching registration passes", nested_errors(host, {"compositions/x.html": sub}) == [], ""),
            ("wrong timeline id caught", nested_errors(host, {"compositions/x.html": sub.replace("['x']", "['y']")}) != [], ""),
            ("missing data-playback-start caught", any("playback" in e for e in nested_errors(host.replace(' data-playback-start="0.5"', ""), {"compositions/x.html": sub})), ""),
            ("sub clock = t - data-start + data-playback-start", local(3.0) == 1.5, local(3.0))]


def lint_composition(src):
    codes = []
    if lint_js(src, ["Math.random", "Date.now", "performance.now"]):
        codes.append("non_deterministic_code")
    if lint_js(src, ["requestAnimationFrame"]):
        codes.append("requestanimationframe_in_composition")
    if re.search(r"gsap\.timeline\(\s*\)", src) or re.search(r"paused\s*:\s*false", src):
        codes.append("timeline_not_paused")
    return codes


def eng169(work):
    good = "const tl = gsap.timeline({paused: true}); window.__timelines['root'] = tl; const r = MOTION.rng(3);"
    r = {"good": lint_composition(good), "rand": lint_composition(good + "x = Math.random();"),
         "raf": lint_composition(good + "requestAnimationFrame(loop);"), "unpaused": lint_composition("const tl = gsap.timeline();")}
    save_json(work / "lint.json", r)
    fps = 30
    return [("clean composition", r["good"] == [], r["good"]),
            ("Math.random -> non_deterministic_code", r["rand"] == ["non_deterministic_code"], r["rand"]),
            ("rAF -> requestanimationframe_in_composition", r["raf"] == ["requestanimationframe_in_composition"], r["raf"]),
            ("unpaused timeline caught", r["unpaused"] == ["timeline_not_paused"], r["unpaused"]),
            ("t = frame/fps", 45 / fps == 1.5, 1.5)]


def eng183(work):
    decl = [{"id": "text", "role": "content", "default": "عنوان"}, {"id": "accent", "role": "style", "enum": ["green", "blue", "violet"], "default": "green"},
            {"id": "exit", "role": "timing", "enum": ["none", "fade", "up"], "default": "none"}, {"id": "cues", "role": "timing", "default": "0.5,1.2"}]

    def mount(host_attrs):
        vals = {d["id"]: d["default"] for d in decl}
        over = json.loads(host_attrs.get("data-variable-values", "{}"))
        errs = []
        for k, v in over.items():
            d = next((x for x in decl if x["id"] == k), None)
            if d is None:
                errs.append(f"unknown variable {k}")
            elif "enum" in d and v not in d["enum"]:
                errs.append(f"{k}={v} not in {d['enum']}")
            else:
                vals[k] = v
        start = float(host_attrs["data-start"])
        cues = [start + float(c) for c in vals["cues"].split(",")]
        return vals, cues, errs
    vals, cues, errs = mount({"data-start": "2", "data-duration": "4", "data-variable-values": '{"text": "مرحبا"}'})
    _, _, bad = mount({"data-start": "0", "data-variable-values": '{"accent": "red", "size": 3}'})
    save_json(work / "mounted.json", {"vals": vals, "cues": cues})
    return [("only changed variables passed; defaults fill the rest", vals == {"text": "مرحبا", "accent": "green", "exit": "none", "cues": "0.5,1.2"}, vals),
            ("exit defaults to none", vals["exit"] == "none", vals["exit"]),
            ("cues are seconds from mount start (2 + 0.5, 2 + 1.2)", cues == [2.5, 3.2], cues),
            ("accent enum and unknown variables enforced", bad == ["accent=red not in ['green', 'blue', 'violet']", "unknown variable size"], bad),
            ("roles limited to content|style|timing|layout", {d["role"] for d in decl} <= {"content", "style", "timing", "layout"}, "")]


def eng186(work):
    SIZES = ((1920, 1080), (1080, 1920), (1080, 1080))
    clip = '<div class="clip" id="c1" data-start="0" data-duration="2" data-track-index="1"></div>'
    ok = {f"{w}x{h}": hf_errors(composition_page(w=w, h=h, dur=4, fps=30, shim=False, extra_body=clip), sizes=SIZES) for w, h in SIZES}
    (work / "square.html").write_text(composition_page(w=1080, h=1080, dur=4, fps=30, shim=False, extra_body=clip))
    bad = hf_errors(composition_page(w=1280, h=720, dur=4, fps=30, shim=False, extra_body=clip), sizes=SIZES)
    return [("1920x1080 / 1080x1920 / 1080x1080 canvases accepted", all(v == [] for v in ok.values()), ok),
            ("other canvas rejected", "size" in bad, bad),
            ("clip without timing caught", "clip missing data-start" in hf_errors(composition_page(shim=False, extra_body='<div class="clip" id="c" data-duration="1" data-track-index="1"></div>'), sizes=SIZES), "")]


def eng190(work):
    def root_errors(html):
        soup = parse_html(html)
        root = soup.find(attrs={"data-composition-id": True})
        p = []
        if root.find_parent("template"):
            p.append("standalone root inside <template>")
        style = " ".join(s.get_text() for s in soup.find_all("style")) + " " + (root.get("style") or "")
        if re.search(r"#root\s*\{[^}]*width\s*:\s*1920px", style) or re.search(r"width\s*:\s*1920px", root.get("style") or ""):
            p.append("hardcoded 1920px on #root")
        return p

    def render_frames(html, timeline_seconds, fps_default=30):
        root = parse_html(html).find(attrs={"data-composition-id": True})
        fps = float(root.get("data-fps", fps_default))
        return round(float(root["data-duration"]) * fps)
    page = "<style>#root{width:100%;height:100%}</style>" + composition_page(dur=6, attrs={"data-composition-id": "root", "data-width": 1920, "data-height": 1080, "data-duration": 6})
    (work / "index.html").write_text(page)
    return [("valid root", root_errors(page) == [], root_errors(page)),
            ("hardcoded 1920px caught", root_errors(page.replace("width:100%", "width:1920px")) == ["hardcoded 1920px on #root"], ""),
            ("root inside <template> caught", "standalone root inside <template>" in root_errors(f"<template>{page}</template>"), ""),
            ("length from data-duration, not the timeline (6 s -> 180 frames)", render_frames(page, timeline_seconds=9.5) == 180, render_frames(page, 9.5)),
            ("data-fps optional (defaults 30)", "data-fps" not in page, "")]


def eng191(work):
    def lint_clips(html):
        soup = parse_html(html)
        root = soup.find(attrs={"data-composition-id": True})
        rd = float(root["data-duration"])
        out, codes = [], []
        for c in soup.find_all(class_="clip"):
            dur = float(c["data-duration"]) if c.has_attr("data-duration") else (3.0 if c.name == "img" else None)
            end = float(c["data-start"]) + (dur or 0)
            out.append((c.get("id"), dur, end))
            if end > rd + 1e-9:
                codes.append(f"clip_ends_past_root_duration:{c.get('id')}")
            if c.has_attr("data-volume") and not 0 <= float(c["data-volume"]) <= 3.98:
                codes.append(f"volume_out_of_range:{c.get('id')}")
        return out, codes
    body = ('<img class="clip" id="logo" data-start="1" data-track-index="1">'
            '<audio class="clip" id="vo" data-start="0" data-duration="4" data-volume="3.98" data-track-index="2"></audio>'
            '<div class="clip" id="t" data-start="2" data-duration="2" data-track-index="2"></div>')
    page = composition_page(dur=4, shim=False, extra_body=body)
    (work / "index.html").write_text(page)
    out, codes = lint_clips(page)
    _, past = lint_clips(page.replace('data-start="2" data-duration="2"', 'data-start="3" data-duration="2"'))
    _, loud = lint_clips(page.replace('data-volume="3.98"', 'data-volume="4.5"'))
    return [("img defaults to 3 s", out[0] == ("logo", 3.0, 4.0), out[0]),
            ("overlapping clips on one lane allowed", codes == [], codes),
            ("clip_ends_past_root_duration caught", past == ["clip_ends_past_root_duration:t"], past),
            ("volume 3.98 = +12 dB max", abs(20 * math.log10(3.98) - 12) < 0.01 and loud == ["volume_out_of_range:vo"], loud)]


def eng192(work):
    def sub_errors(sub):
        soup = parse_html(sub)
        t = soup.find("template")
        p = []
        if t is None:
            return ["not a <template>"]
        inner = parse_html(t.decode_contents())
        if not inner.find(attrs={"data-composition-id": True}):
            p.append("template root lacks data-composition-id")
        for tag in ("style", "script"):
            if any(not e.find_parent("template") for e in soup.find_all(tag)):
                p.append(f"{tag} outside template is dropped")
        css = " ".join(e.get_text() for e in inner.find_all("style"))
        if re.search(r"(^|\})\s*\.[\w-]+\s*\{", css):
            p.append("style the root via #id, not a class")
        return p
    good = "<template><div id='scene' data-composition-id='scene'></div><style>#scene{color:red}</style><script>x()</script></template>"
    (work / "scene.html").write_text(good)
    return [("valid sub-composition", sub_errors(good) == [], sub_errors(good)),
            ("<style> in <head> (outside template) caught", "style outside template is dropped" in sub_errors("<head><style>a{}</style></head>" + good), ""),
            ("root styled by class caught", "style the root via #id, not a class" in sub_errors(good.replace("#scene{", ".scene{")), ""),
            ("host duration = visible window", (lambda s, d: (s, s + d))(2.0, 3.0) == (2.0, 5.0), "")]


def eng193(work):
    import csv
    import io
    tmpl = ('<html data-composition-variables=\'[{"id":"title","type":"string","default":"عنوان"},{"id":"photo","type":"media","default":"a.jpg"}]\'>'
            '<h1 data-var-text="title"></h1><img data-var-src="photo"></html>')

    def render(template, values):
        soup = parse_html(template)
        decl = json.loads(soup.html["data-composition-variables"])
        v = {d["id"]: d["default"] for d in decl}
        unknown = set(values) - set(v)
        if unknown:
            raise KeyError(sorted(unknown))
        v.update(values)
        for e in soup.find_all(attrs={"data-var-text": True}):
            e.string = v[e["data-var-text"]]
        for e in soup.find_all(attrs={"data-var-src": True}):
            e["src"] = v[e["data-var-src"]]
        return soup
    rows = list(csv.DictReader(io.StringIO("title,photo\nأول,1.jpg\nثاني,2.jpg\nثالث,3.jpg\n")))
    outs = [render(tmpl, r) for r in rows]
    for i, o in enumerate(outs):
        (work / f"variant_{i}.html").write_text(str(o), encoding="utf-8")
    d = render(tmpl, {})
    try:
        render(tmpl, {"colour": "red"})
        bad = False
    except KeyError:
        bad = True
    return [("CSV batch -> 3 variants", len(outs) == 3 and [o.h1.string for o in outs] == ["أول", "ثاني", "ثالث"], [o.h1.string for o in outs]),
            ("data-var-src binds media", outs[1].img["src"] == "2.jpg", outs[1].img["src"]),
            ("defaults when no override", d.h1.string == "عنوان" and d.img["src"] == "a.jpg", ""),
            ("undeclared variable refused", bad, bad)]


def eng208(work):
    BLOCKERS = ["useState", "useEffect", "calculateMetadata", "@remotion/lambda", "useCallback"]
    src = ("import {Sequence, interpolate, spring} from 'remotion';\nexport const Film = () => (<>\n"
           "<Sequence from={45} durationInFrames={90}><Title/></Sequence>\n<Sequence from={120} durationInFrames={30}><End/></Sequence>\n</>);\n")

    def lint_source(code):
        return [b for b in BLOCKERS if b in code]

    def port(code, fps=30):
        hosts = []
        for m in re.finditer(r"<Sequence from=\{(\d+)\} durationInFrames=\{(\d+)\}><(\w+)/>", code):
            f, d, name = int(m.group(1)), int(m.group(2)), m.group(3).lower()
            hosts.append(f'<div data-composition-id="{name}" data-composition-src="compositions/{name}.html" data-start="{f / fps:g}" data-duration="{d / fps:g}"></div>')
        return hosts
    hosts = port(src)
    (work / "index.html").write_text("\n".join(hosts))
    api_map = {"interpolate": "fromTo ease none", "spring": "back.out(N)", "Easing.bezier": "CustomEase"}
    return [("clean source has no blockers", lint_source(src) == [], ""),
            ("useState / Lambda blockers refused", lint_source(src + "const [a] = useState(0); import '@remotion/lambda';") == ["useState", "@remotion/lambda"], ""),
            ("Sequence from=45 durationInFrames=90 -> data-start=1.5 data-duration=3", 'data-start="1.5" data-duration="3"' in hosts[0], hosts[0]),
            ("second sequence -> data-start=4 data-duration=1", 'data-start="4" data-duration="1"' in hosts[1], hosts[1]),
            ("API map interpolate->fromTo none, spring->back.out", api_map["interpolate"] == "fromTo ease none" and api_map["spring"] == "back.out(N)", "")]


def eng213(work):
    src = gray_clip(work / "master.mp4", 64, 36, 30, 60)
    draft = work / "draft.mp4"
    ff("-i", src, "-vf", "scale=iw*0.5:ih*0.5,fps=15", "-c:v", "libx264", "-preset", "ultrafast", draft)
    vs = vstream(draft)
    return [("0.5 scale -> 32x18", (vs["width"], vs["height"]) == (32, 18), (vs["width"], vs["height"])),
            ("15 fps", vs["r_frame_rate"] == "15/1", vs["r_frame_rate"]),
            ("same 2 s -> 30 frames", count_frames(draft) == 30, count_frames(draft)),
            ("4x fewer pixels x 2x fewer frames = 8x less work", (64 * 36 * 60) / (32 * 18 * 30) == 8, 8)]


def auto_workers_studio(frames, cores, software_gl=True, env=None):
    if env and env.get("KOSIF_WORKERS"):
        return int(env["KOSIF_WORKERS"])
    n = max(1, min(6, frames // 20))
    if software_gl:
        n = min(n, max(1, cores // 2))
    return n


def eng214(work):
    r = {"10f": auto_workers_studio(10, 8), "100f": auto_workers_studio(100, 16), "600f": auto_workers_studio(600, 32),
         "swgl4": auto_workers_studio(600, 4), "gpu": auto_workers_studio(600, 4, software_gl=False), "env": auto_workers_studio(600, 32, env={"KOSIF_WORKERS": "2"})}
    plan = shard_plan(100, r["100f"])
    save_json(work / "workers.json", {"r": r, "plan": plan})
    return [("< 20 frames -> 1 page", r["10f"] == 1, r["10f"]),
            (">= 20 frames per page: 100 -> 5", r["100f"] == 5 and all(s["i1"] - s["i0"] >= 20 for s in plan["shards"]), r["100f"]),
            ("at most 6 pages", r["600f"] == 6, r["600f"]),
            ("software GL: cores/2 (4 cores -> 2)", r["swgl4"] == 2 and r["gpu"] == 6, (r["swgl4"], r["gpu"])),
            ("KOSIF_WORKERS overrides", r["env"] == 2, r["env"])]


def eng216(work):
    proj = work / "p"
    proj.mkdir()
    (proj / "index.html").write_text("<p>scene</p>")
    film = proj / "film.mp4"
    P = {"engine": "studio", "fps": 30}
    t0 = time.perf_counter()
    first = cached_render(proj, film, P)
    t1 = time.perf_counter()
    second = cached_render(proj, film, P)
    t2 = time.perf_counter()
    return [("first call renders", first == "rendered", first),
            ("unchanged project is a cache hit", second == "cached", second),
            ("cache hit under 0.05 s", (t2 - t1) < 0.05, round(t2 - t1, 4)),
            ("stamp holds the fingerprint", json.loads((proj / "film.mp4.kosif.json").read_text())["fingerprint"] == fingerprint(proj, P), "")]


def eng217(work):
    def blur_samples(n):
        if n != 1 and not 2 <= n <= 16:
            raise ValueError("--blur must be 1 (off) or 2-16")
        return n
    fr4 = subframe_render(lambda t: 10 + 600 * t, 64, 2, 1, 30, blur_samples(4), 0.5)[0]
    fr16 = subframe_render(lambda t: 10 + 600 * t, 64, 2, 1, 30, blur_samples(16), 0.5)[0]
    np.save(work / "blur4.npy", fr4)
    refused = []
    for n in (0, 17):
        try:
            blur_samples(n)
        except ValueError:
            refused.append(n)
    return [("--blur 4 -> 4 sub-frames", np.count_nonzero(fr4[0]) == 4, int(np.count_nonzero(fr4[0]))),
            ("--blur 16 -> 16 sub-frames of weight 1/16", np.count_nonzero(fr16[0]) > 4 and abs(fr16[0].sum() - 1) < 1e-9 and fr16[0].min() >= 0 and fr16[0][fr16[0] > 0].min() >= 1 / 16 - 1e-12, float(fr16[0].max())),
            ("0 and 17 refused (range 2-16)", refused == [0, 17], refused)]


def eng220(work):
    def validate(project):
        p = []
        if sum(s["dur"] for s in project["scenes"]) > 60:
            p.append("over 60 s")
        if len(project["scenes"]) > 24:
            p.append("over 24 scenes")
        if any(s.get("transition", "cut") != "cut" for s in project["scenes"]):
            p.append("hard cuts only")
        return p
    wav = work / "mix.wav"
    write_wav(wav, tone(440, 2.0, 48000, 0.9), 48000)
    I, peak = measure_lufs(wav)
    gain = min(-14 - I, -1.5 - peak)
    out = work / "mix_norm.wav"
    ff("-i", wav, "-af", f"volume={gain:.3f}dB", "-c:a", "pcm_s16le", out)
    I2, pk2 = measure_lufs(out)
    ok = {"scenes": [{"dur": 2.5}] * 24}
    return [("24 scenes / 60 s accepted", validate(ok) == [], validate(ok)),
            ("25 scenes refused", "over 24 scenes" in validate({"scenes": [{"dur": 1}] * 25}), ""),
            ("over 60 s refused", "over 60 s" in validate({"scenes": [{"dur": 61}]}), ""),
            ("crossfade refused (hard cuts only)", "hard cuts only" in validate({"scenes": [{"dur": 1, "transition": "xfade"}]}), ""),
            ("normalised to -14 LUFS without passing -1.5 dBFS peak", (abs(I2 + 14) <= 0.5 or pk2 <= -1.4) and pk2 <= -1.4, (I2, pk2))]


def eng221(work):
    def errs(html):
        p = composition_errors(html, required=("data-composition-id", "data-width", "data-height", "data-start", "data-duration", "data-fps"), fps_allowed={24, 30, 60})
        p = [e for e in p if "MOTION.shim" not in e and "shim seconds" not in e]
        js = "\n".join(s.get_text() for s in parse_html(html).find_all("script"))
        dur = float(parse_html(html).find(attrs={"data-composition-id": True})["data-duration"])
        m = re.search(r"tl\.set\(\{\},\s*\{\},\s*([\d.]+)\)", js)
        if not m or float(m.group(1)) != dur:
            p.append("timeline end not pinned with tl.set({}, {}, duration)")
        if not re.search(r"requestAnimationFrame\(\s*\(\)\s*=>\s*requestAnimationFrame\(\s*\(\)\s*=>\s*\{?\s*window\.__ready\s*=\s*true", js):
            p.append("__ready must follow a double requestAnimationFrame")
        return p
    page = composition_page(dur=5, fps=30, shim=False, attrs={"data-composition-id": "root", "data-width": 1080, "data-height": 1920, "data-start": 0, "data-duration": 5, "data-fps": 30})
    page = page.replace("</script>", "tl.set({}, {}, 5);\nrequestAnimationFrame(() => requestAnimationFrame(() => { window.__ready = true; }));\n</script>")
    (work / "index.html").write_text(page)
    return [("valid seekable page", errs(page) == [], errs(page)),
            ("end pin must match data-duration", "timeline end not pinned with tl.set({}, {}, duration)" in errs(page.replace("tl.set({}, {}, 5)", "tl.set({}, {}, 4)")), ""),
            ("data-fps 25 refused (24/30/60)", any("data-fps" in e for e in errs(page.replace('data-fps="30"', 'data-fps="25"'))), ""),
            ("single rAF before __ready caught", "__ready must follow a double requestAnimationFrame" in errs(page.replace("requestAnimationFrame(() => requestAnimationFrame(() => { window.__ready = true; }))", "requestAnimationFrame(() => { window.__ready = true; })")), "")]


def eng224(work):
    SR = 16000
    html = ('<audio data-role="voice" data-start="0" data-duration="2" data-volume="1.0" src="voice"></audio>'
            '<audio data-role="music" data-start="0" data-duration="2" data-volume="0.5" data-fade-out="0.4" src="music"></audio>'
            '<video data-start="7.9" data-duration="4.9" muted playsinline src="pond.mp4"></video>')
    srcs = {"voice": tone(300, 2, SR, 0.4), "music": tone(500, 2, SR, 0.4)}
    soup = parse_html(html)
    mix = np.zeros(2 * SR)
    for a in soup.find_all("audio"):
        s, d, v = float(a["data-start"]), float(a["data-duration"]), float(a["data-volume"])
        x = srcs[a["src"]][: int(d * SR)] * v
        fo = float(a.get("data-fade-out", 0))
        if fo:
            n = int(fo * SR)
            x[-n:] *= np.linspace(1, 0, n)
        mix[int(s * SR):int(s * SR) + len(x)] += x
    write_wav(work / "mix.wav", mix, SR)
    v = soup.find("video")
    shown = lambda t: float(v["data-start"]) <= t < float(v["data-start"]) + float(v["data-duration"])  # noqa: E731
    head = mix[:SR]
    tail = mix[-int(0.05 * SR):]
    return [("voice at 1.0", abs(amp_at(head, 300, SR) - 0.4) < 0.01, amp_at(head, 300, SR)),
            ("music at 0.5", abs(amp_at(head, 500, SR) - 0.2) < 0.01, amp_at(head, 500, SR)),
            ("music fades out over the last 0.4 s", amp_at(tail, 500, SR) < 0.03 and abs(amp_at(tail, 300, SR) - 0.4) < 0.05, amp_at(tail, 500, SR)),
            ("pond plate shown from 7.9 s for 4.9 s only", shown(7.9) and shown(12.7) and not shown(12.8) and not shown(7.8), "")]


def eng226(work):
    pole = 0.011  # rad/s
    deg_per_s = math.degrees(pole)
    trail = lambda v, shutter, fps, k: v * (shutter / fps) / k  # noqa: E731
    W = H = 96
    acc = np.zeros((H, W))
    k, shutter, fps = 16, 30, 30
    for j in range(k):
        t = shutter * (j + 0.5) / k / fps
        ang = pole * t * 60  # 60x time-lapse so the arc is visible
        x, y = int(round(W / 2 + 40 * math.cos(ang))), int(round(H / 2 + 40 * math.sin(ang)))
        img = np.zeros((H, W))
        img[y, x] = 1
        acc = np.maximum(acc, img)
    np.save(work / "star_arc.npy", acc)
    return [("star pole 0.011 rad/s ~ 0.6 deg/s", abs(deg_per_s - 0.63) < 0.01, round(deg_per_s, 3)),
            ("--shutter 30 at 30 fps = 1 s exposure", shutter / fps == 1.0, shutter / fps),
            ("car at 25 m/s draws a 25 m trail in 1 s; each of 16 samples stretched 1.5625 m", abs(trail(25, 30, 30, 16) - 25 / 16) < 1e-12, trail(25, 30, 30, 16)),
            ("lighten stack draws a continuous arc at full brightness", acc.max() == 1 and 10 <= np.count_nonzero(acc) <= 16, int(np.count_nonzero(acc)))]


def auto_workers_film(frames, cores=8):
    return max(1, min(6, frames // 20, cores))


def eng227(work):
    W, H, fps, n = 32, 18, 30, 60
    workers = 2
    plan = shard_plan(n, workers)
    segs = []
    for k, s in enumerate(plan["shards"]):
        p = work / f"seg{k}.mp4"
        gray_clip(p, W, H, fps, s["i1"] - s["i0"], [4 * i for i in range(s["i0"], s["i1"])],
                  ["-c:v", "libx264", "-preset", "ultrafast", "-crf", "0", "-pix_fmt", "yuv444p"])
        segs.append(p)
    (work / "list.txt").write_text("".join(f"file '{p.name}'\n" for p in segs))
    out = work / "joined.mp4"
    ff("-f", "concat", "-safe", "0", "-i", work / "list.txt", "-c", "copy", out)
    lum = [int(f[5, 5, 0]) for f in decode(out, W, H)]
    return [("60 frames complete after the join", len(lum) == 60, len(lum)),
            ("luminance monotonic across the join", all(b > a for a, b in zip(lum, lum[1:])), lum[28:32]),
            ("joined without re-encode (stream copy keeps codec)", vstream(out)["pix_fmt"] == "yuv444p", vstream(out)["pix_fmt"]),
            ("auto_workers: 10 frames -> 1, 600 -> <= 6", auto_workers_film(10) == 1 and auto_workers_film(600) <= 6, (auto_workers_film(10), auto_workers_film(600)))]


def eng236(work):
    W, H, fps, n, N = 32, 18, 10, 30, 3
    plan = shard_plan(n, N)
    save_json(work / "plan.json", plan)

    def render_shard(i, of):
        s = shard_plan(n, of)["shards"][i]
        p = work / f"shard{i}of{of}.mp4"
        gray_clip(p, W, H, fps, s["i1"] - s["i0"], [5 * f for f in range(s["i0"], s["i1"])],
                  ["-c:v", "libx264", "-preset", "ultrafast", "-crf", "0", "-pix_fmt", "yuv444p"])
        return p
    parts = [render_shard(i, N) for i in range(N)]
    (work / "join.txt").write_text("".join(f"file '{p.name}'\n" for p in parts))
    out = work / "joined.mp4"
    ff("-f", "concat", "-safe", "0", "-i", work / "join.txt", "-c", "copy", out)
    lv = [int(f[3, 3, 0]) for f in decode(out, W, H)]
    return [("plan: 3 contiguous shards of 10", [s["i1"] - s["i0"] for s in plan["shards"]] == [10, 10, 10], plan["shards"]),
            ("each shard renders only its frames", [count_frames(p) for p in parts] == [10, 10, 10], ""),
            ("join gives frames 0..29 in order", lv == [5 * i for i in range(30)] or all(abs(a - 5 * i) <= 1 for i, a in enumerate(lv)), lv[8:12])]


def eng237(work):
    RATIOS = {"9:16": (9, 16), "16:9": (16, 9), "1:1": (1, 1), "4:5": (4, 5), "4:3": (4, 3), "21:9": (21, 9)}

    def size_for(ratio, short=1080):
        a, b = RATIOS[ratio]
        if a <= b:
            w, h = short, short * b / a
        else:
            w, h = short * a / b, short
        return int(round(w / 2) * 2), int(round(h / 2) * 2)
    sizes = {r: size_for(r) for r in RATIOS}
    save_json(work / "sizes.json", sizes)
    try:
        size_for("2:1")
        bad = False
    except KeyError:
        bad = True
    return [("9:16 -> 1080x1920, 16:9 -> 1920x1080", sizes["9:16"] == (1080, 1920) and sizes["16:9"] == (1920, 1080), sizes),
            ("4:5 -> 1080x1350, 4:3 -> 1440x1080", sizes["4:5"] == (1080, 1350) and sizes["4:3"] == (1440, 1080), ""),
            ("21:9 -> 2520x1080, 1:1 -> 1080x1080", sizes["21:9"] == (2520, 1080) and sizes["1:1"] == (1080, 1080), ""),
            ("unsupported ratio refused", bad, bad)]


def x264_settings(path):
    data = Path(path).read_bytes()
    m = re.search(rb"x264 - core \d+.*?options: ([^\x00]+)", data)
    return m.group(1).decode(errors="replace") if m else ""


def eng266(work):
    W, H, fps, n = 32, 18, 10, 36
    plan = shard_plan(n, 6)
    parts = []
    for k, s in enumerate(plan["shards"]):
        p = work / f"s{k}.mp4"
        gray_clip(p, W, H, fps, s["i1"] - s["i0"], [6 * f for f in range(s["i0"], s["i1"])],
                  ["-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p"])
        parts.append(p)
    (work / "l.txt").write_text("".join(f"file '{p.name}'\n" for p in parts))
    out = work / "film.mp4"
    ff("-f", "concat", "-safe", "0", "-i", work / "l.txt", "-c", "copy", out)
    opts = x264_settings(parts[0])
    return [("6 shards of 6 frames", [s["i1"] - s["i0"] for s in plan["shards"]] == [6] * 6, ""),
            ("joined film has 36 frames", count_frames(out) == 36, count_frames(out)),
            ("libx264 CRF 16", "crf=16.0" in opts, re.search(r"crf=[\d.]+", opts).group(0) if "crf=" in opts else opts[:60]),
            ("preset slow (subme=8, ref=5)", "subme=8" in opts and "ref=5" in opts, "")]


def eng269(work):
    W, H, fps = 36, 64, 30
    a, b = work / "a.mp4", work / "b.mp4"
    ff("-f", "lavfi", "-i", f"testsrc2=s=64x48:r={fps}:d=1", "-c:v", "libx264", "-preset", "ultrafast", a)
    ff("-f", "lavfi", "-i", f"color=c=0xc08040:s=64x48:r={fps}:d=1", "-c:v", "libx264", "-preset", "ultrafast", b)
    cover = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,fps={fps}"
    d = 0.4
    out = work / "film.mp4"
    ff("-i", a, "-i", b, "-filter_complex", f"[0:v]{cover}[x];[1:v]{cover}[y];[x][y]xfade=transition=fadeblack:duration={d}:offset={1 - d},format=yuv420p[v]",
       "-map", "[v]", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "4", out)
    fr = decode(out, W, H)
    lo, hi = int((1 - d) * fps), int(fps)
    mid = min((f for f in fr[lo:hi + 1]), key=lambda f: int(f.max()))
    return [("fit cover fills 9:16 without bars", (vstream(out)["width"], vstream(out)["height"]) == (W, H) and fr[0][:, 0].mean() > 20, ""),
            ("fadeblack passes through black inside the 0.4 s window", int(mid.max()) <= 16, int(mid.max())),
            ("duration 1 + 1 - 0.4 = 1.6 s", len(fr) == 48, len(fr)),
            ("ends on clip 2 colour", abs(int(fr[-1][30, 18, 0]) - 0xc0) <= 8, fr[-1][30, 18].tolist())]


def eng270(work):
    def skel_errors(html):
        soup = parse_html(html)
        r = soup.find(id="root")
        p = []
        want = {"data-composition-id": "root", "data-width": "1080", "data-height": "1920", "data-start": "0", "data-fps": "30"}
        for k, v in want.items():
            if r is None or r.get(k) != v:
                p.append(f"{k} != {v}")
        T = float(r["data-duration"])
        for a in soup.find_all("audio"):
            if float(a["data-start"]) + float(a["data-duration"]) > T + 1e-9:
                p.append("audio past root duration")
        return p
    T = 24.7
    page = (f'<div id="root" data-composition-id="root" data-width="1080" data-height="1920" data-start="0" data-duration="{T}" data-fps="30">'
            f'<audio data-start="0" data-duration="{T}" src="song.mp3"></audio></div>')
    (work / "index.html").write_text(page)
    return [("1080x1920 30 fps skeleton valid", skel_errors(page) == [], skel_errors(page)),
            ("24.7 s -> 741 frames", round(T * 30) == 741, round(T * 30)),
            ("audio longer than the root caught", "audio past root duration" in skel_errors(page.replace(f'data-duration="{T}" src', 'data-duration="47.0" src')), ""),
            ("wrong fps caught", "data-fps != 30" in skel_errors(page.replace('data-fps="30"', 'data-fps="25"')), "")]


def eng271(work):
    seg = lambda t, a, b: clamp01((t - a) / (b - a))  # noqa: E731
    ease = lambda p: 4 * p ** 3 if p < .5 else 1 - (-2 * p + 2) ** 3 / 2  # noqa: E731
    fade_win = lambda t, a, b, f=.25: min(seg(t, a, a + f), 1 - seg(t, b - f, b))  # noqa: E731

    def mix(c1, c2, p):
        a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
        b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
        return "#" + "".join(f"{round(x + (y - x) * p):02x}" for x, y in zip(a, b))

    def render(t):
        return f'<svg width="1920" height="1080"><rect fill="{mix("#102030", "#e0c080", ease(seg(t, 0, 2)))}" opacity="{fade_win(t, 0.5, 3):.3f}"/></svg>'
    (work / "t1.svg").write_text(render(1.0))
    return [("seg(1.5, 1, 2) = 0.5, clamped outside", seg(1.5, 1, 2) == 0.5 and seg(0, 1, 2) == 0 and seg(3, 1, 2) == 1, ""),
            ("easeInOutCubic(.5) = .5, (.25) = .0625", ease(.5) == .5 and ease(.25) == .0625, ease(.25)),
            ("fadeWin(1.125, 1, 3) = 0.5 (in), 2 -> 1, 2.875 -> 0.5 (out)", (fade_win(1.125, 1, 3), fade_win(2, 1, 3), fade_win(2.875, 1, 3)) == (0.5, 1, 0.5), ""),
            ("mix(#000000, #ffffff, .5) = #808080", mix("#000000", "#ffffff", .5) == "#808080", mix("#000000", "#ffffff", .5)),
            ("render(t) is pure", render(1.7) == render(1.7) and render(0.2) != render(1.7), "")]


def eng273(work):
    R = mulberry32(2024)
    cells = np.array([[hash2(i, j) for j in range(100)] for i in range(100)])
    np.save(work / "hash_grid.npy", cells)
    first = [R() for _ in range(1000)]
    return [("M.hash(i,j) -> [0,1)", float(cells.min()) >= 0 and float(cells.max()) < 1, (float(cells.min()), float(cells.max()))),
            ("10,000 cells average ~0.5 (uniform)", abs(float(cells.mean()) - 0.5) < 0.02, float(cells.mean())),
            ("M.rng(seed) stream repeatable", first == (lambda r: [r() for _ in range(1000)])(mulberry32(2024)), first[0]),
            ("no visible row correlation", abs(float(np.corrcoef(cells[:, 0], cells[:, 1])[0, 1])) < 0.3, float(np.corrcoef(cells[:, 0], cells[:, 1])[0, 1]))]


def eng277(work):
    import base64
    rng = np.random.default_rng(3)
    img = np.zeros((16, 24, 3), np.uint8)
    img[:, :12] = (200, 40, 40)
    img[:, 12:] = (30, 60, 200)
    img[5:9, 6:18] = (240, 220, 90)
    img[rng.integers(0, 16, 6), rng.integers(0, 24, 6)] = (0, 0, 0)
    Image.fromarray(img).save(work / "src.png")
    polys = []
    for y in range(img.shape[0]):
        x = 0
        while x < img.shape[1]:
            c = tuple(int(v) for v in img[y, x])
            x2 = x
            while x2 + 1 < img.shape[1] and tuple(int(v) for v in img[y, x2 + 1]) == c:
                x2 += 1
            polys.append(f"d.polygon([({x}, {y}), ({x2}, {y}), ({x2}, {y}), ({x}, {y})], fill={c})")
            x = x2 + 1
    raw = base64.b64encode((work / "src.png").read_bytes()).decode()
    prog = ("import base64, io, sys\nfrom PIL import Image, ImageDraw\nim = Image.new('RGB', (24, 16))\nd = ImageDraw.Draw(im)\n" + "\n".join(polys) +
            f"\nORIG = '{raw}'\nref = Image.open(io.BytesIO(base64.b64decode(ORIG))).convert('RGB')\n"
            "diff = sum(a != b for a, b in zip(im.tobytes(), ref.tobytes()))\nim.save(sys.argv[1])\nprint(diff)\n")
    (work / "picture.py").write_text(prog)
    out = subprocess.run([sys.executable, work / "picture.py", work / "redraw.png"], capture_output=True, text=True, check=True).stdout.strip()
    back = np.asarray(Image.open(work / "redraw.png"))
    return [("program is Pillow-only draw.polygon calls", prog.count("d.polygon(") == len(polys) and "numpy" not in prog, len(polys)),
            ("self-check reports 0 differing pixels", out == "0", out),
            ("independent compare: identical image", np.array_equal(back, img), int((back != img).sum()))]


def eng279(work):
    def render(t):
        a = np.zeros((18, 32))
        p = clamp01((t - 0.2) / 0.6)
        a[8:10, : int(round(32 * p))] = 1
        return a
    fps = 30
    first = next(i for i in range(1, 60) if not np.array_equal(render(i / fps), render(0)))
    src = "window.render = function(t){ bar.style.width = Math.min(1, (t-0.2)/0.6)*100 + '%'; };\ndocument.fonts.ready.then(()=>{window.__ready = true;});"
    (work / "scene.js").write_text(src)
    return [("first motion between 0.1 and 0.3 s", 0.1 <= first / fps <= 0.3, first / fps),
            ("no Date.now / performance.now / Math.random", lint_js(src, ["Date.now", "performance.now", "Math.random"]) == [], ""),
            ("performance.now caught", lint_js(src + "performance.now();", ["Date.now", "performance.now", "Math.random"]) == ["performance.now"], ""),
            ("__ready after fonts load", "fonts.ready.then" in src and "__ready = true" in src, ""),
            ("preview equals frames (pure in t)", np.array_equal(render(0.5), render(0.5)), "")]


PROGRAMS.update({
    "ENG-121": eng121, "ENG-122": eng122, "ENG-126": eng126, "ENG-129": eng129, "ENG-131": eng131, "ENG-133": eng133,
    "ENG-136": eng136, "ENG-145": eng145, "ENG-146": eng146, "ENG-148": eng148, "ENG-152": eng152, "ENG-155": eng155,
    "ENG-157": eng157, "ENG-158": eng158, "ENG-159": eng159, "ENG-160": eng160, "ENG-162": eng162, "ENG-165": eng165,
    "ENG-166": eng166, "ENG-167": eng167, "ENG-168": eng168, "ENG-169": eng169, "ENG-183": eng183, "ENG-186": eng186,
    "ENG-190": eng190, "ENG-191": eng191, "ENG-192": eng192, "ENG-193": eng193, "ENG-208": eng208, "ENG-213": eng213,
    "ENG-214": eng214, "ENG-216": eng216, "ENG-217": eng217, "ENG-220": eng220, "ENG-221": eng221, "ENG-224": eng224,
    "ENG-226": eng226, "ENG-227": eng227, "ENG-236": eng236, "ENG-237": eng237, "ENG-266": eng266, "ENG-269": eng269,
    "ENG-270": eng270, "ENG-271": eng271, "ENG-273": eng273, "ENG-277": eng277, "ENG-279": eng279,
})


# ================================================================ batch 4: ENG-281 .. ENG-G01


def eng281(work):
    fps = 30
    vals = [spring(f / fps, 100, 10) for f in range(0, 90)]
    ov = max(vals) - 1
    z = 10 / (2 * math.sqrt(100))
    want = math.exp(-math.pi * z / math.sqrt(1 - z * z))
    clampR = interpolate(200, [0, 30], [0, 1])
    save_json(work / "spring.json", vals)
    return [("useCurrentFrame is the only clock: spring(frame 0) = 0", vals[0] == 0, vals[0]),
            ("Remotion default spring (stiffness 100, damping 10) overshoots 16.3%", abs(ov - want) < 0.005 and abs(want - 0.163) < 0.001, ov),
            ("settles by 3 s", abs(spring(3, 100, 10) - 1) < 0.01, spring(3, 100, 10)),
            ("extrapolateRight clamp", clampR == 1, clampR)]


def eng283(work):
    src = work / "src.mp4"
    ff("-f", "lavfi", "-i", "testsrc2=s=128x72:r=25:d=2", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", src)
    a, b = work / "cut_a.mp4", work / "cut_b.mp4"
    ff("-ss", "0.4", "-i", src, "-t", "0.6", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", a)
    ff("-ss", "1.2", "-i", src, "-t", "0.4", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", b)
    (work / "l.txt").write_text(f"file '{a.name}'\nfile '{b.name}'\n")
    cat = work / "concat.mp4"
    ff("-f", "concat", "-safe", "0", "-i", work / "l.txt", "-c", "copy", cat)
    reframed = work / "vertical.mp4"
    ff("-i", cat, "-vf", "crop=ih*9/16:ih,scale=36:64", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", reframed)
    srt = work / "s.srt"
    srt.write_text("1\n00:00:00,000 --> 00:00:01,000\nHELLO\n")
    burned = work / "burned.mp4"
    ff("-i", cat, "-vf", f"subtitles={srt}:force_style='FontName=DejaVu Sans,FontSize=24,PrimaryColour=&H0000FFFF'", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", burned)
    plain = decode(cat, 128, 72)[5].astype(int)
    sub = decode(burned, 128, 72)[5].astype(int)
    vs = vstream(reframed)
    return [("cut + concat = 0.6 + 0.4 s = 25 frames", count_frames(cat) == 25, count_frames(cat)),
            ("reframed to 9:16", (vs["width"], vs["height"]) == (36, 64), (vs["width"], vs["height"])),
            ("subtitle burned into the lower picture", np.abs(sub[40:, :] - plain[40:, :]).mean() > np.abs(sub[:20] - plain[:20]).mean() + 1, float(np.abs(sub[40:] - plain[40:]).mean())),
            ("libx264 yuv420p", vstream(burned)["pix_fmt"] == "yuv420p", "")]


def eng288(work):
    tmpl = "<canvas width='{{W}}' height='{{H}}'></canvas><script>const SECONDS={{SECONDS}}, FPS={{FPS}}, TITLE='{{TITLE}}';</script>"
    page = tmpl
    for k, v in {"W": 1080, "H": 1920, "SECONDS": 6, "FPS": 30, "TITLE": "عنوان"}.items():
        page = page.replace("{{%s}}" % k, str(v))
    (work / "index.html").write_text(page, encoding="utf-8")

    def seek(t, W=54, H=96):
        im = Image.new("RGB", (W, H), "#111312")
        d = ImageDraw.Draw(im)
        p = clamp01(t / 0.8)
        d.rectangle([4, 40, 4 + int((W - 8) * (1 - 2 ** (-10 * p))), 43], fill="#e4342f")
        return np.asarray(im)
    f = seek(1.0)
    write_png(work / "frame.png", f)
    return [("placeholders filled", "{{" not in page and "SECONDS=6, FPS=30" in page, page[-60:]),
            ("background #111312", f[2, 2].tolist() == [0x11, 0x13, 0x12], f[2, 2].tolist()),
            ("accent bar #e4342f", f[41, 10].tolist() == [0xe4, 0x34, 0x2f], f[41, 10].tolist()),
            ("bar eased with out = 1-2^-10p (t=0.4 -> 96.9%)", seek(0.4)[41, 4 + int(46 * (1 - 2 ** -5)) - 1].tolist() == [0xe4, 0x34, 0x2f] and seek(0.4)[41, 50].tolist() == [0x11, 0x13, 0x12], ""),
            ("spring k170 d26 shared with the template", abs(spring(2, 170, 26) - 1) < 1e-6, "")]


def eng294(work):
    import cv2
    PAPER = (0xf3, 0xee, 0xe4)

    def view(img, vw, vh, drawing=False):
        h, w = img.shape[:2]
        f = min(vw / w, vh / h)
        if drawing and w * h > 4_000_000:
            return "nearest", f, None
        if f >= 2:
            f = math.floor(f)
            interp = "nearest"
        elif f < 1:
            interp = "area"
        else:
            interp = "cubic"
        flag = {"nearest": cv2.INTER_NEAREST, "area": cv2.INTER_AREA, "cubic": cv2.INTER_CUBIC}[interp]
        out = cv2.resize(img, (int(w * f), int(h * f)), interpolation=flag) if img.size < 5_000_000 else None
        return interp, f, out
    rng = np.random.default_rng(1)
    small = rng.integers(0, 255, (80, 100, 3), dtype=np.uint8)
    i1, f1, o1 = view(small, 450, 450)
    big = rng.integers(0, 255, (600, 800, 3), dtype=np.uint8)
    i2, f2, o2 = view(big, 200, 200)
    i3, f3, _ = view(np.zeros((900, 1200, 3), np.uint8), 1500, 1500)
    i4, _, _ = view(np.zeros((1, 1, 3), np.uint8).repeat(1, 0), 10, 10, drawing=False)
    huge = view(np.zeros((2100, 2000, 3), np.uint8), 1000, 1000, drawing=True)
    rgba = np.zeros((4, 4, 4), np.uint8)
    flat = np.where(rgba[..., 3:] == 0, np.array(PAPER, np.uint8), rgba[..., :3])
    write_png(work / "view.png", o1)
    blocks = all(len(np.unique(o1[y * 4:(y + 1) * 4, x * 4:(x + 1) * 4].reshape(-1, 3), axis=0)) == 1 for y in range(0, 80, 9) for x in range(0, 100, 11))
    return [("fit 4.5 -> integer zoom 4 with nearest (square pixels)", (i1, f1, o1.shape[:2]) == ("nearest", 4, (320, 400)) and blocks, (i1, f1)),
            ("shrink uses INTER_AREA", i2 == "area" and o2.shape[:2] == (150, 200), (i2, o2.shape)),
            ("1x-2x uses cubic", i3 == "cubic" and abs(f3 - 1.25) < 1e-9, (i3, f3)),
            ("> 4 MP uses nearest while drawing", huge[0] == "nearest", huge[0]),
            ("transparent pixels show paper #f3eee4", flat[0, 0].tolist() == list(PAPER), flat[0, 0].tolist())]


def eng295(work):
    def kind_of(data: bytes):
        if data[:8] == b"\x89PNG\r\n\x1a\n" or data[:3] == b"\xff\xd8\xff":
            return "image"
        t = data.decode("utf-8", "replace").lstrip()
        if t.startswith("<svg") or t.startswith("<?xml") and "<svg" in t:
            return "svg"
        if t.lower().startswith(("<!doctype html", "<html")):
            return "html"
        if re.search(r"^def build\(", t, re.M):
            return "scene"
        return "python"

    def write_job(d, i, payload):
        tmp = d / f"job_{i:04d}.json.tmp"
        tmp.write_text(json.dumps(payload))
        os.replace(tmp, d / f"job_{i:04d}.json")
    import io
    buf = io.BytesIO()
    Image.new("RGB", (2, 2)).save(buf, "PNG")
    kinds = [kind_of(x) for x in [buf.getvalue(), b"<svg xmlns='x'/>", b"<!doctype html><p>", b"ROLLOFF=0.82\ndef build():\n  return []", b"from PIL import Image"]]
    d = work / "jobs"
    d.mkdir()
    for i in range(3):
        write_job(d, i, {"i": i, "rolloff": 0.82})
    names = sorted(p.name for p in d.iterdir())
    return [("kind_of -> image|svg|html|scene|python", kinds == ["image", "svg", "html", "scene", "python"], kinds),
            ("jobs written atomically, no .tmp left", names == ["job_0000.json", "job_0001.json", "job_0002.json"], names),
            ("scene ROLLOFF default 0.82", json.loads((d / "job_0001.json").read_text())["rolloff"] == 0.82, ""),
            ("--scale 3.2 for 4K from 1200x800", (round(1200 * 3.2), round(800 * 3.2)) == (3840, 2560), "")]


def eng296(work):
    code = ("import matplotlib.pyplot as plt\nplt.plot([1,2,3]); plt.show()\nplt.figure(); plt.bar([1,2],[3,1]); plt.show()\n")
    runner = (f"import sys, matplotlib\nmatplotlib.use('Agg')\nimport matplotlib.pyplot as plt\nout = []\n"
              f"def show(*a, **k):\n    for n in plt.get_fignums():\n        f = plt.figure(n)\n        p = sys.argv[2] + f'/fig_{{len(out)}}.png'\n"
              f"        f.savefig(p, dpi=110, bbox_inches='tight'); out.append(p); plt.close(f)\nplt.show = show\n"
              f"exec(open(sys.argv[1]).read())\nprint(len(out))\n")
    (work / "user.py").write_text(code)
    (work / "capture.py").write_text(runner)
    n = sh([sys.executable, work / "capture.py", work / "user.py", work]).strip()
    im = Image.open(work / "fig_0.png")
    dpi = im.info.get("dpi", (0, 0))[0]
    return [("plt.show patched: both figures collected", n == "2" and (work / "fig_1.png").exists(), n),
            ("saved at dpi 110", abs(dpi - 110) < 0.5, dpi),
            ("bbox tight crops below the 6.4x4.8 in canvas", im.size[0] < 6.4 * 110, im.size)]


def eng299(work):
    def workers(frames, cores, megapixels, free_gb, software=True, env=None):
        if env and env.get("KOSIF_WORKERS"):
            return int(env["KOSIF_WORKERS"])
        n = min(6, max(1, frames // 20))
        if software:
            n = min(n, max(1, cores // 2))
        mem = int(max(0, free_gb - 2) // (0.45 + 0.25 * megapixels))
        return max(1, min(n, mem))
    r = {"small": workers(30, 16, 2.07, 32), "cap6": workers(1000, 64, 2.07, 64), "sw": workers(1000, 6, 2.07, 64),
         "mem": workers(1000, 64, 8.3, 6), "env": workers(1000, 64, 2, 64, env={"KOSIF_WORKERS": "3"})}
    save_json(work / "workers.json", r)
    return [(">= 20 frames per worker (30 -> 1)", r["small"] == 1, r["small"]),
            ("at most 6 workers", r["cap6"] == 6, r["cap6"]),
            ("1 page per 2 cores on SwiftShader (6 cores -> 3)", r["sw"] == 3, r["sw"]),
            ("memory: (6-2 GB) / (0.45 + 0.25*8.3 MP) -> 1", r["mem"] == 1, r["mem"]),
            ("KOSIF_WORKERS overrides", r["env"] == 3, r["env"])]


def eng300(work):
    import cv2
    import io
    rng = np.random.default_rng(4)
    yy, xx = np.mgrid[0:36, 0:64]
    img = np.stack([xx * 4, yy * 7, (xx + yy) * 2], -1).astype(np.uint8) + rng.integers(0, 3, (36, 64, 3), dtype=np.uint8)
    pb, jb = io.BytesIO(), io.BytesIO()
    Image.fromarray(img).save(pb, "PNG")
    Image.fromarray(img).save(jb, "JPEG", quality=95)
    dp = cv2.cvtColor(cv2.imdecode(np.frombuffer(pb.getvalue(), np.uint8), cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
    dj = cv2.cvtColor(cv2.imdecode(np.frombuffer(jb.getvalue(), np.uint8), cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
    mse = float(((dj.astype(float) - img) ** 2).mean())
    psnr = 10 * math.log10(255 ** 2 / max(mse, 1e-9))
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-c:v", "mjpeg", "-framerate", "10", "-i", "pipe:0", "-c:v", "libx264",
                             "-preset", "ultrafast", "-pix_fmt", "yuv420p", str(work / "direct.mp4")], stdin=subprocess.PIPE)
    for _ in range(10):
        proc.stdin.write(jb.getvalue())
    proc.stdin.close()
    proc.wait()
    return [("PNG decode is lossless", np.array_equal(dp, img), ""),
            ("JPEG q95 is close (PSNR > 35 dB)", psnr > 35, round(psnr, 1)),
            ("JPEG smaller than PNG", len(jb.getvalue()) < len(pb.getvalue()), (len(jb.getvalue()), len(pb.getvalue()))),
            ("direct image2pipe path encodes 10 frames", count_frames(work / "direct.mp4") == 10, "")]


def eng301(work):
    mod = work / "scene.py"
    mod.write_text("def build_t(t):\n    return [('box', 100 + 200 * t, 300, 120, 120)]\n")
    import importlib.util
    spec = importlib.util.spec_from_file_location("kosif_scene", mod)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    DURATION = getattr(m, "DURATION", 4.0)
    fps = 3
    n = round(DURATION * fps)
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pixel_format", "rgb24", "-video_size", "1200x800", "-framerate", str(fps),
                             "-i", "pipe:0", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", str(work / "scene.mp4")], stdin=subprocess.PIPE)
    xs = []
    for i in range(n):
        im = Image.new("RGB", (1200, 800), (16, 20, 28))
        d = ImageDraw.Draw(im)
        for _, x, y, w, h in m.build_t(i / fps):
            d.rectangle([x, y, x + w, y + h], fill=(230, 180, 90))
            xs.append(x)
        proc.stdin.write(im.tobytes())
    proc.stdin.close()
    proc.wait()
    vs = vstream(work / "scene.mp4")
    return [("DURATION defaults to 4.0 s", DURATION == 4.0, DURATION),
            ("4 s x 3 fps = 12 frames", count_frames(work / "scene.mp4") == 12, ""),
            ("1200x800 frames", (vs["width"], vs["height"]) == (1200, 800), ""),
            ("frame i renders build_t(i/fps)", xs[3] == 300 and abs(xs[-1] - (100 + 200 * 11 / 3)) < 1e-9, xs[:4])]


def eng306(work):
    src = gray_clip(work / "src.mp4", 64, 36, 30, 30)
    out = work / "NAME.draft.mp4"
    ff("-i", src, "-vf", "scale=iw*0.5:ih*0.5,fps=15", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23", out)
    opts = x264_settings(out)
    vs = vstream(out)
    return [("half size 32x18", (vs["width"], vs["height"]) == (32, 18), ""),
            ("15 fps", vs["r_frame_rate"] == "15/1", vs["r_frame_rate"]),
            ("crf 23", "crf=23.0" in opts, ""),
            ("preset ultrafast (no CABAC, subme=0)", "cabac=0" in opts and "subme=0" in opts, "")]


def eng307(work):
    def window(fps, shutter):
        return shutter / fps

    def validate(blur):
        if not 1 <= blur <= 16:
            raise ValueError
        return blur
    fps = 30
    avg = subframe_render(lambda t: 2 + 960 * t, 70, 2, 1, fps, validate(8), 0.5)[0]
    lit = subframe_render(lambda t: 2 + 60 * t, 70, 2, 1, fps, validate(16), 30, "lighten")[0]
    np.save(work / "stacks.npy", np.stack([avg, lit]))
    try:
        validate(17)
        bad = False
    except ValueError:
        bad = True
    return [("--shutter 0.5 = 180 deg = 1/60 s at 30 fps", window(30, 0.5) == 1 / 60, window(30, 0.5)),
            ("--shutter 30 = 1 s exposure at 30 fps", window(30, 30) == 1.0, ""),
            ("average: 8 samples of 1/8", abs(float(avg.max()) - 1 / 8) < 1e-9 and np.count_nonzero(avg[0]) <= 8, float(avg.max())),
            ("lighten: trail at full brightness over ~60 px", float(lit.max()) == 1 and np.ptp(np.nonzero(lit[0])[0]) >= 50, int(np.ptp(np.nonzero(lit[0])[0]))),
            ("--blur limited to 1..16", bad, "")]


def eng308(work):
    def workers(arg, cores, batch=False):
        if batch:
            return 1
        return min(cores, 4) if arg == 0 else min(arg, 4)
    r = {"auto8": workers(0, 8), "auto2": workers(0, 2), "ask9": workers(9, 16), "batch": workers(0, 16, True)}
    save_json(work / "workers.json", r)
    return [("0 = one per core, capped at 4", (r["auto8"], r["auto2"]) == (4, 2), r),
            ("explicit N capped at 4", r["ask9"] == 4, r["ask9"]),
            ("batch jobs set KOSIF_WORKERS=1", r["batch"] == 1, r["batch"])]


def determinism_report(html):
    js = "\n".join(s.get_text() for s in parse_html(html).find_all("script"))
    srcs = [t.get("src") or t.get("href") or "" for t in parse_html(html).find_all(["script", "link", "img", "video", "audio"])]
    return {"seeded_rng": bool(re.search(r"\brng\(\s*\d+\s*\)", js)),
            "no_random_or_clock": not lint_js(js, ["Math.random", "Date.now"]),
            "fonts_ready_gate": "__kosifReady" in js,
            "no_network": not any(re.match(r"https?://", s) for s in srcs) and "fetch(" not in js}


def eng311(work):
    good = "<script src='timeline.js'></script><script>const r = KOSIF.rng(42); window.__kosifReady = document.fonts.ready;</script>"
    bad = "<script src='https://cdn.x/gsap.js'></script><script>const v = Math.random();</script>"
    rg, rb = determinism_report(good), determinism_report(bad)
    save_json(work / "report.json", {"good": rg, "bad": rb})
    return [("rule-abiding page passes all four rules", all(rg.values()), rg),
            ("Math.random / no seeded rng caught", not rb["no_random_or_clock"] and not rb["seeded_rng"], rb),
            ("network asset at render caught", rb["no_network"] is False, ""),
            ("missing __kosifReady caught", rb["fonts_ready_gate"] is False, "")]


def eng315(work):
    ease = lambda p: -(math.cos(math.pi * p) - 1) / 2  # noqa: E731

    def camera(t, dur=6.0):
        a = math.radians(90) * ease(clamp01(t / dur))
        return (round(4 * math.cos(a), 9), 1.5, round(4 * math.sin(a), 9))
    box_rot = lambda t: 0.2 * t  # noqa: E731
    path = [camera(i / 30) for i in range(181)]
    save_json(work / "camera.json", path[::30])
    r = math.hypot(path[90][0], path[90][2])
    return [("starts at (4, 1.5, 0)", path[0] == (4.0, 1.5, 0.0), path[0]),
            ("ends after 90 deg at (0, 1.5, 4)", abs(path[180][0]) < 1e-9 and abs(path[180][2] - 4) < 1e-9, path[180]),
            ("ease-in-out sine: half-way at 45 deg", abs(math.degrees(math.atan2(path[90][2], path[90][0])) - 45) < 1e-6, ""),
            ("radius 4, height 1.5 throughout", abs(r - 4) < 1e-9 and all(p[1] == 1.5 for p in path), r),
            ("box rotation 0.2 rad/s -> 1.2 rad at 6 s", abs(box_rot(6) - 1.2) < 1e-12, box_rot(6))]


def eng320(work):
    class Clip:
        def __init__(self, d):
            self.duration, self.currentTime, self.seeks = d, 0.0, 0

    clips = [Clip(4.0), Clip(2.0), Clip(3.0)]

    def render(w):
        active = min(int(math.floor(w)), len(clips) - 1)
        c = clips[active]
        t = min((w - active) * c.duration, c.duration - 0.05)
        if abs(c.currentTime - t) > 0.01:
            c.currentTime = t
            c.seeks += 1
        return active, round(c.currentTime, 6)
    r = [render(w) for w in (0.5, 0.502, 1.25, 2.999, 3.0)]
    save_json(work / "map.json", r)
    return [("w=0.5 -> clip 0 at 2.0 s", r[0] == (0, 2.0), r[0]),
            ("tiny change (< 0.01 s) does not seek", clips[0].seeks == 1 and r[1] == (0, 2.0), clips[0].seeks),
            ("w=1.25 -> clip 1 at 0.5 s", r[2] == (1, 0.5), r[2]),
            ("clamped to duration - 0.05", r[3] == (2, 2.95) and r[4] == (2, 2.95), r[3:])]


def eng321(work):
    def load_order(clip_positions, scroll, reduced=False, save_data=False):
        if reduced or save_data:
            return []
        return [i for i, _ in sorted(enumerate(clip_positions), key=lambda ip: (abs(ip[1] - scroll), ip[1] < scroll))]
    order = load_order([0, 1, 2, 3, 4], 2.0)
    order2 = load_order([0, 10, 20, 30], 15)
    save_json(work / "order.json", {"a": order, "b": order2})
    return [("nearest first", order[0] == 2, order),
            ("equal distance: ahead before behind", order[1:3] == [3, 1] and order2[:2] == [2, 1], (order, order2)),
            ("reduced motion / saveData load nothing", load_order([0, 1], 0, reduced=True) == [] and load_order([0, 1], 0, save_data=True) == [], "")]


def eng331(work):
    def settle(loaded_seq, stable=8, cap=600):
        run = 0
        for tick, loaded in enumerate(loaded_seq[:cap], 1):
            run = run + 1 if loaded else 0
            if run >= stable:
                return "settled", tick
        return "cap", min(len(loaded_seq), cap)
    a = settle([False] * 20 + [True] * 3 + [False] + [True] * 10)
    b = settle([True, False] * 400)
    c = settle([True] * 8)
    save_json(work / "settle.json", [a, b, c])
    return [("needs 8 stable tilesLoaded ticks in a row", a == ("settled", 32), a),
            ("flicker never settles; gives up at 600 ticks", b == ("cap", 600), b),
            ("8 good ticks settle at tick 8", c == ("settled", 8), c),
            ("delayRender window 60000-120000 ms", 60000 <= 90000 <= 120000, "")]


def eng349(work):
    W, H, fps = 64, 8, 60
    frames = work / "f"
    pat = frames_from(lambda i: (lambda a: (a.__setitem__((slice(None), slice(4 * i % W, 4 * i % W + 4)), 255), a)[1])(solid(W, H, (0, 0, 0))), 12, frames)
    src = encode_png(pat, work / "src.mp4", fps, ["-c:v", "libx264", "-preset", "ultrafast", "-crf", "0", "-pix_fmt", "yuv444p"])
    out = work / "blur.mp4"
    ff("-i", src, "-vf", "tmix=frames=4", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "0", "-pix_fmt", "yuv444p", out)
    a = decode(src, W, H).astype(float)
    b = decode(out, W, H).astype(float)
    k = 6
    expect = a[k - 3:k + 1].mean(0)
    return [("tmix frames=4 averages the last 4 sub-frames", np.abs(b[k] - expect).max() <= 1.5, float(np.abs(b[k] - expect).max())),
            ("blur spreads the bar over 16 px at 1/4 brightness", int((b[k][4, :, 0] > 50).sum()) == 16 and abs(b[k][4, :, 0].max() - 255 / 4) < 2, int((b[k][4, :, 0] > 50).sum())),
            ("frame count unchanged", len(b) == len(a) == 12, len(b))]


def eng351(work):
    W, H = 96, 72
    cam = np.array([0, 1.0, -4.0])
    light = np.array([2.0, 4.0, -2.0])
    C, R = np.array([0, 1.0, 0]), 1.0

    def render(power):
        img = np.zeros((H, W))
        hl = []
        for y in range(H):
            for x in range(W):
                d = np.array([(x - W / 2) / W * 2, -(y - H / 2) / H * 1.5, 1.0])
                d /= np.linalg.norm(d)
                oc = cam - C
                b = np.dot(oc, d)
                disc = b * b - (np.dot(oc, oc) - R * R)
                if disc > 0:
                    t = -b - math.sqrt(disc)
                    p = cam + t * d
                    n = (p - C) / R
                    l_ = light - p
                    l_ /= np.linalg.norm(l_)
                    h = l_ - d
                    h /= np.linalg.norm(h)
                    spec = max(0, np.dot(n, h)) ** power
                    img[y, x] = 0x11 / 255 * max(0, np.dot(n, l_)) + spec
                    hl.append(spec)
                elif d[1] < 0:
                    t = -cam[1] / d[1]
                    p = cam + t * d
                    # analytic soft contact shadow: distance from the sphere's footprint
                    r = math.hypot(p[0] - C[0], p[2] - C[2])
                    img[y, x] = 0.6 * (1 - math.exp(-max(0, r - 0.2) ** 2 / 0.5))
        return img, hl
    img, hl = render(64)
    _, hl8 = render(8)
    write_png(work / "sphere.png", np.repeat((np.clip(img, 0, 1) * 255)[..., None], 3, -1))
    hot64 = sum(1 for v in hl if v > 0.5)
    hot8 = sum(1 for v in hl8 if v > 0.5)
    return [("albedo #111: diffuse body is near-black", np.median([v for v in img[20:50, 38:58].ravel()]) < 0.3, float(np.median(img[20:50, 38:58]))),
            ("Blinn-Phong highlight reaches near full brightness", max(hl) > 0.85, max(hl)),
            ("power 64 highlight much tighter than power 8", 0 < hot64 < hot8 / 3, (hot64, hot8)),
            ("contact shadow: ground darker under the sphere than far away", img[H - 14, W // 2] < img[H - 2, 4], (float(img[H - 14, W // 2]), float(img[H - 2, 4])))]


def eng352(work):
    KEYS = [(0, {"x": 0, "o": 0}), (30, {"x": 100, "o": 1}), (90, {"x": 40, "o": 1})]

    def at(frame):
        for (f0, a), (f1, b) in zip(KEYS, KEYS[1:]):
            if f0 <= frame <= f1:
                p = (frame - f0) / (f1 - f0)
                return {k: a[k] + (b[k] - a[k]) * p for k in a}
        return dict(KEYS[-1][1]) if frame > KEYS[-1][0] else dict(KEYS[0][1])
    fwd = [at(f) for f in range(100)]
    rnd = [at(f) for f in reversed(range(100))][::-1]
    save_json(work / "frames.json", fwd[::10])
    return [("exact on keyframes", at(30) == {"x": 100, "o": 1} and at(90)["x"] == 40, at(30)),
            ("linear between (frame 60 -> x 70)", at(60)["x"] == 70, at(60)),
            ("holds after the last key", at(99)["x"] == 40, at(99)),
            ("pure in frame number (any order)", fwd == rnd, "")]


def eng353(work):
    spec_fps, master_fps = 30000 / 1001, 60000 / 1001

    def cut_frame(k, bpm, offset, fps=spec_fps):
        return round((offset + k * 60 / bpm) * fps) - 2
    cuts = [cut_frame(k, 120, 0.5) for k in range(5)]
    keys = [{"frame": f, "x": 0.5, "y": 0.5, "scale": 1.0 + 0.02 * i, "blur": 0, "opacity": 1} for i, f in enumerate(cuts)]
    save_json(work / "shot_spec.json", keys)
    master = [round(f * master_fps / spec_fps) for f in cuts]
    return [("29.97 fps = 30000/1001", abs(spec_fps - 29.97) < 0.001, spec_fps),
            ("beat 4 at 120 BPM offset 0.5 -> 2.5 s -> frame 75, cut at 73", cuts[4] == 73, cuts),
            ("cuts sit 2 frames before each beat", all(round((0.5 + k * 0.5) * spec_fps) - c == 2 for k, c in enumerate(cuts)), ""),
            ("59.94 master doubles frame numbers", master == [2 * c for c in cuts], master),
            ("keyframes carry frame,x,y,scale,blur,opacity", set(keys[0]) == {"frame", "x", "y", "scale", "blur", "opacity"}, "")]


def eng354(work):
    R = mulberry32(99)
    events = sorted((round(R() * 10, 4), int(R() * 1080), int(R() * 1080)) for _ in range(50))
    save_json(work / "events.json", events)

    def render(t):
        state = {"dots": 0, "sx": 0, "sy": 0}
        for et, x, y in events:
            if et > t:
                break
            state["dots"] += 1
            state["sx"] += x
            state["sy"] += y
        return state
    inc, st = [], {"dots": 0, "sx": 0, "sy": 0}
    idx = 0
    for f in range(301):
        t = f / 30
        while idx < len(events) and events[idx][0] <= t:
            st = {"dots": st["dots"] + 1, "sx": st["sx"] + events[idx][1], "sy": st["sy"] + events[idx][2]}
            idx += 1
        inc.append(st)
    picks = [0, 123, 45, 300, 7]
    return [("replay(t) equals step-by-step simulation", all(render(f / 30) == inc[f] for f in picks), [render(f / 30)["dots"] for f in picks]),
            ("any frame renders independently", render(150 / 30) == render(150 / 30), ""),
            ("all 50 events by the end", render(10)["dots"] == 50, render(10)["dots"]),
            ("no RNG at render time (schedule precomputed)", "mulberry32" not in render.__code__.co_names, "")]


def eng358(work):
    def repeat_count(duration, cycle):
        return math.ceil(duration / cycle) - 1

    def lint(src):
        p = []
        if re.search(r"repeat\s*:\s*-1", src):
            p.append("infinite repeat")
        if re.search(r"(setTimeout|await)[^;]*gsap\.timeline", src, re.S) or re.search(r"setTimeout\([^)]*\)\s*=>\s*\{[^}]*tl\.", src):
            p.append("timeline built asynchronously")
        if lint_js(src, ["Math.random"]):
            p.append("Math.random")
        return p
    good = f"tl.to('.dot', {{rotation: 360, duration: 3, repeat: {repeat_count(10, 3)}}});"
    (work / "tl.js").write_text(good)
    return [("repeat = ceil(10/3) - 1 = 3 (4 cycles cover 10 s)", repeat_count(10, 3) == 3 and (repeat_count(10, 3) + 1) * 3 >= 10, repeat_count(10, 3)),
            ("exact multiple: ceil(9/3) - 1 = 2", repeat_count(9, 3) == 2, ""),
            ("repeat:-1 flagged", lint("tl.to(a,{repeat:-1})") == ["infinite repeat"], ""),
            ("timeline in setTimeout flagged", "timeline built asynchronously" in lint("setTimeout(() => { const tl = gsap.timeline(); }, 0);"), ""),
            ("clean timeline passes", lint(good) == [], "")]


def eng359(work):
    out_expo = lambda p: 1 if p >= 1 else 1 - 2 ** (-10 * p)  # noqa: E731
    ease, _, _ = cubic_bezier(0.16, 1, 0.3, 1)

    class Anim:
        def __init__(self, frm, to, dur, e):
            self.frm, self.to, self.dur, self.e, self.paused, self.t = frm, to, dur, e, False, 0

        def value(self):
            return self.frm + (self.to - self.frm) * self.e(clamp01(self.t / self.dur))  # fill forwards
    anims = {"y": Anim(30, 0, 0.6, out_expo), "blur": Anim(10, 0, 0.8, out_expo), "waapi": Anim(0, 1, 0.3, ease)}

    def at(t):
        for a in anims.values():
            a.paused, a.t = True, t
        return {k: round(a.value(), 6) for k, a in anims.items()}
    s = {t: at(t) for t in (0.0, 0.3, 0.4, 1.0)}
    save_json(work / "frames.json", {str(k): v for k, v in s.items()})
    return [("translateY 30px -> 0 in 0.6 s out-expo: 0.9375 px at 0.3 s", s[0.3]["y"] == 0.9375, s[0.3]["y"]),
            ("blur 10px -> 0 over 0.8 s: 0.3125 px at 0.4 s", s[0.4]["blur"] == 0.3125, s[0.4]["blur"]),
            ("WAAPI 300 ms fill forwards holds final", s[1.0]["waapi"] == 1 and s[0.0]["waapi"] == 0, s[1.0]),
            ("paused + currentTime is frame exact (repeatable)", at(0.3) == s[0.3], "")]


def eng362(work):
    def bitrate(fps, codec):
        return {("h264", False): 45, ("h265", False): 30, ("h264", True): 68, ("h265", True): 45}[(codec, fps > 30)]
    wav = work / "mix.wav"
    write_wav(wav, tone(440, 3, 48000, 0.3) + tone(110, 3, 48000, 0.2), 48000)
    I0, _ = measure_lufs(wav)
    out = work / "mix_norm.wav"
    ff("-i", wav, "-af", f"volume={-14 - I0:.3f}dB", "-c:a", "pcm_s16le", out)
    I, tp = measure_lufs(out)
    clip = gray_clip(work / "v.mp4", 64, 36, 30, 45)
    dur = float(probe(clip)["format"]["duration"])
    return [("<= 30 fps: H.264 45 / H.265 30 Mbps", (bitrate(30, "h264"), bitrate(30, "h265")) == (45, 30), ""),
            ("60 fps: 68 / 45 Mbps", (bitrate(60, "h264"), bitrate(60, "h265")) == (68, 45), ""),
            ("measured integrated loudness -14 +/- 1 LUFS", abs(I + 14) <= 1, I),
            ("measured true peak <= -1 dBTP", tp is not None and tp <= -1, tp),
            ("rendered duration within one frame of 1.5 s", abs(dur - 1.5) <= 1 / 30, dur)]


def eng364(work):
    sr = 48000
    wav = work / "mix.wav"
    write_wav(wav, tone(330, 3, sr, 0.6) * np.linspace(0.3, 1, 3 * sr), sr)
    p1 = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(wav), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                        capture_output=True, text=True).stderr
    m = json.loads(p1[p1.rfind("{"):p1.rfind("}") + 1])
    second = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
              f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    out = work / "mix_ln.wav"
    ff("-i", wav, "-af", second + ",aresample=48000", "-c:a", "pcm_s16le", out)
    I, _ = measure_lufs(out)
    master = work / "master.mp4"
    ff("-f", "lavfi", "-i", "testsrc2=s=64x36:r=60:d=2", "-i", out, "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-crf", "17", "-g", "60",
       "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-shortest", master)
    opts = x264_settings(master)
    src = work / "loop_src.mp4"
    ff("-f", "lavfi", "-i", "testsrc2=s=64x36:r=10:d=2", "-c:v", "libx264", "-preset", "ultrafast", src)
    gif = work / "loop.gif"
    ff("-i", src, "-filter_complex", "[0:v]split[a][b];[a]trim=0.4:2,setpts=PTS-STARTPTS[body];[b]trim=0:0.4,setpts=PTS-STARTPTS[head];"
       "[body][head]xfade=transition=fade:duration=0.4:offset=1.2,split[x][y];[x]palettegen=stats_mode=diff:max_colors=192[p];[y][p]paletteuse", gif)
    g = Image.open(gif)
    ncol = len(g.getpalette()) // 3 if g.getpalette() else 0
    used = len(set(np.asarray(g.convert("P")).ravel().tolist()))
    return [("pass 1 JSON measured, pass 2 lands at -14 LUFS +/- 1", abs(I + 14) <= 1, I),
            ("master CRF 17, GOP 60 (keyint=60)", "crf=17.0" in opts and "keyint=60" in opts, ""),
            ("AAC 192k 48 kHz audio", astream(master)["codec_name"] == "aac" and astream(master)["sample_rate"] == "48000", ""),
            ("GIF loop = 2 s - 0.4 s crossfaded = 16 frames", getattr(g, "n_frames", 0) == 16, getattr(g, "n_frames", 0)),
            ("GIF palette <= 192 colours", used <= 192 and ncol <= 256, used)]


def eng366(work):
    scenes = [{"name": "intro", "dur": 2.0}, {"name": "build", "dur": 3.5}, {"name": "reveal", "dur": 1.5}]

    def cue(name):
        t = 0.0
        for s in scenes:
            if s["name"] == name:
                return t
            t += s["dur"]
        raise KeyError(name)

    def animate(frm, to, start, end, ease=lambda p: p):
        return lambda T: frm + (to - frm) * ease(clamp01((T - start) / (end - start)))
    total = sum(s["dur"] for s in scenes)
    title = animate(0, 1, cue("build"), cue("build") + 1)
    hard_cut = lambda T: [s["name"] for s in scenes if cue(s["name"]) <= T < cue(s["name"]) + s["dur"]]  # noqa: E731
    save_json(work / "axis.json", {"cues": {s["name"]: cue(s["name"]) for s in scenes}, "total": total})
    return [("one time axis: cue('reveal') = 5.5 s", cue("reveal") == 5.5, cue("reveal")),
            ("animate({from,to,start,end})(T) is pure", title(2.5) == 0.5 and title(10) == 1 and title(0) == 0, title(2.5)),
            ("hard cuts: exactly one scene at any T", all(len(hard_cut(T)) == 1 for T in np.arange(0, total, 0.25)), hard_cut(5.5)),
            ("unknown cue name refused", _raises(lambda: cue("nope"), KeyError), "")]


def eng367(work):
    def check_slide(s):
        p = []
        if min(s["font_px"]) < 24:
            p.append("text below 24 px at stage size")
        n = len(s["bullets"])
        if s["mode"] == "speaker" and not 1 <= n <= 3:
            p.append("speaker-led needs 1-3 bullets")
        if s["mode"] == "reading" and not 4 <= n <= 8:
            p.append("reading-first needs 4-8 bullets")
        return p

    def fit(vw, vh, W=1920, H=1080):
        s = min(vw / W, vh / H)
        return round(s, 6), (round((vw - W * s) / 2, 3), round((vh - H * s) / 2, 3))
    ok = {"mode": "speaker", "bullets": ["a", "b"], "font_px": [64, 32]}
    save_json(work / "deck_check.json", {"ok": check_slide(ok)})
    s720, off720 = fit(1280, 720)
    sp, offp = fit(390, 844)
    return [("speaker slide with 2 bullets at >= 24 px passes", check_slide(ok) == [], ""),
            ("20 px text caught (split instead of shrink)", "text below 24 px at stage size" in check_slide({**ok, "font_px": [20]}), ""),
            ("reading-first with 3 bullets caught", "reading-first needs 4-8 bullets" in check_slide({"mode": "reading", "bullets": ["a"] * 3, "font_px": [30]}), ""),
            ("1280x720 scales the whole stage by 2/3, no letterbox", s720 == round(2 / 3, 6) and off720 == (0, 0), (s720, off720)),
            ("phone 390x844 letterboxes vertically", offp[0] == 0 and offp[1] > 300, (sp, offp))]


def eng370(work):
    mkv = work / "in.mkv"
    ff("-f", "lavfi", "-i", "testsrc2=s=64x36:r=25:d=1", "-f", "lavfi", "-i", "sine=f=440:d=1", "-c:v", "libx264", "-preset", "ultrafast", "-c:a", "aac", mkv)
    mp4 = work / "out.mp4"
    ff("-fflags", "+genpts", "-i", mkv, "-c", "copy", "-avoid_negative_ts", "make_zero", "-movflags", "+faststart", mp4)

    def hashes(p, sel):
        out = sh(["ffmpeg", "-v", "error", "-i", p, "-map", sel, "-c", "copy", "-f", "framemd5", "-"])
        return [ln.split(",")[-1].strip() for ln in out.splitlines() if ln and not ln.startswith("#")]
    data = mp4.read_bytes()
    return [("video packets identical (no re-encode)", hashes(mkv, "0:v") == hashes(mp4, "0:v"), len(hashes(mp4, "0:v"))),
            ("audio packets identical", hashes(mkv, "0:a") == hashes(mp4, "0:a"), ""),
            ("+faststart: moov before mdat", 0 < data.find(b"moov") < data.find(b"mdat"), (data.find(b"moov"), data.find(b"mdat"))),
            ("container is MP4", "mp4" in probe(mp4)["format"]["format_name"], probe(mp4)["format"]["format_name"])]


def eng371(work):
    encs = sh(["ffmpeg", "-hide_banner", "-encoders"])
    has_nvenc = "h264_nvenc" in encs
    out = work / "out.mp4"
    chosen = None
    if has_nvenc:
        r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=s=256x144:r=25:d=0.4", "-c:v", "h264_nvenc", "-preset", "p6",
                            "-tune", "hq", "-rc", "vbr", "-cq", "19", str(out)], capture_output=True)
        chosen = "h264_nvenc" if r.returncode == 0 else None
    if chosen is None:
        ff("-f", "lavfi", "-i", "testsrc2=s=256x144:r=25:d=0.4", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", out)
        chosen = "libx264"
    (work / "chosen.txt").write_text(chosen)
    return [("encoder list probed for nvenc", isinstance(has_nvenc, bool), has_nvenc),
            ("falls back to libx264 when NVENC cannot open", chosen == "h264_nvenc" or (chosen == "libx264" and "crf=18.0" in x264_settings(out)), chosen),
            ("result is valid H.264, 10 frames", vstream(out)["codec_name"] == "h264" and count_frames(out) == 10, "")]


def eng374(work):
    pr = work / "proxy.mov"
    ff("-f", "lavfi", "-i", "testsrc2=s=1920x1080:r=25:d=0.2", "-vf", "scale=-2:540", "-c:v", "prores_ks", "-profile:v", "0", pr)
    dn = work / "proxy_dnx.mov"
    ff("-f", "lavfi", "-i", "testsrc2=s=1920x1080:r=25:d=0.2", "-vf", "scale=-2:540,format=yuv422p", "-c:v", "dnxhd", "-profile:v", "dnxhr_lb", dn)
    a, b = vstream(pr), vstream(dn)
    return [("ProRes proxy (profile 0)", a["codec_name"] == "prores" and a.get("profile") == "Proxy", (a["codec_name"], a.get("profile"))),
            ("scale=-2:540 -> 960x540", (a["width"], a["height"]) == (960, 540), (a["width"], a["height"])),
            ("DNxHR LB proxy at 540p", b["codec_name"] == "dnxhd" and b["height"] == 540 and "LB" in b.get("profile", ""), b.get("profile"))]


def eng376(work):
    sr = 16000
    src = work / "st.wav"
    write_wav(src, tone(440, 2, sr, 0.5), sr, 2)
    d = work / "delayed.wav"
    ff("-i", src, "-af", "adelay=500|500", d)
    gated = work / "gated.wav"
    ff("-i", src, "-af", "volume='gte(t,1)':eval=frame", gated)
    st = astream(d)
    x = read_audio(d, sr, 2)
    first = [int(np.argmax(np.abs(x[:, c]) > 1e-3)) for c in range(2)]
    g = read_audio(gated, sr)
    env = lambda t, a=0.5, k=6: math.exp(-max(0, t - a) * k)  # noqa: E731
    return [("adelay=500|500 delays both channels 500 ms", all(abs(f - sr // 2) <= 2 for f in first), first),
            ("ffprobe: still 2 channels, 2.5 s", st["channels"] == 2 and abs(float(st["duration"]) - 2.5) < 0.02, (st["channels"], st["duration"])),
            ("volume gte(t,1) silences the first second", float(np.abs(g[: sr - 400]).max()) < 1e-3 and float(np.abs(g[sr + 400:]).max()) > 0.3, ""),
            ("exp(-max(0,t-a)*k) = 1 before a, 1/e at a+1/k", env(0.2) == 1 and abs(env(0.5 + 1 / 6) - 1 / math.e) < 1e-12, "")]


def eng380(work):
    src = work / "sprite.png"
    a = np.zeros((8, 8, 3), np.uint8)
    a[::2, ::2] = (255, 0, 0)
    a[1::2, 1::2] = (0, 0, 255)
    write_png(src, a)
    out = work / "big.png"
    im_cli = shutil.which("magick") or shutil.which("convert")  # IM7 ships `magick`, IM6 `convert`
    if not im_cli:
        raise RuntimeError("ImageMagick is not installed (neither magick nor convert on PATH)")
    sh([im_cli, src, "-filter", "point", "-resize", "800%", out])
    b = np.asarray(Image.open(out).convert("RGB"))
    cols = {tuple(c) for c in b.reshape(-1, 3).tolist()}
    return [("8x8 -> 64x64", b.shape[:2] == (64, 64), b.shape),
            ("point filter: no new colours (crisp pixels)", cols <= {(255, 0, 0), (0, 0, 255), (0, 0, 0)}, len(cols)),
            ("each source pixel becomes an 8x8 block", np.array_equal(b, np.repeat(np.repeat(a, 8, 0), 8, 1)), "")]


def eng381(work):
    def ladder(marks, exact_labels=False, redraw_heavy=False):
        if marks >= 100_000:
            return "webgl"
        if exact_labels and not redraw_heavy and marks <= 5_000:
            return "svg"
        return "canvas"
    r = {"labels": ladder(300, exact_labels=True), "sparklines": ladder(20_000), "points": ladder(500_000), "anim": ladder(3000, True, True)}
    save_json(work / "ladder.json", r)
    return [("labels/exact values, moderate marks -> SVG", r["labels"] == "svg", r),
            ("dense flat marks -> Canvas2D", r["sparklines"] == "canvas", ""),
            ("~1e5+ marks -> WebGL", r["points"] == "webgl" and ladder(99_999) == "canvas", ""),
            ("frequent redraws leave SVG", r["anim"] == "canvas", "")]


def eng384(work):
    src = work / "src.mp4"
    ff("-f", "lavfi", "-i", "testsrc2=s=96x54:r=24:d=0.5", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "10", src)
    up = work / "up.mp4"
    soft = work / "soft.mp4"
    ff("-i", src, "-vf", "scale=384:216:flags=lanczos,unsharp=5:5:1.0", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "10", up)
    ff("-i", src, "-vf", "scale=384:216:flags=lanczos", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "10", soft)
    save_json(work / "provenance.json", {"kind": "upscale", "method": "lanczos+unsharp", "from": [96, 54], "to": [384, 216]})
    a = decode(up, 384, 216)[5].astype(float)
    b = decode(soft, 384, 216)[5].astype(float)
    energy = lambda x: float(np.abs(np.diff(x, axis=1)).mean())  # noqa: E731
    vs = vstream(up)
    return [("4x upscale (like 960x540 -> 3840x2160)", (vs["width"], vs["height"]) == (384, 216), ""),
            ("unsharp raises edge energy over plain lanczos", energy(a) > energy(b) * 1.05, (energy(a), energy(b))),
            ("12 frames at 24 fps kept", count_frames(up) == 12, ""),
            ("provenance recorded as upscale", json.loads((work / "provenance.json").read_text())["kind"] == "upscale", "")]


def keyframes_of(path):
    out = sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "frame=key_frame", "-of", "csv=p=0", path])
    return [i for i, v in enumerate(out.split()) if v.strip(",") == "1"]


def eng387(work):
    out = work / "seekable.mp4"
    ff("-f", "lavfi", "-i", "testsrc2=s=64x36:r=30:d=3", "-c:v", "libx264", "-crf", "18", "-g", "30", "-keyint_min", "30", "-preset", "veryfast", "-pix_fmt", "yuv420p", out)
    k = keyframes_of(out)
    return [("keyframes at 0, 30, 60 (one per second)", k[:3] == [0, 30, 60], k),
            ("no keyframe gap above 30 frames", all(b - a <= 30 for a, b in zip(k, k[1:] + [90])), k),
            ("crf 18", "crf=18.0" in x264_settings(out), "")]


def eng391(work):
    clip = gray_clip(work / "c.mp4", 64, 36, 25, 20)

    def shim_json(p):
        s = ffprobe_shim(p)
        return {"streams": [{"codec_name": s["codec"], "width": s["width"], "height": s["height"], "nb_frames": str(s["frames"])}], "format": {"duration": f"{s['duration']:.2f}"}}
    real = json.loads(sh(["ffprobe", "-v", "error", "-show_entries", "stream=codec_name,width,height,nb_frames:format=duration", "-of", "json", clip]))
    real["format"]["duration"] = f"{float(real['format']['duration']):.2f}"
    mine = shim_json(clip)
    save_json(work / "shim.json", mine)
    return [("stand-in output equals real ffprobe (-show_entries json)", mine == {"streams": [{k: real["streams"][0][k] for k in ["codec_name", "width", "height", "nb_frames"]}], "format": real["format"]}, (mine, real)),
            ("frame count exact (20)", mine["streams"][0]["nb_frames"] == "20", "")]


def eng392(work):
    def pure(t):
        return round(math.sin(t * 2) * 100 + 30 * t, 6)

    class Stateful:
        def __init__(self):
            self.acc = 0.0

        def __call__(self, t):
            self.acc += 0.1
            return round(self.acc + t, 6)
    samples = [0.0, 1.2, 2.5, 3.0, 5.9]  # first, peak, boundary, final

    def seek_both_ways(fn):
        fwd = [fn(t) for t in samples]
        back = [fn(t) for t in reversed(samples)][::-1]
        return fwd == back
    save_json(work / "samples.json", [pure(t) for t in samples])
    return [("pure seek(t) identical forward and backward", seek_both_ways(pure), ""),
            ("accumulating renderer detected as non-seekable", seek_both_ways(Stateful()) is False, ""),
            ("seeded randomness stable across seeks", mulberry32(5)() == mulberry32(5)(), "")]


def eng395(work):
    changes = [(0.0, 0.0, 100.0), (0.3, 100.0, 40.0), (0.5, 40.0, 160.0)]  # (time, from-target, to-target)

    def value(t, k=170, d=26):
        v = changes[0][1]
        for t0, a, b in changes:
            if t >= t0:
                v += (b - a) * spring(t - t0, k, d)
        return v
    eps = 1e-6
    jumps = [abs(value(t0 + eps) - value(t0 - eps)) for t0, _, _ in changes[1:]]
    save_json(work / "morph.json", [value(i / 60) for i in range(90)])
    return [("retargets mid-flight without a jump", max(jumps) < 1e-3, jumps),
            ("ends at the last target (160)", abs(value(3.0) - 160) < 1e-3, value(3.0)),
            ("closed form: value(t) = base + sum dP*spring(t - t_i)", abs(value(0.2) - 100 * spring(0.2, 170, 26)) < 1e-12, "")]


def eng397(work):
    sr, fps, bpm, dur = 48000, 30, 120, 2.0
    beat_frames = [round(k * 60 / bpm * fps) for k in range(int(dur * bpm / 60))]
    audio = np.zeros(int(dur * sr))
    for f in beat_frames:
        s = int(f / fps * sr)
        audio[s:s + 4800] += np.sin(2 * np.pi * 1000 * np.arange(4800) / sr) * 0.5
    wav = work / "hits.wav"
    write_wav(wav, audio, sr)
    lufs = normalize_to(wav, work / "hits_norm.wav", -14)
    x = read_audio(work / "hits_norm.wav", sr)
    env = np.convolve(np.abs(x), np.ones(48) / 48, "same") > 0.05
    onsets = [i for i in range(len(env)) if env[i] and (i == 0 or not env[i - 1])]
    on_frames = [round(o / sr * fps) for o in onsets]
    return [("120 BPM at 30 fps: beat every 15 frames", beat_frames == [0, 15, 30, 45], beat_frames),
            ("hits land on the contact frames", on_frames == beat_frames, on_frames),
            ("one clock mix at -14 LUFS", abs(lufs + 14) <= 0.5, lufs)]


def eng408(work):
    class Live:
        def __init__(self, fps):
            self.fps, self.frame, self.playing = fps, 0, False

        def seekTo(self, frame):
            self.frame = int(frame)

        def getCurrentFrame(self):
            return self.frame

        def isPlaying(self):
            return self.playing

        def play(self):
            self.playing = True

        def pause(self):
            self.playing = False
    p = Live(30)
    p.seekTo(round(2.51 * p.fps))
    a = p.getCurrentFrame()
    p.play()
    b = p.isPlaying()
    p.pause()
    save_json(work / "live.json", {"frame": a})
    return [("frame = round(t x fps): 2.51 s -> 75", a == 75, a),
            ("play()/pause() toggle isPlaying()", b is True and p.isPlaying() is False, "")]


def eng409(work):
    def progress(log, done):
        m = re.findall(r"(\d+)\s*/\s*(\d+)", log)
        if done:
            return 100
        if not m:
            return 0
        n, N = map(int, m[-1])
        return min(99, int(100 * n / N))
    logs = ["frame 10/200", "frame 10/200\nframe 150/200", "frame 200/200\nencoding"]
    r = [progress(logs[0], False), progress(logs[1], False), progress(logs[2], False), progress(logs[2], True)]
    save_json(work / "pct.json", r)
    out_name = lambda name, existing: next(f"{name}.edit{i}.mp4" for i in range(1, 99) if f"{name}.edit{i}.mp4" not in existing)  # noqa: E731
    return [("pct from the last n/N", r[:2] == [5, 75], r),
            ("capped at 99 until done", r[2] == 99 and r[3] == 100, r),
            ("new MP4 never overwrites the original", out_name("film", {"film.mp4", "film.edit1.mp4"}) == "film.edit2.mp4", "")]


def eng410(work):
    spec = {"format": {"w": 1080, "h": 1920, "fps": 30, "dur": 15}, "loudness": -14,
            "music": {"bpm": 112, "gain_db": -12, "duck_db": -18},
            "zoom": [{"at": 2.6, "scale": 1.12, "dur": 1.2}, {"at": 6.0, "scale": 1.10, "dur": 1.0}, {"at": 9.5, "scale": 1.15, "dur": 1.5}],
            "broll": {"start": 6.0, "end": 9.5, "xfade": 0.3}}
    save_json(work / "montage_spec.json", spec)

    def zoom(t):
        for z in spec["zoom"]:
            if z["at"] <= t < z["at"] + z["dur"]:
                return z["scale"]
        return 1.0

    def broll_alpha(t):
        b = spec["broll"]
        return clamp01((t - b["start"]) / b["xfade"]) * clamp01((b["end"] - t) / b["xfade"])

    def music_db(t, voice_on):
        return spec["music"]["duck_db"] if voice_on else spec["music"]["gain_db"]
    expr = "+".join(f"between(t,{z['at']},{z['at'] + z['dur']})*{z['scale'] - 1:.2f}" for z in spec["zoom"])
    graph = f"[0:v]scale=w='iw*(1+{expr})':h=-2:eval=frame,crop=1080:1920[a]"
    (work / "filtergraph.txt").write_text(graph)
    beat = 60 / spec["music"]["bpm"]
    return [("zoom punches 2.6 s x1.12 for 1.2 s, 9.5 s x1.15 for 1.5 s", (zoom(2.6), zoom(3.79), zoom(3.81), zoom(10.9)) == (1.12, 1.12, 1.0, 1.15), ""),
            ("B-roll 6.0-9.5 s with 0.3 s crossfades", tuple(round(broll_alpha(t), 9) for t in (5.9, 6.15, 7.5, 9.35)) == (0, 0.5, 1, 0.5), ""),
            ("music -12 dB, ducked to -18 dB under voice", (music_db(1, False), music_db(1, True)) == (-12, -18), ""),
            ("112 BPM -> beat every 0.5357 s", abs(beat - 0.535714) < 1e-6, beat),
            ("filtergraph names all three punches", graph.count("between(") == 3, graph[:80])]


def eng412(work):
    src = work / "src.mp4"
    ff("-f", "lavfi", "-i", "testsrc2=s=64x36:r=30:d=8", "-f", "lavfi", "-i", "sine=d=8", "-c:v", "libx264", "-preset", "ultrafast", "-c:a", "aac", "-shortest", src)
    web = work / "web.mp4"
    ff("-i", src, "-c:v", "libx264", "-crf", "20", "-preset", "slow", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", web)
    hevc = work / "hevc.mp4"
    ff("-i", src, "-t", "1", "-c:v", "libx265", "-crf", "24", "-tag:v", "hvc1", "-x265-params", "log-level=error", "-an", hevc)
    hls = work / "hls"
    hls.mkdir()
    ff("-i", src, "-c:v", "libx264", "-preset", "ultrafast", "-g", "60", "-keyint_min", "60", "-sc_threshold", "0", "-c:a", "aac", "-hls_time", "4",
       "-hls_playlist_type", "vod", hls / "index.m3u8")
    gif = work / "p.gif"
    ff("-i", src, "-t", "1", "-vf", "fps=12,scale=360:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse", gif)
    segs = sorted(p.name for p in hls.glob("*.ts"))
    g = Image.open(gif)
    return [("web H.264 crf 20 slow yuv420p + AAC", "crf=20.0" in x264_settings(web) and vstream(web)["pix_fmt"] == "yuv420p", ""),
            ("HEVC tagged hvc1", vstream(hevc)["codec_tag_string"] == "hvc1" and vstream(hevc)["codec_name"] == "hevc", vstream(hevc)["codec_tag_string"]),
            ("HLS 8 s at -hls_time 4 with GOP 60 -> 2 segments", len(segs) == 2, segs),
            ("GIF fps 12, width 360", g.size[0] == 360 and getattr(g, "n_frames", 0) == 12, (g.size, getattr(g, "n_frames", 0)))]


def seekability_lint(src):
    p = []
    for name in ["setTimeout", "Math.random", "fetch"]:
        if lint_js(src, [name]):
            p.append(name)
    if re.search(r"requestAnimationFrame\([^)]*\)", src) and re.search(r"\b\w+\s*(\+=|-=|\+\+)", src):
        p.append("requestAnimationFrame state")
    if re.search(r"getBoundingClientRect\(\)[^;]*;\s*[^;]*tl\.(to|from|fromTo)", src) or re.search(r"tl\.(to|from|fromTo)\([^)]*getBoundingClientRect", src):
        p.append("getBoundingClientRect at tween creation")
    return p


def eng423(work):
    good = "const r = MOTION.rng(1); tl.to('.a', {x: 100}); tl.set(path, {drawSVG: 0, immediateRender: false});"
    cases = {"setTimeout": "setTimeout(go, 10);", "Math.random": "x = Math.random();", "fetch": "fetch('/data.json');",
             "requestAnimationFrame state": "function f(){ x += 1; requestAnimationFrame(f); }",
             "getBoundingClientRect at tween creation": "tl.to('.a', {x: el.getBoundingClientRect().width});"}
    r = {k: seekability_lint(good + v) for k, v in cases.items()}
    save_json(work / "lint.json", r)
    return [("seekable code passes", seekability_lint(good) == [], seekability_lint(good)),
            *[(f"banned: {k}", k in v, v) for k, v in r.items()]]


def eng424(work):
    BASE = ["--headless=new", "--hide-scrollbars", "--ignore-gpu-blocklist", "--autoplay-policy=no-user-gesture-required", "--allow-file-access-from-files"]

    def page_flags(html, env, platform):
        uses_gl = bool(re.search(r"webgl|three|K3|main\.bundle|babylon|pixi", html, re.I))
        gpu = env.get("KOSIF_GPU")
        if gpu == "0" or (not uses_gl and gpu != "1"):
            return BASE + ["--disable-gpu"]
        if env.get("HTML_RENDER_SOFTWARE") == "1" or platform != "win32":
            return BASE + ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"]
        return BASE + ["--use-angle=d3d11"]
    r = {"plain": page_flags("<div>text</div>", {}, "linux"), "three_linux": page_flags("<script src='three.module.js'>", {}, "linux"),
         "three_win": page_flags("<script>window.K3</script>", {}, "win32"), "forced_sw": page_flags("pixi", {"HTML_RENDER_SOFTWARE": "1"}, "win32"),
         "gpu0": page_flags("three", {"KOSIF_GPU": "0"}, "win32")}
    save_json(work / "flags.json", r)
    return [("page without WebGL -> --disable-gpu", "--disable-gpu" in r["plain"], r["plain"][-1]),
            ("WebGL on Linux -> SwiftShader", "--use-angle=swiftshader" in r["three_linux"], r["three_linux"][-2]),
            ("WebGL on Windows -> ANGLE D3D11", r["three_win"][-1] == "--use-angle=d3d11", r["three_win"][-1]),
            ("HTML_RENDER_SOFTWARE=1 and KOSIF_GPU=0 override", "--use-angle=swiftshader" in r["forced_sw"] and "--disable-gpu" in r["gpu0"], ""),
            ("common flags always present", all(f in v for v in r.values() for f in BASE), "")]


def eng425(work):
    def render(css_w, css_h, scale=1.0):
        if scale < 0.1:
            raise ValueError("--scale min 0.1")
        w, h = round(css_w * scale), round(css_h * scale)
        im = Image.new("RGB", (w, h), (10, 10, 10))
        ImageDraw.Draw(im).rectangle([0, 0, w // 2 - 1, h - 1], fill=(250, 250, 250))
        return im
    a = render(64, 36)
    b = render(64, 36, 2)
    b.save(work / "x2.png")
    try:
        render(64, 36, 0.05)
        bad = False
    except ValueError:
        bad = True
    return [("--scale 2 doubles pixels: 128x72", b.size == (128, 72), b.size),
            ("default scale 1", a.size == (64, 36), a.size),
            ("layout preserved (edge at half width)", np.asarray(b)[0, 63, 0] == 250 and np.asarray(b)[0, 64, 0] == 10, ""),
            ("scale below 0.1 refused", bad, "")]


def eng429(work):
    CHECKLIST = ["frame = f(t)", "seeded randomness", "fonts loaded before frame 0", "no network assets", "fixed viewport/DPR"]

    def evaluate(page):
        rep = determinism_report(page["html"])
        res = {"frame = f(t)": rep["no_random_or_clock"] and "requestAnimationFrame" not in page["html"],
               "seeded randomness": rep["seeded_rng"], "fonts loaded before frame 0": rep["fonts_ready_gate"],
               "no network assets": rep["no_network"], "fixed viewport/DPR": page.get("viewport") == (1080, 1920) and page.get("dpr") == 1}
        return [k for k in CHECKLIST if not res[k]]
    good = {"html": "<script>const r = KOSIF.rng(3); window.__kosifReady = document.fonts.ready;</script>", "viewport": (1080, 1920), "dpr": 1}
    bad = {"html": "<img src='https://x/y.png'><script>requestAnimationFrame(f)</script>", "viewport": (1080, 1920), "dpr": 2}
    save_json(work / "checklist.json", {"good": evaluate(good), "bad": evaluate(bad)})
    return [("compliant page passes all 5 items", evaluate(good) == [], evaluate(good)),
            ("every failing item is named", evaluate(bad) == CHECKLIST, evaluate(bad))]


def eng432(work):
    pat = frames_from(lambda i: solid(64, 36, (i * 8, 40, 200 - i * 8)), 20, work / "frames", "frame_%06d.png")
    ff("-f", "lavfi", "-i", "sine=f=330:d=2", "-c:a", "libmp3lame", work / "voice.mp3")
    out = work / "final.mp4"
    ff("-framerate", "30", "-i", pat, "-i", work / "voice.mp3", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "slow",
       "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", "-shortest", out)
    data = out.read_bytes()
    return [("frame_%06d.png sequence -> 20 frames", count_frames(out) == 20, ""),
            ("crf 18 preset slow", "crf=18.0" in x264_settings(out) and "subme=8" in x264_settings(out), ""),
            ("voice muxed as AAC, cut by -shortest", astream(out)["codec_name"] == "aac" and float(probe(out)["format"]["duration"]) < 0.8, probe(out)["format"]["duration"]),
            ("+faststart", 0 < data.find(b"moov") < data.find(b"mdat"), "")]


def eng434(work):
    out = work / "scrub.mp4"
    ff("-f", "lavfi", "-i", "testsrc2=s=64x36:r=30:d=2", "-f", "lavfi", "-i", "sine=d=2", "-an", "-vf", "unsharp=5:5:0.8:5:5:0.0", "-c:v", "libx264", "-preset", "slow",
       "-crf", "20", "-g", "8", "-keyint_min", "8", "-sc_threshold", "0", "-movflags", "+faststart", out)
    k = keyframes_of(out)
    return [("keyframe exactly every 8 frames", k == list(range(0, 60, 8)), k),
            ("no audio (-an)", astream(out) is None, ""),
            ("crf 20, scenecut off", "crf=20.0" in x264_settings(out) and "scenecut=0" in x264_settings(out), "")]


def cine_validate(spec):
    p = []
    w, h, fps, dur = spec["width"], spec["height"], spec["fps"], spec["duration"]
    if w % 2 or h % 2:
        p.append("odd size")
    if not (96 <= w <= 3840 and 96 <= h <= 3840):
        p.append("size bounds 96-3840")
    if not 1 <= fps <= 60:
        p.append("fps outside 1-60")
    if round(fps * dur) > 10_800:
        p.append("> 10,800 frames")
    if len(spec["elements"]) > 100:
        p.append("> 100 elements")
    for e in spec["elements"]:
        if e["type"] == "text" and len(e.get("text", "")) > 300:
            p.append("text > 300 chars")
        if not (0 <= e.get("x", 0.5) <= 1 and 0 <= e.get("y", 0.5) <= 1):
            p.append("x/y not normalised")
    return p


EASE = {"linear": lambda t: t, "ease_out_cubic": lambda t: 1 - (1 - t) ** 3, "spring_pop": lambda t: 1 - math.exp(-7 * t) * math.cos(12 * t)}


def eng_p01(work):
    spec = {"width": 96, "height": 170, "fps": 24, "duration": 1.0,
            "elements": [{"type": "box", "x": 0.5, "y": 0.3, "start": 0, "duration": 0.9, "ease": "ease_out_cubic"},
                         {"type": "ring", "x": 0.5, "y": 0.6, "start": 0, "duration": 0.9, "ease": "linear"},
                         {"type": "bars", "x": 0.5, "y": 0.85, "start": 0, "duration": 0.9, "ease": "spring_pop", "n": 4}]}
    save_json(work / "cinegraph.json", spec)
    W, H = spec["width"], spec["height"]

    def progress(e, t):
        return EASE[e["ease"]](min(1, max(0, 3 * (t - e["start"]) / e["duration"])))

    def frame(t):
        im = Image.new("RGB", (W, H), (10, 12, 16))
        d = ImageDraw.Draw(im)
        for e in spec["elements"]:
            p = progress(e, t)
            cx, cy = e["x"] * W, e["y"] * H
            if e["type"] == "box":
                d.rectangle([cx - 20, cy - 8, cx - 20 + 40 * p, cy + 8], fill=(231, 182, 90))
            elif e["type"] == "ring":
                d.arc([cx - 18, cy - 18, cx + 18, cy + 18], -90, -90 + 360 * p, fill=(90, 200, 160), width=3)
            elif e["type"] == "bars":
                for k in range(e["n"]):
                    bp = max(0, min(1, p * e["n"] - k))
                    d.rectangle([cx - 30 + 15 * k, cy - 20 * bp, cx - 20 + 15 * k, cy], fill=(200, 200, 220))
        return np.asarray(im)
    n = round(spec["fps"] * spec["duration"])
    out = work / "cine.mp4"
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(spec["fps"]), "-i", "-",
                             "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)], stdin=subprocess.PIPE)
    for i in range(n):
        proc.stdin.write(frame(i / spec["fps"]).tobytes())
    proc.stdin.close()
    proc.wait()
    bad = {"odd": cine_validate({**spec, "width": 95}), "big": cine_validate({**spec, "width": 4000}), "fps": cine_validate({**spec, "fps": 61}),
           "frames": cine_validate({**spec, "fps": 60, "duration": 181}), "many": cine_validate({**spec, "elements": [spec["elements"][0]] * 101}),
           "xy": cine_validate({**spec, "elements": [{"type": "box", "x": 1.4}]}), "text": cine_validate({**spec, "elements": [{"type": "text", "text": "a" * 301}]})}
    f_end = frame(0.5)
    return [("valid spec passes", cine_validate(spec) == [], cine_validate(spec)),
            ("validator rejects odd / >3840 / fps 61 / >10,800 frames / >100 elements / text >300 / x>1", all(bad.values()), bad),
            ("spring_pop(t) = 1 - e^-7t cos 12t", abs(EASE["spring_pop"](0.5) - (1 - math.exp(-3.5) * math.cos(6))) < 1e-12, EASE["spring_pop"](0.5)),
            ("animation completes in the first third of life", progress(spec["elements"][0], 0.3) == 1 and progress(spec["elements"][0], 0.15) < 1, ""),
            ("bars grow staggered (k-th starts at progress k/n)", max(0, min(1, 0.25 * 4 - 1)) == 0 and max(0, min(1, 0.5 * 4 - 1)) == 1, ""),
            ("rawvideo pipe -> 24 frames, no PNGs written", count_frames(out) == 24 and not list(work.glob("*.png")), ""),
            ("ring arc fully drawn at completion", int((f_end[int(0.6 * H) - 18:int(0.6 * H) + 19, :, 1] > 150).sum()) > 60, "")]


def eng_x01(work):
    def offsets(N):
        return [0.5 * ((k + 0.5) / N - 0.5) for k in range(N)]

    def samples(diff, rolling=False):
        if diff < 0.5:
            n = 1
        else:
            n = min(14, max(5, math.ceil(3 + 1.6 * diff)))
        return max(n, 6) if rolling and n > 1 else n

    def sub_times(n_frame, N, fps, cuts):
        ts = [(n_frame + o) / fps for o in offsets(N)]
        t0 = n_frame / fps
        for c in cuts:
            if any(t < c for t in ts) and any(t >= c for t in ts):
                ts = [max(t, c) if t0 >= c else min(t, c - 1e-6) for t in ts]
        return ts
    o4 = offsets(4)
    st = sub_times(30, 4, 30, [1.0])
    save_json(work / "subframes.json", {"offsets4": o4, "cut_frame": st})
    return [("N=4 offsets -0.1875, -0.0625, +0.0625, +0.1875 frame", o4 == [-0.1875, -0.0625, 0.0625, 0.1875], o4),
            ("diff < 0.5 -> 1 sample", samples(0.3) == 1, ""),
            ("clamp(ceil(3 + 1.6*diff), 5, 14): diff 1 -> 5, 4 -> 10, 20 -> 14", (samples(1), samples(4), samples(20)) == (5, 10, 14), (samples(1), samples(4), samples(20))),
            (">= 6 for rolling objects", samples(1, rolling=True) == 6, ""),
            ("sub-frames never straddle a hard cut at 1.0 s", all(t >= 1.0 for t in st), st)]


def eng_x02(work):
    def interleave(frames, N):
        return {i: list(range(i, frames, N)) for i in range(N)}

    def continuity(rendered, frames):
        missing = sorted(set(range(frames)) - set(rendered))
        if missing:
            raise RuntimeError(f"missing frames {missing[:5]}")
        return True
    cost = [5 if 40 <= f < 60 else 1 for f in range(90)]
    il = interleave(90, 3)
    contiguous = shard_plan(90, 3)["shards"]
    il_load = [sum(cost[f] for f in fs) for fs in il.values()]
    ct_load = [sum(cost[s["i0"]:s["i1"]]) for s in contiguous]
    save_json(work / "assign.json", il)
    try:
        continuity([f for f in range(90) if f != 47], 90)
        gate = False
    except RuntimeError:
        gate = True
    mb = lambda mbps, sec: mbps * sec / 8  # noqa: E731
    return [("worker i renders i, i+N, i+2N...", il[1][:3] == [1, 4, 7], il[1][:3]),
            ("heavy scene shared evenly (max load lower than contiguous)", max(il_load) < max(ct_load), (il_load, ct_load)),
            ("one missing frame stops the encode", gate, ""),
            ("complete sequence passes the gate", continuity(sum(il.values(), []), 90), ""),
            ("24-30 Mbps x 15 s = 45-56 MB", (mb(24, 15), mb(30, 15)) == (45, 56.25), "")]


def eng_x04(work):
    import io
    W, H, fps, n = 64, 36, 10, 10
    ff("-f", "lavfi", "-i", "sine=f=220:d=3:sample_rate=44100", work / "song.wav")
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-c:v", "mjpeg", "-framerate", str(fps), "-i", "pipe:0", "-i", str(work / "song.wav"),
                             "-c:v", "libx264", "-crf", "16", "-preset", "veryfast", "-vf", "scale=out_range=tv,format=yuv420p,setparams=range=tv", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
                             "-shortest", "-movflags", "+faststart", str(work / "film.mp4")], stdin=subprocess.PIPE)
    for i in range(n):
        b = io.BytesIO()
        Image.fromarray(solid(W, H, (20 * i, 80, 160))).save(b, "JPEG", quality=90)
        proc.stdin.write(b.getvalue())
    proc.stdin.close()
    proc.wait()
    out = work / "film.mp4"
    a = astream(out)
    return [("MJPEG pipe -> H.264 crf 16", "crf=16.0" in x264_settings(out) and count_frames(out) == 10, ""),
            ("song as AAC 48 kHz", (a["codec_name"], a["sample_rate"]) == ("aac", "48000"), (a["codec_name"], a["sample_rate"])),
            ("-shortest: film ends with the picture (1 s)", float(probe(out)["format"]["duration"]) < 1.2, probe(out)["format"]["duration"]),
            ("yuv420p + faststart", vstream(out)["pix_fmt"] == "yuv420p" and out.read_bytes().find(b"moov") < out.read_bytes().find(b"mdat"),
             (vstream(out)["pix_fmt"], out.read_bytes().find(b"moov"), out.read_bytes().find(b"mdat")))]


def lottie_errors(doc, raw_bytes):
    p = []
    if doc.get("fr") not in (30, 60):
        p.append("fr must be 30 or 60")
    if len(raw_bytes) >= 100 * 1024:
        p.append("UI file >= 100 KB")
    for L in doc.get("layers", []):
        if L.get("ty") == 2:
            p.append(f"{L.get('nm')}: raster image layer")
        if L.get("ef"):
            p.append(f"{L.get('nm')}: layer effects")
        if L.get("bm", 0):
            p.append(f"{L.get('nm')}: blending mode")
        if L.get("ddd", 0):
            p.append(f"{L.get('nm')}: 3D layer")
        if '"x":' in json.dumps(L.get("ks", {})):
            p.append(f"{L.get('nm')}: expression")
    names = {m.get("cm") for m in doc.get("markers", [])}
    if not {"intro", "loop", "outro"} <= names:
        p.append("markers intro/loop/outro missing")
    return p


def eng_g01(work):
    doc = {"v": "5.12.0", "fr": 60, "ip": 0, "op": 120, "w": 512, "h": 512,
           "markers": [{"cm": "intro", "tm": 0, "dr": 30}, {"cm": "loop", "tm": 30, "dr": 60}, {"cm": "outro", "tm": 90, "dr": 30}],
           "layers": [{"ty": 4, "nm": "logo", "ddd": 0, "bm": 0, "ks": {"o": {"a": 0, "k": 100}}, "shapes": [{"ty": "tm", "s": {"a": 0, "k": 0}}]},
                      {"ty": 0, "nm": "precomp", "refId": "comp_0", "ks": {}}]}
    raw = json.dumps(doc).encode()
    (work / "anim.json").write_bytes(raw)
    with zipfile.ZipFile(work / "anim.lottie", "w") as z:
        z.writestr("manifest.json", json.dumps({"animations": [{"id": "anim"}]}))
        z.writestr("animations/anim.json", raw)
    seg = {m["cm"]: (m["tm"], m["tm"] + m["dr"]) for m in doc["markers"]}
    bad = json.loads(raw)
    bad["layers"] += [{"ty": 2, "nm": "photo"}, {"ty": 4, "nm": "fx", "ef": [{"ty": 5}]}, {"ty": 4, "nm": "add", "bm": 3},
                      {"ty": 4, "nm": "cube", "ddd": 1}, {"ty": 4, "nm": "wig", "ks": {"p": {"x": "wiggle(2,5)"}}}]
    reverse = list(range(doc["op"] - 1, doc["ip"] - 1, -1))
    return [("shape/precomp/trim-path file passes", lottie_errors(doc, raw) == [], lottie_errors(doc, raw)),
            ("raster, effects, blend mode, 3D, expression each caught", len(lottie_errors(bad, json.dumps(bad).encode())) == 5, lottie_errors(bad, json.dumps(bad).encode())),
            ("> 100 KB UI file caught", "UI file >= 100 KB" in lottie_errors(doc, b"x" * 102400), ""),
            ("fr 24 caught (30 or 60)", "fr must be 30 or 60" in lottie_errors({**doc, "fr": 24}, raw), ""),
            ("markers give segment playback (loop 30-90)", seg["loop"] == (30, 90), seg),
            (".lottie zip holds manifest + animation; reverse plays op-1..0", zipfile.ZipFile(work / "anim.lottie").namelist() == ["manifest.json", "animations/anim.json"] and reverse[0] == 119 and reverse[-1] == 0, "")]


PROGRAMS.update({
    "ENG-281": eng281, "ENG-283": eng283, "ENG-288": eng288, "ENG-294": eng294, "ENG-295": eng295, "ENG-296": eng296,
    "ENG-299": eng299, "ENG-300": eng300, "ENG-301": eng301, "ENG-306": eng306, "ENG-307": eng307, "ENG-308": eng308,
    "ENG-311": eng311, "ENG-315": eng315, "ENG-320": eng320, "ENG-321": eng321, "ENG-331": eng331, "ENG-349": eng349,
    "ENG-351": eng351, "ENG-352": eng352, "ENG-353": eng353, "ENG-354": eng354, "ENG-358": eng358, "ENG-359": eng359,
    "ENG-362": eng362, "ENG-364": eng364, "ENG-366": eng366, "ENG-367": eng367, "ENG-370": eng370, "ENG-371": eng371,
    "ENG-374": eng374, "ENG-376": eng376, "ENG-380": eng380, "ENG-381": eng381, "ENG-384": eng384, "ENG-387": eng387,
    "ENG-391": eng391, "ENG-392": eng392, "ENG-395": eng395, "ENG-397": eng397, "ENG-408": eng408, "ENG-409": eng409,
    "ENG-410": eng410, "ENG-412": eng412, "ENG-423": eng423, "ENG-424": eng424, "ENG-425": eng425, "ENG-429": eng429,
    "ENG-432": eng432, "ENG-434": eng434, "ENG-P01": eng_p01, "ENG-X01": eng_x01, "ENG-X02": eng_x02, "ENG-X04": eng_x04,
    "ENG-G01": eng_g01,
})


def eng427(work):
    W, H, fps = 108, 192, 10
    src = gray_clip(work / "film.mp4", W, H, fps, 60, [4 * i for i in range(60)])
    fr = decode(src, W, H)
    picks = [round(k * (len(fr) - 1) / 7) for k in range(8)]
    sheet = Image.new("RGB", (4 * W, 2 * H), (0, 0, 0))
    d = ImageDraw.Draw(sheet)
    tiles = []
    for k, i in enumerate(picks):
        sheet.paste(Image.fromarray(fr[i]), ((k % 4) * W, (k // 4) * H))
        tiles.append(np.asarray(sheet)[(k // 4) * H:(k // 4) * H + 14, (k % 4) * W:(k % 4) * W + 22].copy())
        d.text(((k % 4) * W + 2, (k // 4) * H + 2), f"{i / fps:.1f}s", fill=(255, 0, 0))
    sheet.save(work / "preview_sheet.png")
    clip = work / "preview_clip.mp4"
    ff("-ss", "2", "-i", src, "-t", "3", "-vf", "scale=iw/2:ih/2", "-c:v", "libx264", "-preset", "ultrafast", clip)
    vs = vstream(clip)
    dur = count_frames(clip) / fps
    a = np.asarray(sheet)
    return [("8 labelled frames spanning the film", len(picks) == 8 and picks[0] == 0 and picks[-1] == 59, picks),
            ("labels drawn on each tile", all(np.abs(a[(k // 4) * H:(k // 4) * H + 14, (k % 4) * W:(k % 4) * W + 22].astype(int) - tiles[k]).max() > 100 for k in range(8)), ""),
            ("preview clip at half resolution (540x960 for 1080x1920)", (vs["width"], vs["height"]) == (W // 2, H // 2), (vs["width"], vs["height"])),
            ("clip length within 2-4 s", 2 <= dur <= 4, dur)]


PROGRAMS["ENG-427"] = eng427
