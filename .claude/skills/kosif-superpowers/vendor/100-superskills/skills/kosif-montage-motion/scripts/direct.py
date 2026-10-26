"""KOSIF direct — a directed edit of a talking clip, built automatically and left editable.

    python direct.py CLIP.mp4 --name NAME [--size 1080x1920] [--model large-v3] [--words CLIP.words.json]
                     [--accent "#E7B65A"] [--credit "insta: name"] [--no-decaption] [--render]

What it decides (each choice is written to projects/NAME/edit.js, so Claude or you can change it and re-render):
- words and times (transcribe), the plate (decaption → restore → reframe → all-intra), the voice chain, music only if
  the clip has none;
- the subject of each shot (skin region, else the moving region) → the camera pushes on it and text stays off it;
- stress per word (loudness × length) → one keyword per sentence in large type, a camera punch and a sound accent;
- numbers → a clock ring beside the subject; a cut between shots → the keyword becomes the transition plane;
- the last sentence → the payoff (first half light, the rest dominant with a light sweep); a deliberate dip to black.
Then `kmotion render projects/NAME --engine studio` (or --render here) and `kmotion inspect`.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

FF = shutil.which("ffmpeg") or "ffmpeg"
STOP = set("""في من على الى إلى عن مع ان أن إن لا ما مش مو هو هي هم انت إنت انتي أنا انا احنا إحنا ده دي دا دول اللي الذي التي و ف ب ل
يا لك ليك له لها كده كدا بس لو اذا إذا كل اي أي ايه إيه علشان عشان لأن لان يعني ممكن كان كانت يكون تكون هذا هذه ذلك تلك ثم او أو حتى قد لقد
لكل بكل بالنسبة عبارة حوالي واحد قال قالي قالتلي حاجة طب طيب فعلا تاني حتة بقى اوي أوي جدا عند عندي كنا كنت ليه فين امتى ازاي إزاي شوف""".split())
TEMPLATE = next((p for p in (HERE / "templates" / "directed.html", HERE.parent / "templates" / "directed.html") if p.exists()), None)


def _run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        raise RuntimeError(r.stderr[-1500:])
    return r


def subject_box(video: Path, a: int, b: int, fps: float) -> tuple[float, float, float, float] | None:
    """Median box of the subject in frames a..b: the largest skin region in the upper 78 % of the frame, else the region
    that moves. Coordinates as fractions of the source frame."""
    import cv2
    cap = cv2.VideoCapture(str(video))
    idx = np.linspace(a, max(a, b - 1), num=min(12, max(1, b - a))).astype(int)
    boxes, prev, motion = [], None, None
    for i in idx:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(i)); ok, f = cap.read()
        if not ok:
            continue
        H, W = f.shape[:2]
        y = cv2.cvtColor(f, cv2.COLOR_BGR2YCrCb)
        m = ((y[..., 1] >= 133) & (y[..., 1] <= 178) & (y[..., 2] >= 80) & (y[..., 2] <= 130) & (y[..., 0] > 60)).astype(np.uint8)
        m[int(H * 0.78):] = 0
        m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)); m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
        n, lab, st, _ = cv2.connectedComponentsWithStats(m)
        if n > 1:
            j = 1 + int(np.argmax(st[1:, 4]))
            if st[j, 4] > 0.012 * W * H:
                x0, y0, w, h = st[j, :4]; boxes.append((x0 / W, y0 / H, w / W, h / H))
        g = cv2.GaussianBlur(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (9, 9), 0).astype(np.float32)
        if prev is not None:
            d = np.abs(g - prev); motion = d if motion is None else motion + d
        prev = g
    if boxes:
        return tuple(float(v) for v in np.median(np.array(boxes), axis=0))
    if motion is not None:
        mm = motion[: int(motion.shape[0] * 0.8)]
        thr = np.percentile(mm, 97)
        ys, xs = np.nonzero(mm > thr)
        if len(xs) > 50:
            H, W = motion.shape
            x0, x1, y0, y1 = np.percentile(xs, 5), np.percentile(xs, 95), np.percentile(ys, 5), np.percentile(ys, 95)
            return (x0 / W, y0 / H, (x1 - x0) / W, (y1 - y0) / H)
    return None


def word_stress(voice: Path, words: list[dict]) -> list[float]:
    with wave.open(str(voice)) as w:
        sr, ch = w.getframerate(), w.getnchannels()
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    x = x.reshape(-1, ch).mean(1) if ch > 1 else x
    rms = []
    for wd in words:
        seg = x[int(wd["start"] * sr):max(int(wd["start"] * sr) + 1, int(wd["end"] * sr))]
        rms.append(float(np.sqrt(np.mean(seg ** 2))) if len(seg) else 0.0)
    r = np.array(rms); L = np.array([len(re.sub(r"\W", "", wd["text"])) for wd in words], float)
    z = lambda v: (v - v.mean()) / (v.std() + 1e-9)
    return list(0.65 * z(np.log(r + 1e-4)) + 0.35 * z(L))


def plan(segs: list[dict], shots: list[dict], stress: list[float], W: int, H: int, duration: float, max_words: int = 6) -> dict:
    words = [dict(w) for s in segs for w in s["words"]]
    for w, st in zip(words, stress):
        w["stress"] = st
    clean = lambda t: re.sub(r"[^\w؀-ۿ]", "", t)
    shot_of = lambda t: next((s for s in shots if s["start"] <= t < s["end"]), shots[-1])
    # layout per shot: captions under the subject, keywords above the captions, motifs on the free side
    # the stack, top to bottom: the face, then the keyword below it, then the caption — never text over the mouth
    for s in shots:
        fy1 = (s["box"][1] + s["box"][3]) * H if s.get("box") else H * 0.55
        s["keyY"] = float(np.clip(fy1 + 0.015 * H, 0.50 * H, 0.66 * H))      # top of the keyword line
        s["capY"] = float(np.clip(s["keyY"] + 0.135 * H, 0.64 * H, 0.80 * H))
        cx = (s["box"][0] + s["box"][2] / 2) * W if s.get("box") else W / 2
        s["side"] = 0.20 * W if cx > W / 2 else 0.80 * W
        s["eyeY"] = (s["box"][1] + s["box"][3] * 0.35) * H if s.get("box") else 0.35 * H
    # the payoff: the most stressed sentence (≥ 3 words) in the last 40 % — the climax is often not the very last line
    def seg_score(sg):
        cw = [w for w in words if sg["start"] - 1e-6 <= w["start"] < sg["end"] - 1e-6 and clean(w["text"]) not in STOP]
        return float(np.mean([w["stress"] for w in cw])) if cw else -9.0
    # rhetoric first: a repeated short line ("كافح … كافح … كافح") builds, and the first full sentence after its last
    # repetition resolves it — that is the payoff; otherwise the most stressed full sentence in the last 40 %
    norm = lambda sg: " ".join(clean(w["text"]) for w in sg["words"])
    counts = {}
    for sg in segs:
        if len(sg["words"]) <= 2:
            counts[norm(sg)] = counts.get(norm(sg), 0) + 1
    reps = [i for i, sg in enumerate(segs) if len(sg["words"]) <= 2 and counts.get(norm(sg), 0) >= 2]
    payoff_seg = None
    if reps:
        payoff_seg = next((sg for sg in segs[reps[-1] + 1:] if len(sg["words"]) >= 3), None)
    if payoff_seg is None:
        late = [sg for sg in segs if sg["start"] >= 0.6 * duration and len(sg["words"]) >= 3] or segs[-1:]
        payoff_seg = max(late, key=lambda sg: (seg_score(sg), sg["start"])) if late else None
    payoff_start, payoff_end = (payoff_seg["start"], payoff_seg["end"]) if payoff_seg else (duration, duration)
    # refrains (a word in ≥ 4 sentences) are the hook's word, not every sentence's keyword
    seen = {}
    for sg in segs:
        for wt in {clean(x["text"]) for x in sg["words"]}:
            seen[wt] = seen.get(wt, 0) + 1
    refrain = {wt for wt, n in seen.items() if n >= 4}
    is_num = lambda t: bool(re.search(r"[0-9٠-٩]", t))

    def key_score(w, ws):
        i = ws.index(w)
        sc = w["stress"] + 0.9 * (i + 1) / len(ws)                    # end-focus: the sentence lands on its last content word
        if 2 <= seen.get(clean(w["text"]), 0) <= 3:
            sc += 0.5                                                 # a theme word the speaker returns to
        if i > 0 and is_num(ws[i - 1]["text"]):
            sc -= 3                                                   # the unit after a number ("24 ساعة") belongs to the ring
        return sc
    captions, keys, motifs, camera, chapters = [], [], [], [], []
    last_key = -9.0
    for s in segs:
        if payoff_start - 1e-6 <= s["start"] < payoff_end - 1e-6:
            continue
        ws = [w for w in words if s["start"] - 1e-6 <= w["start"] < s["end"] - 1e-6]
        if not ws:
            continue
        first = s is segs[0]
        cand = [w for w in ws if clean(w["text"]) not in STOP and len(clean(w["text"])) >= 3 and (first or clean(w["text"]) not in refrain)]
        kw = max(cand, key=lambda w: key_score(w, ws)) if cand else None
        after_payoff = s["start"] >= payoff_end - 1e-6
        if kw and not after_payoff and kw["start"] - last_key > 1.2:
            sh = shot_of(kw["start"])
            nxt = min([x["start"] for x in words if x["start"] > kw["end"] + 0.25] + [s["end"]])
            keys.append({"t": round(kw["start"], 3), "end": round(min(s["end"], max(kw["end"] + 0.6, nxt)), 3), "text": kw["text"],
                         "y": round(sh["keyY"]), "size": 190, "accent": True})
            camera.append({"t": round(kw["start"], 3), "punch": 0.035})
            last_key = kw["start"]
            kw["key"] = True
        for i in range(0, len(ws), max_words):
            chunk = ws[i:i + max_words]
            sh = shot_of(chunk[0]["start"])
            end = min(s["end"], (ws[i + max_words]["start"] if i + max_words < len(ws) else s["end"])) - 0.02
            captions.append({"words": [{"t": round(w["start"], 3), "text": w["text"], "key": bool(w.get("key"))} for w in chunk],
                             "end": round(end, 3), "y": round(sh["capY"]), "size": 54})
        for w in ws:                                             # numbers → a clock ring, moved to the repetition if repeated
            if is_num(w["text"]):
                sh = shot_of(w["start"])
                ring = {"type": "ring", "t": round(w["start"], 3), "end": round(min(s["end"], w["start"] + 1.4), 3), "text": clean(w["text"]),
                        "cx": round(sh["side"]), "cy": round(sh["eyeY"]), "r": 150}
                motifs = [m for m in motifs if not (m["text"] == ring["text"] and ring["t"] - m["t"] < 6)]
                motifs.append(ring)
                break
    # cuts → chapters: the strongest content word nearest the cut becomes the transition plane
    for s in shots[1:]:
        before = [w for w in words if s["start"] - 0.8 <= w["start"] < s["start"] + 0.2 and clean(w["text"]) not in STOP and len(clean(w["text"])) >= 3]
        if before:
            w = max(before, key=lambda x: x["stress"] - 2.5 * abs(x["start"] - s["start"]))   # the word AT the cut wins
            chapters.append({"t": round(s["start"], 3), "text": w["text"]})
            keys = [k for k in keys if not (s["start"] - 1.2 < k["t"] < s["start"] + 0.6)]
    payoff = None
    if payoff_seg:
        pw = payoff_seg["words"]
        cut = max(1, len(pw) // 2) if len(pw) > 2 else 1
        payoff = {"t": round(pw[0]["start"], 3), "t2": round(pw[cut]["start"] if cut < len(pw) else pw[0]["start"] + 0.5, 3),
                  "end": round(min(duration - 0.4, pw[-1]["end"] + 0.5), 3), "lines": [" ".join(w["text"] for w in pw[:cut]), " ".join(w["text"] for w in pw[cut:])],
                  "y": round(shot_of(pw[0]["start"])["keyY"] + 0.05 * H)}
        camera.append({"t": round(payoff["t2"], 3), "punch": 0.05})
    end = round(min(duration - 0.05, (segs[-1]["end"] if segs else duration) + 0.35), 3)
    return {"captions": captions, "keys": keys, "motifs": motifs, "camera": camera, "chapters": chapters, "payoff": payoff,
            "end": max(0.5, min(end, duration - 0.33)), "hook": {"release": round(segs[0]["words"][1]["start"], 3) if segs and len(segs[0]["words"]) > 1 else 0.4}}


def apply_fixes(segs: list[dict], fixes: str | dict | None) -> list[dict]:
    """Correct the transcript and keep the timing: {"ما حدش": "محدش", "بتعودش ضايع": "متقعدش تضيّع"} or
    "ما حدش=محدش;بتعودش ضايع=متقعدش تضيّع". A source of n words becomes the target's m words spread over the same span."""
    if not fixes:
        return segs
    if isinstance(fixes, str):
        fixes = dict(x.split("=", 1) for x in fixes.split(";") if "=" in x)
    fixes = {k: v for k, v in fixes.items() if k.split()}                # an empty source phrase would never advance
    out = []
    for sg in segs:
        ws = [dict(w) for w in sg["words"]]
        for src, dst in fixes.items():
            a, b = src.split(), dst.split()
            if not a:                                          # an empty key would match everywhere and never advance
                continue
            i = 0
            while i + len(a) <= len(ws):
                if [w["text"].strip() for w in ws[i:i + len(a)]] == a:
                    t0, t1 = ws[i]["start"], ws[i + len(a) - 1]["end"]
                    step = (t1 - t0) / max(1, len(b))
                    ws[i:i + len(a)] = [{"text": tx, "start": round(t0 + k * step, 3), "end": round(t0 + (k + 1) * step, 3), "p": 1.0} for k, tx in enumerate(b)]
                    i += len(b)
                else:
                    i += 1
        out.append({"start": sg["start"], "end": sg["end"], "text": " ".join(w["text"] for w in ws), "words": ws})
    return out


