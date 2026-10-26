"""End-to-end regression on the synthetic reference: analyse → (texts from truth) → fonts → scorecard.

    python run_synthetic.py REF_DIR WORK_DIR [--build CAND_DIR] [--skip-analyze]

REF_DIR holds ref.mp4 + truth.json from make_reference.py.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from mm_common import load_json, save_json  # noqa: E402


def score_transitions(spec, truth):
    det = spec["transitions"]
    tru = truth["transitions"]
    ok_type = ok_span = 0
    rows = []
    for t in tru:
        d = min(det, key=lambda d: abs((d["ts"] + d["te"]) / 2 - (t["ts"] + t["te"]) / 2)) if det else None
        if d is None:
            rows.append((t["type"], None))
            continue
        same = d["type"] == t["type"] or {d["type"], t["type"]} <= {"fadeblack", "dipblack"}
        span = abs(d["ts"] - t["ts"]) <= 1 and abs(d["te"] - t["te"]) <= 1
        ok_type += same
        ok_span += span
        rows.append((t["type"], d["type"], (t["ts"], t["te"]), (d["ts"], d["te"]), same, span))
    return ok_type, ok_span, len(tru), len(det), rows


def score_texts(spec, truth):
    rows = []
    good_t = good_a = 0
    for e, t in zip(spec["texts"], truth["texts"]):
        tm = e["time"]
        det = [tm["in_start"], tm["full_in"], tm["full_out"], tm["out_end"]]
        err = [abs(a - b) for a, b in zip(det, t["t"])]
        kin = {"fade": "fade", "words": "words", "slideup": "slide_up", "pop": "pop", "blur": "blur"}
        a_ok = e["anim_in"]["type"] == kin.get(t["in"], t["in"]) and e["anim_out"]["type"] == kin.get(t["out"], t["out"])
        good_t += max(err) <= 2
        good_a += a_ok
        font = (e.get("font") or {}).get("chosen") or ""
        rows.append((e["id"], det, t["t"], err, e["anim_in"]["type"], e["anim_out"]["type"], a_ok,
                     Path(font).name, t["font"]))
    return good_t, good_a, len(truth["texts"]), rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ref_dir")
    ap.add_argument("work")
    ap.add_argument("--skip-analyze", action="store_true")
    a = ap.parse_args()
    ref = Path(a.ref_dir) / "ref.mp4"
    truth = json.load(open(Path(a.ref_dir) / "truth.json", encoding="utf-8"))
    import mm_analyze
    import mm_fonts
    t0 = time.time()
    if not a.skip_analyze:
        mm_analyze.analyze(str(ref), a.work)
    t1 = time.time()
    spec = load_json(Path(a.work) / "spec.json")
    for e, t in zip(spec["texts"], truth["texts"]):
        for ln, txt in zip(e["lines"], t["lines"]):
            ln["text"] = txt
    save_json(Path(a.work) / "spec.json", spec)
    mm_fonts.match(a.work)
    t2 = time.time()
    spec = load_json(Path(a.work) / "spec.json")
    ot, osn, nt, nd, rows = score_transitions(spec, truth)
    print(f"\nTRANSITIONS  type {ot}/{nt}  span±1 {osn}/{nt}  (detected {nd})")
    for r in rows:
        print("  ", r)
    gt, ga, ne, rows = score_texts(spec, truth)
    print(f"TEXT EVENTS  timing±2 {gt}/{ne}  animation {ga}/{ne}")
    fonts_ok = 0
    for r in rows:
        print("  ", r)
        fonts_ok += r[7] == r[8]
    print(f"FONTS  {fonts_ok}/{ne}")
    print(f"time: analyse {t1 - t0:.1f}s, fonts {t2 - t1:.1f}s")


if __name__ == "__main__":
    main()
