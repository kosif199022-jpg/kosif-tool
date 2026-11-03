"""music-beat-sound: method cards as real programs with known-answer checks.

Every runner synthesises a deterministic fixture in its work folder (click tracks at a known BPM, tones, speech-like
bursts, noise), applies the card's method (its what/how/params) with the repo's own scripts where they exist
(kosif-montage-motion score.py / qa.py / ambience.py / songreel.py / offline.mjs, the HyperFrames CLI and its skill
scripts), otherwise with numpy / ffmpeg implementing the card's stated formula, and measures the output against the
known answer. Each runner carries a negative control: the same measurement on the unprocessed input fails.
"""
import importlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np

from _harness import card, check, fx

HERE = Path(__file__).resolve().parent
SKILLS = HERE.parents[1]
VEND = SKILLS / "kosif-superpowers/vendor/100-superskills/skills/kosif-montage-motion/scripts"
ARC = SKILLS / "kosif-superpowers/vendor/100-superskills/skills/audio-reactive-captions-studio/scripts"
PVE = SKILLS / "kosif-superpowers/vendor/100-superskills/skills/pro-video-editor-ffmpeg/scripts"
SR = 48000

GAPS: dict = {}


# ───────────────────────── shared helpers ─────────────────────────
def vmod(name, where=VEND):
    if str(where) not in sys.path:
        sys.path.insert(0, str(where))
    return importlib.import_module(name)


def hf_root():
    w = shutil.which("hyperframes")
    if not w:
        return None
    for p in Path(w).resolve().parents:
        if (p / "dist" / "skills").is_dir():
            return p
    return None


def sh(cmd, cwd=None, timeout=60, env=None):
    done = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, timeout=timeout, cwd=cwd,
                          stdin=subprocess.DEVNULL, env=env)
    if done.returncode:
        raise RuntimeError("command failed (%d): %s %s" % (done.returncode, " ".join(map(str, cmd))[:200], (done.stderr or done.stdout)[-500:]))
    return done.stdout


def ff(*args, timeout=60):
    return fx.ffmpeg(*args, timeout=timeout)


def tt(d, sr=SR):
    return np.arange(int(round(d * sr))) / sr


def tone(f, d, amp=0.5, sr=SR):
    return amp * np.sin(2 * np.pi * f * tt(d, sr))


def save(wd, name, x, sr=SR):
    return fx.write_wav(Path(wd) / name, x, sr)


def load(p):
    x, sr = fx.read_wav(p)
    return x.mean(1), sr


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


def peak_hz(x, sr=SR):
    w = np.hanning(len(x))
    X = np.abs(np.fft.rfft(x * w))
    f = np.fft.rfftfreq(len(x), 1 / sr)
    X[f < 15] = 0
    return float(f[int(np.argmax(X))])


def band_db(x, sr, lo, hi):
    X = np.abs(np.fft.rfft(x * np.hanning(len(x)))) ** 2
    f = np.fft.rfftfreq(len(x), 1 / sr)
    return 10 * math.log10(float(X[(f >= lo) & (f < hi)].sum()) + 1e-20)


def envelope(x, sr, ms=5.0):
    n = max(1, int(sr * ms / 1000))
    return np.sqrt(np.convolve(np.square(x), np.ones(n) / n, mode="same"))


def onsets(x, sr, rel=0.3, gap=0.06):
    """Independent measurement: rising crossings of rel·max of a 5 ms envelope, at least gap apart."""
    e = envelope(x, sr)
    thr = rel * e.max()
    up = np.flatnonzero((e[1:] >= thr) & (e[:-1] < thr)) + 1
    out, last = [], -1e9
    for i in up:
        if i / sr - last >= gap:
            out.append(i / sr)
            last = i / sr
    return out


def clicks(bpm, secs, sr=SR, f=1000.0, dur=0.03, amp=0.8, offset=0.0, accent=4):
    x = np.zeros(int(secs * sr))
    times, k = [], 0
    t0 = tt(dur, sr)
    while offset + k * 60 / bpm < secs - dur:
        t = offset + k * 60 / bpm
        i = int(round(t * sr))
        a = amp if k % accent == 0 else amp * 0.6
        x[i:i + len(t0)] += a * np.sin(2 * np.pi * f * t0) * np.exp(-t0 * 120)
        times.append(round(t, 4))
        k += 1
    return x, times


def kick(sr=SR, amp=0.9):
    t = tt(0.25, sr)
    return amp * np.sin(2 * np.pi * np.cumsum(46 + 110 * np.exp(-t / 0.032)) / sr) * np.exp(-t / 0.08)


def drum_loop(bpm, secs, sr=SR, seed=1):
    """Kick on every beat, hats on off-beats: a rhythmic fixture at a known tempo."""
    rng = np.random.default_rng(seed)
    x = np.zeros(int(secs * sr))
    k, times = kick(sr), []
    b = 0
    while b * 60 / bpm < secs - 0.3:
        i = int(b * 60 / bpm * sr)
        x[i:i + len(k)] += k
        times.append(round(b * 60 / bpm, 4))
        j = int((b + 0.5) * 60 / bpm * sr)
        h = rng.standard_normal(int(0.03 * sr)) * np.exp(-tt(0.03, sr) / 0.008) * 0.15
        x[j:j + len(h)] += h[: len(x) - j]
        b += 1
    return x, times


def speechlike(secs, spans, sr=SR, f0=140.0, amp=0.35, seed=3):
    """Voiced harmonic bursts (f0 + 10 partials, ~4 Hz syllable envelope) inside the given spans; silence elsewhere."""
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


def music_bed(secs, sr=SR, amp=0.3):
    t = tt(secs, sr)
    x = sum(np.sin(2 * np.pi * f * t) for f in (220, 277.2, 329.6, 440))
    return amp * x / 4 * (0.85 + 0.15 * np.sin(2 * np.pi * 0.5 * t))


def ebur(p):
    """ffmpeg ebur128 (BS.1770) measurement: integrated LUFS, LRA, true peak dBTP."""
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(p), "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True, timeout=60, stdin=subprocess.DEVNULL).stderr
    summ = err[err.rfind("Summary:"):]
    g = lambda pat: float(re.search(pat, summ, re.S).group(1))
    return {"I": g(r"I:\s+(-?[\d.]+|-inf) LUFS"), "LRA": g(r"LRA:\s+(-?[\d.]+) LU"),
            "TP": g(r"True peak:\s+Peak:\s+(-?[\d.]+|-inf) dBFS")}


def loudnorm_measure(p, I, TP, LRA):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(p), "-af",
                          "loudnorm=I=%s:TP=%s:LRA=%s:print_format=json" % (I, TP, LRA), "-f", "null", "-"],
                         capture_output=True, text=True, timeout=60, stdin=subprocess.DEVNULL).stderr
    return json.loads(err[err.rfind("{"):err.rfind("}") + 1])


def loudnorm2(src, out, I=-14, TP=-1.5, LRA=11, post="", codec=("-c:a", "pcm_s16le"), sr=48000):
    m = loudnorm_measure(src, I, TP, LRA)
    af = ("loudnorm=I=%s:TP=%s:LRA=%s:measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:offset=%s:"
          "linear=true:print_format=summary,aresample=%d" % (I, TP, LRA, m["input_i"], m["input_tp"], m["input_lra"],
                                                            m["input_thresh"], m["target_offset"], sr))
    if post:
        af += "," + post
    ff("-i", src, "-af", af, *codec, out)
    return m


def song_fixture(wd, secs=4.0, level=-30.0, name="mix_in.wav", sr=SR):
    """A music-like mix (chord + kicks) scaled to a known RMS level in dBFS."""
    x = music_bed(secs, sr) + 0.6 * drum_loop(120, secs, sr)[0]
    x *= 10 ** ((level - dbfs(x)) / 20)
    return save(wd, name, x, sr), x


def sidechain(music, voice, out, thr=0.02, ratio=12, attack=20, release=300, makeup=1, extra=""):
    ff("-i", music, "-i", voice, "-filter_complex",
       "[0:a][1:a]sidechaincompress=threshold=%s:ratio=%s:attack=%s:release=%s:makeup=%s%s[d]"
       % (thr, ratio, attack, release, makeup, extra), "-map", "[d]", "-c:a", "pcm_s16le", out)
    return Path(out)


def duck_fixture(wd, secs=4.0, spans=((1.0, 2.6),)):
    m = save(wd, "music.wav", music_bed(secs))
    v = save(wd, "voice.wav", speechlike(secs, spans))
    return m, v


def duck_depth(ducked, spans, margin=0.4, secs=4.0):
    """Music level change (dB) inside the voice span (after the attack) against outside it."""
    x, sr = load_any(ducked)
    a, b = spans[0]
    inside = seg_db(x, sr, a + margin, b - 0.1)
    outside = seg_db(x, sr, 0.1, a - 0.1)
    return inside - outside


# ───────────────────────── video helpers ─────────────────────────
def write_video(path, frame_fn, n, fps=30, size=(160, 90), audio=None, extra=()):
    w, h = size
    buf = b"".join(np.ascontiguousarray(np.clip(frame_fn(i), 0, 255).astype(np.uint8)).tobytes() for i in range(n))
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (w, h),
           "-r", str(fps), "-i", "-"]
    if audio:
        cmd += ["-i", str(audio), "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "192k", "-shortest"]
    cmd += ["-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", *extra, str(path)]
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


def cut_video(path, cuts, secs, fps=30, size=(96, 54), audio=None):
    """A shot plan rendered: each shot a different colour field with a moving bar, hard cuts at the given times."""
    bounds = [0.0] + list(cuts) + [secs + 1]

    def frame(i):
        t = i / fps
        k = max(j for j in range(len(bounds) - 1) if bounds[j] <= t + 1e-9)
        a = solid(size, PAL[k % len(PAL)])
        x = int((t * 40) % size[0])
        a[:, x:x + 3] = 255
        return a
    return write_video(path, frame, int(round(secs * fps)), fps, size, audio)


def cut_frames(path, size=(48, 27), thr=40.0):
    fr = fx.frames(path, size)
    d = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2, 3))
    return [int(i + 1) for i in np.flatnonzero(d > thr)], fr


def frame_err(found, expected):
    """Worst distance in frames between expected cut frames and the nearest detected cut."""
    if not expected:
        return 0
    if not found:
        return 999
    return max(min(abs(f - e) for f in found) for e in expected)


def grid(bpm, n, offset=0.0):
    return [round(offset + k * 60.0 / bpm, 6) for k in range(n)]


def jdump(p, obj):
    Path(p).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    return Path(p)


def hf_project(d, body, w=160, h=90, dur=2.0, head=""):
    d = Path(d)
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(
        '<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:#000;width:%dpx;height:%dpx;overflow:hidden}</style>%s</head>'
        '<body><div id="root" data-composition-id="main" data-width="%d" data-height="%d" data-duration="%s" data-start="0" data-no-timeline>%s</div>'
        '</body></html>' % (w, h, head, w, h, dur, body), encoding="utf-8")
    return d


def hf(*args, cwd=None, timeout=120):
    return sh(["hyperframes", *args], cwd=cwd, timeout=timeout)


