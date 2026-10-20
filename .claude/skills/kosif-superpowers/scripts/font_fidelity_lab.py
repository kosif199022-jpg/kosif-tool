#!/usr/bin/env python3
"""KOSIF Font Fidelity Lab: Arabic-aware font fingerprint and candidate visual ranking.

It DOES NOT identify proprietary typefaces by magic: a high visual score on
one phrase is only a candidate. User supplies licensed fonts and a tight text crop.

Usage:
  python font_fidelity_lab.py inspect /path/to/font.ttf --text "جمعة مباركة"
  python font_fidelity_lab.py rank target-crop.png --text "جمعة مباركة" --fonts ./licensed --top 5

Pillow is required for rendering. fontTools is optional for OpenType metadata
(WOFF2 metadata also needs brotli). A missing or unreadable font exits 2 with FONT FIDELITY ERROR.
For correct Arabic use libraqm text shaping (Pillow RAQM). Never fake RTL.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

def _pillow():
    try:
        from PIL import Image, ImageFont, features
    except ImportError as exc:
        raise RuntimeError("install Pillow and its libraqm support for visual matching") from exc
    return Image,ImageFont,features

def rtl(text: str) -> bool:
    return any("\u0600" <= c <= "\u08ff" or "\ufb50" <= c <= "\ufeff" for c in text)

def info(path: Path, text: str="") -> dict:
    if path.suffix.lower() not in (".ttf",".otf",".woff",".woff2"):
        raise ValueError("use a licensed TTF/OTF/WOFF/WOFF2 font")
    if not path.is_file():
        raise FileNotFoundError(path)
    o={"path":str(path),"bytes":path.stat().st_size,"coverage":None,
       "gsub":None,"gpos":None,"variable_axes":[],"family":None,
       "source_rights":"user must verify font license"}
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        o["inspection_note"]="fontTools not installed; raster inspection still possible"
        return o
    if path.suffix.lower()==".woff2":
        try:
            from fontTools.ttLib import woff2
            have_brotli=getattr(woff2,"haveBrotli",True)
        except ImportError:
            have_brotli=False
        if not have_brotli:
            o["inspection_note"]="fontTools is installed but reading WOFF2 needs the brotli module (pip install brotli)"
            return o
    try:
        f=TTFont(str(path))
        cps=set(f.getBestCmap() or {})
        o["coverage"]={"requested":len(text),"missing":[f"U+{ord(c):04X}" for c in text if ord(c) not in cps],
                       "glyph_cmap":len(cps)}
        o["gsub"]="GSUB" in f
        o["gpos"]="GPOS" in f
        if "fvar" in f:
            o["variable_axes"]=[{"tag":v.axisTag,"min":v.minValue,"default":v.defaultValue,
                                 "max":v.maxValue} for v in f["fvar"].axes]
        if "name" in f:
            names=f["name"].names
            family=next((n.toUnicode() for n in names if n.nameID==1),None)
            o["family"]=family
        f.close()
    except ImportError as exc:
        o["inspection_note"]=f"fontTools could not load a decoder for this font: {exc}"
    except Exception as exc:
        raise ValueError(f"not a readable TTF/OTF/WOFF/WOFF2 font: {path} ({exc})") from exc
    return o

def render_font(font: Path, text: str, size: int):
    Image,ImageFont,features=_pillow()
    direction="rtl" if rtl(text) else "ltr"
    if direction=="rtl" and not features.check("raqm"):
        raise RuntimeError("Arabic shaping requires Pillow built with libraqm; do not claim RTL fidelity without it")
    try:
        layout=ImageFont.Layout.RAQM if features.check("raqm") else ImageFont.Layout.BASIC
        face=ImageFont.truetype(str(font),size,layout_engine=layout)
    except (ValueError,OSError) as exc:
        raise RuntimeError("unable to render supplied font: "+str(exc)) from exc
    kwargs={"direction":direction,"language":"ar" if direction=="rtl" else "en"} if features.check("raqm") else {}
    box=face.getbbox(text,**kwargs)
    width=max(1,box[2]-box[0])
    height=max(1,box[3]-box[1])
    im=Image.new("L",(width+24,height+24),0)
    from PIL import ImageDraw
    draw=ImageDraw.Draw(im)
    draw.text((12-box[0],12-box[1]),text,font=face,fill=255,**kwargs)
    return im

def crop_mask(im):
    Image,_,_=_pillow()
    src=im.convert("L")
    # Test both dark-on-light and light-on-dark polarity; choose the sparser ink.
    light=src.point(lambda p:255 if p>=160 else 0)
    dark=src.point(lambda p:255 if p<=95 else 0)
    return [tight_mask(x) for x in (light,dark)]

def tight_mask(src):
    box=src.getbbox()
    return src.crop(box) if box else src

def ratio_overlap(a,b) -> float:
    """Scale-normalized binary IoU in one 128x64 canvas; 1 is identical."""
    Image,_,_=_pillow()
    if not a.getbbox() or not b.getbbox():return 0.0
    aa=tight_mask(a).resize((128,64),Image.Resampling.NEAREST).point(lambda p:255 if p>=128 else 0)
    bb=tight_mask(b).resize((128,64),Image.Resampling.NEAREST).point(lambda p:255 if p>=128 else 0)
    ab=aa.tobytes();by=bb.tobytes()
    intersection=sum(x>0 and y>0 for x,y in zip(ab,by))
    union=sum(x>0 or y>0 for x,y in zip(ab,by))
    return round(intersection/union,5) if union else 0.0

def rank(reference: Path, text: str, font_dir: Path, top: int=5) -> list[dict]:
    Image,_,_=_pillow()
    if not reference.is_file():raise FileNotFoundError(reference)
    if not font_dir.is_dir():raise FileNotFoundError(font_dir)
    target=crop_mask(Image.open(reference))
    candidates=[]
    for p in sorted(font_dir.rglob("*")):
        if p.suffix.lower() not in (".ttf",".otf") or not p.is_file():
            continue
        result={"font":str(p),"score":0.0,"best_size":None,"status":"candidate_only"}
        try:
            best=(0.0,None)
            for size in (48,64,80,104,128):
                probe=render_font(p,text,size)
                score=max(ratio_overlap(probe,t) for t in target)
                if score>best[0]:best=(score,size)
            result["score"],result["best_size"]=best
        except (RuntimeError,OSError,ValueError) as exc:
            result["status"]="unsupported:"+str(exc)[:160]
        candidates.append(result)
    candidates.sort(key=lambda x:(-x["score"],x["font"]))
    return candidates[:max(1,min(top,50))]

def main(argv=None)->int:
    ap=argparse.ArgumentParser(description=__doc__)
    sub=ap.add_subparsers(dest="cmd",required=True)
    x=sub.add_parser("inspect");x.add_argument("font");x.add_argument("--text",default="جمعة مباركة")
    y=sub.add_parser("rank");y.add_argument("reference");y.add_argument("--text",required=True);y.add_argument("--fonts",required=True);y.add_argument("--top",type=int,default=5)
    ns=ap.parse_args(argv)
    try:
        if ns.cmd=="inspect":
            data={"schema":"font_fidelity_inspection_v1","font":info(Path(ns.font),ns.text)}
        else:
            data={"schema":"font_fidelity_ranking_v1","reference":ns.reference,"text":ns.text,
                  "metric":"normalized mask IoU; higher is visually closer on given phrase",
                  "limitations":"not font identification; crop/polarity, size, ligatures, diacritics, layout and font licensing can alter results",
                  "candidates":rank(Path(ns.reference),ns.text,Path(ns.fonts),ns.top)}
    except (ValueError,FileNotFoundError,RuntimeError) as exc:
        ap.exit(2,f"FONT FIDELITY ERROR: {exc}\n")
    print(json.dumps(data,ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
