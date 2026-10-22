#!/usr/bin/env python3
"""Original deterministic perspective + palette workshop.

Research anchors:
  G. A. Storey, Theory and Practice of Perspective, Gutenberg 20165,
      Book I horizon/sight; Book III angular perspective.
  A. H. Munsell, A Color Notation, Gutenberg 26054,
      separable Hue / Value / Chroma concept.
Neither native Munsell color transforms nor reproductions of source drawings.
"""
import argparse
import colorsys
import json
import math
import sys
from pathlib import Path


def real(v, name, minimum, maximum):
    if type(v) not in (int, float) or not math.isfinite(v) or not minimum <= v <= maximum:
        raise ValueError("invalid " + name)
    return float(v)


def point(p, name, w, h):
    if type(p) is not list or len(p) != 2:
        raise ValueError(name + " must be [x,y]")
    return (real(p[0], name+".x", 0, w), real(p[1], name+".y", 0, h))


def lerp(a, b, t):
    return (a[0] + (b[0]-a[0])*t, a[1] + (b[1]-a[1])*t)


def vecstr(p):
    return "{:.3f},{:.3f}".format(*p)


def perspective(scene):
    """A two-point cube schematic. Every receding edge intersects its named VP."""
    if type(scene) is not dict:
        raise ValueError("scene must be an object")
    w = real(scene.get("width"), "width", 240, 2048)
    h = real(scene.get("height"), "height", 240, 2048)
    horizon = real(scene.get("horizon_y"), "horizon_y", 0, h)
    left = real(scene.get("left_vp_x"), "left_vp_x", -4*w, 5*w)
    right = real(scene.get("right_vp_x"), "right_vp_x", -4*w, 5*w)
    front = point(scene.get("front_bottom"), "front_bottom", w, h)
    tall = real(scene.get("front_height"), "front_height", 1, h)
    tleft = real(scene.get("depth_left"), "depth_left", 0.02, 0.88)
    tright = real(scene.get("depth_right"), "depth_right", 0.02, 0.88)
    if not (left < front[0] < right and horizon < front[1] and front[1] - tall >= 0):
        raise ValueError("vanishing points must bracket the front x; horizon below cube top is optional but front must be below horizon")
    bottom = front
    top = (front[0], front[1] - tall)
    lv, rv = (left, horizon), (right, horizon)
    lt, lb = lerp(top, lv, tleft), lerp(bottom, lv, tleft)
    rt, rb = lerp(top, rv, tright), lerp(bottom, rv, tright)
    def path(*pts):
        return " ".join(vecstr(x) for x in pts)
    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {:.0f} {:.0f}" width="{:.0f}" height="{:.0f}" role="img">'.format(w,h,w,h),
        '<title>Original two-point perspective construction</title>',
        '<rect width="100%" height="100%" fill="#fff9ed"/>',
        '<g id="guides" fill="none" stroke="#adb4b4" stroke-width="1.5" stroke-dasharray="6 5">',
        '<path d="M 0,{0:.3f} L {1:.3f},{0:.3f}"/>'.format(horizon,w),
        '<path d="M {0} L {1} M {2} L {1} M {0} L {3} M {2} L {3}"/>'.format(vecstr(top),vecstr(lv),vecstr(bottom),vecstr(rv)),
        '</g>',
        '<g id="faces" stroke="#24312c" stroke-width="2.5">',
        '<polygon points="{}" fill="#b5c4b5"/>'.format(path(top,lt,lb,bottom)),
        '<polygon points="{}" fill="#e8d5a9"/>'.format(path(top,rt,rb,bottom)),
        '</g>',
        '<path id="front-edge" d="M {} L {}" stroke="#141f1b" stroke-width="4" fill="none"/>'.format(vecstr(top),vecstr(bottom)),
        '<g id="vanishing-points" fill="#8f4637">',
        '<circle cx="{:.3f}" cy="{:.3f}" r="4"/>'.format(*lv),
        '<circle cx="{:.3f}" cy="{:.3f}" r="4"/>'.format(*rv),
        '</g></svg>'
    ]
    return "\n".join(lines)+"\n", {
        "schema": "kosif.perspective.two_point.v1",
        "source_anchor": "Storey 20165, Book I horizon, Book III angular perspective",
        "vanishing_points": {"left": list(lv), "right": list(rv)},
        "vertices": {"front_bottom": list(bottom), "front_top": list(top), "left_bottom": list(lb),
                     "left_top": list(lt), "right_bottom": list(rb), "right_top": list(rt)},
        "status": "GEOMETRIC_CONSTRUCTION_NOT_ARTISTIC_VERIFICATION",
        "notes": ["Edges connecting front to side vertices are exactly collinear with their vanishing point.",
                  "This draws a two-point cube schematic, not a full perspective scene or 3D renderer."]
    }


