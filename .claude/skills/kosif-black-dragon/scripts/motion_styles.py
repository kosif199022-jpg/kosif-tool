#!/usr/bin/env python3
"""Black Dragon code-motion style studio: style briefs, voiceover timing, mix checks.

Native and deterministic. It reads `data/motion_styles.json` (7 style cards and
16 working principles studied from a public motion-graphics style library and
rewritten in our own words). It never renders video, calls a model or fetches
anything. `vo-timeline` and `cue-check` are real computations on files you give.

Commands (run from the repository root):
  motion_styles.py list
  motion_styles.py match "شرح برنامج خطوة بخطوة"
  motion_styles.py brief data-story --topic "نمو المبيعات" --storyboard
  motion_styles.py clone-plan --topic "عادات النوم"
  motion_styles.py vo-timeline --srt voice.srt
  motion_styles.py cue-check --cues cues.json [--speech words.json]
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "motion_styles.json"
TAIL_SECONDS = 1.2
SMALL_SOUNDS = {"pop", "tick", "marker", "keys", "click"}
_TIME = re.compile(r"(\d+):(\d{2}):(\d{2})[,.](\d{1,3})")


def _studio():
    spec = importlib.util.spec_from_file_location("_kosif_build_studio_nlp", Path(__file__).with_name("build_studio.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load(path: Path = DATA) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    ids = [s["id"] for s in data["styles"]]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate style id")
    return data


def match(task: str, data: dict, limit: int = 3) -> list[dict]:
    nlp = _studio()
    task_norm, task_toks = nlp.normalize(task), nlp.tokens(task)
    ranked = []
    for s in data["styles"]:
        hits = [k for k in s["keywords"] if nlp._keyword_hits(task_norm, task_toks, k)]
        if hits:
            ranked.append({"id": s["id"], "title_ar": s["title_ar"], "family": s["family"],
                           "score": len(hits), "matched_keywords": hits})
    ranked.sort(key=lambda x: (-x["score"], x["id"]))
    return ranked[:limit]


def _style(ref: str, data: dict) -> dict:
    by_id = {s["id"]: s for s in data["styles"]}
    if ref in by_id:
        return by_id[ref]
    found = match(ref, data)
    if not found:
        raise ValueError("no style matched; run `list` and pass a style id")
    return by_id[found[0]["id"]]


def brief(ref: str, data: dict, topic: str = "", timeline: dict | None = None, storyboard: bool = True) -> dict:
    s = _style(ref, data)
    p = {x["id"]: x["ar"] for x in data["principles"]}
    use = ["M01", "M02", "M03", "M04", "M08", "M09", "M10", "M11", "M12", "M13", "M15"]
    use += ["M05"] if storyboard else []
    use += ["M06", "M07"] if timeline else ["M07"]
    questions = []
    if not topic.strip():
        questions.append("الموضوع أو النص؟ (لن نبدأ البناء بدونه)")
    stages = (["ستوري بورد 6–10 لوحات بنفس كود الأسلوب + سجل الافتراضات ← انتظار الموافقة"] if storyboard else []) + [
        "بناء ملف HTML واحد: المحرك ثابت والقصة جديدة حول الموضوع",
        "فحص: وضوح على الموبايل، ميزانية الإطار، تزامن الصوت مع الجدول",
        "رندر حتمي إطار بإطار + صوت أوفلاين ودمجهم",
    ]
    return {
        "status": "STYLE_BRIEF_NOT_A_RENDER",
        "style": s["id"], "title_ar": s["title_ar"], "family": s["family"],
        "topic": topic.strip() or None, "open_questions": questions,
        "look_ar": s["look_ar"], "explains_ar": s["explains_ar"],
        "type_roles_ar": s["type_roles_ar"], "sound_map_ar": s["sound_map_ar"],
        "duration_seconds": timeline["duration"] if timeline else "15–40",
        "voiceover_words": len(timeline["words"]) if timeline else 0,
        "stages": stages,
        "principles": [{"id": i, "ar": p[i]} for i in use],
        "renderer_hint": "kosif-web-film (tools/render_html.cjs) هو المنفذ في الريبو؛ هذا الموجز لا يرندر.",
    }


def clone_plan(data: dict, topic: str = "") -> dict:
    p = {x["id"]: x["ar"] for x in data["principles"]}
    return {
        "status": "CLONE_PLAN_NOT_A_RENDER", "topic": topic.strip() or None,
        "steps": [
            {"n": 1, "ar": "اقرأ المحرك المرجعي واشرحه في نقاط: الإطار دالة في t، البذرة، الجدول الواحد للصورة والصوت، طبقات التشطيب، وما يكشفه المشغّل."},
            {"n": 2, "ar": "بطاقة أسلوب من اللقطة: 4–7 ألوان بأدوارها، السطح، أقرب خطوط مجانية بأوزانها، الأشكال والمسافات، طريقة التمييز، الحركة المستنتجة وسببها، الأصوات المناسبة؛ مع فصل المرئي عن المستنتج."},
            {"n": 3, "ar": "إثبات قبل البناء: إطار ثابت + عيّنة متكررة 5–8ث بالصوت، ثم أكبر 3 فروق عن اللقطة وتصليحها وانتظار الموافقة."},
            {"n": 4, "ar": "البناء الكامل 15–40ث حول الموضوع مع ثبات المحرك، ثم رندر MP4 لو التشغيل متاح."},
            {"n": 5, "ar": "اكتب برومت أسلوب قابل لإعادة الاستخدام (بطاقة + قواعد + صوت + ما يُستبدل وما يُحتفظ به)."},
        ],
        "guardrail_ar": p["M14"] + " " + p["M13"],
    }


def _sec(stamp: str) -> float:
    m = _TIME.search(stamp)
    if not m:
        raise ValueError(f"bad SRT time: {stamp!r}")
    h, mi, s, ms = m.groups()
    return int(h) * 3600 + int(mi) * 60 + int(s) + int(ms.ljust(3, "0")) / 1000


def parse_srt(text: str) -> list[dict]:
    lines = []
    for block in re.split(r"\n\s*\n", text.replace("\r\n", "\n").strip()):
        rows = [r for r in block.split("\n") if r.strip()]
        idx = next((i for i, r in enumerate(rows) if "-->" in r), None)
        if idx is None:
            continue
        a, b = rows[idx].split("-->")
        start, end = _sec(a), _sec(b)
        if end <= start:
            raise ValueError(f"SRT cue ends before it starts at {start:.3f}s")
        words = " ".join(rows[idx + 1:]).split()
        if words:
            lines.append({"start": start, "end": end, "words": words})
    if not lines:
        raise ValueError("no SRT cues found")
    return lines


def vo_timeline(lines: list[dict]) -> dict:
    """Spread each line's words over its span by word length (M06)."""
    words = []
    for ln in lines:
        span = ln["end"] - ln["start"]
        weights = [max(len(w), 1) for w in ln["words"]]
        total, t = sum(weights), ln["start"]
        for w, k in zip(ln["words"], weights):
            dur = span * k / total
            words.append({"w": w, "start": round(t, 3), "end": round(t + dur, 3)})
            t += dur
    word_level = all(len(ln["words"]) == 1 for ln in lines)
    return {"status": "WORD_TIMELINE_COMPUTED", "source_granularity": "word" if word_level else "line-spread-by-length",
            "words": words, "duration": round(words[-1]["end"] + TAIL_SECONDS, 3),
            "idea_boundaries": [round(ln["start"], 3) for ln in lines]}


