#!/usr/bin/env python3
"""Neon Glow — procedural sound design synced to the same ignition schedule as the picture.

Reads schedule.js (JSON after "window.NEON_SCHEDULE ="), writes a 48 kHz stereo WAV of exactly
`duration` seconds, loudness-normalised to -14 LUFS (EBU R128) with a -1.5 dBFS sample-peak ceiling.

Layers: rain bed + drops, 120 Hz neon hum (+ harmonics) whose level follows the lit tubes,
ignition crackles on every rising edge, the faulty "T" buzz, a rising fizz while the cup draws on,
relay ticks of the steam chaser, and a wet-tyre car pass panned left → right with the headlight sweep.
Deterministic: every random source is seeded.

usage: python sound.py <out.wav>
"""
import json, re, sys, pathlib
import numpy as np
import soundfile as sf
import pyloudnorm as pyln
from scipy.signal import butter, sosfilt

HERE = pathlib.Path(__file__).resolve().parent
S = json.loads(re.search(r"^window\.NEON_SCHEDULE = (\{.*\})\s*;", (HERE / "schedule.js").read_text(), re.S | re.M).group(1))
SR, DUR = 48000, float(S["duration"])
N = int(round(SR * DUR))
t = np.arange(N) / SR
rng = np.random.default_rng(20261016)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], btype="band", fs=SR, output="sos"), x)


def lp(x, f, order=2):
    return sosfilt(butter(order, f, btype="low", fs=SR, output="sos"), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f, btype="high", fs=SR, output="sos"), x)


def seg_level(segs, tt, warm=S["warmup"]):
    out = np.zeros_like(tt)
    for a, b, v in segs:
        m = (tt >= a) & (tt < b)
        if b >= 99:
            out[m] = v * (0.78 + 0.22 * (1 - (1 - np.clip((tt[m] - a) / warm, 0, 1)) ** 3))
        else:
            out[m] = v
    return out


def shift(segs, s):
    return [[a + s, 99 if b >= 99 else b + s, v] for a, b, v in segs]


letters = [c for c in "OPEN LATE" if c != " "]
lat_segs = []
for i, _ in enumerate(letters):
    s0 = S["latinStart"] + i * S["latinStep"]
    lat_segs.append(shift(S["faulty"]["pattern"] if i == S["faulty"]["index"] else S["latinPattern"], s0))
ar = seg_level(S["arabic"], t)
lat = [seg_level(sg, t) for sg in lat_segs]
fi = S["faulty"]["index"]
for a, b, d in S["faulty"]["dropouts"]:
    lat[fi][(t >= a) & (t < b)] = d
cup_on = np.clip((t - S["cup"]["body"][0]) / (S["cup"]["saucer"][1] - S["cup"]["body"][0]), 0, 1)
lit = 0.5 * ar + 0.3 * np.mean(lat, axis=0) + 0.2 * cup_on
L = np.zeros(N); R = np.zeros(N)

# ---- rain bed (decorrelated L/R) + drops
for ch in (L, R):
    n = rng.standard_normal(N)
    ch += 0.05 * bp(n, 500, 7000) + 0.03 * lp(rng.standard_normal(N), 400)
for _ in range(260):
    at = rng.uniform(0, DUR); f = rng.uniform(1800, 5200); dur = 0.012
    k = np.arange(int(dur * SR)); i0 = int(at * SR)
    if i0 + len(k) >= N:
        continue
    blip = np.sin(2 * np.pi * f * k / SR) * np.exp(-k / (0.0025 * SR)) * rng.uniform(0.02, 0.07)
    pan = rng.uniform(0, 1)
    L[i0:i0 + len(k)] += blip * (1 - pan); R[i0:i0 + len(k)] += blip * pan

# ---- neon hum: 120 Hz + harmonics, slight shimmer, follows how much glass is lit
hum = sum(a * np.sin(2 * np.pi * 120 * h * t + h) for h, a in [(1, 1.0), (2, 0.5), (3, 0.32), (4, 0.2), (5, 0.12), (8, 0.05)])
hum *= 1 + 0.04 * np.sin(2 * np.pi * 4.7 * t)
buzz = hp(np.sign(np.sin(2 * np.pi * 120 * t)) * 0.3, 1500) * rng.uniform(0.9, 1.1, N)
hum_env = lp(lit, 30)
L += 0.035 * hum * hum_env + 0.01 * buzz * hum_env
R += 0.035 * hum * hum_env + 0.01 * buzz * hum_env