def hf_render(d, out, timeout=120):
    hf("render", ".", "-o", str(out), cwd=d, timeout=timeout)
    return Path(out)


# ───────────────────────── loudness & mastering ─────────────────────────
def _loud(wd, I, TP, LRA, level=-30.0, tol=0.5, tp_lim=None, codec=("-c:a", "pcm_s16le"), ext="wav", name="norm", post=""):
    src, _ = song_fixture(wd, 4.0, level)
    out = Path(wd) / ("%s.%s" % (name, ext))
    loudnorm2(src, out, I, TP, LRA, post=post, codec=codec)
    a, b = ebur(src), ebur(out)
    tp_lim = TP + 0.5 if tp_lim is None else tp_lim
    return [check("%s integrated loudness on target" % name, abs(b["I"] - I) <= tol, b["I"], I),
            check("%s true peak under ceiling" % name, b["TP"] <= tp_lim, b["TP"], "<= %s" % tp_lim),
            check("negative control: input is not on target", abs(a["I"] - I) > tol, a["I"], "!= %s" % I)], [out]


@card("BEAT-01")
def two_pass_loudnorm(task, wd):
    """pass 1 measures, pass 2 applies measured_* linearly (aresample 48000), AAC so TP -1.5 measures about -1 dBTP."""
    checks, outs = _loud(wd, -14, -1.5, 11, codec=("-c:a", "aac", "-b:a", "256k"), ext="m4a", tol=1.0, tp_lim=-0.9)
    sr = int(fx.probe(outs[0])["streams"][0]["sample_rate"])
    return checks + [check("pass 2 resampled to 48 kHz", sr == 48000, sr, 48000)], outs


@card("BEAT-09")
def bs1770_meter_node(task, wd):
    """offline.mjs measureLoudness / normalizeLoudness run in node: 1 kHz sine at 1.0 in one channel = -3.01 LUFS,
    normalise to -14 with a -1.5 dB peak ceiling; spiky content is limited by the peak."""
    mod = VEND / "web/static/studio/offline.mjs"
    js = Path(wd) / "probe.mjs"
    js.write_text("""
import {measureLoudness, normalizeLoudness} from %s;
import {writeFileSync} from 'fs';
const sr=48000, n=sr*3;
const one=[new Float32Array(n), new Float32Array(n)];
for(let i=0;i<n;i++) one[0][i]=Math.sin(2*Math.PI*1000*i/sr);
const ref=measureLoudness(one, sr);
const q=[new Float32Array(n), new Float32Array(n)];
for(let i=0;i<n;i++){const v=0.05*Math.sin(2*Math.PI*440*i/sr); q[0][i]=v; q[1][i]=v;}
const before=measureLoudness(q, sr);
const r=normalizeLoudness(q, sr, -14, -1.5);
const s=[new Float32Array(n), new Float32Array(n)];
for(let i=0;i<n;i+=sr/2){ for(let k=0;k<200;k++){const v=0.02*Math.sin(k)+(k<5?0.5:0); s[0][i+k]=v; s[1][i+k]=v;} }
const r2=normalizeLoudness(s, sr, -14, -1.5);
const buf=Buffer.alloc(n*4); for(let i=0;i<n;i++) buf.writeFloatLE(q[0][i], i*4);
writeFileSync('norm.f32', buf);
console.log(JSON.stringify({ref, before, r, r2}));
""" % json.dumps(mod.as_uri()), encoding="utf-8")
    res = json.loads(sh(["node", js.name], cwd=wd).strip().splitlines()[-1])
    raw = Path(wd) / "norm.f32"
    out = Path(wd) / "norm.wav"
    ff("-f", "f32le", "-ar", "48000", "-ac", "1", "-i", raw, "-af", "pan=stereo|c0=c0|c1=c0", "-c:a", "pcm_s16le", out)
    m = ebur(out)
    lim = res["r2"]
    jdump(Path(wd) / "loudness.json", {**res, "ffmpeg_ebur128": m})
    return [check("1 kHz sine at 1.0 in one channel reads -3.01 LUFS", abs(res["ref"]["lufs"] - (-3.01)) < 0.1, res["ref"]["lufs"], -3.01),
            check("normalised file measures -14 LUFS (ffmpeg ebur128)", abs(m["I"] + 14) <= 0.5, m["I"], -14),
            check("meter reports after = -14", abs(res["r"]["after"] + 14) < 0.3, res["r"]["after"], -14),
            check("spiky content limited by the -1.5 dB peak", bool(lim["limitedByPeak"]) and lim["peakDb"] <= -1.49, lim, "limitedByPeak, peak<=-1.5"),
            check("negative control: input was not at -14", abs(res["before"]["lufs"] + 14) > 3, res["before"]["lufs"], "!= -14")], [out, Path(wd) / "loudness.json"]


@card("BEAT-18")
def master_minus14_alimiter(task, wd):
    """montage/reel: loudnorm I=-14 TP=-1.5 LRA=11 + alimiter limit 0.84 attack 3 release 60 → AAC; mux: two-pass linear I=-14 TP=-1."""
    src, _ = song_fixture(wd, 6.0, -28)
    one = Path(wd) / "reel_master.m4a"
    ff("-i", src, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.84:level=false:attack=3:release=60,aresample=48000",
       "-c:a", "aac", "-b:a", "256k", one)
    two = Path(wd) / "mux_master.wav"
    loudnorm2(src, two, -14, -1, 11)
    a, b, c = ebur(src), ebur(one), ebur(two)
    pk = peak_db(load_any(one)[0])
    return [check("one-pass + limiter lands -14 ±1.5 LUFS", abs(b["I"] + 14) <= 1.5, b["I"], -14),
            check("limiter keeps decoded AAC samples under -1.0 dBFS", pk <= -1.0, pk, "<= -1.0"),
            check("two-pass linear mux on -14 ±0.5", abs(c["I"] + 14) <= 0.5, c["I"], -14),
            check("two-pass true peak <= -0.5 dBTP", c["TP"] <= -0.5, c["TP"], "<= -0.5"),
            check("negative control: input far from -14", abs(a["I"] + 14) > 5, a["I"], "!= -14")], [one, two]


@card("BEAT-39")
def master_generated_music(task, wd):
    """Two-pass loudnorm + limiter, measured with ebur128=peak=true: web -14/-1 dBTP and music bed under SFX -18/-1.5."""
    c1, o1 = _loud(wd, -14, -1, 11, name="web", post="alimiter=limit=0.89:level=false")
    c2, o2 = _loud(wd, -18, -1.5, 11, name="bed", post="alimiter=limit=0.84:level=false")
    return c1 + c2, o1 + o2


@card("BEAT-73")
def loudnorm_lra7(task, wd):
    """smart_montage: loudnorm=I=-14:LRA=7:TP=-1.0 then AAC 256k; gate -14 ±1.5 LUFS."""
    src, _ = song_fixture(wd, 6.0, -30)
    out = Path(wd) / "final.m4a"
    ff("-i", src, "-af", "loudnorm=I=-14:LRA=7:TP=-1.0", "-ar", "48000", "-c:a", "aac", "-b:a", "256k", out)
    a, b = ebur(src), ebur(out)
    br = int(fx.probe(out)["streams"][0].get("bit_rate", 0))
    return [check("gate -14 ±1.5 LUFS", abs(b["I"] + 14) <= 1.5, b["I"], -14),
            check("AAC stream written", fx.probe(out)["streams"][0]["codec_name"] == "aac", fx.probe(out)["streams"][0]["codec_name"], "aac"),
            check("negative control: input outside the gate", abs(a["I"] + 14) > 1.5, a["I"], "outside -14±1.5")], [out]


@card("BEAT-77")
def broadcast_master_aac(task, wd):
    """loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.84:level=false:attack=3:release=60 → AAC 256k 48 kHz."""
    src, _ = song_fixture(wd, 6.0, -26, sr=44100)
    out = Path(wd) / "mix.m4a"
    ff("-i", src, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.84:level=false:attack=3:release=60",
       "-ar", "48000", "-c:a", "aac", "-b:a", "256k", out)
    st = fx.probe(out)["streams"][0]
    a, b = ebur(src), ebur(out)
    return [check("-14 LUFS ±1.5", abs(b["I"] + 14) <= 1.5, b["I"], -14),
            check("true peak under -1 dBTP (+0.5 AAC)", b["TP"] <= -0.5, b["TP"], "<= -0.5"),
            check("AAC 48 kHz", st["codec_name"] == "aac" and st["sample_rate"] == "48000", [st["codec_name"], st["sample_rate"]], ["aac", "48000"]),
            check("negative control: 44.1 kHz input off target", abs(a["I"] + 14) > 1.5, a["I"], "!= -14")], [out]


@card("BEAT-106")
def hf_normalize_audio(task, wd):
    """npx hyperframes normalize-audio --target ID --lufs -16 --write: the measured gain is written to data-volume."""
    d = Path(wd) / "proj"
    d.mkdir()
    x = tone(440, 3.0, 0.1)
    save(d, "clip.wav", np.stack([x, x], 1))
    hf_project(d, '<audio id="clip" class="clip" src="clip.wav" data-start="0" data-duration="3" data-track-index="0" data-volume="1"></audio>', dur=3)
    before = (d / "index.html").read_text()
    res = json.loads(hf("normalize-audio", ".", "--target=clip", "--lufs=-16", "--write", "--json", cwd=d))
    html = (d / "index.html").read_text()
    vol = float(re.search(r'data-volume="([\d.]+)"', html).group(1))
    out = Path(wd) / "applied.wav"
    ff("-i", d / "clip.wav", "-af", "volume=%f" % vol, out)
    m, m0 = ebur(out), ebur(d / "clip.wav")
    return [check("data-volume written into index.html", html != before and abs(vol - 1) > 0.5, vol, "!= 1"),
            check("clip at the written volume measures -16 LUFS", abs(m["I"] + 16) <= 0.6, m["I"], -16),
            check("CLI projected -16", abs(res["projectedLufs"] + 16) <= 0.5, res["projectedLufs"], -16),
            check("negative control: source clip not at -16", abs(m0["I"] + 16) > 3, m0["I"], "!= -16")], [out, d / "index.html"]


@card("BEAT-152")
def loudness_targets_bed(task, wd):
    """-14 LUFS integrated, -1 dBTP, music bed -18 dB under speech: measured, not guessed."""
    v = speechlike(4.0, [(0.2, 3.8)])
    m = music_bed(4.0)
    vp, mp = save(wd, "voice.wav", v), save(wd, "bed.wav", m)
    lv, lm = ebur(vp)["I"], ebur(mp)["I"]
    bed = m * 10 ** ((lv - 18 - lm) / 20)
    mix = save(wd, "mix_raw.wav", v + bed)
    bp = save(wd, "bed_set.wav", bed)
    out = Path(wd) / "mix_master.wav"
    loudnorm2(mix, out, -14, -1, 11)
    gap = lv - ebur(bp)["I"]
    r = ebur(out)
    return [check("bed sits 18 dB under speech (measured)", abs(gap - 18) <= 0.5, gap, 18),
            check("master -14 LUFS", abs(r["I"] + 14) <= 0.5, r["I"], -14),
            check("true peak <= -1 dBTP (+0.3)", r["TP"] <= -0.7, r["TP"], "<= -1"),
            check("negative control: unbalanced bed is not -18 under", abs((lv - lm) - 18) > 3, lv - lm, "!= 18")], [out, bp]


