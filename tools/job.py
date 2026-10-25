#!/usr/bin/env python3
"""Run a long job (render, encode, download) in the background and wait on it without `sleep N; check`.

Claude Code blocks `sleep 60; grep ... render.log` and chained sleeps. This tool replaces that pattern:

  start   launch the command detached; returns at once (log, pid and exit code go into --dir)
  wait    block until the job ends, printing one PROGRESS line when progress changes (throttled),
          then DONE or FAILED; exit code = the job's exit code. Run it with the Monitor tool
          (each line is a notification) or with Bash run_in_background (one notification at the end).
  status  print one line about the job right now and return (never waits)

Examples:
  python3 tools/job.py start --dir out/20261024-film/render -- node tools/render_html.cjs --in film.html --out out/film.mp4
  python3 tools/job.py wait  --dir out/20261024-film/render            # via Monitor or run_in_background
  python3 tools/job.py status --dir out/20261024-film/render

Stdlib only. Progress is read from the job log: render_html.cjs `frame 120/450`, ffmpeg `frame=  120`,
percentages (`37%`, yt-dlp, Remotion), and `x/y` counters.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import signal
import subprocess
import sys
import time
from pathlib import Path

PROGRESS_RE = re.compile(r"frame[ =]\s*\d+(?:/\d+)?|\b\d{1,3}(?:\.\d+)?%|\b\d+/\d+\b|encoding|VERIFY")
ERROR_RE = re.compile(r"Traceback|\bError\b|\bERROR\b|FAILED|\bFAIL\b|Killed|out of memory|No space left", re.I)


def _paths(d: Path) -> dict:
    return {k: d / f"job.{k}" for k in ("log", "pid", "exit", "json")}


def _alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    # a finished child of ours that nobody reaped is a zombie: treat as dead
    try:
        with open(f"/proc/{pid}/stat", encoding="utf-8") as fh:
            return fh.read().split(")")[-1].split()[0] != "Z"
    except OSError:
        return True


def _tail(log: Path, size: int = 65536) -> list[str]:
    if not log.exists():
        return []
    with open(log, "rb") as fh:
        fh.seek(0, os.SEEK_END)
        end = fh.tell()
        fh.seek(max(0, end - size))
        data = fh.read().decode("utf-8", "replace")
    # ffmpeg rewrites its progress line with \r, so split on both
    return [ln.strip() for ln in re.split(r"[\r\n]+", data) if ln.strip()]


def _last(lines: list[str], rx: re.Pattern) -> str:
    for ln in reversed(lines):
        if rx.search(ln):
            return ln[:300]
    return ""


def _state(d: Path) -> dict:
    p = _paths(d)
    if not p["pid"].exists():
        return {"state": "missing", "detail": f"no job in {d} (run `job.py start` first)"}
    lines = _tail(p["log"])
    pid = int(p["pid"].read_text().strip() or 0)
    # liveness first, exit file second: the job writes its exit code before it dies, so this order has no race
    alive = bool(pid) and _alive(pid)
    if p["exit"].exists():
        txt = p["exit"].read_text().strip()
        code = int(txt) if txt.lstrip("-").isdigit() else 1
        return {"state": "done" if code == 0 else "failed", "code": code, "progress": _last(lines, PROGRESS_RE), "lines": lines}
    if alive:
        return {"state": "running", "pid": pid, "progress": _last(lines, PROGRESS_RE), "error": _last(lines[-20:], ERROR_RE), "lines": lines}
    return {"state": "failed", "code": 1, "detail": "job process is gone and left no exit code (killed?)", "lines": lines}


def cmd_run(args) -> int:  # internal: the detached supervisor
    d = Path(args.dir)
    p = _paths(d)
    with open(p["log"], "ab", buffering=0) as log:
        try:
            code = subprocess.call(args.cmd, stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
        except OSError as exc:
            log.write(f"[job] cannot start: {exc}\n".encode())
            code = 127
    if code < 0:  # killed by a signal: report it the shell way (128 + signal number)
        code = 128 - code
    tmp = p["exit"].with_suffix(".exit.tmp")
    tmp.write_text(str(code))
    os.replace(tmp, p["exit"])
    return code


def cmd_start(args) -> int:
    if not args.cmd:
        print("usage: job.py start --dir DIR -- COMMAND ...", file=sys.stderr)
        return 2
    d = Path(args.dir)
    d.mkdir(parents=True, exist_ok=True)
    p = _paths(d)
    st = _state(d)
    if st["state"] == "running":
        print(f"ALREADY_RUNNING pid={st['pid']} dir={d}")
        return 1
    for k in ("exit", "pid"):
        p[k].unlink(missing_ok=True)
    p["log"].write_text("")
    proc = subprocess.Popen(
        [sys.executable, os.path.abspath(__file__), "_run", "--dir", str(d), "--", *args.cmd],
        stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        start_new_session=True, cwd=os.getcwd(),
    )
    p["pid"].write_text(str(proc.pid))
    p["json"].write_text(json.dumps({"cmd": args.cmd, "cwd": os.getcwd(), "started": time.time()}, ensure_ascii=False))
    print(f"STARTED pid={proc.pid} log={p['log']}")
    print(f"next: python3 tools/job.py wait --dir {d}   (Monitor, or Bash run_in_background)")
    return 0


def _finish(st: dict) -> int:
    lines = st.get("lines") or []
    if st["state"] == "done":
        print(f"DONE exit=0 {st.get('progress', '')}".rstrip())
        return 0
    print(f"FAILED exit={st.get('code', 1)} {st.get('detail', '')}".rstrip())
    for ln in lines[-5:]:
        print(f"  | {ln[:300]}")
    return st.get("code", 1) or 1


def cmd_wait(args) -> int:
    d = Path(args.dir)
    t0 = time.monotonic()
    last_print = 0.0
    last_progress = None
    last_error = None
    while True:
        st = _state(d)
        if st["state"] == "missing":
            print(f"FAILED {st['detail']}")
            return 2
        if st["state"] != "running":
            return _finish(st)
        now = time.monotonic()
        err = st.get("error")
        if err and err != last_error:
            last_error = err
            print(f"WARN {err}", flush=True)
        prog = st.get("progress")
        if not args.quiet and prog and prog != last_progress and now - last_print >= args.every:
            last_progress, last_print = prog, now
            print(f"PROGRESS {prog} ({int(now - t0)}s)", flush=True)
        if args.timeout and now - t0 >= args.timeout:
            print(f"TIMEOUT still running after {args.timeout}s, pid={st['pid']}: wait again or stop it")
            return 124
        time.sleep(args.poll)


def cmd_status(args) -> int:
    st = _state(Path(args.dir))
    if st["state"] == "running":
        print(f"RUNNING pid={st['pid']} {st.get('progress', '')}".rstrip())
        return 0
    if st["state"] == "missing":
        print(f"MISSING {st['detail']}")
        return 2
    return _finish(st)


def cmd_stop(args) -> int:
    st = _state(Path(args.dir))
    if st["state"] != "running":
        print(f"NOT_RUNNING {st['state']}")
        return 0
    os.killpg(os.getpgid(st["pid"]), signal.SIGTERM)
    print(f"STOPPED pid={st['pid']}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="action", required=True)
    for name in ("start", "_run"):
        s = sub.add_parser(name)
        s.add_argument("--dir", required=True)
        s.add_argument("cmd", nargs=argparse.REMAINDER)
    w = sub.add_parser("wait")
    w.add_argument("--dir", required=True)
    w.add_argument("--every", type=float, default=20, help="at most one PROGRESS line per N seconds (default 20)")
    w.add_argument("--poll", type=float, default=1, help="check interval in seconds (default 1)")
    w.add_argument("--timeout", type=float, default=0, help="give up after N seconds with exit 124 (0 = never)")
    w.add_argument("--quiet", action="store_true", help="no PROGRESS lines; only the final DONE/FAILED (for run_in_background)")
    for name in ("status", "stop"):
        sub.add_parser(name).add_argument("--dir", required=True)
    args = ap.parse_args(argv)
    if getattr(args, "cmd", None) and args.cmd[0] == "--":
        args.cmd = args.cmd[1:]
    return {"start": cmd_start, "_run": cmd_run, "wait": cmd_wait, "status": cmd_status, "stop": cmd_stop}[args.action](args)


if __name__ == "__main__":
    sys.exit(main())
