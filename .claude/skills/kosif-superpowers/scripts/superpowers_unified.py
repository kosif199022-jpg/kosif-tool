#!/usr/bin/env python3
"""KOSIF Superpowers Ultimate: master capability router and reversible Claude installer.

Third-party process skills are vendored from obra/superpowers v7.0.0 (MIT).
This script never invokes external skill scripts or installs paid packages.
"""
from __future__ import annotations
import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
SOURCE = SKILL_DIR / "vendor" / "obra-superpowers-v7" / "skills"
SOURCE_LICENSE = SKILL_DIR / "vendor" / "obra-superpowers-v7" / "LICENSE"
KOSIF = "kosif-superpowers"
SKILLS = (
    "brainstorming", "diagnosing-superpowers", "dispatching-parallel-agents",
    "executing-plans", "finishing-a-development-branch", "receiving-code-review",
    "requesting-code-review", "subagent-driven-development", "systematic-debugging",
    "test-driven-development", "using-git-worktrees", "using-superpowers",
    "verification-before-completion", "writing-plans", "writing-skills"
)
PROCESS_RULES = (
    ("systematic-debugging", ("bug", "debug", "error", "failed", "fix", "crash",
                               "مشكلة", "خطأ", "اصلح", "إصلاح", "تعطل")),
    ("receiving-code-review", ("review feedback", "review comments", "ملاحظات مراجعة")),
    ("requesting-code-review", ("code review", "review code", "مراجعة الكود")),
    ("using-git-worktrees", ("worktree", "parallel branches", "ورك تري")),
    ("dispatching-parallel-agents", ("parallel agents", "independent tasks", "وكلاء متوازيين")),
    ("writing-skills", ("create skill", "write skill", "تطوير مهارة", "إنشاء مهارة")),
    ("brainstorming", ("create", "build", "design", "develop", "idea", "new app",
                        "ابداع", "إبداع", "فكرة", "صمم", "تصميم", "ابني", "بناء", "طور", "تطوير")),
    ("writing-plans", ("plan", "roadmap", "architecture", "strategy", "خطة", "تخطيط", "معمارية")),
    ("executing-plans", ("implement the plan", "execute plan", "نفذ الخطة", "تنفيذ الخطة")),
    ("finishing-a-development-branch", ("merge", "release", "ship branch", "ادمج", "دمج", "فرع")),
)
GLOBAL_START = "<!-- KOSIF_SUPERPOWERS_ULTIMATE_START -->"
GLOBAL_END = "<!-- KOSIF_SUPERPOWERS_ULTIMATE_END -->"
GLOBAL_POLICY = """<!-- KOSIF_SUPERPOWERS_ULTIMATE_START -->
# KOSIF Superpowers Ultimate — canonical skill entry point
For each substantial task, discover relevant skills and begin with the installed
~/.claude/skills/kosif-superpowers/SKILL.md and its boot/capability-router guidance.
KOSIF is the master capability registry and executor. obra/superpowers v7 skills
are separate process-method specialists, NOT a replacement for KOSIF.
Before implementing, choose relevant process skills with:
python ~/.claude/skills/kosif-superpowers/scripts/superpowers_unified.py plan "<task>"
Read the selected process skill's SKILL.md when applicable. Use brainstorming
before major design, systematic-debugging for bugs, TDD when coding, and
verification-before-completion before claiming success.
Report verified capabilities distinctly from merely documented ones.
Preserve originals; do not trigger paid calls, system-wide installs, publishing,
credential disclosure, or external uploads without explicit authorization.
Honor licensing and the user's requirements. No fictional successful tool runs.
<!-- KOSIF_SUPERPOWERS_ULTIMATE_END -->
"""

def verify_source():
    problems = []
    if not SOURCE_LICENSE.is_file():
        problems.append("Missing MIT LICENSE")
    for s in SKILLS:
        if not (SOURCE / s / "SKILL.md").is_file():
            problems.append("Missing source skill: " + s)
    return problems

