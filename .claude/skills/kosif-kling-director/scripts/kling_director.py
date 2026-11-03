#!/usr/bin/env python3
"""kling_director.py: build a Kling 4.0 short-film prompt pack from a story line, then lint it.

  python3 kling_director.py plan SECONDS [--flash] [--json]
  python3 kling_director.py build --task "the story" --seconds N --out DIR [--ratio 21:9] [--flash] [--json]
  python3 kling_director.py check PROMPT.txt [--duration N] [--flash] [--json]
  python3 kling_director.py --self-test

plan   splits a film into generation blocks (30 s or less; 20 s or less with --flash), as Step 2 of
       the director method says: 60 s = 2 blocks, 90 s = 3 blocks.
build  writes, for every block, a master prompt in the 15-header order of template H
       (block_NN.txt), a 3x3 storyboard prompt whose 9 panels follow the block's clock
       (storyboard_NN.txt), and plan.json with the settings box, the takes plan and every
       block's lint result. Shots are at most 6 s, their ranges start at 0 and touch end to end,
       so the director only fills the [bracketed] slots. The story line goes into SCENE CONTEXT
       untouched: if it says "8K" or names a camera brand, the lint says so (exit 1).
check  runs the living-site gate tools/kling_lint.py on a prompt (same checks, same exit codes).

It writes text only: it never calls Kling, Higgsfield or Nano Banana and spends no credits.
Exit 0 = every block passes the lint, 1 = a block fails, 2 = usage error.
Method: .claude/skills/living-site/references/level-2-kling-director.md (see ../ORIGIN.md).
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
LINT_PATH = HERE.parents[1] / "living-site" / "tools" / "kling_lint.py"
SHOT_MAX = 6  # edited shots longer than 6 s draw a lint warning
PANELS = ("top-left", "top-center", "top-right", "middle-left", "middle-center", "middle-right",
          "bottom-left", "bottom-center", "bottom-right")
RATIOS = ("21:9", "16:9", "9:16", "1:1")


def load_lint():
    spec = importlib.util.spec_from_file_location("kling_lint", LINT_PATH)
    if spec is None or not LINT_PATH.is_file():
        raise SystemExit(f"kling_lint.py not found at {LINT_PATH}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def plan(seconds: int, flash: bool = False) -> list[tuple[int, int]]:
    """Even blocks of whole seconds, none longer than the model's limit (30 s, Flash 20 s)."""
    top = 20 if flash else 30
    n = max(1, math.ceil(seconds / top))
    base, extra = divmod(seconds, n)
    out, t = [], 0
    for i in range(n):
        size = base + (1 if i < extra else 0)
        out.append((t, t + size))
        t += size
    return out


def cuts(duration: float, parts: int) -> list[tuple[float, float]]:
    """parts ranges from 0 to duration that touch end to end (one decimal)."""
    edges = [round(duration * i / parts, 1) for i in range(parts)] + [float(duration)]
    return list(zip(edges, edges[1:]))


def _fmt(x: float) -> str:
    return f"{x:.1f}"


FRAMINGS = ("Wide establishing frame, 84° diagonal FOV, lens at waist height, three-quarter angle",
            "Medium shot, 47° FOV, lens at chest height",
            "Close-up, 47° FOV, eye level, focus on the eyes",
            "Over-the-shoulder medium shot, 57° FOV",
            "Insert on the key prop, 29° FOV",
            "Medium-full shot, 63° FOV, low-angle")
MOVES = ("slow dolly-in", "side-tracking", "locked-off", "handheld", "locked-off", "crane up")


