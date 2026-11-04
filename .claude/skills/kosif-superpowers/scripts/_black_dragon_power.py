#!/usr/bin/env python3
"""Black Dragon power adapters: run the code a catalogued power cites as its proof, and check it.

Usage: _black_dragon_power.py POWER_ID ARTIFACT [--task=TEXT] [--timeout=SECONDS]

A power card (data/powers/*.json) lists `proof` references. The ones that start with
`kosif-tool/` and name a code file that exists in this repository are its runnable proofs.
Each one is turned into a verification unit:

  test file     the file itself runs (unittest, `node --test`, or a plain test script that must
                exit 0 and report its cases);
  tool script   a script registered in data/tools.json runs through _black_dragon_tool.py (its
                registered test files, or its known-answer recipe);
  other script  the test files under tests/ or evals/ that name the script run (at most four,
                best match first); failing that, its own `--self-test` must exit 0.

`--help` is never enough. A proof with no unit (a sketch, a probe that aggregates many optional
checks, a script nobody tests) makes the power refused (exit 2). Exit 0 only when the power has at
least one unit and every unit passed: tests really ran (not all skipped) and the runner said OK.

Cache: units are keyed by the SHA-256 of every file they run (proof file, test files, runner), and
results are stored once per job in `power-proof-cache/` next to the job's `artifacts/` folder, with
a file lock, so 60 powers that cite evals/test_app_studio.py run it once. Every power still writes
its own artifact: the power, each proof path and SHA-256, the command, test counts and whether the
result came from the cache. The task text is not used: this proves the cited code works here.
"""
from __future__ import annotations
import argparse
import fcntl
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
SKILL = SCRIPTS.parent
REPO = SKILL.parents[2]
POWERS = SKILL / "data" / "powers"
TOOLS = SKILL / "data" / "tools.json"
TOOL_RUNNER = SCRIPTS / "_black_dragon_tool.py"
SCHEMA = "kosif.black-dragon.power-proof-adapter.v1"
CODE_SUFFIXES = (".py", ".js", ".mjs", ".cjs")
JS_SUFFIXES = (".js", ".mjs", ".cjs")
MAX_TESTS_PER_SCRIPT = 4
PRUNE = {"node_modules", "vendor", "out", ".git", "__pycache__", "fixtures"}
sys.path.insert(0, str(SCRIPTS))
import _black_dragon_tool as tool_mod  # noqa: E402

sha256 = tool_mod.sha256


# ---------------------------------------------------------------- catalog and proof resolution
def load_power(power_id: str, powers_dir: Path | None = None) -> dict:
    powers_dir = powers_dir or POWERS
    pid = power_id[len("power:"):] if power_id.startswith("power:") else power_id
    for path in sorted(powers_dir.glob("*.json")):
        obj = json.loads(path.read_text(encoding="utf-8"))
        rows = obj if isinstance(obj, list) else obj.get("powers", [])
        for row in rows:
            if isinstance(row, dict) and row.get("id") == pid:
                return dict(row, _catalog=path.name)
    raise KeyError(f"unknown power id: {pid}")


def local_proof(ref: str, repo: Path = REPO) -> str | None:
    """`kosif-tool/<path>[:line[-line]][#anchor]` -> repo-relative path of an existing code file."""
    if not isinstance(ref, str) or not ref.startswith("kosif-tool/"):
        return None
    raw = re.sub(r":\d+(?:[-:]\d+)?$", "", ref[len("kosif-tool/"):].split("#", 1)[0])
    rel = Path(raw)
    if not raw or rel.is_absolute() or ".." in rel.parts or rel.suffix not in CODE_SUFFIXES:
        return None
    target = (repo / rel).resolve()
    if not target.is_relative_to(repo.resolve()) or not target.is_file():
        return None
    return rel.as_posix()


def proof_files(row: dict, repo: Path = REPO) -> list[str]:
    out = []
    for ref in row.get("proof") or []:
        rel = local_proof(ref, repo)
        if rel and rel not in out:
            out.append(rel)
    return out


def is_test_file(rel: str) -> bool:
    name = Path(rel).name
    stem = name.split(".")[0]
    return stem.startswith("test") or stem.endswith("_test") or ".test." in name or ".spec." in name


