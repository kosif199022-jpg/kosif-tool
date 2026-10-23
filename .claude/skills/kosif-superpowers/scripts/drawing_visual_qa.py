#!/usr/bin/env python3
"""Evidence-based drawing critique & edit-preservation lab, KOSIF original code.

This is a *diagnostic* aid for Claude: objective metrics + source-linked
practice tasks, not a beauty classifier, aesthetic judge or model training.
Pillow is optional for this narrow tool and already used by KOSIF art runtimes.
"""
import argparse
import colorsys
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

BOOKS = {
 "speed": {"book":"The Practice and Science of Drawing","author":"Harold Speed",
           "source":"https://www.gutenberg.org/cache/epub/14264/pg14264-images.html",
           "section":"IX, Mass Drawing: Practical", "review_status":"source_section_read",
           "principle":"Separate light, half-tone and shadow masses before detail.",
           "practice":"Sketch one object with only three values and keep the shape of each mass readable.",
           "verify":"Review all three tonal masses and deliberately assess boundaries; no numeric ideal ratio is claimed."},
 "dow": {"book":"Composition","author":"Arthur Wesley Dow",
         "source":"https://www.gutenberg.org/cache/epub/45410/pg45410-images.html",
         "section":"VIII, Harmony-Building with Dark-and-Light","review_status":"source_section_read",
         "principle":"Arrange contrasting dark and light masses as a whole (notan).",
         "practice":"Make three thumbnails using only black and paper-white before a detailed draft.",
         "verify":"Inspect visual harmony and direction of attention; balance numbers are diagnostics only."},
 "storey": {"book":"The Theory and Practice of Perspective","author":"G. A. Storey",
            "source":"https://www.gutenberg.org/cache/epub/20165/pg20165-images.html",
            "section":"XXV-XXVII, Perspective Vanishing Scale and Application to Figures","review_status":"source_section_read",
            "principle":"Use horizon/vanishing scales to relate objects or people placed at different depths.",
            "practice":"Draw a row of figures and verify equal real-world heights project to a shared vanishing scale.",
            "verify":"Check geometric convergence manually or use a verified perspective construction test; a raster cannot prove it."},
 "munsell": {"book":"A Color Notation","author":"Albert H. Munsell",
            "source":"https://www.gutenberg.org/cache/epub/26054/pg26054-images.html",
            "section":"II, Color Qualities: hue, value, chroma","review_status":"source_section_read",
            "principle":"Treat hue, lightness/value and chroma as distinct design questions.",
            "practice":"Create three variations: change hue, change value, change colorfulness independently.",
            "verify":"Measure RGB/HSV proxies; HSV saturation is NOT Munsell chroma and no conversion is claimed."}
}
MAX_BYTES=48*1024*1024
MAX_PIXELS=22_000_000


def _pillow():
    from PIL import Image
    return Image


