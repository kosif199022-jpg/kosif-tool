#!/usr/bin/env python3
"""KOSIF Character IK: analytic two-bone arm, word-cued motion, actual image/video.
Original code; delegates primitive drawing to creative_paint.py.
No model-based character generation or commercial editor internals.
"""
import argparse
import hashlib
import json
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from PIL import Image

from creative_paint import paint, svg, color, num

MAX_FRAMES=600
SCHEMA="kosif.ik.v1"

def point(p):
    if not isinstance(p,list) or len(p)!=2: raise ValueError("point must be [x,y]")
    return (num(p[0],-10000,10000),num(p[1],-10000,10000))

def solve_ik(shoulder,target,upper,lower,bend=1):
    """Law-of-cosines two-bone IK. Exact bone lengths; clamps unreachable targets."""
    x,y=point(list(shoulder));tx,ty=point(list(target))
    a=num(upper,1,5000);b=num(lower,1,5000)
    if bend not in (-1,1):raise ValueError("bend must be -1 or 1")
    dx,dy=tx-x,ty-y;raw=math.hypot(dx,dy)
    direction=(dx/raw,dy/raw) if raw>1e-12 else (1.0,0.0)
    dist=max(abs(a-b)+1e-6,min(a+b-1e-6,raw))
    wrist=(x+direction[0]*dist,y+direction[1]*dist)
    projection=(a*a-b*b+dist*dist)/(2*dist)
    height=math.sqrt(max(0,a*a-projection*projection))
    elbow=(x+direction[0]*projection-bend*direction[1]*height,
           y+direction[1]*projection+bend*direction[0]*height)
    return {"shoulder":(x,y),"elbow":elbow,"wrist":wrist,
            "desired":(tx,ty),"clamped":abs(dist-raw)>1e-4,
            "end_error":math.hypot(wrist[0]-tx,wrist[1]-ty)}

def words_from_file(path):
    if path is None:return []
    src=json.loads(Path(path).read_text(encoding="utf-8-sig"))
    words=src["words"] if isinstance(src,dict) else src
    if not isinstance(words,list):raise ValueError("words JSON must contain array")
    prev=-1
    for w in words:
        if not isinstance(w,dict) or not isinstance(w.get("word"),str):raise ValueError("bad word entry")
        start=num(w.get("start"),0,3600);end=num(w.get("end"),start,3600)
        if start<prev:raise ValueError("words must be sorted by start")
        prev=start
    return words

def resolve(scene,words):
    if not isinstance(scene,dict) or scene.get("schema")!=SCHEMA:raise ValueError("bad IK schema")
    w=scene.get("width");h=scene.get("height");duration=num(scene.get("duration"),0.1,30)
    if not isinstance(w,int) or not isinstance(h,int) or not (128<=w<=2048 and 128<=h<=2048):raise ValueError("bad dimensions")
    color(scene.get("background","#F4F0E6"))
    rig=scene.get("rig",{})
    if not isinstance(rig,dict):raise ValueError("rig is not an object")
    shoulder=point(rig.get("shoulder"))
    upper=num(rig.get("upper"),5,1000);lower=num(rig.get("lower"),5,1000)
    bend=rig.get("bend",1)
    if type(bend) is not int or bend not in (-1,1):raise ValueError("bad bend")
    color(rig.get("skin","#E6BF96"));color(rig.get("clothes","#355B47"))
    for v in ("body_width","head_radius","arm_width"):
        if v in rig:num(rig[v],4,500)
    cues=scene.get("targets")
    if not isinstance(cues,list) or not 1<=len(cues)<=100:raise ValueError("targets must be 1..100")
    resolved=[];lastend=-1
    for i,cue in enumerate(cues):
        if not isinstance(cue,dict):raise ValueError("bad target")
        if ("time" in cue)==("word" in cue):raise ValueError("target requires exactly time or word")
        if "time" in cue:at=num(cue["time"],0,duration)
        else:
            match=cue["word"];n=cue.get("occurrence",1)
            if not isinstance(match,str) or not isinstance(n,int) or n<1:raise ValueError("bad cue")
            matching=[x for x in words if x["word"].strip()==match.strip()]
            if len(matching)<n:raise ValueError("word cue not found")
            at=num(matching[n-1]["start"],0,duration)
        travel=num(cue.get("travel",.25),0,5)
        if i==0:
            if abs(at)>1e-9 or travel!=0:raise ValueError("first target must start at 0 with travel=0")
        elif at<lastend-1e-8:raise ValueError("overlapping or unsorted target transitions")
        if at+travel>duration+1e-8:raise ValueError("target travel extends beyond duration")
        xy=point(cue.get("point"))
        resolved.append({"time":at,"point":xy,"travel":travel,"word":cue.get("word")})
        lastend=at+travel
    return {"width":w,"height":h,"duration":duration,"background":scene.get("background","#F4F0E6"),
            "rig":{"shoulder":shoulder,"upper":upper,"lower":lower,"bend":bend,
                   "skin":rig.get("skin","#E6BF96"),"clothes":rig.get("clothes","#355B47"),
                   "body_width":rig.get("body_width",100),"head_radius":rig.get("head_radius",65),
                   "arm_width":rig.get("arm_width",24)},
            "cues":resolved}

