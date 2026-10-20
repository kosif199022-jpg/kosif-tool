#!/usr/bin/env python3
"""KOSIF background Blender MP4 export; verified frame count and H.264.

No arbitrary code, external .blend, browser downloads, license bypass, or shell.
This requires the user's installed Blender and FFmpeg, not the KOSIF native renderer.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from blender_bridge import blender_exe, validate

def discover_blender(executable=None):
    if executable:
        return blender_exe(executable)
    on_path = blender_exe()
    if on_path:
        return on_path
    # User-scoped verified official portable release on the KOSIF Windows host.
    portable = (Path.home() / "KOSIF-Tools" / "Blender5.2" /
                "blender-5.2.2-windows-x64" / "blender.exe")
    if portable.is_file():
        return str(portable.resolve())
    return None

def encode(scene_file, output_file, blender=None, timeout=300):
    src = Path(scene_file).resolve(strict=True)
    scene = validate(json.loads(src.read_text(encoding="utf-8-sig")))
    dest = Path(output_file).resolve()
    if dest.suffix.lower() != ".mp4":
        raise ValueError("MP4 only")
    if dest.exists():
        raise ValueError("refusing to overwrite output")
    if not dest.parent.is_dir():
        raise ValueError("output directory missing")
    exe = discover_blender(blender)
    ffmpeg = shutil.which("ffmpeg")
    ffprobe = shutil.which("ffprobe")
    if not exe or not ffmpeg or not ffprobe:
        raise ValueError("Blender, FFmpeg and FFprobe are required; no implicit installation")
    worker = Path(__file__).with_name("blender_worker.py").resolve(strict=True)
    fps, count = scene.get("fps", 24), scene.get("frames", 1)
    with tempfile.TemporaryDirectory(prefix="kosif-blender-motion-") as tmp:
        root = Path(tmp)
        frames = root / "frames.frames"
        movie = root / "render.mp4"
        cmd = [exe, "--background", "--factory-startup", "--disable-autoexec",
               "--python-exit-code", "3", "--python", str(worker),
               "--", str(src), str(frames)]
        try:
            run = subprocess.run(cmd, shell=False, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            raise ValueError("Blender animation timed out") from exc
        if run.returncode != 0:
            raise ValueError("Blender animation failed: " + run.stderr[-500:])
        found = list(frames.glob("frame_*.png"))
        if len(found) != count:
            raise ValueError("incomplete frame sequence: %s of %s" % (len(found), count))
        command = [ffmpeg, "-hide_banner", "-loglevel", "error", "-nostdin",
                   "-framerate", str(fps), "-start_number", "1",
                   "-i", str(frames / "frame_%04d.png"),
                   "-frames:v", str(count), "-c:v", "libx264",
                   "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(movie)]
        encoded = subprocess.run(command, shell=False, capture_output=True, text=True, timeout=timeout)
        if encoded.returncode != 0:
            raise ValueError("FFmpeg failed: " + encoded.stderr[-500:])
        verified = subprocess.run([ffprobe, "-v", "error", "-count_frames",
                   "-select_streams", "v:0",
                   "-show_entries", "stream=codec_name,nb_read_frames,width,height,r_frame_rate",
                   "-of", "json", str(movie)],
                   shell=False, check=True, capture_output=True, text=True, timeout=30)
        streams = json.loads(verified.stdout)["streams"]
        if len(streams) != 1 or streams[0].get("codec_name") != "h264":
            raise ValueError("video codec verification failed")
        if int(streams[0].get("nb_read_frames", -1)) != count:
            raise ValueError("video frame count verification failed")
        if (streams[0].get("width"), streams[0].get("height")) != tuple(scene.get("size", [512, 512])):
            raise ValueError("video dimensions verification failed")
        if dest.exists():
            raise ValueError("destination appeared during rendering")
        shutil.copyfile(movie, dest)
    return {"success": True, "engine": "Blender+FFmpeg",
            "frames": count, "fps": fps, "seconds": count / fps,
            "width": streams[0]["width"], "height": streams[0]["height"],
            "output": str(dest), "size": dest.stat().st_size,
            "sha256": hashlib.sha256(dest.read_bytes()).hexdigest()}

def main():
    p = argparse.ArgumentParser(description="KOSIF safe Blender-to-MP4 motion export")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("doctor")
    r = sub.add_parser("render")
    r.add_argument("--scene", required=True)
    r.add_argument("--output", required=True)
    r.add_argument("--blender")
    args = p.parse_args()
    try:
        if args.cmd == "doctor":
            print(json.dumps({"blender": bool(discover_blender()),
                "ffmpeg": bool(shutil.which("ffmpeg")),
                "ffprobe": bool(shutil.which("ffprobe")),
                "formats": ["mp4"], "auto_installs": False}))
        else:
            print(json.dumps(encode(args.scene, args.output, args.blender)))
        return 0
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError,
            json.JSONDecodeError) as e:
        print(json.dumps({"success": False, "error": str(e)}), file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
