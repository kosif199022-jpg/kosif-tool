#!/usr/bin/env python3
"""Original, executable exercises derived from the *principles* in Lutz, Speed, Dow.

No book pages or illustrations are copied, no remote services are contacted.
Status is execution of specific algorithms, not a claim of training Claude.
"""
import argparse
import html
import json
import math
from pathlib import Path


def finite(v, lo, hi):
    if type(v) not in (int, float) or not math.isfinite(v) or not lo <= v <= hi:
        raise ValueError("invalid coordinate / pixel value")
    return v


def shape_markup(shape, width, height):
    kind = shape.get("kind")
    if kind == "circle":
        x = finite(shape.get("x"), 0, width)
        y = finite(shape.get("y"), 0, height)
        r = finite(shape.get("r"), 0.1, min(width, height))
        return f'<circle cx="{x}" cy="{y}" r="{r}"/>'
    if kind == "rect":
        x = finite(shape.get("x"), 0, width)
        y = finite(shape.get("y"), 0, height)
        w = finite(shape.get("w"), 0.1, width)
        h = finite(shape.get("h"), 0.1, height)
        if x + w > width or y + h > height:
            raise ValueError("rectangle leaves canvas")
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}"/>'
    if kind == "line":
        pts = [finite(shape.get(k), 0, width if k.startswith("x") else height)
               for k in ("x1", "y1", "x2", "y2")]
        return '<line x1="{0}" y1="{1}" x2="{2}" y2="{3}"/>'.format(*pts)
    raise ValueError("shapes must be circle/rect/line")


def staged_svg(spec):
    """Build four original progression frames, with a visible construction layer."""
    w, h = spec.get("width"), spec.get("height")
    finite(w, 100, 2048)
    finite(h, 100, 2048)
    shapes = spec.get("shapes", [])
    if not 1 <= len(shapes) <= 150:
        raise ValueError("requires 1..150 original shapes")
    parts = {"guide": [], "mass": [], "outline": [], "detail": []}
    for shape in shapes:
        stage = shape.get("stage")
        if stage not in parts:
            raise ValueError("shape stage must be guide/mass/outline/detail")
        parts[stage].append(shape_markup(shape, w, h))
    if not parts["outline"] and not parts["mass"]:
        raise ValueError("at least one outline or mass required")
    output = []
    layers = (
        ("guide",),
        ("guide", "mass"),
        ("guide", "mass", "outline"),
        ("mass", "outline", "detail"),
    )
    for step, active in enumerate(layers, 1):
        pieces = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">',
                  '<rect width="100%" height="100%" fill="#fffaf0"/>',
                  f'<title>Original construction study: stage {step}/4</title>']
        for key in active:
            if not parts[key]:
                continue
            style = {
                "guide": 'stroke="#aaa" stroke-dasharray="5 5" stroke-width="1" fill="none"',
                "mass": 'stroke="#666" stroke-width="1.5" fill="#d7d7d7"',
                "outline": 'stroke="#202020" stroke-width="3" fill="none"',
                "detail": 'stroke="#202020" stroke-width="1.5" fill="none"',
            }[key]
            pieces += [f'<g data-layer="{html.escape(key)}" {style}>', *parts[key], "</g>"]
        pieces.append("</svg>")
        output.append("\n".join(pieces) + "\n")
    return output


