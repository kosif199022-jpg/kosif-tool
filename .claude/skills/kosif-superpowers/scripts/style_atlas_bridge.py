#!/usr/bin/env python3
"""KOSIF Style Atlas bridge: offline discovery, synthesis and ORIGINAL SVG sketches.

15 independently expressed technique presets from the publicly readable part of
Futurepedia AI Style Atlas, not a model, prompt clone, or full animation renderer.
Never downloads, executes an external generator, or calls Katana.
"""
import argparse
import hashlib
import html
import json
import math
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
DATA = SKILL / "data" / "futurepedia_style_methods_15.json"
ALLOWED = ("9:16", "16:9", "1:1", "4:5")
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")


def registry(path=DATA):
    obj = json.loads(Path(path).read_text(encoding="utf-8"))
    if obj.get("schema") != "kosif.style.atlas.v1":
        raise ValueError("unexpected registry schema")
    items = obj.get("styles")
    if not isinstance(items, list) or len(items) != 15:
        raise ValueError("only the 15 public, reviewed style summaries are registered")
    ids = set()
    for i, item in enumerate(items, 1):
        if item.get("id") != "FA-" + str(i).zfill(2) or item.get("id") in ids:
            raise ValueError("duplicate or unordered capability IDs")
        ids.add(item["id"])
        if not isinstance(item.get("technique_cues"), list) or not item["technique_cues"]:
            raise ValueError("empty techniques")
        if len(item.get("palette", [])) != 4 or any(not isinstance(c, str) or not HEX.fullmatch(c) for c in item["palette"]):
            raise ValueError("invalid HEX palette")
        if item.get("executor_verified") is not False:
            raise ValueError("style technique cannot imply a verified executor")
        if not isinstance(item.get("suggested_tools"), list):
            raise ValueError("missing tool routing")
    return obj


def resolve(items, token):
    key = token.strip().casefold()
    if not key:
        raise ValueError("style must not be blank")
    matches = [s for s in items if key in (s["id"].casefold(), s["slug"].casefold(), s["name"].casefold())]
    if len(matches) != 1:
        raise ValueError("unknown or ambiguous style " + token)
    return matches[0]


def search(items, query):
    q = query.strip().casefold()
    if not q or len(q) > 200:
        raise ValueError("search must be 1-200 characters")
    aliases = {"سبورة": "whiteboard", "ألوان": "color", "مائي": "watercolor",
               "نيون": "glow", "منتج": "product", "منظور": "isometric",
               "رياضيات": "math", "ظل": "shadow", "كرتون": "pop", "سينما": "film"}
    for word, meaning in aliases.items():
        if word in q:
            q += " " + meaning
    words = [w for w in re.split(r"[^\w\u0600-\u06ff]+", q) if len(w) >= 2]
    ranked = []
    for s in items:
        hay = " ".join([s["id"], s["slug"], s["name"], s["category"], s["capability_ar"],
                        " ".join(s["technique_cues"]), s["motion_direction"]]).casefold()
        score = sum(3 if w in s["slug"] else 1 for w in words if w in hay)
        if score:
            ranked.append((score, s["id"], s))
    return [s for _, _, s in sorted(ranked, key=lambda x: (-x[0], x[1]))]


