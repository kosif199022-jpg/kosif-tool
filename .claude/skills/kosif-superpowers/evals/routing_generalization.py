#!/usr/bin/env python3
"""Measure how well the USIP brief understands fresh, everyday requests it was never tuned on.

Reads evals/routing_generalization.json (held-out cases, labels written before the changes they measure) and reports:
  * request-card accuracy: primary deliverable and protocol level match the label,
  * off-domain rate: share of the recommended plan's superpowers that come from a group the label calls irrelevant
    (a pricing decision planned with motion or 3D picks is a reasoning failure, not a style choice).

  python3 evals/routing_generalization.py            # table + totals
  python3 evals/routing_generalization.py --json     # one JSON document
Exit code 0 always; the thresholds live in evals/test_routing_generalization.py.
"""
import argparse, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
import skill_intelligence as S  # noqa: E402

CASES = HERE / "routing_generalization.json"


def card_errors(an: dict, e: dict) -> list:
    errs = []
    if "primary" in e and an["primary"] != e["primary"]:
        errs.append(f"primary {an['primary']} != {e['primary']}")
    if "primary_in" in e and an["primary"] not in e["primary_in"]:
        errs.append(f"primary {an['primary']} not in {e['primary_in']}")
    if "primary_not" in e and an["primary"] == e["primary_not"]:
        errs.append(f"primary {an['primary']} is excluded")
    if "level_in" in e and an["level"] not in e["level_in"]:
        errs.append(f"level {an['level']} not in {e['level_in']}")
    if an["level"] in e.get("level_not", []):
        errs.append(f"level {an['level']} is excluded")
    return errs


def evaluate(cases=None) -> dict:
    cases = cases if cases is not None else json.loads(CASES.read_text(encoding="utf-8"))["cases"]
    rows, picks, off = [], 0, 0
    for c in cases:
        b = S.build_brief(c["request"])
        an = b["analysis"]
        errs = card_errors(an, c["expect"])
        rec = b.get("recommended")
        sps = b["plans"][rec]["superpowers"] if rec and b.get("plans") else []
        bad = [f'{x["group"]}:{x["name_en"]}' for x in sps if x["group"] in c.get("irrelevant_groups", [])]
        picks += len(sps)
        off += len(bad)
        rows.append({"id": c["id"], "request": c["request"], "level": an["level"], "primary": an["primary"],
                     "card_ok": not errs, "errors": errs, "plan_picks": len(sps), "off_domain": bad})
    ok = sum(r["card_ok"] for r in rows)
    return {"cases": rows, "n": len(rows), "card_ok": ok, "card_accuracy": round(ok / len(rows), 3) if rows else 0.0,
            "plan_picks": picks, "off_domain_picks": off, "off_domain_rate": round(off / picks, 3) if picks else 0.0}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    res = evaluate()
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    for r in res["cases"]:
        mark = "PASS" if r["card_ok"] and not r["off_domain"] else "FAIL"
        print(f'{mark} {r["id"]} {str(r["level"]):<2} {str(r["primary"]):<11} {r["request"][:55]:<55} '
              + "; ".join(r["errors"] + ([f'off-domain {len(r["off_domain"])}/{r["plan_picks"]}'] if r["off_domain"] else [])))
    print(f'\nrequest card: {res["card_ok"]}/{res["n"]} correct ({res["card_accuracy"]:.0%}) · '
          f'off-domain plan picks: {res["off_domain_picks"]}/{res["plan_picks"]} ({res["off_domain_rate"]:.0%})')
    return 0


if __name__ == "__main__":
    sys.exit(main())
