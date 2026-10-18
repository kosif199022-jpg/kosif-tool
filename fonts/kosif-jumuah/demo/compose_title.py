#!/usr/bin/env python3
"""Compose the «الجمعة» title as original SVG lettering from Amiri Bold outlines — تركيب عنوان «الجمعة».

The reference title is a Thuluth composition: two tall verticals for «ال», then «جمعة» spread wide and
cascading down to the left under its vowel marks. No open-licensed Thuluth face exists, so this script
builds that structure from the OFL Amiri Bold glyphs: alef and lam are stretched vertically, kashida
strokes widen the word, the connected «لجمعة» group is sheared so its baseline descends to the left while
stems stay vertical, individual letters can be scaled about their joins, and the marks are placed by hand.
The output is one <path> per glyph (same fill) so the demo can draw the title on stroke by stroke.

  python3 compose_title.py [--font Amiri-Bold.ttf] [--out title-aljumuah.svg] [--set key=value ...] [--json]

Tunable values live in PARAMS (font units, 1000/em, y up, right-to-left pen). Source glyphs
© The Amiri Project Authors, SIL Open Font License 1.1; the composition is KOSIF's own.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.ttLib import TTFont
except ImportError:  # pragma: no cover
    sys.exit("fontTools is required: pip install fonttools")

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
DEFAULT_FONT = REPO / ".kosif-cache" / "fonts-src" / "amiri" / "Amiri-Bold.ttf"

# shaped glyphs via presentation forms: alef isolated, lam initial, jeem medial, meem medial, ain medial, taa-marbuta final
LETTERS = {"alef": 0xFE8D, "lam": 0xFEDF, "jeem": 0xFEA0, "meem": 0xFEE4, "ain": 0xFECC, "taa": 0xFE94, "kashida": 0x0640}
MARKS = {"damma": 0x064F, "fatha": 0x064E}
ORDER = ["alef", "lam", "jeem", "meem", "ain", "taa"]

PARAMS = {
    "alef_sy": 1.6, "lam_sy": 1.6,     # vertical stretch of the two stems (about the baseline)
    "lam_gap": 60,                      # extra space between alef and lam
    "shear": 0.18,                      # tan of the cascade angle for «لجمعة»: the baseline drops to the left, stems stay vertical
    "kashida_meem": 1, "kashida_ain": 1,  # tatweel strokes inserted after these letters to widen the word
    "kashida_sx": 1.0,                  # horizontal scale of each tatweel
    "jeem_s": 1.3, "meem_s": 1.0, "ain_s": 1.05, "taa_s": 1.1,  # per-letter scale about the right join
    "cascade_dy": 0,
    "mark_scale": 0.95,
    "marks": [("damma", "jeem", 40, 110), ("damma", "meem", 30, 150), ("fatha", "ain", 0, 140)],
}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--font", default=str(DEFAULT_FONT))
    ap.add_argument("--out", default=str(HERE / "title-aljumuah.svg"))
    ap.add_argument("--json", action="store_true", help="print the viewBox and glyph boxes as JSON")
    ap.add_argument("--set", action="append", default=[], help="override a PARAMS value, e.g. --set shear=0.2")
    a = ap.parse_args(argv)
    for kv in a.set:
        k, v = kv.split("=", 1)
        PARAMS[k] = float(v)
    font = TTFont(a.font)
    cmap, gs, hmtx = font.getBestCmap(), font.getGlyphSet(), font["hmtx"]
    adv_of = lambda key: hmtx[cmap[LETTERS[key]]][0]

    # 1. sequence with kashidas, laid right-to-left on a flat baseline; each item: (key, glyph key, scale)
    seq = []
    for key in ORDER:
        s = PARAMS.get(f"{key}_s", 1.0)
        seq.append((key, key, s))
        for _ in range(int(PARAMS.get(f"kashida_{key}", 0))):
            seq.append((f"kashida-{key}-{len(seq)}", "kashida", PARAMS["kashida_sx"]))
    x = 0.0
    placed = []  # (id, glyph key, left x, scale)
    for ident, gkey, s in seq:
        sx = s
        sy = s if gkey != "kashida" else 1.0
        x -= adv_of(gkey) * sx
        placed.append((ident, gkey, x, sx, sy))
        if gkey == "alef":
            x -= PARAMS["lam_gap"]
    anchor_x = next(p[2] for p in placed if p[0] == "lam") + adv_of("lam")  # lam's right edge: the cascade pivot
    k = PARAMS["shear"]

    # 2. outlines with transforms; TransformPen(TransformPen(pen, outer), inner): inner first, then outer
    paths, boxes = [], {}
    for ident, gkey, gx, sx, sy in placed:
        if gkey == "alef":
            inner = (1, 0, 0, PARAMS["alef_sy"], gx, 0); outer = (1, 0, 0, 1, 0, 0)
        else:
            if gkey == "lam":
                inner = (1, 0, 0, PARAMS["lam_sy"], gx, 0)
            else:
                inner = (sx, 0, 0, sy, gx, PARAMS["cascade_dy"])
            outer = (1, k, 0, 1, 0, -k * anchor_x)  # y' = y + k*(x - anchor): descends to the left
        name = cmap[LETTERS[gkey]]
        pen = SVGPathPen(gs); gs[name].draw(TransformPen(TransformPen(pen, outer), inner))
        bp = BoundsPen(gs); gs[name].draw(TransformPen(TransformPen(bp, outer), inner))
        paths.append((ident, pen.getCommands()))
        if bp.bounds:
            boxes[ident] = list(bp.bounds)

    # 3. vowel marks above letters
    for mark, over, mdx, mdy in PARAMS["marks"]:
        if over not in boxes:
            continue
        b = boxes[over]
        cx, top, s = (b[0] + b[2]) / 2 + mdx, b[3] + mdy, PARAMS["mark_scale"]
        name = cmap[MARKS[mark]]
        bp = BoundsPen(gs); gs[name].draw(bp); mb = bp.bounds or (0, 0, 0, 0)
        t = (s, 0, 0, s, cx - (mb[0] + mb[2]) / 2 * s, top - mb[1] * s)
        pen = SVGPathPen(gs); gs[name].draw(TransformPen(pen, t))
        ident = f"{mark}-{over}"
        paths.append((ident, pen.getCommands()))
        boxes[ident] = [t[4] + mb[0] * s, t[5] + mb[1] * s, t[4] + mb[2] * s, t[5] + mb[3] * s]

    # 4. SVG (y flipped), viewBox from the union of boxes
    xs0, xs1 = min(b[0] for b in boxes.values()), max(b[2] for b in boxes.values())
    ys0, ys1 = min(b[1] for b in boxes.values()), max(b[3] for b in boxes.values())
    pad = 40
    w, h = xs1 - xs0 + 2 * pad, ys1 - ys0 + 2 * pad
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" role="img" aria-label="الجمعة">',
             f'<!-- KOSIF composition of الجمعة from Amiri Bold glyphs (SIL OFL 1.1, © The Amiri Project Authors); params {json.dumps({k: v for k, v in PARAMS.items() if k != "marks"})} -->',
             f'<g id="lettering" transform="translate({-xs0 + pad:.1f},{ys1 + pad:.1f}) scale(1,-1)" fill="currentColor">']
    parts += [f'<path id="g-{ident}" d="{d}"/>' for ident, d in paths]
    parts += ["</g>", "</svg>"]
    Path(a.out).write_text("\n".join(parts) + "\n", encoding="utf-8")
    if a.json:
        print(json.dumps({"viewBox": [round(w), round(h)], "aspect": round(w / h, 2), "boxes": {k: [round(v) for v in b] for k, b in boxes.items()}}, indent=1))
    print(f"wrote {a.out} ({w:.0f}×{h:.0f} units, aspect {w / h:.2f}, {len(paths)} paths)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
