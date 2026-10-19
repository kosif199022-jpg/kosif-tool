#!/usr/bin/env python3
"""Original KOSIF software 3D renderer: basic primitives, keyframes and MP4; no Blender."""
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
from PIL import Image, ImageDraw

SCHEMA = "kosif.native3d.v1"
SHAPES = {"cube", "sphere", "cylinder"}
def vec(raw, max_abs=100.0):
    if not isinstance(raw,list) or len(raw)!=3 or any(type(v) not in (int,float) or
          not math.isfinite(v) or abs(v)>max_abs for v in raw):
        raise ValueError("expected three finite bounded coordinates")
    return tuple(float(v) for v in raw)
def integer(value, lo, hi):
    if type(value) is not int or not lo<=value<=hi:
        raise ValueError("integer out of bounds")
    return value
def rgb(value):
    if not isinstance(value,str) or len(value)!=7 or not value.startswith("#"):
        raise ValueError("hex RGB required")
    try:
        return tuple(int(value[i:i+2],16) for i in (1,3,5))
    except ValueError as exc:
        raise ValueError("invalid RGB hex") from exc
def norm(v):
    q=math.sqrt(sum(x*x for x in v))
    if q<1e-8: raise ValueError("zero length camera vector")
    return tuple(x/q for x in v)
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def cross(a,b):
    return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def mix(a,b,t):
    return tuple(x*(1-t)+y*t for x,y in zip(a,b))
def validate(scene):
    if not isinstance(scene,dict) or scene.get("schema")!=SCHEMA:
        raise ValueError("invalid KOSIF native 3D schema")
    w=integer(scene.get("width",640),128,1280)
    h=integer(scene.get("height",360),128,1280)
    fps=integer(scene.get("fps",24),1,60)
    frames=integer(scene.get("frames",120),1,240)
    if scene.get("render_mode", "painter") not in ("painter", "zbuffer"):
        raise ValueError("render mode must be painter or zbuffer")
    rgb(scene.get("background","#253543"))
    cam=scene.get("camera",{})
    if not isinstance(cam,dict):raise ValueError("camera must be an object")
    loc=vec(cam.get("position",[6,-10,7]))
    target=vec(cam.get("target",[0,0,.6]))
    norm(sub(target,loc))
    scale=cam.get("ortho_scale",7.0)
    if type(scale) not in (int,float) or not math.isfinite(scale) or not 1<=scale<=50:
        raise ValueError("invalid ortho scale")
    objects=scene.get("objects")
    if not isinstance(objects,list) or not 1<=len(objects)<=60:
        raise ValueError("objects length must be from 1 to 60")
    for obj in objects:
        if not isinstance(obj,dict) or obj.get("shape") not in SHAPES:
            raise ValueError("invalid shape")
        vec(obj.get("location",[0,0,0]))
        sc=vec(obj.get("scale",[1,1,1]),50)
        if any(x<=.01 for x in sc):raise ValueError("positive scales required")
        rgb(obj.get("color","#4E896A"))
        yaw=obj.get("yaw",0)
        if type(yaw) not in (int,float) or not math.isfinite(yaw) or abs(yaw)>3600:
            raise ValueError("invalid rotation")
        keys=obj.get("keyframes",[])
        if not isinstance(keys,list) or len(keys)>32:
            raise ValueError("too many keyframes")
        last=0
        for key in keys:
            if not isinstance(key,dict):
                raise ValueError("invalid keyframe")
            f=integer(key.get("frame"),1,frames)
            if f<=last: raise ValueError("keyframes must be strictly ordered")
            last=f
            if "location" in key:vec(key["location"])
            if "yaw" in key:
                y=key["yaw"]
                if type(y) not in (int,float) or not math.isfinite(y) or abs(y)>3600:
                    raise ValueError("invalid animated yaw")
    return scene
def cube():
    v=[(-.5,-.5,-.5),(.5,-.5,-.5),(.5,.5,-.5),(-.5,.5,-.5),
       (-.5,-.5,.5),(.5,-.5,.5),(.5,.5,.5),(-.5,.5,.5)]
    f=[(0,2,1),(0,3,2),(4,5,6),(4,6,7),(0,1,5),(0,5,4),
       (1,2,6),(1,6,5),(2,3,7),(2,7,6),(3,0,4),(3,4,7)]
    return v,f
