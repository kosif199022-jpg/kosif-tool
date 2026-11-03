#!/usr/bin/env python3
"""يستخرج طاقة الصوت ونبضاته (onsets) وBPM تقريبياً من أي ملف عبر ffmpeg + numpy، ويقترح نقاط قطع على الإيقاع.

usage: python beat_cuts.py music.mp3 [--every 2] [--min-gap 0.5] [--out beats.json]
--every N يختار كل N نبضة كنقطة قطع (1 = كل نبضة، 2 = كل نبضتين …). المخرج: {bpm, beats_s, cut_points_s, energy_fps,
steady_beat, tempo_confidence, bpm_candidate, steadiness}
يحتاج numpy. الطريقة: غلاف طاقة على 100 إطار/ث → فرق طيفي موجب → عتبة متكيفة → ذروات → مسح إيقاع 60–200 BPM
بمطابقة النبضات على شبكة ثابتة. إذا لم تتفوّق المطابقة على مستوى الصدفة يكون bpm = null و steady_beat = false
(لا إيقاع ثابت: اقطع على الطاقة بدلاً من ذلك). القاعدة نفسها في kosif-superpowers/scripts/music_rhythm_engine.py.
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


def pick_peaks(flux, min_gap_frames=25, salience=4.0):
    k = 50
    pad = np.pad(flux, (k, k), mode="edge")
    win = np.lib.stride_tricks.sliding_window_view(pad, 2 * k)[: len(flux)]
    thr = win.mean(axis=1) + 0.6 * win.std(axis=1)
    # A peak must also stand out from the local noise floor (median + salience*MAD).
    # Without this, stationary noise yields a peak right after every refractory gap,
    # a fake periodic "beat" at the --min-gap spacing.
    med = np.median(win, axis=1)
    mad = np.median(np.abs(win - med[:, None]), axis=1)
    floor = med + salience * mad
    peaks, last = [], -10 ** 9
    for i in range(1, len(flux) - 1):
        if (flux[i] > thr[i] and flux[i] > floor[i] and flux[i] >= flux[i - 1] and flux[i] >= flux[i + 1]
                and i - last >= min_gap_frames):
            peaks.append(i); last = i
    return peaks


def estimate_bpm(beats_s):
    """Legacy histogram estimate (mode of inter-onset gaps). Always answers, even for
    noise, so it is reported only as bpm_histogram; use tempo_scan for the bpm."""
    if len(beats_s) < 4:
        return None
    gaps = np.diff(beats_s)
    gaps = gaps[(gaps > 0.25) & (gaps < 2.0)]
    if not len(gaps):
        return None
    hist, edges = np.histogram(gaps, bins=60, range=(0.25, 2.0))
    g = edges[hist.argmax()] + (edges[1] - edges[0]) / 2
    bpm = 60 / g
    while bpm < 70: bpm *= 2
    while bpm > 180: bpm /= 2
    return round(bpm, 1)


# Same steadiness rule and constants as kosif-superpowers/scripts/music_rhythm_engine.py,
# so both tools agree on what is (and is not) a steady beat.
MIN_BPM, MAX_BPM = 60, 200
ALIGN_TOL = 0.055
STEADY_MIN_MATCH = 0.60
STEADY_MARGIN = 0.10


def chance_match(n):
    return 0.30 + 1.2 / np.sqrt(max(1, n))


def steadiness(match, n):
    chance = chance_match(n)
    required = max(STEADY_MIN_MATCH, chance + STEADY_MARGIN)
    conf = 0.0 if n < 4 else float(np.clip((match - chance) / max(1e-9, 1 - chance), 0, 1))
    return {"match": round(float(match), 5), "onsets": int(n), "chance_match": round(float(chance), 5),
            "required_match": round(float(required), 5), "tempo_confidence": round(conf, 4),
            "steady_beat": bool(n >= 4 and match >= required),
            "rule": "steady when onsets >= 4 and match >= max(0.60, chance_match + 0.10); chance_match = 0.30 + 1.2/sqrt(onsets)"}


def _score(ev, duration, bpm):
    period = 60.0 / bpm
    anchors = ev[:12]
    d = np.mod(ev[None, :] - anchors[:, None], period)
    err = np.minimum(d, period - d)
    close = (err <= ALIGN_TOL).sum(axis=1)
    coverage = min(1.0, len(ev) / max(1.0, np.floor(duration / period + 1e-9)))
    score = close / len(ev) * (0.60 + 0.40 * coverage)
    mean_err = err.mean(axis=1)
    i = int(np.lexsort((mean_err, -np.round(score, 9)))[0])
    return {"bpm": bpm, "match": round(float(score[i]), 5), "aligned_onsets": int(close[i]),
            "mean_error_seconds": round(float(mean_err[i]), 6), "phase_anchor_seconds": float(anchors[i])}


def tempo_scan(beats_s, duration):
    """Integer 60-200 BPM scan of onset/grid alignment, then 0.1 BPM refinement."""
    ev = np.asarray(beats_s, dtype=float)
    if len(ev) < 4 or duration <= 0:
        return None, steadiness(0.0, len(ev))
    scores = sorted((_score(ev, duration, b) for b in range(MIN_BPM, MAX_BPM + 1)),
                    key=lambda x: (-x["match"], x["mean_error_seconds"], x["bpm"]))
    alts = []
    for x in scores:
        if all(abs(x["bpm"] - a["bpm"]) >= 6 for a in alts):
            alts.append(x)
        if len(alts) >= 3:
            break
    refined = []
    for x in alts:
        best = x
        for step in range(-9, 10):
            b = round(x["bpm"] + step / 10, 1)
            if step and MIN_BPM <= b <= MAX_BPM:
                c = _score(ev, duration, b)
                if c["match"] > best["match"] + 1e-9:
                    best = c
        refined.append(best)
    refined.sort(key=lambda x: (-x["match"], x["mean_error_seconds"], x["bpm"]))
    return refined, steadiness(refined[0]["match"], len(ev))


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
    duration = len(x) / SR
    bpm_hist = estimate_bpm(np.array(beats))
    # Tempo uses onsets with a short 0.12 s refractory (as audio_cue_mapper does), not the
    # --min-gap cut spacing: a long refractory turns noise into a fake beat at that spacing.
    tempo_onsets = [p / 100 for p in pick_peaks(flux, 12)]
    hyps, gate = tempo_scan(tempo_onsets, duration)
    bpm_candidate = hyps[0]["bpm"] if hyps else None
    bpm = bpm_candidate if gate["steady_beat"] else None
    cuts = beats[:: max(1, a.every)]
    # also expose per-video-frame energy at 30fps for animation use
    idx = (np.arange(0, len(rms), 100 / 30)).astype(int)
    energy30 = [round(float(v), 3) for v in rms[idx[idx < len(rms)]]]
    out = {"file": a.audio, "duration_s": round(len(x) / SR, 2), "bpm": bpm, "beats_s": beats, "cut_points_s": cuts,
           "beat_period_s": round(60 / bpm, 3) if bpm else None, "energy_fps": 30, "energy": energy30,
           "steady_beat": gate["steady_beat"], "tempo_confidence": gate["tempo_confidence"],
           "bpm_candidate": bpm_candidate, "tempo_onsets": len(tempo_onsets), "bpm_histogram": bpm_hist, "tempo_hypotheses": hyps or [],
           "steadiness": gate,
           "note": None if gate["steady_beat"] else "no steady beat: onsets do not align to a tempo grid above chance; cut on energy/onsets instead"}
    open(a.out, "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False))
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(json.dumps({k: out[k] for k in ("duration_s", "bpm", "beat_period_s", "steady_beat", "tempo_confidence")} | {"beats": len(beats), "cuts": len(cuts), "out": a.out}, ensure_ascii=False))


if __name__ == "__main__":
    main()