@card("BEAT-231")
def music_premaster(task, wd):
    """Cue mastered to -16 LUFS / peaks under -1, resampled to 48 kHz; SFX on top; final pass -14."""
    src, _ = song_fixture(wd, 4.0, -30, sr=44100)
    cue = Path(wd) / "cue_premaster.wav"
    loudnorm2(src, cue, -16, -1, 11, sr=48000)
    x, sr = load_any(cue)
    x[int(2 * sr):int(2 * sr) + 2400] += 0.2 * np.sin(2 * np.pi * 2000 * tt(0.05))
    sfx = save(wd, "cue_sfx.wav", x, sr)
    fin = Path(wd) / "final.wav"
    loudnorm2(sfx, fin, -14, -1, 11)
    c, f = ebur(cue), ebur(fin)
    rate = int(fx.probe(cue)["streams"][0]["sample_rate"])
    return [check("cue -16 LUFS", abs(c["I"] + 16) <= 0.5, c["I"], -16),
            check("cue peaks under -1 dBTP (+0.3)", c["TP"] <= -0.7, c["TP"], "<= -1"),
            check("cue at 48 kHz", rate == 48000, rate, 48000),
            check("final -14", abs(f["I"] + 14) <= 0.5, f["I"], -14),
            check("negative control: 44.1 kHz source not -16", abs(ebur(src)["I"] + 16) > 3, ebur(src)["I"], "!= -16")], [cue, fin]


@card("BEAT-246")
def mastering_iterate(task, wd):
    """28 Hz high-pass, -1.5 dB shelf at 10 kHz, iterate normalise → limit (≤4 rounds) until within 0.15 LU, ceiling -1.5 dBFS."""
    t = tt(4.0)
    x = music_bed(4.0) + 0.6 * drum_loop(120, 4.0)[0] + 0.2 * np.sin(2 * np.pi * 12 * t)
    x *= 10 ** ((-24 - dbfs(x)) / 20)
    src = save(wd, "in.wav", x)
    cur = Path(wd) / "stage0.wav"
    ff("-i", src, "-af", "highpass=f=28,treble=g=-1.5:f=10000", "-c:a", "pcm_f32le", cur)
    target, rounds, I = -14.0, 0, None
    for k in range(4):
        I = ebur(cur)["I"]
        if abs(I - target) <= 0.15:
            break
        nxt = Path(wd) / ("stage%d.wav" % (k + 1))
        ff("-i", cur, "-af", "volume=%.3fdB,alimiter=limit=%.5f:level=false:attack=2:release=50" % (target - I, 10 ** (-1.5 / 20)), "-c:a", "pcm_f32le", nxt)
        cur, rounds = nxt, k + 1
    I = ebur(cur)["I"]
    y, _ = load_any(cur)
    out = Path(wd) / "master.wav"
    shutil.copy(cur, out)
    return [check("within 0.15 LU of -14 after <=4 rounds", abs(I - target) <= 0.15, I, target),
            check("sample ceiling -1.5 dBFS", peak_db(y) <= -1.45, peak_db(y), "<= -1.5"),
            check("12 Hz rumble cut >= 12 dB relative to 200-800 Hz by the 28 Hz high-pass",
                  (band_db(x, SR, 8, 16) - band_db(x, SR, 200, 800)) - (band_db(y, SR, 8, 16) - band_db(y, SR, 200, 800)) >= 12,
                  (band_db(x, SR, 8, 16) - band_db(x, SR, 200, 800)) - (band_db(y, SR, 8, 16) - band_db(y, SR, 200, 800)), ">= 12"),
            check("negative control: input not within 0.15 LU", abs(ebur(src)["I"] - target) > 0.15, ebur(src)["I"], target)], [out]


@card("BEAT-248")
def publish_loudnorm(task, wd):
    """Two-pass loudnorm for publishing: socials -14 LUFS, podcast -16 LUFS, TP -1.5, LRA 11."""
    c1, o1 = _loud(wd, -14, -1.5, 11, name="social")
    c2, o2 = _loud(wd, -16, -1.5, 11, name="podcast")
    return c1 + c2, o1 + o2


@card("BEAT-261")
def platform_targets(task, wd):
    """Platform -14, podcast -16 stereo / -19 mono, TP -1, adjacent scenes differ <= 6 dB (measured with loudnorm/ebur128)."""
    checks, outs = [], []
    for nm, I, mono in (("video", -14, False), ("podcast", -16, False), ("podcast_mono", -19, True)):
        src, _ = song_fixture(wd, 4.0, -32, name=nm + "_in.wav")
        o = Path(wd) / (nm + ".wav")
        loudnorm2(src, o, I, -1, 11)
        if mono:
            m2 = Path(wd) / (nm + "_1ch.wav")
            ff("-i", o, "-ac", "1", m2)
            o = m2
        r = ebur(o)
        checks.append(check("%s on %s LUFS" % (nm, I), abs(r["I"] - I) <= 0.6, r["I"], I))
        outs.append(o)
    s1, _ = song_fixture(wd, 3.0, -20, name="scene1.wav")
    s2, _ = song_fixture(wd, 3.0, -30, name="scene2.wav")
    n1, n2 = Path(wd) / "scene1_n.wav", Path(wd) / "scene2_n.wav"
    loudnorm2(s1, n1, -14, -1, 11)
    loudnorm2(s2, n2, -14, -1, 11)
    d_in, d_out = abs(ebur(s1)["I"] - ebur(s2)["I"]), abs(ebur(n1)["I"] - ebur(n2)["I"])
    checks += [check("adjacent scenes differ <= 6 dB after", d_out <= 6, d_out, "<= 6"),
               check("negative control: raw adjacent scenes differ > 6 dB", d_in > 6, d_in, "> 6")]
    return checks, outs + [n1, n2]


@card("BEAT-263")
def mastering_chain_report(task, wd):
    """Measure LUFS/TP/LRA/clipping → clean hum → corrective EQ → compression → limiter → loudness; re-measure; report."""
    t = tt(4.0)
    x = music_bed(4.0) + 0.5 * clicks(120, 4.0, f=2000)[0]
    x = x * 10 ** ((-26 - dbfs(x)) / 20) + 0.03 * np.sin(2 * np.pi * 50 * t)
    src = save(wd, "in.wav", x)
    pre = Path(wd) / "pre.wav"
    ff("-i", src, "-af", "bandreject=f=50:width_type=h:w=4,bandreject=f=50:width_type=h:w=4,bandreject=f=50:width_type=h:w=4,highpass=f=30,"
       "equalizer=f=300:t=q:w=1:g=-2,acompressor=threshold=-20dB:ratio=2:attack=10:release=100,alimiter=limit=0.89:level=false", pre)
    out = Path(wd) / "master.wav"
    loudnorm2(pre, out, -14, -1, 11)
    b, a = ebur(out), ebur(src)
    y, _ = load_any(out)
    hum_in = band_db(x, SR, 45, 55) - band_db(x, SR, 200, 500)
    hum_out = band_db(y, SR, 45, 55) - band_db(y, SR, 200, 500)
    rep = {"before": a, "after": b, "hum_rel_db": [hum_in, hum_out], "clipped_samples": int(np.sum(np.abs(y) >= 0.999))}
    jdump(Path(wd) / "analysis.json", rep)
    (Path(wd) / "report.md").write_text("| | before | after |\n|---|---|---|\n| LUFS | %.1f | %.1f |\n| TP | %.1f | %.1f |\n" % (a["I"], b["I"], a["TP"], b["TP"]))
    return [check("hum at 50 Hz reduced by >= 15 dB relative to music", hum_in - hum_out >= 15, hum_in - hum_out, ">= 15"),
            check("-14 LUFS after", abs(b["I"] + 14) <= 0.5, b["I"], -14),
            check("TP <= -1 (+0.3)", b["TP"] <= -0.7, b["TP"], "<= -1"),
            check("no clipped samples", rep["clipped_samples"] == 0, rep["clipped_samples"], 0),
            check("negative control: input off target with hum", abs(a["I"] + 14) > 3 and hum_in > -15, [a["I"], hum_in], "off target, hum")], [out, Path(wd) / "analysis.json"]


@card("BEAT-145")
def self_master_numpy(task, wd):
    """Code-only master: synthetic exp-decay noise IR (2.4 s, tau .55, LP 5 kHz) fftconvolved wet .28, HP 35 Hz,
    +0.9×HP(2500) shelf, RMS to -15 dBFS, tanh(1.1x)·.89, -2.05 dB trim, 4× oversampled true-peak ≤ -1.2 dBTP, 0.6 s fade."""
    from scipy.signal import butter, fftconvolve, resample_poly, sosfilt
    sr = 48000
    x, _ = drum_loop(112, 3.0, sr)
    x = np.concatenate([x * 0.5 + music_bed(3.0, sr) * 0.5, np.zeros(int(2.0 * sr))])
    save(wd, "dry.wav", x, sr)
    rng = np.random.default_rng(2120)
    it = tt(2.4, sr)
    ir = rng.standard_normal(len(it)) * np.exp(-it / 0.55)
    ir = sosfilt(butter(2, 5000, "low", fs=sr, output="sos"), ir)
    ir /= np.sqrt(np.sum(ir ** 2))
    y = x + 0.28 * fftconvolve(x, ir)[: len(x)]
    y = sosfilt(butter(2, 35, "high", fs=sr, output="sos"), y)
    y = y + 0.9 * sosfilt(butter(2, 2500, "high", fs=sr, output="sos"), y)
    y *= 10 ** ((-15 - dbfs(y)) / 20)
    pre_rms = dbfs(y)
    y = np.tanh(1.1 * y) * 0.89 * 10 ** (-2.05 / 20)
    nf = int(0.6 * sr)
    y[-nf:] *= np.linspace(1, 0, nf)
    tp = peak_db(resample_poly(y, 4, 1))
    out = save(wd, "master.wav", y, sr)
    tail_wet = seg_db(y, sr, 3.15, 3.6)
    tail_dry = seg_db(x, sr, 3.15, 3.6)
    hf_gain = (band_db(y, sr, 3000, 8000) - band_db(y, sr, 200, 800)) - (band_db(x, sr, 3000, 8000) - band_db(x, sr, 200, 800))
    return [check("RMS normalised to -15 dBFS before the limiter", abs(pre_rms + 15) < 0.05, pre_rms, -15),
            check("4x oversampled true peak <= -1.2 dBTP", tp <= -1.2, tp, "<= -1.2"),
            check("reverb tail present after the dry signal ends", tail_wet > -60 and tail_wet - tail_dry > 30, [tail_wet, tail_dry], "wet tail >> dry"),
            check("presence shelf lifts 3-8 kHz relative to 200-800 Hz", hf_gain > 1.0, hf_gain, "> 1 dB"),
            check("0.6 s end fade reaches silence", abs(y[-1]) < 1e-3, float(abs(y[-1])), 0),
            check("negative control: dry input has no tail", tail_dry < -80, tail_dry, "< -80")], [out]