def rgb_hex(s):
    if not isinstance(s, str) or len(s) != 7 or not s.startswith("#") or any(ch not in "0123456789abcdefABCDEF" for ch in s[1:]):
        raise ValueError("use exactly #RRGGBB")
    return tuple(int(s[i:i+2],16)/255 for i in (1,3,5))


def linear(v):
    return v/12.92 if v <= .04045 else ((v+.055)/1.055)**2.4


def relative_luminance(rgb):
    return sum(c * linear(v) for c,v in zip((.2126,.7152,.0722),rgb))


def palette(spec):
    """HSV-style hue/saturation and WCAG luminance, explicitly NOT Munsell HVC."""
    if type(spec) is not dict or type(spec.get("colors")) is not list:
        raise ValueError("colors must be a list")
    colors = spec["colors"]
    if not 2 <= len(colors) <= 16 or len({c.lower() for c in colors if isinstance(c,str)}) != len(colors):
        raise ValueError("supply 2..16 distinct color strings")
    rows = []
    for c in colors:
        rgb = rgb_hex(c)
        hue,sat,value = colorsys.rgb_to_hsv(*rgb)
        luminance = relative_luminance(rgb)
        rows.append({
            "hex": c.upper(),
            "hue_degrees_hsv": None if sat < 1e-10 else round(360*hue,2),
            "saturation_hsv_0_to_1": round(sat,4),
            "value_hsv_0_to_1": round(value,4),
            "wcag_relative_luminance": round(luminance,6),
            "_luminance": luminance,
        })
    pairs = []
    for i in range(len(rows)):
        for j in range(i+1,len(rows)):
            a,b = rows[i],rows[j]
            la,lb = a["_luminance"], b["_luminance"]
            contrast = (max(la,lb)+.05)/(min(la,lb)+.05)
            pairs.append({"a":a["hex"],"b":b["hex"],"contrast":round(contrast,3),
                          "wcag_normal_text_AA_4_5":contrast >= 4.5,
                          "wcag_large_text_AA_3":contrast >= 3})
    for row in rows:
        del row["_luminance"]
    return {"schema":"kosif.palette.value_contrast.v1",
            "source_anchor":"Munsell 26054: hue, value, chroma as distinct design attributes",
            "calculation_method":"HSV proxy for hue/saturation/value; WCAG relative luminance for contrast, NOT Munsell HVC",
            "colors":rows,"pairs":pairs,
            "status":"MEASURED_COLOR_DIAGNOSTIC_NOT_VISUAL_QUALITY_CERTIFICATE",
            "warnings":["HSV saturation is not Munsell chroma; do not label color matches as native Munsell values.",
                        "AA ratios describe numeric contrast only. Font size, context and color vision need separate review."]}


def write_fresh(p, content):
    path = Path(p)
    if path.exists():
        raise ValueError("output already exists (no overwrite)")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x",encoding="utf-8") as f:
        f.write(content)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command",required=True)
    for name in ("perspective","palette"):
        p=sub.add_parser(name)
        p.add_argument("--input",required=True)
        p.add_argument("--out",required=True)
    args=ap.parse_args(argv)
    try:
        spec=json.loads(Path(args.input).read_text(encoding="utf-8"))
        if args.command=="perspective":
            svg,report=perspective(spec)
            out=Path(args.out)
            if out.suffix.lower()!=".svg":
                raise ValueError("perspective output must end .svg")
            meta=out.with_suffix(".json")
            if out.exists() or meta.exists():
                raise ValueError("refusing to overwrite")
            write_fresh(out,svg)
            write_fresh(meta,json.dumps(report,ensure_ascii=False,indent=2)+"\n")
            result={"svg":str(out),"report":str(meta)}
        else:
            write_fresh(args.out,json.dumps(palette(spec),ensure_ascii=False,indent=2)+"\n")
            result={"report":args.out}
        print(json.dumps({"status":"OUTPUT_CREATED","outputs":result}))
        return 0
    except (ValueError,TypeError,OSError,UnicodeError,json.JSONDecodeError) as exc:
        print("PERSPECTIVE_COLOR_ERROR: "+str(exc),file=sys.stderr)
        return 2


if __name__=="__main__":
    raise SystemExit(main())
