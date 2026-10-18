#!/usr/bin/env python3
"""Transitions Reel — 120 BPM synthesized bed + one designed SFX per transition, all from reel.js timing.

usage:  node reel.js > reel.json && python sound.py reel.json out.wav

Bed: kick on every beat (sine 150→48 Hz), closed hat on the off-beats, sub-bass on A–F–C–G (one chord per bar),
soft saw pad. SFX are centred on each transition window so the impact lands exactly on the cut:
  iris   rising filtered swish + click at the cut      wipe  band-swept noise (bright → dark, right → left pan)
  zoom   inExpo riser into a boom at the cut           glitch bit-crushed square buzz + random stutters
  whip   fast doppler whoosh (pan left → right)        leak  airy shimmer swell (detuned sines + noise)
  shape  pop + rotating swoosh                         match two-note chime (circle note → square note)
-14 LUFS integrated, -2.5 dBTP true-peak limiter (4× oversampled).
"""
import json, sys
import numpy as np
import soundfile as sf
import pyloudnorm as pyln
from scipy.signal import butter, sosfilt, resample_poly
from scipy.ndimage import minimum_filter1d

SR = 48000
reel = json.load(open(sys.argv[1]))
DUR = float(reel["duration"]); N = int(round(SR * DUR)); BEAT = 60 / reel["bpm"]
rng = np.random.default_rng(20261016)
L = np.zeros(N); R = np.zeros(N)
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], btype="band", fs=SR, output="sos"), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, btype="low", fs=SR, output="sos"), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, btype="high", fs=SR, output="sos"), x)
def tt(d): return np.arange(int(d * SR)) / SR


def add(sig, t0, pan=0.0, pan1=None):
    i0 = int(round(t0 * SR));
    if i0 < 0: sig = sig[-i0:]; i0 = 0
    i1 = min(N, i0 + len(sig)); sig = sig[: i1 - i0]
    p = np.full(len(sig), pan) if pan1 is None else np.linspace(pan, pan1, len(sig))
    a = (np.clip(p, -1, 1) + 1) * np.pi / 4
    L[i0:i1] += sig * np.cos(a); R[i0:i1] += sig * np.sin(a)


# ---------------- bed ----------------
n_beats = int(DUR / BEAT)
for b in range(n_beats):
    t0 = b * BEAT
    t = tt(0.35); f = 48 + 102 * np.exp(-t / 0.035)
    add(0.55 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.16), t0)                # kick
    h = tt(0.05); add(0.12 * hp(rng.standard_normal(len(h)), 7000) * np.exp(-h / 0.012), t0 + BEAT / 2, 0.3)   # hat
ROOTS = [55.0, 43.65, 65.41, 49.0]                 # A1 F1 C2 G1 — one chord per bar (2 s)
CHORDS = [[220, 261.6, 329.6], [174.6, 220, 261.6], [261.6, 329.6, 392], [196, 246.9, 293.7]]
for bar in range(int(np.ceil(DUR / (4 * BEAT)))):
    t0 = bar * 4 * BEAT; d = min(4 * BEAT, DUR - t0)
    if d <= 0: break
    t = tt(d); r = ROOTS[bar % 4]
    env = np.minimum(1, t / 0.02) * np.minimum(1, (d - t) / 0.05)
    # sub-bass pulses on each beat (sidechain feel)
    duck = 1 - 0.7 * np.exp(-((t % BEAT) / 0.09))
    add(0.32 * np.sin(2 * np.pi * r * t) * env * duck, t0)
    pad = sum(sum(2 * ((f * (1 + dt) * t) % 1) - 1 for dt in (-0.004, 0.004)) for f in CHORDS[bar % 4])
    add(0.05 * lp(pad, 1800) * env * duck, t0)

# ---------------- SFX per transition ----------------
def noise(d): return rng.standard_normal(int(d * SR))
def swept(d, f0, f1, bands=12):
    n = noise(d); out = np.zeros_like(n)
    for i in range(bands):
        a, b = i * len(n) // bands, (i + 1) * len(n) // bands; fc = f0 * (f1 / f0) ** (i / (bands - 1))
        out[a:b] = bp(n, fc * 0.7, min(fc * 1.4, 20000))[a:b]
    return out
def chime(f, d=0.6, lvl=0.3):
    t = tt(d); return lvl * (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * 2.76 * f * t) * np.exp(-t / 0.08)) * np.exp(-t / 0.22)

for tr in reel["transitions"]:
    t0, cut, d, kind = tr["t0"], tr["cut"], tr["dur"], tr["id"]
    if kind == "iris":
        s = swept(d, 500, 4000) * np.sin(np.pi * tt(d) / d) ** 2; add(0.5 * s, t0)
        c = tt(0.03); add(0.4 * hp(noise(0.03), 2000) * np.exp(-c / 0.004), cut)
    elif kind == "wipe":
        s = swept(d, 6000, 700) * np.sin(np.pi * tt(d) / d) ** 1.5; add(0.55 * s, t0, 0.6, -0.6)
    elif kind == "zoom":
        rd = d / 2 + 0.25; t = tt(rd); u = t / rd
        riser = swept(rd, 300, 6000, 16) * (2 ** (10 * u - 10)) * 3
        add(0.6 * riser, cut - rd)
        b = tt(0.6); add(0.8 * np.sin(2 * np.pi * (40 + 60 * np.exp(-b / 0.05)) * b) * np.exp(-b / 0.25), cut)
        add(0.25 * lp(noise(0.5), 1200) * np.exp(-tt(0.5) / 0.12), cut)
    elif kind == "glitch":
        t = tt(d); sq = np.sign(np.sin(2 * np.pi * (180 + 900 * (rng.random() )) * t))
        crushed = np.round(sq * 4 + bp(noise(d), 800, 6000) * 3) / 4
        gate = (np.floor(t / 0.022) % 3 != 1).astype(float)
        add(0.22 * crushed * gate * (1 - np.abs(2 * t / d - 1)), t0, -0.3, 0.3)
    elif kind == "whip":
        t = tt(d); k = 1 - np.abs(2 * t / d - 1)
        s = swept(d, 900, 3500) * k ** 2.5; add(0.9 * s, t0, -0.8, 0.8)
    elif kind == "leak":
        t = tt(d + 0.4); k = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.2 * np.minimum(1, (d + 0.4 - t) / 0.4)
        sh = sum(np.sin(2 * np.pi * f * t + i) for i, f in enumerate([1318.5, 1320.8, 1975.5, 1979.0, 2637.0]))
        add(0.08 * sh * k + 0.12 * hp(noise(d + 0.4), 5000) * k, t0)
    elif kind == "shape":
        c = tt(0.08); add(0.5 * np.sin(2 * np.pi * (700 - 400 * c / 0.08) * c) * np.exp(-c / 0.03), cut - d / 2 + 0.02)
        s = swept(d, 1500, 300) * np.sin(np.pi * tt(d) / d); add(0.4 * s, t0, 0.4, -0.4)
    elif kind == "match":
        add(chime(659.3), cut - 0.12); add(chime(987.8, 0.9), cut + 0.05)

# end sting
add(chime(880, 1.0, 0.25), 8.0 + 0.6)

st = np.stack([L, R], 1)
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
