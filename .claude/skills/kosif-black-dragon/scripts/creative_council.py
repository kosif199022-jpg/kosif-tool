#!/usr/bin/env python3
"""KOSIF Black Dragon Creative Council — traceable specialist roster, not simulated intelligence.

Builds a task-fitted council from the original Dragon Mind / Superpowers thinking
sources. Planning does not invoke an LLM, hold a debate, download assets or render
video. A verdict requires external, explicitly labelled submissions from every
member across three rounds; it never treats persona prompts as independent agents.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DRAGON = ".claude/skills/kosif-dragon-mind/data/frameworks.json"
MODELS = ".claude/skills/kosif-superpowers/data/mental_models.json"
POWERS = ".claude/skills/kosif-superpowers/data/powers/thinking-core.json"
SCHEMA = "kosif.black-dragon.creative-council.v1"

# Thirteen expert seats. The chairman facilitates, never overrides a rights veto.
SEATS = {
    "chair": ("رئيس المجلس ومنسق الجلسات", "Ensures all voices, dissent and evidence are recorded"),
    "analyst": ("محلل المعنى والمبادئ", "Separates facts, assumptions, audience and objective"),
    "story": ("الكاتب الدرامي", "Designs the emotional arc and scene-by-scene meaning"),
    "creative": ("المخرج الإبداعي", "Generates genuinely different visual approaches"),
    "visual": ("المخرج البصري", "Checks style, visual language, continuity and compositions"),
    "engineer": ("مهندس المونتاج والموشن", "Checks render routes, dependencies and budgets"),
    "critic": ("الناقد المعارض", "Attacks weak claims and predicts failure"),
    "decision": ("خبير القرارات والمفاضلة", "Compares alternatives with sensitivity and tradeoffs"),
    "research": ("الباحث ومدقق الأدلة", "Checks sources and uncertainty before relying on claims"),
    "systems": ("خبير الأنظمة والترابط", "Checks dependencies, handoffs and second-order effects"),
    "audience": ("ممثل الجمهور والمنصة", "Tests readability, audience intent and accessibility"),
    "learning": ("خبير التجارب والتعلم", "Records tested outcomes and lessons, not assumptions"),
    "rights": ("حارس الحقوق والموافقات", "Checks assets, licences, privacy and paid actions"),
}
FRAMEWORK_FAMILY = {
    "frame": "analyst", "diverge": "creative", "converge": "decision",
    "decide": "decision", "risk": "critic", "systems": "systems",
    "product": "visual", "learn": "learning", "communicate": "story",
    "execute": "engineer",
}
# Some risk operators are best owned by the independent rights/guardrails seat.
RIGHTS_FRAMEWORKS = {"margin-of-safety", "via-negativa", "swiss-cheese-model", "normal-accidents"}
MODEL_DISCIPLINE = {
    "decision": "decision", "planning": "engineer", "systems": "systems",
    "epistemics": "research", "creativity": "creative", "biases": "critic",
    "reasoning": "analyst", "communication": "story", "learning": "learning",
    "strategy": "analyst", "people": "audience", "probability": "research",
    "economics": "decision", "engineering": "engineer", "argument": "critic",
    "structuring": "analyst", "diagnosis": "analyst", "quantitative": "research",
    "prioritisation": "decision", "complexity": "systems", "product": "visual",
    "forecasting": "research", "capability": "engineer",
}
POWER_SECTION = {
    "Cognition layer": "analyst",
    "حلقة التفكير — Thinking Loop": "chair",
    "التخطيط والتفويض — Planning & delegation": "engineer",
    "وحدات المرحلة صفر — Stage-0 modules": "analyst",
    "القدرات قبل الحل — Capability-first": "research",
    "الأرقام والتغطية — Numbers & coverage": "research",
    "الأنماط المضادة — Anti-patterns": "critic",
    "أكبر مستودعات GitHub — Top GitHub repositories (2026-10-23)": "research",
}
REVIEW_FIELDS = {
    "1": ("proposal", "reasoning", "evidence"),
    "2": ("target_member", "objection", "steelman"),
    "3": ("revised_proposal", "remaining_objection", "scores"),
}
DEFAULT_OPTIONS = ("licensed-footage", "code-motion", "hybrid")
CRITERIA = ("meaning", "drama", "feasibility", "visual-cohesion", "rights", "audience", "editability")
WEIGHTS = {"meaning": 3, "drama": 3, "feasibility": 2, "visual-cohesion": 2,
           "rights": 3, "audience": 2, "editability": 1}


def _read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _record(kind: str, row: dict, role: str, source: str) -> dict:
    if role not in SEATS:
        raise ValueError("unassigned cognitive role for " + str(row.get("id")))
    if kind == "framework":
        name = row.get("name_ar") or row.get("name_en") or row["id"]
        text = " ".join([name, row.get("name_en", ""), " ".join(row.get("triggers_ar", [])),
                         " ".join(row.get("triggers_en", []))])
        maturity = "documented-framework-not-executed"
    elif kind == "model":
        name = row.get("name_ar") or row.get("name_en") or row["id"]
        text = " ".join([name, row.get("name_en", ""), " ".join(row.get("triggers", [])),
                         row.get("question", "")])
        maturity = "documented-model-not-executed"
    else:
        name = row.get("name_ar") or row.get("name_en") or row["id"]
        text = " ".join([name, row.get("name_en", ""), row.get("what", ""), row.get("when", ""),
                         " ".join(row.get("tags", [])[:30])])
        maturity = "source-reports-" + str(row.get("status", "unknown")) + "-not-rerun"
    secondary = set()
    if kind == "framework" and row.get("family") == "product":
        secondary.add("audience")
    if kind == "framework" and row.get("family") == "communicate":
        secondary.add("audience")
    if kind == "framework" and row.get("family") == "risk" and role != "rights":
        secondary.add("rights")
    if role == "creative":
        secondary.add("visual")
    if role == "story":
        secondary.add("audience")
    return {"id": kind + ":" + row["id"], "name": name, "primary": role,
            "secondary": sorted(secondary), "source": source, "maturity": maturity,
            "search_text": text[:1200]}


def inventory(root: Path = ROOT) -> list[dict]:
    f = _read(root / DRAGON)
    models = _read(root / MODELS)
    powers = _read(root / POWERS)
    frameworks = f.get("frameworks", []) if isinstance(f, dict) else []
    if not all(isinstance(x, list) for x in (frameworks, models, powers)):
        raise ValueError("invalid thinking source format")
    rows = []
    for x in frameworks:
        family = x.get("family")
        if family not in FRAMEWORK_FAMILY:
            raise ValueError("unknown framework family: " + str(family))
        role = "rights" if x["id"] in RIGHTS_FRAMEWORKS else FRAMEWORK_FAMILY[family]
        rows.append(_record("framework", x, role, DRAGON))
    for x in models:
        discipline = x.get("discipline")
        if discipline not in MODEL_DISCIPLINE:
            raise ValueError("unknown model discipline: " + str(discipline))
        rows.append(_record("model", x, MODEL_DISCIPLINE[discipline], MODELS))
    for x in powers:
        section = x.get("section")
        if section not in POWER_SECTION:
            raise ValueError("unknown thinking-core section: " + str(section))
        rows.append(_record("power", x, POWER_SECTION[section], POWERS))
    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate thinking entry ID")
    return rows


def tokens(text: str) -> set[str]:
    text = unicodedata.normalize("NFKC", text).casefold()
    text = re.sub(r"[\u064b-\u065f\u0670\u0640]", "", text)
    text = text.translate(str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ى": "ي"}))
    result = set()
    for word in re.findall(r"[a-z0-9]+|[\u0621-\u064a]+", text):
        if len(word) > 2:
            result.add(word)
            if word.startswith("ال") and len(word) > 5:
                result.add(word[2:])
            if word.startswith("وال") and len(word) > 6:
                result.add(word[3:])
    return result


def plan(task: str, root: Path = ROOT, options=DEFAULT_OPTIONS) -> dict:
    if not task or not task.strip():
        raise ValueError("task is required")
    options = list(options)
    if len(options) < 2 or len(options) > 8 or len(set(options)) != len(options):
        raise ValueError("provide 2-8 unique candidate routes")
    entries = inventory(root)
    words = tokens(task)
    seats = []
    for sid, (name, mission) in SEATS.items():
        primary = [x for x in entries if x["primary"] == sid]
        secondary = [x for x in entries if sid in x["secondary"]]
        chosen = sorted(primary + secondary, key=lambda x:
                        (-len(words & tokens(x["search_text"])),
                         x["primary"] != sid, x["id"]))[:5]
        seats.append({"id": sid, "name_ar": name, "mission": mission,
                      "primary_count": len(primary), "secondary_count": len(secondary),
                      "focus": [{"id": r["id"], "role": "primary" if r["primary"] == sid else "secondary",
                                 "source": r["source"], "maturity": r["maturity"]}
                                for r in chosen]})
    record = {
        "schema": SCHEMA + ".plan", "task": task, "status": "PLANNED_NOT_DEBATED",
        "independence": "requires genuine independent runs; one-model roleplay must be labelled SIMULATED",
        "execution": "no assets fetched, models invoked, tools executed or video rendered",
        "total_source_records": len(entries),
        "source_counts": dict(sorted(Counter(x["id"].split(":", 1)[0] for x in entries).items())),
        "primary_assigned": sum(s["primary_count"] for s in seats),
        "roles": seats,
        "assignments": [{k: v for k, v in x.items() if k != "search_text"} for x in entries],
        "options": options,
        "rubric": WEIGHTS,
        "rounds": {
            "1": "Independent proposal; keep other members' submissions hidden. Cite real evidence.",
            "2": "Cross-examine a different member; state their strongest case fairly and one objection.",
            "3": "Revise position; keep dissent visible; score each route 1-5 with reasons.",
        },
        "rights_gate": "licensed assets and explicit approval for paid services, external upload or publishing",
        "preview_gate": "story -> real preview -> actual final media verification; plan is not an MP4",
        "limits": "lexical relevance ranking only; source counts are not independent intelligences or executions",
    }
    record["fingerprint"] = hashlib.sha256(json.dumps(record["assignments"], sort_keys=True,
                                               ensure_ascii=False).encode("utf-8")).hexdigest()
    return record


def verdict(council: dict, submissions: dict) -> dict:
    """Reject incomplete or unlabelled debates instead of faking experts' reasoning."""
    if council.get("schema") != SCHEMA + ".plan":
        raise ValueError("not a creative council plan")
    options = council["options"]
    seat_ids = {s["id"] for s in council["roles"]}
    rounds = submissions.get("rounds") or {}
    mode = submissions.get("mode")
    if mode not in ("INDEPENDENT", "SIMULATED"):
        raise ValueError("mode must be INDEPENDENT or SIMULATED")
    for phase, fields in REVIEW_FIELDS.items():
        reports = rounds.get(phase) or {}
        if set(reports) != seat_ids:
            raise ValueError("round " + phase + " requires all council seats")
        for seat, entry in reports.items():
            for field in fields:
                if field not in entry or not entry[field]:
                    raise ValueError("round %s: %s missing %s" % (phase, seat, field))
            if phase == "2" and entry["target_member"] == seat:
                raise ValueError("member cannot cross-examine itself")
            if phase == "2" and entry["target_member"] not in seat_ids:
                raise ValueError("cross-examination target is not a council member")
            if phase == "3":
                if set(entry["scores"]) != set(options):
                    raise ValueError("every option needs an explicit score")
                for opt in options:
                    grades = entry["scores"][opt]
                    if not isinstance(grades, dict) or set(grades) != set(WEIGHTS):
                        raise ValueError("each route needs every weighted criterion")
                    if any(type(v) is not int or not 1 <= v <= 5 for v in grades.values()):
                        raise ValueError("criterion scores must be integers from 1 to 5")
    if not submissions.get("evidence_attested"):
        raise ValueError("evidence must be independently checked before scoring")
    if not submissions.get("rights_checked"):
        raise ValueError("rights gate has not been checked")
    if mode == "INDEPENDENT":
        receipts = submissions.get("independent_run_ids") or {}
        if set(receipts) != seat_ids or len(set(receipts.values())) != len(seat_ids) or not all(receipts.values()):
            raise ValueError("independent mode requires a distinct run ID for every seat")
    vetoed = submissions.get("rights_vetoes") or []
    if not isinstance(vetoed, list) or any(o not in options for o in vetoed):
        raise ValueError("rights vetoes must name declared options only")
    scores = {opt: sum(sum(rounds["3"][sid]["scores"][opt][criterion] * weight
                            for criterion, weight in WEIGHTS.items()) for sid in sorted(seat_ids))
              for opt in options}
    eligible = [o for o in options if o not in vetoed]
    ranked = sorted(eligible, key=lambda x: (-scores[x], x))
    tied = [o for o in ranked if ranked and scores[o] == scores[ranked[0]]]
    return {
        "schema": SCHEMA + ".verdict",
        "status": "DELIBERATED_NOT_EXECUTED" if mode == "INDEPENDENT" else "SIMULATED_NOT_EXECUTED",
        "mode": mode, "winning_route": ranked[0] if len(tied) == 1 else None,
        "ties_need_human_decision": tied if len(tied) > 1 else [],
        "rights_vetoed": vetoed, "no_eligible_route": not eligible,
        "weighted_votes": scores, "evidence_attested_by_caller": True,
        "rights_checked_by_caller": True,
        "dissent": {sid: rounds["3"][sid]["remaining_objection"] for sid in sorted(seat_ids)},
        "warning": "scores are participant judgments, not proof of artistic merit, media execution or licence",
    }


