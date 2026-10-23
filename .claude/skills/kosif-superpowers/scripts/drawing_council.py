#!/usr/bin/env python3
"""KOSIF Drawing Council: eleven drawing experts built from the 48 method cards review an image before it is sent.

PROTOCOL law 27 and appendix A31. The script calls no model. It runs the automated gates, writes one prompt per
expert from that expert's method cards (checks, common errors, veto conditions), records what each expert returned,
and computes a deterministic verdict with a receipt and the list of fixes still required. The experts are run by
Claude itself: real subagents (Agent tool or Workflow) that open the rendered PNG, or, when no agent tool exists,
voices in one context that the minutes then label SIMULATED.

From the repository root:
  python3 .claude/skills/kosif-superpowers/scripts/drawing_council.py roster [--markdown | --personas]
  python3 .claude/skills/kosif-superpowers/scripts/drawing_council.py plan --png scene.png [--svg scene.svg] --brief "<what was asked>" --dir out/<work>/drawing-council
  python3 .claude/skills/kosif-superpowers/scripts/drawing_council.py ingest --dir out/<work>/drawing-council --expert E04 --file e04.json [--simulated]
  python3 .claude/skills/kosif-superpowers/scripts/drawing_council.py verdict --dir out/<work>/drawing-council

An expert answers {"expert": "E04", "verdict": "pass|fix|veto", "scores": {"correctness": 1-5, "craft": 1-5,
"beauty": 1-5}, "findings": [{"check": "...", "observed": "...", "fix": "..."}], "evidence": ["what was looked at"]}.
PASS needs every automated gate PASS, all eleven experts answered on the same PNG, no fix or veto open, every score
at least 3 and a mean beauty score of at least 3.5. After fixes, re-render and plan a new council directory.

Scores are recorded judgements, not measurements: the verdict says who judged and how, never that taste was proven.
Python stdlib only (the visual metrics step uses drawing_visual_qa.py when Pillow is present and is skipped otherwise).
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import drawing_methods as dm  # noqa: E402

SCHEMA = "kosif.drawing-council.v1"
ANSWER_SCHEMA = "kosif.drawing-council.answer.v1"
VERDICTS = ("pass", "fix", "veto")
SCORE_KEYS = ("correctness", "craft", "beauty")
MIN_SCORE = 3
MIN_BEAUTY_MEAN = 3.5

# Every method card belongs to exactly one expert (evals/test_drawing_council.py checks the cover).
EXPERTS = [
    {"id": "E01", "name_ar": "خبير الرؤية والبناء", "name_en": "Observation and construction",
     "cards": ["DM-01", "DM-02", "DM-03", "DM-04", "DM-41", "DM-42", "DM-44"],
     "focus_ar": "هل بُني كل شيء من أشكال بسيطة لها حجم، وهل المقاسات والفراغات السالبة صحيحة؟",
     "veto": ["A form reads flat or broken where it should turn in space",
              "Measured proportions between objects contradict what they are"]},
    {"id": "E02", "name_ar": "خبير التشريح والنسب", "name_en": "Anatomy and proportion",
     "cards": ["DM-07", "DM-08", "DM-09", "DM-10", "DM-11", "DM-34"],
     "focus_ar": "النسب بوحدة الرأس، والقفص والحوض والمفاصل، واليد والرأس والقماش.",
     "veto": ["A limb or segment length is impossible for the body (beyond foreshortening)",
              "Wrong number of limbs, fingers or joints, or a joint bends the wrong way"]},
    {"id": "E03", "name_ar": "خبير الإيماءة والحركة", "name_en": "Gesture and motion",
     "cards": ["DM-06", "DM-29", "DM-30", "DM-45", "DM-27", "DM-28", "DM-17"],
     "focus_ar": "خط الفعل، والاندفاع، والفعل لا الاسم، ودورة المشي والجري، والانضغاط والتمدد والتوقيت.",
     "veto": ["The pose does not perform the action the brief asks for",
              "The body is stiff and symmetrical where the action needs a line of action"]},
    {"id": "E04", "name_ar": "حارس المنطق والفيزياء", "name_en": "Logic and physics guardian",
     "cards": ["DM-12"],
     "focus_ar": "جسم واحد متصل لكل شخصية، وكل يد أو قدم تلمس ما تمسكه أو تقف عليه، والوزن فوق قاعدة الارتكاز، ولا شيء يطفو بلا سبب.",
     "automated": "law27_review",
     "veto": ["Any body is in pieces (neck, waist or a limb not joined)",
              "A hand or foot does not touch what holds it, or a body is held by nothing",
              "The weight would make the figure or object fall"]},
    {"id": "E05", "name_ar": "خبير المنظور والفراغ", "name_en": "Perspective and space",
     "cards": ["DM-05", "DM-31", "DM-37", "DM-39"],
     "focus_ar": "خط أفق واحد، ونقاط تلاشٍ متسقة، والأشخاص والأشياء بالمقياس الصحيح في العمق.",
     "veto": ["Two parts of the scene use incompatible horizons or vanishing points",
              "A figure or object has an impossible size for its depth"]},
    {"id": "E06", "name_ar": "خبير الضوء والقيم", "name_en": "Light and value",
     "cards": ["DM-19", "DM-20", "DM-32", "DM-33"],
     "focus_ar": "مصدر ضوء واحد مقروء، وعائلة ضوء وعائلة ظل، وظلال ساقطة تتبع المصدر، وتجميع القيم.",
     "automated": "visual_metrics",
     "veto": ["Shadows or highlights contradict the light direction"]},
    {"id": "E07", "name_ar": "خبير اللون", "name_en": "Colour",
     "cards": ["DM-21", "DM-36"],
     "focus_ar": "حرارة اللون ولوحة محدودة متناغمة، والبشرة والتظليل، والتباين الذي يخدم نقطة التركيز.",
     "automated": "visual_metrics",
     "veto": ["Colours clash with the mood of the brief or make the focal point unreadable"]},
    {"id": "E08", "name_ar": "خبير التكوين والسرد", "name_en": "Composition and storytelling",
     "cards": ["DM-22", "DM-23", "DM-26"],
     "focus_ar": "نقطة تركيز واحدة، ومسار العين، والأشكال التي تحمل الشعور، ووضوح القصة من نظرة.",
     "veto": ["The story of the brief cannot be read at a glance", "The focal point is lost or there are two competing ones"]},
    {"id": "E09", "name_ar": "خبير الخط والتشطيب", "name_en": "Line and finish",
     "cards": ["DM-24", "DM-47", "DM-48"],
     "focus_ar": "أوزان الخط، والتراكب، والملمس، ونظافة الحواف والتقاطعات (لا مماسات مزعجة).",
     "veto": ["Tangents, stray marks or uneven line weights make shapes unreadable"]},
    {"id": "E10", "name_ar": "خبير تصميم الشخصيات والتعبير", "name_en": "Character design and expression",
     "cards": ["DM-13", "DM-14", "DM-15", "DM-16", "DM-18", "DM-35", "DM-40", "DM-43", "DM-46"],
     "focus_ar": "لغة الأشكال، والسيلويت المقروء، والجاذبية، وتعبير الوجه والعين والحاجب، والشعر ككتل.",
     "veto": ["The expression contradicts the emotion of the brief", "The silhouette does not read"]},
    {"id": "E11", "name_ar": "خبير الحيوان والطبيعة", "name_en": "Animals and nature",
     "cards": ["DM-25", "DM-38"],
     "focus_ar": "بناء الحيوان من خط العمود الفقري وكتل الصدر والحوض، والأشجار والنبات من أشكال بسيطة.",
     "veto": ["An animal's anatomy or pose is impossible for that animal"]},
]


class CouncilError(Exception):
    pass


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise CouncilError(f"missing {path}")
    except json.JSONDecodeError as exc:
        raise CouncilError(f"{path} is not JSON: {exc}")


def roster(atlas=None) -> list:
    """The eleven experts with their cards expanded from the atlas (checks, common errors, books)."""
    cards = {m["id"]: m for m in (atlas or dm.load_atlas())["methods"]}
    out = []
    for e in EXPERTS:
        missing = [c for c in e["cards"] if c not in cards]
        if missing:
            raise CouncilError(f"{e['id']} names unknown cards {missing}")
        ms = [cards[c] for c in e["cards"]]
        out.append(dict(e, books=sorted({b for m in ms for b in m["books"]}),
                        methods=[{"id": m["id"], "name_ar": m["name_ar"], "name_en": m["name_en"],
                                  "checks": m["checks"], "common_errors": m["common_errors"]} for m in ms]))
    return out


PERSONA_LANE = {"E04": "guardrails", "E08": "audience", "E03": "cross_domain"}
PERSONA_TRIGGERS = ["رسم", "رسمة", "صورة", "شخصية", "drawing", "illustration", "image", "character", "sketch"]


def personas(experts: list) -> dict:
    """The experts in the general council's persona schema (kosif.council-personas.v1) for council.py --personas-file."""
    out = []
    for e in experts:
        n = int(e["id"][1:])
        out.append({"id": f"D{n:02d}", "name_ar": e["name_ar"], "name_en": e["name_en"], "title_ar": e["name_ar"],
                    "title_en": f"Drawing council: {e['name_en']}", "lane": PERSONA_LANE.get(e["id"], "verification"),
                    "domains": ["image", "motion"], "triggers": PERSONA_TRIGGERS,
                    "character_ar": e["focus_ar"], "lens_en": "; ".join(m["name_en"] for m in e["methods"]),
                    "superpowers": ([m["id"] + " " + m["name_en"] for m in e["methods"]] + ["Veto: " + v for v in e["veto"]])[:3],
                    "signature_questions": [q for m in e["methods"] for q in m["checks"]][:3],
                    "blind_spot": "Judges only its own lane; geometry and taste outside it belong to other experts.",
                    "evidence_demand": "Opened the rendered PNG and named the region looked at.",
                    "counterpart": "D04" if e["id"] != "E04" else "D08"})
    return {"schema": "kosif.council-personas.v1", "source": "drawing_council.py roster --personas", "personas": out}


