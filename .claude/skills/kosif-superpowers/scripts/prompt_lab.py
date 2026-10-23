#!/usr/bin/env python3
"""Prompt lab: build, lint, refine and test prompts / مختبر البرومبت: بناء وفحص وتحسين واختبار.

Makes the prompt-craft method (references/prompt-optimizer.md, PROMPT-01…PROMPT-41) runnable:

    python3 scripts/prompt_lab.py kinds                                   # the prompt kinds and their slots
    python3 scripts/prompt_lab.py build --kind image --goal "..." [--set subject=... --set aspect=9:16] [--lang ar]
    python3 scripts/prompt_lab.py lint PROMPT.txt --kind agent [--json]   # 20-point rubric proxy, hard gates, anti-patterns
    python3 scripts/prompt_lab.py refine PROMPT.txt --kind code           # ordered fixes + the kind's skeleton to merge into
    python3 scripts/prompt_lab.py eval --cases cases.json --outputs outputs.json [--baseline A]   # assertion matrix, keep-or-revert
    python3 scripts/prompt_lab.py pairwise --verdicts verdicts.json       # order-swapped judge votes -> stable winner
    python3 scripts/prompt_lab.py pairwise --plan --a A.txt --b B.txt --task "..."   # the two judge prompts (A/B, then B/A)
    python3 scripts/prompt_lab.py --self-test

Everything is deterministic and offline: the linter measures what text can show (slots present, anti-patterns, gates)
and cannot judge whether the prompt will work. Proving "better" is the eval command on real outputs (PROMPT-15, -31).
The pairwise judge is the order-robust method of the owner's Jev decision service, done locally: each pair is judged
twice with positions swapped and only an agreeing verdict counts. Python 3.8+ standard library only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------------------------------------------
# Kinds: the slots each kind of prompt needs, in render order. (slot, label, required, hint)
COMMON = [
    ("goal", "Task", True, "one verb + one deliverable"),
    ("audience", "Audience and purpose", True, "who reads the result and what decision it supports"),
    ("context", "Context and why", True, "background the model cannot guess, with the reason behind each rule"),
    ("inputs", "Inputs", False, "what is provided and where; long material goes first, inside tags"),
    ("constraints", "Constraints", False, "in scope, out of scope, each rule with its reason"),
    ("output", "Output format", True, "format, length, structure, file type"),
    ("success", "Done when", True, "a pass/fail check and the evidence to show"),
    ("uncertainty", "If unsure", False, "ask one question, assume and state, or return null"),
]
KINDS = {
    "system": {"about": "system prompt for an app or assistant (PROMPT-07)", "visual": False,
               "slots": [("role", "Role", True, "what the assistant is for, in one sentence")] + COMMON
               + [("tools", "Tools", False, "each tool and when to use it"),
                  ("tone", "Tone", False, "register and dialect, with one sample sentence")]},
    "agent": {"about": "task brief for a subagent, scheduled task or Claude Code (PROMPT-08)", "visual": False,
              "slots": COMMON + [("tools", "Tools and permissions", True, "what it may run, what needs approval"),
                                 ("stop", "Stop conditions", True, "when to stop and report instead of continuing"),
                                 ("budget", "Budget", False, "time, calls or tokens; the return size"),
                                 ("state", "State files", False, "where progress and receipts are written")]},
    "code": {"about": "coding task for an LLM or a coding agent", "visual": False,
             "slots": COMMON + [("repo", "Codebase facts", True, "language, versions, files to read first, conventions"),
                                ("tests", "Tests", True, "the command that proves it works and what must stay green"),
                                ("nongoals", "Non-goals", False, "what not to refactor or touch")]},
    "research": {"about": "research or analysis question", "visual": False,
                 "slots": COMMON + [("sources", "Sources", True, "allowed sources, recency window, citation format"),
                                    ("claims", "Claim policy", False, "how to mark unverified or conflicting findings")]},
    "writing": {"about": "writing task: article, script, caption, email", "visual": False,
                "slots": COMMON + [("voice", "Voice", True, "register, dialect, person, a sample of the wanted voice"),
                                   ("length", "Length", False, "words or seconds of speech")]},
    "judge": {"about": "LLM-grader prompt for an eval (PROMPT-15)", "visual": False,
              "slots": [("goal", "Task", True, "what is being graded"),
                        ("rubric", "Rubric", True, "numbered criteria, each with what passes and what fails"),
                        ("labels", "Labels", True, "the fixed output labels, e.g. PASS / FAIL or 1-5"),
                        ("output", "Output format", True, "label first, then one-sentence reason"),
                        ("success", "Done when", False, "agreement with a few human-labelled cases")]},
    "image": {"about": "image-generator prompt (PROMPT-10, PROMPT-35)", "visual": True,
              "slots": [("subject", "Subject", True, "who or what, with visible attributes"),
                        ("action", "Action", True, "what the subject is doing"),
                        ("environment", "Environment", True, "place, time, weather"),
                        ("shot", "Shot and lens", True, "framing, angle, focal length"),
                        ("light", "Light", True, "source and direction"),
                        ("style", "Style and palette", True, "visible properties, materials, colours, never a living artist"),
                        ("text", "On-image text", False, "exact words in quotes and their placement"),
                        ("lock", "Series lock", False, "words repeated verbatim across a series"),
                        ("aspect", "Aspect", True, "e.g. 9:16"),
                        ("negative", "Negative field", False, "unwanted elements, for the platform's negative field")]},
    "video": {"about": "video-generator shot prompt (PROMPT-11)", "visual": True,
              "slots": [("shot", "Shot type and angle", True, "e.g. medium close-up, low angle"),
                        ("subject", "Subject", True, "who or what"),
                        ("action", "One action", True, "a single clear action"),
                        ("environment", "Place and time", True, "place, time, weather"),
                        ("camera", "Camera move", True, "static, pan, tilt, dolly, truck, crane, orbit, handheld"),
                        ("style", "Style, palette, light", True, "look and light direction"),
                        ("duration", "Duration", True, "seconds"),
                        ("aspect", "Aspect", True, "e.g. 16:9"),
                        ("audio", "Audio", True, "ambience, effects, dialogue, or none"),
                        ("negative", "Negative field", False, "unwanted elements")]},
}

# Words that show a slot is present, for the linter (English and Arabic).
SLOT_SIGNS = {
    "goal": r"^\s*(\W*\s*)?(write|create|build|make|draft|summari[sz]e|analy[sz]e|fix|review|translate|generate|design|plan|classify|extract|answer|compare|rewrite|convert|اكتب|أنشئ|ابن|اعمل|لخص|لخّص|حلل|حلّل|أصلح|راجع|ترجم|ولّد|صمم|صمّم|خطط|استخرج|قارن|حوّل)\b|<task>|^task:|المهمة",
    "audience": r"\baudience\b|\breader|\bfor (a|an|the|our|my) \w+|\busers?\b|decision|الجمهور|القارئ|للمستخدم|موجه",
    "context": r"\bbecause\b|\bso that\b|\bsince\b|\bcontext\b|<context>|background|\bwhy\b|لأن|عشان|حتى |السياق|الخلفية",
    "inputs": r"<(document|doc|input|data|source|example)s?\b|\battached\b|\bprovided\b|\bfile\b|\bbelow\b|المرفق|الملف|أدناه",
    "constraints": r"\bmust\b|\bonly\b|\bavoid\b|\bdo not\b|\bdon't\b|\bwithout\b|\bout of scope\b|\bnon-goals?\b|فقط|بدون|تجنب|لا ت",
    "output": r"\bformat\b|\bjson\b|\btable\b|\bmarkdown\b|\bbullet|\bsections?\b|\bwords?\b|\blines?\b|\bschema\b|<output|\breturn\b|\blength\b|صيغة|جدول|كلمة|سطر|أقسام|بصيغة",
    "success": r"\bdone when\b|\bsuccess\b|\bcriteria\b|\bpass(es)?\b|\bverify\b|\bcheck\b|\btests? (pass|green)|\bacceptance\b|معيار|يتحقق|تحقق|ينجح|الاختبار",
    "uncertainty": r"\bif (you are )?(unsure|uncertain|unclear|missing)\b|\bask\b|\bassum|\bnull\b|\bunknown\b|إذا لم|لو مش|اسأل|افترض",
    "examples": r"<example|\bexample:|\be\.g\.|\bfor example\b|مثال|مثلا|مثلًا",
    "role": r"\byou are\b|\bas an?\b|\bassistant\b|\brole\b|أنت ",
    "tools": r"\btools?\b|\bapi\b|\bcommand\b|\brun\b|\bcall\b|أداة|أدوات|نفّذ",
    "stop": r"\bstop\b|\bhalt\b|\bescalate\b|\breport back\b|\bbefore (deleting|publishing|pushing)\b|توقف|ارجع لي",
    "budget": r"\bbudget\b|\bat most\b|\bminutes?\b|\btokens?\b|\bunder \d+|ميزانية|بحد أقصى",
    "state": r"\bstate\b|\bprogress\b|\breceipt|\blog\b|سجل|إيصال",
    "repo": r"\bpython\b|\bnode\b|\btypescript\b|\bjavascript\b|\brepo\b|\bfile\b|\bversion\b|\.py\b|\.ts\b|\.js\b",
    "tests": r"\btests?\b|pytest|unittest|npm test|\bci\b|اختبار",
    "nongoals": r"\bnon-goals?\b|\bdo not (touch|change|refactor)\b|\bout of scope\b|لا تلمس|خارج النطاق",
    "sources": r"\bsources?\b|\bcite|\bcitation|\breferences?\b|\bsince \d{4}\b|مصادر|مصدر|استشهد",
    "claims": r"\bunverified\b|\bconflict|\bconfidence\b|غير مؤكد|تعارض",
    "voice": r"\bvoice\b|\btone\b|\bregister\b|\bdialect\b|\bstyle\b|نبرة|أسلوب|لهجة|مصري|فصحى",
    "length": r"\b\d+\s*(words?|seconds?|lines?|sentences?)\b|\d+\s*(كلمة|ثانية|سطر|جملة)",
    "tone": r"\btone\b|\bregister\b|\bdialect\b|نبرة|لهجة",
    "rubric": r"\brubric\b|\bcriteri|معايير|معيار",
    "labels": r"\bPASS\b|\bFAIL\b|\b[1-5]\s*-\s*[1-5]\b|\blabels?\b|تسمية",
    # visual
    "subject": r"\b(a|an|the|one|two|young|old)\s+\w+|شخص|رجل|امرأة|طفل|قطة",
    "action": r"\w+ing\b|يجري|يمشي|يقف|يجلس|يحمل|ينظر",
    "environment": r"\bin (a|an|the)\b|\bat (dawn|dusk|night|noon|sunset|sunrise)\b|\b(street|room|forest|desert|city|studio|beach|kitchen)\b|في |شارع|غرفة|صحراء|مدينة",
    "shot": r"\b(close-?up|medium|wide|full|aerial|overhead|low|high)[ -]?(shot|angle)?\b|\b\d{2,3}\s?mm\b|لقطة|عدسة",
    "light": r"\blight|\blit\b|\bsun|\bglow|\bbacklit|\brim\b|\bshadow|إضاءة|ضوء|شمس",
    "style": r"\bstyle\b|\bpalette\b|\bcolou?rs?\b|\bwatercolou?r|\bink\b|\bmatte\b|\bcinematic\b|\bpastel|\bmonochrome|أسلوب|ألوان|لوحة",
    "text": r"[\"“«][^\"”»]{1,80}[\"”»]",
    "lock": r"\block\b|\bsame (character|style)\b|\bconsistent\b|ثابت|نفس الشخصية",
    "aspect": r"\b\d{1,2}:\d{1,2}\b|\baspect\b|\bportrait\b|\blandscape\b|\bsquare\b",
    "negative": r"\bnegative\b|سلبي",
    "camera": r"\b(static|pan|tilt|dolly|truck|crane|orbit|handheld|tracking|push[- ]in|pull[- ]out)\b|كاميرا",
    "duration": r"\b\d+(\.\d+)?\s*(s|sec|seconds?)\b|ثوان|ثانية",
    "audio": r"\baudio\b|\bsound\b|\bambien|\bdialogue\b|\bsilent\b|صوت|حوار",
}

VAGUE = r"\b(some|stuff|things|etc|better|nice|good|great|amazing|awesome|cool|kind of|sort of|various|appropriate|properly)\b|إلخ|حلو|جامد|شوية|كويس|حاجة|حاجات|مناسب"
HYPE = r"\b(8k|4k|16k|masterpiece|ultra[- ]?detailed|hyper[- ]?realistic|award[- ]winning|trending on artstation|best quality|highly detailed|octane render|unreal engine 5)\b"
SHOUT = r"\b(CRITICAL|IMPORTANT|MUST|NEVER|ALWAYS|ABSOLUTELY|DO NOT)\b"
COT_EXPOSE = r"(think step[- ]by[- ]step and (show|print|write out)|show (me )?your (full )?(reasoning|chain[- ]of[- ]thought)|print your (reasoning|thoughts))"
NEGATIVE = r"\b(don't|do not|never|no|avoid|without)\b|(^|\s)لا\s|ممنوع|تجنب"
PLACEHOLDER = r"\{\{[^}]+\}\}|\[(TODO|TBD|INSERT[^\]]*)\]|<insert[^>]*>|\bXXX\b|\bلاحقا\b"
SECRET = r"(sk-[A-Za-z0-9_-]{16,}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|xox[bap]-[A-Za-z0-9-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|AIza[0-9A-Za-z_-]{30,})"
LIVING_ARTIST = r"\bin the style of [A-Z][a-z]+ [A-Z][a-z]+"
PERSONA_THEATRE = r"\b(world[- ]class|the best .{0,20} in the world|10x|genius|legendary)\b"


def rx(p: str) -> re.Pattern:
    return re.compile(p, re.I | re.M)


def found(pattern: str, text: str) -> list:
    return [m.group(0) for m in rx(pattern).finditer(text)]


def lint(text: str, kind: str) -> dict:
    """Score a prompt 0-20 with hard gates. A proxy for the PROMPT-14 rubric: it reads only what text can show."""
    spec = KINDS[kind]
    slots = [s for s in spec["slots"]]
    present = {s[0]: bool(rx(SLOT_SIGNS.get(s[0], r"(?!x)x")).search(text)) for s in slots}
    findings, gates = [], []

    def add(level, code, msg, fix):
        findings.append({"level": level, "code": code, "message": msg, "fix": fix})

    for name, label, required, hint in slots:
        if required and not present[name]:
            add("warn", f"slot:{name}", f"missing slot: {label}", f"add {label.lower()}: {hint}")
    # gates (any one fails the prompt)
    if found(SECRET, text):
        gates.append("secret in the prompt")
    if found(COT_EXPOSE, text):
        gates.append("asks the model to print its chain of thought")
    if len(text) > 1500 and not rx(r"<[a-z_]+>|```").search(text):
        gates.append("long pasted material with no tags or fences: data is not separated from instructions")
    for g in gates:
        add("gate", "gate", g, "remove it" if "secret" in g else ("ask for the answer and a short rationale instead" if "chain" in g
                                                                   else "wrap the material in <document> tags and put the ask after it"))
    # anti-patterns
    vague = sorted({w.lower() for w in found(VAGUE, text)})
    if vague:
        add("warn", "vague", "vague words: " + ", ".join(vague[:8]), "replace each with a measurable property")
    shout = found(SHOUT, text)
    if len(shout) >= 2:
        add("warn", "shouting", f"{len(shout)} shouted words ({', '.join(sorted(set(shout))[:5])})",
            "state the rule calmly with its reason; capitals make models over-apply rules")
    neg, lines = len(found(NEGATIVE, text)), max(1, len([l for l in text.splitlines() if l.strip()]))
    pos = len(found(r"\b(write|use|keep|return|include|give|put|start|end|make|اكتب|استخدم|احتفظ|أرجع|ضع|ابدأ)\b", text))
    if neg >= 4 and neg > pos:
        add("warn", "negative-heavy", f"{neg} negative rules vs {pos} positive directives",
            "say what to do; keep a 'don't' only where the default would be wrong")
    ph = found(PLACEHOLDER, text)
    if ph:
        add("warn", "placeholder", "unfilled placeholders: " + ", ".join(sorted(set(ph))[:5]), "fill them or mark them as questions")
    dup = [l for l in {l.strip() for l in text.splitlines() if len(l.strip()) > 25}
           if [x.strip() for x in text.splitlines()].count(l) > 1]
    if dup:
        add("warn", "duplicate", f"{len(dup)} duplicated line(s)", "keep each rule once")
    if found(PERSONA_THEATRE, text):
        add("info", "persona", "persona theatre (world-class, genius …)", "describe the job and the standard instead")
    if spec["visual"]:
        hype = sorted({w.lower() for w in found(HYPE, text)})
        if hype:
            add("warn", "hype", "hype tokens: " + ", ".join(hype), "replace with visible properties (light, lens, material)")
        if found(LIVING_ARTIST, text):
            add("warn", "artist", "imitates a named artist", "describe the visible properties of the style instead")
        if rx(r"\bno [a-z]+").search(text) and not present.get("negative"):
            add("info", "inline-negative", "'no X' inside the positive prompt", "move it to the negative field or write the positive replacement")
    # score: 20 points spread over required slots (14) and hygiene (6)
    req = [s[0] for s in slots if s[2]]
    slot_pts = round(14 * sum(present[s] for s in req) / max(1, len(req)))
    hygiene = 6 - min(6, sum(1 for f in findings if f["level"] == "warn" and not f["code"].startswith("slot:")))
    score = slot_pts + hygiene
    band = "fail-gate" if gates else ("ship" if score >= 16 else ("fix-lowest" if score >= 12 else "rewrite"))
    return {"kind": kind, "score": score, "of": 20, "band": band, "gates": gates,
            "slots": {k: v for k, v in present.items()}, "findings": findings, "chars": len(text), "lines": lines,
            "limits": "Heuristic proxy: it sees whether slots and anti-patterns appear in the text, not whether the prompt works. Prove with `eval`."}


def build(kind: str, goal: str, values: dict, lang: str = "en", only: set = None) -> str:
    """Render the kind's slots in order; an unfilled required slot becomes a [[...]] question. `only` limits the slots."""
    spec = dict(KINDS[kind])
    if only is not None:
        spec["slots"] = [s for s in spec["slots"] if s[0] in only]
    vals = dict(values, goal=goal) if goal else dict(values)
    if spec["visual"]:
        parts = []
        for name, label, required, hint in spec["slots"]:
            if name in ("negative",):
                continue
            v = vals.get(name)
            if v:
                parts.append(v.strip().rstrip("."))
            elif required:
                parts.append(f"[[{label}: {hint}]]")
        if goal and not vals.get("subject"):
            parts.insert(0, goal.strip().rstrip("."))
        line = ". ".join(parts) + "."
        if kind == "video" and vals.get("audio") and not line.lower().count("audio:"):
            line = line.replace(vals["audio"].strip().rstrip("."), "Audio: " + vals["audio"].strip().rstrip("."))
        out = [line]
        if vals.get("negative"):
            out.append("Negative: " + vals["negative"])
        return "\n".join(out) + "\n"
    L = []
    for name, label, required, hint in spec["slots"]:
        v = vals.get(name)
        tag = name if name != "goal" else "task"
        if v:
            L.append(f"<{tag}>\n{v.strip()}\n</{tag}>")
        elif required:
            ask = f"[[ask or assume and state: {hint}]]" if lang == "en" else f"[[اسأل أو افترض واذكر الافتراض: {hint}]]"
            L.append(f"<{tag}>\n{ask}\n</{tag}>")
    if lang == "ar":
        L.append("<language>\nاكتب الناتج بالعربية بنفس لهجة الطلب، واحتفظ بالأرقام والأسماء والروابط كما هي.\n</language>")
    return "\n\n".join(L) + "\n"