@card("BEAT-100")
def speech_enhance_chain(task, wd):
    """AUD.chain: HPF 90 Hz (120 if SNR < 14 dB) → peaking 3.2 kHz +2 dB → gain to speech RMS -20 dBFS (clamp -12..+26)
    → compressor thr -24+(1-k)·12, ratio 2+4k, attack 4 ms, release 180 ms → limiter -2 dB → make-up k·1.5 dB."""
    k = 0.5
    t = tt(4.0)
    sp = speechlike(4.0, [(0.3, 1.6), (2.0, 3.6)], amp=0.05)
    rum = 0.012 * np.sin(2 * np.pi * 45 * t)
    x = sp + rum
    src = save(wd, "raw.wav", x)
    voiced = np.abs(sp) > 0
    snr = dbfs(sp[voiced]) - dbfs(rum)
    hpf = 120 if snr < 14 else 90
    speech_rms = dbfs(x[voiced])
    filt = Path(wd) / "filtered.wav"
    ff("-i", src, "-af", "highpass=f=%d:t=q:w=0.7,equalizer=f=3200:t=q:w=0.8:g=2" % hpf, "-c:a", "pcm_f32le", filt)
    gain = float(np.clip(-20 - dbfs(load_any(filt)[0][voiced]), -12, 26))
    thr, ratio = -24 + (1 - k) * 12, 2 + 4 * k
    out = Path(wd) / "enhanced.wav"
    ff("-i", src, "-af", "highpass=f=%d:t=q:w=0.7,equalizer=f=3200:t=q:w=0.8:g=2,volume=%.2fdB,"
       "acompressor=threshold=%.1fdB:ratio=%.1f:knee=8:attack=4:release=180,alimiter=limit=%.4f:level=false:attack=1:release=80,volume=%.2fdB"
       % (hpf, gain, thr, ratio, 10 ** (-2 / 20), k * 1.5), out)
    stage = Path(wd) / "gain_stage.wav"
    ff("-i", src, "-af", "highpass=f=%d:t=q:w=0.7,equalizer=f=3200:t=q:w=0.8:g=2,volume=%.2fdB" % (hpf, gain), stage)
    lvl = dbfs(load_any(stage)[0][voiced])
    y, _ = load_any(out)
    rum_rel_in = band_db(x, SR, 40, 50) - band_db(x, SR, 130, 2000)
    rum_rel_out = band_db(y, SR, 40, 50) - band_db(y, SR, 130, 2000)
    return [check("SNR < 14 dB selects the 120 Hz high-pass", hpf == 120, [round(snr, 1), hpf], 120),
            check("gain stage brings speech RMS to -20 dBFS (±1)", abs(lvl + 20) <= 1, lvl, -20),
            check("rumble cut >= 12 dB relative to speech", rum_rel_in - rum_rel_out >= 12, rum_rel_in - rum_rel_out, ">= 12"),
            check("limiter ceiling -2 dB (+make-up 0.75 dB)", peak_db(y) <= -2 + k * 1.5 + 0.1, peak_db(y), "<= -1.25"),
            check("negative control: raw speech far from -20 dBFS", abs(speech_rms + 20) > 6, speech_rms, "!= -20")], [out]


@card("BEAT-101")
def downward_expander(task, wd):
    """AUD.gate: envelope attack 4 / release 40 ms; close = min(quiet25%+1.5, speech-12), open = min(close+5, speech-7);
    gain eases to a -10 dB floor (attack 5 ms, release 160 ms)."""
    sr = SR
    rng = np.random.default_rng(4)
    spans = [(0.3, 1.0), (2.0, 2.7), (3.2, 3.8)]
    x = speechlike(4.0, spans, amp=0.25) + 10 ** (-50 / 20) * rng.standard_normal(int(4 * sr))
    src = save(wd, "in.wav", x)
    a_att, a_rel = math.exp(-1 / (0.004 * sr)), math.exp(-1 / (0.040 * sr))
    env = np.empty_like(x)
    e = 0.0
    ax = np.abs(x)
    for i in range(len(x)):
        c = a_att if ax[i] > e else a_rel
        e = c * e + (1 - c) * ax[i]
        env[i] = e
    edb = 20 * np.log10(env + 1e-9)
    quiet, speech = np.percentile(edb, 25), np.percentile(edb, 95)
    close = min(quiet + 1.5, speech - 12)
    opn = min(close + 5, speech - 7)
    g_att, g_rel = math.exp(-1 / (0.005 * sr)), math.exp(-1 / (0.160 * sr))
    g = np.empty_like(x)
    state, gv = True, 1.0
    floor = 10 ** (-10 / 20)
    for i in range(len(x)):
        if state and edb[i] < close:
            state = False
        elif not state and edb[i] > opn:
            state = True
        tgt = 1.0 if state else floor
        c = g_att if tgt > gv else g_rel
        gv = c * gv + (1 - c) * tgt
        g[i] = gv
    y = x * g
    out = save(wd, "gated.wav", y)
    gap_in, gap_out = seg_db(x, sr, 1.55, 1.95), seg_db(y, sr, 1.55, 1.95)
    sp_in, sp_out = seg_db(x, sr, 0.45, 0.95), seg_db(y, sr, 0.45, 0.95)
    return [check("room noise between words pushed down ~10 dB", -11.5 <= gap_out - gap_in <= -8.5, gap_out - gap_in, -10),
            check("speech level kept within 1 dB", abs(sp_out - sp_in) <= 1.0, sp_out - sp_in, 0),
            check("thresholds ordered close < open < speech", close < opn < speech, [close, opn, speech], "close<open<speech"),
            check("negative control: input gap still at the room level", abs(seg_db(x, sr, 1.55, 1.95) - seg_db(x, sr, 2.85, 3.1)) < 1.5,
                  seg_db(x, sr, 1.55, 1.95), "room level")], [out]


@card("BEAT-256")
def mix_chain_numbers(task, wd):
    """HPF (voice 80-100) → mud cut 200-400 → compression 3:1 10/80 ms → de-ess 5-8 kHz → delay 60000/BPM ms → limiter → loudness."""
    bpm = 120
    x = np.zeros(int(3 * SR))
    x[int(0.2 * SR):int(0.2 * SR) + int(0.4 * SR)] = speechlike(0.4, [(0, 0.4)], amp=0.4)
    src = save(wd, "voice.wav", x)
    dms = 60000 / bpm
    pre = Path(wd) / "chain.wav"
    ff("-i", src, "-af", "highpass=f=90,equalizer=f=300:t=q:w=1:g=-3,acompressor=threshold=-18dB:ratio=3:attack=10:release=80,"
       "deesser=i=0.4:f=0.5,aecho=0.8:0.5:%d:0.35,alimiter=limit=0.89:level=false" % dms, pre)
    out = Path(wd) / "voice_master.wav"
    loudnorm2(pre, out, -16, -1, 11)
    y, _ = load_any(out)
    on = onsets(y, SR, rel=0.12, gap=0.3)
    echo = [t for t in on if 0.6 < t < 0.85]
    r = ebur(out)
    return [check("echo arrives 60000/BPM = 500 ms after the phrase (±15 ms)", bool(echo) and abs(echo[0] - 0.2 - 0.5) <= 0.015, on, 0.7),
            check("loudness -16 LUFS", abs(r["I"] + 16) <= 0.6, r["I"], -16),
            check("negative control: dry input has no echo at 500 ms", seg_db(x, SR, 0.7, 1.0) < -80, seg_db(x, SR, 0.7, 1.0), "< -80")], [out]


# ───────────────────────── ducking, mixing, HyperFrames audio graph ─────────────────────────
BED_F = (233.0, 311.0, 466.0)        # bed partials that a 170 Hz voice's harmonics never touch


def bed(secs, amp=0.3, sr=SR, freqs=BED_F):
    t = tt(secs, sr)
    return amp * sum(np.sin(2 * np.pi * f * t) for f in freqs) / len(freqs)


def narrow_db(x, sr, f, a, b, bw=4.0):
    """Level of one partial inside [a, b] s: power within ±bw Hz of f (Hann window), so the bed can be read under a voice."""
    s = x[int(a * sr):int(b * sr)]
    w = np.hanning(len(s))
    X = np.abs(np.fft.rfft(s * w)) ** 2
    fr = np.fft.rfftfreq(len(s), 1 / sr)
    return 10 * math.log10(float(X[(fr > f - bw) & (fr < f + bw)].sum()) / (np.sum(w ** 2) * len(s)) + 1e-20)


def bed_drop(x, sr, span, pre=(0.2, 0.9), margin=0.35, f=BED_F[0]):
    a, b = span
    return narrow_db(x, sr, f, a + margin, b - 0.1) - narrow_db(x, sr, f, *pre)


def flat(x, a, b, c=0.2, e=0.9, sr=SR):
    """Partial level in [a,b] minus in [c,e] on an unprocessed signal (the negative control value)."""
    return narrow_db(x, sr, BED_F[0], a, b) - narrow_db(x, sr, BED_F[0], c, e)


def voice_bed(wd, secs=4.0, span=(1.0, 2.6), amp_v=0.35):
    v = speechlike(secs, [span], f0=170, amp=amp_v)
    m = bed(secs)
    return save(wd, "voice.wav", v), save(wd, "music.wav", m), v, m


def _sc_card(wd, span=(1.0, 2.6), thr=0.02, ratio=12, attack=20, release=300, makeup=1, lo=10, hi=40, name="ducked"):
    vp, mp, v, m = voice_bed(wd, span=span)
    d = sidechain(mp, vp, Path(wd) / (name + ".wav"), thr, ratio, attack, release, makeup)
    mix = Path(wd) / (name + "_mix.wav")
    ff("-i", d, "-i", vp, "-filter_complex", "[0:a][1:a]amix=inputs=2:normalize=0[m]", "-map", "[m]", mix)
    y, sr = load_any(d)
    drop = bed_drop(y, sr, span)
    out_ch = narrow_db(y, sr, BED_F[0], 3.2, 3.9) - narrow_db(y, sr, BED_F[0], 0.2, 0.9)
    neg = bed_drop(m, SR, span)
    return drop, out_ch, neg, [d, mix]


def _duck_checks(drop, out_ch, neg, lo, hi):
    return [check("music drops %s..%s dB under the voice" % (lo, hi), -hi <= drop <= -lo, drop, "-%s..-%s" % (lo, hi)),
            check("music back to level after the voice (±1.5 dB)", abs(out_ch) <= 1.5, out_ch, 0),
            check("negative control: the unprocessed bed does not dip", abs(neg) < 0.5, neg, 0)]


