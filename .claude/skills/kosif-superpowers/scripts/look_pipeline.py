#!/usr/bin/env python3
"""KOSIF Look Pipeline — معادلة ألوان واحدة تعطي المعاينة والتصدير النتيجة نفسها (فكرة من دراسة «مونتاجي»، كود أصلي).

Idea learnt from a read-only study of the Montaji 1.0.0 macOS editor: a colour look is written ONCE as numbers
(a per-channel affine step, then a 3x3 colour matrix) and the same numbers drive every renderer, so the browser
preview never disagrees with the exported MP4. Montaji feeds them to ffmpeg, an SVG filter and a WebGL shader;
this tool does the same with KOSIF's own parameters, presets and constants, and adds a measured parity check.
No Montaji code is used.

  python3 look_pipeline.py presets [--json]
  python3 look_pipeline.py build [--preset cinematic] [--amount 0.8] [--set contrast=0.1 --set vignette=0.4]
                                 --target ffmpeg|svg|css|glsl|json
  python3 look_pipeline.py verify [--preset NAME | --all] [--tolerance 3]      # ffmpeg output vs this file's maths
  python3 look_pipeline.py apply IN.mp4 OUT.mp4 --preset warm [--amount 0.6]  # new file only, never overwrites

Parameters (0 = untouched): brightness, contrast, saturation, temperature in -1..1; fade, sepia, teal, vignette in
0..1. Vignette is spatial, so it is emitted for each target but left out of the per-pixel parity check.
Python 3.8+ standard library; ffmpeg only for verify and apply.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

KEYS = ["brightness", "contrast", "saturation", "temperature", "fade", "sepia", "teal", "vignette"]
UNIT = {"fade", "sepia", "teal", "vignette"}          # 0..1; the others are -1..1
LUMA = (0.2126, 0.7152, 0.0722)                        # Rec. 709
ID3 = ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
SEPIA = ((0.393, 0.769, 0.189), (0.349, 0.686, 0.168), (0.272, 0.534, 0.131))   # W3C Filter Effects sepia()
TEAL = ((1.07, -0.03, -0.04), (-0.02, 1.03, -0.01), (-0.09, 0.03, 1.06))        # KOSIF cool-shadow split

PRESETS = {
    "natural":   ("الأصلي", "untouched", {}),
    "vivid":     ("حيوي", "punchy colour", {"saturation": 0.32, "contrast": 0.1}),
    "bright":    ("مشرق", "airy daylight", {"brightness": 0.15, "saturation": 0.1, "contrast": 0.05}),
    "warm":      ("دافئ", "golden hour", {"temperature": 0.45, "saturation": 0.06}),
    "cool":      ("بارد", "clean blue", {"temperature": -0.45, "saturation": 0.04}),
    "cinematic": ("سينمائي", "teal shadows, firm contrast", {"teal": 0.75, "contrast": 0.14, "saturation": -0.08, "vignette": 0.3}),
    "vintage":   ("كلاسيكي", "warm print, lifted blacks", {"sepia": 0.5, "fade": 0.35, "contrast": -0.05}),
    "faded":     ("باهت", "matte, low colour", {"fade": 0.65, "saturation": -0.22, "contrast": -0.06}),
    "dramatic":  ("درامي", "hard contrast, muted colour", {"contrast": 0.32, "saturation": -0.32, "brightness": -0.05, "vignette": 0.45}),
    "mono":      ("أبيض وأسود", "black and white", {"saturation": -1.0, "contrast": 0.16}),
    "night-dua": ("ليلي هادئ", "dim, cool and soft (dua and night reels)", {"brightness": -0.08, "temperature": -0.3, "saturation": -0.18, "fade": 0.2, "vignette": 0.5}),
}

clamp = lambda v, a, b: max(a, min(b, v))  # noqa: E731


def params_for(preset="natural", amount=1.0, overrides=None) -> dict:
    if preset not in PRESETS:
        raise SystemExit(f"look_pipeline: unknown preset {preset!r} (see: presets)")
    base = PRESETS[preset][2]
    p = {k: base.get(k, 0.0) * amount for k in KEYS}
    for k, v in (overrides or {}).items():
        if k not in KEYS:
            raise SystemExit(f"look_pipeline: unknown parameter {k!r}; use one of {', '.join(KEYS)}")
        p[k] = float(v)
    return {k: clamp(v, 0.0 if k in UNIT else -1.0, 1.0) for k, v in p.items()}


def _mul(A, B):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)) for i in range(3))


def _mix(A, B, t):
    return tuple(tuple(A[i][j] + (B[i][j] - A[i][j]) * t for j in range(3)) for i in range(3))


def pipeline(p: dict) -> dict:
    """Parameters → {slope[3], intercept[3] (0..1 units), matrix 3x3, vignette}. The single source of truth."""
    gain = 1 + 0.4 * p["brightness"]
    t = p["temperature"]
    slope = [gain * (1 + 0.12 * t), gain * (1 + 0.02 * t), gain * (1 - 0.12 * t)]
    icpt = [0.0, 0.0, 0.0]
    k = 1 + p["contrast"]                                     # pivot at mid grey
    slope = [s * k for s in slope]
    icpt = [i * k + 0.5 * (1 - k) for i in icpt]
    f = p["fade"]                                             # lift blacks, pull whites
    slope = [s * (1 - 0.2 * f) for s in slope]
    icpt = [i * (1 - 0.2 * f) + 0.08 * f for i in icpt]
    s = max(0.0, 1 + p["saturation"])
    M = tuple(tuple(s * ID3[i][j] + (1 - s) * LUMA[j] for j in range(3)) for i in range(3))
    if p["sepia"] > 0:
        M = _mul(_mix(ID3, SEPIA, p["sepia"]), M)
    if p["teal"] > 0:
        M = _mul(_mix(ID3, TEAL, p["teal"]), M)
    r = lambda v: round(v, 6)  # noqa: E731
    return {"slope": [r(x) for x in slope], "intercept": [r(x) for x in icpt],
            "matrix": [[r(x) for x in row] for row in M], "vignette": r(p["vignette"])}


def _is_identity(c):
    affine = all(abs(s - 1) < 1e-6 for s in c["slope"]) and all(abs(i) < 1e-6 for i in c["intercept"])
    matrix = all(abs(c["matrix"][i][j] - ID3[i][j]) < 1e-6 for i in range(3) for j in range(3))
    return affine, matrix


# ---------------------------------------------------------------- renderers

def to_ffmpeg(c, spatial=True) -> str:
    affine_id, matrix_id = _is_identity(c)
    out = ["format=rgb24"]
    if not affine_id:
        ch = [f"{n}='clip(val*{c['slope'][i]}+{c['intercept'][i]}*255,0,255)'" for i, n in enumerate("rgb")]
        out.append("lutrgb=" + ":".join(ch))
    if not matrix_id:
        out.append("colorchannelmixer=" + ":".join(f"{a}{b}={c['matrix'][i][j]}"
                                                     for i, a in enumerate("rgb") for j, b in enumerate("rgb")))
    if spatial and c["vignette"] > 0:
        out.append(f"vignette=angle={round(c['vignette'] * 1.1, 4)}")
    return ",".join(out)


def to_svg(c, fid="kosif-look") -> str:
    tr = "".join(f'<feFunc{n} type="linear" slope="{c["slope"][i]}" intercept="{c["intercept"][i]}"/>' for i, n in enumerate("RGB"))
    m = c["matrix"]
    vals = " ".join(f"{m[i][0]} {m[i][1]} {m[i][2]} 0 0" for i in range(3)) + " 0 0 0 1 0"
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" style="position:absolute">'
           f'<filter id="{fid}" color-interpolation-filters="sRGB">'
           f'<feComponentTransfer>{tr}</feComponentTransfer><feColorMatrix type="matrix" values="{vals}"/></filter></svg>')
    if c["vignette"] > 0:
        svg += (f'\n<!-- vignette: overlay a radial-gradient(transparent 55%, rgba(0,0,0,{round(0.75 * c["vignette"], 3)})) '
                f'above the filtered element -->')
    return svg


def to_css(c, fid="kosif-look") -> str:
    return f"/* put the SVG from --target svg in the page once */\n.kosif-look {{ filter: url(#{fid}); }}"


def to_glsl(c) -> str:
    m = c["matrix"]
    col = lambda j: ", ".join(f"{m[i][j]:.6f}" for i in range(3))  # noqa: E731 — GLSL mat3 takes columns
    v = c["vignette"]
    return f"""precision mediump float;
