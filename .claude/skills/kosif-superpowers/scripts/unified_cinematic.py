#!/usr/bin/env python3
"""KOSIF cinematic integration: measured PCM WAV + layered drawing/photo + MP4.

Audio source is the timing master and never modified. Output audio is AAC re-encoded.
Onset candidates are amplitude transients, NOT verified beats or word alignment.
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

from audio_cue_mapper import measure_wav
from unified_draw import compile_scene
from unified_media import checked_image, compose, processed_photo

CAMERAS = {"static", "push-in", "pull-back", "pan-right"}
MAX_FRAMES = 300
MAX_DIM = 2048


def camera_frame(base, dimensions, position, movement):
    """Safe 2D simulated camera move: center crop from a large background."""
    if movement not in CAMERAS:
        raise ValueError("unsupported camera movement")
    w, h = dimensions
    if movement == "static":
        return ImageOps.fit(base, (w, h), method=Image.Resampling.LANCZOS)
    pos = max(0.0, min(1.0, float(position)))
    if movement == "push-in":
        z = 1 + .12 * pos
        center = (.5, .5)
    elif movement == "pull-back":
        z = 1 + .12 * (1-pos)
        center = (.5, .5)
    else:
        z = 1.16
        center = (.43 + .14 * pos, .5)
    sw, sh = max(1, round(w/z)), max(1, round(h/z))
    fitted = ImageOps.fit(base, (w, h), method=Image.Resampling.LANCZOS)
    x = min(w-sw, max(0, round((w-sw)*center[0]*2 - (w-sw)*.5)))
    y = (h-sh)//2
    return fitted.crop((x,y,x+sw,y+sh)).resize((w,h), Image.Resampling.LANCZOS)


def pulse_scene(scene, events, duration, element_index):
    """Apply explicit 2D keyframe impulses to one previously unkeyframed layer."""
    if element_index is None:
        return scene, []
    if type(element_index) is not int or not (1<=element_index<=len(scene["layers"])):
        raise ValueError("pulse-element must index an existing drawing element (1-based)")
    layer = scene["layers"][element_index-1]
    if layer.get("keyframes"):
        raise ValueError("pulse-element already has keyframes; refusing to replace manual animation")
    boundaries = [float(t) for t in events if isinstance(t,(int,float)) and .16<=t<=duration-.20]
    accepted, previous=[], -.5
    for t in boundaries:
        if t-previous >= .26 and len(accepted)<40:
            accepted.append(t)
            previous=t
    keys=[{"time":0,"scale":1,"opacity":1}]
    for t in accepted:
        keys.extend([
            {"time":round(t-.05,6),"scale":1,"opacity":1},
            {"time":round(t,6),"scale":1.12,"opacity":1},
            {"time":round(t+.15,6),"scale":1,"opacity":1}
        ])
    keys.append({"time":round(duration,6),"scale":1,"opacity":1})
    updated=dict(scene,layers=[dict(x) for x in scene["layers"]])
    updated["layers"][element_index-1]["keyframes"]=keys
    return updated, accepted


def fade_frame(im, frame_index, frames, fade):
    if not fade:
        return im
    n=min(fade, frames//2)
    if n<=0:
        return im
    alpha=min(1.0,(frame_index+1)/n,(frames-frame_index)/n)
    if alpha>=1:
        return im
    return Image.blend(Image.new("RGB",im.size,"black"),im,alpha)


def plan(photo, scene_data, audio, output, fps=12, camera="static", fade_frames=2, pulse_element=None, effect="none", exposure=0):
    dest=Path(output)
    if dest.suffix.lower()!=".mp4" or not dest.parent.is_dir() or dest.exists():
        raise ValueError("output must be a new MP4 path under an existing folder")
    if camera not in CAMERAS:
        raise ValueError("invalid camera movement")
    if type(fps) is not int or not 1<=fps<=60:
        raise ValueError("fps must be integer 1..60")
    if type(fade_frames) is not int or not 0<=fade_frames<=30:
        raise ValueError("fade-frames must be integer 0..30")
    source_info=measure_wav(audio)
    duration=source_info["duration"]
    if duration>30 or duration<.1:
        raise ValueError("audio duration for this renderer must be 0.1..30 seconds")
    frames=math.ceil(duration*fps)
    if frames>MAX_FRAMES:
        raise ValueError("300 frame limit; lower FPS or shorten the audio")
    scene,details=compile_scene(scene_data)
    if scene["width"]*scene["height"]*frames>100_000_000:
        raise ValueError("frame pixel budget exceeded")
    if fade_frames>frames//2:
        raise ValueError("fade-frames exceeds half the available frames")
    base=checked_image(photo)
    if base.width*base.height>32_000_000:
        raise ValueError("photo exceeds pixel limit")
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise ValueError("FFmpeg and FFprobe required for audio/video")
    scene,pulses=pulse_scene(scene,source_info["onset_candidates_seconds"],duration,pulse_element)
    return {"dest":dest,"scene":scene,"photo":Path(photo),"audio":Path(audio),
            "details":details,"duration":duration,"frames":frames,"fps":fps,
            "camera":camera,"fade_frames":fade_frames,"pulses":pulses,
            "cue_metadata":source_info,"effect":effect,"exposure":exposure}


def probe(path):
    result=subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)],
                          check=True,capture_output=True,text=True,timeout=25)
    return json.loads(result.stdout)


def produce(photo,scene_data,audio,output,fps=12,camera="static",fade_frames=2,pulse_element=None,effect="none",exposure=0):
    job=plan(photo,scene_data,audio,output,fps,camera,fade_frames,pulse_element,effect,exposure)
    base=processed_photo(job["photo"],job["effect"],job["exposure"])
    frames=job["frames"]
    with tempfile.TemporaryDirectory(prefix="kosif-cinematic-audio-") as td:
        folder=Path(td)
        for i in range(frames):
            t=i/job["fps"]
            adjusted=camera_frame(base,(job["scene"]["width"],job["scene"]["height"]),
                                  i/max(1,frames-1),camera)
            image=compose(adjusted,job["scene"],t)
            fade_frame(image,i,frames,fade_frames).save(folder/f"{i:05d}.png")
        # Original WAV remains untouched; MP4 receives a re-encoded AAC track.
        command=["ffmpeg","-hide_banner","-loglevel","error","-nostdin","-n",
                 "-framerate",str(fps),"-i",str(folder/"%05d.png"),
                 "-i",str(job["audio"]),"-map","0:v:0","-map","1:a:0",
                 "-c:v","libx264","-pix_fmt","yuv420p","-crf","18",
                 "-c:a","aac","-b:a","192k","-af","aresample=async=1:first_pts=0",
                 "-t",str(frames/fps),"-movflags","+faststart",str(job["dest"])]
        subprocess.run(command,check=True,capture_output=True,timeout=120)
    report=probe(job["dest"])
    video=next((s for s in report["streams"] if s["codec_type"]=="video"),None)
    soundtrack=next((s for s in report["streams"] if s["codec_type"]=="audio"),None)
    if not video or video.get("codec_name")!="h264" or int(video.get("nb_frames",0))!=frames:
        raise ValueError("render failed frame/codec verification")
    if not soundtrack or soundtrack.get("codec_name")!="aac":
        raise ValueError("render lacks AAC audio")
    if abs(float(report["format"].get("duration",0))-frames/fps)>.15:
        raise ValueError("audio/video output duration mismatch")
    return {"schema":"kosif.unified-cinematic.v1","verified":True,
            "audio_master_seconds":job["duration"],"output_duration":report["format"].get("duration"),
            "source_audio_unchanged":True,"output_audio_codec":"aac (re-encoded)",
            "video_codec":"h264","frames":frames,"fps":fps,
            "camera":camera,"fade_frames":fade_frames,
            "measured_onset_candidates":len(job["cue_metadata"]["onset_candidates_seconds"]),
            "pulse_keyframes_added":len(job["pulses"]),"verified_beats":False,
            "word_alignment":"not performed",
            "sha256":hashlib.sha256(job["dest"].read_bytes()).hexdigest(),
            "bytes":job["dest"].stat().st_size,"output":str(job["dest"]),
            "engines":["audio_cue_mapper","app_studio","unified_draw","creative_paint","ffmpeg"]}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("command",choices=["doctor","render"])
    p.add_argument("--photo");p.add_argument("--scene");p.add_argument("--audio");p.add_argument("--output")
    p.add_argument("--effect",choices=["none","develop","ink-sketch","pencil-sketch"],default="none")
    p.add_argument("--exposure",type=float,default=0)
    p.add_argument("--fps",type=int,default=12)
    p.add_argument("--camera",choices=sorted(CAMERAS),default="static")
    p.add_argument("--fade-frames",type=int,default=2)
    p.add_argument("--pulse-element",type=int,default=None)
    a=p.parse_args()
    if a.command=="doctor":
        print(json.dumps({"ready":bool(shutil.which("ffmpeg") and shutil.which("ffprobe")),
                          "master_clock":"16-bit PCM WAV","video":"H264 MP4",
                          "audio":"AAC re-encoded","cameras":sorted(CAMERAS),
                          "onset_timing":"amplitude candidates, not verified beats"}))
        return 0
    try:
        if not all((a.photo,a.scene,a.audio,a.output)):
            raise ValueError("--photo --scene --audio --output required")
        data=json.loads(Path(a.scene).read_text(encoding="utf-8-sig"))
        result=produce(a.photo,data,a.audio,a.output,a.fps,a.camera,a.fade_frames,
                       a.pulse_element,a.effect,a.exposure)
        print(json.dumps(result,ensure_ascii=False))
        return 0
    except (ValueError,OSError,subprocess.CalledProcessError,subprocess.TimeoutExpired,
            KeyError,TypeError,json.JSONDecodeError) as exc:
        print(json.dumps({"verified":False,"error":str(exc)},ensure_ascii=False),file=sys.stderr)
        return 1


if __name__=="__main__":
    raise SystemExit(main())
