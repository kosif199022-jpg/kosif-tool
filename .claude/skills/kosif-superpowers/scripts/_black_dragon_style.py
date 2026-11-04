#!/usr/bin/env python3
"""Black Dragon style adapter: scaffold one catalog motion style and render real frames of it.

Usage: _black_dragon_style.py STYLE_ID ARTIFACT [--task=TEXT] [--keep-frames]

Steps, all inside ARTIFACT's own .work folder (never in the repository tree):
  1. `python3 tools/kosif.py scaffold STYLE_ID <work>/scaffold --starter html-canvas`
     (the catalog's real scaffold command: STYLE.md, PLAN.md, TEST_REPORT.md, words.json,
     REQUEST.md and a copy of the deterministic html-canvas starter film).
  2. The scaffolded starter is given the style's identity from its STYLE.json: the title
     words become the style's name, the frame size is the style's own `aspect` (1080x1920
     when it has none), and the Google Fonts link is dropped so the render is offline.
  3. Headless Chromium (Playwright, via _black_dragon_style_frames.cjs) seeks the film to
     t=1.5 s, t=5.0 s and t=1.5 s again through the renderer contract (window.__kosif.seek)
     and screenshots each frame.

Checks (exit 0 only when every one passes):
  * the style is in catalog/styles.json and styles/<id>/STYLE.json carries the same id;
  * the scaffold exited 0 and wrote every expected file, and REQUEST.md names this style;
  * the page loaded with no JavaScript or console error and exposes the seek contract;
  * every frame has exactly the expected pixel size;
  * every frame is not blank (grey-level standard deviation above STD_MIN);
  * the two times differ (mean pixel change and changed-pixel share above thresholds):
    the film moves with time, it is not a static slide;
  * seeking back to t=1.5 s gives the identical frame (time-driven and deterministic);
  * known answers read from the DOM: at t=1.5 s the title shows exactly the style's name
    words, fully faded in; at t=5.0 s the counter shows the value the timeline's easing
    formula gives at that time (computed here independently).

What this is not: the frame is the shared KOSIF html-canvas starter, scaffolded for this
style and retitled and sized from its STYLE.json. It proves the style's scaffold-and-render
path works on this machine now; it does not prove that the look described in the style's
SKILL.md has been designed. The artifact says so in `mode`.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
SKILL = SCRIPTS.parent
REPO = SKILL.parents[2]
HELPER = SCRIPTS / "_black_dragon_style_frames.cjs"
SCHEMA = "kosif.black-dragon.style-adapter.v1"
T1, T2 = 1.5, 5.0
TIMES = [T1, T2, T1]
STD_MIN = 6.0           # grey-level standard deviation (0..255) a non-blank frame must exceed
MOTION_MEAN_MIN = 1.0   # mean absolute grey change between T1 and T2
CHANGED_SHARE_MIN = 0.01  # share of pixels whose grey level moved by more than CHANGED_DELTA
CHANGED_DELTA = 8
DEFAULT_SIZE = (1080, 1920)
SCAFFOLD_FILES = ("STYLE.md", "PLAN.md", "TEST_REPORT.md", "words.json", "REQUEST.md",
                  "html-canvas/index.html", "html-canvas/timeline.js", "html-canvas/words.js")
TITLE_ANCHOR = "const titleWords = ['الحركة', 'تبدأ', 'مع', 'أول', 'كلمة'];"
FONT_LINK = re.compile(r'^<link rel="(?:preconnect|stylesheet)" href="https://fonts\.googleapis\.com[^"]*"[^>]*>\n', re.M)
MAX_TITLE_WORDS = 6
MODE = ("scaffold + offline headless-Chromium frames of the shared html-canvas starter, retitled "
        "and sized from this style's STYLE.json; proves the style's scaffold/render path, not that "
        "the look in its SKILL.md was designed")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


class Report:
    def __init__(self) -> None:
        self.checks: list[dict] = []
        self.commands: list[dict] = []

    def check(self, name: str, passed: bool, value=None) -> bool:
        self.checks.append({"check": name, "pass": bool(passed), "value": value})
        return bool(passed)

    @property
    def passed(self) -> bool:
        return bool(self.checks) and all(c["pass"] for c in self.checks)

    def failed(self) -> list[str]:
        return [c["check"] for c in self.checks if not c["pass"]]


def load_style(style_id: str) -> tuple[dict, Path]:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", style_id):
        raise ValueError(f"invalid style id: {style_id!r}")
    catalog = json.loads((REPO / "catalog" / "styles.json").read_text(encoding="utf-8"))
    if style_id not in {row.get("id") for row in catalog if isinstance(row, dict)}:
        raise KeyError(f"style not in catalog/styles.json: {style_id}")
    path = REPO / "styles" / style_id / "STYLE.json"
    return json.loads(path.read_text(encoding="utf-8")), path


def frame_size(style: dict) -> tuple[int, int]:
    aspect = style.get("aspect")
    if isinstance(aspect, dict):
        w, h = aspect.get("w"), aspect.get("h")
        if isinstance(w, int) and isinstance(h, int) and 64 <= w <= 4096 and 64 <= h <= 4096:
            return w, h
    return DEFAULT_SIZE


def title_words(style: dict) -> list[str]:
    name = str(style.get("name_ar") or style.get("name") or style.get("id") or "").strip()
    words = [w for w in name.split() if w][:MAX_TITLE_WORDS]
    return words or [str(style.get("id"))]


def expected_counter(t: float) -> int:
    """The starter's scene-2 counter: round(lerp(0, 128, prog(t - 3.4, 0.2, 2.6, outQuint)))."""
    local = t - 3.4
    x = min(1.0, max(0.0, (local - 0.2) / 2.4))
    value = 128 * (1 - (1 - x) ** 5)
    return int(math.floor(value + 0.5))  # JavaScript Math.round


