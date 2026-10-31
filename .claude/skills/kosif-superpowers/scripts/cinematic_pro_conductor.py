#!/usr/bin/env python3
"""Single entry point for KOSIF Cinema Pro. No downloads or paid calls.

doctor: local tools and skill inventory (presence != execution).
plan --kind audio|video: roles, stages, gates, no claims of work.
run MEDIA --job OUT_DIR [--option kinetic-film] [--style cinematic]:
  local intake -> options -> render -> mandatory independent verification.
Run writes a truthful receipt and returns nonzero unless an MP4 was verified.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
import montage_pro as m
import cinema_all_skills as full_skills

SKILL = Path(__file__).resolve().parent.parent
REPO = SKILL.parents[2]
STAGES = [
    ["source", "Check source integrity, rights, audio/video and duration"],
    ["direction", "Storyboard, tone, captions, rhythm and selected tools"],
    ["edit", "Actual renderer on a supported option, not a proposed pipeline"],
    ["quality", "Independent verification, original hash and visual review"],
]
EXTRAS = {
    "story": "script_storyboard.py",
    "see_pro": "see_superpower_unifier.py",
    "music": "music_rhythm_engine.py",
    "arabic_captions": "caption_lines.py",
    "timing": "audio_cue_mapper.py",
    "broll": "cinematic_cut_planner.py",
    "motion": "motion_director.py",
    "3d": "native_3d.py",
    "quality": "verify_video.py",
}
DEFAULTS = {"audio": "kinetic-film", "video": "highlight-reel"}


def doctor():
    return {"schema": "kosif.cinema-pro.doctor.v1",
            "installed_skills": sorted(p.parent.name for p in (REPO / ".claude/skills").glob("*/SKILL.md")),
            "optional_modules": {k: {"file": v, "installed": (SKILL / "scripts" / v).is_file(),
                                     "executed": False} for k, v in EXTRAS.items()},
            "environment": m.doctor(),
            "truth": "Module presence and an option menu do not prove an edit was rendered."}


def plan(kind, option=None, recipe="single"):
    if kind not in DEFAULTS:
        raise ValueError("Expected kind audio or video")
    recipes = {
        "single": None,
        "cinematic-reel": ("video", ["highlight-reel", "reframe", "look"]),
        "cinematic-audio": ("audio", ["kinetic-film", "look"]),
    }
    if recipe not in recipes:
        raise ValueError("Unknown recipe")
    config = recipes[recipe]
    if config and kind != config[0]:
        raise ValueError("Recipe incompatible with source kind")
    chosen = (config[1][0] if config else (option or DEFAULTS[kind]))
    if config and option and option != chosen:
        raise ValueError("Recipe fixes the initial option; do not override it")
    item = next((x for x in m.OPTIONS if x["id"] == chosen and kind in x["for"]), None)
    if item is None:
        raise ValueError("Unsupported option for this media kind")
    chain = list(config[1]) if config else [chosen]
    roles = m.team()["roles"]
    return {"schema": "kosif.cinema-pro.plan.v2", "kind": kind, "option": chosen,
            "recipe": recipe, "render_chain": chain,
            "team": [{"role": x["id"], "mission": x["mission"], "state": "candidate"}
                     for x in roles],
            "chosen_roles": item["team"], "pipeline": item["pipeline"],
            "readiness": "runnable" if item["runs"] else "needs-other-inputs",
            "stages": [{"name": x, "acceptance": y} for x, y in STAGES],
            "policies": ["No paid APIs or unattended download", "No invented transcript",
                         "Each pass's actual source and MP4 are checked before the next pass",
                         "Original source SHA-256 must be unchanged",
                         "Do not call a plan or Remotion project a finished MP4",
                         "Run verified checks before claiming delivery"]}

def safe_output(job):
    dst = job.resolve()
    if dst == SKILL or SKILL in dst.parents:
        raise ValueError("Output may not overwrite installed Superpowers")
    out = REPO / "out"
    if dst == REPO or (REPO in dst.parents and dst != out and out not in dst.parents):
        raise ValueError("Repository outputs must be under the git-ignored out/ directory")
    if any(x.is_symlink() for x in (job, *job.parents)):
        raise ValueError("Symlinked job paths are not allowed")


def gate(result, source, source_sha):
    if result.get("status") != "rendered":
        return {"passed": False, "reason": "build state is " + str(result.get("status"))}
    video = Path(result.get("output") or "/nonexistent")
    if not video.is_file() or video.suffix.lower() != ".mp4" or video.stat().st_size == 0:
        return {"passed": False, "reason": "No nonempty MP4 output"}
    verification = result.get("verify")
    if not isinstance(verification, dict) or verification.get("exit") != 0:
        return {"passed": False, "reason": "MP4 verification failed or absent"}
    if result.get("master_unchanged") is not True or m.sha256(source) != source_sha:
        return {"passed": False, "reason": "Source changed since intake"}
    mix = result.get("delivery_mix")
    if isinstance(mix, dict) and (mix.get("status") == "failed" or
                                  (mix.get("verify") is not None and mix["verify"].get("exit") != 0)):
        return {"passed": False, "reason": "Extra audio mix not verified"}
    return {"passed": True, "output": str(video), "video_verification": verification}


def run(media, job, option=None, style=None, title="", recipe="single", transcribe_local=False, require_all_skills=False):
    safe_output(job)
    media = media.resolve()
    if not media.is_file():
        raise ValueError("Source media not found")
    info = m.probe(media)
    kind = "video" if info["video"] else ("audio" if info["audio"] else None)
    if kind is None:
        raise ValueError("Not an audio or video source")
    plan_doc = plan(kind, option, recipe)
    chosen = plan_doc["option"]
    if chosen == "reference-remix":
        raise ValueError("This creates a Remotion project, not a verified MP4; use montage_pro.py directly")
    if plan_doc["readiness"] != "runnable":
        raise ValueError("Option needs extra assets; cannot one-shot render it")
    chain = plan_doc["render_chain"]
    catalog = {o["id"]: o for o in m.OPTIONS}
    tools = m.doctor()["tools"]
    missing = sorted({tool for step in chain for tool in catalog[step]["needs"]
                      if not tools.get(tool, {}).get("present")})
    if missing:
        raise ValueError("Missing tools: " + ", ".join(missing))
    if transcribe_local and not info["audio"]:
        raise ValueError("No source audio for local transcription")
    sha = m.sha256(media)
    job.mkdir(parents=True, exist_ok=True)
    if require_all_skills:
        all_catalog = full_skills.catalog()
        coverage_job = job / "full-skills"
        if not (coverage_job / "all_skills_ledger.json").exists():
            full_skills.init(coverage_job, all_catalog)
    receipt = {"schema": "kosif.cinema-pro.receipt.v2", "plan": plan_doc,
               "source_sha256": sha, "executed": [], "status": "failed", "passes": []}
    try:
        current = media
        for index, step in enumerate(chain):
            stage_job = job if index == 0 else job / "passes" / ("%02d-" % (index + 1) + step)
            stage_sha = m.sha256(current)
            transcript_options = ({"model": "medium", "language": "ar", "local_only": True}
                                  if index == 0 and transcribe_local else None)
            intake = m.intake(current, stage_job, transcript_options)
            receipt["executed"].append({"stage": "intake", "pass": index + 1, "kind": intake["kind"]})
            if transcript_options and not (intake.get("transcribe") or {}).get("ok"):
                raise ValueError("Cached-model transcription failed; not using invented captions")
            menu = m.options(stage_job, title if index == 0 else "")
            receipt["executed"].append({"stage": "options", "pass": index + 1,
                                        "count": len(menu["menu"])})
            if recipe == "cinematic-reel":
                stage_style = (style if style in ("15", "30", "60") else "30") if index == 0 else (
                    "9:16" if step == "reframe" else "film")
            elif recipe == "cinematic-audio":
                stage_style = (style or "cinematic") if index == 0 else "film"
            else:
                stage_style = style
            result = m.build(stage_job, step, stage_style, title if index == 0 else "")
            verified = gate(result, current, stage_sha)
            receipt["executed"].append({"stage": "render", "pass": index + 1,
                                        "option": step, "style": stage_style,
                                        "status": result.get("status")})
            receipt["executed"].append({"stage": "verify", "pass": index + 1, **verified})
            receipt["passes"].append({"option": step, "style": stage_style,
                                      "verification": verified})
            if not verified["passed"]:
                break
            current = Path(verified["output"])
        if len(receipt["passes"]) == len(chain) and all(
                p["verification"]["passed"] for p in receipt["passes"]) and m.sha256(media) == sha:
            receipt["status"] = "verified"
            receipt["output"] = str(current)
        elif m.sha256(media) != sha:
            receipt["error"] = "Original source changed during the render passes"
    except Exception as exc:
        receipt["error"] = type(exc).__name__ + ": " + str(exc)
    if require_all_skills:
        coverage = full_skills.report(coverage_job, all_catalog)
        receipt["full_skills_coverage"] = coverage
        if not coverage["fully_executed"]:
            receipt["status"] = "coverage-incomplete"
            receipt["coverage_warning"] = ("Export may be technically verified, but every catalogued "
                                           "skill/power/tool has NOT been executed with evidence")
    m.jsave(job / "cinema_pro_receipt.json", receipt)
    return receipt

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    subs = p.add_subparsers(dest="cmd", required=True)
    subs.add_parser("doctor")
    q = subs.add_parser("plan"); q.add_argument("--kind", choices=("audio", "video"), required=True); q.add_argument("--option"); q.add_argument("--recipe", choices=("single", "cinematic-reel", "cinematic-audio"), default="single")
    q = subs.add_parser("run"); q.add_argument("media", type=Path); q.add_argument("--job", type=Path, required=True)
    q.add_argument("--option"); q.add_argument("--style"); q.add_argument("--title", default="")
    q.add_argument("--recipe", choices=("single", "cinematic-reel", "cinematic-audio"), default="single")
    q.add_argument("--transcribe-local", action="store_true", help="opt-in: cached local model only")
    q.add_argument("--require-all-skills", action="store_true", help="strict full-catalog proof gate; incomplete returns nonzero")
    a = p.parse_args(argv)
    try:
        data = doctor() if a.cmd == "doctor" else (plan(a.kind, a.option, a.recipe) if a.cmd == "plan"
                                                     else run(a.media, a.job, a.option, a.style, a.title, a.recipe,
                                                              a.transcribe_local, a.require_all_skills))
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0 if a.cmd != "run" or data["status"] == "verified" else 4
    except (OSError, ValueError) as exc:
        print("cinema-pro: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
