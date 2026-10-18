#!/usr/bin/env python3
"""Whiteboard Draw — procedural marker foley driven by the same schedule as the picture.

usage:  node scene.js > schedule.json && python sound.py schedule.json out.wav

Layers (all seeded, 48 kHz stereo, exactly `duration` s):
  * felt-tip scribble per stroke: band-passed noise (1.6–5.5 kHz squeak + 350–1100 Hz felt body) whose level follows
    the pen speed e'(u) = 0.55·(π/2)·sin(πu) + 0.45 — the same easing the picture uses;
    hatching adds a zig-zag tremolo, Arabic writing a 7 Hz tremolo (the pen wiggle frequency in index.html)
  * pen-down tap at every stroke start, softer lift tick at the end
  * double cap click when the marker colour changes
  * quiet room tone
Panned with the pen's x position; normalised to -14 LUFS with a -2.5 dBTP true-peak limiter (4× oversampled).
"""
import json, sys
import numpy as np
import soundfile as sf
import pyloudnorm as pyln
from scipy.signal import butter, sosfilt, resample_poly
from scipy.ndimage import minimum_filter1d

SR = 48000
sched = json.load(open(sys.argv[1]))
DUR = float(sched["duration"]); N = int(round(SR * DUR))
rng = np.random.default_rng(20261016)
L = np.zeros(N); R = np.zeros(N)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], btype="band", fs=SR, output="sos"), x)


def add(sig, t0, pan):
    """add mono `sig` at time t0 with constant-power pan (-1 … 1)."""
    i0 = int(round(t0 * SR)); i1 = min(N, i0 + len(sig))
    if i1 <= i0: return
    a = (pan + 1) * np.pi / 4
    L[i0:i1] += sig[: i1 - i0] * np.cos(a); R[i0:i1] += sig[: i1 - i0] * np.sin(a)


def panx(x): return float(np.clip((x / 1080 - 0.5) * 0.7, -0.6, 0.6))


def tap(level, bright=1.0):
    n = int(0.05 * SR); tt = np.arange(n) / SR
    click = bp(rng.standard_normal(n), 1800, 7000) * np.exp(-tt / 0.004) * bright
    thump = np.sin(2 * np.pi * 190 * tt) * np.exp(-tt / 0.018)
    return level * (0.6 * click + 0.5 * thump)


prev_ink = None
for it in sched["items"]:
    t0, t1 = it["t0"], it["t1"]; d = t1 - t0
    n = int(round(d * SR)); tt = np.arange(n) / SR; u = tt / d
    vel = 0.55 * 0.5 * np.pi * np.sin(np.pi * u) + 0.45
    env = vel / vel.max() * np.minimum(1, u / 0.04) * np.minimum(1, (1 - u) / 0.06)
    if it["type"] == "text":
        env *= 0.55 + 0.45 * np.abs(np.sin(2 * np.pi * 7 * tt))
    elif it["hatch"]:
        zz = max(4, it["L"] / 150) / d                    # ≈ number of chords per second
        env *= 0.45 + 0.55 * np.abs(np.sin(np.pi * zz * tt))
    noise = rng.standard_normal(n + 2000)
    squeak = bp(noise, 1600, 5500)[2000:]
    body = bp(noise, 350, 1100)[2000:]
    # a faint resonant squeal that wanders with speed (felt on melamine)
    f = 2300 + 600 * vel + 120 * np.sin(2 * np.pi * 3.1 * tt)
    squeal = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.08
    lvl = 0.16 if it["hatch"] else 0.2
    sig = lvl * env * (0.75 * squeak + 0.55 * body + squeal)
    pan0, pan1 = panx(it["x0"]), panx(it["x1"])
    # pan follows the pen across the stroke (split in 8 chunks)
    for k in range(8):
        a, b = k * n // 8, (k + 1) * n // 8
        add(sig[a:b], t0 + a / SR, pan0 + (pan1 - pan0) * (k + 0.5) / 8)
    add(tap(0.3), t0 - 0.004, pan0)
    add(tap(0.18, 0.5), t1, pan1)
    if prev_ink and prev_ink != it["ink"]:
        add(tap(0.35, 1.6), t0 - 0.16, pan0); add(tap(0.28, 1.6), t0 - 0.1, pan0)
    prev_ink = it["ink"]

room = bp(rng.standard_normal(N), 80, 900) * 0.004
L += room; R += room
st = np.stack([L, R], 1)
st[: int(0.02 * SR)] *= np.linspace(0, 1, int(0.02 * SR))[:, None]
st[-int(0.3 * SR):] *= np.linspace(1, 0, int(0.3 * SR))[:, None] ** 2
meter = pyln.Meter(SR)


def limit(x, ceil_db=-2.5):
    """true-peak limiter: 4× oversampled peak → gain curve (1.5 ms look-ahead, 40 ms release, zero-phase)."""
    os_ = resample_poly(x, 4, 1, axis=0)
    env = np.abs(os_).max(1).reshape(-1, 4).max(1)[: len(x)]
    g = np.minimum(1.0, 10 ** (ceil_db / 20) / np.maximum(env, 1e-9))
    g = minimum_filter1d(g, size=int(0.003 * SR))
    a = np.exp(-1 / (0.04 * SR))
    fw = g.copy(); bw = g.copy()                                # instant attack, 40 ms release, both directions
    for i in range(1, len(g)): fw[i] = min(g[i], a * fw[i - 1] + (1 - a) * g[i])
    for i in range(len(g) - 2, -1, -1): bw[i] = min(g[i], a * bw[i + 1] + (1 - a) * g[i])
    g = np.minimum(fw, bw)
    return x * g[:, None]


for _ in range(4):                                     # loudness → true-peak limit → re-measure
    st = pyln.normalize.loudness(st, meter.integrated_loudness(st), -14.0)
    st = limit(st)
tp = 20 * np.log10(np.abs(resample_poly(st, 4, 1, axis=0)).max())
print(f"LUFS {meter.integrated_loudness(st):.2f}  true peak {tp:.2f} dBTP  {len(st)/SR:.3f} s")
sf.write(sys.argv[2], st.astype(np.float32), SR, subtype="PCM_24")
