#!/usr/bin/env python3
"""Black Dragon method adapter: apply ONE catalog entry to the task and write its sheet.

Usage: _black_dragon_apply.py ARTIFACT KEY KIND SOURCE TASK

Most catalog entries (powers, superpowers, skills, styles, playbooks, protocol
rules) are methods, not programs. This adapter does the real work a method
entry allows, from the entry's own source file:
  1. loads the entry (fails with exit 3 if it cannot be found),
  2. checks every declared requirement on THIS machine (python module, npm
     package, program on PATH, environment key present - never its value),
  3. checks that the entry's cited proof files exist in the repository,
  4. scores how well the entry fits the task (shared words),
  5. writes an application sheet: what to do for this task, what is ready,
     what is missing, and the acceptance check.
The receipt written by black_dragon.py marks this class "method-apply": it
proves the entry was read and applied to the task here, NOT that a program
with that name ran. Reports keep the two classes apart.
"""
from __future__ import annotations
import importlib.util
import json
import os
import re
import shutil
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
REPO = SKILL.parents[2]
WORD = re.compile(r"[\w؀-ۿ]{3,}")


def words(text: str) -> set[str]:
    return {w.lower() for w in WORD.findall(text or "")}


def load_entry(key: str, kind: str, source: str) -> tuple[dict, str]:
    """Return (record, text) for the entry, or raise LookupError."""
    ident = key.split(":", 1)[1]
    if kind == "power":
        rows = json.loads((SKILL / source).read_text(encoding="utf-8"))
        rows = rows if isinstance(rows, list) else rows.get("powers", [])
        for row in rows:
            if row.get("id") == ident:
                return row, " ".join(str(row.get(k, "")) for k in
                                     ("name_ar", "name_en", "what", "how", "when", "tags"))
    elif kind == "superpower":
        for row in json.loads((SKILL / "data" / "superpowers.json").read_text(encoding="utf-8"))["items"]:
            if row.get("id") == ident:
                return row, " ".join(str(row.get(k, "")) for k in ("name_ar", "name_en", "focus", "family"))
    elif kind == "tool":
        for row in json.loads((SKILL / "data" / "tools.json").read_text(encoding="utf-8"))["tools"]:
            if row.get("id") == ident:
                return row, json.dumps(row, ensure_ascii=False)[:3000]
    elif kind == "style":
        for row in json.loads((REPO / "catalog" / "styles.json").read_text(encoding="utf-8")):
            if row.get("id") == ident:
                extra = REPO / "styles" / ident / "STYLE.json"
                if extra.is_file():
                    row = {**row, "style_json": json.loads(extra.read_text(encoding="utf-8"))}
                return row, json.dumps(row, ensure_ascii=False)[:3000]
    elif kind in ("skill", "playbook", "protocol"):
        base = {"skill": SKILL.parent, "playbook": REPO, "protocol": SKILL}[kind]
        path = base / source
        if path.is_file():
            text = path.read_text(encoding="utf-8", errors="replace")
            return {"id": ident, "path": str(path.relative_to(REPO))}, text
    raise LookupError(f"entry {key} not found in {source}")


PIP_IMPORT = {"pillow": "PIL", "opencv": "cv2", "opencv-python": "cv2", "opencv_python": "cv2",
              "scikit-learn": "sklearn", "pyyaml": "yaml", "beautifulsoup4": "bs4", "faster-whisper": "faster_whisper"}
BIN_ALIASES = {"imagemagick": ("convert", "magick"), "chromium": ("chromium", "chromium-browser", "google-chrome"),
               "python3": ("python3",), "node": ("node",), "ffmpeg": ("ffmpeg",)}
PSEUDO = {"optional": "optional extra the card does not name", "binaries": "unnamed binaries",
          "network": "outbound network (session policy)"}