def plan(topic, styles, *, duration=15, aspect="9:16"):
    if not isinstance(topic, str) or not 1 <= len(topic.strip()) <= 300:
        raise ValueError("topic must have 1-300 characters")
    if type(duration) not in (int, float) or not math.isfinite(duration) or not 2 <= duration <= 180:
        raise ValueError("duration must be 2-180 seconds")
    if aspect not in ALLOWED:
        raise ValueError("invalid aspect")
    if not 1 <= len(styles) <= 2 or len({x["id"] for x in styles}) != len(styles):
        raise ValueError("use one or two distinct reviewed styles")
    a = styles[0]
    b = styles[1] if len(styles) == 2 else None
    sequence = [
        {"node": "N01", "role": "rights_and_assets", "input": "topic + user authorized assets",
         "output": "asset_manifest", "owner": "human + source scout", "verified": False},
        {"node": "N02", "role": "art_direction", "input": "asset_manifest + style contracts",
         "output": "visual_style_brief", "owner": "style_atlas_bridge.plan", "verified": True},
        {"node": "N03", "role": "original_scene", "input": "visual_style_brief",
         "output": "original_editable_scene", "owner": "suggested art engines; confirm live availability", "verified": False},
        {"node": "N04", "role": "timed_animation", "input": "original_editable_scene + measured audio/word timings",
         "output": "candidate_video", "owner": "motion director / montage pro; not invoked", "verified": False},
        {"node": "N05", "role": "independent_verification", "input": "candidate_video + source audio",
         "output": "qa_receipt", "owner": "verify_video.py + visual review", "verified": False}
    ]
    palette = a["palette"][:3] + ([b["palette"][2]] if b else [a["palette"][3]])
    return {"schema": "kosif.style.fusion_recipe.v1", "status": "PLAN_ONLY_NOT_RENDERED",
            "topic": topic.strip(), "duration_seconds": duration, "aspect": aspect,
            "source": a["source_url"], "source_review": "15 public descriptions, not all 86",
            "styles": [{"id":s["id"], "name":s["name"], "techniques":s["technique_cues"],
                        "motion":s["motion_direction"], "qa":s["acceptance_checks"],
                        "suggested_tools":s["suggested_tools"], "mix_weight": .85 if s == a and b else .15 if b else 1.0}
                       for s in styles],
            "technique_fusion": {"primary_id": a["id"], "secondary_id": b["id"] if b else None,
                 "guard": "Keep one dominant visual system; secondary supplies accents up to 15%, never hides text.",
                 "palette": palette, "visual_conflict_review_required": bool(b)},
            "workflow": sequence,
            "required_gates": ["media rights and user approval", "Arabic shaping + safe margins when applicable",
                               "real audio word timing if sync requested", "video dimensions / fps / duration",
                               "original audio integrity", "visual inspection of result"],
            "katana_policy": "ANALYSIS_ONLY_IF_VERIFIED_FREE_READ_ONLY; never generate or spend credits",
            "claim_boundary": "Method recipe is executable planning output, not proof 15 full render engines run."}


