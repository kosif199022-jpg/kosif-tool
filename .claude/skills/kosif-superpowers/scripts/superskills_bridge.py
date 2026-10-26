#!/usr/bin/env python3
"""Read-only discovery and availability bridge for all 114 pinned 100-superskills."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

HOME = Path(__file__).resolve().parent.parent
INDEX = HOME / "data" / "100-superskills-index.json"
VENDOR = HOME / "vendor" / "100-superskills"

def catalog():
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    skills = data["skills"]
    if len(skills) != data["count"] or len({s["slug"] for s in skills}) != data["count"]:
        raise ValueError("Malformed 100-superskills index")
    return data, skills

def local_path(item):
    return VENDOR / "skills" / item["slug"] / "SKILL.md"

def tokens(s):
    return set(re.findall(r"[^\\W_]+", s.lower(), re.UNICODE))

def rank(query, items, limit):
    q = tokens(query)
    parts = []
    for s in items:
        names = s["slug"].replace("-", " ") + " " + s["ar"] + " " + s["en"]
        words = tokens(names)
        detail = tokens(s["description"])
        score = 3 * len(q & words) + len(q & detail)
        if query.lower() in names.lower():
            score += 10
        if score:
            parts.append((score, s["slug"], s))
    parts.sort(key=lambda x: (-x[0], x[1]))
    return [item for _, _, item in parts[:limit]]

def status(data, items):
    present = sum(local_path(s).is_file() for s in items)
    commit = None
    if (VENDOR / ".git").exists():
        try:
            p = subprocess.run(["git", "-C", str(VENDOR), "rev-parse", "HEAD"], capture_output=True,
                               text=True, timeout=5, check=False)
            if p.returncode == 0:
                commit = p.stdout.strip()
        except (OSError, subprocess.TimeoutExpired):
            pass
    return {
        "cataloged_skills": len(items),
        "available_skill_files": present,
        "source_checkout_present": present == len(items),
        "source_repository": data["source_repository"],
        "pinned_source_commit": data["source_commit"],
        "checkout_head": commit,
        "pinned_commit_matches": commit == data["source_commit"] if commit else None,
        "initialization_command": "git submodule update --init --recursive",
    }

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    subs.add_parser("doctor")
    sub = subs.add_parser("list")
    sub.add_argument("--category", default=None)
    sub = subs.add_parser("find")
    sub.add_argument("query")
    sub.add_argument("-n", "--limit", type=int, default=8)
    sub = subs.add_parser("show")
    sub.add_argument("slug")
    sub = subs.add_parser("path")
    sub.add_argument("slug")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    data, items = catalog()
    by_slug = {x["slug"]: x for x in items}
    if args.command == "doctor":
        out = status(data, items)
    elif args.command == "list":
        out = [s for s in items if not args.category or s["category"] == args.category]
    elif args.command == "find":
        out = rank(args.query, items, max(1, args.limit))
    else:
        if args.slug not in by_slug:
            parser.error("Unknown skill: " + args.slug)
        item = by_slug[args.slug]
        out = dict(item, available=local_path(item).is_file(),
                   local_path=str(local_path(item)))
        if args.command == "path":
            if not local_path(item).is_file():
                print("Submodule not checked out; run: git submodule update --init --recursive", file=sys.stderr)
                return 2
            print(local_path(item))
            return 0
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    elif isinstance(out, list):
        for s in out:
            print(f"{s['slug']} | {s['ar']} | {s['category']} | {s['path']} | {'ready' if local_path(s).is_file() else 'needs submodule'}")
    elif args.command == "doctor":
        for k, v in out.items():
            print(f"{k}: {v}")
    else:
        for k, v in out.items():
            print(f"{k}: {v}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
