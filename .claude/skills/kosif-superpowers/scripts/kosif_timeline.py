#!/usr/bin/env python3
"""KOSIF Timeline v1: non-destructive multitrack video/audio editing with FFmpeg.

Project schema: kosif.timeline.v1. Video/image layers are ordered by layer
(ascending) then track then clip start. Overlap crossfades via alpha fade
in/out, not claimed frame-perfect audio word alignment. Audio is mixed as PCM
in FFmpeg then re-encoded to AAC. Source files are immutable.

No proprietary Canva/Adobe code is used.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys

SCHEMA="kosif.timeline.v1"
KINDS={"video":{".mp4",".mov",".mkv",".webm",".m4v"},
       "image":{".png",".jpg",".jpeg",".webp"},
       "audio":{".wav",".mp3",".m4a",".aac",".flac"}}
COLOR=re.compile(r"^#[0-9a-fA-F]{6}$")
MAX_MEDIA_BYTES=1_000_000_000
MAX_CLIPS=32
TIMEOUT=240


def number(value, name, minimum=0, maximum=3600):
    if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be finite numeric")
    x=float(value)
    if not minimum<=x<=maximum:
        raise ValueError(f"{name} must be within {minimum}..{maximum}")
    return x


def integer(value,name,minn,maxx):
    if type(value) is not int or not minn<=value<=maxx:
        raise ValueError(f"{name} must be an integer within {minn}..{maxx}")
    return value


def probing(path):
    cmd=["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)]
    res=subprocess.run(cmd,check=True,capture_output=True,text=True,timeout=25)
    return json.loads(res.stdout)


def validate(project, *, do_probe=True, output=None):
    if not isinstance(project,dict) or project.get("schema")!=SCHEMA:
        raise ValueError("unknown project schema")
    width=integer(project.get("width"),"width",64,1920)
    height=integer(project.get("height"),"height",64,1920)
    if width%2 or height%2:
        raise ValueError("video width/height must be even")
    fps=integer(project.get("fps"),"fps",1,30)
    duration=number(project.get("duration"),"duration",.1,60)
    if math.ceil(duration*fps)>1800:
        raise ValueError("frame limit exceeded")
    if width*height*math.ceil(duration*fps)>300_000_000:
        raise ValueError("pixel-frame budget exceeded; lower resolution, FPS, or duration")
    color=project.get("background","#161c1b")
    if not isinstance(color,str) or not COLOR.fullmatch(color):
        raise ValueError("background must be #RRGGBB")
    tracks=project.get("tracks")
    if not isinstance(tracks,list) or not 1<=len(tracks)<=12:
        raise ValueError("tracks must contain 1..12 items")
    seen=set()
    ordered=[]
    count=0
    for ti,track in enumerate(tracks):
        if not isinstance(track,dict) or not isinstance(track.get("id"),str):
            raise ValueError("track id missing")
        tid=track["id"]
        if not tid or tid in seen or len(tid)>60:
            raise ValueError("track ids must be unique and nonempty")
        seen.add(tid)
        kind=track.get("kind")
        if kind not in KINDS:
            raise ValueError("unsupported track kind")
        layer=integer(track.get("layer",0),"layer",0,99)
        clips=track.get("clips",[])
        if not isinstance(clips,list):
            raise ValueError("clips must be an array")
        for ci,clip in enumerate(clips):
            count+=1
            if count>MAX_CLIPS:raise ValueError("too many clips")
            if not isinstance(clip,dict):
                raise ValueError("clip must be an object")
            cid=clip.get("id")
            if not isinstance(cid,str) or not cid or len(cid)>80 or cid in seen:
                raise ValueError("clip ids must be unique")
            seen.add(cid)
            src=clip.get("path")
            if not isinstance(src,str):
                raise ValueError("clip path must be local")
            path=Path(src).expanduser()
            if not path.is_file() or path.is_symlink() or path.suffix.lower() not in KINDS[kind]:
                raise ValueError(f"unsupported/missing local {kind} source: {cid}")
            if not 0<path.stat().st_size<=MAX_MEDIA_BYTES:
                raise ValueError(f"{cid}: source size limit")
            start=number(clip.get("start"),f"{cid}.start",0,60)
            length=number(clip.get("duration"),f"{cid}.duration",.05,60)
            source_in=number(clip.get("in",0),f"{cid}.in",0,3600)
            if kind=="image" and source_in!=0:
                raise ValueError("image source-in must be 0")
            if start+length>duration+.001:
                raise ValueError(f"{cid}: clip extends past timeline")
            fi=number(clip.get("fade_in",0),f"{cid}.fade_in",0,length/2)
            fo=number(clip.get("fade_out",0),f"{cid}.fade_out",0,length/2)
            if kind=="audio" and any(k in clip for k in ("x","y","width","height")):
                raise ValueError("audio clips cannot have layout")
            has_audio=kind=="audio" or (kind=="video" and clip.get("include_audio",False) is True)
            if kind=="video" and clip.get("include_audio",False) not in (True,False):
                raise ValueError("include_audio must be bool")
            if kind!="audio":
                x=integer(clip.get("x",0),f"{cid}.x",-width,width)
                y=integer(clip.get("y",0),f"{cid}.y",-height,height)
                cw=integer(clip.get("width",width),f"{cid}.width",2,width)
                ch=integer(clip.get("height",height),f"{cid}.height",2,height)
                if cw%2 or ch%2:raise ValueError("clip scaled width/height must be even")
            else:x=y=cw=ch=None
            vol=number(clip.get("volume",1.0),f"{cid}.volume",0,3)
            md=None
            if do_probe:
                md=probing(path)
                fmt=md.get("format",{})
                streams=md.get("streams",[])
                actual_video=any(s.get("codec_type")=="video" for s in streams)
                actual_audio=any(s.get("codec_type")=="audio" for s in streams)
                if kind=="video" and not actual_video:
                    raise ValueError(f"{cid}: no video stream")
                if has_audio and not actual_audio:
                    raise ValueError(f"{cid}: no audio stream")
                if kind in ("audio","video"):
                    actual_dur=float(fmt.get("duration",0))
                    if not math.isfinite(actual_dur) or source_in+length>actual_dur+.05:
                        raise ValueError(f"{cid}: requested interval exceeds source duration")
            ordered.append({"track":tid,"track_order":ti,"clip_order":ci,"id":cid,
                            "kind":kind,"path":path,"start":start,"duration":length,
                            "source_in":source_in,"fade_in":fi,"fade_out":fo,
                            "layer":layer,"x":x,"y":y,"width":cw,"height":ch,
                            "volume":vol,"include_audio":has_audio})
    if not ordered:
        raise ValueError("no clips")
    if output is not None:
        dest=Path(output).expanduser()
        if dest.suffix.lower()!=".mp4" or not dest.parent.is_dir() or dest.exists() or dest.is_symlink():
            raise ValueError("output must be a new MP4 in an existing folder")
        if any(dest.resolve()==a["path"].resolve() for a in ordered):
            raise ValueError("source cannot be overwritten")
    return {"width":width,"height":height,"fps":fps,"duration":duration,
            "background":color,"clips":ordered}


def filters_and_inputs(doc):
    clips=doc["clips"]
    width,height,fps=doc["width"],doc["height"],doc["fps"]
    duration=doc["duration"]
    args=[]
    expressions=[f"color=c=0x{doc['background'][1:]}:s={width}x{height}:r={fps}:d={duration:.6f},format=yuv420p[background]"]
    visuals=sorted([v for v in clips if v["kind"]!="audio"],
                   key=lambda v:(v["layer"],v["track_order"],v["start"],v["clip_order"]))
    audios=[v for v in clips if v["include_audio"]]
    for idx, clip in enumerate(clips):
        # Image loops are bounded by atrim/trim and global timeline cap.
        if clip["kind"]=="image":
            args+=["-loop","1","-framerate",str(fps),"-i",str(clip["path"])]
        else:
            args+=["-i",str(clip["path"])]
    for clip in visuals:
        idx=clips.index(clip)
        src_in=clip["source_in"]
        length=clip["duration"]
        fw,fh=clip["width"],clip["height"]
        op=f"[{idx}:v]trim=start={src_in:.6f}:duration={length:.6f},setpts=PTS-STARTPTS,"
        op+=f"fps={fps},scale={fw}:{fh}:force_original_aspect_ratio=decrease,"
        op+=f"pad={fw}:{fh}:(ow-iw)/2:(oh-ih)/2:color=black,format=rgba"
        if clip["fade_in"]>0:
            op+=f",fade=t=in:st=0:d={clip['fade_in']:.6f}:alpha=1"
        if clip["fade_out"]>0:
            op+=f",fade=t=out:st={length-clip['fade_out']:.6f}:d={clip['fade_out']:.6f}:alpha=1"
        op+=f",setpts=PTS+{clip['start']:.6f}/TB[v{idx}]"
        expressions.append(op)
    last="background"
    for pos,clip in enumerate(visuals):
        idx=clips.index(clip)
        next_label=f"stack{pos}"
        expressions.append(f"[{last}][v{idx}]overlay=x={clip['x']}:y={clip['y']}:"
                           f"eof_action=pass:repeatlast=0:shortest=0:format=auto[{next_label}]")
        last=next_label
    expressions.append(f"[{last}]format=yuv420p[vout]")
    audio_labels=[]
    for clip in audios:
        idx=clips.index(clip)
        start=clip["source_in"]
        length=clip["duration"]
        a=f"[{idx}:a]atrim=start={start:.6f}:duration={length:.6f},asetpts=PTS-STARTPTS,"
        a+="aresample=44100,aformat=sample_fmts=fltp:channel_layouts=stereo"
        if clip["fade_in"]>0:a+=f",afade=t=in:st=0:d={clip['fade_in']:.6f}"
        if clip["fade_out"]>0:a+=f",afade=t=out:st={length-clip['fade_out']:.6f}:d={clip['fade_out']:.6f}"
        a+=f",volume={clip['volume']:.4f},adelay={round(clip['start']*1000)}:all=1[a{idx}]"
        expressions.append(a)
        audio_labels.append(f"[a{idx}]")
    if audio_labels:
        if len(audio_labels)==1:
            expressions.append(f"{audio_labels[0]}atrim=duration={duration:.6f},asetpts=PTS-STARTPTS[aout]")
        else:
            expressions.append("".join(audio_labels)+f"amix=inputs={len(audio_labels)}:"
                               f"duration=longest:dropout_transition=0:normalize=0,"
                               f"atrim=duration={duration:.6f},asetpts=PTS-STARTPTS[aout]")
    return args,";".join(expressions),bool(audio_labels)


def load_project(path):
    p=Path(path)
    if p.suffix.lower()!=".json" or not p.is_file():
        raise ValueError("existing JSON project required")
    if p.stat().st_size>120_000:
        raise ValueError("project file exceeds safe limit")
    return json.loads(p.read_text(encoding="utf-8-sig"))


def resolve_relative(project, base):
    """Copy of project whose relative clip paths are anchored at base (the project file's folder).

    Project files keep paths relative to their own folder so they stay portable and never leak a machine path."""
    doc=json.loads(json.dumps(project))
    base=Path(base)
    for track in doc.get("tracks") or []:
        for clip in track.get("clips") or []:
            src=clip.get("path")
            if isinstance(src,str) and src and "://" not in src:
                path=Path(src).expanduser()
                if not path.is_absolute():
                    clip["path"]=str(base/path)
    return doc


def render(project, output, *, dry_run=False):
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise ValueError("FFmpeg and FFprobe required")
    valid=validate(project,output=output)
    ins,graph,with_audio=filters_and_inputs(valid)
    args=["ffmpeg","-hide_banner","-loglevel","error","-nostdin","-n",*ins,
          "-filter_complex",graph,"-map","[vout]"]
    if with_audio:args+=["-map","[aout]"]
    else:args+=["-an"]
    args+=["-r",str(valid["fps"]),"-frames:v",str(math.ceil(valid["duration"]*valid["fps"])),
           "-c:v","libx264","-crf","19","-pix_fmt","yuv420p"]
    if with_audio:args+=["-c:a","aac","-b:a","192k"]
    args+=["-movflags","+faststart","-t",f"{valid['duration']:.6f}",str(output)]
    if dry_run:
        return {"valid":True,"clips":len(valid["clips"]),"video_layers":sum(x["kind"]!="audio" for x in valid["clips"]),
                "audio_layers":sum(x["include_audio"] for x in valid["clips"]),
                "frames":math.ceil(valid["duration"]*valid["fps"]),"render_executed":False}
    subprocess.run(args,check=True,capture_output=True,timeout=TIMEOUT)
    dest=Path(output)
    md=probing(dest)
    streams=md["streams"]
    video=next((x for x in streams if x.get("codec_type")=="video"),None)
    audio=next((x for x in streams if x.get("codec_type")=="audio"),None)
    expected=math.ceil(valid["duration"]*valid["fps"])
    if not video or video.get("codec_name")!="h264" or int(video.get("nb_frames",0))!=expected:
        raise ValueError("output video verification failed")
    if with_audio and (not audio or audio.get("codec_name")!="aac"):
        raise ValueError("output AAC verification failed")
    if not with_audio and audio:
        raise ValueError("unexpected output audio")
    actual=float(md["format"]["duration"])
    if abs(actual-valid["duration"])>1/valid["fps"]+.09:
        raise ValueError("output duration mismatch")
    return {"schema":"kosif.timeline-render-receipt.v1","verified":True,
            "frames":expected,"fps":valid["fps"],"width":video["width"],"height":video["height"],
            "duration_seconds":actual,"clips":len(valid["clips"]),
            "video_layers":sum(x["kind"]!="audio" for x in valid["clips"]),
            "audio_layers":sum(x["include_audio"] for x in valid["clips"]),
            "video_codec":"h264","audio_codec":"aac" if audio else None,
            "sha256":hashlib.sha256(dest.read_bytes()).hexdigest(),"bytes":dest.stat().st_size,
            "source_files_unchanged":True,"output":str(dest)}


def edit(project, action, clip_id, fields):
    # Never modifies source project; write an independent new revision.
    data=json.loads(json.dumps(project))
    validate(data,do_probe=False)
    if action not in ("move","trim","fade"):
        raise ValueError("unsupported edit operation")
    found=[c for t in data["tracks"] for c in t["clips"] if c["id"]==clip_id]
    if len(found)!=1:raise ValueError("clip not found")
    clip=found[0]
    allowed={"move":{"start"},"trim":{"in","duration"},"fade":{"fade_in","fade_out"}}[action]
    if not fields or any(k not in allowed for k in fields):
        raise ValueError("invalid edit fields")
    history=data.setdefault("history",{"past":[],"future":[]})
    if not isinstance(history,dict) or not isinstance(history.get("past"),list) or not isinstance(history.get("future"),list):
        raise ValueError("invalid history")
    # Whole-project snapshots preserve reversible clip layer/track changes.
    before=json.loads(json.dumps(data["tracks"]))
    for key,value in fields.items():
        clip[key]=number(value,key,0,60)
    validate(data,do_probe=False)
    history["past"]=(history["past"]+[before])[-10:]
    history["future"]=[]
    return data


def step_history(project, action):
    if action not in ("undo","redo"):
        raise ValueError("expected undo/redo")
    data=json.loads(json.dumps(project))
    hist=data.get("history")
    if not isinstance(hist,dict) or not isinstance(hist.get("past"),list) or not isinstance(hist.get("future"),list):
        raise ValueError("no edit history")
    src="past" if action=="undo" else "future"
    dst="future" if action=="undo" else "past"
    if not hist[src]:
        raise ValueError("no "+action+" snapshot available")
    current=json.loads(json.dumps(data["tracks"]))
    data["tracks"]=hist[src].pop()
    hist[dst].append(current)
    validate(data,do_probe=False)
    return data


def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest="action",required=True)
    sub.add_parser("doctor")
    check=sub.add_parser("check");check.add_argument("--project",required=True)
    ren=sub.add_parser("render");ren.add_argument("--project",required=True);ren.add_argument("--output",required=True)
    patch=sub.add_parser("edit");patch.add_argument("--project",required=True);patch.add_argument("--output",required=True)
    for action in ("undo","redo"):
        rev=sub.add_parser(action)
        rev.add_argument("--project",required=True)
        rev.add_argument("--output",required=True)
    patch.add_argument("--operation",choices=["move","trim","fade"],required=True)
    patch.add_argument("--clip",required=True)
    for field in ("start","source-in","duration","fade-in","fade-out"):
        patch.add_argument("--"+field,type=float,default=None)
    a=p.parse_args()
    try:
        if a.action=="doctor":
            print(json.dumps({"ready":bool(shutil.which("ffmpeg") and shutil.which("ffprobe")),
                 "schema":SCHEMA,"media_kinds":list(KINDS),
                 "video":"H264","audio":"AAC","max_duration_s":60,"max_clips":MAX_CLIPS}))
            return 0
        data=load_project(a.project)
        anchored=resolve_relative(data,Path(a.project).parent)
        if a.action=="check":
            valid=validate(anchored)
            print(json.dumps({"valid":True,"clips":len(valid["clips"]),"tracks":len(data["tracks"]),
                              "duration":valid["duration"],"fps":valid["fps"]}))
            return 0
        if a.action=="render":
            print(json.dumps(render(anchored,a.output),ensure_ascii=False))
            return 0
        out=Path(a.output)
        if out.suffix.lower()!=".json" or out.exists() or not out.parent.is_dir():
            raise ValueError("edited project must be a NEW JSON file in an existing folder")
        if a.action in ("undo","redo"):
            updated=step_history(data,a.action)
            op=a.action
            clip_id=None
        else:
            fields={}
            for raw,key in (("start","start"),("source_in","in"),("duration","duration"),
                            ("fade_in","fade_in"),("fade_out","fade_out")):
                value=getattr(a,raw)
                if value is not None:fields[key]=value
            updated=edit(data,a.operation,a.clip,fields)
            op=a.operation
            clip_id=a.clip
        out.write_text(json.dumps(updated,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        print(json.dumps({"saved":True,"operation":op,"clip":clip_id,"new_project":str(out)}))
        return 0
    except (OSError,ValueError,KeyError,json.JSONDecodeError,subprocess.CalledProcessError,
            subprocess.TimeoutExpired) as exc:
        print(json.dumps({"error":str(exc),"success":False},ensure_ascii=False),file=sys.stderr)
        return 1

if __name__=="__main__":
    raise SystemExit(main())