def _tool_by_path(repo: Path = REPO, tools_file: Path = TOOLS) -> dict:
    out = {}
    try:
        rows = json.loads(tools_file.read_text(encoding="utf-8"))["tools"]
    except (OSError, ValueError, KeyError):
        return out
    try:
        from _black_dragon_tool_recipes import RECIPES
    except ImportError:
        RECIPES = {}
    for row in rows:
        if not isinstance(row, dict) or not row.get("id") or not row.get("path"):
            continue
        base = repo if row.get("root") == "repo" else repo / SKILL.relative_to(REPO)
        try:
            rel = (base / row["path"]).resolve().relative_to(repo.resolve()).as_posix()
        except ValueError:
            continue
        if row.get("tests") or row["id"] in RECIPES:
            out.setdefault(rel, row["id"])
    return out


def test_index(repo: Path = REPO) -> list[Path]:
    """Test files in tests/ and evals/ folders of this repository (vendored code is never searched)."""
    found = []
    for dirpath, dirnames, filenames in os.walk(repo):
        dirnames[:] = sorted(d for d in dirnames if d not in PRUNE)
        if Path(dirpath).name not in ("tests", "evals"):
            continue
        for name in sorted(filenames):
            if Path(name).suffix in CODE_SUFFIXES and is_test_file(name):
                found.append(Path(dirpath) / name)
    return found


def mentions(text: str, rel: str) -> bool:
    p = Path(rel)
    if p.name in text or rel in text:
        return True
    if p.suffix == ".py" and re.search(r"(?m)^\s*(?:from|import)\s+" + re.escape(p.stem) + r"\b", text):
        return True
    return False


def tests_naming(rel: str, index: list[Path], repo: Path = REPO) -> list[str]:
    stem = Path(rel).stem
    hits = []
    for test in index:
        if test.resolve() == (repo / rel).resolve():
            continue
        try:
            text = test.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if mentions(text, rel):
            exact = test.stem in (f"test_{stem}", f"{stem}_test", f"test_{stem.lstrip('_')}") or test.name.startswith(stem + ".test")
            hits.append((0 if exact else 1, test.stat().st_size, test.relative_to(repo).as_posix()))
    return [h[2] for h in sorted(hits)[:MAX_TESTS_PER_SCRIPT]]


