#!/usr/bin/env python3
"""KOSIF Motion Director: compile a validated audio-timed script to original SVG animation.

Builds a self-contained HTML animation (with window.__kosif.seek(t)) using only
the Python standard library. Optional MP4 uses the EXISTING kosif-tool render
pipeline, only when present. It never downloads dependencies or audio.
"""
import argparse
import html
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

SKILL = Path(__file__).resolve().parent.parent
ENGINE = SKILL / "assets" / "motion_engine.js"
RENDERER = SKILL.parents[2] / "tools" / "render_html.cjs"
if not RENDERER.is_file():
    RENDERER = SKILL / "resources" / "motion-runtime" / "render_html.cjs"
HEX = re.compile(r"^#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?$")
PATH_DATA = re.compile(r"^[\d\s+\-.,EeMmLlHhVvCcQqSsTtAaZz]+$")
MAX_ELEMENTS = 80
MAX_DURATION = 120.0


def number(value, minimum=None, maximum=None):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("expected numeric property")
    x = float(value)
    import math
    if not math.isfinite(x) or (minimum is not None and x < minimum) or (maximum is not None and x > maximum):
        raise ValueError("numeric property out of range")
    return x


def color(value):
    if not isinstance(value, str) or not HEX.fullmatch(value):
        raise ValueError("color must be an RGB/RRGGBB hex literal")
    return value


def text(value, max_len=160):
    if not isinstance(value, str) or not value or len(value) > max_len or any(ord(c)<32 for c in value):
        raise ValueError("invalid visible text")
    return value


def validate(spec):
    if not isinstance(spec, dict) or spec.get("version") != 1:
        raise ValueError("unsupported spec version")
    width = spec.get("width")
    height = spec.get("height")
    fps = spec.get("fps")
    duration = spec.get("duration")
    if type(width) is not int or type(height) is not int or width<320 or height<320 or width>4096 or height>4096 or width%2 or height%2:
        raise ValueError("width/height must be even integers within 320..4096")
    if type(fps) is not int or fps not in (24, 25, 30, 60):
        raise ValueError("fps must be 24,25,30 or 60")
    duration = number(duration,0.1,MAX_DURATION)
    scenes=spec.get("scenes")
    if not isinstance(scenes,list) or not scenes or len(scenes)>30:
        raise ValueError("1..30 scenes required")
    previous=0.0
    count=0
    ids=set()
    for sc in scenes:
        if not isinstance(sc,dict) or not isinstance(sc.get("id"),str) or not re.fullmatch(r"[a-zA-Z0-9_-]{1,32}",sc["id"]) or sc["id"] in ids:
            raise ValueError("unique alphanumeric scene id required")
        ids.add(sc["id"])
        start=number(sc.get("start"),0,duration)
        end=number(sc.get("end"),0,duration)
        if abs(start-previous)>1e-6 or end<=start:
            raise ValueError("scenes must form a continuous, ordered timeline")
        previous=end
        color(sc.get("background","#f4f0e6"))
        words=sc.get("words",[])
        if not isinstance(words,list) or len(words)>240:
            raise ValueError("invalid word list")
        last_word=start
        for w in words:
            if not isinstance(w,dict):
                raise ValueError("invalid word")
            text(w.get("text"),120)
            a=number(w.get("start"),start,end)
            b=number(w.get("end"),start,end)
            if a<last_word-1e-6 or b<=a:
                raise ValueError("word timings must be monotonic, non-overlapping and within scene")
            last_word=b
        camera=sc.get("camera",{})
        if not isinstance(camera,dict):
            raise ValueError("invalid camera")
        for k,v in camera.items():
            if k not in {"start","end","fromZoom","toZoom","fromX","toX","fromY","toY"}:
                raise ValueError("unknown camera property")
            number(v,0.3,3.0) if k.endswith("Zoom") else number(v,-4096,4096)
        elements=sc.get("elements",[])
        if not isinstance(elements,list):
            raise ValueError("elements must be a list")
        count+=len(elements)
        if count>MAX_ELEMENTS:
            raise ValueError("too many elements")
        for item in elements:
            if not isinstance(item,dict) or item.get("type") not in {"path","circle","text","character","actor"}:
                raise ValueError("unsupported vector element type")
            a=number(item.get("start",start),start,end)
            b=number(item.get("end",end),start,end)
            if b<a:
                raise ValueError("element ends before it starts")
            if "stroke" in item:
                color(item["stroke"])
            if "fill" in item and item["fill"]!="none":
                color(item["fill"])
            if "strokeWidth" in item:
                number(item["strokeWidth"],0.1,50)
            if item["type"]=="path":
                d=item.get("d")
                if not isinstance(d,str) or len(d)>2500 or not PATH_DATA.fullmatch(d):
                    raise ValueError("unsafe SVG path")
            elif item["type"]=="circle":
                for k in ("x","y","r"):
                    number(item.get(k),0 if k=="r" else -4096,4096)
            elif item["type"]=="character":
                for k in ("x","y"):
                    number(item.get(k),-4096,4096)
                if "scale" in item:
                    number(item["scale"],0.1,4)
            elif item["type"]=="actor":
                for k in ("x","y"):
                    number(item.get(k),-4096,4096)
                if "scale" in item:
                    number(item["scale"],0.1,4)
                if item.get("action","idle") not in {"idle","walk","run","wave","point","sit"}:
                    raise ValueError("unsupported actor action")
                parts=item.get("parts")
                if not isinstance(parts,list) or not 3<=len(parts)<=64:
                    raise ValueError("actor requires 3..64 vector parts")
                for part in parts:
                    if not isinstance(part,dict):
                        raise ValueError("invalid actor part")
                    role=part.get("role","detail")
                    if role not in {"head","body","hair","eye","nose","mouth","jacket",
                                    "shirt","arm-left","arm-right","leg-left","leg-right",
                                    "hand-left","hand-right","shoe-left","shoe-right",
                                    "ear","tail","whisker","detail"}:
                        raise ValueError("unsupported actor part role")
                    d=part.get("d")
                    if not isinstance(d,str) or len(d)>2500 or not PATH_DATA.fullmatch(d):
                        raise ValueError("unsafe actor SVG path")
                    if "stroke" in part:
                        color(part["stroke"])
                    if "fill" in part and part["fill"]!="none":
                        color(part["fill"])
                    if "strokeWidth" in part:
                        number(part["strokeWidth"],0.1,40)
                    pivot=part.get("pivot",[0,0])
                    if not isinstance(pivot,list) or len(pivot)!=2:
                        raise ValueError("actor joint pivot must be a 2-point list")
                    for v in pivot:
                        number(v,-4096,4096)
            else:
                text(item.get("text"))
                for k in ("x","y"):
                    number(item.get(k),-4096,4096)
                if "fontSize" in item:
                    number(item["fontSize"],10,250)
                if item.get("direction","rtl") not in ("rtl","ltr"):
                    raise ValueError("invalid text direction")
                if item.get("anchor","middle") not in ("middle","start","end"):
                    raise ValueError("invalid text anchor")
            move=item.get("move",{})
            if not isinstance(move,dict) or any(k not in {"fromX","toX","fromY","toY","start","end"} for k in move):
                raise ValueError("unsafe motion fields")
            for k,v in move.items():
                number(v,-4096,4096)
    if abs(previous-duration)>1e-6:
        raise ValueError("scenes must cover the full duration")
    return {"scenes":len(scenes),"elements":count,"duration":duration,
            "frames":round(duration*fps),"format":f"{width}x{height}"}