def refine(text: str, kind: str) -> dict:
    rep = lint(text, kind)
    order = {"gate": 0, "warn": 1, "info": 2}
    fixes = sorted(rep["findings"], key=lambda f: (order[f["level"]], f["code"]))
    missing = {s[0] for s in KINDS[kind]["slots"] if s[2] and not rep["slots"].get(s[0])}
    return {"lint": {k: rep[k] for k in ("score", "of", "band", "gates")}, "fixes": [f"{f['level']}: {f['fix']} ({f['message']})" for f in fixes],
            "skeleton": build(kind, "", {}, only=missing) if missing else "", "keep": "Merge the original text into the skeleton; keep every number, name, path and quoted string verbatim (PROMPT-02)."}


# ---------------------------------------------------------------------------------------------------------------
# Eval: assertion matrix over saved outputs (PROMPT-34) and keep-or-revert (PROMPT-15)
def check_assert(a: dict, out: str) -> bool:
    t, v = a.get("type"), a.get("value")
    if t == "contains":
        return str(v) in out
    if t == "icontains":
        return str(v).lower() in out.lower()
    if t == "not-contains":
        return str(v) not in out
    if t == "regex":
        return re.search(str(v), out, re.M) is not None
    if t == "not-regex":
        return re.search(str(v), out, re.M) is None
    if t == "starts-with":
        return out.lstrip().startswith(str(v))
    if t == "max-chars":
        return len(out) <= int(v)
    if t == "min-chars":
        return len(out) >= int(v)
    if t == "is-json":
        try:
            json.loads(out)
            return True
        except ValueError:
            return False
    if t == "json-keys":
        try:
            obj = json.loads(out)
        except ValueError:
            return False
        return isinstance(obj, dict) and all(k in obj for k in v)
    if t == "equals":
        return out.strip() == str(v).strip()
    raise ValueError(f"unknown assertion type: {t}")


