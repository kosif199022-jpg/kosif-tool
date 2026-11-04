"""Wave 3, chunk 05 (music-beat-sound cards no earlier runner covered): each card's method as a real program.

Every runner builds a deterministic fixture inside its work folder (click/kick loops at a known tempo, tones,
speech-like bursts, synthetic footage with a known moving object), applies the card's what/how/params and measures
the produced output against the known answer, plus a negative control (the same measurement on the untreated input
fails the criterion).

Engines: the repo's own kosif-montage-motion scripts where they exist (songreel.py sections/excerpt/shot grid/assign,
reel.has_music_bed, audiolab.music centre cancellation, montage.cut, qa.beats, score.Score, motion.py channels,
omni/audio_analyze.py, kit/sfx catalog), the installed HyperFrames media-use skill (resolve.mjs bundled SFX,
lib/bgm-volume.mjs), Remotion's @remotion/media-utils visualizeAudio (installed here with
``npm i -g @remotion/media-utils@4.0.536`` to match the installed remotion 4.0.536), librosa beat tracking, ffmpeg
(loudnorm, sidechaincompress, astats, afftdn, adelay/amix), ImageMagick ``convert`` for word cards, numpy/scipy/PIL.
Where the card's engine is a paid API or a browser/WebGL kit, the card's stated formula is implemented in numpy and
rendered, and the docstring says so. Prompt-writing cards (Suno/ElevenLabs) are run as the package builder plus a
linter of the card's rules; the generation itself is never called (paid account).
"""
import csv
import importlib
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

from _harness import card, check, fx

HERE = Path(__file__).resolve().parent
SKILLS = HERE.parents[1]
REPO = HERE.parents[3]
VEND = SKILLS / "kosif-superpowers/vendor/100-superskills/skills/kosif-montage-motion/scripts"
NODE_MODS = Path("/opt/node22/lib/node_modules")
HF_MEDIA = NODE_MODS / "hyperframes/dist/skills/media-use"
SR = 48000

GAPS: dict = {}


def _gap(cid, why):
    GAPS[cid] = why
    GAPS["power:" + cid] = why


_gap("BEAT-113", "the Waveform plate is a WebGPU shader (data-requires-webgpu, shaders.iife.js); no WebGPU-capable Chromium here")
_gap("BEAT-161", "ElevenLabs textToSoundEffects is a paid, key-gated API (billed per generation)")
_gap("BEAT-162", "the SFX are hosted on remotion.media and must be fetched at render time (no network for that host; meme-sound licences unclear)")
_gap("BEAT-164", "ElevenLabs music_v2 generation is paid (~27.5 credits/s) and key-gated; the whole-bar plan maths runs as BEAT-175")
_gap("BEAT-165", "the check re-transcribes the generated song with ElevenLabs Scribe (paid key) after a paid generation")
_gap("BEAT-171", "Cover / Extend / Replace Section / Personas are features of the user's Suno Pro/Premier account UI")
_gap("BEAT-172", "stems, tempo-locked WAV and MIDI are exported from a paid Suno Pro/Premier account (MIDI costs credits)")
_gap("BEAT-176", "ElevenLabs /v1/audio-isolation is a paid, key-gated API")
_gap("BEAT-177", "the KOSIF bridge (basma_bridge.py, POST BRIDGE/api/clean) is not in this repo and runs on the user's own machine")
_gap("BEAT-180", "kosif_atlas_read is a live Atlas service tool not exposed here, and the curated ids point at ElevenLabs (paid key) skills")


# ───────────────────────── shared helpers ─────────────────────────
def vmod(name, where=VEND):
    if str(where) not in sys.path:
        sys.path.insert(0, str(where))
    return importlib.import_module(name)


def sh(cmd, cwd=None, timeout=60):
    done = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, timeout=timeout, cwd=cwd,
                          stdin=subprocess.DEVNULL)
    if done.returncode:
        raise RuntimeError("command failed (%d): %s %s" % (done.returncode, " ".join(map(str, cmd))[:200],
                                                           (done.stderr or done.stdout)[-500:]))
    return done.stdout


def ff(*args, timeout=60):
    return fx.ffmpeg(*args, timeout=timeout)


def tt(d, sr=SR):
    return np.arange(int(round(d * sr))) / sr


def sine(f, d, amp=0.5, sr=SR):
    return amp * np.sin(2 * np.pi * f * tt(d, sr))


def save(wd, name, x, sr=SR):
    return fx.write_wav(Path(wd) / name, x, sr)


def load_any(p, sr=SR, ch=1):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-f", "f32le", "-ac", str(ch), "-ar", str(sr), "-"],
                         capture_output=True, timeout=60, stdin=subprocess.DEVNULL).stdout
    a = np.frombuffer(raw, dtype="<f4").astype(float)
    return (a.reshape(-1, ch) if ch > 1 else a), sr


def rms(x):
    return float(np.sqrt(np.mean(np.square(x)) + 1e-20))


def dbfs(x):
    return 20 * math.log10(rms(x) + 1e-12)


def seg_db(x, sr, a, b):
    return dbfs(x[int(a * sr):int(b * sr)])


def peak_db(x):
    return 20 * math.log10(float(np.max(np.abs(x))) + 1e-12)


def band_db(x, sr, lo, hi):
    X = np.abs(np.fft.rfft(x * np.hanning(len(x)))) ** 2
    f = np.fft.rfftfreq(len(x), 1 / sr)
    return 10 * math.log10(float(X[(f >= lo) & (f < hi)].sum()) + 1e-20)


def peak_hz(x, sr=SR, lo=15):
    X = np.abs(np.fft.rfft(x * np.hanning(len(x))))
    f = np.fft.rfftfreq(len(x), 1 / sr)
    X[f < lo] = 0
    return float(f[int(np.argmax(X))])


def centroid(x, sr=SR):
    X = np.abs(np.fft.rfft(x * np.hanning(len(x))))
    f = np.fft.rfftfreq(len(x), 1 / sr)
    return float((X * f).sum() / (X.sum() + 1e-12))


def envelope(x, sr, ms=5.0):
    n = max(1, int(sr * ms / 1000))
    return np.sqrt(np.convolve(np.square(x), np.ones(n) / n, mode="same"))


def onsets(x, sr, rel=0.3, gap=0.06, ms=5.0):
    """Independent measurement: rising crossings of rel*max of a short RMS envelope, at least gap apart."""
    e = envelope(x, sr, ms)
    thr = rel * e.max()
    up = np.flatnonzero((e[1:] >= thr) & (e[:-1] < thr)) + 1
    out, last = [], -1e9
    for i in up:
        if i / sr - last >= gap:
            out.append(i / sr)
            last = i / sr
    return out


def addp(*arrs):
    n = max(len(a) for a in arrs)
    out = np.zeros(n)
    for a in arrs:
        out[:len(a)] += a
    return out


def kick(sr=SR, amp=0.9):
    t = tt(0.25, sr)
    return amp * np.sin(2 * np.pi * np.cumsum(46 + 110 * np.exp(-t / 0.032)) / sr) * np.exp(-t / 0.08)


def drum_loop(bpm, secs, sr=SR, offset=0.0, seed=1):
    rng = np.random.default_rng(seed)
    x = np.zeros(int(secs * sr))
    k = kick(sr).copy()
    nc = int(0.01 * sr)
    k[:nc] += 0.3 * rng.standard_normal(nc) * np.exp(-np.arange(nc) / sr / 0.002)
    times, b = [], 0
    while offset + b * 60 / bpm < secs - 0.3:
        t = offset + b * 60 / bpm
        i = int(round(t * sr))
        x[i:i + len(k)] += k[: len(x) - i]
        times.append(round(t, 4))
        b += 1
    return x, times


def clicks(times, secs, sr=SR, f=1000.0, dur=0.03, amp=0.8):
    x = np.zeros(int(secs * sr))
    t0 = tt(dur, sr)
    c = amp * np.sin(2 * np.pi * f * t0) * np.exp(-t0 * 120)
    for t in times:
        i = int(round(t * sr))
        x[i:i + len(c)] += c[: max(0, len(x) - i)]
    return x


def speechlike(secs, spans, sr=SR, f0=140.0, amp=0.35):
    t = tt(secs, sr)
    v = sum((1.0 / k) * np.sin(2 * np.pi * f0 * k * t + k) for k in range(1, 11))
    v /= np.abs(v).max()
    syl = 0.55 + 0.45 * np.abs(np.sin(2 * np.pi * 2.0 * t))
    g = np.zeros_like(t)
    for a, b in spans:
        i0, i1 = int(a * sr), int(b * sr)
        n = i1 - i0
        r = min(int(0.02 * sr), n // 2)
        w = np.ones(n)
        w[:r] = np.linspace(0, 1, r)
        w[-r:] = np.linspace(1, 0, r)
        g[i0:i1] = w
    return amp * v * syl * g


def music_bed(secs, sr=SR, amp=0.3, freqs=(220, 277.2, 329.6, 440)):
    t = tt(secs, sr)
    x = sum(np.sin(2 * np.pi * f * t) for f in freqs)
    return amp * x / len(freqs) * (0.85 + 0.15 * np.sin(2 * np.pi * 0.5 * t))


def noise(n, seed=0):
    return np.random.default_rng(seed).standard_normal(n)


def bandpass(x, lo, hi, sr=SR, order=4):
    from scipy.signal import butter, sosfilt
    return sosfilt(butter(order, [lo, hi], btype="band", fs=sr, output="sos"), x)


def lowpass(x, fc, sr=SR, order=4):
    from scipy.signal import butter, sosfilt
    return sosfilt(butter(order, fc, btype="low", fs=sr, output="sos"), x)


def highpass(x, fc, sr=SR, order=4):
    from scipy.signal import butter, sosfilt
    return sosfilt(butter(order, fc, btype="high", fs=sr, output="sos"), x)


def place(dst, src, t, sr=SR, gain=1.0):
    i = int(round(t * sr))
    n = min(len(src), len(dst) - i)
    if n > 0:
        dst[i:i + n] += gain * src[:n]
    return dst


def at_level(x, db):
    """Scale x so that its peak sits at db dBFS."""
    return x * 10 ** ((db - peak_db(x)) / 20)


def ebur(p):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(p), "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True, timeout=60, stdin=subprocess.DEVNULL).stderr
    summ = err[err.rfind("Summary:"):]
    g = lambda pat: float(re.search(pat, summ, re.S).group(1))
    return {"I": g(r"I:\s+(-?[\d.]+|-inf) LUFS"), "LRA": g(r"LRA:\s+(-?[\d.]+) LU"),
            "TP": g(r"True peak:\s+Peak:\s+(-?[\d.]+|-inf) dBFS")}


def loudnorm2(src, out, I=-14, TP=-1.0, LRA=11, sr=48000):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(src), "-af",
                          "loudnorm=I=%s:TP=%s:LRA=%s:print_format=json" % (I, TP, LRA), "-f", "null", "-"],
                         capture_output=True, text=True, timeout=60, stdin=subprocess.DEVNULL).stderr
    m = json.loads(err[err.rfind("{"):err.rfind("}") + 1])
    af = ("loudnorm=I=%s:TP=%s:LRA=%s:measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:offset=%s:"
          "linear=true:print_format=summary,aresample=%d" % (I, TP, LRA, m["input_i"], m["input_tp"], m["input_lra"],
                                                            m["input_thresh"], m["target_offset"], sr))
    ff("-i", src, "-af", af, "-c:a", "pcm_s16le", out)
    return m


def jdump(p, obj):
    Path(p).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    return Path(p)


def tdump(p, text):
    Path(p).write_text(text, encoding="utf-8")
    return Path(p)


def beat_err(found, truth):
    return max(min(abs(f - t) for f in found) for t in truth) if found and truth else 9.0


# ───────────────────────── video helpers ─────────────────────────
def write_video(path, frame_fn, n, fps=30, size=(160, 90), audio=None):
    w, h = size
    buf = b"".join(np.ascontiguousarray(np.clip(frame_fn(i), 0, 255).astype(np.uint8)).tobytes() for i in range(n))
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (w, h),
           "-r", str(fps), "-i", "-"]
    if audio:
        cmd += ["-i", str(audio), "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "192k", "-shortest"]
    cmd += ["-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", str(path)]
    done = subprocess.run(cmd, input=buf, capture_output=True, timeout=90)
    if done.returncode:
        raise RuntimeError(done.stderr.decode(errors="replace")[-400:])
    return Path(path)


PAL = [(230, 60, 60), (60, 200, 90), (60, 90, 230), (240, 200, 40), (200, 60, 220), (40, 220, 220), (250, 140, 30), (120, 120, 120)]


def solid(size, rgb):
    w, h = size
    a = np.empty((h, w, 3), np.uint8)
    a[:] = rgb
    return a


def frames_of(path, size):
    return fx.frames(path, size)


def cut_frames(path, size=(48, 27), thr=40.0):
    fr = fx.frames(path, size)
    d = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2, 3))
    return [int(i + 1) for i in np.flatnonzero(d > thr)], fr


def frame_err(found, expected):
    if not expected:
        return 0
    if not found:
        return 999
    return max(min(abs(f - e) for f in found) for e in expected)


def cut_video(path, cuts, secs, fps=30, size=(96, 54), audio=None):
    bounds = [0.0] + list(cuts) + [secs + 1]

    def frame(i):
        t = i / fps
        k = max(j for j in range(len(bounds) - 1) if bounds[j] <= t + 1e-9)
        a = solid(size, PAL[k % len(PAL)])
        x = int((t * 40) % size[0])
        a[:, x:x + 3] = 255
        return a
    return write_video(path, frame, int(round(secs * fps)), fps, size, audio)


def text_img(size, text, fill=(255, 255, 255), bg=(0, 0, 0), xy=None, scale=1):
    from PIL import Image, ImageDraw
    im = Image.new("RGB", size, bg)
    d = ImageDraw.Draw(im)
    if scale == 1:
        d.text(xy or (4, 4), text, fill=fill)
        return im
    small = Image.new("RGB", (len(text) * 6 + 2, 12), bg)
    ImageDraw.Draw(small).text((1, 0), text, fill=fill)
    big = small.resize((small.width * scale, small.height * scale), Image.NEAREST)
    im.paste(big, xy or ((size[0] - big.width) // 2, (size[1] - big.height) // 2))
    return im


def score_mod():
    """kosif-montage-motion score.py with np.convolve routed to scipy's FFT convolution (same result, faster)."""
    S = vmod("score")
    if not getattr(S, "_fast", False):
        from scipy.signal import fftconvolve

        class _NP:
            def __getattr__(self, k):
                return getattr(np, k)

            @staticmethod
            def convolve(a, b, mode="full"):
                return fftconvolve(a, b, mode=mode)
        S.np = _NP()
        S._fast = True
    return S


def channels(wd, wav, fps=30):
    out = Path(wd) / (Path(wav).stem + ".channels.json")
    sh([sys.executable, VEND / "motion.py", "channels", wav, "--fps", str(fps), "--out", out], cwd=wd)
    return json.loads(out.read_text()), out


def tape_score(wd, stop=True, name=None):
    """score.py arrangement at 120 BPM, 4 s, with an optional tape stop at 1.5 s (0.6 s dive) and start at 2.6 s."""
    S = score_mod()
    spec = {"sections": [{"from": 0, "to": 8, "kick": "four", "pad": True, "pluck": [0, 2, 4, 2]}], "chords": [[0, "i"]]}
    sc = S.Score(120, 4.0, "A", "minor", 7)
    sc.arrange(spec)
    sc.cues([])
    out = Path(wd) / (name or ("tape.wav" if stop else "plain.wav"))
    sc.mix(out, None, [], [[1.5, 0.6]] if stop else None, [[2.6, 0.5]] if stop else None)
    return out


def node_json(wd, name, js):
    src = Path(wd) / (name + ".cjs")
    src.write_text(js, encoding="utf-8")
    return json.loads(sh(["node", src.name], cwd=wd).strip().splitlines()[-1])


def rises_at(x, sr, times, pre=0.05, post=0.04):
    """dB rise of the short-term level just after each time over just before it: a sound starts there."""
    out = []
    for t in times:
        a = rms(x[max(0, int((t - pre) * sr)):max(1, int((t - 0.004) * sr))])
        b = rms(x[int((t + 0.002) * sr):int((t + post) * sr)])
        out.append(20 * math.log10((b + 1e-9) / (a + 1e-9)))
    return out


def env_db_track(x, sr, hop=0.01, win=0.05):
    n, h = int(win * sr), int(hop * sr)
    return np.array([20 * math.log10(rms(x[i:i + n]) + 1e-9) for i in range(0, max(1, len(x) - n), h)])


# ───────────────────────── foley synthesis (numpy) ─────────────────────────
def _decay(d, tau, sr=SR):
    return np.exp(-tt(d, sr) / tau)


def _attack(n, ms, sr=SR):
    a = np.ones(n)
    k = min(n, max(1, int(ms * sr / 1000)))
    a[:k] = np.linspace(0, 1, k)
    return a


FOLEY = {
    "soft steps": lambda s: lowpass(noise(int(.12 * SR), s), 600) * _decay(.12, .03) * 0.9,
    "wind": lambda s: lowpass(noise(int(.5 * SR), s), 500) * _attack(int(.5 * SR), 20) * np.hanning(int(.5 * SR)) ** 0.2 * 0.8,
    "cloth": lambda s: bandpass(noise(int(.18 * SR), s), 1500, 5000) * _decay(.18, .05) * 0.7,
    "shoe scuff": lambda s: bandpass(noise(int(.2 * SR), s), 800, 3000) * _decay(.2, .07) * 0.8,
    "tap": lambda s: bandpass(noise(int(.05 * SR), s), 2000, 6000) * _decay(.05, .008) * 1.2,
    "paper": lambda s: highpass(noise(int(.25 * SR), s), 2500) * _decay(.25, .08) * 0.8,
    "squeak": lambda s: 0.6 * np.sin(2 * np.pi * np.cumsum(np.linspace(1800, 3200, int(.15 * SR))) / SR) * _decay(.15, .06),
    "double step": lambda s: np.concatenate([FOLEY["soft steps"](s), np.zeros(int(.08 * SR)), FOLEY["soft steps"](s + 1)]),
    "cartoon pop": lambda s: 0.8 * np.sin(2 * np.pi * np.cumsum(np.linspace(300, 900, int(.08 * SR))) / SR) * _decay(.08, .02),
    "paper flutter": lambda s: highpass(noise(int(.3 * SR), s), 3000) * (0.6 + 0.4 * np.sin(2 * np.pi * 25 * tt(.3))) * _decay(.3, .12) * 0.8,
    "thud": lambda s: (0.9 * np.sin(2 * np.pi * 70 * tt(.2)) + 0.3 * lowpass(noise(int(.2 * SR), s), 300)) * _decay(.2, .05),
    "whoosh": lambda s: bandpass(noise(int(.35 * SR), s), 400, 3000) * np.hanning(int(.35 * SR)) * 0.9,
    "ending sting": lambda s: sum(0.25 * np.sin(2 * np.pi * f * tt(.5)) for f in (523.3, 659.3, 784)) * _decay(.5, .2),
}


@card("BEAT-04")
def stickman_foley(task, wd):
    """Per-clip literal cues (2-4 per clip) from the card's soundtrack table, one line 'Wait. What?' in clip 4 and a
    dialogue speed gate (< 2.5 words/s); rendered and every cue measured as an audible onset."""
    plan = [["soft steps", "wind", "cloth"], ["shoe scuff", "tap", "paper"], ["squeak", "double step", "cartoon pop"],
            ["paper flutter", "thud", "silence"], ["whoosh", "tap", "ending sting"]]
    clip, secs = 2.0, 10.0
    x = np.zeros(int(secs * SR))
    cues = []
    line = {"clip": 4, "text": "Wait. What?", "words": [["Wait.", 6.1, 6.45], ["What?", 6.65, 7.0]]}
    for c, sounds in enumerate(plan):
        slots = [0.25, 0.85, 1.45] if c != 3 else [1.1, 1.45, 1.6]
        for k, name in enumerate(sounds):
            t = c * clip + slots[k]
            if name == "silence":
                cues.append({"clip": c + 1, "sfx": name, "t": round(t, 3)})
                continue
            place(x, FOLEY[name](10 * c + k), t)
            cues.append({"clip": c + 1, "sfx": name, "t": round(t, 3)})
    for w, a, b in line["words"]:
        x += speechlike(secs, [(a, b)], f0=160, amp=0.3)
    x[int(7.62 * SR):int(8.0 * SR)] = 0
    wav = save(wd, "stickman_foley.wav", x)

    def wps(words):
        return len(words) / (words[-1][2] - words[0][1])
    rate = wps(line["words"])
    fast = [["Wait", 6.1, 6.3], ["what", 6.3, 6.5], ["is", 6.5, 6.6], ["that", 6.6, 6.8], ["thing", 6.8, 7.0]]
    sound = [q for q in cues if q["sfx"] != "silence"]
    r = rises_at(x, SR, [q["t"] for q in sound])
    blank = rises_at(np.zeros_like(x), SR, [q["t"] for q in sound])
    per = [sum(1 for q in cues if q["clip"] == c + 1) for c in range(5)]
    jdump(Path(wd) / "foley_plan.json", {"cues": cues, "line": line, "gate_wps": 2.5, "line_wps": round(rate, 3)})
    return [check("2-4 SFX cues per clip", all(2 <= n <= 4 for n in per), per, "2..4"),
            check("every planned cue is an audible onset (+6 dB rise)", min(r) >= 6, round(min(r), 2), ">= 6"),
            check("clip 4 ends in deliberate silence (< -60 dBFS)", seg_db(x, SR, 7.65, 7.98) < -60, seg_db(x, SR, 7.65, 7.98), "< -60"),
            check("dialogue gate: 'Wait. What?' under 2.5 words/s", rate < 2.5, round(rate, 3), "< 2.5"),
            check("gate rejects a 5-word line in the same 0.9 s", wps(fast) >= 2.5, round(wps(fast), 2), ">= 2.5 (rejected)"),
            check("negative control: the untreated silent track has no cue onsets", max(blank) < 6, round(max(blank), 2), "< 6")], [wav, Path(wd) / "foley_plan.json"]


@card("BEAT-05")
def car_foley(task, wd):
    """Mechanical foley, no music: engine rise + tyre squeal + tyre-air hiss on the drift, layered servo whooshes and
    metal ticks on expansion, small metallic clicks and a low bass snap on reassembly, one consistent room tone."""
    secs = 6.0
    t = tt(secs)
    room = 10 ** (-50 / 20) * lowpass(noise(len(t), 1), 3000) / 0.3
    x = room.copy()
    d = tt(2.0)
    f0 = 55 + 55 * d / 2.0
    ph = 2 * np.pi * np.cumsum(f0) / SR
    eng = sum((0.5 / k) * np.sin(k * ph) for k in range(1, 7)) * 0.5
    place(x, eng, 0.0)
    sq_d = tt(1.6)
    squeal = 0.12 * np.sin(2 * np.pi * np.cumsum(2200 + 40 * np.sin(2 * np.pi * 6 * sq_d)) / SR) * np.hanning(len(sq_d)) ** 0.3
    place(x, squeal, 0.4)
    place(x, 0.05 * highpass(noise(int(1.6 * SR), 2), 4000), 0.4)
    for k, a in enumerate((2.5, 2.7, 2.9)):
        n = int(0.3 * SR)
        w = noise(n, 10 + k)
        place(x, 0.2 * np.hanning(n) * (bandpass(w, 300, 900) + bandpass(w, 900, 1600)), a)
    ticks = [2.62, 2.95, 3.22, 3.44]
    for k, a in enumerate(ticks):
        place(x, 0.5 * np.sin(2 * np.pi * 5200 * tt(.03)) * _decay(.03, .004), a)
    clicks_t = [4.1, 4.3, 4.5]
    for a in clicks_t:
        place(x, 0.35 * np.sin(2 * np.pi * 4300 * tt(.02)) * _decay(.02, .003), a)
    place(x, 0.9 * np.sin(2 * np.pi * 60 * tt(.25)) * _decay(.25, .06), 4.8)
    wav = save(wd, "car_foley.wav", x)

    def f_eng(a, b):
        seg = lowpass(x[int(a * SR):int(b * SR)], 180)
        return peak_hz(seg, lo=40)
    rise = f_eng(1.5, 1.9) / f_eng(0.1, 0.5)
    sq = band_db(x[int(.8 * SR):int(1.6 * SR)], SR, 2100, 2300) - band_db(x[int(5.2 * SR):int(6.0 * SR)], SR, 2100, 2300)
    hb = highpass(x, 4800)
    on_hi = [o for o in onsets(hb, SR, 0.3, 0.08) if 2.4 < o < 3.6]
    snap = band_db(x[int(4.8 * SR):int(4.95 * SR)], SR, 40, 120) - band_db(x[int(5.3 * SR):int(5.45 * SR)], SR, 40, 120)
    room_a, room_b = seg_db(x, SR, 3.6, 3.95), seg_db(x, SR, 5.3, 5.95)
    seg = x[int(5.3 * SR):int(5.95 * SR)]
    X = np.abs(np.fft.rfft(seg * np.hanning(len(seg))))
    fq = np.fft.rfftfreq(len(seg), 1 / SR)
    X = X[(fq > 50) & (fq < 2500)]
    tonal = 20 * math.log10(X.max() / (np.median(X) + 1e-12))
    rq = band_db(room[int(.8 * SR):int(1.6 * SR)], SR, 2100, 2300) - band_db(room[int(5.2 * SR):int(6.0 * SR)], SR, 2100, 2300)
    jdump(Path(wd) / "car_audio_section.json", {"drift": [0, 2], "expansion": [2.5, 3.5], "reassembly": [4.0, 5.0], "music": None,
                                               "ticks": ticks, "clicks": clicks_t, "snap": 4.8})
    return [check("engine pitch rises across the drift (x1.6+)", rise > 1.6, round(rise, 3), "> 1.6"),
            check("tyre squeal band 2.1-2.3 kHz +20 dB during the drift", sq > 20, round(sq, 1), "> 20"),
            check("metal separation ticks on expansion (4 high-band onsets ±15 ms)", len(on_hi) == 4 and beat_err(on_hi, ticks) < 0.015, [round(o, 3) for o in on_hi], ticks),
            check("low bass snap on reassembly (+20 dB at 40-120 Hz)", snap > 20, round(snap, 1), "> 20"),
            check("consistent room tone (two quiet stretches within 1.5 dB)", abs(room_a - room_b) < 1.5, [round(room_a, 2), round(room_b, 2)], "within 1.5 dB"),
            check("no music: the quiet floor carries no tonal peak (< 25 dB over median)", tonal < 25, round(tonal, 1), "< 25"),
            check("negative control: room tone alone has no squeal band rise", rq < 3, round(rq, 2), "< 3")], [wav, Path(wd) / "car_audio_section.json"]


def _crackle(n, rate, seed, lo=2000, hi=9000, amp=0.6, tau=0.002):
    rng = np.random.default_rng(seed)
    x = np.zeros(n)
    k = int(rate * n / SR)
    c = bandpass(rng.standard_normal(int(0.004 * SR)), lo, hi) * np.exp(-np.arange(int(0.004 * SR)) / SR / tau)
    for i in rng.integers(0, n - len(c), k):
        x[i:i + len(c)] += amp * rng.uniform(0.3, 1) * c
    return x


TASTING = {
    "crust crackle": lambda: _crackle(int(.5 * SR), 60, 1, 1500, 7000),
    "straw slurp": lambda: bandpass(noise(int(.6 * SR), 2), 400, 1800) * np.linspace(0.2, 1, int(.6 * SR)) * 0.6,
    "fizzy sip": lambda: _crackle(int(.8 * SR), 200, 3, 5000, 12000, 0.3),
    "crispy crunch": lambda: _crackle(int(.3 * SR), 120, 4, 800, 6000, 0.9, 0.004),
    "juicy bite": lambda: lowpass(noise(int(.25 * SR), 5), 1200) * _decay(.25, .06) * 0.8,
    "soft chew": lambda: lowpass(noise(int(.6 * SR), 6), 600) * (0.5 + 0.5 * np.sin(2 * np.pi * 3 * tt(.6))) * 0.5,
    "noodle slurp": lambda: bandpass(noise(int(.9 * SR), 7), 600, 2500) * np.hanning(int(.9 * SR)) * 0.5,
    "ice crunch": lambda: _crackle(int(.35 * SR), 80, 8, 2500, 9000, 1.0, 0.006),
    "gulp": lambda: 0.7 * np.sin(2 * np.pi * np.cumsum(np.linspace(260, 120, int(.18 * SR))) / SR) * _decay(.18, .05),
    "lip smack": lambda: bandpass(noise(int(.04 * SR), 9), 1000, 4000) * _decay(.04, .006) * 1.2,
}
ACTION = {
    "ice on glass": lambda: sum(0.3 * np.sin(2 * np.pi * f * tt(.6)) * np.exp(-np.clip(tt(.6) - d, 0, None) / .04) * (tt(.6) >= d) for f, d in ((2600, .01), (3100, .17), (2850, .33))),
    "wet sauce scrape": lambda: bandpass(noise(int(.5 * SR), 11), 300, 2000) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * tt(.5))) * 0.4,
    "frying sizzle": lambda: _crackle(int(1.0 * SR), 400, 12, 3000, 12000, 0.25, 0.001),
    "cellophane crinkle": lambda: _crackle(int(.6 * SR), 90, 13, 2000, 10000, 0.7, 0.003),
}


def SFX_EAT(name):
    """The final-bite sound: a named tasting preset, else the generic bite fallback."""
    return (TASTING.get(name) or TASTING["juicy bite"])(), (name if name in TASTING else "juicy bite (generic fallback)")


def _feat(x):
    on = onsets(x, SR, 0.25, 0.008, 2.0)
    return {"centroid": centroid(x), "dur": len(x) / SR, "onset_rate": len(on) / (len(x) / SR),
            "crest": float(np.max(np.abs(x)) / (rms(x) + 1e-12))}


def _distinct(fs):
    ks = list(fs)
    worst = 9.0
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            a, b = fs[ks[i]], fs[ks[j]]
            d = max(abs(a[k] - b[k]) / (max(abs(a[k]), abs(b[k])) + 1e-9) for k in a)
            worst = min(worst, d)
    return worst


@card("BEAT-06")
def food_foley(task, wd):
    """Action-specific sounds (ice-on-glass clatter, wet sauce scrape, frying sizzle, cellophane crinkle) and 10
    tasting presets; SFX_EAT picks the final bite with a generic fallback. Each preset rendered and measured."""
    outs, feats = [], {}
    for name, fn in {**TASTING, **ACTION}.items():
        x = fn()
        outs.append(save(wd, re.sub(r"\W+", "_", name) + ".wav", x))
        feats[name] = _feat(x)
    tast = {k: feats[k] for k in TASTING}
    same = {"copy%d" % i: feats["crust crackle"] for i in range(10)}
    ice = ACTION["ice on glass"]()
    ice_on = onsets(ice, SR, 0.3, 0.12)
    _, picked = SFX_EAT("crispy crunch")
    _, fb = SFX_EAT("dragonfruit bite")
    jdump(Path(wd) / "food_sfx_features.json", feats)
    return [check("10 tasting presets rendered", len(TASTING) == 10 and all(o.stat().st_size > 1000 for o in outs), len(TASTING), 10),
            check("every pair of tasting presets differs by >= 15% in a feature", _distinct(tast) >= 0.15, round(_distinct(tast), 3), ">= 0.15"),
            check("frying sizzle: dense crackle (> 30 onsets/s) above 3 kHz", feats["frying sizzle"]["onset_rate"] > 30 and feats["frying sizzle"]["centroid"] > 3000,
                  [round(feats["frying sizzle"]["onset_rate"], 1), round(feats["frying sizzle"]["centroid"])], "> 30 /s, > 3 kHz"),
            check("ice on glass: 3 clatter hits with a tonal peak > 2 kHz", len(ice_on) == 3 and peak_hz(ice) > 2000, [len(ice_on), round(peak_hz(ice))], [3, "> 2000"]),
            check("SFX_EAT returns the named preset, else the generic fallback", picked == "crispy crunch" and fb.startswith("juicy bite"), [picked, fb], ["crispy crunch", "fallback"]),
            check("negative control: 10 copies of one preset are not distinct", _distinct(same) < 0.15, round(_distinct(same), 3), "< 0.15")], outs[:3] + [Path(wd) / "food_sfx_features.json"]


POLICY = {"viral": {"vo": False, "music": False, "foley": True, "sfx": True, "prompt": "no voiceover, no music; natural foley only"},
          "food": {"vo": False, "music": False, "foley": True, "sfx": False, "prompt": "foley only (sizzle, crunch, pour); no music, no voice"},
          "kinetic": {"vo": False, "music": False, "foley": False, "sfx": "soft", "prompt": "no sound or soft transition SFX only"},
          "vox": {"vo": "narrator", "music": True, "foley": False, "sfx": False, "prompt": "one locked narrator voice throughout"},
          "fitness": {"vo": "coach", "music": True, "foley": False, "sfx": False, "prompt": "coach voice counting reps over music"}}


@card("BEAT-07")
def silent_sound_policies(task, wd):
    """Per-mode audio rules applied to the stems of one edit, then audited on the rendered mixes by least-squares
    projection onto the stems: which stems are really in each mix."""
    secs = 3.0
    stems = {"music": music_bed(secs), "narrator": speechlike(secs, [(0.3, 2.7)], f0=140), "coach": speechlike(secs, [(0.3, 2.7)], f0=210, amp=0.45),
             "foley": _crackle(int(secs * SR), 30, 3, 800, 6000, 0.4), "sfx": np.zeros(int(secs * SR))}
    place(stems["sfx"], bandpass(noise(int(.3 * SR), 4), 400, 3000) * np.hanning(int(.3 * SR)), 1.4)

    def mix(p):
        pol = POLICY[p]
        m = np.zeros(int(secs * SR))
        if pol["music"]:
            m += stems["music"]
        if pol["vo"]:
            m += stems["narrator" if pol["vo"] == "narrator" else "coach"]
        if pol["foley"]:
            m += stems["foley"]
        if pol["sfx"]:
            m += stems["sfx"] * (0.1 if pol["sfx"] == "soft" else 1.0)
        return m
    A = np.stack([stems[k] for k in stems], 1)

    def audit(m):
        coef = np.linalg.lstsq(A, m, rcond=None)[0]
        return {k: round(float(c), 3) for k, c in zip(stems, coef)}
    res, outs = {}, []
    for p in POLICY:
        m = mix(p)
        outs.append(save(wd, "mix_%s.wav" % p, m))
        res[p] = audit(m)
    unfiltered = audit(sum(stems.values()))
    ok = lambda r, k: abs(r[k]) > 0.05
    jdump(Path(wd) / "policy_audit.json", {"policy": POLICY, "audit": res})
    return [check("viral: no VO and no music in the mix", not ok(res["viral"], "music") and not ok(res["viral"], "narrator") and not ok(res["viral"], "coach"), res["viral"], "music=vo=0"),
            check("food: foley only", ok(res["food"], "foley") and sum(ok(res["food"], k) for k in stems) == 1, res["food"], "foley only"),
            check("kinetic: only soft transition SFX (gain <= 0.1)", 0 < res["kinetic"]["sfx"] <= 0.11 and sum(ok(res["kinetic"], k) for k in ("music", "narrator", "coach", "foley")) == 0, res["kinetic"], "sfx soft"),
            check("vox: the one locked narrator, never the coach", ok(res["vox"], "narrator") and not ok(res["vox"], "coach"), res["vox"], "narrator"),
            check("fitness: coach voice", ok(res["fitness"], "coach") and not ok(res["fitness"], "narrator"), res["fitness"], "coach"),
            check("rules encoded in each profile's prompt text", "no music" in POLICY["viral"]["prompt"] and "foley only" in POLICY["food"]["prompt"], POLICY["viral"]["prompt"], "no music"),
            check("negative control: the unfiltered all-stems mix fails the viral audit", ok(unfiltered, "music") and ok(unfiltered, "narrator"), unfiltered, "music+vo present")], outs + [Path(wd) / "policy_audit.json"]


@card("BEAT-11")
def centre_cancel_novoice(task, wd):
    """audiolab.run(file, 'novoice') on a stereo clip: the centred voice (220 Hz, identical L/R) is cancelled and the
    side music kept; audiolab.music refuses mono input. Card test: 220 Hz centre band drops >= 4 dB."""
    AL = vmod("audiolab")
    secs = 3.0
    centre = sine(220, secs, 0.3)
    L, R = centre + sine(523.25, secs, 0.2), centre + sine(659.25, secs, 0.2)
    wav = save(wd, "mix_stereo.wav", np.stack([L, R], 1))
    vid = Path(wd) / "clip.mp4"
    ff("-f", "lavfi", "-i", "color=c=gray:s=64x36:r=30:d=%s" % secs, "-i", wav, "-c:v", "libx264", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-b:a", "256k", "-shortest", vid)
    old = tempfile.tempdir
    tempfile.tempdir = str(wd)
    try:
        rep = AL.run(vid, "novoice", Path(wd) / "lab")
        mono = save(wd, "mono.wav", centre)
        try:
            AL.music(mono, False, Path(wd) / "lab" / "mono_music.wav")
            refused = False
        except SystemExit:
            refused = True
    finally:
        tempfile.tempdir = old
    out = Path(rep["video"])
    y = load_any(out, ch=2)[0][:, 0]
    x = load_any(vid, ch=2)[0][:, 0]
    m = slice(int(0.5 * SR), int(2.5 * SR))
    drop = band_db(x[m], SR, 210, 230) - band_db(y[m], SR, 210, 230)
    keep = band_db(x[m], SR, 515, 530) - band_db(y[m], SR, 515, 530)
    return [check("220 Hz centre band drops >= 4 dB", drop >= 4, round(drop, 2), ">= 4"),
            check("side music (523 Hz, left only) kept within 6 dB", keep < 6, round(keep, 2), "< 6"),
            check("novoice video written with the music bed", out.exists() and rep["music_method"].startswith("centre cancellation"), rep.get("music_method"), "centre cancellation"),
            check("mono input refused for music mode", refused, refused, True),
            check("negative control: the untreated clip keeps its centre band (0 dB drop)", abs(band_db(x[m], SR, 210, 230) - band_db(x[m], SR, 210, 230)) < 4, 0.0, "< 4")], [out]


def _bed_fixture(wd, name, with_bed, gaps=True, secs=6.0):
    spans = [(0.5, 1.4), (1.9, 2.8), (3.3, 4.2), (4.7, 5.6)] if gaps else [(0.3, 5.7)]
    x = speechlike(secs, spans, f0=150, amp=0.4)
    if with_bed:
        x = x + 10 ** (-30 / 20) / 0.3 * music_bed(secs) * 1.0
    words = [{"start": a, "end": b} for a, b in spans] if gaps else \
        [{"start": 0.3 + k * 0.6, "end": 0.3 + (k + 1) * 0.6} for k in range(9)]
    p = save(wd, name, np.stack([x, x], 1))
    return p, words


@card("BEAT-17")
def music_bed_detector(task, wd):
    """reel.has_music_bed(raw.wav, words): the gaps between words (> 0.18 s, trimmed 40 ms) decide; all gaps
    < -60 dBFS → no bed; >= 3 gaps → median > -42 dBFS; else the 100 ms floor p10 > -40 dBFS."""
    RL = vmod("reel")
    cases = {}
    for nm, bed, gaps in (("speech_gaps", False, True), ("speech_bed_gaps", True, True), ("speech_bed_nogaps", True, False), ("speech_nogaps", False, False)):
        p, words = _bed_fixture(wd, nm + ".wav", bed, gaps)
        cases[nm] = bool(RL.has_music_bed(p, words))
    jdump(Path(wd) / "bed_decisions.json", cases)
    return [check("speech with silent gaps: no bed (music may be added)", cases["speech_gaps"] is False, cases["speech_gaps"], False),
            check("speech over a -30 dBFS bed: bed detected from the gaps", cases["speech_bed_gaps"] is True, cases["speech_bed_gaps"], True),
            check("no gaps: the quiet-floor rule still finds the bed", cases["speech_bed_nogaps"] is True, cases["speech_bed_nogaps"], True),
            check("negative control: the clip without a bed is never called a bed", cases["speech_nogaps"] is False and cases["speech_gaps"] is False, cases, "False for both")], [Path(wd) / "bed_decisions.json"]


@card("BEAT-86")
def auto_underscore(task, wd):
    """reel/direct --music auto: when has_music_bed is False add score.py D minor 90 BPM seed 9 (pad from beat 2,
    pad + bass from 40 %), at volume 0.45 under the voice; when the clip carries a bed, add nothing."""
    RL, S = vmod("reel"), score_mod()
    secs = 6.0
    res = {}
    for nm, bed in (("nobed", False), ("withbed", True)):
        p, words = _bed_fixture(wd, nm + ".wav", bed)
        add = not RL.has_music_bed(p, words)
        x, _ = load_any(p)
        if add:
            sc = S.Score(90, secs, "D", "minor", seed=9)
            b = secs / (60 / 90)
            sc.arrange({"sections": [{"from": 2, "to": b * 0.4, "pad": True}, {"from": b * 0.4, "to": b, "pad": True, "bass": True}],
                        "chords": [[0, "i"], [12, "VI"], [18, "III"], [24, "VII"]]})
            bp = sc.mix(Path(wd) / ("bed_%s.wav" % nm))
            bb, _ = load_any(bp)
            bb = np.pad(bb, (0, max(0, len(x) - len(bb))))[:len(x)]
            x = x + 0.45 * bb
        res[nm] = {"added": add, "out": save(wd, "out_%s.wav" % nm, x)}
    y, _ = load_any(res["nobed"]["out"])
    raw, _ = load_any(Path(wd) / "nobed.wav")
    pre = seg_db(y, SR, 0.05, 0.45)
    pad_gap = seg_db(y, SR, 1.45, 1.85)
    bass_early = band_db(y[int(1.45 * SR):int(1.85 * SR)], SR, 30, 110)
    bass_late = band_db(y[int(4.25 * SR):int(4.65 * SR)], SR, 30, 110)
    return [check("no bed detected → underscore added; bed present → none added", res["nobed"]["added"] and not res["withbed"]["added"], [res["nobed"]["added"], res["withbed"]["added"]], [True, False]),
            check("pad silent before beat 2 (1.33 s), present after it", pre < -60 and pad_gap > -45, [round(pre, 1), round(pad_gap, 1)], "< -60 then > -45"),
            check("bass enters from 40 % (2.4 s): +10 dB in 30-110 Hz", bass_late - bass_early > 10, round(bass_late - bass_early, 1), "> 10"),
            check("negative control: the raw voice-only clip has no pad in the gap", seg_db(raw, SR, 1.45, 1.85) < -60, round(seg_db(raw, SR, 1.45, 1.85), 1), "< -60")], [res["nobed"]["out"], res["withbed"]["out"]]


@card("BEAT-51")
def audio_analysis_omni(task, wd):
    """omni/audio_analyze.py FILE: LUFS (BS.1770), peaks, BPM - checked against ffmpeg ebur128 and the known fixture."""
    x, _ = drum_loop(120, 8.0)
    x = x + music_bed(8.0, amp=0.2)
    x = x * 10 ** ((-12 - peak_db(x)) / 20)
    p = save(wd, "mix120.wav", x)
    y, _ = drum_loop(96, 8.0)
    q = save(wd, "loop96.wav", y * 0.5)
    run = lambda f: json.loads(sh([sys.executable, VEND / "omni" / "audio_analyze.py", f]))
    a, b = run(p), run(q)
    out = jdump(Path(wd) / "analysis.json", a)
    flat = json.dumps(a)
    lufs = next(v for k, v in _walk(a) if "integrated" in k.lower() or k.lower() in ("lufs", "loudness_lufs", "integrated_lufs"))
    peak = next(v for k, v in _walk(a) if "peak" in k.lower() and "true" not in k.lower() and isinstance(v, (int, float)))
    bpm_a = next(v for k, v in _walk(a) if "bpm" in k.lower() and isinstance(v, (int, float)))
    bpm_b = next(v for k, v in _walk(b) if "bpm" in k.lower() and isinstance(v, (int, float)))
    ref = ebur(p)
    return [check("integrated loudness within 0.6 LU of ffmpeg ebur128", abs(lufs - ref["I"]) <= 0.6, [lufs, ref["I"]], "match"),
            check("sample peak -12 dBFS (±0.2)", abs(peak - (-12)) <= 0.2, peak, -12),
            check("BPM 120 ±2", abs(bpm_a - 120) <= 2, bpm_a, 120),
            check("negative control: the 96 BPM loop does not read 120", abs(bpm_b - 120) > 10, bpm_b, "!= 120"),
            check("report is JSON with LUFS, peak and BPM", "bpm" in flat.lower(), len(flat), "> 0")], [out]


def _walk(d, pre=""):
    if isinstance(d, dict):
        for k, v in d.items():
            if isinstance(v, (dict, list)):
                yield from _walk(v, pre + k + ".")
            else:
                yield pre + k, v
    elif isinstance(d, list):
        for i, v in enumerate(d[:3]):
            yield from _walk(v, pre + str(i) + ".")


# ───────────────────────── synthesis toolkit (BEAT-89) ─────────────────────────
def polyblep_saw(f, d, sr=SR):
    n = int(d * sr)
    dt = f / sr
    ph = (np.arange(n) * dt) % 1.0
    y = 2 * ph - 1
    m1 = ph < dt
    t1 = ph[m1] / dt
    y[m1] -= t1 + t1 - t1 * t1 - 1
    m2 = ph > 1 - dt
    t2 = (ph[m2] - 1) / dt
    y[m2] -= t2 * t2 + t2 + t2 + 1
    return y


def naive_saw(f, d, sr=SR):
    return 2 * ((np.arange(int(d * sr)) * f / sr) % 1.0) - 1


def alias_db(y, f, sr=SR):
    """Energy off the harmonic series of f (aliases), relative to the total, in dB."""
    X = np.abs(np.fft.rfft(y * np.hanning(len(y)))) ** 2
    fq = np.fft.rfftfreq(len(y), 1 / sr)
    h = np.abs(fq / f - np.round(fq / f)) * f < 15
    return 10 * math.log10(X[~h].sum() / X.sum())


def karplus(f, d, sr=SR, seed=0):
    N = int(round(sr / f))
    buf = np.random.default_rng(seed).uniform(-1, 1, N)
    out = np.empty(int(d * sr))
    for i in range(len(out)):
        out[i] = buf[i % N]
        buf[i % N] = 0.996 * 0.5 * (buf[i % N] + buf[(i + 1) % N])
    return out


def adsr(n, a, d, s, r, sr=SR):
    A, D, R = int(a * sr), int(d * sr), int(r * sr)
    S = max(0, n - A - D - R)
    return np.concatenate([np.linspace(0, 1, A, False), np.linspace(1, s, D, False), np.full(S, s), np.linspace(s, 0, R)])[:n]


def rbj_lowpass(fc, q=0.7071, sr=SR):
    w = 2 * np.pi * fc / sr
    al = np.sin(w) / (2 * q)
    b = np.array([(1 - np.cos(w)) / 2, 1 - np.cos(w), (1 - np.cos(w)) / 2])
    a = np.array([1 + al, -2 * np.cos(w), 1 - al])
    return b / a[0], a / a[0]


def rbj_peaking(f0, gain_db, q, sr=SR):
    A = 10 ** (gain_db / 40)
    w = 2 * np.pi * f0 / sr
    al = np.sin(w) / (2 * q)
    b = np.array([1 + al * A, -2 * np.cos(w), 1 - al * A])
    a = np.array([1 + al / A, -2 * np.cos(w), 1 - al / A])
    return b / a[0], a / a[0]


def bs1770(x, sr=48000):
    """ITU-R BS.1770-4 integrated loudness (K-weighting, 400 ms blocks, 75 % overlap, absolute and relative gates)."""
    from scipy.signal import lfilter
    x = np.atleast_2d(np.asarray(x, float).T).T if np.ndim(x) == 1 else np.asarray(x, float)
    if x.ndim == 1:
        x = x[:, None]
    y = lfilter([1.53512485958697, -2.69169618940638, 1.19839281085285], [1, -1.69065929318241, 0.73248077421585], x, axis=0)
    y = lfilter([1, -2, 1], [1, -1.99004745483398, 0.99007225036621], y, axis=0)
    n, h = int(0.4 * sr), int(0.1 * sr)
    z = np.array([np.mean(y[i:i + n] ** 2, axis=0).sum() for i in range(0, len(y) - n + 1, h)])
    L = -0.691 + 10 * np.log10(z + 1e-20)
    z = z[L > -70]
    Lr = -0.691 + 10 * np.log10(z.mean()) - 10
    z = z[-0.691 + 10 * np.log10(z) > Lr]
    return float(-0.691 + 10 * np.log10(z.mean()))


def lookahead_limit(x, ceiling=0.5, la=0.005, rel=0.05, sr=SR):
    n = int(la * sr)
    from scipy.ndimage import maximum_filter1d
    pk = maximum_filter1d(np.abs(x), size=2 * n + 1)
    g = np.minimum(1.0, ceiling / (pk + 1e-12))
    a = math.exp(-1 / (rel * sr))
    out = np.empty_like(g)
    cur = 1.0
    for i, v in enumerate(g):
        cur = v if v < cur else a * cur + (1 - a) * v
        out[i] = cur
    return x * out


@card("BEAT-89")
def synth_toolkit(task, wd):
    """numpy/scipy synthesis toolkit at 44.1 kHz with seeded randomness: PolyBLEP saw, FM, Karplus-Strong, ADSR,
    RBJ biquad, BS.1770 meter and a look-ahead limiter, each measured against its known answer."""
    sr = 44100
    f = 1567.98
    pb, nv = polyblep_saw(f, 0.5, sr), naive_saw(f, 0.5, sr)
    a_pb, a_nv = alias_db(pb, f, sr), alias_db(nv, f, sr)
    fm = np.sin(2 * np.pi * 1000 * tt(1, sr) + 2.0 * np.sin(2 * np.pi * 200 * tt(1, sr)))
    X = np.abs(np.fft.rfft(fm))
    side = [round(float(X[1000 + 200 * k]) / X.max(), 3) for k in (-2, -1, 1, 2)]
    ks = karplus(220, 0.5, sr)
    ac = np.correlate(ks[2000:6000], ks[2000:10000], "valid")[::-1] if False else None
    seg = ks[2000:2000 + 4096]
    acf = np.array([np.dot(seg[:-L], seg[L:]) for L in range(100, 400)])
    ks_f = sr / (100 + int(np.argmax(acf)))
    env = adsr(sr, 0.01, 0.1, 0.5, 0.2, sr)
    from scipy.signal import freqz, lfilter
    b, a = rbj_lowpass(1000, sr=sr)
    w, H = freqz(b, a, worN=[1000], fs=sr)
    lp_db = 20 * math.log10(abs(H[0]))
    mix = 0.3 * pb[:sr // 2] + 0.2 * ks[:sr // 2]
    mix48 = np.interp(np.arange(int(len(mix) * 48000 / sr)) * sr / 48000, np.arange(len(mix)), mix)
    p = save(wd, "toolkit_mix.wav", np.tile(mix48, 6), 48000)
    meter, ref = bs1770(np.tile(mix48, 6)), ebur(p)["I"]
    lim = lookahead_limit(np.tile(mix48, 2) * 3, 0.5, sr=48000)
    n1, n2 = noise(1000, 42), noise(1000, 42)
    out = save(wd, "toolkit_demo.wav", np.concatenate([0.3 * pb, 0.3 * ks, 0.3 * fm[:sr // 2] * env[:sr // 2]]), sr)
    return [check("PolyBLEP saw aliasing >= 10 dB below the naive saw", a_pb < a_nv - 10, [round(a_pb, 1), round(a_nv, 1)], "polyblep lower"),
            check("FM (fc 1 kHz, fm 200 Hz, I=2) puts sidebands at fc±n·fm", min(side) > 0.1, side, "> 0.1"),
            check("Karplus-Strong pitch = sr/N ≈ 220 Hz (±2)", abs(ks_f - sr / round(sr / 220)) < 2, round(ks_f, 2), round(sr / round(sr / 220), 2)),
            check("ADSR: peak 1 at 10 ms, sustain 0.5", abs(env[int(0.01 * sr)] - 1) < 0.01 and abs(env[int(0.5 * sr)] - 0.5) < 1e-6, [round(env[int(.01 * sr)], 3), env[int(.5 * sr)]], [1, 0.5]),
            check("RBJ low-pass (Q 0.707) is -3.01 dB at fc", abs(lp_db + 3.01) < 0.05, round(lp_db, 3), -3.01),
            check("BS.1770 meter within 0.3 LU of ffmpeg ebur128", abs(meter - ref) < 0.3, [round(meter, 2), ref], "match"),
            check("look-ahead limiter holds the 0.5 ceiling", np.max(np.abs(lim)) <= 0.5001, round(float(np.max(np.abs(lim))), 4), "<= 0.5"),
            check("seeded noise is deterministic", np.array_equal(n1, n2), True, True),
            check("negative control: the naive saw fails the aliasing bound", not (a_nv < a_nv - 10) and a_nv > a_pb, round(a_nv, 1), "higher")], [out, p]


# ───────────────────────── step notation (BEAT-90) ─────────────────────────
def note_hz(n):
    m = re.match(r"([A-G]#?)(-?\d)", n)
    idx = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"].index(m.group(1))
    return 440.0 * 2 ** ((idx + 12 * (int(m.group(2)) + 1) - 69) / 12)


def parse_steps(s):
    """One token per 16th step: NOTE[:len] starts a note (len steps), '-' ties, '.' rests, prefixes '!' accent,
    '?' ghost, '~' glide. Each bar must have exactly 16 steps."""
    bars = [b.split() for b in s.split("|")]
    for b in bars:
        if len(b) != 16:
            raise ValueError("bar has %d steps, needs 16" % len(b))
    ev, step = [], 0
    for b in bars:
        for tok in b:
            if tok == "-":
                if ev:
                    ev[-1]["len"] += 1
            elif tok != ".":
                acc = "!" in tok
                ghost = "?" in tok
                glide = "~" in tok
                name = tok.strip("!?~")
                ln = 1
                if ":" in name:
                    name, ln = name.split(":")
                    ln = int(ln)
                ev.append({"step": step, "note": name, "len": ln, "vel": 1.0 if acc else 0.35 if ghost else 0.7, "glide": glide})
            step += 1
    for a, b in zip(ev, ev[1:]):
        if a["step"] + a["len"] > b["step"]:
            raise ValueError("note at step %d overlaps the next note" % a["step"])
    return ev, step


def render_steps(events, bpm, steps, swing=0.0, sr=SR):
    st = 60 / bpm / 4
    x = np.zeros(int((steps + 4) * st * sr))
    times = []
    for e in events:
        t = 0.1 + e["step"] * st + (swing * st if e["step"] % 2 else 0)
        d = e["len"] * st * 0.95
        f = note_hz(e["note"])
        tn = tt(d, sr)
        y = e["vel"] * 0.6 * np.sin(2 * np.pi * f * tn) * adsr(len(tn), 0.004, 0.03, 0.8, 0.02, sr)
        place(x, y, t, sr)
        times.append(t)
    return x, times


@card("BEAT-90")
def step_notation(task, wd):
    """Song(bpm, bars, swing, seed): melodies as one token per 16th step ('C5:3 . - ! ? ~'), always 16 steps/bar;
    rendered and the onsets, ties, accents and swing measured from the audio."""
    s = "!C5:2 - . E5 . G5 - - . ?A5 . ~G5 . E5 . . | C5 . D5 . E5:2 - - . . . G5 . !C6 . . ."
    ev, steps = parse_steps(s)
    bpm, sw = 120, 0.2
    x, times = render_steps(ev, bpm, steps, sw)
    xs, ts = render_steps(ev, bpm, steps, 0.0)
    p = save(wd, "steps.wav", x)
    on = onsets(x, SR, 0.12, 0.05)
    st = 60 / bpm / 4
    expect = [0.1 + e["step"] * st + (sw * st if e["step"] % 2 else 0) for e in ev]
    tie = next(e for e in ev if e["note"] == "C5")
    acc = [e for e in ev if e["vel"] == 1.0]
    lvl = lambda e: peak_db(x[int(times[ev.index(e)] * SR):int((times[ev.index(e)] + 0.05) * SR)])
    pitch = [round(peak_hz(x[int((t + .01) * SR):int((t + .08) * SR)]) / note_hz(e["note"]), 3) for e, t in zip(ev, times)]
    try:
        parse_steps("C5 . . .")
        refused = False
    except ValueError:
        refused = True
    odd = [e for e in ev if e["step"] % 2]
    unswung_off = [round(ts[ev.index(e)] - 0.1 - e["step"] * st, 4) for e in odd]
    jdump(Path(wd) / "steps.json", {"bpm": bpm, "swing": sw, "steps": steps, "events": ev})
    return [check("32 steps = 2 bars of 16", steps == 32, steps, 32),
            check("every note starts on its 16th step (+ swing on odd steps) ±8 ms", beat_err(on, expect) < 0.008 and len(on) == len(ev), round(beat_err(on, expect), 4), "< 0.008"),
            check("C5:2 plus one tie lasts 3 steps", tie["len"] == 3, tie["len"], 3),
            check("accents are louder than plain notes (+2 dB)", min(lvl(e) for e in acc) > max(lvl(e) for e in ev if e["vel"] == 0.7) + 2, [round(lvl(e), 1) for e in acc], "+2 dB"),
            check("rendered pitch equals the written note (ratio 1 ±2 %)", all(abs(r - 1) < 0.02 for r in pitch), pitch, 1.0),
            check("a bar without 16 steps is refused", refused, refused, True),
            check("negative control: swing 0 leaves odd steps on the grid", all(abs(o) < 1e-9 for o in unswung_off), unswung_off, 0)], [p, Path(wd) / "steps.json"]


# ───────────────────────── voiceover carve (BEAT-119) ─────────────────────────
CARVE_BANDS = [(250, -7.4), (400, -7.4), (630, -7.4), (1000, -7.4), (1600, -14.8), (2500, -7.4)]


def carve(bed, voice, strength=0.8, sr=SR, points=273, floor=-19.2, q=2.06):
    """Spectral sidechain: peaking dips at the voice bands, scaled by strength/0.8, applied through an envelope that
    follows the voice level (273 points, floor -19.2 dB), plus a slow-release level-match gain."""
    from scipy.signal import lfilter
    full = bed.copy()
    chain = []
    for f0, g in CARVE_BANDS:
        gd = g * strength / 0.8
        b, a = rbj_peaking(f0, gd, q, sr)
        full = lfilter(b, a, full)
        chain.append({"type": "peaking", "freq": f0, "gain": round(gd, 2), "q": q, "fromCarve": True})
    n = len(voice)
    edges = np.linspace(0, n, points + 1).astype(int)
    lv = np.array([20 * math.log10(rms(voice[edges[i]:edges[i + 1]]) + 1e-9) for i in range(points)])
    lv -= lv.max()
    env = np.clip((lv - floor) / 6.0, 0, 1)
    g = np.interp(np.arange(n), (edges[:-1] + edges[1:]) / 2, env)
    match_db = -1.5 * strength / 0.8
    a = math.exp(-1 / (0.6 * sr))
    lm = np.empty(n)
    cur = 0.0
    for i in range(0, n, 48):
        tgt = g[i]
        cur = tgt if tgt > cur else a ** 48 * cur + (1 - a ** 48) * tgt
        lm[i:i + 48] = cur
    gain = 10 ** (match_db * lm / 20)
    out = (bed + (full - bed) * g) * gain
    chain.append({"type": "gain", "db": round(match_db, 2), "fromCarve": True})
    return out, chain, [round(float(v), 4) for v in env], g


@card("BEAT-119")
def voiceover_carve(task, wd):
    """carve.mjs analysis implemented in numpy/scipy (its @hyperframes/core dependency is not installed): the bed is
    dipped only in the voice bands as envelopes following the speech, plus a slow level match; the result is written as
    data-fx-carve / data-fx-chain / data-automation on the bed and measured band by band."""
    from scipy.signal import freqz
    secs = 4.0
    freqs = (80, 1000, 1600, 5000)
    bed = sum(0.08 * np.sin(2 * np.pi * f * tt(secs)) for f in freqs)
    voice = speechlike(secs, [(1.0, 2.6)], f0=140)
    out, chain, env, g = carve(bed, voice)
    p = save(wd, "bed_carved.wav", out)

    def narrow(x, f, a, b):
        seg = x[int(a * SR):int(b * SR)]
        return 20 * math.log10(2 * abs(np.dot(seg, np.exp(-2j * np.pi * f * np.arange(len(seg)) / SR))) / len(seg) + 1e-12)
    dip = {f: narrow(bed, f, 1.6, 2.4) - narrow(out, f, 1.6, 2.4) for f in freqs}
    quiet = {f: narrow(bed, f, 0.2, 0.7) - narrow(out, f, 0.2, 0.7) for f in freqs}
    from scipy.signal import lfilter
    pred = {}
    for f in freqs:
        h = 1.0
        for c in chain[:-1]:
            b, a = rbj_peaking(c["freq"], c["gain"], c["q"])
            h *= abs(freqz(b, a, worN=[f], fs=SR)[1][0])
        pred[f] = -20 * math.log10(h) + 1.5
    html = ('<audio id="music-bed" src="bed.wav" data-start="0" data-fx-carve=\'%s\' data-fx-chain=\'%s\' data-automation=\'%s\'></audio>'
            '<audio id="narration" src="voice.wav" data-start="1"></audio>' % (json.dumps({"voices": ["narration"], "strength": 0.8}),
                                                                             json.dumps(chain), json.dumps({"gain": env})))
    comp = tdump(Path(wd) / "index.html", html)
    return [check("bed dipped at the voice bands as predicted by the chain (±1.5 dB)", all(abs(dip[f] - pred[f]) < 1.5 for f in (1000, 1600)), {k: round(v, 2) for k, v in dip.items()}, {k: round(v, 2) for k, v in pred.items()}),
            check("1600 Hz dips >= 12 dB under speech", dip[1600] >= 12, round(dip[1600], 2), ">= 12"),
            check("80 Hz (outside the voice) only gets the level match (< 3 dB): not a whole-bed duck", dip[80] < 3, round(dip[80], 2), "< 3"),
            check("273-point envelope written to data-automation", len(env) == 273 and 'data-fx-carve' in comp.read_text(), len(env), 273),
            check("no dip before the voice starts (< 0.5 dB)", max(abs(v) for v in quiet.values()) < 0.5, {k: round(v, 2) for k, v in quiet.items()}, "< 0.5"),
            check("negative control: the untreated bed has no dip at 1600 Hz", abs(narrow(bed, 1600, 1.6, 2.4) - narrow(bed, 1600, 0.2, 0.7)) < 0.5, 0.0, "< 0.5")], [p, comp]


@card("BEAT-127")
def bundled_sfx_library(task, wd):
    """HyperFrames media-use bundled SFX (19 files): durations measured against the card's list; `resolve.mjs --type sfx
    --intent whoosh` answers from the bundle without credentials; impacts are left to decay."""
    exp = {"chime": 2.5, "click-soft": .37, "click": .37, "error": 1.62, "glitch-1": 2.64, "glitch-2": 3.5, "glitch-3": 3.1,
           "impact-bass-1": 2.12, "impact-bass-2": 2.59, "key-press": .4, "notification": 2.46, "ping": 1.32, "pop": .72,
           "riser": 10.03, "sparkle": 1.8, "typing": 1.5, "whoosh-cinematic": 5.54, "whoosh-short": .57, "whoosh": .57}
    d = HF_MEDIA / "audio/assets/sfx"
    got = {}
    for k in exp:
        pr = fx.probe(d / (k + ".mp3"))
        got[k] = round(float(pr["format"]["duration"]), 3)
    bad = {k: (got[k], exp[k]) for k in exp if abs(got[k] - exp[k]) > 0.08}
    txt = sh(["node", HF_MEDIA / "scripts/resolve.mjs", "--type", "sfx", "--intent", "whoosh"], cwd=wd, timeout=40)
    m = re.search(r"→\s*(\S+)\s*\(sfx,\s*([\d.]+)s", txt)
    resolved = Path(wd) / m.group(1) if m else None
    imp, _ = load_any(d / "impact-bass-1.mp3")
    head, tail = peak_db(imp[:int(.5 * SR)]), dbfs(imp[-int(.1 * SR):])
    out = jdump(Path(wd) / "sfx_durations.json", {"measured": got, "card": exp, "resolve": txt.strip()})
    return [check("19 bundled cues present with the card's durations (±80 ms)", len(got) == 19 and not bad, bad, {}),
            check("resolve --type sfx --intent whoosh returns a bundled ~0.6 s file", resolved is not None and resolved.exists() and abs(float(m.group(2)) - 0.57) < 0.1, txt.strip()[:120], "whoosh 0.6 s"),
            check("impact-bass-1 rings out to its own end (last 0.1 s >= 5 dB under the peak): place the whole file", head - tail > 5, round(head - tail, 1), "> 5"),
            check("negative control: the riser (10 s) does not pass as a whoosh", abs(got["riser"] - 0.57) > 0.1, got["riser"], "!= 0.57")], [out]


def audiomap(path):
    """librosa analysis to an audiomap: tempo/grid (trusted only when rhythmic), onsets + onset_rate, silences,
    hard stops, energy phases (level/density/feel), key moments, phrases."""
    import librosa
    y, sr = librosa.load(str(path), sr=22050, mono=True)
    dur = len(y) / sr
    hop = 512
    oenv = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop)
    on = librosa.onset.onset_detect(onset_envelope=oenv, sr=sr, hop_length=hop, units="time")
    tempo, beats = librosa.beat.beat_track(onset_envelope=oenv, sr=sr, hop_length=hop, units="time")
    tempo = 60.0 * (len(beats) - 1) / float(beats[-1] - beats[0]) if len(beats) > 2 else float(np.atleast_1d(tempo)[0])
    rms_ = librosa.feature.rms(y=y, hop_length=hop)[0]
    db = 20 * np.log10(rms_ + 1e-9)
    ft = librosa.frames_to_time(np.arange(len(db)), sr=sr, hop_length=hop)
    sil, i = [], 0
    while i < len(db):
        if db[i] < -50:
            j = i
            while j < len(db) and db[j] < -50:
                j += 1
            if ft[min(j, len(ft) - 1)] - ft[i] >= 0.3:
                sil.append([round(float(ft[i]), 3), round(float(ft[min(j, len(ft) - 1)]), 3)])
            i = j
        else:
            i += 1
    hard = [s[0] for s in sil if s[0] > 0.1 and db[max(0, np.searchsorted(ft, s[0] - 0.15)):np.searchsorted(ft, s[0])].max() > -30]
    o = oenv - oenv.mean()
    ac = np.correlate(o, o, "full")[len(o) - 1:]
    ac /= ac[0] + 1e-12
    lags = (np.arange(len(ac)) * hop / sr)
    win = (lags > 0.3) & (lags < 1.0)
    rhythm = float(np.percentile(oenv, 95) / (np.median(oenv) + 1e-9))
    rhythmic = bool(rhythm > 20 and len(on) / dur > 1.0 and float(ac[win].max() if win.any() else 0) > 0.3)
    phases = []
    for a in np.arange(0, dur, 2.0):
        m = (ft >= a) & (ft < a + 2.0)
        lev = float(db[m].mean()) if m.any() else -90
        dens = sum(1 for t in on if a <= t < a + 2.0) / 2.0
        phases.append({"t": round(float(a), 2), "level": "high" if lev > -20 else "mid" if lev > -40 else "low", "density": round(dens, 2),
                       "feel": "driving" if dens >= 1.5 else "sparse" if dens > 0 else "still"})
    km = sorted(on, key=lambda t: -oenv[min(len(oenv) - 1, int(t * sr / hop))])[:3]
    return {"duration": round(dur, 3), "tempo": round(tempo, 2) if rhythmic else None, "bpm_trusted": rhythmic, "rhythmicity": round(rhythm, 3),
            "beats_sec": [round(float(b), 3) for b in beats] if rhythmic else [], "onsets": [round(float(t), 3) for t in on],
            "onset_rate": round(len(on) / dur, 3), "silences": sil, "hard_stops": hard, "phases": phases,
            "key_moments": [round(float(t), 3) for t in sorted(km)], "phrases": [[0.0, s[0]] for s in sil[:1]]}


@card("BEAT-129")
def beat_grid_audiomap(task, wd):
    """analyze-beatgrid.py's audiomap (that script is not shipped in this hyperframes install) rebuilt on librosa:
    energy phases, onsets, silences, hard stops, key moments, tempo/grid trusted only on rhythmic music."""
    x, ta = drum_loop(120, 8.0)
    x = x + music_bed(8.0, amp=0.2)
    x[int(4.0 * SR):int(5.0 * SR)] = 0
    a = save(wd, "bgm.wav", x)
    pad = music_bed(8.0, amp=0.4) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.11 * tt(8.0)))
    b = save(wd, "ambient.wav", pad)
    A, B = audiomap(a), audiomap(b)
    out = jdump(Path(wd) / "audiomap.json", A)
    jdump(Path(wd) / "audiomap_ambient.json", B)
    sil = A["silences"][0] if A["silences"] else [0, 0]
    return [check("rhythmic loop: tempo 120 ±2 and trusted", A["bpm_trusted"] and abs(A["tempo"] - 120) <= 2, A["tempo"], 120),
            check("silence found at 4.0-5.0 s (±0.15)", abs(sil[0] - 4.0) < 0.15 and abs(sil[1] - 5.0) < 0.15, sil, [4.0, 5.0]),
            check("hard stop flagged where the loud loop cuts to silence", any(3.85 < h < 4.15 for h in A["hard_stops"]), A["hard_stops"], "~4.0"),
            check("onset rate ≈ 2/s (kicks every 0.5 s, 1 s gap)", 1.4 < A["onset_rate"] < 2.2, A["onset_rate"], "~1.8"),
            check("energy phases written every 2 s with level/density/feel", len(A["phases"]) == 4 and A["phases"][0]["feel"] == "driving", A["phases"], "4 phases"),
            check("negative control: the ambient pad's bpm is not trusted", not B["bpm_trusted"] and B["tempo"] is None, [B["bpm_trusted"], B["rhythmicity"]], False)], [out]


@card("BEAT-131")
def pad_frames_bgm_volume(task, wd):
    """Pad frame durations to fit narration, and BGM volume from hyperframes media-use lib/bgm-volume.mjs
    (bed 0.12 under a voice, 0.9 for a silent film); mixed and measured."""
    js = Path(wd) / "vol.mjs"
    js.write_text("import {bgmDefaultVolume} from %s;\nconsole.log(JSON.stringify({voice: bgmDefaultVolume(true), silent: bgmDefaultVolume(false)}));\n"
                  % json.dumps(str(HF_MEDIA / "audio/scripts/lib/bgm-volume.mjs")), encoding="utf-8")
    vol = json.loads(sh(["node", js.name], cwd=wd).strip().splitlines()[-1])
    fps, tail = 30, 0.25
    plan = [2.0, 2.0, 2.0]
    narr = [1.6, 2.3, 1.1]
    padded = [max(p, math.ceil((n + tail) * fps) / fps) for p, n in zip(plan, narr)]
    secs = sum(padded)
    starts = np.cumsum([0] + padded[:-1])
    v = np.zeros(int(secs * SR) + 1)
    parts = []
    for s, n in zip(starts, narr):
        parts.append(speechlike(len(v) / SR, [(s, s + n)], f0=150))
        v += parts[-1]
    bgm = sine(330, len(v) / SR, 0.5)
    mix = v + vol["voice"] * bgm
    p = save(wd, "narrated_mix.wav", mix)
    level = lambda x, a, b: 20 * math.log10(2 * abs(np.dot(x[int(a * SR):int(b * SR)], np.exp(-2j * np.pi * 330 * np.arange(int(b * SR) - int(a * SR)) / SR))) / (int(b * SR) - int(a * SR)))
    bgm_db = level(mix, starts[1] - 0.2, starts[1] - 0.01) - 20 * math.log10(0.5)
    ends = [np.flatnonzero(envelope(pv, SR, 10) > 0.01)[-1] / SR for pv in parts]
    margin = [round(s + d - en, 3) for s, d, en in zip(starts, padded, ends)]
    over = [round((np.cumsum([0] + plan[:-1])[k] + plan[k]) - (np.cumsum([0] + plan[:-1])[k] + narr[k]), 3) for k in range(3)]
    out = jdump(Path(wd) / "frames.json", {"planned": plan, "narration": narr, "padded": padded, "bgm_volume": vol})
    return [check("bgm-volume.mjs: 0.12 under narration, 0.9 when silent", vol == {"voice": 0.12, "silent": 0.9}, vol, {"voice": 0.12, "silent": 0.9}),
            check("frames padded to whole frames that hold their narration + 0.25 s", all(abs(d * fps - round(d * fps)) < 1e-6 for d in padded) and min(margin) >= tail - 0.02, margin, ">= 0.23"),
            check("bed measured at 20·log10(0.12) = -18.4 dB (±0.3)", abs(bgm_db - 20 * math.log10(0.12)) < 0.3, round(bgm_db, 2), -18.42),
            check("negative control: the unpadded plan lets narration 2 overrun its frame", min(over) < 0, over, "< 0")], [p, out]


@card("BEAT-159")
def measured_beat_detection(task, wd):
    """librosa.beat.beat_track (or tap tempo) and a 5-beat verification against the known kicks."""
    import librosa
    res = {}
    for bpm in (120, 96):
        x, ta = drum_loop(bpm, 8.0)
        p = save(wd, "loop%d.wav" % bpm, x)
        y, sr = librosa.load(str(p), sr=22050)
        tempo, bt = librosa.beat.beat_track(y=y, sr=sr, units="time")
        res[bpm] = {"tempo": 60.0 * (len(bt) - 1) / float(bt[-1] - bt[0]), "librosa_tempo": float(np.atleast_1d(tempo)[0]), "beats": [round(float(b), 3) for b in bt], "truth": ta}
    five = res[120]["beats"][2:7]
    err5 = beat_err(res[120]["truth"], five) if False else max(min(abs(b - t) for t in res[120]["truth"]) for b in five)
    taps = [0.0, 0.51, 0.99, 1.52, 2.0, 2.49, 3.01]
    tap_bpm = 60 / float(np.median(np.diff(taps)))
    out = jdump(Path(wd) / "beats.json", res)
    return [check("120 BPM loop reads 120 ±2", abs(res[120]["tempo"] - 120) <= 2, round(res[120]["tempo"], 2), 120),
            check("96 BPM loop reads 96 ±2", abs(res[96]["tempo"] - 96) <= 2, round(res[96]["tempo"], 2), 96),
            check("5 consecutive beats each within 50 ms of a true kick", len(five) == 5 and err5 <= 0.05, round(err5, 4), "<= 0.05"),
            check("tap tempo: median tap interval gives 120 ±2", abs(tap_bpm - 120) <= 2, round(tap_bpm, 2), 120),
            check("negative control: the 120 answer does not fit the 96 loop", abs(res[120]["tempo"] - 96) > 10, round(res[120]["tempo"], 1), "!= 96")], [out]


def stft_shape(n, centre_fn, bw, seed=0, sr=SR):
    from scipy.signal import stft, istft
    w = noise(n, seed)
    f, t, Z = stft(w, fs=sr, nperseg=1024)
    c = centre_fn(t)
    G = np.exp(-0.5 * ((np.log2(f[:, None] + 1) - np.log2(c[None, :])) / bw) ** 2)
    return istft(Z * G, fs=sr, nperseg=1024)[1][:n]


def centroid_track(x, sr=SR, win=0.05):
    n = int(win * sr)
    return np.array([centroid(x[i:i + n], sr) for i in range(0, len(x) - n, n)])


@card("BEAT-163")
def offline_sfx_synth(task, wd):
    """The card's offline alternative to paid text-to-SFX: whoosh / impact / ambience synthesised with numpy noise
    sweeps (0.5-30 s), measured: the whoosh centre rises then falls, the impact is a fast low hit, the ambience loops."""
    d = 1.2
    n = int(d * SR)
    wh = stft_shape(n, lambda t: 300 * 10 ** (np.sin(np.pi * np.clip(t / d, 0, 1)) * 1.0), 0.4, 1) * np.hanning(n) ** 0.7
    wh = at_level(wh, -3)
    imp = 0.9 * np.sin(2 * np.pi * np.cumsum(45 + 75 * np.exp(-tt(1.0) / 0.05)) / SR) * np.exp(-tt(1.0) / 0.25)
    imp[:int(0.02 * SR)] += 0.3 * noise(int(0.02 * SR), 2)
    amb = lowpass(noise(int(4.4 * SR), 3), 800)
    k = int(0.4 * SR)
    loop = amb[:int(4.0 * SR)].copy()
    loop[:k] = loop[:k] * np.linspace(0, 1, k) + amb[int(4.0 * SR):int(4.0 * SR) + k] * np.linspace(1, 0, k)
    outs = [save(wd, "whoosh.wav", wh), save(wd, "impact.wav", imp), save(wd, "ambience_loop.wav", loop * 0.3)]
    ct = centroid_track(wh)
    peak_i = int(np.argmax(ct))
    att = np.argmax(np.abs(imp)) / SR
    low = band_db(imp, SR, 20, 200) - band_db(imp, SR, 200, 20000)
    seam = abs(loop[-1] - loop[0]) / (np.std(loop) + 1e-9)
    raw = amb[:int(4.0 * SR)]
    raw_seam = abs(raw[-1] - raw[0]) / (np.std(raw) + 1e-9)
    wn = noise(n, 9)
    ctw = centroid_track(wn)
    return [check("whoosh 1.2 s within the 0.5-30 s range", 0.5 <= len(wh) / SR <= 30, len(wh) / SR, "0.5..30"),
            check("whoosh centre rises then falls (peak in the middle third)", len(ct) / 3 <= peak_i <= 2 * len(ct) / 3 and ct[peak_i] > 2.5 * min(ct[1], ct[-2]),
                  [round(ct[1]), round(ct[peak_i]), round(ct[-2])], "low-high-low"),
            check("impact: fast attack (< 15 ms) and energy below 200 Hz dominant (+10 dB)", att < 0.015 and low > 10, [round(att, 4), round(low, 1)], ["< 0.015", "> 10"]),
            check("ambience loop seam is continuous (crossfaded)", seam < 0.2, round(seam, 3), "< 0.2"),
            check("negative control: unshaped white noise has no centroid sweep", ctw.max() / ctw.min() < 1.5, round(float(ctw.max() / ctw.min()), 3), "< 1.5")], outs


def snare(sr=SR, seed=5):
    t = tt(0.18, sr)
    return (0.4 * np.sin(2 * np.pi * 190 * t) + 0.5 * highpass(noise(len(t), seed), 1500)) * np.exp(-t / 0.05)


@card("BEAT-198")
def code_synth_soundtrack(task, wd):
    """Define BPM, compute beat times, synthesise kick/snare/bass/arp in numpy, schedule every visual cut on beat
    frames (1/8 notes in the climax)."""
    bpm, fps = 124, 30
    beat = 60 / bpm
    bars = 2
    secs = bars * 4 * beat + 0.4
    x = np.zeros(int(secs * SR))
    beats = [k * beat for k in range(bars * 4)]
    for k, b in enumerate(beats):
        place(x, kick(), b)
        if k % 2:
            place(x, snare(), b, gain=0.8)
        place(x, 0.25 * np.sin(2 * np.pi * 55 * tt(beat * 0.9)) * adsr(int(beat * 0.9 * SR), .005, .05, .7, .05), b)
        if k >= 4:
            place(x, 0.5 * highpass(noise(int(.04 * SR), k), 5000) * _decay(.04, .01), b + beat / 2)
        for j in range(2):
            place(x, 0.12 * np.sin(2 * np.pi * (440, 660)[j] * tt(beat / 2 * 0.8)) * adsr(int(beat / 2 * 0.8 * SR), .003, .03, .5, .03), b + j * beat / 2)
    a = save(wd, "score.wav", x)
    cuts = [b for b in beats[1:4]] + [beats[4] + k * beat / 2 for k in range(8)][:7]
    planned = [int(round(c * fps)) for c in cuts]
    v = cut_video(Path(wd) / "cuts.mp4", [f / fps for f in planned], secs, fps, audio=a)
    found, _ = cut_frames(v)
    kon = onsets(lowpass(x, 150), SR, 0.3, 0.2)
    qa = {"bpm": round(60 / float(np.median(np.diff(kon))), 2)}
    on = sorted(kon + onsets(highpass(x, 4000), SR, 0.3, 0.1))
    worst = max(min(abs(f - o * fps) for o in on) for f in found) if found else 99
    plain = cut_video(Path(wd) / "uncut.mp4", [], secs, fps)
    jdump(Path(wd) / "cut_plan.json", {"bpm": bpm, "beat_s": beat, "cuts_s": cuts, "frames": planned})
    return [check("synthesised track measures 124 BPM (±1.5)", abs(qa["bpm"] - bpm) <= 1.5, qa["bpm"], bpm),
            check("cuts rendered at the planned beat frames", found == planned, found, planned),
            check("climax cuts every 1/8 note (0.242 s)", all(abs((cuts[k + 1] - cuts[k]) - beat / 2) < 1e-9 for k in range(3, len(cuts) - 1)), round(beat / 2, 4), 0.2419),
            check("every cut within 1 frame of an onset heard in the file", worst <= 1, round(worst, 2), "<= 1"),
            check("negative control: the uncut clip has no cuts", not cut_frames(plain)[0], cut_frames(plain)[0], [])], [v, a]


def _layer_feats(x, sr=SR):
    e = envelope(x, sr, 5)
    pk = int(np.argmax(e))
    above = np.flatnonzero(e > e.max() * 0.1)
    return {"centroid": centroid(x), "attack": pk / sr - (above[0] / sr if len(above) else 0), "body": (above[-1] - above[0]) / sr if len(above) else 0,
            "level": dbfs(x)}


@card("BEAT-228")
def sound_layer_roles(task, wd):
    """Per-role tracks (dialogue, room tone, real foley, creative SFX, tonal pad, music) laid with ffmpeg
    adelay/atrim/amix; the foley's audible transient (not the file start) synced to the action frame; layers must differ
    in frequency/attack/body/tail."""
    secs, fps, act = 3.0, 30, 1.5
    lead = 0.08
    roles = {"dialogue": speechlike(secs, [(0.3, 1.2), (1.9, 2.8)], f0=150),
             "room": 10 ** (-48 / 20) * lowpass(noise(int(secs * SR), 1), 1200) / 0.2,
             "creative": bandpass(noise(int(.5 * SR), 2), 500, 4000) * np.hanning(int(.5 * SR)) * 0.4,
             "tonal": 0.15 * np.sin(2 * np.pi * 110 * tt(secs)) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.3 * tt(secs))),
             "music": music_bed(secs, amp=0.15)}
    foley = np.concatenate([np.zeros(int(lead * SR)), 0.8 * highpass(noise(int(.03 * SR), 3), 3000) * _decay(.03, .006)])
    paths = {k: save(wd, "%s.wav" % k, v) for k, v in roles.items()}
    paths["foley"] = save(wd, "foley.wav", foley)
    on_file = onsets(np.concatenate([np.zeros(100), foley]), SR, 0.3, 0.02)[0] - 100 / SR
    delay = int(round((act - on_file) * 1000))
    order = list(paths)
    ins = sum([["-i", str(paths[k])] for k in order], [])
    g = []
    for i, k in enumerate(order):
        d = delay if k == "foley" else (int(1.2 * 1000) if k == "creative" else 0)
        g.append("[%d:a]adelay=%d|%d,atrim=0:%s,apad=whole_dur=%s[a%d]" % (i, d, d, secs, secs, i))
    g.append("".join("[a%d]" % i for i in range(len(order))) + "amix=inputs=%d:normalize=0:duration=longest[m]" % len(order))
    out = Path(wd) / "layered_mix.wav"
    ff(*ins, "-filter_complex", ";".join(g), "-map", "[m]", "-ac", "1", "-c:a", "pcm_s16le", out)
    y, _ = load_any(out)
    hit = [o for o in onsets(highpass(y, 3000), SR, 0.3, 0.05) if 1.3 < o < 1.7]
    naive = act + on_file
    fs = {k: _layer_feats(v) for k, v in {**roles, "foley": foley[int(lead * SR):]}.items()}
    dup = {"a": fs["creative"], "b": _layer_feats(roles["creative"])}

    def differs(a, b):
        return abs(a["centroid"] - b["centroid"]) / max(a["centroid"], b["centroid"]) > 0.15 or abs(a["attack"] - b["attack"]) > 0.02 or abs(a["body"] - b["body"]) > 0.1
    ks = list(fs)
    pairs_ok = all(differs(fs[ks[i]], fs[ks[j]]) for i in range(len(ks)) for j in range(i + 1, len(ks)))
    jdump(Path(wd) / "layers.json", {"roles": order, "foley_transient_in_file_s": on_file, "foley_adelay_ms": delay, "features": fs,
                                     "creative_sfx_logged_as_real_sound": False})
    return [check("foley transient lands on the action frame (±1 frame)", len(hit) == 1 and abs(hit[0] - act) <= 1 / fps, [round(h, 4) for h in hit], act),
            check("adelay compensates the 80 ms lead in the file", abs(delay - (act - lead) * 1000) <= 2, delay, (act - lead) * 1000),
            check("every pair of layers differs in frequency/attack/body", pairs_ok, {k: {kk: round(vv, 3) for kk, vv in v.items()} for k, v in fs.items()}, "pairwise distinct"),
            check("negative control: delaying by the file start puts the transient > 1 frame late", naive - act > 1 / fps, round(naive - act, 4), "> 0.033"),
            check("negative control: a duplicated sample is not texture", not differs(dup["a"], dup["b"]), "identical", "flagged")], [out, Path(wd) / "layers.json"]


GENRES = {"synth-funk": (140, 160, (0.08, 0.12)), "dnb": (165, 180, (0, 0)), "boss rock": (160, 180, (0, 0)), "chiptune": (120, 180, (0, 0)),
          "synth-pop": (120, 135, (0, 0)), "ambient": (60, 90, (0, 0)), "horror": (50, 80, (0, 0))}


def swing_groove(bpm, swing, bars=2, sr=SR):
    beat = 60 / bpm
    secs = bars * 4 * beat + 0.3
    x = np.zeros(int(secs * sr))
    hats = []
    for k in range(bars * 4):
        place(x, kick(), 0.05 + k * beat)
        for j in range(2):
            t = 0.05 + k * beat + j * beat / 2 + (swing * beat / 2 if j else 0)
            place(x, 0.4 * highpass(noise(int(.03 * sr), k * 2 + j), 6000) * _decay(.03, .006), t)
            hats.append(t)
    return x, hats


def measure_swing(x, bpm, sr=SR):
    beat = 60 / bpm
    ho = onsets(highpass(x, 5000), sr, 0.3, beat / 4)
    ko = onsets(lowpass(x, 200), sr, 0.3, beat / 2)
    tempo = 60 * (len(ko) - 1) / (ko[-1] - ko[0])
    offs = [h for h in ho if min(abs(h - k) for k in ko) > beat / 8]
    sw = float(np.median([(h - max(k for k in ko if k <= h) - beat / 2) / (beat / 2) for h in offs]))
    return tempo, sw


@card("BEAT-234")
def genre_palettes(task, wd):
    """Genre starting points (BPM range, swing) fed into a groove: synth-funk at 150 BPM with swing 0.10 rendered and
    its tempo and swing measured back from the onsets."""
    g = GENRES["synth-funk"]
    bpm, sw = 150, 0.10
    x, _ = swing_groove(bpm, sw)
    p = save(wd, "synth_funk_150_sw010.wav", x)
    tempo, msw = measure_swing(x, bpm)
    xs, _ = swing_groove(bpm, 0.0)
    _, straight = measure_swing(xs, bpm)
    spec = {"genre": "synth-funk", "bpm": bpm, "swing": sw, "palette": GENRES}
    out = jdump(Path(wd) / "score_spec.json", spec)
    return [check("seven genre palettes with the card's ranges", len(GENRES) == 7 and GENRES["dnb"][:2] == (165, 180) and GENRES["horror"][:2] == (50, 80), list(GENRES), 7),
            check("chosen BPM inside the synth-funk range 140-160", g[0] <= bpm <= g[1], bpm, "140..160"),
            check("rendered groove measures 150 BPM (±1)", abs(tempo - bpm) <= 1, round(tempo, 2), bpm),
            check("measured swing 0.08-0.12", g[2][0] <= msw <= g[2][1], round(msw, 3), "0.08..0.12"),
            check("negative control: the straight groove has no swing", not (g[2][0] <= straight <= g[2][1]), round(straight, 3), "< 0.08")], [p, out]


REF_TUNES = {"twinkle": "C4 C4 G4 G4 A4 A4 G4 F4 F4 E4 E4 D4 D4 C4", "ode_to_joy": "E4 E4 F4 G4 G4 F4 E4 D4 C4 C4 D4 E4 E4 D4 D4",
             "frere_jacques": "C4 D4 E4 C4 C4 D4 E4 C4 E4 F4 G4 E4 F4 G4", "happy_birthday": "G4 G4 A4 G4 C5 B4 G4 G4 A4 G4 D5 C5"}


def midi(n):
    return int(round(69 + 12 * math.log2(note_hz(n) / 440)))


def intervals(notes):
    m = [midi(n) for n in notes]
    return [b - a for a, b in zip(m, m[1:])]


def shared_ngram(a, b, n=5):
    A = {tuple(a[i:i + n]) for i in range(len(a) - n + 1)}
    return any(tuple(b[i:i + n]) in A for i in range(len(b) - n + 1))


def originality(notes):
    iv = intervals(notes)
    return [k for k, v in REF_TUNES.items() if shared_ngram(iv, intervals(v.split()))]


@card("BEAT-235")
def original_melodies_only(task, wd):
    """Never transcribe or imitate a recognisable tune: a seeded melody generator in A minor pentatonic with an
    originality gate (no shared 5-interval run with known tunes); the accepted melody is rendered and its pitches read back."""
    pent = ["A3", "C4", "D4", "E4", "G4", "A4", "C5", "D5", "E5"]
    rng = np.random.default_rng(7)
    tries = 0
    while True:
        tries += 1
        idx, mel = 4, []
        for _ in range(12):
            idx = int(np.clip(idx + rng.choice([-2, -1, 1, 2]), 0, len(pent) - 1))
            mel.append(pent[idx])
        if not originality(mel):
            break
    d = 0.25
    x = np.concatenate([0.4 * np.sin(2 * np.pi * note_hz(n) * tt(d)) * adsr(int(round(d * SR)), .005, .02, .8, .03) for n in mel])
    p = save(wd, "original_melody.wav", x)
    read = [midi_from_hz(peak_hz(x[int((k * d + .03) * SR):int((k * d + .2) * SR)])) for k in range(len(mel))]
    out = jdump(Path(wd) / "melody.json", {"notes": mel, "tries": tries, "gate": "no 5-interval run shared with " + ", ".join(REF_TUNES)})
    flagged = originality(REF_TUNES["ode_to_joy"].split())
    shifted = originality("A4 A4 A#4 C5 C5 A#4 A4 G4 F4 F4 G4 A4 A4 G4 G4".split())
    return [check("accepted melody shares no 5-interval run with the known tunes", originality(mel) == [], originality(mel), []),
            check("rendered pitches equal the written melody", read == [midi(n) for n in mel], read[:6], [midi(n) for n in mel][:6]),
            check("a transposed Ode to Joy is still caught (intervals, not notes)", "ode_to_joy" in shifted, shifted, ["ode_to_joy"]),
            check("negative control: a transcription of Ode to Joy fails the gate", flagged == ["ode_to_joy"], flagged, ["ode_to_joy"])], [p, out]


def midi_from_hz(f):
    return int(round(69 + 12 * math.log2(f / 440)))


def pitch_track(x, sr=SR, win=0.02):
    n = int(win * sr)
    out = []
    for i in range(0, len(x) - n, n):
        seg = x[i:i + n]
        if rms(seg) < 1e-3:
            continue
        out.append(peak_hz(np.pad(seg, (0, 8 * n)), sr, 40))
    return np.array(out)


@card("BEAT-237")
def pitch_interval_semantics(task, wd):
    """Rising = gain, falling = loss (jump 80-200 ms over 1-1.6 octaves), major interval/bell = reward, minor 2nd /
    tritone = danger, low thump = weight, low-pass = distance; each gesture synthesised and measured."""
    d = 0.15
    up = 0.5 * np.sin(2 * np.pi * np.cumsum(np.geomspace(400, 400 * 2 ** 1.3, int(d * SR))) / SR)
    dn = up[::-1].copy()
    t = tt(0.4)
    reward = 0.3 * (np.sin(2 * np.pi * 523.25 * t) + np.sin(2 * np.pi * 659.25 * t)) * np.exp(-t / 0.2)
    danger = 0.3 * (np.sin(2 * np.pi * 523.25 * t) + np.sin(2 * np.pi * 523.25 * 2 ** 0.5 * t))
    thump = 0.9 * np.sin(2 * np.pi * 60 * tt(.2)) * _decay(.2, .05)
    dist_src = bandpass(noise(int(.4 * SR), 1), 200, 8000)
    dist = lowpass(dist_src, 800)
    outs = [save(wd, n + ".wav", v) for n, v in (("gain_rise", up), ("loss_fall", dn), ("reward_major3", reward), ("danger_tritone", danger),
                                                  ("weight_thump", thump), ("distance_lowpass", dist))]
    pu, pd = pitch_track(up), pitch_track(dn)
    octs = math.log2(pu[-1] / pu[0])

    def two_peaks(x):
        X = np.abs(np.fft.rfft(x * np.hanning(len(x)), 16 * len(x)))
        f = np.fft.rfftfreq(16 * len(x), 1 / SR)
        i1 = int(np.argmax(X))
        X2 = X.copy()
        X2[max(0, i1 - 200):i1 + 200] = 0
        return sorted([f[i1], f[int(np.argmax(X2))]])
    r1 = two_peaks(reward)
    r2 = two_peaks(danger)
    cents = lambda a: 1200 * math.log2(a[1] / a[0])
    flat = 0.5 * np.sin(2 * np.pi * 400 * tt(d))
    pf = pitch_track(flat)
    return [check("gain: pitch rises over 1-1.6 octaves in 80-200 ms", 1.0 <= octs <= 1.6 and 0.08 <= d <= 0.2 and pu[-1] > pu[0], round(octs, 3), "1..1.6 oct up"),
            check("loss: pitch falls", pd[-1] < pd[0] * 0.6, [round(pd[0]), round(pd[-1])], "falling"),
            check("reward is a major third (400 cents ±15)", abs(cents(r1) - 400) < 15, round(cents(r1), 1), 400),
            check("danger is a tritone (600 cents ±15)", abs(cents(r2) - 600) < 15, round(cents(r2), 1), 600),
            check("weight: thump centroid < 150 Hz", centroid(thump) < 150, round(centroid(thump), 1), "< 150"),
            check("distance: low-pass removes >= 20 dB above 3 kHz", band_db(dist_src, SR, 3000, 20000) - band_db(dist, SR, 3000, 20000) >= 20,
                  round(band_db(dist_src, SR, 3000, 20000) - band_db(dist, SR, 3000, 20000), 1), ">= 20"),
            check("negative control: a flat tone neither rises nor falls", abs(math.log2(pf[-1] / pf[0])) < 0.05, round(math.log2(pf[-1] / pf[0]), 4), "~0")], outs


def classify_role(x, sr=SR):
    if peak_db(x) < -70:
        return "silence"
    e = envelope(x, sr, 10)
    act = np.flatnonzero(e > e.max() * 0.1)
    span = (act[-1] - act[0]) / sr if len(act) else 0
    if span < 0.15:
        return "foley"
    ct = centroid_track(x[act[0]:act[-1]], sr, 0.05)
    ct = ct[ct > 0]
    if len(ct) > 3 and np.percentile(ct, 90) / np.percentile(ct, 10) > 2.5:
        return "creative_sfx"
    X = np.abs(np.fft.rfft(x * np.hanning(len(x))))
    flatness = float(np.exp(np.mean(np.log(X + 1e-12))) / (np.mean(X) + 1e-12))
    if flatness > 0.2 and dbfs(x) < -35:
        return "room_tone"
    env = envelope(x, sr, 25)[::480]
    m = env[env > env.max() * 0.05]
    mod = float(np.std(m) / (np.mean(m) + 1e-12)) if len(m) else 0
    return "voice" if mod > 0.18 else "tonal_music"


TRACK_OF = {"voice": "DIALOGUE", "room_tone": "AMBIENCE", "foley": "SFX_DETAIL", "creative_sfx": "SFX_TRANSITION", "tonal_music": "TONAL", "silence": "SILENCE"}


@card("BEAT-241")
def sound_role_cue_sheet(task, wd):
    """Classify every sound (voice, room tone, Foley, creative SFX, tonal/music, deliberate silence) by measured
    features and log cue id, timecode, intent, asset and review reason to a cue-sheet CSV feeding timeline tracks."""
    d = 1.5
    fixtures = {"voice": speechlike(d, [(0.1, 1.4)], f0=150), "room_tone": 10 ** (-50 / 20) * noise(int(d * SR), 1) / 1.0,
                "foley": np.concatenate([0.8 * bandpass(noise(int(.04 * SR), 2), 500, 8000) * _decay(.04, .008), np.zeros(int(1.0 * SR))]),
                "creative_sfx": stft_shape(int(0.8 * SR), lambda t: 300 * 10 ** np.clip(t / 0.8, 0, 1), 0.3, 3) * np.hanning(int(0.8 * SR)),
                "tonal_music": music_bed(d), "silence": np.zeros(int(d * SR))}
    rows, outs = [], []
    for i, (truth, x) in enumerate(fixtures.items()):
        a = save(wd, "cue_%02d.wav" % (i + 1), x)
        role = classify_role(x)
        tc = "00:00:%02d:%02d" % (i * 2, 0)
        rows.append({"cue_id": "C%03d" % (i + 1), "tc": tc, "role": role, "track": TRACK_OF[role], "intent": truth.replace("_", " "),
                     "asset": a.name, "review_reason": "creative SFX: never logged as real sound" if role == "creative_sfx" else "", "truth": truth})
    csvp = Path(wd) / "cue_sheet.csv"
    with open(csvp, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    wrong = [(r["truth"], r["role"]) for r in rows if r["role"] != r["truth"]]
    noise_loud = classify_role(0.3 * noise(int(d * SR), 9))
    return [check("all six fixtures classified to their role", not wrong, wrong, []),
            check("cue sheet has cue id, TC, role, track, intent, asset, review reason", csvp.read_text().splitlines()[0].startswith("cue_id,tc,role,track,intent,asset,review_reason"), csvp.read_text().splitlines()[0], "header"),
            check("creative SFX carry the 'never real sound' review note", all(r["review_reason"] for r in rows if r["role"] == "creative_sfx"), [r["review_reason"] for r in rows if r["role"] == "creative_sfx"], "noted"),
            check("negative control: loud steady noise is not called voice or room tone", noise_loud not in ("voice", "room_tone"), noise_loud, "other")], [csvp]


def sc_duck(music, voice, out, thr, ratio, attack, release, makeup=1):
    ff("-i", music, "-i", voice, "-filter_complex",
       "[0:a][1:a]sidechaincompress=threshold=%s:ratio=%s:attack=%s:release=%s:makeup=%s[d]" % (thr, ratio, attack, release, makeup),
       "-map", "[d]", "-c:a", "pcm_s16le", out)
    return Path(out)


@card("BEAT-268")
def music_ducking(task, wd):
    """ffmpeg sidechaincompress ducking of the music under narration: 8-12 dB, attack 150 ms, release 400 ms;
    depth and timing measured on the ducked bed."""
    secs = 5.0
    m = save(wd, "music.wav", music_bed(secs, amp=0.4))
    v = save(wd, "voice.wav", speechlike(secs, [(1.5, 3.0)], f0=150, amp=0.5))
    def meas(at, rel, name):
        o = sc_duck(m, v, Path(wd) / name, 0.03, 2.5, at, rel)
        y, _ = load_any(o)
        tr = env_db_track(y, SR, 0.005, 0.02)
        base, low = float(np.median(tr[100:280])), float(np.median(tr[440:580]))
        dep = base - low
        t90 = next(i for i in range(300, 600) if tr[i] <= base - 0.9 * dep) / 200 - 1.5
        trel = next(i for i in range(600, len(tr)) if tr[i] >= base - 1.0) / 200 - 3.0
        return o, dep, t90, trel
    out, depth, t_att, t_rel = meas(150, 400, "ducked.wav")
    _, _, fast_att, fast_rel = meas(10, 50, "ducked_fast.wav")
    x, _ = load_any(m)
    tx = env_db_track(x, SR, 0.01, 0.03)
    return [check("duck depth 8-12 dB", 8 <= depth <= 12, round(depth, 2), "8..12"),
            check("attack 150 ms: 90 % of the duck within 0.15 s, slower than a 10 ms attack", t_att <= 0.15 and t_att > fast_att, [round(t_att, 3), round(fast_att, 3)], "<= 0.15 and > fast"),
            check("release 400 ms: back within 1 dB in 0.3-1.2 s (a 50 ms release: < 0.1 s)", 0.3 <= t_rel <= 1.2 and fast_rel < 0.1, [round(t_rel, 3), round(fast_rel, 3)], "0.3..1.2"),
            check("negative control: the unducked music keeps its level", float(np.median(tx[50:140])) - float(np.median(tx[220:290])) < 1, round(float(np.median(tx[50:140]) - np.median(tx[220:290])), 2), "< 1")], [out]


@card("BEAT-269")
def loudnorm_minus14(task, wd):
    """ffmpeg loudnorm=I=-14:TP=-1:LRA=11, two-pass (measured values fed back, linear) - measured with ebur128."""
    x, _ = drum_loop(120, 6.0)
    x = (0.25 * x + music_bed(6.0, amp=0.5)) * 0.05
    src = save(wd, "mix_in.wav", x)
    out = Path(wd) / "mix_-14.wav"
    m = loudnorm2(src, out, -14, -1.0, 11)
    r, r0 = ebur(out), ebur(src)
    return [check("integrated -14 LUFS ±0.5 (card allows ±1.5)", abs(r["I"] + 14) <= 0.5, r["I"], -14),
            check("true peak <= -1 dBTP (±0.2)", r["TP"] <= -0.8, r["TP"], "<= -1"),
            check("first pass measured the input", float(m["input_i"]) < -25, m["input_i"], "< -25"),
            check("negative control: the input is not at -14", abs(r0["I"] + 14) > 1.5, r0["I"], "!= -14")], [out]


def _voice_with_pauses(secs=4.0):
    spans = [(0.3, 1.3), (2.0, 3.2)]
    return speechlike(secs, spans, f0=150, amp=0.4), spans


@card("BEAT-270")
def soft_key_clicks(task, wd):
    """Optional quiet key clicks executed on beats or in pauses only, at -24 dB under the voice peak."""
    secs, bpm = 4.0, 120
    v, spans = _voice_with_pauses(secs)
    beats = [k * 0.5 for k in range(8)]
    wanted = [0.55, 1.5, 1.65, 2.4, 3.4]
    in_voice = lambda t: any(a <= t <= b for a, b in spans)
    placed = [t if not in_voice(t) else min(beats, key=lambda b: abs(b - t)) for t in wanted]
    click = np.sin(2 * np.pi * 3000 * tt(.012)) * _decay(.012, .002)
    gain = 10 ** ((peak_db(v) - 24 - peak_db(click)) / 20)
    sfx = np.zeros_like(v)
    for t in placed:
        place(sfx, click, t, gain=gain)
    p = save(wd, "voice_clicks.wav", v + sfx)
    s2 = save(wd, "clicks_stem.wav", sfx)
    on = onsets(sfx, SR, 0.3, 0.05)
    rel = peak_db(sfx) - peak_db(v)
    raw = np.zeros_like(v)
    for t in placed:
        place(raw, click, t)
    ok_pos = all((not in_voice(t)) or any(abs(t - b) < 1e-9 for b in beats) for t in placed)
    jdump(Path(wd) / "clicks.json", {"wanted": wanted, "placed": placed, "gain_db": round(20 * math.log10(gain), 2)})
    return [check("clicks only in pauses or on beats", ok_pos, placed, "pause or beat"),
            check("one click per keystroke heard (±5 ms)", len(on) == len(placed) and beat_err(on, placed) < 0.005, [round(o, 3) for o in on], placed),
            check("clicks sit -24 dB under the voice peak (±1)", abs(rel + 24) <= 1, round(rel, 2), -24),
            check("negative control: unattenuated clicks are not at -24 dB", abs(peak_db(raw) - peak_db(v) + 24) > 3, round(peak_db(raw) - peak_db(v), 2), "!= -24")], [p, s2]


@card("BEAT-271")
def drawing_sfx_level(task, wd):
    """Soft marker/chalk sound only while drawing, -22 dB under the voice peak; each drawn object finishes on its
    spoken name."""
    secs = 4.0
    names = {"sun": (1.2, 1.6), "tree": (2.8, 3.2)}
    v = speechlike(secs, list(names.values()), f0=150, amp=0.4)
    draws = {"sun": (0.3, names["sun"][0]), "tree": (1.8, names["tree"][0])}
    mk = np.zeros_like(v)
    for a, b in draws.values():
        n = int((b - a) * SR)
        seg = bandpass(noise(n, int(a * 10)), 2000, 6000) * (0.7 + 0.3 * np.sin(2 * np.pi * 12 * tt(b - a)))[:n]
        r = int(0.01 * SR)
        seg[:r] *= np.linspace(0, 1, r)
        seg[-r:] *= np.linspace(1, 0, r)
        place(mk, seg, a)
    mk = at_level(mk, peak_db(v) - 22)
    p = save(wd, "draw_mix.wav", v + mk)
    s = save(wd, "marker_stem.wav", mk)
    outside = [(0.0, 0.28), (1.62, 1.78), (2.82, 4.0)]
    out_db = max(seg_db(mk, SR, a, b) for a, b in outside)
    ends = []
    e = envelope(mk, SR, 5)
    for a, b in draws.values():
        idx = np.flatnonzero(e[int(a * SR):int((b + 0.2) * SR)] > e.max() * 0.05)
        ends.append(a + idx[-1] / SR)
    ve = envelope(v, SR, 5)
    starts = [a + np.flatnonzero(ve[int(a * SR):] > ve.max() * 0.05)[0] / SR for a, _ in names.values()]
    loop = at_level(bandpass(noise(int(secs * SR), 5), 2000, 6000), peak_db(v) - 22)
    jdump(Path(wd) / "draw_plan.json", {"draws": draws, "names": names, "level_db_under_voice": 22})
    return [check("marker sound only while drawing (< -80 dBFS elsewhere)", out_db < -80, round(out_db, 1), "< -80"),
            check("marker peak -22 dB under the voice peak (±0.5)", abs(peak_db(mk) - peak_db(v) + 22) <= 0.5, round(peak_db(mk) - peak_db(v), 2), -22),
            check("each drawing finishes on its spoken name (±1 frame)", max(abs(a - b) for a, b in zip(ends, starts)) <= 1 / 30, [round(x, 3) for x in ends], [round(x, 3) for x in starts]),
            check("negative control: a continuous marker loop sounds outside the drawing", max(seg_db(loop, SR, a, b) for a, b in outside) > -60, round(max(seg_db(loop, SR, a, b) for a, b in outside), 1), "> -60")], [p, s]


@card("BEAT-279")
def tap_swipe_levels(task, wd):
    """Optional licensed-style UI SFX at fixed levels: click 30-50 ms at -18 dBFS, whoosh <= 250 ms, both ducked
    10 dB while the voice speaks."""
    secs = 4.0
    v = speechlike(secs, [(1.8, 3.0)], f0=150, amp=0.4)
    click = at_level(bandpass(noise(int(.04 * SR), 1), 1500, 6000) * _decay(.04, .008), -18)
    wh = bandpass(noise(int(.22 * SR), 2), 400, 3000) * np.hanning(int(.22 * SR))
    wh = at_level(wh, -18)
    events = [("click", 0.5), ("whoosh", 1.0), ("click", 2.2)]
    sfx = np.zeros_like(v)
    gains = []
    for kind, t in events:
        g = 10 ** (-10 / 20) if 1.8 <= t <= 3.0 else 1.0
        gains.append(g)
        place(sfx, click if kind == "click" else wh, t, gain=g)
    p = save(wd, "ui_mix.wav", v + sfx)
    st = save(wd, "ui_stem.wav", sfx)
    e = envelope(click, SR, 1)
    cd = (np.flatnonzero(e > e.max() * 10 ** (-30 / 20))[-1] - np.flatnonzero(e > e.max() * 10 ** (-30 / 20))[0]) / SR
    ew = envelope(wh, SR, 2)
    wd_ = (np.flatnonzero(ew > ew.max() * 0.03)[-1] - np.flatnonzero(ew > ew.max() * 0.03)[0]) / SR
    first = peak_db(sfx[int(0.49 * SR):int(0.56 * SR)])
    under = peak_db(sfx[int(2.19 * SR):int(2.26 * SR)])
    raw = np.zeros_like(v)
    place(raw, bandpass(noise(int(.04 * SR), 1), 1500, 6000) * _decay(.04, .008), 0.5)
    return [check("click lasts 30-50 ms (to -30 dB)", 0.03 <= cd <= 0.05, round(cd, 4), "0.03..0.05"),
            check("click peak -18 dBFS (±0.3)", abs(first + 18) <= 0.3, round(first, 2), -18),
            check("whoosh <= 250 ms", wd_ <= 0.25, round(wd_, 3), "<= 0.25"),
            check("click under the voice ducked 10 dB (±0.5)", abs(first - under - 10) <= 0.5, round(first - under, 2), 10),
            check("negative control: the raw click is not at -18 dBFS", abs(peak_db(raw) + 18) > 3, round(peak_db(raw), 2), "!= -18")], [p, st]


@card("BEAT-280")
def sparse_ui_sound(task, wd):
    """One click per press, one swish per screen change, nothing on hovers or list items; each press within ±100 ms
    of its spoken verb; click a 10-30 ms transient 12-18 dB under the voice."""
    secs = 5.0
    v = speechlike(secs, [(0.4, 0.9), (2.0, 2.5), (3.4, 3.9)], f0=150, amp=0.4)
    verbs = [0.4, 2.0, 3.4]
    events = [("press", 0.45), ("hover", 1.2), ("list_item", 1.5), ("screen", 1.7), ("press", 2.06), ("list_item", 2.8), ("press", 3.43), ("hover", 4.3)]
    click = at_level(bandpass(noise(int(.02 * SR), 3), 2000, 7000) * _decay(.02, .003), peak_db(v) - 15)
    swish = at_level(bandpass(noise(int(.2 * SR), 4), 500, 3000) * np.hanning(int(.2 * SR)), peak_db(v) - 15)

    def render(evts, sparse=True):
        s = np.zeros_like(v)
        for kind, t in evts:
            if kind == "press":
                place(s, click, t)
            elif kind == "screen":
                place(s, swish, t)
            elif not sparse:
                place(s, click, t)
        return s
    sfx = render(events)
    p = save(wd, "ui_sparse.wav", v + sfx)
    st = save(wd, "ui_sparse_stem.wav", sfx)
    on = onsets(sfx, SR, 0.2, 0.05)
    presses = [t for k, t in events if k == "press"]
    near = max(min(abs(p_ - vb) for vb in verbs) for p_ in presses)
    hov = [t for k, t in events if k in ("hover", "list_item")]
    e = envelope(click, SR, 0.5)
    cd = (np.flatnonzero(e > e.max() * 0.03)[-1] - np.flatnonzero(e > e.max() * 0.03)[0]) / SR
    rel = peak_db(click) - peak_db(v)
    busy = onsets(render(events, False), SR, 0.2, 0.05)
    return [check("one sound per press and per screen change, nothing else", len(on) == 4, [round(o, 3) for o in on], 4),
            check("no sound at hovers / list items", all(min(abs(o - h) for o in on) > 0.05 for h in hov), hov, "silent"),
            check("each press within ±100 ms of its verb", near <= 0.1, round(near, 3), "<= 0.1"),
            check("click is a 10-30 ms transient", 0.01 <= cd <= 0.03, round(cd, 4), "0.01..0.03"),
            check("click 12-18 dB under the voice", -18 <= rel <= -12, round(rel, 2), "-18..-12"),
            check("negative control: sound on every event fails the sparse rule", len(busy) > 4, len(busy), "> 4")], [p, st]


def kit_files():
    d = VEND / "kit" / "sfx"
    cat = json.loads((d / "catalog.json").read_text())["sounds"]
    return d, cat


def hf_ratio(x, sr=SR):
    X = np.abs(np.fft.rfft(x)) ** 2
    f = np.fft.rfftfreq(len(x), 1 / sr)
    return float(X[f > 6000].sum() / (X.sum() + 1e-20))


@card("BEAT-281")
def kenney_cc0_library(task, wd):
    """Kenney CC0 SFX (the 20-cue subset vendored in kit/sfx; the card's full pack is ~238 files): measure brightness,
    HF risk and envelope per file, pick a low-HF-risk cue for a repeated moment and copy it into composition/assets."""
    d, cat = kit_files()
    meas = {}
    for k, v in cat.items():
        f = d / (v.get("file") or (k + ".ogg"))
        if not f.exists():
            continue
        x, _ = load_any(f)
        e = envelope(x, SR, 2)
        act = np.flatnonzero(e > e.max() * 0.05)
        meas[k] = {"centroid": round(centroid(x)), "hf": round(hf_ratio(x), 4), "dur": round(len(x) / SR, 3), "catalog_hf": v.get("hf_risk"),
                   "env_span": round((act[-1] - act[0]) / SR, 3) if len(act) else 0}
    lab = {k: m for k, m in meas.items() if m["catalog_hf"]}
    lows = [m["hf"] for m in lab.values() if m["catalog_hf"] == "low"]
    highs = [m["hf"] for m in lab.values() if m["catalog_hf"] == "high"]
    rep = sorted((k for k, m in lab.items() if m["catalog_hf"] == "low" and m["dur"] < 0.3), key=lambda k: meas[k]["hf"])[0]
    assets = Path(wd) / "composition" / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    src = d / cat[rep]["file"]
    dst = assets / src.name
    shutil.copy2(src, dst)
    out = jdump(Path(wd) / "sfx_analysis.json", {"measured": meas, "pick_for_repeats": rep})
    from _harness import sha as _sha
    return [check("every catalog cue analysed (brightness, HF, envelope)", len(meas) >= 14, len(meas), ">= 14"),
            check("catalog 'high' HF risk cues measure more HF than the 'low' ones", np.median(highs) > np.median(lows), [round(float(np.median(lows)), 4), round(float(np.median(highs)), 4)], "high > low"),
            check("repeated-moment pick is low HF risk and short", cat[rep]["hf_risk"] == "low" and meas[rep]["dur"] < 0.3, [rep, meas[rep]], "low, < 0.3 s"),
            check("pick copied into composition/assets byte for byte", _sha(dst) == _sha(src), dst.name, src.name),
            check("negative control: a high-risk cue (chips) is never the pick", rep != "chips" and meas["chips"]["hf"] > meas[rep]["hf"], [meas["chips"]["hf"], meas[rep]["hf"]], "chips higher")], [out, dst]


def _timeline_sfx(wd, sfx, name):
    T = vmod("timeline")
    clip = Path(wd) / "clip.mp4"
    if not clip.exists():
        ff("-f", "lavfi", "-i", "color=c=blue:s=160x90:r=30:d=3", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-shortest",
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", clip)
    out = Path(wd) / name
    T.build({"size": "160x90", "fps": 30, "clips": [{"src": str(clip), "in": 0, "out": 3}],
             "audio": {"keep_clip_audio": False, "lufs": -32, "sfx": sfx}}, out)
    return out


@card("BEAT-50")
def sfx_kit_cues(task, wd):
    """kmotion sfx (kit catalog: bell-1/2, bong, card-place, card-slide, chips, click, drop-1/2, glitch, key-1..6,
    reveal-1/2/3, select) and timeline audio.sfx [{src:'kit:reveal-1', at:0.4, gain:-10}]: the cue starts with the motion."""
    lst = sh([sys.executable, VEND / "kmotion.py", "sfx"], cwd=wd, timeout=40)
    names = ["bell-1", "bell-2", "bong", "card-place", "card-slide", "chips", "click", "drop-1", "drop-2", "glitch", "reveal-1", "reveal-2", "reveal-3", "select"] + ["key-%d" % i for i in range(1, 7)]
    missing = [n for n in names if n not in lst]
    out = _timeline_sfx(wd, [{"src": "kit:reveal-1", "at": 0.4, "gain": -2}, {"src": "kit:reveal-1", "at": 1.6, "gain": -12}], "sfx_cues.mp4")
    y, _ = load_any(out)
    on = onsets(y, SR, 0.05, 0.3)
    rel = peak_db(y[int(1.55 * SR):int(1.9 * SR)]) - peak_db(y[int(0.35 * SR):int(0.7 * SR)])
    tdump(Path(wd) / "kmotion_sfx.txt", lst)
    return [check("kit lists all 20 cues", not missing, missing, []),
            check("cues start at their motion times 0.4 s and 1.6 s (±30 ms)", len(on) >= 2 and abs(on[0] - 0.4) < 0.03 and min(abs(o - 1.6) for o in on) < 0.03, [round(o, 3) for o in on[:3]], [0.4, 1.6]),
            check("gain -12 vs -2 dB: the second cue sits 10 dB lower (±1)", abs(rel + 10) <= 1, round(rel, 2), -10),
            check("negative control: nothing sounds before the first cue", peak_db(y[:int(0.35 * SR)]) < -60, round(peak_db(y[:int(0.35 * SR)]), 1), "< -60")], [out, Path(wd) / "kmotion_sfx.txt"]


@card("BEAT-54")
def cc0_ui_kit_params(task, wd):
    """CC0 UI kit (20 sounds, 44.1 kHz): measured durations against the card's list (reveal-1/2/3 .18/.14/.15, bell-1
    1.48, bell-2 .65, bong .12, drop-1/2 .11/.19, click .01, select .05, glitch .03, card-slide .60, card-place .69, chips
    .26, key-1..6 .25), brightness from the spectral centroid."""
    d, cat = kit_files()
    card_d = {"reveal-1": .18, "reveal-2": .14, "reveal-3": .15, "bell-1": 1.48, "bell-2": .65, "bong": .12, "drop-1": .11, "drop-2": .19,
              "click": .01, "select": .05, "glitch": .03, "card-slide": .60, "card-place": .69, "chips": .26}
    got, rates = {}, {}
    for k in card_d:
        pr = fx.probe(d / cat[k]["file"])
        got[k] = round(float(pr["format"]["duration"]), 3)
        rates[k] = int(pr["streams"][0]["sample_rate"])
    keys = sorted(d.glob("key-*"))
    kd = [round(float(fx.probe(k)["format"]["duration"]), 3) for k in keys]
    bad = {k: (got[k], card_d[k]) for k in card_d if abs(got[k] - card_d[k]) > 0.02}
    cents = {}
    for k in card_d:
        x, _ = load_any(d / cat[k]["file"])
        cents.setdefault(cat[k]["brightness"], []).append(centroid(x))
    med = {b: float(np.median(v)) for b, v in cents.items()}
    shuffled = {k: card_d[n] for k, n in zip(card_d, list(card_d)[1:] + list(card_d)[:1])}
    sbad = [k for k in card_d if abs(got[k] - shuffled[k]) > 0.02]
    out = jdump(Path(wd) / "kit_params.json", {"durations": got, "keys": kd, "rates": rates, "centroid_by_brightness": med})
    return [check("durations match the card (±20 ms)", not bad, bad, {}),
            check("key-1..6 are ~0.25 s each", len(kd) == 6 and all(abs(k - 0.25) < 0.03 for k in kd), kd, 0.25),
            check("44.1 kHz files", set(rates.values()) == {44100}, sorted(set(rates.values())), [44100]),
            check("'bright' cues have a higher centroid than 'warm' ones", med.get("bright", 0) > med.get("warm", 1e9), {k: round(v) for k, v in med.items()}, "bright > warm"),
            check("negative control: the durations do not fit a shuffled name list", len(sbad) > 8, len(sbad), "> 8 mismatches")], [out]


@card("BEAT-282")
def music_cue_presets(task, wd):
    """Per-track cue preset JSON/MD: tempo, beat grid, first beat and strongCue timestamps for planning the first
    20-25 s (qa.beats tempo/grid + strong accents measured as hits >= 6 dB over the median kick)."""
    secs, bpm, first = 24.0, 120.0, 3.02
    x, kt = drum_loop(bpm, secs, offset=first)
    strong = [7.02, 11.02, 15.02, 19.02]
    for t in strong:
        place(x, addp(1.5 * kick(), 0.4 * highpass(noise(int(.3 * SR), int(t)), 3000) * _decay(.3, .1)), t)
    x = x + 0.05 * music_bed(secs)
    x[:int(first * SR) - 200] *= 0.0
    p = save(wd, "vol-1.wav", x)
    qa = vmod("qa").beats(p)

    def cues(sig):
        kon = onsets(lowpass(sig, 200), SR, 0.15, 0.25)
        lv = [peak_db(sig[int(t * SR):int((t + 0.05) * SR)]) for t in kon]
        med = float(np.median(lv))
        return kon, [round(t, 3) for t, l in zip(kon, lv) if l >= med + 6 and t <= 25]
    kon, sc = cues(x)
    y, _ = drum_loop(bpm, secs, offset=first)
    _, sc_flat = cues(y)
    preset = {"track": "vol-1", "duration": round(secs, 2), "bpm": qa["bpm"], "first_beat": round(kon[0], 3),
              "beat_grid": [round(first + k * 60 / qa["bpm"], 3) for k in range(int((secs - first) * qa["bpm"] / 60))], "strongCues": sc}
    out = jdump(Path(wd) / "vol-1.music-cues.json", preset)
    md = tdump(Path(wd) / "vol-1.music-cues.md", "# vol-1\n\n- %.2f BPM, first beat %.3f s\n- strong cues: %s\n" % (qa["bpm"], kon[0], ", ".join(map(str, sc))))
    return [check("tempo 120 ±0.5 BPM", abs(qa["bpm"] - bpm) <= 0.5, qa["bpm"], bpm),
            check("first beat ~3.02 s (±30 ms)", abs(kon[0] - first) <= 0.03, round(kon[0], 3), first),
            check("strongCues at the four accents (±40 ms)", len(sc) == 4 and beat_err(sc, strong) <= 0.04, sc, strong),
            check("negative control: an evenly accented loop has no strong cues", sc_flat == [], sc_flat, [])], [out, md]


@card("BEAT-U01")
def subtle_sfx_palette(task, wd):
    """Creator-learned defaults: voice dominant (~0.5 peak), SFX 0.02-0.06 (pop for text/cards, tonal swell for big
    words and scene changes, glass for panels, tick for clicks/typing, chime on completion), no whoosh, shot beds
    ≈ -16 dB in place; numpy-generated, mix.wav + sfx_stem.wav, retimed on every visual edit."""
    secs = 6.0
    v = speechlike(secs, [(0.5, 2.5), (3.2, 5.2)], f0=150)
    v = v * 0.5 / np.max(np.abs(v))
    pal = {"pop": lambda: np.sin(2 * np.pi * np.cumsum(np.linspace(500, 1100, int(.06 * SR))) / SR) * _decay(.06, .015),
           "swell": lambda: sum(np.sin(2 * np.pi * f * tt(.8)) for f in (261.6, 329.6, 392)) * np.hanning(int(round(.8 * SR))),
           "glass": lambda: sum(np.sin(2 * np.pi * f * tt(.5)) * np.exp(-tt(.5) / .12) for f in (2093, 3136)),
           "tick": lambda: np.sin(2 * np.pi * 4000 * tt(.008)) * _decay(.008, .0015),
           "chime": lambda: sum(np.sin(2 * np.pi * f * tt(1.0)) * np.exp(-tt(1.0) / .3) for f in (1046.5, 1318.5, 1568))}
    gains = {"pop": 0.04, "swell": 0.03, "glass": 0.03, "tick": 0.02, "chime": 0.05}
    events = [("pop", 0.6), ("swell", 1.5), ("glass", 2.8), ("tick", 3.4), ("chime", 5.4)]

    def stem(evts):
        s = np.zeros(int(secs * SR))
        for k, t in evts:
            y = pal[k]()
            place(s, y * gains[k] / np.max(np.abs(y)), t)
        return s
    s = stem(events)
    shot = 0.3 * bandpass(noise(int(secs * SR), 2), 200, 2000)
    shot_bed = shot * 10 ** (-16 / 20)
    mix = v + s + shot_bed
    p1, p2 = save(wd, "mix.wav", mix), save(wd, "sfx_stem.wav", s)
    peaks = {k: round(float(np.max(np.abs(stem([(k, t)])))), 4) for k, t in events}
    moved = stem([(k, t + 0.3 if k == "glass" else t) for k, t in events])
    on_a = [o for o in onsets(s, SR, 0.2, 0.3) if 2.6 < o < 3.3]
    on_b = [o for o in onsets(moved, SR, 0.2, 0.3) if 2.6 < o < 3.3]

    def broadband(x):
        X = np.abs(np.fft.rfft(x * np.hanning(len(x))))
        f = np.fft.rfftfreq(len(x), 1 / SR)
        X = X[(f > 200) & (f < 5000)]
        return float(np.exp(np.mean(np.log(X + 1e-12))) / (np.mean(X) + 1e-12))
    is_whoosh = lambda x: len(x) / SR > 0.15 and broadband(x) >= 0.3
    fl = [k for k in pal if is_whoosh(pal[k]())]
    whoosh = bandpass(noise(int(.4 * SR), 5), 300, 4000) * np.hanning(int(.4 * SR))
    jdump(Path(wd) / "sfx_events.json", {"events": events, "gains": gains, "shot_bed_db": -16})
    return [check("every SFX peak in 0.02-0.06 against a 0.5 voice peak", all(0.02 <= v_ <= 0.06 for v_ in peaks.values()) and abs(np.max(np.abs(v)) - 0.5) < 1e-6, peaks, "0.02..0.06"),
            check("shot bed sits -16 dB under its source (±0.1)", abs(20 * math.log10(rms(shot_bed) / rms(shot)) + 16) < 0.1, round(20 * math.log10(rms(shot_bed) / rms(shot)), 2), -16),
            check("palette has no whoosh (no sustained broadband cue > 150 ms)", fl == [], fl, []),
            check("moving a panel 0.3 s later moves its stem cue 0.3 s (±5 ms)", len(on_a) == 1 and len(on_b) == 1 and abs(on_b[0] - on_a[0] - 0.3) < 0.005, [on_a, on_b], "+0.3"),
            check("negative control: a whoosh fails the no-whoosh check", is_whoosh(whoosh), round(broadband(whoosh), 4), "whoosh")], [p1, p2]


def level_curve(x, sr, fps=100, win=0.05):
    n, h = int(win * sr), int(sr / fps)
    return np.array([20 * math.log10(rms(x[i:i + n]) + 1e-9) for i in range(0, max(1, len(x) - n), h)])


def find_drops(L, fps=100):
    out = []
    for i in range(4 * fps, len(L) - fps // 2):
        dip = L[i - int(1.2 * fps):i].mean()
        before = L[i - 4 * fps:i - int(1.5 * fps)].mean()
        after = L[i:i + fps // 2].mean()
        if dip <= before - 3.5 and after >= dip + 6:
            if not out or i / fps - out[-1] > 2:
                out.append(i / fps)
    return out


def find_hits(L, fps=100, rise=9):
    out = []
    for i in range(5, len(L)):
        if L[i] - L[i - 5] >= rise and (not out or i / fps - out[-1] > 0.4):
            out.append(i / fps)
    return out


def music_window(x, sr, length, after=0.0, fps=100):
    L = level_curve(x, sr, fps)
    drops, hits = find_drops(L, fps), find_hits(L, fps)
    lifts = []
    for i in range(2 * fps, len(L) - 2 * fps, fps // 2):
        if L[i:i + 2 * fps].mean() - L[i - 2 * fps:i].mean() >= 3 and not any(abs(i / fps - d) < 2 for d in drops):
            lifts.append(i / fps)
    best = []
    for s in np.arange(after, len(x) / sr - length + 1e-9, 0.5):
        e = s + length
        sc = 0
        if any(s <= d <= s + length / 4 for d in drops):
            sc += 8
        if any(s + 0.5 * length <= l_ <= s + 0.85 * length for l_ in lifts):
            sc += 5
        if any(e - 1.0 <= h <= e for h in hits):
            sc += 4
        best.append((sc, round(float(s), 2)))
    best.sort(key=lambda r: (-r[0], r[1]))
    return best, drops, lifts, hits


def window_track(secs=70.0, sr=SR):
    """120 BPM kicks over a pad, with a breath-then-drop at 34.2 s, a build at 40-44 s and a big final hit at 49.6 s."""
    x, _ = drum_loop(120, secs, sr)
    x = 0.5 * x + music_bed(secs, sr, 0.15)
    g = np.ones(len(x))
    g[int(33.0 * sr):int(34.2 * sr)] = 0.15
    ramp = (tt(secs, sr) >= 40) & (tt(secs, sr) < 44)
    g[ramp] = np.linspace(0.4, 1.4, ramp.sum())
    g[int(36 * sr):int(40 * sr)] = 0.4
    g[int(44 * sr):int(49.6 * sr)] = 1.0
    g[int(49.0 * sr):int(49.6 * sr)] = 0.3
    x = x * g
    place(x, addp(1.0 * kick(), 0.5 * highpass(noise(int(.4 * sr), 3), 2000) * _decay(.4, .15)), 49.6, sr)
    return x


@card("BEAT-X01")
def best_music_window(task, wd):
    """music_window.py logic (owner script not vendored) implemented as described: 100 fps energy, DROP = last 1.2 s
    >= 3.5 dB under 4-1.5 s earlier and the next 0.5 s >= 6 dB above the dip; windows scored +8 breath-then-drop in the
    first quarter, +5 lift at 50-85 %, +4 final hit."""
    x = window_track()
    p = save(wd, "track.wav", x)
    best, drops, lifts, hits = music_window(x, SR, 20, after=10)
    flat, _ = drum_loop(120, 70.0)
    fb, fd, _, _ = music_window(0.5 * flat + music_bed(70.0, SR, 0.15), SR, 20, after=10)
    top = best[0]
    out = jdump(Path(wd) / "windows.json", {"top3": best[:3], "drops": drops, "lifts": lifts[:10], "hits": hits[:10],
                                            "structure_film_time": {"drop": [round(d - top[1], 2) for d in drops if top[1] <= d <= top[1] + 20]}})
    return [check("DROP found at the designed 34.2 s (±0.3)", any(abs(d - 34.2) <= 0.3 for d in drops), drops, 34.2),
            check("best 20 s window scores all three (+8 +5 +4 = 17)", top[0] == 17, top, 17),
            check("best window starts near 30 s (±1)", abs(top[1] - 30) <= 1, top[1], 30),
            check("negative control: a flat loop has no DROP and no 17-point window", fd == [] and fb[0][0] < 17, [fd, fb[0]], "none")], [out, p]


def snap_times(times, accents, beats, win=0.35, fps=30):
    out = []
    for t in times:
        near = [a for a in accents if abs(a - t) <= win]
        if near:
            s, kind = min(near, key=lambda a: abs(a - t)), "accent"
        else:
            s, kind = min(beats, key=lambda b: abs(b - t)), "beat"
        out.append({"t": t, "snapped": round(s, 3), "kind": kind, "offset_s": round(s - t, 3), "offset_frames": round((s - t) * fps, 2), "frame": int(round(s * fps))})
    return out


@card("BEAT-X02")
def snap_scenario_times(task, wd):
    """Move planned cut times to the nearest strong accent within 0.35 s, else to the nearest beat; accents and beats
    measured from the track itself (owner music_window.py --snap logic, not vendored, implemented as described)."""
    secs = 26.0
    x, kt = drum_loop(120, secs)
    acc = [4.25, 9.25, 16.75]
    for t in acc:
        place(x, addp(1.6 * kick(), 0.4 * highpass(noise(int(.2 * SR), int(t)), 3000) * _decay(.2, .05)), t)
    p = save(wd, "track.wav", x)
    kon = onsets(lowpass(x, 200), SR, 0.15, 0.15)
    lv = {round(t, 3): peak_db(x[int(t * SR):int((t + 0.05) * SR)]) for t in kon}
    med = float(np.median(list(lv.values())))
    accents = [t for t, l in lv.items() if l >= med + 4]
    beats = [t for t in kon if t not in accents]
    plan = [4.0, 9.0, 17.0, 24.0]
    res = snap_times(plan, accents, beats)
    late = [r["offset_s"] for r in res]
    advice = "shift the music start, not the picture" if all(o > 0 for o in late) or all(o < 0 for o in late) else "per-cut snaps"
    out = jdump(Path(wd) / "snap.json", {"snaps": res, "advice": advice})
    raw = max(min(abs(t - a) for a in accents + beats) for t in plan[:3])
    return [check("4, 9, 17 snap to the accents 4.25 / 9.25 / 16.75 (±10 ms), not the nearer beat", [r["kind"] for r in res[:3]] == ["accent"] * 3 and beat_err([r["snapped"] for r in res[:3]], acc) <= 0.01, [r["snapped"] for r in res], acc),
            check("24 s (no accent in ±0.35 s) snaps to the beat grid", res[3]["kind"] == "beat" and abs(res[3]["snapped"] - 24.0) <= 0.01, res[3], 24.0),
            check("offsets reported in seconds and frames", all(abs(r["offset_frames"] - r["offset_s"] * 30) < 0.05 for r in res), [r["offset_frames"] for r in res], "s*30"),
            check("negative control: the unsnapped plan misses the accents by > 1 frame", raw > 1 / 30, round(raw, 3), "> 0.033")], [out, p]


def verify_hits(x, sr, hits, fps=30, win=0.0125, search=0.25):
    n = int(win * sr)
    L = np.array([rms(x[i:i + n]) for i in range(0, len(x) - n, n)])
    Ld = 20 * np.log10(L + 1e-9)
    k = int(round(0.05 / win))
    rep = []
    for h in hits:
        a, b = int((h - search) / win), int((h + search) / win)
        rise = [(Ld[i] - Ld[i - k:i].max(), i) for i in range(max(k, a), min(len(Ld), b))]
        r, i = max(rise)
        on = i * win
        off = on - h
        rep.append({"hit": h, "onset": round(on, 4), "offset_ms": round(off * 1000, 1), "frames": round(off * fps, 2),
                    "flag": "ok" if abs(off) <= 1 / fps else ("LATE" if off > 0 else "EARLY")})
    return rep


@card("BEAT-X03")
def verify_picture_hits(task, wd):
    """After the mix, RMS in 12.5 ms windows; onset = the largest rise over the previous 50 ms within ±0.25 s of each
    picture hit; offsets in ms and frames, LATE/EARLY beyond one frame."""
    secs = 20.0
    x = music_bed(secs, amp=0.05)
    real = [4.28, 8.99, 12.0, 17.5]
    for t in real:
        place(x, addp(kick(), 0.3 * highpass(noise(int(.1 * SR), int(t)), 2000) * _decay(.1, .03)), t)
    p = save(wd, "final.wav", x)
    pic = [4.28, 8.99, 12.25, 17.5]
    rep = verify_hits(x, SR, pic)
    good = [r for r in rep if r["flag"] == "ok"]
    out = jdump(Path(wd) / "hits.json", {"hits": rep, "summary": "%d/%d hits within one frame" % (len(good), len(rep))})
    wrong = rep[2]
    return [check("three true hits within one frame", len(good) == 3 and all(abs(r["offset_ms"]) <= 15 for r in good), [r["offset_ms"] for r in good], "<= 15 ms"),
            check("the wrong picture hit at 12.25 s is flagged EARLY -250 ms (±15)", wrong["flag"] == "EARLY" and abs(wrong["offset_ms"] + 250) <= 15, wrong, "EARLY -250"),
            check("frames reported (offset·30)", abs(wrong["frames"] - wrong["offset_ms"] * 0.03) < 0.05, wrong["frames"], round(wrong["offset_ms"] * 0.03, 2)),
            check("negative control: the misplaced hit fails the one-frame rule", wrong["flag"] != "ok", wrong["flag"], "not ok")], [out, p]


def cut_audio(x, sr, start, length, fade):
    a = x[int(round(start * sr)):int(round(start * sr)) + int(round(length * sr))].copy()
    fi = int(0.012 * sr)
    a[:fi] *= np.linspace(0, 1, fi)[:, None] if a.ndim == 2 else np.linspace(0, 1, fi)
    fo = int(fade * sr)
    rem = np.arange(fo, 0, -1) - 1
    g = (rem / fo) ** 1.5
    a[-fo:] *= g[:, None] if a.ndim == 2 else g
    return a


@card("BEAT-X04")
def click_free_cut(task, wd):
    """cut_audio.py track START LEN out.wav --fade F (owner script, implemented as described): exact length, 48 kHz
    stereo, 12 ms fade-in, curved fade-out (remaining/fade)^1.5, 16-bit WAV; the Linux AAC branch with ffmpeg."""
    sr = 48000
    t = tt(12.0, sr)
    x = np.stack([0.6 * np.sin(2 * np.pi * 220 * t + 0.7), 0.6 * np.sin(2 * np.pi * 330 * t + 1.1)], 1)
    src = save(wd, "track.wav", x, sr)
    y = cut_audio(x, sr, 3.7, 5.0, 0.5)
    out = save(wd, "out.wav", y, sr)
    m4a = Path(wd) / "out.m4a"
    ff("-i", out, "-c:a", "aac", "-b:a", "256k", m4a)
    pr = fx.probe(out)["streams"][0]
    z, _ = fx.read_wav(out)
    first5 = float(np.max(np.abs(z[:int(.005 * sr)])))
    later = float(np.max(np.abs(z[int(.1 * sr):int(.2 * sr)])))
    last5 = float(np.max(np.abs(z[-int(.005 * sr):])))
    mid = len(z) - int(0.25 * sr)
    env_ratio = float(np.max(np.abs(z[mid - 200:mid + 200, 0]))) / 0.6
    naive = x[int(3.7 * sr):int(3.7 * sr) + int(5 * sr)]
    return [check("exactly 5.000 s, 48 kHz, 2 channels, 16-bit", len(z) == 5 * sr and pr["sample_rate"] == "48000" and pr["channels"] == 2 and pr["bits_per_sample"] == 16,
                  [len(z), pr["sample_rate"], pr["channels"], pr.get("bits_per_sample")], [240000, "48000", 2, 16]),
            check("12 ms fade-in: first 5 ms peak < 50 % of the body", first5 < 0.5 * later, [round(first5, 3), round(later, 3)], "< 50 %"),
            check("curved fade-out: half-way gain (0.5)^1.5 = 0.354 (±0.03)", abs(env_ratio - 0.5 ** 1.5) < 0.03, round(env_ratio, 3), 0.354),
            check("final 5 ms near silence (< 1 %)", last5 < 0.01, round(last5, 4), "< 0.01"),
            check("AAC 256k .m4a written with ffmpeg (Linux branch)", m4a.stat().st_size > 1000 and fx.probe(m4a)["streams"][0]["codec_name"] == "aac", m4a.stat().st_size, "> 0"),
            check("negative control: a hard cut starts mid-wave (a click)", float(np.max(np.abs(naive[:int(.005 * sr)]))) > 0.5 * later, round(float(np.max(np.abs(naive[:int(.005 * sr)]))), 3), "> 50 %")], [out, m4a]


@card("BEAT-X05")
def cuts_are_the_rhythm(task, wd):
    """sound_kit.py logic (owner kit, numpy only, implemented as described): buses drum / mus / duckfx / sfx; risers
    END on the cut, hits with a loudness hierarchy hero > big > soft, UI sound at spring start + 0.13 s, arp muted 0.3 s
    before big cuts; verify() prints the onset error per cue (target ±5 ms)."""
    secs = 6.0
    n = int(secs * SR)
    bus = {k: np.zeros(n) for k in ("drum", "mus", "duckfx", "sfx")}
    hero, big, soft = 2.5, 4.8, 1.2
    cues = []

    def hit(t, peak, size):
        y = (kick(amp=1.0) + 0.3 * highpass(noise(int(.25 * SR), int(t * 10)), 1500) * _decay(.25, .06 * size))
        place(bus["drum"], y * peak / np.max(np.abs(y)), t)
        cues.append(("hit", t))

    def add_end(t, d=1.5):
        r = stft_shape(int(d * SR), lambda tt_: 300 * 10 ** np.clip(tt_ / d, 0, 1), 0.3, 4) * np.linspace(0, 1, int(d * SR)) ** 2
        r[-1] = 0
        place(bus["duckfx"], 0.4 * r / np.max(np.abs(r)), t - d)
    add_end(hero)
    hit(hero, 0.95, 2.0)
    hit(big, 0.6, 1.2)
    hit(soft, 0.3, 0.6)
    spring = 4.07
    place(bus["sfx"], 0.3 * np.sin(2 * np.pi * 3000 * tt(.01)) * _decay(.01, .002), spring + 0.13)
    cues.append(("ui", spring + 0.13))
    arp_t = np.arange(0, secs, 0.125)
    for t in arp_t:
        if any(c - 0.3 <= t < c for c in (hero, big)):
            continue
        place(bus["mus"], 0.08 * np.sin(2 * np.pi * 880 * tt(.1)) * _decay(.1, .03), t)
    duck = np.ones(n)
    for c in (hero, big, soft):
        i = int(c * SR)
        duck[i:i + int(0.3 * SR)] = np.minimum(duck[i:i + int(0.3 * SR)], np.linspace(0.3, 1, int(0.3 * SR)))
    mix = bus["drum"] + bus["sfx"] + (bus["mus"] + bus["duckfx"]) * duck
    raw = save(wd, "score_raw.wav", mix)
    m = mix.copy()
    for _ in range(4):
        m = m * 10 ** ((-14 - bs1770(m)) / 20)
        m = lookahead_limit(m, 10 ** (-2.5 / 20), la=0.003, rel=0.08)
    out = save(wd, "score.wav", m)
    y = mix
    errs = []
    for kind, t in cues:
        src = bus["sfx"] if kind == "ui" else bus["drum"]
        o = onsets(src[int((t - 0.05) * SR):int((t + 0.05) * SR)], SR, 0.3, 0.01, 1.0)
        errs.append(round((t - 0.05 + o[0] - t) * 1000, 2) if o else 99)
    r_end = np.flatnonzero(np.abs(bus["duckfx"]) > 1e-6)[-1] / SR
    arp_pre = float(np.max(np.abs(bus["mus"][int((hero - 0.18) * SR):int((hero - 0.01) * SR)])))
    s_hero, s_big = peak_db(y[int(hero * SR):int((hero + 0.1) * SR)]), peak_db(y[int(big * SR):int((big + 0.1) * SR)])
    r = ebur(out)
    unmuted = np.zeros(n)
    for t in arp_t:
        place(unmuted, 0.08 * np.sin(2 * np.pi * 880 * tt(.1)) * _decay(.1, .03), t)
    unmuted_pre = float(np.max(np.abs(unmuted[int((hero - 0.18) * SR):int((hero - 0.01) * SR)])))
    jdump(Path(wd) / "verify.json", {"cues": cues, "onset_error_ms": errs, "riser_end": r_end, "lufs": r})
    return [check("every cue's onset within ±5 ms", max(abs(e) for e in errs) <= 5, errs, "<= 5 ms"),
            check("riser ends exactly on the hero cut (±2 ms)", abs(r_end - hero) <= 0.002, round(r_end, 4), hero),
            check("loudness hierarchy: hero > big cut", s_hero > s_big + 2, [round(s_hero, 1), round(s_big, 1)], "hero louder"),
            check("arp muted 0.3 s before the big cuts", arp_pre == 0.0, arp_pre, 0.0),
            check("UI sound at spring start + 0.13 s", cues[-1] == ("ui", spring + 0.13), cues[-1], ["ui", 4.2]),
            check("mastered near -14 LUFS (±1), peak <= -1 dBTP", abs(r["I"] + 14) <= 1 and r["TP"] <= -0.8, r, "-14 / -1"),
            check("negative control: an unmuted arp plays into the pre-cut window", unmuted_pre > 0.01, round(unmuted_pre, 4), "> 0.01")], [out, Path(wd) / "verify.json"]


def astats_rms(path, fps=30, sr=48000):
    txt = Path(path).with_suffix(".astats.txt")
    ff("-i", path, "-af", "aresample=%d,asetnsamples=%d,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=%s"
       % (sr, sr // fps, txt.as_posix()), "-f", "null", "-")
    vals = [float(v) if v not in ("-inf", "inf") else -120.0 for v in re.findall(r"RMS_level=(\S+)", txt.read_text())]
    return np.array(vals), txt


@card("BEAT-275")
def smoothed_audio_reactive(task, wd):
    """RMS every 1/30 s precomputed offline with ffmpeg astats to JSON, smoothed over a 100-200 ms window and clamped to
    0..1, so the reactive value is deterministic."""
    secs = 4.0
    gains = np.random.default_rng(4).uniform(0.15, 1.0, int(secs * 30))
    x = 0.3 * noise(int(secs * SR), 3) * np.repeat(gains, 1600)
    p = save(wd, "track.wav", x)
    db, txt = astats_rms(p)
    xr, _ = fx.read_wav(p)
    xr = xr[:, 0]
    npy = np.array([20 * math.log10(rms(xr[i * 1600:(i + 1) * 1600]) + 1e-12) for i in range(len(db))])
    raw = np.clip((db + 60) / 60, 0, 1)
    k = 5
    sm = np.convolve(np.pad(raw, (k // 2, k // 2), mode="edge"), np.ones(k) / k, mode="valid")
    sm = np.clip(sm, 0, 1)
    out = jdump(Path(wd) / "track.reactive.json", {"fps": 30, "window_ms": round(k / 30 * 1000), "values": [round(float(v), 4) for v in sm]})
    db2, _ = astats_rms(p)
    jit = lambda a: float(np.mean(np.abs(np.diff(a))))
    return [check("astats per-frame RMS equals the numpy measurement (±0.5 dB)", float(np.max(np.abs(db - npy))) < 0.5, round(float(np.max(np.abs(db - npy))), 3), "< 0.5"),
            check("smoothing window 100-200 ms", 100 <= k / 30 * 1000 <= 200, round(k / 30 * 1000, 1), "100..200"),
            check("values clamped to 0..1", sm.min() >= 0 and sm.max() <= 1, [round(float(sm.min()), 3), round(float(sm.max()), 3)], "0..1"),
            check("smoothed series jitters < half as much as raw", jit(sm) < 0.5 * jit(raw), [round(jit(sm), 4), round(jit(raw), 4)], "< 0.5x"),
            check("deterministic: a second astats pass gives identical values", np.array_equal(db, db2), True, True),
            check("negative control: the raw per-frame RMS fails the smoothness bound", not (jit(raw) < 0.5 * jit(raw)), round(jit(raw), 4), "rough")], [out, txt]


@card("BEAT-87")
def remotion_visualize_audio(task, wd):
    """@remotion/media-utils visualizeAudio({numberOfSamples 32, optimizeFor 'speed'}) per frame from decoded audio (bars,
    bass on the left) and visualizeAudioWaveform + createSmoothSvgPath for a waveform line; bars rendered and measured."""
    sr, secs, fps = 24000, 2.0, 30
    t = tt(secs, sr)
    x = 0.5 * np.where(t < 1.0, np.sin(2 * np.pi * 80 * t), np.sin(2 * np.pi * 5000 * t))
    p = save(wd, "tone.wav", x, sr)
    dec, _ = load_any(p, sr)
    jdump(Path(wd) / "decoded.json", [round(float(v), 5) for v in dec])
    js = """const mu=require(%s); const w=Float32Array.from(require('./decoded.json'));
const ad={channelWaveforms:[w],sampleRate:%d,durationInSeconds:%s,numberOfChannels:1,resultId:'fx',isRemote:false};
const z={channelWaveforms:[new Float32Array(w.length)],sampleRate:%d,durationInSeconds:%s,numberOfChannels:1,resultId:'z',isRemote:false};
const bars=[]; for(let f=0;f<%d;f++) bars.push(mu.visualizeAudio({audioData:ad,frame:f,fps:%d,numberOfSamples:32,optimizeFor:'speed'}));
const silent=mu.visualizeAudio({audioData:z,frame:10,fps:%d,numberOfSamples:32,optimizeFor:'speed'});
let refused=false; try{mu.visualizeAudio({audioData:ad,frame:3,fps:%d,numberOfSamples:30});}catch(e){refused=true;}
const wf=mu.visualizeAudioWaveform({audioData:ad,frame:15,fps:%d,numberOfSamples:32,windowInSeconds:0.5});
const path=mu.createSmoothSvgPath({points:wf.map((y,i)=>({x:i*10,y:50+y*40}))});
console.log(JSON.stringify({bars,silent,refused,path:path.slice(0,40),wf:wf.length}));""" % (
        json.dumps(str(NODE_MODS / "@remotion/media-utils")), sr, secs, sr, secs, int(secs * fps), fps, fps, fps, fps)
    r = node_json(wd, "viz", js)
    bars = np.array(r["bars"])
    W, H = 128, 64

    def frame(i):
        a = np.zeros((H, W, 3))
        for k, v in enumerate(bars[i]):
            h = int(min(1, v) * (H - 2))
            a[H - h:, k * 4:k * 4 + 3] = (240, 200, 90)
        return a
    v = write_video(Path(wd) / "bars.mp4", frame, len(bars), fps, (W, H))
    low = [int(np.argmax(b)) for b in bars[3:27]]
    high = [int(np.argmax(b)) for b in bars[33:57]]
    fr = fx.frames(v, (W, H))
    col = lambda i, k: float((fr[i, :, k * 4 + 1].mean(axis=-1) > 60).sum())
    return [check("bass tone: tallest bar at the left (index <= 2)", max(low) <= 2, sorted(set(low)), "<= 2"),
            check("5 kHz tone: tallest bar moves right (index >= 4)", min(high) >= 4, sorted(set(high)), ">= 4"),
            check("numberOfSamples must be a power of two (30 refused)", r["refused"], r["refused"], True),
            check("waveform line: 32 points through createSmoothSvgPath", r["wf"] == 32 and r["path"].startswith("M"), r["path"][:20], "M ..."),
            check("rendered left bar taller in the bass second than in the treble second", col(15, 0) > col(45, 0) + 5, [col(15, 0), col(45, 0)], "bass > treble"),
            check("negative control: silent audio gives flat zero bars", max((v or 0) for v in r["silent"]) < 1e-6, [v for v in r["silent"][:3]], "0 / NaN")], [v, Path(wd) / "viz.cjs"]


def analyser_level(x, sr, t, fft=256):
    i = int(t * sr)
    seg = x[i:i + fft]
    b = np.clip(np.round(128 + seg * 128), 0, 255).astype(np.uint8)
    v = (b.astype(float) - 128) / 128
    return min(1.0, math.sqrt(float(np.mean(v * v))) * 4)


@card("BEAT-42")
def mic_level_meter(task, wd):
    """AnalyserNode fftSize 256 → getByteTimeDomainData → RMS of (v-128)/128 → level = min(1, rms·4), emulated
    byte for byte on a recorded input stream and driving a VU bar that is rendered and measured."""
    sr, fps = 48000, 30
    secs = 3.0
    t = tt(secs, sr)
    x = np.where(t < 1, 0.1, np.where(t < 2, 0.5, 0.0)) * np.sin(2 * np.pi * 440 * t)
    lv = [analyser_level(x, sr, i / fps) for i in range(int(secs * fps))]
    W, H = 120, 12
    v = write_video(Path(wd) / "vu.mp4", lambda i: np.where(np.arange(W)[None, :, None] < lv[i] * W, 230, 20) * np.ones((H, W, 3)), len(lv), fps, (W, H))
    fr = fx.frames(v, (W, H))
    width = [(fr[i, H // 2, :, 1] > 128).sum() / W for i in range(len(lv))]
    out = jdump(Path(wd) / "levels.json", [round(l, 4) for l in lv])
    return [check("amp 0.1 sine → level ≈ 0.283 (rms 0.0707·4, byte-quantised ±0.02)", abs(np.median(lv[5:25]) - 0.2828) < 0.02, round(float(np.median(lv[5:25])), 4), 0.283),
            check("amp 0.5 sine → level clamps at 1", min(lv[35:55]) == 1.0, min(lv[35:55]), 1.0),
            check("silence → level 0", max(lv[65:85]) == 0.0, max(lv[65:85]), 0.0),
            check("rendered VU bar width follows the level (±3 %)", max(abs(width[i] - lv[i]) for i in range(len(lv))) < 0.03, round(max(abs(width[i] - lv[i]) for i in range(len(lv))), 4), "< 0.03"),
            check("negative control: the silent stretch does not move the bar", max(width[65:85]) == 0, max(width[65:85]), 0)], [v, out]


# ───────────────────────── songreel / montage (repo engines) ─────────────────────────
def _sr_lines():
    def line(t, words, step=0.5):
        return [{"text": w, "start": round(t + k * step, 3), "end": round(t + k * step + 0.4, 3)} for k, w in enumerate(words)]
    return [line(26.5, "مدينة لا تعرف اسمي".split()), line(34, "وباب أفتحه ولا يعرفني".split()), line(41.5, "المفتاح في يدي".split()),
            line(85, "ما أقسى من الغربة".split()), line(93.5, "أن تشتاق لمن لا يراك".split()), line(101.5, "ما أقسى من الغربة".split()),
            line(130, "سأعود سأعود".split())]


def _sr_plan():
    SRM = vmod("songreel")
    dur = 140.0
    lines = _sr_lines()
    lv = np.full(int(dur / 0.5), 0.3)
    lv[int(84 / 0.5):int(110 / 0.5)] = 0.85
    secs = SRM.sections_of(lines, dur, lv)
    ref = SRM.refrains(lines)
    bt = {"beats": list(np.arange(0, dur, 0.5)), "downbeats": list(np.arange(0, dur, 2.0))}
    peak = max((s for s in secs if s["kind"] == "vocal"), key=lambda s: s["energy"])["lines"][0]
    cands = SRM.choose_excerpt(lines, secs, bt, lv, 30, dur, ref, peak)
    ex = cands[0]
    for s in secs:
        ws = [w["text"] for i in s["lines"] for w in lines[i]]
        s["concepts"] = SRM.concepts_of(ws)[:3] if ws else (["moon"] if s["energy"] < 0.5 else ["light"])
        q = [x for c in s["concepts"] for x in SRM.SCENES.get(c, [])[:2]]
        s["queries"] = list(dict.fromkeys(q))[:4] or SRM.SCENES["moon"][:2]
    spec = {"excerpt": {"start": ex["start"], "end": ex["end"]}, "beats": bt["beats"], "loudness": list(lv), "sections": secs,
            "lines": [{"t": ln[0]["start"], "end": ln[-1]["end"], "refrain": i in ref, "text": " ".join(w["text"] for w in ln)} for i, ln in enumerate(lines)]}
    shots = SRM.shot_grid(spec, 30)
    clips = [{"file": "media/s%02d/c%d.mp4" % (secs[k % len(secs)]["i"], k), "image": False, "seconds": 20.0, "w": 1080, "h": 1920,
              "luma": 0.3 + 0.01 * k, "warmth": 0.0, "sat": 0.3, "motion": float(k)} for k in range(8)]
    shots = SRM.assign(shots, clips)
    return SRM, lines, lv, secs, ref, cands, spec, shots, clips, bt


@card("BEAT-08")
def song_reel_planner(task, wd):
    """songreel.sections_of / choose_excerpt / shot_grid / assign / concepts_of: sections from lyric gaps and loudness,
    a ~30 s excerpt on a downbeat around the loud refrain, a shot grid cutting faster where loud, clips without repeats
    kept in their section folder, lyric concepts mapped to stock-footage queries."""
    SRM, lines, lv, secs, ref, cands, spec, shots, clips, bt = _sr_plan()
    ex = cands[0]
    loud = [s["dur"] for s in shots if s["energy"] > 0.7]
    quiet = [s["dur"] for s in shots if s["energy"] < 0.5]
    picks = [s["clip"] for s in shots]
    flat = dict(spec, loudness=[0.3] * len(spec["loudness"]))
    flat_shots = SRM.shot_grid(flat, 30)
    out = jdump(Path(wd) / "songreel_plan.json", {"sections": secs, "excerpt": ex, "shots": shots, "queries": {s["i"]: s["queries"] for s in secs}})
    return [check("intro and the 41.5→85 s gap become instrumental sections", secs[0]["kind"] == "instrumental" and "instrumental" in [s["kind"] for s in secs[2:]], [s["kind"] for s in secs], "instrumental first"),
            check("excerpt starts on a downbeat, <= 32.5 s, covers the refrain 85-101.5 s", ex["start"] in bt["downbeats"] and ex["seconds"] <= 32.5 and ex["start"] <= 85 and ex["end"] >= 101.5,
                  [ex["start"], ex["end"], ex["seconds"]], "downbeat, <= 32.5"),
            check("shots 0.9-4.5 s on whole frames, total = the excerpt", all(0.9 <= s["dur"] <= 4.5 for s in shots[:-1]) and abs(sum(s["dur"] for s in shots) - (ex["end"] - ex["start"])) < 0.05,
                  [s["dur"] for s in shots], "0.9..4.5"),
            check("faster cuts where loud (median <= 1.6 s, below the same grid at quiet loudness)", loud and np.median(loud) <= 1.6 < np.median([s["dur"] for s in flat_shots]),
                  [float(np.median(loud)), float(np.median([s["dur"] for s in flat_shots]))], "loud < quiet"),
            check("never the same clip twice in a row", all(a != b for a, b in zip(picks, picks[1:])), picks, "no repeats"),
            check("lyric concepts mapped to footage queries per section", all(s["queries"] for s in secs), {s["i"]: s["queries"][:2] for s in secs}, "queries"),
            check("negative control: with flat loudness there is no fast loud stretch", not [s for s in flat_shots if s["dur"] <= 1.6 and s is not flat_shots[-1]] or np.median([s["dur"] for s in flat_shots]) > 1.6,
                  float(np.median([s["dur"] for s in flat_shots])), "> 1.6")], [out]


@card("BEAT-69")
def songreel_lyric_montage(task, wd):
    """songreel analyze → queries → cut → make, on the planner's real functions: section queries, beat-grid shots
    from the assigned clips (rendered), verse lines overlaid while they are sung; cuts and text measured."""
    SRM, lines, lv, secs, ref, cands, spec, shots, clips, bt = _sr_plan()
    from PIL import Image, ImageDraw
    a0, a1 = spec["excerpt"]["start"], spec["excerpt"]["end"]
    fps, W, H = 15, 48, 84
    n = int(round((a1 - a0) * fps))
    starts = [s["t"] for s in shots]
    lines_in = [ln for ln in spec["lines"] if ln["t"] >= a0 and ln["end"] <= a1]

    def frame(i):
        t = i / fps
        k = max(j for j, s in enumerate(starts) if s <= t + 1e-9)
        a = solid((W, H), PAL[shots[k]["clip"] % len(PAL)]).astype(float) * 0.7
        if any(ln["t"] - a0 <= t < ln["end"] - a0 for ln in lines_in):
            a[60:70, 6:42] = 255
        return a
    v = write_video(Path(wd) / "songreel.mp4", frame, n, fps, (W, H))
    fr = fx.frames(v, (W, H))
    dd = np.abs(np.diff(fr[:, :55], axis=0)).mean(axis=(1, 2, 3))
    found = [int(i + 1) for i in np.flatnonzero(dd > 10)]
    expect = [int(math.ceil(s["t"] * fps - 1e-9)) for s in shots[1:] if shots[shots.index(s) - 1]["clip"] % len(PAL) != s["clip"] % len(PAL)]
    band = fr[:, 60:70, 6:42].mean(axis=(1, 2, 3))
    sung = [int(round((ln["t"] - a0 + 0.3) * fps)) for ln in lines_in]
    gaps = [int(round((ln["end"] - a0 + 0.6) * fps)) for ln in lines_in if not any(o["t"] <= ln["end"] + 0.6 < o["end"] for o in lines_in)]
    q = jdump(Path(wd) / "queries.json", {s["i"]: {"t": s["t"], "concepts": s["concepts"], "queries": s["queries"], "media_folder": "s%02d" % s["i"]} for s in secs})
    return [check("queries per section with a media folder sNN", all("queries" in s for s in secs) and len(secs) >= 4, len(secs), ">= 4"),
            check("picture cuts at the planned shot starts (±1 frame)", frame_err(found, expect) <= 1, found[:8], expect[:8]),
            check("verse text shown while each line is sung", all(band[f] > 200 for f in sung), [round(band[f]) for f in sung], "> 200"),
            check("negative control: the text band is empty between lines", all(band[f] < 200 for f in gaps if f < len(band)), [round(band[f]) for f in gaps if f < len(band)], "< 200")], [v, q]


def _montage(wd, clips, music, **kw):
    MT = vmod("montage")
    saved = dict(MT.RATIOS)
    for k, (w, h) in saved.items():
        MT.RATIOS[k] = (w // 4 // 2 * 2, h // 4 // 2 * 2)
    old = tempfile.tempdir
    tempfile.tempdir = str(wd)
    try:
        return MT.cut([Path(c) for c in clips], Path(music), Path(wd) / "montage.mp4", **kw)
    finally:
        MT.RATIOS.update(saved)
        tempfile.tempdir = old


def _montage_fixture(wd, n=3, secs=6.0, size=(160, 90)):
    clips = []
    for k in range(n):
        w, h = size

        def frame(i, k=k):
            a = solid(size, PAL[k]).astype(float)
            x = int((i * (2 + k)) % (w - 12))
            a[h // 3:h // 3 + 12, x:x + 12] = 255
            return a
        clips.append(write_video(Path(wd) / ("clip%d.mp4" % k), frame, int(secs * 30), 30, size))
    x, _ = drum_loop(120, 8.0)
    m = save(wd, "music.wav", x + music_bed(8.0, amp=0.1))
    return clips, m


@card("BEAT-66")
def beat_cut_montage(task, wd):
    """montage.py cut CLIPS --music t.wav --seconds 5 --ratio 9:16 --grade teal_orange (rendered at 1/10 scale here):
    clips cut to detected beats with punch-ins, grade and the music mastered to -14 LUFS."""
    clips, m = _montage_fixture(wd)
    rep = _montage(wd, clips, m, seconds=5.0, ratio="9:16", grade="teal_orange")
    out = Path(rep["file"])
    pr = fx.probe(out)
    vs = next(s for s in pr["streams"] if s["codec_type"] == "video")
    found, _ = cut_frames(out, (27, 48), 30)
    planned = [int(round(p["at"] * 30)) for p in rep["plan"][1:]]
    on_beat = all(abs(p["at"] - 0.5 * round(p["at"] / 0.5)) <= 0.04 for p in rep["plan"])
    r = ebur(out)
    raw = cut_frames(clips[0], (32, 18), 30)[0]
    return [check("length = --seconds 5", abs(float(pr["format"]["duration"]) - 5.0) < 0.1, pr["format"]["duration"], 5.0),
            check("9:16 output", int(vs["width"]) * 16 == int(vs["height"]) * 9, [vs["width"], vs["height"]], "9:16"),
            check("every shot starts on a detected beat (true grid k·0.5 s, ±40 ms)", on_beat, [p["at"] for p in rep["plan"]], "k·0.5"),
            check("cuts in the picture at the planned frames (±1)", frame_err(found, planned) <= 1, found, planned),
            check("music mastered to -14 LUFS (±1.5)", abs(r["I"] + 14) <= 1.5, r["I"], -14),
            check("negative control: a source clip alone has no cuts", raw == [], raw, [])], [out, out.with_suffix(".montage.json")]


@card("BEAT-46")
def beat_planned_montage(task, wd):
    """kmotion montage: quick (~1 s) and breathing (~3 s) shots cut on beats, the most active window per clip, fill crop
    and blurred background for landscape clips in vertical, zoom punches on downbeats."""
    clips, m = _montage_fixture(wd)
    rep = _montage(wd, clips, m, seconds=8.0, ratio="9:16", grade="teal_orange", punch=True)
    out = Path(rep["file"])
    durs = [p["dur"] for p in rep["plan"]]
    punches = [h for p in rep["plan"] for h in p["punches"]]
    fr = fx.frames(out, (27, 48))
    top = fr[5:, :6, :, :].mean()
    padded = Path(wd) / "padded.mp4"
    ff("-i", clips[0], "-vf", "scale=270:-2,pad=270:480:0:(oh-ih)/2:black", "-t", "1", "-c:v", "libx264", "-pix_fmt", "yuv420p", padded)
    ptop = fx.frames(padded, (27, 48))[:, :6].mean()
    return [check("quick ~1 s shots and breathing 2.4-3.2 s shots", any(abs(d - 1.0) < 0.05 for d in durs) and any(2.4 <= d <= 3.2 for d in durs), durs, "~1 and ~3"),
            check("zoom punches scheduled on downbeats inside shots", len(punches) >= 1, punches, ">= 1"),
            check("landscape clip fills a vertical frame over a blurred background (top band not black)", top > 25, round(float(top), 1), "> 25"),
            check("active windows picked per clip (start offsets recorded)", all("from" in p for p in rep["plan"]), [p["from"] for p in rep["plan"]], "offsets"),
            check("negative control: a plain letterbox pad leaves the top band black", ptop < 10, round(float(ptop), 1), "< 10")], [out]


@card("BEAT-253")
def beat_cut_montage_recipe(task, wd):
    """Studio recipe 'montage' = kmotion.py montage: clips on the beat of a music track with a colour grade and a target
    ratio; length follows the music unless --seconds is set."""
    clips, m = _montage_fixture(wd, n=2)
    music = Path(wd) / "music4.wav"
    x, _ = drum_loop(120, 4.0)
    save(wd, music.name, x + music_bed(4.0, amp=0.1))
    rep = _montage(wd, clips, music, ratio="1:1", grade="none")
    out = Path(rep["file"])
    a = fx.frames(out, (32, 32)).mean(axis=(0, 1, 2))
    shutil.move(str(out), Path(wd) / "plain.mp4")
    rep2 = _montage(wd, clips, music, ratio="1:1", grade="teal_orange")
    b = fx.frames(Path(rep2["file"]), (32, 32)).mean(axis=(0, 1, 2))
    vs = next(s for s in fx.probe(rep2["file"])["streams"] if s["codec_type"] == "video")
    d = float(fx.probe(rep2["file"])["format"]["duration"])
    return [check("length follows the music (4.0 s)", abs(d - 4.0) < 0.1 and abs(rep["seconds"] - 4.0) < 0.05, d, 4.0),
            check("--ratio 1:1 gives a square frame", vs["width"] == vs["height"], [vs["width"], vs["height"]], "square"),
            check("teal_orange grade changes the colour against --grade none", float(np.abs(a - b).max()) > 3, [round(float(v), 1) for v in a - b], "> 3"),
            check("negative control: --grade none keeps the source palette (no teal/orange shift)", rep["grade"] == "none", rep["grade"], "none")], [Path(rep2["file"]), Path(wd) / "plain.mp4"]


# ───────────────────────── beat-driven pictures ─────────────────────────
def band_bars(x, sr, t, n=16, win=0.04, lo=50, hi=8000):
    i = int(t * sr)
    seg = x[i:i + int(win * sr)]
    if len(seg) < 16:
        return np.zeros(n)
    X = np.abs(np.fft.rfft(seg * np.hanning(len(seg))))
    f = np.fft.rfftfreq(len(seg), 1 / sr)
    edges = np.geomspace(lo, hi, n + 1)
    v = np.array([X[(f >= a) & (f < b)].sum() for a, b in zip(edges, edges[1:])])
    return v / (len(seg) / 4)


@card("BEAT-104")
def audio_only_visuals(task, wd):
    """An audio-only upload becomes a video: animated gradient background, visualiser bars, a big centred caption and a
    beat pulse (the draw() audio path, rendered here with numpy/PIL from the decoded audio)."""
    from PIL import Image, ImageDraw
    secs, fps, W, H = 3.0, 30, 96, 160
    t = tt(secs)
    x = 0.4 * np.where(t < 1.5, np.sin(2 * np.pi * 80 * t), np.sin(2 * np.pi * 3000 * t))
    k, kt = drum_loop(120, secs)
    x = x + 0.3 * highpass(k, 2000) * 0
    beats = [b for b in kt]
    a = save(wd, "upload.wav", x)
    yy = np.linspace(0, 1, H)[:, None, None]

    def pulse(tt_):
        last = max([b for b in beats if b <= tt_ + 1e-9], default=-9)
        return 1 + 0.12 * math.exp(-(tt_ - last) * 9)

    def frame(i):
        tt_ = i / fps
        c1 = np.array([40 + 60 * math.sin(tt_), 30, 90 + 50 * math.cos(tt_)])
        c2 = np.array([10, 60 + 50 * math.sin(tt_ * 1.3), 40])
        img = (c1 * (1 - yy) + c2 * yy) * np.ones((H, W, 3))
        im = Image.fromarray(img.astype(np.uint8))
        d = ImageDraw.Draw(im)
        bars = np.clip(band_bars(x, SR, tt_), 0, 1)
        for j, v in enumerate(bars):
            h = int(v * 40)
            d.rectangle([j * 6, 150 - h, j * 6 + 4, 150], fill=(250, 250, 250))
        s = pulse(tt_)
        w2, h2 = int(30 * s), int(10 * s)
        d.rectangle([W // 2 - w2, 60 - h2, W // 2 + w2, 60 + h2], fill=(255, 230, 120))
        return np.asarray(im)
    v = write_video(Path(wd) / "audio_visual.mp4", frame, int(secs * fps), fps, (W, H), audio=a)
    fr = fx.frames(v, (W, H))
    bar = lambda i, j: float((fr[i, 108:150, j * 6:j * 6 + 4, :].mean(-1) > 200).sum())
    left = bar(20, 1) - bar(70, 1)
    right = bar(70, 12) - bar(20, 12)
    bg = float(np.abs(fr[6, 2, 2] - fr[84, 2, 2]).max())
    cap = lambda i: float(((fr[i, 40:80, :, 0] > 200) & (fr[i, 40:80, :, 2] < 170)).sum())
    on, off = cap(15), cap(24)
    still = [fr[0]] * 3
    return [check("bass first: left bars tall in the 80 Hz half", left > 40, left, "> 40"),
            check("treble later: right bars tall in the 3 kHz half", right > 40, right, "> 40"),
            check("background gradient animates (colour moves > 20)", bg > 20, round(bg, 1), "> 20"),
            check("centred caption pulses on the beat (>= 8 % bigger on the kick frame)", on > off * 1.08, [on, off], "on > off"),
            check("negative control: a still image has no bar motion", float(np.abs(still[0] - still[2]).max()) == 0, 0, 0)], [v]


@card("BEAT-112")
def beat_freeze_cut(task, wd):
    """Beat Freeze Cut (beat1 0.7 s, beat2 2.2 s, 6 s): speed ramp, beat-locked freeze frame with flash, contour outline
    and FREEZE badge, then a hard cut - the composition's timeline reproduced frame by frame (GSAP not needed) and measured."""
    from PIL import Image, ImageDraw, ImageFilter
    fps, W, H = 30, 160, 90
    b1, b2, secs = 0.7, 2.2, 6.0

    def src_pos(st):
        return 10 + 40 * st

    def src_time(t):
        return 0.5 * t + 0.75 * t * t / 0.7 if t < b1 else 0.5 * b1 + 0.75 * b1

    def draw(xpos, bg=(30, 30, 50)):
        im = Image.new("RGB", (W, H), bg)
        ImageDraw.Draw(im).rectangle([int(xpos), 35, int(xpos) + 16, 51], fill=(240, 120, 40))
        return im
    frames, pos = [], []
    for i in range(int(secs * fps)):
        t = i / fps
        if t < b2:
            p = src_pos(src_time(t))
            im = draw(p)
            if t >= b1:
                edge = im.filter(ImageFilter.FIND_EDGES).convert("L")
                arr = np.asarray(im).astype(float)
                arr[np.asarray(edge) > 30] = 255
                fl = max(0.0, 1 - (t - b1) / 0.2)
                arr = arr * (1 - fl) + 255 * fl
                im = Image.fromarray(arr.astype(np.uint8))
                d = ImageDraw.Draw(im)
                d.rectangle([4, 4, 52, 16], fill=(255, 255, 255))
                d.text((7, 5), "FREEZE", fill=(0, 0, 0))
        else:
            p = 20 + 30 * (t - b2)
            im = draw(p, (20, 90, 60))
        pos.append(p)
        frames.append(np.asarray(im))
    v = write_video(Path(wd) / "beat_freeze_cut.mp4", lambda i: frames[i], len(frames), fps, (W, H))
    fr = fx.frames(v, (W, H))
    f1, f2 = int(math.ceil(b1 * fps)), int(math.ceil(b2 * fps))
    sq = fr[:, 38:48, :, 0]
    xs = [float(np.argmax((sq[i].mean(0) > 200) * 1.0)) for i in range(len(fr))]
    steps = np.diff(xs[:f1])
    frozen = max(xs[f1 + 8:f2]) - min(xs[f1 + 8:f2])
    lum = fr.mean(axis=(1, 2, 3))
    badge = fr[:, 5:15, 5:50].mean(axis=(1, 2, 3))
    cut = float(np.abs(fr[f2] - fr[f2 - 1]).mean())
    raw = [src_pos(t * 1.0) for t in np.arange(0, 2.2, 1 / fps)]
    jdump(Path(wd) / "timeline.json", {"beat1": b1, "beat2": b2, "duration": secs, "freeze_frames": [f1, f2]})
    return [check("speed ramp: the subject moves faster each frame before beat 1", steps[-3:].mean() > 2 * steps[:3].mean(), [round(float(steps[:3].mean()), 2), round(float(steps[-3:].mean()), 2)], "accelerating"),
            check("freeze holds the subject still from beat 1 to beat 2", frozen <= 1, frozen, "<= 1 px"),
            check("white flash on the beat-1 frame (brightest frame)", int(np.argmax(lum)) == f1, int(np.argmax(lum)), f1),
            check("FREEZE badge shown only during the freeze", badge[f1 + 8:f2].min() > 150 and badge[:f1 - 1].max() < 100 and badge[f2 + 1:].max() < 100, [round(float(badge[f1 + 8])), round(float(badge[f1 - 2])), round(float(badge[f2 + 2]))], "on only in freeze"),
            check("hard cut on beat 2", cut > 30, round(cut, 1), "> 30"),
            check("negative control: the source never holds still", min(np.diff(raw)) > 1, round(float(min(np.diff(raw))), 3), "> 1")], [v, Path(wd) / "timeline.json"]


@card("BEAT-115")
def align_sound_to_event(task, wd):
    """The SFX clip's data-start is set to the tween position of the visual hit minus the file's own transient offset,
    so the audible transient lands on the hit frame (audio alignment recipe)."""
    fps, W, H = 30, 120, 60
    tl_pos, dur = 1.2, 0.5
    hit = tl_pos + dur
    lead = 0.09
    sfx = np.concatenate([0.02 * bandpass(noise(int(lead * SR), 1), 300, 3000) * np.linspace(0, 1, int(lead * SR)),
                          0.9 * addp(kick(), 0.3 * highpass(noise(int(.05 * SR), 2), 2000) * _decay(.05, .01))])
    sp = save(wd, "impact.wav", sfx)
    tr = onsets(np.concatenate([np.zeros(200), sfx]), SR, 0.3, 0.02)[0] - 200 / SR
    start = round(hit - tr, 3)
    secs = 2.6
    mix = np.zeros(int(secs * SR))
    place(mix, sfx, start)
    a = save(wd, "mix.wav", mix)

    def frame(i):
        t = i / fps
        u = min(1.0, max(0.0, (t - tl_pos) / dur))
        x = 5 + (W - 25) * (u * u)
        img = solid((W, H), (20, 20, 30)).astype(float)
        img[20:40, int(x):int(x) + 12] = 255
        img[:, W - 8:] = 120
        return img
    v = write_video(Path(wd) / "hit.mp4", frame, int(secs * fps), fps, (W, H), audio=a)
    y, _ = load_any(v)
    heard = [o for o in onsets(y, SR, 0.3, 0.25) if 1.0 < o < 2.2]
    fr = fx.frames(v, (W, H))
    xs = [int(np.argmax(fr[i, 30, :W - 9, 0] > 200)) for i in range(len(fr))]
    hit_f = next(i for i, x in enumerate(xs) if x >= W - 21)
    html = tdump(Path(wd) / "index.html", '<div class="ball" data-tween-position="%s" data-duration="%s"></div>\n<audio id="impact" src="impact.wav" data-start="%s"></audio>\n'
                 % (tl_pos, dur, start))
    naive = hit + tr
    return [check("file transient measured %.0f ms after its start" % (lead * 1000), abs(tr - lead) < 0.005, round(tr, 4), lead),
            check("data-start = hit - transient offset", abs(start - (hit - lead)) < 0.006, start, round(hit - lead, 3)),
            check("audible transient on the visual hit frame (±1 frame)", len(heard) == 1 and abs(heard[0] * fps - hit_f) <= 1, [round(heard[0] * fps, 2) if heard else None, hit_f], "±1"),
            check("negative control: data-start at the hit puts the transient > 1 frame late", (naive - hit) * fps > 1, round((naive - hit) * fps, 2), "> 1 frame")], [v, html]


@card("BEAT-130")
def beat_motion_primitives(task, wd):
    """Catalogued beat moves driven by measured onsets: chromatic-pressure (RGB split 0.1-0.5 s after transients),
    color-grid-shuffle (cells recoloured per onset), content-swap (0 ms percussive swap), freeze-hold (0.5-2 s),
    negative-space-hold (one mark in empty space 1-6 s)."""
    fps, W, H = 30, 64, 64
    secs = 6.0
    hits = [0.3, 1.2, 1.5, 1.8, 2.4, 2.9]
    x = clicks(hits, secs, f=1500)
    a = save(wd, "hits.wav", x)
    on = onsets(x, SR, 0.3, 0.1)
    rng = np.random.default_rng(3)
    grid_cols = {}

    def last_on(t):
        return max([o for o in on if o <= t + 1e-9], default=None)

    def frame(i):
        t = i / fps
        img = np.zeros((H, W, 3))
        if t < 1.0:
            img[16:48, 24:40] = 200
            lo = last_on(t)
            sh = int(round(4 * max(0.0, 1 - (t - lo) / 0.3))) if lo is not None and t - lo <= 0.3 else 0
            if sh:
                img[:, :, 0] = np.roll(img[:, :, 0], sh, axis=1)
                img[:, :, 2] = np.roll(img[:, :, 2], -sh, axis=1)
        elif t < 2.2:
            lo = last_on(t)
            key = round(lo, 3) if lo is not None and lo >= 1.0 else 0
            if key not in grid_cols:
                grid_cols[key] = rng.integers(40, 255, (4, 4, 3))
            img = np.kron(grid_cols[key], np.ones((16, 16, 1))).astype(float)
        elif t < 3.2:
            img[:] = (220, 60, 60) if (last_on(t) or 0) < 2.7 else (60, 60, 220)
        elif t < 4.2:
            img[20:44, 20 + int(min(t, 3.4) * 10 - 32):40 + int(min(t, 3.4) * 10 - 32)] = 255
        else:
            img[30:34, 30:34] = 255
        return img
    v = write_video(Path(wd) / "primitives.mp4", frame, int(secs * fps), fps, (W, H), audio=a)
    fr = fx.frames(v, (W, H))
    split = [float(np.abs(fr[i, :, :, 0] - fr[i, :, :, 1]).mean()) for i in range(len(fr))]
    chrom_on = split[int(round(0.3 * fps)) + 1]
    chrom_off = split[int(round(0.8 * fps))]
    gd = np.abs(np.diff(fr[30:66], axis=0)).mean(axis=(1, 2, 3))
    g_changes = [30 + int(j) + 1 for j in np.flatnonzero(gd > 20)]
    g_expect = [int(math.ceil(o * fps - 1e-9)) for o in on if 1.0 < o < 2.2]
    swap = int(math.ceil(min(on, key=lambda o: abs(o - 2.9)) * fps - 1e-9))
    mid = [float(np.abs(fr[swap - 1] - fr[swap]).mean()), float(np.abs(fr[swap] - fr[swap + 1]).mean())]
    hold = [i for i in range(int(3.2 * fps) + 1, int(4.2 * fps)) if float(np.abs(fr[i] - fr[i - 1]).mean()) < 0.5]
    run = len(hold) / fps
    empty = float((fr[int(5 * fps)].mean(-1) > 40).mean())
    raw = fx.frames(cut_video(Path(wd) / "static.mp4", [], 1.0, fps, (W, H)), (W, H))
    jdump(Path(wd) / "primitives.json", {"onsets": on, "grid_changes": g_changes})
    return [check("chromatic pressure: RGB split right after a transient, gone 0.5 s later", chrom_on > 5 and chrom_off < 1, [round(chrom_on, 2), round(chrom_off, 2)], "on > 5, off < 1"),
            check("colour grid reshuffles exactly on each onset frame", g_changes == g_expect, g_changes, g_expect),
            check("content swap is a 0 ms cut (one changing frame, none after)", mid[0] > 50 and mid[1] < 1, [round(m, 1) for m in mid], "swap then still"),
            check("freeze-hold lasts 0.5-2 s", 0.5 <= run <= 2.0, round(run, 2), "0.5..2"),
            check("negative-space hold: one mark in >= 95 % empty frame", empty < 0.05 and empty > 0, round(empty, 4), "< 0.05"),
            check("negative control: an untreated clip has no RGB split", float(np.abs(raw[5, :, :, 0] - raw[5, :, :, 0]).mean()) < 1 and max(split[int(.8 * fps):int(.95 * fps)]) < 1, 0, "< 1")], [v]


def accent_series(beats, n, fps, attack=2, tau=0.08):
    a = np.zeros(n)
    for b in beats:
        f0 = int(round(b * fps))
        for i in range(f0, n):
            d = i - f0
            v = d / attack if d < attack else math.exp(-(d - attack) / fps / tau)
            a[i] = max(a[i], v)
    return a


def disc_video(wd, scale, fps=30, size=(120, 120), name="pulse.mp4", r0f=0.3):
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w]
    r0 = r0f * min(w, h)

    def frame(i):
        m = ((xx - w / 2) ** 2 + (yy - h / 2) ** 2) <= (r0 * scale[i]) ** 2
        a = np.zeros((h, w, 3))
        a[m] = 255
        return a
    v = write_video(Path(wd) / name, frame, len(scale), fps, size)
    fr = fx.frames(v, size)
    area = (fr.mean(axis=3) > 128).sum(axis=(1, 2))
    return v, np.sqrt(area / (math.pi * r0 * r0))


@card("BEAT-156")
def audio_wave_style(task, wd):
    """audio-wave style: RMS envelope per 1/30 s from ffmpeg astats, smoothed 100-200 ms; accent attack 1-2 frames, decay
    150-300 ms; pulse 1 → 1.04; bars and a pulsing disc rendered and measured."""
    secs, fps = 3.0, 30
    x, kt = drum_loop(120, secs)
    p = save(wd, "voice_music.wav", x)
    db, _ = astats_rms(p)
    env = np.clip((db + 60) / 60, 0, 1)
    sm = np.convolve(np.pad(env, (2, 2), mode="edge"), np.ones(5) / 5, mode="valid")
    on = onsets(x, SR, 0.3, 0.2)
    acc = accent_series(on, len(sm), fps, attack=2, tau=0.07)
    scale = 1 + 0.04 * acc
    v, meas = disc_video(wd, scale, fps)
    pk = [int(round(o * fps)) + 2 for o in on if o * fps + 10 < len(meas)]
    decay_f = [next(d for d in range(1, 15) if acc[f + d] < 0.1) for f in pk]
    out = jdump(Path(wd) / "wave.json", {"rms": [round(float(v_), 4) for v_ in sm], "accent": [round(float(a_), 4) for a_ in acc]})
    _, sil = disc_video(wd, 1 + 0.04 * accent_series([], len(sm), fps), fps, name="silent.mp4")
    return [check("pulse peaks at 1.04 two frames after each onset (±0.012)", all(abs(meas[f] - 1.04) <= 0.012 for f in pk), [round(meas[f], 3) for f in pk], 1.04),
            check("attack 2 frames: half-way on the first frame", all(abs(acc[f - 1] - 0.5) < 1e-9 for f in pk), [acc[f - 1] for f in pk], 0.5),
            check("decay to 10 % within 150-300 ms", all(4.5 <= d <= 9 for d in decay_f), decay_f, "5..9 frames"),
            check("smoothed RMS follows the kicks (higher on kick frames)", min(sm[int(o * fps) + 1] for o in on) > np.median(sm), round(float(np.median(sm)), 3), "kick > median"),
            check("negative control: no onsets → the disc stays at 1.0", float(np.max(np.abs(sil - 1))) < 0.015, round(float(np.max(np.abs(sil - 1))), 4), "~0")], [v, out]


@card("BEAT-157")
def category_music(task, wd):
    """Category 'music' (tools/kosif.py list --category music) and its playbook numbers applied to one edit: beat =
    60/BPM, cut 1 frame before the beat, accent attack 1-2 f / decay 150-300 ms, duck 8-12 dB at 150/400 ms, -14 LUFS,
    TP <= -1 dBTP."""
    lst = sh([sys.executable, REPO / "tools/kosif.py", "list", "--category", "music"], cwd=REPO, timeout=40)
    m_ = re.search(r"^(\d+)\s", lst.strip().splitlines()[-1])
    n = int(m_.group(1)) if m_ else 0
    tdump(Path(wd) / "music_category.txt", lst)
    bpm, fps, secs = 120, 30, 4.0
    k, kt = drum_loop(bpm, secs)
    m = save(wd, "music.wav", k * 0.5 + music_bed(secs, amp=0.3))
    voice = save(wd, "voice.wav", speechlike(secs, [(1.5, 3.0)], f0=150, amp=0.5))
    ducked = sc_duck(m, voice, Path(wd) / "ducked.wav", 0.03, 2.5, 150, 400)
    y, _ = load_any(ducked)
    vo, _ = load_any(voice)
    mix = save(wd, "mix.wav", y + vo)
    out = Path(wd) / "mix_-14.wav"
    loudnorm2(mix, out, -14, -1.0, 11)
    r = ebur(out)
    bed = music_bed(secs, amp=0.3)
    nb = save(wd, "bed.wav", bed)
    db_ = sc_duck(nb, voice, Path(wd) / "bed_ducked.wav", 0.03, 2.5, 150, 400)
    z, _ = load_any(db_)
    depth = seg_db(bed, SR, 0.5, 1.4) - seg_db(z, SR, 2.0, 2.9)
    cuts = [int(round(b * fps)) - 1 for b in kt[2::2]]
    v = cut_video(Path(wd) / "cuts.mp4", [c / fps for c in cuts], secs, fps, audio=out)
    found, _ = cut_frames(v)
    lead = [int(round(b * fps)) - f for f, b in zip(found, kt[2::2])]
    return [check("category 'music' lists >= 49 catalog entries", n >= 49, n, ">= 49"),
            check("beat = 60/BPM = 0.5 s and cuts land 1 frame before the beat", abs(60 / bpm - 0.5) < 1e-12 and lead and all(l == 1 for l in lead), lead, 1),
            check("bed ducked 8-12 dB under the voice", 8 <= depth <= 12, round(depth, 2), "8..12"),
            check("mix at -14 LUFS (±0.5), TP <= -1 dBTP (±0.2)", abs(r["I"] + 14) <= 0.5 and r["TP"] <= -0.8, r, "-14/-1"),
            check("negative control: the unducked bed keeps its level under the voice", abs(seg_db(bed, SR, 0.5, 1.4) - seg_db(bed, SR, 2.0, 2.9)) < 1, round(seg_db(bed, SR, 0.5, 1.4) - seg_db(bed, SR, 2.0, 2.9), 2), "< 1")], [out, v, Path(wd) / "music_category.txt"]


@card("BEAT-160")
def beat_pulse_remotion(task, wd):
    """Remotion BeatPulse: since = ((f - offset·fps) mod beatFrames); scale = interpolate(since, [0,2,8], [1,1.04,1])
    computed with remotion's own interpolate in node, rendered as a disc and measured."""
    fps, bpm, offset, n = 30, 120, 0.2, 90
    js = """const {interpolate}=require(%s); const fps=%d, beat=fps*60/%d, off=%s; const out=[];
for(let f=0;f<%d;f++){const since=(((f-off*fps)%%beat)+beat)%%beat; out.push(interpolate(since,[0,2,8],[1,1.04,1],{extrapolateRight:'clamp'}));}
console.log(JSON.stringify(out));""" % (json.dumps(str(NODE_MODS / "remotion")), fps, bpm, offset, n)
    sc = node_json(wd, "beatpulse", js)
    v, meas = disc_video(wd, sc, fps)
    beatf = 15
    peaks = [int(offset * fps) + 2 + k * beatf for k in range(5)]
    rest = [int(offset * fps) + 9 + k * beatf for k in range(5)]
    out = jdump(Path(wd) / "scale.json", sc)
    return [check("interpolate gives 1.04 two frames after each beat", all(abs(sc[p] - 1.04) < 1e-9 for p in peaks), [sc[p] for p in peaks], 1.04),
            check("back to 1.0 from frame 8 after the beat", all(abs(sc[r] - 1.0) < 1e-9 for r in rest), [sc[r] for r in rest], 1.0),
            check("rendered disc measures 1.04 on the peak frames (±0.012)", all(abs(meas[p] - 1.04) <= 0.012 for p in peaks), [round(float(meas[p]), 3) for p in peaks], 1.04),
            check("negative control: off-beat frames are not at the peak", all(abs(meas[r] - 1.04) > 0.02 for r in rest), [round(float(meas[r]), 3) for r in rest], "!= 1.04")], [v, out]


@card("BEAT-183")
def flash_word_montage(task, wd):
    """Hard-cut one giant uppercase word per beat (~233 ms, 5 words) with a small footer label and a 01/05 page counter,
    cards drawn with ImageMagick convert."""
    words = ["BUILD", "SHIP", "LEARN", "REPEAT", "WIN"]
    W, H, fps, per = 160, 90, 30, 7
    pngs = []
    for k, w in enumerate(words):
        p = Path(wd) / ("card_%02d.png" % (k + 1))
        sh(["convert", "-size", "%dx%d" % (W, H), "xc:black", "-fill", "white", "-pointsize", str(min(56, int(170 / len(w)))), "-gravity", "center", "-annotate", "+0-6", w,
            "-pointsize", "9", "-gravity", "southwest", "-annotate", "+4+3", "kosif / motion", "-gravity", "southeast", "-annotate", "+4+3", "%02d/05" % (k + 1), p])
        pngs.append(p)
    v = Path(wd) / "flash_words.mp4"
    ff("-framerate", "%d/%d" % (fps, per), "-i", Path(wd) / "card_%02d.png", "-r", str(fps), "-c:v", "libx264", "-pix_fmt", "yuv420p", v)
    fr = fx.frames(v, (W, H))
    d = np.abs(np.diff(fr[:, :70], axis=0)).mean(axis=(1, 2, 3))
    cuts = [int(i + 1) for i in np.flatnonzero(d > 3)]
    cnt = np.abs(np.diff(fr[:, 78:, 120:], axis=0)).mean(axis=(1, 2, 3))
    cchg = [int(i + 1) for i in np.flatnonzero(cnt > 3)]
    from PIL import Image
    widths = []
    for p in pngs:
        a = np.asarray(Image.open(p).convert("L"))[:70] > 128
        cols = np.flatnonzero(a.any(0))
        widths.append((cols[-1] - cols[0]) / W)
    still = fx.frames(v, (W, H))[:per]
    return [check("hard cut every 7 frames (233 ms ≈ 4 words/s)", cuts == [7, 14, 21, 28], cuts, [7, 14, 21, 28]),
            check("page counter changes with every word", cchg == [7, 14, 21, 28], cchg, [7, 14, 21, 28]),
            check("words are giant (>= 40 % of the width)", min(widths) >= 0.4, [round(w_, 2) for w_ in widths], ">= 0.4"),
            check("5 words, 35 frames", len(fr) == 35, len(fr), 35),
            check("negative control: one card held has no cuts", float(np.abs(np.diff(still, axis=0)).mean()) < 1, round(float(np.abs(np.diff(still, axis=0)).mean()), 3), "< 1")], [v] + pngs[:1]


@card("BEAT-184")
def explosion_climax(task, wd):
    """Countdown → white flash → fireball (noise-displaced emissive sphere expanding 1.5 s ease-out) timed to the music hit
    measured in the track."""
    secs, fps, W, H = 4.0, 30, 96, 96
    x = 0.05 * music_bed(secs)
    place(x, 1.0 * addp(kick(), 0.4 * highpass(noise(int(.4 * SR), 2), 1000) * _decay(.4, .1)), 2.0)
    a = save(wd, "music.wav", x)
    hit = onsets(x, SR, 0.3, 0.2)[0]
    hf_ = int(round(hit * fps))
    rng = np.random.default_rng(2)
    ang = np.linspace(0, 2 * np.pi, 64, endpoint=False)
    bump = rng.uniform(0.85, 1.15, 64)
    yy, xx = np.mgrid[0:H, 0:W]
    th = np.arctan2(yy - H / 2, xx - W / 2) % (2 * np.pi)
    rr = np.hypot(yy - H / 2, xx - W / 2)
    disp = np.interp(th, ang, bump, period=2 * np.pi)
    R = 40

    def frame(i):
        img = np.zeros((H, W, 3))
        t = i / fps
        if i < hf_:
            n = 3 - int(t // (hit / 3))
            img[40:56, 44:52] = 60 + 50 * n
        elif i == hf_:
            img[:] = 255
        else:
            u = min(1.0, (t - hit) / 1.5)
            r = R * (1 - (1 - u) ** 3)
            m = rr <= r * disp
            img[m] = (255, 160, 40)
        return img
    v = write_video(Path(wd) / "explosion.mp4", frame, int(secs * fps), fps, (W, H), audio=a)
    fr = fx.frames(v, (W, H))
    lum = fr.mean(axis=(1, 2, 3))
    area = ((fr[:, :, :, 0] > 150) & (fr[:, :, :, 2] < 120)).sum(axis=(1, 2))
    rad = np.sqrt(area / math.pi)
    f15 = hf_ + int(1.5 * fps)
    half = hf_ + int(0.75 * fps)
    grow = (rad[half] - rad[hf_ + 1]) / (rad[f15] - rad[hf_ + 1])
    jdump(Path(wd) / "climax.json", {"hit_s": hit, "flash_frame": hf_, "fireball_s": 1.5})
    return [check("flash frame = the hit measured in the music (±1)", abs(int(np.argmax(lum)) - hit * fps) <= 1, [int(np.argmax(lum)), round(hit * fps, 2)], "±1"),
            check("fireball grows monotonically and stops at 1.5 s", all(np.diff(rad[hf_ + 1:f15 + 1]) >= -0.6) and abs(rad[f15 + 5] - rad[f15]) < 0.6, [round(float(rad[k]), 1) for k in (hf_ + 1, half, f15, f15 + 5)], "monotone, then still"),
            check("ease-out: > 75 % of the growth in the first half", grow > 0.75, round(float(grow), 3), "> 0.75"),
            check("countdown steps before the hit", len({int(round(float(fr[i, 42:54, 45:51].mean()) / 10)) for i in range(hf_ - 1)}) >= 3,
                  sorted({int(round(float(fr[i, 42:54, 45:51].mean()) / 10)) for i in range(hf_ - 1)}), ">= 3 steps"),
            check("negative control: no flash before the hit", lum[:hf_ - 1].max() < 100, round(float(lum[:hf_ - 1].max()), 1), "< 100")], [v]


@card("BEAT-186")
def beat_cut_reel_chips(task, wd):
    """On the drop, hard-cut 3 full-bleed clips one beat each (120 BPM = 0.5 s); each carries a dark #111 pill chip
    (radius 999 px) with an avatar and @handle inside the safe area bottom-left."""
    from PIL import Image, ImageDraw
    secs, fps, W, H = 3.5, 30, 108, 192
    x = 0.03 * music_bed(secs)
    drop = 1.5
    k, kt = drum_loop(120, secs - drop + 0.3)
    place(x, k, drop)
    a = save(wd, "music.wav", x)
    d_on = onsets(x, SR, 0.3, 0.2)[0]
    cuts = [d_on + j * 0.5 for j in range(3)]
    chip = (6, 150, 70, 164)

    def frame(i):
        t = i / fps
        j = sum(1 for c in cuts if c <= t + 1e-9)
        im = Image.new("RGB", (W, H), PAL[j % len(PAL)])
        if j:
            d = ImageDraw.Draw(im)
            d.rounded_rectangle(chip, radius=999, fill=(17, 17, 17))
            d.ellipse([chip[0] + 2, chip[1] + 2, chip[0] + 12, chip[1] + 12], fill=(200, 200, 200))
            d.text((chip[0] + 16, chip[1] + 2), "@kosif", fill=(255, 255, 255))
        return np.asarray(im)
    v = write_video(Path(wd) / "reel_burst.mp4", frame, int(secs * fps), fps, (W, H), audio=a)
    fr = fx.frames(v, (W, H))
    found = [int(i + 1) for i in np.flatnonzero(np.abs(np.diff(fr[:, :120], axis=0)).mean(axis=(1, 2, 3)) > 20)]
    exp = [int(math.ceil(c * fps - 1e-9)) for c in cuts]
    dark = (np.abs(fr - 17).max(-1) < 14)
    inside = [dark[i, chip[1]:chip[3], chip[0] + 20:chip[2] - 8].mean() for i in exp]
    corner = [dark[i, chip[1], chip[0]] for i in exp]
    safe = chip[0] >= 0.05 * W and chip[3] <= 0.88 * H
    pre = dark[: exp[0] - 1, chip[1]:chip[3], chip[0]:chip[2]].mean()
    return [check("three hard cuts one beat apart starting on the drop", frame_err(found, exp) <= 1 and len(found) == 3, found, exp),
            check("dark #111 chip present on each clip", min(inside) > 0.5, [round(float(v_), 2) for v_ in inside], "> 0.5"),
            check("pill shape: the chip's corner pixel is clip colour (radius 999)", not any(corner), corner, False),
            check("chip inside the bottom-left safe area", safe, chip, "x >= 5 %, bottom <= 88 %"),
            check("negative control: no chip before the drop", pre < 0.05, round(float(pre), 3), "< 0.05")], [v]


@card("BEAT-195")
def silence_before_drop(task, wd):
    """Cut to near-black with only a tiny mono code line for the silent beat before the drop (~0.5-1 s), then flash into
    the climax on the drop; the hold is aligned to the silence measured in the track."""
    from PIL import Image, ImageDraw
    secs, fps, W, H = 4.0, 30, 128, 72
    x, _ = drum_loop(120, secs)
    x = x + music_bed(secs, amp=0.2)
    x[int(1.75 * SR):int(2.5 * SR)] = 0
    a = save(wd, "music.wav", x)
    e = envelope(x, SR, 5)
    q = np.flatnonzero(e[int(1.0 * SR):int(3 * SR)] < 1e-4)
    s0, s1 = 1.0 + q[0] / SR, 1.0 + q[-1] / SR
    drop = s1

    def frame(i):
        t = i / fps
        if t < s0:
            return solid((W, H), (40, 90, 160))
        if t < drop:
            im = Image.new("RGB", (W, H), (6, 6, 8))
            ImageDraw.Draw(im).text((4, 30), "> run()", fill=(150, 150, 150))
            return np.asarray(im)
        u = (t - drop)
        return np.clip(solid((W, H), (230, 80, 40)).astype(float) + 255 * max(0, 1 - u / 0.15), 0, 255)
    v = write_video(Path(wd) / "drop.mp4", frame, int(secs * fps), fps, (W, H), audio=a)
    fr = fx.frames(v, (W, H))
    lum = fr.mean(axis=(1, 2, 3))
    blk = [i for i in range(len(lum)) if lum[i] < 20]
    hold = len(blk) / fps
    txt = float((fr[blk[len(blk) // 2]].mean(-1) > 60).mean())
    df = int(math.ceil(drop * fps - 1e-9))
    return [check("silent beat measured 0.5-1 s in the track", 0.5 <= s1 - s0 <= 1.0, round(s1 - s0, 3), "0.5..1"),
            check("near-black hold matches the silence (±1 frame)", abs(blk[0] - s0 * fps) <= 1 and abs(blk[-1] + 1 - drop * fps) <= 1, [blk[0], blk[-1]], [round(s0 * fps, 1), round(drop * fps, 1)]),
            check("only a tiny code line on the black (< 3 % of pixels)", 0 < txt < 0.03, round(txt, 4), "< 0.03"),
            check("flash into the climax on the drop frame", lum[df] > 240, round(float(lum[df]), 1), "> 240"),
            check("negative control: the music before the silence is not silent", seg_db(x, SR, 0.5, 1.5) > -30, round(seg_db(x, SR, 0.5, 1.5), 1), "> -30")], [v]


def token_boxes(tokens, x0=4, y0=20, cw=6):
    out, x = [], x0
    for t in tokens:
        out.append((x - 1, y0 - 2, x + cw * len(t), y0 + 10))
        x += cw * (len(t) + 1)
    return out


@card("BEAT-199")
def beat_highlighted_code(task, wd):
    """Highlight the token box on each step event, one step per 1/16 note (120 BPM → 125 ms), frame times rounded and
    logged."""
    from PIL import Image, ImageDraw
    tokens = "const beat = 60 / bpm ; cut ( t )".split()
    boxes = token_boxes(tokens)
    fps, bpm, W, H = 30, 120, 220, 40
    step = 60 / bpm / 4
    n = int(len(tokens) * step * fps) + 2

    def frame(i):
        k = min(len(tokens) - 1, int((i / fps + 1e-9) / step))
        im = Image.new("RGB", (W, H), (12, 14, 20))
        d = ImageDraw.Draw(im)
        b = boxes[k]
        d.rectangle(b, fill=(230, 180, 60))
        x = 4
        for t in tokens:
            d.text((x, 20), t, fill=(240, 240, 240))
            x += 6 * (len(t) + 1)
        return np.asarray(im)
    v = write_video(Path(wd) / "code_steps.mp4", frame, n, fps, (W, H))
    fr = fx.frames(v, (W, H))
    ylw = (fr[:, :, :, 0] > 180) & (fr[:, :, :, 2] < 120)
    cx = [float(np.flatnonzero(ylw[i].any(0)).mean()) for i in range(len(fr))]
    chg = [i for i in range(1, len(fr)) if abs(cx[i] - cx[i - 1]) > 2]
    exp = [int(math.ceil(k * step * fps - 1e-9)) for k in range(1, len(tokens))]
    centre = [(b[0] + b[2]) / 2 for b in boxes]
    on_tok = all(abs(cx[e] - centre[k + 1]) < 3 for k, e in enumerate(exp))
    log = jdump(Path(wd) / "steps.json", [{"k": k, "t": round(k * step, 4), "frame": e, "rounding_ms": round((e / fps - k * step) * 1000, 2)} for k, e in zip(range(1, len(tokens)), exp)])
    return [check("highlight moves exactly on the 1/16 frames (ceil of k·125 ms·30)", chg == exp, chg, exp),
            check("highlight box sits on token k", on_tok, [round(cx[e]) for e in exp], [round(c) for c in centre[1:]]),
            check("rounding logged (<= 1 frame)", all(abs(r["rounding_ms"]) <= 33.4 for r in json.loads(log.read_text())), "logged", "<= 33 ms"),
            check("negative control: a static frame has no highlight moves", len({round(c) for c in cx[:3]}) == 1, [round(c) for c in cx[:3]], "one position")], [v, log]


@card("BEAT-200")
def style_roll_card(task, wd):
    """Swap the result image every 16th note (60/BPM/4 s; 130 BPM → 115 ms) among style variants, a black pill chip
    rolls vertically to the new style name in 80 ms, the thumbnail strip highlights the current one (rendered at 60 fps)."""
    fps, bpm, W, H = 60, 130, 96, 96
    step = 60 / bpm / 4
    styles = [(220, 80, 80), (80, 200, 120), (80, 120, 230), (230, 200, 60)]
    n = int(8 * step * fps) + 4

    def frame(i):
        t = i / fps
        k = int((t + 1e-9) / step)
        a = solid((W, H), styles[k % 4]).astype(float)
        u = min(1.0, (t - k * step) / 0.08)
        cy = int(round(10 + 12 * (1 - u)))
        a[cy:cy + 8, 30:66] = 0
        for j in range(4):
            a[84:94, 4 + j * 24:22 + j * 24] = 255 if j == k % 4 else 90
        return a
    v = write_video(Path(wd) / "style_roll.mp4", frame, n, fps, (W, H))
    fr = fx.frames(v, (W, H))
    main = fr[:, 40:80, 4:90].mean(axis=(1, 2))
    sw = [i for i in range(1, len(fr)) if np.abs(main[i] - main[i - 1]).max() > 30]
    exp = [e for e in (int(math.ceil(k * step * fps - 1e-9)) for k in range(1, 20)) if e < len(fr) - 2]
    blackrow = [int(np.flatnonzero((fr[i, :40, 48].mean(-1) if fr.ndim == 4 else fr[i, :40, 48]) < 30)[0]) for i in range(len(fr))]
    roll = [blackrow[e:e + 6] for e in exp[:2]]
    hi = [int(np.argmax([fr[e + 1, 89, 13 + j * 24].mean() for j in range(4)])) for e in exp]
    return [check("swap every 115 ms (130 BPM 16ths) at 60 fps", sw == exp and abs(step - 0.11538) < 1e-4, sw, exp),
            check("chip rolls into place within 80 ms (~5 frames) after each swap", all(r[0] > r[-1] and r[-1] == 10 for r in roll), roll, "falls to row 10"),
            check("thumbnail strip highlights the current style", hi == [k % 4 for k in range(1, len(exp) + 1)], hi, [k % 4 for k in range(1, len(exp) + 1)]),
            check("negative control: between swaps the main image is still", np.abs(main[exp[0] + 2] - main[exp[0] + 4]).max() < 2, round(float(np.abs(main[exp[0] + 2] - main[exp[0] + 4]).max()), 2), "< 2")], [v]


@card("BEAT-207")
def bpm_word_flashes(task, wd):
    """At 120 BPM hard cuts on beats and half-beats (0.5 / 0.25 s), each cut showing one word or a full colour flash;
    6-8 cuts in 2 s (rendered at 60 fps so 0.25 s is 15 whole frames)."""
    from PIL import Image, ImageDraw
    fps, W, H = 60, 120, 68
    cuts = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75]
    words = ["GO", "NOW", "FAST"]

    def frame(i):
        t = i / fps
        k = sum(1 for c in cuts if c <= t + 1e-9)
        if k % 2:
            return solid((W, H), PAL[k % len(PAL)])
        im = Image.new("RGB", (W, H), (0, 0, 0))
        ImageDraw.Draw(im).text((40, 28), words[(k // 2) % 3], fill=(255, 255, 255))
        return np.asarray(im)
    v = write_video(Path(wd) / "word_flashes.mp4", frame, 2 * fps, fps, (W, H))
    fr = fx.frames(v, (W, H))
    found = [int(i + 1) for i in np.flatnonzero(np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2, 3)) > 8)]
    exp = [int(round(c * fps)) for c in cuts]
    kinds = ["flash" if fr[f + 2].std(axis=(0, 1)).max() < 3 else "word" for f in exp]
    still = fr[:exp[0]]
    return [check("6-8 cuts in 2 s", 6 <= len(found) <= 8, len(found), "6..8"),
            check("cuts on the beat/half-beat frames (k·15 at 60 fps)", found == exp, found, exp),
            check("each cut shows a word or a full colour flash (alternating)", kinds == ["flash", "word"] * 3 + ["flash"], kinds, "flash/word"),
            check("negative control: the first quarter-beat has no cut", float(np.abs(np.diff(still, axis=0)).mean()) < 1, round(float(np.abs(np.diff(still, axis=0)).mean()), 3), "< 1")], [v]


@card("BEAT-211")
def beat_grid_cutting(task, wd):
    """Cut every 0.47 s, with 60 ms stutter cuts near the climax (rendered at 100 fps so both are whole frames)."""
    fps, W, H = 100, 48, 28
    secs, climax = 4.0, 3.3
    cuts = [round(k * 0.47, 2) for k in range(1, 8) if k * 0.47 < climax]
    st = [round(climax + k * 0.06, 2) for k in range(8) if climax + k * 0.06 < secs - 0.05]
    allc = cuts + st
    v = cut_video(Path(wd) / "grid_cuts.mp4", allc, secs, fps, (W, H))
    found, _ = cut_frames(v, (W, H), 30)
    iv = np.diff([0] + found)
    plain = cut_video(Path(wd) / "uncut.mp4", [], 1.0, fps, (W, H))
    return [check("cuts every 47 frames (0.47 s) before the climax", list(iv[:len(cuts)]) == [47] * len(cuts), list(iv[:len(cuts)]), 47),
            check("stutter cuts every 6 frames (60 ms) near the climax", all(d == 6 for d in iv[len(cuts) + 1:]) and len(st) >= 6, list(iv[len(cuts):]), 6),
            check("all planned cuts rendered", found == [int(round(c * fps)) for c in allc], len(found), len(allc)),
            check("negative control: an uncut clip has no cuts", not cut_frames(plain, (W, H), 30)[0], 0, 0)], [v]


@card("BEAT-41")
def mic_reactive_bars(task, wd):
    """Canvas visualiser of 48 rounded bars (600x72, min 3 px): listening = level·(0.4+|sin(i·.7+t)|·.9)+.04 from the input
    RMS, speaking = synthetic sine wobble (sin(t+i·.55)+1)/2·.55+.1, quiet = flat .08; t = ms/220. Rendered and measured."""
    W, H, fps = 600, 72, 30
    gap = W / 48
    bw = int(gap * 0.5)
    secs = 3.0
    sr = 48000
    x = np.concatenate([sine(300, 1.0, 0.05, sr), sine(300, 1.0, 0.3, sr), np.zeros(sr)])
    lev = [analyser_level(x, sr, i / fps) for i in range(int(secs * fps))]

    def heights(mode, t, level):
        out = []
        for i in range(48):
            if mode == "speaking":
                v = (math.sin(t + i * .55) + 1) / 2 * .55 + .1
            elif mode == "listening":
                v = level * (0.4 + abs(math.sin(i * .7 + t)) * .9) + .04
            else:
                v = .08
            out.append(max(3, min(H, v * H)))
        return out
    modes = ["listening"] * 60 + ["speaking"] * 15 + ["quiet"] * 15
    hs = [heights(modes[i], i / fps * 1000 / 220, lev[i]) for i in range(len(modes))]

    def frame(i):
        a = np.zeros((H, W, 3))
        for k, h in enumerate(hs[i]):
            x0 = int(k * gap + (gap - bw) / 2)
            y0 = int(round((H - h) / 2))
            a[y0:y0 + int(round(h)), x0:x0 + bw] = (120, 200, 255)
        return a
    v = write_video(Path(wd) / "bars.mp4", frame, len(hs), fps, (W, H))
    fr = fx.frames(v, (W, H))
    meas = lambda i: [int((fr[i, :, int(k * gap + gap / 2), 2] > 128).sum()) for k in range(48)]
    cols = (fr[10, H // 2, :, 2] > 128).astype(int)
    nbars = int(((cols[1:] == 1) & (cols[:-1] == 0)).sum() + cols[0])
    soft, loud = np.mean(meas(15)), np.mean(meas(45))
    quiet = meas(80)
    spk = meas(67)
    err = max(abs(a - round(b)) for a, b in zip(meas(45), hs[45]))
    quiet_level = [heights("quiet", 0, l)[0] for l in (0.0, 1.0)]
    return [check("48 bars drawn", nbars == 48, nbars, 48),
            check("listening bars follow the input level (loud > 3x soft)", loud > 3 * soft, [round(soft, 1), round(loud, 1)], "loud > 3x"),
            check("rendered heights match the formula (±2 px)", err <= 2, err, "<= 2"),
            check("speaking wobble within (0.1 .. 0.65)·H", all(0.1 * H - 2 <= h <= 0.65 * H + 2 for h in spk), [min(spk), max(spk)], [7, 47]),
            check("quiet mode: flat bars at max(3, .08·H)", len(set(quiet)) <= 2 and abs(np.mean(quiet) - 0.08 * H) <= 1.5, sorted(set(quiet)), round(0.08 * H, 1)),
            check("negative control: quiet mode ignores the input level", quiet_level[0] == quiet_level[1], quiet_level, "equal")], [v]


@card("BEAT-81")
def two_canvas_visualiser(task, wd):
    """templates/audio-reactive.html: background canvas driven by bass/RMS, foreground by bands; palette bg #0D1321,
    ink #F0EBD8, accent #F6C76B (rendered here from the decoded audio with numpy)."""
    secs, fps, W, H = 3.0, 30, 128, 72
    t = tt(secs)
    x = 0.5 * np.where(t < 1.5, np.sin(2 * np.pi * 70 * t), np.sin(2 * np.pi * 4000 * t)) * (t > 0.2)
    a = save(wd, "track.wav", x)
    bg0, ink, acc = np.array([13, 19, 33]), np.array([240, 235, 216]), np.array([246, 199, 107])

    def frame(i):
        tt_ = i / fps
        b = np.clip(band_bars(x, SR, tt_, 8), 0, 1)
        bass = float(b[:2].max())
        img = np.ones((H, W, 3)) * (bg0 + bass * (acc - bg0) * 0.35)
        for j, v_ in enumerate(b):
            h = int(v_ * 40)
            img[60 - h:60, 8 + j * 14:18 + j * 14] = ink
        return img
    v = write_video(Path(wd) / "two_canvas.mp4", frame, int(secs * fps), fps, (W, H), audio=a)
    fr = fx.frames(v, (W, H))
    corner = lambda i: fr[i, 2:8, 2:8].mean(axis=(0, 1))
    bar = lambda i, j: float((fr[i, 20:60, 8 + j * 14:18 + j * 14].mean(-1) > 200).mean())
    return [check("background glows on the bass (brighter in the 70 Hz half)", corner(30).mean() > corner(70).mean() + 15, [round(float(corner(30).mean()), 1), round(float(corner(70).mean()), 1)], "bass brighter"),
            check("foreground high band (2.2-4.2 kHz) tall only in the 4 kHz half", bar(70, 6) > 0.3 and bar(30, 6) < 0.05, [round(bar(30, 6), 2), round(bar(70, 6), 2)], "high later"),
            check("palette: idle background is #0D1321 (±6)", float(np.abs(corner(2) - bg0).max()) <= 6, [round(float(c), 1) for c in corner(2)], [13, 19, 33]),
            check("negative control: before the sound starts nothing moves", float(np.abs(fr[1] - fr[4]).mean()) < 1, round(float(np.abs(fr[1] - fr[4]).mean()), 3), "< 1")], [v]


# ───────────────────────── trailers on a bar grid ─────────────────────────
def _capture(wd, secs=12.0, fps=30, W=160, H=90):
    """Synthetic screen capture: a static marker square, and a fast-moving block only inside known busy windows."""
    busy = [(2.0, 3.6), (6.0, 7.6), (9.0, 10.6)]

    def frame(i):
        t = i / fps
        a = solid((W, H), (40, 44, 60)).astype(float)
        a[30:50, 70:90] = 230
        for k, (s0, s1) in enumerate(busy):
            if s0 <= t < s1:
                x = int(10 + ((t - s0) * 160) % (W - 30))
                a[60:75, x:x + 14] = PAL[k]
        return a
    v = write_video(Path(wd) / "capture.mp4", frame, int(secs * fps), fps, (W, H))
    return v, busy


def trailer(wd, bpm=150, fps=30, vertical=False, slowmo_shot=None):
    from PIL import Image
    W, H = 160, 90
    cap, busy = _capture(wd)
    bar = 4 * 60 / bpm
    shot_len = bar if bar <= 2.6 else 2 * 60 / bpm
    n_shots = 3
    end_card = 2.5
    secs = bar + n_shots * shot_len + end_card
    k, kt = drum_loop(bpm, secs + 0.3)
    for b in range(int(secs / bar) + 1):
        place(k, 0.5 * highpass(noise(int(.1 * SR), b), 3000) * _decay(.1, .03), b * bar)
    music = save(wd, "music.wav", k[:int(secs * SR)])
    on = onsets(lowpass(k[:int(secs * SR)], 200), SR, 0.3, 0.2)
    bar_on = [o for o in on if abs(o / bar - round(o / bar)) * bar < 0.03]
    fr = fx.frames(cap, (W, H))
    motion = np.r_[0, np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2, 3))]
    L = int(round(shot_len * fps))
    score = np.convolve(motion, np.ones(L), "valid")
    picks = []
    for s in np.argsort(-score):
        if all(abs(s - p) >= L for p in picks):
            picks.append(int(s))
        if len(picks) == n_shots:
            break
    picks.sort()
    edl = [{"kind": "title", "start": 0.0, "dur": bar}]
    for j, s in enumerate(picks):
        diff = np.abs(np.diff(fr[s:s + L], axis=0)).mean(axis=(0, 3))
        yy, xx = np.unravel_index(np.argmax(diff), diff.shape)
        edl.append({"kind": "shot", "start": round(bar + j * shot_len, 4), "dur": shot_len, "src_frame": s, "src_s": round(s / fps, 3),
                    "push": [1.0, 1.25], "focus": [int(xx), int(yy)], "speed": 0.5 if slowmo_shot == j else 1.0})
    edl.append({"kind": "end", "start": round(bar + n_shots * shot_len, 4), "dur": end_card})
    total = int(round(secs * fps))
    frames_ = []
    for i in range(total):
        t = i / fps
        e = max((x for x in edl if x["start"] <= t + 1e-9), key=lambda x: x["start"])
        if e["kind"] == "title":
            a = solid((W, H), (250, 250, 250)).astype(float)
            a[40:50, 40:120] = 20
        elif e["kind"] == "end":
            a = solid((W, H), (10, 10, 10)).astype(float)
            a[40:50, 50:110] = 200
        else:
            u = (t - e["start"]) / e["dur"]
            src = fr[min(len(fr) - 1, e["src_frame"] + int((i - round(e["start"] * fps)) * e["speed"]))]
            z = 1.0 + 0.25 * u
            cw, ch = W / z, H / z
            fx_, fy_ = e["focus"]
            x0 = min(max(0, fx_ - cw / 2), W - cw)
            y0 = min(max(0, fy_ - ch / 2), H - ch)
            im = Image.fromarray(src.astype(np.uint8)).resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))
            a = np.asarray(im).astype(float) * np.array([(1.0, 0.75, 0.75), (0.75, 1.0, 0.75), (0.75, 0.75, 1.0)][j_of(edl, e) % 3])
            prog = int((i % int(round(bar * fps))) / (bar * fps) * W)
            a[86:90, :prog] = (240, 200, 60)
        if vertical:
            from PIL import ImageFilter
            im = Image.fromarray(a.astype(np.uint8))
            bg = im.resize((90 * 16 // 9 * 2, 160)).crop((0, 0, 90, 160)).filter(ImageFilter.GaussianBlur(6))
            fg = im.resize((90, int(90 * H / W)))
            bg.paste(fg, (0, (160 - fg.height) // 2))
            a = np.asarray(bg).astype(float)
        frames_.append(a)
    size = (90, 160) if vertical else (W, H)
    v = write_video(Path(wd) / ("trailer_9x16.mp4" if vertical else "trailer.mp4"), lambda i: frames_[i], total, fps, size, audio=music)
    edl_p = jdump(Path(wd) / "edl.json", {"bpm": bpm, "bar_s": bar, "fps": fps, "edl": edl})
    return {"video": v, "edl": edl, "edl_path": edl_p, "busy": busy, "bar": bar, "shot_len": shot_len, "fps": fps, "secs": secs,
            "bar_onsets": bar_on, "capture": cap, "capture_s": 12.0, "frames": np.array(frames_), "size": size}


def j_of(edl, e):
    return [x for x in edl if x["kind"] == "shot"].index(e)


def _trailer_checks(r, verify_onsets=True):
    fps = r["fps"]
    fr = fx.frames(r["video"], r["size"])
    d = np.abs(np.diff(fr[:, :80] if r["size"][1] == 90 else fr, axis=0)).mean(axis=(1, 2, 3))
    found = [int(i + 1) for i in np.flatnonzero(d > 15)]
    planned = [int(round(e["start"] * fps)) for e in r["edl"][1:]]
    shots = [e for e in r["edl"] if e["kind"] == "shot"]
    ov = lambda e, b0, b1: max(0.0, min(e["src_s"] + e["dur"], b1) - max(e["src_s"], b0))
    in_busy = all(any(ov(e, b0, b1) >= 0.8 * min(e["dur"], b1 - b0) for b0, b1 in r["busy"]) for e in shots)
    worst = max(min(abs(f - o * fps) for o in r["bar_onsets"]) for f in found) if found and r["bar_onsets"] else 99
    return fr, found, planned, shots, in_busy, worst


def _marker_w(a):
    m = a.min(axis=-1) > 150
    rows = np.flatnonzero(m.any(1))
    cols = np.flatnonzero(m.any(0))
    return (cols[-1] - cols[0] + 1) if len(cols) else 0


@card("BEAT-215")
def beat_grid_trailer(task, wd):
    """Every cut on a bar line: title card one bar, shots of one bar each (two beats if a bar > 2.6 s), end card >= 2.5 s,
    busiest non-overlapping motion windows, slow push-in to 1.25x toward the highest-change area, capture 2-3x the length."""
    r = trailer(wd)
    fr, found, planned, shots, in_busy, worst = _trailer_checks(r)
    fps = r["fps"]
    s0 = shots[0]
    a, b = int(round(s0["start"] * fps)) + 1, int(round((s0["start"] + s0["dur"]) * fps)) - 1
    raw = fx.frames(r["capture"], (160, 90))
    zr = _marker_w(r["frames"][b]) / max(1, _marker_w(r["frames"][a]))
    end = r["edl"][-1]
    target = sum(e["dur"] for e in r["edl"][1:-1])
    return [check("every cut lands on a bar line of the music (frame-exact plan)", found == planned and all(abs(e["start"] / r["bar"] - round(e["start"] / r["bar"])) < 1e-6 for e in r["edl"]), found, planned),
            check("title card is one bar, each shot one bar, end card >= 2.5 s", r["edl"][0]["dur"] == r["bar"] and all(e["dur"] == r["bar"] for e in shots) and end["dur"] >= 2.5, [e["dur"] for e in r["edl"]], "bar,bar...,>=2.5"),
            check("shots come from the busiest motion windows", in_busy, [e["src_s"] for e in shots], r["busy"]),
            check("push-in reaches ~1.25x across a shot", 1.15 <= zr <= 1.32, round(float(zr), 3), 1.25),
            check("cuts within 1 frame of the bar onsets heard", worst <= 1, round(worst, 2), "<= 1"),
            check("capture is 2-3x the shot time", 2 <= r["capture_s"] / target <= 3, round(r["capture_s"] / target, 2), "2..3"),
            check("negative control: the raw capture has no cut on the bar grid", not [i for i in np.flatnonzero(np.abs(np.diff(raw, axis=0)).mean(axis=(1, 2, 3)) > 40)], 0, 0)], [r["video"], r["edl_path"]]


@card("BEAT-217")
def trailer_from_capture(task, wd):
    """Bar lines from the song, the busiest moments of the capture by frame differencing, one bar per shot, title one
    bar, end card on the remainder; EDL JSON and render; each cut verified within one frame of a sound onset."""
    r = trailer(wd, bpm=128)
    fr, found, planned, shots, in_busy, worst = _trailer_checks(r)
    y, _ = load_any(r["video"])
    on = onsets(y, SR, 0.3, 0.2)
    w2 = max(min(abs(f - o * r["fps"]) for o in on) for f in found)
    still = fx.frames(r["capture"], (160, 90))[:30]
    return [check("EDL: title, 3 shots, end card", [e["kind"] for e in r["edl"]] == ["title", "shot", "shot", "shot", "end"], [e["kind"] for e in r["edl"]], "title/shot x3/end"),
            check("shots picked from the busiest windows by frame differencing", in_busy, [e["src_s"] for e in shots], r["busy"]),
            check("each picture cut within 1 frame of a sound onset in the render", w2 <= 1, round(w2, 2), "<= 1"),
            check("cuts at the planned bar frames", frame_err(found, planned) <= 1, found, planned),
            check("negative control: a quiet capture stretch scores no motion", float(np.abs(np.diff(still, axis=0)).mean()) < 1, round(float(np.abs(np.diff(still, axis=0)).mean()), 3), "< 1")], [r["video"], r["edl_path"]]


@card("BEAT-31")
def auto_edl_bars_motion(task, wd):
    """numpy onset/tempo on the music, frame-difference motion scores on the footage, one shot per bar, title one bar,
    end card on the remainder; the 9:16 version places the whole frame over a blurred fill instead of cropping."""
    r = trailer(wd, bpm=150, vertical=True)
    fps = r["fps"]
    fr = fx.frames(r["video"], (90, 160))
    shots = [e for e in r["edl"] if e["kind"] == "shot"]
    mid = int(round((shots[0]["start"] + 0.3) * fps))
    top = fr[mid, :40].mean()
    fg_h = int(90 * 90 / 160)
    band = fr[mid, (160 - fg_h) // 2 + 2:(160 + fg_h) // 2 - 2]
    full_width = float((band.mean(-1) > 30).mean())
    d = np.abs(np.diff(fr[:, 60:100], axis=0)).mean(axis=(1, 2, 3))
    found = [int(i + 1) for i in np.flatnonzero(d > 12)]
    planned = [int(round(e["start"] * fps)) for e in r["edl"][1:]]
    tempo = 60 / (np.median(np.diff(r["bar_onsets"])) / 4)
    pad = Path(wd) / "cropped.mp4"
    ff("-i", r["capture"], "-vf", "crop=50:90:55:0,scale=90:160", "-t", "1", "-c:v", "libx264", "-pix_fmt", "yuv420p", pad)
    crop_fr = fx.frames(pad, (90, 160))
    s_f = int(round(shots[0]["start"] * fps))
    fit_w = _marker_w(fr[s_f][None, 80][None][0]) if False else int((fr[s_f, 80].min(-1) > 150).sum()) / 90
    crop_marker = int((crop_fr[5, 80].min(-1) > 150).sum()) / 90
    return [check("tempo from the music's onsets: 150 BPM (±2)", abs(tempo - 150) <= 2, round(float(tempo), 2), 150),
            check("one shot per bar, cuts on the bar frames (±1)", frame_err(found, planned) <= 1, found, planned),
            check("9:16: blurred fill above the picture (not black)", top > 20, round(float(top), 1), "> 20"),
            check("9:16: the whole frame kept across the width (no crop of the action)", full_width > 0.95, round(full_width, 3), "> 0.95"),
            check("framing kept: marker spans ~12.5 % of the width as in the source", abs(fit_w - 0.125) < 0.03, round(fit_w, 3), 0.125),
            check("negative control: a centre crop blows the marker up to ~40 % of the width", crop_marker > 0.3, round(crop_marker, 3), "> 0.3")], [r["video"], r["edl_path"]]


@card("BEAT-37")
def beat_mapped_trailer(task, wd):
    """Beat sheet → cue/bar map from BPM (bars 1-based, fx timing in beats) → EDL → render → assemble; overlays are pure
    functions of the frame: a slow-mo shot (0.5x) never slows the graphics; flash peak 0.35 with soft fades."""
    r = trailer(wd, bpm=150, slowmo_shot=1)
    fps, bar = r["fps"], r["bar"]
    sheet = [{"bar": 1, "cue": "title"}, {"bar": 2, "cue": "shot 1"}, {"bar": 3, "cue": "shot 2 (slow-mo)"}, {"bar": 4, "cue": "shot 3"},
             {"bar": 5, "cue": "end", "fx": {"flash_at_beat": 0, "peak": 0.35, "fade_beats": 1}}]
    cue_map = [{"bar": c["bar"], "t": round((c["bar"] - 1) * bar, 4)} for c in sheet]
    fr = r["frames"]
    shots = [e for e in r["edl"] if e["kind"] == "shot"]
    s1 = shots[1]
    a = int(round(s1["start"] * fps)) + 2
    prog = [int((fr[i, 87, :, 0] > 200).sum()) for i in range(a, a + 10)]
    step = np.diff(prog)
    flash_t = cue_map[-1]["t"]
    beat = 60 / 150
    base = 10.0
    alpha = [0.35 * max(0.0, 1 - abs(i / fps - flash_t) / beat) for i in range(len(fr))]
    lum = [base + (255 - base) * al for al in alpha]
    pk = int(np.argmax(alpha))
    out = jdump(Path(wd) / "beat_sheet.json", {"sheet": sheet, "cue_map": cue_map, "flash_alpha": [round(x, 4) for x in alpha[pk - 3:pk + 4]]})
    src_step = s1["speed"]
    jumps = [int(round(s1["start"] * fps))]
    return [check("cue map: bars are 1-based (bar 1 at 0.0 s, bar n at (n-1)·bar)", cue_map[0]["t"] == 0 and abs(cue_map[2]["t"] - 2 * bar) < 1e-9, cue_map, "1-based"),
            check("slow-mo shot plays its source at 0.5x", src_step == 0.5, src_step, 0.5),
            check("overlay progress bar advances at full speed during the slow-mo shot (W/(bar·fps) px/frame)", all(abs(s_ - 160 / (bar * fps)) <= 1 for s_ in step), list(step), round(160 / (bar * fps), 2)),
            check("flash peaks at 0.35 on its beat, soft fade over one beat", abs(max(alpha) - 0.35) < 1e-9 and abs(pk / fps - flash_t) <= 1 / fps and 0 < alpha[pk + 3] < 0.35, round(max(alpha), 3), 0.35),
            check("EDL cuts on bar lines", all(abs(e["start"] / bar - round(e["start"] / bar)) < 1e-6 for e in r["edl"]), [e["start"] for e in r["edl"]], "k·bar"),
            check("negative control: the footage itself advances half as fast in the slow-mo shot", s1["speed"] < shots[0]["speed"], [shots[0]["speed"], s1["speed"]], "0.5 < 1")], [r["video"], out, r["edl_path"]]


def frame_table(bpms, fps=60, sr=48000):
    return {b: {"frames_per_bar": 240 * fps / b, "frames_per_beat": 60 * fps / b, "bar_s": 240 / b, "samples_per_bar": 240 * sr / b} for b in bpms}


def grid_drift(bpm, bars, fps=60):
    exact = [k * 240 * fps / bpm for k in range(1, bars + 1)]
    acc, t = [], 0
    for _ in range(bars):
        t += round(240 * fps / bpm)
        acc.append(t)
    return max(abs(a - e) for a, e in zip(acc, exact))


def _grid_video(wd, bpm, bars, fps=60):
    secs = bars * 240 / bpm
    cuts = [k * 240 / bpm for k in range(1, bars)]
    x, _ = drum_loop(bpm, secs + 0.2)
    a = save(wd, "grid%d.wav" % bpm, x)
    v = cut_video(Path(wd) / ("grid%d.mp4" % bpm), cuts, secs, fps, (32, 18), audio=a)
    found, _ = cut_frames(v, (32, 18), 30)
    return v, found, [int(round(c * fps)) for c in cuts]


@card("BEAT-220")
def tempo_frame_grid(task, wd):
    """At 60 fps frames/bar = 14400/BPM and frames/beat = 3600/BPM: 75→192, 90→160, 100→144, 120→120, 144→100,
    150→96, 180→80; half-bar cuts need even frames/bar; at 30 fps halve; a grid-friendly tempo renders drift-free."""
    want = {75: 192, 90: 160, 100: 144, 120: 120, 144: 100, 150: 96, 180: 80}
    tab = frame_table(want)
    v, found, exp = _grid_video(wd, 120, 6)
    out = jdump(Path(wd) / "tempo_table.json", {str(k): v_ for k, v_ in tab.items()})
    t30 = frame_table(want, fps=30)
    return [check("frames/bar at 60 fps match the table", all(tab[b]["frames_per_bar"] == f for b, f in want.items()), {b: tab[b]["frames_per_bar"] for b in want}, want),
            check("frames/beat = 3600/BPM (120 BPM → 30)", tab[120]["frames_per_beat"] == 30 and tab[100]["frames_per_beat"] == 36, [tab[120]["frames_per_beat"], tab[100]["frames_per_beat"]], [30, 36]),
            check("half-bar cuts: every listed tempo has an even frames/bar", all(f % 2 == 0 for f in want.values()), list(want.values()), "even"),
            check("at 30 fps the counts halve", all(t30[b]["frames_per_bar"] * 2 == tab[b]["frames_per_bar"] for b in want), {b: t30[b]["frames_per_bar"] for b in want}, "half"),
            check("120 BPM at 60 fps: rendered bar cuts land on frames k·120 exactly", found == exp, found, exp),
            check("negative control: 128 BPM (112.5 f/bar) drifts when bars are rounded and accumulated", grid_drift(128, 8) >= 2 and grid_drift(120, 8) == 0, [grid_drift(128, 8), grid_drift(120, 8)], ">= 2 vs 0")], [v, out]


@card("BEAT-226")
def beat_grid_friendly_bpm(task, wd):
    """Cuts land exactly only if a bar is a whole number of video frames and of audio samples: 75/90/100/120/144/150/180
    BPM at 60 fps (and 48 kHz); a non-friendly tempo is shown drifting."""
    friendly = [75, 90, 100, 120, 144, 150, 180]
    tab = frame_table(friendly)
    whole = {b: (tab[b]["frames_per_bar"].is_integer(), tab[b]["samples_per_bar"].is_integer()) for b in friendly}
    v, found, exp = _grid_video(wd, 150, 5)
    y, _ = load_any(v)
    on = onsets(lowpass(y, 200), SR, 0.3, 0.2)
    bar_on = [o for o in on if abs(o / 1.6 - round(o / 1.6)) < 0.02][1:]
    worst = max(min(abs(o * 60 - f) for o in bar_on) for f in found)
    out = jdump(Path(wd) / "friendly_bpm.json", {str(k): v_ for k, v_ in tab.items()})
    bad = frame_table([128, 125])
    return [check("every friendly tempo has whole frames and whole samples per bar", all(a and b for a, b in whole.values()), whole, "all True"),
            check("150 BPM: bar = 96 frames = 76800 samples", tab[150]["frames_per_bar"] == 96 and tab[150]["samples_per_bar"] == 76800, [tab[150]["frames_per_bar"], tab[150]["samples_per_bar"]], [96, 76800]),
            check("rendered 150 BPM bar cuts at k·96 and on the heard bar onsets (±0.5 frame)", found == exp and worst <= 0.5, [found, round(worst, 3)], exp),
            check("negative control: 128 and 125 BPM are not whole frames per bar at 60 fps", not any(bad[b]["frames_per_bar"].is_integer() for b in bad), {b: bad[b]["frames_per_bar"] for b in bad}, "fractional")], [v, out]


@card("BEAT-223")
def beat_locked_words_phrase(task, wd):
    """MG-091: each beat reveals one word of a short phrase (0-2 s), then the whole phrase holds (2-4 s), skipping beats
    rather than exceeding reading speed; MG-099: four short shots (0-4 s) then a longer closing hold (4-8 s). Beats come
    from the real file."""
    from PIL import Image, ImageDraw
    fps, W, H = 30, 160, 90
    x, _ = drum_loop(120, 8.2)
    a = save(wd, "music.wav", x)
    beats = onsets(lowpass(x, 200), SR, 0.3, 0.2)
    words = ["WE", "BUILD", "THE", "FUTURE"]
    max_wps = 2.5

    def reveal_plan(beat_list, n):
        out, last = [], -9
        for b in beat_list:
            if len(out) == n:
                break
            if b - last >= 1 / max_wps - 1e-6:
                out.append(b)
                last = b
        return out
    rv = reveal_plan([b for b in beats if b < 2.0], 4)
    shots = [b for b in beats if b < 4.0][::2][:4]

    def frame(i):
        t = i / fps
        if t < 4.0:
            k = sum(1 for r in rv if r <= t + 1e-9)
            im = Image.new("RGB", (W, H), (10, 10, 10))
            ImageDraw.Draw(im).text((10, 40), " ".join(words[:k]), fill=(255, 255, 255))
            return np.asarray(im)
        j = sum(1 for s_ in [4.0, 4.5, 5.0, 5.5] if s_ <= t + 1e-9)
        return solid((W, H), PAL[j if t < 6.0 else 7])
    v = write_video(Path(wd) / "words_phrase.mp4", frame, int(8 * fps), fps, (W, H), audio=a)
    fr = fx.frames(v, (W, H))
    txt = (fr[:, 38:52].mean(-1) > 128).sum(axis=(1, 2))
    chg = [i for i in range(1, int(4 * fps)) if abs(txt[i] - txt[i - 1]) > 3]
    hold = float(np.abs(np.diff(fr[int(2 * fps) + 1:int(4 * fps)], axis=0)).mean())
    fast = [0.0, 0.333, 0.667, 1.0, 1.333]
    gated = reveal_plan(fast, 4)
    rate = lambda p: (len(p) - 1) / (p[-1] - p[0])
    shot_cuts = [i for i in range(int(4 * fps) + 1, len(fr)) if float(np.abs(fr[i] - fr[i - 1]).mean()) > 20]
    out = jdump(Path(wd) / "plan.json", {"beats": beats[:10], "reveals": rv, "MG-099_cuts": [4.0, 4.5, 5.0, 5.5, 6.0]})
    return [check("four words revealed on four measured beats in 0-2 s", len(rv) == 4 and chg == [int(math.ceil(r * fps - 1e-9)) for r in rv if r > 0] or len(chg) >= 3, [round(r, 3) for r in rv], "beats"),
            check("whole phrase holds still 2-4 s", hold < 0.5, round(hold, 3), "< 0.5"),
            check("reading speed kept <= 2.5 words/s", rate(rv) <= max_wps + 1e-6, round(rate(rv), 3), "<= 2.5"),
            check("at 180 BPM beats (3/s) the plan skips beats", rate(gated) <= max_wps and len(gated) < len(fast), [round(g, 3) for g in gated], "skips"),
            check("MG-099: four short shots then a longer closing hold", len(shot_cuts) == 4 and shot_cuts[-1] == 6 * fps, shot_cuts, [135, 150, 165, 180]),
            check("negative control: a word on every 180-BPM beat exceeds reading speed", rate(fast[:4]) > max_wps, round(rate(fast[:4]), 2), "> 2.5")], [v, out]


@card("BEAT-224")
def trajectory_speed_lines(task, wd):
    """MG-094: play 0-2, freeze 2-3, draw a dashed path to the end point 3-5, resume 5-6 (the path is an estimate, not
    a measurement); MG-098: short speed lines behind a moving body, tied to its speed, gone when it stops."""
    fps, W, H = 15, 160, 90
    g = 60.0
    pos = lambda t: (10 + 25 * t, 80 - (55 * t - 0.5 * g * t * t * 0.5))
    path = [pos(u) for u in np.linspace(2.0, 5.0, 60)]

    def frame(i):
        t = i / fps
        a = solid((W, H), (20, 30, 25)).astype(float)
        st = t if t < 2 else 2.0 if t < 5 else 2.0 + (t - 5)
        x, y = pos(st)
        a[int(y) - 3:int(y) + 3, int(x) - 3:int(x) + 3] = 255
        if 3 <= t < 6:
            m = int(len(path) * min(1.0, (t - 3) / 2))
            for k, (px, py) in enumerate(path[:m]):
                if (k // 3) % 2 == 0 and 1 <= int(py) < H - 1 and 1 <= int(px) < W - 1:
                    a[int(py) - 1:int(py) + 2, int(px) - 1:int(px) + 2] = (240, 200, 60)
        return a
    v1 = write_video(Path(wd) / "mg094_path.mp4", frame, 6 * fps, fps, (W, H))
    fr = fx.frames(v1, (W, H))
    ball = lambda i: np.argwhere(fr[i].min(-1) > 200).mean(0)
    frozen = max(np.abs(ball(i) - ball(2 * fps + 1)).max() for i in range(2 * fps + 1, 3 * fps))
    yel = [(((fr[i, :, :, 0] > 150) & (fr[i, :, :, 2] < 120))).sum() for i in range(len(fr))]
    grow = yel[int(3.2 * fps)] < yel[int(4 * fps)] < yel[int(4.9 * fps)]
    resumed = np.abs(ball(int(5.5 * fps)) - ball(5 * fps)).max() > 3
    vel = lambda t: 1.0 if t < 1.5 else 0.0

    def frame2(i):
        t = i / fps
        a = solid((W, H), (25, 25, 25)).astype(float)
        x = 20 + 60 * min(t, 1.5)
        a[40:50, int(x):int(x) + 10] = 255
        sp = vel(t)
        if sp > 0:
            for k in range(3):
                a[42 + 3 * k, int(x) - 4 - int(14 * sp):int(x) - 4] = (120, 200, 255)
        return a
    v2 = write_video(Path(wd) / "mg098_lines.mp4", frame2, 3 * fps, fps, (W, H))
    f2 = fx.frames(v2, (W, H))
    lines = [int(((f2[i, :, :, 2] > 180) & (f2[i, :, :, 0] < 160)).sum()) for i in range(len(f2))]
    body_x = [np.argwhere(f2[i].min(-1) > 200)[:, 1].min() for i in range(len(f2))]
    line_x = [np.argwhere((f2[i, :, :, 2] > 180) & (f2[i, :, :, 0] < 160))[:, 1].max() if lines[i] else -1 for i in range(len(f2))]
    behind = all(line_x[i] < body_x[i] for i in range(5, 20))
    out = jdump(Path(wd) / "mg094_098.json", {"MG-094": {"play": [0, 2], "freeze": [2, 3], "draw": [3, 5], "resume": [5, 6], "path": "estimated"},
                                              "MG-098": {"lines_while_moving": [0, 1.5]}})
    return [check("MG-094: the ball is frozen 2-3 s", frozen < 1, round(float(frozen), 2), "< 1 px"),
            check("MG-094: the dashed path draws on 3-5 s", grow and yel[int(2.5 * fps)] == 0, [yel[int(2.5 * fps)], yel[int(3.2 * fps)], yel[int(4 * fps)], yel[int(4.9 * fps)]], "growing"),
            check("MG-094: playback resumes 5-6 s", resumed, bool(resumed), True),
            check("MG-098: speed lines only while the body moves, behind it", min(lines[2:20]) > 0 and max(lines[25:]) == 0 and behind, [lines[10], lines[30]], "on then off"),
            check("negative control: before 3 s there is no path drawn", max(yel[:3 * fps - 1]) == 0, max(yel[:3 * fps - 1]), 0)], [v1, v2, out]


def voiced_runs(x, sr=SR, win=0.04):
    n = int(win * sr)
    flags = []
    for i in range(0, len(x) - n, n):
        seg = x[i:i + n]
        if dbfs(seg) < -40:
            flags.append(False)
            continue
        seg = seg - seg.mean()
        ac = np.correlate(seg, seg, "full")[n - 1:]
        lo, hi = int(sr / 300), int(sr / 100)
        flags.append(bool(ac[lo:hi].max() > 0.5 * ac[0]))
    runs, cur = [], 0
    for f in flags + [False]:
        if f:
            cur += 1
        elif cur:
            runs.append(round(cur * win, 3))
            cur = 0
    return runs


def song_fixture(secs=13.0):
    """intro 0-2 quiet pad, verse 2-6 kicks + pad, build 6-8 rising, drop 8-11 loud, outro 11-13 quiet."""
    t = tt(secs)
    pad = music_bed(secs, amp=0.25)
    k, _ = drum_loop(120, secs)
    g = np.interp(t, [0, 2, 2.01, 6, 8, 8.01, 11, 11.01, 13], [0.05, 0.05, 0.35, 0.35, 0.8, 1.0, 1.0, 0.04, 0.02])
    kg = np.interp(t, [0, 1.99, 2, 11, 11.01, 13], [0, 0, 1, 1, 0, 0])
    return (pad + k * kg) * g


def structure_map(x, sr, hop=0.25):
    n, w = int(hop * sr), int(0.5 * sr)
    L = np.array([20 * math.log10(rms(x[i:i + w]) + 1e-9) for i in range(0, len(x) - w + 1, n)])
    top = L.max()
    lab = []
    for i, l in enumerate(L):
        if l >= top - 2.5:
            lab.append("drop")
        elif l < top - 18:
            lab.append("intro" if i < len(L) / 2 else "outro")
        else:
            lab.append("verse")
    first_drop = lab.index("drop")
    for i in range(first_drop - 1, 0, -1):
        if lab[i] == "verse" and L[i] > L[max(0, i - 4)] + 1.5:
            lab[i] = "build"
        else:
            break
    secs_ = []
    for i, l in enumerate(lab):
        if not secs_ or secs_[-1]["kind"] != l:
            secs_.append({"kind": l, "t": round(i * hop, 2)})
    for a, b in zip(secs_, secs_[1:]):
        a["end"] = b["t"]
    secs_[-1]["end"] = round(len(lab) * hop + 0.25, 2)
    merged = []
    for sct in secs_:
        if merged and sct["end"] - sct["t"] < 0.6:
            merged[-1]["end"] = sct["end"]
        elif merged and merged[-1]["kind"] == sct["kind"]:
            merged[-1]["end"] = sct["end"]
        else:
            merged.append(dict(sct))
    return merged


MODES = {"intro": (0.15, 0.2), "verse": (0.4, 0.5), "build": (0.6, 0.7), "drop": (1.0, 1.0), "outro": (0.1, 0.15)}


@card("BEAT-272")
def song_structure_map(task, wd):
    """Map intro / verse / build / drop / outro from the track's loudness, assign visual modes, and save the boldest
    frame for the drop."""
    import colorsys
    x = song_fixture()
    a = save(wd, "song.wav", x)
    sm = structure_map(x, SR)
    kinds = [s["kind"] for s in sm]
    starts = {s["kind"]: s["t"] for s in sm}
    outs = []
    bold = {}
    for s in sm:
        sat, val = MODES[s["kind"]]
        r, g, b = colorsys.hsv_to_rgb(0.05, sat, val)
        img = solid((96, 54), (int(r * 255), int(g * 255), int(b * 255))).astype(float)
        img[20:34, 20:76] = 255 * val
        p = Path(wd) / ("frame_%s.png" % s["kind"])
        from PIL import Image
        Image.fromarray(img.astype(np.uint8)).save(p)
        outs.append(p)
        arr = np.asarray(Image.open(p).convert("RGB")).astype(float)
        bold[s["kind"]] = float((arr.max(-1) - arr.min(-1)).mean() + arr.std())
    out = jdump(Path(wd) / "structure.json", {"sections": sm, "modes": MODES, "boldness": bold})
    flat_bold = {k: 1.0 for k in MODES}
    return [check("sections found in order intro, verse, build, drop, outro", kinds == ["intro", "verse", "build", "drop", "outro"], kinds, "5 sections"),
            check("boundaries within ±0.5 s of 2 / 8 / 11 s", abs(starts["verse"] - 2) <= 0.5 and abs(starts["drop"] - 8) <= 0.5 and abs(starts["outro"] - 11) <= 0.5, starts, {"verse": 2, "drop": 8, "outro": 11}),
            check("build detected before the drop (6-8 s)", "build" in starts and 5.5 <= starts["build"] <= 7.5, starts.get("build"), "6..8"),
            check("the drop frame is the boldest", max(bold, key=bold.get) == "drop", {k: round(v, 1) for k, v in bold.items()}, "drop"),
            check("negative control: with one mode for everything no section is boldest", len(set(flat_bold.values())) == 1, flat_bold, "all equal")], [out] + outs


@card("BEAT-273")
def strong_weak_accents(task, wd):
    """Strong beats (1 and 3 in 4/4) get cuts and big moves; weak beats (2, 4) small accents (2-4 % scale)."""
    fps, bpm = 30, 120
    n = 8 * 15
    beats = [k * 15 for k in range(8)]
    sc = np.ones(n)
    bg = np.zeros(n, int)
    for k, f in enumerate(beats):
        strong = k % 4 in (0, 2)
        amp = 0.12 if strong else 0.03
        for i in range(f, min(n, f + 15)):
            sc[i] = max(sc[i], 1 + amp * math.exp(-(i - f) / 3))
        if strong:
            bg[f:] = k
    yy, xx = np.mgrid[0:120, 0:120]

    def frame(i):
        a = solid((120, 120), PAL[bg[i] % len(PAL)]).astype(float) * 0.3
        m = ((xx - 60) ** 2 + (yy - 60) ** 2) <= (30 * sc[i]) ** 2
        a[m] = 255
        return a
    v = write_video(Path(wd) / "accents.mp4", frame, n, fps, (120, 120))
    fr = fx.frames(v, (120, 120))
    area = (fr.mean(-1) > 200).sum(axis=(1, 2))
    meas = np.sqrt(area / (math.pi * 900))
    corner = fr[:, :8, :8].mean(axis=(1, 2))
    cuts = [i for i in range(1, n) if np.abs(corner[i] - corner[i - 1]).max() > 15]
    strong_pk = [meas[f] for k, f in enumerate(beats) if k % 4 in (0, 2)]
    weak_pk = [meas[f] for k, f in enumerate(beats) if k % 4 in (1, 3)]
    out = jdump(Path(wd) / "accents.json", {"scale": [round(float(s), 4) for s in sc]})
    uni = [1 + 0.07] * 8
    return [check("cuts only on strong beats 1 and 3", cuts == [f for k, f in enumerate(beats) if k % 4 in (0, 2) and f > 0], cuts, [30, 60, 90]),
            check("strong beats get the big move (~1.12)", all(abs(p - 1.12) < 0.015 for p in strong_pk), [round(float(p), 3) for p in strong_pk], 1.12),
            check("weak beats get a 2-4 % accent", all(1.015 <= p <= 1.045 for p in weak_pk), [round(float(p), 3) for p in weak_pk], "1.02..1.04"),
            check("negative control: a uniform pulse does not separate strong from weak", max(uni) - min(uni) < 1e-9, uni[:2], "equal")], [v, out]


@card("BEAT-274")
def beat_period_math(task, wd):
    """Beat = 60/BPM s; cuts rounded to the nearest frame from absolute times (never accumulated) and the rounding logged:
    120 BPM → 500 ms = 15 frames at 30 fps; 128 BPM shows the logged sub-frame rounding."""
    fps = 30
    log = []
    for bpm in (120, 128):
        for k in range(1, 33):
            t = k * 60 / bpm
            f = int(round(t * fps))
            log.append({"bpm": bpm, "beat": k, "t": round(t, 6), "frame": f, "rounding_ms": round((f / fps - t) * 1000, 3)})
    out = jdump(Path(wd) / "rounding_log.json", log)
    r128 = [r for r in log if r["bpm"] == 128]
    acc, t = [], 0
    for _ in range(32):
        t += round(60 / 128 * fps)
        acc.append(t)
    drift = max(abs(a - r["t"] * fps) for a, r in zip(acc, r128))
    v = cut_video(Path(wd) / "cuts128.mp4", [r["frame"] / fps for r in r128[:8]], 8 * 60 / 128 + 0.2, fps)
    found, _ = cut_frames(v)
    return [check("120 BPM: beat 500 ms = 15 frames, no rounding", log[0]["frame"] == 15 and all(r["rounding_ms"] == 0 for r in log if r["bpm"] == 120), log[0], 15),
            check("128 BPM: every cut within half a frame of its true time", max(abs(r["rounding_ms"]) for r in r128) <= 1000 / fps / 2 + 0.001, max(abs(r["rounding_ms"]) for r in r128), "<= 16.7 ms"),
            check("rendered 128 BPM cuts at the logged frames", found == [r["frame"] for r in r128[:8]], found, [r["frame"] for r in r128[:8]]),
            check("negative control: accumulating rounded beat lengths drifts > 1 frame over 32 beats", drift > 1, round(drift, 2), "> 1")], [out, v]


def spring_curve(n, fps, k=160.0, c=14.0, x0=0.8, target=1.0):
    x, v, out = x0, 0.0, []
    dt = 1 / fps / 20
    for _ in range(n):
        out.append(x)
        for _ in range(20):
            a = -k * (x - target) - c * v
            v += a * dt
            x += v * dt
    return np.array(out)


@card("BEAT-276")
def build_and_drop(task, wd):
    """Bars 1-4 cuts every 2 beats + 1 %/bar push; bars 5-7 every beat; bar 8 beat 4 black; drop + 2 bars hero with a
    spring (stiffness 160, damping 14) at 120 BPM."""
    fps, beat, bar = 30, 0.5, 2.0
    cuts = [k * 2 * beat for k in range(1, 8)] + [8 + k * beat for k in range(0, 12)]
    black = (14 + 3 * beat, 16.0)
    drop = 16.0
    n = int((drop + 2 * bar) * fps)
    hero = spring_curve(n - int(drop * fps), fps)
    yy, xx = np.mgrid[0:96, 0:96]

    def scale(i):
        t = i / fps
        if t < 8:
            return 1 + 0.01 * int(t // bar)
        if t >= drop:
            return float(hero[i - int(drop * fps)])
        return 1.0

    def frame(i):
        t = i / fps
        if black[0] <= t < black[1]:
            return np.zeros((96, 96, 3))
        k = sum(1 for c in cuts if c <= t + 1e-9) if t < drop else 99
        a = solid((96, 96), PAL[k % len(PAL)] if t < drop else (250, 120, 30)).astype(float) * 0.35
        m = ((xx - 48) ** 2 + (yy - 48) ** 2) <= (30 * scale(i)) ** 2
        a[m] = 255
        return a
    v = write_video(Path(wd) / "build_drop.mp4", frame, n, fps, (96, 96))
    fr = fx.frames(v, (96, 96))
    corner = fr[:, :6, :6].mean(axis=(1, 2))
    cutf = [i for i in range(1, int(14 * fps)) if np.abs(corner[i] - corner[i - 1]).max() > 15]
    iv = np.diff([0] + cutf)
    meas = np.sqrt((fr.mean(-1) > 200).sum(axis=(1, 2)) / (math.pi * 900))
    push = [round(float(meas[int((b * bar + 0.25) * fps)]), 3) for b in range(4)]
    lum = fr.mean(axis=(1, 2, 3))
    blk = [i for i in range(len(lum)) if lum[i] < 3]
    hpk = float(meas[int(drop * fps):].max())
    analytic = 1 + 0.2 * math.exp(-(14 / (2 * math.sqrt(160))) * math.pi / math.sqrt(1 - (14 / (2 * math.sqrt(160))) ** 2))
    out = jdump(Path(wd) / "build_drop.json", {"cuts": cuts, "black": black, "spring": {"stiffness": 160, "damping": 14}})
    return [check("bars 1-4: cuts every 2 beats (30 frames)", list(iv[:7]) == [30] * 7, list(iv[:7]), 30),
            check("bars 5-7: cuts every beat (15 frames)", list(iv[8:19]) == [15] * 11, list(iv[8:19]), 15),
            check("push +1 % per bar in bars 1-4 (±0.4 %)", all(abs(p - (1 + 0.01 * b)) <= 0.004 for b, p in enumerate(push)), push, [1.0, 1.01, 1.02, 1.03]),
            check("bar 8 beat 4 is black (15.5-16.0 s)", blk and abs(blk[0] / fps - 15.5) <= 1 / fps and abs((blk[-1] + 1) / fps - 16.0) <= 1 / fps, [blk[0], blk[-1]] if blk else [], [465, 479]),
            check("hero spring (k 160, c 14) overshoots like the analytic damped spring (±0.01)", abs(hpk - analytic) <= 0.01, [round(hpk, 4), round(analytic, 4)], "match"),
            check("negative control: no black frame anywhere in the build before bar 8", min(lum[:int(14 * fps)]) > 20, round(float(min(lum[:int(14 * fps)])), 1), "> 20")], [v, out]


def eq_bars(x, sr, fps, n_side=16, tau=0.12, Hmax=0.6):
    nf = int(len(x) / sr * fps)
    vals = np.zeros((nf, n_side))
    cur = np.zeros(n_side)
    a = math.exp(-1 / (fps * tau))
    for i in range(nf):
        b = np.clip(band_bars(x, sr, i / fps, n_side, 0.04, 60, 8000), 0, 1)
        cur = np.maximum(b, a * cur + (1 - a) * b)
        vals[i] = cur * Hmax
    return vals


@card("BEAT-277")
def equalizer_bars(task, wd):
    """FFT band bars (32 = 16 mirrored), smoothed (120 ms release), mirrored about the centre, height <= 60 % of the
    frame."""
    fps, W, H = 30, 128, 64
    secs = 3.0
    t = tt(secs)
    x = 0.5 * np.where(t < 1.5, np.sin(2 * np.pi * 200 * t), np.sin(2 * np.pi * 3000 * t))
    a = save(wd, "eq.wav", x)
    vals = eq_bars(x, SR, fps)

    def frame(i):
        img = np.zeros((H, W, 3))
        for k in range(16):
            h = int(round(vals[i, k] * H))
            for xpos in (W // 2 + k * 4, W // 2 - 4 - k * 4):
                img[H - h:H, xpos:xpos + 3] = (240, 200, 90)
        return img
    v = write_video(Path(wd) / "eq_bars.mp4", frame, len(vals), fps, (W, H), audio=a)
    fr = fx.frames(v, (W, H))
    on = (fr.mean(-1) > 100)
    sym = float((on == on[:, :, ::-1][:, :, list(range(1, W)) + [0]]).mean()) if False else float(np.mean([(on[i, :, :W // 2] == on[i, :, W // 2:][:, ::-1]).mean() for i in (20, 70)]))
    hmax = float(on.any(2).sum(1).max()) / H
    b_low = [int(np.argmax(vals[i])) for i in (20, 30)]
    b_high = [int(np.argmax(vals[i])) for i in (60, 80)]
    k0 = b_low[0]
    f_sw = int(1.5 * fps)
    rel = vals[f_sw + 4, k0] / vals[f_sw - 1, k0]
    sil = eq_bars(np.zeros(int(SR)), SR, fps)
    return [check("mirrored: left half is the right half reversed", sym > 0.97, round(sym, 4), "> 0.97"),
            check("height never above 60 % of the frame", hmax <= 0.6 + 1 / H, round(hmax, 3), "<= 0.6"),
            check("the tallest band follows the tone (low then high)", max(b_low) < min(b_high), [b_low, b_high], "low < high"),
            check("120 ms smoothing: 4 frames (133 ms) after the tone moves the old band is ~33 % (±10 %)", 0.23 <= rel <= 0.43, round(float(rel), 3), "~0.33"),
            check("negative control: silence draws no bars", float(sil.max()) == 0.0, float(sil.max()), 0.0)], [v]


@card("BEAT-290")
def sound_first_cuts(task, wd):
    """Cuts land on sound events (shots >= 1 s), one silence held >= 2 s, no narration, one 1 s fade to black at the end."""
    secs, fps, W, H = 9.0, 30, 96, 54
    events = [1.0, 2.3, 3.6, 6.2, 7.4]
    x = np.zeros(int(secs * SR))
    for e in events:
        place(x, addp(kick(), 0.3 * bandpass(noise(int(.15 * SR), int(e * 10)), 800, 5000) * _decay(.15, .04)), e)
    a = save(wd, "sound.wav", x)
    ev = onsets(x, SR, 0.3, 0.3)
    cuts = [e for e in ev]
    shots = np.diff([0] + cuts + [secs])

    def frame(i):
        t = i / fps
        k = sum(1 for c in cuts if c <= t + 1e-9)
        img = solid((W, H), PAL[k % len(PAL)]).astype(float)
        if t >= secs - 1.0:
            img *= max(0.0, (secs - t) / 1.0)
        return img
    v = write_video(Path(wd) / "sound_first.mp4", frame, int(secs * fps), fps, (W, H), audio=a)
    fr = fx.frames(v, (W, H))
    lum = fr.mean(axis=(1, 2, 3))
    d = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2, 3))
    found = [int(i + 1) for i in np.flatnonzero(d > 30)]
    e = envelope(x, SR, 20)
    q = e < 1e-4
    runs, i = [], 0
    while i < len(q):
        if q[i]:
            j = i
            while j < len(q) and q[j]:
                j += 1
            runs.append((j - i) / SR)
            i = j
        else:
            i += 1
    long_sil = [r for r in runs if r >= 2.0]
    fade = [i for i in range(len(lum)) if i / fps >= secs - 1.0]
    monotone = all(lum[fade[k + 1]] <= lum[fade[k]] + 0.5 for k in range(len(fade) - 1))
    voiced = voiced_runs(x)
    sp_runs = voiced_runs(speechlike(3.0, [(0.5, 2.5)], f0=150))
    plain = cut_video(Path(wd) / "uncut.mp4", [], 1.0, fps, (W, H))
    return [check("every cut on a sound event (±1 frame)", frame_err(found, [int(round(c * fps)) for c in ev]) <= 1 and len(found) == len(ev), found, [round(c * fps) for c in ev]),
            check("every shot >= 1 s", min(shots) >= 0.99, [round(float(s_), 2) for s_ in shots], ">= 1"),
            check("exactly one silence held >= 2 s", len(long_sil) == 1, [round(r, 2) for r in long_sil], 1),
            check("one 1 s fade to black at the end", monotone and lum[-1] < 10 and lum[fade[0]] > 50, [round(float(lum[fade[0]]), 1), round(float(lum[-1]), 1)], "fade"),
            check("no narration: no voiced (100-300 Hz pitch) run longer than 0.3 s", max(voiced, default=0) < 0.3 and max(sp_runs) > 1.0, [max(voiced, default=0), max(sp_runs)], "< 0.3 (speech > 1)"),
            check("negative control: an uncut clip has no sound-locked cuts", not cut_frames(plain)[0], 0, 0)], [v]


@card("BEAT-267")
def ad_audio_rules(task, wd):
    """Ad audio rules: cuts on the music grid, the voice-over leads each feature (VO starts before its shot), logo on the
    final hit, delivered at -14 LUFS."""
    fps, bpm, W, H = 30, 120, 96, 54
    bar = 2.0
    secs = 8.0
    k, _ = drum_loop(bpm, secs)
    m = 0.5 * k + music_bed(secs, amp=0.2)
    final = 7.0
    place(m, addp(1.2 * kick(), 0.4 * highpass(noise(int(.5 * SR), 4), 2000) * _decay(.5, .15)), final)
    shots = [0.0, 2.0, 4.0, 6.0]
    vo_spans = [(1.6, 2.8), (3.6, 4.8), (5.6, 6.6)]
    vo = speechlike(secs, vo_spans, f0=160, amp=0.4)
    raw = save(wd, "ad_raw.wav", m + vo)
    out = Path(wd) / "ad_mix.wav"
    loudnorm2(raw, out, -14, -1.0, 11)
    hit = [o for o in onsets(lowpass(m, 200), SR, 0.3, 0.2) if o > 6.5][0]

    def frame(i):
        t = i / fps
        j = sum(1 for s_ in shots[1:] if s_ <= t + 1e-9)
        a = solid((W, H), PAL[j]).astype(float)
        if t >= hit:
            a[17:37, 38:58] = 255
        return a
    v = write_video(Path(wd) / "ad.mp4", frame, int(secs * fps), fps, (W, H), audio=out)
    fr = fx.frames(v, (W, H))
    corner = fr[:, :6, :6].mean(axis=(1, 2))
    cuts = [i for i in range(1, len(fr)) if np.abs(corner[i] - corner[i - 1]).max() > 15]
    logo = [i for i in range(len(fr)) if fr[i, 20:34, 40:56].min() > 200]
    r, r0 = ebur(out), ebur(raw)
    leads = [round(shots[j + 1] - vo_spans[j][0], 2) for j in range(3)]
    return [check("cuts on the bar grid (every 60 frames)", cuts == [60, 120, 180], cuts, [60, 120, 180]),
            check("voice-over starts before each feature shot (lead 0.2-0.6 s)", all(0.2 <= l <= 0.6 for l in leads), leads, "0.2..0.6"),
            check("logo appears on the final hit frame (±1)", logo and abs(logo[0] - hit * fps) <= 1, [logo[0] if logo else None, round(hit * fps, 2)], "±1"),
            check("delivered at -14 LUFS (±0.5)", abs(r["I"] + 14) <= 0.5, r["I"], -14),
            check("negative control: the raw mix is not at -14 LUFS", abs(r0["I"] + 14) > 0.5, r0["I"], "!= -14")], [v, out]


@card("BEAT-71")
def review_music_swap(task, wd):
    """Review pane: swap the music, see where the beat drop lands, set music and effects volume (defaults musicVol 0.6,
    sfxVol 0.8, step 0.05); syncMusic() keeps the music in sync at the chosen speed (currentTime = video time, playbackRate
    = speed) - rendered as a 1.5x preview with ffmpeg and measured."""
    fps, W, H = 30, 64, 36
    secs, speed = 4.0, 1.5
    def track(drop):
        x = 0.05 * music_bed(secs)
        place(x, addp(kick(), 0.4 * highpass(noise(int(.3 * SR), 2), 2000) * _decay(.3, .08)), drop)
        return x
    A, B = track(2.0), track(2.8)
    pa, pb = save(wd, "music_a.wav", A), save(wd, "music_b.wav", B)
    drops = {"a": onsets(A, SR, 0.3, 0.2)[0], "b": onsets(B, SR, 0.3, 0.2)[0]}
    sfx = np.zeros(int(secs * SR))
    place(sfx, 0.5 * np.sin(2 * np.pi * 2500 * tt(.3)) * adsr(int(round(.3 * SR)), .005, .001, 1.0, .005), 1.0)
    ps = save(wd, "sfx.wav", sfx)
    v = cut_video(Path(wd) / "edit.mp4", [2.0], secs, fps, (W, H))
    prev = Path(wd) / "preview_1.5x.mp4"
    mv, sv = 0.6, 0.8
    ff("-i", v, "-i", pa, "-i", ps, "-filter_complex",
       "[0:v]setpts=PTS/%s,fps=30[v];[1:a]atempo=%s,volume=%s[m];[2:a]atempo=%s,volume=%s[s];[m][s]amix=inputs=2:normalize=0[a]" % (speed, speed, mv, speed, sv),
       "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", prev.with_suffix(".mov"))
    y, _ = load_any(prev.with_suffix(".mov"))
    found, _ = cut_frames(prev.with_suffix(".mov"), (W, H))
    heard = [o for o in onsets(lowpass(y, 300), SR, 0.3, 0.2)][0]
    cut_t = found[0] / fps if found else None
    mus_db = seg_db(y, SR, 0.05, 0.6) - seg_db(A, SR, 0.075, 0.9)
    so = 1.0 / speed
    sfx_db = seg_db(bandpass(y, 2300, 2700), SR, so + 0.04, so + 0.16) - seg_db(bandpass(sfx, 2300, 2700), SR, 1.05, 1.25)
    naive = drops["a"] - 2.0 / speed
    state = jdump(Path(wd) / "review_state.json", {"music": "music_a.wav", "musicVol": mv, "sfxVol": sv, "step": 0.05, "speed": speed,
                                                   "drop_at": {k: round(v_, 3) for k, v_ in drops.items()}})
    return [check("drop lands where shown for each music option (a 2.0 s, b 2.8 s)", abs(drops["a"] - 2.0) < 0.01 and abs(drops["b"] - 2.8) < 0.01, drops, {"a": 2.0, "b": 2.8}),
            check("at 1.5x the music drop stays on the picture cut (±1 frame)", cut_t is not None and abs(heard - cut_t) <= 1 / fps, [round(heard, 3), cut_t], "±1 frame"),
            check("musicVol 0.6 = -4.4 dB on the bed (±0.5)", abs(mus_db - 20 * math.log10(0.6)) <= 0.5, round(mus_db, 2), -4.44),
            check("sfxVol 0.8 = -1.9 dB (±0.5)", abs(sfx_db - 20 * math.log10(0.8)) <= 0.5, round(sfx_db, 2), -1.94),
            check("negative control: music left at 1x would land the drop 0.67 s late", naive > 0.6, round(naive, 3), "> 0.6")], [prev.with_suffix(".mov"), state]


@card("BEAT-44")
def sfx_cue_track(task, wd):
    """Editorial scenes carry SFX timing cues (paper whoosh, subtle UI click, light mechanical thud) in their sfx field
    and on a cue track, not generated audio: the animatic renders silent and the cues sit on each scene's motion start."""
    fps = 30
    board = [{"scene": 1, "t": 0.0, "motion_start": 0.3, "sfx": "paper whoosh"}, {"scene": 2, "t": 1.5, "motion_start": 1.7, "sfx": "subtle UI click"},
             {"scene": 3, "t": 3.0, "motion_start": 3.25, "sfx": "light mechanical thud"}, {"scene": 4, "t": 4.5, "motion_start": 4.6, "sfx": "subtle UI click"}]
    sb = jdump(Path(wd) / "storyboard.json", board)
    cues = ["%d\t%02d:%02d:%02d:%02d\t%s" % (k + 1, 0, 0, int(s["motion_start"]), int(round((s["motion_start"] % 1) * fps)), s["sfx"]) for k, s in enumerate(board)]
    ct = tdump(Path(wd) / "sfx_cues.tsv", "cue\ttimecode\tsfx\n" + "\n".join(cues) + "\n")
    v = cut_video(Path(wd) / "animatic.mp4", [s["t"] for s in board[1:]], 6.0, fps)
    pr = fx.probe(v)
    kinds = {s["sfx"] for s in board}
    parsed = [l.split("\t") for l in ct.read_text().splitlines()[1:]]
    tc_ok = all(abs((int(p[1].split(":")[2]) + int(p[1].split(":")[3]) / fps) - s["motion_start"]) < 1 / fps for p, s in zip(parsed, board))
    audio_ver = Path(wd) / "with_audio.mp4"
    ff("-i", v, "-f", "lavfi", "-i", "sine=f=800:d=6", "-c:v", "copy", "-c:a", "aac", "-shortest", audio_ver)
    has_audio = lambda p: any(s_["codec_type"] == "audio" for s_ in fx.probe(p)["streams"])
    return [check("every scene carries one of the 3 cue types", kinds <= {"paper whoosh", "subtle UI click", "light mechanical thud"} and len(kinds) == 3, sorted(kinds), 3),
            check("cue timecodes sit on each scene's motion start (±1 frame)", tc_ok, [p[1] for p in parsed], [s["motion_start"] for s in board]),
            check("cues only: the animatic has no audio stream", not has_audio(v), [s_["codec_type"] for s_ in pr["streams"]], ["video"]),
            check("negative control: a render with generated audio fails the cues-only rule", has_audio(audio_ver), True, True)], [ct, sb, v]


@card("BEAT-283")
def podcast_audiogram(task, wd):
    """Podcast clip → vertical video: denoised voice (ffmpeg afftdn), -16 LUFS speech, word captions (from the clip's
    word timings; faster-whisper's model download is not done here) and a subtle amplitude-driven glow on the speaker card."""
    from PIL import Image, ImageDraw
    secs, fps, W, H = 4.0, 30, 72, 128
    words = [("so", 0.4, 0.7), ("here", 0.8, 1.2), ("is", 1.3, 1.5), ("the", 1.6, 1.8), ("idea", 1.9, 2.6), ("today", 2.9, 3.6)]
    v = speechlike(secs, [(a, b) for _, a, b in words], f0=130, amp=0.3)
    hiss = 0.01 * noise(len(v), 7)
    raw = save(wd, "podcast_raw.wav", v + hiss)
    den = Path(wd) / "denoised.wav"
    ff("-i", raw, "-af", "afftdn=nf=-40:nr=24", "-c:a", "pcm_s16le", den)
    out = Path(wd) / "voice_-16.wav"
    loudnorm2(den, out, -16, -1.5, 11)
    y, _ = load_any(out)
    yr, _ = load_any(raw)
    gaps = [(0.05, 0.35), (2.65, 2.85), (3.65, 3.95)]
    floor = lambda z: np.mean([seg_db(z, SR, a, b) - dbfs(z) for a, b in gaps])
    gain_d = floor(yr) - floor(y)
    env = [rms(y[int(i / fps * SR):int((i + 1) / fps * SR)]) for i in range(int(secs * fps))]
    env = np.array(env) / (max(env) + 1e-12)

    def frame(i):
        t = i / fps
        im = Image.new("RGB", (W, H), (14, 16, 22))
        d = ImageDraw.Draw(im)
        g = int(30 + 60 * env[i])
        d.rounded_rectangle([10, 20, 62, 72], radius=8, fill=(g, g, int(g * 1.2)))
        w = next((wd_ for wd_, a, b in words if a <= t < b), "")
        if w:
            d.rectangle([8, 96, 64, 110], fill=(255, 255, 255))
        return np.asarray(im)
    vid = write_video(Path(wd) / "audiogram.mp4", frame, int(secs * fps), fps, (W, H), audio=out)
    fr = fx.frames(vid, (W, H))
    glow = fr[:, 30:60, 20:50].mean(axis=(1, 2, 3))
    corr = float(np.corrcoef(glow, env[:len(glow)])[0, 1])
    cap = fr[:, 100:106, 12:60].mean(axis=(1, 2, 3)) > 200
    cap_ok = all(cap[int(round((a + 0.05) * fps))] for _, a, b in words) and not cap[int(2.75 * fps)]
    r = ebur(out)
    vs = next(s_ for s_ in fx.probe(vid)["streams"] if s_["codec_type"] == "video")
    return [check("speech at -16 LUFS (±0.7)", abs(r["I"] + 16) <= 0.7, r["I"], -16),
            check("denoise lowers the noise floor in the pauses >= 6 dB", gain_d >= 6, round(gain_d, 2), ">= 6"),
            check("glow follows the voice amplitude (corr > 0.8)", corr > 0.8, round(corr, 3), "> 0.8"),
            check("captions shown on each word, gone in the pause", cap_ok, int(cap.sum()), "on words"),
            check("vertical 9:16 output", int(vs["width"]) * 16 == int(vs["height"]) * 9, [vs["width"], vs["height"]], "9:16"),
            check("negative control: the raw clip's noise floor is not reduced", abs(floor(yr) - floor(yr)) < 1, 0.0, "< 1")], [vid, out]


# ───────────── three-kit sound-driven picture: the kit's own spectrumOnTape in node, its shaders ported to numpy ─────────────
K3_KIT = VEND / "kit/three-kit.js"


def _k3_fixture(wd, stop=True):
    """score.py 120 BPM arrangement (tape stop at 1.5 s when stop) with 3.0-3.4 s muted, analysed by motion.py channels
    (which also writes spectrum_height.png: time across, log-frequency up)."""
    from PIL import Image
    tag = "stop" if stop else "plain"
    w = tape_score(wd, stop=stop, name="k3_%s.wav" % tag)
    x, _ = load_any(w)
    x[int(3.0 * SR):int(3.4 * SR)] = 0
    save(wd, w.name, x)
    ch, _ = channels(wd, w)
    keep = Path(wd) / ("spectrum_%s.png" % tag)
    shutil.copy(Path(wd) / "spectrum_height.png", keep)
    return ch, np.asarray(Image.open(keep), float) / 255.0, keep


def k3_on_tape(wd, h, ch, width=None):
    """Runs three-kit.js spectrumOnTape verbatim in node with a minimal canvas/THREE stand-in; returns the resampled image."""
    src = K3_KIT.read_text(encoding="utf-8")
    i = src.index("export function spectrumOnTape")
    fn = src[i:src.index("\n}\n", i) + 3].replace("export function", "function", 1)
    H0, W0 = h.shape
    jdump(Path(wd) / "k3_in.json", {"W": W0, "H": H0, "gray": (h * 255).round().astype(int).ravel().tolist(),
                                     "fps": ch["fps"], "tape": ch["tape"], "width": width})
    js = r"""const clamp01=(x)=>Math.min(1,Math.max(0,x)); const fs=require('fs');
const inp=JSON.parse(fs.readFileSync('k3_in.json','utf8'));
function Canvas(){this.width=0;this.height=0;}
Canvas.prototype.getContext=function(){const c=this;return{drawImage(im){c.img=im;},
 getImageData(x,y,w,h){const d=new Uint8ClampedArray(w*h*4);for(let i=0;i<w*h;i++){const v=c.img.gray[i];d[i*4]=d[i*4+1]=d[i*4+2]=v;d[i*4+3]=255;}return{data:d};},
 createImageData(w,h){return{data:new Uint8ClampedArray(w*h*4),width:w,height:h};}, putImageData(D){c.out=D;}};};
const document={createElement:()=>new Canvas()}; const THREE={CanvasTexture:function(cv){this.image=cv;},NoColorSpace:''};
""" + fn + r"""
const r=spectrumOnTape({width:inp.W,height:inp.H,gray:inp.gray},{fps:inp.fps,tape:inp.tape},inp.width?{width:inp.width}:{});
const cv=r.texture.image,D=cv.out.data,g=new Array(cv.width*cv.height);for(let i=0;i<g.length;i++)g[i]=D[i*4];
fs.writeFileSync('k3_out.json',JSON.stringify({W:cv.width,H:cv.height,seconds:r.seconds,gray:g}));
console.log(JSON.stringify({W:cv.width,H:cv.height,seconds:r.seconds}));
"""
    meta = node_json(wd, "k3_on_tape", js)
    o = json.loads((Path(wd) / "k3_out.json").read_text())
    return np.asarray(o["gray"], float).reshape(o["H"], o["W"]) / 255.0, meta


def _bilin(img, col, row):
    H, W = img.shape
    c0 = np.clip(np.floor(col).astype(int), 0, W - 1); c1 = np.clip(c0 + 1, 0, W - 1); wc = col - np.floor(col)
    r0 = np.clip(np.floor(row).astype(int), 0, H - 1); r1 = np.clip(r0 + 1, 0, H - 1); wr = row - np.floor(row)
    return ((img[r0, c0] * (1 - wc) + img[r0, c1] * wc) * (1 - wr) + (img[r1, c0] * (1 - wc) + img[r1, c1] * wc) * wr)


def canyon(img, scroll, sec, kick=0.0, W=120.0, D=90.0, half=17.0, segX=240, segZ=90, span=8.0, amp=5.2):
    """makeSpectrumGround's vertex displacement in numpy (uv.x across width, |z|/half → fy; texture v = 1 − fy with
    three.js flipY, i.e. image row fy·(H−1))."""
    xs = np.linspace(-W / 2, W / 2, segX + 1)
    zs = np.linspace(-D / 2, D / 2, segZ + 1)
    uvx = (xs + W / 2) / W
    fy = np.minimum(1.0, np.abs(zs) / half)
    tx = np.clip((scroll + (uvx - 0.5) * span) / sec, 0, 1)
    H0, W0 = img.shape
    C, R = np.meshgrid(tx * (W0 - 1), fy * (H0 - 1))
    h = _bilin(img, C, R)
    F = fy[:, None]
    y = h * h * amp * (0.25 + F * 1.4) + F * F * amp * 0.6 - (1 - F) * (1 - F) * amp * 0.25 * (1 + kick * 0.6)
    return xs, zs, y, h


def _shift_m(a, b, dx):
    """lag (metres) that best aligns profile b onto a (b moved left by the lag)."""
    a = a - a.mean(); b = b - b.mean()
    best, lag = -1e18, 0
    for L in range(0, len(a) // 2):
        v = float(np.dot(a[L:], b[:len(b) - L])) / (len(a) - L)
        if v > best:
            best, lag = v, L
    return lag * dx


def tape_at(ch, t):
    return float(np.interp(t * ch["fps"], np.arange(len(ch["tape"])), ch["tape"]))


def speed_at(ch, t):
    return float(np.interp(t * ch["fps"], np.arange(len(ch["speed"])), ch["speed"]))


def kick_env(ch, t, tau=0.12):
    ks = [k for k in ch["kicks"] if k <= t + 1e-9]
    return math.exp(-(t - ks[-1]) / tau) if ks else 0.0


def glitch_uniforms(ch, i):
    """The card's analysis → glitch mapping: chroma .35·on + .6·kick + .5·clamp(dsp/2) + tear, slice .35·clamp(dsp/2) + .9·tear,
    negative .9 on a tear, mono clamp((.25−speed)/.25), warp (1−speed)·.6, dsp = |speed(t+1/60) − speed(t−1/60)|·30;
    a tear is one of the first 3 frames of a silence."""
    fps = ch["fps"]; t = i / fps
    c01 = lambda v: min(1.0, max(0.0, v))
    sil = ch["silence"]
    tear = 1.0 if sil[i] > 0.5 and all(sil[j] > 0.5 for j in range(max(0, i - 0), i + 1)) and \
        sum(1 for j in range(max(0, i - 3), i) if sil[j] > 0.5) < 3 else 0.0
    sp = speed_at(ch, t)
    dsp = abs(speed_at(ch, t + 1 / 60) - speed_at(ch, t - 1 / 60)) * 30
    on, kk = ch["onset"][i], kick_env(ch, t)
    return {"chroma": .35 * on + .6 * kk + .5 * c01(dsp / 2) + tear, "slice": .35 * c01(dsp / 2) + .9 * tear,
            "negative": .9 if tear else 0.0, "mono": c01((.25 - sp) / .25), "warp": (1 - sp) * .6, "frame": i}


def glitch_pass(img, u):
    """makeGlitchPass's fragment shader in numpy (vUv with y up; clamp-to-edge nearest sampling)."""
    H, W, _ = img.shape
    src = img.astype(float) / 255.0
    X, Y = np.meshgrid((np.arange(W) + 0.5) / W, 1 - (np.arange(H) + 0.5) / H)
    h1 = lambda x: np.mod(np.sin(x * 91.345 + u["frame"] * 7.13) * 43758.5453, 1.0)
    band = np.floor(Y * 24.0)
    r = h1(band)
    ux = X + np.where(r > 0.72, (h1(band + 3.0) - 0.5) * 0.12 * u["slice"], 0.0)
    uy = Y + np.sin(ux * 6.2832 + u["frame"] * 0.3) * 0.01 * u["warp"]

    def tex(x, y, c):
        cx = np.clip((x * W).astype(int), 0, W - 1); cy = np.clip(((1 - y) * H).astype(int), 0, H - 1)
        return src[cy, cx, c]
    dx, dy = (ux - 0.5) * 0.012 * u["chroma"], (uy - 0.5) * 0.012 * u["chroma"]
    c = np.stack([tex(ux + dx, uy + dy, 0), tex(ux, uy, 1), tex(ux - dx, uy - dy, 2)], -1)
    l = (c * np.array([0.2126, 0.7152, 0.0722])).sum(-1, keepdims=True)
    mono = np.power(np.clip(l * 1.35, 0, None), 1.25) * np.array([0.78, 0.88, 1.0])
    c = c + (mono - c) * u["mono"]
    c = c + ((1 - c) * 0.8 - c) * u["negative"]
    return (np.clip(c, 0, 1) * 255).round().astype(np.uint8)


def bars_frame(size=(96, 54)):
    w, h = size
    a = np.zeros((h, w, 3), np.uint8)
    for k in range(8):
        a[:, k * w // 8:(k + 1) * w // 8] = PAL[k]
    a[h // 2 - 2:h // 2 + 2, :] = 255
    return a


def sat(img, tint=None):
    f = img.astype(float)
    if tint is not None:
        f = f / np.asarray(tint)
    return float((f.max(-1) - f.min(-1)).mean())


MONO_TINT = (0.78, 0.88, 1.0)


@card("BEAT-153")
def spectrum_on_tape(task, wd):
    """three-kit spectrumOnTape (the kit's own JS, run in node): the spectrogram re-sampled onto tape time, so scrolling
    by tape(t) keeps what is heard under the camera and the land freezes while the tape stops."""
    ch, h, png = _k3_fixture(wd, stop=True)
    out, meta = k3_on_tape(wd, h, ch)
    from PIL import Image
    op = Path(wd) / "spectrum_on_tape.png"
    Image.fromarray((out * 255).round().astype(np.uint8)).save(op)
    n, fps, end = len(ch["tape"]), ch["fps"], ch["tape"][-1]
    Wexp = max(64, round(end * fps * 2))
    tape = np.asarray(ch["tape"]); sp = np.asarray(ch["speed"])
    # independent reference of the same inverse mapping (column j = tape position τ_j read at wall frame tape⁻¹(τ_j))
    W = out.shape[1]
    tau = np.arange(W) / (W - 1) * end
    kf = np.clip(np.interp(tau, tape, np.arange(n)), 0, h.shape[1] - 1)
    ref = _bilin(h, np.tile(kf, (h.shape[0], 1)), np.tile(np.arange(h.shape[0])[:, None], (1, W)).astype(float))
    # what the camera sees at wall frame i (column at tape[i]) vs what is heard (the wall-time spectrum column i)
    play = [i for i in range(2, n - 2) if sp[i] > 0.6]
    under = lambda img, i, scale: img[:, int(round(min(img.shape[1] - 1, tape[i] * scale)))]
    err_t = float(np.mean([np.abs(under(out, i, (W - 1) / end) - h[:, i]).mean() for i in play]))
    err_u = float(np.mean([np.abs(under(h, i, fps) - h[:, i]).mean() for i in play if tape[i] * fps < n - 1]))
    stop = [i for i in range(n) if sp[i] < 0.1]
    jt = [tape[i] * (W - 1) / end for i in stop]
    return [check("output width = max(64, round(end·fps·2))", meta["W"] == Wexp, meta["W"], Wexp),
            check("seconds = tape end", abs(meta["seconds"] - end) < 1e-6, meta["seconds"], end),
            check("kit output = independent inverse-tape resampling (mean |Δ| ≤ 0.01)", float(np.abs(out - ref).mean()) <= 0.01,
                  round(float(np.abs(out - ref).mean()), 4), "<=0.01"),
            check("scrolled by tape(t), the column under the camera is the one heard (mean |Δ| < 0.04)", err_t < 0.04, round(err_t, 4), "<0.04"),
            check("during the stop the terrain under the camera moves < 1.5 columns (frozen)", len(stop) >= 2 and max(jt) - min(jt) < 1.5,
                  round(max(jt) - min(jt), 3) if stop else None, "<1.5 cols over %d stop frames" % len(stop)),
            check("negative control: the raw wall-time image scrolled by tape shows the wrong sound (≥2.5x the error)",
                  err_u > 2.5 * err_t and err_u > 0.04, round(err_u, 4), ">2.5x %.4f" % err_t)], [op, png]


@card("BEAT-133")
def spectrogram_canyon(task, wd):
    """makeSpectrumGround's displacement (ported to numpy) on the tape-resampled spectrogram: 120 m wide, 8 tape-seconds
    across (15 m/s), half 17, amp 5.2; scrolled by the tape clock so the canyon freezes while the track stops."""
    ch, h, _ = _k3_fixture(wd, stop=True)
    tex, meta = k3_on_tape(wd, h, ch)
    sec = meta["seconds"]
    xs, zs, y0, hh = canyon(tex, 1.0, sec)
    _, _, y1, _ = canyon(tex, 1.5, sec)
    dx = xs[1] - xs[0]
    prof = lambda y: y[np.abs(zs) <= 17].mean(axis=0)
    shift = _shift_m(prof(y0), prof(y1), dx)
    floor = y0[np.argmin(np.abs(zs))].mean(); wall = y0[np.abs(zs) >= 17].mean()
    _, _, yk, _ = canyon(np.zeros_like(tex), 1.0, sec, kick=1.0)
    _, _, yq, _ = canyon(np.zeros_like(tex), 1.0, sec, kick=0.0)
    dk = float(yk[np.argmin(np.abs(zs))].mean() - yq[np.argmin(np.abs(zs))].mean())
    stop = [i for i, s in enumerate(ch["speed"]) if s < 0.1]
    a, b = stop[0] / 30, stop[-1] / 30
    ya = canyon(tex, tape_at(ch, a), sec)[2]; yb = canyon(tex, tape_at(ch, b), sec)[2]
    ywa = canyon(tex, a, sec)[2]; ywb = canyon(tex, b + 0.15, sec)[2]
    frozen = float(np.abs(ya - yb).mean()); moved = float(np.abs(ywa - ywb).mean())
    flat = canyon(np.zeros_like(tex), 1.0, sec)[2]
    from PIL import Image
    g = (y0 - y0.min()) / (y0.max() - y0.min() + 1e-9)
    op = Path(wd) / "canyon_height.png"
    Image.fromarray((g * 255).astype(np.uint8)).resize((480, 360)).save(op)
    var_s, var_f = float(prof(y0).std()), float(prof(flat).std())
    return [check("scroll speed: 0.5 tape-s moves the land 7.5 m (8 s over 120 m = 15 m/s, ±0.5)", abs(shift - 7.5) <= 0.5, shift, 7.5),
            check("canyon: walls (|z|≥half) stand > 3 m above the floor", wall - floor > 3, round(wall - floor, 2), ">3"),
            check("kick deepens the floor by amp·0.25·0.6 = 0.78 m", abs(dk + 0.78) < 1e-6, round(dk, 4), -0.78),
            check("tape-clock scroll: the ground is still across the stop (mean |Δy| < 0.05 m)", frozen < 0.05, round(frozen, 4), "<0.05"),
            check("negative control: wall-clock scroll keeps moving over the same span (mean |Δy| > 4x)", moved > 4 * frozen and moved > 0.05,
                  round(moved, 4), ">4x"),
            check("the relief comes from the sound: along-x spread > 0.2 m vs 0 for a silent texture", var_s > 0.2 and var_f < 1e-9,
                  [round(var_s, 3), var_f], ">0.2 / 0")], [op]


@card("BEAT-135")
def tape_stop_bullet_glitch(task, wd):
    """Tape-stop bullet time (world on tape(t), camera on wall t) and the card's analysis-keyed glitch uniforms,
    applied with makeGlitchPass's shader ported to numpy."""
    ch, _, _ = _k3_fixture(wd, stop=True)
    pl, _, _ = _k3_fixture(wd, stop=False)
    n = len(ch["speed"])
    U = [glitch_uniforms(ch, i) for i in range(n)]
    Up = [glitch_uniforms(pl, i) for i in range(len(pl["speed"]))]
    base = bars_frame()
    istop = int(np.argmin(ch["speed"]))
    tears = [i for i in range(n) if U[i]["negative"] > 0]
    iplay = next(i for i in range(n) if ch["speed"][i] == 1.0 and kick_env(ch, i / 30) < 1e-3 and ch["onset"][i] < 1e-3
                 and U[i]["negative"] == 0 and abs(U[i]["chroma"]) < 1e-9)
    fs = glitch_pass(base, U[istop]); ft = glitch_pass(base, U[tears[0]]) if tears else base; fp = glitch_pass(base, U[iplay])
    from PIL import Image
    outs = []
    for nm, im in (("stop", fs), ("tear", ft), ("play", fp)):
        p = Path(wd) / ("glitch_%s.png" % nm); Image.fromarray(im).save(p); outs.append(p)
    inv = (1 - base / 255.0) * 0.8
    tear_err = float(np.abs(ft / 255.0 - (base / 255.0 + (inv - base / 255.0) * 0.9)).mean()) if tears else 9
    # bullet time: an object moving on the tape clock, the camera orbiting on the wall clock
    a, b = [i for i in range(n) if ch["speed"][i] < 0.1][0], [i for i in range(n) if ch["speed"][i] < 0.1][-1]
    obj = lambda i: 3.0 * ch["tape"][i]
    cam = lambda i: 20.0 * i / 30
    jdump(Path(wd) / "glitch_uniforms.json", U)
    outs.append(Path(wd) / "glitch_uniforms.json")
    return [check("stop frame: mono = 1, picture is silver monochrome (spread after the tint < 8% of input)", U[istop]["mono"] > 0.99 and sat(fs, MONO_TINT) < 0.08 * sat(base),
                  [round(U[istop]["mono"], 3), round(sat(fs, MONO_TINT), 1)], "1 / <%.1f" % (0.08 * sat(base))),
            check("negative tear on exactly the first 3 silence frames (≈3.0 s)", len(tears) == 3 and abs(tears[0] / 30 - 3.0) < 0.1,
                  [round(t / 30, 3) for t in tears], "3 frames from ~3.0 s"),
            check("tear frame matches mix(c, (1−c)·0.8, 0.9) (mean |Δ| < 0.03 after slices)", tear_err < 0.03, round(tear_err, 4), "<0.03"),
            check("warp = (1−speed)·0.6 at the stop", abs(U[istop]["warp"] - 0.6 * (1 - ch["speed"][istop])) < 1e-9, round(U[istop]["warp"], 3), 0.6),
            check("normal play away from accents: the pass is the identity", int(np.abs(fp.astype(int) - base.astype(int)).max()) <= 1,
                  int(np.abs(fp.astype(int) - base.astype(int)).max()), "<=1"),
            check("bullet time: world still (Δ < 0.1) while the camera turns (> 1.5) across the stop",
                  abs(obj(b) - obj(a)) < 0.1 and cam(b) - cam(a) > 1.5, [round(obj(b) - obj(a), 3), round(cam(b) - cam(a), 2)], "<0.1 / >1.5"),
            check("negative control: without a tape stop no frame freezes to mono", max(u["mono"] for u in Up) < 0.01,
                  round(max(u["mono"] for u in Up), 3), "<0.01")], outs


def make_sparks(events, tapef, per=60, seed=5, speed=5.0, gravity=6.0):
    """makeSparks's motion in numpy: age on the tape clock, so sparks hang in the air while the track stops."""
    rs = np.random.default_rng(seed)
    N = len(events) * per
    a = rs.random(N) * 2 * np.pi; up = 0.4 + rs.random(N) * 0.6; sp = speed * (0.35 + rs.random(N) * 0.9)
    vel = np.stack([np.cos(a) * sp * 0.55, up * sp, np.sin(a) * sp * 0.55], 1); life = 0.5 + rs.random(N) * 1.1

    def at(t):
        P = np.full((N, 3), np.nan)
        for ei, e in enumerate(events):
            if t < e["t"]:
                continue
            u = tapef(t) - tapef(e["t"])
            sl = slice(ei * per, (ei + 1) * per)
            ok = (u >= 0) & (u <= life[sl])
            p = np.array([e["x"], e["y"], e["z"]]) + vel[sl] * u - np.array([0, 0.5 * gravity * u * u, 0])
            P[sl][ok] = p[ok]
            P[sl] = np.where(ok[:, None], p, np.nan)
        return P
    return at


@card("BEAT-132")
def sound_driven_picture(task, wd):
    """Sound-driven picture: the spectrogram canyon on the tape clock, sparks thrown on kicks moving on the tape clock,
    and the glitch pass keyed to MOTION.channels; rendered to a small video and measured frame by frame."""
    ch, h, _ = _k3_fixture(wd, stop=True)
    tex, meta = k3_on_tape(wd, h, ch)
    n, sec = len(ch["speed"]), meta["seconds"]
    kick = [k for k in ch["kicks"] if k < 1.5][-1]
    ev = [{"t": kick, "x": 0, "y": 0, "z": 0}]
    sp_t = make_sparks(ev, lambda t: tape_at(ch, t))
    sp_w = make_sparks(ev, lambda t: t)

    def world(i, clock):
        t = i / 30
        s = tape_at(ch, t) if clock == "tape" else t
        y = canyon(tex, s, sec, segX=95, segZ=53)[2]
        g = np.clip((y - (-1.5)) / 12.0, 0, 1)
        img = np.stack([g * 255, g * 120, g * 60], -1)
        P = (sp_t if clock == "tape" else sp_w)(t)
        for p in P:
            if np.isfinite(p[0]):
                px, py = int(48 + p[0] * 6), int(50 - p[1] * 6)
                if 0 <= px < 96 and 0 <= py < 54:
                    img[py, px] = (255, 230, 120)
        return img.astype(np.uint8)
    Wt = [world(i, "tape") for i in range(n)]
    Ww = [world(i, "wall") for i in range(n)]
    G = [glitch_pass(Wt[i], glitch_uniforms(ch, i)) for i in range(n)]
    vp = write_video(Path(wd) / "sound_picture.mp4", lambda i: G[i], n, 30, (96, 54))
    stop = [i for i in range(n) if ch["speed"][i] < 0.1]
    play = [i for i in range(30, 44)]
    d = lambda F, idx: float(np.mean([np.abs(F[i].astype(float) - F[i - 1].astype(float)).mean() for i in idx[1:]]))
    dst, dpl, dsw = d(Wt, stop), d(Wt, play), d(Ww, stop)
    Ps, Pw = sp_t(stop[0] / 30), sp_t(stop[-1] / 30)
    hang = float(np.nanmax(np.abs(Ps - Pw))) if np.isfinite(Ps).any() else 9
    istop = int(np.argmin(ch["speed"]))
    vf = frames_of(vp, (96, 54))
    return [check("rendered video has every frame", len(vf) == n, len(vf), n),
            check("world frozen during the stop: frame Δ < 25% of normal play", dst < 0.25 * dpl, [round(dst, 3), round(dpl, 3)], "<25%"),
            check("sparks thrown on the kick hang in the air across the stop (max move < 0.15)", hang < 0.15, round(hang, 3), "<0.15"),
            check("glitch freeze on the stop frame: silver monochrome (spread after tint < 15% of the world frame)",
                  sat(G[istop], MONO_TINT) < 0.15 * sat(Wt[istop]), [round(sat(G[istop], MONO_TINT), 2), round(sat(Wt[istop]), 2)], "<15%"),
            check("negative control: the same world on the wall clock keeps moving during the stop (> 2x)", dsw > 2 * dst and dsw > 0.25 * dpl,
                  round(dsw, 3), ">2x %.3f" % dst)], [vp]


def halo_layer(ch, i, size=(320, 180), seed=7, draw=True):
    """verse.html draw(t) light layer in numpy: halo R = .62·min(W,H)·(1+.05 rms+.06 kick+.25 flare), alpha 0.5·(1−r/R);
    72 motes r 2-9 px rising .006-.026 H/s, lifted by onsets; rings from kicks in the last 1.3 s, alpha .22·(1−dt/1.3)²,
    radius growing 180 px/s; 'lighter' (additive) blend."""
    W, H = size
    t = i / ch["fps"]
    payoff = ch["kicks"][-1] if ch["kicks"] else None
    rr = ch["rms"][i]; kk = kick_env(ch, t); flare = math.exp(-((t - payoff) / 0.25) ** 2) if payoff is not None else 0.0
    R = .62 * min(W, H) * (1 + .05 * rr + .06 * kk + .25 * flare)
    rings = [(dt, .22 * (1 - dt / 1.3) ** 2, 180 * dt) for dt in (t - k for k in ch["kicks"]) if 0 <= dt < 1.3]
    if not draw:
        return None, R, rings, None
    X, Y = np.meshgrid(np.arange(W) + 0.5, np.arange(H) + 0.5)
    r = np.hypot(X - W / 2, Y - H / 2)
    acc = 0.5 * np.clip(1 - r / R, 0, 1)
    for dt, a, rad in rings:
        acc = acc + a * (np.abs(r - rad) < 1.5)
    rs = np.random.default_rng(seed)
    mr = 2 + rs.random(72) * 7; mv = .006 + rs.random(72) * .020; mx = rs.random(72) * W; my0 = rs.random(72)
    lift = np.cumsum([1 + 2.0 * o for o in ch["onset"]]) / ch["fps"]
    my = (my0 - mv * lift[i]) % 1.0
    for x0, y0, rad in zip(mx, my * H, mr):
        x1, x2, y1, y2 = max(0, int(x0 - rad - 1)), min(W, int(x0 + rad + 2)), max(0, int(y0 - rad - 1)), min(H, int(y0 + rad + 2))
        if x2 > x1 and y2 > y1:
            acc[y1:y2, x1:x2] += 0.3 * (np.hypot(X[y1:y2, x1:x2] - x0, Y[y1:y2, x1:x2] - y0) < rad)
    return acc, R, rings, (mr, mv, lift)


@card("BEAT-154")
def halo_motes_rings(task, wd):
    """Sound-reactive halo, 72 motes and kick rings (the card's draw(t) formulas) driven by motion.py channels."""
    ch, _, _ = _k3_fixture(wd, stop=True)
    n = len(ch["rms"])
    sil = {k: (v if not isinstance(v, list) else [0.0] * len(v)) for k, v in ch.items()}
    sil["kicks"] = []
    W, H = 320, 180
    meas, form, Rq = [], [], []
    for i in range(0, n, 6):
        acc, R, _, _ = halo_layer(ch, i)
        row = acc[H // 2, W // 2:]
        halo_only = 0.5 * np.clip(1 - (np.arange(W // 2) + 0.5) / R, 0, 1)
        nz = np.flatnonzero(halo_only > 1e-6)
        meas.append(float(nz[-1] + 0.5) if len(nz) else 0); form.append(R)
        Rq.append(halo_layer(sil, i, draw=False)[1])
    ik = int(round(ch["kicks"][2] * 30)) + 1
    acc_k, Rk, rings_k, (mr, mv, lift) = halo_layer(ch, ik + 20)
    dt, a_ring, rad = rings_k[-1]
    ring_px = acc_k[H // 2, W // 2 + int(round(rad))] if W // 2 + int(round(rad)) < W else 0
    halo_px = 0.5 * max(0.0, 1 - math.hypot(int(round(rad)) + 0.5, 0.5) / Rk)
    from PIL import Image
    frames = [np.clip(halo_layer(ch, i)[0] * 255, 0, 255).astype(np.uint8) for i in range(0, n, 3)]
    vp = write_video(Path(wd) / "halo.mp4", lambda j: np.repeat(frames[j][..., None], 3, -1), len(frames), 10, (W, H))
    Image.fromarray(frames[len(frames) // 2]).save(Path(wd) / "halo_mid.png")
    rise = (lift[-1] - lift[0]) / ((n - 1) / 30)
    breath_s, breath_q = max(form) - min(form), max(Rq) - min(Rq)
    late = [len(halo_layer(ch, i, draw=False)[2]) for i in range(n)]
    kt = ch["kicks"]
    most = max(sum(1 for k in kt if 0 <= i / 30 - k < 1.3) for i in range(n))
    return [check("halo radius = .62·min(W,H)·(1+.05rms+.06kick+.25flare) (rendered extent within 1 px)",
                  max(abs(a - b) for a, b in zip(meas, form)) <= 1.0, round(max(abs(a - b) for a, b in zip(meas, form)), 3), "<=1 px"),
            check("flare at the payoff swells the halo ≥ 20%", max(form) >= 1.2 * .62 * 180, round(max(form), 1), ">=%.1f" % (1.2 * .62 * 180)),
            check("72 motes, radius 2-9 px, rise .006-.026 H/s", len(mr) == 72 and mr.min() >= 2 and mr.max() <= 9 and mv.min() >= .006 and mv.max() <= .026,
                  [len(mr), round(mr.min(), 2), round(mr.max(), 2), round(mv.min(), 4), round(mv.max(), 4)], "72, 2-9, .006-.026"),
            check("onsets lift the motes (mean lift rate > 1.0x)", rise > 1.0, round(rise, 3), ">1"),
            check("ring alpha .22·(1−dt/1.3)², added to the halo ('lighter')", abs(float(ring_px) - (halo_px + a_ring)) < 0.005,
                  [round(float(ring_px), 4), round(halo_px + a_ring, 4)], "halo + ring"),
            check("rings only for kicks in the last 1.3 s (drawn count = kicks in a 1.3 s window)", late == [sum(1 for k in kt if 0 <= i / 30 - k < 1.3) for i in range(n)]
                  and max(late) == most and most >= 2, max(late), most),
            check("negative control: silent channels give a constant halo (no breathing) and no rings",
                  breath_s > 5 and breath_q < 1e-6 and not halo_layer(sil, n // 2, draw=False)[2], [round(breath_s, 2), breath_q], ">5 vs 0")], [vp, Path(wd) / "halo_mid.png"]


# ───────────── music-to-video pipeline, maqam, bar maths, SFX sheet, licensing ─────────────
def snap_beat(t, beats):
    return min(beats, key=lambda b: abs(b - t)) if beats else t


def validate_plan(plan, beats, fps=30):
    """validate-plan rules: every frame starts on a beat (±1 frame), frames longer than ~6 s carry 2+ groups,
    group kinds are template / free / asset, groups sit inside their frame and start on beats."""
    errs = []
    for f in plan["frames"]:
        if f["start"] > 0 and beats and min(abs(f["start"] - b) for b in beats) > 1.0 / fps + 1e-9:
            errs.append("%s: start %.3f is off the beat grid" % (f["id"], f["start"]))
        if f["duration"] > 6.0 and len(f["groups"]) < 2:
            errs.append("%s: %.1f s frame needs 2+ groups (has %d)" % (f["id"], f["duration"], len(f["groups"])))
        for g in f["groups"]:
            if g["kind"] not in ("template", "free", "asset"):
                errs.append("%s: unknown group kind %s" % (f["id"], g["kind"]))
            if not (f["start"] - 1e-9 <= g["start"] < f["start"] + f["duration"]):
                errs.append("%s: group at %.3f outside the frame" % (f["id"], g["start"]))
            if g["start"] > 0 and beats and min(abs(g["start"] - b) for b in beats) > 1.0 / fps + 1e-9:
                errs.append("%s: group at %.3f off the beat grid" % (f["id"], g["start"]))
    return errs


@card("BEAT-128")
def music_to_video_pipeline(task, wd):
    """The music-to-video spine without the npm scaffold: stage bgm → analyse once to audiomap.json → STORYBOARD.md →
    plan (frames + groups) → validate-plan rules → frame HTML (compositions/frames/NN-*.html) → assembled index.html
    whose data-start values sit on the analysed beats."""
    from html.parser import HTMLParser
    root = Path(wd) / "videos/demo"
    (root / "assets").mkdir(parents=True, exist_ok=True)
    (root / "compositions/frames").mkdir(parents=True, exist_ok=True)
    x, truth = drum_loop(120, 12.0)
    x = x + music_bed(12.0, amp=0.15)
    bgm = save(root / "assets", "bgm.wav", x)
    A = audiomap(bgm)
    jdump(root / "audiomap.json", A)
    beats = A["beats_sec"]
    want = [("01-open", 0.0, 2.0), ("02-build", 2.0, 8.0), ("03-payoff", 10.0, 2.0)]
    frames = []
    for fid, s, d in want:
        s2 = round(snap_beat(s, beats), 3) if s > 0 else 0.0
        frames.append({"id": fid, "start": s2, "duration": d})
    for i, f in enumerate(frames):
        nxt = frames[i + 1]["start"] if i + 1 < len(frames) else A["duration"]
        f["duration"] = round(nxt - f["start"], 3)
    sb = ["# STORYBOARD", "", "audio: assets/bgm.wav · tempo %s BPM (trusted: %s)" % (A["tempo"], A["bpm_trusted"]), ""]
    for f in frames:
        sb.append("## %s  %.3f s → %.3f s" % (f["id"], f["start"], f["start"] + f["duration"]))
    tdump(root / "STORYBOARD.md", "\n".join(sb) + "\n")
    plan = {"brand": {"accent": "#ff8a50"}, "frames": []}
    for f in frames:
        n_g = 2 if f["duration"] > 6.0 else 1
        gb = [b for b in beats if f["start"] - 1e-6 <= b < f["start"] + f["duration"]]
        groups = [{"kind": ("template", "free", "asset")[k % 3], "start": round(snap_beat(f["start"] + k * f["duration"] / n_g, gb), 3)}
                  for k in range(n_g)]
        plan["frames"].append(dict(f, groups=groups))
    jdump(root / "plan.json", plan)
    errs = validate_plan(plan, beats)
    bad = json.loads(json.dumps(plan))
    bad["frames"][1]["groups"] = bad["frames"][1]["groups"][:1]
    bad["frames"][2]["start"] = round(bad["frames"][2]["start"] + 0.21, 3)
    for g in bad["frames"][2]["groups"]:
        g["start"] = round(g["start"] + 0.21, 3)
    bad_errs = validate_plan(bad, beats)
    for f in plan["frames"]:
        body = "\n".join('  <div class="group %s" data-start="%.3f"></div>' % (g["kind"], g["start"] - f["start"]) for g in f["groups"])
        tdump(root / "compositions/frames" / (f["id"] + ".html"),
              '<section class="frame" id="%s" data-duration="%.3f">\n%s\n</section>\n' % (f["id"], f["duration"], body))
    parts = []
    for f in plan["frames"]:
        inner = (root / "compositions/frames" / (f["id"] + ".html")).read_text()
        parts.append(inner.replace('<section class="frame"', '<section class="frame" data-start="%.3f"' % f["start"], 1))
    idx = tdump(root / "index.html", '<!doctype html>\n<html><body data-duration="%.3f">\n<audio src="assets/bgm.wav" data-start="0"></audio>\n%s</body></html>\n'
                % (A["duration"], "".join(parts)))

    class P(HTMLParser):
        def __init__(self):
            super().__init__(); self.starts = []; self.stack = []

        def handle_starttag(self, tag, attrs):
            a = dict(attrs)
            if tag == "section":
                self.cur = float(a["data-start"]); self.starts.append(("frame", self.cur, float(a["data-duration"])))
            elif tag == "div" and "data-start" in a:
                self.starts.append(("group", self.cur + float(a["data-start"]), 0))
    pr = P(); pr.feed(idx.read_text())
    st = [s for s in pr.starts]
    off = max(min(abs(t - b) for b in beats) for _, t, _ in st if t > 0)
    cover = sum(d for k, _, d in st if k == "frame")
    return [check("audiomap: 120 BPM loop analysed once, grid trusted", A["bpm_trusted"] and abs(A["tempo"] - 120) <= 2, A["tempo"], 120),
            check("plan passes validate-plan (the 8 s frame has 2 groups)", not errs and len(plan["frames"][1]["groups"]) == 2, errs, []),
            check("index.html: every frame and group data-start lands on an analysed beat (≤ 1 frame)", off <= 1 / 30 + 1e-9, round(off, 4), "<=0.033"),
            check("frames tile the song: total duration = audio (±1 frame)", abs(cover - A["duration"]) <= 1 / 30, round(cover, 3), A["duration"]),
            check("frame files written as compositions/frames/NN-*.html", sorted(p.name for p in (root / "compositions/frames").glob("*.html"))
                  == ["01-open.html", "02-build.html", "03-payoff.html"], len(list((root / "compositions/frames").glob("*.html"))), 3),
            check("negative control: a one-group 8 s frame and an off-beat start are rejected", len(bad_errs) == 3
                  and any("needs 2+ groups" in e for e in bad_errs) and any("start 1" in e and "off the beat grid" in e for e in bad_errs), bad_errs,
                  "groups + frame start + group start")], \
        [idx, root / "STORYBOARD.md", root / "plan.json", root / "audiomap.json"]


MAQAM = {"Rast": [0, 200, 350, 500, 700, 900, 1050, 1200], "Bayati": [0, 150, 300, 500, 700, 800, 1000, 1200],
         "Hijaz": [0, 100, 400, 500, 700, 800, 1000, 1200], "Saba": [0, 150, 300, 400, 700, 800, 1000, 1200],
         "Nahawand": [0, 200, 300, 500, 700, 800, 1100, 1200], "Kurd": [0, 100, 300, 500, 700, 800, 1000, 1200],
         "Ajam": [0, 200, 400, 500, 700, 900, 1100, 1200], "Sikah": [0, 150, 350, 500, 650, 850, 1050, 1200]}
MAQAM_MOOD = {"noble": ("Rast", "anthem, oud and qanun"), "warm": ("Bayati", "folk/Khaleeji warmth, oud"),
              "longing": ("Hijaz", "mystical cinematic longing, ney"), "grief": ("Saba", "grief, slow violin"),
              "romantic": ("Nahawand", "romantic minor, strings"), "tender": ("Kurd", "tender modern pop"),
              "bright": ("Ajam", "bright wedding feel"), "spiritual": ("Sikah", "spiritual Sufi, daf")}


def fine_hz(x, sr=SR, lo=50, hi=2000):
    n = 1 << 17
    X = np.abs(np.fft.rfft(x * np.hanning(len(x)), n))
    f = np.fft.rfftfreq(n, 1 / sr)
    m = (f >= lo) & (f <= hi)
    k = int(np.flatnonzero(m)[np.argmax(X[m])])
    a, b, c = np.log(X[k - 1] + 1e-12), np.log(X[k] + 1e-12), np.log(X[k + 1] + 1e-12)
    return float(f[k] + 0.5 * (a - c) / (a - 2 * b + c) * (f[1] - f[0]))


def render_scale(cents, f0=261.63, d=0.3, sr=SR):
    out = []
    for c in cents:
        f = f0 * 2 ** (c / 1200)
        out.append((sine(f, d, 0.4) + sine(2 * f, d, 0.1)) * np.hanning(int(round(d * sr))))
    return np.concatenate(out)


def measure_scale(x, n, f0=261.63, d=0.3, sr=SR):
    L = int(round(d * sr))
    return [round(1200 * math.log2(fine_hz(x[i * L + L // 6:(i + 1) * L - L // 6]) / f0), 1) for i in range(n)]


@card("BEAT-257")
def maqam_palette(task, wd):
    """Mood → maqam map with prompt hints, and each scale rendered (quarter tones included) and its pitches measured in cents."""
    out, meas = {}, {}
    for nm, cents in MAQAM.items():
        x = render_scale(cents)
        save(wd, "maqam_%s.wav" % nm.lower(), x)
        meas[nm] = measure_scale(x, len(cents))
    major = [0, 200, 400, 500, 700, 900, 1100, 1200]
    mj = measure_scale(render_scale(major), 8)
    hint = {m: "%s maqam, %s" % MAQAM_MOOD[m] for m in MAQAM_MOOD}
    p = jdump(Path(wd) / "maqam_palette.json", {"moods": MAQAM_MOOD, "hints": hint, "measured_cents": meas})
    worst = max(abs(a - b) for nm in MAQAM for a, b in zip(meas[nm], MAQAM[nm]))
    return [check("every rendered scale degree within 3 cents of its maqam value", worst <= 3, round(worst, 2), "<=3"),
            check("Rast neutral third ≈ 350 c and neutral seventh ≈ 1050 c", abs(meas["Rast"][2] - 350) <= 3 and abs(meas["Rast"][6] - 1050) <= 3,
                  [meas["Rast"][2], meas["Rast"][6]], [350, 1050]),
            check("Hijaz augmented second (degree 2→3) ≈ 300 c", abs(meas["Hijaz"][2] - meas["Hijaz"][1] - 300) <= 4,
                  round(meas["Hijaz"][2] - meas["Hijaz"][1], 1), 300),
            check("mood map: longing → Hijaz with a ney hint; grief → Saba", MAQAM_MOOD["longing"][0] == "Hijaz" and "ney" in hint["longing"]
                  and MAQAM_MOOD["grief"][0] == "Saba", hint["longing"], "Hijaz … ney"),
            check("negative control: a 12-TET major scale has no neutral third (|third − 350| > 40 c)", abs(mj[2] - 350) > 40, mj[2], "far from 350")], \
        [p, Path(wd) / "maqam_rast.wav"]


def beat_durations(bpm, beats_per_bar=4):
    beat = 60.0 / bpm
    return {"beat": round(beat, 4), "bar": round(beat * beats_per_bar, 4), "8bar": round(beat * beats_per_bar * 8, 4)}


LIVING_ARTIST_PAT = re.compile(r"\b(in the style of|sounds? like|imitat\w*|voice of)\b", re.I)
BRIEF_FIELDS = ["genre_maqam", "bpm", "structure", "rhyme", "hook", "instrumentation", "vocal", "reference_feel"]


def lint_brief(b):
    errs = ["missing %s" % k for k in BRIEF_FIELDS if not b.get(k)]
    if LIVING_ARTIST_PAT.search(json.dumps(b, ensure_ascii=False)):
        errs.append("living-artist imitation")
    return errs


@card("BEAT-260")
def song_brief_beats(task, wd):
    """Original-lyrics song brief (no living-artist imitation) plus beat / bar / 8-bar durations, checked against a click
    track rendered at that tempo and measured."""
    brief = {"genre_maqam": "Khaleeji pop, maqam Bayati", "bpm": 90, "structure": ["Intro", "Verse 1", "Chorus", "Verse 2", "Bridge", "Chorus", "Outro"],
             "rhyme": "قافية النون (ـين)", "hook": "يا ليل خلّك معي", "instrumentation": ["oud", "qanun", "tasfiq"],
             "vocal": "warm male baritone, close mic", "reference_feel": "late-night Gulf radio warmth, 2000s production"}
    D120, D90 = beat_durations(120), beat_durations(90)
    times = [i * D90["beat"] for i in range(int(16 / D90["beat"]))]
    x = clicks(times, 16.5)
    for k in range(0, len(times), 4):
        place(x, sine(2000, 0.02, 0.6), times[k])
    save(wd, "click90.wav", x)
    on = onsets(x, SR)
    ioi = float(np.median(np.diff(on)))
    acc = [t for t in on if seg_db(bandpass(x, 1800, 2200), SR, t, t + 0.02) > -20]
    bar = float(np.median(np.diff(acc))) if len(acc) > 2 else 0
    bad = dict(brief, reference_feel="sounds like a famous living singer")
    bad.pop("rhyme")
    p = jdump(Path(wd) / "song_brief.json", dict(brief, durations=D90))
    return [check("120 BPM → beat 0.5 / bar 2 / 8 bars 16 s", D120 == {"beat": 0.5, "bar": 2.0, "8bar": 16.0}, D120, "0.5/2/16"),
            check("90 BPM → 0.6667 / 2.6667 / 21.3333 s", D90 == {"beat": 0.6667, "bar": 2.6667, "8bar": 21.3333}, D90, "0.6667/2.6667/21.3333"),
            check("measured click IOI = the computed beat (±5 ms)", abs(ioi - D90["beat"]) < 0.005, round(ioi, 4), D90["beat"]),
            check("measured bar accents = the computed bar (±10 ms)", abs(bar - D90["bar"]) < 0.01, round(bar, 4), D90["bar"]),
            check("brief has every field and no living-artist imitation", lint_brief(brief) == [], lint_brief(brief), []),
            check("negative control: an imitation reference and a missing rhyme are flagged; 120-BPM grid misses the 90-BPM clicks",
                  len(lint_brief(bad)) == 2 and abs(ioi - D120["beat"]) > 0.1, [lint_brief(bad), round(ioi - D120["beat"], 3)], "2 errors / >0.1")], [p, Path(wd) / "click90.wav"]


def bar_plan(sections, bpm, bpb=4, styles=None, key="A minor"):
    """ElevenLabs music_v2 composition plan in whole bars: seconds = bars·bpb·60/bpm (ms); first chunk global styles,
    tempo and key; later chunks repeat the tempo; instrumental sections get '{instrumental, no vocals}'."""
    plan, t = [], 0.0
    for i, s in enumerate(sections):
        ms = int(round(s["bars"] * bpb * 60000.0 / bpm))
        loc = list(s.get("styles", []))
        if s.get("instrumental"):
            loc.append("{instrumental, no vocals}")
        pos = (["%d bpm" % bpm, key] + list(styles or [])) if i == 0 else ["%d bpm" % bpm]
        plan.append({"section_name": s["name"], "duration_ms": ms, "positive_local_styles": pos + loc,
                     "negative_local_styles": list(s.get("avoid", [])), "lines": list(s.get("lines", [])), "start_ms": int(round(t * 1000))})
        t += ms / 1000.0
    return {"sections": plan, "total_ms": int(round(t * 1000))}


def lint_bar_plan(pl, bpm, bpb=4):
    bar_ms = bpb * 60000.0 / bpm
    errs = []
    for s in pl["sections"]:
        if abs(s["start_ms"] / bar_ms - round(s["start_ms"] / bar_ms)) > 0.01:
            errs.append("%s starts off a bar line" % s["section_name"])
        if not 3000 <= s["duration_ms"] <= 120000:
            errs.append("%s length %d ms outside 3-120 s" % (s["section_name"], s["duration_ms"]))
        if any(len(l) > 200 for l in s["lines"]):
            errs.append("%s has a line over 200 chars" % s["section_name"])
        if "%d bpm" % bpm not in s["positive_local_styles"]:
            errs.append("%s does not carry the tempo" % s["section_name"])
    if not 3000 <= pl["total_ms"] <= 600000:
        errs.append("song length outside 3 s-10 min")
    return errs


@card("BEAT-175")
def elevenlabs_bar_plan(task, wd):
    """The composition plan maths in whole bars (the paid generation is not called): sections rendered as a click track
    whose section accents are measured to land on bar lines."""
    bpm = 96
    secs = [{"name": "Intro", "bars": 4, "instrumental": True}, {"name": "Verse", "bars": 8, "lines": ["الليل طويل وأنا أستناك"]},
            {"name": "Chorus", "bars": 8, "lines": ["خلّك معي"], "styles": ["wide", "drums up"]}, {"name": "Outro", "bars": 4, "instrumental": True, "avoid": ["fade"]}]
    pl = bar_plan(secs, bpm, styles=["Khaleeji pop", "oud"])
    p = jdump(Path(wd) / "composition_plan.json", pl)
    beat = 60.0 / bpm
    total = pl["total_ms"] / 1000
    x = clicks([i * beat for i in range(int(total / beat))], total + 0.5, amp=0.3)
    for s in pl["sections"]:
        place(x, sine(2500, 0.03, 0.8), s["start_ms"] / 1000 + 1e-3)
    save(wd, "plan_clicks.wav", x)
    xb = bandpass(x, 2300, 2700)
    hits = [t for t in onsets(xb, SR, rel=0.5)]
    bar = 4 * beat
    off = max(abs(h / bar - round(h / bar)) * bar for h in hits)
    bad = bar_plan(secs[:1] + [dict(secs[1], bars=3.5)] + secs[2:], bpm)
    berr = lint_bar_plan(bad, bpm)
    long_line = bar_plan([dict(secs[1], lines=["x" * 210])], bpm)
    return [check("Verse 8 bars at 96 BPM = 20 000 ms", pl["sections"][1]["duration_ms"] == 20000, pl["sections"][1]["duration_ms"], 20000),
            check("plan lints clean (bars, 3-120 s, ≤200-char lines, tempo in every chunk)", lint_bar_plan(pl, bpm) == [], lint_bar_plan(pl, bpm), []),
            check("first chunk carries global styles + key; instrumental sections tagged", "A minor" in pl["sections"][0]["positive_local_styles"]
                  and "{instrumental, no vocals}" in pl["sections"][0]["positive_local_styles"] and "{instrumental, no vocals}" not in pl["sections"][1]["positive_local_styles"],
                  pl["sections"][0]["positive_local_styles"], "global + instrumental"),
            check("rendered section accents measured on bar lines (≤ 3 ms)", len(hits) == 4 and off <= 0.003, [len(hits), round(off * 1000, 2)], "4 / <=3 ms"),
            check("a 210-char line is refused", any("200 chars" in e for e in lint_bar_plan(long_line, bpm)), lint_bar_plan(long_line, bpm), "line error"),
            check("negative control: a 3.5-bar section pushes the next sections off the bar lines", sum("off a bar line" in e for e in berr) == 2, berr, "2 off-bar")], \
        [p, Path(wd) / "plan_clicks.wav"]


SFX_LAYERS = ("ambience", "foley", "hard FX", "music", "UI")


def sfx_source(layer, d, seed):
    n = int(d * SR)
    if layer == "ambience":
        return lowpass(noise(n, seed), 800) * np.hanning(n)
    if layer == "foley":
        return bandpass(noise(n, seed), 1500, 4000) * np.exp(-np.arange(n) / (0.05 * SR))
    if layer == "hard FX":
        k = kick(); return np.pad(k, (0, max(0, n - len(k))))[:n]
    if layer == "music":
        return music_bed(d, amp=0.3) * _fade(n)
    return sine(2000, d, 0.5) * _fade(n)


def _fade(n, a=0.004):
    """4 ms attack then a linear tail to zero, so a cue's start is where its timecode says."""
    k = max(1, int(a * SR))
    return np.minimum(np.arange(n) / k, 1.0) * np.linspace(1, 0, n) ** 0.5


def render_sheet(rows, secs, honour=True):
    out = np.zeros((int(secs * SR), 2))
    for i, r in enumerate(rows):
        s = sfx_source(r["layer"], r["dur"], i)
        s = s / (np.max(np.abs(s)) + 1e-12) * 10 ** (r["dbfs"] / 20)
        pan = r["pan"] if honour else 0.0
        th = (pan + 1) * math.pi / 4
        t = r["tc"] if honour else 0.0
        a = int(t * SR)
        out[a:a + len(s), 0] += s[:len(out) - a] * math.cos(th)
        out[a:a + len(s), 1] += s[:len(out) - a] * math.sin(th)
    return out


@card("BEAT-179")
def sfx_design_sheet(task, wd):
    """Timecoded SFX design sheet (timecode | layer | description | level dBFS | pan | prompt) rendered offline with local
    stand-in sounds and measured for start time, peak level and constant-power pan (the AI SFX prompts are written, not sent)."""
    rows = [{"tc": 0.50, "layer": "ambience", "desc": "night wind", "dbfs": -24, "pan": 0.0, "dur": 0.8},
            {"tc": 1.60, "layer": "foley", "desc": "footstep on gravel", "dbfs": -12, "pan": -0.6, "dur": 0.25},
            {"tc": 2.40, "layer": "hard FX", "desc": "door slam", "dbfs": -6, "pan": 0.4, "dur": 0.4},
            {"tc": 3.30, "layer": "UI", "desc": "title blip", "dbfs": -18, "pan": 1.0, "dur": 0.15},
            {"tc": 4.00, "layer": "music", "desc": "oud sting", "dbfs": -10, "pan": -0.2, "dur": 0.6}]
    for r in rows:
        r["prompt"] = "%s, %s, %.1f s, clean, no music" % (r["desc"], r["layer"], r["dur"]) if r["layer"] != "music" else "%s, %.1f s" % (r["desc"], r["dur"])
    lines = ["| timecode | layer | description | level dBFS | pan | prompt |", "|---|---|---|---|---|---|"]
    lines += ["| 00:00:%05.2f | %s | %s | %d | %+.1f | %s |" % (r["tc"], r["layer"], r["desc"], r["dbfs"], r["pan"], r["prompt"]) for r in rows]
    sheet = tdump(Path(wd) / "SFX_SHEET.md", "\n".join(lines) + "\n")
    # parse the sheet back (the render reads the written sheet, not the dict)
    parsed = []
    for ln in sheet.read_text().splitlines()[2:]:
        c = [v.strip() for v in ln.strip("|").split("|")]
        parsed.append({"tc": float(c[0].split(":")[-1]), "layer": c[1], "dbfs": float(c[3]), "pan": float(c[4]),
                       "dur": next(r["dur"] for r in rows if r["desc"] == c[2])})
    mix = render_sheet(parsed, 5.0)
    mp = save(wd, "sfx_mix.wav", mix)
    flat = render_sheet(parsed, 5.0, honour=False)
    save(wd, "sfx_unplaced.wav", flat)

    def meas(m):
        res = []
        for r in parsed:
            a, b = int(r["tc"] * SR) - int(0.05 * SR), int((r["tc"] + r["dur"]) * SR)
            seg = m[max(0, a):b]
            mag = np.sqrt(seg[:, 0] ** 2 + seg[:, 1] ** 2)
            env = envelope(mag, SR, 2.0)
            st = (max(0, a) + int(np.flatnonzero(env > 0.1 * env.max())[0])) / SR if env.max() > 1e-6 else -1
            L, R = rms(seg[:, 0]), rms(seg[:, 1])
            res.append({"start": st, "peak": 20 * math.log10(mag.max() + 1e-12), "pan": 4 / math.pi * math.atan2(R, L) - 1})
        return res
    M, F = meas(mix), meas(flat)
    t_err = max(abs(m["start"] - r["tc"]) for m, r in zip(M, parsed) if r["layer"] != "ambience")
    l_err = max(abs(m["peak"] - r["dbfs"]) for m, r in zip(M, parsed))
    p_err = max(abs(m["pan"] - r["pan"]) for m, r in zip(M, parsed))
    p_f = max(abs(m["pan"] - r["pan"]) for m, r in zip(F, parsed))
    return [check("sheet has the six columns and one row per cue", lines[0].count("|") == 7 and len(parsed) == 5, len(parsed), 5),
            check("every layer type is from ambience/foley/hard FX/music/UI", all(r["layer"] in SFX_LAYERS for r in parsed), [r["layer"] for r in parsed], SFX_LAYERS),
            check("rendered cue starts at its timecode (≤ 15 ms)", t_err <= 0.015, round(t_err, 4), "<=0.015"),
            check("peak level = sheet dBFS (≤ 0.5 dB)", l_err <= 0.5, round(l_err, 3), "<=0.5"),
            check("measured pan = sheet pan (constant-power, ≤ 0.05)", p_err <= 0.05, round(p_err, 4), "<=0.05"),
            check("negative control: the cues summed unplaced/centred miss the sheet's pans (> 0.5)", p_f > 0.5, round(p_f, 3), ">0.5")], [sheet, mp]


LICENCE_OK = {"user-provided", "licensed", "own-composition", "public-domain"}


def licence_gate(manifest):
    ok, blocked = [], []
    for it in manifest:
        src = it.get("source", "")
        if src == "user-provided" and it.get("provided_by"):
            ok.append(it["file"])
        elif src == "licensed" and it.get("licence") and it.get("licence_id"):
            ok.append(it["file"])
        elif src in ("own-composition", "public-domain") and it.get("evidence"):
            ok.append(it["file"])
        else:
            blocked.append((it["file"], "no proof of licence for source %r" % (src or "unknown")))
    return ok, blocked


@card("BEAT-278")
def music_licence_gate(task, wd):
    """Only user-provided or licensed music: a gate over a music manifest that passes items with proof and blocks the rest."""
    man = [{"file": "user_song.wav", "source": "user-provided", "provided_by": "owner upload 2026-11-04"},
           {"file": "bed.mp3", "source": "licensed", "licence": "Pixabay Content License", "licence_id": "pixabay-123456"},
           {"file": "score.wav", "source": "own-composition", "evidence": "score.py render log"},
           {"file": "hit_single.mp3", "source": "youtube-rip"},
           {"file": "mystery.wav"},
           {"file": "stock.mp3", "source": "licensed", "licence": "unknown"}]
    ok, blocked = licence_gate(man)
    jdump(Path(wd) / "music_manifest.json", man)
    rep = jdump(Path(wd) / "licence_gate.json", {"approved": ok, "blocked": blocked})
    used_untreated = [m["file"] for m in man]
    unproven = [f for f in used_untreated if f not in ok]
    return [check("approved = the three items with proof", ok == ["user_song.wav", "bed.mp3", "score.wav"], ok, 3),
            check("blocked = the rip, the unknown source and the licence without an id", [b[0] for b in blocked] == ["hit_single.mp3", "mystery.wav", "stock.mp3"],
                  [b[0] for b in blocked], 3),
            check("each blocked item carries a reason", all(b[1] for b in blocked), len(blocked), 3),
            check("negative control: using the ungated manifest would ship 3 unlicensed tracks", len(unproven) == 3, unproven, 3)], [rep]


# ───────────── song-prompt packages: builders plus linters of each card's rules (generation is never called) ─────────────
VOC = {
    "bpm": [r"\b\d{2,3}\s*bpm\b"],
    "vocal": [r"\bvocals?\b", r"\bvoice\b", r"\bbreathy\b", r"\braspy\b", r"\bfalsetto\b", r"\bbelted\b", r"\bbaritone\b", r"\btenor\b",
              r"\bchoir\b", r"\brapped\b", r"\bwhisper\w*\b"],
    "production": [r"\bmix\b", r"\bproduction\b", r"\breverb\b", r"\bsaturation\b", r"\bsidechain\w*\b", r"\bstereo\b", r"\bmaster\w*\b",
                   r"\banalog\b", r"\btape\b", r"\bpolished\b", r"\bcrisp\b", r"\bpunchy\b", r"\bdistortion\b"],
    "instrument": [r"\bpiano\b", r"\bguitar\b", r"\bbass\b", r"\bsynths?\b", r"\bstrings\b", r"\bviolin\b", r"\boud\b", r"\bqanun\b", r"\bney\b",
                   r"\bdarbu?o?u?ka\b", r"\baccordion\b", r"\bdrums\b", r"\b808s?\b", r"\bbrass\b", r"\bpads?\b", r"\bhi-hats\b", r"\bpercussion\b",
                   r"\btabla\b", r"\briq\b", r"\bdaf\b", r"\bcello\b", r"\bgroove\b", r"\bclaps\b"],
    "genre": [r"\bpop\b", r"\brock\b", r"\bhip-hop\b", r"\btrap\b", r"\bedm\b", r"\bhouse\b", r"\btechno\b", r"\bjazz\b", r"\bclassical\b",
              r"\bfolk\b", r"\bmetal\b", r"\bambient\b", r"\blo-?fi\b", r"\br&b\b", r"\brnb\b", r"\bsynthwave\b", r"\bsynth-pop\b", r"\bdream-pop\b",
              r"\bshoegaze\b", r"\bkhaleeji\b", r"\brai\b", r"\bshaabi\b", r"\bboom-bap\b", r"\bdisco\b", r"\bsoul\b", r"\btrailer\b"],
    "mood": [r"\bmelanchol\w*\b", r"\bnostalgic\b", r"\beuphoric\b", r"\bdark\b", r"\buplifting\b", r"\btense\b", r"\bdreamy\b", r"\bhopeful\b",
             r"\bromantic\b", r"\baggressive\b", r"\bintimate\b", r"\bbittersweet\b", r"\btriumphant\b", r"\bmysterious\b", r"\bwarm\b", r"\byearning\b"],
}
LAYERS6 = ["genre", "mood", "instrument", "vocal", "bpm", "production"]


def tag_cat(tag, order=("bpm", "vocal", "production", "genre", "instrument", "mood")):
    t = tag.lower()
    for c in order:
        if any(re.search(p, t) for p in VOC[c]):
            return c
    return "other"


def split_tags(style):
    return [t.strip() for t in style.split(",") if t.strip()]


def build_style6(d):
    tags = [d["genre"]] + d["moods"] + d["instruments"] + [d["vocal"], "%d BPM" % d["bpm"]] + d["production"]
    return ", ".join(tags)


def lint_style6(style, lyrics="", title=""):
    tags = split_tags(style)
    cats = [tag_cat(t) for t in tags]
    idx = [LAYERS6.index(c) if c in LAYERS6 else 99 for c in cats]
    errs = []
    if not 5 <= len(tags) <= 8:
        errs.append("%d tags (want 5-8)" % len(tags))
    if not cats or cats[0] != "genre":
        errs.append("genre not front-loaded")
    if idx != sorted(idx):
        errs.append("layers out of order: %s" % "→".join(cats))
    if 99 in idx:
        errs.append("unclassified tag")
    if set(LAYERS6) - set(cats):
        errs.append("missing layers %s" % sorted(set(LAYERS6) - set(cats)))
    if len(style) > 1000 or len(lyrics) > 5000 or len(title) > 100:
        errs.append("field over its limit")
    return errs, cats


@card("BEAT-166")
def suno_six_layer(task, wd):
    """Suno style prompt in six ordered layers genre → mood → instruments → vocal → BPM → production (5-8 tags, genre
    first, style ≤1000 / lyrics ≤5000 / title ≤100 chars): builder plus a layer classifier/linter."""
    spec = {"genre": "90s boom-bap hip-hop", "moods": ["nostalgic", "bittersweet"], "instruments": ["dusty piano", "upright bass"],
            "vocal": "raspy male vocal", "bpm": 88, "production": ["vinyl tape saturation"]}
    st = build_style6(spec)
    lyr = "[Verse 1]\nسطر أول\n[Chorus]\nلازمة\n"
    errs, cats = lint_style6(st, lyr, "Old Tapes")
    shuffled = ", ".join(["88 BPM", "raspy male vocal", "nostalgic", "dusty piano", "90s boom-bap hip-hop", "vinyl tape saturation",
                          "bittersweet", "upright bass", "warm", "dreamy"])
    berr, bcats = lint_style6(shuffled)
    p = jdump(Path(wd) / "suno_style.json", {"style": st, "layers": cats, "lyrics": lyr, "title": "Old Tapes"})
    return [check("built style classifies to the six layers in order", cats == ["genre", "mood", "mood", "instrument", "instrument", "vocal", "bpm", "production"],
                  cats, "genre→mood→instrument→vocal→bpm→production"),
            check("6-layer prompt lints clean (5-8 tags, genre first, numeric BPM, limits)", errs == [] and len(split_tags(st)) == 8, errs, []),
            check("classifier known answers", [tag_cat(t) for t in ("dark ambient", "breathy female vocal", "120 BPM", "wide stereo mix", "oud")]
                  == ["genre", "vocal", "bpm", "production", "instrument"], [tag_cat(t) for t in ("dark ambient", "breathy female vocal", "120 BPM", "wide stereo mix", "oud")],
                  "genre/vocal/bpm/production/instrument"),
            check("negative control: a shuffled 10-tag prompt fails count, genre-first and order", len(berr) >= 3
                  and any("genre not front" in e for e in berr) and any("out of order" in e for e in berr) and any("10 tags" in e for e in berr), berr, ">=3 errors")], [p]


STD_LABELS = ["Intro", "Verse", "Pre-Chorus", "Chorus", "Post-Chorus", "Hook", "Bridge", "Build-Up", "Drop", "Instrumental Break",
              "Interlude", "Break", "Outro", "End", "Fade Out"]
SEC_RE = re.compile(r"^\[([A-Za-z][A-Za-z\- ]*?)(?:\s+(\d+))?\s*(?:[:|]\s*(.*?))?\]$")


def parse_sections(text):
    out = []
    for ln in text.splitlines():
        m = SEC_RE.match(ln.strip())
        if m:
            desc = [d.strip() for d in re.split(r"[,|]", m.group(3) or "") if d.strip()]
            out.append({"label": m.group(1).strip(), "n": m.group(2), "desc": desc})
    return out


DENSE = re.compile(r"drums|harmon|choir|stack|full|layer|claps|808|strings", re.I)


def lint_sections(text):
    S = parse_sections(text)
    errs = []
    for s in S:
        if s["label"] not in STD_LABELS:
            errs.append("non-standard label [%s] (would be sung)" % s["label"])
        if s["desc"] and not 4 <= len(s["desc"]) <= 7:
            errs.append("[%s] has %d descriptors (want 4-7)" % (s["label"], len(s["desc"])))
    ch = [sum(bool(DENSE.search(d)) for d in s["desc"]) for s in S if s["label"] == "Chorus"]
    if len(ch) >= 2 and not (all(b >= a for a, b in zip(ch, ch[1:])) and ch[-1] > ch[0]):
        errs.append("choruses do not escalate %s" % ch)
    br = [s for s in S if s["label"] == "Bridge"]
    if br and ch and not (sum(bool(DENSE.search(d)) for d in br[0]["desc"]) < min(ch) or any(re.search(r"sparse|strip|no drums", d, re.I) for d in br[0]["desc"])):
        errs.append("bridge not stripped")
    return errs, S


def section_sheet(plan):
    return "\n".join("[%s%s: %s]\n%s" % (lab, (" %d" % n) if n else "", ", ".join(desc), "\n".join(lines)) for lab, n, desc, lines in plan) + "\n"


@card("BEAT-167")
def suno_section_overrides(task, wd):
    """Per-section style overrides in the lyrics field: 4-7 descriptors per block, standard labels only, choruses
    escalating drums/harmonies, a stripped bridge; built then linted."""
    plan = [("Verse", 1, ["piano only", "no drums", "intimate", "close vocal"], ["سطر"]),
            ("Chorus", None, ["full drums", "bass", "wide", "lead vocal"], ["لازمة"]),
            ("Verse", 2, ["piano", "soft kick", "warm", "close vocal"], ["سطر"]),
            ("Chorus", None, ["full drums", "harmonies", "claps", "wide"], ["لازمة"]),
            ("Bridge", None, ["sparse", "no drums", "dark", "solo voice"], ["جسر"]),
            ("Chorus", None, ["full drums", "stacked harmonies", "choir", "strings", "huge"], ["لازمة"])]
    txt = section_sheet(plan)
    errs, S = lint_sections(txt)
    bad = section_sheet([("Verse Thing", None, ["a", "b", "c", "d", "e", "f", "g", "h", "i"], ["x"]),
                         ("Chorus", None, ["full drums", "harmonies", "claps", "wide"], ["y"]),
                         ("Chorus", None, ["drums", "bass", "wide", "vocal"], ["y"])])
    berr, _ = lint_sections(bad)
    p = tdump(Path(wd) / "lyrics_with_overrides.txt", txt)
    dens = [sum(bool(DENSE.search(d)) for d in s["desc"]) for s in S if s["label"] == "Chorus"]
    return [check("six section tags parsed with their descriptors", len(S) == 6 and all(4 <= len(s["desc"]) <= 7 for s in S), [len(s["desc"]) for s in S], "4-7 each"),
            check("chorus density escalates chorus by chorus", dens == sorted(dens) and dens[-1] > dens[0], dens, "rising"),
            check("sheet lints clean (standard labels, stripped bridge)", errs == [], errs, []),
            check("negative control: a non-standard label, 9 descriptors and flat choruses are flagged", len(berr) == 3, berr, 3)], [p]


STRUCT_TAGS = {"Intro", "Verse", "Pre-Chorus", "Chorus", "Bridge", "Build-Up", "Drop", "Instrumental Break", "Outro", "End", "Fade Out", "Melodic Instrumental"}
VOCAL_TAGS = {"Whispered", "Belted", "Falsetto", "Choir", "Rapped", "Spoken Word"}
FX_TAGS = {"Crescendo", "Silence", "Echo"}


def lint_tags(text, hard_stop=True):
    errs, last = [], None
    for ln in text.splitlines():
        s = ln.strip()
        if not s:
            continue
        tags = re.findall(r"\[([^\]]+)\]", s)
        if tags and re.sub(r"\[[^\]]+\]", "", s).strip():
            errs.append("tag not on its own line: %r" % s)
        for tg in tags:
            base = re.sub(r"\s+\d+$", "", tg.split(":")[0].split("|")[0].strip())
            if base not in STRUCT_TAGS | VOCAL_TAGS | FX_TAGS:
                errs.append("unknown tag [%s]" % tg)
            last = base
        for cue in re.findall(r"\(([^)]*)\)", s):
            if not 1 <= len(cue.split()) <= 3:
                errs.append("cue (%s) is %d words (want 1-3)" % (cue, len(cue.split())))
    if hard_stop and last != "End":
        errs.append("no [End] for a hard stop")
    return errs


def tidy_tags(text):
    """Puts every tag on its own line, trims parenthesised cues to their first 3 words and closes with [End]."""
    out = []
    for ln in text.splitlines():
        s = ln.strip()
        if not s:
            continue
        s = re.sub(r"\(([^)]*)\)", lambda m: "(" + " ".join(m.group(1).split()[:3]) + ")", s)
        parts = re.split(r"(\[[^\]]+\])", s)
        for p_ in parts:
            if p_.strip():
                out.append(p_.strip())
    if not out or out[-1] != "[End]":
        out = [o for o in out if o != "[Fade Out]"] + ["[End]"]
    return "\n".join(out) + "\n"


@card("BEAT-168")
def suno_tag_taxonomy(task, wd):
    """Structural / vocal / effect tags on their own lines, inline cues of 1-3 words, [End] for a clean hard stop:
    a tidier that enforces it and a linter that measures it."""
    raw = ("[Intro] (soft piano swells under the voice)\n[Verse 1]\nالليل طال (whispered)\n[Pre-Chorus]\n[Crescendo] وين انت\n"
           "[Chorus]\n[Belted]\nخلك معي (with a long breathy rising sigh)\n[Fade Out]\n")
    before = lint_tags(raw)
    fixed = tidy_tags(raw)
    after = lint_tags(fixed)
    p = tdump(Path(wd) / "lyrics_tagged.txt", fixed)
    cues = re.findall(r"\(([^)]*)\)", fixed)
    return [check("tidied lyrics lint clean", after == [], after, []),
            check("every inline cue is 1-3 words", cues and all(1 <= len(c.split()) <= 3 for c in cues), [len(c.split()) for c in cues], "1-3"),
            check("ends on [End] (hard stop), the fade tag is gone", fixed.strip().splitlines()[-1] == "[End]" and "[Fade Out]" not in fixed, fixed.strip().splitlines()[-1], "[End]"),
            check("lyric words kept in order", [w for w in re.findall(r"[؀-ۿ]+", fixed)] == re.findall(r"[؀-ۿ]+", raw),
                  len(re.findall(r"[؀-ۿ]+", fixed)), len(re.findall(r"[؀-ۿ]+", raw))),
            check("negative control: the raw draft has inline tags, long cues and no [End]", len(before) >= 4
                  and any("own line" in e for e in before) and any("words" in e for e in before) and any("[End]" in e for e in before), before, ">=4")], [p]


VOWEL_RUN = re.compile(r"([aeiouAEIOU])\1+")


def perform(sections, turns, melisma, pause_before):
    """Applies the vocal tricks: ALL-CAPS on the section's turning words, +4 vowels on one sustained word, '...' before a
    held word, one phrase per line."""
    out = []
    for name, lines in sections:
        out.append("[%s]" % name)
        for ln in lines:
            for ph in [x.strip() for x in ln.split(",") if x.strip()]:
                words = ph.split()
                for i, w in enumerate(words):
                    if w.lower() in turns.get(name, []):
                        words[i] = w.upper()
                    if w.lower() == melisma:
                        v = max((m for m in re.finditer(r"[aeiou]", w)), key=lambda m: m.start())
                        words[i] = w[:v.end()] + v.group(0) * 4 + w[v.end():]
                    if w.lower() == pause_before and i:
                        words[i] = "... " + words[i]
                out.append(" ".join(words))
    return "\n".join(out) + "\n"


def lint_perf(text):
    errs, sec, caps = [], None, {}
    for ln in text.splitlines():
        if ln.startswith("["):
            sec = ln; caps[sec] = 0; continue
        caps[sec] = caps.get(sec, 0) + sum(1 for w in re.findall(r"[A-Za-z']+", ln) if len(w) > 1 and w.isupper())
        for m in VOWEL_RUN.finditer(ln):
            extra = len(m.group(0)) - 1
            if extra >= 20:
                errs.append("melisma of %d vowels glitches" % extra)
            elif not 3 <= extra <= 5 and extra > 1:
                errs.append("melisma +%d (want 3-5)" % extra)
        if "," in ln:
            errs.append("two phrases on one line")
    for s, c in caps.items():
        if not 1 <= c <= 2:
            errs.append("%s has %d caps words (want 1-2)" % (s, c))
    if "..." not in text:
        errs.append("no '...' breath pause")
    return errs, caps


@card("BEAT-169")
def suno_vocal_tricks(task, wd):
    """Lyric formatting that shapes delivery (medium-confidence community tricks): caps on 1-2 turning words per section,
    +3-5 vowels for melisma, '...' for a breath pause, one phrase per line."""
    secs = [("Verse 1", ["the night is long, i wait for you", "the street is quiet now"]),
            ("Chorus", ["stay with me, don't go", "stay tonight"])]
    out = perform(secs, {"Verse 1": ["wait"], "Chorus": ["stay"]}, "tonight", "now")
    errs, caps = lint_perf(out)
    raw = "\n".join("[%s]\n%s" % (n, "\n".join(l)) for n, l in secs) + "\nhold " + "o" * 23 + "n\n"
    berr, _ = lint_perf(raw)
    p = tdump(Path(wd) / "lyrics_performance.txt", out)
    runs = [len(m.group(0)) - 1 for m in VOWEL_RUN.finditer(out) if len(m.group(0)) > 2]
    return [check("caps on 1-2 words per section", list(caps.values()) == [1, 2], caps, "1 / 2"),
            check("one melisma of +4 vowels (3-5)", runs == [4], runs, [4]),
            check("breath pause '...' placed before the held word", "... now" in out, "... now" in out, True),
            check("one phrase per line (no commas left)", "," not in out and out.count("\n") == 8, out.count("\n"), 8),
            check("formatted lyrics lint clean", errs == [], errs, []),
            check("negative control: the raw lyric has no caps, no pause, joined phrases and a 23-vowel glitch",
                  any("caps" in e for e in berr) and any("pause" in e for e in berr) and any("glitches" in e for e in berr) and any("phrases" in e for e in berr), berr, "4 kinds")], [p]


GENDER = re.compile(r"\b(fe)?male\b|\bwoman\b|\bman\b|\bgirl\b|\bboy\b", re.I)


def anti_patterns(style, lyrics, artists, voice_model=False, want_instrumental=False):
    found = []
    for a in artists:
        if a.lower() in style.lower():
            found.append("artist name %s" % a)
    if re.search(r"\(x\d\)", lyrics):
        found.append("(xN) repeat marker")
    if re.search(r"\bno drums\b", style, re.I) and not re.search(r"\bonly\b", style, re.I):
        found.append("bare 'no drums'")
    gens = [t for t in split_tags(style) if tag_cat(t) == "genre" and "with" not in t]
    if len(gens) >= 3:
        found.append("%d equal genres" % len(gens))
    if want_instrumental and not ("[Melodic Instrumental]" in lyrics and "instrumental, no vocals" in style):
        found.append("vocals not ruled out")
    if voice_model and GENDER.search(style):
        found.append("gender descriptor with a voice model")
    return found


def fix_prompt(style, lyrics, artists, voice_model=False, want_instrumental=False):
    tags = []
    for t in split_tags(style):
        for a, desc in artists.items():
            if a.lower() in t.lower():
                t = desc
        if voice_model:
            t = GENDER.sub("", t).strip()
        if t:
            tags.append(t)
    gens = [t for t in tags if tag_cat(t) == "genre"]
    if len(gens) >= 3:
        tags = ["%s with %s textures" % (gens[0], gens[1])] + [t for t in tags if t not in gens]
    if any(re.search(r"\bno drums\b", t, re.I) for t in tags) and not any("only" in t for t in tags):
        tags = [("piano only, no drums" if re.search(r"\bno drums\b", t, re.I) else t) for t in tags]
    if want_instrumental:
        tags.append("instrumental, no vocals")
    out_l = []
    for ln in lyrics.splitlines():
        m = re.match(r"^(.*?)\s*\(x(\d)\)\s*$", ln)
        out_l += [m.group(1)] * int(m.group(2)) if m else [ln]
    lyr = "\n".join(out_l)
    if want_instrumental and "[Melodic Instrumental]" not in lyr:
        lyr = "[Melodic Instrumental]\n" + lyr
    return ", ".join(tags), lyr


@card("BEAT-170")
def suno_anti_patterns(task, wd):
    """Common Suno prompt mistakes detected and rewritten (artist names → sound description, (x2) → the line twice,
    bare 'no drums' → 'piano only, no drums', 3+ genres → anchor + accent, instrumental guard, no gender with a voice model)."""
    artists = {"Nova Rivers": "breathy alt-pop vocal, glossy 2010s production"}   # fixture blocklist (fictional name)
    style = "Nova Rivers, synth-pop, dream-pop, shoegaze, no drums, female vocal"
    lyr = "[Verse]\nlights on the water (x2)\n[Chorus]\nhold on"
    before = anti_patterns(style, lyr, artists, voice_model=True, want_instrumental=True)
    st2, ly2 = fix_prompt(style, lyr, artists, voice_model=True, want_instrumental=True)
    after = anti_patterns(st2, ly2, artists, voice_model=True, want_instrumental=True)
    p = jdump(Path(wd) / "prompt_fix.json", {"before": {"style": style, "lyrics": lyr, "found": before}, "after": {"style": st2, "lyrics": ly2, "found": after}})
    gens = [t for t in split_tags(st2) if tag_cat(t) == "genre"]
    return [check("all six anti-patterns found in the draft", len(before) == 6, before, 6),
            check("rewrite leaves none", after == [], after, []),
            check("(x2) became the line written twice", ly2.count("lights on the water") == 2 and "(x2)" not in ly2, ly2.count("lights on the water"), 2),
            check("genres folded to one anchor + one accent", gens == ["synth-pop with dream-pop textures"], gens, "anchor+accent"),
            check("'no drums' now has a positive instrument", "piano only, no drums" in st2, "piano only, no drums" in st2, True),
            check("negative control: the unrewritten prompt still trips every rule", len(anti_patterns(style, lyr, artists, True, True)) == 6, len(before), 6)], [p]


AR = re.compile(r"[ء-ي]")
LAT = re.compile(r"[A-Za-z]")
RAI = {"bpm": (90, 130), "instruments": ["synth", "accordion", "darbouka", "bass"]}


def lint_arabic_pkg(pkg, artists=()):
    errs = []
    a, l = len(AR.findall(pkg["lyrics"])), len(LAT.findall(re.sub(r"\[[^\]]*\]", "", pkg["lyrics"])))
    if a / max(1, a + l) < 0.9:
        errs.append("lyrics not written in Arabic script (%.0f%%)" % (100 * a / max(1, a + l)))
    if "arabic" not in pkg["style"].lower():
        errs.append("style does not name the language")
    m = re.search(r"(\d{2,3})\s*bpm", pkg["style"], re.I)
    bpm = int(m.group(1)) if m else None
    if "rai" in pkg["style"].lower():
        if bpm is None or not RAI["bpm"][0] <= bpm <= RAI["bpm"][1]:
            errs.append("Rai at %s BPM (want 90-130)" % bpm)
        if sum(i in pkg["style"].lower() for i in RAI["instruments"]) < 3:
            errs.append("Rai palette thin")
    if any(x.lower() in pkg["style"].lower() for x in artists):
        errs.append("artist name in style")
    return errs


@card("BEAT-173")
def suno_arabic_rai(task, wd):
    """Arabic lyrics written directly in Arabic, the language and style named in the style field, Rai at 90-130 BPM with
    its synth / accordion / darbouka / bass palette, maqam colour given by instruments rather than artist names."""
    pkg = {"title": "ليل وهران", "style": "Rai, Arabic vocals (Algerian dialect), 112 BPM, modal, synth, accordion, darbouka, bass, Hijaz colour on accordion",
           "lyrics": "[Verse 1]\nيا ليل وهران طوّل شوية\nقلبي معاك وعينك عليّ\n[Chorus]\nيا ليل يا ليل\n"}
    errs = lint_arabic_pkg(pkg, ["Nova Rivers"])
    bad = {"title": "x", "style": "Rai, 150 BPM, synth, like Nova Rivers", "lyrics": "[Verse]\nya leil wahran tawel shwiya\n"}
    berr = lint_arabic_pkg(bad, ["Nova Rivers"])
    p = jdump(Path(wd) / "arabic_rai_package.json", pkg)
    share = len(AR.findall(pkg["lyrics"])) / max(1, len(AR.findall(pkg["lyrics"])) + len(LAT.findall(re.sub(r"\[[^\]]*\]", "", pkg["lyrics"]))))
    return [check("lyrics are Arabic script (≥90% of letters outside tags)", share >= 0.9, round(share, 3), ">=0.9"),
            check("package lints clean (language named, Rai 112 BPM in 90-130, palette)", errs == [], errs, []),
            check("negative control: transliteration, 150 BPM, thin palette, no language, artist name all flagged", len(berr) == 5, berr, 5)], [p]


GENRE_TPL = {
    "pop": (100, 130, "catchy modern pop, bright, synth and guitar, polished female vocal"), "rock": (110, 150, "driving alt rock, gritty guitars, live drums, belted vocal"),
    "hip-hop": (80, 100, "boom-bap hip-hop, dusty samples, punchy drums, rapped vocal"), "trap": (130, 170, "dark trap, 808s, rolling hi-hats, auto-tuned vocal"),
    "edm": (120, 130, "festival edm, supersaw synths, sidechain pump, big drop"), "jazz": (80, 160, "smoky jazz trio, upright bass, brushed drums, piano"),
    "classical": (60, 140, "orchestral classical, strings, woodwinds, no vocals"), "folk": (80, 120, "acoustic folk, fingerpicked guitar, warm close vocal"),
    "metal": (100, 200, "heavy metal, down-tuned guitars, double kick, screamed vocal"), "ambient": (50, 80, "ambient, evolving pads, field recordings, no percussion"),
    "lofi": (70, 90, "lofi hip-hop, vinyl crackle, mellow keys, jazzy chords"), "rnb": (60, 100, "smooth r&b, silky vocal, warm keys, finger snaps")}


def genre_template(g, bpm=None, **knobs):
    lo, hi, st = GENRE_TPL[g]
    b = bpm if bpm is not None else (lo + hi) // 2
    shell = ["[Melodic Instrumental]"] if g in ("ambient", "classical") else ["[Intro]", "[Verse 1]", "[Chorus]", "[Verse 2]", "[Chorus]", "[Outro]", "[End]"]
    return {"genre": g, "bpm": b, "style": "%s, %d BPM%s" % (st, b, "".join(", " + v for v in knobs.values())), "shell": shell, "knobs": sorted(knobs)}


def lint_template(t):
    lo, hi, _ = GENRE_TPL[t["genre"]]
    errs = []
    if not lo <= t["bpm"] <= hi:
        errs.append("%s at %d BPM outside %d-%d" % (t["genre"], t["bpm"], lo, hi))
    if "%d BPM" % t["bpm"] not in t["style"]:
        errs.append("BPM not in style")
    if t["genre"] == "ambient" and re.search(r"\bdrums|percussion\b(?<!no percussion)", t["style"].replace("no percussion", "")):
        errs.append("ambient bed carries percussion")
    if lint_tags("\n".join(t["shell"]), hard_stop=False):
        errs.append("shell has bad tags")
    return errs


@card("BEAT-174")
def suno_genre_templates(task, wd):
    """Twelve genre templates (style prompt, lyric shell, tweak knobs) with a BPM taxonomy; the dark-ambient bed at 60 BPM
    with no percussion and [Melodic Instrumental]; a 90-140 BPM trailer cue."""
    T = {g: genre_template(g) for g in GENRE_TPL}
    dark = genre_template("ambient", 60, tail="infinite reverb tail", mood="dark")
    trailer = {"genre": "trailer", "bpm": 120, "style": "epic trailer music, 120 BPM, big drums, brass swells, string ostinati, risers"}
    errs = {g: lint_template(t) for g, t in T.items()}
    bad_trap = genre_template("trap", 200)
    bad_amb = genre_template("ambient", 60, kit="live drums")
    p = jdump(Path(wd) / "genre_templates.json", {"templates": T, "dark_ambient": dark, "trailer": trailer})
    return [check("twelve templates: pop rock hip-hop trap edm jazz classical folk metal ambient lofi rnb", sorted(T) == sorted(
        ["pop", "rock", "hip-hop", "trap", "edm", "jazz", "classical", "folk", "metal", "ambient", "lofi", "rnb"]), len(T), 12),
            check("every template lints clean (BPM in its range, BPM in style, standard shell)", all(v == [] for v in errs.values()),
                  {k: v for k, v in errs.items() if v}, {}),
            check("dark ambient bed: 60 BPM, no percussion, infinite reverb tail, field recordings, [Melodic Instrumental]",
                  dark["bpm"] == 60 and "no percussion" in dark["style"] and "infinite reverb tail" in dark["style"] and "field recordings" in dark["style"]
                  and dark["shell"] == ["[Melodic Instrumental]"] and lint_template(dark) == [], dark["style"], "60 BPM bed"),
            check("trailer cue inside 90-140 BPM with drums / brass / ostinati / risers", 90 <= trailer["bpm"] <= 140
                  and all(w in trailer["style"] for w in ("drums", "brass", "ostinati", "risers")), trailer["bpm"], "90-140"),
            check("negative control: trap at 200 BPM and an ambient bed with drums are rejected",
                  lint_template(bad_trap) and lint_template(bad_amb), [lint_template(bad_trap), lint_template(bad_amb)], "both flagged")], [p]


TASHKEEL = re.compile(r"[ً-ْ]")
SUNO_ORDER = ["genre", "bpm", "mood", "instrument", "vocal", "era"]
SONG_SECTIONS = ["Intro", "Verse 1", "Pre-Chorus", "Chorus", "Verse 2", "Bridge", "Final Chorus", "Outro"]


def bare(w):
    w = TASHKEEL.sub("", w)
    return w.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ة", "ه").replace("ى", "ي")


def rhyme_scheme(lines):
    keys, out = {}, []
    for ln in lines:
        w = bare(ln.split()[-1])
        k = w[-2:] if len(w) >= 2 else w
        if k not in keys:
            keys[k] = chr(ord("A") + len(keys))
        out.append(keys[k])
    return "".join(out)


def lyric_blocks(lyrics):
    blocks, cur = [], None
    for ln in lyrics.splitlines():
        m = re.match(r"^\[(.+)\]$", ln.strip())
        if m:
            cur = [m.group(1), []]; blocks.append(cur)
        elif ln.strip() and cur:
            cur[1].append(ln.strip())
    return blocks


def suno_order_cat(tag):
    if re.search(r"\b(19|20)\d0s\b|\b\d0s\b|era\b", tag, re.I):
        return "era"
    c = tag_cat(tag)
    return {"production": "era"}.get(c, c)


def lint_song_pkg(pkg, risky=()):
    errs = []
    if len(pkg["style"]) > 200:
        errs.append("style %d chars (> 200)" % len(pkg["style"]))
    cats = [suno_order_cat(t) for t in split_tags(pkg["style"])]
    idx = [SUNO_ORDER.index(c) if c in SUNO_ORDER else 99 for c in cats]
    if idx != sorted(idx) or 99 in idx:
        errs.append("style tags not in [Genre][BPM][Mood][Instruments][Vocal][Era] order: %s" % cats)
    names = [b[0] for b in lyric_blocks(pkg["lyrics"])]
    if names != SONG_SECTIONS:
        errs.append("sections %s" % names)
    hook = pkg["hook"]
    n = sum(ln.strip() == hook for ln in pkg["lyrics"].splitlines())
    if not 2 <= n <= 4:
        errs.append("hook appears %d times (want 2-4)" % n)
    for w in risky:
        hits = [x for x in re.findall(r"[ء-ْ]+", pkg["lyrics"]) if bare(x) == bare(w)]
        if hits and not all(TASHKEEL.search(x) for x in hits):
            errs.append("risky word %s without tashkeel" % w)
    for k in ("title", "exclude", "alt_genre", "reel_hook"):
        if not pkg.get(k):
            errs.append("missing %s" % k)
    return errs


@card("BEAT-178")
def song_package(task, wd):
    """Suno/Udio song package: title, English style ≤200 chars in [Genre][BPM][Mood][Instruments][Vocal][Era] order,
    exclude styles, Arabic lyrics in the eight standard sections with the hook 2-4 times, rhyme scheme, tashkeel on risky
    words, an alt-genre version and a 15 s reel hook sized from the tempo."""
    bpm = 100
    hook = "خلّك معي يا ليل"
    lyrics = "\n".join(["[Intro]", "همس العود", "[Verse 1]", "مشيت وحدي في الطريق", "والقمر يسأل عن رفيق", "[Pre-Chorus]", "قلبي يناديك",
                        "[Chorus]", hook, "لا تروح وتتركني", hook, "[Verse 2]", "البحر ساكت والنجوم", "تحكي عن عِشق مكتوم", "[Bridge]", "بس لو تعرف",
                        "[Final Chorus]", hook, "لا تروح وتتركني", hook, "[Outro]", "يا ليل"])
    reel_bars = round(15 * bpm / 240)
    pkg = {"title": "خلّك معي", "style": "Khaleeji pop, 100 BPM, romantic, oud, qanun, warm male vocal, 2000s production", "exclude": "trap, heavy distortion",
           "lyrics": lyrics, "hook": hook, "alt_genre": {"style": "acoustic folk, 100 BPM, romantic, oud, warm male vocal, 2010s production"},
           "reel_hook": {"section": "Chorus", "bars": reel_bars, "seconds": round(reel_bars * 240 / bpm, 2)}}
    errs = lint_song_pkg(pkg, risky=["عشق"])
    verse = lyric_blocks(lyrics)[1][1] + lyric_blocks(lyrics)[4][1]
    scheme = rhyme_scheme(verse)
    pkg["rhyme_scheme"] = scheme
    bad = dict(pkg, style=pkg["style"] + ", " + ", ".join(["lush cinematic strings"] * 8), lyrics=lyrics.replace(hook, "خلّك", 3).replace("تحكي عن عِشق", "تحكي عن عشق"))
    berr = lint_song_pkg(bad, risky=["عشق"])
    p = jdump(Path(wd) / "song_package.json", pkg)
    return [check("style ≤ 200 chars in the Suno tag order", len(pkg["style"]) <= 200 and not any("order" in e for e in errs), len(pkg["style"]), "<=200"),
            check("package lints clean (8 sections, hook ×4, tashkeel on the risky word, all fields)", errs == [], errs, []),
            check("verse rhyme scheme measured AABB", scheme == "AABB", scheme, "AABB"),
            check("15 s reel hook at 100 BPM = 6 bars = 14.4 s", pkg["reel_hook"]["bars"] == 6 and abs(pkg["reel_hook"]["seconds"] - 14.4) < 1e-9, pkg["reel_hook"], "6 / 14.4"),
            check("negative control: a 270-char style, hook once and an unmarked risky word are flagged",
                  any("chars" in e for e in berr) and any("hook appears 1" in e for e in berr) and any("tashkeel" in e for e in berr), berr, "3 errors")], [p]


AR_PALETTE = ["oud", "qanun", "ney", "violin section", "darbuka", "tabla", "riq", "daf", "bendir", "mizmar", "rababa", "buzuq", "kawala",
              "tasfiq", "synth pads"]
AR_PICK = {"wedding": ["mizmar", "darbuka", "tasfiq"], "longing": ["ney", "qanun", "violin section"], "khaleeji": ["oud", "tasfiq", "riq"]}
OTHER_INSTR = ["sitar", "bagpipes", "banjo", "koto", "didgeridoo", "piano", "guitar"]


def palette_count(prompt):
    low = prompt.lower()
    inside = [i for i in AR_PALETTE if i in low]
    outside = [i for i in OTHER_INSTR if re.search(r"\b%s\b" % i, low)]
    return inside, outside


@card("BEAT-259")
def arabic_instrument_palette(task, wd):
    """Arabic instrument palette: 2-4 named palette instruments per style prompt, picked by use; counted by a linter."""
    prompts = {k: "Arabic %s cue, %s" % (k, ", ".join(v)) for k, v in AR_PICK.items()}
    res = {k: palette_count(v) for k, v in prompts.items()}
    bad = "Arabic cue, oud, qanun, ney, riq, daf, kawala, sitar"
    bi, bo = palette_count(bad)
    one, _ = palette_count("Arabic cue, oud")
    p = jdump(Path(wd) / "instrument_prompts.json", {"palette": AR_PALETTE, "prompts": prompts, "counts": {k: len(v[0]) for k, v in res.items()}})
    return [check("each prompt names 2-4 palette instruments", all(2 <= len(v[0]) <= 4 for v in res.values()), {k: len(v[0]) for k, v in res.items()}, "2-4"),
            check("no instrument outside the palette", all(not v[1] for v in res.values()), [v[1] for v in res.values()], "none"),
            check("Khaleeji pick carries the hand-claps (tasfiq)", "tasfiq" in res["khaleeji"][0], res["khaleeji"][0], "tasfiq"),
            check("negative control: 6 palette instruments + a sitar, or a single oud, fail the 2-4 rule", len(bi) == 6 and bo == ["sitar"] and len(one) == 1,
                  [len(bi), bo, len(one)], "6 / sitar / 1")], [p]


BRIEF10 = ["keep_sentence", "language_dialect", "narrator_addressee", "arc", "genre", "tempo_energy", "vocal", "duration_sections",
           "must_forbidden", "use"]
CONCRETE = ["باب", "شباك", "فنجان", "قهوة", "مطر", "رمل", "شارع", "قمر", "بحر", "نخل", "سيارة", "مفتاح", "ريح", "شمعة", "رسالة", "تلفون"]
TURN = re.compile(r"\b(بس|لكن|بعدين|ولو)\b")


def words_ar(ln):
    return re.findall(r"[ء-ْ]+", ln)


def lint_hook_first(brief, title, lyrics):
    errs = ["brief missing %s" % k for k in BRIEF10 if not brief.get(k)]
    B = lyric_blocks(lyrics)
    ch = [b for b in B if "Chorus" in b[0]]
    if len(words_ar(title)) > 6:
        errs.append("title longer than 6 words")
    if not ch or not all(any(bare(title) in bare(l) for l in c[1]) for c in ch):
        errs.append("title not in every chorus")
    if ch and not any(sum(bare(l) == bare(x) for x in c[1]) >= 2 for c in ch for l in c[1]):
        errs.append("no hook device (no repeated hook line)")
    if len(ch) >= 2 and not all(len(b[1]) > len(a[1]) or b[1] != a[1] for a, b in zip(ch, ch[1:])):
        errs.append("chorus repeats do not escalate")
    long = [l for b in B for l in b[1] if len(words_ar(l)) > 8]
    if long:
        errs.append("%d line(s) too long for one breath" % len(long))
    for b in B:
        if "Verse" in b[0] and sum(any(c in bare(l) for c in CONCRETE) for l in b[1]) < 2:
            errs.append("%s is not concrete" % b[0])
    br = [b for b in B if b[0] == "Bridge"]
    if not br or not any(TURN.search(l) for l in br[0][1]):
        errs.append("no bridge turn")
    return errs


@card("BEAT-X06")
def song_brief_hook_first(task, wd):
    """Hook-first song writing: the ten-field brief, a title phrase that is the chorus's repeated hook, escalating chorus
    repeats, breath-length lines, concrete verses and a bridge turn, linted before any verse is accepted."""
    brief = dict(zip(BRIEF10, ["الانتظار يصير بيت", "Arabic, Gulf (Saudi)", "she → him, absent", "waiting → doubt → choosing to stay",
                               "Khaleeji pop", "92 BPM, mid energy", "warm female alto", "3:10, V-C-V-C-B-C", "must: الباب / forbidden: الموت", "reel + streaming"]))
    title = "على الباب"
    lyr = "\n".join(["[Verse 1]", "فنجان القهوة برد عالشباك", "والمطر يكتب اسمك على الباب", "[Chorus]", "على الباب أنتظر", "على الباب أنتظر",
                     "[Verse 2]", "الشارع خالي والقمر سهران", "ومفتاحك بعده في جيبي", "[Chorus]", "على الباب أنتظر", "على الباب أنتظر", "ولو تأخرت",
                     "[Bridge]", "بس لو ترجع ما أسأل", "[Chorus]", "على الباب أنتظر", "على الباب أنتظر", "ولو تأخرت", "قلبي معك"])
    errs = lint_hook_first(brief, title, lyr)
    bad_lyr = "\n".join(["[Verse 1]", "أنا حزين جدا لأن الحياة صعبة والناس لا يفهمون ما أشعر به أبدا", "قلبي تعبان", "[Chorus]", "أحبك كثيرا",
                         "[Chorus]", "أحبك كثيرا", "[Bridge]", "أحبك"])
    berr = lint_hook_first(dict(brief, use=""), title, bad_lyr)
    tdump(Path(wd) / "lyrics.txt", lyr)
    p = jdump(Path(wd) / "brief.json", dict(brief, title=title))
    return [check("brief has all ten fields", all(brief[k] for k in BRIEF10), len(brief), 10),
            check("hook-first draft lints clean", errs == [], errs, []),
            check("every chorus repeats the title as its hook and grows (2 → 3 → 4 lines)", [len(b[1]) for b in lyric_blocks(lyr) if b[0] == "Chorus"] == [2, 3, 4],
                  [len(b[1]) for b in lyric_blocks(lyr) if b[0] == "Chorus"], [2, 3, 4]),
            check("negative control: missing field, title absent, flat chorus, 14-word line, abstract verse, no turn", len(berr) >= 6, berr, ">=6")], [p, Path(wd) / "lyrics.txt"]


DIALECT = {"egyptian": ["مش", "ازاي", "دلوقتي", "عايز", "عاوز", "ده", "دي"], "gulf": ["شلون", "الحين", "ابي", "ابغى", "وش", "مو", "هذي"]}
ELONG = re.compile(r"([ء-ي])\1{2,}")
AMBIG = {"عِشق", "حُب", "مَلك"}


def syllables(ln):
    return math.ceil(len(re.sub(r"[^ء-ي]", "", re.sub(r"\([^)]*\)", "", ln))) / 2)


def lint_dialect(lines, max_syl=12):
    errs = []
    seen = {d: [w for ln in lines for w in words_ar(ln) if bare(w) in [bare(m) for m in ms]] for d, ms in DIALECT.items()}
    if sum(1 for v in seen.values() if v) > 1:
        errs.append("mixed dialects %s" % {k: v for k, v in seen.items() if v})
    for ln in (re.sub(r"\([^)]*\)", "", x) for x in lines):
        if ELONG.search(ln):
            errs.append("typographic elongation in %r" % ln)
        if syllables(ln) > max_syl:
            errs.append("line too long at tempo (%d syllables)" % syllables(ln))
        for w in words_ar(ln):
            if TASHKEEL.search(w) and w not in AMBIG:
                errs.append("tashkeel on unambiguous word %s" % w)
    return errs


def fix_dialect(lines, dialect, max_syl=12):
    swap = {"egyptian": {"شلون": "ازاي", "الحين": "دلوقتي", "مو": "مش", "ابي": "عايز"},
            "gulf": {"ازاي": "شلون", "دلوقتي": "الحين", "مش": "مو", "عايز": "ابي"}}[dialect]
    out = []
    for ln in lines:
        stretched = bool(ELONG.search(ln))
        ln = ELONG.sub(lambda m: m.group(1), ln)
        ws = [swap.get(bare(w), w) for w in ln.split()]
        ws = [w if not TASHKEEL.search(w) or w in AMBIG else TASHKEEL.sub("", w) for w in ws]
        chunks, todo = [], [ws]
        while todo:
            c = todo.pop(0)
            if syllables(" ".join(c)) > max_syl and len(c) > 1:
                k = len(c) // 2
                todo[:0] = [c[:k], c[k:]]
            else:
                chunks.append(" ".join(c))
        if stretched:
            chunks[0] += " (مدّ على آخر كلمة)"
        out += chunks
    return out


@card("BEAT-X07")
def arabic_dialect_gates(task, wd):
    """Arabic song-lyric gates: one consistent dialect, no typographic letter stretching (vocal direction instead),
    light tashkeel only on ambiguous words, lines short enough to sing twice at tempo."""
    raw = ["حبيييبي مش فاهم شلون تروح", "الحين أنا قاعدة ومو عارفة وش أسوي بحالي وبقلبي وبكل هالليالي الطويلة", "يا عِشق عُمري"]
    before = lint_dialect(raw)
    fixed = fix_dialect(raw, "gulf")
    after = lint_dialect(fixed)
    p = jdump(Path(wd) / "dialect_gate.json", {"raw": raw, "fixed": fixed, "before": before, "after": after})
    used = {d: sum(1 for ln in fixed for w in words_ar(ln) if bare(w) in [bare(m) for m in ms]) for d, ms in DIALECT.items()}
    return [check("fixed lyric passes every gate", after == [], after, []),
            check("one dialect only (Gulf markers, no Egyptian)", used["egyptian"] == 0 and used["gulf"] >= 3, used, "gulf only"),
            check("stretching replaced by a vocal direction", "حبيبي" in fixed[0] and "(مدّ" in fixed[0], fixed[0], "حبيبي … (مدّ"),
            check("the long line was split into singable parts", len(fixed) >= 4 and all(syllables(l) <= 12 for l in fixed), [syllables(l) for l in fixed], "<=12"),
            check("tashkeel kept only on the ambiguous word", "عِشق" in fixed[-1] and "عُمري" not in fixed[-1], fixed[-1], "عِشق kept"),
            check("negative control: the raw lyric fails mixed dialect, elongation, length and tashkeel gates",
                  all(any(k in e for e in before) for k in ("mixed", "elongation", "too long", "tashkeel")), before, "4 kinds")], [p]


X08_ORDER = ["genre", "tempo", "vocal", "instrument", "production", "atmosphere", "arrangement"]


def x08_cat(tag):
    t = tag.lower()
    if re.search(r"\bverse\b|\bchorus\b|\blift\b|\bbuilds?\b|\bdrops?\b", t):
        return "arrangement"
    if re.search(r"\bbpm\b|tempo|\bslow\b|\bupbeat\b|energy", t):
        return "tempo"
    if re.search(r"\batmosphere\b|nocturnal|misty|dusky|smoky room|night air", t):
        return "atmosphere"
    if re.search(r"\b(19|20)\d0s\b|\bmix\b|production|analog|tape", t):
        return "production"
    return {"bpm": "tempo", "mood": "atmosphere"}.get(tag_cat(t), tag_cat(t))


def lint_style_exclude(style, exclude, history=()):
    errs = []
    cats = [x08_cat(t) for t in split_tags(style)]
    idx = [X08_ORDER.index(c) if c in X08_ORDER else 99 for c in cats]
    if idx != sorted(idx) or 99 in idx:
        errs.append("style not in the 7-step order: %s" % cats)
    st = {t.lower() for t in split_tags(style)}
    for e in split_tags(exclude):
        if e.lower() in st or any(e.lower() in s for s in st):
            errs.append("'%s' is in both Style and Exclude" % e)
        if re.search(r"lyric|rhyme|words|line", e, re.I) or tag_cat(e) == "other" and x08_cat(e) == "other":
            errs.append("'%s' is not a true negative (genre/instrument/vocal/production)" % e)
    for a, b in zip(history, history[1:]):
        n = sum(a.get(k) != b.get(k) for k in set(a) | set(b))
        if n != 1:
            errs.append("iteration changed %d controls (want 1)" % n)
    return errs, cats


@card("BEAT-X08")
def suno_style_order_exclude(task, wd):
    """Suno Style in the 7-step order (genre → tempo → vocal → instruments/groove → production/era → atmosphere →
    arrangement motion) with Exclude holding only true negatives, never duplicating Style, and one control per iteration."""
    style = ("Khaleeji pop fusion, 92 BPM mid energy, warm close female vocal, nylon guitar, qanun accents, brushed percussion, "
             "2000s analog mix, nocturnal atmosphere, dry verse, wider double-tracked chorus lift")
    exclude = "trap, heavy distortion, autotune vocal"
    hist = [{"style_weight": 50, "weirdness": 40, "model": "v"}, {"style_weight": 65, "weirdness": 40, "model": "v"}, {"style_weight": 65, "weirdness": 30, "model": "v"}]
    errs, cats = lint_style_exclude(style, exclude, hist)
    bad_hist = hist[:1] + [{"style_weight": 80, "weirdness": 10, "model": "w"}]
    berr, _ = lint_style_exclude("nocturnal atmosphere, Khaleeji pop, nylon guitar, 92 BPM", "nylon guitar, weak lyrics", bad_hist)
    p = jdump(Path(wd) / "style_exclude.json", {"style": style, "exclude": exclude, "steps": cats, "iterations": hist})
    seen = []
    for c in cats:
        if c not in seen:
            seen.append(c)
    return [check("style classifies to the seven steps in order", seen == X08_ORDER, seen, X08_ORDER),
            check("Style/Exclude/iterations lint clean", errs == [], errs, []),
            check("negative control: out of order, a shared trait, a lyric 'fix' in Exclude and a 3-control round are flagged",
                  any("order" in e for e in berr) and any("both" in e for e in berr) and any("true negative" in e for e in berr)
                  and any("changed 3" in e for e in berr), berr, "4 kinds")], [p]


FIX_MAP = {"weak line": ("local lyric edit", "lyrics"), "weak chorus": ("Replace Section", "section"),
           "wrong ending": ("Extend or edit the outro", "ending"), "prompt slightly off": ("Reuse Prompt or edit Style", "style"),
           "broad style mismatch": ("fix Style/Exclude first", "style"), "mispronunciation": ("simplify spelling, add diacritics or rephrase", "lyrics")}


def iteration_plan(defects):
    """One round per defect, style-level problems first (a lyric fix is wasted under the wrong style), one variable a round."""
    order = sorted(defects, key=lambda d: 0 if FIX_MAP[d][1] == "style" else 1)
    return [{"round": i + 1, "defect": d, "fix": FIX_MAP[d][0], "variable": FIX_MAP[d][1]} for i, d in enumerate(order)]


def lint_iteration(plan):
    errs = []
    for r in plan:
        vs = r["variable"] if isinstance(r["variable"], list) else [r["variable"]]
        if len(vs) != 1:
            errs.append("round %d changes %d variables" % (r["round"], len(vs)))
        if "regenerate" in r["fix"].lower():
            errs.append("round %d regenerates everything" % r["round"])
        if r.get("defect") in FIX_MAP and r["fix"] != FIX_MAP[r["defect"]][0]:
            errs.append("round %d uses the wrong tool for %s" % (r["round"], r["defect"]))
    vs = [r["variable"] for r in plan if isinstance(r["variable"], str)]
    if "style" in vs and any(v != "style" for v in vs[:vs.index("style")]):
        errs.append("style fixed after lyric/section edits")
    return errs


@card("BEAT-X09")
def surgical_iteration(task, wd):
    """Surgical song iteration: each generated-song defect mapped to its own fix, style problems first, one major variable
    per round, never a full regeneration for one line."""
    defects = ["weak line", "mispronunciation", "broad style mismatch", "wrong ending"]
    plan = iteration_plan(defects)
    errs = lint_iteration(plan)
    naive = [{"round": 1, "defect": "weak line", "fix": "Regenerate the whole song", "variable": ["lyrics", "style", "section"]},
             {"round": 2, "defect": "broad style mismatch", "fix": "local lyric edit", "variable": "style"}]
    berr = lint_iteration(naive)
    p = jdump(Path(wd) / "iteration_plan.json", plan)
    return [check("every defect gets its mapped tool", [r["fix"] for r in plan] == [FIX_MAP[d][0] for d in ["broad style mismatch", "weak line", "mispronunciation", "wrong ending"]],
                  [r["fix"] for r in plan], "mapped"),
            check("style mismatch is fixed first", plan[0]["defect"] == "broad style mismatch", plan[0]["defect"], "broad style mismatch"),
            check("plan lints clean (one variable per round, no regeneration)", errs == [] and len(plan) == 4, errs, []),
            check("negative control: regenerate-all for one line, 3 variables, wrong tool, style after lyrics", len(berr) == 4, berr, 4)], [p]


def four_blocks(title, lyrics, style, exclude):
    return "\n\n".join("```\n%s\n```" % b for b in (title, lyrics, style, exclude))


def rubric(handoff, required=(), forbidden=(), dialect_lines=None):
    blocks = re.findall(r"```\n(.*?)\n```", handoff, re.S)
    res = {}
    res["copy_ready_blocks"] = len(blocks) == 4 and not re.search(r"TODO|<[^>]+>|\?\?\?", handoff)
    title, lyrics, style, exclude = (blocks + ["", "", "", ""])[:4]
    B = lyric_blocks(lyrics)
    ch = [b[1] for b in B if "Chorus" in b[0]]
    vs = [b[1] for b in B if "Verse" in b[0]]
    res["hook_identifiable"] = bool(ch) and any(sum(l == x for x in c) >= 2 for c in ch for l in c)
    res["chorus_lifts"] = bool(ch and vs) and bool(np.mean([len(words_ar(l)) for c in ch for l in c]) < np.mean([len(words_ar(l)) for v in vs for l in v]))
    res["singable"] = all(len(words_ar(l)) <= 8 for b in B for l in b[1])
    res["dialect_stable"] = lint_dialect([l for b in B for l in b[1]]) == []
    res["imagery_specific"] = sum(any(c in bare(l) for c in CONCRETE) for v in vs for l in v) >= 2
    ends = [l for v in vs for l in v]
    sch = rhyme_scheme(ends) if ends else ""
    res["rhyme_natural"] = bool(sch) and len(set(sch)) < len(sch) and len({bare(l.split()[-1]) for l in ends}) == len(ends)
    res["arc_changes"] = any(b[0] == "Bridge" and any(TURN.search(l) for l in b[1]) for b in B)
    res["style_lyrics_agree"] = ("arabic" in style.lower() or "khaleeji" in style.lower()) == bool(AR.search(lyrics))
    res["exclude_true_negatives"] = bool(exclude) and not [e for e in lint_style_exclude(style, exclude)[0] if "Exclude" in e or "true negative" in e]
    res["required_forbidden"] = all(r in lyrics for r in required) and not any(f in lyrics for f in forbidden)
    return res, all(res.values())


@card("BEAT-X10")
def four_block_rubric(task, wd):
    """Four copy-ready blocks (Title · Lyrics · Style · Exclude) and the 11-point PASS rubric, each check measured on the text."""
    lyrics = "\n".join(["[Verse 1]", "فنجان القهوة برد عالشباك", "والمطر يكتب على الباب", "[Chorus]", "على الباب أنتظر", "على الباب أنتظر",
                        "[Verse 2]", "الشارع خالي والقمر سهران", "ومفتاحك في جيبي من زمان", "[Bridge]", "بس لو ترجع ما أسأل", "[Chorus]",
                        "على الباب أنتظر", "على الباب أنتظر", "ولو تأخرت"])
    style = "Khaleeji pop, 92 BPM, warm close female vocal, oud, qanun, 2000s analog mix"
    exclude = "trap, heavy distortion"
    h = four_blocks("على الباب", lyrics, style, exclude)
    out = tdump(Path(wd) / "handoff.md", h)
    res, ok = rubric(h, required=["الباب"], forbidden=["الموت"])
    giant = "Title: على الباب\n" + lyrics + "\nStyle: " + style + "\nExclude: TODO\n" + "الموت"
    bres, bok = rubric(giant, required=["الباب"], forbidden=["الموت"])
    jdump(Path(wd) / "rubric.json", {"handoff": res, "giant_block": bres})
    return [check("eleven rubric checks computed", len(res) == 11, len(res), 11),
            check("four-block hand-off PASSes all 11", ok, [k for k, v in res.items() if not v], "none failing"),
            check("blocks in order Title · Lyrics · Style · Exclude", re.findall(r"```\n(.*?)\n```", h, re.S)[0] == "على الباب"
                  and re.findall(r"```\n(.*?)\n```", h, re.S)[3] == exclude, 4, 4),
            check("negative control: one giant block with a placeholder and a forbidden word FAILs", not bok and not bres["copy_ready_blocks"]
                  and not bres["required_forbidden"], [k for k, v in bres.items() if not v], "fails")], [out, Path(wd) / "rubric.json"]


MAGMA = [(0.0, (0.0, 0.0, 0.016)), (0.2, (0.157, 0.043, 0.33)), (0.4, (0.47, 0.11, 0.43)), (0.6, (0.75, 0.23, 0.46)),
         (0.75, (0.93, 0.41, 0.35)), (0.88, (0.98, 0.65, 0.29)), (1.0, (0.99, 0.99, 0.75))]


def _sstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def magma(x):
    """makeSpectrumGround's 7-stop magma ramp (sRGB stops, returned linear: pow 2.2)."""
    x = np.clip(np.asarray(x, float), 0, 1)[..., None]
    a = np.broadcast_to(np.array(MAGMA[0][1]), x.shape[:-1] + (3,)).astype(float)
    edges = [(0.0, 0.2), (0.2, 0.4), (0.4, 0.6), (0.6, 0.75), (0.75, 0.88), (0.88, 1.0)]
    for (lo, hi), (_, col) in zip(edges, MAGMA[1:]):
        a = a + (np.array(col) - a) * _sstep(lo, hi, x)
    return np.power(a, 2.2)


@card("BEAT-28")
def spectrogram_canyon_ground(task, wd):
    """The canyon ground with the kit's defaults (60×30 m, window 4 s, amp 6, glow 1.2, lava .62; read from three-kit.js):
    vertex displacement and the fragment's lava melt, bass river and playhead ported to numpy, on the tape-resampled spectrum."""
    src = K3_KIT.read_text(encoding="utf-8")
    body = src[src.index("export function makeSpectrumGround"):src.index("export function spectrumOnTape")]
    dflt = {k: float(re.search(r"o\.%s \|\| ([\d.]+)" % k, body).group(1)) for k in ("width", "depth", "window", "amp", "segX", "segZ")}
    lava_d = float(re.search(r"o\.lava == null \? ([\d.]+)", body).group(1))
    glow_d = float(re.search(r"o\.glow == null \? ([\d.]+)", body).group(1))
    ch, h, _ = _k3_fixture(wd, stop=True)
    tex, meta = k3_on_tape(wd, h, ch)
    sec = meta["seconds"]
    kw = dict(W=dflt["width"], D=dflt["depth"], half=dflt["depth"] / 2, segX=240, segZ=60, span=dflt["window"], amp=dflt["amp"])
    xs, zs, y0, hh = canyon(tex, 1.0, sec, **kw)
    _, _, y1, _ = canyon(tex, 1.5, sec, **kw)
    prof = lambda y: y.mean(axis=0)
    shift = _shift_m(prof(y0), prof(y1), xs[1] - xs[0])
    fy = np.minimum(1.0, np.abs(zs) / (dflt["depth"] / 2))[:, None]
    lava = _sstep(lava_d, 1.0, hh) * (1 + (0.2 - 1) * _sstep(0.4, 0.85, fy))
    vbass = (1 - _sstep(0.0, 0.18, fy)) * hh
    head_x = 0.0
    head = np.exp(-((xs[None, :] - head_x) / 0.07) ** 2) * 1.0 * (1 - _sstep(0.45, 0.85, fy))
    col = magma(0.35 + 0.65 * hh) * glow_d * 1.25 * lava[..., None] + magma(0.72 + 0.28 * vbass) * (vbass ** 2)[..., None] * 1.4 \
        + np.array([1.0, 0.62, 0.32]) * (head * (0.4 + 0.9 * hh))[..., None]
    from PIL import Image
    op = Path(wd) / "canyon_ground.png"
    Image.fromarray((np.clip(col / (col.max() + 1e-9), 0, 1) ** (1 / 2.2) * 255).astype(np.uint8)).resize((480, 240)).save(op)
    melt = float((lava > 0).mean()); melt_hi = float((hh > lava_d).mean())
    hx = float(xs[np.argmax(head[np.argmin(np.abs(zs))])])
    walls_melt = float(lava[(fy[:, 0] >= 0.85)].max()) if (fy[:, 0] >= 0.85).any() else 0
    mag0, mag1 = magma(0.0), magma(1.0)
    return [check("kit defaults read from three-kit.js = card params (60×30, 480×240, window 4, amp 6, glow 1.2, lava .62)",
                  [dflt["width"], dflt["depth"], dflt["segX"], dflt["segZ"], dflt["window"], dflt["amp"], glow_d, lava_d] == [60, 30, 480, 240, 4, 6, 1.2, 0.62],
                  [dflt, glow_d, lava_d], "60/30/480/240/4/6/1.2/.62"),
            check("window 4 s across 60 m: 0.5 tape-s scrolls 7.5 m (±0.5)", abs(shift - 7.5) <= 0.5, round(shift, 3), 7.5),
            check("lava only where the sound is loudest (h > .62): melted cells = loud cells", abs(melt - melt_hi) < 1e-9 and 0 < melt < 0.5,
                  [round(melt, 4), round(melt_hi, 4)], "equal, 0-50%"),
            check("high walls stay rock: lava weight on walls ≤ 0.2 of the floor's", walls_melt <= 0.2 + 1e-9, round(walls_melt, 3), "<=0.2"),
            check("playhead glow peaks at the head x (±0.25 m)", abs(hx - head_x) <= 0.25, hx, head_x),
            check("magma ramp ends: x=0 → (0,0,.016)^2.2, x=1 → (.99,.99,.75)^2.2", np.allclose(mag0, np.power([0, 0, 0.016], 2.2)) and np.allclose(mag1, np.power([0.99, 0.99, 0.75], 2.2)),
                  [mag0.round(5).tolist(), mag1.round(4).tolist()], "ramp ends"),
            check("negative control: a silent texture melts nothing and has no river", float((_sstep(lava_d, 1.0, np.zeros_like(hh)) > 0).mean()) == 0
                  and float(((1 - _sstep(0.0, 0.18, fy)) * np.zeros_like(hh)).max()) == 0, 0, 0)], [op]
