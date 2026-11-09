# -*- coding: utf-8 -*-
"""native_musicmap.py - Black Dragon "music map" for montage.
Own implementation using librosa APIs (librosa is ISC licensed; ideas only, no copied code).
Outputs: tempo, beats, downbeat-ish bars, strong cut points, sections (structural
segmentation), energy curve, drop/climax times, key. All times in seconds.
"""
import argparse, json, os, sys, tempfile
import numpy as np

KEY_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
MAJ = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
MIN = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])


def _norm(x):
    x = np.asarray(x, float)
    r = x.max() - x.min()
    return (x - x.min()) / r if r > 1e-12 else np.zeros_like(x)


def _smooth(x, n):
    n = max(1, int(n))
    return np.convolve(x, np.ones(n) / n, mode="same")


def estimate_key(chroma):
    v = chroma.mean(axis=1)
    best = (-2, 0, "major")
    for i in range(12):
        for prof, mode in ((MAJ, "major"), (MIN, "minor")):
            c = np.corrcoef(v, np.roll(prof, i))[0, 1]
            if c > best[0]:
                best = (c, i, mode)
    return {"key": f"{KEY_NAMES[best[1]]} {best[2]}", "confidence": round(float(best[0]), 3)}


def analyze(path, n_sections=0, hop=512, max_sec=0):
    import librosa
    y, sr = librosa.load(path, sr=22050, mono=True, duration=max_sec or None)
    dur = len(y) / sr
    # harmonic/percussive split: beats from percussive, chroma from harmonic
    yh, yp = librosa.effects.hpss(y)
    oenv = librosa.onset.onset_strength(y=yp, sr=sr, hop_length=hop)
    tempo, bf = librosa.beat.beat_track(onset_envelope=oenv, sr=sr, hop_length=hop, trim=False)
    tempo = float(np.atleast_1d(tempo)[0])
    beats = librosa.frames_to_time(bf, sr=sr, hop_length=hop)
    if len(beats) < 4:  # fallback: predominant local pulse
        pulse = librosa.beat.plp(onset_envelope=oenv, sr=sr, hop_length=hop)
        pk = np.flatnonzero(librosa.util.localmax(pulse))
        beats = librosa.frames_to_time(pk, sr=sr, hop_length=hop)
    bfr = librosa.time_to_frames(beats, sr=sr, hop_length=hop)
    ostr = np.interp(bfr, np.arange(len(oenv)), oenv) if len(beats) else np.array([])
    # downbeat heuristic: bar phase (of 4) with the largest summed low-band + onset weight
    S = np.abs(librosa.stft(y, hop_length=hop)) ** 2
    freqs = librosa.fft_frequencies(sr=sr)
    low = S[freqs < 150].sum(axis=0)
    lowb = np.interp(bfr, np.arange(len(low)), low) if len(beats) else np.array([])
    phase = 0
    if len(beats) >= 8:
        w = _norm(ostr) + _norm(lowb)
        phase = int(np.argmax([w[p::4].mean() for p in range(4)]))
    downbeats = beats[phase::4] if len(beats) else beats
    # energy curve (RMS, 2 points per second)
    rms = librosa.feature.rms(y=y, hop_length=hop)[0]
    step = max(1, int(sr / hop / 2))
    n = len(rms) // step
    ec = rms[: n * step].reshape(n, step).mean(axis=1)
    ec_n = _norm(ec)
    ec_t = (np.arange(n) * step + step / 2) * hop / sr
    # drops: biggest rise of mean energy (next 4s) vs (previous 4s)
    k = 8
    contrast = np.zeros(n)
    for i in range(k, n - k):
        contrast[i] = ec_n[i:i + k].mean() - ec_n[i - k:i].mean()
    drops = []
    c = contrast.copy()
    for _ in range(3):
        i = int(np.argmax(c))
        if c[i] < 0.18:
            break
        t = float(ec_t[i])
        pool = downbeats if len(downbeats) else beats
        if len(pool):  # snap to the nearest downbeat
            t = float(pool[np.argmin(np.abs(pool - t))])
        drops.append({"t": round(t, 2), "rise": round(float(c[i]), 3)})
        c[max(0, i - 2 * k): i + 2 * k] = 0
    sm = _smooth(ec_n, 6)
    climax = float(ec_t[int(np.argmax(sm))])
    # sections: beat-synchronous chroma+MFCC, agglomerative clustering with temporal constraint
    chroma = librosa.feature.chroma_cqt(y=yh, sr=sr, hop_length=hop)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, hop_length=hop, n_mfcc=13)
    ref = bf if len(bf) > 8 else np.arange(0, chroma.shape[1], 8)
    cs = librosa.util.sync(chroma, ref, aggregate=np.median)
    ms = librosa.util.sync(mfcc[1:], ref, aggregate=np.mean)
    feat = np.vstack([librosa.util.normalize(cs, axis=1),
                      librosa.util.normalize(ms - ms.mean(1, keepdims=True), axis=1)])
    kk = n_sections or int(min(8, max(3, round(dur / 20))))
    kk = min(kk, feat.shape[1])
    sb = librosa.segment.agglomerative(feat, kk)  # boundaries as indices into the synced columns
    sb_frames = librosa.util.fix_frames(ref, x_min=0, x_max=chroma.shape[1] - 1)
    sec_t = librosa.frames_to_time(sb_frames[np.clip(sb, 0, len(sb_frames) - 1)], sr=sr, hop_length=hop)
    edges = [0.0] + [float(t) for t in sec_t if 0.5 < t < dur - 0.5] + [dur]
    edges = sorted(set(round(e, 2) for e in edges))
    sections = []
    for a, b in zip(edges[:-1], edges[1:]):
        m = (ec_t >= a) & (ec_t < b)
        sections.append({"start": a, "end": b,
                         "mean_energy": round(float(ec_n[m].mean()) if m.any() else 0.0, 3)})
    me = [s["mean_energy"] for s in sections]
    for s in sections:
        s["role"] = ("high" if s["mean_energy"] >= 0.66 * max(me)
                     else ("low" if s["mean_energy"] <= 0.33 * max(me) else "mid"))
    # strong cut points: downbeats + strong beats (top quartile onset) + section edges + drops
    cuts = [(float(t), "downbeat") for t in downbeats]
    thr = np.percentile(ostr, 75) if len(ostr) else 0
    for t, s in zip(beats, ostr):
        if s >= thr and not any(abs(t - c0) < 0.05 for c0, _ in cuts):
            cuts.append((float(t), "strong-beat"))
    cuts += [(e, "section") for e in edges[1:-1]]
    cuts += [(d["t"], "drop") for d in drops]
    cuts.sort()
    return {
        "file": os.path.basename(path), "duration": round(dur, 2), "tempo_bpm": round(tempo, 1),
        "beats": [round(float(t), 3) for t in beats], "downbeat_phase": phase,
        "downbeats": [round(float(t), 3) for t in downbeats],
        "strong_cuts": [{"t": round(t, 3), "kind": kd} for t, kd in cuts],
        "sections": sections, "drops": drops, "climax_t": round(climax, 2),
        "energy_curve": {"hz": 2, "values": [round(float(v), 3) for v in ec_n]},
        "key": estimate_key(chroma),
    }