def evaluate(cases: list, outputs: dict, baseline: str = "") -> dict:
    table = {}
    for variant, outs in outputs.items():
        row = {}
        for c in cases:
            o = outs.get(c["id"])
            row[c["id"]] = None if o is None else all(check_assert(a, o) for a in c.get("assert", []))
        table[variant] = row
    totals = {v: sum(1 for x in r.values() if x) for v, r in table.items()}
    verdict = {}
    if baseline and baseline in table:
        for v, r in table.items():
            if v == baseline:
                continue
            regress = [cid for cid, ok in table[baseline].items() if ok and not r.get(cid)]
            gain = totals[v] - totals[baseline]
            verdict[v] = {"gain": gain, "regressions": regress,
                          "keep": gain > 0 and not regress,
                          "reason": ("wins with no regressions" if gain > 0 and not regress else
                                     f"regresses on {', '.join(regress)}" if regress else "no gain over the baseline")}
    return {"cases": len(cases), "pass": table, "totals": totals, "baseline": baseline, "verdict": verdict}


def pairwise(verdicts: list) -> dict:
    """Each item: {case, first: 'A'|'B'|'tie' (A shown first), second: 'A'|'B'|'tie' (B shown first, answer names the
    variant, not the position)}. A case counts only when both orders agree (Jev's order-robust rule)."""
    agree, split, tally = [], [], {"A": 0, "B": 0, "tie": 0}
    for v in verdicts:
        if v["first"] == v["second"]:
            agree.append(v["case"])
            tally[v["first"]] += 1
        else:
            split.append(v["case"])
    winner = "A" if tally["A"] > tally["B"] else "B" if tally["B"] > tally["A"] else "none"
    return {"cases": len(verdicts), "agreeing": len(agree), "position_bias_cases": split, "tally": tally, "winner": winner,
            "stable": bool(verdicts) and len(split) <= len(verdicts) // 4,
            "note": "A winner is reported only from cases where both orders agree; more than a quarter split means the judge is unreliable here."}


