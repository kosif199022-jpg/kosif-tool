#!/usr/bin/env python3
"""LLM Council / مجلس الخمسة: the mandatory, gated council of USIP v5.8 (appendix A38 §7).

One decision goes to five advisors who think in five opposed styles, their answers are reviewed
anonymously, and a chairman writes one verdict. The method is Andrej Karpathy's LLM Council as packaged
for Claude in github.com/aiwithremy/claude-skills-llm-council (its README credits Ole Lehmann; his own
profile could not be opened from this session, so that credit is unverified here). The repository ships
no licence file, so only the idea is used and every prompt is written in our own words. From REA
(github.com/morluto/rea, MIT) we take one pattern only: every input is either EVIDENCE with a source or a
named UNKNOWN, and a claim resting on an unknown turns into a "verify first" step.

The council's own first run (out/20261026-smart-council) decided how the protocol uses it:
  * the mandate is on the GATE: every L1+ request runs `gate` and gets a depth with its reason; L1+ is
    never skipped, the lowest depth is LIGHT (one line per voice);
  * depth = the higher of the level rule and the reversal-cost rule (money, publishing, personal data,
    architecture, anything irreversible = FULL); the user can force FULL ("مجلس كامل");
  * the question is derived from the brief's plans ("between A, B and C under these constraints, which
    and why?"), not the raw request;
  * one round only; no automatic escalation to the 100-persona council (only on explicit request);
  * correlated voices are caught by a similarity check, the Outsider gets no context, and every verdict
    records whether it changed the plan (CHANGED / NO_DELTA) so `stats` can measure the council's worth;
  * the user's hard constraints (--constraints, e.g. «لا ترجمة للآيات») are never truncated: their own section
    "Hard constraints / قيود ملزمة" sits right after the question in EVERY prompt (the five advisors, the
    Outsider's bare prompt included, the reviewers, the chairman, LIGHT). --context stays capped at
    MAX_CONTEXT files; whatever the cap drops is listed in "dropped_context", and a stderr warning names
    every --context item the user gave that was cut (lesson of 2026-10-29: a rule passed as --context was
    dropped without a word and no advisor saw it).

The script never calls a model. It gates, frames, writes every prompt, keeps the anonymous letter map,
checks each answer and the verdict, and writes a receipt. Claude runs the voices:
  FULL      five advisor subagents in parallel, five reviewer subagents in parallel, the chairman.
  STANDARD  five advisor subagents in parallel; the review round is skipped when 4 of 5 pick the same plan.
  LIGHT     one pass in Claude's own context: one or two lines per voice, one review line, the verdict.
  Receipts: COUNCIL5_RUN (real agents) · COUNCIL5_LIGHT · COUNCIL5_SIMULATED · COUNCIL5_INCOMPLETE.

From the repository root (S = python3 .claude/skills/kosif-superpowers/scripts/llm_council.py):
  S gate --level L2 [--from-brief brief.json] [--options 3] [--irreversible] [--force-full] [--dir D]
  S frame "<question>" --dir D [--from-brief brief.json] [--level L2] [--constraints "rule" ...] [--context F ...]
          [--evidence "src: fact" ...] [--unknowns "..." ...]
  S ingest --dir D --advisor contrarian --file a.md [--simulated]
  S review --dir D                  # similarity check, consensus check, anonymised reviewer prompts
  S ingest-review --dir D --reviewer R1 --file r1.md [--simulated]
  S chair --dir D                   # de-anonymised chairman prompt
  S verdict --dir D --file verdict.md [--simulated]
  S light "<question>" --dir D [--from-brief brief.json] [--constraints "rule" ...]
  S status --dir D · S stats [--root out] · S advisors · S --self-test

Exit codes: 0 ok, 2 usage or missing step, 3 the checked text fails the contract (fix and ingest again).
Python stdlib only.
"""
from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import hashlib
import io
import itertools
import json
import random
import re
import sys
import tempfile
from pathlib import Path

SCHEMA = "kosif.llm_council.v2"
SOURCE = ("Karpathy LLM Council via github.com/aiwithremy/claude-skills-llm-council (credited there to Ole Lehmann, "
          "unverified here; no licence file: idea only, our wording); evidence/unknowns pattern from github.com/morluto/rea")

ADVISORS = [
    {
        "id": "contrarian", "name": "The Contrarian", "ar": "المعارض",
        "style": "Assume the idea hides a fatal flaw and hunt for it: what fails, what is missing, which question is "
                 "being avoided. If it all looks sound, dig one level deeper. Not gloom for its own sake: the friend "
                 "who stops a bad deal.",
        "ar_style": "يفترض أن في الفكرة عيبًا قاتلًا ويبحث عنه: ما الذي سيفشل وما الناقص وما السؤال الذي نتهرب منه.",
    },
    {
        "id": "first_principles", "name": "The First-Principles Thinker", "ar": "مفكر المبادئ الأولى",
        "style": "Ignore the surface question and ask what is really being solved. Strip the assumptions and rebuild "
                 "the problem from the ground. Saying 'this is the wrong question' is a valid and valuable answer.",
        "ar_style": "يتجاهل السؤال الظاهر ويسأل: ما المشكلة الحقيقية؟ يجرد الافتراضات ويعيد البناء من الأساس.",
    },
    {
        "id": "expansionist", "name": "The Expansionist", "ar": "الموسِّع",
        "style": "Look for the upside nobody priced in: what could be bigger, which adjacent opportunity hides here, "
                 "what is undervalued, what happens if this works better than expected. Risk is someone else's job.",
        "ar_style": "يبحث عن المكسب الذي لم يره أحد: ما الأكبر، وما الفرصة المجاورة، وماذا لو نجح أكثر من المتوقع.",
    },
    {
        "id": "outsider", "name": "The Outsider", "ar": "الغريب",
        "style": "Know nothing about the person, the field or the history; react only to what is on the page. Catch "
                 "the curse of knowledge: jargon, leaps and things obvious to insiders but opaque to everyone else.",
        "ar_style": "لا يعرف شيئًا عن صاحب السؤال ولا مجاله؛ يرد على المكتوب فقط ويكشف لعنة المعرفة والمصطلحات.",
    },
    {
        "id": "executor", "name": "The Executor", "ar": "المنفِّذ",
        "style": "Care about one thing: can it be done, and what is the fastest path? Judge every idea by 'what do we "
                 "do first thing tomorrow'. A brilliant idea with no clear first step gets called out.",
        "ar_style": "يهمه شيء واحد: هل يُنفذ، وما أسرع طريق؟ «إيه أول حاجة نعملها بكرة الصبح؟»",
    },
]
IDS = [a["id"] for a in ADVISORS]
BY_ID = {a["id"]: a for a in ADVISORS}
LETTERS = "ABCDE"
REVIEWERS = [f"R{i}" for i in range(1, 6)]
DEPTHS = ("NONE", "LIGHT", "STANDARD", "FULL")

