#!/usr/bin/env python3
"""KOSIF original safe Blender command adapter; no automatic download or installation."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys

SCHEMA = "kosif.blender.v1"
FORMATS = {".png", ".blend", ".glb"}
SHAPES = {"cube", "sphere", "cylinder", "cone", "torus"}


def vector(value, bound=100):
    if not isinstance(value, list) or len(value) != 3:
        raise ValueError("expected 3-element vector")
    if any(type(x) not in (int, float) or not math.isfinite(x) or abs(x) > bound for x in value):
        raise ValueError("invalid vector coordinate")
    return [float(x) for x in value]


def validate(scene):
    if not isinstance(scene, dict) or scene.get("schema") != SCHEMA:
        raise ValueError("unsupported Blender scene schema")
    size = scene.get("size", [512, 512])
    if (not isinstance(size, list) or len(size) != 2 or
            any(type(v) is not int or not 128 <= v <= 1920 for v in size)):
        raise ValueError("invalid render size")
    fps, frames = scene.get("fps", 24), scene.get("frames", 1)
    if type(fps) is not int or not 1 <= fps <= 60:
        raise ValueError("invalid fps")
    if type(frames) is not int or not 1 <= frames <= 240:
        raise ValueError("invalid frame count")
    objects = scene.get("objects", [])
    if not isinstance(objects, list) or not 1 <= len(objects) <= 12:
        raise ValueError("1-12 objects required")
    for item in objects:
        if not isinstance(item, dict) or item.get("shape") not in SHAPES:
            raise ValueError("unsupported shape")
        vector(item.get("location", [0, 0, 0]))
        vector(item.get("scale", [1, 1, 1]), 20)
        if "color" in item:
            c = item["color"]
            if not isinstance(c, list) or len(c) != 4 or any(type(x) not in (int, float) or not math.isfinite(x) or not 0 <= x <= 1 for x in c):
                raise ValueError("invalid RGBA color")
        keys = item.get("keyframes", [])
        if not isinstance(keys, list) or len(keys) > 24:
            raise ValueError("too many keyframes")
        last = 0
        for key in keys:
            if not isinstance(key, dict) or type(key.get("frame")) is not int or not last < key["frame"] <= frames:
                raise ValueError("keyframes must be ordered and within scene frames")
            vector(key.get("location"))
            last = key["frame"]
    return scene


def blender_exe(spec=None):
    if spec:
        path = Path(spec).expanduser()
        if not path.is_file():
            raise ValueError("Blender executable does not exist")
        return str(path.resolve())
    return shutil.which("blender")


def render(scene_path, output_path, executable=None, timeout=180):
    scene_file = Path(scene_path).resolve(strict=True)
    scene = validate(json.loads(scene_file.read_text(encoding="utf-8-sig")))
    dest = Path(output_path).resolve()
    if dest.suffix.lower() not in FORMATS:
        raise ValueError("output must be PNG, BLEND, or GLB")
    if dest.exists():
        raise ValueError("refusing to overwrite output")
    if not dest.parent.is_dir():
        raise ValueError("output directory missing")
    blender = blender_exe(executable)
    if not blender:
        raise ValueError("Blender not installed; no download or replacement renderer attempted")
    worker = Path(__file__).with_name("blender_worker.py").resolve(strict=True)
    cmd = [blender, "--background", "--factory-startup", "--disable-autoexec",
           "--python-exit-code", "3", "--python", str(worker), "--",
           str(scene_file), str(dest)]
    try:
        result = subprocess.run(cmd, check=False, capture_output=True, text=True,
                                timeout=timeout, shell=False)
    except subprocess.TimeoutExpired as exc:
        raise ValueError("Blender render timed out") from exc
    if result.returncode != 0:
        raise ValueError("Blender failed (exit %s): %s" % (result.returncode, result.stderr[-350:]))
    if not dest.is_file() or dest.stat().st_size < 24:
        raise ValueError("Blender returned without a valid output")
    return {"executed": True, "verified_file": True, "engine": "Blender",
            "format": dest.suffix.lower()[1:], "bytes": dest.stat().st_size,
            "sha256": hashlib.sha256(dest.read_bytes()).hexdigest(),
            "object_count": len(scene["objects"]), "output": str(dest)}


def main():
    p = argparse.ArgumentParser(description="KOSIF Blender independent integration")
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor")
    cmd = sub.add_parser("render")
    cmd.add_argument("--scene", required=True)
    cmd.add_argument("--output", required=True)
    cmd.add_argument("--blender")
    args = p.parse_args()
    try:
        if args.command == "doctor":
            exe = blender_exe()
            result = {"blender_installed": bool(exe), "path": exe, "formats": sorted(FORMATS),
                      "user_code_loaded": False, "automatically_installs": False,
                      "render_verified": False}
        else:
            result = render(args.scene, args.output, args.blender)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"executed": False, "error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
