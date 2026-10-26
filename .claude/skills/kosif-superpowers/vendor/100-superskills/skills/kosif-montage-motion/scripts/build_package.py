"""Build the skill's zip packages.

    python scripts/build_package.py --out ../KOSIF-Montage-Motion-v6.1.zip                 full: everything for a local install
    python scripts/build_package.py --claude-ai --out ../KOSIF-Montage-Motion-v6.1-claude-ai.zip
                                                                                         the claude.ai skill upload (≤ 200 files)

Both leave out runtime folders (workbench, out, frames, caches) and scratch projects. The claude.ai package also leaves
out what an uploaded skill never uses and what `kmotion sync` restores: the test suites, the example videos/GIF served
by the local site, and the kit copies (motion-kit, gsap, 3D/lab/shape kits, fonts) inside example projects.
"""
from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLAUDE_AI_MAX_FILES = 200
SKIP_DIRS = {"__pycache__", "workbench", "out", "frames", ".claude", "node_modules", ".git"}
SCRATCH_PROJECTS = re.compile(r"^(demo_|tt_|wb_|ui_card$|title_demo$|t_card$|mcp_p$|direct_test$|verse_5s$|card\d*$|film\d*$)")
HISTORY_DOCS = {"CHANGELOG_v1.2_structural.md", "VOICE2MOTION_CHANGELOG.md", "UPGRADE_REPORT.md", "audit-v5.1.md", "audit-v5.3-python.md"}
KIT_COPIES = {"motion-kit.js", "gsap.min.js", "three-kit.bundle.js", "lab-kit.js", "shape-kit.js"}


def wanted(rel: Path, claude_ai: bool) -> bool:
    parts = rel.parts
    if set(parts) & SKIP_DIRS or rel.suffix in (".pyc", ".pyo") or rel.name.endswith(".bak"):
        return False
    in_projects = len(parts) > 2 and parts[0] == "scripts" and parts[1] == "projects"
    if in_projects and SCRATCH_PROJECTS.match(parts[2]):
        return False
    if in_projects and len(parts) > 4 and parts[3] in ("review", "sheet", "exports"):     # review copies, critique sheets, exports
        return False
    if in_projects and rel.name == "reel.json":                     # generated per machine (absolute local paths): never shipped
        return False
    if rel.name.endswith(".html.bak") or rel.name.endswith(".json.bak"):
        return False
    if not claude_ai:
        return True
    if parts[0] == "tests" or rel.name in ("test_audio2motion.py",):
        return False
    if parts[:4] == ("scripts", "web", "static", "examples") and rel.suffix.lower() in (".mp4", ".gif", ".webm", ".mov"):
        return False
    if in_projects and len(parts) > 4 and parts[3] == "assets" and (rel.name in KIT_COPIES or parts[4] == "fonts"):
        return False
    if parts[:3] == ("scripts", "kit", "sfx") and rel.suffix.lower() in (".ogg", ".wav"):      # the CC0 effects: full package only
        return False
    if rel.name in HISTORY_DOCS:                                   # past changelogs and audit notes: kept in the full package only
        return False
    if rel.name.endswith(".bat"):
        return False
    return True


def build(out: Path, claude_ai: bool) -> dict:
    files = sorted(p for p in ROOT.rglob("*") if p.is_file() and wanted(p.relative_to(ROOT), claude_ai))
    if not (ROOT / "SKILL.md").exists():
        raise SystemExit("SKILL.md missing")
    if claude_ai and len(files) > CLAUDE_AI_MAX_FILES:
        raise SystemExit(f"{len(files)} files: claude.ai accepts at most {CLAUDE_AI_MAX_FILES}")
    head = (ROOT / "SKILL.md").read_text(encoding="utf-8").split("\n---\n", 1)[0]
    m = re.search(r'^description:\s*"(.*)"\s*$', head, re.M)
    if not m or len(m.group(1)) > 1024:
        raise SystemExit(f"SKILL.md description must be ≤ 1024 characters (now {len(m.group(1)) if m else 'missing'})")
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in files:
            z.write(p, Path("kosif-montage-motion") / p.relative_to(ROOT))
    return {"file": str(out), "files": len(files), "kb": out.stat().st_size // 1024, "claude_ai": claude_ai}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True); ap.add_argument("--claude-ai", action="store_true")
    a = ap.parse_args()
    print(build(Path(a.out), a.claude_ai))
    return 0


if __name__ == "__main__":
    sys.exit(main())