varying vec2 uv;
uniform sampler2D tex;
const vec3 SLOPE = vec3({', '.join(f'{x:.6f}' for x in c['slope'])});
const vec3 ICPT = vec3({', '.join(f'{x:.6f}' for x in c['intercept'])});
const mat3 M = mat3({col(0)}, {col(1)}, {col(2)});
const float VIGNETTE = {v:.4f};
void main() {{
  vec4 src = texture2D(tex, uv);
  vec3 c = clamp(M * clamp(src.rgb * SLOPE + ICPT, 0.0, 1.0), 0.0, 1.0);
  float d = distance(uv, vec2(0.5));
  c *= 1.0 - VIGNETTE * 0.75 * smoothstep(0.35, 0.75, d);
  gl_FragColor = vec4(c, src.a);
}}
"""


def apply_pixel(c, rgb):
    """Reference maths on one 8-bit pixel, in the same order and with the same clipping as the ffmpeg chain."""
    a = [clamp(int(v * c["slope"][i] + c["intercept"][i] * 255), 0, 255) for i, v in enumerate(rgb)]
    return [clamp(int(round(sum(c["matrix"][i][j] * a[j] for j in range(3)))), 0, 255) for i in range(3)]


# ---------------------------------------------------------------- ffmpeg-backed commands

def _need_ffmpeg():
    if not shutil.which("ffmpeg"):
        raise SystemExit("look_pipeline: ffmpeg is not installed (needed for verify/apply)")


def _raw(vf, w=64, h=36):
    cmd = ["ffmpeg", "-v", "error", "-f", "lavfi", "-i", f"testsrc2=size={w}x{h}:rate=1", "-frames:v", "1"]
    if vf:
        cmd += ["-vf", vf]
    cmd += ["-pix_fmt", "rgb24", "-f", "rawvideo", "-"]
    return subprocess.run(cmd, check=True, capture_output=True).stdout


def verify(name, amount=1.0, tolerance=3) -> dict:
    c = pipeline(params_for(name, amount))
    src = _raw("format=rgb24")
    got = _raw(to_ffmpeg(c, spatial=False))
    worst, total = 0, 0
    for o in range(0, len(src), 3):
        exp = apply_pixel(c, src[o:o + 3])
        d = max(abs(exp[i] - got[o + i]) for i in range(3))
        worst = max(worst, d)
        total += d
    n = len(src) // 3
    return {"preset": name, "amount": amount, "pixels": n, "max_abs_error": worst,
            "mean_abs_error": round(total / n, 3), "tolerance": tolerance, "ok": worst <= tolerance}


def _overrides(pairs):
    out = {}
    for s in pairs or []:
        k, _, v = s.partition("=")
        out[k.strip()] = float(v)
    return out


def cmd_presets(a):
    if a.json:
        print(json.dumps({k: {"name_ar": ar, "name_en": en, "params": p} for k, (ar, en, p) in PRESETS.items()},
                         ensure_ascii=False, indent=1))
        return 0
    for k, (ar, en, p) in PRESETS.items():
        print(f"{k:10} {ar:12} {en:42} " + ", ".join(f"{x}={v:+g}" for x, v in p.items()))
    return 0


def cmd_build(a):
    p = params_for(a.preset, a.amount, _overrides(a.set))
    c = pipeline(p)
    if a.target == "json":
        print(json.dumps({"schema": "kosif.look.v1", "preset": a.preset, "amount": a.amount, "params": p,
                          "pipeline": c, "ffmpeg": to_ffmpeg(c)}, ensure_ascii=False, indent=1))
    else:
        print({"ffmpeg": to_ffmpeg, "svg": to_svg, "css": to_css, "glsl": to_glsl}[a.target](c))
    return 0


def cmd_verify(a):
    _need_ffmpeg()
    names = list(PRESETS) if a.all else [a.preset]
    rows = [verify(n, a.amount, a.tolerance) for n in names]
    for r in rows:
        print(f"{'PASS' if r['ok'] else 'FAIL'} {r['preset']:10} max |Δ| {r['max_abs_error']} · mean {r['mean_abs_error']} over {r['pixels']} px")
    return 0 if all(r["ok"] for r in rows) else 1


def cmd_apply(a):
    _need_ffmpeg()
    src, out = Path(a.input), Path(a.output)
    if not src.is_file():
        raise SystemExit(f"look_pipeline: {src} not found")
    if out.exists() or out.resolve() == src.resolve():
        raise SystemExit(f"look_pipeline: {out} exists; choose a new output name")
    c = pipeline(params_for(a.preset, a.amount, _overrides(a.set)))
    vf = to_ffmpeg(c) + ",format=yuv420p"
    subprocess.run(["ffmpeg", "-v", "error", "-n", "-i", str(src), "-vf", vf, "-c:v", "libx264", "-crf", "17",
                    "-preset", "slow", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", str(out)], check=True)
    print(f"{src.name} → {out} ({a.preset} × {a.amount})")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="One colour look, identical in ffmpeg, SVG/CSS and GLSL, with a parity check.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("presets", help="list the looks")
    s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_presets)

    def look_args(q):
        q.add_argument("--preset", default="natural", choices=list(PRESETS))
        q.add_argument("--amount", type=float, default=1.0, help="0..1 strength of the preset")
        q.add_argument("--set", action="append", metavar="KEY=VALUE", help=f"override one of: {', '.join(KEYS)}")

    b = sub.add_parser("build", help="emit the look for one renderer")
    look_args(b)
    b.add_argument("--target", required=True, choices=["ffmpeg", "svg", "css", "glsl", "json"])
    b.set_defaults(fn=cmd_build)
    v = sub.add_parser("verify", help="ffmpeg output vs the reference maths on a test frame")
    v.add_argument("--preset", default="cinematic", choices=list(PRESETS))
    v.add_argument("--all", action="store_true")
    v.add_argument("--amount", type=float, default=1.0)
    v.add_argument("--tolerance", type=int, default=3, help="largest allowed 8-bit difference")
    v.set_defaults(fn=cmd_verify)
    p = sub.add_parser("apply", help="grade a video into a NEW file")
    p.add_argument("input")
    p.add_argument("output")
    look_args(p)
    p.set_defaults(fn=cmd_apply)
    a = ap.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