def plan(task: str) -> dict:
    low = task.casefold()
    matches = [name for name, words in PROCESS_RULES if any(w in low for w in words)]
    if not matches:
        matches = ["brainstorming"] if any(w in low for w in ("video", "montage", "موشن", "مونتاج")) else []
    ordered = ["using-superpowers"] + matches
    if "brainstorming" in ordered or "writing-plans" in ordered:
        ordered += ["writing-plans"]
    if any(w in low for w in ("code", "app", "program", "develop", "build", "كود", "برنامج", "تطبيق", "برمجة", "تطوير", "اصلح")):
        ordered += ["test-driven-development"]
    ordered += ["verification-before-completion"]
    selected = list(dict.fromkeys(ordered))
    return {
        "master": KOSIF, "process_skills": selected, "task": task,
        "source": "obra/superpowers v7.0.0 (MIT), vendored in KOSIF",
        "next": ["Read KOSIF SKILL.md", "Run boot.py and powers.py suggest for the task",
                 "Read each selected process skill SKILL.md", "Execute and verify real results"],
    }

def doctor(home: Path) -> dict:
    installed = home / ".claude" / "skills"
    missing = verify_source()
    return {
        "status": "ready" if not missing else "incomplete",
        "source_skill_count": len(SKILLS) - len([m for m in missing if m.startswith("Missing source skill")]),
        "source_errors": missing,
        "installed_kosif": (installed / KOSIF / "SKILL.md").is_file(),
        "installed_process_count": sum((installed / x / "SKILL.md").is_file() for x in SKILLS),
        "target": str(installed),
        "license": "MIT; original copyright and LICENSE preserved",
        "note": "Installed != executed; rerun KOSIF boot.py on this host.",
    }

def _same_files(src: Path, dest: Path) -> bool:
    if not dest.exists(): return False
    sf = [p for p in src.rglob("*") if p.is_file()]
    df = [p for p in dest.rglob("*") if p.is_file()]
    if len(sf) != len(df): return False
    return all((dest / p.relative_to(src)).is_file()
               and (dest / p.relative_to(src)).read_bytes() == p.read_bytes() for p in sf)

def install(home: Path, force: bool = False, global_instructions: bool = True) -> dict:
    errors = verify_source()
    if errors: raise RuntimeError("Source verification failed: " + "; ".join(errors))
    target = home / ".claude" / "skills"
    target.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = home / ".claude" / "backups" / ("kosif-ultimate-" + stamp)
    results = []
    paths = [(KOSIF, SKILL_DIR)] + [(n, SOURCE / n) for n in SKILLS]
    for name, src in paths:
        dst = target / name
        if _same_files(src, dst):
            results.append({"skill": name, "result": "already_current"})
            continue
        if dst.exists():
            if not force:
                results.append({"skill": name, "result": "skipped_existing_use_force"})
                continue
            backup.mkdir(parents=True, exist_ok=True)
            shutil.copytree(dst, backup / name)
            shutil.rmtree(dst)
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        results.append({"skill": name, "result": "installed"})
    instructions = "not requested"
    if global_instructions:
        path = home / ".claude" / "CLAUDE.md"
        original = path.read_text(encoding="utf-8") if path.is_file() else ""
        if GLOBAL_START in original and GLOBAL_END in original:
            instructions = "already_present"
        else:
            if path.is_file():
                backup.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, backup / "CLAUDE.md")
            with path.open("a", encoding="utf-8") as f:
                f.write(("\n\n" if original.strip() else "") + GLOBAL_POLICY)
            instructions = "appended_to_global_CLAUDE.md"
    return {"results": results, "instructions": instructions, "backup": str(backup) if backup.exists() else None,
            "verified": doctor(home)}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor")
    q = sub.add_parser("plan"); q.add_argument("task")
    q = sub.add_parser("install"); q.add_argument("--force", action="store_true"); q.add_argument("--no-global-instructions", action="store_true")
    sub.add_parser("list")
    a = p.parse_args()
    if a.command == "doctor": result = doctor(Path.home())
    elif a.command == "plan": result = plan(a.task)
    elif a.command == "list": result = {"master": KOSIF, "process_skills": SKILLS}
    else: result = install(Path.home(), force=a.force, global_instructions=not a.no_global_instructions)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if a.command == "doctor" and result["source_errors"]: return 2
    return 0

if __name__ == "__main__":
    sys.exit(main())
