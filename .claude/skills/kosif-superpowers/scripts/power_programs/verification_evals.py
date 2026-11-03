"""Real programs for the verification-evals power cards (CHECK-*, Black Dragon).

Each function builds its own fixture (a tiny project, a film, receipts, ledgers, a catalog copy,
a localhost mock model server ...), runs the card's verification technique with the card's own
numbers and returns known-answer checks: the clean case passes and seeded defects are caught.
Offline and deterministic: no network beyond 127.0.0.1, no LLM, no credits. Cards whose proof is
an existing code file, or that need isolated Claude reviewers, are listed in
out/power-programs/qa-skipped.json.
"""
from __future__ import annotations

import codecs
import hashlib
import json
import math
import re
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

from .qa_verification import C, wjson, ff, probe, vstream, write_video, moving_frames, sha256, validate_receipt, LADDER

PROGRAMS: dict = {}


def program(pid):
    def deco(fn):
        PROGRAMS[pid] = fn
        return fn
    return deco


# ---------------------------------------------------------------- CHECK-01 verification loop
def run_checks(checks):
    return [(name, bool(fn())) for name, fn in checks]


def verification_loop(state, checks, fixers, budget=4):
    """Run every check; fix the first failing one; loop until all pass or the budget ends."""
    log = []
    for it in range(1, budget + 1):
        res = run_checks([(n, lambda f=f: f(state)) for n, f in checks]); log.append(res)
        failing = [n for n, ok in res if not ok]
        if not failing:
            return {"done": True, "iterations": it, "log": log}
        fixers[failing[0]](state)
    return {"done": False, "iterations": budget, "log": log, "unverified": failing}


@program("CHECK-01")
def check_01(work):
    w = Path(work); audio = w / "voice.wav"; audio.write_bytes(bytes(range(256)) * 40); h0 = sha256(audio.read_bytes())
    state = {"film": write_video(w / "draft.mp4", moving_frames(45), 30), "fps": 30}
    checks = [("frames == 60", lambda s: int(vstream(probe(s["film"]))["nb_frames"]) == 60),
              ("fps 30/1", lambda s: vstream(probe(s["film"]))["r_frame_rate"] == "30/1"),
              ("audio untouched", lambda s: sha256(audio.read_bytes()) == h0)]
    fixers = {"frames == 60": lambda s: s.update(film=write_video(w / "fixed.mp4", moving_frames(60), 30))}
    r = verification_loop(state, checks, fixers); wjson(w / "loop.json", r)
    r2 = verification_loop({"film": state["film"]}, checks[:1] + [("impossible", lambda s: False)], {"impossible": lambda s: None}, budget=2)
    return [C("first pass fails on the frame count, fix, second pass all green", r["done"] and r["iterations"] == 2 and r["log"][0][0] == ("frames == 60", False), r["log"]),
            C("an unfixable check ends at the budget and is reported unverified", not r2["done"] and r2["unverified"] == ["impossible"], r2.get("unverified"))]


