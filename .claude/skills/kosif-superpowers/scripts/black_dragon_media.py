#!/usr/bin/env python3
"""Real, opt-in Black Dragon media workflow. No catalog-wide execution claims.

Run from the repository checkout:
  python3 .claude/skills/kosif-superpowers/scripts/black_dragon_media.py doctor
  python3 .claude/skills/kosif-superpowers/scripts/black_dragon_media.py run --input clip.mp4 --job-name my-film --execute --stabilize --reframe
  python3 .claude/skills/kosif-superpowers/scripts/black_dragon_media.py verify --job-name my-film

A job uses already-bundled montage_pro, audio_cue_mapper, music_rhythm_engine
and cinema_lab, creates actual artifacts, then hashes them. No network, model
downloads, paid providers, implicit transcript, or silently executed options.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
JOBS = REPO / "out" / "black-dragon-media"
SCHEMA = "kosif.black-dragon.media.v1"
TOOLS = {
    "montage": "montage_pro.py",
    "cues": "audio_cue_mapper.py",
    "rhythm": "music_rhythm_engine.py",
    "cinema": "cinema_lab.py",
}

def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def job_path(name: str) -> Path:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,47}", name):
        raise ValueError("job name must be 1-48 ASCII letters/digits/_/-")
    return JOBS / name

def existing_file(path: Path) -> Path:
    if path.is_symlink() or not path.is_file():
        raise ValueError("input must be an existing regular file, not a symlink")
    return path.resolve()

def artifact_proof(job: Path, path: Path) -> dict:
    resolved = path.resolve()
    if not resolved.is_relative_to(job.resolve()) or path.is_symlink() or not path.is_file():
        raise ValueError("missing, symlinked or external stage output")
    if not path.stat().st_size:
        raise ValueError("empty output is not execution evidence")
    return {"path": str(path.relative_to(job)), "bytes": path.stat().st_size, "sha256": digest(path)}

def _run_stage(report: dict, job: Path, name: str, argv: list[str],
               outputs: list[Path], timeout: int) -> None:
    stage = {"name": name, "status": "failed", "command": argv}
    report["stages"].append(stage)
    try:
        result = subprocess.run(argv, cwd=REPO, text=True, capture_output=True,
                                stdin=subprocess.DEVNULL, timeout=timeout, check=False)
        stage["exit_code"] = result.returncode
        stage["stdout_tail"] = result.stdout[-500:]
        if result.returncode:
            raise RuntimeError(f"{name} exited {result.returncode}: {result.stderr[-450:]}")
        stage["artifacts"] = [artifact_proof(job, p) for p in outputs]
        stage["status"] = "executed"
    except (OSError, ValueError, subprocess.TimeoutExpired, RuntimeError) as exc:
        stage["error"] = str(exc)[:600]
        raise RuntimeError(f"{name}: {exc}") from exc

def _save(job: Path, report: dict) -> None:
    (job / "black_dragon_media_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def doctor() -> dict:
    return {
        "schema": SCHEMA + ".doctor",
        "ffmpeg": bool(shutil.which("ffmpeg")),
        "ffprobe": bool(shutil.which("ffprobe")),
        "scripts": {name: (HERE / path).is_file() for name, path in TOOLS.items()},
        "notes": "Read-only presence check; only a successful run + verified artifacts proves execution.",
    }

def run(args: argparse.Namespace) -> tuple[int, dict]:
    media = existing_file(args.input)
    words = existing_file(args.aligned_words) if args.aligned_words else None
    job = job_path(args.job_name)
    if not args.execute:
        raise ValueError("explicit --execute required before reading media or creating a job")
    available = doctor()
    if not available["ffmpeg"] or not available["ffprobe"] or not all(available["scripts"].values()):
        raise ValueError("ffmpeg, ffprobe and all four bundled media scripts are required; run doctor")
    if job.exists() or job.is_symlink():
        raise ValueError("job already exists; choose a new --job-name")
    job.parent.mkdir(parents=True, exist_ok=True)
    job.mkdir(exist_ok=False)
    (job / "work").mkdir()
    (job / "exports").mkdir()
    report = {
        "schema": SCHEMA, "status": "running",
        "source": {"path": str(media), "sha256": digest(media)},
        "analysis_scope": "original media (rhythm limited to first 120 seconds if necessary)",
        "stages": [], "verified_artifact_count": 0,
        "catalog_coverage_claim": False,
        "transcription": "not attempted (no model downloads)",
        "paid_provider_calls": 0,
    }
    py = sys.executable
    try:
        if words:
            dst = job / "words.json"
            shutil.copyfile(words, dst)
            report["imported_aligned_words"] = artifact_proof(job, dst)
        intake = job / "intake"
        _run_stage(report, job, "montage-intake",
                   [py, str(HERE / TOOLS["montage"]), "intake", str(media), "--job", str(intake)],
                   [intake / "intake.json"], args.timeout)
        obj = json.loads((intake / "intake.json").read_text(encoding="utf-8"))
        kind = obj.get("kind")
        report["media_kind"] = kind
        if kind not in ("audio", "video"):
            raise RuntimeError("unsupported media: ffprobe found no usable audio or video streams")
        if words:
            # The import is explicit and must be recognized by the cue mapper.
            shutil.copyfile(job / "words.json", intake / "words.json")
        if obj.get("probe", {}).get("audio"):
            cues = intake / "work" / "cues.json"
            if not cues.is_file():
                # audio_cue_mapper deliberately limits analysis to 120 seconds.
                # Analyze only an excerpt rather than claiming full-track rhythm.
                excerpt = job / "work" / "rhythm_excerpt.wav"
                _run_stage(report, job, "rhythm-excerpt",
                           ["ffmpeg", "-nostdin", "-v", "error", "-n", "-i", str(media),
                            "-t", "120", "-vn", "-ac", "1", "-ar", "44100", "-c:a", "pcm_s16le", str(excerpt)],
                           [excerpt], args.timeout)
                cues = job / "work" / "cues.json"
                _run_stage(report, job, "measured-audio-cues",
                           [py, str(HERE / TOOLS["cues"]), str(excerpt), "--out", str(cues)],
                           [cues], args.timeout)
                report["rhythm_input_scope"] = "first 120 seconds, not entire media"
            else:
                report["rhythm_input_scope"] = "full audio (up to 120 seconds)"
                report["stages"].append({"name": "measured-audio-cues", "status": "executed",
                                         "artifacts": [artifact_proof(job, cues)],
                                         "provenance": "montage-intake invoked bundled audio_cue_mapper"})
            rhythm = job / "rhythm.json"
            _run_stage(report, job, "rhythm-estimate",
                       [py, str(HERE / TOOLS["rhythm"]), str(cues), "--out", str(rhythm)],
                       [rhythm], args.timeout)
        else:
            report["stages"].append({"name": "rhythm-estimate", "status": "skipped",
                                     "reason": "media has no audio stream"})
        if kind == "video" and not args.skip_scenes:
            scene = job / "scenes" / "scenes.json"
            _run_stage(report, job, "scene-analysis",
                       [py, str(HERE / TOOLS["cinema"]), "scenes",
                        "--input", str(media), "--out", str(job / "scenes"), "--engine", "ffmpeg"],
                       [scene], args.timeout)
        source = media
        changes = [("stabilize", args.stabilize), ("reframe", args.reframe),
                   ("grade", bool(args.grade_look))]
        if kind != "video" and any(enabled for _, enabled in changes):
            raise ValueError("stabilize, reframe and grade require a video input")
        for operation, enabled in changes:
            if not enabled:
                continue
            output = job / "exports" / (operation + ".mp4")
            argv = [py, str(HERE / TOOLS["cinema"]), operation,
                    "--input", str(source), "--output", str(output)]
            if operation == "grade":
                argv += ["--look", args.grade_look]
            _run_stage(report, job, "video-" + operation, argv, [output], args.timeout)
            source = output
        report["final_video"] = str(source.relative_to(job)) if source != media else None
        report["verified_artifact_count"] = sum(len(s.get("artifacts", [])) for s in report["stages"])
        report["status"] = "completed"
        _save(job, report)
        return 0, report
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        report["status"] = "failed"
        report["error"] = str(exc)[:600]
        _save(job, report)
        return 4, report

def verify(name: str) -> dict:
    job = job_path(name)
    path = job / "black_dragon_media_report.json"
    if path.is_symlink() or not path.is_file():
        raise ValueError("job report missing")
    report = json.loads(path.read_text(encoding="utf-8"))
    if report.get("schema") != SCHEMA or report.get("status") != "completed":
        raise ValueError("incomplete or malformed run")
    checked = 0
    for stage in report.get("stages", []):
        if stage.get("status") == "skipped":
            continue
        if stage.get("status") != "executed" or not stage.get("artifacts"):
            raise ValueError("unverified execution stage")
        for obj in stage["artifacts"]:
            rel = Path(obj["path"])
            if rel.is_absolute() or ".." in rel.parts:
                raise ValueError("unsafe output reference")
            output = job / rel
            if artifact_proof(job, output) != obj:
                raise ValueError("artifact changed: " + str(rel))
            checked += 1
    if not checked or report.get("verified_artifact_count") != checked:
        raise ValueError("artifact count mismatch")
    return {"status": "verified", "job": str(job), "verified_artifacts": checked,
            "whole_catalog_executed": False, "report_sha256": digest(path)}

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor", help="read-only prerequisite check")
    p = sub.add_parser("run", help="opt-in real asset-processing pipeline")
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--job-name", required=True)
    p.add_argument("--aligned-words", type=Path, help="optional pre-aligned words.json; no transcription")
    p.add_argument("--execute", action="store_true", help="explicitly allow local media processing")
    p.add_argument("--skip-scenes", action="store_true")
    p.add_argument("--stabilize", action="store_true")
    p.add_argument("--reframe", action="store_true")
    p.add_argument("--grade-look", help="named cinematic look, for example teal-orange")
    p.add_argument("--timeout", type=int, default=1800)
    v = sub.add_parser("verify", help="independently check output file hashes")
    v.add_argument("--job-name", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "doctor":
            print(json.dumps(doctor(), ensure_ascii=False, indent=2))
            return 0
        if args.command == "verify":
            print(json.dumps(verify(args.job_name), ensure_ascii=False, indent=2))
            return 0
        if not 30 <= args.timeout <= 3600:
            raise ValueError("timeout must be 30-3600 seconds")
        if args.grade_look and not re.fullmatch(r"[a-z0-9-]{1,40}", args.grade_look):
            raise ValueError("invalid grade look")
        status, report = run(args)
        print(json.dumps({"status": report["status"], "job": str(job_path(args.job_name)),
                          "artifacts": report["verified_artifact_count"],
                          "error": report.get("error")}, ensure_ascii=False, indent=2))
        return status
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print("black-dragon-media: " + str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
