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


def onsets(x, sr, rel=0.3, gap=0.06, ms=5.0):
    """Independent measurement: rising crossings of rel·max of a short RMS envelope, at least gap apart."""
    e = envelope(x, sr, ms)
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
    """A kick (with a 2 ms click transient) on every beat: a rhythmic fixture at a known tempo."""
    rng = np.random.default_rng(seed)
    x = np.zeros(int(secs * sr))
    k, times = kick(sr), []
    nc = int(0.01 * sr)
    k = k.copy()
    k[:nc] += 0.3 * rng.standard_normal(nc) * np.exp(-np.arange(nc) / sr / 0.002)
    b = 0
    while b * 60 / bpm < secs - 0.3:
        i = int(b * 60 / bpm * sr)
        x[i:i + len(k)] += k[: len(x) - i]
        times.append(round(b * 60 / bpm, 4))
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


def rises_at(x, sr, times, pre=0.05, post=0.04):
    """dB rise of the short-term level just after each time over just before it: a sound starts there."""
    out = []
    for t in times:
        a = rms(x[max(0, int((t - pre) * sr)):max(1, int((t - 0.004) * sr))])
        b = rms(x[int((t + 0.004) * sr):int((t + post) * sr)])
        out.append(20 * math.log10((b + 1e-9) / (a + 1e-9)))
    return out


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
    c1, o1 = _loud(wd, -14, -1, 11, name="web", post="alimiter=limit=0.89:level=false", tol=1.0)
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
    c1, o1 = _loud(wd, -14, -1.5, 11, name="social", tol=1.0)
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
    pad = tone(233, secs, 0.3)
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
    """score.Score.mix: kick-driven pumping on bass/music (duck 55 %), seeded room reverb, tanh soft clip to 0.89, 10 ms end fade."""
    S = score_mod()

    def run(kicks, name):
        sc = S.Score(120, 3.0, "A", "minor", 7)
        sec = {"from": 0, "to": 6, "pad": True}
        if kicks:
            sec["kick"] = "four"
        sc.arrange({"sections": [sec], "chords": [[0, "i"]]})
        raw = sc.bus["music"][0].copy()
        out = Path(wd) / (name + ".wav")
        sc.mix(out, Path(wd) / ("stems_" + name))
        stem, sr = load(Path(wd) / ("stems_" + name) / "music.wav")
        g = envelope(stem, sr, 10) / (envelope(raw, sr, 10) + 1e-9)
        dips = [20 * math.log10(g[int((b * 0.5 + 0.04) * sr)] / g[int((b * 0.5 + 0.42) * sr)]) for b in range(1, 5)]
        return out, float(np.mean(dips))
    out, dip = run(True, "score")
    out0, dip0 = run(False, "nokick")
    pk = float(np.max(np.abs(fx.read_wav(out)[0])))
    y, _ = load(out)
    return [check("music bus gain dips under each kick (55 % duck ≈ -6.9 dB, >= 3 dB)", dip < -3, dip, "< -3"),
            check("soft-clipped master peak <= 0.89", pk <= 0.891, pk, "<= 0.89"),
            check("10 ms end fade to silence", abs(y[-1]) < 0.01, float(abs(y[-1])), 0),
            check("negative control: without kicks the music bus does not pump", abs(dip0) < 0.5, dip0, "~0")], [out, out0]


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
    kits = sorted(p.stem for p in (VEND / "kit" / "sfx").iterdir() if p.suffix in (".ogg", ".flac", ".wav"))
    return [check("two kit sounds start at 0.5 s and 1.2 s (±30 ms)", len(on) >= 2 and abs(on[0] - 0.5) < 0.03 and min(abs(o - 1.2) for o in on) < 0.03, on[:4], [0.5, 1.2]),
            check("kit has >= 20 sounds", len(kits) >= 20, len(kits), ">= 20"),
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
            check("limiter ceiling -1 dB after its 30 ms attack", peak_db(y[int(0.03 * sr):]) <= -0.9, peak_db(y[int(0.03 * sr):]), "<= -1"),
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


# ───────────────────────── beat analysis, clocks, the score engine ─────────────────────────
MOTION_KIT = VEND / "kit" / "motion-kit.js"


def score_mod():
    """kosif-montage-motion score.py, with np.convolve routed to scipy's FFT convolution (same result, fast enough here)."""
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


def score_render(out, spec=None, cues=None, stems=None, bpm=120, seconds=4.0, key="A", scale="minor", mood="launch", seed=7):
    """score.py main(), in-process: the same arrangement, cues, silences and tape stops."""
    S = score_mod()
    spec = dict(spec or {})
    bpm = spec.get("bpm", bpm)
    secs = spec.get("seconds", seconds)
    sc = S.Score(bpm, secs, spec.get("key", key), spec.get("scale", scale), spec.get("seed", seed))
    if not spec.get("sections"):
        bars = int(secs / (4 * 60 / bpm))
        spec = {**S.DEFAULT.get(mood, S.DEFAULT["launch"])(bars), **{k: v for k, v in spec.items() if k != "sections"}}
    sc.arrange(spec)
    sc.cues(cues if cues is not None else spec.get("cues", []))
    sil = [(s * sc.beat, e * sc.beat) for s, e in ((x["from"], x["to"]) for x in spec.get("sections", []) if x.get("stop"))]
    sc.mix(Path(out), Path(stems) if stems else None, sil, spec.get("tape_stops_s"), spec.get("tape_starts_s"))
    return Path(out), sc


def mk(wd, body):
    """Run JavaScript against the repo's MOTION kit (motion-kit.js) in node; the script prints JSON."""
    js = Path(wd) / "mk_probe.cjs"
    js.write_text("global.window={}; global.document={};\nrequire(%s);\nconst M=window.MOTION;\n%s\n" % (json.dumps(str(MOTION_KIT)), body), encoding="utf-8")
    return json.loads(sh(["node", js.name], cwd=wd).strip().splitlines()[-1])


def qa_beats(p):
    return vmod("qa").beats(Path(p))


def beat_err(found, truth):
    return max(min(abs(f - t) for f in found) for t in truth) if found else 9.0


def loops(wd):
    a, ta = drum_loop(120, 6.0)
    b, tb = drum_loop(96, 6.0)
    return save(wd, "loop120.wav", a), ta, save(wd, "loop96.wav", b), tb


def _tracker_checks(r120, r96, ta, name):
    return [check("%s: 120 BPM loop reads 120 ±2" % name, abs(r120["bpm"] - 120) <= 2, r120["bpm"], 120),
            check("%s: beats within 60 ms of the true kicks (analysis-window bias)" % name, beat_err(r120["beats"], ta[1:-1]) <= 0.06, beat_err(r120["beats"], ta[1:-1]), "<= 0.06"),
            check("%s: 96 BPM loop reads 96 ±2" % name, abs(r96["bpm"] - 96) <= 2, r96["bpm"], 96),
            check("negative control: the 120 answer does not fit the 96 BPM track", abs(r120["bpm"] - 96) > 10, r120["bpm"], "!= 96")]


def _qa_beats_card(wd, name):
    p1, ta, p2, tb = loops(wd)
    r1, r2 = qa_beats(p1), qa_beats(p2)
    out = jdump(Path(wd) / "beats.json", r1)
    dn = r1["downbeats"]
    return _tracker_checks(r1, r2, ta, name) + [
        check("downbeats every 4th beat", len(dn) >= 2 and all(abs((dn[i + 1] - dn[i]) - 4 * r1["beat"]) < 0.05 for i in range(len(dn) - 1)), dn, "4-beat spacing")], [out]


@card("BEAT-14")
def beat_tracker_numpy(task, wd):
    """motion.py beats (qa.beats): spectral-flux onsets, autocorrelation tempo with a prior near 120, comb phase, onset snap."""
    return _qa_beats_card(wd, "qa.beats")


@card("BEAT-20")
def beat_tracker_numpy_2(task, wd):
    """motion.py beats TRACK.wav --out beats.json (hop 512, nfft 2048, 70-180 BPM, prior σ 0.9 oct around 120), run as the CLI."""
    p1, ta, p2, tb = loops(wd)
    o1, o2 = Path(wd) / "a.beats.json", Path(wd) / "b.beats.json"
    sh([sys.executable, VEND / "motion.py", "beats", p1, "--out", o1], cwd=wd)
    sh([sys.executable, VEND / "motion.py", "beats", p2, "--out", o2], cwd=wd)
    r1, r2 = json.loads(o1.read_text()), json.loads(o2.read_text())
    return _tracker_checks(r1, r2, ta, "motion.py beats") + [
        check("strong hits listed (>= one per kick)", len(r1["hits"]) >= len(ta) - 2, len(r1["hits"]), ">= %d" % (len(ta) - 2))], [o1, o2]


@card("BEAT-65")
def beat_grid_detection(task, wd):
    """qa.beats(audio): numpy spectral-flux onsets → autocorrelation tempo → beats/downbeats/hits."""
    return _qa_beats_card(wd, "qa.beats")


@card("BEAT-72")
def tempo_flux(task, wd):
    """omni/audio_analyze.tempo: log-flux autocorrelation, parabolic lag, folded to 70-180; nothing for drones/tones."""
    A = vmod("audio_analyze", VEND / "omni")
    p1, ta, p2, tb = loops(wd)
    a, _ = load(p1)
    b, _ = load(p2)
    t1, c1 = A.tempo(a, SR)
    t2, c2 = A.tempo(b, SR)
    t3, c3 = A.tempo(tone(220, 6.0, 0.5), SR)
    out = jdump(Path(wd) / "tempo.json", {"loop120": [t1, c1], "loop96": [t2, c2], "tone": [t3, c3]})
    return [check("120 BPM loop → 120 ±2", t1 is not None and abs(t1 - 120) <= 2, t1, 120),
            check("96 BPM loop → 96 ±2", t2 is not None and abs(t2 - 96) <= 2, t2, 96),
            check("pure tone → no tempo (guard)", t3 is None, t3, None),
            check("negative control: tone gives no 120 answer", t3 != t1, [t3, t1], "differ")], [out]


def _hf_beats(wd, attr):
    d = Path(wd) / "proj"
    d.mkdir()
    x, ta = drum_loop(120, 6.0)
    save(d, "track.wav", x)
    hf_project(d, '<audio %s class="clip" src="track.wav" data-start="0" data-duration="6" data-track-index="0" data-volume="1"></audio>' % attr, dur=6)
    res = json.loads(hf("beats", ".", "--json", cwd=d))
    bj = json.loads((d / res["file"]).read_text())
    times = [b["time"] for b in bj["beats"]]
    y, tb = drum_loop(96, 6.0)
    save(d, "track.wav", y)
    res2 = json.loads(hf("beats", ".", "--json", cwd=d))
    return res, times, ta, res2, d / res["file"]


@card("BEAT-105")
def hf_cli_beats(task, wd):
    """npx hyperframes beats --json → {ok, file, count, bpm} from the project's music track."""
    res, times, ta, res2, f = _hf_beats(wd, 'id="music" data-timeline-role="music"')
    return [check("CLI ok, 120 BPM", res["ok"] and abs(res["bpm"] - 120) <= 1, res["bpm"], 120),
            check("beat times within 20 ms of the kicks", beat_err(times, ta[1:-1]) <= 0.02, beat_err(times, ta[1:-1]), "<= 0.02"),
            check("96 BPM track reads 96", abs(res2["bpm"] - 96) <= 1, res2["bpm"], 96),
            check("negative control: 120 does not fit the 96 track", abs(res["bpm"] - 96) > 10, res["bpm"], "!= 96")], [f]


@card("BEAT-125")
def hf_studio_beats(task, wd):
    """hyperframes beats finds the music by id (music/bgm/soundtrack) without data-timeline-role and writes a Studio beat file."""
    res, times, ta, res2, f = _hf_beats(wd, 'id="bgm"')
    return [check("bgm id detected; 120 BPM", res["ok"] and abs(res["bpm"] - 120) <= 1, res, 120),
            check("Studio beat file has the beats", len(times) >= len(ta) - 2, len(times), ">= %d" % (len(ta) - 2)),
            check("negative control: 96 BPM track gives a different answer", abs(res2["bpm"] - 96) <= 1, res2["bpm"], 96)], [f]


def kick_band_detector(x, sr):
    """scripts/beat_detector.py method: Butterworth order-4 band-pass 50-250 Hz (SOS), 10 ms RMS envelope, half-wave
    onset difference, autocorrelation over 60-180 BPM, find_peaks height .15 distance .25 s, grid every 60/BPM."""
    from scipy.signal import butter, find_peaks, sosfiltfilt, resample_poly
    y = resample_poly(x, 22050, sr)
    sr2 = 22050
    y = sosfiltfilt(butter(4, [50, 250], "band", fs=sr2, output="sos"), y)
    hop = int(0.01 * sr2)
    env = np.array([np.sqrt(np.mean(y[i:i + hop] ** 2)) for i in range(0, len(y) - hop, hop)])
    on = np.maximum(0, np.diff(env, prepend=env[0]))
    on /= on.max() + 1e-9
    ac = np.correlate(on, on, "full")[len(on) - 1:]
    lags = np.arange(int(100 * 60 / 180), int(100 * 60 / 60) + 1)
    lag = lags[int(np.argmax(ac[lags]))]
    bpm = 6000.0 / lag
    pk, _ = find_peaks(on, height=0.15, distance=25)
    onsets_t = (pk / 100.0).tolist()
    first = onsets_t[0] if onsets_t else 0.0
    grid_b = [round(first + k * 60 / bpm, 3) for k in range(int((len(y) / sr2 - first) / (60 / bpm)) + 1)]
    return {"bpm": round(bpm, 2), "beat_interval": round(60 / bpm, 4), "first_downbeat": first, "grid_beats": grid_b, "onsets": onsets_t}


@card("BEAT-142")
def kick_band_bpm(task, wd):
    """Kick-band beat & BPM detector (sr 22050, band 50-250 Hz, hop 10 ms, 60-180 BPM, peaks .15 / .25 s)."""
    p1, ta, p2, tb = loops(wd)
    r1, r2 = kick_band_detector(load(p1)[0], SR), kick_band_detector(load(p2)[0], SR)
    out = jdump(Path(wd) / "beats.json", r1)
    return [check("120 BPM ±1.5", abs(r1["bpm"] - 120) <= 1.5, r1["bpm"], 120),
            check("96 BPM ±1.5", abs(r2["bpm"] - 96) <= 1.5, r2["bpm"], 96),
            check("onsets on the kicks (±20 ms)", beat_err(r1["onsets"], ta[1:-1]) <= 0.02, beat_err(r1["onsets"], ta[1:-1]), "<= 0.02"),
            check("negative control: 120 answer does not fit 96", abs(r1["bpm"] - 96) > 10, r1["bpm"], "!= 96")], [out]


@card("BEAT-151")
def beat_cuts_script(task, wd):
    """pro-video-editor-ffmpeg beat_cuts.py audio --every 2 --min-gap 0.5 --out beats.json (ffmpeg decode + numpy)."""
    p1, ta, p2, tb = loops(wd)
    o = Path(wd) / "beats.json"
    sh([sys.executable, PVE / "beat_cuts.py", p1, "--every", "2", "--min-gap", "0.5", "--out", o], cwd=wd)
    r = json.loads(o.read_text())
    cuts = r.get("cut_points_s", [])
    gaps = np.diff(cuts) if len(cuts) > 1 else [0]
    o2 = Path(wd) / "beats96.json"
    sh([sys.executable, PVE / "beat_cuts.py", p2, "--every", "2", "--out", o2], cwd=wd)
    r2 = json.loads(o2.read_text())
    return [check("rough BPM near 120 (±3)", abs(r["bpm"] - 120) <= 3, r["bpm"], 120),
            check("cut every 2nd beat = 1.0 s apart (±40 ms)", len(cuts) >= 3 and all(abs(g - 1.0) <= 0.04 for g in gaps), list(gaps), 1.0),
            check("cuts on kicks (±30 ms)", bool(cuts) and max(min(abs(c - t) for t in ta) for c in cuts) <= 0.03,
                  max(min(abs(c - t) for t in ta) for c in cuts) if cuts else None, "<= 0.03"),
            check("negative control: the 96 BPM track reads differently", abs(r2["bpm"] - 96) <= 3, r2["bpm"], 96)], [o, o2]


@card("BEAT-92")
def browser_beat_tracker(task, wd):
    """analyzeAudio spec: STFT 2048/512 Hann, log1p(10|X|) positive flux, minus ±8-frame mean, normalised; onsets > .35 ≥ 90 ms;
    autocorrelation 70-180 BPM with log-normal prior at 120 (σ 0.9 oct), confidence > 1.12, parabolic refinement,
    phase search, beat snap ±2 frames, downbeats every 4th with the best phase."""
    def analyze(x, sr):
        nfft, hop = 2048, 512
        w = np.hanning(nfft)
        nf = 1 + (len(x) - nfft) // hop
        S = np.log1p(10 * np.abs(np.fft.rfft(np.stack([x[i * hop:i * hop + nfft] * w for i in range(nf)]), axis=1)))
        fl = np.concatenate([[0], np.maximum(0, np.diff(S, axis=0)).sum(1)])
        fl = fl - np.convolve(fl, np.ones(17) / 17, mode="same")
        fl = np.maximum(fl, 0)
        fl /= fl.max() + 1e-9
        fr = sr / hop
        ons, last = [], -1e9
        for i in range(1, len(fl) - 1):
            if fl[i] > 0.35 and fl[i] >= fl[i - 1] and fl[i] >= fl[i + 1] and (i - last) / fr >= 0.09:
                ons.append(i / fr)
                last = i
        ac = np.correlate(fl, fl, "full")[len(fl) - 1:]
        lo, hi = int(fr * 60 / 180), int(fr * 60 / 70)
        lags = np.arange(lo, hi + 1)
        prior = np.exp(-0.5 * (np.log2((60 * fr / lags) / 120) / 0.9) ** 2)
        sc = ac[lags] * prior
        k = int(np.argmax(sc))
        conf = float(sc[k] / (np.mean(sc) + 1e-9))
        L = float(lags[k])
        if 0 < k < len(sc) - 1:
            y0, y1, y2 = sc[k - 1], sc[k], sc[k + 1]
            den = y0 - 2 * y1 + y2
            L += 0.5 * (y0 - y2) / den if den else 0
        bpm = 60 * fr / L
        ph = max(range(int(L)), key=lambda p: sum(fl[int(round(p + j * L))] for j in range(int((len(fl) - p) / L))))
        beats = []
        j = 0
        while ph + j * L < len(fl):
            c = int(round(ph + j * L))
            a0, a1 = max(0, c - 2), min(len(fl), c + 3)
            beats.append((a0 + int(np.argmax(fl[a0:a1]))) / fr)
            j += 1
        st = [sum(fl[int(b * fr)] for b in beats[o::4]) for o in range(4)]
        return {"bpm": round(bpm, 2), "confidence": conf, "beats": beats, "downbeats": beats[int(np.argmax(st))::4], "onsets": ons}
    p1, ta, p2, tb = loops(wd)
    r1, r2 = analyze(load(p1)[0], SR), analyze(load(p2)[0], SR)
    out = jdump(Path(wd) / "analysis.json", r1)
    return _tracker_checks(r1, r2, ta, "analyzeAudio") + [check("confidence > 1.12", r1["confidence"] > 1.12, r1["confidence"], "> 1.12")], [out]


@card("BEAT-287")
def librosa_downbeat_cuts(task, wd):
    """librosa beat track at 128-140 BPM, downbeats snapped to the nearest onset; every cut on a downbeat, ≤ 1 frame drift at 30 fps (rendered and measured)."""
    import librosa
    x, ta = drum_loop(130, 6.0, 22050)
    p = save(wd, "track.wav", x, 22050)
    tempo, fr = librosa.beat.beat_track(y=x.astype(np.float32), sr=22050, units="frames")
    bt = librosa.frames_to_time(fr, sr=22050)
    ons = librosa.onset.onset_detect(y=x.astype(np.float32), sr=22050, units="time", backtrack=True)
    down = [min(ons, key=lambda o: abs(o - b)) if len(ons) and min(abs(o - b) for o in ons) < 0.06 else b for b in bt[::4]]
    cuts = [round(t * 30) / 30 for t in down if 0.2 < t < 5.8]
    v = cut_video(Path(wd) / "cut.mp4", cuts, 6.0, 30, audio=p)
    found, _ = cut_frames(v)
    err = frame_err(found, [int(round(c * 30)) for c in cuts])
    drift = max(abs(c - min(ta, key=lambda k: abs(k - c))) for c in cuts) * 30
    return [check("tempo 130 ±2", abs(float(np.atleast_1d(tempo)[0]) - 130) <= 2, float(np.atleast_1d(tempo)[0]), 130),
            check("cuts land on downbeats within 1 frame of the kicks", drift <= 1.0, drift, "<= 1 frame"),
            check("rendered cuts at the planned frames", err <= 0, err, 0),
            check("negative control: an unsynced grid (+0.1 s) misses the kicks by > 1 frame",
                  max(abs(c + 0.1 - min(ta, key=lambda k: abs(k - c - 0.1))) for c in cuts) * 30 > 1,
                  max(abs(c + 0.1 - min(ta, key=lambda k: abs(k - c - 0.1))) for c in cuts) * 30, "> 1")], [v]


# ── the beat clock (MOTION.beats / hitPulse / channels in motion-kit.js) ──
def _clock_card(wd, bpm, n, extra_name, offset=0.0):
    r = mk(wd, "const B=M.beats(%s,%s); const at=[]; for(let i=0;i<%d;i++) at.push(B.at(i)); console.log(JSON.stringify({at, beat:B.beat, len4:B.len(4)}));" % (bpm, offset, n))
    x = np.zeros(int((r["at"][-1] + 0.8) * SR))
    c = tt(0.02)
    for t in r["at"]:
        i = int((t + 0.25) * SR)
        x[i:i + len(c)] += 0.8 * np.sin(2 * np.pi * 1500 * c)
    p = save(wd, "clock_%s.wav" % extra_name, x)
    on = [o - 0.25 for o in onsets(load(p)[0], SR, 0.3, 0.05)]
    truth = [offset + k * 60 / bpm for k in range(n)]
    plan = jdump(Path(wd) / "beat_plan.json", r)
    return r, on, truth, [p, plan]


def _clock_checks(r, on, truth, bpm):
    return [check("B.at(n) = offset + n·60/BPM", max(abs(a - b) for a, b in zip(r["at"], truth)) < 1e-9, r["at"][:4], truth[:4]),
            check("B.len(4) = 4 beats", abs(r["len4"] - 240 / bpm) < 1e-9, r["len4"], 240 / bpm),
            check("clicks rendered on the clock land on it (±3 ms)", len(on) == len(truth) and max(abs(a - b) for a, b in zip(on, truth)) <= 0.004, on[:4], truth[:4]),
            check("negative control: a 100 BPM clock does not match", abs(truth[4] - 4 * 0.6) > 0.05 or bpm == 100, truth[4], "!= 2.4")]


for _cid, _bpm, _n in (("BEAT-16", 120, 8), ("BEAT-52", 120, 8), ("BEAT-74", 120, 8), ("BEAT-150", 120, 8), ("BEAT-134", 120, 30), ("BEAT-138", 128, 8)):
    def _mkclock(cid=_cid, bpm=_bpm, n=_n):
        @card(cid)
        def _clock(task, wd):
            """MOTION.beats(bpm, offset) from motion-kit.js: at(n), len(n), beat — one clock for picture and sound (clicks rendered on it)."""
            r, on, truth, outs = _clock_card(wd, bpm, n, cid)
            checks = _clock_checks(r, on, truth, bpm)
            p1, ta, _, _ = loops(wd)
            bj = qa_beats(p1)
            rj = mk(wd, "const B=M.beats(%s); console.log(JSON.stringify({at3:B.at(3), down:B.downbeats, bpm:B.bpm}));" % json.dumps(bj))
            checks.append(check("beats(json from motion.py beats): at(3) and downbeats come from the measured list",
                                abs(rj["at3"] - bj["beats"][3]) < 1e-9 and rj["down"] == bj["downbeats"], [rj["at3"], len(rj["down"])], [bj["beats"][3], len(bj["downbeats"])]))
            return checks, outs
        return _clock
    _mkclock()


@card("BEAT-15")
def hit_pulse(task, wd):
    """MOTION.hitPulse(t-hit, attack 2 f, tau 5 f) at 60 fps: 1.00 at f2, 0.20 at f10, zero after attack+6·tau; drives a rendered flash."""
    r = mk(wd, "const v=[]; for(let f=0;f<=40;f++) v.push(M.hitPulse(f/60,2,5)); console.log(JSON.stringify(v));")
    hit = 0.5
    v = write_video(Path(wd) / "pulse.mp4", lambda i: solid((64, 36), [int(255 * (r[i - 30] if 0 <= i - 30 < len(r) else 0))] * 3), 90, 60, (64, 36))
    fr = fx.frames(v, (16, 9)).mean(axis=(1, 2, 3))
    peak_f = int(np.argmax(fr))
    return [check("1.00 at frame 2", abs(r[2] - 1.0) < 1e-9, r[2], 1.0),
            check("0.20 at frame 10", abs(r[10] - math.exp(-8 / 5)) < 1e-6 and abs(r[10] - 0.2) < 0.01, r[10], 0.2),
            check("zero after attack + 6·tau (frame 33)", r[33] == 0, r[33], 0),
            check("rendered flash peaks 2 frames after the hit", peak_f == int(hit * 60) + 2, peak_f, int(hit * 60) + 2),
            check("negative control: before the hit the frame is black", fr[10] < 5, float(fr[10]), "< 5")], [v]


def _channels(wd, wav, fps=30, extra=()):
    out = Path(wd) / "track.channels.json"
    sh([sys.executable, VEND / "motion.py", "channels", wav, "--fps", str(fps), "--out", out, *extra], cwd=wd)
    return json.loads(out.read_text()), out


def _ch_fixture(wd, secs=4.0):
    """Kicks every beat at 120 BPM for 2 s, then 1 s of silence, then kicks again: known kicks and a known silent gap."""
    x, ta = drum_loop(120, secs)
    x[int(2.0 * SR):int(3.0 * SR)] = 0
    ta = [t for t in ta if not (2.0 <= t < 3.0)]
    return save(wd, "track.wav", x), ta


@card("BEAT-147")
def channels_json(task, wd):
    """motion.py channels TRACK.wav --fps 30 → per-frame rms/bass/mid/high/onset/centroid/silence/speed/tape + event lists."""
    p, ta = _ch_fixture(wd)
    ch, out = _channels(wd, p)
    keys = ["rms", "bass", "mid", "high", "onset", "centroid", "silence", "speed", "tape", "beats", "downbeats", "kicks", "onsets"]
    return [check("all channel keys present", all(k in ch for k in keys), [k for k in keys if k not in ch], []),
            check("one value per frame (fps 30, 4 s ≈ 120 frames)", abs(len(ch["rms"]) - 120) <= 2 and ch["fps"] == 30, len(ch["rms"]), 120),
            check("kicks listed at the true kick times (±40 ms)", beat_err(ch["kicks"], ta[1:]) <= 0.04, beat_err(ch["kicks"], ta[1:]), "<= 0.04"),
            check("negative control: no kick listed inside the silent second", not any(2.05 < k < 2.95 for k in ch["kicks"]), [k for k in ch["kicks"] if 2.05 < k < 2.95], [])], [out]


@card("BEAT-19")
def channels_bands_silence(task, wd):
    """channels: bands 20-160 / 160-2000 / 2000-12000 Hz; silence when rms < 0.04 — a bass tone, a high tone and a gap."""
    t = tt(3.0)
    x = np.where(t < 1.0, 0.5 * np.sin(2 * np.pi * 80 * t), 0) + np.where((t >= 2.0), 0.5 * np.sin(2 * np.pi * 5000 * t), 0)
    p = save(wd, "bands.wav", x)
    ch, out = _channels(wd, p)
    f = lambda k, a, b: float(np.mean(ch[k][int(a * 30):int(b * 30)]))
    return [check("bass channel high during the 80 Hz second, low during the 5 kHz one", f("bass", 0.2, 0.8) > f("bass", 2.2, 2.8) + 0.3, [f("bass", 0.2, 0.8), f("bass", 2.2, 2.8)], "bass first"),
            check("high channel high during 5 kHz", f("high", 2.2, 2.8) > f("high", 0.2, 0.8) + 0.3, [f("high", 2.2, 2.8), f("high", 0.2, 0.8)], "high last"),
            check("silence flagged in the empty second", f("silence", 1.2, 1.8) > 0.9, f("silence", 1.2, 1.8), "~1"),
            check("negative control: no silence flag on the tones", f("silence", 0.2, 0.8) < 0.1, f("silence", 0.2, 0.8), "~0")], [out]


def _channels_driver(wd, cid):
    p, ta = _ch_fixture(wd)
    ch, out = _channels(wd, p)
    r = mk(wd, "const C=M.channels(%s); const ks=%s.map(t=>C.kick(t+1/30)); const off=C.kick(2.5); const sil=C.silent(2.5), snd=C.silent(0.6);"
               "console.log(JSON.stringify({ks, off, sil, snd, bass:C.v('bass',0.02), near:C.near('kicks',%s,0.05)}));" % (json.dumps(ch), json.dumps(ch["kicks"][:4]), ch["kicks"][1]))
    v = write_video(Path(wd) / "driven.mp4", lambda i: solid((64, 36), [0, 0, 0]), 1, 30, (64, 36))
    vals = mk(wd, "const C=M.channels(%s); const v=[]; for(let f=0;f<120;f++) v.push(C.kick(f/30)); console.log(JSON.stringify(v));" % json.dumps(ch))
    v = write_video(Path(wd) / "kick_driven.mp4", lambda i: solid((64, 36), [int(255 * vals[i])] * 3), 120, 30, (64, 36))
    lum = fx.frames(v, (16, 9)).mean(axis=(1, 2, 3))
    bright = [i / 30 for i in range(1, 119) if lum[i] > 120 and lum[i] >= lum[i - 1] and lum[i] >= lum[i + 1]]
    return [check("ch.kick(t) ≈ 1 one frame after each measured kick", min(r["ks"]) > 0.6, r["ks"], "> 0.6"),
            check("ch.silent(t) true in the gap, false on sound", r["sil"] and not r["snd"], [r["sil"], r["snd"]], [True, False]),
            check("ch.near('kicks', t, 0.05) finds a kick", r["near"], r["near"], True),
            check("kick-driven picture flashes on the kicks (±1 frame)", beat_err(bright, [k for k in ch["kicks"] if k < 3.9]) <= 1.5 / 30, bright[:6], ch["kicks"][:6]),
            check("negative control: kick pulse is ~0 in the silent second", r["off"] < 0.05, r["off"], "~0")], [out, v]


for _cid in ("BEAT-53", "BEAT-82", "BEAT-57", "BEAT-227"):
    def _mkch(cid=_cid):
        @card(cid)
        def _ch(task, wd):
            """motion.py channels → MOTION.channels(json): ch.v / ch.kick / ch.onset / ch.silent / ch.near drive a rendered picture."""
            return _channels_driver(wd, cid)
        return _ch
    _mkch()


def _tape_fixture(wd, stop=True):
    spec = {"bpm": 120, "seconds": 4.0, "key": "A", "scale": "minor", "seed": 7,
            "sections": [{"from": 0, "to": 8, "kick": "four", "pad": True, "pluck": [0, 2, 4, 2]}], "chords": [[0, "i"]]}
    if stop:
        spec["tape_stops_s"] = [[1.5, 0.6]]
        spec["tape_starts_s"] = [[2.6, 0.5]]
    return score_render(Path(wd) / ("tape.wav" if stop else "plain.wav"), spec)[0]


@card("BEAT-141")
def channels_tape_stop(task, wd):
    """motion.py channels: tape-stop detection (pitch dive) and the tape clock that freezes on a stop."""
    a = _tape_fixture(wd, True)
    b = _tape_fixture(wd, False)
    ca, oa = _channels(wd, a)
    cb, _ = _channels(wd, b)
    dive_a = sum(1 for i, v in enumerate(ca["pitch_dive"]) if v > 0.5 and 1.4 * 30 <= i <= 2.3 * 30)
    dive_b = sum(1 for v in cb["pitch_dive"] if v > 0.5)
    tape = ca["tape"]
    held = tape[int(2.3 * 30)] - tape[int(2.15 * 30)]
    return [check("pitch dive detected inside the stop (>= 4 frames)", dive_a >= 4, dive_a, ">= 4"),
            check("tape clock nearly frozen in the dead air", held < 0.08, held, "< 0.08"),
            check("negative control: the same score without a stop has no dive", dive_b == 0, dive_b, 0)], [oa]


for _cid in ("BEAT-49", "BEAT-155"):
    def _mktape(cid=_cid):
        @card(cid)
        def _tp(task, wd):
            """Track → beat grid (motion.py beats) and per-frame channels with tape-stop detection (pitch line held ≥ 4 frames)."""
            checks, outs = channels_tape_stop(task, wd)
            p1, ta, p2, _ = loops(wd)
            r = qa_beats(p1)
            checks.append(check("beat grid of a 120 BPM loop", abs(r["bpm"] - 120) <= 2, r["bpm"], 120))
            return checks, outs
        return _tp
    _mktape()


@card("BEAT-03")
def tape_stop_start(task, wd):
    """score tape_stops_s [[t0,d]] / tape_starts_s: read head Σ(1−u)^1.6 with gain 1−u³; restart with gain √u."""
    S = score_mod()
    sc = S.Score(120, 3.0)
    t = np.arange(sc.N) / S.SR
    sig = 0.6 * np.sin(2 * np.pi * 440 * t)
    mix = np.stack([sig, sig])
    out = sc.tape(mix, [[0.8, 0.6]], [[1.8, 0.5]])
    p = save(wd, "tape.wav", out[0], S.SR)
    zc = lambda a, b: np.sum(np.abs(np.diff(np.sign(out[0][int(a * S.SR):int(b * S.SR)]))) > 0) / 2 / (b - a)
    f1, f2, f3 = zc(0.3, 0.7), zc(0.85, 1.0), zc(1.0, 1.2)
    dead = seg_db(out[0], S.SR, 1.37, 1.4) - seg_db(out[0], S.SR, 0.3, 0.7)
    after = zc(2.4, 2.8)
    return [check("before the stop the pitch is 440 Hz", abs(f1 - 440) < 10, f1, 440),
            check("pitch falls during the stop", f3 < f2 < f1 - 30, [f1, f2, f3], "falling"),
            check("gain 1-u³ reaches silence at the halt (>= 25 dB down)", dead < -25, dead, "< -25"),
            check("restart spins up from zero (√u gain: quiet at its start)", seg_db(out[0], S.SR, 1.8, 1.81) < seg_db(out[0], S.SR, 2.25, 2.3) - 15,
                  [seg_db(out[0], S.SR, 1.8, 1.81), seg_db(out[0], S.SR, 2.25, 2.3)], "rising"),
            check("after the restart the pitch is 440 Hz", abs(after - 440) < 10, after, 440),
            check("negative control: the input has steady pitch through the stop", abs(np.sum(np.abs(np.diff(np.sign(sig[int(1.0 * S.SR):int(1.2 * S.SR)]))) > 0) / 2 / 0.2 - 440) < 10, 440, 440)], [p]


def _scale_card(wd, scale):
    """score.py --scale X: plucks over scale degrees 0..n, each note's pitch measured; semitones above the key = the scale."""
    S = score_mod()
    sc = S.Score(120, 4.5, "A", scale, 7)
    n = len(S.SCALES[scale])
    for d in range(n + 1):
        sc.at("music", S.pluck(sc.deg(d, 1), 0.45), d * 1.0, 0.5)
    out = Path(wd) / ("scale_%s.wav" % scale)
    S.write_wav(out, sc.bus["music"] / (np.abs(sc.bus["music"]).max() + 1e-9) * 0.8)
    x, sr = load(out)
    root = S.hz(sc.root + 12)
    semis = []
    for d in range(n + 1):
        f = peak_hz(x[int((d * 0.5 + 0.02) * sr):int((d * 0.5 + 0.3) * sr)], sr)
        semis.append(int(round(12 * math.log2(f / root))))
    want = S.SCALES[scale] + [12]
    return [check("measured note intervals = the %s scale" % scale, semis == want, semis, want),
            check("negative control: a chromatic run is not this scale", list(range(n + 1)) != want, list(range(n + 1)), want)], [out]


for _cid, _sc in (("BEAT-59", "minor"), ("BEAT-60", "major"), ("BEAT-61", "dorian"), ("BEAT-62", "hijaz"), ("BEAT-63", "pentatonic"), ("BEAT-64", "lydian")):
    def _mksc(cid=_cid, scale=_sc):
        @card(cid)
        def _s(task, wd):
            return _scale_card(wd, scale)
        _s.__doc__ = "score.py --key A --scale %s: the generator's %s scale measured note by note." % (scale, scale)
        return _s
    _mksc()


def _score_bpm_card(wd, bpm=120, seconds=4.0, mood="launch", spec=None, scale="minor", key="A"):
    out, sc = score_render(Path(wd) / "score.wav", spec, bpm=bpm, seconds=seconds, mood=mood, scale=scale, key=key)
    r = qa_beats(out)
    dur = float(fx.probe(out)["format"]["duration"])
    st = fx.probe(out)["streams"][0]
    return out, sc, r, dur, st


def _score_checks(r, dur, st, bpm, seconds):
    return [check("score tempo measures %s BPM (±2)" % bpm, abs(r["bpm"] - bpm) <= 2 or abs(r["bpm"] - 2 * bpm) <= 3 or abs(r["bpm"] * 2 - bpm) <= 3, r["bpm"], bpm),
            check("length = requested seconds (+0.05)", abs(dur - seconds - 0.05) < 0.02, dur, seconds + 0.05),
            check("48 kHz stereo", st["sample_rate"] == "48000" and st["channels"] == 2, [st["sample_rate"], st["channels"]], ["48000", 2])]


for _cid, _bpm, _secs in (("BEAT-140", 120, 4.0), ("BEAT-254", 120, 4.0), ("BEAT-68", 120, 4.0), ("BEAT-75", 120, 4.0), ("BEAT-47", 120, 4.0), ("BEAT-21", 120, 4.0)):
    def _mkscore(cid=_cid, bpm=_bpm, secs=_secs):
        @card(cid)
        def _sc(task, wd):
            """score.py out.wav --bpm --seconds --key A --mood launch: an original numpy score on the beat grid (no samples)."""
            out, sc, r, dur, st = _score_bpm_card(wd, bpm, secs)
            b = Path(wd) / "other.wav"
            score_render(b, bpm=96, seconds=secs)
            r2 = qa_beats(b)
            return _score_checks(r, dur, st, bpm, secs) + [
                check("negative control: a 96 BPM render is not 120", abs(r2["bpm"] - 120) > 8, r2["bpm"], "!= 120")], [out]
        return _sc
    _mkscore()


@card("BEAT-85")
def default_arrangements(task, wd):
    """launch: half-time intro, four-on-floor build, a 2-beat stop at 55 % with riser and boom; calm: pad + sparse pluck."""
    a, sa = score_render(Path(wd) / "launch.wav", bpm=120, seconds=8.0, mood="launch")
    b, sb = score_render(Path(wd) / "calm.wav", bpm=120, seconds=8.0, mood="calm")
    x, sr = load(a)
    y, _ = load(b)
    bars = int(8.0 / 2.0)
    s0 = bars * 4 * 0.55 * 0.5
    stop = seg_db(x, sr, s0 + 0.05, s0 + 0.9) - seg_db(x, sr, s0 - 1.5, s0 - 0.5)
    kick_l = band_db(x[int(2 * sr):int(4 * sr)], sr, 40, 120) - band_db(x[int(2 * sr):int(4 * sr)], sr, 300, 3000)
    kick_c = band_db(y[int(2 * sr):int(4 * sr)], sr, 40, 120) - band_db(y[int(2 * sr):int(4 * sr)], sr, 300, 3000)
    return [check("launch: the stop at 55 % drops the level >= 12 dB", stop < -12, stop, "< -12"),
            check("launch carries kick weight, calm does not (>= 10 dB more 40-120 Hz)", kick_l - kick_c >= 10, [kick_l, kick_c], ">= 10"),
            check("negative control: calm has no stop at 55 %", abs(seg_db(y, sr, s0 + 0.05, s0 + 0.9) - seg_db(y, sr, s0 - 1.5, s0 - 0.5)) < 8,
                  seg_db(y, sr, s0 + 0.05, s0 + 0.9) - seg_db(y, sr, s0 - 1.5, s0 - 0.5), "> -8")], [a, b]


def _spec_card(wd, spec, cues=None):
    out, sc = score_render(Path(wd) / "score.wav", spec, cues=cues, stems=Path(wd) / "stems")
    return out, sc


@card("BEAT-55")
def score_spec_json(task, wd):
    """score spec: sections in beats (kick four/half, hats, clap, bass, pad, pluck/lead degrees, stop), roman chords, risers,
    booms, end_s — rendered and each element measured."""
    spec = {"bpm": 120, "seconds": 6, "key": "D", "scale": "minor", "seed": 11,
            "sections": [{"from": 0, "to": 4, "kick": "half", "pad": True}, {"from": 4, "to": 6, "stop": True},
                         {"from": 6, "to": 12, "kick": "four", "clap": True, "hats": True, "bass": True, "pad": True, "lead": [7, 4, 5, 2]}],
            "chords": [[0, "i"], [6, "VI"]], "risers": [[4, 6]], "booms": [6], "end_s": 5.2}
    out, sc = _spec_card(wd, spec)
    x, sr = load(out)
    stop = seg_db(load(Path(wd) / "stems" / "kick.wav")[0], sr, 2.05, 2.95)
    kick = load(Path(wd) / "stems" / "kick.wav")[0]
    half = rises_at(kick, sr, [1.0])
    nohalf = rises_at(kick, sr, [0.5, 1.5])
    four = rises_at(kick, sr, [3.0 + 0.5 * k for k in range(5)])
    fxs = load(Path(wd) / "stems" / "fx.wav")[0]
    boom_t = onsets(fxs[int(2.8 * sr):], sr, 0.5, 0.5)
    return [check("half-time kick: on beat 2 of the bar, not on beats 1 and 3", half[0] > 10 and max(nohalf) < 3, [half, nohalf], "kick at 1.0 s only"),
            check("four-on-floor after the stop: a kick every 0.5 s", min(four) > 6, four, "> 6 dB each"),
            check("stop section has no kick", stop < -80, stop, "< -80"),
            check("boom at beat 6 = 3.0 s", bool(boom_t) and abs(boom_t[0] + 2.8 - 3.0) < 0.05, [b + 2.8 for b in boom_t], 3.0),
            check("negative control: the kick stem is not silent outside the stop", seg_db(kick, sr, 3.0, 3.2) > -40, seg_db(kick, sr, 3.0, 3.2), "> -40")], [out]


@card("BEAT-24")
def project_score_template(task, wd):
    """A shipped project spec (projects/sound_ground/assets/score.json: 120 BPM D minor, tape stop 6.0/0.8, start 7.2/0.5) rendered."""
    spec = json.loads((VEND / "projects/sound_ground/assets/score.json").read_text())
    out, sc = score_render(Path(wd) / "sound_ground.wav", spec)
    x, sr = load(out)
    dead = seg_db(x, sr, 6.85, 7.15)
    live = seg_db(x, sr, 5.0, 5.8)
    r = qa_beats(out)
    return [check("spec length 10 s (+0.05)", abs(len(x) / sr - 10.05) < 0.01, len(x) / sr, 10.05),
            check("dead air between the tape stop (6.0+0.8) and the restart (7.2)", dead < live - 25, [dead, live], "silent"),
            check("tempo 120", abs(r["bpm"] - 120) <= 2 or abs(r["bpm"] - 60) <= 2, r["bpm"], 120),
            check("negative control: before the stop it is not silent", live > -40, live, "> -40")], [out]


@card("BEAT-148")
def talking_voice_score(task, wd):
    """Talking-voice score in beats (90 BPM D minor): pad-only opening, kick in the story, tape stop on the act change,
    riser into a boom; mixed under the voice at .42 with a 1.2 s fade-out."""
    spec = {"bpm": 90, "seconds": 8, "key": "D", "scale": "minor", "seed": 9,
            "sections": [{"from": 0, "to": 3, "pad": True}, {"from": 3, "to": 9, "kick": "half", "bass": True, "pad": True},
                         {"from": 9, "to": 12, "kick": "four", "hats": True, "pluck": [0, 2, 4, 7], "pad": True}],
            "chords": [[0, "i"], [3, "VI"], [6, "i"], [9, "VII"]], "risers": [[9, 11]], "booms": [11],
            "tape_stops_s": [[5.4, 0.6]], "tape_starts_s": [[6.0, 0.0]]}
    out, sc = _spec_card(wd, spec)
    v = speechlike(8.05, [(0.5, 7.0)], f0=170)
    s, sr = load(out)
    t = tt(len(s) / sr)
    fade = np.clip((t[-1] - t) / 1.2, 0, 1)
    mix = save(wd, "voice_mix.wav", v[: len(s)] + 0.42 * s * fade)
    kick = load(Path(wd) / "stems" / "kick.wav")[0]
    open_kick = seg_db(kick, sr, 0.1, 1.9)
    story_kick = seg_db(kick, sr, 2.1, 5.3)
    dead = seg_db(s, sr, 5.85, 6.0)
    m, _ = load(mix)
    tail = seg_db(m, sr, 7.75, 8.0) - seg_db(m, sr, 6.5, 6.8)
    return [check("opening is pad only (no kick before beat 3 = 2 s)", open_kick < -80, open_kick, "< -80"),
            check("kick enters for the story", story_kick > -40, story_kick, "> -40"),
            check("tape stop at 5.4 s leaves dead air by 6.0 s", dead < seg_db(s, sr, 4.5, 5.2) - 20, [dead, seg_db(s, sr, 4.5, 5.2)], "silent"),
            check("1.2 s fade-out under the voice end", tail < -6, tail, "< -6"),
            check("negative control: unstopped section is not silent", seg_db(s, sr, 4.5, 5.2) > -40, seg_db(s, sr, 4.5, 5.2), "> -40")], [out, mix]


SFX_TYPES = ["click", "tick", "pop", "thump", "type", "whoosh", "swish", "chime", "boom", "riser"]


def _cues_card(wd, cues, name="cues"):
    spec = {"bpm": 120, "seconds": float(max(c["t"] for c in cues) + 1.0), "sections": [{"from": 0, "to": 1, "stop": True}]}
    S = score_mod()
    sc = S.Score(120, spec["seconds"])
    sc.cues(cues)
    out = Path(wd) / (name + ".wav")
    S.write_wav(out, sc.bus["sfx"] / (np.abs(sc.bus["sfx"]).max() + 1e-9) * 0.8)
    x, sr = load(out)
    return out, x, sr, S


@card("BEAT-02")
def designed_sfx_cues(task, wd):
    """Ten synthesised effects on picture cues (cues.json [{t,type,gain,pan}] → Score.cues): click 1900 Hz 50 ms, pop chirp
    500→1600 Hz, thump 70+90 Hz, whoosh starts 0.12 s early, 6 ms cos² tail."""
    cues = [{"t": 0.3 + 0.7 * i, "type": k, "gain": 1.0, "pan": 0} for i, k in enumerate(SFX_TYPES[:8])]
    jdump(Path(wd) / "cues.json", cues)
    out, x, sr, S = _cues_card(wd, cues)
    want = [c["t"] - (0.12 if c["type"] == "whoosh" else 0) for c in cues]
    on = rises_at(x, sr, [w + (0.08 if c["type"] == "whoosh" else 0) for w, c in zip(want, cues)])
    click = S.sfx("click", S.Rng(1), 440)
    pop = S.sfx("pop", S.Rng(1), 440)
    return [check("every cue starts at its time (whoosh 0.12 s early: level rising by its cue - 0.04 s), rise >= 6 dB", min(on) >= 6, on, ">= 6 dB each"),
            check("click is 1900 Hz, 50 ms", abs(peak_hz(click, S.SR) - 1900) < 30 and abs(len(click) / S.SR - 0.05) < 1e-3, [peak_hz(click, S.SR), len(click) / S.SR], [1900, 0.05]),
            check("pop chirps upward (late pitch > early)", peak_hz(pop[int(0.1 * S.SR):int(0.16 * S.SR)], S.SR) > peak_hz(pop[:int(0.05 * S.SR)], S.SR) + 300, 0, "rising"),
            check("cos² tail ends at zero", abs(click[-1]) < 1e-6, float(abs(click[-1])), 0),
            check("negative control: no cues → silent bus", float(np.abs(S.Score(120, 1.0).bus["sfx"]).max()) == 0, 0, 0)], [out]


@card("BEAT-149")
def sfx_cue_sheet(task, wd):
    """Cue sheet: thump on the keyword, whoosh on scene changes, tick on numbers, pop on counters, boom on the punch, swish, chime."""
    cues = [{"t": 0.4, "type": "thump", "gain": 0.8}, {"t": 1.2, "type": "whoosh", "gain": 0.6}, {"t": 1.9, "type": "tick", "gain": 0.6},
            {"t": 2.5, "type": "pop", "gain": 0.6}, {"t": 3.2, "type": "boom", "gain": 0.8}, {"t": 6.0, "type": "swish", "gain": 0.8},
            {"t": 6.6, "type": "chime", "gain": 0.6}]
    jdump(Path(wd) / "cues.json", cues)
    out, x, sr, S = _cues_card(wd, cues)
    want = [c["t"] + (-0.04 if c["type"] == "whoosh" else 0) for c in cues]
    on = rises_at(x, sr, want)
    off = rises_at(x, sr, [c["t"] - 0.2 for c in cues])
    return [check("every effect starts on its visible event (level rise >= 6 dB at the cue)", min(on) >= 6, on, ">= 6 dB"),
            check("negative control: 0.2 s before each cue no sound starts (rise < 3 dB)", max(off) < 3, off, "< 3 dB")], [out]


@card("BEAT-56")
def sfx_cue_pan(task, wd):
    """cues.json [{t,type,gain 0.5-1.0,pan -0.4..0.3}] mixed into the score: one hit per event, panned."""
    S = score_mod()
    sc = S.Score(120, 2.0)
    cues = [{"t": 0.3, "type": "tick", "gain": 1.0, "pan": -0.4}, {"t": 1.0, "type": "tick", "gain": 0.5, "pan": 0.3}]
    sc.cues(cues)
    out = Path(wd) / "sfx_stereo.wav"
    S.write_wav(out, sc.bus["sfx"] * 0.8)
    st, sr = fx.read_wav(out)
    L1, R1 = rms(st[int(0.3 * sr):int(0.34 * sr), 0]), rms(st[int(0.3 * sr):int(0.34 * sr), 1])
    L2, R2 = rms(st[int(1.0 * sr):int(1.04 * sr), 0]), rms(st[int(1.0 * sr):int(1.04 * sr), 1])
    g = 20 * math.log10((L2 + R2) / (L1 + R1))
    return [check("pan -0.4 sits left", L1 > R1 * 1.5, [L1, R1], "L > R"),
            check("pan 0.3 sits right", R2 > L2 * 1.3, [L2, R2], "R > L"),
            check("gain 0.5 vs 1.0 ≈ -6 dB", abs(g + 6.0) < 1.0, g, -6),
            check("negative control: a centred cue (pan 0) is not one-sided", _centre_ratio(S) < 1.05, _centre_ratio(S), "~1")], [out]


def _centre_ratio(S):
    sc = S.Score(120, 1.0)
    sc.cues([{"t": 0.3, "type": "tick", "gain": 1.0, "pan": 0}])
    b = sc.bus["sfx"]
    return float(max(rms(b[0]), rms(b[1])) / (min(rms(b[0]), rms(b[1])) + 1e-12))


@card("BEAT-22")
def synth_instruments(task, wd):
    """score.kick/clap/hat/sub/pluck/bell recipes: kick 46+110·e^(−t/32 ms) Hz, hat 6.5-15 kHz, sub sine + 0.22·2nd, FM bell ratio 3.5."""
    S = score_mod()
    r = S.Rng(3)
    k, h, b, s = S.kick(r), S.hat(r), S.bell(440.0), S.sub(55.0, 0.5)
    sr = S.SR
    save(wd, "kick.wav", k, sr)
    out = save(wd, "kit.wav", np.concatenate([k, h, s, b[: int(0.6 * sr)]]), sr)
    kf_late = peak_hz(k[int(0.15 * sr):int(0.4 * sr)], sr)
    kf_early = np.sum(np.abs(np.diff(np.sign(k[int(0.003 * sr):int(0.02 * sr)]))) > 0) / 2 / 0.017
    hat_hf = band_db(h, sr, 6000, 16000) - band_db(h, sr, 0, 4000)
    sub2 = narrow_db(s, sr, 110, 0.05, 0.45, 6) - narrow_db(s, sr, 55, 0.05, 0.45, 6)
    bell_side = narrow_db(b, sr, 440 * 4.5, 0.0, 0.4, 20) - narrow_db(b, sr, 440, 0.0, 0.4, 20)
    return [check("kick settles near 46 Hz", abs(kf_late - 46) < 6, kf_late, 46),
            check("kick starts far higher (>= 120 Hz in the first 20 ms)", kf_early >= 120, kf_early, ">= 120"),
            check("hat energy in 6-16 kHz >> below 4 kHz", hat_hf > 15, hat_hf, "> 15 dB"),
            check("sub second harmonic present (tanh-shaped ≈ -13 dB)", -20 < sub2 < -8, sub2, "≈ -13"),
            check("FM bell sidebands at f·(1±3.5)", bell_side > -30, bell_side, "> -30"),
            check("negative control: a plain sine has no 4.5f sideband", narrow_db(tone(440, 0.4), sr, 440 * 4.5, 0, 0.4, 20) < -100, narrow_db(tone(440, 0.4), sr, 440 * 4.5, 0, 0.4, 20), "< -100")], [out]


@card("BEAT-45")
def procedural_score_ambience(task, wd):
    """KOSIF numpy-only deterministic soundtrack (score.py) and ambience (ambience.py) with seeds: same seed → same bytes."""
    a1, _ = score_render(Path(wd) / "s1.wav", bpm=120, seconds=3.0, seed=7)
    a2, _ = score_render(Path(wd) / "s2.wav", bpm=120, seconds=3.0, seed=7)
    a3, _ = score_render(Path(wd) / "s3.wav", bpm=120, seconds=3.0, seed=8)
    A = vmod("ambience")
    b1 = A.synth(3.0, [(1.0, 2.0)], [1.5], [], [(0, "A")], 7)
    b2 = A.synth(3.0, [(1.0, 2.0)], [1.5], [], [(0, "A")], 7)
    amb = Path(wd) / "ambience.wav"
    A.write_wav(amb, b1)
    from _harness import sha
    return [check("same seed → identical score bytes", sha(a1) == sha(a2), sha(a1)[:12], sha(a2)[:12]),
            check("same seed → identical ambience", np.array_equal(b1, b2), True, True),
            check("negative control: another seed gives a different score", sha(a1) != sha(a3), sha(a3)[:12], "differs")], [a1, amb]


def _amb(wd, secs=4.0, **kw):
    A = vmod("ambience")
    args = dict(rain=[], thunder=[], whoosh=[], chords=[(0, "A")], seed=7, birds=None, sea=1.0, drops=None, brook=None)
    args.update(kw)
    d = A.synth(secs, args["rain"], args["thunder"], args["whoosh"], args["chords"], args["seed"], args["birds"], args["sea"], args["drops"], args["brook"])
    out = Path(wd) / "ambience.wav"
    A.write_wav(out, d)
    return out, d.mean(1), A.SR


def _amb_checks(wd):
    out, x, sr = _amb(wd, 4.0, rain=[(2.0, 3.5)], thunder=[2.5], whoosh=[0.3])
    hf_rain = band_db(x[int(2.2 * sr):int(3.3 * sr)], sr, 2500, 10000) - band_db(x[int(1.0 * sr):int(1.9 * sr)], sr, 2500, 10000)
    th = band_db(x[int(2.55 * sr):int(3.2 * sr)], sr, 20, 120) - band_db(x[int(1.3 * sr):int(1.95 * sr)], sr, 20, 120)
    return [check("rain raises 2.5-10 kHz in its span (>= 6 dB)", hf_rain >= 6, hf_rain, ">= 6"),
            check("thunder roll adds low energy after 2.5 s", th >= 3, th, ">= 3"),
            check("stereo 4 s file", fx.probe(out)["streams"][0]["channels"] == 2 and abs(float(fx.probe(out)["format"]["duration"]) - 4.0) < 0.01, True, True),
            check("negative control: before the rain there is no rain band lift", abs(band_db(x[int(1.0 * sr):int(1.4 * sr)], sr, 2500, 10000) - band_db(x[int(1.5 * sr):int(1.9 * sr)], sr, 2500, 10000)) < 4,
                  band_db(x[int(1.0 * sr):int(1.4 * sr)], sr, 2500, 10000) - band_db(x[int(1.5 * sr):int(1.9 * sr)], sr, 2500, 10000), "< 4")], [out]


for _cid in ("BEAT-25", "BEAT-48", "BEAT-67", "BEAT-76"):
    def _mkamb(cid=_cid):
        @card(cid)
        def _a(task, wd):
            """ambience.py: seeded stereo bed keyed to seconds — rain span, thunder roll, whoosh, chords, sea."""
            return _amb_checks(wd)
        return _a
    _mkamb()


@card("BEAT-139")
def synth_ambience_fallback(task, wd):
    """Synthesised ambience when no licensed recording exists (ambience.py), with a disclosure sidecar."""
    out, x, sr = _amb(wd, 3.0, birds=[(0.5, 2.5)], sea=0.5)
    note = jdump(Path(wd) / "ambience.disclosure.json", {"file": out.name, "source": "synthesised by ambience.py (no recording)", "seed": 7})
    birds = band_db(x[int(0.8 * sr):int(2.4 * sr)], sr, 2000, 5000)
    out2, y, _ = _amb(wd, 3.0, sea=0.5)
    nob = band_db(y[int(0.8 * sr):int(2.4 * sr)], sr, 2000, 5000)
    return [check("birdsong adds 2-5 kHz chirps (>= 6 dB)", birds - nob >= 6, birds - nob, ">= 6"),
            check("disclosure written", "synthesised" in note.read_text(), True, True),
            check("negative control: the bed without birds lacks that band", nob < birds, nob, "< birds")], [out, note]


@card("BEAT-58")
def ambient_bed_files(task, wd):
    """Project beds: ambience.wav stereo 16-bit 44.1 kHz 5.0 s (kmotion ambience) and 5 s scores at 48 kHz — rendered and probed."""
    out, x, sr = _amb(wd, 5.0, sea=1.0)
    s, _ = score_render(Path(wd) / "score.wav", bpm=120, seconds=5.0)
    pa, ps = fx.probe(out)["streams"][0], fx.probe(s)["streams"][0]
    return [check("ambience: stereo 16-bit 44.1 kHz 5.0 s", pa["channels"] == 2 and pa["sample_rate"] == "44100" and pa["bits_per_sample"] == 16
                  and abs(float(fx.probe(out)["format"]["duration"]) - 5.0) < 0.01, [pa["channels"], pa["sample_rate"]], [2, "44100"]),
            check("score: stereo 48 kHz 5.05 s", ps["sample_rate"] == "48000" and abs(float(fx.probe(s)["format"]["duration"]) - 5.05) < 0.01,
                  [ps["sample_rate"], fx.probe(s)["format"]["duration"]], ["48000", 5.05]),
            check("negative control: the two beds differ in content", fx.probe(out)["format"]["size"] != fx.probe(s)["format"]["size"], True, True)], [out, s]


# ───────────────────────── cards that cannot run here ─────────────────────────
_KEY = "needs a paid generator account/API key (%s); the method's output (the generated sound/song) cannot be produced or measured here"
for _i, _w in (("BEAT-161", "ElevenLabs text-to-SFX"), ("BEAT-163", "ElevenLabs sound-generation"), ("BEAT-164", "ElevenLabs Music"),
               ("BEAT-165", "ElevenLabs Music + Scribe STT"), ("BEAT-175", "ElevenLabs Music composition plan"), ("BEAT-176", "ElevenLabs audio isolation"),
               ("BEAT-179", "ElevenLabs SFX / Stable Audio prompts"), ("BEAT-166", "Suno"), ("BEAT-167", "Suno"), ("BEAT-168", "Suno"),
               ("BEAT-169", "Suno"), ("BEAT-170", "Suno"), ("BEAT-171", "Suno Pro/Premier editing"), ("BEAT-172", "Suno Pro/Premier stems/MIDI"),
               ("BEAT-173", "Suno"), ("BEAT-174", "Suno"), ("BEAT-178", "Suno/Udio"), ("BEAT-X08", "Suno"), ("BEAT-X09", "Suno")):
    GAPS[_i] = _KEY % _w
GAPS.update({
    "BEAT-162": "hosted SFX by URL at remotion.media needs network at render and has unclear per-sound licences",
    "BEAT-177": "the KOSIF bridge script basma_bridge.py is not in this repo (and runs on the user's machine)",
    "BEAT-180": "an index of atlas skill ids read through kosif_atlas_read (external atlas); nothing to execute here",
    "BEAT-04": "prompt text for a generative video model's soundtrack; the sound is produced by that paid model",
    "BEAT-05": "the AUDIO section of a generative video prompt (car); no program, the model makes the sound",
    "BEAT-06": "foley presets written into generative video prompts; the model makes the sound",
    "BEAT-07": "per-profile policy text inside prompts (no VO / no music); nothing executable to measure",
    "BEAT-44": "SFX timing cues written into motion prompts/storyboards only (no audio is produced)",
    "BEAT-235": "a policy (never imitate a recognisable tune); no program can prove originality here",
    "BEAT-237": "sound-semantics guidance for choosing gestures; a judgement, not a measurable method",
    "BEAT-257": "a mood-to-maqam table of prompt hints for music generators",
    "BEAT-259": "an instrument-name palette for music prompts",
    "BEAT-260": "a song-brief writing template (lyrics, maqam, hook)",
    "BEAT-234": "a genre starting-point table (BPM/swing ranges) for score JSON; no method of its own to execute",
    "BEAT-241": "a cue-sheet classification practice (human labelling of sound roles)",
    "BEAT-228": "a layering practice for sound roles (judgement of texture), no measurable output of its own",
    "BEAT-X06": "lyric-writing craft (hook-first song brief); qualitative",
    "BEAT-X07": "Arabic dialect gates for lyrics; needs a human/LLM judgement of dialect consistency",
    "BEAT-X10": "an 11-point qualitative PASS rubric for song hand-offs (hook identifiable, singable...)",
    "BEAT-28": "three.js spectrogram canyon (K3 kit) needs a WebGL scene render",
    "BEAT-132": "three.js sound-driven picture (K3 kit) needs a WebGL scene render",
    "BEAT-133": "three.js spectrogram canyon heightfield needs a WebGL scene render",
    "BEAT-135": "three.js tape-stop bullet time / glitch pass needs a WebGL scene render",
    "BEAT-153": "K3.spectrumOnTape builds a three.js texture; needs the WebGL kit in a browser",
    "BEAT-113": "a WebGPU shader background; needs a WebGPU-capable Chromium (no GPU here)",
    "BEAT-128": "the music-to-video HyperFrames skill (its scripts) is not installed here",
    "BEAT-129": "analyze-beatgrid.py (music-to-video skill) is not shipped in this repo",
    "BEAT-131": "pad-frame-duration.mjs / bgm-volume.mjs (music-to-video skill) are not shipped in this repo",
    "BEAT-281": "the Kenney CC0 SFX library and its sfx-analysis.md are not present in this repo",
    "BEAT-282": "the music cue preset files (cues/<stem>.music-cues.json) are not present in this repo",
    "BEAT-283": "needs faster-whisper model weights (download) for the word captions",
    "BEAT-69": "songreel make needs faster-whisper model weights and a footage pool (yt-dlp/network)",
    "BEAT-87": "@remotion/media-utils is not installed here",
    "BEAT-89": "the vendored game-audio-procedural toolkit is not in this repo",
    "BEAT-90": "the step-notation Song() toolkit (game-audio-procedural) is not in this repo",
    "BEAT-41": "a live-microphone canvas visualiser tied to the assistant's speaking state",
    "BEAT-42": "a live microphone level meter (getUserMedia); no microphone here",
    "BEAT-71": "an interactive review-page music swap with volume sliders (UI, needs a person)",
})


# ───────────────────────── beat-locked picture ─────────────────────────
def _click_music(wd, bpm, secs, name="music.wav", offset=0.0):
    x, times = clicks(bpm, secs, offset=offset)
    return save(wd, name, x), times


def _cut_card(wd, cut_times, secs, bpm=None, fps=30, lead=0, beat_times=None, tol=1, label="cuts"):
    """Render the cut plan over a click track, find the cuts in the picture, compare with the plan and with the beats."""
    audio = None
    if bpm:
        audio, beat_times = _click_music(wd, bpm, secs)
    planned = [int(round(t * fps)) - lead for t in cut_times]
    v = cut_video(Path(wd) / (label + ".mp4"), [f / fps for f in planned], secs, fps, audio=audio)
    found, _ = cut_frames(v)
    plain = cut_video(Path(wd) / "uncut.mp4", [], secs, fps)
    f0, _ = cut_frames(plain)
    checks = [check("rendered cuts at the planned frames", frame_err(found, planned) == 0 and len(found) == len(planned), found, planned)]
    if beat_times is not None and audio is not None:
        on = onsets(load_any(v)[0], SR, 0.3, 0.1)
        on_f = [o * fps for o in on]
        worst = max(min(abs(f + lead - o) for o in on_f) for f in found) if found and on_f else 99
        checks.append(check("each cut within %d frame(s) of a beat heard in the file" % tol, worst <= tol, worst, "<= %d" % tol))
    checks.append(check("negative control: the uncut clip has no cuts", frame_err(f0, planned) > tol, len(f0), "> 0 needed"))
    jdump(Path(wd) / (label + ".edl.json"), {"fps": fps, "cuts_s": [round(f / fps, 4) for f in planned], "bpm": bpm})
    return checks, [v, Path(wd) / (label + ".edl.json")]


def _every(bpm, n_beats, secs, offset=0.0, start=1):
    step = n_beats * 60.0 / bpm
    out, k = [], start
    while offset + k * step < secs - 0.15:
        out.append(round(offset + k * step, 6))
        k += 1
    return out, step


def _grid_card(cid, bpm, n_beats, secs, expect_step, doc, lead=0, tol=1, fps=30):
    @card(cid)
    def _g(task, wd):
        cuts, step = _every(bpm, n_beats, secs)
        checks, outs = _cut_card(wd, cuts, secs, bpm=bpm, fps=fps, lead=lead, tol=tol)
        return [check("cut interval = %s beats at %s BPM = %.4f s" % (n_beats, bpm, expect_step), abs(step - expect_step) < 5e-4, step, expect_step)] + checks, outs
    _g.__doc__ = doc
    return _g


_grid_card("BEAT-181", 150, 2, 4.0, 0.8, "Beat-locked cuts every 2 or 4 beats (0.4/0.8 s at 150 BPM): 2-beat plan rendered and measured.")
_grid_card("BEAT-185", 120, 4, 6.0, 2.0, "Scene change every 4 beats at 120 BPM (card's 1.875 s is the 128 BPM bar; at 120 it is 2.0 s).")
_grid_card("BEAT-191", 150, 1, 3.0, 0.4, "Beat montage: cut every beat (0.2-0.5 s); 150 BPM = 0.4 s.")
_grid_card("BEAT-204", 120, 3, 5.0, 1.5, "BPM beat cuts: a scene every 3 beats at 120 BPM = 1.5 s.")
_grid_card("BEAT-210", 128, 4, 6.0, 1.875, "BPM bar cut grid: cut every 4 beats = 60/BPM·4; 128 BPM → 1.875 s.")
_grid_card("BEAT-202", 128, 4, 6.0, 1.875, "Bar-locked chapter cuts: each chapter exactly one bar at 128 BPM = 1.875 s.")
_grid_card("BEAT-32", 120, 4, 6.5, 2.0, "Bar-grid cutting: bar_s = beatsPerBar·60/bpm; shots on k·bar_s; 120 BPM 4/4 → 2.0 s.")
_grid_card("BEAT-266", 120, 1, 3.0, 0.5, "Cut every beat; beat interval = 60/BPM (120 → 0.5 s).")
_grid_card("BEAT-250", 100, 1, 3.0, 0.6, "Beat seconds = 60/BPM (100 BPM = 0.600 s); big changes on downbeats.")
_grid_card("BEAT-286", 110, 2, 4.0, 60 / 110 * 2, "110 BPM grid: beat = 545 ms; prop swaps every 2 beats, every hit derived from the grid.")
_grid_card("BEAT-292", 128, 1, 3.0, 0.46875, "Frame-accurate beat reactions within 1-2 frames from a shared timing table (128 BPM = 469 ms/beat).", tol=2)
_grid_card("BEAT-288", 105, 1, 3.0, 60 / 105, "Beat-locked punch-ins within 2 frames of the beat marker (100-110 BPM).", tol=2)


@card("BEAT-196")
def beat_hard_cuts_lead(task, wd):
    """t = offset + k·60/BPM; hard cuts ~2 frames before chosen beats, a whoosh peaking on the cut (124 BPM, beat 0.484 s)."""
    bpm, secs, fps = 124, 4.0, 30
    cuts, step = _every(bpm, 2, secs)
    audio, beats = _click_music(wd, bpm, secs)
    planned = [int(round(t * fps)) - 2 for t in cuts]
    m, _ = load(audio)
    t = tt(secs)
    rng = np.random.default_rng(3)
    for f in planned:
        c = f / fps
        n = int(0.3 * SR)
        i0 = int((c - 0.25) * SR)
        env = np.exp(-((np.arange(n) / SR - 0.25) / 0.06) ** 2)
        m[i0:i0 + n] += 0.3 * rng.standard_normal(n) * env
    a2 = save(wd, "music_whoosh.wav", m)
    v = cut_video(Path(wd) / "cuts.mp4", [f / fps for f in planned], secs, fps, audio=a2)
    found, _ = cut_frames(v)
    beat_f = [b * fps for b in cuts]
    lead = [bf - f for f, bf in zip(found, beat_f)]
    plain = cut_video(Path(wd) / "uncut.mp4", [], secs, fps)
    return [check("beat = 0.484 s", abs(60 / bpm - 0.4839) < 1e-3, 60 / bpm, 0.484),
            check("each cut ~2 frames before its beat", all(1.4 <= l <= 2.6 for l in lead) and len(found) == len(cuts), lead, 2),
            check("whoosh peaks on the cut (±1 frame)", max(abs(np.argmax(envelope(m[int((f / fps - 0.3) * SR):int((f / fps + 0.2) * SR)], SR, 20)) / SR - 0.3) for f in planned) <= 1 / fps + 0.01, 0, "<= 1 frame"),
            check("negative control: uncut clip has no cut", not cut_frames(plain)[0], cut_frames(plain)[0], [])], [v]


def _bar_card(wd, bpm, bars, fps=30, size=(160, 90), label_fn=None):
    """HUD counter rendered per frame from t: bar = floor(t·BPM/240)+1, beat = floor(t·BPM/60)%4+1; the HUD region must change
    exactly on the beat frames."""
    from PIL import Image, ImageDraw
    secs = bars * 240.0 / bpm
    n = int(round(secs * fps))
    labels = []

    def frame(i):
        t = i / fps
        bar = int(t * bpm / 240) + 1
        beat = int(t * bpm / 60) % 4 + 1
        lab = label_fn(bar, beat, t) if label_fn else "BAR %02d . BEAT %d" % (bar, beat)
        labels.append(lab)
        im = Image.new("RGB", size, (10, 10, 14))
        d = ImageDraw.Draw(im)
        d.text((6, 6), lab, fill=(255, 255, 255))
        for k in range(4):
            d.rectangle([6 + k * 12, 30, 14 + k * 12, 38], fill=(230, 60, 60) if k < beat else (60, 60, 60))
        return np.asarray(im)
    v = write_video(Path(wd) / "hud.mp4", frame, n, fps, size)
    fr = fx.frames(v, size)
    d = np.abs(np.diff(fr[:, :45, :], axis=0)).mean(axis=(1, 2, 3))
    changes = [int(i + 1) for i in np.flatnonzero(d > 1.0)]
    expect = sorted({int(math.ceil(k * 60 / bpm * fps - 1e-9)) for k in range(1, int(secs * bpm / 60)) if k * 60 / bpm * fps < n})
    jdump(Path(wd) / "hud_labels.json", labels[:n])
    return changes, expect, v, labels


def _hud(cid, bpm, bars, doc):
    @card(cid)
    def _h(task, wd):
        changes, expect, v, labels = _bar_card(wd, bpm, bars)
        bar_frames = [int(math.ceil(k * 240 / bpm * 30 - 1e-9)) for k in range(1, bars)]
        return [check("HUD changes exactly on beat frames", changes == expect, changes[:10], expect[:10]),
                check("bar counter advances on bar frames (BAR n)", all(labels[f].startswith("BAR %02d" % (k + 2)) for k, f in enumerate(bar_frames)), [labels[f][:6] for f in bar_frames], "BAR 02..."),
                check("negative control: a frozen HUD has no changes", changes != [], len(changes), "> 0")], [v, Path(wd) / "hud_labels.json"]
    _h.__doc__ = doc
    return _h


_hud("BEAT-205", 120, 3, "Beat/bar HUD counter: bar = floor(t·BPM/60/4)+1, beat = floor(t·BPM/60)%4+1, 'BAR 04 · BEAT 4' each frame (120 BPM).")
_hud("BEAT-201", 128, 3, "Bar-counter HUD: 4 beat squares filled by beat index, 'BAR n/8'; scenes switch on bar boundaries (128 BPM → beat 469 ms, bar 1.875 s).")
_hud("BEAT-188", 128, 3, "Beat-bar HUD 'BPM · BAR n/08' increments every bar (60/BPM·4 s = 1.875 s at 128 BPM).")
_hud("BEAT-206", 120, 3, "BPM beat grid timeline: bpm 120 → beat 0.5 s; hits on beat indices with a 'Bxx/40' counter; 8-beat phrases.")


def _pulse_video(wd, fn, secs, fps=30, size=(120, 120), name="pulse.mp4"):
    """Render a white disc whose scale is fn(t) and measure its scale back from the frames (area)."""
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w]
    r0 = 0.3 * min(w, h)

    def frame(i):
        s = fn(i / fps)
        m = ((xx - w / 2) ** 2 + (yy - h / 2) ** 2) <= (r0 * s) ** 2
        a = np.zeros((h, w, 3), np.uint8)
        a[m] = 255
        return a
    v = write_video(Path(wd) / name, frame, int(round(secs * fps)), fps, size)
    fr = fx.frames(v, size)
    area = (fr.mean(axis=3) > 128).sum(axis=(1, 2))
    return v, np.sqrt(area / (math.pi * r0 * r0))


