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


def plan(kind, option=None):
    if kind not in DEFAULTS:
        raise ValueError("Expected kind audio or video")
    chosen = option or DEFAULTS[kind]
    item = next((x for x in m.OPTIONS if x["id"] == chosen and kind in x["for"]), None)
    if item is None:
        raise ValueError("Unsupported option for this media kind")
    roles = m.team()["roles"]
    return {"schema": "kosif.cinema-pro.plan.v1", "kind": kind, "option": chosen,
            "team": [{"role": x["id"], "mission": x["mission"], "state": "candidate"}
                     for x in roles],
            "chosen_roles": item["team"], "pipeline": item["pipeline"],
            "readiness": "runnable" if item["runs"] else "needs-other-inputs",
            "stages": [{"name": x, "acceptance": y} for x, y in STAGES],
            "policies": ["No paid APIs or unattended download", "No invented transcript",
                         "Original audio retained unless source format forces conversion",
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


def run(media, job, option=None, style=None, title=""):
    safe_output(job)
    media = media.resolve()
    if not media.is_file():
        raise ValueError("Source media not found")
    info = m.probe(media)
    kind = "video" if info["video"] else ("audio" if info["audio"] else None)
    if kind is None:
        raise ValueError("Not an audio or video source")
    plan_doc = plan(kind, option)
    chosen = plan_doc["option"]
    if chosen == "reference-remix":
        raise ValueError("This creates an editable Remotion project, not a verified MP4; use montage_pro.py directly")
    if plan_doc["readiness"] != "runnable":
        raise ValueError("Option needs additional assets; cannot one-shot render it")
    target = next(x for x in m.OPTIONS if x["id"] == chosen)
    tools = m.doctor()["tools"]
    missing = [x for x in target["needs"] if not tools.get(x, {}).get("present")]
    if missing:
        raise ValueError("Missing tools: " + ", ".join(missing))
    sha = m.sha256(media)
    job.mkdir(parents=True, exist_ok=True)
    receipt = {"schema": "kosif.cinema-pro.receipt.v1", "plan": plan_doc,
               "source_sha256": sha, "executed": [], "status": "failed"}
    try:
        intake = m.intake(media, job)
        receipt["executed"].append({"stage": "intake", "kind": intake["kind"]})
        menu = m.options(job, title)
        receipt["executed"].append({"stage": "options", "count": len(menu["menu"])})
        result = m.build(job, chosen, style, title)
        verified = gate(result, media, sha)
        receipt["executed"].append({"stage": "render", "status": result.get("status")})
        receipt["executed"].append({"stage": "verify", **verified})
        receipt["status"] = "verified" if verified["passed"] else "failed"
        receipt["output"] = verified.get("output")
    except Exception as exc:
        receipt["error"] = type(exc).__name__ + ": " + str(exc)
    m.jsave(job / "cinema_pro_receipt.json", receipt)
    return receipt


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    subs = p.add_subparsers(dest="cmd", required=True)
    subs.add_parser("doctor")
    q = subs.add_parser("plan"); q.add_argument("--kind", choices=("audio", "video"), required=True); q.add_argument("--option")
    q = subs.add_parser("run"); q.add_argument("media", type=Path); q.add_argument("--job", type=Path, required=True)
    q.add_argument("--option"); q.add_argument("--style"); q.add_argument("--title", default="")
    a = p.parse_args(argv)
    try:
        data = doctor() if a.cmd == "doctor" else (plan(a.kind, a.option) if a.cmd == "plan"
                                                     else run(a.media, a.job, a.option, a.style, a.title))
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0 if a.cmd != "run" or data["status"] == "verified" else 4
    except (OSError, ValueError) as exc:
        print("cinema-pro: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