def roster_markdown(experts: list) -> str:
    rows = ["| الخبير | يركّز على | البطاقات | كتب | شروط الرفض (veto) |", "|---|---|---|---|---|"]
    for e in experts:
        rows.append(f"| {e['id']} {e['name_ar']} / {e['name_en']} | {e['focus_ar']} | {' '.join(e['cards'])} | "
                    f"{len(e['books'])} | {'؛ '.join(e['veto'])} |")
    return "\n".join(rows) + "\n"


def visual_metrics(png: Path) -> dict:
    script = HERE / "drawing_visual_qa.py"
    try:
        r = subprocess.run([sys.executable, str(script), "diagnose", str(png)], capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"status": "SKIPPED", "reason": str(exc)}
    if r.returncode != 0:
        return {"status": "SKIPPED", "reason": (r.stderr or r.stdout).strip()[-300:]}
    d = json.loads(r.stdout)
    return {"status": d.get("status"), "three_value_ratio": d.get("three_value_ratio"),
            "dark_mass_left_right_index": d.get("dark_mass_left_right_index"),
            "approx_hsv_saturation_mean": d.get("approx_hsv_saturation_mean"), "warnings": d.get("warnings", [])}


CODE_MAP_LIMIT = 240
_TAG = re.compile(r"<([A-Za-z][\w:-]*)\b([^>]*)>")
_ATTR = re.compile(r'\b(id|data-figure|data-part|data-contact)="([^"]*)"')