def check_requirement(req: str) -> tuple[str, str]:
    """(state, note) for one declared requirement. Never prints secret values."""
    prefix, _, name = req.partition(":")
    if not name:
        prefix, name = "bin", req
    if prefix == "bin" and name in PSEUDO:
        return ("unknown" if name != "network" else "external", PSEUDO[name])
    if prefix == "fonts":
        ok = (REPO / "fonts").is_dir() and any((REPO / "fonts").iterdir())
        return ("ready" if ok else "missing", f"fonts ({name}) in the repository fonts/ folder")
    if prefix == "bin" and name == "chromium" and Path("/opt/pw-browsers").is_dir():
        return ("ready", "Chromium from the pre-installed Playwright browsers")
    if prefix == "bin" and name in BIN_ALIASES:
        return ("ready" if any(shutil.which(b) for b in BIN_ALIASES[name]) else "missing", f"program {name}")
    if prefix == "pip":
        base = name.split("[")[0].split("=")[0].lower()
        mod = PIP_IMPORT.get(base, base.replace("-", "_"))
        return ("ready" if importlib.util.find_spec(mod) else "missing", f"python module {mod}")
    if prefix == "npm":
        roots = [REPO / "node_modules", Path("/usr/lib/node_modules"), Path("/usr/local/lib/node_modules"),
                 Path("/opt/node22/lib/node_modules"), Path("/opt/node-tools/node_modules")]
        found = any((r / name).is_dir() for r in roots)
        return ("ready" if found else "missing", f"npm package {name}")
    if prefix == "key":
        env = name.upper().replace("-", "_")
        if name in ("unspecified", ""):
            return ("unknown", "an API key the card does not name")
        present = any(k.startswith(env) for k in os.environ)
        return ("ready" if present else "missing", f"environment key {env}* (value not read)")
    if prefix in ("claude", "mcp", "connector"):
        return ("external", f"{prefix} capability {name} (session-side)")
    return ("ready" if shutil.which(name) else "missing", f"program {name}")


def proof_paths(row: dict) -> list[tuple[str, bool]]:
    out = []
    for item in row.get("proof", []) or []:
        p = str(item).split(":")[0]
        if p.startswith("kosif-tool/"):
            path = REPO / p[len("kosif-tool/"):]
            out.append((str(item), path.exists()))
        elif p.startswith((".claude/", "playbooks/", "styles/", "tools/", "catalog/")):
            out.append((str(item), (REPO / p).exists()))
        else:
            out.append((str(item), False))  # outside this repository: not checkable here
    return out


def checklist(text: str, task_words: set[str], limit: int = 10) -> list[str]:
    lines = [l.strip() for l in text.splitlines() if re.match(r"\s*(?:[-*]|\d+[.)])\s+\S", l)]
    scored = sorted(lines, key=lambda l: -len(words(l) & task_words))
    return [l[:220] for l in scored[:limit]]


def main(argv: list[str]) -> int:
    if len(argv) != 5:
        print(__doc__, file=sys.stderr)
        return 2
    artifact, key, kind, source, task = Path(argv[0]), argv[1], argv[2], argv[3], argv[4]
    try:
        row, text = load_entry(key, kind, source)
    except (LookupError, OSError, ValueError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        return 3
    tw, ew = words(task), words(text)
    shared = sorted(tw & ew)
    reqs = [check_requirement(str(r)) + (str(r),) for r in (row.get("requires") or [])]
    missing = [r for s, _, r in reqs if s == "missing"]
    proofs = proof_paths(row)
    sheet = {
        "schema": "kosif.black-dragon.method-sheet.v1", "entry": key, "kind": kind, "source": source,
        "class": "method-apply",
        "name": row.get("name_ar") or row.get("name") or row.get("id"),
        "name_en": row.get("name_en", ""),
        "status_in_catalog": row.get("status") or row.get("best") or "",
        "task_fit": {"shared_words": shared[:40], "score": len(shared)},
        "apply": (row.get("how") or row.get("what") or row.get("description") or "")[:1200],
        "when": row.get("when", ""),
        "requirements": [{"requirement": r, "state": s, "note": n} for s, n, r in reqs],
        "ready_here": not missing,
        "missing": missing,
        "proofs": [{"proof": p, "exists_here": ok} for p, ok in proofs],
        "checklist": checklist(text, tw) if kind in ("skill", "playbook", "protocol") else [],
        "pipeline": [p.get("id") for p in row.get("pipeline", [])][:40] if kind == "superpower" else [],
        "acceptance": ("the step that uses this method shows its result in the delivered file and "
                       "passes the job's own checks (duration, fps, audio checksum, stills reviewed)"),
        "truth": "applied as a method to this task here; not a separate program run",
    }
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text(json.dumps(sheet, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
