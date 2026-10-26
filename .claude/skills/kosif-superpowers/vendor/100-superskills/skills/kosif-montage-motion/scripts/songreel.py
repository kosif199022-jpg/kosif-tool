"""KOSIF songreel — a song → a lyric reel cut from collected footage (Pinterest pins, TikTok links or any folder):
the song is understood (lyrics on their times, structure, energy, the strongest excerpt), every section gets the
searches that match its meaning, the clips are matched to the sections and cut on the beats, and the words are
animated over the footage (the verse engine with a video plate) — then the delivery gate and the post pack.

    python songreel.py analyze SONG --name NAME [--lyrics lyrics.txt] [--seconds 45] [--start S] [--model small]
    python songreel.py queries NAME                                    # the searches per section (edit songreel.json)
    python songreel.py cut NAME --media DIR [--grade auto] [--fps 30]   # clips → sections → shots on the beats → plate
    python songreel.py build NAME [--title "…"] [--sub "…"] [--mood night] [--accent "#E7B65A"] [--credit "…"]
                                  [--model large-v3] [--render] [--draft]

analyze  · structure pass with a fast model (`small`, no speech filter: singing under a music bed) over the whole song;
           with --lyrics the true words are aligned onto it; beats/downbeats/BPM; loudness per second; sections from the
           pauses and the instrumentals; the refrain (a line sung ≥ 2 times) and the peak; the excerpt (default 45 s;
           Reels/Shorts take up to 180) that starts on a downbeat before a line, ends after a line, and scores highest on
           loudness + refrain/peak; Pinterest searches per section from the meaning of its words (editable).
cut      · every clip measured (length, shape, brightness, warmth, saturation, motion); shots on the beat grid —
           2 beats in loud sections, 4 in the middle, 8 in quiet ones, every section start and the payoff line a forced
           cut; each shot takes the clip whose motion matches the section's energy and whose look stays near the set
           (no repeat back-to-back, fewest uses first, a clip fetched for that section's search preferred), its most
           active unused window; one grade over all → an all-intra plate the composition seeks frame-exactly.
build    · the excerpt's audio (fades), word times from the accurate model on the excerpt only, aligned to the lyrics →
           the verse composition over the plate (words rise on their times, keyword glow, payoff light sweep, a push
           per shot, kick nudges, section flashes, type kept off faces) → render → gate → poster → post-pack skeleton.
Nothing is downloaded or posted here: collecting is `kmotion fetch` (Pinterest through the browser pane, signed in by
the user); credits from fetch-credits.json go with the film.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

import qa  # noqa: E402

FF = shutil.which("ffmpeg") or "ffmpeg"
FP = shutil.which("ffprobe") or "ffprobe"
VIDEO_EXT = {".mp4", ".mov", ".webm", ".mkv", ".m4v", ".avi"}
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp"}

# meaning → what to search (Pinterest works best in English; the Arabic goes along for Arabic boards). Keys are the
# verse concepts plus a few song-specific ones; matched on the words of each section.
SCENES = {
    "home": ["old wooden door night", "empty house window light", "old arabic house courtyard", "keys in hand close up"],
    "moon": ["city night rain street lights", "lonely street lamp night", "night window rain drops", "moon clouds night sky"],
    "rain": ["rain on window cinematic", "rainy street night reflections", "storm clouds dramatic sky", "sea waves night"],
    "road": ["lonely man walking street night", "train station empty night", "airport window planes night", "long road horizon"],
    "heart": ["hands holding old photo", "mother hands close up", "tears close up cinematic", "candle light dark room"],
    "clock": ["clock ticking close up", "time lapse city night", "old clock dark", "hourglass sand"],
    "light": ["sunrise golden horizon", "dawn mosque minaret silhouette", "light rays through clouds", "golden hour field"],
    "sun": ["sunrise over city", "morning light window", "golden sunrise sea", "bright sky clouds timelapse"],
    "trophy": ["mountain summit sunrise", "man standing hill horizon", "city skyline sunrise", "running at dawn"],
    "money": ["city lights skyline night", "busy street crowd night", "neon city rain", "office window night city"],
    "question": ["fog forest mysterious", "man looking at horizon", "misty road", "silhouette window thinking"],
    "check": ["sunrise hope", "open road sunrise", "birds flying sunset", "light at end of tunnel"],
    "alone": ["man alone dark room", "empty chair room", "lonely bench night", "shadow on wall street lamp"],
    "phone": ["phone screen night bed", "video call mother", "hand touching screen", "phone light dark room"],
    "bread": ["fresh bread oven", "family table food warm", "steam coffee morning", "old kitchen warm light"],
}
EXTRA_ROOTS = {
    "alone": "وحد وحدي وحيد وحده وحدها غريب غربه غربتي ظل ظلي فراغ خلا خالي alone lonely empty",
    "phone": "شاشه هاتف تلفون تلفاز صوره رساله phone screen call",
    "bread": "خبز عشاء طعام اكل كل قهوه bread dinner food",
}
MOOD_GRADE = {"night": "blue_hour", "dawn": "golden_hour", "gold": "golden_hour", "sea": "teal_orange", "ink": "vintage_film"}


def _run(cmd: list[str]) -> subprocess.CompletedProcess:
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        raise RuntimeError(r.stderr[-1500:])
    return r


def _dur(p: Path) -> float:
    try:
        return float(_run([FP, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).stdout.strip())
    except (RuntimeError, ValueError):
        return 0.0


def workdir(name: str) -> Path:
    import motion as MO
    d = MO.PROJECTS / MO.safe_name(name) / "songreel"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _load(name: str) -> tuple[Path, dict]:
    d = workdir(name)
    f = d / "songreel.json"
    if not f.exists():
        raise SystemExit(f"run `songreel analyze SONG --name {name}` first")
    return d, json.loads(f.read_text(encoding="utf-8"))


def _save(d: Path, spec: dict) -> None:
    (d / "songreel.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")


# ───────────────────────── understanding the song ─────────────────────────
def asr(audio: Path, model: str) -> list[dict]:
    """Words with times; singing under music needs the speech filter off (transcribe retries without it)."""
    import transcribe as T
    return T.transcribe(audio, model, "ar", None, True, None)


def loudness(wav: Path, hop: float = 0.5) -> np.ndarray:
    """RMS in dB per hop seconds, normalised to 0..1 over the song (5th → 95th percentile)."""
    from verse import _mono
    x, sr = _mono(wav)
    n = int(sr * hop)
    v = np.array([np.sqrt(np.mean(x[i:i + n] ** 2)) for i in range(0, max(1, len(x) - n), n)]) + 1e-9
    db = 20 * np.log10(v)
    lo, hi = np.percentile(db, 5), np.percentile(db, 95)
    return np.clip((db - lo) / max(1e-6, hi - lo), 0, 1)


def mean_level(lv: np.ndarray, a: float, b: float, hop: float = 0.5) -> float:
    i, j = int(a / hop), max(int(a / hop) + 1, int(b / hop))
    return float(lv[i:j].mean()) if j <= len(lv) and i < len(lv) else float(lv[i:].mean() if i < len(lv) else 0)


def concepts_of(words: list[str]) -> list[str]:
    """The concepts a section's words point to, most frequent first (verse's table + a few song ones)."""
    import verse as VE
    found: dict[str, int] = {}
    for w in words:
        k = VE.concept_of(w)
        n = VE.norm(w)
        cands = {n} | {n[len(p):] for p in ("وال", "فال", "بال", "لل", "ال", "و", "ف", "ب", "ل") if n.startswith(p) and len(n) - len(p) >= 2}
        for kind, roots in EXTRA_ROOTS.items():
            if any(c.startswith(r) for c in cands for r in roots.split() if len(r) >= 3):
                found[kind] = found.get(kind, 0) + 2               # the song words are stronger evidence
        if k:
            found[k] = found.get(k, 0) + 1
    return sorted(found, key=lambda x: -found[x])


def sections_of(lines: list[list[dict]], duration: float, lv: np.ndarray) -> list[dict]:
    """Vocal sections split at pauses ≥ 3 s; gaps ≥ 6 s become instrumental sections."""
    secs: list[dict] = []
    if not lines:
        return [{"i": 0, "t": 0.0, "end": round(duration, 3), "kind": "instrumental", "lines": []}]
    if lines[0][0]["start"] >= 6:
        secs.append({"t": 0.0, "end": lines[0][0]["start"], "kind": "instrumental", "lines": []})
    cur = {"t": lines[0][0]["start"], "kind": "vocal", "lines": [0]}
    for i in range(1, len(lines)):
        gap = lines[i][0]["start"] - lines[i - 1][-1]["end"]
        if gap >= 3.0:
            cur["end"] = lines[i - 1][-1]["end"]
            secs.append(cur)
            if gap >= 6.0:
                secs.append({"t": lines[i - 1][-1]["end"], "end": lines[i][0]["start"], "kind": "instrumental", "lines": []})
            cur = {"t": lines[i][0]["start"], "kind": "vocal", "lines": [i]}
        else:
            cur["lines"].append(i)
    cur["end"] = lines[-1][-1]["end"]
    secs.append(cur)
    if duration - secs[-1]["end"] >= 6:
        secs.append({"t": secs[-1]["end"], "end": duration, "kind": "instrumental", "lines": []})
    # a song sung through without 3 s pauses: split long vocal sections at their widest line gaps (each part ≥ 3 lines
    # and ≥ 10 s) until none is longer than 30 s — verses and choruses, not one 90 s block
    out: list[dict] = []
    stack = list(secs)
    while stack:
        s = stack.pop(0)
        li = s["lines"]
        if s["kind"] != "vocal" or s["end"] - s["t"] <= 30 or len(li) < 6:
            out.append(s)
            continue
        cands = [k for k in range(3, len(li) - 2) if lines[li[k]][0]["start"] - s["t"] >= 10 and s["end"] - lines[li[k]][0]["start"] >= 10]
        if not cands:
            out.append(s)
            continue
        k = max(cands, key=lambda k: (lines[li[k]][0]["start"] - lines[li[k - 1]][-1]["end"], -abs(k - len(li) / 2)))
        cut_t = lines[li[k]][0]["start"]
        stack[:0] = [{"t": s["t"], "end": lines[li[k - 1]][-1]["end"], "kind": "vocal", "lines": li[:k]},
                     {"t": cut_t, "end": s["end"], "kind": "vocal", "lines": li[k:]}]
    secs = out
    for i, s in enumerate(secs):
        s["i"] = i
        s["t"], s["end"] = round(s["t"], 3), round(s["end"], 3)
        s["energy"] = round(mean_level(lv, s["t"], s["end"]), 3)
    return secs


def refrains(lines: list[list[dict]], floor: float = 0.8) -> set[int]:
    """Lines heard more than once: the same words give or take an interjection («آه.. ما أقسى» = «ما أقسى»)."""
    import difflib
    import verse as VE
    keys = [" ".join(VE.norm(w["text"]) for w in ln) for ln in lines]
    out: set[int] = set()
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            if len(lines[i]) >= 2 and len(lines[j]) >= 2:
                a, b = keys[i], keys[j]
                r = difflib.SequenceMatcher(None, a, b).ratio()
                short, long_ = sorted((a, b), key=len)
                if r >= floor or (len(short) >= 12 and short in long_ and len(short) / len(long_) >= 0.75):
                    out |= {i, j}
    return out


def _snap_before(t: float, grid: list[float], max_lead: float) -> float:
    c = [g for g in grid if t - max_lead <= g <= t]
    return max(c) if c else max(0.0, t - min(1.0, max_lead))


def _snap_after(t: float, grid: list[float], max_tail: float, duration: float) -> float:
    c = [g for g in grid if t <= g <= t + max_tail]
    return min(c) if c else min(duration, t + min(1.2, max_tail))


def choose_excerpt(lines: list[list[dict]], sections: list[dict], bt: dict, lv: np.ndarray, seconds: float, duration: float,
                   refrain: set[int], peak: int | None) -> list[dict]:
    """Candidate windows (a downbeat before a line → after the last line that fits), best first."""
    grid = bt.get("downbeats") or bt.get("beats") or []
    starts_of_sections = {s["lines"][0] for s in sections if s["lines"]}
    out = []
    for i, ln in enumerate(lines):
        a = _snap_before(ln[0]["start"] - 0.35, grid, 2.5)
        j = max((k for k in range(i, len(lines)) if lines[k][-1]["end"] <= a + seconds - 1.0), default=None)
        if j is None or j - i < 1:
            continue
        b = _snap_after(lines[j][-1]["end"] + 0.6, grid, 2.5, duration)
        if b - a < 0.6 * seconds:
            continue
        idx = set(range(i, j + 1))
        score = mean_level(lv, a, b) + (0.6 if idx & refrain else 0) + (0.5 if peak is not None and peak in idx else 0) \
            + (0.25 if i in starts_of_sections else 0) - (0.3 if j + 1 < len(lines) and lines[j + 1][0]["start"] - lines[j][-1]["end"] < 0.6 else 0)
        out.append({"start": round(a, 3), "end": round(b, 3), "seconds": round(b - a, 2), "first_line": i, "last_line": j,
                    "score": round(score, 3), "text": [" ".join(w["text"] for w in lines[k]) for k in range(i, j + 1)]})
    out.sort(key=lambda c: -c["score"])
    keep: list[dict] = []
    for c in out:                                              # distinct candidates (not the same window shifted)
        if all(abs(c["start"] - k["start"]) > 8 for k in keep):
            keep.append(c)
        if len(keep) == 3:
            break
    return keep


def analyze(song: Path, name: str, lyrics: Path | None = None, seconds: float = 45.0, start: float | None = None,
            model: str = "small") -> dict:
    import verse as VE
    d = workdir(name)
    wav = d / "song.wav"
    _run([FF, "-y", "-v", "error", "-i", str(song), "-vn", "-ac", "2", "-ar", "48000", str(wav)])
    duration = _dur(wav)
    asr_file = d / f"structure.{model}.words.json"
    if asr_file.exists():                                      # the slow part is cached per model
        segs = json.loads(asr_file.read_text(encoding="utf-8"))
    else:
        segs = asr(wav, model)
        asr_file.write_text(json.dumps(segs, ensure_ascii=False, indent=1), encoding="utf-8")
    words = [w for s in segs for w in s["words"]]
    if lyrics:
        true = VE.read_text(lyrics)
        lines = [ln for ln in VE.align(true, words) if ln] if words else VE.estimate(true, wav)
        timing = "aligned" if words else "estimated"
    else:
        lines = [p for s in segs for p in VE.segment([dict(w) for w in s["words"]]) if p]
        timing = "asr"
    lv = loudness(wav)
    bt = qa.beats(wav)
    secs = sections_of(lines, duration, lv)
    refrain = refrains(lines)
    vocal = [s for s in secs if s["kind"] == "vocal"]
    peak_sec = max(vocal, key=lambda s: s["energy"]) if vocal else None
    peak = peak_sec["lines"][0] if peak_sec else None
    cands = choose_excerpt(lines, secs, bt, lv, seconds, duration, refrain, peak)
    if start is not None:
        a = float(start)
        b = min(duration, a + seconds)
        inside = [i for i, ln in enumerate(lines) if ln[0]["start"] >= a and ln[-1]["end"] <= b]
        ex = {"start": round(a, 3), "end": round(b, 3), "seconds": round(b - a, 2), "first_line": inside[0] if inside else None,
              "last_line": inside[-1] if inside else None, "score": None, "text": [" ".join(w["text"] for w in lines[i]) for i in inside], "chosen_by": "user"}
    elif cands:
        ex = {**cands[0], "chosen_by": "score"}
    else:
        ex = {"start": 0.0, "end": round(min(duration, seconds), 3), "seconds": round(min(duration, seconds), 2), "first_line": None,
              "last_line": None, "score": None, "text": [], "chosen_by": "fallback (no lyric lines found)"}
    for s in secs:
        s["text"] = [" ".join(w["text"] for w in lines[i]) for i in s["lines"]]
        ws = [w["text"] for i in s["lines"] for w in lines[i]]
        s["concepts"] = concepts_of(ws)[:3] if ws else (["moon"] if s["energy"] < 0.5 else ["light"])
        q = [x for c in s["concepts"] for x in SCENES.get(c, [])[:2]]
        s["queries"] = list(dict.fromkeys(q))[:4] or SCENES["moon"][:2]
        s["in_excerpt"] = s["end"] > ex["start"] and s["t"] < ex["end"]
    spec = {"song": str(song), "wav": str(wav), "duration": round(duration, 3), "timing": timing, "structure_model": model,
            "bpm": bt.get("bpm"), "beats": bt.get("beats"), "downbeats": bt.get("downbeats"),
            "lines": [{"i": i, "t": ln[0]["start"], "end": ln[-1]["end"], "text": " ".join(w["text"] for w in ln),
                       "words": ln, "refrain": i in refrain} for i, ln in enumerate(lines)],
            "sections": secs, "peak_section": peak_sec["i"] if peak_sec else None, "excerpt": ex, "candidates": cands,
            "loudness_hop": 0.5, "loudness": [round(float(v), 3) for v in lv]}
    _save(d, spec)
    return {"workdir": str(d), "duration": spec["duration"], "bpm": spec["bpm"], "timing": timing, "lines": len(lines),
            "sections": [{"i": s["i"], "t": s["t"], "end": s["end"], "kind": s["kind"], "energy": s["energy"],
                          "concepts": s["concepts"], "in_excerpt": s["in_excerpt"]} for s in secs],
            "refrain_lines": sorted(refrain), "peak_section": spec["peak_section"], "excerpt": ex,
            "other_candidates": cands[1:]}


def queries(name: str) -> dict:
    d, spec = _load(name)
    return {"excerpt": [spec["excerpt"]["start"], spec["excerpt"]["end"]],
            "sections": [{"i": s["i"], "t": s["t"], "end": s["end"], "text": s["text"], "concepts": s["concepts"],
                          "queries": s["queries"], "media_folder": f"s{s['i']:02d}"}
                         for s in spec["sections"] if s["in_excerpt"]],
            "how": "collect each section's clips into MEDIA/sNN/ (kmotion fetch LINKS --out MEDIA/sNN) so cut prefers them there; "
                   "edit the queries in songreel.json if the meaning calls for other pictures"}


# ───────────────────────── clips → shots → plate ─────────────────────────
def media_files(root: Path) -> list[Path]:
    """Videos (and images) under root; a `.edit.mp4` copy from kmotion fetch replaces its original."""
    files = sorted(f for f in Path(root).rglob("*") if f.is_file() and f.suffix.lower() in VIDEO_EXT | IMAGE_EXT
                   and "plate" not in f.parts)
    edits = {(f.parent, f.name[: -len(".edit.mp4")]) for f in files if f.name.endswith(".edit.mp4")}
    return [f for f in files if f.name.endswith(".edit.mp4") or (f.parent, f.stem) not in edits]


def measure_clip(p: Path) -> dict | None:
    import montage as MT
    if p.suffix.lower() in IMAGE_EXT:
        w, h = MT._dims(p)
        from PIL import Image
        a = np.asarray(Image.open(p).convert("RGB").resize((160, max(2, int(160 * h / max(1, w))))), np.float32)
        return {"file": str(p), "image": True, "seconds": 1e9, "w": w, "h": h, "luma": float(a.mean() / 255),
                "warmth": float((a[..., 0].mean() - a[..., 2].mean()) / 255), "sat": float((a.max(-1) - a.min(-1)).mean() / 255),
                "motion": 0.0, "energy": [0.0]}
    secs = _dur(p)
    if secs < 1.0:
        return None
    w, h = MT._dims(p)
    if not w:
        return None
    frames = list(qa._frames(p, 2.0, 160, gray=False))
    if not frames:
        return None
    a = np.stack(frames).astype(np.float32)
    e = MT.energy(p)
    return {"file": str(p), "image": False, "seconds": round(secs, 3), "w": w, "h": h, "luma": round(float(a.mean() / 255), 4),
            "warmth": round(float((a[..., 0].mean() - a[..., 2].mean()) / 255), 4),
            "sat": round(float((a.max(-1) - a.min(-1)).mean() / 255), 4), "motion": round(float(np.median(e)), 4),
            "energy": [round(float(v), 3) for v in e]}


def shot_grid(spec: dict, fps: int) -> list[dict]:
    """Shots on the beat grid inside the excerpt — ≈1.4 s where loud, ≈2.6 s in the middle, ≈3.8 s where quiet, counted
    in beats; forced cuts at section starts and at the payoff (the last refrain line, else the loudest line), never
    within 0.9 s of either end; every cut on a whole frame."""
    ex = spec["excerpt"]
    a0, a1 = ex["start"], ex["end"]
    beats = [b for b in (spec.get("beats") or []) if a0 < b < a1 - 0.3]
    if len(beats) < 4:                                          # no beat grid: every 2 s
        beats = list(np.arange(a0 + 2.0, a1 - 0.3, 2.0))
    lv = np.array(spec["loudness"])
    forced = {s["t"] for s in spec["sections"] if a0 + 0.9 < s["t"] < a1 - 1.0}
    lines_in = [ln for ln in spec["lines"] if ln["t"] >= a0 and ln["end"] <= a1]
    ref = [ln for ln in lines_in if ln["refrain"]]
    pay = ref[-1] if ref else (max(lines_in, key=lambda ln: mean_level(lv, ln["t"], ln["end"])) if lines_in else None)
    if pay and a0 + 0.9 < pay["t"] < a1 - 1.0:
        forced.add(pay["t"])
    snapped = {min(beats, key=lambda b: abs(b - f)) if beats else f for f in forced}
    snapped = {f for f in snapped if a0 + 0.9 <= f <= a1 - 0.9}
    beat = float(np.median(np.diff(beats))) if len(beats) > 2 else 0.5
    cuts, t = [a0], a0
    grid = sorted(set(beats) | snapped)
    while True:
        # shot length by loudness, counted in beats of this tempo: ≈1.4 s loud, ≈2.6 s middle, ≈3.8 s quiet — a ballad
        # whose beat tracker reads double time still breathes
        e = mean_level(lv, t, min(a1, t + 2.0))
        target = 1.4 if e >= 0.62 else 2.6 if e >= 0.35 else 3.8
        step = max(1, int(round(target / max(0.2, beat))))
        nxt = [g for g in grid if g > t + 0.05]
        if not nxt:
            break
        cand = nxt[min(len(nxt) - 1, step - 1)]
        forced = [g for g in nxt if g in snapped and g < cand]    # a section start / the payoff comes first
        if forced:
            cand = forced[0]
        if cand - t > 4.5:                                        # never a shot longer than 4.5 s
            cand = max((g for g in nxt if g - t <= 4.5), default=cand)
        if cand - t < 0.9 and cand not in snapped:                # never a flash shot
            cand = next((g for g in nxt if g - t >= 0.9), a1)
        close = [f for f in snapped if cand < f < cand + 0.9]       # nor a sliver before a section start / the payoff
        if close and cand not in snapped:
            cand = min(close)
        if cand >= a1 - 0.6:
            break
        cuts.append(cand)
        t = cand
    cuts.append(a1)
    # cuts on whole frames: each shot is an exact number of frames, so the joined plate keeps the song's clock
    q = [a0 + round((c - a0) * fps) / fps for c in cuts]
    cuts = [c for k, c in enumerate(q) if k == 0 or c > q[k - 1]]
    shots = []
    for n in range(len(cuts) - 1):
        a, b = cuts[n], cuts[n + 1]
        mid = (a + b) / 2                                         # a shot belongs where most of it plays
        sec = max((s for s in spec["sections"] if s["t"] <= mid), key=lambda s: s["t"], default=spec["sections"][0])
        shots.append({"n": n, "t": round(a - a0, 3), "dur": round(b - a, 3), "abs": round(a, 3), "section": sec["i"],
                      "energy": round(mean_level(lv, a, b), 3)})
    return shots


def assign(shots: list[dict], clips: list[dict]) -> list[dict]:
    """Each shot → a clip: motion rank near the shot's energy, look near the set's median, fewest uses, never the same
    clip twice in a row, a clip collected for that section (folder sNN) preferred."""
    mot = np.array([c["motion"] for c in clips])
    rank = np.argsort(np.argsort(mot)) / max(1, len(clips) - 1) if len(clips) > 1 else np.zeros(1)
    lum = np.array([c["luma"] for c in clips])
    warm = np.array([c["warmth"] for c in clips])
    med_l, med_w = float(np.median(lum)), float(np.median(warm))
    uses = [0] * len(clips)
    prev = -1
    tags = [re.match(r"s(\d+)$", Path(c["file"]).parent.name) for c in clips]
    tagged = {int(t.group(1)) for t in tags if t}
    for s in shots:
        best, bi = 1e9, 0
        for i, c in enumerate(clips):
            if c["seconds"] < s["dur"] + 0.1 and not c["image"]:
                continue
            tag = tags[i]
            # a clip collected for this section's words is preferred; one collected for ANOTHER section stays there
            # (a dawn field in the night verse breaks the story) unless this section has nothing of its own
            own = 0.0
            if tag and s["section"] in tagged:
                own = -0.8 if int(tag.group(1)) == s["section"] else 2.5
            cost = abs(float(rank[i]) - s["energy"]) + 1.2 * abs(lum[i] - med_l) + 0.8 * abs(warm[i] - med_w) \
                + 0.7 * uses[i] + (5 if i == prev else 0) + (0.15 if c["h"] < c["w"] else 0) + own + (0.3 if c["image"] else 0)
            if cost < best:
                best, bi = cost, i
        s["clip"] = bi
        uses[bi] += 1
        prev = bi
    return shots


def cut(name: str, media: Path, grade: str = "auto", fps: int = 30, size=(1080, 1920)) -> dict:
    import montage as MT
    d, spec = _load(name)
    W, H = size
    files = media_files(media)
    if not files:
        raise SystemExit(f"no videos or images under {media}")
    clips = [m for m in (measure_clip(f) for f in files) if m]
    if not clips:
        raise SystemExit("no usable clips (each needs ≥ 1 s of video)")
    shots = assign(shot_grid(spec, fps), clips)
    if grade == "auto":
        grade = MOOD_GRADE.get(spec.get("mood", "night"), "blue_hour")
    by_sec = {s["i"]: s["grade"] for s in spec["sections"] if s.get("grade") in MT.GRADES}
    tmp = Path(tempfile.mkdtemp(prefix="kosif_songreel_"))
    used: list[list[tuple[float, float]]] = [[] for _ in clips]
    parts = []
    for s in shots:
        c = clips[s["clip"]]
        seg = tmp / f"s{s['n']:03d}.mp4"
        g = by_sec.get(s["section"], grade)                     # a section may carry its own grade (night → dawn)
        s["grade"] = g
        if c["image"]:
            MT._still(Path(c["file"]), s["dur"], seg, W, H, fps, g, s["n"])
            s["from"] = 0.0
        else:
            st = MT.pick(np.array(c["energy"], np.float32), 6.0, s["dur"], used[s["clip"]], c["seconds"])
            used[s["clip"]].append((st, st + s["dur"]))
            vf = MT._fit_chain(Path(c["file"]), W, H) + [f"scale={W}:{H}:flags=lanczos", f"fps={fps}", MT.GRADES.get(g, "null"), "format=yuv420p"]
            frames = int(round(s["dur"] * fps))                 # an exact frame count: the plate keeps the song's clock
            _run([FF, "-y", "-v", "error", "-ss", f"{st:.3f}", "-i", c["file"], "-an", "-vf", ",".join(vf), "-frames:v", str(frames),
                  "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-r", str(fps), str(seg)])
            s["from"] = st
        s["file"] = Path(c["file"]).name
        parts.append(seg)
    lst = tmp / "list.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
    raw = tmp / "plate_raw.mp4"
    _run([FF, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(raw)])
    plate = d / "plate.mp4"
    qa.footage(raw, plate, 0.0, None, W, fps)
    shutil.rmtree(tmp, ignore_errors=True)
    credits, seen = [], set()
    used_names = {s["file"] for s in shots}
    for folder in {Path(c["file"]).parent for c in clips}:
        cf = folder / "fetch-credits.json"
        if cf.exists():
            for row in json.loads(cf.read_text(encoding="utf-8")):
                names = {Path(row.get("file", "")).name, Path(row.get("edit", "")).name}
                line = f"{row.get('title') or row.get('id')} — {row.get('creator') or 'creator not listed'} — {row.get('source')}"
                if names & used_names and line not in seen:
                    credits.append(line)
                    seen.add(line)
    spec.update({"media": str(media), "grade": grade, "plate": str(plate), "cuts": [s["t"] for s in shots],
                 "shots": shots, "clips": [{k: v for k, v in c.items() if k != "energy"} for c in clips], "credits": credits})
    _save(d, spec)
    small = sum(1 for c in clips if not c["image"] and min(c["w"], c["h"]) < 1080)
    return {"plate": str(plate), "seconds": round(_dur(plate), 2), "shots": len(shots), "clips_measured": len(clips),
            "clips_used": len({s["clip"] for s in shots}), "grade": grade, "credits": len(credits),
            "below_1080": f"{small} of {len(clips)} clips are under 1080 on the short side (upscaled)" if small else None,
            "shot_lengths": {"min": min(s["dur"] for s in shots), "max": max(s["dur"] for s in shots)}}


# ───────────────────────── build ─────────────────────────
def excerpt_words(spec: dict, d: Path, model: str, lyrics_lines: list[list[str]] | None) -> tuple[Path, str]:
    """Word times for the excerpt from the accurate model on the excerpt alone, aligned to the true words of the lines
    inside it; without a model, the structure pass shifted (said so)."""
    import verse as VE
    ex = spec["excerpt"]
    a0, a1 = ex["start"], ex["end"]
    clip = d / "excerpt.wav"
    out = d / "excerpt.words.json"
    inside = [ln for ln in spec["lines"] if ln["t"] >= a0 - 0.2 and ln["end"] <= a1 + 0.2]
    true = [[w["text"] for w in ln["words"]] for ln in inside]
    how = "structure pass (shifted)"
    lines = [[{**w, "start": round(w["start"] - a0, 3), "end": round(w["end"] - a0, 3)} for w in ln["words"]] for ln in inside]
    if model and model != "none":
        try:
            segs = asr(clip, model)
            ws = [w for s in segs for w in s["words"]]
            if ws and true:
                fine = [ln for ln in VE.align(true, ws) if ln]
                # trust the excerpt pass line by line: where it heard the line it is sharper; where it missed (its words
                # were then stacked after the last heard one) the whole-song pass keeps the line on its real time
                kept = 0
                for k, (f, s) in enumerate(zip(fine, lines)):
                    if abs(f[0]["start"] - s[0]["start"]) <= 1.0 and abs(f[-1]["end"] - s[-1]["end"]) <= 1.5:
                        lines[k] = f
                        kept += 1
                how = f"{model} on the excerpt for {kept}/{len(lines)} lines, the whole-song pass for the rest"
            elif ws and not lines:
                lines = [p for s in segs for p in VE.segment([dict(w) for w in s["words"]]) if p]
                how = f"{model} on the excerpt"
        except SystemExit:
            pass
    segs_out = [{"start": ln[0]["start"], "end": ln[-1]["end"], "text": " ".join(w["text"] for w in ln), "words": ln} for ln in lines if ln]
    out.write_text(json.dumps(segs_out, ensure_ascii=False, indent=1), encoding="utf-8")
    return out, how


def safe_workers() -> int:
    """Parallel browsers the free memory allows: a full-size page with a footage plate takes ≈1.5 GB."""
    try:
        import psutil
        free = psutil.virtual_memory().available / 2 ** 30
    except ImportError:
        return 2
    return max(1, min(6, int(free // 1.5)))


def build(name: str, title: str | None = None, sub: str | None = None, mood: str = "night", accent: str = "#E7B65A",
          credit: str | None = None, model: str = "large-v3", render: bool = False, draft: bool = False, size=(1080, 1920),
          fps: int = 30, workers: int = 0, brand: str | None = None, brand_side: str = "left", font: str | None = None,
          fx3d: bool = True) -> dict:
    import motion as MO
    import verse as VE
    d, spec = _load(name)
    if not spec.get("plate") or not Path(spec["plate"]).exists():
        raise SystemExit(f"run `songreel cut {name} --media DIR` first")
    ex = spec["excerpt"]
    a0, a1 = ex["start"], ex["end"]
    dur = a1 - a0
    fade_in = 0.0 if a0 < 0.5 else 0.35
    _run([FF, "-y", "-v", "error", "-ss", f"{a0:.3f}", "-t", f"{dur:.3f}", "-i", spec["wav"], "-af",
          f"afade=t=in:st=0:d={fade_in},afade=t=out:st={max(0, dur - 1.4):.3f}:d=1.4", "-ar", "48000", str(d / "excerpt.wav")])
    words_json, how = excerpt_words(spec, d, model, None)
    # sources are not printed on the picture: they go to credits.txt next to the film (the brand mark takes the top)
    rep = VE.verse(d / "excerpt.wav", name, None, words_json, title, sub, size, mood, accent, None, "none", credit, model, None, fps,
                   False, Path(spec["plate"]), spec.get("cuts"), brand, brand_side, font, fx3d)
    rep["word_timing"] = how
    proj = Path(rep["project"])
    if spec.get("credits"):
        (proj / "credits.txt").write_text("\n".join(spec["credits"]) + "\n", encoding="utf-8")
    if render or draft:
        film = MO.render(str(proj), "studio", "looks", None, None, 1, draft=draft, workers=workers or safe_workers())
        rep["film"] = str(film)
        if not draft:
            rep["gate"] = qa.inspect(Path(film))
            if spec.get("credits"):
                shutil.copy2(proj / "credits.txt", Path(film).with_suffix(".credits.txt"))
    spec["build"] = {"title": title, "mood": mood, "accent": accent, "word_timing": how, "project": str(proj)}
    _save(d, spec)
    return rep


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("analyze"); p.add_argument("song", type=Path); p.add_argument("--name", required=True)
    p.add_argument("--lyrics", type=Path); p.add_argument("--seconds", type=float, default=45.0); p.add_argument("--start", type=float)
    p.add_argument("--model", default="small")
    p = sub.add_parser("queries"); p.add_argument("name")
    p = sub.add_parser("cut"); p.add_argument("name"); p.add_argument("--media", type=Path, required=True)
    p.add_argument("--grade", default="auto"); p.add_argument("--fps", type=int, default=30); p.add_argument("--size", default="1080x1920")
    p = sub.add_parser("build"); p.add_argument("name"); p.add_argument("--title"); p.add_argument("--sub")
    p.add_argument("--mood", default="night"); p.add_argument("--accent", default="#E7B65A"); p.add_argument("--credit")
    p.add_argument("--model", default="large-v3"); p.add_argument("--render", action="store_true"); p.add_argument("--draft", action="store_true")
    p.add_argument("--size", default="1080x1920"); p.add_argument("--fps", type=int, default=30)
    p.add_argument("--brand"); p.add_argument("--brand-side", default="left", choices=["left", "right"])
    p.add_argument("--font", help="display face for the lyrics (Aref Ruqaa, El Messiri, Amiri, Reem Kufi, a .ttf path)")
    p.add_argument("--flat", action="store_true", help="no 3D words / depth dust / light rays")
    p.add_argument("--workers", type=int, default=0, help="browsers in parallel (0 = by free memory: one per 1.5 GB, at most 6)")
    a = ap.parse_args()
    if a.cmd == "analyze":
        if not a.song.exists():
            raise SystemExit(f"no such file: {a.song}")
        rep = analyze(a.song, a.name, a.lyrics, min(180.0, a.seconds), a.start, a.model)
    elif a.cmd == "queries":
        rep = queries(a.name)
    elif a.cmd == "cut":
        W, H = (int(v) for v in a.size.lower().split("x"))
        rep = cut(a.name, a.media, a.grade, a.fps, (W, H))
    else:
        W, H = (int(v) for v in a.size.lower().split("x"))
        rep = build(a.name, a.title, a.sub, a.mood, a.accent, a.credit, a.model, a.render, a.draft, (W, H), a.fps, a.workers, a.brand, a.brand_side, a.font, not a.flat)
    print(json.dumps(rep, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