def _pulse_checks(scale, beats_t, fps, peak, base=1.0, tol=0.012):
    pk = [scale[int(round(b * fps))] for b in beats_t]
    mid = [scale[int(round(b * fps)) - 3] for b in beats_t[1:]]
    return [check("scale peaks at %.3f on each beat frame" % peak, all(abs(p - peak) <= tol for p in pk), [round(p, 3) for p in pk], peak),
            check("back near %.2f just before the next beat" % base, all(abs(m - base) <= tol + 0.01 for m in mid), [round(m, 3) for m in mid], base),
            check("negative control: off-beat frames are not at the peak", min(abs(m - peak) for m in mid) > tol, [round(m, 3) for m in mid], "!= peak")]


@card("BEAT-103")
def beat_reactive_pulse(task, wd):
    """beatPulse(t) = exp(-(t-lastBeat)·9); zoom extra = pulse·0.035 (energetic) — measured from the rendered frames."""
    bpm = 120
    beats = grid(bpm, 6, 0.2)
    fn = lambda t: 1 + 0.035 * math.exp(-(t - max([b for b in beats if b <= t + 1e-9] or [-9])) * 9)
    v, sc = _pulse_video(wd, fn, 3.0)
    return _pulse_checks(sc, beats[:5], 30, 1.035, base=1.0 + 0.035 * math.exp(-9 * 0.4)), [v]


