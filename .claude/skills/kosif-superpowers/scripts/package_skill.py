#!/usr/bin/env python3
"""Package the skill as a zip for claude.ai upload / حزّم المهارة للرفع.

Builds kosif-superpowers.skill — a zip whose single top folder is kosif-superpowers/
with SKILL.md inside it (the layout the upload screen and the Skills API expect).
Runs scripts/check_skill.py first and stops on errors (use --no-check to skip).

  python3 package_skill.py                     # → dist/kosif-superpowers.skill (dist/ is git-ignored)
  python3 package_skill.py --lite              # drop images/audio/video (keeps all text and fonts)
  python3 package_skill.py -o ~/out/           # another folder
  python3 package_skill.py -o ~/out/ks.zip     # exact file name (.zip or .skill), outside the skill folder
  python3 package_skill.py --list              # show what would be packed, write nothing

Excluded always: dist/, __pycache__/, *.pyc, .DS_Store, node_modules/, .git*, evals/ (dev-only;
add --with-evals to keep them), *.skill/*.zip archives. The archive is deterministic: same files → same bytes.

claude.ai limits (help article 12512198, checked 2026-10-16): name ≤64 chars, description ≤200 chars, the zip
holds the skill folder as its root. The packaged SKILL.md therefore gets the frontmatter key
`claude_ai_description` (≤200 chars) as its description; the long description stays in the repo for Claude Code.
No zip size cap is documented there; if the upload refuses the file, try --lite.
Python 3.8+ standard library only.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SK = HERE.parent
NAME = SK.name
EXCLUDE_DIRS = {"dist", "__pycache__", "node_modules", ".git", "vendor"}
EXCLUDE_FILES = {".DS_Store", "Thumbs.db", ".gitignore", ".gitattributes"}
EXCLUDE_EXT = {".pyc", ".pyo", ".skill", ".zip"}
DESC_MAX = 200
MEDIA_EXT = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".avif", ".mp4", ".webm", ".mov", ".mkv", ".wav", ".mp3",
             ".ogg", ".m4a", ".flac", ".aac"}
FIXED_TIME = (1980, 1, 1, 0, 0, 0)


def human(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.1f} {unit}" if unit != "B" else f"{n} B"
        n /= 1024.0
    return f"{n:.1f} GB"


def collect(lite: bool, with_evals: bool):
    keep, skipped = [], {}
    for p in sorted(SK.rglob("*")):
        if not p.is_file():
            continue
        relp = p.relative_to(SK)
        parts = relp.parts
        reason = None
        if any(x in EXCLUDE_DIRS for x in parts[:-1]):
            reason = "build/cache dirs"
        elif p.name in EXCLUDE_FILES or p.suffix.lower() in EXCLUDE_EXT:
            reason = "cache/vcs files"
        elif parts[0] == "evals" and not with_evals:
            reason = "evals (dev-only)"
        elif lite and p.suffix.lower() in MEDIA_EXT:
            reason = "media (--lite)"
        elif p.is_symlink():
            reason = "symlinks"
        if reason:
            skipped.setdefault(reason, []).append(relp)
        else:
            keep.append(relp)
    return keep, skipped


def target_path(out: str, lite: bool) -> Path:
    fname = f"{NAME}{'-lite' if lite else ''}.skill"
    if not out:
        return SK / "dist" / fname
    o = Path(out).expanduser()
    if o.suffix.lower() in (".skill", ".zip"):
        return o
    return o / fname


def run_checks() -> int:
    sys.path.insert(0, str(HERE))
    try:
        import check_skill
    except ImportError as e:
        print(f"check_skill.py not importable ({e}); packaging without validation", file=sys.stderr)
        return 0
    print("validating with scripts/check_skill.py …")
    return check_skill.main([])


def upload_skill_md(text: str):
    """SKILL.md for claude.ai: description := claude_ai_description (≤200 chars). Returns (text, error)."""
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not m:
        return text, "SKILL.md has no frontmatter"
    lines = m.group(1).splitlines()
    short = next((ln.split(":", 1)[1].strip() for ln in lines if ln.startswith("claude_ai_description:")), "")
    if len(short) >= 2 and short[0] == short[-1] and short[0] in "\"'":
        short = short[1:-1]
    if not short:
        desc = next((ln.split(":", 1)[1].strip() for ln in lines if ln.startswith("description:")), "")
        if len(desc) <= DESC_MAX:
            return text, None
        return text, f"description is {len(desc)} chars; claude.ai allows {DESC_MAX} — add claude_ai_description to the frontmatter"
    if len(short) > DESC_MAX:
        return text, f"claude_ai_description is {len(short)} chars (max {DESC_MAX})"
    out = []
    for ln in lines:
        if ln.startswith("claude_ai_description:"):
            continue
        if ln.startswith("description:"):
            ln = "description: " + short
        out.append(ln)
    return "---\n" + "\n".join(out) + "\n---\n" + text[m.end():], None


def build(dest: Path, files) -> int:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.name + ".tmp")
    total = 0
    with zipfile.ZipFile(str(tmp), "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for relp in files:
            src = SK / relp
            data = src.read_bytes()
            if relp.as_posix() == "SKILL.md":
                data = upload_skill_md(data.decode("utf-8"))[0].encode("utf-8")
            total += len(data)
            info = zipfile.ZipInfo(f"{NAME}/{relp.as_posix()}", date_time=FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            mode = 0o755 if (relp.parts[0] == "scripts" and src.suffix in (".py", ".sh")) or os.access(str(src), os.X_OK) else 0o644
            info.external_attr = (0o100000 | mode) << 16
            z.writestr(info, data, compresslevel=9)
    os.replace(str(tmp), str(dest))
    return total


def verify(dest: Path) -> list:
    problems = []
    with zipfile.ZipFile(str(dest)) as z:
        bad = z.testzip()
        if bad:
            problems.append(f"corrupt entry {bad}")
        names = z.namelist()
        tops = {n.split("/")[0] for n in names}
        if tops != {NAME}:
            problems.append(f"top-level entries {sorted(tops)} (expected only {NAME}/)")
        if f"{NAME}/SKILL.md" not in names:
            problems.append("SKILL.md is not at the top of the skill folder")
        extra = [n for n in names if n.endswith("/SKILL.md") and n != f"{NAME}/SKILL.md"]
        if extra:
            problems.append(f"nested SKILL.md files would be rejected on upload: {extra}")
    return problems


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Zip the skill for claude.ai upload")
    ap.add_argument("-o", "--out", default="", help="output folder or file (.skill/.zip); default dist/ inside the skill")
    ap.add_argument("--lite", action="store_true", help="leave out images, audio and video (all text and fonts stay)")
    ap.add_argument("--with-evals", action="store_true", help="include evals/")
    ap.add_argument("--no-check", action="store_true", help="skip check_skill.py validation")
    ap.add_argument("--list", action="store_true", help="list the files that would be packed and exit")
    a = ap.parse_args(argv)
    files, skipped = collect(a.lite, a.with_evals)
    if a.list:
        for f in files:
            print(f.as_posix())
        print(f"{len(files)} files · skipped: " + (", ".join(f"{k} {len(v)}" for k, v in skipped.items()) or "none"))
        return 0
    if not (SK / "SKILL.md").is_file():
        print("SKILL.md not found — nothing to package", file=sys.stderr)
        return 1
    if not a.no_check and run_checks() != 0:
        print("package_skill: validation failed — fix the errors above or pass --no-check", file=sys.stderr)
        return 1
    dest = target_path(a.out, a.lite)
    try:
        inside = dest.resolve().relative_to(SK.resolve())
    except ValueError:
        inside = None
    if inside is not None and inside.parts[0] != "dist":
        print(f"package_skill: {dest} is inside the skill folder; write to dist/ or a folder outside it", file=sys.stderr)
        return 1
    _t, derr = upload_skill_md((SK / "SKILL.md").read_text(encoding="utf-8"))
    if derr:
        print(f"package_skill: {derr}", file=sys.stderr)
        return 1
    raw = build(dest, files)
    problems = verify(dest)
    size = dest.stat().st_size
    print(f"wrote {dest}")
    print(f"  {len(files)} files · {human(raw)} unpacked · {human(size)} zipped" + (" · lite" if a.lite else ""))
    if skipped:
        print("  skipped: " + ", ".join(f"{k} {len(v)}" for k, v in skipped.items()))
    print(f"  upload: claude.ai → Customize → Skills → upload {dest.name} (rename to .zip if the picker asks for one)")
    print(f"  packaged SKILL.md uses the short claude.ai description (≤{DESC_MAX} chars); no size cap is documented — "
          "if the upload refuses the file, rebuild with --lite")
    for p in problems:
        print(f"  PROBLEM: {p}", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (AttributeError, ValueError, ImportError):
        pass
    sys.exit(main())
