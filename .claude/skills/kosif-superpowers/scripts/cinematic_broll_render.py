#!/usr/bin/env python3
"""Render a REAL footage-first camera-motion b-roll master from audited KOSIF EDL.

Refuses unverified/unlicensed footage, preserves original audio stream by
copying into a compatible container; no audio enhancement or transcript editing.
This tool does NOT create original Arabic captions or license footage for you.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import shutil
import subprocess
import tempfile
from pathlib import Path


def invoke(argv):
    return subprocess.run(argv, check=True, capture_output=True, text=True)


def probe(path: Path) -> dict:
    response=invoke(["ffprobe","-v","error","-count_frames","-show_streams","-show_format","-of","json",str(path)])
    return json.loads(response.stdout)


def encoded_audio_hash(path: Path) -> str:
    """Hash encoded audio packets without decoding or modifying the recording."""
    out=invoke(["ffmpeg","-v","error","-nostdin","-i",str(path),"-map","0:a:0",
                "-c:a","copy","-f","hash","-hash","SHA256","-"])
    return out.stdout.strip()


def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1048576),b""):
            h.update(block)
    return h.hexdigest()


def check_scene_timeline(edl):
    frames=edl["video"]["frame_count"]
    if edl.get("production_ready") is not True or edl.get("blockers"):
        raise ValueError("EDL not production-ready; resolve blocking real-footage gaps first")
    if edl["audio"].get("preserve_original") is not True or edl["audio"].get("audio_editing_allowed") is not False:
        raise ValueError("EDL must preserve immutable master audio")
    if not isinstance(frames,int) or frames < 1:
        raise ValueError("invalid frame count")
    previous=0
    for idx,s in enumerate(edl["scenes"]):
        if s.get("start_frame") != previous or type(s.get("end_frame_exclusive")) is not int:
            raise ValueError(f"gap/overlap before scene {idx}")
        if s["end_frame_exclusive"] <= previous or s.get("rights_status") != "verified":
            raise ValueError(f"invalid scene {idx}")
        previous=s["end_frame_exclusive"]
    if previous != frames:
        raise ValueError("EDL does not cover the full audio timeline")


def verify_footage(edl, manifest, location: Path):
    clip_map={}
    for c in manifest:
        if not isinstance(c,dict) or not c.get("id") or c["id"] in clip_map:
            raise ValueError("missing or duplicate manifest clip ID")
        clip_map[c["id"]]=c
    selected={}
    for s in edl["scenes"]:
        cid=s.get("footage_id")
        if cid not in clip_map:
            raise ValueError(f"missing source for {cid}")
        c=clip_map[cid]
        from cinematic_cut_planner import clean_clip
        good,why=clean_clip(c)
        if not good:
            raise ValueError(f"source {cid} blocked: {why}")
        if not str(c.get("license_evidence_url") or c.get("license_document") or "").strip():
            raise ValueError(f"source {cid} lacks documented license evidence")
        source=Path(str(c["path"])).expanduser()
        if not source.is_absolute():
            source=location/source
        if not source.is_file():
            raise FileNotFoundError(f"source {cid} not found: {source}")
        if source != Path(s["footage_path"]) and str(s["footage_path"]) != str(c["path"]):
            # EDL and manifest source paths must be exactly traceable
            raise ValueError(f"EDL path disagrees with manifest for {cid}")
        claimed=str(c.get("sha256") or "").lower()
        if len(claimed)!=64 or claimed != sha256(source):
            raise ValueError(f"source {cid} SHA256 missing or incorrect")
        if cid not in selected:
            stream=next((v for v in probe(source)["streams"] if v["codec_type"]=="video"),None)
            if not stream:
                raise ValueError(f"source {cid} does not contain a video stream")
            if stream.get("width")!=int(c["width"]) or stream.get("height")!=int(c["height"]):
                raise ValueError(f"source {cid} dimensions differ from manifest")
            src_duration=float(probe(source)["format"].get("duration",0))
            fps=int(edl["video"]["fps"])
            needed=max((s["end_frame_exclusive"]-s["start_frame"])/fps
                       for s in edl["scenes"] if s["footage_id"]==cid)
            if src_duration + (1/fps) < needed:
                raise ValueError(f"source {cid} actually too short for required shot")
            selected[cid]=source
    return selected


def camera_filter(move: str, count: int, fps: int, width: int, height: int) -> str:
    progress=f"(on/{max(1,count-1)})"
    if move=="slow_pull_back":
        zoom=f"(1.15-0.1*{progress})"
    else:
        zoom=f"(1.04+0.09*{progress})"
    if move=="gentle_pan_right":
        x=f"(iw-iw/zoom)*(0.15+0.7*{progress})"
    elif move=="gentle_pan_left":
        x=f"(iw-iw/zoom)*(0.85-0.7*{progress})"
    else:
        x="(iw-iw/zoom)/2"
    y="(ih-ih/zoom)/2"
    return (f"fps={fps},"
            f"scale={width*2}:{height*2}:force_original_aspect_ratio=increase:flags=lanczos,"
            f"crop={width*2}:{height*2},setsar=1,"
            f"zoompan=z='{zoom}':x='{x}':y='{y}':d=1:s={width}x{height}:fps={fps},"
            f"tpad=stop_mode=clone:stop_duration=1,"
            f"trim=end_frame={count},setpts=N/({fps}*TB),format=yuv420p")


def render(edl_file, manifest_file, audio_file, destination, width=1080, height=1920, codec="libx264"):
    # cheap output checks first, so a wrong name never costs a whole render
    if destination.suffix.lower() not in (".mkv",".mp4"):
        raise ValueError("use .mkv for immutable audio master or .mp4 when compatible")
    if destination.exists():
        raise FileExistsError("refusing to overwrite output")
    if codec not in ("libx264","libx265"):
        raise ValueError("unsupported codec")
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise RuntimeError("FFmpeg and FFprobe must be installed")
    edl=json.loads(edl_file.read_text(encoding="utf-8"))
    manifest=json.loads(manifest_file.read_text(encoding="utf-8"))
    if not isinstance(manifest,list):
        raise ValueError("expected a reviewed-footage JSON array")
    check_scene_timeline(edl)
    audio_info=probe(audio_file)
    audio=next((s for s in audio_info["streams"] if s["codec_type"]=="audio"),None)
    if not audio:
        raise ValueError("provided master has no audio")
    duration=float(edl["audio"]["duration"])
    actual=float(audio_info["format"]["duration"])
    if abs(actual-duration)>.04:
        raise ValueError("EDL duration differs from audio master")
    fps=int(edl["video"]["fps"])
    if fps not in (24,25,30,60) or width<32 or height<32 or width%2 or height%2:
        raise ValueError("invalid render dimensions/fps")
    selected=verify_footage(edl,manifest,manifest_file.parent)
    destination.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="kosif_cinematic_") as tmp:
        work=Path(tmp)
        clips=[]
        for i,scene in enumerate(edl["scenes"]):
            n=scene["end_frame_exclusive"]-scene["start_frame"]
            filt=camera_filter(scene.get("camera",{}).get("move","slow_push_in"),n,fps,width,height)
            out=work/f"shot_{i:05d}.mp4"
            invoke(["ffmpeg","-hide_banner","-loglevel","error","-nostdin","-y",
                    "-i",str(selected[scene["footage_id"]]),
                    "-map","0:v:0","-an","-vf",filt,"-frames:v",str(n),
                    "-c:v",codec,"-preset","slow","-crf","17","-pix_fmt","yuv420p",
                    "-r",str(fps),"-video_track_timescale",str(fps*1000),str(out)])
            item=probe(out)
            frame_count=int(next(s for s in item["streams"] if s["codec_type"]=="video")["nb_frames"])
            if frame_count != n:
                raise ValueError(f"shot {i} rendered {frame_count}, expected {n} frames")
            clips.append(out)
        concat=work/"shots.ffconcat"
        concat.write_text("ffconcat version 1.0\n"+"".join(
            "file '"+p.as_posix().replace("'","'\\''")+"'\n" for p in clips),encoding="utf-8")
        silent=work/"visual.mp4"
        invoke(["ffmpeg","-hide_banner","-loglevel","error","-nostdin","-y",
                "-safe","0","-f","concat","-i",str(concat),
                "-map","0:v:0","-c:v","copy",str(silent)])
        try:
            invoke(["ffmpeg","-hide_banner","-loglevel","error","-nostdin","-y",
                    "-i",str(silent),"-i",str(audio_file),"-map","0:v:0","-map","1:a:0",
                    "-c:v","copy","-c:a","copy",str(destination)])
        except subprocess.CalledProcessError as e:
            if destination.exists():
                destination.unlink()
            raise RuntimeError("audio stream copy not supported in requested container; use .mkv") from e
    check=probe(destination)
    v=next(s for s in check["streams"] if s["codec_type"]=="video")
    a=next((s for s in check["streams"] if s["codec_type"]=="audio"),None)
    final_frames = int(v.get("nb_frames") or v.get("nb_read_frames") or 0)
    if not a or final_frames!=edl["video"]["frame_count"]:
        destination.unlink(missing_ok=True)
        raise ValueError("output failed frame/audio verification")
    original_audio_packets=encoded_audio_hash(audio_file)
    delivered_audio_packets=encoded_audio_hash(destination)
    if original_audio_packets != delivered_audio_packets:
        destination.unlink(missing_ok=True)
        raise ValueError("audio bitstream was altered despite stream-copy request")
    return {"path":str(destination),"video_frames":final_frames,
            "width":v["width"],"height":v["height"],"fps":fps,
            "audio_codec":a["codec_name"],"audio_stream_copied":True,
            "audio_original_sha256":sha256(audio_file),
            "audio_packet_sha256":original_audio_packets,
            "audio_bitstream_verified_identical":True,
            "scope":"camera-motion b-roll master; Arabic text overlays not rendered"}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--edl",type=Path,required=True)
    ap.add_argument("--manifest",type=Path,required=True)
    ap.add_argument("--audio",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    ap.add_argument("--width",type=int,default=1080)
    ap.add_argument("--height",type=int,default=1920)
    args=ap.parse_args()
    try:
        result=render(args.edl,args.manifest,args.audio,args.out,args.width,args.height)
    except (OSError, ValueError, RuntimeError, KeyError, subprocess.CalledProcessError) as exc:
        ap.error(f"{type(exc).__name__}: {exc}")
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
