#!/usr/bin/env python3
"""Book-informed decision-review prompts for KOSIF Black Dragon.

A structured, deterministic reasoning aid, not a psychological diagnostic,
independent LLM council, proof of human cognition, or video renderer.
Source: Daniel Kahneman, Thinking, Fast and Slow, supplied PDF (468 pages).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

SCHEMA = "kosif.black-dragon.judgment-guard.v1"
SEATS = {
    "chair", "analyst", "story", "creative", "visual", "engineer",
    "critic", "decision", "research", "systems", "audience", "learning",
}
# PDF page numbers refer to the supplied 468-page edition, not print pagination.
LENSES = {
    "two_systems": (20, 24, "chair", "Use an inexpensive first pass and an evidence-focused second pass where warranted."),
    "question_substitution": (84, 87, "analyst", "Verify that the proposed answer addresses the actual task, not an easier proxy question."),
    "wysiati": (69, 76, "research", "Ask what important evidence is missing, instead of trusting a coherent story."),
    "base_rates": (94, 102, "research", "Check reference classes and sample sizes before generalizing from examples."),
    "anchoring": (103, 111, "decision", "Make an independent estimate before using a supplied price, duration or reference."),
    "availability": (112, 126, "research", "Check whether vivid, recent examples are distorting the evidence sample."),
    "intuition": (198, 206, "learning", "Assess whether experience came from a predictable environment with timely feedback."),
    "outside_view": (207, 213, "engineer", "Compare estimated time and effort with similar completed projects."),
    "premortem": (222, 223, "critic", "Imagine failure beforehand and record concrete causes and mitigations."),
    "framing": (307, 317, "decision", "Evaluate equivalent gain- and loss-framed descriptions against the same criteria."),
    "two_selves": (318, 330, "audience", "Judge both moment-to-moment experience and what the viewer remembers afterward."),
}

def _text(v: Any) -> str:
    return v.strip() if isinstance(v, str) else ""

def _item(key: str, status: str, *, note: str = "") -> dict:
    start, end, owner, prompt = LENSES[key]
    return {"id": key, "status": status, "owner": owner, "prompt": prompt,
            "reference_pdf_pages": [start, end], "note": note}

def _list_text(value: Any, field: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(x, str) for x in value):
        raise ValueError(f"{field} must be a list of strings")
    return [x.strip() for x in value if x.strip()]

def review(brief: dict) -> dict:
    """Create an auditable review plan, without pretending conclusions were verified.

    Expected: goal, options, stakes, reversible, target_question,
    proxy_question, known_evidence, missing_evidence, sample_size,
    reference_class, outside_view_examples, anchor, independent_estimate,
    recent_examples_only, trusted_intuition, stable_environment,
    feedback_history, alternative_framings, failure_scenarios,
    storyboard, intended_audience.
    """
    if not isinstance(brief, dict):
        raise ValueError("input must be a JSON object")
    goal = _text(brief.get("goal"))
    if not goal:
        raise ValueError("goal is required")
    options = _list_text(brief.get("options"), "options")
    if len(options) != len(set(options)):
        raise ValueError("options must be unique")
    stakes = brief.get("stakes", "medium")
    if stakes not in ("low", "medium", "high"):
        raise ValueError("stakes must be low, medium or high")
    reversible = brief.get("reversible", True)
    if not isinstance(reversible, bool):
        raise ValueError("reversible must be boolean")
    for key in ("recent_examples_only", "trusted_intuition", "stable_environment", "feedback_history"):
        if key in brief and not isinstance(brief[key], bool):
            raise ValueError(f"{key} must be boolean")
    known = _list_text(brief.get("known_evidence"), "known_evidence")
    missing = _list_text(brief.get("missing_evidence"), "missing_evidence")
    failures = _list_text(brief.get("failure_scenarios"), "failure_scenarios")
    framings = _list_text(brief.get("alternative_framings"), "alternative_framings")
    sample = brief.get("sample_size")
    if sample is not None and (type(sample) is not int or sample < 0):
        raise ValueError("sample_size must be a nonnegative integer")
    peers = brief.get("outside_view_examples", [])
    if not isinstance(peers, list) or any(type(x) not in (int, float) or x < 0 for x in peers):
        raise ValueError("outside_view_examples must be nonnegative numbers")
    storyboard = brief.get("storyboard", {})
    if not isinstance(storyboard, dict):
        raise ValueError("storyboard must be an object")

    # Deliberation is adaptive, not an imposed three-round council protocol.
    reasons = []
    if stakes == "high": reasons.append("high_stakes")
    if not reversible: reasons.append("hard_to_reverse")
    if missing: reasons.append("identified_evidence_gaps")
    if not known: reasons.append("no_recorded_evidence")
    if not options: reasons.append("no_candidate_options")
    mode = "deliberate_review" if reasons else "lightweight_review"

    checks = []
    checks.append(_item("two_systems", "triggered" if reasons else "advisory",
                        note="Mode is a workflow metaphor, not actual human System 1/System 2."))
    target = _text(brief.get("target_question"))
    proxy = _text(brief.get("proxy_question"))
    checks.append(_item("question_substitution", "review" if proxy or not target else "recorded",
                        note="A proxy is recorded" if proxy else "Explicit target question needed" if not target else "Target question supplied; alignment still needs human review"))
    checks.append(_item("wysiati", "review" if missing or not known else "advisory",
                        note=f"{len(known)} supplied evidence items; {len(missing)} declared gaps"))
    checks.append(_item("base_rates", "review" if (not _text(brief.get("reference_class")) or sample is None or sample < 3) else "recorded",
                        note="Small sample warning is a workflow convention, not a statistically sufficient threshold."))
    anchor_supplied = "anchor" in brief and brief["anchor"] is not None
    independent = "independent_estimate" in brief and brief["independent_estimate"] is not None
    checks.append(_item("anchoring", "review" if anchor_supplied and not independent else "advisory",
                        note="An anchor was provided without a separate initial estimate" if anchor_supplied and not independent else "No anchoring inference made"))
    checks.append(_item("availability", "review" if brief.get("recent_examples_only", False) else "advisory"))
    intuition_used = brief.get("trusted_intuition", False)
    stable = brief.get("stable_environment", False)
    feedback = brief.get("feedback_history", False)
    checks.append(_item("intuition", "review" if intuition_used and not (stable and feedback) else "advisory",
                        note="Expert confidence is not evidence of reliability" if intuition_used else "Intuition reliance not declared"))
    outside = sorted(float(x) for x in peers)
    # Median is a descriptive benchmark, not a project-duration prediction.
    med = None
    if outside:
        mid = len(outside)//2
        med = outside[mid] if len(outside)%2 else (outside[mid-1]+outside[mid])/2
    checks.append(_item("outside_view", "review" if len(outside) < 3 else "recorded",
                        note=f"{len(outside)} comparable examples supplied"))
    checks.append(_item("premortem", "review" if not failures else "recorded",
                        note=f"{len(failures)} failure scenarios provided; no risk elimination claimed"))
    checks.append(_item("framing", "review" if len(framings) < 2 else "recorded",
                        note="Reviewing two phrasings does not guarantee equivalence"))
    story_fields = [k for k in ("hook", "turning_point", "ending") if _text(storyboard.get(k))]
    checks.append(_item("two_selves", "review" if len(story_fields) < 3 or not _text(brief.get("intended_audience")) else "recorded",
                        note="Apply peak/end as a design hypothesis, not a universal audience score."))

    return {
        "schema": SCHEMA, "goal": goal, "mode": mode, "deliberation_reasons": reasons,
        "options": options, "review_checks": checks,
        "checks_needing_attention": [c["id"] for c in checks if c["status"] == "review"],
        "reference_class_benchmark_median": med,
        "reference_class_sample_count": len(outside),
        "sources": {"title": "Thinking, Fast and Slow", "author": "Daniel Kahneman",
                    "edition": "468-page user-supplied PDF", "page_numbers": "PDF page numbers, not print pages"},
        "limits": "Deterministic prompts and validation only; no model agents ran, no independent evidence verified, no footage rendered, no cognitive improvement scientifically measured.",
        "next_step": "Ask relevant specialists for evidence-backed responses; verify with an actual preview and real project data.",
    }

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    args=parser.parse_args(argv)
    payload=review(json.loads(args.input.read_text(encoding="utf-8")))
    content=json.dumps(payload, ensure_ascii=False, indent=2)+"\n"
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(content, encoding="utf-8")
    print(content, end="")

if __name__ == "__main__":
    main()
