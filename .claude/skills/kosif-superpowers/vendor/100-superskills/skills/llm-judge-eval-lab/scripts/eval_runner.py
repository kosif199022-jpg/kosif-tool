#!/usr/bin/env python3
"""مجمّع تقييم مستقل عن النموذج: يقرأ درجات القضاة (JSON) ويحسب المتوسطات وσ وفجوة القاضي الخصومي والتأكيدات وpass@k/pass^k وبوابة الانحدار.

usage:
  python eval_runner.py score  --rubric rubric.json --judges scores/*.json [--assertions assert.json] [--out result.json]
  python eval_runner.py compare --a a_scores/*.json --b b_scores/*.json            # A/B مع تبديل الموضع المسجّل في كل ملف
  python eval_runner.py bench  --runs run1.json run2.json ... [--k 3]              # pass@k و pass^k لكل استراتيجية
  python eval_runner.py gate   --run result.json --baseline baseline.json          # exit 3 عند الانحدار
  python eval_runner.py kappa  --human human.json --judge judge.json                # Cohen's κ لكل معيار

ملف درجات قاضٍ: {"judge":"j1","role":"standard|adversarial","vendor":"claude","scores":{"criterion":1-10|"N/A",...},"reasons":{...},"position":"AB"|"BA"}
rubric.json: {"name":"code-quality","pass_threshold":7,"criteria":{"correctness":0.3,"security":0.3,"readability":0.2,"tests":0.2}}
assert.json: {"results":[{"name":"tests","kind":"cmd|judge|file|grep","result":"PASS|HARD_FAIL"}]}
القواعد: σ<0.8 بين القياسيين = «يحتاج تحققاً»؛ فجوة خصومي >1.5 ← 0.6×قياسي+0.4×خصومي؛ >3 ← الخصومي يسود؛ N/A لا يُستبدل برقم؛ أي HARD_FAIL يُسقط النجاح.
"""
import argparse
import glob
import json
import math
import statistics as st
import sys


def load(paths):
    out = []
    for p in paths:
        for f in sorted(glob.glob(p)):
            out.append(json.load(open(f, encoding="utf-8")))
    return out


def weighted(scores: dict, weights: dict):
    num = den = 0.0
    for k, w in weights.items():
        v = scores.get(k)
        if isinstance(v, (int, float)):
            num += v * w; den += w
    return num / den if den else None