def code_map(svg: str) -> list:
    """Where each named piece of the drawing lives in the SVG source: line, tag, figure, part, id.
    The experts use it to point every defect at the code that draws it."""
    text = Path(svg).read_text(encoding="utf-8")
    rows, figure = [], None
    for m in _TAG.finditer(text):
        attrs = dict(_ATTR.findall(m.group(2)))
        if "data-figure" in attrs:
            figure = attrs["data-figure"]
        if not ({"data-part", "data-figure"} & attrs.keys() or (attrs.get("id") and m.group(1) not in ("clipPath", "path", "circle"))):
            continue
        rows.append({"line": text.count("\n", 0, m.start()) + 1, "tag": m.group(1), "figure": figure,
                     **{k.replace("data-", ""): v for k, v in attrs.items()}})
        if len(rows) >= CODE_MAP_LIMIT:
            break
    return rows


def expert_prompt(c: dict, e: dict) -> str:
    auto = c["automated"]
    lines = [f"# {e['id']} — {e['name_en']} / {e['name_ar']}", "",
             f"You are one member of an eleven-expert drawing council. The brief was: «{c['brief']}».",
             f"Open the rendered image `{c['png']}` and look at it yourself (zoom into the figures); judge only your lane.",
             f"Your lane: {e['focus_ar']}", "", "## Your method cards (from the drawing books, summarised)"]
    for m in e["methods"]:
        lines.append(f"- **{m['id']} {m['name_en']}** — checks: {'; '.join(m['checks'])}. Common errors: {'; '.join(m['common_errors'])}.")
    lines += ["", "## Veto conditions (any one of these is a veto)"] + [f"- {v}" for v in e["veto"]]
    if e.get("automated") == "law27_review":
        lines += ["", "## Automated law-27 review (you own it)", "```json",
                  json.dumps({k: auto["law27_review"].get(k) for k in ("status", "passed", "total")}, ensure_ascii=False),
                  json.dumps([x for x in auto["law27_review"].get("checks", []) if not x["pass"]], ensure_ascii=False), "```"]
    if e.get("automated") == "visual_metrics":
        lines += ["", "## Measured tone and saturation (advisory, not a beauty judgement)", "```json",
                  json.dumps(auto["visual_metrics"], ensure_ascii=False), "```"]
    if c.get("style"):
        lines += ["", "## Style lock", f"The drawing's chosen style is: «{c['style']}». Judge within it: every fix must keep this style, "
                  "palette and composition. Do not push it toward another style (for example a flat cartoon toward semi-realism); "
                  "fix what is wrong inside the style."]
    if c.get("baseline"):
        lines += ["", "## Compare with the best earlier version",
                  f"Also open `{c['baseline']}`, the best version so far. Say in `vs_baseline` whether this image is "
                  "`better`, `same` or `worse` overall in your lane. A round that most experts call worse is rejected and the "
                  "baseline is kept, however many single fixes it made."]
    code = c.get("code_required")
    if code:
        src = [f"- the SVG: `{c['svg']}`"] if c.get("svg") else []
        src += [f"- the generator that writes it: `{c['source']}`"] if c.get("source") else []
        lines += ["", "## The drawing's code: name the cause, not only the symptom",
                  "Open the source and find what draws each defect. Every finding with a fix must carry `code`: "
                  "`where` (file:line, and the element's data-figure/data-part or id, or the generator's function/constant), "
                  "`cause` (the attribute, value, coordinate or logic that produces the defect) and `change` "
                  "(the exact new value or the code edit). Say so when you could not trace it.", *src]
        if c.get("code_map"):
            lines += ["", "Named parts in the SVG (line · tag · figure · part · id):", "```"]
            lines += [f"{r['line']} · {r['tag']} · {r.get('figure') or '-'} · {r.get('part') or '-'} · {r.get('id') or '-'}" for r in c["code_map"]]
            lines.append("```")
    lines += ["", "## Answer", "Return only JSON:",
              '{"expert": "%s", "verdict": "pass|fix|veto", "scores": {"correctness": 1-5, "craft": 1-5, "beauty": 1-5},' % e["id"],
              ' "findings": [{"check": "<card id or veto>", "observed": "<what you saw, where>", "fix": "<concrete change>"'
              + (', "code": {"where": "<file:line, element or function>", "cause": "<attribute/value/logic>", "change": "<exact edit>"}' if code else "") + '}],',
              ' "evidence": ["<what you looked at, e.g. zoom on the man\'s waist>"]' + (', "vs_baseline": "better|same|worse"' if c.get("baseline") else "") + '}',
              "`fix` and `veto` need at least one finding with a concrete fix"
              + (", and every finding with a fix needs its `code`" if code else "") + ". Do not pass what you did not look at."]
    return "\n".join(lines) + "\n"


