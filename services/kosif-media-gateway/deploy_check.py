#!/usr/bin/env python3
"""Is the DEPLOYED gateway running the code in this checkout? Public, no token.

    python3 services/kosif-media-gateway/deploy_check.py [--url URL] [--expect-commit SHA] [--json]

Reads the public /health and compares it with server.py here:
  FRESH        deployed VERSION == this checkout's VERSION (and, with --expect-commit, the same commit)
  STALE        deployed VERSION differs, or the commit differs from --expect-commit
  UNREACHABLE  /health did not answer (Render Free sleeps; the first call can take a minute)
Every change to server.py bumps VERSION, so a version match means the code matches.
/health reports `build.commit` (Render's RENDER_GIT_COMMIT) from 0.3.0 on; an older deploy has no `build`.
Exit 0 FRESH, 1 STALE, 2 UNREACHABLE. The fix for STALE is the owner's: Render dashboard >
kosif-media-gateway > Manual Deploy > Deploy latest commit (or turn Auto-Deploy on).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_URL = "https://kosif-media-gateway-free-20261030.onrender.com"


def local_version(server: Path = HERE / "server.py") -> str:
    m = re.search(r'^VERSION = "([^"]+)"', server.read_text(encoding="utf-8"), re.M)
    if not m:
        raise SystemExit(f"no VERSION in {server}")
    return m.group(1)


def fetch_health(base: str, timeout: int = 120) -> dict:
    with urllib.request.urlopen(base.rstrip("/") + "/health", timeout=timeout) as r:
        return json.load(r)


def judge(health: dict | None, want_version: str, expect_commit: str = "") -> dict:
    if health is None:
        return {"verdict": "UNREACHABLE", "why": "/health did not answer"}
    got_version = health.get("version")
    build = health.get("build") or {}
    commit = build.get("commit")
    out = {"deployed_version": got_version, "repo_version": want_version, "deployed_commit": commit,
           "deployed_branch": build.get("branch"), "uptime_seconds": health.get("uptime_seconds")}
    if got_version != want_version:
        out.update(verdict="STALE", why=f"deployed {got_version}, repository {want_version}")
    elif expect_commit and not (commit and (commit.startswith(expect_commit) or expect_commit.startswith(commit))):
        out.update(verdict="STALE", why=f"deployed commit {commit or 'unknown'}, expected {expect_commit[:12]}")
    else:
        out.update(verdict="FRESH", why=f"deployed {got_version} = repository")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", default=os.environ.get("KOSIF_GATEWAY_URL", DEFAULT_URL))
    ap.add_argument("--expect-commit", default="", help="also require this deployed commit (hex prefix)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        health = fetch_health(a.url)
    except Exception as e:  # noqa: BLE001 - any network failure is UNREACHABLE
        health = None
        err = type(e).__name__
    r = judge(health, local_version(), a.expect_commit.strip().lower())
    r["gateway"] = a.url.rstrip("/")
    r["checked_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    if health is None:
        r["error"] = err
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else f"{r['verdict']}: {r['why']}")
    return {"FRESH": 0, "STALE": 1}.get(r["verdict"], 2)


if __name__ == "__main__":
    sys.exit(main())
