#!/usr/bin/env python3
"""Create original synthetic video+audio+image sources and render a KOSIF timeline.

No personal media, no internet, no vendor application code. Directory must not exist.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from PIL import Image, ImageDraw
from kosif_timeline import render, validate


def create(directory):
    out=Path(directory).expanduser()
    if out.exists() or not out.parent.is_dir() or out.is_symlink():
        raise ValueError("demo destination must be a new folder under an existing directory")
    out.mkdir()
    source_a=out/"scene-a.mp4"
    source_b=out/"scene-b.mp4"
    music=out/"music.wav"
    art=out/"overlay.png"
    project_file=out/"project.json"
    movie=out/"timeline.mp4"

    commands=[
       ["ffmpeg","-hide_banner","-loglevel","error","-nostdin","-n",
         "-f","lavfi","-i","color=c=0x24536b:s=480x270:r=12:d=2",
         "-f","lavfi","-i","sine=frequency=440:sample_rate=44100:duration=2",
         "-c:v","libx264","-pix_fmt","yuv420p","-c:a","aac","-shortest",str(source_a)],
       ["ffmpeg","-hide_banner","-loglevel","error","-nostdin","-n",
         "-f","lavfi","-i","color=c=0x9a4f30:s=480x270:r=12:d=2",
         "-c:v","libx264","-pix_fmt","yuv420p",str(source_b)],
       ["ffmpeg","-hide_banner","-loglevel","error","-nostdin","-n",
         "-f","lavfi","-i","sine=frequency=660:sample_rate=44100:duration=3",
         "-c:a","pcm_s16le",str(music)]
    ]
    for args in commands:
        subprocess.run(args,check=True,capture_output=True,timeout=60)
    img=Image.new("RGBA",(130,80),(8,130,112,170))
    ImageDraw.Draw(img).ellipse((25,9,104,70),fill=(240,211,109,255))
    img.save(art)

    project={
      "schema":"kosif.timeline.v1","width":480,"height":270,"fps":12,"duration":3,
      "background":"#182522","tracks":[
      {"id":"picture","kind":"video","layer":0,"clips":[
        {"id":"shot1","path":str(source_a.resolve()),"start":0,"in":0,
         "duration":1.65,"fade_out":.3,"include_audio":True,"volume":.6},
        {"id":"shot2","path":str(source_b.resolve()),"start":1.3,"in":0,
         "duration":1.7,"fade_in":.35}]},
      {"id":"graphics","kind":"image","layer":5,"clips":[
        {"id":"badge","path":str(art.resolve()),"start":.4,
         "duration":2.3,"x":20,"y":20,"width":130,"height":80,
         "fade_in":.2,"fade_out":.3}]},
      {"id":"music","kind":"audio","layer":0,"clips":[
        {"id":"melody","path":str(music.resolve()),"start":.1,"in":0,
         "duration":2.7,"volume":.22,"fade_in":.2,"fade_out":.3}]}]}
    validate(project)
    project_file.write_text(json.dumps(project,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt=render(project,movie)
    receipt_file=out/"receipt.json"
    receipt_file.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return {"demo_folder":str(out),"project":str(project_file),"movie":str(movie),
            "receipt":str(receipt_file),"verified":receipt["verified"],
            "frames":receipt["frames"],"audio_codec":receipt["audio_codec"]}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dir",required=True)
    args=parser.parse_args()
    try:
        print(json.dumps(create(args.dir),ensure_ascii=False))
    except (ValueError,OSError,subprocess.CalledProcessError,subprocess.TimeoutExpired) as e:
        parser.exit(1,str(e)+"\n")


if __name__=="__main__":
    main()