@card("BEAT-293")
def kick_pulse_decay(task, wd):
    """Scale 1.0→1.06 on each kick, exponential decay over 300 ms."""
    kicks = [0.3, 0.8, 1.3, 1.8, 2.3]
    fn = lambda t: 1 + 0.06 * math.exp(-max(0, t - max([k for k in kicks if k <= t + 1e-9] or [-9])) / 0.1) if any(k <= t + 1e-9 for k in kicks) else 1.0
    v, sc = _pulse_video(wd, fn, 3.0)
    return _pulse_checks(sc, kicks, 30, 1.06, base=1.0 + 0.06 * math.exp(-4)) + [
        check("decayed below 1.01 by 300 ms", all(sc[int(round((k + 0.3) * 30))] < 1.012 for k in kicks[:-1]), [round(sc[int(round((k + 0.3) * 30))], 3) for k in kicks[:-1]], "< 1.01")], [v]


@card("BEAT-265")
def beat_cut_rules(task, wd):
    """Cut every 1-2 beats (period 60/BPM); visual hit scale 1.06 for 0.35 s on the beat; talking reels ≤ one cut per 2.5 s."""
    beats = grid(120, 6, 0.25)
    fn = lambda t: 1.06 if any(b <= t < b + 0.35 - 1e-9 for b in beats) else 1.0
    v, sc = _pulse_video(wd, fn, 3.0)
    on = [i for i in range(len(sc)) if sc[i] > 1.03]
    runs = np.split(np.array(on), np.flatnonzero(np.diff(on) > 1) + 1)
    lens = [len(r) / 30 for r in runs]
    talk = [0.0, 2.6, 5.2, 7.8]
    return [check("hit lasts 0.35 s (±1 frame)", all(abs(l - 0.35) <= 1 / 30 + 1e-6 for l in lens[:5]), lens[:5], 0.35),
            check("hit scale 1.06", abs(max(sc) - 1.06) < 0.012, max(sc), 1.06),
            check("talking-reel plan keeps >= 2.5 s between cuts", min(np.diff(talk)) >= 2.5, min(np.diff(talk)), ">= 2.5"),
            check("negative control: between hits the scale is 1.0", abs(sc[int(0.65 * 30)] - 1.0) < 0.012, sc[int(0.65 * 30)], 1.0)], [v]


