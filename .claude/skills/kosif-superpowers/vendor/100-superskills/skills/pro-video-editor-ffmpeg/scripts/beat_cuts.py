#!/usr/bin/env python3
"""يستخرج طاقة الصوت ونبضاته (onsets) وBPM تقريبياً من أي ملف عبر ffmpeg + numpy، ويقترح نقاط قطع على الإيقاع.

usage: python beat_cuts.py music.mp3 [--every 2] [--min-gap 0.5] [--out beats.json]
--every N يختار كل N نبضة كنقطة قطع (1 = كل نبضة، 2 = كل نبضتين …). المخرج: {bpm, beats_s, cut_points_s, energy_fps}
يحتاج numpy. الطريقة: غلاف طاقة على 100 إطار/ث → فرق طيفي موجب → عتبة متكيفة → ذروات → BPM من التوزيع الزمني للفواصل.
"""
import argparse
import json
import subprocess
import sys

try:
    import numpy as np
except ImportError:
    sys.exit("numpy غير مثبت: pip install numpy")

SR = 22050
HOP = SR // 100  # 100 frames per second


def load_mono(path):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True)
    if r.returncode != 0:
        raise SystemExit(r.stderr.decode(errors="ignore")[-800:])
    return np.frombuffer(r.stdout, dtype=np.float32)


def onset_envelope(x):
    n = len(x) // HOP
    frames = x[: n * HOP].reshape(n, HOP)
    win = np.hanning(HOP * 2)
    spec_prev, flux = None, np.zeros(n)
    for i in range(n):
        seg = np.concatenate([frames[i - 1] if i else np.zeros(HOP), frames[i]]) * win
        spec = np.abs(np.fft.rfft(seg))
        if spec_prev is not None:
            d = spec - spec_prev
            flux[i] = np.sum(d[d > 0])
        spec_prev = spec
    flux = flux / (flux.max() or 1)
    rms = np.sqrt((frames ** 2).mean(axis=1)); rms = rms / (rms.max() or 1)
    return flux, rms


def pick_peaks(flux, min_gap_frames=25):
    k = 50
    pad = np.pad(flux, (k, k), mode="edge")
    thr = np.array([pad[i:i + 2 * k].mean() + 0.6 * pad[i:i + 2 * k].std() for i in range(len(flux))])
    peaks, last = [], -10 ** 9
    for i in range(1, len(flux) - 1):
        if flux[i] > thr[i] and flux[i] >= flux[i - 1] and flux[i] >= flux[i + 1] and i - last >= min_gap_frames:
            peaks.append(i); last = i
    return peaks


def estimate_bpm(beats_s):
    """Return a tempo hypothesis only for an actual repeatable pulse train.

    The old single histogram-bin maximum gave plausible BPM values for
    unrelated transient intervals (e.g. 92.9 BPM in a clip with no steady
    beat). Require both consistent intervals and a coherent global beat phase.
    Return None rather than invent precision when either test fails.
    """
    beats = np.asarray(beats_s, dtype=np.float64)
    if len(beats) < 7 or not np.isfinite(beats).all() or np.any(np.diff(beats) <= 0):
        return None
    gaps = np.diff(beats)
    usable = gaps[(gaps > 0.25) & (gaps < 2.0)]
    if len(usable) < 6:
        return None
    period = float(np.median(usable))
    if not 0.25 < period < 2.0:
        return None
    # Missing individual beats are allowed (gaps of 2x or 3x the period).
    multiples = usable / period
    interval_support = float(np.mean(np.abs(multiples - np.rint(multiples)) <= 0.12))
    phases = (beats - beats[0]) / period
    phase_support = float(np.mean(np.abs(phases - np.rint(phases)) <= 0.15))
    if interval_support < 0.80 or phase_support < 0.75:
        return None
    bpm = 60.0 / period
    while bpm < 70:
        bpm *= 2
    while bpm > 180:
        bpm /= 2
    return round(bpm, 1)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("--every", type=int, default=2)
    ap.add_argument("--min-gap", type=float, default=0.5)
    ap.add_argument("--out", default="beats.json")
    a = ap.parse_args()
    x = load_mono(a.audio)
    flux, rms = onset_envelope(x)
    peaks = pick_peaks(flux, int(a.min_gap * 100 * 0.6))
    beats = [round(p / 100, 3) for p in peaks]
    bpm = estimate_bpm(np.array(beats))
    cuts = beats[:: max(1, a.every)]
    # also expose per-video-frame energy at 30fps for animation use
    idx = (np.arange(0, len(rms), 100 / 30)).astype(int)
    energy30 = [round(float(v), 3) for v in rms[idx[idx < len(rms)]]]
    out = {"file": a.audio, "duration_s": round(len(x) / SR, 2), "bpm": bpm, "beats_s": beats, "cut_points_s": cuts,
           "beat_period_s": round(60 / bpm, 3) if bpm else None, "tempo_status": "candidate" if bpm else "no_steady_tempo",
           "verified_bpm": False, "energy_fps": 30, "energy": energy30}
    open(a.out, "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False))
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(json.dumps({k: out[k] for k in ("duration_s", "bpm", "beat_period_s")} | {"beats": len(beats), "cuts": len(cuts), "out": a.out}, ensure_ascii=False))


if __name__ == "__main__":
    main()
