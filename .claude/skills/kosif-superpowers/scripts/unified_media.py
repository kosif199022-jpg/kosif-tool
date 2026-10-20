#!/usr/bin/env python3
"""KOSIF Unified Media: App Studio photo effects + Unified Draw 2D layers + video.

Works on user-authorized local imagery. Only named photo operations are allowed.
Does not copy or inspect proprietary Photoshop files. This is not photorealistic 3D.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageOps
from creative_paint import paint
from unified_draw import compile_scene

PHOTO_EXT = {".jpg", ".jpeg", ".png", ".webp"}
OUTPUT_EXT = {".png", ".gif", ".mp4"}
FILTERS = {"none", "develop", "ink-sketch", "pencil-sketch"}
MAX_PIXELS = 32_000_000
MAX_FRAMES = 300
HERE = Path(__file__).resolve().parent


def checked_image(path):
    src = Path(path)
    if not src.is_file() or src.suffix.lower() not in PHOTO_EXT:
        raise ValueError("photo must be an existing local JPG, PNG or WebP")
    if src.stat().st_size > 30_000_000:
        raise ValueError("photo exceeds 30 MB input limit")
    with Image.open(src) as image:
        if image.width * image.height > MAX_PIXELS:
            raise ValueError("photo exceeds 32 megapixels")
        return ImageOps.exif_transpose(image).convert("RGBA")


def processed_photo(src, effect, exposure=0.0):
    if effect == "none":
        return checked_image(src)
    if effect not in FILTERS:
        raise ValueError("unsupported photo effect")
    if not isinstance(exposure, (int, float)) or isinstance(exposure, bool) or not math.isfinite(exposure) or not -2 <= exposure <= 2:
        raise ValueError("exposure must be finite, between -2 and 2 EV")
    with tempfile.TemporaryDirectory(prefix="kosif-app-studio-") as td:
        target = Path(td) / "developed.png"
        cmd = [sys.executable, str(HERE/"app_studio.py"), effect, str(src),
               "-o", str(target)]
        if effect == "develop":
            cmd.extend(["--set", f"exposure={exposure}"])
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=90,
                                encoding="utf-8", errors="replace")
        if result.returncode != 0 or not target.is_file():
            raise ValueError("App Studio photo adjustment failed: " + result.stdout[:260] + result.stderr[:260])
        return checked_image(target)


def validate_job(photo, data, output, effect="none", exposure=0.0, fps=12, duration=2):
    target = Path(output)
    if target.suffix.lower() not in OUTPUT_EXT:
        raise ValueError("supported outputs: PNG, GIF, MP4")
    if not target.parent.is_dir() or target.exists():
        raise ValueError("output folder must exist and output must not overwrite an existing file")
    if Path(photo).resolve() == target.resolve():
        raise ValueError("photo and output must differ")
    if effect not in FILTERS:
        raise ValueError("unsupported photo effect")
    if not isinstance(exposure, (int,float)) or isinstance(exposure,bool) or not math.isfinite(exposure) or not -2 <= exposure <= 2:
        raise ValueError("exposure must be finite and between -2 and 2")
    scene, details = compile_scene(data)
    if type(fps) is not int or not 1 <= fps <= 60:
        raise ValueError("fps must be an integer from 1 to 60")
    if not isinstance(duration, (int, float)) or isinstance(duration, bool) or not math.isfinite(duration) or not .05 <= duration <= 30:
        raise ValueError("duration must be from 0.05 to 30 seconds")
    frames = math.ceil(duration * fps)
    if frames > MAX_FRAMES:
        raise ValueError("300 frame limit")
    if target.suffix.lower() == ".gif" and scene["width"] * scene["height"] * frames > 65_000_000:
        raise ValueError("GIF frame pixel budget exceeded")
    checked_image(photo)
    return target, scene, details, frames


def compose(base, scene, t):
    # Unified Draw paints a transparent overlay, while the photograph remains untouched.
    base = ImageOps.fit(base, (scene["width"], scene["height"]),
                        method=Image.Resampling.LANCZOS, centering=(.5,.5))
    overlay_scene = dict(scene, background="transparent")
    layer = paint(overlay_scene, t).convert("RGBA")
    return Image.alpha_composite(base.convert("RGBA"), layer).convert("RGB")


def export(photo, data, output, effect="none", exposure=0.0, fps=12, duration=2):
    dest, scene, details, frames = validate_job(photo,data,output,effect,exposure,fps,duration)
    base = processed_photo(photo, effect, exposure)
    suffix = dest.suffix.lower()
    if suffix == ".png":
        compose(base,scene,0).save(dest)
    elif suffix == ".gif":
        imgs = [compose(base,scene,i/fps) for i in range(frames)]
        imgs[0].save(dest,save_all=True,append_images=imgs[1:],
                     duration=round(1000/fps),loop=0,optimize=False)
    else:
        if not shutil.which("ffmpeg"):
            raise ValueError("FFmpeg unavailable for MP4")
        with tempfile.TemporaryDirectory(prefix="kosif-unified-media-") as td:
            for i in range(frames):
                compose(base,scene,i/fps).save(Path(td)/f"{i:05d}.png")
            command=["ffmpeg","-hide_banner","-loglevel","error","-n",
                     "-framerate",str(fps),"-i",str(Path(td)/"%05d.png"),
                     "-frames:v",str(frames),"-c:v","libx264","-pix_fmt","yuv420p",
                     "-crf","18",str(dest)]
            subprocess.run(command, check=True,capture_output=True,timeout=120)
    return {"schema":"kosif.unified-media.v1","photo_effect":effect,
            "drawing_elements":len(details),"outputs":str(dest),
            "bytes":dest.stat().st_size,
            "sha256":hashlib.sha256(dest.read_bytes()).hexdigest(),
            "frames":1 if suffix==".png" else frames,
            "fps":None if suffix==".png" else fps,
            "engines":["app_studio","unified_draw","creative_paint",
                       "ffmpeg" if suffix==".mp4" else "pillow"],
            "verified":dest.is_file() and dest.stat().st_size>100}


def main():
    p=argparse.ArgumentParser(description="Photo editing + freehand + animated shapes + video")
    p.add_argument("command",choices=["doctor","render"])
    p.add_argument("--photo")
    p.add_argument("--scene")
    p.add_argument("--output")
    p.add_argument("--effect",default="none",choices=sorted(FILTERS))
    p.add_argument("--exposure",type=float,default=0.0)
    p.add_argument("--fps",type=int,default=12)
    p.add_argument("--duration",type=float,default=2)
    a=p.parse_args()
    if a.command=="doctor":
        print(json.dumps({"ready":True,"effects":sorted(FILTERS),
                          "formats":["png","gif","mp4"],
                          "ffmpeg":bool(shutil.which("ffmpeg")),
                          "engines":["app_studio","unified_draw","creative_paint"]}))
        return 0
    try:
        if not a.photo or not a.scene or not a.output:
            raise ValueError("--photo, --scene and --output are required")
        data=json.loads(Path(a.scene).read_text(encoding="utf-8-sig"))
        result=export(a.photo,data,a.output,a.effect,a.exposure,a.fps,a.duration)
        print(json.dumps(result,ensure_ascii=False))
        return 0
    except (ValueError, OSError, KeyError, subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
        print(json.dumps({"verified":False,"error":str(e)},ensure_ascii=False),file=sys.stderr)
        return 1


if __name__=="__main__":
    raise SystemExit(main())