def cmd_roster(a) -> int:
    ex = roster()
    if a.personas:
        sys.stdout.write(json.dumps(personas(ex), ensure_ascii=False, indent=2) + "\n")
    else:
        sys.stdout.write(roster_markdown(ex) if a.markdown else json.dumps(ex, ensure_ascii=False, indent=2) + "\n")
    return 0


def cmd_plan(a) -> int:
    d, png = Path(a.dir), Path(a.png)
    if a.baseline and not Path(a.baseline).is_file():
        raise CouncilError(f"no baseline image at {a.baseline}")
    if not png.is_file():
        raise CouncilError(f"no rendered image at {png}: render the PNG first and look at it")
    if (d / "council.json").exists() and not a.force:
        raise CouncilError(f"{d} already holds a council; plan a new directory for a new round (or --force)")
    automated = {"visual_metrics": visual_metrics(png)}
    if a.svg:
        automated["law27_review"] = dm.review_svg(a.svg)
        try:
            kind_check = dm.check_svg(a.svg)
            if kind_check.get("kind"):
                automated["method_checks"] = kind_check
        except (KeyError, TypeError, ValueError):
            pass
    else:
        automated["law27_review"] = {"status": "NOT_RUN", "reason": "no SVG: the logic guardian judges from the image alone"}
    experts = roster()
    c = {"schema": SCHEMA, "created": now_iso(), "brief": a.brief, "png": str(png), "png_sha256": sha256(png),
         "svg": a.svg, "source": a.source, "style": a.style,
         "baseline": a.baseline, "baseline_sha256": sha256(Path(a.baseline)) if a.baseline else None, "code_required": bool(a.svg or a.source),
         "code_map": code_map(a.svg) if a.svg else [], "automated": automated, "experts": experts,
         "thresholds": {"min_score": MIN_SCORE, "min_beauty_mean": MIN_BEAUTY_MEAN}}
    save(d / "council.json", c)
    for e in experts:
        p = d / "prompts" / f"{e['id']}.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(expert_prompt(c, e), encoding="utf-8")
    print(json.dumps({"dir": str(d), "experts": len(experts), "prompts": str(d / "prompts"),
                      "law27_review": automated["law27_review"].get("status"),
                      "visual_metrics": automated["visual_metrics"].get("status")}, ensure_ascii=False))
    return 0


