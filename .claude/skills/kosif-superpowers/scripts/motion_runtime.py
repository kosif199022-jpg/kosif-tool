#!/usr/bin/env python3
"""KOSIF Motion Runtime: real, original, offline-ready SVG film + opt-in MP4 render.

No package installation and no third-party source vendoring.
Scaffold creates an editable HTML film compatible with tools/render_html.cjs.
"""
import argparse
import html
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

SKILL = Path(__file__).resolve().parents[1]
TEMPLATE = SKILL / "resources" / "motion-runtime" / "doodle-film.template.html"
ENGINE_DATA = SKILL / "data" / "motion_engines.json"
REPO_ROOT = Path(__file__).resolve().parents[4]
RENDERER = REPO_ROOT / "tools" / "render_html.cjs"


def read_engines():
    rows = json.loads(ENGINE_DATA.read_text(encoding="utf-8"))
    assert isinstance(rows, list) and len(rows) >= 20
    return rows


def detect():
    found={k:shutil.which(k) for k in ("python3", "node", "ffmpeg", "ffprobe")}
    return {"status":"probe_only", "programs":{k:bool(v) for k,v in found.items()},
            "template_found":TEMPLATE.is_file(), "renderer_found":RENDERER.is_file(),
            "browser_automation_verified":False,
            "svg_seek_verified":False,
            "mp4_render_verified":False,
            "note":"Installed executables are not proof of a working render; verify a real output."}


def safe_text(x, label):
    if not x or len(x)>120 or "\n" in x or "\r" in x:
        raise ValueError(label+" must be 1-120 characters without newlines")
    return html.escape(x,quote=True)


def make_html(title, subtitle, duration=8, fps=30):
    d=float(duration)
    f=int(fps)
    if not 8<=d<=120 or not (24<=f<=60):
        raise ValueError("duration must be 8..120 and FPS 24..60")
    sample = TEMPLATE.read_text(encoding="utf-8")
    required={"__TITLE__", "__SUBTITLE__", "__DURATION__", "__FPS__"}
    if any(sample.count(x)!=1 for x in required):
        raise ValueError("Template marker mismatch")
    return (sample.replace("__TITLE__", safe_text(title, "title"))
                  .replace("__SUBTITLE__",safe_text(subtitle, "subtitle"))
                  .replace("__DURATION__",str(d)).replace("__FPS__",str(f)))