def customise(index: Path, words: list[str]) -> str:
    text = index.read_text(encoding="utf-8")
    if TITLE_ANCHOR not in text:
        raise ValueError("starter title anchor not found in scaffolded index.html")
    literal = json.dumps(words, ensure_ascii=False).replace("<", "\\u003c")
    text = text.replace(TITLE_ANCHOR, f"const titleWords = {literal};", 1)
    text = FONT_LINK.sub("", text)
    index.write_text(text, encoding="utf-8")
    return sha256(index)


def grey(path: Path):
    import numpy as np
    from PIL import Image
    with Image.open(path) as im:
        size = im.size
        arr = np.asarray(im.convert("L"), dtype=np.float32)
    return size, arr


def render_frames(html: Path, work: Path, size: tuple[int, int], times: list[float],
                  rep: Report, timeout: int = 45, attempts: int = 2) -> dict | None:
    """Run the frame helper; a crash or timeout of the browser itself is retried once.

    Every attempt is recorded in rep.commands. Only the helper's own failure is retried:
    the frames of a successful attempt are judged once, by frame_checks, never re-rolled.
    """
    problem = None
    for attempt in range(1, attempts + 1):
        try:
            out, problem = _render_once(html, work, size, times, rep, timeout, attempt)
        except subprocess.TimeoutExpired:
            rep.commands.append({"step": "render frames (headless Chromium)", "attempt": attempt,
                                 "exit_code": None, "error": f"timed out after {timeout} s"})
            out, problem = None, f"timed out after {timeout} s"
        if out is not None:
            break
    rep.check("frame helper exited 0 and wrote every frame", out is not None, problem if out is None else
              {"attempts": attempt})
    return out


def _render_once(html: Path, work: Path, size: tuple[int, int], times: list[float],
                 rep: Report, timeout: int, attempt: int):
    spec = {"html": str(html), "width": size[0], "height": size[1], "times": times,
            "out_dir": str(work / "frames")}
    spec_path = work / "frames_spec.json"
    spec_path.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
    argv = ["node", str(HELPER), str(spec_path)]
    done = subprocess.run(argv, cwd=work, text=True, capture_output=True, timeout=timeout,
                          stdin=subprocess.DEVNULL, check=False)
    step = {"step": "render frames (headless Chromium)", "attempt": attempt, "command": argv,
            "exit_code": done.returncode}
    if done.stderr.strip():
        step["stderr_tail"] = done.stderr[-600:]
    rep.commands.append(step)
    try:
        out = json.loads(done.stdout.strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError):
        out = None
    if done.returncode == 0 and out is not None and "fatal" not in out and len(out.get("frames", [])) == len(times):
        return out, None
    return None, (out or {}).get("fatal") or f"exit {done.returncode}"