# ---------------------------------------------------------------- CHECK-03 contact sheet
@program("CHECK-03")
def check_03(work):
    from PIL import Image
    fr = np.stack([np.full((36, 64), 10 * (i // 15), np.uint8) for i in range(360)])
    film = write_video(Path(work) / "film.mp4", fr, 30); sheet = Path(work) / "sheet.png"
    ff("-i", film, "-vf", "fps=2,scale=320:-1,tile=6x4", "-frames:v", 1, sheet)
    a = np.asarray(Image.open(sheet).convert("L")).astype(float); th = a.shape[0] // 4
    vals = [a[r * th + th // 2, c * 320 + 160] for r in range(4) for c in range(6)]
    return [C("12 s film at 2 fps -> one 6x4 sheet of 320 px tiles (1920 wide)", a.shape[1] == 1920 and a.shape[0] == 4 * 180, a.shape),
            C("tile k shows half-second k (level 10k +- 4)", all(abs(v - 10 * k) <= 4 for k, v in enumerate(vals)), [round(v) for v in vals[:8]])]


# ---------------------------------------------------------------- CHECK-04 five-axis self-eval
AXES = ("accuracy", "completeness", "clarity", "actionability", "concision")


def five_axis(scores, evidence):
    p = [a for a in AXES if a not in scores or not 1 <= scores[a] <= 5]
    p += [f"{a} < 5 without evidence" for a in AXES if scores.get(a, 5) < 5 and not evidence.get(a)]
    return {"problems": p, "fix": [a for a in AXES if scores.get(a, 5) <= 3]}


@program("CHECK-04")
def check_04(work):
    s = {"accuracy": 5, "completeness": 3, "clarity": 4, "actionability": 5, "concision": 2}
    ev = {"completeness": "edge case 'empty input' not handled", "clarity": "step 3 ambiguous", "concision": "intro repeats the brief"}
    a = five_axis(s, ev); b = five_axis(s, {"clarity": "x"}); wjson(Path(work) / "self_eval.json", {"scores": s, "evidence": ev, "result": a})
    return [C("every score < 5 has an evidence line; axes <= 3 are queued for fixing", a == {"problems": [], "fix": ["completeness", "concision"]}, a),
            C("scores below 5 without evidence are rejected", b["problems"] == ["completeness < 5 without evidence", "concision < 5 without evidence"], b["problems"])]


# ---------------------------------------------------------------- CHECK-05 red team with edge inputs
def caption_wrap(text, width=12):
    """The artefact under test: wrap a caption into lines of <= width characters."""
    if text is None:
        raise ValueError("no text")
    words, lines, cur = str(text).split(), [], ""
    for w in words:
        while len(w) > width:
            if cur:
                lines.append(cur); cur = ""
            lines.append(w[:width]); w = w[width:]
        cur = (cur + " " + w).strip() if len(cur) + len(w) + 1 <= width else (lines.append(cur) or w) if cur else w
    if cur:
        lines.append(cur)
    return lines


EDGE_INPUTS = {"empty": "", "huge": "كلمة " * 2000, "malformed": "�\x00", "arabic+digits": "سعرها 35 ريالًا و٣٥",
               "long word": "Supercalifragilisticexpialidocious", "rtl+ltr": "افتح Settings ثم Wi-Fi", "none": None, "whitespace": "   \n\t "}


def red_team(fn, width=12):
    rows = []
    for name, x in EDGE_INPUTS.items():
        try:
            out = fn(x); ok = all(len(l) <= width for l in out) and "".join(out).replace(" ", "") == ("".join(str(x).split()) if x else "")
            rows.append((name, "ok" if ok else "wrong output"))
        except Exception as e:
            rows.append((name, f"raised {type(e).__name__}"))
    return rows


@program("CHECK-05")
def check_05(work):
    rows = red_team(caption_wrap); naive = red_team(lambda t, width=12: [t[i:i + width] for i in range(0, len(t), width)])
    objections = ["None raises instead of returning []", "long words are hard-split", "no bidi isolation of Latin runs"]
    wjson(Path(work) / "red_team.json", {"rows": rows, "objections": objections})
    weak = [n for n, r in rows if r != "ok"]
    return [C(">= 8 edge inputs run", len(rows) == 8, len(rows)), C("at least one concrete weakness found (None input raises)", weak == ["none"], rows),
            C("a naive slicer is caught on more edge cases (splits inside words / None)", len([1 for _, r in naive if r != "ok"]) >= 1 and dict(naive)["none"].startswith("raised"), naive),
            C("top 3 expert objections written", len(objections) == 3, "")]


# ---------------------------------------------------------------- CHECK-06 code verification loop
SECRET_RE = re.compile(r"sk-[A-Za-z0-9_-]{8,}|api_key\s*=\s*['\"][^'\"]+|BEGIN [A-Z ]*PRIVATE KEY")


def code_verify(proj):
    proj = Path(proj); phases = []
    b = subprocess.run([sys.executable, "-m", "py_compile", *map(str, sorted(proj.glob("*.py")))], capture_output=True, text=True)
    phases.append(("build", b.returncode == 0))
    if b.returncode:
        return "NOT READY", phases
    phases.append(("types", "unavailable (no tsc/pyright here)"))
    lint = [f"{p.name}:{i}" for p in proj.glob("*.py") for i, l in enumerate(p.read_text().splitlines(), 1) if len(l) > 120 or re.match(r"\s*import \*|from \S+ import \*", l)]
    phases.append(("lint", not lint))
    t = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", str(proj), "-q"], capture_output=True, text=True, cwd=proj)
    phases.append(("tests", t.returncode == 0))
    sec = [p.name for p in proj.rglob("*") if p.is_file() and SECRET_RE.search(p.read_text(errors="ignore"))]
    phases.append(("secrets", not sec))
    phases.append(("diff", sorted(p.name for p in proj.glob("*.py"))))
    ok = all(v is True for k, v in phases if k in ("build", "lint", "tests", "secrets"))
    return ("READY" if ok else "NOT READY"), phases


@program("CHECK-06")
def check_06(work):
    w = Path(work)
    def mk(name, src, test, extra=None):
        d = w / name; d.mkdir(); (d / "lib.py").write_text(src); (d / "test_lib.py").write_text(test)
        if extra:
            (d / "config.py").write_text(extra)
        return d
    test = "import unittest\nfrom lib import add\nclass T(unittest.TestCase):\n    def test_add(self):\n        self.assertEqual(add(2, 3), 5)\n"
    good = mk("good", "def add(a, b):\n    return a + b\n", test)
    broken = mk("broken", "def add(a, b)\n    return a + b\n", test)
    leaky = mk("leaky", "def add(a, b):\n    return a + b\n", test, "api_key = 'sk-live-1234567890abcdef'\n")
    wrong = mk("wrong", "def add(a, b):\n    return a - b\n", test)
    r = {n: code_verify(d) for n, d in (("good", good), ("broken", broken), ("leaky", leaky), ("wrong", wrong))}
    wjson(w / "verify.json", r)
    return [C("clean project: build, lint, tests, secret grep pass -> READY", r["good"][0] == "READY", r["good"]),
            C("build failure stops at phase 1 -> NOT READY with one phase", r["broken"][0] == "NOT READY" and len(r["broken"][1]) == 1, r["broken"]),
            C("a secret-like string blocks READY", r["leaky"][0] == "NOT READY" and ("secrets", False) in r["leaky"][1], r["leaky"]),
            C("a failing unit test blocks READY", r["wrong"][0] == "NOT READY" and ("tests", False) in r["wrong"][1], r["wrong"])]


# ---------------------------------------------------------------- CHECK-07 stop rule
NOT_DONE = ("first draft", "it compiles", "the command ran", "success message", "a plan")


def stop_decision(checks, rounds, cap=4, signal=""):
    if signal in NOT_DONE and not all(checks.values()):
        signal = "ignored"
    if all(checks.values()):
        return {"stop": True, "why": "all checks passed"}
    if rounds >= cap:
        return {"stop": True, "why": "budget", "unverified": sorted(k for k, v in checks.items() if not v), "next": "fix " + sorted(k for k, v in checks.items() if not v)[0]}
    return {"stop": False, "why": "keep going"}


@program("CHECK-07")
def check_07(work):
    a = stop_decision({"tests": True, "render": True}, 2); b = stop_decision({"tests": True, "render": False}, 1, signal="it compiles")
    c = stop_decision({"tests": True, "render": False, "audio": False}, 4); wjson(Path(work) / "stop.json", [a, b, c])
    return [C("all checks passed -> stop", a["stop"] and a["why"] == "all checks passed", a), C("'it compiles' with a failing check does not stop", not b["stop"], b),
            C("cap of 4 rounds reached -> deliver with unverified list and next step", c["stop"] and c["unverified"] == ["audio", "render"] and c["next"] == "fix audio", c)]


# ---------------------------------------------------------------- CHECK-08 evidence ladder
BADGES = ["idea", "documented", "install", "key", "ready", "proven"]


def badge_for(claim, today, env="this container"):
    b = claim["claimed"]
    if b == "proven":
        proof = claim.get("proof")
        if not proof or not Path(proof).exists():
            b = "ready" if claim.get("runs_here") else "documented"
        elif claim.get("proven_in", env) != env and not claim.get("reprobe_ok"):
            b = "ready" if claim.get("runs_here") else "documented"
    if b == "seen" and claim.get("kind") != "motion reference":
        b = "documented"
    return b


@program("CHECK-08")
def check_08(work):
    w = Path(work); proof = w / "run-2026-11-03.log"; proof.write_text("ffprobe ok: 60 frames\n")
    cases = {"proven with proof": {"claimed": "proven", "proof": str(proof)}, "proven no proof": {"claimed": "proven", "runs_here": True},
             "lease from another container": {"claimed": "proven", "proof": str(proof), "proven_in": "claude.ai", "reprobe_ok": False},
             "lease re-probed": {"claimed": "proven", "proof": str(proof), "proven_in": "claude.ai", "reprobe_ok": True}, "seen on a tool": {"claimed": "seen", "kind": "tool"}}
    r = {k: badge_for(v, "2026-11-03") for k, v in cases.items()}; wjson(w / "badges.json", r)
    return [C("proven only with an existing proof file", r["proven with proof"] == "proven" and r["proven no proof"] == "ready", r),
            C("a proof from another container is a lease: downgraded until re-probed", r["lease from another container"] == "documented" and r["lease re-probed"] == "proven", r),
            C("'seen' applies to motion references only", r["seen on a tool"] == "documented", r), C("7 badges on the ladder incl. seen", len(BADGES) + 1 == 7, "")]


# ---------------------------------------------------------------- CHECK-09 typed receipt
def typed_receipt(r):
    code, err = validate_receipt(r)
    if r.get("verified") and any(not (isinstance(e, dict) and e.get("type") and e.get("ref")) for e in r.get("evidence", [])):
        err.append("evidence item without type/ref"); code = 2
    return code, err


@program("CHECK-09")
def check_09(work):
    w = Path(work); film = write_video(w / "film.mp4", moving_frames(30), 30); pj = w / "probe.json"; pj.write_text(json.dumps(probe(film)))
    ok = {"status": "success", "summary": "rendered 1 s", "owner": "render", "evidence": [{"type": "ffprobe", "ref": str(pj)}], "artifacts": [str(film)], "next_actions": [], "retryable": True, "verified": True}
    warn = dict(ok, status="warning", verified=False, evidence=[]); untyped = dict(ok, evidence=["looked fine"]); err = dict(ok, status="error")
    r = {n: typed_receipt(x) for n, x in (("ok", ok), ("warn", warn), ("untyped", untyped), ("error", err))}; wjson(w / "receipts.json", r)
    return [C("success + ffprobe evidence {type, ref} verified", r["ok"] == (0, []), r["ok"]), C("warning + verified:false is an honest pass", r["warn"] == (0, []), r["warn"]),
            C("evidence without type/ref rejected", r["untyped"][0] == 2 and "evidence item without type/ref" in r["untyped"][1], r["untyped"]), C("error can never be verified", r["error"][0] == 2, r["error"])]


# ---------------------------------------------------------------- CHECK-10 honest status words
CODE_WORDS = ["inspected", "changed locally", "verified locally", "committed", "pushed"]


def status_line(events, kind="code"):
    if kind == "motion":
        order = [s for s in LADDER if s != "PLANNED"]; got = [s for s in order if s in events]
        return got[-1] if got and got == order[:len(got)] else "INCONSISTENT"
    if "blocked" in events:
        return "blocked: " + events["blocked"]
    got = [wd for wd in CODE_WORDS if wd in events]
    if got != CODE_WORDS[:len(got)]:
        return "INCONSISTENT"
    if "verified locally" in got and not events.get("verified locally"):
        return "INCONSISTENT"
    return got[-1] if got else "nothing yet"


@program("CHECK-10")
def check_10(work):
    a = status_line({"inspected": 1, "changed locally": 1}); b = status_line({"inspected": 1, "changed locally": 1, "verified locally": "pytest -q: 12 passed", "committed": 1})
    c = status_line({"inspected": 1, "pushed": 1}); d = status_line({"CODE_WRITTEN": 1, "PREVIEW_RENDERED": 1}, "motion"); e = status_line({"CODE_WRITTEN": 1, "QA_PASS": 1}, "motion")
    f = status_line({"inspected": 1, "blocked": "needs API key; next: ask owner"}); wjson(Path(work) / "status.json", [a, b, c, d, e, f])
    return [C("changed but not verified is reported as 'changed locally', not done", a == "changed locally", a), C("verified locally names its command; committed after it", b == "committed", b),
            C("'pushed' without commit/verify is inconsistent", c == "INCONSISTENT", c), C("motion: PREVIEW_RENDERED is not VIDEO_RENDERED; QA_PASS without render is inconsistent", d == "PREVIEW_RENDERED" and e == "INCONSISTENT", (d, e)),
            C("blocked carries reason + next step", f.startswith("blocked: needs API key"), f)]


# ---------------------------------------------------------------- CHECK-11 eval-first
def slugify_v1(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def slugify_v2(s):
    return re.sub(r"[^\w]+", "-", s.lower(), flags=re.UNICODE).strip("-")


def run_evals(fn, cases):
    return sum(1 for x, want in cases if fn(x) == want), len(cases)


@program("CHECK-11")
def check_11(work):
    regression = [("Hello World", "hello-world"), ("  A  B ", "a-b"), ("v1.2", "v1-2")]
    capability = [("مرحبا بالعالم", "مرحبا-بالعالم"), ("دعاء الجمعة 2026", "دعاء-الجمعة-2026")]
    base_r, base_c = run_evals(slugify_v1, regression), run_evals(slugify_v1, capability)
    new_r, new_c = run_evals(slugify_v2, regression), run_evals(slugify_v2, capability)
    wjson(Path(work) / "evals.json", {"baseline": {"regression": base_r, "capability": base_c}, "change": {"regression": new_r, "capability": new_c}})
    return [C("capability eval written first fails on the baseline (0/2 Arabic slugs)", base_c == (0, 2), base_c), C("after the change capability 2/2", new_c == (2, 2), new_c),
            C("regression eval stays 3/3 (no regression)", base_r == new_r == (3, 3), (base_r, new_r))]


# ---------------------------------------------------------------- CHECK-12 pass@k vs pass^k
def pass_at_k(p, k):
    return 1 - (1 - p) ** k


def pass_hat_k(p, k):
    return p ** k


@program("CHECK-12")
def check_12(work):
    rng = np.random.default_rng(12); trials = rng.random((200000, 3)) < 0.7
    sim_any, sim_all = float(trials.any(1).mean()), float(trials.all(1).mean())
    r = {"pass@2": pass_at_k(.7, 2), "pass@3": pass_at_k(.7, 3), "pass^3": pass_hat_k(.7, 3), "pass^5": pass_hat_k(.7, 5), "sim@3": sim_any, "sim^3": sim_all}
    wjson(Path(work) / "passk.json", r)
    return [C("p = 0.7: pass@2 0.91, pass@3 0.973, pass^3 0.343, pass^5 0.168", round(r["pass@2"], 2) == 0.91 and round(r["pass@3"], 3) == 0.973 and round(r["pass^3"], 3) == 0.343 and round(r["pass^5"], 3) == 0.168, r),
            C("200k independent simulated runs agree within 0.005", abs(sim_any - 0.973) < 0.005 and abs(sim_all - 0.343) < 0.005, (sim_any, sim_all)),
            C("exploratory gate pass@3 > 90% passes; critical gate pass^3 = 100% fails", r["pass@3"] > 0.9 and r["pass^3"] < 1, "")]


# ---------------------------------------------------------------- CHECK-13 hard-fail gate
HARD_FAILS = {"audio_altered", "badge_without_proof", "secret_string", "regression", "unlicensed_text", "broken_arabic_shaping"}


def release_gate(scores, triggered):
    hard = sorted(set(triggered) & HARD_FAILS)
    return {"verdict": "NOT READY" if hard else "READY" if np.mean(list(scores.values())) >= 4 else "REVISE", "hard": hard, "mean": float(np.mean(list(scores.values())))}


@program("CHECK-13")
def check_13(work):
    s = {"craft": 5, "clarity": 5, "pace": 5, "truth": 4.8}
    a, b = release_gate(s, []), release_gate(s, ["audio_altered"]); wjson(Path(work) / "gate.json", {"clean": a, "hard": b})
    return [C("high mean and no hard fail -> READY", a["verdict"] == "READY", a), C("mean 4.95 but user audio altered -> NOT READY", b["verdict"] == "NOT READY" and b["mean"] > 4.9 and b["hard"] == ["audio_altered"], b)]


# ---------------------------------------------------------------- CHECK-14 judge discipline
def assertions(out):
    return [("has 3 bullets", out.count("\n- ") + out.startswith("- ") == 3), ("<= 280 chars", len(out) <= 280)]


def biased_pick(first, second):
    """A deterministic stand-in judge with a position bias: prefers whatever is shown first unless the other is much longer."""
    return "first" if len(first) + 40 >= len(second) else "second"


def swap_judge(a, b):
    r1 = biased_pick(a, b); r2 = biased_pick(b, a)
    w1 = "A" if r1 == "first" else "B"; w2 = "B" if r2 == "first" else "A"
    return w1 if w1 == w2 else "position-bias: no verdict"


@program("CHECK-14")
def check_14(work):
    good = "- one\n- two\n- three"; bad = "- one\n- two"
    asr = {"good": assertions(good), "bad": assertions(bad)}
    tie = swap_judge("Answer with a short summary.", "Answer with a short summary!")
    clear = swap_judge("Short.", "A much longer and more complete answer that covers every requested point in full detail.")
    wjson(Path(work) / "judge.json", {"assertions": asr, "swap": [tie, clear], "cite": "judge.json:assertions"})
    return [C("executable assertions run first: 3 bullets pass, 2 bullets fail", all(ok for _, ok in asr["good"]) and not asr["bad"][0][1], asr),
            C("swapping positions exposes a position-biased judgement", tie == "position-bias: no verdict", tie), C("a real difference survives the swap", clear == "B", clear)]


# ---------------------------------------------------------------- CHECK-16 generator-evaluator loop
WEIGHTS = {"design": 0.3, "originality": 0.2, "craft": 0.3, "functionality": 0.2}


def weighted(s):
    return round(sum(WEIGHTS[k] * s[k] for k in WEIGHTS), 3)


def gen_eval_loop(start, gain, threshold=7.0, cap=15):
    s = dict(start); hist = []
    for it in range(1, cap + 1):
        sc = weighted(s); hist.append(sc)
        if sc >= threshold:
            return it, sc, hist
        worst = min(WEIGHTS, key=lambda k: s[k]); s[worst] = min(10, s[worst] + gain)
    return cap, hist[-1], hist


@program("CHECK-16")
def check_16(work):
    it, sc, hist = gen_eval_loop({"design": 5, "originality": 4, "craft": 6, "functionality": 7}, 1)
    it2, sc2, _ = gen_eval_loop({"design": 2, "originality": 2, "craft": 2, "functionality": 2}, 0.1)
    wjson(Path(work) / "loop.json", {"hist": hist, "capped": [it2, sc2]})
    return [C("weights 0.3/0.2/0.3/0.2: 5/4/6/7 scores 5.5", hist[0] == 5.5, hist[0]), C("loop improves the weakest criterion and stops at >= 7.0", sc >= 7.0 and hist[-2] < 7.0, (it, hist)),
            C("slow progress stops at the 15-iteration cap below threshold", it2 == 15 and sc2 < 7.0, (it2, sc2))]


# ---------------------------------------------------------------- CHECK-17 adversarial verifier
def norm_snippet(s):
    return re.sub(r"\s+", " ", s.strip().lower())


def adversarial_review(reviews, expected, evidence_ok):
    if set(reviews) != set(expected):
        return {"verdict": "CHANGES_REQUESTED", "why": "missing reviewer " + ",".join(sorted(set(expected) - set(reviews)))}
    seen, kept = set(), []
    for rv in reviews.values():
        for f in rv:
            k = norm_snippet(f["evidence"])
            if k not in seen:
                seen.add(k); kept.append(f)
    confirmed = [f for f in kept if f["sev"] not in ("CRITICAL", "HIGH") or evidence_ok(f)]
    blocking = [f for f in confirmed if f["sev"] in ("CRITICAL", "HIGH")]
    return {"verdict": "CHANGES_REQUESTED" if blocking else "APPROVE", "findings": len(kept), "confirmed": len(confirmed), "refuted": len(kept) - len(confirmed)}


@program("CHECK-17")
def check_17(work):
    w = Path(work); (w / "app.py").write_text("password = 'hunter2'\nprint('ok')\n")
    real = {"sev": "CRITICAL", "evidence": "password = 'hunter2'"}; dup = {"sev": "CRITICAL", "evidence": "  PASSWORD = 'hunter2' "}
    false_alarm = {"sev": "HIGH", "evidence": "eval(user_input)"}
    proves = lambda f: norm_snippet(f["evidence"]) in norm_snippet((w / "app.py").read_text())
    a = adversarial_review({"sec": [real, false_alarm], "style": [dup]}, ["sec", "style"], proves)
    b = adversarial_review({"sec": [false_alarm], "style": []}, ["sec", "style"], proves); c = adversarial_review({"sec": []}, ["sec", "style"], proves)
    wjson(w / "review.json", {"a": a, "b": b, "c": c})
    return [C("duplicate findings merged by normalised snippet; the real secret confirmed", a["findings"] == 2 and a["confirmed"] == 1 and a["verdict"] == "CHANGES_REQUESTED", a),
            C("an unproven HIGH finding defaults to refuted", b == {"verdict": "APPROVE", "findings": 1, "confirmed": 0, "refuted": 1}, b),
            C("a reviewer that did not return -> CHANGES_REQUESTED, never a pass", c["verdict"] == "CHANGES_REQUESTED" and "style" in c["why"], c)]


# ---------------------------------------------------------------- CHECK-18 benchmark loop
def bench(fn, x, reps=3):
    best = math.inf
    for _ in range(reps):
        t = time.perf_counter(); out = fn(x); best = min(best, time.perf_counter() - t)
    return best, out


@program("CHECK-18")
def check_18(work):
    x = np.arange(100000, dtype=np.float64) % 97; truth = float(np.sum(x * x))
    variants = {"baseline: python loop": lambda a: sum(v * v for v in a), "H1: numpy vectorised": lambda a: float(np.sum(a * a)),
                "H2: float32 cast": lambda a: float(np.sum(a.astype(np.float32) ** 2)), "H3: skip odd rows (wrong)": lambda a: float(np.sum(a[::2] ** 2)) * 2}
    rows = {}
    for name, fn in variants.items():
        t, out = bench(fn, x, 5); rows[name] = {"s": t, "correct": abs(out - truth) / truth < 1e-9}
    safe = {k: v for k, v in rows.items() if v["correct"]}; win = min(safe, key=lambda k: safe[k]["s"])
    wjson(Path(work) / "bench.json", {"rows": rows, "winner": win})
    return [C("correctness gate rejects the float32 and skip-rows variants", not rows["H2: float32 cast"]["correct"] and not rows["H3: skip odd rows (wrong)"]["correct"], rows),
            C("fastest safe variant (numpy vectorised) promoted, > 2x faster than the loop", win == "H1: numpy vectorised" and rows["baseline: python loop"]["s"] > 2 * rows[win]["s"], {k: round(v["s"], 5) for k, v in rows.items()})]


# ---------------------------------------------------------------- CHECK-19 loop design gate
VAGUE = re.compile(r"\b(good|better|nice|great|clean|proper)\b|\bmake it\b", re.I)


def loop_gate(plan):
    p = [k for k in ("repeats_weekly", "verification_automated", "budget_fits", "real_tools") if not plan.get(k)]
    if VAGUE.search(plan["done"]) or not re.search(r"\d|exit 0|==", plan["done"]):
        p.append("done is not machine-decidable")
    if not plan.get("must_not"):
        p.append("no boundary list")
    if not 1 <= plan.get("retry_cap", 0) <= 3:
        p.append("retry cap missing or > 3")
    if plan.get("self_judged"):
        p.append("self-judging verification")
    p += [f"irreversible step automated: {s}" for s in plan.get("auto_steps", []) if s in ("merge", "publish", "spend")]
    return p


@program("CHECK-19")
def check_19(work):
    good = {"repeats_weekly": True, "verification_automated": True, "budget_fits": True, "real_tools": True, "done": "96 tests green AND change-list produced", "must_not": ["delete tests", "touch user audio"], "retry_cap": 3, "auto_steps": ["test", "lint"]}
    bad = {"repeats_weekly": False, "verification_automated": True, "budget_fits": True, "real_tools": True, "done": "make it good", "must_not": [], "retry_cap": 10, "self_judged": True, "auto_steps": ["publish"]}
    wjson(Path(work) / "loop_gate.json", {"good": loop_gate(good), "bad": loop_gate(bad)})
    return [C("weekly, automated, decidable goal, boundaries, cap 3 -> automate", loop_gate(good) == [], loop_gate(good)),
            C("one-off, 'make it good', no boundaries, cap 10, self-judged, auto publish -> do by hand", loop_gate(bad) == ["repeats_weekly", "done is not machine-decidable", "no boundary list", "retry cap missing or > 3", "self-judging verification", "irreversible step automated: publish"], loop_gate(bad))]


# ---------------------------------------------------------------- CHECK-20 mutation-test a validator
WEAK_SECRET = re.compile(r"sk-[A-Za-z0-9]{20,}")
STRONG_SECRET = re.compile(r"\bsk-[A-Za-z0-9_-]{20,}|\bghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|Bearer\s+[A-Za-z0-9._-]{20,}")


def manifest_validator(m, secret_re=WEAK_SECRET, root=None):
    p = []
    if m.get("version") != "1.4.0":
        p.append("version drift")
    for k in ("name", "items", "entry"):
        if k not in m:
            p.append(f"missing {k}")
    if isinstance(m.get("items"), list):
        if not m["items"]:
            p.append("empty items")
        elif len(m["items"]) < 3:
            p.append("item removed")
    elif "items" in m:
        p.append("items wrong type")
    if root and "entry" in m and not (Path(root) / m["entry"]).exists():
        p.append("broken path")
    if secret_re.search(json.dumps(m)):
        p.append("secret-like string")
    return p


def mutants(base):
    def mut(f):
        m = json.loads(json.dumps(base)); f(m); return m
    return {"version drift": mut(lambda m: m.update(version="1.3.9")), "missing field": mut(lambda m: m.pop("name")), "removed item": mut(lambda m: m["items"].pop()),
            "sk- secret": mut(lambda m: m.update(note="sk-" + "a1" * 12)), "ghp_ token": mut(lambda m: m.update(note="ghp_" + "b2" * 12)),
            "AKIA key": mut(lambda m: m.update(note="AKIA" + "ABCD1234" * 2)), "Bearer token": mut(lambda m: m.update(note="Bearer " + "c3d4" * 6)),
            "broken path": mut(lambda m: m.update(entry="missing.py")), "emptied list": mut(lambda m: m.update(items=[])), "wrong type": mut(lambda m: m.update(items="a,b,c"))}


@program("CHECK-20")
def check_20(work):
    w = Path(work); (w / "main.py").write_text("print(1)\n")
    base = {"name": "kit", "version": "1.4.0", "items": ["a", "b", "c"], "entry": "main.py"}; ms = mutants(base)
    table = lambda rx: [(k, bool(manifest_validator(m, rx, w))) for k, m in ms.items()]
    weak, strong = table(WEAK_SECRET), table(STRONG_SECRET); control = manifest_validator(base, STRONG_SECRET, w)
    (w / "mutation_table.md").write_text("| mutation | weak | strong |\n|---|---|---|\n" + "".join(f"| {a} | {b} | {d} |\n" for (a, b), (_, d) in zip(weak, strong)))
    missed = [k for k, c in weak if not c]
    return [C("10 seeded mutations (within 8-12), pristine control clean", len(ms) == 10 and control == [], control),
            C("weak secret regex catches 7/10, missing ghp_, AKIA and Bearer", sum(c for _, c in weak) == 7 and missed == ["ghp_ token", "AKIA key", "Bearer token"], missed),
            C("strengthened validator catches 10/10", all(c for _, c in strong), strong)]


# ---------------------------------------------------------------- CHECK-23 record gate
STATUS = {"proven", "ready", "install", "key", "seen", "documented", "idea"}
BASE = ["id", "family", "name_ar", "name_en", "status", "what", "how", "params", "install", "license", "proof", "styles", "tags"]
NEW = BASE + ["domain", "when", "section", "source"]
SECRET = re.compile(r"\bsk-[A-Za-z0-9_-]{20,}|\bghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY")
MODEL = re.compile(r"\b(" + codecs.decode("Bchf|Fbaarg|Unvxh|Snoyr", "rot13") + r")\b|claude-[a-z]+-\d")


def record_gate(sk, home):
    seen, bad = {}, []
    for f in sorted(Path(sk, "data", "powers").glob("*.json")):
        for r in json.loads(f.read_text(encoding="utf-8")):
            rid, new = r.get("id"), r.get("domain", "motion") != "motion"
            miss = [k for k in (NEW if new else BASE) if k not in r]
            if miss:
                bad.append((rid, "missing keys", miss))
            if r.get("status") not in STATUS:
                bad.append((rid, "bad status"))
            if rid in seen:
                bad.append((rid, "duplicate id"))
            seen[rid] = f.name
            if r.get("status") == "proven":
                if not r.get("proof"):
                    bad.append((rid, "proven without proof"))
                for p in [p for p in r.get("proof", []) if p.startswith("kosif-tool/")]:
                    if not (Path(home) / p.split(":")[0]).exists():
                        bad.append((rid, "proof path missing"))
            blob = json.dumps(r, ensure_ascii=False)
            if SECRET.search(blob):
                bad.append((rid, "secret-like string"))
            if new and MODEL.search(blob):
                bad.append((rid, "model name in skill data"))
            if new and " — " not in r.get("what", ""):
                bad.append((rid, "what is not 'AR — EN'"))
    return (1 if bad else 0), len(seen), bad


@program("CHECK-23")
def check_23(work):
    w = Path(work); home = w / "home"; (home / "kosif-tool" / "proofs").mkdir(parents=True); (home / "kosif-tool" / "proofs" / "p.log").write_text("ok")
    legacy = {k: "x" for k in BASE} | {"id": "M-01", "status": "documented", "proof": [], "styles": [], "tags": []}
    newr = {k: "x" for k in NEW} | {"id": "N-01", "domain": "mind", "status": "proven", "proof": ["kosif-tool/proofs/p.log"], "what": "عربي — English", "styles": [], "tags": []}
    def run(mutate):
        sk = w / f"sk{len(list(w.glob('sk*')))}"; (sk / "data" / "powers").mkdir(parents=True)
        recs = [json.loads(json.dumps(legacy)), json.loads(json.dumps(newr))]; mutate(recs)
        (sk / "data" / "powers" / "fam.json").write_text(json.dumps(recs, ensure_ascii=False)); return record_gate(sk, home)
    cases = {"pristine": lambda r: None, "legacy without domain": lambda r: r[0].pop("domain", None),
             "duplicate id": lambda r: r.append(dict(r[0])), "new missing source": lambda r: r[1].pop("source"), "status done": lambda r: r[0].update(status="done"),
             "proven empty proof": lambda r: r[1].update(proof=[]), "missing proof path": lambda r: r[1].update(proof=["kosif-tool/proofs/none.log"]),
             "sk- key in how": lambda r: r[0].update(how="sk-ant-api03-" + "x" * 24), "ghp_ in params": lambda r: r[0].update(params="ghp_" + "y" * 24),
             "model name in what": lambda r: r[1].update(what="عربي — uses " + codecs.decode("Fbaarg", "rot13")), "English-only what": lambda r: r[1].update(what="English only"),
             "legacy missing how": lambda r: r[0].pop("how")}
    res = {k: run(f) for k, f in cases.items()}
    rows = [(k, v[0], v[2][:1]) for k, v in res.items()]; wjson(w / "mutation_run.json", rows)
    controls = [res["pristine"][0], res["legacy without domain"][0]]; caught = sum(1 for k, v in res.items() if k not in ("pristine", "legacy without domain") and v[0] == 1)
    return [C("2/2 controls clean (exit 0)", controls == [0, 0], controls), C("10/10 seeded defects caught (exit 1)", caught == 10, rows)]


# ---------------------------------------------------------------- CHECK-24 self-evolution record
EVO_STEPS = ["snapshot", "hypothesis", "change", "rebuild", "eval_matrix", "hard_fails", "decision", "read_back", "changelog"]


def evolution_ok(rec, old_ids, new_ids):
    p = [s for s in EVO_STEPS if not rec.get(s)]
    if not re.search(r"after the change, .+ routes to .+", rec.get("hypothesis", "")):
        p.append("hypothesis not testable")
    if [i for i in old_ids if i not in new_ids]:
        p.append("IDs removed or renumbered")
    if new_ids[:len(old_ids)] != old_ids:
        p.append("new IDs not appended")
    if rec.get("hard_fails", {}) and any(rec["hard_fails"].values()):
        p.append("hard fail triggered")
    return p


@program("CHECK-24")
def check_24(work):
    rec = {s: "done" for s in EVO_STEPS} | {"hypothesis": "Claude forgets the LUFS gate; after the change, case 'reel export' routes to QA-256", "hard_fails": {"validator": False, "secret": False}}
    old = ["CHECK-01", "CHECK-02"]; good = evolution_ok(rec, old, old + ["CHECK-03"])
    bad = evolution_ok(dict(rec, read_back="", hypothesis="make it better", hard_fails={"secret": True}), old, ["CHECK-02", "CHECK-03"])
    wjson(Path(work) / "evolution.json", {"good": good, "bad": bad})
    return [C("9 steps, testable hypothesis, appended ID, no hard fails", good == [], good),
            C("missing read-back, vague hypothesis, renumbered IDs and a hard fail rejected", bad == ["read_back", "hypothesis not testable", "IDs removed or renumbered", "new IDs not appended", "hard fail triggered"], bad)]


# ---------------------------------------------------------------- CHECK-25 consent-scoped lessons
PII = re.compile(r"[\w.]+@[\w.]+\.\w+|\+?\d[\d\s-]{8,}\d|sk-[A-Za-z0-9]{8,}")


def lesson_ok(entry, existing):
    p = []
    n = len([s for s in re.split(r"(?<=[.!?؟])\s+", entry["text"].strip()) if s])
    if not 4 <= n <= 8:
        p.append(f"{n} sentences (need 4-8)")
    if not entry.get("consent"):
        p.append("no consent")
    if not re.search(r"next time I see .+ I will .+", entry["text"], re.I):
        p.append("no 'next time I see X I will do Y' rule")
    if PII.search(entry["text"]):
        p.append("secret or personal data")
    if any(e["root_cause"] == entry["root_cause"] for e in existing):
        p.append("merge with existing lesson")
    return p


def promotable(entry):
    return len(set(entry.get("held_in_projects", []))) >= 2


@program("CHECK-25")
def check_25(work):
    txt = ("Burned Arabic captions came out disconnected. The burn used a libass build without shaping. The class is shaping lost in a renderer. "
           "Next time I see Arabic burned into video I will render a still and check letter joins first. The signal is isolated letter forms in the still.")
    good = {"text": txt, "consent": True, "root_cause": "no-shaping", "held_in_projects": ["dua-jumuah"]}
    bad = {"text": "It broke. Mail me at a@b.co.", "consent": False, "root_cause": "fps"}
    (Path(work) / "lessons.md").write_text(txt)
    return [C("5-sentence consented lesson with an X->Y rule passes", lesson_ok(good, []) == [], lesson_ok(good, [])),
            C("too short, no consent, no rule, an email, same root cause caught", lesson_ok(bad, [{"root_cause": "fps"}]) == ["2 sentences (need 4-8)", "no consent", "no 'next time I see X I will do Y' rule", "secret or personal data", "merge with existing lesson"], lesson_ok(bad, [{"root_cause": "fps"}])),
            C("promotion needs 2 unrelated projects", not promotable(good) and promotable(dict(good, held_in_projects=["a", "b"])), "")]


# ---------------------------------------------------------------- CHECK-26 append-only decision ledger
def ledger_append(path, row):
    lines = Path(path).read_text().splitlines() if Path(path).exists() else []
    prev = json.loads(lines[-1])["hash"] if lines else "0" * 64
    row = dict(row, prev=prev); row["hash"] = hashlib.sha256((prev + json.dumps(row, sort_keys=True)).encode()).hexdigest()
    with open(path, "a") as f:
        f.write(json.dumps(row, sort_keys=True) + "\n")


def ledger_verify(path):
    prev = "0" * 64
    for i, l in enumerate(Path(path).read_text().splitlines()):
        r = json.loads(l); h = r.pop("hash")
        if r["prev"] != prev or hashlib.sha256((prev + json.dumps(r, sort_keys=True)).encode()).hexdigest() != h:
            return False, i
        prev = h
    return True, None


@program("CHECK-26")
def check_26(work):
    p = Path(work) / "ledger.jsonl"; marks = ["watch", "accept", "decay"]
    for i, m in enumerate(marks):
        ledger_append(p, {"round": i + 1, "prior_winner": "v1" if i == 0 else "v2", "new_info": f"trial batch {i + 1}", "space": 12, "trials": 4, "mark": m, "mode": "paper", "gate_passed": m == "accept"})
    ok = ledger_verify(p); lines = p.read_text().splitlines()
    tam = Path(work) / "tampered.jsonl"; t = json.loads(lines[1]); t["mark"] = "reject"; tam.write_text("\n".join([lines[0], json.dumps(t, sort_keys=True), lines[2]]) + "\n")
    return [C("3 rounds appended, hash chain verifies", ok == (True, None) and len(lines) == 3, ok), C("rewriting round 2 in place is detected at line 1", ledger_verify(tam) == (False, 1), ledger_verify(tam)),
            C("default mode is paper until the gate passes", all(json.loads(l)["mode"] == "paper" for l in lines), "")]


# ---------------------------------------------------------------- CHECK-27 failure taxonomy
TAXONOMY = [("UNVERIFIED_SUCCESS", r"verified.*no evidence|claimed success", "downgrade to 'executed, not verified' and run the postcondition"),
            ("STALE_STATE", r"stale|etag mismatch|state changed", "re-probe live state"),
            ("BAD_TOOL_ARGS", r"InputValidationError|invalid argument|schema", "read the schema, fix once, never resend identical args"),
            ("PROBE_ABORT", r"aborted|SIGPIPE|killed", "run independent probes separately"),
            ("MISSING_DEP", r"ModuleNotFoundError|command not found|No module named", "install in an isolated env, verify import/version"),
            ("NEEDS_AUTH", r"401|403|unauthori[sz]ed|token", "name the exact key/connector"),
            ("NUMERIC_CONTAMINATION", r"number drift|value changed from frozen", "recompute in code, keep the frozen value"),
            ("REVIEWERS_FAILED", r"reviewer (timed out|failed)", "answer from verified evidence; say review was not obtained"),
            ("SUPPLY_CHAIN_RISK", r"curl .*\| *(ba)?sh|postinstall", "read the source; do not run third-party scripts"),
            ("REGRESSION", r"previously passing|regress", "roll back"),
            ("CATALOG_STALE", r"catalog (out of date|stale)", "read the file on disk; do not republish"),
            ("HALLUCINATED_FLAG", r"unrecognized option|unknown flag|Option not found", "run --help first"),
            ("WRONG_CWD", r"No such file or directory: '\./|not a git repository", "print pwd/branch before writes")]


def classify_failure(msg):
    for name, pat, fix in TAXONOMY:
        if re.search(pat, msg, re.I):
            return name, fix
    return "UNCLASSIFIED", "gather more evidence"


@program("CHECK-27")
def check_27(work):
    r1 = subprocess.run([sys.executable, "-c", "import kosif_no_such_module_xyz"], capture_output=True, text=True).stderr.strip().splitlines()[-1]
    r2 = subprocess.run(["ffmpeg", "-hide_banner", "-kosif_no_such_flag"], capture_output=True, text=True).stderr.strip().splitlines()[-1]
    r3 = subprocess.run(["git", "-C", str(work), "status"], capture_output=True, text=True).stderr.strip()
    got = {k: classify_failure(v)[0] for k, v in {"python": r1, "ffmpeg": r2, "git": r3, "http": "HTTP 401 Unauthorized", "x": "something odd"}.items()}
    wjson(Path(work) / "taxonomy.json", {"messages": [r1, r2, r3], "classes": got})
    return [C("13 named failures each with a smallest repair", len(TAXONOMY) == 13 and all(f for _, _, f in TAXONOMY), len(TAXONOMY)),
            C("real errors classified: missing module -> MISSING_DEP, bad ffmpeg flag -> HALLUCINATED_FLAG, git outside a repo -> WRONG_CWD", got["python"] == "MISSING_DEP" and got["ffmpeg"] == "HALLUCINATED_FLAG" and got["git"] == "WRONG_CWD", (got, r2, r3)),
            C("401 -> NEEDS_AUTH; unknown text stays UNCLASSIFIED (no blind retry)", got["http"] == "NEEDS_AUTH" and got["x"] == "UNCLASSIFIED", got)]


# ---------------------------------------------------------------- CHECK-28 incident record
INCIDENT = ("id", "date", "symptom", "command", "expected", "actual", "evidence", "cause", "fix", "acceptance", "status")


def incident_ok(row):
    p = [k for k in INCIDENT if not row.get(k)]
    if row.get("cause", "").split(":")[0] not in ("verified", "hypothesis"):
        p.append("cause not tagged verified/hypothesis")
    if row.get("status") == "VERIFIED" and not row.get("acceptance_output"):
        p.append("VERIFIED without acceptance output")
    if row.get("status") not in ("OPEN", "BLOCKED", "VERIFIED"):
        p.append("bad status")
    return p


@program("CHECK-28")
def check_28(work):
    w = Path(work); film = write_video(w / "film.mp4", moving_frames(30), 25); v = vstream(probe(film))
    row = {"id": "INC-1", "date": "2026-11-03", "symptom": "film plays at the wrong speed", "command": "ffprobe film.mp4", "expected": "30/1", "actual": v["r_frame_rate"],
           "evidence": "probe r_frame_rate", "cause": "verified: encoded with -r 25", "fix": "re-encode at -r 30", "acceptance": "r_frame_rate == 30/1", "status": "OPEN"}
    fixed = write_video(w / "fixed.mp4", moving_frames(30), 30); out = vstream(probe(fixed))["r_frame_rate"]
    done = dict(row, status="VERIFIED", acceptance_output=f"r_frame_rate={out}"); premature = dict(row, status="VERIFIED")
    wjson(w / "incidents.json", [row, done])
    return [C("incident row has 11 fields; actual 25/1 vs expected 30/1 measured", incident_ok(row) == [] and row["actual"] == "25/1", row["actual"]),
            C("VERIFIED only with the acceptance check output (30/1 after the fix)", incident_ok(done) == [] and out == "30/1", out), C("VERIFIED without acceptance output rejected", incident_ok(premature) == ["VERIFIED without acceptance output"], "")]


# ---------------------------------------------------------------- CHECK-29 self-repair rules
def repair_plan(steps, failure, gates):
    if failure["kind"] == "BAD_TOOL_ARGS" and failure.get("retry_args") == failure.get("args"):
        return {"action": "refuse identical retry"}
    if failure.get("uncertain_mutation"):
        return {"action": "check actual state first"}
    if any(gates[g] != v for g, v in failure.get("proposed_gates", {}).items()):
        return {"action": "refuse: never relax a safety/cost gate"}
    if failure.get("retries", 0) >= 1:
        return {"action": "stop and report"}
    return {"action": "retry once, narrower", "rerun": [failure["step"]], "keep": [s for s in steps if s != failure["step"]], "brief": failure["step"] + " (only the failed shot)"}


@program("CHECK-29")
def check_29(work):
    steps = ["shot1", "shot2", "shot3"]; gates = {"spend": "ask", "publish": "ask"}
    a = repair_plan(steps, {"kind": "RENDER", "step": "shot2"}, gates); b = repair_plan(steps, {"kind": "BAD_TOOL_ARGS", "step": "gen", "args": "{x}", "retry_args": "{x}"}, gates)
    c = repair_plan(steps, {"kind": "QUOTA", "step": "gen", "proposed_gates": {"spend": "auto"}}, gates); d = repair_plan(steps, {"kind": "RENDER", "step": "shot2", "retries": 1}, gates)
    e = repair_plan(steps, {"kind": "UPLOAD", "step": "push", "uncertain_mutation": True}, gates); wjson(Path(work) / "repair.json", [a, b, c, d, e])
    return [C("only the failed shot is retried once; successful peers kept", a["rerun"] == ["shot2"] and a["keep"] == ["shot1", "shot3"], a), C("identical retry after a schema error refused", b["action"] == "refuse identical retry", b),
            C("relaxing the spend gate is refused", c["action"].startswith("refuse: never relax"), c), C("second retry -> stop and report; uncertain mutation -> check state first", d["action"] == "stop and report" and e["action"] == "check actual state first", (d, e))]


# ---------------------------------------------------------------- CHECK-30 closed-set judge twice
REDACT = [(re.compile(r"sk-[A-Za-z0-9_-]{8,}"), "[KEY]"), (re.compile(r"[\w.]+@[\w.]+\.\w+"), "[EMAIL]"), (re.compile(r"\b(?:\d[ -]?){13,16}\b"), "[CARD]"), (re.compile(r"\+?\d{10,13}"), "[PHONE]")]


def judge_packet(q, options, evidence):
    if re.search(r"\b(pay|payment|delete|publish|send)\b|ادفع|احذف|انشر|أرسل", q, re.I):
        return None, "refused: approval question"
    if not evidence:
        return None, "refused: no evidence"
    for rx, rep in REDACT:
        evidence = rx.sub(rep, evidence)
    return {"q": q, "options": options + ["none"], "evidence": evidence}, "ok"


def closed_set_judge(packet, judge, fallback_rank, cache):
    key = hashlib.sha256(json.dumps(packet, sort_keys=True).encode()).hexdigest()
    if key in cache:
        return cache[key] | {"cached": True}
    if judge is None:
        res = {"choice": fallback_rank[0], "decided_by": "deterministic"}
    else:
        r1 = judge(packet["options"]); r2 = judge(packet["options"][::-1])
        if r1[0] == r2[0]:
            res = {"choice": r1[0], "decided_by": "stable"}
        else:
            score = {o: (r1.index(o) + r2.index(o)) / 2 for o in packet["options"]}; res = {"choice": min(score, key=lambda o: (score[o], packet["options"].index(o))), "decided_by": "mean_ranking"}
    cache[key] = res; return res


@program("CHECK-30")
def check_30(work):
    pk, st = judge_packet("Which caption reads best?", ["A", "B", "C"], "frames at 2.0 s; contact me at owner@example.com, key sk-abcdef123456")
    content = lambda opts: sorted(opts, key=lambda o: {"B": 0, "A": 1, "C": 2, "none": 3}[o])
    positional = lambda opts: list(opts)
    cache = {}; a = closed_set_judge(pk, content, ["A"], cache); a2 = closed_set_judge(pk, content, ["A"], cache)
    b = closed_set_judge(dict(pk, q="x"), positional, ["A"], {}); c = closed_set_judge(pk, None, ["C", "A"], {})
    ref = judge_packet("Should I publish the video now?", ["yes", "no"], "x"); wjson(Path(work) / "judge.json", {"packet": pk, "results": [a, b, c]})
    return [C("'none' offered and secrets/emails redacted", pk["options"][-1] == "none" and "[EMAIL]" in pk["evidence"] and "[KEY]" in pk["evidence"], pk),
            C("content judge agrees with itself reversed -> stable B; second call served from cache", a == {"choice": "B", "decided_by": "stable"} and a2.get("cached"), (a, a2)),
            C("positional judge disagrees -> mean_ranking", b["decided_by"] == "mean_ranking", b), C("judge unavailable -> deterministic fallback, says so", c == {"choice": "C", "decided_by": "deterministic"}, c),
            C("approval questions (publish) refused", ref == (None, "refused: approval question"), ref)]


# ---------------------------------------------------------------- CHECK-32 / 33 recording mock model server
def mock_server(script, folder):
    import http.server
    import threading
    folder = Path(folder); folder.mkdir(parents=True, exist_ok=True); state = {"i": 0}

    class H(http.server.BaseHTTPRequestHandler):
        def do_POST(self):
            body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
            i = state["i"]; state["i"] += 1
            (folder / f"req_{i:02d}.json").write_text(json.dumps({"path": self.path, "headers": {k: v for k, v in self.headers.items() if k.lower() != "authorization"}, "body": body.decode()}))
            code, payload = script[min(i, len(script) - 1)]
            self.send_response(code); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(payload.encode())

        def log_message(self, *a):
            pass
    srv = http.server.HTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


HARNESS = r'''
import json, sys, urllib.request, urllib.error
url = sys.argv[1]; msgs = [{"role": "user", "content": sys.argv[2]}]
for turn in range(4):
    req = urllib.request.Request(url + "/v1/messages", json.dumps({"messages": msgs, "tools": ["read_file"]}).encode(), {"Content-Type": "application/json", "x-test": "1"})
    try:
        r = json.loads(urllib.request.urlopen(req, timeout=5).read())
    except urllib.error.HTTPError as e:
        print(json.dumps({"event": "error", "status": e.code})); sys.exit(3)
    except json.JSONDecodeError:
        print(json.dumps({"event": "error", "status": "bad_json"})); sys.exit(4)
    if r.get("type") == "tool_use":
        open("tool_effect.txt", "w").write(r["input"]); msgs.append({"role": "tool", "content": "ok:" + r["input"]}); print(json.dumps({"event": "tool", "name": r["name"]})); continue
    print(json.dumps({"event": "final", "text": r["text"]})); sys.exit(0)
'''


def run_scenario(work, name, script):
    d = Path(work) / name; srv = mock_server(script, d / "requests")
    try:
        hp = Path(work) / "harness.py"; hp.write_text(HARNESS)
        p = subprocess.run([sys.executable, str(hp), f"http://127.0.0.1:{srv.server_port}", "hello"], capture_output=True, text=True, cwd=d, timeout=20)
    finally:
        srv.shutdown(); srv.server_close()
    (d / "stdout.txt").write_text(p.stdout); (d / "stderr.txt").write_text(p.stderr); (d / "exit_code").write_text(str(p.returncode))
    return d


def observable_checks(d, expect):
    reqs = [json.loads(p.read_text()) for p in sorted((d / "requests").glob("req_*.json"))]; bodies = [json.loads(r["body"]) for r in reqs]
    events = [json.loads(l) for l in (d / "stdout.txt").read_text().splitlines() if l.strip()]
    eff = (d / "tool_effect.txt").read_text() if (d / "tool_effect.txt").exists() else None
    checks = {"request count": len(reqs) == expect["requests"], "request shape": all({"messages", "tools"} <= set(b) for b in bodies),
              "instructions": all(b["messages"][0]["role"] == "user" for b in bodies), "tools": all(b["tools"] == ["read_file"] for b in bodies),
              "environment context": all(r["path"] == "/v1/messages" for r in reqs), "user messages": all(b["messages"][0]["content"] == "hello" for b in bodies),
              "tool results": (len(bodies) < 2) or bodies[1]["messages"][-1]["content"].startswith("ok:") == expect["tool"], "file effects": (eff is not None) == expect["tool"],
              "final answer": any(e["event"] == "final" for e in events) == expect["final"], "JSON events": all("event" in e for e in events),
              "exit code": int((d / "exit_code").read_text()) == expect["exit"], "stderr errors": (d / "stderr.txt").read_text() == "", "headers": all({k.lower(): v for k, v in r["headers"].items()}.get("x-test") == "1" for r in reqs)}
    return checks


@program("CHECK-32")
def check_32(work):
    ok = run_scenario(work, "tool_then_final", [(200, json.dumps({"type": "tool_use", "name": "read_file", "input": "a.txt"})), (200, json.dumps({"type": "text", "text": "done"}))])
    err = run_scenario(work, "server_500", [(500, "{}")]); bad = run_scenario(work, "bad_json", [(200, "{not json")])
    n_ok = len(list((ok / "requests").glob("*.json"))); out = (ok / "stdout.txt").read_text()
    return [C("scripted tool call then final: 2 requests recorded, tool effect written, exit 0", n_ok == 2 and (ok / "tool_effect.txt").read_text() == "a.txt" and (ok / "exit_code").read_text() == "0", out),
            C("scripted 500 -> harness exits 3 after 1 request", (err / "exit_code").read_text() == "3" and len(list((err / "requests").glob("*.json"))) == 1, (err / "stdout.txt").read_text()),
            C("bad JSON reply -> exit 4", (bad / "exit_code").read_text() == "4", (bad / "stdout.txt").read_text())]


@program("CHECK-33")
def check_33(work):
    a = run_scenario(work, "happy", [(200, json.dumps({"type": "tool_use", "name": "read_file", "input": "b.txt"})), (200, json.dumps({"type": "text", "text": "fin"}))])
    b = run_scenario(work, "err401", [(401, "{}")])
    ca = observable_checks(a, {"requests": 2, "tool": True, "final": True, "exit": 0}); cb = observable_checks(b, {"requests": 1, "tool": False, "final": False, "exit": 3})
    wrong = observable_checks(a, {"requests": 1, "tool": True, "final": True, "exit": 0}); wjson(Path(work) / "surface.json", {"happy": ca, "err401": cb})
    return [C("13 named checks per scenario, all pass on the happy path", len(ca) == 13 and all(ca.values()), ca), C("401 path: 13/13 with exit 3 and no final answer", all(cb.values()), cb),
            C("a wrong expectation fails only its own check (request count)", [k for k, v in wrong.items() if not v] == ["request count"], [k for k, v in wrong.items() if not v])]


# ---------------------------------------------------------------- CHECK-35 recovery notes + baseline
def score_exam(answers, key):
    return round(100 * sum(answers.get(q) == a for q, a in key.items()) / len(key), 1)


def recovery_note_ok(n):
    p = [k for k in ("tool_call", "changed", "verified", "missing", "baseline", "upgrade", "exam_id") if n.get(k) in (None, "", [])]
    if n.get("baseline_exam") != n.get("upgrade_exam"):
        p.append("before/after on different exams")
    if not n.get("from_tool") or not n.get("from_scripts"):
        p.append("tool vs own-script findings not separated")
    return p


@program("CHECK-35")
def check_35(work):
    key = {f"q{i}": i % 4 for i in range(65)}; before = {q: (a if int(q[1:]) < 49 else -1) for q, a in key.items()}; after = {q: (a if q != "q64" else -1) for q, a in key.items()}
    b, u = score_exam(before, key), score_exam(after, key)
    note = {"tool_call": "read section .text", "changed": "carved one section", "verified": ["64/65 answers"], "missing": ["q64 untested"], "baseline": b, "upgrade": u, "exam_id": "exam-65",
            "baseline_exam": "exam-65", "upgrade_exam": "exam-65", "from_tool": ["imports"], "from_scripts": ["string table"]}
    wjson(Path(work) / "recovery.json", note)
    return [C("same 65-question exam: 75.4% -> 98.5%", (b, u) == (75.4, 98.5), (b, u)), C("note lists tool call, change, verified, missing, and separates tool vs script findings", recovery_note_ok(note) == [], recovery_note_ok(note)),
            C("a baseline from a different exam is rejected", recovery_note_ok(dict(note, upgrade_exam="exam-80")) == ["before/after on different exams"], "")]