def svg_study(style, topic):
    """Produce a deterministic vector study with a distinct original motif per preset.
    This is a schematic study, NOT a generated animated scene or prompt recreation.
    """
    if not isinstance(topic, str) or not 1 <= len(topic.strip()) <= 100:
        raise ValueError("topic must have 1-100 characters")
    p = style["palette"]
    slug = style["slug"]
    pale = slug in {"watercolor-wash", "whiteboard-explainer", "papercraft-models",
                    "illuminated-manuscript", "editorial-essay-collage", "halftone-pop-panel", "isometric-pastel"}
    ink = "#171F27" if pale else "#F8F8F1"
    body = []
    def line(x1,y1,x2,y2,c=None,width=3,dash=""):
        body.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s" %s/>' %
                    (x1,y1,x2,y2,c or p[2],width,('stroke-dasharray="'+dash+'"') if dash else ""))
    def circle(x,y,r,c,opacity=1):
        body.append('<circle cx="%s" cy="%s" r="%s" fill="%s" opacity="%s"/>'%(x,y,r,c,opacity))
    def rect(x,y,w,h,c,rx=0,opacity=1):
        body.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" opacity="%s"/>'%(x,y,w,h,rx,c,opacity))
    if slug == "flat-vector-science":
        circle(215,245,120,p[1]);circle(215,245,80,p[2],.8);circle(220,240,30,p[3])
        for i in range(5): circle(58+i*65,95+i%2*13,4,p[3])
    elif slug == "watercolor-wash":
        for i in range(12): circle(100+i*17,185+(i%3-1)*25,46+i%4*9,p[i%4],.10)
        for i in range(7): circle(135+i*25,284-i%3*19,47,p[(i+1)%4],.13)
    elif slug == "shadow-puppet-theatre":
        rect(55,116,338,232,p[3],18);circle(218,227,82,p[0]);rect(178,285,90,55,p[0])
        circle(194,215,8,p[2]);line(214,290,153,355,p[0]);line(257,290,322,355,p[0])
    elif slug == "whiteboard-explainer":
        circle(214,197,58,"none");body.append('<circle cx="214" cy="197" r="58" fill="none" stroke="%s" stroke-width="5"/>'%p[1])
        line(214,256,214,337,p[1],6);line(214,277,148,315,p[1],5);line(214,277,279,314,p[1],5)
        line(214,337,169,376,p[1],5);line(214,337,265,376,p[1],5)
        body.append('<path d="M 122 136 Q 213 75 305 136" fill="none" stroke="%s" stroke-width="4" stroke-dasharray="9 7"/>'%p[2])
    elif slug == "psychedelic-poster":
        for i in range(10):circle(220,250,150-i*14,p[(i+1)%4],.92)
        body.append('<path d="M 95 210 Q 220 35 330 230 Q 160 355 95 210" fill="%s"/>'%p[1])
    elif slug == "tech-glow-explainer":
        for i in range(4):
            line(70+i*95,110,120+i*55,335,p[1],2)
        for i in range(8):
            x=80+(i%4)*95;y=170+(i//4)*130
            circle(x,y,33,p[1],.45);circle(x,y,13,p[2]);circle(x,y,5,p[3])
    elif slug == "papercraft-models":
        body.append('<polygon points="220,117 342,190 221,262 97,192" fill="%s"/>'%p[2])
        body.append('<polygon points="97,192 221,262 221,379 97,310" fill="%s"/>'%p[1])
        body.append('<polygon points="221,262 342,190 342,310 221,379" fill="%s"/>'%p[3])
        line(220,117,221,262,p[0],3,"8 8")
    elif slug == "1940s-film-noir":
        rect(90,135,245,270,"#111111",10)
        for i in range(8):body.append('<polygon points="%d,115 %d,115 %d,385 %d,385" fill="#EEEEEE" opacity=".26"/>'%
                            (70+i*38,88+i*38,157+i*38,140+i*38))
        circle(211,256,62,p[1])
    elif slug == "manim-style-math":
        line(88,332,368,332,p[3],3);line(108,368,108,136,p[3],3)
        body.append('<path d="M 112 290 Q 195 118 287 251 Q 325 312 368 169" fill="none" stroke="%s" stroke-width="5"/>'%p[2])
        for i in range(5):line(105+i*55,325,105+i*55,339,p[3],2)
    elif slug == "illuminated-manuscript":
        rect(75,98,297,284,"none");body.append('<rect x="75" y="98" width="297" height="284" fill="none" stroke="%s" stroke-width="10"/>'%p[1])
        for i in range(5):circle(80+i*70,115,8,p[2])
        body.append('<text x="214" y="294" font-size="155" text-anchor="middle" font-family="serif" fill="%s">K</text>'%p[1])
    elif slug == "editorial-essay-collage":
        body.append('<g transform="rotate(-10 200 250)">')
        body.append('<rect x="86" y="127" width="260" height="234" fill="%s" stroke="%s" stroke-width="8"/>'%(p[3],p[1]))
        for i in range(5):body.append('<rect x="110" y="%d" width="%d" height="8" fill="%s"/>'%(166+i*34,110+(i%3)*55,p[1]))
        body.append('</g>')
        rect(105,155,140,39,p[2],1,.7)
    elif slug == "bioluminescent-deep-sea":
        for i in range(11): circle(66+i*30,130+(i*i*17)%227,4+i%4,p[2],.4)
        body.append('<path d="M 128 235 Q 215 120 310 238 Z" fill="%s"/>'%p[2])
        for i in range(8):
            body.append('<path d="M %d 239 Q %d 310 %d 368" fill="none" stroke="%s" stroke-width="3"/>'%(140+i*21,135+i*18,155+i*18,p[2]))
    elif slug == "product-launch-reveal":
        circle(218,331,120,p[1],.22)
        rect(154,132,132,210,p[2],22);rect(167,150,106,169,p[1],11)
        circle(220,330,6,p[3]);body.append('<ellipse cx="220" cy="355" rx="125" ry="17" fill="%s" opacity=".35"/>'%p[2])
    elif slug == "halftone-pop-panel":
        for x in range(76,362,16):
            for y in range(112,356,16):
                circle(x,y,3 if (x+y)%3 else 5,p[2],.8)
        body.append('<path d="M 122 172 Q 205 88 304 174 L 304 273 Q 235 330 122 258 Z" fill="%s" stroke="%s" stroke-width="9"/>'%(p[0],p[3]))
    elif slug == "isometric-pastel":
        body.append('<polygon points="218,137 342,211 218,285 95,211" fill="%s"/>'%p[1])
        body.append('<polygon points="95,211 218,285 218,377 95,303" fill="%s"/>'%p[2])
        body.append('<polygon points="218,285 342,211 342,303 218,377" fill="%s"/>'%p[3])
    else:
        raise ValueError("unknown technique preview")
    safe_title=html.escape(topic.strip(),quote=True)
    safe_name=html.escape(style["name"],quote=True)
    body.append('<rect x="20" y="20" width="400" height="58" rx="13" fill="%s" opacity=".92"/>'%p[1])
    body.append('<text x="220" y="56" fill="%s" font-size="20" text-anchor="middle" font-family="sans-serif">%s</text>'%(ink,safe_name))
    body.append('<rect x="20" y="404" width="400" height="78" rx="10" fill="%s"/>'%p[1])
    body.append('<text x="220" y="451" fill="%s" font-size="21" text-anchor="middle" font-family="sans-serif">%s</text>'%(ink,safe_title))
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="440" height="500" viewBox="0 0 440 500" role="img">'
            '<title>%s — original procedural schematic</title>'%safe_name+
            '<rect width="440" height="500" fill="%s"/>'%p[0]+''.join(body)+'</svg>\n')