def sample():
    return {"version":1,"width":1080,"height":1920,"fps":30,"duration":9,
            "scenes":[
                {"id":"intro","start":0,"end":3,"background":"#f4f0e6",
                 "camera":{"fromZoom":1,"toZoom":1.06,"start":0,"end":3},
                 "words":[{"text":"كل","start":0.1,"end":0.8},{"text":"فكرة","start":0.8,"end":1.8},{"text":"تبدأ بخط","start":1.8,"end":2.9}],
                 "elements":[
                     {"type":"text","x":540,"y":340,"text":"كل فكرة تبدأ بخط","fontSize":64,"start":0,"end":1.0},
                     {"type":"path","d":"M170 690 C320 510 600 940 920 660","start":0.3,"end":2.4,"strokeWidth":9},
                     {"type":"circle","x":540,"y":1110,"r":115,"start":1,"end":2.5,"stroke":"#355b47"}]},
                {"id":"character","start":3,"end":6,"background":"#f4f0e6",
                 "camera":{"fromX":-10,"toX":20,"fromZoom":1,"toZoom":1.07},
                 "words":[{"text":"ثم","start":3.1,"end":4},{"text":"تتحرك","start":4,"end":4.9},{"text":"وتعيش","start":4.9,"end":5.9}],
                 "elements":[
                     {"type":"text","x":540,"y":330,"text":"الرسم يتحرك","fontSize":70,"start":3,"end":4},
                     {"type":"character","x":510,"y":990,"scale":1.7,"start":3.2,"end":4.8,
                      "move":{"fromX":-110,"toX":120,"fromY":0,"toY":0,"start":4.8,"end":6}}]},
                {"id":"outro","start":6,"end":9,"background":"#f4f0e6",
                 "words":[{"text":"هذا","start":6.1,"end":7},{"text":"موشن","start":7,"end":8},{"text":"بالكود","start":8,"end":8.9}],
                 "elements":[
                     {"type":"text","x":540,"y":510,"text":"KOSIF MOTION","direction":"ltr",
                      "fontSize":72,"start":6,"end":7.4,"fill":"#355b47"},
                     {"type":"path","d":"M180 720 L900 720 M180 760 L690 760",
                      "stroke":"#172824","start":6.4,"end":8.8,"strokeWidth":10}]}
            ]}


