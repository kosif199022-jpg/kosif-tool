#!/usr/bin/env python3
"""Run one superpower for real: execute every member power's real runner, in pipeline order.

Usage: superpower_run.py ARTIFACT SUPERPOWER_ID TASK [--step-timeout SECONDS]

A superpower in data/superpowers.json is a pipeline of power IDs. This runner executes each
member's *real* runner (a reviewed adapter, or a generated proof/style runner), never the method
applier. Every step writes its own artifact, hashed with SHA-256, into ARTIFACT's sibling folder
``<artifact stem>.steps/``. ARTIFACT is a JSON summary of every step.

Exit 0 only when every member has a real runner and every step passed with a non-empty output
("executed"). Otherwise the summary is still written, with the verdict "partial" or "none",
and the exit code is 3, so the Black Dragon records the superpower as failed instead of executed.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _mind_vocab as V  # noqa: E402

REPO = HERE.parents[3]
SUPERPOWERS = REPO / ".claude/skills/kosif-superpowers/data/superpowers.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_superpowers() -> dict:
    raw = json.loads(SUPERPOWERS.read_text(encoding="utf-8"))
    return {sp["id"]: sp for sp in raw["items"]}


def real_runners() -> dict:
    """Reviewed and generated runners, without any method applier or superpower chain."""
    import dragon_mind as dm
    bd, _ = dm._dragon()
    out = {}
    for key, spec in dm.reviewed_adapters(bd).items():
        if spec.get("method_applier") or spec.get("script") in (V.APPLIER_SCRIPT, V.SUPERPOWER_SCRIPT):
            continue
        out[key] = spec
    return out


def coverage(sp: dict, runners: dict) -> tuple[list, list]:
    members = ["power:" + step["id"] for step in sp["pipeline"]]
    return [m for m in members if m in runners], [m for m in members if m not in runners]


def run_step(key: str, spec: dict, task: str, steps_dir: Path, timeout: int) -> dict:
    import dragon_mind as dm
    bd, _ = dm._dragon()
    name = re.sub(r"[^a-zA-Z0-9_.-]", "_", key)[:80]
    artifact = steps_dir / (name + ".txt")
    try:
        script = bd._safe_script(spec["script"])
    except (ValueError, KeyError) as exc:
        return {"entry": key, "status": "failed", "reason": str(exc)[:200]}
    args = [a.replace("{task}", task).replace("{artifact}", str(artifact)) for a in spec.get("args", [])]
    command = [sys.executable, str(script), *args]
    try:
        done = subprocess.run(command, cwd=REPO, text=True, capture_output=True, timeout=timeout,
                              check=False, stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        return {"entry": key, "status": "failed", "reason": "timeout after %ds" % timeout}
    if done.returncode or not artifact.is_file() or artifact.stat().st_size == 0:
        return {"entry": key, "status": "failed", "exit_code": done.returncode,
                "reason": (done.stderr or "missing or empty output")[-200:]}
    return {"entry": key, "status": "executed", "exit_code": 0, "artifact": str(artifact),
            "artifact_sha256": sha(artifact)}


def execute(artifact: Path, sp_id: str, task: str, step_timeout: int = 120, runners: dict | None = None) -> int:
    sps = load_superpowers()
    if sp_id.startswith("superpower:"):
        sp_id = sp_id.split(":", 1)[1]
    if sp_id not in sps:
        print("unknown superpower: %s" % sp_id, file=sys.stderr)
        return 3
    sp = sps[sp_id]
    runners = real_runners() if runners is None else runners
    covered, missing = coverage(sp, runners)
    steps_dir = artifact.parent / (artifact.stem + ".steps")
    steps_dir.mkdir(parents=True, exist_ok=True)
    steps = [run_step(key, runners[key], task, steps_dir, step_timeout) for key in covered]
    passed = sum(s["status"] == "executed" for s in steps)
    total = len(sp["pipeline"])
    verdict = "executed" if total and passed == total else ("partial" if passed else "none")
    summary = {"superpower": "superpower:" + sp_id, "name_en": sp.get("name_en"), "task": task,
               "verdict": verdict, "members": total, "members_with_real_runner": len(covered),
               "members_executed": passed, "members_without_runner": missing, "steps": steps,
               "rule": "executed only when every member power ran its own real runner with a hashed output"}
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if verdict == "executed" else 3


def registry(runners: dict | None = None) -> tuple[dict, dict]:
    """Chain adapters for the superpowers whose every member has a real runner, plus counts."""
    runners = real_runners() if runners is None else runners
    adapters, counts = {}, {"full": 0, "partial": 0, "none": 0}
    for sp_id, sp in sorted(load_superpowers().items()):
        covered, missing = coverage(sp, runners)
        if not missing:
            counts["full"] += 1
            adapters["superpower:" + sp_id] = {
                "script": V.SUPERPOWER_SCRIPT, "args": ["{artifact}", sp_id, "{task}"],
                "why": "superpower chain: runs all %d member powers' real runners in order" % len(covered)}
        else:
            counts["partial" if covered else "none"] += 1
    return adapters, counts


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    timeout = 120
    if "--step-timeout" in argv:
        i = argv.index("--step-timeout")
        timeout = int(argv[i + 1])
        del argv[i:i + 2]
    if len(argv) != 3:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    return execute(Path(argv[0]), argv[1], argv[2], timeout)


if __name__ == "__main__":
    sys.exit(main())
