#!/usr/bin/env python3
"""Black Dragon tool adapters: run a registered tool's own test suite against its real code, and check it.

Usage: _black_dragon_tool.py TOOL_ID ARTIFACT [--task=TEXT]

Every tool in data/tools.json names the test files that exercise it (`tests`). This adapter
runs each of those files with unittest, in a subprocess, from the repository root, and keeps
the log inside ARTIFACT's .work folder. When the tool documents a `--self-test` command, that
runs too. The tests feed the tool known inputs and check known answers, so a pass means the
tool's code ran and gave the right results here, on this machine, now.

Exit 0 only when, for every test file:
  * the file exists and mentions the tool's script (so the receipt is about THIS tool),
  * at least one test really ran (not all skipped),
  * unittest reported OK (no failure, no error);
and the self-test, when there is one, exited 0.

What this is not: it does not run the tool on the user's task (most tools need inputs a task
does not give). The artifact says so in `mode`. Tools whose record names no test file are
refused (exit 2) instead of being given an empty pass.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
SKILL = SCRIPTS.parent
REPO = SKILL.parents[2]
TOOLS = SKILL / "data" / "tools.json"
SCHEMA = "kosif.black-dragon.tool-suite-adapter.v1"
sys.path.insert(0, str(SCRIPTS))
from _black_dragon_tool_recipes import RECIPES, Ctx  # noqa: E402


class _Done(Exception):
    """A recipe finished; skip the test-suite path."""
RAN = re.compile(r"^Ran (\d+) tests? in ", re.M)
SKIPPED = re.compile(r"skipped=(\d+)")
EXPECTED_FAIL = re.compile(r"expected failures=(\d+)")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_tool(tool_id: str) -> dict:
    for row in json.loads(TOOLS.read_text(encoding="utf-8"))["tools"]:
        if row["id"] == tool_id:
            return row
    raise KeyError(f"unknown tool id: {tool_id}")


def script_path(tool: dict) -> Path:
    base = REPO if tool.get("root") == "repo" else SKILL
    return (base / tool["path"]).resolve()


def self_test_argv(tool: dict, script: Path) -> list[str] | None:
    """The tool's documented `--self-test` call, rebuilt as an argv on the real script (no shell)."""
    for cmd in tool.get("commands") or []:
        example = str(cmd.get("example") or "")
        if "--self-test" not in example or script.suffix != ".py":
            continue
        words = shlex.split(example)
        if "--self-test" not in words or any(w in ("|", ">", "&&", ";") for w in words):
            continue
        return [sys.executable, "-B", str(script), "--self-test"]
    return None


def run_suite(test: Path, work: Path, env: dict, timeout: int) -> dict:
    argv = [sys.executable, "-B", "-m", "unittest", "discover", "-s", str(test.parent), "-p", test.name, "-v"]
    done = subprocess.run(argv, cwd=REPO, env=env, text=True, capture_output=True,
                          stdin=subprocess.DEVNULL, timeout=timeout, check=False)
    log = work / f"{test.stem}.log"
    log.write_text(done.stdout + "\n--- stderr ---\n" + done.stderr, encoding="utf-8")
    text = done.stderr + done.stdout
    ran = sum(int(n) for n in RAN.findall(text))
    skipped = sum(int(n) for n in SKIPPED.findall(text))
    expected = sum(int(n) for n in EXPECTED_FAIL.findall(text))
    # unittest prints its verdict ("OK", "OK (skipped=2)", "FAILED (...)", "NO TESTS RAN") last on stderr.
    verdicts = [ln.strip() for ln in done.stderr.splitlines() if re.match(r"^(OK|FAILED|NO TESTS RAN)\b", ln.strip())]
    tail = verdicts[-1] if verdicts else "no unittest verdict"
    return {"step": f"unittest {test.relative_to(REPO)}", "command": argv, "exit_code": done.returncode,
            "ran": ran, "skipped": skipped, "expected_failures": expected,
            "result": tail[:200], "log": str(log), "log_sha256": sha256(log)}


NODE_COUNT = re.compile(r"^# (tests|pass|fail|cancelled|skipped|todo) (\d+)$", re.M)


def run_node_test(test: Path, work: Path, env: dict, timeout: int) -> dict:
    """A JavaScript test file written for the built-in `node --test` runner (TAP summary at the end)."""
    argv = ["node", "--test", str(test)]
    done = subprocess.run(argv, cwd=REPO, env=env, text=True, capture_output=True,
                          stdin=subprocess.DEVNULL, timeout=timeout, check=False)
    log = work / f"{test.stem}.log"
    log.write_text(done.stdout + "\n--- stderr ---\n" + done.stderr, encoding="utf-8")
    n = {k: int(v) for k, v in NODE_COUNT.findall(done.stdout)}
    return {"step": f"node --test {test.relative_to(REPO)}", "command": argv, "exit_code": done.returncode,
            "ran": n.get("tests", 0), "skipped": n.get("skipped", 0) + n.get("todo", 0), "expected_failures": 0,
            "result": f"pass {n.get('pass', 0)} fail {n.get('fail', 0)} cancelled {n.get('cancelled', 0)}",
            "failed": n.get("fail", 0) + n.get("cancelled", 0), "log": str(log), "log_sha256": sha256(log)}