def sphere(steps=12,rings=8):
    v=[]
    for j in range(rings+1):
        phi=math.pi*j/rings
        for i in range(steps):
            th=2*math.pi*i/steps
            v.append((.5*math.sin(phi)*math.cos(th),
                      .5*math.sin(phi)*math.sin(th),.5*math.cos(phi)))
    f=[]
    for j in range(rings):
        for i in range(steps):
            a=j*steps+i;b=j*steps+(i+1)%steps;c=a+steps;d=b+steps
            f.extend([(a,c,b),(b,c,d)])
    return v,f
def cylinder(steps=12):
    v=[(.5*math.cos(2*math.pi*i/steps),.5*math.sin(2*math.pi*i/steps),z)
       for z in (-.5,.5) for i in range(steps)]
    v.extend([(0,0,-.5),(0,0,.5)])
    f=[]
    for i in range(steps):
        j=(i+1)%steps
        f.extend([(i,j,steps+j),(i,steps+j,steps+i),(2*steps,j,i),(2*steps+1,steps+i,steps+j)])
    return v,f
MESHES={"cube":cube(),"sphere":sphere(),"cylinder":cylinder()}
def pose(obj,frame):
    loc=vec(obj.get("location",[0,0,0]))
    yaw=float(obj.get("yaw",0))
    keys=obj.get("keyframes",[])
    def curve(field,base):
        pts=[(1,base)]
        for k in keys:
            if field in k:pts.append((k["frame"],vec(k[field]) if field=="location" else float(k[field])))
        # explicit 1st frame wins and prevents duplicate vertices
        by_frame={f:x for f,x in pts}
        pts=sorted(by_frame.items())
        for i,(fr,v) in enumerate(pts):
            if frame<=fr:
                if i==0:return v
                f0,p0=pts[i-1]
                k=(frame-f0)/float(fr-f0)
                return mix(p0,v,k) if field=="location" else p0+(v-p0)*k
        return pts[-1][1]
    return curve("location",loc),curve("yaw",yaw)
def render(scene,frame):
    validate(scene)
    w,h=scene.get("width",640),scene.get("height",360)
    camera=scene.get("camera",{})
    pos=vec(camera.get("position",[6,-10,7]))
    target=vec(camera.get("target",[0,0,.6]))
    view=norm(sub(target,pos))
    right=norm(cross(view,(0,0,1)))
    up=norm(cross(right,view))
    zoom=min(w,h)/float(camera.get("ortho_scale",7))
    bg=rgb(scene.get("background","#253543"))
    canvas=Image.new("RGB",(w,h),bg)
    pen=ImageDraw.Draw(canvas)
    pen.rectangle((0,int(.8*h),w,h),fill=tuple(min(255,int(x*1.12)) for x in bg))
    tris=[]
    light=norm((-.5,-.6,1))
    for ob in scene["objects"]:
        vertices,faces=MESHES[ob["shape"]]
        loc,yaw=pose(ob,frame)
        sx,sy,sz=vec(ob.get("scale",[1,1,1]),50)
        ang=math.radians(yaw)
        cc,ss=math.cos(ang),math.sin(ang)
        world=[]
        for x,y,z in vertices:
            xx,yy=x*sx,y*sy
            world.append((xx*cc-yy*ss+loc[0],xx*ss+yy*cc+loc[1],z*sz+loc[2]))
        base=rgb(ob.get("color","#4E896A"))
        for i,j,k in faces:
            a,b,c=world[i],world[j],world[k]
            normal=cross(sub(b,a),sub(c,a))
            if sum(t*t for t in normal)<1e-12:continue
            normal=norm(normal)
            lighting=max(.34,min(1.0,.60+.38*dot(normal,light)))
            col=tuple(max(0,min(255,int(v*lighting))) for v in base)
            pp=[]
            for pt in (a,b,c):
                rel=sub(pt,target)
                pp.append((w/2+dot(rel,right)*zoom,h/2-dot(rel,up)*zoom))
            center=tuple((a[n]+b[n]+c[n])/3 for n in range(3))
            depth=dot(sub(center,pos),view)
            tris.append((depth,pp,col,tuple(dot(sub(pt,pos),view) for pt in (a,b,c))))
    if scene.get("render_mode", "painter") == "zbuffer":
        # Original CPU triangle rasterizer: per-pixel interpolated camera depth
        # fixes overlap errors of centroid-depth painter sorting, no Blender.
        buf=[float("inf")]*(w*h)
        pixels=canvas.load()
        for _, tri, col, depths in tris:
            (x0,y0),(x1,y1),(x2,y2)=tri
            denominator=(y1-y2)*(x0-x2)+(x2-x1)*(y0-y2)
            if abs(denominator)<1e-12:
                continue
            left=max(0,math.floor(min(x0,x1,x2)))
            top=max(0,math.floor(min(y0,y1,y2)))
            right_px=min(w-1,math.ceil(max(x0,x1,x2)))
            bottom_px=min(h-1,math.ceil(max(y0,y1,y2)))
            for yy in range(top,bottom_px+1):
                for xx in range(left,right_px+1):
                    px,py=xx+.5,yy+.5
                    a=((y1-y2)*(px-x2)+(x2-x1)*(py-y2))/denominator
                    b=((y2-y0)*(px-x2)+(x0-x2)*(py-y2))/denominator
                    c=1-a-b
                    if min(a,b,c)<-1e-10:
                        continue
                    depth=a*depths[0]+b*depths[1]+c*depths[2]
                    index=yy*w+xx
                    if depth<buf[index]:
                        buf[index]=depth
                        pixels[xx,yy]=col
    else:
        for _,points,col,_ in sorted(tris,key=lambda q:q[0],reverse=True):
            pen.polygon(points,fill=col)
    return canvas
