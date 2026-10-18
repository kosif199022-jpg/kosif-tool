#!/usr/bin/env python3
"""Local reference-video timing probe: ffprobe metadata + ffmpeg cut candidates.

This is an actual opt-in analyzer for videos provided locally by the user. It
does NOT infer animation semantics, copy source assets, track objects, transcribe
speech or claim a visual match to the reference.
"""
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

CUT_RE = re.compile(r"pts_time:\s*([0-9]+(?:\.[0-9]+)?)")
MAX_SECONDS = 300.0
MAX_BYTES = 1_000_000_000


def parse_cuts(stderr, duration, threshold=0.35):
    # FFmpeg's showinfo is emitted only for frames selected by scene detection.
    times = []
    for m in CUT_RE.finditer(stderr):
        t=float(m.group(1))
        if 0.2 < t < duration - 0.2 and (not times or t-times[-1] >= 0.25):
            times.append(round(t, 3))
    return times


def cmd(args, timeout=120):
    return subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                          text=True,stdin=subprocess.DEVNULL,timeout=timeout,check=False)


def probe(path, threshold=0.35, detect_cuts=False):
    input_path=Path(path).expanduser()
    if not input_path.is_file() or input_path.is_symlink():
        raise ValueError("must be a regular locally authorized video file")
    if input_path.stat().st_size > MAX_BYTES:
        raise ValueError("video exceeds 1 GB analysis bound")
    if not shutil.which("ffprobe"):
        raise ValueError("ffprobe is missing")
    if not 0 < threshold < 1:
        raise ValueError("threshold must be between zero and one")
    info=cmd(["ffprobe","-v","error","-show_streams","-show_format","-of","json",
              str(input_path.resolve())],timeout=30)
    if info.returncode:
        raise ValueError("ffprobe failed to inspect input")
    try:
        j=json.loads(info.stdout)
        streams=j["streams"]
        duration=float(j["format"]["duration"])
    except (KeyError,TypeError,ValueError,json.JSONDecodeError) as exc:
        raise ValueError("ffprobe returned invalid metadata") from exc
    if not 0 < duration <= MAX_SECONDS:
        raise ValueError("duration must be 0..300 seconds")
    video=next((s for s in streams if s.get("codec_type")=="video"),None)
    if not video:
        raise ValueError("no video stream")
    audio=any(s.get("codec_type")=="audio" for s in streams)
    times=[]
    if detect_cuts:
        if not shutil.which("ffmpeg"):
            raise ValueError("ffmpeg is missing for cuts")
        filter_arg="select=gt(scene\\,"+str(threshold)+"),showinfo"
        p=cmd(["ffmpeg","-nostdin","-hide_banner","-loglevel","info","-i",
               str(input_path.resolve()),"-map","0:v:0","-vf",filter_arg,
               "-an","-f","null","-"],timeout=240)
        if p.returncode:
            raise ValueError("ffmpeg cut detection failed")
        times=parse_cuts(p.stderr,duration,threshold)
    bounds=[0.0]+times+[round(duration,3)]
    return {"status":"reference_timing_observed_not_animation_reconstructed",
            "target":str(input_path.resolve()),"width":video.get("width"),
            "height":video.get("height"),"fps_rational":video.get("avg_frame_rate"),
            "duration_seconds":duration,"audio_present":audio,
            "cut_detection_run":detect_cuts,"cut_candidates_seconds":times,
            "segments":[{"start":a,"end":b} for a,b in zip(bounds,bounds[1:])],
            "important_limitations":["cuts are heuristic visual-change candidates",
                                     "no object/pose/motion-vector tracking",
                                     "no audio word-level alignment",
                                     "no copying proprietary visuals"],
            "next":"Review sampled keyframes and map observed motion to original motion_director scenes"}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video")
    parser.add_argument("--cuts",action="store_true")
    parser.add_argument("--threshold",type=float,default=0.35)
    parser.add_argument("--out",help="new JSON report path; never overwrite")
    args=parser.parse_args()
    try:
        result=probe(args.video,args.threshold,args.cuts)
        if args.out:
            p=Path(args.out).expanduser()
            if p.exists() or not p.parent.is_dir() or p.is_symlink():
                raise ValueError("output already exists or parent missing")
            with p.open("x",encoding="utf-8") as f:
                json.dump(result,f,ensure_ascii=False,indent=2)
            print(json.dumps({"status":result["status"],"saved":str(p.resolve()),
                              "cuts":len(result["cut_candidates_seconds"])}))
        else:
            print(json.dumps(result,ensure_ascii=False,indent=2))
        return 0
    except (ValueError,OSError,subprocess.TimeoutExpired) as error:
        print(json.dumps({"status":"failed","error":str(error)}),file=sys.stderr)
        return 2


if __name__=="__main__":
    sys.exit(main())