@card("BEAT-143")
def duck_spec_vs_static(task, wd):
    """Real ducking [music][voice]sidechaincompress=threshold=0.05:ratio=8:attack=20:release=300 then amix, against the
    smart_montage static 0.35 gain (-9.1 dB everywhere, no sidechain)."""
    drop, out_ch, neg, outs = _sc_card(wd, thr=0.05, ratio=8, attack=20, release=300)
    st = Path(wd) / "static.wav"
    ff("-i", Path(wd) / "music.wav", "-af", "volume=0.35", st)
    s, sr = load_any(st)
    m, _ = load_any(Path(wd) / "music.wav")
    g_in = narrow_db(s, sr, BED_F[0], 1.35, 2.5) - narrow_db(m, sr, BED_F[0], 1.35, 2.5)
    g_out = narrow_db(s, sr, BED_F[0], 0.2, 0.9) - narrow_db(m, sr, BED_F[0], 0.2, 0.9)
    return _duck_checks(drop, out_ch, neg, 6, 30) + [
        check("static 0.35 = -9.1 dB in and out of speech", abs(g_in + 9.12) < 0.3 and abs(g_out + 9.12) < 0.3, [g_in, g_out], -9.12),
        check("static gain does not follow the voice (contrast with sidechain)", abs(g_in - g_out) < 0.3, g_in - g_out, 0)], outs + [st]


@card("BEAT-230")
def speech_first_ducking(task, wd):
    """sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300 keyed by the voice, plus an EQ notch 2-4 kHz on the music."""
    vp, mp, v, m = voice_bed(wd)
    t = tt(4.0)
    m2 = m + 0.1 * np.sin(2 * np.pi * 3000 * t)
    mp = save(wd, "music.wav", m2)
    eq = Path(wd) / "music_eq.wav"
    ff("-i", mp, "-af", "equalizer=f=3000:t=h:w=2000:g=-8", eq)
    d = sidechain(eq, vp, Path(wd) / "ducked.wav", 0.03, 8, 20, 300)
    y, sr = load_any(d)
    notch = narrow_db(y, sr, 3000, 0.2, 0.9) - narrow_db(m2, sr, 3000, 0.2, 0.9)
    return _duck_checks(bed_drop(y, sr, (1.0, 2.6)), narrow_db(y, sr, BED_F[0], 3.2, 3.9) - narrow_db(y, sr, BED_F[0], 0.2, 0.9),
                        bed_drop(m2, SR, (1.0, 2.6)), 6, 30) + [
        check("2-4 kHz carved out of the music (>= 6 dB at 3 kHz)", notch <= -6, notch, "<= -6")], [d]


@card("BEAT-244")
def ducking_music_under_voice(task, wd):
    """ffmpeg sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300 with the voice as key."""
    drop, out_ch, neg, outs = _sc_card(wd, thr=0.03, ratio=8, attack=20, release=300)
    return _duck_checks(drop, out_ch, neg, 6, 30), outs


@card("BEAT-262")
def sidechain_400ms(task, wd):
    """[1:a][0:a]sidechaincompress=threshold=0.05:ratio=8:attack=20:release=400[m];amix normalize=0."""
    drop, out_ch, neg, outs = _sc_card(wd, thr=0.05, ratio=8, attack=20, release=400)
    y, sr = load_any(outs[0])
    just_after = narrow_db(y, sr, BED_F[0], 2.62, 2.8) - narrow_db(y, sr, BED_F[0], 0.2, 0.9)
    return _duck_checks(drop, out_ch, neg, 6, 30) + [
        check("400 ms release: still ducked right after the voice", just_after < -2, just_after, "< -2")], outs


@card("BEAT-78")
def vo_sidechain_montage(task, wd):
    """montage: sidechaincompress threshold=0.02 ratio=12 attack=20 release=300 (~-18 dB under speech); reel: ratio 10, bed volume 0.45."""
    drop, out_ch, neg, outs = _sc_card(wd, thr=0.02, ratio=12, attack=20, release=300)
    vp, mp = Path(wd) / "voice.wav", Path(wd) / "music.wav"
    reel = Path(wd) / "reel.wav"
    ff("-i", mp, "-i", vp, "-filter_complex", "[0:a]volume=0.45[b];[b][1:a]sidechaincompress=threshold=0.02:ratio=10:attack=20:release=300[d]",
       "-map", "[d]", reel)
    y, sr = load_any(reel)
    pre = narrow_db(y, sr, BED_F[0], 0.2, 0.9) - narrow_db(load_any(mp)[0], sr, BED_F[0], 0.2, 0.9)
    return _duck_checks(drop, out_ch, neg, 12, 26) + [
        check("reel bed sits at 0.45 (-6.9 dB) before the voice", abs(pre + 6.94) < 0.4, pre, -6.94),
        check("reel bed ducks too (ratio 10)", bed_drop(y, sr, (1.0, 2.6)) < -10, bed_drop(y, sr, (1.0, 2.6)), "< -10")], outs + [reel]


@card("BEAT-84")
def sidechain_presets(task, wd):
    """montage 0.02/12/20/300 makeup 1 (≈-18 dB), voice_cut release 320, reel ratio 10 bed 0.45, mux 0.03/6/380."""
    vp, mp, v, m = voice_bed(wd)
    presets = {"montage": (0.02, 12, 20, 300, 1.0), "voice_cut": (0.02, 12, 20, 320, 1.0), "reel": (0.02, 10, 20, 300, 0.45),
               "mux": (0.03, 6, 20, 380, 1.0)}
    res, outs = {}, []
    for k, (thr, ratio, att, rel, vol) in presets.items():
        o = Path(wd) / ("%s.wav" % k)
        ff("-i", mp, "-i", vp, "-filter_complex", "[0:a]volume=%s[b];[b][1:a]sidechaincompress=threshold=%s:ratio=%s:attack=%s:release=%s:makeup=1[d]"
           % (vol, thr, ratio, att, rel), "-map", "[d]", o)
        y, sr = load_any(o)
        res[k] = bed_drop(y, sr, (1.0, 2.6))
        outs.append(o)
    jdump(Path(wd) / "presets.json", res)
    return [check("every preset ducks >= 8 dB under speech", all(d < -8 for d in res.values()), res, "< -8"),
            check("montage (ratio 12) ducks deeper than mux (ratio 6)", res["montage"] < res["mux"] - 2, [res["montage"], res["mux"]], "montage < mux"),
            check("montage ≈ -18 dB (±5)", abs(res["montage"] + 18) <= 5, res["montage"], -18),
            check("negative control: bed alone does not dip", abs(bed_drop(m, SR, (1.0, 2.6))) < 0.5, bed_drop(m, SR, (1.0, 2.6)), 0)], outs


@card("BEAT-79")
def static_bed(task, wd):
    """[1:a]volume=-18dB[m];[0:a][m]amix=inputs=2:duration=first:normalize=0, music fade_out 1.0 s."""
    vp, mp, v, m = voice_bed(wd)
    bedp = Path(wd) / "bed_-18.wav"
    ff("-i", mp, "-af", "volume=-18dB,afade=t=out:st=3.0:d=1.0", bedp)
    mix = Path(wd) / "mix.wav"
    ff("-i", vp, "-i", mp, "-filter_complex", "[1:a]volume=-18dB,afade=t=out:st=3.0:d=1.0[m];[0:a][m]amix=inputs=2:duration=first:normalize=0[o]", "-map", "[o]", mix)
    y, sr = load_any(mix)
    g = narrow_db(y, sr, BED_F[0], 0.2, 0.9) - narrow_db(m, sr, BED_F[0], 0.2, 0.9)
    g_sp = narrow_db(y, sr, BED_F[0], 1.3, 2.5) - narrow_db(m, sr, BED_F[0], 1.3, 2.5)
    tail = narrow_db(y, sr, BED_F[0], 3.6, 3.95) - narrow_db(y, sr, BED_F[0], 2.7, 2.95)
    dur = float(fx.probe(mix)["format"]["duration"])
    return [check("bed at -18 dB before speech", abs(g + 18) < 0.4, g, -18),
            check("bed at -18 dB during speech too (static)", abs(g_sp + 18) < 0.6, g_sp, -18),
            check("1 s fade-out at the end", tail < -8, tail, "< -8"),
            check("duration=first keeps the voice length", abs(dur - 4.0) < 0.05, dur, 4.0),
            check("negative control: the source bed is not at -18", abs(narrow_db(load_any(mp)[0], sr, BED_F[0], 0.2, 0.9) - narrow_db(m, sr, BED_F[0], 0.2, 0.9) + 18) > 10, narrow_db(load_any(mp)[0], sr, BED_F[0], 0.2, 0.9) - narrow_db(m, sr, BED_F[0], 0.2, 0.9), "not -18")], [mix, bedp]


@card("BEAT-94")
def duck_032_edges(task, wd):
    """level = vol·(duck && speaking ? 0.32 : 1)·edge, edge = min((t-at)/0.4, (end-t)/0.6); offline gain every 0.1 s."""
    secs, at, end, vol = 4.0, 0.0, 4.0, 1.0
    spans = [(1.2, 2.4)]
    m = bed(secs)
    t = tt(secs)
    kt = np.arange(0, secs + 1e-9, 0.1)
    speaking = np.array([any(a <= k < b for a, b in spans) for k in kt])
    edge = np.clip(np.minimum((kt - at) / 0.4, (end - kt) / 0.6), 0, 1)
    lvl = vol * np.where(speaking, 0.32, 1.0) * edge
    g = np.interp(t, kt, lvl)
    y = m * g
    out = save(wd, "bed_ducked.wav", y)
    jdump(Path(wd) / "automation.json", {"t": kt.round(2).tolist(), "gain": lvl.round(4).tolist()})
    d = narrow_db(y, SR, BED_F[0], 1.4, 2.3) - narrow_db(y, SR, BED_F[0], 0.6, 1.1)
    fade = rms(y[int(0.18 * SR):int(0.22 * SR)]) / rms(y[int(0.7 * SR):int(0.74 * SR)])
    return [check("x0.32 under speech = -9.9 dB", abs(d + 9.9) < 0.5, d, -9.9),
            check("0.4 s fade-in: half level at 0.2 s", abs(fade - 0.5) < 0.06, fade, 0.5),
            check("0.6 s fade-out reaches 0 at the end", abs(y[-1]) < 1e-3, float(abs(y[-1])), 0),
            check("negative control: undocked bed has no dip", abs(flat(m, 1.4, 2.3, 0.6, 1.1)) < 0.3, flat(m, 1.4, 2.3, 0.6, 1.1), 0)], [out]