def fresh_write(path, content):
    p=Path(path)
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("x",encoding="utf-8") as f:
        f.write(content)


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    sub=ap.add_subparsers(dest="command",required=True)
    sub.add_parser("list")
    sr=sub.add_parser("search");sr.add_argument("query")
    pl=sub.add_parser("plan");pl.add_argument("--topic",required=True)
    pl.add_argument("--style",required=True);pl.add_argument("--accent")
    pl.add_argument("--duration",type=float,default=15);pl.add_argument("--aspect",default="9:16")
    pl.add_argument("--out",required=True)
    rd=sub.add_parser("study-svg");rd.add_argument("--style",required=True)
    rd.add_argument("--topic",required=True);rd.add_argument("--out",required=True)
    args=ap.parse_args(argv)
    try:
        data=registry()
        items=data["styles"]
        if args.command=="list":
            print(json.dumps({"scope":data["scope"],"styles":[{"id":s["id"],"name":s["name"],"area":s["primary_area"]} for s in items]},ensure_ascii=False,indent=2))
        elif args.command=="search":
            print(json.dumps({"matches":[{"id":s["id"],"name":s["name"]} for s in search(items,args.query)]},ensure_ascii=False,indent=2))
        elif args.command=="plan":
            selected=[resolve(items,args.style)]
            if args.accent: selected.append(resolve(items,args.accent))
            result=plan(args.topic,selected,duration=args.duration,aspect=args.aspect)
            fresh_write(args.out,json.dumps(result,ensure_ascii=False,indent=2)+"\n")
            print(json.dumps({"status":"PLAN_CREATED_NOT_RENDERED","file":args.out}))
        else:
            selected=resolve(items,args.style)
            if Path(args.out).suffix.lower()!=".svg":
                raise ValueError("study-svg requires .svg")
            fresh_write(args.out,svg_study(selected,args.topic))
            print(json.dumps({"status":"STATIC_STUDY_SVG_CREATED_NOT_VIDEO","file":args.out,"style":selected["id"]}))
        return 0
    except (ValueError,TypeError,KeyError, OSError,json.JSONDecodeError) as e:
        print("STYLE_ATLAS_ERROR: "+str(e),file=sys.stderr)
        return 2


if __name__=="__main__":
    raise SystemExit(main())