def scaffold(out, title, subtitle, duration, fps):
    out = Path(out).expanduser().absolute()
    if not out.parent.is_dir() or out.is_symlink() or out.exists():
        raise ValueError("target directory must be new and have an existing parent")
    film=make_html(title,subtitle,duration,fps)
    out.mkdir()
    (out/"film.html").write_text(film,encoding="utf-8")
    (out/"motion.json").write_text(json.dumps({
        "schema":"kosif.motion-project.v1",
        "title":title,"subtitle":subtitle,"duration":float(duration),
        "fps":int(fps),"aspect":"9:16",
        "runtime":"deterministic-svg-seek",
        "external_media_bundled":False,
        "render_verified":False
    },ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (out/"README.md").write_text(
        "# KOSIF Motion Runtime — original Doodle Film\n\n"
        "Open film.html locally. For a rendered, independently verified movie use "
        "the parent kosif-tool repository's renderer after checking dependencies.\n\n"
        "    node tools/render_html.cjs --in /absolute/project/film.html --out /absolute/project/out.mp4 --width 1080 --height 1920 --fps 30 --offline\n\n"
        "Use --audio /absolute/voice.wav to keep the user's narration on the timeline. "
        "This template has a fixed 8-second drawing performance; for other durations, extend the storyboard and keyframes.\n"
        "For a preview use --preview and output preview.png. "
        "Verify with tools/verify_video.py and inspect frames before saying delivered.\n",
        encoding="utf-8")
    return {"status":"scaffold_created_not_rendered","file":str(out/"film.html"),
            "project":str(out), "runtime":"seek_svg", "render_verified":False}


def render(html_file, out_file, *, fps=30, width=1080, height=1920, audio=None, approved=False):
    source=Path(html_file).expanduser().resolve()
    destination=Path(out_file).expanduser().absolute()
    if not approved:
        return {"status":"approval_required","executed":False}
    if not source.is_file() or source.suffix.lower()!=".html":
        raise ValueError("source HTML must exist")
    if destination.exists() or destination.is_symlink() or not destination.parent.is_dir() or destination.suffix.lower() not in (".mp4",".png"):
        raise ValueError("output must be a new PNG or MP4 with an existing parent directory")
    if int(fps) not in (24,30,60) or (int(width),int(height))!=(1080,1920):
        raise ValueError("approved output: 1080x1920, FPS 24/30/60")
    if not RENDERER.is_file() or not shutil.which("node"):
        return {"status":"render_engine_unavailable","executed":False}
    cmd=["node",str(RENDERER),"--in",str(source),"--out",str(destination),
         "--width","1080","--height","1920","--fps",str(int(fps)),"--offline","--mode","seek"]
    if destination.suffix.lower()==".png":
        cmd.append("--preview")
    if audio:
        ap=Path(audio).expanduser().resolve()
        if not ap.is_file():
            raise ValueError("audio file missing")
        if destination.suffix.lower()!=".mp4":
            raise ValueError("audio only supported with MP4 render")
        cmd += ["--audio",str(ap)]
    try:
        completed=subprocess.run(cmd,stdin=subprocess.DEVNULL,capture_output=True,
                                 text=True,timeout=240,check=False)
    except (OSError,subprocess.TimeoutExpired):
        return {"status":"render_process_failed","executed":True,"verified":False}
    if completed.returncode:
        return {"status":"render_command_failed","exit_code":completed.returncode,
                "executed":True,"verified":False}
    if not destination.is_file() or destination.stat().st_size<200:
        return {"status":"render_output_missing_or_empty","executed":True,"verified":False}
    return {"status":"rendered_requires_visual_qa","output":str(destination),"bytes":destination.stat().st_size,
            "executed":True,"verified":False,
            "next":"Run tools/verify_video.py and inspect actual frames and audio"}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    sub=ap.add_subparsers(dest="action",required=True)
    sub.add_parser("doctor")
    engines=sub.add_parser("engines");engines.add_argument("--family",default="")
    s=sub.add_parser("scaffold")
    s.add_argument("--out",required=True);s.add_argument("--title",default="قصيف يرسم")
    s.add_argument("--subtitle",default="الحركة تُولد بالكود")
    s.add_argument("--duration",type=float,default=8)
    s.add_argument("--fps",type=int,default=30)
    r=sub.add_parser("render");r.add_argument("--in",dest="source",required=True)
    r.add_argument("--out",required=True);r.add_argument("--fps",type=int,default=30)
    r.add_argument("--audio");r.add_argument("--run",action="store_true")
    args=ap.parse_args()
    try:
        if args.action=="doctor":result=detect()
        elif args.action=="engines":
            e=read_engines()
            result={"status":"knowledge_and_adapters_only","engines":[x for x in e if not args.family or x["family"]==args.family],
                    "installed_runtime_verified":False}
        elif args.action=="scaffold":result=scaffold(args.out,args.title,args.subtitle,args.duration,args.fps)
        else:result=render(args.source,args.out,fps=args.fps,audio=args.audio,approved=args.run)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 0 if result.get("status") not in ("render_command_failed","render_process_failed","render_output_missing_or_empty") else 2
    except (ValueError,OSError,AssertionError,json.JSONDecodeError) as exc:
        print(json.dumps({"status":"invalid_request_or_registry","error":str(exc)},ensure_ascii=False),file=sys.stderr)
        return 2


if __name__=="__main__":
    sys.exit(main())
