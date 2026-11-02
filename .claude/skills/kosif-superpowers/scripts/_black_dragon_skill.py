#!/usr/bin/env python3
"""Black Dragon skill adapters: run the program that ships inside a skill, and check it.

Usage: _black_dragon_skill.py RECIPE ARTIFACT --task=TEXT [--media=FILE]

Most skills are written methods with no code, and they stay "method
descriptions". A few skills ship a real script; each recipe here runs that
script on the task (or on --media, or on the known-answer self-test clip from
_black_dragon_media.py), keeps every output inside ARTIFACT's .work folder and
checks the result. Exit 0 only when the script ran and every required check
passed. Scripts run with `python3 -I`, no shell, no network.
"""
from __future__ import annotations
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

import _black_dragon_media as media

SCRIPTS = Path(__file__).resolve().parent
SKILLS = SCRIPTS.parents[1]           # .claude/skills
VENDOR = SCRIPTS.parent / "vendor" / "100-superskills" / "skills"
SCHEMA = "kosif.black-dragon.skill-adapter.v1"
PY = [sys.executable, "-I"]

SCRIPT = {
    "prompt-master": VENDOR / "prompt-master-pro" / "scripts",
    "prompt-architect": VENDOR / "prompt-architect-reasoning-models" / "scripts",
    "reel-hooks": SKILLS / "kosif-reel-hooks" / "scripts",
    "excel-lambdas": VENDOR / "excel-automation-power" / "scripts",
    "social": VENDOR / "kosif-social" / "scripts",
    "video-editor": VENDOR / "pro-video-editor-ffmpeg" / "scripts",
    "motion-energy": VENDOR / "motion-director-pro" / "scripts",
}
RECIPES = tuple(SCRIPT)
NEEDS_MEDIA = {"social", "video-editor", "motion-energy"}
NEEDS_MODULE = {"excel-lambdas": "openpyxl", "motion-energy": "PIL"}  # Python packages a recipe's script imports


def _json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def prompt_master(r, d, task, clip, selftest):
    brief = r.work / "brief.json"
    brief.write_text(json.dumps({
        "role": "KOSIF video editor", "context": task, "task": [task], "language": "العربية",
        "output_format": "خطة مونتاج مرقّمة: لقطة، توقيت، انتقال، نص على الشاشة",
        "quality_bar": ["كل انتقال على ضربة", "النص العربي مقروء"], "constraints": ["لا تخترع مصادر"],
    }, ensure_ascii=False), encoding="utf-8")
    prompt = r.work / "prompt-v1.md"
    r.call("prompt_build", [*PY, str(d / "prompt_build.py"), str(brief), "--out", str(prompt)])
    for name in ("prompt-v1.md", "prompt-v1-tests.md", "prompt-v1-variants.md", "prompt-v1-blindspots.md"):
        r.output(r.work / name)
    # exit 1 = REVISE, 3 = BLOCK: the linter's verdict on the prompt, not a broken tool.
    step = r.call("prompt_lint", [*PY, str(d / "prompt_lint.py"), str(prompt), "--json"], ok_codes=(0, 1, 3))
    lint = step.get("receipt") or {}
    r.check("prompt linted with a verdict", lint.get("verdict") in ("PASS", "REVISE", "BLOCK"), lint.get("verdict"))
    r.check("task text is inside the built prompt", task in prompt.read_text(encoding="utf-8"), len(task))
    r.findings.append({"lint_verdict": lint.get("verdict"), "lint_score": lint.get("score"),
                       "issues": [i.get("code") for i in lint.get("issues", [])]})


def prompt_architect(r, d, task, clip, selftest):
    text = r.work / "task.txt"
    text.write_text(task, encoding="utf-8")
    # The suite WRITES 20 attack cases for testing a model; it does not test one by itself.
    suite = r.call("injection_shield suite (writes 20 attack test cases)", [*PY, str(d / "injection_shield.py"), "suite"])
    cases = (suite.get("receipt") or {}).get("cases")
    r.output(r.work / "attacks.jsonl")
    r.check("attack test set has its 20 cases", cases == 20, cases)
    step = r.call("prompt_frontier on the task", [*PY, str(d / "prompt_frontier.py"), str(text), "--json"])
    r.check("frontier analysis returned", isinstance(step.get("receipt"), dict), type(step.get("receipt")).__name__)
    r.findings.append({"frontier_keys": sorted((step.get("receipt") or {}).keys())[:12]})


def reel_hooks(r, d, task, clip, selftest):
    text = r.work / "hook.txt"
    text.write_text(task, encoding="utf-8")
    step = r.call("reel_tools hook (score the task as an opening hook)",
                  [*PY, str(d / "reel_tools.py"), "hook", str(text), "--json"])
    rows = step.get("receipt") or []
    r.check("hook scored", bool(rows) and isinstance(rows[0].get("score"), (int, float)), rows[0].get("score") if rows else None)
    if rows:
        r.findings.append({"score": rows[0].get("score"), "verdict": rows[0].get("verdict"),
                           "weakest": rows[0].get("weakest")})