def quantize_pgm(text, low=85, high=170):
    """PGM-P2 grayscale -> two/three-valued original tone study (no Pillow)."""
    if not 0 < low < high < 255:
        raise ValueError("thresholds must satisfy 0 < low < high < 255")
    toks = []
    for line in text.splitlines():
        toks.extend(line.partition("#")[0].split())
    if len(toks) < 5 or toks[0] != "P2":
        raise ValueError("only ASCII PGM P2 is supported")
    w, h, maxval = map(int, toks[1:4])
    if not (1 <= w <= 4096 and 1 <= h <= 4096 and w * h <= 1_000_000):
        raise ValueError("unsupported image size")
    if maxval != 255:
        raise ValueError("PGM maxval must be 255")
    values = list(map(int, toks[4:]))
    if len(values) != w * h or any(v < 0 or v > 255 for v in values):
        raise ValueError("invalid grayscale pixels")
    tones = [0 if x < low else 127 if x < high else 255 for x in values]
    counts = {str(v): tones.count(v) for v in (0, 127, 255)}
    left = sum(1 for y in range(h) for x in range(w // 2) if tones[y * w + x] == 0)
    right = sum(1 for y in range(h) for x in range((w + 1) // 2, w) if tones[y * w + x] == 0)
    total = left + right
    balance = 1.0 if total == 0 else 1 - abs(left - right) / total
    pgm = "P2\n# Original KOSIF value study\n{} {}\n255\n".format(w, h)
    pgm += "\n".join(" ".join(str(tones[y*w+x]) for x in range(w)) for y in range(h)) + "\n"
    return pgm, {
        "schema": "kosif.drawing.value_study.v1",
        "method_origin": "Harold Speed: line vs mass; Arthur Wesley Dow: notan/value arrangement",
        "source_anchors": [
            "https://www.gutenberg.org/ebooks/14264 (chapters V, IX)",
            "https://www.gutenberg.org/ebooks/45410 (chapters VIII, XII)",
        ],
        "counts": counts,
        "dark_distribution_left": left, "dark_distribution_right": right,
        "dark_balance_index_0_to_1": round(balance, 4),
        "warning": "Quantization and balance are measurable; visual quality is NOT certified.",
    }


def visual_cuts(studies):
    """Compare three-tone distributions of consecutive frames; not a video decoder."""
    if not 2 <= len(studies) <= 1000:
        raise ValueError("2..1000 frame studies required")
    result = []
    prev_time = None
    prev_vec = None
    for item in studies:
        time = finite(item.get("time_seconds"), 0, 86400)
        if prev_time is not None and time <= prev_time:
            raise ValueError("frame times must strictly increase")
        vals = [finite(item.get("tone_ratio", {}).get(str(v)), 0, 1) for v in (0, 127, 255)]
        if abs(sum(vals) - 1) > 0.00001:
            raise ValueError("tone ratios must sum to 1")
        if prev_vec is not None:
            distance = sum(abs(a-b) for a, b in zip(vals, prev_vec)) / 2
            result.append({"at_seconds": time, "tone_distribution_change_0_to_1": round(distance, 5),
                           "flag_large_change": distance >= 0.35})
        prev_vec, prev_time = vals, time
    return {"schema": "kosif.drawing.cut_tone_continuity.v1", "cuts": result,
            "warning": "A high change can be an intentional edit; requires editor judgment and source-video review."}


def safe_write(path, content):
    p = Path(path)
    if p.exists():
        raise ValueError("refusing to overwrite")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    subs = ap.add_subparsers(dest="command", required=True)
    dr = subs.add_parser("construct")
    dr.add_argument("--input", required=True)
    dr.add_argument("--out-prefix", required=True)
    va = subs.add_parser("values")
    va.add_argument("--input", required=True)
    va.add_argument("--out", required=True)
    ca = subs.add_parser("cut-tones")
    ca.add_argument("--input", required=True)
    ca.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    try:
        if args.command == "construct":
            frames = staged_svg(json.loads(Path(args.input).read_text(encoding="utf-8")))
            paths = [Path(f"{args.out_prefix}-{n}.svg") for n in range(1, 5)]
            if any(p.exists() for p in paths):
                raise ValueError("refusing to overwrite staged SVG")
            for p, s in zip(paths, frames):
                safe_write(p, s)
            print(json.dumps({"status": "SVG_STAGES_CREATED", "paths": [str(x) for x in paths]}))
        elif args.command == "values":
            image, report = quantize_pgm(Path(args.input).read_text(encoding="ascii"))
            p = Path(args.out)
            meta = p.with_suffix(".json")
            if p.exists() or meta.exists():
                raise ValueError("refusing to overwrite")
            safe_write(p, image)
            safe_write(meta, json.dumps(report, indent=2))
            print(json.dumps({"status": "TONES_CREATED", "output": str(p), "report": str(meta)}))
        else:
            frames = json.loads(Path(args.input).read_text(encoding="utf-8"))
            report = visual_cuts(frames)
            safe_write(args.out, json.dumps(report, indent=2))
            print(json.dumps({"status": "CUT_TONE_REPORT_CREATED", "output": args.out}))
        return 0
    except (OSError, ValueError, UnicodeError, TypeError, KeyError, json.JSONDecodeError) as e:
        ap.exit(2, "CREATIVE_PRINCIPLE_ERROR: " + str(e) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
