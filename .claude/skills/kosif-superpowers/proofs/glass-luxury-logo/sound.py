#!/usr/bin/env python3
"""Glass Luxury Logo — procedural score synced to the film's cue times (see CUES, same numbers as index.html).

Warm D-add9 pad swell, panned whooshes for each glass card (side = the side it enters from), a wide whoosh
when the cards part, a low boom under the logotype reveal, a bell chime + sparkle when the emblem closes,
and a glassy rising shimmer with each metallic sweep. 48 kHz stereo, exactly 10 s, -14 LUFS, peak <= -1.5 dBFS.
Deterministic (seeded).  usage: python sound.py <out.wav>
"""
import sys
import numpy as np
import soundfile as sf
import pyloudnorm as pyln
from scipy.signal import butter, sosfilt

SR, DUR = 48000, 10.0
N = int(SR * DUR)
t = np.arange(N) / SR
rng = np.random.default_rng(7022026)
CUES = {
    "cards": [(0.30, -0.8), (0.48, 0.8), (0.66, -0.6), (0.84, 0.6)],  # (start s, pan -1..1) — CARDS[].t0
    "part": 3.25,            # PART[0]
    "reveal": 4.9,           # T_WORD[0]
    "emblem_done": 5.45,     # dust burst / sparkle
    "shine": [(6.45, 1.0), (8.85, 0.55)],  # T_SHINE
}
L = np.zeros(N); R = np.zeros(N)


def put(sig, start, pan=0.0, gain=1.0):
    i = int(start * SR); n = min(len(sig), N - i)
    if n <= 0:
        return
    a = (pan + 1) * np.pi / 4
    L[i:i + n] += sig[:n] * np.cos(a) * gain; R[i:i + n] += sig[:n] * np.sin(a) * gain


def sweep_noise(dur, f0, f1, f2):
    """noise through a one-pole low-pass whose cutoff rises f0→f1 then falls to f2 (a whoosh)"""
    n = int(dur * SR); x = rng.standard_normal(n); y = np.zeros(n); s = 0.0
    k = np.arange(n) / n
    fc = np.where(k < 0.45, f0 + (f1 - f0) * (k / 0.45), f1 + (f2 - f1) * ((k - 0.45) / 0.55))
    a = 1 - np.exp(-2 * np.pi * fc / SR)
    for i in range(n):
        s += a[i] * (x[i] - s); y[i] = s
    env = np.sin(np.pi * k) ** 2
    return sosfilt(butter(2, 120, "high", fs=SR, output="sos"), y * env)


# ---- pad: D2 A2 D3 F#3 E4 with slow chorus, swells in, breathes, fades at the very end
pad = np.zeros(N)
for f, a in [(73.42, 0.9), (110.0, 0.6), (146.83, 0.5), (185.0, 0.35), (329.63, 0.18)]:
    for det in (-0.6, 0.6):
        pad += a * np.sin(2 * np.pi * (f + det) * t + rng.uniform(0, 6.28))
pad = sosfilt(butter(2, 900, "low", fs=SR, output="sos"), pad)
env = np.clip(t / 3.0, 0, 1) ** 1.3 * (1 + 0.6 * np.clip((t - 4.9) / 1.5, 0, 1)) * (1 - np.clip((t - 9.5) / 0.5, 0, 1))
put(pad * env * 0.06, 0)

# ---- card whooshes and the parting whoosh
for start, pan in CUES["cards"]:
    put(sweep_noise(0.9, 300, 2600, 500), start - 0.05, pan, 0.11)
w = sweep_noise(1.4, 200, 1800, 300)
put(w, CUES["part"], -0.5, 0.16); put(w[::-1].copy(), CUES["part"] + 0.05, 0.5, 0.12)

# ---- low boom under the reveal
k = np.arange(int(2.0 * SR)) / SR
boom = np.sin(2 * np.pi * (58 * np.exp(-k * 1.2) + 32) * k) * np.exp(-k * 2.2)
boom += sosfilt(butter(2, 180, "low", fs=SR, output="sos"), rng.standard_normal(len(k))) * np.exp(-k * 18) * 0.6
put(boom, CUES["reveal"] - 0.05, 0, 0.5)

# ---- bell chime + sparkle when the emblem closes
k = np.arange(int(3.0 * SR)) / SR
bell = sum(a * np.sin(2 * np.pi * 880 * r * k) * np.exp(-k * d) for r, a, d in [(1, 1, 1.6), (2.756, 0.5, 2.4), (5.404, 0.28, 3.5), (8.933, 0.14, 5)])
put(bell * np.minimum(1, k / 0.004), CUES["emblem_done"], 0.1, 0.06)
for _ in range(40):
    f = rng.uniform(3500, 9000); n = int(0.08 * SR); kk = np.arange(n) / SR
    put(np.sin(2 * np.pi * f * kk) * np.exp(-kk * 60), CUES["emblem_done"] + rng.uniform(0, 1.2), rng.uniform(-0.8, 0.8), rng.uniform(0.004, 0.012))

# ---- glassy rising shimmer with each metallic sweep (pans left → right like the light band)
for start, g in CUES["shine"]:
    n = int(1.3 * SR); kk = np.arange(n) / SR; p = kk / kk[-1]
    sh = sum(np.sin(2 * np.pi * np.cumsum(f0 * (1 + 0.5 * p)) / SR) for f0 in (1760, 2637, 3520))
    sh *= np.sin(np.pi * p) ** 2
    i = int(start * SR); m = min(n, N - i)
    pan = -0.7 + 1.4 * p[:m]
    L[i:i + m] += sh[:m] * np.cos((pan + 1) * np.pi / 4) * 0.012 * g; R[i:i + m] += sh[:m] * np.sin((pan + 1) * np.pi / 4) * 0.012 * g

# ---- master
mix = np.stack([L, R], axis=1)
mix[:int(0.01 * SR)] *= np.linspace(0, 1, int(0.01 * SR))[:, None]
mix[-int(0.03 * SR):] *= np.linspace(1, 0, int(0.03 * SR))[:, None]
meter = pyln.Meter(SR); ceiling = 10 ** (-1.5 / 20)
for _ in range(4):
    mix = pyln.normalize.loudness(mix, meter.integrated_loudness(mix), -14.0)
    if np.max(np.abs(mix)) <= ceiling:
        break
    mix = ceiling * np.tanh(mix / ceiling)
print(f"loudness {meter.integrated_loudness(mix):.2f} LUFS, peak {20 * np.log10(np.max(np.abs(mix))):.2f} dBFS, {len(mix) / SR:.3f} s")
sf.write(sys.argv[1], mix.astype(np.float32), SR, subtype="PCM_24")
