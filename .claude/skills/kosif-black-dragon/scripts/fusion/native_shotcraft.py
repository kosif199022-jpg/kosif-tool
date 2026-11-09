#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""native_shotcraft.py - Black Dragon native port of ideas from video-shotcraft
(Vincentwei1021/video-shotcraft, Apache-2.0). Re-written in our own code; no
upstream code is pasted. Ideas ported:

  arc          promo energy-arc frame budget (references/sequences/promo-energy-arc.md)
  beatgrid     least-squares beat grid + 0.5x/1x/2x candidate scoring + kick/snare/hihat
               hit table (references/music-beat-sync.md sections 1-3)
  av-offset    cross-correlation lag between a source audio and a rendered audio track
               (references/sound-design.md 4.6, AAC priming check)
  sfx-peak     internal peak time of an SFX so its peak (not file head) lands on the beat
  jy-plan      Remotion-style frame timeline -> JianYing/CapCut-CN draft plan in
               microseconds: per-shot plate cuts, merged captions, greedy SFX lanes,
               CSS->JianYing style conversion, overlap/gap checks
               (references/jianying-export.md 3-4, jianying-export/aifl_promo.py)
  jy-script    emit a pyJianYingDraft builder script from a plan (the user runs it in a
               venv with pyJianYingDraft; this file never imports it)
  jy-install   safe Windows draft installer: name validation, media bundling into
               Resources/ with case-insensitive unique names, trash-dir atomic replace,
               rollback (jianying-export/windows_draft.py)
  self-test    builds its own inputs in a temp dir and asserts real results

Python 3.12, stdlib + numpy (+ librosa only for audio-file beat analysis).
All outputs: --json prints machine-readable JSON.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unicodedata
import wave

import numpy as np

# ----------------------------------------------------------------------------- utils


def emit(obj, as_json: bool, text: str | None = None) -> None:
    if as_json or text is None:
        sys.stdout.write(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")
    else:
        sys.stdout.write(text + "\n")


def load_json(path: str):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: str, obj) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def read_wav_mono(path: str) -> tuple[np.ndarray, int]:
    """Read PCM WAV (8/16/24/32-bit int) to float32 mono. Other formats -> librosa."""
    try:
        with wave.open(path, "rb") as w:
            sr, ch, sw, n = w.getframerate(), w.getnchannels(), w.getsampwidth(), w.getnframes()
            raw = w.readframes(n)
        if sw == 1:
            a = (np.frombuffer(raw, np.uint8).astype(np.float32) - 128) / 128
        elif sw == 2:
            a = np.frombuffer(raw, "<i2").astype(np.float32) / 32768
        elif sw == 3:
            b = np.frombuffer(raw, np.uint8).reshape(-1, 3)
            v = (b[:, 0].astype(np.int32) | (b[:, 1].astype(np.int32) << 8) | (b[:, 2].astype(np.int32) << 16))
            v = np.where(v >= 1 << 23, v - (1 << 24), v)
            a = v.astype(np.float32) / (1 << 23)
        else:
            a = np.frombuffer(raw, "<i4").astype(np.float32) / (1 << 31)
        a = a.reshape(-1, ch).mean(axis=1)
        return a, sr
    except (wave.Error, EOFError):
        import librosa  # noqa: PLC0415
        y, sr = librosa.load(path, sr=None, mono=True)
        return y.astype(np.float32), int(sr)