def master_prompt(task: str, index: int, total: int, duration: int, ratio: str) -> str:
    story = " ".join(task.split())
    shots = cuts(duration, max(1, math.ceil(duration / SHOT_MAX)))
    timing = []
    for n, (a, b) in enumerate(shots, 1):
        frame = FRAMINGS[(n - 1) % len(FRAMINGS)]
        move = MOVES[(n - 1) % len(MOVES)]
        end = "Hard cut." if n < len(shots) else "Final image holds to the last frame."
        timing.append(f"{_fmt(a)}-{_fmt(b)}s — SHOT {n} — @loc_[place]_v1. {frame}, {move}. "
                      f"[ONE action and its physical consequence]. {end}")
    return "\n".join([
        "SCENE CONTEXT",
        f"Block {index} of {total}. {duration} s, {ratio}. Story: {story}",
        "[2-4 sentences: who, where, what happens in this block, how it ends, genre and mood.]",
        "",
        "ACTIVE REFERENCES",
        "@Image1 — CHARACTER — [NAME]: face, hair, build and wardrobe match the reference 100%. "
        "Reference controls identity only; backdrop, lighting and pose are not inherited.",
        "@Image2 — LOCATION — [PLACE]: controls layout, materials and practical lights. "
        "The reference's camera angle and framing are not inherited.",
        "@Image3 — STORYBOARD: follow its shot order and framing. Do not render the storyboard itself.",
        "",
        "LOCATION MAP",
        "[Geometry in metres, where each object sits, screen direction frame-left / frame-right, "
        "where the camera works from.]",
        "",
        "FIRST FRAME AND SPATIAL BLOCKING",
        "[What is in frame on frame 1: lens height, angle, who stands where.] Exactly 1 person in the shot.",
        "",
        "FORMAT MODE",
        f"Controlled multi-shot sequence, {len(shots)} shots, hard cuts between shots.",
        "",
        "OPTICS",
        "Close-ups 47°, medium-wide 63°, wide 84°, inserts 29°; anamorphic rectilinear character; "
        "lens locked within each shot; focus on the eyes at held moments.",
        "",
        "CAMERA",
        "Dolly and gimbal moves motivated by the action, at most two moves per shot.",
        "",
        "ACTION TIMING",
        *timing,
        "",
        "ACTING TASK — [NAME]",
        "SCENE DIRECTION (shared, unspoken): [...]. MOTIVE: [...]. GOAL: [...]. OBSTACLE: [...].",
        "TACTIC: [verbs aimed at the partner; the work happens in the eyes]. "
        "Gaze stays engaged in the task with a natural blink cadence.",
        "",
        "PHYSICS",
        "[Weight, cloth, smoke, dust and footfalls: how each object really behaves.]",
        "",
        "LIGHTING",
        "[Practical sources only: positions, colour temperature, what stays dark.]",
        "",
        "AUDIO",
        "English lines only, or silent acting with Arabic voice-over added in the edit. "
        "[Ambience; SFX timed to the action.] No music. No subtitles.",
        "",
        "STYLE",
        "[Genre look], fine film grain, natural skin texture with pores, one consistent grade.",
        "",
        "QUALITY",
        "Readable faces and hands at held moments; natural 180° shutter motion blur on fast moves; "
        "stable temporal continuity; consistent anatomy; each object stays one consistent object.",
        "",
        "POSITIVE CONSTRAINTS",
        "Exactly 1 person in every shot; [handedness]; [object sizes against known things]; "
        "screen direction stays frame-left to frame-right; [what the last frame shows].",
        "",
    ])


def storyboard_prompt(task: str, index: int, duration: int, ratio: str) -> str:
    story = " ".join(task.split())
    lines = [f"Create a 3x3 grid storyboard (nine equal panels, thin white borders, {ratio} overall, 2K) "
             f"for a short film, block {index}. Story: {story}",
             "References: Image 1 is [NAME] — keep the face, hair and wardrobe the same in every panel; "
             "Image 2 is the location.",
             "Consistent practical lighting and grade across all panels: [light + palette]. Photorealistic "
             "film stills, anamorphic look with oval bokeh and horizontal flares, fine film grain, "
             "three-quarter angles, varied framing. Panels carry pictures only, free of text, numbers and captions."]
    for n, (name, (a, b)) in enumerate(zip(PANELS, cuts(duration, 9)), 1):
        lines.append(f"Panel {n} ({name}): {_fmt(a)}-{_fmt(b)}s — [framing, angle, height] — [what we see].")
    return "\n".join(lines) + "\n"


def summarize(results: list[dict]) -> dict:
    failed = [t["name"] for t in results if t["status"] == "FAIL"]
    warned = [t["name"] for t in results if t["status"] == "warn"]
    return {"result": "FAIL" if failed else "PASS", "failed": failed, "warnings": warned, "tests": results}