@card("BEAT-218")
def section_music_direction(task, wd):
    """Section table (intro bright, core under the voice, reveal lift, outro resolve) → ffmpeg volume automation; voice untouched."""
    table = [{"section": "intro", "from": 0.0, "to": 1.0, "target": "bright/curious", "db": 0.0},
             {"section": "core", "from": 1.0, "to": 2.5, "target": "focused under voice", "db": -12.0},
             {"section": "reveal", "from": 2.5, "to": 3.2, "target": "lift/swell", "db": 2.0},
             {"section": "outro", "from": 3.2, "to": 4.0, "target": "resolve", "db": -4.0}]
    vp, mp, v, m = voice_bed(wd, span=(1.05, 2.45))
    expr = "+".join("between(t,%s,%s)*%s" % (r["from"], r["to"] - 1e-3, 10 ** (r["db"] / 20)) for r in table)
    shaped = Path(wd) / "music_directed.wav"
    ff("-i", mp, "-af", "volume='%s':eval=frame" % expr, shaped)
    mix = Path(wd) / "mix.wav"
    ff("-i", vp, "-i", shaped, "-filter_complex", "[0:a][1:a]amix=inputs=2:normalize=0[o]", "-map", "[o]", mix)
    y, sr = load_any(shaped)
    got = {r["section"]: narrow_db(y, sr, BED_F[0], r["from"] + 0.1, r["to"] - 0.1) - narrow_db(m, sr, BED_F[0], r["from"] + 0.1, r["to"] - 0.1) for r in table}
    jdump(Path(wd) / "music_direction.json", {"table": table, "measured_db": got})
    voice_after, _ = load_any(vp)
    return [check("each section sits at its planned level (±0.5 dB)", all(abs(got[r["section"]] - r["db"]) <= 0.5 for r in table), got, {r["section"]: r["db"] for r in table}),
            check("voice file untouched", np.array_equal(voice_after, load_any(vp)[0]) and fx.probe(vp)["streams"][0]["codec_name"] == "pcm_s16le", True, True),
            check("negative control: raw bed is flat across sections", abs(flat(m, 1.1, 2.4, 0.1, 0.9)) < 0.3, flat(m, 1.1, 2.4, 0.1, 0.9), 0)], [mix, shaped]


@card("BEAT-289")
def typing_duck(task, wd):
    """Score ducks -6 dB under typing sounds (volume automation keyed to the typing spans)."""
    secs = 4.0
    m = bed(secs)
    typ = np.zeros(int(secs * SR))
    rng = np.random.default_rng(5)
    keys = [1.2 + 0.09 * k for k in range(12)]
    for k in keys:
        i = int(k * SR)
        n = int(0.02 * SR)
        typ[i:i + n] += 0.4 * rng.standard_normal(n) * np.exp(-tt(0.02) / 0.004)
    on = onsets(typ, SR, 0.2, 0.05)
    spans, a = [], None
    for k, t0 in enumerate(on):
        a = t0 if a is None else a
        if k == len(on) - 1 or on[k + 1] - t0 > 0.3:
            spans.append((a - 0.05, t0 + 0.15))
            a = None
    t = tt(secs)
    g = np.ones_like(t)
    for a, b in spans:
        g[(t >= a) & (t < b)] = 10 ** (-6 / 20)
    g = np.convolve(g, np.ones(480) / 480, mode="same")
    y = m * g
    out = save(wd, "score_ducked.wav", y + typ)
    sb = save(wd, "score_only.wav", y)
    a, b = spans[0]
    d = narrow_db(y, SR, BED_F[0], a + 0.05, b - 0.05) - narrow_db(y, SR, BED_F[0], 0.2, 0.9)
    return [check("one typing span found from the sound", len(spans) == 1, spans, "1 span"),
            check("score -6 dB under typing", abs(d + 6) < 0.5, d, -6),
            check("negative control: raw score is flat", abs(flat(m, a + 0.05, b - 0.05)) < 0.3, flat(m, a + 0.05, b - 0.05), 0)], [out, sb]


@card("BEAT-35")
def kick_pump(task, wd):
    """Pads/bass dip on every kick (duck 0.35-0.5) and recover within half a beat."""
    bpm, secs, duck = 120, 4.0, 0.4
    beat = 60 / bpm
    pad = bed(secs)
    t = tt(secs)
    since = np.mod(t, beat)
    env = np.clip(1 - since / (beat / 2), 0, 1) ** 2
    g = 1 - duck * env
    y = pad * g
    k, _ = drum_loop(bpm, secs)
    out = save(wd, "pumped.wav", y + 0.5 * k)
    so = save(wd, "pad_pumped.wav", y)
    e = envelope(y, SR, 10)
    at_kick = np.mean([e[int((b * beat + 0.012) * SR)] for b in range(1, 7)])
    half = np.mean([e[int((b * beat + beat / 2 + 0.02) * SR)] for b in range(1, 7)])
    dip = 20 * math.log10(at_kick / half)
    e0 = envelope(pad, SR, 10)
    neg = 20 * math.log10(np.mean([e0[int((b * beat + 0.012) * SR)] for b in range(1, 7)]) / np.mean([e0[int((b * beat + beat / 2 + 0.02) * SR)] for b in range(1, 7)]))
    return [check("pad dips ~-4 dB (duck 0.4) on each kick", -5.5 < dip < -3.0, dip, -4.4),
            check("recovered at half a beat (full level)", abs(20 * math.log10(half / np.mean(e0[int(0.5 * SR):int(3.5 * SR)]))) < 0.6,
                  20 * math.log10(half / np.mean(e0[int(0.5 * SR):int(3.5 * SR)])), 0),
            check("negative control: raw pad does not pump", abs(neg) < 0.5, neg, 0)], [out, so]


@card("BEAT-23")
def score_mix_bus(task, wd):
    """score.Score.mix: kick-driven pumping on bass/music (duck 55 %), bus gains, seeded room reverb, tanh soft clip, 10 ms end fade; stems."""
    S = vmod("score")
    sc = S.Score(120, 3.0, "A", "minor", 7)
    sc.arrange({"sections": [{"from": 0, "to": 6, "kick": "four", "pad": True}], "chords": [[0, "i"]]})
    pad_raw = sc.bus["music"][0].copy()
    out = Path(wd) / "score.wav"
    sc.mix(out, Path(wd) / "stems")
    stem, sr = load(Path(wd) / "stems" / "music.wav")
    beat = 0.5
    e = envelope(stem, sr, 8)
    e0 = envelope(pad_raw, sr, 8)
    dips = [20 * math.log10((e[int((b * beat + 0.03) * sr)] + 1e-9) / (e[int((b * beat + 0.4) * sr)] + 1e-9)) for b in range(1, 5)]
    raw = [20 * math.log10((e0[int((b * beat + 0.03) * sr)] + 1e-9) / (e0[int((b * beat + 0.4) * sr)] + 1e-9)) for b in range(1, 5)]
    y, _ = load(out)
    return [check("music stem pumps under each kick (>= 3 dB dip)", float(np.mean(dips)) < -3, dips, "< -3"),
            check("soft-clipped master peak <= 0.89", float(np.max(np.abs(fx.read_wav(out)[0]))) <= 0.891, float(np.max(np.abs(fx.read_wav(out)[0]))), "<= 0.89"),
            check("10 ms end fade to silence", abs(y[-1]) < 0.01, float(abs(y[-1])), 0),
            check("negative control: pre-mix pad bus has no pump", abs(float(np.mean(raw))) < 1.5, raw, "~0")], [out, Path(wd) / "stems" / "music.wav"]


def _timeline(wd, spec):
    T = vmod("timeline")
    out = Path(wd) / "film.mp4"
    rep = T.build(spec, out)
    return rep, out


def _tl_fixture(wd, span=(1.0, 2.6), secs=4.0, voice_in_clip=True):
    v = speechlike(secs, [span], f0=170) if voice_in_clip else np.zeros(int(secs * SR))
    save(wd, "clip_audio.wav", np.stack([v, v], 1))
    clip = Path(wd) / "clip.mp4"
    ff("-f", "lavfi", "-i", "color=c=blue:s=320x180:r=30:d=%s" % secs, "-i", Path(wd) / "clip_audio.wav", "-c:v", "libx264",
       "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-shortest", clip)
    save(wd, "music.wav", bed(secs))
    return clip


@card("BEAT-10")
def timeline_duck_clips(task, wd):
    """timeline.build: audio {music {src, gain -6, fade_in .3, fade_out .5}, keep_clip_audio, duck 'clips', lufs -14} → sidechaincompress."""
    clip = _tl_fixture(wd)
    rep, out = _timeline(wd, {"size": "320x180", "fps": 30, "clips": [{"src": str(clip), "in": 0, "out": 4}],
                              "audio": {"music": {"src": str(Path(wd) / "music.wav"), "gain": -6, "fade_in": 0.3, "fade_out": 0.5},
                                        "keep_clip_audio": True, "duck": "clips", "lufs": -14}})
    y, sr = load_any(out)
    drop = bed_drop(y, sr, (1.0, 2.6))
    r = ebur(out)
    fi = narrow_db(y, sr, BED_F[0], 0.0, 0.12) - narrow_db(y, sr, BED_F[0], 0.4, 0.9)
    m, _ = load_any(Path(wd) / "music.wav")
    return [check("duck mode resolved to 'clips'", rep["audio"]["duck"] == "clips", rep["audio"]["duck"], "clips"),
            check("music ducks >= 10 dB under the clip's speech", drop < -10, drop, "< -10"),
            check("mix normalised to -14 LUFS (±1)", abs(r["I"] + 14) <= 1.0, r["I"], -14),
            check("0.3 s music fade-in", fi < -3, fi, "< -3"),
            check("negative control: the bed alone has no dip", abs(bed_drop(m, sr, (1.0, 2.6))) < 0.5, bed_drop(m, sr, (1.0, 2.6)), 0)], [out]


@card("BEAT-137")
def timeline_duck_modes(task, wd):
    """timeline audio.duck auto|voice|clips|none: auto picks voice when a voice track exists; none leaves the bed alone."""
    clip = _tl_fixture(wd, voice_in_clip=False)
    v = speechlike(4.0, [(1.0, 2.6)], f0=170)
    save(wd, "vo.wav", np.stack([v, v], 1))
    base = {"size": "320x180", "fps": 30, "clips": [{"src": str(clip), "in": 0, "out": 4}]}
    au = {"music": {"src": str(Path(wd) / "music.wav"), "fade_out": 0}, "voice": {"src": str(Path(wd) / "vo.wav"), "start": 0}, "lufs": -14}
    T = vmod("timeline")
    r1 = T.build({**base, "audio": {**au, "duck": "auto"}}, Path(wd) / "auto.mp4")
    r2 = T.build({**base, "audio": {**au, "duck": "none"}}, Path(wd) / "none.mp4")
    y1, sr = load_any(Path(wd) / "auto.mp4")
    y2, _ = load_any(Path(wd) / "none.mp4")
    d1, d2 = bed_drop(y1, sr, (1.0, 2.6)), bed_drop(y2, sr, (1.0, 2.6))
    return [check("auto resolves to voice", r1["audio"]["duck"] == "voice", r1["audio"]["duck"], "voice"),
            check("voice ducking ≈ -18 dB (12..26)", -26 <= d1 <= -12, d1, -18),
            check("negative control: duck none leaves the bed (|Δ| < 1.5 dB)", abs(d2) < 1.5 and r2["audio"]["duck"] == "none", d2, 0)], [Path(wd) / "auto.mp4", Path(wd) / "none.mp4"]