def target_at(prepared,t):
    t=num(t,0,prepared["duration"])
    current=prepared["cues"][0]["point"]
    for c in prepared["cues"][1:]:
        if t<c["time"]:break
        if t<c["time"]+c["travel"] and c["travel"]>0:
            u=(t-c["time"])/c["travel"]
            u=u*u*(3-2*u)
            return tuple(old*(1-u)+new*u for old,new in zip(current,c["point"]))
        current=c["point"]
    return current

def figure(prepared,t):
    """Produces standard validated creative_paint scene with independent limbs."""
    w,h=prepared["width"],prepared["height"];r=prepared["rig"]
    x,y=r["shoulder"]; upper,lower=r["upper"],r["lower"]
    desired=target_at(prepared,t)
    arm=solve_ik((x,y),desired,upper,lower,r["bend"])
    def pt(q):return [round(q[0],4),round(q[1],4)]
    skin=r["skin"];shirt=r["clothes"];ink="#172824"
    hand=arm["wrist"];elbow=arm["elbow"]
    bw=r["body_width"];head=r["head_radius"];bodybottom=min(h-25,y+head*2.1)
    def line(a,b,fill,width):return {"kind":"line","points":[pt(a),pt(b)],"stroke":fill,"stroke_width":width}
    def ellipse(cx,cy,rx,ry,fill,stroke=ink,sw=3):
        return {"kind":"ellipse","x":cx-rx,"y":cy-ry,"width":2*rx,"height":2*ry,"fill":fill,"stroke":stroke,"stroke_width":sw}
    art=[
        {"kind":"rectangle","x":0,"y":h-65,"width":w,"height":65,"fill":"#E9D9B9","stroke_width":0},
        {"kind":"polygon","points":[[x-bw/2,y-2],[x+bw/2,y-2],[x+bw*.54,bodybottom],[x-bw*.54,bodybottom]],"fill":shirt,"stroke":ink,"stroke_width":4},
        ellipse(x,y-head*1.58,head,head*1.1,skin),
        ellipse(x-head*.32,y-head*1.68,head*.08,head*.08,ink,ink,0),
        ellipse(x+head*.32,y-head*1.68,head*.08,head*.08,ink,ink,0),
        line((x-head*.25,y-head*1.30),(x+head*.25,y-head*1.30),ink,3),
        line((x-bw*.42,y+10),(x-bw*.42-25,bodybottom-10),shirt,r["arm_width"]),
        line((x,y),elbow,shirt,r["arm_width"]+5),
        line(elbow,hand,skin,r["arm_width"]),
        ellipse(x,y,8,8,ink,ink,0),
        ellipse(elbow[0],elbow[1],r["arm_width"]*.45,r["arm_width"]*.45,skin,ink,2),
        ellipse(hand[0],hand[1],r["arm_width"]*.6,r["arm_width"]*.6,skin,ink,2)
    ]
    return {"schema":"kosif.paint.v1","width":w,"height":h,"background":prepared["background"],
            "layers":[{"name":"ik-character","visible":True,"opacity":1,"shapes":art}]},arm

def probe(path,select):
    args=["ffprobe","-v","error","-select_streams",select,"-show_entries","stream=codec_name,duration","-of","json",str(path)]
    data=json.loads(subprocess.run(args,check=True,capture_output=True,text=True).stdout)
    return data.get("streams",[])

def packet_hashes(file):
    args=["ffprobe","-v","error","-select_streams","a:0","-show_packets","-show_data_hash","sha256",
          "-show_entries","packet=data_hash","-of","json",str(file)]
    result=json.loads(subprocess.run(args,check=True,capture_output=True,text=True).stdout)
    return [p["data_hash"] for p in result.get("packets",[]) if "data_hash" in p]

