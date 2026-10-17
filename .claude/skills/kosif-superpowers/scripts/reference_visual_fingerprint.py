#!/usr/bin/env python3
"""KOSIF Reference Visual Fingerprint: real sampled palette, exposure and frame motion.

Reads ONLY an authorized local video via ffprobe/ffmpeg, downsamples frames to
64x36 at 2 FPS and reports aggregate measurements. Outputs no source video
frames, no face identity or original graphic assets. Pixel change != object
tracking, camera recognition, motion capture or semantic understanding.

The tool never downloads models/packages and never edits the input.
"""
from __future__ import annotations
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import shutil
import subprocess

from motion_reference_probe import probe as probe_video

W, H, FPS = 64, 36, 2
STRIDE=W*H*3
MAX_DURATION=120.0
MAX_OUTPUT=int(MAX_DURATION*FPS+2)*STRIDE


def num(value,name,lo,hi):
    if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or not lo<=value<=hi:
        raise ValueError(f"{name}: finite number in range {lo}..{hi} required")
    return float(value)


def read_frames(source,duration):
    if not shutil.which("ffmpeg"):
        raise ValueError("ffmpeg is required for actual frame decoding")
    # Limit duration and decoded bytes. The file must have been validated as a
    # local path and measured by ffprobe first.
    cmd=["ffmpeg","-nostdin","-hide_banner","-v","error",
         "-i",str(Path(source).resolve()),"-an","-sn","-dn",
         "-vf",f"fps={FPS},scale={W}:{H}:flags=bilinear,format=rgb24",
         "-pix_fmt","rgb24","-f","rawvideo","-frames:v",str(math.ceil(duration*FPS)+1),"pipe:1"]
    try:
        result=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                              stdin=subprocess.DEVNULL,timeout=150,check=False)
    except subprocess.TimeoutExpired as exc:
        raise ValueError("video decode exceeded time bound") from exc
    if result.returncode!=0 or not result.stdout:
        raise ValueError("ffmpeg frame decode failed")
    raw=result.stdout
    if len(raw)>MAX_OUTPUT or len(raw)%STRIDE:
        raise ValueError("decoded frames exceed bounded raw RGB size")
    return [raw[i:i+STRIDE] for i in range(0,len(raw),STRIDE)]


def _pixels(frame):
    if not isinstance(frame,(bytes,bytearray)) or len(frame)!=STRIDE:
        raise ValueError("expected single 64x36 RGB frame")
    return list(zip(frame[0::3],frame[1::3],frame[2::3]))


def frame_features(frame):
    pixels=_pixels(frame)
    count=len(pixels)
    mean=[sum(p[k] for p in pixels)/count for k in range(3)]
    # ITU-R BT.709 approximation in display RGB, not calibrated linear light.
    lum=[(54*p[0]+183*p[1]+19*p[2])>>8 for p in pixels]
    avg=sum(lum)/count
    contrast=math.sqrt(sum((y-avg)**2 for y in lum)/count)
    bins=Counter(((r>>5),(g>>5),(b>>5)) for r,g,b in pixels)
    common=bins.most_common(4)
    palette=[{"hex":"#"+ "".join(f"{min(255,32*c+16):02x}" for c in key),
              "share":round(n/count,4)} for key,n in common]
    return {"mean_rgb":[round(x,3) for x in mean],
            "luma":round(avg/255,5),"contrast":round(contrast/255,5),
            "saturation_proxy":round(sum(max(p)-min(p) for p in pixels)/(count*255),5),
            "palette":palette, "luma_pixels":lum}


def _motion(previous,current):
    # Coarse translational matching of a sparse luminance grid. Changes from
    # moving actors, cuts or lighting can mimic camera translation. We flag this
    # as a *candidate* when a translated match materially improves alignment.
    def mse(dx,dy):
        total=0;n=0
        for y in range(5,H-5,2):
            for x in range(5,W-5,2):
                a=previous[y*W+x];b=current[(y+dy)*W+x+dx]
                total+=(a-b)**2;n+=1
        return total/n if n else 0.0
    baseline=mse(0,0)
    mean_luma=sum(previous)/len(previous)
    texture=math.sqrt(sum((v-mean_luma)**2 for v in previous)/len(previous))
    if baseline<50 or texture<8:
        return {"dx":0,"dy":0,"evidence":"insufficient texture/change"}
    best=(baseline,0,0)
    for dy in range(-3,4):
        for dx in range(-3,4):
            if dx==0 and dy==0:continue
            score=mse(dx,dy)
            if score<best[0]:
                best=(score,dx,dy)
    if best[0]>baseline*.77:
        return {"dx":0,"dy":0,"evidence":"no confident global displacement"}
    return {"dx":best[1],"dy":best[2],
            "improvement":round(1-best[0]/baseline,3),
            "evidence":"possible frame translation, not verified camera motion"}