def synth(path, sr=22050):
    """48 s at 120 BPM: A (0-16) soft pad+hats, B (16-32) riser build, C (32-48) loud kick+bass drop."""
    import wave
    T = 48
    t = np.arange(T * sr) / sr
    y = np.zeros_like(t)
    beat = 0.5
    rng = np.random.default_rng(1)

    def kick(t0, dur, f0, f1, amp):
        i0 = int(t0 * sr); n = int(dur * sr); tt = np.arange(n) / sr
        ph = 2 * np.pi * np.cumsum(np.linspace(f0, f1, n)) / sr
        out = amp * np.sin(ph) * np.exp(-tt * (5 / dur))
        j = min(len(y), i0 + n); y[i0:j] += out[: j - i0]

    def noise(t0, n, a, tau):
        i = int(t0 * sr); j = min(len(y), i + n)
        y[i:j] += a * rng.standard_normal(j - i) * np.exp(-np.arange(j - i) / tau)

    pa = 0.08 * (np.sin(2*np.pi*220*t) + np.sin(2*np.pi*261.6*t) + np.sin(2*np.pi*329.6*t))
    y[: 16*sr] += pa[: 16*sr]
    for b in np.arange(0, 16, beat):
        noise(b, 600, 0.05, 150)
    pb = 0.10 * (np.sin(2*np.pi*174.6*t) + np.sin(2*np.pi*220*t) + np.sin(2*np.pi*261.6*t))
    y[16*sr:32*sr] += pb[16*sr:32*sr]
    for b in np.arange(16, 32, beat):
        noise(b, 1500, 0.06 + 0.2 * (b - 16) / 16, 400)
    pc = 0.25 * (np.sin(2*np.pi*130.8*t) + np.sin(2*np.pi*164.8*t) + np.sin(2*np.pi*196*t))
    y[32*sr:] += pc[32*sr:]
    for k, b in enumerate(np.arange(32, 48, beat)):
        kick(b, 0.25, 120, 45, 0.9 if k % 4 == 0 else 0.6)
        noise(b + beat / 2, 600, 0.15, 150)
    y *= 0.8 / max(1e-9, np.abs(y).max())
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((y * 32767).astype("<i2").tobytes())