def run_script_test(test: Path, work: Path, env: dict, timeout: int) -> dict:
    """A plain test script (no unittest): it checks its own cases and exits 0 only when all pass."""
    argv = [sys.executable, "-B", str(test)]
    done = subprocess.run(argv, cwd=REPO, env=env, text=True, capture_output=True,
                          stdin=subprocess.DEVNULL, timeout=timeout, check=False)
    log = work / f"{test.stem}.log"
    log.write_text(done.stdout + "\n--- stderr ---\n" + done.stderr, encoding="utf-8")
    return {"step": f"test script {test.relative_to(REPO)}", "command": argv, "exit_code": done.returncode,
            "lines": len([ln for ln in done.stdout.splitlines() if ln.strip()]),
            "result": (done.stdout.strip().splitlines() or [""])[-1][:200], "log": str(log), "log_sha256": sha256(log)}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tool")
    ap.add_argument("artifact", type=Path)
    ap.add_argument("--task", default="")
    ap.add_argument("--timeout", type=int, default=900)
    a = ap.parse_args(argv)
    artifact = a.artifact.resolve()
    work = artifact.with_name(artifact.stem + ".work")
    work.mkdir(parents=True, exist_ok=False)
    # Scratch files go to a fresh folder in the system temp dir, removed afterwards. Not inside the job:
    # the job usually sits in the repository's out/, and several tools rightly refuse to write private or
    # third-party files inside a git checkout, so their tests expect a temp dir outside one.
    tmp = Path(tempfile.mkdtemp(prefix="black-dragon-tool-"))
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=str(tmp), TEMP=str(tmp), TMP=str(tmp))
    report = {"schema": SCHEMA, "tool": a.tool, "mode": "own-test-suite",
              "note": "the tool's own tests ran against its real code with known inputs and answers; "
                      "it was not run on the task text"}
    steps, checks = [], []

    def check(name, ok, value=None):
        checks.append({"check": name, "pass": bool(ok), "value": value})

    code, error = 1, None
    try:
        tool = load_tool(a.tool)
        script = script_path(tool)
        report["script"] = str(script.relative_to(REPO))
        recipe = RECIPES.get(a.tool)
        if recipe is not None:
            report["mode"] = "known-answer-recipe"
            report["note"] = ("the real tool ran on a fixture built here with a known answer (and, for checkers, a planted "
                              "flaw it must catch); it was not run on the task text unless a step says so")
            report["script_sha256"] = sha256(script) if script.is_file() else None
            recipe(Ctx(tool=tool, script=script, work=work, env=env, timeout=a.timeout, task=a.task,
                       steps=steps, check=check))
            code = 0 if checks and all(c["pass"] for c in checks) else 1
            raise _Done
        tests = [(REPO / t).resolve() for t in (tool.get("tests") or [])]
        if not tests:
            report.update(error="no test files are registered for this tool", verdict="refused")
            artifact.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            return 2
        check("tool script exists", script.exists(), report["script"])
        report["script_sha256"] = sha256(script) if script.is_file() else None
        needles = {script.stem, script.name, tool["path"].rstrip("/")}
        unrelated, related = [], 0
        for test in tests:
            name = str(test.relative_to(REPO)) if test.is_relative_to(REPO) else str(test)
            if not test.is_file():
                check(f"test file exists: {name}", False)
                continue
            text = test.read_text(encoding="utf-8", errors="replace")
            if not any(n in text for n in needles):
                # The registry lists it, but it never names this tool: running it would prove nothing about the tool.
                unrelated.append(name)
                continue
            related += 1
            if test.suffix in (".mjs", ".js", ".cjs"):
                step = run_node_test(test, work, env, a.timeout)
                steps.append(step)
                check(f"{name}: at least one test really ran", step["ran"] - step["skipped"] >= 1,
                      {"ran": step["ran"], "skipped": step["skipped"]})
                check(f"{name}: node --test passed", step["exit_code"] == 0 and step["failed"] == 0, step["result"])
                continue
            if "unittest" not in text and "pytest" not in text:
                step = run_script_test(test, work, env, a.timeout)
                steps.append(step)
                check(f"{name}: script test exits 0 and reports its cases", step["exit_code"] == 0 and step["lines"] > 0,
                      {"exit": step["exit_code"], "lines": step["lines"]})
                continue
            step = run_suite(test, work, env, a.timeout)
            steps.append(step)
            really = step["ran"] - step["skipped"] - step["expected_failures"]
            check(f"{name}: at least one test really ran", really >= 1,
                  {"ran": step["ran"], "skipped": step["skipped"]})
            check(f"{name}: unittest OK", step["exit_code"] == 0 and step["result"].startswith("OK"), step["result"])
        report["unrelated_tests_not_run"] = unrelated
        check("at least one registered test file names this tool", related >= 1, {"related": related, "unrelated": unrelated})
        st = self_test_argv(tool, script)
        if st:
            done = subprocess.run(st, cwd=REPO, env=env, text=True, capture_output=True,
                                  stdin=subprocess.DEVNULL, timeout=a.timeout, check=False)
            steps.append({"step": "documented --self-test", "command": st, "exit_code": done.returncode,
                          "stdout_tail": done.stdout[-600:], "stderr_tail": done.stderr[-300:]})
            check("documented --self-test exits 0", done.returncode == 0, done.returncode)
        code = 0 if checks and all(c["pass"] for c in checks) else 1
    except _Done:
        pass
    except (KeyError, OSError, ValueError, subprocess.SubprocessError, json.JSONDecodeError, AssertionError) as exc:
        error = str(exc)[:500]
        code = 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    report.update(steps=steps, checks=checks, error=error,
                  tests_ran=sum(s.get("ran", 0) for s in steps),
                  tests_skipped=sum(s.get("skipped", 0) for s in steps),
                  verdict="passed" if code == 0 else "failed")
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