def frame_checks(out: dict, size: tuple[int, int], rep: Report, expect: dict | None) -> list[dict]:
    """Every pixel and DOM check on the helper's output. `expect` holds the DOM known answers."""
    import numpy as np
    rep.check("page loaded with no JavaScript or console error", not out.get("errors"), out.get("errors")[:5])
    contract = out.get("contract")
    rep.check("page exposes the seek contract (window.__kosif)", bool(contract) and
              isinstance(contract.get("duration"), (int, float)) and contract["duration"] > 0, contract)
    frames, greys = [], []
    for row in out["frames"]:
        path = Path(row["png"])
        (w, h), arr = grey(path)
        std = float(arr.std())
        frames.append({"t": row["t"], "png": str(path), "bytes": path.stat().st_size, "sha256": sha256(path),
                       "width": w, "height": h, "grey_std": round(std, 3), "dom": row.get("dom")})
        greys.append(arr)
        rep.check(f"frame t={row['t']:.3f}s has size {size[0]}x{size[1]}", (w, h) == tuple(size), [w, h])
        rep.check(f"frame t={row['t']:.3f}s is not blank (grey std > {STD_MIN})", std > STD_MIN, round(std, 3))
    if len(greys) >= 2 and greys[0].shape == greys[1].shape:
        delta = np.abs(greys[0] - greys[1])
        mean, share = float(delta.mean()), float((delta > CHANGED_DELTA).mean())
    else:
        mean = share = 0.0
    rep.check(f"frames at t={TIMES[0]}s and t={TIMES[1]}s differ (motion: mean change > {MOTION_MEAN_MIN}, "
              f"changed share > {CHANGED_SHARE_MIN})", mean > MOTION_MEAN_MIN and share > CHANGED_SHARE_MIN,
              {"mean_abs_change": round(mean, 3), "changed_share": round(share, 4)})
    if len(frames) >= 3:
        rep.check(f"seeking back to t={TIMES[2]}s reproduces the identical frame (deterministic)",
                  frames[0]["sha256"] == frames[2]["sha256"] or bool(np.array_equal(greys[0], greys[2])),
                  [frames[0]["sha256"][:16], frames[2]["sha256"][:16]])
    if expect is not None:
        dom1 = frames[0]["dom"] or {}
        rep.check(f"t={T1}s title shows the style's name words", dom1.get("title_words") == expect["title_words"],
                  dom1.get("title_words"))
        opac = dom1.get("title_opacity") or []
        rep.check(f"t={T1}s every title word is faded in (opacity >= 0.99)",
                  bool(opac) and len(opac) == len(expect["title_words"]) and min(opac) >= 0.99, opac)
        dom2 = frames[1]["dom"] or {}
        rep.check(f"t={T2}s counter equals the easing formula's known answer {expect['counter']}",
                  dom2.get("counter") == str(expect["counter"]), dom2.get("counter"))
    return frames


def thumbnail(src: Path, dest: Path) -> dict:
    from PIL import Image
    with Image.open(src) as im:
        im = im.convert("RGB")
        im.thumbnail((360, 360))
        im.save(dest, "PNG", optimize=True)
    return {"path": str(dest), "bytes": dest.stat().st_size, "sha256": sha256(dest)}


