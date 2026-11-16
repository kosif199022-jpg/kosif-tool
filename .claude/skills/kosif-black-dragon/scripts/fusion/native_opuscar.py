#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""native_opuscar.py - Black Dragon port of the lemo-opuscar (MIT, LemoLab 2026) director/technique QA ideas.

Ideas ported (re-written, not copied):
  * rhythm      : objective rhythm report of a finished film: motion energy, hard cuts, flat stretches,
                  spectral-flux onsets, near-silences, and visual-hit -> audio-onset alignment
                  (idea: styles/briefing-board/demo/tools/rhythm_report.py).
  * readcheck   : reading-time check for on-screen texts and subtitle cues, script-aware
                  (CJK, Arabic, Latin) (idea: core/render/readcheck.mjs + subcheck.mjs + DIRECTOR.md section 7).
  * lint        : director lint of a treatment JSON against DIRECTOR.md rules (hook <= 3 s, >= 4 camera moves,
                  one signature shot, >= 2 silences, >= 2 J/L sound transitions, pace variation, title >= 4 s,
                  "not the demo again": >= 4 of 6 axes differ).
  * self-test   : builds a tiny synthetic film + treatment in a temp dir and asserts real results.

Python 3.12, stdlib + numpy only (ffmpeg/ffprobe on PATH for `rhythm`). UTF-8 output, Windows paths OK.
Arabic reading rate (default 12 chars/s) is a KOSIF addition; the source has only CJK 4.5 and Latin 15.
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile, unicodedata
import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


# ------------------------------------------------------------------ helpers
def _median_filter(x, size):
    size = max(1, int(size) | 1)
    h = size // 2
    p = np.pad(np.asarray(x, float), h, mode="edge")
    return np.median(np.lib.stride_tricks.sliding_window_view(p, size), axis=1)


def _peaks(x, height, distance):
    """local maxima above a (per-sample) height, at least `distance` samples apart (greedy by size)."""
    x = np.asarray(x, float)
    h = np.broadcast_to(height, x.shape)
    cand = [i for i in range(1, len(x) - 1) if x[i] >= x[i - 1] and x[i] > x[i + 1] and x[i] > h[i]]
    cand.sort(key=lambda i: -x[i])
    keep = []
    for i in cand:
        if all(abs(i - j) >= distance for j in keep):
            keep.append(i)
    return np.array(sorted(keep), int)


def _ffprobe_fps(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=avg_frame_rate,width,height", "-of", "json", path],
                         capture_output=True, text=True, check=True).stdout
    s = json.loads(out)["streams"][0]
    n, d = s["avg_frame_rate"].split("/")
    return float(n) / float(d or 1)


def _need_ffmpeg():
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise SystemExit("ffmpeg/ffprobe not found on PATH")


