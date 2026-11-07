#!/usr/bin/env python3
"""Dragon Montage — optional station «المحاكاة» («اعمل زي الفيديو ده»).

  dm_mimic.py mimic --job DIR --reference ref.mp4 [--skip-text] [--sensitivity 1.0]

Wraps kosif-superpowers/scripts/mimic/mm_analyze.py (shot boundaries, transition
kind by re-synthesis, on-screen text, global look) on the owner's reference video
and writes, inside the job folder:

  reference_rhythm.json  "kosif.dm.reference_rhythm.v1": shots, transitions, texts,
                         stats and pacing hints the director uses for shot lengths
  look_override.json     a "kosif.dm.look.v1" look measured from the reference
                         (grade preset, transitions as xfade ids, punch-in camera,
                         caption hint) that the taste station lets override its pick
  mimic/                 the raw mm_analyze work folder (spec.json, frames, sheets)

Reads the reference only; uploads nothing and spends nothing.
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dm_common as C  # noqa: E402

MIMIC = C.SP / "mimic"
SCHEMA = "kosif.dm.reference_rhythm.v1"

# mimic transition kinds → ffmpeg xfade names (CONTRACTS: look.transitions ids)
XFADE = {"cut": "cut", "dipblack": "fadeblack", "dipwhite": "fadewhite", "flash": "fadewhite",
         "blurcross": "hblur", "zoomblur": "zoomin", "zoomblurout": "zoomin", "spin": "fade",
         "whipleft": "slideleft", "whipright": "slideright", "whipup": "slideup", "whipdown": "slidedown",
         "fadefast": "fade", "fadeslow": "fade", "radial": "radial", "distance": "distance"}
XFADE_OK = {"fade", "fadeblack", "fadewhite", "wipeleft", "wiperight", "wipeup", "wipedown", "slideleft",
            "slideright", "slideup", "slidedown", "smoothleft", "smoothright", "smoothup", "smoothdown",
            "circleopen", "circleclose", "dissolve", "pixelize", "hblur", "zoomin", "fadegrays", "radial",
            "distance", "squeezeh", "squeezev", "hlslice", "hrslice", "vuslice", "vdslice", "coverleft",
            "coverright", "coverup", "coverdown", "revealleft", "revealright", "revealup", "revealdown"}


def xfade(kind: str) -> str:
    k = XFADE.get(kind, kind)
    return k if k == "cut" or k in XFADE_OK else "fade"


def run_mm(job: Path, ref: Path, work: Path, skip_text: bool, sensitivity: float) -> dict:
    code = ("import sys; sys.path.insert(0, sys.argv[1]); import mm_analyze; "
            "mm_analyze.analyze(sys.argv[2], sys.argv[3], sensitivity=float(sys.argv[4]), skip_text=sys.argv[5]=='1')")
    C.run(job, "mimic", "mm_analyze", [sys.executable, "-E", "-s", "-B", "-c", code, MIMIC, ref, work,
                                       sensitivity, "1" if skip_text else "0"],
          out=work / "spec.json", owner_media=True, timeout=1800)
    return json.loads((work / "spec.json").read_text(encoding="utf-8"))


def grade_from(spec: dict) -> dict:
    shots = spec.get("shots", [])
    look = spec.get("look", {})
    sat = statistics.fmean([float(s.get("sat") or 0) for s in shots]) if shots else 0.3
    lum = statistics.fmean([float(s.get("lum") or 0) for s in shots]) if shots else 0.5
    lab = [(s.get("lab") or {}).get("mean") for s in shots if isinstance(s.get("lab"), dict)]
    lab = [x for x in lab if isinstance(x, (list, tuple)) and len(x) >= 3]
    warm = statistics.fmean([float(x[2]) for x in lab]) if lab else 0.0  # Lab b*: + yellow, - blue
    vig = float((look.get("vignette") or {}).get("strength") or 0)
    if sat < 0.06:
        gid = "mono"
    elif lum < 0.3 and warm < 0:
        gid = "night-dua"
    elif lum < 0.35 or vig > 0.35:
        gid = "dramatic"
    elif sat > 0.45:
        gid = "vivid"
    elif warm > 12:
        gid = "warm"
    elif warm < -12:
        gid = "cool"
    elif sat < 0.18:
        gid = "faded"
    elif lum > 0.62:
        gid = "bright"
    else:
        gid = "cinematic"
    return {"id": gid, "engine": "look_pipeline", "lut": None,
            "measured": {"saturation": round(sat, 3), "luminance": round(lum, 3), "warmth_b": round(warm, 2),
                         "vignette": round(vig, 3), "grain": (look.get("grain") or {}).get("sigma"),
                         "letterbox": look.get("letterbox"),
                         "fade_in_frames": look.get("fade_in_frames"), "fade_out_frames": look.get("fade_out_frames")}}


def rhythm(spec: dict, ref: Path) -> dict:
    r = spec["reference"]
    dur = float(r.get("duration") or 0)
    shots = [{"n": s["id"], "start": float(s["start_s"]), "end": float(s["end_s"]), "seconds": float(s["dur_s"]),
              "motion": (s.get("motion") or {}).get("speed"), "kenburns": s.get("kenburns"),
              "palette": [p.get("name") for p in s.get("palette", [])[:3]]} for s in spec.get("shots", [])]
    trans = [{"at": float(t.get("ts_s", 0)), "type": t["type"], "xfade": xfade(t["type"]),
              "seconds": round(float(t.get("te_s", 0)) - float(t.get("ts_s", 0)), 3),
              "confidence": t.get("confidence")} for t in spec.get("transitions", [])]
    texts = []
    for e in spec.get("texts", []):
        tm = e.get("time", {})
        texts.append({"start": tm.get("in_start_s"), "end": tm.get("out_end_s"),
                      "text": " / ".join(l.get("ocr", "") for l in e.get("lines", [])),
                      "anim_in": (e.get("anim_in") or {}).get("type"), "anim_out": (e.get("anim_out") or {}).get("type")})
    lens = [s["seconds"] for s in shots if s["seconds"] > 0] or [dur or 1.0]
    mean = statistics.fmean(lens)
    cuts = sum(1 for t in trans if t["xfade"] == "cut")
    mix: dict[str, float] = {}
    for t in trans:
        mix[t["xfade"]] = mix.get(t["xfade"], 0) + 1
    mix = {k: round(v / len(trans), 3) for k, v in mix.items()} if trans else {"cut": 1.0}
    pace = "fast" if mean < 1.5 else "medium" if mean < 3.5 else "slow"
    hints = [f"متوسط طول اللقطة في المرجع {mean:.2f} ث — الإيقاع {'سريع' if pace == 'fast' else 'متوسط' if pace == 'medium' else 'هادي'}",
             f"عدد القطعات في الدقيقة {60 * len(trans) / dur:.1f}" if dur else "المدة غير معروفة",
             f"نسبة القطع المباشر {cuts}/{len(trans)}" if trans else "المرجع لقطة واحدة من غير انتقالات"]
    if texts:
        hints.append(f"فيه {len(texts)} كتابة على الشاشة — خلّي الكابشن ظاهر")
    if any(s["kenburns"] for s in shots):
        hints.append("فيه زووم بطيء ثابت (Ken Burns) على لقطات — استخدم punch-in")
    return {"schema": SCHEMA, "reference": {"path": str(ref), "duration": dur, "w": r.get("w"), "h": r.get("h"),
                                            "fps": r.get("fps"), "has_audio": (r.get("audio") or {}).get("has_audio")},
            "shots": shots, "transitions": trans, "texts": texts,
            "stats": {"shot_count": len(shots), "mean_shot_s": round(mean, 3),
                      "median_shot_s": round(statistics.median(lens), 3), "min_shot_s": round(min(lens), 3),
                      "max_shot_s": round(max(lens), 3),
                      "cuts_per_min": round(60 * len(trans) / dur, 2) if dur else None},
            "pacing": {"pace": pace, "mean_shot_s": round(mean, 3),
                       "shot_lengths_s": [round(x, 3) for x in lens],
                       "shot_pattern": [round(x / mean, 3) for x in lens],
                       "cut_ratio": round(cuts / len(trans), 3) if trans else 1.0,
                       "transition_mix": mix, "hints_ar": hints},
            "source": {"tool": "kosif-superpowers/scripts/mimic/mm_analyze.py", "spec": "mimic/spec.json"}}


def look_override(spec: dict, rh: dict) -> dict:
    trans, seen = [], set()
    for t in rh["transitions"]:
        if t["xfade"] in seen:
            continue
        seen.add(t["xfade"])
        trans.append({"id": t["xfade"]} if t["xfade"] == "cut" else
                     {"id": t["xfade"], "seconds": max(0.1, round(t["seconds"], 3) or 0.25)})
    if not trans:
        trans = [{"id": "cut"}]
    kb = [s["kenburns"]["zoom_per_s"] for s in rh["shots"] if s.get("kenburns")]
    camera = [{"id": "punch-in", "scale": round(min(1.2, max(1.02, kb[0] ** rh["pacing"]["mean_shot_s"])), 3)}] if kb else []
    texts = rh["texts"]
    pace = rh["pacing"]["pace"]
    captions = {"style": ("punchy" if pace == "fast" else "clean") if texts else "none", "font": "Cairo",
                "position": "center" if texts and any(t.get("anim_in") for t in texts) else "lower"}
    bpm = {"fast": [110, 140], "medium": [90, 115], "slow": [60, 90]}[pace]
    return {"schema": C.SCHEMAS["look"], "style_id": "mimic-reference", "style_source": "mimic",
            "grade": grade_from(spec), "transitions": trans, "camera": camera, "captions": captions,
            "music": {"mood": None, "bpm_range": bpm},
            "why": f"مقاس من الفيديو المرجعي: {rh['stats']['shot_count']} لقطة، متوسط {rh['stats']['mean_shot_s']} ث، "
                   f"انتقالات {', '.join(t['id'] for t in trans)}"}


def cmd_mimic(a) -> int:
    job = C.job_dir(a.job)
    ref = Path(a.reference).resolve()
    if not ref.is_file():
        raise SystemExit(f"reference {ref} not found")
    spec = run_mm(job, ref, job / "mimic", a.skip_text, a.sensitivity)
    rh = rhythm(spec, ref)
    lk = look_override(spec, rh)
    C.validate("look", lk)
    (job / "reference_rhythm.json").write_text(json.dumps(rh, ensure_ascii=False, indent=2), encoding="utf-8")
    (job / "look_override.json").write_text(json.dumps(lk, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"job": str(job), "shots": rh["stats"]["shot_count"], "mean_shot_s": rh["stats"]["mean_shot_s"],
                      "grade": lk["grade"]["id"], "transitions": [t["id"] for t in lk["transitions"]]},
                     ensure_ascii=False))
    return 0


def main(argv=None) -> int:
    C.utf8_stdio()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("mimic", help="measure a reference video's rhythm and look")
    m.add_argument("--job", required=True)
    m.add_argument("--reference", required=True)
    m.add_argument("--skip-text", action="store_true", help="skip on-screen text detection (faster)")
    m.add_argument("--sensitivity", type=float, default=1.0)
    a = p.parse_args(argv)
    return cmd_mimic(a)


if __name__ == "__main__":
    sys.exit(main())