def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as inp:
        for chunk in iter(lambda:inp.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()


def check_file(value):
    p=Path(value).expanduser()
    if not p.is_file() or p.is_symlink() or not 1 <= p.stat().st_size <= MAX_BYTES:
        raise ValueError("use an existing regular image file <=48 MB (not symlink)")
    if p.suffix.lower() not in (".png",".jpg",".jpeg",".webp",".tif",".tiff"):
        raise ValueError("unsupported raster image extension")
    return p


def sample(path):
    """Sampling capped at 512 px long edge, no remote requests or modifications."""
    Image=_pillow()
    p=check_file(path)
    with Image.open(p) as im:
        if im.width*im.height > MAX_PIXELS or im.width<1 or im.height<1:
            raise ValueError("image exceeds 22 million pixels")
        size=im.size
        rgba=im.convert("RGBA")
        if max(size)>512:
            ratio=512/max(size)
            rgba=rgba.resize((max(1,round(size[0]*ratio)),max(1,round(size[1]*ratio))),Image.Resampling.BILINEAR)
        return {"path":p,"size":size,"image":rgba,"file_sha256":sha(p)}


def _luma(pixel):
    return round(.2126*pixel[0]+.7152*pixel[1]+.0722*pixel[2])


def pixels(img):
    """Pillow 13/14 compatibility without deprecated getdata API."""
    if hasattr(img, "get_flattened_data"):
        return list(img.get_flattened_data())
    return list(img.getdata())


def summary(s):
    pix=pixels(s["image"])
    n=len(pix)
    visible=[p for p in pix if p[3]>=16]
    alpha= len(visible)!=n
    used=visible or pix
    vals=[_luma(p) for p in used]
    bins=[sum(v<85 for v in vals),sum(85<=v<171 for v in vals),sum(v>=171 for v in vals)]
    proportions=[round(x/len(vals),4) for x in bins]
    w,h=s["image"].size
    dark_left=sum(_luma(pix[y*w+x])<85 and pix[y*w+x][3]>=16 for y in range(h) for x in range(w//2))
    dark_right=sum(_luma(pix[y*w+x])<85 and pix[y*w+x][3]>=16 for y in range(h) for x in range((w+1)//2,w))
    balance=1.0 if dark_left+dark_right==0 else 1-abs(dark_left-dark_right)/(dark_left+dark_right)
    rgb_saturation=[colorsys.rgb_to_hsv(*(v/255 for v in p[:3]))[1] for p in used[::max(1,len(used)//4096)]]
    warnings=["A numeric tone histogram cannot judge artistic quality or perspective."]
    if not alpha:
        warnings.append("No transparent pixels: subject occupancy/negative-space cannot be isolated from background.")
    if proportions[0]<=0.01:
        warnings.append("Very little dark-value coverage; inspect focal contrast instead of adding darks blindly.")
    if proportions[2]<=0.01:
        warnings.append("Very little light-value coverage; inspect form separation.")
    return {"schema":"kosif.drawing.visual_diagnostic.v1","status":"MEASURED_NOT_ART_JUDGMENT",
            "file_sha256":s["file_sha256"],"size_px":{"width":s["size"][0],"height":s["size"][1]},
            "samples":n, "sampled_size_px":{"width":w,"height":h},
            "transparent_background_detected":alpha,"visible_fraction":round(len(visible)/n,5),
            "three_value_ratio":{"dark":proportions[0],"middle":proportions[1],"light":proportions[2]},
            "dark_mass_left_right_index":round(balance,4),
            "approx_hsv_saturation_mean":round(sum(rgb_saturation)/len(rgb_saturation),4),
            "methods":[{"book_key":k,"section":b["section"],"source":b["source"],"review_status":b["review_status"]} for k,b in BOOKS.items()],
            "exercises":[b["practice"] for b in BOOKS.values()],
            "warnings":warnings}


def diagnostic(path):
    return summary(sample(path))


def compare(before,after,roi=None,threshold=12,max_outside_fraction=0.005):
    """Compare same-sized before/after pixel images to spot accidental edits.

    roi: allowed rectangle in pixel coordinates (x,y,width,height).
    A PASS means change scope is bounded ONLY; not that text/face are correct.
    """
    if not (0<=threshold<=255 and 0<=max_outside_fraction<=1):
        raise ValueError("invalid threshold or outside fraction")
    a,b=sample(before),sample(after)
    if a["size"]!=b["size"]:
        return {"schema":"kosif.drawing.edit_preservation.v1","status":"SIZE_MISMATCH",
                "before_size":a["size"],"after_size":b["size"],
                "before_sha256":a["file_sha256"],"after_sha256":b["file_sha256"],
                "pass":False}
    w0,h0=a["size"]
    if roi is not None:
        if type(roi) not in (list,tuple) or len(roi)!=4:
            raise ValueError("ROI must be x,y,width,height")
        x,y,rw,rh=roi
        if not all(type(v)==int for v in roi) or not (0<=x<w0 and 0<=y<h0 and 0<rw<=w0-x and 0<rh<=h0-y):
            raise ValueError("ROI must fit original image exactly")
    w,h=a["image"].size
    pa=pixels(a["image"]);pb=pixels(b["image"])
    changed=outside=outside_count=inside_count=0
    changed_inside=0
    for i,(v,u) in enumerate(zip(pa,pb)):
        diff=max(abs(t-z) for t,z in zip(v,u))
        px,py=i%w,i//w
        orig_x=(px+.5)*w0/w
        orig_y=(py+.5)*h0/h
        inside=roi is None or (x<=orig_x<x+rw and y<=orig_y<y+rh)
        if inside:inside_count+=1
        else:outside_count+=1
        if diff>threshold:
            changed+=1
            if inside:changed_inside+=1
            else:outside+=1
    outside_rate=outside/max(1,outside_count)
    result={"schema":"kosif.drawing.edit_preservation.v1","status":"SCOPE_PRESERVED" if roi is not None and outside_rate<=max_outside_fraction else ("OUT_OF_SCOPE_CHANGE" if roi is not None else "CHANGE_MEASURED"),
            "pass":bool(roi is not None and outside_rate<=max_outside_fraction),
            "before_sha256":a["file_sha256"],"after_sha256":b["file_sha256"],
            "original_size":list(a["size"]),"sampled_size":[w,h],
            "changed_sample_fraction":round(changed/len(pa),6),
            "changed_inside_sample_fraction":round(changed_inside/max(inside_count,1),6),
            "changed_outside_sample_fraction":round(outside_rate,6),
            "outside_budget":max_outside_fraction,"roi_original_px":list(roi) if roi is not None else None,
            "warnings":["This check cannot verify identity, spelling, artistic merit, or semantic fidelity.",
                        "Resampling can underreport small details; inspect full resolution and source artwork.",
                        "A PASS only checks whether visual changes stayed inside the requested region."]}
    return result


def curriculum(goal):
    if not goal.strip() or len(goal)>2000:
        raise ValueError("goal required")
    words=goal.lower()
    keys=["speed","dow","storey","munsell"]
    if any(x in words for x in ("منظور","عمارة","perspective","isometric")): keys=["storey","dow","speed","munsell"]
    elif any(x in words for x in ("لون","ألوان","color","palette")): keys=["munsell","dow","speed","storey"]
    elif any(x in words for x in ("شخصية","وجه","portrait","character","رسم")): keys=["speed","storey","dow","munsell"]
    return {"schema":"kosif.drawing.source_study.v1","status":"SOURCE_CHAPTERS_READ_NOT_200_BOOKS",
            "goal":goal,"books_reviewed_in_this_module":len(BOOKS),
            "lessons":[{"order":i+1,**BOOKS[k],"success_criteria":"Student produces an artifact and records independent visual review"} for i,k in enumerate(keys)],
            "handoff":"KOSIF drawing_methods.py constructs; this tool diagnoses a generated raster; human checks style and expression; FusionForge records evidence.",
            "limitations":"Reading chapters and running exercises do not retrain model weights or guarantee a professional artist."}


def fresh(path,result):
    p=Path(path)
    if not p.parent.is_dir() or p.exists() or p.is_symlink():
        raise ValueError("output directory must exist and result must be new")
    with p.open("x",encoding="utf-8") as f:
        json.dump(result,f,ensure_ascii=False,indent=2)
        f.write("\n")


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    sub=ap.add_subparsers(dest="cmd",required=True)
    co=sub.add_parser("curriculum");co.add_argument("goal");co.add_argument("--out")
    dg=sub.add_parser("diagnose");dg.add_argument("image");dg.add_argument("--out")
    ck=sub.add_parser("compare");ck.add_argument("before");ck.add_argument("after")
    ck.add_argument("--roi",nargs=4,type=int,metavar=("X","Y","WIDTH","HEIGHT"))
    ck.add_argument("--threshold",type=int,default=12);ck.add_argument("--out")
    args=ap.parse_args(argv)
    try:
        if args.cmd=="curriculum":result=curriculum(args.goal)
        elif args.cmd=="diagnose":result=diagnostic(args.image)
        else:result=compare(args.before,args.after,args.roi,args.threshold)
        if getattr(args,"out",None):fresh(args.out,result)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 0
    except (ValueError,OSError,ImportError,TypeError,RuntimeError) as e:
        print(json.dumps({"status":"ERROR","message":str(e)},ensure_ascii=False),file=sys.stderr)
        return 2


if __name__=="__main__":
    raise SystemExit(main())