def check_answer(obj: dict, eid: str, code_required: bool = False, baseline: bool = False) -> list:
    probs = []
    if obj.get("expert") != eid:
        probs.append(f"expert is {obj.get('expert')!r}, expected {eid}")
    if obj.get("verdict") not in VERDICTS:
        probs.append(f"verdict must be one of {VERDICTS}")
    sc = obj.get("scores") or {}
    for k in SCORE_KEYS:
        if not isinstance(sc.get(k), int) or not 1 <= sc[k] <= 5:
            probs.append(f"scores.{k} must be an integer 1-5")
    fs = obj.get("findings")
    if not isinstance(fs, list):
        probs.append("findings must be a list")
        fs = []
    for i, f in enumerate(fs):
        if not isinstance(f, dict) or not f.get("check") or not f.get("observed"):
            probs.append(f"findings[{i}] needs check and observed")
    if obj.get("verdict") in ("fix", "veto") and not any(isinstance(f, dict) and f.get("fix") for f in fs):
        probs.append("a fix or veto verdict needs at least one finding with a concrete fix")
    if code_required and obj.get("verdict") in ("fix", "veto"):
        for i, f in enumerate(fs):
            cd = f.get("code") if isinstance(f, dict) else None
            if isinstance(f, dict) and f.get("fix") and not (isinstance(cd, dict) and all(str(cd.get(k) or "").strip() for k in ("where", "cause", "change"))):
                probs.append(f"findings[{i}] needs code.where, code.cause and code.change: point the fix at the drawing's source")
    if baseline and obj.get("vs_baseline") not in ("better", "same", "worse"):
        probs.append("vs_baseline must be better, same or worse: compare with the baseline image")
    if not obj.get("evidence"):
        probs.append("evidence must say what was looked at")
    return probs