def judge_plan(a: str, b: str, task: str) -> str:
    def one(x, y, nx, ny):
        return (f"<task>\n{task}\n</task>\n\n<response_1>\n{x}\n</response_1>\n\n<response_2>\n{y}\n</response_2>\n\n"
                f"Which response better completes the task? Judge only the task's success criteria, not length or style. "
                f"Answer with one line: '1', '2' or 'tie', then one sentence of reason.\n"
                f"(record: response_1 = {nx}, response_2 = {ny})")
    return "=== judge call 1 (A first) ===\n" + one(a, b, "A", "B") + "\n\n=== judge call 2 (B first) ===\n" + one(b, a, "B", "A") + "\n"


# ---------------------------------------------------------------------------------------------------------------
def read_text(p: str) -> str:
    return sys.stdin.read() if p == "-" else Path(p).read_text(encoding="utf-8")


def self_test() -> int:
    bad = []
    weak = "Make a nice image of a cat, 8k, masterpiece, ultra detailed."
    strong = ("A ginger cat sitting on a wooden windowsill, watching rain. In a small kitchen at dusk. Medium close-up, 50mm, "
              "eye level. Warm light from a lamp on the left, cool rim light from the window. Soft watercolour style, muted "
              "amber and slate palette. Aspect 4:5.")
    w, s = lint(weak, "image"), lint(strong, "image")
    if not (s["score"] > w["score"] and s["band"] == "ship" and any(f["code"] == "hype" for f in w["findings"])):
        bad.append(("image lint", w["score"], s["score"], s["band"]))
    if lint("Use key sk-abcdefghijklmnopqrstuvwx to call the API", "agent")["band"] != "fail-gate":
        bad.append("secret gate")
    if lint("Think step by step and show your reasoning. Summarise the report.", "writing")["band"] != "fail-gate":
        bad.append("cot gate")
    agent = ("Fix the failing date parser in utils/dates.py so that imports from Excel keep the day first, because our users are in "
             "Egypt. The audience is the maintainers reviewing the PR. Context: CSV files come from Excel with dd/mm/yyyy. Only touch "
             "utils/dates.py. Return a unified diff and a two-line summary. Done when python3 -m unittest tests.test_dates passes. "
             "If the format is ambiguous, ask one question. Tools: you may run the tests; stop and report before pushing. Budget: at most 20 minutes.")
    a = lint(agent, "agent")
    if a["band"] != "ship":
        bad.append(("agent lint", a["score"], [f["message"] for f in a["findings"]]))
    ar = lint("اكتب ملخصًا من 100 كلمة لتقرير المبيعات المرفق للمدير لأن القرار يوم الأحد. الصيغة: ثلاث نقاط. معيار النجاح: كل رقم كما هو.", "writing")
    if not ar["slots"]["goal"] or not ar["slots"]["output"]:
        bad.append(("arabic slots", ar["slots"]))
    b = build("video", "", {"shot": "Wide shot, low angle", "subject": "a fisherman", "action": "pulling a net",
                            "environment": "on a wooden boat at sunrise", "camera": "slow dolly in", "style": "warm golden light from the right",
                            "duration": "6 seconds", "aspect": "16:9", "audio": "waves and gulls, no music", "negative": "text, watermark"})
    if "Audio: waves" not in b or "Negative: text" not in b or lint(b, "video")["band"] != "ship":
        bad.append(("video build", b, lint(b, "video")["score"]))
    sk = build("agent", "Rename the config key", {})
    if "[[ask or assume" not in sk or "<stop>" not in sk:
        bad.append("agent skeleton")
    rf = refine("Write a blog post about AI for our customers. Make it good.", "writing")
    if "<task>" in rf["skeleton"] or "<voice>" not in rf["skeleton"]:
        bad.append(("refine skeleton", rf["skeleton"]))
    cases = [{"id": "c1", "assert": [{"type": "is-json"}]}, {"id": "c2", "assert": [{"type": "contains", "value": "42"}]},
             {"id": "c3", "assert": [{"type": "max-chars", "value": 10}]}]
    ev = evaluate(cases, {"A": {"c1": "{}", "c2": "no", "c3": "short"}, "B": {"c1": "{\"a\":1}", "c2": "42", "c3": "short"},
                          "C": {"c1": "{}", "c2": "42", "c3": "far too long text"}}, baseline="A")
    if not (ev["verdict"]["B"]["keep"] and not ev["verdict"]["C"]["keep"] and ev["verdict"]["C"]["regressions"] == ["c3"]):
        bad.append(("eval", ev["verdict"]))
    pw = pairwise([{"case": 1, "first": "B", "second": "B"}, {"case": 2, "first": "A", "second": "B"},
                   {"case": 3, "first": "B", "second": "B"}, {"case": 4, "first": "B", "second": "B"}])
    if pw["winner"] != "B" or pw["position_bias_cases"] != [2] or not pw["stable"]:
        bad.append(("pairwise", pw))
    if "B first" not in judge_plan("x", "y", "t"):
        bad.append("judge plan")
    if lint(strong, "image") != lint(strong, "image"):
        bad.append("determinism")
    for x in bad:
        print("FAIL", x)
    print("self-test OK" if not bad else f"self-test: {len(bad)} failure(s)")
    return 1 if bad else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--self-test", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("kinds")
    b = sub.add_parser("build")
    b.add_argument("--kind", choices=sorted(KINDS), required=True)
    b.add_argument("--goal", default="")
    b.add_argument("--set", action="append", default=[], metavar="SLOT=VALUE")
    b.add_argument("--lang", choices=["en", "ar"], default="en")
    for name in ("lint", "refine"):
        p = sub.add_parser(name)
        p.add_argument("file", help="prompt file, or - for stdin")
        p.add_argument("--kind", choices=sorted(KINDS), required=True)
        p.add_argument("--json", action="store_true")
    e = sub.add_parser("eval")
    e.add_argument("--cases", required=True)
    e.add_argument("--outputs", required=True)
    e.add_argument("--baseline", default="")
    pw = sub.add_parser("pairwise")
    pw.add_argument("--verdicts")
    pw.add_argument("--plan", action="store_true")
    pw.add_argument("--a")
    pw.add_argument("--b")
    pw.add_argument("--task", default="")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if a.cmd == "kinds":
        for k, spec in KINDS.items():
            print(f"{k:<9} {spec['about']}")
            print("          slots: " + ", ".join(s[0] + ("*" if s[2] else "") for s in spec["slots"]))
        print("(* = required)")
        return 0
    if a.cmd == "build":
        vals = {}
        for kv in a.set:
            k, _, v = kv.partition("=")
            vals[k.strip()] = v
        print(build(a.kind, a.goal, vals, a.lang), end="")
        return 0
    if a.cmd == "lint":
        rep = lint(read_text(a.file), a.kind)
        if a.json:
            print(json.dumps(rep, ensure_ascii=False, indent=1))
        else:
            print(f"{rep['kind']}: {rep['score']}/20 → {rep['band']}" + (f"  gates: {'; '.join(rep['gates'])}" if rep["gates"] else ""))
            for f in rep["findings"]:
                print(f"  {f['level']:<5} {f['message']}  → {f['fix']}")
            print("  " + rep["limits"])
        return 1 if rep["band"] in ("fail-gate", "rewrite") else 0
    if a.cmd == "refine":
        rep = refine(read_text(a.file), a.kind)
        if a.json:
            print(json.dumps(rep, ensure_ascii=False, indent=1))
        else:
            print(f"{rep['lint']['score']}/20 → {rep['lint']['band']}")
            for i, f in enumerate(rep["fixes"], 1):
                print(f"{i}. {f}")
            if rep["skeleton"]:
                print("\nmissing slots to add:\n" + rep["skeleton"])
            print(rep["keep"])
        return 0
    if a.cmd == "eval":
        rep = evaluate(json.loads(read_text(a.cases)), json.loads(read_text(a.outputs)), a.baseline)
        print(json.dumps(rep, ensure_ascii=False, indent=1))
        return 0
    if a.cmd == "pairwise":
        if a.plan:
            if not (a.a and a.b):
                ap.error("--plan needs --a and --b")
            print(judge_plan(read_text(a.a), read_text(a.b), a.task), end="")
            return 0
        if not a.verdicts:
            ap.error("pairwise needs --verdicts or --plan")
        print(json.dumps(pairwise(json.loads(read_text(a.verdicts))), ensure_ascii=False, indent=1))
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