def write_wav(path: str, y: np.ndarray, sr: int) -> None:
    pcm = (np.clip(y, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())

# ----------------------------------------------------------------------------- arc

# Segment table: (key, share-of-remaining, energy, role). Shares from the
# promo-energy-arc card: open 8-12 %, hero 12-15 %, features 55-65 %, finale 13-16 %.
ARC_FIXED = [("brand_open", 0.10, "low", "wordmark stamp, hold >= 1 s"),
             ("hero", 0.13, "mid", "one subject, one full action arc >= 3 s")]
ARC_FINALE = ("finale", 0.145, "peak", "group shot around wordmark, sign-off hold >= 1 s")


def plan_arc(total_sec: float, fps: int, features: list[str], breath_cards: int | None = None,
             card_frames: int = 52) -> dict:
    total = round(total_sec * fps)
    n = max(1, len(features))
    if breath_cards is None:  # one card every 1-2 feature shots, 2-4 total
        breath_cards = max(0, min(4, max(2 if n >= 3 else 1, n // 2)))
    shots: list[dict] = []
    open_f = round(total * ARC_FIXED[0][1])
    hero_f = round(total * ARC_FIXED[1][1])
    fin_f = round(total * ARC_FINALE[1])
    cards_f = breath_cards * card_frames
    feat_total = total - open_f - hero_f - fin_f - cards_f
    if feat_total < n * fps:  # short film: merge segments, keep both ends
        breath_cards, cards_f = 0, 0
        feat_total = total - open_f - hero_f - fin_f
        if feat_total < n * fps:
            hero_f = 0
            feat_total = total - open_f - fin_f
    per = feat_total // n
    rem = feat_total - per * n
    # where to drop breath cards: evenly between feature shots
    card_after = set()
    if breath_cards:
        step = n / (breath_cards + 1)
        card_after = {max(0, min(n - 2, round(step * (k + 1)) - 1)) for k in range(breath_cards)}
        while len(card_after) < breath_cards and len(card_after) < max(0, n - 1):
            card_after.add(max(set(range(n - 1)) - card_after))
        breath_cards = len(card_after)
    cur = 0

    def add(name, frames, energy, role, hold):
        nonlocal cur
        shots.append({"name": name, "from": cur, "to": cur + frames, "frames": frames,
                      "sec": round(frames / fps, 3), "energy": energy, "role": role,
                      "hold_budget_f": min(hold, frames // 2),
                      "action_budget_f": frames - min(hold, frames // 2)})
        cur += frames

    add("brand_open", open_f, "low", ARC_FIXED[0][3], fps)
    if hero_f:
        add("hero", hero_f, "mid", ARC_FIXED[1][3], fps // 2)
    energies = ["mid-high", "steady"]
    for i, feat in enumerate(features or ["feature"]):
        add(f"feature:{feat}", per + (1 if i < rem else 0), energies[i % 2],
            "one feature, one technique used once as lead; batch end rest 15 f", fps // 2)
        if i in card_after:
            add(f"breath_card_{len([s for s in shots if s['name'].startswith('breath')]) + 1}",
                card_frames, "rest", "paper title card, never a second tagline", fps // 2)
    add("finale", total - cur, "peak", ARC_FINALE[3], fps)
    warnings = []
    if total_sec < 20:
        warnings.append("short film: segment shares are a single-example default; merge freely, keep open hold and finale peak")
    return {"schema": "kosif.shotcraft.arc.v1", "fps": fps, "total_frames": total,
            "breath_cards": breath_cards, "shots": shots, "warnings": warnings,
            "rules": ["hold/rest frames are reserved before animating",
                      "alternate high-energy and steady shots in the feature climb",
                      "densest document/report shot goes 2nd-3rd from last",
                      "full-frame beat impacts <= 3 per film, >= 16 beats apart"]}

# ----------------------------------------------------------------------------- beat grid


def fit_grid(beats: np.ndarray) -> dict:
    i = np.arange(len(beats), dtype=float)
    A = np.vstack([i, np.ones_like(i)]).T
    (T, t0), *_ = np.linalg.lstsq(A, beats, rcond=None)
    res = beats - (t0 + i * T)
    return {"T": float(T), "t0": float(t0), "bpm": 60.0 / float(T),
            "residual_max_ms": float(np.abs(res).max() * 1000) if len(res) else 0.0}


def score_grid(t0: float, T: float, onsets: np.ndarray, end: float, tol: float = 0.035) -> dict:
    """Score a grid against measured transients: match ratio, mean abs error, drift."""
    if T <= 0 or len(onsets) == 0:
        return {"match": 0.0, "mean_abs_ms": None, "drift_ms": None, "first_beat_valid": False}
    while t0 - T >= onsets[0] - tol:
        t0 -= T
    n = int(math.floor((end - t0) / T)) + 1
    grid = t0 + np.arange(max(n, 1)) * T
    grid = grid[grid >= 0]
    idx = np.searchsorted(onsets, grid)
    lo = np.clip(idx - 1, 0, len(onsets) - 1)
    hi = np.clip(idx, 0, len(onsets) - 1)
    near = np.where(np.abs(onsets[lo] - grid) < np.abs(onsets[hi] - grid), onsets[lo], onsets[hi])
    err = near - grid
    hit = np.abs(err) <= tol
    m = float(hit.mean()) if len(hit) else 0.0
    drift = None
    if hit.sum() >= 3:
        slope = np.polyfit(grid[hit], err[hit], 1)[0]
        drift = float(abs(slope) * (grid[-1] - grid[0]) * 1000)
    return {"match": round(m, 4),
            "mean_abs_ms": round(float(np.abs(err[hit]).mean() * 1000), 3) if hit.any() else None,
            "drift_ms": None if drift is None else round(drift, 3),
            "first_beat_valid": bool(hit[0]) if len(hit) else False}


def band_hits(y: np.ndarray, sr: int, onsets: np.ndarray, win: float = 0.05) -> list[dict]:
    """Classify each onset as kick/snare/hihat by spectral band energy right after it."""
    bands = {"kick": (40, 160), "snare": (150, 500), "snare_hi": (1000, 3000), "hihat": (6000, 14000)}
    n = int(win * sr)
    freqs = np.fft.rfftfreq(n, 1 / sr)
    hann = np.hanning(n)
    out = []
    for t in onsets:
        s = int(t * sr)
        seg = y[s:s + n]
        if len(seg) < n:
            seg = np.pad(seg, (0, n - len(seg)))
        spec = np.abs(np.fft.rfft(seg * hann)) ** 2
        e = {k: float(spec[(freqs >= lo) & (freqs < hi)].sum()) for k, (lo, hi) in bands.items()}
        tot = sum(e.values()) + 1e-12
        kick, snare, hat = e["kick"] / tot, min(e["snare"], e["snare_hi"] * 4) / tot, e["hihat"] / tot
        k = max((("kick", kick), ("snare", snare), ("hihat", hat)), key=lambda kv: kv[1])[0]
        out.append({"t": round(float(t), 4), "s": round(float(np.sqrt(np.mean(seg ** 2))), 5), "k": k})
    # drop near-silent false onsets (e.g. a sample's tail cut-off): below -54 dB of the loudest hit
    peak = max((h["s"] for h in out), default=0.0)
    return [h for h in out if h["s"] > max(1e-5, peak * 0.002)]


def beat_analysis(beats: np.ndarray | None, onsets: np.ndarray | None, end: float | None,
                  audio: str | None = None, fps: int = 30) -> dict:
    hits: list[dict] = []
    if audio:
        import librosa  # noqa: PLC0415
        y, sr = librosa.load(audio, sr=None, mono=True)
        _, perc = librosa.effects.hpss(y)
        _, bt = librosa.beat.beat_track(y=perc, sr=sr, tightness=400, units="time")
        beats = np.asarray(bt, float)
        onsets = np.asarray(librosa.onset.onset_detect(y=perc, sr=sr, units="time", backtrack=False), float)
        end = len(y) / sr
        hits = band_hits(y, sr, onsets)
    assert beats is not None and len(beats) >= 4, "need >= 4 beat times"
    onsets = np.sort(onsets if onsets is not None and len(onsets) else beats)
    end = float(end or beats[-1])
    base = fit_grid(np.sort(beats))
    cands = []
    kicks = np.array([h["t"] for h in hits if h["k"] == "kick"])
    for mult in (0.5, 1.0, 2.0):
        T = base["T"] / mult
        # also test the half-beat phase: beat_track may lock onto off-beat hats
        for phase in (0.0, 0.5):
            t0c = base["t0"] + phase * T
            sc = score_grid(t0c, T, onsets, end)
            if len(kicks):
                ph = ((kicks - t0c) / T) % 1.0
                sc["kick_on_beat"] = round(float(np.mean((ph < 0.12) | (ph > 0.88))), 3)
                # fraction of grid beats carrying a kick: penalises a grid that is too fast
                g0 = t0c % T
                grid = g0 + np.arange(int((end - g0) / T) + 1) * T
                filled = np.min(np.abs(grid[:, None] - kicks[None, :]), axis=1) <= 0.12 * T
                sc["kick_fill"] = round(float(np.mean(filled)), 3)
                sc["kick_score"] = round(sc["kick_on_beat"] * sc["kick_fill"], 3)
            cands.append({"mult": mult, "phase": phase, "t0": round(t0c, 6), "bpm": round(60 / T, 3),
                          "T": round(T, 6), **sc})

    def rank(c):  # coverage bucket, then drum evidence, then base phase/tempo, then low error
        return (c["match"] >= 0.95, c.get("kick_score", 0), round(c["match"], 2), -c["phase"],
                -abs(math.log2(c["mult"])), -(c["mean_abs_ms"] or 1e9))
    win = max(cands, key=rank)
    gates = {"match>=0.98": win["match"] >= 0.98,
             "mean_abs_ms<10": (win["mean_abs_ms"] or 1e9) < 10,
             "drift_ms<5": (win["drift_ms"] or 0) < 5,
             "first_beat_valid": win["first_beat_valid"],
             "residual<=15ms": base["residual_max_ms"] <= 15}
    if len(kicks):
        gates["kick_on_beat>=0.8"] = win.get("kick_on_beat", 0) >= 0.8
    t0 = win["t0"]
    while t0 - win["T"] >= onsets[0] - 0.035:
        t0 -= win["T"]
    return {"schema": "kosif.shotcraft.beatgrid.v1", "bpm": win["bpm"], "t0": round(t0, 6),
            "T": win["T"], "fps": fps, "fit": base, "candidates": cands,
            "winner_reason": f"coverage {win['match']:.0%}, kick score {win.get('kick_score', 'n/a')} at {win['mult']}x phase {win['phase']}",
            "gates": gates, "accepted": all(gates.values()),
            "beat_frames_first16": [round((t0 + n * win["T"]) * fps) for n in range(16)],
            "frame_quantization_ms": round(500 / fps, 2),
            "hits": hits, "note": "times are float seconds; round to frames only at the last step"}

# ----------------------------------------------------------------------------- audio offset / peak


def av_offset(ref: str, render: str, max_lag_s: float = 0.5, fps: int = 30) -> dict:
    a, sra = read_wav_mono(ref)
    b, srb = read_wav_mono(render)
    if sra != srb:
        import librosa  # noqa: PLC0415
        b = librosa.resample(b, orig_sr=srb, target_sr=sra)
    sr = sra
    n = min(len(a), len(b), sr * 20)
    a, b = a[:n] - a[:n].mean(), b[:n] - b[:n].mean()
    size = 1 << int(math.ceil(math.log2(2 * n)))
    xc = np.fft.irfft(np.fft.rfft(b, size) * np.conj(np.fft.rfft(a, size)), size)
    m = int(max_lag_s * sr)
    lags = np.concatenate([np.arange(0, m + 1), np.arange(-m, 0)])
    vals = np.concatenate([xc[:m + 1], xc[-m:]])
    k = int(np.argmax(vals))
    lag = int(lags[k])
    norm = float(vals[k] / (np.sqrt((a ** 2).sum() * (b ** 2).sum()) + 1e-12))
    return {"lag_samples": lag, "lag_ms": round(lag / sr * 1000, 3), "lag_frames": round(lag / sr * fps, 3),
            "sample_rate": sr, "correlation": round(norm, 4),
            "advice": "positive lag = render audio is late; put it in OUTPUT_AUDIO_OFFSET only, never into the source t0"}


def sfx_peak(path: str, fps: int = 30, hop_ms: float = 5.0) -> dict:
    y, sr = read_wav_mono(path)
    hop = max(1, int(sr * hop_ms / 1000))
    nwin = len(y) // hop
    env = np.sqrt(np.mean(y[:nwin * hop].reshape(nwin, hop) ** 2, axis=1)) if nwin else np.array([0.0])
    k = int(np.argmax(env))
    t = (k + 0.5) * hop / sr
    return {"file": path, "peak_sec": round(t, 4), "peak_frames": round(t * fps, 3),
            "duration_sec": round(len(y) / sr, 4),
            "placement": "start_frame = target_frame - round(peak_sec * fps)  (minus output offset in Remotion only)"}

# ----------------------------------------------------------------------------- JianYing plan


def f2us(f: float, fps: float) -> int:
    return round(f * 1_000_000 / fps)


def us_range(f0: float, f1: float, fps: float) -> dict:
    """Round start and end separately, then subtract: adjacent segments never gap/overlap by 1 us."""
    s, e = f2us(f0, fps), f2us(f1, fps)
    return {"start": s, "duration": e - s}


def css_px_to_jy_size(px: float, canvas_h: int = 1080) -> float:
    return round(px / (canvas_h / 100.0), 3)          # size ~ % of canvas height (64px@1080 -> ~6.0)


def screen_y_to_transform_y(y_px: float, canvas_h: int = 1080) -> float:
    return round(1 - y_px / (canvas_h / 2), 4)        # y = H/2 * (1 - t)


def hex_to_float3(h: str) -> list[float]:
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return [round(int(h[i:i + 2], 16) / 255, 3) for i in (0, 2, 4)]


def greedy_lanes(items: list[dict]) -> int:
    lanes: list[int] = []
    for it in sorted(items, key=lambda d: (d["start"], d["duration"])):
        lane = next((i for i, end in enumerate(lanes) if end <= it["start"]), len(lanes))
        if lane == len(lanes):
            lanes.append(0)
        lanes[lane] = it["start"] + it["duration"]
        it["lane"] = lane
    return len(lanes)


def check_track(segs: list[dict], name: str) -> list[str]:
    errs = []
    s = sorted(segs, key=lambda d: d["start"])
    for a, b in zip(s, s[1:]):
        if a["start"] + a["duration"] > b["start"]:
            errs.append(f"{name}: overlap {a['start']}+{a['duration']} > {b['start']}")
    return errs


def jy_plan(tl: dict) -> dict:
    fps = tl.get("fps", 30)
    W, H = tl.get("width", 1920), tl.get("height", 1080)
    total_f = tl["total_frames"]
    total_us = f2us(total_f, fps)
    beat = tl.get("beat")  # {"t0": s, "T": s}

    def beat_frame(n: float) -> int:
        return round((beat["t0"] + n * beat["T"]) * fps)

    plate = []
    shots = tl.get("shots", [])
    for name, f0, f1 in shots:
        r = us_range(f0, f1, fps)
        plate.append({"name": name, **r, "source_start": r["start"], "source_duration": r["duration"]})
    warns = []
    for (_, _, a1), (_, b0, _) in zip(shots, shots[1:]):
        if a1 != b0:
            warns.append(f"plate gap/overlap between shots at frame {a1} vs {b0}")

    # captions: merge adjacent identical text (cross-shot continuation)
    caps_in = sorted(tl.get("captions", []), key=lambda c: c[-2])
    merged: list[list] = []
    for c in caps_in:
        texts, f0, f1 = list(c[:-2]), c[-2], c[-1]
        if merged and merged[-1][0] == texts and merged[-1][2] >= f0 - 1:
            merged[-1][2] = max(merged[-1][2], f1)
        else:
            merged.append([texts, f0, f1])
    style_in = tl.get("caption_style", [{"css_px": 22, "color": "#575552", "center_y_px": 995}])
    styles = []
    for st in style_in:
        styles.append({"size": css_px_to_jy_size(st.get("css_px", 22), H),
                       "color": hex_to_float3(st.get("color", "#FFFFFF")),
                       "transform_y": screen_y_to_transform_y(st.get("center_y_px", 0.92 * H), H),
                       "align": 1, "letter_spacing": st.get("letter_spacing", 0),
                       "background": st.get("background")})
    n_lang = max((len(m[0]) for m in merged), default=1)
    text_tracks = [[] for _ in range(n_lang)]
    for texts, f0, f1 in merged:
        r = us_range(f0, f1, fps)
        for li, t in enumerate(texts):  # one size per text segment -> one track per language
            text_tracks[li].append({"text": t, **r, "style": li if li < len(styles) else 0})

    sfx = []
    for s in tl.get("sfx", []):
        if "beat" in s:
            assert beat, "sfx uses 'beat' but timeline has no beat grid"
            target = beat_frame(s["beat"])
        else:
            target = s["frame"]
        start_f = max(0, target - round(s.get("peak_sec", 0) * fps) + s.get("audio_lag_f", 0))
        dur = f2us(s.get("cap_frames", 90), fps)
        if "duration_sec" in s:
            dur = min(dur, round(s["duration_sec"] * 1_000_000))
        start = f2us(start_f, fps)
        dur = min(dur, total_us - start)
        if dur <= 0:
            warns.append(f"sfx {s['file']} starts after end; dropped")
            continue
        sfx.append({"file": s["file"], "start": start, "duration": dur, "volume": s.get("volume", 1.0),
                    "target_frame": target, "start_frame": start_f})
    n_lanes = greedy_lanes(sfx)
    errs = check_track(plate, "plate")
    for li, tr in enumerate(text_tracks):
        errs += check_track(tr, f"text{li}")
    for ln in range(n_lanes):
        errs += check_track([s for s in sfx if s["lane"] == ln], f"sfx{ln + 1}")
    bgm = None
    if tl.get("bgm"):
        b = tl["bgm"]
        bgm = {"file": b["file"], "start": 0,
               "duration": min(total_us, round(b.get("duration_sec", 1e9) * 1_000_000)),
               "volume": b.get("volume", 0.72)}
    return {"schema": "kosif.shotcraft.jianying-plan.v1", "name": tl.get("name", "kosif-draft"),
            "fps": fps, "width": W, "height": H, "total_frames": total_f, "total_us": total_us,
            "plate": {"file": tl.get("plate"), "segments": plate},
            "text_styles": styles, "text_tracks": text_tracks,
            "sfx_lanes": n_lanes, "sfx": sfx, "bgm": bgm,
            "errors": errs, "warnings": warns, "ok": not errs,
            "layers": {"baked": "in-shot motion (camera, particles, 3D, per-element choreography, brand lock-ups)",
                       "editable": "shot cuts (speed/reorder/delete), screen-space captions, SFX/BGM volume+position"}}


def jy_script(plan: dict, staging: str) -> str:
    """Emit a pyJianYingDraft 0.3.x builder. Run it in a venv: pip install pyJianYingDraft."""
    P = json.dumps(plan, ensure_ascii=False)
    return f'''# Generated by native_shotcraft.py jy-script (Black Dragon). Requires: pip install pyJianYingDraft
# Run inside a venv; then install with: python native_shotcraft.py jy-install --draft <staging>/<name>
import json
import pyJianYingDraft as draft

PLAN = json.loads(r"""{P}""")
STAGING = r"{staging}"

folder = draft.DraftFolder(STAGING)
script = folder.create_draft(PLAN["name"], PLAN["width"], PLAN["height"], fps=PLAN["fps"], allow_replace=True)
script.append_track(draft.TrackSpec(draft.TrackType.video, name="plate"))
if PLAN["bgm"]:
    script.append_track(draft.TrackSpec(draft.TrackType.audio, name="BGM"))
for i, _ in enumerate(PLAN["text_tracks"]):
    script.append_track(draft.TrackSpec(draft.TrackType.text, name=f"caption{{i}}"))
for i in range(PLAN["sfx_lanes"]):
    script.append_track(draft.TrackSpec(draft.TrackType.audio, name=f"SFX{{i + 1}}"))

mat = draft.VideoMaterial(PLAN["plate"]["file"])
for s in PLAN["plate"]["segments"]:
    rng = draft.Timerange(s["start"], s["duration"])
    script.add_segment(draft.VideoSegment(mat, rng, source_timerange=draft.Timerange(s["source_start"], s["source_duration"])), "plate")

for i, track in enumerate(PLAN["text_tracks"]):
    for seg in track:
        st = PLAN["text_styles"][seg["style"]]
        kw = dict(style=draft.TextStyle(size=st["size"], color=tuple(st["color"]), align=st["align"],
                                        letter_spacing=st["letter_spacing"]),
                  clip_settings=draft.ClipSettings(transform_y=st["transform_y"]))
        if st.get("background"):
            b = st["background"]
            kw["background"] = draft.TextBackground(color=b.get("color", "#FFFFFF"), alpha=b.get("alpha", 0.82),
                                                    round_radius=b.get("round_radius", 0.35))
        script.add_segment(draft.TextSegment(seg["text"], draft.Timerange(seg["start"], seg["duration"]), **kw), f"caption{{i}}")

cache = {{}}
for s in PLAN["sfx"]:
    m = cache.setdefault(s["file"], draft.AudioMaterial(s["file"]))
    dur = min(s["duration"], m.duration)
    script.add_segment(draft.AudioSegment(m, draft.Timerange(s["start"], dur), volume=s["volume"]), f"SFX{{s['lane'] + 1}}")

if PLAN["bgm"]:
    b = draft.AudioMaterial(PLAN["bgm"]["file"])
    script.add_segment(draft.AudioSegment(b, draft.Timerange(0, min(b.duration, PLAN["bgm"]["duration"])),
                                          volume=PLAN["bgm"]["volume"]), "BGM")
script.save()
print("staging draft:", STAGING, PLAN["name"])
'''

# ----------------------------------------------------------------------------- Windows installer


def default_draft_root() -> str:
    for c in (os.path.expandvars(r"%LOCALAPPDATA%\JianyingPro\User Data\Projects\com.lveditor.draft"),
              os.path.expanduser(r"~\JianyingPro Drafts")):
        if os.path.isdir(c):
            return c
    raise FileNotFoundError("JianYing draft root not found; pass --draft-root (Settings > Draft location)")


def jianying_running() -> bool:
    if os.name != "nt":
        return False
    out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq JianyingPro.exe", "/NH"],
                         capture_output=True, text=True).stdout
    return "JianyingPro" in out


def safe_target(name: str, root: str) -> str:
    bad = (not name or name in (".", "..") or any(c in name for c in '/\\:') or os.path.isabs(name))
    if bad:
        raise ValueError(f"illegal draft name {name!r}")
    tgt = os.path.realpath(os.path.join(root, name))
    if os.path.dirname(tgt) != os.path.realpath(root):
        raise ValueError(f"draft name escapes the draft root: {tgt}")
    return os.path.join(root, name)


def _key(n: str) -> str:
    return unicodedata.normalize("NFC", n).casefold()   # NTFS is case-insensitive


def _unique(n: str, used: set) -> str:
    if _key(n) not in used:
        return n
    stem, ext = os.path.splitext(n)
    i = 2
    while _key(f"{stem}-{i}{ext}") in used:
        i += 1
    return f"{stem}-{i}{ext}"


def bundle_media(draft_dir: str, name: str, root: str) -> dict:
    cp = os.path.join(draft_dir, "draft_content.json")
    content = load_json(cp)
    res = os.path.join(draft_dir, "Resources")
    os.makedirs(res, exist_ok=True)
    final_base = os.path.join(root, name, "Resources")
    mapping, used, copied = {}, set(), 0
    for kind in ("videos", "audios"):
        for m in content.get("materials", {}).get(kind, []):
            src = m["path"]
            if src.startswith(final_base + os.sep):
                if not os.path.exists(os.path.join(res, os.path.basename(src))):
                    raise FileNotFoundError(f"already-rewritten path but staged copy missing: {src}")
                used.add(_key(os.path.basename(src)))
                continue
            if src not in mapping:
                nm = _unique(os.path.basename(src), used)
                used.add(_key(nm))
                shutil.copy2(src, os.path.join(res, nm))
                copied += 1
                mapping[src] = os.path.join(final_base, nm)
            m["path"] = mapping[src]
    save_json(cp, content)
    return {"copied": copied, "rewritten": len(mapping)}


def install_draft(draft_dir: str, root: str | None, bundle: bool = True, dry_run: bool = False) -> dict:
    if jianying_running():
        raise RuntimeError("JianYing is running; quit it fully first")
    root = root or default_draft_root()
    name = os.path.basename(os.path.normpath(draft_dir))
    target = safe_target(name, root)
    if not os.path.isfile(os.path.join(draft_dir, "draft_content.json")):
        raise FileNotFoundError("draft_content.json missing in staging draft")
    if dry_run:
        return {"target": target, "would_replace": os.path.exists(target), "dry_run": True}
    info = bundle_media(draft_dir, name, root) if bundle else {}
    old = None
    if os.path.exists(target):
        trash = os.path.join(root, ".vs-export-trash")
        os.makedirs(trash, exist_ok=True)
        old = os.path.join(trash, f"{name}.replaced-{time.strftime('%Y%m%d-%H%M%S')}")
        os.rename(target, old)
    try:
        shutil.move(draft_dir, target)
    except BaseException:
        if os.path.exists(target) and not os.path.exists(draft_dir):
            shutil.move(target, draft_dir)
        elif os.path.exists(target):
            shutil.rmtree(target, ignore_errors=True)
        if old and os.path.exists(old):
            os.rename(old, target)
        raise
    warn = None
    if old:
        try:
            shutil.rmtree(old)
        except OSError as e:
            warn = f"old copy left in trash dir: {old} ({e})"
    return {"target": target, "replaced": bool(old), "bundle": info, "warning": warn}


def verify_installed(target: str) -> dict:
    c = load_json(os.path.join(target, "draft_content.json"))
    paths = [m["path"] for k in ("videos", "audios") for m in c.get("materials", {}).get(k, [])]
    inside = all(os.path.realpath(p).startswith(os.path.realpath(target) + os.sep) for p in paths)
    return {"media": len(paths), "all_exist": all(os.path.exists(p) for p in paths), "all_inside_draft": inside,
            "tracks": len(c.get("tracks", []))}

# ----------------------------------------------------------------------------- self-test


def self_test() -> dict:
    results = {}
    tmp = tempfile.mkdtemp(prefix="shotcraft_st_")
    try:
        # 1 arc
        arc = plan_arc(36, 30, ["search", "filter", "table", "report"])
        fr = [s["frames"] for s in arc["shots"]]
        assert sum(fr) == 1080 and arc["shots"][0]["from"] == 0 and arc["shots"][-1]["to"] == 1080
        assert all(a["to"] == b["from"] for a, b in zip(arc["shots"], arc["shots"][1:]))
        assert arc["shots"][-1]["name"] == "finale" and arc["breath_cards"] >= 1
        results["arc"] = f"{len(fr)} shots, {arc['breath_cards']} breath cards, sum={sum(fr)}f"

        # 2 beat grid from times: 128 BPM with jitter, onsets include off-beat hats
        rng = np.random.default_rng(7)
        T = 60 / 128
        beats = 0.21 + np.arange(64) * T + rng.normal(0, 0.003, 64)
        onsets = np.sort(np.concatenate([beats, 0.21 + (np.arange(63) + 0.5) * T]))
        bg = beat_analysis(beats, onsets, float(beats[-1] + T))
        assert abs(bg["fit"]["bpm"] - 128) < 0.3, bg["fit"]
        assert bg["fit"]["residual_max_ms"] < 15 and abs(bg["bpm"] - 128) < 0.3 and bg["accepted"], bg["gates"]
        results["beatgrid_times"] = f"bpm={bg['fit']['bpm']:.2f} winner={bg['bpm']} residual={bg['fit']['residual_max_ms']:.1f}ms"

        # 3 beat grid from synthetic audio (kick on beats, hihat on off-beats) via librosa
        sr = 22050
        bpm = 120
        dur = 16.0
        y = np.zeros(int(sr * dur), np.float32)
        tk = np.arange(int(sr * 0.12)) / sr
        kick = (np.sin(2 * np.pi * 70 * tk) * np.exp(-tk * 30)).astype(np.float32)
        th = np.arange(int(sr * 0.03)) / sr
        hat = (rng.normal(0, 1, len(th)) * np.exp(-th * 150)).astype(np.float32)
        hat = np.diff(np.concatenate([[0], hat])).astype(np.float32) * 0.6  # crude high-pass
        for b in range(int(dur * bpm / 60)):
            s = int((0.5 + b * 60 / bpm) * sr)
            if s + len(kick) < len(y):
                y[s:s + len(kick)] += kick
            s2 = int((0.5 + (b + 0.5) * 60 / bpm) * sr)
            if s2 + len(hat) < len(y):
                y[s2:s2 + len(hat)] += hat
        wav = os.path.join(tmp, "beat.wav")
        write_wav(wav, y * 0.8, sr)
        try:
            ba = beat_analysis(None, None, None, audio=wav)
            kinds = {h["k"] for h in ba["hits"]}
            assert abs(ba["bpm"] - 120) < 2, (ba["bpm"], ba["candidates"])
            assert abs(ba["t0"] - 0.5) < 0.03 and ba["accepted"], (ba["t0"], ba["gates"])
            assert "kick" in kinds
            results["beatgrid_audio"] = f"bpm={ba['bpm']} hits={len(ba['hits'])} kinds={sorted(kinds)} accepted={ba['accepted']}"
        except ImportError:
            results["beatgrid_audio"] = "skipped (librosa missing)"

        # 4 av-offset: render = ref delayed by 2048 samples (AAC priming)
        ref = rng.normal(0, 0.3, sr * 3).astype(np.float32)
        ren = np.concatenate([np.zeros(2048, np.float32), ref])[:len(ref)]
        write_wav(os.path.join(tmp, "ref.wav"), ref, sr)
        write_wav(os.path.join(tmp, "ren.wav"), ren, sr)
        off = av_offset(os.path.join(tmp, "ref.wav"), os.path.join(tmp, "ren.wav"))
        assert off["lag_samples"] == 2048, off
        results["av_offset"] = f"lag={off['lag_samples']} samples = {off['lag_frames']}f"

        # 5 sfx-peak: silence then hit at 0.25 s
        z = np.zeros(int(sr * 0.8), np.float32)
        p = int(0.25 * sr)
        z[p:p + len(kick)] = kick
        write_wav(os.path.join(tmp, "impact.wav"), z, sr)
        pk = sfx_peak(os.path.join(tmp, "impact.wav"))
        assert 0.24 <= pk["peak_sec"] <= 0.30, pk
        results["sfx_peak"] = f"peak={pk['peak_sec']}s"

        # 6 jy-plan
        tl = {"name": "st-draft", "fps": 30, "total_frames": 300, "plate": os.path.join(tmp, "plate.mp4"),
              "beat": {"t0": 0.0538, "T": 0.47609},
              "shots": [["open", 0, 101], ["mid", 101, 203], ["end", 203, 300]],
              "captions": [["你好", "HELLO", 10, 101], ["你好", "HELLO", 101, 150], ["再见", "BYE", 210, 280]],
              "caption_style": [{"css_px": 64, "color": "#2C2C2C", "center_y_px": 915},
                                {"css_px": 22, "color": "#575552", "center_y_px": 985}],
              "sfx": [{"file": "whoosh.mp3", "beat": 2, "peak_sec": 0.1, "volume": 0.5},
                      {"file": "pop.mp3", "frame": 40, "volume": 0.4, "cap_frames": 30},
                      {"file": "impact.mp3", "frame": 50, "volume": 0.6},
                      {"file": "tail.mp3", "frame": 290, "volume": 0.3}],
              "bgm": {"file": "bgm.mp3", "volume": 0.72}}
        plan = jy_plan(tl)
        assert plan["ok"], plan["errors"]
        segs = plan["plate"]["segments"]
        assert all(a["start"] + a["duration"] == b["start"] for a, b in zip(segs, segs[1:]))
        assert segs[-1]["start"] + segs[-1]["duration"] == plan["total_us"] == 10_000_000
        assert len(plan["text_tracks"]) == 2 and len(plan["text_tracks"][0]) == 2   # merged
        assert plan["sfx_lanes"] == 3, plan["sfx_lanes"]
        assert abs(plan["text_styles"][0]["size"] - 5.926) < 0.01
        assert abs(plan["text_styles"][0]["transform_y"] - (1 - 915 / 540)) < 1e-3
        assert plan["text_styles"][0]["color"] == [0.173, 0.173, 0.173]
        tail = [s for s in plan["sfx"] if s["file"] == "tail.mp3"][0]
        assert tail["start"] + tail["duration"] == plan["total_us"]
        results["jy_plan"] = (f"plate {len(segs)} segs gapless, captions merged to {len(plan['text_tracks'][0])}, "
                              f"sfx lanes={plan['sfx_lanes']}, size64px={plan['text_styles'][0]['size']}")

        # 7 jy-script compiles
        src = jy_script(plan, os.path.join(tmp, "staging"))
        compile(src, "builder.py", "exec")
        results["jy_script"] = f"{len(src.splitlines())} lines, compiles"

        # 8 jy-install into a fake draft root (twice -> replace path) + traversal refusal
        root = os.path.join(tmp, "JYRoot")
        os.makedirs(root)
        media = os.path.join(tmp, "media")
        os.makedirs(media)
        for nm in ("clip.mp4", "CLIP.mp4"):
            os.makedirs(os.path.join(media, nm.split(".")[0] + "_" + str(len(os.listdir(media)))))
        f1 = os.path.join(media, "clip_0", "clip.mp4")
        f2 = os.path.join(media, "CLIP_1", "CLIP.mp4")
        for f in (f1, f2):
            with open(f, "wb") as h:
                h.write(os.urandom(64))

        def mk_stage():
            st = os.path.join(tmp, "stage", "st-draft")
            os.makedirs(st, exist_ok=True)
            save_json(os.path.join(st, "draft_content.json"),
                      {"materials": {"videos": [{"path": f1}, {"path": f2}], "audios": [{"path": f1}]},
                       "tracks": [{}, {}]})
            return st
        r1 = install_draft(mk_stage(), root)
        r2 = install_draft(mk_stage(), root)
        v = verify_installed(r2["target"])
        res_names = sorted(os.listdir(os.path.join(r2["target"], "Resources")))
        assert r2["replaced"] and v["all_exist"] and v["all_inside_draft"] and v["media"] == 3
        assert res_names == ["CLIP-2.mp4", "clip.mp4"], res_names
        for bad in ("..", "a/b", "C:x", ""):
            try:
                safe_target(bad, root)
                raise AssertionError(f"accepted {bad!r}")
            except ValueError:
                pass
        results["jy_install"] = f"installed+replaced, resources={res_names}, traversal names refused, first copied={r1['bundle']['copied']}"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return {"self_test": "PASS", "checks": len(results), "results": results}

# ----------------------------------------------------------------------------- CLI


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="video-shotcraft ideas, native (Black Dragon)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("arc", help="energy-arc frame budget for a promo")
    a.add_argument("--seconds", type=float, required=True)
    a.add_argument("--fps", type=int, default=30)
    a.add_argument("--features", required=True, help="comma list of feature names")
    a.add_argument("--breath-cards", type=int)
    a.add_argument("--out")

    b = sub.add_parser("beatgrid", help="least-squares beat grid with acceptance gates")
    b.add_argument("--audio")
    b.add_argument("--beats", help="JSON list of beat seconds")
    b.add_argument("--onsets", help="JSON list of onset seconds")
    b.add_argument("--fps", type=int, default=30)
    b.add_argument("--out")

    o = sub.add_parser("av-offset", help="lag of rendered audio vs source (WAV)")
    o.add_argument("ref")
    o.add_argument("render")
    o.add_argument("--fps", type=int, default=30)

    p = sub.add_parser("sfx-peak", help="internal peak time of an SFX (WAV)")
    p.add_argument("file")
    p.add_argument("--fps", type=int, default=30)

    j = sub.add_parser("jy-plan", help="timeline JSON -> JianYing plan JSON")
    j.add_argument("timeline")
    j.add_argument("--out")

    s = sub.add_parser("jy-script", help="plan JSON -> pyJianYingDraft builder .py")
    s.add_argument("plan")
    s.add_argument("--staging", required=True)
    s.add_argument("--out", required=True)

    i = sub.add_parser("jy-install", help="install a staged draft into Windows JianYing")
    i.add_argument("--draft", required=True)
    i.add_argument("--draft-root")
    i.add_argument("--no-bundle", action="store_true")
    i.add_argument("--dry-run", action="store_true")

    sub.add_parser("self-test")
    for sp in sub.choices.values():
        sp.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    if args.cmd == "arc":
        r = plan_arc(args.seconds, args.fps, [x.strip() for x in args.features.split(",") if x.strip()],
                     args.breath_cards)
        if args.out:
            save_json(args.out, r)
        txt = "\n".join(f"{s['from']:>5}-{s['to']:<5} {s['sec']:>5}s {s['energy']:<8} {s['name']}" for s in r["shots"])
        emit(r, args.json, txt)
    elif args.cmd == "beatgrid":
        beats = np.array(load_json(args.beats), float) if args.beats else None
        ons = np.array(load_json(args.onsets), float) if args.onsets else None
        r = beat_analysis(beats, ons, None, audio=args.audio, fps=args.fps)
        if args.out:
            save_json(args.out, r)
        emit(r, args.json, f"BPM {r['bpm']}  t0 {r['t0']}s  accepted={r['accepted']}  gates={r['gates']}")
    elif args.cmd == "av-offset":
        r = av_offset(args.ref, args.render, fps=args.fps)
        emit(r, args.json, f"lag {r['lag_samples']} samples = {r['lag_ms']} ms = {r['lag_frames']} f (corr {r['correlation']})")
    elif args.cmd == "sfx-peak":
        r = sfx_peak(args.file, fps=args.fps)
        emit(r, args.json, f"peak at {r['peak_sec']} s ({r['peak_frames']} f)")
    elif args.cmd == "jy-plan":
        r = jy_plan(load_json(args.timeline))
        if args.out:
            save_json(args.out, r)
        emit(r, args.json, f"ok={r['ok']} plate={len(r['plate']['segments'])} text_tracks={len(r['text_tracks'])} "
                           f"sfx={len(r['sfx'])} lanes={r['sfx_lanes']} errors={r['errors']} warnings={r['warnings']}")
    elif args.cmd == "jy-script":
        src = jy_script(load_json(args.plan), args.staging)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(src)
        emit({"written": args.out, "lines": len(src.splitlines())}, args.json, f"wrote {args.out}")
    elif args.cmd == "jy-install":
        r = install_draft(args.draft, args.draft_root, not args.no_bundle, args.dry_run)
        if not args.dry_run:
            r["verify"] = verify_installed(r["target"])
        emit(r, args.json, json.dumps(r, ensure_ascii=False))
    elif args.cmd == "self-test":
        r = self_test()
        emit(r, args.json, "self-test PASS\n" + "\n".join(f"  {k}: {v}" for k, v in r["results"].items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
