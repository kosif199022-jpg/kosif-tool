#!/usr/bin/env python3
"""KOSIF Invention Lab — explicit, falsifiable concept generation; not patent clearance.

Generate structured engineering alternatives without pretending an LLM or expert council ran.
Run: python3 invention_lab.py invent "problem statement" --count 12 --constraint "budget"
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from dataclasses import asdict, dataclass

METHODS = [
    ("segmentation", "Break a single expensive step into independently replaceable modules", "Modularize and compare the costly step against current end-to-end behavior"),
    ("extraction", "Separate a harmful or slow subsystem from the critical path", "Remove a bottleneck behind a reversible feature flag"),
    ("local_quality", "Invest extra fidelity only where observation shows high user value", "A/B test the affected high-salience region"),
    ("asymmetry", "Use differing mechanisms for unlike inputs instead of one uniform path", "Run stratified tests on the two hardest input classes"),
    ("merging", "Combine adjacent operations to remove unnecessary handoffs", "Measure handoff count, throughput and error rate"),
    ("universality", "Reuse one independently verified component across separate tasks", "Verify cross-task correctness and regression footprint"),
    ("nested", "Encapsulate a smaller controllable module inside the existing system", "Prototype behind an opt-in boundary and compare failure containment"),
    ("dynamics", "Adapt processing to measurable input complexity", "Test simple and complex fixtures under deterministic thresholds"),
    ("preliminary_action", "Precompute expensive but stable intermediate representations", "Benchmark cold versus warm requests and invalidation"),
    ("feedback", "Observe outcomes, identify measurable errors, and close a feedback loop", "Define a baseline and record feedback-driven improvement"),
    ("copying", "Use a cheap reversible simulation before full-cost production", "Compare simulator prediction with an independent real fixture"),
    ("parameter_change", "Vary a controlled parameter instead of rewriting the whole system", "Sweep bounded parameter values and record quality/cost curves"),
    ("intermediary", "Introduce an explicit adapter to preserve incompatible interfaces", "Test old/new interface compatibility under a rollback"),
    ("self_service", "Move repetitive verification into deterministic checks", "Add a regression test and measure escaped defects"),
    ("other_way_round", "Invert the order, direction or responsibility of two steps", "Prototype an inverse workflow on representative user tasks"),
    ("resource_use", "Reuse already-existing data or compute rather than adding dependencies", "Inventory available resources and compare total cost")
]
LENSES = [
    ("quality", "Improve accuracy, legibility or output fidelity"),
    ("latency", "Reduce delay and repeated work"),
    ("resilience", "Improve error isolation and recovery"),
    ("accessibility", "Reduce operator effort and make edge cases discoverable")
]

@dataclass
class Idea:
    id: str
    method: str
    lens: str
    proposal: str
    hypothesis: str
    test: str
    success_metric: str
    failure_threshold: str
    novelty_status: str
    risk: str
    cost_class: str
    priority_score: int

def normalize(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()

def make_ideas(problem: str, count: int = 12, constraints: list[str] | None = None) -> list[Idea]:
    problem = normalize(problem)
    if not (8 <= len(problem) <= 2000):
        raise ValueError("provide a specific problem of 8–2000 characters")
    if not (1 <= count <= 64):
        raise ValueError("count must be 1–64")
    restrictions = [normalize(x) for x in (constraints or []) if normalize(x)]
    seed = hashlib.sha256(problem.lower().encode()).digest()
    candidates: list[Idea] = []
    for mi, (tag, method, experiment) in enumerate(METHODS):
        for li, (lens, improvement) in enumerate(LENSES):
            key = seed[(mi * 4 + li) % len(seed)]
            # Order candidates reproducibly without hallucinating any measured novelty score.
            priority = 25 + key % 30 + (7 if tag in ("segmentation", "feedback", "self_service") else 0) + (6 if li == 0 else 0)
            metric = {
                "quality":"Measured error rate or expert-graded legibility on a fixed blind fixture",
                "latency":"Median and p95 elapsed time on equal workloads",
                "resilience":"Failure recovery rate and regression count on fault injection",
                "accessibility":"Median task completion time and observed operator errors"
            }[lens]
            proposal = f"For '{problem}', apply {tag}: {method.lower()}; optimize for {improvement.lower()}."
            risk = ("Constraints to check: " + "; ".join(restrictions[:6])) if restrictions else "Unvalidated assumptions, implementation cost and regressions"
            candidates.append(Idea(
                id=f"KIN-{mi+1:02d}-{li+1}",method=tag,lens=lens,proposal=proposal,
                hypothesis=f"Applying {tag} to the scoped problem will yield an observable gain in {lens} without violating constraints.",
                test=experiment + f"; independently compare against a fixed baseline for {lens}.",
                success_metric=metric,
                failure_threshold="Reject if the named metric does not improve or any security/correctness gate fails",
                novelty_status="unverified_candidate_not_a_patent_search",
                risk=risk, cost_class="unknown_until_prototype",
                priority_score=priority
            ))
    candidates.sort(key=lambda x:(-x.priority_score,x.id))
    return candidates[:count]

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("action", choices=["invent", "methods"])
    ap.add_argument("problem", nargs="?")
    ap.add_argument("--count", type=int, default=12)
    ap.add_argument("--constraint", action="append", default=[])
    ns=ap.parse_args(argv)
    if ns.action == "methods":
        print(json.dumps([{"method":a,"technique":b,"experiment":c} for a,b,c in METHODS], indent=2))
        return 0
    if not ns.problem:
        ap.error("invent needs an explicit problem description")
    try:
        out=make_ideas(ns.problem,ns.count,ns.constraint)
    except ValueError as exc:
        ap.error(str(exc))
    print(json.dumps({"schema":"kosif-invention-candidates-v1",
        "problem":normalize(ns.problem),"constraints":ns.constraint,
        "disclaimer":"Ideas are hypotheses only; rankings are heuristics, not independent innovation/patent evidence",
        "candidates":[asdict(x) for x in out]},ensure_ascii=False,indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