def direct(clip: Path, name: str, size=(1080, 1920), model="large-v3", words_json: Path | None = None, accent="#E7B65A",
           credit: str | None = None, decap=True, render=False, fixes: str | dict | None = None) -> dict:
    import decaption as D
    import motion as MO
    import reel as RL
    import transcribe as T
    clip = Path(clip)
    W, H = size
    info = RL._probe(clip)
    proj = MO.PROJECTS / MO.safe_name(name)
    (proj / "assets").mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix="kosif_direct_"))
    # words
    if words_json and Path(words_json).exists():
        segs = json.loads(Path(words_json).read_text(encoding="utf-8"))
    else:
        segs = T.transcribe(clip, model)
        T.write_all(segs, proj / "transcript")
    segs = apply_fixes(segs, fixes)
    T.write_all(segs, proj / "transcript")                    # what the edit will show: review it, fix with --fix, re-run
    # plate: erase captions, restore, reframe, all-intra
    base = clip
    if decap:
        r = D.decaption(clip, tmp / "clean.mp4")
        base = tmp / "clean.mp4" if r.get("captions") else clip
    scale = f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H}"
    _run([FF, "-y", "-v", "error", "-i", str(base), "-an", "-vf", RL.RESTORE.format(scale=scale) + ",format=yuv420p",
          "-c:v", "libx264", "-preset", "slow", "-crf", "15", "-g", "1", "-keyint_min", "1", "-r", f"{info['fps']:.5f}", str(proj / "assets" / "plate.mp4")])
    _run([FF, "-y", "-v", "error", "-i", str(clip), "-vn", "-ac", "2", "-ar", "48000", "-af", RL.VOICE, str(proj / "assets" / "voice.wav")])
    words = [w for s in segs for w in s["words"]]
    music = ""
    _run([FF, "-y", "-v", "error", "-i", str(clip), "-vn", "-ac", "2", "-ar", "48000", str(tmp / "raw.wav")])
    if not RL.has_music_bed(tmp / "raw.wav", words):                  # judged on the raw mix (denoising lowers a bed)
        import score as SC
        sc = SC.Score(90, info["dur"], "D", "minor", seed=9)
        b = info["dur"] / (60 / 90)
        sc.arrange({"sections": [{"from": 2, "to": b * 0.4, "pad": True}, {"from": b * 0.4, "to": b, "pad": True, "bass": True}]})
        sc.mix(proj / "assets" / "music.wav")
        music = '<audio id="music" src="assets/music.wav" data-start="0" data-duration="{{SECONDS}}" data-volume="0.5" data-role="music" data-fade-out="0.4"></audio>'
    # shots and subjects (in output coordinates: fill-crop of the source)
    A = D.analyse(clip, band=(0.0, 0.01))
    fps = A["fps"]; sw, shh = info["w"], info["h"]
    s_ = max(W / sw, H / shh); offx, offy = (sw * s_ - W) / 2, (shh * s_ - H) / 2
    shots = []
    for a, b in A["shots"]:
        box = subject_box(clip, a, b, fps)
        sh = {"start": round(a / fps, 3), "end": round(b / fps, 3), "from": 1.03, "to": 1.09}
        if box:
            bx = (box[0] * sw * s_ - offx, box[1] * shh * s_ - offy, box[2] * sw * s_, box[3] * shh * s_)
            sh["box"] = (bx[0] / W, bx[1] / H, bx[2] / W, bx[3] / H)
            sh["cx"], sh["cy"] = round(bx[0] + bx[2] / 2), round(bx[1] + bx[3] * 0.4)
            if bx[3] < 0.2 * H:                                   # a small, far subject: start wider and push more
                sh["from"], sh["to"] = 1.12, 1.22
        else:
            sh["cx"], sh["cy"] = W // 2, round(H * 0.4)
        shots.append(sh)
    stress = word_stress(proj / "assets" / "voice.wav", words)
    edit = {"W": W, "H": H, "fps": round(fps, 3), "duration": round(info["dur"], 3), "palette": {"ivory": "#F5F0E6", "accent": accent},
            "credit": credit, "shots": shots, **plan(segs, shots, stress, W, H, info["dur"])}
    (proj / "edit.js").write_text("window.EDIT = " + MO.json_for_script(edit) + ";\n", encoding="utf-8")
    (proj / "edit.json").write_text(json.dumps(edit, ensure_ascii=False, indent=1), encoding="utf-8")
    html = TEMPLATE.read_text(encoding="utf-8").replace("{{MUSIC}}", music)
    for kk, v in {"{{W}}": W, "{{H}}": H, "{{SECONDS}}": round(info["dur"], 3), "{{FPS}}": round(fps), "{{TITLE}}": MO.html_text(name)}.items():
        html = html.replace(kk, str(v))
    (proj / "index.html").write_text(html, encoding="utf-8")
    MO.sync_assets(proj)
    rep = {"project": str(proj), "keywords": [k["text"] for k in edit["keys"]], "chapters": [c["text"] for c in edit["chapters"]],
           "motifs": [m["text"] for m in edit["motifs"]], "payoff": edit["payoff"]["lines"] if edit["payoff"] else None,
           "music": "original bed kept" if not music else "underscore"}
    if render:
        out = MO.render(str(proj), "studio", "looks", None, None, 1)
        rep["film"] = str(out)
    return rep


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("clip"); ap.add_argument("--name", required=True); ap.add_argument("--size", default="1080x1920")
    ap.add_argument("--model", default="large-v3"); ap.add_argument("--words"); ap.add_argument("--accent", default="#E7B65A")
    ap.add_argument("--credit"); ap.add_argument("--no-decaption", action="store_true"); ap.add_argument("--render", action="store_true")
    ap.add_argument("--fix", help='transcript corrections: "ما حدش=محدش;بتعودش ضايع=متقعدش تضيّع"')
    a = ap.parse_args()
    W, H = (int(v) for v in a.size.lower().split("x"))
    rep = direct(Path(a.clip), a.name, (W, H), a.model, Path(a.words) if a.words else None, a.accent, a.credit, not a.no_decaption, a.render, a.fix)
    print(json.dumps(rep, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