# ------------------------------------------------------------------ rhythm
def rhythm(film, events=None, hit_types=None, flat=1.0, silence_db=-45.0, tol_ms=40.0, w=320, h=180):
    _need_ffmpeg()
    fps = _ffprobe_fps(film)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", film, "-vf", f"scale={w}:{h},format=gray",
                          "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(np.float32)
    diff = np.r_[0.0, np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))]
    n = len(diff)
    dur = n / fps
    med = _median_filter(diff, 25)
    # a hard cut is a spike far above the local median
    cuts = [round(i / fps, 3) for i in range(2, n) if diff[i] > 6 * max(med[i], 0.5) and diff[i] > 8]
    k = max(1, int(round(fps)))
    per_sec = [float(diff[i:i + k].mean()) for i in range(0, n - k + 1, k)]
    flat_secs = [i for i, v in enumerate(per_sec) if v < flat]

    # audio
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", film, "-vn", "-ac", "1", "-ar", "24000",
                          "-f", "f32le", "-"], capture_output=True).stdout
    x = np.frombuffer(pcm, np.float32).astype(np.float64)
    sr, hop, nfft = 24000, 240, 1024
    onsets, rms, quiet = np.array([]), [], []
    if len(x) > nfft:
        fr_a = np.lib.stride_tricks.sliding_window_view(np.pad(x, (0, nfft)), nfft)[::hop] * np.hanning(nfft)
        S = np.abs(np.fft.rfft(fr_a, axis=1))
        flux = np.r_[0.0, np.maximum(0, np.diff(np.log1p(S * 10), axis=0)).sum(1)]
        flux = flux / (np.percentile(flux, 99) + 1e-9)
        thr = _median_filter(flux, 31) + 0.12
        pk = _peaks(flux, thr, int(0.07 * sr / hop))
        # spectral frame i covers samples [i*hop, i*hop+nfft); the onset is near the frame start + nfft/2
        onsets = (pk * hop + nfft // 2) / sr
        for t in np.arange(0, len(x) / sr - 0.499, 0.5):
            seg = x[int(t * sr):int((t + 0.5) * sr)]
            rms.append((round(float(t), 2), float(20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-9))))
        quiet = [t for t, v in rms if v < silence_db]
    # merge contiguous quiet windows into silences
    silences = []
    for t in quiet:
        if silences and abs(silences[-1][1] - t) < 1e-6:
            silences[-1][1] = t + 0.5
        else:
            silences.append([t, t + 0.5])

    align = []
    if events:
        evs = json.load(open(events, encoding="utf-8"))
        evs = evs.get("ev", evs) if isinstance(evs, dict) else evs
        for e in evs:
            if hit_types and e.get("type") not in hit_types:
                continue
            if len(onsets):
                d = onsets - float(e["t"])
                j = int(np.argmin(np.abs(d)))
                align.append({"t": float(e["t"]), "type": e.get("type"), "offset_ms": round(float(d[j] * 1000), 1)})
            else:
                align.append({"t": float(e["t"]), "type": e.get("type"), "offset_ms": None})
    offs = [abs(a["offset_ms"]) for a in align if a["offset_ms"] is not None]
    shot_lens = np.diff([0.0] + cuts + [dur]) if dur else np.array([])
    pace_cv = float(np.std(shot_lens) / np.mean(shot_lens)) if len(shot_lens) > 1 else 0.0
    report = {
        "film": film, "fps": fps, "frames": n, "duration": round(dur, 3),
        "motion_mean": round(float(diff.mean()), 3), "motion_per_sec": [round(v, 2) for v in per_sec],
        "hard_cuts": cuts, "shot_lengths": [round(float(s), 3) for s in shot_lens],
        "pace_variation_cv": round(pace_cv, 3), "flat_seconds": flat_secs,
        "onsets": [round(float(o), 3) for o in onsets],
        "silences": [[round(a, 2), round(b, 2)] for a, b in silences],
        "alignment": align,
        "alignment_within_tol": f"{sum(o <= tol_ms for o in offs)}/{len(offs)}" if offs else None,
        "director_flags": [],
    }
    if len(silences) < 2:
        report["director_flags"].append("fewer than 2 silences/near-silences (DIRECTOR 6)")
    if len(shot_lens) > 2 and pace_cv < 0.25:
        report["director_flags"].append("even pace: shot lengths barely vary (DIRECTOR 7)")
    if offs and max(offs) > tol_ms:
        report["director_flags"].append(f"visual hits off their sound by > {tol_ms:.0f} ms")
    return report


# ------------------------------------------------------------------ readcheck
_CJK = re.compile(r"[぀-ヿ㐀-䶿一-鿿가-힯豈-﫿]")
_AR = re.compile(r"[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]")


def need_seconds(text, cjk_cps=4.5, ar_cps=12.0, latin_cps=15.0, pad=1.5, min_s=1.5):
    cjk = ar = other = 0
    for ch in text:
        if ch.isspace() or unicodedata.category(ch) == "Mn":   # Arabic harakat do not add reading time
            continue
        if _CJK.match(ch):
            cjk += 1
        elif _AR.match(ch):
            ar += 1
        else:
            other += 1
    return max(min_s, cjk / cjk_cps + ar / ar_cps + other / latin_cps + pad)