def cmd_ingest(a) -> int:
    d = Path(a.dir)
    c = load(d / "council.json")
    ids = {e["id"] for e in c["experts"]}
    if a.expert not in ids:
        raise CouncilError(f"unknown expert {a.expert}")
    obj = load(Path(a.file))
    probs = check_answer(obj, a.expert, bool(c.get("code_required")), bool(c.get("baseline")))
    if probs:
        raise CouncilError("; ".join(probs))
    obj.update({"schema": ANSWER_SCHEMA, "simulated": bool(a.simulated), "recorded": now_iso(),
                "png_sha256": sha256(Path(c["png"]))})
    save(d / "answers" / f"{a.expert}.json", obj)
    print(json.dumps({"recorded": a.expert, "verdict": obj["verdict"], "simulated": obj["simulated"]}))
    return 0


def verdict(d: Path) -> dict:
    c = load(d / "council.json")
    png_now = sha256(Path(c["png"])) if Path(c["png"]).is_file() else None
    answers = {e["id"]: load(d / "answers" / f"{e['id']}.json") for e in c["experts"]
               if (d / "answers" / f"{e['id']}.json").exists()}
    missing = [e["id"] for e in c["experts"] if e["id"] not in answers]
    stale = [k for k, v in answers.items() if v.get("png_sha256") != c["png_sha256"]]
    auto_fail = [k for k, v in c["automated"].items() if v.get("status") == "FAIL"]
    fixes = [dict(f, expert=k, verdict=v["verdict"]) for k, v in sorted(answers.items())
             for f in v.get("findings", []) if v["verdict"] != "pass" and f.get("fix")]
    low = [{"expert": k, "scores": v["scores"]} for k, v in sorted(answers.items())
           if min(v["scores"].values()) < MIN_SCORE]
    beauty = [v["scores"]["beauty"] for v in answers.values()]
    beauty_mean = round(sum(beauty) / len(beauty), 2) if beauty else None
    vetoes = sorted(k for k, v in answers.items() if v["verdict"] == "veto")
    open_fix = sorted(k for k, v in answers.items() if v["verdict"] == "fix")
    reasons = []
    if png_now != c["png_sha256"]:
        reasons.append("the PNG changed after planning: plan a new council for the new render")
    if auto_fail:
        reasons.append(f"automated gate FAIL: {', '.join(auto_fail)}")
    if missing:
        reasons.append(f"experts not heard: {', '.join(missing)}")
    if stale:
        reasons.append(f"answers about another image: {', '.join(stale)}")
    if vetoes:
        reasons.append(f"veto: {', '.join(vetoes)}")
    if open_fix:
        reasons.append(f"fixes required by: {', '.join(open_fix)}")
    if low:
        reasons.append(f"a score below {MIN_SCORE}: {', '.join(x['expert'] for x in low)}")
    worse = sorted(k for k, v in answers.items() if v.get("vs_baseline") == "worse")
    if c.get("baseline") and answers and len(worse) * 2 > len(answers):
        reasons.append(f"worse than the baseline for {len(worse)} of {len(answers)} experts: keep the baseline and fix it instead")
    if beauty_mean is not None and beauty_mean < MIN_BEAUTY_MEAN:
        reasons.append(f"mean beauty {beauty_mean} below {MIN_BEAUTY_MEAN}")
    status = "INCOMPLETE" if missing and not (auto_fail or vetoes) else ("PASS" if not reasons else "FAIL")
    simulated = sorted(k for k, v in answers.items() if v.get("simulated"))
    mode = "REAL_AGENTS" if answers and not simulated else ("SIMULATED" if simulated else "NONE")
    return {"schema": SCHEMA + ".verdict", "computed": now_iso(), "status": status, "mode": mode,
            "simulated_experts": simulated, "reasons": reasons, "required_fixes": fixes,
            "scores": {k: v["scores"] for k, v in sorted(answers.items())}, "beauty_mean": beauty_mean,
            "automated": {k: v.get("status") for k, v in c["automated"].items()},
            "png": c["png"], "png_sha256": c["png_sha256"], "brief": c["brief"], "style": c.get("style"),
            "baseline": c.get("baseline"), "vs_baseline": {k: v.get("vs_baseline") for k, v in sorted(answers.items()) if v.get("vs_baseline")},
            "scope": ("Automated gates measure geometry and tone; the scores are the experts' recorded judgements "
                      "against their method cards, not a proof of beauty. SIMULATED means one context played the experts.")}


