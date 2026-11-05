#!/usr/bin/env python3
"""KOSIF World Film («التنين الأسود»): one world, one continuous camera, every frame drawn by code.

  world_film.py example --out JOB/world.plan.json         a small working plan to start from (no photos)
  world_film.py beats  PLAN.json [--out beats.md]          beat table to show the owner BEFORE building
  world_film.py check  PLAN.json [--json]                  storytelling, readability and camera rules
  world_film.py build  PLAN.json --out JOB/film.html       page = engine + camera + plan (assets copied)
  world_film.py review PLAN.json                           still times: every beat, every hit, every move

`check` exits 1 on any error. It enforces the brief's rules that can be measured:
  one hero per beat, every on-screen phrase once, no typed phrase that the narrator also says,
  big type (hero text and labels measured in screen pixels at the beat's camera), no unused decoration,
  hits land inside their beat (and on the named word when word timings are given), beats cover the
  voiceover exactly, and the camera never stops dead, never jerks and never cuts.
It proves structure, not taste: look at the review stills and camera sequences before rendering.
"""
from __future__ import annotations

import argparse
import html
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORLD = HERE.parent / "world"
ROOT = HERE.parents[3]
KINDS = {"desk", "map", "area", "pin", "route", "photo", "text", "book", "stamp"}
ACTIONS = {"circle", "glow", "lift", "open", "draw", "stamp"}
WORLD_KINDS = {"desk", "map"}
MIN_HERO_TEXT_PX = 84     # hero words: very large on a 1080-wide frame
MIN_LABEL_PX = 46         # nothing on screen smaller than this
MIN_PHOTO_PX = 0.55       # hero photo spans at least 55% of the frame width
STOP_SPEED = 0.35         # screen px per frame under which the camera counts as stopped
MAX_STOP = 0.4            # seconds the designed camera may stay under STOP_SPEED
MAX_JERK = 2.5            # max change of screen speed between frames (px/frame^2)
MAX_JUMP = 140            # px moved in one frame = a cut

AR_DIAC = re.compile(r"[ً-ْٰـ]")
STOP = {"يا", "في", "من", "على", "و", "ال", "the", "a", "of", "to", "and"}


