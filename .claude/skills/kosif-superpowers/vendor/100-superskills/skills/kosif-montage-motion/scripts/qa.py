"""KOSIF Motion QA — the measurements behind the critique loop (used by motion.py; each also runs alone).

    lint(project)            determinism + HyperFrames contract + taste warnings, as a list of findings
    sheet(film, out)         contact sheet (2 fps), a strip around a moment, and a phone-width test
    speed(film)              on-screen speed in px/frame from optical flow: what needs motion blur, what is too fast
    beats(audio)             a beat grid from any track: bpm, beats, downbeats, hits (numpy only)
    study(reference)         measure a reference film: cuts, shot lengths, first change, motion energy, palette → style guide
    footage(video, out)      an all-intra clip a composition can seek frame-exactly (<video data-start ...>)
    inspect(film)            the delivery gate: yuv420p/H.264, black and frozen stretches, LUFS + true peak, exposure

Numbers follow references/craft-numbers.md (measured launch-film norms).
"""
from __future__ import annotations
import sys as _sys
for _s in (_sys.stdout, _sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")   # Windows consoles default to a legacy code page

import json
import math
import re
import shutil
import subprocess
import tempfile
import wave
from pathlib import Path

import numpy as np

FF = shutil.which("ffmpeg") or "ffmpeg"
FP = shutil.which("ffprobe") or "ffprobe"


def _probe(film: Path) -> dict:
    r = subprocess.run([FP, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate,nb_frames:format=duration",
                        "-of", "json", str(film)], capture_output=True, text=True)
    j = json.loads(r.stdout or "{}")
    s = (j.get("streams") or [{}])[0]
    num, den = (s.get("r_frame_rate") or "30/1").split("/")
    return {"w": int(s.get("width", 0)), "h": int(s.get("height", 0)), "fps": float(num) / float(den or 1),
            "duration": float((j.get("format") or {}).get("duration", 0))}


def _frames(film: Path, fps: float, width: int, gray=True):
    """Decoded frames as numpy arrays at a given rate and width (streamed, no temp files)."""
    info = _probe(film)
    h = int(round(info["h"] * width / max(1, info["w"]) / 2) * 2)
    pix = "gray" if gray else "rgb24"
    cmd = [FF, "-v", "error", "-i", str(film), "-vf", f"fps={fps},scale={width}:{h}:flags=area", "-f", "rawvideo", "-pix_fmt", pix, "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    n = width * h * (1 if gray else 3)
    while True:
        buf = p.stdout.read(n)
        if len(buf) < n:
            break
        a = np.frombuffer(buf, np.uint8).reshape(h, width) if gray else np.frombuffer(buf, np.uint8).reshape(h, width, 3)
        yield a
    p.wait()


# ───────────────────────── lint ─────────────────────────
RULES = [
    ("error", r"Math\.random\s*\(", "Math.random: use a seeded rng (MOTION.rng / three-kit rng) so every render is identical"),
    ("error", r"Date\.now\s*\(|performance\.now\s*\(|new Date\s*\(\s*\)", "wall clock in a composition: drive everything from t"),
    ("error", r"setTimeout\s*\(|setInterval\s*\(", "timers in a composition: state must be a function of t"),
    ("error", r"<html[^>]*\bdir\s*=\s*[\"']rtl", "dir=rtl on <html> renders a black silent video in HyperFrames: put direction:rtl on the text elements"),
    ("error", r"<audio(?![^>]*\bid=)[^>]*>", "<audio> without an id is dropped from the mix"),
    ("warn", r"will-change\s*:[^;]*(filter|transform)", "will-change on a layer that blurs or scales: ghost frames and blurry text"),
    ("warn", r"transition\s*:\s*(?!none)[a-z]", "CSS transition: not seekable; animate on the timeline"),
    ("warn", r"repeat\s*:\s*-1", "repeat:-1 makes the timeline infinite; give repeats a count"),
    ("warn", r"backdrop-filter", "glassmorphism (backdrop-filter): reads as a template unless the brand asks for it"),
    ("warn", r"text-shadow\s*:[^;]*(?:[2-9]\dpx|\d{3}px)|text-shadow\s*:[^;]*rgba?\((?!0\s*,\s*0\s*,\s*0)", "glow on type (large or coloured text-shadow): a fast tell of generated work"),
    ("warn", r"ease\s*:\s*[\"']linear[\"']|ease\s*:\s*[\"']none[\"']", "linear ease on a move: keep linear for drift, data and luminance ramps only"),
    ("info", r"\.from\s*\(", "gsap.from renders its from-state immediately: prefer fromTo with immediateRender:false for later entrances"),
]
# the kit's own files (what `kmotion sync` copies in) are vetted once, not linted as project code
ALLOW = {"motion-kit.js", "gsap.min.js", "main.bundle.js", "three-kit.js", "three-kit.bundle.js", "shape-kit.js", "lab-kit.js"}


def lint(project: Path) -> list[dict]:
    project = Path(project)
    files = [project / "index.html"] + sorted((project / "src").rglob("*.js")) if (project / "src").exists() else [project / "index.html"]
    files += [f for f in sorted((project / "assets").glob("*.js")) if f.name not in ALLOW] if (project / "assets").exists() else []
    out = []
    for f in files:
        if not f.exists():
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        # strip the kit's own shim block lines, comments
        scan = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
        scan = re.sub(r"(?m)//[^\n]*$", "", scan)
        for level, rx, msg in RULES:
            for m in re.finditer(rx, scan, flags=re.I):
                line = scan.count("\n", 0, m.start()) + 1
                out.append({"level": level, "file": f.name, "line": line, "rule": msg, "text": scan[m.start():m.start() + 60].replace("\n", " ")})
    idx = project / "index.html"
    if idx.exists():
        html = idx.read_text(encoding="utf-8", errors="replace")
        if "data-composition-id" not in html:
            out.append({"level": "error", "file": "index.html", "line": 0, "rule": "no root [data-composition-id]", "text": ""})
        if "window.__timelines" not in html and "window.seek" not in html:
            out.append({"level": "error", "file": "index.html", "line": 0, "rule": "no timeline registered (window.__timelines[...] = tl) and no window.seek(t)", "text": ""})
        fonts = set(re.findall(r"font-family\s*:\s*[\"']?([A-Za-z][\w \-]+)", html)) - {"inherit", "system-ui", "sans-serif", "serif", "monospace"}
        faces = set(re.findall(r"@font-face[^}]*font-family\s*:\s*[\"']?([\w \-]+)", html))
        if len(fonts) > 3:
            out.append({"level": "warn", "file": "index.html", "line": 0, "rule": f"{len(fonts)} type families: one display face + one UI face (+ mono) reads as designed", "text": ", ".join(sorted(fonts))[:80]})
    return out


# ───────────────────────── sheets ─────────────────────────
def sheet(film: Path, out: Path, at: float | None = None, cols: int = 6) -> dict:
    film, out = Path(film), Path(out)
    out.mkdir(parents=True, exist_ok=True)
    info = _probe(film)
    files = {}
    rows = max(1, math.ceil(info["duration"] * 2 / cols))
    contact = out / "contact.png"
    subprocess.run([FF, "-y", "-v", "error", "-i", str(film), "-vf", f"fps=2,scale=320:-2,tile={cols}x{rows}:padding=4:color=0x111111", "-frames:v", "1", str(contact)], check=True)
    files["contact"] = str(contact)
    phone = out / "phone.png"
    prow = max(1, math.ceil(info["duration"] / 5))
    subprocess.run([FF, "-y", "-v", "error", "-i", str(film), "-vf", f"fps=1,scale=360:-2,tile=5x{prow}:padding=4:color=0x111111", "-frames:v", "1", str(phone)], check=True)
    files["phone"] = str(phone)
    if at is not None:
        strip = out / f"strip_{at:05.2f}.png"
        subprocess.run([FF, "-y", "-v", "error", "-ss", f"{max(0, at - 0.1):.3f}", "-i", str(film), "-vf", "scale=320:-2,tile=12x1:padding=2", "-frames:v", "1", str(strip)], check=True)
        files["strip"] = str(strip)
    first = out / "first_frame.png"
    subprocess.run([FF, "-y", "-v", "error", "-i", str(film), "-frames:v", "1", str(first)], check=True)
    files["first"] = str(first)
    review = out / "review.md"
    if not review.exists():
        review.write_text(REVIEW_TEMPLATE, encoding="utf-8")
    files["review"] = str(review)
    return files


REVIEW_TEMPLATE = """# Critique round — look at contact.png, phone.png and first_frame.png before the code

Two reviewers, one fixer (Voxyz's polish loop). Each reviewer works alone, then the lists are merged:
P0 = breaks the film (wrong, unreadable, broken frame, out of sync) — fix before anything else;
P1 = reads as generated or amateur — fix this round; P2 = taste — fix if time allows. The fixer changes code only for
P0/P1 items a reviewer can point to on a frame. Re-render, re-sheet, repeat (≥ 3 rounds; stop when a round finds no P0/P1).

## Scores (1–10)
| Criterion | Reviewer A | Reviewer B | Evidence (timestamp) |
|---|---|---|---|
| Hook: frame 0 composed and moving, the idea felt by 1 s | | | |
| Readability at phone size (360 px wide) | | | |
| Motion quality: springs, velocity across cuts, no dead frames, no pops | | | |
| Variety: something new every 2–4 s, ≤ 2 uses per transition type | | | |
| Composition: one hero per frame, margins, no voids | | | |
| Truth: data, words and story agree on every paused frame | | | |
| Sound sync: hits on contact frames, cuts on the grid, −14 LUFS | | | |
| Identity: its own look, not the template's | | | |

## The twelve lenses (KOSIF visual aesthetics council) — one line each, judged on frames
world/place & depth layers · character silhouette & continuity · action: verbs, contact, momentum, cause → effect ·
camera: shot size, height, lens, focus & eye path · light: key/fill/rim, direction, ratio, Kelvin, shadows agree ·
colour: palette, value separation, one accent · VFX: sparks, dust, smoke, trails react to the world ·
atmosphere: haze, weather, time of day · materials respond to light · production design: era & culture consistent ·
composition: hierarchy, negative space, leading lines · beauty: coherence, novelty, emotional read, clutter.

Failure hunt: text overlapping during swaps · anything sliding instead of easing · corner labels and frame borders ·
a centred title on a gradient · blurry scaled text · a dead beat · a stutter at the loop seam · the device blinking out ·
inconsistent light direction · bad scale · impossible contact · blown highlights / crushed blacks (motion.py inspect).

## Findings
| ID | P | Reviewer | Timestamp | Problem | Fix |
|---|---|---|---|---|---|
| 1 | | | | | |

## What I'd still change
"""


# ───────────────────────── inspect: the delivery gate ─────────────────────────
def inspect(film: Path, lufs: float = -14.0, tol: float = 1.5, expect: list | None = None, samples: int = 12) -> dict:
    """The last gate before a film leaves (after KOSIF Omni's QA inspector): container and pixel format, black and frozen
    stretches (fades at the ends and listed holds such as a tape-stop are allowed), integrated loudness and true peak, and
    exposure measured on sampled frames (blown highlights, crushed blacks)."""
    film = Path(film)
    if not film.is_file():
        raise SystemExit(f"{film}: no such file")
    expect = expect or []
    r = subprocess.run([FP, "-v", "error", "-show_entries", "stream=codec_type,codec_name,pix_fmt,width,height,r_frame_rate:format=duration",
                        "-of", "json", str(film)], capture_output=True, text=True)
    j = json.loads(r.stdout or "{}")
    v = next((x for x in j.get("streams", []) if x.get("codec_type") == "video"), {})
    au = next((x for x in j.get("streams", []) if x.get("codec_type") == "audio"), None)
    dur = float((j.get("format") or {}).get("duration", 0))
    issues, warns = [], []
    if v.get("pix_fmt") != "yuv420p":
        issues.append(f"pixel format {v.get('pix_fmt')}: phones and social players want yuv420p")
    if v.get("codec_name") != "h264":
        warns.append(f"codec {v.get('codec_name')}: H.264 plays everywhere")
    if int(v.get("width", 0)) % 2 or int(v.get("height", 0)) % 2:
        issues.append("odd frame size")

    def _log(args: list) -> str:
        return subprocess.run([FF, "-v", "info", "-i", str(film), *args, "-f", "null", "-"], capture_output=True, text=True,
                              encoding="utf-8", errors="replace").stderr

    def allowed(s0, e0):
        return any(s0 >= a0 - 0.2 and e0 <= a1 + 0.2 for a0, a1 in expect)

    e = _log(["-vf", "blackdetect=d=0.4:pic_th=0.999:pix_th=0.03", "-an"])        # truly empty frames, not a dark design
    black = [(float(x), float(y)) for x, y in re.findall(r"black_start:([\d.]+)\s+black_end:([\d.]+)", e)]
    for s0, e0 in black:
        if e0 <= 0.8 or s0 >= dur - 1.2 or allowed(s0, e0):      # a fade from or to black at the ends is fine
            continue
        issues.append(f"black frames {s0:.2f}–{e0:.2f} s")
    e = _log(["-vf", "freezedetect=n=-60dB:d=1.5", "-an"])
    st = [float(x) for x in re.findall(r"freeze_start:\s*([\d.]+)", e)]
    en = [float(x) for x in re.findall(r"freeze_end:\s*([\d.]+)", e)]
    frozen = [(x, en[i] if i < len(en) else dur) for i, x in enumerate(st)]
    for s0, e0 in frozen:
        if allowed(s0, e0):
            continue
        if e0 >= dur - 0.6:
            warns.append(f"frozen picture {s0:.2f}–{e0:.2f} s (an end hold)")
        else:
            issues.append(f"frozen picture {s0:.2f}–{e0:.2f} s")
    loud = {}
    if au:
        e = _log(["-vn", "-af", "ebur128=peak=true"])
        tail = e[e.rfind("Summary:"):]
        m_i = re.search(r"I:\s*(-?[\d.]+) LUFS", tail)
        m_tp = re.search(r"Peak:\s*(-?[\d.]+) dBFS", tail)
        m_lra = re.search(r"LRA:\s*(-?[\d.]+) LU", tail)
        loud = {"lufs": float(m_i.group(1)) if m_i else None, "true_peak": float(m_tp.group(1)) if m_tp else None,
                "lra": float(m_lra.group(1)) if m_lra else None}
        if loud["lufs"] is not None and abs(loud["lufs"] - lufs) > tol:
            issues.append(f"loudness {loud['lufs']} LUFS (target {lufs} ± {tol})")
        if loud["true_peak"] is not None and loud["true_peak"] > -0.9:
            issues.append(f"true peak {loud['true_peak']} dBTP (limit −1)")
    else:
        warns.append("no audio stream")
    info = _probe(film)
    step = max(1e-3, dur / (samples + 1))
    clip_hi, crush, means = [], [], []
    for f in _frames(film, 1 / step, 320, gray=False):
        g = f.astype(np.float32)
        clip_hi.append(float(np.mean(np.all(g >= 252, axis=2))))
        crush.append(float(np.mean(np.all(g <= 3, axis=2))))
        means.append(float(g.mean()))
    if clip_hi and float(np.median(clip_hi)) > 0.02:
        warns.append(f"blown highlights on the typical frame: {np.median(clip_hi) * 100:.1f} % of pixels at white")
    if crush and float(np.median(crush)) > 0.25:
        warns.append(f"crushed blacks on the typical frame: {np.median(crush) * 100:.1f} % of pixels at black")
    return {"file": str(film), "ok": not issues, "issues": issues, "warnings": warns, "seconds": round(dur, 3),
            "size": f"{v.get('width')}x{v.get('height')}", "fps": round(info["fps"], 3), "codec": v.get("codec_name"),
            "pix_fmt": v.get("pix_fmt"), "black": [[round(x, 2), round(y, 2)] for x, y in black],
            "frozen": [[round(x, 2), round(y, 2)] for x, y in frozen], **loud,
            "exposure": {"white_pct_median": round(float(np.median(clip_hi)) * 100, 2) if clip_hi else None,
                         "black_pct_median": round(float(np.median(crush)) * 100, 2) if crush else None,
                         "mean_level": round(float(np.mean(means)), 1) if means else None}}


# ───────────────────────── speed ─────────────────────────
def speed(film: Path, fps: float | None = None, width: int = 480) -> dict:
    """Optical-flow speed per frame in px/frame at the film's native size. Counts only pixels whose forward and
    backward flow agree (flat interiors and repeats do not inflate it); the frame speed is the 99.5th percentile."""
    import cv2
    film = Path(film)
    info = _probe(film)
    fps = fps or info["fps"]
    k = info["w"] / width
    prev, sp = None, []
    for g in _frames(film, fps, width):
        if prev is not None:
            fw = cv2.calcOpticalFlowFarneback(prev, g, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            bw = cv2.calcOpticalFlowFarneback(g, prev, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            h, w = g.shape
            yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
            mx = np.clip(xx + fw[..., 0], 0, w - 1).astype(np.int32); my = np.clip(yy + fw[..., 1], 0, h - 1).astype(np.int32)
            err = np.hypot(fw[..., 0] + bw[my, mx, 0], fw[..., 1] + bw[my, mx, 1])
            mag = np.hypot(fw[..., 0], fw[..., 1])
            ok = (err < 0.5 + 0.1 * mag) & (mag > 0.25)
            sp.append(float(np.percentile(mag[ok], 99.5)) * k if ok.sum() > 30 else 0.0)
        prev = g
    s = np.array(sp) * (info["fps"] / fps if fps != info["fps"] else 1)
    need = [i for i, v in enumerate(s) if v > 12]
    fast = [i for i, v in enumerate(s) if v > 80]
    peak = float(s.max()) if len(s) else 0.0
    samples = 1 if peak < 2 else int(min(48, max(4, math.ceil((240 / 360) * peak / 3))))
    rep = {"fps": round(fps, 2), "frames": int(len(s)), "peak_px_f": round(peak, 1), "median_px_f": round(float(np.median(s)) if len(s) else 0, 2),
           "share_needs_blur": round(len(need) / max(1, len(s)), 3), "too_fast_frames": fast[:40], "too_fast_count": len(fast),
           "suggested_blur_samples": samples,
           "verdict": "clean" if peak <= 12 else ("blur it (motion.py render --blur %d)" % min(8, samples) if peak <= 80 else "redesign the moves over 80 px/f: a cut on the beat, a match cut, a mask wipe or a shorter distance")}
    return rep


# ───────────────────────── beats ─────────────────────────
def _read_wav_mono(path: Path) -> tuple[np.ndarray, int]:
    path = Path(path)
    if path.suffix.lower() != ".wav":
        tmp = Path(tempfile.mkdtemp(prefix="kosif_beats_")) / "a.wav"
        subprocess.run([FF, "-y", "-v", "error", "-i", str(path), "-ac", "1", "-ar", "22050", str(tmp)], check=True)
        path = tmp
    with wave.open(str(path)) as w:
        sr, n, ch, sw = w.getframerate(), w.getnframes(), w.getnchannels(), w.getsampwidth()
        raw = w.readframes(n)
    dt = {1: np.int8, 2: np.int16, 4: np.int32}[sw]
    x = np.frombuffer(raw, dt).astype(np.float32) / float(np.iinfo(dt).max)
    if ch > 1:
        x = x.reshape(-1, ch).mean(1)
    return x, sr


def beats(audio: Path, bpm_range=(70, 180)) -> dict:
    """Spectral-flux onsets → tempo by autocorrelation (with a mild prior near 120) → beat phase by the comb that
    collects the most onset energy → beats every period, refined to the nearest onset peak; hits = strong onsets."""
    x, sr = _read_wav_mono(Path(audio))
    hop, nfft = 512, 2048
    win = np.hanning(nfft).astype(np.float32)
    nfr = max(1, 1 + (len(x) - nfft) // hop)
    mags = np.empty((nfr, nfft // 2 + 1), np.float32)
    for i in range(nfr):
        seg = x[i * hop:i * hop + nfft]
        if len(seg) < nfft:
            seg = np.pad(seg, (0, nfft - len(seg)))
        mags[i] = np.abs(np.fft.rfft(seg * win))
    logm = np.log1p(mags * 10)
    flux = np.maximum(0, np.diff(logm, axis=0)).sum(1)
    flux = np.concatenate([[0], flux])
    flux -= np.convolve(flux, np.ones(16) / 16, mode="same")
    flux = np.maximum(flux, 0)
    flux /= flux.max() + 1e-9
    fr = sr / hop
    ac = np.correlate(flux, flux, mode="full")[len(flux) - 1:]
    lags = np.arange(len(ac))
    lo, hi = int(fr * 60 / bpm_range[1]), int(fr * 60 / bpm_range[0])
    cand = lags[lo:hi + 1]
    bpms = 60 * fr / np.maximum(cand, 1)
    score = ac[lo:hi + 1] * np.exp(-0.5 * (np.log2(bpms / 120) / 0.9) ** 2)
    period = cand[int(np.argmax(score))]
    # sub-frame tempo refinement around the best lag
    best = max(np.linspace(period - 1, period + 1, 21), key=lambda p: sum(flux[int(round(k * p))] for k in range(int(len(flux) / p)) if int(round(k * p)) < len(flux)))
    phase = max(range(int(best)), key=lambda ph: sum(flux[int(round(ph + k * best))] for k in range(int((len(flux) - ph) / best))))
    times = []
    k = 0
    while True:
        c = phase + k * best
        if c >= len(flux):
            break
        j0, j1 = max(0, int(c - 2)), min(len(flux), int(c + 3))
        j = j0 + int(np.argmax(flux[j0:j1])) if flux[j0:j1].max() > 0.15 else int(round(c))
        times.append(round(j / fr, 3))
        k += 1
    peaks = [i for i in range(1, len(flux) - 1) if flux[i] > 0.35 and flux[i] >= flux[i - 1] and flux[i] >= flux[i + 1]]
    hits, last = [], -1e9
    for i in peaks:
        if i - last > fr * 0.09:
            hits.append(round(i / fr, 3)); last = i
    bpm = round(60 * fr / best, 2)
    # downbeats: the beat phase (mod 4) with the most onset energy
    strength = [sum(flux[int(t * fr)] for t in times[o::4] if int(t * fr) < len(flux)) for o in range(4)]
    off = int(np.argmax(strength)) if times else 0
    return {"bpm": bpm, "beat": round(60 / bpm, 4), "beats": times, "downbeats": times[off::4], "hits": hits, "duration": round(len(x) / sr, 3)}


# ───────────────────────── study a reference ─────────────────────────
def study(ref: Path, out: Path) -> dict:
    """Measure a reference film so its grammar can be borrowed (never its content): cuts and shot lengths, the first
    visible change, motion energy and stillness, palette, and a 2 fps contact sheet; writes style_guide.md."""
    ref, out = Path(ref), Path(out)
    out.mkdir(parents=True, exist_ok=True)
    info = _probe(ref)
    fps = min(30.0, info["fps"] or 30.0)
    diffs, prev, frames_rgb = [], None, []
    for i, g in enumerate(_frames(ref, fps, 320)):
        if prev is not None:
            diffs.append(float(np.abs(g.astype(np.int16) - prev.astype(np.int16)).mean()))
        prev = g
    d = np.array(diffs) if diffs else np.zeros(1)
    med = float(np.median(d)) if len(d) else 0
    cut_thr = max(18.0, med * 8)
    cuts = [round((i + 1) / fps, 3) for i, v in enumerate(d) if v > cut_thr]
    bounds = [0.0] + cuts + [info["duration"]]
    shots = [round(b - a, 3) for a, b in zip(bounds, bounds[1:]) if b - a > 0.05]
    first = next((round((i + 1) / fps, 3) for i, v in enumerate(d) if v > 0.5), None)
    still = d < 0.5
    longest = run = 0
    for s in still:
        run = run + 1 if s else 0
        longest = max(longest, run)
    for k, rgb in enumerate(_frames(ref, 1, 160, gray=False)):
        frames_rgb.append(rgb.reshape(-1, 3))
    palette = []
    if frames_rgb:
        import cv2
        px = np.concatenate(frames_rgb).astype(np.float32)
        if len(px) > 60000:
            px = px[np.random.default_rng(7).choice(len(px), 60000, replace=False)]
        _, lab, cen = cv2.kmeans(px, 6, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.5), 3, cv2.KMEANS_PP_CENTERS)
        counts = np.bincount(lab.ravel(), minlength=6) / len(lab)
        palette = [{"hex": "#%02x%02x%02x" % tuple(int(v) for v in c), "share": round(float(s), 3)} for c, s in sorted(zip(cen, counts), key=lambda z: -z[1])]
    files = sheet(ref, out)
    rep = {"duration": round(info["duration"], 2), "size": f"{info['w']}x{info['h']}", "fps": round(info["fps"], 2), "cuts": len(cuts),
           "cuts_per_10s": round(len(cuts) / max(info["duration"], 1e-3) * 10, 2), "median_shot_s": round(float(np.median(shots)), 2) if shots else None,
           "shortest_shot_s": min(shots) if shots else None, "longest_shot_s": max(shots) if shots else None, "first_change_s": first,
           "motion_median": round(med, 2), "motion_p90": round(float(np.percentile(d, 90)), 2) if len(d) else 0, "near_still_share": round(float(still.mean()), 3),
           "longest_still_s": round(longest / fps, 2), "palette": palette, "cut_times": cuts[:80], "sheet": files}
    (out / "study.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False), encoding="utf-8")
    pal = "\n".join(f"- {p['hex']} ({p['share']*100:.0f}%)" for p in palette)
    (out / "style_guide.md").write_text(f"""# Style guide drawn from {ref.name}
Take the grammar, never the content, logos or characters.

## Measured
- {rep['duration']} s at {rep['size']}, {rep['fps']} fps
- cuts: {rep['cuts']} ({rep['cuts_per_10s']} per 10 s); median shot {rep['median_shot_s']} s (shortest {rep['shortest_shot_s']}, longest {rep['longest_shot_s']})
- first visible change at {rep['first_change_s']} s; near-still frames {rep['near_still_share']*100:.0f}%, longest still {rep['longest_still_s']} s
- motion energy: median {rep['motion_median']}, p90 {rep['motion_p90']} (craft norms: median 1.4, p90 6.0)

## Palette (by area)
{pal}

## Fill in by looking at contact.png
- type: family, weight, case, tracking; how text enters and leaves
- transitions: which kinds, how long, what carries across each cut
- camera: moves per shot, push/pull ranges, holds
- texture: grain, blur, depth, light
- the one device that travels through the film
""", encoding="utf-8")
    return rep


# ───────────────────────── footage ─────────────────────────
def footage(video: Path, out: Path, start: float = 0.0, dur: float | None = None, width: int = 1280, fps: int = 30) -> dict:
    """Re-encode a clip as all-intra H.264 (every frame a keyframe) so the composition can seek it exactly; muted."""
    video, out = Path(video), Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [FF, "-y", "-v", "error", "-ss", f"{start:.3f}", "-i", str(video)]
    if dur:
        cmd += ["-t", f"{dur:.3f}"]
    cmd += ["-vf", f"fps={fps},scale={width}:-2:flags=lanczos", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-g", "1", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True)
    info = _probe(out)
    return {"file": str(out), "seconds": round(info["duration"], 3), "size": f"{info['w']}x{info['h']}", "fps": info["fps"],
            "tag": f'<video id="clip" src="{out.name}" muted playsinline data-start="0" data-duration="{round(info["duration"], 3)}"></video>'}


# ───────────────────────── listen with math: per-frame channels from a track ─────────────────────────
def _magma(v: np.ndarray) -> np.ndarray:
    """A compact magma-like colormap (black → violet → magenta → coral → orange → pale gold), v in [0, 1]."""
    stops = np.array([[0.0, 0, 0, 4], [0.2, 40, 11, 84], [0.4, 120, 28, 109], [0.6, 192, 58, 118], [0.75, 236, 105, 89], [0.88, 251, 165, 74], [1.0, 252, 253, 191]], np.float32)
    out = np.empty(v.shape + (3,), np.float32)
    for c in range(3):
        out[..., c] = np.interp(v, stops[:, 0], stops[:, c + 1])
    return out.astype(np.uint8)


def channels(audio: Path, fps: int = 30, out: Path | None = None, bpm: float | None = None) -> dict:
    """The soundtrack as animation channels, one value per output frame (all 0..1 unless noted), so every visual can be
    driven by the sound itself: rms, bass / mid / high band energy, onset strength, kick (low-band onset peaks), onsets,
    silence (gated dead air), centroid (brightness), pitch_dive / pitch_rise (tape-stop / tape-start: the dominant pitch
    falling or rising fast), speed (an estimate of playback speed from the pitch slope, 1 = normal, 0 = stopped) and tape
    (the integral of speed: a clock in seconds that slows, freezes and overdrives with the track). Also the beat grid, a
    magma spectrogram (spectrogram.png) and a height map of it (spectrum_height.png) for a ground made of the sound."""
    from PIL import Image
    x, sr = _read_wav_mono(Path(audio))
    hop = int(round(sr / fps))
    nfft = 4096
    win = np.hanning(nfft).astype(np.float32)
    n = int(math.ceil(len(x) / hop))
    xp = np.pad(x, (nfft // 2, nfft))
    freqs = np.fft.rfftfreq(nfft, 1 / sr)
    mag = np.empty((n, len(freqs)), np.float32)
    rms = np.empty(n, np.float32)
    for i in range(n):
        seg = xp[i * hop:i * hop + nfft]
        mag[i] = np.abs(np.fft.rfft(seg * win))
        core = x[i * hop:i * hop + hop]
        rms[i] = float(np.sqrt(np.mean(core ** 2))) if len(core) else 0.0
    band = lambda lo, hi: mag[:, (freqs >= lo) & (freqs < hi)].sum(1)
    bass, mid, high = band(20, 160), band(160, 2000), band(2000, 12000)
    norm = lambda a: (a / (np.percentile(a, 99) + 1e-9)).clip(0, 1)
    logm = np.log1p(mag * 10)
    flux = np.concatenate([[0], np.maximum(0, np.diff(logm, axis=0)).sum(1)])
    lowflux = np.concatenate([[0], np.maximum(0, np.diff(np.log1p(mag[:, freqs < 160] * 10), axis=0)).sum(1)])
    onset = norm(flux)
    kick_strength = norm(lowflux)
    kicks, last = [], -99
    for i in range(1, n - 1):
        if kick_strength[i] > 0.42 and kick_strength[i] >= kick_strength[i - 1] and kick_strength[i] >= kick_strength[i + 1] and i - last >= int(0.18 * fps):
            kicks.append(i); last = i
    onsets, last = [], -99
    for i in range(1, n - 1):
        if onset[i] > 0.35 and onset[i] >= onset[i - 1] and onset[i] >= onset[i + 1] and i - last >= max(1, int(0.06 * fps)):
            onsets.append(i); last = i
    centroid = (mag * freqs).sum(1) / (mag.sum(1) + 1e-9)
    rms_n = norm(rms)
    silence = (rms_n < 0.04).astype(np.float32)
    # dominant pitch (60–1200 Hz peak) and its slope in semitones per second → tape-stop / tape-start detection
    band_idx = np.flatnonzero((freqs >= 60) & (freqs <= 1200))
    peak_f = freqs[band_idx[np.argmax(mag[:, band_idx], axis=1)]]
    semis = 12 * np.log2(np.maximum(peak_f, 1) / 440.0)
    # a tape-stop is a smooth continuous glide, a melody is a staircase: fit a line over 0.3 s and require a good fit
    w = max(3, int(round(0.3 * fps)))
    tt = np.arange(w) / fps
    A = np.vstack([tt, np.ones(w)]).T
    def glide(curve):
        sl = np.zeros(n, np.float32); fit = np.zeros(n, np.float32)
        for i in range(n - w):
            y = curve[i:i + w]
            coef, res, *_ = np.linalg.lstsq(A, y, rcond=None)
            ss = float(((y - y.mean()) ** 2).sum()) + 1e-9
            c = i + w // 2
            sl[c], fit[c] = coef[0], 1 - (float(res[0]) if len(res) else 0.0) / ss
        return sl, fit
    slope, r2 = glide(semis)
    # a tape-stop slides the WHOLE log-frequency spectrum down (a note's decay only dims it): find the shift, in log bins,
    # that best aligns each frame with the next, and accumulate it over 0.25 s
    lb = np.geomspace(40, min(12000, sr / 2 - 1), 192)
    li = np.clip(np.searchsorted(freqs, lb), 0, len(freqs) - 1)
    L = logm[:, li]
    L = (L - L.mean(1, keepdims=True)) / (L.std(1, keepdims=True) + 1e-6)
    shift = np.zeros(n, np.float32)
    for i in range(n - 1):
        a, b = L[i], L[i + 1]
        best, bs = 0, -1e9
        for d in range(-6, 7):
            cc = float(np.dot(a[max(0, d):len(a) + min(0, d)], b[max(0, -d):len(b) + min(0, -d)])) / (len(a) - abs(d))
            if cc > bs:
                bs, best = cc, d
        shift[i] = -best if bs > 0.3 else 0.0                 # negative = the spectrum moved down
    win = max(2, int(round(0.25 * fps)))
    acc = np.convolve(shift, np.ones(win), mode="same")
    oct_per_bin = np.log2(lb[-1] / lb[0]) / (len(lb) - 1)
    rate = acc * oct_per_bin * 12 / (win / fps)                 # semitones per second over the window
    voiced = rms_n > 0.04
    def held(mask, k=4):                                       # keep only runs of at least k frames (a glide, not a step)
        out = np.zeros_like(mask); run = 0
        for i, m in enumerate(mask):
            run = run + 1 if m else 0
            if run >= k:
                out[i - run + 1:i + 1] = 1
        return out
    dive = held(((rate < -30) & voiced) | ((slope < -15) & (r2 > 0.9) & voiced)).astype(np.float32)
    rise = held(((rate > 30) & voiced) | ((slope > 15) & (r2 > 0.9) & voiced)).astype(np.float32)
    # playback speed, a small state machine: a dive starts a stop that runs down to 0 and stays there through the dead air;
    # a rise (or the sound coming back) spins it up again
    speed = np.ones(n, np.float32)
    s_, state = 1.0, "play"
    for i in range(n):
        if state == "play":
            s_ = s_ + (1.0 - s_) * min(1.0, 6.0 / fps)
            if dive[i]:
                state = "stopping"
        if state == "stopping":
            s_ = max(0.0, s_ - 1.6 / fps)
            if silence[i] or s_ == 0.0:
                state, s_ = "stopped", 0.0
        elif state == "stopped":
            s_ = 0.0
            if rise[i] or (not silence[i] and rms_n[i] > 0.15 and i > 0 and silence[i - 1] == 0):
                state = "starting"
        if state == "starting":
            s_ = min(1.0, s_ + 2.2 / fps)
            if s_ >= 1.0:
                state = "play"
        speed[i] = s_
    tape = np.cumsum(speed) / fps
    bt = beats(Path(audio))
    if bpm:
        bt["bpm"] = bpm
    ch = {"fps": fps, "frames": n, "seconds": round(n / fps, 3), "bpm": bt["bpm"], "beats": bt["beats"], "downbeats": bt["downbeats"],
          "kicks": [round(i / fps, 3) for i in kicks], "onsets": [round(i / fps, 3) for i in onsets],
          "rms": rms_n.round(3).tolist(), "bass": norm(bass).round(3).tolist(), "mid": norm(mid).round(3).tolist(), "high": norm(high).round(3).tolist(),
          "onset": onset.round(3).tolist(), "centroid": (centroid / 8000).clip(0, 1).round(3).tolist(), "silence": silence.tolist(),
          "pitch_dive": dive.tolist(), "pitch_rise": rise.tolist(), "speed": speed.round(3).tolist(), "tape": tape.round(4).tolist()}
    out = Path(out) if out else Path(audio).with_suffix(".channels.json")
    out.write_text(json.dumps(ch), encoding="utf-8")
    # the spectrogram as an image: time across, log-frequency up, magma colours; and a height map of it
    fbins = np.geomspace(30, min(16000, sr / 2 - 1), 256)
    idx = np.clip(np.searchsorted(freqs, fbins), 0, len(freqs) - 1)
    spec = logm[:, idx].T[::-1]
    spec = (spec - np.percentile(spec, 5)) / (np.percentile(spec, 99.5) - np.percentile(spec, 5) + 1e-9)
    spec = spec.clip(0, 1)
    Image.fromarray(_magma(spec)).save(out.with_name("spectrogram.png"))
    Image.fromarray((spec * 255).astype(np.uint8)).save(out.with_name("spectrum_height.png"))
    return {"file": str(out), "frames": n, "bpm": ch["bpm"], "kicks": len(kicks), "onsets": len(onsets), "silent_frames": int(silence.sum()),
            "pitch_dive_frames": int(dive.sum()), "pitch_rise_frames": int(rise.sum()), "tape_end_s": round(float(tape[-1]), 2),
            "spectrogram": str(out.with_name("spectrogram.png"))}


def loopcheck(film: Path, k: int = 8) -> dict:
    """A seamless loop: the step from the last frame back to the first must look like an ordinary step. Pass when the seam
    difference ≤ max(0.4, 1.5 × the median of the k steps at each end) (320 px luma, 0–255)."""
    info = _probe(Path(film))
    frames = list(_frames(Path(film), info["fps"] or 30, 320))
    if len(frames) < 4:
        return {"ok": False, "reason": "too short"}
    d = lambda a, b: float(np.abs(a.astype(np.int16) - b.astype(np.int16)).mean())
    steps = [d(frames[i], frames[i + 1]) for i in range(len(frames) - 1)]
    ends = steps[:k] + steps[-k:]
    seam = d(frames[-1], frames[0])
    limit = max(0.4, 1.5 * float(np.median(ends)))
    return {"seam": round(seam, 3), "median_end_step": round(float(np.median(ends)), 3), "limit": round(limit, 3), "ok": seam <= limit}


# ───────────────────────── measure real motion: a performer's silhouette as particles ─────────────────────────
def mocap(video: Path, out: Path, fps: int = 30, points: int = 1200, width: int = 480, start: float = 0.0, dur: float | None = None,
          threshold: int = 28, seed: int = 7) -> dict:
    """A fixed-camera video of a performer → per-frame particle positions inside their silhouette (JSON for three-kit's
    makeParticleBody). The background is the per-pixel median of frames across the clip (the performer moves, the room does
    not), the silhouette is the cleaned difference, and the points come from one seeded candidate list in a fixed order, so
    the same particle tends to stay on the same part of the body from frame to frame. Coordinates are 0..1000 (x right,
    y down); -1 marks an unused slot. Nothing is generated: the timing, the stops and the snap are the performer's own."""
    import cv2
    cap = cv2.VideoCapture(str(video))
    src_fps = cap.get(cv2.CAP_PROP_FPS) or 30
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    i0 = int(start * src_fps)
    i1 = int((start + dur) * src_fps) if dur else total
    step = max(1.0, src_fps / fps)
    want = [int(round(i0 + k * step)) for k in range(int((i1 - i0) / step))]
    frames, idx, k = [], 0, 0
    while k < len(want):
        ok, img = cap.read()
        if not ok:
            break
        if idx == want[k]:
            h = int(round(img.shape[0] * width / img.shape[1] / 2) * 2)
            frames.append(cv2.cvtColor(cv2.resize(img, (width, h), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY))
            k += 1
        idx += 1
    cap.release()
    if len(frames) < 3:
        raise RuntimeError("the clip is too short to measure")
    stack = np.stack(frames[:: max(1, len(frames) // 60)])
    bg = np.median(stack, axis=0).astype(np.uint8)
    h, w = frames[0].shape
    rng = np.random.default_rng(seed)
    cand = rng.random((points * 30, 2))
    cx = np.clip((cand[:, 0] * w).astype(int), 0, w - 1); cy = np.clip((cand[:, 1] * h).astype(int), 0, h - 1)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    outf, cover = [], []
    for g in frames:
        diff = cv2.absdiff(cv2.GaussianBlur(g, (5, 5), 0), cv2.GaussianBlur(bg, (5, 5), 0))
        _, m = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
        m = cv2.morphologyEx(cv2.morphologyEx(m, cv2.MORPH_OPEN, kernel), cv2.MORPH_CLOSE, kernel, iterations=2)
        n, lab, stats, _ = cv2.connectedComponentsWithStats(m)
        if n > 1:                                              # keep the larger bodies, drop specks
            keep = [j for j in range(1, n) if stats[j, cv2.CC_STAT_AREA] >= 0.01 * stats[1:, cv2.CC_STAT_AREA].max()]
            m = np.isin(lab, keep).astype(np.uint8) * 255
        inside = np.flatnonzero(m[cy, cx] > 0)[:points]
        row = np.full(points * 2, -1, np.int16)
        row[0:len(inside) * 2:2] = (cand[inside, 0] * 1000).astype(np.int16)
        row[1:len(inside) * 2:2] = (cand[inside, 1] * 1000).astype(np.int16)
        outf.append(row.tolist())
        cover.append(len(inside) / points)
    data = {"fps": fps, "points": points, "aspect": round(w / h, 4), "scale": 1000, "frames": outf}
    out = Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, separators=(",", ":")), encoding="utf-8")
    return {"file": str(out), "frames": len(outf), "points": points, "fps": fps, "mean_fill": round(float(np.mean(cover)), 3),
            "size_kb": out.stat().st_size // 1024}