def minutes(v: dict, c: dict) -> str:
    names = {e["id"]: f"{e['id']} {e['name_ar']}" for e in c["experts"]}
    out = [f"# محضر مجلس الرسم — {v['status']} ({v['mode']})", "", f"الطلب: {v['brief']}", f"الصورة: `{v['png']}`", "",
           "## الفحوص الآلية", ""] + [f"- {k}: {s}" for k, s in v["automated"].items()]
    out += ["", "## الدرجات (صحة · حِرفة · جمال)", ""]
    out += [f"- {names[k]}: {s['correctness']} · {s['craft']} · {s['beauty']}" for k, s in v["scores"].items()]
    out += ["", f"متوسط الجمال: {v['beauty_mean']}", ""]
    if v.get("style"):
        out += [f"الستايل المثبّت: {v['style']}", ""]
    if v.get("vs_baseline"):
        out += [f"مقارنة بأحسن نسخة سابقة (`{v['baseline']}`): " + "، ".join(f"{k} {x}" for k, x in v["vs_baseline"].items()), ""]
    if v["reasons"]:
        out += ["## أسباب عدم القبول", ""] + [f"- {r}" for r in v["reasons"]] + [""]
    if v["required_fixes"]:
        out += ["## التصليحات المطلوبة", ""]
        for f in v["required_fixes"]:
            out.append(f"- {names[f['expert']]} ({f['verdict']}) · {f['check']}: {f['observed']} ← {f['fix']}")
            if isinstance(f.get("code"), dict):
                cd = f["code"]
                out.append(f"  - الكود: `{cd.get('where')}` · السبب: {cd.get('cause')} · التعديل: {cd.get('change')}")
        out.append("")
    out += ["", v["scope"]]
    return "\n".join(out) + "\n"


def cmd_verdict(a) -> int:
    d = Path(a.dir)
    v = verdict(d)
    save(d / "verdict.json", v)
    (d / "minutes.md").write_text(minutes(v, load(d / "council.json")), encoding="utf-8")
    print(json.dumps({k: v[k] for k in ("status", "mode", "reasons", "beauty_mean")}, ensure_ascii=False))
    return 0 if v["status"] == "PASS" else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("roster", help="the eleven experts and their cards")
    s.add_argument("--markdown", action="store_true")
    s.add_argument("--personas", action="store_true", help="emit the experts in the general council persona schema")
    s = sub.add_parser("plan", help="run the automated gates and write one prompt per expert")
    s.add_argument("--png", required=True)
    s.add_argument("--svg")
    s.add_argument("--source", help="the generator that writes the SVG (experts trace defects into it too)")
    s.add_argument("--style", help="lock the drawing's style: experts fix within it, never toward another style")
    s.add_argument("--baseline", help="the best earlier version: each expert says better/same/worse, and a majority 'worse' fails the round")
    s.add_argument("--brief", required=True)
    s.add_argument("--dir", required=True)
    s.add_argument("--force", action="store_true")
    s = sub.add_parser("ingest", help="record one expert's answer")
    s.add_argument("--dir", required=True)
    s.add_argument("--expert", required=True)
    s.add_argument("--file", required=True)
    s.add_argument("--simulated", action="store_true", help="the answer was written in the main context, not by a separate agent")
    s = sub.add_parser("verdict", help="compute PASS/FAIL, write verdict.json and minutes.md")
    s.add_argument("--dir", required=True)
    a = ap.parse_args(argv)
    try:
        return {"roster": cmd_roster, "plan": cmd_plan, "ingest": cmd_ingest, "verdict": cmd_verdict}[a.cmd](a)
    except (CouncilError, OSError, ValueError, dm.ET.ParseError) as exc:
        print("DRAWING_COUNCIL_ERROR: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