# ---- ignition crackles on every rising edge (pink word centre, Latin letters across the stereo field)
def crackles(level, pan, gain):
    d = np.diff(level, prepend=0)
    for i in np.where(d > 0.2)[0]:
        n = int(0.03 * SR)
        if i + n >= N:
            continue
        k = np.arange(n)
        burst = hp(rng.standard_normal(n), 2500) * np.exp(-k / (0.006 * SR)) * d[i] * gain
        burst[:40] += np.linspace(gain * 2.0, 0, 40) * d[i]       # relay "tick"
        L[i:i + n] += burst * (1 - pan); R[i:i + n] += burst * pan


crackles(ar, 0.5, 0.18)
for j, lv in enumerate(lat):
    crackles(lv, 0.25 + 0.5 * j / (len(lat) - 1), 0.12)

# ---- the faulty T buzzes while it flickers (before it settles and during its dropout)
s_t = S["latinStart"] + fi * S["latinStep"]
zone = ((t >= s_t) & (t < s_t + 1.5)) | ((t >= 7.78) & (t < 8.0))
zz = bp(np.sign(np.sin(2 * np.pi * 120 * t)) * rng.uniform(0.7, 1.0, N), 300, 4000) * zone * 0.06
zz = lp(zz, 6000)
pan_t = 0.25 + 0.5 * fi / (len(lat) - 1)
L += zz * (1 - pan_t); R += zz * pan_t

# ---- cup draw-on: rising gas fizz 3.4 → 4.65 s
a0, a1 = S["cup"]["body"][0], S["cup"]["saucer"][1]
m = (t >= a0) & (t < a1 + 0.15)
fz = np.zeros(N)
seg = rng.standard_normal(m.sum())
p = (t[m] - a0) / (a1 - a0)
fz[m] = (bp(seg, 900, 2600) * 0.6 + bp(seg, 2600, 7000) * 0.4 * np.clip(p, 0, 1)) * np.sin(np.pi * np.clip(p, 0, 1)) ** 0.6 * 0.05
L += fz * 0.55; R += fz * 0.45

# ---- steam chaser relay ticks
st = S["steam"]
for k in range(int((DUR - st["start"]) / st["step"]) + 1):
    i = int((st["start"] + k * st["step"]) * SR)
    if i + 300 < N:
        tick = np.exp(-np.arange(300) / 40.0) * 0.05 * rng.choice([-1, 1])
        L[i:i + 300] += tick * 0.4; R[i:i + 300] += tick * 0.6

# ---- car pass on a wet street, panned with the headlight sweep
c0, c1 = S["sweep"]
m = (t >= c0 - 0.6) & (t < c1 + 0.6)
pc = np.clip((t - (c0 - 0.6)) / (c1 - c0 + 1.2), 0, 1)
env = np.sin(np.pi * pc) ** 2 * m
tyre = bp(rng.standard_normal(N), 350, 3800) * 0.22 + lp(rng.standard_normal(N), 150) * 0.25
eng = np.sin(2 * np.pi * (52 + 10 * pc) * t) * 0.05
car = (tyre + eng) * env
pan = np.clip((t - c0) / (c1 - c0), 0, 1)
L += car * np.cos(pan * np.pi / 2); R += car * np.sin(pan * np.pi / 2)

# ---- fade in with the picture, master, loudness
fade = np.clip(t / S["fadeIn"], 0, 1) ** 2
mix = np.stack([L * fade, R * fade], axis=1)
mix[-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR))[:, None]
meter = pyln.Meter(SR)
for _ in range(4):
    mix = pyln.normalize.loudness(mix, meter.integrated_loudness(mix), -14.0)
    peak = np.max(np.abs(mix))
    ceiling = 10 ** (-1.5 / 20)
    if peak <= ceiling:
        break
    mix = ceiling * np.tanh(mix / ceiling)  # soft clip, then measure again
print(f"loudness {meter.integrated_loudness(mix):.2f} LUFS, peak {20 * np.log10(np.max(np.abs(mix))):.2f} dBFS, {len(mix) / SR:.3f} s")
sf.write(sys.argv[1], mix.astype(np.float32), SR, subtype="PCM_24")
