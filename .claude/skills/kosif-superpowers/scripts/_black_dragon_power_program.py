#!/usr/bin/env python3
"""Black Dragon adapter: run the real program written for one power card and check its known answers.

Usage: _black_dragon_power_program.py POWER_ID ARTIFACT [--task=TEXT]

The program lives in power_programs/<family>.py (PROGRAMS[POWER_ID]). It performs the card's
technique on a fixture it builds in ARTIFACT's .work folder and returns checks. Exit 0 only when
the program wrote at least one non-empty output file, returned at least one check, and every
check passed. The artifact JSON records the card's sha256, the program file's sha256, every
output's sha256 and every check with its observed value. It does not run the technique on the
user's task text: the mode field says so.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import shutil
import sys
import time
import traceback
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))
import power_programs as pp  # noqa: E402

SCHEMA = "kosif.black-dragon.power-program-adapter.v1"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run_program(pid: str, work: Path) -> dict:
    cards = pp.card_index()
    if pid not in cards:
        return {"ok": False, "error": f"unknown power id: {pid}"}
    family, card = cards[pid]
    mod, fn = pp.program_for(family, pid)
    if fn is None:
        return {"ok": False, "refused": True, "error": f"no program written for {pid} ({family})"}
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    started = time.time()
    try:
        checks = list(fn(work))
        error = ""
    except Exception:  # the program itself failed: record it, never pass
        checks, error = [], traceback.format_exc()[-1500:]
    # Read each output once. Helpers a program starts can still be running (git's background
    # auto-maintenance in a test repo makes and deletes a lock file), so a file gone by now is skipped.
    outputs = []
    for p in sorted(work.rglob("*")):
        try:
            if p.is_file():
                data = p.read_bytes()
                outputs.append((p, len(data), sha(data)))
        except FileNotFoundError:
            continue
    rows = [{"name": str(n), "passed": bool(ok), "observed": str(obs)[:400]} for n, ok, obs in checks]
    problems = []
    if error:
        problems.append("program raised")
    if not rows:
        problems.append("no checks returned")
    if not any(size for _, size, _ in outputs):
        problems.append("no non-empty output file")
    problems += [f"check failed: {r['name']}" for r in rows if not r["passed"]]
    mod_file = Path(mod.__file__)
    return {"ok": not problems, "power": pid, "family": family,
            "card_sha256": sha(json.dumps(card, ensure_ascii=False, sort_keys=True).encode()),
            "program": str(mod_file.relative_to(SCRIPTS.parents[3])), "program_sha256": sha(mod_file.read_bytes()),
            "function": fn.__name__, "seconds": round(time.time() - started, 3),
            "outputs": [{"path": p.name if p.parent == work else str(p.relative_to(work)),
                         "bytes": size, "sha256": digest} for p, size, digest in outputs][:50],
            "checks": rows, "problems": problems, "error": error}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("power_id")
    ap.add_argument("artifact")
    ap.add_argument("--task", default="")
    a = ap.parse_args(argv)
    artifact = Path(a.artifact)
    artifact.parent.mkdir(parents=True, exist_ok=True)
    result = run_program(a.power_id, artifact.with_suffix(".work"))
    if result.get("refused"):
        print(result["error"], file=sys.stderr)
        return 2
    result.update({"schema": SCHEMA, "task": a.task,
                   "mode": "the card's technique performed on a self-built fixture with known answers; not run on the task text"})
    if not result["ok"]:
        print("; ".join(result.get("problems") or [result.get("error", "failed")]), file=sys.stderr)
        return 1
    artifact.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
