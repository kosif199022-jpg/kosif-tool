#!/usr/bin/env python3
"""Local-first entry point for Claude Code; NEVER clones, downloads or installs.

Use this script inside the distributed skill bundle or the full kosif-tool repo.
Source availability is discovered without executing untrusted repository files.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import subprocess
import sys


def discover(skill_dir: Path):
    skill = skill_dir.resolve()
    if not (skill / "SKILL.md").is_file():
        raise ValueError("not a KOSIF skill directory")
    if not (skill / "scripts" / "powers.py").is_file():
        raise ValueError("missing powers.py")
    candidate = skill.parents[2] if len(skill.parents) > 2 else None
    cli = (candidate / "tools" / "kosif.py") if candidate else None
    # Only treat this as the full repo if the files actually exist at
    # the standard repo placement; never search random parent folders.
    styles = cli if (skill.parent.name == "skills"
                     and skill.parent.parent.name == ".claude"
                     and cli is not None and cli.is_file()) else None
    return {"skill": skill, "powers": skill / "scripts" / "powers.py",
            "styles": styles}


def doctor(paths):
    inventory = sorted((paths["skill"] / "data" / "powers").glob("*.json"))
    total = 0
    kinds = {}
    for path in inventory:
        records = json.loads(path.read_text(encoding="utf-8-sig"))
        if not isinstance(records, list):
            raise ValueError("catalog family is not a list: " + path.name)
        total += len(records)
        for record in records:
            if not isinstance(record, dict):
                raise ValueError("invalid record " + path.name)
            state = record.get("status", "missing")
            kinds[state] = kinds.get(state, 0) + 1
    return {"local_only": True, "network": False, "clone_required": False,
            "full_style_atlas_available": paths["styles"] is not None,
            "power_records": total, "families": len(inventory), "status_counts": kinds,
            "catalog_records_are_not_executed_capabilities": True,
            "next_step": "For style search without a full checkout, use power search and ask for a user-approved checkout only if the full atlas is essential."}


def main(argv=None):
    p = argparse.ArgumentParser(description="KOSIF Superpowers; no clone / no network")
    p.add_argument("--skill-dir", type=Path,
                   default=Path(__file__).resolve().parent.parent)
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor")
    search = sub.add_parser("search")
    search.add_argument("query", nargs="+")
    search.add_argument("--scope", choices=("auto", "styles", "powers"),
                        default="auto")
    args = p.parse_args(argv)
    try:
        paths = discover(args.skill_dir)
        if args.command == "doctor":
            print(json.dumps(doctor(paths), ensure_ascii=False))
            return 0
        if args.scope == "styles" and paths["styles"] is None:
            print(json.dumps({"error": "full_style_atlas_not_installed",
                  "resolution": "Use local power search. Full styles require an authorized existing repo checkout; this tool never clones automatically."}))
            return 2
        selected = (paths["styles"] if args.scope != "powers" and paths["styles"]
                    else paths["powers"])
        cmd = [sys.executable, str(selected), "search", *args.query]
        # Resolved known local scripts only, not untrusted arguments used as shell.
        return subprocess.run(cmd, shell=False, check=False).returncode
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
