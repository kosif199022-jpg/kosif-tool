"""beat-sync — synthesise a 120 BPM drum loop, detect its beats/onsets with librosa,
write beats.json (+ beats.js for the page). Original code, numpy only for the sound.

usage: python drums.py <out.wav> [<proof dir>]
"""
import json, sys, pathlib
import numpy as np, soundfile as sf, librosa, pyloudnorm as pyln

SR, BPM, BARS, LEAD, TAIL = 48000, 120, 4, 0.5, 0.5
BEAT = 60 / BPM
DUR = LEAD + BARS * 4 * BEAT + TAIL           # 9.0 s
rng = np.random.default_rng(20261016)
n = int(round(DUR * SR))
mix = np.zeros((n, 2))

def place(sig, t, gain=1.0, pan=0.0):
    sig = sig.copy(); k = int(0.02 * SR); sig[-k:] *= np.linspace(1, 0, k) ** 2   # 20 ms release: no end click
    i = int(round(t * SR)); j = min(n, i + len(sig))
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    mix[i:j, 0] += sig[: j - i] * gain * l * 1.414
    mix[i:j, 1] += sig[: j - i] * gain * r * 1.414

def kick():
    t = np.arange(int(0.45 * SR)) / SR
    f = 48 + 110 * np.exp(-t / 0.035)                       # pitch sweep 158 -> 48 Hz
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t / 0.16)
    click = rng.standard_normal(len(t)) * np.exp(-t / 0.003) * 0.35
    return np.tanh(1.6 * (body + click))

def snare():
    t = np.arange(int(0.3 * SR)) / SR
    tone = np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.05) * 0.5
    nz = rng.standard_normal(len(t))
    nz = nz - np.concatenate([[0], nz[:-1]]) * 0.6           # tilt brighter
    return (tone + nz * np.exp(-t / 0.075) * 0.7) * 0.9

def hat(open_=False):
    t = np.arange(int((0.18 if open_ else 0.06) * SR)) / SR
    nz = rng.standard_normal(len(t))
    hp = np.diff(nz, prepend=0); hp = np.diff(hp, prepend=0)  # crude 2nd-order high-pass
    return hp * np.exp(-t / (0.06 if open_ else 0.012)) * 0.18

truth = []
for bar in range(BARS):
    for b in range(4):
        t = LEAD + (bar * 4 + b) * BEAT
        if b in (0, 2): place(kick(), t, 0.95); truth.append((t, 'kick'))
        if b in (1, 3): place(snare(), t, 0.7, 0.05); truth.append((t, 'snare'))
        place(hat(), t, 0.6, 0.3)
        place(hat(open_=(b == 3 and bar % 2 == 1)), t + BEAT / 2, 0.75, 0.3); truth.append((t + BEAT / 2, 'hat'))
# simple bass on the root of each bar, sidechained by the kick shape
roots = [55.0, 55.0, 65.41, 49.0]
tt = np.arange(n) / SR
bass = np.zeros(n)
for bar, f in enumerate(roots):
    a, b = LEAD + bar * 4 * BEAT, LEAD + (bar + 1) * 4 * BEAT
    m = (tt >= a) & (tt < b)
    bass[m] = np.sin(2 * np.pi * f * tt[m]) * 0.22 + np.sin(4 * np.pi * f * tt[m]) * 0.05
duck = np.ones(n)
for t, k in truth:
    if k == 'kick':
        i = int(t * SR); L = int(0.25 * SR); seg = 1 - 0.6 * np.exp(-np.arange(L) / SR / 0.08)
        duck[i:i + L] = np.minimum(duck[i:i + L], seg[: max(0, min(L, n - i))])
fade = np.clip((DUR - tt) / 0.3, 0, 1)
bass *= duck * fade
mix[:, 0] += bass; mix[:, 1] += bass

meter = pyln.Meter(SR)
for _ in range(4):                                          # normalise to -13.4 LUFS (AAC lands ~-14), soft-limit at 0.84 (~ -1.5 dBFS)
    mix = mix * 10 ** ((-13.4 - meter.integrated_loudness(mix)) / 20)
    mix = 0.84 * np.tanh(mix / 0.84)
out = pathlib.Path(sys.argv[1]); sf.write(out, mix.astype(np.float32), SR, subtype='PCM_24')

# ---------------- analysis (what the film is driven by) ----------------
y, sr = librosa.load(out, sr=SR, mono=True)
hop = 128                                                   # 2.67 ms resolution
env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop)
on_f = librosa.onset.onset_detect(onset_envelope=env, sr=sr, hop_length=hop, units='frames', wait=int(0.08 * sr / hop))
on_t = librosa.frames_to_time(on_f, sr=sr, hop_length=hop)
tempo, beat_f = librosa.beat.beat_track(onset_envelope=env, sr=sr, hop_length=hop, units='frames')
beat_t = librosa.frames_to_time(beat_f, sr=sr, hop_length=hop)
tempo = float(np.atleast_1d(tempo)[0])
# per-band spectral flux (low < 150 Hz, mid 150-4000 Hz, high > 6000 Hz) to label each onset
M = librosa.feature.melspectrogram(y=y, sr=sr, hop_length=hop, n_fft=2048, n_mels=64, fmax=16000)
mf = librosa.mel_frequencies(n_mels=64, fmax=16000)
band = {k: librosa.onset.onset_strength(S=np.sqrt(M[m]), sr=sr, hop_length=hop)
        for k, m in (('low', mf < 150), ('mid', (mf >= 150) & (mf < 4000)), ('high', mf >= 6000))}
band = {k: v / (v.max() + 1e-9) for k, v in band.items()}

def classify(t):
    f = int(round(t * sr / hop)); w = slice(max(0, f - 3), f + 4)
    lo, mi = band['low'][w].max(), band['mid'][w].max()
    if lo > 0.3: return 'kick'
    return 'snare' if mi > 0.3 else 'hat'

onsets = [{'t': round(float(t), 4), 'type': classify(t), 'strength': round(float(env[f] / env.max()), 3)} for t, f in zip(on_t, on_f)]
# beats: librosa beat_track positions snapped to the nearest detected onset (the tracker's phase is frame-coarse)
beats = []
for bt in beat_t:
    near = min(onsets, key=lambda o: abs(o['t'] - bt))
    if abs(near['t'] - bt) < 0.06 and (not beats or near['t'] - beats[-1] > 0.25): beats.append(near['t'])
truth_t = np.array([t for t, _ in truth])
err = [min(abs(truth_t - o['t'])) * 1000 for o in onsets]
data = {
    'bpm_detected': round(tempo, 2), 'beat_track_raw': [round(float(b), 4) for b in beat_t], 'bpm_true': BPM, 'sr': SR, 'hop': hop, 'duration': DUR, 'lead': LEAD,
    'beats': beats, 'downbeats': beats[::4], 'onsets': onsets,
    'detector_error_ms': {'mean': round(float(np.mean(err)), 2), 'max': round(float(np.max(err)), 2), 'n': len(err), 'n_truth': len(truth)},
}
dst = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else pathlib.Path(__file__).parent
(dst / 'beats.json').write_text(json.dumps(data, indent=1))
(dst / 'beats.js').write_text('window.BEATS = ' + json.dumps(data) + ';\n')
print(json.dumps({k: data[k] for k in ('bpm_detected', 'detector_error_ms')}), len(beats), 'beats', len(onsets), 'onsets')