def has_self_test(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    return path.suffix == ".py" and "--self-test" in text and "argparse" in text


class Resolver:
    """Turns a proof file into a verification unit (or a reason it has none). Pure: runs nothing."""

    def __init__(self, repo: Path = REPO, tools_file: Path = TOOLS):
        self.repo = repo
        self.tools = _tool_by_path(repo, tools_file)
        self._index = None

    @property
    def index(self) -> list[Path]:
        if self._index is None:
            self._index = test_index(self.repo)
        return self._index

    def unit(self, rel: str) -> dict:
        path = self.repo / rel
        if is_test_file(rel):
            return {"kind": "test-file", "proof": rel, "tests": [rel]}
        if rel in self.tools:
            return {"kind": "tool-runner", "proof": rel, "tool": self.tools[rel], "tests": []}
        tests = tests_naming(rel, self.index, self.repo)
        if tests:
            return {"kind": "tests-naming-script", "proof": rel, "tests": tests}
        if has_self_test(path):
            return {"kind": "self-test", "proof": rel, "tests": []}
        return {"kind": "none", "proof": rel,
                "reason": "no test file names it, no --self-test and no known-answer recipe (only --help would run)"}

    def units(self, row: dict) -> list[dict]:
        return [self.unit(rel) for rel in proof_files(row, self.repo)]


def unit_key(unit: dict, repo: Path = REPO) -> str:
    files = sorted({unit["proof"], *unit.get("tests", [])})
    payload = {"kind": unit["kind"], "tool": unit.get("tool"),
               "files": {f: sha256(repo / f) for f in files if (repo / f).is_file()},
               "runner": sha256(Path(__file__)) + sha256(TOOL_RUNNER)}
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


# ---------------------------------------------------------------- running one unit
def _run_test(test: Path, work: Path, env: dict, timeout: int) -> tuple[dict, list]:
    """Run one test file and return (step, checks)."""
    name = test.relative_to(REPO).as_posix() if test.is_relative_to(REPO) else str(test)
    text = test.read_text(encoding="utf-8", errors="replace")
    if test.suffix in JS_SUFFIXES:
        if "node:test" in text or re.search(r"\b(?:describe|test|it)\s*\(", text):
            step = tool_mod.run_node_test(test, work, env, timeout)
            return step, [(f"{name}: at least one test really ran", step["ran"] - step["skipped"] >= 1),
                          (f"{name}: node --test passed", step["exit_code"] == 0 and step["failed"] == 0)]
        argv = ["node", str(test)]
        done = subprocess.run(argv, cwd=REPO, env=env, text=True, capture_output=True,
                              stdin=subprocess.DEVNULL, timeout=timeout, check=False)
        log = work / f"{test.stem}.log"
        log.write_text(done.stdout + "\n--- stderr ---\n" + done.stderr, encoding="utf-8")
        lines = len([ln for ln in done.stdout.splitlines() if ln.strip()])
        step = {"step": f"node script test {name}", "command": argv, "exit_code": done.returncode,
                "lines": lines, "result": (done.stdout.strip().splitlines() or [""])[-1][:200],
                "log": str(log), "log_sha256": sha256(log)}
        return step, [(f"{name}: script test exits 0 and reports its cases", done.returncode == 0 and lines > 0)]
    if "unittest" in text:
        step = tool_mod.run_suite(test, work, env, timeout)
        really = step["ran"] - step["skipped"] - step["expected_failures"]
        return step, [(f"{name}: at least one test really ran", really >= 1),
                      (f"{name}: unittest OK", step["exit_code"] == 0 and step["result"].startswith("OK"))]
    if re.search(r"(?m)^\s*(?:import pytest|from pytest\b)|@pytest\.", text):
        return ({"step": f"pytest {name}", "command": [], "exit_code": None,
                 "result": "pytest-only test file; pytest is not a dependency here"},
                [(f"{name}: runnable without pytest", False)])
    step = tool_mod.run_script_test(test, work, env, timeout)
    return step, [(f"{name}: script test exits 0 and reports its cases",
                   step["exit_code"] == 0 and step["lines"] > 0)]


def run_unit(unit: dict, work: Path, env: dict, timeout: int) -> dict:
    steps, checks = [], []
    start = time.monotonic()
    kind = unit["kind"]
    try:
        if kind == "none":
            checks.append((unit["reason"], False))
        elif kind in ("test-file", "tests-naming-script"):
            for rel in unit["tests"]:
                test = REPO / rel
                if kind == "tests-naming-script" and not mentions(test.read_text(encoding="utf-8", errors="replace"),
                                                                  unit["proof"]):
                    checks.append((f"{rel} names {unit['proof']}", False))
                    continue
                step, cs = _run_test(test, work, env, timeout)
                steps.append(step)
                checks.extend(cs)
        elif kind == "tool-runner":
            out = work / "tool.json"
            argv = [sys.executable, "-B", str(TOOL_RUNNER), unit["tool"], str(out), f"--timeout={timeout}"]
            done = subprocess.run(argv, cwd=REPO, env=env, text=True, capture_output=True,
                                  stdin=subprocess.DEVNULL, timeout=timeout + 60, check=False)
            sub = json.loads(out.read_text(encoding="utf-8")) if out.is_file() else {}
            steps.append({"step": f"tool runner {unit['tool']}", "command": argv, "exit_code": done.returncode,
                          "mode": sub.get("mode"), "ran": sub.get("tests_ran", 0),
                          "skipped": sub.get("tests_skipped", 0), "result": sub.get("verdict"),
                          "tool_checks": sub.get("checks", []), "tool_artifact": str(out),
                          "tool_artifact_sha256": sha256(out) if out.is_file() else None})
            checks.append((f"tool {unit['tool']}: runner verdict passed (exit 0)",
                           done.returncode == 0 and sub.get("verdict") == "passed"))
            checks.append((f"tool {unit['tool']}: at least one real check ran", bool(sub.get("checks"))))
        elif kind == "self-test":
            script = REPO / unit["proof"]
            argv = [sys.executable, "-B", str(script), "--self-test"]
            done = subprocess.run(argv, cwd=REPO, env=env, text=True, capture_output=True,
                                  stdin=subprocess.DEVNULL, timeout=timeout, check=False)
            log = work / f"{script.stem}.self-test.log"
            log.write_text(done.stdout + "\n--- stderr ---\n" + done.stderr, encoding="utf-8")
            help_only = "usage:" in done.stdout[:400].lower() and "--self-test" not in done.stdout
            steps.append({"step": f"--self-test {unit['proof']}", "command": argv, "exit_code": done.returncode,
                          "result": (done.stdout.strip().splitlines() or [""])[-1][:200],
                          "log": str(log), "log_sha256": sha256(log)})
            checks.append((f"{unit['proof']} --self-test exits 0", done.returncode == 0))
            checks.append((f"{unit['proof']} --self-test did more than print usage", not help_only))
        else:
            checks.append((f"unknown unit kind {kind}", False))
    except subprocess.TimeoutExpired:
        checks.append((f"finished within {timeout}s", False))
    except (OSError, ValueError) as exc:
        checks.append((f"runner error: {str(exc)[:200]}", False))
    passed = bool(checks) and all(ok for _, ok in checks)
    return {"unit": unit, "steps": steps, "checks": [{"check": n, "pass": bool(ok)} for n, ok in checks],
            "tests_ran": sum(int(s.get("ran") or 0) for s in steps),
            "tests_skipped": sum(int(s.get("skipped") or 0) for s in steps),
            "seconds": round(time.monotonic() - start, 2), "verdict": "passed" if passed else "failed"}


def cache_root(artifact: Path) -> Path:
    parent = artifact.parent
    return (parent.parent if parent.name == "artifacts" else parent) / "power-proof-cache"


def cached_unit(unit: dict, cache: Path, timeout: int) -> tuple[dict, bool, str]:
    """Run a unit once per job; later callers wait on the lock and reuse the stored result."""
    key = unit_key(unit)
    entry = cache / key[:32]
    cache.mkdir(parents=True, exist_ok=True)
    with open(cache / f"{key[:32]}.lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        result_file = entry / "result.json"
        if result_file.is_file():
            stored = json.loads(result_file.read_text(encoding="utf-8"))
            if stored.get("key") == key:
                return stored, True, key
        if entry.exists():
            shutil.rmtree(entry)
        entry.mkdir(parents=True)
        # Scratch files go to the system temp dir (several tools refuse to write inside a git checkout).
        tmp = Path(tempfile.mkdtemp(prefix="black-dragon-power-"))
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=str(tmp), TEMP=str(tmp), TMP=str(tmp))
        try:
            result = run_unit(unit, entry, env, timeout)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        result["key"] = key
        result_file.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return result, False, key


# ---------------------------------------------------------------- one power
def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("power")
    ap.add_argument("artifact", type=Path)
    ap.add_argument("--task", default="")
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--cache", type=Path, default=None, help="cache folder (default: power-proof-cache in the job)")
    a = ap.parse_args(argv)
    artifact = a.artifact.resolve()
    artifact.parent.mkdir(parents=True, exist_ok=True)
    report = {"schema": SCHEMA, "power": a.power, "mode": "cited-proof-code",
              "note": "the code this power cites as proof ran here with known inputs and answers "
                      "(its tests, its tool runner or its --self-test); it was not run on the task text"}
    code, error, proofs = 1, None, []
    try:
        row = load_power(a.power)
        report.update(name_en=row.get("name_en"), catalog=row.get("_catalog"), status=row.get("status"))
        units = Resolver().units(row)
        cache = (a.cache.resolve() if a.cache else cache_root(artifact))
        for unit in units:
            entry = {"path": unit["proof"], "sha256": sha256(REPO / unit["proof"]), "runner": unit["kind"]}
            if unit["kind"] == "none":
                entry.update(verdict="no-runner", reason=unit["reason"])
                proofs.append(entry)
                continue
            result, hit, key = cached_unit(unit, cache, a.timeout)
            entry.update(tool=unit.get("tool"), tests=unit.get("tests"), cache_hit=hit, cache_key=key,
                         cache_entry=str(cache / key[:32]),
                         commands=[s.get("command") for s in result["steps"]],
                         tests_ran=result["tests_ran"], tests_skipped=result["tests_skipped"],
                         seconds=result["seconds"], checks=result["checks"], verdict=result["verdict"])
            proofs.append(entry)
        runnable = [p for p in proofs if p["verdict"] != "no-runner"]
        if not runnable:
            report.update(proofs=proofs, verdict="refused",
                          error="no cited proof can be run and checked here (only --help would run)")
            artifact.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            return 2
        code = 0 if all(p["verdict"] == "passed" for p in runnable) else 1
        report["proofs_without_runner"] = [p["path"] for p in proofs if p["verdict"] == "no-runner"]
    except (KeyError, OSError, ValueError, subprocess.SubprocessError) as exc:
        error, code = str(exc)[:500], 1
    report.update(proofs=proofs, error=error, verdict="passed" if code == 0 else "failed",
                  tests_ran=sum(int(p.get("tests_ran") or 0) for p in proofs))
    artifact.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