def _parse_srt(path):
    txt = open(path, encoding="utf-8-sig").read()
    cues = []
    for block in re.split(r"\n\s*\n", txt.strip()):
        lines = block.strip().splitlines()
        for i, l in enumerate(lines):
            m = re.match(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)", l)
            if m:
                g = [int(v) for v in m.groups()]
                t0 = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
                t1 = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
                cues.append({"t0": t0, "t1": t1, "text": " ".join(lines[i + 1:])})
                break
    return cues


def readcheck(path, frame=None, **rates):
    """texts JSON: [{id,text,t0,t1,(x0,y0,x1,y1),pass?,speech?,kind?}] or an .srt (kind=subtitle)."""
    items = _parse_srt(path) if path.lower().endswith(".srt") else json.load(open(path, encoding="utf-8"))
    if path.lower().endswith(".srt"):
        for c in items:
            c["kind"] = "subtitle"
    rows, bad = [], 0
    for i, it in enumerate(items):
        text, t0, t1 = it.get("text", ""), float(it["t0"]), float(it["t1"])
        held = t1 - t0
        row = {"id": str(it.get("id", i + 1)), "t0": t0, "held": round(held, 3), "text": text[:40]}
        if it.get("pass"):
            row.update(status="pass-through", need=None); rows.append(row); continue
        if frame and all(k in it for k in ("x0", "y0", "x1", "y1")):
            W, H = frame
            if not (it["x0"] >= 0 and it["y0"] >= 0 and it["x1"] <= W and it["y1"] <= H):
                row.update(status="BAD", need=None, why="never fully in frame"); bad += 1; rows.append(row); continue
        if it.get("kind") == "subtitle":
            need = max(1.8, float(it.get("speech", 0)) + 0.6)          # DIRECTOR 7 subtitle rule
        elif it.get("kind") == "title":
            need = max(4.0, need_seconds(text, **rates))               # title cards >= 4 s
        else:
            need = need_seconds(text, **rates)
        ok = held + 1e-6 >= need
        bad += not ok
        row.update(status="OK" if ok else "BAD", need=round(need, 3))
        rows.append(row)
    return {"file": path, "checked": len(rows), "bad": bad, "rows": rows}


# ------------------------------------------------------------------ director lint
MOVES = {"static", "push", "pull", "pan", "tilt", "track", "crane", "zoom", "dolly", "orbit", "handheld", "parallax", "focus-pull", "roll"}


def lint(treatment, demo=None):
    T = json.load(open(treatment, encoding="utf-8"))
    shots = T.get("shots", [])
    issues, notes = [], []
    dur = float(T.get("duration") or sum(float(s.get("dur", 0)) for s in shots))
    if not (30 <= dur <= 60):
        notes.append(f"length {dur:.1f}s is outside the default 30-60 s")
    hook = T.get("hook_t")
    if hook is None or float(hook) > 3.0:
        issues.append("no hook within the first 3 s (hook_t)")
    moves = {str(s.get("move", "")).lower() for s in shots} - {"", "static"}
    if len(moves) < 4:
        issues.append(f"only {len(moves)} distinct camera moves (need >= 4): {sorted(moves)}")
    if not any(s.get("signature") for s in shots):
        issues.append("no signature shot marked")
    for s in shots:
        if not s.get("why"):
            issues.append(f"shot {s.get('id')} has no 'why' (every shot needs a reason)")
    framings = {s.get("framing") for s in shots if s.get("framing")}
    if len(framings) < 3:
        issues.append(f"framing barely changes ({sorted(framings)})")
    sound = T.get("sound", {})
    if len(sound.get("silences", [])) < 2:
        issues.append("fewer than 2 planned silences before the turn/peak")
    jl = [t for t in sound.get("transitions", []) if str(t.get("type", "")).upper() in ("J", "L", "J-CUT", "L-CUT")]
    if len(jl) < 2:
        issues.append("fewer than 2 sound transitions (J/L cuts)")
    lens = [float(s.get("dur", 0)) for s in shots if s.get("dur")]
    if len(lens) > 2:
        cv = float(np.std(lens) / np.mean(lens))
        if cv < 0.25:
            issues.append(f"even pace: shot-length variation {cv:.2f} < 0.25 (needs a breath and an acceleration)")
        if max(lens) < 2.5:
            issues.append("no breath: no shot or hold of at least 2.5 s")
    for s in T.get("subtitles", []):
        d = float(s["t1"]) - float(s["t0"])
        if d + 1e-6 < max(1.8, float(s.get("speech", 0)) + 0.6):
            issues.append(f"subtitle at {s['t0']}s held {d:.2f}s < max(1.8, speech+0.6)")
    for s in T.get("titles", []):
        if float(s["t1"]) - float(s["t0"]) < 4.0:
            issues.append(f"title card at {s['t0']}s shorter than 4 s")
    if not T.get("native_move"):
        issues.append("no native move named (the medium-only moment at the peak)")
    if len(T.get("structures", [])) < 3:
        notes.append("treatment should list three candidate structures")
    diff = None
    if demo:
        D = json.load(open(demo, encoding="utf-8"))
        axes = ["structure", "opening", "signature", "camera_path", "score_shape", "ending"]
        same = [a for a in axes if T.get(a) and D.get(a) and str(T[a]).strip().lower() == str(D[a]).strip().lower()]
        diff = len(axes) - len(same)
        if diff < 4:
            issues.append(f"too close to the demo: only {diff}/6 axes differ (same: {same})")
    return {"treatment": treatment, "duration": dur, "distinct_moves": sorted(moves), "demo_axes_differ": diff,
            "issues": issues, "notes": notes, "ok": not issues}


