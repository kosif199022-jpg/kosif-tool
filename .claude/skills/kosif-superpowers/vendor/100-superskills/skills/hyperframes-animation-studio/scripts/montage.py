"""KOSIF Montage — edit any footage to a beat, the way the films are cut (taken from the Ultra Motion & Montage skill in
KOSIF Omni and made measured: the beats, the shot choice and the loudness are computed, never guessed).

    python montage.py cut CLIP [CLIP ...] --music track.wav [--seconds 20] [--ratio 9:16] [--grade teal_orange]
                          [--punch] [--voice vo.wav] [--captions caps.json] [--keep-audio] --out film.mp4
    python montage.py grade VIDEO --preset golden_hour [--out graded.mp4]
    python montage.py captions VIDEO --spec caps.json [--style reels|cinema|punchy] [--out captioned.mp4]
    python montage.py presets

cut:      beats from the music (qa.beats) → a shot plan that alternates quick shots (≈1 s) with breathing ones (≈3 s) and
          lands every cut on a beat (the big ones on downbeats) → for each slot, the most active window of the next clip
          that has not been used yet (frame-difference energy) → fill-crop to the frame, optional zoom punches that decay
          like a hit, a grade → hard cuts (no crossfades) → music (+ voice with real sidechain ducking, + the clips' own
          sound) → −14 LUFS / −1 dBTP → optional karaoke captions.
captions: [{"start": s, "end": e, "text": "..."}] or voice.py timings [{"t": s, "end": e, "text": "..."}]. The spoken word is
          coloured and pops (one event per word, so Arabic shapes and orders correctly); words get time by their length.
"""
from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import qa  # noqa: E402

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

FF = shutil.which("ffmpeg") or "ffmpeg"

# FFmpeg grades (curves/colorbalance/eq). Grain is seeded so a re-render is identical.
GRADES = {
    "teal_orange": "curves=r='0/0 0.2/0.1 0.7/0.8 1/1':b='0/0.05 0.3/0.38 0.7/0.65 1/0.95',colorbalance=rs=0.08:gs=-0.02:bs=-0.08:rh=-0.04:gh=0.02:bh=0.08",
    "golden_hour": "curves=r='0/0 0.5/0.58 1/1':b='0/0 0.5/0.42 1/0.92',eq=saturation=1.25:contrast=1.08:brightness=0.02",
    "cyberpunk": "curves=r='0/0.05 0.5/0.45 1/1':b='0/0.08 0.5/0.62 1/1',colorbalance=rs=-0.1:gs=-0.05:bs=0.15:rh=0.12:gh=-0.05:bh=0.08,eq=saturation=1.35:contrast=1.2",
    "vintage_film": "curves=all='0/0.06 0.5/0.5 1/0.94':r='0/0 0.5/0.52 1/1':b='0/0.04 0.5/0.48 1/0.96',noise=alls=10:allf=t+u:all_seed=7,eq=contrast=1.05:saturation=0.9",
    "matrix_tech": "curves=g='0/0.04 0.5/0.54 1/1':b='0/0 0.5/0.46 1/0.92',colorbalance=rs=-0.08:gs=0.1:bs=-0.05,eq=contrast=1.15:saturation=0.85",
    "clean_commercial": "eq=contrast=1.12:saturation=1.18:brightness=0.01,unsharp=5:5:0.8:5:5:0.0",
    # night (Night Photography + Gurney): tungsten white balance turns the sky deep blue, lamps stay warm; darks go rod-blue
    "blue_hour": "colortemperature=temperature=4300:mix=0.85,curves=b='0/0.06 0.5/0.56 1/1':r='0/0 0.5/0.47 1/1',eq=saturation=1.08:contrast=1.06",
    "sodium_night": "curves=r='0/0 0.4/0.46 1/1':g='0/0 0.5/0.47 1/0.96':b='0/0.05 0.3/0.3 1/0.86',colorbalance=bs=0.10:gs=0.02:rh=0.06:bh=-0.08,eq=contrast=1.12",
    # restoration of old/soft footage: light temporal denoise, cleaner blacks, highlight roll-off, warmer mids, CAS sharpening
    "restore": "hqdn3d=1.2:1.2:3:3,eq=contrast=1.12:brightness=-0.015:saturation=1.07:gamma=0.97,curves=all='0/0 0.06/0.035 0.25/0.22 0.5/0.5 0.8/0.82 0.94/0.93 1/0.97',colorbalance=rs=0.012:bs=-0.01:rm=0.025:gm=0.005:bm=-0.02,cas=0.3",
    "magma_night": "curves=r='0/0.02 0.5/0.56 1/1':g='0/0 0.5/0.44 1/0.95':b='0/0.05 0.5/0.42 1/0.88',eq=contrast=1.1:saturation=1.1",
    "none": "null",
}
RATIOS = {"9:16": (1080, 1920), "16:9": (1920, 1080), "1:1": (1080, 1080), "4:5": (1080, 1350)}