def export(scene,dest,frame=1):
    validate(scene)
    dest=Path(dest)
    if dest.exists():raise ValueError("refusing to overwrite existing output")
    if not dest.parent.is_dir():raise ValueError("output folder missing")
    if dest.suffix.lower() not in (".png",".mp4"):raise ValueError("PNG/MP4 only")
    frame=integer(frame,1,scene.get("frames",120))
    with tempfile.TemporaryDirectory(prefix="kosif-native3d-") as tmp:
        temp=Path(tmp)/("render"+dest.suffix.lower())
        if dest.suffix.lower()==".png":
            render(scene,frame).save(temp)
        else:
            exe=shutil.which("ffmpeg")
            if not exe:raise ValueError("FFmpeg required for video, not Blender")
            w,h=scene.get("width",640),scene.get("height",360)
            fps,frames=scene.get("fps",24),scene.get("frames",120)
            cmd=[exe,"-hide_banner","-loglevel","error","-y","-f","rawvideo",
                 "-pix_fmt","rgb24","-s",f"{w}x{h}","-r",str(fps),"-i","-",
                 "-frames:v",str(frames),"-c:v","libx264","-preset","veryfast",
                 "-crf","20","-pix_fmt","yuv420p","-movflags","+faststart",str(temp)]
            proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
            try:
                for f in range(1,frames+1):
                    proc.stdin.write(render(scene,f).tobytes())
                proc.stdin.close()
                err=proc.stderr.read()
                code=proc.wait(timeout=90)
                if code!=0:raise ValueError("FFmpeg encode failed: "+err.decode(errors="replace")[-300:])
            finally:
                if proc.poll() is None: proc.kill()
                if proc.stderr: proc.stderr.close()
        if not temp.is_file() or temp.stat().st_size<100:
            raise ValueError("output missing or incomplete")
        dest.write_bytes(temp.read_bytes())
    return {"renderer":"KOSIF native Python","uses_blender":False,"output":str(dest),
            "frames":scene.get("frames",120) if dest.suffix.lower()==".mp4" else 1,
            "bytes":dest.stat().st_size,"sha256":hashlib.sha256(dest.read_bytes()).hexdigest()}
def main():
    a=argparse.ArgumentParser()
    sub=a.add_subparsers(dest="cmd",required=True)
    sub.add_parser("doctor")
    r=sub.add_parser("render")
    r.add_argument("--scene",required=True)
    r.add_argument("--output",required=True)
    r.add_argument("--frame",type=int,default=1)
    args=a.parse_args()
    try:
        if args.cmd=="doctor":
            print(json.dumps({"schema":SCHEMA,"blender_required":False,"pillow":True,
                              "ffmpeg":bool(shutil.which("ffmpeg")),"shapes":sorted(SHAPES),"render_modes":["painter","zbuffer"]}))
        else:
            scene=json.loads(Path(args.scene).read_text(encoding="utf-8-sig"))
            print(json.dumps(export(scene,args.output,args.frame)))
        return 0
    except (ValueError,OSError,subprocess.SubprocessError) as e:
        print(json.dumps({"ok":False,"error":str(e)}),file=sys.stderr)
        return 1
if __name__=="__main__":
    raise SystemExit(main())
