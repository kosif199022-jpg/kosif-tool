"""Does a rendered picture read as painted-realistic, or as a flat cartoon? Measured, not guessed.

    python judge.py out/whale_dragon_1200x800.png [--prompt "…"] [--no-jev]

Letterbox bars and pure black/white backgrounds are left out of the measurements, so a dark studio photo and a
widescreen frame are judged on their subject, not on their empty areas.

Measures (calibrated on the photographs, scenes and flat art that passed through the studio):
  smooth_share     share of subject pixels whose neighbourhood changes gently (informational: grain lowers it)
  flat_share       share of subject pixels (not black/white) that are perfectly flat: cartoon fills
                   photos 0.11-0.23 · shaded scenes < 0.02 · flat cartoon 0.76
  hard_edge_share  among edges, those that jump within one pixel (outline look)
  distinct_colours colours in the subject (/8 bins at 200 px)
  tonal_range      2nd..98th percentile of brightness

Jev is then asked, from the numbers alone, which description fits; Jev judges, it does not see.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))

# calibrated 2026-10-06: photos flat 0.11-0.23 / hard 0.46-0.51; shaded scenes flat < 0.02 / hard 0.18-0.34;
# flat cartoon (PIL house) flat 0.76 / hard 0.64 / 184 colours; flat illustration hard 0.63; logo hard 0.73
THRESH = {"smooth_share": 0.12, "flat_share": 0.30, "hard_edge_share": 0.55, "distinct_colours": 900, "tonal_range": 150}


def measure(path) -> dict:
    im = Image.open(path).convert("RGB")
    a = np.asarray(im)
    g = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY)
    rows = np.flatnonzero(g.max(axis=1) > 8)                          # drop letterbox bars
    if rows.size:
        a, g = a[rows.min():rows.max() + 1], g[rows.min():rows.max() + 1]
    gf = g.astype(np.float32)
    lap = np.abs(cv2.Laplacian(gf, cv2.CV_32F, ksize=3))
    gx = cv2.Sobel(gf, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(gf, cv2.CV_32F, 0, 1, ksize=3)
    mag = np.hypot(gx, gy)
    subject = (g > 12) & (g < 243)                                     # not the empty black or white areas
    n = max(1, int(subject.sum()))
    smooth = float(((lap >= 0.5) & (lap < 14) & subject).sum() / n)
    flat = float(((lap < 0.5) & subject).sum() / n)
    edges = (mag > 60) & subject
    hard = float(((mag > 220) & edges).sum() / max(1, int(edges.sum())))
    small = cv2.resize(a, (200, 200), interpolation=cv2.INTER_AREA)
    sg = cv2.cvtColor(small, cv2.COLOR_RGB2GRAY)
    keep = (sg > 12) & (sg < 243)
    distinct = int(len(np.unique((small[keep] // 8).reshape(-1, 3), axis=0))) if keep.any() else 0
    lo, hi = np.percentile(g, [2, 98])
    hsv = cv2.cvtColor(a, cv2.COLOR_RGB2HSV)
    sat = hsv[..., 1][subject].astype(np.float32) / 255 if subject.any() else np.zeros(1)
    return {"smooth_share": round(smooth, 3), "flat_share": round(flat, 3), "hard_edge_share": round(hard, 3),
            "distinct_colours": distinct, "tonal_range": int(hi - lo), "sat_mean": round(float(sat.mean()), 3),
            "sat_spread": round(float(sat.std()), 3), "subject_share": round(n / g.size, 3), "size": im.size}


def verdict(m: dict) -> tuple[str, list[str]]:
    reasons = []
    if m["smooth_share"] < THRESH["smooth_share"]:
        reasons.append(f"little shading or texture: smooth share {m['smooth_share']:.0%} < {THRESH['smooth_share']:.0%}")
    if m["flat_share"] > THRESH["flat_share"]:
        reasons.append(f"flat fills: {m['flat_share']:.0%} of the subject is perfectly flat (> {THRESH['flat_share']:.0%})")
    if m["hard_edge_share"] > THRESH["hard_edge_share"]:
        reasons.append(f"outline look: {m['hard_edge_share']:.0%} of edges are one-pixel jumps (> {THRESH['hard_edge_share']:.0%})")
    if m["distinct_colours"] < THRESH["distinct_colours"]:
        reasons.append(f"few distinct colours ({m['distinct_colours']} < {THRESH['distinct_colours']})")
    if m["tonal_range"] < THRESH["tonal_range"]:
        reasons.append(f"tonal range {m['tonal_range']} < {THRESH['tonal_range']}: no deep blacks or bright lights")
    return ("PASS" if not reasons else "REVISE"), reasons


def ask_jev(m: dict, prompt: str | None):
    try:
        import jev_client
    except ImportError:
        return None
    state = {"measurements": m, "thresholds": THRESH,
             "calibration": "photographs: flat 0.11-0.23, hard edges 0.46-0.51, colours 1300-2600; "
                            "shaded digital paintings: flat < 0.02, hard edges 0.18-0.34, colours 1100-2000; "
                            "flat cartoons and flat illustrations: flat 0.76 or hard edges > 0.6, colours < 400",
             "prompt_quality_locks": prompt or "photorealistic, cinematic, no cartoon look"}
    return jev_client.choose("From these measurements alone, which description fits the rendered picture best?", state,
                             {"realistic_painting": "painted-realistic: shaded forms, textures, soft atmosphere, wide tonal range",
                              "stylised_illustration": "stylised but shaded illustration: some flat areas, clean edges",
                              "flat_cartoon": "flat cartoon: flat fills, outlines, few colours"})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--prompt")
    ap.add_argument("--no-jev", action="store_true")
    a = ap.parse_args()
    m = measure(a.image)
    v, reasons = verdict(m)
    out = {"image": a.image, "measurements": m, "verdict": v, "reasons": reasons}
    if not a.no_jev:
        out["jev"] = ask_jev(m, a.prompt)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
