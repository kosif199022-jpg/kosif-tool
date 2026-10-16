#!/usr/bin/env python3
"""Character Rig — procedural foley from the motion events (no recordings).

usage:  node motion.js > events.json && python sound.py events.json out.wav

  * step     : gravel crunch (band-passed noise 0.9–6 kHz, 60 ms) + soft heel thump (95 Hz, 70 ms), level ∝ walking speed
  * notice   : two-note "huh?" rising sine blip (520 → 780 Hz)
  * crouch   : cloth rustle swell
  * takeoff  : whoosh — noise through a band-pass that sweeps 400 → 2600 Hz over 0.45 s
  * land     : thump (62 Hz, 180 ms) + gravel burst
  * bubble   : pop (sine 900 → 300 Hz in 60 ms)
  * word     : wordless "voice" — 3 formant blips per word (vowel formants, pitch 190–260 Hz), never real speech
  * bed      : soft wind (low-passed noise with slow gusts)
Panned by world x relative to the camera path; -14 LUFS, -2.5 dBTP true-peak limiter (4× oversampled).
"""
import json, sys
import numpy as np
import soundfile as sf
import pyloudnorm as pyln
from scipy.signal import butter, sosfilt, resample_poly
from scipy.ndimage import minimum_filter1d

SR = 48000
ev = json.load(open(sys.argv[1]))
DUR = float(ev["duration"]); N = int(round(SR * DUR))
rng = np.random.default_rng(20261016)
L = np.zeros(N); R = np.zeros(N)


def bp(x, lo, hi, order=2): return sosfilt(butter(order, [lo, hi], btype="band", fs=SR, output="sos"), x)
def lp(x, f, order=2): return sosfilt(butter(order, f, btype="low", fs=SR, output="sos"), x)


def add(sig, t0, pan=0.0):
    i0 = int(round(t0 * SR)); i1 = min(N, i0 + len(sig))
    if i1 <= i0 or i0 < 0: return
    a = (np.clip(pan, -1, 1) + 1) * np.pi / 4
    L[i0:i1] += sig[: i1 - i0] * np.cos(a); R[i0:i1] += sig[: i1 - i0] * np.sin(a)


def tt(d): return np.arange(int(d * SR)) / SR


def crunch(level):
    t = tt(0.09); n = bp(rng.standard_normal(len(t)), 900, 6000) * np.exp(-t / 0.018)
    grains = (rng.random(len(t)) < 0.004) * rng.standard_normal(len(t)) * 3
    th = np.sin(2 * np.pi * 95 * t) * np.exp(-t / 0.025)
    return level * (0.5 * n + 0.25 * bp(grains, 1500, 7000) + 0.6 * th)


def blip(f0, f1, d, level):
    t = tt(d); f = np.linspace(f0, f1, len(t))
    return level * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d) ** 2


FORMANTS = [(700, 1220), (300, 2300), (450, 900), (600, 1700), (350, 1900)]   # a, i, u, e-ish, o-ish
def syllable(pitch, vowel, d=0.11, level=0.35):
    t = tt(d); f = pitch * (1 + 0.06 * np.sin(np.pi * t / d))
    ph = 2 * np.pi * np.cumsum(f) / SR
    src = sum(np.sin(k * ph) / k for k in range(1, 18))                    # bright glottal-ish source
    f1, f2 = FORMANTS[vowel % len(FORMANTS)]
    v = bp(src, f1 * 0.8, f1 * 1.2) * 1.0 + bp(src, f2 * 0.85, f2 * 1.15) * 0.6
    env = np.minimum(1, t / 0.012) * np.minimum(1, (d - t) / 0.03)
    return level * v * env


# camera x roughly follows the hero: pan relative to the event position at its own time
def pan_for(e): return 0.0 if e["type"] == "word" else float(np.clip((e["x"] % 400 - 200) / 900, -0.25, 0.25))


k = 0
for e in ev["events"]:
    t0, ty = e["t"], e["type"]
    if ty == "step": add(crunch(0.55 * (0.4 + 0.6 * e.get("v", 1))), t0, pan_for(e))
    elif ty == "notice": add(blip(520, 560, 0.09, 0.3), t0); add(blip(600, 800, 0.14, 0.3), t0 + 0.1)
    elif ty == "crouch":
        t = tt(0.45); add(0.25 * bp(rng.standard_normal(len(t)), 1200, 5000) * np.sin(np.pi * t / 0.45) ** 2, t0)
    elif ty == "takeoff":
        t = tt(0.5); n = rng.standard_normal(len(t)); out = np.zeros_like(n)
        for i in range(10):                                                 # stepped sweep 400 → 2600 Hz
            a, b = i * len(t) // 10, (i + 1) * len(t) // 10; fc = 400 * (6.5 ** (i / 9))
            out[a:b] = bp(n, fc * 0.7, fc * 1.4)[a:b]
        add(0.7 * out * np.sin(np.pi * t / 0.5) ** 1.5, t0 - 0.05); add(crunch(0.5), t0, -0.1)
    elif ty == "land":
        t = tt(0.25); add(0.9 * np.sin(2 * np.pi * 62 * t * (1 - 0.3 * t)) * np.exp(-t / 0.06), t0)
        add(crunch(0.8), t0); add(crunch(0.5), t0 + 0.03, 0.15)
    elif ty == "bubble": add(blip(900, 300, 0.07, 0.45), t0 + 0.02)
    elif ty == "word":
        for s in range(3):
            add(syllable(205 + 30 * np.sin(k * 1.7) + (25 if e["w"].endswith("!") and s == 2 else 0), k), t0 + s * 0.1); k += 1

wind = lp(rng.standard_normal(N), 500) * (0.5 + 0.5 * np.sin(2 * np.pi * np.arange(N) / SR * 0.21) ** 2) * 0.05
L += wind; R += np.roll(wind, 900)
st = np.stack([L, R], 1)
st[: int(0.3 * SR)] *= np.linspace(0, 1, int(0.3 * SR))[:, None]
st[-int(0.25 * SR):] *= np.linspace(1, 0, int(0.25 * SR))[:, None]


def limit(x, ceil_db=-2.5):
    os_ = resample_poly(x, 4, 1, axis=0)
    env = np.abs(os_).max(1).reshape(-1, 4).max(1)[: len(x)]
    g = minimum_filter1d(np.minimum(1.0, 10 ** (ceil_db / 20) / np.maximum(env, 1e-9)), size=int(0.003 * SR))
    a = np.exp(-1 / (0.04 * SR)); fw = g.copy(); bw = g.copy()
    for i in range(1, len(g)): fw[i] = min(g[i], a * fw[i - 1] + (1 - a) * g[i])
    for i in range(len(g) - 2, -1, -1): bw[i] = min(g[i], a * bw[i + 1] + (1 - a) * g[i])
    return x * np.minimum(fw, bw)[:, None]


meter = pyln.Meter(SR)
for _ in range(4):
    st = limit(pyln.normalize.loudness(st, meter.integrated_loudness(st), -14.0))
tp = 20 * np.log10(np.abs(resample_poly(st, 4, 1, axis=0)).max())
print(f"LUFS {meter.integrated_loudness(st):.2f}  true peak {tp:.2f} dBTP  {len(st)/SR:.3f} s")
sf.write(sys.argv[2], st.astype(np.float32), SR, subtype="PCM_24")
