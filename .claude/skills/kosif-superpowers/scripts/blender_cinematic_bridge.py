#!/usr/bin/env python3
"""KOSIF Blender-to-Cinematic bridge: Cycles 3D video + 2D overlays + master audio.

This preserves prior KOSIF engines. Input .blend playback is rendered via the
existing blender_cycles_render.py (with Blender --disable-autoexec). No Blender
or proprietary application binaries are embedded into this repository.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from PIL import Image
from audio_cue_mapper import measure_wav
from unified_draw import compile_scene
from unified_media import compose
from unified_cinematic import fade_frame, pulse_scene

MAX_FRAMES=300
MAX_PIXELS=110_000_000
ACCEPTED_EXTS={".blend",".gltf",".glb"}


def exe(name):
    found=shutil.which(name)
    if not found:
        raise ValueError(name+" not installed")
    return found


def probe(path):
    cmd=[exe("ffprobe"),"-v","error","-show_streams","-show_format","-of","json",str(path)]
    result=subprocess.run(cmd,capture_output=True,text=True,check=True,timeout=30)
    return json.loads(result.stdout)


def validate(blender_video, scene_data, wav, output, fps):
    raw=Path(blender_video)
    dest=Path(output)
    if not raw.is_file() or raw.suffix.lower() not in (".mp4",".mkv"):
        raise ValueError("existing Blender-generated MP4/MKV required")
    if dest.suffix.lower()!=".mp4" or dest.exists() or not dest.parent.is_dir():
        raise ValueError("new MP4 output required, under existing directory")
    if type(fps)!=int or not 1<=fps<=60:
        raise ValueError("fps must be integer 1..60")
    cues=measure_wav(wav)
    if not .1<=cues["duration"]<=30:
        raise ValueError("WAV must be .1..30 sec")
    n=math.ceil(cues["duration"]*fps)
    if n>MAX_FRAMES:
        raise ValueError("maximum 300 frames")
    scene,details=compile_scene(scene_data)
    info=probe(raw)
    stream=next((s for s in info["streams"] if s["codec_type"]=="video"),None)
    if not stream or stream.get("codec_name") not in ("h264","hevc","av1","vp9"):
        raise ValueError("video codec unsupported")
    w,h=stream.get("width"),stream.get("height")
    if (w,h)!=(scene["width"],scene["height"]):
        raise ValueError("3D render and overlay scene size mismatch")
    if w*h*n>MAX_PIXELS:
        raise ValueError("too many frame pixels for bounded integration")
    fps_txt=stream.get("avg_frame_rate", "0/1")
    rate_num,rate_den=map(int,fps_txt.split("/"))
    if rate_den<=0 or abs(rate_num/rate_den-fps)>1e-4:
        raise ValueError("3D video fps must match soundtrack frame clock")
    counts=[int(stream[k]) for k in ("nb_frames","nb_read_frames") if str(stream.get(k,"")).isdigit()]
    if not counts or any(c!=n for c in counts):
        raise ValueError("3D render frame count differs from WAV frame count")
    if any(s.get("codec_type")=="audio" for s in info["streams"]):
        raise ValueError("Blender input must be silent video (soundtrack is source WAV)")
    return scene,details,cues,info,n


def compose_video(blender_video, scene_data, wav, output, fps=12, fade_frames=2, pulse_element=None):
    scene,details,cues,info,n=validate(blender_video,scene_data,wav,output,fps)
    if type(fade_frames)!=int or not 0<=fade_frames<=min(30,n//2):
        raise ValueError("invalid fade-frames")
    scene,pulses=pulse_scene(scene,cues["onset_candidates_seconds"],cues["duration"],pulse_element)
    exe("ffmpeg")
    with tempfile.TemporaryDirectory(prefix="kosif-blender-overlay-") as tmp:
        work=Path(tmp)
        rawframes=work/"from_cycles";rawframes.mkdir()
        finished=work/"composited";finished.mkdir()
        subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-nostdin",
                       "-i",str(blender_video),"-map","0:v:0","-fps_mode","passthrough",
                       str(rawframes/"%05d.png")],
                       check=True,capture_output=True,timeout=90)
        pictures=sorted(rawframes.glob("*.png"))
        if len(pictures)!=n:
            raise ValueError("decoded 3D video frame count mismatched the audio timeline")
        for i,src in enumerate(pictures):
            with Image.open(src) as original:
                frame=compose(original.convert("RGBA"),scene,i/fps)
            frame=fade_frame(frame,i,n,fade_frames)
            frame.save(finished/f"{i:05d}.png")
        command=["ffmpeg","-hide_banner","-loglevel","error","-nostdin","-n",
                 "-framerate",str(fps),"-i",str(finished/"%05d.png"),"-i",str(wav),
                 "-map","0:v:0","-map","1:a:0",
                 "-frames:v",str(n),"-c:v","libx264","-preset","slow","-pix_fmt","yuv420p","-crf","17",
                 "-c:a","aac","-b:a","320k","-af","aresample=async=1:first_pts=0",
                 "-t",str(n/fps),"-movflags","+faststart",str(output)]
        subprocess.run(command,check=True,capture_output=True,timeout=120)
    delivered=probe(output)
    vid=next((s for s in delivered["streams"] if s["codec_type"]=="video"),None)
    snd=next((s for s in delivered["streams"] if s["codec_type"]=="audio"),None)
    if not vid or vid["codec_name"]!="h264" or str(vid.get("nb_frames"))!=str(n):
        raise ValueError("failed composited video verification")
    if not snd or snd["codec_name"]!="aac":
        raise ValueError("composited MP4 missing AAC audio")
    if abs(float(delivered["format"]["duration"])-n/fps)>.15:
        raise ValueError("composited MP4 duration mismatch")
    out=Path(output)
    return {"schema":"kosif.blender-cinematic-bridge.v1",
            "verified":True,"3d_renderer":"Blender Cycles (input provenance requires checked render report)",
            "source_video_sha256":hashlib.sha256(Path(blender_video).read_bytes()).hexdigest(),
            "source_audio_sha256":hashlib.sha256(Path(wav).read_bytes()).hexdigest(),
            "output_sha256":hashlib.sha256(out.read_bytes()).hexdigest(),
            "frame_count":n,"fps":fps,"width":vid["width"],"height":vid["height"],
            "video_codec":vid["codec_name"],"audio_codec":snd["codec_name"],
            "audio_master_seconds":cues["duration"],
            "2d_layer_elements":len(details),"onset_candidates":len(cues["onset_candidates_seconds"]),
            "pulse_count":len(pulses),"verified_musical_beats":False,
            "source_audio_unchanged":True,"output_audio_reencoded":True,
            "output":str(out),"bytes":out.stat().st_size,
            "engines":["blender_cycles_render","audio_cue_mapper","unified_draw","creative_paint","ffmpeg"]}


def pipeline(blend, scene, audio, output, fps=12, width=384, height=216, samples=6, fade_frames=2, pulse_element=None, fur_count=0, fur_seed=2307):
    src=Path(blend)
    dest=Path(output)
    if dest.suffix.lower() != ".mp4" or dest.exists() or not dest.parent.is_dir():
        raise ValueError("new MP4 output required, under existing directory")
    if type(fps) is not int or not 1 <= fps <= 60:
        raise ValueError("fps must be integer 1..60")
    checked_scene,_=compile_scene(scene)
    if (checked_scene["width"], checked_scene["height"]) != (width, height):
        raise ValueError("scene overlay dimensions must match requested Cycles render")
    if not src.is_file() or src.suffix.lower() not in ACCEPTED_EXTS:
        raise ValueError("authorized existing .blend/.glb/.gltf required")
    if not (64<=width<=2048 and 64<=height<=2048 and width%2==0 and height%2==0):
        raise ValueError("even size 64..2048 required")
    if type(samples)!=int or not 4<=samples<=64:
        raise ValueError("Cycles samples 4..64 required for this pipeline")
    if type(fur_count) is not int or (fur_count!=0 and not 200<=fur_count<=7000):
        raise ValueError("fur-count must be 0 or between 200 and 7000")
    if type(fur_seed) is not int or not 0<=fur_seed<=10000000:
        raise ValueError("invalid fur seed")
    if fur_count and src.suffix.lower()!=".blend":
        raise ValueError("fur upgrade requires an editable .blend input")
    cues=measure_wav(audio)
    if not .1<=cues["duration"]<=30 or math.ceil(cues["duration"]*fps)>MAX_FRAMES:
        raise ValueError("audio too long for bounded Blender pipeline")
    with tempfile.TemporaryDirectory(prefix="kosif-blender-to-cinema-") as td:
        upgraded_scene=src
        if fur_count:
            from blender_cycles_render import executable
            blender=executable(None,"blender")
            if not blender:
                raise ValueError("Blender executable unavailable for fur upgrade")
            upgraded_scene=Path(td)/"upgraded_cat_fur.blend"
            upgraded_cmd=[blender,"--background","--factory-startup","--disable-autoexec",
                          "--python-exit-code","7","--python",
                          str(Path(__file__).with_name("blender_cat_fur_upgrade.py")),
                          "--","--source",str(src),"--output",str(upgraded_scene),
                          "--fur-count",str(fur_count),"--seed",str(fur_seed)]
            upgraded=subprocess.run(upgraded_cmd,capture_output=True,text=True,timeout=120)
            if upgraded.returncode or not upgraded_scene.is_file():
                raise ValueError("Blender fur upgrade failed: "+(upgraded.stdout+upgraded.stderr)[-500:])
        intermediate=Path(td)/"cycles_raw.mp4"
        cmd=[sys.executable,str(Path(__file__).with_name("blender_cycles_render.py")),
             "render","--scene",str(upgraded_scene),"--out",str(intermediate),
             "--width",str(width),"--height",str(height),"--frames",str(math.ceil(cues["duration"]*fps)),
             "--fps",str(fps),"--samples",str(samples),"--device","CPU"]
        done=subprocess.run(cmd,capture_output=True,text=True,timeout=600)
        if done.returncode:
            raise ValueError("Blender Cycles render failed: "+(done.stderr+done.stdout)[-550:])
        result=compose_video(intermediate,scene,audio,output,fps,fade_frames,pulse_element)
        result["3d_scene_sha256"]=hashlib.sha256(src.read_bytes()).hexdigest()
        result["fur_strands"]=fur_count
        result["fur_seed"]=fur_seed if fur_count else None
        result["rendered_blend_sha256"]=hashlib.sha256(upgraded_scene.read_bytes()).hexdigest()
        report_path=intermediate.with_name("cycles_raw.render-report.json")
        if not report_path.is_file():
            raise ValueError("Cycles rendering report missing")
        report=json.loads(report_path.read_text(encoding="utf-8"))
        result["render_report_verified"]=(report.get("status")=="VERIFIED_VIDEO"
          and report.get("sha256")==result["rendered_blend_sha256"]
          and report.get("video_sha256")==result["source_video_sha256"])
        if not result["render_report_verified"]:
            raise ValueError("Cycles rendering report disagrees with source scene or video")
        return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("action",choices=["doctor","compose","pipeline"])
    p.add_argument("--blend");p.add_argument("--blender-video");p.add_argument("--scene");p.add_argument("--audio");p.add_argument("--output")
    p.add_argument("--fps",type=int,default=12);p.add_argument("--width",type=int,default=384);p.add_argument("--height",type=int,default=216)
    p.add_argument("--samples",type=int,default=6);p.add_argument("--fade-frames",type=int,default=2)
    p.add_argument("--pulse-element",type=int,default=None)
    p.add_argument("--fur-count",type=int,default=0,help="0 disables fur; 200..7000 enables procedural Blender hair")
    p.add_argument("--fur-seed",type=int,default=2307)
    a=p.parse_args()
    if a.action=="doctor":
        from blender_cycles_render import executable
        result={name:executable(None,name) for name in ("blender","ffmpeg","ffprobe")}
        print(json.dumps({"ready":all(result.values()),"engines":result,"backend":"Blender Cycles CPU and KOSIF overlays+WAV"}))
        return 0
    try:
        if not (a.scene and a.audio and a.output):
            raise ValueError("--scene --audio --output required")
        data=json.loads(Path(a.scene).read_text(encoding="utf-8-sig"))
        if a.action=="compose":
            if not a.blender_video: raise ValueError("--blender-video is required")
            result=compose_video(a.blender_video,data,a.audio,a.output,a.fps,a.fade_frames,a.pulse_element)
        else:
            if not a.blend: raise ValueError("--blend is required")
            result=pipeline(a.blend,data,a.audio,a.output,a.fps,a.width,a.height,a.samples,
                            a.fade_frames,a.pulse_element,a.fur_count,a.fur_seed)
        print(json.dumps(result,ensure_ascii=False))
        return 0
    except (ValueError, OSError, RuntimeError, KeyError, TypeError, subprocess.TimeoutExpired,
            subprocess.CalledProcessError, json.JSONDecodeError) as error:
        print(json.dumps({"verified":False,"error":str(error)},ensure_ascii=False),file=sys.stderr)
        return 1


if __name__=="__main__":
    raise SystemExit(main())