VERDICT_SECTIONS = [
    ("agree", r"(where the council agrees|أين اتفق المجلس|نقاط الاتفاق|اتفق المجلس)"),
    ("clash", r"(where the council clashes|أين اختلف المجلس|نقاط الخلاف|اختلف المجلس)"),
    ("blind", r"(blind spots|النقاط العمياء|ما كشفته المراجعة)"),
    ("recommend", r"(the recommendation|recommendation|التوصية)"),
    ("first", r"(the one thing to do first|one thing to do first|أول خطوة|الخطوة الأولى)"),
]
HEDGES = re.compile(r"\b(it depends|consider both sides|both have merit)\b|حسب الظروف|يعتمد على ظروفك|الاثنين كويسين",
                    re.I)
GROUNDING = re.compile(r"(\w+\.(py|md|json|js|html|txt)\b|/\w|\d|unknown|مجهول|غير معروف|لم يُتحقق|دليل|evidence)",
                       re.I)
PLAN_REF = re.compile(r"(?:\bplan\s*|الخطة\s*|خطة\s*)([A-D])\b", re.I)
WORDS_MIN, WORDS_MAX = 120, 360   # advisors are asked for 150-300 words; a little slack either way
LIGHT_MAX = 120                   # a LIGHT voice is one or two lines
REVIEW_MAX = 260
DUP_THRESHOLD = 0.6               # word-set Jaccard above this = two voices said the same thing
MAX_CONTEXT = 4                   # the brief plus the files the request names; more context = more generic answers
CONTEXT_CANDIDATES = ["CLAUDE.md", "claude.md", "memory", "PROJECT.md"]
IRREVERSIBLE_HINTS = re.compile(r"(publish|deploy|production|payment|spend|delete|migrat|personal data|انشر|نشر|ادفع|"
                                r"دفع|احذف|حذف|إنتاج|بيانات شخصية|معمارية|architecture)", re.I)


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def words(text: str) -> int:
    return len(re.findall(r"\w+", text, re.U))


def word_set(text: str) -> set:
    return {w for w in re.findall(r"\w+", text.lower(), re.U) if len(w) > 2}


def jaccard(a: str, b: str) -> float:
    x, y = word_set(a), word_set(b)
    return len(x & y) / len(x | y) if x | y else 0.0


def load(d: Path) -> dict:
    p = d / "council5.json"
    if not p.exists():
        raise SystemExit(f"no council in {d}: run `frame` or `light` first")
    return json.loads(p.read_text(encoding="utf-8"))