def fingerprints(frames,duration,cuts=()):
    duration=num(duration,"duration",.1,MAX_DURATION)
    if not isinstance(frames,list) or not 1<=len(frames)<=MAX_DURATION*FPS+2:
        raise ValueError("frame sample list invalid")
    if not isinstance(cuts,(list,tuple)) or len(cuts)>79:
        raise ValueError("cut list invalid")
    bounds=[0.0];prev=0.0
    for v in cuts:
        sec=num(v,"cut",0,duration)
        if sec<=prev+.01 or sec>=duration-.01:raise ValueError("cuts must be ordered/in range")
        bounds.append(sec);prev=sec
    bounds.append(duration)
    features=[frame_features(frame) for frame in frames]
    sample_rows=[]
    previous=None
    for i,f in enumerate(features):
        row={"time":round(i/FPS,3),"luma":f["luma"],"contrast":f["contrast"],
             "saturation_proxy":f["saturation_proxy"],"mean_rgb":f["mean_rgb"]}
        if previous is not None:
            p=previous["luma_pixels"];c=f["luma_pixels"]
            row["change_ratio"]=round(sum(abs(a-b) for a,b in zip(p,c))/(len(p)*255),5)
            row["translation"]=_motion(p,c)
        sample_rows.append(row);previous=f
    sections=[]
    for idx,(start,end) in enumerate(zip(bounds,bounds[1:])):
        selected=[i for i,row in enumerate(sample_rows) if start<=row["time"]<end]
        if not selected:
            # Very short shots (< .5s) might have no sampled frame.
            near=min(range(len(sample_rows)),key=lambda i:abs(sample_rows[i]["time"]-(start+end)/2))
            selected=[near]
        colors=Counter()
        for i in selected:
            for p in features[i]["palette"]:
                # Weighted by each sample's actual histogram share.
                colors[p["hex"]]+=p["share"]
        ordered=[x for x,_ in colors.most_common(4)]
        def avg(k):return round(sum(sample_rows[i][k] for i in selected)/len(selected),5)
        changes=[sample_rows[i].get("change_ratio",0) for i in selected]
        shifts=[sample_rows[i].get("translation",{}) for i in selected]
        candidates=[x for x in shifts if x.get("improvement",0)>=.23]
        direction="none"
        if len(candidates)>=2:
            dx=sum(x["dx"] for x in candidates)
            dy=sum(x["dy"] for x in candidates)
            if abs(dx)>abs(dy)*1.4 and abs(dx)>=2:direction="horizontal_candidate"
            elif abs(dy)>=2:direction="vertical_candidate"
        sections.append({"index":idx,"start":round(start,4),"end":round(end,4),
                         "sample_count":len(selected),
                         "mean_luma":avg("luma"),"mean_contrast":avg("contrast"),
                         "saturation_proxy":avg("saturation_proxy"),
                         "change_ratio_mean":round(sum(changes)/len(changes),5),
                         "palette":ordered,
                         "possible_translation":direction,
                         "motion_candidate_count":len(candidates)})
    return {"schema":"kosif.reference-visual-fingerprint.v1",
            "duration":duration,"sample_fps":FPS,"sample_dimensions":[W,H],
            "sample_count":len(sample_rows),"sections":sections,
            "samples":sample_rows,
            "confidence":"observed low-resolution pixel statistics; high semantic uncertainty",
            "exclusions":["no reference pixels exported","no object/face tracking",
                          "no camera pose reconstruction","no style or rights transfer",
                          "not accurate colorimetry or cut classification"],
            "source_video_unchanged":True}


def analyze(input_path,probe_json=None):
    path=Path(input_path).expanduser()
    if not path.is_file() or path.is_symlink():
        raise ValueError("user-authorized local regular video required")
    metadata=probe_video(path,detect_cuts=False)
    duration=num(metadata["duration_seconds"],"video duration",.1,MAX_DURATION)
    cuts=[]
    if probe_json:
        report=json.loads(Path(probe_json).read_text(encoding="utf-8"))
        if (report.get("status")!="reference_timing_observed_not_animation_reconstructed"
            or abs(num(report.get("duration_seconds"),"probe duration",.1,300)-duration)>.25
            or report.get("cut_detection_run") is not True):
            raise ValueError("requires real matching cut-enabled reference probe report")
        cuts=report.get("cut_candidates_seconds",[])
    result=fingerprints(read_frames(path,duration),duration,cuts)
    result["source_name"]=path.name
    result["cut_report_provided"]=bool(probe_json)
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("video",help="authorized local video; under 120s")
    p.add_argument("--probe",help="matching output from motion_reference_probe.py --cuts")
    p.add_argument("--out",required=True,help="new JSON path; will never overwrite")
    args=p.parse_args()
    try:
        data=analyze(args.video,args.probe)
        dest=Path(args.out)
        if dest.is_symlink() or not dest.parent.is_dir():raise ValueError("output parent missing or unsafe")
        with dest.open("x",encoding="utf-8") as f:
            json.dump(data,f,ensure_ascii=False,indent=2)
            f.write("\n")
        print(json.dumps({"status":"measured_visual_fingerprint","output":str(dest.resolve()),
                          "samples":data["sample_count"],"sections":len(data["sections"]),
                          "camera_motion_verified":False,"reference_style_copied":False},ensure_ascii=False))
    except (OSError,ValueError,TypeError,json.JSONDecodeError) as e:
        p.error(str(e))


if __name__=="__main__":
    main()