def cue_check(cues: list[dict], speech: list[dict] | None = None, window: float = 0.15) -> dict:
    """Check a sound score against the mix rules (M07). Lexical names, no audio analysis."""
    cues = sorted(cues, key=lambda c: float(c["t"]))
    issues = []
    vo = bool(speech)
    times = [float(c["t"]) for c in cues]
    if not vo:
        for i, t in enumerate(times):
            n = sum(1 for u in times[i:] if u - t <= window)
            if n > 3:
                issues.append({"rule": "max_3_simultaneous", "at": t, "count": n})
                break
    ticks = [float(c["t"]) for c in cues if c["name"] == "tick"]
    for i, t in enumerate(ticks):
        n = sum(1 for u in ticks[i:] if u - t < 1.0)
        if n > 12:
            issues.append({"rule": "ticks_max_12_per_second", "at": t, "count": n})
            break
    booms = [c for c in cues if c["name"] == "boom"]
    if len(booms) > 3:
        issues.append({"rule": "booms_for_2_or_3_moments", "count": len(booms)})
    if booms and not vo:
        def quiet_before(b):
            bt = float(b["t"])
            return not any(bt - 0.3 <= float(c["t"]) < bt and c is not b and not c.get("soft") for c in cues)
        if not any(quiet_before(b) for b in booms):
            issues.append({"rule": "near_silence_before_biggest_hit", "at": float(booms[-1]["t"])})
    if vo:
        loud_small = [float(c["t"]) for c in cues if c["name"] in SMALL_SOUNDS and not c.get("soft")]
        if loud_small:
            issues.append({"rule": "small_sounds_soft_under_voiceover", "at": loud_small[:5], "count": len(loud_small)})
        for c in cues:
            if c["name"] in {"riser", "drone"}:
                a, b = float(c["t"]), float(c["t"]) + float(c.get("dur", 1.0))
                if any(w["start"] < b and w["end"] > a for w in speech):
                    issues.append({"rule": f"no_{c['name']}_under_speech", "at": a})
    return {"status": "MIX_RULES_CHECKED_ON_CUE_LIST_NOT_AUDIO", "cue_count": len(cues),
            "voiceover": vo, "passed": not issues, "issues": issues}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Black Dragon code-motion style studio (no rendering)")
    ap.add_argument("--data", type=Path, default=DATA)
    sub = ap.add_subparsers(dest="action", required=True)
    sub.add_parser("list")
    sub.add_parser("principles")
    m = sub.add_parser("match")
    m.add_argument("task")
    b = sub.add_parser("brief")
    b.add_argument("ref")
    b.add_argument("--topic", default="")
    b.add_argument("--srt", type=Path)
    b.add_argument("--direct", action="store_true", help="skip the storyboard gate")
    c = sub.add_parser("clone-plan")
    c.add_argument("--topic", default="")
    v = sub.add_parser("vo-timeline")
    v.add_argument("--srt", type=Path, required=True)
    v.add_argument("--out", type=Path)
    q = sub.add_parser("cue-check")
    q.add_argument("--cues", type=Path, required=True, help='JSON list of {"t":sec,"name":str,"soft":bool,"dur":sec}')
    q.add_argument("--speech", type=Path, help="vo-timeline JSON output (enables voiceover rules)")
    args = ap.parse_args(argv)
    try:
        data = load(args.data)
        if args.action == "list":
            result = [{k: s[k] for k in ("id", "order", "title_ar", "family")} for s in data["styles"]]
        elif args.action == "principles":
            result = data["principles"]
        elif args.action == "match":
            result = match(args.task, data)
        elif args.action == "brief":
            tl = vo_timeline(parse_srt(args.srt.read_text(encoding="utf-8"))) if args.srt else None
            result = brief(args.ref, data, args.topic, tl, storyboard=not args.direct)
        elif args.action == "clone-plan":
            result = clone_plan(data, args.topic)
        elif args.action == "vo-timeline":
            result = vo_timeline(parse_srt(args.srt.read_text(encoding="utf-8")))
            if args.out:
                args.out.parent.mkdir(parents=True, exist_ok=True)
                args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        else:
            speech = json.loads(args.speech.read_text(encoding="utf-8"))["words"] if args.speech else None
            result = cue_check(json.loads(args.cues.read_text(encoding="utf-8")), speech)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if args.action != "cue-check" or result["passed"] else 3
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print("motion-styles: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
