#!/usr/bin/env python3
"""Lint every SKILL.md in the repository, not only kosif-superpowers itself.

check_skill.py validates the kosif-superpowers skill. This tool covers all the
other skill folders too: the top-level skills under .claude/skills/, the vendored
sets (kosif-atlas, 100-superskills, obra-superpowers-v7) and the video styles
under styles/. It is stdlib only, reads files, and never changes anything.

Checks per SKILL.md
  error    no frontmatter, no name, no description, description over 1024 chars,
           a relative Markdown link [text](path) that points at a missing file
  warning  description under 60 chars, the same description shared by 5+ skills
           (Claude cannot tell them apart), a name used by two skills

Code blocks and inline code are skipped when looking for links, so example paths
in commands do not count. Frontmatter may be YAML or a one-line JSON object.

  python3 scripts/skills_lint.py                 # summary per group
  python3 scripts/skills_lint.py --list errors   # every error, one per line
  python3 scripts/skills_lint.py --json          # full report
  python3 scripts/skills_lint.py --group styles  # one group only

Exit code: 0 when there are no errors, 1 otherwise (warnings never fail).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SKILL_ROOTS = (ROOT / ".claude" / "skills", ROOT / "styles")
MAX_DESC = 1024
MIN_DESC = 60
SHARED_DESC = 5

FENCE_RE = re.compile(r"^(```|~~~).*?^\1[^\n]*$", re.M | re.S)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
LINK_RE = re.compile(r"\[[^\]\n]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
FM_RE = re.compile(r"^---[ \t]*\n(.*?)\n---[ \t]*(?:\n|$)", re.S)


def group_of(rel: str) -> str:
    if rel.startswith("styles/"):
        return "styles"
    for key, name in (("/vendor/kosif-atlas/", "atlas"), ("/vendor/100-superskills/", "superskills"),
                      ("/vendor/obra-superpowers-v7/", "obra")):
        if key in rel:
            return name
    return "top-level"


def parse_frontmatter(text: str) -> tuple[dict | None, str]:
    m = FM_RE.match(text)
    if not m:
        return None, text
    raw, body = m.group(1), text[m.end():]
    stripped = raw.strip()
    if stripped.startswith("{"):
        try:
            data = json.loads(stripped)
            return {k: str(v) for k, v in data.items()}, body
        except ValueError:
            pass
    fm: dict[str, str] = {}
    key = None
    for line in raw.splitlines():
        mm = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if mm:
            key = mm.group(1)
            fm[key] = mm.group(2).strip()
        elif key and line.strip():
            fm[key] = (fm[key] + " " + line.strip()).strip()
    for k, v in fm.items():
        v = re.sub(r"^[>|][-+]?\s*", "", v)
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            v = v[1:-1]
        fm[k] = v.strip()
    return fm, body


def broken_links(text: str, folder: Path) -> list[str]:
    prose = INLINE_CODE_RE.sub("", FENCE_RE.sub("", text))
    out = []
    for target in LINK_RE.findall(prose):
        if re.match(r"^(?:[a-z][a-z0-9+.-]*:|#|//)", target, re.I) or "{" in target or "<" in target:
            continue
        path = target.split("#", 1)[0].split("?", 1)[0]
        if not path:
            continue
        if not (folder / path).exists() and not (ROOT / path.lstrip("/")).exists():
            out.append(target)
    return sorted(set(out))


def lint(groups: set[str] | None = None) -> dict:
    files = sorted(p for base in SKILL_ROOTS if base.is_dir() for p in base.rglob("SKILL.md"))
    rows = []
    names: dict[str, list[str]] = defaultdict(list)
    descs: Counter = Counter()
    for p in files:
        rel = p.relative_to(ROOT).as_posix()
        g = group_of(rel)
        if groups and g not in groups:
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        fm, _body = parse_frontmatter(text)
        row = {"path": rel, "group": g, "errors": [], "warnings": []}
        if fm is None:
            row["errors"].append("no frontmatter")
            fm = {}
        name, desc = fm.get("name", ""), fm.get("description", "")
        if fm and not name:
            row["errors"].append("no name")
        if fm and not desc:
            row["errors"].append("no description")
        elif len(desc) > MAX_DESC:
            row["errors"].append(f"description is {len(desc)} chars (max {MAX_DESC})")
        elif desc and len(desc) < MIN_DESC:
            row["warnings"].append(f"description is only {len(desc)} chars; say what it does and when to use it")
        for link in broken_links(text, p.parent):
            row["errors"].append(f"broken link: {link}")
        if name:
            names[name].append(rel)
        if desc:
            descs[desc] += 1
        row["description"] = desc
        rows.append(row)
    for r in rows:
        n = descs.get(r["description"], 0)
        if n >= SHARED_DESC:
            r["warnings"].append(f"same description as {n - 1} other skills")
    for name, paths in names.items():
        if len(paths) > 1:
            for r in rows:
                if r["path"] in paths:
                    r["warnings"].append(f"name '{name}' is used by {len(paths)} skills")
    summary: dict[str, dict] = {}
    for r in rows:
        s = summary.setdefault(r["group"], {"skills": 0, "with_errors": 0, "with_warnings": 0, "errors": 0})
        s["skills"] += 1
        s["errors"] += len(r["errors"])
        s["with_errors"] += bool(r["errors"])
        s["with_warnings"] += bool(r["warnings"])
        r.pop("description")
    return {"ok": not any(r["errors"] for r in rows), "summary": summary, "skills": rows}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Lint every SKILL.md in the repository")
    ap.add_argument("--json", action="store_true", help="print the full report as JSON")
    ap.add_argument("--list", choices=("errors", "warnings", "all"), help="print one line per finding")
    ap.add_argument("--group", action="append", choices=("top-level", "atlas", "superskills", "obra", "styles"))
    a = ap.parse_args(argv)
    rep = lint(set(a.group) if a.group else None)
    if a.json:
        print(json.dumps(rep, ensure_ascii=False, indent=1))
    else:
        if a.list:
            for r in rep["skills"]:
                kinds = ("errors", "warnings") if a.list == "all" else (a.list,)
                for k in kinds:
                    for msg in r[k]:
                        print(f"{k[:-1]}\t{r['path']}\t{msg}")
        for g, s in sorted(rep["summary"].items()):
            print(f"{g:12} {s['skills']:4} skills · {s['with_errors']:3} with errors ({s['errors']}) · "
                  f"{s['with_warnings']:3} with warnings")
        print("skills_lint:", "OK" if rep["ok"] else "errors found")
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