def _save(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    cmd = parser.add_subparsers(dest="command", required=True)
    roster = cmd.add_parser("roster", help="Count every mapped thinking source by expert")
    draft = cmd.add_parser("plan", help="Build a task-specific council; no agents are run")
    draft.add_argument("task")
    draft.add_argument("--out", type=Path)
    draft.add_argument("--options", default=",".join(DEFAULT_OPTIONS),
                       help="2-8 comma-separated implementation routes")
    judge = cmd.add_parser("verdict", help="Validate three real rounds; do not simulate them")
    judge.add_argument("--plan", type=Path, required=True)
    judge.add_argument("--submissions", type=Path, required=True)
    judge.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "roster":
            entries = inventory(args.root)
            data = {"total": len(entries), "by_source": dict(Counter(x["id"].split(":")[0] for x in entries)),
                    "by_primary_role": {sid: sum(x["primary"] == sid for x in entries) for sid in SEATS},
                    "assigned_once": len({x["id"] for x in entries}) == len(entries)}
        elif args.command == "plan":
            data = plan(args.task, args.root, args.options.split(","))
        else:
            data = verdict(_read(args.plan), _read(args.submissions))
        if getattr(args, "out", None):
            _save(args.out, data)
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0
    except (OSError, TypeError, ValueError, KeyError) as exc:
        print("creative-council: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
