#!/usr/bin/env python3
"""Black Dragon: real, optional 12-tool video dependency bridge (no fake execution claims).

Installations happen on the machine where this command is run, NOT on GitHub.
`doctor` means module/binary resolution, not a successful render.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REGISTRY = json.loads((HERE / "registry.json").read_text(encoding="utf-8"))
TOOLS = {entry["id"]: entry for entry in REGISTRY["tools"]}
PIP_MODULES = {"manim": "manim", "whisperx": "whisperx", "auto-editor": "auto_editor"}
CLI_TOOLS = {"remotion", "hyperframes", "manim", "whisperx", "auto-editor", "ffmpeg"}


def python_exe() -> Path:
    candidate = HERE / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    return candidate if candidate.is_file() else Path(sys.executable)


def pip_cli(name: str) -> str | None:
    directory = HERE / ".venv" / ("Scripts" if os.name == "nt" else "bin")
    candidate = directory / (name + (".exe" if os.name == "nt" else ""))
    return str(candidate) if candidate.is_file() else shutil.which(name)


def node_cli(name: str) -> str | None:
    candidate = HERE / "node_modules" / ".bin" / (name + (".cmd" if os.name == "nt" else ""))
    return str(candidate) if candidate.is_file() else None


def run_capture(cmd: list[str], timeout: int = 20) -> str | None:
    try:
        return subprocess.run(cmd, cwd=HERE, capture_output=True, text=True, timeout=timeout, check=True).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None


def node_packages() -> dict[str, bool]:
    names = sorted({name for tool in TOOLS.values()
                    if tool["manager"] in {"npm", "system-or-npm"}
                    for name in tool["packages"]})
    if not shutil.which("node"):
        return {name: False for name in names}
    js = ("const r=require('module').createRequire(process.cwd()+'/package.json');"
          "const names=" + json.dumps(names) + ";"
          "console.log(JSON.stringify(Object.fromEntries(names.map(n=>"
          "[n,(()=>{try{return !!r.resolve(n)}catch{return false}})()]))));")
    output = run_capture(["node", "-e", js])
    try:
        return json.loads(output or "")
    except (ValueError, TypeError):
        return {name: False for name in names}


def python_modules() -> dict[str, bool]:
    names = list(PIP_MODULES.values())
    code = ("import importlib.util,json; names=" + repr(names) +
            "; print(json.dumps({n:importlib.util.find_spec(n) is not None for n in names}))")
    output = run_capture([str(python_exe()), "-c", code])
    try:
        return json.loads(output or "")
    except (ValueError, TypeError):
        return {name: False for name in names}


def bundled_binary(package: str) -> str | None:
    if not shutil.which("node"):
        return None
    code = "try{console.log(require(" + json.dumps(package) + ").path)}catch(e){process.exit(1)}"
    output = run_capture(["node", "-e", code])
    return output if output and Path(output).is_file() else None


def binary(name: str) -> str | None:
    found = shutil.which(name)
    if found:
        return found
    if name == "ffmpeg":
        return bundled_binary("@ffmpeg-installer/ffmpeg")
    if name == "ffprobe":
        return bundled_binary("@ffprobe-installer/ffprobe")
    return None


def doctor() -> dict:
    npm = node_packages()
    pip = python_modules()
    ff = bool(binary("ffmpeg") and binary("ffprobe"))
    rows = []
    for entry in REGISTRY["tools"]:
        manager = entry["manager"]
        if manager == "npm":
            ready = all(npm.get(pkg, False) for pkg in entry["packages"])
        elif manager == "pip":
            ready = pip.get(PIP_MODULES[entry["id"]], False)
        else:
            ready = ff
        rows.append({"id": entry["id"], "phase": entry["phase"], "available": bool(ready),
                     "manager": manager, "packages": entry["packages"]})
    return {"schema": REGISTRY["schema"], "dependency_resolution_only": True,
            "node": bool(shutil.which("node")), "npm": bool(shutil.which("npm")),
            "python": str(python_exe()), "ffmpeg_and_ffprobe": ff,
            "available_count": sum(x["available"] for x in rows),
            "total_count": len(rows), "tools": rows}


def plan(task: str) -> dict:
    s = task.lower()
    selected = ["remotion", "gsap", "ffmpeg"]
    def pick(key: str, *keywords: str):
        if any(k in s for k in keywords) and key not in selected:
            selected.append(key)
    pick("hyperframes", "html", "ويب", "تفاعلي", "seek", "hyperframes")
    pick("motion-canvas", "موشن", "motion canvas", "timing", "توقيت")
    pick("threejs", "3d", "ثلاثي", "بلندر", "three")
    pick("manim", "معادلة", "رياض", "mathemat", "equation", "manim")
    pick("roughjs", "يدوي", "مرسوم", "سبورة", "handdraw", "rough")
    pick("animejs", "anime", "نص متحرك", "kinetic")
    pick("mojs", "particles", "جزيئات", "انفجار", "burst")
    pick("whisperx", "صوت", "كلام", "تعليق", "تفريغ", "captions", "subtitle", "voice")
    pick("auto-editor", "صمت", "سكتات", "توقفات", "silence", "autocut", "pause")
    return {"task": task, "recommended": selected,
            "available_in_catalog": list(TOOLS),
            "execution_status": "planning_only",
            "stages": ["brief", "concept", "color-design", "shots", "produce", "qa-color", "deliver"],
            "constraints": ["Follow existing video_protocol.py CORE receipts and delivery gates",
                            "Do not claim any dependency executed until a real command succeeds",
                            "For auto-editor, retain natural pauses and manually review cuts",
                            "Confirm Remotion license eligibility; do not auto-buy licenses",
                            "Prefer WhisperX GPU when available; models may need separate downloads"]}


def install(args) -> int:
    selected = [x for x in ("node", "python") if getattr(args, x) or args.all]
    if not selected:
        print("Choose --all, --node or --python. No changes made.", file=sys.stderr)
        return 2
    commands = []
    if "node" in selected:
        if not shutil.which("npm"):
            print("npm/Node.js missing. Install Node.js first.", file=sys.stderr)
            return 2
        commands.append(["npm", "install", "--no-audit", "--no-fund"])
    if "python" in selected:
        venv = HERE / ".venv"
        if not python_exe().is_relative_to(venv):
            commands.append([sys.executable, "-m", "venv", str(venv)])
        pip = venv / ("Scripts/pip.exe" if os.name == "nt" else "bin/pip")
        commands.append([str(pip), "install", "-r", str(HERE / "requirements.txt")])
    print(json.dumps({"cwd": str(HERE), "commands": commands,
                      "note": "FFmpeg/ffprobe provided by bundled npm packages when system binaries are absent."},
                     ensure_ascii=False, indent=2))
    if args.dry_run:
        return 0
    if not args.yes:
        print("Add --yes to authorize downloads/installer scripts on this machine.", file=sys.stderr)
        return 2
    for command in commands:
        print("RUN:", " ".join(command), flush=True)
        try:
            subprocess.run(command, cwd=HERE, check=True)
        except (OSError, subprocess.CalledProcessError) as exc:
            print(f"Installation failed: {exc}", file=sys.stderr)
            return 1
    return 0


def execute(tool_id: str, args: list[str]) -> int:
    if tool_id not in CLI_TOOLS:
        print(f"{tool_id} is a JS library, not a standalone CLI; import it from node_modules.", file=sys.stderr)
        return 2
    cli = {"remotion": node_cli("remotion"), "hyperframes": node_cli("hyperframes"),
           "manim": pip_cli("manim"), "whisperx": pip_cli("whisperx"),
           "auto-editor": pip_cli("auto-editor"), "ffmpeg": binary("ffmpeg")}[tool_id]
    if not cli:
        print(f"{tool_id} CLI not installed on this worker. Run doctor/install.", file=sys.stderr)
        return 2
    if args and args[0] == "--":
        args = args[1:]
    if not args:
        print("Supply the real CLI arguments after --; refusing empty execution.", file=sys.stderr)
        return 2
    try:
        return subprocess.run([cli, *args], cwd=HERE, check=False).returncode
    except OSError as exc:
        print(f"Unable to execute: {exc}", file=sys.stderr)
        return 1


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Black Dragon Instagram Reel 12 video toolchain")
    sub = p.add_subparsers(dest="action", required=True)
    dr = sub.add_parser("doctor", help="Detect local libraries and executables (no execution proof)")
    dr.add_argument("--json", action="store_true")
    pl = sub.add_parser("plan", help="Select tools using keywords; no execution")
    pl.add_argument("task")
    ins = sub.add_parser("install", help="Opt-in install on THIS machine")
    ins.add_argument("--all", action="store_true")
    ins.add_argument("--node", action="store_true")
    ins.add_argument("--python", action="store_true")
    ins.add_argument("--yes", action="store_true")
    ins.add_argument("--dry-run", action="store_true")
    ex = sub.add_parser("run", help="Run supported, installed CLIs using explicit arguments")
    ex.add_argument("tool", choices=sorted(TOOLS))
    ex.add_argument("args", nargs=argparse.REMAINDER)
    args = p.parse_args(argv)
    if args.action == "doctor":
        value = doctor()
        if args.json:
            print(json.dumps(value, ensure_ascii=False, indent=2))
        else:
            for row in value["tools"]:
                print(f"{'READY' if row['available'] else 'MISSING':7} {row['id']:16} {row['manager']}")
            print(f"Detected {value['available_count']}/{value['total_count']} dependencies; not render-tested.")
        return 0
    if args.action == "plan":
        print(json.dumps(plan(args.task), ensure_ascii=False, indent=2))
        return 0
    if args.action == "install":
        return install(args)
    if args.action == "run":
        return execute(args.tool, args.args)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