def self_test():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "synth.wav")
        synth(p)
        r = analyze(p, n_sections=3)
    res = []

    def chk(name, ok, info):
        res.append(ok)
        print(("PASS " if ok else "FAIL ") + name + ": " + str(info))

    chk("tempo ~120 (or 60/240 octave)", any(abs(r["tempo_bpm"] - x) <= 5 for x in (120, 60, 240)), r["tempo_bpm"])
    chk("beats found", len(r["beats"]) >= 40, len(r["beats"]))
    bd = np.diff(r["downbeats"])
    chk("downbeat spacing = 4 beats", len(bd) > 4 and abs(np.median(bd) - 4 * 60 / r["tempo_bpm"]) < 0.3,
        round(float(np.median(bd)), 2) if len(bd) else None)
    chk("drop within 1.5s of 32s", any(abs(x["t"] - 32) <= 1.5 for x in r["drops"]), r["drops"])
    chk("climax in last section (>=32s)", r["climax_t"] >= 32, r["climax_t"])
    inner = [s["start"] for s in r["sections"][1:]]
    chk("section boundaries near 16s and 32s (+-3s)",
        any(abs(x - 16) <= 3 for x in inner) and any(abs(x - 32) <= 3 for x in inner), inner)
    chk("last section is high-energy", r["sections"][-1]["role"] == "high", r["sections"][-1])
    chk("strong cuts include drop/section/downbeat",
        {"drop", "section", "downbeat"} <= {c["kind"] for c in r["strong_cuts"]}, len(r["strong_cuts"]))
    chk("key estimated", r["key"]["key"].split()[0] in KEY_NAMES, r["key"])
    ok = all(res)
    print(f"SELF-TEST {'OK' if ok else 'FAILED'} ({sum(res)}/{len(res)})")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="Music map for montage (beats, sections, cuts, energy, drops)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("map")
    a.add_argument("audio")
    a.add_argument("--sections", type=int, default=0)
    a.add_argument("--max-sec", type=float, default=0)
    a.add_argument("--out")
    a.add_argument("--json", action="store_true")
    sub.add_parser("self-test")
    args = ap.parse_args()
    if args.cmd == "self-test":
        sys.exit(self_test())
    r = analyze(args.audio, args.sections, max_sec=args.max_sec)
    s = json.dumps(r, ensure_ascii=False, indent=None if args.json else 2)
    if args.out:
        open(args.out, "w", encoding="utf-8").write(s)
    if args.json or not args.out:
        print(s)
    else:
        print(f"tempo {r['tempo_bpm']} bpm | {len(r['beats'])} beats | {len(r['sections'])} sections | "
              f"drops {[d['t'] for d in r['drops']]} | climax {r['climax_t']}s -> {args.out}")


if __name__ == "__main__":
    main()