def _run(cmd: list[str]):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-1500:])
    return r


def _duration(path: Path) -> float:
    r = subprocess.run([qa.FP, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def _has_audio(path: Path) -> bool:
    r = subprocess.run([qa.FP, "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return bool(r.stdout.strip())


# ───────────────────────── shot plan ─────────────────────────
def plan(beat_times: list[float], downbeats: list[float], seconds: float, beat: float) -> list[tuple[float, float]]:
    """Cut points on the beat grid: a hook shot first (≤ 1.5 s), then quick, quick, breathing, quick, quick, quick,
    breathing ... with the breathing shots ending on downbeats when one is near."""
    fast = max(1, round(1.0 / beat)); slow = max(2, round(3.0 / beat)); hook = max(1, min(fast, round(1.4 / beat)))
    pattern = [hook, fast, fast, slow, fast, fast, fast, slow, fast, slow]
    grid = [0.0] + [b for b in beat_times if 0.05 < b < seconds - 0.05] + [seconds]
    down = set(round(d, 3) for d in downbeats)
    cuts, i, k = [0.0], 0, 0
    while i < len(grid) - 1:
        step = pattern[k % len(pattern)]; k += 1
        j = min(len(grid) - 1, i + step)
        if step >= slow:                                     # breathing shots prefer to land on a downbeat (±1 beat)
            for dj in (0, 1, -1):
                jj = j + dj
                if 0 < jj < len(grid) - 1 and round(grid[jj], 3) in down:
                    j = jj; break
        if grid[j] - cuts[-1] < 0.35:                        # never a flash frame
            j = min(len(grid) - 1, j + 1)
        cuts.append(grid[j]); i = j
    if seconds - cuts[-2] < 0.5 and len(cuts) > 2:          # fold a sliver at the end into the last shot
        cuts.pop(-2)
    return [(cuts[n], cuts[n + 1]) for n in range(len(cuts) - 1)]


def energy(clip: Path, fps: float = 6.0) -> np.ndarray:
    """Motion energy per 1/fps s: mean absolute difference of consecutive small grey frames."""
    prev, out = None, []
    for f in qa._frames(clip, fps, 160):
        f = f.astype(np.float32)
        out.append(0.0 if prev is None else float(np.mean(np.abs(f - prev))))
        prev = f
    return np.asarray(out or [0.0], np.float32)


def pick(e: np.ndarray, fps: float, dur: float, used: list[tuple[float, float]], total: float) -> float:
    """Start of the most active window of length dur that does not overlap what was used (falls back to the least used)."""
    w = max(1, int(round(dur * fps)))
    if len(e) <= w:
        return 0.0
    c = np.convolve(e, np.ones(w) / w, mode="valid")        # c[i] = mean energy over [i, i+w)
    best, best_s = -1.0, 0.0
    for i in range(len(c)):
        s = i / fps
        if s + dur > total - 0.05:
            break
        if any(s < b and s + dur > a for a, b in used):
            continue
        if c[i] > best:
            best, best_s = float(c[i]), s
    if best < 0:                                             # every window overlaps: take the one with least overlap
        best_s = min((i / fps for i in range(len(c)) if i / fps + dur <= total), key=lambda s: sum(max(0, min(b, s + dur) - max(a, s)) for a, b in used), default=0.0)
    return round(best_s, 3)


# ───────────────────────── render ─────────────────────────
def _segment(clip: Path, start: float, dur: float, out: Path, W: int, H: int, fps: int, grade: str, punches: list[float]):
    """One shot: fill-crop to W×H (rendered at 2× so the zoom punch has half-pixel steps), punches that jump to +9 % and
    decay with a 0.32 s time constant (a hit, not a pulse), the grade, CFR."""
    vf = [f"scale={2 * W}:{2 * H}:force_original_aspect_ratio=increase:flags=lanczos", f"crop={2 * W}:{2 * H}", "setsar=1"]
    if punches:
        z = "+".join(f"0.09*exp(-(t-{p:.3f})/0.32)*gte(t,{p:.3f})" for p in punches)
        vf += [f"scale=w='trunc({2 * W}*(1+{z})/2)*2':h='trunc({2 * H}*(1+{z})/2)*2':eval=frame", f"crop={2 * W}:{2 * H}"]
    vf += [f"scale={W}:{H}:flags=lanczos", f"fps={fps}", GRADES.get(grade, "null"), "format=yuv420p"]
    _run([FF, "-y", "-v", "error", "-ss", f"{start:.3f}", "-t", f"{dur:.3f}", "-i", str(clip), "-an", "-vf", ",".join(vf),
          "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-r", str(fps), str(out)])


def cut(clips: list[Path], music: Path, out: Path, seconds: float | None = None, ratio: str = "9:16", fps: int = 30,
        grade: str = "teal_orange", punch: bool = True, voice: Path | None = None, captions: Path | None = None,
        keep_audio: bool = False, style: str = "reels") -> dict:
    clips = [Path(c) for c in clips]
    W, H = RATIOS.get(ratio, RATIOS["9:16"])
    bt = qa.beats(Path(music))
    total_music = bt["duration"]
    seconds = round(min(seconds or total_music, total_music), 3)
    shots = plan(bt["beats"], bt["downbeats"], seconds, bt["beat"])
    tmp = Path(tempfile.mkdtemp(prefix="kosif_montage_"))
    lens = [_duration(c) for c in clips]
    ens = [energy(c) for c in clips]
    used: list[list[tuple[float, float]]] = [[] for _ in clips]
    downs = [d for d in bt["downbeats"] if d < seconds]
    parts, log = [], []
    for n, (a, b) in enumerate(shots):
        ci = n % len(clips)                                  # round robin keeps every clip in play
        d = b - a
        s = pick(ens[ci], 6.0, d, used[ci], lens[ci])
        used[ci].append((s, s + d))
        hits = [round(x - a, 3) for x in downs if a - 1e-3 <= x < b - 0.12] if punch else []
        seg = tmp / f"s{n:03d}.mp4"
        _segment(clips[ci], s, d, seg, W, H, fps, grade, hits)
        parts.append(seg)
        log.append({"shot": n, "at": round(a, 3), "dur": round(d, 3), "clip": clips[ci].name, "from": s, "punches": hits})
    lst = tmp / "list.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
    picture = tmp / "picture.mp4"
    _run([FF, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(picture)])

    # sound: music bed (+ the clips' own sound) ducked under the voice, then −14 LUFS
    ins, nin = ["-i", str(picture), "-i", str(music)], 2
    graph = [f"[1:a]atrim=0:{seconds},asetpts=N/SR/TB,afade=t=out:st={max(0, seconds - 0.6):.3f}:d=0.6,aformat=sample_rates=48000:channel_layouts=stereo[bed0]"]
    bed = "bed0"
    if keep_audio:
        nat = []
        for n, ((a, b), lg) in enumerate(zip(shots, log)):
            src = clips[[c.name for c in clips].index(lg["clip"])]
            if _has_audio(src):
                k, nin = nin, nin + 1
                ins += ["-ss", f"{lg['from']:.3f}", "-t", f"{b - a:.3f}", "-i", str(src)]
                graph.append(f"[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.35,adelay={int(a * 1000)}|{int(a * 1000)}[n{n}]")
                nat.append(f"[n{n}]")
        if nat:
            graph.append(f"[bed0]{''.join(nat)}amix=inputs={len(nat) + 1}:normalize=0:duration=first[bed1]")
            bed = "bed1"
    if voice:
        k, nin = nin, nin + 1
        ins += ["-i", str(voice)]
        graph.append(f"[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit=2[vk][vm]")
        # −18 dB under speech: threshold low, ratio high, 20 ms attack, 300 ms release
        graph.append(f"[{bed}][vk]sidechaincompress=threshold=0.02:ratio=12:attack=20:release=300:makeup=1[duck]")
        graph.append("[duck][vm]amix=inputs=2:normalize=0:duration=first[mix]")
        bed = "mix"
    # loudnorm alone can overshoot after AAC: aim under the ceiling and catch the rest with a limiter (≈ −1.5 dBFS)
    graph.append(f"[{bed}]loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.84:level=false:attack=3:release=60[aout]")
    mixed = tmp / "mixed.mp4"
    _run([FF, "-y", "-v", "error", *ins, "-filter_complex", ";".join(graph), "-map", "0:v", "-map", "[aout]",
          "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-t", f"{seconds:.3f}", str(mixed)])
    out = Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    if captions:
        burn(mixed, out, json.loads(Path(captions).read_text(encoding="utf-8")), style)
    else:
        shutil.copy2(mixed, out)
    rep = {"file": str(out), "seconds": seconds, "bpm": bt["bpm"], "shots": len(shots), "ratio": ratio, "grade": grade, "plan": log}
    out.with_suffix(".montage.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    return rep


def grade_video(video: Path, out: Path, preset: str) -> Path:
    if preset not in GRADES:
        raise SystemExit(f"unknown preset {preset}: {', '.join(GRADES)}")
    _run([FF, "-y", "-v", "error", "-i", str(video), "-vf", GRADES[preset] + ",format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-c:a", "copy", str(out)])
    return out


# ───────────────────────── captions ─────────────────────────
STYLES = {  # font, size (per 1080 px of height), primary, highlight (ASS &HBBGGRR), outline, shadow, bottom margin (per 1920)
    "reels": ("Noto Sans Arabic", 74, "&H00FFFFFF", "&H0059DEFF", 6, 3, 300),
    "cinema": ("Noto Naskh Arabic", 46, "&H00EAEAEA", "&H00A8E6FF", 3, 2, 150),
    "punchy": ("Noto Kufi Arabic", 72, "&H00FFFFFF", "&H00F8BD38", 8, 4, 330),
}


def _ass_time(s: float) -> str:
    s = max(0.0, s); cs = int(round(s * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"


def _norm_caps(spec: list[dict]) -> list[dict]:
    out = []
    for c in spec:
        a = float(c.get("start", c.get("t", 0.0))); b = float(c.get("end", a + 2.0))
        out.append({"start": a, "end": b, "text": str(c.get("text", "")).strip(), "words": c.get("words")})
    return out


def word_times(cap: dict) -> list[tuple[str, float, float]]:
    """Words of a line with times: given ones, or the line's span shared by length (letters + a small constant)."""
    if cap.get("words") and isinstance(cap["words"][0], dict):
        return [(w["text"], float(w["start"]), float(w["end"])) for w in cap["words"]]
    words = cap["text"].split()
    if not words:
        return []
    weights = np.array([len(w) + 2 for w in words], np.float32)
    edges = cap["start"] + np.concatenate([[0], np.cumsum(weights)]) / weights.sum() * (cap["end"] - cap["start"])
    return [(w, float(edges[i]), float(edges[i + 1])) for i, w in enumerate(words)]


def ass(spec: list[dict], W: int, H: int, style: str = "reels", max_words: int = 6) -> str:
    # Encoding -1 lets libass detect the paragraph direction: with a fixed charset the base direction is left-to-right and
    # an Arabic line split by a highlight override comes out in the wrong word order
    font, size, prim, hi, outl, shad, mv = STYLES.get(style, STYLES["reels"])
    k = H / 1080 if W >= H else W / 1080                     # sizes scale with the short side
    fs, ol, sh, margin = round(size * k), max(1, round(outl * k)), round(shad * k), round(mv * H / 1920)
    head = (f"[Script Info]\nScriptType: v4.00+\nPlayResX: {W}\nPlayResY: {H}\nScaledBorderAndShadow: yes\nWrapStyle: 2\n\n"
            "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
            "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
            f"Style: Cap,{font},{fs},{prim},{hi},&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,{ol},{sh},2,{round(W * 0.06)},{round(W * 0.06)},{margin},-1\n\n"
            "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    ev = []
    for cap in _norm_caps(spec):
        wt = word_times(cap)
        for g in range(0, len(wt), max_words):               # 5–7 words on screen at most
            chunk = wt[g:g + max_words]
            for i, (w, a, b) in enumerate(chunk):
                end = chunk[i + 1][1] if i + 1 < len(chunk) else b
                parts = []
                for j, (x, _, _) in enumerate(chunk):
                    if j == i:   # the spoken word: highlight colour and a quick pop (112 % → 100 % in 120 ms)
                        parts.append(f"{{\\1c{hi}\\fscx112\\fscy112\\t(0,120,\\fscx100\\fscy100)}}{x}{{\\r}}")
                    else:
                        parts.append(x)
                ev.append(f"Dialogue: 0,{_ass_time(a)},{_ass_time(end)},Cap,,0,0,0,,{' '.join(parts)}")
    return head + "\n".join(ev) + "\n"


def burn(video: Path, out: Path, spec: list[dict], style: str = "reels") -> Path:
    info = qa._probe(Path(video))
    tmp = Path(tempfile.mkdtemp(prefix="kosif_caps_")) / "caps.ass"
    tmp.write_text(ass(spec, info["w"], info["h"], style), encoding="utf-8")
    p = tmp.as_posix().replace(":", "\\:")
    _run([FF, "-y", "-v", "error", "-i", str(video), "-vf", f"ass='{p}',format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-c:a", "copy", str(out)])
    return Path(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("cut"); p.add_argument("clips", nargs="+"); p.add_argument("--music", required=True); p.add_argument("--out", required=True)
    p.add_argument("--seconds", type=float); p.add_argument("--ratio", default="9:16", choices=list(RATIOS)); p.add_argument("--fps", type=int, default=30)
    p.add_argument("--grade", default="teal_orange", choices=list(GRADES)); p.add_argument("--no-punch", action="store_true")
    p.add_argument("--voice"); p.add_argument("--captions"); p.add_argument("--keep-audio", action="store_true"); p.add_argument("--style", default="reels", choices=list(STYLES))
    p = sub.add_parser("grade"); p.add_argument("video"); p.add_argument("--preset", default="teal_orange", choices=list(GRADES)); p.add_argument("--out")
    p = sub.add_parser("captions"); p.add_argument("video"); p.add_argument("--spec", required=True); p.add_argument("--style", default="reels", choices=list(STYLES)); p.add_argument("--out")
    sub.add_parser("presets")
    a = ap.parse_args()
    if a.cmd == "cut":
        rep = cut(a.clips, Path(a.music), Path(a.out), a.seconds, a.ratio, a.fps, a.grade, not a.no_punch,
                  Path(a.voice) if a.voice else None, Path(a.captions) if a.captions else None, a.keep_audio, a.style)
        rep.pop("plan"); print(json.dumps(rep, ensure_ascii=False))
    elif a.cmd == "grade":
        v = Path(a.video); out = Path(a.out) if a.out else v.with_stem(v.stem + "_" + a.preset)
        print(grade_video(v, out, a.preset))
    elif a.cmd == "captions":
        v = Path(a.video); out = Path(a.out) if a.out else v.with_stem(v.stem + "_captions")
        print(burn(v, out, json.loads(Path(a.spec).read_text(encoding="utf-8")), a.style))
    else:
        print("\n".join(GRADES))


if __name__ == "__main__":
    main()