# ------------------------------------------------------------------ self-test
def self_test():
    tmp = tempfile.mkdtemp(prefix="opuscar_st_")
    results = {}
    try:
        # --- readcheck
        texts = [
            {"id": "en", "text": "Every shot needs a reason", "t0": 0, "t1": 4.0},          # 22 chars -> 2.97 s, OK
            {"id": "ar", "text": "كل لقطة لازم يكون ليها سبب واضح", "t0": 5, "t1": 6.5},    # 25 ar -> 3.58 s, BAD
            {"id": "zh", "text": "每个镜头都要有理由", "t0": 7, "t1": 9.0},                    # 9 cjk -> 3.5 s, BAD
            {"id": "sign", "text": "SHOP", "t0": 9, "t1": 9.2, "pass": True},
            {"id": "edge", "text": "cut off", "t0": 0, "t1": 9, "x0": 1800, "y0": 10, "x1": 2100, "y1": 60},
            {"id": "sub", "kind": "subtitle", "text": "hi", "t0": 1, "t1": 2.5, "speech": 1.2},  # needs 1.8, BAD
            {"id": "title", "kind": "title", "text": "THE END", "t0": 20, "t1": 24.5},          # OK
        ]
        tp = os.path.join(tmp, "texts.json")
        json.dump(texts, open(tp, "w", encoding="utf-8"), ensure_ascii=False)
        rc = readcheck(tp, frame=(1920, 1080))
        st = {r["id"]: r["status"] for r in rc["rows"]}
        assert st == {"en": "OK", "ar": "BAD", "zh": "BAD", "sign": "pass-through", "edge": "BAD", "sub": "BAD", "title": "OK"}, st
        assert abs(need_seconds("كَتَبَ") - (3 / 12 + 1.5)) < 1e-9          # harakat ignored
        srt = os.path.join(tmp, "a.srt")
        open(srt, "w", encoding="utf-8").write("1\n00:00:01,000 --> 00:00:02,000\nقصير\n\n2\n00:00:03,000 --> 00:00:05,500\nOK line\n")
        rs = readcheck(srt)
        assert [r["status"] for r in rs["rows"]] == ["BAD", "OK"], rs
        results["readcheck"] = f"{rc['checked']} texts, {rc['bad']} bad as expected; srt 1/2 bad"

        # --- lint
        good = {"duration": 40, "hook_t": 1.2, "native_move": "ink blooms into the next scene",
                "structures": ["journey", "before/after", "countdown"],
                "structure": "countdown", "opening": "clock face", "signature": "oner", "camera_path": "spiral",
                "score_shape": "build-drop", "ending": "echo",
                "shots": [{"id": 1, "framing": "wide", "move": "push", "dur": 3, "why": "set the place"},
                          {"id": 2, "framing": "close", "move": "pan", "dur": 1.2, "why": "detail"},
                          {"id": 3, "framing": "medium", "move": "track", "dur": 6, "why": "breath", "signature": True},
                          {"id": 4, "framing": "insert", "move": "crane", "dur": 0.8, "why": "hit"},
                          {"id": 5, "framing": "wide", "move": "pull", "dur": 4, "why": "scale reveal"}],
                "sound": {"silences": [10.0, 30.5], "transitions": [{"type": "J", "t": 12}, {"type": "L", "t": 25}]},
                "subtitles": [{"t0": 2, "t1": 4, "speech": 1.3}], "titles": [{"t0": 35, "t1": 40}]}
        bad = {"duration": 40, "hook_t": 5, "shots": [{"id": i, "framing": "wide", "move": "push", "dur": 2} for i in range(6)],
               "sound": {}, "subtitles": [{"t0": 1, "t1": 2}], "titles": [{"t0": 0, "t1": 2}],
               "structure": "countdown", "opening": "clock face", "signature": "oner", "camera_path": "spiral",
               "score_shape": "build-drop", "ending": "other"}
        gp, bp = os.path.join(tmp, "good.json"), os.path.join(tmp, "bad.json")
        json.dump(good, open(gp, "w", encoding="utf-8")); json.dump(bad, open(bp, "w", encoding="utf-8"))
        dp = os.path.join(tmp, "demo.json")
        json.dump({"structure": "journey", "opening": "clock face", "signature": "fold", "camera_path": "line",
                   "score_shape": "drone", "ending": "loop"}, open(dp, "w", encoding="utf-8"))
        lg, lb = lint(gp, demo=dp), lint(bp, demo=gp)
        assert lg["ok"] and lg["demo_axes_differ"] == 5, lg
        assert not lb["ok"] and len(lb["issues"]) >= 9 and lb["demo_axes_differ"] == 1, lb
        results["lint"] = f"good treatment ok ({lg['demo_axes_differ']}/6 differ); bad treatment {len(lb['issues'])} issues"

        # --- rhythm on a synthetic film
        if shutil.which("ffmpeg"):
            fps, W, H, dur = 24, 160, 90, 6.0
            n = int(fps * dur)
            frames = np.zeros((n, H, W, 3), np.uint8)
            for i in range(n):
                t = i / fps
                if t < 2.0:
                    frames[i] = 40                                               # flat dark stretch
                elif t < 4.0:
                    frames[i] = 200; x = int((t - 2) * 50); frames[i, 30:60, x:x + 20] = (255, 0, 0)  # bright, moving
                else:
                    frames[i] = 90; frames[i, :, : int((t - 4) * 40)] = 160     # a wipe
            sr = 48000
            a = np.zeros(int(sr * dur), np.float32)
            clicks = [0.5, 1.0, 2.0, 3.25, 4.0, 5.5]
            rng = np.random.default_rng(1)
            for c in clicks:
                s = int(c * sr); L = int(0.03 * sr)
                a[s:s + L] += (rng.standard_normal(L) * np.exp(-np.arange(L) / (0.006 * sr)) * 0.8).astype(np.float32)
            wav = os.path.join(tmp, "a.f32"); a.tofile(wav)
            film = os.path.join(tmp, "film.mp4")
            p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                                  "-r", str(fps), "-i", "-", "-f", "f32le", "-ar", str(sr), "-ac", "1", "-i", wav,
                                  "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-c:a", "aac", "-b:a", "192k",
                                  "-shortest", film], stdin=subprocess.PIPE)
            p.communicate(frames.tobytes())
            assert p.returncode == 0 and os.path.getsize(film) > 0
            ev = os.path.join(tmp, "ev.json")
            json.dump({"ev": [{"t": 2.0, "type": "cut"}, {"t": 3.25, "type": "hit"}, {"t": 4.0, "type": "cut"}]}, open(ev, "w"))
            r = rhythm(film, events=ev, w=W, h=H)
            assert any(abs(c - 2.0) < 0.05 for c in r["hard_cuts"]) and any(abs(c - 4.0) < 0.05 for c in r["hard_cuts"]), r["hard_cuts"]
            assert 0 in r["flat_seconds"] and 1 in r["flat_seconds"], r["flat_seconds"]
            for c in clicks:
                assert any(abs(o - c) < 0.04 for o in r["onsets"]), (c, r["onsets"])
            assert all(abs(x["offset_ms"]) <= 40 for x in r["alignment"]), r["alignment"]
            assert len(r["silences"]) >= 2, r["silences"]
            results["rhythm"] = (f"cuts {r['hard_cuts']}, {len(r['onsets'])} onsets, flat secs {r['flat_seconds']}, "
                                 f"silences {r['silences']}, hits aligned {r['alignment_within_tol']}")
        else:
            results["rhythm"] = "SKIPPED (no ffmpeg)"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return results


