#!/usr/bin/env python3
"""Original KOSIF Creative Paint: declarative layered drawing + keyframe exports.

Independent Pillow implementation, no copied commercial code. Strict JSON only.
"""
import argparse
import hashlib
import html
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageChops

SCHEMA = "kosif.paint.v1"
MAX_DIM, MAX_LAYERS, MAX_SHAPES, MAX_FRAMES = 2048, 150, 1500, 300
KINDS = {"rectangle", "ellipse", "line", "polygon", "brush", "text"}
HEX = re.compile(r"^#[0-9a-fA-F]{6}(?:[0-9a-fA-F]{2})?$")

def num(value, low=-100000, high=100000):
    if isinstance(value, bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or not low <= value <= high:
        raise ValueError(f"Expected finite numeric value in [{low},{high}]")
    return float(value)

def color(value):
    if not isinstance(value,str) or not HEX.fullmatch(value):
        raise ValueError("Color must be #RRGGBB or #RRGGBBAA")
    return value

def pts(points):
    if not isinstance(points,list) or not 2 <= len(points) <= 1500:
        raise ValueError("Expected 2..1500 points")
    for p in points:
        if not isinstance(p,list) or len(p) not in (2,3): raise ValueError("Points must be [x,y,pressure?]")
        for n,v in enumerate(p): num(v,0,100000) if n<2 else num(v,0.1,5)
    return points

def validate(s):
    if not isinstance(s,dict) or s.get("schema")!=SCHEMA: raise ValueError("Invalid schema")
    w,h=s.get("width"),s.get("height")
    num(w,1,MAX_DIM);num(h,1,MAX_DIM)
    if not isinstance(w,int) or not isinstance(h,int): raise ValueError("Integer dimensions required")
    bg=s.get("background","#FFFFFF")
    if bg!="transparent":color(bg)
    ls=s.get("layers")
    if not isinstance(ls,list) or not 1<=len(ls)<=MAX_LAYERS: raise ValueError("1..150 layers required")
    total=0
    for layer in ls:
        if not isinstance(layer,dict) or not isinstance(layer.get("name"),str) or len(layer["name"])>100:
            raise ValueError("Layer needs a name")
        num(layer.get("opacity",1),0,1)
        if layer.get("blend","normal") not in ("normal","multiply","screen"):raise ValueError("Invalid blend")
        if not isinstance(layer.get("visible",True),bool):raise ValueError("Invalid visible")
        keys=layer.get("keyframes",[])
        if not isinstance(keys,list) or len(keys)>100:raise ValueError("Too many keyframes")
        last=-1
        for key in keys:
            if not isinstance(key,dict):raise ValueError("Invalid keyframe")
            time=num(key.get("time"),0,3600)
            if time<=last:raise ValueError("Keyframes not increasing")
            last=time
            for v in ("x","y","angle"):num(key.get(v,0),-360 if v=="angle" else -100000,360 if v=="angle" else 100000)
            num(key.get("opacity",1),0,1);num(key.get("scale",1),0.01,20)
            if key.get("ease","linear") not in ("linear","ease-in-out"):raise ValueError("Invalid ease")
        shapes=layer.get("shapes")
        if not isinstance(shapes,list):raise ValueError("Expected shapes array")
        total+=len(shapes)
        for shape in shapes:
            if not isinstance(shape,dict) or shape.get("kind") not in KINDS:raise ValueError("Unsupported shape")
            for v in ("fill","stroke"):
                if v in shape:color(shape[v])
            num(shape.get("stroke_width",2),0,200)
            if shape["kind"] in ("rectangle","ellipse"):
                num(shape["x"]);num(shape["y"]);num(shape["width"],0,MAX_DIM);num(shape["height"],0,MAX_DIM)
            if shape["kind"] in ("line","polygon","brush"):
                pp=pts(shape["points"])
                if shape["kind"]=="polygon" and len(pp)<3:raise ValueError("Polygon needs 3+ points")
            if shape["kind"]=="text":
                num(shape["x"]);num(shape["y"]);num(shape.get("size",36),6,300)
                if not isinstance(shape.get("text"),str) or len(shape["text"])>250:raise ValueError("Invalid text")
                if "font" in shape and (not isinstance(shape["font"],str) or len(shape["font"])>512):raise ValueError("Invalid font")
    if total>MAX_SHAPES:raise ValueError("Too many shapes")
    return w,h,bg

def rgba(v):
    if v is None:return None
    z=tuple(bytes.fromhex(v[1:]))
    return z+(255,) if len(z)==3 else z

def pose(layer,t):
    init={"x":0.0,"y":0.0,"angle":0.0,"scale":1.0,"opacity":1.0}
    keys=layer.get("keyframes",[])
    if not keys:return init
    if t<=keys[0]["time"]:return {k:float(keys[0].get(k,v)) for k,v in init.items()}
    if t>=keys[-1]["time"]:return {k:float(keys[-1].get(k,v)) for k,v in init.items()}
    for a,b in zip(keys,keys[1:]):
        if a["time"]<=t<=b["time"]:
            u=(t-a["time"])/(b["time"]-a["time"])
            if b.get("ease","linear")=="ease-in-out":u=u*u*(3-2*u)
            return {k:float(a.get(k,v))*(1-u)+float(b.get(k,v))*u for k,v in init.items()}
    return init

def paint_shape(draw,s):
    k=s["kind"]; fill=rgba(s.get("fill","#192F36")); stroke=rgba(s.get("stroke","#1B2527"))
    width=round(s.get("stroke_width",2))
    if k in ("rectangle","ellipse"):
        box=[round(s["x"]),round(s["y"]),round(s["x"]+s["width"]),round(s["y"]+s["height"])]
        f=draw.rectangle if k=="rectangle" else draw.ellipse
        f(box,fill=fill,outline=stroke if width>0 else None,width=width)
    elif k=="text":
        try:
            font=ImageFont.truetype(s["font"],int(s.get("size",36))) if "font" in s else ImageFont.load_default(size=int(s.get("size",36)))
        except OSError as exc:raise ValueError("Font unavailable") from exc
        draw.text((s["x"],s["y"]),s["text"],font=font,fill=fill)
    else:
        points=pts(s["points"])
        plain=[(round(p[0]),round(p[1])) for p in points]
        if k=="polygon":
            draw.polygon(plain,fill=fill)
            if width:draw.line(plain+[plain[0]],fill=stroke,width=width,joint="curve")
        if k=="line":draw.line(plain,fill=stroke,width=max(1,width),joint="curve")
        if k=="brush":
            for a,b in zip(points,points[1:]):
                steps=max(1,round(math.hypot(b[0]-a[0],b[1]-a[1])*1.5))
                for i in range(steps+1):
                    u=i/steps;x=a[0]*(1-u)+b[0]*u;y=a[1]*(1-u)+b[1]*u
                    press=(a[2] if len(a)==3 else 1)*(1-u)+(b[2] if len(b)==3 else 1)*u
                    radius=max(.5,width*press/2)
                    draw.ellipse((round(x-radius),round(y-radius),round(x+radius),round(y+radius)),fill=stroke)

def paint(scene,t=0):
    w,h,bg=validate(scene)
    canvas=Image.new("RGBA",(w,h),(0,0,0,0) if bg=="transparent" else rgba(bg))
    for layer in scene["layers"]:
        if not layer.get("visible",True):continue
        temp=Image.new("RGBA",(w,h),(0,0,0,0));draw=ImageDraw.Draw(temp)
        for s in layer["shapes"]:paint_shape(draw,s)
        p=pose(layer,t)
        if p["scale"]!=1:
            temp=temp.resize((max(1,round(w*p["scale"])),max(1,round(h*p["scale"]))),Image.Resampling.BICUBIC)
        left,top=p["x"],p["y"]
        if p["angle"]:
            # Turn clockwise about the centre of the (scaled) layer box, as svg() does;
            # expand=True grows the image around that centre, so shift it back by half the growth.
            before=temp.size
            temp=temp.rotate(-p["angle"],resample=Image.Resampling.BICUBIC,expand=True)
            left-=(temp.width-before[0])/2;top-=(temp.height-before[1])/2
        placed=Image.new("RGBA",(w,h),(0,0,0,0))
        placed.paste(temp,(round(left),round(top)))
        alpha=placed.getchannel("A").point(lambda a:round(a*layer.get("opacity",1)*p["opacity"]))
        placed.putalpha(alpha)
        blend=layer.get("blend","normal")
        if blend=="normal":canvas=Image.alpha_composite(canvas,placed)
        else:
            rgb=ImageChops.multiply(canvas.convert("RGB"),placed.convert("RGB")) if blend=="multiply" else ImageChops.screen(canvas.convert("RGB"),placed.convert("RGB"))
            composite=Image.merge("RGBA",(*rgb.split(),placed.getchannel("A")))
            canvas=Image.alpha_composite(canvas,composite)
    return canvas

def svg(scene,t=0):
    w,h,bg=validate(scene)
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    if bg!="transparent":parts.append(f'<rect width="{w}" height="{h}" fill="{bg}"/>')
    for layer in scene["layers"]:
        if not layer.get("visible",True):continue
        p=pose(layer,t)
        parts.append(f'<g data-layer="{html.escape(layer["name"],quote=True)}" opacity="{layer.get("opacity",1)*p["opacity"]:.4f}" transform="translate({p["x"]:.4f} {p["y"]:.4f}) rotate({p["angle"]:.4f} {w*p["scale"]/2:.4f} {h*p["scale"]/2:.4f}) scale({p["scale"]:.4f})">')
        for s in layer["shapes"]:
            k=s["kind"];fill=s.get("fill","#192F36");stroke=s.get("stroke","#1B2527");sw=s.get("stroke_width",2)
            if k=="rectangle":parts.append(f'<rect x="{s["x"]}" y="{s["y"]}" width="{s["width"]}" height="{s["height"]}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
            elif k=="ellipse":parts.append(f'<ellipse cx="{s["x"]+s["width"]/2}" cy="{s["y"]+s["height"]/2}" rx="{s["width"]/2}" ry="{s["height"]/2}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
            elif k=="text":parts.append(f'<text x="{s["x"]}" y="{s["y"]+s.get("size",36)}" fill="{fill}" font-size="{s.get("size",36)}">{html.escape(s["text"])}</text>')
            else:
                pts_str=" ".join(f'{p[0]},{p[1]}' for p in s["points"])
                tag="polygon" if k=="polygon" else "polyline"
                parts.append(f'<{tag} points="{pts_str}" fill="{fill if k=="polygon" else "none"}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')
        parts.append('</g>')
    parts.append('</svg>')
    return "\n".join(parts)

def hash_file(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def render(scene,output,t=0):
    out=Path(output)
    if out.exists():raise ValueError("Refusing to overwrite existing output")
    if out.suffix.lower()==".svg":out.write_text(svg(scene,t),encoding="utf-8")
    elif out.suffix.lower()==".png":paint(scene,t).save(out)
    else:raise ValueError("Use .png or .svg")
    return {"output":str(out),"sha256":hash_file(out),"bytes":out.stat().st_size,"verified":True}

def animate(scene,output,fps=24,duration=2):
    fps=int(num(fps,1,60));duration=num(duration,.01,30);frames=math.ceil(duration*fps)
    if frames>MAX_FRAMES:raise ValueError("300 frame safety limit")
    out=Path(output)
    if out.exists():raise ValueError("Refusing to overwrite existing output")
    if out.suffix.lower()==".gif":
        images=[paint(scene,i/fps).convert("RGB") for i in range(frames)]
        images[0].save(out,save_all=True,append_images=images[1:],duration=round(1000/fps),loop=0,optimize=False)
    elif out.suffix.lower()==".mp4":
        if not shutil.which("ffmpeg"):raise ValueError("FFmpeg unavailable")
        with tempfile.TemporaryDirectory(prefix="kosif-paint-") as td:
            for i in range(frames):
                im=paint(scene,i/fps)
                backdrop=Image.new("RGBA",im.size,"white");backdrop.alpha_composite(im)
                backdrop.convert("RGB").save(Path(td)/f'{i:05d}.png')
            cmd=["ffmpeg","-hide_banner","-loglevel","error","-y","-framerate",str(fps),"-i",str(Path(td)/"%05d.png"),"-frames:v",str(frames),"-c:v","libx264","-pix_fmt","yuv420p","-preset","slow","-crf","17","-movflags","+faststart",str(out)]
            subprocess.run(cmd,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    else:raise ValueError("Use .gif or .mp4")
    return {"output":str(out),"sha256":hash_file(out),"fps":fps,"frames":frames,"verified":out.stat().st_size>100}

def main(argv=None):
    parser=argparse.ArgumentParser(description="KOSIF Creative Paint: PNG/SVG editable layers + GIF/MP4 keyframes")
    sub=parser.add_subparsers(dest="command",required=True)
    sub.add_parser("doctor")
    for command in ("render","animate"):
        p=sub.add_parser(command);p.add_argument("--scene",required=True);p.add_argument("--output",required=True)
        if command=="render":p.add_argument("--time",type=float,default=0)
        else:p.add_argument("--fps",type=int,default=24);p.add_argument("--duration",type=float,default=2)
    a=parser.parse_args(argv)
    if a.command=="doctor":
        print(json.dumps({"schema":SCHEMA,"pillow":Image.__version__,"ffmpeg":bool(shutil.which("ffmpeg")),"max_frames":MAX_FRAMES,"formats":["png","svg","gif","mp4"]}));return 0
    try:
        scene=json.loads(Path(a.scene).read_text(encoding="utf-8-sig"))
        validate(scene)
        result=render(scene,a.output,num(a.time,0,3600)) if a.command=="render" else animate(scene,a.output,a.fps,a.duration)
        print(json.dumps(result));return 0
    except (ValueError,OSError,KeyError,subprocess.CalledProcessError) as exc:
        print(json.dumps({"verified":False,"error":str(exc)},ensure_ascii=False),file=sys.stderr);return 1

if __name__=="__main__":raise SystemExit(main())