def score(a):
    rubric = json.load(open(a.rubric, encoding="utf-8"))
    weights = rubric["criteria"]; judges = load(a.judges)
    if not judges:
        sys.exit("no judge files")
    std = [j for j in judges if j.get("role", "standard") != "adversarial"]
    adv = [j for j in judges if j.get("role") == "adversarial"]
    per_crit = {}
    for c in weights:
        vals = [j["scores"].get(c) for j in judges]
        nums = [v for v in vals if isinstance(v, (int, float))]
        per_crit[c] = {"avg": round(st.mean(nums), 2) if nums else None, "n": len(nums), "na": len(vals) - len(nums),
                       "by_judge": {j["judge"]: j["scores"].get(c) for j in judges}}
    std_scores = [weighted(j["scores"], weights) for j in std]; std_scores = [s for s in std_scores if s is not None]
    adv_scores = [weighted(j["scores"], weights) for j in adv]; adv_scores = [s for s in adv_scores if s is not None]
    std_avg = st.mean(std_scores) if std_scores else None
    adv_avg = st.mean(adv_scores) if adv_scores else None
    sigma = st.pstdev(std_scores) if len(std_scores) > 1 else None
    notes, final = [], None
    if std_avg is not None and adv_avg is not None:
        gap = std_avg - adv_avg
        if gap > 3:
            final = adv_avg; notes.append(f"فجوة خصومي {gap:.1f} > 3: مشكلة جودة جوهرية؛ درجة الخصومي تسود")
        elif gap > 1.5:
            final = 0.6 * std_avg + 0.4 * adv_avg; notes.append(f"فجوة خصومي {gap:.1f} > 1.5: تحيز مشترك مكتشف؛ 0.6×قياسي + 0.4×خصومي")
        else:
            final = st.mean(std_scores + adv_scores)
    else:
        final = std_avg if std_avg is not None else adv_avg
    if sigma is not None and sigma < 0.8:
        notes.append("σ < 0.8 بين القياسيين: اتفاق عالٍ = خطر تحيز مشترك؛ قارن بالخصومي، لا تقرأه يقيناً")
    elif sigma is not None and sigma > 1.5:
        notes.append("σ > 1.5: خلاف حقيقي؛ استدعِ قاضياً إضافياً من نموذج مختلف أو أعلن «بلا حكم»")
    vendors = {j.get("vendor") for j in judges if j.get("vendor")}
    if len(vendors) > 1:
        notes.append(f"قضاة من مورّدين متعددين ({', '.join(sorted(vendors))}): σ هنا إشارة اتفاق حقيقية عبر النماذج")
    assertions, hard_fail = [], False
    if a.assertions:
        assertions = json.load(open(a.assertions, encoding="utf-8")).get("results", [])
        hard_fail = any(r.get("result") == "HARD_FAIL" for r in assertions)
    thr = rubric.get("pass_threshold", 7)
    passed = (final is not None and final >= thr) and not hard_fail
    res = {"rubric": rubric["name"], "judges": len(judges), "standard": len(std), "adversarial": len(adv), "per_criterion": per_crit,
           "standard_avg": round(std_avg, 2) if std_avg is not None else None, "adversarial_avg": round(adv_avg, 2) if adv_avg is not None else None,
           "sigma": round(sigma, 2) if sigma is not None else None, "final": round(final, 2) if final is not None else None,
           "pass_threshold": thr, "assertions": assertions, "hard_fail": hard_fail, "passed": passed, "notes": notes,
           "na_criteria": [c for c, v in per_crit.items() if v["n"] == 0]}
    if a.out:
        open(a.out, "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1))
    return res


def compare(a):
    A = load(a.a); B = load(a.b)
    def tally(js, side):
        return sum(1 for j in js if j.get("winner") == side)
    wins_a = tally(A, "A") + tally(B, "A"); wins_b = tally(A, "B") + tally(B, "B")
    positions = {j.get("position") for j in A + B}
    note = "ترتيب A/B لم يُبدَّل بين القضاة؛ تحيز الموضع غير مضبوط" if len(positions) < 2 else "ترتيب A/B مبدَّل بين القضاة"
    return {"wins_A": wins_a, "wins_B": wins_b, "judges": len(A + B), "position_variants": sorted(p for p in positions if p), "note": note,
            "winner": "A" if wins_a > wins_b else "B" if wins_b > wins_a else "tie"}


def bench(a):
    runs = [json.load(open(p, encoding="utf-8")) for p in a.runs]  # each: {"strategy":..., "trials":[{"passed":bool,"score":float}]}
    out = {}
    for r in runs:
        tr = r["trials"]; n = len(tr); c = sum(1 for t in tr if t.get("passed"))
        p = c / n if n else 0
        k = min(a.k, n)
        pass_at_k = 1 - math.comb(n - c, k) / math.comb(n, k) if n >= k and n - c >= k else (1.0 if c else 0.0)
        pass_pow_k = p ** k
        out[r["strategy"]] = {"trials": n, "pass_rate": round(p, 3), f"pass@{k}": round(pass_at_k, 3), f"pass^{k}": round(pass_pow_k, 3),
                              "avg_score": round(st.mean([t.get("score", 0) for t in tr]), 2) if tr else None}
    best = max(out.items(), key=lambda kv: (kv[1][f"pass^{min(a.k, 10**6)}"] if f"pass^{a.k}" in kv[1] else 0, kv[1]["avg_score"] or 0))[0] if out else None
    return {"strategies": out, "best_by_reliability": best}


def gate(a):
    run = json.load(open(a.run, encoding="utf-8")); base = json.load(open(a.baseline, encoding="utf-8"))
    drop = (base.get("final") or 0) - (run.get("final") or 0)
    lost_pass = base.get("passed") and not run.get("passed")
    blocked = lost_pass or drop >= 0.5 or (run.get("hard_fail") and not base.get("hard_fail"))
    return {"baseline_final": base.get("final"), "run_final": run.get("final"), "drop": round(drop, 2), "lost_pass": bool(lost_pass), "blocked": bool(blocked)}


def kappa(a):
    H = json.load(open(a.human, encoding="utf-8")); J = json.load(open(a.judge, encoding="utf-8"))  # {"items":[{"id":..,"labels":{"crit":"PASS|FAIL"}}]}
    out = {}
    hj = {i["id"]: i["labels"] for i in H["items"]}; jj = {i["id"]: i["labels"] for i in J["items"]}
    crits = set().union(*(set(v) for v in hj.values()))
    for c in crits:
        pairs = [(hj[i][c], jj[i][c]) for i in hj if i in jj and c in hj[i] and c in jj[i]]
        n = len(pairs)
        if n == 0:
            continue
        po = sum(1 for h, j in pairs if h == j) / n
        labels = set(h for h, _ in pairs) | set(j for _, j in pairs)
        pe = sum((sum(1 for h, _ in pairs if h == l) / n) * (sum(1 for _, j in pairs if j == l) / n) for l in labels)
        k = (po - pe) / (1 - pe) if pe < 1 else 1.0
        out[c] = {"n": n, "agreement": round(po, 3), "kappa": round(k, 3), "verdict": "strong" if k >= 0.8 else "moderate" if k >= 0.6 else "weak: لا تستخدم للبوابات"}
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["score", "compare", "bench", "gate", "kappa"])
    ap.add_argument("--rubric"); ap.add_argument("--judges", nargs="*", default=[]); ap.add_argument("--assertions"); ap.add_argument("--out")
    ap.add_argument("--a", nargs="*", default=[]); ap.add_argument("--b", nargs="*", default=[]); ap.add_argument("--runs", nargs="*", default=[]); ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--run"); ap.add_argument("--baseline"); ap.add_argument("--human"); ap.add_argument("--judge")
    a = ap.parse_args()
    res = {"score": score, "compare": compare, "bench": bench, "gate": gate, "kappa": kappa}[a.cmd](a)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(json.dumps(res, ensure_ascii=False, indent=1))
    if a.cmd == "gate" and res["blocked"]:
        sys.exit(3)
    if a.cmd == "score" and not res["passed"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