# ------------------------------------------------------------------ cli
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("rhythm", help="rhythm report of a finished film")
    r.add_argument("film"); r.add_argument("--events"); r.add_argument("--hit-types", nargs="*")
    r.add_argument("--flat", type=float, default=1.0); r.add_argument("--silence-db", type=float, default=-45.0)
    r.add_argument("--tol-ms", type=float, default=40.0)
    c = sub.add_parser("readcheck", help="reading time of on-screen texts JSON or an .srt")
    c.add_argument("file"); c.add_argument("--size", default=None, help="WxH frame for box checks, e.g. 1080x1920")
    c.add_argument("--cjk-cps", type=float, default=4.5); c.add_argument("--ar-cps", type=float, default=12.0)
    c.add_argument("--latin-cps", type=float, default=15.0); c.add_argument("--pad", type=float, default=1.5)
    c.add_argument("--min", type=float, default=1.5)
    l = sub.add_parser("lint", help="director lint of a treatment JSON"); l.add_argument("treatment"); l.add_argument("--demo")
    sub.add_parser("self-test")
    for s in sub.choices.values():
        s.add_argument("--json", action="store_true", help="JSON output")
    a = ap.parse_args()

    if a.cmd == "self-test":
        res = self_test()
        if a.json:
            print(json.dumps({"self_test": "PASS", **res}, ensure_ascii=False, indent=1))
        else:
            for k, v in res.items():
                print(f"{k}: {v}")
            print("SELF-TEST PASS")
        return 0
    if a.cmd == "rhythm":
        res = rhythm(a.film, a.events, set(a.hit_types) if a.hit_types else None, a.flat, a.silence_db, a.tol_ms)
        code = 1 if res["director_flags"] else 0
    elif a.cmd == "readcheck":
        frame = tuple(int(v) for v in a.size.lower().split("x")) if a.size else None
        res = readcheck(a.file, frame, cjk_cps=a.cjk_cps, ar_cps=a.ar_cps, latin_cps=a.latin_cps, pad=a.pad, min_s=a.min)
        code = 1 if res["bad"] else 0
    else:
        res = lint(a.treatment, a.demo)
        code = 0 if res["ok"] else 1
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    elif a.cmd == "readcheck":
        for r_ in res["rows"]:
            print(f"{r_['status']:12s} {r_['id']:10s} t0={r_['t0']:.2f} held={r_['held']:.2f} need={r_['need']} {r_.get('why', '')} {r_['text']!r}")
    elif a.cmd == "lint":
        print("OK" if res["ok"] else "ISSUES"); [print(" -", i) for i in res["issues"]]; [print(" ~", n) for n in res["notes"]]
    else:
        print(f"{res['duration']}s @ {res['fps']:.3f} fps, cuts {res['hard_cuts']}, pace cv {res['pace_variation_cv']}")
        print(f"onsets {len(res['onsets'])}, silences {res['silences']}, flat seconds {res['flat_seconds']}")
        if res["alignment"]:
            print(f"alignment {res['alignment_within_tol']}: " + ", ".join(f"{x['type']}@{x['t']} {x['offset_ms']}ms" for x in res["alignment"]))
        [print(" !", f) for f in res["director_flags"]]
    return code


if __name__ == "__main__":
    sys.exit(main())