def compile_spec(spec,out):
    stats=validate(spec)
    if not ENGINE.is_file():
        raise ValueError("engine asset is missing from the skill")
    js=ENGINE.read_text(encoding="utf-8")
    data=json.dumps(spec,ensure_ascii=False,separators=(",",":"))
    # Harden script-tag boundary against user text like '</script>'.
    safe=data.replace("<","\\u003c").replace(">","\\u003e").replace("&","\\u0026")
    template=("<!doctype html>\n<html lang='ar' dir='rtl'><head><meta charset='utf-8'>"
              "<meta name='viewport' content='width=device-width,initial-scale=1'>"
              "<title>KOSIF Motion</title><style>html,body{margin:0;width:100%;height:100%;"
              "overflow:hidden;background:#f4f0e6}svg{display:block;width:100%;height:100%}"
              "text{font-family:Arial,'Noto Sans Arabic',sans-serif}</style></head><body>"
              f"<svg id='scene' xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {spec['width']} {spec['height']}'>"
              f"<rect id='background' width='{spec['width']}' height='{spec['height']}'/>"
              "<g id='stage'><g id='art'></g></g><g id='captions'></g></svg>"
              f"<script type='application/json' id='kosif-data'>{safe}</script>"
              f"<script>{js}</script></body></html>\n")
    p=Path(out).expanduser()
    if p.exists() or not p.parent.is_dir() or p.is_symlink():
        raise ValueError("output must be a new path in an existing directory")
    with p.open("x",encoding="utf-8") as f:
        f.write(template)
    return {**stats,"html":str(p.resolve()),"bytes":len(template.encode("utf-8")),
            "status":"html_compiled_not_rendered","engine":"KOSIF original SVG motion"}


def doctor():
    return {"engine_available":ENGINE.is_file(),
            "renderer_available":RENDERER.is_file(),
            "node_available":bool(shutil.which("node")),
            "ffmpeg_available":bool(shutil.which("ffmpeg")),
            "ffprobe_available":bool(shutil.which("ffprobe")),
            "status":"environment_probe_only","video_rendered":False}


def render(html_path,output,audio=None):
    src=Path(html_path).expanduser()
    dest=Path(output).expanduser()
    if not src.is_file() or dest.suffix.lower()!=".mp4" or dest.exists() or not dest.parent.is_dir():
        raise ValueError("existing HTML and fresh output .mp4 path required")
    if not (RENDERER.is_file() and shutil.which("node") and shutil.which("ffmpeg") and shutil.which("ffprobe")):
        raise ValueError("KOSIF bundled render_html.cjs + node + Playwright/Chromium + ffmpeg/ffprobe required")
    cmd=["node",str(RENDERER),"--in",str(src.resolve()),"--out",str(dest.resolve()),
         "--mode","seek","--offline"]
    if audio:
        source=Path(audio).expanduser()
        if not source.is_file():
            raise ValueError("audio file does not exist")
        cmd+=["--audio",str(source.resolve())]
    result=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,
                          stdin=subprocess.DEVNULL,check=False,timeout=1200)
    return {"status":"render_command_completed" if result.returncode==0 else "render_failed",
            "return_code":result.returncode,"mp4_exists":dest.is_file(),
            "verified":False,"next":"Independently inspect video with scripts/verify_video.py in the skill",
            "stderr_tail":result.stderr[-1500:] if result.returncode else ""}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    sub=ap.add_subparsers(dest="command",required=True)
    sub.add_parser("doctor")
    demo=sub.add_parser("sample")
    demo.add_argument("--out",required=True)
    comp=sub.add_parser("compile")
    comp.add_argument("spec")
    comp.add_argument("--out",required=True)
    rend=sub.add_parser("render")
    rend.add_argument("html")
    rend.add_argument("--out",required=True)
    rend.add_argument("--audio")
    args=ap.parse_args()
    try:
        if args.command=="doctor":
            result=doctor()
        elif args.command=="sample":
            spec=sample()
            dest=Path(args.out)
            if dest.exists() or not dest.parent.is_dir():
                raise ValueError("sample output must not exist")
            dest.write_text(json.dumps(spec,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
            result={"status":"sample_created","path":str(dest.resolve()),**validate(spec)}
        elif args.command=="compile":
            result=compile_spec(json.loads(Path(args.spec).read_text(encoding="utf-8")),args.out)
        else:
            result=render(args.html,args.out,args.audio)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 1 if result["status"]=="render_failed" else 0
    except (OSError,ValueError,json.JSONDecodeError,subprocess.TimeoutExpired) as exc:
        print(json.dumps({"status":"failed","error":str(exc)},ensure_ascii=False),file=sys.stderr)
        return 2


if __name__=="__main__":
    sys.exit(main())
