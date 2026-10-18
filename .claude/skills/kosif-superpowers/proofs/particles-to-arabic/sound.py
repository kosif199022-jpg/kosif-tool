#!/usr/bin/env python3
"""Synthesized score for particles-to-arabic (10 s, 48 kHz stereo, -14 LUFS).
Cue times mirror the T table in index.html. Seeded = identical WAV every run.
usage: python3 sound.py out/master.wav     (needs numpy, scipy, soundfile, pyloudnorm)
"""
import sys
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import soundfile as sf
import pyloudnorm as pyln
from scipy.signal import butter, sosfilt

SR, DUR, SEED = 48000, 10.0, 20261016
n = int(SR * DUR)
t = np.arange(n) / SR
rng = np.random.default_rng(SEED)


def env(a, b, c, d):
    """trapezoid: 0 before a, rises to 1 at b, holds, falls to 0 at d"""
    return np.clip(np.minimum((t - a) / max(1e-6, b - a), (d - t) / max(1e-6, d - c)), 0, 1)


def bp(x, lo, hi):
    return sosfilt(butter(2, [lo, hi], btype='band', fs=SR, output='sos'), x)


L = np.zeros(n); R = np.zeros(n)

# 1) pad: A minor add9, slow fade in, ducks at the burst, returns for the end card
pad = np.zeros(n)
for f, a in [(110, .5), (164.8, .35), (220, .3), (261.6, .22), (329.6, .18), (493.9, .08)]:
    pad += a * (np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * f * 1.003 * t + 1))
pad *= env(0, 2.5, 6.9, 7.3) * .10 + env(8.3, 9.0, 9.6, 10.0) * .07
L += pad; R += pad

# 2) drifting sparkle: seeded tiny clicks through a high band, density follows the drift phase
clicks = np.zeros(n)
for k in rng.integers(0, int(SR * 5.0), 900):
    clicks[k] += rng.uniform(-1, 1)
sp = bp(clicks, 4000, 11000) * env(0, 0.8, 3.5, 5.0) * .9
pan = rng.uniform(0, 1)
L += sp * .8; R += np.roll(sp, 37) * .8

# 3) attraction whoosh: noise through a band that sweeps up 300 Hz → 3 kHz (2.2–5.0 s)
noise = rng.standard_normal(n)
w = np.zeros(n)
for i, (a0, a1) in enumerate(zip(np.linspace(2.2, 4.8, 14)[:-1], np.linspace(2.2, 4.8, 14)[1:])):
    f = 300 * (10 ** (i / 13))
    seg = env(a0 - .25, a0, a1, a1 + .25)
    w += bp(noise, f, f * 1.6) * seg
w *= env(2.2, 4.6, 4.8, 5.15) * .5
L += w; R += np.roll(w, 120)

# 4) formation chime (5.0 s) and light-sweep shimmer (5.15–6.55 s)
def bell(t0, f0, amp, decay=1.6):
    x = np.zeros(n); m = t >= t0; tt = t[m] - t0
    for ratio, a in [(1, 1), (2.76, .45), (5.4, .25), (8.93, .12)]:
        x[m] += a * np.sin(2 * np.pi * f0 * ratio * tt) * np.exp(-tt * decay * ratio ** .5)
    return x * amp
ch = bell(5.0, 880, .22) + bell(5.08, 1318.5, .14)
L += ch; R += np.roll(ch, 240)
sh = bp(noise, 6000, 12000) * env(5.15, 5.6, 6.1, 6.55) * .25 * (0.6 + .4 * np.sin(2 * np.pi * 9 * t))
L += np.roll(sh, 300); R += sh

# 5) anticipation: reverse swell 6.85–7.3 (exponential rise, cut dead at the burst)
rs = bp(noise, 500, 5000) * np.where((t > 6.85) & (t < 7.3), np.exp((t - 7.3) * 7), 0) * .9
L += rs; R += rs

# 6) burst at 7.3 s: sub drop 70 → 38 Hz + broadband crack
m = t >= 7.3; tt = t[m] - 7.3
boom = np.zeros(n)
ph = 2 * np.pi * np.cumsum(38 + 32 * np.exp(-tt * 6)) / SR
boom[m] = np.sin(ph) * np.exp(-tt * 2.2) * .55
crack = np.zeros(n); crack[m] = noise[m] * np.exp(-tt * 9) * .7
crack = bp(crack, 120, 9000)
L += boom + crack; R += boom + np.roll(crack, 90)

# 7) embers: sparse crackle with fading density 7.4–9.6 s
em = np.zeros(n)
for _ in range(500):
    k = int(SR * (7.35 + rng.exponential(.7)))
    if k < n - 200:
        em[k:k + 60] += rng.uniform(-1, 1) * np.exp(-np.arange(60) / 9)
em = bp(em, 1500, 9000) * .6
L += em; R += np.roll(em, 53)

# 8) end card chime
ec = bell(8.5, 659.3, .16, 1.2) + bell(8.62, 987.8, .1, 1.2)
L += ec; R += np.roll(ec, 200)

mix = np.stack([L, R], 1)
mix[: 480] *= np.linspace(0, 1, 480)[:, None]; mix[-4800:] *= np.linspace(1, 0, 4800)[:, None]
meter = pyln.Meter(SR)
mix = pyln.normalize.loudness(mix, meter.integrated_loudness(mix), -14.0)
ceil = 10 ** (-3.0 / 20)                     # soft limiter: tanh knee at -3 dBFS, re-normalise, repeat
for _ in range(8):
    mix = pyln.normalize.loudness(mix, meter.integrated_loudness(mix), -14.0)
    mix = ceil * np.tanh(mix / ceil)
sf.write(sys.argv[1] if len(sys.argv) > 1 else 'master.wav', mix.astype(np.float32), SR, subtype='PCM_24')
print('LUFS', round(meter.integrated_loudness(mix), 2), 'peak dBFS', round(20 * np.log10(np.max(np.abs(mix))), 2))
