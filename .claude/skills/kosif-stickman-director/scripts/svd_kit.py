#!/usr/bin/env python3
"""Fetch and check Stickman Video Director (kaomei/stickman-video-director, MIT) for KOSIF.

The upstream skill is about 485 MB (audio library, reference films, fonts, art kits), so this
repository does not store it. This script fetches the pinned commit into a gitignored folder
(default out/stickman-video-director) or into ~/.claude/skills, and checks what arrived.

  python3 -I svd_kit.py fetch  [--dest out/stickman-video-director] [--commit SHA]
  python3 -I svd_kit.py status [--dest out/stickman-video-director] [--json]
  python3 -I svd_kit.py self-test

fetch uses git only (shallow, one commit, Git LFS smudge skipped). It never runs upstream code,
never runs npm, and never touches API keys. The skill folder ends up at
<dest>/skills/directing-stickman-videos/; copy or link that into ~/.claude/skills to install it.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

UPSTREAM = "https://github.com/kaomei/stickman-video-director"
PINNED = "8ef02ece5f12b8c7969fce1009d21653b597d203"   # reviewed 2026-11-16
SKILL_SUB = Path("skills/directing-stickman-videos")
REPO = Path(__file__).resolve().parents[4]
DEFAULT_DEST = REPO / "out" / "stickman-video-director"


def _git(*args, cwd=None) -> subprocess.CompletedProcess:
    env = dict(os.environ, GIT_LFS_SKIP_SMUDGE="1", GIT_TERMINAL_PROMPT="0")
    return subprocess.run(["git", *args], cwd=cwd, env=env, text=True, capture_output=True)


def fetch(dest: Path, commit: str) -> dict:
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise SystemExit("--commit must be a full 40-character SHA")
    dest = dest.resolve()
    if dest.exists() and any(dest.iterdir()) and not (dest / ".git").is_dir():
        raise SystemExit(f"{dest} exists and is not a git checkout; choose another --dest")
    if not (dest / ".git").is_dir():
        dest.mkdir(parents=True, exist_ok=True)
        for args in (("init", "-q"), ("remote", "add", "origin", UPSTREAM)):
            r = _git(*args, cwd=dest)
            if r.returncode:
                raise SystemExit(r.stderr.strip())
    r = _git("fetch", "-q", "--depth", "1", "origin", commit, cwd=dest)
    if r.returncode:
        raise SystemExit("git fetch failed: " + r.stderr.strip())
    r = _git("checkout", "-q", "--force", "FETCH_HEAD", cwd=dest)
    if r.returncode:
        raise SystemExit("git checkout failed: " + r.stderr.strip())
    return status(dest)


def status(dest: Path) -> dict:
    dest = dest.resolve()
    skill = dest / SKILL_SUB
    head = _git("rev-parse", "HEAD", cwd=dest).stdout.strip() if (dest / ".git").is_dir() else ""
    lic = (dest / "LICENSE").read_text(encoding="utf-8", errors="replace") if (dest / "LICENSE").is_file() else ""
    files = [p for p in skill.rglob("*") if p.is_file()] if skill.is_dir() else []
    return {
        "dest": str(dest),
        "commit": head,
        "pinned": head == PINNED,
        "licence_mit": lic.startswith("MIT License"),
        "skill_md": (skill / "SKILL.md").is_file(),
        "skill_dir": str(skill),
        "files": len(files),
        "references": len(list((skill / "references").glob("*.md"))) if skill.is_dir() else 0,
        "scripts": len([p for p in files if p.parent.name == "scripts"]),
        "bytes": sum(p.stat().st_size for p in files),
    }


def self_test() -> dict:
    """Known-answer test without network: fetch from a local git repo that imitates the layout."""
    with tempfile.TemporaryDirectory() as t:
        src = Path(t) / "src"
        (src / SKILL_SUB / "references").mkdir(parents=True)
        (src / "LICENSE").write_text("MIT License\n\nCopyright (c) test\n")
        (src / SKILL_SUB / "SKILL.md").write_text("---\nname: directing-stickman-videos\ndescription: x\n---\n")
        (src / SKILL_SUB / "references" / "a.md").write_text("a\n")
        for args in (("init", "-q"), ("add", "-A"),
                     ("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "t")):
            assert _git(*args, cwd=src).returncode == 0
        sha = _git("rev-parse", "HEAD", cwd=src).stdout.strip()
        global UPSTREAM
        saved, UPSTREAM = UPSTREAM, str(src)
        try:
            _git("-C", str(src), "config", "uploadpack.allowReachableSHA1InWant", "true")
            st = fetch(Path(t) / "dest", sha)
        finally:
            UPSTREAM = saved
        ok = st["commit"] == sha and st["licence_mit"] and st["skill_md"] and st["references"] == 1
        return {"ok": ok, "status": st}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fetch"); f.add_argument("--dest", type=Path, default=DEFAULT_DEST)
    f.add_argument("--commit", default=PINNED)
    s = sub.add_parser("status"); s.add_argument("--dest", type=Path, default=DEFAULT_DEST)
    s.add_argument("--json", action="store_true")
    sub.add_parser("self-test")
    a = ap.parse_args(argv)
    if a.cmd == "fetch":
        out = fetch(a.dest, a.commit)
    elif a.cmd == "status":
        out = status(a.dest)
    else:
        out = self_test()
        print(json.dumps(out, indent=1))
        return 0 if out["ok"] else 1
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