@card("BEAT-12")
def timeline_kit_sfx(task, wd):
    """timeline audio.sfx [{src:'kit:reveal-1', at:.5}, {src:'kit:bell-1', at:1.2, gain:-6}]: default gain -10 dB; unknown names fail validation."""
    clip = _tl_fixture(wd, voice_in_clip=False)
    T = vmod("timeline")
    base = {"size": "320x180", "fps": 30, "clips": [{"src": str(clip), "in": 0, "out": 3}]}
    rep = T.build({**base, "audio": {"keep_clip_audio": False, "lufs": -14, "sfx": [{"src": "kit:reveal-1", "at": 0.5}, {"src": "kit:bell-1", "at": 1.2, "gain": -6}]}},
                  Path(wd) / "sfx.mp4")
    y, sr = load_any(Path(wd) / "sfx.mp4")
    on = onsets(y, sr, 0.05, 0.2)
    try:
        T.build({**base, "audio": {"sfx": [{"src": "kit:no-such-sound", "at": 0.5}]}}, Path(wd) / "bad.mp4")
        refused = False
    except Exception:
        refused = True
    kits = sorted(p.stem for p in (VEND / "kit" / "sfx").glob("*.ogg"))
    return [check("two kit sounds start at 0.5 s and 1.2 s (±30 ms)", len(on) >= 2 and abs(on[0] - 0.5) < 0.03 and min(abs(o - 1.2) for o in on) < 0.03, on[:4], [0.5, 1.2]),
            check("kit has >= 20 sounds", len(kits) >= 19, len(kits), ">= 19"),
            check("unknown kit name refused", refused, refused, True),
            check("negative control: the same edit without sfx is silent", _nosfx_ok(T, base, wd), "silent", "silent")], [Path(wd) / "sfx.mp4"]


def _nosfx_ok(T, base, wd):
    p = Path(wd) / "nosfx.mp4"
    T.build({**base, "audio": {"keep_clip_audio": False, "lufs": -14}}, p)
    y, sr = load_any(p)
    return float(np.max(np.abs(y))) < 1e-3


@card("BEAT-83")
def mux_audio_voice_duck(task, wd):
    """motion.mux_audio: every <audio> (src, data-start, data-volume, fades, data-role) mixed; data-role=voice ducks the rest
    (sidechain 0.03/6/20/380) → two-pass loudnorm -14 → AAC 256k 48 kHz."""
    M = vmod("motion")
    save(wd, "music.wav", bed(4.0))
    v = speechlike(3.0, [(0.3, 1.8)], f0=170)
    save(wd, "vo.wav", v)
    idx = Path(wd) / "index.html"
    idx.write_text('<div id="root" data-composition-id="main" data-width="160" data-height="90" data-duration="4">'
                   '<audio src="music.wav" data-start="0" data-duration="4" data-volume="0.8"></audio>'
                   '<audio src="vo.wav" data-start="0.7" data-duration="3" data-role="voice"></audio></div>', encoding="utf-8")
    film = Path(wd) / "film.mp4"
    ff("-f", "lavfi", "-i", "color=c=black:s=160x90:r=30:d=4", "-c:v", "libx264", "-pix_fmt", "yuv420p", film)
    M.mux_audio(idx, film)
    st = fx.probe(film)["streams"]
    y, sr = load_any(film)
    drop = bed_drop(y, sr, (1.0, 2.5))
    r = ebur(film)
    return [check("audio stream muxed (AAC 48 kHz)", any(s["codec_type"] == "audio" and s["codec_name"] == "aac" and s["sample_rate"] == "48000" for s in st),
                  [s["codec_name"] for s in st], "aac"),
            check("bed ducked under data-role=voice (>= 6 dB)", drop < -6, drop, "< -6"),
            check("two-pass loudnorm -14 LUFS", abs(r["I"] + 14) <= 0.8, r["I"], -14),
            check("negative control: bed source is flat", abs(bed_drop(load_any(Path(wd) / "music.wav")[0], sr, (1.0, 2.5))) < 0.5, bed_drop(load_any(Path(wd) / "music.wav")[0], sr, (1.0, 2.5)), 0)], [film]


def _hf_audio(wd, body, dur, name="out.mp4"):
    d = hf_project(Path(wd) / "hf", body, dur=dur)
    out = hf_render(d, Path(wd) / name)
    y, sr = load_any(out)
    return y, sr, out, d


def _aud(id_, src, dur, extra="", track=0):
    return '<audio id="%s" class="clip" src="%s" data-start="0" data-duration="%s" data-track-index="%d" data-volume="1" %s></audio>' % (id_, src, dur, track, extra)


def _q(obj):
    return json.dumps(obj).replace('"', "&quot;")


@card("BEAT-114")
def hf_automation_volume(task, wd):
    """data-automation volume lane: fade-in 0-1 s, duck to 0.3 at 2-2.2 s, hold, back up 3-3.2 s, fade-out 4-5 s (rendered by HyperFrames)."""
    d = Path(wd) / "hf"
    d.mkdir()
    save(d, "bed.wav", bed(5.0))
    lane = {"version": 1, "lanes": [{"target": "volume", "points": [{"t": 0, "v": 0}, {"t": 1, "v": 1}, {"t": 2, "v": 1}, {"t": 2.2, "v": 0.3},
                                                                   {"t": 3, "v": 0.3}, {"t": 3.2, "v": 1}, {"t": 4, "v": 1}, {"t": 5, "v": 0}]}]}
    y, sr, out, _ = _hf_audio(wd, _aud("music", "bed.wav", 5, 'data-automation="%s"' % _q(lane)), 5)
    full = narrow_db(y, sr, BED_F[0], 1.2, 1.9)
    duck = narrow_db(y, sr, BED_F[0], 2.3, 2.9) - full
    back = narrow_db(y, sr, BED_F[0], 3.3, 3.9) - full
    fin = narrow_db(y, sr, BED_F[0], 0.0, 0.3) - full
    return [check("duck to 0.3 = -10.5 dB at 2.2-3 s", abs(duck + 10.46) < 1.0, duck, -10.46),
            check("back to full at 3.2-4 s", abs(back) < 1.0, back, 0),
            check("fade-in: first 0.3 s well below full", fin < -10, fin, "< -10"),
            check("negative control: source bed is flat", abs(flat(load(d / "bed.wav")[0], 2.3, 2.9, 1.2, 1.9)) < 0.3, flat(load(d / "bed.wav")[0], 2.3, 2.9, 1.2, 1.9), 0)], [out]


@card("BEAT-121")
def hf_automation_fx_param(task, wd):
    """data-automation lane on fx.<node>.<param>: a gain node's dB ridden from 0 to -20 dB (rendered by HyperFrames)."""
    d = Path(wd) / "hf"
    d.mkdir()
    save(d, "bed.wav", bed(3.0))
    chain = {"version": 1, "nodes": [{"type": "gain", "id": "g1", "params": {"gain": 0}}]}
    lane = {"version": 1, "lanes": [{"target": "fx.g1.gain", "points": [{"t": 0, "v": 0}, {"t": 1.0, "v": 0}, {"t": 1.5, "v": -20}, {"t": 3, "v": -20}]}]}
    y, sr, out, _ = _hf_audio(wd, _aud("music", "bed.wav", 3, 'data-fx-chain="%s" data-automation="%s"' % (_q(chain), _q(lane))), 3)
    dd = narrow_db(y, sr, BED_F[0], 1.8, 2.8) - narrow_db(y, sr, BED_F[0], 0.2, 0.9)
    return [check("fx.g1.gain lane takes the track down 20 dB", abs(dd + 20) < 1.5, dd, -20),
            check("negative control: source bed is flat", abs(flat(load(d / "bed.wav")[0], 1.8, 2.8)) < 0.3, flat(load(d / "bed.wav")[0], 1.8, 2.8), 0)], [out]


@card("BEAT-108")
def hf_automation_curve(task, wd):
    """Automation points with curve -1..1: the same 1→0 ramp with curve 0 and curve 0.9 renders different midpoints."""
    d = Path(wd) / "hf"
    d.mkdir()
    save(d, "bed.wav", bed(3.0))
    mk = lambda c: _q({"version": 1, "lanes": [{"target": "volume", "points": [{"t": 0, "v": 1}, {"t": 0.5, "v": 1, "curve": c}, {"t": 2.5, "v": 0.05}, {"t": 3, "v": 0.05}]}]})
    body = _aud("a", "bed.wav", 3, 'data-automation="%s"' % mk(0))
    y0, sr, o0, _ = _hf_audio(wd, body, 3, "curve0.mp4")
    shutil.rmtree(Path(wd) / "hf" / "renders", ignore_errors=True)
    body = _aud("a", "bed.wav", 3, 'data-automation="%s"' % mk(0.9))
    (Path(wd) / "hf" / "index.html").unlink()
    y1, _, o1, _ = _hf_audio(wd, body, 3, "curve09.mp4")
    m0 = narrow_db(y0, sr, BED_F[0], 1.3, 1.7) - narrow_db(y0, sr, BED_F[0], 0.1, 0.4)
    m1 = narrow_db(y1, sr, BED_F[0], 1.3, 1.7) - narrow_db(y1, sr, BED_F[0], 0.1, 0.4)
    lin = 20 * math.log10(1 - 0.95 * 0.5)
    return [check("curve 0 is a linear ramp (midpoint ≈ %.1f dB)" % lin, abs(m0 - lin) < 1.5, m0, lin),
            check("curve 0.9 bends the segment (midpoint differs >= 2 dB)", abs(m1 - m0) >= 2, [m0, m1], "differ"),
            check("negative control: the source bed has no ramp", abs(flat(load(d / "bed.wav")[0], 1.3, 1.7, 0.1, 0.4)) < 0.3, flat(load(d / "bed.wav")[0], 1.3, 1.7, 0.1, 0.4), 0)], [o0, o1]


@card("BEAT-107")
def hf_fx_chain_order(task, wd):
    """Per-clip effects in signal order (highpass → pitchshift +12 st → delay → limiter) rendered by HyperFrames' Web Audio graph."""
    d = Path(wd) / "hf"
    d.mkdir()
    x = tone(60, 2.0, 0.4) + np.concatenate([tone(440, 0.3, 0.4), np.zeros(int(1.7 * SR))])
    save(d, "src.wav", x)
    chain = {"version": 1, "nodes": [{"type": "highpass", "id": "hp", "params": {"frequency": 200}},
                                     {"type": "pitchshift", "id": "ps", "params": {"semitones": 12, "mix": 1}},
                                     {"type": "delay", "id": "dl", "params": {"time": 600, "feedback": 0, "wet": 0.5, "dry": 1}},
                                     {"type": "limiter", "id": "lim", "params": {"limit": -1}}]}
    y, sr, out, _ = _hf_audio(wd, _aud("a", "src.wav", 2, 'data-fx-chain="%s"' % _q(chain)), 2)
    p = peak_hz(y[int(0.08 * sr):int(0.28 * sr)], sr)
    hum = narrow_db(y, sr, 60, 0.4, 0.55) - narrow_db(x, SR, 60, 0.4, 0.55)
    echo = narrow_db(y, sr, 880, 0.75, 0.9) - narrow_db(y, sr, 880, 0.4, 0.55)
    return [check("pitchshift +12 st: 440 Hz comes out at 880 Hz", abs(p - 880) < 15, p, 880),
            check("highpass 200 Hz removes the 60 Hz hum (>= 15 dB)", hum < -15, hum, "< -15"),
            check("600 ms delay repeats the note", echo > 10, echo, "> 10 dB"),
            check("limiter last: peak <= -0.9 dBFS", peak_db(y) <= -0.9, peak_db(y), "<= -1"),
            check("negative control: source note is at 440 Hz", abs(peak_hz(x[:int(0.3 * SR)]) - 440) < 5, peak_hz(x[:int(0.3 * SR)]), 440)], [out]