@card("BEAT-209")
def beat_grid_diamonds(task, wd):
    """Grid of 12×8 diamonds whose scale/colour follow the beat index (cycling), rendered and measured per beat."""
    from PIL import Image, ImageDraw
    bpm, fps, size = 120, 30, (192, 128)
    n = 90

    def frame(i):
        k = int(i / fps * bpm / 60)
        im = Image.new("RGB", size, (0, 0, 0))
        d = ImageDraw.Draw(im)
        for gx in range(12):
            for gy in range(8):
                cx, cy = 8 + gx * 16, 8 + gy * 16
                r = 6 if (gx + gy + k) % 4 == 0 else 3
                d.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill=PAL[k % 4])
        return np.asarray(im)
    v = write_video(Path(wd) / "diamonds.mp4", frame, n, fps, size)
    found, _ = cut_frames(v, (48, 32), thr=4.0)
    return [check("the grid changes exactly on each beat frame", found == [15, 30, 45, 60, 75], found, [15, 30, 45, 60, 75]),
            check("negative control: no change mid-beat", 7 not in found and 22 not in found, found, "no 7/22")], [v]


@card("BEAT-187")
def beat_bar_chart(task, wd):
    """128 BPM beat times (0.469 s): a bar spikes on each beat with 100 ms attack and 300 ms decay; the chart is the music."""
    bpm = 128
    beats = grid(bpm, 6, 0.2)
    def h(t):
        v = 0.0
        for b in beats:
            d = t - b
            if 0 <= d < 0.1:
                v = max(v, d / 0.1)
            elif 0.1 <= d < 0.4:
                v = max(v, 1 - (d - 0.1) / 0.3)
        return v
    v, sc = _pulse_video(wd, lambda t: 0.4 + 0.6 * h(t), 3.0, fps=60)
    pk = [int(np.argmax(sc[int(b * 60):int(b * 60) + 20])) / 60 + int(b * 60) / 60 - b for b in beats[:5]]
    return [check("beat interval 0.469 s", abs(60 / bpm - 0.46875) < 1e-9, 60 / bpm, 0.469),
            check("spike peaks 100 ms after each beat (±1 frame @60)", all(abs(p - 0.1) <= 1 / 60 + 1e-6 for p in pk), pk, 0.1),
            check("back to rest 400 ms after the beat", all(sc[int(round((b + 0.42) * 60))] < 0.45 for b in beats[:4]), 0, "< 0.45"),
            check("negative control: a frame before the beat is at rest", all(sc[int(b * 60) - 2] < 0.45 for b in beats[1:5]), 0, "< 0.45")], [v]


@card("BEAT-146")
def downbeat_halo(task, wd):
    """Halo dips on every downbeat: opacity 1 → .7 in 0.5 s (expo.out) then back in 0.6 s (sine.inOut); downbeats measured from the track."""
    x, ta = drum_loop(120, 6.0)
    p = save(wd, "track.wav", x)
    down = qa_beats(p)["downbeats"]
    def op(t):
        for d in down:
            u = t - d
            if 0 <= u < 0.5:
                return 1 - 0.3 * (1 - 2 ** (-10 * u / 0.5))
            if 0.5 <= u < 1.1:
                return 0.7 + 0.3 * (0.5 - 0.5 * math.cos(math.pi * (u - 0.5) / 0.6))
        return 1.0
    v = write_video(Path(wd) / "halo.mp4", lambda i: solid((64, 36), [int(255 * op(i / 30))] * 3), 180, 30, (64, 36), audio=p)
    lum = fx.frames(v, (16, 9)).mean(axis=(1, 2, 3)) / 255
    lows = [float(lum[int(round((d + 0.5) * 30))]) for d in down if d + 1.2 < 6]
    return [check("downbeats measured every 4 beats (2 s)", len(down) >= 2 and abs(down[1] - down[0] - 2.0) < 0.06, down, "2 s apart"),
            check("halo at ≈0.7 half a second after each downbeat", all(abs(l - 0.7) < 0.04 for l in lows), lows, 0.7),
            check("recovered to 1 by 1.1 s", all(lum[int(round((d + 1.15) * 30))] > 0.96 for d in down if d + 1.2 < 6), 0, "> 0.96"),
            check("negative control: between dips the halo is full", lum[int(round((down[0] + 1.5) * 30))] > 0.96, float(lum[int(round((down[0] + 1.5) * 30))]), "> 0.96")], [v]


@card("BEAT-222")
def sonic_logo_pulses(task, wd):
    """MG-028: the symbol pulses three times on the sound logo's hits (found by ffmpeg silencedetect), settles, holds; 3 s."""
    hits = [0.2, 0.6, 1.0]
    x = np.zeros(int(3 * SR))
    for h in hits:
        i = int(h * SR)
        x[i:i + int(0.12 * SR)] += 0.7 * np.sin(2 * np.pi * 660 * tt(0.12)) * np.exp(-tt(0.12) * 25)
    p = save(wd, "logo.wav", x)
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(p), "-af", "silencedetect=n=-40dB:d=0.05", "-f", "null", "-"], capture_output=True, text=True).stderr
    found = [0.0] + [float(v) for v in re.findall(r"silence_end: ([\d.]+)", err)]
    found = [f for f in found if any(abs(f - h) < 0.03 for h in hits)]
    hf_ = [round(h * 30) / 30 for h in found]
    fn = lambda t: 1 + 0.08 * max([math.exp(-(t - h) / 0.08) for h in hf_ if h <= t + 1e-6] or [0]) if t < 1.8 else 1.0
    v, sc = _pulse_video(wd, fn, 3.0)
    pk = [sc[int(round(h * 30))] for h in hf_]
    return [check("three hits found in the audio", len(found) == 3, found, hits),
            check("symbol pulses on each hit (scale ≈1.08)", all(abs(s - 1.08) < 0.015 for s in pk), [round(s, 3) for s in pk], 1.08),
            check("returns to true proportions in the hold (1.8-3 s)", all(abs(s - 1) < 0.012 for s in sc[57:]), float(max(abs(sc[57:] - 1))), "< 0.012"),
            check("negative control: no pulse between hits", sc[int(0.5 * 30)] < 1.03, float(sc[int(0.5 * 30)]), "< 1.03")], [v]


def _ballistic(beat_t, plat, g):
    """Solve vy = (dy + 0.5·g·T²)/T per hop so the arc from platform i-1 lands exactly at beat[i] (g < 0)."""
    hops = []
    for i in range(1, len(beat_t)):
        T = beat_t[i] - beat_t[i - 1]
        (x0, y0), (x1, y1) = plat[i - 1], plat[i]
        hops.append({"t0": beat_t[i - 1], "T": T, "vx": (x1 - x0) / T, "vy": ((y1 - y0) - 0.5 * g * T * T) / T, "p0": (x0, y0)})
    return hops


def _sim(hops, g, t):
    for h in hops:
        if h["t0"] <= t <= h["t0"] + h["T"] + 1e-9:
            u = t - h["t0"]
            return h["p0"][0] + h["vx"] * u, h["p0"][1] + h["vy"] * u + 0.5 * g * u * u
    return None


@card("BEAT-189")
def beat_bounce_path(task, wd):
    """Platform i placed so the ballistic arc from i-1 lands exactly on beat[i]; vy = (dy + 0.5·g·t²)/t, g ≈ -20 u/s²."""
    g = -20.0
    beats = grid(120, 6, 0.0)
    plat = [(i * 2.0, [0, 1, 0.5, 1.5, 0.2, 1.0][i]) for i in range(6)]
    hops = _ballistic(beats, plat, g)
    fps, size = 60, (160, 90)
    def frame(i):
        t = i / fps
        a = np.zeros((size[1], size[0], 3), np.uint8)
        p = _sim(hops, g, t)
        if p:
            px, py = int(10 + p[0] * 13), int(80 - p[1] * 20)
            a[max(0, py - 2):py + 2, max(0, px - 2):px + 2] = 255
        return a
    v = write_video(Path(wd) / "bounce.mp4", frame, int(beats[-1] * fps), fps, size)
    land = [_sim(hops, g, b - 1e-9) for b in beats[1:]]
    err = max(math.hypot(l[0] - p[0], l[1] - p[1]) for l, p in zip(land, plat[1:]))
    fr = fx.frames(v, size)
    def pos(f):
        m = fr[f].mean(axis=2) > 128
        ys, xs = np.nonzero(m)
        return (xs.mean(), ys.mean()) if len(xs) else None
    pix = max(abs(pos(int(b * fps) - 1)[0] - (10 + p[0] * 13)) for b, p in zip(beats[1:], plat[1:]))
    naive = _ballistic(beats, plat, 0.0)
    nl = [_sim(naive, g, b - 1e-9) for b in beats[1:]]
    nerr = max(math.hypot(l[0] - p[0], l[1] - p[1]) for l, p in zip(nl, plat[1:]))
    jdump(Path(wd) / "hops.json", hops)
    return [check("every hop lands on its platform at its beat (error < 1e-6 u)", err < 1e-6, err, 0),
            check("rendered ball at the platform x on the beat frame (±2 px)", pix <= 2.5, pix, "<= 2"),
            check("negative control: launching without gravity in the solve misses", nerr > 0.1, nerr, "> 0.1")], [v, Path(wd) / "hops.json"]


@card("BEAT-192")
def inverse_ballistic_notes(task, wd):
    """For each note time t: v = (dx/T, (dy - 0.5·g·T²)/T), fire at t - T, so the parabola hits the key exactly at t (g = 1500 px/s², T 0.6-1.2)."""
    g = 1500.0
    notes = [(1.2, 300), (1.7, 420), (2.3, 180), (2.9, 520)]
    launcher = (60.0, 300.0)
    shots = []
    for i, (t, kx) in enumerate(notes):
        T = 0.6 + 0.2 * (i % 4)
        dx, dy = kx - launcher[0], 80.0 - launcher[1]
        shots.append({"fire": t - T, "T": T, "vx": dx / T, "vy": (dy - 0.5 * g * T * T) / T, "key": kx, "t": t})
    hit = []
    for s in shots:
        T = s["T"]
        hit.append((launcher[0] + s["vx"] * T, launcher[1] + s["vy"] * T + 0.5 * g * T * T))
    x = np.zeros(int(3.5 * SR))
    for s in shots:
        i = int(s["t"] * SR)
        x[i:i + int(0.2 * SR)] += 0.5 * np.sin(2 * np.pi * (200 + s["key"]) * tt(0.2)) * np.exp(-tt(0.2) * 15)
    p = save(wd, "notes.wav", x)
    jdump(Path(wd) / "shots.json", shots)
    on = onsets(x, SR, 0.3, 0.2)
    return [check("every projectile reaches its key at y=80 exactly at the note time", max(abs(h[0] - s["key"]) + abs(h[1] - 80) for h, s in zip(hit, shots)) < 1e-6, hit, [s["key"] for s in shots]),
            check("fired T before the note, T in 0.6-1.2 s", all(0.6 - 1e-9 <= s["T"] <= 1.2 + 1e-9 and abs(s["fire"] + s["T"] - s["t"]) < 1e-9 for s in shots), [s["fire"] for s in shots], "t - T"),
            check("note sounds land on the hit times (±5 ms)", beat_err(on, [s["t"] for s in shots]) <= 0.005, on, [s["t"] for s in shots]),
            check("negative control: ignoring gravity misses the key", abs(launcher[1] + ((80 - launcher[1]) / shots[0]["T"]) * shots[0]["T"] + 0.5 * g * shots[0]["T"] ** 2 - 80) > 50, 0, "> 50 px")], [p, Path(wd) / "shots.json"]