def run(style_id: str, artifact: Path, task: str, keep_frames: bool) -> dict:
    started = time.monotonic()
    rep = Report()
    work = artifact.parent / (artifact.stem + ".work")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    result: dict = {"schema": SCHEMA, "entry": "style:" + style_id, "style_id": style_id, "mode": MODE,
                    "task": task, "work_dir": str(work)}
    try:
        style, style_json = load_style(style_id)
    except (OSError, ValueError, KeyError) as exc:
        rep.check("style record found in catalog and styles/<id>/STYLE.json", False, str(exc)[:300])
        return finish(result, rep, started)
    rep.check("styles/<id>/STYLE.json carries the same id", style.get("id") == style_id, style.get("id"))
    skill_md = REPO / "styles" / style_id / "SKILL.md"
    result["style"] = {"name": style.get("name"), "name_ar": style.get("name_ar"),
                       "category": style.get("category"), "aspect": style.get("aspect"),
                       "style_json": str(style_json.relative_to(REPO)), "style_json_sha256": sha256(style_json),
                       "skill_md_sha256": sha256(skill_md) if skill_md.is_file() else None}
    size = frame_size(style)
    words = title_words(style)
    expect = {"title_words": words, "counter": expected_counter(T2), "size": list(size)}
    result["known_answers"] = expect

    scaffold = work / "scaffold"
    argv = [sys.executable, str(REPO / "tools" / "kosif.py"), "scaffold", style_id, str(scaffold),
            "--starter", "html-canvas"]
    done = subprocess.run(argv, cwd=REPO, text=True, capture_output=True, timeout=60,
                          stdin=subprocess.DEVNULL, check=False)
    rep.commands.append({"step": "kosif.py scaffold", "command": argv, "exit_code": done.returncode,
                         "stdout_tail": done.stdout[-400:], "stderr_tail": done.stderr[-400:]})
    if not rep.check("scaffold exited 0", done.returncode == 0, done.returncode):
        return finish(result, rep, started)
    files = []
    for rel in SCAFFOLD_FILES:
        p = scaffold / rel
        ok = p.is_file() and p.stat().st_size > 0
        files.append({"path": str(p.relative_to(work)), "bytes": p.stat().st_size if p.is_file() else 0,
                      "sha256": sha256(p) if p.is_file() else None})
        rep.check(f"scaffold wrote {rel}", ok)
    result["scaffold_files"] = files
    request = scaffold / "REQUEST.md"
    rep.check("REQUEST.md names this style", request.is_file() and
              f"`{style_id}`" in request.read_text(encoding="utf-8"))
    index = scaffold / "html-canvas" / "index.html"
    if not rep.passed:
        return finish(result, rep, started)
    try:
        result["film_html_sha256"] = customise(index, words)
        rep.check("starter retitled from STYLE.json (anchor found, fonts offline)", True)
    except (OSError, ValueError) as exc:
        rep.check("starter retitled from STYLE.json (anchor found, fonts offline)", False, str(exc))
        return finish(result, rep, started)

    try:
        out = render_frames(index, work, size, TIMES, rep)
    except OSError as exc:
        rep.check("frame helper exited 0 and wrote every frame", False, str(exc)[:300])
        out = None
    if out is None:
        return finish(result, rep, started)
    result["playwright"] = out.get("playwright")
    result["blocked_requests"] = out.get("blocked_requests", [])
    frames = frame_checks(out, size, rep, expect)
    thumbs = work / "thumbs"
    thumbs.mkdir()
    for row in frames[:2]:
        row["thumbnail"] = thumbnail(Path(row["png"]), thumbs / (Path(row["png"]).stem + ".png"))
    if not keep_frames:
        for row in frames:
            Path(row["png"]).unlink(missing_ok=True)
            row["png_kept"] = False
    result["frames"] = frames
    return finish(result, rep, started)


def finish(result: dict, rep: Report, started: float) -> dict:
    result["commands"] = rep.commands
    result["checks"] = rep.checks
    result["failed_checks"] = rep.failed()
    result["passed"] = rep.passed
    result["seconds"] = round(time.monotonic() - started, 3)
    return result


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("style_id")
    ap.add_argument("artifact")
    ap.add_argument("--task", default="")
    ap.add_argument("--keep-frames", action="store_true", help="keep the full-size PNG frames")
    args = ap.parse_args(argv)
    artifact = Path(args.artifact).resolve()
    artifact.parent.mkdir(parents=True, exist_ok=True)
    result = run(args.style_id, artifact, args.task, args.keep_frames)
    artifact.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"style": args.style_id, "passed": result["passed"], "failed_checks": result["failed_checks"],
                      "seconds": result["seconds"], "artifact": str(artifact)}, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