def export(prepared,out,fps=24,time=0,audio=None):
    out=Path(out);fps=int(num(fps,1,60))
    if out.exists():raise ValueError("Refusing to overwrite")
    suffix=out.suffix.lower()
    if suffix not in (".png",".svg",".gif",".mp4"):raise ValueError("Use .png .svg .gif .mp4")
    if audio and suffix!=".mp4":raise ValueError("--audio is supported only with MP4 output")
    if suffix in (".png",".svg"):
        scene,arm=figure(prepared,time)
        if suffix==".png":paint(scene).save(out)
        else:out.write_text(svg(scene),encoding="utf-8")
        frames=1
    elif suffix in (".gif",".mp4"):
        n=round(prepared["duration"]*fps)
        if abs(n/fps-prepared["duration"])>1e-8:raise ValueError("duration*fps must be an exact frame count")
        if n>MAX_FRAMES:raise ValueError("frame count exceeds safety limit")
        if suffix==".mp4" and not (shutil.which("ffmpeg") and shutil.which("ffprobe")):
            raise ValueError("MP4 needs ffmpeg and ffprobe on PATH")
        if audio:
            tracks=probe(audio,"a:0")
            if not tracks or tracks[0]["codec_name"]!="aac":raise ValueError("Pass compatible AAC input for stream-copy to MP4")
            source_duration=float(tracks[0].get("duration") or 0)
            if abs(source_duration-prepared["duration"])>1/fps+.02:raise ValueError("audio length must match scene duration")
        with tempfile.TemporaryDirectory(prefix="kosif-ik-") as td:
            folder=Path(td);frames=[]
            for i in range(n):
                scene,_=figure(prepared,i/fps)
                im=paint(scene).convert("RGB")
                if suffix==".gif":frames.append(im)
                else:im.save(folder/f"{i:05d}.png")
            # Build and verify inside the temp folder; only a verified file reaches --output.
            final=folder/("final"+suffix)
            if suffix==".gif":
                frames[0].save(final,save_all=True,append_images=frames[1:],duration=round(1000/fps),loop=0,optimize=False)
            else:
                temp=folder/"silent.mp4"
                cmd=["ffmpeg","-v","error","-y","-framerate",str(fps),"-i",str(folder/"%05d.png"),
                    "-frames:v",str(n),"-c:v","libx264","-pix_fmt","yuv420p","-crf","18",str(temp)]
                subprocess.run(cmd,check=True,capture_output=True)
                if audio:
                    cmd=["ffmpeg","-v","error","-y","-i",str(temp),"-i",str(audio),
                         "-map","0:v:0","-map","1:a:0","-c:v","copy","-c:a","copy","-movflags","+faststart",str(final)]
                    subprocess.run(cmd,check=True,capture_output=True)
                    if packet_hashes(audio)!=packet_hashes(final):raise ValueError("audio packet hashes changed")
                else:shutil.copyfile(temp,final)
                video=probe(final,"v:0")
                if not video or video[0].get("codec_name")!="h264":raise ValueError("invalid H.264 video")
            if out.exists():raise ValueError("output appeared concurrently; not overwriting")
            shutil.copyfile(final,out)
        frames=n
    digest=hashlib.sha256(out.read_bytes()).hexdigest()
    return {"output":str(out),"verified":out.exists() and out.stat().st_size>100,
            "frames":frames,"fps":fps,"audio_packet_copy_verified":bool(audio),
            "sha256":digest,"cue_times":[{"time":c["time"],"word":c["word"]} for c in prepared["cues"]]}

def main(argv=None):
    ap=argparse.ArgumentParser(description="Original IK Character animator, timed words -> real images/video")
    sub=ap.add_subparsers(dest="command",required=True)
    sub.add_parser("doctor")
    render=sub.add_parser("render")
    for a in ("--scene","--output"):render.add_argument(a,required=True)
    render.add_argument("--words");render.add_argument("--fps",type=int,default=24)
    render.add_argument("--time",type=float,default=0);render.add_argument("--audio")
    args=ap.parse_args(argv)
    if args.command=="doctor":
        print(json.dumps({"schema":SCHEMA,"pillow":Image.__version__,"ffmpeg":bool(shutil.which("ffmpeg")),
                          "ffprobe":bool(shutil.which("ffprobe")),"formats":["png","svg","gif","mp4"],"max_frames":MAX_FRAMES}))
        return 0
    try:
        words=words_from_file(args.words)
        scene=json.loads(Path(args.scene).read_text(encoding="utf-8-sig"))
        prep=resolve(scene,words)
        data=export(prep,args.output,args.fps,args.time,args.audio)
        print(json.dumps(data,ensure_ascii=False));return 0
    except (ValueError,KeyError,OSError,json.JSONDecodeError,subprocess.CalledProcessError) as exc:
        print(json.dumps({"verified":False,"error":str(exc)},ensure_ascii=False),file=sys.stderr)
        return 1

if __name__=="__main__":raise SystemExit(main())