def save(d: Path, c: dict) -> None:
    d.mkdir(parents=True, exist_ok=True)
    (d / "council5.json").write_text(json.dumps(c, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_brief(path) -> dict:
    if not path:
        return {}
    b = json.loads(Path(path).read_text(encoding="utf-8"))
    plans = b.get("plans") or {}
    return {"path": str(path),
            "plans": {k: (v.get("idea") or v.get("name") or k) if isinstance(v, dict) else str(v)
                      for k, v in sorted(plans.items())},
            "recommended": b.get("recommended"),
            "reason": b.get("recommended_reason") or "",
            "request": ((b.get("analysis") or {}).get("request") or (b.get("analysis") or {}).get("text") or "")}


# ---------------------------------------------------------------------------------------------- gate
def gate(level: str, options: int = 0, irreversible: bool = False, force_full: bool = False,
         full_power: bool = False) -> dict:
    """Depth and reason. Depth = the higher of the level rule and the reversal-cost rule; L1+ is never skipped."""
    if level == "L0":
        return {"depth": "NONE", "reason": "L0: answered at once, no council", "review": False,
                "pro_council": "no", "hundred": "explicit request only"}
    reasons = []
    by_level = {"L1": "LIGHT", "L2": "STANDARD", "L3": "FULL"}[level]
    reasons.append(f"{level} -> {by_level}")
    depth = by_level
    if irreversible:
        depth = "FULL"
        reasons.append("irreversible / money / publishing / personal data / architecture -> FULL")
    if force_full or full_power:
        depth = "FULL"
        reasons.append("the user asked for the full council" if force_full else "full-power mode -> FULL")
    if level == "L1" and options < 2 and depth == "LIGHT":
        reasons.append("no fork (fewer than two real options): LIGHT checks the single path, one line per voice")
    review = {"LIGHT": False, "STANDARD": "only without a 4-of-5 consensus", "FULL": True}[depth]
    pro = "offer A13 (Pro council) if a factual clash survives the review" if depth == "FULL" else "no"
    return {"depth": depth, "reason": "; ".join(reasons), "review": review, "pro_council": pro,
            "hundred": "explicit request or «نفّذ بأقصى قوة» only"}


def cmd_gate(a) -> dict:
    br = read_brief(a.from_brief)
    options = a.options if a.options is not None else len(br.get("plans") or {})
    irreversible = a.irreversible or bool(IRREVERSIBLE_HINTS.search(br.get("request", "")))
    g = gate(a.level, options, irreversible, a.force_full, a.full_power)
    g.update({"level": a.level, "options": options, "at": now_iso()})
    if a.dir:
        Path(a.dir).mkdir(parents=True, exist_ok=True)
        (Path(a.dir) / "gate.json").write_text(json.dumps(g, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return g


# --------------------------------------------------------------------------------------------- frame
def context_report(root: Path, extra: list) -> tuple:
    """(kept, dropped). The files the request names come first, then the project's entry doc or memory;
    at most MAX_CONTEXT are kept and the rest is returned, never silently lost."""
    found = list(dict.fromkeys(extra or []))
    for name in CONTEXT_CANDIDATES:
        p = root / name
        if p.is_file():
            cand = [str(p.relative_to(root))]
        elif p.is_dir():
            cand = [str(f.relative_to(root)) for f in sorted(p.glob("*.md"))[:2]]
        else:
            cand = []
        found += [c for c in cand if c not in found]
    return found[:MAX_CONTEXT], found[MAX_CONTEXT:]


def scan_context(root: Path, extra: list) -> list:
    """The kept context files only (at most MAX_CONTEXT); context_report also says what was dropped."""
    return context_report(root, extra)[0]


def clean_constraints(items) -> list:
    """Hard user constraints, stripped and de-duplicated in order. Never truncated and never capped."""
    return list(dict.fromkeys(s.strip() for s in (items or []) if s and s.strip()))


CONSTRAINTS_HEAD = ("Hard constraints / قيود ملزمة (the user's own rules: binding, never traded off, reinterpreted "
                    "or dropped; a plan that breaks one is out / قواعد صاحب الطلب: ملزمة لا تُقايَض ولا تُؤوَّل، "
                    "والخطة التي تخالف واحدًا منها مرفوضة):")


def constraints_block(constraints: list) -> str:
    return CONSTRAINTS_HEAD + "\n" + "\n".join(f"- {k}" for k in constraints) + "\n"


def derive_question(question: str, br: dict) -> str:
    plans = br.get("plans") or {}
    if len(plans) < 2:
        return question.strip()
    opts = "; ".join(f"{k}: {v}" for k, v in plans.items())
    rec = f" The brief currently recommends {br['recommended']}." if br.get("recommended") else ""
    return (f"{question.strip()}\nDecision / القرار: between {opts} — under this request's constraints, which plan, "
            f"what does it miss, and what would change the choice?{rec}")


def framed_text(question: str, context: list, stakes: str, evidence: list, unknowns: list,
                with_context: bool = True, constraints: list = None) -> str:
    """The framed question. Hard constraints come right after the question, also without context (the
    Outsider's bare prompt): they are the user's rules, not background."""
    parts = [f"Question / السؤال:\n{question.strip()}\n"]
    if constraints:
        parts.append(constraints_block(constraints))
    if with_context:
        ctx = "\n".join(f"- {c}" for c in context) or "- (no context files; answer from the question alone)"
        parts.append(f"Context worth reading / سياق مفيد:\n{ctx}\n")
        if evidence:
            parts.append("Known, with evidence / معلوم بدليل:\n" + "\n".join(f"- {e}" for e in evidence) + "\n")
        if unknowns:
            parts.append("Unknown / مجهول (do not treat as fact):\n" + "\n".join(f"- {u}" for u in unknowns) + "\n")
    parts.append(f"What is at stake / ما على المحك:\n{stakes or 'a wrong call costs time, money or trust'}\n")
    return "\n".join(parts)


def advisor_prompt(a: dict, framed: str) -> str:
    return (f"You sit on a five-member council as {a['name']} ({a['ar']}).\n\n"
            f"How you think: {a['style']}\n\n"
            f"The question in front of the council:\n---\n{framed}---\n\n"
            "Answer from your angle only. Be direct and concrete; do not balance or hedge, the other four cover "
            "the angles you skip. If you see a fatal flaw or a big upside, say it plainly. Ground every claim: "
            "cite a file, a number or a fact from the context, or name it as an unknown (مجهول); a claim that "
            "rests on an unknown becomes 'verify first'. If plans are named, say which plan you back.\n"
            "150-300 words, no preamble. Answer in the user's language.")


def context_warnings(root: Path, user_ctx: list, dropped: list) -> list:
    """Plain-language warnings: --context items the user gave that MAX_CONTEXT cut, and --context items that
    are not files (a rule typed as --context belongs in --constraints)."""
    out = []
    cut = [x for x in dropped if x in user_ctx]
    if cut:
        out.append(f"--context: kept {len(user_ctx) - len(cut)} of {len(user_ctx)} item(s) you gave "
                   f"(MAX_CONTEXT={MAX_CONTEXT}, a brief included); dropped: " + "; ".join(cut) +
                   ". No advisor will see them. Pass hard user rules with --constraints (never truncated).")
    loose = [x for x in user_ctx if not (root / x).exists() and not Path(x).exists()]
    if loose:
        out.append("--context item(s) that are not files: " + "; ".join(loose) +
                   ". If one is a user rule, pass it with --constraints instead.")
    return out


def new_council(a, level: str, gate_info: dict) -> tuple:
    root = Path(a.root).resolve()
    br = read_brief(getattr(a, "from_brief", None))
    user_ctx = list(dict.fromkeys(getattr(a, "context", None) or []))
    context, dropped = context_report(root, ([br["path"]] if br else []) + user_ctx)
    question = derive_question(a.question, br)
    ev, un = list(getattr(a, "evidence", None) or []), list(getattr(a, "unknowns", None) or [])
    hard = clean_constraints(getattr(a, "constraints", None))
    framed = framed_text(question, context, a.stakes, ev, un, constraints=hard)
    bare = framed_text(question, [], a.stakes, [], [], with_context=False, constraints=hard)
    warns = context_warnings(root, user_ctx, dropped)
    for w in warns:
        print(f"llm_council: warning: {w}", file=sys.stderr)
    c = {"schema": SCHEMA, "source": SOURCE, "created": now_iso(), "question": question, "level": level,
         "depth": gate_info["depth"], "gate": gate_info, "framed": framed, "framed_outsider": bare,
         "constraints": hard, "context": context, "dropped_context": dropped,
         "dropped_user_context": [x for x in dropped if x in user_ctx], "warnings": warns,
         "evidence": ev, "unknowns": un, "plans": br.get("plans") or {},
         "brief_recommended": br.get("recommended"), "advisors": {}, "reviews": {}, "map": None,
         "consensus": None, "duplicates": [], "verdict": None}
    return c, framed, bare


def frame_report(c: dict) -> dict:
    """What the caller must see about a new council: the hard rules, what was kept and what was dropped."""
    return {"constraints": c["constraints"], "context": c["context"], "dropped_context": c["dropped_context"],
            "warnings": c["warnings"]}


def cmd_frame(a) -> dict:
    d = Path(a.dir)
    br = read_brief(a.from_brief)
    g = gate(a.level, len(br.get("plans") or {}) or 2, a.irreversible, a.force_full, False)
    c, framed, bare = new_council(a, a.level, g)
    save(d, c)
    pd = d / "prompts"
    pd.mkdir(parents=True, exist_ok=True)
    for adv in ADVISORS:
        text = bare if adv["id"] == "outsider" else framed
        (pd / f"advisor_{adv['id']}.txt").write_text(advisor_prompt(adv, text), encoding="utf-8")
    return {"dir": str(d), "depth": g["depth"], "reason": g["reason"], **frame_report(c),
            "next": "run the five advisor prompts in parallel (one message), then `ingest` each"}


# ---------------------------------------------------------------------------------------- advisors
def check_advisor(text: str, light: bool = False) -> list:
    n = words(text)
    probs = []
    if light:
        if n > LIGHT_MAX:
            probs.append(f"too long for LIGHT: {n} words (one or two lines)")
        return probs
    if n < WORDS_MIN:
        probs.append(f"too short: {n} words (aim for 150-300)")
    if n > WORDS_MAX:
        probs.append(f"too long: {n} words (aim for 150-300)")
    if not GROUNDING.search(text):
        probs.append("no evidence and no named unknown: cite a file, number or fact, or say what is unknown")
    return probs


def cmd_ingest(a) -> dict:
    d = Path(a.dir)
    c = load(d)
    if a.advisor not in BY_ID:
        raise SystemExit(f"unknown advisor {a.advisor}; one of {', '.join(IDS)}")
    text = Path(a.file).read_text(encoding="utf-8").strip()
    probs = check_advisor(text, light=c.get("depth") == "LIGHT")
    plans = PLAN_REF.findall(text)
    c["advisors"][a.advisor] = {"text": text, "words": words(text), "simulated": bool(a.simulated),
                                "plan": plans[0].upper() if plans else None, "problems": probs, "at": now_iso()}
    save(d, c)
    return {"advisor": a.advisor, "words": words(text), "plan": c["advisors"][a.advisor]["plan"],
            "problems": probs, "ok": not probs}


def duplicates(c: dict) -> list:
    out = []
    for x, y in itertools.combinations(IDS, 2):
        if x in c["advisors"] and y in c["advisors"]:
            j = jaccard(c["advisors"][x]["text"], c["advisors"][y]["text"])
            if j > DUP_THRESHOLD:
                out.append({"pair": [x, y], "jaccard": round(j, 2)})
    return out


def consensus(c: dict):
    picks = [v.get("plan") for v in c["advisors"].values() if v.get("plan")]
    if not picks:
        return None
    top = max(set(picks), key=picks.count)
    return top if picks.count(top) >= 4 else None


# ------------------------------------------------------------------------------------------ review
def letter_map(question: str, seed=None) -> dict:
    """advisor id -> letter, shuffled so no advisor sits in a fixed slot; deterministic per question."""
    s = seed if seed is not None else int(hashlib.sha256(question.encode("utf-8")).hexdigest()[:8], 16)
    order = IDS[:]
    random.Random(s).shuffle(order)
    return {adv: LETTERS[i] for i, adv in enumerate(order)}


def reviewer_prompt(framed: str, lettered: list, constraints: list = None) -> str:
    body = "\n\n".join(f"**Response {L}:**\n{t}" for L, t in lettered)
    hard = (" A response that breaks a hard constraint (قيد ملزم) above cannot be the strongest; name it under 2."
            if constraints else "")
    return ("You are reviewing a council. Five advisors answered this question independently:\n---\n"
            f"{framed}---\n\nTheir answers, anonymised:\n\n{body}\n\n"
            "Answer three questions, citing responses by letter:\n"
            "1. Strongest response, and why?\n"
            "2. Biggest blind spot: which response, and what does it miss?\n"
            "3. What did all five miss that the council should weigh?\n"
            f"Under 200 words, direct, in the user's language.{hard}")


def cmd_review(a) -> dict:
    d = Path(a.dir)
    c = load(d)
    missing = [i for i in IDS if i not in c["advisors"]]
    if missing:
        raise SystemExit(f"advisors still missing: {', '.join(missing)}")
    c["duplicates"] = duplicates(c)
    c["consensus"] = consensus(c)
    if c["duplicates"]:
        save(d, c)
        return {"problems": [f"DUPLICATE_VOICE {p['pair'][0]} ~ {p['pair'][1]} (jaccard {p['jaccard']}): "
                             "re-run the second voice with its own angle" for p in c["duplicates"]]}
    m = letter_map(c["question"], a.seed)
    c["map"] = m
    lettered = sorted(((m[i], c["advisors"][i]["text"]) for i in IDS))
    prompt = reviewer_prompt(c["framed"], lettered, c.get("constraints"))
    for r in REVIEWERS:
        (d / "prompts" / f"review_{r}.txt").write_text(prompt, encoding="utf-8")
    save(d, c)
    skip = c.get("depth") == "STANDARD" and c["consensus"]
    return {"consensus": c["consensus"], "review_needed": not skip,
            "next": ("4 of 5 back plan " + c["consensus"] + ": the review round may be skipped; go to `chair`")
            if skip else "run the five reviewer prompts in parallel, then `ingest-review` each"}


def check_review(text: str) -> list:
    probs = []
    cited = set(re.findall(r"\b(?:Response\s*)?([A-E])\b", text)) | set(
        re.findall(r"(?:الرد|رد|الإجابة)\s*([A-E])", text))
    if len(cited) < 2:
        probs.append("cite at least two responses by letter (strongest and blind spot)")
    if not re.search(r"(3[.)]|missed|all five|كلهم|الخمسة|فات|غاب)", text, re.I):
        probs.append("answer question 3: what all five missed")
    if words(text) > REVIEW_MAX:
        probs.append(f"too long: {words(text)} words (under 200)")
    return probs


def cmd_ingest_review(a) -> dict:
    d = Path(a.dir)
    c = load(d)
    if c.get("map") is None:
        raise SystemExit("run `review` first")
    if a.reviewer not in REVIEWERS:
        raise SystemExit(f"unknown reviewer {a.reviewer}; one of {', '.join(REVIEWERS)}")
    text = Path(a.file).read_text(encoding="utf-8").strip()
    probs = check_review(text)
    c["reviews"][a.reviewer] = {"text": text, "simulated": bool(a.simulated), "problems": probs, "at": now_iso()}
    save(d, c)
    return {"reviewer": a.reviewer, "problems": probs, "ok": not probs}


def reviews_required(c: dict) -> bool:
    if c.get("depth") == "FULL":
        return True
    if c.get("depth") == "STANDARD":
        return not c.get("consensus")
    return False


# ------------------------------------------------------------------------------------------- chair
def chair_prompt(c: dict) -> str:
    def tag(i):
        return f" — was Response {c['map'][i]}" if c.get("map") else ""
    adv = "\n\n".join(f"**{BY_ID[i]['name']} ({BY_ID[i]['ar']}){tag(i)}:**\n{c['advisors'][i]['text']}" for i in IDS)
    rev = "\n\n".join(f"**Review {r}:**\n{c['reviews'][r]['text']}" for r in REVIEWERS if r in c["reviews"]) \
        or "(no review round: 4 of 5 advisors backed the same plan)"
    plan_rule = (" Name the plan letter you recommend, and say if it differs from the brief's recommendation "
                 f"({c['brief_recommended']}).") if c.get("plans") else ""
    if c.get("constraints"):
        plan_rule += (" The hard constraints (قيود ملزمة) are the user's rules: the recommendation and the first "
                      "step keep every one of them, and an advisor who breaks one is overruled on that point.")
    return ("You chair the council. Turn five advisors and their peer reviews into one verdict.\n\n"
            f"The question:\n---\n{c['framed']}---\n\nADVISORS (de-anonymised):\n\n{adv}\n\nPEER REVIEWS:\n\n{rev}\n\n"
            "Write the verdict with exactly these five headings, in order:\n"
            "## Where the Council Agrees / أين اتفق المجلس\n"
            "## Where the Council Clashes / أين اختلف المجلس\n"
            "## Blind Spots the Council Caught / النقاط العمياء\n"
            "## The Recommendation / التوصية\n"
            "## The One Thing to Do First / أول خطوة\n"
            "Agreement reached independently is a strong signal. Do not smooth over real disagreement. The "
            "recommendation is a real answer, never 'it depends'; you may side with a lone dissenter when their "
            "reasoning is best, and say why. A step that rests on an unknown is 'verify X first'. The first step "
            "is ONE concrete action, not a list. The user's explicit choice of plan outranks the council: advise, "
            f"never overrule.{plan_rule} Scannable bullets, in the user's language.")


def cmd_chair(a) -> dict:
    d = Path(a.dir)
    c = load(d)
    if reviews_required(c):
        if c.get("map") is None:
            raise SystemExit("run `review` first")
        missing = [r for r in REVIEWERS if r not in c["reviews"]]
        if missing:
            raise SystemExit(f"reviews still missing: {', '.join(missing)}")
    (d / "prompts").mkdir(parents=True, exist_ok=True)
    (d / "prompts" / "chair.txt").write_text(chair_prompt(c), encoding="utf-8")
    return {"prompt": str(d / "prompts" / "chair.txt"), "next": "run the chairman, then `verdict --file`"}


# ----------------------------------------------------------------------------------------- verdict
def split_sections(text: str) -> dict:
    heads = [(m.start(), m.group(0)) for m in re.finditer(r"(?m)^#{2,4}\s*.+$|^\*\*[^*\n]+\*\*\s*$", text)]
    out = {}
    for i, (pos, head) in enumerate(heads):
        end = heads[i + 1][0] if i + 1 < len(heads) else len(text)
        for key, pat in VERDICT_SECTIONS:
            if key not in out and re.search(pat, head, re.I):
                out[key] = text[pos + len(head):end].strip()
                break
    return out


def check_verdict(text: str, plans: dict = None) -> list:
    secs = split_sections(text)
    probs = [f"missing section: {k}" for k, _ in VERDICT_SECTIONS if k not in secs or not secs[k]]
    rec = secs.get("recommend", "")
    if rec and HEDGES.search(rec):
        probs.append("the recommendation hedges ('it depends'): give a real answer")
    if rec and plans and len(plans) >= 2 and not PLAN_REF.search(rec):
        probs.append("plans were on the table: name the recommended plan letter (e.g. 'الخطة B')")
    first = secs.get("first", "")
    items = [ln for ln in first.splitlines() if re.match(r"\s*([-*•]|\d+[.)])\s+", ln)]
    if len(items) > 1:
        probs.append(f"the first step must be ONE action, found a list of {len(items)}")
    return probs


def delta(c: dict, text: str) -> str:
    if not c.get("brief_recommended"):
        return "n/a"
    m = PLAN_REF.search(split_sections(text).get("recommend", ""))
    if not m:
        return "n/a"
    return "NO_DELTA" if m.group(1).upper() == str(c["brief_recommended"]).upper() else "CHANGED"


def receipt_status(c: dict) -> str:
    voices = list(c["advisors"].values()) + list(c["reviews"].values())
    if c.get("depth") == "LIGHT":
        return "COUNCIL5_LIGHT"
    if any(v.get("simulated") for v in voices) or (c.get("verdict") or {}).get("simulated"):
        return "COUNCIL5_SIMULATED"
    return "COUNCIL5_RUN"


def cmd_verdict(a) -> dict:
    d = Path(a.dir)
    c = load(d)
    text = Path(a.file).read_text(encoding="utf-8").strip()
    probs = check_verdict(text, c.get("plans"))
    c["verdict"] = {"text": text, "simulated": bool(a.simulated), "problems": probs, "at": now_iso()}
    open_items = [] if c.get("depth") == "LIGHT" else [f"advisor {i}" for i in IDS if i not in c["advisors"]]
    if reviews_required(c):
        open_items += [f"review {r}" for r in REVIEWERS if r not in c["reviews"]]
    if c.get("duplicates"):
        open_items.append("duplicate voices not re-run")
    status = "COUNCIL5_INCOMPLETE" if (open_items or probs) else receipt_status(c)
    c["receipt"] = {"status": status, "depth": c.get("depth"), "reason": (c.get("gate") or {}).get("reason"),
                    "delta": delta(c, text), "consensus": c.get("consensus"), "open": open_items,
                    "problems": probs, "at": now_iso(),
                    "verdict_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()}
    save(d, c)
    (d / "VERDICT.md").write_text(f"<!-- {status} · depth {c.get('depth')} · {c['receipt']['delta']} -->\n{text}\n",
                                  encoding="utf-8")
    return c["receipt"]


# ------------------------------------------------------------------------------------------- light
def light_prompt(framed: str) -> str:
    lines = "\n".join(f"- {a['name']} / {a['ar']}: {a['ar_style']}" for a in ADVISORS)
    return ("Light council (LIGHT): in one pass, give each of the five voices one or two lines, then one line of "
            "peer review (strongest voice and the biggest blind spot), then the five-heading verdict.\n\n"
            f"{framed}\nVoices:\n{lines}\n\n"
            "Verdict headings: Where the Council Agrees · Where the Council Clashes · Blind Spots · "
            "The Recommendation · The One Thing to Do First. Label it LIGHT; it is not a run of subagents.")


def cmd_light(a) -> dict:
    d = Path(a.dir)
    g = gate("L1", 2)
    c, framed, _ = new_council(a, "L1", g)
    save(d, c)
    (d / "prompts").mkdir(parents=True, exist_ok=True)
    (d / "prompts" / "light.txt").write_text(light_prompt(framed), encoding="utf-8")
    return {"prompt": str(d / "prompts" / "light.txt"), **frame_report(c),
            "next": "answer the light prompt in context, save the verdict, then `verdict --file v.md`"}


# --------------------------------------------------------------------------------------- reporting
def cmd_status(a) -> dict:
    c = load(Path(a.dir))
    return {"level": c.get("level"), "depth": c.get("depth"), "constraints": c.get("constraints") or [],
            "dropped_context": c.get("dropped_context") or [], "advisors": sorted(c["advisors"]),
            "reviews": sorted(c["reviews"]), "anonymised": c.get("map") is not None,
            "consensus": c.get("consensus"), "duplicates": c.get("duplicates"), "receipt": c.get("receipt")}


def cmd_stats(a) -> dict:
    """How the council is really used: depth mix, receipts, and how often a verdict changed the plan."""
    rows = []
    for p in sorted(Path(a.root).rglob("council5.json")):
        try:
            c = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        r = c.get("receipt") or {}
        rows.append({"dir": str(p.parent), "depth": c.get("depth") or "v1", "status": r.get("status", "OPEN"),
                     "delta": r.get("delta", "n/a")})

    def count(key):
        out = {}
        for r in rows:
            out[r[key]] = out.get(r[key], 0) + 1
        return out
    decided = [r for r in rows if r["delta"] in ("CHANGED", "NO_DELTA")]
    changed = sum(r["delta"] == "CHANGED" for r in decided)
    return {"councils": len(rows), "by_depth": count("depth"), "by_status": count("status"),
            "delta": {"changed": changed, "no_delta": len(decided) - changed,
                      "changed_rate": round(changed / len(decided), 2) if decided else None},
            "note": "a low changed rate over many councils means the gate is too generous; LIGHT receipts are "
                    "audited by reading a sample of their VERDICT.md files"}


def cmd_advisors(_a) -> list:
    return [{"id": a["id"], "name": a["name"], "ar": a["ar"], "style": a["ar_style"]} for a in ADVISORS]


# --------------------------------------------------------------------------------------- self-test
SAMPLE = {i: (f"{i} " + " ".join(f"w{i}{n}" for n in range(170)) + " evidence brief.json backs الخطة B").strip()
          for i in IDS}


def self_test() -> int:
    ns = argparse.Namespace
    assert gate("L0")["depth"] == "NONE"
    assert gate("L1", 1)["depth"] == "LIGHT" and "no fork" in gate("L1", 1)["reason"]
    assert gate("L2", 3)["depth"] == "STANDARD"
    assert gate("L1", 2, irreversible=True)["depth"] == "FULL"
    assert gate("L2", 3, force_full=True)["depth"] == "FULL" and gate("L3")["review"] is True
    with tempfile.TemporaryDirectory() as t:
        tp = Path(t)
        brief = tp / "brief.json"
        brief.write_text(json.dumps({"plans": {"A": {"idea": "templates"}, "B": {"idea": "custom engine"},
                                               "C": {"idea": "outsource"}}, "recommended": "A",
                                     "analysis": {"request": "publish a launch video"}}), encoding="utf-8")
        g = cmd_gate(ns(level="L2", from_brief=str(brief), options=None, irreversible=False, force_full=False,
                        full_power=False, dir=None))
        assert g["depth"] == "FULL" and g["options"] == 3, g          # "publish" makes it irreversible
        d = tp / "c"
        cmd_frame(ns(question="Which way for the launch video?", dir=str(d), level="L3", context=[], stakes="",
                     root=t, from_brief=str(brief), evidence=["brief.json: 3 plans"], unknowns=["budget"],
                     irreversible=False, force_full=False))
        c = load(d)
        assert "between A: templates" in c["question"] and c["brief_recommended"] == "A"
        outsider = (d / "prompts" / "advisor_outsider.txt").read_text(encoding="utf-8")
        assert "Context worth reading" not in outsider and "Unknown / مجهول" not in outsider
        assert "Context worth reading" in (d / "prompts" / "advisor_executor.txt").read_text(encoding="utf-8")
        for i in IDS:
            f = tp / f"{i}.md"
            f.write_text(SAMPLE[i], encoding="utf-8")
            out = cmd_ingest(ns(dir=str(d), advisor=i, file=str(f), simulated=False))
            assert out["ok"] and out["plan"] == "B", out
        assert check_advisor(" ".join(["word"] * 200))[0].startswith("no evidence")
        rv = cmd_review(ns(dir=str(d), seed=None))
        assert rv["consensus"] == "B" and rv["review_needed"] is True          # FULL always reviews
        m = load(d)["map"]
        assert sorted(m.values()) == list(LETTERS) and m == letter_map(load(d)["question"])
        assert "The Contrarian" not in (d / "prompts" / "review_R1.txt").read_text(encoding="utf-8")
        rf = tp / "r.md"
        rf.write_text("1. Response B is strongest. 2. Response D misses cost. 3. All five missed timing.",
                      encoding="utf-8")
        for r in REVIEWERS:
            assert cmd_ingest_review(ns(dir=str(d), reviewer=r, file=str(rf), simulated=False))["ok"]
        assert check_review("I liked it")
        cmd_chair(ns(dir=str(d)))
        assert "was Response" in (d / "prompts" / "chair.txt").read_text(encoding="utf-8")
        good = ("## Where the Council Agrees\n- demand is real\n## Where the Council Clashes\n- price\n"
                "## Blind Spots the Council Caught\n- naming\n## The Recommendation\nGo with الخطة B, piloted small.\n"
                "## The One Thing to Do First\nVerify the budget today.\n")
        vf = tp / "v.md"
        vf.write_text(good, encoding="utf-8")
        r = cmd_verdict(ns(dir=str(d), file=str(vf), simulated=False))
        assert r["status"] == "COUNCIL5_RUN" and r["delta"] == "CHANGED", r
        bad = good.replace("Go with الخطة B, piloted small.", "It depends on your goals.").replace(
            "Verify the budget today.", "- a\n- b")
        probs = check_verdict(bad, {"A": 1, "B": 2})
        assert any("hedges" in p for p in probs) and any("ONE action" in p for p in probs) \
            and any("plan letter" in p for p in probs), probs
        ar = ("## أين اتفق المجلس\nس\n## أين اختلف المجلس\nس\n## النقاط العمياء\nس\n## التوصية\nابدأ بتجربة.\n"
              "## أول خطوة\nافتح صفحة انتظار.\n")
        assert not check_verdict(ar), check_verdict(ar)
        # STANDARD with a 4-of-5 consensus may skip the review round
        d2 = tp / "s"
        cmd_frame(ns(question="q", dir=str(d2), level="L2", context=[], stakes="", root=t, from_brief=str(brief),
                     evidence=[], unknowns=[], irreversible=False, force_full=False))
        c2 = load(d2)
        c2["depth"] = "STANDARD"
        save(d2, c2)
        for i in IDS:
            cmd_ingest(ns(dir=str(d2), advisor=i, file=str(tp / f"{i}.md"), simulated=False))
        assert cmd_review(ns(dir=str(d2), seed=None))["review_needed"] is False
        cmd_chair(ns(dir=str(d2)))
        assert cmd_verdict(ns(dir=str(d2), file=str(vf), simulated=False))["status"] == "COUNCIL5_RUN"
        # duplicate voices are caught
        d3 = tp / "dup"
        cmd_frame(ns(question="q", dir=str(d3), level="L3", context=[], stakes="", root=t, from_brief=None,
                     evidence=[], unknowns=[], irreversible=False, force_full=False))
        for i in IDS:
            cmd_ingest(ns(dir=str(d3), advisor=i, file=str(tp / "contrarian.md"), simulated=False))
        assert cmd_review(ns(dir=str(d3), seed=None))["problems"]
        assert cmd_verdict(ns(dir=str(d3), file=str(vf), simulated=False))["status"] == "COUNCIL5_INCOMPLETE"
        # LIGHT
        d4 = tp / "l"
        cmd_light(ns(question="Which font?", dir=str(d4), context=[], stakes="", root=t, from_brief=None))
        assert cmd_verdict(ns(dir=str(d4), file=str(vf), simulated=True))["status"] == "COUNCIL5_LIGHT"
        st = cmd_stats(ns(root=t))
        assert st["councils"] == 4 and st["delta"]["changed"] >= 1, st
        # hard constraints: never truncated, right after the question in EVERY prompt; a cut --context is reported
        rule = "لا ترجمة للآيات"
        rules = [rule] + [f"rule {n}" for n in range(1, 8)]          # eight rules: more than MAX_CONTEXT
        for n in range(4):
            (tp / f"f{n}.md").write_text("x", encoding="utf-8")
        user_ctx = [f"f{n}.md" for n in range(4)] + [rule]             # the 2026-10-29 bug: a rule passed as context
        d5 = tp / "k"
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            fr = cmd_frame(ns(question="Which reel?", dir=str(d5), level="L3", context=user_ctx, stakes="", root=t,
                              from_brief=str(brief), evidence=["brief.json: 3 plans"], unknowns=[],
                              irreversible=False, force_full=False, constraints=rules + [rule, "  "]))
        c5 = load(d5)
        assert fr["constraints"] == rules and c5["constraints"] == rules, fr           # de-duplicated, never cut
        assert fr["context"] == [str(brief), "f0.md", "f1.md", "f2.md"], fr
        assert fr["dropped_context"] == ["f3.md", rule] == c5["dropped_user_context"], fr
        warned = err.getvalue()
        assert "dropped: f3.md; " + rule in warned and "--constraints" in warned and "not files" in warned, warned
        head = f"{c5['question']}\n\n{CONSTRAINTS_HEAD}"                              # right after the question

        def holds(text: str) -> bool:
            return head in text and all(f"- {r}\n" in text for r in rules)
        for i in IDS:
            assert holds((d5 / "prompts" / f"advisor_{i}.txt").read_text(encoding="utf-8")), i
        assert "Context worth reading" not in (d5 / "prompts" / "advisor_outsider.txt").read_text(encoding="utf-8")
        for i in IDS:
            cmd_ingest(ns(dir=str(d5), advisor=i, file=str(tp / f"{i}.md"), simulated=False))
        cmd_review(ns(dir=str(d5), seed=None))
        review = (d5 / "prompts" / "review_R1.txt").read_text(encoding="utf-8")
        assert holds(review) and "cannot be the strongest" in review
        for r in REVIEWERS:
            cmd_ingest_review(ns(dir=str(d5), reviewer=r, file=str(rf), simulated=False))
        cmd_chair(ns(dir=str(d5)))
        chair = (d5 / "prompts" / "chair.txt").read_text(encoding="utf-8")
        assert holds(chair) and "overruled on that point" in chair
        assert cmd_status(ns(dir=str(d5)))["constraints"] == rules
        d6 = tp / "kl"
        lf = cmd_light(ns(question="Which font?", dir=str(d6), context=[], stakes="", root=t, from_brief=None,
                          constraints=[rule]))
        assert lf["constraints"] == [rule] and lf["dropped_context"] == [] and not lf["warnings"], lf
        assert f"Which font?\n\n{CONSTRAINTS_HEAD}\n- {rule}\n" in (d6 / "prompts" / "light.txt").read_text(
            encoding="utf-8")
        # without constraints nothing changes: no section, no reviewer or chair clause
        assert CONSTRAINTS_HEAD not in (d / "prompts" / "advisor_executor.txt").read_text(encoding="utf-8")
        assert "overruled on that point" not in (d / "prompts" / "chair.txt").read_text(encoding="utf-8")
    print("llm_council self-test: OK")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--self-test", action="store_true")
    sub = ap.add_subparsers(dest="cmd")

    def ctx(p):
        p.add_argument("question")
        p.add_argument("--dir", required=True)
        p.add_argument("--from-brief")
        p.add_argument("--constraints", nargs="*", default=[],
                       help="the user's hard rules (e.g. «لا ترجمة للآيات»): never truncated, placed right after "
                            "the question in every prompt, the Outsider's included")
        p.add_argument("--context", nargs="*", default=[],
                       help=f"files worth reading: at most {MAX_CONTEXT} with the brief; the rest is listed in "
                            "dropped_context with a stderr warning")
        p.add_argument("--evidence", nargs="*", default=[])
        p.add_argument("--unknowns", nargs="*", default=[])
        p.add_argument("--stakes", default="")
        p.add_argument("--root", default=".")

    p = sub.add_parser("gate")
    p.add_argument("--level", required=True, choices=["L0", "L1", "L2", "L3"])
    p.add_argument("--from-brief")
    p.add_argument("--options", type=int)
    p.add_argument("--irreversible", action="store_true")
    p.add_argument("--force-full", action="store_true")
    p.add_argument("--full-power", action="store_true")
    p.add_argument("--dir")
    p = sub.add_parser("frame")
    ctx(p)
    p.add_argument("--level", default="L2", choices=["L1", "L2", "L3"])
    p.add_argument("--irreversible", action="store_true")
    p.add_argument("--force-full", action="store_true")
    ctx(sub.add_parser("light"))
    p = sub.add_parser("ingest")
    p.add_argument("--dir", required=True)
    p.add_argument("--advisor", required=True)
    p.add_argument("--file", required=True)
    p.add_argument("--simulated", action="store_true")
    p = sub.add_parser("review")
    p.add_argument("--dir", required=True)
    p.add_argument("--seed", type=int)
    p = sub.add_parser("ingest-review")
    p.add_argument("--dir", required=True)
    p.add_argument("--reviewer", required=True)
    p.add_argument("--file", required=True)
    p.add_argument("--simulated", action="store_true")
    p = sub.add_parser("chair")
    p.add_argument("--dir", required=True)
    p = sub.add_parser("verdict")
    p.add_argument("--dir", required=True)
    p.add_argument("--file", required=True)
    p.add_argument("--simulated", action="store_true")
    p = sub.add_parser("status")
    p.add_argument("--dir", required=True)
    p = sub.add_parser("stats")
    p.add_argument("--root", default="out")
    sub.add_parser("advisors")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    fn = {"gate": cmd_gate, "frame": cmd_frame, "light": cmd_light, "ingest": cmd_ingest, "review": cmd_review,
          "ingest-review": cmd_ingest_review, "chair": cmd_chair, "verdict": cmd_verdict,
          "status": cmd_status, "stats": cmd_stats, "advisors": cmd_advisors}.get(a.cmd)
    if not fn:
        ap.print_help()
        return 2
    out = fn(a)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    if isinstance(out, dict) and (out.get("problems") or out.get("status") == "COUNCIL5_INCOMPLETE"):
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
