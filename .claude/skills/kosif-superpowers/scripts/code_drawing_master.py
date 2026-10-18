#!/usr/bin/env python3
"""KOSIF Code Drawing Master — original procedural vector storytelling.

Build real human/cat SVG body-part rigs and street/park locations, ordered
hand-drawn outlines and post-draw movement as validated Motion Director JSON.
Python standard library only. No user-supplied code, assets, URLs or imports.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
_spec=importlib.util.spec_from_file_location("kosif_motion_director",HERE/"motion_director.py")
director=importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(director)

INK="#172824"
GREEN="#355b47"
CREAM="#f4f0e6"
SKIN="#e6bf96"
WHITE="#fff9eb"
CLOTH="#445d4e"
PANTS="#394443"


def part(role, d, fill="none", stroke=INK, width=4, pivot=None):
    result={"role":role,"d":d,"fill":fill,"stroke":stroke,"strokeWidth":width}
    if pivot is not None:
        result["pivot"]=list(pivot)
    return result


def human_parts(expression="happy"):
    if expression not in {"happy","sad","determined"}:
        raise ValueError("unsupported human expression")
    mouth={"happy":"M-13 -120 Q0 -108 14 -122",
           "sad":"M-14 -111 Q0 -128 15 -111",
           "determined":"M-12 -116 L13 -116"}[expression]
    return [
        part("head","M-41 -193 C-55 -185 -58 -167 -54 -145 C-53 -112 -33 -92 -7 -91 C26 -86 50 -107 51 -143 C54 -173 40 -196 10 -204 C-10 -209 -30 -203 -41 -193 Z",SKIN),
        part("eye","M-25 -151 Q-17 -158 -9 -152 M11 -151 Q19 -158 27 -151",stroke=INK,width=5),
        part("nose","M1 -148 Q-6 -136 2 -132 L8 -132",width=3),
        part("mouth",mouth,width=4),
        part("hair","M-55 -168 Q-63 -211 -29 -225 Q5 -242 39 -211 Q59 -197 54 -163 Q33 -189 13 -188 Q-8 -190 -20 -174 Q-33 -167 -55 -168 Z",INK,width=3),
        part("detail","M-55 -148 Q-73 -145 -61 -131 M51 -148 Q68 -140 57 -131",width=3),
        part("body","M-13 -95 L-14 -74 L13 -74 L13 -95",SKIN),
        part("shirt","M-28 -65 Q0 -50 28 -65 L23 91 L-23 91 Z",WHITE),
        part("jacket","M-36 -70 L-66 -51 L-52 78 L-22 100 L-8 -65 Z",CLOTH),
        part("jacket","M36 -70 L66 -51 L52 78 L22 100 L8 -65 Z",CLOTH),
        part("detail","M-8 -64 L0 86 L8 -64 M-43 -2 L-22 5 M22 5 L43 -2",width=3),
        part("arm-left","M-59 -52 Q-80 -40 -87 0 L-76 48 L-57 48 L-64 -1 L-37 -35 Z",CLOTH,pivot=(-55,-52)),
        part("arm-right","M59 -52 Q83 -42 88 0 L80 55 L58 55 L64 0 L37 -35 Z",CLOTH,pivot=(55,-52)),
        part("hand-left","M-76 46 Q-86 61 -71 75 L-57 59 L-57 46 Z",SKIN,pivot=(-55,-52)),
        part("hand-right","M58 53 Q57 74 76 77 Q90 65 80 53 Z",SKIN,pivot=(55,-52)),
        part("leg-left","M-24 90 L-42 214 L-9 216 L0 99 Z",PANTS,pivot=(-18,93)),
        part("leg-right","M0 99 L8 216 L42 214 L24 90 Z",PANTS,pivot=(18,93)),
        part("shoe-left","M-42 210 Q-62 216 -65 234 L-6 234 L-9 214 Z",INK,pivot=(-18,93)),
        part("shoe-right","M8 214 L42 210 Q60 215 63 234 L8 234 Z",INK,pivot=(18,93)),
        part("detail","M-48 -186 Q-18 -210 14 -207 M-19 -90 Q2 -83 18 -91",width=2)
    ]


def cat_parts(expression="happy"):
    if expression not in {"happy","sad","determined"}:
        raise ValueError("unsupported cat expression")
    eye={"happy":"M-22 -151 Q-16 -145 -10 -151 M13 -151 Q19 -145 25 -151",
         "sad":"M-23 -147 Q-16 -141 -10 -151 M12 -151 Q18 -141 26 -147",
         "determined":"M-24 -153 L-9 -148 M12 -148 L27 -153"}[expression]
    return [
        part("body","M-55 -73 Q-85 3 -54 81 Q-8 109 57 73 Q81 0 54 -72 Q15 -96 -55 -73 Z",WHITE),
        part("head","M-50 -173 L-59 -225 L-23 -197 Q0 -207 24 -197 L59 -225 L49 -169 Q79 -124 39 -99 Q1 -83 -41 -100 Q-75 -122 -50 -173 Z",SKIN),
        part("ear","M-43 -196 L-48 -216 L-28 -199 M30 -197 L48 -217 L45 -195",WHITE,width=3),
        part("eye",eye,width=5),
        part("nose","M-8 -137 L8 -137 L0 -128 Z",INK,width=3),
        part("mouth","M0 -128 Q-12 -112 -23 -122 M0 -128 Q12 -112 23 -122",width=3),
        part("whisker","M-30 -129 L-75 -140 M-30 -123 L-79 -120 M30 -129 L75 -140 M30 -123 L79 -120",width=3),
        part("detail","M-28 -180 Q-6 -191 12 -187 M-11 -178 L-8 -168 M12 -179 L16 -166",width=4),
        part("arm-left","M-43 -22 Q-64 11 -49 60 L-31 60 L-23 -14 Z",WHITE,pivot=(-45,-35)),
        part("arm-right","M43 -22 Q64 11 49 60 L31 60 L23 -14 Z",WHITE,pivot=(45,-35)),
        part("leg-left","M-45 64 Q-66 108 -36 124 L-10 104 L-18 73 Z",WHITE,pivot=(-32,68)),
        part("leg-right","M45 64 Q66 108 36 124 L10 104 L18 73 Z",WHITE,pivot=(32,68)),
        part("tail","M54 35 Q128 19 112 -51 Q101 -80 75 -62",width=14,pivot=(53,30)),
        part("detail","M-25 76 L-31 91 M24 76 L31 91",width=2)
    ]


def scene_paths(location):
    if location not in {"street","park"}:
        raise ValueError("unsupported scene location")
    def stroke(d,start,end,width=6,color=INK):
        return {"type":"path","d":d,"start":start,"end":end,
                "strokeWidth":width,"stroke":color}
    shared=[
        stroke("M0 1430 L1080 1430 M0 1530 L1080 1530",0.05,0.9,7),
        stroke("M100 1560 L245 1560 M440 1560 L630 1560 M820 1560 L1000 1560",0.7,1.4,5)
    ]
    if location=="street":
        shared += [
            stroke("M60 1415 L60 650 L315 650 L315 1415",0.2,1.4,5),
            stroke("M80 710 L298 710 M120 775 L173 775 L173 890 L120 890 Z M222 775 L275 775 L275 890 L222 890 Z",0.4,1.7,4),
            stroke("M785 1400 L785 545 L1030 545 L1030 1400",0.3,1.8,5),
            stroke("M808 660 L870 660 L870 780 L808 780 Z M926 660 L1000 660 L1000 780 L926 780 Z",0.7,1.9,4),
            stroke("M900 540 L900 435 M855 450 Q900 390 945 450",0.8,1.9,5),
            stroke("M390 1420 L390 970 M365 982 Q390 946 415 982",0.9,2.1,5),
        ]
    else:
        shared += [
            stroke("M130 1420 L130 890 M130 1110 Q-5 1080 80 935 Q130 800 185 917 Q305 1014 130 1110",0.2,1.5,6),
            stroke("M900 1420 L900 905 M900 1070 Q735 1040 806 924 Q897 791 978 914 Q1090 1022 900 1070",0.3,1.8,6),
            stroke("M370 1380 Q520 1230 710 1390 M350 1400 Q540 1290 725 1400",0.6,2.0,4),
            stroke("M420 730 Q450 706 477 730 M523 705 Q550 683 576 705",0.8,1.9,3),
        ]
    return shared


def load_words(path,duration):
    if path is None:
        return []
    obj=json.loads(Path(path).read_text(encoding="utf-8"))
    rows=obj.get("words") if isinstance(obj,dict) else None
    if rows is None and isinstance(obj,dict) and isinstance(obj.get("segments"),list):
        rows=[word for segment in obj["segments"] if isinstance(segment,dict)
              for word in segment.get("words",[])]
    if not isinstance(rows,list):
        raise ValueError("word timing file needs words or WhisperX segments[].words")
    result=[]
    previous=0.0
    for row in rows:
        if not isinstance(row,dict) or not isinstance(row.get("word",row.get("text")),str):
            raise ValueError("each word requires text")
        word=row.get("word",row.get("text")).strip()
        if not word:
            continue
        # WhisperX can return no timestamps for noisy words; do not synthesize them.
        if row.get("start") is None or row.get("end") is None:
            raise ValueError("unaligned word lacks timestamp")
        a=director.number(row["start"],0,duration)
        b=director.number(row["end"],0,duration)
        if not (previous<=a<b):
            raise ValueError("word alignment overlap/out-of-range")
        result.append({"text":director.text(word,120),"start":a,"end":b})
        previous=b
    if len(result)>240:
        raise ValueError("too many words for a scene")
    return result


def make_story(cast="human",expression="happy",location="street",action="walk",
               duration=9.0,fps=30,words=None):
    dur=director.number(duration,4,120)
    if cast not in {"human","cat","human+cat"}:
        raise ValueError("unsupported cast")
    if action not in {"idle","walk","run","wave","point","sit"}:
        raise ValueError("unsupported action")
    if expression not in {"happy","sad","determined"}:
        raise ValueError("unsupported mood")
    stage=scene_paths(location)
    stage += [{"type":"text","text":"KOSIF DRAWING","direction":"ltr","fontSize":60,
               "x":540,"y":330,"start":0.3,"end":1.5,"fill":GREEN}]
    stage.append({"type":"morph","start":round(dur*0.72,3),
                  "end":round(dur*0.96,3),"closed":True,
                  "from":[[510,500],[555,500],[575,545],[535,578],[494,545]],
                  "to":[[535,470],[558,520],[600,526],[568,558],[532,590]],
                  "stroke":GREEN,"strokeWidth":7})
    actors=[cast] if cast!="human+cat" else ["human","cat"]
    for kind in actors:
        x=400 if cast=="human+cat" and kind=="human" else (700 if kind=="cat" and cast=="human+cat" else 540)
        y=1180 if kind=="human" else 1250
        scale=1.75 if kind=="human" else (1.35 if cast=="human+cat" else 2.15)
        parts=human_parts(expression) if kind=="human" else cat_parts(expression)
        stage.append({"type":"actor","x":x,"y":y,"scale":scale,
                      "parts":parts,"action":action,
                      "start":1.6,"end":min(5.4,dur-1),
                      "move":{"fromX":-40 if kind=="human" else 25,
                              "toX":80 if action in {"run","walk"} else 0,
                              "start":min(5.4,dur-1),"end":dur}})
    result={"version":1,"width":1080,"height":1920,"fps":fps,"duration":dur,
            "scenes":[{"id":"draw_story","start":0,"end":dur,"background":CREAM,
                       "camera":{"fromZoom":1,"toZoom":1.065,"start":0,"end":dur},
                       "words":words or [],"elements":stage}]}
    director.validate(result)
    return result


def write_new(path,text):
    p=Path(path).expanduser()
    if p.is_symlink() or p.exists() or not p.parent.is_dir():
        raise ValueError("output must be new, with existing parent directory")
    with p.open("x",encoding="utf-8") as f:
        f.write(text)
    return str(p.resolve())


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cast",choices=["human","cat","human+cat"],default="human+cat")
    ap.add_argument("--expression",choices=["happy","sad","determined"],default="happy")
    ap.add_argument("--location",choices=["street","park"],default="street")
    ap.add_argument("--action",choices=["idle","walk","run","wave","point","sit"],default="walk")
    ap.add_argument("--duration",type=float,default=9)
    ap.add_argument("--fps",type=int,choices=[24,25,30,60],default=30)
    ap.add_argument("--words-json",help="pre-aligned, timestamped word JSON; never synthesize timing")
    ap.add_argument("--out",required=True)
    ap.add_argument("--html",help="optional new compiled HTML path")
    args=ap.parse_args()
    try:
        words=load_words(args.words_json,args.duration)
        spec=make_story(args.cast,args.expression,args.location,args.action,
                        args.duration,args.fps,words)
        output=write_new(args.out,json.dumps(spec,ensure_ascii=False,indent=2)+"\n")
        report={"status":"editable_storyboard_created","path":output,
                "actors":args.cast,"parts":[len(e["parts"]) for e in spec["scenes"][0]["elements"]
                          if e["type"]=="actor"],
                "verified_word_timestamps":len(words),"rendered":False}
        if args.html:
            report["html"]=director.compile_spec(spec,args.html)
        print(json.dumps(report,ensure_ascii=False,indent=2))
        return 0
    except (OSError,ValueError,json.JSONDecodeError) as exc:
        print(json.dumps({"status":"failed","reason":str(exc)},ensure_ascii=False),file=sys.stderr)
        return 2


if __name__=="__main__":
    sys.exit(main())
