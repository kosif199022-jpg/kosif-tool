#!/usr/bin/env python3
"""Original KOSIF Smart Draw: bounded freehand and deterministic shape assist.
Informed by publicly described workflows, no AutoDraw/Canva code or art.
Not an ML drawing model or a product clone.
"""
import argparse
import json
import math
from pathlib import Path
from creative_paint import paint, svg, color, num

SCHEMA = "kosif.smartdraw.v1"

def distance(a,b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

def simplify(points, tolerance):
    """Ramer-Douglas-Peucker simplification of [x,y,pressure?]."""
    if len(points)<3:
        return points[:]
    a,b=points[0],points[-1]
    line=distance(a,b)
    def error(p):
        if line<1e-9: return distance(a,p)
        return abs((b[0]-a[0])*(a[1]-p[1])-(a[0]-p[0])*(b[1]-a[1]))/line
    split=max(range(1,len(points)-1),key=lambda i:error(points[i]))
    if error(points[split])<=tolerance: return [a,b]
    return simplify(points[:split+1],tolerance)[:-1]+simplify(points[split:],tolerance)

def classify(points):
    if len(points)<2: raise ValueError("two or more points required")
    xs=[p[0] for p in points]; ys=[p[1] for p in points]
    w=max(xs)-min(xs); h=max(ys)-min(ys)
    dia=math.hypot(w,h)
    if dia<4: return "freehand"
    closed=distance(points[0],points[-1])<0.14*dia
    if closed and min(w,h)>5 and len(points)>=4:
        # Use segment direction, not only near-corner distances, so rectangles
        # with 5 nodes can be recognized without a neural classifier.
        segs=[(b[0]-a[0],b[1]-a[1]) for a,b in zip(points,points[1:])]
        axis=sum(1 for dx,dy in segs if min(abs(dx),abs(dy))<=.12*math.hypot(dx,dy)+1)
        horizontal=sum(1 for dx,dy in segs if abs(dx)>abs(dy)*3)
        vertical=sum(1 for dx,dy in segs if abs(dy)>abs(dx)*3)
        if axis/len(segs)>=.78 and horizontal>=2 and vertical>=2:
            return "rectangle"
        if len(points)>=8:
            cx=sum(xs)/len(xs); cy=sum(ys)/len(ys)
            radii=[math.hypot(p[0]-cx,p[1]-cy) for p in points]
            avg=sum(radii)/len(radii)
            variation=(sum((v-avg)**2 for v in radii)/len(radii))**.5
            if avg>0 and variation/avg<.16 and .65<w/h<1.6:
                return "ellipse"
    end=distance(points[0],points[-1])
    if end>.65*dia:
        dx,dy=points[-1][0]-points[0][0],points[-1][1]-points[0][1]
        errors=[abs(dx*(points[0][1]-p[1])-(points[0][0]-p[0])*dy)/end for p in points]
        if max(errors)<.065*dia:
            return "line"
    return "freehand"

def to_scene(doc):
    if not isinstance(doc,dict) or doc.get("schema")!=SCHEMA:
        raise ValueError("expected kosif.smartdraw.v1")
    w,h=doc.get("width"),doc.get("height")
    if type(w) is not int or type(h) is not int or not 128<=w<=2048 or not 128<=h<=2048:
        raise ValueError("unsupported dimensions")
    background=doc.get("background","#F4F0E6")
    if background!="transparent": color(background)
    strokes=doc.get("strokes")
    if not isinstance(strokes,list) or not 1<=len(strokes)<=100:
        raise ValueError("expected 1..100 strokes")
    layers=[]
    labels=[]
    for i,stroke in enumerate(strokes):
        if not isinstance(stroke,dict): raise ValueError("stroke must be object")
        pts=stroke.get("points")
        if not isinstance(pts,list) or not 2<=len(pts)<=1500:
            raise ValueError("invalid stroke point count")
        for point in pts:
            if not isinstance(point,list) or len(point) not in (2,3):
                raise ValueError("invalid stroke point")
            num(point[0],0,w); num(point[1],0,h)
            if len(point)==3:num(point[2],.1,5)
        ink=color(stroke.get("color","#253F35"))
        width=num(stroke.get("width",6),1,80)
        brush=stroke.get("brush","pen")
        if brush not in ("pen","marker","highlighter"):
            raise ValueError("unsupported brush type")
        opacity={"pen":1,"marker":.9,"highlighter":.32}[brush]
        assist=stroke.get("assist",False)
        if type(assist) is not bool:raise ValueError("assist must be boolean")
        label=classify(pts) if assist else "freehand"
        xs=[p[0] for p in pts];ys=[p[1] for p in pts]
        if label=="rectangle":
            shape={"kind":"rectangle","x":min(xs),"y":min(ys),
                   "width":max(xs)-min(xs),"height":max(ys)-min(ys),
                   "fill":"#00000000","stroke":ink,"stroke_width":width}
        elif label=="ellipse":
            shape={"kind":"ellipse","x":min(xs),"y":min(ys),
                   "width":max(xs)-min(xs),"height":max(ys)-min(ys),
                   "fill":"#00000000","stroke":ink,"stroke_width":width}
        elif label=="line":
            shape={"kind":"line","points":[pts[0][:2],pts[-1][:2]],"stroke":ink,"stroke_width":width}
        else:
            shapes=simplify(pts, 1.2)
            shape={"kind":"brush","points":shapes,"stroke":ink,"stroke_width":width}
        layers.append({"name":f"Stroke {i+1}: {label}", "visible":True,
                       "opacity":opacity,"shapes":[shape]})
        labels.append({"stroke":i+1,"recognized":label,"brush":brush})
    scene={"schema":"kosif.paint.v1","width":w,"height":h,
           "background":background,"layers":layers}
    return scene,labels

def main():
    p=argparse.ArgumentParser(description="KOSIF original freehand shape assist")
    sub=p.add_subparsers(dest="command",required=True)
    sub.add_parser("doctor")
    for cmd in ("analyze","render"):
        q=sub.add_parser(cmd);q.add_argument("--scene",required=True)
        if cmd=="render":q.add_argument("--output",required=True)
    args=p.parse_args()
    try:
        if args.command=="doctor":
            result={"engine":"original deterministic KOSIF Shape Assist",
                    "classification":["rectangle","ellipse","line","freehand"],
                    "brushes":["pen","marker","highlighter"],
                    "formats":["png","svg"],"is_ml":False}
        else:
            data=json.loads(Path(args.scene).read_text(encoding="utf-8-sig"))
            scene,labels=to_scene(data)
            result={"recognized":labels,"layers":len(scene["layers"])}
            if args.command=="render":
                dest=Path(args.output)
                if dest.exists():raise ValueError("refusing to overwrite")
                if dest.suffix.lower()==".svg":dest.write_text(svg(scene),encoding="utf-8")
                elif dest.suffix.lower()==".png":paint(scene).save(dest)
                else: raise ValueError("supported outputs: PNG, SVG")
                result["output"]=str(dest)
                result["bytes"]=dest.stat().st_size
        print(json.dumps(result,ensure_ascii=False))
        return 0
    except (ValueError,OSError,KeyError) as err:
        print(json.dumps({"error":str(err)},ensure_ascii=False))
        return 1
if __name__=="__main__":
    raise SystemExit(main())