def excel_lambdas(r, d, task, clip, selftest):
    out = r.work / "lambdas.xlsx"
    step = r.call("lambda_library (named LAMBDA workbook)", [*PY, str(d / "lambda_library.py"), "--out", str(out)])
    r.output(out)
    funcs = (step.get("receipt") or {}).get("functions") or []
    r.check("workbook defines LAMBDA functions", len(funcs) >= 10, len(funcs))
    r.check("output is a real xlsx (zip) file", out.is_file() and out.read_bytes()[:2] == b"PK", None)


def social(r, d, task, clip, selftest):
    pack = r.work / "pack.json"
    r.call("social limits", [*PY, str(d / "social.py"), "limits"])
    r.call("social pack (post-pack skeleton from the video)",
           [*PY, str(d / "social.py"), "pack", str(clip), "--platforms", "tiktok,reels,shorts", "--out", str(pack)])
    r.output(pack)
    data = _json(pack)
    r.check("pack has the three platforms", set(data.get("posts", {})) >= {"tiktok", "reels", "shorts"},
            sorted(data.get("posts", {})))
    r.check("pack measured the video", bool((data.get("probe") or {}).get("seconds")), data.get("probe"))


def video_editor(r, d, task, clip, selftest):
    probe, wav, beats = r.work / "probe.json", r.work / "audio.wav", r.work / "beats.json"
    r.call("probe", [*PY, str(d / "probe.py"), str(clip), "--json", str(probe)])
    r.output(probe)
    r.call("extract WAV (ffmpeg)", ["ffmpeg", "-y", "-loglevel", "error", "-i", str(clip), "-vn", str(wav)])
    r.call("beat_cuts", [*PY, str(d / "beat_cuts.py"), str(wav), "--out", str(beats)])
    r.output(beats)
    data = _json(beats)
    r.findings.append({"bpm": data.get("bpm"), "beats": len(data.get("beats_s") or []),
                       "cut_points_s": (data.get("cut_points_s") or [])[:8]})
    if selftest:
        bpm = data.get("bpm")
        r.check(f"self-test tempo near {media.SELF_TEST['bpm']} BPM (±3)",
                isinstance(bpm, (int, float)) and abs(bpm - media.SELF_TEST["bpm"]) <= 3, bpm)


def motion_energy(r, d, task, clip, selftest):
    out = r.work / "motion_energy.json"
    r.call("motion_energy", [*PY, str(d / "motion_energy.py"), str(clip), "--out", str(out)])
    r.output(out)
    build = _json(out).get("build") or {}
    r.check("motion measured per frame", (build.get("frames") or 0) > 0, build.get("frames"))
    r.findings.append({k: build.get(k) for k in ("mean", "peak", "near_still_share", "longest_still_s")})
    if selftest:
        r.check("self-test clip (shaking camera) is never still", (build.get("near_still_share") or 0) < 0.1,
                build.get("near_still_share"))


RUNNERS = {"prompt-master": prompt_master, "prompt-architect": prompt_architect, "reel-hooks": reel_hooks,
           "excel-lambdas": excel_lambdas, "social": social, "video-editor": video_editor,
           "motion-energy": motion_energy}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("recipe", choices=RECIPES)
    ap.add_argument("artifact", type=Path)
    ap.add_argument("--task", default="")
    ap.add_argument("--media", default="")
    a = ap.parse_args(argv)
    artifact = a.artifact.resolve()
    work = artifact.with_name(artifact.stem + ".work")
    work.mkdir(parents=True, exist_ok=False)
    r = media.Run(a.recipe, work)
    report = {"schema": SCHEMA, "recipe": a.recipe, "skill_scripts": str(SCRIPT[a.recipe]), "task": a.task}
    try:
        if not a.task.strip():
            raise RuntimeError("task text is required")
        clip, selftest = None, False
        if a.recipe in NEEDS_MEDIA:
            if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
                raise RuntimeError("ffmpeg and ffprobe are required")
            if a.media:
                clip = Path(a.media).expanduser().resolve()
                if not clip.is_file():
                    raise RuntimeError(f"media not found: {clip}")
                report["input"] = {"kind": "user-media", "path": str(clip), "sha256": media.sha256(clip)}
            else:
                clip, selftest = media.self_test_clip(work), True
                report["input"] = {"kind": "self-test", "path": str(clip), "sha256": media.sha256(clip),
                                   "known_answers": media.SELF_TEST,
                                   "note": "generated test clip with known answers, NOT your footage"}
        RUNNERS[a.recipe](r, SCRIPT[a.recipe], a.task, clip, selftest)
        error = None
    except (RuntimeError, OSError, ValueError, KeyError, IndexError, subprocess.SubprocessError,
            json.JSONDecodeError) as exc:
        error = str(exc)[:500]
    passed = error is None and bool(r.checks) and all(c["pass"] for c in r.checks)
    report.update(steps=r.steps, outputs=r.outputs, checks=r.checks, findings=r.findings,
                  error=error, verdict="passed" if passed else "failed")
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
