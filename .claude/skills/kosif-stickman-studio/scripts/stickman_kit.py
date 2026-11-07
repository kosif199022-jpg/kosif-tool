#!/usr/bin/env python3
"""stickman_kit.py: inspect and install the GrowKaz Stickman studio from the owner's own plugin file.

The GrowKaz kit (renderer, engine, tools, audio) is not in this repository: it has a named
author and no licence, and the repo is public. The owner keeps the original
`GrowKaz_Stickman.plugin` (a zip) privately and this script installs it from there.

  python3 stickman_kit.py inspect  PLUGIN [--json]          what is inside, and anything risky
  python3 stickman_kit.py install  PLUGIN --dest DIR [--force-kit]
  python3 stickman_kit.py status   --dest DIR [--json]      is a studio installed there, and which version
  python3 stickman_kit.py self-test [--out DIR]             known-answer test on a synthetic plugin

Safety: reads the zip without running anything in it; refuses absolute paths, `..`, symlinks
and files over 50 MB; flags hooks, MCP servers, slash-command shell lines and network calls.
Install copies only `skills/make-2d-video/kit/` and never overwrites `projects/`.
Pure standard library, no network.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

KIT_PREFIX = "skills/make-2d-video/kit/"
MAX_FILE = 50 * 1024 * 1024
MARKER = ".kosif-stickman.json"
RISKY_PATHS = (
    (re.compile(r"(^|/)hooks?(/|\.json$)"), "hook definition: runs on Claude Code events"),
    (re.compile(r"(^|/)\.mcp\.json$"), "MCP server definition"),
    (re.compile(r"(^|/)commands/.*\.md$"), "slash command"),
    (re.compile(r"(^|/)agents/.*\.md$"), "subagent definition"),
    (re.compile(r"\.(exe|dll|so|dylib|bat|cmd|ps1|sh)$"), "native or shell executable"),
)
RISKY_TEXT = (
    (re.compile(r"\bcurl\b[^\n]*\|\s*(sudo\s+)?(ba)?sh"), "pipes a download into a shell"),
    (re.compile(r"\beval\s*\("), "eval()"),
    (re.compile(r"shell\s*=\s*True"), "subprocess with shell=True"),
    (re.compile(r"\brm\s+-rf\s+[/~]"), "rm -rf on a root or home path"),
    (re.compile(r"https?://(?!localhost|127\.0\.0\.1)[\w.-]+"), "remote URL"),
)
TEXT_EXT = {".py", ".js", ".mjs", ".cjs", ".json", ".md", ".html", ".sh", ".txt"}


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _safe_name(name: str) -> str | None:
    p = PurePosixPath(name)
    if name.startswith(("/", "\\")) or p.is_absolute() or ".." in p.parts or re.match(r"^[A-Za-z]:", name):
        return None
    return str(p)


def _is_symlink(info: zipfile.ZipInfo) -> bool:
    return stat.S_ISLNK(info.external_attr >> 16)


def inspect(plugin: Path) -> dict:
    report = {"schema": "kosif.stickman.inspect.v1", "plugin": str(plugin), "sha256": _sha(plugin.read_bytes()),
              "manifest": None, "skills": [], "kit_files": 0, "files": 0, "bytes": 0,
              "license_files": [], "refused": [], "flags": []}
    with zipfile.ZipFile(plugin) as z:
        for info in z.infolist():
            if info.is_dir():
                continue
            name = _safe_name(info.filename)
            if name is None:
                report["refused"].append({"path": info.filename, "why": "absolute or parent path"})
                continue
            if _is_symlink(info):
                report["refused"].append({"path": name, "why": "symlink"})
                continue
            if info.file_size > MAX_FILE:
                report["refused"].append({"path": name, "why": f"over {MAX_FILE} bytes"})
                continue
            report["files"] += 1
            report["bytes"] += info.file_size
            if name.startswith(KIT_PREFIX):
                report["kit_files"] += 1
            if re.search(r"(^|/)(LICEN[CS]E|COPYING|NOTICE)", name, re.I):
                report["license_files"].append(name)
            m = re.match(r"skills/([^/]+)/SKILL\.md$", name)
            if m:
                report["skills"].append(m.group(1))
            for rx, why in RISKY_PATHS:
                if rx.search(name):
                    report["flags"].append({"path": name, "why": why})
            data = z.read(info)
            if name == ".claude-plugin/plugin.json":
                try:
                    report["manifest"] = json.loads(data.decode("utf-8"))
                except ValueError:
                    report["flags"].append({"path": name, "why": "manifest is not valid JSON"})
            if Path(name).suffix in TEXT_EXT and not name.endswith(".md"):
                text = data.decode("utf-8", "replace")
                for rx, why in RISKY_TEXT:
                    for hit in rx.finditer(text):
                        line = text.count("\n", 0, hit.start()) + 1
                        report["flags"].append({"path": name, "line": line, "why": why, "match": hit.group(0)[:80]})
    report["skills"].sort()
    report["has_kit"] = report["kit_files"] > 0
    report["license"] = (report["manifest"] or {}).get("license") or (report["license_files"] or None)
    return report


def install(plugin: Path, dest: Path, force_kit: bool = False) -> dict:
    rep = inspect(plugin)
    if not rep["has_kit"]:
        raise SystemExit(f"no {KIT_PREFIX} inside {plugin}: not a GrowKaz Stickman plugin")
    dest = dest.resolve()
    marker = dest / MARKER
    if (dest / "render.mjs").exists() and not force_kit:
        return {"schema": "kosif.stickman.install.v1", "dest": str(dest), "installed": False,
                "reason": "already installed (use --force-kit to refresh the kit; projects/ is never touched)",
                "status": status(dest)}
    written = []
    with zipfile.ZipFile(plugin) as z:
        for info in z.infolist():
            name = _safe_name(info.filename)
            if info.is_dir() or name is None or _is_symlink(info) or info.file_size > MAX_FILE:
                continue
            if not name.startswith(KIT_PREFIX):
                continue
            rel = PurePosixPath(name[len(KIT_PREFIX):])
            if not rel.parts or rel.parts[0] == "projects":
                continue
            target = (dest / Path(*rel.parts)).resolve()
            if dest not in target.parents:
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            data = z.read(info)
            target.write_bytes(data)
            written.append({"path": str(rel), "sha256": _sha(data)})
    (dest / "projects").mkdir(parents=True, exist_ok=True)
    marker.write_text(json.dumps({"schema": "kosif.stickman.kit.v1", "plugin_sha256": rep["sha256"],
                                  "version": (rep["manifest"] or {}).get("version"),
                                  "files": written}, indent=1, ensure_ascii=False), encoding="utf-8")
    return {"schema": "kosif.stickman.install.v1", "dest": str(dest), "installed": True,
            "files": len(written), "version": (rep["manifest"] or {}).get("version"),
            "flags": rep["flags"], "next": [f"cd {dest}", "npm install", "python3 tools/verify_kit.py",
                                            "python3 tools/doctor.py"]}


def status(dest: Path) -> dict:
    dest = dest.resolve()
    marker = dest / MARKER
    out = {"schema": "kosif.stickman.status.v1", "dest": str(dest), "installed": (dest / "render.mjs").exists()}
    if marker.exists():
        m = json.loads(marker.read_text(encoding="utf-8"))
        changed = [f["path"] for f in m["files"]
                   if not (dest / f["path"]).exists() or _sha((dest / f["path"]).read_bytes()) != f["sha256"]]
        out.update(version=m.get("version"), plugin_sha256=m.get("plugin_sha256"), files=len(m["files"]),
                   changed=changed)
    out["projects"] = sorted(p.name for p in (dest / "projects").iterdir() if p.is_dir()) if (dest / "projects").is_dir() else []
    return out


def self_test(out: Path) -> dict:
    """Build a small fake plugin with one good kit file, one path-escape, one symlink and one hook; check the
    inspector and installer handle each one."""
    out.mkdir(parents=True, exist_ok=True)
    plug = out / "fake.plugin"
    with zipfile.ZipFile(plug, "w") as z:
        z.writestr(".claude-plugin/plugin.json", json.dumps({"name": "fake", "version": "9.9.9"}))
        z.writestr("skills/make-2d-video/SKILL.md", "---\nname: make-2d-video\n---\n")
        z.writestr("skills/new-video/SKILL.md", "---\nname: new-video\n---\n")
        z.writestr(KIT_PREFIX + "render.mjs", "// renderer\n")
        z.writestr(KIT_PREFIX + "tools/doctor.py", "import subprocess\nsubprocess.run('x', shell=True)\n")
        z.writestr(KIT_PREFIX + "projects/demo/config.json", "{}")
        z.writestr("../escape.txt", "bad")
        link = zipfile.ZipInfo(KIT_PREFIX + "link")
        link.external_attr = (stat.S_IFLNK | 0o777) << 16
        z.writestr(link, "/etc/passwd")
        z.writestr("hooks/hooks.json", "{}")
    rep = inspect(plug)
    dest = out / "studio"
    (dest / "projects" / "mine").mkdir(parents=True, exist_ok=True)
    (dest / "projects" / "mine" / "keep.txt").write_text("user work", encoding="utf-8")
    first = install(plug, dest)
    second = install(plug, dest)
    st = status(dest)
    checks = [
        ("manifest version read", rep["manifest"] == {"name": "fake", "version": "9.9.9"}),
        ("two skills found", rep["skills"] == ["make-2d-video", "new-video"]),
        ("parent path refused", any(r["path"] == "../escape.txt" for r in rep["refused"])),
        ("symlink refused", any(r["why"] == "symlink" for r in rep["refused"])),
        ("hook flagged", any("hook" in f["why"] for f in rep["flags"])),
        ("shell=True flagged with its line", any(f["why"].startswith("subprocess") and f.get("line") == 2 for f in rep["flags"])),
        ("no licence found", rep["license"] is None),
        ("install wrote 2 kit files", first["installed"] and first["files"] == 2),
        ("bundled projects/ skipped", not (dest / "projects" / "demo").exists()),
        ("user's projects/ kept", (dest / "projects" / "mine" / "keep.txt").read_text(encoding="utf-8") == "user work"),
        ("nothing escaped dest", not (out / "escape.txt").exists() and not (dest / "link").exists()),
        ("second install is a no-op", second["installed"] is False),
        ("status sees version and no changes", st["version"] == "9.9.9" and st["changed"] == [] and st["projects"] == ["mine"]),
    ]
    result = {"schema": "kosif.stickman.selftest.v1", "passed": all(ok for _, ok in checks),
              "checks": [{"name": n, "passed": ok} for n, ok in checks]}
    (out / "selftest.json").write_text(json.dumps(result, indent=1), encoding="utf-8")
    return result


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("inspect"); a.add_argument("plugin", type=Path); a.add_argument("--json", action="store_true")
    b = sub.add_parser("install"); b.add_argument("plugin", type=Path); b.add_argument("--dest", type=Path, required=True)
    b.add_argument("--force-kit", action="store_true")
    c = sub.add_parser("status"); c.add_argument("--dest", type=Path, required=True); c.add_argument("--json", action="store_true")
    d = sub.add_parser("self-test"); d.add_argument("--out", type=Path)
    args = ap.parse_args(argv)
    if args.cmd == "inspect":
        rep = inspect(args.plugin)
        if args.json:
            print(json.dumps(rep, indent=1, ensure_ascii=False))
        else:
            m = rep["manifest"] or {}
            print(f"{m.get('name')} {m.get('version')}  ({rep['files']} files, {rep['kit_files']} in the kit)")
            print("skills:", ", ".join(rep["skills"]) or "none")
            print("licence:", rep["license"] or "none found")
            for r in rep["refused"]:
                print(f"REFUSED {r['path']}: {r['why']}")
            for f in rep["flags"]:
                print(f"FLAG {f['path']}{':' + str(f['line']) if 'line' in f else ''}: {f['why']}")
        return 0
    if args.cmd == "install":
        print(json.dumps(install(args.plugin, args.dest, args.force_kit), indent=1, ensure_ascii=False))
        return 0
    if args.cmd == "status":
        print(json.dumps(status(args.dest), indent=1, ensure_ascii=False))
        return 0
    with tempfile.TemporaryDirectory() as tmp:
        res = self_test(args.out or Path(tmp))
        for c in res["checks"]:
            print(("PASS " if c["passed"] else "FAIL ") + c["name"])
        print("self-test:", "PASS" if res["passed"] else "FAIL")
        return 0 if res["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