def build(task: str, seconds: int, out: Path, ratio: str = "21:9", flash: bool = False) -> dict:
    lint = load_lint()
    out.mkdir(parents=True, exist_ok=True)
    blocks = plan(seconds, flash)
    rows = []
    for i, (a, b) in enumerate(blocks, 1):
        dur = b - a
        text = master_prompt(task, i, len(blocks), dur, ratio)
        (out / f"block_{i:02d}.txt").write_text(text, encoding="utf-8")
        (out / f"storyboard_{i:02d}.txt").write_text(storyboard_prompt(task, i, dur, ratio), encoding="utf-8")
        rows.append({"block": i, "film_range_s": [a, b], "duration_s": dur,
                     "prompt": f"block_{i:02d}.txt", "storyboard": f"storyboard_{i:02d}.txt",
                     "lint": summarize(lint.lint(text, dur, flash))})
    doc = {"schema": "kosif.kling-director.plan.v1", "task": task, "seconds": seconds, "ratio": ratio,
           "model": "Kling 4.0 Flash" if flash else "Kling 4.0", "blocks": rows,
           "settings": {"mode": "Omni Reference (images, videos, elements) or Keyframes (images only); never both",
                        "resolution": "1080p", "flash_allowed": all(r["duration_s"] <= 20 for r in rows),
                        "upload_order": "@Image1 character sheet, @Image2 location plate, @Image3 storyboard"},
           "takes_plan": "2-4 takes per block; quote credits as takes x blocks and log each paid job in "
                         "living-site tools/ledger.py before generating",
           "continuity": "the last frame of block N becomes the first keyframe of block N+1",
           "credits_spent": 0,
           "result": "PASS" if all(r["lint"]["result"] == "PASS" for r in rows) else "FAIL"}
    (out / "plan.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return doc


PLANTED = {"polish": ("STYLE\n", "STYLE\n8K masterpiece, "),
           "brands": ("OPTICS\n", "OPTICS\nShot on an ARRI Alexa. "),
           "arabic-dlg": ("AUDIO\n", "AUDIO\nHe says: «يا صاحبي استنى». "),
           "timing": ("SHOT 2 —", "SHOT 2 — (starts late)")}


def plant(text: str) -> str:
    """Four known mistakes: polish words, a camera brand, Arabic dialogue, and a gap in the clock."""
    for old, new in PLANTED.values():
        text = text.replace(old, new, 1)
    lines = text.splitlines()
    for k, line in enumerate(lines):  # move SHOT 2's start 0.5 s later: a gap after SHOT 1
        if "SHOT 2 —" in line:
            a, rest = line.split("-", 1)
            lines[k] = f"{float(a) + 0.5:.1f}-{rest}"
            break
    return "\n".join(lines) + "\n"


def self_test() -> int:
    lint = load_lint()
    checks = []
    for s in (3, 29, 30, 31, 45, 60, 90, 100):
        checks.append((f"plan {s} s matches kling_lint.plan", plan(s) == lint.plan(s)))
    checks.append(("90 s = 3 blocks of 30 s", plan(90) == [(0, 30), (30, 60), (60, 90)]))
    checks.append(("Flash 45 s = 3 blocks of at most 20 s", plan(45, True) == [(0, 15), (15, 30), (30, 45)]))
    with tempfile.TemporaryDirectory() as tmp:
        doc = build("A courier races the rain to deliver one last letter.", 60, Path(tmp))
        checks.append(("60 s builds 2 blocks of 30 s", [r["film_range_s"] for r in doc["blocks"]] == [[0, 30], [30, 60]]))
        checks.append(("every built block passes the lint", doc["result"] == "PASS"))
        text = (Path(tmp) / "block_01.txt").read_text(encoding="utf-8")
        bad = summarize(lint.lint(plant(text), 30))
        checks.append(("all 4 planted flaws caught", set(PLANTED) <= set(bad["failed"])))
        loud = build("Perfect 8K hero shot on an ARRI camera.", 10, Path(tmp) / "loud")
        checks.append(("polish and brand words in the story are reported",
                       {"polish", "brands"} <= set(loud["blocks"][0]["lint"]["failed"])))
    for name, ok in checks:
        print(f"{'ok  ' if ok else 'FAIL'} {name}")
    passed = all(ok for _, ok in checks)
    print("SELF-TEST PASS" if passed else "SELF-TEST FAIL")
    return 0 if passed else 1


def main(argv: list[str]) -> int:
    if argv == ["--self-test"]:
        return self_test()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--self-test", action="store_true", help="known-answer checks, then exit")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan", help="split a film into generation blocks")
    p.add_argument("seconds", type=int)
    p.add_argument("--flash", action="store_true")
    p.add_argument("--json", action="store_true")
    b = sub.add_parser("build", help="write master prompts, storyboards and plan.json, then lint them")
    b.add_argument("--task", required=True, help="the story line, in any language")
    b.add_argument("--seconds", type=int, required=True)
    b.add_argument("--out", type=Path, required=True)
    b.add_argument("--ratio", choices=RATIOS, default="21:9")
    b.add_argument("--flash", action="store_true")
    b.add_argument("--json", action="store_true")
    c = sub.add_parser("check", help="lint one prompt with living-site tools/kling_lint.py")
    c.add_argument("prompt", type=Path)
    c.add_argument("--duration", type=float)
    c.add_argument("--flash", action="store_true")
    c.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.cmd in ("plan", "build") and a.seconds < 3:
        ap.error("seconds must be 3 or more (Kling's shortest generation)")
    if a.cmd == "plan":
        rows = plan(a.seconds, a.flash)
        if a.json:
            print(json.dumps({"blocks": [list(r) for r in rows]}))
        else:
            for i, (x, y) in enumerate(rows, 1):
                print(f"block {i}: {x}-{y} s ({y - x} s)")
        return 0
    if a.cmd == "build":
        if not a.task.strip():
            ap.error("--task is empty")
        doc = build(a.task, a.seconds, a.out, a.ratio, a.flash)
        if a.json:
            print(json.dumps(doc, ensure_ascii=False, indent=1))
        else:
            for r in doc["blocks"]:
                extra = f" (failed: {', '.join(r['lint']['failed'])})" if r["lint"]["failed"] else ""
                print(f"block {r['block']}: {r['film_range_s'][0]}-{r['film_range_s'][1]} s -> {r['prompt']}, "
                      f"{r['storyboard']}: {r['lint']['result']}{extra}")
            print(doc["result"], "-", a.out / "plan.json", "- no credits spent")
        return 0 if doc["result"] == "PASS" else 1
    lint = load_lint()
    try:
        text = a.prompt.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"cannot read {a.prompt}: {exc}", file=sys.stderr)
        return 2
    return lint.report(lint.lint(text, a.duration, a.flash), a.json)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
