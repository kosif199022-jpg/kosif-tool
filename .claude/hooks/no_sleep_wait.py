#!/usr/bin/env python3
"""PreToolUse hook for Bash: stop `sleep N; check` waits before Claude Code's own block does, with a fix that works here.

Blocks a foreground Bash command that sleeps 3 s or more outside a while/until loop (`sleep 60; grep ...`,
`sleep 30 && tail log`, `sleep 30; sleep 30`), or a one-liner `time.sleep(N)`. Allows run_in_background,
condition loops (`until <check>; do sleep 2; done`) and short settle sleeps (`sleep 1`). Never fails the session.
"""
from __future__ import annotations

import json
import re
import sys

LIMIT = 3  # seconds
SLEEP_RE = re.compile(r"(?:^|[;&|(\n]|\bthen\b|\belse\b)\s*sleep\s+(\d+(?:\.\d+)?)([smhd]?)\b")
PY_SLEEP_RE = re.compile(r"time\.sleep\(\s*(\d+(?:\.\d+)?)\s*\)")
UNIT = {"": 1, "s": 1, "m": 60, "h": 3600, "d": 86400}

HELP = (
    "Blocked by kosif-tool: do not wait with `sleep N; check` (Claude Code blocks it too).\n"
    "- Long job you are about to start: python3 tools/job.py start --dir <work>/job -- <command>\n"
    "  then wait with the Monitor tool: python3 tools/job.py wait --dir <work>/job  (one line per progress step)\n"
    "  or Bash run_in_background: python3 tools/job.py wait --dir <work>/job --quiet  (one notification at the end).\n"
    "- Or run the command itself with Bash run_in_background: true and keep working.\n"
    "- Waiting for a condition: Monitor with an until-loop, e.g. until grep -q VERIFY render.log; do sleep 2; done\n"
    "- A quick look at progress now: python3 tools/job.py status --dir <work>/job, or tail the log without sleeping.\n"
    "Do not chain shorter sleeps to get around this. Rules: playbooks/render-pipeline.md section 5 (waiting on a long render)."
)


def seconds(cmd: str) -> float:
    """Total sleep outside while/until loop bodies, in seconds (chained short sleeps add up)."""
    # a condition loop is the recommended pattern: ignore sleeps inside its do ... done body
    cmd = re.sub(r"\bdo\b.*?\bdone\b", " ", cmd, flags=re.S)
    worst = 0.0
    for num, unit in SLEEP_RE.findall(cmd):
        worst += float(num) * UNIT[unit]
    if re.search(r"\bpython3?\b[^\n]*\s-c\b", cmd):
        for num in PY_SLEEP_RE.findall(cmd):
            worst += float(num)
    return worst


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if data.get("tool_name") != "Bash":
        return 0
    ti = data.get("tool_input") or {}
    if ti.get("run_in_background"):
        return 0
    cmd = ti.get("command") or ""
    if seconds(cmd) >= LIMIT:
        print(HELP, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