@card("BEAT-117")
def hf_fx_chain_dynamics(task, wd):
    """data-fx-chain compressor (threshold -18, ratio 3) then limiter last; the render runs the same Web Audio graph as preview."""
    d = Path(wd) / "hf"
    d.mkdir()
    t = tt(2.0)
    x = np.where(t < 1.0, 0.9, 0.09) * np.sin(2 * np.pi * 330 * t)
    save(d, "src.wav", x)
    chain = {"version": 1, "nodes": [{"type": "compressor", "id": "c1", "params": {"threshold": -18, "ratio": 3}},
                                     {"type": "limiter", "id": "l1", "params": {"limit": -1}}]}
    y, sr, out, _ = _hf_audio(wd, _aud("a", "src.wav", 2, 'data-fx-chain="%s"' % _q(chain)), 2)
    span_in = seg_db(x, SR, 0.3, 0.9) - seg_db(x, SR, 1.3, 1.9)
    span_out = seg_db(y, sr, 0.3, 0.9) - seg_db(y, sr, 1.3, 1.9)
    return [check("compressor narrows the 20 dB step by >= 6 dB", span_in - span_out >= 6, [span_in, span_out], ">= 6"),
            check("limiter ceiling -1 dB", peak_db(y) <= -0.9, peak_db(y), "<= -1"),
            check("negative control: source step is 20 dB", abs(span_in - 20) < 0.2, span_in, 20)], [out]


@card("BEAT-118")
def hf_fx_defaults(task, wd):
    """Effect registry defaults: highpass default 300 Hz and lowpass default 8000 Hz (nodes with no params), measured on tones."""
    d = Path(wd) / "hf"
    d.mkdir()
    t = tt(2.0)
    x = 0.25 * (np.sin(2 * np.pi * 75 * t) + np.sin(2 * np.pi * 1200 * t) + np.sin(2 * np.pi * 16000 * t))
    save(d, "src.wav", x)
    chain = {"version": 1, "nodes": [{"type": "highpass", "id": "h"}, {"type": "lowpass", "id": "l"}]}
    y, sr, out, _ = _hf_audio(wd, _aud("a", "src.wav", 2, 'data-fx-chain="%s"' % _q(chain)), 2)
    rel = lambda s, f: narrow_db(s, SR, f, 0.3, 1.7) - narrow_db(s, SR, 1200, 0.3, 1.7)
    lo, hi = rel(y, 75) - rel(x, 75), rel(y, 16000) - rel(x, 16000)
    return [check("default highpass (300 Hz, 12 dB/oct) takes 75 Hz down >= 18 dB", lo <= -18, lo, "<= -18"),
            check("default lowpass (8 kHz) takes 16 kHz down >= 9 dB", hi <= -9, hi, "<= -9"),
            check("negative control: source partials are equal", abs(rel(x, 75)) < 0.5 and abs(rel(x, 16000)) < 0.5, [rel(x, 75), rel(x, 16000)], 0)], [out]


@card("BEAT-120")
def hf_audio_group_bus(task, wd):
    """<hf-audio-group id=voiceover data-fx-chain=...> + <audio data-audio-group=voiceover>: one chain for all narration clips."""
    d = Path(wd) / "hf"
    d.mkdir()
    save(d, "a.wav", tone(300, 2.0, 0.3))
    save(d, "b.wav", tone(500, 2.0, 0.3))
    save(d, "c.wav", tone(700, 2.0, 0.3))
    chain = {"version": 1, "nodes": [{"type": "gain", "id": "g", "params": {"gain": -12}}]}
    body = ('<hf-audio-group id="voiceover" data-volume="1" data-fx-chain="%s"></hf-audio-group>' % _q(chain) +
            _aud("v1", "a.wav", 2, 'data-audio-group="voiceover"', 0) + _aud("v2", "b.wav", 2, 'data-audio-group="voiceover"', 1) + _aud("m", "c.wav", 2, "", 2))
    y, sr, out, _ = _hf_audio(wd, body, 2)
    g1 = narrow_db(y, sr, 300, 0.3, 1.7) - narrow_db(y, sr, 700, 0.3, 1.7)
    g2 = narrow_db(y, sr, 500, 0.3, 1.7) - narrow_db(y, sr, 700, 0.3, 1.7)
    return [check("both group members -12 dB against the ungrouped track", abs(g1 + 12) < 1 and abs(g2 + 12) < 1, [g1, g2], -12),
            check("negative control: source tracks are equal level", abs(dbfs(load(d / "a.wav")[0]) - dbfs(load(d / "c.wav")[0])) < 0.1, dbfs(load(d / "a.wav")[0]) - dbfs(load(d / "c.wav")[0]), 0)], [out]


SPACE = {"room-tight": {"size": .25, "damping": .6, "wet": .18, "dry": .9}, "room-natural": {"size": .5, "damping": .5, "wet": .25, "dry": .85},
         "hall": {"size": .9, "damping": .3, "wet": .4, "dry": .75}}


@card("BEAT-122")
def hf_space_presets(task, wd):
    """Space presets (values from HyperFrames' preset table): room-tight vs hall reverb; the hall's tail is longer and louder."""
    d = Path(wd) / "hf"
    d.mkdir()
    x = np.concatenate([speechlike(0.3, [(0, 0.3)], amp=0.5), np.zeros(int(2.7 * SR))])
    save(d, "hit.wav", x)
    tails = {}
    outs = []
    for k in ("room-tight", "hall"):
        chain = {"version": 1, "nodes": [{"type": "reverb", "id": "r", "label": k, "params": SPACE[k]}]}
        (d / "index.html").unlink(missing_ok=True)
        y, sr, out, _ = _hf_audio(wd, _aud("a", "hit.wav", 3, 'data-fx-chain="%s"' % _q(chain)), 3, k + ".mp4")
        tails[k] = seg_db(y, sr, 0.9, 1.4) - seg_db(y, sr, 0.05, 0.25)
        outs.append(out)
    return [check("hall tail louder than tight room at 0.6-1.1 s after the hit", tails["hall"] > tails["room-tight"] + 6, tails, "hall > tight + 6"),
            check("negative control: dry hit has no tail", seg_db(x, SR, 0.9, 1.4) < -100, seg_db(x, SR, 0.9, 1.4), "< -100")], outs


@card("BEAT-123")
def hf_one_knob(task, wd):
    """One-knob profile 'Evenness' (compressor): threshold -12-18t, ratio 2+4t, attack 25-20t, release 300-210t, makeup t²·9.5."""
    d = Path(wd) / "hf"
    d.mkdir()
    t = tt(2.0)
    x = np.where(t < 1.0, 0.9, 0.09) * np.sin(2 * np.pi * 330 * t)
    save(d, "src.wav", x)
    knob = lambda v: {"threshold": round(-12 - v * 18, 2), "ratio": round(2 + v * 4, 2), "attack": round(25 - v * 20, 2),
                      "release": round(300 - v * 210, 2), "makeup": round(v * v * 9.5, 2)}
    spans = {}
    outs = []
    for v in (0.0, 1.0):
        chain = {"version": 1, "nodes": [{"type": "compressor", "id": "c", "params": knob(v)}]}
        (d / "index.html").unlink(missing_ok=True)
        y, sr, out, _ = _hf_audio(wd, _aud("a", "src.wav", 2, 'data-fx-chain="%s"' % _q(chain)), 2, "even_%d.mp4" % v)
        spans[v] = seg_db(y, sr, 0.3, 0.9) - seg_db(y, sr, 1.3, 1.9)
        outs.append(out)
    return [check("Evenness 1 squashes the 20 dB step more than Evenness 0 (>= 4 dB)", spans[0.0] - spans[1.0] >= 4, spans, "knob 1 < knob 0"),
            check("knob mapping at 1: thr -30, ratio 6, attack 5, release 90", knob(1) == {"threshold": -30, "ratio": 6, "attack": 5, "release": 90, "makeup": 9.5}, knob(1), "-30/6/5/90"),
            check("negative control: source step is 20 dB", abs(seg_db(x, SR, 0.3, 0.9) - seg_db(x, SR, 1.3, 1.9) - 20) < 0.2, seg_db(x, SR, 0.3, 0.9) - seg_db(x, SR, 1.3, 1.9), 20)], outs


@card("BEAT-126")
def hf_auto_duck_lane(task, wd):
    """media-use audio-duck.mjs --meta words.json --target '#bgm' --composition index.html → a volume lane, rendered by HyperFrames."""
    d = Path(wd) / "hf"
    d.mkdir()
    save(d, "bgm.wav", bed(4.0))
    v = speechlike(4.0, [(1.0, 2.6)], f0=170)
    save(d, "vo.wav", v)
    jdump(d / "words.json", [{"text": "a", "start": 1.0, "end": 1.6}, {"text": "b", "start": 1.7, "end": 2.6}])
    hf_project(d, _aud("bgm", "bgm.wav", 4) + _aud("vo", "vo.wav", 4, "", 1), dur=4)
    root = hf_root()
    env = {**os.environ, "DO_NOT_TRACK": "1", "HYPERFRAMES_NO_TELEMETRY": "1"}
    res = json.loads(sh(["node", root / "dist/skills/media-use/scripts/audio-duck.mjs", "--meta", "words.json", "--target", "#bgm",
                         "--composition", "index.html", "--json"], cwd=d, env=env).strip().splitlines()[-1])
    html = (d / "index.html").read_text().replace('id="bgm" ', 'id="bgm" data-automation="%s" ' % _q(res["lane"]))
    (d / "index.html").write_text(html)
    out = hf_render(d, Path(wd) / "ducked.mp4")
    y, sr = load_any(out)
    drop = narrow_db(y, sr, BED_F[0], 1.3, 2.5) - narrow_db(y, sr, BED_F[0], 0.2, 0.9)
    return [check("one merged speech span 1.0-2.6 s", res["spans"] == [{"start": 1.0, "end": 2.6}], res["spans"], [{"start": 1.0, "end": 2.6}]),
            check("bgm at 0.25 (-12 dB) under narration", abs(drop + 12.04) < 1.5, drop, -12.04),
            check("negative control: source bgm is flat", abs(flat(load(d / "bgm.wav")[0], 1.3, 2.5)) < 0.3, flat(load(d / "bgm.wav")[0], 1.3, 2.5), 0)], [out, d / "index.html"]


GAPS["BEAT-119"] = "carve.mjs needs the @hyperframes/core npm package (audio-carve), which is not installed here; installing packages is out of scope"
