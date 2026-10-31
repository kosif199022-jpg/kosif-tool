#!/usr/bin/env python3
"""Black Dragon adapter runner: run one registered repo tool and keep its output.

Usage: _black_dragon_exec.py ARTIFACT TOOL_SCRIPT [tool args...]
TOOL_SCRIPT is a repo-relative .py path. The tool's stdout is written to
ARTIFACT (stderr tail appended); the exit code is the tool's own, so a failed
tool can never produce an 'executed' receipt. No shell is used.
"""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    artifact, rel = Path(argv[0]), Path(argv[1])
    if rel.is_absolute() or ".." in rel.parts or rel.suffix != ".py":
        print("tool script must be a repo-relative .py path", file=sys.stderr)
        return 2
    script = (REPO / rel).resolve()
    if REPO not in script.parents or not script.is_file():
        print("tool script not found inside the repository", file=sys.stderr)
        return 2
    done = subprocess.run([sys.executable, str(script), *argv[2:]], cwd=REPO, text=True,
                          capture_output=True, stdin=subprocess.DEVNULL, check=False)
    artifact.parent.mkdir(parents=True, exist_ok=True)
    body = done.stdout
    if done.stderr.strip():
        body += "\n--- stderr (tail) ---\n" + done.stderr[-2000:]
    artifact.write_text(body, encoding="utf-8")
    return done.returncode


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