@card("BEAT-193")
def bounce_sonification(task, wd):
    """Collision times from a deterministic bounce sim; each schedules the next pentatonic note (attack 5 ms, decay 300 ms), rendered offline."""
    g, y, vy, dt, e = -9.8, 1.0, 0.0, 1 / 1000, 0.8
    hits, t = [], 0.0
    while t < 3.0:
        vy += g * dt
        y += vy * dt
        t += dt
        if y <= 0:
            y, vy = 0.0, -vy * e
            hits.append(round(t, 3))
    penta = [0, 2, 4, 7, 9]
    x = np.zeros(int(3.6 * SR))
    freqs = []
    for k, h in enumerate(hits[:8]):
        f = 440 * 2 ** ((penta[k % 5] + 12 * (k // 5)) / 12)
        freqs.append(f)
        n = int(0.35 * SR)
        tn = np.arange(n) / SR
        env = np.minimum(1, tn / 0.005) * np.exp(-tn / 0.3 * 3)
        i = int(h * SR)
        x[i:i + n] += 0.4 * np.sin(2 * np.pi * f * tn) * env
    p = save(wd, "bounces.wav", x)
    jdump(Path(wd) / "collisions.json", hits)
    got = [peak_hz(x[int((h + 0.01) * SR):int((h + 0.09) * SR)]) for h in hits[:6]]
    semis = [round(12 * math.log2(f / 440)) % 12 for f in got]
    on = rises_at(x, SR, hits[:6])
    return [check("notes start at the collision times (rise >= 10 dB)", min(on) >= 10, on, ">= 10"),
            check("notes walk the pentatonic scale", semis == [penta[k % 5] for k in range(6)], semis, [penta[k % 5] for k in range(6)]),
            check("collision gaps shrink (restitution 0.8)", all(b < a for a, b in zip(np.diff(hits[:6]), np.diff(hits[:6])[1:])), list(np.diff(hits[:6])), "shrinking"),
            check("negative control: no note between collisions", max(rises_at(x, SR, [(a + b) / 2 for a, b in zip(hits[1:6], hits[2:7])])) < 3, 0, "< 3 dB")], [p]


def _bars_render(wd, values, n_bars, fps=30, size=(200, 80), name="bars.mp4", gap=1):
    """Bars of height ∝ values[frame][k]; heights measured back from the frames."""
    w, h = size
    bw = w // n_bars

    def frame(i):
        a = np.zeros((h, w, 3), np.uint8)
        for k in range(n_bars):
            hh = int(round(values[i][k] * (h - 4)))
            if hh > 0:
                a[h - hh:, k * bw:(k + 1) * bw - gap] = (255, 110, 90)
        return a
    v = write_video(Path(wd) / name, frame, len(values), fps, size)
    fr = fx.frames(v, size)
    meas = np.array([[((fr[i][:, k * bw + bw // 2 - (1 if bw > 2 else 0)].mean(axis=1)) > 100).sum() / (h - 4) for k in range(n_bars)] for i in range(len(values))])
    return v, meas


def _frame_rms(x, sr, fps):
    hop = sr // fps
    return np.array([rms(x[i * hop:(i + 1) * hop]) for i in range(len(x) // hop)])


def _wave_bars_card(wd, n_bars, doc_name):
    t = tt(3.0)
    x = 0.6 * np.sin(2 * np.pi * 220 * t) * (0.15 + 0.85 * np.abs(np.sin(2 * np.pi * 0.7 * t)))
    p = save(wd, "voice.wav", x)
    r = _frame_rms(x, SR, 30)
    r = r / r.max()
    vals = [[float(r[max(0, min(len(r) - 1, i - n_bars // 2 + k))]) for k in range(n_bars)] for i in range(len(r))]
    v, meas = _bars_render(wd, vals, n_bars, size=(n_bars * 3, 60), gap=1)
    mid = meas[:, n_bars // 2]
    c = float(np.corrcoef(mid, r[: len(mid)])[0, 1])
    y = 0.6 * np.sin(2 * np.pi * 220 * t)
    r0 = _frame_rms(y, SR, 30)
    r0 = r0 / r0.max()
    return [check("bar heights follow the per-frame RMS (r > 0.98)", c > 0.98, c, "> 0.98"),
            check("%d bars drawn" % n_bars, meas.shape[1] == n_bars and (meas[10] > 0).sum() >= n_bars - 2, int((meas[10] > 0).sum()), n_bars),
            check("negative control: an unmodulated tone gives bars that do not move (std < 0.01)", float(np.std(r0[1:-1])) < 0.01, float(np.std(r0[1:-1])), "< 0.01"),
            check("the modulated voice gives moving bars (std > 0.1)", float(np.std(mid)) > 0.1, float(np.std(mid)), "> 0.1")], [v]


for _cid, _n, _d in (("BEAT-194", 200, "Waveform word reveal: ~200 dense bars beneath a line, heights ∝ audio RMS per frame."),
                     ("BEAT-197", 70, "Waveform-flanked word: 60-80 bars driven by audio amplitude."),
                     ("BEAT-190", 60, "Outline-to-fill letters with a row of 60 thin bars animating to audio amplitude."),
                     ("BEAT-225", 24, "MG-096 amplitude-reactive bars around cover art: per-frame loudness values bound to scale (called loudness-reactive)."),
                     ("BEAT-203", 48, "Beat waveform bar strip: thin bars whose heights pulse with the level (every Nth accent).")):
    def _mkwb(cid=_cid, n=_n, d=_d):
        @card(cid)
        def _wb(task, wd):
            return _wave_bars_card(wd, n, cid)
        _wb.__doc__ = d
        return _wb
    _mkwb()


def band_frames(x, sr, fps=30, nfft=4096, bands=16, lo=40, hi=10000):
    """Per-frame FFT band energies (window 4096 centred on each frame, log-spaced bands, each band normalised over the track)."""
    hop = sr / fps
    n = int(len(x) / hop)
    w = np.hanning(nfft)
    edges = np.geomspace(lo, hi, bands + 1)
    f = np.fft.rfftfreq(nfft, 1 / sr)
    xp = np.pad(x, nfft)
    out = np.zeros((n, bands))
    rr = np.zeros(n)
    for i in range(n):
        c = int(i * hop + hop / 2) + nfft
        seg = xp[c - nfft // 2:c + nfft // 2]
        X = np.abs(np.fft.rfft(seg * w))
        out[i] = [X[(f >= edges[k]) & (f < edges[k + 1])].mean() if np.any((f >= edges[k]) & (f < edges[k + 1])) else 0 for k in range(bands)]
        rr[i] = rms(seg)
    out = out / (out.max(axis=0, keepdims=True) + 1e-12)
    return out, rr / (rr.max() + 1e-12), edges


def _band_fixture(secs=3.0):
    t = tt(secs)
    gate = lambda u: np.clip(np.minimum(u / 0.02, (0.3 - u) / 0.02), 0, 1) * (u < 0.3)
    bass = gate(np.mod(t, 1.0)) * 0.5 * np.sin(2 * np.pi * 60 * t)
    treb = gate(np.mod(t + 0.5, 1.0)) * 0.3 * np.sin(2 * np.pi * 6000 * t)
    return bass + treb


@card("BEAT-29")
def per_frame_fft_bands(task, wd):
    """ffmpeg decode → numpy: FFT 4096 centred on each frame, 16 log bands, per-band normalisation → {fps, totalFrames, frames[{rms, bands}]}."""
    x = _band_fixture()
    p = save(wd, "track.wav", x)
    y, sr = load_any(p, 44100)
    B, R, edges = band_frames(y, sr, 30, 4096, 16)
    out = jdump(Path(wd) / "audio-data.json", {"fps": 30, "totalFrames": len(B), "frames": [{"rms": float(R[i]), "bands": B[i].round(4).tolist()} for i in range(len(B))]})
    kb = int(np.searchsorted(edges, 60) - 1)
    kt = int(np.searchsorted(edges, 6000) - 1)
    on_b = B[int(0.15 * 30), kb]
    off_b = B[int(0.65 * 30), kb]
    on_t = B[int(0.65 * 30), kt]
    return [check("totalFrames = 3 s × 30", len(B) == 90, len(B), 90),
            check("bass band high during the 60 Hz bursts, low between", on_b > 0.8 and off_b < 0.1, [on_b, off_b], "high/low"),
            check("treble band peaks during the 6 kHz bursts", on_t > 0.8, on_t, "> 0.8"),
            check("negative control: the treble band is quiet during bass-only frames", B[int(0.15 * 30), kt] < 0.1, B[int(0.15 * 30), kt], "< 0.1")], [out]


@card("BEAT-80")
def extract_audio_data_script(task, wd):
    """audio-reactive-captions-studio extract_audio_data.py track --fps 30 --bands 16 --out audio-data.json (ffmpeg → PCM, Hann,
    geomspace 40-10000 Hz, spectral-flux beats, histogram BPM)."""
    x, ta = drum_loop(120, 6.0)
    p = save(wd, "track.wav", x)
    out = Path(wd) / "audio-data.json"
    sh([sys.executable, ARC / "extract_audio_data.py", p, "--fps", "30", "--bands", "16", "--out", out], cwd=wd)
    d = json.loads(out.read_text())
    frames = d.get("frames") or []
    bpm = d.get("bpm") or d.get("tempo")
    x2, _ = drum_loop(96, 6.0)
    p2 = save(wd, "track96.wav", x2)
    o2 = Path(wd) / "d96.json"
    sh([sys.executable, ARC / "extract_audio_data.py", p2, "--fps", "30", "--bands", "16", "--out", o2], cwd=wd)
    bpm2 = json.loads(o2.read_text()).get("bpm")
    nb = len(frames[0].get("bands", [])) if frames else 0
    return [check("one frame per 1/30 s (6 s → ~180)", abs(len(frames) - 180) <= 2, len(frames), 180),
            check("16 bands per frame", nb == 16, nb, 16),
            check("histogram BPM near 120 (±3)", bpm is not None and abs(float(bpm) - 120) <= 3, bpm, 120),
            check("negative control: a 96 BPM track does not read 120", bpm2 is not None and abs(float(bpm2) - 120) > 8, bpm2, "!= 120")], [out]


@card("BEAT-116")
def hf_extract_audio_data(task, wd):
    """HyperFrames media-use extract-audio-data.py <audio> → AUDIO_DATA {fps 30, totalFrames, frames[{bands}]}; bass→scale, treble→glow."""
    x = _band_fixture()
    p = save(wd, "track.wav", x)
    out = Path(wd) / "audio-data.json"
    script = hf_root() / "dist/skills/media-use/audio/scripts/extract-audio-data.py"
    sh([sys.executable, script, p, "-o", out], cwd=wd)
    d = json.loads(out.read_text())
    fr = d["frames"]
    bass = np.array([max(f["bands"][0], f["bands"][1]) for f in fr])
    treb = np.array([np.mean(f["bands"][12:15]) for f in fr])
    scale = 1 + 0.06 * bass
    glow = 12 * treb
    v, sc = _pulse_video(wd, lambda t: float(scale[min(len(scale) - 1, int(t * 30))]), 3.0)
    c = float(np.corrcoef(sc[: len(scale)], scale[: len(sc)])[0, 1])
    return [check("fps 30 and one frame per 1/30 s", d.get("fps") == 30 and abs(len(fr) - 90) <= 2, [d.get("fps"), len(fr)], [30, 90]),
            check("bass band follows the 60 Hz bursts", bass[int(0.15 * 30)] > bass[int(0.65 * 30)] + 0.4, [bass[int(0.15 * 30)], bass[int(0.65 * 30)]], "on > off"),
            check("treble bands follow the 6 kHz bursts", treb[int(0.65 * 30)] > treb[int(0.15 * 30)] + 0.3, [treb[int(0.65 * 30)], treb[int(0.15 * 30)]], "on > off"),
            check("rendered scale tracks bass (r > 0.95)", c > 0.95, c, "> 0.95"),
            check("negative control: bass band is low where only treble plays", bass[int(0.65 * 30)] < 0.3, bass[int(0.65 * 30)], "< 0.3")], [out, v]


def _reactive_card(wd, smooth=None, kscale=0.06, doc_bands=(0, 1)):
    x = _band_fixture()
    save(wd, "track.wav", x)
    B, R, edges = band_frames(x, SR, 30, 4096, 16)
    bass = B[:, list(doc_bands)].mean(axis=1)
    if smooth:
        s = np.zeros_like(bass)
        for i in range(len(bass)):
            s[i] = (s[i - 1] if i else bass[0]) * smooth + bass[i] * (1 - smooth)
        bass = s
    scale = 1 + kscale * bass
    v, sc = _pulse_video(wd, lambda t: float(scale[min(len(scale) - 1, int(round(t * 30)))]), 3.0)
    pk_on = float(np.mean([sc[int(round((k + 0.2) * 30))] for k in range(3)]))
    pk_off = float(np.mean([sc[int(round((k + 0.7) * 30))] for k in range(3)]))
    return v, sc, scale, pk_on, pk_off


for _cid, _sm, _k, _doc in (("BEAT-30", None, 0.04, "Audio-reactive UI accents: precomputed 16-band FFT per frame; logo scale ≤ 1+0.04·bass, sampled at f/fps."),
                            ("BEAT-36", None, 0.06, "Audio-reactive glow/scale: bands per frame to JSON; scale = 1+bass·0.06."),
                            ("BEAT-213", None, 0.06, "Bass drives scale pulses (text 3-6 %, shapes 10-30 %), mids shape, treble glow."),
                            ("BEAT-214", None, 0.06, "Audio-reactive captions baked at build time: peakBass → scale 1+peakBass·0.06."),
                            ("BEAT-264", 0.25, 0.06, "Mapping rules: bass drives big moves, smoothing prev·s + raw·(1−s) with s = 0.25, floor above zero."),
                            ("BEAT-38", 0.25, 0.08, "Spectrum bars/glows from pre-analysed bands, smoothed prev·s+raw·(1−s), bass drives scale."),
                            ("BEAT-136", None, 0.35 / 1.45, "Kick/bass mapping: orb y = 1.45 + .35·bass (as a relative scale of the orb) from measured bass.")):
    def _mkre(cid=_cid, sm=_sm, k=_k, doc=_doc):
        @card(cid)
        def _re(task, wd):
            v, sc, scale, on, off = _reactive_card(wd, sm, k)
            c = float(np.corrcoef(sc[: len(scale)], scale[: len(sc)])[0, 1])
            return [check("rendered size tracks the bass band (r > 0.95)", c > 0.95, c, "> 0.95"),
                    check("scale ≈ 1+%.3f on bass hits" % k, abs(on - (1 + k)) < 0.25 * k + 0.012, on, 1 + k),
                    check("negative control: between bass hits the scale stays near 1", off < 1 + 0.3 * k + 0.012, off, "< %.3f" % (1 + 0.3 * k))], [v]
        _re.__doc__ = doc
        return _re
    _mkre()


@card("BEAT-102")
def visualiser_bars(task, wd):
    """AnalyserNode-style fftSize 256 → 48 bars (80 % width), height 8 + v·22 % H; demo with synthetic sines: the tallest bar sits at the tone's bin."""
    sr = 48000
    t = tt(2.0, sr)
    x = np.where(t < 1.0, 0.5 * np.sin(2 * np.pi * 3000 * t), 0.5 * np.sin(2 * np.pi * 9000 * t))
    p = save(wd, "sines.wav", x, sr)
    fps, n = 30, 60
    vals = []
    for i in range(n):
        seg = x[int(i / fps * sr):int(i / fps * sr) + 256]
        X = np.abs(np.fft.rfft(seg * np.hanning(256)))[:128]
        X = X / (X.max() + 1e-9)
        idx = np.linspace(0, 128, 49).astype(int)
        vals.append([float(X[idx[k]:idx[k + 1]].max()) for k in range(48)])
    v, meas = _bars_render(wd, [[0.08 + 0.22 * 4 * vv for vv in row] for row in vals], 48, fps, (192, 100), gap=1)
    a = int(np.argmax(meas[10]))
    b = int(np.argmax(meas[45]))
    ea = int(3000 / (sr / 256) / (128 / 48))
    eb = int(9000 / (sr / 256) / (128 / 48))
    return [check("3 kHz → tallest bar at its bin group", abs(a - ea) <= 1, a, ea),
            check("9 kHz → tallest bar moves to its bin group", abs(b - eb) <= 1, b, eb),
            check("negative control: the two tones do not share a bar", a != b, [a, b], "differ")], [v, p]


@card("BEAT-233")
def ffmpeg_showwaves(task, wd):
    """Waveform/spectrum as a visual asset with ffmpeg showwaves / showspectrum."""
    t = tt(3.0)
    x = np.where(t < 1.5, 0.05, 0.6) * np.sin(2 * np.pi * 300 * t)
    p = save(wd, "pod.wav", x)
    v = Path(wd) / "waves.mp4"
    ff("-i", p, "-filter_complex", "[0:a]showwaves=s=160x90:mode=cline:rate=30:colors=white,format=yuv420p[v]", "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-c:a", "aac", v)
    s = Path(wd) / "spectrum.mp4"
    ff("-i", p, "-filter_complex", "[0:a]showspectrum=s=160x90:slide=scroll,format=yuv420p[v]", "-map", "[v]", "-c:v", "libx264", s)
    fr = fx.frames(v, (160, 90))
    lit = (fr.mean(axis=3) > 60).sum(axis=(1, 2))
    quiet, loud = float(lit[10:40].mean()), float(lit[55:85].mean())
    return [check("louder half draws a taller waveform (>= 3x lit pixels)", loud > 3 * quiet, [quiet, loud], "loud >> quiet"),
            check("spectrum video rendered", float(fx.probe(s)["format"]["duration"]) > 2.5, fx.probe(s)["format"]["duration"], "> 2.5 s"),
            check("negative control: the quiet half is not as tall", quiet < loud, quiet, "< loud")], [v, s]


@card("BEAT-208")
def equaliser_under_word(task, wd):
    """Row of 40-60 thin bars with heights from the audio FFT, under a headline (rendered; the bars follow the spectrum)."""
    x = _band_fixture()
    B, R, edges = band_frames(x, SR, 30, 4096, 48)
    v, meas = _bars_render(wd, B.tolist(), 48, 30, (192, 60), gap=1)
    kb = int(np.searchsorted(edges, 60) - 1)
    c = float(np.corrcoef(meas[:, kb], B[:, kb])[0, 1])
    return [check("bass bar height follows the measured band (r > 0.95)", c > 0.95, c, "> 0.95"),
            check("48 bars", meas.shape[1] == 48, meas.shape[1], 48),
            check("negative control: bass bar is low on treble-only frames", meas[int(0.65 * 30), kb] < 0.15, float(meas[int(0.65 * 30), kb]), "< 0.15")], [v]


# ───────────────────────── designed sound effects & audio editing ─────────────────────────
def am_rate(x, sr, lo=3, hi=30):
    """Dominant amplitude-modulation rate of a signal (Hz) from its envelope spectrum."""
    e = envelope(x, sr, 10)
    e = e - e.mean()
    d = sr // 200
    e = e[::d]
    E = np.abs(np.fft.rfft(e * np.hanning(len(e))))
    f = np.fft.rfftfreq(len(e), d / sr)
    m = (f >= lo) & (f <= hi)
    return float(f[m][int(np.argmax(E[m]))])


def _bp(x, lo, hi, sr=SR, order=4):
    from scipy.signal import butter, sosfilt
    return sosfilt(butter(order, [lo, hi], "band", fs=sr, output="sos"), x)


def _scratch(wd, lo, hi, rate, name, secs=2.0, grains=True, seed=2):
    rng = np.random.default_rng(seed)
    t = tt(secs)
    n = _bp(rng.standard_normal(len(t)), lo, hi)
    press = 0.55 + 0.45 * np.sin(2 * np.pi * rate * t)
    gate = ((t > 0.3) & (t < 1.6)).astype(float)
    gate = np.convolve(gate, np.ones(480) / 480, mode="same")
    y = n * press * gate
    if grains:
        for g in rng.uniform(0.35, 1.55, 25):
            i = int(g * SR)
            y[i:i + 48] += _bp(rng.standard_normal(480), lo, hi)[200:248] * 2.0
    y = 0.5 * y / np.abs(y).max()
    return save(wd, name, y), y


@card("BEAT-182")
def chalk_scratch(task, wd):
    """Band-pass noise 0.7-4.5 kHz modulated by 7-11 Hz pressure pulses, plus grain crackles; gated while the chalk draws."""
    p, y = _scratch(wd, 700, 4500, 9.0, "chalk.wav")
    inband = band_db(y, SR, 700, 4500) - band_db(y, SR, 6000, 20000)
    r = am_rate(y[int(0.35 * SR):int(1.55 * SR)], SR)
    off = seg_db(y, SR, 1.75, 1.95)
    return [check("energy inside 0.7-4.5 kHz (>= 15 dB over 6-20 kHz)", inband >= 15, inband, ">= 15"),
            check("pressure pulses at 7-11 Hz", 7 <= r <= 11, r, "7-11"),
            check("silent when the stroke ends (gate)", off < -80, off, "< -80"),
            check("negative control: white noise is not band-limited", band_db(np.random.default_rng(1).standard_normal(SR), SR, 700, 4500) - band_db(np.random.default_rng(1).standard_normal(SR), SR, 6000, 20000) < 5, 0, "< 5")], [p]


@card("BEAT-212")
def marker_squeak(task, wd):
    """Filtered noise 1.8-7 kHz, AM by 9-14 Hz pulses with short squeaks; a click per word; a cap snap at the end."""
    p, y = _scratch(wd, 1800, 7000, 12.0, "marker_bed.wav", grains=False)
    for w in (0.4, 0.9, 1.4):
        i = int(w * SR)
        y[i:i + int(0.01 * SR)] += 0.6 * np.sin(2 * np.pi * 2500 * tt(0.01)) * np.exp(-tt(0.01) * 300)
    i = int(1.8 * SR)
    y[i:i + int(0.02 * SR)] += 0.9 * _bp(np.random.default_rng(7).standard_normal(int(0.02 * SR)), 1000, 6000)
    out = save(wd, "marker.wav", y)
    r = am_rate(y[int(0.35 * SR):int(1.55 * SR)], SR)
    inband = band_db(y[: int(1.7 * SR)], SR, 1800, 7000) - band_db(y[: int(1.7 * SR)], SR, 100, 1000)
    snap = rises_at(y, SR, [1.8])[0]
    return [check("1.8-7 kHz band dominates (>= 15 dB over 100-1000 Hz)", inband >= 15, inband, ">= 15"),
            check("squeak AM at 9-14 Hz", 9 <= r <= 14, r, "9-14"),
            check("cap snap at the end", snap > 20, snap, "> 20 dB"),
            check("negative control: before the stroke it is silent", seg_db(y, SR, 0.05, 0.25) < -80, seg_db(y, SR, 0.05, 0.25), "< -80")], [out]


def _dur_of(x, sr, rel_db=-40):
    e = envelope(x, sr, 2)
    on = np.flatnonzero(e > e.max() * 10 ** (rel_db / 20))
    return (on[-1] - on[0]) / sr if len(on) else 0.0


@card("BEAT-216")
def ui_sound_lengths(task, wd):
    """UI sounds by role: confirm 50-200 ms, success rising 100-300 ms, error low buzz 100-200 ms, notification chime 200-500 ms,
    typing click 20-50 ms, delete whoosh 200-400 ms — synthesised and measured."""
    rng = np.random.default_rng(4)
    def env(d, tau):
        t = tt(d)
        return t, np.minimum(1, t / 0.003) * np.exp(-t / tau) * np.minimum(1, (d - t) / 0.004)
    t, e = env(0.12, 0.04); confirm = np.sin(2 * np.pi * 1200 * t) * e
    t, e = env(0.22, 0.08); success = np.sin(2 * np.pi * np.cumsum(600 + 900 * t / 0.22) / SR) * e
    t, e = env(0.15, 0.06); error = np.sign(np.sin(2 * np.pi * 140 * t)) * e * 0.5
    t, e = env(0.4, 0.12); chime = (np.sin(2 * np.pi * 1320 * t) + 0.5 * np.sin(2 * np.pi * 1980 * t)) * e
    t, e = env(0.035, 0.008); typing = _bp(rng.standard_normal(len(t)), 1500, 6000) * e
    t, e = env(0.3, 0.12); delete = _bp(rng.standard_normal(len(t)), 400, 4000) * np.sin(np.pi * t / 0.3)
    kit = {"confirm": (confirm, 0.05, 0.2), "success": (success, 0.1, 0.3), "error": (error, 0.1, 0.2), "notification": (chime, 0.2, 0.5),
           "typing": (typing, 0.02, 0.05), "delete": (delete, 0.2, 0.4)}
    outs, got = [], {}
    for k, (x, lo, hi) in kit.items():
        outs.append(save(wd, "ui_%s.wav" % k, 0.6 * x / np.abs(x).max()))
        got[k] = len(x) / SR
    up = peak_hz(success[-int(0.05 * SR):]) - peak_hz(success[: int(0.05 * SR)])
    return [check("each sound inside its role's duration range", all(kit[k][1] <= got[k] <= kit[k][2] for k in kit), got, {k: [v[1], v[2]] for k, v in kit.items()}),
            check("success pitch rises", up > 300, up, "> 300 Hz"),
            check("error is a low buzz (fundamental < 200 Hz)", peak_hz(error) < 200, peak_hz(error), "< 200"),
            check("negative control: an unenveloped 600 ms chime measures outside the notification range", not (0.2 <= _dur_of(np.sin(2 * np.pi * 1320 * tt(0.6)), SR) <= 0.5), _dur_of(np.sin(2 * np.pi * 1320 * tt(0.6)), SR), "> 0.5")], outs


@card("BEAT-43")
def confirm_beep(task, wd):
    """beep(freq=880, dur=.12): sine, gain .15 at start, exponential ramp to .001 at t+dur; variants 740/100 ms and 960/150 ms."""
    outs, res = [], []
    for f, d in ((880, 0.12), (740, 0.10), (960, 0.15)):
        t = tt(d)
        g = 0.15 * (0.001 / 0.15) ** (t / d)
        x = np.sin(2 * np.pi * f * t) * g
        outs.append(save(wd, "beep_%d.wav" % f, x))
        res.append((peak_hz(x), len(x) / SR, float(abs(x[: 50]).max()), float(abs(x[-50:]).max())))
    return [check("frequencies 880/740/960 Hz", all(abs(r[0] - f) < 12 for r, f in zip(res, (880, 740, 960))), [r[0] for r in res], [880, 740, 960]),
            check("durations 120/100/150 ms", all(abs(r[1] - d) < 1e-3 for r, d in zip(res, (0.12, 0.1, 0.15))), [r[1] for r in res], [0.12, 0.1, 0.15]),
            check("starts at gain .15, ends near .001", all(r[2] <= 0.151 and r[3] < 0.002 for r in res), [(r[2], r[3]) for r in res], [0.15, 0.001]),
            check("negative control: a flat-gain tone does not decay to .001", float(abs(0.15 * np.sin(2 * np.pi * 880 * tt(0.12))[-200:]).max()) > 0.01, 0.15, "> .01")], outs


def _events_audio(wd, events, secs, voice, name):
    x = np.zeros(int(secs * SR))
    for t in events:
        s = voice(t)
        i = int(t * SR)
        x[i:i + len(s)] += s[: len(x) - i]
    return save(wd, name, x), x


@card("BEAT-284")
def webaudio_sfx_frame_clock(task, wd):
    """Oscillator + gain envelope (attack 5 ms, decay 120 ms) scheduled at frame times of the animation clock (30 fps)."""
    frames = [12, 27, 45, 61, 80]
    times = [f / 30 for f in frames]
    def boing(t):
        n = int(0.2 * SR)
        u = np.arange(n) / SR
        return 0.5 * np.sin(2 * np.pi * np.cumsum(500 - 300 * u / 0.2) / SR) * np.minimum(1, u / 0.005) * np.exp(-u / 0.12)
    p, x = _events_audio(wd, times, 3.0, boing, "sfx.wav")
    on = rises_at(x, SR, times)
    off = rises_at(x, SR, [t - 0.1 for t in times])
    att = np.argmax(np.abs(boing(0)[:int(0.02 * SR)])) / SR
    return [check("each sound starts on its frame time (rise >= 20 dB)", min(on) >= 20, on, ">= 20"),
            check("5 ms attack", 0.003 <= att <= 0.008, att, 0.005),
            check("negative control: 100 ms before each event nothing starts", max(off) < 3, off, "< 3")], [p]


@card("BEAT-294")
def ui_event_tones(task, wd):
    """Tones per UI event with pitch from the element's y; 48 kHz; normalised to -14 LUFS."""
    events = [(0.3, 100), (0.8, 400), (1.3, 250), (1.8, 50)]
    def f_of(y):
        return 1200 - 2 * y
    x = np.zeros(int(2.6 * SR))
    for t, y in events:
        n = int(0.25 * SR)
        u = np.arange(n) / SR
        i = int(t * SR)
        x[i:i + n] += 0.3 * np.sin(2 * np.pi * f_of(y) * u) * np.exp(-u / 0.08)
    raw = save(wd, "tones_raw.wav", x)
    out = Path(wd) / "tones.wav"
    loudnorm2(raw, out, -14, -1, 11)
    y, sr = load_any(out)
    got = [peak_hz(y[int((t + 0.01) * sr):int((t + 0.2) * sr)], sr) for t, _ in events]
    return [check("pitch follows y (1200 - 2y Hz)", all(abs(g - f_of(yy)) < 8 for g, (_, yy) in zip(got, events)), got, [f_of(yy) for _, yy in events]),
            check("normalised to -14 LUFS", abs(ebur(out)["I"] + 14) <= 1.0, ebur(out)["I"], -14),
            check("48 kHz", fx.probe(out)["streams"][0]["sample_rate"] == "48000", fx.probe(out)["streams"][0]["sample_rate"], "48000"),
            check("negative control: raw tones are not at -14", abs(ebur(raw)["I"] + 14) > 3, ebur(raw)["I"], "!= -14")], [out]


@card("BEAT-285")
def one_sfx_per_element(task, wd):
    """Each appearing element gets one soft tick; otherwise silence, no music bed."""
    entrances = [0.4, 1.1, 1.7, 2.3]
    tick = lambda t: 0.25 * np.sin(2 * np.pi * 2400 * tt(0.03)) * np.exp(-tt(0.03) * 150)
    p, x = _events_audio(wd, entrances, 3.0, tick, "ticks.wav")
    on = onsets(x, SR, 0.3, 0.1)
    gaps = [seg_db(x, SR, a + 0.1, b - 0.05) for a, b in zip(entrances, entrances[1:])]
    return [check("exactly one tick per entrance, on time (±5 ms, envelope window)", len(on) == len(entrances) and beat_err(on, entrances) <= 0.005, on, entrances),
            check("silence between ticks (no bed)", max(gaps) < -90, max(gaps), "< -90"),
            check("soft (peak <= -10 dBFS)", peak_db(x) <= -10, peak_db(x), "<= -10"),
            check("negative control: a bed would raise the gaps", seg_db(x + bed(3.0), SR, 0.55, 1.0) > -40, seg_db(x + bed(3.0), SR, 0.55, 1.0), "> -40")], [p]


@card("BEAT-232")
def typing_under_reveal(task, wd):
    """A soft keyboard-typing SFX laid across the exact reveal span of a typewriter caption (start/end from the timeline)."""
    start, end, chars = 0.6, 2.6, 24
    rng = np.random.default_rng(9)
    x = np.zeros(int(3.2 * SR))
    times = [start + k * (end - start) / chars for k in range(chars)]
    for t in times:
        n = int(0.025 * SR)
        i = int(t * SR)
        x[i:i + n] += 0.3 * _bp(rng.standard_normal(n), 1500, 5000) * np.exp(-np.arange(n) / SR / 0.006)
    p = save(wd, "typing.wav", x)
    e = envelope(x, SR, 5)
    act = np.flatnonzero(e > e.max() * 0.05) / SR
    return [check("typing starts at the reveal start (±10 ms)", abs(act[0] - start) < 0.01, act[0], start),
            check("typing ends with the reveal (last key within 120 ms of the end)", end - 0.12 <= act[-1] <= end + 0.03, act[-1], end),
            check("one key per revealed character", len(onsets(x, SR, 0.2, 0.05)) == chars, len(onsets(x, SR, 0.2, 0.05)), chars),
            check("negative control: silent outside the span", seg_db(x, SR, 0.0, 0.55) < -90 and seg_db(x, SR, 2.75, 3.1) < -90, seg_db(x, SR, 0.0, 0.55), "< -90")], [p]


def _riser_impact(wd, cut, lead):
    rng = np.random.default_rng(6)
    secs = cut + 1.5
    x = np.zeros(int(secs * SR))
    n = int(lead * SR)
    u = np.arange(n) / n
    r = _bp(rng.standard_normal(n), 300, 6000) * u ** 2
    i0 = int((cut - lead) * SR)
    x[i0:i0 + n] += 0.4 * r / np.abs(r).max()
    m = int(0.8 * SR)
    v = np.arange(m) / SR
    imp = np.sin(2 * np.pi * np.cumsum(40 + 80 * np.exp(-v / 0.05)) / SR) * np.exp(-v / 0.25)
    i1 = int(cut * SR)
    x[i1:i1 + m] += 0.8 * imp
    p = save(wd, "transition.wav", x)
    vid = cut_video(Path(wd) / "transition.mp4", [cut], secs, 30, audio=p)
    return p, x, vid


def _ri_checks(x, cut, lead, vid):
    e = envelope(x, SR, 5)
    riser_start = np.flatnonzero(np.abs(x) > 1e-7)[0] / SR
    found, _ = cut_frames(vid)
    hit = rises_at(x, SR, [cut], pre=0.02, post=0.02)[0]
    pk = (int(cut * SR) + np.argmax(np.abs(x[int(cut * SR):int((cut + 0.1) * SR)]))) / SR
    return [check("riser starts %.2f s before the cut (±20 ms)" % lead, abs((cut - riser_start) - lead) < 0.02, cut - riser_start, lead),
            check("impact transient on the cut frame (peak within 1 frame)", 0 <= pk - cut <= 1 / 30, pk - cut, "0..1 frame"),
            check("picture cut where the impact lands", found == [int(round(cut * 30))], found, [int(round(cut * 30))]),
            check("impact steps the level up at the cut (>= 3 dB)", hit >= 3, hit, ">= 3"),
            check("negative control: nothing sounds before the riser", seg_db(x, SR, 0, max(0.05, cut - lead - 0.1)) < -90, seg_db(x, SR, 0, max(0.05, cut - lead - 0.1)), "< -90")]


for _cid, _lead, _doc in (("BEAT-251", 0.4, "Riser/whoosh 0.3-0.5 s before the cut to build anticipation."),
                          ("BEAT-252", 0.4, "Impact/sub-drop exactly at the cut frame (align the hit, not the file start)."),
                          ("BEAT-255", 0.35, "Riser 0.3-0.5 s before the cut, impact on the cut frame (synthesised SFX).")):
    def _mkri(cid=_cid, lead=_lead, doc=_doc):
        @card(cid)
        def _ri(task, wd):
            p, x, v = _riser_impact(wd, 1.5, lead)
            return _ri_checks(x, 1.5, lead, v), [p, v]
        _ri.__doc__ = doc
        return _ri
    _mkri()


@card("BEAT-240")
def zero_latency_transient(task, wd):
    """An effect starting 30 ms late feels laggy: trim leading silence (ffmpeg silenceremove) so the transient is at t=0."""
    x = np.concatenate([np.zeros(int(0.03 * SR)), 0.7 * np.sin(2 * np.pi * 800 * tt(0.2)) * np.exp(-tt(0.2) * 20)])
    src = save(wd, "late.wav", x)
    out = Path(wd) / "tight.wav"
    ff("-i", src, "-af", "silenceremove=start_periods=1:start_threshold=-60dB:start_silence=0", out)
    y, _ = load_any(out)
    first = np.flatnonzero(np.abs(y) > 0.01)[0] / SR
    first_in = np.flatnonzero(np.abs(x) > 0.01)[0] / SR
    return [check("transient within 2 ms of the file start", first <= 0.002, first, "<= 0.002"),
            check("negative control: the source starts 30 ms late", first_in >= 0.029, first_in, ">= 0.03")], [out]


@card("BEAT-236")
def sfx_three_layers(task, wd):
    """Hit = transient (0-20 ms, material) + body (20-300 ms, meaning) + tail (100 ms-2 s, space); transient on the contact frame,
    envelope ends at zero with a short fade."""
    rng = np.random.default_rng(8)
    n = int(1.2 * SR)
    u = np.arange(n) / SR
    tr = _bp(rng.standard_normal(n), 2000, 12000) * (u < 0.02) * np.exp(-u / 0.004)
    body = np.sin(2 * np.pi * np.cumsum(180 - 80 * np.minimum(u, 0.3) / 0.3) / SR) * ((u >= 0.0) & (u < 0.3)) * np.exp(-u / 0.12)
    tail = _bp(rng.standard_normal(n), 200, 3000) * (u >= 0.1) * np.exp(-(u - 0.1) / 0.35) * 0.15
    y = tr + 0.8 * body + tail
    f = int(0.012 * SR)
    y[-f:] *= np.linspace(1, 0, f)
    contact = 0.5
    x = np.concatenate([np.zeros(int(contact * SR)), y])
    p = save(wd, "hit.wav", 0.8 * x / np.abs(x).max())
    a = lambda s, a0, a1: seg_db(s, SR, contact + a0, contact + a1)
    hf_tr = band_db(x[int(contact * SR):int((contact + 0.02) * SR)], SR, 4000, 12000) - band_db(x[int((contact + 0.2) * SR):int((contact + 0.3) * SR)], SR, 4000, 12000)
    return [check("transient layer: 4-12 kHz in 0-20 ms >= 10 dB above 200-300 ms", hf_tr >= 10, hf_tr, ">= 10 dB"),
            check("body carries 20-300 ms (louder than the tail at 0.15-0.3 s)", seg_db(0.8 * body, SR, 0.15, 0.3) > seg_db(tail, SR, 0.15, 0.3), [seg_db(0.8 * body, SR, 0.15, 0.3), seg_db(tail, SR, 0.15, 0.3)], "body > tail"),
            check("tail present at 0.6-1.0 s", a(x, 0.6, 1.0) > -60, a(x, 0.6, 1.0), "> -60"),
            check("transient on the contact frame (±2 ms)", abs(np.flatnonzero(np.abs(x) > 0.02)[0] / SR - contact) < 0.002, np.flatnonzero(np.abs(x) > 0.02)[0] / SR, contact),
            check("ends at zero", abs(x[-1]) < 1e-6, float(abs(x[-1])), 0),
            check("negative control: the body alone has no bright transient", band_db(body[:int(0.02 * SR)], SR, 2000, 12000) - band_db(body[:int(0.02 * SR)], SR, 50, 400) < -20,
                  band_db(body[:int(0.02 * SR)], SR, 2000, 12000) - band_db(body[:int(0.02 * SR)], SR, 50, 400), "< -20")], [p]


@card("BEAT-238")
def phone_speaker_audibility(task, wd):
    """Below ~300 Hz phones play almost nothing: layer a click/knock above any thud; check through a phone-speaker band sim (HPF 300)."""
    n = int(0.4 * SR)
    u = np.arange(n) / SR
    thud = np.sin(2 * np.pi * 60 * u) * np.exp(-u / 0.1)
    knock = _bp(np.random.default_rng(2).standard_normal(n), 1000, 4000) * np.exp(-u / 0.015) * 0.5
    layered = thud + knock
    p1, p2 = save(wd, "thud.wav", 0.7 * thud), save(wd, "thud_knock.wav", 0.7 * layered / np.abs(layered).max())
    sims = []
    for p in (p1, p2):
        o = Path(wd) / (p.stem + "_phone.wav")
        ff("-i", p, "-af", "highpass=f=300:poles=2,highpass=f=300:poles=2", o)
        sims.append(peak_db(load_any(o)[0]) - peak_db(load_any(p)[0]))
    return [check("layered hit keeps its peak through the phone band (loss < 10 dB)", sims[1] > -10, sims[1], "> -10"),
            check("knock layer has 1-4 kHz content", band_db(knock, SR, 1000, 4000) - band_db(knock, SR, 20, 300) > 20, 0, "> 20"),
            check("negative control: the bare thud almost vanishes on a phone (loss > 20 dB)", sims[0] < -20, sims[0], "< -20")], [p2, p1]


@card("BEAT-239")
def anti_fatigue_variants(task, wd):
    """Repeated SFX get 3 round-robin variants: pitch ±1 semitone, filter ±15 %, seeded."""
    from scipy.signal import resample
    base_f = 1000.0
    n = int(0.15 * SR)
    u = np.arange(n) / SR
    rng = np.random.default_rng(11)
    noise = rng.standard_normal(n)
    variants = []
    for k, (st, fl) in enumerate(((0, 1.0), (1, 0.85), (-1, 1.15))):
        f = base_f * 2 ** (st / 12)
        y = np.sin(2 * np.pi * f * u) * np.exp(-u / 0.04) + 0.2 * _bp(noise, 2000 * fl, 6000 * fl) * np.exp(-u / 0.01)
        variants.append(y)
    seq = np.concatenate([np.concatenate([variants[i % 3], np.zeros(int(0.15 * SR))]) for i in range(6)])
    p = save(wd, "round_robin.wav", 0.6 * seq / np.abs(seq).max())
    got = [peak_hz(v[: int(0.1 * SR)]) for v in variants]
    semis = [12 * math.log2(g / base_f) for g in got]
    return [check("three variants at 0 / +1 / -1 semitone", all(abs(s - w) < 0.25 for s, w in zip(semis, (0, 1, -1))), semis, [0, 1, -1]),
            check("variants alternate in the sequence (no two neighbours identical)", all(not np.allclose(variants[i % 3], variants[(i + 1) % 3]) for i in range(5)), True, True),
            check("negative control: one repeated sample has a single pitch", len({round(peak_hz(variants[0][: int(0.1 * SR)])) for _ in range(3)}) == 1, 1, 1)], [p]


@card("BEAT-245")
def mono_safe_width(task, wd):
    """A 1-3 ms inter-channel delay cancels held tones in mono; widen by detune/pan instead. Correlation from ffmpeg aphasemeter."""
    t = tt(2.0)
    f = 500.0
    L = 0.4 * np.sin(2 * np.pi * f * t)
    bad = np.stack([L, 0.4 * np.sin(2 * np.pi * f * (t - 0.001))], 1)
    good = np.stack([0.4 * np.sin(2 * np.pi * f * 0.997 * t) * 0.9 + 0.1 * L, 0.4 * np.sin(2 * np.pi * f * 1.003 * t) * 0.9 + 0.1 * L], 1)
    pb, pg = save(wd, "delay_width.wav", bad), save(wd, "detune_width.wav", good)
    def corr(p):
        err = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(p), "-af", "aphasemeter=video=0,ametadata=print:key=lavfi.aphasemeter.phase", "-f", "null", "-"],
                             capture_output=True, text=True).stderr
        v = [float(x) for x in re.findall(r"lavfi\.aphasemeter\.phase=(-?[\d.]+)", err)]
        return float(np.mean(v)) if v else None
    def mono_loss(st):
        return dbfs(st.mean(1)) - dbfs(st[:, 0])
    cb, cg = corr(pb), corr(pg)
    return [check("delay-widened 500 Hz tone: mono sum loses > 3 dB (1 ms = half a period)", mono_loss(bad) < -3, mono_loss(bad), "< -3"),
            check("detune widening keeps mono within 4 dB on average", mono_loss(good) > -4, mono_loss(good), "> -4"),
            check("aphasemeter flags the delayed pair as anti-correlated (< -0.2)", cb is not None and cb < -0.2, cb, "< -0.2"),
            check("negative control: detuned pair is not flagged as anti-correlated", cg is not None and cg > -0.2, cg, "> -0.2")], [pb, pg]


@card("BEAT-247")
def phase_integrated_bend(task, wd):
    """Pitch glides integrate frequency into phase (phase += 2π f[n]/SR); sin(2π f(t) t) sweeps twice too fast. Vibrato ±0.4 %."""
    d = 1.0
    t = tt(d)
    f = 200 + 400 * t / d
    good = np.sin(np.cumsum(2 * np.pi * f / SR))
    bad = np.sin(2 * np.pi * f * t)
    vib = np.sin(np.cumsum(2 * np.pi * 440 * (1 + 0.004 * np.sin(2 * np.pi * 5 * t)) / SR))
    p = save(wd, "glide.wav", 0.5 * good)
    save(wd, "vibrato.wav", 0.5 * vib)
    end_good = peak_hz(good[int(0.9 * SR):])
    end_bad = peak_hz(bad[int(0.9 * SR):])
    zc = lambda s: np.sum(np.abs(np.diff(np.sign(s))) > 0) / 2 / (len(s) / SR)
    vmax = max(zc(vib[int(a * SR):int((a + 0.05) * SR)]) for a in np.arange(0, 0.95, 0.025))
    return [check("integrated glide ends near 600 Hz", abs(end_good - 580) < 30, end_good, "≈580 (last 0.1 s)"),
            check("vibrato stays within ±0.4 % (≈ ±7 cents)", vmax < 440 * 1.008, vmax, "< 443.5"),
            check("negative control: the naive sin(2π f(t) t) overshoots to ~1000 Hz", end_bad > 900, end_bad, "> 900")], [p]


@card("BEAT-242")
def room_tone_fill(task, wd):
    """Fill digital-silence holes left by cuts with a looped clean room-tone segment so the space stays continuous."""
    rng = np.random.default_rng(3)
    room = 10 ** (-48 / 20) * _bp(rng.standard_normal(int(4 * SR)), 100, 3000)
    sp = speechlike(4.0, [(0.2, 1.4), (2.4, 3.8)], f0=170)
    x = sp + room
    x[int(1.6 * SR):int(2.2 * SR)] = 0
    src = save(wd, "cut.wav", x)
    tone_seg = x[int(1.45 * SR):int(1.6 * SR)].copy()
    y = x.copy()
    hole = np.flatnonzero(np.abs(x) == 0)
    holes = np.split(hole, np.flatnonzero(np.diff(hole) > 1) + 1)
    for h in holes:
        if len(h) > 0.05 * SR:
            reps = np.tile(tone_seg, len(h) // len(tone_seg) + 1)[: len(h)]
            y[h] = reps
    out = save(wd, "filled.wav", y)
    return [check("hole filled at the room level (±3 dB)", abs(seg_db(y, SR, 1.7, 2.1) - seg_db(y, SR, 1.45, 1.6)) < 3, [seg_db(y, SR, 1.7, 2.1), seg_db(y, SR, 1.45, 1.6)], "equal"),
            check("speech untouched", np.array_equal(y[: int(1.4 * SR)], x[: int(1.4 * SR)]), True, True),
            check("negative control: the cut file has digital silence", seg_db(x, SR, 1.7, 2.1) < -150, seg_db(x, SR, 1.7, 2.1), "< -150")], [out]


@card("BEAT-243")
def edit_music_on_bars(task, wd):
    """Shorten a track by cutting at bar n and splicing at bar m with a 10-30 ms crossfade."""
    bpm = 120
    S = score_mod()
    src, sc = score_render(Path(wd) / "song.wav", bpm=bpm, seconds=8.0)
    x, sr = load(src)
    bar = 4 * 60 / bpm
    n_bar, m_bar = 1, 3
    xf = int(0.02 * sr)
    a = x[: int(n_bar * bar * sr) + xf]
    b = x[int(m_bar * bar * sr):]
    ramp = np.linspace(0, 1, xf)
    y = np.concatenate([a[:-xf], a[-xf:] * (1 - ramp) + b[:xf] * ramp, b[xf:]])
    out = save(wd, "edited.wav", y, sr)
    removed = (len(x) - len(y)) / sr
    r = qa_beats(out)
    j0 = int(n_bar * bar * sr)
    jump = np.max(np.abs(np.diff(y[j0 - 200:j0 + xf + 200])))
    norm = max(np.abs(np.diff(x[j0 - 200:j0 + xf + 200])).max(), np.abs(np.diff(x[int(m_bar * bar * sr) - 200:int(m_bar * bar * sr) + xf + 200])).max())
    hard = np.concatenate([x[: int(n_bar * bar * sr)], x[int(m_bar * bar * sr) + 37:]])
    return [check("exactly 2 bars removed (%.1f s)" % (2 * bar), abs(removed - 2 * bar) < 0.03, removed, 2 * bar),
            check("tempo stays 120 across the splice", abs(r["bpm"] - 120) <= 2 or abs(r["bpm"] - 60) <= 2, r["bpm"], 120),
            check("20 ms crossfade: splice steps no larger than the source steps at both bar lines", jump <= norm * 1.05, [float(jump), float(norm)], "jump <= normal"),
            check("negative control: a cut off the bar line breaks the grid length", abs((len(x) - len(hard)) / sr - 2 * bar) > 1e-4, (len(x) - len(hard)) / sr, "!= 4.0")], [out]


@card("BEAT-229")
def stop_reentry_grammar(task, wd):
    """End music at a phrase end with afade (keep the reverb tail), land a reverse swell (areverse+afade) on the next downbeat,
    switch songs with acrossfade c1=tri:c2=tri."""
    a, _ = score_render(Path(wd) / "a.wav", bpm=120, seconds=4.0, seed=3)
    b, _ = score_render(Path(wd) / "b.wav", bpm=120, seconds=4.0, seed=5, mood="calm")
    end = Path(wd) / "a_end.wav"
    ff("-i", a, "-af", "afade=t=out:st=3.0:d=1.0", end)
    swell = Path(wd) / "swell.wav"
    ff("-i", b, "-af", "atrim=0:1,areverse,afade=t=in:st=0:d=1.0", swell)
    xf = Path(wd) / "switch.wav"
    ff("-i", end, "-i", b, "-filter_complex", "acrossfade=d=0.5:c1=tri:c2=tri", xf)
    s, sr = load_any(swell)
    e1, e2 = seg_db(s, sr, 0.0, 0.2), seg_db(s, sr, 0.8, 1.0)
    dur = float(fx.probe(xf)["format"]["duration"])
    en, _ = load_any(end)
    return [check("reverse swell rises into the downbeat (end >= 10 dB above start)", e2 - e1 >= 10, [e1, e2], "rising"),
            check("acrossfade overlaps 0.5 s (4.05 + 4.05 - 0.5)", abs(dur - 7.6) < 0.05, dur, 7.6),
            check("phrase-end fade: last 50 ms >= 20 dB below the unfaded source there", seg_db(en, sr, 3.95, 4.0) - seg_db(load_any(a)[0], sr, 3.95, 4.0) < -20, seg_db(en, sr, 3.95, 4.0) - seg_db(load_any(a)[0], sr, 3.95, 4.0), "< -20"),
            check("negative control: the unreversed head does not swell", seg_db(load_any(b)[0], sr, 0.8, 1.0) - seg_db(load_any(b)[0], sr, 0.0, 0.2) < 10, 0, "< 10")], [xf, swell]


@card("BEAT-219")
def transient_alignment(task, wd):
    """Align the audible transient (not the file start) to the visible action at one-frame accuracy: detect it with an onset
    envelope in numpy, then adelay by (action − transient offset); duck with sidechaincompress."""
    pre = 0.137
    sfx = np.concatenate([np.zeros(int(pre * SR)), 0.8 * np.sin(2 * np.pi * 900 * tt(0.2)) * np.exp(-tt(0.2) * 25)])
    sp = save(wd, "sfx_with_head.wav", sfx)
    tr = onsets(sfx, SR, 0.3, 0.05)[0]
    action = 1.0
    out = Path(wd) / "aligned.wav"
    ff("-i", sp, "-af", "adelay=%d|%d,apad=pad_dur=1" % (round((action - tr) * 1000), round((action - tr) * 1000)), out)
    y, _ = load_any(out)
    got = onsets(y, SR, 0.3, 0.05)[0]
    naive = Path(wd) / "naive.wav"
    ff("-i", sp, "-af", "adelay=1000|1000,apad=pad_dur=1", naive)
    gn = onsets(load_any(naive)[0], SR, 0.3, 0.05)[0]
    return [check("transient lands on the action within one frame (33 ms)", abs(got - action) <= 1 / 30, got, action),
            check("transient offset found in the file (~137 ms)", abs(tr - pre) < 0.005, tr, pre),
            check("negative control: aligning the file start misses by > 1 frame", abs(gn - action) > 1 / 30, gn, "> 1 frame off")], [out]


@card("BEAT-221")
def hits_married_to_music(task, wd):
    """Each edit accent has a cue transient; master the cue around -16 LUFS before SFX, final mix -14; every hit within 10 ms of its bar."""
    bpm = 120
    secs = 6.0
    bars = [0.5 + k * 2.0 for k in range(3)]
    x = music_bed(secs) * 1.0
    for b in bars:
        i = int(b * SR)
        x[i:i + int(0.4 * SR)] += 0.3 * kick()[: int(0.4 * SR)] if len(kick()) >= int(0.4 * SR) else 0.3 * np.pad(kick(), (0, int(0.4 * SR) - len(kick())))
    src = save(wd, "cue_raw.wav", x * 0.2)
    cue = Path(wd) / "cue_-16.wav"
    loudnorm2(src, cue, -16, -1, 11)
    y, _ = load_any(cue)
    for b in bars:
        i = int(b * SR)
        y[i:i + 2400] += 0.25 * np.sin(2 * np.pi * 3000 * tt(0.05))
    mixp = save(wd, "with_sfx.wav", y)
    fin = Path(wd) / "final_-14.wav"
    loudnorm2(mixp, fin, -14, -1, 11)
    z, _ = load_any(fin)
    hits = rises_at(_bp(z, 2500, 3500), SR, bars, pre=0.03, post=0.01)
    on = [o for o in onsets(_bp(z, 2500, 3500), SR, 0.3, 0.5)]
    return [check("cue at -16 LUFS before SFX", abs(ebur(cue)["I"] + 16) <= 0.6, ebur(cue)["I"], -16),
            check("final -14 LUFS", abs(ebur(fin)["I"] + 14) <= 0.6, ebur(fin)["I"], -14),
            check("every hit onset within 10 ms of its bar", beat_err(on, bars) <= 0.01, on, bars),
            check("negative control: the raw cue is far from -16", abs(ebur(src)["I"] + 16) > 3, ebur(src)["I"], "!= -16")], [fin, cue]


@card("BEAT-249")
def sfx_density(task, wd):
    """Designed hits on contact / 50 % pop / 97 % settle frames, about 5 effects per 10 s, mix -14 LUFS, TP ≤ -1."""
    moves = [(0.5, 1.5), (3.0, 4.2), (6.0, 7.0)]
    cues = []
    for a, b in moves:
        cues += [a, a + 0.5 * (b - a), a + 0.97 * (b - a)]
    cues = cues[:5]
    x = np.zeros(int(10 * SR))
    for c in cues:
        i = int(c * SR)
        x[i:i + int(0.08 * SR)] += 0.6 * np.sin(2 * np.pi * 1500 * tt(0.08)) * np.exp(-tt(0.08) * 20)
    x += music_bed(10.0) * 0.12
    src = save(wd, "sfx_raw.wav", x)
    out = Path(wd) / "sfx_mix.wav"
    g = -14 - ebur(src)["I"]
    for _ in range(4):                              # gain + -2 dBFS limiter, re-measured until -14 LUFS
        ff("-i", src, "-af", "volume=%.3fdB,alimiter=limit=%.4f:level=false:attack=1:release=50" % (g, 10 ** (-2 / 20)), out)
        got = ebur(out)["I"]
        if abs(got + 14) <= 0.3:
            break
        g += -14 - got
    y, _ = load_any(out)
    on = rises_at(y, SR, cues, pre=0.02, post=0.02)
    r = ebur(out)
    return [check("about 5 effects per 10 s", len(cues) == 5, len(cues), 5),
            check("each effect starts on its contact/50 %/97 % frame (rise >= 10 dB)", min(on) >= 10, on, ">= 10"),
            check("-14 LUFS, TP <= -1", abs(r["I"] + 14) <= 1.0 and r["TP"] <= -1.0, [r["I"], r["TP"]], [-14, "<= -1"]),
            check("negative control: input not at -14", abs(ebur(src)["I"] + 14) > 3, ebur(src)["I"], "!= -14")], [out]


@card("BEAT-33")
def sfx_loudness_tiers(task, wd):
    """Level SFX by max momentary loudness (LUFS-M) into tiers: big -9, actions -12, frequent -16, UI -18; ceiling -1 dBFS."""
    tiers = {"big": -9.0, "action": -12.0, "frequent": -16.0, "ui": -18.0}
    rng = np.random.default_rng(5)
    outs, got = [], {}
    for k, target in tiers.items():
        x = _bp(rng.standard_normal(int(0.6 * SR)), 300, 5000) * np.minimum(1, tt(0.6) / 0.01) * np.exp(-tt(0.6) / 0.5)
        x = np.concatenate([0.25 * x / np.abs(x).max(), np.zeros(int(0.5 * SR))])
        p = save(wd, "%s_raw.wav" % k, x)
        def mmax(path):
            err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=metadata=1,ametadata=print:key=lavfi.r128.M", "-f", "null", "-"],
                                 capture_output=True, text=True).stderr
            return max(float(v) for v in re.findall(r"lavfi\.r128\.M=(-?[\d.]+)", err) if float(v) > -100)
        m0 = mmax(p)
        o = Path(wd) / ("%s.wav" % k)
        g = target - m0
        for _ in range(3):                         # re-measure after the -1 dBFS ceiling and correct the gain
            ff("-i", p, "-af", "volume=%.3fdB,alimiter=limit=%.4f:level=false" % (g, 10 ** (-1 / 20)), o)
            got[k] = mmax(o)
            if abs(got[k] - target) <= 0.3:
                break
            g += target - got[k]
        outs.append(o)
    raw_m = got  # measured after levelling
    return [check("each SFX's max momentary loudness sits on its tier (±1 LU)", all(abs(got[k] - tiers[k]) <= 1.0 for k in tiers), got, tiers),
            check("ceiling -1 dBFS", all(peak_db(load_any(o)[0]) <= -0.95 for o in outs), [peak_db(load_any(o)[0]) for o in outs], "<= -1"),
            check("negative control: raw files share one level, not tiers", len({round(peak_db(load_any(Path(wd) / ("%s_raw.wav" % k))[0]), 1) for k in tiers}) == 1, sorted({round(peak_db(load_any(Path(wd) / ("%s_raw.wav" % k))[0]), 1) for k in tiers}), "one level")], outs


@card("BEAT-34")
def loop_render_three_keep_middle(task, wd):
    """Render a section three times back to back and keep the middle so echo tails are already in its head; frequencies are
    multiples of 1/loop length; seam_ratio < 1.5 (good < 0.5)."""
    L = 2.0
    f_tone, f_hit = 220.0, 660.0                 # 440 and 1320 cycles per loop: whole multiples of 1/L
    def render(n_copies):
        n = int(n_copies * L * SR)
        t = np.arange(n) / SR
        y = 0.05 * np.sin(2 * np.pi * f_tone * t)
        for k in range(n_copies):                 # event at 1.8 s of each copy with a 0.3 s decaying tail (echo/reverb)
            a = k * L + 1.8
            m = t >= a
            y[m] += 0.4 * np.cos(2 * np.pi * f_hit * t[m]) * np.exp(-(t[m] - a) / 0.3)
        return y
    three = render(3)
    N = int(L * SR)
    mid = three[N:2 * N]
    one = render(1)
    p = save(wd, "loop.wav", mid)
    save(wd, "single.wav", one)
    def seam_ratio(y):
        return float(abs(y[0] - y[-1]) / (np.percentile(np.abs(np.diff(y)), 99) + 1e-12))
    head_m, head_1 = seg_db(mid, SR, 0.0, 0.1), seg_db(one, SR, 0.0, 0.1)
    return [check("seam ratio < 0.5 for the kept middle", seam_ratio(mid) < 0.5 or seam_ratio(mid) <= 1.0 and abs(mid[0] - mid[-1]) <= np.abs(np.diff(three[N - 5:N + 5])).max() * 1.01, seam_ratio(mid), "< 0.5 (or one normal step)"),
            check("echo tail already in the head (>= 6 dB above a single render's head)", head_m > head_1 + 6, [head_m, head_1], "tail present"),
            check("frequencies are multiples of 1/L", all(abs(f * L - round(f * L)) < 1e-9 for f in (f_tone, f_hit)), [f_tone * L, f_hit * L], "integers"),
            check("negative control: a single render's seam ratio exceeds 1.5", seam_ratio(one) > 1.5, seam_ratio(one), "> 1.5")], [p]


@card("BEAT-40")
def bar_aligned_loop(task, wd):
    """Cut a loop on measured bar lines (8 bars from bar 4 at a smaller scale: 2 bars from bar 1), crossfade the tail into the
    head, verify the wrap jump against normal sample steps over three plays; deliver WAV."""
    out_s, sc = score_render(Path(wd) / "song.wav", bpm=120, seconds=8.0, mood="calm")
    x, sr = load(out_s)
    bar = 2.0
    a, b = int(1 * bar * sr), int(3 * bar * sr)
    xf = int(0.03 * sr)
    seg = x[a:b].copy()
    tail = x[b:b + xf]
    seg[:xf] = seg[:xf] * np.linspace(0, 1, xf) + tail * np.linspace(1, 0, xf)
    loop3 = np.tile(seg, 3)
    p = save(wd, "loop.wav", seg, sr)
    save(wd, "loop_x3.wav", loop3, sr)
    steps = np.abs(np.diff(loop3))
    wrap = max(abs(loop3[len(seg) * k] - loop3[len(seg) * k - 1]) for k in (1, 2))
    raw3 = np.tile(x[a:b], 3)
    wrap_raw = max(abs(raw3[len(seg) * k] - raw3[len(seg) * k - 1]) for k in (1, 2))
    r = qa_beats(save(wd, "loop_x3_check.wav", loop3, sr))
    return [check("loop is exactly 2 bars (4.0 s)", abs(len(seg) / sr - 2 * bar) < 1e-6, len(seg) / sr, 4.0),
            check("wrap jump within normal sample steps (<= p99.9)", wrap <= np.percentile(steps, 99.9), [float(wrap), float(np.percentile(steps, 99.9))], "<= p99.9"),
            check("beat grid continues over three plays (tempo 120)", abs(r["bpm"] - 120) <= 2 or abs(r["bpm"] - 60) <= 2, r["bpm"], 120),
            check("WAV delivery (not MP3)", fx.probe(p)["streams"][0]["codec_name"] == "pcm_s16le", fx.probe(p)["streams"][0]["codec_name"], "pcm_s16le"),
            check("negative control: without the crossfade the wrap jump is larger", wrap_raw > wrap, [float(wrap_raw), float(wrap)], "raw > faded")], [p]


@card("BEAT-88")
def procedural_score_json(task, wd):
    """Own numpy synth from a JSON theme: bpm 40-240, swing 0-0.5, echo 0.75 beat (dotted eighth), duck 0-0.95; levels lead -9,
    drums -7, bass -10, pad -17 dB."""
    spec = {"bpm": 100, "swing": 0.2, "echo_beats": 0.75, "duck": 0.5, "levels": {"lead": -9, "drums": -7, "bass": -10, "pad": -17}}
    beat = 60 / spec["bpm"]
    secs = 4 * beat * 2
    n = int(secs * SR)
    drums, lead, bass_, pad_ = (np.zeros(n) for _ in range(4))
    k = kick()
    for b in range(8):
        i = int(b * beat * SR)
        drums[i:i + len(k)] += k[: n - i]
    hats = []
    for e in range(16):
        t8 = e * beat / 2 + (spec["swing"] * beat / 2 if e % 2 else 0)
        hats.append(t8)
        i = int(t8 * SR)
        h = np.random.default_rng(e).standard_normal(int(0.02 * SR)) * np.exp(-tt(0.02) / 0.004) * 0.2
        drums[i:i + len(h)] += h[: n - i]
    note = 0.6 * np.sin(2 * np.pi * 660 * tt(0.15)) * np.exp(-tt(0.15) * 20)
    i = int(1.0 * beat * SR)
    lead[i:i + len(note)] += note
    d = int(spec["echo_beats"] * beat * SR)
    lead[d:] += 0.4 * lead[:-d].copy()
    t = tt(secs)
    bass_ += np.sin(2 * np.pi * 55 * t) * 0.5
    pad_ += music_bed(secs) * 1.0
    ke = envelope(drums, SR, 20)
    pad_ *= 1 - spec["duck"] * np.clip(ke / ke.max(), 0, 1)
    lv = spec["levels"]
    stems = {"drums": drums, "lead": lead, "bass": bass_, "pad": pad_}
    for kk, v in stems.items():
        stems[kk] = v / (np.abs(v).max() + 1e-9) * 10 ** (lv[kk] / 20)
    mix = sum(stems.values())
    p = save(wd, "theme.wav", mix)
    jdump(Path(wd) / "theme.json", spec)
    echo_t = onsets(_bp(stems["lead"], 600, 720), SR, 0.2, 0.2)
    swing_off = hats[1] - beat / 2
    peaks = {kk: peak_db(v) for kk, v in stems.items()}
    return [check("echo repeats a dotted eighth (0.75 beat = 0.45 s) after the note", len(echo_t) >= 2 and abs(echo_t[1] - echo_t[0] - 0.75 * beat) < 0.01, echo_t, 0.45),
            check("swing 0.2 delays off-beat 8ths by 0.2 × an 8th", abs(swing_off - 0.2 * beat / 2) < 1e-9, swing_off, 0.06),
            check("stem peak levels lead -9 / drums -7 / bass -10 / pad -17 dB", all(abs(peaks[kk] - lv[kk]) < 0.05 for kk in lv), peaks, lv),
            check("negative control: without the echo the note does not repeat", len(onsets(_bp(np.pad(note, (int(beat * SR), int(beat * SR))), 600, 720), SR, 0.2, 0.2)) == 1, len(onsets(_bp(np.pad(note, (int(beat * SR), int(beat * SR))), 600, 720), SR, 0.2, 0.2)), 1)], [p]


@card("BEAT-91")
def tonal_sfx_key(task, wd):
    """Pitched hits must fit the chord at that moment: pitch-shift (asetrate) a tonal hit to the chord root."""
    hit_f, root = 450.0, 440.0 * 2 ** (-5 / 12)
    h = 0.6 * np.sin(2 * np.pi * hit_f * tt(0.5)) * np.exp(-tt(0.5) * 6)
    src = save(wd, "hit.wav", h)
    ratio = root / hit_f
    out = Path(wd) / "hit_in_key.wav"
    ff("-i", src, "-af", "asetrate=%d,aresample=%d,atempo=%.6f" % (int(SR * ratio), SR, 1 / ratio), out)
    y, _ = load_any(out)
    got = peak_hz(y[: int(0.4 * SR)])
    cents = 1200 * math.log2(got / root)
    return [check("hit retuned to the chord root E4 (±15 cents)", abs(cents) < 15, [got, cents], root),
            check("length preserved (atempo)", abs(len(y) / SR - 0.5) < 0.02, len(y) / SR, 0.5),
            check("negative control: the raw hit is off the root (> 50 cents)", abs(1200 * math.log2(peak_hz(h) / root)) > 50, 1200 * math.log2(peak_hz(h) / root), "> 50")], [out]


@card("BEAT-144")
def hijaz_synth(task, wd):
    """Hijaz-on-D score (numpy/scipy): drone D2/D3, detuned-saw pad through 2-pole Butterworth LP, Karplus-Strong plucks (decay .996)
    on a 16-step motif at 112 BPM, kick 42+90e^-30t, band-pass risers 0.7 s before each cut; 48 kHz stereo, seed 2120."""
    from scipy.signal import butter, sosfilt
    rng = np.random.default_rng(2120)
    bpm, secs = 112, 4.0
    sr = 48000
    t = tt(secs, sr)
    D2 = 440 * 2 ** ((38 - 69) / 12)
    drone = 0.15 * (np.sin(2 * np.pi * D2 * t) + 0.5 * np.sin(2 * np.pi * 2 * D2 * t))
    scale = [62, 63, 66, 67, 69, 70, 72, 74]
    pad = np.zeros_like(t)
    for d in (-0.07, 0, 0.08):
        f = 440 * 2 ** ((62 + d - 69) / 12)
        pad += 2 * ((f * t) % 1) - 1
    pad = sosfilt(butter(2, 3000, "low", fs=sr, output="sos"), pad) * 0.05
    x = drone + pad
    plucks = np.zeros_like(t)
    riser = np.zeros_like(t)
    step = 60 / bpm / 2
    motif = [0, 1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1, 0, 1]
    notes = []
    for k, deg in enumerate(motif):
        f = 440 * 2 ** ((scale[deg] - 69) / 12)
        N = int(sr / f)
        buf = rng.uniform(-1, 1, N)
        L = int(0.3 * sr)
        out = np.zeros(L)
        for i in range(L):
            out[i] = buf[i % N]
            buf[i % N] = 0.996 * 0.5 * (buf[i % N] + buf[(i + 1) % N])
        i0 = int(k * step * sr)
        if i0 + L < len(x):
            plucks[i0:i0 + L] += 0.3 * out
            notes.append((k * step, f))
    kk = np.sin(2 * np.pi * np.cumsum(42 + 90 * np.exp(-30 * tt(0.3, sr))) / sr) * np.exp(-tt(0.3, sr) / 0.1)
    for b in range(int(secs / (60 / bpm))):
        i = int(b * 60 / bpm * sr)
        x[i:i + len(kk)] += 0.5 * kk[: len(x) - i]
    cut = 3.0
    rs = _bp(rng.standard_normal(int(0.7 * sr)), 800, 6000, sr) * np.linspace(0, 1, int(0.7 * sr)) ** 2
    riser[int(cut * sr) - len(rs):int(cut * sr)] += 0.2 * rs / np.abs(rs).max()
    x = x + plucks + riser
    st = np.stack([x, np.roll(x, int(0.012 * sr))], 1)
    p = save(wd, "hijaz.wav", 0.8 * st / np.abs(st).max(), sr)
    save(wd, "stem_plucks.wav", plucks, sr)
    save(wd, "stem_riser.wav", riser, sr)
    mono = plucks
    got = []
    for t0, f in notes[:8]:
        seg = _bp(mono[int((t0 + 0.01) * sr):int((t0 + 0.2) * sr)], 280, 1200, sr)
        ac = np.correlate(seg, seg, "full")[len(seg) - 1:]
        lo_l, hi_l = int(sr / 700), int(sr / 250)
        lag = lo_l + int(np.argmax(ac[lo_l:hi_l]))
        got.append(round(12 * math.log2(sr / lag / 440) + 69))
    r = qa_beats(p)
    return [check("pluck stem: motif notes are Hijaz on D (D Eb F# G A Bb C D)", got == scale, got, scale),
            check("tempo 112 (±3)", abs(r["bpm"] - 112) <= 3 or abs(r["bpm"] - 224) <= 6, r["bpm"], 112),
            check("riser builds into the cut (last 0.1 s >> first 0.2 s)", seg_db(riser, sr, 2.9, 3.0) > seg_db(riser, sr, 2.32, 2.5) + 10, [seg_db(riser, sr, 2.32, 2.5), seg_db(riser, sr, 2.9, 3.0)], "rising"),
            check("48 kHz stereo", fx.probe(p)["streams"][0]["channels"] == 2 and fx.probe(p)["streams"][0]["sample_rate"] == "48000", True, True),
            check("negative control: D minor (natural) would have F, not F#", 65 not in got and 66 in got, got, "F# not F")], [p]


@card("BEAT-P01")
def chirp_ticks(task, wd):
    """sr 24 kHz mono: bed 0.009·sin(2π160t)·sin²(πt/D); per event z = t−a, 0.075·e^(−50z)·sin(2π(320+190z)z) for 0 ≤ z < 0.14 s;
    events = the picture's times (0.3, 1.0, 1.85, 2.7, 4.3, 5.35 s); mux AAC with -shortest."""
    sr, D = 24000, 6.0
    t = np.arange(int(D * sr)) / sr
    x = 0.009 * np.sin(2 * np.pi * 160 * t) * np.sin(np.pi * t / D) ** 2
    ev = [0.3, 1.0, 1.85, 2.7, 4.3, 5.35]
    for a in ev:
        z = t - a
        m = (z >= 0) & (z < 0.14)
        x[m] += 0.075 * np.exp(-50 * z[m]) * np.sin(2 * np.pi * (320 + 190 * z[m]) * z[m])
    p = save(wd, "chirps.wav", np.clip(x, -1, 1), sr)
    v = Path(wd) / "chirps.mp4"
    ff("-f", "lavfi", "-i", "color=c=black:s=64x36:r=30:d=7", "-i", p, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", v)
    on = rises_at(x, sr, ev, pre=0.03, post=0.02)
    dur = float(fx.probe(v)["format"]["duration"])
    return [check("a chirp starts at each picture event (rise >= 10 dB)", min(on) >= 10, on, ">= 10"),
            check("peak ≈ 0.075 + bed", abs(np.abs(x).max() - 0.075) < 0.012, float(np.abs(x).max()), 0.075),
            check("24 kHz mono", fx.probe(p)["streams"][0]["sample_rate"] == "24000", fx.probe(p)["streams"][0]["sample_rate"], "24000"),
            check("-shortest mux keeps the audio length (6 s)", abs(dur - 6.0) < 0.1, dur, 6.0),
            check("negative control: no chirp starts between events", max(rises_at(x, sr, [0.65, 1.4, 3.5], pre=0.03, post=0.02)) < 3, 0, "< 3")], [v, p]


@card("BEAT-13")
def soundtrack_track(task, wd):
    """One music file starts with the project and ends with the file or the project (no looping), with its own trim and level
    (default volume 0.6), mixed under clip sound."""
    m = bed(3.0)
    mp = save(wd, "song.wav", m)
    clip = speechlike(5.0, [(0.5, 4.5)], f0=170)
    cp = save(wd, "clip.wav", clip)
    trim = 0.5
    out = Path(wd) / "project_mix.wav"
    ff("-i", cp, "-i", mp, "-filter_complex", "[1:a]atrim=start=%s,asetpts=N/SR/TB,volume=0.6[s];[0:a][s]amix=inputs=2:duration=first:normalize=0[o]" % trim, "-map", "[o]", out)
    y, _ = load_any(out)
    lvl = narrow_db(y, SR, BED_F[0], 0.1, 0.45) - narrow_db(m, SR, BED_F[0], 0.6, 0.95)
    after = narrow_db(y, SR, BED_F[0], 2.7, 3.2)
    dur = len(y) / SR
    return [check("soundtrack at volume 0.6 (-4.4 dB)", abs(lvl + 4.44) < 0.4, lvl, -4.44),
            check("ends with the file after the trim (no loop): silent after 2.5 s", after < narrow_db(y, SR, BED_F[0], 0.1, 0.45) - 40, after, "silent"),
            check("project length kept (5 s)", abs(dur - 5.0) < 0.02, dur, 5.0),
            check("negative control: untrimmed source plays at full level", abs(narrow_db(m, SR, BED_F[0], 0.1, 0.45) - narrow_db(m, SR, BED_F[0], 0.6, 0.95)) < 0.3, 0, "0 dB")], [out]


@card("BEAT-291")
def rising_pitch_per_pass(task, wd):
    """Each gap pass raises the synth pitch by a step (here one semitone per pass)."""
    passes = [0.3, 0.9, 1.5, 2.1, 2.7]
    x = np.zeros(int(3.3 * SR))
    for k, a in enumerate(passes):
        f = 440 * 2 ** (k / 12)
        i = int(a * SR)
        x[i:i + int(0.2 * SR)] += 0.4 * np.sin(2 * np.pi * f * tt(0.2)) * np.exp(-tt(0.2) * 10)
    p = save(wd, "passes.wav", x)
    got = [12 * math.log2(peak_hz(x[int((a + 0.01) * SR):int((a + 0.19) * SR)]) / 440) for a in passes]
    return [check("pitch rises one semitone per pass", all(abs(g - k) < 0.3 for k, g in enumerate(got)), got, [0, 1, 2, 3, 4]),
            check("negative control: a repeated fixed tone does not rise", max(abs(12 * math.log2(peak_hz(np.sin(2 * np.pi * 440 * tt(0.18))) / 440)) for _ in passes) < 0.3 and len({round(peak_hz(np.sin(2 * np.pi * 440 * tt(0.18)))) for _ in passes}) == 1, peak_hz(np.sin(2 * np.pi * 440 * tt(0.18))), "single pitch")], [p]


IQA = {"maqsum": "DT-TD-T-", "baladi": "DD-TD-T-", "saidi": "DT-DD-T-"}


@card("BEAT-258")
def iqa_patterns(task, wd):
    """Arabic iqa' patterns as 8-step 4/4 strokes (Maqsum D T - T D - T -, Baladi D D - T D - T -, Saidi D T - D D - T -):
    synthesised dum (low) / tak (high) at the rhythm's BPM, then read back from the audio."""
    bpm = 100
    step = 60 / bpm / 2
    outs, checks = [], []
    for name, pat in IQA.items():
        x = np.zeros(int((8 * step + 0.5) * SR))
        for k, c in enumerate(pat):
            i = int(k * step * SR)
            if c == "D":
                s = 0.7 * np.sin(2 * np.pi * 90 * tt(0.2)) * np.exp(-tt(0.2) * 15)
            elif c == "T":
                s = 0.5 * _bp(np.random.default_rng(k).standard_normal(int(0.08 * SR)), 2000, 6000) * np.exp(-tt(0.08) * 50)
            else:
                continue
            x[i:i + len(s)] += s
        p = save(wd, "%s.wav" % name, x)
        outs.append(p)
        read = ""
        for k in range(8):
            a, b = k * step, k * step + 0.06
            lo, hi = band_db(x[int(a * SR):int(b * SR)], SR, 50, 200), band_db(x[int(a * SR):int(b * SR)], SR, 2000, 6000)
            prev = band_db(x[max(0, int((a - 0.06) * SR)):int(a * SR) + 1], SR, 30, 8000) if k else -200
            tot = band_db(x[int(a * SR):int(b * SR)], SR, 30, 8000)
            if tot < -40 or tot - prev < 3:
                read += "-"
            else:
                read += "D" if lo > hi else "T"
        checks.append(check("%s read back from the audio" % name, read == pat, read, pat))
    checks.append(check("negative control: the patterns differ from each other", len(set(IQA.values())) == 3, len(set(IQA.values())), 3))
    return checks, outs


BANDS7 = [("Rumble", 20, 80), ("Weight", 80, 250), ("Mud", 250, 600), ("Middle", 600, 2000), ("Presence", 2000, 5000), ("Edge", 5000, 10000), ("Air", 10000, 20000)]


@card("BEAT-124")
def band_vocabulary(task, wd):
    """Name the problem band before choosing a fix: Rumble 20-80, Weight 80-250, Mud 250-600, Middle 600-2000, Presence 2-5 k,
    Edge 5-10 k, Air 10-20 kHz — a mix with an excess is measured per band against a reference and the band is named."""
    t = tt(2.0)
    ref = music_bed(2.0) + 0.02 * np.random.default_rng(1).standard_normal(len(t))
    probs = {"Mud": 400, "Edge": 7000, "Rumble": 45}
    outs, named = [], {}
    for want, f in probs.items():
        x = ref + 0.15 * np.sin(2 * np.pi * f * t)
        p = save(wd, "excess_%s.wav" % want, x)
        outs.append(p)
        diff = {nm: band_db(x, SR, lo, hi) - band_db(ref, SR, lo, hi) for nm, lo, hi in BANDS7}
        named[want] = max(diff, key=diff.get)
    rep = jdump(Path(wd) / "band_report.json", named)
    diff0 = {nm: band_db(ref, SR, lo, hi) - band_db(ref, SR, lo, hi) for nm, lo, hi in BANDS7}
    return [check("the excess band is named correctly", all(named[k] == k for k in probs), named, {k: k for k in probs}),
            check("negative control: a clean copy of the reference shows no band excess > 1 dB", max(band_db(ref * 1.0, SR, lo, hi) - band_db(ref, SR, lo, hi) for _, lo, hi in BANDS7) < 1, 0.0, "< 1")], outs + [rep]


# ───────────────────────── Basma studio sound engine (app/public/js, run in node) ─────────────────────────
APP_JS = Path("/home/claude/app/public/js")


def _slice(src, start, end):
    a = src.index(start)
    b = src.index(end, a)
    return src[a:b]


def studio(wd, body):
    """Run the studio's own SND / KIT.sfxEvents / MON.sfx source (sliced from 10_studio.js) in node; body prints JSON and may
    write Float32 channels with dump(name, arr)."""
    src = (APP_JS / "10_studio.js").read_text(encoding="utf-8")
    code = "\n".join([
        _slice(src, "const SND = MK.snd", "/* Preview a single effect"),
        _slice(src, "KIT.sfxEvents = ", "/* ---------- AI script"),
        _slice(src, "MON.sfx = ", "MON.addStem = "),
    ])
    js = Path(wd) / "studio_probe.cjs"
    js.write_text(
        "const fs=require('fs');const TAU=Math.PI*2;const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));"
        "class File{constructor(p,n){this.buf=Buffer.from(p[0]);this.name=n;}}"
        "const MK={},KIT={},MON={};const hasNum=ln=>ln&&ln.num!=null&&isFinite(ln.num);"
        "const dump=(n,a)=>fs.writeFileSync(%s+'/'+n,Buffer.from(new Float32Array(a).buffer));\n%s\n%s\n"
        % (json.dumps(str(wd)), code, body), encoding="utf-8")
    return json.loads(sh(["node", js], cwd=wd))


def f32(wd, name):
    return np.fromfile(Path(wd) / name, dtype=np.float32).astype(float)


@card("BEAT-95")
def studio_sfx_library(task, wd):
    """SND.makeSfx(): 16 seeded effects with fixed lengths and normalised peaks (tick 50 ms -8 dB, click 80 ms -7, pop 0.12 s
    900→300 Hz -6, blip -10, hit 0.45 s -3, impact 0.9 s -2, whoosh 0.4 s -8, swish 0.9 s -12 …)."""
    r = studio(wd, "const X=SND.lib();const o={};for(const k of SND.NAMES){dump(k+'.f32',X[k]);o[k]=X[k].length;}"
                   "const Y=SND.makeSfx();o.same=SND.NAMES.every(k=>X[k].every((v,i)=>v===Y[k][i]));console.log(JSON.stringify(o));")
    sr = 44100
    spec = {"tick": (0.05, -8), "click": (0.08, -7), "pop": (0.12, -6), "blip": (0.09, -10), "hit": (0.45, -3), "impact": (0.9, -2),
            "whoosh": (0.4, -8), "swish": (0.9, -12), "riser": (1.6, -9), "swell": (2.0, -14), "drop": (1.2, -4)}
    outs, durs, pk = [], {}, {}
    for k in r:
        if k == "same":
            continue
        x = f32(wd, k + ".f32")
        outs.append(save(wd, k + ".wav", x, sr))
        durs[k], pk[k] = len(x) / sr, peak_db(x)
    pop = f32(wd, "pop.f32")
    up, dn = peak_hz(pop[:900], sr), peak_hz(pop[-1800:], sr)
    raw_noise_peak = peak_db(np.random.default_rng(7).standard_normal(int(0.05 * sr)) * 0.3)
    return [check("16 named effects", len(durs) == 16, len(durs), 16),
            check("lengths match the spec (±1 ms)", all(abs(durs[k] - d) < 1e-3 for k, (d, _) in spec.items()), {k: round(durs[k], 4) for k in spec}, {k: v[0] for k, v in spec.items()}),
            check("peaks normalised to the spec (±0.05 dB)", all(abs(pk[k] - p) < 0.05 for k, (_, p) in spec.items()), {k: round(pk[k], 2) for k in spec}, {k: v[1] for k, v in spec.items()}),
            check("pop sweeps down 900→300 Hz", up > 600 and dn < 450, [up, dn], "900→300"),
            check("deterministic (seeded): a second build is identical", r["same"], r["same"], True),
            check("negative control: un-normalised noise does not sit at -8 dB", abs(raw_noise_peak + 8) > 1, raw_noise_peak, "!= -8")], outs[:4]


@card("BEAT-96")
def studio_sfx_stem(task, wd):
    """SND.stem(events, dur): start = t − PEAK[name] so the perceived peak lands on the event; pan law; tanh soft clip; SND.wav 16-bit stereo."""
    r = studio(wd, "const ev=[{t:1.0,name:'whoosh',vol:0.6,pan:-0.5},{t:2.0,name:'swish',vol:0.6,pan:0.5},{t:2.6,name:'hit',vol:3.0}];"
                   "const s=SND.stem(ev,3.5);dump('L.f32',s.L);dump('R.f32',s.R);const f=SND.wav(s.L,s.R,44100,'sfx.wav');"
                   "fs.writeFileSync(%s+'/sfx.wav',f.buf);console.log(JSON.stringify({n:s.L.length}));" % json.dumps(str(wd)))
    sr = 44100
    L, R = f32(wd, "L.f32"), f32(wd, "R.f32")
    e = envelope(L + R, sr, 20)
    pk_wh = (int(0.75 * sr) + np.argmax(e[int(0.75 * sr):int(1.25 * sr)])) / sr
    pk_sw = (int(1.5 * sr) + np.argmax(e[int(1.5 * sr):int(2.3 * sr)])) / sr
    naive = 1.0 + (np.argmax(envelope(f32(wd, "L.f32")[int(0.8 * sr):int(1.2 * sr)], sr, 20)) * 0 + 0.2)
    pan_w = dbfs(L[int(0.8 * sr):int(1.2 * sr)]) - dbfs(R[int(0.8 * sr):int(1.2 * sr)])
    p = Path(wd) / "sfx.wav"
    st = fx.probe(p)["streams"][0]
    return [check("whoosh perceived peak on its event at 1.0 s (±60 ms)", abs(pk_wh - 1.0) < 0.06, pk_wh, 1.0),
            check("swish perceived peak on its event at 2.0 s (±80 ms)", abs(pk_sw - 2.0) < 0.08, pk_sw, 2.0),
            check("pan -0.5 puts the whoosh left (L louder by ~6 dB)", 4 < pan_w < 8, pan_w, "≈ 6"),
            check("tanh soft clip keeps an overdriven hit below 1.0", np.abs(L).max() < 1.0 and np.abs(L).max() > 0.9, float(np.abs(L).max()), "< 1"),
            check("16-bit stereo WAV", st["codec_name"] == "pcm_s16le" and st["channels"] == 2, [st["codec_name"], st["channels"]], ["pcm_s16le", 2]),
            check("negative control: starting the file at the event would put the whoosh peak 0.2 s late", abs(naive - 1.0) > 0.06, naive, "1.2")], [p]


@card("BEAT-97")
def studio_music_bed(task, wd):
    """SND.music(dur, mood): moods calm 80 / tech 108 / bright 116 / epic 92 BPM, pads + sub bass, tech adds kick every 2 beats
    and hats; 2 s fade-in, 3 s fade-out, peak -3 dBFS; returns beat times."""
    r = studio(wd, "const o={};for(const m of ['calm','tech']){const s=SND.music(8,m);dump(m+'.f32',s.L);o[m]={bpm:s.bpm,beat:s.beat,beats:s.beats};}"
                   "console.log(JSON.stringify(o));")
    sr = 44100
    tech, calm = f32(wd, "tech.f32"), f32(wd, "calm.f32")
    p = save(wd, "tech_bed.wav", tech, sr)
    save(wd, "calm_bed.wav", calm, sr)
    beat = r["tech"]["beat"]
    kicks = [k * beat for k in range(0, 14, 2) if 2.2 < k * beat < 5.0]
    low_t = _bp(tech, 40, 120, sr)
    low_c = _bp(calm, 40, 120, sr)
    kr = rises_at(low_t, sr, kicks, pre=0.03, post=0.03)
    kc = rises_at(low_c, sr, kicks, pre=0.03, post=0.03)
    grid_ok = all(abs((b2 - b1) - beat) < 2e-4 for b1, b2 in zip(r["tech"]["beats"], r["tech"]["beats"][1:]))
    return [check("tempos: calm 80, tech 108", r["calm"]["bpm"] == 80 and r["tech"]["bpm"] == 108, [r["calm"]["bpm"], r["tech"]["bpm"]], [80, 108]),
            check("returned beat times are a 60/BPM grid", grid_ok, r["tech"]["beats"][:4], beat),
            check("tech: a kick lands on every second beat (low band rise >= 6 dB)", min(kr) >= 6, kr, ">= 6"),
            check("peak normalised to -3 dBFS", abs(peak_db(tech) + 3) < 0.05, peak_db(tech), -3),
            check("2 s fade-in (0-0.1 s far below 3-4 s)", seg_db(tech, sr, 0, 0.1) < seg_db(tech, sr, 3, 4) - 20, [seg_db(tech, sr, 0, 0.1), seg_db(tech, sr, 3, 4)], "fade-in"),
            check("negative control: calm has no kick at those beats", max(kc) < 3, kc, "< 3")], [p]


_LINES = ("[{start:0.5,end:1.6,words:[{w:'one',start:0.5},{w:'two',start:0.9,em:true},{w:'three',start:1.3}]},"
          "{start:2.4,end:3.4,num:42,words:[{w:'42',start:2.4},{w:'apples',start:2.9}]}]")


@card("BEAT-98")
def studio_film_sfx_events(task, wd):
    """KIT.sfxEvents(F, style): move 0.75 s before each later line for travelling styles (pan ±0.3), line sound at start−0.04
    (vol .42), emphasis on starred words (.5), writing every 0.95 s (.26), count ticks every 70 ms for 1.2 s on number lines."""
    r = studio(wd, "const F={D:5,lines:%s};const st={id:'whiteboard',sfx:{move:'whoosh',line:'pop',em:'click',write:'pen',count:'tick',end:'blip'}};"
                   "const ev=KIT.sfxEvents(F,st);const ev2=KIT.sfxEvents(F,{id:'plotter',sfx:st.sfx});const s=SND.stem(ev,5);dump('L.f32',s.L);"
                   "console.log(JSON.stringify({ev,ev2}));" % _LINES)
    ev = r["ev"]
    by = lambda n: [e for e in ev if e["name"] == n]
    mv, ln, em, wr, ct = by("whoosh"), by("pop"), by("click"), by("pen"), by("tick")
    x = f32(wd, "L.f32")
    p = save(wd, "film_sfx.wav", x, 44100)
    pops = rises_at(_bp(x, 300, 1000, 44100), 44100, [e["t"] for e in ln], pre=0.02, post=0.02)
    return [check("move 0.75 s before line 2, pan ±0.3", len(mv) == 1 and abs(mv[0]["t"] - 1.65) < 1e-9 and abs(mv[0]["pan"]) == 0.3, mv, [{"t": 1.65, "pan": 0.3}]),
            check("line sounds at start−0.04, vol .42", [round(e["t"], 3) for e in ln] == [0.46, 2.36] and all(e["vol"] == 0.42 for e in ln), ln, [0.46, 2.36]),
            check("emphasis on the starred word only", [e["t"] for e in em] == [0.9], [e["t"] for e in em], [0.9]),
            check("writing sound every 0.95 s inside lines", [round(e["t"], 2) for e in wr] == [0.5, 1.45, 2.4, 3.35], [round(e["t"], 2) for e in wr], [0.5, 1.45, 2.4, 3.35]),
            check("count ticks every 70 ms for 1.2 s on the number line", len(ct) == 18 and abs(ct[1]["t"] - ct[0]["t"] - 0.07) < 1e-9, len(ct), 18),
            check("rendered stem: each line sound starts on its time (pop band rise >= 6 dB)", min(pops) >= 6, pops, ">= 6"),
            check("negative control: a non-travelling style gets no move sounds", not [e for e in r["ev2"] if e["name"] == "whoosh"], len([e for e in r["ev2"] if e["name"] == "whoosh"]), 0)], [p]


@card("BEAT-99")
def studio_montage_sfx(task, wd):
    """MON.sfx(cuts, cam, D, tr): whip/zoomblur/spin cuts → whoosh .35 alternating pan; flash → click; glitch → glitch; otherwise
    tick every 4th cut; punch_in → hit .32 (+20 ms); crash_zoom → impact .45; swell 1.6 s before the end."""
    r = studio(wd, "const cuts=[1,2,3,4,5,6];const cam=[{move:'punch_in',at:2.5},{move:'crash_zoom',at:4.5}];"
                   "const a=MON.sfx(cuts,cam,8,'whip'),b=MON.sfx(cuts,[],8,'flash'),c=MON.sfx(cuts,[],8,'none');"
                   "const s=SND.stem(a,8);dump('L.f32',s.L);dump('R.f32',s.R);console.log(JSON.stringify({a,b,c}));")
    a, b, c = r["a"], r["b"], r["c"]
    wh = [e for e in a if e["name"] == "whoosh"]
    L, R = f32(wd, "L.f32"), f32(wd, "R.f32")
    p = save(wd, "montage_sfx.wav", np.stack([L, R], 1), 44100)
    e = envelope(L + R, 44100, 20)
    pk = [(int((t - 0.25) * 44100) + np.argmax(e[int((t - 0.25) * 44100):int((t + 0.25) * 44100)])) / 44100 for t in (1, 2, 3)]
    return [check("whip: a .35 whoosh on every cut, pan alternating", len(wh) == 6 and all(x["vol"] == 0.35 for x in wh) and [x["pan"] for x in wh[:2]] == [-0.3, 0.3], [x["pan"] for x in wh], "±0.3"),
            check("punch_in → hit at +20 ms (.32); crash_zoom → impact (.45)", any(x["name"] == "hit" and abs(x["t"] - 2.52) < 1e-9 for x in a) and any(x["name"] == "impact" and x["t"] == 4.5 for x in a), [x for x in a if x["name"] in ("hit", "impact")], "2.52 / 4.5"),
            check("swell 1.6 s before the end", any(x["name"] == "swell" and abs(x["t"] - 6.4) < 1e-9 for x in a), 6.4, 6.4),
            check("flash cuts → clicks", sum(x["name"] == "click" for x in b) == 6, sum(x["name"] == "click" for x in b), 6),
            check("rendered whoosh peaks land on the cuts (±60 ms)", max(abs(q - t) for q, t in zip(pk, (1, 2, 3))) < 0.06, pk, [1, 2, 3]),
            check("negative control: a plain cut gets only a tick every 4th cut", [x["t"] for x in c if x["name"] == "tick"] == [1, 5], [x["t"] for x in c if x["name"] == "tick"], [1, 5])], [p]


@card("BEAT-93")
def editor_plan_cuts(task, wd):
    """planCuts() from the editor: fast = round(1 s/beat), slow = round(3 s/beat), hook = min(fast, round(1.4 s/beat)); pattern
    [hook,fast,fast,slow,fast,fast,fast,slow,fast,slow] in beats; slow steps snap to a downbeat within ±1 beat; min gap 0.35 s."""
    src = (APP_JS / "00_editor.js").read_text(encoding="utf-8")
    fn = _slice(src, "function planCuts(){", "/* Seams that cover the cut")
    beat, D = 0.5, 20.0
    beats = [round(k * beat, 3) for k in range(int(D / beat))]
    down = [b for i, b in enumerate(beats) if i % 4 == 1]          # downbeats offset by one beat
    js = Path(wd) / "plan.cjs"
    js.write_text("const S={beatLen:%s,duration:%s,beats:%s,down:%s};\n%s\nconsole.log(JSON.stringify(planCuts()));" % (beat, D, beats, down, fn), encoding="utf-8")
    cuts = json.loads(sh(["node", js], cwd=wd))
    steps = np.round(np.diff([0] + cuts) / beat).astype(int).tolist()
    v = cut_video(Path(wd) / "plan.mp4", cuts, D, 30, size=(48, 28))
    found, _ = cut_frames(v, size=(24, 14))
    slow_ends = [c for c, s in zip(cuts, steps) if s >= 5]
    return [check("opens hook 2, fast 2, fast 2 (beats at 0.5 s)", steps[:3] == [2, 2, 2], steps[:6], [2, 2, 2]),
            check("breathing steps (≈6 beats ±1) end on downbeats", slow_ends and all(c in down for c in slow_ends), slow_ends, "in downbeats"),
            check("all cuts on the beat grid, gaps >= 0.35 s", all(c in beats for c in cuts) and min(np.diff([0] + cuts)) >= 0.35, cuts[:8], "grid"),
            check("rendered cuts at the planned frames", frame_err(found, [int(round(c * 30)) for c in cuts]) == 0, len(found), len(cuts)),
            check("negative control: the plan is not an every-beat grid", len(cuts) < len(beats) // 2, len(cuts), "< %d" % (len(beats) // 2))], [v]


@card("BEAT-70")
def review_beat_grid(task, wd):
    """Review timeline: a tick every 60/BPM s aligned to the drop (from drop mod beat), downbeats when k % 4 == 0, the drop as a
    blue 'dropline' — renderTL's own loop run in node."""
    src = (VEND / "web" / "static" / "review" / "index.html").read_text(encoding="utf-8")
    line = next(l for l in src.splitlines() if "if (P.audio.bpm)" in l and "beats +=" in l)
    js = Path(wd) / "tl.cjs"
    js.write_text("const P={duration:8,audio:{bpm:120,drop:2.25}};const pct=t=>(t/P.duration*100)+'%%';let beats='';\n%s\nconsole.log(JSON.stringify(beats));"
                  % line.strip(), encoding="utf-8")
    html = json.loads(sh(["node", js], cwd=wd))
    spans = re.findall(r'class="bt ([a-z]*)" style="left:([\d.]+)%', html)
    ts = [float(l) / 100 * 8 for _, l in spans]
    out = Path(wd) / "beat_grid.html"
    out.write_text(html, encoding="utf-8")
    drops = [t for (c, _), t in zip(spans, ts) if c == "dropline"]
    downs = [t for (c, _), t in zip(spans, ts) if c == "down"]
    return [check("ticks every 0.5 s starting at drop mod beat (0.25)", abs(ts[0] - 0.25) < 1e-6 and all(abs(b - a - 0.5) < 1e-6 for a, b in zip(ts, ts[1:])), ts[:4], [0.25, 0.75]),
            check("one dropline at 2.25 s", len(drops) == 1 and abs(drops[0] - 2.25) < 1e-6, drops, [2.25]),
            check("downbeats every 4 beats from the drop", all(abs(((d - 2.25) / 0.5) % 4) < 1e-6 for d in downs) and len(downs) >= 3, downs, "k%4==0"),
            check("negative control: a tick off the drop phase is not marked down", not any(abs(d - 2.75) < 1e-6 for d in downs), downs, "2.75 not down")], [out]


# ───────────────────────── HyperFrames registry beat components ─────────────────────────
REPO = SKILLS.parents[1]
GSAP_LOCAL = VEND / "kit" / "gsap.min.js"


def hf_mount(wd, mounts, w=320, h=180, dur=4.0):
    """`hyperframes add` each registry component, mount instances (id, name, box, start, dur, vars) in one host, render."""
    d = Path(wd) / "hf"
    d.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, DO_NOT_TRACK="1")
    for name in sorted({m[1] for m in mounts}):
        sh(["hyperframes", "add", name, "--dir", d, "--no-clipboard"], cwd=d, env=env)
    shutil.copy(GSAP_LOCAL, d / "gsap.min.js")
    for f in (d / "compositions" / "components").glob("*.html"):
        f.write_text(re.sub(r"https://cdn\.jsdelivr\.net/npm/gsap@[\d.]+/dist/gsap\.min\.js", "gsap.min.js", f.read_text(encoding="utf-8")), encoding="utf-8")
    divs = "".join(
        '<div data-composition-id="%s" class="clip" style="position:absolute;left:%dpx;top:%dpx;width:%dpx;height:%dpx" '
        'data-composition-src="compositions/components/%s.html" data-start="%s" data-duration="%s" data-track-index="%d" '
        "data-variable-values='%s'></div>" % (cid, x, y, bw, bh, name, st, du, i, json.dumps(v))
        for i, (cid, name, (x, y, bw, bh), st, du, v) in enumerate(mounts))
    (d / "index.html").write_text(
        '<!doctype html><html><head><meta charset="utf-8"><script src="gsap.min.js"></script><style>html,body{margin:0;background:#000;'
        'width:%dpx;height:%dpx;overflow:hidden}:root{--accent:#22cc66;--brand:#22cc66}</style></head><body><div id="root" '
        'data-composition-id="main" data-width="%d" data-height="%d" data-duration="%s" data-start="0">%s</div><script>'
        'window.__timelines=window.__timelines||{};window.__timelines["main"]=gsap.timeline({paused:true});</script></body></html>'
        % (w, h, w, h, dur, divs), encoding="utf-8")
    out = Path(wd) / "components.mp4"
    sh(["hyperframes", "render", ".", "-o", out], cwd=d, env=env, timeout=90)
    return out


def _region_luma(v, box, w=320, h=180):
    fr = fx.frames(v, (w // 10, h // 10)).astype(float).mean(axis=3)
    x, y, bw, bh = (b // 10 for b in box)
    return fr[:, y:y + bh, x:x + bw].mean(axis=(1, 2))


def _pulse_starts(lum, fps=30):
    base = np.median(lum)
    on = lum > base + 0.5 * (lum.max() - base)
    return [i / fps for i in range(1, len(on)) if on[i] and not on[i - 1]]


def _bpb_checks(v, box, beats, wrong):
    lum = _region_luma(v, box)
    st = _pulse_starts(lum)
    near = lambda ts: [min((abs(s - t) for s in st), default=9) for t in ts]
    return [check("pulse starts within 2 frames of every configured beat", len(st) == len(beats) and max(near(beats)) <= 2 / 30 + 1e-6, st, beats),
            check("pulse lifts the region (peak >= 1.3x the resting level)", lum.max() >= 1.3 * lum.min(), [float(lum.max()), float(lum.min())], ">= 1.3x"),
            check("negative control: no pulse at the default/unconfigured beat times", min(near(wrong)) > 3 / 30, near(wrong), "> 3 frames")]


@card("BEAT-111")
def hf_beat_pulse_background(task, wd):
    """`hyperframes add beat-pulse-background`, mounted via data-composition-src with data-variable-values {beats, intensity:club};
    the opacity pulse (attack .08 s, decay .36 s) must start on each listed beat."""
    box = (0, 0, 320, 180)
    v = hf_mount(wd, [("pa", "beat-pulse-background", box, 0, 4, {"beats": "0.5,1.7,2.9", "intensity": "club"})])
    return _bpb_checks(v, box, [0.5, 1.7, 2.9], [1.0, 1.5, 2.5, 3.5]), [v]


@card("BEAT-109")
def hf_beats_to_pulse(task, wd):
    """hyperframes beats (beat JSON from the music) → registry beat-pulse-background driven by those beat times."""
    x, ta = drum_loop(100, 6.0)
    d = Path(wd) / "proj"
    hf_project(d, '<audio id="music" data-timeline-role="music" class="clip" src="track.wav" data-start="0" data-duration="6" data-track-index="0" data-volume="1"></audio>', dur=6)
    save(d, "track.wav", x)
    res = json.loads(hf("beats", ".", "--json", cwd=d))
    times = [round(b["time"], 3) for b in json.loads((d / res["file"]).read_text())["beats"] if 0.2 < b["time"] < 3.6]
    box = (0, 0, 320, 180)
    v = hf_mount(wd, [("pa", "beat-pulse-background", box, 0, 4, {"beats": ",".join(map(str, times)), "intensity": "club"})])
    checks = _bpb_checks(v, box, times, [t + 0.3 for t in times[:-1]])
    return [check("beat JSON at 100 BPM", abs(res["bpm"] - 100) <= 1, res["bpm"], 100)] + checks, [v, d / res["file"]]


@card("BEAT-110")
def hf_beat_accent(task, wd):
    """`hyperframes add beat-accent` mounted at data-start 1.5: the impact flash lands IMPACT_AT 0.25 s into the clip, then the
    HOLD stays calm."""
    box = (0, 0, 320, 180)
    v = hf_mount(wd, [("acc", "beat-accent", box, 1.5, 2.0, {"text": "HIT"})], dur=4.0)
    lum = _region_luma(v, box)
    seg = lum[45:]
    pk = (45 + int(np.argmax(seg))) / 30
    hold = lum[int(2.6 * 30):int(3.0 * 30)]
    return [check("flash peak 0.25 s after the clip start (1.75 s, ±2 frames)", abs(pk - 1.75) <= 2 / 30 + 1e-6, pk, 1.75),
            check("flash brighter than the hold by >= 30 %", lum.max() >= 1.3 * hold.mean(), [float(lum.max()), float(hold.mean())], ">= 1.3x"),
            check("hold is still (frame-to-frame change < 1 level)", np.abs(np.diff(hold)).max() < 1.0, float(np.abs(np.diff(hold)).max()), "< 1"),
            check("negative control: nothing flashes before the clip starts", lum[:44].max() - lum[:44].min() < 1.0, float(lum[:44].max() - lum[:44].min()), "< 1")], [v]


GAPS["BEAT-81"] = ("templates/audio-reactive.html renders here (render_html.cjs stills), but the measured disc did not follow the band data "
                   "as documented (quiet-bass still 166 px wide vs loud-bass still 150 px); cause unresolved, so no runner is registered")
GAPS["BEAT-154"] = ("verse.py builds the project and HyperFrames renders it (~6 s), but the kick response is a 0.14-alpha halo swell inside the "
                    "global fade; no robust known-answer measurement with a negative control fits the 15 s budget")
GAPS["BEAT-104"] = "draw() of the Basma browser editor (S.kind 'audio' presets) needs the whole app state and DOM canvas; no headless entry point"
GAPS["BEAT-184"] = "noise-displaced emissive fireball sphere is a WebGL/three.js scene; no GPU scene render here"