def norm_words(s: str) -> list[str]:
    s = AR_DIAC.sub("", s or "")
    s = re.sub("[أإآ]", "ا", s).replace("ة", "ه").replace("ى", "ي")
    out = []
    for w in re.findall(r"[\w]+", s.lower()):
        w = re.sub(r"^(وال|بال|لل|ال|و|ب)(?=\w{3,})", "", w)
        if w and w not in STOP:
            out.append(w)
    return out


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def camera_samples(plan_path: Path, fps: int) -> dict:
    r = subprocess.run(["node", str(WORLD / "camera.cjs"), str(plan_path), "--fps", str(fps)],
                       capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


def beat_camera(plan, i):
    return plan["beats"][i]["camera"]


def check(plan: dict, plan_path: Path | None = None, camera: dict | None = None) -> tuple[list[str], dict]:
    errs: list[str] = []
    stats: dict = {}
    fmt = plan.get("format") or {}
    W, H, fps = fmt.get("width"), fmt.get("height"), fmt.get("fps", 30)
    if not (isinstance(W, int) and isinstance(H, int) and W > 0 and H > 0):
        return ["format.width/height must be positive whole numbers"], stats
    dur = plan.get("duration")
    if not isinstance(dur, (int, float)) or dur <= 0:
        return ["duration must be a positive number (the voiceover's exact length)"], stats
    if plan.get("audio_duration") and abs(plan["audio_duration"] - dur) > 1.0 / fps:
        errs.append(f"duration {dur} does not match the voiceover ({plan['audio_duration']} s): length must match exactly")
    objs = plan.get("objects") or []
    by = {}
    for o in objs:
        if o.get("kind") not in KINDS:
            errs.append(f"object {o.get('id')}: kind must be one of {', '.join(sorted(KINDS))}")
        if o.get("id") in by:
            errs.append(f"object id {o.get('id')} is used twice")
        by[o.get("id")] = o
    if sum(1 for o in objs if o.get("kind") == "map") > 1:
        errs.append("one world only: at most one map")
    beats = plan.get("beats") or []
    if len(beats) < 2:
        errs.append("need at least 2 beats")
    # timing: beats tile the voiceover (small breaths between lines are allowed inside a beat's end)
    t = 0.0
    for i, b in enumerate(beats):
        a, e = b.get("start"), b.get("end")
        if not isinstance(a, (int, float)) or not isinstance(e, (int, float)) or e <= a:
            errs.append(f"beat {i}: start/end invalid")
            continue
        if abs(a - t) > 1e-3:
            errs.append(f"beat {i} starts at {a}, expected {round(t, 3)}: beats must follow each other with no gap")
        t = e
    if beats and abs(t - dur) > 1e-3:
        errs.append(f"beats end at {round(t, 3)} but the film is {dur} s")
    # one hero per beat, text once, never both said and typed
    seen_text: dict[str, int] = {}
    # "never both" holds across the whole film: a typed phrase may not be one the narrator says anywhere
    narr_all = set(w for b in beats for w in norm_words(b.get("narration", "")))
    used = set()
    words = plan.get("words") or []
    for i, b in enumerate(beats):
        hero = b.get("hero")
        if isinstance(hero, list):
            errs.append(f"beat {i}: one hero only, found {len(hero)}")
            continue
        if hero not in by:
            errs.append(f"beat {i}: hero {hero!r} is not an object")
            continue
        used.add(hero)
        for x in b.get("also") or []:
            used.add(x)
        if not (isinstance(b.get("start"), (int, float)) and isinstance(b.get("end"), (int, float))):
            continue  # already reported as invalid start/end
        cam = b.get("camera") or {}
        if not all(isinstance(cam.get(k), (int, float)) for k in ("x", "y", "zoom")) or cam.get("zoom", 0) <= 0:
            errs.append(f"beat {i}: camera needs x, y and a positive zoom")
            continue
        z = cam["zoom"]
        narr = norm_words(b.get("narration", ""))
        tid = b.get("text")
        if tid:
            if tid not in by or by[tid].get("kind") != "text":
                errs.append(f"beat {i}: text {tid!r} is not a text object")
            else:
                used.add(tid)
                to = by[tid]
                phrase = " ".join(norm_words(to.get("text", "")))
                if phrase in seen_text:
                    errs.append(f"beat {i}: on-screen text {to['text']!r} already appeared in beat {seen_text[phrase]}: every phrase appears once")
                seen_text[phrase] = i
                tw = norm_words(to.get("text", ""))
                said = [w for w in tw if w in narr_all]
                if tw and len(said) * 2 >= len(tw):
                    errs.append(f"beat {i}: {to['text']!r} is typed while the narrator says it ({' '.join(said)}): show it or type it, never both")
                px = to.get("size", 0) * z
                need = MIN_HERO_TEXT_PX if hero == tid else MIN_LABEL_PX
                if px < need:
                    errs.append(f"beat {i}: text {to['text']!r} is {px:.0f}px on screen, needs {need}px+ to read on a phone in one second")
                if len(tw) > 7:
                    errs.append(f"beat {i}: {to['text']!r} has {len(tw)} words: too much to read in one beat")
        h = by[hero]
        if h.get("kind") == "photo" and h.get("w", 0) * z < MIN_PHOTO_PX * W:
            errs.append(f"beat {i}: hero photo {hero} is {h.get('w', 0) * z:.0f}px wide, push in to {MIN_PHOTO_PX * W:.0f}px+")
        if h.get("kind") == "text" and h.get("size", 0) * z < MIN_HERO_TEXT_PX:
            errs.append(f"beat {i}: hero text is {h.get('size', 0) * z:.0f}px, needs {MIN_HERO_TEXT_PX}px+")
        if h.get("kind") == "text" and tid is None:
            tw = norm_words(h.get("text", ""))
            if tw and sum(w in narr_all for w in tw) * 2 >= len(tw):
                errs.append(f"beat {i}: hero text {h['text']!r} repeats the narration")
        hs = b.get("hits") or ([b["hit"]] if b.get("hit") else [])
        for hh in hs:
            tgt = hh.get("target", hero)
            used.add(tgt)
            if hh.get("action") not in ACTIONS:
                errs.append(f"beat {i}: hit action must be one of {', '.join(sorted(ACTIONS))}")
            if tgt not in by:
                errs.append(f"beat {i}: hit target {tgt!r} is not an object")
            ht = hh.get("t")
            if not isinstance(ht, (int, float)) or not (b["start"] - 1e-6 <= ht <= b["end"] + 1e-6):
                errs.append(f"beat {i}: hit at {ht} is outside the beat {b['start']}-{b['end']}")
            elif hh.get("word") and words:
                cand = [w for w in words if norm_words(w["w"]) == norm_words(hh["word"]) and b["start"] - 0.05 <= w["start"] <= b["end"]]
                if not cand:
                    errs.append(f"beat {i}: hit word {hh['word']!r} is not spoken in this beat")
                elif min(abs(w["start"] - ht) for w in cand) > 1.5 / fps:
                    errs.append(f"beat {i}: hit at {ht} misses the word {hh['word']!r} (said at {cand[0]['start']}): land it on the word")
            if hh.get("action") == "draw" and not isinstance(hh.get("from"), (int, float)):
                errs.append(f"beat {i}: a draw hit needs 'from' (when the line starts drawing)")
    for o in objs:
        if o.get("kind") in WORLD_KINDS or o.get("kind") == "pin":
            continue
        if o.get("id") not in used:
            errs.append(f"object {o.get('id')} ({o.get('kind')}) is never a hero, a text or a hit target: leave it out (less is more)")
    # camera motion
    sampleable = all(isinstance(b.get("start"), (int, float)) and isinstance(b.get("end"), (int, float))
                     and all(isinstance((b.get("camera") or {}).get(k), (int, float)) for k in ("x", "y", "zoom"))
                     and (b.get("camera") or {}).get("zoom", 0) > 0 for b in beats)
    if camera is None and plan_path is not None and sampleable:
        try:
            camera = camera_samples(plan_path, fps)
        except (OSError, subprocess.CalledProcessError) as e:
            errs.append(f"camera could not be sampled with node: {e}")
    if camera:
        s = camera["samples"]
        speeds, jumps = [], []
        for a, b in zip(s, s[1:]):
            z = (a[3] + b[3]) / 2
            v = math.hypot((b[1] - a[1]) * z, (b[2] - a[2]) * z) + abs(math.log(b[3] / a[3])) * W * 0.5
            speeds.append(v)
        run = best = 0
        stop_at = None
        for i, v in enumerate(speeds):
            run = run + 1 if v < STOP_SPEED else 0
            if run > best:
                best, stop_at = run, s[i][0]
        jerk = max((abs(b - a) for a, b in zip(speeds, speeds[1:])), default=0)
        stats["camera"] = {"max_speed_px_per_frame": round(max(speeds), 2), "min_speed_px_per_frame": round(min(speeds), 3),
                           "longest_stop_s": round(best / fps, 3), "max_jerk": round(jerk, 3), "keys": len(camera["keys"])}
        if best / fps > MAX_STOP:
            errs.append(f"camera stops dead for {best / fps:.2f}s near {stop_at}s: keep it drifting toward the next move")
        if jerk > MAX_JERK:
            i = max(range(len(speeds) - 1), key=lambda k: abs(speeds[k + 1] - speeds[k]))
            errs.append(f"camera jerks near {s[i][0]}s (speed changes by {jerk:.1f}px/frame in one frame): ease the move")
        if max(speeds) > MAX_JUMP:
            errs.append(f"camera moves {max(speeds):.0f}px in one frame: that reads as a cut, slow the travel")
    return errs, stats


def beats_md(plan: dict) -> str:
    by = {o["id"]: o for o in plan.get("objects", [])}
    rows = ["| الوقت | الكلام | البطل الوحيد | نص على الشاشة | اللحظة على الكلمة |", "|---|---|---|---|---|"]
    for b in plan["beats"]:
        h = by.get(b["hero"], {})
        hero = (h.get("label") or h.get("text") or b["hero"]).replace("\n", " ")
        txt = by.get(b.get("text") or "", {}).get("text", "—").replace("\n", " · ")
        hs = b.get("hits") or ([b["hit"]] if b.get("hit") else [])
        hit = "؛ ".join(f"{x['action']} على «{x.get('word', '')}» ({x['t']:.2f})" for x in hs) or "—"
        rows.append(f"| {b['start']:.2f}–{b['end']:.2f} | {b.get('narration') or '(موسيقى)'} | {hero} | {txt} | {hit} |")
    head = f"# {plan.get('title', 'World film')}\n\n**العالم:** {plan.get('world_note', '')}\n\n"
    return head + "\n".join(rows) + "\n"


def review_times(plan: dict) -> dict:
    """Stills for every beat (mid and hit) plus frame sequences across every camera move."""
    fps = plan["format"].get("fps", 30)
    beats, moves = [], []
    for i, b in enumerate(plan["beats"]):
        ts = {round(b["start"] + (b["end"] - b["start"]) * 0.55, 3)}
        for h in b.get("hits") or ([b["hit"]] if b.get("hit") else []):
            ts.add(round(h["t"] + 0.35, 3))
        beats += sorted(ts)
        if i + 1 < len(plan["beats"]):
            c = plan["beats"][i + 1]["start"]
            moves.append([round(max(0, c - 1.0 + k * (2.0 / 7)), 3) for k in range(8)])
    return {"beats": beats, "moves": moves, "fps": fps}


def build(plan_path: Path, out: Path) -> Path:
    plan = load(plan_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    base = plan_path.parent
    for rel in [o["src"] for o in plan["objects"] if o.get("kind") == "photo"] + [f["src"] for f in plan.get("fonts", [])]:
        if Path(rel).is_absolute() or ".." in Path(rel).parts:
            raise SystemExit(f"asset path {rel!r} must stay inside the job folder (relative, no '..')")
    for o in plan["objects"]:
        if o.get("kind") == "photo":
            src = (base / o["src"]).resolve()
            dst = out.parent / o["src"]
            if src != dst.resolve():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
    for f in plan.get("fonts", []):
        dst = out.parent / f["src"]
        src = (base / f["src"]) if (base / f["src"]).is_file() else ROOT / f.get("from", "")
        if src.is_file() and src.resolve() != dst.resolve():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    data = json.dumps(plan, ensure_ascii=False).replace("</", "<\\/")
    page = f"""<!doctype html>
<html lang="ar"><head><meta charset="utf-8"><title>{html.escape(str(plan.get('title', 'world film')))}</title>
<style>html,body{{margin:0;background:#000;overflow:hidden}}canvas{{display:block}}</style></head>
<body><canvas id="film"></canvas>
<script>window.WORLD_PLAN = {data};</script>
<script>{(WORLD / 'camera.cjs').read_text(encoding='utf-8')}</script>
<script>{(WORLD / 'engine.js').read_text(encoding='utf-8')}</script>
</body></html>
"""
    out.write_text(page, encoding="utf-8")
    return out


def example_plan() -> dict:
    """A 12-second world film that passes every check: a map, a book, a route, a stamp, one title."""
    proj = {"lon0": 24.0, "lat0": 34.0, "k": 150.0, "ky": 1.1}
    sea = [[34.5, 23.0], [34.5, 36.5], [31.3, 34.2], [31.5, 31.0], [31.6, 25.1], [32.4, 23.0]]
    red = [[30.0, 32.5], [27.2, 33.8], [22.0, 36.9], [16.9, 42.6], [12.6, 43.4], [9.0, 44.0], [9.0, 61.0],
           [25.3, 61.0], [26.4, 56.3], [25.2, 55.3], [24.2, 52.5], [26.2, 50.2], [30.0, 49.0], [28.4, 48.6],
           [24.6, 51.3], [21.4, 39.1], [28.0, 34.6], [29.5, 34.9], [27.9, 34.3]]
    egypt = [[31.6, 25.1], [31.5, 31.0], [31.3, 34.2], [29.5, 34.9], [27.9, 34.3], [30.0, 32.5], [27.2, 33.8],
             [22.0, 36.9], [22.0, 25.0]]
    g = lambda lat, lon: [1000 + (lon - 24) * 150, 1100 + (34 - lat) * 165]
    a, b = g(31.0, 31.0), g(25.2, 55.3)
    objects = [
        {"id": "desk", "kind": "desk", "x": -1400, "y": -1600, "w": 9800, "h": 9400},
        {"id": "map", "kind": "map", "x": 1000, "y": 1100, "w": 5550, "h": 4125, "projection": proj,
         "seas": [sea, red], "rivers": [[[31.4, 30.4], [30.0, 31.2], [24.1, 32.9], [22.0, 31.4]]]},
        {"id": "egypt", "kind": "area", "poly": egypt, "label": "مصر على الخريطة"},
        {"id": "pin_a", "kind": "pin", "x": a[0], "y": a[1], "enter": 0.5},
        {"id": "book", "kind": "book", "x": a[0] + 500, "y": a[1] + 400, "w": 640, "rot": 5, "enter": 2.6,
         "label": "كتاب بيتفتح"},
        {"id": "route", "kind": "route", "path": [[31.0, 31.0], [35.0, 43.0], [25.2, 55.3]], "width": 44,
         "dash": 90, "gap": 60, "label": "خط الرحلة"},
        {"id": "t_place", "kind": "text", "text": "دبي", "x": b[0], "y": b[1] + 260, "size": 420, "enter": 7.9, "exit": 9.4},
        {"id": "t_end", "kind": "text", "text": "قصة نجاح", "x": 3600, "y": 4300, "size": 440, "enter": 9.3},
        {"id": "stamp", "kind": "stamp", "text": "الأولى", "x": 3600, "y": 4800, "size": 320, "rot": -8},
    ]
    beats = [
        {"start": 0.0, "end": 3.0, "narration": "هنا بدأت الحكاية", "hero": "egypt",
         "camera": {"x": 1950, "y": 2250, "zoom": 0.36, "from": {"x": 3300, "y": 2900, "zoom": 0.2}},
         "hits": [{"t": 0.8, "action": "circle", "target": "egypt"}]},
        {"start": 3.0, "end": 6.0, "narration": "كتاب واحد", "hero": "book",
         "camera": {"x": a[0] + 500, "y": a[1] + 400, "zoom": 1.25}, "hits": [{"t": 3.6, "action": "open"}]},
        {"start": 6.0, "end": 9.0, "narration": "رحلة لكل الدنيا", "hero": "route", "text": "t_place",
         "camera": {"x": (a[0] + b[0]) / 2, "y": 1950, "zoom": 0.205, "drift": 0.03},
         "hits": [{"t": 8.0, "action": "draw", "from": 6.2}]},
        {"start": 9.0, "end": 12.0, "narration": "والنهاية بداية", "hero": "t_end", "text": "t_end", "also": ["stamp"],
         "camera": {"x": 3600, "y": 3900, "zoom": 0.22, "end_push": 1.06},
         "hits": [{"t": 10.4, "action": "stamp", "target": "stamp"}]},
    ]
    return {"schema": "kosif.world_film.plan.v1", "title": "مثال: عالم واحد وكاميرا واحدة",
            "world_note": "خريطة ورق على مكتب خشب، والكاميرا حركة واحدة متصلة",
            "format": {"width": 1080, "height": 1920, "fps": 30}, "duration": 12.0, "seed": 7,
            "font": "Cairo", "fonts": [{"family": "Cairo", "src": "fonts/Cairo.ttf",
                                        "from": ".claude/skills/kosif-superpowers/proofs/_shared/fonts/Cairo[slnt,wght].ttf"}],
            "objects": objects, "beats": beats}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("example"); p.add_argument("--out", required=True)
    p = sub.add_parser("beats"); p.add_argument("plan"); p.add_argument("--out")
    p = sub.add_parser("check"); p.add_argument("plan"); p.add_argument("--json", action="store_true")
    p = sub.add_parser("build"); p.add_argument("plan"); p.add_argument("--out", required=True)
    p = sub.add_parser("review"); p.add_argument("plan")
    a = ap.parse_args(argv)
    if a.cmd == "example":
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(json.dumps(example_plan(), ensure_ascii=False, indent=1), encoding="utf-8")
        print(a.out)
        return 0
    plan = load(a.plan)
    if a.cmd == "beats":
        md = beats_md(plan)
        if a.out:
            Path(a.out).write_text(md, encoding="utf-8")
        print(md)
        return 0
    if a.cmd == "check":
        errs, stats = check(plan, Path(a.plan))
        if a.json:
            print(json.dumps({"ok": not errs, "errors": errs, "stats": stats}, ensure_ascii=False, indent=1))
        else:
            for e in errs:
                print("FAIL", e)
            print(json.dumps(stats, ensure_ascii=False))
            print("OK" if not errs else f"{len(errs)} problem(s)")
        return 1 if errs else 0
    if a.cmd == "build":
        print(build(Path(a.plan), Path(a.out)))
        return 0
    if a.cmd == "review":
        print(json.dumps(review_times(plan)))
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
